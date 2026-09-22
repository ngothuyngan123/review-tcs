# 03 — Đánh giá ảnh hưởng từ Dev

> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — journal #135432. Assignee Redmine: Ngô Thúy Ngần (QA nhận test) |
| Commit / Pull Request | repo `sns-line`, commit `d64c20a1d9` (1 file) — không có link PR. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=40539 |
| Branch | `ai_fixbug_40539` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | `2026-09-09` (journal #135432; custom field Commit Date = 2026-09-09) |
| Auto-filled | `2026-09-11 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khung hội thoại của màn Chat 1:1 bắt TẤT CẢ sự kiện kéo-thả (drag/dragstart/dragover/drop...) rồi bật ngay màn hình upload, không kiểm tra thứ đang kéo là tệp hay chỉ là văn bản. Vì vậy chỉ cần bôi đen rồi kéo chữ trong ô soạn tin hoặc trong nội dung tin nhắn là màn hình upload phủ kín màn hình, đồng thời thao tác kéo-thả chữ bị chặn.

> Bằng chứng Dev nêu ở mục 6 VERIFY: `public/js/chats/chat-v2.js` dòng 893 (bản cũ) — handler `.content-chat` set `openUploadFileModal = true` cho MỌI sự kiện `drag/dragstart/dragover/drop`, không kiểm tra `dataTransfer`. Ô soạn tin (`send_message_content.blade.php`) nằm trong `#contentChat.content-chat` nên thao tác kéo chữ trong ô soạn tin cũng lọt vào handler này.

## 2. Cách fix

Thêm hàm kiểm tra `isDragFileEvent` trong `public/js/chats/chat-v2.js`: chỉ bật màn hình upload của Chat 1:1 khi dữ liệu đang kéo thực sự là tệp (`dataTransfer` khai báo kiểu `Files` / `application/x-moz-file`, dự phòng đọc `dataTransfer.files`). Kéo-thả văn bản trong khung chat được trả về hành vi mặc định của trình duyệt, không còn bật màn hình upload và không bị chặn thao tác.

**Quét ngang (Dev tự kê)**: chỉ màn Chat 1:1 có kiểu bắt mọi sự kiện kéo-thả trên cả khung màn hình, các vùng thả tệp khác là vùng chuyên dụng nhỏ nên không dính triệu chứng này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục 3 của Dev, convert sang bảng. Cột "Thay đổi" suy từ mục 2 + mục 6 VERIFY của Dev, KHÔNG phải Dev tự ghi từng dòng. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `mounted` — handler kéo-thả trên `.content-chat` (`public/js/chats/chat-v2.js`) | **CÓ sửa** — thêm điều kiện chỉ mở màn upload khi kéo tệp | Chính là handler gây bug |
| 2 | `isDragFileEvent` (`public/js/chats/chat-v2.js`) | **MỚI thêm** — kiểm tra sự kiện kéo có mang tệp | Hàm nhận diện tệp vs văn bản |
| 3 | `mounted` — handler kéo-thả trên `.upload-file-modal` (`public/js/chats/chat-v2.js`) | Không đổi (Dev ghi luồng thả tệp giữ nguyên) | Nơi nhận cú thả tệp thật |
| 4 | `getFileUpload` (`public/js/chats/chat-v2.js`) | Không đổi | Hàm nhận tệp dùng chung với nút 「メディア送信」 |
| 5 | `handleFileUpload` / `openUploadFileMedia` (`public/js/chats/chat-v2.js`) | Không đổi | Luồng đính kèm / mở màn upload |
| 6 | modal upload (`resources/views/basic/chat/modal/upload_file.blade.php`) | Không đổi (không sửa file PHP) | View lớp phủ upload |
| 7 | khung hội thoại + ô soạn tin (`resources/views/basic/chat/content_chat.blade.php`, `send_message_content.blade.php`) | Không đổi (không sửa file PHP) | Vùng DOM chịu handler kéo-thả |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- ⚠️ Dev ghi ở mục 4.1 CHỈ là "File thay đổi: public/js/chats/chat-v2.js" — KHÔNG kê function theo dạng F1/F2. Bảng dưới đây tag lại F* từ mục 3 (nguyên văn Dev) để /review-tc map coverage. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `mounted` — handler kéo-thả trên `.content-chat` | `public/js/chats/chat-v2.js` | Direct | Handler bị thêm điều kiện — điểm sửa duy nhất |
| F2 | `isDragFileEvent` (hàm mới) | `public/js/chats/chat-v2.js` | Direct | Nhận diện tệp qua `dataTransfer.types` (`Files` / `application/x-moz-file`), fallback `dataTransfer.files` |
| F3 | `mounted` — handler kéo-thả trên `.upload-file-modal` | `public/js/chats/chat-v2.js` | Indirect | Nhận cú thả tệp; Dev ghi giữ nguyên |
| F4 | `getFileUpload` | `public/js/chats/chat-v2.js` | Indirect | Dùng chung với luồng chọn tệp bằng nút 「メディア送信」 |
| F5 | `handleFileUpload` / `openUploadFileMedia` | `public/js/chats/chat-v2.js` | Indirect | Luồng đính kèm + mở lớp phủ upload |

**File thay đổi (nguyên văn 4.1 của Dev)**: `public/js/chats/chat-v2.js`

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** (nguyên văn 4.2 của Dev) | — | Fix thuần front-end JS, không đụng DB, không bump version cấu hình |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | 1-on-1 Chat (FA-001) | F1, F2 | Dev **không ghi mức** — nguyên văn: "kéo-thả văn bản trong khung chat không còn bật màn hình upload; kéo-thả tệp ảnh/video/âm thanh để đính kèm vẫn giữ nguyên" |

---

## BUG — Root cause / cách fix (tag cho coverage)

| Tag | Nội dung |
|---|---|
| `BUG` | Handler kéo-thả `.content-chat` bật lớp phủ upload vô điều kiện → fix bằng điều kiện `isDragFileEvent` (chỉ mở khi `dataTransfer` mang tệp) |

---

## Mục 5 / 6 + tự review của Dev (nguyên văn — input cho BƯỚC 2 khi review)

**5. RECOVER DATA**: ✔ Không cần recover data

**6. VERIFY**
- Mức: `lint`
- Lệnh: `node --check public/js/chats/chat-v2.js`: OK (không lỗi cú pháp); Không sửa file PHP nên không cần `php -l`; không có logic service/helper nên không viết PHPUnit; Đối chiếu code: chỉ nhánh mở màn upload bị thêm điều kiện, luồng thả tệp (`.upload-file-modal` drop → `getFileUpload`) giữ nguyên.
- ⚠️ **Không tái hiện được bằng script trên container** (bug thuần thao tác chuột trên trình duyệt), xác định qua đọc code.

**TỰ REVIEW (AI)**: Sửa tối giản đúng 1 handler. Luồng đính kèm tệp (kéo tệp vào khung chat, nút chọn tệp, giới hạn 5 tệp, validate loại/dung lượng) không đổi. Không sửa PHP, không đụng DB, không bump version cấu hình.

**Rủi ro / lưu ý khi test (Dev tự nêu)**:
1. Với các thao tác kéo-thả không phải tệp, khung chat không còn gọi `preventDefault` nên trình duyệt xử lý mặc định (thả chữ vào ô nhập là chèn chữ; thả một liên kết kéo từ nơi khác vào vùng không nhập liệu có thể khiến trình duyệt điều hướng theo liên kết — đây là hành vi mặc định giống mọi màn khác của hệ thống).
2. Trình duyệt quá cũ không cung cấp `dataTransfer.types` thì rơi về kiểm tra `dataTransfer.files` (chỉ có lúc thả) — trường hợp này màn upload không bật lúc rê chuột, cần thả tệp; các trình duyệt hiện hành đều có `types`.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
