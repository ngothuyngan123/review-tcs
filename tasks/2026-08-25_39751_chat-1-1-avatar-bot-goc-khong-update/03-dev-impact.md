# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Nguồn: journal AI Auto-fixbug** (Redmine #39751, journal #131960, 2026-08-21 04:19 UTC) — **KHÔNG phải Dev người viết**. Nội dung dưới đây paste nguyên văn từ báo cáo AI. Tester/Leader phải đối chiếu lại mục 3 (caller đã check) và mục 4.1 trước khi chốt coverage.
>
> ⚠️ **Dev KHÔNG chạy thực nghiệm** — mục 6 VERIFY ghi rõ: *"CHƯA kiểm chứng thực nghiệm: dev stack MySQL host.docker.internal:3306 từ chối kết nối (Connection refused) nên không chạy được truy vấn/tái hiện thật; kết luận dựa trên đọc code"*. Mức verify chỉ = **lint** (`php -l`).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine hiện tại: `Đoàn Thị Bích Hảo` |
| Commit / Pull Request | `sns-line` commit `fda3c1e983` (1 file, +18/-2) — **đã push**. Không có link PR Github/Gitlab trong Redmine. Session AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=727093c9-c59e-4c4f-8847-3aefbf49c8a9 · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=39751 |
| Branch | `ai_fixbug_39751` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-21` |
| Auto-filled | `2026-08-25 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "■ 1. NGUYÊN NHÂN" của journal #131960 -->

Khung chat 1:1 trên web dựng thông tin người gửi của tin đã gửi bằng ảnh chụp lưu trong bảng hồ sơ người gửi, trong khi ảnh thật của bot gốc nằm ở cột ảnh đại diện của bot — mọi màn CHỌN hồ sơ (web lẫn app) đều ghi đè bằng ảnh bot cho hồ sơ mặc định, riêng 2 chỗ dựng dữ liệu tin đã gửi thì không, nên sau khi bot đổi avatar thì hover vào tin vẫn ra ảnh cũ. Ngoài ra ảnh bot upload từ trong LME được lưu dạng đường dẫn tương đối của máy chủ media, còn giao diện chat gắn thẳng giá trị đó vào thẻ ảnh nên ảnh không tải được và rơi về avatar mặc định.

> **Ghi chú Leader**: đây là **2 root cause tách biệt** trong cùng 1 ticket —
> (a) hồ sơ mặc định dùng **ảnh snapshot cũ** thay vì ảnh bot hiện tại;
> (b) ảnh bot upload từ LME lưu **đường dẫn tương đối** → 404 → rơi về placeholder.
> TC phải cover **cả 2** riêng biệt, không gộp làm một.

## 2. Cách fix

<!-- Nguyên văn mục "■ 2. CÁCH FIX" của journal #131960 -->

Sửa 2 chỗ dựng thông tin người gửi của chat 1:1 web (danh sách tin khi mở hội thoại và tin nhận realtime qua socket): với hồ sơ mặc định (bot gốc) lấy ảnh đại diện hiện tại của bot thay vì ảnh chụp cũ trong bảng hồ sơ, đúng như cách các màn chọn hồ sơ vẫn làm; đồng thời chuẩn hoá ảnh bot thành URL đầy đủ của máy chủ media (dùng helper sẵn có) để ảnh upload từ LME hiển thị được. Quét ngang còn 3 chỗ cùng kiểu chưa sửa vì khác phạm vi: 2 chỗ hiển thị cho app điện thoại và nội dung trích dẫn lưu lúc gửi.

> ⚠️ **Dev tự khai còn 3 chỗ cùng kiểu CHƯA sửa** (khác phạm vi): 2 chỗ hiển thị cho **app điện thoại** + **nội dung trích dẫn (quoted)** lưu lúc gửi. Pre-Conditions của bug report (file 01) có nhắc "trên app chọn bot gốc gửi tin" → Leader chốt scope trước khi member viết TC.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN" — Dev list dạng plain, convert sang bảng. Cột "Thay đổi" suy từ mục 4.1 (chỉ 1 file thay đổi). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ChatController::refreshMessage` (`app/Http/Controllers/ChatController.php`) | **CÓ SỬA** | Chỗ dựng danh sách tin khi mở hội thoại — 1 trong 2 điểm fix chính |
| 2 | `ChatController::getMessageSocket` (`app/Http/Controllers/ChatController.php`) | **CÓ SỬA** | Chỗ dựng tin nhận realtime qua socket — 1 trong 2 điểm fix chính |
| 3 | `ChatController::ajaxGetProfileOfBots` (`app/Http/Controllers/ChatController.php`) | Không sửa | Màn chọn hồ sơ — đã sẵn quy ước "hồ sơ mặc định lấy ảnh bot" (`:1071/1079/1100`), dùng làm chuẩn để fix theo |
| 4 | `ChatController::saveSelectedProfileBot` (`app/Http/Controllers/ChatController.php`) | Không sửa | Lưu hồ sơ được chọn — đã sẵn quy ước (`:1147`) |
| 5 | `ChatController::reGetProfileBot` (`app/Http/Controllers/ChatController.php`) | Không sửa | Lấy lại hồ sơ bot |
| 6 | `Admin\BotController::reGetAvatarBot` (`app/Http/Controllers/Admin/BotController.php`) | Không sửa | Đồng bộ avatar bot từ LINE (button "đồng bộ" ở Pre-Conditions bug) |
| 7 | `Admin\SettingBotController::update` (`app/Http/Controllers/Admin/SettingBotController.php`) | Không sửa | Chỉ ghi `bots.bot_image` (đường dẫn tương đối), **không đồng bộ** `bots_profiles.avt_path` (`:246`) → nguồn gây lệch dữ liệu |
| 8 | `Api\ChatController::getProfileOfBots` (`app/Http/Controllers/Api/ChatController.php`) | Không sửa | API app — đã sẵn quy ước (`:3756/3766`) |
| 9 | `checkFullUrl` (`app/Helpers/functions.php`) | Không sửa (dùng lại) | Helper phân biệt URL đầy đủ vs đường dẫn tương đối |
| 10 | `content_chat.blade.php` (`resources/views/basic/chat/`) | Không sửa | Gắn thẳng `item.bot_send.bot_image` vào thẻ `img` (không qua `getUrlDomain` như modal hồ sơ) → đường dẫn tương đối sẽ 404 rồi rơi về `/images/avatar_bot_v2.png` |
| 11 | `chat-v2.js` hover `.bot_send_content` + `getUrlDomain` (`public/js/chats/chat-v2.js`) | Không sửa | JS xử lý hover hiển thị thông tin người gửi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục "■ 4.1 File thay đổi" — Dev CHỈ liệt kê file, KHÔNG liệt kê function. Bảng dưới tách theo mục 2 + mục 3. -->

> ⚠️ **Dev chỉ ghi 1 dòng file**: `app/Http/Controllers/ChatController.php`. Bảng dưới đây do `/new-task` tách ra từ mục 2 + mục 3 — **Leader BẮT BUỘC verify**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChatController::refreshMessage` | `app/Http/Controllers/ChatController.php` | Direct | Dựng danh sách tin khi mở hội thoại (endpoint `GET /basic/refresh_message`). Hồ sơ mặc định → lấy ảnh bot hiện tại + chuẩn hoá URL media |
| F2 | `ChatController::getMessageSocket` | `app/Http/Controllers/ChatController.php` | Direct | Dựng tin nhận realtime qua socket. Cùng logic với F1 |
| F3 | `checkFullUrl` + env `URL_SERVER_MEDIA` | `app/Helpers/functions.php` + env | Indirect (dùng lại, không sửa) | Nếu `URL_SERVER_MEDIA` cấu hình sai → ảnh bot upload từ LME vẫn không tải được |
| F4 | Render avatar người gửi ở view / JS | `content_chat.blade.php`, `chat-v2.js` | Indirect (không sửa) | Nhận `bot_send.bot_image` từ F1/F2 rồi gắn thẳng vào `img`. Fix ở tầng controller nên view không đổi |
| F5 | *(NGOÀI SCOPE — Dev khai chưa sửa)* 2 chỗ hiển thị cho **app điện thoại** | `Api\ChatController` (suy đoán, Dev không nêu rõ file) | Chưa sửa | Dev ghi "khác phạm vi". **Leader chốt có test không** |
| F6 | *(NGOÀI SCOPE — Dev khai chưa sửa)* nội dung **trích dẫn (quoted)** lưu lúc gửi | `<chưa rõ file — Dev không nêu>` | Chưa sửa | Dev ghi "khác phạm vi" |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục "■ 4.2 Data ảnh hưởng" -->

**Nguyên văn Dev**: *"Không có — chỉ đổi cách dựng dữ liệu trả về cho giao diện, không ghi DB"*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | **KHÔNG có thao tác ghi DB** | Fix chỉ đổi cách **đọc / dựng** response, không CREATE/UPDATE/DELETE/MIGRATE |

**Data ĐỌC (không ghi) — suy từ mục 1 + mục 3, Dev không liệt kê:**

| # | Data đọc | Vai trò |
|---|---|---|
| R1 | `bots.bot_image` | Ảnh đại diện hiện tại của bot — **nguồn mới** cho hồ sơ mặc định. Có 2 dạng: đường dẫn tương đối (upload từ LME) **hoặc** full URL (lấy từ LINE) |
| R2 | `bots_profiles.avt_path` | Ảnh snapshot cũ — **nguồn cũ**, nay chỉ còn dùng cho hồ sơ **nhân viên** (không mặc định) |
| R3 | `bots_profiles.nick_name` / `view_name` | Tên hiển thị người gửi — cùng quy ước với avatar |
| R4 | env `URL_SERVER_MEDIA` | Prefix chuẩn hoá URL ảnh tương đối |

> ⚠️ **Data lệch KHÔNG được fix**: `Admin\SettingBotController::update` chỉ ghi `bots.bot_image`, **không đồng bộ** `bots_profiles.avt_path` → dữ liệu lệch vẫn tồn tại trong DB; fix này chỉ **né** nó khi render, không dọn nó. Mục 5 khẳng định không cần recover data.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục "■ 4.3 Tính năng liên quan" -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **1-on-1 Chat (FA-001)** — hover vào tin đã gửi bằng hồ sơ bot gốc hiện đúng avatar hiện tại của bot, kể cả tin cũ | F1, F2, R1 | *(Dev KHÔNG ghi mức)* — Leader chốt |
| T2 | **Chat Settings (outside glossary)** — hồ sơ người gửi (`bots_profiles`) mặc định vẫn giữ quy ước "hồ sơ mặc định = danh tính bot hiện tại" | F1, F2, R1, R2 | *(Dev KHÔNG ghi mức)* — Leader chốt |

> Nguyên văn 2 dòng trên là **toàn bộ** mục 4.3 của Dev. Dev **không ghi cột nguy cơ regression** — cần Leader/tester bổ sung.

---

## 5. Recover data

**Nguyên văn Dev**: ✔ Không cần recover data

## 6. Verify (nguyên văn Dev)

| Trường | Nội dung |
|---|---|
| Mức | **lint** (không chạy runtime) |
| Lệnh | `php -l app/Http/Controllers/ChatController.php`: No syntax errors detected; `git diff --stat origin/release_step_20260805...ai_fixbug_39751`: chỉ 1 file `ChatController.php` (+18/-2) |
| Bằng chứng | Quy ước hồ sơ mặc định lấy ảnh bot đã có sẵn ở `ajaxGetProfileOfBots` (`ChatController.php:1071/1079/1100`), `saveSelectedProfileBot` (`:1147`) và `Api\ChatController::getProfileOfBots` (`:3756/3766`) — 2 chỗ dựng tin đã gửi là ngoại lệ duy nhất; `Admin\SettingBotController::update` (`:246`) chỉ ghi `bots.bot_image` (đường dẫn tương đối), không đồng bộ `bots_profiles.avt_path` → sinh lệch dữ liệu; Giao diện `resources/views/basic/chat/content_chat.blade.php` gắn thẳng `item.bot_send.bot_image` vào thẻ `img` (không qua `getUrlDomain` như modal hồ sơ) → đường dẫn tương đối sẽ 404 rồi rơi về `/images/avatar_bot_v2.png` |
| ⚠️ Chưa kiểm chứng | **CHƯA kiểm chứng thực nghiệm**: dev stack MySQL `host.docker.internal:3306` từ chối kết nối (Connection refused) nên **không chạy được truy vấn / tái hiện thật**; kết luận dựa trên **đọc code** |

## 7. Tự review của AI + rủi ro khi test (nguyên văn)

Fix tối giản 1 file, 2 điểm dựng dữ liệu người gửi của chat 1:1 web, đi theo đúng quy ước đã có sẵn trong code (hồ sơ mặc định lấy ảnh bot hiện tại) nên không phát sinh khái niệm mới. Hồ sơ nhân viên (không phải mặc định) giữ nguyên hành vi cũ.

> ⚠️ **Cảnh báo XUNG ĐỘT MERGE (Dev tự nêu)**: ticket **#39612** (branch `ai_fixbug_33137`, **chưa lên release**) từng chạm **đúng 2 dòng này** với cách sửa tương tự — khi merge có thể trùng, human cân nhắc gộp hay bỏ 1 bên.

**Rủi ro / lưu ý khi test (nguyên văn Dev):**

1. **Bot chưa đặt ảnh đại diện**: hồ sơ mặc định sẽ hiện ảnh placeholder thay vì ảnh chụp cũ — đúng ý nghĩa "hồ sơ mặc định = danh tính bot hiện tại" nhưng là **thay đổi nhìn thấy được**.
2. **Phụ thuộc biến môi trường `URL_SERVER_MEDIA`** của web; nếu cấu hình sai thì ảnh bot upload từ LME vẫn không tải được (ảnh lấy từ LINE là URL đầy đủ nên không bị ảnh hưởng).
3. **Chưa chạy thử runtime** (dev DB tắt) — cần QA xác nhận trên môi trường có dữ liệu thật.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — **Dev chỉ ghi 1 dòng file, bảng F1–F6 do `/new-task` tách ra, BẮT BUỘC verify**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — **Dev ghi "không có", bảng R1–R4 (data đọc) do `/new-task` tách ra**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — **Dev không ghi mức nguy cơ regression**
- [ ] **Chốt scope app điện thoại + quoted message** (Dev khai 3 chỗ cùng kiểu chưa sửa, nhưng Pre-Conditions bug có nhắc app)
- [ ] **Chốt cách xử lý xung đột với #39612** (cùng chạm 2 dòng, chưa lên release)
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
