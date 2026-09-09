# FA-019 「レッスン予約」 — Logic Spec: Trang public (LIFF) & API ứng dụng di động

> Tạo bởi: **web-analyzer** agent | Phương pháp: **code-first** — đọc trực tiếp `Mobile\CalendarController`, `Api\CalendarLessonController`, các service `App\Services\CalendarManagement\*`, helper thanh toán và model.
> Tài liệu **anh em**: `web/api-spec-public.md` (32 endpoint `EP-P01`…`EP-P17`, `EP-M01`…`EP-M15` — hợp đồng request/response). File này mô tả **tầng nghiệp vụ**: luồng, máy trạng thái, quy tắc, side effect. Không lặp lại chi tiết tham số — tra ở `api-spec-public.md`.
> Phạm vi: **không** bao gồm `Basic\CalendarManagementController` / `Basic\SettingPaymentCalendarController` (portal Admin — spec riêng).
> Đường dẫn gốc source: `src/web/sns-line/`. Ký hiệu `:NNN` = số dòng trong file đang nói tới.
> Confidence tổng thể: **Cao**.

---

## 1. Luồng đặt chỗ end-to-end phía server

### 1.1 Bản đồ bước UI → server

Trình đặt chỗ LIFF là **SPA một trang** (`EP-P01` render toàn bộ), người dùng đi qua 6 bước. Chỉ **3 bước cuối** thực sự ghi DB.

| Bước UI | Màn hình | Endpoint gọi | Method server | Ghi DB | Side effect |
|---|---|---|---|---|---|
| 0. Mở trang | L01, L02, L03 | `EP-P01` `GET /mobile/calendar/{hash}/{uCode}` | `CalendarController@index` :73 | Không | Kiểm tra bot hết hạn / bị chặn / filter bạn bè |
| 0b. Kiểm tra bạn bè | toàn trang | `EP-P17` `POST /ajax/mobile/calendar-salon/check-friend` | `CalendarSalonController@checkFriend` :4408 | Không | (dùng chung FA-020) |
| 1. Chọn 「コース」 | L04, L05 | `EP-P03` | `getListCourseByCalendar` :281 | Không | Lọc course theo FilterV2 của bạn bè |
| 2. Chọn 「希望日時」 | L06 (週) | `EP-P04` | `getListTimeBookingByCourse` :363 → `getListTimeWeek` :2756 | Không | Tính `total_person - total_booking`, tự nhảy tối đa 4 tuần |
| 2. Chọn 「希望日時」 | L06 (月) | `EP-P05` | `initDataBooking` :515 → `getListTimeMonth` :2871 | Không | |
| 3. 「お客様情報」 | L07 | `EP-P06` | `getDataFriendInfo` :560 | Không | Prefill từ `line_user` + `friend_information_values` |
| 4. 「カード情報」 | L08 | `EP-P08`, `EP-P09` (UnivaPay) | `createCustomerIdUnivapay` :2666, `getInfoCardPayment` :2622 | Không | Gọi API UnivaPay bằng khoá bí mật của bot |
| 5. 「内容の最終確認」 → bấm 予約する (có thanh toán, Stripe) | L09 | `EP-P10` | `paymentStripe` :848 | **`calendar_course_bookings` INSERT** + `calendar_course_receptions` UPDATE | Giữ chỗ, thu tiền Stripe |
| 5. như trên (UnivaPay) | L09 | `EP-P11` | `paymentUnivapay` :1042 | như trên | Giữ chỗ, thu tiền UnivaPay |
| 5b. Chốt đặt chỗ | L09 | `EP-P12` | `order` :1414 | INSERT **hoặc** UPDATE booking + history + đếm lại reception | Gửi LINE, `t_actions`, `event_step_time`, `mobile_notify`, Google Sheet, ghi đè hồ sơ bạn bè |
| 5c. Nhánh 「キャンセル待ち」 | L10 | `EP-P12` (`register_notify_slot=true`) | `order` :1414 | INSERT booking `status = 3` | Gửi LINE + action `11009` |
| 5d. Rollback khi 3-D Secure hỏng | L09 | `EP-P13` | `deleteOrderConfirmFail` :1371 | **forceDelete** booking | Đếm lại reception |
| 6. Hoàn tất | L11, L12 | — | — | Không | JS chỉ hiển thị |
| 6b. Chờ webhook | L18 | (poll trong `EP-P11`) | `checkStatusProcessCallback` | UPDATE `status_webhook` | UnivaPay webhook chốt sau |

> **Điểm mấu chốt kiến trúc**: đặt chỗ **có thanh toán** đi **2 request** (`EP-P10`/`EP-P11` giữ chỗ + thu tiền → rồi `EP-P12` chốt). Đặt chỗ **không thanh toán** chỉ đi **1 request** (`EP-P12`). Toàn bộ khác biệt do **cờ `checkHasPayment` client gửi** quyết định (`CalendarController.php:1425`, `:1468`). Xem BR-P02 và §10 RP-01.

### 1.2 Luồng có thanh toán — 2 pha

```
PHA 1: EP-P10 (Stripe) / EP-P11 (UnivaPay)
  checkCanBooking(courseId, receptionId, lineUserId)      :870 / :1073
     └ 6 rào chắn nghiệp vụ (§2.2) — ném Exception nếu hỏng
  ├─ Stripe, approve_type == 1 (thu ngay):
  │    handleKeepSlot()          :1224  → checkValidSlot() GIỮ CHỖ (atomic)
  │                                     → createOrderPayment() INSERT booking
  │                                        status = 1 (APPROVE), payment_status = 0 (NOT_PAYMENT)
  │    StripePayment::paymentIntents(confirm = true, setup_future_usage = off_session)
  │       ├─ Exception → deleteOrderError() forceDelete + countTotalBookingStatus  :966
  │       └─ OK → trả charge_id; nếu status != 'succeeded' → isConfirm = true + client_secret
  │                (client làm 3-D Secure, hỏng thì gọi EP-P13)
  ├─ Stripe, approve_type == 2 (chờ duyệt):
  │    isPaymentAfter = true → CHỈ setupIntent() lưu thẻ.
  │    KHÔNG giữ chỗ, KHÔNG tạo booking.                  :925-960
  └─ UnivaPay (mọi approve_type):
       handleKeepSlot() LUÔN chạy                          :1086
       chargeMoneyUnivapaySale(metaData = {module:'lesson', booking_id, bot_id, ...})
       ├─ có webhook  → checkStatusProcessCallback() poll 5×1s → success / error / pending(L18)
       └─ không webhook → getChargesSale() xác nhận đồng bộ

PHA 2: EP-P12  order()                                     :1414
  nhận lại bookingId + bookingType từ pha 1
  → UPDATE booking (ghi đè toàn bộ trường thanh toán + status/payment_status thật)
  → tạo calendar_course_booking_history_actions
  → countTotalBookingStatus()
  → insertNotifyLesson() / addActionRemind() / sendAction() / gửi LINE / Google Sheet
```

### 1.3 Luồng không thanh toán — 1 pha

```
EP-P12  order()  với checkHasPayment falsy                 :1468-1487
  → checkCanBooking()  (chỉ chạy khi KHÔNG phải register_notify_slot)
  → xoá sạch mọi trường thẻ client gửi (univapay_token, charge_id, pm_id, last4…)
  → payment_status = 2 (SP_NO_PAYMENT)
  → INSERT booking mới (bookingId rỗng ⇒ nhánh 'case unpaid -> new'  :1638)
  → arbiter chống trùng đồng thời (§2.3)
  → phần side effect chung
```

> ⚠ Ở nhánh này server **không gọi `checkValidSlot()`** — tức **không tăng `total_booking` theo cách nguyên tử**. Chỗ trống chỉ được kiểm bằng `checkCanBooking()` (đọc rồi so sánh, non-atomic) rồi `countTotalBookingStatus()` đếm lại sau. Đó chính là lý do tồn tại khối "arbiter" §2.3.

### 1.4 Ghi DB khi tạo booking

`createOrderPayment()` :1297-1356 (pha 1) và `order()` :1596-1622 (pha 2) ghi cùng bộ cột vào `calendar_course_bookings`:

| Cột | Giá trị | Nguồn |
|---|---|---|
| `course_id`, `calendar_id`, `reception_id` | client | request |
| `booking_date` | `now()` | server |
| `line_user_id` | `line_user.id` tra từ `line_id` | server |
| `name`, `email` | client | request |
| `payment_system` | `calendar.type_payment` nếu `checkHasPayment`, ngược lại `null` | DB + cờ client |
| `payment_amount` | **`request->amount` — client gửi** | request ⚠ |
| `payment_status` | pha 1: luôn `0`; pha 2: `1`/`0`/`2` (§3.3) | logic |
| `status` | pha 1: luôn `1`; pha 2: `1`/`0`/`3` (§3.2) | logic |
| `charge_id`, `strip_customer_id`, `strip_pm_id`, `last4`, `brand_name`, `payment_card_expired`, `payment_email` | client | request ⚠ không xác minh với cổng |
| `univapay_token`, `univapay_customer_id`, `univapay_customer_code` | client | request ⚠ |
| `environment` | `calendar.environment` | DB ✅ |
| `friend_info` | `json_encode($request->friend_info_settings)` | request |
| `user_update_time` | `now()` | server |
| `status_webhook` | pha 1: `0` hoặc `3` nếu client gửi `isProcessWithWebhook = false`; pha 2: **luôn `1` (PROCESSED)** | :1258-1263, :1621 |

> ⚠ Pha 2 **luôn ghi đè `status_webhook = 1`** (`STATUS_WEBHOOK_PROCESSED`, :1621) bất kể pha 1 để `0` hay `3`. Nghĩa là sau khi `order()` chạy, mọi dấu vết "đang chờ webhook" bị xoá. Confidence: Cao.

---

## 2. Kiểm soát chỗ trống & chống overbooking

### 2.1 Nguồn sự thật của "còn bao nhiêu chỗ"

Chỗ trống được lưu **denormalized** trên `calendar_course_receptions`:

| Cột | Ý nghĩa | Công thức tái tính (`countTotalBookingStatus` `CalendarCourseBookingService.php:1424-1443`) |
|---|---|---|
| `total_person` | Sức chứa do Admin đặt | Admin nhập, không tự đổi |
| `type_limit_booking` | `1` = có giới hạn, `0` = **không giới hạn** | Admin nhập |
| `total_booking` | **Số chỗ đang bị chiếm** | `count(status ∈ {1 APPROVE, 2 ADMIN_BOOK}) + count(status = 5 REQUEST_CANCEL)` |
| `total_approve` | | `count(status ∈ {1, 2})` |
| `total_request` | | `count(status = 0)` |
| `total_request_cancel` | | `count(status = 5)` |
| `total_cancel` | | `count(status ∈ {4, 7})` |
| `total_request_booking_wait_cancel` | Số người 「キャンセル待ち」 | `count(status = 3)` |

> **Quy tắc quan trọng**: `status = 0` (`SB_REQUEST_BOOKING` — 「リクエスト」 chờ Admin duyệt) **KHÔNG được tính vào `total_booking`** ⇒ **không chiếm chỗ**. Ở chế độ 「承認制」 (`approve_type = 2`), số người gửi yêu cầu là **không giới hạn**; slot chỉ bị chiếm khi Admin duyệt (`EP-M01 approveBooking` → status 1). Confidence: Cao (`:1424-1443`).
>
> `status = 5` (đã xin huỷ, chờ Admin duyệt huỷ) **vẫn chiếm chỗ** — đúng nghiệp vụ vì huỷ chưa được chấp thuận.

### 2.2 Sáu rào chắn của `checkCanBooking()`

`CalendarController.php:2073-2151`. Chạy trước mọi lần giữ chỗ **có thanh toán** (`EP-P10` :870, `EP-P11` :1073) và ở nhánh **không thanh toán** của `EP-P12` (:1474).

| # | Kiểm tra | Nguồn cấu hình | Lỗi ném ra | Dòng |
|---|---|---|---|---|
| 1 | Course tồn tại **và** `booking_page_display = BOOKING_DISPLAY_ON` | `calendar_course` | 「コースが存在していません。」 code `1` | :2075-2082 |
| 2 | Giới hạn số lần đặt/khách | `calendar_setting_send_messages.limit_book_each_customer`, `.number_limit_booking` | 「1人あたりの予約受付上限に達しています」 (không set code ⇒ `0`) | :2088-2095 |
| 3 | Reception tồn tại | `calendar_course_receptions` | 「予約の時間が存在していません。」 code `2` | :2097-2103 |
| 4 | Đã đến giờ mở nhận đặt | `start_receive_booking_type == 2` → `checkIsValidStartReceive()` | 「予約の受付を開始していません。」 | :2106-2120 |
| 5 | Chưa quá hạn nhận đặt | `deadline_receive_booking_type == 2` → `checkIsValidDeadlineReceive()`; ngược lại `start_time > now` | 「予約の受付が終了されました。」 | :2123-2142 |
| 6 | Còn chỗ | `type_limit_booking == 1` → `WHERE (total_person - total_booking) > 0` | 「予約がいっぱいです。別の枠を予約してください。」 | :2144-2151 |

**`checkLimitBookEachCustomer()`** (:246-260) — đếm booking của **cùng `line_user_id` trong cùng `calendar_id`**, chỉ tính slot **còn ở tương lai** (`CONCAT(received_booking_date," ",start_time) > NOW()`) và `status ∈ {1, 2, 5}`. Đạt trần khi `count >= number_limit_booking`.

> Chú ý: không tính `status = 0` (đang chờ duyệt) và `status = 3` (chờ chỗ trống). Vậy ở chế độ 「承認制」 khách có thể gửi **vô hạn** yêu cầu mà không chạm trần; trần chỉ chặn sau khi Admin đã duyệt. Confidence: Cao.

**`checkIsValidStartReceive` / `checkIsValidDeadlineReceive` / `checkIsValidCancel`** (:414-508) đều theo cùng khuôn:
- `setting_*_type == 1` — 「日付指定」: mốc = `start_time − before_booking_day` ngày, giờ đặt theo `before_booking_hour`.
- `setting_*_type != 1` — 「日時指定」: mốc = `start_time − booking_time_from` giờ `− booking_time_to` phút.
- `checkIsValidStartReceive` yêu cầu mốc **đã qua** (mốc `> time()` ⇒ false); hai hàm kia yêu cầu mốc **chưa qua** (mốc `< time()` ⇒ false).

> 🐛 Đặt tên cột gây bẫy: `booking_time_from` được dùng làm **số giờ**, `booking_time_to` làm **số phút** — không phải khoảng "từ…đến". Ai đọc DB sẽ hiểu sai. Confidence: Cao (:434-436).

### 2.3 Ba cơ chế giữ chỗ — không thống nhất

Hệ thống dùng **ba** cơ chế khác nhau tuỳ luồng, và chỉ **một** cơ chế là nguyên tử.

#### (a) `checkValidSlot()` — nguyên tử ✅ (`CalendarController.php:1385-1412`)

```
if (reception.type_limit_booking == 0) {            // không giới hạn
    UPDATE total_booking + 1, total_approve + 1;  return true;
}
DB::beginTransaction();
  recordAffected = UPDATE calendar_course_receptions
                   SET total_booking = total_booking + 1, total_approve = total_approve + 1
                   WHERE id = ? AND (total_person - total_booking) > 0;
DB::commit();
return recordAffected >= 1;
```

Đây là mẫu **conditional UPDATE nguyên tử** — InnoDB khoá hàng trong lúc UPDATE, hai request đồng thời không thể cùng thấy `> 0`. **Chống race đúng cách.** Cặp `DB::beginTransaction()/commit()` bao quanh một câu lệnh đơn là **thừa** (UPDATE vốn tự-commit) nhưng vô hại.

Chỉ được gọi từ `handleKeepSlot()` (:1226) ⇒ **chỉ luồng CÓ thanh toán mới được bảo vệ nguyên tử**.

#### (b) `checkCanBooking()` rào #6 — không nguyên tử ❌

`SELECT … WHERE (total_person - total_booking) > 0` rồi mới INSERT ở bước sau (:2144-2151). Kinh điển **check-then-act**: hai request đồng thời cùng đọc thấy còn 1 chỗ ⇒ cùng INSERT ⇒ overbooking. Đây là con đường duy nhất ở luồng **không thanh toán**.

Hàm `checkValidBooking()` (:1901-1915) còn lỏng hơn — dùng `total_person - total_booking >= 0` (cho phép **bằng 0**, tức đã đầy vẫn qua) — nhưng grep toàn repo cho thấy **không nơi nào gọi**. Code chết. Confidence: Cao.

#### (c) Khối 「arbiter theo id」 — vá lỗi hậu kiểm ⚠ (`order()` :1651-1699)

Comment trong code ghi rõ đây là bản vá cho sự cố thật (「Mẫu arbiter theo id: lessons #37711/#37780」). Logic:

```
Chỉ chạy khi: booking VỪA được INSERT mới (isNewBookingCreated)
           && !register_notify_slot
           && reception.type_limit_booking == 1
           && statusOrder == 1 (APPROVE)
1) Có booking khác status=1, cùng reception, id NHỎ HƠN, created_at TRÙNG TỚI GIÂY?
2) Nếu có → đếm booking id nhỏ hơn mình có status ∈ {1, 2, 5}
3) Nếu count >= total_person → mình là bản dư:
     forceDelete booking + forceDelete history action
     countTotalBookingStatus()
     throw 「予約がいっぱいです。別の枠を予約してください。」
```

**Điểm yếu đã xác định** (Confidence: Cao):

| # | Vấn đề | Hệ quả |
|---|---|---|
| 1 | So khớp trùng bằng **`created_at` chính xác tới GIÂY** (:1673) | Hai request cách nhau 1.001s (vẫn là race thật vì cùng đọc snapshot cũ) **không** bị bắt ⇒ overbooking lọt |
| 2 | Bước phát hiện chỉ xét `status = 1`; bỏ qua `status = 2` (ADMIN_BOOK) | Admin đặt hộ đồng thời với khách ⇒ không phát hiện |
| 3 | Không chạy khi `bookingId` đã có (nhánh 「case paid -> update」 :1633) | Luồng có thanh toán không có arbiter — nhưng luồng đó đã có `checkValidSlot()` nguyên tử nên chấp nhận được |
| 4 | Là **hậu kiểm**: booking đã ghi vào DB rồi mới xoá. Process chết giữa chừng ⇒ booking dư nằm lại | Dữ liệu bẩn |
| 5 | `DB::beginTransaction()` trong `order()` **đã bị comment** (:1624, và `// DB::rollback();` :1884) | Toàn bộ `order()` **không có transaction**: INSERT booking, INSERT history, UPDATE reception, gửi LINE là các thao tác rời rạc. Lỗi giữa chừng ⇒ trạng thái nửa vời |

#### So sánh nhanh

| Luồng | Giữ chỗ bằng | Nguyên tử? | Rủi ro |
|---|---|---|---|
| Có thanh toán (`EP-P10` `approve_type=1`, `EP-P11`) | `checkValidSlot()` | ✅ Có | Thấp |
| Có thanh toán (`EP-P10` `approve_type=2` / `isPaymentAfter`) | **Không giữ chỗ gì cả** | — | Xem §6.4 |
| Không thanh toán (`EP-P12`) | `checkCanBooking()` + arbiter hậu kiểm | ❌ Không | **Cao** |
| Client gửi `checkHasPayment=false` giả | `checkCanBooking()` + arbiter | ❌ | **Cao** + bỏ qua tiền |
| Admin app `EP-M15 add-booking` | **Không kiểm tra gì** | — | **Rất cao** — `Api/CalendarLessonController.php:1700-1745` |
| Admin app `EP-M11 course-reception/update` | Cho phép hạ `total_person` xuống dưới `total_booking` | — | Overbooking vĩnh viễn |

### 2.4 Rò rỉ chỗ (slot leak)

`handleKeepSlot()` tăng `total_booking` **ngay** (`checkValidSlot`), nhưng `order()` (pha 2) mới ghi trạng thái thật. Nếu người dùng **bỏ ngang giữa hai pha** (đóng LIFF sau khi thẻ đã charge nhưng trước khi gọi `EP-P12`):

- Booking nằm lại với `status = 1`, `payment_status = 0`, `status_webhook ∈ {0, 3}` — **vẫn chiếm 1 chỗ**.
- `EP-P15 getListHistoryBooking` chủ động **lọc bỏ** đúng bộ ba này khỏi lịch sử (`NOT (status=1 AND payment_status=0 AND status_webhook IN (0,3,4))`, :2417, :2475) ⇒ khách **không nhìn thấy** booking treo của chính mình, không thể tự huỷ.
- Không tìm thấy job/cron nào dọn các booking treo này. **Confidence: Trung bình**.

⇒ **Chỗ bị chiếm treo vô thời hạn**, chỉ Admin thấy và xử lý thủ công được. Xem §10 RP-04.

---

## 3. Máy trạng thái `calendar_course_bookings`

### 3.1 Ba trục trạng thái độc lập

Một booking mang **ba** trường trạng thái không đồng bộ với nhau — đây là nguồn gốc phần lớn sự phức tạp của tính năng.

| Trục | Cột | Miền giá trị | Ai đổi |
|---|---|---|---|
| Đặt chỗ | `status` | `0`…`7` | LINE User, Admin (web + app), job |
| Thanh toán | `payment_status` | `0`…`3` | LINE User (gián tiếp), Admin |
| Webhook UnivaPay | `status_webhook` | `0`…`4` | Server + webhook callback |

### 3.2 Trục `status` — đầy đủ giá trị

Hằng số: `app/CalendarCourseBooking.php:16-23`. Nhãn hiển thị: `Api/CalendarLessonController.php:890-908`.

| Giá trị | Hằng số | Ý nghĩa nghiệp vụ | Nhãn app 「」 | Chiếm chỗ? |
|---|---|---|---|---|
| `0` | `SB_REQUEST_BOOKING` | Khách gửi yêu cầu, chờ Admin duyệt (chế độ 承認制) | リクエスト | **Không** |
| `1` | `SB_BOOKING_APPROVE` | Đặt chỗ đã xác nhận (tự động duyệt) | 予約確定 | **Có** |
| `2` | `SB_BOOKING_ADMIN_BOOK` | Admin đặt hộ khách | 予約確定 | **Có** |
| `3` | `SB_REQUEST_BOOKING_WAIT_CANCEL` | 「キャンセル待ち」 — đăng ký nhận thông báo khi có chỗ | 通知受取希望 | **Không** |
| `4` | `SB_BOOKING_CANCEL` | Khách đã huỷ (hoặc Admin duyệt huỷ) | キャンセル | Không |
| `5` | `SB_REQUEST_BOOKING_CANCEL` | Khách xin huỷ, chờ Admin duyệt | リクエスト | **Có** |
| `6` | `SB_BOOKING_DENY` | Admin từ chối yêu cầu đặt | 否認済 | Không |
| `7` | `SB_BOOKING_ADMIN_CANCEL` | Admin chủ động huỷ | キャンセル | Không |

> ⚠ Nhãn hiển thị **gộp nhập nhằng**: `0` và `5` cùng hiện 「リクエスト」 dù ý nghĩa trái ngược (xin đặt vs xin huỷ); `1` và `2` cùng 「予約確定」; `4` và `7` cùng 「キャンセル」. Người vận hành không phân biệt được ai huỷ. Confidence: Cao (`:890-908`).
> Hằng số `BOOKING_STATUS` trong model (`CalendarCourseBooking.php:36-43`) **thiếu** mục cho `6` và `7` — nếu blade nào dùng map này sẽ ra rỗng. Confidence: Cao.

### 3.3 Trục `payment_status`

| Giá trị | Hằng số | Ý nghĩa | Nhãn app |
|---|---|---|---|
| `0` | `SP_NOT_PAYMENT` | Chưa thanh toán (đã tạo booking, chờ thu tiền hoặc chờ duyệt) | 未決済 |
| `1` | `SP_PAYMENT` | Đã thu tiền thành công | 決済成功 |
| `2` | `SP_NO_PAYMENT` | Khoá học miễn phí / calendar không bật thanh toán | 決済なし |
| `3` | `SP_REFUND` | Đã hoàn tiền | 返金済み |

Quyết định giá trị lúc tạo booking (`order()` :1554-1567):

```
checkHasPayment == true  &&  approve_type == 1  →  payment_status = 1 (SP_PAYMENT)
checkHasPayment == true  &&  approve_type == 2  →  payment_status = 0 (SP_NOT_PAYMENT)  // thu sau khi duyệt
checkHasPayment falsy                            →  payment_status = 2 (SP_NO_PAYMENT)
```

> 🔴 `payment_status = 1` được ghi **chỉ dựa vào cờ client**, không đối chiếu kết quả thật từ Stripe/UnivaPay ở pha 2. Xem BR-P02, §10 RP-01.

### 3.4 Trục `status_webhook` (chỉ có nghĩa với UnivaPay)

| Giá trị | Hằng số | Ý nghĩa |
|---|---|---|
| `0` | `STATUS_WEBHOOK_UNPROCESSED` | Đã charge, đang chờ webhook |
| `1` | `STATUS_WEBHOOK_PROCESSED` | Webhook đã xử lý xong (hoặc luồng không dùng webhook đã hoàn tất) |
| `2` | `STATUS_WEBHOOK_ERROR` | Webhook báo thất bại |
| `3` | `STATUS_WEBHOOK_TIMEOUT` | Client báo `isProcessWithWebhook = false` ngay từ đầu |
| `4` | `STATUS_WEBHOOK_TIMEOUT_WEBHOOK` | Poll 5 lần không thấy webhook về → chuyển màn L18 |

`EP-M01 change-status-booking` **chặn mọi thao tác Admin** khi `status_webhook ∈ {0, 3, 4}` **và** `payment_system == 1` (UnivaPay) → 「決済処理を行っていますので、操作できません。」 (`Api/CalendarLessonController.php:294-308`).

> ⚠ Booking kẹt ở `status_webhook = 4` (webhook không bao giờ về) **bị khoá vĩnh viễn với Admin** và **bị ẩn khỏi lịch sử của khách** (§2.4). Không có đường thoát tự động. Confidence: Cao.

### 3.5 Sơ đồ chuyển trạng thái `status`

```
                          ┌──────────── (không tồn tại) ────────────┐
                          │                                          │
   [LINE User] order()    │    [LINE User] order()      [Admin app] EP-M15
   approve_type=1         │    register_notify_slot     add-booking
   checkHasPayment ✓/✗    │    = true                   (không kiểm sức chứa)
          │               │           │                        │
          ▼               ▼           ▼                        ▼
       ┌─────┐        ┌─────┐     ┌─────┐                  ┌─────┐
       │  1  │        │  0  │     │  3  │                  │  2  │
       │確定 │        │リクエスト│  │通知待ち│                │確定 │
       └──┬──┘        └──┬──┘     └──┬──┘                  └──┬──┘
          │              │            │                        │
          │              │ EP-M01     │ order() lần 2          │
          │              │ approve    │ (handleKeepSlot        │
          │              │ Booking    │  thấy booking status=3 │
          │              ├───────────►│  → UPDATE về status 1) │
          │              │   status 1 └────────┬───────────────┘
          │              │                     │
          │              │ EP-M01              ▼ (hoà vào 1)
          │              │ denyBooking      ┌─────┐
          │              └────────────────► │  6  │ 否認済 (kết thúc)
          │                                 └─────┘
          │              │ EP-P14 cancelBooking (status 0, mọi approve_type)
          │              └──────────────────────────────► [4]
          │
          ├─ EP-P14 cancelBooking, cancel approve_type = 1 ──────► ┌─────┐
          │                                                        │  4  │ キャンセル
          ├─ EP-M01 approveCancel (từ 5) ─────────────────────────►└─────┘  (kết thúc)
          │
          ├─ EP-P14 cancelBooking, cancel approve_type = 2 ──────► ┌─────┐
          ├─ EP-M01 requestCancel (từ 1/2) ──────────────────────► │  5  │ キャンセル申請中
          │                                                        └──┬──┘
          │                     EP-M01 denyCancel  ◄─────────────────┤ (→ 1)
          │                     EP-P14 nhánh 2 (rút lại) ◄───────────┤ (→ 1 hoặc 2)
          │                     EP-M01 approveCancel ────────────────┴──► 4
          │
          └─ EP-M01 adminCancel ─────────────────────────────────► ┌─────┐
                                                                   │  7  │ (kết thúc)
                                                                   └─────┘

   [3] ── EP-P14 nhánh 1 (dừng nhận thông báo) ──► XOÁ MỀM (deleted_at)
   bất kỳ ── EP-P13 deleteOrderConfirmFail ──► XOÁ CỨNG (forceDelete)
```

### 3.6 Bảng chuyển trạng thái đầy đủ

| # | `status` vào | Tác nhân | Hành động / endpoint | `status` ra | Bản ghi `..._history_actions` | `reason` | Bằng chứng |
|---|---|---|---|---|---|---|---|
| T-01 | — | LINE User | `EP-P12 order`, `approve_type = 1` | `1` | `1` `SB_REQUEST_BOOKING_AUTO_APPROVE` | 予約完了 | `CalendarController.php:1546-1550` |
| T-02 | — | LINE User | `EP-P12 order`, `approve_type = 2` | `0` | `2` `SB_REQUEST_BOOKING_WAITING_APPROVE` | 予約リクエスト | :1546-1550 |
| T-03 | — | LINE User | `EP-P12 order`, `register_notify_slot = true` | `3` | `11` `SB_REQUEST_BOOKING_WAIT_ANOTHER_CANCEL` | キャンセル待ち 登録 | :1541-1545 |
| T-04 | — | Admin (app) | `EP-M15 add-booking` | `2` | `5` `SB_REQUEST_BOOKING_ADMIN_BOOK` | 手動予約追加 | `Api/CalendarLessonController.php:1714-1739` |
| T-05 | `3` | LINE User | `EP-P10`/`EP-P11` `handleKeepSlot()` phát hiện booking `status=3` cùng slot ⇒ **UPDATE đè** thay vì tạo mới | `1` | (tạo ở pha 2) | | `CalendarController.php:1231-1289` |
| T-06 | `3` | LINE User | `EP-P12 order` `bookingType = notify` ⇒ UPDATE đè | `1` hoặc `0` | theo `approve_type` | | :1626-1650, :1701-1717 |
| T-07 | `3` | Admin (app) | `EP-M15 add-booking`, khách đã có bản `status=3` ở slot ⇒ **UPDATE đè** | `2` | `5` | 手動予約追加 | `Api/…:1733-1739` |
| T-08 | `3` | LINE User | `EP-P14 cancelBooking` nhánh 1 — 「通知受け取りを解除」 | **xoá mềm** | không tạo | | `CalendarController.php:2165-2181` |
| T-09 | `0` | Admin (app) | `EP-M01 approveBooking` | `1` | `4` `SB_REQUEST_BOOKING_APPROVE` | 予約リクエスト 承認 | `Api/…:312-370` |
| T-10 | `0` | Admin (app) | `EP-M01 denyBooking` | `6` | `14` `SB_REQUEST_BOOKING_DENY` | 予約リクエスト 否認 | `Api/…:372-380` |
| T-11 | `0` | LINE User | `EP-P14 cancelBooking` — **huỷ thẳng, bỏ qua duyệt** dù `approve_type` = gì | `4` | `6` `SB_REQUEST_CANCEL_AUTO_APPROVE`; đồng thời **sửa** bản ghi cũ `2` → `3` `…_WAITING_APPROVE_HISTORY` | 予約キャンセル | `CalendarController.php:2255-2270` |
| T-12 | `1`/`2` | LINE User | `EP-P14`, `calendar_setting_send_messages(moment=cancel).approve_type = 1` | `4` | `6` | 予約キャンセル | :2231-2260 |
| T-13 | `1`/`2` | LINE User | `EP-P14`, `moment=cancel` `approve_type = 2` | `5` | `7` `SB_REQUEST_CANCEL_WAITING_APPROVE` | キャンセルリクエスト | :2231-2260 |
| T-14 | `1`/`2` | Admin (app) | `EP-M01 requestCancel` | `5` | `7` | キャンセルリクエスト | `Api/…:414-432` |
| T-15 | `1`/`2` | Admin (app) | `EP-M01 adminCancel` | `7` | `10` `SB_REQUEST_CANCEL_ADMIN_CANCEL` | 手動予約キャンセル | `Api/…:434-462` |
| T-16 | `5` | Admin (app) | `EP-M01 approveCancel` | `4` | `9` `SB_REQUEST_CANCEL_APPROVE` | キャンセルリクエスト 承認 | `Api/…:382-400` |
| T-17 | `5` | Admin (app) | `EP-M01 denyCancel` | `1` | `15` `SB_REQUEST_CANCEL_DENY` | キャンセルリクエスト 否認 | `Api/…:402-412` |
| T-18 | `5` | LINE User | `EP-P14` nhánh 2 — **rút lại yêu cầu huỷ**. `admin_id` có ⇒ về `2`, không ⇒ về `1` | `1`/`2` | không tạo | | `CalendarController.php:2182-2196` |
| T-19 | bất kỳ | LINE User | `EP-P13 deleteOrderConfirmFail` | **xoá cứng** | không tạo | | :1371-1384 |
| T-20 | bất kỳ | Server | `deleteOrderError()` khi thanh toán hỏng ở pha 1 | **xoá cứng** | không tạo | | :1358-1366 |
| T-21 | `4`/`6`/`7` | LINE User | `EP-P14` nhánh 3 rơi vào `else` cuối | 🐛 **`status = NULL`** | tạo bản ghi với `status = null` | `null` | :2272-2290 |

### 3.7 Ai được phép chuyển trạng thái

| Tác nhân | Chuyển được | Cơ chế xác thực thực tế |
|---|---|---|
| **LINE User (LIFF)** | T-01, T-02, T-03, T-05, T-06, T-08, T-11, T-12, T-13, T-18, T-19 | **Không có** — chỉ cần biết `booking_id` (số nguyên tự tăng). Xem `api-spec-public.md` S-02, S-03 |
| **Admin / Staff (app di động)** | T-04, T-09, T-10, T-14, T-15, T-16, T-17 | Guard `api-mobile`; **không kiểm quyền role** (trừ `EP-M02`); **không kiểm booking thuộc bot mình** |
| **Admin (portal web)** | (ngoài phạm vi — `Basic\CalendarManagementController`) | — |
| **Job Spring Boot** | **Không chuyển `status`** — chỉ đọc `event_step_time` để gửi nhắc lịch, và `mobile_notify` để đẩy push | xem `job-spec.md` |
| **Webhook UnivaPay** | Chỉ đổi `payment_status` + `status_webhook`, không đổi `status` | `CalendarCourseBookingService::handleOrderCallback()` :1527 |

### 3.8 Bug đã xác định: `status = NULL`

`cancelBooking()` nhánh 3 (:2226-2284) khởi tạo `$statusUpdate = null` rồi chỉ gán trong các nhánh `if` cho `status ∈ {0, 1, 2}`. Với booking đã ở `4`, `6`, `7` **không có nhánh nào khớp** nhưng code **vẫn chạy tiếp** xuống lệnh UPDATE (:2281-2284) ⇒ ghi `status = NULL` vào DB.

Hệ quả:
- Booking biến mất khỏi mọi truy vấn `whereIn('status', …)` — kể cả `countTotalBookingStatus()` ⇒ đếm sai.
- `getTextBookingStatus(null)` rơi vào `default` ⇒ app hiện chuỗi rỗng.
- Không thể phục hồi qua UI.

Kích hoạt: gọi `EP-P14` hai lần liên tiếp trên cùng `booking_id` (lần 1 → `4`, lần 2 → `NULL`). Vì endpoint **không xác thực và không CSRF**, ai cũng gây được. Confidence: **Cao**.

---

## 4. Luồng huỷ và luồng duyệt 承認/否認

### 4.1 Hai chế độ 「承認」 độc lập

`calendar_setting_send_messages` có **hai hàng** cho mỗi calendar, phân biệt bằng cột `moment`:

| `moment` | Cột `approve_type` điều khiển | Ảnh hưởng |
|---|---|---|
| `'booking'` | `1` = 自動承認 (đặt xong là xác nhận), `2` = 承認制 (chờ Admin duyệt) | Trạng thái khởi tạo `1` hay `0` |
| `'cancel'` | `1` = huỷ tự động, `2` = huỷ phải được duyệt | Huỷ đi thẳng `4` hay dừng ở `5` |

> 🔴 Với `moment = 'booking'`, giá trị `approve_type` **không được server đọc lại từ DB** trong `order()` — nó lấy từ `$request->approve_type` do client gửi (`CalendarController.php:1440`, `:1546-1550`). Server **chỉ** đọc từ DB ở `sendActionBooking()` (luồng Admin) và ở `checkCanBooking()` (cho `limit_book_each_customer`). Xem BR-P03.
> Với `moment = 'cancel'`, `approve_type` **được đọc từ DB** (`:2237`) ⇒ luồng huỷ an toàn hơn luồng đặt.

### 4.2 Luồng huỷ do LINE User (`EP-P14 cancelBooking` :2157-2389)

```
đọc booking theo id  (KHÔNG kiểm null, KHÔNG kiểm chủ sở hữu)
│
├─ status == 3 → NHÁNH 1: 「キャンセル待ち」を解除
│     booking->delete()                      // xoá MỀM
│     countTotalBookingStatus()
│     xoá mobile_notifies (lesson_booking_id, type=calendar_lesson, is_confirm=0, status=1)
│     recountAppBadgeNotify(getBotId())
│     → {"status":true,"delete_booking":true}
│
├─ status == 5 → NHÁNH 2: rút lại yêu cầu huỷ
│     status ← 2 nếu booking.admin_id có giá trị, ngược lại 1
│     user_update_time ← now()
│     → {"status":true,"cancel_request_booking":true,"status_order":1|2}
│     ⚠ KHÔNG countTotalBookingStatus, KHÔNG history, KHÔNG thông báo
│     ⚠ KHÔNG có client nào gọi (nghi vấn #1 — xem §9 BR-P14)
│
└─ còn lại → NHÁNH 3: luồng huỷ chuẩn
      1. đọc calendar_setting_send_messages moment='cancel'
      2. nếu deadline_cancel_booking_type == 2 → checkIsValidCancel()
            sai → throw 「キャンセルできません。」
      3. ánh xạ trạng thái (§3.6 T-11/T-12/T-13; T-21 nếu status ∈ {4,6,7})
      4. UPDATE booking.status + user_update_time
      5. INSERT calendar_course_booking_history_actions
      6. countTotalBookingStatus(reception_id)
      7. insertNotifyLesson(booking, 'autoCancel' | 'requestCancel')
      8. CalendarGoogleSheetService::updateStatusBooking(bookingId)
      9. nếu cancel approve_type == 1 → XOÁ event_step_time chưa gửi
           (user_booking_id = booking.id, bot_id, status = 0, event_step.type = 4)
     10. sendAction('11005' huỷ xong | '11006' yêu cầu huỷ)
     11. gửi tin LINE (message_send_end | message_send_booking)
           thành công → bots.free_send_count += 1 + updateMessageSendCount(botId, today, 3, 1)
     12. nếu status ra == 4 → sendNotifyWhenThereIsSlotEmpty(reception_id, calendar_id)
      → {"status":true,"status_order":4|5}
```

**Điểm cần lưu ý nghiệp vụ**

| # | Quan sát | Bằng chứng |
|---|---|---|
| 1 | `status = 0` (đang chờ duyệt) **huỷ được ngay**, không cần Admin duyệt, dù `moment='cancel'` cấu hình 承認制 — vì booking chưa chiếm chỗ nên không thiệt hại gì cho Admin | :2261-2284 |
| 2 | Khi huỷ từ `status = 0`, hệ thống còn **sửa ngược bản ghi lịch sử cũ** `SB_REQUEST_BOOKING_WAITING_APPROVE (2)` → `…_HISTORY (3)` để đánh dấu yêu cầu đã hết hiệu lực | :2274-2282 |
| 3 | `deadline_cancel_booking_type == 2` dùng lại **chính các cột** `before_booking_day`/`before_booking_hour`/`booking_time_from`/`booking_time_to` mà `start_receive_booking_type` cũng dùng — **chia sẻ cột giữa hai chức năng khác nhau** trên cùng hàng `moment='cancel'` (hàng `moment='booking'` là hàng khác nên không đụng nhau). Dễ nhầm khi đọc DB | :2211-2220 |
| 4 | **Không hoàn tiền tự động** khi khách huỷ. `payment_status` giữ nguyên `1`. Hoàn tiền là thao tác Admin thủ công (`EP-M08`) | toàn nhánh 3 |
| 5 | `DB::beginTransaction()`/`commit()` ở nhánh 3 **đã bị comment** (:2204, :2295) ⇒ không nguyên tử | :2204, :2295 |
| 6 | Nhánh 2 (rút lại) **không** gọi `countTotalBookingStatus()` — nhưng `5` và `1`/`2` đều chiếm chỗ nên `total_booking` không đổi; tuy vậy `total_approve`/`total_request_cancel` **sai** cho tới lần đếm lại kế tiếp | :2182-2196 |

### 4.3 Luồng duyệt 承認 / 否認 (Admin — `EP-M01`)

Xem bảng T-09…T-17 (§3.6). Trình tự chi tiết nhánh **`approveBooking`** (`Api/CalendarLessonController.php:315-374`):

```
1. Chặn nếu status_webhook ∈ {0,3,4} && payment_system == 1
     → 「決済処理を行っていますので、操作できません。」
2. Chỉ chạy khi status == 0
3. Nếu payment_status == 0 (chưa thu tiền):
     courseBookingService->payment($request, $botId, $booking)     :368
       ├ Stripe (payment_system == 0): autoPaymentIntents(secretKey theo booking.environment,
       │     amount = booking.payment_amount, customer = strip_customer_id, pm = strip_pm_id)
       │     thành công CHỈ KHI status == 'succeeded'
       └ UnivaPay (payment_system == 1):
             metaData.module = 'lesson_change_status'
             set status_webhook = 0 nếu isProcessWithWebhook
             chargeMoneyUnivapaySale() → getInfoTokenSale() → cancelCharge(authorizeChargeId)
             (huỷ khoản authorize tạm trước đó)
             ├ có webhook → checkStatusProcessCallback(bookingId, 25) poll 25 lần
             └ không webhook → getChargesSale() xác nhận
     ├ paymentStatus == false → TRẢ LỖI NGAY, KHÔNG đổi status  ✅ đúng
     ├ payment_system == 1 && isProcessWithWebhook → TRẢ {"result":"ok"} NGAY,
     │    KHÔNG đổi status — phó thác cho webhook callbackChangeStatusBooking  ⚠
     └ ngược lại → booking.update(charge_id, payment_status = 1)
                   GoogleSheet::updateStatusPaymentBooking()
4. changeStatusBooking(1, [bookingId])
5. sửa bản ghi lịch sử SB_REQUEST_BOOKING_WAITING_APPROVE (2) → …_HISTORY (3)
6. addActionRemind(booking, botId, reception)   → ghi event_step_time
7. INSERT history: status 4 SB_REQUEST_BOOKING_APPROVE, reason 予約リクエスト 承認, admin_id = Auth::id()
8. sendMessage(action, moment, booking, executeAction, bot) nếu có line_user_id
9. insertNotifyLesson(booking, action) nếu statusOld != statusNew
--- cuối method, luôn chạy ---
10. CalendarGoogleSheetService::updateStatusBooking()
11. countTotalBookingStatus()
```

**Rủi ro nghiệp vụ trong luồng duyệt**

| # | Vấn đề | Bằng chứng |
|---|---|---|
| 1 | **Duyệt xong mới thu tiền, không giữ chỗ trước** — giữa lúc khách gửi yêu cầu và lúc Admin duyệt, slot có thể đã đầy bởi người đặt 自動承認. `approveBooking` **không kiểm tra sức chứa** ⇒ duyệt luôn ⇒ overbooking | `Api/…:315-374` |
| 2 | **Nhánh UnivaPay + webhook trả `ok` sớm**: tiền đã charge nhưng `status` vẫn `0`, chờ webhook `module = lesson_change_status`. Webhook không về ⇒ đã trừ tiền mà booking không được duyệt, và Admin bị khoá thao tác (`status_webhook = 0`) | `Api/…:328-336`, `Service:437-441` |
| 3 | **Không có transaction** bao quanh (thu tiền + đổi trạng thái + ghi lịch sử) | toàn method |
| 4 | Cặp (status, action) không khớp ⇒ **im lặng trả `{"result":"ok"}`** mà không làm gì | `Api/…:471-476` |
| 5 | `denyBooking` (0 → 6) **không hoàn tiền** — nhưng `status = 0` thường có `payment_status = 0` nên không có tiền để hoàn. Trừ khi client đã gửi `checkHasPayment` + `approve_type=1` lệch nhau | `Api/…:372-380` |
| 6 | `approveCancel` gọi `sendNotifyWhenThereIsSlotEmpty()` **trước** `countTotalBookingStatus()` (chạy cuối method) ⇒ người 「キャンセル待ち」 nhận tin trong khi `total_booking` vẫn còn cũ; nếu họ bấm ngay có thể thấy 「予約がいっぱいです」 | `Api/…:382-392` vs `:466-469` |

---

## 5. 「キャンセル待ち」 — đăng ký nhận thông báo khi kín chỗ

### 5.1 Lưu ở đâu

**Không có bảng riêng.** Đăng ký chờ chỗ là **một hàng `calendar_course_bookings` với `status = 3`** (`SB_REQUEST_BOOKING_WAIT_CANCEL`), cùng `reception_id` + `line_user_id` như booking thật. Số lượng được đếm vào `calendar_course_receptions.total_request_booking_wait_cancel`.

Hệ quả thiết kế:
- Một khách chỉ có **một** đăng ký/slot (mọi truy vấn dùng `where(reception_id) + where(line_user_id) + where(status,3)->first()`).
- Bản ghi này **không chiếm chỗ** (`total_booking` không tính `status = 3`).
- Khi khách đặt thật, bản ghi **được tái sử dụng — UPDATE đè** thay vì tạo mới (T-05, T-06, T-07) ⇒ **mất dấu vết** rằng người này từng chờ chỗ.

### 5.2 Điều kiện bật

| Cấp | Cột | Ý nghĩa |
|---|---|---|
| Calendar | `calendar_management.is_notify_full_slot` | `0` ⇒ `EP-P12` với `register_notify_slot` ném lỗi 「この機能は現在利用できませんん。」 code `3` |
| Calendar | `calendar_management.is_display_course_full` | Slot kín có hiện trên lịch không (`getListTimeWeek` :2798-2800) |
| Slot | `type_limit_booking == 1` + hết chỗ | `is_can_booking = false` nhưng slot **vẫn hiện** nếu `is_notify_full_slot = 1` (:2794-2801) |

### 5.3 Đăng ký (`EP-P12` với `register_notify_slot = 'true'`)

```
1. Kiểm calendar.is_notify_full_slot != 0, ngược lại throw code 3        :1462-1464
2. BỎ QUA checkCanBooking() hoàn toàn                                     :1474
   ⇒ không kiểm khoá học có hiển thị, không kiểm hạn nhận đặt,
     không kiểm trần số lần đặt/khách
3. amount ép về 0                                                        :1476-1478
4. status = 3, history = 11 SB_REQUEST_BOOKING_WAIT_ANOTHER_CANCEL,
   reason = 「キャンセル待ち 登録」                                         :1541-1545
5. payment_status theo checkHasPayment (thường = 2 SP_NO_PAYMENT)
6. countTotalBookingStatus()
7. BỎ QUA insertNotifyLesson() và addActionRemind()                       :1718-1731
   ⇒ Admin KHÔNG nhận push khi có người đăng ký chờ chỗ
8. sendAction(calendar.action_id_notify_full_slot, …, code '11009')       :1758-1762
9. gửi LINE calendar.message_notify_full_slot nếu use_message_notify_full_slot == 0
   typeMessageAction = MessagesV2::ACTION_REQUEST_FULL_SLOT
10. BỎ QUA Google Sheet (`&& !$register_notify_slot`)                     :1862
```

**Chặn trùng**: nếu client gửi `bookingType != 'notify'` nhưng đã tồn tại bản `status = 3` của khách ở slot đó **và** slot vẫn kín (`type_limit_booking == 1 && total_booking >= total_person`) ⇒ trả 「キャンセル待ち通知受け取りがすでに登録されています。」 (:1525-1542).

> ⚠ Nếu slot **đã có chỗ trống trở lại**, nhánh trên không chặn mà rơi vào luồng UPDATE đè ⇒ đăng ký chờ chỗ **âm thầm biến thành booking thật**. Đúng ý đồ UX, nhưng khách bấm 「通知を受け取る」 lần hai lại thành đặt chỗ — cần đọc kỹ `bookingType` client gửi. Confidence: Cao.

### 5.4 Huỷ đăng ký (`EP-P14` nhánh 1, màn L20)

Xoá **mềm** bản ghi + xoá các `mobile_notifies` chưa đọc liên quan + `recountAppBadgeNotify()`. Không ghi lịch sử. (`:2165-2181`)

### 5.5 Ai bắn thông báo khi có chỗ trống

Toàn bộ do **`CalendarCourseBookingService::sendNotifyWhenThereIsSlotEmpty($receptionId, $calendarId, $userLoginId = null)`** (`:1292-1355`) — **chạy đồng bộ trong request**, **không qua queue**, **không có job Spring Boot**.

Luồng:
```
1. calendar.is_notify_full_slot == 0 → return (không gửi)
2. userLoginId ?: Auth::id()     ← dùng lấy Session profiles_selected_{botId}_{userId}
3. reception không tồn tại → return
4. reception.received_booking_date + start_time đã QUA → return
5. lấy TẤT CẢ booking status = 3 của reception đó
6. với mỗi người:
     - nếu calendar.use_message_notify_not_full == 0 && message_notify_not_full có nội dung
         → replaceContentCalendar() → messageService->createMessageV2() gửi LINE
     - nếu calendar.action_id_not_full → sendAction(…, code '11009')
```

**4 nơi gọi** `sendNotifyWhenThereIsSlotEmpty()`:

| Nơi gọi | Ngữ cảnh | Bằng chứng |
|---|---|---|
| `EP-P14 cancelBooking` | Khách huỷ và trạng thái ra là `4` | `CalendarController.php:2376-2379` |
| `EP-M01 approveCancel` | Admin duyệt yêu cầu huỷ (`5` → `4`) | `Api/…:387` |
| `EP-M01 adminCancel` | Admin chủ động huỷ (`1`/`2` → `7`) | `Api/…:449` |
| `EP-M11 course-reception/update` | Admin **tăng sức chứa** slot đang kín, hoặc đổi sang không giới hạn | `Api/…:1508-1512` |

**Không gọi ở**: `denyBooking` (không cần — `status 0` không chiếm chỗ), `EP-P13 deleteOrderConfirmFail` (**xoá cứng booking đang chiếm chỗ mà không báo cho ai** ⚠), `deleteOrderError()` (thanh toán hỏng, cũng không báo ⚠), xoá reception/course từ portal Admin (ngoài phạm vi).

**Vấn đề đã xác định**

| # | Vấn đề | Hệ quả | Bằng chứng |
|---|---|---|---|
| 1 | **Gửi cho TẤT CẢ người chờ cùng lúc**, không xếp hàng, không giữ chỗ tạm | 10 người chờ, 1 chỗ trống ⇒ 10 người nhận tin, 9 người bấm vào gặp 「予約がいっぱいです」. Không có khái niệm "ưu tiên người đăng ký trước" | `:1319-1355` |
| 2 | **Bản ghi `status = 3` không bị xoá sau khi gửi** | Cùng một người sẽ nhận tin **lại** ở mọi lần huỷ tiếp theo của slot đó cho tới khi tự huỷ đăng ký | `:1319-1355` |
| 3 | **Chạy đồng bộ trong request huỷ** | Slot có 100 người chờ ⇒ request huỷ của khách phải gửi 100 tin LINE trước khi trả về ⇒ timeout. Không rate limit, không queue | `:1319` |
| 4 | Dùng `Session::get('profiles_selected_…')` để chọn 送信者プロフィール | Ở luồng **LINE User** (`EP-P14`) không có session Admin ⇒ `Auth::id()` null ⇒ khoá session không khớp ⇒ **profile gửi luôn rỗng**, tin đi bằng profile mặc định. Ở luồng Admin app cũng không có session web ⇒ tương tự | `:1303-1327` |
| 5 | Biến `$calendar` bị **gán đè bên trong vòng lặp** (`$calendar = CalendarManagement::find($calendarId)`) | Vô hại về kết quả nhưng thực hiện 1 query thừa mỗi người nhận | `:1332` |
| 6 | Không kiểm tra **slot có thật sự còn chỗ** trước khi bắn | Ở `EP-M11`, nếu Admin đổi `type_limit_booking` sang `0` rồi lại về `1`, vẫn có thể bắn tin sai | `Api/…:1508-1512` |

---

## 6. Thanh toán

### 6.1 Chọn cổng thanh toán

| Cấu hình | Nguồn | Ý nghĩa |
|---|---|---|
| `calendar_management.is_use_payment` | DB | Calendar có bật thanh toán không. **Bị ép `0`** khi `bot_contracts.contract_type == 'free'` — nhưng chỉ trên object PHP, **không ghi DB** (`CalendarController.php:96-102`) |
| `calendar_management.type_payment` | DB | `0` = Stripe, `1` = UnivaPay. Ghi vào `calendar_course_bookings.payment_system` |
| `calendar_management.environment` | DB | `0` = test, `1` = live. Ghi vào `calendar_course_bookings.environment` — **snapshot tại thời điểm đặt**, nên hoàn tiền sau này vẫn dùng đúng khoá |
| `strip_bots.*` | DB theo `bot_id` | `strip_secret_test_key`, `strip_secret_live_key`, `univapay_app_id/token/secret` (test + live), `univapay_webhook_id`, `status_webhook` |

`isProcessWithWebhook($stripBot)` (`app/Helpers/functions.php:138-147`) = true khi bot **có** `univapay_webhook_id` **và** `strip_bots.status_webhook == 1`.

### 6.2 Ma trận 4 luồng thanh toán

| Cổng | `approve_type` | Thu tiền lúc nào | Booking tạo lúc nào | Giữ chỗ | Endpoint |
|---|---|---|---|---|---|
| Stripe | `1` 自動承認 | **Ngay** — `paymentIntents(confirm=true, setup_future_usage='off_session')` | Pha 1 (`handleKeepSlot`) | ✅ nguyên tử | `EP-P10` |
| Stripe | `2` 承認制 | **Sau khi Admin duyệt** — `autoPaymentIntents(off_session=true)` trong `EP-M01` | Pha 2 (`order()`) | ❌ không giữ | `EP-P10` → `EP-P12` → `EP-M01` |
| UnivaPay | `1` | **Ngay** — `chargeMoneyUnivapaySale()` | Pha 1 (`handleKeepSlot` **luôn chạy**) | ✅ nguyên tử | `EP-P11` |
| UnivaPay | `2` | Ngay ở pha 1 **cũng chạy `handleKeepSlot`** ⇒ hành vi khác Stripe | Pha 1 | ✅ | `EP-P11` :1086 |

> 🐛 **Bất đối xứng Stripe vs UnivaPay**: với `approve_type = 2`, Stripe chỉ lưu thẻ (`setupIntent`) còn UnivaPay **thu tiền luôn**. Cùng một cấu hình 承認制, khách trả tiền trước hay sau tuỳ vào cổng Admin chọn. Confidence: Cao (`:924` vs `:1086`).

### 6.3 Stripe — chi tiết

**Đặt + thu ngay** (`EP-P10`, `approve_type = 1`):
1. `createCustomer()` nếu client không gửi `customer_id`; lỗi → `getMessageError()` (từ điển 16 mã Stripe → tiếng Nhật, `:815-846`).
2. `attachPaymentMethodToCustomer($secretKey, $pmId, $customerId)` (`StripePayment.php:260`).
3. `handleKeepSlot()` — giữ chỗ nguyên tử + INSERT booking.
4. `paymentIntents(secretKey, amount, metaData{module:'lesson', booking_id: Hashids, bot_id: Hashids, booking_type}, description, customerId, pmId, email, onSession=false)` — `confirm => true`, `setup_future_usage => 'off_session'` (`StripePayment.php:337-374`).
5. Kết quả:
   - **Exception** ⇒ `deleteOrderError()` **forceDelete booking** + `countTotalBookingStatus()` ⇒ **rollback đầy đủ** ✅ (`:966-971`).
   - `status != 'succeeded'` (cần 3-D Secure) ⇒ trả `client_secret` + `isConfirm = true`; **booking vẫn nằm trong DB, vẫn chiếm chỗ**. Client tự làm 3DS; hỏng thì **phải tự gọi `EP-P13`** để rollback. Nếu client không gọi ⇒ **slot leak** (§2.4).
   - `succeeded` ⇒ `UPDATE charge_id`.

**Thu sau khi duyệt** (`EP-M01 approveBooking` → `CalendarCourseBookingService::payment()` :398-423): `autoPaymentIntents(off_session = true)`, **không** metadata (nên webhook Stripe không map được về booking). Chỉ coi là thành công khi `responseIntent->status == 'succeeded'`.

**Hoàn tiền** (`EP-M08`, `refundType == 'now'`): `setApiKey($secretKey)` rồi `\Stripe\Refund::create(['payment_intent' => $chargeId])` (`StripePayment.php:209-231`). **Toàn phần, không hỗ trợ hoàn một phần.**

### 6.4 Nghi vấn #3 — nhánh `isPaymentAfter` không rollback

**Kết luận: nhánh này KHÔNG CÓ GÌ ĐỂ ROLLBACK — nhưng đó chính là vấn đề.** Confidence: **Cao** (đọc `:985-1010`).

Bằng chứng: khi `approve_type != 1`, `EP-P10` đi vào `else` (`:985`), đặt `isPaymentAfter = true`, gọi **chỉ** `setupIntent()`. Biến `$bookingId` **giữ nguyên `null`** suốt nhánh — không `handleKeepSlot()`, không INSERT, không tăng `total_booking`.

Hệ quả dây chuyền:

| # | Tình huống | Hành vi thực tế |
|---|---|---|
| 1 | `setupIntent` thất bại | Trả `status = 'error'` + `errorMessage`. Không có booking ⇒ không cần rollback. **Đúng.** |
| 2 | `setupIntent` cần 3-D Secure (`status != 'succeeded'`) ⇒ `isConfirm = true` + `client_secret`, nhưng response cũng trả **`bookingId = null`** | Client làm 3DS; **nếu hỏng** và client gọi `EP-P13` với `bookingId = null` ⇒ `where('id', null)->forceDelete()` khớp **0 hàng**, vẫn trả `{"status": true}`. Rollback là **no-op giả thành công** |
| 3 | 3DS hỏng nhưng client **vẫn** gọi `EP-P12 order` | Booking `status = 0`, `payment_status = 0` được tạo với `strip_pm_id` **chưa hề được xác minh là dùng được**. Không ai biết cho tới khi Admin duyệt |
| 4 | Admin duyệt sau vài ngày, thẻ hết hạn / hết hạn mức | `payment()` trả `paymentStatus = false` ⇒ `EP-M01` trả lỗi, **status vẫn `0`**. Khách **không được thông báo gì**, slot có thể đã bị người khác lấy mất |
| 5 | Slot đầy giữa lúc gửi yêu cầu và lúc duyệt | `approveBooking` **không kiểm sức chứa** ⇒ vẫn duyệt ⇒ overbooking (§4.3 #1) |

⇒ Rủi ro thật không nằm ở "thiếu rollback" mà ở **thiếu giữ chỗ + thiếu xác minh thẻ + thiếu phản hồi cho khách** ở toàn bộ luồng 承認制 + Stripe. Xem §10 RP-03.

### 6.5 UnivaPay — chi tiết

**Chuẩn bị thẻ (client-side)**
1. `EP-P08 call-create-customer-id` — sinh `customerCode = 'calendar' . str_random(20)`, gọi `POST https://api.univapay.com/stores/{appId}/create_customer_id`, header `Authorization: Bearer {secret}.{token}`.
2. Client dùng UnivaPay JS widget lấy `transaction_token_id`.
3. `EP-P09 get-info-card-event-booking` — đổi token lấy `last4`/`brand`/`expired_card`/`authorizeChargeId`.

**Thu tiền** (`EP-P11` :1105-1194)
```
handleKeepSlot()  (LUÔN chạy — kể cả approve_type = 2)
chargeMoneyUnivapaySale(botKey, 1, token, amount, customerId, environment, null, metaData)
   metaData = {module:'lesson', booking_id: Hashids, bot_id: Hashids, booking_type,
               transaction_token_id, univapay_customer_code, shipping_details}
UPDATE booking.charge_id
├─ !success → errorMessage (JP) + isDeleteBooking = true
├─ isProcessWithWebhook:
│    checkStatusProcessCallback(bookingId)  — poll 5 lần × sleep(1s)
│      ├ status_webhook = 2 ERROR   → lỗi + xoá booking
│      ├ status_webhook = 0 chưa có → set 4 TIMEOUT_WEBHOOK, trả {"status":"pending"} (màn L18)
│      └ khác                        → success
└─ không webhook:
     getChargesSale() → thất bại && status == 'failed' → xoá booking
     nếu tổng thời gian > 120s → gửi tin LINE cảnh báo cho khách
```

**Webhook — đường đi đầy đủ** (đã truy vết, đính chính `api-spec-public.md` §4)

```
UnivaPay  ──POST──►  /mobile/univapay-callback-payment          routes/web.php:4067
                     WebhookUnivapayControler@webhook           (KHÔNG middleware, KHÔNG chữ ký)
                     └ lọc metadata.module ∈ {lesson, lesson_change_status, salon, …}
                       và event == 'charge_finished'
                     └ HandleWebhookUnivapay::dispatch($data, 'univapay')   → QUEUE
                                     │
        ┌────────────────────────────┴────────────────────────────┐
   module = 'lesson'                                    module = 'lesson_change_status'
   CalendarCourseBookingService::handleOrderCallback()   ::callbackChangeStatusBooking()
   (:1527)  — chốt booking do LINE User tạo              (:641) — chốt duyệt do Admin bấm
```

**`handleOrderCallback()` — logic chống lặp và chống lạc** (`:1527-1700`)

| Bước | Xử lý |
|---|---|
| 1 | `getDataCallback()` giải Hashids `metadata.booking_id` / `bot_id` (:1485-1525) |
| 2 | Booking không tồn tại ⇒ return im lặng |
| 3 | Calendar không khớp `bot_id` ⇒ return im lặng ✅ (nơi **duy nhất** trong FA-019 có kiểm tra chéo bot) |
| 4 | `status_webhook ∈ {1 PROCESSED, 2 ERROR}` ⇒ return — **chống xử lý lặp** ✅ |
| 5 | `status_webhook == 3 TIMEOUT` **và** không có `data['from_job']` ⇒ return |
| 6 | `statusPayment != 'successful'` ⇒ `status_webhook = 2`, ghi `error_message`/`error_code`, **`status = 7 SB_BOOKING_ADMIN_CANCEL`**, `payment_status = 2 SP_NO_PAYMENT` |
| 7 | Nếu trạng thái cũ là `3 TIMEOUT` (có `from_job`) hoặc `4 TIMEOUT_WEBHOOK` ⇒ **forceDelete booking** |
| 8 | `countTotalBookingStatus()` để trả chỗ |
| 9 | Nếu quá 120s kể từ `created_on` ⇒ gửi tin LINE 「決済に失敗しました。…」 |
| 10 | Thành công ⇒ `payment_status = 1`, `status = 1`, `charge_id`, `status_webhook = 1` + toàn bộ side effect như `order()` |

> ⚠ Ở bước 6, thanh toán hỏng làm booking mang `status = 7` (**手動予約キャンセル** — "Admin huỷ") dù Admin **không hề đụng tới**. Lịch sử vận hành bị bóp méo. Confidence: Cao (`:1573-1578`).

**Hoàn tiền UnivaPay** (`EP-M08`): `refundMoney(botKey, charge_id, (int)amount, environment)` rồi `getRefundMoney()` xác nhận. Số tiền = **toàn bộ `booking.payment_amount`** — không có hoàn một phần.

### 6.6 Hoàn tiền — điều chưa làm

| # | Quan sát | Bằng chứng |
|---|---|---|
| 1 | Hoàn tiền **không đổi `status`** — booking vẫn 「予約確定」, **vẫn chiếm chỗ**. Admin phải huỷ riêng bằng `adminCancel` | `Api/…:1125-1131` |
| 2 | **Không kiểm tra `payment_status` hiện tại** ⇒ gọi lại nhiều lần. `charge_id` rỗng ⇒ bỏ qua toàn bộ khối gọi cổng nhưng **vẫn đánh dấu `SP_REFUND`** | `Api/…:1057`, `:1125` |
| 3 | `refundType != 'now'` = 「決済システムから返金」 — chỉ ghi nhận, **không gọi cổng**. Admin tự hoàn ở dashboard Stripe/UnivaPay. Không có đối soát | `Api/…:1122-1124` |
| 4 | `botKey` lấy theo `botId` **client gửi**, không đối chiếu `booking.calendar.bot_id` ⇒ có thể dùng khoá Stripe của bot khác | `Api/…:1062`, `:1085` |
| 5 | **Không có hoàn tiền tự động** khi khách huỷ, kể cả huỷ trước hạn | `CalendarController.php:2198-2389` |

### 6.7 Nghi vấn #2 — server có kiểm tra lại `checkHasPayment` không?

**Kết luận: KHÔNG.** Đã được `api-spec-public.md` §3.1 S-04 xác minh; ở tầng nghiệp vụ bổ sung ba điểm:

1. `checkHasPayment` là **chuỗi/boolean client gửi**, so sánh `=== true || === 'true'` (`:1468`, `:1487`). Không nơi nào đối chiếu `calendar_management.is_use_payment` hay `calendar_course.amount > 0`.
2. Gửi `checkHasPayment = false` ⇒ nhánh `:1470-1486` **xoá sạch** mọi trường thẻ, đặt `payment_status = 2 (SP_NO_PAYMENT)` — trạng thái dành cho khoá học **miễn phí** — rồi tạo booking `status = 1` 「予約確定」 bình thường.
3. `payment_amount` cũng lấy thẳng từ `$request->amount`, **không đối chiếu `calendar_course.amount`** (`:1596-1622`). Kể cả khi trả tiền thật, khách có thể tự đặt giá.

⇒ Đây là **rủi ro nghiêm trọng nhất của toàn tính năng**: đặt lớp học có phí mà **không mất một đồng**, và Admin nhìn vào app chỉ thấy nhãn 「決済なし」 — trùng với khoá miễn phí hợp lệ, **không có dấu hiệu bất thường nào**. Xem §10 RP-01.

---

## 7. Ghi queue & side effect

### 7.1 Bảng tổng hợp side effect theo hành động

| Hành động | `event_step_time` | `mobile_notify` | `t_actions` (`sendAction`) | Tin LINE cho khách | Google Sheet | Hồ sơ bạn bè |
|---|---|---|---|---|---|---|
| `EP-P12` đặt, `approve_type = 1` | **INSERT** (`addActionRemind`) | INSERT `autoApprove` | `11001` | `message_send_after_booking` (course) ưu tiên, fallback `message_send_end` | `insertDataToGoogleSheet` | **UPDATE đè** |
| `EP-P12` đặt, `approve_type = 2` | không | INSERT `requestBooking` | `11002` | `message_send_booking` | `insertDataToGoogleSheet` | **UPDATE đè** |
| `EP-P12` đăng ký 「キャンセル待ち」 | không | **không** | `11009` | `message_notify_full_slot` | **không** | **UPDATE đè** |
| `EP-P14` huỷ (cancel `approve_type = 1`) | **DELETE** (chưa gửi) | INSERT `autoCancel` | `11005` | `message_send_end` | `updateStatusBooking` | không |
| `EP-P14` xin huỷ (cancel `approve_type = 2`) | không đụng | INSERT `requestCancel` | `11006` | `message_send_booking` | `updateStatusBooking` | không |
| `EP-P14` nhánh 1 (huỷ đăng ký chờ) | không | **DELETE** `mobile_notifies` chưa đọc | không | không | không | không |
| `EP-P14` nhánh 2 (rút yêu cầu huỷ) | không | không | không | không | **không** ⚠ | không |
| `EP-P13` xoá khi 3DS hỏng | **không dọn** ⚠ | **không dọn** ⚠ | không | không | **không** ⚠ | không |
| `EP-M01 approveBooking` | **INSERT** | INSERT `approveBooking` | qua `sendMessage()` | theo `moment` | `updateStatusPaymentBooking` + `updateStatusBooking` | không |
| `EP-M01 denyBooking` | không (chưa từng có) | INSERT `denyBooking` | qua `sendMessage()` | theo `moment` | `updateStatusBooking` | không |
| `EP-M01 approveCancel` | **DELETE** (chưa gửi) | INSERT `approveCancel` | qua `sendMessage()` | theo `moment` | `updateStatusBooking` | không |
| `EP-M01 denyCancel` | không | INSERT `denyCancel` | qua `sendMessage()` | theo `moment` | `updateStatusBooking` | không |
| `EP-M01 requestCancel` | không | INSERT `requestCancel` | qua `sendMessage()` | theo `moment` | `updateStatusBooking` | không |
| `EP-M01 adminCancel` | **DELETE** (chưa gửi) | INSERT `adminCancel` | qua `sendMessage()` | theo `moment` | `updateStatusBooking` | không |
| `EP-M08 order-refund` | không | **không** ⚠ | không | **không** ⚠ | `updateStatusPaymentBooking` | không |
| `EP-M15 add-booking` | **INSERT** | INSERT `autoApprove` | `sendActionBooking` `11001`/`11003` | theo cấu hình | `insertDataToGoogleSheet` | **UPDATE đè** |
| Webhook `handleOrderCallback` thành công | **INSERT** | INSERT | có | có | có | — |
| Webhook `handleOrderCallback` thất bại | không | không | không | 「決済に失敗しました。」 nếu > 120s | không | — |

> ✅ **Đóng khoảng trống G7 của `job-spec.md`**: `autoCancel` phía LINE User (`EP-P14` nhánh 3, cancel `approve_type == 1`) **CÓ xoá** `event_step_time` (`CalendarController.php:2296-2310`). `denyBooking` **không xoá** nhưng cũng **không cần** — `status = 0` chưa bao giờ chạy `addActionRemind()` nên chưa có bản ghi nào. `requestCancel` (→ `5`) không xoá là **đúng nghiệp vụ** vì huỷ chưa được chấp thuận. Confidence: **Cao**.

### 7.2 `event_step_time` — hàng đợi nhắc lịch

**Ghi**: `CalendarCourseBookingService::addActionRemind($booking, $botId, $reception)` (`:529-640`).

```
1. tìm events WHERE booking_calendar_id = calendar_id AND bot_id AND type = 4
   không có → không làm gì
2. lấy tất cả event_step của event đó
3. với mỗi event_step, tính sent_date_time theo type_remind:
     type_remind = 1 「日付指定」:
        is_after_day = 1 → sent = (date + event_step.time_send) + before_day ngày
                            và yêu cầu start_time > sent  (nhắc SAU buổi học)
        is_after_day = 0 → sent = (date + time_send) − before_day ngày
                            và yêu cầu start_time < sent  (nhắc TRƯỚC buổi học)
     type_remind = 2 「カウントダウン」:
        is_after_day = 1 → sent = end_time  + hh:mm của time_send
        is_after_day = 0 → sent = start_time − hh:mm của time_send
4. chỉ INSERT khi sent_date_time >= thời điểm hiện tại
5. lọc theo khoá học: is_use_filter_course == 1 && course_ids không chứa booking.course_id → bỏ qua
6. INSERT event_step_time { event_id, event_step_id, bot_id, user_id = NULL,
                            user_booking_id = booking.id, sent_date_time }
```

**Xoá**: 3 nơi, cùng một mẫu truy vấn 3 tầng:
```
event_step_time WHERE user_booking_id = booking.id AND bot_id AND status = 0
  → pluck(event_step_id)
  → event_step WHERE id IN (…) AND type = 4  → pluck(id)
  → event_step_time DELETE WHERE event_step_id IN (…) AND user_booking_id AND status = 0
```
Nơi gọi: `EP-P14` (`CalendarController.php:2296-2310`), `EP-M01 approveCancel` (`Api/…:381-392`), `EP-M01 adminCancel` (`Api/…:449-460`).

**Vấn đề**

| # | Vấn đề | Bằng chứng |
|---|---|---|
| 1 | Toàn bộ `addActionRemind()` bọc trong `try/catch` chỉ `Log::error` — **nuốt lỗi im lặng**. Insert hỏng ⇒ booking vẫn thành công nhưng **mất nhắc lịch**, không ai biết | `:636-639` |
| 2 | Chỉ xoá bản ghi `status = 0`. Nếu job Spring Boot **vừa nhặt** (đã đổi `status = 1`) thì huỷ không kịp ⇒ **khách đã huỷ vẫn nhận tin nhắc lịch** | `:2296-2310` + `job-spec.md` R10 |
| 3 | `user_id = NULL` — định danh người nhận **hoàn toàn** qua `user_booking_id`. Nếu booking bị `forceDelete` (`EP-P13`, `deleteOrderError`) ⇒ `event_step_time` **mồ côi**, job phải tự chịu | `:625-631` |
| 4 | `EP-P13 deleteOrderConfirmFail` **không dọn** `event_step_time` — nhưng ở luồng đó `addActionRemind` chưa chạy (nó ở pha 2) nên thực tế chưa có bản ghi. **Trừ khi** client gọi `EP-P13` **sau** `EP-P12` ⇒ đúng là để lại rác | `:1371-1384` |

### 7.3 `mobile_notify` — thông báo cho Admin

**Ghi**: `MobileNotifyService::insertNotifyLesson($booking, $action)` (`app/Services/Notify/MobileNotifyService.php:121+`).

| `$action` | Nội dung 「」 | `setting_value` |
|---|---|---|
| `autoApprove` | [予約が入りました] {calendar} /{date} {HH:mm} / {course} | `CALENDAR_LESSON_BOOKED` |
| `requestBooking` | [予約リクエストが入りました] … | `CALENDAR_LESSON_BOOKING_REQUEST` |
| `approveBooking` | [予約リクエストを承認しました] … | `CALENDAR_LESSON_BOOKING_APPROVE` |
| `denyBooking` | [予約リクエストを否認しました] … | `CALENDAR_LESSON_BOOKING_DENY` |
| `autoCancel` / `adminCancel` | [予約がキャンセルされました] … | `CALENDAR_LESSON_BOOKING_CANCEL` |
| `requestCancel` | [キャンセルリクエストが入りました] … | `CALENDAR_LESSON_REQUEST_BOOKING_CANCEL` |
| `approveCancel` | [キャンセルリクエストを承認しました] … | `CALENDAR_LESSON_APPROVE_BOOKING_CANCEL` |
| `denyCancel` | [キャンセルリクエストを否認しました] … | `CALENDAR_LESSON_DENY_BOOKING_CANCEL` |

Bản ghi: `notify_title = 'レッスン予約'`, `type = config('sns-line.type_of_notification_key.calendar_lesson')`, `notify_badge = -1`, `lesson_booking_id = booking.id`, `line_user_id`, `line_user_name`, `bot_id` (lấy từ `calendar.bot_id`, **không tin client** ✅).

`courseName = course.system_name ?: course.course_name` — dùng tên nội bộ nếu Admin đặt.

**Vấn đề**

| # | Vấn đề |
|---|---|
| 1 | **Không có nhánh cho `register_notify_slot`** ⇒ Admin **không hề biết** có người đăng ký 「キャンセル待ち」. `order()` chủ động bỏ qua (`CalendarController.php:1718`) |
| 2 | **Không có nhánh cho hoàn tiền** ⇒ `EP-M08` không sinh thông báo |
| 3 | `$action` không khớp case nào ⇒ `notifyContent` rỗng, `setting_value` rỗng ⇒ vẫn INSERT bản ghi trắng |
| 4 | `EP-P14` nhánh 1 xoá `mobile_notifies` chưa đọc rồi `recountAppBadgeNotify(getBotId())` — nhưng `getBotId()` dựa **session Admin**, mà đây là request của LINE User ⇒ **badge đếm sai / trả null**. Cùng loại bug đã ghi nhận ở `deleteFromApp` (BUG #38208). Confidence: **Trung bình** |

### 7.4 `t_actions` — mã hành động (`sendAction`)

Chữ ký: `sendAction($actionId, $lineUserId, $botId, $bookingId, $code, true, [], null, null, null, $calendarId, $bookingId)`.

| Mã | Ngữ cảnh | Nơi gọi |
|---|---|---|
| `11001` | Đặt chỗ được xác nhận (自動承認) | `CalendarController.php:1801`; `sendActionBooking` |
| `11002` | Gửi yêu cầu đặt chỗ (承認制) | `:1823` |
| `11003` | Admin duyệt yêu cầu đặt | `CalendarCourseBookingService::sendActionBooking` |
| `11005` | Huỷ hoàn tất | `:2318-2330` |
| `11006` | Gửi yêu cầu huỷ | `:2318-2330` |
| `11009` | 「キャンセル待ち」 — cả lúc **đăng ký** (`action_id_notify_full_slot`) lẫn lúc **báo có chỗ** (`action_id_not_full`) | `:1760`; `CalendarCourseBookingService.php:1352` |

> ⚠ `11009` **dùng lại cho hai sự kiện trái ngược** (đăng ký chờ vs báo đã có chỗ). Thống kê action không phân biệt được. Confidence: Cao.

**Ưu tiên chọn action/tin nhắn khi đặt chỗ `approve_type = 1`** (`:1780-1806`):
```
1. course.action_id_send_after_booking (nếu có ActionDetail thật)  → dùng
   course.message_send_after_booking (nếu use_message_notify_send_after_booking == 0) → dùng
2. Nếu CẢ HAI đều rỗng → fallback calendar_setting_send_messages.setting_action_id
   và message_send_end (nếu is_send_message == 0)
```
Tức **cấu hình cấp khoá học đè cấu hình cấp calendar**, và fallback chỉ xảy ra khi cấp khoá học **hoàn toàn** trống.

### 7.5 Đếm tin nhắn LINE

Mỗi lần `sendMessageAction()` trả về thành công (`$response->isSucceeded()`):
```
Bots::where('id', bot.id)->update(['free_send_count' => $bot->free_send_count + 1]);
updateMessageSendCount($botId, today, 3, 1);
```
Nơi: `order()` :1856-1861, `cancelBooking()` :2356-2374, `sendActionBooking()` `Service:1400-1405`, `handleOrderCallback()`.

> 🐛 `free_send_count + 1` dùng **giá trị đọc trong PHP** rồi ghi đè, **không phải `DB::raw('free_send_count + 1')`**. Hai request đồng thời ⇒ **mất lượt đếm** (lost update). Với tính năng công khai không rate limit, sai số tích luỹ theo thời gian. Confidence: **Cao** (`:1856-1858`).

### 7.6 Google Sheet

`CalendarGoogleSheetService` — chỉ chạy khi `calendar_management.google_sheet_id` có giá trị.

| Method | Gọi ở |
|---|---|
| `insertDataToGoogleSheet($calendar, $order)` | `EP-P12` (bỏ qua khi `register_notify_slot`), `EP-M15` |
| `updateStatusBooking($bookingId)` | `EP-P14`, `EP-M01` (cuối method, luôn chạy) |
| `updateStatusPaymentBooking($bookingId)` | `EP-M01 approveBooking`, `EP-M08 order-refund` |

**Chạy đồng bộ trong request** — API Google chậm/lỗi làm chậm hoặc hỏng luồng đặt chỗ. `EP-P12` có đo thời gian riêng (`$endtExcecuteGoogleSheet`, :1866-1876) — dấu hiệu đã từng gặp sự cố hiệu năng ở đây. Confidence: **Trung bình**.

### 7.7 Ghi đè hồ sơ bạn bè — side effect ẩn

`updateFriendInfoValue($friendInfo, $lineUser, $botId)` (`CalendarController.php:1934-2071`) chạy **mỗi lần** `EP-P12` có `friend_info_settings`:

| `friend_information_id` | Ghi vào |
|---|---|
| `-1` | `line_user.view_name` |
| `-2` | `line_user.phone_number` |
| `-3` | `line_user.email` |
| `-4` | `line_user.birthday` |
| `-6` | `line_user.province` |
| khác | `friend_information_values` (upsert theo `bot_id` + `friend_information_id`) |
| kiểu datetime | thêm `settingEventTimeFriendInfo()` — có thể kích hoạt kịch bản theo ngày |

Toàn bộ bọc `try/catch` chỉ `Log::info` (:2068-2070) ⇒ hỏng thì im lặng.

> 🔴 Đây là **ghi dữ liệu chính chủ khách hàng từ một endpoint không xác thực**. Kết hợp với việc `line_user_id` do client gửi ⇒ sửa hồ sơ bất kỳ ai. Đã ghi nhận ở `api-spec-public.md` S-06.

### 7.8 Cảnh báo giao dịch chậm

`checkExecutionTimeMoreThanTwoMinute($startTime, $endTime)` (`Service:1796`) — nếu tổng thời gian xử lý > **120 giây**, gửi tin LINE trấn an/cảnh báo cho khách:
- Thành công: `sendNotifyExecutionTimeMoreThanTwoMinute('success', $bot, $lineUser)` — gọi ở `EP-P12` (:1745-1754) khi có `charge_id` và `startTimeAction`.
- Thất bại (webhook): 「決済に失敗しました。\nカードのご利用枠や有効期限などをご確認いただき\n再度、購入手続きを行なってください。」 (`Service:1620`).

Sự tồn tại của cơ chế này là bằng chứng luồng thanh toán **thường xuyên vượt 2 phút** trong thực tế. Confidence: **Trung bình** (suy luận từ code, không có số liệu).

---

## 8. Models & hằng số liên quan

| Model | Bảng | Vai trò trong FA-019 public | Ghi chú |
|---|---|---|---|
| `App\CalendarManagement` | `calendar_management` | Cấu hình gốc: `bot_id`, `type_payment`, `environment`, `is_use_payment`, `is_notify_full_slot`, `is_display_course_full`, `filter_id_show_booking`, `action_id_notify_full_slot`, `action_id_not_full`, `message_notify_full_slot`, `message_notify_not_full`, `google_sheet_id`, `calendar_name`, `line_name` | `EP-P01` truyền **toàn bộ record** vào blade |
| `App\CalendarCourse` | `calendar_course` | Khoá học: `amount`, `course_name`, `system_name`, `course_order`, `booking_page_display`, `hour_done`, `minute_done`, `filter_id_send_after_booking`, `action_id_send_after_booking`, `message_send_after_booking`, `use_message_notify_send_after_booking` | Hằng `BOOKING_DISPLAY_ON` |
| `App\CalendarCourseReception` | `calendar_course_receptions` | Khung giờ + bộ đếm chỗ (§2.1) | `SoftDeletes`; accessor ép `start_time`/`end_time` về `H:i` và `amount` về `number_format` |
| `App\CalendarCourseBooking` | `calendar_course_bookings` | Bản ghi đặt chỗ | `SoftDeletes`; `$guarded = []` (**mass assignment mở hoàn toàn**); accessor `payment_amount` trả `number_format` ⇒ code phải `str_replace(",", "", …)` trước khi tính |
| `App\CalendarCourseBookingHistoryAction` | `calendar_course_booking_history_actions` | Nhật ký thao tác | 16 hằng `SB_*` + 13 hằng `REASON_*` (§3.6) |
| `App\CalendarSettingSendMessage` | `calendar_setting_send_messages` | **Hai hàng/calendar** theo `moment ∈ {booking, cancel}` — chứa `approve_type`, `limit_book_each_customer`, `number_limit_booking`, `start_receive_booking_type`, `deadline_receive_booking_type`, `deadline_cancel_booking_type`, `setting_action_id`, `setting_action_request`, `setting_action_approve`, `message_send_end`, `message_send_booking`, `message_send_approve`, `is_send_message*`, `text_filter_show_booking` | `EP-P03` dùng **không kiểm null** ⇒ 500 |
| `App\CalendarSettingSendForms` | `calendar_setting_send_forms` | Định nghĩa form 「お客様情報」: `question`, `sub_question`, `form_type`, `required`, `rule_type`, `rule_validation_type`, `friend_information_id`, `order`, `enable`, `can_delete`, `link_friend_information`, `enable_load_friend_information`, `display_method`, `date_form`, `recording_time` | `EP-M12` **tự tạo 2 bản ghi mặc định** nếu chưa có |
| `App\LineUser` / `App\BotLineUser` | `line_user`, `bot_line_users` | Danh tính khách; `u_code`, `is_blocked`, `view_name`, `email`, `phone_number`, `birthday`, `province` | |
| `App\StripBot` | `strip_bots` | Khoá cổng thanh toán + `status_webhook`, `univapay_webhook_id` | |
| `App\Bots` / `App\BotContracts` | `bots`, `bot_contracts` | `liff_app_id_booking`, `url_add_friend`, `free_send_count`; `contract_type`, `plan_type`, `expired_date`, `status` | `checkIsBotExpired()` :234-244 |
| `App\EventStepTime` / `App\EventStep` / `App\Events` | `event_step_time`, `event_step`, `events` | Hàng đợi nhắc lịch, `type = 4` = lesson | Xem `job-spec.md` |
| `App\MobileNotify` | `mobile_notify` | Thông báo push cho Admin | |
| `App\FriendInformationSetting` / `FriendInformationValue` | `friend_information_settings`, `friend_information_values` | Hồ sơ bạn bè tuỳ biến | |

**Hằng số controller** (`CalendarController.php:49-60`)

| Hằng | Giá trị |
|---|---|
| `MESSAGE_REACHES_MAX_BOOKING_EACH_CUSTOMER` | 「1人あたりの予約受付上限に達しています」 |
| `CODE_ERROR_COURSE_EMPTY` | `1` — 「コースが存在していません。」 |
| `CODE_ERROR_RECEPTION_NOT_EXISTS` | `2` — 「予約の時間が存在していません。」 |
| `CODE_ERROR_DISABLED_NOTIFY_FULL_SLOT` | `3` — 「この機能は現在利用できませんん。」 (**lỗi chính tả: hai ký tự ん**) |

> Lỗi 「予約がいっぱいです。別の枠を予約してください。」 và 「予約の受付を開始していません。」/「予約の受付が終了されました。」/「キャンセルできません。」 **không có hằng số** — viết thẳng chuỗi trong nhiều nơi. Sửa text phải sửa nhiều điểm.

---

## 9. Business Rules

Ký hiệu đường dẫn: `MC` = `app/Http/Controllers/Mobile/CalendarController.php`; `AC` = `app/Http/Controllers/Api/CalendarLessonController.php`; `SV` = `app/Services/CalendarManagement/CalendarCourseBookingService.php`.

### 9.1 Truy cập & hiển thị

| ID | Quy tắc | Bằng chứng | Tin cậy |
|---|---|---|---|
| **BR-P01** | Trang đặt chỗ chỉ mở khi: Hashids giải mã được, calendar tồn tại, bot tồn tại, người dùng **không** `is_blocked`, và bot **chưa hết hạn** (`plan_type == 1` && (`expired_date + 7 ngày < now` \|\| `bot_contracts.status == 3`) ⇒ 410) | `MC:80-150`, `:234-244` | Cao |
| **BR-P02** | `uCode == 'preview'` ⇒ bỏ qua toàn bộ lọc filter bạn bè và bỏ qua kiểm tra trần số lần đặt | `MC:152-154`, `:302-307`, `:2856` | Cao |
| **BR-P03** | Khoá học chỉ hiển thị khi `booking_page_display = BOOKING_DISPLAY_ON`; nếu có `filter_id_send_after_booking` thì người dùng phải thoả FilterV2 (`parent_type = 'calendar-course-setting-status-send-after-booking'`) | `MC:285-350` | Cao |
| **BR-P04** | Khung giờ bị **ẩn** khỏi lịch khi: quá hạn nhận đặt (`!is_valid_deadline_receive`), hoặc kín chỗ + `is_notify_full_slot = 0` + `is_display_course_full = 0`. Bị **hiện nhưng khoá** (`is_can_booking = false`) khi kín chỗ mà `is_notify_full_slot = 1`, hoặc chưa tới giờ mở nhận đặt | `MC:2794-2835` | Cao |
| **BR-P05** | Chế độ 「月」 **loại bỏ** slot chưa tới giờ mở nhận đặt, trong khi chế độ 「週」 chỉ **khoá** nó ⇒ hai chế độ hiển thị lệch nhau | `MC:2934-2936` vs `:2806-2816` | Cao |
| **BR-P06** | Khi tuần/tháng đang xem không có slot nào, server **tự nhảy** tối đa 4 tuần (chế độ tuần) hoặc 2 tháng (chế độ tháng), rồi nhảy thêm 1 đơn vị nữa và trả kết quả kể cả rỗng | `MC:371-405`, `:521-552` | Cao |

### 9.2 Điều kiện đặt chỗ

| ID | Quy tắc | Bằng chứng | Tin cậy |
|---|---|---|---|
| **BR-P07** | Trần số lần đặt/khách (`limit_book_each_customer = 1`) đếm booking **cùng calendar, cùng `line_user_id`, slot còn ở tương lai, `status ∈ {1, 2, 5}`**. Đạt trần khi `count >= number_limit_booking`. **Chỉ áp dụng ở luồng có `checkCanBooking()`** — bỏ qua hoàn toàn khi `register_notify_slot = true` và khi Admin đặt hộ | `MC:246-260`, `:2088-2095`, `:1474` | Cao |
| **BR-P08** | Đặt chỗ bị chặn nếu chưa tới mốc mở nhận đặt (`start_receive_booking_type = 2`) hoặc đã quá hạn (`deadline_receive_booking_type = 2`; nếu `!= 2` thì mặc định hạn = `start_time`) | `MC:2106-2142` | Cao |
| **BR-P09** | `type_limit_booking = 0` ⇒ **không giới hạn sức chứa**; `checkValidSlot()` luôn trả `true` và vẫn tăng bộ đếm | `MC:1387-1394` | Cao |
| **BR-P10** | `status = 0` (chờ duyệt) **không chiếm chỗ**; `status ∈ {1, 2, 5}` chiếm chỗ. Do đó chế độ 承認制 nhận **không giới hạn** yêu cầu | `SV:1424-1443` | Cao |
| **BR-P11** | Một khách chỉ có **một** bản 「キャンセル待ち」 mỗi slot; khi đặt thật, bản đó bị **UPDATE đè** thành booking chứ không tạo bản mới | `MC:1231-1240`, `:1518-1542`; `AC:1733-1739` | Cao |
| **BR-P12** | Đăng ký 「キャンセル待ち」 **bỏ qua toàn bộ `checkCanBooking()`** — không kiểm khoá học hiển thị, không kiểm hạn nhận đặt, không kiểm trần/khách; chỉ kiểm `calendar.is_notify_full_slot != 0` | `MC:1462-1478` | Cao |

### 9.3 Trạng thái & huỷ

| ID | Quy tắc | Bằng chứng | Tin cậy |
|---|---|---|---|
| **BR-P13** | Trạng thái khởi tạo: `register_notify_slot` ⇒ `3`; `approve_type = 1` ⇒ `1`; `approve_type = 2` ⇒ `0`; Admin đặt hộ ⇒ `2` | `MC:1541-1550`; `AC:1714-1720` | Cao |
| **BR-P14** | Khách huỷ: `moment='cancel'.approve_type = 1` ⇒ về `4` ngay; `= 2` ⇒ về `5` chờ duyệt. **Ngoại lệ**: booking đang ở `status = 0` luôn về `4` bất kể cấu hình | `MC:2231-2284` | Cao |
| **BR-P15** | Backend **có** năng lực "rút lại yêu cầu huỷ" (`5` → `1`/`2`) qua `EP-P14`, nhưng **UI khoá** năng lực này (`public/js/booking_news/booking.js:944` `cancelRequestCancel()` không được bind; màn L14 hiện text chết 「キャンセルリクエストの取り消しはできません」) | `MC:2182-2196`; `public/js/booking_news/booking.js:944` | Cao |
| **BR-P16** | Hạn huỷ (`deadline_cancel_booking_type = 2`) dùng `checkIsValidCancel()` với cùng bộ cột `before_booking_day` / `before_booking_hour` / `booking_time_from` / `booking_time_to` của hàng `moment='cancel'` | `MC:2211-2226`, `:482-508` | Cao |
| **BR-P17** | Trạng thái kết thúc (không có chuyển tiếp hợp lệ nào ra khỏi): `4`, `6`, `7`. Gọi `EP-P14` lên các trạng thái này ⇒ **ghi `status = NULL`** (bug) | `MC:2226-2284` | Cao |
| **BR-P18** | Admin chỉ đổi được trạng thái theo đúng 6 cặp (status, action) đã định nghĩa; cặp không khớp ⇒ **im lặng trả `ok`**, không đổi gì | `AC:312-476` | Cao |
| **BR-P19** | Mọi thao tác Admin bị chặn khi booking đang chờ webhook UnivaPay (`status_webhook ∈ {0,3,4}` && `payment_system = 1`) | `AC:294-308` | Cao |

### 9.4 Thanh toán

| ID | Quy tắc | Bằng chứng | Tin cậy |
|---|---|---|---|
| **BR-P20** | Cổng thanh toán do `calendar_management.type_payment` quyết định (`0` Stripe / `1` UnivaPay), lưu snapshot vào `booking.payment_system`; môi trường test/live snapshot vào `booking.environment` | `MC:1596-1622` | Cao |
| **BR-P21** | Bot hợp đồng `free` ⇒ `is_use_payment` bị ép `0` **chỉ trên object PHP truyền vào view**, DB không đổi. Nếu client vẫn gửi `checkHasPayment=true` thì server **vẫn thu tiền** | `MC:96-102` | Cao |
| **BR-P22** | Stripe + `approve_type = 1` ⇒ thu ngay lúc đặt. Stripe + `approve_type = 2` ⇒ **chỉ lưu thẻ** (`setupIntent`), thu khi Admin duyệt. UnivaPay ⇒ **luôn thu ngay** bất kể `approve_type` | `MC:924-1010`, `:1086` | Cao |
| **BR-P23** | Thanh toán hỏng ở pha 1 ⇒ booking bị **xoá cứng** + đếm lại chỗ (`deleteOrderError`). Thanh toán cần 3-D Secure ⇒ booking **giữ nguyên**, client phải tự gọi `EP-P13` khi hỏng | `MC:966-971`, `:1371-1384` | Cao |
| **BR-P24** | UnivaPay có webhook (`univapay_webhook_id` && `strip_bots.status_webhook = 1`) ⇒ server poll 5 lần × 1s; hết mà chưa có kết quả ⇒ `status_webhook = 4` và trả `pending` (màn L18), chờ webhook chốt sau | `MC:1152-1166`; `SV:1958-1994` | Cao |
| **BR-P25** | Webhook UnivaPay thất bại ⇒ booking bị đặt `status = 7 (ADMIN_CANCEL)` + `payment_status = 2`; nếu trạng thái webhook cũ là `3` (kèm `from_job`) hoặc `4` thì **xoá cứng booking** | `SV:1571-1620` | Cao |
| **BR-P26** | Webhook được xử lý **đúng một lần**: `status_webhook ∈ {1, 2}` ⇒ bỏ qua. Đây là cơ chế idempotency duy nhất của tính năng | `SV:1557-1563` | Cao |
| **BR-P27** | Hoàn tiền là **toàn phần**, do Admin bấm tay, **không đổi `status`** (booking vẫn chiếm chỗ), **không thông báo cho khách**, và ghi lịch sử `SB_REFUND` với lý do 「¥{amount}︎の返金（エルメから／決済システムから）」 | `AC:1042-1141` | Cao |
| **BR-P28** | `refundType != 'now'` ⇒ **chỉ đánh dấu**, không gọi cổng thanh toán | `AC:1122-1124` | Cao |

### 9.5 Thông báo & tích hợp

| ID | Quy tắc | Bằng chứng | Tin cậy |
|---|---|---|---|
| **BR-P29** | Cấu hình action/tin nhắn cấp **khoá học** đè cấp **calendar**; chỉ fallback khi cấp khoá học rỗng hoàn toàn | `MC:1780-1806` | Cao |
| **BR-P30** | Nhắc lịch (`event_step_time`) chỉ được tạo khi booking vào trạng thái `1` hoặc `2` (`addActionRemind`), và bị xoá khi huỷ tự động / duyệt huỷ / Admin huỷ — **chỉ với bản ghi `status = 0`** | `SV:529-640`; `MC:2296-2310`; `AC:381-392`, `:449-460` | Cao |
| **BR-P31** | Thông báo 「chỗ trống」 gửi cho **tất cả** người `status = 3` của slot, không xếp hàng, không giữ chỗ, và **không xoá** bản đăng ký sau khi gửi | `SV:1292-1355` | Cao |
| **BR-P32** | Không gửi thông báo chỗ trống khi `calendar.is_notify_full_slot = 0`, hoặc reception không tồn tại, hoặc thời điểm slot **đã qua** | `SV:1296-1316` | Cao |
| **BR-P33** | Admin **không** nhận `mobile_notify` cho hai sự kiện: đăng ký 「キャンセル待ち」 và hoàn tiền | `MC:1718-1731`; `MobileNotifyService.php:151-188` | Cao |
| **BR-P34** | Mỗi tin LINE gửi thành công ⇒ `bots.free_send_count += 1` và `updateMessageSendCount(botId, today, 3, 1)` | `MC:1856-1861`, `:2356-2363` | Cao |
| **BR-P35** | Google Sheet chỉ đồng bộ khi `calendar.google_sheet_id` có giá trị; **không** đồng bộ cho đăng ký 「キャンセル待ち」 và cho `EP-P14` nhánh 1/2 | `MC:1866-1876`, `:2311` | Cao |
| **BR-P36** | Mỗi lần gửi form 「お客様情報」, hệ thống **ghi đè hồ sơ bạn bè** (`line_user` + `friend_information_values`) theo `friend_information_id`, trừ trường hợp `link_friend_information == 1` | `MC:1734-1738`, `:1934-2071` | Cao |
| **BR-P37** | Xử lý > 120 giây ⇒ gửi tin LINE trấn an (thành công) hoặc báo lỗi thẻ (thất bại) | `MC:1747-1754`; `SV:1607-1628` | Cao |

---

## 10. Nợ kỹ thuật & rủi ro

### 10.1 Rủi ro nghiệp vụ (khác với lỗ hổng bảo mật đã liệt kê ở `api-spec-public.md` §3)

| ID | Mức | Rủi ro | Bằng chứng | Tin cậy |
|---|---|---|---|---|
| **RP-01** | 🔴 Nghiêm trọng | **Bỏ qua thanh toán bằng một cờ boolean.** `checkHasPayment`, `amount`, `approve_type` đều do client quyết định; server không đối chiếu `calendar_management.is_use_payment` hay `calendar_course.amount`. Kết quả là booking 「予約確定」 + 「決済なし」 — **không phân biệt được với khoá học miễn phí hợp lệ** khi Admin nhìn vào app | `MC:1425-1430`, `:1468-1487`, `:1546-1567`; `AC:890-925` | Cao |
| **RP-02** | 🔴 Nghiêm trọng | **Overbooking ở luồng không thanh toán.** `checkCanBooking()` là check-then-act; lớp vá "arbiter" chỉ bắt được các request **trùng nhau tới từng giây** và chỉ xét `status = 1` | `MC:2144-2151`, `:1651-1699` | Cao |
| **RP-03** | 🟠 Cao | **Luồng 承認制 + Stripe không giữ chỗ và không xác minh thẻ.** Khách gửi yêu cầu ⇒ không chiếm chỗ ⇒ slot có thể đầy trước khi Admin duyệt; `approveBooking` **không kiểm sức chứa** nên vẫn duyệt ⇒ overbooking. Thẻ chỉ được `setupIntent`, lỗi thanh toán lộ ra sau nhiều ngày và **khách không được báo** | `MC:985-1010`; `AC:315-374` | Cao |
| **RP-04** | 🟠 Cao | **Booking treo chiếm chỗ vĩnh viễn.** Bỏ ngang giữa pha 1 và pha 2 ⇒ `status=1, payment_status=0, status_webhook ∈ {0,3,4}`; bộ ba này bị **ẩn khỏi lịch sử của khách** (`EP-P15`) nên khách không tự huỷ được, và **bị khoá thao tác Admin** (`EP-M01`). Không có job dọn dẹp | `MC:2417`, `:2475`; `AC:294-308` | Trung bình |
| **RP-05** | 🟠 Cao | **Không có transaction ở bất kỳ luồng ghi nào.** `DB::beginTransaction()` bị comment ở `order()` (`:1624`, `:1884`) và ở `cancelBooking()` (`:2204`, `:2295`); `EP-M01` chưa từng có. Thu tiền thành công + đổi trạng thái thất bại ⇒ mất tiền không có booking | `MC:1624`, `:2204`; `AC:312-476` | Cao |
| **RP-06** | 🟠 Cao | **Tiền charge nhưng trạng thái không đổi (UnivaPay + webhook).** `approveBooking` trả `ok` ngay sau khi charge, giao việc đổi `status` cho webhook `lesson_change_status`. Webhook không về ⇒ đã trừ tiền, booking vẫn `status = 0`, Admin bị khoá | `AC:328-336`; `SV:437-441` | Cao |
| **RP-07** | 🟠 Cao | **Webhook không xác thực chữ ký.** `POST /mobile/univapay-callback-payment` không middleware, nằm trong `VerifyCsrfToken::$except`, `WebhookUnivapayControler@webhook` **không kiểm chữ ký / IP / secret** — chỉ đọc `metadata.module` và `event`. Ai gửi được payload đúng dạng đều điều khiển được trạng thái thanh toán của booking (cần Hashids hợp lệ) | `routes/web.php:4067`; `WebhookUnivapayControler.php:11-38`; `VerifyCsrfToken.php:52` | Cao (thiếu kiểm tra) / Trung bình (khả năng khai thác) |
| **RP-08** | 🟡 Trung bình | **`status = NULL`** — gọi `EP-P14` hai lần liên tiếp ⇒ booking rơi khỏi mọi truy vấn, bộ đếm sai vĩnh viễn | `MC:2226-2284` | Cao |
| **RP-09** | 🟡 Trung bình | **Thông báo chỗ trống gửi đồng loạt, đồng bộ trong request.** N người chờ ⇒ N tin LINE trong request huỷ ⇒ nguy cơ timeout; và N−1 người vào sau gặp lỗi hết chỗ | `SV:1319-1355` | Cao |
| **RP-10** | 🟡 Trung bình | **Bản đăng ký `status = 3` không hết hạn.** Không xoá sau khi gửi, không xoá khi slot đã qua ⇒ tích luỹ và gửi lặp | `SV:1319-1355` | Cao |
| **RP-11** | 🟡 Trung bình | **Lost update `free_send_count`** — dùng `$bot->free_send_count + 1` thay vì `DB::raw`. Sai lệch chỉ số tính phí gửi tin | `MC:1856-1858`, `:2360` | Cao |
| **RP-12** | 🟡 Trung bình | **Nuốt lỗi im lặng** ở `addActionRemind()` (`SV:636-639`) và `updateFriendInfoValue()` (`MC:2068-2070`) — chỉ `Log`, không báo ai. Mất nhắc lịch / mất cập nhật hồ sơ mà không ai biết | | Cao |
| **RP-13** | 🟡 Trung bình | **Google Sheet chạy đồng bộ** trong request đặt chỗ; đo thời gian riêng cho thấy đây từng là điểm nghẽn | `MC:1866-1876` | Trung bình |
| **RP-14** | 🟡 Trung bình | **`status_webhook` bị ghi đè thành `1` ở pha 2** bất kể pha 1 để `0`/`3` ⇒ mất dấu vết chờ webhook | `MC:1621` | Cao |
| **RP-15** | 🟢 Thấp | **`$guarded = []`** trên `CalendarCourseBooking` — mass assignment mở hoàn toàn; kết hợp với các endpoint nhận `$request->all()` là mặt tấn công tiềm tàng | `app/CalendarCourseBooking.php:13` | Cao |

### 10.2 Nợ kỹ thuật (chất lượng mã)

| ID | Vấn đề | Bằng chứng |
|---|---|---|
| D-01 | **Không một `$request->validate()` nào** trong cả hai controller (2971 + 1862 dòng); mọi kiểm tra là `if` thủ công, nhiều chỗ thiếu hẳn | toàn bộ `MC`, `AC` |
| D-02 | **Code chết**: `checkValidBooking()` (`MC:1901-1915`, còn dùng `>= 0` sai logic), `checkReachesMaxEachCustomer` (`EP-P07`, không client nào gọi), `cancelRequestCancel()` phía JS, `changeStatusBookingOld` (`AC:85`), `checkDeleteReception` (`AC:1649`) | |
| D-03 | **Comment-out làm đổi hành vi**: transaction (`MC:1624`, `:2204`), `countTotalBookingStatus` trong `handleKeepSlot` (`MC:1292`), redirect `closeBooking` (`MC:173-175`), `whereNotNull('charge_id')` ở thống kê hoá đơn (`AC:993`), map `bookingStatus` (`AC:1206-1222`), `PaginationResource` (`AC:731`), `throttle` (`Kernel.php:44-47`) | |
| D-04 | **Chuỗi lỗi tiếng Anh lọt ra UI tiếng Nhật**: `'Calendar does not exit'` (sai chính tả), `'line user not exists'`, `'reception not exists'`, `'calendar not exists'`, `'create customer error'` | `MC:1456`, `:1504`, `:1533`, `:2679`, `:2723` |
| D-05 | **Lỗi chính tả trong text hiển thị**: 「この機能は現在利用できませんん。」 (hai ký tự ん) | `MC:60` |
| D-06 | **Khoá response không nhất quán**: `errorMessage` (camel) ở hầu hết endpoint nhưng `error_message` (snake) ở `EP-P14`, `EP-P16`; `status` khi thì boolean, khi thì chuỗi `'success'`/`'error'`/`'pending'` | `MC:2385-2389`, `:2593-2598` vs `:1023-1039` |
| D-07 | **Tên tham số nhất quán kém**: `EP-M12` dùng `bot_id`, 14 endpoint còn lại dùng `botId`; `EP-P06` dùng `line_user_id`, `EP-P03`/`EP-P04` dùng `line_id` | `AC:1540`; `MC:301`, `:563` |
| D-08 | **So sánh lỗi bằng chuỗi tiếng Nhật cứng** ở `EP-M14 delete-reception` — đổi một ký tự ở service làm lỗi âm thầm thành công | `AC:1672-1679` |
| D-09 | **Đặt tên cột gây hiểu nhầm**: `booking_time_from`/`booking_time_to` thực chất là **số giờ / số phút**, không phải mốc thời gian | `MC:434-436` |
| D-10 | **`select('*')` / `select()` không giới hạn cột** trên endpoint public ⇒ lộ cấu hình nội bộ và số liệu vận hành | `MC:285-289`, `:2765-2769` |
| D-11 | **Copy-paste giữa FA-019 và FA-020**: log ghi `'Api getCalendarSalonInfoById start'` trong controller lesson; `EP-P17` dùng chung endpoint của FA-020; `booking.js` của lesson nằm ở `public/js/calendar_salon/` | `AC:540`; `MC` ↔ `Mobile\CalendarSalonController:4408` |
| D-12 | **`getBotId()` dựa session Admin bị gọi trong request LINE User** (`recountAppBadgeNotify(getBotId())` ở `EP-P14` nhánh 1) — cùng loại lỗi đã ghi nhận trong BUG #38208 | `MC:2174`; `AC:1667-1669` |
| D-13 | **Đo thời gian rải rác trong code sản phẩm** (`$endtExcecuteCountBooking`, `$endtExcecuteNotify`, `$endtExcecuteRemind`, `$endtExcecuteFriendInfo`, `$endtExcecuteSendAction`, `$endtExcecuteGoogleSheet`) — dấu vết điều tra hiệu năng chưa dọn | `MC:1714-1876` |
| D-14 | **Comment tiếng Việt lẫn trong code sản phẩm**, kể cả comment mô tả bản vá race condition kèm số ticket nội bộ (`lessons #37711/#37780`) | `MC:1651-1660` |
| D-15 | **`$calendarSettingSendMessage` không kiểm null** trước khi truy cập thuộc tính ở nhiều nơi ⇒ calendar thiếu cấu hình sẽ gây 500 thay vì lỗi nghiệp vụ | `MC:295`, `:1793-1797` |

---

## 11. Kết luận 5 nghi vấn

| # | Nghi vấn | Kết luận | Bằng chứng | Tin cậy |
|---|---|---|---|---|
| **1** | `cancelRequestCancel()` — có route không, có ai gọi không | **Có route, backend hoạt động, nhưng UI khoá.** `POST /ajax/calendar-cancel-booking` (`routes/web.php:3854`) nhánh `status = 5` chuyển về `1`/`2`. Phía client `public/js/booking_news/booking.js:944` định nghĩa `cancelRequestCancel()` nhưng **không blade nào bind**; màn L14 hiển thị text chết 「キャンセルリクエストの取り消しはできません」. Đây là **năng lực backend bị UI vô hiệu hoá**, không phải lỗi backend. Vẫn là **lỗ hổng**: kẻ tấn công gọi trực tiếp để rút yêu cầu huỷ của người khác | `MC:2182-2196`; `routes/web.php:3854` | Cao |
| **2** | Server có kiểm tra lại `checkHasPayment` không | **KHÔNG.** Không có bất kỳ đối chiếu nào với `calendar_management.is_use_payment`, `calendar_course.amount`, hay kết quả thật từ cổng thanh toán. `checkHasPayment = false` ⇒ `payment_status = 2 (SP_NO_PAYMENT)` + `status = 1` 「予約確定」 mà không mất tiền. `amount` cũng do client đặt. **Đây là rủi ro nghiêm trọng nhất của tính năng** (RP-01) | `MC:1425-1430`, `:1468-1487`, `:1554-1567` | Cao |
| **3** | Nhánh `isPaymentAfter` không rollback booking khi confirm thất bại | **Không có gì để rollback — vì nhánh này chưa từng tạo booking.** `approve_type != 1` (Stripe) chỉ gọi `setupIntent()`, `bookingId` giữ nguyên `null`, không giữ chỗ. Hệ quả thật nghiêm trọng hơn: (a) `EP-P13` gọi với `bookingId = null` là **no-op trả `{"status":true}` giả**; (b) thẻ chỉ được lưu, **chưa xác minh thu được tiền**; (c) slot **không được giữ**, và `approveBooking` **không kiểm sức chứa** ⇒ overbooking; (d) thất bại lộ ra sau nhiều ngày, khách **không được thông báo** (RP-03) | `MC:985-1010`, `:1371-1384`; `AC:315-374` | Cao |
| **4** | Giới hạn số lần đặt mỗi khách có được kiểm ở server khi tạo booking không | **CÓ — nhưng không phải qua `EP-P07`.** `EP-P07 check-reaches-max-each-customer` là **code chết** (lời gọi duy nhất ở `booking.js:999` đã bị comment). Kiểm tra thật nằm trong `checkCanBooking()` → `checkLimitBookEachCustomer()`, ném 「1人あたりの予約受付上限に達しています」. **Lỗ hổng còn lại**: bỏ qua hoàn toàn khi `register_notify_slot = true`, khi `uCode = 'preview'`, và khi Admin đặt hộ (`EP-M15`); ngoài ra không đếm `status ∈ {0, 3}` nên chế độ 承認制 nhận vô hạn yêu cầu | `MC:246-260`, `:2088-2095`, `:1474`, `:2856` | Cao |
| **5** | Dùng chung `POST /ajax/mobile/calendar-salon/check-friend` của FA-020 | **ĐÚNG — phụ thuộc chéo thật.** FA-019 (`public/js/booking_news/booking.js:409`) gọi endpoint thuộc nhóm route `calendar-salon` của FA-020 → `Mobile\CalendarSalonController@checkFriend` (`:4408-4438`). Sửa FA-020 ảnh hưởng trực tiếp FA-019. Nhiều dấu vết copy-paste khác giữa hai tính năng (D-11) | `routes/web.php:3810`; `Mobile\CalendarSalonController:4408` | Cao |

---

## 12. Phụ thuộc chéo (bổ sung cho `api-spec-public.md` §4)

| Thành phần | Quan hệ | Ghi chú |
|---|---|---|
| **FA-020 「サロン予約」** | Dùng chung `checkFriend`; chia sẻ mẫu code `handleOrderCallback` / `callbackChangeStatusBooking`; JS đặt lẫn thư mục | Nghi vấn #5 |
| **Webhook UnivaPay dùng chung** | `POST /mobile/univapay-callback-payment` phục vụ **9 module**: `lesson`, `lesson_change_status`, `salon`, `salon_change_status`, `event-booking`, `event_booking_change`, `sales`, `sales_change_card`, `sales_job` | `WebhookUnivapayControler.php:18-28`; `HandleWebhookUnivapay.php:39-73`. Sửa controller/job này ảnh hưởng **toàn bộ** tính năng thanh toán của hệ thống |
| **Queue Laravel** | `HandleWebhookUnivapay` là job Laravel (`ShouldQueue`) — **khác** hệ Spring Boot | Nếu queue worker Laravel chết ⇒ mọi booking UnivaPay kẹt ở `status_webhook ∈ {0,4}` |
| **Job Spring Boot** | `event_step_time` (nhắc lịch, `event_step.type = 4`), `mobile_notify` (push Admin) | `job-spec.md` §2.1, §2.4 |
| **FilterV2 / `Conversation::advanceFilterPost()`** | Lọc hiển thị calendar (`filter_id_show_booking`) và lọc khoá học (`filter_id_send_after_booking`) | `MC:156-172`, `:312-350` |
| **Hồ sơ bạn bè** | `EP-P06` đọc, `EP-P12`/`EP-M15` **ghi đè** | `friend_information_settings`, `friend_information_values`, `line_user` |
| **Hệ thống Action (`t_actions`)** | Mã `11001`, `11002`, `11003`, `11005`, `11006`, `11009` | `11009` dùng cho **hai** sự kiện khác nhau |
| **Google Sheet** | `CalendarGoogleSheetService` — đồng bộ đồng bộ trong request | |
| **Màn timeout dùng chung** | `GET /lme/timeout/{bot_id?}/{type?}/{calendar_id?}` (`routes/web.php:4155`) | JS chuyển hướng khi ajax lỗi |
| **`Basic\CalendarManagementController`** | Portal Admin — cấu hình calendar/course/reception/setting mà toàn bộ luồng public đọc; cũng chứa `addActionRemindNew()` backfill `event_step_time` hàng loạt | **Ngoài phạm vi file này** — xem spec riêng |
