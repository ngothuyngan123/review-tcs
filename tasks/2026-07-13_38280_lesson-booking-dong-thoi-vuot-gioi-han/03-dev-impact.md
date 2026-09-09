# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #38280 journal **#124653** (AI LME Fix bug, 2026-07-02 10:56) — **bản MỚI NHẤT, thay thế** journal #124643 (10:28, chỉ cover Lesson).
> Journal #124643 = fix v1 (chỉ Lesson, commit `c2cb945fa4`). Journal #124653 = fix v2 (Lesson + Salon, commit `41cc44c4ce`). **File này lấy theo v2.**

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | `41cc44c4ce` (2 file) — không có link PR trong Redmine |
| Branch | `ai_fixbug_38280` (nhánh gốc `release_step_20260623`), repo `sns-line` — đã push |
| Ngày submit đánh giá | `2026-07-02` |
| Auto-filled | `2026-07-13 by /new-task` |
| Phiên xử lý AI | https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=2d2a45f3-0a83-47c1-a54f-eae27e32262e |
| Mức verify của Dev | `lint` (php -l + thử nghiệm mutex/query trên dev DB) — **CHƯA có test tích hợp race thật** |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn:

Luồng đặt lịch học MIỄN PHÍ (không thanh toán) trong `order()` kiểm tra còn chỗ trống (đọc `total_booking`) rồi mới tạo bản ghi đặt chỗ và đếm lại — **không khóa giữa 2 bước**. Hai người bấm đăng ký đồng thời cùng đọc thấy còn 1 chỗ nên cả hai cùng tạo được, vượt giới hạn 1 khung/ngày. Luồng CÓ thanh toán không dính lỗi vì đã dùng cập nhật số chỗ có điều kiện nguyên tử (`checkValidSlot`).

## 2. Cách fix

> Nguyên văn:

Chống đặt trùng khi 2 người đặt ĐỒNG THỜI cho cả **Lesson (FA-019)** và **Salon (FA-020)**. Cơ chế **arbiter khử trùng cùng-giây**: sau khi tạo booking APPROVE mới, nếu có booking APPROVE khác cùng khung tạo **CÙNG GIÂY** id nhỏ hơn VÀ tổng chiếm chỗ tạo trước đã đủ giới hạn → bản mới **tự xóa** (giữ bản id nhỏ), báo lỗi dừng.

- **LESSON**: áp cho luồng đặt **miễn phí** `order()`; luồng **THANH TOÁN** lesson đã an toàn sẵn nhờ `checkValidSlot` (UPDATE nguyên tử có điều kiện) nên không cần thêm.
- **SALON**: áp cho **CẢ luồng miễn phí `order()` LẪN luồng thanh toán (`createOrderPayment`, chạy trước khi charge)** — gom vào 1 helper `rejectDuplicateSalonBooking` dùng chung; giới hạn đọc từ `calendar_salon_setting_limit_booking` (theo lịch/nhân viên), **fail-safe bỏ qua** nếu không xác định chắc chắn.
- **KHÔNG dùng named lock** (theo quyết định review).

Trọng tài theo `id` auto-increment: bản tạo trước (id nhỏ) được giữ, bản dư (id lớn) tự xóa + báo lỗi.

> ⚠️ **MÂU THUẪN trong report của Dev (Leader cần confirm)**: mục 2 nói Salon **có** áp arbiter cho luồng thanh toán (`createOrderPayment`), nhưng mục "Rủi ro / lưu ý khi test" lại ghi *"Salon luồng THANH TOÁN (paymentStripe/paymentUnivapay → createOrderPayment) CHƯA áp arbiter — chỉ mới luồng free order()"*. Phải hỏi Dev chốt trước khi kết luận coverage cho Salon paid flow.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `order` — `app/Http/Controllers/Mobile/CalendarController.php` | Bọc khóa + arbiter theo `id` sau khi tạo | Luồng đặt Lesson miễn phí — nơi phát sinh race |
| 2 | `checkCanBooking` — `app/Http/Controllers/Mobile/CalendarController.php` | Không sửa logic; nằm trong vùng khóa | Kiểm tra giới hạn chỗ/khách (chỉ đọc) |
| 3 | `countTotalBookingStatus` — `app/Services/CalendarManagement/CalendarCourseBookingService.php` | Gọi lại sau khi xóa booking dư | Đếm lại `total_booking` từ bản ghi thực |
| 4 | `checkValidSlot` — `app/Http/Controllers/Mobile/CalendarController.php` | **KHÔNG sửa** | Luồng thanh toán Lesson — đã an toàn nhờ UPDATE nguyên tử |
| 5 | `acquireReceptionBookingLock` / `releaseReceptionBookingLock` — `app/Http/Controllers/Mobile/CalendarController.php` | Helper khóa khung giờ **mới** | ⚠️ Report ghi "KHÔNG dùng named lock" nhưng vẫn liệt kê helper khóa — Leader hỏi Dev code cuối cùng có còn lock không |
| 6 | `rejectDuplicateSalonBooking` — `app/Http/Controllers/Mobile/CalendarSalonController.php` | Helper arbiter **mới** dùng chung cho Salon | Áp cho `order()` (free) và (theo mục 2) `createOrderPayment` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `order()` — đặt Lesson **miễn phí** | `app/Http/Controllers/Mobile/CalendarController.php` | Direct | Thêm arbiter khử trùng cùng-giây |
| F2 | `checkCanBooking()` | `app/Http/Controllers/Mobile/CalendarController.php` | Direct | Đọc giới hạn chỗ/khách, nằm trong vùng khóa |
| F3 | `countTotalBookingStatus()` | `app/Services/CalendarManagement/CalendarCourseBookingService.php` | Direct | Đếm lại sau khi xóa booking dư (APPROVE + ADMIN_BOOK + REQUEST_CANCEL = status 1,2,5) |
| F4 | `checkValidSlot()` — Lesson luồng **thanh toán** | `app/Http/Controllers/Mobile/CalendarController.php` | Indirect | **KHÔNG sửa** — an toàn sẵn (UPDATE nguyên tử) |
| F5 | `acquireReceptionBookingLock()` / `releaseReceptionBookingLock()` | `app/Http/Controllers/Mobile/CalendarController.php` | Direct | Helper mới ⚠️ (xem mâu thuẫn "không dùng named lock") |
| F6 | `rejectDuplicateSalonBooking()` — Salon | `app/Http/Controllers/Mobile/CalendarSalonController.php` | Direct | Helper arbiter dùng chung; đọc giới hạn từ `calendar_salon_setting_limit_booking`, fail-safe bỏ qua khi không xác định được giới hạn |

**File thay đổi (mục 4.1 nguyên văn của Dev):**
- `app/Http/Controllers/Mobile/CalendarController.php`
- `app/Http/Controllers/Mobile/CalendarSalonController.php`

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_course_bookings` (booking Lesson) | CREATE / **DELETE** | Bản trùng dư (id lớn, cùng giây) bị **tự xóa** — không đổi cấu trúc |
| D2 | `calendar_salon_line_booking` (booking Salon) | CREATE / **DELETE** | Cùng cơ chế khử trùng |
| D3 | `calendar_course_receptions.total_booking` | UPDATE | Đếm lại sau khi xóa booking dư; = APPROVE + ADMIN_BOOK + REQUEST_CANCEL (status 1, 2, 5) |
| D4 | `calendar_salon_setting_limit_booking` | READ | Nguồn giới hạn cho Salon (theo lịch / nhân viên) |

**Recover data**: ✔ Dev khẳng định **không cần recover / migrate**.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Lesson / Calendar Booking (FA-019)** — đặt lịch học phía LINE user, luồng **miễn phí** | F1, F2, F3, F5, D1, D3 | High |
| T2 | **Lesson (FA-019)** — luồng đặt **có thanh toán** (`checkValidSlot`, không sửa) | F4, D3 | Medium (regression check — code không đổi nhưng dùng chung `total_booking`) |
| T3 | **Salon Booking (FA-020)** — đặt lịch salon/phỏng vấn, luồng miễn phí (+ luồng thanh toán, đang mâu thuẫn) | F6, D2, D4 | High |

---

## Rủi ro / lưu ý khi test (nguyên văn Dev)

- **Không có lock** nên còn **khe race rất hẹp**: nếu bản id nhỏ (thắng) chưa commit đúng lúc bản id lớn chạy query arbiter thì bản id lớn không thấy → cả 2 cùng tồn tại (over-book). Xác suất thấp.
- `created_at` độ phân giải **giây**: race lệch qua **ranh giới giây** sẽ không bị arbiter bắt.
- **Salon**: chỉ áp cho khung **giống hệt** (cùng nhân viên/ngày/giờ) — không phủ overlap khác giờ; giới hạn theo **mùa (season)** không tra → fail-safe bỏ qua.
- **Salon luồng THANH TOÁN** (`paymentStripe` / `paymentUnivapay` → `createOrderPayment`): report **mâu thuẫn** giữa mục 2 và mục rủi ro — cần confirm.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Đã hỏi Dev**: Salon luồng thanh toán có arbiter hay chưa? Code cuối cùng còn `acquireReceptionBookingLock` không?
- [ ] **Đã hỏi Dev**: bản dư bị **xóa cứng (DELETE)** — có ảnh hưởng dữ liệu liên quan (mail xác nhận, sync Google Calendar, bill) đã gửi/tạo trước đó không?
