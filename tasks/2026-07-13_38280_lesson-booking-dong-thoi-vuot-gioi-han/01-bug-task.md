# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38280 — [29-06-2026][28719][Lesson] Đặt giới hạn 1 khung/ngày cho đặt lịch học nhưng khi 2 người bấm đăng ký cùng lúc thì cả hai đều đặt được (vượt giới hạn), hỏi cách ngăn chặn.` |
| Redmine URL | https://redmine.watermelon.vn/issues/38280 |
| Auto-filled | `2026-07-13 by /new-task` |
| Ngày báo cáo | `2026-06-29` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn KH: ty.photo.office@gmail.com — bot STUDIO CUDDLE公式LINE; comment Slack: 沖原裕樹) |
| Module / Màn hình | `Lesson` (category Redmine) — レッスン予約 / trang booking phía LINE user |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>` — KH thao tác trên bot thật (STUDIO CUDDLE公式LINE) ⇒ nhiều khả năng Production |
| Tracker / Status | `Bug KH` / `KH Feedback` |
| Parent | `#36898` |
| Commit Date (custom field) | `2026-07-13` |
| Assignee | `Ngô Thúy Ngần` |

## Mô tả bug (nguyên văn từ khách hàng)

```
User: ty.photo.office@gmail.com
Bot Name: STUDIO CUDDLE公式LINE

Xin lỗi, còn một điểm nữa.

Ở chức năng đặt lịch học (レッスン予約), tôi đã thiết lập số khung tiếp nhận trong 1 ngày là 1 khung.
Hai nhân viên của công ty chúng tôi đã thử nghiệm: cùng lúc bấm nút đăng ký đặt chỗ hoàn toàn đồng thời, thì cả hai đều đặt được. Có cách nào để ngăn chặn việc này không?

Chức năng: Đặt lịch học (レッスン予約)
Thời điểm phản hồi: 2026/06/29 10:38:00

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=28719
Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BDS8N06KC
Nguồn: Google Sheet dòng 54, 回答ID 28719

---

h3. 原文 (JP)
<pre>
もう一点申し訳ありません。

レッスン予約で、1日の受付枠を1枠に設定しました。
当社スタッフ2人で実験的に、全く同時に予約申し込みボタンを押したら、2人とも予約できてしまいました。これをどうにか防ぐ方法は無いでしょうか？
</pre>

<!-- TaskRef: cs_form:28719 -->
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Nguyên văn từ journal Redmine #123920 (Ngọc Ánh, 2026-06-29 03:02) — Redmine KHÔNG có heading "Tái hiện bug" riêng; steps được ghi trong journal.
>
> ```
> line_user_id: 362332
> calendar_id: 10955
> Về các bước thao tác cụ thể:
> ・Đặt 2 chiếc điện thoại cạnh nhau
> ・Bấm nút đặt lịch cùng lúc
> ```

1. Setting lịch học (レッスン予約): số khung tiếp nhận trong 1 ngày = **1 khung** (calendar_id: 10955).
2. Chuẩn bị 2 LINE user (2 điện thoại) mở cùng trang đặt lịch, cùng khung giờ còn **1 chỗ**.
3. Đặt 2 điện thoại cạnh nhau, **bấm nút đăng ký đặt chỗ hoàn toàn đồng thời**.

## Expected result

- Chỉ **1** lượt đặt được tạo; lượt còn lại bị chặn / báo hết chỗ (không vượt giới hạn 1 khung/ngày).

## Actual result

- **Cả hai** lượt đặt đều thành công ⇒ vượt giới hạn số khung tiếp nhận đã setting.
- Nhận định của KH (journal #124020): "khi hai lượt đặt lịch được thực hiện gần như cùng một thời điểm, dù số lượng đặt lịch đã vượt quá giới hạn tối đa thì hệ thống vẫn không thể chặn một trong hai lượt đặt lịch."

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/27637/1782701333gmTysY.png
- https://redmine.watermelon.vn/attachments/download/27664/image_1113189_620538014652957256_1782700791042.jpg
- https://redmine.watermelon.vn/attachments/download/27665/image_1113188_620538015021793477_1782700791043.jpg
- https://redmine.watermelon.vn/attachments/download/27667/image_1113189_620538014652957256_1782700791042.jpg
- https://redmine.watermelon.vn/attachments/download/27668/image_1113188_620538015021793477_1782700791043.jpg

## Ghi chú thêm của Leader

- ⚠️ **Bug là race condition** — chỉ tái hiện khi 2+ user bấm đặt **cùng thời điểm (cùng giây)**. TC phải mô tả rõ cách tạo đồng thời (2 thiết bị/2 tab bấm cùng lúc), không thể verify bằng thao tác tuần tự.
- ⚠️ Redmine **không ghi env phát hiện**; KH báo trên bot thật ⇒ giả định Production. Tester confirm env test với Leader.
- ⚠️ Scope fix của Dev **mở rộng sang Salon (FA-020)** dù bug KH chỉ báo Lesson — xem `03-dev-impact.md` mục 4.3.
- Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1782699228003619
- Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=38280
