# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | `<chưa có PR — chỉ có commit trên branch, xem Branch>` |
| Branch | `sns-line: ai_fixbug_35578` (nhánh gốc `release_step_20260805`, commit `c0e9e042b7`, 1 file) — đã push lên origin |
| Ngày submit đánh giá | 2026-08-27 |
| Auto-filled | 2026-10-14 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (Journal #133250/#133251) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi bill phí theo lượng bạn bè thất bại rồi bấm bill lại và nhập thẻ mới, hàm xử lý bill ghi đè thẻ chính của hợp đồng bằng thẻ mới (mã khách, số thẻ 4 số cuối, hãng thẻ) nhưng không ghi bản ghi lịch sử đổi thẻ chính. Vì vậy màn lịch sử hợp đồng chỉ có dòng bill phí theo lượng bạn bè thành công, thiếu dòng đổi thẻ chính. Ở trạng thái bill lỗi, nút đổi thẻ chính trên màn chi tiết hợp đồng cũng bị ẩn nên đây là đường duy nhất đổi thẻ, dẫn tới mất hẳn vết đổi thẻ.

## 2. Cách fix

Trong luồng xử lý bill lại phí theo lượng bạn bè, sau khi bill thành công và đã ghi đè thẻ chính của hợp đồng bằng thẻ mới, bổ sung ghi thêm 1 bản ghi lịch sử đổi thẻ chính (loại 11) kèm gói, kỳ thanh toán, 4 số cuối thẻ mới và phương thức thanh toán thẻ. Điều kiện ghi dùng đúng cờ người dùng có nhập thẻ mới, khớp 1-1 với nhánh thực sự thay thẻ nên không sinh lịch sử thừa khi bill lại bằng thẻ cũ.

Yokoten: quét các chỗ khác ghi đè thẻ chính của hợp đồng, còn 1 chỗ cùng kiểu chưa sửa (**gia hạn hợp đồng nhập thẻ mới** — re-contract) — chỉ ghi nhận, **không sửa ngoài phạm vi ticket**.

Verify của Dev (mức lint, không reproduce được thật):
- `php -l app/Http/Controllers/PointSettingController.php`: No syntax errors detected.
- `git diff --stat origin/release_step_20260805...ai_fixbug_35578`: 1 file, +16 dòng.
- Không chạy PHPUnit (fix nằm ở Controller, không thuộc `app/Services`/`app/Helpers`, phụ thuộc request/DB).
- Không tái hiện được trên dev: MySQL `host.docker.internal:3306` connection refused, và kịch bản cần bot trên 100.000 bạn + tài khoản Univapay thật. Dev confirm fix qua đọc code + schema, **chưa có bằng chứng chạy thật**.
- Data: **không cần recover data**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `PointSettingController::acceptBillMaxFriendV2` (`app/Http/Controllers/PointSettingController.php`) | **Đã sửa** — nơi bill lại + ghi đè thẻ chính, bổ sung ghi lịch sử | Root cause — thiếu `BotLifeCycle::addState` sau khi ghi đè thẻ |
| 2 | `PointSettingController::changeCard` (`app/Http/Controllers/PointSettingController.php`) | Không sửa | Luồng đổi thẻ chính chuẩn — dùng làm mẫu dữ liệu lịch sử cho fix |
| 3 | `BotController::handleCallbackBillMaxFriendSuccess` (`app/Http/Controllers/Admin/BotController.php`) | Không sửa | Callback bill phí theo lượng bạn bè, chỉ ghi lịch sử thanh toán, không đụng thẻ chính hợp đồng |
| 4 | `BotController::handleCallbackChangeCardSuccess` (`app/Http/Controllers/Admin/BotController.php`) | Không sửa | Callback đổi thẻ, đã có sẵn lịch sử đổi thẻ chính |
| 5 | `BotController::paymentBillMaxFriend` (`app/Http/Controllers/Admin/BotController.php`) | Không sửa | Chỉ ghi bảng thẻ bill phí theo lượng bạn bè, không đổi thẻ chính hợp đồng |
| 6 | `BotLifeCycle::addState` (`app/BotLifeCycle.php`) | Không sửa | Hàm ghi lịch sử, tự nuốt lỗi nên không ảnh hưởng kết quả bill |
| 7 | `state.blade.php` (`resources/views/basic/bill/modals/detail/state.blade.php`) | Không sửa | Modal hiển thị lịch sử loại 11, dùng `last4_card_main` — render sẵn có |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `PointSettingController::acceptBillMaxFriendV2` | `app/Http/Controllers/PointSettingController.php` | Direct | Bổ sung gọi `BotLifeCycle::addState` (type=11) sau khi ghi đè thẻ chính thành công bằng thẻ mới |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_life_cycles` | CREATE | Thêm 1 bản ghi mới (`status=3`, `type=11`) mỗi lần bill lại phí theo lượng bạn bè thành công **bằng thẻ mới**; không sửa/xoá bản ghi cũ |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Contract Plan & Payment (FA-031) — màn lịch sử hợp đồng | F1, D1 | Medium — bổ sung lịch sử đổi thẻ chính khi bill lại phí theo lượng bạn bè bằng thẻ mới; cần verify không sinh thừa khi bill lại bằng thẻ cũ |
| T2 | Payment History (FS-009) | D1 | Low — không đổi số liệu thanh toán, chỉ thêm vết đổi thẻ trong lịch sử hợp đồng |

**Rủi ro / lưu ý khi test (Dev tự nêu — AI tự review):**
- TH1: Hợp đồng đang là **chuyển khoản**, user chọn trả phí theo lượng bạn bè **bằng thẻ** → thẻ chính hợp đồng cũng bị ghi đè → sinh thêm 1 dòng lịch sử đổi thẻ chính (hành vi đúng theo data mới, nhưng là dòng lịch sử **mới** so với trước fix).
- TH2: User nhập lại **đúng thẻ cũ** khi bill lại → vẫn sinh 1 dòng lịch sử đổi thẻ (giống hành vi chuẩn của luồng đổi thẻ chính hiện có).
- Không tái hiện được trên dev → **chưa có bằng chứng chạy thật**, cần tester xác nhận lại theo các bước tái hiện (xem file 01).
- ⚠️ **RULE-08** (bill tiền / media / domain / job / loadbalance — không kết luận từ staging/dev): kịch bản cần bot > 100.000 bạn + tài khoản Univapay thật → TC verify phải có scope chạm **prd** hoặc môi trường có dữ liệu/thanh toán tương đương, không kết luận "Đạt" chỉ từ code review hoặc dev/local.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
