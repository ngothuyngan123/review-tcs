# API Spec — FA-034: Liên kết hệ thống thanh toán「決済システム連携設定」

> **Mã tính năng**: FA-034
> **Portal**: Admin
> **Ngày tạo**: 2026-03-26
> **Nguồn**: Phân tích source code Laravel — routes, controllers, helpers, views

---

## 1. Tổng quan endpoints

| Mã | Method | URI | Controller@Action | Mô tả | Middleware |
|----|--------|-----|-------------------|-------|-----------|
| EP-01 | GET | `/basic/list-items` | `Basic\SalesManagementController@linkPayment` | Trang chính liên kết thanh toán + xử lý Stripe OAuth callback | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-02 | GET | `/sales/stripe/test/connect` | Closure (routes/web.php) | Khởi tạo Stripe OAuth Connect cho môi trường test | web |
| EP-03 | GET | `/sales/stripe/production/connect` | Closure (routes/web.php) | Khởi tạo Stripe OAuth Connect cho môi trường production | web |
| EP-04 | POST | `/ajax/save-info-univapay` | `Basic\LinkPaymentController@saveInfoUnivapay` | Lưu thông tin liên kết UnivaPay (token, secret, webhook ID) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-05 | POST | `/ajax/unlink-payment-v2` | `Basic\LinkPaymentController@unlinkPaymentMethod` | Ngắt liên kết thanh toán (Stripe hoặc UnivaPay) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-06 | POST | `/ajax/update-flag-image-sale` | `Basic\LinkPaymentController@updateFlagImage` | Cập nhật flag hiển thị hình ảnh sản phẩm | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-07 | POST | `/ajax/change-brand-card-univapay` | `Basic\LinkPaymentController@changeBrandCardunivapay` | Cập nhật danh sách card brand được chấp nhận (UnivaPay) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-08 | POST | `/ajax/update-flag-installment` | `Basic\LinkPaymentController@updateFlagInstallment` | Cập nhật flag cho phép trả góp | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-09 | GET | `/basic/list-item/check-step3-stripe` | `Basic\SalesManagementController@checkStep3Stripe` | Xác nhận hoàn thành bước 3 Stripe (set status = 3) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-10 | POST | `/mobile/univapay-callback-payment` | `WebhookUnivapayControler@webhook` | Webhook nhận callback từ UnivaPay khi thanh toán hoàn tất | web, NotifyChatworkRequestTimeSlow |

> **Lưu ý**: EP-02, EP-03 là closure routes (inline function trong `routes/web.php`), không phải controller method.
> EP-10 là webhook endpoint — không được gọi từ UI mà từ hệ thống UnivaPay bên ngoài.

---

## 2. Chi tiết từng endpoint

### EP-01: GET `/basic/list-items` — Trang chính + Stripe OAuth callback

**Controller**: `Basic\SalesManagementController@linkPayment`
**File**: `app/Http/Controllers/Basic/SalesManagementController.php:66`
**Mức độ tin cậy**: **Cao** (đọc trực tiếp source code)

**Chức năng kép**:
1. **Hiển thị trang chính** liên kết thanh toán (view `basic.link_payment.index`)
2. **Xử lý Stripe OAuth callback** — khi Stripe redirect về URL này kèm `code` + `state`

#### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `code` | query | string | Không | Authorization code từ Stripe OAuth (chỉ có khi redirect từ Stripe) |
| `state` | query | int | Không | `1` = test, `2` = production (chỉ có khi redirect từ Stripe) |
| `connect` | query | int | Không | `1` = vừa kết nối test xong, hiển thị màn hình Stripe connect |

#### Xác thực
- Session-based (web middleware) — user phải đã đăng nhập
- Sử dụng `getBotId()` để lấy bot_id từ session hiện tại

#### Response
- **Trường hợp Stripe callback thành công (state=1, test)**: Redirect về `GET /basic/list-items?connect=1`
- **Trường hợp Stripe callback thành công (state=2, production)**: Redirect về `GET /basic/list-items` (không có param connect)
- **Trường hợp bình thường**: Render view `basic.link_payment.index` với data:

```json
{
  "emailStripe": "user@example.com",
  "univapayWebhook": "https://form.watermeru.com/mobile/univapay-callback-payment",
  "emailUnivapay": "merchant@univapay.com",
  "univapayLinked": true,
  "flagStripe": 3,
  "hashBotId": "abc123xyz",
  "flagImage": 0,
  "flagInstallment": 0,
  "univpayBotEdit": { "...toàn bộ record StripBot..." },
  "msgError": "テストと本番は同じアカウントを利用してください。",
  "flag_brand_card_univapay": [0, 1]
}
```

#### Lỗi có thể xảy ra

| Tình huống | Hành vi | Thông báo |
|-----------|---------|----------|
| Stripe OAuth thất bại (ApiErrorException) | Hiển thị trang chính bình thường, không lưu gì | Log error, không hiện lỗi cho user trực tiếp |
| Stripe test & production là khác account | Xóa toàn bộ Stripe credentials, set `status_strip_bot = 0` | Alert: `テストと本番は同じアカウントを利用してください。` |

---

### EP-02: GET `/sales/stripe/test/connect` — Stripe OAuth (test)

**Route type**: Closure (inline function)
**File**: `routes/web.php:3727`
**Mức độ tin cậy**: **Cao**

#### Hành vi
1. Lấy `email` của user hiện tại từ bảng `users`
2. Tạo URL Stripe OAuth: `https://connect.stripe.com/oauth/v2/authorize`
3. Redirect user đến Stripe

#### Query params gửi đến Stripe

| Tên | Giá trị | Mô tả |
|-----|---------|-------|
| `response_type` | `code` | OAuth authorization code flow |
| `client_id` | `env('ITEM_CLIENT_ID_TEST')` | Stripe Connect client ID (test) |
| `state` | `1` | Đánh dấu đây là test environment |
| `scope` | `read_write` | Quyền truy cập Stripe account |
| `stripe_user[email]` | email user | Pre-fill email trên form Stripe |
| `stripe_user[country]` | `JP` | Pre-fill quốc gia = Nhật Bản |
| `redirect_uri` | `{APP_URL}/basic/list-items` | URL callback → EP-01 |

#### Response
- HTTP 302 Redirect đến `https://connect.stripe.com/oauth/v2/authorize?...`

---

### EP-03: GET `/sales/stripe/production/connect` — Stripe OAuth (production)

**Route type**: Closure (inline function)
**File**: `routes/web.php:3719`
**Mức độ tin cậy**: **Cao**

#### Hành vi
Tương tự EP-02, chỉ khác:
- `client_id` = `env('ITEM_CLIENT_ID_LIVE')` (production)
- `state` = `2` (đánh dấu production)

#### Response
- HTTP 302 Redirect đến `https://connect.stripe.com/oauth/v2/authorize?...`

---

### EP-04: POST `/ajax/save-info-univapay` — Lưu thông tin UnivaPay

**Controller**: `Basic\LinkPaymentController@saveInfoUnivapay`
**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:194`
**Mức độ tin cậy**: **Cao**

#### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-----|--------|------|----------|-----------|-------|
| `univapay_app_token` | body | string | Có (client-side) | Validate class client-side | App Token production (JWT) |
| `univapay_secret` | body | string | Có (client-side) | Validate class client-side | App Secret production |
| `univapay_app_token_test` | body | string | Có (client-side) | Validate class client-side | App Token test (JWT) |
| `univapay_secret_test` | body | string | Có (client-side) | Validate class client-side | App Secret test |
| `univapay_webhook` | body | string | Có (client-side) | Validate class client-side | Webhook URL (read-only, pre-filled) |
| `univapay_webhook_id` | body | string | Không | — | Webhook ID tạo trên UnivaPay admin |
| `univapay_app_id` | body | string | Không | — | App ID (sẽ bị ghi đè bởi API response) |
| `univapay_app_test_id` | body | string | Không | — | Test App ID (sẽ bị ghi đè bởi API response) |

> **Lưu ý**: Validation chỉ xảy ra ở client-side (JS `Validate` class). Server-side **không có FormRequest validation**.

#### Request mẫu

```json
{
  "univapay_app_token": "jwt.token.production.here",
  "univapay_secret": "secret-production",
  "univapay_app_token_test": "jwt.token.test.here",
  "univapay_secret_test": "secret-test",
  "univapay_webhook": "https://form.watermeru.com/mobile/univapay-callback-payment",
  "univapay_webhook_id": "webhook-id-from-univapay-admin",
  "univapay_app_id": "",
  "univapay_app_test_id": ""
}
```

#### Response thành công

```json
{
  "status": true,
  "email": "merchant@univapay.com",
  "appId": "store-uuid-from-univapay",
  "message": "保存しました。"
}
```

#### Lỗi có thể xảy ra

| Tình huống | HTTP | Response |
|-----------|------|----------|
| Production token domain không khớp `URL_OUTSIDE_STEP` | 200 | `{"status": false, "message": "本番環境用のドメインは「xxx」のみ指定可能です。正しいドメインを入力してください。"}` |
| Test token domain không khớp | 200 | `{"status": false, "message": "テスト環境用のドメインは「xxx」のみ指定可能です。正しいドメインを入力してください。"}` |
| UnivaPay API trả lỗi (production) | 200 | `{"status": false, "message": "<lỗi từ UnivaPay, đã dịch>"}` |
| UnivaPay API trả lỗi (test) | 200 | `{"status": false, "message": "<lỗi từ UnivaPay, đã dịch>"}` |
| Không có app ID trong response | 200 | `{"status": false, "message": "no app id"}` |
| Webhook ID sai | 200 | `{"status": true, ..., "message": "Webhook IDが間違っています。再度確認してください。 "}` |

---

### EP-05: POST `/ajax/unlink-payment-v2` — Ngắt liên kết

**Controller**: `Basic\LinkPaymentController@unlinkPaymentMethod`
**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:447`
**Mức độ tin cậy**: **Cao**

#### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `type` | body | string | Có | `"stripe"` hoặc `"univapay"` |
| `password` | body | string | Có | Mật khẩu đăng nhập hiện tại để xác nhận |

#### Request mẫu

```json
{
  "type": "stripe",
  "password": "current_login_password"
}
```

#### Response thành công

```json
{
  "status": true
}
```

#### Lỗi

| Tình huống | Response |
|-----------|----------|
| Sai mật khẩu | `{"status": false, "error": "パスワードが間違っています。"}` |

---

### EP-06: POST `/ajax/update-flag-image-sale` — Cập nhật flag hình ảnh

**Controller**: `Basic\LinkPaymentController@updateFlagImage`
**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:486`
**Mức độ tin cậy**: **Cao**

#### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `flag_image` | body | int | Có | Flag hiển thị hình ảnh sản phẩm (0 hoặc 1) |

#### Response

```json
{
  "status": true
}
```

---

### EP-07: POST `/ajax/change-brand-card-univapay` — Cập nhật card brands

**Controller**: `Basic\LinkPaymentController@changeBrandCardunivapay`
**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:492`
**Mức độ tin cậy**: **Cao**

#### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `flag_brand_card_univapay` | body | array[int] | Có | Danh sách mã card brand: 0=Visa, 1=Mastercard, 2=AmEx, 3=JCB, 4=Diners |

#### Request mẫu

```json
{
  "flag_brand_card_univapay": [0, 1, 3]
}
```

#### Response

```json
{
  "status": true
}
```

---

### EP-08: POST `/ajax/update-flag-installment` — Cập nhật flag trả góp

**Controller**: `Basic\LinkPaymentController@updateFlagInstallment`
**File**: `app/Http/Controllers/Basic/LinkPaymentController.php:503`
**Mức độ tin cậy**: **Cao**

#### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `flagInstallment` | body | int | Có | 0 = tắt, 1 = bật trả góp |

#### Response

```json
{
  "status": true
}
```

---

### EP-09: GET `/basic/list-item/check-step3-stripe` — Xác nhận Stripe bước 3

**Controller**: `Basic\SalesManagementController@checkStep3Stripe`
**File**: `app/Http/Controllers/Basic/SalesManagementController.php:533`
**Mức độ tin cậy**: **Cao**

#### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `botIdCurrent` | query | string | Có | Bot ID hiện tại trong trang (kiểm tra chống đổi account giữa chừng) |

#### Response thành công

```json
{
  "success": true
}
```

#### Lỗi

| Tình huống | Response |
|-----------|----------|
| Bot ID không khớp (đã đổi account) | `{"success": false, "msgBot": "別のアカウントに切り替えたので、要求を処理できません。"}` |
| Exception | `{"success": false}` |

---

### EP-10: POST `/mobile/univapay-callback-payment` — Webhook UnivaPay

**Controller**: `WebhookUnivapayControler@webhook`
**File**: `app/Http/Controllers/WebhookUnivapayControler.php:11`
**Mức độ tin cậy**: **Cao**

> **Đây là webhook endpoint** — được UnivaPay gọi khi có sự kiện thanh toán, không phải từ UI.

#### Request body (từ UnivaPay)

```json
{
  "event": "charge_finished",
  "data": {
    "metadata": {
      "module": "sales"
    },
    "...": "...charge data..."
  }
}
```

#### Module hỗ trợ

| Module | Mô tả |
|--------|-------|
| `lesson` | Đặt lịch bài học (Calendar) |
| `lesson_change_status` | Thay đổi trạng thái booking bài học |
| `salon` | Đặt lịch salon |
| `salon_change_status` | Thay đổi trạng thái booking salon |
| `event-booking` | Đặt lịch sự kiện |
| `event_booking_change` | Thay đổi booking sự kiện |
| `sales` | Thanh toán sản phẩm |
| `sales_change_card` | Đổi thẻ thanh toán sản phẩm |
| `sales_job` | Job xử lý thanh toán sản phẩm |

#### Response

```json
{
  "status": "success"
}
```

#### Side effect
- Dispatch job `HandleWebhookUnivapay` vào queue (chỉ khi `event == "charge_finished"` và module nằm trong danh sách hỗ trợ)

---

## 3. Middleware chi tiết

| Middleware | Mô tả | Áp dụng cho |
|-----------|-------|-------------|
| `web` | Session-based authentication, CSRF protection | Tất cả endpoints |
| `NotifyChatworkRequestTimeSlow` | Log request chậm vào Chatwork | Tất cả endpoints |
| `LogRequestMultipart` | Log request multipart | EP-01, EP-04~EP-09 |

> **Không có middleware `admin_access` hay permission check** — tất cả user đã đăng nhập đều có thể truy cập. **Mức độ tin cậy**: **Cao**

---

## 4. Liên kết Endpoint ↔ Màn hình UI

| Endpoint | Màn hình | Hành động |
|----------|---------|----------|
| EP-01 | SCR-PSI-01 | Render trang chính; xử lý Stripe callback |
| EP-02 | SCR-PSI-03 (Bước 2) | Click「テスト決済に利用する アカウントを選択」 |
| EP-03 | SCR-PSI-03 (Bước 3) | Click「本番決済に利用する アカウントを選択」 |
| EP-04 | SCR-PSI-02 | Click「保存」trên form UnivaPay |
| EP-05 | SCR-PSI-01 (sau liên kết) | Click「連携解除」trên card đã liên kết |
| EP-06 | SCR-PSI-01 (sau liên kết UnivaPay) | Toggle flag hiển thị hình ảnh |
| EP-07 | SCR-PSI-01 (sau liên kết UnivaPay) | Thay đổi checkbox card brands |
| EP-08 | SCR-PSI-01 (sau liên kết UnivaPay) | Toggle flag trả góp |
| EP-09 | SCR-PSI-03 (sau bước 2) | Gọi AJAX sau khi production connect thành công |
| EP-10 | — (webhook bên ngoài) | UnivaPay gọi khi có sự kiện charge_finished |

---

## 5. External API calls

| Dịch vụ | Endpoint | Gọi từ | Mục đích |
|---------|----------|--------|---------|
| Stripe OAuth | `https://connect.stripe.com/oauth/v2/authorize` | EP-02, EP-03 | Redirect user để authorize |
| Stripe OAuth Token | `\Stripe\OAuth::token()` | EP-01 (callback) | Đổi authorization code → access token |
| Stripe Account | `\Stripe\StripeClient->accounts->retrieve()` | EP-01 | Lấy email account đã liên kết |
| Stripe Tax Rate | `\Stripe\StripeClient->taxRates->create()` | EP-01 | Tạo tax rate 8% và 10% khi hoàn thành Stripe |
| UnivaPay Account Info | `GET https://api.univapay.com/me` | EP-04 | Xác thực credentials, lấy email |
| UnivaPay Stores | `GET https://api.univapay.com/stores` | EP-04 | Lấy store ID (= `univapay_app_id`) |
| UnivaPay Get Webhook | `GET https://api.univapay.com/stores/{id}/webhooks/{wh_id}` | EP-04 | Kiểm tra webhook configuration |
| UnivaPay Update Webhook | `PATCH https://api.univapay.com/stores/{id}/webhooks/{wh_id}` | EP-04 | Cập nhật webhook URL + trigger |
| LINE Login Token | `POST https://api.line.me/v2/oauth/accessToken` | EP-04 | Lấy access token LINE Login |
| LINE LIFF App | `PUT https://api.line.me/liff/v1/apps/{liff_id}` | EP-04 | Cập nhật LIFF callback URL |
