# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine bởi `/new-task` (Section "Đánh giá ảnh hưởng" — journal 124139, AI Auto-fixbug, bản mới nhất 2026-06-30, supersede journal 124019 cũ). Tester đọc lại + tick checkbox verify.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | commit `638308272a` (branch `ai_fixbug_38208`, 2 file) — `<chưa có PR URL>` |
| Branch | `ai_fixbug_38208` (repo sns-line, gốc `release_step_20260623`) |
| Ngày submit đánh giá | `2026-06-30` |
| Auto-filled | `2026-07-01 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- BUG: root cause -->

Khi xóa slot (受付枠) của calendar Lesson **TRÊN APP**, hệ thống soft-delete các booking trong slot rồi xóa thông báo (mobile_notify) tương ứng. Nhưng câu xóa thông báo lọc thêm điều kiện `bot_id` lấy từ `getBotId()` = `Session('current_bot_id')`, mà session này **TRỐNG** trong ngữ cảnh app (API/JWT không có session web).

Hậu quả: booking bị xóa (lọc theo id, không cần bot) nhưng thông báo **KHÔNG khớp điều kiện** (bot_id null) nên không bị xóa → thông báo trở thành **mồ côi** (chưa đọc), bị tính mãi vào badge mà không xem/đánh dấu đã đọc được (màn danh sách & đếm theo lịch dùng JOIN bắt buộc booking còn sống) → dù làm gì cũng không xóa/mất đi. Trên web `getBotId()` có session nên xóa đúng — lỗi **chỉ xảy ra khi thao tác trên app**.

## 2. Cách fix

Hàm **MỚI** `deleteFromApp()` cho luồng xóa slot lesson **TỪ APP**: API không gửi botId & app không có session nên suy botId qua course của slot — `reception.course_id → calendar_course.calendar_id → calendar_management.bot_id` — rồi xóa đúng mobile_notify của booking bị xóa. Trỏ `Api\CalendarLessonController@deleteReception` sang hàm mới. **GIỮ NGUYÊN** `delete()`/`deleteList()` web (diff service 0 dòng xóa).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarCourseReceptionService::deleteFromApp` (app/Services/CalendarManagement/CalendarCourseReceptionService.php) | **MỚI** | Lấy botId từ CalendarManagement theo booking.calendar_id, xóa mobile_notify đúng cho luồng app |
| 2 | `CalendarCourseReceptionService::delete` / `deleteList` (cùng file) | **GIỮ NGUYÊN** | Web dùng `getBotId()` từ session — web có session nên đúng |
| 3 | `Api\CalendarLessonController::deleteReception` | Đổi gọi `delete()` → `deleteFromApp()` | Trỏ luồng app sang hàm mới |
| 4 | `CalendarManagement` (app/CalendarManagement.php) | Không đổi (đọc) | Bảng `calendar_management`, có `bot_id` — nguồn suy botId |
| 5 | `CalendarCourseBookingRepository::getBookingListWithReceptionId` | Không đổi (đọc) | Trả `calendar_course_bookings.*` (có `calendar_id`) để suy botId |
| 6 | `getBotId` (app/Helpers/functions.php) | Không đổi | **Nguồn lỗi**: trả `Session('current_bot_id')`, trống trên API/app |
| 7 | `CalendarCourseBookingRepository::deleteBooking` | Không đổi | Soft-delete booking (`deleted_at`) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarCourseReceptionService::deleteFromApp` | app/Services/CalendarManagement/CalendarCourseReceptionService.php | Direct | Hàm MỚI cho app: suy botId qua calendar_management, xóa mobile_notify đúng |
| F2 | `Api\CalendarLessonController::deleteReception` | app/Http/Controllers/Api/CalendarLessonController.php | Direct | Đổi sang gọi `deleteFromApp()` |
| F3 | `CalendarCourseReceptionService::delete` / `deleteList` | (cùng file service) | Indirect (không đổi) | Web giữ nguyên — cần regression xác nhận không đụng chạm |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `mobile_notify` (type=11 lesson) | DELETE | App xóa slot nay dọn đúng mobile_notify của booking bị xóa (theo botId suy từ calendar_management) |
| D2 | `calendar_course_bookings.deleted_at` | UPDATE (soft-delete) | Booking trong slot bị soft-delete khi xóa reception |
| D3 | `mobile_notify` orphan đã tồn tại | DELETE (recovery 1 lần) | ⚠️ Fix forward KHÔNG tự dọn orphan cũ. Cần chạy 1 lần trên DB prod (sau khi human duyệt): `DELETE mn FROM mobile_notify mn WHERE mn.type=11 AND mn.is_confirm=0 AND mn.status=1 AND NOT EXISTS (SELECT 1 FROM calendar_course_bookings b WHERE b.id=mn.lesson_booking_id AND b.deleted_at IS NULL);` (cân nhắc type=10 salon). Backup/đếm trước; có thể giới hạn theo bot_id KH Risa Yoga |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lesson Booking (FA-019) — xóa slot trên app | F1, F2, D1, D2 | Medium — xóa slot trên app nay dọn đúng thông báo booking bị xóa (web không đổi) |
| T2 | Notification Settings (FA-006) — badge/danh sách notify app | F1, D1, D3 | Medium — badge thông báo app không còn kẹt thông báo mồ côi do xóa slot trên app |
| T3 | Xóa slot Lesson trên **Web** (delete/deleteList) | F3 | Low — diff service 0 dòng xóa, nhưng cần regression xác nhận |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — lưu ý **D3 data recovery orphan cũ** cần verify riêng
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- ⚠️ Lưu ý AI tự review (từ Redmine): trùng lặp logic giữa deleteFromApp() và delete() — nếu sau này sửa logic xóa slot phải đồng bộ cả 2. deleteFromApp suy botId qua calendar_management (booking KHÔNG có cột bot_id, chỉ có calendar_id). -->
