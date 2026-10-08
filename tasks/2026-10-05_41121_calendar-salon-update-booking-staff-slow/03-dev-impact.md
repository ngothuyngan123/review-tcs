# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: **Journal #137390** trên Redmine #41121 (tác giả "AI LME Fix bug", 2026-09-21), do hệ thống **Auto-fixbug LME** tự sinh — ticket này không có section "Đánh giá ảnh hưởng" nằm trong description (ticket do AI check-performance tự tạo từ thống kê request chậm), mà nằm trong journal note (báo cáo fix). Dev tự ghi nhận đây là **"sửa lần 2"** theo quyết định vận hành của human (lần 1 không có journal riêng — chỉ được nhắc lại trong chính note này ở mục "Nền tảng lần 1 giữ nguyên"). Nội dung dưới đây chép **nguyên văn** mục 1–6 của journal.
>
> Bổ sung đối chiếu **diff thật** lấy từ MCP LME TEST STUDIO (`task_get_context` task #349, section `dev_impact` + `spec_delta`) ở cuối file.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `f02a52db01` trên nhánh `ai_small_41121` (repo `sns-line`), đã push origin (5 file, 224 dòng thêm / 7 dòng xoá, 2 commit) |
| Branch | `ai_small_41121` (gốc `release_step_20260827`) |
| Ngày submit đánh giá | `2026-09-21` (Journal #137390) |
| Auto-filled | `2026-10-05 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #137390 trên Redmine, xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact), **và đã đọc mục "Hành vi có đổi" + "Rủi ro Dev tự nêu" ở cuối file này**.

---

## 1. Nguyên nhân

Khi tắt hiển thị nhân viên trên trang đặt lịch (`booking_page_display=0`), endpoint chạy TOÀN BỘ việc gỡ liên kết Google Calendar ngay trong request: xoá từng sự kiện trên Google cho mọi lượt đặt đã đồng bộ (mỗi lượt = 1 lần gọi HTTP sang Google + 3 câu truy vấn), rồi xoá theo lô toàn bộ dữ liệu đồng bộ và lịch sử đồng bộ (bảng lịch sử có thể tới hàng triệu dòng cho 1 salon/nhân viên). Khối lượng việc tỉ lệ thuận với dữ liệu tích luỹ và không có trần.

Tệ hơn: bảng lịch sử đồng bộ và bảng lượt đặt salon đều KHÔNG có index theo (salon, nhân viên) nên câu tìm lượt đặt quét toàn bảng, còn vòng xoá theo lô thì MỖI lô lại quét toàn bảng + khoá khoảng — xoá hàng triệu dòng trở thành chi phí bậc hai. Nhân viên có nhiều lịch sử đồng bộ thì request treo tới 471s.

## 2. Cách fix

Sửa lần 2 theo quyết định human:
1. **BỎ chốt kiểm cờ hiển thị trong job** — đã đẩy vào hàng đợi là CHẮC CHẮN gỡ liên kết Google; người dùng bật hiển thị lại trong lúc chờ cũng không huỷ được, muốn dùng lại thì phải liên kết Google lại từ màn cấu hình nhân viên.
2. **Chuyển job sang connection + queue RIÊNG** (`database_salon_google` / `salonGoogleUnlink`) thay vì `database`/`default` để việc nặng không chiếm worker dùng chung — connection mới cùng bảng `jobs` nhưng `retry_after=7200` > timeout job `3600` nên job dài không bị nhả ra chạy trùng và không sinh bản ghi `failed_jobs` giả.
3. **Thêm `failed()`** ghi `logError` + `notifyChatworkException` để dev biết khi job hỏng giữa chừng (`tries=1` nên dữ liệu có thể dọn dở).

Nền tảng **lần 1** giữ nguyên: toàn bộ khối gỡ liên kết Google ra khỏi request (request chỉ lưu cờ hiển thị rồi trả JSON y hệt cũ) + 2 migration index (`calendar_salon_id`, `staff_id`) cho `calendar_salon_sync_booking_google_calendar_histories` và `calendar_salon_line_booking`.

Verify (nguyên văn mục 6): `php -l` 3 file sửa lần 2 (job, controller, `config/queue.php`) — No syntax errors; boot Laravel trong worktree xác nhận `tries=1`, `timeout=3600`, `CONNECTION=database_salon_google`, `QUEUE=salonGoogleUnlink`, `retry_after=7200` > timeout job (không bị re-reserve chạy trùng); đã bỏ hẳn guard `booking_page_display` khỏi job; `failed()` + `notifyChatworkException` tồn tại; `git diff --stat release_step_20260827...ai_small_41121`: 5 file, 224 thêm / 7 bớt (2 commit).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Basic\CalendarSalonController::updateBookingPageDisplayStaff` (`app/Http/Controllers/Basic/CalendarSalonController.php:1181`) | Có | Entrypoint — nay chỉ lưu cờ + dispatch job, không còn gỡ Google đồng bộ trong request |
| 2 | `App\Jobs\CalendarSalonDeleteGoogleSyncStaff::handle` (`app/Jobs/CalendarSalonDeleteGoogleSyncStaff.php`) | Có (file mới) | Toàn bộ logic gỡ liên kết Google chuyển vào đây, chạy nền ở queue riêng |
| 3 | `CalendarSalonGoogleCalendarService::deleteBookingSyncFromLme` (`app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php:413`) | Không đổi logic | Caller từ job — xoá liên kết + dữ liệu đồng bộ |
| 4 | `CalendarSalonGoogleCalendarService::deleteEventByBookingId` + `executeDeleteEventByBookingSalon` (cùng file, ~161/~952) | Không đổi | Xoá từng sự kiện Google theo lượt đặt; lỗi Google (401/403/404/400) bị catch, không làm job fail |
| 5 | `CalendarSalonBookingByGoogleService::deleteBookingByGoogleCalendar` + `deleteInChunks` (`app/Services/CalendarSalon/CalendarSalonBookingByGoogleService.php:101/124`) | Không đổi | Xoá theo lô `calendar_salon_booking_by_google` + lịch sử đồng bộ |
| 6 | `CalendarSalonStaffService::updateBookingPageStaff` (`app/Services/CalendarSalon/CalendarSalonStaffService.php:84`) | Không đổi | Lưu cờ hiển thị |
| 7 | `updateBookingPageDisplayStaff` (`public/js/calendar_salon/calendar_detail.js:2057`) | Không đổi | Phía gọi — sau khi success chỉ reload danh sách nhân viên |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarSalonController::updateBookingPageDisplayStaff` | `app/Http/Controllers/Basic/CalendarSalonController.php` | Direct | Chỉ lưu cờ + dispatch job, trả JSON y hệt cũ |
| F2 | `CalendarSalonDeleteGoogleSyncStaff::handle` (job mới) | `app/Jobs/CalendarSalonDeleteGoogleSyncStaff.php` | Direct | `tries=1`, `timeout=3600`, không kiểm lại cờ hiển thị, có `failed()` |
| F3 | `config/queue.php` — connection `database_salon_google` | `config/queue.php` | Direct | `retry_after=7200`; cần worker riêng, không có worker ⇒ job nằm im |
| F4 | `CalendarSalonGoogleCalendarService` / `CalendarSalonBookingByGoogleService` (gỡ liên kết + xoá theo lô) | 2 file service | Indirect | Logic không đổi — nay chạy nền thay vì trong request; hưởng 2 index mới |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_line_booking.google_event_id` / `google_calendar_id` | UPDATE (set null) | Vẫn xoá như cũ, nay chạy nền; thêm index `(calendar_salon_id, staff_id)` |
| D2 | `calendar_salon_sync_booking_google_calendar_histories` | DELETE theo lô | Vẫn xoá như cũ, nay chạy nền; thêm index `(calendar_salon_id, staff_id)` — bảng có thể tới hàng triệu dòng |
| D3 | `calendar_salon_booking_by_google` | DELETE theo lô | Vẫn xoá như cũ, chạy nền; **KHÔNG** được thêm index trong diff này ⇒ mỗi lô vẫn quét toàn bảng |
| D4 | `bc_salon_google_calendars` | DELETE | Bản ghi liên kết Google của nhân viên vẫn bị xoá, **sau khi job chạy xong**; bật hiển thị lại KHÔNG cứu được bản ghi này (quyết định human 2026-09-21) |
| D5 | `jobs` / `failed_jobs` | INSERT | Job mới nằm ở queue riêng `salonGoogleUnlink` (vẫn bảng `jobs`); `failed_jobs` chỉ ghi khi job thật sự hỏng |
| D6 | `database/migrations/2026_09_18_110001_...` + `..._110002_...` | MIGRATE (CREATE INDEX) | 2 migration index trên 2 bảng lớn — khuyến nghị chạy giờ thấp điểm |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — tắt hiển thị nhân viên trên trang đặt lịch | F1, F2, D4, D5 | High — phản hồi ngay; việc gỡ liên kết Google chạy nền ở hàng đợi riêng và **không thể huỷ** bằng cách bật hiển thị lại |
| T2 | Salon Booking (FA-020) — gỡ liên kết Google thủ công / callback OAuth / xoá nhân viên, xoá calendar (luồng dùng chung service) | F4, D1, D2 | Medium — không sửa code, chỉ nhanh hơn nhờ 2 index mới; cần regression không bị đụng |
| T3 | Vận hành / Ops — worker queue `salonGoogleUnlink` | F3 | High — thiếu worker thì liên kết Google không bao giờ được gỡ dù UI báo thành công |

---

## 5. Recover data (nguyên văn journal)

✔ Không cần recover data

## 6. Verify của Dev (nguyên văn journal)

- **Mức:** runtime-data
- **Lệnh:** `php -l` 3 file sửa lần 2 (job, controller, `config/queue.php`): No syntax errors detected; Boot Laravel trong worktree: `tries=1`, `timeout=3600`, `CONNECTION=database_salon_google`, `QUEUE=salonGoogleUnlink`; `config('queue.connections.database_salon_google')` resolve OK, `retry_after=7200` > timeout job `3600` (không bị re-reserve chạy trùng), queue mặc định của connection = `salonGoogleUnlink`, class = `Illuminate\Queue\DatabaseQueue`; xác nhận đã bỏ hẳn guard `booking_page_display` khỏi job; method `failed()` tồn tại; helper `notifyChatworkException` tồn tại; `git diff --stat release_step_20260827...ai_small_41121`: 5 file, 224 thêm / 7 bớt (2 commit).
- **Bằng chứng:** Không EXPLAIN được trên dev: MySQL `host.docker.internal:3306` 'Connection refused' — kết luận thiếu index dựa trên migration 2 bảng + lesson #38446 (EXPLAIN cũ: `type=ALL, key=NULL, rows=42358`); migration index của #39523 có commit nhưng KHÔNG có trong cây `release_step_20260827` (rơi khi merge) ⇒ bảng histories thật sự chưa có index ngoài PRIMARY; tên index mới không trùng; quy ước queue riêng đã có sẵn trong repo (`googleEvent`, `googleFormAnswer`, `countView`) nên cách đặt queue riêng là nhất quán.

## Hành vi có đổi (human chốt 2026-09-21 — KHÔNG phải spec cũ)

- Tắt rồi bật lại ngay thì liên kết Google **vẫn bị gỡ** — người dùng phải liên kết Google lại. Cần PM/CS biết để trả lời khách.
- Bất đồng bộ: từ lúc trả về tới khi job xong, tab `Google連携` của nhân viên còn hiện đang liên kết trong chốc lát.

## Rủi ro Dev tự nêu (nguyên văn journal)

- ⚠ **BẮT BUỘC ops**: phải thêm worker cho queue mới, ví dụ `php artisan queue:work database_salon_google --queue=salonGoogleUnlink` (supervisor). Nếu không có worker lắng nghe, job nằm im vĩnh viễn ⇒ liên kết Google KHÔNG bị gỡ dù đã tắt hiển thị.
- `tries=1`: job hỏng giữa chừng thì dọn dở và không tự chạy lại — nay đã có `failed()` ghi log + báo Chatwork để dev xử lý tay.
- Tạo index trên 2 bảng rất lớn: chạy migration vào giờ thấp điểm (đã ghi cảnh báo trong migration).

---

## Đối chiếu diff thật (MCP LME TEST STUDIO — `task_get_context` task #349)

> `diffAvailable = true`, `diffStrategy = stat`. Khớp với Journal #137390 ở trên.

- **Files đổi** (diffstat, 5 file / 224 thêm / 7 bớt):
  - `app/Http/Controllers/Basic/CalendarSalonController.php` (-)
  - `app/Jobs/CalendarSalonDeleteGoogleSyncStaff.php` (+119, file mới)
  - `config/queue.php` (+14)
  - `database/migrations/..._add_index_salon_staff_to_calendar_salon_sync_booking_google_calendar_histories_table.php` (+41, mới)
  - `database/migrations/..._add_index_salon_staff_to_calendar_salon_line_booking_table.php` (+40, mới)
- **`dev_impact` (Studio tự suy từ diff):**
  - `EP-A47 POST /basic/calendar-salon/staff/update-booking-page-display-staff`: khi `booking_page_display=0`, không còn gỡ liên kết Google trong request mà dispatch job `CalendarSalonDeleteGoogleSyncStaff` (connection `database_salon_google`, queue `salonGoogleUnlink`); `booking_page_display=1` không đổi hành vi (chỉ lưu cờ).
  - Response JSON `{success, data, message}` giữ nguyên; FE `calendar_detail.js` không đổi (chỉ reload list staff khi success).
  - Job mới: `tries=1`, `timeout=3600`, không kiểm lại cờ hiển thị; xoá Google event từng booking có `google_event_id` → set null `google_event_id`/`google_calendar_id` → xoá theo lô `calendar_salon_booking_by_google` + histories → xoá `bc_salon_google_calendar` của (calendar, staff).
  - `failed()`: `logError` + `notifyChatworkException`; lỗi Google từng event (401/403/404/400) vẫn bị catch trong `deleteEventByBookingId` (ghi `ResultErrorGoogle`, set `status_connect_gg_calendar=0`) nên **thường KHÔNG** làm job fail.
  - `config/queue.php` thêm connection `database_salon_google` (bảng `jobs`, `retry_after=7200`) — cần worker riêng; không có worker ⇒ job nằm im, liên kết Google không bao giờ được gỡ.
  - 2 migration index `(calendar_salon_id, staff_id)` trên `calendar_salon_sync_booking_google_calendar_histories` và `calendar_salon_line_booking` — bảng lớn, chạy giờ thấp điểm; ảnh hưởng tốc độ cả các luồng dùng chung.
  - Hành vi đổi (human chốt 2026-09-21): tắt rồi bật lại hiển thị vẫn bị gỡ liên kết Google; tab `連携設定` chỉ liệt kê staff đang hiển thị, nên chỉ khi bật lại **trước khi job chạy** mới thấy staff còn hiện đang liên kết.
  - **Rủi ro race (Studio suy luận từ code, chưa xác nhận)**: re-link Google qua OAuth (`EP-A89`) TRƯỚC khi job chạy ⇒ job xoá theo (calendar, staff) lúc chạy nên có thể xoá luôn liên kết mới + event mới đồng bộ. **Chưa có expected chính thức — cần PO chốt** (xem TC `NEW-11` ở `04-tc-list.md`, hiện đang `skip`).
  - Luồng dùng chung service (không đổi code, hưởng index): gỡ liên kết thủ công `deleteGoogleSyncLink`, OAuth callback, xoá staff (`EP-A43`), xoá calendar (`EP-A11`) — vẫn chạy đồng bộ trong request.
  - Pre-existing (ngoài scope fix): `EP-A47` không kiểm staff thuộc bot/calendar hiện tại; `calendar_id` lấy từ request được truyền thẳng vào job.
  - **Rủi ro FE (phân tích tĩnh, Studio flag)**: `staff_list.blade.php:256` `@click` truyền `item.booking_page_display` TRƯỚC khi `v-model` cập nhật ⇒ có thể gửi giá trị cũ; bật lại có thể gửi `0` và kích hoạt gỡ Google ngoài ý muốn. TC `NEW-4` của Studio chủ đích bắt case này (đã PASS trên local).
  - `calendar_salon_booking_by_google` KHÔNG được thêm index ⇒ `deleteInChunks` trên bảng này vẫn quét toàn bảng mỗi lô (trong job) — không ảnh hưởng thời gian request nữa nhưng ảnh hưởng thời lượng job trên production.

### Studio task #349 — kết quả chạy TC (round 1)

- 20 TC: **18 Đạt** · 0 Không đạt · **2 Skip** (`NEW-3` — cần tài khoản Google thật + app LINE thật, exec_mode manual, chưa chạy; `NEW-11` — case liên kết lại Google trong lúc job cũ còn chờ, **chờ PO chốt expected**, chưa được dùng để đánh pass/fail).
- `reviewState = leader` — Studio đang chờ Leader duyệt review, chưa phải kết luận cuối.
- Chi tiết từng TC + cảnh báo rủi ro chưa verify (race re-link Google, FE `@click` trước `v-model`) — xem `04-tc-list.md`.
