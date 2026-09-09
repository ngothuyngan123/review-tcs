# FA-019 「レッスン予約」 — API Spec: Portal Admin

> Tạo bởi: **web-analyzer** agent | Phương pháp: **code-first** (đọc trực tiếp routes + controller + middleware + FormRequest)
> Phạm vi: `Basic\CalendarManagementController` (2598 dòng) và `Basic\SettingPaymentCalendarController` (213 dòng) — backend của **portal Admin/Staff**.
> **Không** bao gồm `Mobile\CalendarController` và `Api\CalendarLessonController` — xem `api-spec-public.md` (mã `EP-P*` / `EP-M*`).
> Root source: `src/web/sns-line/`. Mọi khẳng định truy vết `file.php:dòng`.
> Confidence tổng thể: **Cao**.

---

## 0. Bối cảnh route & prefix

Có **hai nhóm route riêng biệt** cùng phục vụ FA-019 phía Admin, với **hai bộ middleware khác nhau**:

| Nhóm | Prefix URL | Middleware chồng lên | Vị trí | Số endpoint |
|---|---|---|---|---|
| **Nhóm A** — quản lý lịch/khoá học/đặt chỗ | `/basic/calendar-management/…` (+2 route `/basic/calendar/…`) | `NotifyChatworkRequestTimeSlow` → `LogRequestMultipart` → `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` (+ `checkLessonCalendarInBot` cho nhóm con) | `routes/web.php:81`, `:835`, `:882`, `:1484`, `:1532` | 65 (EP-01…EP-65) |
| **Nhóm B** — cấu hình toàn cục & remind | `/ajax/calendar/…` | `NotifyChatworkRequestTimeSlow` → `LogRequestMultipart` → **`check_login`, `check_remember_token`** | `routes/web.php:81`, `:835`, `:2485`, `:3522` | 17 (EP-66…EP-82) |

> 🔴 **Phát hiện then chốt**: Nhóm B **KHÔNG có `basic_access`** (không kiểm tra vai trò/quyền bot mời), **KHÔNG có `is_expire`** (không chặn hợp đồng hết hạn), và nằm trong pattern `'/ajax/*'` của `VerifyCsrfToken::$except` ⇒ **không CSRF**. Nhóm B chính là nơi chứa các thao tác nguy hiểm nhất: **xoá hệ thống đặt lịch** (EP-71), lưu 「利用規約」/「店舗情報」 (EP-67, EP-68), cấu hình remind (EP-74). Bằng chứng: `routes/web.php:2485`, `app/Http/Middleware/VerifyCsrfToken.php:16`.

Đối chiếu với `api-spec-public.md` §0: phần LIFF cũng lợi dụng cùng miễn trừ CSRF `'/ajax/*'` — đây là **cùng một gốc rễ**, ảnh hưởng cả hai phía.

---

## 1. Bảng tổng hợp endpoint

Ký hiệu middleware: **BA** = `basic_access`, **EXP** = `is_expire`, **RT** = `check_remember_token`, **HP** = `https_protocol` (no-op), **CLC** = `checkLessonCalendarInBot`, **CL** = `check_login`.

### 1.1 Nhóm A — `/basic/calendar-management` (và 2 route `/basic/calendar`)

| Mã | Method | URL | Mô tả | Controller@method | Middleware | Màn hình |
|---|---|---|---|---|---|---|
| EP-01 | GET | `/basic/calendar/redirect-google-sheet` | Callback OAuth Google Sheets — lưu token | `CalendarManagementController@redirectUriGoogleSheet` :580 | BA, HP, EXP, RT | SCR-LSN-21 |
| EP-02 | GET | `/basic/calendar/cancel-google-sheet/{id}` | Ngắt liên kết Google Sheets | `@cancelGoogsheet` :628 | BA, HP, EXP, RT | SCR-LSN-21 |
| EP-03 | GET | `/{calendar_id}/get-list-booking` | Danh sách đặt chỗ của lịch | `@getListBooking` :1877 | BA, HP, EXP, RT | SCR-LSN-05 |
| EP-04 | GET | `/api/{calendarId}/get-list-courses` | Danh sách khoá học (perpage 100000) | `@listsCourse` :1491 | BA, HP, EXP, RT | SCR-LSN-08 |
| EP-05 | POST | `/api/course/update-booking-page-display` | Bật/tắt hiển thị khoá học trên trang đặt | `@updateBookingPageDisplay` :1509 | BA, HP, EXP, RT | SCR-LSN-08 |
| EP-06 | POST | `/api/course/sortable` | Sắp xếp thứ tự khoá học | `@updateCalendarCourseOrder` :1709 | BA, HP, EXP, RT | SCR-LSN-08 |
| EP-07 | POST | `/api/{calendarId}/course/create` | Tạo khoá học | `@createCourse` :1536 | BA, HP, EXP, RT | SCR-LSN-09 |
| EP-08 | GET | `/api/course/{id}/edit` | Chi tiết khoá học (JSON) | `@course` :1474 | BA, HP, EXP, RT | SCR-LSN-09 |
| EP-09 | GET | `/api/course/{id}/get-message-notify` | Tin nhắn thông báo của khoá học | `@getMessageNotify` :1809 | BA, HP, EXP, RT | SCR-LSN-09 |
| EP-10 | POST | `/api/course/{id}/update` | Cập nhật khoá học | `@updateCourse` :1610 | BA, HP, EXP, RT | SCR-LSN-09 |
| EP-11 | POST | `/api/course/{id}/image/delete` | Xoá ảnh khoá học | `@deleteImageCalendarCourse` :1686 | BA, HP, EXP, RT | SCR-LSN-09 |
| EP-12 | GET | `/api/course/{id}/init-data-action` | Dữ liệu khởi tạo modal action sau đặt chỗ | `@initDataActionCalendarCourseSetting` :1733 | BA, HP, EXP, RT | SCR-LSN-09 |
| EP-13 | POST | `/api/course/delete-action` | Xoá 1 item action của khoá học | `@deleteItemAction` :1756 | BA, HP, EXP, RT | SCR-LSN-09 |
| EP-14 | GET | `/api/course/{id}/init-data-filter` | Dữ liệu filter bạn bè của khoá học | `@initDataFilter` :1787 | BA, HP, EXP, RT | SCR-LSN-09 |
| EP-15 | POST | `/api/course/{id}/delete` | Xoá khoá học | `@deleteCalendarCourse` :1663 | BA, HP, EXP, RT | SCR-LSN-08 |
| EP-16 | POST | `/api/course/{id}/check-booking-cancel` | Kiểm tra còn đặt chỗ chưa huỷ trước khi xoá | `@checkBookingCancel` :2241 | BA, HP, EXP, RT | SCR-LSN-08 |
| EP-17 | GET | `/{id}/init-data-filter` | Dữ liệu filter hiển thị trang đặt | `@initDataFilterShowBooking` :1799 | BA, HP, EXP, RT | SCR-LSN-17 |
| EP-18 | GET | `/{calendarId}/get-booking-setting-display` | Đọc cấu hình hiển thị trang đặt | `@getDataBookingSettingDisplay` :1826 | BA, HP, EXP, RT | SCR-LSN-17 |
| EP-19 | POST | `/{calendarId}/setting-booking-display` | Lưu cấu hình hiển thị trang đặt | `@settingBookingDisplay` :1844 | BA, HP, EXP, RT | SCR-LSN-17 |
| EP-20 | POST | `/save-setting-payment` | Lưu cấu hình thanh toán | `SettingPaymentCalendarController@saveSettingPayment` | BA, HP, EXP, RT | SCR-LSN-23 |
| EP-21 | GET | `/init-data-setting-payment` | Khởi tạo dữ liệu cấu hình thanh toán | `SettingPaymentCalendarController@initDataSettingPayment` | BA, HP, EXP, RT | SCR-LSN-23 |
| EP-22 | GET | `/get-data-friend-info` | Danh sách trường hồ sơ bạn bè (cho form) | `@getDataFriendInfo` :2281 | BA, HP, EXP, RT | SCR-LSN-16 |
| EP-23 | GET | `/get-category-id-of-friend-setting` | Category của trường hồ sơ bạn bè | `@getCategoryOfFriendSetting` :2442 | BA, HP, EXP, RT | SCR-LSN-16 |
| EP-24 | POST | `/order-refund` | Hoàn tiền đặt chỗ | `@orderRefund` :2007 | BA, HP, EXP, RT | SCR-LSN-05 (modal 返金確認) |
| EP-25 | GET | `/` | Màn danh sách lịch (view) | `@index` :97 | BA, HP, EXP, RT | SCR-LSN-01 |
| EP-26 | GET | `/get-list-calendar` | Dữ liệu danh sách lịch (JSON) | `@getListCalendar` :106 | BA, HP, EXP, RT | SCR-LSN-01 |
| EP-27 | GET | `/create` | Màn tạo lịch mới (view) | `@create` :124 | BA, HP, EXP, RT | SCR-LSN-02 |
| EP-28 | POST | `/store` | Tạo lịch mới | `@storeCalendar` :129 | BA, HP, EXP, RT | SCR-LSN-02 |
| EP-29 | POST | `/{id}/edit` | Sửa thông tin lịch | `@editCalendar` :154 | BA, HP, EXP, RT | SCR-LSN-01 |
| EP-30 | POST | `/sort` | Sắp xếp thứ tự lịch | `@saveSort` :186 | BA, HP, EXP, RT | SCR-LSN-01 |
| EP-31 | GET | `/course/create` | Màn đăng ký khoá học đầu tiên (view) | `@courseCreate` :165 | BA, HP, EXP, RT | SCR-LSN-03 |
| EP-32 | POST | `/course/store` | Lưu khoá học đầu tiên | `@storeCourse` :175 | BA, HP, EXP, RT | SCR-LSN-03 |
| EP-33 | GET | `/{id}` | Màn chi tiết lịch (view, khung tab) | `@detailCalendar` :197 | BA, HP, EXP, RT, **CLC** | SCR-LSN-04 |
| EP-34 | GET | `/{id}/course/list` | Danh sách khoá học của tab lịch | `@getCourseList` :247 | + CLC | SCR-LSN-06, SCR-LSN-08 |
| EP-35 | POST | `/{id}/course/reception/create` | Tạo khung giờ 「受付枠」 hàng loạt | `@addNewReception` :258 | + CLC | SCR-LSN-06 (modal 受付枠追加) |
| EP-36 | GET | `/{id}/course/reception/{receptionId}` | Chi tiết khung giờ | `@detailReception` :265 | + CLC | modal detail_reception |
| EP-37 | GET | `/{id}/today-booking/reception/{receptionId}` | Chi tiết đặt chỗ theo slot (tab 本日) | `@getDetailBookingBySlot` :2197 | + CLC | SCR-LSN-05 |
| EP-38 | POST | `/{id}/course/booking/create` | Admin đặt chỗ hộ khách | `@addNewBooking` :276 | + CLC | modal add_new_booking |
| EP-39 | GET | `/{id}/course/reception/booking-list` | Danh sách đặt chỗ trong 1 khung giờ | `@getBookingList` :287 | + CLC | modal detail_reception |
| EP-40 | GET | `/{id}/booking-list` | Danh sách đặt chỗ (lọc tuỳ biến) | `@getBookingListDataCustom` :298 | + CLC | SCR-LSN-06 |
| EP-41 | GET | `/{id}/reception/list` | Danh sách khung giờ (lọc tuỳ biến) | `@getReceptionListDataCustom` :309 | + CLC | SCR-LSN-06 |
| EP-42 | POST | `/{id}/booking/change-status` | Đổi trạng thái đặt chỗ | `@changeStatusBooking` :320 | + CLC | SCR-LSN-05 |
| EP-43 | DELETE | `/{id}/booking/delete` | Xoá đặt chỗ | `@deleteBooking` :340 | + CLC | modal delete_booking_cancel |
| EP-44 | GET | `/{id}/booking/{bookingId}/history` | Lịch sử thao tác của 1 đặt chỗ | `@getBookingHistory` :352 | + CLC | modal history_booking_status |
| EP-45 | GET | `/{id}/booking/deleted` | Danh sách đặt chỗ đã xoá | `@getBookingDeleted` :363 | + CLC | SCR-LSN-07 |
| EP-46 | POST | `/{id}/course/reception/update` | Sửa khung giờ | `@updateReception` :374 | + CLC | modal detail_reception |
| EP-47 | DELETE | `/{id}/course/reception/delete` | Xoá 1 khung giờ | `@deleteReception` :385 | + CLC | modal detail_reception |
| EP-48 | GET | `/{id}/edit-course/{courseId}` | Màn sửa khoá học (view) | `@editCourse` :421 | + CLC | SCR-LSN-09 |
| EP-49 | POST | `/{id}/reception/export-csv` | Xuất CSV đặt chỗ **của 1 受付枠** | `@exportCsvReception` :461 | + CLC | modal detail_reception |
| EP-50 | POST | `/{id}/course/export-csv` | Xuất CSV đặt chỗ **theo khoảng ngày × khoá học** | `@exportCsv` :450 | + CLC | modal handle_csv |
| EP-51 | POST | `/{id}/course/import-csv` | Nhập CSV khung giờ | `@importCsv` :472 | + CLC | modal handle_csv |
| EP-52 | GET | `/{id}/setting-message` | Đọc cấu hình tin nhắn đặt/huỷ | `@getSettingMessage` :1375 | + CLC | SCR-LSN-11…13 |
| EP-53 | POST | `/{id}/save-setting-message` | Lưu cấu hình tin nhắn đặt/huỷ | `@saveSettingMessage` :1386 | + CLC | SCR-LSN-12, SCR-LSN-13 |
| EP-54 | GET | `/{id}/setting-form` | Đọc cấu hình form câu hỏi | `@getSettingSendForm` :1397 | + CLC | SCR-LSN-16 |
| EP-55 | POST | `/{id}/create-new-setting-form` | Thêm câu hỏi mới | `@createNewSettingForm` :1408 | + CLC | SCR-LSN-16 |
| EP-56 | POST | `/{id}/update-setting-form` | Cập nhật câu hỏi | `@updateSettingForm` :1427 | + CLC | SCR-LSN-16 |
| EP-57 | DELETE | `/{id}/delete-setting-form` | Xoá câu hỏi | `@deleteSettingForm` :1438 | + CLC | SCR-LSN-16 |
| EP-58 | POST | `/{id}/sort-setting-form` | Sắp xếp câu hỏi | `@sortSettingForm` :1456 | + CLC | SCR-LSN-16 |
| EP-59 | GET | `/{id}/preview-top` | Preview trang top | `@previewTop` :1900 | + CLC | SCR-LSN-24 |
| EP-60 | GET | `/{id}/preview` | Preview trang thông tin cửa hàng | `@preview` :1889 | + CLC | SCR-LSN-25 |
| EP-61 | GET | `/{id}/preview-form` | Preview form câu hỏi | `@previewForm` :1912 | + CLC | SCR-LSN-26 |
| EP-62 | GET | `/{id}/booking/last-booking/{lineId}` | Đặt chỗ gần nhất của 1 LINE User | `@getLastBooking` :2208 | + CLC | modal add_new_booking |
| EP-63 | DELETE | `/{id}/course/reception-list/delete` | Xoá nhiều khung giờ | `@deleteListReception` :403 | + CLC | SCR-LSN-06 |
| EP-64 | GET | `/{id}/course/reception/{receptionId}/check-delete` | Kiểm tra có thể xoá khung giờ | `@checkDeleteReception` :2270 | + CLC | SCR-LSN-06 |
| EP-65 | POST | `/disable-tooltip` | Tắt tooltip hướng dẫn cho user hiện tại | `@disableTooltip` :1997 | BA, HP, EXP, RT | SCR-LSN-01 |

Route: `routes/web.php:1482-1598`.

### 1.2 Nhóm B — `/ajax/calendar` (middleware `check_login`, `check_remember_token`)

| Mã | Method | URL | Mô tả | Controller@method | Màn hình |
|---|---|---|---|---|---|
| EP-66 | GET | `/ajax/calendar/init-detail/{id}` | Chi tiết lịch + action 空き枠通知 (JSON) | `@ajaxGetDetailCalendar` :490 | SCR-LSN-10, SCR-LSN-15 |
| EP-67 | POST | `/ajax/calendar/save/policy` | Lưu 「利用規約」 | `@savePolicyCalendar` :507 | SCR-LSN-20 |
| EP-68 | POST | `/ajax/calendar/save/info` | Lưu 「店舗・ビジネス情報」 + 「トップ画面設定」 | `@saveCalendarInfo` :527 | SCR-LSN-18, SCR-LSN-19 |
| EP-69 | POST | `/ajax/calendar/send-mail/delete` | Gửi mã xác thực qua email để xoá lịch | `@sendMailCodeAuthDeleteCalendar` :645 | SCR-LSN-22 |
| EP-70 | POST | `/ajax/calendar/check-author/delete` | Kiểm tra mã xác thực xoá lịch | `@checkAuthorDeleteCalendar` :681 | SCR-LSN-22 |
| EP-71 | POST | `/ajax/calendar/action/delete` | **Xoá hệ thống đặt lịch** | `@deleteCalendar` :715 | SCR-LSN-22 |
| EP-72 | POST | `/ajax/calendar/save-setting/notify-full-slot` | Lưu cấu hình 「空き枠通知受け取り」 | `@saveSettingNotifyFull` :773 | SCR-LSN-15 |
| EP-73 | GET | `/ajax/calendar/history-setting/notify-full-slot` | Lịch sử thay đổi cấu hình 空き枠通知 | `@getHistorySettingNotifyFullSlot` :812 | SCR-LSN-15 |
| EP-74 | POST | `/ajax/calendar/save-setting/remind` | Tạo/sửa bước nhắc nhở (event step) | `@saveCreateSettingRemind` :830 | SCR-LSN-14 |
| EP-75 | GET | `/ajax/calendar/get-list-step-remind` | Danh sách bước nhắc nhở | `@getListStepRemind` :1069 | SCR-LSN-14 |
| EP-76 | POST | `/ajax/calendar/delete-step-remind` | Xoá bước nhắc nhở | `@deleteEventStep` :1045 | SCR-LSN-14 |
| EP-77 | GET | `/ajax/calendar/get-detail-event-step` | Chi tiết 1 bước nhắc nhở | `@getDetailEventStep` :1162 | SCR-LSN-14 |
| EP-78 | GET | `/ajax/calendar/get-list-course-by-calendar` | Danh sách khoá học (cho select remind) | `@getListCourseByCalendar` :1057 | SCR-LSN-14 |
| EP-79 | POST | `/ajax/calendar/save-setting-send-message-event-step` | Lưu tin nhắn của bước nhắc nhở | `@saveSettingSendMessageEventStep` :1226 | SCR-LSN-14 |
| EP-80 | POST | `/ajax/calendar/delete-item-action-event-step` | Xoá 1 item action của bước nhắc nhở | `@deleteItemActionEventStep` :1196 | SCR-LSN-14 |
| EP-81 | POST | `/ajax/calendar/delete-item-action-calendar` | Xoá 1 item action của lịch | `@deleteItemActionCalendar` :2115 | SCR-LSN-15 |
| EP-82 | POST | `/ajax/calendar/save-info-form-booking` | Lưu toàn bộ form câu hỏi 予約時の質問項目 | `@saveInfoFormBooking` :2498 | SCR-LSN-16 |

Route: `routes/web.php:3522-3547`.

---

## 2. Chi tiết từng endpoint

Quy ước response chung của **Nhóm A**: hầu hết method trả bao bọc `{"success": bool, "data": …, "message": string}` (`response()->json([...])`). Một số method (chủ yếu Nhóm B và các method viết sau) dùng `{"status": true, …}`. **Hai quy ước tồn tại song song trong cùng một controller** — front-end phải xử lý cả hai.

### 2.1 Nhóm A — quản lý lịch & khoá học (EP-01…EP-32)

#### EP-01 — `GET /basic/calendar/redirect-google-sheet`

Callback OAuth2 của Google. `CalendarManagementController.php:580-627`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation thật |
|---|---|---|---|---|
| `code` | query | string (authorization code) | Có | `if ($request->has('code'))`; không có ⇒ redirect thẳng về `calendar.detail` (:625) |
| `state` | query | int (= `calendar_id`) | Có | `checkCalendarBelongBot($state)` — **có kiểm tra sở hữu bot** (:584) |
| `scope` | query | string | Có | Phải chứa `https://www.googleapis.com/auth/spreadsheets` (:589) |

**Xử lý**: đổi `code` → access token, `createSheet($client, $calendar->line_name)` tạo spreadsheet mới, đọc `Google_Service_Oauth2->userinfo`, rồi UPDATE `calendar_management`: `google_sheet_id`, `google_sheet_access_token` (JSON), `google_sheet_name`, `google_account_name`, `google_account_picture`, `datetime_connect_google_sheet`, `google_sheet_status = 1` (:604-612).

**Kết quả**: luôn là **redirect** (không JSON).

| Tình huống | Kết quả | Dòng |
|---|---|---|
| Calendar không thuộc bot | `redirect()->route('404')` | :585-587 |
| Thiếu scope spreadsheets | redirect `calendar.detail` + flash 「Google スプレッドシートのアクセス権限をチェックしてください」 | :589-591 |
| Calendar không tồn tại | `redirect()->route('404')` | :592 |
| `Google_Exception` | set `google_sheet_status = 0`, log — **KHÔNG return gì** ⇒ trả về HTTP 200 với body rỗng, trình duyệt hiển thị trang trắng | :613-618 |

> ⚠ Nhánh `catch` không có `return` ⇒ trang trắng thay vì thông báo lỗi. Confidence: **Cao**.

#### EP-02 — `GET /basic/calendar/cancel-google-sheet/{id}`

`:628-644`. Tham số duy nhất `id` (path). Có `checkCalendarBelongBot($id)`; sai ⇒ `redirect()->route('404')` (:633-635).
UPDATE `calendar_management` SET `google_sheet_access_token = null`, `google_sheet_id = null` rồi redirect `calendar.detail`.

> ⚠ **Không reset `google_sheet_status`** ⇒ có thể còn `= 1` dù đã ngắt kết nối; blade dùng `google_sheet_status` để quyết định hiển thị nút reconnect (:640-643, đối chiếu `detailCalendar` :250). Confidence: **Cao**.

#### EP-03 — `GET /{calendar_id}/get-list-booking`

`:1877-1887` → `CalendarCourseService::listBookings($perPage, $calendarId, $condition)`.

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `calendar_id` | path | int | Có | **Không kiểm tra thuộc bot** (route nằm ngoài `checkLessonCalendarInBot`) |
| `perPage` | query | int | Không | mặc định `50` |
| `condition` | query | mixed | Không | truyền thẳng xuống service |

**Response**: `{"success": true, "data": <danh sách booking>, "message": ""}`

#### EP-04 — `GET /api/{calendarId}/get-list-courses`

`:1491-1507`. `perpage` mặc định **100000** (giá trị mặc định của tham số method, không lấy từ query).

**Response**
```json
{ "success": true, "data": { "…": "kết quả getListsCourse (phân trang)" }, "plan_type_bot": 1 }
```

> ⚠ `perpage = 100000` ⇒ lấy **toàn bộ** khoá học trong 1 request; với lịch có nhiều khoá học sẽ nặng. Đây là "phân trang giả".
> ⚠ Không kiểm tra `calendarId` thuộc bot.

#### EP-05 — `POST /api/course/update-booking-page-display`

`:1509-1533`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `course_id` | body | int | Có | ép `(int)`; không kiểm tra tồn tại tại controller |
| `booking_page_display` | body | `"true"`/khác | Có | **so sánh chuỗi** `=== 'true'` ⇒ `1`, mọi giá trị khác ⇒ `0` (:1512) |

**Response OK**: `{"success": true, "data": null, "message": "<message từ service>"}` (HTTP 200)
**Response lỗi**: `{"success": false, "message": "<message>"}` — **HTTP 500** (:1515-1520)

> ⚠ Dùng HTTP 500 cho lỗi nghiệp vụ (không phải lỗi server) — lặp lại ở EP-06, EP-10, EP-11, EP-13, EP-15, EP-19.

#### EP-06 — `POST /api/course/sortable`

`:1709-1731`. Tham số `order` (body, array) → `CalendarCourseService::updateOrderCourse($order)`.
Response OK `{"success":true,"data":"","message":…}`; lỗi ⇒ HTTP 500.

#### EP-07 — `POST /api/{calendarId}/course/create`

`:1536-1600`. Validate qua **`App\Http\Requests\CreateCalendarCourse`**.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation thật (`CreateCalendarCourse.php:26-34`) |
|---|---|---|---|---|
| `course_name` | body | string | **Có** | `bail｜required｜string｜max:50` — 「コース名を入力してください」/「コース名は最大50文字まで」 |
| `calendar_id` | body | int | Có (ngầm) | **không có rule**; dùng để đếm khoá học hiện có (:1540) |
| `calendarId` | path | int | Có | dùng cho `storeCourse` và đếm trần 200 (:1557) |

> ⚠ `authorize()` trả `true` — FormRequest **không kiểm tra quyền** (`CreateCalendarCourse.php:16-18`).
> ⚠ Rule `CheckCourseNameUnique` **đã bị comment** (:31) ⇒ **cho phép trùng tên khoá học**. Confidence: **Cao**.
> ⚠ Số lượng đếm dùng `$request->calendar_id` (body) nhưng tạo theo `$calendarId` (path) — hai nguồn khác nhau, client có thể gửi lệch để né kiểm tra gói free (:1540 vs :1557). Confidence: **Cao**.

**Giới hạn**

| Điều kiện | Response | Dòng |
|---|---|---|
| `bot.plan_type == 2` (free) và đã có ≥ 2 khoá học | `{"success":false,"error":"plan_free","message":"現在のプランは利用できない機能です。アップグレードが必要になります。"}` HTTP 200 | :1547-1554 |
| Đã có ≥ 200 khoá học trong lịch | `{"success":false,"message":"コース数の上限（200）を超えるため、これ以上作成できません。"}` HTTP 200 | :1557-1562 |
| Service lỗi | `{"success":false,"message":…}` HTTP **500** | :1565-1570 |
| Vượt hạn mức khi đếm lại (race 2 tab) | rollback: xoá khoá học vừa tạo, trả message giới hạn | :1572-1593 (`PlanLimitGuard::rollbackIfOverLimit`) |

**Response OK**: `{"success": true, "data": <course_id>, "message": "…"}`

#### EP-08 — `GET /api/course/{id}/edit`

`:1474-1482` → `CalendarCourseService::getCourse((int)$id)`.
**Response**: `{"success": true, "data": <bản ghi calendar_course>, "message": ""}`
> ⚠ Không kiểm tra khoá học thuộc bot hiện tại ⇒ IDOR đọc (xem §5, A-03).

#### EP-09 — `GET /api/course/{id}/get-message-notify`

`:1809-1817` → `getMessageNotify((int)$id)`. Response `{"success":true,"data":…,"message":""}`.

#### EP-10 — `POST /api/course/{id}/update`

`:1610-1660`. Validate qua **`App\Http\Requests\EditCalendarCourse`**.

Bảng tham số (tên body ⇒ cột DB) và rule thật (`EditCalendarCourse.php:31-63`):

| Tên (body) | Cột DB | Kiểu | Bắt buộc | Rule thật |
|---|---|---|---|---|
| `courseName` | `course_name` | string | **Có** | `bail｜required｜string｜max:50` |
| `systemName` | `system_name` | string | Không | `bail｜nullable｜string｜max:10` |
| `amount` | `amount` | numeric | Không | `nullable｜numeric`; controller còn `preg_replace("/[^0-9]/","",…)` (:1616) |
| `courseDescription` | `course_description` | string | Không | `bail｜nullable｜string｜max:1000` |
| `messageSendAfterBooking` | `message_send_after_booking` | string | Không | `bail｜nullable｜string｜max:5000` |
| `messageSendApproveBooking` | `message_send_approve_booking` | string | Không | `bail｜nullable｜string｜max:5000` |
| `hourDone` | `hour_done` | int | Không | **không rule**, mặc định `0` |
| `minuteDone` | `minute_done` | int | Không | **không rule** |
| `use_message_notify_send_after_booking` | cùng tên | `"true"`/khác | Không | so sánh chuỗi ⇒ 1/0 (:1619) |
| `use_message_notify_send_approve_booking` | cùng tên | `"true"`/khác | Không | như trên |
| `actionIdSendAfterBooking` | `action_id_send_after_booking` | int | Không | **không rule** |
| `actionIdSendApproveBooking` | `action_id_send_approve_booking` | int | Không | **không rule** |
| `filterIdSendAfterBooking` | `filter_id_send_after_booking` | int | Không | **không rule** |
| `filterIdSendApproveBooking` | `filter_id_send_approve_booking` | int | Không | **không rule** |
| `numberFilterSendAfterBooking` | `filter_number_send_after_booking` | int | Không | **không rule** |
| `numberFilterSendApproveBooking` | `filter_number_send_approve_booking` | int | Không | **không rule** |
| `courseImage` | `course_image` | base64 | Không | Chỉ khi `imageNew == "true"`: `Base64IsImage`, `Base64ImageType(['jpeg','png','jpg','gif','webp'])`, `Base64ImageSize(10240)` (~10MB) |
| `imageNew` | — | `"true"`/khác | Không | bật nhánh upload (:1631) |
| `imageDelete` | — | `"true"`/khác | Không | bật nhánh xoá ảnh trước khi update (:1638) |

> ⚠ `CheckCourseNameUniqueWhenUpdate` và `CheckSystemNameUnique` **đều bị comment** (`EditCalendarCourse.php:38`, `:45`) ⇒ **không chống trùng tên**. `system_name` là nhãn hiển thị trên lịch nên trùng gây nhầm lẫn vận hành. Confidence: **Cao**.
> ⚠ `authorize()` = `true`; FormRequest **không** kiểm tra `courseId` thuộc bot.

**Response OK**: `{"success":true,"data":"","message":"…"}` — **Lỗi**: `{"success":false,"message":…}` HTTP 500.

#### EP-11 — `POST /api/course/{id}/image/delete`

`:1686-1701`. Không tham số body. Lỗi ⇒ HTTP 500.

#### EP-12 — `GET /api/course/{id}/init-data-action`

`:1733-1748` → `initDataActionCalendarCourseSetting((int)$id)`. Response `{"success":true,"data":…}`; lỗi ⇒ HTTP 500 `{"success":false,"message":…}`.

#### EP-13 — `POST /api/course/delete-action`

`:1756-1781`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `action_id` | body | int | Có |
| `action_detail_id` | body | int | Có |
| `course_id` | body | int | Có |
| `tabCurrent` | body | string | Có |

**Response OK**: `{"success":true,"action_id":<id hoặc null>,"message":…}`
**Lỗi**: cùng cấu trúc, `success=false`, HTTP 500.

#### EP-14 — `GET /api/course/{id}/init-data-filter`

`:1787-1796`. Response `{"success":true,"list_preview_filter_send_after_booking":[…]}`.
> Khoá `list_preview_filter_send_approve_booking` **đã bị comment** (:1789, :1794) — front-end không còn nhận nhánh 「承認時」. Confidence: **Cao**.

#### EP-15 — `POST /api/course/{id}/delete`

`:1663-1684` → `deleteCalendarCourse($id)`. Response OK `{"success":true,"data":"","message":…}`; lỗi HTTP 500.
> ⚠ Không kiểm tra khoá học thuộc bot ⇒ IDOR xoá (xem §5, A-03).

#### EP-16 — `POST /api/course/{id}/check-booking-cancel`

`:2241-2268`. Truy vấn trực tiếp: lấy các `calendar_course_receptions` của `course_id` từ **hôm nay trở đi** (hôm nay thì `end_time >= now`), rồi kiểm tra còn `calendar_course_bookings` nào `deleted_at IS NULL` và `status NOT IN (SB_BOOKING_CANCEL, SB_BOOKING_ADMIN_CANCEL)`.

**Response**: `{"success": true, "allow_delete_course": true|false, "message": ""}`

#### EP-17 — `GET /{id}/init-data-filter`

`:1799-1806`. Response `{"success":true,"list_preview_filter":[…]}`.

#### EP-18 — `GET /{calendarId}/get-booking-setting-display`

`:1826-1835` → `CalendarManagementService::getBookingSettingDisplay($calendarId)` = `findById()` — **`where('id',…)->find()` không lọc `bot_id`** (`CalendarManagementRepository.php:21-24`, `CalendarManagementService.php:166-170`).

**Response**: `{"success": true, "data": <TOÀN BỘ bản ghi calendar_management>, "message": ""}`

> 🔴 **IDOR đọc**: route này **nằm ngoài** `checkLessonCalendarInBot` (`routes/web.php:1502`, group CLC bắt đầu :1532) và service không lọc bot ⇒ đọc được toàn bộ cấu hình lịch của bot khác, kể cả `google_sheet_access_token`, `code_delete`, `content_policy`. Confidence: **Cao**.

#### EP-19 — `POST /{calendarId}/setting-booking-display`

`:1844-1868`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `is_display_course_cost` | body | 0/1 | Không | không |
| `is_display_capacity` | body | 0/1 | Không | không |
| `is_display_course_full` | body | 0/1 | Không | không |
| `booking_setting_name` | body | string | Không | không |
| `setting_show_calendar` | body | int | Không | không |

**Response OK**: `{"success":true,"data":…,"message":…}`; lỗi ⇒ HTTP 500.
> 🔴 Cũng nằm ngoài `checkLessonCalendarInBot`, `updateBookingSettingDisplay` chỉ `findById($calendarId)` (`CalendarManagementService.php:172-180`) ⇒ **IDOR ghi**.

#### EP-20 — `POST /save-setting-payment`

`SettingPaymentCalendarController@saveSettingPayment` (:151-211).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `calendar_id` | body | int | Có | **không kiểm tra thuộc bot** (:154) |
| `is_use_payment` | body | `"true"`/khác | Có | so sánh chuỗi ⇒ 1/0 (:160) |
| `type_payment` | body | int | Khi bật | chỉ ghi khi `is_use_payment == 1` (:184-186) |
| `environment` | body | `0` test / `1` live | Khi bật | không validate giá trị |
| `description_payment` | body | string | Không | không giới hạn độ dài |

**Side effect**: ghi `history_change_payment` (from/to theo `getStatusChange()` :107-150); UPDATE `calendar_management`; đồng thời **ép bật + bắt buộc** 2 trường form 「システム表示名」(`friend_information_id = -1`) và 「メールアドレス」(`-3`) trong `calendar_setting_send_forms` (`enable=1, required=1`, trường email thêm `rule_type=1, rule_validation_type='email'`) (:189-209).

**Response**: `{"status": true}` — **không có nhánh lỗi nào**.

> 🔴 **IDOR ghi nghiêm trọng**: `calendar_id` lấy thẳng từ body, **không** `checkCalendarBelongBot`, route **không** nằm trong `checkLessonCalendarInBot` (`routes/web.php:1505`). Admin bất kỳ có thể **tắt thanh toán hoặc chuyển sang môi trường test cho lịch của bot khác** ⇒ khách đặt chỗ mà không bị thu tiền. Confidence: **Cao**.

#### EP-21 — `GET /init-data-setting-payment`

`SettingPaymentCalendarController@initDataSettingPayment` (:16-105).

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `calendar_id` | query | int | Có |

**Xử lý**: đọc `strip_bots` theo `getBotId()` (đúng bot), suy ra `checkLinkPayment` / `checkLinkedStripe` (`status_strip_bot == 3`) / `checkLinkedUnivapay` (có cả `univapay_app_id` và `univapay_app_test_id`); đọc `calendar_management` (4 cột) theo `calendar_id` **không lọc bot**; đọc `history_change_payment` theo `calendar_id` **không lọc bot** và gắn nhãn tiếng Nhật; đọc `bot_contracts.contract_type`; kiểm tra 2 trường form bắt buộc.

**Response**
```json
{
  "status": true,
  "checkLinkPayment": false,
  "settingPayment": { "type_payment": 1, "environment": 1, "description_payment": "…", "is_use_payment": 1 },
  "checkLinkedUnivapay": true,
  "checkLinkedStripe": false,
  "listHistoryPayment": [
    { "id": 12, "calendar_id": 34, "from": 0, "to": 2, "user": {"…": "quan hệ user"},
      "text_from": "停止", "text_to": "利用中(本番環境)" }
  ],
  "contractType": "standard",
  "checkEnableNameAndEmailDefault": true
}
```
> 🔴 `listHistoryPayment` load kèm quan hệ `user` (**thông tin tài khoản Admin**) và không lọc `bot_id` ⇒ IDOR đọc xuyên bot (:52-56).

#### EP-22 — `GET /get-data-friend-info`

`:2281-2441`. **Không tham số** — dựa hoàn toàn vào `getBotId()`.
Đọc `category` (kind = `information_friend`, `bot_id`, `is_deleted = 0`) kèm `friendInformationSetting` lọc `type_data = TYPE_DATA_INPUT`, cộng thêm nhóm mặc định `group_id = 0`.

**Response** (rút gọn): `{"success": true, "data": { "…danh sách nhóm + trường hồ sơ bạn bè…" }}`
> ✅ Đây là một trong ít endpoint **có** lọc `bot_id` chặt chẽ.

#### EP-23 — `GET /get-category-id-of-friend-setting`

`:2442-2496`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `friend_setting_id` | query | int (có thể âm) | Có |

**Ánh xạ ID âm → nhãn** (:2456-2487): `-1` 「システム表示名」, `-2` 「携帯電話」, `-3` 「メールアドレス」, `-4` 「生年月日」, `-6` 「都道府県名」, `-7` 「郵便番号」, `-8` 「市区町村名」, `-9` 「町名/番地」, `-10` 「建物名・部屋番号」. `category_id` = `-2` khi `id < -4`, ngược lại `-1`.

**Response**: `{"category_id": -1, "title": "システム表示名"}` — `0` khi `friend_setting_id == 0`.
> ⚠ Với `friend_setting_id > 0`, truy vấn `FriendInformationSetting::where('id',…)` **không lọc `bot_id`** ⇒ đọc được tên trường hồ sơ của bot khác (:2451, :2486). Mức độ: thấp (chỉ lộ nhãn).

#### EP-24 — `POST /order-refund`

`:2007-2113`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `booking_id` | body | int | Có | `withTrashed()->find()`; **không kiểm tra null**, **không kiểm tra thuộc bot** (:2016) |
| `refundType` | body | `'now'` / khác | Có | `'now'` = hoàn qua cổng; giá trị khác = chỉ ghi nhận 「決済システムから」 (:2019, :2081) |

**Xử lý**
1. `refundType == 'now'` **và** `booking.charge_id` khác rỗng:
   - `payment_system == 0` (Stripe): lấy `strip_bots` theo **`getBotId()` của người đang đăng nhập**, chọn `strip_secret_test_key` / `strip_secret_live_key` theo `booking.environment`, gọi `refundMoneyPaymentIntent($booking->charge_id)` (:2026-2039).
   - ngược lại (UnivaPay): `refundMoney()` rồi `getRefundMoney()` xác nhận (:2045-2078).
2. UPDATE booking: `payment_status = SP_REFUND`, `admin_id = Auth::id()`, `refund_type` (:2086-2090).
3. `CalendarGoogleSheetService::updateStatusPaymentBooking($bookingId)`; tạo `calendar_course_booking_history_actions` `status = SB_REFUND`, `reason = "¥{payment_amount}の返金（エルメから／決済システムから）"` (:2092-2100).

**Response OK**: `{"status": true}`
**Lỗi cổng thanh toán**: `{"status": false, "error_message": "<JP hoặc message Stripe>"}` HTTP 200 (:2035-2038, :2072-2077)
**Exception**: `{"status": false}` — **không kèm message** (:2107-2111)

> 🔴 **IDOR ghi**: `booking_id` không đối chiếu bot. Với `refundType != 'now'` **không hề gọi cổng thanh toán** ⇒ chỉ cần gửi id là đánh dấu 「返金済み」 cho đặt chỗ của bot khác. Confidence: **Cao** (:2016, :2081-2090).
> ⚠ **Không kiểm tra `payment_status` hiện tại** ⇒ hoàn tiền lặp nhiều lần (trùng với S-21 của phía app di động — cùng một thiếu sót ở hai lớp).
> ⚠ Trộn khoá của bot đang đăng nhập với `charge_id` của booking ⇒ khi IDOR sang bot khác, lệnh gọi Stripe thất bại nhưng **booking vẫn có thể bị đánh dấu hoàn tiền ở nhánh `refundType != 'now'`**.

#### EP-25 — `GET /` (`calendar.index`)

`:97-104`. Trả view `basic.calendar_management.index` với `liffId` (`bots.liff_app_id_booking` hoặc fallback `liff_app_id`) và `numberCalendar` (`BotSlotService::getNumberCalendarByContract()`).

#### EP-26 — `GET /get-list-calendar`

`:106-122`. Không tham số. `CalendarManagementService::getListCalendar()` lọc theo `getBotId()`, `ORDER BY order ASC` (`CalendarManagementRepository.php:31-34`), map qua **`CalendarResource`**.

**Response**
```json
{
  "success": true,
  "data": {
    "calendar": [
      { "id": 12, "calendar_name": "レッスン予約", "line_name": "○○スタジオ",
        "enable_use_calendar": true, "using_google": true, "order": 1,
        "google_sheet_id": "1AbC…", "image_calendar_top": "https://…" }
    ],
    "canCreate": true,
    "enableTooltipCalendar": 1,
    "messageErrorMax": ""
  },
  "message": ""
}
```
`CalendarResource` chỉ trả **8 trường** (`app/Http/Resources/CalendarResource.php:17-27`) — đây là endpoint hiếm hoi có kiểm soát trường trả ra.

**Giới hạn gói** (`CalendarManagementService::checkMaxCalendarMayBeCreate()` :113-158): `contract_type == 'free'` ⇒ 1 lịch; `standard` (flag_contract_new = 1) / `enterprise` ⇒ 3; `standard` (flag = 0) / `pro` / `enterprise_pro` ⇒ 10. Vượt ⇒ `canCreate = false` và `messageErrorMax` = 「上限に達したので、新しく追加できません。」 hoặc 「現在のプランは利用できない機能です。アップグレードが必要になります。」.

#### EP-27 — `GET /create`

`:124-127`. Trả view `basic.calendar_management.create`, **không truyền dữ liệu nào**.

#### EP-28 — `POST /store`

`:129-152` → `CalendarManagementService::addNewCalendar($request->all())`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation thật |
|---|---|---|---|---|
| `line_name` | body | string | Thực tế có | **Không validate**; được copy sang `store_name` (`CalendarManagementService.php:62`) |
| *(mọi trường khác)* | body | mixed | — | `array_merge($request, $data)` ⇒ **mọi field client gửi đều đi vào `create()`** (`CalendarManagementService.php:66`) |

`bot_id` bị **ghi đè** bằng `getBotId()` (an toàn). Hai tin nhắn mặc định 「空き枠通知」 được sinh từ `getMessageTemplate(1|2)`.

**Response OK**: `{"success": true, "data": {"calendarId": 123}, "message": ""}`
**Vượt hạn mức**: `{"success": false, "data": null, "message": "<1 trong 2 chuỗi giới hạn>"}` HTTP 200 (:135-141)

Sau khi tạo, controller khởi tạo bản ghi mặc định: `calendarSettingMessageService->getSettingMessage($id)` và `calendarSettingSendFormService->getSettingForm($id)` (:143-144) — hai method này **tạo dữ liệu nếu chưa có** (side effect trong hàm tên `get*`).

> ⚠ **Mass assignment**: `array_merge($request, $data)` cho phép client set bất kỳ cột nào của `calendar_management` ngay lúc tạo — ví dụ `is_use_payment`, `environment`, `google_sheet_id`. Mức độ phụ thuộc `$fillable` của model. Confidence: **Trung bình** (chưa đối chiếu `$fillable`).
> ✅ Có cơ chế chống race 2-tab: `PlanLimitGuard::rollbackIfOverLimit` đếm lại sau khi tạo và xoá bản ghi thừa (`CalendarManagementService.php:69-82`, ticket #39230).

#### EP-29 — `POST /{id}/edit`

`:154-163` → `CalendarManagementService::editCalendar($id, $request->all())` → `collect($request)->except(['id'])` → `CalendarManagementRepository::editCalendar` = **`where('id', $id)->update($data)`** (`CalendarManagementRepository.php:35-38`).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `id` | path | int | Có | **Không kiểm tra thuộc bot** — route ở `web.php:1524`, nằm **ngoài** nhóm `checkLessonCalendarInBot` (bắt đầu :1532) |
| *(mọi trường khác)* | body | mixed | — | **Không validate gì cả**; toàn bộ trừ `id` được đưa thẳng vào `UPDATE` |

**Response**: `{"success": true, "data": null, "message": ""}` — **luôn thành công**, kể cả khi `id` không tồn tại.

> 🔴 **Lỗ hổng nghiêm trọng nhất của Nhóm A**: kết hợp *IDOR ghi* + *mass assignment* + *không validate*. Một Admin bất kỳ gửi `POST /basic/calendar-management/{id_của_bot_khác}/edit` với payload tuỳ ý sẽ sửa trực tiếp bản ghi `calendar_management` của bot khác (đổi tên, bật/tắt `enable_use_calendar`, ghi đè `google_sheet_access_token`, `code_delete`…). Confidence: **Cao**.

#### EP-30 — `POST /sort`

`:186-195` → `CalendarManagementService::sort($request->listId)` → lặp `editCalendar($id, ['order' => $key + 1])` (`CalendarManagementService.php:105-111`).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `listId` | body | int[] | Có | **Không kiểm tra từng id thuộc bot**; `null` ⇒ `foreach` trên null ⇒ warning/500 |

**Response**: `{"success": true, "data": null, "message": ""}`
> 🔴 IDOR ghi (phạm vi hẹp: chỉ cột `order`) — đảo thứ tự lịch của bot khác.

#### EP-31 — `GET /course/create`

`:165-173`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `calendarId` | query | int | Có | ✅ **Có** kiểm tra thủ công: `empty($calendar) \|\| $calendar->bot_id != getBotId()` ⇒ `redirect()->route('calendar.index')` (:167-170) |

Trả view `basic.calendar_management.course_create` với biến `calendar`.
> Đây là **ví dụ mẫu** cho cách kiểm tra sở hữu đúng — nhưng chỉ được áp dụng ở đúng method này trong toàn bộ Nhóm A ngoài CLC.

#### EP-32 — `POST /course/store`

`:175-184` → `CalendarCourseService::storeCalendarCourse($request->all())` → `$this->model->create($data)` (`CalendarCourseRepository.php:28-31`).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| *(toàn bộ body)* | body | mixed | — | **Không FormRequest, không validate** — khác hẳn EP-07 (`createCourse`) vốn có `CreateCalendarCourse` |

**Response**: `{"success": true, "data": null, "message": ""}`

> 🔴 **Đường vòng qua validation**: EP-32 tạo `calendar_course` mà **không** kiểm tra `course_name` (required/max:50), **không** kiểm tra hạn mức gói free (2 khoá học) hay trần 200 khoá học — tất cả những thứ EP-07 kiểm. `calendar_id` do client gửi ⇒ tạo khoá học vào lịch của bot khác. Confidence: **Cao** (:175-184).

---

### 2.2 Nhóm A — thao tác bên trong 1 lịch (EP-33…EP-65)

> EP-33…EP-64 nằm trong nhóm con có `checkLessonCalendarInBot`; **EP-65 (`/disable-tooltip`) nằm ngoài** nhóm này (`routes/web.php:1598`) nhưng được mô tả ở đây cho liền mạch.

Toàn bộ nhóm này **được bảo vệ IDOR ở cấp `{id}` (calendar)** bởi middleware `checkLessonCalendarInBot` (`routes/web.php:1532`). Tuy nhiên middleware **chỉ kiểm tra `id` calendar**, **không** kiểm tra `receptionId`, `bookingId`, `courseId` gửi kèm có thuộc calendar đó không — xem §5, A-06.

#### EP-33 — `GET /{id}` (`calendar.detail`)

`:197-245`. Trả view `basic.calendar_management.detail`.

**Dữ liệu truyền vào view**: `google_sheet_auth_url` (chỉ sinh khi chưa có token **hoặc** `google_sheet_status == 0`), `richMenus` (rich menu `status_rich = 1`, loại bỏ category đã xoá), `scenario`, `conversion`, `statusObject`, `calendarName`, `storeName`, `usePayment`, `hashCalendarId` (`Hashids::encode($id)`), `totalUser` (số bạn bè chưa block của bot), `google_sheet_auth_url_reconnect`, `google_sheet_status`, `is_google_sheet_error` (`token != null && status == 0`).

> ⚠ `CalendarManagement::find($id)` **không kiểm tra null** (:199) — nhưng CLC đã chặn trước nên thực tế không tới. Confidence: **Cao**.

#### EP-34 — `GET /{id}/course/list`

`:247-256` → `CalendarCourseService::getCourseList($request->all(), $id)`.

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `displayMode` | query | `'day'` / khác | Có | `'day'` ⇒ lấy khung giờ theo ngày (`CalendarCourseService.php:86`) |
| `date` | query | `Y-m-d` | Khi `displayMode='day'` | |

**Response**: `{"success": true, "data": [ …danh sách khoá học kèm `calendarCourseReceptions`, `listHoursReception`, `row`, `totalStatus`… ], "message": ""}`
> ⚠ `$data['displayMode']` truy cập trực tiếp — thiếu tham số ⇒ `Undefined index` (:86).

#### EP-35 — `POST /{id}/course/reception/create` — tạo khung giờ hàng loạt

`:258-263` → `CalendarCourseReceptionService::create($request->all())` (`CalendarCourseReceptionService.php:52-136`).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation thật |
|---|---|---|---|---|
| `scheduleType` | body | `1` = lặp theo thứ / khác = chọn ngày | Có | `isset($request['scheduleType'])` — thiếu thì **toàn bộ khối bị bỏ qua, trả về `null`** (:54) |
| `courseId` | body | int | Có | không kiểm tra tồn tại |
| `needEndTime` | body | `"false"`/khác | Có | so sánh chuỗi ⇒ `set_end_time` 0/1 (:99) |
| `repeatDueDate` | body | `Y-m-d` | Khi `scheduleType == 1` | phải ≥ hôm nay 「将来の日付を選択してください。」; ≤ 1 năm 「最大1年後までの日付を選択できます」 (:70-77) |
| `dayOfWeekSchedule` | body | int[] (`0`–`6`) | Khi `scheduleType == 1` | rỗng ⇒ 「曜日を選択してください」 (:66-69) |
| `dateCanBooking` | body | int[] (**timestamp mili-giây**) | Khi `scheduleType != 1` | `Carbon::createFromTimestamp($date / 1000)` (:91) |
| `settingTime[]` | body | array of `{startTime, endTime, maxPerson, typeLimit}` | Có | mỗi phần tử: `startTime` rỗng ⇒ 「開始時間を入力してください」; `endTime` rỗng ⇒ 「終了時間を入力してください」 (:102-113) |

**Response**: `response()->json($response)` — trả thẳng mảng của service:
- Lỗi: `{"success": false, "message": "<JP>"}`
- Thành công: `null` hoặc mảng do service trả (không chuẩn hoá).

> ⚠ **Không giới hạn số lượng**: `listDate × settingTime` có thể lên tới 365 ngày × N khung giờ trong một request, không transaction (đối chiếu S-? của EP-M13 phía app — **cùng một thiếu sót ở cả hai lớp**).
> ⚠ Khi `scheduleType` không được gửi, method **kết thúc mà không trả gì** ⇒ response body `null`, front-end không phân biệt được thành công/thất bại (:54, :136).

#### EP-36 — `GET /{id}/course/reception/{receptionId}`

`:265-274` → `getDetailReception($request->all(), $receptionId, $id)`. `receptionId` bị ràng buộc regex `([1-9]+[0-9]*)` ở route (`web.php:1539`).

| Tên | Vị trí | Kiểu | Ghi chú |
|---|---|---|---|
| `sortStatus` | query | `asc`/`desc` | sắp xếp danh sách đặt chỗ trong khung giờ (`CalendarCourseReceptionRepository.php:39`) |

**Response**: `{"success": true, "data": <CalendarCourseReceptionWithBookingResource>, "message": ""}` — gồm thông tin khung giờ + danh sách đặt chỗ + `calendar_setting_send_messages` (moment `booking`).
> ⚠ **`receptionId` không được đối chiếu với `{id}` calendar** ⇒ IDOR cấp khung giờ (xem §5, A-06).

#### EP-37 — `GET /{id}/today-booking/reception/{receptionId}`

`:2197-2206` → `CalendarCourseService::getDetailBookingBySlot($calendarId, $receptionId, $type)`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `type` | query | string | Không |

**Response**: `{"success": true, "data": …}` — **không có khoá `message`** (khác quy ước chung).

#### EP-38 — `POST /{id}/course/booking/create` — Admin đặt chỗ hộ khách

`:276-285` → `CalendarCourseBookingService::create($request->all(), $id)` (`CalendarCourseBookingService.php:86-260`).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `receptionId` | body | int | Có | `CalendarCourseReception::find()` — **không kiểm tra null** (:91) |
| `showSelectUser` | body | `1` = chọn bạn bè LINE / `2` = nhập tên tự do | Có | quyết định dùng `lineUserId` hay `lineUserName` (:105-106) |
| `lineUserId` | body | int | Khi `showSelectUser == 1` | |
| `lineUserName` | body | string | Khi `showSelectUser == 2` | |
| `name` | body | string | Có | ghi thẳng `calendar_course_bookings.name` |
| `email` | body | string | Có | ghi thẳng, **không validate định dạng** |
| `doAction` | body | `0`/`1` | Có | `1` ⇒ `sendActionBooking(… 'lessonAdminBooking' …)` (:232-234) |
| `formQuestion` | body | array | Không | `json_encode` → `friend_info`; đồng thời **ghi đè hồ sơ bạn bè** khi `lineUserId > 0 && showSelectUser == 1` (:129-231) |

**Response**: `{"success": true, "data": null, "message": ""}` — **luôn `true`**, kể cả khi service ném lỗi nghiệp vụ.

> 🔴 **Không kiểm tra sức chứa**: `create()` không gọi `checkValidSlot()`/`checkCanBooking()` ⇒ Admin tạo được số đặt chỗ vượt `total_person`. **Trùng khớp với S-20** của `api-spec-public.md` (EP-M15 `addNewBooking` phía app) — đây là **cùng một lỗ hổng thể hiện ở hai lớp**, không phải hai lỗi riêng. Confidence: **Cao**.
> Nếu khách đã có booking `status = 3` (chờ thông báo trống chỗ) ở slot đó thì **cập nhật đè** bản ghi cũ thay vì tạo mới (`getBookingWaitCancel()` :119).

#### EP-39 — `GET /{id}/course/reception/booking-list`

`:287-296` → `CalendarCourseReceptionService::getBookingList($request->all(), $id)` (:155-231).

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `courseIdList` | query | string CSV | Có | `explode(',', …)` (:158) |
| `date` | query | `Y-m-d` | Có | |
| `mode` | query | `week`/`month`… | Có | `week` ⇒ khung 1 giờ, `end_time == '00:00'` được chuyển thành `'23:59'` (:160-164) |
| `startTime` | query | `H:i` | Khi `mode = week` | |

**Response**: `{"success": true, "data": {"time": "2026.09.01(火)", "…": "danh sách đặt chỗ theo khung giờ"}, "message": ""}`

#### EP-40 — `GET /{id}/booking-list`

`:298-307` → `CalendarCourseBookingService::getBookingListDataCustom($request->all(), $id)`.

Tham số lọc (`CalendarCourseBookingRepository.php:46-133`):

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `lineName` | query | string | Có (đọc trực tiếp) | tìm kiếm theo tên khách |
| `courses` | query | string CSV | Không | `explode(',')` |
| `bookingStatus` | query | string CSV | Không | mã trạng thái đặt chỗ |
| `paymentStatus` | query | string CSV | Không | |
| `startTime` / `endTime` | query | `H:i` | Không | giá trị `'0:00'` bị coi như rỗng (:93-94) |
| `dateFrom` / `dateTo` | query | `Y-m-d` | **Có** | `whereBetween(DATE(received_booking_date), [dateFrom, dateTo])` — thiếu ⇒ `Undefined index` (:116) |
| `limit` | query | int | **Có** | dùng cho `limit()` và `offset()` (:132-133) |
| `page` | query | int | **Có** | `offset = limit * page - limit` |

**Response**: `{"success": true, "data": {"totalPage": …, "…": "danh sách đặt chỗ + tổng số đặt/huỷ"}, "message": ""}`
> `data` chứa `friend_info` (JSON câu trả lời form), thông tin thẻ và trạng thái thanh toán — dữ liệu PII, nhưng ở đây **có** CLC bảo vệ ở cấp calendar.

#### EP-41 — `GET /{id}/reception/list`

`:309-318` → `getReceptionListDataCustom($request->all(), $id)` (:232-278).

Tham số lọc (`CalendarCourseReceptionRepository.php:114-148`): `lineName` (thực chất là **tên khoá học** — biến đặt tên sai, :114), `courses` (CSV), `startTime`/`endTime`, `dateFrom`/`dateTo`, `sort` (`asc`/`desc`), `limit`, `page`.

**Response** — mỗi phần tử: `{id, courseName, executionTime, amount, totalBooking (= total_approve), remaining (= total_person - total_booking), requests (= total_request + total_request_cancel), waitingCancel, typeLimit, …}`; `end_time == '00:00'` hiển thị thành `24:00` (:251).

> ⚠ Tên tham số `lineName` dùng để lọc **tên khoá học** — nợ kỹ thuật gây nhầm khi bảo trì. Confidence: **Cao**.

#### EP-42 — `POST /{id}/booking/change-status`

`:320-338` → `CalendarCourseBookingService::changeStatusBooking($request->all())` (:709-965).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `selectedItems` | body | int[] (`booking_id`) | Có | `foreach` trực tiếp — không kiểm tra rỗng/null (:758) |
| `actionChange` | body | enum | Có | `approveBooking`｜`denyBooking`｜`approveCancel`｜`requestCancel`｜`denyCancel`｜`adminCancel`. **Giá trị lạ ⇒ `Undefined index` trong `$actionMapping`** (:786-788) |
| `doAction` | body | `0`/`1` | Có | có gửi action/tin nhắn kèm hay không (:712) |
| `bot_id` | body | int | Không | chỉ dùng khi `getBotId()` rỗng (luồng callback) (:714) |
| `user_login_id` | body | int | Không | chỉ dùng khi `Auth::id()` rỗng (:715) |
| `chargeId` | body | string | Không | dùng ở nhánh thanh toán (:819) |
| `from_callback` | body | any | Không | có mặt ⇒ bỏ qua kiểm tra webhook và bỏ qua bước thu tiền (:771, :798) |

**Chặn đầu vào**: nếu `booking.status_webhook ∈ {UNPROCESSED, TIMEOUT, TIMEOUT_WEBHOOK}` **và** `payment_system == 1` (UnivaPay) **và** không có `from_callback`: nếu chỉ chọn 1 mục ⇒ dừng và trả lỗi 「決済処理を行っていますので、操作できません。」; nếu chọn nhiều mục ⇒ **âm thầm bỏ qua mục đó** (:766-784).

**Ánh xạ trạng thái** (`$actionMapping` :717-756):

| `actionChange` | `status` mới | `statusHistory` | `moment` |
|---|---|---|---|
| `approveBooking` | `SB_BOOKING_APPROVE` | `SB_REQUEST_BOOKING_APPROVE` | booking |
| `denyBooking` | `SB_BOOKING_DENY` | `SB_REQUEST_BOOKING_DENY` | booking |
| `approveCancel` | `SB_BOOKING_CANCEL` | `SB_REQUEST_CANCEL_APPROVE` | cancel |
| `requestCancel` | `SB_REQUEST_BOOKING_CANCEL` | `SB_REQUEST_CANCEL_WAITING_APPROVE` | cancel |
| `denyCancel` | `SB_BOOKING_APPROVE` | `SB_REQUEST_CANCEL_DENY` | cancel |
| `adminCancel` | `SB_BOOKING_ADMIN_CANCEL` | `SB_REQUEST_CANCEL_ADMIN_CANCEL` | cancel |

Khi duyệt đặt chỗ đang `SB_REQUEST_BOOKING` và `payment_status == SP_NOT_PAYMENT` ⇒ gọi `payment()` thu tiền trước khi đổi trạng thái (:790-812).

**Response OK**: `{"success": true, "data": null, "message": null}`
**Lỗi thanh toán / webhook**: `{"success": false, "data": null, "message": "<JP>"}` — controller nhận biết lỗi bằng cách kiểm tra `isset($changeStatus['paymentStatus'])` (:327-332).

> ⚠ **`selectedItems` là mảng `booking_id` tuỳ ý, không đối chiếu với `{id}` calendar** ⇒ CLC không bảo vệ được ở cấp booking (§5, A-06).
> ⚠ Không `DB::transaction`: thu tiền thành công nhưng bước đổi trạng thái lỗi ⇒ đã trừ tiền mà trạng thái không đổi (**trùng ghi nhận ở EP-M01** phía app).

#### EP-43 — `DELETE /{id}/booking/delete`

`:340-350` → `CalendarCourseBookingService::delete($request->all())` (:1075-1099).

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `bookingId` | body | int | Có |

Ghi audit `addLogUserAction('deleteBooking Lesson' . $bookingId)` (:342). Service **xoá mềm** booking, ghi lịch sử và xoá `mobile_notify` liên quan (`lesson_booking_id`, type calendar_lesson, `is_confirm = 0`).

**Response**: `{"success": true, "data": null, "message": ""}` — **luôn `true`**, kể cả `bookingId` không tồn tại.
> ⚠ `bookingId` không đối chiếu calendar `{id}` (§5, A-06).

#### EP-44 — `GET /{id}/booking/{bookingId}/history`

`:352-361` → `CalendarCourseBookingHistoryService::getBookingHistoryList($bookingId)`.
**Response**: `{"success": true, "data": [ …lịch sử thao tác (status, reason, admin_id, action_date)… ], "message": ""}`
> ⚠ `bookingId` không đối chiếu calendar `{id}` ⇒ đọc lịch sử của đặt chỗ bất kỳ trong hệ thống, kể cả bot khác (§5, A-06). Confidence: **Cao**.

#### EP-45 — `GET /{id}/booking/deleted`

`:363-372` → `getDeletedBooking($request->all(), $id)` (:1100-1153). Tham số `sortStatus` (`asc`/`desc`, `CalendarCourseBookingRepository.php:246`) sắp xếp theo `deleted_at`.
**Response**: `{"success": true, "data": [ …đặt chỗ đã xoá kèm tên khoá học, ảnh, tên khách… ], "message": ""}`

#### EP-46 — `POST /{id}/course/reception/update`

`:374-383` → `CalendarCourseReceptionService::update($request->all())` (:279-302).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `receptionId` | body | int | Có | `find()`; rỗng ⇒ `return false` (service), controller **vẫn trả `success: true`** (:282-284) |
| `maxPerson` | body | int | Có | ghi thẳng `total_person`, **không chặn nhỏ hơn `total_booking`** |
| `typeLimit` | body | `0` = không giới hạn / `1` = có giới hạn | Có | ghi thẳng `type_limit_booking` |
| `calendar_id` | body | int | Có | dùng cho `sendNotifyWhenThereIsSlotEmpty()` |

**Side effect**: nếu khung giờ đang kín (`total_booking == total_person`) và thao tác làm nới chỗ (tăng `maxPerson` với `typeLimit=1`, hoặc chuyển `typeLimit=0`) ⇒ **bắn tin LINE cho toàn bộ người đăng ký 「空き枠通知」** (:291-301).

**Response**: `{"success": true, "data": null, "message": ""}` — **luôn `true`**.
> ⚠ **Không chặn hạ `maxPerson` xuống dưới `total_booking`** ⇒ overbooking âm. **Trùng S-22** của phía app di động (EP-M11).

#### EP-47 — `DELETE /{id}/course/reception/delete`

`:385-401` → `CalendarCourseReceptionService::delete($request->all())` (:304-412).

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `receptionId` | body | int | Có |

**Chặn**: `reception.total_approve > 0` ⇒ trả chuỗi 「「ステータス：予約確定」の予約が残っています。 受付枠を削除する場合、この受付枠の全ての予約が 「ステータス：キャンセル」になっている必要があります。」

**Response lỗi**: `{"success": false, "data": null, "message": "<chuỗi trên>"}` (:387-393)
**Response OK**: `{"success": true, "data": null, "message": ""}`

> ⚠ Controller **so sánh bằng chuỗi tiếng Nhật cứng** (`$response == '「ステータス…'`, :387) — sửa một ký tự trong service sẽ âm thầm biến lỗi thành thành công. **Cùng nợ kỹ thuật với EP-M14** phía app di động. Confidence: **Cao**.

#### EP-48 — `GET /{id}/edit-course/{courseId}`

`:421-448`. Trả view `tabs.course.edit_course` với `statusObject`, `conversion`, `scenario`, `richMenus`, `courseId`, `calendarId`, `botId`, `botPlanType`, `totalUser`.
> ⚠ `courseId` **không được kiểm tra thuộc `{id}`** — chỉ truyền xuống view; dữ liệu thật lấy qua EP-08.

#### EP-49 — `POST /{id}/reception/export-csv`

`:461-470` → `CalendarCourseBookingService::exportCsv($request->all(), $id)` (:1154-1291).

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `receptionId` | body | int | Có |

**Nội dung CSV**: header cố định `['タイムスタンプ','ステータス','お客様名（LINE名）','お客様名（システム表示名）','決済金額','決済ステータス']` + **mỗi câu hỏi trong `calendar_setting_send_forms` là một cột** (:1165-1173). Trạng thái được dịch sang tiếng Nhật: 「予約確定」「予約確定（手動追加）」「予約リクエスト」「キャンセル」「キャンセルリクエスト」「キャンセル（手動）」… (:1186-1200).

**Response**: `{"success": true, "data": <danh sách đường dẫn file trong `public/export/`>, "message": ""}`

> 🔴 **File CSV chứa PII được ghi vào `public/`** — thư mục phục vụ web tĩnh, tên file đoán được (`export/{tên_khoá_học}{timestamp}.csv`, `CalendarCourseService.php:309-310`), **không có cơ chế dọn dẹp**. Ai biết/đoán được tên file đều tải được mà không cần đăng nhập. Confidence: **Cao**.

#### EP-50 — `POST /{id}/course/export-csv`

`:450-459` → `CalendarCourseService::exportCsv($request->all())` (:297-350).

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `courseList` | body | int[] | Có |
| `startTime` / `endTime` | body | datetime | Có | dùng làm khoảng lọc khung giờ |

**Header CSV**: `['追加したい日付','開始時間','終了時間','このコースの予約を停止する予約上限人数（上限を設定しない場合は「無制限」とご入力ください）']`. `type_limit_booking = 0` xuất thành 「無制限」 (:319).
**Response**: `{"success": true, "data": [ "export/…csv" ], "message": ""}` — cùng vấn đề thư mục `public/export` như EP-49.
> ⚠ `courseList` **không đối chiếu với `{id}`** ⇒ xuất khung giờ của khoá học thuộc bot khác (§5, A-06).

#### EP-51 — `POST /{id}/course/import-csv`

`:472-488` → `CalendarCourseService::importCsv($request->all())` (:351-461).

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `file` | body | file upload | Có | truyền **thẳng vào `fopen($request['file'], "r")`** (:357) |
| `courseId` | body | int | Có | dùng cho `checkExistReception` và `create` (:411, :425) |

**Validate từng dòng CSV** (bỏ dòng đầu = header):

| Cột | Regex / điều kiện | Thông điệp lỗi |
|---|---|---|
| 1 — ngày | `^[0-9]{4}-(0[1-9]\|1[0-2])-(0[1-9]\|[1-2][0-9]\|3[0-1])$` | `{n}行の追加したい日付のデータに不備があります` |
| 2 — giờ bắt đầu | `^(0?[0-9]\|1[0-9]\|2[0-3]):[0-5][0-9]$` | `{n}行の開始時間のデータに不備があります` |
| 3 — giờ kết thúc | `^(0?[0-9]\|1[0-9]\|2[0-4]):[0-5][0-9]$` | `{n}行の終了時間のデータに不備があります` |
| 4 — sức chứa | `無制限` hoặc `^(0\|[1-9]\d*)$` | `{n}行の予約上限人数のデータに不備があります` |
| 2 vs 3 | `start > end` ⇒ lỗi cột 2; `start == end` ⇒ lỗi cột 3; `end` là `00:00`/`24:00` thì chỉ chặn `start == '24:00'` | như trên |
| 4 vs hiện tại | khung giờ đã tồn tại và `total_booking > giá trị mới` | `{n}行の予約上限人数のデータに不備があります` |

Nếu **có bất kỳ lỗi nào** ⇒ không ghi gì, trả toàn bộ chuỗi lỗi (nhiều dòng nối bằng `\n`).
Nếu hợp lệ ⇒ với mỗi dòng: **bỏ qua thời điểm đã qua** (`isPast()`, :420); chưa có khung giờ ⇒ `create()`; đã có ⇒ `update(total_person, type_limit_booking)`, và nếu thao tác làm nới chỗ trên khung giờ đang kín ⇒ **bắn 「空き枠通知」** (:436-444).

**Response OK**: `{"success": true, "data": null, "message": ""}`
**Response lỗi**: `{"success": false, "data": null, "message": "<chuỗi lỗi nhiều dòng>"}` (:481-486)

> ⚠ `無制限` được lưu thành `total_person = 1, type_limit_booking = 0` (:428-429) — giá trị `1` là giá trị rác, chỉ `type_limit_booking` mới có ý nghĩa. Dễ gây hiểu nhầm khi đọc DB.
> ⚠ **Rủi ro LFI/SSRF**: `fopen($request['file'], "r")` — nếu client gửi `file` dưới dạng **chuỗi** thay vì file upload (ví dụ `/etc/passwd` hoặc `http://…`), `fopen` sẽ mở đúng đường dẫn/URL đó và nội dung được parse như CSV. Chỉ an toàn khi Laravel bind ra `UploadedFile`. Confidence: **Trung bình** (:357) — cần kiểm chứng thực tế.
> ⚠ Không giới hạn số dòng CSV.

#### EP-52 — `GET /{id}/setting-message`

`:1375-1384` → `CalendarSettingMessageService::getSettingMessage($id)`. **Method này tạo bản ghi mặc định nếu chưa có** (được gọi ngay sau EP-28) — side effect trong hàm `get*`.
**Response**: `{"success": true, "data": <calendar_setting_send_messages: các moment `booking` và `cancel`>, "message": ""}`

#### EP-53 — `POST /{id}/save-setting-message`

`:1386-1395` → `CalendarSettingMessageService::saveSettingMessage($request)` — **truyền cả object `Request`** xuống service (khác các method khác truyền `$request->all()`).
**Response**: `{"success": true, "data": <setting sau khi lưu>, "message": ""}` — **không có nhánh lỗi**.
> Đây là endpoint lưu toàn bộ SCR-LSN-12 「予約時の各種設定」 và SCR-LSN-13 「予約キャンセル時の各種設定」 (thời hạn nhận đặt, chế độ リクエスト制, tin nhắn tự động, action kèm theo). Chi tiết quy tắc nghiệp vụ thuộc `logic-spec.md`.

#### EP-54 — `GET /{id}/setting-form`

`:1397-1405` → `CalendarSettingSendFormService::getSettingForm($id)` — cũng **tạo bộ câu hỏi mặc định nếu chưa có**.
**Response**: `{"success": true, "data": [ …`calendar_setting_send_forms` theo `order`… ], "message": ""}`

#### EP-55 — `POST /{id}/create-new-setting-form`

`:1407-1424`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `{id}` | path | int | Có | dùng để đếm số câu hỏi |
| *(nội dung câu hỏi)* | body | mixed | — | truyền `$request` (object) xuống service, **không FormRequest** |

**Chặn**: `count(calendar_setting_send_forms WHERE calendar_id = {id}) >= 100` ⇒ `{"success": false, "message": "質問数の上限（100）を超えるため、これ以上作成できません。"}` HTTP **200** (:1409-1415).
**Response OK**: `{"success": true, "data": <bản ghi mới>, "message": ""}`
> ⚠ Đếm-rồi-tạo, **không có `PlanLimitGuard::rollbackIfOverLimit`** như EP-07/EP-28 ⇒ hai tab bấm cùng lúc vẫn vượt trần 100. Confidence: **Cao**.

#### EP-56 — `POST /{id}/update-setting-form`

`:1426-1435` → `updateSettingForm($request->id, $request->except(['id']), $id)`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `id` | **body** | int (`calendar_setting_send_forms.id`) | Có |
| *(mọi trường khác)* | body | mixed | — |

> ⚠ Trùng tên: `{id}` trên path là **calendar_id**, `id` trong body là **id câu hỏi**. Nguồn nhầm lẫn thường trực.
**Response**: `{"success": true, "data": <setting hoặc []>, "message": ""}`

#### EP-57 — `DELETE /{id}/delete-setting-form`

`:1437-1453`. Tham số `id` (body) = id câu hỏi. Service trả falsy ⇒ `{"success": false, "data": null, "message": "Error"}` (**message tiếng Anh trơ**, :1440-1446). OK ⇒ `{"success": true, "data": <setting>, "message": ""}`.

#### EP-58 — `POST /{id}/sort-setting-form`

`:1455-1464`. Tham số `sortArray` (body, array). Response `{"success": true, "data": null, "message": ""}` — **luôn `true`**.

#### EP-59 / EP-60 / EP-61 — Các trang preview

| Mã | Method@dòng | View | Dữ liệu |
|---|---|---|---|
| EP-60 | `preview` :1889-1898 | `tabs.setting_calendar_tab.preview` | `calendar` (toàn bộ bản ghi) hoặc `[]` |
| EP-59 | `previewTop` :1900-1910 | `tabs.setting_calendar_tab.preview_top` | `calendar` hoặc `[]` |
| EP-61 | `previewForm` :1912-1995 | `tabs.setting_calendar_tab.preview_form` | `settings` (danh sách câu hỏi đã lọc) hoặc `[]` |

Cả ba **đều gọi `checkCalendarBelongBot($id)`** (kiểm tra kép cùng CLC) và trả mảng rỗng nếu sai — cách xử lý an toàn.

**Logic lọc riêng của EP-61** (:1918-1990):
- Chỉ lấy câu hỏi `enable = 1`.
- `options` được giải mã từ JSON; khi `link_friend_information == 3` và trường hồ sơ có `type_data == 1` (select) thì lấy `options_information_friend`; `type_data == 2` thì lấy `options_text_information_friend`.
- `friend_information_id == -6` (都道府県) mà chưa có options ⇒ sinh từ hằng `PROVINCE_DEFAULT` và **ghi ngược vào `$setting->options_information_friend`** (chỉ trên object, không lưu DB).
- Câu hỏi kiểu radio/checkbox mà **mọi option đều thiếu `title` hoặc `value`** ⇒ **bị loại khỏi preview** (:1975-1988).

#### EP-62 — `GET /{id}/booking/last-booking/{lineId}`

`:2208-2215` → `CalendarCourseBookingService::getLastTenBooking($id, $lineId)` (:1442-1448).

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `id` | path | int (calendar) | Có |
| `lineId` | path | int/string (`line_user_id`) | Có |

**Response**: `{"success": true, "data": [ …tối đa 10 đặt chỗ gần nhất… ]}` — **không có khoá `message`**.
> Tên route là `last-booking` (số ít) nhưng service trả 10 bản ghi (`getLastTenBooking`) — sai lệch tên/hành vi.

#### EP-63 — `DELETE /{id}/course/reception-list/delete`

`:403-419` → `CalendarCourseReceptionService::deleteList($request->all())` (:413-…).

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `receptionList` | body | int[] | Có |

**Chặn**: `sum(total_approve) > 0` trên toàn bộ danh sách ⇒ trả 「削除する受付枠の中に「ステータス：予約確定」の予約が1つ以上残っています。受付枠を削除する場合、この受付枠の全ての予約が「ステータス：キャンセル」になっている必要があります。」
**Response lỗi**: `{"success": false, "data": null, "message": "<chuỗi trên>"}` (:405-411) — lại là **so sánh chuỗi JP cứng**.
**Response OK**: `{"success": true, "data": null, "message": ""}`
> ⚠ `receptionList` **không đối chiếu `{id}`** ⇒ xoá hàng loạt khung giờ của bot khác (§5, A-06). Confidence: **Cao**.

#### EP-64 — `GET /{id}/course/reception/{receptionId}/check-delete`

`:2270-2279` → `checkCanDeleteReception($receptionId)`.
**Response**: `{"success": <bool kết quả kiểm tra>, "data": null, "message": ""}`
> ⚠ Ở đây khoá `success` **mang ý nghĩa nghiệp vụ** ("có thể xoá") chứ không phải "gọi API thành công" — mâu thuẫn với quy ước ở 60+ endpoint còn lại. Nguồn lỗi tiềm tàng cho front-end. Confidence: **Cao**.

#### EP-65 — `POST /disable-tooltip`

`:1997-2005`. Không tham số. `UPDATE users SET enable_tooltip_calendar = 0 WHERE id = Auth::id()`.
**Response**: `{"success": true, "data": null, "message": ""}`
> ✅ Endpoint duy nhất trong Nhóm A thao tác trên chính tài khoản đăng nhập — không có rủi ro IDOR.

---

### 2.3 Nhóm B — `/ajax/calendar` (EP-66…EP-82)

Nhóm này dùng quy ước response **khác** Nhóm A: phần lớn trả `{"success": …}` hoặc `{"status": true, …}` **không có** khoá `data`/`message` chuẩn.

Điểm sáng: **10/17 endpoint có gọi `checkCalendarBelongBot($calendarId)`** — bù lại việc thiếu `basic_access`. Điểm tối: 7 endpoint còn lại không kiểm tra gì.

| Endpoint | Có `checkCalendarBelongBot`? |
|---|---|
| EP-66 `ajaxGetDetailCalendar` | ✅ :492 |
| EP-67 `savePolicyCalendar` | ⚠ có, nhưng **vẫn trả dữ liệu khi sai** — xem bên dưới |
| EP-68 `saveCalendarInfo` | ⚠ như EP-67 |
| EP-69 `sendMailCodeAuthDeleteCalendar` | ✅ :659 |
| EP-70 `checkAuthorDeleteCalendar` | ✅ :688 |
| EP-71 `deleteCalendar` | ✅ :720 + lọc `bot_id` ở mọi truy vấn |
| EP-72 `saveSettingNotifyFull` | ✅ :777 |
| EP-73 `getHistorySettingNotifyFullSlot` | ✅ :815 |
| EP-74 `saveCreateSettingRemind` | ✅ :845 |
| EP-75 `getListStepRemind` | ✅ :1072 |
| EP-76 `deleteEventStep` | ❌ **không kiểm tra gì** |
| EP-77 `getDetailEventStep` | ❌ **không kiểm tra gì** |
| EP-78 `getListCourseByCalendar` | ❌ (đọc `$botId` rồi **không dùng**) |
| EP-79 `saveSettingSendMessageEventStep` | ✅ :1242 + kiểm `event.bot_id` |
| EP-80 `deleteItemActionEventStep` | ➖ không kiểm calendar, nhưng **mọi truy vấn đều lọc `bot_id`** |
| EP-81 `deleteItemActionCalendar` | ➖ như EP-80 |
| EP-82 `saveInfoFormBooking` | ➖ không kiểm calendar thuộc bot, nhưng có kiểm `booking.calendar_id == calendar_id` |

#### EP-66 — `GET /ajax/calendar/init-detail/{id}`

`:490-505`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `id` | path | int | Có |

Nếu `checkCalendarBelongBot($id)` đúng ⇒ `$calendar = getById($id)` và gắn thêm `detail_action_full` = `getActionDetailByActionId(action_id_notify_full_slot)`, `detail_action_not_full` = `getActionDetailByActionId(action_id_not_full)`. Sai ⇒ `$calendar = []`.

**Response**: `{"success": true, "calendar": { …toàn bộ `calendar_management` + 2 trường action… } }` hoặc `{"success": true, "calendar": []}`
> ⚠ `success` **luôn `true`** kể cả khi calendar không thuộc bot — front-end phải tự phát hiện mảng rỗng.
> ⚠ Trả **toàn bộ bản ghi**, gồm `google_sheet_access_token`, `code_delete`, `content_policy` — nhưng đã lọc theo bot nên rủi ro giới hạn trong nội bộ bot.

#### EP-67 — `POST /ajax/calendar/save/policy`

`:507-525`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `id` | body | int | Có | `checkCalendarBelongBot($id)` — chỉ dùng để **quyết định có UPDATE hay không** |
| `show_policy` | body | 0/1 | Có | không validate |
| `content_policy` | body | string (HTML) | Có | **không giới hạn độ dài, không lọc HTML** |

**Response**: `{"success": true, "calendar": <toàn bộ bản ghi calendar_management>}`

> 🔴 **IDOR đọc**: dòng `$calendar = $this->calendarService->getById($id);` (:520) nằm **ngoài** khối `if ($exist)` (:514-519) ⇒ dù calendar thuộc bot khác, response **vẫn trả về toàn bộ bản ghi** (kể cả `google_sheet_access_token`, `code_delete` — chính là mã dùng để xác thực xoá lịch ở EP-70/EP-71). Confidence: **Cao**.
> ⚠ `content_policy` là HTML hiển thị cho LINE User trên trang public 「利用規約」 ⇒ nguy cơ **stored XSS** nếu blade in bằng `{!! !!}`. Confidence: **Trung bình** (chưa xác minh blade).

#### EP-68 — `POST /ajax/calendar/save/info`

`:527-577`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `id` | body | int | Có | như EP-67 |
| `calendar_data[line_name]` | body | string | **Có** | rỗng ⇒ `{"success": false, "calendar": "店舗名を入力してください。"}` HTTP **500** (:533-538) |
| `calendar_data[image_calendar]` | body | string / base64 | Có | |
| `calendar_data[image_calendar_top]` | body | string / base64 | Không | `?? null` |
| `calendar_data[update_image]` | body | `'true'`/khác | Có | so sánh `===` **chuỗi**; thiếu key ⇒ `Undefined index` (:560) |
| `calendar_data[update_image_top]` | body | `'true'`/khác | Có | như trên (:564) |
| `calendar_data[url_website]`, `[phone]`, `[address]`, `[access]`, `[business_hours]`, `[business_hours_holiday]`, `[facility]`, `[parking]`, `[payment_method]`, `[number_staff]`, `[description]` | body | string | Có (truy cập trực tiếp) | **không validate**; thiếu key ⇒ `Undefined index` (:540-555) |
| `calendar_data[description_top]` | body | string | Không | `?? null` |
| `calendar_data[enable_top_page]` | body | 0/1 | Có | không validate |

`line_name` được ghi vào **cả hai** cột `store_name` và `line_name` (:541-542).
Ảnh base64 được upload vào `{FOLDER_MEDIA}media/images/{bot.admin_id}/{botId}/calendar_new/` (ảnh cửa hàng) và `…/calendar_new_top/` (ảnh trang top) (:560-567).

**Response OK**: `{"success": true, "calendar": <toàn bộ bản ghi>}`
> 🔴 **Cùng lỗi IDOR đọc như EP-67**: `getById($id)` ở :574 nằm ngoài `if ($exist)` (:570-573).
> ⚠ 15 khoá của `calendar_data` được truy cập bằng `[...]` trực tiếp ⇒ client thiếu bất kỳ khoá nào đều gây `Undefined index` (PHP 7.2: notice + giá trị null, ghi `null` vào DB). Confidence: **Cao**.
> ⚠ Không giới hạn kích thước base64 ở đây (khác EP-10 vốn có `Base64ImageSize(10240)`).

#### EP-69 — `POST /ajax/calendar/send-mail/delete`

`:645-679`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `id` | body | int | Có |

**Xử lý**: lấy email của `getCurrentUser()`, sinh `Str::random(10)` → `checkRandomStringCodeDeleteLesson()` (đảm bảo không trùng), gửi mail `SendAuthCode::SendAuthCodeDeleteCalendar($email, $code)`, rồi **lưu mã vào `calendar_management.code_delete`** (:667).

**Response OK**: `{"success": true, "code": "<mã 10 ký tự>", "message": "Send mail success"}`
**Lỗi**: `{"success": false, "message": "Calendar does not exist"}` hoặc `{"success": false, "message": "<exception message>"}` (**tiếng Anh**, :675-678)

> 🔴 **Mã xác thực bị trả thẳng trong response JSON** (`'code' => $code`, :670). Toàn bộ mục đích của bước "gửi mã qua email để xác nhận xoá" bị vô hiệu: JS đã có mã ngay lập tức, không cần mở hộp thư. Confidence: **Cao**.
> ⚠ `code_delete` lưu **plaintext** trong DB và bị EP-67/EP-68 trả ra qua IDOR ⇒ kẻ tấn công lấy được mã của lịch bot khác rồi gọi EP-71.
> ⚠ Không rate limit ⇒ spam email.

#### EP-70 — `POST /ajax/calendar/check-author/delete`

`:681-713`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `id` | body | int | Có |
| `code` | body | string | Có |

Kiểm tra `CalendarManagement WHERE id = ? AND bot_id = getBotId() AND code_delete = ?`.
**Response OK**: `{"success": true, "message": "auth calendar success"}`
**Sai mã**: `{"success": false, "message": "認証コードが間違っています。"}` (:702-705)
**Không tồn tại**: `{"success": false, "message": "Calendar does not exist"}` (**tiếng Anh**)
> ⚠ Không giới hạn số lần thử ⇒ brute-force mã 10 ký tự (không thực tế nhưng vẫn là thiếu sót).

#### EP-71 — `POST /ajax/calendar/action/delete` — XOÁ HỆ THỐNG ĐẶT LỊCH

`:715-771`. **Endpoint phá huỷ nhất của FA-019 phía Admin.**

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `id` | body | int | Có |
| `code` | body | string | Có — phải khớp `code_delete` |

**Chuỗi xoá** (theo thứ tự thực thi):

| # | Bảng | Kiểu xoá | Dòng |
|---|---|---|---|
| 1 | `calendar_management` (WHERE `id` AND `bot_id`) | soft delete | :738 |
| 2 | `calendar_course` (WHERE `calendar_id`) | soft delete | :740 |
| 3 | `calendar_course_receptions` (WHERE `course_id` IN …) | **forceDelete** | :741 |
| 4 | `calendar_course_booking_history_actions` (theo từng booking) | **forceDelete** | :745 |
| 5 | `mobile_notify` (`lesson_booking_id`, type calendar_lesson, `is_confirm=0`, `status=1`) | soft delete | :746-751 |
| 6 | `calendar_course_bookings` (WHERE `calendar_id`) | **forceDelete** | :754 |
| 7 | `calendar_setting_notify_full_history` | soft delete | :755 |
| 8 | `calendar_setting_send_forms` | **forceDelete** | :756 |
| 9 | `calendar_setting_send_messages` | **forceDelete** | :757 |
| 10 | `event_step`, `event_step_time` (theo `events.booking_calendar_id`, `type = 4`) | soft delete | :758-765 |
| 11 | `events` (`booking_calendar_id`, `type = 4`) | soft delete | :766 |
| 12 | `recountAppBadgeNotify(getBotId())` | — | :767 |

**Response OK**: `{"success": true, "message": "delete calendar success"}`
**Lỗi**: `{"success": false, "message": "Calendar does not exist"}` hoặc `{"success": false, "message": "認証コードが間違っています。"}`

> 🔴 **Không có `DB::transaction`** cho 12 thao tác xoá liên hoàn ⇒ lỗi giữa chừng để lại dữ liệu mồ côi (ví dụ đã forceDelete `calendar_course_receptions` nhưng chưa xoá `calendar_course_bookings`). Confidence: **Cao** (:715-771).
> 🔴 **Trộn soft delete và forceDelete**: toàn bộ **lịch sử đặt chỗ và dữ liệu thanh toán (`calendar_course_bookings`, kèm `charge_id`, `payment_amount`) bị xoá vĩnh viễn**, trong khi bản ghi cha `calendar_management` chỉ soft delete ⇒ **không thể khôi phục, không thể đối soát kế toán sau khi xoá**. Confidence: **Cao**.
> 🔴 **Không CSRF** (nhóm `/ajax/*`): một trang bên thứ ba có thể ép trình duyệt Admin đang đăng nhập POST tới đây — chỉ thiếu `code`, mà `code` lại lộ qua EP-69/EP-67.
> ⚠ Vòng lặp `foreach ($bookings …)` thực hiện 2 truy vấn/booking (:743-752) — lịch nhiều nghìn đặt chỗ sẽ timeout giữa chừng, kết hợp với việc không có transaction.

#### EP-72 — `POST /ajax/calendar/save-setting/notify-full-slot`

`:773-810`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `id` | body | int | Có | `checkCalendarBelongBot` |
| `is_notify_full_slot` | body | bool / `'false'` | Có | `== false \|\| === 'false'` ⇒ 0, ngược lại 1 (:788) |
| `use_message_notify_full_slot` | body | bool / `"false"` | Có | `=== false \|\| === "false"` ⇒ 0, ngược lại 1 (:800) |
| `message_notify_full_slot` | body | string | Có | không validate độ dài |
| `action_id_notify_full_slot` | body | int | Không | |
| `message_notify_not_full` | body | string | Không | |
| `action_id_not_full` | body | int | Không | |

**Ghi lịch sử**: khi `is_notify_full_slot` đổi giá trị ⇒ INSERT `calendar_setting_notify_full_history` (`calendar_id`, `admin_id`, `admin_name` = `Auth::user()->username`, `bot_id`, `status_old`, `status_current`) (:789-798).

**Response**: `{"success": true, "message": "setting calendar success"}`

> ⚠ `use_message_notify_not_full` bị **hard-code `0`** (:804) — cột này không bao giờ bật được từ UI. Confidence: **Cao**.
> ⚠ Hai tham số cùng ngữ nghĩa dùng **hai kiểu so sánh khác nhau** (`==` lỏng cho cái đầu, `===` chặt cho cái sau) ⇒ hành vi lệch khi client gửi `0` / `"0"`. Confidence: **Cao**.
> ⚠ `$calendar->update(...)` không kiểm tra `$calendar` null (`checkCalendarBelongBot` đã bảo đảm nên thực tế an toàn).
> ⚠ Log ghi nhầm nhãn `'deleteCalendar id: '` (:776) — copy-paste từ `deleteCalendar`.

#### EP-73 — `GET /ajax/calendar/history-setting/notify-full-slot`

`:812-828`. Tham số `id` (query). Trả `CalendarSettingNotifyFullHistory WHERE calendar_id AND bot_id`.
**Response**: `{"success": true, "histories": [ {"calendar_id":…, "admin_id":…, "admin_name":"…", "status_old":0, "status_current":1, …} ]}`
> ✅ Lọc `bot_id` đầy đủ.

#### EP-74 — `POST /ajax/calendar/save-setting/remind`

`:830-913`.

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `id` | body | int (calendar) | Có | `checkCalendarBelongBot` |
| `remindId` | body | int (`events.id`) | Không | tra `events` theo `id + bot_id + booking_calendar_id + type=4`; không thấy ⇒ **tạo `events` mới** (:852-866) |
| `remindStepId` | body | int | Không | **Đọc vào biến `$remindStepId` nhưng KHÔNG dùng ở bất kỳ đâu** (:834) |
| `isRemindAfter` | body | `'true'`/khác | Có | `'true'` ⇒ `is_after_day = 1` (nhắc **sau**), khác ⇒ `0` (nhắc **trước**) (:877) |
| `isRemindBefore` | body | any | Không | **đọc nhưng không dùng** (:837) |
| `startDay` | body | int | Khi `typeRemind == 1` | `before_day`; rỗng ⇒ `0` |
| `startTime` | body | `H:i` | Khi `typeRemind == 1` | `Carbon::createFromTimeString()` — chuỗi sai ⇒ **exception 500** (:871) |
| `typeRemind` | body | `1` = theo ngày / `2` = đếm ngược | Có | (:870-874) |
| `startHourse` / `startMinute` | body | int | Khi `typeRemind == 2` | ghép thành `"H:M"` **không zero-pad** ⇒ `time_send` có thể là `"9:5"` (:873) |
| `action_id` | body | int | Không | |

**Ghi DB**: INSERT `event_step` với `type = 4`, `is_use_filter_course = 0`, `is_use_message = 1`, `send_message_course` = template mặc định (`getMessageTemplateRemind(1)` cho nhắc trước / `(2)` cho nhắc sau, :2217-2239).
Sau đó `addActionRemindNew($eventStepId, $calendarId)` (:918-1043) sinh hàng loạt `event_step_time` cho **mọi đặt chỗ đang ở `SB_BOOKING_APPROVE` / `SB_BOOKING_ADMIN_BOOK` / `SB_REQUEST_BOOKING_CANCEL`** của lịch.

**Response**: `{"success": true, "message": "setting remind success", "eventStepId": <id>}`

> 🔴 **`remindStepId` không được dùng ⇒ method LUÔN `insertGetId`, không bao giờ UPDATE.** Bấm 「保存」 nhiều lần trên cùng một bước nhắc sẽ **tạo thêm bản ghi `event_step` mới mỗi lần**, mỗi bản ghi lại sinh `event_step_time` cho toàn bộ đặt chỗ ⇒ **khách nhận tin nhắc trùng lặp nhiều lần**. Confidence: **Cao** (:834, :877-906).
> ⚠ `time_send` không zero-pad: `startHourse=9, startMinute=5` ⇒ `"9:5"`. Về sau `explode(':', time_send)` vẫn parse được, nhưng `Carbon::parse($date . ' ' . '9:5')` và các phép so sánh chuỗi dễ sai. Confidence: **Trung bình**.
> ⚠ `addActionRemindNew` bọc mọi lỗi trong `try/catch` chỉ ghi log ⇒ tin nhắc có thể **thiếu âm thầm** cho một phần đặt chỗ (:1029-1042).
> ⚠ Không giới hạn số bước nhắc.

#### EP-75 — `GET /ajax/calendar/get-list-step-remind`

`:1069-1160`. Tham số `calendar_id` (query).

**Side effect quan trọng**: nếu chưa có `events` (`booking_calendar_id`, `type = 4`) thì method **tự tạo** 1 `events` + **2 `event_step` mặc định** (:1085-1119):
- nhắc **sau** 1 ngày lúc `10:00`, nội dung `getMessageTemplateRemind(2)`;
- nhắc **trước** 1 ngày lúc `10:00`, nội dung `getMessageTemplateRemind(1)`.

**Sắp xếp**: `listStepBefore` sắp theo (loại nhắc, `before_day` giảm dần đảo ngược, `time_send`); `listStepAfter` theo (loại nhắc, thời lượng tăng dần) (:1121-1152).

**Response**
```json
{ "status": true,
  "listStepBefore": [ { "id": 71, "event_id": 9, "is_after_day": 0, "type": 4, "before_day": 1,
                        "time_send": "10:00", "action_id": null, "type_remind": 1,
                        "send_message_course": "{name}様\n\nご予約の【1日前】…", "is_use_message": 1 } ],
  "listStepAfter": [ … ],
  "remindId": 9 }
```
> ⚠ Endpoint **GET nhưng ghi DB** — vi phạm nguyên tắc idempotent, và vì `/ajax/*` miễn CSRF nên một thẻ `<img src>` cũng đủ kích hoạt việc tạo dữ liệu. Confidence: **Cao**.

#### EP-76 — `POST /ajax/calendar/delete-step-remind`

`:1045-1055`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `step_id` | body | int (`event_step.id`) | Có | **KHÔNG kiểm tra gì cả** |

**Xử lý**: `EventStep::where('id', $stepId)->delete()` + `EventStepTime::where('event_step_id', $stepId)->where('status', 0)->delete()`.
**Response**: `{"status": true}` — **luôn `true`**.

> 🔴 **IDOR ghi**: không kiểm tra `bot_id`, không kiểm tra `event_step` thuộc lịch nào, không kiểm tra `type = 4`. Gửi `step_id` tăng dần ⇒ **xoá bước gửi tin của bất kỳ bot nào và bất kỳ tính năng nào dùng `event_step`** (kịch bản, remind sự kiện…), không chỉ FA-019. Đây là lỗ hổng có phạm vi ảnh hưởng **vượt ra ngoài** tính năng đặt lịch. Confidence: **Cao** (:1045-1055).

#### EP-77 — `GET /ajax/calendar/get-detail-event-step`

`:1162-1194`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `stepId` | query | int | Có | **KHÔNG kiểm tra gì**; `$step` null ⇒ `$step->action_id` gây **500** (:1166-1167) |

Bổ sung `course_of_step` (tên hiển thị các khoá học trong `course_ids`, lấy `system_name` hoặc 10 ký tự đầu `course_name`) và `detail_action` (`getActionDetailByActionId`).

**Response**: `{"status": true, "step": { …bản ghi `event_step` + `course_ids` (mảng int) + `course_of_step` + `detail_action`… }}`
> 🔴 **IDOR đọc**: đọc được nội dung tin nhắn và cấu hình action của bất kỳ `event_step` nào trong hệ thống. Confidence: **Cao**.

#### EP-78 — `GET /ajax/calendar/get-list-course-by-calendar`

`:1057-1067`.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `calendar_id` | query | int | Có | **không kiểm tra thuộc bot**; biến `$botId = getBotId()` được gán nhưng **không dùng** (:1058) |

Truy vấn `calendar_course WHERE calendar_id = ? AND booking_page_display = BOOKING_DISPLAY_ON`, chỉ lấy 3 cột `id`, `course_name`, `system_name`.
**Response**: `{"status": true, "courses": [ {"id": 45, "course_name": "体験レッスン", "system_name": "体験"} ]}`
> ⚠ IDOR đọc (mức thấp — chỉ tên khoá học). Đối chiếu: endpoint **cùng tên** ở phía LIFF (`EP-P03` trong `api-spec-public.md`) dùng `select('*')` trả toàn bộ cột; bản Admin này lại **giới hạn 3 cột** — nghịch lý: bản public lộ nhiều hơn bản nội bộ. Confidence: **Cao**.

#### EP-79 — `POST /ajax/calendar/save-setting-send-message-event-step`

`:1226-1374`.

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `calendar_id` | body | int | Có | `checkCalendarBelongBot` (:1242) |
| `event_step_id` | body | int | Có | UPDATE có thêm điều kiện `event_id = $event->id` ⇒ **có ràng buộc sở hữu gián tiếp** (:1264) |
| `is_use_filter_course` | body | `'true'`/khác | Có | so sánh chuỗi ⇒ 1/0 (:1228) |
| `send_message_course` | body | string | Có | nội dung tin nhắc, **không giới hạn độ dài** |
| `is_use_message` | body | `'true'`/khác | Có | ⚠ **đảo ngược**: `'true'` ⇒ lưu `0`, khác ⇒ `1` (:1267) |
| `action_id` | body | int | Không | |
| `course_ids` | body | int[] | Không | `implode(',')` → cột `course_ids` (chuỗi CSV) (:1240) |
| `type_remind` | body | `1`/`2` | Có | |
| `start_day` | body | int | Khi `type_remind = 1` | `before_day`; khi `type_remind = 2` ⇒ ghi **NULL** (:1270) |
| `start_time` | body | `H:i` | Khi `type_remind = 1` | |
| `start_hour` / `start_minute` | body | int | Khi `type_remind = 2` | ghép `"H:M"`, không zero-pad (:1261) |

**Đồng bộ lại lịch gửi** (:1274-1367): duyệt mọi `event_step_time` của bước này (`bot_id` khớp, `status = 0`):
- booking hoặc reception không còn ⇒ bỏ qua;
- tính lại `sent_date_time` theo `type_remind` (theo ngày / đếm ngược từ `start_time` hoặc `end_time`);
- nhắc-trước mà thời điểm gửi **muộn hơn** giờ bắt đầu ⇒ **xoá** bản ghi;
- lọc khoá học không khớp `course_ids` ⇒ **xoá**;
- thời điểm gửi đã qua ⇒ **xoá**; còn lại ⇒ UPDATE `sent_date_time`.
Cuối cùng gọi `addActionRemindNew()` cho phần đặt chỗ **chưa** có lịch gửi (:1358-1367).

**Response**: `{"status": true}`
**Lỗi**: `{"success": false, "message": "Calendar does not exist"}` hoặc `{"success": false, "message": "Event does not exist"}` (:1243-1256)

> ⚠ **Response thành công dùng khoá `status`, response lỗi dùng khoá `success`** — trong cùng một method (:1244 vs :1372). Front-end phải kiểm tra cả hai. Confidence: **Cao**.
> ⚠ `is_use_message` bị đảo nghĩa so với tên biến (`'true'` ⇒ `0`) (:1267) — nợ kỹ thuật dễ gây lỗi khi bảo trì.
> ⚠ Không transaction cho chuỗi cập nhật/xoá `event_step_time`.

#### EP-80 — `POST /ajax/calendar/delete-item-action-event-step`

`:1196-1224`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `action_detail_id` | body | int | Có |
| `action_id` | body | int | Có |
| `event_step_id` | body | int | Có |

Xoá `filter_v2` (`parent_type = 'modal_action'`, `parent_id = action_detail_id`, `bot_id`) và `action_detail` (`action_id`, `id`, `bot_id`). Nếu action không còn detail nào ⇒ set `event_step.action_id = null` (có lọc `bot_id`).

**Response**: `{"status": true, "action_id": <id hoặc null>}`
> ⚠ `ActionDetail::where('action_id', $actionId)->exists()` ở :1211 **không lọc `bot_id`** (trong khi `deleteItemActionCalendar` ở EP-81 thì có, :2126) ⇒ nếu bot khác còn detail của cùng `action_id`, hệ thống sẽ **không** gỡ liên kết. Bất nhất giữa hai method gần như song sinh. Confidence: **Cao**.
> ⚠ Log ghi nhãn `'delete action deleteItemActionEventStep success'` — cùng chuỗi này được dùng ở EP-81 (:2185), không phân biệt được nguồn khi debug.

#### EP-81 — `POST /ajax/calendar/delete-item-action-calendar`

`:2115-2189`.

| Tên | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `action_detail_id` | body | int | Có |
| `action_id` | body | int | Có |
| `calendar_id` | body | int | Có |
| `type_action` | body | enum | Có |

Khi action hết detail, gỡ liên kết theo `type_action` (mọi UPDATE đều lọc `bot_id`):

| `type_action` | Bảng | Cột đặt `null` |
|---|---|---|
| `setting_message_booking` | `calendar_setting_send_messages` (moment `booking`) | `setting_action_id` |
| `setting_message_booking_request` | ↑ | `setting_action_request` |
| `setting_message_booking_approve` | ↑ | `setting_action_approve` |
| `setting_message_booking_deny` **hoặc** `setting_message_booking_reject` | ↑ | `setting_action_reject` |
| `setting_message_cancel_booking` | `calendar_setting_send_messages` (moment `cancel`) | `setting_action_id` |
| `setting_message_cancel_request` | ↑ | `setting_action_request` |
| `setting_message_cancel_approve` | ↑ | `setting_action_approve` |
| `setting_message_cancel_reject` | ↑ | `setting_action_reject` |
| `calendar_notify_full` | `calendar_management` | `action_id_notify_full_slot` |
| `calendar_notify_not_full` | `calendar_management` | `action_id_not_full` |

**Response**: `{"status": true, "action_id": <id hoặc null>}`
> ⚠ Hai giá trị `setting_message_booking_deny` và `…_reject` cùng trỏ về một cột — dấu vết của việc đổi tên chưa dọn (:2148-2153).
> ⚠ `type_action` không khớp nhánh nào ⇒ **im lặng không làm gì**, vẫn trả `status: true`.

#### EP-82 — `POST /ajax/calendar/save-info-form-booking`

`:2498-2597`. Admin sửa câu trả lời form 「お客様情報」 của một đặt chỗ.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `calendar_id` | body | int | Có | dùng trong `where` cùng `id` (:2503) |
| `id` | body | int (`calendar_course_bookings.id`) | Có | ✅ **có kiểm tra `booking.calendar_id == calendar_id`** — nhưng **không** kiểm tra calendar thuộc bot |
| `form_info` | body | **chuỗi JSON** | Có | `json_decode($dataFormInfo, true)`; JSON hỏng ⇒ `null` ⇒ vòng lặp bị bỏ qua nhưng **vẫn ghi `friend_info = "[]"`** (xoá sạch dữ liệu cũ) (:2507, :2641) |

Mỗi phần tử `form_info`: `{question, value, form_type, friend_information_id, recording_time, …}`.

**Xử lý mỗi phần tử**:
- có `question` ⇒ đưa vào `dataFormSaveBooking` (sẽ ghi vào `friend_info`);
- `value` rỗng / `form_type == FORM_TYPE_CHECKBOX` / `friend_information_id` rỗng / `recording_time == 1` ⇒ **bỏ qua bước đồng bộ hồ sơ**;
- có `line_user_id` ⇒ **ghi đè hồ sơ bạn bè** và ghi `recordFriendInfoHistory(..., '7001')`:

| `friend_information_id` | Cột đích |
|---|---|
| `-1` | `line_user.view_name` |
| `-2` | `line_user.phone_number` |
| `-3` | `line_user.email` |
| `-4` | `line_user.birthday` (+ `settingEventTimeFriendInfo(… 'd_4' …)`) |
| `-6` | `line_user.province` |
| khác (> 0) | `friend_information_values.value` (+ `friend_info_option_id` khi `type_data == 1`; tăng `total_user_has_value` khi tạo mới; `settingEventTimeFriendInfo` khi `type_data == TYPE_DATA_DATETIME`) |

Cuối cùng: UPDATE `calendar_course_bookings.friend_info = json_encode($dataFormSaveBooking)` và `CalendarGoogleSheetService::updateFriendInfo($id)` (:2641-2647).

**Response**: `{"success": true, "detailBooking": <toàn bộ bản ghi booking>, "dataFormSaveBooking": [...], "message": ""}`

> ⚠ Khi `booking` không tồn tại hoặc `calendar_id` không khớp, method **không làm gì nhưng vẫn trả `success: true`** với `detailBooking: null` (:2503, :2649-2654).
> ⚠ `FriendInformationValue::where('line_id', …)` **không lọc `bot_id`** khi tìm giá trị cũ (:2617-2619) — cùng kiểu thiếu sót đã ghi nhận ở EP-P06 phía LIFF (`api-spec-public.md` :711-714).
> ⚠ **Không kiểm tra calendar thuộc bot** ⇒ chỉ cần cặp (`id`, `calendar_id`) hợp lệ là sửa được đặt chỗ và **ghi đè hồ sơ bạn bè của bot khác**. Confidence: **Cao**.
> ⚠ `form_info` là **chuỗi JSON lồng trong body** thay vì cấu trúc JSON tự nhiên — bất nhất với EP-38 (`formQuestion` là mảng thật).

---

## 3. Middleware & phân quyền

### 3.1 Bảng tóm tắt

| Middleware | Class | Hành vi thực tế (đọc từ source) | Áp dụng cho |
|---|---|---|---|
| `NotifyChatworkRequestTimeSlow` | `app/Http/Middleware/NotifyChatworkRequestTimeSlow.php` | Bao ngoài toàn bộ `web.php:81` — cảnh báo request chậm qua Chatwork | Nhóm A + B |
| `LogRequestMultipart` | `app/Http/Middleware/LogRequestMultipart.php` | Ghi log request multipart (`web.php:835`) | Nhóm A + B |
| `basic_access` | `BasicAccess.php` | Yêu cầu `Auth::check()` và `role ∈ {-1, 0, 1, 2}`; nếu không ⇒ `redirect()->route('logout')`. Khi là **bot được mời (Staff)**: lấy danh sách route được phép qua `getRouterBotInvite()`, route hiện tại không nằm trong danh sách ⇒ redirect `adminIndex` kèm lỗi 「この権限は許可されていません。」. Ghi `user_access_bot` (nhật ký truy cập Staff, 1 bản ghi/ngày). | **Chỉ Nhóm A** |
| `is_expire` | `IsExpire.php` | Chặn khi bot hết hạn hợp đồng ⇒ redirect `pointSettings` / trang thanh toán. Có cửa hậu bảo trì: `MAINTAIN_SERVE = true\|'SOS'` chỉ cho 4 user id cứng (`29, 152543, 3710, 151876`) đi tiếp, còn lại redirect `maintain`. **Bỏ qua hoàn toàn** nếu `env('ENABLE_PAYPAL')` falsy. | **Chỉ Nhóm A** |
| `check_remember_token` | `CheckRememberToken.php` | So `session('remember_token')` với `users.remember_token_reset_pass`; lệch ⇒ logout + invalidate session. Với request AJAX trả JSON 「ログイン情報が変更されましたので、再度ログインしてください。」 (kèm **6 khoá đồng nghĩa**: `result`, `status`, `success`, `message`, `msg`, `errors`) — **HTTP 200**, không phải 401. | Nhóm A + B |
| `https_protocol` | `HttpsProtocol.php` | **NO-OP** — toàn bộ thân hàm đã bị comment (:17-20), chỉ `return $next($request)` | Nhóm A |
| `check_login` | `CheckLogin.php` | Chỉ kiểm `Auth::check()`. **Không có `else`** ⇒ khi chưa đăng nhập, middleware trả `null` ⇒ Laravel phát HTTP **200 với body rỗng**, không redirect, không 401. | **Chỉ Nhóm B** |
| `checkLessonCalendarInBot` | `CheckLessonCalendarBelongToBot.php` | Lấy `$request->route('id')`; thiếu ⇒ redirect `calendar.index`; `CalendarManagement WHERE id AND bot_id = getBotId()` rỗng ⇒ redirect `calendar.index`. **Redirect im lặng, không thông báo lỗi** (các nhánh trả JSON 500 đã bị comment :22-23, :28-29). | EP-33…EP-64 |

### 3.2 Phân quyền Staff

- **Không có** bất kỳ lệnh `checkHasPermission(...)` nào trong `CalendarManagementController` hay `SettingPaymentCalendarController`. Kiểm chứng: `grep -n "checkHasPermission" app/Http/Controllers/Basic/CalendarManagementController.php` ⇒ **0 kết quả**.
- Phân quyền Staff cho FA-019 **hoàn toàn dựa vào `BasicAccess` + `getRouterBotInvite()`** — tức là dựa trên **tên route** (`calendar.index`, `calendar.detail`, …), không dựa trên hành động.
- Hệ quả: **Nhóm B (`/ajax/calendar/*`) hoàn toàn nằm ngoài cơ chế này** vì không có `basic_access`. Một Staff bị cấm route `calendar.index` **vẫn gọi được** EP-71 (xoá hệ thống đặt lịch), EP-74 (cấu hình remind), EP-67/EP-68 (sửa 利用規約 và 店舗情報). Confidence: **Cao**.
- Đối chiếu `api-spec-public.md` §0.2: phía API app di động có đúng **1/15** endpoint gọi `checkHasPermission`. Phía web Admin là **0/82**. Cùng một khoảng trống phân quyền, thể hiện ở cả ba lớp.

### 3.3 CSRF

| Nhóm | CSRF | Bằng chứng |
|---|---|---|
| Nhóm A (`/basic/calendar-management/*`) | ✅ **Có** — nằm trong middleware group `web`, không khớp pattern miễn trừ nào | `Kernel.php:34-42`, `VerifyCsrfToken.php:14-40` |
| Nhóm B (`/ajax/calendar/*`) | ❌ **Không** — khớp pattern `'/ajax/*'` | `VerifyCsrfToken.php:16` |

---

## 4. Ma trận endpoint ↔ màn hình

| Màn hình | Tên | Endpoint sử dụng |
|---|---|---|
| SCR-LSN-01 | 「レッスン予約（一覧）」 | EP-25 (view), EP-26 (dữ liệu), EP-29 (sửa), EP-30 (sắp xếp), EP-65 (tắt tooltip) |
| SCR-LSN-02 | Trang giới thiệu & tạo lịch mới | EP-27 (view), EP-28 (tạo) |
| SCR-LSN-03 | Đăng ký khoá học đầu tiên | EP-31 (view), EP-32 (lưu) |
| SCR-LSN-04 | Chi tiết lịch — khung & tab bar | EP-33 (view) |
| SCR-LSN-05 | Tab 「本日／新着の予約」 | EP-03 (danh sách), EP-37 (chi tiết theo slot), EP-42 (đổi trạng thái), EP-43 (xoá), EP-44 (lịch sử), EP-24 (hoàn tiền), EP-82 (sửa câu trả lời form) |
| SCR-LSN-06 | Tab 「予約カレンダー」 | EP-40 (danh sách chế độ 一覧), EP-34 (khoá học + khung giờ), EP-41 (danh sách khung giờ), EP-35 (tạo khung giờ), EP-36/EP-39 (chi tiết + đặt chỗ trong khung), EP-46 (sửa), EP-47 (xoá 1), EP-63 (xoá nhiều), EP-64 (kiểm tra xoá), EP-38 (đặt hộ), EP-62 (đặt chỗ gần nhất), EP-49/EP-50/EP-51 (CSV) |
| SCR-LSN-07 | 「削除済み予約」 | EP-45 |
| SCR-LSN-08 | Tab 「コース設定」 | EP-04 (danh sách), EP-05 (bật/tắt hiển thị), EP-06 (sắp xếp), EP-15 (xoá), EP-16 (kiểm tra trước khi xoá), EP-34 |
| SCR-LSN-09 | Chi tiết khoá học | EP-48 (view), EP-07 (tạo), EP-08 (đọc), EP-10 (cập nhật), EP-09 (tin nhắn thông báo), EP-11 (xoá ảnh), EP-12 (init action), EP-13 (xoá item action), EP-14 (init filter) |
| SCR-LSN-10 | Tab 「全体設定」 — sidebar | EP-66 |
| SCR-LSN-11 | Hub 「予約・キャンセルのメッセージ…」 | EP-52 |
| SCR-LSN-12 | 「予約時の各種設定」 | EP-52 (đọc), EP-53 (lưu), EP-81 (xoá item action) |
| SCR-LSN-13 | 「予約キャンセル時の各種設定」 | EP-52, EP-53, EP-81 |
| SCR-LSN-14 | 「予約前後に送るリマインドメッセージ」 | EP-75 (danh sách bước), EP-74 (tạo bước), EP-77 (chi tiết), EP-79 (lưu tin nhắn), EP-76 (xoá bước), EP-80 (xoá item action), EP-78 (chọn khoá học) |
| SCR-LSN-15 | 「空き枠通知受け取り設定」 | EP-66 (đọc), EP-72 (lưu), EP-73 (lịch sử), EP-81 (xoá item action) |
| SCR-LSN-16 | 「予約時のお客様への質問項目」 | EP-54 (đọc), EP-55 (thêm), EP-56 (sửa), EP-57 (xoá), EP-58 (sắp xếp), EP-22 (trường hồ sơ bạn bè), EP-23 (category) |
| SCR-LSN-17 | 「予約ページの表示設定」 | EP-18 (đọc), EP-19 (lưu), EP-17 (filter) |
| SCR-LSN-18 | 「トップ画面設定」 | EP-66 (đọc), EP-68 (lưu) |
| SCR-LSN-19 | 「店舗・ビジネス情報」 | EP-66 (đọc), EP-68 (lưu) |
| SCR-LSN-20 | 「利用規約」 | EP-66 (đọc), EP-67 (lưu) |
| SCR-LSN-21 | 「Googleスプレッドシート連携」 | EP-33 (sinh auth URL), EP-01 (callback OAuth), EP-02 (ngắt liên kết) |
| SCR-LSN-22 | 「予約システムの削除」 | EP-69 (gửi mã), EP-70 (kiểm mã), EP-71 (xoá) |
| SCR-LSN-23 | Tab 「決済連携」 | EP-21 (khởi tạo), EP-20 (lưu) |
| SCR-LSN-24 | Preview trang top | EP-59 |
| SCR-LSN-25 | Preview thông tin cửa hàng | EP-60 |
| SCR-LSN-26 | Preview form câu hỏi | EP-61 |

**Endpoint không gắn với màn hình cụ thể nào**: không có — cả 82 endpoint đều có màn hình tương ứng.

---

## 5. Cảnh báo bảo mật

Xếp theo mức nghiêm trọng giảm dần. Mã `A-xx` để phân biệt với `S-xx` của `api-spec-public.md`.

| # | Mức | Lỗ hổng | Endpoint | Bằng chứng | Confidence |
|---|---|---|---|---|---|
| A-01 | 🔴 Nghiêm trọng | **Nhóm B thiếu `basic_access` + thiếu CSRF.** 17 endpoint (gồm **xoá hệ thống đặt lịch**, sửa 利用規約/店舗情報, cấu hình remind) chỉ được che bởi `check_login` — không kiểm tra vai trò, không kiểm tra route-permission của Staff, không chặn hợp đồng hết hạn, và nằm trong `$except` của CSRF | EP-66…EP-82 | `routes/web.php:2485`, `VerifyCsrfToken.php:16`, `Kernel.php:34-42` | Cao |
| A-02 | 🔴 Nghiêm trọng | **IDOR ghi + mass assignment trên `POST /{id}/edit`.** Route nằm ngoài `checkLessonCalendarInBot`; `editCalendar` = `where('id',$id)->update($request->all() trừ 'id')` **không lọc `bot_id`, không validate trường nào** ⇒ sửa tuỳ ý bản ghi `calendar_management` của bot khác | EP-29 | `CalendarManagementController.php:154-163`, `CalendarManagementService.php:88-93`, `CalendarManagementRepository.php:35-38`, `routes/web.php:1524` | Cao |
| A-03 | 🔴 Nghiêm trọng | **IDOR ghi trên cấu hình thanh toán.** `calendar_id` lấy thẳng từ body, không `checkCalendarBelongBot`, route ngoài CLC ⇒ tắt thanh toán hoặc chuyển sang môi trường test cho lịch của bot khác (khách đặt chỗ mà không bị thu tiền) | EP-20 | `SettingPaymentCalendarController.php:151-211`, `routes/web.php:1505` | Cao |
| A-04 | 🔴 Nghiêm trọng | **IDOR xoá `event_step` toàn hệ thống.** `step_id` không kiểm `bot_id`, không kiểm `type`, không kiểm chủ sở hữu ⇒ xoá bước gửi tin của **bất kỳ bot và bất kỳ tính năng nào** dùng `event_step` (kịch bản, remind sự kiện), không giới hạn ở FA-019 | EP-76 | `:1045-1055` | Cao |
| A-05 | 🔴 Nghiêm trọng | **Mã xác thực xoá lịch bị trả trong response JSON** (`'code' => $code`) và lưu plaintext ở `calendar_management.code_delete`; mã này còn rò ra ngoài qua A-07 ⇒ toàn bộ "xác thực 2 bước bằng email" trước khi xoá hệ thống đặt lịch là **hình thức** | EP-69 → EP-71 | `:645-679` (`:670`), `:715-771` | Cao |
| A-06 | 🔴 Nghiêm trọng | **`checkLessonCalendarInBot` chỉ kiểm `{id}` calendar, không kiểm id con.** `receptionId`, `bookingId`, `courseId`, `receptionList`, `selectedItems`, `courseList` đều do client gửi và **không được đối chiếu với calendar `{id}`** ⇒ chỉ cần có 1 calendar hợp lệ của mình là thao tác được lên khung giờ / đặt chỗ / khoá học của bot khác (đọc, sửa, xoá, xuất CSV) | EP-36, EP-38, EP-42, EP-43, EP-44, EP-46, EP-47, EP-50, EP-63 | `CheckLessonCalendarBelongToBot.php:20-30`; ví dụ `CalendarCourseBookingService.php:758`, `CalendarCourseReceptionService.php:281`, `:306`, `:415` | Cao |
| A-07 | 🟠 Cao | **IDOR đọc do `getById()` nằm ngoài `if ($exist)`.** Hai method lưu cấu hình vẫn trả **toàn bộ bản ghi `calendar_management`** của calendar không thuộc bot — gồm `google_sheet_access_token`, `code_delete`, `content_policy` | EP-67, EP-68 | `:514-521`, `:570-575`, `CalendarManagementService.php:95-98` | Cao |
| A-08 | 🟠 Cao | **IDOR đọc/ghi cấu hình hiển thị trang đặt.** Hai route `{calendarId}` nằm ngoài CLC, service chỉ `findById()` không lọc bot; EP-18 trả **toàn bộ bản ghi** `calendar_management` | EP-18, EP-19 | `:1826-1868`, `CalendarManagementService.php:166-180`, `routes/web.php:1502-1503` | Cao |
| A-09 | 🟠 Cao | **IDOR ghi trên hoàn tiền.** `booking_id` không đối chiếu bot; với `refundType != 'now'` **không gọi cổng thanh toán** mà vẫn set `payment_status = SP_REFUND` + ghi lịch sử ⇒ đánh dấu hoàn tiền cho đặt chỗ của bot khác. Cũng **không kiểm `payment_status` hiện tại** ⇒ hoàn tiền lặp | EP-24 | `:2016`, `:2081-2100` | Cao |
| A-10 | 🟠 Cao | **File CSV chứa PII ghi vào `public/export/`** với tên đoán được (`{tên_khoá_học}{timestamp}.csv`), **không có cơ chế dọn**, phục vụ trực tiếp qua web không cần đăng nhập. CSV đặt chỗ chứa tên khách, mọi câu trả lời form, số tiền, trạng thái thanh toán | EP-49, EP-50 | `CalendarCourseService.php:301-311`, `CalendarCourseBookingService.php:1154-1291` | Cao |
| A-11 | 🟠 Cao | **IDOR đọc `event_step`.** `stepId` không kiểm bot ⇒ đọc nội dung tin nhắn nhắc, `action_id`, `course_ids` của bất kỳ bước gửi tin nào trong hệ thống | EP-77 | `:1162-1194` | Cao |
| A-12 | 🟠 Cao | **Bỏ qua toàn bộ validation khi tạo khoá học qua `POST /course/store`.** EP-32 không dùng FormRequest, không kiểm trần 200 khoá học, không kiểm hạn mức gói free, `calendar_id` do client gửi — trong khi EP-07 (cùng chức năng) kiểm đủ | EP-32 vs EP-07 | `:175-184` vs `:1536-1600` | Cao |
| A-13 | 🟠 Cao | **Ghi đè hồ sơ bạn bè không kiểm bot.** EP-82 chỉ kiểm `booking.calendar_id == calendar_id`, không kiểm calendar thuộc bot ⇒ sửa `line_user.view_name/phone_number/email/birthday/province` và `friend_information_values` của bạn bè thuộc bot khác | EP-82 | `:2503`, `:2588-2640` | Cao |
| A-14 | 🟡 Trung bình | **Không transaction cho thao tác xoá 12 bảng liên hoàn** ở EP-71; trộn soft delete với **forceDelete** trên `calendar_course_bookings` / `calendar_course_receptions` / `calendar_setting_*` ⇒ mất vĩnh viễn lịch sử thanh toán, không đối soát được, dữ liệu mồ côi khi lỗi giữa chừng | EP-71 | `:715-771` | Cao |
| A-15 | 🟡 Trung bình | **`GET` gây ghi DB.** EP-75 tự tạo `events` + 2 `event_step` khi chưa có; kết hợp miễn trừ CSRF của `/ajax/*` ⇒ một thẻ `<img src="…get-list-step-remind?calendar_id=N">` cũng kích hoạt tạo dữ liệu | EP-75 | `:1085-1119` | Cao |
| A-16 | 🟡 Trung bình | **Rủi ro LFI/SSRF ở import CSV**: `fopen($request['file'], "r")` — nếu tham số `file` đến dưới dạng chuỗi (không phải file upload), `fopen` mở đúng đường dẫn/URL đó và nội dung được parse như CSV | EP-51 | `CalendarCourseService.php:357` | Trung bình |
| A-17 | 🟡 Trung bình | **Không giới hạn khối lượng ghi.** EP-35 tạo tới 365 ngày × N khung giờ trong 1 request (không transaction); EP-51 không giới hạn số dòng CSV; EP-55 đếm-rồi-tạo không có `PlanLimitGuard` ⇒ vượt trần 100 câu hỏi khi thao tác song song | EP-35, EP-51, EP-55 | `CalendarCourseReceptionService.php:52-136`, `CalendarCourseService.php:351-461`, `:1409-1415` | Cao |
| A-18 | 🟡 Trung bình | **Mass assignment khi tạo lịch**: `array_merge($request, $data)` đưa mọi field client gửi vào `create()` — client có thể set `is_use_payment`, `environment`, `google_sheet_id`… ngay lúc tạo (mức độ tuỳ `$fillable` của model) | EP-28 | `CalendarManagementService.php:66` | Trung bình |
| A-19 | 🟡 Trung bình | **Stored XSS tiềm tàng**: `content_policy` (EP-67) và `description`/`description_top` (EP-68) là HTML do Admin nhập, **không lọc**, hiển thị cho LINE User trên trang public. Mức độ phụ thuộc blade dùng `{{ }}` hay `{!! !!}` | EP-67, EP-68 | `:507-525`, `:527-577` | Trung bình |
| A-20 | 🟡 Trung bình | **`check_login` không có nhánh `else`** ⇒ người chưa đăng nhập gọi endpoint Nhóm B nhận HTTP **200 body rỗng** thay vì 401/redirect. Không rò dữ liệu, nhưng che giấu lỗi và làm client xử lý sai | EP-66…EP-82 | `CheckLogin.php:21-42` | Cao |
| A-21 | 🟡 Trung bình | **`https_protocol` là no-op** — toàn bộ thân hàm bị comment. Tên middleware gợi ý đang ép HTTPS nhưng thực tế không làm gì; bảo mật kênh truyền phụ thuộc hoàn toàn cấu hình web server | Toàn Nhóm A | `HttpsProtocol.php:15-22` | Cao |
| A-22 | 🟡 Trung bình | **Rò thông tin qua thông điệp lỗi tiếng Anh** hiển thị cho người dùng Nhật: `'Calendar does not exist'`, `'Course not found'`, `'Error'`, `'Send mail success'`, `'auth calendar success'`, `'delete calendar success'`, `'setting calendar success'` | EP-57, EP-69, EP-70, EP-71, EP-72, EP-73, EP-74 | `:1445` ('Error'), `:661`/`:692`/`:725`/`:782`/`:819`/`:849`/`:1076`/`:1246` ('Calendar does not exist'), `:670`, `:704`, `:769`, `:808`, `:913`; `CalendarCourseService.php:480`, `:547`, `:615`, `:673`, `:735` ('Course not found') | Cao |
| A-23 | 🟡 Trung bình | **`success` luôn `true` che giấu thất bại.** EP-29, EP-30, EP-38, EP-43, EP-46, EP-58, EP-66, EP-82 trả `success: true` cả khi bản ghi không tồn tại hoặc thao tác không diễn ra ⇒ Admin tưởng đã lưu | nhiều | `:154-163`, `:276-285`, `:340-350`, `:374-383`, `:490-505`, `:2649-2654` | Cao |
| A-24 | 🟢 Thấp | **IDOR đọc mức thấp**: EP-78 trả tên khoá học của calendar bất kỳ; EP-23 trả nhãn trường hồ sơ của bot bất kỳ; EP-08/EP-09/EP-12/EP-14 trả dữ liệu khoá học không lọc bot | EP-08, EP-09, EP-12, EP-14, EP-23, EP-78 | `:1474-1482`, `:1057-1067`, `:2451` | Cao |
| A-25 | 🟢 Thấp | **500 dễ kích hoạt do thiếu kiểm null / thiếu key**: `$step->action_id` (EP-77 :1166), `$data['displayMode']` (EP-34), `$request['dateFrom']`/`limit`/`page` (EP-40), 15 khoá `calendar_data` (EP-68), `Carbon::createFromTimeString($startTime)` (EP-74 :871), `foreach ($request->listId)` khi null (EP-30) | nhiều | — | Cao |

### 5.1 Điểm bất thường về chất lượng (không phải lỗ hổng)

| # | Vấn đề | Bằng chứng |
|---|---|---|
| Q-01 | **`remindStepId` không bao giờ được dùng** ⇒ EP-74 luôn INSERT, không bao giờ UPDATE ⇒ lưu nhiều lần sinh nhiều bước nhắc trùng, khách nhận tin lặp | `:834`, `:877-906` |
| Q-02 | **Hai quy ước response song song** trong cùng controller: `{success, data, message}` (Nhóm A) và `{status, …}` (Nhóm B). EP-79 dùng **cả hai trong một method** (`status` khi OK, `success` khi lỗi) | `:1244` vs `:1372` |
| Q-03 | **`success` mang nghĩa nghiệp vụ** ở EP-64 ("có thể xoá") thay vì "gọi API thành công" — trái quy ước 60+ endpoint còn lại | `:2270-2279` |
| Q-04 | **So sánh lỗi bằng chuỗi tiếng Nhật cứng** ở EP-47, EP-63 (và ở `deleteFromApp` phía app di động) — sửa 1 ký tự ở service biến lỗi thành thành công | `:387`, `:405` |
| Q-05 | **HTTP 500 cho lỗi nghiệp vụ** (EP-05, EP-06, EP-10, EP-11, EP-13, EP-15, EP-19, EP-68) — làm nhiễu monitoring | `:1518`, `:1653`, `:536` |
| Q-06 | **Rule chống trùng tên đã bị comment**: `CheckCourseNameUnique`, `CheckCourseNameUniqueWhenUpdate`, `CheckSystemNameUnique` | `CreateCalendarCourse.php:31`, `EditCalendarCourse.php:38`, `:45` |
| Q-07 | **`use_message_notify_not_full` hard-code `0`** — cột không bao giờ bật được từ UI | `:804` |
| Q-08 | **`is_use_message` bị đảo nghĩa** ở EP-79: `'true'` ⇒ lưu `0` | `:1267` |
| Q-09 | **`time_send` không zero-pad** ở EP-74/EP-79: `startHourse=9, startMinute=5` ⇒ `"9:5"` | `:873`, `:1261` |
| Q-10 | **Tham số đọc rồi bỏ**: `isRemindBefore` (EP-74 :837), `$botId` (EP-78 :1058), `type` (EP-37 nếu service không dùng) | — |
| Q-11 | **Tên tham số sai nghĩa**: `lineName` ở EP-41 thực chất lọc **tên khoá học**; route `last-booking` (số ít) gọi `getLastTenBooking` (10 bản ghi) | `CalendarCourseReceptionRepository.php:114`, `:2208-2215` |
| Q-12 | **Method `get*` có side effect ghi DB**: `getSettingMessage`, `getSettingForm`, `getListStepRemind` đều tạo bản ghi mặc định | `:143-144`, `:1085-1119` |
| Q-13 | **Trùng tên tham số `id`** ở EP-56/EP-57: `{id}` path = calendar, `id` body = câu hỏi | `:1426-1453` |
| Q-14 | **Log ghi nhãn sai**: EP-72 log `'deleteCalendar id: '`; EP-81 log `'deleteItemActionEventStep success'` | `:776`, `:2185` |
| Q-15 | **`ActionDetail::exists()` bất nhất**: EP-80 không lọc `bot_id`, EP-81 có lọc — hai method gần như song sinh | `:1211` vs `:2126` |
| Q-16 | **`cancelGoogsheet` không reset `google_sheet_status`** ⇒ trạng thái liên kết Google Sheet có thể sai sau khi ngắt | `:628-644` |
| Q-17 | **Nhánh `catch (\Google_Exception)` không `return`** ⇒ trang trắng HTTP 200 | `:613-618` |
| Q-18 | **`perpage = 100000`** ở EP-04 — phân trang giả | `:1491` |
| Q-19 | **`無制限` lưu thành `total_person = 1`** — giá trị rác, chỉ `type_limit_booking` có nghĩa | `CalendarCourseService.php:428-429` |
| Q-20 | **`form_info` là chuỗi JSON lồng trong body** ở EP-82, trong khi EP-38 dùng mảng thật (`formQuestion`) | `:2507` vs `CalendarCourseBookingService.php:111` |

### 5.2 Đối chiếu với phía LIFF / app di động

Các thiếu sót **xuất hiện ở nhiều lớp cùng lúc** (không phải lỗi riêng của từng lớp) — cần sửa ở tầng service/repository chứ không chỉ ở controller:

| Vấn đề | Phía Admin (spec này) | Phía LIFF / app (`api-spec-public.md`) |
|---|---|---|
| Tạo đặt chỗ **không kiểm sức chứa** | EP-38 | S-20 (EP-M15) |
| Hoàn tiền **không kiểm `payment_status`** | A-09 (EP-24) | S-21 (EP-M08) |
| Sửa khung giờ **không chặn hạ dưới `total_booking`** | EP-46 | S-22 (EP-M11) |
| Miễn trừ CSRF `'/ajax/*'` | A-01 (Nhóm B) | S-07 (toàn bộ EP-P*) |
| Thiếu kiểm quyền/role | §3.2 — 0/82 endpoint | S-18 — 14/15 endpoint |
| Thiếu kiểm sở hữu `bot_id` | A-02…A-13 | S-19 |
| `FriendInformationValue` không lọc `bot_id` | EP-82 (`:2617`) | EP-P06 (`:711-714`) |
| So sánh lỗi bằng chuỗi JP cứng | Q-04 (EP-47, EP-63) | EP-M14 |
| Tạo khung giờ hàng loạt không giới hạn | A-17 (EP-35) | EP-M13 |

---

## 6. Phụ thuộc chéo (bổ sung cho §4 của `api-spec-public.md`)

| Thành phần | Phụ thuộc | Ghi chú |
|---|---|---|
| Google Sheets | `GoogleSheetService`, `CalendarGoogleSheetService` | EP-01 tạo spreadsheet + lưu token; EP-02 ngắt; EP-24 `updateStatusPaymentBooking()`; EP-42 `updateStatusBooking()`; EP-82 `updateFriendInfo()` |
| Job Spring Boot | `event_step_time` | Ghi bởi EP-74/EP-79 (`addActionRemindNew`); xoá bởi EP-76, EP-79 |
| Job Spring Boot | `mobile_notify` | Xoá bởi EP-43 (service) và EP-71 |
| Cổng thanh toán | `StripePayment`, `UnivapayPayment`, bảng `strip_bots` | EP-24 (hoàn tiền), EP-42 (thu tiền khi duyệt), EP-20/EP-21 (cấu hình) |
| Hồ sơ bạn bè | `friend_information_settings`, `friend_information_values`, `line_user`, `friend_info_option_selects` | Đọc ở EP-22/EP-23; ghi đè ở EP-38 và EP-82 |
| Action / Filter dùng chung | `action_detail`, `filter_v2` (`parent_type = 'modal_action'`), helper `getActionDetailByActionId()` | EP-12, EP-13, EP-66, EP-77, EP-80, EP-81 |
| Rich menu / Kịch bản / Conversion / Status chat | `rich_menus`, `scenario`, `conversion`, `status_chat` | Truyền vào view ở EP-33 và EP-48 để cấu hình action |
| Hạn mức gói | `PlanLimitGuard`, `bot_slots`, `bot_contracts` | EP-26 (`canCreate`), EP-28 (1/3/10 lịch), EP-07 (2 khoá học gói free, trần 200) |
| Email hệ thống | `App\Mail\SendAuthCode` | EP-69 |
| Badge app di động | `recountAppBadgeNotify()` | EP-71 |
| FA-020 「サロン予約」 | `CheckCalendarSalonInBot` (middleware song sinh của `CheckLessonCalendarBelongToBot`) | Hai middleware có **cùng khiếm khuyết** (chỉ kiểm `id` cấp calendar). Sửa một cần sửa cả hai |

