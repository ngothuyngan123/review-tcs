# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (Auto-fixbug LME)` |
| Commit / Pull Request | `commit 9b45dfda09 (2 file) — nhánh sns-line` |
| Branch | `ai_small_41091 (gốc release_step_20260827)` |
| Ngày submit đánh giá | `2026-09-21` |
| Auto-filled | `2026-10-05 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

API lấy trạng thái menu thông báo của app chạy 14 câu đếm riêng lẻ trên bảng nhật ký thông báo `mobile_notify` (một trong các bảng lớn nhất hệ thống, không dọn định kỳ). Chỉ mục duy nhất dùng được cho nhóm truy vấn này gồm bot - đã đọc - trạng thái gửi - người dùng, KHÔNG có cột loại thông báo (`type`), nên mỗi câu đếm phải mở lần lượt từng dòng chưa đọc của bot rồi mới lọc được đúng loại. Một request vì vậy phải đọc lượng dòng gấp 14 lần số thông báo chưa đọc của bot; bot tích luỹ nhiều thông báo chưa đọc thì thời gian phản hồi lên tới hàng chục giây (ghi nhận tối đa 43 giây).

## 2. Cách fix

Gộp 12 câu đếm thông báo chưa đọc chỉ lọc theo loại thành MỘT câu đếm gộp theo loại (thêm hàm dùng riêng `countUnconfirmNotifyByType` trong controller thông báo của app), giữ nguyên 2 câu đếm riêng cho loại **biểu mẫu** (lọc thêm mã sản phẩm) và **tiếp thị liên kết** (lọc thêm nhóm sự kiện) để không đổi điều kiện cũ — số câu truy vấn mỗi request giảm từ 14 xuống 3, kết quả từng mục menu và tổng badge giữ nguyên.

Thêm migration tạo chỉ mục phủ `(bot_id, type, status, is_confirm, user_id)` cho bảng `mobile_notify` để câu đếm chạy trọn trên chỉ mục thay vì mở từng dòng dữ liệu; migration có kiểm tra chỉ mục đã tồn tại nên chạy lại được và không xung đột nếu nhánh ticket #41026 (chỉ mục 4 cột là tiền tố) lên release trước.

Quét ngang: API đếm thông báo chưa đọc theo từng loại còn lại (`getNumberNotifyUnconfirmForEachType`) cũng theo mẫu này nhưng nhẹ hơn và đã được chỉ mục mới phục vụ — **ghi nhận lại chứ không sửa**, ngoài phạm vi ticket.

⚠️ **Danh sách 12 mã loại được gộp vào `countUnconfirmNotifyByType`**: `[2, 12, 10, 11, 15, 6, 8, 9, 4, 13, 14, 17]` — Dev tự đối chiếu khớp 1-1 với 12 câu đếm cũ, không trùng/sót mã. Loại `3` (biểu mẫu) và `16` (tiếp thị liên kết) **vẫn đếm riêng, không đổi**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `NotifyController::getListStatusMenuNotify` (`app/Http/Controllers/Api/NotifyController.php:1133`) | Sửa — gọi hàm gộp mới thay 12 câu đếm riêng lẻ | Entry point của bug — endpoint `get-list-status-menu-notify` |
| 2 | `NotifyController::countUnconfirmNotifyByType` (`app/Http/Controllers/Api/NotifyController.php:1091`) | **Hàm mới** — 1 câu đếm gộp theo `type`, nhận danh sách loại | Thay thế 12 câu đếm chưa đọc chỉ lọc theo loại |
| 3 | `NotifyController::getNumberNotifyUnconfirmForEachType` (`app/Http/Controllers/Api/NotifyController.php:62`) | Không sửa — cùng mẫu bug, nhẹ hơn, đã được index mới phục vụ | Quét ngang, ghi nhận lại, **ngoài phạm vi ticket** |
| 4 | `setAppBadgeNotifyCount` (`app/Helpers/functions.php:4522`) | Không sửa — hành vi giữ nguyên | Vẫn ghi tổng badge của user+bot sau khi đếm, giá trị không đổi |
| 5 | `AddIndexMenuStatusToMobileNotifyTable` (`database/migrations/2026_09_18_100000_add_index_menu_status_to_mobile_notify_table.php`) | **Migration mới** — tạo chỉ mục phủ `(bot_id, type, status, is_confirm, user_id)` | Để 3 câu đếm còn lại chạy trọn trên index |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `NotifyController::getListStatusMenuNotify` — API `POST /api/mobile/notify/get-list-status-menu-notify` | `app/Http/Controllers/Api/NotifyController.php:1133` | Direct | Entry point bug, số câu đếm giảm 14→3; giá trị highlight từng mục + tổng badge giữ nguyên |
| F2 | `NotifyController::countUnconfirmNotifyByType` (hàm mới) | `app/Http/Controllers/Api/NotifyController.php:1091` | Direct | Gộp 12 câu đếm loại thông báo chưa đọc thành 1 câu `GROUP BY type` |
| F3 | `setAppBadgeNotifyCount` | `app/Helpers/functions.php:4522` | Indirect | Không sửa, nhưng phụ thuộc kết quả đếm — đã check giá trị không đổi |
| F4 | `NotifyController::getNumberNotifyUnconfirmForEachType` | `app/Http/Controllers/Api/NotifyController.php:62` | Indirect (ngoài phạm vi) | Cùng mẫu bug, Dev **không sửa** trong ticket này — ghi nhận lại |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `mobile_notify` (toàn bảng) | READ only (đếm) | Không ghi dữ liệu, chỉ đổi cách đếm (gộp theo `type`) |
| D2 | Index mới `(bot_id, type, status, is_confirm, user_id)` trên `mobile_notify` | CREATE (migration) | Bảng lớn → chạy migration giờ thấp điểm; tăng dung lượng index + chi phí ghi nhỏ khi insert thông báo mới |
| D3 | `mobile_badge_noitfy` | Không đổi hành vi (vẫn UPDATE như cũ) | Vẫn ghi tổng badge theo user+bot sau khi đếm, giá trị tính ra không đổi |

Không cần recover data (Dev xác nhận ✔).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Notification Settings (FA-006) — API trạng thái menu thông báo app Elme (mobile) | F1, F2, D1 | Medium — giảm số câu đếm, giá trị highlight từng mục menu phải giữ nguyên |
| T2 | System Notifications (FS-014) — mục thông báo hệ thống nằm trong câu đếm gộp | F2, D1 | Medium — nằm trong 12 mã loại gộp, cần verify giá trị đúng |
| T3 | App badge thông báo (ngoài glossary chính thức) | F3, D3 | Low — hành vi ghi badge không đổi, nhưng phụ thuộc kết quả đếm mới |

---

## Ghi chú thêm (ngoài 4 mục chuẩn — AI auto-fill bổ sung)

- **5. RECOVER DATA**: ✔ Không cần recover data (Dev xác nhận).
- **6. VERIFY của Dev — chỉ ở mức LINT, chưa chạy thật**:
  - `php -l` cho 2 file sửa: không lỗi syntax.
  - Boot Laravel + in `toSql()`: câu đếm gộp sinh đúng SQL (`GROUP BY type`, cùng bộ điều kiện với câu cũ, hợp lệ `ONLY_FULL_GROUP_BY`).
  - Guard danh sách loại rỗng (qua Reflection): trả mảng rỗng, không chạy query.
  - Đối chiếu danh sách 12 mã loại gộp `[2,12,10,11,15,6,8,9,4,13,14,17]` với 12 câu đếm cũ: khớp 1-1.
  - ⚠️ **MySQL dev từ chối kết nối** lúc Dev verify → **KHÔNG chạy được EXPLAIN / tái hiện dữ liệu thật**. Hiệu quả thực tế (response time có giảm đúng như kỳ vọng không) **CHƯA được đo trên dữ liệu thật** — đây là GAP lớn nhất cần test bổ sung.
  - Index hiện có trên `mobile_notify` (theo Dev kiểm tra code migration của nhánh release): chỉ có `mobile_notify_badge_recount_index (bot_id, is_confirm, status, user_id)` — không có cột `type`, khớp với phân tích nguyên nhân.
- **Rủi ro/lưu ý khi test (Dev tự ghi)**:
  - Migration tạo index trên bảng lớn → khóa bảng một lần khi chạy, phải chạy giờ thấp điểm.
  - Index mới tăng chi phí ghi khi insert thông báo mới (Dev đánh giá chấp nhận được).
  - Không chạy được EXPLAIN vì MySQL dev tắt — hiệu quả thực tế cần đo lại trên môi trường có dữ liệu.
- **Liên quan #41026**: cùng bảng `mobile_notify`, cùng nhóm API đếm thông báo, đã ghi nhận trước vấn đề thiếu cột `type` trong index.
- ⚠️ **Phạm vi chưa rõ**: Endpoint `POST /api/mobile/notify/get-order-history` được gắn thêm vào ticket này ở Journal #138315 (2026-09-25) — **SAU** khi Dev báo fix done (2026-09-21). Đánh giá ảnh hưởng ở trên **KHÔNG đề cập** đến endpoint này → cần xác nhận với Dev xem branch `ai_small_41091` có xử lý `get-order-history` hay không trước khi coi ticket đã fix đủ cho cả 2 endpoint.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Xác nhận riêng cho ticket này**: đã hỏi Dev về phạm vi `get-order-history` (xem Ghi chú thêm ở trên) trước khi chốt coverage
