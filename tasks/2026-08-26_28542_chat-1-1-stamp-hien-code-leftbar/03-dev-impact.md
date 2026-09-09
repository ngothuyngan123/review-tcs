# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #28542 — journal #132530 của **AI LME Fix bug**, 2026-08-24T03:29:21Z ("★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST").
> Nội dung mục 1/2/3/4 bên dưới là **nguyên văn** từ Redmine, chỉ format lại thành bảng theo template.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | `sns-line` commit `c045b0894f` (3 file) — không có link PR |
| Branch | `ai_fixbug_28542` (nhánh gốc `release_step_20260805`) — **đã push lên origin** |
| Ngày submit đánh giá | `2026-08-24` |
| Auto-filled | `2026-08-26 by /new-task` |
| Phiên xử lý AI | https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=28fc6d8d-33f2-4064-b125-8b942ccac13a |
| Dashboard fixbug | https://dashboard.melonglobal.net/fixbug-lme/?id=28542 |
| Thời gian AI xử lý | 1 phút 51 giây |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Ở màn Chat 1:1, khi bạn bè gửi nhãn dán (stamp), phần cập nhật thời gian thực của danh sách hội thoại bên trái so khớp loại tin bằng CHUỖI ('sticker', 'video'...) trong khi bảng tin nhắn bản mới lưu loại tin bằng SỐ, nên rơi vào nhánh mặc định và gán thẳng nội dung thô (đoạn JSON chứa mã nhãn dán) làm dòng tin cuối. Nhánh dành cho hội thoại không mở cũng lấy nội dung thô từ socket nên bị y hệt. Tải lại trang thì đúng vì lúc đó lấy dòng tin cuối do job ghi sẵn trong hội thoại.

## 2. Cách fix

> Refix vòng 1 theo AI review (2 lỗi bắt buộc).
>
> **(1) Lỗi cập nhật nhầm hội thoại**: đoạn gán dòng tin cuối nằm trong callback bất đồng bộ của `/ajax/get-badge` nhưng lại tính lại vị trí hội thoại bằng biến toàn cục `sk_conversation_id` — biến này đã bị tin nhắn mới của hội thoại khác ghi đè trước khi callback chạy, nên nội dung tin cuối của hội thoại A bị gán sang dòng của hội thoại B. Đã bỏ 3 dòng tính lại vị trí trong callback và dùng luôn chỉ số hội thoại đã tính đồng bộ ngay lúc nhận tin (biến cục bộ của mỗi lần chạy handler), nên mỗi phản hồi luôn cập nhật đúng dòng của chính hội thoại đã gửi yêu cầu.
>
> **(2) Lỗ hổng lộ nội dung tin nhắn**: `/ajax/get-badge` nay trả thêm nội dung tin cuối nhưng truy vấn hội thoại chỉ lọc theo id, không lọc theo bot đang đăng nhập, nên tài khoản bất kỳ có thể dò id để đọc nội dung hội thoại khách hàng của bot khác. Đã thêm điều kiện lọc theo bot của phiên đăng nhập (`bot_id = getBotId()`, lấy từ session nên client không giả mạo được) — đúng cách các chỗ khác trong cùng controller đang làm.
>
> Không sửa gì ngoài 2 điểm này (không đụng cảnh báo warning).

> **Ghi chú của core fix (từ mục TỰ REVIEW)**: đổi so khớp loại tin sang **mã số** theo đúng bảng cấu hình dùng chung (`config/sns-line.php`), và lấy dòng tin cuối **đã chuẩn hoá từ máy chủ** cho hội thoại không mở.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `socket.on('message.to.<bot>')` handler — `public/js/chats/chat-v2.js` | **Đã sửa** | Nơi so khớp loại tin bằng chuỗi → đổi sang mã số; sửa lỗi dùng biến toàn cục `sk_conversation_id` trong callback bất đồng bộ |
| 2 | `ChatController::getBadge` — `app/Http/Controllers/ChatController.php` | **Đã sửa** | Trả thêm `last_message`; thêm filter `bot_id = getBotId()` vá lỗ hổng lộ nội dung |
| 3 | `ChatController::getMessageSocket` — `app/Http/Controllers/ChatController.php` | Chỉ đọc để đối chiếu | `json_decode` content cho tin loại stamp → content là object → Vue in ra dạng JSON |
| 4 | `ConversationService::getFriend` — `app/Services/ConversationService.php` | Chỉ đọc để đối chiếu | Nguồn cột `content` của leftbar khi load trang (đường đi ĐÚNG hiện tại) |
| 5 | `HandlePostbackTask.updateLastMessage` — linect-service | Chỉ đọc để đối chiếu nhãn | Nơi ghi `【スタンプ】` vào `conversation.last_message` trước khi bắn socket |
| 6 | `RedisHelper.notifyNewMessage` / `MessagesV2s.getMaxLengthContent` — linect-service | Chỉ đọc | Đường bắn socket + cắt độ dài nội dung |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Redmine mục 4.1 Dev ghi là **"File thay đổi"** (3 file), không phải list function. Bảng dưới map file → function từ mục 2 + 3; cột `Ghi chú` nêu rõ đâu là nguyên văn Dev, đâu là suy từ mục 2/3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Socket handler `message.to.<bot>` — cập nhật realtime leftbar | `public/js/chats/chat-v2.js` | Direct | File nguyên văn từ 4.1; đổi so khớp type chuỗi → số |
| F2 | Logic cập nhật last message cho hội thoại **đang mở** | `public/js/chats/chat-v2.js` | Direct | Suy từ mục 2 — nhánh render trực tiếp từ socket |
| F3 | Logic cập nhật last message cho hội thoại **KHÔNG mở** (qua callback `/ajax/get-badge`) | `public/js/chats/chat-v2.js` | Direct | Suy từ mục 2 (1) — bỏ 3 dòng tính lại vị trí, dùng chỉ số đồng bộ |
| F4 | `ChatController::getBadge` — API `/ajax/get-badge` | `app/Http/Controllers/ChatController.php` | Direct | Bổ sung trường `last_message` vào response |
| F5 | `ChatController::getBadge` — điều kiện lọc `bot_id = getBotId()` | `app/Http/Controllers/ChatController.php` | Direct | Vá lỗ hổng phân quyền cross-bot |
| F6 | Bảng cấu hình mã loại tin nhắn dùng chung | `config/sns-line.php` | Direct | File nguyên văn từ 4.1 — nguồn mã số để so khớp type |
| F7 | `ChatController::getMessageSocket` | `app/Http/Controllers/ChatController.php` | Indirect | Không sửa; nguồn dữ liệu socket cho F1/F2 |
| F8 | `ConversationService::getFriend` (leftbar khi load trang) | `app/Services/ConversationService.php` | Indirect | Không sửa; đường load-page ĐÚNG — dùng làm baseline so sánh |
| F9 | Static asset version (bump JS) | `public/js/chats/chat-v2.js` | Direct | Dev ghi "cần bump phiên bản tài nguyên tĩnh (đã bump)" |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(không có)* | — | **Nguyên văn Dev 4.2**: "Không có — chỉ đọc `conversation.last_message`, không ghi/không đổi dữ liệu" |
| D2 | `conversations.last_message` | READ-only | Đọc để render leftbar; do linect `HandlePostbackTask.updateLastMessage` ghi |
| D3 | `messages_v2s.type` (`int(11)`) | READ-only | Cột kiểu **số** — chính là nguồn gây lệch so khớp chuỗi |
| D4 | Response payload `/ajax/get-badge` | **Thay đổi cấu trúc** | Thêm trường `last_message` — không phải data DB nhưng là contract API đổi (suy từ mục 4.3 Dev) |

> **RECOVER DATA (nguyên văn Dev mục 5)**: ✔ Không cần recover data

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **1-on-1 Chat (FA-001)** — dòng tin cuối ở danh sách hội thoại hiện đúng nhãn loại tin khi nhận tin thời gian thực (stamp/ảnh/video/âm thanh/vị trí/tệp) | F1, F2, F6, D3 | High — *nguyên văn Dev 4.3* |
| T2 | **Chat / Talk Management (FA-002)** — phản hồi `/ajax/get-badge` bổ sung trường `last_message` dùng cho danh sách hội thoại | F4, D4 | High — *nguyên văn Dev 4.3* |
| T3 | **Phân quyền cross-bot trên `/ajax/get-badge`** (badge số chưa đọc + nội dung tin cuối) | F5 | High — suy từ mục 2 (2); Dev ghi ở "Rủi ro khi test" |
| T4 | **Badge số tin chưa đọc** ở leftbar / menu chat | F4, F5 | Medium — cùng API, thêm filter bot có thể đổi số đếm |
| T5 | **Cache static asset JS** phía trình duyệt | F9 | Medium — Dev ghi phải bump version; không bump → tester test nhầm bản cũ |

---

## 5. Rủi ro / lưu ý khi test (nguyên văn Dev)

- Với hội thoại **không đang mở**, dòng tin cuối cập nhật sau khi gọi `/ajax/get-badge` xong (chậm hơn vài trăm mili giây so với trước) — đổi lại không còn nháy đoạn mã thô.
- Nếu gọi `/ajax/get-badge` **lỗi** thì dòng tin cuối của hội thoại đó **giữ nội dung cũ** tới khi tải lại trang (trước đây hiển thị nội dung thô sai).
- `getBadge` nay **chỉ trả dữ liệu của hội thoại thuộc bot đang đăng nhập**; gọi với hội thoại của bot khác sẽ nhận số chưa đọc = 0 và không có nội dung tin cuối (đúng mong muốn, màn chat luôn thao tác trên bot hiện tại).
- Có sửa file JS nên **cần bump phiên bản tài nguyên tĩnh** (đã bump) để trình duyệt không giữ bản cũ.

## 6. VERIFY của Dev (nguyên văn) — ⚠️ chỉ mức `lint`

- **Mức**: `lint`
- **Lệnh**: `php -l app/Http/Controllers/ChatController.php`: OK; `php -l config/sns-line.php`: OK; `node --check public/js/chats/chat-v2.js`: OK; `git diff --stat origin/release_step_20260805...ai_fixbug_28542`: đúng 3 file đã sửa
- **Bằng chứng**:
  - `messages_v2s.type` là `int(11)` (`share/db/db-structure/tables/messages_v2s.sql`) trong khi JS so khớp chuỗi → luôn rơi nhánh mặc định
  - `getMessageSocket` `json_decode` content cho tin loại stamp → content là object → Vue in ra dạng JSON ở `@{{ friend.content }}` (`resources/views/basic/chat/left_side.blade.php:142`)
  - leftbar khi tải trang lấy `conversation.last_message` (`ConversationService.php:111`) — đã đúng `【スタンプ】` do linect `HandlePostbackTask.updateLastMessage` ghi trước khi bắn socket
  - **Không tái hiện được runtime**: MySQL/web dev `host.docker.internal` không kết nối được (Connection refused)

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm Leader cần chú ý (ghi bởi `/new-task`, KHÔNG phải nguyên văn Dev)

1. **Fix rộng hơn bug gốc** — bug gốc chỉ là hiển thị stamp, nhưng fix đụng thêm (a) đúng-hội-thoại khi concurrent và (b) phân quyền cross-bot ở API. Cả 2 là impact độc lập, phải có TC riêng.
2. **Fix dạng generic theo bảng mã type** — đổi so khớp chuỗi → số áp dụng cho **mọi loại tin**, không riêng stamp. Dev tự liệt kê ở 4.3: stamp / ảnh / video / âm thanh / vị trí / tệp → cần cover nhiều loại + 1 loại type lạ/không có trong `config/sns-line.php` (fallback).
3. **Chưa có runtime verify** — Dev không chạy được app (DB refused). Mọi hành vi runtime đều chưa được kiểm chứng lần nào.
4. **Bug đã tái phát 1 lần** (2025-02 → 2026-08-19 vẫn bug) → cần regression bám sát đường load-page (F8) vs realtime (F1) để chắc cả 2 đường cùng ra `【スタンプ】`.
