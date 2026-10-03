# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` (Redmine không assign; Journal #137512 do "AI Reader" post) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `bugs/notify_bill_item_20260922` |
| Ngày submit đánh giá | `2026-09-22` (Journal #137512) |
| Auto-filled | `2026-09-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Univapay có trạng thái charge `authorized` (charge đã được chấp thuận, tiền đã được giữ/capture) bên cạnh `successful`. Đây là trạng thái thành công, không phải lỗi.
- `UnivapayPayment::getChargesSale()` chỉ coi `successful` là thành công và `failed` là thất bại. Khi charge dừng ở `authorized`, hàm poll hết số lần retry rồi trả về `success = false` kèm message `請求できませんでした。`.
- Ở luồng mua hàng của bot không bật webhook, `SalesManagementV2Controller::paymentCreditCardItemV2Univapay()` chỉ xử lý riêng 2 trường hợp `status == 'failed'` (xoá order) và `status == 'pending'` (trả kết quả chờ). Trạng thái `authorized` lọt qua cả hai nhánh nên rơi vào `$result = 'error'` → tạo notify `決済に失敗しました` và trả màn hình lỗi cho friend.
- Sau đó job `recover:payment_univapay_timeout` (chạy 5 phút/lần) quét lại order quá 15 phút và vốn đã coi `authorized` là `successful` nên ghi nhận bill thành công. Kết quả: bill thành công nhưng vẫn tồn tại notify bill error.
- Cùng lỗi trên cũng xảy ra ở luồng webhook: `SalesService::getDataCallback()` lấy nguyên `data.status` từ webhook `charge_finished`, nên `authorized` bị so sánh `!= 'successful'` và bị xử lý như thanh toán thất bại.
- Ảnh hưởng dây chuyền: do màn hình báo lỗi nên friend bấm mua lại nhiều lần, Univapay chặn bằng lỗi `CHARGE_TOO_QUICK` (sinh thêm notify lỗi), và lần bấm sau có thể tạo thêm charge thật thứ hai.

## 2. Cách fix

- `UnivapayPayment::getChargesSale()`: coi `authorized` tương đương `successful`, trả về `success = true` ngay, không poll thừa và không sinh error message.
- `SalesService::getDataCallback()`: map `authorized` thành `successful` cho webhook Univapay, để `handleOrderCallback` / `callbackJob` / `callbackChangeCard` xử lý như thanh toán thành công.
- Sau fix, luồng web ghi nhận order thành công ngay trong request (status_webhook = PROCESSED), tạo notify thành công thay vì notify lỗi, friend không còn thấy màn hình lỗi nên không bấm mua lại → tránh luôn lỗi `CHARGE_TOO_QUICK` và charge trùng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SalesManagementV2Controller::paymentCreditCardItemV2Univapay()` — 2 vị trí gọi `getChargesSale` (luồng trial có tiền đầu kỳ + luồng thanh toán chính) | Không sửa trực tiếp (hưởng theo fix) | Đã check, nay nhận `success = true` nên đi vào nhánh thành công, không tạo notify lỗi |
| 2 | `SalesManagementV2Controller::changeCardUnivapay()` | Không sửa trực tiếp (hưởng theo fix) | Đã check, dùng chung `getChargesSale`, hết tình trạng đổi thẻ bị báo lỗi nhầm khi charge ở trạng thái `authorized` |
| 3 | `HandleSendActionTrialV2::billItemUnivapay()` | Không sửa trực tiếp (hưởng theo fix) | Đã check, bill tự động sau trial / bill chu kỳ cũng hết báo thất bại nhầm |
| 4 | `SalesService::getOrderTimeout()` | Giữ nguyên | Đã check, vốn đã có sẵn xử lý coi `authorized` là thành công; giữ nguyên làm lưới an toàn, không phát sinh xử lý trùng vì luồng web đã set status_webhook = PROCESSED |
| 5 | `SalesService::handleOrderCallback()`, `::callbackJob()`, `::callbackChangeCard()` | Không sửa trực tiếp (hưởng theo fix) | Đã check, cả 3 dùng biến `statusPayment` lấy từ `getDataCallback` nên đều được sửa theo |
| 6 | `HandleWebhookUnivapay` (job xử lý webhook) | Không sửa | Đã check, chỉ điều hướng theo `metadata.module`, không cần sửa |
| 7 | `UnivapayPayment::getCharges()` và `::getChargesJob()` | Không sửa | Đã check, thuộc luồng thanh toán gói cước/point của hệ thống, không liên quan bill item |
| 8 | `UnivapayPayment::getChargeStatus()` | Không sửa | Đã check, không có nơi nào gọi |
| 9 | Toàn bộ caller của `getChargesSale` thuộc レッスン予約 / サロン予約 / イベント予約 (11 caller) | Không sửa trực tiếp (hành vi có đổi) | Đã check, chi tiết ở mục 4.3 [C] |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getChargesSale()` | `app/Helpers/UnivapayPayment.php` | Direct | Helper **dùng chung** — coi `authorized` ≡ `successful`, trả `success = true` ngay, không poll thừa, không sinh error message. 11 caller ngoài 商品販売 (lesson / salon / event) — xem 4.3 [C] |
| F2 | `getDataCallback()` | `app/Services/Sales/SalesService.php` | Direct | Map `authorized` → `successful` cho webhook Univapay. Chỉ bản của `SalesService` (dòng 125) được sửa; 3 bản cùng tên ở lesson/salon/event là private method riêng, **giữ nguyên** |

### 4.2. List data bị update khi fix bug

> **Không thêm/sửa/xoá column nào.** Thay đổi là **giá trị được ghi** khi charge ở trạng thái `authorized`.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `s_order_history`: `status_order`, `status_webhook`, `bill_success_date`, `payment_date`, `register_date`, `o_univapay_*` | UPDATE | `status_order = 1` (trước đây giữ nguyên trạng thái chưa hoàn tất), `status_webhook = PROCESSED` (trước đây giữ `TIMEOUT`) |
| D2 | `s_cycle_order_history`: `status_bill`, `status_webhook`, `c_expired_date`, `last_bill_time`, `number_payment`, `c_univapay_*` | UPDATE | `status_bill = 1`, `status_webhook = PROCESSED` |
| D3 | `bot_line_user_item`: `status_contract`, `total_money`, `contract_expired_time`, `trial_expired_time`, `univapay_token`, `univapay_customer_id` | UPDATE | Liên kết friend ↔ item sau thanh toán |
| D4 | `s_items` / `s_monthly_item`: các cột đếm số đăng ký / số thanh toán / doanh thu | UPDATE | Ảnh hưởng thống kê doanh thu theo tháng |
| D5 | `mobile_notify` | CREATE | Ghi notify **thành công** (商品購入 / 初回決済) thay vì notify `決済に失敗しました` |
| D6 | `s_order_history_notify` | CREATE (không còn tạo) | Không còn tạo bản ghi lỗi (`status_order = -1`) cho case `authorized` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

#### [A] 商品販売 — phạm vi chính của ticket

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn hình thanh toán bằng thẻ của friend (bill 1 lần và bill chu kỳ, gồm cả bot **bật** và **không bật** webhook) | F1, F2, D1, D2 | High |
| T2 | Đổi thẻ thanh toán | F1, F2, D3 | High |
| T3 | Bill tự động sau trial / bill chu kỳ chạy bằng job | F1, D2 | High |
| T4 | Thông báo (app notify / ChatWork / PC) của mục 決済 | D5, D6 | High |
| T5 | Danh sách đơn hàng, thống kê doanh thu theo tháng | D1, D4 | Medium |
| T6 | Action / message gửi cho friend sau khi mua hàng (thành công thay vì lỗi) | D1, D3 | Medium |

#### [B] `getDataCallback` — KHÔNG ảnh hưởng サロン予約 / レッスン予約 / イベント予約

- Có **4 bản `getDataCallback`** là private method riêng biệt, 4 class **không kế thừa nhau**:
  - `SalesService` (dòng 125) — **bản duy nhất được sửa**
  - `CalendarCourseBookingService` (dòng 1500) — lesson, giữ nguyên
  - `CalendarSalonLineBookingService` (dòng 4931) — salon, giữ nguyên
  - `EventBookingService` (dòng 58) — event, giữ nguyên
- Bản của `SalesService` chỉ được dùng bởi `handleOrderCallback` / `callbackChangeCard` / `callbackJob`, mà `HandleWebhookUnivapay` chỉ route tới chúng khi `metadata.module` là `sales`, `sales_change_card`, `sales_job`.

#### [C] `getChargesSale` — CÓ ảnh hưởng サロン予約 / レッスン予約 / イベント予約 (helper dùng chung), đã rà **11 caller**

| Nhóm | Vị trí | Hành vi sau fix |
|---|---|---|
| **A — luồng web đặt lịch (8 vị trí)** | Lesson: `CalendarCourseBookingService:492`, `Mobile/CalendarController:1164`<br>Salon: `CalendarSalonLineBookingService:4538`, `Mobile/CalendarSalonController:1889`<br>Event: `MobileEventBookingController:1147` và `:2254`, `Api/BookingEventController:705`, `BookingEventDayController:3765` | **Hành vi CÓ đổi** — theo hướng sửa cùng loại bug, **không phải regression**. Tất cả dùng chung pattern `if (!charge->success) { result = 'error'; ... }`. Trước fix, charge `authorized` bị đánh lỗi thanh toán dù tiền đã được chấp thuận; sau fix vào nhánh thành công |
| **B — job recover timeout (3 vị trí)** | `CalendarCourseBookingService:2039` (lesson)<br>`CalendarSalonLineBookingService:5668` (salon)<br>`EventBookingService:1283` (event) | **Kết quả cuối KHÔNG đổi.** Lesson vốn đã có sẵn xử lý coi `authorized` là thành công → chạy y hệt trước. Salon + event: trước fix thoát bằng `continue`; sau fix qua được guard nhưng `paymentStatus = 'authorized'` không khớp điều kiện so sánh với `'successful'` hoặc `'failed'` nên không dispatch gì. Kết quả giống hệt, chỉ khác điểm thoát |

> **Dev đề nghị QA test hồi quy thêm luồng thanh toán Univapay của レッスン予約 / サロン予約 / イベント予約.**

#### [D] Hai bug tồn đọng phát hiện khi rà soát — CÓ SẴN TỪ TRƯỚC, **NGOÀI PHẠM VI TICKET NÀY**, Dev đề nghị tách ticket riêng

1. Job recover timeout của **salon** (`CalendarSalonLineBookingService:5668`) và **event** (`EventBookingService:1283`) vẫn bỏ qua booking ở trạng thái `authorized` nên booking **treo mãi không được resolve**. Lesson và sales đã có xử lý, hai module này thì chưa.
2. Luồng **webhook** của lesson / salon / event vẫn coi `authorized` là **thất bại**, do `getDataCallback` của 3 service đó chưa được sửa (xem mục [B]).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
