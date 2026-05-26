# Logic Spec — FA-034: Liên kết hệ thống thanh toán「決済システム連携設定」

> **Mã tính năng**: FA-034
> **Portal**: Admin
> **Ngày tạo**: 2026-03-26
> **Nguồn**: Phân tích source code Laravel — controllers, models, helpers, views, jobs

---

## 1. Controllers & Actions

### 1.1. SalesManagementController — linkPayment()

**File**: `app/Http/Controllers/Basic/SalesManagementController.php:66-292`
**Mức độ tin cậy**: **Cao**

#### Logic chi tiết

**Phần A — Xử lý Stripe OAuth callback (dòng 68-184)**

1. Lấy `code` và `state` từ query params
2. Nếu `code` và `state` tồn tại:
   - **state = 1 (test)**:
     - Set Stripe API key = `env('ITEM_STRIP_SECRET_TEST_KEY')`
     - Gọi `\Stripe\OAuth::token()` với authorization code
     - Lưu vào `s_strip_bot`: `strip_secret_test_key`, `strip_public_test_key`, `account_test_id`, `status_strip_bot = 1`
     - Redirect về `/basic/list-items?connect=1`
   - **state = 2 (production)**:
     - Set Stripe API key = `env('ITEM_STRIP_SECRET_LIVE_KEY')`
     - Gọi `\Stripe\OAuth::token()` với authorization code
     - Lưu vào `s_strip_bot`: `strip_secret_live_key`, `strip_public_live_key`, `account_live_id`, `status_strip_bot = 2`
     - Redirect về `/basic/list-items`

3. **Kiểm tra account test vs production** (dòng 162-179):
   - Nếu cả `account_test_id` và `account_live_id` đều có, và `status_strip_bot != 3`:
     - Nếu **khác nhau** → xóa toàn bộ Stripe keys, set `status_strip_bot = 0`, hiển thị lỗi
     - Nếu **giống nhau** → set `status_strip_bot = 2`

4. **Tự động finalize khi status = 2** (dòng 181-233):
   - Khi `status_strip_bot == 2` → tự động chuyển sang `status_strip_bot = 3` (hoàn thành)
   - Tạo 4 tax rates trên Stripe (cả test và production):
     - 消費税 8% inclusive (test + live)
     - 消費税 10% inclusive (test + live)
   - Lưu tax rate IDs vào `s_strip_bot`

**Phần B — Chuẩn bị dữ liệu view (dòng 235-291)**

5. Lấy thông tin Stripe (nếu `status_strip_bot` có giá trị):
   - Nếu `status_strip_bot == 3` → gọi Stripe API lấy email account
6. Lấy thông tin UnivaPay:
   - Kiểm tra `univapay_app_id` && `univapay_app_test_id` có giá trị → `univapayLinked = true`
   - Webhook URL từ `env('DOMAIN_WEBHOOK_UNIVAPAY_BILL')` hoặc `url('/mobile/univapay-callback-payment')`
7. Lấy `flag_image`, `flag_installment`, `flag_brand_card_univapay`
8. Render view `basic.link_payment.index`

#### status_strip_bot — State Machine

| Giá trị | Ý nghĩa | Chuyển tiếp |
|---------|---------|-------------|
| `null/0` | Chưa liên kết hoặc lỗi | → 1 (khi test connect thành công) |
| `1` | Đã liên kết test | → 2 (khi production connect thành công) |
| `2` | Đã liên kết cả test + production | → 3 (tự động, khi access trang và accounts giống nhau) |
| `3` | Hoàn thành — đã tạo tax rates | Trạng thái cuối cùng |

**Mức độ tin cậy**: **Cao** — xác nhận từ code logic rõ ràng.

---

### 1.2. SalesManagementController — checkStep3Stripe()

**File**: `app/Http/Controllers/Basic/SalesManagementController.php:533-555`
**Mức độ tin cậy**: **Cao**

#### Logic
1. Kiểm tra `botIdCurrent` (từ request) == `getBotId()` (từ session) → tránh trường hợp user đổi account giữa chừng
2. Nếu khớp → set `status_strip_bot = 3` cho StripBot record
3. Trả về `{ success: true }`

> **Ghi chú**: Method này có vẻ là backup/alternative cho việc set status = 3 tự động trong `linkPayment()`. Được gọi từ JS khi UI detect đã hoàn thành production connect.

---

### 1.3. LinkPaymentController — index()

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:31-192`
**Mức độ tin cậy**: **Cao**

> **Lưu ý**: Method này có logic gần giống `SalesManagementController@linkPayment()`. Route `/basic/list-items` trỏ đến `SalesManagementController@linkPayment`. Có khả năng `LinkPaymentController@index()` là phiên bản cũ hơn, còn tồn tại nhưng **không được route tới trực tiếp** ở phiên bản hiện tại.

#### Khác biệt so với SalesManagementController@linkPayment:
- `LinkPaymentController` **không có logic finalize** (tạo tax rates khi status = 2 → 3). Nó chỉ set status = 2 mà không chuyển tiếp.
- `SalesManagementController` có logic chuyển 2 → 3 tự động kèm tạo tax rates.
- Khi Stripe test/production account khác nhau: `LinkPaymentController` chỉ xóa `account_test_id` + set status = 0; `SalesManagementController` xóa toàn bộ keys.

**Mức độ tin cậy**: **Cao** — nhưng cần lưu ý method nào thực sự được route sử dụng.

---

### 1.4. LinkPaymentController — saveInfoUnivapay()

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:194-445`
**Mức độ tin cậy**: **Cao**

#### Logic chi tiết

1. **Nhận dữ liệu** từ request: token/secret (test + production), webhook URL, webhook ID

2. **Xác thực Production credentials** (dòng 210-258):
   - Gọi `UnivapayPayment::getAccountInfo()` với secret + token production
   - **Kiểm tra domain**: decode JWT token → kiểm tra `payload.domains` có chứa domain của `env('URL_OUTSIDE_STEP')` không
   - Nếu domain không khớp → trả lỗi: `本番環境用のドメインは「{host}」のみ指定可能です`
   - Nếu API thành công → lấy `email` và `items_id[0].id` làm `univapay_app_id`

3. **Cập nhật LIFF callback URL** (dòng 260-358):
   - Nếu bot có `channel_id_line_login` và `channel_secret_line_login`:
     - Lấy LINE Login access token
     - Kiểm tra domain trong JWT UnivaPay token
     - Nếu domain khớp → LIFF callback URL = `env('URL_OUTSIDE_STEP') + 'liff-callback/' + liff_callback_unique`
     - Nếu không khớp → sử dụng `env('DOMAIN_WEB_ADMIN')`
     - Gọi LINE API cập nhật LIFF app URL

4. **Xác thực Test credentials** (dòng 360-390):
   - Gọi `UnivapayPayment::getAccountInfo()` với secret + token test
   - Decode JWT test token, kiểm tra domain tương tự
   - Lấy `univapay_app_test_id` và `univapay_email_test`

5. **Lưu dữ liệu** (dòng 392-399):
   - Nếu chưa có record → `StripBot::create()` (kèm `flag_brand_card_univapay = "0,1"` mặc định)
   - Nếu đã có → `StripBot::where('bot_id', $botId)->update()`

6. **Xác thực Webhook** (dòng 401-437):
   - Nếu `univapay_webhook_id` có giá trị:
     - Gọi UnivaPay API `GET /stores/{id}/webhooks/{wh_id}` kiểm tra
     - Kiểm tra: URL đúng, active = true, triggers chứa `charge_finished`
     - Nếu không đúng → gọi `PATCH` cập nhật webhook
     - Nếu thành công → set `status_webhook = 1`
     - Nếu thất bại → set `status_webhook = 0`, xóa `univapay_webhook_id`, trả message lỗi

7. **Trả response JSON** với status, email, appId, message

#### Side effects quan trọng
- **Cập nhật LIFF app URL** trên LINE platform (ảnh hưởng đến booking flow bên ngoài)
- **Cập nhật webhook** trên UnivaPay (ảnh hưởng đến callback payment)

---

### 1.5. LinkPaymentController — unlinkPaymentMethod()

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:447-484`
**Mức độ tin cậy**: **Cao**

#### Logic
1. Kiểm tra `password` bằng `Hash::check()` với mật khẩu user hiện tại
2. Nếu `type == "stripe"`:
   - Xóa: `strip_secret_test_key`, `strip_public_test_key`, `account_test_id`, `strip_secret_live_key`, `strip_public_live_key`, `account_live_id`, `status_strip_bot`
3. Nếu `type != "stripe"` (= univapay):
   - Xóa: `univapay_app_id`, `univapay_app_test_id`, `univapay_app_token`, `univapay_app_token_test`, `univapay_webhook`, `univapay_secret`, `univapay_webhook_id`

> **Ghi chú**: Khi unlink Stripe, các tax rates (`tax_rate_id_*`) **không bị xóa**. Khi unlink UnivaPay, `univapay_secret_test`, `univapay_email`, `univapay_email_test` **không bị xóa**.

---

### 1.6. LinkPaymentController — updateFlagImage(), changeBrandCardunivapay(), updateFlagInstallment()

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:486-509`
**Mức độ tin cậy**: **Cao**

Các method đơn giản, chỉ update 1 field trên `s_strip_bot`:

| Method | Field | Giá trị |
|--------|-------|---------|
| `updateFlagImage()` | `flag_image` | 0 hoặc 1 |
| `changeBrandCardunivapay()` | `flag_brand_card_univapay` | Chuỗi comma-separated: "0,1,2,3,4" |
| `updateFlagInstallment()` | `flag_installment` | 0 hoặc 1 |

---

### 1.7. WebhookUnivapayControler — webhook()

**File**: `app/Http/Controllers/WebhookUnivapayControler.php:11-41`
**Mức độ tin cậy**: **Cao**

#### Logic
1. Nhận request body từ UnivaPay webhook
2. Lấy `event` type và `data.metadata.module`
3. Kiểm tra module nằm trong danh sách cho phép
4. Nếu `event == "charge_finished"` → dispatch `HandleWebhookUnivapay` job vào queue
5. Trả về `{ status: "success" }`

> **Quan trọng**: Endpoint này **không có authentication** — UnivaPay gọi trực tiếp. Không có signature verification.
> **Mức độ tin cậy**: **Cao** (code rõ ràng), nhưng **rủi ro bảo mật** vì thiếu xác thực webhook.

---

## 2. Models Eloquent

### 2.1. StripBot

**File**: `app/StripBot.php`
**Table**: `s_strip_bot`
**Mức độ tin cậy**: **Cao**

```php
class StripBot extends Model
{
    protected $table = 's_strip_bot';
    protected $guarded = [];
    public $timestamps = false;
}
```

- **Không có relationships** khai báo (nhưng logic sử dụng `bot_id` liên kết với `bots` table)
- **Không có timestamps** — không track `created_at`, `updated_at`
- **`$guarded = []`** — cho phép mass assignment toàn bộ columns

#### Columns liên quan đến FA-034

| Column | Type | Mô tả | Nhóm |
|--------|------|-------|------|
| `bot_id` | int | FK → bots.id | Chung |
| `strip_secret_test_key` | varchar(255) | Stripe secret key (test) | Stripe |
| `strip_public_test_key` | varchar(255) | Stripe publishable key (test) | Stripe |
| `account_test_id` | varchar(255) | Stripe account ID (test) | Stripe |
| `strip_secret_live_key` | varchar(255) | Stripe secret key (live) | Stripe |
| `strip_public_live_key` | varchar(255) | Stripe publishable key (live) | Stripe |
| `account_live_id` | varchar(255) | Stripe account ID (live) | Stripe |
| `status_strip_bot` | tinyint | Stripe connection state (0-3) | Stripe |
| `tax_rate_id_percent_8` | varchar(255) | Stripe tax rate ID 8% (live) | Stripe |
| `tax_rate_id_percent_10` | varchar(255) | Stripe tax rate ID 10% (live) | Stripe |
| `tax_rate_id_test_percent_8` | varchar(255) | Stripe tax rate ID 8% (test) | Stripe |
| `tax_rate_id_test_percent_10` | varchar(255) | Stripe tax rate ID 10% (test) | Stripe |
| `univapay_app_id` | varchar(255) | UnivaPay store ID (production) | UnivaPay |
| `univapay_app_test_id` | varchar(255) | UnivaPay store ID (test) | UnivaPay |
| `univapay_app_token` | text | UnivaPay app token (production JWT) | UnivaPay |
| `univapay_app_token_test` | text | UnivaPay app token (test JWT) | UnivaPay |
| `univapay_secret` | varchar(255) | UnivaPay app secret (production) | UnivaPay |
| `univapay_secret_test` | varchar(255) | UnivaPay app secret (test) | UnivaPay |
| `univapay_webhook` | varchar(255) | Webhook URL (thường pre-filled, ít dùng) | UnivaPay |
| `univapay_webhook_id` | varchar(255) | Webhook ID trên UnivaPay | UnivaPay |
| `univapay_email` | varchar(255) | Email tài khoản UnivaPay (production) | UnivaPay |
| `univapay_email_test` | varchar(255) | Email tài khoản UnivaPay (test) | UnivaPay |
| `status_webhook` | tinyint | Trạng thái webhook (0=lỗi, 1=OK) | UnivaPay |
| `flag_image` | tinyint | Flag hiển thị hình ảnh sản phẩm | Cài đặt |
| `flag_installment` | int | Flag cho phép trả góp | Cài đặt |
| `flag_brand_card_univapay` | varchar(255) | Card brands chấp nhận (CSV: "0,1,2,3,4") | Cài đặt |
| `status_connect_univapay` | tinyint | Trạng thái kết nối UnivaPay (default 1) | UnivaPay |

---

### 2.2. Bots (liên quan gián tiếp)

**File**: `app/Bots.php`
**Table**: `bots`
**Mức độ tin cậy**: **Trung bình** (suy luận từ code sử dụng)

Các columns được truy cập trong FA-034:
- `channel_id_line_login` — Channel ID LINE Login
- `channel_secret_line_login` — Channel Secret LINE Login
- `liff_callback_unique` — LIFF callback unique identifier
- `liff_app_id_booking` — LIFF app ID cho booking
- `url_liff_app_callback` — URL LIFF callback hiện tại

---

## 3. Services / Helpers

### 3.1. StripePayment

**File**: `app/Helpers/StripePayment.php`
**Mức độ tin cậy**: **Cao**

Các method được sử dụng trong FA-034:

| Method | Mô tả | Gọi từ |
|--------|-------|--------|
| `getInfoAccount($secretKey, $accountId)` (dòng 232) | Gọi `Stripe API accounts->retrieve()` → trả về account info (email, etc.) | EP-01 (linkPayment) |
| `createTaxRate($secretKey, $param)` (dòng 412) | Gọi `Stripe API taxRates->create()` → tạo tax rate inclusive cho JP | EP-01 (linkPayment) khi status = 2→3 |

---

### 3.2. UnivapayPayment

**File**: `app/Helpers/UnivapayPayment.php`
**Mức độ tin cậy**: **Cao**

Các method được sử dụng trong FA-034:

| Method | API Call | Mô tả | Gọi từ |
|--------|---------|-------|--------|
| `getAccountInfo($secret, $token)` (dòng 1786) | `GET https://api.univapay.com/me` + `GET https://api.univapay.com/stores` | Xác thực credentials, lấy email + store IDs | EP-04 (saveInfoUnivapay) |
| `getWebhook($univapay, $flagEnv)` (dòng 1360) | `GET https://api.univapay.com/stores/{id}/webhooks/{wh_id}` | Lấy thông tin webhook hiện tại | EP-04 (saveInfoUnivapay) |
| `updateWebhook($univapay, $flagEnv)` (dòng 1427) | `PATCH https://api.univapay.com/stores/{id}/webhooks/{wh_id}` | Cập nhật webhook: URL, triggers=["charge_finished"], active=true | EP-04 (saveInfoUnivapay) |
| `getMessageErrorUnivapay($msg, $code)` (dòng 1989) | — | Map error code → message tiếng Nhật (~30 error codes) | EP-04 (saveInfoUnivapay) |

#### UnivaPay Authentication Format
Authorization header: `Bearer {secret}.{token}`

---

### 3.3. Global Helper Functions

**File**: `app/Helpers/functions.php`
**Mức độ tin cậy**: **Cao**

| Function | Dòng | Mô tả |
|----------|------|-------|
| `getBotId()` | 359 | Lấy bot_id từ session hiện tại |
| `getCurrentUser()` | 4532 | Lấy user ID hiện tại |
| `decodeJwtLikeJwtIo($token)` | 11068 | Decode JWT token → lấy payload (dùng kiểm tra domains) |
| `addLogUserAction($action)` | — | Log hành động user |

---

## 4. Form Requests / Validation

**KHÔNG có FormRequest class** cho tính năng này. **Mức độ tin cậy**: **Cao**

### Validation client-side (JavaScript)

**File**: `public/js/link_payment/index.js:138-176`

Sử dụng custom `Validate` class (từ `/js/validate/validate.js`) kiểm tra trước khi gửi AJAX:

```javascript
attributes: {
    univapay_app_id: 'アプリID',
    univapay_app_token: 'アプリトークン',
    univapay_secret: 'アプリシークレット',
    univapay_app_test_id: 'アプリID',
    univapay_app_token_test: 'アプリトークン',
    univapay_secret_test: 'アプリシークレット',
    univapay_webhook: 'webhook',
}
```

> **Ghi chú**: Validation chỉ kiểm tra required (không rỗng). Không có format/length validation.

### Validation server-side (trong controller)

| Kiểm tra | Vị trí | Mô tả |
|---------|--------|-------|
| JWT domain check | `LinkPaymentController.php:216-236` | Decode JWT app token, kiểm tra domain trong `payload.domains` khớp với `URL_OUTSIDE_STEP` |
| UnivaPay API validation | `LinkPaymentController.php:241-258` | Gọi API kiểm tra credentials hợp lệ |
| Webhook ID validation | `LinkPaymentController.php:402-437` | Gọi API kiểm tra webhook ID tồn tại và config đúng |
| Password check (unlink) | `LinkPaymentController.php:451` | `Hash::check()` xác nhận mật khẩu |
| Bot ID check (Stripe step3) | `SalesManagementController.php:539` | So sánh botId request vs session |

---

## 5. Events / Listeners / Queued Jobs

### 5.1. HandleWebhookUnivapay (Queued Job)

**File**: `app/Jobs/HandleWebhookUnivapay.php`
**Mức độ tin cậy**: **Cao**

- Implements `ShouldQueue` — chạy trong background via queue
- Dispatch từ: `WebhookUnivapayControler@webhook` (EP-10)
- Input: `$data` (charge data từ webhook), `$paymentMethod` (= "univapay")

#### Routing theo module

| Module | Service | Method |
|--------|---------|--------|
| `lesson` | `CalendarCourseBookingService` | `handleOrderCallback()` |
| `lesson_change_status` | `CalendarCourseBookingService` | `callbackChangeStatusBooking()` |
| `salon` | `CalendarSalonLineBookingService` | `handleOrderCallback()` |
| `salon_change_status` | `CalendarSalonLineBookingService` | `callbackChangeStatusBooking()` |
| `event-booking` | `EventBookingService` | `handleOrderCallback()` |
| `event_booking_change` | `EventBookingService` | `callbackChangeBooking()` |
| `sales` | `SalesService` | `handleOrderCallback()` |
| `sales_change_card` | `SalesService` | `callbackChangeCard()` |
| `sales_job` | `SalesService` | `callbackJob()` |

> **Liên kết chéo**: Job này xử lý thanh toán cho nhiều tính năng khác (Calendar, Salon, Event Booking, Sales/Products).

---

## 6. Authorization

**Mức độ tin cậy**: **Cao**

### Không có Policies/Gates riêng

- **Không có middleware `admin_access`** trên các routes liên quan
- **Không có permission check** cho Staff role
- Chỉ sử dụng `web` middleware (session-based auth — user phải đăng nhập)
- Tất cả logic dựa trên `getBotId()` — lấy bot_id từ session, đảm bảo user chỉ thao tác trên bot của mình

### Xác nhận mật khẩu khi unlink
- Chỉ EP-05 (`unlinkPaymentMethod`) yêu cầu nhập lại mật khẩu
- Sử dụng `Hash::check()` so sánh với `Auth::user()->password`

---

## 7. Business Rules (tổng hợp)

### BR-01: Stripe Connect — cùng account cho test và production

**File**: `app/Http/Controllers/Basic/SalesManagementController.php:162-179`
**Mức độ tin cậy**: **Cao**

- Sau khi liên kết cả test và production, hệ thống kiểm tra `account_test_id == account_live_id`
- Nếu **khác nhau** → xóa toàn bộ Stripe credentials, hiển thị lỗi: `テストと本番は同じアカウントを利用してください。`
- User phải liên kết lại từ đầu

### BR-02: Stripe — tự động tạo Tax Rates khi hoàn thành

**File**: `app/Http/Controllers/Basic/SalesManagementController.php:187-231`
**Mức độ tin cậy**: **Cao**

- Khi `status_strip_bot` chuyển từ 2 → 3, hệ thống tự động tạo 4 Stripe Tax Rates:
  - 消費税 8% inclusive (test + live)
  - 消費税 10% inclusive (test + live)
- Tax rates dùng cho tính năng sản phẩm đơn lẻ (FA-026) và subscription

### BR-03: UnivaPay — kiểm tra domain trong JWT token

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:215-236, 366-384`
**Mức độ tin cậy**: **Cao**

- App token (JWT) của UnivaPay chứa danh sách domain trong `payload.domains`
- Hệ thống kiểm tra domain của `env('URL_OUTSIDE_STEP')` phải nằm trong danh sách này
- Nếu không khớp → từ chối lưu, hiển thị lỗi chỉ rõ domain đúng
- Kiểm tra riêng cho token production và test

### BR-04: UnivaPay — tự động cập nhật webhook

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:402-437`
**Mức độ tin cậy**: **Cao**

- Khi lưu UnivaPay info với `univapay_webhook_id`:
  1. Gọi API kiểm tra webhook hiện tại
  2. Nếu URL/active/triggers không đúng → tự động PATCH cập nhật:
     - `url` = `env('DOMAIN_WEBHOOK_UNIVAPAY_BILL') + 'mobile/univapay-callback-payment'`
     - `triggers` = `["charge_finished"]`
     - `active` = `true`
  3. Set `status_webhook = 1` (thành công) hoặc `0` (thất bại)

### BR-05: UnivaPay — cập nhật LIFF callback URL

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:264-358`
**Mức độ tin cậy**: **Cao**

- Khi lưu UnivaPay info, nếu bot có LINE Login channel:
  - Lấy LINE Login access token
  - Kiểm tra JWT domain
  - Cập nhật LIFF app callback URL tương ứng
- Mục đích: đảm bảo LIFF app (dùng cho booking flow) trỏ đến đúng domain

### BR-06: Unlink — yêu cầu xác nhận mật khẩu

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:448-456`
**Mức độ tin cậy**: **Cao**

- Ngắt liên kết thanh toán yêu cầu nhập lại mật khẩu đăng nhập
- Hành vi bảo vệ tránh ngắt liên kết nhầm

### BR-07: Card Brand — mặc định Visa + Mastercard

**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:393`
**Mức độ tin cậy**: **Cao**

- Khi tạo mới record StripBot (lần đầu lưu UnivaPay), `flag_brand_card_univapay` = `"0,1"` (Visa + Mastercard)
- Giá trị: 0=Visa, 1=Mastercard, 2=American Express, 3=JCB, 4=Diners Club

### BR-08: Stripe OAuth — redirect flow

**File**: `routes/web.php:3719-3733`
**Mức độ tin cậy**: **Cao**

- Flow: Admin click → redirect to Stripe → user authorize → Stripe redirect back to `/basic/list-items?code=xxx&state=1|2`
- `redirect_uri` = `url('basic/list-items')` — dynamic theo domain hiện tại
- Pre-fill email + country=JP để đơn giản hóa flow

### BR-09: Webhook UnivaPay — chỉ xử lý charge_finished

**File**: `app/Http/Controllers/WebhookUnivapayControler.php:32`
**Mức độ tin cậy**: **Cao**

- Webhook endpoint nhận nhiều loại event từ UnivaPay
- Chỉ xử lý event `charge_finished`
- Dispatch job async, không block response

---

## 8. Environment Variables liên quan

| Variable | Mô tả | Sử dụng tại |
|----------|-------|-------------|
| `ITEM_CLIENT_ID_TEST` | Stripe Connect client ID (test) | EP-02 |
| `ITEM_CLIENT_ID_LIVE` | Stripe Connect client ID (live) | EP-03 |
| `ITEM_STRIP_SECRET_TEST_KEY` | Stripe platform secret key (test) | EP-01 (OAuth token exchange) |
| `ITEM_STRIP_SECRET_LIVE_KEY` | Stripe platform secret key (live) | EP-01 (OAuth token exchange) |
| `DOMAIN_WEBHOOK_UNIVAPAY_BILL` | Domain cho UnivaPay webhook URL | EP-01, EP-04 |
| `URL_OUTSIDE_STEP` | Domain public cho LIFF callback + kiểm tra JWT | EP-04 |
| `DOMAIN_WEB_ADMIN` | Domain admin web (fallback LIFF) | EP-04 |

---

## 9. View / Frontend

### Blade template
**File**: `resources/views/basic/link_payment/index.blade.php`

### JavaScript
**File**: `public/js/link_payment/index.js`

**Vue.js instance** mount trên `#link-payment` với:
- `linkScreen` — điều khiển hiển thị: `''` (trang chính), `'univapay'` (form UnivaPay), `'stripe'` (wizard Stripe)
- `stripeLinked` — `true` khi `flagStripe == 3`
- `univalpayLinked` — `true` khi đã có `univapay_app_id` + `univapay_app_test_id`
- AJAX calls dùng jQuery `$.post()` (không dùng axios)
- Sau khi save UnivaPay thành công → `window.location.reload()` để refresh trang

---

## 10. Phụ thuộc chéo (tính năng khác sử dụng cùng model/endpoint)

| Tính năng | Mã | Sử dụng |
|-----------|----|----|
| Sản phẩm đơn lẻ / Subscription | FA-026 | Đọc `s_strip_bot` để lấy credentials khi xử lý thanh toán |
| Đặt lịch bài học | FA-019 | `HandleWebhookUnivapay` job xử lý `lesson` module |
| Đặt lịch salon | FA-020 | `HandleWebhookUnivapay` job xử lý `salon` module |
| Đặt lịch sự kiện | FA-021 | `HandleWebhookUnivapay` job xử lý `event-booking` module |
| Sales Management V2 | — | `SalesManagementV2Controller` có `iniSettingUnivapay()` và `unlinkPaymentMethod()` riêng (phiên bản đơn giản hơn) |

> **Ghi chú**: `SalesManagementV2Controller` có method `iniSettingUnivapay()` (route `/ajax/sales/ini-setting-univapay`) và `unlinkPaymentMethod()` (route `/ajax/sales/unlink-payment-method`) — đây có thể là phiên bản mới hơn dùng cho tab settings trong Sales Management V2 (route `/basic/sales/index`). Logic đơn giản hơn `LinkPaymentController` (không có domain check, LIFF update, webhook validation).
