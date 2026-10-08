# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42148 — Xóa course của calendar lesson` |
| Module / Màn hình | Lesson / Calendar Booking — xóa khóa học (`CalendarCourseService::deleteCalendarCourse`), liên quan cả xóa lịch bài học (`CalendarManagementController::deleteCalendar`) |

## Mô tả bug (bản dịch tiếng Việt)

Xóa event của booking không chỉ định type có thể xóa nhầm vào booking của salon — method `deleteCalendarCourse`.

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

⚠️ **Bug không tái hiện được trong Redmine theo bộ 3 bước Steps/Expected/Actual** — root cause đã được Dev xác nhận trực tiếp qua đánh giá ảnh hưởng (file [03-dev-impact.md](03-dev-impact.md)), không qua section tái hiện riêng. TCs nên tập trung verify cách fix + regression impact.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có file đính kèm. -->

## Ghi chú thêm của Leader

- Bug do Dev tự detect (tracker "Bug tự detect"), không phải khách hàng báo.
- Root cause: bảng lịch gửi nhắc `event_step_time` dùng chung cột `user_booking_id` cho đơn lịch bài học (lesson), đơn salon và đơn sự kiện. Câu xóa lịch nhắc khi xóa khóa học / xóa lịch bài học chỉ lọc theo `user_booking_id + bot_id`, không lọc loại bước nhắc (`event_step.type`) → đơn salon cùng bot trùng id với đơn bài học bị xóa bị mất lịch nhắc (khách salon không nhận tin nhắc).
- Dev đã xác nhận có **2 round fix** (xem Journal #140485 rồi #140503 refine thêm — chi tiết đầy đủ ở file 03): round đầu chỉ fix `deleteCalendarCourse`; round sau (mới nhất, dùng làm input chính cho file 03) fix thêm cả `CalendarManagementController::deleteCalendar` (xóa cả lịch bài học).
- Dev tự ghi ở mức VERIFY: "Dev DB host không kết nối được (connection refused) — chưa kiểm dữ liệu runtime" → mới verify ở mức lint/toSql, **chưa test runtime trên DB thật**. Cần TC verify thực tế trên env có DB.
- Dev tự nêu 5 câu xóa `event_step_time` khác không lọc type/bot_id tương tự (FriendlistController:2883/4121/4552, BookingManagerController:1268, BookingAjaxController:239, Api/FriendInformationController:1249) — Dev khẳng định **khác tính năng, không fix trong ticket này, đề xuất ticket riêng**. Leader lưu ý khi xét phạm vi task (không được coi các điểm này là trong scope fix #42148).

## Journal / note từ Redmine (nguyên văn)

<!-- 2 journal #140485 + #140503 là báo cáo "Đánh giá ảnh hưởng phía dev" (Section B) đầy đủ — đã chuyển nguyên văn vào file 03-dev-impact.md, không lặp lại ở đây để tránh trùng. -->
