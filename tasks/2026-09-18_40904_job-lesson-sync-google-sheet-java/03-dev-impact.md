# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen` (author + assignee Redmine #40904) |
| Commit / Pull Request | `b03c949` |
| Branch | `m_202609_sync_google_sheet_lesson_40194_40904` (base `release-t08-2026`) |
| Ngày submit đánh giá | `2026-09-16` (Journal #136671) |
| Auto-filled | `2026-09-18 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn mục 1 của Journal #136671 (task **triển khai ngang** nên mục này là "Mục đích" thay vì root cause bug):

- PHP đang gọi Google Sheets API đồng bộ ngay trong request booking lesson (**12 call site** của `CalendarGoogleSheetService`) làm request chậm.
- Chuyển sang outbox theo `ai_docs/task_40194_40904/calendar-sync-googles-plan.md`: PHP chỉ ghi hàng đợi `calendar_sync_googles`, job Java quét rồi ghi sheet.

## 2. Cách fix

> Nguyên văn mục 2 của Journal #136671:

- Thêm `HandleCalendarSyncGoogleSheetTask` quét `calendar_sync_googles`, **lock theo `calendar_id`**, port đủ **4 thao tác PHP** (1 insert, 2 status, 3 payment, 4 friend info) và **nhánh dựng lại toàn bộ khi sheet rỗng**.
- Lỗi ghi vào `result_error_googles` `type_result = 3`, **backoff `[1, 5, 10, 30, 60]` phút**; `RetryErrorGoogleSheetTask` thêm nhánh đẩy lại qua cột mới `calendar_sync_googles_id`. Bật/tắt bằng `ENABLE_HANDLE_CALENDAR_SYNC_GOOGLE_SHEET`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn mục 3 của Journal #136671:
> - Không đổi signature hay behavior của function cũ, chỉ thêm method và field mới nên **không phải sửa caller nào**.
> - Hai entity dùng chung có thêm cột: `ResultErrorGoogle` (**20 call site** luồng form answer) và `CalendarManagement` (`NewEventRemindTask`, `CalendarLessonManager`) — chạy đúng **sau khi ALTER bảng**.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Toàn bộ caller function cũ | Không đổi signature / behavior — chỉ thêm method + field mới | Dev khẳng định không phải sửa caller nào |
| 2 | Entity `ResultErrorGoogle` (20 call site — luồng form answer) | Thêm cột `calendar_sync_googles_id` | Dùng chung bảng `result_error_googles`; chạy đúng sau khi ALTER bảng |
| 3 | Entity `CalendarManagement` → `NewEventRemindTask`, `CalendarLessonManager` | Thêm 3 cột Google Sheet | Entity dùng chung; chạy đúng sau khi ALTER bảng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Nguyên văn mục 4.1 của Journal #136671.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandleCalendarSyncGoogleSheetTask` | file mới | Direct | Toàn bộ luồng sync lesson (quét hàng đợi, lock theo `calendar_id`, 4 thao tác + nhánh sheet rỗng) |
| F2 | `RetryErrorGoogleSheetTask.needRetryErrorGoogleCalendarLesson` (mới) + `startTask` (sửa vòng lặp) | `RetryErrorGoogleSheetTask` | Direct | Nhánh đẩy lại qua cột mới `calendar_sync_googles_id`; **dùng chung với luồng form answer** |
| F3 | `CalendarCourseBookingRepository.findSheetRowByBookingId` / `findSheetRowsByCalendarId` | `CalendarCourseBookingRepository` | Direct | Tra dòng sheet theo booking / theo calendar |
| F4 | `CalendarManagementRepository.updateGoogleSheetAccessToken` / `updateGoogleSheetStatus` | `CalendarManagementRepository` | Direct | Cập nhật token + trạng thái liên kết sheet |
| F5 | `IGoogleSheetChangeService.updateValues` (PUT `values.update`, trước đó chưa có) | `IGoogleSheetChangeService` | Direct | API mới thêm — chưa từng chạy production |

### 4.2. List data bị update khi fix bug

> Nguyên văn mục 4.2 của Journal #136671.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Bảng mới `calendar_sync_googles` | CREATE (migrate) | Hàng đợi outbox: PHP ghi, job Java quét |
| D2 | `result_error_googles.calendar_sync_googles_id` | MIGRATE (ALTER thêm cột) | Bảng **dùng chung** với luồng form answer; lỗi lesson ghi `type_result = 3` |
| D3 | `config.properties`: `ENABLE_HANDLE_CALENDAR_SYNC_GOOGLE_SHEET`, `MAX_CALENDAR_SYNC_GOOGLE_SHEET_THREAD` | CREATE (config mới) | Cờ bật/tắt job + giới hạn số thread |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn mục 4.3 của Journal #136671.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Sync Google Sheet lesson** — test đặt lịch mới, đổi trạng thái, đổi thanh toán, sửa friend info, và case **sheet rỗng phải dựng lại toàn bộ booking** | F1, F3, F4, F5, D1 | High |
| T2 | **Sync Google Sheet form answer** — dùng chung bảng `result_error_googles` và `RetryErrorGoogleSheetTask`, **regression test lại luồng form sau khi ALTER bảng** | F2, D2 | High |
| T3 | **Job PHP `HandleErrorGoogleSpreadSheet`** — **phải gỡ nhánh `type_result = 3` trước khi bật flag**, không thì 2 worker cùng ghi 1 dòng sheet | F2, D2, D3 | High |
| T4 | **Event remind lesson (`NewEventRemindTask`) và `CalendarLessonManager`** — đọc entity `CalendarManagement` vừa thêm 3 cột Google Sheet, **smoke test còn chạy đúng** | mục 3, D1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

## Phụ lục — Journal #136671 (nguyên văn, Thanh Duy Nguyen — 2026-09-16)

```
Triển khai ngang #40904 [JOB][Lesson]Chuyển job sync google sheet của lesson sang java

1. Mục đích
	- PHP đang gọi Google Sheets API đồng bộ ngay trong request booking lesson (12 call site của CalendarGoogleSheetService) làm request chậm.
	- Chuyển sang outbox theo ai_docs/task_40194_40904/calendar-sync-googles-plan.md: PHP chỉ ghi hàng đợi calendar_sync_googles, job Java quét rồi ghi sheet.

2. Cách thực hiện
	- Thêm HandleCalendarSyncGoogleSheetTask quét calendar_sync_googles, lock theo calendar_id, port đủ 4 thao tác PHP (1 insert, 2 status, 3 payment, 4 friend info) và nhánh dựng lại toàn bộ khi sheet rỗng.
	- Lỗi ghi vào result_error_googles type_result = 3, backoff [1,5,10,30,60] phút; RetryErrorGoogleSheetTask thêm nhánh đẩy lại qua cột mới calendar_sync_googles_id. Bật/tắt bằng ENABLE_HANDLE_CALENDAR_SYNC_GOOGLE_SHEET.

3. Đã check và sửa các function sử dụng đến function/data vừa sửa
	- Không đổi signature hay behavior của function cũ, chỉ thêm method và field mới nên không phải sửa caller nào.
	- Hai entity dùng chung có thêm cột: ResultErrorGoogle (20 call site luồng form answer) và CalendarManagement (NewEventRemindTask, CalendarLessonManager) - chạy đúng sau khi ALTER bảng.

4. Đánh giá ảnh hưởng
        4.1 List function
            - HandleCalendarSyncGoogleSheetTask (file mới, toàn bộ luồng sync lesson)
            - RetryErrorGoogleSheetTask.needRetryErrorGoogleCalendarLesson (mới) + startTask (sửa vòng lặp)
            - CalendarCourseBookingRepository.findSheetRowByBookingId / findSheetRowsByCalendarId
            - CalendarManagementRepository.updateGoogleSheetAccessToken / updateGoogleSheetStatus
            - IGoogleSheetChangeService.updateValues (PUT values.update, trước đó chưa có)
        4.2 List những data bị update khi fix bug
            - Bảng mới calendar_sync_googles; ALTER result_error_googles thêm cột calendar_sync_googles_id; config.properties thêm ENABLE_HANDLE_CALENDAR_SYNC_GOOGLE_SHEET và MAX_CALENDAR_SYNC_GOOGLE_SHEET_THREAD.
        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
            - Sync google sheet lesson: test đặt lịch mới, đổi trạng thái, đổi thanh toán, sửa friend info, và case sheet rỗng phải dựng lại toàn bộ booking.
            - Sync google sheet form answer: dùng chung bảng result_error_googles và RetryErrorGoogleSheetTask, regression test lại luồng form sau khi ALTER bảng.
            - Job PHP HandleErrorGoogleSpreadSheet: phải gỡ nhánh type_result = 3 trước khi bật flag, không thì 2 worker cùng ghi 1 dòng sheet.
            - Event remind lesson (NewEventRemindTask) và CalendarLessonManager: đọc entity CalendarManagement vừa thêm 3 cột google sheet, smoke test còn chạy đúng.

5. Commit / Branch
        5.1 Commit hoặc pull request
            - b03c949
        5.2 Branch hiện tại của task
            - m_202609_sync_google_sheet_lesson_40194_40904
```
