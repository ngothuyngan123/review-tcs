# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #43562 (Journal #146733 "Dev handoff") + Studio task #502 `dev_impact` qua `/new-task` (2026-10-23).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (Journal #146699, #146733) |
| Commit / Pull Request | `<chưa có link PR — chỉ có branch + commit ref>` |
| Branch | `ai_studio_fixbug_43562` (nhánh gốc `release_step_20260930_v2` @`d6c0a2653f63`, commit `27ca043b44cf054b6b18a43fa9d8969cf6359977`) — repo `sns-line` |
| Ngày submit đánh giá | `2026-10-22` (Journal #146733, 11:32) |
| Auto-filled | `2026-10-23 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Với sự kiện thu tiền trước qua Stripe (duyệt tự động), khi thẻ cần 3DS thì màn LIFF gọi API thanh toán 2 lần:
- **Lần 1**: server tạo sẵn booking (`予約完了`, chưa thanh toán) rồi trả về để trình duyệt hiện màn 3DS.
- **Lần 2**: sau khi khách nhập mã xác thực, FE gọi lại API để chốt đơn.

Bước chặn "chỉ được đặt 1 lần" trong `MobileEventBookingController::payment` chạy lại ở lần gọi 2 mà **không loại trừ booking của chính lần thanh toán này**, nên tìm thấy booking vừa tạo ở lần 1 và trả về `「このイベントの予約は一回のみです。」`. Đơn vì vậy không được chốt ngay; job `recover:payment_univapay_timeout` chốt đơn và gửi tin hoàn tất trễ 15–20 phút.

## 2. Cách fix

**D-1**: Bước chặn "chỉ đặt 1 lần" (áp dụng cho cả 3 nhánh cấu hình) bỏ qua booking đang chờ của **chính lần thanh toán sau 3DS** — điều kiện loại trừ khớp đủ 5 yếu tố: `id`, `friend`, `sự kiện`, `status_payment = 0` (chưa thanh toán), `strip_charge_id = PaymentIntent` của lần gọi lại.

Kết quả sau fix:
- LIFF đặt chỗ sự kiện (thanh toán trước bằng Stripe, duyệt tự động, thẻ 3DS, cài `「このイベントで1度のみ」`, `「各予約枠で1度のみ」` hoặc từng khung `「1回のみ」`): sau khi nhập mã 3DS, đặt chỗ hoàn tất ngay, không còn alert `「このイベントの予約は一回のみです。」`, không quay lại màn nhập thẻ.
- Tin hoàn tất đặt chỗ, nhắc lịch và thông báo được gửi **ngay** sau khi thanh toán 3DS, thay vì trễ 15–20 phút.
- Friend đã có booking khác (chưa huỷ) của sự kiện/khung đó **vẫn bị chặn** với message như cũ (không đổi).

File đã sửa (`sns-line`, php-web):
| File | Thay đổi |
|---|---|
| `.../Basic/MobileEventBookingController.php` | +39/-3 |
| `.../Feature/MobileEventBookingPaymentOnceTest.php` | +284 (test mới) |

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `MobileEventBookingController::payment` (API `/ajax/booking-event/payment`, cả lần gọi 1 và lần gọi lại sau 3DS) | Thêm điều kiện loại trừ ở bước kiểm số lần đặt | Lần gọi lại hiện đang tìm thấy booking vừa tạo ở lần gọi 1 nên chặn sai |
| 2 | Bước chốt đơn của lần gọi lại (update booking, ghi friend info, nhắc lịch, gửi tin hoàn tất, thông báo app, affiliate) | Không đổi logic, nhưng nay **chạy sớm hơn** (ngay ở lần gọi lại) cho sự kiện `「1度のみ」` | Dùng lại đúng đường code đang chạy sẵn cho sự kiện `「何度でも」` — Dev xác nhận không phải code mới |
| 3 | Job `recover:payment_univapay_timeout` | Không đổi code; Dev đã kiểm: ca 3DS thành công được chốt ngay (`status_webhook=1`) nên job không xử lý lại | Tránh gửi tin hoàn tất 2 lần — **cần test riêng** (xem REQ-003 / điểm cần test của Dev) |
| 4 | Bảng `b_user_booking` | Chỉ thêm 1 câu đọc theo `id` (không ghi mới) | Đủ dữ liệu để so khớp điều kiện loại trừ 5 yếu tố |
| 5 | Univapay, sự kiện cần duyệt (リクエスト制), lần gọi 1, đổi lịch (`changeBooking`), app mobile | Không đi qua điều kiện mới — Dev khẳng định không đổi hành vi | Regression nhẹ — cần ít nhất 1 TC đối chứng mỗi nhánh |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `MobileEventBookingController::payment` — API `POST /ajax/booking-event/payment`, lần gọi lại sau 3DS (`alreadyPayment=true`) của sự kiện Stripe | `MobileEventBookingController.php` | Direct | Endpoint sửa chính |
| F2 | Bước chặn "chỉ đặt 1 lần" — cả 3 nhánh cấu hình: `type_times_booking=3` (toàn sự kiện), `type_times_booking=2` (mỗi khung), slot `times_booking=2` (từng khung cụ thể) | `MobileEventBookingController.php` | Direct | Cần test đủ **3 cấu hình**, không chỉ 1 |
| F3 | Điều kiện loại trừ khớp 5 yếu tố: `id`, `friend`, `sự kiện`, `status_payment=0`, `strip_charge_id=PaymentIntent` | `MobileEventBookingController.php` | Direct | Case âm bắt buộc: booking của friend khác / PaymentIntent khác / booking đã thanh toán / `bookingId` không phải scalar |
| F4 | Bước chốt đơn của lần gọi lại: update `status_payment`/`status_webhook`, tính lại `use_people`/`remain_limit`, gửi action hoàn tất (`sendActionAppBookingV1`), `addActionRemind`, thông báo app, affiliate | `MobileEventBookingController.php` (+ service liên quan) | Indirect | Side effect giờ chạy ở nhánh `「1度のみ」` — phải kiểm **chỉ xảy ra đúng 1 lần** |
| F5 | Job `recover:payment_univapay_timeout` (chạy mỗi 5 phút, ngưỡng >15 phút) | job nền | Indirect | Phải bỏ qua booking đã chốt bởi lần gọi lại; rủi ro race nếu 3DS lâu hơn ngưỡng job |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `b_user_booking` (status_payment, status_webhook, use_people/remain_limit tính lại) | UPDATE (+ 1 SELECT thêm theo `id` ở bước loại trừ) | Không có migration/schema change |
| D2 | Friend info (ghi nhận khi chốt đơn booking) | UPDATE | Chạy ở bước chốt đơn lần 2, không đổi logic ghi |
| D3 | Tin nhắn hoàn tất đặt chỗ + nhắc lịch (remind) + thông báo app | CREATE / gửi sớm hơn | Gửi ngay sau 3DS thay vì qua job timeout (trễ 15–20 phút) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | LIFF đặt chỗ sự kiện có thu tiền trước qua Stripe (duyệt tự động), đủ 3 cấu hình giới hạn "1 lần" | F1, F2, F3 | High |
| T2 | Tin nhắn hoàn tất đặt chỗ / nhắc lịch / thông báo app cho sự kiện (thời điểm gửi đổi + nguy cơ gửi trùng) | F4, D3 | High |
| T3 | Job `recover:payment_univapay_timeout` (đối soát thanh toán sự kiện) | F5 | Medium |
| T4 | Danh sách người tham gia (participant list), đếm chỗ `use_people`/`remain_limit` | F4, D1 | Medium |
| T5 | *(Không đổi — đối chứng)* lần gọi 1, Univapay, sự kiện cần duyệt (`リクエスト制`/setupIntent), thẻ không 3DS, 3DS thất bại, đổi lịch (`changeBooking`), app mobile | — | Low (regression nhẹ, Dev khẳng định không đổi) |

> ⚠️ **Ghi nhận ngoài phạm vi fix** (Dev nêu, KHÔNG thuộc #43562): lần gọi lại vẫn tin cờ `alreadyPayment` do client gửi, không retrieve lại PaymentIntent thật từ Stripe để xác nhận `succeeded` trước khi chốt đơn — lỗ hổng bảo mật thanh toán có sẵn, Dev đề nghị tách ticket riêng (xem Studio `REQ-009`, "chờ leader" — không chặn đóng #43562 trừ khi Leader đưa vào scope).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
