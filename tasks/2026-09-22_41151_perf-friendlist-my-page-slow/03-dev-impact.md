# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `75010b1721` (2 file, 67 thêm / 40 xoá) — Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41151 |
| Branch | `ai_small_41151` (gốc `release_step_20260827` — `ca8fe3c31f`) |
| Ngày submit đánh giá | 2026-09-21 |
| Auto-filled | `2026-09-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Hàm mở màn chi tiết bạn bè tính sẵn **5 khối dữ liệu mà giao diện KHÔNG dùng**:

1. Trạng thái xác nhận tin nhắn (`$special_status`) — **2 truy vấn con trên bảng tin nhắn khổng lồ**
2. Toàn bộ mẫu tin của bot kèm nội dung (`$templates`)
3. Toàn bộ nhóm thẻ (`$categorytags`)
4. Thẻ của bạn bè
5. Bước kịch bản kế tiếp (`$next_scenario`)

Bản giao diện mới đã chuyển sang nạp các phần này bằng **endpoint AJAX riêng** nên 4 biến đó bị bỏ hẳn.

**Nặng nhất**: trang gọi đồng bộ API LINE để đồng bộ tên/ảnh đại diện mà **KHÔNG đặt giới hạn thời gian** — thư viện LINE (`CurlHTTPClient`) mặc định `$timeout`/`$connectTimeout` = `null`, `toCurlOptions` chỉ set `CURLOPT_TIMEOUT`/`CURLOPT_CONNECTTIMEOUT` khi khác null ⇒ **curl chờ vô hạn**. Khi LINE trả chậm thì cả trang treo — **đây là nguồn của mức 35s**.

> Tiền lệ cùng root cause: `knowledge/lessons.md #38390` (cùng controller) fix LINE API không timeout bằng `connect_timeout=5` / `timeout=10` — bản fix này dùng cùng mức.

## 2. Cách fix

Fix cuối gồm **2 phần**, đúng trong phạm vi endpoint `GET /basic/friendlist/my_page/{id}` và **đúng 2 file**:

1. **Bỏ 5 khối truy vấn** mà cây view 26 file chứng minh là không dùng — trong đó có 2 truy vấn con trên bảng `messages`.
2. **Giới hạn thời gian cho lời gọi LINE** (10s đọc / 5s kết nối, qua **2 tham số tuỳ chọn mặc định `null`** nên 12 caller khác không đổi hành vi) + **bắt lỗi tại chỗ** và **BÁO CHATWORK** (`notifyChatworkException`) kèm `bot_id` / `line_user_id` / nội dung lỗi.

Vòng 2 (theo yêu cầu dev): chỉ thêm ĐÚNG một việc ở chỗ gọi LINE trong màn chi tiết bạn bè — khi `getProfile` lỗi hoặc quá thời gian thì ngoài `logError` còn gọi `notifyChatworkException`, để đã bắt lỗi thì dev biết lỗi gì chứ không lặng lẽ bỏ qua. Dùng đúng convention repo (12+ chỗ khác gọi hàm này từ trong khối catch: `FormAnswerController:6353`, `BackupController:48`, `PointSettingController:1808/2413`, `Admin/BotController:5042/6624`).

**KHÔNG sửa `app/Helpers/functions.php`** — bản hardening `notifyChatworkException` ở lần trước đã bị bỏ hẳn khỏi branch theo chỉ đạo human.

Lý do bắt buộc phải có try/catch tại chỗ: `CurlExecutionException extends \Exception` và `BotController::getInfoFromLine` không bắt lỗi ⇒ nếu chỉ đặt timeout mà KHÔNG catch tại chỗ thì **trang sẽ trắng sau 10s**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FriendlistController::mypage` — `app/Http/Controllers/Basic/FriendlistController.php` | **SỬA** — bỏ 5 khối truy vấn, truyền timeout, bọc try/catch + `notifyChatworkException` | Endpoint bị chậm |
| 2 | `BotController::getInfoFromLine` — `app/Http/Controllers/Admin/BotController.php` | **SỬA** — thêm 2 tham số timeout tuỳ chọn (mặc định `null`) | Nơi gọi LINE API |
| 3 | `notifyChatworkException` — `app/Helpers/functions.php` | **KHÔNG sửa** (chỉ đọc để dùng đúng convention) | Human chỉ đạo không sửa helper |
| 4 | `Conversation::getConversationRaw` + `Conversation::getConversation` — `app/Conversation.php` | Không sửa — chỉ check | Liên quan `$conversation` (view chỉ dùng `blocked_by` dòng 1027) |
| 5 | `LineUser::getLineUserMyPage` — `app/LineUser.php` | Không sửa — chỉ check | Nguồn `$line_info` (view chỉ dùng 4 khoá: `avatar_url` 809, `name_display` 813, `is_blocked` 1027, `view_name` 1041) |
| 6 | `Category::getCategoryWithTemplateByBot` + `Category::categoriesTags` — `app/Category.php` | Không sửa — bỏ lời gọi ở `mypage` | Sinh `$categorytags` mà view không dùng |
| 7 | `Template::getTemplateByBot` — `app/Template.php` | Không sửa — bỏ lời gọi ở `mypage` | Sinh `$templates` mà view không dùng |
| 8 | `FriendlistController::getTags` — `app/Http/Controllers/Basic/FriendlistController.php` | Không sửa | Endpoint AJAX riêng đã thay việc nạp sẵn thẻ |
| 9 | `CurlHTTPClient::toCurlOptions` / `setTimeout` / `setConnectTimeout` — `vendor/linecorp/line-bot-sdk` | Không sửa — chỉ đọc | Xác nhận mặc định `null` ⇒ curl chờ vô hạn |
| 10 | view `basic.friend_detail.index` + 25 file trong cây `@extends`/`@include` | Không sửa — quét 26 file | KHÔNG file nào tham chiếu `$special_status`, `$categorytags`, `$next_scenario`, `$templates`; không có `$$var` / `${...}` / `compact` / `get_defined_vars` / `View::composer` ⇒ HTML không đổi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FriendlistController::mypage` — `GET /basic/friendlist/my_page/{id}` | `app/Http/Controllers/Basic/FriendlistController.php` | Direct | Bỏ 5 khối truy vấn; truyền timeout; bọc try/catch + notify Chatwork. HTML trả về **không đổi** |
| F2 | `BotController::getInfoFromLine` | `app/Http/Controllers/Admin/BotController.php` | Direct | Thêm 2 tham số timeout tuỳ chọn, mặc định `null` ⇒ **12 caller khác giữ nguyên hành vi** |
| F3 | `notifyChatworkException` | `app/Helpers/functions.php` | Indirect (không sửa) | Được gọi thêm từ 1 điểm mới. **KHÔNG có timeout, KHÔNG tự bọc try/catch** — rủi ro đã biết |
| F4 | `Conversation::getConversationRaw` / `getConversation` | `app/Conversation.php` | Indirect | Lời gọi tính `$special_status` bị bỏ khỏi `mypage` |
| F5 | `Category::getCategoryWithTemplateByBot` / `categoriesTags` | `app/Category.php` | Indirect | Lời gọi bị bỏ khỏi `mypage` |
| F6 | `Template::getTemplateByBot` | `app/Template.php` | Indirect | Lời gọi bị bỏ khỏi `mypage` |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `line_user.name` / `line_user.avatar_url` / `line_user.status_message` | UPDATE | Vẫn ghi đúng như cũ khi LINE trả thông tin kịp; **nếu LINE vượt 10s hoặc lỗi thì KHÔNG ghi và giữ giá trị đã lưu**, giống nhánh LINE không trả được dữ liệu trước đây |
| D2 | `sync_elasticsearch` | Không đổi | Điều kiện ghi giữ nguyên |
| D3 | Schema DB | Không đổi | Không thêm/sửa/xoá bảng, **không thêm index, không migration, không cần recover data** |
| D4 | **Dữ liệu ra NGOÀI hệ thống** — Chatwork room `291087346` | CREATE | Thêm tin nhắn khi lời gọi LINE ở màn chi tiết bạn bè lỗi/timeout — nội dung chỉ có `bot_id`, `line_user_id` và thông điệp lỗi, **không có token hay thông tin cá nhân của khách** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend List (FA-013)** — màn chi tiết bạn bè (`my_page`) | F1, F4, F5, F6, D4 | **High** — bỏ 5 khối truy vấn vô ích, giới hạn thời gian gọi LINE và báo Chatwork khi lời gọi đó lỗi; nội dung HTML trả về không đổi |
| T2 | **Friend Information (FA-015)** | F1, D1 | **Medium** — tên/ảnh đại diện bạn bè vẫn đồng bộ từ LINE khi LINE trả kịp; quá ngưỡng 10s thì giữ giá trị đã lưu trong DB |
| T3 | **Chat 1:1 (FA-001)** | F2 | **Medium** — dùng chung `BotController::getInfoFromLine`; 2 tham số timeout mới mặc định `null` nên luồng chat và các job/command gọi hàm này giữ nguyên hành vi |
| T4 | **Message Template (FA-010)** | F6 | **Low** — chỉ bỏ việc nạp sẵn danh sách mẫu tin ở màn chi tiết bạn bè (view không dùng, đã có endpoint AJAX riêng); chức năng quản lý mẫu tin không bị đụng |
| T5 | **Tag Management (FA-012)** | F5 | **Low** — chỉ bỏ việc nạp sẵn nhóm thẻ/thẻ ở màn chi tiết bạn bè; chức năng quản lý thẻ không bị đụng |

---

## 5. Recover data

✔ Không cần recover data.

## 6. Verify của Dev

- **Mức: lint** — `php -l` trên 2 file: No syntax errors detected.
- `git diff --stat release...ai_small_41151`: đúng 2 file (BotController, FriendlistController), 67 thêm / 40 xoá — `app/Helpers/functions.php` **KHÔNG còn trong diff**.
- Base branch: `release_step_20260827` (`ca8fe3c31f`) chứa trọn `release_step_20260805`.
- Không sửa `.java` ⇒ không chạy `gradle compileJava`. Fix ở Controller ⇒ không thêm unit test theo B4c.
- ⚠️ **KHÔNG chạy được EXPLAIN / verify runtime** — MySQL dev `host.docker.internal:3306` trả `Connection refused`.

## 7. Rủi ro / lưu ý khi test (Dev tự nêu)

1. ⚠️ **`notifyChatworkException` không có timeout, không tự bọc try/catch** (human chỉ đạo KHÔNG sửa helper): nếu `backendapi.watermeru.com` chậm/lỗi ĐÚNG lúc LINE cũng lỗi thì (a) request bị giữ thêm, (b) exception bay ra giữa khối catch → rơi vào catch tổng của `mypage` (chỉ `Log::error`, không return) = **trang trắng**. Xác suất thấp (phải trùng 2 sự cố). Muốn triệt thì làm ticket riêng hardening 3 helper `notifyChatwork` / `notifyChatworkChat11` / `notifyChatworkException`.
2. ⚠️ Nếu LINE gặp sự cố kéo dài, **mỗi lần mở màn chi tiết bạn bè sẽ đẩy 1 tin vào Chatwork** ⇒ có thể ồn. Repo không có pattern throttle nào cho notify Chatwork.
3. ⚠️ **Ngưỡng 10s đọc**: bot mà LINE trả lời chậm hơn 10s sẽ **không đồng bộ tên/ảnh** trong lần mở màn đó (lần sau vẫn thử lại) — đổi lại trang không treo.
4. ⚠️ Chưa đo được bằng EXPLAIN/runtime ⇒ **nên xác nhận lại p95 của endpoint trên staging** sau khi push.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
