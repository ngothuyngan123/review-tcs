# [FA-036] Trang ca nhan — Logic Spec

## Tong quan
- **Ma tinh nang**: FA-036
- **Ten**: Trang ca nhan (「マイページ」)
- **Portal**: Admin
- **Mo ta**: Logic xu ly cap nhat thong tin ca nhan, doi email (qua xac thuc OTP email), doi mat khau, quan ly avatar, xem lich su hoat dong, va xoa tai khoan.

---

## 1. Controllers & Actions

### 1.1 MyPageController (Phien ban moi — AJAX API)
- **File**: `app/Http/Controllers/Admin/MyPageController.php` (456 dong)
- **Namespace**: `App\Http\Controllers\Admin`
- **Dependency Injection**: `UserService`

| Method | Dong | Logic chinh |
|--------|------|------------|
| `index()` | :21 | Tra ve Blade view `admin.my_page.index`. Khong xu ly logic. |
| `getAccount()` | :29 | Doc `Auth::user()` → map cac truong `username`, `avatar_path`, `company_name`, `email`, `phone_number` thanh JSON. Noi `avatar_path` voi `env('URL_SERVER_MEDIA')`. Lay filter options tu `ActivityLog::getActionTypeFilterOptions()`. |
| `getActivityLogs()` | :58 | Nhan params phan trang va bo loc → delegate cho `UserService@getMyPageActivityLogs`. |
| `changeName()` | :85 | Validate: khong rong, <= 50 ky tu. Delegate cho `UserService@changeMyPageName`. |
| `changeCompany()` | :122 | Validate: khong rong, <= 255 ky tu. Delegate cho `UserService@changeMyPageCompany`. |
| `changePhone()` | :159 | Validate: khong rong, chi so, 10-11 ky tu. Delegate cho `UserService@changeMyPagePhone`. |
| `sendEmailVerification()` | :205 | Validate: khong rong, email hop le, khong trung email hien tai. Merge `userId` → delegate cho `UserService@sendCodeChangeEmail`. |
| `verifyEmailCode()` | :261 | Validate: code khong rong. Merge `userId` → delegate cho `UserService@validateCodeChangeEmail($request, false)` (khong bat re-login). Ghi `ActivityLog` (change_email). |
| `changePassword()` | :306 | Validate: tat ca 3 truong khong rong, mat khau moi >= 6 ky tu, chua ky tu dac biet, confirm khop. Delegate cho `UserService@changeMyPagePassword`. |
| `changeImage()` | :377 | Validate: co file, MIME la jpeg/png/gif/webp, <= 5MB. Delegate cho `UserService@changeMyPageImage`. |
| `deleteImage()` | :424 | Khong validate. Delegate cho `UserService@deleteMyPageImage`. |
| `deleteAccount()` | :443 | **CHUA HOAN THIEN** — luon tra ve 422 voi message 「この機能は現在準備中です。」 |

**Do tin cay**: Cao — doc truc tiep tu source code.

---

### 1.2 UserController (Phien ban cu — Legacy)
- **File**: `app/Http/Controllers/Admin/UserController.php` (9503 dong)
- **Namespace**: `App\Http\Controllers\Admin`

| Method | Dong | Logic chinh |
|--------|------|------------|
| `setting()` | :554 | Tra ve Blade view `admin.setting`. |
| `validateAdmin()` | :559 | Tao Validator voi rules: `email` (required, email, unique), `name` (required, max:50), `confirm_new_pass` (same:new_pass), `phone_number` (required, regex 10-11 so). Tra ve Validator instance. |
| `update()` | :584 | Goi `validateAdmin()` → neu fail redirect voi errors. Xu ly mat khau: kiem tra mat khau cu (Hash::check), validate format mat khau moi (regex 6-12 ky tu, chua chu hoa + chu thuong + so + ky tu dac biet), kiem tra khong trung mat khau cu, kiem tra confirm. Cap nhat bang `users` truc tiep qua `DB::table('users')`. Neu co mat khau moi → luu `password` (bcrypt) + `remember_token_reset_pass` (random 20 ky tu). |
| `checkAuthDeleteAccount()` | :2413 | Kiem tra `bots WHERE admin_id = {id} AND is_deleted = 0`. Neu con bot → redirect `type_view=not_allowed_delete`. Neu het bot → redirect `type_view=account_deletion`. |
| `viewAuthDeleteAccount()` | :9200 | Tra ve Blade view `admin.auth_delete_account` voi params `typeView`, `userId`, `botId`. |
| `deleteAccountMyself()` | :2520 | Security: `Auth::user()->id == $id`. Xoa cascade: staff → role_access → affiliaters → affiliate_info → payment_detail_aff (update rồi xóa) → soft-delete bots → xoa bot_slots, bot_contracts, access_bot → sync Elasticsearch → xoa user → xoa media files & records → luu ly do xoa vao `contract_cancel_reason` → giam path_intro. |

**Do tin cay**: Cao — doc truc tiep tu source code.

---

### 1.3 TwoFactorVerifyController (Xac thuc OTP)
- **File**: `app/Http/Controllers/Admin/TwoFactorVerifyController.php` (291 dong)
- **Namespace**: `App\Http\Controllers\Admin`
- **Dependency Injection**: `UserService`

| Method | Dong | Logic chinh |
|--------|------|------------|
| `sendAuthCode()` | :119 | Nhan `type_receiver` → switch: `auth_delete_account` (luu `account_deletion_auth_code`), `auth_delete_bot` (luu `bot_deletion_auth_code` vao bang `bots`), `auth_change_mail_user` (luu `change_email_auth_code`). Tao ma random 10 ky tu. Gui email tuong ung. **Luu y**: email luon lay tu `user.email`, khong phai param. |
| `checkCodeAuthDelete()` | :189 | Switch theo `type`: doc ma tu DB, kiem tra het han (24h cho tat ca loai). Neu `auth_change_mail_user` + co `new_email` → kiem tra email trung → cap nhat `users.email` + `remember_token_reset_pass`. |
| `sendChangeEmailCode()` | :279 | Delegate cho `UserService@sendCodeChangeEmail`. |
| `validateCodeChangeEmail()` | :285 | Delegate cho `UserService@validateCodeChangeEmail`. |

**Do tin cay**: Cao — doc truc tiep tu source code.

---

## 2. Models Eloquent

### 2.1 User
- **File**: `app/User.php` (suy luan — khong doc truc tiep file nay, thong tin tu models.md va cac controller)
- **Table**: `users`
- **Connection**: `mysql`
- **Cac cot lien quan den FA-036**:

| Cot | Kieu (suy luan) | Mo ta | Su dung boi |
|-----|-----------------|-------|-------------|
| `id` | int (PK) | Ma user | Tat ca |
| `username` | string | Ten hien thi | EP-02, EP-04, EP-14 |
| `email` | string | Email dang ky | EP-02, EP-07, EP-08, EP-14 |
| `password` | string | Mat khau (bcrypt hash) | EP-09, EP-14 |
| `company_name` | string | Ten cong ty | EP-02, EP-05, EP-14 |
| `phone_number` | string | So dien thoai | EP-02, EP-06, EP-14 |
| `avatar_path` | string (nullable) | Duong dan avatar | EP-02, EP-10, EP-11 |
| `admin_id` | int (nullable) | ID admin cha (cho staff) | EP-19 (xoa staff) |
| `level` | int (nullable) | Cap do (null = admin, khac = staff) | EP-19 (phan biet staff) |
| `role` | int | Vai tro (0 = admin, khac = staff/system) | EP-17 |
| `remember_token_reset_pass` | string (nullable) | Token buoc logout cac session khac | EP-08, EP-09, EP-14, EP-21 |
| `change_email_auth_code` | string (nullable) | Ma xac thuc doi email | EP-07, EP-08, EP-17, EP-20, EP-21 |
| `time_generate_change_email_auth_code` | datetime (nullable) | Thoi gian tao ma doi email | EP-07, EP-08, EP-17, EP-20, EP-21 |
| `account_deletion_auth_code` | string (nullable) | Ma xac thuc xoa tai khoan | EP-17, EP-18 |
| `time_generate_account_deletion_auth_code` | datetime (nullable) | Thoi gian tao ma xoa tai khoan | EP-17, EP-18 |
| `max_bot` | int | So bot toi da | EP-19 (lien quan) |
| `path_intro` | string (nullable) | Duong dan gioi thieu (referral) | EP-19 |
| `is_deleted` | int | Co xoa khong (0 = khong) | Kiem tra email trung |

**Do tin cay**: Cao (cot duoc xac nhan qua code controller/service thao tac truc tiep).

### 2.2 ActivityLog
- **File**: `app/Models/ActivityLog.php` (79 dong)
- **Table**: `activity_logs`
- **Connection**: `mysql`
- **Guarded**: `[]` (mass assignable tat ca cot)

| Cot | Kieu | Mo ta |
|-----|------|-------|
| `id` | int (PK) | Auto-increment |
| `user_id` | int (FK → users.id) | User thuc hien hanh dong |
| `action_type` | string | Loai: `create`, `change` |
| `action_name` | string | Ten hanh dong: `change_name`, `change_company`, `change_phone`, `change_email`, `change_password`, `change_avatar`, `delete_avatar`, `create_user`, `add_loa` |
| `old_value` | string (nullable) | Gia tri cu |
| `new_value` | string (nullable) | Gia tri moi |
| `description` | string (nullable) | Mo ta them |
| `created_at` | datetime | Thoi gian |
| `updated_at` | datetime | — |

**Constants**:
- `ACTION_CHANGE_NAME = 'change_name'` → 「ユーザー名変更」
- `ACTION_CHANGE_COMPANY = 'change_company'` → 「会社・組織名 変更」
- `ACTION_CHANGE_PHONE = 'change_phone'` → 「電話番号変更」
- `ACTION_CHANGE_EMAIL = 'change_email'` → 「メールアドレス変更」
- `ACTION_CHANGE_PASSWORD = 'change_password'` → 「パスワード変更」
- `ACTION_CHANGE_AVATAR = 'change_avatar'` → 「アカウント画像変更」
- `ACTION_DELETE_AVATAR = 'delete_avatar'` → 「アカウント画像削除」
- `ACTION_CREATE_USER = 'create_user'` → 「L Messageアカウント登録」
- `ACTION_ADD_LOA = 'add_loa'` → 「LINE公式アカウント接続」

**TYPE_CREATE = 'create'**, **TYPE_CHANGE = 'change'**

**Static methods**:
- `log($userId, $actionType, $actionName, $oldValue, $newValue, $description)` — tao ban ghi activity log
- `getActionTypeFilterOptions()` — tra ve danh sach filter: all/create/change

**Relationships**: `user()` → `belongsTo(User::class)`

**Do tin cay**: Cao — doc truc tiep tu source code.

### 2.3 Cac bang lien quan khac (xoa tai khoan cascade)

| Bang | Vai tro trong FA-036 |
|------|---------------------|
| `bots` | Kiem tra con bot truoc khi xoa. Soft-delete (`is_deleted = 1`) khi xoa tai khoan |
| `bot_slots` | Xoa khi xoa tai khoan |
| `bot_contracts` | Xoa khi xoa tai khoan. Cap nhat `univa_email` khi doi email |
| `access_bot` | Xoa khi xoa tai khoan |
| `role_access` | Xoa khi xoa tai khoan |
| `affiliaters` | Xoa khi xoa tai khoan |
| `affiliate_info` | Xoa khi xoa tai khoan |
| `payment_detail_aff` | Cap nhat rồi xoa khi xoa tai khoan |
| `media` | Xoa files + records khi xoa tai khoan |
| `contract_cancel_reason` | Luu ly do xoa tai khoan |
| `sync_elasticsearch` | Sync event xoa bot |

**Do tin cay**: Cao — doc truc tiep tu source code.

---

## 3. Services

### 3.1 UserService
- **File**: `app/Services/UserService.php` (371 dong)
- **Namespace**: `App\Services`
- **Dependency Injection**: `UserRepositoryInterface`

| Method | Dong | Mo ta | Input | Output |
|--------|------|-------|-------|--------|
| `sendCodeChangeEmail($request)` | :28 | Gui ma xac thuc doi email | `userId`, `email` | `{success, message}` |
| `validateCodeChangeEmail($request, $needReLogin)` | :66 | Xac thuc ma + doi email | `userId`, `code`, `email` | `{success, message}` |
| `changeMyPageName($userId, $name)` | :181 | Doi ten | userId, name | `{success, data, message}` |
| `changeMyPageCompany($userId, $company)` | :200 | Doi ten cong ty | userId, company | `{success, data, message}` |
| `changeMyPagePhone($userId, $phone)` | :219 | Doi SDT | userId, phone | `{success, data, message}` |
| `changeMyPagePassword($userId, $currentPassword, $newPassword)` | :238 | Doi mat khau | userId, currentPassword, newPassword | `{success, data, message}` |
| `changeMyPageImage($userId, $file)` | :264 | Upload avatar | userId, UploadedFile | `{success, data, message}` |
| `deleteMyPageImage($userId)` | :305 | Xoa avatar | userId | `{success, data, message}` |
| `getMyPageActivityLogs($userId, $page, $perPage, $actionType, $dateFrom, $dateTo)` | :328 | Lay activity logs co phan trang + loc | userId + params | `{success, data, message}` |

**Chi tiet logic quan trong**:

#### `sendCodeChangeEmail` (dong 28-64):
1. Tim user qua `userRepository.findById`
2. Kiem tra email trung: `userRepository.checkExistEmail` → loi 「このアドレスはすでにエルメに登録されておりますので、ご利用いただくことはできません。」
3. Tao ma: `Str::random(10)` + `checkRandomStringAuthCode` (helper function)
4. Luu: `change_email_auth_code` + `time_generate_change_email_auth_code` = `now()`
5. Gui email: `SendAuthCode::sendAuthCodeChangeMailUser($email, $code)`

#### `validateCodeChangeEmail` (dong 66-174):
1. Tim user, lay `change_email_auth_code` va `time_generate_change_email_auth_code`
2. Kiem tra email trung (lan nua)
3. So sanh ma: neu khop → kiem tra het han (24h). Neu khong khop → loi
4. Cap nhat: `email`, xoa `change_email_auth_code` + `time_generate_change_email_auth_code`
5. Neu `$needReLogin = true` → cap nhat `remember_token_reset_pass` (buoc logout)
6. **Cap nhat UnivaPay**: Tim `bot_contracts` co `univa_email` = email cu → goi PATCH UnivaPay API de cap nhat email tren he thong thanh toan
7. Cap nhat `bot_contracts.univa_email` = email moi

#### `changeMyPagePassword` (dong 238-259):
1. Kiem tra mat khau hien tai: `Hash::check($currentPassword, $user->password)`
2. Kiem tra mat khau moi khong trung cu: `Hash::check($newPassword, $user->password)`
3. Cap nhat: `password` = `bcrypt($newPassword)`
4. Ghi ActivityLog

#### `changeMyPageImage` (dong 264-300):
1. Xoa avatar cu (neu co file tren disk)
2. Upload moi vao `{FOLDER_MEDIA}/media/user_avatar/{userId}/`
3. Cap nhat `users.avatar_path`
4. Tra ve `image_url` = `env('URL_SERVER_MEDIA') . $avatarPath`

**Do tin cay**: Cao — doc truc tiep tu source code.

### 3.2 UserRepository
- **File**: `app/Repositories/Eloquents/UserRepository.php`
- **Interface**: `App\Contracts\Repositories\UserRepositoryInterface`

| Method | Mo ta |
|--------|-------|
| `findById($id)` | Tim user theo ID. Neu `$id` la array → tra ve list `[id, name]`. Neu scalar → tra ve object |
| `updateUser($id, $data)` | `User::where('id', $id)->update($data)` |
| `checkExistEmail($email)` | `User::where('email', $email)->where('is_deleted', 0)->exists()` |

**Do tin cay**: Cao — doc truc tiep tu source code.

---

## 4. Form Requests / Validation

**Khong su dung Form Request classes**. Tat ca validation duoc thuc hien inline trong controller:

### Phien ban moi (MyPageController) — validation trong tung method:

| Method | Rule | Thong bao loi (JP) |
|--------|------|-------------------|
| `changeName` | required, max 50 ky tu (mb_strlen) | 「アカウント名を入力してください。」「アカウント名は50文字以内で入力してください。」 |
| `changeCompany` | required, max 255 ky tu (mb_strlen) | 「会社・組織名を入力してください。」「会社・組織名は255文字以内で入力してください。」 |
| `changePhone` | required, chi so (`/^\d+$/`), 10-11 ky tu | 「電話番号を入力してください。」「数値のみ入力してください。」「電話番号は10文字以上で入力してください。」 |
| `sendEmailVerification` | required, email hop le (FILTER_VALIDATE_EMAIL), khong trung email hien tai | 「メールアドレスを入力してください。」「有効なメールアドレス形式で入力してください。」「現在のメールアドレスと同じです。」 |
| `verifyEmailCode` | code required | 「認証コードを入力してください。」 |
| `changePassword` | current_password required; new_password required, >= 6 ky tu, chua ky tu dac biet (`/[^a-zA-Z0-9]/`); confirm_password required, khop voi new_password | 「現在のパスワードを入力してください。」「新しいパスワードを入力してください。」「パスワードは6文字以上で入力してください。」「パスワードには少なくとも1つの特殊文字を含めてください。」「確認パスワードを入力してください。」「確認パスワードが一致しません。」 |
| `changeImage` | file required, MIME in [jpeg, png, gif, webp], <= 5MB | 「画像ファイルを選択してください。」「JPG、PNG、GIF、WEBP形式の画像を選択してください。」「画像サイズは5MB以下にしてください。」 |

### Phien ban cu (UserController@validateAdmin) — Laravel Validator:

| Field | Rule | Thong bao loi (JP) |
|-------|------|-------------------|
| `name` | `required|max:50` | 「管理者名を入力してください。」「50以下文字の名前を入力してください。」 |
| `email` | `required|email|unique:users,email,{current_id}` | (comment out — khong hien thi loi email) |
| `phone_number` | `required|regex:/^\d{10,11}$/` | 「電話番号を入力してください。」「電話番号は10から11桁の数字でなければなりません。」 |
| `confirm_new_pass` | `same:new_pass` | 「新しいパスワードとその確認入力内容が異なっています」 |

### Phien ban cu — Validation mat khau bo sung (trong update method, dong 602-645):
- Mat khau cu sai → 「現在のパスワードが間違っています。」
- Nhap mat khau cu nhung mat khau moi trong → 「新しいパスワードを入力してください。」
- Mat khau moi khong dung format (regex: `^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{6,12}$`) → 「英大文字・英小文字・数字・記号それぞれを最低1文字ずつ含む6~12文字のパスワードを入力してください。」
- Mat khau moi trung voi mat khau hien tai → 「このパスワードは最近使用されています。別のパスワードを指定してください。」
- Nhap mat khau moi nhung khong nhap mat khau cu → 「パスワードを入力してください」

**Ghi chu**: Phien ban cu co **validation mat khau chat hon** (6-12 ky tu, yeu cau chu hoa + chu thuong + so + ky tu dac biet). Phien ban moi chi yeu cau >= 6 ky tu va co it nhat 1 ky tu dac biet.

**Do tin cay**: Cao — doc truc tiep tu source code.

---

## 5. Events / Listeners / Jobs

### Khong su dung Laravel Events/Listeners/Jobs truc tiep cho FA-036.

Thay vao do:
- **Email gui qua Mail classes** (static methods):
  - `SendAuthCode::sendAuthCodeChangeMailUser($email, $code)` — gui ma doi email
  - `SendAuthCode::sendAuthCodeDeleteAccount($email, $code)` — gui ma xoa tai khoan
  - `ActiveAccount::sendMailCodeVerifyAdmin(...)` — gui ma xac thuc 2FA (khac flow)

- **Elasticsearch sync** (trong xoa tai khoan):
  - `SyncElasticsearch::insertElasticsearch(...)` — ghi event xoa bot vao bang `sync_elasticsearch` de background job xu ly

- **Activity Logging**:
  - `ActivityLog::log(...)` — ghi vao bang `activity_logs`
  - `addLogUserAction(...)` — helper function ghi log hanh dong (ngoai `activity_logs`)

**Do tin cay**: Cao

---

## 6. Business Rules (tong hop)

### BR-01: Doi ten tai khoan
- **File**: `app/Http/Controllers/Admin/MyPageController.php:85-117`, `app/Services/UserService.php:181-195`
- Ten khong duoc rong, toi da 50 ky tu
- Ghi lich su thay doi (old → new)

### BR-02: Doi ten cong ty
- **File**: `app/Http/Controllers/Admin/MyPageController.php:122-154`, `app/Services/UserService.php:200-214`
- Khong duoc rong, toi da 255 ky tu
- Ghi lich su thay doi

### BR-03: Doi so dien thoai
- **File**: `app/Http/Controllers/Admin/MyPageController.php:159-199`, `app/Services/UserService.php:219-233`
- Chi chua so, 10-11 ky tu
- Ghi lich su thay doi

### BR-04: Doi email (flow 2 buoc)
- **File**: `app/Http/Controllers/Admin/MyPageController.php:205-301`, `app/Services/UserService.php:28-174`
- Buoc 1: Gui ma xac thuc den **email hien tai** (khong phai email moi)
- Buoc 2: Nhap ma xac thuc → kiem tra hop le → doi email
- Ma xac thuc: random 10 ky tu, hieu luc **24 gio**
- Kiem tra email moi khong trung voi email da dang ky (ca khi gui ma va khi xac thuc)
- Sau khi doi email → cap nhat email tren **UnivaPay** (he thong thanh toan) cho cac `bot_contracts` lien quan
- Phien ban moi (`$needReLogin = false`): khong bat dang nhap lai
- Phien ban cu (`$needReLogin = true`): cap nhat `remember_token_reset_pass` → buoc tat ca session khac dang xuat

### BR-05: Doi mat khau
- **File**: `app/Http/Controllers/Admin/MyPageController.php:306-372`, `app/Services/UserService.php:238-259`
- Phai nhap dung mat khau hien tai
- Mat khau moi khong duoc trung voi mat khau hien tai
- **Phien ban moi**: >= 6 ky tu, co it nhat 1 ky tu dac biet
- **Phien ban cu**: 6-12 ky tu, phai co chu hoa + chu thuong + so + ky tu dac biet (regex: `^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{6,12}$`)
- Mat khau luu dang bcrypt hash

### BR-06: Quan ly avatar
- **File**: `app/Http/Controllers/Admin/MyPageController.php:377-437`, `app/Services/UserService.php:264-323`
- Cho phep upload JPEG, PNG, GIF, WEBP, toi da 5MB
- Luu vao thu muc `{FOLDER_MEDIA}/media/user_avatar/{userId}/`
- Khi upload moi → xoa file cu truoc
- Khi xoa → set `avatar_path = null` va xoa file tren disk
- Ghi lich su thay doi

### BR-07: Xoa tai khoan (flow hien tai — Legacy)
- **File**: `app/Http/Controllers/Admin/UserController.php:2413-2648`
- **Dieu kien tien quyet**: Tai khoan **khong duoc con bot dang hoat dong** (`bots.is_deleted = 0`). Neu con bot → khong cho xoa, hien trang thong bao
- **Xac thuc**: Gui ma OTP qua email → nhap ma de xac nhan
- **Security**: Chi cho phep tu xoa tai khoan cua minh (`Auth::user()->id == $id`)
- **Cascade delete** (thu tu):
  1. Xoa toan bo staff cua admin (`users WHERE admin_id = {id}`)
  2. Xoa role_access
  3. Xoa affiliaters, affiliate_info, payment_detail_aff
  4. Soft-delete bots (`is_deleted = 1`)
  5. Xoa bot_slots, bot_contracts, access_bot
  6. Sync xoa bot len Elasticsearch
  7. Xoa user record
  8. Xoa media files (images, thumbnails, pdf, videos, voices) + DB records
  9. Luu ly do xoa vao `contract_cancel_reason` (voi `type_cancel = config('sns-line.type_reason_cancel.user')`)
  10. Giam `path_intro` (referral counter)
- **Message thanh cong**: 「削除を受けました。２４時間以内に完了します。」 (goi y co xu ly bat dong bo bo sung)

### BR-08: Lich su hoat dong (Activity Logs)
- **File**: `app/Http/Controllers/Admin/MyPageController.php:58-80`, `app/Services/UserService.php:328-371`
- Ghi lai moi thay doi: doi ten, doi cong ty, doi SDT, doi email, doi mat khau, doi avatar, xoa avatar
- Ho tro loc theo loai (`create`/`change`) va khoang thoi gian
- Phan trang: mac dinh 100 ban ghi/trang, sap xep moi nhat truoc
- Hien thi: loai, tieu de, ngay gio, chi tiet thay doi (old → new)
- Dac biet: dang ky tai khoan (`create_user`) hien thi `detail_label = 'メールアドレス:'`

### BR-09: Hai phien ban song song
- **File**: `MyPageController.php` (moi) va `UserController.php` (cu)
- He thong **dang chuyen doi** tu phien ban cu (`/admin/setting`) sang phien ban moi (`/admin/my-page`)
- Phien ban cu: form POST truyen thong, luu tat ca 1 lan, server-side rendering
- Phien ban moi: AJAX API rieng tung truong, Vue.js SPA, ho tro avatar + activity logs
- Ca hai van hoat dong song song
- Phien ban moi co them chuc nang: avatar, activity logs, validation tung API rieng
- Phien ban moi chua hoan thien chuc nang xoa tai khoan (luon tra ve 422)

**Do tin cay**: Cao — tat ca business rules duoc xac nhan qua source code.

---

## 7. Cac ban lien quan khac

| Bang | Vai tro | Khi nao truy cap |
|------|---------|-----------------|
| `bot_contracts` | Luu thong tin hop dong bot + email thanh toan UnivaPay | Doi email → cap nhat `univa_email` |
| `sync_elasticsearch` | Queue sync du lieu len Elasticsearch | Xoa tai khoan → sync xoa bot |
| `contract_cancel_reason` | Luu ly do xoa tai khoan | Xoa tai khoan |
| `login_history` | Lich su dang nhap | Khong truc tiep, nhung lien quan user |

---

## 8. Cac helper function duoc su dung

| Function | File (suy luan) | Mo ta |
|----------|----------------|-------|
| `addLogUserAction($message)` | `app/Helpers/functions.php` | Ghi log hanh dong user (ngoai ActivityLog) |
| `uploadFile($file, $name, $dir)` | `app/Helpers/functions.php` | Upload file len server, tra ve duong dan |
| `deleteDir($path)` | `app/Helpers/functions.php` | Xoa thu muc va toan bo file ben trong |
| `checkRandomStringAuthCode($code)` | `app/Helpers/functions.php` | Kiem tra/xu ly ma xac thuc random |

**Do tin cay**: Trung binh — ten function xac nhan qua code, nhung chua doc file helper truc tiep.
