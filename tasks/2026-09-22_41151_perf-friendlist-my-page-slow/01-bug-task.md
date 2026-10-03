# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41151 — [AI][Performance] GET /basic/friendlist/my_page/{id} chậm max 35s (2 lần/24h)` |
| Module / Màn hình | Friend List (FA-013) — màn chi tiết bạn bè `GET /basic/friendlist/my_page/{id}` |

## Mô tả bug (bản dịch tiếng Việt)

*Ticket tự tạo bởi check-performance AI* (từ report request chậm bắn lên Chatwork room 417532006).

### Endpoint

```
GET /basic/friendlist/my_page/{id}
```

**Mức:** high — xếp theo độ chậm: max 35s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 58
**Số lần chậm 24h:** 2 (kỳ trước 0, 1h qua 2) — xu hướng new
**Thời gian:** max 35s · p95 35s · trung bình 26s · median 35s
**Phân bố:** ≥15s SUPPERSLOW 3 · 10–15s VERYSLOW 2 · 5–10s SLOWLV1 0
**User bị ảnh hưởng:** 1 (tổng 4)
**Server:** step.lme.jp — **BotId:** 107152, 30529, 52318
**Lần đầu:** 2026-09-16 00:00 UTC — **Lần cuối:** 2026-09-21 03:19 UTC
**Lịch sử dài hạn:** tổng 5 lần chậm trong 2 ngày, đỉnh 3 lần/24h, chậm nhất 35s, từ 2026-09-16 00:00 UTC

### Vì sao ưu tiên này

- Độ chậm: p95 35s — cực chậm (+38 điểm)
- Tần suất: 2 lần/24h (+2 điểm)
- User ảnh hưởng: 1 user bị chậm (+3 điểm)
- Độ mới: Vừa xảy ra trong 1h qua (+12 điểm)
- Xu hướng: Mới xuất hiện (kỳ trước 0 lần, nay 2) (+3 điểm)

### URL mẫu

- `/basic/friendlist/my_page/60969266`
- `/basic/friendlist/my_page/40672785`
- `/basic/friendlist/my_page/61348430`
- `/basic/friendlist/my_page/23483796`

### Các lần CHẬM NHẤT đã ghi nhận

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 35 | 2026-09-21 10:19 VN | SUPPERSLOW | 171644 | /basic/friendlist/my_page/23483796 |
| 19 | 2026-09-16 07:18 VN | SUPPERSLOW | 107883 | /basic/friendlist/my_page/40672785 |
| 17 | 2026-09-21 10:19 VN | SUPPERSLOW | 171644 | /basic/friendlist/my_page/23483796 |
| 11 | 2026-09-16 07:00 VN | VERYSLOW | 135214 | /basic/friendlist/my_page/60969266 |
| 10 | 2026-09-16 07:18 VN | VERYSLOW | 128846 | /basic/friendlist/my_page/61348430 |

### Nguồn cảnh báo trong source

Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

<!-- Ticket KHÔNG có Section "Tái hiện bug" — sinh tự động từ log performance, không có kịch bản thao tác. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #41151 không có attachment. -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine (không có Section "Tái hiện bug") — ticket do AI check-performance sinh từ log request chậm. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

- **Môi trường phát hiện: Production** — server `step.lme.jp`.
- **Tần suất KHÔNG 100%** — chỉ 2 lần/24h, phụ thuộc thời gian LINE API trả về. Muốn tái hiện phải giả lập LINE API chậm/lỗi (chặn `api.line.me`, hoặc dùng bot có access token sai/hết hạn).
- Fix gồm 2 phần: (a) bỏ 5 khối truy vấn mà view không dùng; (b) đặt timeout gọi LINE (connect 5s / read 10s) + catch tại chỗ + `notifyChatworkException` (Chatwork room 291087346) kèm `bot_id` + `line_user_id` + nội dung lỗi.
- ⚠️ **Rủi ro Dev đã nêu, human quyết giữ nguyên**: `notifyChatworkException` KHÔNG có timeout và KHÔNG tự bọc try/catch → nếu `backendapi.watermeru.com` chậm/lỗi đúng lúc LINE cũng lỗi thì request bị giữ thêm và exception có thể làm **trắng trang**.
- ⚠️ Nếu LINE lỗi kéo dài, **mỗi lần mở màn chi tiết bạn bè đẩy 1 tin vào Chatwork** — không có throttle.
- ⚠️ Dev **chưa đo được bằng EXPLAIN / runtime** (MySQL dev `Connection refused`) → cần xác nhận lại p95 endpoint trên staging sau khi deploy.
- Branch QA checkout: `ai_small_41151` (gốc `release_step_20260827`, commit `75010b1721`, đúng 2 file).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `107152`, `30529`, `52318` |
| Friend | id trong URL: `23483796` (ca 35s), `40672785`, `60969266`, `61348430` |
| Đối tượng cấu hình | Màn chi tiết bạn bè `GET /basic/friendlist/my_page/{id}` |
| Thời điểm lỗi | 2026-09-21 10:19 VN (35s) · 2026-09-16 07:18 VN (19s) |
| Đối chứng | Cùng endpoint, friend khác cùng bot, chạy dưới 5s |

## Journal / note từ Redmine (nguyên văn)

**Journal #137407 — AI LME Fix bug — 2026-09-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Hàm mở màn chi tiết bạn bè tính sẵn 5 khối dữ liệu mà giao diện KHÔNG dùng: trạng thái xác nhận tin nhắn (2 truy vấn con trên bảng tin nhắn khổng lồ), toàn bộ mẫu tin của bot kèm nội dung, toàn bộ nhóm thẻ + thẻ của bạn bè, và bước kịch bản kế tiếp — bản giao diện mới đã chuyển sang nạp các phần này bằng endpoint AJAX riêng nên 4 biến đó bị bỏ hẳn. Nặng nhất là trang gọi đồng bộ API LINE để đồng bộ tên/ảnh đại diện mà KHÔNG đặt giới hạn thời gian (thư viện LINE mặc định để curl chờ vô hạn), nên khi LINE trả chậm thì cả trang treo — đây là nguồn của mức 35s.

■ 2. CÁCH FIX
Vòng 2 (theo yêu cầu dev): chỉ thêm ĐÚNG một việc ở chỗ gọi LINE trong màn chi tiết bạn bè — khi getProfile lỗi hoặc quá thời gian thì ngoài logError còn gọi notifyChatworkException kèm bot_id, line_user_id và nội dung lỗi, để đã bắt lỗi thì dev biết lỗi gì chứ không lặng lẽ bỏ qua. Dùng đúng convention của repo (12+ chỗ khác đang gọi hàm này từ trong khối catch). KHÔNG sửa app/Helpers/functions.php — bản hardening notifyChatworkException ở lần trước đã được bỏ hẳn khỏi branch theo chỉ đạo, branch trở lại đúng 2 file của endpoint này.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
FriendlistController::mypage (app/Http/Controllers/Basic/FriendlistController.php)
BotController::getInfoFromLine (app/Http/Controllers/Admin/BotController.php)
notifyChatworkException — chỉ ĐỌC để dùng đúng convention, KHÔNG sửa (app/Helpers/functions.php)
Conversation::getConversationRaw + Conversation::getConversation (app/Conversation.php)
LineUser::getLineUserMyPage (app/LineUser.php)
Category::getCategoryWithTemplateByBot + Category::categoriesTags (app/Category.php)
Template::getTemplateByBot (app/Template.php)
FriendlistController::getTags (app/Http/Controllers/Basic/FriendlistController.php)
CurlHTTPClient::toCurlOptions / setTimeout / setConnectTimeout (vendor/linecorp/line-bot-sdk)
view basic.friend_detail.index + 25 file trong cây @extends/@include (resources/views/basic/friend_detail/, resources/views/layout/v2/basic/)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/FriendlistController.php
   - app/Http/Controllers/Admin/BotController.php
 • 4.2 Data ảnh hưởng:
   - line_user.name / line_user.avatar_url / line_user.status_message — vẫn ghi đúng như cũ khi LINE trả thông tin kịp; nếu LINE vượt 10s hoặc lỗi thì KHÔNG ghi và giữ giá trị đã lưu, giống nhánh LINE không trả được dữ liệu trước đây
   - sync_elasticsearch — không đổi (điều kiện ghi giữ nguyên)
   - Không thêm/sửa/xoá bảng, không thêm index, không migration, không cần recover data
   - Dữ liệu ra NGOÀI hệ thống: thêm tin nhắn Chatwork (room 291087346 của notifyChatworkException) khi lời gọi LINE ở màn chi tiết bạn bè lỗi/timeout — nội dung chỉ có bot_id, line_user_id và thông điệp lỗi, không có token hay thông tin cá nhân của khách
 • 4.3 Tính năng liên quan:
   - Friend List (FA-013) — màn chi tiết bạn bè (my_page): bỏ 5 khối truy vấn vô ích, giới hạn thời gian gọi LINE và báo Chatwork khi lời gọi đó lỗi; nội dung HTML trả về không đổi
   - Friend Information (FA-015) — tên/ảnh đại diện bạn bè vẫn đồng bộ từ LINE khi LINE trả kịp; quá ngưỡng thì giữ giá trị đã lưu trong DB
   - Chat 1:1 (FA-001) — dùng chung BotController::getInfoFromLine; 2 tham số timeout mới mặc định null nên luồng chat và các job/command gọi hàm này giữ nguyên hành vi
   - Message Template (FA-010) và Tag Management (FA-012) — chỉ bỏ việc nạp sẵn danh sách mẫu tin/thẻ ở màn chi tiết bạn bè (view không dùng, đã có endpoint AJAX riêng); chức năng quản lý mẫu tin/thẻ không bị đụng

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Basic/FriendlistController.php: No syntax errors detected; php -l app/Http/Controllers/Admin/BotController.php: No syntax errors detected; git diff --stat release...ai_small_41151: đúng 2 file (BotController, FriendlistController), 67 thêm / 40 xoá — app/Helpers/functions.php KHÔNG còn trong diff; Branch chưa từng push (pushed:false) nên đã dựng lại sạch thay vì chồng thêm commit revert: worktree tách từ commit 1 (9399ed584e) → chỉ commit phần notify → dời branch bằng CAS git update-ref refs/heads/ai_small_41151 75010b1721 e8504e370b. Lịch sử branch còn đúng 2 commit, không có commit revert rác; Base branch: prompt/config ghi release_step_20260805 nhưng origin có release_step_20260827 CHỨA TRỌN nó (merge-base --is-ancestor = YES) ⇒ branch fix tách từ release_step_20260827 (ca8fe3c31f); Không sửa .java nên không chạy gradle compileJava; fix ở Controller nên không thêm unit test theo B4c
   Bằng chứng: Convention gọi đã đối chiếu: notifyChatworkException('<ngữ cảnh>: '.$e->getMessage()) đang dùng ở 12+ chỗ, trong đó nhiều chỗ gọi TỪ TRONG khối catch của controller (FormAnswerController:6353, BackupController:48, PointSettingController:1808/2413, Admin/BotController:5042/6624) ⇒ cách gọi mới bám đúng convention repo, không đặc cách; RỦI RO ĐÃ BIẾT, human quyết giữ nguyên: notifyChatworkException gọi Guzzle KHÔNG có connect_timeout/timeout và bản thân hàm KHÔNG bọc try/catch. Vì nó được gọi TỪ TRONG khối catch, nếu backendapi.watermeru.com chậm/lỗi thì (a) request bị giữ thêm theo thời gian chờ của lời gọi này, (b) exception bay ra giữa khối catch → rơi vào catch tổng của mypage (chỉ Log::error, không return) = trang trắng. Đã báo trước; human chỉ đạo KHÔNG sửa helper nên giữ nguyên trạng và chấp nhận rủi ro này (đúng mức rủi ro mà 12+ điểm gọi hiện có trong repo đang chịu); Quét toàn bộ 26 file trong cây @extends/@include của view basic.friend_detail.index: KHÔNG file nào tham chiếu $special_status, $categorytags, $next_scenario, $templates; không có truy cập biến động ($$var, ${...}, compact, get_defined_vars) và không có View::composer nhắm view này ⇒ 5 khối truy vấn bỏ đi là công vô ích, HTML không đổi; $line_info trong view chỉ dùng 4 khoá (avatar_url 809, name_display 813, is_blocked 1027, view_name 1041), $conversation chỉ dùng blocked_by (1027) — 2 biến này GIỮ nguyên; vendor/linecorp/line-bot-sdk CurlHTTPClient: $timeout/$connectTimeout mặc định null, toCurlOptions chỉ set CURLOPT_TIMEOUT/CURLOPT_CONNECTTIMEOUT khi khác null ⇒ mặc định curl chờ vô hạn, khớp triệu chứng 35s; CurlExecutionException extends \Exception và BotController::getInfoFromLine không bắt lỗi ⇒ nếu chỉ đặt timeout mà KHÔNG catch tại chỗ thì trang sẽ trắng sau 10s — lý do try/catch là bắt buộc ở đây; Tiền lệ cùng root cause: knowledge/lessons.md #38390 (cùng controller) fix LINE API không timeout bằng connect_timeout=5 / timeout=10 — bản fix này dùng cùng mức; KHÔNG chạy được EXPLAIN / verify runtime: MySQL dev host.docker.internal:3306 trả Connection refused (stack dev trên host đang tắt)

■ TỰ REVIEW (AI)
Fix cuối gồm 2 phần, đúng trong phạm vi endpoint GET /basic/friendlist/my_page/{id} và đúng 2 file: (1) bỏ 5 khối truy vấn mà cây view 26 file chứng minh là không dùng — trong đó có 2 truy vấn con trên bảng messages; (2) giới hạn thời gian cho lời gọi LINE (10s đọc / 5s kết nối, qua 2 tham số tuỳ chọn mặc định null nên 12 caller khác không đổi hành vi) + bắt lỗi tại chỗ và BÁO CHATWORK kèm bot_id/line_user_id/nội dung lỗi. Đường đi thành công giữ y nguyên input/output/phân quyền; đường đi chậm/lỗi trước đây là treo 35s hoặc trắng trang, sau fix dừng ở ~10s, render bằng dữ liệu đã lưu và dev nhận cảnh báo.
 • Rủi ro / lưu ý khi test:
   - notifyChatworkException không có timeout và không tự bọc try/catch (human chỉ đạo KHÔNG sửa helper): nếu backendapi.watermeru.com chậm/lỗi ĐÚNG lúc LINE cũng lỗi thì request bị giữ thêm và exception có thể làm trang trắng. Xác suất thấp (phải trùng 2 sự cố) và bằng đúng mức rủi ro 12+ điểm gọi khác trong repo đang chịu; muốn triệt thì làm 1 ticket riêng hardening 3 helper notifyChatwork/notifyChatworkChat11/notifyChatworkException
   - Nếu LINE gặp sự cố kéo dài, mỗi lần mở màn chi tiết bạn bè sẽ đẩy 1 tin vào Chatwork ⇒ có thể ồn. Repo không có pattern throttle nào cho notify Chatwork nên bám convention sẵn có
   - Ngưỡng 10s đọc: bot mà LINE trả lời chậm hơn 10s sẽ không đồng bộ tên/ảnh trong lần mở màn đó (lần sau vẫn thử lại) — đổi lại trang không treo
   - Chưa đo được bằng EXPLAIN/runtime vì MySQL dev không kết nối được ⇒ nên xác nhận lại p95 của endpoint trên staging sau khi push

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41151 (nhánh gốc release_step_20260827, commit 75010b1721, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 10 phút 57 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=46a7e5c2-a307-48ef-92c1-0f258bfaa5a3
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41151
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
