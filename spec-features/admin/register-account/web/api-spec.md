# [FA-039] Đăng ký tài khoản LME — API Spec

## Lịch sử cập nhật

| Ngày | Nội dung |
|------|----------|
| 2026-11-20 | **Re-spec theo branch `release_step_20261106`** (Laravel 5.5 → 13, PHP ^8.3). Cập nhật toàn bộ `file:line` theo code hiện tại. Thay đổi chính: (1) EP-01 `/register_user` → `AuthController@registerUserV3` render `auth.auth-v3.register-v3` (spec cũ ghi `registerUser` + `register_user_v2`); EP-02/EP-04/EP-12 cũng render `register-v3`; EP-11 render `register_user_success_v3`; (2) EP-03 `/register_user_v2` render view cũ bị lỗi `$referer` ⇒ thực tế **302 về `/`**; (3) rule email ở EP-05/08/09/10 đổi `email` → **`email:filter`** (kiểm tra bằng `filter_var FILTER_VALIDATE_EMAIL`); (4) so sánh thời gian dùng `(int) diffInX(..., true)` (Carbon 3 trả float có dấu — giữ hành vi cũ); (5) `catch (\Exception)` → `catch (\Throwable)` + `reportCaughtError()` ⇒ lỗi PHP `\Error` (TypeError…) nay cũng bị bắt và trả 422/redirect 404 thay vì 500; (6) EP-06/EP-07 **không còn được UI gọi**; (7) EP-12 trả `register-v3` với `errorState` (`invalid`/`registered`/`expired`) thay vì `active_user_error`/`active_user_success`; (8) bổ sung EP-13…EP-16 (luồng kích hoạt legacy); (9) CSRF: `VerifyCsrfToken` nay kế thừa `PreventRequestForgery` (Laravel 13) và tắt cơ chế bỏ qua token theo `Sec-Fetch-Site`. |
| (trước) | Bản gốc (12 endpoints) — dựa trên view `register_user_v2`. |

## Tổng quan

- **Mã tính năng**: FA-039
- **Base URL**: Admin portal (theo `config.yaml`; raw quan sát trên `https://form.watermeru.com`)
- **Authentication**: **Public** — không endpoint nào yêu cầu đăng nhập
- **Route file**: `routes/web.php` — các route nằm trực tiếp trong group `Route::middleware(['NotifyChatworkRequestTimeSlow'])` (`routes/web.php:81`), nạp với middleware group `web` (`app/Providers/RouteServiceProvider.php:56-58`)
- **CSRF**: `App\Http\Middleware\VerifyCsrfToken` (kế thừa `Illuminate\Foundation\Http\Middleware\PreventRequestForgery`), override `hasValidOrigin()` trả `false` (`app/Http/Middleware/VerifyCsrfToken.php:64-67`) ⇒ mọi POST phải có token. View `register-v3` **không** khai báo meta `csrf-token`; axios dựa vào cookie `XSRF-TOKEN` → header `X-XSRF-TOKEN` (cơ chế mặc định axios + Laravel) — **Trung bình**. Lưu ý: `/register` (EP-09) nằm trong `$except` (`VerifyCsrfToken.php:39`) ⇒ **không kiểm tra CSRF**.
- **Throttle**: không có `throttle`/`throttle_json` trên bất kỳ endpoint nào của tính năng.
- **Response**: GET → HTML; POST AJAX (EP-05..08) → JSON; POST legacy (EP-09, EP-10) → redirect.
- **Controller**: `app/Http/Controllers/AuthController.php` (1714 dòng)

---

## Danh sách endpoints

| Mã | Method | URL | Route name | Controller@Method (file:line) | Route (web.php) | UI đang dùng? |
|----|--------|-----|-----------|-------------------------------|-----------------|---------------|
| EP-01 | GET | `/register_user` | `register` | `registerUserV3` (713-721) | 2526 | **Có** — SCR-REG-02 |
| EP-02 | GET | `/register_user/{user_id}` | `registerAff` | `registerUserAff` (1423-1439) | 2540 | Có — link affiliate |
| EP-03 | GET | `/register_user_v2` | `register_v2` | `registerUserV2` (723-728) | 2528 | **Không** — lỗi view → 302 `/` |
| EP-04 | GET | `/register_user_v2/{user_id}` | `registerAffV2` | `registerUserAffV2` (1417-1421) | 2538 | Có (lỗi mất hash — xem chi tiết) |
| EP-05 | POST | `/send_mail_register` | `sendMailRegister` | `sendMail` (730-803) | 2532 | **Có** — SCR-REG-02 |
| EP-06 | POST | `/type_information` | `typeInformation` | `typeInformation` (805-829) | 2534 | **Không** (UI v3 bỏ) |
| EP-07 | POST | `/confirm_information` | `confirmInformation` | `confirmInformation` (831-851) | 2536 | **Không** (UI v3 bỏ) |
| EP-08 | POST | `/register_v2` | `registerUserV2` | `validateRegisterV2` (880-1115) | 2530 | **Có** — SCR-REG-03 |
| EP-09 | POST | `/register` | `registerUser` | `validateRegister` (1144-1326) | 2523 | Không (legacy, không view nào trỏ tới trong luồng hiện tại) |
| EP-10 | POST | `/register_user/{user_id}` | `saveRegisterAff` | `saveRegisterUserAff` (1441-1627) | 2542 | Không (legacy) |
| EP-11 | GET | `/register/success` | `registerUserSuccess` | `registerUserSuccess` (1328-1331) | 2411 | **Có** — SCR-REG-06 |
| EP-12 | GET | `/redirect-regist/{token}` | `redirectRegist` | `redirectRegist` (1371-1390) | 2409 | **Có** — link trong mail |
| EP-13 | GET | `/active-ccount/{token}` | `activeAccount` | `activeAccount` (1392-1415) | 2407 | Legacy (kích hoạt user inactive) |
| EP-14 | POST | `/account/resend-email` | `resendMailActiveUser` | `resendMailActiveUser` (1344-1369) | 2415 | Legacy |
| EP-15 | GET | `/account/resend-email/{email}` | `accountNotActive` | `accountNotActive` (1338-1342) | 2413 | Legacy |
| EP-16 | GET | `/account/resend-email-user/success` | `resendMailSuccess` | `resendMailSuccess` (1333-1336) | 2417 | Legacy |

> Đã xoá khỏi codebase: `app/Http/Controllers/Auth/RegisterController.php` (scaffold mặc định Laravel, không có route trỏ tới — spec cũ cũng không dùng). Method `AuthController@register()` (697-700, view `auth.register`) và `registerUser()` (702-711, view `auth.register_user_v2`) **không có route** — code chết.

---

## Chi tiết từng endpoint

### EP-01: GET `/register_user`

- **Mã nguồn**: `AuthController.php:713-721`
- **Query**: `path_intro` (string, tuỳ chọn), `ucode` (string, tuỳ chọn — hash affiliate)
- **Xử lý**: đọc header `referer` (log debug) → view `auth.auth-v3.register-v3` với `uCode`, `pathIntro`, `referer`.
- **Response**: 200 HTML.
- **UI**: SCR-REG-02. **Tin cậy**: Cao.

### EP-02: GET `/register_user/{user_id}`

- **Mã nguồn**: `AuthController.php:1423-1439`
- **Path**: `user_id` = hash ID affiliator. **Query**: `path_intro`, `is_mobile`.
- **Response**: view `register-v3` với `hashUserId`, `uCode` (= hash), `pathIntro`, `isMobile`, `referer`. View dùng `$uCode` → set cookie `u_code` 1 ngày. (`isMobile` không được view `register-v3` sử dụng.)
- **Tin cậy**: Cao.

### EP-03: GET `/register_user_v2` (legacy — hỏng)

- **Mã nguồn**: `AuthController.php:723-728` → view `auth.register_user_v2` với `uCode`, `pathIntro` (**thiếu `referer`**).
- **Thực tế**: view có `path_intro = '<?= $referer ?>'` (`resources/views/auth/register_user_v2.blade.php:1443`) ⇒ `ErrorException: Undefined variable $referer` ⇒ `app/Exceptions/Handler.php:266-277` (khách chưa login) ⇒ **302 → `/`**. Khớp raw `02-register-user-v2` (2026-11-20).
- **Tin cậy**: Trung bình–Cao (suy luận code + quan sát; nếu `app.debug=true` sẽ hiện trang lỗi thay vì redirect).

### EP-04: GET `/register_user_v2/{user_id}`

- **Mã nguồn**: `AuthController.php:1417-1421` → view `register-v3` với **chỉ** `hashUserId` (`compact('hashUserId')`).
- **Lưu ý (bug)**: `register-v3` đọc `$uCode` (blade 418, 490-492), **không** đọc `$hashUserId` ⇒ hash affiliate trên URL bị bỏ qua; chỉ còn nhận nếu đã có cookie `u_code` từ trước. **Tin cậy**: Cao.

### EP-05: POST `/send_mail_register`

- **Mã nguồn**: `AuthController.php:730-803`

#### Request

| Tên | Kiểu | Bắt buộc | Validation | Message (JP) |
|-----|------|---------|-----------|--------------|
| `email` | string | có | `required\|email:filter\|unique:users,email` | 「メールを入力してください。」/「メールアドレスに誤りがあります。」/「このメールアドレスはすでにエルメに登録済みです。」 |
| `code` | string | có khi `env('APP_ENV') !== 'production'` và `type != 'resend'` | `required\|exists:users,invite_code` | 「招待コードを入力してください。」/「招待コードをもらった方にご確認ください。」 |
| `type` | string | không | — | `'resend'` bỏ qua mã mời (UI v3 không gửi field này) |
| `is_mobile` | string | không | — | UI v3 luôn gửi `''` → NULL |
| `pathIntro` | string | không | — | Nguồn giới thiệu |
| `hashUserId` | string | không | — | Hash affiliator — chỉ nhúng vào link mail |

```json
{"email":"user@example.com","code":"ABC123","is_mobile":"","pathIntro":"https://lme.jp/","hashUserId":"N6LjrY1zr5RA"}
```

#### Xử lý (tóm tắt — chi tiết logic-spec)
1. Validate. 2. `token = Str::random(60)`. 3. Upsert `user_temporary` theo email (cập nhật `code`, `is_mobile`, `created_at = now`, `path_intro` nếu có). 4. Nếu đã có record và lần cập nhật trước cách > 1 phút (`(int) $updateTime->diffInMinutes($now, true) > 1`) → `ActiveAccount::reSendMailRedirectRegist` (SMTP `RESEND_MAIL_*`); ngược lại → `MailApiService::sendMailApi` template `emails.redirect_regist`, tiêu đề 「【重要】L Message本登録のお願い」.

#### Response
- **200**: `{"message":"認証メールが送信されました","sendMail":true}` — trả 200 **kể cả khi gửi mail thất bại** (giá trị trả về của `sendMailApi`/`reSendMailCommon` bị bỏ qua).
- **422**: `{"errors":[{"email":["このメールアドレスはすでにエルメに登録済みです。"]}]}` — `errors` là **mảng bọc 1 message bag** (UI lấy phần tử `[0]`).
- **419/401**: thiếu CSRF token (AJAX → 401 `SESSION_EXPIRED` theo `app/Exceptions/Handler.php:121-130`).
- Không có try/catch: exception khác (DB, render view) → Handler (AJAX → JSON 401/404 chung).

**UI**: SCR-REG-02 「認証メールを送信」. **Tin cậy**: Cao.

### EP-06: POST `/type_information` (không còn dùng)

- **Mã nguồn**: `AuthController.php:805-829` — không đổi so với spec cũ.
- Rule: `username` `required|string|max:255` (msg 「名前を入力してください。」/「50文字の名前を入力してください。」), `company_name` `required|string|max:255`, `phone_number` `required|regex:/^\d{10,11}$/` (msg 「電話番号は10から11桁の数字でなければなりません。」). 200 echo input; 422 `{"errors":{...}}`.
- **Không có view hiện hành nào gọi** (chỉ `register_user_v2` cũ). **Tin cậy**: Cao.

### EP-07: POST `/confirm_information` (không còn dùng)

- **Mã nguồn**: `AuthController.php:831-851` — không đổi.
- Rule: `password` `required|between:6,12` (msg 「 パスワードは6桁〜12桁の文字を入力してください。。」). 200 echo `password`, `repeat_password` (**trả lại mật khẩu plaintext**). Không view hiện hành nào gọi. **Tin cậy**: Cao.

### EP-08: POST `/register_v2` — tạo user (MAIN)

- **Mã nguồn**: `AuthController.php:880-1115`

#### Request

| Tên | Kiểu | Bắt buộc | Validation | Message (JP) |
|-----|------|---------|-----------|--------------|
| `token` | string | có | Thủ công: phải tồn tại `user_temporary.code`; email chưa có user active; `(int) diffInHours(created_at, now, true) < 24` | 410 `{"errors":"token expired"}` |
| `email` | string | có | `required\|email:filter\|unique:users,email` | 「メールを入力してください。」/「メールの形で入力してください。」/「このメールアドレスは既に登録されてます。」 |
| `username` | string | có | `required\|max:50` | 「名前を入力してください。」/「50文字の名前を入力してください。」 |
| `password` | string | có | `required\|between:6,13` | 「パスワードを入力してください。」/「 パスワードは6~13文字で設定してください。」 |
| `company_name` | string | không | — | — |
| `phone_number` | string | không | — (không validate server) | — |
| `hashUserId` | string | không | `Hashids::decode` | — |
| `pathIntro` | string | không | — | `'1'` = FE báo không có |
| `isMobile` | string | không | — | Không dùng (lấy `userTemp.is_mobile`) |

```json
{"token":"<60 ký tự>","email":"user@example.com","username":"エルグラム太郎","company_name":"株式会社エルグラム","phone_number":"09012345678","password":"Abc123!@","hashUserId":"N6LjrY1zr5RA","pathIntro":"https://lme.jp/","isMobile":""}
```

> ⚠ `email` lấy từ **request**, không bắt buộc trùng `user_temporary.email` của token (token chỉ dùng để kiểm tra tồn tại/hạn). Xem logic-spec BR-21.

#### Xử lý (tóm tắt)
Validate token → resolve affiliate → validate input → INSERT `users` (active ngay, `path_intro` = `resolvePathIntro()` hoặc `APP_URL`) → INSERT `activity_logs` (`create_user`) → (affiliate) INSERT `payment_detail_aff` → INSERT `role_access` (35 route × role 1/2/3, chỉ route có `access_feature.visible=1`) → (affiliate) UPDATE `affiliate_info` + mail thông báo → INSERT `user_point_settings` (trial 30 ngày) → 4 mail (`sendMailActiveAccountSuccess`, `sendMailConfirmUserRegisterToUser`, `sendMailConfirmUserRegisterToUserMASP`, `sendMailConfirmUserRegisterSuccessToUserMASP`) → `countPathIntro($pathIntro)` → logout nếu đang login.

#### Response
- **200**: `{"message":"認証メールが送信されました","confirm":false,"currentStep":3}` → UI chuyển `/register/success`.
- **410**: `{"errors":"token expired"}` — token không tồn tại / email của token đã active / quá 24h.
- **422 (validator)**: `{"errors":{"email":["このメールアドレスは既に登録されてます。"]}}`
- **422 (exception — `catch \Throwable`)**: `{"errors":"<exception message>"}` — lộ message nội bộ; có thể để lại dữ liệu dở (không transaction).

**UI**: SCR-REG-03 「この内容で登録」. **Tin cậy**: Cao.

### EP-09: POST `/register` (legacy)

- **Mã nguồn**: `AuthController.php:1144-1326`. **Không kiểm tra CSRF** (`$except`).
- Body: `username` (`required|max:50`), `password_regist` (`required|between:6,13`), `email_regist` (`required|email:filter|unique:users,email`), `invite_code` (`exists:users,invite_code` nếu có), `introduce_u` (hash), `path_intro`.
- Tạo user **inactive** (`is_active = config('sns-line.is_active.no')`, `token_active_register = generateRandomString(32)`, `expire_datetime_active_user = now`), `path_intro` = `urldecode` nếu ≠ 1 (không dùng `resolvePathIntro`), **có** ghi `activity_logs`, payment_detail_aff, role_access, user_point_settings; **không** cập nhật `affiliate_info`, **không** `countPathIntro`. Gửi `sendMailActiveAccount` (link `/active-ccount/{token}`) + 3 mail nội bộ.
- Response: 302 `registerUserSuccess`; lỗi validate → back withErrors; exception → 302 `route('404')`.
- **Tin cậy**: Cao.

### EP-10: POST `/register_user/{user_id}` (legacy affiliate)

- **Mã nguồn**: `AuthController.php:1441-1627`. Giống EP-09 nhưng affiliate từ path `user_id`; `max_bot = env('MAX_BOT')` (không default); **có** cập nhật `affiliate_info.count_user_intro` (1594-1601, không gửi mail thông báo); không `countPathIntro`. Message lỗi email giữ typo 「メールをを入力してください。」.
- **Tin cậy**: Cao.

### EP-11: GET `/register/success`

- **Mã nguồn**: `AuthController.php:1328-1331` → view `auth.register_user_success_v3` (spec cũ: `register_user_success_v2`). Không truy cập DB. **Tin cậy**: Cao.

### EP-12: GET `/redirect-regist/{token}`

- **Mã nguồn**: `AuthController.php:1371-1390`
- **Path**: `token`. **Query**: `uCode` (hash affiliate), `pathIntro` — được nhúng bởi `resources/views/emails/redirect_regist.blade.php:5` (`route('redirectRegist', ['token','uCode','pathIntro'])`).

| Điều kiện | View | Biến |
|-----------|------|------|
| Không có `user_temporary.code = token` | `auth.auth-v3.register-v3` | `errorState = 'invalid'` |
| Có user `email = userTemp.email` và `is_active = 1` | `register-v3` | `errorState = 'registered'` |
| `(int) diffInHours(created_at, now, true) >= 24` | `register-v3` | `errorState = 'expired'`, `expiredEmail` |
| Hợp lệ | `register-v3` | `userTemp` (serialize JSON — có cả `code`, `created_at` dạng `Y-m-d H:i:s` nhờ trait `LegacyDateSerialization`), `uCode`, `pathIntro` |

- **Response**: luôn 200 HTML. **UI**: SCR-REG-03 / SCR-REG-07. **Tin cậy**: Cao.

### EP-13: GET `/active-ccount/{token}` (legacy)

- **Mã nguồn**: `AuthController.php:1392-1415`. Tìm `users.token_active_register = token`: không có → `auth.active_user_error`; `expire_datetime_active_user + 1 ngày < now` → `auth.active_user_success` (`active=false`); ngược lại UPDATE `is_active=1`, xoá token → mail `sendMailActiveAccountSuccess` → `active_user_success` (`active=true`). Exception → JSON 400 `{"success":false}`.

### EP-14: POST `/account/resend-email` (legacy)

- **Mã nguồn**: `AuthController.php:1344-1369`. Body `email`. Nếu user tồn tại → UPDATE `token_active_register` mới, **`is_active = 0`**, `expire_datetime_active_user = now` → `sendMailActiveAccount`. Luôn 200 `{"success":true}` (kể cả email không tồn tại); exception → 400.
- ⚠ Endpoint public, không throttle, có thể đặt bất kỳ user nào về `is_active = 0` chỉ bằng email (rủi ro bảo mật — ngoài phạm vi luồng chính).

### EP-15 / EP-16

- EP-15 `accountNotActive` (1338-1342): view `auth.login_user_not_active` với `email`.
- EP-16 `resendMailSuccess` (1333-1336): view `auth.resend_mail_active_success`.

---

## Middleware áp dụng

| Middleware | Nguồn | Ảnh hưởng |
|-----------|-------|-----------|
| Group `web` (session, cookie, CSRF `VerifyCsrfToken`→`PreventRequestForgery`) | `RouteServiceProvider.php:56-58`, `app/Http/Kernel.php` | POST cần token (trừ `/register`) |
| `NotifyChatworkRequestTimeSlow` | `routes/web.php:81` | Chỉ log/thông báo request chậm |
| Global: `PreventRequestsDuringMaintenance` (thay `CheckForMaintenanceMode`), `TrimStrings`, `ConvertEmptyStringsToNull`, `TrustProxies` (nay `Illuminate\Http\Middleware\TrustProxies`, thêm IP proxy `142.91.106.63`) | `app/Http/Kernel.php` | `''` → `null` (vd `is_mobile`, `company_name`); `getClientIp()` dựa trên danh sách proxy tin cậy |

Không có: `basic_access`, `admin_access`, `check_login`, `throttle`.

---

## Liên kết endpoint ↔ màn hình

| Màn hình | Endpoint |
|----------|----------|
| SCR-REG-01 Login | — (link tới EP-01) |
| SCR-REG-02 Bước 1 | EP-01 / EP-02 / EP-04 (load), EP-05 (gửi mail) |
| Mail xác thực → SCR-REG-03 / SCR-REG-07 | EP-12 |
| SCR-REG-03 Bước 2 | EP-08 |
| SCR-REG-06 Hoàn thành | EP-11 |
| SCR-REG-07 Lỗi | EP-12 (server), EP-08 410 (client) |
| SCR-REG-08 | EP-03 (→ 302 `/`) |
| Không màn hình | EP-06, EP-07, EP-09, EP-10, EP-13…EP-16 |

## Error codes

| HTTP | Khi nào | Endpoint |
|------|---------|----------|
| 200 | Thành công (EP-05 kể cả gửi mail lỗi) | Tất cả GET, EP-05..08, EP-14 |
| 302 | Legacy redirect / EP-03 lỗi view | EP-03, EP-09, EP-10 |
| 400 | Exception | EP-13, EP-14 |
| 401 | CSRF hết hạn trên AJAX (`SESSION_EXPIRED`) | EP-05, EP-08 |
| 410 | Token không hợp lệ / đã đăng ký / hết 24h | EP-08 |
| 422 | Validator / exception (EP-08) | EP-05..08 |

## Phụ thuộc chéo

- FA-040 (login-account): màn login `/` chứa entry 「新規アカウント作成」; `/check-user`.
- Bảng: `users`, `user_temporary`, `activity_logs`, `role_access`, `access_feature`, `payment_detail_aff`, `affiliate_info`, `user_point_settings`, `path_intro_data`.

## Mức độ tin cậy

- Routes, controller, validation, response: **Cao** (đọc trực tiếp source `release_step_20261106`, commit `ae06fb4c54`).
- Hành vi CSRF qua cookie `XSRF-TOKEN`: **Trung bình**.
- EP-03 redirect: **Trung bình–Cao**.
