# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ — đánh giá được pipeline "AI LME Fix bug" post lên Redmine, không có tên Dev cụ thể>` |
| Commit / Pull Request | Commit `f041b42b62` (repo `sns-line`), đã push — không có link PR trong ticket |
| Branch | `ai_fixbug_41887` (repo `sns-line`) |
| Ngày submit đánh giá | 2026-10-02 |
| Auto-filled | 2026-10-03 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (journal #139838) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Lớp chặn "gửi trùng nội dung trong 60 giây" được thêm ở **#41605**: mỗi lần gửi tin text phải tra lịch sử tin nhắn của hội thoại để so sánh nội dung trùng. Nhóm LINE có lịch sử tin nhắn dài (như nhóm 「転職エージェントナビ面談チーム」trong ticket này) thì bước tra lịch sử này bị chậm → gây hiện tượng trễ ~10s khi gửi, và khi nhân viên tưởng chưa gửi mà bấm gửi lại thì sinh tin trùng 3–4 lần hoặc hiện biểu tượng 🚫 không gửi được.

## 2. Cách fix

Gỡ hẳn lớp chặn "gửi trùng nội dung trong 60 giây" (thêm ở #41605). Tính năng **重複送信防止** (chặn khi nhân viên KHÁC vừa gửi cho cùng người bạn) **GIỮ NGUYÊN**, không bị gỡ.

File thay đổi (sns-line, chỉ xoá code):
- `app/Services/ChatService.php`: xoá hàm kiểm tra trùng nội dung + đoạn gọi trong lệnh gửi tin
- `public/js/chats/chat-v2.js`: bỏ nhánh xử lý cờ `duplicate_content` khi gửi tin text
- `public/js/chats/ajax-error.js`: bỏ nhánh `duplicate_content` trong xử lý lỗi nghiệp vụ khi gửi
- `public/js/chats/common.js`: chỉ còn xử lý cờ `prevent_duplicate`

**Thay đổi hành vi:**
- Gửi lại ĐÚNG cùng nội dung vào cùng hội thoại trong 60 giây: trước bị chặn với thông báo 「同じ内容のメッセージが直前に送信済みです…」, nay gửi bình thường (như trước #41605).
- Tin text gửi vào hội thoại có lịch sử dài không còn phải chờ bước tra lịch sử.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev không ghi riêng mục caller-check theo format chuẩn. Nội dung tương đương (phạm vi retest Dev tự đề xuất) được giữ nguyên văn bên dưới để Tester đối chiếu. -->

Dev đề xuất **phạm vi retest** (nguyên văn, dùng thay mục caller-check):

| # | Nội dung retest Dev đề xuất |
|---|---|
| 1 | Chat 1:1 web: gửi tin text tới 1 bạn bè và tới 1 nhóm LINE (ưu tiên nhóm nhiều tin) — tin đi ngay, hiện trong lịch sử, danh sách bên trái cập nhật nội dung mới. |
| 2 | Gửi cùng một nội dung 2 lần liên tiếp — cả 2 đều gửi, không hiện thông báo trùng nội dung. |
| 3 | 重複送信防止 đang bật: nhân viên A gửi xong, nhân viên B gửi cho cùng người bạn trong thời gian khoá — vẫn hiện modal cảnh báo và bị chặn. |
| 4 | Các thông báo lỗi khác khi gửi vẫn đúng: chạm hạn mức gói (modal hạn mức), bạn bè đã chặn, mất mạng. |
| 5 | App Elme: gửi tin text vào hội thoại thường — gửi bình thường. |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Hàm kiểm tra trùng nội dung + đoạn gọi trong lệnh gửi tin | `app/Services/ChatService.php` | Direct | Xoá hẳn (không chỉ disable) |
| F2 | Xử lý cờ `duplicate_content` khi gửi tin text | `public/js/chats/chat-v2.js` | Direct | Bỏ nhánh xử lý |
| F3 | Xử lý `duplicate_content` trong business-error handler khi gửi | `public/js/chats/ajax-error.js` | Direct | Bỏ nhánh xử lý |
| F4 | Xử lý cờ gửi trùng (`prevent_duplicate` / `duplicate_content`) | `public/js/chats/common.js` | Direct | Chỉ còn lại xử lý cờ `prevent_duplicate` (重複送信防止) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | Dev xác nhận: **không ghi / không đổi dữ liệu**, không cần recover data. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 (FA-001) — gửi tin text từ màn Chat 1:1 trên web (`/basic/chat-v3`), cả hội thoại bạn bè 1:1 lẫn nhóm LINE | F1, F2, F3, F4 | High |
| T2 | App Elme (app quản trị di động) — gửi tin text, dùng chung hàm gửi ở server nên cũng mất bước kiểm tra này (Dev không sửa API app riêng) | F1 | Medium |
| T3 | Gửi ảnh / tệp / sticker / mẫu tin (template) | — | Không ảnh hưởng — Dev xác nhận các loại này trước nay vốn không đi qua bước kiểm tra trùng nội dung |

**Rủi ro / lưu ý (nguyên văn từ Dev):**
- Mất lớp chặn: nếu màn báo lỗi nhưng tin thực ra đã đi, nhân viên bấm gửi lại sẽ tạo tin trùng như trước #41605. Thông báo "chưa chắc đã gửi" (#41224) vẫn nhắc kiểm tra lịch sử trước khi gửi lại.
- Chưa đo trên production rằng đây là nguồn chậm duy nhất; nếu nhóm vẫn chậm sau phát hành cần xem log thời gian của bước gửi sang LINE.
- Cùng khách hàng còn một điểm làm màn Chat nặng khi xem lịch sử dài (sắp xếp tin ở trình duyệt, đã sửa ở #39171 nhưng chưa push) — **ngoài phạm vi ticket này**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — *lưu ý: Dev dùng "phạm vi retest" thay cho caller-check chuẩn, cần hỏi lại nếu nghi sót caller*
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
