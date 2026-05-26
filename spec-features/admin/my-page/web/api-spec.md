# [FA-036] Trang ca nhan — API Spec

## Tong quan
- **Ma tinh nang**: FA-036
- **Ten**: Trang ca nhan (「マイページ」)
- **Portal**: Admin
- **Ghi chu**: He thong co **2 phien ban** song song:
  - **Phien ban cu (Legacy)**: URL `/admin/setting` — server-side rendered (Blade), submit form POST truyen thong
  - **Phien ban moi (MyPage)**: URL `/admin/my-page` — Vue.js SPA, giao tiep qua AJAX/JSON API
  - Ca hai cung thao tac tren bang `users` va deu su dung `UserService`

---

## Danh sach Endpoints

### Nhom A: Phien ban moi — MyPage (AJAX API)

| ID | Method | URL | Mo ta | Middleware | Controller |
|----|--------|-----|-------|-----------|------------|
| EP-01 | GET | `/admin/my-page` | Hien thi trang My Page (Blade view) | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@index` |
| EP-02 | GET | `/admin/ajax/my-page/account` | Lay thong tin tai khoan hien tai | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@getAccount` |
| EP-03 | GET | `/admin/ajax/my-page/activity-logs` | Lay lich su hoat dong (phan trang, loc) | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@getActivityLogs` |
| EP-04 | POST | `/admin/ajax/my-page/change-name` | Doi ten tai khoan | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@changeName` |
| EP-05 | POST | `/admin/ajax/my-page/change-company` | Doi ten cong ty | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@changeCompany` |
| EP-06 | POST | `/admin/ajax/my-page/change-phone` | Doi so dien thoai | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@changePhone` |
| EP-07 | POST | `/admin/ajax/my-page/send-email-verification` | Gui ma xac thuc doi email | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@sendEmailVerification` |
| EP-08 | POST | `/admin/ajax/my-page/verify-email-code` | Xac thuc ma va doi email | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@verifyEmailCode` |
| EP-09 | POST | `/admin/ajax/my-page/change-password` | Doi mat khau | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@changePassword` |
| EP-10 | POST | `/admin/ajax/my-page/change-image` | Upload anh dai dien | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@changeImage` |
| EP-11 | POST | `/admin/ajax/my-page/delete-image` | Xoa anh dai dien | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@deleteImage` |
| EP-12 | POST | `/admin/ajax/my-page/delete-account` | Xoa tai khoan (chua hoan thien) | web, NotifyChatworkRequestTimeSlow | `Admin\MyPageController@deleteAccount` |

### Nhom B: Phien ban cu — Legacy Setting

| ID | Method | URL | Mo ta | Middleware | Controller |
|----|--------|-----|-------|-----------|------------|
| EP-13 | GET | `/admin/setting` | Hien thi form cai dat ca nhan (Blade) | web, NotifyChatworkRequestTimeSlow | `Admin\UserController@setting` |
| EP-14 | POST | `/admin/setting/update` | Luu thong tin tai khoan + doi mat khau | web, NotifyChatworkRequestTimeSlow | `Admin\UserController@update` |

### Nhom C: Xoa tai khoan (Legacy — flow hien tai)

| ID | Method | URL | Mo ta | Middleware | Controller |
|----|--------|-----|-------|-----------|------------|
| EP-15 | POST | `/admin/check-auth-delete-account/{id}` | Kiem tra dieu kien xoa (con bot hay khong) | web, NotifyChatworkRequestTimeSlow | `Admin\UserController@checkAuthDeleteAccount` |
| EP-16 | GET | `/admin/auth-delete-account` | Hien thi trang xac thuc xoa tai khoan | web, NotifyChatworkRequestTimeSlow | `Admin\UserController@viewAuthDeleteAccount` |
| EP-17 | POST | `/ajax/send-auth-code` | Gui ma xac thuc (xoa tai khoan / xoa bot / doi email) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | `Admin\TwoFactorVerifyController@sendAuthCode` |
| EP-18 | POST | `/ajax/check-code-auth-delete` | Xac thuc ma va thuc hien hanh dong (xoa tai khoan / doi email) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | `Admin\TwoFactorVerifyController@checkCodeAuthDelete` |
| EP-19 | POST | `/admin/delete-account-myself/{id}` | Thuc hien xoa tai khoan (sau khi xac thuc) | web, NotifyChatworkRequestTimeSlow | `Admin\UserController@deleteAccountMyself` |

### Nhom D: Doi email (Legacy — dung chung)

| ID | Method | URL | Mo ta | Middleware | Controller |
|----|--------|-----|-------|-----------|------------|
| EP-20 | POST | `/ajax/send-change-email-code` | Gui ma xac thuc doi email (API moi) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | `Admin\TwoFactorVerifyController@sendChangeEmailCode` |
| EP-21 | POST | `/ajax/validate-code-change-email` | Xac thuc ma va cap nhat email (API moi) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | `Admin\TwoFactorVerifyController@validateCodeChangeEmail` |

---

## Chi tiet tung Endpoint

### EP-01: GET `/admin/my-page` — Hien thi trang My Page
- **Controller**: `Admin\MyPageController@index` (`app/Http/Controllers/Admin/MyPageController.php:21`)
- **Xac thuc**: Session-based (middleware `web`). Ca Admin va Staff deu truy cap duoc (khong co middleware `supper_admin`). **Do tin cay: Cao**
- **Response**: Blade view `admin.my_page.index` — trang SPA load Vue.js
- **Man hinh**: SCR-MYP-01

---

### EP-02: GET `/admin/ajax/my-page/account` — Lay thong tin tai khoan
- **Controller**: `Admin\MyPageController@getAccount` (`app/Http/Controllers/Admin/MyPageController.php:29`)
- **Request params**: Khong co
- **Response** (JSON):
```json
{
  "success": true,
  "data": {
    "account": {
      "name": "テスト：ゴー・トゥイ・ガン",
      "image": "https://media.example.com/path/to/avatar.jpg",
      "company": "Watermelon Software Solution",
      "email": "ngothuyngan123@gmail.com",
      "phone": "0976870074"
    },
    "action_types": [
      {"value": "all", "label": "全て"},
      {"value": "create", "label": "開始"},
      {"value": "change", "label": "変更"}
    ]
  },
  "message": ""
}
```
- **Logic**: Doc `Auth::user()` → tra ve cac truong `username`, `avatar_path`, `company_name`, `email`, `phone_number`. Neu `avatar_path` co gia tri → noi voi `env('URL_SERVER_MEDIA')`. Dong thoi tra ve danh sach filter options cho activity logs.
- **Do tin cay**: Cao

---

### EP-03: GET `/admin/ajax/my-page/activity-logs` — Lay lich su hoat dong
- **Controller**: `Admin\MyPageController@getActivityLogs` (`app/Http/Controllers/Admin/MyPageController.php:58`)
- **Request params** (query string):

| Param | Kieu | Bat buoc | Mo ta | Mac dinh |
|-------|------|---------|-------|---------|
| `page` | int | Khong | Trang hien tai | 1 |
| `per_page` | int | Khong | So ban ghi/trang | 100 |
| `action_type` | string | Khong | Loc theo loai: `all`, `create`, `change` | (tat ca) |
| `date_from` | string (Y-m-d) | Khong | Loc tu ngay | (khong loc) |
| `date_to` | string (Y-m-d) | Khong | Loc den ngay | (khong loc) |

- **Response** (JSON):
```json
{
  "success": true,
  "data": {
    "logs": [
      {
        "type": "change",
        "title": "ユーザー名変更",
        "date": "2026年03月25日 - 14:30",
        "detail": "Old Name → New Name",
        "detail_label": ""
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 100,
      "last_page": 1,
      "total": 5
    }
  },
  "message": ""
}
```
- **Logic**: Query bang `activity_logs` theo `user_id = Auth::id()`, loc theo `action_type` (neu khong phai `all`), loc theo `date_from`/`date_to` (dung `whereDate`). Sap xep `id DESC`. Phan trang thu cong (offset/limit). Transform qua `ActivityLogResource`.
- **Do tin cay**: Cao

---

### EP-04: POST `/admin/ajax/my-page/change-name` — Doi ten tai khoan
- **Controller**: `Admin\MyPageController@changeName` (`app/Http/Controllers/Admin/MyPageController.php:85`)
- **Request params** (form/JSON):

| Param | Kieu | Bat buoc | Validation | Thong bao loi |
|-------|------|---------|-----------|---------------|
| `name` | string | Co | Khong duoc rong, toi da 50 ky tu (mb_strlen) | 「アカウント名を入力してください。」 / 「アカウント名は50文字以内で入力してください。」 |

- **Response thanh cong** (200):
```json
{"success": true, "data": {"name": "Ten moi"}, "message": "アカウント名を変更しました。"}
```
- **Response loi** (422):
```json
{"success": false, "data": null, "message": "...thong bao loi..."}
```
- **Side effects**: Ghi ActivityLog (action_name=`change_name`, old_value, new_value). Ghi addLogUserAction.
- **Do tin cay**: Cao

---

### EP-05: POST `/admin/ajax/my-page/change-company` — Doi ten cong ty
- **Controller**: `Admin\MyPageController@changeCompany` (`app/Http/Controllers/Admin/MyPageController.php:122`)
- **Request params**:

| Param | Kieu | Bat buoc | Validation | Thong bao loi |
|-------|------|---------|-----------|---------------|
| `company` | string | Co | Khong duoc rong, toi da 255 ky tu (mb_strlen) | 「会社・組織名を入力してください。」 / 「会社・組織名は255文字以内で入力してください。」 |

- **Response thanh cong** (200):
```json
{"success": true, "data": {"company": "Ten cong ty moi"}, "message": "会社・組織名を変更しました。"}
```
- **Side effects**: Ghi ActivityLog (action_name=`change_company`). Ghi addLogUserAction.
- **Do tin cay**: Cao

---

### EP-06: POST `/admin/ajax/my-page/change-phone` — Doi so dien thoai
- **Controller**: `Admin\MyPageController@changePhone` (`app/Http/Controllers/Admin/MyPageController.php:159`)
- **Request params**:

| Param | Kieu | Bat buoc | Validation | Thong bao loi |
|-------|------|---------|-----------|---------------|
| `phone` | string | Co | Khong duoc rong, chi chua so (`/^\d+$/`), 10-11 ky tu | 「電話番号を入力してください。」 / 「数値のみ入力してください。」 / 「電話番号は10文字以上で入力してください。」 |

- **Response thanh cong** (200):
```json
{"success": true, "data": {"phone": "0901234567"}, "message": "電話番号を変更しました。"}
```
- **Side effects**: Ghi ActivityLog (action_name=`change_phone`). Ghi addLogUserAction.
- **Do tin cay**: Cao

---

### EP-07: POST `/admin/ajax/my-page/send-email-verification` — Gui ma xac thuc doi email
- **Controller**: `Admin\MyPageController@sendEmailVerification` (`app/Http/Controllers/Admin/MyPageController.php:205`)
- **Request params**:

| Param | Kieu | Bat buoc | Validation | Thong bao loi |
|-------|------|---------|-----------|---------------|
| `email` | string | Co | Khong duoc rong, dinh dang email hop le (`FILTER_VALIDATE_EMAIL`), khong trung email hien tai, khong trung email da dang ky trong he thong | 「メールアドレスを入力してください。」 / 「有効なメールアドレス形式で入力してください。」 / 「現在のメールアドレスと同じです。」 / 「このアドレスはすでにエルメに登録されておりますので、ご利用いただくことはできません。」 |

- **Response thanh cong** (200):
```json
{"success": true, "data": null, "message": "認証コードを送信しました。メールをご確認ください。"}
```
- **Logic**: Goi `UserService@sendCodeChangeEmail` → tao ma ngau nhien 10 ky tu (`Str::random(10)` + `checkRandomStringAuthCode`), luu vao `users.change_email_auth_code` va `users.time_generate_change_email_auth_code`, gui email qua `SendAuthCode::sendAuthCodeChangeMailUser`. **Ma co hieu luc 24 gio** (kiem tra o buoc verify).
- **Do tin cay**: Cao

---

### EP-08: POST `/admin/ajax/my-page/verify-email-code` — Xac thuc ma va doi email
- **Controller**: `Admin\MyPageController@verifyEmailCode` (`app/Http/Controllers/Admin/MyPageController.php:261`)
- **Request params**:

| Param | Kieu | Bat buoc | Validation | Thong bao loi |
|-------|------|---------|-----------|---------------|
| `email` | string | Co | Email moi can cap nhat | — |
| `code` | string | Co | Khong duoc rong | 「認証コードを入力してください。」 |

- **Response thanh cong** (200):
```json
{"success": true, "data": {"email": "new@example.com"}, "message": "メールアドレスを変更しました。"}
```
- **Response loi** (422):
```json
{"success": false, "data": null, "message": "認証コードが間違っています。"}
```
hoac:
```json
{"success": false, "data": null, "message": "認証コード期限が切れました。再度発行をしてください"}
```
hoac:
```json
{"success": false, "data": null, "message": "メールアドレスは登録済みです。"}
```
- **Logic**: Goi `UserService@validateCodeChangeEmail` voi `$needReLogin = false` (khong bat dang nhap lai). So sanh ma voi `users.change_email_auth_code`, kiem tra het han 24h. Neu hop le → cap nhat `users.email`, xoa `change_email_auth_code`. Dong thoi cap nhat email tren UnivaPay (cac `bot_contracts` co `univa_email` = email cu). Ghi ActivityLog (action_name=`change_email`).
- **Do tin cay**: Cao

---

### EP-09: POST `/admin/ajax/my-page/change-password` — Doi mat khau
- **Controller**: `Admin\MyPageController@changePassword` (`app/Http/Controllers/Admin/MyPageController.php:306`)
- **Request params**:

| Param | Kieu | Bat buoc | Validation | Thong bao loi |
|-------|------|---------|-----------|---------------|
| `current_password` | string | Co | Khong duoc rong | 「現在のパスワードを入力してください。」 |
| `new_password` | string | Co | Khong duoc rong, >= 6 ky tu, chua it nhat 1 ky tu dac biet | 「新しいパスワードを入力してください。」 / 「パスワードは6文字以上で入力してください。」 / 「パスワードには少なくとも1つの特殊文字を含めてください。」 |
| `confirm_password` | string | Co | Khong duoc rong, phai khop voi `new_password` | 「確認パスワードを入力してください。」 / 「確認パスワードが一致しません。」 |

- **Response thanh cong** (200):
```json
{"success": true, "data": null, "message": "パスワードを変更しました。"}
```
- **Response loi** (422):
  - Mat khau hien tai sai: 「現在のパスワードが正しくありません。」
  - Mat khau moi trung voi mat khau hien tai: 「新しいパスワードは現在のパスワードと異なるものを設定してください。」
- **Side effects**: Cap nhat `users.password` (bcrypt). Ghi ActivityLog (action_name=`change_password`). Ghi addLogUserAction.
- **Do tin cay**: Cao

---

### EP-10: POST `/admin/ajax/my-page/change-image` — Upload anh dai dien
- **Controller**: `Admin\MyPageController@changeImage` (`app/Http/Controllers/Admin/MyPageController.php:377`)
- **Request params** (multipart/form-data):

| Param | Kieu | Bat buoc | Validation | Thong bao loi |
|-------|------|---------|-----------|---------------|
| `image` | file | Co | MIME: jpeg, png, gif, webp. Toi da 5MB | 「画像ファイルを選択してください。」 / 「JPG、PNG、GIF、WEBP形式の画像を選択してください。」 / 「画像サイズは5MB以下にしてください。」 |

- **Response thanh cong** (200):
```json
{"success": true, "data": {"image_url": "https://media.example.com/path/to/new-avatar.jpg"}, "message": "アカウント画像を変更しました。"}
```
- **Logic**: Xoa avatar cu (neu co). Upload file moi vao thu muc `{FOLDER_MEDIA}/media/user_avatar/{userId}/`. Cap nhat `users.avatar_path`. Ghi ActivityLog (action_name=`change_avatar`).
- **Do tin cay**: Cao

---

### EP-11: POST `/admin/ajax/my-page/delete-image` — Xoa anh dai dien
- **Controller**: `Admin\MyPageController@deleteImage` (`app/Http/Controllers/Admin/MyPageController.php:424`)
- **Request params**: Khong co
- **Response thanh cong** (200):
```json
{"success": true, "data": null, "message": "アカウント画像を削除しました。"}
```
- **Logic**: Xoa file avatar tren server (neu ton tai). Set `users.avatar_path = null`. Ghi ActivityLog (action_name=`delete_avatar`).
- **Do tin cay**: Cao

---

### EP-12: POST `/admin/ajax/my-page/delete-account` — Xoa tai khoan (CHUA HOAN THIEN)
- **Controller**: `Admin\MyPageController@deleteAccount` (`app/Http/Controllers/Admin/MyPageController.php:443`)
- **Trang thai**: **Chua hoan thien** — luon tra ve loi 422 voi message 「この機能は現在準備中です。」
- **Ghi chu**: Flow xoa tai khoan hien tai van dung phien ban cu (EP-15 → EP-19)
- **Do tin cay**: Cao

---

### EP-13: GET `/admin/setting` — Hien thi form cai dat (Legacy)
- **Controller**: `Admin\UserController@setting` (`app/Http/Controllers/Admin/UserController.php:554`)
- **Response**: Blade view `admin.setting` — form HTML server-side rendered voi thong tin hien tai cua user
- **Man hinh**: SCR-MYP-01 (phien ban cu)
- **Do tin cay**: Cao

---

### EP-14: POST `/admin/setting/update` — Luu thong tin + Doi mat khau (Legacy)
- **Controller**: `Admin\UserController@update` (`app/Http/Controllers/Admin/UserController.php:584`)
- **Request params** (form POST):

| Param | Kieu | Bat buoc | Validation |
|-------|------|---------|-----------|
| `name` | string | Co | `required|max:50` |
| `email` | string | Co | `required|email|unique:users,email,{current_id}` |
| `phone_number` | string | Co | `required|regex:/^\d{10,11}$/` |
| `company_name` | string | Khong | Khong validate |
| `passwordOld` | string | Khong | Kiem tra Hash::check neu co |
| `new_pass` | string | Khong | 6-12 ky tu, regex: `/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{6,12}$/` |
| `confirm_new_pass` | string | Khong | Phai giong `new_pass` |

- **Validation mat khau (chi khi dien)**:
  - Mat khau hien tai sai → 「現在のパスワードが間違っています。」
  - Mat khau moi trong khi da nhap mat khau cu → 「新しいパスワードを入力してください。」
  - Mat khau moi khong dung format → 「英大文字・英小文字・数字・記号それぞれを最低1文字ずつ含む6~12文字のパスワードを入力してください。」
  - Mat khau moi trung voi mat khau hien tai → 「このパスワードは最近使用されています。別のパスワードを指定してください。」
  - Xac nhan mat khau khong khop → flash error

- **Response**: Redirect ve `/admin/setting` voi flash message:
  - Thanh cong (co doi pass): 「パスワードが変更されました」
  - Loi: 「失敗しました。」
  - Validation loi: Redirect voi `errors` object

- **Logic**: Cap nhat `users.username`, `users.company_name`, `users.phone_number`. Neu co mat khau moi → cap nhat `users.password` (bcrypt) va `users.remember_token_reset_pass` (random 20 ky tu — buoc tat ca session khac dang xuat).
- **Do tin cay**: Cao

---

### EP-15: POST `/admin/check-auth-delete-account/{id}` — Kiem tra dieu kien xoa
- **Controller**: `Admin\UserController@checkAuthDeleteAccount` (`app/Http/Controllers/Admin/UserController.php:2413`)
- **Request params**: `{id}` — user ID trong URL
- **Logic**: Kiem tra `bots` table — neu tai khoan con bot dang hoat dong (`is_deleted = 0`) → redirect den trang "khong duoc phep xoa" (`type_view=not_allowed_delete`). Neu khong con bot → redirect den trang "xac thuc xoa" (`type_view=account_deletion`).
- **Response** (JSON):
```json
{"success": true, "url_redirect": "/admin/auth-delete-account?type_view=account_deletion"}
```
hoac:
```json
{"success": true, "url_redirect": "/admin/auth-delete-account?type_view=not_allowed_delete"}
```
- **Do tin cay**: Cao

---

### EP-16: GET `/admin/auth-delete-account` — Trang xac thuc xoa tai khoan
- **Controller**: `Admin\UserController@viewAuthDeleteAccount` (`app/Http/Controllers/Admin/UserController.php:9200`)
- **Query params**: `typeView` (= `not_allowed_delete` hoac `account_deletion`), `userId`, `botId`
- **Response**: Blade view `admin.auth_delete_account`
- **Do tin cay**: Cao

---

### EP-17: POST `/ajax/send-auth-code` — Gui ma xac thuc (da nang)
- **Controller**: `Admin\TwoFactorVerifyController@sendAuthCode` (`app/Http/Controllers/Admin/TwoFactorVerifyController.php:119`)
- **Request params**:

| Param | Kieu | Mo ta |
|-------|------|-------|
| `id` | int | User ID |
| `email` | string | Email (bi override bang email cua user) |
| `type_receiver` | string | Loai: `auth_delete_account`, `auth_delete_bot`, `auth_change_mail_user` |
| `type_alert` | string | `resend` (gui lai) hoac khac |
| `bot_id` | string | Hash ID cua bot (chi cho `auth_delete_bot`) |

- **Logic theo `type_receiver`**:
  - `auth_delete_account`: Tao ma 10 ky tu, luu `users.account_deletion_auth_code` + `users.time_generate_account_deletion_auth_code`, gui email `SendAuthCode::sendAuthCodeDeleteAccount`
  - `auth_delete_bot`: Luu `bots.bot_deletion_auth_code`, gui email `SendAuthCode::sendAuthCodeDeleteBot`
  - `auth_change_mail_user`: Luu `users.change_email_auth_code`, gui email `SendAuthCode::sendAuthCodeChangeMailUser`
- **Response**: `{"status": true, "success": "メールが再送されました"}`
- **Luu y**: Email luon lay tu `user.email` (khong phai param `email`). Ma hieu luc **24 gio**.
- **Do tin cay**: Cao

---

### EP-18: POST `/ajax/check-code-auth-delete` — Xac thuc ma (da nang)
- **Controller**: `Admin\TwoFactorVerifyController@checkCodeAuthDelete` (`app/Http/Controllers/Admin/TwoFactorVerifyController.php:189`)
- **Request params**:

| Param | Kieu | Mo ta |
|-------|------|-------|
| `user_id` | int | User ID |
| `type` | string | `auth_delete_account`, `auth_delete_bot`, `auth_change_mail_user` |
| `code` | string | Ma xac thuc |
| `new_email` | string | Email moi (chi cho `auth_change_mail_user`) |
| `bot_id` | string | Hash ID bot (chi cho `auth_delete_bot`) |

- **Logic**:
  - So sanh `code` voi ma luu trong DB, kiem tra het han 24h
  - Neu `type = auth_change_mail_user` va co `new_email` → kiem tra email trung → cap nhat `users.email`, `users.remember_token_reset_pass`
  - Ma het han → 「認証コード期限が切れました。再度発行をしてください」
  - Ma sai → 「認証コードが間違っています。」
  - Email trung → 「メールアドレスは登録済みです。」
- **Response thanh cong** (doi email): `{"success": "メールアドレスが変更されました", "new_email": "...", "status": true}`
- **Response thanh cong** (xoa): `{"success": "認証コードをメールに送りました。", "status": true}`
- **Do tin cay**: Cao

---

### EP-19: POST `/admin/delete-account-myself/{id}` — Thuc hien xoa tai khoan
- **Controller**: `Admin\UserController@deleteAccountMyself` (`app/Http/Controllers/Admin/UserController.php:2520`)
- **Request params**:

| Param | Kieu | Mo ta |
|-------|------|-------|
| `{id}` | int | User ID (URL param) |
| `note_reason_account_deletion` | string | Ghi chu ly do xoa |
| `array_reason_account_deletion` | array | Danh sach ly do xoa |

- **Security**: Kiem tra `Auth::user()->id == $id` — chi cho phep tu xoa chinh minh
- **Logic xoa (cascade)**:
  1. Xoa staff: `users WHERE admin_id = {id} AND level IS NOT NULL`
  2. Xoa role_access: `role_access WHERE user_id IN [id, staff_ids]`
  3. Xoa affiliate: `affiliaters`, `affiliate_info`, `payment_detail_aff`
  4. Cap nhat `payment_detail_aff` (ghi `bot_name` = username)
  5. Soft-delete bots: `bots SET is_deleted = 1`
  6. Xoa bot_slots, bot_contracts, access_bot
  7. Sync Elasticsearch (delete_bot event cho moi bot)
  8. Xoa user: `users DELETE id = {id}`
  9. Xoa media files (images, thumbnails, pdf, videos, voices) + records
  10. Luu ly do xoa vao `contract_cancel_reason`
  11. Giam `path_intro` (referral tracking)
- **Response thanh cong**: `{"success": true, "message": "削除を受けました。２４時間以内に完了します。"}`
- **Response loi**: `{"success": false, "message": "Delete account false"}` (neu id khong khop) hoac exception message
- **Do tin cay**: Cao

---

### EP-20: POST `/ajax/send-change-email-code` — Gui ma doi email (API moi)
- **Controller**: `Admin\TwoFactorVerifyController@sendChangeEmailCode` (`app/Http/Controllers/Admin/TwoFactorVerifyController.php:279`)
- **Delegate**: `UserService@sendCodeChangeEmail`
- **Request params**: `userId` (int), `email` (string — email moi)
- **Logic**: Tuong tu EP-07 nhung khong co validation email format o controller. Kiem tra email trung trong `UserService`. Tao ma 10 ky tu, luu vao `users.change_email_auth_code`.
- **Response**: `{"success": true, "message": "メールが再送されました"}` hoac `{"success": false, "message": "..."}`
- **Do tin cay**: Cao

---

### EP-21: POST `/ajax/validate-code-change-email` — Xac thuc doi email (API moi)
- **Controller**: `Admin\TwoFactorVerifyController@validateCodeChangeEmail` (`app/Http/Controllers/Admin/TwoFactorVerifyController.php:285`)
- **Delegate**: `UserService@validateCodeChangeEmail` (voi `$needReLogin = true` — mac dinh)
- **Request params**: `userId` (int), `code` (string), `email` (string — email moi)
- **Logic**: Tuong tu EP-08 nhung voi `$needReLogin = true` → cap nhat `remember_token_reset_pass` (buoc logout tat ca session). Dong thoi cap nhat email tren UnivaPay.
- **Response**: `{"success": true}` hoac `{"success": false, "message": "..."}`
- **Do tin cay**: Cao

---

## Lien ket Endpoint ↔ Man hinh

| Man hinh | Endpoints su dung |
|----------|------------------|
| SCR-MYP-01 (Phien ban moi /admin/my-page) | EP-01 (load trang), EP-02 (lay thong tin), EP-03 (lich su), EP-04..EP-06 (doi ten/cong ty/SDT), EP-07..EP-08 (doi email), EP-09 (doi pass), EP-10..EP-11 (avatar), EP-12 (xoa tai khoan) |
| SCR-MYP-01 (Phien ban cu /admin/setting) | EP-13 (load trang), EP-14 (luu form) |
| Trang xoa tai khoan | EP-15 (kiem tra), EP-16 (hien thi xac thuc), EP-17 (gui ma), EP-18 (xac thuc ma), EP-19 (thuc hien xoa) |

---

## Middleware ap dung

| Middleware | Mo ta | Ap dung |
|-----------|-------|---------|
| `web` | Session authentication — kiem tra dang nhap | Tat ca endpoints |
| `NotifyChatworkRequestTimeSlow` | Ghi log request cham vao Chatwork | Tat ca endpoints |
| `LogRequestMultipart` | Log request multipart | EP-17, EP-18, EP-20, EP-21 |
| `supper_admin` | Chi cho phep Super Admin | **KHONG** ap dung cho cac endpoint MyPage — ca Admin va Staff deu truy cap duoc |

---

## Ghi chu kiem tra chua ro (tu UI spec)

| # | Cau hoi | Ket qua kiem tra |
|---|---------|-----------------|
| 1 | Truong email co edit truc tiep duoc khong? | **Khong** (phien ban moi) — phai qua flow gui ma xac thuc (EP-07 → EP-08). Phien ban cu gui email trong form nhung validate `unique:users,email` |
| 2 | Link doi email dan den dau? | Phien ban moi: goi AJAX EP-07. Phien ban cu: co the dung EP-17 (send-auth-code voi type `auth_change_mail_user`) |
| 3 | Form submit thong tin va mat khau chung hay tach? | **Phien ban cu**: chung 1 form POST (EP-14). **Phien ban moi**: tach rieng tung API (EP-04..EP-09) |
| 4 | Xoa tai khoan co confirm dialog? | **Co** — flow EP-15 kiem tra dieu kien → EP-16 hien trang xac thuc → EP-17 gui ma email → EP-18 nhap ma → EP-19 xoa |
| 5 | Staff truy cap duoc khong? | **Co** — khong co middleware `supper_admin` chan. **Do tin cay: Cao** |
| 6 | Truong phone va company co bat buoc? | **Phien ban cu**: phone bat buoc, company khong bat buoc. **Phien ban moi**: ca hai deu bat buoc (validation trong controller). **Do tin cay: Cao** |
