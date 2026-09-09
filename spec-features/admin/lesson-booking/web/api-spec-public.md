# FA-019 「レッスン予約」 — API Spec: Trang public (LIFF) & API ứng dụng di động

> Tạo bởi: **web-analyzer** agent | Phương pháp: **code-first** (đọc trực tiếp controller + routes + middleware)
> Phạm vi: `Mobile\CalendarController` (trang đặt chỗ LIFF cho LINE User) và `Api\CalendarLessonController` (API cho app di động của Admin).
> **Không** bao gồm `Basic\CalendarManagementController` / `Basic\SettingPaymentCalendarController` (Admin portal — spec riêng).
> Confidence tổng thể: **Cao** — mọi khẳng định đều truy vết `file.php:dòng`.

---

## 0. Xác thực & middleware — tổng quan

### 0.1 Phần A — trang public LIFF (`Mobile\CalendarController`)

| Hạng mục | Kết quả | Bằng chứng |
|---|---|---|
| Route group bao ngoài | `Route::middleware(['NotifyChatworkRequestTimeSlow'])->group(...)` — dòng 81 đến 4135 của `routes/web.php`. **Không có** `auth`, `basic_access`, `check_login`, `mobile_access` | `routes/web.php:81`, `:3798-3806`, `:3838-3865` |
| Middleware group | `web` (session, cookie, CSRF) — do `RouteServiceProvider` gắn mặc định | `app/Http/Kernel.php:34-42` |
| CSRF | **TẮT cho toàn bộ `/ajax/*`** — pattern `'/ajax/*'` nằm trong `$except` | `app/Http/Middleware/VerifyCsrfToken.php:16` |
| Danh tính người dùng | Chỉ dựa vào tham số **`line_user_id`** (= `line_user.line_id`) do client gửi, hoặc `uCode` trên URL. Không token, không chữ ký | `CalendarController.php:105-121`, `:301-306`, `:1465` |
| Rate limit | **Không có** — `throttle:60,1` của group `api` đã bị comment; group `web` không có throttle | `app/Http/Kernel.php:44-47` |
| Chế độ xem thử | `uCode == 'preview'` ⇒ `$lineId = 'preview'`, bỏ qua lọc filter bạn bè | `CalendarController.php:152-154`, `:307` |

> **Kết luận**: **mọi endpoint `/ajax/*` của FA-019 đều public, không xác thực, không CSRF, không rate limit.** Xem §3 「Cảnh báo bảo mật」.

### 0.2 Phần B — API ứng dụng di động (`Api\CalendarLessonController`)

| Hạng mục | Kết quả | Bằng chứng |
|---|---|---|
| Prefix | `api/mobile/calendar-lesson/…` (group `mobile` → group middleware → group `calendar-lesson`) | `routes/api.php:30`, `:38`, `:274-289` |
| Middleware | `['mobile-auth', 'mobile_contract_expire']` | `routes/api.php:38` |
| `mobile-auth` | `MobileAuthenticate` — kiểm tra guard **`api-mobile`**. Thất bại → HTTP **401** `{"error":"Unauthenticated"}`. Thêm kiểm tra header `remember-token-mobile` khớp `users.remember_token_reset_pass`, lệch → logout + 401 | `app/Http/Middleware/MobileAuthenticate.php:21-52` |
| `mobile_contract_expire` | Chặn khi bot (`botId`/`bot_id` trong request) hết hợp đồng → mã `contract_expired`. Trừ 5 path ngoại lệ | `app/Http/Middleware/MobileContractExpire.php:24-56` |
| CSRF | Không áp dụng (`api.php`); ngoài ra `/api/mobile/*` cũng nằm trong `$except` | `VerifyCsrfToken.php:24` |
| Kiểm tra quyền (role) | **Chỉ `getListCalendarLesson`** gọi `checkHasPermission('calendar.index', $botId)`. **14 endpoint còn lại không kiểm tra quyền** | `CalendarLessonController.php:491-501` |
| Kiểm tra `botId` sở hữu `calendarId`/`bookingId` | **Không có ở bất kỳ endpoint nào** | toàn bộ file |
| Định dạng response | `App\Helpers\ResponseData` → `{"result":"ok"\|"error","data":…,"errorMessage":…}` | mọi method |

---

# PHẦN A — Trang public LIFF (`Mobile\CalendarController`)

File: `app/Http/Controllers/Mobile/CalendarController.php` (2971 dòng)

## A.1 Bảng tổng hợp endpoint

| Mã | Method | URL | Mô tả | Controller@method | Xác thực | Màn hình |
|---|---|---|---|---|---|---|
| EP-P01 | GET | `/mobile/calendar/{calendarHashId?}/{uCode?}` | Render SPA đặt chỗ (LIFF) | `index` :73 | Không (public) | L01–L18, L21 |
| EP-P02 | GET | `/mobile/calendar-lesson/{calendarHashId}/close-booking` | Trang 「受付停止」 | `closeBooking` :209 | Không | L19 |
| EP-P03 | GET | `/ajax/get-list-course-by-calendar` | Danh sách 「コース」 đã lọc filter bạn bè | `getListCourseByCalendar` :281 | Không | L04, copyBooking |
| EP-P04 | GET | `/ajax/get-list-time-booking-by-course` | Khung giờ theo tuần (+ tự nhảy tối đa 4 tuần) | `getListTimeBookingByCourse` :363 | Không | L06 (週) |
| EP-P05 | GET | `/ajax/init-data-booking-calendar` | Ngày có chỗ trong tháng (FullCalendar events) | `initDataBooking` :515 | Không | L06 (月) |
| EP-P06 | GET | `/ajax/get-data-friend-info-calendar` | Cấu hình form 「お客様情報」 + prefill hồ sơ bạn bè | `getDataFriendInfo` :560 | Không | L07 |
| EP-P07 | GET | `/ajax/check-reaches-max-each-customer` | Kiểm tra khách đã đạt giới hạn số lần đặt | `checkReachesMaxEachCustomer` :262 | Không | **không client nào gọi** |
| EP-P08 | POST | `/ajax/calendar/call-create-customer-id` | Tạo `customer_id` UnivaPay | `createCustomerIdUnivapay` :2666 | Không | L08 (UnivaPay) |
| EP-P09 | POST | `/ajax/calendar/get-info-card-event-booking` | Lấy thông tin thẻ từ token UnivaPay | `getInfoCardPayment` :2622 | Không | L08 (UnivaPay) |
| EP-P10 | POST | `/ajax/calendar-payment-stripe` | Giữ chỗ + thanh toán/lưu thẻ Stripe | `paymentStripe` :848 | Không | L09 |
| EP-P11 | POST | `/ajax/calendar-payment-univapay` | Giữ chỗ + thu tiền UnivaPay | `paymentUnivapay` :1042 | Không | L09 |
| EP-P12 | POST | `/ajax/calendar-order` | Chốt đặt chỗ / đăng ký nhận thông báo | `order` :1414 | Không | L09, L10 |
| EP-P13 | POST | `/ajax/calendar-delete-order-confirm-fail` | Xoá cứng booking khi confirm thẻ thất bại | `deleteOrderConfirmFail` :1371 | Không | L09 (rollback) |
| EP-P14 | POST | `/ajax/calendar-cancel-booking` | Huỷ / yêu cầu huỷ / rút yêu cầu huỷ / dừng nhận thông báo | `cancelBooking` :2157 | Không | L15, L20 |
| EP-P15 | GET | `/ajax/get-list-booking-history-calendar` | Lịch sử đặt chỗ (3 nhóm) | `getListHistoryBooking` :2391 | Không | L13 |
| EP-P16 | GET | `/ajax/get-detail-booking-calendar` | Chi tiết 1 đặt chỗ | `getDetailBookingCalendar` :2557 | Không | L14 (deep link) |
| EP-P17 | POST | `/ajax/mobile/calendar-salon/check-friend` | Kiểm tra còn là bạn bè OA — **dùng chung FA-020** | `Mobile\CalendarSalonController@checkFriend` :4408 | Không | toàn trang |

Route: `routes/web.php:3803`, `:3804`, `:3838`, `:3840`, `:3842`, `:3844`, `:3846`, `:3848`, `:3850`, `:3852`, `:3854`, `:3856`, `:3858`, `:3860`, `:3863`, `:3865`, `:3810`.

> Toàn bộ controller **không có một lệnh `$request->validate()` nào** — mọi kiểm tra là `if` thủ công. Confidence: Cao.

---

## A.2 Chi tiết từng endpoint

### EP-P01 — `GET /mobile/calendar/{calendarHashId?}/{uCode?}`

Render view `basic.calendar_management.bookings.layouts.main`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation thật |
|---|---|---|---|---|
| `calendarHashId` | path | string (Hashids) | Thực tế bắt buộc | `Hashids::decode(...)[0] ?? null`; rỗng → `redirect()->route('404')` (:80-84) |
| `uCode` | path | string | Không | So khớp `bot_line_users.u_code`; giá trị đặc biệt `'preview'` (:152-154) |

**Chuỗi rẽ nhánh** (theo thứ tự thực thi)

| # | Điều kiện | Kết quả | Dòng |
|---|---|---|---|
| 1 | Hashids decode rỗng | redirect `route('404')` | :82-84 |
| 2 | `calendar_management` không tồn tại | redirect `route('404')` | :90-92 |
| 3 | `bot_contracts.contract_type == 'free'` | ép `$calendar->is_use_payment = 0` (chỉ trên object, **không ghi DB**) | :96-102 |
| 4 | `bot_line_users.is_blocked == 1` | redirect `$bot->url_add_friend` | :112-115 |
| 5 | Bot không tồn tại | redirect `route('404')` | :142-145 |
| 6 | `checkIsBotExpired()` false (`plan_type==1` && (`expired_date`+7 ngày < now **hoặc** `bot_contracts.status == 3`)) | redirect `route('410')` | :147-150, :234-244 |
| 7 | `uCode == 'preview'` | `$lineId = 'preview'` | :152-154 |
| 8 | `filter_id_show_booking` có + tồn tại `filter_v2` `parent_type='calendar-setting-show-booking-form'` | `isValidFilter = isValidFilter(...)` → biến JS | :156-172 |
| 9 | UA chứa `facebookexternalhit` | trả view `preview_url` (OGP) | :177-186 |

> Đoạn redirect sang `closeBooking` khi `isValidFilter` **đã bị comment** (:173-175) — việc chặn nay do JS đảm nhiệm. Hệ quả: HTML gốc (kèm toàn bộ dữ liệu `calendar`, `stripeBot`) vẫn được trả về cho user bị chặn.

**Dữ liệu truyền vào view** (:187-206): `calendar` (**toàn bộ record `calendar_management`**), `lineUserId`, `flagImage`, `stripeBot` (**toàn bộ record `strip_bots`**), `calendarSettingBooking`, `calendarSettingCancel`, `emailDefault`, `bot`, `flag_brand_card_univapay`, `url_line_chat`, `isValidFilter`, `hashCalendarId`.

> ⚠ `stripeBot` là toàn bộ hàng `strip_bots`. Nếu blade in nguyên object vào JS global thì khoá bí mật (`strip_secret_live_key`, `univapay_secret`, `univapay_app_token`) lộ ra HTML công khai. Confidence: **Trung bình** (controller chắc chắn truyền cả record; mức lộ phụ thuộc blade).

**Lỗi**: không trả JSON — chỉ redirect (404 / 410 / `url_add_friend`).

---

### EP-P02 — `GET /mobile/calendar-lesson/{calendarHashId}/close-booking`

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `calendarHashId` | path | Hashids | Có | decode rỗng → redirect 404 (:213-216); calendar không tồn tại → 404 (:224-226) |

- Lấy `CalendarSettingSendMessage` với `moment = 'booking'` (:222) rồi render `close-booking`.
- **Không kiểm tra `filter_id_show_booking`, không kiểm tra bạn bè** — ai có hash hợp lệ đều xem được (:209-231).
- `$calendarSendMessage` **không kiểm tra null** trước khi blade dùng `->text_filter_show_booking`.

---

### EP-P03 — `GET /ajax/get-list-course-by-calendar`

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `calendarId` | query | int | Có (ngầm) | Không validate. Sai ⇒ `$calendarSetting` null ⇒ **`ErrorException` trên `->approve_type`** (:295) |
| `line_id` | query | string | Có (ngầm) | `'preview'` ⇒ bỏ qua lọc filter (:302-307) |

**Xử lý** (:281-360)
1. `calendar_course` WHERE `calendar_id` = ? AND `booking_page_display = BOOKING_DISPLAY_ON`, ORDER BY `course_order`, `select('*')`.
2. Với mỗi course có `filter_id_send_after_booking`: dựng filter `parent_type = 'calendar-course-setting-status-send-after-booking'`, `parent_id = course.id`, gọi `Conversation::advanceFilterPost(...)` giới hạn `[$lineUserId]`; `count() < 1` ⇒ loại course (:312-350).

**Request mẫu**
```
GET /ajax/get-list-course-by-calendar?calendarId=123&line_id=Uxxxxxxxxxxxxxxxx
```

**Response thành công**
```json
{
  "courses": [
    {
      "id": 45, "calendar_id": 123, "course_name": "体験レッスン",
      "course_image": "…", "amount": 3000, "hour_done": 1, "minute_done": 0,
      "course_description": "<p>…</p>", "course_order": 1,
      "booking_page_display": 1, "action_id_send_after_booking": null,
      "filter_id_send_after_booking": null,
      "…": "toàn bộ cột calendar_course"
    }
  ]
}
```

> ⚠ `select('*')` trả **toàn bộ cột** `calendar_course` — kể cả cấu hình nội bộ (`message_send_after_booking`, `action_id_send_after_booking`, `system_name`, `use_message_notify_send_after_booking`). Rò rỉ cấu hình Admin ra public (:285-289).

**Lỗi**: không có nhánh lỗi tường minh; lỗi PHP → 500 → JS `$.ajaxSetup` chuyển sang `/lme/timeout/{botId}/lesson/{calendarId}`.

---

### EP-P04 — `GET /ajax/get-list-time-booking-by-course`

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `courseId` | query | int | Có | không |
| `type` | query | string | Không | nhận nhưng **không dùng** trong `getListTimeWeek()` |
| `start_date` | query | `Y-m-d` | Có | `Carbon::parse()` — chuỗi sai ⇒ exception |
| `end_date` | query | `Y-m-d` | Có | như trên |
| `calendarId` | query | int | Có | không |
| `line_id` | query | string | Có | `'preview'` ⇒ bỏ tính `checkCustomerReachesMax` |
| `timeShowWeek` | query | `1`\|khác | Không | `== 1` ⇒ bật chế độ tự nhảy tuần |

**Cơ chế tự nhảy tuần** (:371-405): lặp `i = 1..4`, mỗi vòng gọi `getListTimeWeek()`; rỗng thì `+1 tuần` rồi thử lại; hết 4 vòng vẫn rỗng thì **nhảy thêm 1 tuần nữa** và trả kết quả tuần đó (kể cả rỗng). Trả kèm `startDate`/`endDate` mới.

**`getListTimeWeek()`** (:2756-2869) tính cho mỗi slot:

| Trường | Nguồn |
|---|---|
| `total_person` | `total_person - total_booking` (SQL), ép về 0 nếu ≤ 0 (:2766, :2790-2792) |
| `is_can_booking` | `false` khi (`type_limit_booking==1` && `is_notify_full_slot==0` && hết chỗ) hoặc `!is_valid_start_receive` (:2794-2801, :2833-2835) |
| `is_valid_start_receive` | `checkIsValidStartReceive()` khi `start_receive_booking_type == 2` (:2806-2816) |
| `is_valid_deadline_receive` | `checkIsValidDeadlineReceive()` khi `deadline_receive_booking_type == 2`, ngược lại `start_time > now` (:2818-2830) |
| `new_end_time` | `end_time == '00:00'` → `'24:00'` (:2804) |

Slot bị **loại khỏi response** khi `!is_valid_deadline_receive` (:2831), hoặc kín chỗ + `is_notify_full_slot==0` + `is_display_course_full==0` (:2798-2800).

**Response**
```json
{
  "listTime": [
    { "date": "2026-09-01",
      "data": [ { "id": 9911, "course_id": 45, "received_booking_date": "2026-09-01",
                  "start_time": "10:00", "end_time": "11:00", "new_end_time": "11:00",
                  "type_limit_booking": 1, "total_person": 3, "total_booking": 2,
                  "is_can_booking": true, "is_valid_start_receive": true,
                  "is_valid_deadline_receive": true } ] }
  ],
  "checkCustomerReachesMax": false,
  "text_limit_book_each_customer": "1人あたりの予約受付上限に達しています",
  "startDate": "2026-09-01", "endDate": "2026-09-07"
}
```

> `select()` không tham số ⇒ trả **toàn bộ cột `calendar_course_receptions`**: `total_booking`, `total_approve`, `total_request`, `total_cancel`, `total_request_booking_wait_cancel` — số liệu vận hành nội bộ lộ ra public (:2765-2769).

---

### EP-P05 — `GET /ajax/init-data-booking-calendar`

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `courseId` | query | int | Có | |
| `calendarId` | query | int | Có | |
| `month` | query | `Y-m-d` | Có | |
| `calendar` | query | object | Có | **Client gửi** `is_notify_full_slot`, `is_display_course_full` — server **dùng thẳng giá trị client** (`getListTimeMonth` :2905, :2907) thay vì đọc DB |
| `timeShowMonth` | query | `1`\|khác | Không | `== 1` ⇒ thử tháng hiện tại rồi tháng kế; vẫn rỗng thì nhảy thêm 1 tháng (:521-552) |

**Response**: `{ "events": [ {"id":0,"start":"2026-09-01","display":"background"} ], "month":"…", "startDate":"…", "endDate":"…", "next": 0|1|2 }`

> Ở chế độ tháng, slot bị **loại** khi `!is_valid_start_receive` (:2934-2936) — **khác** chế độ tuần (chỉ đánh dấu `is_can_booking=false`). Hệ quả: lịch tháng và danh sách tuần lệch nhau. Confidence: Cao.

---

### EP-P06 — `GET /ajax/get-data-friend-info-calendar`

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `calendarId` | query | int | Có | |
| `line_user_id` | query | string (`line_id`) | Có | `'preview'` ⇒ không prefill |
| `botId` | query | int | Có | Dùng để đọc `friend_information_values` |

**Xử lý** (:560-812): lấy `calendar_setting_send_forms` WHERE `enable = 1` AND `question IS NOT NULL` ORDER BY `order`.

Sinh chuỗi `rules` cho vee-validate:

| Điều kiện | Rule |
|---|---|
| `required == 1` | `required_calendar` (:580-582) |
| `rule_type == 1 && rule_validation_type == 'email'` | `email_calendar` (:585-586) |
| `… == 'phone'` | `phone_calendar` (:587) |
| `… == 'katakana'` | `kana` (:589) |
| `… == 'number'` | `number` (:591) |
| `can_delete == 0 && friend_information_id == -3 && rule_type == 0` | `email_calendar` (:596-598) |

**Prefill từ hồ sơ bạn bè** khi `link_friend_information != 1 && enable_load_friend_information == 1` (:643-724):

| `friend_information_id` | Nguồn giá trị |
|---|---|
| `-1` | `line_user.view_name` |
| `-2` | `line_user.phone_number` |
| `-3` | `line_user.email` |
| `-4` | `line_user.birthday` |
| `-6` | `line_user.province` (+ options = `PROVINCE_DEFAULT`) |
| `-7`…`-10` | `friend_information_values.value` theo `bot_id` |
| khác | `friend_information_values.value` (**không lọc `bot_id`**, :711-714) |

**Response**
```json
{
  "friendInfoSettings": [
    { "id": 12, "form_type": 1, "question": "お名前を入力してください",
      "sub_question": null, "required": 1, "rules": "required_calendar",
      "friend_information_id": -1, "options": [], "display_method": 1,
      "date_beginning": null, "value": "山田太郎", "value_preview": "山田太郎",
      "recording_time": 0, "time": null, "can_delete": 0 }
  ]
}
```

> 🔴 **Rò rỉ dữ liệu cá nhân**: chỉ cần `calendarId` + `line_id` của một bạn bè bất kỳ là lấy được **tên, email, số điện thoại, ngày sinh, tỉnh, và mọi trường hồ sơ tuỳ biến** của người đó. Không xác thực, không kiểm tra chính chủ (:560-812).

---

### EP-P07 — `GET /ajax/check-reaches-max-each-customer`

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `booking_id` | query | int | Không | **Đọc vào `$bookingId` nhưng không dùng** (:263) |
| `line_id` | query | string | Có | |
| `calendarSetting` | query | object | Có | Client gửi `limit_book_each_customer`, `calendar_id`, `number_limit_booking` — **server tin hoàn toàn** (:268-273) |

**Response**: `{ "status": true, "checkCustomerReachesMax": false }`

> ✅ **Xác minh nghi vấn #4**: endpoint **không có client nào gọi** — grep toàn repo chỉ thấy 1 dòng **đã bị comment** ở `public/js/calendar_salon/booking.js:999`. Đây là code chết. **NHƯNG giới hạn "mỗi khách tối đa N lần" VẪN được kiểm ở server** khi tạo booking, bên trong `checkCanBooking()` (:2088-2095) → ném Exception 「1人あたりの予約受付上限に達しています」. Xem BR-P07 trong `logic-spec-public.md`. Confidence: Cao.

---

### EP-P08 — `POST /ajax/calendar/call-create-customer-id`

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `calendarId` | body | int | Có |
| `botId` | body | int | Có |

**Xử lý** (:2666-2726)
1. `CalendarManagement::find($calendarId)`; rỗng → `{"success": false, "msg": "calendar not exists"}` (**tiếng Anh**, :2679).
2. Sinh `customerCode = 'calendar' . str_random(20)`, lặp cho tới khi không trùng `calendar_course_bookings.univapay_customer_code` (:2683-2690).
3. Chọn app id/token/secret theo `calendar.environment` (0 = test) (:2695-2697).
4. `POST https://api.univapay.com/stores/{appId}/create_customer_id`, header `Authorization: Bearer {secret}.{token}`.

**Response OK**: `{"success": true, "customer_code": "calendarXXXX", "customer_id": "…"}`
**Response lỗi**: `{"success": false, "msg": "create customer error"}` (**tiếng Anh**, :2723)

> ⚠ Endpoint public gọi thẳng API UnivaPay bằng khoá bí mật của bot; không rate limit ⇒ lạm dụng tạo customer hàng loạt. `botId` do client truyền, **không kiểm tra khớp `calendar->bot_id`** (:2692).

---

### EP-P09 — `POST /ajax/calendar/get-info-card-event-booking`

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `botId` | body | int | Có |
| `token` | body | string (UnivaPay transaction token) | Có |
| `emailDefault` | body | string | Không — đọc nhưng **không dùng** (:2626) |
| `nameDefault` | body | string | Không — **không dùng** (:2627) |
| `calendarId` | body | int | Chỉ để log |
| `environment` | body | `0`\|`1` | Có — **client quyết định môi trường test/live** (:2640) |

**Response OK**: `{"status": true, "infoCard": {"univapay": {"last4":"4242","brand":"visa","authorizeChargeId":"…","expired_card":"12/28"}}, "errorMessage": ""}`
**Response lỗi**: `{"status": false, "infoCard": [], "errorMessage": "<JP từ getMessageErrorUnivapay()>"}` (:2645-2647)
**Exception**: `{"status": false, "errorMessage": "<exception message, tiếng Anh>"}` (:2655-2660)

---

### EP-P10 — `POST /ajax/calendar-payment-stripe`

**Tham số** (:849-858)

| Tên | Vị trí | Kiểu | Bắt buộc | Validation thật |
|---|---|---|---|---|
| `amount` | body | int | Có | **Không validate, không đối chiếu `calendar_course.amount`** |
| `courseId` | body | int | Có | dùng trong `checkCanBooking()` |
| `calendarId` | body | int | Có | |
| `reception_id` | body | int | Có | |
| `line_user_id` | body | string (`line_id`) | Có | `LineUser::where('line_id',…)->first()`; **không kiểm tra null** ⇒ `$lineUser->id` gây exception (:872-874) |
| `email`, `name` | body | string | Không | rỗng ⇒ lấy `line_user.email` (:890-892) |
| `pm_id` | body | string (Stripe PaymentMethod) | Có | |
| `customer_id` | body | string | Không | rỗng ⇒ tạo customer mới + attach PM |
| `approve_type` | body | `1`\|`2` | Có | **Client quyết định** thu tiền ngay (1) hay chỉ lưu thẻ (2) (:924) |
| `botId` | body | int | Không | Bị **ghi đè** bằng `$calendar->bot_id` (:878) — an toàn |

**Luồng** (:848-1040)

```
checkCanBooking()  →  chọn secretKey theo calendar.environment
  ├── customer_id rỗng → createCustomer() → attachPaymentMethodToCustomer()
  ├── approve_type == 1 (thu ngay)
  │     handleKeepSlot() → giữ chỗ (checkValidSlot) + tạo booking (status=1, payment_status=0)
  │     paymentIntents(confirm=true, setup_future_usage=off_session)
  │       ├─ lỗi → deleteOrderError() (forceDelete booking + đếm lại reception)
  │       └─ ok  → lưu charge_id; status != 'succeeded' ⇒ trả client_secret + isConfirm=true
  └── approve_type != 1  →  isPaymentAfter = true
        setupIntent() — CHỈ lưu thẻ, KHÔNG tạo booking, KHÔNG giữ chỗ
```

**Response thành công**
```json
{ "status": "success", "customer_id": "cus_…", "charge_id": "pi_…",
  "isConfirm": false, "client_secret": null, "errorMessage": null,
  "isPaymentAfter": false, "bookingId": 37811, "bookingType": "new" }
```
`bookingType` = `'new'` \| `'notify'` (`handleKeepSlot()` :1232-1240).

**Các lỗi**

| Tình huống | Response | Dòng |
|---|---|---|
| `createCustomer` thất bại | `{"status":"error","errorMessage":"<JP từ getMessageError()>"}` | :899-903 |
| Attach PaymentMethod thất bại | `{"status":"error","errorMessage":"<error_message Stripe, tiếng Anh>"}` | :905-913 |
| `paymentIntents` thất bại | `status="error"`, `errorMessage` = `$ex->getMessage()` của Stripe (**tiếng Anh**), booking bị **xoá cứng** | :966-971, `StripePayment.php:368-372` |
| Hết chỗ | Exception 「予約がいっぱいです。別の枠を予約してください。」 → `{"status":"error","errorMessage":…,"error_code":0}` | :1229, :1023-1039 |
| Khoá học không hiển thị | 「コースが存在していません。」, `error_code = 1` | :2080-2082 |
| Slot không tồn tại | 「予約の時間が存在していません。」, `error_code = 2` | :2101-2103 |
| Chưa mở nhận đặt | 「予約の受付を開始していません。」 | :2118 |
| Quá hạn nhận đặt | 「予約の受付が終了されました。」 | :2134, :2141 |
| Vượt giới hạn/khách | 「1人あたりの予約受付上限に達しています」 | :2093 |

**Từ điển thông điệp lỗi thẻ** `getMessageError($errorMessage, $code)` (:815-846) — 16 mã Stripe → text tiếng Nhật; mã không khớp ⇒ dùng `processing_error` 「カードの処理中にエラーが発生しました。…」.

---

### EP-P11 — `POST /ajax/calendar-payment-univapay`

**Tham số**: giống EP-P10, thay `pm_id`/`customer_id` bằng `univapay_token`, `univapay_customer_id`, `univapay_customer_code` (:1043-1053).

**Luồng** (:1042-1221)
1. `checkCanBooking()` (:1073).
2. `isProcessWithWebhook($stripBot)` — true khi có `univapay_webhook_id` và `strip_bots.status_webhook == 1` (`app/Helpers/functions.php:138-147`).
3. `handleKeepSlot()` — **luôn gọi**, bất kể `approve_type` (:1086).
4. `chargeMoneyUnivapaySale()` với `metaData = {module:'lesson', booking_id: Hashids(bookingId), bot_id: Hashids(botId), booking_type, transaction_token_id, univapay_customer_code, shipping_details}` (:1105-1124).
5. Ghi `charge_id` vào booking (:1128-1132).
6. Nhánh kết quả:
   - `!success` ⇒ `errorMessage` (JP) + `isDeleteBooking = true`.
   - `isProcessWithWebhook` ⇒ `checkStatusProcessCallback($bookingId)` (poll tối đa 5 lần × `sleep(1)`, `CalendarCourseBookingService.php:1958-1994`):
     - `STATUS_WEBHOOK_ERROR (2)` ⇒ lỗi + xoá booking.
     - `STATUS_WEBHOOK_UNPROCESSED (0)` ⇒ set `status_webhook = 4 (TIMEOUT_WEBHOOK)`, trả **`status: "pending"`** (màn L18) (:1152-1166).
   - không webhook ⇒ `getChargesSale()`; thất bại + `status == 'failed'` ⇒ xoá booking; nếu tổng thời gian > 120s thì gửi tin LINE cảnh báo cho user (:1176-1194).

**Response thành công**
```json
{ "status": "success", "charge_id": "…", "errorMessage": null,
  "bookingId": 37811, "bookingType": "new",
  "url_line_chat": "https://line.me/R/ti/p/@xxx",
  "isProcessWithWebhook": true, "startTimeAction": "2026-08-21 10:00:00" }
```
**Response pending**: `{"status":"pending","charge_id":"…","errorMessage":null,"bookingId":…,"bookingType":"…","isProcessWithWebhook":true}`
**Response lỗi**: `{"status":"error","errorMessage":"<JP>",…}` hoặc `{"status":"error","errorMessage":"<exception, tiếng Anh>","error_code":…}`.

---

### EP-P12 — `POST /ajax/calendar-order`

Endpoint chốt đặt chỗ — **cũng là endpoint duy nhất cho luồng KHÔNG thanh toán và cho 「通知受け取り」**.

**Tham số** (:1415-1449)

| Tên | Vị trí | Kiểu | Bắt buộc | Validation thật |
|---|---|---|---|---|
| `amount` | body | int | Có | **Không đối chiếu giá khoá học.** Bị ép `0` khi `register_notify_slot` (:1476-1478) |
| `courseId` | body | int | Có | |
| `calendarId` | body | int | Có | sai ⇒ `{"status":false,"errorMessage":"Calendar does not exit"}` (**tiếng Anh + sai chính tả "exit"**, :1453-1458) |
| `reception_id` | body | int | Có | không tồn tại ⇒ `{"status":false,"errorMessage":"reception not exists"}` (**tiếng Anh**, :1576-1581) |
| `line_user_id` | body | string (`line_id`) | Có | không thấy ⇒ `{"status":false,"errorMessage":"line user not exists"}` (**tiếng Anh, lọt ra UI người Nhật**, :1501-1506) |
| `email`, `name` | body | string | Không | ghi thẳng vào booking |
| `checkHasPayment` | body | bool\|`"true"` | Có | **Server tin tuyệt đối** — quyết định `payment_status` và có gọi `checkCanBooking()` hay không (:1468-1487, :1554-1567) |
| `approve_type` | body | `1`\|`2` | Có | **Client quyết định** booking là 「予約確定」(1) hay 「リクエスト」(2) (:1460, :1546-1550) |
| `register_notify_slot` | body | `"true"`\|khác | Không | so sánh **chuỗi** `=== 'true'` (:1430) |
| `bookingId`, `bookingType` | body | int / `'new'`\|`'notify'` | Không | từ response EP-P10/EP-P11 |
| `pm_id`, `customer_id`, `charge_id`, `last4`, `brand_name`, `expired_card`, `payment_email` | body | string | Không | **Ghi thẳng vào booking, không xác minh với cổng thanh toán** |
| `univapay_token`, `univapay_customer_id`, `univapay_customer_code` | body | string | Không | như trên |
| `friend_info_settings` | body | array | Không | `json_encode` → `calendar_course_bookings.friend_info`; đồng thời **ghi đè hồ sơ bạn bè** qua `updateFriendInfoValue()` (:1732-1736) |
| `startTimeAction` | body | datetime | Không | cảnh báo giao dịch chậm > 120s |
| `botId` | body | int | Không | Bị ghi đè bằng `$calendar->bot_id` (:1459) |

**Luồng chính** (:1414-1899) — xem `logic-spec-public.md` §2.

**Response thành công**: `{"status": true, "url_line_chat": "<bot.url_add_friend>"}` (:1888-1891)

**Các lỗi**

| Tình huống | Response |
|---|---|
| Calendar không tồn tại | `{"status":false,"errorMessage":"Calendar does not exit"}` (:1456) |
| `register_notify_slot` nhưng `calendar.is_notify_full_slot == 0` | `{"status":false,"errorMessage":"この機能は現在利用できませんん。","error_code":3}` — **nguyên văn có lỗi chính tả 2 chữ ん** (:60, :1462-1464) |
| LINE User không tồn tại | `{"status":false,"errorMessage":"line user not exists"}` (:1504) |
| Reception không tồn tại | `{"status":false,"errorMessage":"reception not exists"}` (:1533, :1579) |
| Đã đăng ký 「通知受け取り」 mà slot vẫn kín | `{"status":false,"errorMessage":"キャンセル待ち通知受け取りがすでに登録されています。"}` (:1537-1542) |
| Trùng đặt chỗ đồng thời | Exception 「予約がいっぱいです。別の枠を予約してください。」 → `{"status":false,"errorMessage":…,"error_code":0}` (:1687) |
| Các lỗi từ `checkCanBooking()` | như bảng EP-P10 |

---

### EP-P13 — `POST /ajax/calendar-delete-order-confirm-fail`

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `bookingId` | body | int | Có |
| `receptionId` | body | int | Có |

**Xử lý** (:1371-1384): `CalendarCourseBooking::where('id',$bookingId)->forceDelete()` (**xoá cứng, bỏ qua SoftDeletes**) rồi `countTotalBookingStatus($receptionId)`.

**Response**: `{"status": true}` — **luôn `true`**, kể cả khi `bookingId` không tồn tại.

> 🔴 **IDOR huỷ diệt**: không xác thực, không kiểm tra chủ sở hữu, không kiểm tra `bookingId` thuộc `receptionId`. Gửi `bookingId` tăng dần ⇒ **xoá vĩnh viễn mọi đặt chỗ của mọi bot**. Confidence: Cao.

---

### EP-P14 — `POST /ajax/calendar-cancel-booking`

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `id` | body | int | Có | `find($bookingId)`; **không kiểm tra null** ⇒ `$booking->status` gây 500 nếu id sai (:2161-2163) |

**Ba nhánh theo `booking.status`**

| # | `status` vào | Hành động | Response |
|---|---|---|---|
| 1 | `3` (`SB_REQUEST_BOOKING_WAIT_CANCEL`) | **Xoá mềm** booking (`->delete()`), `countTotalBookingStatus()`, xoá `mobile_notifies` (`lesson_booking_id`=id, `type`=calendar_lesson, `is_confirm`=0, `status`=1), `recountAppBadgeNotify(getBotId())` | `{"status":true,"delete_booking":true}` (:2165-2181) |
| 2 | `5` (`SB_REQUEST_BOOKING_CANCEL`) | **Rút lại yêu cầu huỷ** → `status` về `2` nếu có `admin_id`, ngược lại `1`; cập nhật `user_update_time` | `{"status":true,"cancel_request_booking":true,"status_order":1\|2}` (:2182-2196) |
| 3 | còn lại | Luồng huỷ chuẩn (dưới) | `{"status":true,"status_order":<4\|5>}` (:2380-2383) |

**Nhánh 3 chi tiết** (:2198-2385)
1. Đọc `calendar_setting_send_messages` `moment = 'cancel'`.
2. `deadline_cancel_booking_type == 2` ⇒ `checkIsValidCancel()`; sai ⇒ Exception 「キャンセルできません。」 (:2228-2240).
3. Ánh xạ trạng thái:

| `status` vào | `approve_type` (cancel) | `status` ra | Lịch sử |
|---|---|---|---|
| `1`/`2` | `1` | `4` (`SB_BOOKING_CANCEL`) | `SB_REQUEST_CANCEL_AUTO_APPROVE`, reason `REASON_USER_CANCEL` |
| `1`/`2` | `2` | `5` (`SB_REQUEST_BOOKING_CANCEL`) | `SB_REQUEST_CANCEL_WAITING_APPROVE`, reason `REASON_REQUEST_CANCEL` |
| `0` (`SB_REQUEST_BOOKING`) | bất kỳ | `4` — **huỷ luôn, không cần duyệt** | `SB_REQUEST_CANCEL_AUTO_APPROVE`; đồng thời đổi lịch sử `SB_REQUEST_BOOKING_WAITING_APPROVE` → `…_HISTORY` (:2255-2270) |
| khác (`4`,`6`,`7`) | — | `$statusUpdate = null` ⇒ **UPDATE `status = NULL`** ⚠ | vẫn tạo bản ghi lịch sử với `status = null` |

4. `countTotalBookingStatus()`; `insertNotifyLesson($booking,'autoCancel'\|'requestCancel')`; `CalendarGoogleSheetService::updateStatusBooking()`.
5. Nếu `approve_type == 1`: **xoá các `event_step_time` chưa gửi** (`status = 0`) có `user_booking_id = booking.id` và `event_step.type = 4` (:2332-2342).
6. `sendAction()` code `'11005'` (huỷ xong) hoặc `'11006'` (yêu cầu huỷ) (:2344-2354).
7. Gửi tin LINE nếu có `message_send_end` / `message_send_booking`; thành công ⇒ `bots.free_send_count += 1` và `updateMessageSendCount(botId, today, 3, 1)` (:2356-2374).
8. `status` ra là `4` ⇒ `sendNotifyWhenThereIsSlotEmpty($reception_id, $calendar_id)` — bắn tin cho người đăng ký 「通知受け取り」 (:2376-2379).

**Lỗi**: `{"status": false, "error_message": "<message>"}` (:2385-2389) — **key `error_message` (snake), khác các endpoint khác dùng `errorMessage`**.

> 🔴 **IDOR**: không kiểm tra người gọi sở hữu booking ⇒ huỷ đặt chỗ người khác, hoặc **rút lại yêu cầu huỷ** của người khác.
> ✅ **Xác minh nghi vấn #1**: nhánh 2 (`status 5` → `1`/`2`) **có route** (`web.php:3854`) và hoạt động được, nhưng **không client nào gọi**: `booking.js:944-949 cancelRequestCancel()` không được blade nào bind, màn L14 hiển thị text chết 「キャンセルリクエストの取り消しはできません」. Đây là **năng lực backend bị UI khoá lại** — không phải bug backend. Confidence: Cao.

---

### EP-P15 — `GET /ajax/get-list-booking-history-calendar`

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `line_user_id` | query | string (`line_id`) | Có | không thấy ⇒ trả `{"currentBookings":[],"beforeBookings":[]}` — **thiếu key `waitingBookings`** (:2396-2403) |
| `calendarId` | query | int | Có | |
| `type` | query | `'list'`\|`'month'` | Không | `'month'` ⇒ lọc theo `month` |
| `month` | query | `Y-m-d` | Khi `type='month'` | |

**Ba truy vấn** (:2409-2547), đều JOIN `calendar_course_receptions` + `calendar_course`, filter `calendar_id` + `line_user_id`:

| Nhóm | Điều kiện thời gian | Điều kiện trạng thái |
|---|---|---|
| `currentBookings` | `CONCAT(received_booking_date,' ',start_time) > NOW()` | `NOT ((status=1 AND payment_status=0 AND status_webhook IN (0,3,4)) OR status=3)` (:2417) |
| `beforeBookings` | `… < NOW()` | `NOT (status=1 AND payment_status=0 AND status_webhook IN (0,3,4))` (:2475) |
| `waitingBookings` | `… > NOW()` | `status = 3` (:2515) |

`currentBookings` được bổ sung `is_can_cancel` (`checkIsValidCancel()` khi `deadline_cancel_booking_type == 2`) và `new_end_time` (:2451-2467).

**Response**
```json
{
  "currentBookings": [
    { "id": 37811, "payment_status": 1, "course_id": 45, "status": 1,
      "received_booking_date": "2026-09-01", "start_time": "10:00:00",
      "end_time": "11:00:00", "course_name": "体験レッスン", "course_image": "…",
      "payment_amount": "3,000", "hour_done": 1, "minute_done": 0,
      "friend_info": "[{…}]", "amount": 3000, "last4": "4242",
      "brand_name": "visa", "charge_id": "pi_…", "payment_card_number": null,
      "payment_card_expired": "12/28", "is_can_cancel": true,
      "new_end_time": "11:00:00" }
  ],
  "waitingBookings": [],
  "beforeBookings": []
}
```

> ⚠ Trả `friend_info` (JSON toàn bộ câu trả lời form: tên/email/SĐT), `last4`, `charge_id`, `payment_card_expired`. Không xác thực ⇒ biết `line_id` của ai là đọc được toàn bộ lịch sử + PII của người đó.

---

### EP-P16 — `GET /ajax/get-detail-booking-calendar`

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `booking_id` | query | int | Có |
| `calendar_id` | query | int | Có (để đọc setting huỷ) |

**Response OK**: `{"status": true, "booking": { …cùng bộ cột EP-P15, kèm is_can_cancel } }` (:2620)
**Response lỗi**: `{"status": false, "error_message": "予約が削除されました。"}` (:2593-2598)

> 🔴 **IDOR đọc dữ liệu nghiêm trọng nhất**: `booking_id` là **số nguyên tự tăng**. Không kiểm tra `line_user_id`, **không kiểm tra `booking.calendar_id == calendar_id`**. Duyệt `booking_id = 1,2,3,…` ⇒ rút toàn bộ `friend_info` (họ tên, email, SĐT, mọi câu trả lời form), 4 số cuối thẻ, hạn thẻ, `charge_id`, số tiền của **TẤT CẢ đặt chỗ trên toàn hệ thống, xuyên bot**. Confidence: Cao (:2557-2620).

---

### EP-P17 — `POST /ajax/mobile/calendar-salon/check-friend` (dùng chung với FA-020)

Route: `routes/web.php:3810` (group `prefix => '/ajax/mobile/calendar-salon'`) → `Mobile\CalendarSalonController@checkFriend` (:4408-4438).

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `botId` | body | int | Có |
| `line_user_id` | body | string (`line_id`) | Có |

**Xử lý**: tìm `line_user` theo `line_id`; tìm `bot_line_user` (`bot_id`, `line_user_id`, `is_blocked = 0`). Thiếu một trong hai ⇒ `{"success": false, "url": "<bot.url_add_friend>"}`; đủ ⇒ `{"success": true}`.

> ✅ **Xác minh nghi vấn #5**: FA-019 (`public/js/booking_news/booking.js:409`) gọi endpoint thuộc **FA-020 (calendar-salon)**. Đây là phụ thuộc chéo thật. Xem §4. Confidence: Cao.

---

# PHẦN B — API ứng dụng di động của Admin (`Api\CalendarLessonController`)

File: `app/Http/Controllers/Api/CalendarLessonController.php` (1862 dòng)
Prefix chung: `POST /api/mobile/calendar-lesson/…` — **tất cả đều là POST**.
Xác thực: guard `api-mobile` + `mobile_contract_expire` (xem §0.2).

## B.1 Bảng tổng hợp endpoint

| Mã | Method | URL | Mô tả | Controller@method | Xác thực | Màn hình liên quan |
|---|---|---|---|---|---|---|
| EP-M01 | POST | `…/change-status-booking` | Duyệt / từ chối / huỷ đặt chỗ (state machine) | `changeStatusBooking` :240 | api-mobile | ảnh hưởng L13/L14 |
| EP-M02 | POST | `…/get-list-calendar-lesson` | Danh sách calendar + URL LIFF | `getListCalendarLesson` :484 | api-mobile + `checkHasPermission('calendar.index')` | sinh link tới L01 |
| EP-M03 | POST | `…/get-calendar-lesson-info-by-id` | Chi tiết 1 calendar | `getCalendarLessonInfoById` :537 | api-mobile | — |
| EP-M04 | POST | `…/get-list-booking-lesson-by-tab` | Danh sách đặt chỗ theo tab 新規/本日 | `getListBookingLessonByTab` :563 | api-mobile | — |
| EP-M05 | POST | `…/get-detail-booking-lesson` | Chi tiết 1 đặt chỗ | `getDetailBookingLesson` :756 | api-mobile | L14 (bản Admin) |
| EP-M06 | POST | `…/get-detail-history-booking-lesson` | Lịch sử thao tác + 20 đặt chỗ gần nhất của khách | `getDetailHistoryBookingLesson` :927 | api-mobile | — |
| EP-M07 | POST | `…/get-detail-history-bill-lesson` | Lịch sử hoá đơn của 1 khách | `getDetailHistoryBillLesson` :986 | api-mobile | — |
| EP-M08 | POST | `…/order-refund` | Hoàn tiền | `orderRefund` :1042 | api-mobile | L16 (ghi chú hoàn tiền) |
| EP-M09 | POST | `…/get-list-course-lesson` | Danh sách khoá học (kể cả ẩn) | `getListCourseLesson` :1162 | api-mobile | — |
| EP-M10 | POST | `…/get-detail-list-calendar-month-day` | Lịch tháng/ngày + đếm đặt chỗ | `getDetailListCalendarMonthOrDay` :1192 | api-mobile | — |
| EP-M11 | POST | `…/course-reception/update` | Sửa sức chứa khung giờ | `updateCourseReception` :1491 | api-mobile | ảnh hưởng L06 |
| EP-M12 | POST | `…/setting-send-form-booking` | Cấu hình form 「お客様情報」 | `getSettingSendForm` :1535 | api-mobile | L07 |
| EP-M13 | POST | `…/add-reception` | Tạo khung giờ hàng loạt | `addNewReception` :1607 | api-mobile | ảnh hưởng L06 |
| EP-M14 | POST | `…/delete-reception` | Xoá khung giờ | `deleteReception` :1665 | api-mobile | ảnh hưởng L06 |
| EP-M15 | POST | `…/add-booking` | Admin đặt chỗ hộ khách | `addNewBooking` :1700 | api-mobile | ảnh hưởng L13 |

Route: `routes/api.php:275-289`.

> **Code chết**: `checkDeleteReception` (:1649) và `changeStatusBookingOld` (:85) tồn tại trong controller nhưng **không có route** nào trỏ tới. Confidence: Cao.
> Response bọc `ResponseData`: `{"result":"ok","data":{…}}` hoặc `{"result":"error","errorMessage":"…"}`.

---

## B.2 Chi tiết từng endpoint

### EP-M01 — `POST …/change-status-booking`

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `bookingId` | body | int | Có | `findById()`; **không kiểm tra null**, không kiểm tra thuộc `botId` |
| `botId` | body | int | Có | |
| `actionChange` | body | enum | Có | `approveBooking` \| `denyBooking` \| `approveCancel` \| `requestCancel` \| `denyCancel` \| `adminCancel`. **Giá trị lạ ⇒ `Undefined index` PHP** (:310) |
| `doAction` | body | `0`\|`1` | Có | có gửi action/tin nhắn kèm hay không |

**Chặn đầu vào** (:294-308): nếu `status_webhook ∈ {0,3,4}` **và** `payment_system == 1` (UnivaPay) → `{"result":"error","errorMessage":"決済処理を行っていますので、操作できません。"}`

**State machine** (:312-473) — chỉ chuyển khi cặp (`status` hiện tại, `actionChange`) khớp:

| `status` hiện tại | `actionChange` | `status` mới | Side effect |
|---|---|---|---|
| `0` REQUEST_BOOKING | `approveBooking` | `1` APPROVE | Nếu `payment_status == 0` ⇒ `courseBookingService->payment()` thu tiền; lỗi ⇒ dừng, trả `errorMessage`. Thành công ⇒ set `charge_id`, `payment_status = 1`, cập nhật Google Sheet, **`addActionRemind()` ghi `event_step_time`** |
| `0` | `denyBooking` | `6` DENY | Không thu tiền |
| `5` REQUEST_BOOKING_CANCEL | `approveCancel` | `4` CANCEL | `sendNotifyWhenThereIsSlotEmpty()`, **xoá `event_step_time` chưa gửi** (:381-392) |
| `5` | `denyCancel` | `1` APPROVE | — |
| `1`/`2` | `requestCancel` | `5` REQUEST_CANCEL | Nếu **không** có `Auth::id()` thì cập nhật `user_update_time` (:424-427) |
| `1`/`2` | `adminCancel` | `7` ADMIN_CANCEL | `sendNotifyWhenThereIsSlotEmpty()`, xoá `event_step_time` chưa gửi (:449-460) |

Sau mỗi nhánh: tạo `calendar_course_booking_history_actions` (kèm `admin_id = Auth::id()`), `sendMessage()` gửi LINE cho khách nếu có `line_user_id`, `insertNotifyLesson()` khi `statusOld != statusNew`.
Cuối method (luôn chạy): `CalendarGoogleSheetService::updateStatusBooking()` + `countTotalBookingStatus()` (:466-469).

**Response OK**: `{"result":"ok"}`

> ⚠ Nếu cặp (status, action) **không khớp** nhánh nào, method vẫn trả `{"result":"ok"}` mà **không làm gì** — app không phân biệt được thành công thật với no-op (:471-476).
> ⚠ Không có `DB::transaction`: thanh toán thành công nhưng bước đổi trạng thái lỗi ⇒ đã trừ tiền mà trạng thái không đổi.

---

### EP-M02 — `POST …/get-list-calendar-lesson`

| Tên | Kiểu | Bắt buộc |
|---|---|---|
| `botId` | int | Có |

**Kiểm tra quyền**: `checkHasPermission('calendar.index', $botId)`; không có quyền ⇒ `{"result":"ok","data":{"data":[],"permission":false,"message":"この機能の操作権限が付与されていません。"}}` (:491-501).

**Response OK**

```json
{ "result":"ok",
  "data": { "data": [ { "id": 123, "calendar_name": "…",
                        "enable_use_calendar": true, "is_use_payment": 1,
                        "url_booking": "https://liff.line.me/{liffId}?calendar_id=123&ts=1755…",
                        "url_history_booking": "https://liff.line.me/{liffId}?calendar_id=123&tab=history&ts=1755…" } ],
            "base_path": "<URL_SERVER_MEDIA>", "permission": true,
            "message": "この機能の操作権限が付与されていません。" } }
```

`liffId` = `bots.liff_app_id_booking` ?: `bots.liff_app_id` (:506). Trường `message` được trả **kể cả khi `permission = true`** — dữ liệu thừa dễ gây hiểu nhầm (:518).

---

### EP-M03 — `POST …/get-calendar-lesson-info-by-id`

| Tên | Kiểu | Bắt buộc |
|---|---|---|
| `calendarId` | int | Có |

`CalendarManagement::find($calendarId)` → trả **toàn bộ record** (:541-546).

> 🔴 **Không kiểm tra calendar thuộc bot của người đăng nhập** ⇒ IDOR xuyên tài khoản: Admin bất kỳ đọc được cấu hình calendar của Admin khác. Confidence: Cao.
> Log ghi nhầm tên method: `'Api getCalendarSalonInfoById start'` (:540) — copy-paste từ FA-020.

---

### EP-M04 — `POST …/get-list-booking-lesson-by-tab`

| Tên | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `botId` | int | Có | **Đọc vào biến nhưng không dùng để lọc** (:567) |
| `calendarId` | int | Có | Điều kiện lọc duy nhất |
| `tab_query` | `'new_booking'`\|`'today_booking'` | Không | quyết định điều kiện + sắp xếp |
| `keyword` | string | Không | LIKE `%kw%` trên `line_user.name`, `line_user.view_name`, `calendar_course_bookings.line_user_name` |
| `isCancel` | bool | Không | falsy ⇒ loại `status ∈ {4,7}` |
| `last_time_new` | datetime | Có (cho `countNewBooking`) | `Carbon::parse()` — rỗng ⇒ parse thành "now" |
| `last_time_today` | datetime | Có (cho `countTodayBooking`) | như trên |

- `new_booking`: `DATE(user_update_time)` trong 7 ngày gần nhất **và** `received_booking_date >= hôm nay`, sắp `user_update_time DESC` (:621-625).
- `today_booking`: `received_booking_date = hôm nay`, sắp `received_booking_date ASC, start_time ASC` (:626-630).
- Phân trang cố định **20/trang** (:660).

**Response**: `{"result":"ok","data":{"countNewBooking":n,"countTodayBooking":m,"data":{<paginator Laravel đầy đủ>},"base_path":"…"}}`

Mỗi item được làm giàu: `dayOfWeek` (JP), `received_booking_date` → `Y.m.d`, `booking_status_text`, `payment_status_text`, `course_name` = `system_name` ?: 10 ký tự đầu `course_name`, `timeBookingFrom`/`timeBookingTo`, `friendInfo` (đã `json_decode`), `lineBookingName`, `userUpdateTime` (:665-724).

`PaginationResource` đã bị comment (:731) — client nhận nguyên cấu trúc paginator của Laravel.

**Từ điển text trạng thái** (`getTextBookingStatus` :890-908 / `getTextStatusPayment` :910-925)

| `status` | text | `payment_status` | text |
|---|---|---|---|
| 1, 2 | 予約確定 | 0 | 未決済 |
| 0, 5 | リクエスト | 1 | 決済成功 |
| 3 | 通知受取希望 | 2 | 決済なし |
| 4, 7 | キャンセル | 3 | 返金済み |
| 6 | 否認済 | khác | `-` |

---

### EP-M05 — `POST …/get-detail-booking-lesson`

| Tên | Kiểu | Bắt buộc |
|---|---|---|
| `botId` | int | Có (không dùng lọc, :761) |
| `calendarId` | int | Có |
| `bookingId` | int | Có |

Query lọc `calendar_id` + `id` + `deleted_at IS NULL`, `->first()->toArray()`.

> 🔴 **Bug chắc chắn**: `->first()->toArray()` gọi trực tiếp trên kết quả — `bookingId` không tồn tại ⇒ `Call to a member function toArray() on null` → rơi vào catch → `{"result":"error"}` **không kèm thông điệp**, client không biết nguyên nhân (:804, :876-885). Confidence: Cao.

**Response OK**: `{"result":"ok","data":{"data":{…booking đã làm giàu như EP-M04, thêm brand_name…},"base_path":"…"}}`

---

### EP-M06 — `POST …/get-detail-history-booking-lesson`

| Tên | Kiểu | Bắt buộc |
|---|---|---|
| `botId`, `calendarId` | int | `botId` không dùng |
| `bookingId` | int | Có — lấy `calendar_course_booking_history_actions` |
| `line_user_id` | int (`line_user.id`) | Không — có thì trả thêm 20 đặt chỗ gần nhất, gom theo năm |

**Response**: `{"result":"ok","data":{"data":{"history":[…CalendarCourseBookingHistoryAppResource…],"pagination":{…}|[],"lastBooking":{"2026":[{"id","status","date","startTime","endTime","courseName"}]}|{}}}}` (:945-955)

---

### EP-M07 — `POST …/get-detail-history-bill-lesson`

| Tên | Kiểu | Bắt buộc |
|---|---|---|
| `calendarId` | int | Có |
| `line_user_id` | int | Có (rỗng ⇒ trả 0/rỗng) |

Truy vấn `calendar_course_bookings` của khách trong calendar: `sum(payment_amount)`, `count()`, phân trang 20, bọc `CalendarLessonHistoryBillResource`, gom theo năm (:996-1019).

> ⚠ Điều kiện `whereNotNull('charge_id')` **đã bị comment** (:993) ⇒ `totalAmount` cộng cả booking chưa/không thanh toán, kể cả đã huỷ hoặc bị từ chối. Sai lệch số liệu doanh thu. Confidence: Cao.

---

### EP-M08 — `POST …/order-refund`

| Tên | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `botId` | int | Có | dùng lấy `strip_bots` |
| `booking_id` | int | Có | `withTrashed()->find()` — hoàn được cả booking đã xoá mềm (:1053) |
| `refundType` | `'now'` \| khác | Có | `'now'` = gọi API hoàn tiền thật; khác = **chỉ đánh dấu**, không gọi cổng |

**Luồng `refundType == 'now'`** (:1055-1121)

- `payment_system == 0` (Stripe): `StripePayment::refundMoneyPaymentIntent($booking->charge_id)`, secret key theo `booking->environment`. Lỗi ⇒ `{"result":"error","errorMessage":"<Stripe message, tiếng Anh>"}`.
- ngược lại (UnivaPay): `refundMoney()` → `getRefundMoney()` xác nhận. Lỗi ⇒ `errorMessage` tiếng Nhật từ `getMessageErrorUnivapay()`.
- `charge_id` rỗng ⇒ **bỏ qua toàn bộ khối gọi cổng** nhưng vẫn đánh dấu đã hoàn tiền (:1057).

**Luôn thực hiện sau đó** (:1125-1141): `payment_status = 3 (SP_REFUND)`, `admin_id = Auth::id()`, `refund_type = <refundType>`; cập nhật Google Sheet; ghi lịch sử `SB_REFUND` với reason `'¥{amount}︎の返金（エルメから）'` (now) hoặc `'…（決済システムから）'` (khác).

**Response OK**: `{"result":"ok","data":{"status":true}}`

> ⚠ Không kiểm tra `payment_status` hiện tại ⇒ gọi hoàn tiền nhiều lần được; lần 2 cổng sẽ báo lỗi, nhưng nếu `charge_id` null thì đánh dấu `SP_REFUND` không giới hạn. Không kiểm tra booking thuộc `botId`.

---

### EP-M09 — `POST …/get-list-course-lesson`

| Tên | Kiểu | Bắt buộc |
|---|---|---|
| `botId` | int | Có (không dùng) |
| `calendarId` | int | Có |

`calendar_course` WHERE `calendar_id`, ORDER BY `course_order ASC` — **không lọc `booking_page_display`** (khác EP-P03), trả cả khoá học đang ẩn (:1169-1172). Đúng ý đồ cho màn Admin.

---

### EP-M10 — `POST …/get-detail-list-calendar-month-day`

| Tên | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `calendarId` | int | Có | |
| `displayMode` | `'month'`\|`'day'` | Có | |
| `date` | `Y-m-d` | Có | |
| `courseIds` | int[] | Không | lọc theo khoá học |
| `status` | int[] | Không | lọc trạng thái đặt chỗ |
| `payment_status` | int[] | Không | lọc trạng thái thanh toán |
| `isFilter` | bool | Không | `false` ⇒ nhánh tổng hợp toàn bộ khung giờ trong tháng |

Trả cấu trúc lịch theo ngày (`calendarTimes[day]`) kèm thông tin `calendar_course_receptions` + số đếm.

> Khối chuyển đổi `bookingStatus` (map 1→[1,2], 2→[0], 3→[5], 4→[4,7]) **đã bị comment** (:1206-1222) ⇒ app phải tự gửi mã trạng thái thô. Confidence: Cao.

---

### EP-M11 — `POST …/course-reception/update`

| Tên | Kiểu | Bắt buộc |
|---|---|---|
| `botId`, `calendarId` | int | Có (`botId` không dùng) |
| `receptionId` | int | Có |
| `maxPerson` | int | Có |
| `typeLimit` | `0`\|`1` | Có |

Cập nhật `total_person`, `type_limit_booking` (:1503-1506).
Nếu (`maxPerson > total_booking` && `typeLimit == 1`) **hoặc** `typeLimit == 0`, **và** slot đang kín (`total_booking == total_person`) ⇒ `sendNotifyWhenThereIsSlotEmpty()` — bắn tin cho người đăng ký 「通知受け取り」 (:1508-1512).

> ⚠ **Không kiểm tra `maxPerson >= total_booking`** ⇒ Admin có thể hạ sức chứa xuống dưới số người đã đặt, tạo overbooking vĩnh viễn. Confidence: Cao.

---

### EP-M12 — `POST …/setting-send-form-booking`

| Tên | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `calendarId` | int | Có | |
| `bot_id` | int | Có | **snake_case, khác mọi endpoint còn lại dùng `botId`** (:1540) |

`getSettingForm()` (:1574-1605): nếu calendar **chưa có** `calendar_setting_send_forms` nào thì **tự tạo 2 bản ghi mặc định** 「お名前を入力してください」 (`friend_information_id = -1`) và 「メールアドレスを入力してください」 (`= -3`, rule email).
Sau đó lọc bỏ radio/checkbox không có options và chỉ giữ `enable` truthy (:1545-1552); datetime `date_form == 1` ⇒ `date_beginning = hôm nay`.

> ⚠ Endpoint mang ngữ nghĩa "GET" nhưng **có side effect ghi DB**. Confidence: Cao.

---

### EP-M13 — `POST …/add-reception`

| Tên | Kiểu | Bắt buộc |
|---|---|---|
| `courseId` | int | Có |
| `needEndTime` | bool\|`"true"` | Có → `set_end_time` 0/1 |
| `dateCanBooking` | string[] (`Y-m-d`) | Có |
| `settingTime` | array of `{startTime, endTime, maxPerson, typeLimit}` | Có |

Vòng lặp lồng: mỗi ngày × mỗi khung giờ ⇒ `checkExistReception()`; chưa có thì `create()` (:1613-1628).

> ⚠ **Không giới hạn số lượng** ⇒ mảng lớn tạo hàng chục nghìn bản ghi trong 1 request, không transaction. Thiếu key trong mảng ⇒ `Undefined index` → catch → `{"result":"error"}` không kèm message.

---

### EP-M14 — `POST …/delete-reception`

Nhận `$request->all()` chuyển thẳng cho `CalendarCourseReceptionService::deleteFromApp()` (:1671).
Nếu service trả đúng chuỗi 「「ステータス：予約確定」の予約が残っています。 受付枠を削除する場合、この受付枠の全ての予約が 「ステータス：キャンセル」になっている必要があります。」 ⇒ `{"result":"error","errorMessage":"<chuỗi đó>"}` (:1672-1679).

> ⚠ Điều kiện lỗi so sánh **bằng chuỗi tiếng Nhật cứng** — sửa một ký tự ở service sẽ âm thầm biến lỗi thành thành công. Nợ kỹ thuật.
> Ghi chú trong code: dùng `deleteFromApp` thay `delete()` vì `getBotId()` dựa session vốn rỗng trên app (BUG #38208, :1667-1669).

---

### EP-M15 — `POST …/add-booking`

| Tên | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `calendarId` | int | Có | |
| `receptionId` | int | Có | `find()` **không kiểm tra null** ⇒ exception (:1704) |
| `botId` | int | Có | |
| `showSelectUser` | `1`\|`2` | Có | `1` = chọn bạn bè LINE (`lineUserId`), `2` = nhập tên tự do (`lineUserName`) |
| `lineUserId` / `lineUserName` | int / string | Theo `showSelectUser` | |
| `name`, `email` | string | Có | |
| `doAction` | `0`\|`1` | Có | `1` ⇒ `sendActionBooking(… 'lessonAdminBooking' …)` |
| `formQuestion` | array | Không | lưu vào `friend_info` + ghi đè hồ sơ bạn bè |

**Ghi DB** (:1714-1739): `status = SB_BOOKING_ADMIN_BOOK (2)`, `payment_status = SP_NO_PAYMENT (2)`, `payment_amount` = `calendar_course.amount`, `admin_id = Auth::id()`, `environment` = `calendar.environment`.
Nếu đã có booking `status = 3` của khách ở slot đó ⇒ **cập nhật đè** bản ghi cũ thay vì tạo mới (`getBookingWaitCancel()`, :1733-1739).

Sau đó: `countTotalBookingStatus()`; ghi đè hồ sơ bạn bè theo `formQuestion` (bỏ qua checkbox, bỏ qua `recording_time == 1`, :1745-1812); `sendActionBooking()` nếu `doAction == 1`; ghi lịch sử `SB_REQUEST_BOOKING_ADMIN_BOOK`; đẩy Google Sheet; **`addActionRemind()` ghi `event_step_time`** nếu có `line_user_id`; `insertNotifyLesson($booking, 'autoApprove')`.

**Response OK**: `{"result":"ok","data":{"data":null,"success":true}}`
**Response lỗi**: `{"result":"error","errorMessage":"<exception message>"}` (:1846-1851)

> 🔴 **Không kiểm tra sức chứa**: `addNewBooking` **không gọi** `checkValidSlot()` hay `checkCanBooking()` ⇒ tạo được số booking vượt `total_person` không giới hạn. Confidence: Cao (:1700-1745).

---

## 3. Cảnh báo bảo mật

### 3.1 Phần A — trang public LIFF

Xếp theo mức nghiêm trọng giảm dần. Tất cả **Confidence: Cao** (đọc trực tiếp code).

| # | Mức | Lỗ hổng | Endpoint | Bằng chứng |
|---|---|---|---|---|
| S-01 | 🔴 Nghiêm trọng | **IDOR đọc — rò rỉ PII hàng loạt.** `booking_id` là số nguyên tự tăng; không kiểm tra chủ sở hữu, **không kiểm tra `booking.calendar_id == calendar_id`**. Duyệt id ⇒ lấy `friend_info` (họ tên, email, SĐT, mọi câu trả lời form), `last4`, `payment_card_expired`, `charge_id`, số tiền của **mọi booking trên toàn hệ thống, xuyên bot** | EP-P16 | `CalendarController.php:2557-2620` |
| S-02 | 🔴 Nghiêm trọng | **IDOR ghi — xoá vĩnh viễn đặt chỗ.** `forceDelete()` theo `bookingId` client gửi, không xác thực, luôn trả `{"status":true}` | EP-P13 | `:1371-1384` |
| S-03 | 🔴 Nghiêm trọng | **IDOR ghi — huỷ / rút yêu cầu huỷ đặt chỗ người khác.** Chỉ cần `id` | EP-P14 | `:2157-2196` |
| S-04 | 🔴 Nghiêm trọng | **Bỏ qua thanh toán.** `checkHasPayment`, `amount`, `approve_type` đều do client gửi, server **không đối chiếu** với `calendar_course.amount` / `calendar_management.is_use_payment` / `calendar_setting_send_messages.approve_type`. Gửi `checkHasPayment=false` ⇒ `payment_status = SP_NO_PAYMENT (2)`, booking `status = 1` 「予約確定」 mà **không mất tiền** | EP-P12 | `:1425-1430`, `:1468-1487`, `:1546-1567` |
| S-05 | 🔴 Nghiêm trọng | **Rò rỉ hồ sơ bạn bè.** Có `line_id` là lấy được tên/email/SĐT/ngày sinh/tỉnh/mọi trường tuỳ biến | EP-P06 | `:643-724` |
| S-06 | 🟠 Cao | **Ghi đè hồ sơ bạn bè không xác thực.** `friend_info_settings` gửi kèm `order()` sẽ **UPDATE `line_user.view_name/phone_number/email/birthday/province` và `friend_information_values`** của LINE User được chỉ định bằng `line_user_id` | EP-P12 | `:1732-1736`, `:1934-2071` |
| S-07 | 🟠 Cao | **Không CSRF trên mọi endpoint ghi.** `'/ajax/*'` nằm trong `VerifyCsrfToken::$except` ⇒ trang bên thứ ba có thể POST tạo/huỷ/xoá đặt chỗ | EP-P10…P14 | `VerifyCsrfToken.php:16` |
| S-08 | 🟠 Cao | **Không rate limit.** `throttle` đã bị comment ⇒ quét toàn bộ `booking_id`, tạo customer UnivaPay hàng loạt, DoS bằng `getListTimeBookingByCourse` (mỗi request có thể chạy 5 truy vấn tuần) | Toàn bộ Phần A | `Kernel.php:44-47` |
| S-09 | 🟠 Cao | **Rò rỉ lịch sử đặt chỗ theo `line_id`** — trả cả `friend_info`, `charge_id`, `last4` | EP-P15 | `:2409-2547` |
| S-10 | 🟠 Cao | **Client điều khiển môi trường thanh toán** — `environment` gửi từ client quyết định dùng khoá test hay live của UnivaPay | EP-P09 | `:2640` |
| S-11 | 🟡 Trung bình | **Rò rỉ số liệu vận hành.** `select('*')` / `select()` trả toàn bộ cột `calendar_course` và `calendar_course_receptions` (kể cả `total_approve`, `total_cancel`, `message_send_after_booking`, `action_id_…`) | EP-P03, EP-P04 | `:285-289`, `:2765-2769` |
| S-12 | 🟡 Trung bình | **Client cung cấp cấu hình cho server dùng.** `calendar[is_notify_full_slot]`, `calendar[is_display_course_full]` (EP-P05) và `calendarSetting[…]` (EP-P07) do client gửi, server không đọc lại từ DB | EP-P05, EP-P07 | `:519`, `:2905-2907`, `:268-273` |
| S-13 | 🟡 Trung bình | **`botId` do client gửi, không đối chiếu `calendar->bot_id`** khi gọi API UnivaPay bằng khoá bí mật của bot | EP-P08 | `:2692-2697` |
| S-14 | 🟡 Trung bình | **Trang `close-booking` không kiểm tra quyền/filter** — ai có hash cũng xem được thông điệp Admin cấu hình | EP-P02 | `:209-231` |
| S-15 | 🟡 Trung bình | **Rò thông tin qua thông điệp lỗi tiếng Anh**: `'line user not exists'`, `'reception not exists'`, `'Calendar does not exit'`, `'create customer error'`, `'calendar not exists'` — vừa dùng để enumerate, vừa hiển thị trực tiếp cho người dùng Nhật | EP-P08, EP-P12 | `:1456`, `:1504`, `:1533`, `:2679`, `:2723` |
| S-16 | 🟡 Trung bình | **Nguy cơ lộ khoá thanh toán qua view** — controller truyền **toàn bộ record `strip_bots`** vào blade công khai | EP-P01 | `:190` |
| S-17 | 🟢 Thấp | **500 dễ kích hoạt**: `find()` không kiểm tra null (EP-P14 :2161), `$lineUser->id` (EP-P10 :874, EP-P11 :1071), `$calendarSetting->approve_type` (EP-P03 :295) | nhiều | — |

### 3.2 Phần B — API app di động

| # | Mức | Vấn đề | Bằng chứng |
|---|---|---|---|
| S-18 | 🟠 Cao | **Thiếu kiểm tra quyền.** 14/15 endpoint không gọi `checkHasPermission` ⇒ Staff bị hạn chế quyền vẫn duyệt/huỷ/hoàn tiền được qua app | toàn file, đối chiếu `:491` |
| S-19 | 🟠 Cao | **Thiếu kiểm tra sở hữu.** Không endpoint nào xác minh `calendarId`/`bookingId`/`receptionId` thuộc `botId` của tài khoản đăng nhập ⇒ IDOR xuyên tài khoản Admin | EP-M01, M03, M05, M08, M11, M15 |
| S-20 | 🟡 Trung bình | **`addNewBooking` không kiểm tra sức chứa** ⇒ overbooking tuỳ ý | `:1700-1745` |
| S-21 | 🟡 Trung bình | **`orderRefund` không kiểm tra `payment_status` hiện tại** ⇒ đánh dấu hoàn tiền lặp | `:1042-1141` |
| S-22 | 🟡 Trung bình | **`updateCourseReception` không chặn hạ sức chứa dưới `total_booking`** | `:1503-1506` |

---

## 4. Phụ thuộc chéo

| Thành phần | Phụ thuộc | Ghi chú |
|---|---|---|
| **FA-020 「サロン予約」** | `POST /ajax/mobile/calendar-salon/check-friend` → `Mobile\CalendarSalonController@checkFriend` (`:4408`) | FA-019 dùng **chung** endpoint kiểm tra bạn bè của FA-020 (`public/js/booking_news/booking.js:409`). Sửa FA-020 ảnh hưởng trực tiếp FA-019. **Đã xác minh** — nghi vấn #5 |
| Job Spring Boot | `event_step_time` (`user_booking_id` = `calendar_course_bookings.id`) | Ghi bởi `addActionRemind()`; xoá bởi EP-P14 và EP-M01. Xem `job-spec.md` §2.1 |
| Job Spring Boot | `mobile_notify` | Ghi bởi `MobileNotifyService::insertNotifyLesson()`; xoá bởi EP-P14 nhánh `status = 3` |
| Google Sheet | `CalendarGoogleSheetService` | `insertDataToGoogleSheet()` ở EP-P12/EP-M15; `updateStatusBooking()` ở EP-P14/EP-M01; `updateStatusPaymentBooking()` ở EP-M01/EP-M08 |
| Webhook UnivaPay | `POST /univapay/get-callback-webhook` → `CalendarCourseBookingService::handleOrderCallback()` (`:1527`) | Hoàn tất booking ở luồng `pending` (màn L18) |
| Hồ sơ bạn bè | `friend_information_values`, `friend_information_settings`, `line_user` | Đọc ở EP-P06, ghi ở EP-P12 và EP-M15 |
| Màn hình timeout dùng chung | `GET /lme/timeout/{bot_id?}/{type?}/{calendar_id?}` (`routes/web.php:4155`) | JS chuyển hướng khi ajax trả 4xx/5xx |
| Filter bạn bè (FilterV2) | `Conversation::advanceFilterPost()` | Dùng ở EP-P01 (`filter_id_show_booking`) và EP-P03 (`filter_id_send_after_booking`) |
