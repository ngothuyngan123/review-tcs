# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40539 — [31-08-2026] [OEM] [Chat 1:1] Kéo & thả văn bản trong chat 1:1 (1:1チャット) bị hiện màn hình upload` |
| Module / Màn hình | Chat 1:1 (1:1チャット) — khung hội thoại + ô soạn tin, thao tác kéo & thả (drag & drop) |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (質問要望)
担当: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BBQN3GTLP/p1788170774902809

Phụ trách　　　　：沖原
Danh mục　　：修正要望 (yêu cầu sửa)
Nội dung
Khi kéo & thả (drag & drop) văn bản trong chat 1:1 (1:1チャット) thì màn hình upload lại hiện lên.
https://www.loom.com/share/ba6b489becbb4927a8d94d0caa306c83

## Steps to reproduce

<!-- Nguồn: Journal #135806 — Nguyen Ha Vi — 2026-09-11 -->

1. Chọn một đoạn văn bản từ bên ngoài hoặc trong chat.
2. Kéo & thả (Drag & Drop) đoạn văn bản vào detail chat 1:1.
3. Kiểm tra màn hình hiển thị.

## Expected result

<!-- Redmine KHÔNG ghi expected tường minh. Không tự suy diễn — tra lại ticket / hỏi Leader nếu cần chốt kỳ vọng. -->

-

## Actual result

- Khi kéo & thả văn bản vào chat 1:1, hệ thống hiển thị màn hình upload file.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [x] Có video
- [ ] Có log / request-response

<!-- Redmine attachments: 0 (không có file đính kèm). Link video nằm trong description, KHÔNG phải attachment Redmine. -->

- Video Loom (từ description): https://www.loom.com/share/ba6b489becbb4927a8d94d0caa306c83

## Ghi chú thêm của Leader

- ⚠️ **Bug thuần thao tác chuột trên trình duyệt** — Dev ghi rõ "Không tái hiện được bằng script trên container", root cause xác định qua đọc code. TC verify fix bắt buộc kéo-thả thật bằng chuột trên trình duyệt thật, không dựng sự kiện bằng script.
- **Môi trường phát hiện**: Redmine KHÔNG ghi rõ env (dev / staging / production). Cần xác nhận với OEM nếu TC cần chốt env.
- **Trình duyệt là trục rủi ro chính**: cách nhận diện tệp dựa vào `dataTransfer.types` — dòng Chromium báo `Files`, Firefox báo `application/x-moz-file`. Dev tự nêu đây là rủi ro cần test (xem file 03 mục "Rủi ro / lưu ý khi test").
- **Hành vi mặc định trình duyệt sau fix**: với thao tác kéo không phải tệp, khung chat không còn gọi `preventDefault` → thả một liên kết kéo từ nơi khác vào vùng không nhập liệu có thể khiến trình duyệt điều hướng theo liên kết. Dev coi đây là hành vi mặc định giống mọi màn khác, không phải bug.
- Ticket ở trạng thái **Fix done - Đợi test**, Commit Date `2026-09-09`.

## Journal / note từ Redmine (nguyên văn)

**Journal #135432 — AI LME Fix bug — 2026-09-09:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khung hội thoại của màn Chat 1:1 bắt TẤT CẢ sự kiện kéo-thả (drag/dragstart/dragover/drop...) rồi bật ngay màn hình upload, không kiểm tra thứ đang kéo là tệp hay chỉ là văn bản. Vì vậy chỉ cần bôi đen rồi kéo chữ trong ô soạn tin hoặc trong nội dung tin nhắn là màn hình upload phủ kín màn hình, đồng thời thao tác kéo-thả chữ bị chặn.

■ 2. CÁCH FIX
Thêm hàm kiểm tra isDragFileEvent trong public/js/chats/chat-v2.js: chỉ bật màn hình upload của Chat 1:1 khi dữ liệu đang kéo thực sự là tệp (dataTransfer khai báo kiểu Files / application/x-moz-file, dự phòng đọc dataTransfer.files). Kéo-thả văn bản trong khung chat được trả về hành vi mặc định của trình duyệt, không còn bật màn hình upload và không bị chặn thao tác. Quét ngang: chỉ màn Chat 1:1 có kiểu bắt mọi sự kiện kéo-thả trên cả khung màn hình, các vùng thả tệp khác là vùng chuyên dụng nhỏ nên không dính triệu chứng này.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
mounted - handler kéo-thả trên .content-chat (public/js/chats/chat-v2.js)
isDragFileEvent - hàm mới kiểm tra sự kiện kéo có mang tệp (public/js/chats/chat-v2.js)
mounted - handler kéo-thả trên .upload-file-modal (public/js/chats/chat-v2.js)
getFileUpload (public/js/chats/chat-v2.js)
handleFileUpload / openUploadFileMedia (public/js/chats/chat-v2.js)
modal upload (resources/views/basic/chat/modal/upload_file.blade.php)
khung hội thoại + ô soạn tin (resources/views/basic/chat/content_chat.blade.php, send_message_content.blade.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - public/js/chats/chat-v2.js
 • 4.2 Data ảnh hưởng:
   - Không có
 • 4.3 Tính năng liên quan:
   - 1-on-1 Chat (FA-001) — kéo-thả văn bản trong khung chat không còn bật màn hình upload; kéo-thả tệp ảnh/video/âm thanh để đính kèm vẫn giữ nguyên

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: node --check public/js/chats/chat-v2.js: OK (không lỗi cú pháp); Không sửa file PHP nên không cần php -l; không có logic service/helper nên không viết PHPUnit; Đối chiếu code: chỉ nhánh mở màn upload bị thêm điều kiện, luồng thả tệp (.upload-file-modal drop -> getFileUpload) giữ nguyên
   Bằng chứng: public/js/chats/chat-v2.js dòng 893 (bản cũ): handler .content-chat set openUploadFileModal = true cho MỌI sự kiện drag/dragstart/dragover/drop, không kiểm tra dataTransfer; Ô soạn tin (send_message_content.blade.php) nằm trong #contentChat.content-chat nên thao tác kéo chữ trong ô soạn tin cũng lọt vào handler này; Không tái hiện được bằng script trên container (bug thuần thao tác chuột trên trình duyệt), xác định qua đọc code

■ TỰ REVIEW (AI)
Sửa tối giản đúng 1 handler: thêm điều kiện chỉ mở màn hình upload khi kéo tệp. Luồng đính kèm tệp (kéo tệp vào khung chat, nút chọn tệp, giới hạn 5 tệp, validate loại/dung lượng) không đổi. Không sửa PHP, không đụng DB, không bump version cấu hình.
 • Rủi ro / lưu ý khi test:
   - Với các thao tác kéo-thả không phải tệp, khung chat không còn gọi preventDefault nên trình duyệt xử lý mặc định (thả chữ vào ô nhập là chèn chữ; thả một liên kết kéo từ nơi khác vào vùng không nhập liệu có thể khiến trình duyệt điều hướng theo liên kết - đây là hành vi mặc định giống mọi màn khác của hệ thống)
   - Trình duyệt quá cũ không cung cấp dataTransfer.types thì rơi về kiểm tra dataTransfer.files (chỉ có lúc thả) - trường hợp này màn upload không bật lúc rê chuột, cần thả tệp; các trình duyệt hiện hành đều có types

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_40539 (nhánh gốc release_step_20260827, commit d64c20a1d9, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 4 phút 31 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=90594bc4-6979-43ed-b6cb-05cf65564173
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=40539
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #135806 — Nguyen  Ha Vi — 2026-09-11:**

```
Tái hiện bug: 
- B1: Chọn một đoạn văn bản từ bên ngoài hoặc trong chat.
- B2: Kéo & thả (Drag & Drop) đoạn văn bản vào detail chat 11.
- B3: Kiểm tra màn hình hiển thị.

BUG: Khi kéo & thả văn bản vào chat 1:1, hệ thống hiển thị màn hình upload file.
```
