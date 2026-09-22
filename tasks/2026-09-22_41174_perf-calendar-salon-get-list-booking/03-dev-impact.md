# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `2a894b8bc3` (2 file) — Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41174 |
| Branch | `ai_small_41174` (repo `sns-line`, nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | `2026-09-21` (Journal #137408) |
| Auto-filled | `2026-09-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Bảng đặt lịch salon dùng chung cho toàn hệ thống nhưng chưa có chỉ mục nào ngoài khoá chính, nên mỗi lần mở danh sách đặt lịch của một lịch salon, cơ sở dữ liệu phải quét toàn bộ bảng — hai lần cho mỗi lần gọi (một lần đếm tổng để phân trang, một lần lấy dữ liệu) — rồi sắp xếp thủ công. Điều kiện lọc ngày lại bọc cột trong hàm `DATE()` nên kể cả khi có chỉ mục cũng không dùng được. Bảng càng tích luỹ dữ liệu thì thời gian càng tăng, giải thích được mức chậm dao động lớn (trung vị 7 giây, đỉnh 85 giây tuỳ lúc bộ nhớ đệm nguội và tải cao).

## 2. Cách fix

Thêm migration tạo 2 chỉ mục tổng hợp cho bảng đặt lịch salon: `(lịch, thời điểm khách cập nhật)` phục vụ tab 「新着の予約」 (Đặt lịch mới), và `(lịch, ngày hẹn, giờ bắt đầu)` phục vụ tab 「本日の予約」 (Đặt lịch hôm nay); chỉ mục này cũng giúp mọi truy vấn khác lọc theo lịch trên bảng.

Viết lại 2 điều kiện lọc ngày trong truy vấn danh sách để so sánh trực tiếp trên cột thay vì bọc hàm `DATE()` (so sánh thẳng ngày hẹn; đổi khoảng 7 ngày của thời điểm cập nhật thành khoảng thời gian đầu–cuối ngày), nhờ đó dùng được chỉ mục và bỏ được bước sắp xếp thủ công. Kết quả trả về, thứ tự và phân trang giữ nguyên — đã đối chiếu câu SQL sinh ra trước/sau.

**SQL trước / sau (Dev dump toSql):**

| Tab | SQL cũ | SQL mới |
|---|---|---|
| 「本日の予約」 | `date(date_booking) = '2026-09-14'` | `date_booking = '2026-09-14'` (cột kiểu DATE ⇒ tương đương tuyệt đối) |
| 「新着の予約」 | `DATE(user_update_time) between '2026-09-14' and '2026-09-21'` | `user_update_time >= '2026-09-14 00:00:00' and <= '2026-09-21 23:59:59'` (cột timestamp độ chính xác giây; NULL vẫn bị loại ở cả hai) |

**Mức verify của Dev:** `lint` — `php -l` 2 file OK; boot Laravel (không cần DB) + dump `toSql`/bindings cho cả 2 tab; resolve `CalendarSalonLineBookingRepositoryInterface` qua container OK.

⚠️ **Dev CHƯA chạy được EXPLAIN** — MySQL dev `host.docker.internal:3306` và web `:8000` đều Connection refused tại thời điểm xử lý.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonController::getListBooking` — `app/Http/Controllers/Basic/CalendarSalonController.php:734` | Không sửa | Controller nhận request của endpoint chậm, chỉ gọi service |
| 2 | `CalendarSalonLineBookingService::getListBooking` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php:129` | Không sửa | Service gọi repository, chỉ format dữ liệu (Dev khẳng định không có N+1) |
| 3 | `CalendarSalonLineBookingRepository::getListBooking` — `app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php:32` | **ĐÃ SỬA** — viết lại 2 điều kiện lọc ngày, bỏ `DATE()` bọc cột | Đây là điểm nghẽn: điều kiện bọc `DATE()` không dùng được index |
| 4 | `CalendarSalonLineBookingService::getLineBookingName` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php:3328` | Không sửa | Function dùng chung trong luồng lấy tên khách của booking |
| 5 | `getDataBookingList` — `public/js/calendar_salon/calendar_detail.js:1714` | Không sửa | JS phía màn gọi endpoint, tự gửi `date_booking` = ngày hiện tại, `page=1`, `per_page` 50/100 |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev ghi mục 4.1 là **"File thay đổi"** (không phải list function). Bảng dưới là phần Leader chuẩn hoá lại theo tag `F*`, giữ nguyên nội dung Dev cung cấp.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarSalonLineBookingRepository::getListBooking` | `app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php` | Direct | File thay đổi #1. Viết lại 2 điều kiện lọc ngày (nhánh `today_booking` + nhánh `new_booking`), bỏ `DATE()`, bỏ bước sắp xếp thủ công |
| F2 | Migration thêm 2 index cho `calendar_salon_line_booking` | `database/migrations/2026_09_21_100000_add_index_booking_list_to_calendar_salon_line_booking_table.php` | Direct | File thay đổi #2 |
| F3 | `GET /basic/calendar-salon/{id}/get-list-booking` (endpoint trong ticket) | Controller `Basic/CalendarSalonController.php:734` → Service `:129` → Repository F1 | Indirect | Không sửa code, nhưng là endpoint tiêu thụ F1 — mọi thay đổi kết quả/thứ tự/phân trang lộ ra ở đây |
| F4 | Các truy vấn khác trên cùng bảng lọc theo `calendar_salon_id` | (nhiều nơi — Dev không liệt kê cụ thể) | Indirect | Chỉ hưởng lợi kế hoạch thực thi do index mới; Dev khẳng định không đổi logic |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_line_booking` — index `idx_cslb_salon_user_update (calendar_salon_id, user_update_time)` | MIGRATE (CREATE INDEX) | Phục vụ tab 「新着の予約」 |
| D2 | `calendar_salon_line_booking` — index `idx_cslb_salon_date_start (calendar_salon_id, date_booking, start_time)` | MIGRATE (CREATE INDEX) | Phục vụ tab 「本日の予約」 |
| D3 | `calendar_salon_line_booking` — **dữ liệu dòng** | KHÔNG đổi | Không cần recover / migrate dữ liệu |

**Lưu ý vận hành từ Dev:**
- `ALTER TABLE` thêm index trên bảng lớn — MySQL 5.7+ thêm index phụ theo kiểu ONLINE (không khoá ghi) nhưng vẫn chạy lâu ⇒ **chạy migration vào giờ thấp điểm**.
- Chi phí ghi: mỗi lần thêm/sửa đặt lịch salon phải cập nhật thêm 2 index — Dev đánh giá không đáng kể so với lợi ích đọc.
- Nếu DBA đã tự thêm index tương đương trên production dưới **tên khác** ⇒ sẽ có index trùng lặp (không gây lỗi, chỉ tốn dung lượng) — **kiểm `SHOW INDEX` trước khi chạy migration**.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — màn quản lý lịch salon, danh sách đặt lịch tab 「新着の予約」 / 「本日の予約」 | F1, F3, D1, D2 | High — Dev nói "nhanh hơn, nội dung hiển thị giữ nguyên", nhưng đây là 2 nhánh điều kiện vừa bị viết lại ⇒ phải verify tập kết quả + thứ tự + phân trang |
| T2 | Salon Booking (FA-020) — các truy vấn khác trên cùng bảng lọc theo lịch salon: xem theo tuần/tháng, danh sách đã xoá, xuất CSV, kiểm tra trùng giờ | F4, D1, D2 | Medium — hưởng index mới, Dev nói không đổi logic (bảng dùng chung ⇒ đổi execution plan) |

**BUG (root cause / cách fix):** thiếu index trên bảng dùng chung + điều kiện lọc bọc `DATE()` khiến index không dùng được ⇒ full table scan 2 lần/request + filesort. Fix = 2 composite index + viết lại 2 điều kiện lọc ngày để sargable.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm nghi vấn Leader cần chốt với Dev (phát hiện khi auto-fill)

1. **Mục 4.1 Dev ghi là "File thay đổi", không phải list function bị ảnh hưởng** — F4 ("các truy vấn khác lọc theo `calendar_salon_id`") **không được liệt kê cụ thể** ⇒ không có danh sách caller để rà regression theo từng điểm. Bảng là bảng dùng chung ⇒ cần Dev kê tên method/màn cụ thể.
2. **Chưa có bằng chứng EXPLAIN** — cả kết luận "bảng chỉ có PRIMARY(id)" và "sau fix dùng được index" đều chưa được kiểm chứng trên DB thật. Cần verify bằng `SHOW INDEX` + `EXPLAIN` khi test.
3. **Nhánh API app mobile** — ticket ghi cảnh báo `MobileAuthenticate` cũng bắn slow request, nhưng mục 4 không nói gì về endpoint danh sách booking của app quản trị di động (`app/Http/Controllers/Api/CalendarSalonController.php`). Cần xác nhận nhánh này có dùng `CalendarSalonLineBookingRepository::getListBooking` đã sửa hay tự dựng query riêng.
