# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41772 — Journal #139397 (AI LME Fix bug, 2026-09-30, báo cáo auto-fixbug). Nội dung giữ nguyên văn, chỉ chia vào đúng mục template.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) · Assignee Redmine: Nguyen Ha Vi |
| Commit / Pull Request | `sns-line` — chưa có link PR (branch đã push) |
| Branch | `ai_fixbug_41772` (nhánh gốc `release_step_20260930`) — đã push |
| Ngày submit đánh giá | 2026-09-30 (Commit Date Redmine: 2026-09-30) |
| Auto-filled | 2026-09-30 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Endpoint `POST /basic/calendar-management/{id}/edit` là PARTIAL UPDATE (2 caller, 2 tập field khác nhau), nhưng rule validate lại khai `calendar_name => required` ⇒ nút 有効/無効 (chỉ gửi `enable_use_calendar`) trượt validate → HTTP 400, cờ không bao giờ ghi vào DB; nhánh error của toggle lật checkbox về trạng thái cũ mà KHÔNG hiện thông báo ⇒ khách thấy "vừa bật có hiệu lực trong tích tắc rồi tự động về 無効".

Đây là XUNG ĐỘT THỨ TỰ MERGE, không phải 1 commit sai:
1. #41104 (commit `15f0110b10`, 2026-09-18) sửa toggle THÔI gửi `calendar_name` — lúc đó trên release này CHƯA có rule `required` nên #41104 chạy đúng.
2. Nhánh #40050 được CHERRY-PICK vào release ngày 2026-09-25 (commit `64fc537f15`: author date 2026-08-20 nhưng COMMIT date 25/09, sau #41104), mang `required` đặt lên trên một toggle đã không còn gửi tên ⇒ vỡ từ đó. Comment của #40050 vẫn giữ giả định "màn sửa lịch luôn gửi tên quản lý" — đúng trên release cũ nơi nó được viết (khi đó cả 2 caller đều gửi đủ object), sai trên release này.

Ticket báo 30/09, khớp 5 ngày sau cherry-pick. Không phải lỗi quyền (操作権限) như khách suy đoán.

Lịch SALON không bị vì endpoint sinh đôi bên salon đã khai `sometimes|nullable` từ #39566 (11/08) — ở đó endpoint vốn đã có caller gửi payload rất partial (`chooseCalendarStaffType` chỉ gửi `calendar_staff_type`, `saveEditCalendarSalon` chỉ gửi `show_course_menu`) nên khai `required` là vỡ ngay 2 màn đang chạy, người fix buộc phải thấy.

CẢ 2 release đang có bug: `release_staging_20260910` và `release_step_20260930`.

## 2. Cách fix

1. `CalendarManagementController::editCalendar` — `calendar_name` đổi từ `required` sang `sometimes|required`: field CÓ gửi thì vẫn bắt buộc không rỗng (giữ nguyên lớp chặn của #40050 cho modal sửa tên + chặn trùng 管理名 của #41104), field KHÔNG gửi (toggle) thì bỏ qua — cùng khuôn với `CalendarSalonController::editCalendarSalon` vốn đã là `sometimes|nullable`.
2. `public/js/calendar_management/index.js` — nhánh error của `enableUseCalendar` gọi `window.showLessonAjaxError(xhr)` để lần sau thất bại có thông báo, không còn lật cờ âm thầm.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarManagementController::editCalendar` (app/Http/Controllers/Basic/CalendarManagementController.php:585) | Sửa (dòng 599: `required` → `sometimes\|required`) | Route `calendar.edit`; 2 caller JS: `index.js:171` (modal 管理名), `index.js:226` (toggle 有効/無効) |
| 2 | `CalendarManagementService::editCalendar` (app/Services/CalendarManagement/CalendarManagementService.php:89) | KHÔNG sửa | `except([id])` rồi chuyển repository; ràng buộc bot (`checkCalendarBelongBot`) nằm ở đây, vẫn áp |
| 3 | `CalendarManagementRepository::editCalendar` (app/Repositories/Eloquents/CalendarManagementRepository.php:36) | KHÔNG sửa | `where(id)->update($data)` = partial update thật, ghi 1 cột không đè cột khác; cũng được `CalendarManagementService::sort` dùng |
| 4 | `enableUseCalendar()` (public/js/calendar_management/index.js:226) | Sửa (dòng 247-249) | Lối vào duy nhất: checkbox `@change` ở `index.blade.php:76-77` |
| 5 | `window.showLessonAjaxError` (public/js/calendar_management/ajax-error.js:13) | KHÔNG sửa | Đã kiểm `index.blade.php:5-6` và `create.blade.php:5-6` nạp `ajax-error.js` TRƯỚC `index.js` nên không undefined |
| 6 | `CalendarSalonController::editCalendarSalon` (app/Http/Controllers/Basic/CalendarSalonController.php:1009) | KHÔNG sửa | Endpoint sinh đôi bên salon, đã là `sometimes\|nullable` từ #39566 nên KHÔNG bị lỗi này (đối chứng) |
| 7 | Nơi ĐỌC cờ `enable_use_calendar`: `CalendarManagementRepository::getListCalendarActive:51`, `TemplateV2Service:3171` và `:3392`, `CalendarResource:21`, blade LIFF `bookings/layouts/main.blade.php:68`, `UserController:797` và `:3060` | KHÔNG sửa | Grep toàn `app/` xác nhận KHÔNG có job/cron nào ghi 0 (loại giả thuyết server tự tắt lịch) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarManagementController::editCalendar` — dòng 599, `calendar_name` từ `required` → `sometimes\|required` | app/Http/Controllers/Basic/CalendarManagementController.php | Direct | +10 dòng comment |
| F2 | `enableUseCalendar()` — nhánh error nhận `xhr` và gọi `window.showLessonAjaxError` | public/js/calendar_management/index.js (dòng 247-249) | Direct | +5 dòng comment |
| F3 | `Api\CalendarLessonController::getListCalendarLesson` (dòng 505-513) | app/Http/Controllers/Api/CalendarLessonController.php | Indirect | API danh sách lịch lesson cho APP Flutter — đọc `getListCalendar(botId)` rồi ép `enable_use_calendar` về boolean; bổ sung ở tự review v2, KHÔNG sửa code (rule web-only-no-outside-apis) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_management.enable_use_calendar` — tinyint(4) NOT NULL DEFAULT 1 (0: off, 1: on) | UPDATE | GHI: chỉ qua `CalendarManagementRepository::editCalendar` (endpoint đang sửa). ĐỌC: `getListCalendarActive:51`, `TemplateV2Service:3171`/`:3392`, `CalendarResource:21`, blade LIFF `bookings/layouts/main.blade.php:68`, blade màn list `index.blade.php:68/73/76/82/92/118/130`, VÀ `Api/CalendarLessonController:509`. Cột này giờ mới ghi được lại; bản ghi đang kẹt 0 tự về 1 khi khách bấm bật ⇒ KHÔNG cần recover data. |
| D2 | Field request `calendar_name` | Validate | Chỉ nới điều kiện CÓ MẶT; khi có mặt thì vẫn không rỗng + `max:10` + chặn trùng trong cùng bot (`ManagementNameValidator::isDuplicate`, loại trừ chính bản ghi) |
| D3 | `calendar_management.updated_at` | UPDATE | Mỗi lượt bật/tắt giờ thực sự được cập nhật (trước bị chặn ở validate). Không có logic nghiệp vụ nào phụ thuộc mốc này |
| D4 | Không có migration | — | KHÔNG đổi schema, KHÔNG sửa dữ liệu sẵn có |
| D5 | Job Java `linect-service` | Không liên quan | Entity `sns/line/models/linedb/entities/CalendarManagement.java` chỉ map `id`/`bot_id`/`store_name`/`calendar_name`, KHÔNG map `enable_use_calendar` ⇒ không job/cron nào đọc hay ghi cờ này |
| D6 | 15 câu ghi khác của bảng `calendar_management` (`CalendarManagementController:1297/1374/1410/1421/1475`, `SettingPaymentCalendarController:227`, `CalendarGoogleSheetService` x9, `FilterController:1264`) | Không liên quan | Đã truy toàn bộ: tất cả dùng mảng whitelist tường minh KHÔNG chứa `enable_use_calendar` ⇒ xác nhận chỉ có 1 đường ghi cờ |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn danh sách lịch (`/basic/calendar-management`) — nút bật/tắt 有効/無効 | F1, F2 | High (TRỰC TIẾP) |
| T2 | Modal 「カレンダー管理名 変更」(sửa tên quản lý lịch) | F1 | Medium (TRỰC TIẾP, phải giữ nguyên lớp chặn cũ) |
| T3 | Trang LIFF đặt lịch của khách (`bookings/layouts/main.blade.php:68` — chỉ render khi cờ = 1) | D1 | High (GIÁN TIẾP — chính là chỗ sinh triệu chứng "không dùng được chức năng đặt lịch lesson") |
| T4 | Picker chọn lịch lesson trong Tin nhắn mẫu / Step (`TemplateV2Service:3171` và `:3392`) | D1 | Medium (GIÁN TIẾP) |
| T5 | Init-data thiết lập action (`UserController:797` và `:3060`) | D1 | Medium (GIÁN TIẾP) |
| T6 | Danh sách lịch lesson trong APP Flutter (`Api/CalendarLessonController::getListCalendarLesson`) | F3, D1 | Medium (GIÁN TIẾP — bổ sung ở tự review v2, cờ ghi được lại thì trạng thái 有効/無効 trong app cũng đổi theo) |
| — | Đặt lịch salon / サロン・面談予約 (FA-020) | — | KHÔNG bị ảnh hưởng — endpoint, service, JS riêng; diff không chạm file salon nào |

> Nguyên văn Dev mục 4.3: "TRỰC TIẾP: màn danh sách lịch (/basic/calendar-management) — nút bật/tắt 有効/無効 và modal 「カレンダー管理名 変更」. GIÁN TIẾP (đọc cờ enable_use_calendar nên lịch bật lại thì xuất hiện lại): (a) trang LIFF đặt lịch của khách — bookings/layouts/main.blade.php:68 chỉ render khi cờ = 1, đây chính là chỗ sinh triệu chứng 'không dùng được chức năng đặt lịch lesson'; (b) picker chọn lịch lesson trong Tin nhắn mẫu / Step — TemplateV2Service:3171 và :3392; (c) init-data thiết lập action — UserController:797 và :3060. KHÔNG đụng Đặt lịch salon / サロン・面談予約 — FA-020 (endpoint, service, JS riêng; diff không chạm file salon nào). [tự review v2] BỔ SUNG nhóm gián tiếp (d): DANH SÁCH LỊCH LESSON TRONG APP FLUTTER - Api/CalendarLessonController::getListCalendarLesson:505-513 đọc getListCalendar(botId) rồi ép enable_use_calendar về boolean cho app => cờ ghi được lại thì trạng thái 有効/無効 trong app cũng đổi theo, QA nên retest CẢ APP chứ không chỉ web. KHÔNG sửa code Api/* (rule web-only-no-outside-apis). Đã loại khỏi phạm vi: BCCalendarResource (Api/BookingCalendar:56, Api/NotifyController:739) đọc bảng booking_calendar - tính năng khác."
>
> Cột "Nguy cơ regression" do `/new-task` gán theo mô tả rủi ro của Dev (T1/T3 "TRỰC TIẾP"/nguồn phát sinh triệu chứng → High; còn lại → Medium) — Dev không ghi mức tường minh.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
