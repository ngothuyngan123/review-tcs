# 03 — Đánh giá ảnh hưởng từ Dev

<!-- Nguồn: comment "AI AUTO-FIXBUG" trên Redmine #33106 (journal #125936 / #125937, 2026-07-14). Paste nguyên văn nội dung dev impact, KHÔNG diễn giải lại. -->

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | Repo `sns-line`, commit `63b8376c37` (2 file). Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=33106 |
| Branch | `ai_small_33106` (nhánh gốc `release_step_20260623`) — đã push origin |
| Ngày submit đánh giá | 2026-07-14 |
| Auto-filled | 2026-07-15 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Hai API mobile mở màn quản lý Salon (`getListCalendarSalon`) và Lesson (`getListCalendarLesson`) trong `sns-line` **KHÔNG kiểm tra phân quyền staff**, khác với màn Sự kiện (Event booking) đã có `checkHasPermission`. Staff bị thu hồi quyền vẫn xem được danh sách salon/lesson và không thấy thông báo lỗi.

## 2. Cách fix

Thêm `checkHasPermission` vào 2 endpoint list của API mobile:
- `calendar_salon.index` cho `getListCalendarSalon` (`CalendarSalonController`)
- `calendar.index` cho `getListCalendarLesson` (`CalendarLessonController`)

Khi staff **không có quyền** → trả data rỗng + `permission=false` + message `この機能の操作権限が付与されていません。`; khi **có quyền** vẫn trả kèm `permission=true` + message, đúng khuôn mẫu `getListFolder` của event booking.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `getListCalendarSalon` — `Api/CalendarSalonController.php` | Thêm `checkHasPermission(calendar_salon.index)` | Endpoint list salon thiếu check quyền |
| 2 | `getListCalendarLesson` — `Api/CalendarLessonController.php` | Thêm `checkHasPermission(calendar.index)` | Endpoint list lesson thiếu check quyền |
| 3 | `checkHasPermission` — `Helpers/functions.php` | Không đổi (đối chiếu) | Hàm check quyền dùng lại |
| 4 | `getListFolder` — `Api/BookingEventController.php` | Không đổi (mẫu tham chiếu) | Khuôn mẫu trả `permission`/`message` của event booking |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getListCalendarSalon` (API mobile list salon) | `app/Http/Controllers/Api/CalendarSalonController.php` | Direct | Thêm check quyền `calendar_salon.index` |
| F2 | `getListCalendarLesson` (API mobile list lesson) | `app/Http/Controllers/Api/CalendarLessonController.php` | Direct | Thêm check quyền `calendar.index` |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(Không có)* | — | Chỉ thêm check quyền đọc, không ghi/sửa DB |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — App mobile list salon | F1 | Medium — chặn staff không có quyền xem danh sách salon qua API mobile + trả message báo lỗi |
| T2 | Lesson Booking (FA-019) — App mobile list lesson | F2 | Medium — chặn staff không có quyền xem danh sách lesson qua API mobile + trả message báo lỗi |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- ⚠️ Lưu ý reviewer (không thuộc bản gốc Dev):
     - Fix chỉ chạm 2 API LIST (index). Các API khác của salon/lesson (create/update/delete booking, detail, calendar khác) KHÔNG được đề cập trong mục 3 — cân nhắc hỏi Dev xem các endpoint đó đã có check quyền chưa (rủi ro sót sibling endpoint, tương tự pattern bug #38312).
     - "VERIFY" của Dev chỉ ở mức lint (php -l), CHƯA test runtime hành vi phân quyền thực tế.
     - Hiển thị message ở App mobile (Flutter) nằm ngoài repo backend — cần test trên app thật (cả app cũ chưa đọc cờ permission lẫn app mới). -->
