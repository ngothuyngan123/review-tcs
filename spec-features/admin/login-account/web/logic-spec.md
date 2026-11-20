# Logic Spec — FA-040 Đăng nhập LME

> Ngày spec: 2026-11-20 · Branch `release_step_20261106` (Laravel `^13.0`, PHP `^8.3`).
> Business logic: controllers, models, services, middleware, validation, mail, business rules, cảnh báo bảo mật.

## Lịch sử cập nhật

| Ngày | Nội dung |
|------|----------|
| 2026-11-20 | Re-spec theo branch `release_step_20261106`. **Thay đổi do branch (diff `release_step_20260930_v2..release_step_20261106`)**: (1) Laravel 5.5 → 13: `Kernel::$routeMiddleware` → `$middlewareAliases`, `CheckForMaintenanceMode` → `PreventRequestsDuringMaintenance`, CSRF kế thừa `PreventRequestForgery` + `hasValidOrigin()=false`, `TrustProxies` dùng lớp của framework (thêm IP proxy `142.91.106.63`), thêm alias `throttle_json` (`ThrottleRequestsJson`), bỏ alias `check_config_user`; `config/session.php` thêm `'serialization' => 'php'`; mail chuyển từ SwiftMailer sang `App\Mail\SmtpMailer` (Symfony Mailer). (2) `AuthController`: `email` → `email:filter`; `(int) diffInHours(..., true)` cho hạn token; `catch (\Throwable)` + `reportCaughtError()`. (3) `TwoFactorVerifyController`: `addMinutes(10)`, `catch (\Throwable)` + `reportCaughtError()`. (4) Model `User`, `LoginHistory`, `OAuthRefreshToken`, `StaffBotLogin`, `AdminLoginHistory`, `AdminLoginFavorite` thêm trait `LegacyDateSerialization` (JSON ngày giờ giữ dạng `Y-m-d H:i:s`); `User` thêm `HasFactory`, `Affiliates()` ném `\Error`. (5) Xoá scaffold `app/Http/Controllers/Auth/{Login,Register,ForgotPassword,ResetPassword}Controller.php` (không có route trỏ tới — không ảnh hưởng luồng). **Sửa sai so với spec cũ** (spec cũ đọc code cũ hơn): xem bảng §10. Bổ sung 2 cảnh báo bảo mật mới (S-02, S-03). |
| (bản trước) | Bản đầu tiên. |

---

## 1. Controllers và Actions

### 1.1 `AuthController`
**File**: `src/web/sns-line/app/Http/Controllers/AuthController.php` (1714 dòng) · Namespace `App\Http\Controllers`
**Constructor**: inject `UserRepositoryInterface` (dòng 41-44; chỉ dùng cho luồng đăng ký).
**Method `logout`** inject thêm `App\Services\Tutorial\TutorialInitDataCleanupService`.
**Imports chính** (dòng 5-35): `User`, `Bots`, `BotContracts`, `LoginHistory`, `OAuthRefreshToken`, `HistoryTwoFactorVerified`, `UserTemporary`, `Mail\ActiveAccount`, `Mail\ResetPassword`, `Mail\MailApiService`, `Auth`, `Hash`, `Session`, `Validator`, `Carbon`, `Hashids`, `Str`.

| Method | Dòng | Vai trò |
|--------|------|--------|
| `checkLogin` | 46-84 | GET `/`, `/login` — render `auth.auth-v3.login-v3` hoặc redirect nếu đã đăng nhập |
| `checkLoginV2` | 86-114 | GET `/login-v2` — cùng view, logic redirect cũ (`bot_contracts`) |
| `login` | 116-171 | POST `/login` V1 (legacy, còn backdoor) |
| `loginV2` | 173-276 | POST `/login-v2` — luồng chính (JSON) |
| `sendMailCodeVerify` (private) | 278-285 | Tạo mã 2FA cho super admin, gửi qua SMTP admin |
| `settingTwoFactor` / `getAllHistories` / `updateTwoFactorStatus` | 287-343 | Cài đặt bật/tắt 2FA (trong portal — ngoài phạm vi màn đăng nhập) |
| `authCodeLogin` | 345-379 | POST `/auth-code-login` — xác minh mã 2FA (24h) |
| `verifyCodeLogin` | 381-386 | GET `/verify-code-login` (view legacy `auth.verify`) |
| `logout` | 388-430 | GET `/logout` |
| `resetPassword` | 432-449 | GET `/reset_password` (legacy, dual-purpose) |
| `resetPasswordV2` | 451-459 | GET `/reset_password_v2` (không kiểm tra hạn) |
| `resetPasswordV3` | 461-477 | GET `/reset-password` (V3) |
| `resetFormV2` | 479-523 | POST `/post_reset_v2` |
| `confirmPassword` | 525-604 | POST `/confirm_password` |
| `resetForm` | 606-647 | POST `/postReset` (V1) |
| `resetPasswordSuccess` / `changePassword` / `changePasswordSuccess` | 648-660 | View tĩnh |
| `change` | 662-695 | POST `/change_password` (V1, auto-login) |
| `accountNotActive` | 1338-1342 | GET `/account/resend-email/{email}` |
| `checkUser` / `postCheckUser` | 1683-1713 | `/check-user` |

### 1.2 `Admin\TwoFactorVerifyController`
**File**: `app/Http/Controllers/Admin/TwoFactorVerifyController.php` (291 dòng) · inject `App\Services\UserService` (dòng 24).

| Method | Dòng | Vai trò |
|--------|------|--------|
| `viewSendCodeTwoFactoryVerify($id)` | 28-46 | Trang chọn email nhận mã (danh sách `config('sns-line.list_mail')` lọc theo `APP_ENV`) |
| `sendCode` | 48-74 | Tạo mã 10 ký tự cho `users.id = input id`, gửi tới `input email` |
| `viewEnterVerifyCode($id)` | 76-83 | Trang nhập mã |
| `checkVerifyCode` | 85-117 | Xác minh mã (10 phút) → `Auth::loginUsingId` |
| `SendAuthCode` / `checkCodeAuthDelete` / `sendChangeEmailCode` / `validateCodeChangeEmail` | 119-290 | Mã xác thực cho xoá tài khoản/bot, đổi email (ngoài phạm vi); `checkCodeAuthDelete` nay `catch (\Throwable)` + `reportCaughtError` (dòng ~273) |

### 1.3 `Admin\UserController` (LINE OAuth QR — ngoài luồng đăng nhập portal)
`loginLine` dòng 2903-3028 (hardcode `client_id`/`client_secret` dòng 2928-2929), `callbackLoginLine` dòng 3030, `callbackLoginLineError` dòng 3035. Không tạo session LME.

### 1.4 Luồng liên quan khác (ngoài phạm vi FA-040, ghi để tham chiếu)
- `Auth\McpAuthController` (`app/Http/Controllers/Auth/McpAuthController.php`, routes `web.php:4293-4299`, `api.php:437-439`): đăng nhập OAuth cho MCP client, dùng chung bảng `users` + `Hash::check`, có `captcha` `recaptcha`, validate `email:filter`; `createToken`/`refreshToken` trả `invalid_grant` 400 và revoke refresh token khi user không hợp lệ/bị xoá. `confirmPassword` của FA-040 revoke `oauth_refresh_tokens` để vô hiệu token MCP sau khi đổi mật khẩu.
- `AdminLoginHistory` / `AdminLoginFavorite` (`app/Models/`) dùng cho chức năng System Admin "đăng nhập vào tài khoản user" (`UserController.php:10371-10421`) — không thuộc FA-040.
- `StaffBotLogin` (`staff_bot_login`) — dùng trong `ConnectionRateService`, không ghi trong luồng đăng nhập.

---

## 2. Models (Eloquent)

### 2.1 `App\User` — `app/User.php`
- `extends Illuminate\Foundation\Auth\User` implements `JWTSubject`; traits **`LegacyDateSerialization`, `HasFactory`** (mới), `Notifiable`, `HasPushSubscriptions`.
- Table `users`; `$guarded = []`; `$hidden = ['password', 'remember_token']` (dòng 34-36) → khi `json_encode($user)` **mọi cột khác đều lộ** (xem S-03).
- Hằng: `ROLE_ADMIN = -1`, `ROLE_USER = 0`, `ROLE_STAFF = 2` (dòng 38-40).
- `Affiliates()` nay `throw new \Error('Class App\Affiliates not found')` (model không tồn tại — giữ hành vi PHP 7.2; không nơi nào gọi).
- Cột dùng trong luồng: `id, admin_id, email, password, role, is_active, is_two_factor_verified, two_factor_verify_code, time_generate_two_factor_auth_code, last_login_time, remember_token, remember_token_reset_pass, reset_token, reset_token_expired, message_intro`.

### 2.2 `App\LoginHistory` — `app/LoginHistory.php`
`$fillable = ['user_id', 'date_login']`; trait `LegacyDateSerialization` (mới). Table `login_histories`. Ghi 1 dòng / user / ngày (`date_login` = `Ymd`) tại `loginV2` (dòng 218-227) và `authCodeLogin` (dòng 361-370). **Không** ghi ở `login` V1 và `checkVerifyCode` (EP-24).

### 2.3 `App\OAuthRefreshToken` — `app/OAuthRefreshToken.php`
Table `oauth_refresh_tokens`, PK `token` (string, không tự tăng); trait `LegacyDateSerialization` (mới). FA-040 chỉ UPDATE `is_revoked = true` trong `confirmPassword` (dòng 583-585).

### 2.4 `App\Bots`
Dùng trong `postCheckUser`: `where channel_id, channel_secret, is_deleted = 0`. `getListBotIdStaffManagement()` (helper `functions.php:5045`) đọc `bots` (`admin_id`, `is_deleted = 0`) + `user_staff_bots.user_invite_id` để quyết định redirect trong `checkLogin`.

### 2.5 `App\BotContracts`
Table `bot_contracts`. Đếm theo `admin_id` trong `login` V1 và `checkLoginV2` để chọn `botAdd` / `adminIndex`.

### 2.6 `App\HistoryTwoFactorVerified`
Table `history_two_factor_verified` — ghi khi bật/tắt 2FA (`updateTwoFactorStatus`, dòng 322-343). Bật/tắt áp cho **cả admin và toàn bộ staff** cùng `admin_id` (dòng 339-340).

### 2.7 `App\Models\BotsTutorialCleanupQueue`
Table `bots_tutorial_cleanup_queue` (chưa có trong DB dump) — `logout` enqueue reason `logout` qua `TutorialInitDataCleanupService::enqueueCleanupOnLogout` (`app/Services/Tutorial/TutorialInitDataCleanupService.php:144`). Ref `ts_logout_{botId}_{timestamp}`, unique index chặn trùng.

---

## 3. Services / Mail

### 3.1 `App\Mail\ActiveAccount` (static methods)
| Method | Dòng | Vai trò |
|--------|------|--------|
| `sendMailCodeVerify($data)` | 319 | Mã 2FA user thường — qua API mail |
| `sendMailCodeVerifyAdmin($data)` | 343 | Mã 2FA super admin — `SmtpMailer::admin()` (env `ADMIN_MAIL_*`), template `emails.send-code-two-layer-admin` (**đổi** từ SwiftMailer tự dựng transport) |
| `reSendMailResetPass($email, $link)` | 437 | Mail đặt lại khi đã có token cũ — `SmtpMailer::resend()` (env `RESEND_MAIL_*`) |
| `sendMailApi($data, $type)` | 455 | Gateway: `TYPE_SEND_MAIL=default` → `Mail::html(...)`; ngược lại POST `env('EMAIL_API_URL','https://mail2026.watermeru.com/email/add-send')` header `email-token` = `env('EMAIL_API_TOKEN', '<fallback hardcode>')` (dòng 468-470) |

### 3.2 `App\Mail\MailApiService`
Gửi SMTP mặc định qua `SmtpMailer::defaultWithTimeout(2)` (timeout 2s/thao tác, auth LOGIN) — thay cho `Swift_SmtpTransport + SmtpTimeoutPlugin`; fallback API mail (dòng 101-103, cùng token hardcode). Đồng bộ — không queue.

### 3.3 `App\Mail\ResetPassword`
`resetPassword($data)` gọi API mail với template `emails.reset_password`. `build()` nay ném `InvalidArgumentException` (class chỉ dùng hàm tĩnh/instance helper, không gửi như Mailable).

### 3.4 `App\Mail\SmtpMailer` (mới — `app/Mail/SmtpMailer.php`)
Factory mailer riêng (`admin()`, `resend()`, `defaultWithTimeout()`) dựng bằng `Mail::build` — không thay mailer mặc định của tiến trình (task #43857).

### 3.5 Helpers (`app/Helpers/functions.php`)
- `reportCaughtError(\Throwable $e)` (dòng 9539-9555, **mới**): nếu `$e instanceof \Exception` → **bỏ qua** (giữ hành vi cũ: exception đã log); chỉ `report()` các `\Error` (TypeError, ValueError… — PHP 8) và khử trùng lặp 1 giờ qua `Cache::add('report_caught_error:'.md5(class|file:line))`. → Trong luồng FA-040, đổi `catch (\Exception)` → `catch (\Throwable)` khiến lỗi PHP 8 (`\Error`) cũng bị bắt và trả 404/500 thay vì crash, đồng thời được báo về Handler (Chatwork). **Cao**.
- `RandomString(80)`, `getBotId()`, `getAdminId()`, `getCurrentUser()`, `getListBotIdStaffManagement()` (dòng 5045), `logInfo()` (dòng 12316).

---

## 4. Validation (inline `Validator::make`, không có FormRequest)

| Endpoint | Field | Rule |
|---------|-------|------|
| EP-03 `login` | `email` / `password` / `g-recaptcha-response` | `required\|email:filter` / `required` / `required\|recaptcha` |
| EP-05 `loginV2` | `email` / `password` / `captcha` | `required\|email:filter` / `required` / `required\|recaptcha` |
| EP-10 `resetForm`, EP-11 `resetFormV2` | `email` | `required\|email:filter\|exists:users,email` |
| EP-12 `confirmPassword` | `token` | `required\|exists:users,reset_token` |
| | `password` | `required\|string` + closure regex 6–12, đủ hoa/thường/số/ký hiệu |
| | `repeat_password` | `required\|same:password` |
| EP-16 `change` | `password` / `re-password` / `token` | `required\|between:6,13` / `required\|same:password` / `required\|exists:users,reset_token` |
| EP-07, EP-19, EP-23, EP-24 | — | Không validate |

**Ý nghĩa `email:filter`**: Laravel ≥ 5.8 đổi rule `email` mặc định sang `RFCValidation` (egulias — lỏng hơn). `email:filter` dùng `FILTER_VALIDATE_EMAIL` — **đúng như rule `email` của Laravel 5.5** → giữ nguyên hành vi chấp nhận/từ chối email sau khi nâng cấp. **Cao**.

**Custom rule `recaptcha`**: `AppServiceProvider.php:77` → `App\Validators\ReCaptcha::validate` (POST Google siteverify, secret `services.recaptcha.secret` = `GOOGLE_RECAPTCHA_SECRET`). Không đổi.

---

## 5. Events / Jobs

Không `event()`, `dispatch()`, Listener. Mail gửi đồng bộ. Ngoại lệ mới: `logout` ghi `bots_tutorial_cleanup_queue` — bảng hàng đợi dọn dữ liệu tutorial do tiến trình khác xử lý (chưa xác định bên Spring Boot hay Laravel command; ngoài phạm vi FA-040). → Không cần job-spec cho FA-040.

---

## 6. Middleware / Cấu hình

### 6.1 Middleware trên route auth
Group `web` (`Kernel.php:35-43`) + `NotifyChatworkRequestTimeSlow` (`web.php:81`). Không `guest`, không `auth`, không `throttle`.

### 6.2 Aliases liên quan (`Kernel.php` — nay là `$middlewareAliases`)
| Alias | Class | Ghi chú |
|-------|-------|--------|
| `guest` | `RedirectIfAuthenticated` | Vẫn no-op (`return $next($request)`) — không dùng |
| `throttle` | `Illuminate\Routing\Middleware\ThrottleRequests` | Không gắn route auth |
| `throttle_json` | `App\Http\Middleware\ThrottleRequestsJson` (**mới**) | Trả JSON 429 + `Retry-After`; dùng cho endpoint báo lỗi JS (`web.php:4169,4173,4196`), **không** cho auth |
| `check_login` | `CheckLogin` | Đã sửa (trước branch này): chưa đăng nhập → JSON 401「ログインが必要です。再度ログインしてください。」hoặc redirect `login` (spec cũ ghi "không gọi `$next`" — **không còn đúng**) |
| `check_remember_token` | `CheckRememberToken` | So `session('remember_token')` với `users.remember_token_reset_pass` bằng `!==`; khác → logout + invalidate; AJAX trả JSON「ログイン情報が変更されましたので、再度ログインしてください。」. Áp cho group `/admin`, `/basic`… (`web.php:87,95,100,933`) |
| `supper_admin` | `SupperAdmin` | role -1 + quyền route; không kiểm tra đã qua 2FA |

### 6.3 Global middleware thay đổi
`PreventRequestsDuringMaintenance` (thay `CheckForMaintenanceMode`); `TrustProxies` dùng `Illuminate\Http\Middleware\TrustProxies` với bitmask header (cùng tập header cũ) + IP `142.91.106.63`.

### 6.4 CSRF
`VerifyCsrfToken extends PreventRequestForgery`; `hasValidOrigin()` trả `false` → không chấp nhận POST chỉ dựa vào `Sec-Fetch-Site`. Danh sách `$except` không chứa route auth.

### 6.5 Session (`config/session.php`)
`driver = env('SESSION_DRIVER','file')`, `lifetime = env('SESSION_LIFETIME', 20*365 ngày)` (~20 năm), `expire_on_close=false`, `secure = env(...,false)`, `http_only=true`, `same_site=null`, **`serialization = 'php'`** (mới — giữ `serialize()` vì session chứa object; Laravel 13 mặc định `json`).

### 6.6 Auth (`config/auth.php` — không đổi)
Guard `web` (session, provider `users`), `api` (token), `affiliater`, `userEmailSetting`, `affiliater_api`, `api-mobile` (jwt), `api-job`. Broker `password_resets` (expire 600000) khai báo nhưng **không dùng** — luồng dùng `users.reset_token`.

---

## 7. Business Rules (file:line)

| # | Quy tắc | Nguồn | Tin cậy |
|---|---------|-------|---------|
| BR-01 | Mật khẩu lưu bcrypt; verify `Hash::check` (V2) / `Auth::attempt` (V1) | `AuthController.php:153,213,266,577,686` | Cao |
| BR-02 | Kiểm tra `is_active = 0` **trước** khi kiểm tra mật khẩu → redirect trang gửi lại mail kích hoạt | `:141-143`, `:207-209` | Cao |
| BR-03 | 2FA: role ≠ -1 chỉ khi `is_two_factor_verified = 1`; role -1 **luôn** (V2) | `:212-274` | Cao |
| BR-04 | Mã 2FA: `Str::random(10)`, lưu plain text trong `users`, hạn **24h** (EP-07) / **10 phút** (EP-24) | `:255,279,353`; `TwoFactorVerifyController.php:52,93` | Cao |
| BR-05 | Mã 2FA super admin (V2) gửi qua SMTP admin tới email của chính user; user thường gửi qua API mail | `:262,284` | Cao |
| BR-06 | Sau 2FA: redirect `adminTop` (role -1) / `adminIndex` | `:377` | Cao |
| BR-07 | Login V2 thành công không 2FA: redirect `preSelectBot` hoặc trang nhận lời mời staff nếu session có `code_invite` | `:230-249` | Cao |
| BR-08 | `login_histories` 1 bản ghi/user/ngày; V1 & EP-24 không ghi | `:218-227,361-370` | Cao |
| BR-09 | Session `remember_token` = `remember_token_reset_pass` khi đăng nhập V2/2FA; đổi mật khẩu sinh `Str::random(20)` mới → mọi phiên khác bị logout qua `CheckRememberToken` | `:228,373,580,686` | Cao |
| BR-10 | V1 `Auth::attempt(..., true)` luôn remember-me; V2 không remember | `:153,217` | Cao |
| BR-11 | Token reset = `RandomString(80).timestamp.user_id`, plain text | `:501,628` | Cao |
| BR-12 | Hạn token 24h tính từ `reset_token_expired` (thời điểm phát hành) bằng `(int) diffInHours(…, true) >= 24` — ép `int` + `absolute=true` để giữ kết quả Carbon 1 (Carbon 3 trả float có dấu) | `:440,468,564` | Cao |
| BR-13 | V1 `resetForm` không set `reset_token_expired`; `Carbon::parse(null)` = now → token V1 đi qua EP-12/EP-28 **luôn coi là còn hạn** nếu cột NULL, hoặc bị coi hết hạn sớm nếu còn giá trị cũ từ lần V2 trước | `:630,439,563` | Trung bình |
| BR-14 | Chính sách mật khẩu V3: 6–12 ký tự, đủ hoa/thường/số/ký hiệu, không trùng mật khẩu hiện tại; V1: 6–13 không yêu cầu độ phức tạp | `:537-546,570-574,669` | Cao |
| BR-15 | `confirmPassword` xác định user **theo token** (không tin `id` client), xoá token, kích hoạt tài khoản, revoke OAuth refresh token, không auto-login | `:559-591` | Cao |
| BR-16 | V1 `change`: không xoá token, không kiểm tra hạn, auto-login | `:685-688` | Cao |
| BR-17 | Check-user trả email chủ bot (`bots.admin_id`) nếu khớp cả channel_id + channel_secret và bot chưa xoá; không gửi mail | `:1688-1713` | Cao |
| BR-18 | Logout: enqueue dọn dữ liệu tutorial (trước `Auth::logout`), xoá 16 cookie `folder_*`, flush session, giữ cờ mời staff | `:388-430` | Cao |
| BR-19 | Lỗi `\Throwable` trong reset/đổi mật khẩu → `reportCaughtError` + 404 (hoặc JSON 500 cho AJAX ở EP-12) | `:517-522,593-603,640-645,689-694` | Cao |
| BR-20 | Không có giới hạn số lần đăng nhập sai / nhập mã sai / gửi mail reset | routes `web.php:2374-2577` | Cao |

---

## 8. Cảnh báo bảo mật

| Mã | Cảnh báo | Trạng thái so với spec cũ | Nguồn | Tin cậy |
|----|----------|--------------------------|-------|---------|
| S-01 | **Backdoor `env('PASS_LOGIN')`** trong `login` V1: biết mật khẩu chung + 1 email bất kỳ là đăng nhập được (kể cả super admin). UI không còn gọi `POST /login` nhưng route vẫn mở (cần token reCAPTCHA hợp lệ — người thật giải được) | **Còn** | `AuthController.php:145-151`, `web.php:2376` | Cao |
| S-02 | **MỚI — Chiếm tài khoản qua 2FA V1**: `POST /ajax/send-code-two-factor-verify` không cần đăng nhập, nhận `id` (số) và `email` tuỳ ý → sinh mã cho user `id` và gửi tới email kẻ tấn công, trả về `user_id` dạng Hashids; sau đó `POST /ajax/check-verify-code` với Hashids + mã → `Auth::loginUsingId` + set `remember_token` hợp lệ. Áp dụng cho mọi user (kể cả `id=1` super admin). Chỉ cần CSRF token lấy từ trang public | **Mới phát hiện** (code không đổi trong branch) | `TwoFactorVerifyController.php:48-74,85-117`, `web.php:2390,2405` | Cao (đọc code; chưa thử thực tế — tuân thủ quy tắc không thay đổi dữ liệu) |
| S-03 | **MỚI — Lộ toàn bộ bản ghi `users`** trên trang đặt mật khẩu: `reset-password-v3.blade.php:262` và `reset_password_v2.blade.php:215` in `{!! json_encode($user_id) !!}` (model User, chỉ ẩn `password`, `remember_token`) → người cầm link thấy `two_factor_verify_code`, `remember_token_reset_pass`, `key_login`, `channel_secret`, thông tin cá nhân/thanh toán… | **Mới phát hiện** | view + `User.php:34-36` | Cao |
| S-04 | Không throttle/lockout cho login, 2FA, reset, check-user (alias `throttle_json` mới có nhưng không gắn) | **Còn** | `web.php` | Cao |
| S-05 | Token reset lưu plain text; V1 không có hạn và không bị xoá sau khi dùng | **Còn** | `:628-630,686` | Cao |
| S-06 | Liệt kê email: `exists:users,email` trả「メールアドレスが登録されていません。」; `is_active=0` redirect trước khi kiểm tra mật khẩu | **Còn** | `:484-489,611-616,207-209` | Cao |
| S-07 | Check-user lộ email chủ bot khi biết channel_id + secret, không giới hạn | **Còn** | `:1688-1713` | Cao |
| S-08 | Mã 2FA plain text, hạn 24h (V2) không nhất quán với 10 phút (V1), không xoá sau khi dùng, không giới hạn số lần thử | **Còn** | `:353`, `TwoFactorVerifyController.php:93` | Cao |
| S-09 | Bỏ qua 2FA super admin qua V1: `login` gọi `Auth::attempt` (đăng nhập đầy đủ) **trước** khi chuyển tới trang 2FA; `SupperAdmin` middleware không kiểm tra đã qua 2FA. Bị chặn bởi `CheckRememberToken` chỉ khi `remember_token_reset_pass` của user khác NULL (session không có `remember_token`); dữ liệu mẫu user id=1 có cột này NULL | **Mới làm rõ** | `:153,160-161`; `CheckRememberToken.php`; `SupperAdmin.php` | Trung bình |
| S-10 | LINE OAuth `client_id`/`client_secret` hardcode; `EMAIL_API_TOKEN` có giá trị fallback hardcode | **Còn** | `UserController.php:2928-2929`; `ActiveAccount.php:470`; `MailApiService.php:103` | Cao |
| S-11 | Session lifetime mặc định ~20 năm, cookie `secure` mặc định false | **Ghi nhận mới** | `config/session.php:32,167` | Cao (config) / Thấp (giá trị env thực tế) |
| — | ~~`confirmPassword` nhận `id` từ client~~ | **Hết** — nay xác định user theo token + kiểm tra hạn 24h | `:559-568` | Cao |
| — | ~~`CheckLogin` không trả response khi chưa đăng nhập~~ | **Hết** — trả 401/redirect | `CheckLogin.php` | Cao |
| — | `guest` middleware no-op | Còn nhưng không dùng — không ảnh hưởng | `RedirectIfAuthenticated.php` | Cao |

---

## 9. Ảnh hưởng của nâng cấp Laravel 13 / PHP 8.3 tới FA-040

| Hạng mục | Thay đổi | Ảnh hưởng hành vi |
|---------|---------|------------------|
| Rule email | `email` → `email:filter` | Giữ nguyên tập email hợp lệ như 5.5 |
| Carbon 3 `diffInHours` | Thêm `(int)` + `absolute=true` | Giữ nguyên ngưỡng 24h |
| `addMinute` → `addMinutes` | Đổi tên API | Không đổi |
| Exception | `\Exception` → `\Throwable` + `reportCaughtError` | Lỗi PHP 8 `\Error` cũng được bắt → 404/500 có kiểm soát |
| CSRF | `PreventRequestForgery` + `hasValidOrigin()=false` | Giữ yêu cầu token |
| Session | `serialization = php` | Phiên cũ (file) đọc được sau nâng cấp |
| Mail | SwiftMailer → `SmtpMailer` (Symfony Mailer) | Cùng env `ADMIN_MAIL_*`, `RESEND_MAIL_*`; không đổi mailer mặc định |
| JSON ngày giờ model | `LegacyDateSerialization` | `created_at`… giữ `Y-m-d H:i:s` (ảnh hưởng S-03: dữ liệu lộ ra cùng định dạng cũ) |
| Exception Handler | JSON lỗi giữ `message` kiểu 5.5; `TokenMismatchException` không báo Chatwork | Không đổi phản hồi người dùng |

---

## 10. Đính chính so với spec cũ

| Mục spec cũ | Thực tế (code hiện tại) |
|------------|------------------------|
| `checkLogin` render `auth.loginv2` | `auth.auth-v3.login-v3` (`:82`) |
| UI submit `POST /login` | UI submit `POST /login-v2` (`login-v3.blade.php:239`) |
| `loginV2` thành công → `adminIndex` | → `preSelectBot` (`:249`) |
| Super admin V2 → `viewEnterVerifyCode` | → `verifyCode` (step 2 inline) (`:270`) |
| `authCodeLogin` luôn → `adminIndex` | role -1 → `adminTop` (`:377`) |
| `confirmPassword` nhận `id`, không kiểm hạn | Theo `token`, kiểm hạn 24h, revoke OAuth (`:529-585`) |
| Link mail V2 → `/reset_password?token` | → `/reset-password?token` (V3) (`:504`) |
| Logout xoá 13 cookie | 16 cookie + enqueue dọn tutorial (`:393-414`) |
| `check-user` view `auth.check_user` | `auth.auth-v3.check-user-v3` (`:1685`) |
| Routes `web.php:2122-2322` | `web.php:2374-2577` |

---

## 11. Điểm cần điều tra thêm

1. Xác nhận S-02 với team phát triển (không thử trên production). Đề xuất: yêu cầu session `user_id` đã qua mật khẩu, bỏ tham số `email` tự do.
2. `PASS_LOGIN` có được set trên production không (S-01).
3. Tiến trình xử lý `bots_tutorial_cleanup_queue` (Laravel command hay Spring Boot) — thuộc tính năng tutorial.
4. Giá trị thực `SESSION_DRIVER`, `SESSION_LIFETIME`, `SESSION_SECURE_COOKIE` trên production.
5. EP-15 `/change_password_v2` dead route — phản hồi thực tế trên Laravel 13.
