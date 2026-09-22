# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | `fcee76a` |
| Branch | `m_202609_replace_json_41108` |
| Ngày submit đánh giá | 2026-09-18 (Journal #137146) |
| Auto-filled | `2026-09-19 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi friend quote tin nhắc đặt lịch salon/lesson (content là JSON `RemindBookingContent`), `HandlePostbackTask.applyReplaceContent` thay raw tên LINE (chứa `"`) vào JSON mà không escape → `quote_message_content.content` bị vỡ JSON, web lỗi `JSON.parse` tại `showMessageQuotedSalonLesson` (`chat-v2.js`).

## 2. Cách fix

Trong `applyReplaceContent`: nếu content là JSON thì escape giá trị replace (`"`, `\`, xuống dòng) bằng Jackson trước khi thay; content text thường giữ nguyên logic cũ.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn Dev: `applyReplaceContent` có 2 caller (`checkFindQuoteMessage`, `buildQuoteMessageContent`), signature không đổi → không cần sửa caller, scope local.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandlePostbackTask.checkFindQuoteMessage` | Không sửa | Caller của `applyReplaceContent`, signature không đổi |
| 2 | `HandlePostbackTask.buildQuoteMessageContent` | Không sửa | Caller của `applyReplaceContent`, signature không đổi |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `applyReplaceContent` | `HandlePostbackTask` | Direct | Thêm nhánh escape khi content là JSON |
| F2 | `isJsonContent` (mới) | `HandlePostbackTask` | Direct | Function mới — phân biệt content JSON vs text thường |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | Không có | Nguyên văn Dev: chỉ áp dụng cho **tin quote mới**; record `messages_v2s.quote_message_content` đã lỗi trước đó **không tự sửa** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Quote tin nhắc đặt lịch salon/lesson — friend có tên LINE chứa `"` → reply quote, check chat 1:1 PC hiển thị bình thường | F1, F2 | `<Dev chưa ghi mức độ>` |
| T2 | Quote tin text bot gửi có `{name}` / friend info chứa `"` — check nội dung quote hiển thị đúng như trước | F1 | `<Dev chưa ghi mức độ>` |
| T3 | Quote tin template (capture) thường / tin friend gửi — check không thay đổi behavior | F1 | `<Dev chưa ghi mức độ>` |
| T4 | Callback message user / group / inactive user (`handleMessage`, `handleMessageGroup`, `handleMessageInactiveUser`) — check lưu message có quote bình thường | F1 | `<Dev chưa ghi mức độ>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
