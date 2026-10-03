# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI Auto-fixbug (hệ thống, báo cáo tại Journal #139744); Assignee ticket Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `e1e35fcf99` (không có link PR riêng — chỉ có commit hash + branch nêu trong journal) |
| Branch | `sns-line: ai_fixbug_41888` (nhánh gốc `release_step_20260930`, 1 file thay đổi, đã push) |
| Ngày submit đánh giá | 2026-10-02 |
| Auto-filled | 2026-10-02 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Hội thoại 若林まや bị lệch dữ liệu: cờ chưa xác nhận của hội thoại vẫn bằng 1 (nên còn chấm đỏ ở danh sách và vẫn được đếm vào badge 1:1チャット) nhưng không còn bản ghi tin chưa xác nhận nào, nên tab chưa xác nhận ở màn Quản lý chat trống. Trước đây bấm nút "Đổi thành đã xác nhận" sẽ tự đưa cờ về 0; từ bản phát hành 30/09 (#41634) nút này thêm điều kiện chỉ nhìn bảng tin chưa xác nhận, thấy rỗng là báo lỗi 「未読メッセージがありません。」 (đúng như ảnh 2 của khách) và không reset gì, nên chấm đỏ + badge kẹt vĩnh viễn.

## 2. Cách fix

Sửa điều kiện chặn của nút "Đổi thành đã xác nhận" ở Chat 1:1: chỉ báo lỗi "không có tin chưa đọc" khi hội thoại THẬT SỰ không còn gì chưa xác nhận (không còn bản ghi tin chưa xác nhận VÀ cờ chưa xác nhận của hội thoại = 0); hội thoại còn cờ lệch thì cho chạy tiếp để reset cờ về 0 và tính lại badge. Quét ngang: 2 lối vào cùng kiểu chặn (/basic/rec_message, /basic/update-status-confirm) chỉ còn được màn chat cũ / hàm JS không ai gọi dùng — không sửa, chỉ ghi chú.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Basic\ChatController::confirmMessage` (app/Http/Controllers/Basic/ChatController.php) | Đã sửa | Chỗ fix chính — điều kiện chặn nút "Đổi thành đã xác nhận" |
| 2 | `ConversationService::confirmMessage` / `changeStatusReadMessage` (app/Services/ConversationService.php) | Không sửa code | Reset `confirm_count` + tính lại `bots.count_user_unconfirm` — được gọi lại bình thường khi điều kiện 1 không còn chặn nhầm |
| 3 | `totalUserConfirmMessage` (app/Helpers/functions.php) | Không sửa code | Badge đếm `conversation.confirm_count=1` |
| 4 | `sidebar.blade.php` + `countBadge` | Không sửa code | Badge đọc `bots.count_user_unconfirm` |
| 5 | `BotLineUser::makeDataTalkList` / `getListMessagesV2` (app/BotLineUser.php) | Không sửa code | Tab 未確認のみ đọc `unconfirm_message` |
| 6 | `ChatController::confirm` (/basic/rec_message) + `ChatController::updateStatusConfirm` (app/Http/Controllers/ChatController.php) | Không sửa | Cùng kiểu chặn như #41634 nhưng Dev xác định là lối vào đã chết (màn chat cũ / hàm JS không ai gọi) — chỉ ghi chú, không sửa |
| 7 | `chat-v2.js confirmMessage` | Không sửa code | FE gọi `/basic/confirm-message` |
| 8 | `linect HandlePostbackTask` (job Java) | Không sửa — chỉ đọc | Lưu `UnconfirmMessage` rồi `updateLastMessage` set `confirm_count=1` — 2 bước không nguyên tử, là **nguồn gốc gây lệch dữ liệu** nhưng ngoài phạm vi fix (chỉ sửa PHP) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Basic\ChatController::confirmMessage` | app/Http/Controllers/Basic/ChatController.php | Direct | Sửa điều kiện chặn nút "Đổi thành đã xác nhận" |
| F2 | `ConversationService::confirmMessage` / `changeStatusReadMessage` | app/Services/ConversationService.php | Indirect | Reset `confirm_count` + tính lại badge — không đổi code, chạy lại đúng khi F1 không còn chặn nhầm |
| F3 | `totalUserConfirmMessage` | app/Helpers/functions.php | Indirect | Badge đếm `conversation.confirm_count=1` |
| F4 | `sidebar.blade.php` + `countBadge` | (view) | Indirect | Badge đọc `bots.count_user_unconfirm` |
| F5 | `BotLineUser::makeDataTalkList` / `getListMessagesV2` | app/BotLineUser.php | Indirect | Tab 未確認のみ đọc `unconfirm_message` |
| F6 | `ChatController::confirm` (/basic/rec_message) + `ChatController::updateStatusConfirm` | app/Http/Controllers/ChatController.php | Không sửa (lối vào đã chết, theo Dev) | Cùng kiểu chặn cũ — Leader nên xác nhận lại có thực sự "chết" không (xem cảnh báo §Leader bên dưới) |
| F7 | `chat-v2.js confirmMessage` | (FE) | Indirect | FE gọi `/basic/confirm-message` |
| F8 | `linect HandlePostbackTask` | (job Java, ngoài phạm vi) | Chỉ đọc — không sửa | Nguồn gốc gây lệch dữ liệu (2 bước ghi không nguyên tử), KHÔNG được xử lý trong fix này |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `conversation.confirm_count` / `status_last_message` / `has_status_0` / `has_status_1` | UPDATE | Được reset về đã xác nhận khi bấm nút trên hội thoại đang lệch (trước đây bị chặn nhầm, không reset được) |
| D2 | `bots.count_user_unconfirm` | UPDATE | Tính lại sau khi reset D1 (dùng lại luồng sẵn có, không đổi code) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 (FA-001) — nút 「確認済みに変更」/「未確認に変更」 và chấm đỏ chưa đọc | F1, D1, D2 | High — nút đổi thành đã xác nhận giờ reset được chấm đỏ của hội thoại lệch dữ liệu, badge menu 1:1チャット cập nhật đúng |
| T2 | Chat / Talk Management (FA-002) — tab 「未確認のみ」 Quản lý chat | F3, F4, F5, D2 | Medium — không đổi code nhưng số badge giờ khớp lại với tab chưa xác nhận sau khi khách bấm xác nhận |

### Lưu ý từ Dev (tự review — journal #139744)

- ⚠️ Nguồn gốc lệch dữ liệu (job `linect`, xem F8) **CHƯA xử lý** — vẫn có thể tái phát lệch dữ liệu cho hội thoại khác trong tương lai; fix này chỉ trả lại đường tự chữa (bấm nút để reset) cho user/admin, không chặn gốc.
- ⚠️ Dev **CHƯA verify runtime** (DB dev không truy cập được lúc fix) — chỉ verify mức lint (`php -l`) + `git diff --stat`; không có test tự động cho endpoint này.
- 2 lối vào cũ cùng kiểu chặn (F6: `/basic/rec_message`, `/basic/update-status-confirm`) không được sửa — Dev nhận định "màn chat cũ / hàm JS không ai gọi", nhưng cần Leader xác nhận lại trước khi loại hẳn khỏi phạm vi test (màn chat nhóm `/basic/chat/group` có thể vẫn dùng lối vào cũ — xem ghi chú tương ứng ở `04-tc-list.md` TC `NEW-3`).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
