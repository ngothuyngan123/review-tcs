# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio |
| Commit / Pull Request | commit `1f9478b246d1849b15fa556b573d21fc288e9d0e` |
| Branch | `ai_studio_fixbug_44625` (nhánh gốc `release_step_20260930_v2` @303a131b9c03) |
| Ngày submit đánh giá | 2026-10-28 |
| Auto-filled | 2026-10-29 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Hàm `showMessageText` (chat 1:1 PC) và các bản sao dựng thẻ `<a ... href=` + URL + `>` mà **không bọc nháy kép**, và lại **tìm URL sau khi đã escape**. Nhánh regex cho link `line.me/R/ti/p/%40…` chỉ dừng ở dấu cách thường hoặc xuống dòng, nên khi gặp **tab / CR / FF / NBSP** nó khớp luôn phần phía sau. Trình duyệt tách phần `href` không nháy thành attribute mới (`style`, `onanimationstart`…) rồi chạy JS qua `v-html`.

Hai bản sao `displayMessageFromDataMB` (chat 1:1 mobile) và `displayMessageFromData` (chat nhóm, chi tiết tin lỗi) **còn không escape gì cả**, nên chỉ cần gửi `<img onerror>` là JS chạy.

## 2. Cách fix

Thêm một hàm dùng chung **`linkifyMessageText()`** trong `common.js`. Hàm tìm URL trên **chuỗi gốc**, escape riêng từng đoạn, và `href` **luôn được bọc nháy kép**. Hàm vẫn chỉ escape `< > "` giống quy tắc ở #40574, nên các entity cũ như `&nbsp;` vẫn hiển thị đúng. Link có `&` trong query và link rút gọn (短縮) vẫn hiển thị như trước. 6 chỗ copy code lỗi (`BUG`) nay đều gọi hàm mới (D-1 → D-6).

> Dev đã fuzz 20.000 chuỗi trên Chromium. Giữ nguyên regex nhận link và quy tắc escape đang dùng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `linkifyMessageText` — `public/js/common.js` | **MỚI** — hàm dùng chung tạo link an toàn | Root cause fix (D-1) |
| 2 | `showMessageText`, `showPreviewMessageText` — `public/js/chats/chat-v2.js` | Gọi `linkifyMessageText` | Chat 1:1 PC + popup preview (D-2) |
| 3 | `showMessageText` — `public/js/talk_list/index.js` | Gọi `linkifyMessageText` | Talk list / modal chi tiết (D-3) |
| 4 | `showMessageText` — `public/js/error_list/index_v2.js` | Gọi `linkifyMessageText` | Danh sách tin lỗi v2 (D-4) |
| 5 | `displayMessageFromData` (nhánh text) — `public/js/common.js` | Gọi `linkifyMessageText` + escape `< > "` | Chi tiết tin lỗi + màn chat nhóm cũ `/basic/chat/group` (trắng trang từ 2022, bug #4822) — trước KHÔNG escape (D-5). Hội thoại nhóm thật nằm ở `/chat-v3` 「グループ」 → đi qua `showMessageText` (journal #149212) |
| 6 | `displayMessageFromDataMB` (nhánh text) — `public/js/mobile/chat.js` | Gọi `linkifyMessageText` + escape `< > "` | Chat 1:1 mobile — trước KHÔNG escape; link vẫn mở cùng tab (D-6) |

> Caller cần lưu ý ngoài 6 điểm trên: `common.js` nạp ở **mọi trang dùng layout basic/admin** → nguy cơ regression cache giữa `common.js` và các file JS trang. Màn chat cũ `public/js/chats/chat.js` (route `/chat-v2` đã tắt) **chưa** được vá — Dev đề nghị ticket riêng.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `linkifyMessageText` (mới) | `common.js` | Direct | Hàm chung tạo link an toàn |
| F2 | `showMessageText` + `showPreviewMessageText` | `chat-v2.js` | Direct | Chat 1:1 PC `/chat-v3`: tin thường, trích dẫn, salon/lesson, template trích dẫn, popup preview, **hội thoại nhóm (bộ lọc 「グループ」)** — journal #149212 |
| F3 | `showMessageText` | `talk_list/index.js` | Direct | Talk list `/talk-list` + modal chi tiết |
| F4 | `showMessageText` | `error_list/index_v2.js` | Direct | Danh sách tin lỗi v2 `/error-list-v2` (tin `msg_kind 20`) |
| F5 | `displayMessageFromData` (nhánh text) | `common.js` | Direct | Chi tiết tin lỗi `/basic/error-list-setting/{id}` + màn chat nhóm cũ `/basic/chat/group` (đã trắng trang từ 2022) — trước KHÔNG escape |
| F6 | `displayMessageFromDataMB` (nhánh text) | `mobile/chat.js` | Direct | Chat 1:1 mobile `/chat-mobile/{id}` — trước KHÔNG escape; link mở cùng tab |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — (không có) | — | **Không đổi PHP, API hay DB**. Không migration (đã kiểm diff). Không cần recover: tin trong DB là dữ liệu gốc, lỗi chỉ ở khâu render. Tin cũ có HTML giờ hiện **thành chữ**. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 PC `/chat-v3` — hiển thị tin text / link (tin thường, trích dẫn, salon/lesson, template trích dẫn, popup preview) | F1, F2 | Medium |
| T2 | Talk list `/talk-list` + modal chi tiết | F1, F3 | Medium |
| T3 | Danh sách tin lỗi v2 `/error-list-v2` | F1, F4 | Medium |
| T4 | Chat nhóm (`/chat-v3` lọc 「グループ」) + chi tiết tin lỗi `/basic/error-list-setting/{id}` | F1, F2 (nhóm trên `/chat-v3`), F5 (chi tiết tin lỗi) | Medium (chi tiết tin lỗi trước KHÔNG escape → thay đổi hành vi với tin cũ có HTML) |
| T5 | Chat 1:1 mobile `/chat-mobile/{id}` | F1, F6 | Medium (trước KHÔNG escape; link mở cùng tab) |
| T6 | Mọi trang dùng layout basic/admin nạp `common.js` | F1 | Low (chỉ thêm hàm, rủi ro cache asset nếu không bump version) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
