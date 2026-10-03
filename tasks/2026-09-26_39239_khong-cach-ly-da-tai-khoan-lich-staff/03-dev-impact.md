# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #39239 — Journal #133411 (AI LME Fix bug, 2026-08-28), mục 1 → 4. Nguyên văn, không diễn giải lại.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (AI auto-fixbug) · Assignee Redmine: Kim Cúc |
| Commit / Pull Request | commit `ab90476694` (repo sns-line) — chưa có link PR |
| Branch | `ai_fixbug_39239` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | 2026-08-28 |
| Auto-filled | 2026-09-26 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Hai điểm ghi dữ liệu nhận thẳng id do trình duyệt gửi mà không kiểm bản ghi đó có thuộc bot của người đăng nhập không. Endpoint sửa lịch lesson được khai báo NGOÀI nhóm route có lớp kiểm quyền lịch-thuộc-bot (lớp này chỉ bọc các đường dẫn khác cùng nhóm), rồi cập nhật thẳng theo id nên tài khoản A đổi được tên lịch của bot tài khoản B. Endpoint xoá nhân viên cũng tìm rồi xoá bản ghi chỉ theo id thô, không giới hạn theo danh sách bot mà người đăng nhập được quản lý nhân viên.

## 2. Cách fix

Chặn ngay đầu hai điểm ghi. Hàm sửa lịch lesson dùng lại hàm kiểm lịch-thuộc-bot đã có sẵn: lịch không thuộc bot đang đăng nhập thì trả về thông báo không có quyền và không ghi gì; đồng thời bổ sung một hàm truy vấn mới ở tầng kho dữ liệu để câu lệnh cập nhật lịch luôn kèm điều kiện bot sở hữu (giữ nguyên hàm cũ cho luồng sắp xếp). Hàm xoá nhân viên giới hạn tìm bản ghi theo danh sách bot mà người đăng nhập thực sự được quản lý nhân viên, ngoài phạm vi thì trả lỗi 403 và không xoá; nhờ vậy cũng hết lỗi hệ thống khi id gửi lên không tồn tại. LƯU Ý CHO NGƯỜI REVIEW: phần xoá nhân viên trùng nội dung với bản sửa của ticket #38960 (branch ai_fixbug_38960 đang chờ review, chưa lên release) — hai ticket không có quan hệ trên Redmine nên fix ở đây làm độc lập, tự chứa trên release; khi gộp cần chọn một bản để tránh xung đột. Quét ngang thấy còn 6 chỗ cùng kiểu chưa kiểm sở hữu (sắp xếp lịch, cài đặt hiển thị đặt lịch, sắp xếp nhân viên, xoá nhân viên chưa đồng ý...) — đã ghi lại, không sửa ngoài phạm vi ticket.

> Ghi chú auto-fill: mục 2 nói "còn 6 chỗ", phần "Rủi ro / lưu ý khi test" của cùng journal nói "còn 4 điểm" — số liệu lệch, Dev chưa liệt kê đủ danh sách.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarManagementController::editCalendar` — app/Http/Controllers/Basic/CalendarManagementController.php | Sửa (file có trong 4.1) | Điểm ghi sửa lịch — thêm cổng kiểm sở hữu |
| 2 | `CalendarManagementService::editCalendar`, `::checkCalendarBelongBot` — app/Services/CalendarManagement/CalendarManagementService.php | Sửa (file có trong 4.1) | Dùng lại hàm kiểm lịch-thuộc-bot có sẵn |
| 3 | `CalendarManagementRepository::editCalendar`, `::editCalendarOfBot`, `::getCalendarWithBot` — app/Repositories/Eloquents/CalendarManagementRepository.php | Thêm hàm mới (`editCalendarOfBot`), giữ `editCalendar` cũ cho luồng sắp xếp | Câu update kèm điều kiện bot |
| 4 | `StaffManagementController::deleteStaffBot` — app/Http/Controllers/Admin/StaffManagementController.php | Sửa (file có trong 4.1) | Giới hạn tìm bản ghi theo danh sách bot được quản lý nhân viên, ngoài phạm vi → 403 |
| 5 | `getListBotIdStaffManagement` — app/Helpers/functions.php | Dùng lại (không sửa) | Lấy danh sách bot người đăng nhập được quản lý nhân viên |
| 6 | `CheckLessonCalendarBelongToBot::handle` — app/Http/Middleware/CheckLessonCalendarBelongToBot.php | Check (không sửa) | Middleware kiểm lịch-thuộc-bot không bọc route edit |
| 7 | `saveEditCalendar` — public/js/calendar_management/index.js | Check (không sửa) | FE đọc `response.success` |
| 8 | `deleteStaffBot`, `deleteUserStaffNotAgreed` — public/js/admin/employees/employees_management.js | Check (không sửa) | FE xoá nhân viên |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev chỉ ghi danh sách **file thay đổi** (nguyên văn bên dưới); tag F* do `/new-task` đánh theo từng file.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Sửa lịch lesson — POST `/basic/calendar-management/{id}/edit` | app/Http/Controllers/Basic/CalendarManagementController.php | Direct | |
| F2 | Xoá nhân viên — POST `/admin/ajax/delete-staff-bot` | app/Http/Controllers/Admin/StaffManagementController.php | Direct | |
| F3 | `CalendarManagementService` (editCalendar / checkCalendarBelongBot) | app/Services/CalendarManagement/CalendarManagementService.php | Direct | |
| F4 | `CalendarManagementRepository` (thêm `editCalendarOfBot`; `editCalendar` cũ giữ cho luồng sắp xếp) | app/Repositories/Eloquents/CalendarManagementRepository.php | Direct | Luồng sắp xếp lịch dùng hàm cũ → Indirect |
| F5 | `CalendarManagementRepositoryInterface` | app/Contracts/Repositories/CalendarManagementRepositoryInterface.php | Direct | Khai báo hàm mới |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_management.calendar_name` / `line_name` / `enable_use_calendar` / `google_calendar_id` | UPDATE | Từ nay chỉ cập nhật được khi lịch thuộc bot đang đăng nhập |
| D2 | `user_staff_bots` | DELETE | Chỉ xoá được bản ghi thuộc bot mà người đăng nhập được quản lý nhân viên |
| — | — | — | Không cần recover dữ liệu (chỉ chặn ghi, không đổi dữ liệu sẵn có) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Dev không ghi mức risk — cột "Nguy cơ regression" để `<chưa rõ>`.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lesson / Calendar Booking (FA-019) — chặn sửa lịch lesson của bot thuộc tài khoản khác; luồng sửa lịch hợp lệ giữ nguyên | F1, F3, F4, F5, D1 | `<chưa rõ>` |
| T2 | Staff Management (FA-035) — chặn xoá nhân viên của bot ngoài phạm vi quản lý; xoá trong phạm vi giữ nguyên | F2, D2 | `<chưa rõ>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
