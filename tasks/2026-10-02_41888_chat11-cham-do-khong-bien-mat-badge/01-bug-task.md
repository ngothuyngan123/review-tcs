# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41888 — [02-10-2026][31373][Chat 1:1] Khách báo chấm đỏ thông báo chưa đọc ở Chat 1:1 không biến mất dù tab "chưa xác nhận" không có tin nhắn nào.` |
| Module / Màn hình | Chat 1:1 (1:1チャット) › チャット管理 (Quản lý chat) — nút 「確認済みに変更」(Đổi thành đã xác nhận) cạnh ô nhập tin + chấm đỏ/badge menu 1:1チャット |

## Mô tả bug (bản dịch tiếng Việt)

Ticket do hệ thống tạo từ Slack (OEM đăng, quản lý số 31373).

User: info@car-smile.love
Bot Name: CARSM i LE

Không có tin nhắn chưa đọc nhưng chấm đỏ thông báo 🔴 không biến mất.

Tại 1:1チャット › チャット管理 (Chat 1:1 › Quản lý chat), dù bấm tab chỉ 「未確認のみ」 (chỉ chưa xác nhận) thì cũng hiện thông báo 「該当するメッセージがありません」(không có tin nhắn phù hợp), nhưng dấu chấm đỏ ① thông báo chưa đọc của 1:1チャット vẫn không biến mất, khách đang gặp khó khăn.

Tên friend (ca khách báo): まや (若林まや　黒プリウス)
Chức năng: Chat 1:1 (1:1チャット)
Thời điểm phản hồi: 2026/10/02 11:29:00

## Steps to reproduce

> Steps do QA (Đoàn Thị Bích Hảo) tái hiện trên acc test ngày 02/10/2026 — xem nguyên văn ở Journal #139758 bên dưới.

1. Tại màn hình Export CSV, thực hiện export CSV có chứa cột ステータスメッセージ.
2. Download file CSV về máy.
3. Mở file CSV và tìm 1 user cần test.
4. Tại cột ステータスメッセージ của user đó, thay đổi giá trị thành 0.
5. Lưu lại file CSV sau khi chỉnh sửa.
6. Tại màn hình Import CSV, import file CSV vừa chỉnh sửa.
7. Sau khi import thành công, chuyển sang màn hình Chat 1:1.
8. Reload màn hình Chat 1:1.
9. Kiểm tra user đã chỉnh sửa ở bước 4.
10. User xuất hiện chấm đỏ thông báo chưa đọc dù không có message chưa đọc.
11. Thực hiện thao tác đánh dấu đã đọc đối với user này (bấm 「確認済みに変更」).

## Expected result

- User không còn tin nhắn chưa đọc → chấm đỏ thông báo + badge chưa đọc của 1:1チャット phải biến mất.
- Thao tác 「確認済みに変更」 (Đổi thành đã xác nhận) phải thực hiện thành công, không báo lỗi.

## Actual result

- Dù tab 「未確認のみ」 (chỉ chưa xác nhận) trống — không có tin nào — chấm đỏ thông báo + badge chưa đọc của 1:1チャット vẫn không biến mất.
- Bấm 「確認済みに変更」 thì hệ thống báo lỗi 「未読メッセージがありません。」(không có tin nhắn chưa đọc) và không làm gì cả → chấm đỏ/badge kẹt vĩnh viễn.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.watermelon.vn/attachments/download/31310/screenshot1.png
- screenshot2.png — https://redmine.watermelon.vn/attachments/download/31311/screenshot2.png

## Ghi chú thêm của Leader

- Trạng thái ticket: **Fix done - Đợi test**, Priority Normal. Branch fix đã push: `ai_fixbug_41888` (nhánh gốc `release_step_20260930`, commit `e1e35fcf99`).
- Root cause (theo AI Auto-fixbug — chi tiết ở `03-dev-impact.md`): guard thêm ở bản phát hành 30/09 (#41634) chỉ kiểm bảng tin chưa xác nhận (`unconfirm_message`), bỏ qua trường hợp cờ `confirm_count` của hội thoại bị lệch (=1) nhưng bảng tin trống → chặn nhầm nút "Đổi thành đã xác nhận", không reset được cờ → chấm đỏ/badge kẹt vĩnh viễn.
- ⚠️ Nguồn gốc gây lệch dữ liệu (job `linect` ghi `unconfirm_message` và `confirm_count` bằng 2 câu lệnh riêng rẽ, không nguyên tử, có thể đua với thao tác trên web) **CHƯA được xử lý** trong fix này — ngoài phạm vi (thuộc job Java, fix chỉ sửa PHP). Cần lưu ý khi review để không bỏ sót rủi ro tái phát lệch dữ liệu.
- Dev tự nhận: **chưa verify runtime** (DB dev không truy cập được lúc fix) — chỉ verify mức lint (`php -l`) + `git diff --stat`, không có test tự động cho endpoint này.
- Workaround cho khách trước khi release: dùng thao tác đánh dấu tất cả đã đọc / quick action đổi đã đọc trong danh sách bạn bè Chat 1:1.
- Môi trường QA tái hiện: gọi là "acc test" trong journal, không ghi rõ tên môi trường cụ thể (dev/staging) — bot_id/line_user_id xem bảng dưới.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `218363` (ca QA tái hiện trên acc test, theo Journal #139758) |
| Friend | line_user_id: `60433702` (QA repro) |
| Đối tượng cấu hình | Hội thoại Chat 1:1 bị lệch cờ chưa xác nhận — dựng bằng Export CSV → sửa cột `ステータスメッセージ` = 0 → Import CSV lại |
| Thời điểm lỗi | Khách báo: 2026/10/02 11:29:00; QA tái hiện: 2026/10/02 |
| Đối chứng | Ca khách báo gốc: friend まや (若林まや　黒プリウス), bot "CARSM i LE", user `info@car-smile.love` — xem ảnh 1/2 đính kèm (dashboard: https://dashboard.melonglobal.net/css-analytics/?id=31373) |

## Journal / note từ Redmine (nguyên văn)

**Journal #139744 — AI LME Fix bug — 2026-10-02:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Hội thoại 若林まや bị lệch dữ liệu: cờ chưa xác nhận của hội thoại vẫn bằng 1 (nên còn chấm đỏ ở danh sách và vẫn được đếm vào badge 1:1チャット) nhưng không còn bản ghi tin chưa xác nhận nào, nên tab chưa xác nhận ở màn Quản lý chat trống. Trước đây bấm nút "Đổi thành đã xác nhận" sẽ tự đưa cờ về 0; từ bản phát hành 30/09 (#41634) nút này thêm điều kiện chỉ nhìn bảng tin chưa xác nhận, thấy rỗng là báo lỗi 「未読メッセージがありません。」 (đúng như ảnh 2 của khách) và không reset gì, nên chấm đỏ + badge kẹt vĩnh viễn.

■ 2. CÁCH FIX
Sửa điều kiện chặn của nút "Đổi thành đã xác nhận" ở Chat 1:1: chỉ báo lỗi "không có tin chưa đọc" khi hội thoại THẬT SỰ không còn gì chưa xác nhận (không còn bản ghi tin chưa xác nhận VÀ cờ chưa xác nhận của hội thoại = 0); hội thoại còn cờ lệch thì cho chạy tiếp để reset cờ về 0 và tính lại badge. Quét ngang: 2 lối vào cùng kiểu chặn (/basic/rec_message, /basic/update-status-confirm) chỉ còn được màn chat cũ / hàm JS không ai gọi dùng — không sửa, chỉ ghi chú.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
Basic\ChatController::confirmMessage (app/Http/Controllers/Basic/ChatController.php) — đã sửa
ConversationService::confirmMessage / changeStatusReadMessage (app/Services/ConversationService.php) — reset confirm_count + tính lại bots.count_user_unconfirm
totalUserConfirmMessage (app/Helpers/functions.php) — badge đếm conversation.confirm_count=1
sidebar.blade.php + countBadge — badge đọc bots.count_user_unconfirm
BotLineUser::makeDataTalkList / getListMessagesV2 (app/BotLineUser.php) — tab 未確認のみ đọc unconfirm_message
ChatController::confirm (/basic/rec_message) + ChatController::updateStatusConfirm (app/Http/Controllers/ChatController.php) — cùng kiểu chặn, lối vào đã chết
chat-v2.js confirmMessage — FE gọi /basic/confirm-message
linect HandlePostbackTask (save UnconfirmMessage rồi updateLastMessage set confirm_count=1, 2 bước không nguyên tử) — chỉ đọc

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/ChatController.php
 • 4.2 Data ảnh hưởng:
   - conversation.confirm_count / status_last_message / has_status_0/1 — được reset về đã xác nhận khi bấm nút trên hội thoại đang lệch (trước đây bị chặn)
   - bots.count_user_unconfirm — tính lại sau khi reset (giống luồng sẵn có)
 • 4.3 Tính năng liên quan:
   - Chat 1:1 (FA-001) — nút đổi thành đã xác nhận reset được chấm đỏ của hội thoại lệch dữ liệu, badge menu 1:1チャット cập nhật đúng
   - Chat / Talk Management (FA-002) — không đổi code; số badge giờ khớp lại với tab chưa xác nhận sau khi khách bấm xác nhận

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Basic/ChatController.php: No syntax errors; git diff --stat release_step_20260930...ai_fixbug_41888: 1 file, +7/-1; Không có test sẵn cho endpoint; DB dev host.docker.internal:3306 Connection refused nên chưa chạy được harness/đếm số hội thoại lệch
   Bằng chứng: Ảnh 2 của khách: bấm 確認済みに変更 hiện 「未読メッセージがありません。」 — đúng câu của guard #41634 tại Basic\ChatController::confirmMessage; Guard thêm ở commit 65d833534b (2026-09-26), có trong release_step_20260930 — khớp thời điểm khách báo 02/10; Badge = count conversation.confirm_count=1 (totalUserConfirmMessage), tab 未確認のみ = unconfirm_message ⇒ lệch 2 nguồn là trạng thái duy nhất cho ra triệu chứng; job linect ghi 2 nguồn bằng 2 câu lệnh riêng (lưu UnconfirmMessage rồi mới set confirm_count=1) nên có thể lệch khi đua với thao tác xác nhận trên web

■ TỰ REVIEW (AI)
Sửa 1 điều kiện ở cửa vào: guard 422 của #41634 giữ nguyên cho hội thoại thật sự đã xác nhận hết, chỉ mở cho hội thoại còn cờ confirm_count. Truy vấn thêm 1 câu value() theo PK + bot_id (đã kiểm sở hữu ở trên).
 • Rủi ro / lưu ý khi test:
   - Nguồn gốc lệch dữ liệu (job linect ghi unconfirm_message và confirm_count bằng 2 câu riêng, đua với thao tác xác nhận trên web) chưa xử lý — thuộc job Java, ngoài phạm vi chỉ-sửa-PHP; fix này chỉ trả lại đường tự chữa cho người dùng
   - Chưa verify runtime do DB dev không truy cập được
   - Workaround ngay cho khách trước khi phát hành: dùng thao tác đánh dấu tất cả đã đọc / quick action đổi đã đọc trong danh sách bạn bè Chat 1:1

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41888 (nhánh gốc release_step_20260930, commit e1e35fcf99, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 5 phút 36 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=4fadaa5d-6594-42b3-bdf2-c408111ae53e
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=41888
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #139758 — Đoàn Thị Bích Hảo — 2026-10-02:**

```
Tái hiện bug 2/10/2026 trên acc test:

Steps:
1. Tại màn hình Export CSV, thực hiện export CSV có chứa cột ステータスメッセージ.
2. Download file CSV về máy.
3. Mở file CSV và tìm 1 user cần test.
4. Tại cột ステータスメッセージ của user đó, thay đổi giá trị thành 0.
5. Lưu lại file CSV sau khi chỉnh sửa.
6. Tại màn hình Import CSV, import file CSV vừa chỉnh sửa.
7. Sau khi import thành công, chuyển sang màn hình Chat 1:1.
8. Reload màn hình Chat 1:1.
9. Kiểm tra user đã chỉnh sửa ở bước 4:
10. User xuất hiện chấm đỏ thông báo chưa đọc dù không có message chưa đọc.
11. Thực hiện thao tác đánh dấu đã đọc đối với user này.

=> Actuals: hiển thị thông báo lỗi "未読メッセージがありません。"

bot_id: 218363
line_user_id: 60433702
```
