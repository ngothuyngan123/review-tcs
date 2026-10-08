# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41887 — [02-10-2026][T12299][Chat 1:1] Chỉ trong 1 nhóm LINE, gửi tin từ Chat 1:1 bị trễ ~10s, gửi trùng 3–4 lần hoặc hiện biểu tượng 🚫 không gửi được.` |
| Module / Màn hình | `Chat 1:1 (1:1チャット)` |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ TẠO TASK ĐIỀU TRA NỘI BỘ (chưa có ticket Slack)

User: y-kunimoto@circus-group.jp
Bot Name: 転職エージェントナビ by circus

Chỉ riêng nhóm LINE「転職エージェントナビ面談チーム」là đang phát sinh sự cố khi gửi tin nhắn.

Cụ thể:
・Tin nhắn gửi được nhưng bị trễ khoảng 10 giây mới gửi đi.
・Tin nhắn gửi được nhưng ngoài việc bị trễ, cùng một tin còn bị gửi liên tiếp 3～4 lần.
・Khi bấm nút gửi tin nhắn (biểu tượng máy bay giấy) thì hiện biểu tượng 🚫 và không thể gửi tin nhắn.

Chức năng: Chat 1:1 (1:1チャット)
Thời điểm phản hồi: 2026/10/02 11:40:15
Ảnh 1: data/screenshots/T12299_0.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12299
Nguồn: Tayori — task #12299 (不具合に関するお問い合わせフォーム)
Link Tayori: https://tayori.com/admin/task/c4906b6ddc824f6bef78fee9a892a6cee4fe0dbd/

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.melonglobal.net/attachments/download/31309/screenshot1.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

- Bug ban đầu được report qua Tayori (CS form, task #12299) — chỉ xảy ra ở **1 nhóm LINE cụ thể** (「転職エージェントナビ面談チーム」), không rõ có lan sang nhóm/bạn bè khác không (ticket không đề cập case đối chứng).
- Bot liên quan: `転職エージェントナビ by circus`. Không có `bot_id` số cụ thể trong ticket.
- User/KH liên hệ: `y-kunimoto@circus-group.jp`.
- Journal #139747 (2026-10-02): OEM đã xác nhận Bug KH (đổi tracker từ "Bug KH cần xử lý nội bộ" → "Bug KH") và push lên Slack — link item/thread Slack xem mục Journal bên dưới.
- Ticket #41887 có `parent: #41821` — có thể liên quan 1 task mẹ, nên kiểm tra thêm context ở #41821 nếu cần.
- Dev impact (file 03) xác định nguyên nhân là lớp chặn "gửi trùng nội dung trong 60 giây" thêm ở **#41605** — cách fix là gỡ bỏ lớp chặn này. Cách fix cũng tham chiếu các ticket liên quan khác: **#41224** (thông báo "chưa chắc đã gửi"), **#39171** (màn Chat nặng khi xem lịch sử dài, đã sửa nhưng chưa push — ngoài phạm vi #41887).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — ticket chỉ ghi Bot Name>` |
| Bot Name | `転職エージェントナビ by circus` |
| Friend / line_user_id | `<chưa rõ>` — lỗi xảy ra trong nhóm LINE `転職エージェントナビ面談チーム` (group chat, không phải 1:1 với friend cụ thể) |
| Đối tượng cấu hình | N/A |
| Thời điểm lỗi | `<chưa rõ>` — Thời điểm KH phản hồi/báo: `2026/10/02 11:40:15` |
| Đối chứng | Không có — ticket không đề cập case nhóm/bạn khác chạy đúng để so sánh |

## Journal / note từ Redmine (nguyên văn)

**Journal #139747 — AI bug detect Lme — 2026-10-02:**

```
OEM đã push task lên Slack (ユーザー問い合わせ) → xác nhận Bug KH.
Đổi tracker "Bug KH cần xử lý nội bộ" → "Bug KH".
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C692JNCLR
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1790923499231129
```
