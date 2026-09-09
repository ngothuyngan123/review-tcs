# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40128 — [24-08-2026][29927][Salon] Khách báo hệ thống cho phép gửi yêu cầu đặt lịch ngoài khung giờ ca làm việc dù chỉ thiết lập ca đến 20h30.` |
| Redmine URL | https://redmine.watermelon.vn/issues/40128 |
| Auto-filled | `2026-08-26 by /new-task` |
| Ngày báo cáo | `2026-08-24` |
| Khách hàng / PM báo | `AI bug detect Lme` (author Redmine) — khách hàng thật: bot `イメコンサロンPASOKA名古屋店` / user `imecon.pasoka@gmail.com` |
| Module / Màn hình | `Salon` (category Redmine) — KH ghi chức năng: `Quản lý đặt lịch (予約管理)` |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `Production` — suy từ URL media `go.lmes.jp` + bot khách hàng thật trong description. ⚠️ Redmine KHÔNG ghi rõ tên môi trường, tester verify lại. |
| Tracker / Status | `Bug KH` / `Fix done - Đợi test` |
| Assignee | `Ngô Thúy Ngần` |
| Commit Date (custom field) | `2026-08-25` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #40128. KHÔNG diễn giải lại. -->

```
User: imecon.pasoka@gmail.com
Bot Name: イメコンサロンPASOKA名古屋店

Chỉ nhập ca làm việc (shift) đến 20 giờ 30 nhưng vẫn có thể gửi yêu cầu đặt lịch (予約リクエスト) ở ngoài khung giờ ca làm việc.

Tên friend: Risa Yamasaki
Chức năng: Quản lý đặt lịch (予約管理)
Thời điểm phản hồi: 2026/08/24 15:38:00
Ảnh 1: https://go.lmes.jp/msg_template/media/images/3/218/form/1787553496ZXxJj3.png
Ảnh 2: https://go.lmes.jp/msg_template/media/images/3/218/form/17875535078Nih0S.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=29927
Nguồn: Google Sheet dòng 106, 回答ID 29927

---

h3. 原文 (JP)
<pre>
シフトは20時半までしか入力してないのにシフト外の時間に予約リクエスト可能になっている
</pre>

<!-- TaskRef: cs_form:29927 -->
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguồn: Redmine journal #133038 — Kim Cúc, 2026-08-26T05:18:02Z, section "Tái hiện bug KH". Nguyên văn. -->

1. Salon private có setting 2 staff
2. Staff 1 làm việc từ 10h~20h30, staff 2 làm việc từ 14h30~21h
3. Có 2 Course, 1 course 2 giờ, 1 course 3h30p
4. Tại màn [ 店舗とスタッフの受付上限] Setting chọn option [ 1つの予約を1人のスタッフのみで対応する（シフトの合算をしない）], settng 1 staff trong 1 khung thời gian chỉ được 1 booking
5. Tại màn [前後の空き時間] setting time nghỉ là 1 giờ [予約の「後」に空き時間を設定する]
6. Line user có booking vào staff 2 từ 17h30~21h
7. Line user booking chọn vào course làm việc 2h và chọn no staff

## Expected result

⚠️ Redmine KHÔNG ghi Expected tường minh trong section "Tái hiện bug KH". Dưới đây trích **nguyên văn phản hồi KH** (journal #132659, 2026-08-25):

- `Ngày 9/4, ca làm việc của MARIN đến 21時, còn Yayoi đến 20時半, nên ban đầu lịch đặt từ 17時半 đến 21時 đã được MARIN đảm nhận.`
- `Thời gian còn lại có thể nhận yêu cầu đặt lịch chẳng phải là đến 18時半 của Yayoi mới đúng sao?`
- `Ca làm việc của Yayoi chỉ đến 20時半, nên việc có yêu cầu đặt lịch từ 19時 không phải là bất thường sao?` (journal #132658)

## Actual result

<!-- Nguồn: Redmine journal #133038, dòng "Hiện tượng". Nguyên văn. -->

- `Hiện tượng: Vẫn hiển thị lịch làm việc của khung 19:00`
- KH bổ sung (journal #132659): `Vào khoảng 15時 hôm nay đã có yêu cầu đặt lịch từ 9/4 19時 vào nên sau khi phê duyệt tôi đã đổi phụ trách. Không phải là yêu cầu đặt lịch phát sinh sau khi đổi phụ trách.`

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachment Redmine:
- https://redmine.watermelon.vn/attachments/download/29322/screenshot1.png
- https://redmine.watermelon.vn/attachments/download/29323/screenshot2.png
- https://redmine.watermelon.vn/attachments/download/29339/SnapCrab_NoName_2026-8-25_9-46-42_No-00.png

Ảnh KH gửi trong description:
- https://go.lmes.jp/msg_template/media/images/3/218/form/1787553496ZXxJj3.png
- https://go.lmes.jp/msg_template/media/images/3/218/form/17875535078Nih0S.png
- https://go.lmes.jp/msg_template/media/images/3/218/1787560007kvCCXc.png (エルメサポート gửi lại, journal #132657)

## Ghi chú thêm của Leader

- ⚠️ **Giả thuyết đầu tiên của support ĐÃ BỊ KH bác bỏ.** Support (journal #132656) trả lời rằng slot ngoài ca là do admin **đổi nhân viên phụ trách thủ công** (MARIN→Yayoi lúc 8/24 15:31) — gán thủ công vốn không bị chặn theo ca. Nhưng KH phản hồi (journal #132659): **yêu cầu đặt lịch 19:00 phát sinh TRƯỚC khi đổi phụ trách**, nên nguyên nhân thật nằm ở tính khung giờ trống, không phải ở gán thủ công. Dev impact (file 03) đã đi theo hướng này.
- Cấu hình lịch trong bug: chế độ `1つの予約を1人のスタッフのみで対応する（シフトの合算をしない）` (1 đơn = 1 nhân viên, KHÔNG gộp ca) + mỗi nhân viên trần 1 lượt + `予約の「後」に空き時間を設定する` = 60 phút.
- Data ngày sự cố (9/4): MARIN ca đến 21:00, Yayoi ca đến 20:30, đã có đơn 17:30–21:00 của MARIN. Steps tái hiện của Kim Cúc dùng cùng shape data.
- Trạng thái Redmine hiện tại: `Fix done - Đợi test`, branch `ai_fixbug_40128`.
