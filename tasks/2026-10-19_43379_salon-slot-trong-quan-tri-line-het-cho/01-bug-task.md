# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43379 — [18-10-2026][32376][Salon] Khách báo slot 17:30–18:00 ngày 10/28 của staff 丸山智 còn trống trên quản trị nhưng phía LINE hiển thị không còn chỗ; lỗi lặp lại, từng xảy ra tháng 9.` |
| Module / Màn hình | Đặt lịch salon・phỏng vấn (サロン・面談予約) — lịch nhiều nhân viên dùng course + giới hạn theo từng nhân viên (`calendar-salon`) |

## Mô tả bug (bản dịch tiếng Việt)

OEM ĐÃ TẠO TICKET SLACK

User: yorcshincity@gmail.com
Bot Name: ながの駅前BJ整骨院

Đặt lịch salon・phỏng vấn → ながの駅前BJ整骨院 → Dù staff 丸山智 ngày 10/28 còn trống lịch từ 17:30 đến 18:00 nhưng từ LINE lại hiển thị là không còn slot.

Trước đây cũng từng xảy ra hiện tượng tương tự với cùng staff.

Cuối tháng 9 vừa rồi, với tài khoản khác hiện tượng này cũng phát sinh và chúng tôi đã liên hệ エルメ. （Lúc đó cũng chưa giải quyết tận gốc）

Xin hãy cho biết nguyên nhân và cách cải thiện. m(_ _)m

Chức năng: Đặt lịch salon・phỏng vấn (サロン・面談予約)
Thời điểm phản hồi: 2026/10/18 15:21:00
Ảnh 1: https://go.lmes.jp/msg_template/media/images/3/218/form/1792304474tajIGo.jpeg

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=32376

(Card Slack OEM ghi 管理番号 0000 — đã map tay về 回答ID 32376)

Ticket Slack do OEM đăng — 管理番号 32376

> ⚠️ Redmine không có section "Tái hiện bug" / "Đánh giá ảnh hưởng" theo template chuẩn (ticket dạng Bug KH do AI phát hiện từ Slack OEM). Steps/Expected/Actual dưới đây được suy trực tiếp từ câu mô tả trên + journal điều tra của QA (#145044), **không diễn giải thêm**. Đánh giá ảnh hưởng đầy đủ nằm ở các journal "Dev Studio" → đã tổng hợp vào `03-dev-impact.md`.

## Steps to reproduce

Case thực tế (khách báo, journal #145027):
1. Bot `ながの駅前BJ整骨院` (bot_id 60002), salon `ながの駅前BJ整骨院` (salon_id 6186), course `▼総院長コース` (course_id 56331), staff `丸山 智` (staff_id 7576).
2. Friend mở LINE → Đặt lịch salon・面談予約 → chọn salon trên → chọn staff 丸山智 + course → xem khung giờ ngày 10/28.
3. Khung 17:30–18:30 hiển thị **hết chỗ** trên LINE, trong khi màn quản trị cho thấy staff 丸山智 còn trống giờ này.

Case tái hiện tổng quát (QA xác nhận, journal #145044):
1. Lịch salon option **1.1** — mỗi staff = 1 suất, KHÔNG bật random, có 9 staff (staff 1–9 không có lịch nghỉ/vắng).
2. Staff 2 → 5, 8 có ca 16h–20h; staff 6–7 nghỉ.
3. Có 2 course: course 1h (các staff khác làm được) và course 30p (chỉ staff 8 làm được).
4. Course 1h có 1 đơn **指定なし** (không chỉ định nhân viên) chiếm khung 17h30–18h30.
5. Staff 8 có đơn từ 16h–17h30 và 18h30–20h → khung 17h30–18h30 của staff 8 còn trống.
6. Friend chọn staff 8 + course 30p → khung 17h30–18h30 **không hiển thị** để đặt (dù staff 8 chưa có đơn nào trùng giờ).

## Expected result

- Khung giờ 17:30–18:00 (và rộng hơn 17:30–18:30) của staff 丸山智 ngày 10/28 phải hiển thị **còn trống** trên LINE, khớp với trạng thái trên màn quản trị, và đặt được.
- Tổng quát: đơn 指定なし của course mà staff đang được chọn **không làm được** thì không được tính vào số chỗ còn lại của staff đó.

## Actual result

- Từ LINE hiển thị là **không còn slot** cho khung 17:30–18:00 của staff 丸山智 ngày 10/28, trong khi quản trị cho thấy còn trống.
- Tổng quát: mọi đơn 指定なし (bất kể course) đều bị trừ vào số chỗ còn lại của staff, nên 1 đơn 指定なし của course khác vẫn chiếm oan suất duy nhất của staff đang xét → khung bị ẩn, đặt bị báo hết chỗ.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.jpg — https://redmine.melonglobal.net/attachments/download/35405/screenshot1.jpg

## Ghi chú thêm của Leader

- Bug **lặp lại** — từng xảy ra cuối tháng 9 với tài khoản khác, lúc đó CS đã liên hệ エルメ nhưng **chưa giải quyết tận gốc**. Cân nhắc regression theo đúng hướng "sửa dứt điểm" lần này, không chỉ patch theo case đơn lẻ.
- Ticket do **AI bug detect Lme** tạo từ ticket Slack của OEM (quản lý số 32376), không phải Dev/CS report trực tiếp.
- Môi trường phát hiện: **Production** — khách hàng thật, bot thật (bot_id 60002), dashboard css-analytics link đến id 32376.
- Status hiện tại trên Redmine: **Fix done - Đợi test**.
- Dev đã thực hiện **nhiều vòng sửa** (xem `03-dev-impact.md`): v1–v5 cho phần LINE/job, sau đó phát sinh lệch giữa LINE và màn quản trị → có thêm vòng sửa riêng cho màn quản trị xem ngày (`CalendarSalonStaffService`).
- Redmine ghi nhận **4 bug con do QA tạo** trong lúc test task này mà Dev đề nghị Reject (xem journal #145324): `#43447` (hành vi trùng nhánh release, kiểu 上限を設定する nằm ngoài phạm vi), `#43448` (lịch 個人 ngoài phạm vi, fixture QA seed sai limit), `#43449` (lỗi selector automation), `#43450` (automation chờ request không phát sinh). ⚠️ Theo snapshot Studio (`04-tc-list.md`), TC map tới `#43447` (NEW-8) đang **fail thật** trên môi trường local — Leader cần xác nhận lại với Dev trước khi reject.
- Branch Dev: `ai_studio_fixbug_43379` (gốc `release_step_20260930_v2`).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `60002` |
| Friend / User | `nagano-ekimae-bj@north-sun.net` (khách CS báo: `yorcshincity@gmail.com`) |
| Đối tượng cấu hình | Salon: `ながの駅前BJ整骨院` (salon_id `6186`) · Course: `▼総院長コース` (course_id `56331`) · Staff: `丸山 智` (staff_id `7576`) |
| Thời điểm lỗi | `2026/10/28 17:30 ～ 18:30` |
| Đối chứng | Journal #145044 — case tổng quát 9 staff / 2 course tái hiện cùng cơ chế lỗi (đơn 指定なし course khác chiếm oan suất) |

## Journal / note từ Redmine (nguyên văn)

**Journal #145027 — Ngô Thúy Ngần — 2026-10-19:**
```
User: nagano-ekimae-bj@north-sun.net
bot_id: 60002
Tên salon: ながの駅前BJ整骨院 (salon_id: 6186)
Tên course: ▼総院長コース (course_id: 56331)
Tên staff: 丸山 智 (staff_id: 7576)
Thời gian không thể booking: 10月28日17:30～18:30
```

**Journal #145044 — Đỗ Quyên — 2026-10-19:**
```
Cách tái hiện: 
option 1.1, mỗi staff = 1 
ko bật random 
có 9 staff,
staff 1-9 ko có lịch lv
staff 2 -> 5,8: 16 -20h 
staff 6-7 nghỉ 
==> Có 2 course: course 1h (các staff khác thực hiện) và course 30p (chỉ có staff 8 thực hiện) 
course 1h có 1 booking ở no staff chiếm khung giờ 17h30-18h30
staff 8 có booking từ 16h - 17h30 và 18h30 -20h (CÒN TRỐNG KHUNG 17H30 - 18H30)
==> friend chọn staff 8 - course 30p => ko hiển thị slot để book
```

**Journal #145324 — Dev Studio — 2026-10-19 (handoff cuối, 15:43):** xem toàn văn ở `03-dev-impact.md` §1–§4 (đã tổng hợp từ các vòng trước #145075 / #145248 / #145315).
