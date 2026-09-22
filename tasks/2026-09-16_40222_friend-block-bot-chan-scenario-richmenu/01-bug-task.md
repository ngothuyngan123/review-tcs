# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40222 — Với case friend block bot, khi add send scenario và rich menu, không cho phép add và hiển thị báo lỗi` |
| Module / Màn hình | `Chat 1:1 「チャット」 — tab 基本情報 (thông tin cơ bản) — mục ステップ配信 (step delivery) + リッチメニュー (rich menu)` |

## Mô tả bug (bản dịch tiếng Việt)

Với trường hợp friend đã **block bot** (chặn bot), màn Chat 1:1 tab 基本情報 vẫn cho phép quản trị viên **start scenario** (bắt đầu ステップ配信) và **add rich menu** (gán リッチメニュー) cho friend đó.

Sau khi thao tác, màn hình vẫn hiển thị scenario / rich menu vừa gán như thể thao tác thành công — trong khi thực tế friend đã chặn bot nên không còn nhận được gì.

Yêu cầu: **không cho phép add** và **hiển thị báo lỗi** với 2 message tiếng Nhật:
- Khi add scenario: `ブロックされましたため、ステップを開始できません。` (Vì đã bị chặn nên không thể bắt đầu step)
- Khi add rich menu: `ブロックされましたため、リッチメニューを表示できません。` (Vì đã bị chặn nên không thể hiển thị rich menu)

## Steps to reproduce

**ĐKTĐ:** Friend A block bot B

1. Mở màn chat 1:1
2. Tại tab 基本情報, start scenario bất kỳ
3. Tại tab 基本情報, add richmenu bất kỳ

## Expected result

- Không cho phép add và hiển thị báo lỗi.
- Message khi add scenario: `ブロックされましたため、ステップを開始できません。`
- Message khi add richmenu: `ブロックされましたため、リッチメニューを表示できません。`

## Actual result

- Sau bước 2: Vẫn đang hiển thị scenario ở tab 基本情報 (thao tác được chấp nhận, không báo lỗi).
- Sau bước 3: Vẫn đang hiển thị richmenu ở tab 基本情報 (thao tác được chấp nhận, không báo lỗi).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40222 không có attachment nào. -->

## Ghi chú thêm của Leader

- **Điều kiện tiên quyết bắt buộc**: friend phải ở trạng thái **friend chủ động block bot**. Theo journal Dev, trạng thái này ứng với `conversation.is_blocked = 1` **và** `blocked_by = 0`. Môi trường test thường không bấm block được từ phía LINE thật → phải dựng dữ liệu hội thoại trực tiếp (xem note các TC ở file 04).
- ⚠️ **Phân biệt 2 loại block**: friend block bot (`blocked_by = 0`) **vs** admin block friend (`blocked_by = 1`). Fix **chỉ** chặn loại thứ nhất, loại thứ hai giữ nguyên hành vi cũ. Dev đã nêu là điểm cần BA/Leader chốt (message tiếng Nhật đang ở thể bị động 「ブロックされました」).
- **Chỉ chặn 2 thao tác** ticket nêu: bắt đầu/đổi step (`action=change`) và hiển thị/gán rich menu (`rich_menu_id != 0`). Thao tác **dừng step** (`action=cancel`) và **ẩn rich menu** (`rich_menu_id=0`) **vẫn phải chạy được** để admin còn dọn dữ liệu cho friend đã chặn.
- **Tracker là "Improve nội bộ"** (không phải bug khách hàng báo) — issue do QA nội bộ phát hiện, đã Fix done - Đợi test.
- **Dev KHÔNG tái hiện được trên môi trường dev** (MySQL trong container từ chối kết nối) → toàn bộ verify phụ thuộc tester. Lint/syntax check là mức verify duy nhất Dev chạy được.
- **Yokoten Dev tự loại khỏi phạm vi**: các luồng gán scenario / rich menu **tự động** (callback LINE, action sau quét QR, action theo tag) **không** được thêm chốt chặn. Nếu Leader muốn cover thì phải mở ticket riêng.
- Fix chạm thêm **2 màn dùng chung API**: My Page (FA-036) và màn chi tiết bạn bè 「友だち詳細」 — cần regression.

## Journal / note từ Redmine (nguyên văn)

**Journal #133130 — AI LME Fix bug — 2026-08-26:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Màn chat 1:1 tab thông tin cơ bản cho phép bắt đầu kịch bản bước và gán menu hình ảnh cho cả bạn bè đã chặn bot. Hai API xử lý (đổi kịch bản, đổi menu hình ảnh) không kiểm tra trạng thái chặn nên vẫn ghi dữ liệu và hiển thị kết quả như bình thường, dù bạn bè không còn nhận được gì. Phía giao diện, luồng lưu kịch bản cũng không hiển thị thông báo khi máy chủ trả lỗi.

■ 2. CÁCH FIX
Thêm kiểm tra chặn ở phía máy chủ trong bộ điều khiển chat: hàm mới isBlockedByFriend đọc bảng hội thoại (đã chặn = 1 và người chặn = 0 tức bạn bè chủ động chặn bot). API đổi kịch bản từ chối thao tác bắt đầu/đổi bước và API đổi menu hình ảnh từ chối thao tác gán menu, trả về cờ thất bại kèm đúng hai câu thông báo tiếng Nhật theo yêu cầu ticket; thao tác dừng kịch bản và ẩn menu vẫn cho phép. Phía giao diện, luồng lưu kịch bản ở màn chat 1:1 (và hai màn dùng chung API là trang cá nhân, chi tiết bạn bè) nay hiển thị thông báo lỗi máy chủ trả về thay vì im lặng bỏ qua. Yokoten: các luồng gán kịch bản/menu tự động (callback LINE, hành động sau quét mã, hành động theo thẻ) không nằm trong phạm vi ticket nên giữ nguyên.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
ChatController::actionScenarioMyPage (app/Http/Controllers/ChatController.php)
ChatController::chatEditRichMenu (app/Http/Controllers/ChatController.php)
ChatController::isBlockedByFriend (app/Http/Controllers/ChatController.php - hàm mới)
Basic\ChatController::getBasicInfo (app/Http/Controllers/Basic/ChatController.php - xác nhận ngữ nghĩa line_user_id)
saveChangeOrStopStep / handleSaveEditStep / handleSaveEditRichMenu (public/js/chats/chat-v2.js)
saveChangeScenario (public/js/my_page/my_page.js)
saveChangeScenario (resources/views/basic/friend_detail/index.blade.php)
HandleCallback::doHandleUnfollow (app/Console/Commands/HandleCallback.php - xác nhận cờ chặn khi bạn bè chặn bot)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/ChatController.php
   - public/js/chats/chat-v2.js
   - public/js/my_page/my_page.js
   - resources/views/basic/friend_detail/index.blade.php
 • 4.2 Data ảnh hưởng:
   - Không có - chỉ đọc thêm bảng conversation (cột is_blocked, blocked_by), không thêm/sửa/xoá dữ liệu; ngược lại còn tránh ghi rác vào scenario_lineuser, scenario_step_time, bot_line_user.rich_menu_id, rich_menu_history cho bạn bè đã chặn
 • 4.3 Tính năng liên quan:
   - Chat 1:1 (FA-001) — tab thông tin cơ bản chặn thao tác bắt đầu bước và hiển thị menu hình ảnh với bạn bè đã chặn bot, có báo lỗi
   - Step Delivery / Scenario (FA-009) — thao tác bắt đầu/đổi bước thủ công bị chặn khi bạn bè đã chặn bot; thao tác dừng bước không đổi
   - Rich Menu (FA-004) — thao tác gán menu hình ảnh thủ công bị chặn khi bạn bè đã chặn bot; thao tác ẩn menu không đổi
   - My Page (FA-036) — trang cá nhân dùng chung API đổi kịch bản nên cũng bị chặn, nay có hiện thông báo lỗi
   - Friend Detail (outside glossary) — màn chi tiết bạn bè dùng chung API đổi kịch bản nên cũng bị chặn, nay có hiện thông báo lỗi

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/ChatController.php: No syntax errors detected; php -l resources/views/basic/friend_detail/index.blade.php: No syntax errors detected; node --check public/js/chats/chat-v2.js: OK; node --check public/js/my_page/my_page.js: OK; git merge-base --is-ancestor <base> ai_small_40222: OK (branch tách đúng từ đỉnh origin/release_step_20260805)
   Bằng chứng: Nguồn cờ chặn: HandleCallback.php:637 khi bạn bè chặn bot (unfollow) ghi conversation.is_blocked=1, blocked_by=0; functions.php:8111 khi quản trị chặn ghi blocked_by=1 - nên guard chỉ bắt blocked_by=0 cho khớp câu thông báo tiếng Nhật; Ngữ nghĩa khoá: conversation.tb_line_user_id = line_user.id (join tại ChatController và ConversationService), mọi điểm tạo conversation đều set cả line_id lẫn tb_line_user_id = line_user.id; Không kiểm chứng được trên DB dev: MySQL host.docker.internal:3306 Connection refused

■ TỰ REVIEW (AI)
Guard đặt ở tầng máy chủ (nguồn chân lý) nên phủ mọi màn gọi chung 2 API, không phụ thuộc trạng thái cũ ở trình duyệt. Chỉ chặn đúng 2 thao tác ticket nêu (bắt đầu bước, hiển thị menu); thao tác dừng bước và ẩn menu giữ nguyên để quản trị vẫn dọn được cho bạn bè đã chặn. Guard đặt TRƯỚC mọi lệnh gọi API LINE và mọi lệnh ghi dữ liệu nên không có nửa vời. Trường hợp không tìm thấy bản ghi hội thoại thì coi như chưa chặn, giữ nguyên hành vi cũ (không gây hồi quy).
 • Rủi ro / lưu ý khi test:
   - Chỉ chặn khi bạn bè chủ động chặn bot (người chặn = 0). Trường hợp quản trị chặn bạn bè (người chặn = 1) vẫn cho thao tác như cũ, vì câu thông báo tiếng Nhật trong ticket là dạng bị chặn. Nếu BA muốn chặn luôn cả trường hợp này thì cần chốt thêm câu thông báo riêng
   - Thêm 1 truy vấn đếm trên bảng hội thoại mỗi lần bấm 2 thao tác này. Là thao tác thủ công hiếm, lọc theo bot_id + tb_line_user_id nên tải không đáng kể
   - Hàm kiểm tra đặt trong bộ điều khiển (query Eloquent trực tiếp) thay vì tầng dịch vụ/kho như quy ước code mới - chọn cách này để bám sát code legacy xung quanh và giữ diff tối thiểu, tránh đổi hàm khởi tạo của bộ điều khiển hơn 6000 dòng
   - Không tái hiện được trên môi trường dev trong container (MySQL từ chối kết nối) nên cần tester xác nhận lại theo các bước tái hiện

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_40222 (nhánh gốc release_step_20260805, commit 11285b090b, 4 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 10 phút 25 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=688a872c-37f1-4604-b200-34cf6b9be7d2
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40222
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
