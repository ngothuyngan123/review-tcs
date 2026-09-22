# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41108 — [18-09-2026][T12182][Chat 1:1] Khung chat 1:1 trên PC bị trắng cho 1 friend cụ thể do lỗi parse JSON khi tên LINE có chứa dấu ngoặc kép.` |
| Module / Màn hình | Chat 1:1 (1:1チャット) — khung chat bản PC, phần hiển thị **quote tin nhắc đặt lịch salon/lesson** (`showMessageQuotedSalonLesson` trong `chat-v2.js`) |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

- User: tuttunn.dream@gmail.com
- Bot Name: つっつん

Chỉ riêng khung chat 1:1 bản PC của 1 user cụ thể bị trắng. Bản smartphone vẫn bình thường.

Console phát sinh lỗi sau đây:

```
SyntaxError: Expected ',' or '}' after property value in JSON
at JSON.parse
at showMessageQuotedSalonLesson (chat-v2.js)
```

User liên quan có tin nhắn xác nhận đặt lịch salon (サロン予約受付時メッセージ) vào khoảng 2026/8/28 17:16, tại thời điểm đó tên hiển thị LINE (LINE表示名) có chứa dấu ngoặc kép nửa full-width `"`.
Vui lòng kiểm tra lại xử lý parse JSON・xử lý escape (エスケープ処理) của tin nhắn liên quan đặt lịch.

- Tên friend: `*つか咲"き*`
- Chức năng: Chat 1:1 (1:1チャット)
- Thời điểm phản hồi: 2026/09/18 15:34:30
- Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12182

Ticket Slack do OEM đăng — 管理番号 TY-12182.

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — xem Ghi chú thêm của Leader. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #41108 không có attachment. Log console được chép nguyên văn trong phần Mô tả bug. -->

## Ghi chú thêm của Leader

- ⚠️ Bug không có section "Tái hiện bug" trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (escape JSON khi replace tên LINE) + regression impact.
- Điều kiện tiên quyết để tái hiện: friend có **tên hiển thị LINE chứa ký tự `"`** (half-width double quote) và có **tin nhắc đặt lịch salon/lesson** (content JSON `RemindBookingContent`), sau đó friend **quote (reply)** tin đó.
- Bug chỉ xuất hiện trên **bản PC** của màn Chat 1:1; bản smartphone hiển thị bình thường → TC cần chạy trên cả 2 giao diện để phân biệt.
- Bug không phải xác suất: phát sinh cố định với record `messages_v2s.quote_message_content` đã bị vỡ JSON.
- ⚠️ Fix **không** sửa dữ liệu cũ (xem 4.2 file 03) → friend đã dính lỗi trước đó vẫn trắng khung chat sau khi deploy. Cần xác nhận với Dev cách xử lý data cũ trước khi test verify trên môi trường có record lỗi.
- Môi trường phát hiện: production (user thật của OEM, qua form 操作方法に関するお問い合わせ).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — Bot Name: つっつん>` |
| Friend | `つか咲"き` — `<line_user_id chưa rõ>` |
| Tài khoản OEM báo lỗi | tuttunn.dream@gmail.com |
| Đối tượng cấu hình | Tin nhắc đặt lịch salon (サロン予約受付時メッセージ) — content JSON `RemindBookingContent` |
| Thời điểm lỗi | Tin đặt lịch: `2026/08/28 17:16` · Phản hồi CS: `2026/09/18 15:34:30` |
| Ticket CS | T12182 / 管理番号 TY-12182 — https://dashboard.melonglobal.net/css-analytics/?id=T12182 |
| Đối chứng | Cùng friend, cùng khung chat trên **bản smartphone** hiển thị bình thường |

## Journal / note từ Redmine (nguyên văn)

**Journal #137146 — Thanh Duy Nguyen — 2026-09-18:**

```
Bug KH #41108 [18-09-2026][T12182][Chat 1:1] Khung chat 1:1 trên PC bị trắng cho 1 friend cụ thể do lỗi parse JSON khi tên LINE có chứa dấu ngoặc kép.

1. Nguyên nhân
	- Khi friend quote tin nhắc đặt lịch salon/lesson (content là JSON RemindBookingContent), HandlePostbackTask.applyReplaceContent thay raw tên LINE (chứa ") vào JSON mà không escape → quote_message_content.content bị vỡ JSON, web lỗi JSON.parse tại showMessageQuotedSalonLesson (chat-v2.js).

2. Cách fix
	- Trong applyReplaceContent: nếu content là JSON thì escape giá trị replace (", \, xuống dòng) bằng Jackson trước khi thay; content text thường giữ nguyên logic cũ.

3. Đã check và sửa các function sử dụng đến function/data vừa sửa
	- applyReplaceContent có 2 caller (checkFindQuoteMessage, buildQuoteMessageContent), signature không đổi → không cần sửa caller, scope local.

4. Đánh giá ảnh hưởng
        4.1 List function
            - HandlePostbackTask.applyReplaceContent
            - HandlePostbackTask.isJsonContent (mới)
        4.2 List những data bị update khi fix bug
            - Không có (chỉ áp dụng cho tin quote mới, record messages_v2s.quote_message_content đã lỗi trước đó không tự sửa)
        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
            - Quote tin nhắc đặt lịch salon/lesson: friend có tên LINE chứa " → reply quote, check chat 1:1 PC hiển thị bình thường
            - Quote tin text bot gửi có {name}/friend info chứa ": check nội dung quote hiển thị đúng như trước
            - Quote tin template (capture) thường / tin friend gửi: check không thay đổi behavior
            - Callback message user / group / inactive user (handleMessage, handleMessageGroup, handleMessageInactiveUser): check lưu message có quote bình thường

5. Commit / Branch
        5.1 Commit hoặc pull request
            - fcee76a
        5.2 Branch hiện tại của task
            - m_202609_replace_json_41108
```
