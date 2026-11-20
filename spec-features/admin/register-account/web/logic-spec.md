# [FA-039] Đăng ký tài khoản LME — Logic Spec

## Lịch sử cập nhật

| Ngày | Nội dung |
|------|----------|
| 2026-11-20 | **Re-spec theo branch `release_step_20261106`** (commit `ae06fb4c54`; Laravel 13, PHP ^8.3, `vinkla/hashids` ^14). Cập nhật toàn bộ `file:line`. Thay đổi so với spec cũ: (1) rule `email` → `email:filter` (EP-05/08/09/10 + mobile `CreateUserRegisterRequest`); (2) so sánh thời gian `(int) $a->diffInX($b, true)` (Carbon 3) — TTL 24h & ngưỡng resend 1 phút giữ nguyên ý nghĩa; (3) `catch (\Throwable)` + `reportCaughtError()`; (4) `user_point_settings.expire_date` dùng `Carbon::createFromTimestamp(..., date_default_timezone_get())` (giữ giờ JST, Carbon 3 mặc định UTC); (5) **mail**: `ActiveAccount`/`MailApiService` bỏ Swift Mailer, dùng `App\Mail\SmtpMailer` (Symfony Mailer qua `Mail::build`) cho SMTP `ADMIN_MAIL_*`/`RESEND_MAIL_*`, không còn đổi mailer mặc định; bắt `TransportExceptionInterface`; `MailApiService::sendMailAPi` trả true/false, email Hotmail/Outlook/Live/MSN đi thẳng SMTP Gmail; (6) **sửa sai spec cũ** (các điểm này đã có từ trước, spec cũ mô tả nhầm): `/register_user` dùng `registerUserV3` + view `register-v3` (UI gọi thẳng EP-08, bỏ EP-06/07); `ActivityLog::log(create_user)` **đang chạy** ở cả 3 luồng tạo user; `path_intro` dùng `resolvePathIntro()` + fallback `APP_URL`; có **4** mail sau đăng ký (thêm `sendMailConfirmUserRegisterSuccessToUserMASP`); danh sách route mặc định là **35** (không phải 34); `saveRegisterUserAff` **có** cập nhật `affiliate_info`; `UserTemporary::$fillable` **có** `path_intro`; (7) model thêm trait `LegacyDateSerialization` (JSON ngày giờ giữ `Y-m-d H:i:s`). 2 GAP cũ (không transaction, không cleanup `user_temporary`) **vẫn còn**. |
| (trước) | Bản gốc. |

## Tổng quan

- **Stack**: Laravel 13 + PHP ^8.3 (`composer.json`: `"php": "^8.3"`, `"laravel/framework": "^13.0"`). Kiến trúc vẫn dạng cũ: `app/Http/Kernel.php` + `bootstrap/app.php` kiểu Laravel 5 (không dùng `Application::configure()`), `$routeMiddleware` đổi tên thành `$middlewareAliases`.
- **Controller**: `App\Http\Controllers\AuthController` (`app/Http/Controllers/AuthController.php`, 1714 dòng). Logic nằm trực tiếp trong controller, không Service/Repository riêng (trừ `UserRepository::findById`, `getAdminByInviteCode`).
- **Loại**: Public — entry point tạo Admin user.

---

## Controllers + Actions

### `registerUserV3` (713-721) — Bước 1 (route `/register_user`)
Đọc `path_intro`, `ucode`, header `referer` → view `auth.auth-v3.register-v3` (`uCode`, `pathIntro`, `referer`).

### `registerUserAff` (1423-1439) / `registerUserAffV2` (1417-1421) — Bước 1 qua affiliate
- `registerUserAff`: view `register-v3` với `hashUserId`, `uCode` (= hash), `pathIntro`, `isMobile`, `referer`.
- `registerUserAffV2`: view `register-v3` với **chỉ** `hashUserId` → view không đọc biến này (đọc `$uCode`) ⇒ hash bị mất (BR-23).

### `registerUserV2` (723-728) — legacy, hỏng
View `auth.register_user_v2` thiếu `$referer` ⇒ `ErrorException` ⇒ Handler redirect `/` (xem api-spec EP-03).

### `register()` (697-700), `registerUser()` (702-711)
Không có route → code chết.

### `sendMail` (730-803) — Gửi mail xác thực

1. Rule `email: required|email:filter|unique:users,email`; nếu `env('APP_ENV') !== 'production'` và `type != 'resend'` thêm `code: required|exists:users,invite_code` (734-739). Lỗi → 422 `{"errors":[<MessageBag>]}` (748-752).
2. `$token = Str::random(60)` (754).
3. `$userTemp = UserTemporary::where('email', ...)->first()`; `$updateTime = $userTemp->updated_at ?? null`; `$diffInMinutes = (int) $updateTime->diffInMinutes($now, true)` (757-764).
4. Có record → gán `code`, `is_mobile`, `created_at = now`, `path_intro` (nếu request có) → `save()`; `$pathIntro` = request hoặc giá trị đã lưu (765-773). Không có → `UserTemporary::create([email, code, is_mobile, path_intro])` (774-782).
5. Nếu `$updateTime && $diffInMinutes > 1` → `ActiveAccount::reSendMailRedirectRegist($token, $email, $pathIntro, $hashUserId)` (784-786); ngược lại → `MailApiService::sendMailApi(['email','title' => '【重要】L Message本登録のお願い','content' => 'emails.redirect_regist','params' => [token, pathIntro, hashUserId]])` (787-796).
6. Trả 200 `{message: '認証メールが送信されました', sendMail: true}` (799-802) — không kiểm tra kết quả gửi mail.

> Lưu ý: lần gửi đầu và gửi lại trong vòng ≤ 1 phút đi kênh mặc định; gửi lại sau > 1 phút đi kênh Gmail dự phòng. Không có giới hạn số lần gửi / throttle.

### `typeInformation` (805-829), `confirmInformation` (831-851)
Chỉ validate, không ghi DB — **không còn được UI gọi**. Rule: xem api-spec EP-06/07.

### `resolvePathIntro($pathIntroRequest, $userTemp)` (863-878) — private helper
Duyệt lần lượt `[request pathIntro, userTemp->path_intro]`, bỏ qua `null`, `''`, `'1'`; trả về `trim(urldecode(x))` đầu tiên không rỗng; không có → `null`.

### `validateRegisterV2` (880-1115) — Tạo user (MAIN)

| Bước | Dòng | Logic |
|------|------|-------|
| 1. Decode affiliate | 885 | `$userIdInvite = Hashids::decode($request->hashUserId)` |
| 2. Validate token | 887-907 | `UserTemporary::where('code', $token)->first()` — không có → 410; có `User` email = `userTemp.email` & `is_active = 1` → 410; `(int) $createdAt->diffInHours($now, true) >= 24` → 410 (`{"errors":"token expired"}`) |
| 3. Affiliate admin | 909-913 | `$userIdInvite = [0]`, `$admin = userRepository->findById($userIdInvite)` |
| 4. Validate input | 914-948 | `username required\|max:50`, `password required\|between:6,13`, `email required\|email:filter\|unique:users,email`; **email lấy từ request** (918) → 422 |
| 5. user_introduce | 950-954 | `admin.allow_accept_aff == 1` → `user_introduce = $userIdInvite`; ngược lại `user_introduce_2 = $userIdInvite` (hoặc null) |
| 6. path_intro | 955-959, 967 | `$pathIntro = resolvePathIntro(request.pathIntro, $userTemp)`; nếu `userTemp.is_mobile == 1` và có pathIntro → thay `https://lme.jp` → `https://lme.jp/sp.html`; `users.path_intro = $pathIntro ?: env('APP_URL')` |
| 7. `$newData` | 960-974 | `role=0`, `password=bcrypt`, `admin_id = admin->admin_id ?: 1`, `max_bot = env('MAX_BOT', 1)`, `is_mobile = userTemp.is_mobile`, `created_at/updated_at = now`, `is_active = 1`, `token_active_register = null`, `expire_datetime_active_user = null` (ban đầu gán random/now rồi ghi đè), `ip = getClientIp()`; cộng `username`, `company_name`, `phone_number`, `email` |
| 8. INSERT users | 976 | `DB::table('users')->insertGetId($newData)` (bỏ qua model events) |
| 9. Activity log | 979 | `ActivityLog::log($userId, 'create', 'create_user', null, $email)` → `activity_logs` |
| 10. payment_detail_aff | 981-991 | Nếu affiliate: `admin_id = admin->admin_id` (hoặc 1), `user_id = $userIdInvite`, `type_bill = -1`, `remain_day = 0`, `bot_name = email user mới`, `user_bill_id = $userId` |
| 11. role_access | 993-1056 | 35 route (bên dưới). Với mỗi route có `access_feature.visible = 1`: role 1 luôn; role 2 trừ 10 route (`employeesManagement, botAdd, pointSettings, backup, notifySetting, affSetting, affResult, affMemberList, registerInfoAff, managePaymentStatus`); role 3 chỉ `chatBasic, index.talk, adminSetting` |
| 12. affiliate_info | 1057-1081 | `count_user_intro + 1`; nếu `is_receive_notification && when_registered && emails_receive_notify` → mỗi email: `MailApiService::sendMailApi` tiêu đề 「【L Message】ご紹介による新規アカウント登録がありました。」, template `emails.registered_user_aff` |
| 13. user_point_settings | 1082-1088 | `is_trial=true`, `m_bot=1`, `require_paypal=1`, `expire_date = createFromTimestamp(strtotime('+30 days', strtotime(date('Y-m-d 23:59:59'))), date_default_timezone_get())` |
| 14. Mail | 1091-1094 | `sendMailActiveAccountSuccess` (user), `sendMailConfirmUserRegisterToUser` (`MAIL_ADDRESS_CONFIRM_ADMIN`), `sendMailConfirmUserRegisterToUserMASP` (`MAIL_ADDRESS_CONFIRM_ADMIN_MASP`), `sendMailConfirmUserRegisterSuccessToUserMASP` (`MAIL_ADDRESS_CONFIRM_REGISTER_USER_ADMIN_MASP`) |
| 15. Đếm nguồn | 1097 | `countPathIntro($pathIntro)` — dùng giá trị đã resolve (null nếu đăng ký trực tiếp, **không** dùng `APP_URL`) |
| 16. Logout | 1098-1100 | `Auth::check()` → `Auth::logout()` |
| 17. Response | 1101-1105 | 200 `{message, confirm:false, currentStep:3}` |
| Lỗi | 1106-1114 | `catch (\Throwable)` → `reportCaughtError` (chỉ report `\Error`, throttle 1 lần/giờ/vị trí) + `Log::error` → 422 `{"errors": $ex->getMessage()}` |

**35 route mặc định** (993-1031): `chatBasic, index.talk, broadcast.index, scenario.index, index.msg_template, basicReply, settingAddFriend, form_answer.index, list_event.booking_event, events.index, booking.manager, tagHome, friendlistHome, friendInformationList, employeesManagement, errorList, landingIndex, index.conversion, urlHome, sitescriptHome, richMenu, mediaList, registerInfoAff, managePaymentStatus, listItemsOld, orderHistory, cycleOrderHistory, affSetting, affResult, affMemberList, pointSettings, adminSetting, botAdd, backup, notifySetting`.

### `countPathIntro($pathIntro)` (1117-1142)
`PathIntroData::query()->get()` (SoftDeletes → chỉ bản ghi chưa xoá); với mỗi bản ghi: `url_type == 1` và `Str::contains($pathIntro, url)` hoặc `url_type == 2` và `$pathIntro == url` → `increment('count_user')`; log `logInfo` danh sách id; mọi lỗi bị nuốt (`catch \Throwable`).

### `validateRegister` (1144-1326) — legacy POST `/register`
Tạo user **inactive** + mail kích hoạt; `path_intro = urldecode` nếu ≠ 1 (1218, không fallback `APP_URL`); `max_bot = env('MAX_BOT', 1)`; không ghi `ip`. Có `ActivityLog` (1224), `payment_detail_aff` (1227-1238), role_access, `user_point_settings` (1301-1307); **không** `affiliate_info`, **không** `countPathIntro`. Mail: `sendMailActiveAccount` + 3 mail nội bộ (1313-1318). Exception → redirect `route('404')`.

### `saveRegisterUserAff` (1441-1627) — legacy POST `/register_user/{user_id}`
Như `validateRegister`, affiliate từ path; `max_bot = env('MAX_BOT')` (không default, 1500); ghi `ip`; có `ActivityLog` (1517), `payment_detail_aff` (1520-1530), cập nhật `affiliate_info.count_user_intro` (1594-1601, không gửi mail notify); `user_point_settings` (1602-1608); mail 1614-1618.

### `redirectRegist($token)` (1371-1390)
Xem api-spec EP-12 — trả `register-v3` với `errorState` `invalid`/`registered`/`expired` hoặc `userTemp`.

### `activeAccount` (1392-1415), `resendMailActiveUser` (1344-1369), `accountNotActive` (1338-1342), `resendMailSuccess` (1333-1336), `registerUserSuccess` (1328-1331)
Xem api-spec EP-11, EP-13…EP-16.

---

## Models Eloquent

| Model | File | Table | Ghi chú (branch mới) |
|-------|------|-------|----------------------|
| `App\User` | `app/User.php` | `users` | Thêm trait `LegacyDateSerialization`, `HasFactory`; `Affiliates()` nay ném `\Error` (model không tồn tại — không dùng trong tính năng). Const `ROLE_ADMIN=-1`, `ROLE_USER=0`, `ROLE_STAFF=2` |
| `App\UserTemporary` | `app/UserTemporary.php` | `user_temporary` | `$fillable = ['email','code','is_mobile','path_intro']`; thêm `LegacyDateSerialization` ⇒ `json_encode($userTemp)` trong view giữ `created_at` dạng `Y-m-d H:i:s` |
| `App\RoleAccess` | `app/RoleAccess.php` | `role_access` | + trait |
| `App\AccessFeature` | `app/AccessFeature.php` | `access_feature` | + trait |
| `App\PaymentDetailAff` | `app/PaymentDetailAff.php` | `payment_detail_aff` | + trait |
| `App\UserPointSettings` | `app/UserPointSettings.php` | `user_point_settings` | + trait; các helper tính hạn đổi sang `createFromTimestamp(..., date_default_timezone_get())` (không dùng trong luồng đăng ký) |
| `App\AffiliateInfo` | `app/AffiliateInfo.php` | `affiliate_info` | + trait |
| `App\PathIntroData` | `app/PathIntroData.php` | `path_intro_data` | + trait; SoftDeletes; `URL_TYPE_PARTIAL=1`, `URL_TYPE_CORRECT=2` |
| `App\Models\ActivityLog` | `app/Models/ActivityLog.php` | `activity_logs` | `log($userId, $actionType, $actionName, $old, $new, $desc)` (64-74) → `create()`; `ACTION_CREATE_USER = 'create_user'` (title 「L Messageアカウント登録」), `TYPE_CREATE = 'create'` |

---

## Services / Mailers

### `App\Mail\MailApiService` (`app/Mail/MailApiService.php`)
- `sendMailAPi($data)` (7-28): render view `content` với `params` → nếu domain Hotmail/Outlook/Live/MSN (`isHotmailAddress`, 31-36) → `reSendMailCommon` (SMTP Gmail); nếu `TYPE_SEND_MAIL == 'default'` → `sendMailDefault`; ngược lại `sendMailApiChild` (HTTP API). **Trả `true/false`** (#41305) — luồng đăng ký bỏ qua giá trị này.
- `sendMailDefault` (38-69): `SmtpMailer::defaultWithTimeout(2)->html(...)` (cùng SMTP mặc định, timeout 2s/thao tác socket, chỉ AUTH LOGIN) — thay `Swift_SmtpTransport` + `SmtpTimeoutPlugin`; lỗi → `notifyChatwork` + fallback `reSendMailCommon` (nếu `TYPE_RESEND_TIMEOUT == 'google'`) hoặc API.
- `reSendMailCommon` (71-93): `SmtpMailer::resend()->html(...)` (`RESEND_MAIL_*`), trả `false` khi lỗi.

### `App\Mail\SmtpMailer` (`app/Mail/SmtpMailer.php`) — MỚI
Dựng Mailer riêng bằng `Mail::build` (Symfony Mailer): `admin()` (`mail.mailers.admin_smtp` ← `ADMIN_MAIL_*`), `resend()` (`mail.mailers.resend_smtp` ← `RESEND_MAIL_*`), `defaultWithTimeout($s)`. Map `ENCRYPTION` cũ → scheme (`ssl`/465 → `smtps`; `tls` → `smtp` + `require_tls`; rỗng → không tự STARTTLS). Timeout mặc định 30s. Không thay đổi mailer mặc định của tiến trình (khắc phục lỗi cũ quên khôi phục mailer khi exception).

### `App\Mail\ActiveAccount` (`app/Mail/ActiveAccount.php`) — thay đổi lớn
| Method | Dòng | Kênh | Template / Tiêu đề / Người nhận |
|--------|------|------|----------------------------------|
| `build()` | 35-38 | — | Nay `throw InvalidArgumentException('View [view.name] not found.')` — class chỉ dùng hàm static |
| `sendMailActiveAccount` | 40-58 | `MailApiService` | `emails.active_account_register`, 「【重要】L Message本登録のお願い」 — legacy |
| `sendMailRedirectRegist` | 60-70 | `Mail::send` | `emails.redirect_regist` — **không được gọi** (comment trong `sendMail`) |
| `reSendMailRedirectRegist` | 72-77 | `MailApiService::reSendMailCommon` (Gmail) | `emails.redirect_regist`, 「【重要】L Message本登録のお願い」 |
| `sendMailActiveAccountSuccess` | 122-133 | `MailApiService` | `emails.active_account_success`, 「L Message本登録完了のお知らせ」 → user |
| `sendMailConfirmUserRegisterToUser` | 171-192 | `SmtpMailer::admin()` | `emails.confirm_admin_user_register`, 「自動登録」 → `MAIL_ADDRESS_CONFIRM_ADMIN` |
| `sendMailConfirmUserRegisterToUserMASP` | 194-214 | `SmtpMailer::admin()` | `emails.confirm_mysp_admin_user_register`, 「自動登録」 → `MAIL_ADDRESS_CONFIRM_ADMIN_MASP` |
| `sendMailConfirmUserRegisterSuccessToUserMASP` | 238-258 | `SmtpMailer::admin()` | `emails.confirm_mysp_admin_user_register`, 「自動登録」 → `MAIL_ADDRESS_CONFIRM_REGISTER_USER_ADMIN_MASP` |

- 3 mail nội bộ bắt `Symfony\Component\Mailer\Exception\TransportExceptionInterface` (thay `Swift_TransportException`) → log + `return false`. Lỗi khác (vd render view) **không bị bắt** tại đây → nổi lên `catch \Throwable` của controller → 422 dù user đã được tạo.
- Static `ActiveAccount::sendMailApi` (455-…) nay dùng `Mail::html()` thay `setBody()` (không dùng trong luồng đăng ký).

### Template mail
- `resources/views/emails/redirect_regist.blade.php:5` — link 「ユーザー登録へ進む」 → `route('redirectRegist', ['token', 'uCode' => $hashUserId, 'pathIntro'])`.
- `emails/active_account_success.blade.php` — link `https://step.lme.jp/`.
- Không template mail nào thay đổi giữa 2 branch.

### Repository
`App\Repositories\Eloquents\UserRepository`: `findById($id)`, `getAdminByInviteCode($code)` (legacy).

### Helpers
`generateRandomString(32)`, `bcrypt()`, `Str::random(60)`, `Hashids::decode()`, `reportCaughtError()` (`app/Helpers/functions.php:9539` — chỉ `report()` nếu là `\Error`, không phải `\Exception`; chống lặp 1 giờ qua Cache), `logInfo/logDebug/logError`, `notifyChatwork`.

---

## Form Requests / Validation

Không dùng FormRequest cho luồng web (inline `Validator::make`). Luồng mobile `/register-mobile` dùng `App\Http\Requests\Mobile\CreateUserRegisterRequest` (đổi `email` → `email:filter`) — ngoài phạm vi.

| Endpoint | Field | Rule | Ghi chú |
|----------|-------|------|---------|
| EP-05 | `email` | `required\|email:filter\|unique:users,email` | **Đổi** |
| EP-05 | `code` | `required\|exists:users,invite_code` (non-prod, `type≠resend`) | |
| EP-06 | `username` / `company_name` / `phone_number` | `required\|string\|max:255` ×2 / `required\|regex:/^\d{10,11}$/` | Không dùng |
| EP-07 | `password` | `required\|between:6,12` | Không dùng |
| EP-08 | `username` / `password` / `email` | `required\|max:50` / `required\|between:6,13` / `required\|email:filter\|unique:users,email` | **Đổi** email |
| EP-09 | `username` / `password_regist` / `email_regist` / `invite_code` | `required\|max:50` / `required\|between:6,13` / `required\|email:filter\|unique` / `exists:users,invite_code` | **Đổi** email |
| EP-10 | như EP-09 (không invite_code) | | **Đổi** email |

**`email:filter`**: dùng `FilterEmailValidation` (PHP `filter_var(FILTER_VALIDATE_EMAIL)`) — chặt hơn rule `email` cũ của Laravel 5.5 với một số định dạng (vd ký tự Unicode, IP literal); client regex `validateEmail` vẫn có thể cho qua email bị server từ chối → hiển thị 「メールアドレスに誤りがあります。」.

### Lệch client ↔ server

| Field | Client (`register-v3`) | Server (EP-08) |
|-------|------------------------|----------------|
| `password` | 6–12 + 4 nhóm ký tự | `between:6,13`, không kiểm tra nhóm |
| `username` | không rỗng | `max:50` |
| `phone_number` | số, 10–11 chữ số, bắt buộc | **không validate** |
| `company_name` | tuỳ chọn | không validate |
| `email` | readonly từ `userTemp` | lấy từ request, không đối chiếu token |

---

## Events / Listeners / Queued Jobs

- Không Job/Queue/Event. Mail gửi **đồng bộ** trong request (tối đa 1 + 3 + N mail affiliate ở EP-08).
- Không có background job Spring Boot liên quan.

## Authorization

Public, không Policy/Gate. Bảo vệ: CSRF (trừ `/register`). Không throttle / captcha ở trang đăng ký.

---

## Business Rules

| ID | Rule | Nguồn (file:line) | Trạng thái |
|----|------|-------------------|-----------|
| BR-01 | Email unique trong `users` — kiểm tra ở EP-05 và EP-08 (rule `email:filter`) | `AuthController.php:735, 923, 1160, 1463` | Cập nhật |
| BR-02 | Chỉ non-production bắt mã mời (`exists:users,invite_code`) | `:737-739`; view `register-v3.blade.php:139-149` | Giữ |
| BR-03 | Token mail TTL 24h — `(int) diffInHours(created_at, now, true) >= 24` → hết hạn | `:898, 1381` | Cập nhật cú pháp |
| BR-04 | Gửi lại > 1 phút → kênh Gmail (`reSendMailRedirectRegist`); còn lại → `MailApiService` | `:757-796` | Cập nhật cú pháp |
| BR-05 | Mật khẩu: client 6–12 + 4 nhóm; server 6–13 không kiểm nhóm | `register-v3.blade.php:543-553`; `:922` | Cập nhật (EP-07 không còn dùng) |
| BR-06 | Trial 30 ngày: `expire_date` = 23:59:59 hôm nay + 30 ngày (giờ app) | `:1082-1088, 1301-1307, 1602-1608` | Cập nhật timezone |
| BR-07 | `max_bot = env('MAX_BOT', 1)` (EP-10: `env('MAX_BOT')` không default) | `:963, 1209, 1500` | Giữ |
| BR-08 | `user_introduce` vs `user_introduce_2` theo `admin.allow_accept_aff` | `:950-954, 1210-1214, 1501-1505` | Giữ |
| BR-09 | `users.role = 0`; role_access theo 35 route, role 1/2/3 (chỉ route `visible=1`) | `:960, 993-1056` | **Sửa** (34 → 35) |
| BR-10 | Đếm nguồn giới thiệu `path_intro_data.count_user` (PARTIAL/CORRECT), chỉ ở EP-08 | `:1097, 1117-1142` | Giữ |
| BR-11 | Mobile: thay `https://lme.jp` → `https://lme.jp/sp.html` khi `userTemp.is_mobile == 1` — **thực tế không xảy ra** vì UI v3 gửi `is_mobile=''` → NULL | `:957-959`; blade 507 | Cập nhật |
| BR-12 | Affiliate: `count_user_intro++` + mail notify (EP-08); EP-10 chỉ `++` | `:1057-1081, 1594-1601` | **Sửa** (EP-10 có cập nhật) |
| BR-13 | `payment_detail_aff` `type_bill = -1`, `bot_name = email` khi đăng ký qua affiliate | `:981-991, 1227-1238, 1520-1530` | Giữ |
| BR-14 | EP-08 tạo user active ngay (`is_active=1`, token null) | `:971-973` | Giữ |
| BR-15 | Legacy tạo user inactive + link kích hoạt 24h | `:1215-1217, 1399, 1506-1508` | Giữ |
| BR-16 | Logout nếu đang đăng nhập khi đăng ký | `:1098-1100` | Giữ |
| BR-17 | **Không có DB transaction** (users, activity_logs, payment_detail_aff, role_access, affiliate_info, user_point_settings, path_intro_data ghi tuần tự) | `:880-1115` (không `DB::transaction`) | **Còn** (GAP) |
| BR-18 | `DB::table('users')->insertGetId` — bỏ qua model events | `:976, 1221, 1513` | Giữ |
| BR-19 | 3 mail nội bộ 「自動登録」 qua `SmtpMailer::admin()` | `ActiveAccount.php:171-258` | **Sửa** (2 → 3 mail, đổi transport) |
| BR-20 | Mail hoàn tất 「L Message本登録完了のお知らせ」 cho user | `ActiveAccount.php:122-133` | Giữ |
| BR-21 | **MỚI** — EP-08 dùng `$request->email` để tạo user; token chỉ kiểm tra tồn tại/hạn của `userTemp`, không đối chiếu `userTemp.email` ⇒ client sửa payload có thể đăng ký email khác (chưa xác thực) bằng 1 token hợp lệ | `:888-918` | GAP (bảo mật) |
| BR-22 | **MỚI** — `users.path_intro` = `resolvePathIntro(request, userTemp)` ⇒ fallback `env('APP_URL')` khi đăng ký trực tiếp; `countPathIntro` dùng giá trị resolve (null khi trực tiếp) | `:863-878, 955-967, 1097` | Mới ghi nhận |
| BR-23 | **MỚI** — `registerUserAffV2` truyền `hashUserId` nhưng view đọc `uCode` ⇒ affiliate qua `/register_user_v2/{user_id}` bị mất (trừ khi đã có cookie `u_code`) | `:1417-1421`; `register-v3.blade.php:418` | GAP |
| BR-24 | **MỚI** — Ghi `activity_logs` (`create`/`create_user`, `new_value = email`) ở cả 3 luồng tạo user | `:979, 1224, 1517` | Sửa spec cũ (cũ ghi "comment out") |
| BR-25 | **MỚI** — `user_temporary` không bao giờ bị xoá (kể cả sau khi đăng ký thành công) ⇒ link mail cũ vẫn mở được tới khi hết 24h nhưng bị chặn bởi kiểm tra `is_active` | Không có `delete()` trong `AuthController.php` | **Còn** (GAP) |
| BR-26 | **MỚI** — EP-05 luôn trả 200 kể cả gửi mail thất bại (bỏ qua giá trị trả về `sendMailApi`) | `:784-802` | GAP |
| BR-27 | **MỚI** — Exception trong EP-08 trả `getMessage()` cho client (422) — trái quy ước "không lộ getMessage()" của dự án | `:1106-1114` | GAP |

---

## Dữ liệu bị thay đổi (EP-08)

| Bảng | Thao tác | Số record | Điều kiện |
|------|----------|-----------|-----------|
| `user_temporary` | SELECT | 1 | Luôn (không xoá) |
| `users` | SELECT (token/active, unique, affiliate) + INSERT | 1 | Luôn |
| `activity_logs` | INSERT | 1 | Luôn — **mới so với spec cũ** |
| `payment_detail_aff` | INSERT | 1 | Có affiliate |
| `access_feature` | SELECT | 35 | Luôn |
| `role_access` | INSERT | ≤ 63 (35 + 25 + 3); theo data mẫu `access_feature` (30/35 route visible) ⇒ **54** | Luôn |
| `affiliate_info` | UPDATE | 0–1 | Có affiliate |
| `user_point_settings` | INSERT | 1 | Luôn |
| `path_intro_data` | SELECT all + UPDATE | 0–N | Khớp URL |

Ở EP-05: `user_temporary` INSERT hoặc UPDATE 1 record.

## Đầu ra ngoài DB

- EP-05: 1 mail 「【重要】L Message本登録のお願い」.
- EP-08: 1 mail cho user + 3 mail nội bộ + N mail affiliate; `notifyChatwork` khi SMTP mặc định lỗi; `report()` cho `\Error`.

## Mức độ tin cậy

- Logic EP-05, EP-08, EP-12, BR-01…BR-27: **Cao** (đọc trực tiếp source).
- Số `role_access` thực tế (54): **Trung bình** (dựa data mẫu `access_feature` export 04/2026).
- Hành vi gửi mail thực tế (kênh nào được chọn): **Trung bình** (phụ thuộc `.env`: `TYPE_SEND_MAIL`, `TYPE_RESEND_TIMEOUT`).
