# [FA-006] Cài đặt thông báo — API Spec

> Phân tích từ source code Laravel (`src/web/`).
> Confidence: **Cao** — đọc trực tiếp từ code.

## Danh sách Endpoints

| EP | Method | URI | Controller@Action | Middleware | Mô tả |
|----|--------|-----|-------------------|-----------|-------|
| EP-01 | GET | `/basic/notify-setting` | `Basic\NotifySettingController@index` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Hiển thị trang cài đặt thông báo |
| EP-02 | GET | `/ajax/basic/notify-setting` | `Basic\NotifySettingController@getNotifySetting` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy toàn bộ cấu hình thông báo hiện tại (AJAX) |
| EP-03 | POST | `/basic/notify-setting-receive` | `Basic\NotifySettingController@saveNotifySettingReceive` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lưu cài đặt phương tiện thông báo (smartphone, ChatWork, PC) + timing |
| EP-04 | POST | `/basic/notify-setting-receive-page` | `Basic\NotifySettingController@saveNotifySettingReceivePage` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lưu cài đặt hạng mục thông báo theo từng page (chi tiết sự kiện) |
| EP-05 | POST | `/basic/notify-setting` | `Basic\NotifySettingController@saveNotifySettings` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lưu toàn bộ cài đặt (phiên bản cũ — redirect) |
| EP-06 | GET | `/basic/getLandingBot` | `Basic\NotifySettingController@getLandingBot` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy danh sách QR code/landing pages của bot |
| EP-07 | GET | `/basic/getFormAnswerBot` | `Basic\NotifySettingController@getFormAnswerBot` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy danh sách form trả lời của bot |
| EP-08 | GET | `/basic/getActionScheduleBot` | `Basic\NotifySettingController@getActionScheduleBot` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy danh sách action schedule của bot |
| EP-09 | GET | `/basic/getConversionBot` | `Basic\NotifySettingController@getConversionBot` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy danh sách conversion của bot |
| EP-10 | GET | `/basic/notify-setting-chatwork` | `Basic\NotifySettingController@notifySettingChatwork` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Hiển thị trang cài đặt liên kết ChatWork |
| EP-11 | POST | `/ajax/notify/save-url-chat-work` | `Basic\NotifySettingController@ajaxSaveUrlChatWork` | web, NotifyChatworkRequestTimeSlow | Lưu URL room ChatWork |
| EP-12 | POST | `/ajax/notify/save-api-token-chat-work` | `Basic\NotifySettingController@ajaxSaveApiTokenChatWork` | web, NotifyChatworkRequestTimeSlow | Lưu API token ChatWork |
| EP-13 | POST | `/ajax/notify/save-type_notify_send_chatwork` | `Basic\NotifySettingController@ajaxChangeTypeSendChatwork` | web, NotifyChatworkRequestTimeSlow | Thay đổi kiểu gửi thông báo ChatWork |
| EP-14 | POST | `/ajax/notify/test-send-chatwork` | `Basic\NotifySettingController@ajaxTestSendChatwork` | web, NotifyChatworkRequestTimeSlow | Gửi tin nhắn test qua ChatWork |
| EP-15 | GET | `/push/get-vapid-public-key` | `Basic\NotifySettingController@getVapidPublicKey` | web, NotifyChatworkRequestTimeSlow | Lấy VAPID public key cho Web Push |
| EP-16 | POST | `/push/subscribe-push-notification` | `Basic\NotifySettingController@subscribePushNotification` | web, NotifyChatworkRequestTimeSlow | Đăng ký nhận push notification (PC desktop) |
| EP-17 | POST | `/push/unsubscribe-push-notification` | `Basic\NotifySettingController@unsubscribePushNotification` | web, NotifyChatworkRequestTimeSlow | Hủy đăng ký push notification |
| EP-18 | POST | `/api/notify/push-notify` | `Basic\NotifySettingController@pushNotification` | api | Gửi push notification đến user (API nội bộ, gọi từ background job) |

---

## Chi tiết Endpoints

### EP-01: GET `/basic/notify-setting`
- **Controller**: `Basic\NotifySettingController@index`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Render trang cài đặt thông báo. Chỉ lấy `botId` từ session, sau đó trả về Blade view `basic.notify_setting.setting`. Dữ liệu thực tế được load bằng AJAX (EP-02) từ phía client.
- **Liên kết UI**: SCR-NTF-01 → Trang chính cài đặt thông báo

#### Request Parameters
Không có params — page render thuần.

#### Response
Trả về HTML (Blade view `basic.notify_setting.setting`).

---

### EP-02: GET `/ajax/basic/notify-setting`
- **Controller**: `Basic\NotifySettingController@getNotifySetting`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lấy toàn bộ cấu hình thông báo cho bot hiện tại. Nếu chưa có record trong DB → tự động tạo record mới với giá trị mặc định. Các trường chứa danh sách (comma-separated string) được tách thành mảng trước khi trả về. **Lưu ý quan trọng**: giá trị toggle `app_notification_settings`, `chatWork_notification_settings`, `pc_notification_settings` bị **đảo ngược** khi trả về (0 → 1, khác 0 → 0) — DB lưu 0 = ON, nhưng API trả 1 = ON.
- **Liên kết UI**: SCR-NTF-01 → Gọi khi trang load + khi click hạng mục thông báo

#### Request Parameters
Không có request params. `bot_id` lấy từ session (`getBotId()`).

#### Response mẫu (thành công)
```json
{
  "status": true,
  "notifySettingData": {
    "id": 123,
    "user_id": 1,
    "admin_id": 1,
    "bot_id": 456,
    "app_notification_settings": 1,
    "chatWork_notification_settings": 1,
    "pc_notification_settings": 1,
    "notification_schedule": 0,
    "schedule_chat_work": 0,
    "schedule_pc": 0,
    "is_notify_chat11": 1,
    "chat_1_1": ["0", "1", "2", "3"],
    "is_notify_add_friend": 1,
    "add_friends": ["0", "1", "2", "3"],
    "is_notify_send_all": 1,
    "send_all": ["0"],
    "is_notify_qr_code": 1,
    "when_adding_friends": ["1", "5", "10"],
    "is_notify_form": 1,
    "answer_form": ["2", "3"],
    "is_notify_salon_booking": 1,
    "salon_booking": ["0", "1", "4"],
    "is_notify_lesson_booking": 1,
    "lesson_booking": ["0", "1", "4"],
    "is_notify_calendar_booking": 1,
    "booking_calendar": ["0", "1", "4", "6"],
    "is_notify_event_booking": 1,
    "event_reservation_management": ["0", "1", "2", "3", "4"],
    "is_notify_items": 1,
    "settlement": ["5", "6", "7"],
    "is_notify_action_schedule": 1,
    "action_schedule": ["1", "2"],
    "is_notify_conversion": 1,
    "conversion": ["3", "4"],
    "is_notify_asp": 1,
    "asp": ["1", "2", "3"],
    "is_notify_send_error": 1,
    "limitMessage": ["0", "1", "2"],
    "is_notify_system_notify": 1,
    "systemNotify": ["1", "2"],
    "system_notification": [],
    "notification_room_url": "https://www.chatwork.com/...",
    "api_token": "xxxxx",
    "is_all_qrcode_new": 0,
    "is_all_form_new": 0,
    "is_all_schedule_new": 0,
    "is_all_conversion_new": 0
  }
}
```

#### Cách lưu trữ dữ liệu chi tiết sự kiện
Mỗi hạng mục thông báo lưu danh sách ID sự kiện dưới dạng **chuỗi comma-separated** trong DB (VD: `"0,1,2,3"`). Khi API trả về, chúng được `explode(',')` thành mảng. Giá trị ID là số nguyên — mỗi số tương ứng với 1 sự kiện/checkbox cụ thể.

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Exception bất kỳ | `{"status": false, "msg": "{error message}"}` |

---

### EP-03: POST `/basic/notify-setting-receive`
- **Controller**: `Basic\NotifySettingController@saveNotifySettingReceive`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lưu cài đặt phương tiện nhận thông báo (bật/tắt smartphone/ChatWork/PC) và thời gian thông báo (timing). Nếu thay đổi timing → tính toán `next_notify_time` mới. Khi bật lại phương tiện đã tắt → cập nhật trạng thái `mobile_notify` records. Sau khi lưu → cập nhật `count_app_notify` trong bảng `bots`.
- **Liên kết UI**: SCR-NTF-01 → Phần 1: Toggle ON/OFF + dropdown timing

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `app_notification_settings` | Body | Integer (0/1) | Có | Bật/tắt smartphone (0 = ON, 1 = OFF trong DB) | Không có validation rõ ràng |
| `chatWork_notification_settings` | Body | Integer (0/1) | Có | Bật/tắt ChatWork (0 = ON, 1 = OFF trong DB) | Không có validation rõ ràng |
| `pc_notification_settings` | Body | Integer (0/1) | Có | Bật/tắt PC desktop (0 = ON, 1 = OFF trong DB) | Không có validation rõ ràng |
| `notification_schedule` | Body | Integer (0-7) | Không | Timing smartphone: 0=realtime, 1=15m, 2=30m, 3=1h, 4=3h, 5=6h, 6=12h, 7=24h | Default 0 nếu empty |
| `schedule_chat_work` | Body | Integer (0-7) | Không | Timing ChatWork (cùng mapping với smartphone) | Default 0 nếu empty |
| `schedule_pc` | Body | Integer (0-7) | Không | Timing PC desktop (cùng mapping với smartphone) | Default 0 nếu empty |

#### Request mẫu
```json
{
  "app_notification_settings": 0,
  "chatWork_notification_settings": 0,
  "pc_notification_settings": 0,
  "notification_schedule": 0,
  "schedule_chat_work": 0,
  "schedule_pc": 0
}
```

#### Response mẫu (thành công)
```json
{
  "success": true
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Exception bất kỳ | `{"success": false, "message": "{error message}"}` |

---

### EP-04: POST `/basic/notify-setting-receive-page`
- **Controller**: `Basic\NotifySettingController@saveNotifySettingReceivePage`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lưu cài đặt hạng mục thông báo chi tiết theo từng "page" (tên hạng mục). Mỗi lần gọi chỉ cập nhật 1 hạng mục. Dữ liệu chi tiết (danh sách sự kiện) được lưu dưới dạng comma-separated string. Sau khi lưu → cập nhật `count_app_notify` trong bảng `bots`.
- **Liên kết UI**: SCR-NTF-01 → Phần 2: Toggle ON/OFF hạng mục + tick/bỏ tick checkbox sự kiện

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `page` | Body | String | Có | Tên hạng mục: `chat_11`, `addFriend`, `sendAll`, `qrCode`, `form`, `salonBooking`, `lessonBooking`, `eventBooking`, `bookingCalendar`, `items`, `actionSchedule`, `conversion`, `asp`, `limitMessage`, `systemNotify` | Switch case — giá trị không khớp sẽ bị bỏ qua |
| `isAllNew` | Body | Boolean/Truthy | Không | Cờ cho việc cập nhật "tự động tick mục mới thêm" — chỉ áp dụng cho `qrCode`, `form`, `actionSchedule`, `conversion` | Không có validation |
| `is_notify_{page}` | Body | Integer (0/1) | Tùy page | Toggle bật/tắt toàn bộ hạng mục (VD: `is_notify_chat11`, `is_notify_add_friend`) | Không có validation |
| `{detail_field}` | Body | Array of strings | Tùy page | Danh sách ID sự kiện đã tick (VD: `chat_1_1: ["0","1","2"]`) | Được `implode(",")` khi lưu |

#### Mapping page → fields cập nhật

| page | Toggle field | Detail field | "Auto new" fields |
|------|-------------|-------------|-------------------|
| `chat_11` | `is_notify_chat11` | `chat_1_1` | — |
| `addFriend` | `is_notify_add_friend` | `add_friends` | — |
| `sendAll` | `is_notify_send_all` | `send_all` | — |
| `qrCode` | `is_notify_qr_code` | `when_adding_friends` | `is_all_qrcode_new`, `update_select_qr_new` |
| `form` | `is_notify_form` | `answer_form` | `is_all_form_new`, `update_select_form_new` |
| `salonBooking` | `is_notify_salon_booking` | `salon_booking` | — |
| `lessonBooking` | `is_notify_lesson_booking` | `lesson_booking` | — |
| `eventBooking` | `is_notify_event_booking` | `event_reservation_management` | — |
| `bookingCalendar` | `is_notify_calendar_booking` | `booking_calendar` | — |
| `items` | `is_notify_items` | `settlement` | — |
| `actionSchedule` | `is_notify_action_schedule` | `action_schedule` | `is_all_schedule_new`, `update_select_schedule_new` |
| `conversion` | `is_notify_conversion` | `conversion` | `is_all_conversion_new`, `update_select_conversion_new` |
| `asp` | `is_notify_asp` | `asp` | — |
| `limitMessage` | `is_notify_send_error` | `limitMessage` | — |
| `systemNotify` | `is_notify_system_notify` | `systemNotify` | — |

#### Request mẫu (cập nhật hạng mục chat 1:1)
```json
{
  "page": "chat_11",
  "is_notify_chat11": 1,
  "chat_1_1": ["0", "1", "2", "3"]
}
```

#### Request mẫu (cập nhật "tự động tick mục mới" cho QR code)
```json
{
  "page": "qrCode",
  "isAllNew": true,
  "is_all_qrcode_new": 1
}
```

#### Response mẫu (thành công)
```json
{
  "success": true
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Exception bất kỳ | `{"success": false, "message": "{error message}"}` |

---

### EP-05: POST `/basic/notify-setting`
- **Controller**: `Basic\NotifySettingController@saveNotifySettings`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Phiên bản **cũ** (legacy) — lưu toàn bộ cài đặt trong 1 request và redirect (không AJAX). Hiện tại UI mới sử dụng EP-03 + EP-04 thay thế. Endpoint này vẫn hoạt động nhưng có thể không còn được gọi từ frontend hiện tại.
- **Liên kết UI**: Không sử dụng trên UI mới

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `app_notification_settings` | Body | Integer | Có | Bật/tắt smartphone | — |
| `chatWork_notification_settings` | Body | Integer | Có | Bật/tắt ChatWork | — |
| `setting_time_send` | Body | Integer | Không | Cài đặt thời gian gửi chat | — |
| `notification_schedule` | Body | Integer | Không | Timing smartphone | Default 0 |
| `notification_schedule_chat_work` | Body | Integer | Không | Timing ChatWork | Default 0 |
| `when_adding_friends` | Body | Array | Không | QR code events | `implode(",")` |
| `chat_1_1` | Body | Array | Không | Chat 1:1 events | `implode(",")` |
| `answer_form` | Body | Array | Không | Form events | `implode(",")` |
| `event_reservation_management` | Body | Array | Không | Event booking events | `implode(",")` |
| `settlement` | Body | Array | Không | Items events | `implode(",")` |
| `system_notification` | Body | Array | Không | System notification events | `implode(",")` |
| `booking_calendar` | Body | Array | Không | Calendar booking events | `implode(",")` |

#### Response
Redirect về route `notifySetting` (EP-01). Nếu lỗi → redirect về 404.

---

### EP-06: GET `/basic/getLandingBot`
- **Controller**: `Basic\NotifySettingController@getLandingBot`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lấy toàn bộ landing pages (QR code) của bot hiện tại. Dùng để populate danh sách checkbox động cho hạng mục「QRコードアクション」.
- **Liên kết UI**: SCR-NTF-01 → Hạng mục 4: khi click vào「QRコードアクション」

#### Request Parameters
Không có params. `bot_id` lấy từ session.

#### Response mẫu (thành công)
```json
{
  "status": true,
  "data": [
    {
      "id": 1,
      "bot_id": 456,
      "name": "QR Code 1",
      "path_landing": "/qr_landing/...",
      "created_at": "2024-01-15 10:30:00",
      "updated_at": "2024-01-15 10:30:00"
    },
    {
      "id": 2,
      "bot_id": 456,
      "name": "Landing Page 2",
      "path_landing": "/landing/...",
      "created_at": "2024-02-01 08:00:00",
      "updated_at": "2024-02-01 08:00:00"
    }
  ]
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Exception bất kỳ | `{"status": false, "msg": "{error message}"}` |

---

### EP-07: GET `/basic/getFormAnswerBot`
- **Controller**: `Basic\NotifySettingController@getFormAnswerBot`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lấy toàn bộ form trả lời của bot hiện tại. Dùng để populate danh sách checkbox động cho hạng mục「フォーム作成」.
- **Liên kết UI**: SCR-NTF-01 → Hạng mục 5: khi click vào「フォーム作成」

#### Request Parameters
Không có params. `bot_id` lấy từ session.

#### Response mẫu (thành công)
```json
{
  "status": true,
  "data": [
    {
      "id": 1,
      "bot_id": 456,
      "name": "Đăng ký tư vấn",
      "created_at": "2024.01.15",
      "updated_at": "2024-01-15 10:30:00"
    }
  ]
}
```

**Lưu ý**: Model `FormAnswer` có accessor `getCreatedAtAttribute` format `created_at` thành `Y.m.d`.

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Exception bất kỳ | `{"status": false, "msg": "{error message}"}` |

---

### EP-08: GET `/basic/getActionScheduleBot`
- **Controller**: `Basic\NotifySettingController@getActionScheduleBot`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lấy toàn bộ action schedules của bot. Dùng cho hạng mục「アクションスケジュール実行」.
- **Liên kết UI**: SCR-NTF-01 → Hạng mục 10: khi click vào「アクションスケジュール実行」

#### Request Parameters
Không có params. `bot_id` lấy từ session.

#### Response mẫu (thành công)
```json
{
  "status": true,
  "data": [
    {
      "id": 1,
      "bot_id": 456,
      "name": "Gửi nhắc nhở hàng tuần",
      "start_date": "2024-01-01",
      "start_time": "09:00:00",
      "repeat_type": "week",
      "created_at": "2024-01-01 00:00:00",
      "updated_at": "2024-01-01 00:00:00"
    }
  ]
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Exception bất kỳ | `{"status": false, "msg": "{error message}"}` |

---

### EP-09: GET `/basic/getConversionBot`
- **Controller**: `Basic\NotifySettingController@getConversionBot`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lấy danh sách conversions của bot (chỉ `name` và `id`). Dùng cho hạng mục「コンバージョン」.
- **Liên kết UI**: SCR-NTF-01 → Hạng mục 11: khi click vào「コンバージョン」

#### Request Parameters
Không có params. `bot_id` lấy từ session.

#### Response mẫu (thành công)
```json
{
  "status": true,
  "data": [
    {
      "id": 1,
      "name": "Đăng ký thành viên"
    },
    {
      "id": 2,
      "name": "Mua hàng"
    }
  ]
}
```

**Lưu ý**: Khác với EP-06, EP-07, EP-08 trả về toàn bộ fields, EP-09 chỉ `select('name', 'id')`.

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Exception bất kỳ | `{"status": false, "msg": "{error message}"}` |

---

### EP-10: GET `/basic/notify-setting-chatwork`
- **Controller**: `Basic\NotifySettingController@notifySettingChatwork`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Render trang cài đặt liên kết ChatWork. Truyền danh sách landing pages và form answers vào view.
- **Liên kết UI**: SCR-NTF-01 → Nút「連携設定」→ mở trang ChatWork settings

#### Request Parameters
Không có params.

#### Response
Trả về HTML (Blade view `basic.notify_setting.setting_chatwork`) với biến `$landingData` và `$formAnswerData`.

---

### EP-11: POST `/ajax/notify/save-url-chat-work`
- **Controller**: `Basic\NotifySettingController@ajaxSaveUrlChatWork`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Mô tả**: Lưu URL room ChatWork để nhận thông báo. URL này chứa room ID dùng cho ChatWork API.
- **Liên kết UI**: Trang cài đặt ChatWork → form nhập URL

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `notification_room_url` | Body | String | Có | URL room ChatWork (VD: `https://www.chatwork.com/#!rid123456`) | Không có validation |

#### Request mẫu
```json
{
  "notification_room_url": "https://www.chatwork.com/#!rid123456"
}
```

#### Response mẫu (thành công)
```json
{
  "success": true,
  "url": "https://www.chatwork.com/#!rid123456"
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | Exception | `{"success": false, "msg": "{error message}"}` |

**Lưu ý**: Lỗi trả HTTP 200 (không phải 500), cần kiểm tra field `success` để biết kết quả.

---

### EP-12: POST `/ajax/notify/save-api-token-chat-work`
- **Controller**: `Basic\NotifySettingController@ajaxSaveApiTokenChatWork`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Mô tả**: Lưu API token ChatWork để gửi tin nhắn qua ChatWork API.
- **Liên kết UI**: Trang cài đặt ChatWork → form nhập API token

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `api_token` | Body | String | Có | ChatWork API token | Không có validation |

#### Request mẫu
```json
{
  "api_token": "xxxxxxxxxxxxxxxxxxxx"
}
```

#### Response mẫu (thành công)
```json
{
  "success": true,
  "api_token": "xxxxxxxxxxxxxxxxxxxx"
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | Exception | `{"success": false, "msg": "{error message}"}` |

---

### EP-13: POST `/ajax/notify/save-type_notify_send_chatwork`
- **Controller**: `Basic\NotifySettingController@ajaxChangeTypeSendChatwork`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Mô tả**: Thay đổi kiểu gửi thông báo ChatWork (sử dụng URL room hay API token).
- **Liên kết UI**: Trang cài đặt ChatWork → chọn kiểu gửi

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `type_notify_send_chatwork` | Body | Integer (0/1) | Có | 0 = gửi qua URL room, 1 = gửi qua API token (suy luận) | Không có validation |

#### Response mẫu (thành công)
```json
{
  "success": true,
  "type_notify_send_chatwork": 0
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | Exception | `{"success": false, "msg": "{error message}"}` |

---

### EP-14: POST `/ajax/notify/test-send-chatwork`
- **Controller**: `Basic\NotifySettingController@ajaxTestSendChatwork`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Mô tả**: Gửi tin nhắn test đến room ChatWork đã cấu hình. Lấy room ID từ `notification_room_url` (phần sau `#!rid`). Sử dụng ChatWork API v2 (`POST /v2/rooms/{roomId}/messages`). Token sử dụng: `api_token` từ DB hoặc fallback env `TOKEN_API_BOT_CHATWORK`.
- **Liên kết UI**: Trang cài đặt ChatWork → nút test gửi

#### Request Parameters
Không có params. Sử dụng `notification_room_url` và `api_token` đã lưu trong DB.

#### Điều kiện tiên quyết
- `chatWork_notification_settings` phải = 0 (ON) trong DB
- `notification_room_url` phải đã được cấu hình và chứa `#!rid{roomId}`

#### Response mẫu (thành công)
```json
{
  "success": true
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | ChatWork chưa bật hoặc thiếu room URL | `{"success": false, "msg": "エルメ 通知テスト送信失敗"}` |
| 200 | ChatWork API trả lỗi | `{"success": false, "msg": "エルメ 通知テスト送信失敗"}` |
| 200 | Exception | `{"success": false, "msg": "{error message}"}` |

---

### EP-15: GET `/push/get-vapid-public-key`
- **Controller**: `Basic\NotifySettingController@getVapidPublicKey`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Mô tả**: Trả về VAPID public key cho Web Push notification. Client sử dụng key này để đăng ký Push subscription.
- **Liên kết UI**: SCR-NTF-01 → Nút「PC設定」→ cài đặt browser push notification

#### Request Parameters
Không có params.

#### Response mẫu (thành công)
```json
{
  "key": "BGxGRmh5Q..."
}
```

---

### EP-16: POST `/push/subscribe-push-notification`
- **Controller**: `Basic\NotifySettingController@subscribePushNotification`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Mô tả**: Đăng ký nhận PC desktop push notification. Lưu push subscription vào bảng `push_subscriptions` (qua package `laravel-notification-channels/webpush`). Kiểm tra không tạo duplicate subscription cho cùng user + public key.
- **Liên kết UI**: SCR-NTF-01 → Cài đặt PC desktop → cho phép browser notification

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `endpoint` | Body | String | Có | Push subscription endpoint URL | — |
| `keys.p256dh` | Body | String | Có | Public key của subscription | — |
| `keys.auth` | Body | String | Có | Auth secret của subscription | — |

#### Request mẫu
```json
{
  "endpoint": "https://fcm.googleapis.com/fcm/send/...",
  "keys": {
    "p256dh": "BNcR...",
    "auth": "tBH..."
  }
}
```

#### Response mẫu (thành công)
```json
{
  "success": true
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | User chưa đăng nhập | `{"success": false}` |

---

### EP-17: POST `/push/unsubscribe-push-notification`
- **Controller**: `Basic\NotifySettingController@unsubscribePushNotification`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Mô tả**: Hủy đăng ký push notification. Xóa subscription khỏi bảng `push_subscriptions` dựa trên user ID + public key.
- **Liên kết UI**: SCR-NTF-01 → Cài đặt PC desktop → tắt browser notification

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `pushKey` | Body | String | Có | Public key của subscription cần hủy | — |

#### Request mẫu
```json
{
  "pushKey": "BNcR..."
}
```

#### Response mẫu (thành công)
```json
{
  "success": true
}
```

---

### EP-18: POST `/api/notify/push-notify`
- **Controller**: `Basic\NotifySettingController@pushNotification`
- **Middleware**: `api`
- **Mô tả**: **API nội bộ** — gọi từ background job (Spring Boot) để tạo bản ghi push notification cho user. Tìm bot → tìm admin user → insert vào bảng `notification_pc`. **Không thực sự gửi** push notification ngay — chỉ lưu record.
- **Liên kết UI**: Không gọi trực tiếp từ UI

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `notifyTitle` | Body | String | Có | Tiêu đề thông báo | — |
| `notifyContent` | Body | String | Có | Nội dung thông báo | — |
| `botId` | Body | Integer | Có | Bot ID | — |
| `userId` | Body | Integer | Không | User ID (chỉ dùng cho log, user thực sự lấy từ bot.admin_id) | — |

#### Request mẫu
```json
{
  "notifyTitle": "新規友だち追加",
  "notifyContent": "新しい友だちが追加されました。",
  "botId": 456,
  "userId": 1
}
```

#### Response
Không có response body rõ ràng (void method).

---

## Middleware phân tích

| Middleware | Mô tả | Áp dụng cho |
|-----------|-------|------------|
| `web` | Session-based authentication + CSRF | Tất cả EP trừ EP-18 |
| `NotifyChatworkRequestTimeSlow` | Đo thời gian xử lý request. Nếu > 4 giây → gửi thông báo slow request (qua hàm `notifySlowRequestCommon`) | Tất cả EP trừ EP-18 |
| `LogRequestMultipart` | Ghi log multipart request (chi tiết chưa xác minh) | EP-01 đến EP-10 |
| `api` | API authentication (không session, thường dùng JWT hoặc token) | EP-18 |

## Liên kết UI ↔ API

| Màn hình | Action | Endpoint | Ghi chú |
|---------|--------|----------|---------|
| SCR-NTF-01 | Trang load | EP-01 → EP-02 | Render HTML rồi AJAX lấy data |
| SCR-NTF-01 | Toggle ON/OFF phương tiện (smartphone/ChatWork/PC) | EP-03 | Auto-save khi thay đổi toggle |
| SCR-NTF-01 | Chọn dropdown timing | EP-03 | Auto-save khi thay đổi dropdown |
| SCR-NTF-01 | Toggle ON/OFF hạng mục thông báo | EP-04 | `page` param xác định hạng mục |
| SCR-NTF-01 | Tick/bỏ tick checkbox sự kiện chi tiết | EP-04 | `page` param + detail field array |
| SCR-NTF-01 | Tick "tự động tick mục mới thêm" | EP-04 | `isAllNew=true` + `is_all_{type}_new` |
| SCR-NTF-01 | Click「QRコードアクション」 | EP-06 | Load danh sách QR code/landing |
| SCR-NTF-01 | Click「フォーム作成」 | EP-07 | Load danh sách forms |
| SCR-NTF-01 | Click「アクションスケジュール実行」 | EP-08 | Load danh sách action schedules |
| SCR-NTF-01 | Click「コンバージョン」 | EP-09 | Load danh sách conversions |
| SCR-NTF-01 | Click「連携設定」(ChatWork) | EP-10 | Mở trang cài đặt ChatWork |
| Trang ChatWork | Lưu URL room | EP-11 | AJAX save |
| Trang ChatWork | Lưu API token | EP-12 | AJAX save |
| Trang ChatWork | Chọn kiểu gửi | EP-13 | AJAX save |
| Trang ChatWork | Nút test gửi | EP-14 | Gửi test message qua ChatWork API |
| SCR-NTF-01 | Click「PC設定」 | EP-15, EP-16, EP-17 | VAPID key → subscribe/unsubscribe |

## Giá trị enum cho Notification Schedule (timing)

| Giá trị DB | Ý nghĩa | Text JP trên UI |
|-----------|---------|----------------|
| 0 | Thời gian thực (realtime) | 「リアルタイム」 |
| 1 | Mỗi 15 phút | 「15分ごと」 |
| 2 | Mỗi 30 phút | 「30分ごと」 |
| 3 | Mỗi 1 giờ | 「1時間ごと」 |
| 4 | Mỗi 3 giờ | 「3時間ごと」 |
| 5 | Mỗi 6 giờ | 「6時間ごと」 |
| 6 | Mỗi 12 giờ | 「12時間ごと」 |
| 7 | Mỗi 24 giờ | 「24時間ごと」 |

## Giá trị đảo ngược — toggle ON/OFF

**Quan trọng**: Trong DB, các cột `app_notification_settings`, `chatWork_notification_settings`, `pc_notification_settings` sử dụng logic đảo:
- **DB = 0** → Phương tiện **BẬT** (ON)
- **DB = 1** → Phương tiện **TẮT** (OFF)

Khi EP-02 (`getNotifySetting`) trả về, code **đảo ngược** giá trị: `0 → 1` (ON), `khác 0 → 0` (OFF). Do đó client nhận: 1 = ON, 0 = OFF (logic thông thường).

Khi client gửi EP-03 (`saveNotifySettingReceive`), giá trị được lưu **trực tiếp** vào DB mà **không đảo lại** — nghĩa là client gửi logic "thường" (1=ON, 0=OFF) nhưng DB sẽ nhận đúng giá trị đó. Tuy nhiên, ở EP-02, code đảo lại lần nữa, nên kết quả cuối vẫn nhất quán cho client.
