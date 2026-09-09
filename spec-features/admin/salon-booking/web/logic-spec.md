# FA-020 — Đặt lịch salon (「サロン・面談予約」) — Logic Spec

> Tạo bởi: web-analyzer agent | Ngày: 2026-06-04 | Confidence tổng thể: Cao

---

## 1. Controllers

### 1.1 `App\Http\Controllers\Basic\CalendarSalonController`

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php`
**Số dòng:** 4308
**Namespace:** `App\Http\Controllers\Basic`

**Services được inject qua constructor (dòng 94–124):**
| Service | Biến | Mô tả |
|---------|------|-------|
| `BotSlotService` | `$botSlotService` | Kiểm tra slot/bot |
| `BotService` | `$botService` | Lấy thông tin bot |
| `CalendarSalonService` | `$calendarSalonService` | Business logic calendar |
| `CalendarSalonCourseService` | `$calendarSalonCourseService` | Business logic khóa học |
| `CalendarSalonLineBookingService` | `$calendarSalonLineBookingService` | Business logic đặt lịch |
| `CalendarSalonStaffService` | `$calendarSalonStaffService` | Business logic nhân viên |
| `CalendarSalonSettingSendFormService` | `$calendarSalonSettingSendFormService` | Form booking settings |
| `CalendarSalonSettingMessageService` | `$calendarSalonSettingMessageService` | Message settings |
| `CalendarSalonSettingTimeFreeService` | `$calendarSalonSettingTimeFreeService` | Free time settings |
| `CalendarSalonTimeBookingService` | `$calendarSalonTimeBookingService` | Shift management |
| `CalendarSalonSettingLimitBookingService` | `$calendarSalonSettingLimitBookingService` | Booking limit settings |
| `BCSalonGoogleCalendarHistoryService` | `$salonGoogleCalendarHistoryService` | Google calendar history |
| `CalendarSalonGoogleCalendarService` | `$googleCalendarService` | Google calendar sync |
| `CalendarSalonBookingByGoogleService` | `$calendarSalonBookingByGoogleService` | Booking from Google |

---

### 1.2 `App\Http\Controllers\Basic\SettingPaymentCalendarSalonController`

**File:** `app/Http/Controllers/Basic/SettingPaymentCalendarSalonController.php`
**Số dòng:** 216
**Namespace:** `App\Http\Controllers\Basic`

**Models sử dụng trực tiếp:**
- `CalendarSalon` — đọc/ghi cài đặt thanh toán
- `StripBot` — kiểm tra liên kết Stripe/UnivaPay
- `CalendarSalonHistoryChangeSettingPayment` — ghi lịch sử thay đổi
- `CalendarSalonSettingSendForms` — cập nhật trường name/email bắt buộc
- `BotContracts` — kiểm tra contract type

---

## 2. Services

### 2.1 `CalendarSalonService`

**File:** `app/Services/CalendarSalon/CalendarSalonService.php` (1531 dòng)

**Kiểm tra giới hạn tạo calendar — `checkMaxCalendarMayBeCreate()` (dòng 109):**

Logic kiểm tra theo plan:
- **free / plan_type=2**: Tối đa 2 calendars (1 cá nhân + 1 staff, hoặc 2 cùng loại)
- **standard/enterprise mới (flag_contract_new=1)**: Tối đa 3 cá nhân + 3 staff = 6 tổng
- **standard cũ / pro / enterprise_pro**: Tối đa 10 cá nhân + 10 staff = 20 tổng

**Tạo calendar mới — `createNewCalendarSalon()` (dòng 185):**
1. Kiểm tra giới hạn plan (xem bảng trên)
2. Xác định `calendar_staff_type` tự động dựa trên plan và số lượng hiện tại
3. Tạo `CalendarSalon` record với các giá trị mặc định:
   - `enable_use_calendar = 1` (有効)
   - `use_course = 1`, `display_course_cost = 1`, `display_time_make_course = 1`
   - `time_make_course = '01:00'`
   - `store_name = calendar_name`
4. Tạo `CalendarSalonSettingTimeFree` record mặc định (không có giới hạn thời gian)

**Giới hạn plan cho course/staff (dòng 419–452, 1175–1267):**
- free/plan_type=2: tối đa 2 courses per calendar, 2 staffs per calendar
- Tất cả plans: tối đa 200 courses/calendar, 200 staffs/calendar

**Xem trang detail — `detailCalendar()` (dòng 558):**
1. Kiểm tra calendar thuộc bot hiện tại (`checkCalendarBelongBot()`)
2. Nếu là loại 個人 (CALENDAR_ONE_STAFF_TYPE) và chưa có staff → tự động tạo staff mặc định tên 「運営者」 với template tin nhắn mặc định (dòng 566–594)
3. Tự động khởi tạo setting message mặc định nếu chưa có (`createSettingMessageDefault()`)
4. Tự động khởi tạo setting form mặc định nếu chưa có (`createSettingFormDefault()`)
5. Tự động khởi tạo setting limit booking mặc định nếu chưa có (`createSettingLimitDefault()`)
6. Chuẩn bị URL xác thực Google Sheet nếu chưa liên kết hoặc bị lỗi

---

### 2.2 `CalendarSalonLineBookingService`

**File:** `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` (5669 dòng)

**Trạng thái booking (constants từ `CalendarSalonLineBooking`):**
| Constant | Giá trị | Ý nghĩa JP |
|----------|---------|-----------|
| `SB_REQUEST_BOOKING` | 0 | 予約リクエスト中 |
| `SB_BOOKING_APPROVE` | 1 | 予約確定 |
| `SB_BOOKING_ADMIN_BOOK` | 2 | 予約確定 (Admin thêm) |
| `SB_REQUEST_BOOKING_WAIT_CANCEL` | 3 | キャンセルリクエスト中 |
| `SB_BOOKING_CANCEL` | 4 | キャンセル |
| `SB_REQUEST_BOOKING_CANCEL` | 5 | キャンセルリクエスト中 |
| `SB_BOOKING_DENY` | 6 | 否認 |
| `SB_BOOKING_ADMIN_CANCEL` | 7 | キャンセル (Admin) |

**Trạng thái thanh toán (constants):**
| Constant | Giá trị | Ý nghĩa JP |
|----------|---------|-----------|
| `SP_NOT_PAYMENT` | 0 | 未決済 |
| `SP_PAYMENT` | 1 | 決済成功 |
| `SP_NO_PAYMENT` | 2 | 決済なし |
| `SP_REFUND` | 3 | 返金済み |

**Logic `getListBooking()` (dòng 129):**
1. Lấy danh sách booking với filter + pagination
2. Xử lý format ngày giờ: `Y.m.d`, `H:i`
3. Map status → text tiếng Nhật
4. Xác định tên staff: nếu loại MANY_STAFF và có staff_id → hiển thị `staff_system_name`, nếu không → 「指定なし」; nếu loại ONE_STAFF → 「運営者」
5. Xác định `nextDay = true` khi `end_time < start_time` (booking qua ngày)

**Jobs được dispatch từ service này:**
- `CalendarSalonStaffAssignment` (dòng 5069) — phân công staff tự động (dispatch với `onConnection('database').onQueue('default')`)
- `CalendarSalonStaffAssignmentAdmin` (dòng 3977) — phân công staff cho Admin booking
- `HandleWebhookUnivapay` (dòng 5572) — xử lý webhook thanh toán UnivaPay

---

### 2.3 Services khác

| Service | File | Mô tả chính |
|---------|------|-------------|
| `CalendarSalonCourseService` | `app/Services/CalendarSalon/CalendarSalonCourseService.php` | CRUD khóa học, upload ảnh, action settings |
| `CalendarSalonStaffService` | `app/Services/CalendarSalon/CalendarSalonStaffService.php` | CRUD nhân viên, upload ảnh, shift management, CSV |
| `CalendarSalonTimeBookingService` | `app/Services/CalendarSalon/CalendarSalonTimeBookingService.php` | Quản lý ca làm việc (シフト) |
| `CalendarSalonSettingMessageService` | `app/Services/CalendarSalon/CalendarSalonSettingMessageService.php` | Cài đặt tin nhắn booking/cancel |
| `CalendarSalonSettingSendFormService` | `app/Services/CalendarSalon/CalendarSalonSettingSendFormService.php` | Quản lý form hỏi khách khi đặt lịch |
| `CalendarSalonSettingTimeFreeService` | `app/Services/CalendarSalon/CalendarSalonSettingTimeFreeService.php` | Cài đặt thời gian trống trước/sau + mùa vụ |
| `CalendarSalonSettingLimitBookingService` | `app/Services/CalendarSalon/CalendarSalonSettingLimitBookingService.php` | Giới hạn số lượng đặt lịch |
| `CalendarSalonGoogleCalendarService` | `app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php` | Tích hợp Google Calendar |
| `CalendarSalonGoogleSheetService` | `app/Services/CalendarSalon/CalendarSalonGoogleSheetService.php` | Tích hợp Google Spreadsheet |
| `CalendarSalonBookingByGoogleService` | `app/Services/CalendarSalon/CalendarSalonBookingByGoogleService.php` | Đồng bộ booking từ Google Calendar |

---

## 3. Models Eloquent

### 3.1 `CalendarSalon`

**File:** `app/CalendarSalon.php`
**Table:** `calendar_salon`
**SoftDeletes:** Không

**Constants:**
| Constant | Giá trị | Mô tả |
|----------|---------|-------|
| `CALENDAR_ALL_STAFF_TYPE` | 0 | Loại all (không dùng?) |
| `CALENDAR_ONE_STAFF_TYPE` | 1 | 個人 — không có staff list |
| `CALENDAR_MANY_STAFF_TYPE` | 2 | スタッフ — có nhiều nhân viên |
| `ENABLE_NOT_USE_CALENDAR` | 0 | 無効 |
| `ENABLE_USE_CALENDAR` | 1 | 有効 |
| `USE_COURSE` | 1 | Dùng chọn khóa học |
| `NOT_USE_COURSE` | 0 | Không dùng chọn khóa học |
| `DISPLAY_COURSE_COST` | 1 | Hiển thị giá |
| `NOT_DISPLAY_COURSE_COST` | 0 | Ẩn giá |
| `DISPLAY_TIME_MAKE_COURSE` | 1 | Hiển thị thời gian |
| `NOT_DISPLAY_TIME_MAKE_COURSE` | 0 | Ẩn thời gian |
| `SETTING_DISPLAY_LINE_NAME_SYSTEM_NAME` | 1 | Hiển thị LINE名/システム表示名 |
| `SETTING_DISPLAY_SYSTEM_NAME_LINE_NAME` | 2 | Hiển thị システム表示名/LINE名 |
| `SETTING_DISPLAY_LINE_NAME_ONLY` | 3 | Chỉ LINE名 |
| `SETTING_DISPLAY_SYSTEM_NAME_ONLY` | 4 | Chỉ システム表示名 |

**Relationships:**
- `calendarSalonStaffs()` → `hasMany(CalendarSalonStaff::class, 'calendar_salon_id')`

**Các cột quan trọng (suy luận từ code):**
- `id`, `bot_id`, `calendar_name`, `manager_name`, `store_name`
- `calendar_staff_type` (0/1/2)
- `enable_use_calendar` (0/1)
- `use_course`, `display_course_cost`, `display_time_make_course`
- `time_make_course` (string, format "HH:MM")
- `holidays` (JSON)
- `order` (int — thứ tự sắp xếp)
- `is_use_payment` (0/1)
- `type_payment` (1=Stripe, 2=UnivaPay)
- `environment` (1=本番, 2=テスト)
- `description_payment` (text — 特定商取引法)
- `payment_time` (int)
- `google_sheet_id`, `google_sheet_access_token`, `google_sheet_status`, `google_sheet_name`
- `google_account_name`, `google_account_picture`
- `datetime_connect_google_sheet`
- `code_delete` (string — mã xác thực xóa)
- `filter_calendar_salon_ids`, `number_filter_salon`
- `message_outside_filter`
- `is_notify_full_slot`, `use_message_notify_full_slot`, `message_notify_full_slot`
- `action_id_notify_full_slot`, `action_id_not_full`
- `show_policy`, `content_policy`
- `image_calendar`, `image_calendar_top`, `description`, `description_top`
- `booking_setting_name`, `booking_setting_text_fee`, `booking_setting_text_staff`
- `is_show_month`, `show_top_page`
- `setting_display_line_name` (1-4)
- `setting_time_unit`
- `liff_id` (liên kết LIFF)

---

### 3.2 `CalendarSalonLineBooking`

**File:** `app/CalendarSalonLineBooking.php`
**Table:** `calendar_salon_line_booking`
**SoftDeletes:** Có (trait `SoftDeletes`)

**Relationships:**
- `course()` → `belongsTo(CalendarSalonCourse::class, 'course_id', 'id')`
- `staff()` → `belongsTo(CalendarSalonStaff::class, 'staff_id', 'id')`
- `lineUser()` → `belongsTo(LineUser::class, 'line_user_id', 'id')`

**Mutators:**
- `getFriendInfoAttribute($value)` — giải mã JSON từ cột `friend_info`
- `getPaymentAmountAttribute($value)` — format số với `number_format()`

**Các cột quan trọng (suy luận từ code):**
- `id`, `calendar_salon_id`, `bot_id`, `line_user_id`
- `staff_id`, `course_id`
- `date_booking` (date), `end_date_booking` (date — cho booking qua ngày)
- `start_time` (time), `end_time` (time)
- `status` (0-7, xem constants trên)
- `payment_status` (0-3)
- `payment_amount` (int)
- `friend_info` (JSON — thông tin điền khi đặt)
- `received_booking_date`, `user_update_time`

---

### 3.3 `CalendarSalonCourse`

**File:** `app/CalendarSalonCourse.php`
**Table:** `calendar_salon_course`
**SoftDeletes:** Có

**Constants:**
- `BOOKING_PAGE_DISPLAY = 1` — Hiển thị trên trang đặt lịch
- `BOOKING_PAGE_NOT_DISPLAY = 0` — Ẩn khỏi trang đặt lịch

**Mutators:** Format `hour_done` và `minute_done` với zero-padding (2 chữ số)

**Relationships:**
- `filters()` → `hasMany(FilterV2::class, 'parent_id', 'id')`

**Cột quan trọng:** `calendar_salon_id`, `bot_id`, `course_name`, `system_name`, `hour_done`, `minute_done`, `amount`, `course_image`, `course_description`, `booking_page_display`, `course_order`, `course_menu_id`, `use_message_notify_send_after_booking`, `use_message_notify_send_approve_booking`, `message_send_after_booking`, `message_send_approve_booking`, `action_id_send_after_booking`, `action_id_send_approve_booking`, `filter_id`, `filter_number`

---

### 3.4 `CalendarSalonStaff`

**File:** `app/CalendarSalonStaff.php`
**Table:** `calendar_salon_staff`
**SoftDeletes:** Có

**Constants:**
- `BOOKING_PAGE_DISPLAY = 1`
- `IS_All_COURSE = 1` — Nhận tất cả khóa học

**Relationships:**
- `calendarSalonLineBooking()` → `hasMany(CalendarSalonLineBooking::class, 'staff_id', 'id')`
- `shifts()` → `hasMany(CalendarSalonTimeBooking::class, 'staff_id', 'id')`
- `filters()` → `hasMany(FilterV2::class, 'parent_id', 'id')`

**Cột quan trọng:** `calendar_salon_id`, `bot_id`, `staff_name`, `staff_system_name`, `staff_image`, `staff_bill`, `hour_done`, `minute_done`, `order`, `booking_page_display`, `use_message_notify_send_after_booking`, `use_message_notify_send_approve_booking`, `message_send_after_booking`, `message_send_approve_booking`, `action_id_send_after_booking`, `action_id_send_approve_booking`, `filter_id`, `filter_number`, `is_all_course`, `course_ids`, `setting_staff_limit`, `limited_quantity`

---

### 3.5 Các Models phụ

| Model | Table | Mô tả |
|-------|-------|-------|
| `CalendarSalonCourseMenu` | `calendar_salon_course_menu` | Nhóm menu khóa học |
| `CalendarSalonSettingSendMessage` | `calendar_salon_setting_send_message` | Cài đặt tin nhắn booking/cancel |
| `CalendarSalonSettingSendForms` | `calendar_salon_setting_send_forms` | Form hỏi thông tin khi đặt lịch |
| `CalendarSalonSettingTimeFree` | `calendar_salon_setting_time_free` | Thời gian trống trước/sau + mùa vụ |
| `CalendarSalonSettingLimitBooking` | `calendar_salon_setting_limit_booking` | Giới hạn số lượng booking |
| `CalendarSalonTimeBooking` | `calendar_salon_time_booking` | Ca làm việc (シフト) |
| `CalendarSalonHistoryChangeSettingPayment` | `calendar_salon_history_change_setting_payment` | Lịch sử thay đổi cài đặt thanh toán |
| `CalendarSalonLineBookingHistoryAction` | `calendar_salon_line_booking_history_action` | Lịch sử action trên booking |
| `CalendarSalonSettingNotifyFullHistory` | `calendar_salon_setting_notify_full_history` | Lịch sử thay đổi cài đặt thông báo đầy slot |
| `CalendarSalonSyncBookingGoogleCalendarHistory` | `calendar_salon_sync_booking_google_calendar_history` | Lịch sử sync Google Calendar |
| `BCSalonGoogleCalendar` | `bc_salon_google_calendar` | Cấu hình liên kết Google Calendar cho staff |

---

## 4. Business Rules

### BR-01: Giới hạn số lượng calendar theo plan

**File:** `app/Services/CalendarSalon/CalendarSalonService.php` (dòng 109–135)

| Plan | Loại calendar | Giới hạn |
|------|---------------|---------|
| free / plan_type=2 | 個人 + スタッフ tổng cộng | 2 calendars (bất kỳ loại, tối đa 1 mỗi loại) |
| standard/enterprise (flag_contract_new=1) | 個人 | 3 |
| standard/enterprise (flag_contract_new=1) | スタッフ | 3 |
| standard cũ / pro / enterprise_pro | 個人 | 10 |
| standard cũ / pro / enterprise_pro | スタッフ | 10 |

Khi vượt giới hạn → trả về message: 「現在のプランは利用できない機能です。アップグレードが必要になります。」

---

### BR-02: Giới hạn course/staff theo plan

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 419–452, 1175–1267)

- **free / plan_type=2:** Tối đa 2 courses, 2 staffs per calendar
- **Tất cả plans:** Tối đa 200 courses, 200 staffs per calendar (hard limit)
- Giới hạn form questions: 100 questions per calendar (dòng 1578)

---

### BR-03: Tự động tạo staff mặc định cho loại 個人

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 564–594)

Khi truy cập trang detail của calendar loại 個人 (`CALENDAR_ONE_STAFF_TYPE`) mà chưa có staff → tự động tạo staff tên 「運営者」 với template tin nhắn đặt lịch và xác nhận mặc định bằng tiếng Nhật.

**Confidence:** Cao

---

### BR-04: Tự động khởi tạo settings khi lần đầu truy cập

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 597–599)

Khi truy cập trang detail lần đầu:
- `createSettingMessageDefault()` — tạo setting message booking/cancel mặc định
- `createSettingFormDefault()` — tạo form hỏi thông tin mặc định (tên, email)
- `createSettingLimitDefault()` — tạo setting giới hạn booking mặc định

**Confidence:** Cao

---

### BR-05: Điều kiện bật thanh toán

**File:** `app/Http/Controllers/Basic/SettingPaymentCalendarSalonController.php` (dòng 83–95)

Để bật thanh toán, cần:
1. Đã liên kết Stripe hoặc UnivaPay (kiểm tra qua `StripBot` record)
2. Form booking phải có trường tên (`friend_information_id=-1`) và email (`friend_information_id=-3`) đều bật và bắt buộc

Khi bật thanh toán → tự động bắt buộc enable 2 trường name và email trong `calendar_salon_setting_send_forms` (dòng 190–210).

**Confidence:** Cao

---

### BR-06: Logic lịch sử thay đổi trạng thái thanh toán

**File:** `app/Http/Controllers/Basic/SettingPaymentCalendarSalonController.php` (dòng 109–151)

Ghi lịch sử khi:
- Bật từ tắt → ghi `from=停止, to=本番環境/テスト環境`
- Tắt từ bật → ghi `from=本番/テスト, to=停止`
- Thay đổi môi trường → ghi sự thay đổi môi trường

Status constants của `CalendarSalonHistoryChangeSettingPayment`:
- `STATUS_STOPED` — 停止
- `STATUS_PRODUCTION` — 本番環境
- `STATUS_TEST` — テスト環境
- `STATUS_USING_PRODUCTION` — 利用中(本番環境)
- `STATUS_USING_TEST` — 利用中(テスト環境)

**Confidence:** Cao

---

### BR-07: Xóa calendar — quy trình 2 bước xác thực qua email

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 2790–2949)

Quy trình:
1. **Bước 1:** `sendMailCodeAuthDeleteCalendar()` — Gửi email chứa mã xác thực 10 ký tự ngẫu nhiên, lưu mã vào `calendar_salon.code_delete`
2. **Bước 2:** `checkAuthorDeleteCalendar()` — Xác nhận mã
3. **Bước 3:** `deleteCalendarSalon()` — Xóa cascade sau khi xác nhận mã đúng

**Cascade delete bao gồm (dòng 2979–3017):**
- `CalendarSalon` (soft delete)
- `CalendarSalonBookingByGoogle`
- `CalendarSalonCourse` (force delete)
- `CalendarSalonCourseMenu` (force delete)
- `CalendarSalonHistoryChangeSettingPayment`
- `CalendarSalonLineBooking` (force delete) + `CalendarSalonLineBookingHistoryAction`
- `BCSalonGoogleCalendar`, `BCSalonGoogleCalendarHistory`
- `CalendarSalonDownloadCsvSyncGoogleCalendar`
- `CalendarSalonSettingLimitBooking`, `CalendarSalonSettingNotifyFullHistory`
- `CalendarSalonSettingSendForms` (force delete), `CalendarSalonSettingSendMessage` (force delete)
- `CalendarSalonSettingTimeFree`, `CalendarSalonStaff` (force delete)
- `CalendarSalonTimeBooking`
- `Events` (type=5) + `EventStep` + `EventStepTime` — xóa remind events liên quan
- Xóa Google Calendar events (gọi `googleCalendarService->deleteEventByBookingId()`)
- Xóa `MobileNotify` liên quan
- Cập nhật `count_app_notify` trên Bot

**Confidence:** Cao

---

### BR-08: Reminder message — Logic tính thời gian gửi

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 2010–2141)

Hàm `addActionRemindNew()` được gọi sau khi lưu remind setting để tạo `EventStepTime` (lịch gửi) cho từng booking hiện tại.

Hai loại remind:
1. **type_remind=1 (Ngày trước/sau):** Tính ngày gửi = ngày đặt lịch ± số ngày, giờ gửi = `time_send`
2. **type_remind=2 (Đếm ngược):** Tính giờ gửi = giờ bắt đầu/kết thúc booking ± số giờ/phút

Filter remind theo course_ids và staff_ids nếu `is_use_filter` được bật.

**Confidence:** Cao

---

### BR-09: Google Calendar liên kết với nhân viên

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 3040–3059)

Khi liên kết Google Calendar cho staff (`changeGoogleLinkForStaff()`):
- Cập nhật liên kết Google Calendar qua service
- Dispatch Job `CalendarSalonSyncBookingFromGoogleToTool` để đồng bộ booking từ Google sang hệ thống

Khi ngắt liên kết hoặc ẩn staff khỏi booking page:
- Xóa booking được đồng bộ từ Google
- Xóa `BCSalonGoogleCalendar` records

**Confidence:** Cao

---

### BR-10: Toggle hiển thị nhân viên trên trang booking

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 1138–1166)

Khi `updateBookingPageDisplayStaff()` với `status=0` (ẩn):
- Xóa toàn bộ booking sync từ Google cho staff đó
- Xóa `BCSalonGoogleCalendar` record cho staff đó

**Confidence:** Cao

---

### BR-11: Xác nhận xóa course menu — kiểm tra booking active

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 879–901)

Trước khi xóa course menu, kiểm tra có booking chưa cancel trong các course thuộc menu đó không. Nếu có → không cho xóa, hiển thị thông báo lỗi.

**Confidence:** Cao

---

### BR-12: Xóa shift — kiểm tra booking active

**File:** `app/Http/Controllers/Basic/CalendarSalonController.php` (dòng 3438–3455)

Không thể xóa shift nếu còn booking có status 「予約確定」 trong timeline của shift đó.
Error message: 「削除するシフトの中に「ステータス：予約確定」の予約が1つ以上残っています。シフトを削除する場合、選択したシフトに対する全ての予約が「ステータス：キャンセル」になっている必要があります。」

**Confidence:** Cao

---

## 5. Background Jobs (Queue)

> **Ghi chú cho job-analyzer:** Tính năng này có background jobs quan trọng.

| Job | File | Dispatch tại | Mô tả |
|-----|------|-------------|-------|
| `CalendarSalonSyncBookingFromGoogleToTool` | `app/Jobs/CalendarSalonSyncBookingFromGoogleToTool.php` | `CalendarSalonController@changeGoogleLinkForStaff` (dòng 3051) | Đồng bộ booking từ Google Calendar vào hệ thống khi liên kết Google |
| `CalendarSalonSyncBookingGoogle` | `app/Jobs/CalendarSalonSyncBookingGoogle.php` | Không rõ từ web controller (có thể từ Mobile hoặc Spring Boot) | Đồng bộ ngược booking sang Google Calendar |
| `CalendarSalonStaffAssignment` | `app/Jobs/CalendarSalonStaffAssignment.php` | `CalendarSalonLineBookingService` (dòng 5069), queue `default` | Phân công staff tự động cho booking của LINE User |
| `CalendarSalonStaffAssignmentAdmin` | `app/Jobs/CalendarSalonStaffAssignmentAdmin.php` | `CalendarSalonLineBookingService` (dòng 3977), queue `default` | Phân công staff cho booking Admin tạo |
| `HandleWebhookUnivapay` | `app/Jobs/HandleWebhookUnivapay.php` | `CalendarSalonLineBookingService` (dòng 5572) | Xử lý webhook thanh toán UnivaPay |

**Tất cả jobs dùng:** `onConnection('database').onQueue('default')` — queue trong database, không phải Redis.

---

## 6. Tích hợp ngoài (Third-party Integrations)

### 6.1 Stripe

**Helper class:** `App\Helpers\StripePayment`
**Điều kiện:** `StripBot` record với `status_strip_bot == 3` → đã kết nối Stripe
**Cài đặt:** `type_payment=1`, `environment=1/2` (本番/テスト)

### 6.2 UnivaPay

**Helper class:** `App\Helpers\UnivapayPayment`
**Điều kiện:** `StripBot` record với `univapay_app_id` và `univapay_app_test_id` → đã kết nối UnivaPay
**Webhook xử lý:** Job `HandleWebhookUnivapay`

### 6.3 Google Sheet

**Service:** `App\Helpers\GoogleSheetService`
**OAuth Flow:** Admin authorize → callback `/basic/calendar-salon/redirect-google-sheet` → lưu `google_sheet_access_token` + `google_sheet_id`
**Scope:** `SPREADSHEETS` + `USERINFO_PROFILE`
**Ghi sheet mỗi khi:** Booking mới, thay đổi trạng thái (suy luận — cần xác nhận từ Spring Boot job)

### 6.4 Google Calendar

**Service:** `App\Services\CalendarSalon\CalendarSalonGoogleCalendarService`
**OAuth Flow:** Redirect đến `/basic/calendar-salon/oauth/{bot_id}/{calendar_id}/{staff_id}` → `gCalendarController@oauthCalendarSalon`
**Sync:** Booking từ Google → hệ thống (Job `CalendarSalonSyncBookingFromGoogleToTool`)
**Liên kết per-staff:** Mỗi staff có thể liên kết Google Calendar riêng (`BCSalonGoogleCalendar` table)
**Xác thực title display:** Quy trình 2 bước qua email để thay đổi tiêu đề hiển thị (`sendMailCodeAuthGoogleSync` → `checkAuthorGoogleSync`)

---

## 7. Điểm cần điều tra tiếp (cho job-analyzer)

1. **`CalendarSalonSyncBookingGoogle` job** — có trong imports nhưng không thấy dispatch từ web controller. Có thể được dispatch từ Spring Boot hoặc cron job.
2. **Ghi Google Sheet tự động** — Khi nào dữ liệu được đẩy vào Sheet? Cần xem Spring Boot job `CalendarSalonGoogleSheetService`.
3. **Gửi tin nhắn remind** — `EventStepTime` records được tạo bởi web controller, nhưng việc gửi thực sự được thực hiện bởi Spring Boot scheduler.
4. **Gửi tin nhắn sau đặt lịch** — `message_send_after_booking` được lưu trên `CalendarSalonCourse`/`CalendarSalonStaff`, nhưng trigger gửi có thể từ Spring Boot.
5. **Action execution** — Các `action_id_*` fields được lưu nhưng việc thực thi action cần Spring Boot hoặc queue job riêng.
