# API Spec — FA-040 Đăng nhập LME

> Spec các endpoint HTTP của luồng đăng nhập / quên mật khẩu / xác thực 2FA / kiểm tra tài khoản qua Channel ID. Tất cả endpoint nằm trong file `app/Http/Controllers/AuthController.php` (trừ 2FA view và LINE OAuth — ghi chú rõ ở từng endpoint).

## Nguồn tham chiếu

- Routes: `src/web/sns-line/routes/web.php` (dòng 2122–2322)
- Controller chính: `src/web/sns-line/app/Http/Controllers/AuthController.php` (1612 dòng)
- Controller 2FA: `src/web/sns-line/app/Http/Controllers/Admin/TwoFactorVerifyController.php`
- Controller LINE OAuth: `src/web/sns-line/app/Http/Controllers/Admin/UserController.php` (dòng 2812–2946)
- Middleware group cha: `Route::middleware(['NotifyChatworkRequestTimeSlow'])->group(...)` (dòng 77)
- Middleware web mặc định: `EncryptCookies`, `StartSession`, `ShareErrorsFromSession`, `VerifyCsrfToken`, `SubstituteBindings` (từ `app/Http/Kernel.php:34-43`)

---

## Bảng tóm tắt Endpoints

| ID | Method | URL | Controller@Method | Middleware | Xác thực | Màn hình |
|----|--------|-----|-------------------|-----------|---------|---------|
| EP-01 | GET | `/` | `AuthController@checkLogin` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-01 |
| EP-02 | GET | `/login` | `AuthController@checkLogin` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-01 |
| EP-03 | POST | `/login` | `AuthController@login` | web, NotifyChatworkRequestTimeSlow, CSRF | Không (bắt đầu session) | SCR-LGN-01 |
| EP-04 | GET | `/login-v2` | `AuthController@checkLoginV2` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-02 |
| EP-05 | POST | `/login-v2` | `AuthController@loginV2` | web, NotifyChatworkRequestTimeSlow, CSRF | Không (AJAX, JSON) | SCR-LGN-02 |
| EP-06 | GET | `/verify-code-login` | `AuthController@verifyCodeLogin` | web, NotifyChatworkRequestTimeSlow | Partial session (`user_id`) | SCR-LGN-03 |
| EP-07 | POST | `/auth-code-login` | `AuthController@authCodeLogin` | web, NotifyChatworkRequestTimeSlow, CSRF | Partial session (`user_id`) | SCR-LGN-03 |
| EP-08 | GET | `/reset_password` | `AuthController@resetPassword` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-04 / SCR-LGN-06 (dual-purpose) |
| EP-09 | GET | `/reset_password_v2` | `AuthController@resetPasswordV2` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-04 (V2) |
| EP-10 | POST | `/postReset` | `AuthController@resetForm` | web, NotifyChatworkRequestTimeSlow, CSRF | Không | SCR-LGN-04 (V1 submit) |
| EP-11 | POST | `/post_reset_v2` | `AuthController@resetFormV2` | web, NotifyChatworkRequestTimeSlow, CSRF | Không (AJAX, JSON) | SCR-LGN-04 (V2 submit) |
| EP-12 | POST | `/confirm_password` | `AuthController@confirmPassword` | web, NotifyChatworkRequestTimeSlow, CSRF | Không (AJAX, JSON) | SCR-LGN-06 |
| EP-13 | GET | `/reset-password-success` | `AuthController@resetPasswordSuccess` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-05 |
| EP-14 | GET | `/change_password` | `AuthController@changePassword` | web, NotifyChatworkRequestTimeSlow | Không (đang dùng view cũ, ít dùng) | SCR-LGN-06 (V1) |
| EP-15 | GET | `/change_password_v2` | `AuthController@changePasswordV2` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-06 (V2) |
| EP-16 | POST | `/change_password` | `AuthController@change` | web, NotifyChatworkRequestTimeSlow, CSRF | Không | SCR-LGN-06 (V1 submit) |
| EP-17 | GET | `/change_password_success` | `AuthController@changePasswordSuccess` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-07 |
| EP-18 | GET | `/check-user` | `AuthController@checkUser` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-08 |
| EP-19 | POST | `/check-user` | `AuthController@postCheckUser` | web, NotifyChatworkRequestTimeSlow, CSRF | Không (AJAX, JSON) | SCR-LGN-08 |
| EP-20 | GET | `/logout` | `AuthController@logout` | web, NotifyChatworkRequestTimeSlow | Yêu cầu đã đăng nhập | (Logout → SCR-LGN-01) |
| EP-21 | GET | `/view-send-code-two-factor-verify/{id}` | `Admin\TwoFactorVerifyController@viewSendCodeTwoFactoryVerify` | web, NotifyChatworkRequestTimeSlow | Không (dùng cho super admin) | SCR-LGN-03 (V1) |
| EP-22 | GET | `/enter-verify-code/{id}` | `Admin\TwoFactorVerifyController@viewEnterVerifyCode` | web, NotifyChatworkRequestTimeSlow | Không | SCR-LGN-03 (V2) |
| EP-23 | POST | `/ajax/send-code-two-factor-verify` | `Admin\TwoFactorVerifyController@sendCode` | web, NotifyChatworkRequestTimeSlow, CSRF | Không (AJAX) | Gửi lại mã — SCR-LGN-03 |
| EP-24 | POST | `/ajax/check-verify-code` | `Admin\TwoFactorVerifyController@checkVerifyCode` | web, NotifyChatworkRequestTimeSlow, CSRF | Không (AJAX) | Verify mã — SCR-LGN-03 |
| EP-25 | GET | `/line/callback/redirect-login` | `Admin\UserController@loginLine` | web, NotifyChatworkRequestTimeSlow | Không (dùng session `idQr`, `botIdQr`) | LINE OAuth callback |
| EP-26 | GET | `/line/callback/callback-login` | `Admin\UserController@callbackLoginLine` | web, NotifyChatworkRequestTimeSlow | Không | LINE OAuth success |
| EP-27 | GET | `/line/callback/callback-login-error` | `Admin\UserController@callbackLoginLineError` | web, NotifyChatworkRequestTimeSlow | Không | LINE OAuth error |

> **Ghi chú routes**: Các routes login KHÔNG có middleware `guest` (RedirectIfAuthenticated) — thay vào đó `checkLogin` / `checkLoginV2` tự kiểm tra `Auth::check()` ngay trong controller và redirect nếu đã đăng nhập.

---

## Chi tiết từng endpoint

### EP-01 / EP-02 — GET `/` và GET `/login` (hiển thị form đăng nhập)

**Route name**: `login`, `getLogin` (routes/web.php:2122, 2255, 2257)
**Controller**: `AuthController@checkLogin` — `app/Http/Controllers/AuthController.php:43-78`
**Middleware**: web (session + CSRF), `NotifyChatworkRequestTimeSlow`
**Liên kết**: SCR-LGN-01

#### Request
- Không tham số. Có thể nhận query string từ redirect trước đó.

#### Response

| Trường hợp | Phản hồi |
|-----------|----------|
| Chưa đăng nhập | `view('auth.loginv2', ['message' => $message])` — HTML 200 |
| Đã đăng nhập, role = 0 hoặc 1 (admin/user), có bot | redirect `route('adminIndex')` |
| Đã đăng nhập, role = 0/1, chưa có bot | redirect `route('botAdd')` |
| Đã đăng nhập, role = -1 (super admin) | redirect `route('adminTop')` |
| Đã đăng nhập, role khác (staff = 2), có bot, có level | redirect `route('adminIndex', [Hashids::encode(getBotId())])` |
| Đã đăng nhập, role khác, không level | redirect `route('basicHome', [Hashids::encode(getBotId())])` |

#### Ghi chú
- View trả về `auth.loginv2` với biến `message` là `message_intro` của user_id = 1 (dùng cho banner cross-sell L Gram).
- Nếu `last_login_time` trống, update bằng `strtotime(Carbon::now())` (dòng 47-49).

---

### EP-03 — POST `/login` (đăng nhập V1)

**Route name**: `postLogin` (web.php:2124)
**Controller**: `AuthController@login` — `AuthController.php:117-172`
**Middleware**: web (CSRF verify), `NotifyChatworkRequestTimeSlow`
**Liên kết**: SCR-LGN-01

#### Request (form-urlencoded)

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|---------|-----------|
| `email` | body | string | Có | `required|email` |
| `password` | body | string | Có | `required` |
| `g-recaptcha-response` | body | string | Có | `required|recaptcha` (custom rule, xem logic-spec) |
| `remember_me` | body | int (0/1) | Không | — (mapping `1 → true`) |
| `_token` | body | string | Có | CSRF token (do `VerifyCsrfToken` xử lý) |

#### Request mẫu
```
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

email=admin@example.com&password=MyP%40ssw0rd&g-recaptcha-response=03AFcWeA...&remember_me=1&_token=xxx
```

#### Response

| Trường hợp | Status | Phản hồi |
|-----------|--------|----------|
| Validate fail | 302 | `redirect()->back()->withErrors(...)->withInput()` |
| User không active (`is_active = 0`) | 302 | `redirect()->route('accountNotActive', ['email' => $email])` |
| Sai email/password | 302 | `redirect()->back()->withInput(['notice' => 'メールアドレス、もしくはパスワードが正しくありません。', ...])` |
| Login thành công, role = -1 | 302 | `redirect()->route('viewSendCodeTwoFactorVerify', ['id' => Hashids encoded user->id])` |
| Login thành công, role khác, không có bot | 302 | `redirect()->route('botAdd')` |
| Login thành công, role khác, có bot | 302 | `redirect()->route('adminIndex')` |

#### Error messages (tiếng Nhật)
- `email.required`: 「メールアドレスを入力してください。」
- `email.email`: 「正しいメールアドレスを入力してください。」
- `password.required`: 「パスワードを入力してください。」
- `g-recaptcha-response.required`: 「reCAPTCHAをチェックしてください。」
- `g-recaptcha-response.recaptcha`: `Captcha verification failed`

#### Ghi chú
- **Backdoor password**: Nếu input password bằng `env('PASS_LOGIN')`, hệ thống cho phép login bằng `Auth::loginUsingId($user->id)` mà không cần password đúng (dòng 146-152). Flag bảo mật cao — cần xác nhận biến env này có được set trên production không.
- Session Laravel mặc định được set sau `Auth::attempt`. `remember_me` luôn được truyền `true` vào `Auth::attempt` (dòng 154) bất kể giá trị.
- Cập nhật `last_login_time` = `strtotime(now())` sau khi login thành công (dòng 155).
- Nếu `role == -1` (super admin) → **luôn** chuyển sang flow 2FA cũ (V1) qua `viewSendCodeTwoFactorVerify`.

---

### EP-04 — GET `/login-v2`

**Route name**: `getLoginV2` (web.php:2126)
**Controller**: `AuthController@checkLoginV2` — `AuthController.php:80-115`
**Liên kết**: SCR-LGN-02

**Logic giống hệt EP-01/EP-02** — chỉ khác route name. Cùng trả về view `auth.loginv2`. Các nhánh redirect sau login giống hệt `checkLogin`.

---

### EP-05 — POST `/login-v2` (đăng nhập V2 — AJAX)

**Route name**: `postLoginV2` (web.php:2128)
**Controller**: `AuthController@loginV2` — `AuthController.php:174-279`
**Middleware**: web (CSRF verify), `NotifyChatworkRequestTimeSlow`
**Liên kết**: SCR-LGN-02

#### Request (JSON hoặc form-data — trả JSON)

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|---------|-----------|
| `email` | body | string | Có | `required|email` |
| `password` | body | string | Có | `required` |
| `captcha` | body | string | Có | `required|recaptcha` (lưu ý: tên field **khác V1** — `captcha` thay vì `g-recaptcha-response`) |
| `remember_me` | body | int (0/1) | Không | — |

#### Request mẫu
```json
{
  "email": "admin@example.com",
  "password": "MyP@ssw0rd",
  "captcha": "03AFcWeA...",
  "remember_me": 1
}
```

#### Response (JSON)

| Trường hợp | Status | Body |
|-----------|--------|------|
| Validate fail | 422 | `{"errors": {"email": ["..."], "password": ["..."], "captcha": ["..."]}}` |
| User không tồn tại | 422 | `{"errors": {"notice": ["メールアドレス・パスワードに誤りがあります。"]}}` |
| User không active | 200 | `{"redirect": "{route('accountNotActive',[email])}"}` |
| Sai password (role != -1) | 422 | `{"errors": {"notice": ["メールアドレス・パスワードに誤りがあります。"]}}` |
| Login thành công, không 2FA, có invite | 200 | `{"redirect": "{route staff-management.userAccessLinkInviteStaff}"}` |
| Login thành công, không 2FA | 200 | `{"redirect": "{route('adminIndex')}"}` |
| Login thành công, bật 2FA (role != -1) | 200 | `{"redirect": "{route('verifyCode')}"}` — set session `user_id` |
| Login thành công, role = -1 | 200 | `{"redirect": "{route('viewEnterVerifyCode', [Hashids])}"}` — set session `user_id`, gửi mail |

#### Error messages (V2)
- `email.email` (V2): 「メールアドレスに誤りがあります。」 (V1 dùng 「正しいメールアドレスを入力してください。」)
- `password.required` (V2): 「パスワードに誤りがあります。」 (V1 dùng 「パスワードを入力してください。」)
- `captcha.required`: 「reCAPTCHAをチェックしてください。」

#### Ghi chú
- V2 trả **JSON 422/200**, frontend tự redirect; V1 dùng redirect-back HTTP 302 truyền thống.
- Logic trigger 2FA: user có `is_two_factor_verified = 1` → gửi mail mã random 10 ký tự, ghi `two_factor_verify_code` + `time_generate_two_factor_auth_code`, redirect đến `route('verifyCode')` (role user) hoặc `route('viewEnterVerifyCode', [hashId])` (role super admin = -1).
- Nếu login không cần 2FA: tạo/update `login_histories` theo `user_id` + `date_login` (`Ymd`), set session `remember_token` = `$user->remember_token_reset_pass`, set `showPopup = true`, xoá các session tạm `user_access_link_invite`, `user_access_link_edit_owner_bot`, `code_invite`.

---

### EP-06 — GET `/verify-code-login`

**Route name**: `verifyCode` (web.php:2132)
**Controller**: `AuthController@verifyCodeLogin` — `AuthController.php:382-387`
**Liên kết**: SCR-LGN-03

#### Request
Không tham số. Dựa vào session `user_id` đã được set ở EP-05.

#### Response
- `view('auth.verify', ['message' => $message])` — 200 HTML

---

### EP-07 — POST `/auth-code-login`

**Route name**: `authCode` (web.php:2134)
**Controller**: `AuthController@authCodeLogin` — `AuthController.php:348-380`
**Liên kết**: SCR-LGN-03

#### Request (AJAX — form-data)

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|---------|-----------|
| `code` | body | string | Có | — (verify với `users.two_factor_verify_code`) |
| session `user_id` | session | int | Có | (set bởi EP-05 V2 hoặc EP-21 V1) |

#### Response (JSON)

| Trường hợp | Status | Body |
|-----------|--------|------|
| `user_id` session trống hoặc mã sai | 422 | `{"errors": {"notice": ["認証コードが間違っています。"]}}` |
| Mã đúng nhưng quá 24h | 422 | `{"errors": {"notice": ["認証コード期限が切れました。再度発行をしてください"]}}` |
| Thành công | 200 | `{"redirect": "{route('adminIndex')}"}` |

#### Ghi chú
- Hiệu lực mã xác thực: **24 giờ** (`Carbon::parse(...)->addHours(24)`, dòng 356).
- Sau verify thành công:
  - Ghi `login_histories` nếu chưa có record cho user + date hôm nay.
  - `Auth::loginUsingId($id)` + update `last_login_time`.
  - Set session `remember_token` = `remember_token_reset_pass` (dùng cho `CheckRememberToken` middleware).
  - `session()->forget('user_id')`.

---

### EP-08 — GET `/reset_password`

**Route name**: `reset_password` (web.php:2245)
**Controller**: `AuthController@resetPassword` — `AuthController.php:423-440`
**Liên kết**: SCR-LGN-04 (khi không có token) / SCR-LGN-06 (khi có token từ email)

#### Request

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|-----|--------|------|---------|--------|
| `token` | query | string | Không | Nếu có → check token trong `users.reset_token`; hiệu lực 24h |

#### Response

| Trường hợp | Phản hồi |
|-----------|----------|
| Không có token | `view('auth.reset_password_v2', ['user_id' => null])` — render SCR-LGN-04 |
| Có token, không tìm thấy user | `view('auth.reset_password_error')` |
| Có token, user exist nhưng hết hạn (>= 24h) | `view('auth.reset_password_error', ['email' => $user->email])` |
| Có token, user exist và còn hạn | `view('auth.reset_password_v2', ['user_id' => $user])` — render SCR-LGN-06 (form nhập password mới) |

#### Ghi chú
- Dùng cột `users.reset_token` (VARCHAR) và `users.reset_token_expired` (timestamp) để verify.
- View `auth.reset_password_v2` **dual-purpose**: hiện form nhập email (khi `$user_id == null`) hoặc form nhập password mới (khi có user).

---

### EP-09 — GET `/reset_password_v2`

**Route name**: `reset_password_v2` (web.php:2247)
**Controller**: `AuthController@resetPasswordV2` — `AuthController.php:442-450`

Logic tương tự EP-08 nhưng **không check expire**, không hiển thị error view khi token không tìm thấy — chỉ trả về cùng view `auth.reset_password_v2` với `user_id = null` nếu không match.

---

### EP-10 — POST `/postReset` (V1 submit email để nhận mail reset)

**Route name**: `postReset` (web.php:2249)
**Controller**: `AuthController@resetForm` — `AuthController.php:556-596`

#### Request (form-data)

| Tên | Validation |
|-----|-----------|
| `email` | `required|email|exists:users,email` |

#### Error messages
- `email.required`: 「メールアドレスを入力してください。」
- `email.email`: 「正しいメールアドレスを入力してください。」
- `email.exists`: 「メールアドレスが登録されていません。」 (**Lưu ý bảo mật**: endpoint V1 này **tiết lộ** email không tồn tại — khác với pattern chống enumeration thông thường.)

#### Response

| Trường hợp | Status | Phản hồi |
|-----------|--------|----------|
| Validate fail | 302 | redirect back với `withErrors` |
| Thành công | 302 | `redirect()->route('resetPasswordSuccess')` + flash `reset-success` |
| Exception | 302 | `redirect()->route('404')` |

#### Ghi chú
- Generate token: `RandomString(80) . now_timestamp . user_id`
- Lưu `reset_token` vào `users` (KHÔNG set `reset_token_expired` ở V1 — chỉ V2 set)
- Gửi mail qua `ResetPassword::resetPassword($email, $reset_link)` → `MailApiService::sendMailApi` (API bên ngoài `https://mail2026.watermeru.com/email/add-send`)

---

### EP-11 — POST `/post_reset_v2` (V2 submit email — AJAX JSON)

**Route name**: `postResetV2` (web.php:2251)
**Controller**: `AuthController@resetFormV2` — `AuthController.php:452-494`

#### Request (JSON)

| Tên | Validation |
|-----|-----------|
| `email` | `required|email|exists:users,email` |

#### Response (JSON)

| Trường hợp | Status | Body |
|-----------|--------|------|
| Validate fail | 422 | `{"errors": {"email": ["..."]}}` |
| Thành công | 302 | `redirect()->route('resetPasswordSuccess')->with('reset-success','reset-success')` |
| Exception | 302 | `redirect()->route('404')` |

#### Ghi chú
- Cùng validate với V1 nhưng trả JSON khi fail.
- **Khác biệt quan trọng V2**: set `reset_token_expired = Carbon::now()` (dòng 475 — có vẻ là lỗi: expired được set = now thay vì now+24h; expire thực tế kiểm tra ở EP-08 bằng `diffInHours >= 24` kể từ `reset_token_expired`, nên thực chất hết hạn sau 24h kể từ lúc request reset).
- Nếu user đã có `reset_token_db` từ trước → dùng `ActiveAccount::reSendMailResetPass($email, $reset_link)` (qua SMTP `RESEND_MAIL_*`). Nếu lần đầu → `ResetPassword::resetPassword(...)` qua API mail.

---

### EP-12 — POST `/confirm_password` (V2 submit password mới — AJAX JSON)

**Route name**: `confirmPassword` (web.php:2253)
**Controller**: `AuthController@confirmPassword` — `AuthController.php:496-554`
**Liên kết**: SCR-LGN-06 (V2)

#### Request (form-data hoặc JSON)

| Tên | Validation |
|-----|-----------|
| `id` | — (user_id lấy từ form hidden field, đã được render bởi EP-08) |
| `password` | `required|string` + custom: regex `/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{6,12}$/` (6-12 ký tự, ít nhất 1 chữ hoa + 1 thường + 1 số + 1 ký tự đặc biệt) |
| `repeat_password` | `required|same:password` |

#### Error messages
- `password` custom rule fail: 「英大文字・英小文字・数字・記号それぞれを最低1文字ずつ含む6~12文字のパスワードを入力してください。」
- Password mới trùng password cũ: 「このパスワードは最近使用されています。別のパスワードを指定してください。」
- `password.required`: 「パスワードを入力してください。」
- `repeat_password.required`: 「パスワードの確認を入力してください。」
- `repeat_password.same`: 「パスワードの確認が違います。」

#### Response (JSON)

| Trường hợp | Status | Body |
|-----------|--------|------|
| Validate fail | 422 | `{"errors": {"password": ["..."], "repeat_password": ["..."]}}` |
| Password mới trùng password cũ | 422 | `{"errors": {"password": ["このパスワードは最近使用されています。..."]}}` |
| Thành công | 200 | `{"redirect_url": "{route('reset_password', ['success' => true])}"}` |
| Exception (AJAX) | 500 | `{"error": "An unexpected error occurred."}` |

#### Ghi chú
- Cập nhật `users`: `password = bcrypt($new_password)`, `is_active = 1`, `reset_token = null`, `remember_token_reset_pass = Str::random(20)`.
- Setting `remember_token_reset_pass` mới sẽ **invalidate tất cả session hiện tại** (vì `CheckRememberToken` middleware so sánh session value với column này).

---

### EP-13 — GET `/reset-password-success`

**Route name**: `resetPasswordSuccess` (web.php:2163)
**Controller**: `AuthController@resetPasswordSuccess` — `AuthController.php:597-600`
**Liên kết**: SCR-LGN-05

Không tham số. Trả `view('auth.reset_password_success')`.

---

### EP-14 — GET `/change_password`

**Route name**: `change_password` (web.php:2261)
**Controller**: `AuthController@changePassword` — `AuthController.php:602-605`

Trả `view('auth.change_password')` — **view V1, ít dùng**. Flow chính hiện tại dùng `/reset_password?token=xxx` (EP-08) để hiển thị form nhập password mới.

---

### EP-15 — GET `/change_password_v2`

**Route name**: `change_password_v2` (web.php:2263)
**Controller**: `AuthController@changePasswordV2` — không thấy method trong source → **có thể là method bị xoá nhưng route còn** (dead route) hoặc dùng view mặc định. Cần điều tra thêm nếu cần chính xác.

---

### EP-16 — POST `/change_password` (V1 submit password mới)

**Route name**: `postChange` (web.php:2267)
**Controller**: `AuthController@change` — `AuthController.php:611-643`

#### Request (form-data)

| Tên | Validation |
|-----|-----------|
| `token` | `required|exists:users,reset_token` |
| `password` | `required|between:6,13` (6-13 ký tự — khác với V2 là 6-12) |
| `re-password` | `required|same:password` |

#### Error messages
- `token.exists`: 「このページは古いURLから開かれた無効なページです。最新のパスワード再設定用メールに記載されているURLを開いて再設定操作をしてください。」

#### Response

| Trường hợp | Phản hồi |
|-----------|----------|
| Validate fail | `redirect()->route('change_password', ['token' => $token])->withErrors(...)->withInput(...)` |
| Thành công | `redirect('/change_password_success')` — **auto-login user** với `Auth::loginUsingId($user_id)` |
| Exception | `redirect()->route('404')` |

#### Ghi chú
- Cập nhật `users`: `password = bcrypt($new_password)`, `is_active = 1`, `remember_token_reset_pass = Str::random(20)`. **KHÔNG** clear `reset_token` — có thể là bug nhỏ, khiến token vẫn dùng lại được nếu chưa bị overwrite bởi lần request sau.
- V1 khác V2: V2 clear `reset_token = null`, V1 không clear.
- V1 auto-login user, V2 KHÔNG auto-login (user phải tự quay lại login).

---

### EP-17 — GET `/change_password_success`

**Route name**: `change_password_success` (web.php:2265)
**Controller**: `AuthController@changePasswordSuccess` — `AuthController.php:606-609`
**Liên kết**: SCR-LGN-07

Trả `view('auth.change_pass_success')`.

---

### EP-18 — GET `/check-user`

**Route name**: `checkUser` (web.php:2322)
**Controller**: `AuthController@checkUser` — `AuthController.php:1581-1584`
**Liên kết**: SCR-LGN-08

Không tham số. Trả `view('auth.check_user')`.

---

### EP-19 — POST `/check-user` (AJAX)

**Route name**: `postCheckUser` (web.php:2130)
**Controller**: `AuthController@postCheckUser` — `AuthController.php:1586-1611`
**Liên kết**: SCR-LGN-08

#### Request (form-data, JSON)

| Tên | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|-----|--------|------|---------|--------|
| `channel_id` | body | string | Có | LINE Messaging API Channel ID (trim trước khi query) |
| `channel_secret` | body | string | Có | LINE Messaging API Channel Secret |

> **Không có validator** — controller chỉ trim và query.

#### Response (JSON 200)

| Trường hợp | Body |
|-----------|------|
| Không tìm thấy bot khớp channel_id+channel_secret (hoặc bot đã bị xoá) | `{"status": false, "data": null}` |
| Tìm thấy bot | `{"status": true, "data": {"id": 123, "view_name": "...", "bot_image": "...", "created_at": "2023-04-01 10:30", "created_at_display": "2023年04月01日 10時30分", "mail_admin_creator": "admin@example.com"}}` |

#### Ghi chú
- Query: `Bots::where('channel_id', $channelId)->where('channel_secret', $channelSecret)->where('is_deleted', 0)->first()`
- Lấy email admin chủ bot qua `User::find($bot->admin_id)->email`.
- **Không gửi mail tự động** — chỉ hiển thị email admin đã đăng ký để user nhớ.
- Không có rate limiting → lộ info tiềm năng: kẻ tấn công có thể thử cặp (channel_id, channel_secret) để dò email admin.

---

### EP-20 — GET `/logout`

**Route name**: `logout` (web.php:2259)
**Controller**: `AuthController@logout` — `AuthController.php:389-421`

#### Response
- 302 redirect `route('login')`

#### Ghi chú — side effects
- Forget session `current_bot_id`.
- Clear 13 cookies folder path (folder_schedule, folder_event_booking, folder_form_answer, folder_info_friend, folder_template, folder_image_rich_menus, folder_reply, folder_scenario, folder_url, folder_rich_menus, folder_cross_analysis, folder_conversion, folder_landing) — bằng cách `setcookie(..., '', -14400, '/basic/...', host)` (set expire ở quá khứ).
- `Auth::logout()` → Laravel clear auth session.
- Giữ lại (nếu có) `user_access_link_invite`, `user_access_link_edit_owner_bot`, `code_invite` để flow invite staff không bị mất.
- `Session::flush()` → xoá hoàn toàn session.
- Set lại session invite nếu cần → redirect login.

---

### EP-21 — GET `/view-send-code-two-factor-verify/{id}` (V1 — cho super admin)

**Route name**: `viewSendCodeTwoFactorVerify` (web.php:2136)
**Controller**: `Admin\TwoFactorVerifyController@viewSendCodeTwoFactoryVerify` — dòng 28-46

#### Path param
- `id`: user id đã được `Hashids::connection('url_code')->encode(...)`.

#### Response
- `view('admin.two-factory-verify.send_code', compact('listAdmin', 'user_id'))` — HTML 200
- `listAdmin`: danh sách email admin được phép nhận mã theo `config('sns-line.list_mail')` filter theo `APP_ENV`

---

### EP-22 — GET `/enter-verify-code/{id}`

**Route name**: `viewEnterVerifyCode` (web.php:2148)
**Controller**: `Admin\TwoFactorVerifyController@viewEnterVerifyCode` — dòng 76-83

#### Response
- User không tìm thấy → redirect `route('404')`
- Tìm thấy → `view('admin.two-factory-verify.enter_code_v2', ['id' => $id, 'user' => $user])`

---

### EP-23 — POST `/ajax/send-code-two-factor-verify`

**Route name**: `sendCodeTwoFactorVerify` (web.php:2138)
**Controller**: `Admin\TwoFactorVerifyController@sendCode` — dòng 48-74

#### Request
- `id`: user_id (integer, plain — không encode)
- `email`: email nhận mã

#### Response (JSON)
| Trường hợp | Body |
|-----------|------|
| `userId` rỗng | `{"status": false, "success": "Send code verify failed. Please, login again"}` |
| Thành công | `{"status": true, "user_id": "{Hashids encoded}", "success": "認証コードをメールに送りました。"}` |

#### Side effects
- Update `users.two_factor_verify_code` = `Str::random(10)`, `time_generate_two_factor_auth_code` = `now()`.
- Gọi `ActiveAccount::sendMailCodeVerifyAdmin([email, code])` — gửi qua SMTP custom `ADMIN_MAIL_*`.

---

### EP-24 — POST `/ajax/check-verify-code`

**Route name**: `checkVerifyCode` (web.php:2150)
**Controller**: `Admin\TwoFactorVerifyController@checkVerifyCode` — dòng 85-117

#### Request
- `id`: user_id dạng Hashids encoded (`url_code`)
- `code`: mã xác thực

#### Response (JSON)
| Trường hợp | Body |
|-----------|------|
| Sai mã | `{"status": false, "error": "認証コードが間違っています。"}` |
| Mã đúng nhưng quá 10 phút | `{"status": false, "error": "認証コード期限が切れました。再度発行をしてください"}` |
| Thành công | `{"success": "logged", "status": true}` |

#### Ghi chú quan trọng
- **Hiệu lực mã trong flow V1 (EP-24): 10 phút** — `Carbon::parse(...)->addMinute(10)`
- **Hiệu lực mã trong flow V2 (EP-07): 24 giờ** — `Carbon::parse(...)->addHours(24)`
  → **Không nhất quán** giữa 2 flow — điểm cần audit.
- Thành công: `Auth::loginUsingId($id)` + set session `remember_token`, forget `user_id`.

---

### EP-25 — GET `/line/callback/redirect-login`

**Route name**: `redirectLogin` (web.php:2298)
**Controller**: `Admin\UserController@loginLine` — dòng 2812-2936

#### Ghi chú
- **KHÔNG phải login flow cho LME portal** — đây là callback của LINE OAuth dùng cho **QR code follow + login flow** (check user đã là friend của bot, add tag/scenario/template khi scan QR rồi login LINE).
- Hardcoded: `client_id=1604115650`, `client_secret=032ccbec6e31a36d986f66e146475739` (LINE Login Channel).
- Flow: nhận `code` + `state` từ LINE → exchange token → get profile → check `LineUser::checkExistsUser` + `BotLineUser::checkExistsLineUser` (với `bot_id` từ session `botIdQr`) → nếu friend: add tag / scenario / message template theo `qr_url` record → redirect `callbackLogin` hoặc `callbackLoginError`.
- Không ghi nhận login vào LME portal.

---

### EP-26 — GET `/line/callback/callback-login`

**Route**: web.php:2299
**Controller**: `Admin\UserController@callbackLoginLine` (dòng 2938-2941)

Trả `view('callback_login')`.

---

### EP-27 — GET `/line/callback/callback-login-error`

**Route**: web.php:2300
**Controller**: `Admin\UserController@callbackLoginLineError` (dòng 2943-2946)

Trả `view('callback_login_error')`.

---

## Notes về CSRF và reCAPTCHA

### CSRF
- Tất cả POST đi qua `VerifyCsrfToken` middleware (group `web`, `Kernel.php:41`).
- Form login phải có `@csrf` hoặc hidden field `_token`. AJAX phải set header `X-CSRF-TOKEN` hoặc include `_token` trong body.

### reCAPTCHA
- Custom validator rule `recaptcha` đăng ký tại `AppServiceProvider.php:66` — `Validator::extend('recaptcha', 'App\\Validators\\ReCaptcha@validate')`.
- Logic verify: `App\Validators\ReCaptcha` — gọi `POST https://www.google.com/recaptcha/api/siteverify` với `secret = config('services.recaptcha.secret')` và `response = $value`. Trả về `$body->success` (bool).
- Config key: `services.recaptcha.secret` (từ `config/services.php`).
- Áp dụng ở: EP-03 (field `g-recaptcha-response`), EP-05 (field `captcha`).
- **KHÔNG** áp dụng ở: EP-10, EP-11, EP-12, EP-16, EP-19 — các endpoint này không có captcha bảo vệ → cần audit rate limiting.

---

## Liên kết Endpoint ↔ Màn hình

| EP | Màn hình |
|----|---------|
| EP-01, EP-02 | SCR-LGN-01 |
| EP-03 | SCR-LGN-01 (submit) |
| EP-04 | SCR-LGN-02 |
| EP-05 | SCR-LGN-02 (submit) |
| EP-06 | SCR-LGN-03 |
| EP-07 | SCR-LGN-03 (submit V2) |
| EP-08, EP-09 | SCR-LGN-04 (nếu không token) / SCR-LGN-06 (nếu có token) |
| EP-10, EP-11 | SCR-LGN-04 (submit) |
| EP-12 | SCR-LGN-06 (submit V2) |
| EP-13 | SCR-LGN-05 |
| EP-14, EP-15 | SCR-LGN-06 (V1) |
| EP-16 | SCR-LGN-06 (submit V1) |
| EP-17 | SCR-LGN-07 |
| EP-18 | SCR-LGN-08 |
| EP-19 | SCR-LGN-08 (submit) |
| EP-20 | Logout — redirect về SCR-LGN-01 |
| EP-21 | SCR-LGN-03 (V1 cho super admin — view gửi mã lại) |
| EP-22 | SCR-LGN-03 (V2 — view nhập mã) |
| EP-23 | (AJAX — gửi mã lại trong SCR-LGN-03) |
| EP-24 | (AJAX — verify mã V1 trong SCR-LGN-03) |
| EP-25, EP-26, EP-27 | LINE OAuth flow cho QR follow — không phải màn hình login chính |
