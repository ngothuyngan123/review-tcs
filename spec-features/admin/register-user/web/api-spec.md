# [FA-039] Đăng ký tài khoản LME — API Spec

## Tổng quan

- **Mã tính năng**: FA-039
- **Tên**: Đăng ký tài khoản LME (アカウント登録)
- **Base URL**: `https://form.watermeru.com` (production) — theo `config.yaml` (admin portal)
- **Authentication**: **Public** — toàn bộ endpoints đều không yêu cầu session đăng nhập
- **CSRF Protection**: Có — Laravel áp dụng middleware `web` + `VerifyCsrfToken` mặc định; các POST dùng Axios từ blade `auth.register_user_v2` gửi header `X-CSRF-TOKEN` (lấy từ meta tag / `csrf_token()`)
- **Middleware áp dụng**: `NotifyChatworkRequestTimeSlow` (route group bọc ngoài từ `routes/web.php:77`) — chỉ để log chậm, không ảnh hưởng auth
- **Response format**:
  - GET (view endpoints) → trả HTML (Blade view `auth.register_user_v2` / `auth.register_user_success_v2`)
  - POST → JSON (với `validateRegister` và `saveRegisterUserAff` legacy trả redirect — xem từng endpoint)
- **Mức độ tin cậy**: **Cao** (xác nhận từ `src/web/sns-line/app/Http/Controllers/AuthController.php` và `src/web/sns-line/routes/web.php`)

---

## Danh sách endpoints

| Mã | Method | URL | Tên route | Controller@Method | Middleware | Auth |
|----|--------|-----|-----------|-------------------|------------|------|
| EP-01 | GET  | `/register_user` | `register` | `AuthController@registerUser` | `NotifyChatworkRequestTimeSlow` | Public |
| EP-02 | GET  | `/register_user/{user_id}` | `registerAff` | `AuthController@registerUserAff` | như trên | Public |
| EP-03 | GET  | `/register_user_v2` | `register_v2` | `AuthController@registerUserV2` | như trên | Public |
| EP-04 | GET  | `/register_user_v2/{user_id}` | `registerAffV2` | `AuthController@registerUserAffV2` | như trên | Public |
| EP-05 | POST | `/send_mail_register` | `sendMailRegister` | `AuthController@sendMail` | như trên | Public |
| EP-06 | POST | `/type_information` | `typeInformation` | `AuthController@typeInformation` | như trên | Public |
| EP-07 | POST | `/confirm_information` | `confirmInformation` | `AuthController@confirmInformation` | như trên | Public |
| EP-08 | POST | `/register_v2` | `registerUserV2` | `AuthController@validateRegisterV2` | như trên | Public |
| EP-09 | POST | `/register` | `registerUser` | `AuthController@validateRegister` | như trên | Public |
| EP-10 | POST | `/register_user/{user_id}` | `saveRegisterAff` | `AuthController@saveRegisterUserAff` | như trên | Public |
| EP-11 | GET  | `/register/success` | `registerUserSuccess` | `AuthController@registerUserSuccess` | như trên | Public |
| EP-12 | GET  | `/redirect-regist/{token}` | `redirectRegist` | `AuthController@redirectRegist` | như trên | Public |

> Ghi chú: EP-12 (`redirectRegist`) là endpoint user nhận được qua mail xác thực, **không thuộc luồng chính trong user flow 3-step V2 mới** (blade V2 xử lý token qua AJAX), nhưng vẫn được giữ để tương thích — đọc `UserTemporary` theo `code`, render `auth.register_user_v2` kèm `$userTemp`. Xem chi tiết ở mục chi tiết.

---

## Chi tiết từng endpoint

### EP-01: GET `/register_user`

- **Tên route**: `register`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:650-659`
- **Mục đích**: Hiển thị trang đăng ký wizard Step 1 (SCR-REG-02)

#### Request query params

| Tên | Kiểu | Required | Mô tả |
|-----|------|----------|-------|
| `path_intro` | string | không | Tracking nguồn referrer (URL) — truyền trực tiếp qua query string |
| `ucode` | string | không | Hash user ID của affiliator (nếu đi từ link aff) — cookie `u_code` sẽ được set client-side |

Controller cũng đọc header `referer` từ request để truyền vào view (cho JS localStorage tracking).

#### Response

- **Status**: 200
- **Content-Type**: `text/html`
- **Body**: Render `resources/views/auth/register_user_v2.blade.php` với biến:
  - `uCode` = `$request->ucode`
  - `pathIntro` = `$request->path_intro`
  - `referer` = giá trị header `referer` (hoặc `null`)

#### Liên kết UI: SCR-REG-02

---

### EP-02: GET `/register_user/{user_id}`

- **Tên route**: `registerAff`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:1325-1341`
- **Mục đích**: Hiển thị trang đăng ký Step 1 với affiliate tracking (khi user click link aff)

#### Request path params

| Tên | Kiểu | Required | Mô tả |
|-----|------|----------|-------|
| `user_id` | string | có | Hash ID của affiliator (sẽ decode bằng `Hashids::decode` ở step submit cuối) |

#### Request query params

| Tên | Kiểu | Required | Mô tả |
|-----|------|----------|-------|
| `path_intro` | string | không | Tracking URL referrer |
| `is_mobile` | string/int | không | Flag mobile |

#### Response

- **Status**: 200
- **Body**: Render `auth.register_user_v2` với biến `hashUserId`, `uCode` (= hashUserId), `pathIntro`, `isMobile`, `referer`

#### Liên kết UI: SCR-REG-02 (state khởi tạo có uCode)

---

### EP-03: GET `/register_user_v2`

- **Tên route**: `register_v2`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:661-666`
- **Mục đích**: Alias của EP-01 cho Step 1 V2. Giống EP-01 nhưng bỏ phần đọc header `referer`.

#### Request query params

| Tên | Kiểu | Required | Mô tả |
|-----|------|----------|-------|
| `path_intro` | string | không | — |
| `ucode` | string | không | — |

#### Response

- **Status**: 200
- **Body**: Render `auth.register_user_v2` với `uCode`, `pathIntro`

#### Liên kết UI: SCR-REG-02

---

### EP-04: GET `/register_user_v2/{user_id}`

- **Tên route**: `registerAffV2`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:1319-1323`
- **Mục đích**: Alias của EP-02 cho Step 1 V2 với affiliate.

#### Request path params

| Tên | Kiểu | Required | Mô tả |
|-----|------|----------|-------|
| `user_id` | string | có | Hash ID của affiliator |

#### Response

- **Status**: 200
- **Body**: Render `auth.register_user_v2` với `hashUserId = $request->user_id`

#### Liên kết UI: SCR-REG-02

---

### EP-05: POST `/send_mail_register`

- **Tên route**: `sendMailRegister`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:668-741`
- **Mục đích**: Gửi email xác thực cho user tại Step 1

#### Request body (JSON hoặc form-urlencoded)

| Tên | Kiểu | Required | Validation | Error message (JP) | Mô tả |
|-----|------|----------|-----------|---------------------|-------|
| `email` | string | **có** | `required|email|unique:users,email` | `メールを入力してください。` / `メールアドレスに誤りがあります。` / `このメールアドレスはすでにエルメに登録済みです。` | Email user muốn đăng ký |
| `code` (invite code) | string | **điều kiện** | Chỉ khi `env('APP_ENV') !== 'production'` **VÀ** `type != 'resend'` → `required|exists:users,invite_code` | `招待コードを入力してください。` / `招待コードをもらった方にご確認ください。` | Invite code — chỉ bắt buộc ở môi trường DEV/STG |
| `type` | string | không | — | — | `'resend'` → bỏ qua invite-code check; các giá trị khác được xử lý như lần đầu |
| `is_mobile` | int/bool | không | — | — | Flag từ client (hoặc server inject) |
| `pathIntro` | string | không | — | — | Tracking URL referrer |
| `hashUserId` | string | không | — | — | Hash ID của affiliator |

#### Request body mẫu

```json
{
  "email": "user@example.com",
  "code": "ABC123",
  "type": "resend",
  "is_mobile": 0,
  "pathIntro": "https://lme.jp/manual/...",
  "hashUserId": "XYZabc"
}
```

#### Logic nghiệp vụ (tóm tắt)

1. Validate input (`email` + `code` theo env)
2. Sinh `token = Str::random(60)`
3. Tìm `UserTemporary::where('email', ...)->first()`
4. Nếu đã tồn tại: update `code`, `is_mobile`, `created_at = now`, `path_intro` (nếu có) → `save()`. Ngược lại `create()` mới.
5. Tính `diffInMinutes` giữa `updated_at` cũ và now. Nếu `>1 phút` và đã có record cũ → `ActiveAccount::reSendMailRedirectRegist($token, $email, $pathIntro, $hashUserId)` (gửi qua Gmail SMTP fallback).
6. Ngược lại → `MailApiService::sendMailApi()` với template `emails.redirect_regist`, params `{token, pathIntro, hashUserId}`.

#### Response thành công

- **Status**: 200
- **Body**:
```json
{
  "message": "認証メールが送信されました",
  "sendMail": true
}
```

#### Response lỗi

- **Status**: 422 Unprocessable Entity (validation fail)
```json
{
  "errors": [
    {
      "email": ["このメールアドレスはすでにエルメに登録済みです。"]
    }
  ]
}
```

#### Liên kết UI: SCR-REG-02 — action button 「認証メールを送信」

---

### EP-06: POST `/type_information`

- **Tên route**: `typeInformation`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:743-767`
- **Mục đích**: Validate thông tin user ở Step 2a trước khi chuyển sang Step 2b (chỉ validate, **không ghi DB**)

#### Request body

| Tên | Kiểu | Required | Validation | Error message (JP) |
|-----|------|----------|-----------|---------------------|
| `username` | string | **có** | `required|string|max:255` | `名前を入力してください。` / `50文字の名前を入力してください。` |
| `company_name` | string | **có** | `required|string|max:255` | `会社名・屋号を入力してください。` |
| `phone_number` | string | **có** | `required|regex:/^\d{10,11}$/` | `電話番号を入力してください。` / `電話番号は10から11桁の数字でなければなりません。` |
| `email` | string | không | (không validate ở endpoint này) | — | Gửi lại cho response để Vue lưu vào localStorage |

> Ghi chú: rule `string|max:255` nhưng error message dùng "50文字" (không match rule) — UI blade có thể set `maxlength="50"` ở client-side (chưa xác nhận).

#### Request body mẫu

```json
{
  "email": "user@example.com",
  "username": "山田太郎",
  "company_name": "株式会社テスト",
  "phone_number": "09012345678"
}
```

#### Response thành công

- **Status**: 200
- **Body**: echo lại input
```json
{
  "email": "user@example.com",
  "username": "山田太郎",
  "company_name": "株式会社テスト",
  "phone_number": "09012345678"
}
```

#### Response lỗi

- **Status**: 422
```json
{
  "errors": {
    "phone_number": ["電話番号は10から11桁の数字でなければなりません。"]
  }
}
```

#### Liên kết UI: SCR-REG-03 — action button 「次に進む」

---

### EP-07: POST `/confirm_information`

- **Tên route**: `confirmInformation`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:769-789`
- **Mục đích**: Validate password ở Step 2b (chỉ validate, **không ghi DB**)

#### Request body

| Tên | Kiểu | Required | Validation | Error message (JP) |
|-----|------|----------|-----------|---------------------|
| `password` | string | **có** | `required|between:6,12` | `パスワードを入力してください。` / `パスワードは6桁〜12桁の文字を入力してください。。` (2 chấm là từ source) |
| `repeat_password` | string | không | (không validate server-side, chỉ echo lại) | — | |

> Ghi chú: Rule server-side **chỉ kiểm tra độ dài 6-12**; rule "phải có đủ chữ hoa/thường/số/ký tự đặc biệt" là **client-side only** (blade `register_user_v2.blade.php`). Không có rule `Password::mixedCase/numbers/symbols` ở server.

#### Request body mẫu

```json
{
  "password": "Abc123!@",
  "repeat_password": "Abc123!@"
}
```

#### Response thành công

- **Status**: 200 (không có key `status`)
```json
{
  "password": "Abc123!@",
  "repeat_password": "Abc123!@"
}
```

#### Response lỗi

- **Status**: 422
```json
{
  "errors": {
    "password": ["パスワードは6桁〜12桁の文字を入力してください。。"]
  }
}
```

#### Liên kết UI: SCR-REG-04 — action button 「登録内容の確認」

---

### EP-08: POST `/register_v2` (Flow V2 — MAIN endpoint tạo user)

- **Tên route**: `registerUserV2`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:791-1020`
- **Mục đích**: Submit cuối của wizard — tạo user, gán role, gửi mail. Đây là **main write operation** của feature.

#### Request body

| Tên | Kiểu | Required | Validation | Error message (JP) |
|-----|------|----------|-----------|---------------------|
| `token` | string | **có** | Phải khớp với `user_temporary.code` và chưa hết 24h (check thủ công — không qua Validator) | HTTP 410 `{"errors":"token expired"}` |
| `email` | string | **có** | `required|email|unique:users,email` | `メールを入力してください。` / `メールの形で入力してください。` / `このメールアドレスは既に登録されてます。` |
| `username` | string | **có** | `required|max:50` | `名前を入力してください。` / `50文字の名前を入力してください。` |
| `password` | string | **có** | `required|between:6,13` | `パスワードを入力してください。` / `パスワードは6~13文字で設定してください。` |
| `company_name` | string | không | — | — |
| `phone_number` | string | không | — | — |
| `hashUserId` | string | không | — | `Hashids::decode()` — nếu decode OK → coi như có affiliate |
| `pathIntro` | string | không | — | URL tracking |
| `isMobile` | int/bool | không | — | (dùng `userTemp.is_mobile` thay thế nếu có) |

> Ghi chú: `between:6,13` (server) vs client-side check 6-12 — lệch 1 ký tự (bug nhẹ trong source).

#### Request body mẫu

```json
{
  "token": "a1b2c3...60chars",
  "email": "user@example.com",
  "username": "山田太郎",
  "company_name": "株式会社テスト",
  "phone_number": "09012345678",
  "password": "Abc123!@",
  "hashUserId": "XYZabc",
  "pathIntro": "https://lme.jp/manual/",
  "isMobile": 0
}
```

#### Logic nghiệp vụ (tóm tắt)

Xem `logic-spec.md` mục `validateRegisterV2` để có chi tiết đầy đủ. Tóm tắt:

1. Decode `hashUserId` → `$userIdInvite`
2. Query `UserTemporary::where('code', $token)->first()` — nếu không tồn tại → 410
3. Check `User::where('email', $userTemp->email)->where('is_active', 1)->first()` — nếu đã active → 410
4. Check `$userTemp->created_at` + 24h — nếu hết hạn → 410
5. Nếu `$userIdInvite` có → `$admin = userRepository->findById($userIdInvite)`
6. Validate `username/password/email`
7. Gán `user_introduce` (nếu `admin->allow_accept_aff == 1`) hoặc `user_introduce_2`
8. `INSERT INTO users` với role=0, password=bcrypt, admin_id, max_bot, is_active=1, path_intro, is_mobile, ip…
9. Nếu có affiliate → `INSERT INTO payment_detail_aff` (user_id = affiliator, user_bill_id = new user, type_bill = -1)
10. Lặp mảng `roleUserNew` (34 routes) → `AccessFeature::where('route', ...)` → `INSERT INTO role_access` với role_id 1 (luôn), role_id 2 (loại trừ staff-only routes), role_id 3 (chỉ cho chatBasic/index.talk/adminSetting)
11. Nếu có affiliate → update `affiliate_info.count_user_intro++`, gửi mail thông báo tới các `emails_receive_notify` (template `emails.registered_user_aff`)
12. `INSERT INTO user_point_settings` (is_trial=true, m_bot=1, require_paypal=1, expire_date=+30 days end-of-day)
13. Gọi `ActiveAccount::sendMailActiveAccountSuccess` (mail thông báo cho user), `sendMailConfirmUserRegisterToUser` (mail đến admin), `sendMailConfirmUserRegisterToUserMASP` (mail đến MASP)
14. `$this->countPathIntro()` — tăng counter `path_intro_data`
15. Nếu đang login → `Auth::logout()`

#### Response thành công

- **Status**: 200
- **Body**:
```json
{
  "message": "認証メールが送信されました",
  "confirm": false,
  "currentStep": 3
}
```

#### Response lỗi

- **Status**: 410 Gone (token expired / đã active / không tồn tại)
```json
{"errors": "token expired"}
```

- **Status**: 422 Unprocessable Entity (validation fail)
```json
{
  "errors": {
    "email": ["このメールアドレスは既に登録されてます。"]
  }
}
```

- **Status**: 422 (Exception — catch all)
```json
{"errors": "<exception message>"}
```

#### Liên kết UI: SCR-REG-05 — action button 「アカウント登録」

---

### EP-09: POST `/register` (LEGACY flow)

- **Tên route**: `registerUser`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:1049-1229`
- **Mục đích**: Luồng đăng ký cũ — **tạo user inactive + gửi mail activate** (không qua wizard 3-step V2). Nhìn vào blade `auth.register_user_v2` hiện tại thì JS không gọi endpoint này, nhưng route vẫn còn để tương thích ngược.

#### Request body

| Tên | Kiểu | Required | Validation | Error message |
|-----|------|----------|-----------|---------------|
| `username` | string | **có** | `required|max:50` | `名前を入力してください。` / `50文字の名前を入力してください。` |
| `password_regist` | string | **có** | `required|between:6,13` | `パスワードを入力してください。` / `パスワードは6~13文字で設定してください。` |
| `email_regist` | string | **có** | `required|email|unique:users,email` | `メールを入力してください。` / `メールの形で入力してください。` / `このメールアドレスは既に登録されてます。` |
| `invite_code` | string | không | `exists:users,invite_code` (nếu có) | `招待コードをもらった方にご確認ください。` |
| `introduce_u` | string | không | — | Hash ID affiliator |
| `path_intro` | string | không | — | — |
| `_token` | string | (Laravel CSRF) | — | — |

#### Logic nghiệp vụ (tóm tắt)

1. Validate input
2. Nếu có `invite_code` → `userRepository->getAdminByInviteCode($invite_code)` (WHERE `lower(invite_code) = ?`)
3. Decode `introduce_u` → nếu có và chưa set admin → `findById($userIdInvite)`
4. INSERT `users` (is_active=0, token_active_register=random(32), expire_datetime_active_user=now)
5. Nếu có affiliate → INSERT `payment_detail_aff`
6. Gán 34 role_access giống EP-08 (role_id 1/2/3)
7. INSERT `user_point_settings` (trial 30 ngày)
8. Gọi `ActiveAccount::sendMailActiveAccount($token, $email)` gửi link activate, `sendMailConfirmUserRegisterToUser`, `sendMailConfirmUserRegisterToUserMASP`

#### Response

- **Thành công**: Redirect 302 → `route('registerUserSuccess')` tức `/register/success`
- **Validation lỗi**: Redirect back với `->withErrors($validator)` và `withInput`
- **Exception**: Redirect → `route('404')`

#### Liên kết UI: Không dùng trong flow V2 (chỉ còn tương thích ngược)

---

### EP-10: POST `/register_user/{user_id}` (Flow có affiliate — legacy save)

- **Tên route**: `saveRegisterAff`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:1343-1527`
- **Mục đích**: Tương tự EP-09 nhưng `user_id` được lấy từ path param (hash). Flow cũ dành cho link aff dạng `/register_user/{user_id}`.

#### Request path params

| Tên | Kiểu | Required | Mô tả |
|-----|------|----------|-------|
| `user_id` | string | có | Hash ID của affiliator — decode bằng `Hashids::decode` |

#### Request body

| Tên | Kiểu | Required | Validation | Error message |
|-----|------|----------|-----------|---------------|
| `username` | string | **có** | `required|max:50` | `名前を入力してください。` |
| `password_regist` | string | **có** | `required|between:6,13` | `パスワードは6~13文字で設定してください。` |
| `email_regist` | string | **có** | `required|email|unique:users,email` | `メールをを入力してください。` (typo trong source) |
| `path_intro` | string | không | — | — |

#### Logic nghiệp vụ

Giống EP-09 nhưng lấy affiliate từ `user_id` path param thay vì `introduce_u` body param. Tạo inactive user + gửi mail activate.

#### Response

- **Thành công**: Redirect 302 → `route('registerUserSuccess')`
- **Validation lỗi**: Redirect back với withErrors
- **Exception**: Redirect → `route('404')`

---

### EP-11: GET `/register/success`

- **Tên route**: `registerUserSuccess`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:1231-1234`
- **Mục đích**: Trang hoàn thành đăng ký (SCR-REG-06)

#### Response

- **Status**: 200
- **Content-Type**: `text/html`
- **Body**: Render `resources/views/auth/register_user_success_v2.blade.php`

#### Liên kết UI: SCR-REG-06

---

### EP-12: GET `/redirect-regist/{token}`

- **Tên route**: `redirectRegist`
- **Mã nguồn**: `app/Http/Controllers/AuthController.php:1273-1293`
- **Mục đích**: User click link trong email xác thực → backend verify token → render wizard Step 2 với `userTemp` dữ liệu hoặc báo lỗi.

#### Request path params

| Tên | Kiểu | Required | Mô tả |
|-----|------|----------|-------|
| `token` | string | có | Random 60-char token từ `user_temporary.code` |

#### Logic

1. `UserTemporary::where('code', $token)->first()`
2. Nếu không có → view `auth.active_user_error`
3. Nếu `User::where('email', $userTemp->email)->where('is_active', 1)->first()` đã tồn tại → view `auth.active_user_error`
4. Nếu `$userTemp->created_at + 24h < now` → view `auth.active_user_success` với `['active' => false, 'email' => $userTemp->email]`
5. Ngược lại → view `auth.register_user_v2` với `$userTemp`, `$uCode`, `$pathIntro`, `$referer = ''`

#### Response

- **Status**: 200
- **Body**: HTML — 1 trong 3 view nêu trên

#### Liên kết UI: Bridge giữa mail xác thực và SCR-REG-03 (Step 2a)

---

## Middleware áp dụng

Toàn bộ 12 endpoints thuộc route group bọc bởi:

```php
Route::middleware(['NotifyChatworkRequestTimeSlow'])->group(function () { ... });
```

- `NotifyChatworkRequestTimeSlow`: Middleware logging request chậm, gửi thông báo Chatwork. **Không ảnh hưởng auth.**

Ngoài ra, Laravel mặc định áp `web` middleware group (session, CSRF, cookies) — nên các POST cần `_token` CSRF (gửi qua header `X-CSRF-TOKEN` từ Axios trong blade).

**Không có middleware**: `basic_access`, `admin_access`, `check_login`, `check_remember_token`, `is_expire`, `https_protocol` (dù blade có chuyển HTTPS ở production).

---

## Liên kết endpoint ↔ màn hình UI

| Màn hình | Endpoint(s) | Action UI |
|----------|-------------|-----------|
| SCR-REG-01 (Login page) | — (không call — chỉ link đến EP-01) | Click 「新規登録」 |
| SCR-REG-02 (Step 1 — Email) | EP-01 / EP-03 (load view); EP-05 (submit 「認証メールを送信」) | — |
| SCR-REG-02 với affiliate | EP-02 / EP-04 (load view kèm hashUserId) | — |
| (Email → click link) | EP-12 (GET `/redirect-regist/{token}`) | — |
| SCR-REG-03 (Step 2a — Info) | EP-06 (submit 「次に進む」) | — |
| SCR-REG-04 (Step 2b — Password) | EP-07 (submit 「登録内容の確認」) | — |
| SCR-REG-05 (Step 2c — Confirm) | EP-08 (submit 「アカウント登録」) | — |
| SCR-REG-06 (Done) | EP-11 (GET `/register/success`) | — |
| (Legacy) | EP-09, EP-10 (không dùng trong flow V2 hiện tại) | — |

---

## Error codes (tổng hợp)

| HTTP Status | Khi nào | Endpoint |
|------------|---------|----------|
| 200 | Thành công | Tất cả |
| 302 | Redirect (legacy forms) | EP-09, EP-10 |
| 410 Gone | Token `user_temporary.code` không tồn tại / user đã active / token hết 24h | EP-08 |
| 422 Unprocessable Entity | Validation failed | EP-05, EP-06, EP-07, EP-08 |

---

## Phụ thuộc chéo

- **Shared component nghi ngờ**: Step Indicator / Progress Wizard — áp dụng cho toàn bộ màn trong feature (xem `features/shared/pending-refs.md`)
- **Nguồn data**: 
  - Bảng `users` (bảng main)
  - Bảng `user_temporary` (tên singular — giữ nguyên từ `UserTemporary.php:9` `protected $table = "user_temporary"`)
  - Bảng `role_access` (singular — giữ nguyên từ `RoleAccess.php:10` `protected $table = 'role_access'`)
  - Bảng `access_feature` (singular — `AccessFeature.php:10`)
  - Bảng `payment_detail_aff`, `affiliate_info`, `user_point_settings`, `path_intro_data`

---

## Mức độ tin cậy

- Endpoints EP-01 → EP-12: **Cao** (xác nhận từ `AuthController.php` và `routes/web.php`)
- Validation rules: **Cao** (lấy trực tiếp từ Validator trong source)
- Error messages: **Cao** (lấy trực tiếp, chưa translate)
- Mapping endpoint ↔ UI: **Cao** (khớp với blade `register_user_v2.blade.php` và `ui-spec.md`)
