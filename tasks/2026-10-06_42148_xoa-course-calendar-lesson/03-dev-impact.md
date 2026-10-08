# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Ngô Thúy Ngần (assignee ticket; đánh giá do hệ thống AI LME Fix bug sinh tự động, 2 round — xem ghi chú dưới) |
| Commit / Pull Request | `<chưa có PR>` |
| Branch | `sns-line: ai_fixbug_42148` (nhánh gốc `release_step_20260930_v2`, commit `7a00b8cd03`, 2 file — round mới nhất, đã push) |
| Ngày submit đánh giá | 2026-10-06 (Journal #140503 — round 2, thay thế round 1 Journal #140485) |
| Auto-filled | 2026-10-06 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

⚠️ **Lưu ý 2 round fix** — Redmine không có heading "Đánh giá ảnh hưởng" riêng trong description; nội dung đánh giá nằm ở 2 Journal note do hệ thống AI Auto-fixbug sinh:
- Journal #140485 (round 1): chỉ fix `CalendarCourseService::deleteCalendarCourse`.
- Journal #140503 (round 2, **mới nhất, dùng làm nguồn chính dưới đây**): fix thêm cả `CalendarManagementController::deleteCalendar` (lối xóa cả lịch bài học), branch/commit khác round 1.

Dev tự ghi mức verify = **lint only** (`php -l` + render `toSql`) — "Dev DB host không kết nối được (connection refused) — chưa kiểm dữ liệu runtime". **Chưa có bằng chứng test runtime trên data thật.**

---

## 1. Nguyên nhân

Bảng lịch gửi nhắc `event_step_time` dùng chung cột `user_booking_id` cho đơn lịch bài học (lesson), đơn salon và đơn sự kiện. Khi xóa khóa học (và khi xóa cả lịch bài học), code xóa lịch nhắc chỉ lọc theo `user_booking_id + bot_id`, không lọc loại bước nhắc (`event_step.type`), nên đơn salon cùng bot có id trùng với id đơn bài học bị xóa sẽ mất lịch nhắc (khách salon không nhận tin nhắc).

## 2. Cách fix

Theo yêu cầu human: bỏ câu xóa hàng loạt `event_step_time` theo `user_booking_id` (thêm từ #41267, không lọc loại bước nhắc ⇒ xóa nhầm lịch nhắc salon/booking cũ/form trùng id) ở **cả 2 lối**:

- **Xóa khóa học** (`CalendarCourseService::deleteCalendarCourse`) — bỏ cả khối gồm `mobile_notify`, quay về vòng foreach cũ theo từng đơn: chỉ xóa lịch nhắc bước `type=4` còn chờ gửi (`status=0`) + thông báo app chưa xác nhận (`is_confirm=0`, `status=1`).
- **Xóa cả lịch bài học** (`CalendarManagementController::deleteCalendar`) — chỉ bỏ câu `EventStepTime` hàng loạt, **GIỮ** câu xóa mọi `mobile_notify` loại lesson của đơn bị xóa; lịch nhắc của lịch vẫn được dọn qua event nhắc `type=4` của chính lịch theo `event_id`.

Quét ngang còn 5 câu xóa `event_step_time` theo id booking cũ không lọc type/bot_id (FriendlistController:2883/4121/4552, BookingManagerController:1268, BookingAjaxController:239; + Api/FriendInformationController:1249) — **Dev khẳng định khác tính năng, đề xuất ticket riêng, KHÔNG fix trong ticket #42148 này**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarCourseService::deleteCalendarCourse` (app/Services/CalendarManagement/CalendarCourseService.php) | Bỏ khối xóa hàng loạt `event_step_time` + `mobile_notify` theo `user_booking_id`; quay về foreach lọc `type=4`/`status=0` + `is_confirm=0`/`status=1` | Root cause fix |
| 2 | `CalendarManagementController::deleteCalendar` (app/Http/Controllers/Basic/CalendarManagementController.php) | Bỏ câu `EventStepTime` hàng loạt; giữ câu xóa `mobile_notify` loại lesson | Root cause fix (lối xóa cả lịch bài học) |
| 3 | `CalendarSalonCourseService::deleteCalendarCourse` | Không sửa | Đối chứng — đã lọc `type=5` đúng từ trước |
| 4 | `ActionBookingCalendar::removeActionRemind` | Không sửa | Đối chứng — đã lọc `events.type=2` đúng từ trước |
| 5 | `FriendlistController` (dòng 2883/4121/4552) + `Api/FriendInformationController` (dòng 1249) | Không sửa | Lateral — phần lesson/salon đã lọc `event_id`; phần booking cũ (`BCUserBooking`) **CHƯA** lọc type/bot_id, Dev đề xuất ticket riêng (**ngoài scope #42148**) |
| 6 | `BookingManagerController::ajaxRemoveCalendar` (dòng 1268) + `BookingAjaxController::ajaxRemoveCalendar` (dòng 239) | Không sửa | Lateral — **CHƯA** lọc type/bot_id, Dev đề xuất ticket riêng (**ngoài scope #42148**) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarCourseService::deleteCalendarCourse` | app/Services/CalendarManagement/CalendarCourseService.php | Direct | Xóa khóa học — thu hẹp câu xóa lịch nhắc, bỏ khối xóa `mobile_notify` theo `user_booking_id` |
| F2 | `CalendarManagementController::deleteCalendar` | app/Http/Controllers/Basic/CalendarManagementController.php | Direct | Xóa cả lịch bài học — bỏ câu `EventStepTime` hàng loạt, giữ xóa `mobile_notify` lesson |
| F3 | `CalendarSalonCourseService::deleteCalendarCourse` | (không đổi) | Indirect | Đối chứng cùng pattern, không sửa — đã lọc `type=5` đúng |
| F4 | `ActionBookingCalendar::removeActionRemind` | (không đổi) | Indirect | Đối chứng cùng pattern, không sửa — đã lọc `events.type=2` đúng |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `event_step_time` | UPDATE (thu hẹp điều kiện DELETE) | Câu xóa chỉ còn match đúng lịch nhắc `type=4` của bài học bị xóa; dòng nhắc salon/sự kiện trùng `user_booking_id` không còn bị xóa nhầm |
| D2 | `mobile_notify` | UPDATE (thu hẹp điều kiện DELETE ở `CalendarCourseService`; giữ nguyên ở `CalendarManagementController::deleteCalendar`) | Thông báo app chưa xác nhận (`is_confirm=0`, `status=1`) của đơn lesson bị xóa — không còn xóa nhầm thông báo app của đơn salon/sự kiện trùng id khi xóa khóa học |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lesson / Calendar Booking (FA-019) — xóa khóa học / xóa lịch bài học | F1, F2, D1, D2 | High — là điểm sửa trực tiếp, phải verify lịch nhắc/thông báo của **chính đơn lesson bị xóa** vẫn được dọn đúng sau fix |
| T2 | Salon Booking (FA-020) — lịch nhắc/thông báo đơn salon | F1, F2, D1, D2 | High — đây là **bug gốc**: đơn salon trùng `user_booking_id` với đơn lesson bị xóa không còn bị mất lịch nhắc/thông báo oan |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
