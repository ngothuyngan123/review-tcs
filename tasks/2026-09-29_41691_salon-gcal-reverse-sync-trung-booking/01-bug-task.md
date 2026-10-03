# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41691 — [28-09-2026] [31223] [Salon] Lịch Salon bị phản ánh ngược từ Google Calendar gây trùng/lỗi đặt lịch` |
| Module / Màn hình | `Salon Booking (FA-020) — đồng bộ lịch với Google Calendar (予約カレンダー⇒日)` |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 (quản lý No.) 31223
Phụ trách: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1790579182580309?thread_ts=1790579182.580309&cid=C0BALS7S73L
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=31223

Quản lý No：31223
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C4WFCJAD8
Địa chỉ：more.petsalon@gmail.com
Tên LOA：petsalon&hotel モア
Phụ trách：沖原
Công cụ：リンク
Nội dung liên hệ:
Sau khi lịch đặt Salon được phản ánh vào Google Calendar, lịch trình đã phản ánh trên Google Calendar lại bị phản ánh ngược trở lại vào lịch đặt Salon.

## Steps to reproduce

1. Liên kết Google Calendar (bot/lịch salon đã liên kết tài khoản Google).
2. Add booking từ LME (user book hoặc admin book) — đơn đặt lịch được đẩy lên Google Calendar.
3. Set `b_c_salon_google_calendar.next_time_sync` về quá khứ → báo Dev chạy job sync booking google (job này kéo 1 năm các booking từ Google Calendar về, tối đa 2 năm tức 2 lần chạy).

<!-- Steps trên tổng hợp từ Journal #139179 (Thanh Phương, 2026-09-29) — không có section "Tái hiện bug" riêng trong description gốc của khách. -->

## Expected result

- Lịch hẹn Google do chính đơn đặt lịch Salon đẩy lên KHÔNG bị kéo ngược trở lại thành khung giờ chặn (block time); khách vẫn đặt được đúng khung giờ đó, không báo trùng/lỗi.

## Actual result

- Lúc job `syncEventYearlyGoogleCalendarSalon` chạy, job đang sync ngược cả những booking đã add từ LME lên Google Calendar về, khiến các booking này bị tính là khung giờ chặn (block time) → hiển thị trùng lịch, khách không đặt được khung giờ đó.
- Với liên kết có mốc hẹn ở quá khứ, cửa sổ quét bắt đầu từ hiện tại nên toàn bộ đơn đặt lịch trong 1 năm tới bị phản ánh ngược trong một lượt cron.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/31118/SnapCrab_NoName_2026-9-28_16-3-47_No-00.png
- Ảnh khách gửi qua Slack (đính kèm trong Journal, không phải attachment Redmine):
  - https://go.lmes.jp/msg_template/line-user/media-step/218/image/image_1138153_633742788391075841_1790571443510.jpeg
  - https://go.lmes.jp/msg_template/line-user/media-step/218/image/image_1138155_633742856556904823_1790571484210.jpeg
  - https://go.lmes.jp/msg_template/line-user/media-step/218/image/image_1138158_633742990858519132_1790571564250.jpeg

## Ghi chú thêm của Leader

- Trigger chính là **cron `job:syncEventYearlyGoogleCalendarSalon`** (Kernel.php dailyAt 02:15, lên release 2026-09-18) — khách báo lỗi 2026-09-28, khớp thời điểm release lên.
- Khách mô tả nhu cầu nghiệp vụ: muốn đặt "chỗ đè" — đặt tiếp lịch chồng lấn ~30 phút hoặc chèn đặt chỗ giữa các đặt chỗ khác (đang dùng tính năng nhắc nhở LINE theo lịch). Khung giờ khách muốn đặt: 11/24 11:00〜13:00 — bị báo lỗi không đặt được do khung giờ chặn giả (chính là đơn cũ bị phản ánh ngược).
- Root cause đã được Dev/AI-fixbug confirm (xem file 03) — bug không có script tái hiện tự động độc lập trong Redmine, tái hiện dựa trên steps ở Journal #139179 (set `next_time_sync` về quá khứ để ép chạy job).
- Bản sửa lần 1 (đặt guard trong `createBookingFromEvent`) đã bị revert theo yêu cầu human; bản fix hiện tại đặt guard tại `syncEventYearlyFromGoogle` (đúng vòng lặp cron chạy) — cần lưu ý khi review vì đây là điểm đã đổi hướng fix.
- Có **lệnh recover dữ liệu** đi kèm (`RecoverSalonBookingByGoogleReverseSync`) — bắt buộc chạy `--dry-run` trước khi xoá thật (xem chi tiết file 03 mục 2 + 5).
- Chưa verify runtime — Dev ghi rõ "CHƯA chạy được runtime: MySQL dev Connection refused, và bản checkout chính của source/sns-line đang tụt 492 commit nên không boot app để test container resolve được". TCs cần tự dựng env để verify thật, không dựa vào tự-test của Dev.
- Lỗ hổng liên quan nhưng **KHÔNG sửa trong ticket này** (Dev tự nêu, cân nhắc mở ticket riêng, không tính vào phạm vi review): khi user kết nối lại tài khoản Google cho nhân viên, `oauthCalendarSalon` gọi `deleteBookingSyncFromLme` xoá trắng mã sự kiện Google trên các đơn đặt lịch → chọn lại đúng lịch Google cũ thì sự kiện cũ mất dấu vết, vẫn bị kéo về thành khung giờ chặn. Liên quan tới ticket #41324 (đường ghi sự kiện đang chuyển sang job Java).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — quản lý No 31223, tên LOA petsalon&hotel モア>` |
| Friend | `<không áp dụng — bug ở tầng job/admin, không phải friend cụ thể>` |
| Đối tượng cấu hình | `Lịch salon đã liên kết Google Calendar; khung giờ lỗi khách báo: 11/24 11:00〜13:00` |
| Thời điểm lỗi | `2026-09-28 (khách báo), job lên release 2026-09-18` |
| Đối chứng | `Khách xác nhận "trước đây tôi vẫn đặt chỗ được như trong ảnh trên" — trước khi job/release 2026-09-18 lên` |

## Journal / note từ Redmine (nguyên văn)

**Journal #139053 — AI bug detect Lme — 2026-09-28:**

```
Comment slack ngày 2026-09-28 09:56:58

沖原裕樹（エルメサポート）
Cảm ơn quý khách đã liên hệ.

＞Không có thay đổi hệ thống gì cả, và bình thường thì vẫn có thể đặt chỗ đè như trước đây, đúng không ạ？

⇒Gần đây không có thay đổi hệ thống nào được thực hiện.

「被せての予約」(đặt chỗ đè) có nghĩa là đặt 2 chỗ trong cùng một khung giờ phải không ạ？

Trong trường hợp đó, chúng tôi sẽ kiểm tra, nên mong quý khách vui lòng cho biết ảnh chụp màn hình thông báo lỗi hiển thị và ngày giờ tương ứng không thể đặt được.

Mong quý khách vui lòng hỗ trợ.
```

**Journal #139054 — AI bug detect Lme — 2026-09-28:**

```
Comment slack ngày 2026-09-28 13:57:13

お客様
Cảm ơn quý khách.

「被せての予約」(đặt chỗ đè) có nghĩa là,
muốn đặt chỗ tiếp theo đè lên chỗ trước đó chỉ 30 phút(例えば、1予約を9:00〜12:00、2予約を11:30〜14:00)、hoặc muốn chèn một đặt chỗ khác vào giữa các đặt chỗ(1予約10:00〜12:00、2予約9:00〜14:00)。

Vì đang sử dụng chức năng nhắc nhở (reminder), nên tôi muốn gửi LINE cho khách hàng theo lịch đó.
```

**Journal #139058 — AI bug detect Lme — 2026-09-28:**

```
Comment slack ngày 2026-09-28 13:59:11

お客様
Tôi muốn đặt chỗ trong khung giờ 11/24　11:00〜13:00, nhưng như trong ảnh dưới đây, thông báo lỗi hiện lên và không thể đặt được
```

**Journal #139179 — Thanh Phương — 2026-09-29:**

```
Tái hiện:
1. Liên kết google calendar
2. Add booking từ lme (user book/admin book)
3. Set b_c_salon_google_calendar.next_time_sync về quá khứ => Báo dev chạy job sync booking google (JOb này đang get 1 năm 1 các booking từ google calendar về, và get tối đa 2 năm, tức 2 lần chạy)

BUG: LÚc chạy job đang sync cả những booking add từ lme trên google về nên bị tính là block time
```

<!-- Journal #139163 (AI LME Fix bug) là "Đánh giá ảnh hưởng" đầy đủ — đã chuyển toàn bộ sang file 03-dev-impact.md, không lặp lại ở đây. -->
