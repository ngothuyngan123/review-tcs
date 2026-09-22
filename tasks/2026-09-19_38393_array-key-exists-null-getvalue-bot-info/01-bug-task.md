# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #38393 bằng `/new-task` (2026-09-19). Metadata Redmine tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38393 — [AI][Bug Exception] array_key_exists() expects parameter # to be array, null given/var/www/html/sns-line/app/Helpers/functions.#` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không có category). Suy từ description + journal: helper dùng chung `getValue()` (app/Helpers/functions.php) — luồng đổi bot / アカウント変更 (Ajax/ChangeBotController, crash-site production), nút 初期設定 ở chat 1:1 (ChatController::reGetProfileBot), nút lấy lại avatar bot ở màn admin/bots (BotController::reGetAvatarBot). Studio xếp feature `bot-edit`. |

## Mô tả bug (bản dịch tiếng Việt)

*Ticket được tạo tự động bởi check-exception AI (từ exception bắn lên Chatwork).*

*Phân loại:* php_code_error — *Rủi ro:* high — *Đánh giá source:* yes
*Số lần cảnh báo:* 18 — *Số user lỗi:* 0
*Room:* SNSLineException — *Server:* step.lme.jp/
*Lần đầu:* 2026-06-30 10:54 UTC — *Lần cuối:* 2026-07-01 08:44 UTC

**Signature (đã chuẩn hoá)**
```
array_key_exists() expects parameter # to be array, null given/var/www/html/sns-line/app/Helpers/functions.#
```

**Đối chiếu source (sns-line Helpers/functions.php)**
- *Vị trí:* app/Helpers/functions.php:4757 ; app/Http/Controllers/ChatController.php:1202 ; app/Console/Commands/GetProfileBotDefault.php:76
- *Nguyên nhân:* json_decode(body API) trả null (JSON rỗng/hỏng) rồi gọi array_key_exists() trên null — thiếu check null/is_array.
- *Gợi ý sửa:* Kiểm tra is_array($parseJsonResponse) trước khi gọi array_key_exists(); thêm guard cho mọi chỗ decode response LINE/bot.

**Exception mẫu (mới nhất)**
```
Server: step.lme.jp/
 User: line.a@syu-service.net (153318)
 BotId: 203891
array_key_exists() expects parameter 2 to be array, null given/var/www/html/sns-line/app/Helpers/functions.php7190
```

## Steps to reproduce

<!-- Redmine không có Section "Tái hiện bug" — ticket do AI detect từ exception. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response (exception mẫu trong description — không có attachment)

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Môi trường phát hiện: **Production** (`step.lme.jp`). 18 lần cảnh báo, 0 user báo lỗi.
- Điều kiện kích hoạt: API LINE `/v2/bot/info` lỗi (token hết hạn / bot bị xoá / 4xx) hoặc body không parse được JSON → `getLineInfoBot()` trả null. Trên staging cần bot token sai, hoặc stub response body hỏng (api.line.me thật khó trả 200 + body null).
- Fix có **2 vòng**: commit `3a0fd43306` (2026-07-02) → tự review v1 commit `9df5f81524` (2026-09-19) sửa 2 regression ghi rỗng ảnh/tên bot do chính bản fix gây ra. Test trên commit mới nhất.
- Dev khác (tudv) đã vá độc lập 3 dòng ở `ChangeBotController.php:53/54/57` bằng `$infoBot ?? []` trên release (commit `b285b3acd9`, 2026-07-01).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `203891` |
| User (admin) | `line.a@syu-service.net (153318)` |
| Đối tượng cấu hình | API LINE `/v2/bot/info` của bot trên |
| Thời điểm lỗi | Lần đầu `2026-06-30 10:54 UTC` — lần cuối `2026-07-01 08:44 UTC` |
| Đối chứng | Bot có token hợp lệ (API trả 200 + JSON) — không lỗi |

## Journal / note từ Redmine (nguyên văn)

**Journal #124599 — AI LME Fix bug — 2026-07-02:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.

■ 1. NGUYÊN NHÂN
getLineInfoBot() (functions.php) trả null khi API LINE lấy thông tin bot lỗi (token hết hạn/bot bị xoá/API 4xx — Guzzle ném exception, hàm trả null). Ở bản production, luồng ĐỔI BOT (ChangeBotController) gọi helper getValue(key, $infoBot) trên giá trị null này mà chưa guard, nên array_key_exists(key, null) trong thân getValue (functions.php:7190) ném lỗi PHP fatal. Ngoài ra vài chỗ khác gọi array_key_exists trực tiếp trên kết quả json_decode cùng kiểu lỗi.

■ 2. CÁCH FIX
Fix gốc tại helper dùng chung getValue(): thêm is_array() nên trả null an toàn khi $arr không phải mảng — bao trọn MỌI caller đọc displayName/basicId/pictureUrl từ thông tin bot LINE, gồm luồng đổi bot (ChangeBotController) là nơi bắn lỗi production. Bổ sung 2 crash-site gọi array_key_exists trực tiếp (không qua getValue): ChatController::reGetProfileBot và BotController::reGetAvatarBot → dùng getValue null-safe. (GetProfileBotDefault loại khỏi scope vì không còn dùng.)

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
getValue (app/Helpers/functions.php:7188)
ChatController::reGetProfileBot (app/Http/Controllers/ChatController.php:1199) — route POST /ajax/reget-profile-bot, gọi từ chat-v2.js
BotController::reGetAvatarBot (app/Http/Controllers/Admin/BotController.php:11387) — route POST /ajax/reGetAvatarBot, gọi từ bot_add.blade

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi: app/Helpers/functions.php · app/Http/Controllers/ChatController.php · app/Http/Controllers/Admin/BotController.php
 • 4.2 Data ảnh hưởng: Không có — chỉ thêm guard null, không đổi schema/dữ liệu
 • 4.3 Tính năng liên quan: Change Bot (ChangeBotController) · Chat 1:1 (FA-001) nút 初期設定 · Add New Account (FA-032) reGetAvatarBot

■ 5. RECOVER DATA: ✔ Không cần recover data
■ 6. VERIFY: lint — php -l 4 file đã sửa: No syntax errors detected
■ BRANCH / COMMIT: sns-line: ai_fixbug_38393 (nhánh gốc release_step_20260623, commit 3a0fd43306, 3 file) [đã push]
```

**Journal #137191 — AI LME Fix bug — 2026-09-19:**

```
(Bản đầy đủ — xem file 03-dev-impact.md, được parse từ journal này.)
Điểm mới so với journal #124599:
- TỰ REVIEW v1 (commit 9df5f81524) — sửa thêm 2 lỗi high là REGRESSION do chính bản fix gây ra: bỏ exception đi làm 3 lệnh UPDATE phía sau CHẠY TIẾP với giá trị rỗng, ghi đè mất ảnh/tên bot.
  (a) ChatController::reGetProfileBot:1212 + BotController::reGetAvatarBot:11400 — thêm '&& is_array($infoBot)' vào điều kiện 200 để rơi xuống nhánh else sẵn có (giữ nguyên $bot->bot_image/$bot->view_name) thay vì ghi '' vào bots.bot_image/view_name + bots_profiles.avt_path/nick_name;
  (b) BotController::changeNewBotStep1:6566 — bọc DB::table('bots_profiles')->update([...]) bằng if(!empty($infoBot)) vì lệnh này nằm NGOÀI khối if($infoBot) ngay trên, sau khi getValue null-safe thì nó ghi NULL đè profile mặc định.
  Thêm logInfo (PSR-3 placeholder) ở cả 3 chỗ để ops truy nguyên khi body API /v2/bot/info không parse được JSON.
- Branch: sns-line: ai_fixbug_38393 (nhánh gốc release_step_20260623, commit 9df5f81524, 3 file) [đã push]
```
