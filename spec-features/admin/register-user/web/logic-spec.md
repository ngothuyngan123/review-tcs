# [FA-039] Đăng ký tài khoản LME — Logic Spec

## Tổng quan

- **Mã tính năng**: FA-039
- **Tên**: Đăng ký tài khoản LME (アカウント登録)
- **Stack**: Laravel 5 + PHP 7.2
- **Entry controller**: `App\Http\Controllers\AuthController`
- **Loại feature**: Public (không auth) — entry point tạo Admin user mới cho hệ thống LME

---

## Controllers + Actions

Tất cả method dưới đây đều nằm trong file `src/web/sns-line/app/Http/Controllers/AuthController.php`.

### `AuthController@registerUser` (line 650-659) — Hiển thị Step 1

Render view `auth.register_user_v2` với biến:
- `uCode` = `$request->ucode`
- `pathIntro` = `$request->path_intro`
- `referer` = giá trị header `referer` (`$request->header()['referer'][0]` nếu có)

Có log debug header và referer.

### `AuthController@registerUserV2` (line 661-666) — Alias Step 1 V2

Như `registerUser` nhưng không đọc header referer — chỉ truyền `uCode`, `pathIntro`.

### `AuthController@registerUserAff` (line 1325-1341) — Step 1 với affiliate

Nhận `user_id` từ path. Render view `auth.register_user_v2` với `hashUserId`, `uCode` (= hashUserId), `pathIntro`, `isMobile`, `referer`.

### `AuthController@registerUserAffV2` (line 1319-1323) — Step 1 V2 với affiliate

Nhận `user_id` từ path. Render view với `hashUserId`.

### `AuthController@sendMail` (line 668-741) — Gửi mail xác thực

**Đầu vào**: `email` (required|unique:users,email), `code` (invite — required nếu non-production & !resend), `type`, `is_mobile`, `pathIntro`, `hashUserId`.

**Logic**:
1. Validate (tham khảo api-spec EP-05)
2. Sinh token: `$token = Str::random(60)`
3. Tìm `UserTemporary::where('email', ...)->first()`
4. Tính `$diffInMinutes` = diff giữa `updated_at` (nếu có) và now
5. Nếu `$userTemp` tồn tại:
   - `$userTemp->code = $token`
   - `$userTemp->is_mobile = $is_mobile`
   - `$userTemp->created_at = Carbon::now()`
   - Nếu có `pathIntro` → update `$userTemp->path_intro`
   - `$userTemp->save()`
6. Nếu không tồn tại:
   - `UserTemporary::create(['email' => ..., 'code' => $token, 'is_mobile' => ..., 'path_intro' => ...])`
7. Quyết định kênh gửi mail:
   - Nếu `$updateTime && $diffInMinutes > 1` → `ActiveAccount::reSendMailRedirectRegist($token, $email, $pathIntro, $hashUserId)` (dùng SMTP `RESEND_MAIL_*` — fallback Gmail)
   - Ngược lại → `MailApiService::sendMailApi(['email' => $email, 'title' => '【重要】L Message本登録のお願い', 'content' => 'emails.redirect_regist', 'params' => ['token', 'pathIntro', 'hashUserId']])`
8. Trả JSON `{message, sendMail: true}` status 200

### `AuthController@typeInformation` (line 743-767) — Validate Step 2a

**Đầu vào**: `username`, `company_name`, `phone_number`, `email`.

**Rule validation**:
- `username` → `required|string|max:255` (error: 名前を入力してください。/ 50文字の名前を入力してください。)
- `company_name` → `required|string|max:255` (error: 会社名・屋号を入力してください。)
- `phone_number` → `required|regex:/^\d{10,11}$/` (error: 電話番号を入力してください。/ 電話番号は10から11桁の数字でなければなりません。)

**Không ghi DB** — chỉ validate → echo lại input dưới dạng JSON.

### `AuthController@confirmInformation` (line 769-789) — Validate Step 2b

**Đầu vào**: `password`, `repeat_password`.

**Rule validation**:
- `password` → `required|between:6,12` (error: パスワードを入力してください。/ パスワードは6桁〜12桁の文字を入力してください。。)

**Không check** `repeat_password` (chỉ echo lại); **không check** pattern phức tạp 4-nhóm-ký-tự (đó là client-side only).

**Không ghi DB**.

### `AuthController@validateRegisterV2` (line 791-1020) — Tạo user (V2 MAIN)

Đây là **method chính** của feature. Chi tiết:

#### Bước 1 — Validate token

```
$userIdInvite = Hashids::decode($request->hashUserId);
$token = $request->token;
$userTemp = UserTemporary::where('code', $token)->first();
if (!$userTemp) → return 410 {"errors":"token expired"}
$user = User::where('email', $userTemp->email)->where('is_active', 1)->first();
if ($user) → return 410 {"errors":"token expired"}   // User đã active rồi
$createdAt = Carbon::parse($userTemp->created_at);
if ($createdAt->diffInHours(Carbon::now()) >= 24) → return 410 {"errors":"token expired"}
```

#### Bước 2 — Resolve affiliate admin

```
if (!empty($userIdInvite)) {
    $userIdInvite = $userIdInvite[0];
    $admin = $this->userRepository->findById($userIdInvite);   // select * from users where id = ?
}
```

#### Bước 3 — Validate input

```
'username' => 'required|max:50',
'password' => 'required|between:6,13',
'email'    => 'required|email|unique:users,email',
```

Error messages (JP): xem api-spec EP-08.

Lỗi → 422.

#### Bước 4 — Chuẩn bị `$newData` cho INSERT `users`

```
if ($admin && $admin->allow_accept_aff == 1) {
    $newData['user_introduce'] = $userIdInvite ?: null;
} else {
    $newData['user_introduce_2'] = $userIdInvite ?: null;
}

if ($userTemp->is_mobile == 1 && $request->pathIntro != 1) {
    $request->pathIntro = str_replace("https://lme.jp", 'https://lme.jp/sp.html', $request->pathIntro);
}

$newData['role'] = 0;                                  // USER role
$newData['password'] = bcrypt($password);
$newData['admin_id'] = $admin && $admin->admin_id ? $admin->admin_id : 1;
$newData['max_bot'] = env('MAX_BOT', 1);
$newData['token_active_register'] = generateRandomString(32);  // ghi đè = null cuối cùng
$newData['expire_datetime_active_user'] = Carbon::now();        // ghi đè = null cuối cùng
$newData['path_intro'] = $request->pathIntro != 1 ? urldecode($request->pathIntro) : null;
$newData['is_mobile'] = $userTemp->is_mobile;
$newData['created_at'] = Carbon::now();
$newData['updated_at'] = Carbon::now();
$newData['is_active'] = 1;                              // V2: active ngay, không cần verify email lần 2
$newData['token_active_register'] = null;               // override lại = null
$newData['expire_datetime_active_user'] = null;         // override lại = null
$newData['ip'] = $request->getClientIp();
```

#### Bước 5 — INSERT users

```
$userId = DB::table('users')->insertGetId($newData);
```

Dùng `DB::table` (Query Builder) thay vì `User::create` → bỏ qua model events.

#### Bước 6 — INSERT payment_detail_aff (nếu có affiliate)

```
if ($userIdInvite) {
    PaymentDetailAff::query()->create([
        'admin_id'     => $admin->admin_id ?? 1,
        'user_id'      => $userIdInvite,      // user affiliator
        'type_bill'    => -1,                  // magic value: mark đăng ký mới
        'remain_day'   => 0,
        'bot_name'     => $newData['email'],   // lưu email user mới vào field bot_name
        'user_bill_id' => $userId,             // user mới tạo
    ]);
}
```

#### Bước 7 — INSERT role_access (34 routes)

Mảng `$roleUserNew` chứa 34 route names:
```
chatBasic, index.talk, broadcast.index, scenario.index, index.msg_template,
basicReply, settingAddFriend, form_answer.index, list_event.booking_event,
events.index, booking.manager, tagHome, friendlistHome, friendInformationList,
employeesManagement, errorList, landingIndex, index.conversion, urlHome,
sitescriptHome, richMenu, mediaList, registerInfoAff, managePaymentStatus,
listItemsOld, orderHistory, cycleOrderHistory, affSetting, affResult,
affMemberList, pointSettings, adminSetting, botAdd, backup, notifySetting
```

Với mỗi route:
```
$feature = AccessFeature::where('route', $route)->where('visible', 1)->first();
if ($feature) {
    // Role 1 — super admin của account (luôn có)
    RoleAccess::create(['user_id' => $userId, 'access_id' => $feature->id, 'role_id' => 1]);

    // Role 2 — staff default (loại trừ 10 routes: employeesManagement, botAdd, pointSettings, backup, notifySetting, affSetting, affResult, affMemberList, registerInfoAff, managePaymentStatus)
    if (!in array loại trừ) {
        RoleAccess::create(['user_id' => $userId, 'access_id' => $feature->id, 'role_id' => 2]);
    }

    // Role 3 — chat-only staff (chỉ 3 routes: chatBasic, index.talk, adminSetting)
    if (in chatBasic/index.talk/adminSetting) {
        RoleAccess::create(['user_id' => $userId, 'access_id' => $feature->id, 'role_id' => 3]);
    }
}
```

→ Tối đa `34 × 1 + 24 × 1 + 3 × 1 = 61` INSERT vào `role_access`.

#### Bước 8 — Update affiliate counter + notify emails

```
if ($userIdInvite) {
    $userIntroduce = AffiliateInfo::where('user_id', $userIdInvite)->first();
    if ($userIntroduce) {
        $userIntroduce->update(['count_user_intro' => $userIntroduce->count_user_intro + 1]);

        if ($userIntroduce->is_receive_notification
            && $userIntroduce->when_registered
            && !empty($userIntroduce->emails_receive_notify)
        ) {
            foreach (json_decode($userIntroduce->emails_receive_notify) as $emailAff) {
                MailApiService::sendMailApi([
                    'email'   => $emailAff,
                    'title'   => '【L Message】ご紹介による新規アカウント登録がありました。',
                    'content' => 'emails.registered_user_aff',
                    'params'  => ['userName' => $request->username]
                ]);
            }
        }
    }
}
```

#### Bước 9 — INSERT user_point_settings (trial 30 ngày)

```
UserPointSettings::create([
    'user_id'        => $userId,
    'is_trial'       => true,
    'm_bot'          => 1,
    'require_paypal' => 1,
    'expire_date'    => Carbon::createFromTimestamp(
        strtotime('+30 days', strtotime(date('Y-m-d 23:59:59')))
    ),
]);
```

Tức: expire_date = cuối ngày (23:59:59) của ngày hiện tại + 30 ngày.

#### Bước 10 — Gửi các mail thông báo

```
ActiveAccount::sendMailActiveAccountSuccess(['token' => $token, 'email' => $email]);
    // → MailApiService::sendMailApi template 'emails.active_account_success', subject 'L Message本登録完了のお知らせ'
ActiveAccount::sendMailConfirmUserRegisterToUser(['email' => $email, 'user_name' => $newData['username']]);
    // → Mail::send template 'emails.confirm_admin_user_register' to env('MAIL_ADDRESS_CONFIRM_ADMIN'),
    //   dùng Gmail SMTP riêng (ADMIN_MAIL_*). Subject '自動登録'.
ActiveAccount::sendMailConfirmUserRegisterToUserMASP(['email' => $email, 'user_name' => $newData['username']]);
    // → Mail::send template 'emails.confirm_mysp_admin_user_register' to env('MAIL_ADDRESS_CONFIRM_ADMIN_MASP').
```

#### Bước 11 — Track path_intro

```
$this->countPathIntro($request->pathIntro);
```
(Xem mô tả method `countPathIntro` ở dưới)

#### Bước 12 — Logout nếu đang login + trả response

```
if (Auth::check()) {
    Auth::logout();
}
return response()->json([
    'message'     => '認証メールが送信されました',
    'confirm'     => false,
    'currentStep' => 3
], 200);
```

#### Error handler

```
catch (\Exception $ex) {
    Log::error($ex);
    return response()->json(['errors' => $ex->getMessage()], 422);
}
```

→ Bất kỳ exception nào (vd DB fail, mail timeout) đều trả 422 với exception message — **ăn hết mọi lỗi**. Flow không có DB transaction nên có thể để lại dữ liệu dở nếu fail giữa chừng.

### `AuthController@validateRegister` (line 1049-1229) — Legacy flow

Method cũ dùng cho POST `/register` (form-encoded). Khác với V2:
- Nhận `username`, `password_regist`, `email_regist`, `invite_code`, `introduce_u`, `_token`, `path_intro`
- Tạo user **inactive** (`is_active = config('sns-line.is_active.no')`, `token_active_register = generateRandomString(32)`, `expire_datetime_active_user = now`)
- Gửi mail activate (`ActiveAccount::sendMailActiveAccount`) — user phải click link để active
- Redirect → `route('registerUserSuccess')` thay vì trả JSON

Logic còn lại (payment_detail_aff, role_access 34 routes với role 1/2/3, user_point_settings trial 30 ngày) giống hệt V2.

### `AuthController@saveRegisterUserAff` (line 1343-1527) — Legacy save với affiliate

Giống `validateRegister` nhưng:
- `$userIdInvite` lấy từ path param `user_id` (không phải body `introduce_u`)
- Không có update `affiliate_info.count_user_intro` (riêng `validateRegisterV2` mới có)

### `AuthController@registerUserSuccess` (line 1231-1234)

```
return view('auth.register_user_success_v2');
```

### `AuthController@redirectRegist` (line 1273-1293)

User click link từ email xác thực:
1. `UserTemporary::where('code', $token)->first()` — nếu null → view `auth.active_user_error`
2. `User::where('email', $userTemp->email)->where('is_active', 1)->first()` — nếu có → view `auth.active_user_error`
3. Nếu `$userTemp->created_at->diffInHours(now()) >= 24` → view `auth.active_user_success` với `['active' => false, 'email' => $userTemp->email]`
4. Ngược lại → view `auth.register_user_v2` với `$userTemp`, `$uCode`, `$pathIntro`, `$referer = ''`

### `AuthController@countPathIntro` (line 1022-1047) — Helper tracking

```
$listPathIntro = PathIntroData::query()->get();
foreach ($listPathIntro as $item) {
    if (
        ($item->url_type == PathIntroData::URL_TYPE_PARTIAL && Str::contains($pathIntro, $item->url))
        || ($item->url_type == PathIntroData::URL_TYPE_CORRECT && $pathIntro == $item->url)
    ) {
        $item->increment('count_user');
    }
}
```

- `URL_TYPE_PARTIAL = 1`: match partial (contains)
- `URL_TYPE_CORRECT = 2`: match exact

Error được catch và log, không throw.

---

## Models Eloquent

Tất cả nằm trực tiếp trong namespace `App` (không có subfolder `Models/` trong repo này).

### `App\User` (file `app/User.php`, extends `Authenticatable implements JWTSubject`)

- Table: `users`
- `$guarded = []` (mass assignable toàn bộ)
- Hidden: `['password', 'remember_token']`
- Constants: `ROLE_ADMIN = -1`, `ROLE_USER = 0`, `ROLE_STAFF = 2`
- Traits: `Notifiable`, `HasPushSubscriptions`
- Relationships liên quan:
  - `roleAccess() → hasMany('App\RoleAccess', 'user_id', 'id')`
  - `introducer1() → belongsTo(User::class, 'user_introduce')`
  - `introducer2() → belongsTo(User::class, 'user_introduce_2')`
  - `getIntroducerAttribute()` — return introducer1 nếu `allow_accept_aff === 1`, else introducer2
  - `firstBot() → hasOne(Bots::class, 'admin_id', 'id')`
- Static: `generateKeyLogin()` (không dùng trong feature này)

### `App\UserTemporary` (file `app/UserTemporary.php`)

- Table: **`user_temporary`** (singular — lưu ý khác convention Laravel)
- `$fillable = ['email', 'code', 'is_mobile']` (không có `path_intro` trong fillable nhưng vẫn được gán qua update thuộc tính)
- Extends `Illuminate\Database\Eloquent\Model`

### `App\RoleAccess` (file `app/RoleAccess.php`)

- Table: **`role_access`** (singular)
- `$guarded = []`
- `$timestamps = true`
- Relationships:
  - `role() → belongsTo('App\Role', 'role_id', 'id')`
  - `accessFeature() → belongsTo('App\AccessFeature', 'access_id', 'id')`
  - `user() → belongsTo('App\User', 'user_id', 'id')`

### `App\AccessFeature` (file `app/AccessFeature.php`)

- Table: **`access_feature`** (singular)
- `$guarded = []`
- `$timestamps = true`
- Columns dùng trong feature: `route` (string, route name), `visible` (boolean)
- Relationships: `roleAccess() → hasMany('App\RoleAccess', 'access_id', 'id')`

### `App\PaymentDetailAff` (file `app/PaymentDetailAff.php`)

- Table: `payment_detail_aff`
- `$guarded = []`
- Relationships: `firstBot()`, `userBill()`, `affInfo()` (hasOne AffiliateInfo bằng user_id)
- Có scope `scopeTypeBill` (không dùng trong feature register)

### `App\UserPointSettings` (file `app/UserPointSettings.php`)

- Table: `user_point_settings`
- `$guarded = []`
- `$timestamps = true`
- Columns dùng trong feature: `user_id`, `is_trial`, `m_bot`, `require_paypal`, `expire_date`
- Static helpers: `isExpired($expire_date)` — có check `+6 hours` offset (timezone?)

### `App\AffiliateInfo` (file `app/AffiliateInfo.php`)

- Table: `affiliate_info`
- `$guarded = []`
- Columns dùng trong feature: `user_id`, `count_user_intro`, `is_receive_notification`, `when_registered`, `emails_receive_notify` (JSON string array)
- Relationships: `user()`, `payment_detail_aff()`, `affMonthBill()`

### `App\PathIntroData` (file `app/PathIntroData.php`)

- Table: `path_intro_data`
- `$guarded = []`
- Soft deletes
- Columns dùng trong feature: `url`, `url_type` (1=PARTIAL, 2=CORRECT), `count_user`
- Constants: `URL_TYPE_PARTIAL = 1`, `URL_TYPE_CORRECT = 2`

### `App\Bots` (file `app/Bots.php`) — chỉ dùng ở flow `/check-user` (không thuộc pipeline register)

Không phân tích ở đây.

---

## Services / Mailers / Helpers

### `App\Mail\MailApiService` (file `app/Mail/MailApiService.php`)

- `sendMailApi($data, $type = null)`:
  - Render view `$data['content']` với `$data['params']` (nếu có) → lấy HTML
  - Nếu `env('TYPE_SEND_MAIL', 'default') == 'default'` → `sendMailDefault()` (SMTP trực tiếp qua Swift_Mailer với timeout 2s + `SmtpTimeoutPlugin`)
  - Ngược lại → `sendMailApiChild()` (POST đến `env('EMAIL_API_URL')` với headers `email-token`)
  - Fallback: nếu `sendMailDefault` lỗi + `env('TYPE_RESEND_TIMEOUT') == 'google'` → `reSendMailCommon` (SMTP Gmail `RESEND_MAIL_*`)
- `reSendMailCommon($email, $title, $content)`: SMTP Gmail — dùng trong `reSendMailRedirectRegist`

### `App\Mail\ActiveAccount` (file `app/Mail/ActiveAccount.php`, extends Mailable)

- `sendMailRedirectRegist($token, $email, $pathIntro, $hashUserId)` — **comment out trong `sendMail`** (line 727), thay bằng `MailApiService::sendMailApi` trực tiếp
- `reSendMailRedirectRegist($token, $email, $pathIntro, $hashUserId)` — render view `emails.redirect_regist`, gọi `MailApiService::reSendMailCommon` (SMTP Gmail)
- `sendMailActiveAccount($data, $type = null)` — gửi link activate tài khoản (template `emails.active_account_register`, subject `【重要】L Message本登録のお願い`). **Dùng ở flow legacy.**
- `sendMailActiveAccountSuccess($data)` — thông báo đăng ký thành công (template `emails.active_account_success`, subject `L Message本登録完了のお知らせ`) — dùng ở V2 sau khi INSERT user
- `sendMailConfirmUserRegisterToUser($data)` — gửi đến email admin (`MAIL_ADDRESS_CONFIRM_ADMIN`) thông báo có user đăng ký (template `emails.confirm_admin_user_register`, subject `自動登録`). SMTP Gmail riêng (`ADMIN_MAIL_*`).
- `sendMailConfirmUserRegisterToUserMASP($data)` — gửi đến email MASP (`MAIL_ADDRESS_CONFIRM_ADMIN_MASP`) (template `emails.confirm_mysp_admin_user_register`, subject `自動登録`). SMTP Gmail riêng.

### `App\Mail\SmtpTimeoutPlugin`

Plugin custom đảm bảo mail không treo quá `MAIL_TIMEOUT` giây (check trước mỗi SMTP command).

### Helpers

- `generateRandomString(32)` — hàm global (helpers) sinh random string 32 char — dùng cho `token_active_register` (flow legacy) và thực tế bị override `= null` sau đó trong V2
- `bcrypt($password)` — hash password
- `Str::random(60)` — sinh token 60 char cho `user_temporary.code`
- `Vinkla\Hashids\Facades\Hashids::decode()` — decode hash ID affiliate
- `Carbon::now()` — timestamps

### Repository

- `App\Repositories\Eloquents\UserRepository` (inject qua `UserRepositoryInterface`):
  - `findById($id)` — `User::where('id', $id)->first()` (hoặc `whereIn` nếu truyền array)
  - `getAdminByInviteCode($inviteCode)` — `User::whereRaw('lower(invite_code) = ?', $inviteCode)->first()` — **dùng ở EP-09 legacy** (không dùng ở V2)

---

## Form Requests / Validation

Không dùng Form Request class riêng — toàn bộ validation dùng `Validator::make(...)` inline trong controller.

### Tổng hợp rule theo endpoint

| Endpoint | Field | Rule | Error message (JP) |
|----------|-------|------|---------------------|
| EP-05 sendMail | `email` | `required|email|unique:users,email` | メールを入力してください。/ メールアドレスに誤りがあります。/ このメールアドレスはすでにエルメに登録済みです。 |
| EP-05 sendMail | `code` | `required|exists:users,invite_code` (non-production & !resend) | 招待コードを入力してください。/ 招待コードをもらった方にご確認ください。 |
| EP-06 typeInformation | `username` | `required|string|max:255` | 名前を入力してください。/ 50文字の名前を入力してください。 |
| EP-06 typeInformation | `company_name` | `required|string|max:255` | 会社名・屋号を入力してください。 |
| EP-06 typeInformation | `phone_number` | `required|regex:/^\d{10,11}$/` | 電話番号を入力してください。/ 電話番号は10から11桁の数字でなければなりません。 |
| EP-07 confirmInformation | `password` | `required|between:6,12` | パスワードを入力してください。/ パスワードは6桁〜12桁の文字を入力してください。。 |
| EP-08 validateRegisterV2 | `username` | `required|max:50` | 名前を入力してください。/ 50文字の名前を入力してください。 |
| EP-08 validateRegisterV2 | `password` | `required|between:6,13` | パスワードを入力してください。/ パスワードは6~13文字で設定してください。 |
| EP-08 validateRegisterV2 | `email` | `required|email|unique:users,email` | メールを入力してください。/ メールの形で入力してください。/ このメールアドレスは既に登録されてます。 |
| EP-09 validateRegister | `username` | `required|max:50` | (giống EP-08) |
| EP-09 validateRegister | `password_regist` | `required|between:6,13` | (giống EP-08) |
| EP-09 validateRegister | `email_regist` | `required|email|unique:users,email` | (giống EP-08) |
| EP-09 validateRegister | `invite_code` | `exists:users,invite_code` (nếu có) | 招待コードをもらった方にご確認ください。 |

### Inconsistency đã phát hiện

- EP-06 rule `max:255` nhưng error message nói "50文字" → mismatch → blade có thể tự set `maxlength="50"` client-side
- EP-07 rule `between:6,12` client-side cũng là 6-12, **nhưng** EP-08 lại là `between:6,13` (server-side) → lệch 1 ký tự
- EP-07 error message có lỗi double chấm "。。" ở cuối

---

## Events / Listeners / Queued Jobs

- **Không dùng** Job class, Queue, hay Event dispatch.
- Mail được gửi **đồng bộ** trong request thông qua `MailApiService::sendMailApi` (có 2 nhánh: SMTP trực tiếp hoặc HTTP API đến `https://mail2026.watermeru.com/email/add-send`).
- `MailApiService` có timeout 2s cho SMTP và 30s cho API; có fallback qua `reSendMailCommon` (Gmail SMTP) nếu mặc định fail.
- Class `ActiveAccount extends Mailable use Queueable, SerializesModels` — có khai báo trait `Queueable` nhưng **không gọi `->queue()` hay `->later()`** — nên các method static vẫn chạy sync.
- **KHÔNG có background job Spring Boot** liên quan (xác nhận: không có job nào trong `src/job/` scan email confirm, không có trigger từ DB change).

---

## Authorization (Policies, Gates)

- **Public** — không có authorization check.
- Không có Policy, Gate, hay middleware `can` nào áp vào các routes này.
- Bảo vệ duy nhất: `VerifyCsrfToken` (Laravel web middleware).

---

## Business Rules

| ID | Rule | Mô tả | Nguồn |
|----|------|-------|-------|
| BR-01 | Email phải unique trong bảng `users` | Rule `unique:users,email` áp dụng cả EP-05 (send mail) và EP-08 (register final). Double-check race condition. | `AuthController.php:673, 834, 1065, 1365` |
| BR-02 | Chỉ DEV/STG mới bắt invite_code | `env('APP_ENV') !== 'production'` AND `type != 'resend'` → bắt `code` exists `users.invite_code`. Cơ chế giới hạn đăng ký môi trường dev/staging. | `AuthController.php:675-677` |
| BR-03 | Token verify email TTL = 24h | `UserTemporary.created_at + 24h` phải > now. Check ở EP-08 và EP-12. | `AuthController.php:807-813, 1283` |
| BR-04 | Chặn spam gửi mail — diffInMinutes > 1 mới resend với kênh khác | Nếu đã gửi mail trước đó và `updated_at` diff > 1 phút → dùng `reSendMailRedirectRegist` (Gmail SMTP). Ngược lại gửi qua `MailApiService` (có thể là API hoặc SMTP mặc định). | `AuthController.php:697-726` |
| BR-05 | Password 6-12 chars (server: 6-12 cho confirm, 6-13 cho register) | Server rule lỏng hơn client-side. Client-side (blade) yêu cầu 4 nhóm ký tự (hoa/thường/số/đặc biệt); server **không check pattern**. | `AuthController.php:772, 833` |
| BR-06 | User mới được trial 30 ngày | `user_point_settings.expire_date = end of today + 30 days`. | `AuthController.php:991-997, 1206-1212, 1504-1510` |
| BR-07 | Max bot mặc định = `env('MAX_BOT', 1)` | User mới được giới hạn số bot theo env. | `AuthController.php:873, 1114, 1402` |
| BR-08 | Affiliate tracking — `user_introduce` vs `user_introduce_2` | Nếu `admin->allow_accept_aff == 1` → lưu vào `users.user_introduce`. Ngược lại → `users.user_introduce_2`. | `AuthController.php:861-865, 1115-1119, 1403-1407` |
| BR-09 | Role mặc định `users.role = 0` (regular user) | Đồng thời INSERT 34 `role_access` cho role_id=1 (super admin của account). 24 trong số đó cũng INSERT role_id=2 (staff). 3 routes (chatBasic, index.talk, adminSetting) INSERT thêm role_id=3 (chat-only staff). | `AuthController.php:870, 902-965, 1144-1205, 1434-1495` |
| BR-10 | Path intro tracking qua bảng `path_intro_data` | URL type 1 (PARTIAL match — Str::contains), type 2 (CORRECT match — equality). Tăng `count_user`. Có soft-delete. Xử lý catch-all exception. | `AuthController.php:1022-1047` |
| BR-11 | Mobile flag thay path_intro | Nếu `userTemp.is_mobile == 1` AND `pathIntro != 1` → thay `https://lme.jp` → `https://lme.jp/sp.html`. | `AuthController.php:867-869` |
| BR-12 | Affiliate: tăng counter + gửi mail notify | Nếu có affiliator và `affiliate_info.is_receive_notification=true` AND `when_registered=true` AND có `emails_receive_notify` (JSON array) → gửi mail đến từng email. | `AuthController.php:966-990` |
| BR-13 | Record `payment_detail_aff` với type_bill=-1 khi đăng ký affiliate | `bot_name = email` (lưu email user mới, không phải bot name thật) — dùng magic value đánh dấu record đăng ký mới. | `AuthController.php:890-900, 1132-1142, 1422-1432` |
| BR-14 | V2 tạo user active ngay (`is_active=1`, `token_active_register=null`) | Khác với legacy flow yêu cầu click link activate. V2 xác thực qua `user_temporary.code` 1 lần là đủ. | `AuthController.php:880-882` |
| BR-15 | Legacy: tạo user inactive + link activate 24h | `is_active=0`, `token_active_register=random(32)`, `expire_datetime_active_user=now`. Click link `/active-ccount/{token}` trong 24h để active. | `AuthController.php:1120-1122, 1302-1306, 1408-1410` |
| BR-16 | Logout nếu đang login khi register V2 | Chặn trường hợp user đã login lại register tài khoản mới — logout session cũ. | `AuthController.php:1004-1006` |
| BR-17 | Không có DB transaction | Logic tạo user, role_access, payment_detail_aff, user_point_settings chạy tuần tự không wrap trong `DB::transaction()` — có thể để dở nếu exception giữa chừng. | `AuthController.php:791-1020` |
| BR-18 | Dùng `DB::table('users')->insertGetId` thay vì Eloquent create | → **Bỏ qua** model events, observers, mutators trên `User`. | `AuthController.php:885, 1126, 1416` |
| BR-19 | Notify MASP & admin khi user đăng ký | Gửi 2 mail đến `MAIL_ADDRESS_CONFIRM_ADMIN` và `MAIL_ADDRESS_CONFIRM_ADMIN_MASP` với template riêng qua Gmail SMTP (`ADMIN_MAIL_*`). | `ActiveAccount.php:173-244` |
| BR-20 | Gửi welcome mail khi V2 register thành công | Template `emails.active_account_success`, subject `L Message本登録完了のお知らせ`. | `ActiveAccount.php:124-135` |

---

## Dữ liệu bị thay đổi (summary)

Trong `validateRegisterV2` (EP-08) — **main write operation**:

| Bảng | Thao tác | Số record (đánh giá) | Điều kiện |
|------|----------|----------------------|-----------|
| `user_temporary` | Đọc (validate token) | 1 | Luôn |
| `users` | INSERT | 1 | Luôn |
| `role_access` | INSERT | 58-61 (34 role_id=1 + ~24 role_id=2 + 3 role_id=3) | Luôn (với điều kiện `access_feature.visible = 1`) |
| `user_point_settings` | INSERT | 1 | Luôn |
| `payment_detail_aff` | INSERT | 1 | Nếu có `$userIdInvite` (affiliate) |
| `affiliate_info` | UPDATE (`count_user_intro++`) | 1 | Nếu có affiliate và có row tương ứng |
| `path_intro_data` | UPDATE (`count_user++`) | 0-N | Nếu `pathIntro` match URL theo rule PARTIAL/CORRECT |
| `user_temporary` | **KHÔNG xoá** | — | Record không bị cleanup (có thể còn sót) |

---

## Đầu ra bên ngoài DB

- 3 email đồng bộ (user / admin / MASP) qua `MailApiService` / Gmail SMTP
- 1 log ActivityLog — **đã comment out** (line 887, 1128, 1418 — code có nhưng bị comment)
- Nếu có affiliate với `is_receive_notification=true` → gửi thêm N email (N = số email trong `emails_receive_notify`)
- Optional: Chatwork notify khi SMTP timeout (trong `MailApiService`)

---

## Endpoints phụ liên quan (tham khảo)

- `POST /account/resend-email` (`resendMailActiveUser`) — gửi lại mail activate cho user inactive (flow legacy)
- `GET /active-ccount/{token}` (`activeAccount`) — click link để activate user inactive (flow legacy)
- `GET /redirect-regist/{token}` (`redirectRegist`) — xem chi tiết ở EP-12

---

## Mức độ tin cậy

- Toàn bộ logic V2 (EP-05 đến EP-08, EP-11): **Cao** — đọc trực tiếp từ source
- Logic legacy (EP-09, EP-10): **Cao**
- Validation rules: **Cao**
- Mail templates (`emails.*`): **Trung bình** — xác nhận tên template nhưng chưa đọc nội dung HTML
- Business rules 1-20: **Cao**
- `ActivityLog` có hoặc không: **Cao** — **đã xác nhận là comment out** trong source, không ghi log activity khi đăng ký
