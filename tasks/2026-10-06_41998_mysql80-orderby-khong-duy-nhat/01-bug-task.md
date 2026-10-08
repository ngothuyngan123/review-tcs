# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41998 — [WEB-R2] Nâng MySQL 5.7 → 8.0: ORDER BY cột không duy nhất + LIMIT/OFFSET` |
| Module / Màn hình | Đa màn hình (phân trang LIMIT/OFFSET theo cột không duy nhất): Chat 1:1 (FA-001) — danh sách hội thoại web + mobile web + API app · Lịch sử hành động QR của bạn bè (FA-017) · Lịch đặt chỗ Lesson (FA-019) · Lịch đặt chỗ Salon (FA-020) |

## Mô tả bug (bản dịch tiếng Việt)

> Đây là **luận điểm phát hiện qua đối chiếu kỹ thuật** (review migration MySQL 5.7 → 8.0), không phải bug do khách hàng report qua thao tác thực tế — xem ghi chú ở mục "Steps to reproduce" bên dưới.

*Luận điểm R2 — ORDER BY cột không duy nhất + LIMIT/OFFSET — thứ tự các dòng "hoà" đổi theo plan* · Project: sns-line (web Laravel)
Nguồn: báo cáo đối chiếu MySQL 8 — https://dashboard.melonglobal.net/fixbug-lme/mysql80-report/#result/R2 · ticket gốc #39528
Code đối chiếu: release_step_20260930_v2 @441407307e · Máy B: MySQL 8.0.46-0ubuntu0.22.04.4

### 1. Mô tả luận điểm

*Thay đổi 5.7 → 8.0:* SQL không đảm bảo thứ tự giữa các dòng có cùng giá trị ORDER BY. Trên 5.7 thứ tự này "ổn định nhờ plan ổn định". 8.0 đổi plan (P2/P3), đổi thuật toán sort (filesort với LIMIT dùng priority queue, packed sort keys) ⇒ thứ tự dòng hoà đổi, và có thể khác giữa lần lấy trang 1 và trang 2.

*Điều kiện kích hoạt:* Phân trang LIMIT/OFFSET theo cột hay trùng giá trị: last_time_message (broadcast làm hàng loạt hội thoại có cùng thời điểm), followed_at, created_at, date_booking + start_time, is_bookmark. Có id ở cuối ORDER BY thì an toàn.

*Tác động:* Trang sau lặp người/bản ghi của trang trước hoặc bỏ sót — staff không thấy hội thoại, tool AI xử lý trùng/thiếu.

*Bằng chứng:* Không cần runtime để kích hoạt; xác suất tăng theo số dòng hoà. Đối chứng an toàn: TagHistoryRepository (web) có `created_at DESC, id DESC`.

### 2. Các item ảnh hưởng (4)

| # | Ưu tiên | Logic / tính năng | Vị trí | Bảng dữ liệu (B) |
|---|---|---|---|---|
| 1 | Cao | ★ Màn chat — danh sách bạn bè / tìm bạn (get-friends) | app/Services/ConversationService.php:196 | conversation 49.783.904 dòng (24,8 GiB) |
| 2 | Trung bình | Màn chat 1:1 (không ES) | app/Http/Controllers/ChatController.php:259 | conversation 49.783.904 dòng (24,8 GiB) |
| 3 | Trung bình | Lịch sử hành động QR của bạn bè | app/Repositories/Eloquents/QrActionHistoryRepository.php:51 | detail_landing_click 31.320.190 dòng (18,8 GiB) |
| 4 | Thấp | Lịch khoá học — danh sách đặt chỗ (tab1) | app/Services/CalendarManagement/CalendarCourseService.php:1194 | calendar_course_bookings 496.824 dòng (1,4 GiB) |

*1. ★ Màn chat — danh sách bạn bè / tìm bạn (get-friends)*
- Vị trí: app/Services/ConversationService.php:196
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Cao — Danh sách chat staff dùng liên tục; nhiều hội thoại trùng last_time_message sau broadcast
- Rủi ro: `ORDER BY is_bookmark DESC, last_time_message DESC LIMIT 20 OFFSET (page-1)*20` — không có conversation.id.

```
app/Services/ConversationService.php @ 441407307e  (dòng 196-200, * = dòng rủi ro)
  196*             $data = $data->orderBy('conversation.is_bookmark', 'DESC')
  197              ->orderBy('conversation.last_time_message', 'DESC')
  198              ->offset(($request['page'] - 1) * 20)
  199              ->limit(20)
  200              ->get();
```

*2. Màn chat 1:1 (không ES)*
- Vị trí: app/Http/Controllers/ChatController.php:259
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Sai hiển thị / thứ tự / xuất file — không gửi tin cho khách
- Rủi ro: Cùng ORDER BY, simplePaginate.

```
app/Http/Controllers/ChatController.php @ 441407307e  (dòng 255-262, * = dòng rủi ro)
  255              })
  256              ->when(!empty($line_id), function ($sql) use ($line_id) {
  257                  $sql->where("conversation.tb_line_user_id", $line_id);
  258              })
  259*             ->orderBy('conversation.is_bookmark', 'DESC')
  260              ->orderBy('conversation.last_time_message', 'DESC')
  261              ->simplePaginate(30);
```

*3. Lịch sử hành động QR của bạn bè*
- Vị trí: app/Repositories/Eloquents/QrActionHistoryRepository.php:51
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Sai hiển thị / thứ tự / xuất file — không gửi tin cho khách
- Rủi ro: ORDER BY detail_landing_click.time_click DESC + paginate.

```
app/Repositories/Eloquents/QrActionHistoryRepository.php @ 441407307e  (dòng 48-53, * = dòng rủi ro)
   48                  DB::raw('landing.name as qr_name'),
   49                  DB::raw('category.name as folder_name')
   50              )
   51*             ->orderBy('detail_landing_click.time_click', 'desc')
   52              ->paginate($perPage, ['*'], 'page', $page);
```

*4. Lịch khoá học — danh sách đặt chỗ (tab1)*
- Vị trí: app/Services/CalendarManagement/CalendarCourseService.php:1194
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Thấp — Bảng < 5 triệu dòng, ít dữ liệu bị ảnh hưởng
- Rủi ro: ORDER BY user_update_time DESC + paginate.

```
app/Services/CalendarManagement/CalendarCourseService.php @ 441407307e  (dòng 1191-1196, * = dòng rủi ro)
 1191              ->when($condition == 'tab1', function ($query) {
 1192                  $query->whereBetween(DB::raw('DATE(calendar_course_bookings.user_update_time)'), [Carbon::now()->subDays(7)->toDateString(), Carbon::now()->toDateString()])
 1193                      ->where('calendar_course_receptions.received_booking_date', '>=', Carbon::now()->format('Y-m-d'))
 1194*                     ->orderBy('calendar_course_bookings.user_update_time', 'desc');
 1195              })
```

### 3. Hướng xử lý

Thêm khoá phụ duy nhất (id) vào cuối mọi ORDER BY dùng cho phân trang.

## Steps to reproduce

<!-- Không có — xem ghi chú dưới. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Không có attachment trên Redmine #41998. -->

## Ghi chú thêm của Leader

⚠️ **Đây KHÔNG phải bug Redmine không tái hiện được** — ticket thuộc loại **proactive audit** (soát luận điểm khi nâng MySQL 5.7 → 8.0), không có "Tái hiện bug" vì Dev tự phát hiện qua đối chiếu kỹ thuật (dashboard `fixbug-lme/mysql80-report`), không cần runtime để kích hoạt. Dev đã tự confirm + tự fix (xem file 03). TCs nên tập trung verify: (a) cách fix (thêm `id` làm khoá phụ cuối ORDER BY) có áp dụng đúng ở từng vị trí, (b) regression — dữ liệu "hoà" nhiều trang không lặp/sót, (c) không phát sinh filesort mới / mất index trên bảng lớn (conversation ~50M dòng, detail_landing_click ~31M dòng).

Môi trường phát hiện: đối chiếu trên máy B MySQL 8.0.46 (dev); bug chỉ lộ trên MySQL 8, KHÔNG tái hiện được trên MySQL 5.7/5.6. Dev **không chạy được EXPLAIN** (dev DB `host.docker.internal:3306` connection refused) — chỉ đánh giá index extension theo DDL, chưa đo thực tế performance/filesort sau fix.

Phạm vi fix rộng hơn 4 item báo cáo ban đầu — Dev tự review v1 bổ sung thêm 2 controller mobile web (`Mobile\ChatMobileController::getFriends`, `Mobile\ListFriendController::index`) + các bản API app song song (chat, lesson, salon) — tổng cộng 10 file đã sửa (xem mục 4.1 file 03).

Ticket gốc tham chiếu: #39528 (báo cáo đối chiếu MySQL 8 R2).

## Journal / note từ Redmine (nguyên văn)

**Journal #140373 — AI LME Fix bug — 2026-10-06:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Các danh sách có phân trang (danh sách chat, lịch sử QR, danh sách đặt chỗ) chỉ sắp theo cột hay trùng giá trị (thời điểm tin nhắn cuối, thời điểm click, thời điểm cập nhật đặt chỗ, ngày + giờ bắt đầu) mà không có khoá phụ duy nhất. MySQL 8 đổi kế hoạch/thuật toán sort nên thứ tự các dòng trùng giá trị không ổn định giữa các trang ⇒ trang sau lặp hoặc bỏ sót bản ghi.

■ 2. CÁCH FIX
Thêm id làm khoá sắp xếp phụ ở cuối ORDER BY (cùng chiều với cột chính) cho 4 vị trí báo cáo: danh sách chat web (get-friends), chat 1:1, lịch sử QR của bạn bè, danh sách đặt chỗ lịch khoá học (tab mới cập nhật + tab hôm nay). Kèm các bản song song cùng màn: API danh sách chat của app, danh sách đặt chỗ lesson của app, danh sách đặt chỗ salon (web + app). Quét ngang: còn các danh sách khác sắp theo cột không duy nhất (danh sách bạn bè sort followed_at/last_time…) ghi yokoten để tách ticket. Tự review v1: bổ sung lối vào mobile web của cùng danh sách chat (Mobile\ChatMobileController::getFriends, Mobile\ListFriendController::index — simplePaginate(30) chỉ sắp theo time_newest_reiceve) thêm ->orderBy(conversation.id, DESC) (commit 56a88641db).

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
ConversationService::getFriend (app/Services/ConversationService.php) — caller: Basic\ChatController::getFriends (GET /chat/get-friends, màn /basic/chat-v3)
ChatController::getFriends (private) — danh sách bạn chat không ES, gọi từ ChatController::index:621/634 (app/Http/Controllers/ChatController.php; route /chat-v2 đã comment ở routes/web.php:1042)
Api\ChatController::getFriends — POST api /chat/get-list-friend (app/Http/Controllers/Api/ChatController.php)
Mobile\ChatMobileController::getFriends + Mobile\ListFriendController::index — danh sách chat mobile web /chat-mobile, /list-friend (bổ sung ở tự review v1)
QrActionHistoryRepository::paginateByFriend ← QrActionHistoryService ← Basic\FriendlistController::ajaxQrHistory
CalendarCourseService::listBookings ← Basic\CalendarManagementController::getListBooking (tab1/tab2)
Api\CalendarLessonController::getListBookingLessonByTab — POST api get-list-booking-lesson-by-tab (new_booking/today_booking)
CalendarSalonLineBookingRepository::getListBooking ← CalendarSalonLineBookingService::getListBooking ← Basic\CalendarSalonController::getListBooking (GET /{calendar_id}/get-list-booking)
Api\CalendarSalonController::getListBookingSalonByTab — POST api get-list-booking-salon-by-tab
Index conversation idx_bot_hide_bookmark_time(bot_id,is_hide,is_bookmark,last_time_message)+PK ngầm, calendar_salon_line_booking idx_cslb_salon_user_update(calendar_salon_id,user_update_time)+PK ngầm (line_db_struct.sql / migration 2026_09_21)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Services/ConversationService.php
   - app/Http/Controllers/ChatController.php
   - app/Http/Controllers/Api/ChatController.php
   - app/Repositories/Eloquents/QrActionHistoryRepository.php
   - app/Services/CalendarManagement/CalendarCourseService.php
   - app/Http/Controllers/Api/CalendarLessonController.php
   - app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php
   - app/Http/Controllers/Api/CalendarSalonController.php
   - app/Http/Controllers/Mobile/ChatMobileController.php
   - app/Http/Controllers/Mobile/ListFriendController.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ đổi thứ tự đọc (SELECT ... ORDER BY), không ghi dữ liệu
 • 4.3 Tính năng liên quan:
   - Chat 1:1 (FA-001) — danh sách hội thoại bên trái màn chat (web /basic/chat-v3 qua GET /chat/get-friends + API app /get-list-friend + mobile web /list-friend, /chat-mobile): các hội thoại trùng thời điểm tin cuối nay xếp ổn định theo id giảm dần, không lặp/sót khi cuộn trang
   - QR Code Action / Landing (FA-017) — lịch sử hành động QR của bạn bè: các click cùng thời điểm xếp theo id giảm dần
   - Lesson / Calendar Booking (FA-019) — danh sách đặt chỗ tab mới cập nhật (id giảm dần) / tab hôm nay (id tăng dần), web + app
   - Salon Booking (FA-020) — danh sách đặt chỗ salon tab mới cập nhật / hôm nay, web + app

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l 8 file đã sửa: No syntax errors; Rà select/DISTINCT/GROUP BY: không có DISTINCT/GROUP BY ⇒ ORDER BY id hợp lệ với ONLY_FULL_GROUP_BY; Rà index: conversation idx_bot_hide_bookmark_time + PK ngầm (index extension) và salon idx_cslb_salon_user_update + PK ngầm ⇒ id cùng chiều DESC/ASC với cột chính vẫn được index phục vụ sort, không phát sinh filesort mới; Không chạy được EXPLAIN: MySQL dev host.docker.internal:3306 Connection refused
   Bằng chứng: Danh sách vị trí lấy đầy đủ từ fixbug-lme/perf-report redmine_tasks.py web R2 (mô tả record bị cắt 4000 ký tự); Không tái hiện runtime: dev DB không kết nối được; lỗi chỉ phát sinh trên MySQL 8 khi có nhiều dòng trùng giá trị sort

■ TỰ REVIEW (AI)
Diff 8 file, mỗi chỗ chỉ thêm 1 orderBy id cùng chiều cột chính làm khoá phụ; không đổi điều kiện lọc/kết quả, chỉ cố định thứ tự các dòng hoà. Đã rà 4 vị trí báo cáo + bản song song (app API, salon).
 • Rủi ro / lưu ý khi test:
   - Thứ tự các dòng hoà có thể khác chút so với trước (5.7 theo plan) — giờ là id giảm dần/tăng dần, chấp nhận được
   - Không chạy được EXPLAIN do dev DB tắt; đánh giá index extension theo DDL

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41998 (nhánh gốc release_step_20260930_v2, commit 56a88641db, 10 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 3 phút 15 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=a766f7ab-16d4-4c09-927e-7caaa3311189
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41998
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
