# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41174 — [AI][Performance] GET /basic/calendar-salon/{id}/get-list-booking chậm max 85s (95 lần/24h)` |
| Module / Màn hình | Salon Booking (FA-020) — màn quản lý lịch salon → danh sách đặt lịch, tab 「本日の予約」 (đặt lịch hôm nay) / 「新着の予約」 (đặt lịch mới). Endpoint `GET /basic/calendar-salon/{id}/get-list-booking` |

## Mô tả bug (bản dịch tiếng Việt)

> Ticket **tự tạo bởi check-performance AI** (từ report request chậm bắn lên Chatwork room 417532006). Đây là ticket **performance**, không phải bug sai chức năng.

**Endpoint:** `GET /basic/calendar-salon/{id}/get-list-booking`

**Mức:** high — xếp theo độ chậm: max 43s trong kỳ (>30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 74

**Số lần chậm 24h:** 95 (kỳ trước 126, 1h qua 11) — xu hướng flat

**Thời gian:** max 85s · p95 17s · trung bình 8.38s · median 7s

**Phân bố:** ≥15s SUPPERSLOW 37 · 10–15s VERYSLOW 142 · 5–10s SLOWLV1 873

**User bị ảnh hưởng:** 13 (tổng 40)

**Server:** step.lme.jp, s.lmes.jp — **BotId:** 142545, 131127, 151937, 88667, 106869, 35547, 115808, 144016, 27981, 60002

**Lần đầu:** 2026-09-14 02:07 UTC — **Lần cuối:** 2026-09-21 04:59 UTC

**Lịch sử dài hạn:** tổng 1052 lần chậm trong 8 ngày, đỉnh 210 lần/24h, chậm nhất 85s, từ 2026-09-14 02:07 UTC

### Vì sao ưu tiên này

- Độ chậm: p95 17s — SUPPERSLOW (+30 điểm)
- Tần suất: 95 lần/24h (+18 điểm)
- User ảnh hưởng: 13 user bị chậm (+14 điểm)
- Độ mới: Vừa xảy ra trong 1h qua (+12 điểm)
- Xu hướng: Tương đương 24h trước (+0 điểm)

### URL mẫu

- `/basic/calendar-salon/8057/get-list-booking?page=1&tab_query=new_booking&per_page=50&date_booking=2026-09-14`
- `/basic/calendar-salon/4333/get-list-booking?page=1&tab_query=new_booking&per_page=50&date_booking=2026-09-14`
- `/basic/calendar-salon/11374/get-list-booking?page=1&tab_query=new_booking&per_page=50&date_booking=2026-09-14`
- `/basic/calendar-salon/15/get-list-booking?page=1&tab_query=new_booking&per_page=100&date_booking=2026-09-14`
- `/basic/calendar-salon/5870/get-list-booking?page=1&tab_query=new_booking&per_page=50&date_booking=2026-09-14`

**Query param gặp:** `date_booking`, `page`, `per_page`, `tab_query`

### Các lần CHẬM NHẤT đã ghi nhận

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 85 | 2026-09-19 05:04 VN | SUPPERSLOW | 72565 | `/basic/calendar-salon/5870/get-list-booking?page=1&tab_query=new_booking&per_page=50&date_booking=2026-09-19` |
| 59 | 2026-09-20 04:43 VN | SUPPERSLOW | 72565 | `/basic/calendar-salon/5870/...&date_booking=2026-09-20` |
| 55 | 2026-09-17 14:29 VN | SUPPERSLOW | 72565 | `/basic/calendar-salon/5870/...&date_booking=2026-09-17` |
| 51 | 2026-09-16 04:31 VN | SUPPERSLOW | 72565 | `/basic/calendar-salon/5870/...&date_booking=2026-09-16` |
| 43 | 2026-09-21 08:49 VN | SUPPERSLOW | 113368 | `/basic/calendar-salon/11322/...&date_booking=2026-09-21` |
| 33 | 2026-09-21 04:06 VN | SUPPERSLOW | 72565 | `/basic/calendar-salon/5870/...&date_booking=2026-09-21` |
| 31 | 2026-09-18 05:58 VN | SUPPERSLOW | 15116 | `/basic/calendar-salon/8410/...&date_booking=2026-09-18` |
| 30 | 2026-09-20 06:32 VN | SUPPERSLOW | 32244 | `/basic/calendar-salon/6186/...&date_booking=2026-09-20` |
| 25 | 2026-09-16 14:00 VN | SUPPERSLOW | 18319 | `/basic/calendar-salon/6209/...&date_booking=2026-09-16` |
| 24 | 2026-09-21 09:29 VN | SUPPERSLOW | 32244 | `/basic/calendar-salon/6186/...&date_booking=2026-09-21` |
| 24 | 2026-09-14 09:07 VN | SUPPERSLOW | 104867 | `/basic/calendar-salon/8057/...&date_booking=2026-09-14` |
| 21 | 2026-09-18 23:38 VN | SUPPERSLOW | 110545 | `/basic/calendar-salon/11374/...&date_booking=2026-09-19` |
| 21 | 2026-09-18 13:33 VN | SUPPERSLOW | 72565 | `/basic/calendar-salon/5870/...&date_booking=2026-09-18` |
| 21 | 2026-09-15 08:44 VN | SUPPERSLOW | 49841 | `/basic/calendar-salon/719/...&date_booking=2026-09-15` |
| 19 | 2026-09-17 10:40 VN | SUPPERSLOW | 18319 | `/basic/calendar-salon/6209/...&date_booking=2026-09-17` |

### Nguồn cảnh báo trong source

Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket do AI detect performance tự tạo từ log request chậm. -->

## Expected result

<!-- trống — Redmine không có -->

## Actual result

<!-- trống — Redmine không có -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #41174 KHÔNG có attachment. Số liệu chậm nằm ngay trong description (bảng "Các lần CHẬM NHẤT đã ghi nhận"). -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — root cause đã được Dev (AI auto-fixbug) confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix** (2 index + viết lại 2 điều kiện lọc ngày) + **regression impact**, KHÔNG phải tái hiện lại con số 85s.
- **Môi trường phát hiện:** production (`step.lme.jp`, `s.lmes.jp`).
- **Tần suất:** KHÔNG phải 100% — độ chậm phụ thuộc lượng dữ liệu tích luỹ + tải + cache nguội (median 7s, đỉnh 85s). Trong 24h có 95 lần vượt ngưỡng.
- **Endpoint chạy 2 nhánh theo `tab_query`**: `today_booking` (tab 「本日の予約」) và `new_booking` (tab 「新着の予約」). Toàn bộ URL mẫu ghi nhận chậm đều là `tab_query=new_booking`.
- **Màn KHÔNG có ô chọn ngày** — giao diện tự gửi `date_booking` = ngày hiện tại; muốn test ngày khác phải gọi endpoint trực tiếp.
- ⚠️ **Dev CHƯA chạy được EXPLAIN** (MySQL dev `host.docker.internal:3306` + web `:8000` đều Connection refused lúc xử lý) → kết luận "bảng chưa có index nào ngoài PRIMARY" dựa trên grep toàn bộ `database/migrations` + tiền lệ ticket #38446, **chưa có bằng chứng EXPLAIN thực tế**.
- ⚠️ **Lưu ý vận hành:** `ALTER TABLE` thêm index trên bảng lớn chạy lâu → deploy migration vào giờ thấp điểm. Nếu DBA đã tự thêm index tương đương dưới tên khác thì sẽ có index trùng lặp → kiểm `SHOW INDEX` trước khi chạy migration.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `142545, 131127, 151937, 88667, 106869, 35547, 115808, 144016, 27981, 60002` |
| Lịch salon chậm nhiều nhất | `calendar_salon_id = 5870` (5/15 lần chậm nhất, gồm cả đỉnh 85s) — khác: `8057`, `4333`, `11374`, `15`, `11322`, `8410`, `6186`, `6209`, `719` |
| User bị ảnh hưởng | `72565` (nhiều nhất), `113368`, `15116`, `32244`, `18319`, `104867`, `110545`, `49841` |
| Đối tượng cấu hình | Bảng `calendar_salon_line_booking` — theo Dev chỉ có `PRIMARY(id)`, chưa có index phụ |
| Thời điểm lỗi | Đỉnh 85s: `2026-09-19 05:04 VN` · Lần cuối ghi nhận: `2026-09-21 04:59 UTC` |
| Đối chứng | Request cùng endpoint trên lịch salon ít đơn (< 5s, không vào ngưỡng SLOWLV1) |
| Server | `step.lme.jp`, `s.lmes.jp` (production) |

## Journal / note từ Redmine (nguyên văn)

**Journal #137408 — AI LME Fix bug — 2026-09-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Bảng đặt lịch salon dùng chung cho toàn hệ thống nhưng chưa có chỉ mục nào ngoài khoá chính, nên mỗi lần mở danh sách đặt lịch của một lịch salon, cơ sở dữ liệu phải quét toàn bộ bảng — hai lần cho mỗi lần gọi (một lần đếm tổng để phân trang, một lần lấy dữ liệu) — rồi sắp xếp thủ công. Điều kiện lọc ngày lại bọc cột trong hàm DATE() nên kể cả khi có chỉ mục cũng không dùng được. Bảng càng tích luỹ dữ liệu thì thời gian càng tăng, giải thích được mức chậm dao động lớn (trung vị 7 giây, đỉnh 85 giây tuỳ lúc bộ nhớ đệm nguội và tải cao).

■ 2. CÁCH FIX
Thêm migration tạo 2 chỉ mục tổng hợp cho bảng đặt lịch salon: (lịch, thời điểm khách cập nhật) phục vụ tab Đặt lịch mới, và (lịch, ngày hẹn, giờ bắt đầu) phục vụ tab Đặt lịch hôm nay; chỉ mục này cũng giúp mọi truy vấn khác lọc theo lịch trên bảng. Viết lại 2 điều kiện lọc ngày trong truy vấn danh sách để so sánh trực tiếp trên cột thay vì bọc hàm DATE() (so sánh thẳng ngày hẹn; đổi khoảng 7 ngày của thời điểm cập nhật thành khoảng thời gian đầu–cuối ngày), nhờ đó dùng được chỉ mục và bỏ được bước sắp xếp thủ công. Kết quả trả về, thứ tự và phân trang giữ nguyên — đã đối chiếu câu SQL sinh ra trước/sau.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
CalendarSalonController::getListBooking (app/Http/Controllers/Basic/CalendarSalonController.php:734)
CalendarSalonLineBookingService::getListBooking (app/Services/CalendarSalon/CalendarSalonLineBookingService.php:129)
CalendarSalonLineBookingRepository::getListBooking (app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php:32)
CalendarSalonLineBookingService::getLineBookingName (app/Services/CalendarSalon/CalendarSalonLineBookingService.php:3328)
getDataBookingList (public/js/calendar_salon/calendar_detail.js:1714)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php
   - database/migrations/2026_09_21_100000_add_index_booking_list_to_calendar_salon_line_booking_table.php
 • 4.2 Data ảnh hưởng:
   - calendar_salon_line_booking — KHÔNG đổi dữ liệu, chỉ thêm 2 chỉ mục idx_cslb_salon_user_update (calendar_salon_id, user_update_time) và idx_cslb_salon_date_start (calendar_salon_id, date_booking, start_time)
   - Lưu ý vận hành: ALTER TABLE thêm chỉ mục trên bảng lớn — MySQL 5.7+ thêm chỉ mục phụ theo kiểu ONLINE (không khoá ghi) nhưng vẫn chạy lâu, nên chạy migration vào giờ thấp điểm
   - Chi phí ghi: mỗi lần thêm/sửa đặt lịch salon phải cập nhật thêm 2 chỉ mục — không đáng kể so với lợi ích đọc
   - Không cần recover/migrate dữ liệu
 • 4.3 Tính năng liên quan:
   - Salon Booking (FA-020) — màn quản lý lịch salon, danh sách đặt lịch tab Đặt lịch mới / Đặt lịch hôm nay: nhanh hơn, nội dung hiển thị giữ nguyên
   - Salon Booking (FA-020) — các truy vấn khác trên cùng bảng lọc theo lịch salon (xem theo tuần/tháng, danh sách đã xoá, xuất CSV, kiểm tra trùng giờ) được hưởng chỉ mục mới, không đổi logic

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php: OK; php -l database/migrations/2026_09_21_100000_add_index_booking_list_to_calendar_salon_line_booking_table.php: OK; Boot Laravel (không cần DB) + dump toSql/bindings cho cả 2 tab, so câu SQL cũ vs mới: chỉ khác phần điều kiện ngày, cùng tập kết quả; Resolve CalendarSalonLineBookingRepositoryInterface qua container: OK
   Bằng chứng: SQL cũ tab Đặt lịch hôm nay: date(date_booking) = '2026-09-14' → mới: date_booking = '2026-09-14' (cột kiểu DATE nên tương đương tuyệt đối); SQL cũ tab Đặt lịch mới: DATE(user_update_time) between '2026-09-14' and '2026-09-21' → mới: user_update_time >= '2026-09-14 00:00:00' and <= '2026-09-21 23:59:59' (cột timestamp độ chính xác giây; NULL vẫn bị loại ở cả hai); Migration của repo: không có migration nào tạo chỉ mục cho calendar_salon_line_booking (grep toàn bộ database/migrations) ⇒ bảng chỉ có PRIMARY(id); CHƯA chạy được EXPLAIN: MySQL dev host.docker.internal:3306 và web :8000 đều Connection refused tại thời điểm xử lý (dev stack trên host đang tắt)

■ TỰ REVIEW (AI)
Thay đổi tối thiểu, đúng điểm nghẽn: chỉ mục cho bảng chưa có chỉ mục nào + bỏ hàm DATE() bọc cột để điều kiện dùng được chỉ mục. Không đổi input/output/thứ tự/phân trang của endpoint; đã đối chiếu SQL sinh ra trước-sau để chắc chắn cùng tập kết quả. Không có N+1 trong vòng lặp PHP của service (chỉ định dạng dữ liệu), không có gọi API bên thứ 3 trong luồng này.
 • Rủi ro / lưu ý khi test:
   - Chưa chạy được EXPLAIN vì MySQL dev đang tắt — kết luận thiếu chỉ mục dựa trên toàn bộ migration của repo (không có migration index nào cho bảng này) và tiền lệ #38446 (bảng salon anh em cũng chỉ có PRIMARY)
   - ALTER TABLE thêm chỉ mục trên bảng lớn chạy lâu ⇒ nên deploy migration vào giờ thấp điểm
   - Nếu DBA đã tự thêm chỉ mục tương đương trên production dưới tên khác thì sẽ có chỉ mục trùng lặp (không gây lỗi, chỉ tốn dung lượng) — kiểm SHOW INDEX trước khi chạy migration

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41174 (nhánh gốc release_step_20260827, commit 2a894b8bc3, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 10 phút 39 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=19be0cc6-02da-4129-bd47-aee2220b2ca1
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41174
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
