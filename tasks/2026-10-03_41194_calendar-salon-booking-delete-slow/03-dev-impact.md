# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: **Journal #138767** trên Redmine #41194 (tác giả "AI LME Fix bug", 2026-09-26), do hệ thống **Auto-fixbug LME** tự sinh — ticket này không có section "Đánh giá ảnh hưởng" nằm trong description (ticket do AI check-performance tự tạo từ thống kê request chậm), mà nằm trong journal note (báo cáo fix). Đây là **bản fix thứ 3 (cuối cùng)** trên cùng 1 journal, Dev tự ghi lại cả quá trình 3 vòng điều tra — nội dung dưới đây chép **nguyên văn** mục 1–6 của journal này (đã là bản đã cập nhật sau lần 3).
>
> ⚠️ Journal #137527 (2026-09-22, "lần 1") đã bị **chính Dev phủ định một phần** ở journal này ("NAY ĐÃ GỠ") — xem mục "Lịch sử 3 lần fix" bên dưới để không nhầm migration lần 1 vẫn còn hiệu lực.
>
> Bổ sung đối chiếu **diff thật** lấy từ MCP LME TEST STUDIO (`task_get_context` task #348, section `dev_impact` + `spec_delta`) + **1 bug mới phát sinh từ chính TC Studio của task này** (Redmine #41979) ở cuối file.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `81f4db9ab3` trên nhánh `ai_small_41194` (repo `sns-line`), đã push origin — đây là trạng thái SAU lần 3 (3 file, 54 dòng thêm/1 dòng xoá so với base `6e1bfdc205`) |
| Branch | `ai_small_41194` (gốc `release_step_20260827`) |
| Ngày submit đánh giá | `2026-09-26` (Journal #138767, lần 3) |
| Auto-filled | `2026-10-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #138767 (và #137527 để hiểu lịch sử) trên Redmine, xác nhận đầy đủ 4 mục, **và đã đọc cảnh báo Redmine #41979 ở cuối file này**.

---

## Lịch sử 3 lần fix (tóm tắt để không đọc nhầm)

| Lần | Journal | Thay đổi | Trạng thái hiện tại trên branch |
|---|---|---|---|
| 1 | #137527 (2026-09-22) | Thêm migration `2026_09_21_110000` tạo chỉ mục `mobile_notify_salon_booking_index (salon_booking_id)` | ❌ **ĐÃ BỊ XOÁ** ở lần 3 |
| 2 | #138767 mục 2 (2026-09-26) | Ghim `recountAppBadgeNotify` dispatch job vào `connection('database')->queue('default')` cho 30 chỗ gọi + test `RecountAppBadgeNotifyDispatchTest` | ✅ **Còn giữ** |
| 3 | #138767 mục 2 (2026-09-26, cùng journal) | Xoá hẳn file migration của lần 1 vì Dev cho rằng DB thật **đã có sẵn** chỉ mục `salon_booking_id`; sửa lại 1 câu chú thích | ✅ Migration đã xoá, chú thích đã sửa — ⚠️ xem Redmine #41979 |

**Nội dung branch hiện tại (commit `81f4db9ab3`, 3 file, 54 dòng thêm / 1 dòng xoá):**
- `app/Helpers/functions.php` — ghim connection/queue cho `recountAppBadgeNotify`.
- `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` — chỉ sửa chú thích.
- `tests/Feature/RecountAppBadgeNotifyDispatchTest.php` — test mới (Queue::fake).
- **KHÔNG còn migration nào** liên quan tới chỉ mục `mobile_notify`.

---

## 1. Nguyên nhân

ĐÃ KIỂM TRA LẠI theo nghi vấn của dev (2026-09-26). Trong request `DELETE /basic/calendar-salon/{id}/booking/delete` chỉ có 4 việc (`Basic/CalendarSalonController::deleteBooking` → `CalendarSalonLineBookingService::delete`): (1) xoá mềm đặt lịch theo khoá chính, (2) ghi 1 dòng lịch sử, (3) xoá thông báo chưa đọc của đúng đặt lịch đó trên bảng nhật ký thông báo (`mobile_notify`), (4) gọi hàm đếm lại badge thông báo `recountAppBadgeNotify(getBotId())`.

**Điểm mới tìm được ở (4)** — đúng hướng dev nghi: hàm đếm lại badge đẩy việc sang hàng đợi NHƯNG là chỗ **DUY NHẤT** trong toàn bộ repo dispatch job mà **KHÔNG ghim connection/queue** (14 chỗ dispatch khác đều ghim `database/default` vì worker của hệ thống dựng ngoài repo và chỉ nghe lane đó). Không ghim thì connection lấy theo biến môi trường `QUEUE_DRIVER`: môi trường nào đặt `sync` thì **toàn bộ vòng đếm chạy THẲNG TRONG REQUEST** — mỗi user của bot một câu đếm trên bảng nhật ký thông báo (bảng lớn nhất hệ thống, không dọn định kỳ), bot nhiều thông báo chưa đọc và nhiều nhân viên thì cộng lại tới hàng chục giây tới hàng phút; môi trường nào trỏ lane khác thì job rơi vào lane không worker nào nghe nên badge không bao giờ được cập nhật lại. Đây là rủi ro thật, nằm đúng trong request, và không phụ thuộc chỉ mục nào cả.

Về (3) — nguyên nhân kết luận ở lần 1: câu xoá thông báo theo mã đặt lịch vẫn là việc nặng KHI bảng chưa có chỉ mục chứa `salon_booking_id` (phải mở và khoá từng dòng trong dải thông báo chưa đọc của bot). Dev cho biết chỉ mục đó nay **ĐÃ CÓ** (migration của lần 1 đã push 2026-09-22), nên phần này coi như đã được xử lý và không còn là chi phí không giới hạn trong request nữa.

⚠️ **Chưa kiểm chứng được** (Dev tự nói rõ, không kết luận quá tay): không đọc được biến `QUEUE_DRIVER` thực tế của server step; MySQL dev trong container tắt nên không chạy được `EXPLAIN`. Kết luận dựa trên đọc code + lịch sử git + quy ước dispatch của repo.

**⚠️ Diễn biến mới SAU khi journal này được viết (bổ sung bởi `/new-task`, không phải nội dung gốc của Dev):** TC Studio `NEW-12` (task #348, chạy 2026-10-03) đã **chạy `SHOW INDEX FROM mobile_notify` trên DB test thật** và phát hiện **KHÔNG có chỉ mục nào bắt đầu bằng `salon_booking_id`** — mâu thuẫn trực tiếp với giả định "DB đã có sẵn" ở trên. Xem mục "Đối chiếu diff thật" cuối file.

## 2. Cách fix

**LẦN 1** (đã push 2026-09-22 — **NAY ĐÃ GỠ**, xem lần 3): migration `2026_09_21_110000` thêm chỉ mục `mobile_notify_salon_booking_index` (`salon_booking_id`) cho bảng nhật ký thông báo + chú thích tại chỗ xoá.

**LẦN 2** (kiểm tra lại nguyên nhân theo yêu cầu dev): GHIM việc đếm lại badge vào đúng hàng đợi worker đang nghe — `recountAppBadgeNotify` nay dispatch job với `connection('database')` + `queue('default')` thay vì để mặc định theo biến môi trường `QUEUE_DRIVER`. Nhờ vậy vòng đếm badge CHẮC CHẮN nằm ngoài request ở mọi môi trường (kể cả môi trường đặt `sync`) và job cũng không rơi vào lane không ai nghe. Áp dụng cho cả **30 chỗ gọi** (xoá/huỷ đặt lịch salon và bài học, xoá bạn bè, xác nhận thông báo app...). Đã rà: KHÔNG chỗ gọi nào đọc badge ngay sau khi gọi hàm này nên dữ liệu trả về của các API không đổi. Kèm test tự động `tests/Feature/RecountAppBadgeNotifyDispatchTest.php` (`Queue::fake`) khẳng định job đi đúng lane `database/default` và không đẩy khi thiếu mã bot.

**LẦN 3** (theo spec bổ sung mới — BỎ migration chỉ mục): XOÁ hẳn file migration `2026_09_21_110000_add_index_salon_booking_to_mobile_notify_table.php` khỏi nhánh vì dev xác nhận cơ sở dữ liệu **ĐÃ CÓ SẴN** chỉ mục trên cột `salon_booking_id` — chạy thêm ALTER TABLE trên bảng nhật ký lớn là thừa và còn tốn cửa sổ deploy. Sửa kèm chú thích tại chỗ xoá thông báo trong `CalendarSalonLineBookingService::delete`: bỏ câu dẫn tới số hiệu migration vừa xoá, chỉ giữ lời nhắc câu xoá phụ thuộc chỉ mục sẵn có trên `salon_booking_id` (đừng gỡ). Đã grep toàn repo: không còn chỗ nào nhắc tên file migration hay tên chỉ mục vừa bỏ.

Verify lần 3: `php -l` file service PASS; chạy lại `RecountAppBadgeNotifyDispatchTest` — OK (2 tests, 2 assertions); `git diff 6e1bfdc205..ai_small_41194 --stat` = 3 file, 54 dòng thêm, 1 dòng xoá (không còn migration nào).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonController::deleteBooking` (`app/Http/Controllers/Basic/CalendarSalonController.php`) | Không đổi | Caller chính — entrypoint của ticket |
| 2 | `CalendarSalonLineBookingService::delete` (`app/Services/CalendarSalon/CalendarSalonLineBookingService.php:4383`) | Có — chỉ chú thích (lần 1 trỏ migration, lần 3 sửa lại cho khỏi lỗi thời) | Xoá mềm theo khoá chính, ghi 1 dòng lịch sử, xoá thông báo chưa đọc, gọi đếm badge |
| 3 | `CalendarSalonLineBookingRepository::deleteBooking` (`app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php:491`) | Không đổi | Xoá mềm theo khoá chính |
| 4 | `CalendarSalonLineBookingHistoryRepository::create` (`app/Repositories/Eloquents/CalendarSalonLineBookingHistoryRepository.php:27`) | Không đổi | Insert 1 dòng lịch sử |
| 5 | `recountAppBadgeNotify` (`app/Helpers/functions.php:4664`) | **Có** — ghim `connection('database')->queue('default')` | Root cause chính (lần 2) |
| 6 | `RecountAppBadgeNotify::handle` + `getBotUserIds` (`app/Jobs/RecountAppBadgeNotify.php`) | Không đổi | Logic đếm lại badge |
| 7 | `MobileBadgeNotifyRepository::recountUnconfirmNotify` / `setCount` / `increment` (`app/Repositories/Eloquents/MobileBadgeNotifyRepository.php:74`) | Không đổi | Ghi giá trị badge cuối |
| 8 | **30 chỗ gọi `recountAppBadgeNotify`** (NotifySettingController, Admin/BotController, Basic+Mobile/CalendarSalonController, BookingManagerController, CalendarManagementController, Mobile/CalendarController, FriendlistController, BookingAjaxController, Api/NotifyController 908/1018/1081, Mobile/MobileNotifyController:115, Api/FriendInformationController, CalendarCourseService, CalendarCourseBookingService, HandlePushMessageNotify, recoverCountNotifyApp) | Hưởng chung thay đổi ở #5 (không sửa riêng từng chỗ) | Đã rà KHÔNG chỗ nào đọc badge ngay sau khi gọi hàm này |
| 9 | 14 chỗ dispatch job khác của repo | Không đổi | Đối chiếu quy ước ghim `onConnection('database')->onQueue('default')` — xác nhận #5 là chỗ duy nhất thiếu |
| 10 | `NotifyChatworkRequestTimeSlow` (`app/Http/Middleware/NotifyChatworkRequestTimeSlow.php`) | Không đổi | Xác nhận số giây báo chậm là thời gian chạy thật của controller (nguồn cảnh báo ticket) |
| 11 | `config/queue.php:18` (`'default' => env('QUEUE_DRIVER','database')`) | Không đổi | Xác nhận biến môi trường chi phối hành vi trước fix |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `recountAppBadgeNotify` — ghim connection/queue | `app/Helpers/functions.php` | Direct | Lần 2, giữ nguyên ở lần 3 |
| F2 | `CalendarSalonLineBookingService::delete` | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Direct (chú thích only) | Lần 3 sửa lại chú thích cho khỏi trỏ migration đã xoá |
| F3 | `RecountAppBadgeNotifyDispatchTest` (test mới) | `tests/Feature/RecountAppBadgeNotifyDispatchTest.php` | Direct (test) | Queue::fake — khẳng định lane, KHÔNG đo hiệu năng |
| F4 | Migration `2026_09_21_110000_add_index_salon_booking_to_mobile_notify_table` | `database/migrations/...` | **ĐÃ XOÁ** (lần 3) | ⚠️ Xem Redmine #41979 — giả định "DB đã có sẵn" chưa được xác nhận đúng trên DB test |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `mobile_notify` | Không tạo/gỡ chỉ mục nào trong migration của nhánh này | Chỉ mục `salon_booking_id` theo Dev là "đã có sẵn trên DB thật" — **chưa kiểm chứng được, xem cảnh báo #41979** |
| D2 | `mobile_badge_noitfy` (tên bảng có lỗi chính tả trong DB) | Không đổi cấu trúc | Badge cập nhật qua worker ngay sau request thay vì có thể ghi đồng bộ khi `QUEUE_DRIVER=sync`; giá trị cuối cùng tính lại từ dữ liệu thật |
| D3 | `jobs` | INSERT | Mỗi lần gọi `recountAppBadgeNotify` ghi 1 bản ghi job vào lane `database/default` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — xoá đặt lịch Salon | F1, F2, D1, D3 | High — response/thông báo bị xoá không đổi nhưng phần đếm badge chắc chắn không còn nằm trong request; thời gian request chỉ cải thiện thật nếu chỉ mục `salon_booking_id` tồn tại |
| T2 | Notification Settings (FA-006) — badge thông báo app | F1, D2, D3 | Medium — badge cập nhật trễ qua hàng đợi ở **mọi** môi trường (kể cả trước đây có thể đồng bộ); cần worker lane `database/default` đang chạy |
| T3 | Các luồng khác cùng gọi `recountAppBadgeNotify` (huỷ đặt lịch Salon từ app, xoá đặt lịch bài học, xoá bạn bè đã chặn, xác nhận thông báo app) | F1 (30 chỗ gọi) | Medium — cùng đổi sang chạy nền, cùng phụ thuộc worker |
| T4 | Deploy/DB | F4 | Low (nếu Dev đúng) / **High (nếu Redmine #41979 đúng)** — môi trường dựng mới từ migration của repo sẽ **thiếu hẳn** chỉ mục `salon_booking_id` vì không còn migration nào tạo nó |

---

## 5. Recover data (nguyên văn journal)

✔ Không cần recover data

## 6. Verify của Dev (nguyên văn journal)

- **Mức:** test
- **Lệnh:** `php -l app/Services/CalendarSalon/CalendarSalonLineBookingService.php` → No syntax errors (lần 3); `vendor/bin/phpunit --filter RecountAppBadgeNotifyDispatchTest` → OK (2 tests, 2 assertions); `grep` toàn repo chuỗi `2026_09_21_110000` và `mobile_notify_salon_booking_index` → KHÔNG còn chỗ nào tham chiếu; `git diff 6e1bfdc205..ai_small_41194 --stat` → 3 file, 54 dòng thêm, 1 dòng xoá.
- **Bằng chứng:** Dev xác nhận trong spec bổ sung: chỉ mục trên `salon_booking_id` đã có sẵn trên DB nên không cần migrate; `git grep` trên `origin/release_step_20260827 -- database/migrations`: không có migration nào khác tạo chỉ mục cho `salon_booking_id` ⇒ chỉ mục hiện có (theo Dev) là do DBA/thao tác ngoài repo, KHÔNG nằm trong lịch sử migration.
- ⚠️ **Dev tự nêu:** MySQL dev `host.docker.internal:3306` từ chối kết nối trong phiên làm việc ⇒ **KHÔNG tự kiểm chứng được chỉ mục bằng `SHOW INDEX`**, ghi nhận hoàn toàn theo "xác nhận của dev" (không rõ nguồn). **→ Đây chính xác là khoảng trống mà Redmine #41979 phát hiện ra là SAI.**

## Rủi ro Dev tự nêu (nguyên văn journal)

- Chỉ mục `salon_booking_id` không nằm trong lịch sử migration của repo ⇒ môi trường dựng mới từ migration sẽ **THIẾU** chỉ mục này. Nếu muốn ghi nhận lâu dài thì cần một ticket/migration riêng do DB team chốt.
- Badge cập nhật qua hàng đợi ở mọi môi trường: cần worker lane `database/default` thực sự đang chạy.
- Chưa đo được bằng EXPLAIN/log thật vì MySQL dev trong container đang tắt.

---

## Đối chiếu diff thật (MCP LME TEST STUDIO — `task_get_context` task #348)

> `diffAvailable = true`, `diffStrategy = stat`. Khớp với Journal #138767 ở trên.

- **Files đổi** (diffstat): `app/Helpers/functions.php` (+14/-1) · `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` (+3) · `tests/Feature/RecountAppBadgeNotifyDispatchTest.php` (+38 mới). Tổng 3 file, 54 dòng thêm / 1 dòng xoá.
- **`dev_impact` (Studio tự suy từ diff):**
  - Hàm dùng chung `recountAppBadgeNotify`: job đếm badge luôn ghi vào bảng `jobs` (connection `database`, queue `default`), không còn chạy đồng bộ trong request kể cả env `QUEUE_DRIVER=sync`.
  - Luồng xoá đặt lịch Salon (`EP-A62`): logic không đổi; cần regression xoá mềm booking, lịch sử xoá, xoá `mobile_notify` chưa đọc đúng scope booking/bot/type, response JSON.
  - Thời gian phản hồi xoá booking: **chỉ giảm nếu trước đây đếm badge chạy sync**; câu xoá `mobile_notify` **vẫn phụ thuộc chỉ mục `salon_booking_id` không có trong migration và không có ở DB test**.
  - Badge app của owner/staff/notify_setting user: nay cập nhật trễ theo worker; rủi ro không cập nhật nếu không có worker `database/default`.
  - **29 chỗ gọi khác** (huỷ booking Salon từ app, xoá calendar Salon, booking Lesson/Calendar, xoá/chặn bạn bè, xác nhận thông báo app, lưu cài đặt thông báo, command push notify/recover) — cùng đổi sang chạy nền.
  - Job không đổi constructor nên job cũ đang chờ trong hàng đợi lúc release vẫn chạy được.
- **8 requirements** Studio tự suy (`REQ-001`…`REQ-008`) — đáng chú ý **`REQ-008`**: "Bảng thông báo app có chỉ mục trên `salon_booking_id` ở môi trường release" — risk **High**, mô tả rõ "thiếu thì báo DBA trước release". Đây chính là requirement mà TC `NEW-12` verify và **FAIL**.

### 🔴 Bug phát sinh từ chính TC Studio của task này — Redmine #41979

> Ticket mới (`status: New`, severity Medium, tracker "Bug Tester", tạo 2026-10-03 bởi "AI Auto test Lme"), KHÔNG phải do `/new-task` suy diễn — fetch trực tiếp để đối chiếu.

- **Nguồn:** TC Studio `NEW-12` (task #348) — code test `web@81f4db9a` (nhánh `ai_small_41194`).
- **Các bước tái hiện (nguyên văn Redmine):**
  1. Trên DB test, chạy `SHOW INDEX FROM mobile_notify`.
  2. Chạy `EXPLAIN SELECT * FROM mobile_notify WHERE salon_booking_id = 12071 AND bot_id = 993965586 AND type = 10 AND is_confirm = 0`.
  3. Đối chiếu repo nhánh `ai_small_41194`: tìm migration tạo chỉ mục `salon_booking_id` cho `mobile_notify`.
- **Kết quả thực tế:** `SHOW INDEX` chỉ có `PRIMARY(id)` và `mobile_notify_badge_recount_index(bot_id, is_confirm, status, user_id)` — **không có chỉ mục nào chứa `salon_booking_id`**. `EXPLAIN` chọn `key = mobile_notify_badge_recount_index` (theo `bot_id`, không phải theo `salon_booking_id`). Repo **không có migration** tạo chỉ mục này (migration đã bị gỡ ở commit `81f4db9ab3`). Tái hiện độc lập 2 lần (run #2588, #2596) + kiểm chứng bằng `mysql` CLI trực tiếp, cùng kết quả. TC đo hiệu năng `NEW-5` (id Studio 21557) bị **BLOCK** vì cùng nguyên nhân.
- **Kết quả mong đợi (theo bug):** `mobile_notify` phải có ít nhất một chỉ mục có cột đầu `salon_booking_id`, và `EXPLAIN` câu xoá thông báo phải chọn chỉ mục đó. Cần **DBA xác nhận trên step/production**; nếu môi trường thật cũng thiếu thì **cần migration** (khác với kết luận "đã có sẵn" ở Journal #138767 lần 3).
- **Tác động tới việc review task #41194:** đây là **mâu thuẫn trực tiếp giữa lời khai của Dev và bằng chứng kỹ thuật độc lập**. Bug #41979 hiện `status=New`, **chưa được Dev confirm/fix** — tức là tại thời điểm `/new-task` này chạy, **chưa đủ căn cứ để coi lần 3 (xoá migration) là an toàn**. Leader/Tester nên: (a) không tự ý thêm lại migration khi chưa xác nhận; (b) bắt buộc chạy TC `NEW-12`/`NEW-5` trên **step/production thật** (không chỉ DB test) trước khi coi request xoá đặt lịch Salon đã hết chậm; (c) theo dõi #41979 song song với #41194.
