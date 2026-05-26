# API Spec — 「LOA接続設定」(Cài đặt kết nối LOA)

**Feature ID**: bot-edit
**Ngày phân tích**: 2026-03-30
**Nguồn**: Laravel source code — `app/Http/Controllers/Admin/BotController.php`, `app/Http/Controllers/Admin/UserController.php`
**Confidence**: Cao (phân tích trực tiếp từ source code)

---

## 1. Tổng quan endpoints

| EP | Method | URL | Controller@Action | Middleware | Mô tả |
|----|--------|-----|-------------------|------------|-------|
| EP-01 | GET | `/admin/bot-edit` | `BotController@botAdd` | web, NotifyChatworkRequestTimeSlow | Hiển thị trang cài đặt kết nối LOA |
| EP-02 | POST | `/admin/bot-save` | `BotController@botChange` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lưu thay đổi cài đặt LOA |
| EP-03 | POST | `/admin/bot/check-mode` | `UserController@adminCheckMode` | web, NotifyChatworkRequestTimeSlow | Kiểm tra kết nối LOA (接続チェック) |
| EP-04 | POST | `/ajax/add-flag-get-old-friend` | `BotController@addFlagGetOldFriend` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy thông tin bạn bè hiện có (既存友だち情報取得) |
| EP-05 | POST | `/ajax/reGetAvatarBot` | `BotController@reGetAvatarBot` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Đồng bộ ảnh/tên từ LINE Manager (情報更新) |
| EP-06 | POST | `/ajax/bot/re-create-liffapp` | `BotController@reCreateLiffApp` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Kết nối lại LIFF App (SCR-BE-04 dialog「はい」) |
| EP-07 | POST | `/ajax/check-enable-use-webhook-modal` | `BotController@checkEnableWebhookModal` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Kiểm tra LIFF/Webhook (チェックする) |
| EP-08 | GET | `/admin/change-bots-new/{id}` | `BotController@adminChangeNewBot` | web, NotifyChatworkRequestTimeSlow | Trang thay thế LOA (LOA入れ替え) |
| EP-09 | GET | `/admin/home` | `UserController@index` | web, NotifyChatworkRequestTimeSlow | Trang danh sách tài khoản (アカウント一覧) |
| EP-10 | POST | `/admin/check-auth-bot` | `BotController@checkAuthBot` | web, NotifyChatworkRequestTimeSlow | Kiểm tra bot có campaign (dùng internal, không trực tiếp từ bot-edit) |
| EP-11 | POST | `/ajax/set-time-check-webhook` | `BotController@setTimeCheckWebHook` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Cập nhật thời gian kiểm tra webhook |
| EP-12 | POST | `/admin/bot/set-domain` | `UserController@adminSetDomain` | web, NotifyChatworkRequestTimeSlow | Cập nhật webhook URL trên LINE Platform |
| EP-13 | POST | `/ajax/check-transfer-code` | `BotController@checkTransferCode` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Kiểm tra mã transfer code (データコピー) |

---

## 2. Chi tiết từng endpoint

### EP-01: GET `/admin/bot-edit` — Hiển thị trang cài đặt kết nối LOA

**Route name**: `botEdit`
**Controller**: `Admin\BotController@botAdd` — `BotController.php:278`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `id` | query | string (Hashids encoded) | Có (khi edit) | Hashids::decode | Bot ID đã mã hóa. Null = trang thêm mới bot |
| `msg` | query | string | Không | — | Flag hiển thị thông báo |
| `upgrade_bot_id` | query | string (Hashids encoded) | Không | Hashids::decode | Bot ID để upgrade |
| `bot_slot_id` | query | int | Không | — | Slot ID cho bot mới |

#### Response (HTML View)

Trả về view `admin.bots.bot_add` với data:
- `managers`: Danh sách users (staff) thuộc admin, dùng để chọn quản lý bot
- `bots`: Object Bots model — chứa toàn bộ thông tin bot
- `baseUrl`: Base URL của request
- `flagChangeFreePlan`: 0 hoặc 1 — flag cho user đăng ký sau 2021-07-01
- `botFreeNumber`: Số bot free hiện có
- `ipServer`: IP server hiện tại
- `flag_bot_line_id`: Flag thông báo
- `roleId`: Level (quyền) của user hiện tại
- `basicFee`: Phí cơ bản từ admin chính (user ID = 1)
- `botSlotId`: Bot slot ID (nếu có)
- `upgradeBotId`: Bot ID để upgrade (nếu có)

#### Logic xử lý
1. Lấy `adminId` từ `getCurrentUser()`
2. Decode `id` bằng Hashids
3. Nếu `id` không null → tìm bot, lấy danh sách managers kèm thông tin quyền trên bot (qua `user_bot`)
4. Nếu `id` null → trang thêm mới, lấy managers không có bot
5. Kiểm tra và sinh `liff_callback_unique` (10 ký tự random) nếu chưa có → lưu vào DB
6. Tính `flagChangeFreePlan` dựa trên ngày đăng ký user (trước/sau 2021-07-01)
7. Tính IP server từ `BASE_URL` env
8. Kiểm tra quyền `bot_slot_id` — phải thuộc admin hiện tại

#### Lỗi có thể xảy ra

| HTTP | Mô tả | Điều kiện |
|------|-------|-----------|
| 302 | Redirect 404 | Bot không tồn tại hoặc exception |
| 302 | Redirect 404 | `bot_slot_id` không thuộc admin hiện tại |

---

### EP-02: POST `/admin/bot-save` — Lưu thay đổi cài đặt LOA

**Route name**: `botSave`
**Controller**: `Admin\BotController@botChange` — `BotController.php:566`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `id` | body | string (Hashids encoded) | Có (khi edit) | Hashids::decode | Bot ID. Null = tạo mới |
| `bot_name` | body | string | Có | `required\|max:100` | Tên hiển thị LOA (アカウント名) |
| `channel_secret` | body | string | Không | — | Messaging API Channel Secret |
| `channel_access_token` | body | string | Không | — | Channel Access Token (auto-generated nếu thay đổi) |
| `channel_id_line_login` | body | string | Không | — | LINE Login Channel ID (チャネル ID) |
| `channel_secret_line_login` | body | string | Không | — | LINE Login Channel Secret (チャネルシークレット) |
| `url` | body | string | Có (khi tạo mới) | `required\|url\|max:200\|url_exists:bots` | URL thêm bạn (khi tạo mới) |
| `image` | body (multipart) | file | Không | — | File ảnh đại diện upload |
| `url_image` | body | string | Không | — | URL ảnh hiện tại hoặc `/images/camera.png` (khi xóa ảnh) |
| `link_of_image` | body | string | Không | — | URL ảnh bên ngoài cần clone |
| `phone` | body | string | Không | — | Số điện thoại (không bắt buộc trên giao diện bot-edit) |
| `ids` | body | JSON array | Không | — | Danh sách user IDs được gán quyền quản lý bot |
| `domain_url_shorten` | body | string | Không | `nullable\|url\|max:100\|check_point` | Domain rút gọn URL tùy chỉnh |

#### Request mẫu (khi edit)

```json
{
  "id": "hashid_encoded_string",
  "bot_name": "Xuka_BOT_Booking",
  "channel_secret": "058a91a81994ce8e6b1b241fb7540e77",
  "channel_id_line_login": "2006160353",
  "channel_secret_line_login": "fe96384af7daddc93c3378dad8f7b0bb",
  "ids": "[1, 2, 3]",
  "url_image": "https://example.com/avatar.jpg"
}
```

#### Response thành công

```json
{
  "success": true
}
```

#### Logic xử lý (khi edit — `id` có giá trị)

1. **Validation**: `bot_name` required, max 100 ký tự
2. **Channel Secret thay đổi**: Gọi LINE API `POST https://api.line.me/v2/oauth/accessToken` để lấy access token mới
   - Input: `client_id` (channel_id hiện tại), `client_secret` (channel_secret mới)
   - Nếu thành công → lưu `channel_access_token` mới, set `expired_date_channel_access_token` = now + 28 ngày
   - Nếu thất bại → trả lỗi `'入力した情報が間違っています。...'`
3. **LINE Login thay đổi** (channel_id_line_login hoặc channel_secret_line_login thay đổi):
   - Gọi LINE API `POST https://api.line.me/v2/oauth/accessToken` với LINE Login credentials
   - Nếu thành công → tạo 2 LIFF Apps mới:
     - **LIFF App 1** (流入アクション用): `POST https://api.line.me/liff/v1/apps` — `view.type = 'full'`, URL = `/liff-callback/{unique}`
     - **LIFF App 2** (各種フォーム用): `POST https://api.line.me/liff/v1/apps` — `botPrompt = 'aggressive'`, URL = env(`URL_OUTSIDE_STEP`) + `/liff-callback/{unique}`
   - Cập nhật DB: `liff_app_id`, `liff_app_id_booking`, `liff_callback_unique`, `channel_id_line_login`, `channel_secret_line_login`, `url_liff_app_callback`
   - Lưu `liff_app_id_old` nếu chưa có (backup lần đầu)
4. **Xử lý ảnh**: Upload file → resize max 2048px → lưu vào `media/images/{adminId}/{botId}/bot/`
5. **Cập nhật bảng `bots`**: `view_name`, `channel_secret`, `channel_access_token`, `bot_image`, `domain_url_shorten`, `bot_error_message` (xóa)
6. **Cập nhật `user_bot`**: Soft-delete tất cả → upsert lại theo `ids`
7. **Cập nhật `bots_profiles`**: `avt_path`, `nick_name` cho profile mặc định (`is_default = 1`)
8. **Reset callback events**: `status = 10 → status = 0`

#### Lỗi có thể xảy ra

| HTTP | Code | Mô tả | Điều kiện |
|------|------|-------|-----------|
| 200 | `success: false` | `'契約以上に追加できません。'` | Tạo mới nhưng vượt quá max_bot |
| 200 | `success: false, errors` | Validation errors | bot_name rỗng, URL sai format |
| 200 | `success: false, msg` | `'入力した情報が間違っています。WEBブラウザの自動翻訳機能が原因の可能性がございますので、自動翻訳を無効にした状態でお試しください。'` | Channel Secret sai, không lấy được access token từ LINE API |
| 200 | `success: false, msg` | `'LINEログイン設定情報に誤りがあります。再確認してください。'` | LINE Login credentials sai hoặc tạo LIFF App thất bại |
| 200 | `success: false, message` | `'cannot clone this image'` | Không clone được ảnh từ URL |

---

### EP-03: POST `/admin/bot/check-mode` — Kiểm tra kết nối LOA (接続チェック)

**Route name**: `adminCheckMode`
**Controller**: `Admin\UserController@adminCheckMode` — `UserController.php:380`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `bot_id` | body | int | Có | — | Bot ID (plain, không encode) |

#### Response thành công

```json
{
  "success": true,
  "msg": "正常に接続しています。",
  "bot": { /* Bots model object */ }
}
```

#### Logic xử lý

1. Lấy bot từ DB: `Bots::where('id', botId)->where('is_deleted', '<>', 1)`
2. **Kiểm tra LINE Bot Info** — `GET https://api.line.me/v2/bot/info` với `channel_access_token`
   - Nếu lỗi (401 hoặc exception) → cập nhật `is_connected = 0` → trả `'認証できませんでした。'`
3. **Kiểm tra Webhook** — `GET https://api.line.me/v2/bot/channel/webhook/endpoint` với `channel_access_token`
   - Lấy `endpoint` từ response
   - So sánh với expected webhook URL: `env('DOMAIN_ENDPOINT_WEBHOOK') + 'line/callback/add/' + botId`
   - Nếu endpoint khác → `is_connected = 2` → trả `'webhookの設定が間違っています'`
   - Nếu `active == false` → `is_connected = 3` → trả `'一度オフしてからオンにして下さい'`
4. **Thành công** → `is_connected = 1`, `last_time_connection_check = now()` → trả `'正常に接続しています。'`

#### Lỗi có thể xảy ra

| HTTP | Code | Mô tả | Điều kiện |
|------|------|-------|-----------|
| 200 | `success: false` | `'認証できませんでした。'` | Channel access token hết hạn hoặc sai |
| 200 | `success: false, status_link: false` | `'webhookの設定が間違っています'` | Webhook URL trên LINE khác với URL của hệ thống |
| 200 | `success: false, status_link: false` | `'一度オフしてからオンにして下さい'` | Webhook đang tắt (active = false) |

#### Side effects
- Cập nhật `bots.is_connected` (0 = lỗi auth, 1 = OK, 2 = webhook URL sai, 3 = webhook off)
- Cập nhật `bots.last_time_connection_check`

---

### EP-04: POST `/ajax/add-flag-get-old-friend` — Lấy thông tin bạn bè hiện có (既存友だち情報取得)

**Route name**: `add.flag.get.old.friend`
**Controller**: `Admin\BotController@addFlagGetOldFriend` — `BotController.php:5962`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `bot_id` | body | string (Hashids encoded) | Có | Hashids::decode | Bot ID đã mã hóa |

#### Response thành công

```json
{
  "success": true,
  "message": "既存友だち情報の取得には最大5時間程度かかる場合があります。ページを閉じてください。"
}
```

#### Logic xử lý

1. Decode `bot_id` bằng Hashids → tìm bot trong DB
2. Gọi LINE API: `GET https://api.line.me/v2/bot/followers/ids` với `channel_access_token`
3. Nếu thất bại (exception chứa `'Access to this API is not available for your account'`):
   - Cập nhật `is_get_old_friend = config('sns-line.status_is_get_old_friend.fail')`
   - Trả lỗi `'認証アカウントしか取得できません。'`
4. Nếu thành công:
   - Kiểm tra `is_get_old_friend`:
     - Nếu = 3 hoặc = fail → cập nhật thành 1 (đang xử lý)
     - Nếu khác → log `'get old friend proccessing'` (đã đang xử lý, không đặt lại)
   - Trả message thành công: `'既存友だち情報の取得には最大5時間程度かかる場合があります。ページを閉じてください。'`

**Lưu ý**: Đây là thao tác **bất đồng bộ**. Frontend chỉ nhận response khởi tạo, việc lấy danh sách bạn bè thực tế do **background job** (Spring Boot) xử lý sau đó (polling `is_get_old_friend` flag).

#### Lỗi có thể xảy ra

| HTTP | Code | Mô tả | Điều kiện |
|------|------|-------|-----------|
| 400 | `success: false` | `'Bot does not exist'` | Bot không tồn tại |
| 200 | `success: false` | `'認証アカウントしか取得できません。'` | Tài khoản chưa xác thực (unverified LINE account) — API trả 403 |

---

### EP-05: POST `/ajax/reGetAvatarBot` — Đồng bộ ảnh/tên từ LINE Manager (情報更新)

**Route name**: `reGetAvatarBot`
**Controller**: `Admin\BotController@reGetAvatarBot` — `BotController.php:11149`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `bot_id` | body | int | Có | — | Bot ID (plain, không encode) |

#### Response thành công

```json
{
  "success": true,
  "img": "https://profile.line-scdn.net/xxx/xxx",
  "nick_name": "Xuka_BOT_Booking"
}
```

#### Logic xử lý

1. Tìm bot theo `bot_id`
2. Gọi LINE API: `GET https://api.line.me/v2/bot/info` với `channel_access_token`
3. Nếu HTTP 200:
   - Lấy `pictureUrl` → `avturl`
   - Lấy `displayName` → `nick_name`
4. Nếu không 200: giữ nguyên giá trị cũ từ DB
5. Cập nhật bảng `bots`: `bot_image`, `view_name`
6. Cập nhật bảng `bots_profiles` (where `is_default = true`): `avt_path`, `nick_name`
7. Trả về `img` và `nick_name` cho frontend cập nhật giao diện

#### Lỗi có thể xảy ra

| HTTP | Code | Mô tả | Điều kiện |
|------|------|-------|-----------|
| 200 | `success: false` | `'認証できませんでした。'` | Channel access token hết hạn hoặc sai |

---

### EP-06: POST `/ajax/bot/re-create-liffapp` — Kết nối lại LIFF App

**Route name**: `check.liff.re.create`
**Controller**: `Admin\BotController@reCreateLiffApp` — `BotController.php:11196`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `bot_id` | body | string (Hashids encoded) | Có | Hashids::decode | Bot ID đã mã hóa |
| `channel_id_line_login` | body | string | Có | — | LINE Login Channel ID |
| `channel_secret_line_login` | body | string | Có | — | LINE Login Channel Secret |
| `liffAppError` | body | int (0 hoặc 1) | Có | — | 1 = LIFF App chính bị lỗi, cần tạo lại |
| `liffAppErrorBooking` | body | int (0 hoặc 1) | Có | — | 1 = LIFF App booking bị lỗi, cần tạo lại |

#### Response thành công

```json
{
  "success": true,
  "bot": { /* Bots model object sau khi update */ }
}
```

#### Logic xử lý

1. Decode `bot_id` bằng Hashids → tìm bot
2. **Lấy LINE Login token**: `POST https://api.line.me/v2/oauth/accessToken` với `channel_id_line_login`, `channel_secret_line_login`
3. Nếu `liffAppError == 1`: **Tạo LIFF App chính** (流入アクション用)
   - `POST https://api.line.me/liff/v1/apps`
   - `view.type = 'full'`, URL = `/liff-callback/{liff_callback_unique}`
   - `description = 'エルメ流入アクション用LIFF'`
   - Cập nhật `bots`: `liff_app_id`, `liff_callback_unique`, `channel_id_line_login`, `channel_secret_line_login`
   - Lưu `liff_app_id_old` nếu chưa có (backup)
4. Nếu `liffAppErrorBooking == 1`: **Tạo LIFF App booking** (各種フォーム用)
   - `POST https://api.line.me/liff/v1/apps`
   - `view.type = 'full'`, `botPrompt = 'aggressive'`, URL = env(`URL_OUTSIDE_STEP`) + `liff-callback/{unique}`
   - `description = 'エルメ各種フォーム用LIFF'`
   - Cập nhật `bots`: `liff_app_id_booking`, `url_liff_app_callback`

#### Lỗi có thể xảy ra

| HTTP | Code | Mô tả | Điều kiện |
|------|------|-------|-----------|
| 200 | `success: false, msg` | `'LINEログイン設定情報に誤りがあります。再確認してください。'` | LINE Login credentials sai |
| 200 | `success: false, msg` | `'LINEログイン設定情報に誤りがあります。再確認してください。'` | Tạo LIFF App chính thất bại |
| 200 | `success: false, msg` | `'ステップ4の入力内容に誤りがあります。再確認してください。'` | Tạo LIFF App booking thất bại |

#### Side effects
- **LIFF ID thay đổi** → các tính năng sử dụng LIFF cũ (回答フォーム, 商品, カレンダー予約, イベント予約, 流入アクション) có thể bị ảnh hưởng
- Lưu `liff_app_id_old` để tham chiếu LIFF cũ

---

### EP-07: POST `/ajax/check-enable-use-webhook-modal` — Kiểm tra Webhook/LIFF (チェックする)

**Route name**: `checkEnableWebhookModal`
**Controller**: `Admin\BotController@checkEnableWebhookModal` — `BotController.php:4999`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `bot_id` | body | int | Có | — | Bot ID (plain, không encode) |

#### Response thành công

```json
{
  "success": true,
  "bot_hash": "hashid_encoded_string"
}
```

#### Logic xử lý

1. Tìm bot theo `bot_id`, lấy `channel_access_token`
2. **Kiểm tra Webhook**: `GET https://api.line.me/v2/bot/channel/webhook/endpoint`
3. Nếu `active == false`:
   - Cập nhật `is_connected = 3`
   - Trả lỗi với `flagError: 1`
4. So sánh `endpoint` với expected webhook URL
   - Nếu khác → `is_connected = 2` → trả lỗi với `flagError: 1` và `webhook_url` đúng
5. Nếu OK → `is_connected = 1` → trả `success: true`

#### Lỗi có thể xảy ra

| HTTP | Code | Mô tả | Điều kiện |
|------|------|-------|-----------|
| 200 | `success: false, flagError: 1` | `'Webhookをオンにして下さい。既にオンの場合は、一度オフにしてから再度オンに変更して下さい。'` | Bot không tồn tại, webhook tắt, hoặc webhook URL sai |

---

### EP-08: GET `/admin/change-bots-new/{id}` — Trang thay thế LOA (LOA入れ替え)

**Route name**: `change.bots.new`
**Controller**: `Admin\BotController@adminChangeNewBot` — `BotController.php:6003`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `id` | URL path | string (Hashids encoded) | Có | Hashids::decode | Bot ID đã mã hóa |
| `bot_slot_id` | query | int | Không | — | Bot slot ID |
| `type` | query | string | Không | — | Loại thay thế |
| `type_change` | query | string | Không | — | Kiểu thay đổi |

#### Response (HTML View)

Trả về view `admin.bots.bot_add_v3` — trang đăng ký LOA mới (flow thay thế).

#### Logic xử lý

1. Decode `id` → tìm bot
2. Nếu bot không tồn tại hoặc `plan_type == 2` (free) → redirect về `/admin/home`
3. Trả view với: `bot_slot_id`, `type`, `typeChange`, `bot_id`, `username`, `hash_id`

---

### EP-09: GET `/admin/home` — Trang danh sách tài khoản (アカウント一覧)

**Route name**: `adminIndex`
**Controller**: `Admin\UserController@index` — `UserController.php:341`

#### Request

Không có request params đặc biệt.

#### Response (HTML View)

Trả về view `admin.index_v2` với data:
- `notifications`: 10 thông báo mới nhất
- `roleId`: Quyền của user (`user.level`)
- `listBot`: Rỗng (lấy async qua JS)
- `botId`: Bot ID hiện tại trong session
- `user`: User object
- `basic_fee`: Phí cơ bản
- `showPopup`: Popup quảng cáo (nếu có, hiển thị 14 ngày)

**Lưu ý**: Danh sách bot được load bằng JavaScript (AJAX) sau khi trang tải, không phải render server-side.

---

### EP-10: POST `/admin/check-auth-bot` — Kiểm tra bot có campaign

**Route name**: `checkAuthBot`
**Controller**: `Admin\BotController@checkAuthBot` — `BotController.php:411`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `bot_id` | body | int | Có | — | Bot ID |

#### Response thành công

```json
{
  "success": true,
  "bot_name": "Xuka_BOT_Booking"
}
```

#### Logic xử lý

1. Tìm bot theo `bot_id`
2. Kiểm tra `has_campaign == 1` → `success: true`
3. Nếu `has_campaign != 1` → `success: false` + `'Unauthorized access.'`

**Lưu ý**: Method này kiểm tra bot có campaign hay không, KHÔNG kiểm tra kết nối LINE. Nút「接続チェック」trên giao diện sử dụng EP-03 (`adminCheckMode`).

---

### EP-11: POST `/ajax/set-time-check-webhook` — Cập nhật thời gian kiểm tra webhook

**Route name**: `ajax.SetTimeCheckWebHook`
**Controller**: `Admin\BotController@setTimeCheckWebHook` — `BotController.php:11693`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `bot_id` | body | int | Có | — | Bot ID |

#### Response thành công

```json
{
  "success": true,
  "bot_id": 1057
}
```

#### Logic xử lý

1. Cập nhật `bots`: `is_connected = 1`, `last_time_connection_check = now() + 6 tháng`
2. Mục đích: đánh dấu webhook đã kiểm tra, tránh kiểm tra lại trong 6 tháng

---

### EP-12: POST `/admin/bot/set-domain` — Cập nhật webhook URL trên LINE Platform

**Route name**: `adminSetDomain`
**Controller**: `Admin\UserController@adminSetDomain` — `UserController.php:489`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `bot_id` | body | int | Có | — | Bot ID |

#### Response thành công

```json
{
  "success": true,
  "bot_id": 1057
}
```

#### Logic xử lý

1. Tìm bot theo `bot_id`
2. Tạo endpoint mới: `env('DOMAIN_ENDPOINT_WEBHOOK') + 'line/callback/add/' + bot_id`
3. Gọi LINE API: `PUT https://api.line.me/v2/bot/channel/webhook/endpoint` với `channel_access_token`
4. Cập nhật `bots.is_connected = 1`

---

### EP-13: POST `/ajax/check-transfer-code` — Kiểm tra mã transfer code (データコピー)

**Route name**: `check.transfer.code`
**Controller**: `Admin\BotController@checkTransferCode` — `BotController.php:5940`

#### Request

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `transfer_code` | body | string | Có | — | Mã transfer code |

#### Response thành công

```json
{
  "success": true,
  "data": { /* Bots model object */ }
}
```

#### Logic xử lý

1. Tìm bot trong DB: `bots.transfer_code = transfer_code` (via `BotRepository::checkExistTransferCode`)
2. Nếu bot tìm thấy và là bot hiện tại (`bot.id == getBotId()`) → lỗi: không thể tự copy
3. Nếu bot tìm thấy và khác bot hiện tại → trả thành công
4. Nếu không tìm thấy → lỗi

#### Lỗi có thể xảy ra

| HTTP | Code | Mô tả | Điều kiện |
|------|------|-------|-----------|
| 200 | `success: false` | `'現在のアカウントのデータ受信コードは入力できません。別のアカウントのコードを入力してください。'` | Transfer code là của chính bot hiện tại |
| 200 | `success: false` | `'バックアップコードが存在しません。'` | Transfer code không tồn tại |

---

## 3. LINE API Dependencies

| API | Method | URL | Mục đích | Dùng bởi |
|-----|--------|-----|----------|----------|
| Bot Info | GET | `https://api.line.me/v2/bot/info` | Lấy thông tin bot (ảnh, tên, chatMode) | EP-03, EP-05 |
| Webhook Endpoint | GET | `https://api.line.me/v2/bot/channel/webhook/endpoint` | Kiểm tra trạng thái webhook | EP-03, EP-07 |
| Set Webhook | PUT | `https://api.line.me/v2/bot/channel/webhook/endpoint` | Cập nhật webhook URL | EP-12 |
| Access Token | POST | `https://api.line.me/v2/oauth/accessToken` | Lấy access token từ credentials | EP-02, EP-06 |
| Create LIFF App | POST | `https://api.line.me/liff/v1/apps` | Tạo LIFF App mới | EP-02, EP-06 |
| Get Followers | GET | `https://api.line.me/v2/bot/followers/ids` | Lấy danh sách bạn bè (cần verified account) | EP-04 |

---

## 4. Mapping Endpoint ↔ Màn hình UI

| Endpoint | Màn hình | Action trên UI |
|----------|----------|----------------|
| EP-01 | SCR-BE-01 | Load trang「接続設定」 |
| EP-02 | SCR-BE-01 | Nhấn「保存」 |
| EP-03 | SCR-BE-01 | Nhấn「接続チェック」 |
| EP-04 | SCR-BE-01 | Nhấn「既存友だち情報取得」 |
| EP-05 | SCR-BE-01 | Nhấn「情報更新」 |
| EP-06 | SCR-BE-04 | Nhấn「はい」trong dialog LIFF reconnect |
| EP-07 | SCR-BE-01 | Nhấn「チェックする」(LIFF check) |
| EP-08 | SCR-BE-03 | Nhấn「LINE公式アカウント入れ替え」→ navigate |
| EP-09 | SCR-BE-02 | Load trang「アカウント一覧」 |
| EP-11 | SCR-BE-01 | Tự động (sau khi check webhook thành công) |
| EP-12 | SCR-BE-01 | Tự động (khi phát hiện webhook URL sai → sửa) |
| EP-13 | SCR-BE-01 | Section「データコピー」— kiểm tra mã copy |

---

## 5. Middleware & Xác thực

### Middleware chung cho tất cả routes

| Middleware | Mô tả |
|-----------|-------|
| `web` | Session-based authentication — user phải đăng nhập |
| `NotifyChatworkRequestTimeSlow` | Monitor performance — gửi thông báo Chatwork nếu request chậm |

### Middleware bổ sung cho một số routes

| Middleware | Routes áp dụng | Mô tả |
|-----------|----------------|-------|
| `LogRequestMultipart` | EP-02 (bot-save), các AJAX routes | Log multipart request data |

### Xác thực quyền truy cập

- **Tất cả routes `/admin/*`**: Yêu cầu session đăng nhập (middleware `web`)
- **Không có middleware `supper_admin`**: Các endpoint trong scope bot-edit không yêu cầu quyền super admin
- **Quyền trên bot**: Controller kiểm tra `getCurrentUser()` → `admin_id` — user phải là admin sở hữu bot hoặc staff được gán quyền (qua `user_bot`)
- **Staff access**: Staff không truy cập được trang `/admin/bot-edit` vì sidebar menu chỉ hiện cho Admin. Tuy nhiên, backend **không có middleware chặn rõ ràng** — nếu staff biết URL, có thể truy cập (cần xác nhận bổ sung)
