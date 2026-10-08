# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug pipeline) |
| Commit / Pull Request | commit `56a88641db` (10 file, đã push lên origin, chưa merge) |
| Branch | `ai_small_41998` (nhánh gốc `release_step_20260930_v2`) |
| Ngày submit đánh giá | 2026-10-06 |
| Auto-filled | 2026-10-06 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Các danh sách có phân trang (danh sách chat, lịch sử QR, danh sách đặt chỗ) chỉ sắp theo cột hay trùng giá trị (thời điểm tin nhắn cuối, thời điểm click, thời điểm cập nhật đặt chỗ, ngày + giờ bắt đầu) mà không có khoá phụ duy nhất. MySQL 8 đổi kế hoạch/thuật toán sort nên thứ tự các dòng trùng giá trị không ổn định giữa các trang ⇒ trang sau lặp hoặc bỏ sót bản ghi.

## 2. Cách fix

Thêm `id` làm khoá sắp xếp phụ ở cuối ORDER BY (cùng chiều với cột chính) cho 4 vị trí báo cáo: danh sách chat web (get-friends), chat 1:1, lịch sử QR của bạn bè, danh sách đặt chỗ lịch khoá học (tab mới cập nhật + tab hôm nay). Kèm các bản song song cùng màn: API danh sách chat của app, danh sách đặt chỗ lesson của app, danh sách đặt chỗ salon (web + app). Quét ngang: còn các danh sách khác sắp theo cột không duy nhất (danh sách bạn bè sort followed_at/last_time…) — Dev ghi yokoten để tách ticket riêng (**không nằm trong phạm vi fix #41998**).

Tự review v1 (Dev tự bổ sung): thêm lối vào mobile web của cùng danh sách chat (`Mobile\ChatMobileController::getFriends`, `Mobile\ListFriendController::index` — `simplePaginate(30)` trước đó chỉ sắp theo `time_newest_reiceve`) → thêm `->orderBy(conversation.id, DESC)` (commit 56a88641db).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ConversationService::getFriend` (app/Services/ConversationService.php) | Thêm `orderBy(conversation.id, DESC)` | Caller: `Basic\ChatController::getFriends` (GET /chat/get-friends, màn /basic/chat-v3) |
| 2 | `ChatController::getFriends` (private, app/Http/Controllers/ChatController.php) | Thêm id DESC | Danh sách bạn chat không ES, gọi từ `ChatController::index` dòng 621/634; route `/chat-v2` đã comment ở routes/web.php:1042 (code chết, vẫn sửa cho an toàn) |
| 3 | `Api\ChatController::getFriends` (app/Http/Controllers/Api/ChatController.php) | Thêm id DESC | POST api `/chat/get-list-friend` |
| 4 | `Mobile\ChatMobileController::getFriends` + `Mobile\ListFriendController::index` | Thêm `orderBy(conversation.id, DESC)` (tự review v1, commit 56a88641db) | Danh sách chat mobile web `/chat-mobile`, `/list-friend` |
| 5 | `QrActionHistoryRepository::paginateByFriend` | Thêm id DESC | ← `QrActionHistoryService` ← `Basic\FriendlistController::ajaxQrHistory` |
| 6 | `CalendarCourseService::listBookings` (tab1/tab2) | Thêm id ASC/DESC theo tab | ← `Basic\CalendarManagementController::getListBooking` |
| 7 | `Api\CalendarLessonController::getListBookingLessonByTab` | Thêm id ASC/DESC theo tab | POST api `get-list-booking-lesson-by-tab` (new_booking/today_booking) |
| 8 | `CalendarSalonLineBookingRepository::getListBooking` | Thêm id ASC/DESC theo tab | ← `CalendarSalonLineBookingService::getListBooking` ← `Basic\CalendarSalonController::getListBooking` (GET /{calendar_id}/get-list-booking) |
| 9 | `Api\CalendarSalonController::getListBookingSalonByTab` | Thêm id ASC/DESC theo tab | POST api `get-list-booking-salon-by-tab` |
| 10 | Index liên quan | Không đổi — Dev đối chiếu DDL sẵn có | `conversation.idx_bot_hide_bookmark_time(bot_id,is_hide,is_bookmark,last_time_message)` + PK ngầm, `calendar_salon_line_booking.idx_cslb_salon_user_update(calendar_salon_id,user_update_time)` + PK ngầm (line_db_struct.sql / migration 2026_09_21) — id cùng chiều với cột chính vẫn tận dụng được index extension |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ConversationService::getFriend` | app/Services/ConversationService.php | Direct | ★ Ưu tiên Cao gốc — danh sách chat web get-friends |
| F2 | `ChatController::getFriends` (private) | app/Http/Controllers/ChatController.php | Direct | Route `/chat-v2` đã comment — code gần như chết |
| F3 | `Api\ChatController::getFriends` | app/Http/Controllers/Api/ChatController.php | Direct | API app POST /chat/get-list-friend |
| F4 | `QrActionHistoryRepository::paginateByFriend` | app/Repositories/Eloquents/QrActionHistoryRepository.php | Direct | Ưu tiên gốc Trung bình |
| F5 | `CalendarCourseService::listBookings` | app/Services/CalendarManagement/CalendarCourseService.php | Direct | Ưu tiên gốc Thấp (tab1), tab2 thêm ở bản fix |
| F6 | `Api\CalendarLessonController::getListBookingLessonByTab` | app/Http/Controllers/Api/CalendarLessonController.php | Direct | Bản song song API app — không có trong 4 item báo cáo gốc |
| F7 | `CalendarSalonLineBookingRepository::getListBooking` | app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php | Direct | Bản song song salon — không có trong 4 item báo cáo gốc |
| F8 | `Api\CalendarSalonController::getListBookingSalonByTab` | app/Http/Controllers/Api/CalendarSalonController.php | Direct | Bản song song API app salon |
| F9 | `Mobile\ChatMobileController::getFriends` | app/Http/Controllers/Mobile/ChatMobileController.php | Direct | Bổ sung ở tự review v1 (commit 56a88641db) |
| F10 | `Mobile\ListFriendController::index` | app/Http/Controllers/Mobile/ListFriendController.php | Direct | Bổ sung ở tự review v1 (commit 56a88641db) |

### 4.2. List data bị update khi fix bug

**Không có** — Dev xác nhận chỉ đổi thứ tự đọc (`SELECT ... ORDER BY`), không ghi dữ liệu, không migration, không cache.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 (FA-001) — danh sách hội thoại bên trái màn chat (web /basic/chat-v3 qua GET /chat/get-friends + API app /get-list-friend + mobile web /list-friend, /chat-mobile) | F1, F2, F3, F9, F10 | High — màn dùng liên tục nhất, bảng conversation ~50M dòng |
| T2 | QR Code Action / Landing (FA-017) — lịch sử hành động QR của bạn bè | F4 | Medium |
| T3 | Lesson / Calendar Booking (FA-019) — danh sách đặt chỗ tab mới cập nhật (id giảm dần) / tab hôm nay (id tăng dần), web + app | F5, F6 | Low–Medium |
| T4 | Salon Booking (FA-020) — danh sách đặt chỗ salon tab mới cập nhật / hôm nay, web + app | F7, F8 | Low–Medium |

---

## Đối chiếu diff thật — MCP LME TEST STUDIO (`task_get_context`, task_id=368)

> Theo CLAUDE.md BƯỚC 2(b): dùng trực tiếp `dev_impact` + `spec_delta` của Studio thay vì tự đọc PR / tự suy từ snippet. `diffAvailable=true`.

- **diffStat** (10 file, +36/-8 dòng — mỗi chỗ chỉ thêm 1 `orderBy(id, ...)`):
  `app/Http/Controllers/Api/CalendarLessonController.php` (+8/-2) · `app/Http/Controllers/Api/CalendarSalonController.php` (+8/-2) · `app/Http/Controllers/Api/ChatController.php` (+2) · `app/Http/Controllers/ChatController.php` (+2) · `app/Http/Controllers/Mobile/ChatMobileController.php` (+2) · `app/Http/Controllers/Mobile/ListFriendController.php` (+2) · `app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php` (+8/-2) · `app/Repositories/Eloquents/QrActionHistoryRepository.php` (+2) · `app/Services/CalendarManagement/CalendarCourseService.php` (+8/-2) · `app/Services/ConversationService.php` (+2)
- **dev_impact (Studio, rủi ro hồi quy)**: nhánh tìm kiếm theo tên dùng bảng `conversation_replicate` cùng ORDER BY mới — cần check cả có/không `searchKey` và các `filterTypeFriend` (hide/unconfirm/confirm/schedule/groupChat, tag and/or, status); API app `get-list-friend` cần đồng nhất thứ tự với web; mobile web `/list-friend`, `/chat-mobile` sort `time_newest_reiceve` (CASE, không index) + id DESC — khi có `line_id` phần còn lại xếp theo id (**chưa PO xác nhận chiều sort** — xem TC Studio NEW-16); rủi ro hồi quy chính là **thứ tự hiển thị dòng hoà khác trước** + **hiệu năng sort trên bảng lớn** (conversation ~50M dòng, detail_landing_click ~31M dòng) — Dev chưa chạy EXPLAIN.
- **requirements Studio (10, REQ-001 → REQ-010)**: cover đủ 4 vùng — web list (REQ-001, REQ-002), API app (REQ-003, REQ-007, REQ-009), mobile web (REQ-004), QR history (REQ-005), lesson/salon booking web (REQ-006, REQ-008), performance/index (REQ-010 — risk Medium, "không phát sinh filesort mới" mới là **giả thuyết** Dev tự suy từ DDL, chưa đo thực tế).

⚠️ **Gap giữa Journal Redmine và diff Studio**: Journal mục 4.1 chỉ liệt kê đúng 10 file khớp diffStat — không có mismatch. Riêng `ChatController::getFriends` cũ (F2) Dev tự ghi "route đã comment, không còn route vào" → cân nhắc hạ ưu tiên TC cho nhánh này khi viết TC (code gần như chết nhưng vẫn đã sửa).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
