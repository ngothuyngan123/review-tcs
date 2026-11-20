# 01 — Bug Task từ khách hàng

> **Lượt B của sprint #45229** — nhóm **T15. Exception PHP do AI phát hiện**, phần liên quan **đặt lịch Salon** (#41717 · #41529 · #41718). Phần còn lại của T15 (#45186 · #42266) review ở lượt C. Folder cha: [tasks/2026-11-16_45229_sprint-fix-bug-bao-mat-hieu-nang-php-web/](../2026-11-16_45229_sprint-fix-bug-bao-mat-hieu-nang-php-web/). Nội dung lấy từ Redmine (`scripts/redmine_fetch.py`) ngày 2026-11-16.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45229 (lượt B) — T15: #41717 · #41529 · #41718` |
| Module / Màn hình | FA-020 サロン・面談予約: trang đặt lịch phía khách (`/mobile/calendar-salon/{hash}/{uCode}`) + API khung giờ `GET /ajax/mobile/calendar-salon/get-list-time-booking`; FA-013 友だちリスト: xoá bạn bè đã chặn; lệnh định kỳ `recover:payment_univapay_timeout` (thanh toán UnivaPay của đơn salon). Studio: task **#560** (task cha), TC gắn `REQ-X-<ticket>`. |

## Mô tả bug (bản dịch tiếng Việt)

Cả 3 ticket do **check-exception AI** tự tạo từ exception bắn lên Chatwork room `SNSLineException` (production). Tracker `AI detect exception`, status `New`, không có assignee, không có journal của Dev.

### #41717 — Maximum execution time of # seconds exceeded (`Collection.php`) — Priority High

- **Phân loại:** `php_resource` — **Rủi ro:** medium — **Đánh giá source:** yes.
- **Số lần cảnh báo:** 1 — **Số user lỗi:** 0 — **Server:** `s.lmes.jp/` — **Lần đầu / cuối:** 2026-09-28 11:21 UTC.
- **Signature:** `Maximum execution time of # seconds exceeded … Illuminate/Support/Collection.#`
- **Đối chiếu source (AI):** serialize JsonResponse collection lớn; **nghi** `getListTimeLineBooking` @ `app/Services/.../CalendarSalonLineBookingService.php:2253-2271` (nạp toàn bộ `time_booking`, không phân trang).
- **Nguyên nhân (AI):** query nạp toàn bộ bản ghi rồi merge/group trong bộ nhớ → tràn 1GB khi dữ liệu lớn. Bug hiệu năng / thiếu phân trang.
- **Gợi ý sửa (AI):** phân trang / chunk / lazy collection cho query `time_booking`; tránh materialize cả tập rồi encode JSON.
- **Exception mẫu:** `Maximum execution time of 500 seconds exceeded … Collection.php892`.

### #41529 — Allowed memory size of # bytes exhausted (`JsonResponse.php`) — Priority High

- **Phân loại:** `php_resource` — **Rủi ro:** high — **Đánh giá source:** yes.
- **Số lần cảnh báo:** 10 — **Số user lỗi:** 0 — **Server:** `step.lme.jp/` — **Lần đầu / cuối:** 2026-09-25 03:14 → 03:20 UTC.
- **Signature:** `Allowed memory size of # bytes exhausted (tried to allocate # bytes) … Illuminate/Http/JsonResponse.#`
- **Đối chiếu source (AI):** giống #41717 — nghi `getListTimeLineBooking` nạp toàn bộ `time_booking`.
- **Exception mẫu:** `Allowed memory size of 1073741824 bytes exhausted (tried to allocate 561590272 bytes) … JsonResponse.php71` (1 GB, cấp thêm 561 MB).

### #41718 — Packets out of order. Expected # received # (SQL đọc `calendar_salon_line_booking`) — Priority Low

- **Phân loại:** `uncategorized` — **Rủi ro:** low.
- **Số lần cảnh báo:** 4 (+1 nhóm gộp) — **Số user lỗi:** 0 — **Server:** `step.lme.jp/` — **Lần đầu / cuối:** 2026-09-28 11:40 → 2026-09-29 03:18 UTC.
- **Signature:** `Packets out of order. Expected # received #. Packet size=? (SQL: …) … Illuminate/Database/Connection.#`
- **Exception mẫu 1:** `Packets out of order. Expected 1 received 53. Packet size=5 (SQL: select * from calendar_salon_line_booking where line_user_id = … and bot_id = … and deleted_at is null) … Connection.php664`
- **Exception mẫu 2** (journal #139169, AI gộp vì cùng nguyên nhân): cùng lỗi ở `select * from calendar_salon_line_booking where status_webhook in (3, 4) and charge_id is not null and created_at < '2026-09-28 20:30:03' and deleted_at is null`.
- AI **không** đưa ra nguyên nhân / gợi ý sửa cho ticket này.

## Steps to reproduce

<!-- Ticket AI không có bước tái hiện. Bước dưới suy từ exception mẫu + requirement Studio REQ-X-41717 / 41529 / 41718. -->

1. **#41717 / #41529**: lịch salon có nhiều nhân viên × nhiều ngày ca và nhiều đơn → khách mở trang đặt lịch (tuần / tháng / danh sách) hoặc bấm 「予約確定」; hoặc gọi API khung giờ với khoảng ngày dài.
2. **#41718 (mẫu 1)**: admin xoá bạn bè đã chặn (từng người / hàng loạt) mà bạn bè đó có đơn salon.
3. **#41718 (mẫu 2)**: lệnh `recover:payment_univapay_timeout` (chạy mỗi 5 phút) đọc đơn salon chờ webhook thanh toán (`status_webhook` 3 / 4, có `charge_id`, tạo quá 15 phút).

## Expected result

- Trang / API khung giờ salon trả kết quả trong giới hạn thời gian + bộ nhớ của PHP, khung giờ đúng; khoảng ngày bất thường bị từ chối bằng 4xx, không 500.
- Đặt lịch trên lịch dữ liệu lớn lưu được đơn.
- Xoá bạn bè đã chặn và lệnh khôi phục thanh toán quá hạn chạy không lỗi giao thức DB.
- Sửa nguyên nhân, không chỉ bọc try/catch (yêu cầu chung của nhóm T15).

## Actual result

- Production: request bị kill khi quá 500 giây (#41717); tiến trình PHP vượt 1 GB khi encode JSON (#41529); `QueryException: Packets out of order` khi đọc `calendar_salon_line_booking` (#41718).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — exception mẫu nằm ngay trong description ticket (không có file đính kèm). Chi tiết nhóm lỗi #41718: dashboard check-exception `bug=df117cf937`.

## Ghi chú thêm của Leader

- ⚠️ **Dev không có commit riêng cho cả 3 ticket** (Studio requirement `REQ-X-41718`: *"Nhánh test KHÔNG có commit riêng cho #41718"*; ghi chú NEW-701 / 702 / 703 / 762 / 763: *"Nhánh test KHÔNG có commit riêng cho ticket này (ticket AI chỉ 'nghi' getListTimeLineBooking); T16 #41345 đã viết lại truy vấn khung giờ tuần"*). Journal handoff T15 của ticket cha chỉ nói tới #45186 (bộ lọc thiếu tham số) và #42266 (refresh token MCP).
- Thay đổi thực tế chạm luồng của #41717 / #41529 đến từ **nhóm khác**: T16 #41345 (viết lại truy vấn khung giờ tuần, commit `229f1a4788`) + 2 bug Studio phát sinh khi test lượt này (đều `Closed` 2026-11-07):
  - **#45409** — khoảng 1 năm / 10 năm trả 500 sau ~30 giây ⇒ sau fix: **422 「表示期間は31日以内で指定してください。」** (quy tắc mới: khoảng hiển thị ≤ 31 ngày).
  - **#45410** — calendarId không tồn tại / thiếu / ngày sai trả 500 ⇒ sau fix: 404 「カレンダーが見つかりません。」 · 422 「パラメータが不正です。」, không ghi rác `calendar_salon_setting_time_free`.
- Môi trường đã chạy trên Studio: **100% `local`**, dữ liệu seed 30 nhân viên × 90 ngày ca (≈ 2.700 dòng `calendar_salon_time_booking`) + ≈ 20.000 đơn. Quy mô dữ liệu thật của 2 bot gặp lỗi chưa có.

## Dữ liệu định danh ca lỗi

| Ticket | Server | User admin (id) | BotId | Thời điểm (UTC) | Ghi chú |
|---|---|---|---|---|---|
| #41717 | `s.lmes.jp` | 114949 | 153361 | 2026-09-28 11:21 | timeout 500 s |
| #41529 | `step.lme.jp` | 177888 | 52318 | 2026-09-25 03:14 → 03:20 | 10 lần, memory 1 GB |
| #41718 (mẫu 1) | `step.lme.jp` | 74366 | 108684 | 2026-09-28 → 29 | `line_user_id = 62856142` |
| #41718 (mẫu 2) | `step.lme.jp` | — | — | 2026-09-28 11:45 | lệnh `recover:payment_univapay_timeout` |

<!-- Email user admin có trong ticket gốc — không chép sang đây; tra Redmine khi cần. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #139169 — ai-exception detect-bug — 2026-09-29:** (ticket #41718)
```
*[check-exception AI] Gộp thêm một nhóm exception CÙNG NGUYÊN NHÂN vào ticket này* (người review xác nhận, không tạo ticket mới).
*Phân loại:* uncategorized — *Rủi ro:* low
*Số lần cảnh báo:* 1 — *Số user lỗi:* 0
*Room:* SNSLineException — *Server:* step.lme.jp/
*Lần đầu:* 2026-09-28 11:45 UTC — *Lần cuối:* 2026-09-28 11:45 UTC
Signature: Packets out of order. Expected # received #. Packet size= ? (SQL:.. and `..` is not null and `..` < #-#-# #:#:# and `..`.`..` is null)
Exception mẫu: select * from `calendar_salon_line_booking` where `status_webhook` in (3, 4) and `charge_id` is not null and `created_at` < 2026-09-28 20:30:03 and `calendar_salon_line_booking`.`deleted_at` is null
```
