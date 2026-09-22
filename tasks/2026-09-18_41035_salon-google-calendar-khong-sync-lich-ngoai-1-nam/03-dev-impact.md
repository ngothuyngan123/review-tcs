# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41035 — Journal #137013 (AI Reader AI Reader, 2026-09-18). Tester verify rồi tick checkbox bên dưới.
>
> ⚠️ Đánh giá do **AI Reader** viết (không phải Dev người). Verify mức **lint** — CHƯA chạy migration, CHƯA test với dữ liệu thật (bot_id 82253 / calendar_id 17841 / staff_id 27698).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI Reader (Redmine chưa có assignee) |
| Commit / Pull Request | commit `250a522b08` (12 file, +591/-3) — chưa có link PR |
| Branch | `bugs/job_resync_event_google_calendar_20260918` (repo sns-line, nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-18 |
| Auto-filled | 2026-09-18 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi salon liên kết Google Calendar lần đầu và chọn マイカレンダー, hệ thống chỉ kéo về những lịch hẹn nằm trong khoảng 1 năm kể từ thời điểm bấm liên kết. Sau lần đó, chỉ còn cơ chế nhận thông báo thay đổi từ Google đẩy về các lịch hẹn mới tạo hoặc vừa được sửa. Hệ quả: lịch hẹn nằm ngoài khoảng 1 năm đó — đặc biệt là các buổi của lịch lặp — mà từ đó tới nay không ai sửa lại trên Google thì không bao giờ được đưa về Elme. Vì phía Elme không có dữ liệu chặn, khung giờ đó vẫn hiển thị là còn trống và khách vẫn đặt được, dẫn tới nguy cơ trùng lịch. Khớp đúng với dữ liệu đã kiểm tra ở comment trước: buổi 7v154eb3rln4traa10rv7u4r23_20260919T090000Z được tạo ngày 2025-09-05 nhưng rơi vào ngày 2026-09-19, tức nằm ngoài khoảng đã đồng bộ (2025-09-05 đến 2026-09-05), nên không có dòng nào trong bảng lịch đồng bộ từ Google.

## 2. Cách fix

Lưu thêm mốc "lần đồng bộ kế tiếp" cho từng liên kết Google Calendar, đặt bằng thời điểm sync cộng 1 năm và ghi ngay từ lần liên kết đầu. Thêm một tác vụ nền chạy hằng ngày, quét các liên kết đã tới mốc đó và kéo tiếp dải lịch hẹn 1 năm kế tiếp về cho từng calendar, rồi dời mốc lên 1 năm nữa. Tác vụ chỉ thêm những buổi CHƯA CÓ: trước khi tạo, đối chiếu theo mã buổi hẹn của Google trong phạm vi salon + nhân viên + calendar tương ứng, nên chạy lại nhiều lần cũng không sinh dữ liệu trùng. Phần đọc dữ liệu từ Google và phần tạo bản ghi dùng lại đúng hàm sẵn có của luồng đồng bộ cũ, không viết lại logic. Quét ngang: lịch salon là màn duy nhất dùng cửa sổ 1 năm cố định này; lịch đặt chỗ (calendar management) đi qua luồng đồng bộ khác nên không nằm trong phạm vi sửa.

**Recover data (mục 5 Dev):**
- ✔ Không cần recover data thủ công — sau khi chạy migration, chính tác vụ nền sẽ kéo bù các buổi hẹn còn thiếu về cho từng salon.
- ⚠ Cần chạy 2 migration mới trước khi bật lịch chạy định kỳ.

**Verify (mục 6 Dev):** Mức lint. `php -l` trên toàn bộ 12 file: OK; `php artisan list`: lệnh `job:syncEventYearlyGoogleCalendarSalon` đã đăng ký và khởi tạo được (container resolve được service + 2 repository mới); `git show --stat 250a522b08`: 12 file, +591/-3.
Bằng chứng: `CalendarSalonGoogleCalendarService.php:406-408` — timeMin đặt bằng thời điểm hiện tại, timeMax bằng hiện tại cộng 1 năm, đúng là cửa sổ 1 năm cố định; hàm này chỉ được gọi từ `CalendarSalonSyncBookingFromGoogleToTool` (lúc chọn マイカレンダー) và command recover, không có nơi nào kéo lại định kỳ; `createBookingFromEvent` không hề kiểm tra trùng trước khi tạo, nên bắt buộc phải thêm bước đối chiếu mã buổi hẹn ở luồng mới; dữ liệu ở comment trước của ticket (buổi ngày 2026-09-19 tạo từ 2025-09-05) rơi đúng ngoài cửa sổ 1 năm — khớp với mô tả của khách; CHƯA chạy migration và CHƯA test với dữ liệu thật của khách.

**Tự review (AI) — rủi ro / lưu ý khi test:**
- Ngay sau khi migrate, các liên kết cũ sẽ có mốc sync nằm trong quá khứ nên lượt chạy đầu tiên đẩy tối đa 200 liên kết vào hàng đợi; có thể cần chạy tay thêm vài lượt cho hết tồn.
- Buổi hẹn đã bị xóa ở phía Elme nhưng vẫn còn trên Google sẽ được tạo lại ở lượt sync kế tiếp, do việc chống trùng dựa trên sự tồn tại của bản ghi.
- Thêm index trên `calendar_salon_booking_by_google` là thao tác nặng với bảng lớn, nên chạy vào khung giờ thấp điểm.
- Nếu gọi Google thất bại, job sẽ báo lỗi và thử lại, mốc sync giữ nguyên để không mất nguyên 1 năm dữ liệu — cần theo dõi log lượt chạy đầu tiên.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `syncEventFromGoogle` — app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php | Sửa | Ghi thêm mốc sync kế tiếp |
| 2 | `dispatchDueYearlySync` — CalendarSalonGoogleCalendarService.php | Mới | |
| 3 | `syncEventYearlyFromGoogle` — CalendarSalonGoogleCalendarService.php | Mới | |
| 4 | `__construct` — CalendarSalonGoogleCalendarService.php | Sửa | Thêm 2 repository dạng optional |
| 5 | `createBookingFromEvent` — CalendarSalonGoogleCalendarService.php | KHÔNG sửa | Tái sử dụng |
| 6 | `handle` + `failed` — app/Jobs/CalendarSalonSyncEventYearlyFromGoogle.php | Mới | |
| 7 | `handle` — app/Console/Commands/SyncEventYearlyGoogleCalendarSalon.php | Mới | |
| 8 | `schedule` + `$commands` — app/Console/Kernel.php | Sửa | Đăng ký lịch chạy 02:15 hằng ngày |
| 9 | `getCalendarsDueYearlySync` / `findActiveLinkedCalendarById` / `updateAccessToken` / `markYearlySynced` — app/Repositories/Eloquents/BCSalonGoogleCalendarRepository.php | Mới | |
| 10 | `existsSyncedGoogleEvent` — app/Repositories/Eloquents/CalendarSalonLineBookingGoogleRepository.php | Mới (chỉ thêm method) | |
| 11 | `register` — app/Providers/RepositoryServiceProvider.php | Sửa | Bind repository mới |
| 12 | `$fillable` — app/BCSalonGoogleCalendar.php | Sửa | Thêm cột `next_time_sync` |
| 13 | `CalendarSalonController@changeGoogleLinkForStaff` — app/Http/Controllers/Basic/CalendarSalonController.php | Chỉ đọc | Luồng liên kết giữ nguyên |
| 14 | `CalendarSalonSyncBookingFromGoogleToTool` — app/Jobs | Chỉ đọc | Job đồng bộ lần đầu giữ nguyên |
| 15 | `recoverGoogleCalendarSalon` — app/Console/Commands | Chỉ đọc | Command recover vẫn dùng hàm cũ |
| 16 | 3 chỗ `new CalendarSalonGoogleCalendarService()` — Api\CalendarSalonController, CalendarSalonLineBookingService, gCalendarController | Đã check | 2 repository để optional + tự resolve nên không vỡ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev ghi mục 4.1 dạng **danh sách file thay đổi**; mã F* do `/new-task` đánh để tham chiếu.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Service đồng bộ Google Calendar salon | app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php | Direct | |
| F2 | Job đồng bộ theo năm | app/Jobs/CalendarSalonSyncEventYearlyFromGoogle.php | Direct | mới |
| F3 | Command chạy định kỳ | app/Console/Commands/SyncEventYearlyGoogleCalendarSalon.php | Direct | mới |
| F4 | Lịch chạy (scheduler) | app/Console/Kernel.php | Direct | |
| F5 | Repository liên kết Google salon | app/Repositories/Eloquents/BCSalonGoogleCalendarRepository.php + app/Contracts/Repositories/BCSalonGoogleCalendarRepositoryInterface.php | Direct | mới |
| F6 | Repository lịch bận từ Google | app/Repositories/Eloquents/CalendarSalonLineBookingGoogleRepository.php + app/Contracts/Repositories/CalendarSalonLineBookingGoogleRepositoryInterface.php | Direct | |
| F7 | Service provider | app/Providers/RepositoryServiceProvider.php | Direct | |
| F8 | Model liên kết | app/BCSalonGoogleCalendar.php | Direct | |
| F9 | Migration thêm `next_time_sync` | database/migrations/2026_09_18_100000_add_next_time_sync_to_b_c_salon_google_calendar_table.php | Direct | mới |
| F10 | Migration thêm index | database/migrations/2026_09_18_100001_add_index_google_event_to_calendar_salon_booking_by_google_table.php | Direct | mới |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `b_c_salon_google_calendar.next_time_sync` (datetime, nullable) + index `idx_bcsgc_next_time_sync` | MIGRATE | |
| D2 | `b_c_salon_google_calendar.next_time_sync` của liên kết đã có | MIGRATE (UPDATE 1 lần) | = ngày kết nối Google (hoặc ngày tạo dòng) + 1 năm |
| D3 | `calendar_salon_booking_by_google` index `idx_csbbg_salon_staff_event` (calendar_salon_id, staff_id, event_id_google_calendar) | MIGRATE | Bảng rất lớn ở salon đông khách, cần cân nhắc thời điểm chạy |
| D4 | `calendar_salon_booking_by_google` + `calendar_salon_sync_booking_google_calendar_history` | CREATE | Khi tác vụ nền chạy |
| D5 | `b_c_salon_google_calendar.next_time_sync` · `sync_token_google_calendar` · `access_token` (khi token được làm mới) | UPDATE | Khi tác vụ nền chạy |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Dev không ghi mức risk — cột Nguy cơ để trống cho Leader đánh giá.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking — màn đặt lịch phía khách và màn quản lý: các khung giờ trước đây hiển thị trống sai sẽ chuyển thành đã kín sau khi dữ liệu được kéo về (đúng kết quả khách mong đợi ở ticket này) | F1, F2, D4 | |
| T2 | Liên kết Google Calendar lần đầu (chọn マイカレンダー): logic cũ giữ nguyên, chỉ ghi thêm 1 cột | F1, F8, D1 | |
| T3 | Nhận thông báo thay đổi từ Google (webhook): mã đồng bộ được ghi đè lại sau mỗi lượt sync năm, giống hành vi sẵn có của lần sync đầu tiên | F1, D5 | |
| T4 | Hàng đợi và tác vụ định kỳ: thêm 1 lệnh chạy 02:15 hằng ngày, mỗi liên kết tới hạn là 1 job; giới hạn mặc định 200 liên kết mỗi lượt để không dồn quota Google API | F2, F3, F4 | |
| T5 | Các màn đếm slot / giới hạn số lượt đặt dùng chung repository lịch Google: không ảnh hưởng, chỉ thêm method mới | F6 | |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
