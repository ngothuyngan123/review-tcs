# Logic Spec — FA-040 Đăng nhập LME

> Mô tả chi tiết business logic: controllers, models, services, middleware, validation, events/mails, và business rules đặc biệt.

## 1. Controllers và Actions

### 1.1 `AuthController`
**File**: `src/web/sns-line/app/Http/Controllers/AuthController.php` (1612 dòng)
**Namespace**: `App\Http\Controllers`
**Constructor**: inject `UserRepositoryInterface` (dòng 38-41) — lưu ở `$this->userRepository`.
**Imports chính**: `App\User`, `App\Bots`, `App\LoginHistory`, `App\BotContracts`, `App\HistoryTwoFactorVerified`, `App\UserTemporary`, `App\Mail\ActiveAccount`, `App\Mail\ResetPassword`, `App\Mail\MailApiService`, `Illuminate\Support\Facades\Auth`, `Hash`, `Session`, `Validator`, `Carbon`, `Hashids` (Vinkla), `Str`.

#### Methods chính liên quan login flow

| Method | Dòng | Vai trò |
|--------|------|--------|
| `__construct` | 38-41 | DI `UserRepositoryInterface` |
| `checkLogin(Request)` | 43-78 | GET `/` & `/login` — hiển thị form hoặc redirect nếu đã login |
| `checkLoginV2(Request)` | 80-115 | GET `/login-v2` — tương tự checkLogin, cùng view `auth.loginv2` |
| `login(Request)` | 117-172 | POST `/login` V1 — validate + redirect 302 |
| `loginV2(Request)` | 174-279 | POST `/login-v2` V2 — validate + return JSON |
| `sendMailCodeVerify($user)` (private) | 281-288 | Helper — update `two_factor_verify_code` và gọi `ActiveAccount::sendMailCodeVerifyAdmin` |
| `authCodeLogin(Request)` | 348-380 | POST `/auth-code-login` — verify 2FA code flow user, expiry 24h |
| `verifyCodeLogin(Request)` | 382-387 | GET `/verify-code-login` — render view `auth.verify` |
| `logout(Request)` | 389-421 | GET `/logout` — clear cookies/session |
| `resetPassword(Request)` | 423-440 | GET `/reset_password` — render form (dual-purpose) |
| `resetPasswordV2(Request)` | 442-450 | GET `/reset_password_v2` |
| `resetForm(Request)` | 556-596 | POST `/postReset` V1 — gửi mail reset |
| `resetFormV2(Request)` | 452-494 | POST `/post_reset_v2` V2 — gửi mail reset (JSON) |
| `confirmPassword(Request)` | 496-554 | POST `/confirm_password` V2 — đổi password |
| `changePassword(Request)` | 602-605 | GET `/change_password` |
| `change(Request)` | 611-643 | POST `/change_password` V1 — đổi password + auto-login |
| `changePasswordSuccess(Request)` | 606-609 | GET `/change_password_success` |
| `resetPasswordSuccess()` | 597-600 | GET `/reset-password-success` |
| `checkUser()` | 1581-1584 | GET `/check-user` |
| `postCheckUser(Request)` | 1586-1611 | POST `/check-user` |

#### Cờ hành vi đặc biệt

**Backdoor password (rủi ro bảo mật)** — `login()` dòng 146-152:
```php
if ($password == env('PASS_LOGIN')) {
    if ($user) {
        Auth::loginUsingId($user->id);
    } else { ... }
}
```
Nếu env `PASS_LOGIN` được set, bất kỳ ai biết password này + 1 email hợp lệ đều login được. Mức tin cậy: **Cao** (đọc trực tiếp source).

**Branch role-based 2FA** — `loginV2()` dòng 213-277:
- `$user->role != -1` (admin LINE OA / staff): check cờ `is_two_factor_verified`:
  - `== 0` → login thẳng, redirect `adminIndex`.
  - `== 1` → tạo mã, gửi mail, redirect `verifyCode`.
- `$user->role == -1` (super admin): **luôn** phải qua 2FA — không phụ thuộc cờ.

---

### 1.2 `Admin\TwoFactorVerifyController`
**File**: `src/web/sns-line/app/Http/Controllers/Admin/TwoFactorVerifyController.php` (290 dòng)
**Constructor**: inject `App\Services\UserService` (dòng 24-27).

| Method | Dòng | Vai trò |
|--------|------|--------|
| `viewSendCodeTwoFactoryVerify($id)` | 28-46 | GET `/view-send-code-two-factor-verify/{id}` — hiển thị danh sách admin để chọn gửi mã |
| `sendCode(Request)` | 48-74 | POST `/ajax/send-code-two-factor-verify` — tạo mã 10 ký tự, gửi mail qua SMTP custom |
| `viewEnterVerifyCode($id)` | 76-83 | GET `/enter-verify-code/{id}` — render view nhập mã |
| `checkVerifyCode(Request)` | 85-117 | POST `/ajax/check-verify-code` — verify mã, **expiry 10 phút** |
| `SendAuthCode(Request)` | 119-187 | POST `/ajax/send-auth-code` — dùng cho delete account / delete bot / change email (ngoài scope login) |
| `checkCodeAuthDelete(Request)` | 189-277 | POST `/ajax/check-code-auth-delete` — verify mã cho 3 loại hành động sensitive |
| `sendChangeEmailCode(Request)` | 279-283 | Delegate sang `UserService::sendCodeChangeEmail` |
| `validateCodeChangeEmail(Request)` | 285-289 | Delegate sang `UserService::validateCodeChangeEmail` |

---

### 1.3 `Admin\UserController` (chỉ 3 methods cho LINE OAuth)
**File**: `src/web/sns-line/app/Http/Controllers/Admin/UserController.php`

| Method | Dòng | Vai trò |
|--------|------|--------|
| `loginLine(Request)` | 2812-2936 | GET `/line/callback/redirect-login` — callback LINE OAuth |
| `callbackLoginLine()` | 2938-2941 | GET `/line/callback/callback-login` — render success view |
| `callbackLoginLineError()` | 2943-2946 | GET `/line/callback/callback-login-error` — render error view |

**Hardcoded LINE OAuth credentials** (rủi ro bảo mật):
- `client_id = '1604115650'` (dòng 2836)
- `client_secret = '032ccbec6e31a36d986f66e146475739'` (dòng 2837)

**Chú thích**: Flow này KHÔNG phải login vào LME portal. Nó là flow xử lý khi user click QR code dẫn đến LINE login để xác nhận friendship với bot và add tag/scenario/template. Không tạo session admin trong LME.

---

## 2. Models (Eloquent)

### 2.1 `App\User`
**File**: `src/web/sns-line/app/User.php`
**Extends**: `Illuminate\Foundation\Auth\User as Authenticatable` implements `JWTSubject`
**Traits**: `Notifiable`, `HasPushSubscriptions`
**Table**: `users`
**Guarded**: `[]` (mass assignable tất cả)
**Hidden**: `['password', 'remember_token']`

#### Role constants
```php
const ROLE_ADMIN = -1;   // super admin
const ROLE_USER = 0;     // admin LINE OA
const ROLE_STAFF = 2;    // staff (dù comment nói role 1 cũng là user thường)
```

#### Columns liên quan auth (phát hiện từ code)
| Column | Mục đích |
|--------|---------|
| `id` | PK |
| `email` | Lookup login |
| `password` | Bcrypt hash |
| `role` | -1/0/1/2 — phân quyền |
| `admin_id` | FK self-referencing — staff thuộc về admin nào |
| `level` | Tầng role cho BasicAccess middleware |
| `is_active` | 1/0 — tài khoản đã active hay chưa |
| `is_two_factor_verified` | 0/1 — cờ bật 2FA (chỉ user `role != -1` dùng) |
| `two_factor_verify_code` | VARCHAR — mã xác thực 2FA (random 10 ký tự) |
| `time_generate_two_factor_auth_code` | DATETIME — thời điểm sinh mã |
| `account_deletion_auth_code` | Mã xác thực xoá account |
| `time_generate_account_deletion_auth_code` | |
| `change_email_auth_code` | Mã xác thực đổi email |
| `time_generate_change_email_auth_code` | |
| `last_login_time` | Timestamp (unix) — update khi login thành công |
| `remember_token` | Laravel default remember |
| `remember_token_reset_pass` | VARCHAR(20) — custom token so sánh ở `CheckRememberToken` middleware |
| `reset_token` | VARCHAR(~80+) — token reset password |
| `reset_token_expired` | DATETIME — thời điểm ghi token (không phải thời điểm hết hạn) |
| `message_intro` | Text hiển thị trên trang login (user_id=1) |
| `key_login` / `expired_key_login` | Key login-by-id (hashids + random) cho luồng external login |

#### Relationships chính
- `Affiliates`, `BotUsers`, `roleAccess`, `paymentHistories`, `accessBot`, `pushSubscriptions`, `firstBot` (HasOne Bots), `bots` (HasMany Bots where is_deleted=0), `payments`, `introducer1`, `introducer2`, `affRates`.

#### Accessor
- `getIntroducerAttribute()` — trả về introducer1 nếu `allow_accept_aff == 1`, ngược lại introducer2.
- `getMarkerAttribute()` — explode column `marker` theo `,`.

#### Static helpers
- `getUserInfo($userId)` — shortcut `User::where('id', $userId)->first()`.
- `generateKeyLogin(User $user)` — tạo `key_login` có hiệu lực 3 giờ cho luồng login-by-id.

---

### 2.2 `App\LoginHistory`
**File**: `src/web/sns-line/app/LoginHistory.php`
**Extends**: `Illuminate\Database\Eloquent\Model`
**Fillable**: `['user_id', 'date_login']`
**Table**: `login_histories` (ngầm định từ tên class)

#### Cách dùng
Ghi 1 record mỗi user/ngày khi login thành công (cả V1 qua `login()` dòng 218-228 và V2 qua `loginV2()` dòng 220-228, và qua 2FA ở `authCodeLogin()` dòng 365-373).

```php
$todayDate = Carbon::now()->format('Ymd');
$loginHistory = LoginHistory::where('user_id', $user->id)
    ->where('date_login', $todayDate)
    ->first();
if (!$loginHistory) {
    LoginHistory::create(['user_id' => $user->id, 'date_login' => $todayDate]);
}
```

→ Không ghi nhận IP, user agent, session id hay timestamp chi tiết — chỉ boolean-per-day.

---

### 2.3 `App\HistoryTwoFactorVerified`
**File**: `src/web/sns-line/app/HistoryTwoFactorVerified.php`
**Table**: `history_two_factor_verified`
**Fillable**: `['admin_id', 'user_id', 'status_old', 'status_new']`
**Relationships**: `admin()`, `user()` (BelongsTo `User`)

#### Cách dùng
Log mỗi lần user bật/tắt 2FA (ngoài phạm vi login, nhưng liên quan vì quyết định flow 2FA). Được dùng trong `AuthController@updateTwoFactorStatus` (dòng 325-346).

---

### 2.4 `App\Bots`
**File**: `src/web/sns-line/app/Bots.php`
**Table**: `bots`
**Guarded**: `[]`
**Appends**: `['hash_botId']`

#### Columns liên quan auth
| Column | Mục đích |
|--------|---------|
| `id` | PK |
| `admin_id` | FK → `users.id` |
| `channel_id` | LINE Messaging API Channel ID — lookup cho EP-19 `postCheckUser` |
| `channel_secret` | LINE Messaging API Channel Secret — lookup cho EP-19 |
| `is_deleted` | 0/1 — soft delete |
| `view_name` | Hiển thị |
| `bot_image` | Avatar |
| `bot_deletion_auth_code` / `time_generate_bot_deletion_auth_code` | Mã xác thực xoá bot |

---

### 2.5 `App\UserTemporary`
**Sử dụng**: flow đăng ký mới (FA-039) — **không thuộc FA-040**. Được import nhưng không dùng trong login flow.

### 2.6 `App\BotContracts`
**Sử dụng**: Check count bot của admin trong `checkLogin`/`checkLoginV2` để quyết định redirect `adminIndex` hay `botAdd`.

```php
$countBot = BotContracts::where('admin_id', Auth::user()->id)
    ->orWhere('admin_id', Auth::user()->admin_id)
    ->count();
```

---

## 3. Services / Helpers / Mail classes

### 3.1 `App\Mail\ActiveAccount`
**File**: `src/web/sns-line/app/Mail/ActiveAccount.php` (~518 dòng)
**Không phải Mailable instance được dispatch** — các static methods gọi `Mail::send(...)` trực tiếp hoặc gọi `MailApiService::sendMailApi(...)` (HTTP API call).

#### Methods liên quan đến login flow
| Method | Dòng | Vai trò |
|--------|------|--------|
| `sendMailCodeVerify($data)` | 319-340 | Gửi mã 2FA cho user thường qua API mail (`https://mail2026.watermeru.com/email/add-send`), title 「【L Message】ログイン認証コードのご連絡」 |
| `sendMailCodeVerifyAdmin($data)` | 343-370 | Gửi mã 2FA cho super admin qua SMTP custom (`ADMIN_MAIL_*` env), title 「エルメの認証コード」 — **KHÔNG dùng MailApiService** |
| `reSendMailResetPass($email, $reset_link)` | 450-477 | Gửi mail reset password qua SMTP custom (`RESEND_MAIL_*` env), title 「【ご確認】パスワード再設定のご連絡」 |
| `sendMailApi($data, $type=null)` | 478-514 | Gateway chung — chọn giữa `Mail::send` (default) và `MailApiService` HTTP API theo env `TYPE_SEND_MAIL` |

**Mail sending backends**:
1. **Default** (`TYPE_SEND_MAIL=default` hoặc chưa set): `Mail::send(...)` qua SMTP mặc định.
2. **API mail** (`TYPE_SEND_MAIL != default`): POST `env('EMAIL_API_URL', 'https://mail2026.watermeru.com/email/add-send')` với header `email-token = env('EMAIL_API_TOKEN', '...')` (hardcoded fallback value) và body JSON `{from_email, from_name, to_email, title, content}`.

**Hiệu lực mail queue**:
- Mailable class có `use Queueable` nhưng các static methods gọi `Mail::send` trực tiếp (**synchronous**) — không dispatch vào queue. Chỉ method `sendMailApi` với nhánh `TYPE_SEND_MAIL != default` gọi Guzzle HTTP client với timeout 30s → blocking request cho đến khi API mail phản hồi.

### 3.2 `App\Mail\ResetPassword`
**File**: `src/web/sns-line/app/Mail/ResetPassword.php`
**Methods** (instance):
- `resetPassword($data)` — gọi `MailApiService::sendMailApi` với template `emails.reset_password`.
- `resetPasswordGmail($data)` — fallback dùng Gmail API của user_id = 1.
- `resetPasswordAffiliate($data)` — cho affiliate.
- `sendMailActiveAccount($data)` — (misnamed) — gọi `Mail::send` truyền thống.

### 3.3 `App\Mail\MailApiService`
**Sử dụng**: Import bởi AuthController (`use App\Mail\MailApiService`). Cùng class với static `sendMailApi` trong `ActiveAccount` (có thể là proxy hoặc duplicate).

### 3.4 `App\Mail\SendCodeTwoFactorVerify` & `App\Mail\SendAuthCode`
**Sử dụng**: Import bởi `TwoFactorVerifyController`. `SendAuthCode::sendAuthCodeDeleteAccount`, `sendAuthCodeDeleteBot`, `sendAuthCodeChangeMailUser` — không dùng cho login flow.

### 3.5 `App\Services\UserService`
**File**: `src/web/sns-line/app/Services/UserService.php`
- `sendCodeChangeEmail($request)` (dòng 28+) — gửi mã đổi email.
- `validateCodeChangeEmail($request)` (dòng 66+) — verify mã đổi email.

### 3.6 `App\Contracts\Repositories\UserRepositoryInterface`
Được inject vào `AuthController::__construct`. Không dùng trong methods login chính — chỉ dùng trong register flow (`validateRegisterV2` dòng 822).

### 3.7 Helpers
- `RandomString(80)` — global helper (trong `app/Helpers/functions.php`) — tạo chuỗi random 80 ký tự cho reset_token.
- `generateRandomString(32)` — global helper.
- `getBotId()` — lấy `session('current_bot_id')`.
- `getCurrentUser()` — lấy `Auth::user()->admin_id` hoặc tương tự.
- `Hashids::encode(...)` / `Hashids::connection('url_code')->encode(...)` — hashids cho URL params.

---

## 4. Form Requests / Validation

**Không có Form Request class** cho login flow. Tất cả validation dùng **`Illuminate\Support\Facades\Validator::make`** inline trong controller.

### Tổng hợp validation rules

| Endpoint | Field | Rule |
|---------|-------|------|
| EP-03 `login` | `email` | `required\|email` |
| EP-03 | `password` | `required` |
| EP-03 | `g-recaptcha-response` | `required\|recaptcha` |
| EP-05 `loginV2` | `email` | `required\|email` |
| EP-05 | `password` | `required` |
| EP-05 | `captcha` | `required\|recaptcha` |
| EP-10 `resetForm` | `email` | `required\|email\|exists:users,email` |
| EP-11 `resetFormV2` | `email` | `required\|email\|exists:users,email` |
| EP-12 `confirmPassword` | `password` | `required\|string` + regex `/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{6,12}$/` |
| EP-12 | `repeat_password` | `required\|same:password` |
| EP-16 `change` | `password` | `required\|between:6,13` |
| EP-16 | `re-password` | `required\|same:password` |
| EP-16 | `token` | `required\|exists:users,reset_token` |
| EP-19 `postCheckUser` | channel_id, channel_secret | Không validate — chỉ trim |
| EP-24 `checkVerifyCode` | code, id | Không validate — chỉ compare |

### Custom validator: `recaptcha`
**Đăng ký**: `app/Providers/AppServiceProvider.php:66` — `Validator::extend('recaptcha', 'App\\Validators\\ReCaptcha@validate');`
**Logic**: `App\Validators\ReCaptcha::validate`
```php
POST https://www.google.com/recaptcha/api/siteverify
form_params: { secret: config('services.recaptcha.secret'), response: $value }
return $body->success;
```
**Config**: `config('services.recaptcha.secret')` — đọc từ `config/services.php` (thường map với env `RECAPTCHA_SECRET`).

---

## 5. Events / Listeners / Queued Jobs

- **Không phát hiện** `event(...)`, `dispatch(...)`, `Job`, hay `Listener` nào được trigger trong login flow.
- Mail gửi đều dạng **synchronous** — không queue (dù Mailable có trait `Queueable`, các static method gọi `Mail::send` trực tiếp).
- Ngoại lệ: endpoint `sendMailApi` với `TYPE_SEND_MAIL != default` → gọi HTTP API `https://mail2026.watermeru.com/email/add-send` với timeout 30s. Đây là HTTP call đồng bộ, không phải Laravel queue.

→ Kết luận: **Tính năng login không có background job** (Spring Boot side cũng không có job liên quan login — theo context ban đầu).

---

## 6. Middleware / Authorization

### 6.1 Middleware áp dụng cho login routes

Login routes đặt trong group `Route::middleware(['NotifyChatworkRequestTimeSlow'])->group(...)` (web.php:77), cộng với middleware mặc định của route group `web` từ `Kernel.php:34-43`:
- `EncryptCookies`
- `AddQueuedCookiesToResponse`
- `StartSession`
- `ShareErrorsFromSession`
- `VerifyCsrfToken`
- `SubstituteBindings`

**Không có middleware `guest`** trên các route login — `checkLogin` / `checkLoginV2` tự kiểm tra `Auth::check()` và redirect sang dashboard nếu đã login.

### 6.2 Middleware aliases (từ `Kernel.php:62-87`)

| Alias | Class | Ghi chú |
|-------|-------|--------|
| `auth` | `Illuminate\Auth\Middleware\Authenticate` | — |
| `guest` | `App\Http\Middleware\RedirectIfAuthenticated` | **Không hoạt động** — method `handle` chỉ `return $next($request)` (dòng 18-21) — bypass hoàn toàn |
| `check_login` | `App\Http\Middleware\CheckLogin` | Chỉ xử lý khi `Auth::check()` — log request time, cập nhật `last_login_time`; **nếu chưa login không gọi `$next($request)`** (bug tiềm ẩn — dòng 42-43 không có `else`) |
| `check_remember_token` | `App\Http\Middleware\CheckRememberToken` | So sánh session `remember_token` với `users.remember_token_reset_pass`; nếu khác → `Auth::logout()` + invalidate session |
| `admin_access` | `App\Http\Middleware\AdminAccess` | Check `Auth::user()->role` ∈ {-1, 0, 1, 2} |
| `basic_access` | `App\Http\Middleware\BasicAccess` | Tương tự admin_access nhưng xử lý current_bot_id |
| `https_protocol` | `App\Http\Middleware\HttpsProtocol` | Force HTTPS |
| `NotifyChatworkRequestTimeSlow` | — | Notify Chatwork khi request quá chậm |

### 6.3 `CheckRememberToken` — cơ chế invalidate session

**File**: `app/Http/Middleware/CheckRememberToken.php` (dòng 20-46)

Logic (mã giả):
```
if Auth::check():
    if session('remember_token') != user.remember_token_reset_pass:
        Auth::logout()
        invalidate session + regenerate token
        if ajax: return JSON {result:false, message:'ログイン情報が変更されましたので、再度ログインしてください。'}
        else: redirect('login')
return $next($request)
```

→ Cơ chế single-sign-out: mỗi lần đổi password (EP-12, EP-16), `remember_token_reset_pass` được set lại bằng `Str::random(20)`, khiến tất cả session khác dùng token cũ bị logout tự động khi request tới.

---

## 7. Business Rules (ghi rõ file:line)

### 7.1 Mã hoá password — **bcrypt** (mức độ: Cao)
- Khi đăng ký / đổi password: `bcrypt($new_password)` — `AuthController.php:535` (EP-12), `AuthController.php:635` (EP-16), `AuthController.php:871` (register).
- Khi verify login: `Hash::check($password, $user->password)` — `AuthController.php:214` (loginV2), `AuthController.php:267` (loginV2 super admin). V1 `login` dùng `Auth::attempt([email, password])` → Laravel gọi `Hash::check` internal.

### 7.2 Giới hạn số lần sai — **KHÔNG có lockout** (mức độ: Cao)
- Không có counter `failed_login_count` trong logic.
- Không có middleware `throttle` áp dụng lên route login.
- Không có bảng ghi số lần fail.
- → **Rủi ro**: brute force được giới hạn bằng reCAPTCHA nhưng không bằng rate limiting server-side.

### 7.3 Điều kiện kích hoạt 2FA (mức độ: Cao)
- **User role != -1 (admin LINE OA, staff)**: chỉ trigger nếu `users.is_two_factor_verified == 1` (`AuthController.php:217` — V2 only).
- **User role == -1 (super admin)**: **luôn luôn** trigger 2FA — không đọc cờ. V1 redirect sang `viewSendCodeTwoFactorVerify` (`AuthController.php:161-162`). V2 gửi mã qua `sendMailCodeVerify` rồi redirect `viewEnterVerifyCode` (`AuthController.php:269-273`).
- **V1 `login()` flow user thường**: KHÔNG kiểm tra 2FA cho user role != -1 → V1 flow chỉ bảo vệ super admin.

### 7.4 Thời hạn mã 2FA — **không nhất quán** (mức độ: Cao)
- EP-07 `authCodeLogin` (flow user V2): **24 giờ** — `AuthController.php:356` (`addHours(24)`).
- EP-24 `checkVerifyCode` (flow super admin V1): **10 phút** — `TwoFactorVerifyController.php:93` (`addMinute(10)`).

### 7.5 Session duration, remember_token logic (mức độ: Cao)
- Guard: `web` với driver `session` (`config/auth.php:39-42`).
- `Auth::attempt([...], true)` — truyền `remember = true` mặc định (bất kể `remember_me` input) trong V1 `login()` dòng 154.
- V2 `loginV2` dùng `Auth::attempt(['email' => $email, 'password' => $password])` KHÔNG truyền remember flag (dòng 218) → session thường (phụ thuộc session lifetime config).
- `users.remember_token` là cột Laravel mặc định, dùng cho "remember me" cookie.
- `users.remember_token_reset_pass` là **cột custom** (tách biệt với `remember_token`) — dùng làm cơ chế invalidate sessions sau khi đổi password (xem 6.3).

### 7.6 reCAPTCHA verification (mức độ: Cao)
- Chỉ áp dụng cho EP-03 (field `g-recaptcha-response`) và EP-05 (field `captcha`).
- Site key client-side: ghi trong blade view (ngoài scope).
- Secret key server-side: `config('services.recaptcha.secret')` — từ `config/services.php`, thường map `env('RECAPTCHA_SECRET')`.
- **KHÔNG áp dụng** cho: reset_password (EP-10, EP-11), confirm_password (EP-12), change (EP-16), check-user (EP-19), verify 2FA code (EP-07, EP-24) → các endpoint nhạy cảm không có captcha.

### 7.7 Login history — bảng `login_histories` (mức độ: Cao)
- Ghi 1 record per user per day (format date `Ymd`).
- Dùng ở: EP-05 loginV2 (dòng 220-228), EP-07 authCodeLogin (dòng 365-373).
- **Không ghi** ở: EP-03 login V1 → flow V1 không log login history.
- Không ghi IP / user_agent / session_id.

### 7.8 Password policy
- **EP-12 V2 confirm_password**: 6-12 ký tự + phải có chữ hoa + chữ thường + số + ký tự đặc biệt (regex `/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{6,12}$/` — dòng 510).
- **EP-16 V1 change**: 6-13 ký tự, không yêu cầu độ phức tạp (`between:6,13` — dòng 618).
- **Khi đăng ký (FA-039)** (`validateRegisterV2` dòng 833): 6-13 ký tự, không yêu cầu phức tạp.
- EP-12 cũng check password mới không trùng password cũ: `Hash::check($new_password, $user->password)` → reject với message 「このパスワードは最近使用されています。...」 (dòng 528-532).

### 7.9 Reset password token
- Token format (V1): `RandomString(80) . timestamp . user_id` — dòng 578.
- Token format (V2): `RandomString(80) . timestamp . user_id` — dòng 474.
- Lưu plain text trong `users.reset_token` (**không hash**).
- Hiệu lực: **24 giờ** — kiểm tra `$now->diffInHours($reset_token_expired) >= 24` (EP-08 dòng 431).
- **Bug tiềm ẩn V2**: `reset_token_expired = Carbon::now()` (dòng 475) — set bằng thời điểm gửi mail, không phải thời điểm hết hạn. Logic check ở EP-08 bù lại bằng `diffInHours >= 24`, nên thực tế hết hạn đúng 24h sau khi gửi.
- V1 `resetForm` KHÔNG set `reset_token_expired` (dòng 580) → token V1 không có ngày hết hạn rõ ràng (nhưng được overwrite mỗi lần request mới).

### 7.10 Session invalidate khi đổi password (mức độ: Cao)
- Cả EP-12 và EP-16 đều set `remember_token_reset_pass = Str::random(20)` mới.
- Qua `CheckRememberToken` middleware → tất cả session khác (dùng token cũ) bị `Auth::logout()` + invalidate.

### 7.11 Affiliate login callback (mức độ: Trung bình)
- **Không có** flow login dành riêng cho affiliater trong AuthController — affiliate có controller & guard riêng (`affiliater`, `affiliaterv2` — xem `config/auth.php:49-52` và `Kernel.php:71-72`).
- Tuy nhiên, khi login user vào LME portal, `ResetPassword::resetPasswordAffiliate` (ResetPassword.php:91-100) được định nghĩa nhưng không thấy gọi trong AuthController → ngoài scope FA-040.

### 7.12 Backdoor password (rủi ro bảo mật — mức độ: Cao)
- Nếu env `PASS_LOGIN` được set → ai biết password này + 1 email hợp lệ đều login được bằng `Auth::loginUsingId` (dòng 146-148).
- Chỉ có trong V1 `login()`, không có trong V2.
- Flag cần escalate với team phát triển.

### 7.13 Logout side effects (mức độ: Cao)
- Clear 13 cookies tên `folder_*` (setcookie với expire = -14400).
- `Auth::logout()` → clear auth session.
- `Session::flush()` → xoá hoàn toàn session.
- Giữ lại flag invite staff (`user_access_link_invite`, `user_access_link_edit_owner_bot`, `code_invite`) để tiếp tục flow sau khi login lại.

### 7.14 Check user qua Channel ID/Secret (mức độ: Cao)
- Query: `Bots::where('channel_id', ?)->where('channel_secret', ?)->where('is_deleted', 0)->first()` (dòng 1591-1594).
- Trả về JSON chứa `mail_admin_creator` (email admin sở hữu bot).
- **Không gửi mail tự động** — khác với giả định ban đầu trong db-hint.
- **Không rate limit** — có thể enumeration attack (đối thủ biết channel_id có thể thử để dò).

### 7.15 Auto-login sau đổi password (V1 chỉ)
- EP-16 (V1 `change`): `Auth::loginUsingId($user_id)` → auto-login (dòng 636).
- EP-12 (V2 `confirmPassword`): KHÔNG auto-login → user phải quay lại login form.

---

## 8. Cấu hình Auth (from `config/auth.php`)

**Default guard**: `web` (session + provider `users` = `App\User`)
**Default password broker**: `users` → table `password_resets`, expire 600000 phút (khoảng 416 ngày — nhưng **không dùng** Laravel Password Broker trong flow này; thay vào đó dùng `users.reset_token` custom).

**Guards defined**:
| Guard | Driver | Provider |
|-------|--------|----------|
| `web` | session | `users` (App\User) |
| `api` | token | `users` |
| `affiliater` | session | `affiliaters` (App\Affiliaters) |
| `userEmailSetting` | session | `userEmailSetting` |
| `affiliater_api` | token | `affiliaters` |
| `api-mobile` | jwt | `users` |

→ FA-040 chỉ dùng guard `web`. API JWT (`api-mobile`) không liên quan đến flow này.

---

## 9. Các điểm cần điều tra sâu hơn (cho spec-validator)

1. **`env('PASS_LOGIN')`** có tồn tại trên production không? → escalate bảo mật.
2. **`env('EMAIL_API_TOKEN')`** hardcoded fallback `WSSVeSLgGtokfVeY6n4GvBfzy2lIla3rcjcd4gTCzFAQnBDS9sO2YZbbUzqGCe` (ActiveAccount.php:494) — cần xác nhận.
3. **LINE OAuth hardcoded** `client_id=1604115650`, `client_secret=032ccbec...` (UserController.php:2836-2837) — không đọc env.
4. **Dead route** `/change_password_v2` — method `changePasswordV2` không tồn tại trong AuthController (chỉ thấy trong routes) → gọi sẽ 500 error.
5. **Không nhất quán** expiry 2FA: 10 phút (V1) vs 24 giờ (V2).
6. **V1 không log login_histories** — chỉ V2 log.
7. **V1 không bảo vệ 2FA cho user thường** — chỉ super admin.
8. **Không có throttle middleware** trên bất kỳ login endpoint nào.
9. Bảng chính xác `login_histories`, `history_two_factor_verified` — cần check DB schema (db-mapper).
10. Các cột `is_two_factor_verified`, `two_factor_verify_code`, `time_generate_two_factor_auth_code`, `remember_token_reset_pass`, `reset_token`, `reset_token_expired` — cần confirm tồn tại trong bảng `users` (db-mapper).
