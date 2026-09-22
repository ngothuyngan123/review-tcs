# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #39668 — journal **#129182** (AI LME Fix bug, 2026-08-18). Journal **#129183** là **bản trùng nội dung y hệt** của #129182, không có thông tin mới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME (hệ thống tự động)` — assignee Redmine: `Ngô Thúy Ngần` |
| Commit / Pull Request | `<chưa có PR>` — commit `dd76d969c4` (2 file). Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=39668 |
| Branch | `ai_small_39668` (repo `sns-line`, nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | `2026-08-18` |
| Auto-filled | `2026-09-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Với các giao dịch thẻ qua cổng thanh toán UnivaPay, nơi DUY NHẤT ghi bản ghi lịch sử thanh toán là webhook báo hoàn tất giao dịch (`charge_finished`). Webhook này không có cơ chế chống xử lý lặp: mỗi lần cổng thanh toán gửi lại cùng một sự kiện (cổng tự gửi lại khi phía LME xử lý lâu / không phản hồi kịp — riêng luồng gia hạn tự động còn gửi mail, cập nhật rich menu, ghi vòng đời hợp đồng nên rất dễ quá thời gian chờ), toàn bộ **5 nhánh xử lý thành công** đều chèn THÊM một bản ghi mới mang đúng mã giao dịch cũ. Vì vậy trang lịch sử thanh toán - biên lai hiện 2 dòng cùng một ID thanh toán, trong khi trên cổng thanh toán chỉ có duy nhất một giao dịch (không hề bị trừ tiền 2 lần). Cùng cơ chế đó còn **nhân đôi bản ghi hoa hồng giới thiệu** và **có thể cộng dồn hạn hợp đồng thêm một kỳ**.

## 2. Cách fix

Sửa theo lỗi bắt buộc của AI review vòng 1: chốt chống trùng cũ chỉ ĐỌC `payment_histories` rồi mới ghi (check-then-write, không khoá) nên cửa sổ hở đúng bằng toàn bộ thời gian xử lý webhook (tới ~5 phút) — chính là lúc cổng thanh toán gửi lại, nên chưa chặn được kịch bản chính của ticket. Nay thay bằng **chốt NGUYÊN TỬ** đặt ngay đầu webhook, trước mọi nhánh xử lý:

1. Thêm bảng mới `univapay_webhook_processed` (migration `2026_08_18_000000`) có **ràng buộc DUY NHẤT** trên mã giao dịch.
2. Đầu `univapayCallback`, với event thành công, gọi `claimUnivaChargeEvent` — dùng **INSERT IGNORE** (thao tác nguyên tử của DB, không phụ thuộc kết nối nên đúng cả khi chạy nhiều web server): chỉ tiến trình ghi được dòng đánh dấu mới được xử lý tiếp; lần gửi lại chạy SONG SONG lúc lần đầu còn đang xử lý dở sẽ bị chặn ngay và **trả về 200 như cũ**.
3. Giữ hàm kiểm tra lịch sử thanh toán `isUnivaChargeRecorded` làm **lớp chốt thứ hai**.
4. Khối `catch` của webhook gọi `releaseUnivaChargeClaim` gỡ dấu đã nhận để lần gửi lại sau một lượt hỏng thật vẫn xử lý được — nhưng **CHỈ gỡ khi lịch sử thanh toán chưa được ghi**, tránh biến lỗi ghi trùng thành lỗi bỏ sót/ghi trùng lần nữa.
5. Trường hợp tiến trình chết đột ngột không chạy được `catch` (fatal error / bị kill): dấu **quá 900 giây** mà vẫn chưa ghi được lịch sử thì cho nhận lại bằng câu `UPDATE` có điều kiện thời gian (cũng nguyên tử).

**KHÔNG** đặt ràng buộc duy nhất trực tiếp lên `payment_histories.univa_charge_id` vì các bản ghi chia tháng **cố tình dùng chung** mã giao dịch.

⚠️ **LƯU Ý TRIỂN KHAI**: cần chạy migration tạo bảng mới khi deploy.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn danh sách "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN" của Dev, convert sang bảng. Cột "Thay đổi" suy từ mục 2 + mục 4.1 (chỉ BotController.php được sửa). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotController::univapayCallback` (app/Http/Controllers/Admin/BotController.php) | **SỬA** — thêm `claimUnivaChargeEvent` ở đầu webhook + `releaseUnivaChargeClaim` trong `catch` | Điểm vào duy nhất của webhook — nơi đặt chốt nguyên tử |
| 2 | `BotController::isUnivaChargeRecorded` (cùng file) | **THÊM MỚI** | Lớp chốt thứ hai — kiểm tra lịch sử thanh toán đã ghi chưa |
| 3 | `BotController::handleCallbackBillJob` | Đã check — không sửa | 1 trong 5 nhánh xử lý thành công (gia hạn tự động) |
| 4 | `BotController::handleCallbackPaymentCardSuccess` | Đã check — không sửa | 1 trong 5 nhánh (đăng ký mới / nâng gói) |
| 5 | `BotController::handleCallbackChangeCardSuccess` | Đã check — không sửa | 1 trong 5 nhánh (đổi thẻ / gia hạn / tái ký) |
| 6 | `BotController::handleCallbackBillAgainCardSuccess` | Đã check — không sửa | 1 trong 5 nhánh (thanh toán lại) |
| 7 | `BotController::handleExtendContractSuccess` | Đã check — không sửa | Nhánh gia hạn hợp đồng — nguy cơ cộng dồn hạn thêm 1 kỳ |
| 8 | `BotController::handleCallbackBillMaxFriendSuccess` | Đã check — không sửa | 1 trong 5 nhánh (thanh toán theo số bạn bè) |
| 9 | `Basic\UserController::ajaxPaymentHistories` (app/Http/Controllers/Basic/UserController.php) | Đã check — không sửa | Nguồn dữ liệu màn 支払履歴 — nơi khách thấy dòng trùng |
| 10 | `PaymentHistories::scopeTypeBill / scopeFilterDate / scopeFilterContractIds` (app/PaymentHistories.php) | Đã check — không sửa | Bộ lọc hiển thị: chỉ bản ghi cha (`parent_month=1`) mới hiện |
| 11 | `PointSettingController::changePaymentMethod / extendContract / billTransferUnivapayContract` (app/Http/Controllers/PointSettingController.php) | Đã check — không sửa | Nhánh **chuyển khoản** tạo bản ghi TRƯỚC — không được chặn nhầm |
| 12 | `AutoPaymentJobUnivapay::handle` (app/Console/Commands/AutoPaymentJobUnivapay.php) | Đã check — không sửa | Xác nhận job **KHÔNG** tự ghi lịch sử (có `continue` trước phần ghi = code chết) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev chỉ kê "File thay đổi" ở mục 4.1 (1 file). F2+ suy từ mục 3 — giữ NGUYÊN nội dung Dev, chỉ gán tag để /review-tc map coverage. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `univapayCallback` — webhook `POST /univapay/get-callback-webhook` | app/Http/Controllers/Admin/BotController.php | **Direct** | **File DUY NHẤT Dev kê ở mục 4.1.** Thêm chốt nguyên tử ở đầu webhook + gỡ dấu trong `catch` |
| F2 | `claimUnivaChargeEvent` / `releaseUnivaChargeClaim` — hàm mới | app/Http/Controllers/Admin/BotController.php | **Direct** | INSERT IGNORE + UPDATE có điều kiện 900 giây |
| F3 | `isUnivaChargeRecorded` — hàm mới | app/Http/Controllers/Admin/BotController.php | **Direct** | Lớp chốt thứ hai |
| F4 | 5 nhánh xử lý thành công: `handleCallbackBillJob` · `handleCallbackPaymentCardSuccess` · `handleCallbackChangeCardSuccess` · `handleCallbackBillAgainCardSuccess` · `handleCallbackBillMaxFriendSuccess` · `handleExtendContractSuccess` | app/Http/Controllers/Admin/BotController.php | **Indirect** | Không sửa code nhưng **bị chặn từ lần gửi lại thứ 2** — phải verify lần gửi ĐẦU vẫn chạy đủ |
| F5 | `Basic\UserController::ajaxPaymentHistories` | app/Http/Controllers/Basic/UserController.php | **Indirect** | Màn khách hàng thấy dòng trùng — không sửa code |
| F6 | `PaymentHistories::scopeTypeBill / scopeFilterDate / scopeFilterContractIds` | app/PaymentHistories.php | **Indirect** | Bộ lọc `parent_month=1` — quyết định dòng nào hiện |
| F7 | `PointSettingController::changePaymentMethod / extendContract / billTransferUnivapayContract` | app/Http/Controllers/PointSettingController.php | **Indirect** | Luồng **chuyển khoản** — rủi ro bị chốt chặn nhầm |
| F8 | `AutoPaymentJobUnivapay::handle` | app/Console/Commands/AutoPaymentJobUnivapay.php | **Indirect** | Dev xác nhận KHÔNG ghi lịch sử (code chết sau `continue`) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `payment_histories` | CREATE (chặn thêm) | Không tạo thêm bản ghi trùng `univa_charge_id`. ⚠️ **Dữ liệu cũ đã trùng vẫn còn, cần rà và dọn thủ công** |
| D2 | `payment_detail_aff` | CREATE (chặn thêm) | Không tạo thêm bản ghi hoa hồng trùng cho cùng một giao dịch |
| D3 | `bot_contracts.expired_date_contract` / `bot_contracts.status_payment` | UPDATE (chặn lặp) | Không bị cập nhật lặp lần 2 cho cùng một giao dịch (rủi ro cộng dồn hạn thêm 1 kỳ) |
| D4 | `univapay_webhook_processed` — **bảng MỚI** | MIGRATE + CREATE + UPDATE + DELETE | Migration `2026_08_18_000000`, unique index trên mã giao dịch. ⚠️ **Dev không kê ở mục 4.2** — suy từ mục 2. Chưa chạy migration → webhook lỗi bảng không tồn tại |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Contract Plan & Payment (FA-031)** — trang lịch sử thanh toán・biên lai của LOA không còn hiện trùng ID thanh toán | F1, F5, F6, D1 | **High** |
| T2 | **Payment History (FS-009)** — màn quản trị lịch sử thanh toán đọc cùng bảng nên cũng hết dòng trùng | F5, F6, D1 | **High** |
| T3 | **Affiliate Reward Program (FA-027)** — chặn nhân đôi bản ghi hoa hồng giới thiệu khi cổng gửi lại thông báo | F1, F4, D2 | **High** |
| T4 | **Affiliate Payment Mgmt (FS-013)** — cùng nguồn dữ liệu hoa hồng | F1, F4, D2 | **High** |

---

## Phụ lục — nguyên văn từ Redmine (mục 5 / 6 / TỰ REVIEW)

> Không nằm trong 4 mục chuẩn của template nhưng là **input bắt buộc** để viết TC — giữ nguyên văn.

### ■ 5. RECOVER DATA

⚠ **CÓ** — Bản ghi trùng đã phát sinh trước khi có chốt này vẫn nằm trong dữ liệu, nên trang lịch sử của khách TY-11918 vẫn hiện 2 dòng cho tới khi dọn. Cần rà `payment_histories` tìm các mã giao dịch có nhiều hơn 1 bản ghi cha hiển thị được, đối chiếu với cổng thanh toán (chỉ 1 giao dịch thật) rồi xoá/ẩn bản ghi thừa; rà kèm `payment_detail_aff` để tránh chi trả hoa hồng 2 lần, và kiểm tra hạn hợp đồng có bị cộng dư một kỳ không. Việc dọn dữ liệu do người phụ trách thực hiện, **KHÔNG nằm trong phạm vi thay đổi code này**. (phạm vi: `payment_histories`, `payment_detail_aff`, `bot_contracts.expired_date_contract` — các hợp đồng có mã giao dịch UnivaPay trùng)

### ■ 6. VERIFY (Dev đã làm được tới đâu)

- **Mức: `lint`** (chỉ kiểm tra cú pháp — KHÔNG chạy thực tế).
- Lệnh: `php -l app/Http/Controllers/Admin/BotController.php`: No syntax errors detected; `git diff --stat aca920ce...ai_small_39668`: 1 file changed, 40 insertions(+) — đúng phạm vi; `git merge-base --is-ancestor <đỉnh release>`: OK, commit nằm đúng trên `release_step_20260805`.
- **Bằng chứng**: KHÔNG kết nối được MySQL dev (`host.docker.internal:3306` - Connection refused) nên **chưa dump được dữ liệu trùng thực tế**; kết luận dựa trên đọc code toàn bộ 5 nhánh ghi lịch sử của webhook. Bộ lọc hiển thị của màn (`PaymentHistories::scopeTypeBill` + `scopeFilterDate`) cho thấy chỉ bản ghi cha (`parent_month=1`) mới hiện, nên **12 bản ghi con chia tháng KHÔNG phải nguyên nhân trùng** — chỉ 2 bản ghi cha cùng mã giao dịch mới gây trùng. `AutoPaymentJobUnivapay` nhánh charge thành công có lệnh `continue` trước phần ghi lịch sử (code chết) ⇒ xác nhận **chỉ webhook ghi lịch sử** cho luồng gia hạn tự động.

### ■ TỰ REVIEW (AI) — Rủi ro / lưu ý khi test

Vòng refix 1: bỏ cách kiểm-tra-rồi-mới-ghi, chuyển sang giành quyền xử lý nguyên tử theo mã giao dịch (INSERT IGNORE vào bảng có unique index) đặt ở ĐẦU webhook, trước mọi nhánh — chặn được cả lần gửi lại chạy song song khi lượt đầu còn đang xử lý dở. Không dùng khoá phiên (`GET_LOCK`) theo tinh thần PlanLimitGuard/#39230 vì khoá gắn với connection dễ âm thầm mất tác dụng; INSERT IGNORE + unique index chạy đúng cả khi có nhiều web server. Giữ nguyên toàn bộ logic nghiệp vụ sẵn có, chỉ thêm 2 hàm private + 1 dòng gỡ dấu trong khối catch + 1 migration.

- Cần chạy migration tạo bảng `univapay_webhook_processed` khi deploy; **chưa chạy migration thì webhook sẽ ném lỗi bảng không tồn tại** (rơi vào catch, trả 200 failed) — đây là điểm bắt buộc lưu ý khi release.
- Nếu một lượt xử lý **chết đột ngột** (fatal error/timeout) sau khi đã đánh dấu, các lần gửi lại **trong vòng 900 giây sẽ bị bỏ qua**; sau 900 giây (và khi lịch sử thanh toán vẫn chưa ghi) hệ thống tự cho nhận lại. Chọn 900 giây vì dài hơn hẳn thời gian xử lý thực tế (màn chờ tối đa ~320 giây) nên không cắt ngang lượt đang chạy bình thường.
- Nếu lượt đầu **đã ghi được lịch sử thanh toán rồi mới lỗi giữa chừng**, dấu được GIỮ nên lần gửi lại bị bỏ qua (không ghi trùng) — đổi lại **phần việc còn dang dở sau điểm ghi lịch sử sẽ không được chạy lại**; đánh giá là đánh đổi đúng với yêu cầu của ticket, nhưng **cần người review xác nhận**.
- Chưa chạy thử được trên môi trường thật: MySQL dev không kết nối được từ container nên chỉ kiểm tra cú pháp (`php -l`) và dựng thử câu SQL của migration bằng grammar của Laravel.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
