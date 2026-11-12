# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #42668 bằng `/new-task` lúc 2026-10-14.
>
> ⚠️ Redmine không có heading "Tái hiện bug" / "再現手順" tường minh — mô tả chỉ ghi lại báo cáo khách hàng (qua Slack OEM) + ID log do QA (Ngô Thúy Ngần) tra ra ở Journal #142497. Steps to reproduce/Expected/Actual bên dưới để trống; root cause đã được Dev Studio confirm đầy đủ ở `03-dev-impact.md`.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42668 — [10-10-2026][31767][Auto reply] Khách đặt keyword đúng nhưng tin nhắn tự động trả lời (自動応答) không được gửi, hiện mã lỗi ghi "エルメサポートまで".` |
| Module / Màn hình | `<chưa rõ — Redmine không gán category>`. Suy từ nội dung: màn soạn mẫu tin (テンプレート作成, quick reply クイックリプライ) + job tự động trả lời (自動応答 auto-reply) |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

User: nakamurahiromi.bodysprout+bs@gmail.com
Bot Name: ボディスプラウト【公式』

Đã cài đặt keyword không sai nhưng tin nhắn trả lời tự động không được gửi.

Trong mã lỗi có ghi 「エルメサポートまで」(liên hệ エルメサポート).

Tên friend: Hiromi Nakamura
Chức năng: Trả lời tự động (自動応答)
Thời điểm phản hồi: 2026/10/10 06:10:00

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=31767

Ticket Slack do OEM đăng — 管理番号 31767
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C86T1AT7U
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1791589289752869

## Steps to reproduce

<!-- Không có trong Redmine — xem "Dữ liệu định danh ca lỗi" + Journal #142497 để dựng lại case cụ thể. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #42668 không có attachment (0). Journal #142525 có 1 ảnh do エルメサポート gửi trên Slack (không phải attachment Redmine): https://go.lmes.jp/msg_template/media/images/3/218/1791623071BauHHT.png -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine theo format Steps/Expected/Actual chuẩn — root cause đã được Dev Studio confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (chặn lưu nhãn nút rỗng) + regression trên mọi luồng dùng chung endpoint lưu mẫu tin.

Ticket hiện **Status: Closed** (REST API fetch lúc chạy `/new-task`) — theo RULE-11 là bằng chứng hợp lệ để flag `[BLOCKER]`/`[MAJOR]` nếu TC thiếu coverage. Lưu ý: tab "Thông tin" của MCP LME TEST STUDIO đang cache Redmine status cũ hơn ("Fix done - Đợi test") — ưu tiên status REST API mới nhất (Closed) khi có mâu thuẫn.

Lỗi xảy ra ở **production** (bot khách hàng thật, `bot_id=179050`) — không phải case xác suất: nguyên nhân là 1 mẫu tin quick reply cụ thể bị lưu với nút trống nhãn (ボタンテキスト rỗng) từ trước, auto-reply nào dùng đúng mẫu tin này đều lỗi 100% cho tới khi khách tự sửa nhãn (đã sửa ngày 11/10 trên production).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `179050` |
| Friend | `Hiromi Nakamura — line_id 41286847` |
| Đối tượng cấu hình | Mẫu tin quick reply 「通知設定」— `template_group_id=15908627`, `template_child_id=15908633` |
| Thời điểm lỗi | `2026/10/10 06:10:00` (thời điểm job auto-reply gửi lỗi, `message_id=2273349419`); mẫu tin bị lưu nhãn rỗng trước đó lúc `05:36` và `05:54` cùng ngày qua màn soạn web |
| Đối chứng | `<không có trong Redmine — chưa rõ case chạy đúng để so sánh>` |

## Journal / note từ Redmine (nguyên văn)

**Journal #142497 — Ngô Thúy Ngần — 2026-10-09:**

```
bot_id: 179050
line_id: 41286847
error_message: "messages[0].quickReply.items[0].action -> `label` must be specified"
message_id: 2273349419

Check template: template_group_id=15908627&template_child_id=15908633

Tại sao user lại tạo được template quick mà lại trống tên button?
```

**Journal #142524 — AI bug detect Lme — 2026-10-10:**

```
Comment slack ngày 2026-10-10 18:04:32

鈴木 隆宏（エルメサポート）
Xin chào (cảm ơn anh/chị đã luôn hợp tác).

Chúng tôi đã kiểm tra lỗi gửi tin nhắn tự động trả lời (自動応答) mà quý khách đã hỏi.

Trong template「通知設定」được dùng để gửi tự động trả lời, có nút chưa được thiết lập văn bản nút (ボタンテキスト).

Xin phiền quý khách thiết lập văn bản cho nút.
```
