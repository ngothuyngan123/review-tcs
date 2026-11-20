# API Spec — FA-040 Đăng nhập LME

> Ngày spec: 2026-11-20 · Branch `release_step_20261106` (Laravel `^13.0`, PHP `^8.3` — `composer.json:8,14`).
> Endpoint HTTP của luồng đăng nhập / 2FA / đặt lại mật khẩu / check-user / logout.

## Lịch sử cập nhật

| Ngày | Nội dung |
|------|----------|
| 2026-11-20 | Re-spec theo branch `release_step_20261106` (diff từ `release_step_20260930_v2`, 697 commit). **Thay đổi do branch**: validate email `email` → `email:filter` (EP-03, EP-05, EP-10, EP-11); so sánh hạn token `(int) diffInHours(..., true) >= 24` (EP-08, EP-12, EP-29) — giữ hành vi cũ trên Carbon 3; `catch (\Exception)` → `catch (\Throwable)` + `reportCaughtError($e)` (EP-10, EP-11, EP-12, EP-16); `addMinute(10)` → `addMinutes(10)` (EP-24); CSRF middleware nay kế thừa `PreventRequestForgery` nhưng tắt cơ chế `Sec-Fetch-Site` (giữ hành vi 5.5); `Kernel::$routeMiddleware` → `$middlewareAliases`, thêm alias `throttle_json` (không gắn vào route auth). Route khối auth **không đổi**. **Sửa sai so với spec cũ** (spec cũ dựa trên code cũ hơn): số dòng route/controller; `checkLogin`/`checkLoginV2` render `auth.auth-v3.login-v3`; UI chính gửi `POST /login-v2`; super admin qua `loginV2` redirect `verifyCode` (không phải `viewEnterVerifyCode`); `loginV2` thành công redirect `preSelectBot`; `authCodeLogin` redirect `adminTop` cho role -1; `confirmPassword` xác định user theo `token` (không nhận `id`), kiểm tra hạn 24h, revoke `oauth_refresh_tokens`; thêm EP-28 `/reset-password` (V3) và EP-29 `/account/resend-email/{email}`; `logout` có thêm enqueue dọn dữ liệu tutorial. |
| (bản trước) | Bản đầu tiên. |

## Nguồn tham chiếu

- Routes: `src/web/sns-line/routes/web.php:2374-2577` (khối AuthController, trong group `Route::middleware(['NotifyChatworkRequestTimeSlow'])` mở tại `web.php:81`)
- Controller: `src/web/sns-line/app/Http/Controllers/AuthController.php` (1714 dòng)
- 2FA super admin: `app/Http/Controllers/Admin/TwoFactorVerifyController.php` (291 dòng)
- LINE OAuth QR: `app/Http/Controllers/Admin/UserController.php:2903-3038`
- Middleware group `web`: `app/Http/Kernel.php:35-43` (`EncryptCookies`, `AddQueuedCookiesToResponse`, `StartSession`, `ShareErrorsFromSession`, `App\Http\Middleware\VerifyCsrfToken`, `SubstituteBindings`); áp qua `RouteServiceProvider::mapWebRoutes()` (`app/Providers/RouteServiceProvider.php:54`)
- Laravel 13 vẫn dùng `app/Http/Kernel.php` + `bootstrap/app.php` kiểu cũ (bootstrap không đổi) — middleware **không** chuyển sang `bootstrap/app.php`.

---

## Bảng tóm tắt Endpoints

| ID | Method | URL | Route name | Controller@Method | Xác thực | Màn hình |
|----|--------|-----|-----------|-------------------|---------|---------|
| EP-01 | GET | `/` | `login` | `AuthController@checkLogin` | Không | SCR-LGN-01 |
| EP-02 | GET | `/login` | `getLogin` | `AuthController@checkLogin` | Không | SCR-LGN-01 |
| EP-03 | POST | `/login` | `postLogin` | `AuthController@login` | Không | (V1 legacy — UI không còn gọi) |
| EP-04 | GET | `/login-v2` | `getLoginV2` | `AuthController@checkLoginV2` | Không | SCR-LGN-02 |
| EP-05 | POST | `/login-v2` | `postLoginV2` | `AuthController@loginV2` | Không (AJAX JSON) | SCR-LGN-01, SCR-LGN-02 |
| EP-06 | GET | `/verify-code-login` | `verifyCode` | `AuthController@verifyCodeLogin` | Không | SCR-LGN-03b |
| EP-07 | POST | `/auth-code-login` | `authCode` | `AuthController@authCodeLogin` | Session `user_id` | SCR-LGN-03a/b |
| EP-08 | GET | `/reset_password` | `reset_password` | `AuthController@resetPassword` | Không | SCR-LGN-04 |
| EP-09 | GET | `/reset_password_v2` | `reset_password_v2` | `AuthController@resetPasswordV2` | Không | SCR-LGN-04 (biến thể) |
| EP-10 | POST | `/postReset` | `postReset` | `AuthController@resetForm` | Không | (V1 legacy) |
| EP-11 | POST | `/post_reset_v2` | `postResetV2` | `AuthController@resetFormV2` | Không (AJAX) | SCR-LGN-04, SCR-LGN-09 step 1 |
| EP-12 | POST | `/confirm_password` | `confirmPassword` | `AuthController@confirmPassword` | Token reset | SCR-LGN-04 (form token), SCR-LGN-09 step 3 |
| EP-13 | GET | `/reset-password-success` | `resetPasswordSuccess` | `AuthController@resetPasswordSuccess` | Không | SCR-LGN-05 |
| EP-14 | GET | `/change_password` | `change_password` | `AuthController@changePassword` | Không | SCR-LGN-06 |
| EP-15 | GET | `/change_password_v2` | `change_password_v2` | `AuthController@changePasswordV2` | — | **Dead route** (method không tồn tại) |
| EP-16 | POST | `/change_password` | `postChange` | `AuthController@change` | Token reset | SCR-LGN-06 |
| EP-17 | GET | `/change_password_success` | `change_password_success` | `AuthController@changePasswordSuccess` | Không | SCR-LGN-07 |
| EP-18 | GET | `/check-user` | `checkUser` | `AuthController@checkUser` | Không | SCR-LGN-08 |
| EP-19 | POST | `/check-user` | `postCheckUser` | `AuthController@postCheckUser` | Không (AJAX) | SCR-LGN-08 |
| EP-20 | GET | `/logout` | `logout` | `AuthController@logout` | (không bắt buộc) | — |
| EP-21 | GET | `/view-send-code-two-factor-verify/{id}` | `viewSendCodeTwoFactorVerify` | `Admin\TwoFactorVerifyController@viewSendCodeTwoFactoryVerify` | **Không** | 2FA super admin (V1) |
| EP-22 | GET | `/enter-verify-code/{id}` | `viewEnterVerifyCode` | `Admin\TwoFactorVerifyController@viewEnterVerifyCode` | **Không** | 2FA super admin (V1) |
| EP-23 | POST | `/ajax/send-code-two-factor-verify` | `sendCodeTwoFactorVerify` | `Admin\TwoFactorVerifyController@sendCode` | **Không** | 2FA super admin (V1) |
| EP-24 | POST | `/ajax/check-verify-code` | `checkVerifyCode` | `Admin\TwoFactorVerifyController@checkVerifyCode` | **Không** | 2FA super admin (V1) |
| EP-25 | GET | `/line/callback/redirect-login` | `redirectLogin` | `Admin\UserController@loginLine` | Không | LINE OAuth QR (ngoài luồng login portal) |
| EP-26 | GET | `/line/callback/callback-login` | `callbackLogin` | `Admin\UserController@callbackLoginLine` | Không | như trên |
| EP-27 | GET | `/line/callback/callback-login-error` | `callbackLoginError` | `Admin\UserController@callbackLoginLineError` | Không | như trên |
| EP-28 | GET | `/reset-password` | `reset-password` | `AuthController@resetPasswordV3` | Không | **SCR-LGN-09 (MỚI trong spec)** |
| EP-29 | GET | `/account/resend-email/{email}` | `accountNotActive` | `AuthController@accountNotActive` | Không | Đích redirect khi `is_active = 0` |

> Tất cả route trên chỉ có middleware group `web` + `NotifyChatworkRequestTimeSlow`. **Không có** `guest`, `auth`, `throttle`/`throttle_json` trên bất kỳ route nào của khối này (grep `routes/web.php` — `throttle` chỉ xuất hiện ở dòng 664, 1023, 4169, 4173, 4196, không liên quan auth). **Cao**.
>
> `web.php:32` còn khai báo `Route::get('/', fn => view('welcome'))` ở đầu file; route `GET /` tại `web.php:2511` đăng ký sau nên ghi đè (RouteCollection giữ route đăng ký cuối cùng cho cùng method+URI). **Trung bình**.

---

## Chi tiết từng endpoint

### EP-01 / EP-02 — GET `/`, GET `/login`

**Controller**: `AuthController@checkLogin` — `AuthController.php:46-84` · **Route**: `web.php:2511`, `web.php:2374`

| Trường hợp | Phản hồi |
|-----------|----------|
| Chưa đăng nhập | `view('auth.auth-v3.login-v3', ['message' => User::find(1)->message_intro])` (dòng 79-82) |
| Đã đăng nhập, role 0/1, không có bot (`getListBotIdStaffManagement`) | redirect `botAddV2` |
| Đã đăng nhập, role 0/1, có `current_bot_id` trong session | redirect `overview` |
| Đã đăng nhập, role 0/1, chưa chọn bot | redirect `preSelectBot` |
| Đã đăng nhập, role -1 | redirect `adminTop` |
| Đã đăng nhập, role khác (staff 2) | như role 0/1 (`botAddV2` / `overview` / `preSelectBot` kèm hash bot) |

Ghi chú: nếu `last_login_time` rỗng → cập nhật `strtotime(now)` (dòng 50-52). Biến `message` vẫn được truyền nhưng view login-v3 không dùng. **Cao**.

---

### EP-03 — POST `/login` (V1 legacy)

**Controller**: `AuthController@login` — `AuthController.php:116-171` · **Route**: `web.php:2376`
UI hiện tại **không gọi** endpoint này, nhưng route vẫn mở.

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|---------|-----------|
| `email` | body | string | Có | `required\|email:filter` (**đổi** từ `email`) |
| `password` | body | string | Có | `required` |
| `g-recaptcha-response` | body | string | Có | `required\|recaptcha` |
| `remember_me` | body | 0/1 | Không | Đọc nhưng không dùng (`Auth::attempt(..., true)` luôn remember) |
| `_token` | body/header | string | Có | CSRF |

| Trường hợp | Phản hồi |
|-----------|----------|
| Validate fail | 302 back + errors + input |
| `is_active = 0` | 302 `accountNotActive` (dòng 141-143) |
| `password == env('PASS_LOGIN')` + email tồn tại | `Auth::loginUsingId` — **backdoor vẫn còn** (dòng 145-151) |
| Sai thông tin | 302 back, `notice`「メールアドレス、もしくはパスワードが正しくありません。」(kèm `password` trong old input) |
| Thành công role -1 | 302 `viewSendCodeTwoFactorVerify` (id Hashids `url_code`) — lưu ý: **đã `Auth` đăng nhập trước khi qua 2FA** |
| Thành công, không có `bot_contracts` | 302 `botAdd` |
| Thành công | 302 `adminIndex` |

Lỗi: 「メールアドレスを入力してください。」「正しいメールアドレスを入力してください。」「パスワードを入力してください。」「reCAPTCHAをチェックしてください。」`Captcha verification failed`.

---

### EP-04 — GET `/login-v2`

**Controller**: `AuthController@checkLoginV2` — `AuthController.php:86-114` · **Route**: `web.php:2378`
Chưa đăng nhập → cùng view `auth.auth-v3.login-v3`. Đã đăng nhập → logic redirect **cũ**: đếm `bot_contracts` (admin_id = user.id OR user.admin_id) = 0 → `botAdd`; role 0/1 → `adminIndex`; role -1 → `adminTop`; khác → `adminIndex` kèm hash bot. **Cao**.

---

### EP-05 — POST `/login-v2` (AJAX — luồng chính)

**Controller**: `AuthController@loginV2` — `AuthController.php:173-276` · **Route**: `web.php:2380` · **Gọi từ**: `login-v3.blade.php:239`

#### Request (JSON)

| Tên | Kiểu | Bắt buộc | Validation |
|-----|------|---------|-----------|
| `email` | string | Có | `required\|email:filter` (**đổi**) |
| `password` | string | Có | `required` |
| `captcha` | string | Có | `required\|recaptcha` |
| `remember_me` | 0/1 | Không | Đọc nhưng không dùng; UI không gửi |

```json
{ "email": "admin@example.com", "password": "MyP@ssw0rd", "captcha": "03AFcWeA..." }
```

#### Response

| Trường hợp | Status | Body |
|-----------|--------|------|
| Validate fail | 422 | `{"errors": {"email": [...], "password": [...], "captcha": [...]}}` |
| Email không tồn tại | 422 | `{"errors": {"notice": ["メールアドレス・パスワードに誤りがあります。"]}}` |
| `is_active = 0` (kiểm tra **trước** mật khẩu) | 200 | `{"redirect": "/account/resend-email/{email}"}` |
| role ≠ -1, sai mật khẩu | 422 | `notice` như trên |
| role ≠ -1, `is_two_factor_verified = 0`, `Auth::attempt` OK, session có `code_invite` | 200 | `{"redirect": route('staff-management.userAccessLinkInviteStaff', {code})}` |
| role ≠ -1, không 2FA, OK | 200 | `{"redirect": route('preSelectBot', $params)}` (params có thể gồm `user_access_link_invite`/`user_access_link_edit_owner_bot`, `code_invite`) |
| role ≠ -1, `is_two_factor_verified = 1`, mật khẩu đúng | 200 | `{"redirect": route('verifyCode')}` — tạo mã, gửi `ActiveAccount::sendMailCodeVerify` (API mail), session `user_id` |
| role = -1, mật khẩu đúng | 200 | `{"redirect": route('verifyCode')}` — `sendMailCodeVerify()` private → `ActiveAccount::sendMailCodeVerifyAdmin` (SMTP `ADMIN_MAIL_*`, gửi tới chính email user), session `user_id` |
| role = -1, sai mật khẩu | 422 | `notice` |

Lỗi validate (V2): 「メールアドレスを入力してください。」「メールアドレスに誤りがあります。」「パスワードに誤りがあります。」「reCAPTCHAをチェックしてください。」`Captcha verification failed`.

Frontend: nếu `redirect` chứa `verify-code-login` → chuyển step 2 tại chỗ (không điều hướng). **Cao**.

Side effects (không 2FA): INSERT `login_histories` nếu chưa có hôm nay; session `remember_token` = `remember_token_reset_pass`; `showPopup = true`; xoá session `user_access_link_invite`, `user_access_link_edit_owner_bot`, `code_invite`. **Không** cập nhật `last_login_time` ở nhánh này (chỉ `CheckLogin` middleware bù khi rỗng).

---

### EP-06 — GET `/verify-code-login`

`AuthController@verifyCodeLogin` — `AuthController.php:381-386` · `web.php:2384`. Trả `view('auth.verify', ['message' => …])` — màn legacy (không kiểm tra session `user_id`).

---

### EP-07 — POST `/auth-code-login`

**Controller**: `AuthController@authCodeLogin` — `AuthController.php:345-379` · `web.php:2386` · Gọi từ `login-v3.blade.php:272`

| Tên | Vị trí | Bắt buộc | Ghi chú |
|-----|--------|---------|--------|
| `code` | body | Có | So sánh `==` với `users.two_factor_verify_code` |
| `user_id` | session | Có | Set bởi EP-05 |

| Trường hợp | Status | Body |
|-----------|--------|------|
| Không có session / mã sai | 422 | `{"errors": {"notice": ["認証コードが間違っています。"]}}` |
| Quá 24 giờ kể từ `time_generate_two_factor_auth_code` | 422 | `{"errors": {"notice": ["認証コード期限が切れました。再度発行をしてください"]}}` |
| Thành công | 200 | `{"redirect": role == -1 ? route('adminTop') : route('adminIndex')}` (dòng 377) |

Side effects: INSERT `login_histories` (nếu chưa có), `Auth::loginUsingId`, UPDATE `last_login_time`, session `remember_token`, forget `user_id`. Mã **không bị xoá** sau khi dùng (có thể dùng lại trong 24h nếu còn session). Không giới hạn số lần nhập sai. **Cao**.

---

### EP-08 — GET `/reset_password` (legacy)

`AuthController@resetPassword` — `AuthController.php:432-449` · `web.php:2500`

| Trường hợp | Phản hồi |
|-----------|----------|
| Không `token` | `view('auth.reset_password_v2', ['user_id' => null])` |
| Token không khớp | `view('auth.reset_password_error')` |
| `(int) now->diffInHours(reset_token_expired, true) >= 24` (**đổi**) | `view('auth.reset_password_error', ['email'])` |
| Còn hạn | `view('auth.reset_password_v2', ['user_id' => $user])` |

---

### EP-09 — GET `/reset_password_v2`

`AuthController@resetPasswordV2` — `AuthController.php:451-459` · `web.php:2503`. Tìm user theo token, **không kiểm tra hạn**, trả `auth.reset_password_v2`.

---

### EP-10 — POST `/postReset` (V1 legacy)

`AuthController@resetForm` — `AuthController.php:606-647` · `web.php:2505`

| Field | Validation |
|-------|-----------|
| `email` | `required\|email:filter\|exists:users,email` (**đổi**) |

Lỗi:「メールアドレスを入力してください。」「正しいメールアドレスを入力してください。」「メールアドレスが登録されていません。」(lộ email có tồn tại hay không).
Thành công: UPDATE `reset_token` (không set `reset_token_expired`), mail link `/change_password?token=…` qua `ResetPassword::resetPassword` → 302 `resetPasswordSuccess` + flash `reset-success`. Lỗi bất kỳ (`\Throwable`, **đổi**) → `reportCaughtError` + 302 `404`.

---

### EP-11 — POST `/post_reset_v2` (AJAX)

`AuthController@resetFormV2` — `AuthController.php:479-523` · `web.php:2507` · Gọi từ `reset-password-v3.blade.php:308` và `reset_password_v2`

| Field | Validation |
|-------|-----------|
| `email` | `required\|email:filter\|exists:users,email` (**đổi**) |

| Trường hợp | Status | Body |
|-----------|--------|------|
| Validate fail | 422 | `{"errors": {"email": [...]}}` |
| Thành công | 302 → `/reset-password-success` (axios đi theo redirect, nhận HTML 200) | flash `reset-success` |
| `\Throwable` | 302 → `404` | `reportCaughtError($e)` |

Side effects: UPDATE `users.reset_token = RandomString(80).timestamp.user_id`, `reset_token_expired = now()`; link mail = `route('reset-password', ['token'])` (V3). Nếu user đã có `reset_token` cũ → `ActiveAccount::reSendMailResetPass` (SMTP `RESEND_MAIL_*` qua `SmtpMailer::resend()`), ngược lại `ResetPassword::resetPassword` (API mail). **Cao**.

---

### EP-12 — POST `/confirm_password` (AJAX)

`AuthController@confirmPassword` — `AuthController.php:525-604` · `web.php:2509` · Gọi từ `reset-password-v3.blade.php:353`

| Field | Validation |
|-------|-----------|
| `token` | `required\|exists:users,reset_token` — lỗi「このページは古いURLから開かれた無効なページです。最新のパスワード再設定用メールに記載されているURLを開いて再設定操作をしてください。」 |
| `password` | `required\|string` + closure regex `/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{6,12}$/` —「英大文字・英小文字・数字・記号それぞれを最低1文字ずつ含む6~12文字のパスワードを入力してください。」 |
| `repeat_password` | `required\|same:password` —「パスワードの確認を入力してください。」「パスワードの確認が違います。」 |

> Spec cũ ghi field `id` từ client — **không còn**: user được xác định bằng `reset_token` (comment dòng 559 "chặn account-takeover").

| Trường hợp | Status | Body |
|-----------|--------|------|
| Validate fail | 422 | `{"errors": {...}}` |
| Token quá 24h (`(int) diffInHours(..., true) >= 24`, dòng 563-568) | 422 | `{"errors": {"token": ["リンクの有効期限が切れました。お手数ですが、再度パスワード再設定のお手続きをお願いします。"]}}` |
| Trùng mật khẩu hiện tại | 422 | `{"errors": {"password": ["このパスワードは最近使用されています。別のパスワードを指定してください。"]}}` |
| Thành công | 200 | `{"redirect_url": route('reset-password', ['success' => true])}` (UI V3 bỏ qua, tự chuyển step 4) |
| `\Throwable` + AJAX | 500 | `{"error": "An unexpected error occurred."}` |
| `\Throwable` không AJAX | 302 `404` | |

Side effects: UPDATE `users` (`password=bcrypt`, `is_active=1`, `reset_token=null`, `remember_token_reset_pass=Str::random(20)`); UPDATE `oauth_refresh_tokens SET is_revoked=1 WHERE user_id=? AND is_revoked=0` (dòng 583-585); log `logInfo('[action=confirm_password][entity=User][id=…]')`. **Cao**.

---

### EP-13 — GET `/reset-password-success`

`AuthController.php:648-651` · `web.php:2418` → `view('auth.reset_password_success')`.

### EP-14 — GET `/change_password`

`AuthController.php:653-656` · `web.php:2515` → `view('auth.change_password')` (không kiểm tra token khi GET).

### EP-15 — GET `/change_password_v2` (dead route)

`web.php:2517` trỏ `AuthController@changePasswordV2` nhưng method **không tồn tại** (grep toàn file). Trên Laravel 13 gọi sẽ ném `BadMethodCallException` → `Exceptions\Handler` xử lý như lỗi (redirect/404 tuỳ nhánh). **Cao** (về việc thiếu method), **Trung bình** (về phản hồi cụ thể).

### EP-16 — POST `/change_password` (V1 legacy)

`AuthController@change` — `AuthController.php:662-695` · `web.php:2521`

| Field | Validation |
|-------|-----------|
| `password` | `required\|between:6,13` (message key `password.digits_between` không khớp rule → dùng message mặc định) |
| `re-password` | `required\|same:password` |
| `token` | `required\|exists:users,reset_token` |

Thành công: UPDATE `password`, `is_active=1`, `remember_token_reset_pass` (**không** xoá `reset_token`, **không** kiểm tra hạn, **không** revoke OAuth token), `Auth::loginUsingId` → redirect `/change_password_success`. Lỗi validate → redirect `change_password?token` + input (gồm mật khẩu). `\Throwable` → `reportCaughtError` + 302 `404`.

### EP-17 — GET `/change_password_success`

`AuthController.php:657-660` · `web.php:2519` → `view('auth.change_pass_success')`.

### EP-18 — GET `/check-user`

`AuthController.php:1683-1686` · `web.php:2577` → `view('auth.auth-v3.check-user-v3')` (**đổi view** so với spec cũ `auth.check_user`).

### EP-19 — POST `/check-user` (AJAX)

`AuthController@postCheckUser` — `AuthController.php:1688-1713` · `web.php:2382` · Gọi từ `check-user-v3.blade.php:275`

| Field | Bắt buộc | Ghi chú |
|-------|---------|--------|
| `channel_id` | (client) | `trim`, không validate server |
| `channel_secret` | (client) | `trim`, không validate server |

| Trường hợp | Body (200) |
|-----------|-----------|
| Không tìm thấy bot `is_deleted = 0` khớp cả 2 | `{"status": false, "data": null}` |
| Tìm thấy | `{"status": true, "data": {"id", "view_name", "bot_image", "created_at": "Y-m-d H:i", "created_at_display": "Y年m月d日 H時i分", "mail_admin_creator": email|null}}` |

Không có throttle. **Cao**.

### EP-20 — GET `/logout`

`AuthController@logout` — `AuthController.php:388-430` · `web.php:2513`

Side effects theo thứ tự:
1. Nếu đã đăng nhập: `TutorialInitDataCleanupService::enqueueCleanupOnLogout(getAdminId(user), Auth::id())` — ghi `bots_tutorial_cleanup_queue` cho các bot có dữ liệu tutorial seed (best-effort, tự nuốt lỗi) — **mới so với spec cũ**.
2. Forget `current_bot_id`; xoá **16** cookie `folder_*` (thêm `folder_event_booking_day`, `folder_popup`, `folder_sales` so với spec cũ).
3. `Auth::logout()`; giữ cờ invite; `Session::flush()`; khôi phục cờ invite.
4. 302 `login`.

### EP-21 → EP-24 — 2FA super admin (V1, chỉ dùng sau EP-03)

| EP | Dòng | Mô tả |
|----|------|-------|
| EP-21 | `TwoFactorVerifyController.php:28-46` · `web.php:2388` | Decode Hashids `url_code`; render `admin.two-factory-verify.send_code` với danh sách email nhận mã từ `config('sns-line.list_mail')` theo `APP_ENV` |
| EP-23 | `:48-74` · `web.php:2390` | Body `id` (user id **dạng số, không mã hoá**), `email` (**bất kỳ**). Tạo mã `Str::random(10)`, UPDATE `users`, gửi `sendMailCodeVerifyAdmin` tới `email` truyền lên. Trả `{"status": true, "user_id": <Hashids>, "success": "認証コードをメールに送りました。"}`; `id` rỗng → `{"status": false, "success": "Send code verify failed. Please, login again"}` |
| EP-22 | `:76-83` · `web.php:2403` | Render `admin.two-factory-verify.enter_code_v2`; user không tồn tại → `404` |
| EP-24 | `:85-117` · `web.php:2405` | Body `id` (Hashids), `code`. Sai →「認証コードが間違っています。」; quá **10 phút** (`addMinutes(10)` — **đổi** từ `addMinute(10)`, cùng nghĩa) →「認証コード期限が切れました。再度発行をしてください」; đúng → `Auth::loginUsingId($id)` + session `remember_token` → `{"success": "logged", "status": true}` |

> ⚠ EP-23 + EP-24 **không yêu cầu đăng nhập, không kiểm tra session/mật khẩu, không giới hạn email nhận** → xem cảnh báo bảo mật S-02 trong logic-spec.

### EP-25 → EP-27 — LINE OAuth callback (QR follow)

`Admin\UserController@loginLine` — `UserController.php:2903-3028` · `web.php:2553-2555`. Không phải đăng nhập portal. `client_id='1604115650'`, `client_secret='032ccbec6e31a36d986f66e146475739'` **vẫn hardcode** (dòng 2928-2929). `callbackLoginLine` (dòng 3030) / `callbackLoginLineError` (dòng 3035) render view.

### EP-28 — GET `/reset-password` (V3 — MỚI trong spec)

**Controller**: `AuthController@resetPasswordV3` — `AuthController.php:461-477` · `web.php:2501`

| Tham số | Vị trí | Ghi chú |
|---------|--------|--------|
| `token` | query | Tuỳ chọn |
| `success` | query | `1` → UI hiển thị step 4 (xử lý ở client) |

| Trường hợp | Phản hồi |
|-----------|----------|
| Không token | `view('auth.auth-v3.reset-password-v3', ['user_id' => null])` → step 1 |
| Token không khớp | `view('auth.auth-v3.reset-password-error')` |
| Token quá 24h | `view('auth.auth-v3.reset-password-error', ['email'])` |
| Còn hạn | `view('auth.auth-v3.reset-password-v3', ['user_id' => $user])` → step 3; **toàn bộ model User được `json_encode` vào trang** |

### EP-29 — GET `/account/resend-email/{email}`

`AuthController@accountNotActive` — `AuthController.php:1338-1342` · `web.php:2413` → `view('auth.login_user_not_active', ['email'])`. Đích redirect khi `is_active = 0` (EP-03, EP-05). Gửi lại mail thuộc FA-039.

---

## CSRF & reCAPTCHA

### CSRF
- `App\Http\Middleware\VerifyCsrfToken` nay `extends Illuminate\Foundation\Http\Middleware\PreventRequestForgery` (Laravel 13) và override `hasValidOrigin()` → `false` (`VerifyCsrfToken.php`, task #43854): **mọi POST vẫn bắt buộc token** như Laravel 5.5, không chấp nhận chỉ header `Sec-Fetch-Site: same-origin`. **Cao**.
- AJAX auth-v3 dùng axios → header `X-XSRF-TOKEN` từ cookie `XSRF-TOKEN`.
- Lệch token trên request JSON → `Exceptions\Handler` trả 401 (#41500); `TokenMismatchException` không báo Chatwork.

### reCAPTCHA
- Rule `recaptcha` đăng ký `AppServiceProvider.php:77` → `App\Validators\ReCaptcha@validate` (gọi `https://www.google.com/recaptcha/api/siteverify` với `services.recaptcha.secret` = env `GOOGLE_RECAPTCHA_SECRET`). Không đổi.
- Áp dụng: EP-03 (`g-recaptcha-response`), EP-05 (`captcha`). **Không** áp dụng: EP-07, EP-10, EP-11, EP-12, EP-16, EP-19, EP-23, EP-24.

---

## Liên kết Endpoint ↔ Màn hình

| Màn hình | Endpoint |
|---------|---------|
| SCR-LGN-01 | EP-01, EP-02 (hiển thị), EP-05 (submit), EP-07 (step 2) |
| SCR-LGN-02 | EP-04, EP-05, EP-07 |
| SCR-LGN-03a (inline) | EP-07 |
| SCR-LGN-03b (legacy) | EP-06, EP-07 |
| SCR-LGN-04 | EP-08/EP-09, EP-11, EP-12 (khi có token) |
| SCR-LGN-05 | EP-13 |
| SCR-LGN-06 | EP-14, EP-16 (link từ EP-10) |
| SCR-LGN-07 | EP-17 |
| SCR-LGN-08 | EP-18, EP-19 |
| SCR-LGN-09 | EP-28, EP-11 (step 1), EP-12 (step 3) |
| (không màn hình) | EP-03, EP-15, EP-20, EP-21…EP-27, EP-29 |
