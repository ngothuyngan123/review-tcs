# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41885 — [Kết nối bot] Chạy lại bước 2 (step2Check) trên bot tạm làm nhân đôi dữ liệu mặc định: status chat, mục thông tin bạn bè chat 1-1, profile mặc định, add_friend_setting` |
| Module / Màn hình | `Add New Account (FA-032) — bước 2 kết nối bot (step2Check / step2-check-friend), PC接続 wizard Path B. Ảnh hưởng lan ra: Chat 1:1 (FA-001 — status chat, khung thông tin bạn bè), Broadcast (FA-008 — filter theo status chat), ActionSchedule (filter theo status chat)` |

## Mô tả bug (bản dịch tiếng Việt)

Phát hiện khi rà soát triển khai ngang cho Bug KH #40599 (notify_setting bị tạo trùng → thông báo trên app nhận 2 lần). Fix #40599 chỉ chặn trùng cho riêng `notify_setting`. Các dữ liệu mặc định khác được tạo trong cùng đoạn code vẫn bị nhân đôi theo đúng kịch bản đó.

**Hiện tượng:**

Bot được kết nối theo kịch bản tái hiện bên dưới, sau khi kết nối xong:
- Danh sách trạng thái chat (status chat): mỗi trạng thái mặc định hiện 2 lần. Bị ở chat 1-1 trên app, filter của 一斉配信 (broadcast) và アクション予約 (action schedule).
- Khung thông tin bạn bè ở chat 1-1: trùng 3 mục LINE名 / 友だち追加日時 / システム表示名.
- Danh sách profile của user: có 2 profile mặc định.
- `add_friend_setting`: có 2 dòng cho cùng bot. Không lộ ra UI vì mọi nơi đọc đều lấy `->first()`, chỉ là dữ liệu rác.

Mỗi lần chạy lại bước 2 thêm 1 bộ nữa (chạy 3 lần → 3 bộ).

## Steps to reproduce

Kịch bản: PC接続 wizard, Path B.

1. Thêm bot mới bằng PC接続, cố ý dùng LINE Login channel thuộc provider KHÁC với Messaging API channel.
2. Tới SCR-21 (LINE Login channel), bấm 「次のステップへ」 → gọi `/admin/step2-check` lần 1 → tạo bot tạm (`is_deleted=2`) kèm toàn bộ dữ liệu mặc định, hiện QR (SCR-22).
3. Quét QR, kết bạn → `/admin/step2-check-friend` trả `fail_provider` → bot tạm được giữ lại, không xoá (Task #36412).
4. Bấm 「Step 2に戻って対処法を確認する」 → 「解決したのでログインチャネル設定に戻る」 → về SCR-21, đổi sang LINE Login channel cùng provider → 「次のステップへ」 → gọi `/admin/step2-check` lần 2 (dùng lại đúng bot tạm, cùng `bot_id`).
5. Quét QR, kết nối thành công.
6. Chạy các câu SQL kiểm tra ở mục "Ghi chú thêm của Leader" cho `bot_id` vừa tạo.

> **Cách nhanh cho dev**: khi bot tạm (`is_deleted=2`, cùng `admin_id` + `channel_id`) còn tồn tại, gọi lại `/admin/step2-check` với cùng credential (không cần thao tác lại toàn bộ wizard).

## Expected result

- Mỗi bot chỉ có 1 bộ dữ liệu mặc định (status_chat, setting_display_info_friend_chat11, add_friend_setting, bots_profiles), dù chạy lại bước 2 bao nhiêu lần.

## Actual result

- Mỗi bảng dữ liệu mặc định (status_chat, setting_display_info_friend_chat11, add_friend_setting, bots_profiles) có thêm 1 bộ mới cho cùng `bot_id` mỗi lần chạy lại bước 2.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #41885 không có attachment. -->

## Ghi chú thêm của Leader

- Bug tự detect (AI Reader), không phải khách hàng báo trực tiếp. Status Redmine hiện tại: **Fix done - Đợi test**.
- **Dữ liệu đã bị nhân đôi trên production CHƯA được Recover data** (xem mục "RECOVER DATA" ở `03-dev-impact.md`) — Leader cần yêu cầu Dev chạy SQL Recover data trước/song song khi test, vì status_chat và bots_profiles thừa có thể đã được dùng (conversation đã gán status, profile đã được chọn để gửi tin) → phải chuyển tham chiếu sang bản giữ lại trước khi xoá, không xoá thẳng.
- SQL kiểm tra dữ liệu đã bị lặp (dùng để verify trước/sau fix, và trước/sau khi Recover data production):
  ```sql
  SELECT bot_id, name_status, COUNT(*) c FROM status_chat GROUP BY bot_id, name_status HAVING c > 1;
  SELECT bot_id, id_setting, COUNT(*) c FROM setting_display_info_friend_chat11 WHERE type = 0 GROUP BY bot_id, id_setting HAVING c > 1;
  SELECT bot_id, user_id, COUNT(*) c FROM bots_profiles WHERE is_default = 1 GROUP BY bot_id, user_id HAVING c > 1;
  SELECT bot_id, COUNT(*) c FROM add_friend_setting GROUP BY bot_id HAVING c > 1;
  ```
  ⚠️ Câu status_chat có thể bắt nhầm nếu user tự tạo status trùng tên status mặc định → cần đối chiếu thêm trước khi kết luận là bug.
- Dev tự đánh giá (trong Redmine, trước khi fix — xem thêm bản fix thực tế đã triển khai ở `03-dev-impact.md`):
  - `ActionInfoFriendDefault` trong `step2Check` đã có kiểm tra tồn tại từ trước nên KHÔNG bị bug này.
  - `BotUsers` (dòng 5886-5889 branch gốc) cũng tạo vô điều kiện, nhưng luồng v5 gửi `ids=[]` nên không phát sinh; luồng cũ (`public/js/admin/add_bot/steps.js`, `public/js/admin/step_add_bot.js`) có gửi ids thì có thể bị — **cần hỏi lại Dev xem luồng cũ này còn được dùng không** trước khi quyết định có cần TC riêng.
- Ticket liên quan:
  - Bug KH #40599 — notify_setting bị tạo trùng, cùng kịch bản, đã fix bằng `firstOrCreate` + UNIQUE (bot_id, user_id).
  - Task #36409 — reuse bot tạm ở bước 2 (nguồn gốc sinh ra kịch bản gọi lại `step2Check`).
  - Task #36412 — giữ bot tạm khi quét QR bị `fail_provider` (lý do bot tạm tồn tại đủ lâu để bị gọi lại).

## Journal / note từ Redmine (nguyên văn)

**Journal #139877 — AI LME Fix bug — 2026-10-03:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Ở bước 2 kết nối bot (step2Check), nếu đã có bot tạm cùng admin + channel thì hệ thống dùng lại bot cũ, nhưng các dữ liệu mặc định phía sau (trạng thái chat, 3 mục thông tin bạn bè ở chat 1-1, cài đặt khi thêm bạn, profile mặc định, liên kết nhân viên) vẫn được tạo vô điều kiện nên mỗi lần chạy lại bước 2 sinh thêm 1 bộ trùng. Fix #40599 trước đó mới chặn trùng riêng cài đặt thông báo.

■ 2. CÁCH FIX
Trong step2Check (nhánh tạo bot, có dùng lại bot tạm) chỉ tạo dữ liệu mặc định khi bot chưa có: status chat (khi bot chưa có status nào), 3 mục thông tin bạn bè chat 1-1 (khi chưa có dòng type=0), profile mặc định (khi chưa có is_default=1 của cặp bot+user), add_friend_setting và user_bot đổi sang firstOrCreate. Kèm sửa kiểm tra bots_tutorial từ cột id sang bot_id (refix vòng 1) — hệ quả phụ: bot mới kết nối qua bước 2 nay luôn có dòng tutorial (trước đây có thể thiếu nếu id tutorial của bot khác trùng số với bot_id). Tự review v1: bổ sung report cho đầy đủ, không đổi code.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
BotController::step2Check (app/Http/Controllers/Admin/BotController.php)
BotController::finalizeBot (đối chứng, cùng file)
BotController::preCreateBot EP-17 (nhánh existingBot idempotent, cùng file)
BotController::changeNewBotStep1 (mẫu guard AddFriendSetting count==0)
BotController::botChange / saveOlioa / saveChangeBot / saveBotAfterLogin (luôn insertGetId bot mới)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/BotController.php
 • 4.2 Data ảnh hưởng:
   - status_chat, setting_display_info_friend_chat11 (type=0), add_friend_setting, bots_profiles (is_default=1), user_bot — chỉ không tạo thêm khi bot đã có; bot mới lần đầu vẫn tạo đủ như cũ
   - bots_tutorial — kiểm tồn tại theo bot_id thay vì khoá chính id: không tạo trùng khi chạy lại, và bot mới không còn bị bỏ sót dòng tutorial khi id tutorial của bot khác trùng số với bot_id
 • 4.3 Tính năng liên quan:
   - Add New Account (FA-032) — bước 2 kết nối bot (PC接続) không còn nhân đôi dữ liệu mặc định khi chạy lại trên bot tạm
   - Chat 1:1 (FA-001) — danh sách trạng thái chat và khung thông tin bạn bè hết bị trùng mục với bot kết nối theo kịch bản chạy lại bước 2
   - Broadcast (FA-008) — bộ lọc trạng thái chat hết hiện trạng thái trùng
   - Tutorial cho bot mới — bot kết nối qua bước 2 nay luôn được tạo dữ liệu tutorial (hiện hướng dẫn), cần retest màn tutorial sau khi kết nối

■ 5. RECOVER DATA
   ⚠ CÓ — Bot đã kết nối theo kịch bản chạy lại bước 2 trước khi có fix đang có dữ liệu mặc định trùng. Cần human chạy SQL dọn riêng: giữ bản ghi id nhỏ nhất mỗi nhóm, xoá bản thừa. Lưu ý status_chat thừa có thể đã được gán cho hội thoại (conversation status) và bots_profiles thừa có thể đã được chọn làm profile gửi — phải chuyển tham chiếu về bản giữ lại trước khi xoá. (phạm vi: status_chat (bot_id,name_status), setting_display_info_friend_chat11 (bot_id,type=0,id_setting), bots_profiles (bot_id,user_id,is_default=1), add_friend_setting (bot_id))

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Admin/BotController.php: No syntax errors; git diff --stat release_step_20260930_v2...ai_fixbug_41885: 1 file, chỉ step2Check
   Bằng chứng: Dev MySQL host.docker.internal:3306 Connection refused — không kiểm được dữ liệu trùng trên dev, không tái hiện runtime; Đối chứng finalizeBot (EP-18) đã guard bằng hasSettings/hasProfile — fix theo đúng mẫu

■ TỰ REVIEW (AI)
Fix tối thiểu trong step2Check, theo đúng mẫu guard của finalizeBot; bot mới lần đầu không đổi hành vi. Không kiểm được runtime do dev DB không kết nối được.
 • Rủi ro / lưu ý khi test:
   - Guard status_chat theo 'bot chưa có trạng thái nào': trên bot tạm người dùng chưa thao tác nên an toàn
   - user_bot firstOrCreate theo (bot_id,user_id) không xét is_deleted — bot tạm không có thao tác xoá nhân viên nên không ảnh hưởng
   - Dữ liệu trùng đã phát sinh trên production chưa được dọn (cần SQL riêng)
   - Refix vòng 1: guard bots_tutorial đổi sang where(bot_id) như finalizeBot; chỗ where(id,$bot_id)->update ở luồng khác (dòng 6913) không đụng

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41885 (nhánh gốc release_step_20260930_v2, commit e8a74f3123, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 25 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=3da70980-59e7-4cfe-8c08-a854e8147eac
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=41885
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
