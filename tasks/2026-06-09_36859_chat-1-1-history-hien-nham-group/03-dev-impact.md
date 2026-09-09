# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kieu Son Tung` (assigned_to) — báo cáo đánh giá: Thanh Phương |
| Commit / Pull Request | https://bitbucket.org/snstool/sns-line/pull-requests/10351/overview |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-09` |
| Auto-filled | `2026-06-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Có 2 nguyên nhân khiến lịch sử chat 1:1 / tên user của một hội thoại bị hiển thị nhầm sang hội thoại (hoặc nhóm LINE) khác:

- **(a) Race condition khi tải lịch sử chat:** hàm `refresh()` gọi API `/basic/refresh_message` nhưng không kiểm tra hội thoại đang chọn lúc response trả về. Nếu user bấm chuyển sang hội thoại khác trong lúc request cũ chưa về, response cũ về muộn vẫn được ghi vào `items`/`conversation` → hiển thị nhầm lịch sử và tên người dùng của hội thoại trước đó.
- **(b) Sai điều kiện tự chọn hội thoại khi scroll tải thêm bạn bè:** trong `loadFriend()`, điều kiện cũ dùng `!this.current_friend.id`. Trường `id` là id của `BotLineUser`, bị NULL với nhóm LINE / hội thoại không có `BotLineUser`. Khi đang xem một nhóm (`id = null`) rồi scroll danh sách để tải thêm, điều kiện `!this.current_friend.id` thành `true` → bị reset `current_friend` về phần tử đầu danh sách, làm nhảy/hiển thị nhầm sang hội thoại khác.

## 2. Cách fix

- **(a) Trong `refresh()`:** lưu lại `requestedConversationId = this.current_friend.conversation_id` trước khi gọi AJAX; trong callback success, nếu `requestedConversationId != this.current_friend.conversation_id` thì `return` bỏ qua response cũ (cùng pattern guard mà luồng socket message ở đầu file đã áp dụng).
- **(b) Trong `loadFriend()`:** đổi điều kiện từ `!this.current_friend.id` sang `!this.current_friend.conversation_id` — dùng `conversation_id` (luôn có cho mọi hội thoại, kể cả nhóm LINE) để chỉ tự chọn hội thoại đầu list khi thật sự chưa chọn hội thoại nào, không reset khi đang scroll tải thêm.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `refresh()` — public/js/chats/chat-v2.js | Thêm guard chống race condition theo `conversation_id` | Đã rà các nơi gọi: chuyển hội thoại (`getHistory`), sau khi gửi tin, polling và `loadFriend()` (line ~874, ~2537, ~2642). Guard mới bảo vệ tất cả các luồng này, response cũ về muộn đều bị bỏ qua, không ảnh hưởng luồng bình thường. |
| 2 | `loadFriend()` — public/js/chats/chat-v2.js | Đổi điều kiện tự chọn hội thoại đầu list dùng `conversation_id` thay cho `id` | Đã rà các nơi gọi: load lần đầu (line ~810), scroll tải thêm với `isLoadingNewPage=true` (line ~866), tìm kiếm/lọc bạn bè (line ~2715, ~2833, ~2867, ~2898). Thay đổi chỉ tác động nhánh scroll pagination (không còn bị reset về hội thoại đầu); các nhánh lần đầu/tìm kiếm vẫn tự chọn hội thoại đầu như cũ. |
| 3 | (rà soát chung) | Không thay đổi | Đã check, không ảnh hưởng tới các logic khác đọc `current_friend.conversation_id` / `current_friend.id` trong file. |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `refresh()` | public/js/chats/chat-v2.js | Direct | Thêm guard chống race condition theo `conversation_id` (bỏ qua response cũ về muộn) |
| F2 | `loadFriend()` | public/js/chats/chat-v2.js | Direct | Sửa điều kiện tự chọn hội thoại đầu list dùng `conversation_id` thay cho `id` |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Chỉ sửa logic client-side JS, không thay đổi DB / API field. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn hình Chat 1:1 (1:1チャット) — hiển thị lịch sử chat và tên người dùng đúng hội thoại đang chọn | F1, F2 | High |
| T2 | Chuyển nhanh giữa các hội thoại / nhóm LINE trong lúc đang tải lịch sử | F1 | High |
| T3 | Scroll tải thêm danh sách bạn bè (friend list pagination) khi đang xem một nhóm LINE | F2 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
