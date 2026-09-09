# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | commit `64cdcfdce5` (repo `sns-line`, 1 file) — `<chưa có link PR>` |
| Branch | `ai_small_38690` (nhánh gốc `release_step_20260623`) |
| Ngày submit đánh giá | `2026-07-11` |
| Auto-filled | `2026-07-13 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> Nguồn: journal #125635 / #125637 của "AI LME Fix bug" (2026-07-11). Hai journal nội dung **trùng nhau**.

---

## 1. Nguyên nhân

Màn quản lý booking event khi admin bấm refund qua Stripe luôn báo "refund fail" với các booking thanh toán kiểu mới (PaymentIntent — id lưu dạng `pi_`). Hàm `refundMoneyBookingEvent` chỉ gọi API hoàn tiền theo charge (`refundMoney` → Stripe `Refund::create(['charge'=>...])`), nhưng id lưu trong `strip_charge_id` là `pi_` nên Stripe từ chối. Kiểm DB dev xác nhận cột này có cả `ch_` (charge cũ) lẫn `pi_` (PaymentIntent mới).

## 2. Cách fix

Sửa `refundMoneyBookingEvent` trong `BookingEventDayManagementController`: trước khi hoàn tiền Stripe, kiểm tiền tố `strip_charge_id` — nếu bắt đầu `'ch'` thì gọi `refundMoney` (theo charge), còn lại (`pi_`) gọi `refundMoneyPaymentIntent` (theo payment_intent). Áp đúng pattern đã dùng ở `SalesManagementV2Controller`.

**LƯU Ý (nguyên văn Dev):** Redmine parent #26684 — run offline không truy cập được Redmine/Bitbucket để xác minh #26684 có phải bug đang mở + fetch branch cha, nên fix độc lập trên `ai_small_38690`; nếu #26684 là bug đang mở có branch `ai_small_26684`, human nên chuyển commit này sang branch đó trước khi push.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `refundMoneyBookingEvent` — `app/Http/Controllers/Basic/BookingEventDayManagementController.php` | **Có sửa** — thêm phân nhánh chọn API refund theo tiền tố `strip_charge_id` | Function chứa root cause |
| 2 | `StripePayment::refundMoney` — `app/Helpers/StripePayment.php` | Không sửa (chỉ check) | Nhánh refund theo charge (`ch_`) — giữ nguyên cho data cũ |
| 3 | `StripePayment::refundMoneyPaymentIntent` — `app/Helpers/StripePayment.php` | Không sửa (chỉ check) | Nhánh refund theo payment_intent (`pi_`) — được gọi mới |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `refundMoneyBookingEvent` | `app/Http/Controllers/Basic/BookingEventDayManagementController.php` | Direct | File duy nhất thay đổi (Dev ghi ở mục 4.1: "File thay đổi") |
| F2 | `StripePayment::refundMoney` | `app/Helpers/StripePayment.php` | Indirect | Nhánh `ch_` — Dev list ở mục 3, không sửa |
| F3 | `StripePayment::refundMoneyPaymentIntent` | `app/Helpers/StripePayment.php` | Indirect | Nhánh `pi_` — Dev list ở mục 3, không sửa |

> Nguyên văn mục 4.1 của Dev chỉ ghi **file thay đổi**: `app/Http/Controllers/Basic/BookingEventDayManagementController.php`. F2/F3 lấy từ mục 3 (function đã check).

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `b_user_booking.strip_charge_id` | READ | Chỉ **ĐỌC** để chọn API refund; không đổi cấu trúc/giá trị |
| D2 | `b_user_booking.status_payment` / `refund_date` / `reason_refund` | UPDATE | Sau refund thành công **vẫn update như cũ** (`status_payment = 2`) — logic không đổi |

> Nguyên văn Dev: "b_user_booking.strip_charge_id — chỉ ĐỌC để chọn API refund; không đổi cấu trúc/giá trị. Sau refund thành công vẫn update status_payment=2, refund_date, reason_refund như cũ."

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Event Booking (FA-021) — thao tác hoàn tiền (refund) Stripe ở màn quản lý booking event | F1, D1, D2 | `<Dev không ghi mức risk>` |

> Nguyên văn Dev: "Event Booking (FA-021) — sửa thao tác hoàn tiền (refund) Stripe cho booking thanh toán kiểu PaymentIntent (pi_), trước đây luôn refund fail".

---

## 5. Recover data (từ báo cáo Dev)

✔ Không cần recover data.

## 6. Verify của Dev

- **Mức**: lint
- **Lệnh**: `php -l BookingEventDayManagementController.php` → No syntax errors; DB dev (`SELECT LEFT(strip_charge_id,3)...`) → xác nhận `b_user_booking` có cả `ch_` và `pi_`
- **Bằng chứng**: `b_user_booking.strip_charge_id`: 5 bản ghi `ch_` + 5 bản ghi `pi_` trên dev → chứng minh cần phân nhánh theo tiền tố

## 7. Tự review của Dev (AI) — rủi ro khi test

- Fix tối thiểu, focused: thêm phân nhánh chọn API refund Stripe theo tiền tố `strip_charge_id`, mirror pattern `SalesManagementV2Controller`. **Không đổi logic update DB, không đụng nhánh Univapay.**
- **Rủi ro**: giả định id không phải `ch_` thì là `pi_` (payment_intent) — đúng với `autoPaymentIntents` của event booking; các id `ch_` cũ vẫn đi nhánh `refundMoney`.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
