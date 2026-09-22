# FA-044 — Change Bot / Đổi LINE Official Account (LOA変更) — API Spec

> **Nguồn phân tích (v2)**
> - Web: `src/web/sns-line` @ nhánh **`release_step_20260805`**, commit **`da839e26e4`** (2026-08-18)
> - Job: `src/job/linect-service` @ nhánh **`release-t07-2026`**, commit **`debe45bc`** (2026-08-13) — chỉ dùng để xác định ranh giới trách nhiệm
> - Ngày cập nhật spec: **2026-08-19**
>
> **Phạm vi**: thế hệ code hiện hành của tính năng đổi LOA — view `resources/views/admin/bots/change_bot_new/index.blade.php` + JS `public/_assets/modules/change_bots/js/change_new.js` + `App\Http\Controllers\Ajax\ChangeBotController`. Các route thế hệ cũ liệt kê ở **mục 6**.
>
> ⚠ **Đính chính lớn so với bản spec trước**: tính năng **ĐÃ HOÀN THIỆN và ĐANG CHẠY PRODUCTION**. Bản spec v1 (dựa trên nhánh `release_step_20260623`) kết luận sai rằng backend là "dummy" và rằng EP-04/EP-05/EP-06 là code chết. Xem **mục 7 — Thay đổi so với bản spec trước**.
>
> Mức tin cậy mặc định: **Cao** (đọc trực tiếp source).

---

## 1. Prefix & nhóm route — xác định thực tế

Toàn bộ route của thế hệ hiện hành nằm trong nhóm:

```php
// src/web/sns-line/routes/web.php:81
Route::middleware(['NotifyChatworkRequestTimeSlow'])->group(function () {
    // src/web/sns-line/routes/web.php:96
    Route::group(['prefix' => '/admin', 'middleware' => ['admin_access', 'https_protocol', 'check_remember_token']], function () {
        // ... khai báo route change-bot tại dòng 208–223
    });
});
```

Vì nhóm có `prefix => '/admin'`, **URL thật có thêm tiền tố `/admin`**:

| Khai báo trong `routes/web.php` | URL thật | JS gọi (bằng chứng) |
|---|---|---|
| `/ajax/change-bot/init` (`:212`) | `/admin/ajax/change-bot/init` | `change_new.js:112` |
| `/ajax/change-bot/validate` (`:213`) | `/admin/ajax/change-bot/validate` | `change_new.js:202` |
| `/ajax/change-bot/check-webhook` (`:214`) | `/admin/ajax/change-bot/check-webhook` | `change_new.js:242` |
| `/ajax/change-bot/set-webhook` (`:215`) | `/admin/ajax/change-bot/set-webhook` | `change_new.js:187` |
| `/ajax/change-bot/execute` (`:216`) | `/admin/ajax/change-bot/execute` | `change_new.js:286` |
| `/ajax/change-bot/progress` (`:217`) | `/admin/ajax/change-bot/progress` | `change_new.js:332` |
| `/ajax/change-bot/delete-reservation` (`:218`) | `/admin/ajax/change-bot/delete-reservation` | `change_new.js:364` |
| `/ajax/change-bot/execute-reservation` (`:219`) | `/admin/ajax/change-bot/execute-reservation` | `change_new.js:383` |

Endpoint `POST /admin/step2-check-friend` thuộc nhóm **khác, không có prefix**:

```php
// src/web/sns-line/routes/web.php:835
Route::middleware(['LogRequestMultipart'])->group(function () {
    // src/web/sns-line/routes/web.php:1877
    Route::middleware(['check_login', 'check_remember_token'])->group(function () {
        // src/web/sns-line/routes/web.php:1885
        Route::post('/admin/step2-check-friend', ['as' => 'step2CheckFriend', 'uses' => 'Admin\BotController@step2CheckFriend']);
    });
});
```

→ URL giữ nguyên `/admin/step2-check-friend` (xác nhận chéo: `public/js/admin/add_bot/add_bot.js:329`).

---

## 2. Bảng tổng hợp endpoints

> Cột **Trạng thái sử dụng thực tế** dựa trên bằng chứng grep JS/Blade gọi tới endpoint, không phỏng đoán.

| ID | Method | URL | Mô tả | Middleware | Xác thực | Trạng thái sử dụng thực tế |
|----|--------|-----|-------|-----------|----------|---------------------------|
| EP-01 | GET | `/admin/change-bots-new/{id}` | Trang wizard đổi LOA (SPA Vue). `{id}` = Hashids của `bots.id` | `NotifyChatworkRequestTimeSlow`, `admin_access`, `https_protocol`, `check_remember_token` | Session + ownership bot | **Đang dùng** — vào từ `resources/views/basic/modal-campaign-changebot.blade.php:143` và `public/js/admin/add_bot/add_bot.js:356` |
| EP-02 | GET | `/admin/change-bot-sub/{id}` | Mở wizard kết nối LOA cũ (view `bot_add_v3`) | như EP-01 | như EP-01 | **Mồ côi (legacy)** — grep toàn `resources/` + `public/` **không còn** chỗ nào trỏ tới URL này sau khi `goToInput()` được sửa (`change_new.js:157-161`). Route vẫn mở |
| EP-03 | GET | `/admin/ajax/change-bot/init` | Khởi tạo dữ liệu trang: cờ campaign, reservation, tiến độ | như EP-01 | Session; `bot_id` lấy từ **session**, không tin client | **Đang dùng** (`change_new.js:112`) |
| EP-04 | POST | `/admin/ajax/change-bot/validate` | Xác thực credential LOA mới (Messaging API + LINE Login), trả thông tin OA + `webhook_url` | như EP-01 | Session | **Đang dùng** (`change_new.js:202`) |
| EP-05 | POST | `/admin/ajax/change-bot/set-webhook` | Tự động ghi Webhook endpoint cho LOA mới | như EP-01 | Session | **Đang dùng** — debounce 600ms khi gõ credential (`change_new.js:175-194`) |
| EP-06 | POST | `/admin/ajax/change-bot/execute` | **Tạo bản ghi `schedule_change_bots`** (đổi ngay hoặc đặt lịch) | như EP-01 | Session + so khớp `bot_id` | **Đang dùng** (`change_new.js:286`) — **đường tạo bản ghi chính** của màn hình `change_bot_new` |
| EP-07 | GET | `/admin/ajax/change-bot/progress` | Poll tiến độ xử lý (3 giây/lần) | như EP-01 | Session, scope theo `bot_id` session | **Đang dùng** (`change_new.js:332`) |
| EP-08 | POST | `/admin/ajax/change-bot/delete-reservation` | Huỷ đặt lịch (`status = CANCEL`) | như EP-01 | Session, scope theo `bot_id` session | **Đang dùng** (`change_new.js:364`) |
| EP-09 | POST | `/admin/ajax/change-bot/execute-reservation` | Thực thi ngay một đặt lịch (`DRAFT → WAITING`) | như EP-01 | Session, scope theo `bot_id` session | **Đang dùng** (`change_new.js:383`) |
| EP-10 | POST | `/admin/step2-check-friend` | Polling kiểm tra kết bạn ở wizard kết nối bot. **Nhánh `botIdChange` + `type_change`** cũng tạo `schedule_change_bots` | `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`, `check_login`, `check_remember_token` | Session | **Đang dùng cho luồng THÊM BOT** (`add_bot.js:329`, `add_bot_v5.js:1114`, `step5qr.js:52`). **Nhánh đổi-LOA hiện MỒ CÔI** — xem ghi chú dưới |
| EP-11 | POST | `/admin/ajax/change-bot/check-webhook` | **MỚI** — kiểm tra Webhook của LOA mới đã bật chưa (tách khỏi EP-04) | như EP-01 | Session | **Đang dùng** (`change_new.js:242`) |

### Ghi chú quan trọng — đường nào tạo bản ghi `schedule_change_bots`?

Tồn tại **hai** đoạn code `ScheduleChangeBot::create()`:

| Đoạn code | Vị trí | Màn hình phục vụ | Còn sống? |
|---|---|---|---|
| `Ajax\ChangeBotController@execute` | `app/Http/Controllers/Ajax/ChangeBotController.php:232-244` | `change_bot_new/index.blade.php` (SPA `change_new.js`) | ✅ **Đang chạy** — `goToInput()` (`change_new.js:157-161`) nay đặt `this.currentStep = 'input'` (trước đây redirect sang EP-02), nên chuỗi `select → input → webhook → confirm → execute` chạy trọn trong 1 trang |
| `Admin\BotController@step2CheckFriend` (nhánh `botIdChange`) | `app/Http/Controllers/Admin/BotController.php:4803-4816` | `bot_add_v3.blade.php` + `add_bot.js`, mở qua EP-02 | ⚠ **Mồ côi** — `bot_add_v3` chỉ được render bởi `adminChangeBotSub` (`BotController.php:7298`), mà EP-02 **không còn link nào trỏ tới**. `add_bot_v5.js` (view `bot_add_v5`) tuy có gửi `botIdChange` nhưng **không gửi `type_change`** (`add_bot_v5.js:1112-1132`) nên rẽ nhánh `saveStep1()`, không tạo `ScheduleChangeBot`; ngoài ra `botAddV2()` không truyền `$bot_id` vào view nên `#botIdChange` luôn rỗng ở `bot_add_v5` (`BotController.php:518-527`, `bot_add_v5.blade.php:19`) |

**Kết luận**: với màn hình `change_bot_new`, bản ghi `schedule_change_bots` **do EP-06 (`Ajax\ChangeBotController@execute`) tạo**. Mức tin cậy: **Cao**.

---

## 3. Chi tiết từng endpoint

### EP-01 — GET `/admin/change-bots-new/{id}`

- **Controller**: `Admin\BotController@adminChangeNewBot` — `src/web/sns-line/app/Http/Controllers/Admin/BotController.php:7256`
- **Route**: `src/web/sns-line/routes/web.php:208` (name `change.bots.new`)
- **View**: `resources/views/admin/bots/change_bot_new/index.blade.php`

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú / validation |
|-----|--------|------|----------|----------------------|
| `id` | path | string (Hashids) | Có | `Hashids::decode($id)[0]`; hash sai → `$botId = null` → redirect |
| `bot_slot_id` | query | int | Không | Mã hoá lại thành `hash_id` truyền vào view |
| `type` | query | string | Không | Giá trị dùng: `change_sub` → SPA vào thẳng bước `processing` (`change_new.js:135`) |
| `type_change` | query | string | Không | `immediate` \| `scheduled` |
| `change_success` | query | int | Không | `1` → SPA khởi động ở bước `processing` (`change_new.js:4`) |

**Request mẫu**

```
GET /admin/change-bots-new/aBcD3fG?type=change_sub&change_success=1
```

**Response thành công**: HTML. Biến truyền vào view: `bot_slot_id`, `type`, `typeChange`, `bot_id`, `username`, `hash_id`, `changeSuccess` (`BotController.php:7271`).

**Lỗi**

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 302 → `/basic/overview` | — | `$botId != getBotId()` **hoặc** bot không tồn tại **hoặc** `userCanAccessChangeBot()` = false (`BotController.php:7262-7264`) |

**LINE API bên ngoài**: không gọi.

---

### EP-02 — GET `/admin/change-bot-sub/{id}` *(legacy, không còn link từ UI)*

- **Controller**: `Admin\BotController@adminChangeBotSub` — `BotController.php:7275`
- **Route**: `routes/web.php:209` (name `change.bots.sub`)
- **View**: `resources/views/admin/bots/bot_add_v3.blade.php` (JS `public/js/admin/add_bot/add_bot.js`, nạp tại `bot_add_v3.blade.php:739`)
- **View chặn**: `resources/views/admin/bots/change_bot_plan_blocked.blade.php`

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|-----|--------|------|----------|---------|
| `id` | path | string (Hashids) | Có | Hashids của `bots.id` |
| `type_change` | query | string | Không | `immediate` \| `scheduled` — quyết định guard gói Free |
| `bot_slot_id` | query | int | Không | |
| `type` | query | string | Không | |

**Response thành công**: HTML view `admin.bots.bot_add_v3` (`BotController.php:7298`).

**Lỗi**

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 302 → `/basic/overview` | — | Không sở hữu bot / bot không tồn tại (`BotController.php:7281-7283`) |
| 200 (view chặn) | View `change_bot_plan_blocked` | `plan_type === 2` **và** (`type_change === 'scheduled'` **hoặc** campaign đã hết) — `BotController.php:7288-7292` |

**LINE API bên ngoài**: không gọi trực tiếp.

---

### EP-03 — GET `/admin/ajax/change-bot/init`

- **Controller**: `Ajax\ChangeBotController@init` — `app/Http/Controllers/Ajax/ChangeBotController.php:39`
- **Route**: `routes/web.php:212` (name `changeBot.init`)

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|----------|-----------|
| `bot_id` | query | int | Không | JS gửi nhưng controller **không dùng** — bot lấy từ `getBotId()` (session) |
| `type` | query | string | Không | `=== 'change_sub'` → mảng `$status` được mở rộng thêm `DONE`; nhưng `$status` là **biến chết** vì dòng lọc bị comment (`ChangeBotController.php:54`) |

**Request mẫu**

```
GET /admin/ajax/change-bot/init?bot_id=1234&type=change_sub
```

**Response thành công** (`ChangeBotController.php:85-98`)

```json
{
  "success": true,
  "data": {
    "is_free_plan": false,
    "campaign_countdown": "06 日 15 時間 39 分",
    "is_processing": true,
    "progress": 45,
    "reservation": {
      "exists": true,
      "date": "2026-08-10 09:12:33",
      "bot_name": "テストアカウント",
      "bot_id_line": "@test_oa",
      "plan_name": "コミュニケーションプラン",
      "friend_count": 1180,
      "avatar_url": "https://profile.line-scdn.net/..."
    },
    "has_campaign": true,
    "schedule_id": 42,
    "schedule": {
      "id": 42,
      "bot_id": 1234,
      "type": 1,
      "status": 2,
      "progress": 45,
      "channel_id": "2009999999",
      "channel_secret": "<plaintext>",
      "channel_id_line_login": "2008888888",
      "channel_secret_line_login": "<plaintext>",
      "channel_id_new": "2001234567",
      "channel_secret_new": "<plaintext>",
      "channel_id_line_login_new": "2007654321",
      "channel_secret_line_login_new": "<plaintext>",
      "message_error": null,
      "created_at": "2026-08-10 09:12:33",
      "updated_at": "2026-08-10 09:20:00"
    },
    "campaign_change_bot": "2026-09-10 23:59:59"
  }
}
```

Khi bot chưa có bản ghi nào: `reservation` = `{"exists": false, "date": "", "bot_name": "", "bot_id_line": "", "plan_name": "", "friend_count": 0, "avatar_url": ""}`, `schedule = null`, `schedule_id = null`, `is_processing = false`, `progress = 0`.

**Lỗi**

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 404 | `Bot not found` (HttpException, không phải tiếng Nhật) | `Bots::where('id', getBotId())->where('is_deleted', 0)` không tìm thấy (`ChangeBotController.php:43-44`) |

**LINE API bên ngoài** (chỉ khi tồn tại `$schedule`, dùng **credential LOA MỚI** đã lưu trong DB):

| Helper | Endpoint LINE | Mục đích |
|--------|---------------|----------|
| `lineChanelAccessToken` | `POST https://api.line.me/v2/oauth/accessToken` | Lấy channel access token của LOA mới |
| `getLineInfoBot` | `GET https://api.line.me/v2/bot/info` | `displayName`, `basicId`, `pictureUrl` |
| `lineFollowers` | `GET https://api.line.me/v2/bot/insight/followers?date=YYYYMMDD` | `followers`, `blocks` → số bạn bè |
| `getLimitMessageLine` | `GET https://api.line.me/v2/bot/message/quota` | Quota → tên gói |

> **Hiệu năng**: mỗi lần load trang gọi 4 request đồng bộ tới LINE, không cache. Mức tin cậy: **Cao**.

---

### EP-04 — POST `/admin/ajax/change-bot/validate`

- **Controller**: `Ajax\ChangeBotController@validateChannel` — `ChangeBotController.php:101`
- **Route**: `routes/web.php:213` (name `changeBot.validate`)
- **FormRequest**: `App\Http\Requests\ChangeBotRequest`
- **Kích hoạt từ UI**: nút 「次に進む」 ở bước `input` (`index.blade.php:273`) → `validateAndConfirm()` (`change_new.js:196-229`) → thành công thì chuyển sang bước **`webhook`** (`change_new.js:224`)

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation rule |
|-----|--------|------|----------|-----------------|
| `channel_id` | body | string | Có | `required\|max:500` + rule tuỳ biến: không trùng `bots.channel_id` với `is_deleted = 0` (`ChangeBotRequest.php:33-43`) |
| `channel_secret` | body | string | Có | `required\|max:500` |
| `login_channel_id` | body | string | Có | `required\|max:500` |
| `login_channel_secret` | body | string | Có | `required\|max:500` |
| `bot_id` | body | int | Không | JS gửi, controller **không dùng** |
| `type` | body | string | Không | JS gửi, controller **không dùng** |

**Request mẫu**

```json
{
  "bot_id": 1234,
  "channel_id": "2001234567",
  "channel_secret": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
  "login_channel_id": "2007654321",
  "login_channel_secret": "f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3",
  "type": "immediate"
}
```

**Response thành công** (`ChangeBotController.php:129-153`)

```json
{
  "success": true,
  "data": {
    "bot_name": "テストアカウント",
    "bot_id_line": "@test_oa",
    "friend_count": 1180,
    "avatar_url": "https://profile.line-scdn.net/...",
    "channel_access_token": "eyJhbGciOi...",
    "channel_access_token_line_login": "eyJhbGciOi...",
    "plan_name": "コミュニケーションプラン",
    "webhook_url": "https://<DOMAIN_ENDPOINT_WEBHOOK>line/callback/add/0",
    "messaging_api": {
      "channel_id": "2001234567",
      "channel_name": "テストアカウント",
      "channel_secret_masked": "a1b••••••••••••5d6",
      "bot_id": "@test_oa",
      "status": "valid"
    },
    "line_login": {
      "channel_id": "2007654321",
      "channel_secret_masked": "f6e••••••••••••4c3",
      "status": "valid"
    }
  }
}
```

> **MỚI so với bản trước**: trường `webhook_url` (`ChangeBotController.php:127,139`) — `env('DOMAIN_ENDPOINT_WEBHOOK') . 'line/callback/add/0'`, fallback `url('line/callback/add/0')`. FE lưu vào `self.webhook_url` (`change_new.js:223`) để hiển thị + copy ở bước `webhook`.
> **ĐÃ BỎ so với bản trước**: `validateChannel` **không còn gọi `checkWebhook()`** — việc này chuyển sang **EP-11**.

**Lỗi** — tất cả đều trả **HTTP 200**, phân biệt bằng `success: false`

| HTTP | Message (nguyên văn) | Điều kiện |
|------|----------------------|-----------|
| 200 | `{"success": false, "errors": {...}}` — 「チャネルIDを入力してください」/「チャネルIDは500文字以内で入力してください」/「チャネルシークレットを入力してください」/「チャネルシークレットは500文字以内で入力してください」/「ログインチャネルIDを入力してください」/「ログインチャネルIDは500文字以内で入力してください」/「ログインチャネルシークレットを入力してください」/「ログインチャネルシークレットは500文字以内で入力してください」 | Validation FormRequest thất bại (`BaseRequest.php:16-21`) |
| 200 | 「このLINE公式アカウントは、すでにL Messageに接続されています。 ご不明な場合は、サポート窓口までお問い合わせください 」 (trong `errors.channel_id`) | `channel_id` đã tồn tại ở `bots` với `is_deleted = 0` (`ChangeBotRequest.php:37-41`) |
| 200 | 「入力した情報に誤りがありますので、入力情報を再度ご確認ください。ご不明な場合は、サポート窓口までお問い合わせください。」 | Không lấy được Messaging API access token (`ChangeBotController.php:106`) **hoặc** LINE Login access token (`:118`) |
| 200 | 「認証できませんでした。」 | `getLineInfoBot()` trả rỗng (`:112`) |
| 200 | 「入力した情報が間違っています。再確認してください。」 | Response `/v2/bot/info` thiếu `userId` (`:114`) |

**LINE API bên ngoài**

| Thứ tự | Helper | Endpoint LINE | Mục đích |
|--------|--------|---------------|----------|
| 1 | `lineChanelAccessToken` | `POST /v2/oauth/accessToken` | Xác thực Messaging API channel |
| 2 | `lineFollowers` | `GET /v2/bot/insight/followers` | Đếm bạn bè |
| 3 | `getLineInfoBot` | `GET /v2/bot/info` | Tên OA, `basicId`, avatar |
| 4 | `lineLoginAccessToken` | `POST /v2/oauth/accessToken` (login channel) | Xác thực LINE Login channel |
| 5 | `getLimitMessageLine` | `GET /v2/bot/message/quota` | Suy ra tên gói LOA |

---

### EP-11 — POST `/admin/ajax/change-bot/check-webhook` *(MỚI ở nhánh này)*

- **Controller**: `Ajax\ChangeBotController@checkWebhookEnabled` — `ChangeBotController.php:156`
- **Route**: `routes/web.php:214` (name `changeBot.checkWebhook`)
- **Kích hoạt từ UI**: nút 「接続情報の確認にすすむ」 ở bước `webhook` (`index.blade.php:387`) → `goToConfirm()` (`change_new.js:239-257`); thành công → bước `confirm`
- **Không dùng FormRequest** — kiểm tra `empty()` inline

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|----------|-----------|
| `channel_id` | body | string | Có | `empty()` inline (`ChangeBotController.php:159`) |
| `channel_secret` | body | string | Có | `empty()` inline |
| `bot_id` | body | int | Không | JS gửi, controller không dùng |

**Request mẫu**

```json
{ "bot_id": 1234, "channel_id": "2001234567", "channel_secret": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6" }
```

**Response thành công**

```json
{ "success": true }
```

**Lỗi** (đều HTTP 200)

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 200 | 「入力情報が不足しています。」 | Thiếu `channel_id` hoặc `channel_secret` (`:160`) |
| 200 | 「入力した情報に誤りがありますので、入力情報を再度ご確認ください。」 | Không lấy được access token (`:165`) |
| 200 | 「Webhookをオンにして下さい。 既にオンの場合は、一度オフにしてから再度オンに変更して下さい。」 | `checkWebhook()` trả `false` (`:168-171`) |

**LINE API bên ngoài**

| Helper | Endpoint LINE | Mục đích |
|--------|---------------|----------|
| `lineChanelAccessToken` | `POST /v2/oauth/accessToken` | Lấy token |
| `checkWebhook` | `GET /v2/bot/channel/webhook/endpoint` | Đọc cờ `active` (`app/Helpers/functions.php:4256-4278`) |

---

### EP-05 — POST `/admin/ajax/change-bot/set-webhook`

- **Controller**: `Ajax\ChangeBotController@setWebhook` — `ChangeBotController.php:176`
- **Route**: `routes/web.php:215` (name `changeBot.setWebhook`)
- **Kích hoạt từ UI**: debounce 600ms khi user gõ `channel_id`/`channel_secret` ở bước `input` (`change_new.js:175-194`); chỉ chạy khi `currentStep === 'input'` và cặp `channel_id|channel_secret` thay đổi

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|----------|-----------|
| `channel_id` | body | string | Có | `empty()` inline (`:179`) |
| `channel_secret` | body | string | Có | `empty()` inline |
| `bot_id` | body | int | Không | JS gửi, controller không dùng |

**Request mẫu**

```json
{ "bot_id": 1234, "channel_id": "2001234567", "channel_secret": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6" }
```

**Response thành công**

```json
{ "success": true }
```

**Lỗi** (đều HTTP 200)

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 200 | 「入力情報が不足しています。」 | Thiếu `channel_id` hoặc `channel_secret` (`:180`) |
| 200 | 「入力した情報に誤りがありますので、入力情報を再度ご確認ください。」 | Không lấy được access token (`:185`) |
| 200 | 「Webhookエンドポイントの設定に失敗しました」 | `setWebhookUrl()` trả `false` (`:190`) |

**LINE API bên ngoài**

| Helper | Endpoint LINE | Mục đích |
|--------|---------------|----------|
| `lineChanelAccessToken` | `POST /v2/oauth/accessToken` | Lấy token |
| `setWebhookUrl` | `PUT /v2/bot/channel/webhook/endpoint` | Ghi đè webhook endpoint = `env('DOMAIN_ENDPOINT_WEBHOOK') . 'line/callback/add/0'` (fallback `url('line/callback/add/0')`) — `app/Helpers/functions.php:5820-5843` (chuỗi URL tại `:5824`) |

> ⚠ Endpoint này **thay đổi cấu hình trên LINE Developers của LOA mới** mà không hỏi xác nhận, chỉ cần gõ đủ 2 field. Mức tin cậy: **Cao**.

---

### EP-06 — POST `/admin/ajax/change-bot/execute`

- **Controller**: `Ajax\ChangeBotController@execute` — `ChangeBotController.php:196`
- **Route**: `routes/web.php:216` (name `changeBot.execute`)
- **FormRequest**: `ChangeBotRequest` (cùng rule như EP-04)
- **Kích hoạt từ UI**: nút 「この内容で接続する」 ở bước `confirm` → `executeConnect()` (`change_new.js:283-321`)

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|----------|-----------|
| `bot_id` | body | int | Có (thực tế) | `!= getBotId()` → 404 (`:199`) |
| `channel_id` | body | string | Có | `required\|max:500` + không trùng bot đang hoạt động |
| `channel_secret` | body | string | Có | `required\|max:500` |
| `login_channel_id` | body | string | Có | `required\|max:500` |
| `login_channel_secret` | body | string | Có | `required\|max:500` |
| `type` | body | string | Có (thực tế) | `immediate` \| `scheduled` → `ScheduleChangeBot::TYPE[strtoupper(...)]` (`:203`). **Không có rule `in:`** → giá trị lạ gây `Undefined index` (xem logic-spec) |

**Request mẫu**

```json
{
  "bot_id": 1234,
  "channel_id": "2001234567",
  "channel_secret": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
  "login_channel_id": "2007654321",
  "login_channel_secret": "f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3",
  "type": "scheduled"
}
```

**Response thành công — nhánh `immediate`** (`:280`)

```json
{
  "success": true,
  "data": {
    "processing": true,
    "schedule": { "id": 43, "bot_id": 1234, "type": 1, "status": 1, "progress": 0, "created_at": "2026-08-19 10:35:00" }
  }
}
```

**Response thành công — nhánh `scheduled`** (`:266-279`)

```json
{
  "success": true,
  "data": {
    "reservation": {
      "exists": true,
      "date": "2026年08月19日 10:35",
      "bot_name": "エルメ公式アカウント名",
      "bot_id_line": "@lme_official",
      "plan_name": "コミュニケーションプラン",
      "friend_count": 1240,
      "avatar_url": ""
    },
    "schedule": { "id": 43, "bot_id": 1234, "type": 2, "status": 0, "progress": 0, "created_at": "2026-08-19 10:35:00" }
  }
}
```

> ⚠ Khối `reservation` ở nhánh `scheduled` là **chuỗi mẫu hardcode** (`:271-275`), không phản ánh LOA thật. Front-end **không đọc** khối này — nó tự dựng `reservation` từ `confirmData` và chỉ lấy `data.schedule.id` / `data.schedule.created_at` (`change_new.js:308-318`). Đây là **rác code sót lại**, không ảnh hưởng hành vi thực tế.

**Lỗi**

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 404 | `Bot not found` | `bot_id` gửi lên khác `getBotId()` (`:199`) hoặc bot không tồn tại / `is_deleted = 1` (`:201`) |
| 200 | `{"success": false, "errors": {...}}` — 「チャネルIDを入力してください」 v.v. | Validation FormRequest thất bại |
| 200 | 「このLINE公式アカウントは、すでにL Messageに接続されています。 ご不明な場合は、サポート窓口までお問い合わせください 」 | `channel_id` trùng bot đang hoạt động (`ChangeBotRequest.php:37-41`) |
| 200 | `{"success": false, "msg": "現在のプランは利用できない機能です。アップグレードが必要になります。"}` | **[#39230 — MỚI]** `botCanChangeBot($bot, $type)` = false: bot `plan_type = 2` (free) và (`type = scheduled` **hoặc** đã quá 1 tháng kể từ `bots.created_at`) — `:208-218` |
| 200 | `{"success": false, "msg": "LOA変更処理中のため、変更できません。処理完了後に再度お試しください。"}` | (a) Bot đã có bản ghi `DRAFT/WAITING/PROCESSING` — pre-check `:221-231`; hoặc (b) **[#39230 — MỚI]** `PlanLimitGuard::rollbackIfOverLimit()` đếm lại sau INSERT thấy vượt hạn mức 1 → **xoá bản vừa tạo** rồi trả lỗi (`:248-264`) |

> Front-end đọc đúng key `r.msg` (`change_new.js:299-302`) → các thông báo trên **hiển thị được**. (Bản v1 FE đọc `r.message` nên nuốt lỗi — đã sửa.)

**LINE API bên ngoài**: không gọi (chỉ ghi DB).

---

### EP-07 — GET `/admin/ajax/change-bot/progress`

- **Controller**: `Ajax\ChangeBotController@progress` — `ChangeBotController.php:283`
- **Route**: `routes/web.php:217` (name `changeBot.progress`)
- **Kích hoạt**: `setInterval` 3000ms (`change_new.js:327-351`)

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|----------|-----------|
| `schedule_id` | query | int | Có (thực tế) | Không có rule; kết hợp `where('bot_id', getBotId())` nên chống IDOR |

**Request mẫu**

```
GET /admin/ajax/change-bot/progress?schedule_id=43
```

**Response thành công**

```json
{ "success": true, "data": { "progress": 60, "completed": false, "confirm_data": null } }
```

**Lỗi**

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 404 | `Schedule not found` | Không tìm thấy schedule thuộc bot hiện tại (`:287`) |
| 200 | `{"success": false, "message": "ERROR", "message_error": "<nội dung lỗi từ DB>"}` | `status ∈ {ERROR(4), CANCEL(5)}` (`:288`). FE hiển thị toast bằng `message_error` (`change_new.js:340`) |

**LINE API bên ngoài**: không gọi.

---

### EP-08 — POST `/admin/ajax/change-bot/delete-reservation`

- **Controller**: `Ajax\ChangeBotController@deleteReservation` — `ChangeBotController.php:294` (comment `/** TODO: replace with real DB deletion */` tại `:293`)
- **Route**: `routes/web.php:218` (name `changeBot.delete.reservation`)

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|----------|-----------|
| `schedule_id` | body | int | Có (thực tế) | Không có rule; scope theo `bot_id` session |
| `bot_id` | body | int | Không | JS gửi, controller không dùng |

**Request mẫu**

```json
{ "bot_id": 1234, "schedule_id": 43 }
```

**Response thành công**

```json
{ "success": true, "message": "接続予約を削除しました" }
```

**Lỗi**

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 404 | `Schedule not found` | Không tìm thấy schedule của bot hiện tại (`:298`) |

> ⚠ **Không kiểm tra trạng thái nguồn** — có thể chuyển bản ghi đang `PROCESSING` (worker đang chạy) hoặc đã `DONE` về `CANCEL`.

**LINE API bên ngoài**: không gọi.

---

### EP-09 — POST `/admin/ajax/change-bot/execute-reservation`

- **Controller**: `Ajax\ChangeBotController@executeReservation` — `ChangeBotController.php:306` (comment `/** TODO: replace with real execution logic */` tại `:305`)
- **Route**: `routes/web.php:219` (name `changeBot.execute.reservation`)

**Request params**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|----------|-----------|
| `schedule_id` | body | int | Có (thực tế) | Không có rule; scope theo `bot_id` session |
| `bot_id` | body | int | Không | JS gửi, controller không dùng |

**Request mẫu**

```json
{ "bot_id": 1234, "schedule_id": 43 }
```

**Response thành công**

```json
{ "success": true, "data": { "processing": true } }
```

**Lỗi** (đều HTTP 200, FE đọc `r.message` — `change_new.js:390`)

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 200 | 「現在のプランは利用できない機能です。アップグレードが必要になります。」 | **[#39230 — MỚI]** bot không tồn tại **hoặc** `botCanChangeBot($bot)` = false (gọi **không truyền `$type`** ⇒ mọi bot `plan_type = 2` đều bị chặn) — `:310-317` |
| 200 | 「LOA変更処理中のため、変更できません。処理完了後に再度お試しください。」 | Bot đã có bản ghi `WAITING/PROCESSING` (`:318-319`) |
| 404 | `Schedule not found` | Không tìm thấy schedule (`:321-322`) |
| 200 | 「このLINE公式アカウントは、すでにL Messageに接続されています。ご不明な場合は、サポート窓口までお問い合わせください。」 | `channel_id_new` trùng `bots.channel_id` với `is_deleted = 0` (`:325-328`) |
| 200 | 「LOA変更処理中のため、変更できません。処理完了後に再度お試しください。」 | `channel_id_new` + `channel_secret_new` trùng target của schedule khác đang `WAITING/PROCESSING` (`:330-337`) |

**LINE API bên ngoài**: không gọi.

---

### EP-10 — POST `/admin/step2-check-friend` *(nhánh đổi LOA hiện mồ côi)*

- **Controller**: `Admin\BotController@step2CheckFriend` — `BotController.php:4738`
- **Route**: `routes/web.php:1885` (name `step2CheckFriend`)
- **Kích hoạt**: polling từ `public/js/admin/add_bot/add_bot.js:329` (view `bot_add_v3`), `add_bot_v5.js:1114` (view `bot_add_v5`), `step5qr.js:52`
- **Vai trò trong FA-044**: nhánh `botIdChange` + `type_change` tạo bản ghi `schedule_change_bots` (`BotController.php:4790-4820`). **Hiện không có đường vào UI** cho nhánh này — xem ghi chú ở mục 2.

**Request params (phần liên quan FA-044)**

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|-----|--------|------|----------|---------|
| `bot_id` | body (multipart) | int | Có | ID **bot MỚI** vừa được tạo |
| `botIdChange` | body | int | Có (khi đổi LOA) | ID **bot CŨ** đang được thay thế |
| `landing_id` | body | int | Có | Landing dùng để kiểm tra kết bạn thử |
| `bot_slot_id` | body | int | Không | |
| `type` | body | string | Không | |
| `type_change` | body | string | Có (khi đổi LOA) | `immediate` \| `scheduled`, đọc từ query string trang hiện tại (`add_bot.js:325-327`) |

**Response thành công (nhánh đổi LOA)** (`BotController.php:4822-4829`)

```json
{ "success": true, "msg": "", "changeBot": true, "botIdChange": 5678, "bot_id_new": 1234 }
```

FE nhận `changeBot: true` + có `type_change` → redirect `/admin/change-bots-new/{hash}?type=change_sub&change_success=1` (immediate) hoặc `/admin/change-bots-new/{hash}` (scheduled) — `add_bot.js:352-356`.

**Lỗi (phần liên quan FA-044)**

| HTTP | Message | Điều kiện |
|------|---------|-----------|
| 200 | `{"success": false, "msg": "LOA変更処理中のため、変更できません。処理完了後に再度お試しください。"}` | Bot cũ đã có schedule `DRAFT/WAITING/PROCESSING` (`BotController.php:4817-4818`) |

> ⚠ Nhánh này **KHÔNG có** guard gói cước `#39230` và **KHÔNG dùng** `PlanLimitGuard` (khác EP-06). Grep `PlanLimitGuard` trong `BotController.php` → 0 kết quả.

**LINE API bên ngoài**: gửi tin nhắn 「新規接続が完了しました！エルメの管理画面に戻って、次へ進んでください」 tới người dùng test qua `MessageService::createMessageV2` (`BotController.php:4775`).

---

## 4. Bảng middleware áp dụng

| Middleware | Class | Áp dụng cho | Ý nghĩa |
|-----------|-------|-------------|---------|
| `NotifyChatworkRequestTimeSlow` | `App\Http\Middleware\NotifyChatworkRequestTimeSlow` | EP-01…EP-11 | Cảnh báo Chatwork khi request chậm (`routes/web.php:81`) |
| `admin_access` | `App\Http\Middleware\AdminAccess` (`app/Http/Kernel.php:69`) | EP-01…EP-09, EP-11 | Yêu cầu `Auth::check()` và `users.role ∈ {0, 1, 2, -1}` (`AdminAccess.php:23`); ghi log `user_access_bots` cho staff; kiểm tra cờ `ENABLE_BOT` cho một số route |
| `https_protocol` | `App\Http\Middleware\HttpsProtocol` (`Kernel.php:75`) | EP-01…EP-09, EP-11 | **No-op** — thân hàm redirect HTTPS bị comment (`HttpsProtocol.php:18-20`) |
| `check_remember_token` | `App\Http\Middleware\CheckRememberToken` (`Kernel.php:83`) | EP-01…EP-11 | So khớp `session('remember_token')` với `users.remember_token_reset_pass` |
| `LogRequestMultipart` | `App\Http\Middleware\LogRequestMultipart` | EP-10 | Ghi log request multipart (`routes/web.php:835`) |
| `check_login` | `App\Http\Middleware\CheckLogin` | EP-10 | Xác thực phiên đăng nhập (`routes/web.php:1877`) |
| `web` (nhóm mặc định) | Kernel group `web` | mọi POST | Session + **CSRF token** — FE gửi header `X-CSRF-TOKEN` |

---

## 5. Liên kết endpoint ↔ màn hình UI

> ID `SCR-CHB-XX` dưới đây **đã đồng bộ với `ui/ui-spec.md` v2** (bộ mã mới: màn hình Webhook được chèn làm `SCR-CHB-04`, các mã từ `confirm` trở đi dịch +1 so với bản v1). Mức tin cậy về ID: **Cao**; về mapping bước ↔ endpoint: **Cao**.

| Màn hình | Bước SPA (`currentStep`) | Blade dòng | Endpoint liên quan |
|----------|--------------------------|-----------|--------------------|
| SCR-CHB-01 — Trang chiến dịch (Campaign Landing) | `campaign` | `index.blade.php:24` | EP-01, EP-03 |
| SCR-CHB-02 — Chọn phương thức (ngay / đặt lịch) | `select` | `:93` | EP-01, EP-03 |
| SCR-CHB-03 — Nhập credential LOA mới | `input` | `:209` | EP-04, EP-05 |
| **SCR-CHB-04** *(mới)* — Cấu hình Webhook URL | `webhook` | `:289` | EP-11 (nút 「接続情報の確認にすすむ」); dữ liệu `webhook_url` đến từ EP-04 |
| SCR-CHB-05 — Xác nhận thông tin LOA mới | `confirm` | `:403` | EP-06 |
| SCR-CHB-06 — Màn hình tiến độ xử lý | `processing` | `:477` | EP-07 |
| SCR-CHB-07 — Màn hình đặt lịch đã tạo | `reservation` | `:505` | EP-03, EP-08, EP-09 |
| SCR-CHB-08 — Modal hoàn tất | `showSuccessModal` | `:549` | (đóng modal → `/basic/overview`) |
| SCR-CHB-09 — Modal xác nhận xoá đặt lịch | `showDeleteModal` | `:579` | EP-08 |
| SCR-CHB-10 — Modal xác nhận thực thi ngay | `showExecuteModal` | `:615` | EP-09 |
| SCR-CHB-11 — Modal quảng bá chiến dịch (toàn hệ thống) | `#modalCampaignChangebot` trong header | mọi trang Admin/Basic | — (không gọi endpoint; hiện bị vô hiệu hoá bằng `return;`) |
| SCR-CHB-12 — Màn hình chặn theo gói | trang riêng | `resources/views/admin/bots/change_bot_plan_blocked.blade.php` | EP-02 |

> Wizard `bot_add_v3` (`resources/views/admin/bots/bot_add_v3.blade.php`, dùng EP-02 + EP-10) **không còn thuộc phạm vi FA-044** — ui-spec v2 đã gỡ khỏi danh sách màn hình vì không còn link nào trỏ tới. Xem mục nợ kỹ thuật TD-B20 trong `web/logic-spec.md`.

**Luồng chuyển bước trong SPA** (`change_new.js`):

```
select ──goToInput():157──► input ──validateAndConfirm():196 (EP-04)──► webhook
                                                                          │
                                                            goToConfirm():239 (EP-11)
                                                                          ▼
                                       processing ◄──executeConnect():283 (EP-06)── confirm
                                            │  type=immediate                          │
                                            │                                          │ type=scheduled
                                            │ pollProgress():327 (EP-07)                ▼
                                            └──────────────────────────────────► reservation
                                                                          (EP-08 xoá / EP-09 chạy ngay)
```

---

## 6. Bản cũ — ngoài phạm vi

Các route dưới đây cũng mang tên "change bot" nhưng thuộc thế hệ code cũ. Cách xác định: view/JS của thế hệ hiện hành (`change_bot_new/index.blade.php` + `change_new.js`) **không gọi tới chúng**.

| Method | URL thật | Controller@Method | Vị trí | View / JS gọi tới | Lý do ngoài phạm vi |
|--------|----------|-------------------|--------|-------------------|---------------------|
| GET | `/admin/change-new-bot` | `Admin\BotController@changeNewBot` | `BotController.php:729`; route `routes/web.php:389` | `resources/views/admin/bots/change_new_bot.blade.php` | View riêng, không liên quan `change_bot_new/`. Route nằm trong nhóm `supper_admin` (`routes/web.php:248`) |
| POST | `/admin/save-change-bot` | `Admin\BotController@saveChangeBot` | `BotController.php:1565`; route `routes/web.php:391` | form của `change_new_bot.blade.php` | Luồng lưu kiểu form-post cũ (validate `bot_name`, `url`, `channel_access_token`…), **không** đụng `schedule_change_bots` |
| GET | `/admin/change-bot-new` | `Admin\ChangeBotController@index` | `app/Http/Controllers/Admin/ChangeBotController.php:35` → view `admin.bots.change_bots` (`:39`) | `resources/views/admin/bots/change_bots.blade.php` | View thế hệ trung gian |
| POST | `/admin/change-bot-new` | `Admin\ChangeBotController@store` | `Admin/ChangeBotController.php:48` | như trên | như trên |
| POST | `/ajax/admin/validate-change-new-bot` | `Admin\BotController@validateChangeNewBot` | `BotController.php:7318`; route `routes/web.php:3398` | **chỉ** `public/js/admin/change_bots_new.js:31` → nạp bởi `change_new_bots.blade.php:149` | View `change_new_bots` không còn được controller nào render (dòng render đã bị comment tại `BotController.php:7272`) |
| POST | `/ajax/admin/step1-change-new-bot` | `Admin\BotController@changeNewBotStep1` | `BotController.php:7496`; route `routes/web.php:3399` | `change_bots_new.js:104`; `add_bot.js:457` (**nhánh `else`, chỉ khi KHÔNG có `type_change`**); `add_bot_v5.js:1406`; `step5qr.js:116` | Vẫn sống cho luồng **thêm bot**, không thuộc luồng đổi LOA hiện hành |
| POST | `/ajax/admin/cancel-change-new-bot` | `Admin\BotController@cancelChangeBot` | `BotController.php:8196`; route `routes/web.php:3400` | **chỉ** `change_bots_new.js:67` | JS hiện hành không gọi |

> Ba route `/ajax/admin/*-change-new-bot` nằm trong nhóm `Route::group(['prefix' => 'ajax', 'middleware' => ['check_login', 'check_remember_token']])` — `routes/web.php:2485`, nên URL đầy đủ là `/ajax/admin/...` (**không phải** `/admin/ajax/...`). Xác nhận chéo: `change_bots_new.js:31,67,104`.

---

## 7. Thay đổi so với bản spec trước

So sánh `release_step_20260623` → `release_step_20260805` (`git diff --stat`: `ChangeBotController.php` +94, `BotController.php` +1627, `routes/web.php` +51, `change_new.js` +69, `change_bot_new/index.blade.php` +251, file mới `PlanLimitGuard.php` 236 dòng, file mới `bot_add_v5.blade.php` 2481 dòng).

| Loại | Endpoint / hành vi | Chi tiết thay đổi |
|------|--------------------|-------------------|
| **THÊM** | **EP-11** `POST /admin/ajax/change-bot/check-webhook` | Route mới `routes/web.php:214`; controller mới `ChangeBotController@checkWebhookEnabled` (`:156-174`) |
| **SỬA** | EP-04 `/validate` | (a) **Bỏ** bước `checkWebhook()` khỏi thân method — chuyển sang EP-11; message 「Webhookをオンにして下さい。…」 **không còn** phát ra từ EP-04. (b) **Thêm** trường `webhook_url` vào response (`:127,139`) |
| **SỬA** | EP-06 `/execute` | (a) **Thêm** guard gói cước `#39230` qua `botCanChangeBot()` → lỗi mới 「現在のプランは利用できない機能です。アップグレードが必要になります。」 (`:208-218`). (b) **Thêm** `PlanLimitGuard::rollbackIfOverLimit()` sau INSERT → có thể xoá lại bản ghi vừa tạo và trả 「LOA変更処理中のため…」 (`:248-264`) |
| **SỬA** | EP-09 `/execute-reservation` | **Thêm** guard gói cước `#39230` (gọi `botCanChangeBot($bot)` **không truyền `$type`** ⇒ chặn toàn bộ bot free) — `:309-317` |
| **ĐỔI HÀNH VI UI** | EP-02, EP-10 | `goToInput()` (`change_new.js:157-161`) **không còn redirect** sang `/admin/change-bot-sub/...`. Hệ quả: EP-02 và nhánh đổi-LOA của EP-10 **mất đường vào từ UI**; EP-04/EP-05/EP-06 **trở lại là code SỐNG** |
| **ĐỔI HÀNH VI UI** | EP-06 | FE nay đọc `r.msg` khi `success = false` (`change_new.js:299-302`) → thông báo lỗi hiển thị được (trước đây bị nuốt) |
| **THÊM (UI)** | bước `webhook` | Blade thêm block `currentStep === 'webhook'` (`index.blade.php:289`) + `copyWebhookUrl()` / `fallbackCopy()` / `backToInput()` trong JS |
| **KHÔNG ĐỔI** | EP-01, EP-03, EP-05, EP-07, EP-08, EP-10 | Hợp đồng HTTP giữ nguyên |

> **Giữ nguyên đánh số ID**: EP-01…EP-10 giữ đúng ý nghĩa như bản v1 để không phá cross-reference; endpoint mới nhận ID **EP-11** thay vì chen vào giữa.

### Kết luận của bản v1 bị BÁC BỎ

| Kết luận trong spec v1 | Thực tế trên `release_step_20260805` |
|---|---|
| "Tính năng chưa hoàn thiện / backend dummy" | **Sai.** Tính năng đã hoàn thiện, đang chạy production; worker `ChangeBotTask` có thật ở `src/job/linect-service` |
| "EP-04, EP-05, EP-06 là code chết trên UI" | **Sai.** Cả ba đều được `change_new.js` gọi trong luồng chính |
| "Bản ghi `schedule_change_bots` thực tế do `BotController@step2CheckFriend` tạo" | **Sai** cho màn hình `change_bot_new`. Nay do **EP-06** tạo; nhánh `step2CheckFriend` mới là phần mồ côi |
| "Worker xử lý `schedule_change_bots` không tồn tại trong repository đã clone" | **Sai** trên nhánh job mới — `src/job/linect-service/src/main/java/sns/line/task/ChangeBotTask.java` + `threads/changebot/ChangeBotJob.java` |
| "EP-06 trả lỗi ở key `msg` nên user không thấy thông báo" | **Đã được vá ở FE** — `change_new.js:299-302` đọc `r.msg` |
