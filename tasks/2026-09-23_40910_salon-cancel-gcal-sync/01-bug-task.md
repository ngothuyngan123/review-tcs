# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40910 — [14-09-2026][T12148][Salon] Khách báo hủy đặt lịch salon ở calendar dành cho hội viên nhưng calendar dành cho khách mới (chia sẻ chung Google Calendar) vẫn còn booking đã xóa, không sửa được từ Elme.` |
| Module / Màn hình | Đặt lịch salon・phỏng vấn (サロン・面談予約) — FA-020. Cụ thể: hủy đặt lịch ở lịch đặt salon 会員様用 + hiển thị khung giờ bị chặn ở lịch 新規様用 (2 lịch salon dùng CHUNG 1 Google Calendar) |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ TẠO TASK ĐIỀU TRA NỘI BỘ (chưa có ticket Slack)

User: ecconeil.hiroshima@gmail.com
Bot Name: エッコネイル広島京橋店

Cảm ơn quý công ty đã luôn hỗ trợ.

**＜Tiền đề＞**

Về đặt lịch salon, chúng tôi đang vận hành với lịch đặt (予約カレンダー) chia riêng cho「新規様用」(dành cho khách mới) và「会員様用」(dành cho hội viên), liên kết chung với một Google Calendar.

Hiện tại, mặc dù đã hủy và xóa booking (桑田様 9/24 từ 11 giờ 30〜) từ calendar đặt lịch dành cho hội viên, nhưng thông tin booking đã xóa vẫn còn lại trong calendar đặt lịch dành cho khách mới, và không thể chỉnh sửa từ phía エルメ (Elme).

**＜Việc cần xử lý gấp＞**

Lần này, dự định sẽ xử lý bằng cách xóa trực tiếp booking trên Google Calendar, nhưng mong quý công ty sớm điều tra nguyên nhân và có biện pháp gấp về việc「なぜ、会員様用の予約カレンダーでキャンセルした予約が、まだGoogleカレンダーに反映されたままになっており、エルメ上に残ったままになったのか」(tại sao đặt lịch đã hủy ở calendar đặt lịch dành cho hội viên vẫn còn được phản ánh trên Google Calendar và vẫn còn nằm lại trên Elme).

Chúng tôi đã sử dụng Elme khoảng nửa năm, nhưng cảm thấy số lỗi phát sinh nhiều hơn so với các dịch vụ khác, nên mong quý công ty triệt để có biện pháp để không xảy ra trường hợp tương tự trong tương lai.

Xin lỗi vì đã làm phiền quý công ty trong lúc bận rộn, mong nhận được sự hỗ trợ.

---

- Tên friend: くわた こまち
- Chức năng: Đặt lịch salon・phỏng vấn (サロン・面談予約)
- Thời điểm phản hồi: 2026/09/14 13:18:35
- Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12148
- Nguồn: Tayori — task #12148 (操作方法に関するお問い合わせフォーム)
- Link Tayori: https://tayori.com/admin/task/58f4fd7fe1f41df9dcb8fe584dd3916770d298ca/

## Steps to reproduce

> Nguồn: **Journal #137841 — Đỗ Quyên — 2026-09-23** (cách tái hiện do QA chốt, dùng để dựng env test).

**Tiền điều kiện:** lịch salon có staff + bật phân bổ nhân viên tự động (random staff) + đã liên kết Google Calendar.

1. Dev **dừng** job random staff (`CalendarSalonStaffAssignment` / `CalendarSalonStaffAssignmentAdmin`).
2. Đặt lịch (booking) khi chưa có staff ⇒ **hủy (cancel) ngay** đặt lịch đó.
3. Dev **bật lại** job random staff.

## Expected result

- Sau khi job được bật lại ⇒ đặt lịch được sync lên Google Calendar rồi **bị xóa luôn** (vì đặt lịch này đã bị hủy).
- Theo mô tả của khách: hủy đặt lịch trên エルメ phải được phản ánh sang Google Calendar, và **lịch đặt salon khác cùng khung giờ được liên kết với Google Calendar đó cũng bị xóa theo** (他のエルメ予約カレンダーにも反映される).

## Actual result

- Sau khi random staff, booking được sync lên Google Calendar và **KHÔNG bị xóa đi** (dù booking này đã được cancel) ⇒ đặt lịch "ma" nằm lại trên Google Calendar.
- Hệ quả trên màn hình khách: đặt lịch đã hủy ở lịch 会員様用 vẫn hiện (chiếm khung giờ) ở lịch 新規様用 dùng chung Google Calendar, và **không sửa / không xóa được từ Elme** (vì bản ghi đó là bản sao chặn giờ kéo từ Google, không phải đặt lịch của Elme).
- Khách xác nhận: **hơn 1 tiếng** sau khi hủy trên エルメ, Google Calendar vẫn chưa được phản ánh, đặt lịch vẫn còn nguyên.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.watermelon.vn/attachments/download/30401/screenshot1.png
- screenshot2.png — https://redmine.watermelon.vn/attachments/download/30402/screenshot2.png
- SnapCrab_NoName_2026-9-21_10-15-11_No-00.png — https://redmine.watermelon.vn/attachments/download/30647/SnapCrab_NoName_2026-9-21_10-15-11_No-00.png
- SnapCrab_NoName_2026-9-21_10-15-45_No-00.png — https://redmine.watermelon.vn/attachments/download/30648/SnapCrab_NoName_2026-9-21_10-15-45_No-00.png
- SnapCrab_NoName_2026-9-14_14-45-52_No-00.png — https://redmine.watermelon.vn/attachments/download/30649/SnapCrab_NoName_2026-9-14_14-45-52_No-00.png

## Ghi chú thêm của Leader

- **Điều kiện tiên quyết bắt buộc để tái hiện**: bot phải có **≥ 2 lịch salon** (vd 新規様用 + 会員様用) **cùng trỏ 1 `google_calendar_id`**; lịch salon bật **phân bổ nhân viên tự động** (ランダム / 設定順) và đã liên kết Google Calendar.
- **Không phải lỗi 100%** — theo Dev (journal #137774), xóa hụt xảy ra khi: (a) không tra được bản ghi liên kết Google của lịch/nhân viên, hoặc token rỗng → hàm xóa **bỏ qua im lặng**, không ghi retry; (b) đặt lịch **không chỉ định nhân viên** thì cách tra liên kết lúc xóa lỏng hơn lúc tạo → bốc nhầm tài khoản Google khác; (c) hủy **ngay khi job phân bổ nhân viên chưa xong** → lệnh xóa chạy TRƯỚC lệnh tạo sự kiện.
- **Timing nhạy cảm**: kịch bản (c) cần hủy trong khoảng **~10–30 giây** sau khi đặt lịch (trước khi job random staff hoàn tất). Cách tái hiện ổn định = dừng job thủ công như Journal #137841.
- **Môi trường phát hiện**: Production (bot khách hàng エッコネイル広島京橋店).
- ⚠️ **RECOVER DATA — CÓ** (journal #137774 mục 5): sự kiện mồ côi đã tồn tại trên Google Calendar của khách + bản sao chặn giờ trong `calendar_salon_booking_by_google` **KHÔNG tự biến mất sau deploy** — fix chỉ chặn ca phát sinh mới. Cần rà & dọn dữ liệu cũ riêng.
- ⚠️ **Lưu ý deploy** (journal #137774): 2 migration (`ALTER TABLE` thêm cột + tạo index) chạy trên bảng **rất lớn** ⇒ phải chạy **giờ thấp điểm**.
- ⚠️ Support đã trả lời sai hướng ở journal #137287 (nói "Google Calendar không có lịch nào đăng ký" + "phản ánh không realtime"), khách phản bác ở journal #137288 — root cause thật nằm ở luồng xóa sự kiện, không phải độ trễ đồng bộ.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — Bot Name: エッコネイル広島京橋店>` |
| Friend | `くわた こまち` (桑田様) |
| Đối tượng cấu hình | 2 lịch salon dùng chung 1 Google Calendar: `新規様用` + `会員様用` |
| Đặt lịch lỗi | 桑田様 — **2026/09/24 (木) 11:30〜** (support tra theo khung `11:45〜13:45`) |
| Thời điểm lỗi | Khách báo `2026/09/14 13:18:35` |
| Đối chứng | `<chưa có case đối chứng trong ticket>` |
| Account báo lỗi | `ecconeil.hiroshima@gmail.com` |

## Journal / note từ Redmine (nguyên văn)

**Journal #137287 — AI bug detect Lme (comment slack 2026-09-14 14:49:00, 沖原 裕樹（エルメサポート）) — 2026-09-21:**

```
Cảm ơn quý khách đã luôn ủng hộ.

Sau khi kiểm tra, hiện tại lịch đặt Salon liên quan không có lịch Google Calendar nào được đăng ký vào 2026.09.24 (木) 11:45～13:45.

Vì lịch Google Calendar không được phản ánh theo thời gian thực, nên dù đã xóa lịch trên Google Calendar, có thể mất thời gian để phản ánh sang エルメ.

Do đó, nếu lịch Google Calendar chưa được phản ánh lên lịch đặt Salon, mong quý khách vui lòng đợi một thời gian rồi kiểm tra lại.

Xin cảm ơn quý khách.
```

**Journal #137288 — AI bug detect Lme (comment slack 2026-09-20 19:03:00, お客様) — 2026-09-21:**

```
Có ghi rằng「Googleカレンダーの予定は登録されていませんでした。」, nhưng như đã đề cập ngay từ đầu phần ＜Nội dung cần xử lý gấp＞ trong yêu cầu, đó là vì cần xử lý ngay lập tức nên tôi đã xóa trực tiếp lịch đặt trên Google Calendar để xử lý.

Vốn dĩ, việc hủy đặt lịch trên エルメ sẽ được phản ánh sang Google Calendar, và lịch đặt Salon khác cùng khung giờ được liên kết với Google Calendar đó cũng sẽ bị xóa theo (他のエルメ予約カレンダーにも反映される), nhưng lần này điều đó đã không hoạt động.

※ Mặc dù đã hơn 1 tiếng kể từ khi hủy đặt lịch trên エルメ, nhưng điều đó vẫn chưa được phản ánh trên Google Calendar, lịch đặt vẫn còn nguyên.

Để việc này không xảy ra lần nữa, mong quý vị điều tra lại nguyên nhân giúp tôi.

Xin cảm ơn quý vị.
```

**Journal #137841 — Đỗ Quyên — 2026-09-23:**

```
Cách tái hiện:
***Tiền điều kiện: calendar staff + bật random staff + đã liên kết gg calendar
1. dev dừng job random staff
2. booking no staff => cancel luôn
3. dev bật lại job random staff

Hiện tại: booking sau khi random staff thì được sync lên gg calendar và ĐANG KHÔNG XÓA đi (booking này đã được cancel)
Expect: sau khi job bật lại => booking được sync lên gg rồi bị xóa luôn
```

**Journal #137283 — AI bug detect Lme — 2026-09-21 (tracking):**

```
OEM đã push task lên Slack (ユーザー問い合わせ) → xác nhận Bug KH.
Đổi tracker "Bug KH cần xử lý nội bộ" → "Bug KH".
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C35NSU35L
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1789953679855679?thread_ts=1789953679.855679&cid=C0BALS7S73L
```
