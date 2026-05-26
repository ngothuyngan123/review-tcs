# Logic Spec — 「LOA接続設定」(Cài đặt kết nối LOA)

**Feature ID**: bot-edit
**Ngày phân tích**: 2026-03-30
**Nguồn**: Laravel source code — phân tích trực tiếp
**Confidence**: Cao (từ code)

---

## 1. Controllers & Actions

### 1.1 Admin\BotController — `app/Http/Controllers/Admin/BotController.php` (11,763 dòng)

Controller chính xử lý mọi thao tác liên quan đến bot (LOA). Trong scope tính năng bot-edit, các methods liên quan:

| Method | Line | Route | Mô tả logic |
|--------|------|-------|-------------|
| `botAdd()` | :278 | GET `/admin/bot-edit` | Load trang cài đặt. Decode Hashids ID → lấy bot + managers + settings → render view |
| `botChange()` | :566 | POST `/admin/bot-save` | Xử lý lưu thay đổi phức tạp nhất: validate, gọi LINE API, tạo LIFF Apps, upload ảnh, cập nhật DB |
| `checkAuthBot()` | :411 | POST `/admin/check-auth-bot` | Kiểm tra `has_campaign` flag (không kiểm tra kết nối LINE) |
| `addFlagGetOldFriend()` | :5962 | POST `/ajax/add-flag-get-old-friend` | Kiểm tra LINE API followers → set flag cho background job lấy bạn bè |
| `reGetAvatarBot()` | :11149 | POST `/ajax/reGetAvatarBot` | Gọi LINE Bot Info API → đồng bộ ảnh + tên vào `bots` và `bots_profiles` |
| `reCreateLiffApp()` | :11196 | POST `/ajax/bot/re-create-liffapp` | Tạo lại LIFF App (1 hoặc 2 apps) khi kết nối bị đứt |
| `checkEnableWebhookModal()` | :4999 | POST `/ajax/check-enable-use-webhook-modal` | Kiểm tra webhook status trên LINE Platform → cập nhật `is_connected` |
| `adminChangeNewBot()` | :6003 | GET `/admin/change-bots-new/{id}` | Load trang thay thế LOA — redirect nếu bot free |
| `checkTransferCode()` | :5940 | POST `/ajax/check-transfer-code` | Kiểm tra transfer code tồn tại → trả bot info |
| `setTimeCheckWebHook()` | :11693 | POST `/ajax/set-time-check-webhook` | Set `is_connected = 1` + `last_time_connection_check = now + 6 tháng` |
| `checkDisCallbackUnique()` | :501 | — (private) | Đệ quy kiểm tra `liff_callback_unique` chưa trùng → trả random string |

#### botAdd() — Chi tiết logic (:278)

```
1. getCurrentUser() → adminId
2. Hashids::decode(request.id) → id_decode
3. IF id không null (chế độ EDIT):
   a. Bots::find(id_decode) → data
   b. LEFT JOIN users + user_bot → managers (kèm hasChoose flag)
   c. Bots::where(id_decode) → bots
   d. Nếu bots.liff_callback_unique == null:
      - str_random(10) → checkDisCallbackUnique() → liff_callback_unique
      - Lưu vào DB
4. ELSE (chế độ ADD):
   a. managers = Users có role=1, cùng admin_id, chưa xóa
5. Tính flagChangeFreePlan: user đăng ký sau 2021-07-01 → 1, trước → 0
6. Đếm botFreeNumber (plan_type=2, is_deleted=0)
7. Lấy IP server từ env('BASE_URL')
8. roleId = Auth::user()->level
9. Kiểm tra bot_slot_id hợp lệ (thuộc admin hiện tại)
10. Render view admin.bots.bot_add
```

#### botChange() — Chi tiết logic (:566)

```
1. VALIDATE: bot_name required|max:100
2. Nếu tạo mới (id == null):
   a. Kiểm tra countBot < admin.max_bot
   b. Validate url: required|url|max:200|url_exists:bots
3. Nếu edit (id có giá trị):
   a. Decode Hashids → id_decode
   b. Validate url_exists (exclude self)
   c. Validate domain_url_shorten (check DNS pointing)

4. === GỌI LINE MESSAGING API ===
   a. POST https://api.line.me/v2/oauth/accessToken
      - Input: channel_id (hiện tại), channel_secret (từ request)
      - Output: access_token (30-day token)
      - Lưu: channel_access_token, expired_date +28 ngày, renew_channel_access_error=0
   b. Nếu thất bại → lỗi: '入力した情報が間違っています...'

5. === GỌI LINE LOGIN API (chỉ khi thay đổi) ===
   Điều kiện: channel_id_line_login không rỗng VÀ (channel_id hoặc secret thay đổi so với DB)
   a. POST https://api.line.me/v2/oauth/accessToken (LINE Login)
      - Input: channel_id_line_login, channel_secret_line_login
      - Output: tokenLineLogin
   b. Nếu thất bại → lỗi: 'LINEログイン設定情報に誤りがあります...'

6. === TẠO LIFF APPS (chỉ khi LINE Login thay đổi) ===
   a. Lấy hoặc sinh liff_callback_unique
   b. LIFF App 1 (流入アクション用):
      - POST https://api.line.me/liff/v1/apps
      - view.type = 'full', url = /liff-callback/{unique}
      - description = 'エルメ流入アクション用LIFF'
      → Lưu: liff_app_id, liff_callback_unique, channel_id_line_login, channel_secret_line_login
      → Backup: liff_app_id_old (lần đầu)
   c. LIFF App 2 (各種フォーム用):
      - POST https://api.line.me/liff/v1/apps
      - view.type = 'full', botPrompt = 'aggressive'
      - url = env(URL_OUTSIDE_STEP) + liff-callback/{unique}
      - description = 'エルメ各種フォーム用LIFF'
      → Lưu: liff_app_id_booking, url_liff_app_callback

7. === CẬP NHẬT DB ===
   a. settings = {channel_secret, channel_access_token, view_name, url, phone, ...}
   b. Nếu channel_secret → trim whitespace
   c. Nếu token mới → ghi đè channel_access_token + expired_date +28 ngày

8. === XỬ LÝ ẢNH ===
   a. Nếu url_image == '/images/camera.png' → bot_image = null (xóa ảnh)
   b. Nếu link_of_image → grab_image() clone từ URL
   c. Nếu image file upload:
      - Image::make() → save
      - resizeImageToMaxSize(path, 2048) — resize nếu > 2048px
   d. Lưu path ảnh vào settings['bot_image']

9. === KHI TẠO MỚI ===
   a. Kiểm tra bot đã bị xóa (is_deleted=1) có cùng URL → khôi phục
   b. Nếu không → INSERT bots + tạo webhook_url + AddFriendSetting
   c. Gán role_add_bot dựa trên quyền user:
      - role=0 → 0 (primary admin)
      - level=1 → 1 (deputy), level=2 → 2 (manager), else → 3 (support)

10. === KHI EDIT ===
    a. UPDATE bots SET settings
    b. UPDATE domain_url_shorten (http thay https)
    c. Xóa bot_error_message
    d. Soft-delete tất cả user_bot → upsert lại
    e. Reset callback events (status 10 → 0)

11. === CẬP NHẬT PROFILE ===
    a. BotsProfiles (is_default=1) → avt_path, nick_name

12. Trả JSON success: true
```

#### reCreateLiffApp() — Chi tiết logic (:11196)

```
1. Decode bot_id (Hashids) → tìm bot
2. Gọi LINE Login accessToken API → tokenLineLogin
3. Nếu liffAppError == 1:
   - Tạo LIFF App chính (流入アクション用)
   - Lưu: liff_app_id, liff_callback_unique, channel_id_line_login, channel_secret_line_login
   - Backup: liff_app_id_old (nếu chưa có)
4. Nếu liffAppErrorBooking == 1:
   - Tạo LIFF App booking (各種フォーム用)
   - Lưu: liff_app_id_booking, url_liff_app_callback
5. Trả success + bot object
```

### 1.2 Admin\UserController — `app/Http/Controllers/Admin/UserController.php` (9,503 dòng)

| Method | Line | Route | Mô tả logic |
|--------|------|-------|-------------|
| `index()` | :341 | GET `/admin/home` | Load trang chính, danh sách bot load async qua JS |
| `adminCheckMode()` | :380 | POST `/admin/bot/check-mode` | Kiểm tra kết nối 3 lớp: Bot Info API + Webhook status + Webhook URL |
| `adminSetDomain()` | :489 | POST `/admin/bot/set-domain` | Gọi LINE API cập nhật webhook URL |
| `adminCheckActiveDomain()` | :516 | POST `/admin/bot/check-active-domain` | Kiểm tra webhook active status |

#### adminCheckMode() — Chi tiết logic (:380)

```
1. Lấy bot từ DB (where is_deleted <> 1)
2. Init newDataBot = { is_connected: 0 }
3. Nếu is_connected == 1 hoặc last_time_connection_check rỗng:
   → newDataBot.last_time_connection_check = now()

4. === KIỂM TRA 1: Bot Info ===
   GET https://api.line.me/v2/bot/info (Authorization: Bearer channel_access_token)
   - Thất bại → is_connected = 0, trả '認証できませんでした。'

5. === KIỂM TRA 2: Webhook URL ===
   GET https://api.line.me/v2/bot/channel/webhook/endpoint
   - Lấy data.endpoint
   - So sánh với expected: env('DOMAIN_ENDPOINT_WEBHOOK') + 'line/callback/add/' + botId
   - Khác nhau → is_connected = 2, trả 'webhookの設定が間違っています'

6. === KIỂM TRA 3: Webhook Active ===
   - data.active == false → is_connected = 3, trả '一度オフしてからオンにして下さい'

7. === TẤT CẢ OK ===
   is_connected = 1, last_time_connection_check = now()
   Trả: success: true, msg: '正常に接続しています。', bot object
```

---

## 2. Models Eloquent

### 2.1 Bots — `app/Bots.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| **Table** | `bots` |
| **Primary Key** | `id` |
| **Timestamps** | true (`created_at`, `updated_at`) |
| **Guarded** | `[]` (mass assignable tất cả) |

#### Cột DB liên quan đến tính năng bot-edit

| Cột | Kiểu | Mô tả | Dùng bởi |
|-----|------|-------|----------|
| `id` | int(12) | PK — Bot ID | Tất cả |
| `admin_id` | int(12) | FK → users.id — Admin sở hữu | Quyền truy cập |
| `view_name` | varchar(128) | Tên hiển thị LOA (アカウント名) | EP-02 save |
| `bot_image` | varchar(500) | URL hoặc path ảnh đại diện | EP-02 save, EP-05 sync |
| `channel_id` | varchar(128) | Messaging API Channel ID (read-only trên UI) | EP-02 lấy token |
| `channel_secret` | varchar(500) | Messaging API Channel Secret | EP-02 save |
| `channel_access_token` | varchar(500) | Access token LINE (auto-renew) | EP-02, EP-03, EP-04, EP-05 |
| `channel_id_line_login` | varchar(255) | LINE Login Channel ID | EP-02, EP-06 |
| `channel_secret_line_login` | varchar(255) | LINE Login Channel Secret | EP-02, EP-06 |
| `liff_app_id` | varchar(50) | LIFF App ID chính (流入アクション用) | EP-02, EP-06 |
| `liff_app_id_booking` | varchar(64) | LIFF App ID booking (各種フォーム用) | EP-02, EP-06 |
| `liff_app_id_old` | varchar(255) | Backup LIFF App ID cũ (lần thay đổi đầu tiên) | EP-02, EP-06 |
| `liff_callback_unique` | varchar(50) | Random string 10 ký tự — unique per bot | EP-01, EP-02, EP-06 |
| `url_liff_app_callback` | varchar(255) | URL callback cho LIFF App booking | EP-02, EP-06 |
| `webhook_url` | varchar(500) | Webhook URL (generated: domain + bot_id) | EP-01 display |
| `transfer_code` | varchar(16) | Mã transfer code (コピーコード trên UI) | EP-13 |
| `backup_code` | varchar(16) | Mã backup code | — |
| `is_connected` | tinyint(4) | Trạng thái kết nối: 0=lỗi, 1=OK, 2=webhook sai, 3=webhook tắt | EP-03, EP-07 |
| `last_time_connection_check` | datetime | Thời điểm kiểm tra kết nối gần nhất | EP-03, EP-11 |
| `expired_date_channel_access_token` | datetime | Hạn access token (now + 28 ngày) | EP-02 |
| `renew_channel_access_error` | tinyint(4) | 0=renew OK, 1=renew fail | EP-02 |
| `is_get_old_friend` | tinyint(4) | Flag lấy bạn bè: 0=chưa, 1=đang xử lý, 3=hoàn thành(?), fail=lỗi | EP-04 |
| `plan_type` | int(11) | 1=standard, 2=free | EP-08 check |
| `is_deleted` | tinyint(1) | Soft delete flag | Tất cả |
| `domain_url_shorten` | varchar(255) | Domain rút gọn URL tùy chỉnh | EP-02 save |
| `has_campaign` | tinyint(4) | 0=không, 1=có campaign | EP-10 |
| `is_verify` | tinyint(1) | Tài khoản đã xác thực | — |
| `role_add_bot` | tinyint(4) | Quyền người tạo bot: 0=primary, 1=deputy, 2=manager, 3=support | EP-02 create |
| `user_add` | int(11) | User ID người tạo bot | EP-02 create |

#### Relationships

| Relationship | Kiểu | Model liên quan | FK |
|-------------|------|----------------|-----|
| `admin()` | belongsTo | User | `admin_id` → `users.id` |
| `bot_line_users()` | hasMany | BotLineUser | `bot_id` |
| `accessBot()` | hasMany | AccessBot | `bot_id` |
| `Individuals()` | hasMany | IndividualSetting | `bot_id` |
| `landingPages()` | hasMany | LandingPages | `bot_id` |
| `Affiliates()` | hasMany | Affiliaters | `admin_id` |
| `botServices()` | hasMany | BotService | `bot_id` |
| `staffBot()` | hasOne | UserStaffBot | `bot_id` |
| `category()` | hasOne | BotCategory | `bot_id` |

#### Accessors

| Accessor | Logic |
|----------|-------|
| `getHashBotIdAttribute()` | `Hashids::encode(id)` — trả Hashids encoded ID |
| `getBotImageAttribute()` | Nếu `bot_image` không chứa `https` → wrap bằng `asset()` |

### 2.2 BotsProfiles — `app/BotsProfiles.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| **Table** | `bots_profiles` |
| **Guarded** | `[]` |
| **Timestamps** | true |

#### Cột

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `bot_id` | int(11) | FK → bots.id |
| `user_id` | int(11) | FK → users.id |
| `avt_path` | varchar(255) | URL/path ảnh đại diện |
| `nick_name` | varchar(255) | Tên hiển thị |
| `is_default` | tinyint(4) | 1 = profile mặc định |
| `position` | int(11) | Thứ tự sắp xếp |

**Vai trò**: Mỗi bot có nhiều profiles (cho chat). Profile `is_default = 1` là profile chính, được đồng bộ khi thay đổi ảnh/tên bot.

### 2.3 BotUsers — `app/BotUsers.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| **Table** | `user_bot` |
| **Guarded** | `[]` |

#### Cột

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `user_id` | int(12) | FK → users.id — User được gán quyền |
| `bot_id` | int(12) | FK → bots.id — Bot được gán |
| `is_tester` | tinyint(1) | Flag tester |
| `is_deleted` | tinyint(1) | Soft delete |

**Vai trò**: Bảng pivot liên kết user (staff/manager) với bot. Được cập nhật khi save bot-edit (soft-delete all → upsert).

### 2.4 AccessBot — `app/AccessBot.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| **Table** | `access_bot` |

#### Cột

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `admin_id` | int(11) | FK → users.id |
| `bot_id` | int(11) | FK → bots.id |

**Vai trò**: Quyền truy cập bot cho admin/staff phụ.

### 2.5 BotSlots — `app/BotSlots.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| **Table** | `bot_slots` |

**Vai trò**: Mỗi hợp đồng (`bot_contracts`) có nhiều slots, mỗi slot gắn 1 bot. Dùng trong EP-01 (kiểm tra quyền `bot_slot_id`) và EP-08 (thay thế LOA).

### 2.6 BotContracts — `app/BotContracts.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| **Table** | `bot_contracts` |

**Vai trò**: Quản lý hợp đồng thanh toán. Liên kết `bot_contracts → bot_slots → bots`. Trạng thái `status_payment_fail` ảnh hưởng hiển thị trên SCR-BE-02.

---

## 3. Services / Repositories

### 3.1 BotRepository — `app/Repositories/Eloquents/BotRepository.php`

| Method | Line | Mô tả |
|--------|------|-------|
| `findById($id)` | :30 | Tìm bot by ID (single hoặc array) |
| `checkExistTransferCode($transferCode)` | :141 | Tìm bot theo `transfer_code` (where NOT NULL) |
| `getListBotsUser($userId)` | :44 | Lấy danh sách bot kèm đếm friend (block/active/all) |
| `updateBot($id, $data)` | :113 | Update bot by ID |
| `countBotUser($userId)` | :119 | Đếm số bot active của user |

### 3.2 UserRepository

Inject vào BotController qua constructor. Method sử dụng: `findById($id)`.

### 3.3 CallbackEventRepository

Inject vào BotController. Method sử dụng: `updateWithCondition()` — reset callback events khi save bot.

---

## 4. Form Requests / Validation

### Validation trong botChange() (:566)

**Không dùng Form Request class riêng** — validate inline bằng `Validator::make()`.

#### Rules (khi edit)

| Field | Rule | Error Message (JP) |
|-------|------|--------------------|
| `bot_name` | `required\|max:100` | (Laravel default: 「アカウント名（管理用）は必ず指定してください。」) |
| `url` | `required\|url\|max:200\|url_exists:bots` (khi tạo mới) | `'フォーマットが不正です、URLのフォーマットで入力してください。'` / `'友だち追加URLは既に登録されています。'` |
| `domain_url_shorten` | `nullable\|url\|max:100\|check_point` (khi có giá trị) | `'URLのフォーマットで入力して下さい。'` / `'ドメイン設定が確認できません。...'` |

#### Custom Validators

| Validator | Logic | File:Line |
|-----------|-------|-----------|
| `url_exists` | Kiểm tra URL chưa được bot khác sử dụng (exclude self) | BotController.php:593 |
| `check_point` | Kiểm tra domain DNS trỏ đúng IP server (gethostbyname) | BotController.php:626 |

---

## 5. Events / Listeners / Queued Jobs

### Không có Events/Listeners trực tiếp trong scope bot-edit

Tuy nhiên, có 2 tác động liên quan đến background jobs:

#### 5.1 Flag `is_get_old_friend` — Trigger job lấy bạn bè

- Khi EP-04 (`addFlagGetOldFriend`) set `is_get_old_friend = 1`
- **Background job** (Spring Boot) poll database, thấy flag = 1 → bắt đầu lấy danh sách bạn bè từ LINE API
- Job gọi `GET https://api.line.me/v2/bot/followers/ids` (phân trang) → INSERT vào `bot_line_user`
- Quá trình có thể mất tối đa 5 giờ (message trả về cho user)

#### 5.2 Callback Events Reset

- Khi save bot (EP-02), reset `callback_events` table: `status = 10 → status = 0`
- Mục đích: đánh dấu callback events cần xử lý lại sau khi thay đổi cấu hình bot

#### 5.3 Channel Access Token Renewal

- `expired_date_channel_access_token` = now + 28 ngày
- **Background job** (Spring Boot hoặc Laravel schedule) kiểm tra và renew token trước khi hết hạn
- Nếu renew thất bại → `renew_channel_access_error = 1`

---

## 6. Authorization (Policies, Gates)

### Không có Policy/Gate class riêng

Quyền truy cập được kiểm tra trực tiếp trong controller:

| Kiểm tra | Method | Logic | File:Line |
|----------|--------|-------|-----------|
| **User đăng nhập** | Middleware `web` | Session-based | — |
| **Admin sở hữu bot** | `getCurrentUser()` | Lấy admin_id từ session, so sánh với `bots.admin_id` | BotController.php:282 |
| **Bot slot thuộc admin** | `BotSlots::where('id', bot_slot_id)->value('admin_id') == getCurrentUser()` | Kiểm tra quyền sở hữu slot | BotController.php:351 |
| **Quyền thêm bot** | `countBot < admin.max_bot` | Giới hạn số bot theo hợp đồng | BotController.php:586 |
| **Bot free không thay thế** | `bot.plan_type == 2 → redirect` | Bot free không cho phép thay thế | BotController.php:6008 |

### Phân quyền Admin/Staff

| Cơ chế | Mô tả |
|--------|-------|
| `user.role` | 0 = admin gốc |
| `user.level` | 1 = deputy manager (副管理人), 2 = manager, 3+ = support |
| `role_add_bot` | Ghi nhận quyền người tạo bot: 0 = primary admin, 1 = deputy, 2 = manager, 3 = support |

**Lưu ý quan trọng**: Không có middleware chặn rõ ràng cho Staff truy cập `/admin/bot-edit`. Sidebar menu ẩn mục này cho Staff (qua view logic), nhưng nếu Staff biết URL → có thể truy cập (cần kiểm tra thêm ở view layer hoặc JS).

---

## 7. Business Rules (tổng hợp từ code)

### 7.1 Hashids Encoding

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-01 | Bot ID trên URL và request luôn được encode bằng Hashids. Decode trước khi query DB | BotController.php:289, :602, :950 |
| BR-02 | Một số AJAX endpoint nhận bot_id plain (không encode): `check-mode`, `reGetAvatarBot`, `check-enable-use-webhook-modal` | UserController.php:384, BotController.php:11152, :5000 |

### 7.2 LIFF App Management

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-03 | Mỗi bot có 2 LIFF Apps: 1 cho 流入アクション (liff_app_id), 1 cho 各種フォーム (liff_app_id_booking) | BotController.php:748, :789 |
| BR-04 | Khi thay đổi LINE Login credentials → tạo lại cả 2 LIFF Apps | BotController.php:709 |
| BR-05 | LIFF App cũ được backup vào `liff_app_id_old` (chỉ lần đầu thay đổi) | BotController.php:774 |
| BR-06 | `liff_callback_unique` là random string 10 ký tự, unique toàn hệ thống, sinh 1 lần per bot | BotController.php:311, :501 |
| BR-07 | LIFF App booking dùng URL prefix từ env(`URL_OUTSIDE_STEP`) nếu có, fallback `url()` | BotController.php:786 |

### 7.3 Channel Access Token

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-08 | Khi thay đổi Channel Secret → tự động gọi LINE API lấy access token mới (30 ngày) | BotController.php:685 |
| BR-09 | Token mới lưu với `expired_date_channel_access_token = now + 28 ngày` (buffer 2 ngày) | BotController.php:848 |
| BR-10 | Reset `renew_channel_access_error = 0` khi lấy token thành công | BotController.php:849 |
| BR-11 | Whitespace trong `channel_secret` bị trim trước khi lưu (`preg_replace('/\s+/', '')`) | BotController.php:827 |

### 7.4 Image Handling

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-12 | Path ảnh: `media/images/{adminId}/{botId}/bot/{timestamp}{random6}.{ext}` | BotController.php:885 |
| BR-13 | Ảnh upload được resize max 2048px (giữ aspect ratio) | BotController.php:890 |
| BR-14 | Nếu `url_image == '/images/camera.png'` → xóa ảnh (set `bot_image = null`) | BotController.php:952 |
| BR-15 | Ảnh có thể upload trực tiếp (file) hoặc clone từ URL (`link_of_image`) | BotController.php:870, :880 |

### 7.5 Connection Check

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-16 | `is_connected` states: 0=auth lỗi, 1=OK, 2=webhook URL sai, 3=webhook tắt | UserController.php:394-478 |
| BR-17 | Kiểm tra kết nối 3 lớp: (1) Bot Info API → (2) Webhook endpoint URL → (3) Webhook active flag | UserController.php:399, :430, :460 |
| BR-18 | Webhook URL expected format: `env('DOMAIN_ENDPOINT_WEBHOOK') + 'line/callback/add/' + botId` | UserController.php:451 |
| BR-19 | `setTimeCheckWebHook` set `last_time_connection_check = now + 6 tháng` (tránh check lại liên tục) | BotController.php:11698 |

### 7.6 Get Old Friends

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-20 | Chỉ tài khoản đã xác thực (verified/certified) mới lấy được danh sách bạn bè | BotController.php:5983 |
| BR-21 | `is_get_old_friend` states: 0=chưa, 1=đang xử lý, 3=hoàn thành, fail=API không hỗ trợ | BotController.php:5994 |
| BR-22 | Nếu đang xử lý (is_get_old_friend khác 3 và khác fail) → không set lại flag (tránh restart job) | BotController.php:5996 |
| BR-23 | Thời gian xử lý: tối đa 5 giờ (thông báo cho user) | BotController.php:5999 |

### 7.7 Bot Creation (khi tạo mới qua bot-save)

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-24 | Giới hạn số bot: `countBot < admin.max_bot` | BotController.php:586 |
| BR-25 | URL thêm bạn (`url_add_friend`) phải unique per admin | BotController.php:593 |
| BR-26 | Nếu bot đã bị xóa (is_deleted=1) có cùng URL → khôi phục thay vì tạo mới | BotController.php:909 |
| BR-27 | Webhook URL tự sinh: `env('DOMAIN_ENDPOINT_WEBHOOK') + 'line/callback/add/' + bot_id` | BotController.php:929 |
| BR-28 | Tự tạo `AddFriendSetting` mặc định cho bot mới | BotController.php:937 |

### 7.8 LOA Replacement (Thay thế LOA)

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-29 | Bot free (`plan_type == 2`) không cho phép thay thế → redirect về `/admin/home` | BotController.php:6008 |
| BR-30 | Trang thay thế LOA dùng chung view `admin.bots.bot_add_v3` (flow đăng ký LOA mới) | BotController.php:6016 |

### 7.9 Data Copy (Transfer Code)

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-31 | Transfer code phải tồn tại và NOT NULL trong DB | BotRepository.php:144 |
| BR-32 | Không thể nhập transfer code của chính bot hiện tại | BotController.php:5947 |

### 7.10 Profile Sync

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-33 | Khi save bot (EP-02): tự động cập nhật `bots_profiles` (is_default=1) với `avt_path` và `nick_name` | BotController.php:1018-1022 |
| BR-34 | Khi đồng bộ từ LINE (EP-05): cập nhật cả `bots` và `bots_profiles` (is_default=1) | BotController.php:11186-11189 |

### 7.11 Free Plan Flag

| Rule | Mô tả | File:Line |
|------|-------|-----------|
| BR-35 | `flagChangeFreePlan`: User đăng ký sau 2021-07-01 → flag = 1 (áp dụng chính sách mới) | BotController.php:327-334 |
| BR-36 | `botFreeNumber`: Đếm số bot free (plan_type=2, is_deleted=0) của admin | BotController.php:329-331 |

---

## 8. Tóm tắt thay đổi DB theo action

| Action (UI) | Bảng `bots` | Bảng `bots_profiles` | Bảng `user_bot` | Bảng khác |
|-------------|-------------|---------------------|-----------------|-----------|
| 「保存」 | UPDATE: view_name, channel_secret, channel_access_token, bot_image, domain_url_shorten, channel_id_line_login, channel_secret_line_login, liff_app_id, liff_app_id_booking, liff_callback_unique, expired_date_channel_access_token, renew_channel_access_error, bot_error_message | UPDATE (is_default=1): avt_path, nick_name | Soft-delete all → upsert | callback_events: status 10→0 |
| 「情報更新」 | UPDATE: bot_image, view_name | UPDATE (is_default=1): avt_path, nick_name | — | — |
| 「接続チェック」 | UPDATE: is_connected, last_time_connection_check | — | — | — |
| 「既存友だち情報取得」 | UPDATE: is_get_old_friend | — | — | (Background job: INSERT bot_line_user) |
| LIFF reconnect「はい」 | UPDATE: liff_app_id, liff_app_id_booking, liff_app_id_old, liff_callback_unique, channel_id_line_login, channel_secret_line_login, url_liff_app_callback | — | — | — |
| 「チェックする」(LIFF) | UPDATE: is_connected | — | — | — |

---

## 9. Ghi chú cho Job Analyzer

Các điểm cần điều tra bên Spring Boot (background jobs):

1. **Job lấy bạn bè cũ**: Poll `bots.is_get_old_friend = 1` → gọi LINE Followers API → INSERT `bot_line_user` → cập nhật `is_get_old_friend`
2. **Job renew channel access token**: Poll `bots.expired_date_channel_access_token` gần hết hạn → gọi LINE OAuth API → cập nhật token mới
3. **Job kiểm tra webhook**: Có thể có job định kỳ kiểm tra `is_connected` cho tất cả bot

---

## 10. Ghi chú cho DB Mapper

### Mapping cột DB ↔ UI field (đã xác nhận từ code)

| UI Field (JP) | DB Column | Bảng |
|---------------|-----------|------|
| 「アカウント名」 | `view_name` | bots |
| 「アカウント画像」 | `bot_image` | bots |
| 「Channel ID」 | `channel_id` | bots |
| 「Channel Secret」 | `channel_secret` | bots |
| 「Webhook URL」 | `webhook_url` | bots |
| 「チャネル ID」(LIFF) | `channel_id_line_login` | bots |
| 「チャネルシークレット」(LIFF) | `channel_secret_line_login` | bots |
| 「接続済みLIFF ID」 | `liff_app_id` | bots |
| 「コピーコード」 | `transfer_code` | bots |

### Bảng liên quan chính

```
users (admin accounts)
  ├── bots (admin_id → users.id)
  │     ├── bots_profiles (bot_id → bots.id) — profile chat, is_default=1 là chính
  │     ├── bot_line_user (bot_id → bots.id) — LINE users liên kết
  │     ├── access_bot (bot_id → bots.id) — quyền truy cập
  │     └── callback_events — (admin_id, bot_id)
  ├── user_bot (user_id → users.id, bot_id → bots.id) — staff/manager gán bot
  └── bot_slots (admin_id → users.id)
        └── bot_contracts (id → bot_slots.bot_contract_id)
```
