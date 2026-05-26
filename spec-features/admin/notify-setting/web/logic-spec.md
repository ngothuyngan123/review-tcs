# [FA-006] Cài đặt thông báo — Logic Spec

> Phân tích từ source code Laravel (`src/web/`).
> Confidence: **Cao** — đọc trực tiếp từ code.

## Controllers

### Basic\NotifySettingController
- **File**: `app/Http/Controllers/Basic/NotifySettingController.php` (872 dòng)
- **Namespace**: `App\Http\Controllers\Basic`

#### Action: index()
- **Route**: GET `/basic/notify-setting` (EP-01)
- **Chức năng**: Render trang cài đặt thông báo
- **Luồng xử lý**:
  1. Lấy `botId` từ session qua helper `getBotId()`
  2. Trả về Blade view `basic.notify_setting.setting`
- **Gọi đến**: Không gọi service/model — chỉ render view
- **Ghi chú**: Dữ liệu thực tế được load bằng AJAX từ client (gọi `getNotifySetting`)

#### Action: getNotifySetting()
- **Route**: GET `/ajax/basic/notify-setting` (EP-02)
- **Chức năng**: Lấy toàn bộ cấu hình thông báo cho bot hiện tại, tự tạo record mặc định nếu chưa tồn tại
- **Luồng xử lý**:
  1. Lấy `botId` từ session
  2. Query `NotifySetting` theo `bot_id`
  3. Nếu không có record → **tạo mới** với giá trị mặc định:
     - Tất cả toggle `is_notify_*` = 1 (ON)
     - Tất cả `*_notification_settings` = 0 (ON trong logic đảo)
     - Tất cả detail fields = null (chưa chọn sự kiện cụ thể)
     - `is_all_*_new` = 0 (tắt tự động tick mục mới)
     - `notification_schedule`, `schedule_chat_work`, `schedule_pc` = 0 (realtime)
  4. Fetch lại record sau khi tạo
  5. **Biến đổi dữ liệu trước khi trả về**:
     - Các trường comma-separated → `explode(',')` thành array
     - Các trường toggle phương tiện → **đảo ngược**: `0 → 1`, `khác 0 → 0`
  6. Trả JSON response
- **Gọi đến**: Model `NotifySetting`
- **Side effects**: Có thể INSERT record mới nếu chưa tồn tại

**Danh sách fields được explode:**
| Field DB | Biến trả về | Hạng mục |
|---------|-----------|---------|
| `chat_1_1` | `chat_1_1` | Chat 1:1 |
| `add_friends` | `add_friends` | Bạn bè đăng ký |
| `send_all` | `send_all` | Gửi tin nhắn hàng loạt |
| `when_adding_friends` | `when_adding_friends` | QR code |
| `answer_form` | `answer_form` | Form |
| `booking_calendar` | `booking_calendar` | Đặt lịch (cũ — tổng hợp) |
| `event_reservation_management` | `event_reservation_management` | Đặt lịch sự kiện |
| `settlement` | `settlement` | Bán hàng |
| `system_notification` | `system_notification` | Thông báo hệ thống (cũ) |
| `action_schedule` | `action_schedule` | Action schedule |
| `conversion` | `conversion` | Conversion |
| `asp` | `asp` | ASP |
| `limitMessage` | `limitMessage` | Cảnh báo số lượng phát hành |
| `systemNotify` | `systemNotify` | Thông báo hệ thống (mới) |
| `lesson_booking` | `lesson_booking` | Đặt lịch bài học |
| `salon_booking` | `salon_booking` | Đặt lịch salon |

#### Action: saveNotifySettingReceive()
- **Route**: POST `/basic/notify-setting-receive` (EP-03)
- **Chức năng**: Lưu cài đặt phương tiện thông báo (bật/tắt + timing) — phiên bản AJAX mới
- **Luồng xử lý**:
  1. Lấy `botId` từ session
  2. Query `NotifySetting` hiện tại
  3. Đếm `MessageError` chưa xác nhận (`is_confirmed = 0`)
  4. **Nếu đã có record** (`$notifySettingData` tồn tại):
     a. Nếu ChatWork vừa **tắt → bật** (DB 0 → request 1): cập nhật `mobile_notify.status_chat_work = 1` cho tất cả record chưa gửi
     b. Nếu Smartphone vừa **tắt → bật** (DB 0 → request 1): cập nhật `mobile_notify.status = 1` cho tất cả record chưa gửi
     c. Nếu ChatWork thay đổi: cập nhật `chat_work_total_msg_error` = số lỗi hiện tại
     d. Nếu Smartphone thay đổi: cập nhật `app_total_msg_error` = số lỗi hiện tại
     e. Chuẩn bị `paramsUpdate` với 6 trường: 3 toggle + 3 schedule
     f. **Tính toán next_notify_time** cho từng phương tiện nếu timing thay đổi:
        - Lấy `last_notify_time` (hoặc `now()` nếu chưa có)
        - Cộng thêm thời gian theo schedule value (switch case 0-7)
        - Cập nhật `next_notify_time`, `next_notify_chat_work_time`, `next_notify_pc_time`
     g. Update record
  5. **Nếu chưa có record**: Tạo mới với giá trị từ request + `countMsgError` + `next_notify_*_time = now()`
  6. Tính `getTotalNotifyExceptSystemAndBillCycle($botId)` → cập nhật `bots.count_app_notify`
  7. Trả JSON `{"success": true}`
- **Gọi đến**: Model `NotifySetting`, `MobileNotify`, `MessageError`, `Bots`; Helper `getTotalNotifyExceptSystemAndBillCycle`
- **Side effects**:
  - UPDATE `mobile_notify` records khi bật lại phương tiện
  - UPDATE/INSERT `notify_setting`
  - UPDATE `bots.count_app_notify`

#### Action: saveNotifySettingReceivePage()
- **Route**: POST `/basic/notify-setting-receive-page` (EP-04)
- **Chức năng**: Lưu cài đặt chi tiết từng hạng mục thông báo
- **Luồng xử lý**:
  1. Lấy `botId`, query `NotifySetting` hiện tại
  2. Đọc `page` param từ request
  3. **Switch case theo page** — 15 case:
     - Mỗi case cập nhật 2 fields: toggle (`is_notify_*`) + detail (danh sách sự kiện)
     - 4 cases (`qrCode`, `form`, `actionSchedule`, `conversion`) có thêm nhánh `isAllNew`:
       - Nếu `isAllNew = true` → chỉ cập nhật `is_all_{type}_new` + `update_select_{type}_new = now()`
       - Nếu `isAllNew = false/null` → cập nhật toggle + detail
     - Detail field: array → `implode(",")` → lưu dưới dạng comma-separated string
  4. Nếu chưa có record → tạo mới với giá trị từ request (cũng switch case tương tự)
  5. Tính `getTotalNotifyExceptSystemAndBillCycle($botId)` → cập nhật `bots.count_app_notify`
  6. Trả JSON `{"success": true}`
- **Gọi đến**: Model `NotifySetting`, `MessageError`, `Bots`; Helper `getTotalNotifyExceptSystemAndBillCycle`

#### Action: saveNotifySettings()
- **Route**: POST `/basic/notify-setting` (EP-05)
- **Chức năng**: **Phiên bản cũ** — lưu toàn bộ cài đặt (cả phương tiện + hạng mục), redirect (không AJAX)
- **Luồng xử lý**:
  1. Tương tự EP-03 nhưng bao gồm cả detail fields
  2. Cũng cập nhật `mobile_notify` khi bật lại phương tiện
  3. Redirect về route `notifySetting` (EP-01). Lỗi → redirect route `404`
- **Ghi chú**: Không còn sử dụng trên UI hiện tại — UI mới dùng EP-03 + EP-04 để auto-save từng phần

#### Action: notifySettingChatwork()
- **Route**: GET `/basic/notify-setting-chatwork` (EP-10)
- **Chức năng**: Render trang cài đặt liên kết ChatWork
- **Luồng xử lý**:
  1. Lấy `botId` từ session
  2. Query `Landing` và `FormAnswer` theo `bot_id`
  3. Trả Blade view `basic.notify_setting.setting_chatwork` với `$landingData`, `$formAnswerData`
- **Gọi đến**: Model `Landing`, `FormAnswer`

#### Action: ajaxSaveUrlChatWork()
- **Route**: POST `/ajax/notify/save-url-chat-work` (EP-11)
- **Chức năng**: Lưu URL room ChatWork
- **Luồng xử lý**:
  1. Lấy `botId`, query `NotifySetting`
  2. Update `notification_room_url` (hoặc tạo mới nếu chưa có record)
  3. Trả JSON `{"success": true, "url": "..."}`
- **Gọi đến**: Model `NotifySetting`

#### Action: ajaxSaveApiTokenChatWork()
- **Route**: POST `/ajax/notify/save-api-token-chat-work` (EP-12)
- **Chức năng**: Lưu ChatWork API token
- **Luồng xử lý**:
  1. Lấy `botId`, query `NotifySetting`
  2. Update `api_token` (hoặc tạo mới nếu chưa có record)
  3. Trả JSON `{"success": true, "api_token": "..."}`
- **Gọi đến**: Model `NotifySetting`
- **Lưu ý bảo mật**: API token được trả lại trong response — có thể lộ qua network logs

#### Action: ajaxChangeTypeSendChatwork()
- **Route**: POST `/ajax/notify/save-type_notify_send_chatwork` (EP-13)
- **Chức năng**: Thay đổi kiểu gửi thông báo ChatWork
- **Luồng xử lý**:
  1. Lấy `botId`, query `NotifySetting`
  2. Update `type_notify_send_chatwork` (hoặc tạo mới)
  3. Trả JSON `{"success": true, "type_notify_send_chatwork": N}`
- **Gọi đến**: Model `NotifySetting`

#### Action: ajaxTestSendChatwork()
- **Route**: POST `/ajax/notify/test-send-chatwork` (EP-14)
- **Chức năng**: Gửi tin nhắn test đến ChatWork room
- **Luồng xử lý**:
  1. Lấy `botId`, query `NotifySetting`
  2. Kiểm tra `chatWork_notification_settings == 0` (ChatWork đang bật)
  3. Lấy room ID từ `notification_room_url` bằng `explode('#!rid', url)[1]`
  4. Gửi POST request đến ChatWork API: `https://api.chatwork.com/v2/rooms/{roomId}/messages`
     - Header: `X-ChatWorkToken` = `api_token` từ DB hoặc fallback env `TOKEN_API_BOT_CHATWORK`
     - Body: `body = "エルメ 通知テスト送信完了"`
  5. Nếu ChatWork API trả 200 → success, ngược lại → fail
- **Gọi đến**: Model `NotifySetting`, Guzzle HTTP client
- **External API**: ChatWork API v2

#### Action: getLandingBot()
- **Route**: GET `/basic/getLandingBot` (EP-06)
- **Chức năng**: Lấy toàn bộ landing pages (QR code) của bot
- **Luồng xử lý**:
  1. Lấy `botId` từ session
  2. Query `Landing::where('bot_id', $botId)->get()` — không filter, không paginate
  3. Trả JSON `{"status": true, "data": [...]}`
- **Gọi đến**: Model `Landing`
- **Ghi chú**: Có đoạn code bị comment out filter `category_id <> 0` — từng có filter nhưng đã bỏ

#### Action: getFormAnswerBot()
- **Route**: GET `/basic/getFormAnswerBot` (EP-07)
- **Chức năng**: Lấy toàn bộ form answers của bot
- **Luồng xử lý**:
  1. Lấy `botId` từ session
  2. Query `FormAnswer::where('bot_id', $botId)->get()`
  3. Trả JSON `{"status": true, "data": [...]}`
- **Gọi đến**: Model `FormAnswer`
- **Lưu ý**: `FormAnswer` có accessor `getCreatedAtAttribute` format `created_at` thành `Y.m.d`

#### Action: getActionScheduleBot()
- **Route**: GET `/basic/getActionScheduleBot` (EP-08)
- **Chức năng**: Lấy toàn bộ action schedules của bot
- **Luồng xử lý**:
  1. Lấy `botId` từ session
  2. Query `ActionSchedule::where('bot_id', $botId)->get()`
  3. Trả JSON `{"status": true, "data": [...]}`
- **Gọi đến**: Model `ActionSchedule`

#### Action: getConversionBot()
- **Route**: GET `/basic/getConversionBot` (EP-09)
- **Chức năng**: Lấy danh sách conversions (chỉ name + id)
- **Luồng xử lý**:
  1. Lấy `botId` từ session
  2. Query `Conversion::select('name', 'id')->where('bot_id', $botId)->get()`
  3. Trả JSON `{"status": true, "data": [...]}`
- **Gọi đến**: Model `Conversion`
- **Ghi chú**: Chỉ trả `name` và `id`, không trả toàn bộ fields

#### Action: getVapidPublicKey()
- **Route**: GET `/push/get-vapid-public-key` (EP-15)
- **Chức năng**: Trả VAPID public key cho Web Push
- **Luồng xử lý**:
  1. Lấy key từ `config('webpush.vapid.public_key')` (env `VAPID_PUBLIC_KEY`)
  2. Trả JSON `{"key": "..."}`
- **Gọi đến**: Không gọi model/service

#### Action: subscribePushNotification()
- **Route**: POST `/push/subscribe-push-notification` (EP-16)
- **Chức năng**: Đăng ký Web Push subscription
- **Luồng xử lý**:
  1. Lấy user đang đăng nhập (`Auth::user()`)
  2. Kiểm tra subscription đã tồn tại (theo `subscribable_id` + `public_key`)
  3. Nếu chưa tồn tại → gọi `$user->updatePushSubscription(endpoint, p256dh, auth)`
  4. Trả JSON `{"success": true}`
- **Gọi đến**: Model `PushSubscription` (package `laravel-notification-channels/webpush`)
- **Bảng DB**: `push_subscriptions`

#### Action: unsubscribePushNotification()
- **Route**: POST `/push/unsubscribe-push-notification` (EP-17)
- **Chức năng**: Hủy Web Push subscription
- **Luồng xử lý**:
  1. Lấy user đang đăng nhập
  2. Tìm `PushSubscription` theo `subscribable_id` + `public_key` (= `pushKey`)
  3. Nếu tìm thấy → gọi `$user->deletePushSubscription(endpoint)`
  4. Trả JSON `{"success": true}`
- **Gọi đến**: Model `PushSubscription`

#### Action: pushNotification()
- **Route**: POST `/api/notify/push-notify` (EP-18)
- **Chức năng**: API nội bộ — nhận yêu cầu push notification từ background job, insert record vào `notification_pc`
- **Luồng xử lý**:
  1. Lấy `notifyTitle`, `notifyContent`, `botId` từ request
  2. Tìm bot: `Bots::find($botId)`
  3. Tìm user: `User::find($bot->admin_id)`
  4. Insert vào `notification_pc`: `{content, title, bot_id, user_id}`
  5. Không trả response body rõ ràng
- **Gọi đến**: Model `Bots`, `User`, `NotificationPC`
- **Ghi chú**: Đây là API được gọi từ Spring Boot job, không phải từ frontend

---

## Models

### NotifySetting
- **File**: `app/NotifySetting.php`
- **Bảng DB**: `notify_setting`
- **Guarded**: `[]` (mass assignment cho tất cả fields)
- **Timestamps**: Có (`created_at`, `updated_at`)

#### Relationships
Không có relationship định nghĩa trong model.

#### Scopes
Không có scope.

#### Mutators / Accessors
Không có mutator/accessor.

#### Ghi chú
Model rất đơn giản — chỉ là data container. Toàn bộ business logic nằm trong controller.

---

### MobileNotify
- **File**: `app/MobileNotify.php`
- **Bảng DB**: `mobile_notify`
- **Guarded**: `[]`
- **Timestamps**: Có

#### Constants (Enum Values) — Rất quan trọng

**Calendar Lesson:**
| Constant | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `CALENDAR_LESSON_BOOKED` | 0 | Đặt lịch thành công |
| `CALENDAR_LESSON_BOOKING_REQUEST` | 6 | Yêu cầu đặt lịch |
| `CALENDAR_LESSON_BOOKING_APPROVE` | 1 | Duyệt yêu cầu đặt lịch |
| `CALENDAR_LESSON_BOOKING_DENY` | 10 | Từ chối yêu cầu đặt lịch |
| `CALENDAR_LESSON_BOOKING_CANCEL` | 4 | Hủy đặt lịch |
| `CALENDAR_LESSON_REQUEST_BOOKING_CANCEL` | 8 | Yêu cầu hủy đặt lịch |
| `CALENDAR_LESSON_APPROVE_BOOKING_CANCEL` | 5 | Duyệt yêu cầu hủy |
| `CALENDAR_LESSON_DENY_BOOKING_CANCEL` | 11 | Từ chối yêu cầu hủy |

**Calendar Salon:**
| Constant | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `CALENDAR_SALON_BOOKED` | 0 | Đặt lịch thành công |
| `CALENDAR_SALON_BOOKING_REQUEST` | 6 | Yêu cầu đặt lịch |
| `CALENDAR_SALON_BOOKING_APPROVE` | 1 | Duyệt yêu cầu đặt lịch |
| `CALENDAR_SALON_BOOKING_DENY` | 9 | Từ chối yêu cầu đặt lịch |
| `CALENDAR_SALON_BOOKING_CANCEL` | 4 | Hủy đặt lịch |
| `CALENDAR_SALON_REQUEST_BOOKING_CANCEL` | 8 | Yêu cầu hủy đặt lịch |
| `CALENDAR_SALON_APPROVE_BOOKING_CANCEL` | 5 | Duyệt yêu cầu hủy |
| `CALENDAR_SALON_DENY_BOOKING_CANCEL` | 11 | Từ chối yêu cầu hủy |

**Event Booking:**
| Constant | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `EVENT_BOOKING_BOOKED` | 0 | Đặt lịch thành công |
| `EVENT_BOOKING_REQUEST` | 6 | Yêu cầu đặt lịch |
| `EVENT_BOOKING_APPROVE` | 3 | Duyệt yêu cầu đặt lịch |
| `EVENT_BOOKING_DENY` | 4 | Từ chối yêu cầu đặt lịch |
| `EVENT_BOOKING_CHANGE` | 1 | Thay đổi đặt lịch |
| `EVENT_BOOKING_REQUEST_CHANGE` | 7 | Yêu cầu thay đổi |
| `EVENT_BOOKING_APPROVE_CHANGE` | 8 | Duyệt yêu cầu thay đổi |
| `EVENT_BOOKING_DENY_CHANGE` | 9 | Từ chối yêu cầu thay đổi |
| `EVENT_BOOKING_CANCEL` | 2 | Hủy đặt lịch |
| `EVENT_BOOKING_REQUEST_CANCEL` | 10 | Yêu cầu hủy |
| `EVENT_BOOKING_APPROVE_CANCEL` | 11 | Duyệt yêu cầu hủy |
| `EVENT_BOOKING_DENY_CANCEL` | 5 | Từ chối yêu cầu hủy |

**Product Sales (Items):**
| Constant | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `PRODUCT_SALES_ONE_TIMES_SUCCESS` | 5 | Mua sản phẩm đơn lẻ thành công |
| `PRODUCT_SALES_ONE_TIMES_FAIL` | 6 | Mua sản phẩm đơn lẻ thất bại |
| `PRODUCT_SALES_CYCLE_FIRST_SUCCESS` | 7 | Thanh toán sản phẩm định kỳ lần đầu thành công |
| `PRODUCT_SALES_CYCLE_SECOND_SUCCESS` | 12 | Thanh toán sản phẩm định kỳ lần thứ 2 thành công (chưa có trên design) |
| `PRODUCT_SALES_CYCLE_TRIAL_START` | 8 | Bắt đầu dùng thử sản phẩm định kỳ |
| `PRODUCT_SALES_CYCLE_ADMIN_CANCEL` | 9 | Hủy thủ công sản phẩm định kỳ |
| `PRODUCT_SALES_CYCLE_FAIL` | 11 | Thanh toán sản phẩm định kỳ thất bại |
| `PRODUCT_SALES_CYCLE_JOB_CANCEL` | 10 | Tự động (cưỡng chế) hủy sản phẩm định kỳ |

**Delivery Count Alert (配信数アラート):**
| Constant | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `DELIVERY_COUNT_ALERT_ALL` | 0 | Chọn tất cả |
| `DELIVERY_COUNT_ALERT_LINE_100` | 1 | LOA >= 100 tin |
| `DELIVERY_COUNT_ALERT_LINE_200` | 2 | LOA >= 200 tin |
| `DELIVERY_COUNT_ALERT_LINE_4000` | 3 | LOA >= 4,000 tin |
| `DELIVERY_COUNT_ALERT_LINE_5000` | 4 | LOA >= 5,000 tin |
| `DELIVERY_COUNT_ALERT_LINE_25000` | 5 | LOA >= 25,000 tin |
| `DELIVERY_COUNT_ALERT_LINE_30000` | 6 | LOA >= 30,000 tin |
| `DELIVERY_COUNT_ALERT_LME_500` | 7 | Elme >= 500 tin |
| `DELIVERY_COUNT_ALERT_LME_1000` | 8 | Elme >= 1,000 tin |

**System Notification:**
| Constant | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `SYSTEM_NOTIFICATION_ERROR_MESSAGE` | 1 | Lỗi gửi tin nhắn |
| `SYSTEM_NOTIFICATION_ADD_BOT` | 2 | Thêm bot |
| `SYSTEM_NOTIFICATION_DELETE_BOT` | 3 | Xóa bot |
| `SYSTEM_NOTIFICATION_PAYMENT_SUCCESS` | 4 | Thanh toán thành công |
| `SYSTEM_NOTIFICATION_PAYMENT_ERROR` | 5 | Thanh toán thất bại |
| `SYSTEM_NOTIFICATION_ADD_STAFF` | 6 | Thêm staff |

**Affiliate (ASP):**
| Constant | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `AFF_NEW_REGISTER` | 1 | Affiliate đăng ký mới |
| `AFF_COMMISSION_AUTO_VERIFICATION` | 2 | Thưởng affiliate tự động xác nhận |
| `AFF_COMMISSION_MANUAL_VERIFICATION` | 3 | Thưởng affiliate thủ công xác nhận |

#### Relationships
Không có relationship định nghĩa trong model.

#### Model Type Constants
| Constant | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `MODEL_TYPE_ORDER_NOTIFY_DEFAULT` | 0 | Thông báo order mặc định |
| `MODEL_TYPE_ORDER_NOTIFY` | 1 | Thông báo order |
| `MODEL_TYPE_SALON` | 2 | Thông báo salon |

---

### NotificationPC
- **File**: `app/NotificationPC.php`
- **Bảng DB**: `notification_pc`
- **Guarded**: `[]`
- **Timestamps**: Có

#### Relationships
Không có relationship định nghĩa.

#### Ghi chú
Dùng để lưu push notification records. Background job (EP-18) insert vào bảng này. Client-side sẽ query và hiển thị.

---

### Landing
- **File**: `app/Landing.php`
- **Bảng DB**: `landing`
- **Traits**: `SoftDeletes`
- **Guarded**: `[]`

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `tags()` | hasOne | `Tags` | `tag_id` → `id` | Tag gắn với landing |
| `scenario()` | hasOne | `Scenario` | `scenario_id` → `id` | Kịch bản liên quan |
| `template()` | hasOne | `Template` | `template_id` → `id` | Template tin nhắn |
| `action()` | belongsTo | `Actions` | `action_id` → `id` | Hành động khi quét QR |
| `details()` | hasMany | `DetailLandingClick` | `landing_id` → `id` | Chi tiết click |
| `actions()` | hasMany | `ActionDetail` | `action_id` → `action_id` | Chi tiết hành động |
| `operator()` | belongsTo | `User` | `operator_id` → `id` | Người tạo |

#### Sử dụng trong tính năng này
Chỉ dùng `Landing::where('bot_id', $botId)->get()` — lấy danh sách để hiển thị checkbox.

---

### FormAnswer
- **File**: `app/FormAnswer.php`
- **Bảng DB**: `form_answer`
- **Traits**: `SoftDeletes`
- **Guarded**: `[]`

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `form_details()` | hasMany | `FormAnswerDetails` | `form_id` → `id` | Chi tiết form |
| `pages()` | hasMany | `FormAnswerPage` | `form_id` → `id` | Trang form |
| `setting_common()` | belongsTo | `FormAnswerSettingCommon` | `id` → `form_id` | Cài đặt chung |

#### Accessors
| Attribute | Kiểu | Mô tả |
|----------|------|-------|
| `created_at` | Accessor | Format `Y-m-d H:i:s` → `Y.m.d` |
| `setting_page_confirm` | Accessor | Trả cài đặt nút xác nhận, fallback JSON decode |

#### Sử dụng trong tính năng này
Chỉ dùng `FormAnswer::where('bot_id', $botId)->get()` — lấy danh sách để hiển thị checkbox.

---

### ActionSchedule
- **File**: `app/ActionSchedule.php`
- **Bảng DB**: `action_schedules`
- **Fillable**: `name`, `filter_ids`, `action_id`, `category_id`, `next_running_day`, `start_date`, `start_time`, `end_date_type`, `repeat_type`, `end_date`, `number_of_repetitions`, `day_add`, `number_week_to_repeat`, `day_of_week_repeat`, `number_month_to_repeat`, `date_repeat_after_number_of_month`, `skip_date`, `bot_id`, `position`, `number_user_filter`, `action_count`, `first_day_of_running`

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `histories()` | hasMany | `ActionScheduleHistory` | `action_schedule_id` | Lịch sử chạy |

#### Sử dụng trong tính năng này
Chỉ dùng `ActionSchedule::where('bot_id', $botId)->get()` — lấy danh sách để hiển thị checkbox.

---

### Conversion
- **File**: `app/Conversion.php`
- **Bảng DB**: `conversion`
- **Guarded**: `[]`

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `conversion_result()` | hasMany | `ConversionResult` | `conversion_id` → `id` | Kết quả conversion |

#### Sử dụng trong tính năng này
Chỉ dùng `Conversion::select('name', 'id')->where('bot_id', $botId)->get()` — chỉ lấy name + id.

---

### AccessBot
- **File**: `app/AccessBot.php`
- **Bảng DB**: `access_bot`
- **Guarded**: `[]`

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `user()` | belongsTo | `User` | `admin_id` → `id` | Admin sở hữu |
| `bot()` | hasOne | `Bots` | `bot_id` → `id` | Bot liên quan |

#### Sử dụng trong tính năng này
Được import nhưng **không sử dụng trực tiếp** trong controller.

---

### WebPushNotification (Notification Class)
- **File**: `app/Notifications/WebPushNotification.php`
- **Kênh**: `WebPushChannel` (package `laravel-notification-channels/webpush`)
- **Chức năng**: Gửi push notification qua Web Push API

#### Sử dụng trong tính năng này
Được import nhưng **không gọi trực tiếp** trong NotifySettingController. Có thể được dùng bởi các phần khác của hệ thống để gửi push notification đến `push_subscriptions`.

---

## Services

### MobileNotifyService
- **File**: `app/Services/Notify/MobileNotifyService.php`
- **Mô tả**: Service tạo bản ghi thông báo cho các loại sự kiện (salon, lesson, event booking, v.v.)
- **Sử dụng trong tính năng này**: **Không gọi trực tiếp** từ NotifySettingController. Service này được gọi từ các controller/service khác khi sự kiện xảy ra (VD: khi có đặt lịch mới → insert vào `mobile_notify`). Nội dung thông báo sau đó được gửi/hiển thị dựa trên cài đặt trong `notify_setting`.

---

## Form Requests

**Không sử dụng Form Request cho tính năng này.** Toàn bộ validation (nếu có) được thực hiện trực tiếp trong controller methods. Thực tế, hầu như **không có validation** rõ ràng — request parameters được chấp nhận trực tiếp.

---

## Events & Listeners

**Không dispatch event nào** trong NotifySettingController. Không có event/listener liên quan.

---

## Authorization

| Quyền | Kiểm tra ở đâu | Logic | Ảnh hưởng |
|-------|----------------|-------|----------|
| Authentication | Middleware `web` (session) | User phải đăng nhập | Chưa đăng nhập → redirect login |
| Bot Access | Helper `getBotId()` từ session | User phải có bot đang chọn trong session | Không có bot → `null` → lỗi query |
| Staff Permission | **Chưa kiểm tra rõ ràng** | Không thấy kiểm tra role/permission trong controller | Staff có thể truy cập nếu có session — **cần xác minh thêm** middleware ở route group level |

**Ghi chú**: Controller không kiểm tra quyền Staff rõ ràng. Quyền có thể được kiểm tra ở route middleware group level hoặc trong Blade view (ẩn/hiển menu). Cần xác minh thêm.

---

## Helper Functions

### getBotId()
- **File**: `app/Helpers/functions.php:359`
- **Chức năng**: Lấy `current_bot_id` từ session
- **Return**: Integer hoặc null

### getCurrentUser()
- **File**: `app/Helpers/functions.php:4532`
- **Chức năng**: Trả về `Auth::id()` — ID của user đang đăng nhập
- **Return**: Integer

### getTotalNotifyExceptSystemAndBillCycle($botId)
- **File**: `app/Helpers/functions.php:4178`
- **Chức năng**: Đếm số thông báo chưa xác nhận (không tính system + payment) cho bot
- **Logic**:
  ```
  MobileNotify::where('bot_id', $botId)
    ->where('is_confirm', 0)          // Chưa xác nhận
    ->where('status', 1)              // Đã gửi
    ->where('type', '!=', 1)          // Không phải message type
    ->where('type', '!=', config('sns-line.type_of_notification_key.system_notification'))  // = 6
    ->where('type', '!=', config('sns-line.type_of_notification_key.payment'))              // = 5
    ->count()
  ```
- **Return**: Integer — số lượng thông báo
- **Sử dụng**: Được gọi sau mỗi lần lưu cài đặt (EP-03, EP-04, EP-05) để cập nhật `bots.count_app_notify`

### addLogUserAction($action)
- **File**: `app/Helpers/functions.php:8813`
- **Chức năng**: Ghi log hành động user (email, id, bot_id) vào Laravel log
- **Sử dụng**: Gọi trong EP-03, EP-04, EP-05, EP-11, EP-12, EP-13, EP-14

---

## Config — Notification Type Keys

Từ `config/sns-line.php` dòng 454:

| Key | Giá trị | Hạng mục thông báo |
|-----|---------|-------------------|
| `chat_1_1` | 1 | Chat 1:1 |
| `when_adding_friends` | 2 | QR code / Bạn bè (qua landing) |
| `answer_form` | 3 | Form trả lời |
| `event_reservation_management` | 4 | Đặt lịch sự kiện |
| `payment` | 5 | Thanh toán |
| `system_notification` | 6 | Thông báo hệ thống |
| `booking_calendar` | 7 | Đặt lịch (calendar chung) |
| `bill_one` | 8 | Hóa đơn đơn lẻ |
| `bill_cycle` | 9 | Hóa đơn định kỳ |
| `calendar_salon` | 10 | Lịch salon |
| `calendar_lesson` | 11 | Lịch bài học |
| `add_friend_qr_code` | 12 | Bạn bè đăng ký qua QR |
| `send_all` | 13 | Gửi tin nhắn hàng loạt |
| `action_schedule` | 14 | Action schedule |
| `delivery_count_alert` | 15 | Cảnh báo số lượng phát hành |
| `affiliate` | 16 | Affiliate (ASP) |
| `conversion` | 17 | Conversion |

---

## Business Rules tổng hợp

| # | Rule | Mô tả | Nơi implement |
|---|------|-------|--------------|
| 1 | **Toggle đảo ngược** | DB lưu 0 = ON, 1 = OFF cho `*_notification_settings`. API trả về đảo lại (1 = ON, 0 = OFF). | `NotifySettingController@getNotifySetting:170-172` |
| 2 | **Auto-create settings** | Nếu bot chưa có record `notify_setting` → tự tạo mới với mọi thông báo BẬT khi lần đầu truy cập. | `NotifySettingController@getNotifySetting:100-150` |
| 3 | **Comma-separated storage** | Danh sách sự kiện được chọn lưu dưới dạng chuỗi comma-separated (VD: `"0,1,2,3"`). Explode khi đọc, implode khi ghi. | Toàn bộ save/get methods |
| 4 | **Bật phương tiện → requeue notifications** | Khi bật lại smartphone (0→1 trong DB), tất cả `mobile_notify` chưa gửi (`status=0`) được chuyển thành đã sẵn sàng gửi (`status=1`). Tương tự cho ChatWork (`status_chat_work`). | `NotifySettingController@saveNotifySettingReceive:196-201` |
| 5 | **Next notify time calculation** | Khi thay đổi timing → tính `next_notify_time` = `last_notify_time` + khoảng thời gian mới. Nếu chưa có `last_notify_time` → dùng `now()`. Realtime (schedule=0) → `next_notify_time = now()`. | `NotifySettingController@saveNotifySettingReceive:217-320` |
| 6 | **Error count snapshot** | Khi thay đổi phương tiện thông báo → ghi lại số lỗi (`MessageError`) hiện tại vào `app_total_msg_error` / `chat_work_total_msg_error`. | `NotifySettingController@saveNotifySettingReceive:202-207` |
| 7 | **Cập nhật badge count** | Sau mỗi lần lưu cài đặt → đếm lại thông báo chưa xác nhận → cập nhật `bots.count_app_notify`. | `NotifySettingController@saveNotifySettingReceive:350-353` |
| 8 | **Tự động tick mục mới** | 4 hạng mục (QR code, Form, Action Schedule, Conversion) có tùy chọn "tự động tick mục mới thêm". Khi `isAllNew=true` → cập nhật flag `is_all_{type}_new` + ghi timestamp `update_select_{type}_new`. Logic thực tế sử dụng timestamp này ở nơi khác để xác định items nào được tạo sau thời điểm này sẽ tự động ON. | `NotifySettingController@saveNotifySettingReceivePage:396-407, 411-423, 460-471, 475-486` |
| 9 | **ChatWork test — điều kiện** | Chỉ gửi test ChatWork khi `chatWork_notification_settings == 0` (BẬT). Sử dụng API token từ DB hoặc fallback env var `TOKEN_API_BOT_CHATWORK`. Room ID trích xuất từ URL bằng cách split theo `#!rid`. | `NotifySettingController@ajaxTestSendChatwork:773-801` |
| 10 | **Push subscription dedup** | Khi subscribe push notification, kiểm tra đã tồn tại subscription với cùng user ID + public key chưa. Nếu đã có → không tạo mới. | `NotifySettingController@subscribePushNotification:819-825` |
| 11 | **Mỗi bot 1 record notify_setting** | Mỗi bot chỉ có 1 record trong `notify_setting`. Query luôn dùng `where('bot_id', $botId)->first()`. Nếu chưa có → tạo mới. | Toàn bộ methods trong controller |

---

## Ghi chú cho Job Analyzer

Tính năng này **có khả năng liên quan đến background jobs**:

1. **Bảng `mobile_notify`** là bảng trung gian giữa web và job — các sự kiện hệ thống (đặt lịch, thanh toán, v.v.) tạo records ở đây, background job sẽ poll và gửi thông báo dựa trên cài đặt trong `notify_setting`.

2. **EP-18 (`POST /api/notify/push-notify`)** là API được gọi từ Spring Boot job để tạo push notification records.

3. **Trường `next_notify_time`**, `next_notify_chat_work_time`, `next_notify_pc_time` trong `notify_setting` cho thấy có scheduled notification processing — background job kiểm tra thời gian và gửi hàng loạt thay vì realtime.

4. **Trường `status`**, `status_chat_work`, `status_pc` trong `mobile_notify` là state machine cho việc gửi qua 3 phương tiện.

→ **Đề xuất**: Chạy `/spec-job` để phân tích Spring Boot code liên quan đến notification processing.
