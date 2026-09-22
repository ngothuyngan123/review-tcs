# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #38393 bằng `/new-task`. Nguồn: **Journal #137191 (AI LME Fix bug — 2026-09-19)** = bản mới nhất, thay thế Journal #124599 (2026-07-02). Description Redmine không có section "Đánh giá ảnh hưởng" — đánh giá nằm trong journal auto-fixbug.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) — assignee Redmine: Ngọc Ánh |
| Commit / Pull Request | sns-line commit `9df5f81524` (tự review v1) · commit trước `3a0fd43306` · không có link PR |
| Branch | `ai_fixbug_38393` (nhánh gốc `release_step_20260623`) |
| Ngày submit đánh giá | 2026-09-19 (bản đầu 2026-07-02) |
| Auto-filled | 2026-09-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

getLineInfoBot() (functions.php) trả null khi API LINE lấy thông tin bot lỗi (token hết hạn/bot bị xoá/API 4xx — Guzzle ném exception, hàm trả null). Ở bản production, luồng ĐỔI BOT (ChangeBotController) gọi helper getValue(key, $infoBot) trên giá trị null này mà chưa guard, nên array_key_exists(key, null) trong thân getValue (functions.php:7190) ném lỗi PHP fatal. Ngoài ra vài chỗ khác gọi array_key_exists trực tiếp trên kết quả json_decode cùng kiểu lỗi.

## 2. Cách fix

Fix gốc tại helper dùng chung getValue(): thêm is_array() nên trả null an toàn khi $arr không phải mảng — bao trọn MỌI caller đọc displayName/basicId/pictureUrl từ thông tin bot LINE, gồm luồng đổi bot (ChangeBotController) là nơi bắn lỗi production. Bổ sung 2 crash-site gọi array_key_exists trực tiếp (không qua getValue): ChatController::reGetProfileBot và BotController::reGetAvatarBot → dùng getValue null-safe. (GetProfileBotDefault loại khỏi scope vì command chạy tay, không có trong Console/Kernel.)

**TỰ REVIEW v1 (commit 9df5f81524)** — sửa thêm 2 lỗi high là REGRESSION do chính bản fix gây ra: bỏ exception đi làm 3 lệnh UPDATE phía sau CHẠY TIẾP với giá trị rỗng, ghi đè mất ảnh/tên bot.
- (a) ChatController::reGetProfileBot:1212 + BotController::reGetAvatarBot:11400 — thêm `&& is_array($infoBot)` vào điều kiện 200 để rơi xuống nhánh else sẵn có (giữ nguyên `$bot->bot_image` / `$bot->view_name`) thay vì ghi `''` vào bots.bot_image/view_name + bots_profiles.avt_path/nick_name;
- (b) BotController::changeNewBotStep1:6566 — bọc `DB::table('bots_profiles')->update([...])` bằng `if(!empty($infoBot))` vì lệnh này nằm NGOÀI khối `if($infoBot)` ngay trên, sau khi getValue null-safe thì nó ghi NULL đè profile mặc định.
- Thêm logInfo (PSR-3 placeholder) ở cả 3 chỗ để ops truy nguyên khi body API /v2/bot/info không parse được JSON.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

getValue (app/Helpers/functions.php:7188) — **20 điểm gọi trên 8 file**, phân loại: (A) 8 điểm CHỈ ĐỌC → thuần lợi; (B) 9 điểm ghi DB nhưng có guard `if($infoBot)` bao ngoài → hành vi không đổi; (C) 3 điểm ghi DB KHÔNG guard → regression, đã sửa ở tự review v1.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `getValue` — app/Helpers/functions.php:7188 | Thêm `is_array()` guard | Root fix — helper dùng chung |
| 2 | `ChatController::reGetProfileBot` — app/Http/Controllers/ChatController.php:1201 | Dùng getValue null-safe + `&& is_array($infoBot)` (v1) | Route POST /ajax/reget-profile-bot; 2 điểm vào FE: chat-v2.js:4117 (bản đang chạy) + chat.js:1774 (bản cũ), blade layout/screen_chat/detail_content.blade.php:409 (nút 初期設定) + basic/chat/modal/setting_profile.blade.php:37 (modal プロフィール設定) |
| 3 | `BotController::reGetAvatarBot` — app/Http/Controllers/Admin/BotController.php:11387 | Dùng getValue null-safe + `&& is_array($infoBot)` (v1) | Route POST /ajax/reGetAvatarBot; gọi từ admin/bots/bot_add.blade.php:1545 + admin/bots/confirm_contract_standard.blade.php:643 (màn ADMIN, không phải FA-032 người dùng cuối) |
| 4 | `BotController::changeNewBotStep1` — app/Http/Controllers/Admin/BotController.php:6347 | Bọc update bots_profiles bằng `if(!empty($infoBot))` (v1) | Route POST /admin/step1-change-new-bot; KHÔNG có trong diff gốc nhưng hứng thay đổi hành vi của getValue (điểm ghi bots_profiles nằm ngoài guard) — nơi regression thứ 2 |
| 5 | `Ajax/ChangeBotController::init` — app/Http/Controllers/Ajax/ChangeBotController.php:43-57 | Không sửa (hưởng lợi từ getValue null-safe) | Route GET /ajax/change-bot/init: **CRASH SITE THẬT trên production** (chỉ dựng JSON response, không ghi DB). Dev khác đã vá cùng 3 dòng này trên release bằng `$infoBot ?? []` (commit b285b3acd9, 2026-07-01 18:48 +0900) |
| 6 | `Ajax/ChangeBotController::validateChannel:102-104` | Không sửa | An toàn sẵn nhờ `if (empty($infoBot)) return` ở dòng 88 |
| 7 | `BotController::step2Check:5482-5485`, `Basic/UserController:3099` + `:3923`, `functions.php:264-265 getLineIdOfBot`, `LiffController:1164`, `RecoverLineIdAndLiff.php:72` | Không sửa | Đều nằm trong guard `if($infoBot)` / `if($responseArr)` ⇒ hành vi KHÔNG đổi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev ghi mục 4.1 là **danh sách file thay đổi**: app/Helpers/functions.php · app/Http/Controllers/ChatController.php · app/Http/Controllers/Admin/BotController.php. Bảng dưới map F* theo mục 3 (không thêm function ngoài những gì Dev đã kê).

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getValue()` | app/Helpers/functions.php | Direct | Helper dùng chung, 20 caller / 8 file |
| F2 | `ChatController::reGetProfileBot` — POST /ajax/reget-profile-bot | app/Http/Controllers/ChatController.php | Direct | |
| F3 | `BotController::reGetAvatarBot` — POST /ajax/reGetAvatarBot | app/Http/Controllers/Admin/BotController.php | Direct | |
| F4 | `BotController::changeNewBotStep1` — POST /admin/step1-change-new-bot | app/Http/Controllers/Admin/BotController.php | Direct (sửa ở v1) | |
| F5 | `Ajax/ChangeBotController::init` — GET /ajax/change-bot/init | app/Http/Controllers/Ajax/ChangeBotController.php | Indirect (qua F1) | Crash site production |
| F6 | Caller có guard: step2Check, Basic/UserController, getLineIdOfBot, LiffController, RecoverLineIdAndLiff | nhiều file | Indirect — hành vi không đổi | Theo Dev |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bots.bot_image` (varchar(500) DEFAULT NULL) | UPDATE | Đổi HÀNH VI GHI: trước fix body API hỏng thì exception chặn, không ghi; sau fix ghi '' đè mất ảnh bot. Đã chặn ở tự review v1 |
| D2 | `bots.view_name` (varchar(128) DEFAULT NULL) | UPDATE | Như trên, mất tên hiển thị bot; lưu ý `bot_category.bot_view_name` là bản mirror denormalized của cột này nên có nguy cơ lệch dữ liệu |
| D3 | `bots_profiles.avt_path` (profile is_default=1) | UPDATE | Bị ghi '' ở reGetProfileBot/reGetAvatarBot và NULL ở changeNewBotStep1. Đã chặn cả 3 |
| D4 | `bots_profiles.nick_name` (profile is_default=1) | UPDATE | Như trên. Đã chặn cả 3 |
| D5 | API contract POST /ajax/reget-profile-bot và /ajax/reGetAvatarBot: `{success,img,nick_name}` | — | Trước fix trả success:false khi lỗi; sau fix (chưa sửa) trả success:true với img/nick_name rỗng; sau khi sửa trả success:true với giá trị CŨ |
| — | Schema DB | — | KHÔNG đổi — không migration, không thêm/xoá cột |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Dev không ghi mức risk — cột "Nguy cơ regression" để `<chưa rõ>` trừ khi Dev có nêu.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đổi bot / アカウント変更 (Change Bot, nhóm account-setting アカウント設定) — GET /ajax/change-bot/init: nơi exception thật sự bắn ra production (18 lần, step.lme.jp). Sau fix API bot lỗi chỉ làm hiện tên/ảnh rỗng thay vì HTTP 500 | F1, F5 | `<chưa rõ>` |
| T2 | Chat 1:1 (FA-001) — nút 初期設定 lấy lại ảnh/tên bot. HAI điểm vào: detail_content.blade.php:409 và modal プロフィール設定 setting_profile.blade.php:37; cả chat.js (cũ) lẫn chat-v2.js (đang chạy) | F2, D1–D5 | `<chưa rõ>` |
| T3 | Quản lý bot phía ADMIN (màn admin/bots: thêm tài khoản + duyệt hợp đồng) — reGetAvatarBot ở bot_add.blade.php:287 và confirm_contract_standard.blade.php:639. Lưu ý đây là màn admin nội bộ, KHÔNG phải FA-032 新規アカウント追加 của người dùng cuối | F3, D1–D5 | `<chưa rõ>` |
| T4 | Đổi sang bot mới — POST /admin/step1-change-new-bot (changeNewBotStep1): ghi bots_profiles của bot đang đổi, là nơi regression thứ 2 nằm. Đã sửa ở tự review v1 | F4, D3, D4 | `<chưa rõ>` |
| T5 | Thêm tài khoản mới (FA-032) — step2Check + Basic/UserController: dùng getValue nhưng đã có guard ⇒ hành vi KHÔNG đổi, chỉ an toàn hơn về lý thuyết | F6 | `<chưa rõ>` — Dev: hành vi không đổi |
| T6 | LIFF access + command recover:RecoverLineIdAndLiff — có guard, không đổi | F6 | `<chưa rõ>` — Dev: hành vi không đổi |

**Recover data:** ✔ Không cần recover data.

**Verify phía Dev:** Mức lint — `php -l` 3 file đã sửa: No syntax errors detected (chạy lại sau commit tự review v1). PHPUnit: KHÔNG chạy — getValue không có test class nào phủ (`grep -rl getValue tests/` rỗng). Cơ chế: PHP 7.4 `array_key_exists(null)` là E_WARNING, Laravel HandleExceptions đổi thành ErrorException — vì vậy TRƯỚC fix luồng nhảy sang catch và KHÔNG chạy lệnh UPDATE; SAU fix luồng chạy tiếp và ghi rỗng (gốc của 2 regression đã sửa ở v1). Branch tụt sau release 316 commit; Dev đã kiểm vùng sửa của cả 3 file vẫn nguyên văn trên `origin/release_step_20260623 @4f48ec4f4e` ⇒ merge sạch.

**Tự review (AI) — rủi ro khi test:** Rất thấp: getValue nay trả null thay vì fatal — các caller đã có `?:` hoặc `??` nên hành vi không đổi khi dữ liệu bình thường.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
