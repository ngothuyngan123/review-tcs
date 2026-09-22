# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41090 — Journal #137010 (**AI LME Fix bug** — báo cáo AI AUTO-FIXBUG, không phải Dev người viết).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (AI auto-fixbug) · assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `sns-line` commit `9cbd4412ee` (không có link PR) |
| Branch | `ai_fixbug_41090` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-18 |
| Auto-filled | 2026-09-18 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn đặt lịch salon ở chế độ ưu tiên hiển thị theo tháng không đặt lại cờ "không có lịch trống" khi đổi nhân viên. Chọn nhân viên không có ca làm thì cờ bật lên và toàn bộ khung lịch bị gỡ khỏi trang; chọn tiếp nhân viên có ca làm, hàm dựng lịch tháng không tìm thấy khung lịch (đang bị ẩn) nên lỗi giữa chừng, kéo theo lệnh nạp dữ liệu lịch ngay sau đó không chạy. Cờ không bao giờ được cập nhật lại nên màn hình kẹt ở thông báo không có lịch đặt được. Chế độ hiển thị theo tuần không dính vì nó chỉ nạp dữ liệu bằng ajax, không phải dựng lại khung lịch.

## 2. Cách fix

Đặt lại cờ không-có-lịch-trống về mặc định ngay trước khi dựng lại lịch tháng ở cả 5 lối vào bước chọn ngày (chọn nhân viên, vào bước đặt lịch khi không dùng khoá học, đặt lại từ lịch sử đặt, chọn xong khoá học, đổi tab tuần/tháng) để khung lịch kịp hiện lại trước khi khởi tạo. Thêm chốt an toàn: hàm dựng lịch dừng sớm khi khung lịch chưa có trên trang, và phần cập nhật sự kiện lịch chịu được trường hợp lịch chưa dựng, nhờ đó trạng thái màn hình vẫn được cập nhật theo dữ liệu mới. Quét ngang: các màn lịch khác (đặt lịch bài học, quản lý đặt chỗ) giữ khung lịch trong trang nên không dính lỗi này.

**Tự review (AI) — rủi ro / lưu ý khi test (nguyên văn):**
- Sau khi tắt cờ, thông báo không có lịch biến mất trong lúc chờ phản hồi rồi hiện lại nếu nhân viên mới cũng không có ca — chớp nhẹ, đúng với hành vi của lần chọn nhân viên đầu tiên
- Chốt an toàn dừng sớm khi chưa có khung lịch giữ lại đối tượng lịch cũ đã bị gỡ khỏi trang; đường này chỉ còn là dự phòng vì cờ đã được tắt trước đó

**Verify (nguyên văn):** Mức: lint · `node --check public/js/calendar_salon/booking.js`: OK · `git diff --stat origin/release_step_20260827...ai_fixbug_41090`: 1 file, +23/-1 · Bằng chứng: `booking_create_step2.blade.php:34` — khung lịch nằm trong panel `v-if="!noScheduleAvailable"`, nên khi cờ bật thì thẻ lịch (dòng 147) và nút hôm nay bị gỡ khỏi trang; `booking.js initializeFullCalendar()` lấy phần tử theo id rồi dựng ngay: phần tử null thì hàm lỗi, lệnh `initDataBooking()` đứng sau trong cùng `nextTick` không chạy; Chế độ tuần tự khỏi được vì `getListTimeBooking` chỉ gọi ajax rồi gán lại cờ — khớp với mô tả khách. **Không tái hiện trên dev** (không có dữ liệu lịch salon + ca làm nhân viên phù hợp trên DB dev).

**Recover data:** ✔ Không cần recover data.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `selectStaff` — public/js/calendar_salon/booking.js | Reset cờ trước khi dựng lịch tháng | Lối vào: chọn nhân viên |
| 2 | `showScreenBookingStep1` — public/js/calendar_salon/booking.js | Reset cờ | Lối vào: vào bước đặt lịch khi không dùng khoá học |
| 3 | `copyBookingStepTime` — public/js/calendar_salon/booking.js | Reset cờ | Lối vào: đặt lại từ lịch sử đặt |
| 4 | `nextStep2` — public/js/calendar_salon/booking.js | Reset cờ | Lối vào: chọn xong khoá học |
| 5 | `displayTypeCalendar` + `changeDisplayCalendar` — public/js/calendar_salon/booking.js | Reset cờ | Lối vào: đổi tab tuần/tháng |
| 6 | `initDataBooking` — public/js/calendar_salon/booking.js | Chịu được trường hợp lịch chưa dựng | Cập nhật sự kiện lịch |
| 7 | `getListTimeBooking` — public/js/calendar_salon/booking.js | (đã check) | Nạp dữ liệu chế độ tuần |
| 8 | `initializeFullCalendar` — public/js/calendar_salon/booking.js | Dừng sớm khi khung lịch chưa có trên trang | Chốt an toàn |
| 9 | `CalendarSalonController::initDataBooking` — app/Http/Controllers/Mobile/CalendarSalonController.php | Chỉ đọc | — |
| 10 | `CalendarSalonController::getListTimeBookingWeek` — app/Http/Controllers/Mobile/CalendarSalonController.php | Chỉ đọc | — |
| 11 | `booking_create_step2.blade.php` + `no-schedule-available.blade.php` — resources/views/basic/calendar_salon/bookings | Chỉ đọc | — |

> Cột "Thay đổi" / "Lý do" suy từ mục 2 (Dev chỉ liệt kê tên function dạng plain list). Leader verify lại với diff thật.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev chỉ ghi **file thay đổi**: `public/js/calendar_salon/booking.js`. Tách F* theo function ở mục 3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `selectStaff` | public/js/calendar_salon/booking.js | Direct | Lối vào chọn nhân viên — đường bug gốc |
| F2 | `showScreenBookingStep1` | public/js/calendar_salon/booking.js | Direct | Không dùng khoá học |
| F3 | `copyBookingStepTime` | public/js/calendar_salon/booking.js | Direct | 「同じ内容で予約」 |
| F4 | `nextStep2` | public/js/calendar_salon/booking.js | Direct | Chọn xong khoá học |
| F5 | `displayTypeCalendar` / `changeDisplayCalendar` | public/js/calendar_salon/booking.js | Direct | Đổi tab 週/月 |
| F6 | `initializeFullCalendar` | public/js/calendar_salon/booking.js | Direct | Chốt an toàn dừng sớm |
| F7 | `initDataBooking` | public/js/calendar_salon/booking.js | Direct | Cập nhật sự kiện khi lịch chưa dựng |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Dev ghi "Không có"; không cần recover data |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — màn đặt lịch salon phía khách: hiện lại lịch tháng khi đổi nhân viên, thông báo không có lịch chỉ còn hiện đúng với nhân viên thật sự không có ca | F1–F7 | `<Dev không ghi mức>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
