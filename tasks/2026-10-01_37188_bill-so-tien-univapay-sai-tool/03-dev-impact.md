# 03 — Đánh giá ảnh hưởng từ Dev

<!-- Nguồn: Journal #133178 — AI LME Fix bug — 2026-08-27 (báo cáo AI AUTO-FIXBUG, ghi nguyên văn theo nội dung journal Redmine #37188). -->

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Ngô Thúy Ngần (assignee ticket)` — fix do AI Auto-fixbug LME sinh, chưa có Dev người review lại trong journal |
| Commit / Pull Request | `commit 8d8602963a` (không có link PR trong Redmine) |
| Branch | `sns-line: ai_fixbug_37188` (nhánh gốc `release_step_20260805`, 2 file, đã push) |
| Ngày submit đánh giá | `2026-08-27` |
| Auto-filled | `2026-10-01 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

**(1) Thu tiền định kỳ (bill_job)**: callback thanh toán của Univapay không dùng số tiền đã thu thật mà TÍNH LẠI tiền từ trạng thái hợp đồng ở thời điểm callback chạy. Job tạo giao dịch lúc 06:30 rồi thoát ngay, callback có thể tới muộn; nếu trong khoảng đó hợp đồng đổi kỳ thanh toán, đổi gói hoặc đổi số slot thì số tiền ghi nhận lệch hẳn số thực thu. Đúng ca báo lỗi: `116424 = 10780 x 0.9 x 12`, tức thu tiền kỳ THÁNG nhưng ghi nhận giá kỳ NĂM.

**(2) Hợp đồng lại (case bổ sung 2026-08-26)**: trong callback hợp đồng lại (`handleCallbackChangeCardSuccess`, `actionBill=recontractV2`), số tiền được tính ở ĐẦU hàm — tức TRƯỚC khi callback cập nhật gói và kỳ thanh toán mới lấy từ dữ liệu gửi kèm giao dịch — và luôn ép số kỳ = 1. Vì vậy khi khách hợp đồng lại và chuyển từ bill NĂM sang bill THÁNG, lịch sử thanh toán vẫn lưu số tiền kỳ NĂM của hợp đồng CŨ dù chỉ thu tiền tháng; hoa hồng affiliate, số tiền lần thu gần nhất và nhật ký vòng đời hợp đồng sai theo. Chiều ngược lại (tháng sang năm) cũng sai: lưu tiền tháng rồi vẫn chia thành 12 dòng.

## 2. Cách fix

**(1) Thu tiền định kỳ**: job gửi kèm số tiền thật vào dữ liệu đính kèm khi tạo giao dịch Univapay; callback thêm hàm lấy số tiền thực thu từ dữ liệu Univapay trả về (số đã thu, rồi số yêu cầu thu, rồi số gửi kèm) và dùng số đó thay cho số tính lại từ hợp đồng khi ghi lịch sử thanh toán, hoa hồng affiliate, số tiền lần thu gần nhất và nhật ký vòng đời; lệch số thì ghi log cảnh báo, không có số nào dùng được (giao dịch cũ) thì giữ nguyên cách tính cũ.

**(2) Hợp đồng lại (case bổ sung)**: tính LẠI số tiền SAU khi callback đã cập nhật gói và kỳ thanh toán mới cho hợp đồng (đúng số kỳ khách chọn với gói năm), rồi cũng ưu tiên số tiền thật đã charge trên Univapay, lệch thì ghi log cảnh báo. Số tiền mới này chảy vào cùng chỗ: lịch sử thanh toán (kể cả các dòng chia theo tháng của gói năm), hoa hồng affiliate, số tiền lần thu gần nhất và nhật ký vòng đời. Chỉ đặt trong nhánh hợp đồng lại nên đổi thẻ chính / thẻ phụ giữ nguyên hành vi cũ.

⚠ **Quét ngang (Dev tự nêu)**: còn 3 handler callback khác cùng kiểu tính lại tiền nhưng NGOÀI phạm vi ticket này — chỉ ghi nhận, KHÔNG fix.

**TỰ REVIEW (AI)**: Fix tối giản, tự chứa trên release — chỉ đổi NGUỒN của biến số tiền trong 2 callback (thu định kỳ và hợp đồng lại), không đụng hàm dùng chung `calculateSaleEnterprise` (nhiều màn/handler khác đang dùng) và không đổi luồng thu tiền / tính hạn hợp đồng. Có fallback 3 lớp nên giao dịch cũ (chưa có dữ liệu đính kèm) hoặc payload thiếu trường vẫn chạy y như trước. Phần hợp đồng lại đặt riêng trong nhánh `recontractV2` nên đổi thẻ chính / thẻ phụ không đổi hành vi.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Journal gốc chỉ liệt kê danh sách function (không ghi rõ per-function có sửa hay không). Cột "Thay đổi" bên dưới suy từ §4.1 "File thay đổi" (chỉ 2 file: AutoPaymentJobUnivapay.php + BotController.php) — function nằm NGOÀI 2 file đó mặc định "Đã check, không sửa". Tester verify lại khi đối chiếu diff thật. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AutoPaymentJobUnivapay::chargeUnivapayCardBots` (app/Console/Commands/AutoPaymentJobUnivapay.php) | Có sửa *(suy từ §4.1)* | Job thu tiền định kỳ bằng thẻ — gửi kèm số tiền thật vào dữ liệu đính kèm khi tạo giao dịch |
| 2 | `AutoPaymentJobUnivapay::chargeUnivapayTransferBots` (app/Console/Commands/AutoPaymentJobUnivapay.php) | Có sửa *(suy từ §4.1)* | Job thu tiền định kỳ bằng chuyển khoản — cùng file, cùng cơ chế gửi kèm số tiền thật |
| 3 | `BotController::univapayCallback` (app/Http/Controllers/Admin/BotController.php) | Có sửa *(suy từ §4.1)* | Callback chung Univapay — điểm nhận dữ liệu thực thu |
| 4 | `BotController::handleCallbackBillJob` (app/Http/Controllers/Admin/BotController.php) | Có sửa *(suy từ §4.1)* | Xử lý kết quả webhook thu tiền định kỳ — nơi ghi `payment_histories`/affiliate/`amount_payment`/`bot_life_cycle` bằng số tiền thực thu |
| 5 | `BotController::getUnivapayChargedAmount` (app/Http/Controllers/Admin/BotController.php) | Có sửa — hàm MỚI *(suy từ §4.1 + mô tả "callback thêm hàm lấy số tiền thực thu")* | Hàm helper lấy số tiền thực thu từ dữ liệu Univapay trả về (fallback 3 lớp) |
| 6 | `UnivapayPayment::chargeMoneyUnivapayJob` (app/Helpers/UnivapayPayment.php) | Đã check, không sửa | Hàm charge dùng chung — KHÔNG nằm trong 2 file thay đổi |
| 7 | `calculateSaleEnterprise` (app/Helpers/functions.php) | Đã check, không sửa (cố ý — xem TỰ REVIEW) | Hàm tính giá dùng chung, nhiều màn/handler khác đang dùng — đụng vào sẽ vượt phạm vi fix tối giản |
| 8 | `PointSettingController::changeTypePayment` (app/Http/Controllers/PointSettingController.php) | Đã check, không sửa | Đổi `contract_bill_type` NGAY khi user bấm — đây là NGUỒN GỐC của điều kiện race (trạng thái hợp đồng đổi trước khi callback tới), nhưng bản thân hàm không sửa |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `chargeUnivapayCardBots` / `chargeUnivapayTransferBots` | app/Console/Commands/AutoPaymentJobUnivapay.php | Direct | Job gửi kèm số tiền thật vào payload tạo giao dịch Univapay (thẻ + chuyển khoản) |
| F2 | `univapayCallback` / `handleCallbackBillJob` / `getUnivapayChargedAmount` (mới) | app/Http/Controllers/Admin/BotController.php | Direct | Callback thu tiền định kỳ — dùng số tiền thực thu thay vì tính lại từ hợp đồng |
| F3 | `handleCallbackChangeCardSuccess` (`actionBill=recontractV2`) | app/Http/Controllers/Admin/BotController.php | Direct | Case bổ sung — hợp đồng lại: tính lại số tiền SAU khi cập nhật gói/kỳ mới |
| F4 | `calculateSaleEnterprise` | app/Helpers/functions.php | Indirect | Hàm tính giá dùng chung — KHÔNG sửa, nhưng là nguồn công thức gây lệch số (bằng chứng số học của ticket) |
| F5 | `changeTypePayment` | app/Http/Controllers/PointSettingController.php | Indirect | Đổi kỳ thanh toán ngay khi user bấm — nguồn gốc điều kiện race khiến callback tính sai, KHÔNG sửa |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `payment_histories.amount` (dòng thu định kỳ, thẻ Univapay) | UPDATE (hành vi ghi, schema không đổi) | Ghi đúng số thực thu — các dòng chia 12 tháng của gói năm cũng theo số này |
| D2 | `payment_histories.amount` (dòng thu của hợp đồng lại) | UPDATE | Ghi đúng số tiền của hợp đồng HIỆN TẠI (đổi bill năm→tháng thì lưu tiền tháng, không còn lưu tiền năm) |
| D3 | `payment_detail_aff.amount` / `sub_amount` | UPDATE | Hoa hồng affiliate tính trên số tiền thực thu (cả 2 luồng: thu định kỳ + hợp đồng lại) |
| D4 | `bot_contracts.amount_payment` | UPDATE | Ảnh chụp số tiền lần thu gần nhất |
| D5 | `bot_life_cycle.data.amount` | UPDATE | Nhật ký thanh toán / hợp đồng lại |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Contract Plan & Payment (FA-031) — thu tiền định kỳ phí tool + hợp đồng lại | F1, F2, F3, D1, D2, D4 | High |
| T2 | Payment History (FS-009) — lịch sử thanh toán khớp số tiền cổng thanh toán thu | D1, D2, D5 | High — số tiền hiển thị trực tiếp cho khách/CS đối chiếu |
| T3 | Affiliate Payment Mgmt (FS-013) — hoa hồng affiliate | D3 | Medium — sai số tiền gốc kéo theo sai hoa hồng |

---

## 5. Recover data (bổ sung từ Dev — không thuộc 4 mục chuẩn nhưng bắt buộc đọc trước khi test)

⚠ **CÓ** — Các dòng `payment_histories` (và `payment_detail_aff` tương ứng) đã ghi sai số tiền TRONG QUÁ KHỨ vẫn đang sai — code chỉ chặn phát sinh mới. Ca trong ticket #37188 đã được "anh Tư" recover tay.

**Phạm vi recover**: đối chiếu `payment_histories.amount` (lọc `parent_month=1`) với số tiền thật của `univa_charge_id` bên Univapay cho các bản ghi `type_bill=2, type=1`; lệch thì sửa cả dòng cha, 12 dòng chia tháng, và `payment_detail_aff` cùng `univa_charge_id`.

## 6. Verify — mức Dev đã đạt được (bổ sung từ Dev)

- **Mức**: lint (chưa chạy test thực tế bằng dữ liệu thật)
- **Lệnh**: `php -l app/Http/Controllers/Admin/BotController.php` → No syntax errors detected; `php -l app/Console/Commands/AutoPaymentJobUnivapay.php` → No syntax errors detected; `git diff --stat origin/release_step_20260805...ai_fixbug_37188` → đúng 2 file, 38 thêm / 2 sửa
- **Bằng chứng (suy luận số học, KHÔNG phải kết quả chạy thật)**: Số học khớp chính xác — `calculateSaleEnterprise`: `standard_month = basic_fee = 10780`; `standard_year = basic_fee*0.9*12 = 116424` (đúng số trên ticket) ⇒ tool ghi giá kỳ NĂM cho 1 giao dịch thu kỳ THÁNG; `AutoPaymentJobUnivapay::chargeUnivapayCardBots` nhánh charge thành công có `continue` ⇒ job KHÔNG ghi `payment_histories` trực tiếp — nơi ghi thật là callback `handleCallbackBillJob` (khớp lessons #39668/#40049); `PointSettingController::changeTypePayment` đổi `contract_bill_type` sang kỳ mới NGAY khi user bấm ⇒ trạng thái hợp đồng lúc callback có thể khác lúc tạo charge.
- **Không kiểm chứng được bằng dữ liệu thật**: MySQL dev `host.docker.internal:3306` Connection refused (dev stack đang tắt).
- **Rủi ro Dev tự nêu**:
  - Tên trường `charged_amount`/`requested_amount` trong payload webhook Univapay CHƯA xác minh được bằng log thật (dev stack tắt); nếu Univapay không gửi thì fallback về số tiền hệ thống gắn kèm lúc tạo giao dịch — vẫn đúng, chỉ áp dụng cho giao dịch tạo SAU khi deploy.
  - Với hợp đồng lại, ngay cả khi không lấy được số của Univapay thì số tiền vẫn được tính lại theo hợp đồng SAU cập nhật nên case báo lỗi (năm sang tháng) được sửa cho mọi giao dịch, không phụ thuộc payload.
  - Ở luồng thu định kỳ, fix chỉ đồng bộ SỐ TIỀN. Kỳ thanh toán dùng để ghi reason/remain_day/chia 12 tháng của gói năm vẫn đọc kỳ thanh toán HIỆN TẠI, nên ca đổi kỳ giữa chừng bản ghi có thể mang nhãn kỳ năm với số tiền kỳ tháng — sửa tiếp phải đụng cách tính hạn hợp đồng nên cố ý để ngoài phạm vi.
  - Callback trùng (Univapay gửi lại) vẫn sinh dòng lịch sử trùng — đó là ticket #39668, chốt chống trùng nằm ở branch khác chưa lên release.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
