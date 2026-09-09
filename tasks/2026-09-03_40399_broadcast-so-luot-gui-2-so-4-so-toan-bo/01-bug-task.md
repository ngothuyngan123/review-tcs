# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40399 — [01-09-2026] [TY-12033] [Broadcast] Hiển thị số lượt gửi bất thường (2 số/4 số) khi cài đặt broadcast toàn bộ` |
| Redmine URL | https://redmine.watermelon.vn/issues/40399 |
| Auto-filled | `2026-09-03 by /new-task` |
| Ngày báo cáo | `2026-09-01` |
| Khách hàng / PM báo | `AI bug detect Lme` (author Redmine). Khách thật: アドライフ株式会社 (adlife1001@gmail.com) — 担当 後藤, quản lý số TY-12033 |
| Module / Màn hình | `Broadcast` (Redmine category) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — Redmine không ghi env. Ticket tracker "Bug KH", khách hàng thật đang dùng ⇒ nhiều khả năng **Production**. Tester confirm trước khi viết TC. |

**Thông tin bổ sung từ Redmine** (không có trong template — để Leader trace):

| Trường | Giá trị |
|---|---|
| Status | `Fix done - Đợi test` |
| Tracker | `Bug KH` |
| Assigned to | `Ngô Thúy Ngần` |
| Commit Date (custom field) | `2026-09-03` |
| Parent issue | `#40400` (đổi từ `#39408` lúc 2026-09-01) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description từ Redmine #40399. KHÔNG diễn giải lại. -->

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-12033
担当: 後藤
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1788242033585909?thread_ts=1788242033.585909&cid=C0BALS7S73L
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12033

Số quản lý：TY-12033
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BU04RA6Q6
Địa chỉ email：adlife1001@gmail.com
Tên LOA　　：アドライフ株式会社
Người phụ trách　　 ：後藤
Công cụ　 ：リンク
Nội dung liên hệ
【操作方法に関するお問い合わせフォーム】
Vào cuối tháng 8, hệ thống hiển thị thông báo 「配信数上限が近づいています。料金プランのアップグレードを推奨します。」
Tại thời điểm đó, số lượt gửi khoảng 15,000 trong khi giới hạn của tài khoản LINE chính thức là 30,000.
Khi kiểm tra lại cài đặt gửi, dù cài đặt gửi cho toàn bộ (全員配信) nhưng số hiển thị chỉ có 2 chữ số (ít), còn khi tạo lại bản nháp thì số người toàn bộ lại hiển thị 4 chữ số — có triệu chứng bất thường này.
Hôm nay số liệu đã được reset, nhưng khách lo lắng không biết tháng này có thể gửi broadcast như bình thường được không.
Không biết tình trạng trên là như thế nào? Mong được xác nhận giúp.

---
h3. 原文 (JP)
<pre>管理No　：TY-12033
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BU04RA6Q6
アドレス ：adlife1001@gmail.com
LOA名　　：アドライフ株式会社
担当　　 ：後藤
ツール　 ：リンク
問い合わせ内容
【操作方法に関するお問い合わせフォーム】
8月末に「配信数上限が近づいています。料金プランのアップグレードを推奨します。」と表示が出ました。
この時点での配信数は約15,000でLINE公式アカウントの上限は3万でした。
配信設定を見直すと、全員配信の設定でも表示が2桁で少なく、再度下書き設定すると全員の人数4桁表示になるという症状がみられました。
今日、リセットされましたが、今月もこれまで通りの配信ができるのか不安です。
上記、どのような状況でしょうか？ご確認お願いします。</pre>

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" / 再現手順 → để trống, xem Ghi chú của Leader. -->

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

- https://redmine.watermelon.vn/attachments/download/29816/screenshot1.jpg
- https://redmine.watermelon.vn/attachments/download/29817/1788166413971.jpg (đính kèm bởi 後藤宏司 qua Slack 2026-09-01 14:54)

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

**Triệu chứng khách mô tả (nằm trong phần Mô tả bug, KHÔNG phải section "Tái hiện bug" chuẩn)** — dùng làm gốc để dựng flow reproduce khi viết TC:
- Broadcast cài **gửi toàn bộ (全員配信)** → số người dự kiến ở **danh sách** hiển thị 2 chữ số (nhỏ bất thường).
- **Tạo lại bản nháp** cho cùng nội dung → số người toàn bộ hiển thị 4 chữ số (số thật).

**2 vấn đề tách biệt trong 1 ticket** (Dev đã kết luận ở journal 2026-09-03):
1. Số người dự kiến sai ở danh sách broadcast gửi toàn bộ → **đây là bug, đã fix**.
2. Cảnh báo 「配信数上限が近づいています」 khi 15.000/30.000 → **KHÔNG phải bug**, đúng thiết kế (ngưỡng cảnh báo 50% hạn mức). Không cần TC verify fix, nhưng nên có TC xác nhận ngưỡng 50% không bị fix này làm lệch.

**Trao đổi với khách còn đang mở** (journal 2026-09-03 12:27 / 12:29, ホアン): phía support vẫn đang xác nhận lại triệu chứng 2 chữ số/4 chữ số với khách. Khách chưa xác nhận lại → **flow reproduce chính xác từ phía khách chưa được chốt**.
