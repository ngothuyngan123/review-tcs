# FA-020 — Đặt lịch salon (「サロン・面談予約」) — API Spec

> Tạo bởi: web-analyzer agent | Ngày: 2026-06-04 | Confidence tổng thể: Cao

---

## 1. Tổng quan

Tất cả endpoint Admin/Staff đều nằm dưới prefix `/basic/` (middleware `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`) hoặc prefix `/ajax/` (middleware `check_login`, `check_remember_token`).

**Controller chính:** `App\Http\Controllers\Basic\CalendarSalonController`
**Controller thanh toán:** `App\Http\Controllers\Basic\SettingPaymentCalendarSalonController`

---

## 2. Danh sách tổng hợp Endpoints

| EP | Method | URL | Controller@method | Màn hình liên quan |
|----|--------|-----|-------------------|--------------------|
| EP-01 | GET | `/basic/calendar-salon` | `CalendarSalonController@index` | SCR-SLN-01 (view) |
| EP-02 | GET | `/basic/calendar-salon/list-calendar-salon` | `CalendarSalonController@getListCalendarSalon` | SCR-SLN-01 |
| EP-03 | POST | `/basic/calendar-salon/create-new-calendar-salon` | `CalendarSalonController@createNewCalendarSalon` | SCR-SLN-01 |
| EP-04 | POST | `/basic/calendar-salon/sort` | `CalendarSalonController@saveSort` | SCR-SLN-01 |
| EP-05 | GET | `/basic/calendar-salon/{calendar_id}` | `CalendarSalonController@detailCalendar` | SCR-SLN-02 (view) |
| EP-06 | GET | `/basic/calendar-salon/{calendar_id}/detail` | `CalendarSalonController@detailCalendarSalon` | SCR-SLN-02 (AJAX) |
| EP-07 | GET | `/basic/calendar-salon/{calendar_id}/get-list-booking` | `CalendarSalonController@getListBooking` | SCR-SLN-02a |
| EP-08 | GET | `/basic/calendar-salon/{calendar_id}/get-staffs-active` | `CalendarSalonController@getListStaffActive` | SCR-SLN-02b (Modal 予約追加) |
| EP-09 | GET | `/basic/calendar-salon/{calendar_id}/get-courses-active` | `CalendarSalonController@getListCourseActive` | SCR-SLN-02b (Modal 予約追加) |
| EP-10 | POST | `/basic/calendar-salon/{calendar_id}/create-booking` | `CalendarSalonController@createBooking` | SCR-SLN-02b |
| EP-11 | GET | `/basic/calendar-salon/{calendar_id}/get-booking-setting-display` | `CalendarSalonController@getDataBookingSettingDisplay` | SCR-SLN-03b |
| EP-12 | POST | `/basic/calendar-salon/{calendar_id}/setting-booking-display` | `CalendarSalonController@settingBookingDisplay` | SCR-SLN-03b |
| EP-13 | GET | `/basic/calendar-salon/{calendar_id}/get-list-courses` | `CalendarSalonController@listsCourse` | SCR-SLN-03a |
| EP-14 | GET | `/basic/calendar-salon/{calendar_id}/get-courses-menu` | `CalendarSalonController@getCoursesMenu` | SCR-SLN-03a |
| EP-15 | GET | `/basic/calendar-salon/{calendar_id}/setting-message` | `CalendarSalonController@getSettingMessage` | SCR-SLN-04a |
| EP-16 | POST | `/basic/calendar-salon/{id}/save-setting-message` | `CalendarSalonController@saveSettingMessage` | SCR-SLN-04a |
| EP-17 | GET | `/ajax/calendar-salon/init-data-setting-payment` | `SettingPaymentCalendarSalonController@initDataSettingPayment` | SCR-SLN-05 |
| EP-18 | POST | `/ajax/calendar-salon/save-setting-payment` | `SettingPaymentCalendarSalonController@saveSettingPayment` | SCR-SLN-05 |
| EP-19 | POST | `/basic/calendar-salon/{calendar_id}/add-work-schedule` | `CalendarSalonController@addWorkScheduleForStaff` | SCR-SLN-02b (Modal シフト追加) |
| EP-20 | POST | `/basic/calendar-salon/{calendar_id}/salon-course/create` | `CalendarSalonController@createCourseSalon` | SCR-SLN-03a |
| EP-21 | POST | `/basic/calendar-salon/{calendar_id}/salon-staff/create` | `CalendarSalonController@createStaffSalon` | SCR-SLN-03 (Staff) |
| EP-22 | GET | `/basic/calendar-salon/{calendar_id}/edit-course/{id}` | `CalendarSalonController@editCourse` | SCR-SLN-03a (view) |
| EP-23 | GET | `/basic/calendar-salon/{calendar_id}/edit-staff/{id}` | `CalendarSalonController@editStaff` | SCR-SLN-03 (view) |
| EP-24 | GET | `/basic/calendar-salon/api/course/{id}/edit` | `CalendarSalonController@course` | SCR-SLN-03a (AJAX detail) |
| EP-25 | POST | `/basic/calendar-salon/api/course/{id}/update` | `CalendarSalonController@updateCourse` | SCR-SLN-03a |
| EP-26 | GET | `/basic/calendar-salon/api/staff/{id}/edit` | `CalendarSalonController@staff` | SCR-SLN-03 (Staff) |
| EP-27 | POST | `/basic/calendar-salon/api/staff/{id}/update` | `CalendarSalonController@updateStaff` | SCR-SLN-03 (Staff) |
| EP-28 | GET | `/basic/calendar-salon/{id}/get-list-staffs` | `CalendarSalonController@getListStaffs` | SCR-SLN-03 (Staff) |
| EP-29 | POST | `/basic/calendar-salon/api/course/{id}/delete` | `CalendarSalonController@deleteCalendarCourse` | SCR-SLN-03a |
| EP-30 | POST | `/basic/calendar-salon/api/staff/{id}/delete` | `CalendarSalonController@deleteCalendarStaff` | SCR-SLN-03 (Staff) |
| EP-31 | POST | `/basic/calendar-salon/{id}/booking/change-status` | `CalendarSalonController@changeStatusBooking` | SCR-SLN-02a |
| EP-32 | DELETE | `/basic/calendar-salon/{id}/booking/delete` | `CalendarSalonController@deleteBooking` | SCR-SLN-02a |
| EP-33 | POST | `/basic/calendar-salon/{calendar_id}/export-csv-staff` | `CalendarSalonController@exportCsvStaff` | SCR-SLN-02a (Modal CSV) |
| EP-34 | POST | `/basic/calendar-salon/{calendar_id}/import-csv-staff` | `CalendarSalonController@importCsvStaff` | SCR-SLN-02a (Modal CSV) |
| EP-35 | GET | `/ajax/calendar-salon/init-setting-free-time-before-after/{id}` | `CalendarSalonController@ajaxGetSettingFreeTimeBeforeAfter` | SCR-SLN-04 (前後の空き時間) |
| EP-36 | POST | `/ajax/calendar-salon/save-setting-free-time` | `CalendarSalonController@saveSettingFreeTime` | SCR-SLN-04 |
| EP-37 | GET | `/ajax/calendar-salon/init-setting-limit-booking/{id}` | `CalendarSalonController@ajaxGetSettingLimitBooking` | SCR-SLN-04 (受付上限) |
| EP-38 | POST | `/ajax/calendar-salon/save-setting-limit-booking` | `CalendarSalonController@saveSettingLimitBooking` | SCR-SLN-04 |
| EP-39 | GET | `/ajax/calendar-salon/get-list-step-remind` | `CalendarSalonController@getListStepRemind` | SCR-SLN-04 (リマインド) |
| EP-40 | POST | `/ajax/calendar-salon/save-setting/remind` | `CalendarSalonController@saveCreateSettingRemind` | SCR-SLN-04 |
| EP-41 | GET | `/ajax/calendar-salon/get-list-courses-by-calendar` | `CalendarSalonController@getListCourseByCalendar` | SCR-SLN-04 |
| EP-42 | POST | `/ajax/calendar-salon/action/delete` | `CalendarSalonController@deleteCalendarSalon` | SCR-SLN-04 (削除) |
| EP-43 | POST | `/ajax/calendar-salon/send-mail/delete` | `CalendarSalonController@sendMailCodeAuthDeleteCalendar` | SCR-SLN-04 (削除) |
| EP-44 | POST | `/ajax/calendar-salon/check-author/delete` | `CalendarSalonController@checkAuthorDeleteCalendar` | SCR-SLN-04 (削除) |
| EP-45 | GET | `/basic/calendar-salon/{id}/booking-staff` | `CalendarSalonController@getBookingStaff` | SCR-SLN-02b (Calendar view) |
| EP-46 | POST | `/basic/calendar-salon/{id}/save-staff-assignment` | `CalendarSalonController@saveStaffAssignment` | SCR-SLN-02b |
| EP-47 | GET | `/basic/calendar-salon/{calendar_id}/get-data-staff-google` | `CalendarSalonController@getStaffCalendarSyncGoogle` | SCR-SLN-04 (Google連携) |
| EP-48 | POST | `/basic/calendar-salon/{calendar_id}/change-google-link` | `CalendarSalonController@changeGoogleLinkForStaff` | SCR-SLN-04 (Google連携) |
| EP-49 | GET | `/ajax/calendar-salon/setting-reservation/get-data-setting-policy` | `CalendarSalonController@getDataSettingPolicy` | SCR-SLN-04 (店舗情報) |
| EP-50 | POST | `/ajax/calendar-salon/save/policy` | `CalendarSalonController@savePolicyCalendar` | SCR-SLN-04 (利用規約) |
| EP-51 | POST | `/ajax/calendar-salon/save/info` | `CalendarSalonController@saveCalendarInfo` | SCR-SLN-04 (店舗情報) |
| EP-52 | POST | `/basic/calendar-salon/{calendar_id}/save-system-word-change` | `CalendarSalonController@saveSystemWordChange` | SCR-SLN-04 (システムワード) |
| EP-53 | GET | `/basic/calendar-salon/{calendar_id}/get-list-booking-delete` | `CalendarSalonController@getListBookingDelete` | SCR-SLN-02a (削除済み予約) |
| EP-54 | POST | `/basic/calendar-salon/{id}/change-display-line-name` | `CalendarSalonController@changeDisplayLineName` | SCR-SLN-02 |
| EP-55 | GET | `/ajax/calendar-salon/get-data-setting-notify-full-slot/{calendar_id}` | `CalendarSalonController@getDataSettingNotifyFullSlot` | SCR-SLN-04 (受付上限通知) |
| EP-56 | POST | `/ajax/calendar-salon/save-setting/notify-full-slot` | `CalendarSalonController@saveSettingNotifyFull` | SCR-SLN-04 |
| EP-57 | DELETE | `/basic/calendar-salon/{id}/staff/delete-time-working` | `CalendarSalonController@deleteTimeWorking` | SCR-SLN-02b (シフト) |
| EP-58 | POST | `/basic/calendar-salon/{id}/staff/update-time-working` | `CalendarSalonController@updateTimeWorkingStaff` | SCR-SLN-02b (シフト) |
| EP-59 | POST | `/basic/calendar-salon/api/course/sortable` | `CalendarSalonController@updateCalendarCourseOrder` | SCR-SLN-03a |
| EP-60 | POST | `/basic/calendar-salon/api/staff/sortable` | `CalendarSalonController@updateCalendarStaffOrder` | SCR-SLN-03 (Staff) |
| EP-61 | POST | `/basic/calendar-salon/course/update-booking-page-display` | `CalendarSalonController@updateBookingPageDisplay` | SCR-SLN-03a |
| EP-62 | POST | `/basic/calendar-salon/staff/update-booking-page-display-staff` | `CalendarSalonController@updateBookingPageDisplayStaff` | SCR-SLN-03 (Staff) |
| EP-63 | POST | `/basic/calendar-salon/{id}/order-refund` | `CalendarSalonController@orderRefund` | SCR-SLN-02a (決済返金) |

---

## 3. Chi tiết Endpoints quan trọng

### EP-02: GET `/basic/calendar-salon/list-calendar-salon`

**Controller@method:** `CalendarSalonController@getListCalendarSalon` (dòng 245)
**Màn hình:** SCR-SLN-01

**Request params:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `staffTypeFilter` | query | int | Không | Lọc loại calendar: 0=tất cả, 1=個人 (一スタッフ), 2=スタッフ (多スタッフ) |

**Response thành công:**
```json
{
  "success": true,
  "data": {
    "calendar_salon": [/* CalendarSalonResource collection */],
    "canCreate": true,
    "enableTooltipCalendar": 1
  },
  "message": ""
}
```

**Ghi chú:** `canCreate` là kết quả `checkMaxCalendarMayBeCreate()` — kiểm tra giới hạn theo plan.

**Confidence:** Cao

---

### EP-03: POST `/basic/calendar-salon/create-new-calendar-salon`

**Controller@method:** `CalendarSalonController@createNewCalendarSalon` (dòng 187)
**Màn hình:** SCR-SLN-01

**Request body (JSON):**

| Param | Kiểu | Bắt buộc | Mô tả |
|-------|------|----------|-------|
| `calendar_name` | string | Có | Tên salon calendar |
| `holidays` | array | Có | Danh sách ngày nghỉ (JSON array) |

**Response thành công:**
```json
{
  "success": true,
  "data": {/* CalendarSalon object */},
  "message": ""
}
```

**Response thất bại (giới hạn plan):**
```json
{
  "success": false,
  "data": null,
  "message": "現在のプランは利用できない機能です。アップグレードが必要になります。"
}
```

**Business logic:** Kiểm tra giới hạn plan → nếu vượt quá trả về lỗi. Nếu đủ, tạo `CalendarSalon` record + `CalendarSalonSettingTimeFree` record mặc định.

**Confidence:** Cao

---

### EP-07: GET `/basic/calendar-salon/{calendar_id}/get-list-booking`

**Controller@method:** `CalendarSalonController@getListBooking` (dòng 660)
**Màn hình:** SCR-SLN-02a

**Request params:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `page` | query | int | Không | Số trang, mặc định 1 |
| `tab_query` | query | string | Không | `new_booking` (新着) hoặc `today_booking` (本日) |
| `per_page` | query | int | Không | Số bản ghi mỗi trang (50 hoặc 100) |
| `date_booking` | query | date | Không | Ngày đặt lịch (format `Y-m-d`) |
| `date_start` | query | date | Không | Bộ lọc: ngày bắt đầu |
| `date_end` | query | date | Không | Bộ lọc: ngày kết thúc |
| `time_start` | query | time | Không | Bộ lọc: giờ bắt đầu |
| `time_end` | query | time | Không | Bộ lọc: giờ kết thúc |
| `course_ids` | query | array | Không | Bộ lọc: danh sách course ID |
| `staff_ids` | query | array | Không | Bộ lọc: danh sách staff ID |
| `booking_status` | query | array | Không | Bộ lọc: trạng thái booking |
| `payment_status` | query | array | Không | Bộ lọc: trạng thái thanh toán |

**Response thành công:**
```json
{
  "success": true,
  "data": {
    "data": [/* danh sách booking */],
    "total": 100,
    "per_page": 50,
    "current_page": 1
  },
  "message": ""
}
```

**Mỗi item booking có các field:** `id`, `received_booking_date`, `start_time`, `end_time`, `booking_status`, `booking_status_text`, `payment_status`, `payment_status_text`, `course_name`, `staff_name`, `payment_amount`, `lineBookingName`, `nextDay`, `userUpdateTime`, `dayOfWeek`

**Confidence:** Cao

---

### EP-08: GET `/basic/calendar-salon/{calendar_id}/get-staffs-active`

**Controller@method:** `CalendarSalonController@getListStaffActive` (dòng 3499)
**Màn hình:** SCR-SLN-02b (Modal 予約追加)

**URL param:** `calendar_id` — ID của salon calendar

**Response thành công:**
```json
{
  "staffs": [
    {
      "id": 1,
      "staff_system_name": "staff 1",
      "staff_name": "Staff One",
      "staff_bill": 1200,
      "booking_page_display": 1
    }
  ]
}
```

**Confidence:** Cao

---

### EP-09: GET `/basic/calendar-salon/{calendar_id}/get-courses-active`

**Controller@method:** `CalendarSalonController@getListCourseActive` (dòng 3482)
**Màn hình:** SCR-SLN-02b (Modal 予約追加)

**Response thành công:**
```json
{
  "courses": [
    {
      "id": 1,
      "course_name": "Course A",
      "system_name": "A",
      "hour_done": "01",
      "minute_done": "30",
      "amount": 1200,
      "booking_page_display": 1
    }
  ]
}
```

**Confidence:** Cao

---

### EP-10: POST `/basic/calendar-salon/{calendar_id}/create-booking`

**Controller@method:** `CalendarSalonController@createBooking` (dòng 3545)
**Màn hình:** SCR-SLN-02b (Modal 予約追加)

**Request body:**

| Param | Kiểu | Bắt buộc | Mô tả |
|-------|------|----------|-------|
| `line_user_id` | int | Có (nếu chọn từ danh sách) | ID LINE user đã có trong hệ thống |
| `manual_name` | string | Có (nếu nhập thủ công) | Tên khách hàng nhập tay |
| `course_id` | int | Có | ID khóa học |
| `staff_id` | int | Không | ID nhân viên phụ trách |
| `date_booking` | date | Có | Ngày đặt lịch (YYYY-MM-DD) |
| `start_time` | string | Có | Giờ bắt đầu (HH:MM) |
| `is_run_action` | bool | Có | Có thực thi action khi đặt lịch không |

**Response thành công:**
```json
{
  "success": true,
  "data": { ... },
  "message": ""
}
```

**Confidence:** Trung bình (delegate sang `CalendarSalonLineBookingService@createBooking`)

---

### EP-13: GET `/basic/calendar-salon/{calendar_id}/get-list-courses`

**Controller@method:** `CalendarSalonController@listsCourse` (dòng 762)
**Màn hình:** SCR-SLN-03a

**Request params:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `course_menu_id` | query | int | Không | Lọc theo menu nhóm khóa học. Rỗng = không lọc |

**Response thành công:**
```json
{
  "success": true,
  "data": [/* danh sách CalendarSalonCourse */],
  "isAdd": true,
  "msg_plan": null
}
```

**Business logic:** Nếu plan free hoặc plan_type=2 và số course >= 2 → `isAdd=false`, `msg_plan` chứa thông báo nâng cấp.

**Confidence:** Cao

---

### EP-15: GET `/basic/calendar-salon/{id}/setting-message`

**Controller@method:** `CalendarSalonController@getSettingMessage` (dòng 1014)
**Màn hình:** SCR-SLN-04a

**URL param:** `id` — ID của salon calendar

**Response thành công:**
```json
{
  "success": true,
  "data": {/* CalendarSalonSettingSendMessage object */},
  "list_preview_filter_calendar_booking": [],
  "number_filter_salon": 0,
  "message": "",
  "message_outside_filter": "詳細は運営元までお問い合わせください"
}
```

**Confidence:** Cao

---

### EP-17: GET `/ajax/calendar-salon/init-data-setting-payment`

**Controller@method:** `SettingPaymentCalendarSalonController@initDataSettingPayment` (dòng 17)
**Màn hình:** SCR-SLN-05
**Prefix:** `/ajax/` — middleware `check_login`, `check_remember_token`

**Request params:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `calendar_id` | query | int | Có | ID của salon calendar |

**Response thành công:**
```json
{
  "status": true,
  "checkLinkPayment": false,
  "settingPayment": {
    "type_payment": 1,
    "environment": 1,
    "description_payment": "...",
    "is_use_payment": 1,
    "payment_time": 1
  },
  "checkLinkedUnivapay": false,
  "checkLinkedStripe": true,
  "listHistoryPayment": [/* lịch sử thay đổi */],
  "contractType": "standard",
  "checkEnableNameAndEmailDefault": true
}
```

**Giải thích fields:**
- `checkLinkPayment`: `true` = chưa liên kết Stripe/UnivaPay → hiện hướng dẫn
- `checkLinkedStripe`: `true` = đã liên kết Stripe
- `checkLinkedUnivapay`: `true` = đã liên kết UnivaPay
- `checkEnableNameAndEmailDefault`: `true` = form booking đã có trường tên + email bắt buộc (điều kiện để dùng thanh toán)

**Confidence:** Cao (đọc trực tiếp source code)

---

### EP-18: POST `/ajax/calendar-salon/save-setting-payment`

**Controller@method:** `SettingPaymentCalendarSalonController@saveSettingPayment` (dòng 152)
**Màn hình:** SCR-SLN-05

**Request body:**

| Param | Kiểu | Bắt buộc | Mô tả |
|-------|------|----------|-------|
| `calendar_id` | int | Có | ID của salon calendar |
| `type_payment` | int | Có (nếu bật) | 1=Stripe, 2=UnivaPay |
| `environment` | int | Có (nếu bật) | 1=本番環境, 2=テスト環境 |
| `description_payment` | string | Không | Nội dung 「特定商取引法に基づく表記」 |
| `payment_time` | int | Không | Phương thức thanh toán khi đặt: 1=予約時のみ, 2=選択可能 |
| `is_use_payment` | string | Có | `"true"` hoặc `"false"` |

**Side effects:**
- Ghi lịch sử thay đổi vào `calendar_salon_history_change_setting_payment`
- Cập nhật `calendar_salon` record
- Khi bật thanh toán: bắt buộc enable trường name (friend_information_id=-1) và email (friend_information_id=-3) trong `calendar_salon_setting_send_forms`

**Response thành công:**
```json
{
  "status": true
}
```

**Confidence:** Cao

---

### EP-19: POST `/basic/calendar-salon/{calendar_id}/add-work-schedule`

**Controller@method:** `CalendarSalonController@addWorkScheduleForStaff`
**Màn hình:** SCR-SLN-02b (Modal シフト追加 / シフト編集)

**Request body:** Delegate sang `CalendarSalonTimeBookingService@addWorkScheduleForStaff`

**Response thành công:**
```json
{
  "status": true,
  "error_message": ""
}
```

**Confidence:** Trung bình

---

### EP-31: POST `/basic/calendar-salon/{id}/booking/change-status`

**Controller@method:** `CalendarSalonController@changeStatusBooking` (dòng 3525)
**Màn hình:** SCR-SLN-02a (Modal リクエスト一括操作)

**Request body:** Delegate sang `CalendarSalonLineBookingService@changeStatusBooking`

**Response thành công:**
```json
{
  "success": true,
  "data": null,
  "message": null
}
```

**Response khi có lỗi thanh toán:**
```json
{
  "success": false,
  "data": null,
  "message": "..."
}
```

**Business logic:** Khi thay đổi status booking có liên quan đến thanh toán, kiểm tra `paymentStatus` trong response của service.

**Confidence:** Trung bình

---

### EP-33: POST `/basic/calendar-salon/{calendar_id}/export-csv-staff`

**Controller@method:** `CalendarSalonController@exportCsvStaff` (dòng 3404)
**Màn hình:** SCR-SLN-02a (Modal CSV管理 - Tab エクスポート)

**Request body:**

| Param | Kiểu | Bắt buộc | Mô tả |
|-------|------|----------|-------|
| `staff_ids` | array | Không | Danh sách staff ID cần export |
| `start_date` | date | Có | Ngày bắt đầu khoảng export |
| `end_date` | date | Có | Ngày kết thúc khoảng export |
| `staff_type` | int | Không | Loại staff (0=個人, 1=staff) |

**Confidence:** Trung bình

---

### EP-42: POST `/ajax/calendar-salon/action/delete`

**Controller@method:** `CalendarSalonController@deleteCalendarSalon` (dòng 2957)
**Màn hình:** SCR-SLN-04 (「予約システムの削除」)

**Request body:**

| Param | Kiểu | Bắt buộc | Mô tả |
|-------|------|----------|-------|
| `id` | int | Có | ID salon calendar |
| `code` | string | Có | Mã xác thực từ email (10 ký tự) |

**Business logic:** Kiểm tra mã code → nếu đúng, xóa cascade toàn bộ dữ liệu liên quan (xem logic spec).

**Confidence:** Cao

---

### EP-45: GET `/basic/calendar-salon/{id}/booking-staff`

**Controller@method:** `CalendarSalonController@getBookingStaff` (dòng 2744)
**Màn hình:** SCR-SLN-02b (Tab 予約カレンダー)

**Request params:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `displayMode` | query | string | Có | `day`, `week`, hoặc `month` |
| `date` | query | date | Có | Ngày hiện tại đang xem |

**Business logic:**
- `day` → `CalendarSalonStaffService@getStaffWithBookingInDay2`
- `week` → `CalendarSalonLineBookingService@getBookingListWeek`
- `month` → `CalendarSalonLineBookingService@getBookingListMonth`

**Confidence:** Cao

---

## 4. Mapping Endpoint ↔ Màn hình UI

| Màn hình | Endpoints |
|----------|-----------|
| SCR-SLN-01: Danh sách calendar | EP-01 (view), EP-02 (AJAX list), EP-03 (tạo mới), EP-04 (sắp xếp) |
| SCR-SLN-02: Trang quản lý chi tiết | EP-05 (view), EP-06 (AJAX detail), EP-54 (LINE name setting) |
| SCR-SLN-02a: Tab 本日／新着の予約 | EP-07 (list), EP-31 (change status), EP-32 (delete), EP-33 (export CSV), EP-34 (import CSV), EP-53 (削除済み) |
| SCR-SLN-02b: Tab 予約カレンダー | EP-08 (staffs), EP-09 (courses), EP-10 (create booking), EP-19 (add shift), EP-45 (calendar data), EP-46 (staff assignment), EP-57, EP-58 (shift CRUD) |
| SCR-SLN-03a: コース作成・編集 | EP-13 (list), EP-14 (course menu), EP-20 (create), EP-22 (view), EP-24 (detail), EP-25 (update), EP-29 (delete), EP-59 (sort), EP-61 (display toggle) |
| SCR-SLN-03b: コースの表示設定 | EP-11 (get), EP-12 (save) |
| SCR-SLN-03 Staff | EP-21 (create), EP-23 (view), EP-26 (detail), EP-27 (update), EP-28 (list), EP-30 (delete), EP-60 (sort), EP-62 (display toggle) |
| SCR-SLN-04a: 予約・キャンセルのメッセージ | EP-15 (get), EP-16 (save) |
| SCR-SLN-04: Các cài đặt khác | EP-35~40 (free time/remind), EP-37~38 (limit booking), EP-49~52 (info/policy/word), EP-55~56 (notify full), EP-43~44 (delete auth) |
| SCR-SLN-05: 決済連携 | EP-17 (init), EP-18 (save) |
