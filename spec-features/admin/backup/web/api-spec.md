# FA-033「データコピー」— API Spec

**Feature**: データコピー (Data Copy)
**Portal**: Admin
**Ngày tạo**: 2026-03-30
**Nguồn**: `app/Http/Controllers/Basic/BasicController.php`, `app/Http/Controllers/Admin/BotController.php`

---

## Danh sách Endpoints

| EP | Method | URL | Controller | Route Name | Mô tả |
|----|--------|-----|-----------|------------|-------|
| EP-01 | GET | `/basic/backup` | `Basic\BasicController@backup` | `backup` | Hiển thị trang データコピー |
| EP-02 | POST | `/basic/backup/export-zip` | `Basic\BasicController@backupStore` | `backup.store` | Đăng ký yêu cầu sao chép dữ liệu |
| EP-03 | POST | `/ajax/check-transfer-code` | `Admin\BotController@checkTransferCode` | `check.transfer.code` | Kiểm tra mã nhận dữ liệu (AJAX) |

> **Lưu ý**: Route `POST /api/backup` → `Api\RichmenuApiController@buildRichmenu` (route name `buildRichmenu`) **không liên quan** đến tính năng データコピー — đây là API xây dựng rich menu, tên route trùng nhưng controller khác.

---

## Middleware áp dụng

Tất cả 3 endpoints áp dụng middleware stack:
- `web` — Session, CSRF, cookie, auth session
- `NotifyChatworkRequestTimeSlow` — Ghi log khi request chậm
- `LogRequestMultipart` — Ghi log request multipart

**Xác thực**: Session-based auth (`basic_access`). Người dùng phải đăng nhập và có bot được chọn trong session (`current_bot_id`).

---

## Chi tiết Endpoints

---

### EP-01: GET `/basic/backup`

**Mô tả**: Hiển thị trang データコピー với form nhập mã nhận dữ liệu và bảng lịch sử sao chép.

**Controller**: `app/Http/Controllers/Basic/BasicController.php:1230`

**Request**: Không có params

**Response**: HTML view `basic.backup_new`

**Dữ liệu truyền vào view**:

| Biến | Nguồn | Mô tả |
|------|-------|-------|
| `folderTags` | `Category` (kind=tag, is_deleted=0) | Danh sách folder tag theo bot |
| `listTagFolderDefault` | `Tag` (category_id=0) | Tag không thuộc folder |
| `scenarioList` | `ScenarioRepository@findByBot` | Danh sách scenario |
| `folderTemplates` | `Category` (kind=template, is_deleted=0) | Folder template |
| `templateListFolderDefault` | `Template` (category_id=0, in_park=0) | Template không thuộc folder |
| `folderFormanswer` | `FormAnswerFolder` with formanswers | Folder form answer |
| `formAnswerListFolderDefault` | `FormAnswer` (group_id=0) | Form answer không thuộc folder |
| `folderAutoReply` | `Category` (kind=reply, is_deleted=0) | Folder tự động trả lời |
| `autoReplyListFolderDefault` | `AutoReply` (category_id=0, is_deleted=0) | AutoReply không thuộc folder |
| `richMenuList` | `RichMenuRepository@getRichMenuByBotId` | Danh sách rich menu |
| `remindList` | `Events` (bot_id) | Danh sách remind |
| `bookingList` | `BEventDetail` (bot_id) | Danh sách booking event |
| `backupHistory` | `BackupHistory` (bot_id, desc created_at) | Lịch sử sao chép |
| `plan_type` | `Bots.plan_type` | Loại plan của bot |

**Lỗi có thể xảy ra**: Redirect về trang login nếu chưa xác thực.

**Liên kết UI**: SCR-01 (trang chính データコピー)

---

### EP-02: POST `/basic/backup/export-zip`

**Mô tả**: Đăng ký yêu cầu sao chép dữ liệu từ LOA hiện tại sang LOA đích (theo mã nhận dữ liệu). Tạo bản ghi `backup_history` với trạng thái chờ xử lý.

**Controller**: `app/Http/Controllers/Basic/BasicController.php:1277`

**Request Params** (form POST):

| Param | Type | Required | Validation | Mô tả |
|-------|------|----------|------------|-------|
| `transfer_code` | string | Có | `required`, `exists:bots` | Mã nhận dữ liệu của LOA đích |
| `_token` | string | Có | CSRF token | CSRF protection |

**Validation Rules** (`Validator::make`):

```php
'transfer_code' => 'required|exists:bots'
```

**Thông báo lỗi validation**:

| Rule | Thông báo (JP) |
|------|---------------|
| `transfer_code.required` | `が必要です。` |
| `transfer_code.exists` | `バックアップコードが存在しません。` |

**Request mẫu**:
```
POST /basic/backup/export-zip
Content-Type: application/x-www-form-urlencoded

transfer_code=ABCD1234EFGH5678&_token=xxx
```

**Xử lý thành công**:
1. Lấy `transfer_code` từ request
2. Lấy `botId` hiện tại từ session (`getBotId()`)
3. Gọi `BotRepository@checkExistTransferCode($transferCode)` — tìm bot đích
4. Nếu bot đích tồn tại (`!empty($botTransfer)`):
   - Tạo bản ghi `BackupHistory` với `status=0` (BACKUP_CREATING)
   - Fields: `bot_id`, `code` (transfer_code), `line_account` (view_name của bot đích), `status=0`
5. Redirect về trang trước (`redirect()->back()`)

**Response thành công**: `302 Redirect` → `GET /basic/backup`

**Lỗi có thể xảy ra**:

| Case | Hành vi |
|------|---------|
| `transfer_code` rỗng | Redirect back + `$errors->has('transfer_code')` = thông báo lỗi |
| `transfer_code` không tồn tại trong bảng `bots` | Redirect back + thông báo `バックアップコードが存在しません。` |
| Bot đích không tìm thấy qua `checkExistTransferCode` | Tạo bản ghi `BackupHistory` bị bỏ qua, redirect về |
| Exception (catch \Exception) | Log error, redirect back |

**Liên kết UI**: SCR-01 → button「コピー実行」→ submit form `#backup_data`

---

### EP-03: POST `/ajax/check-transfer-code`

**Mô tả**: Kiểm tra tính hợp lệ của mã nhận dữ liệu (AJAX call). Được gọi khi user nhấn button「登録」để tra cứu tên account đích trước khi thực hiện sao chép.

**Controller**: `app/Http/Controllers/Admin/BotController.php:5940`

**Request Params** (JSON/form):

| Param | Type | Required | Mô tả |
|-------|------|----------|-------|
| `transfer_code` | string | Có | Mã nhận dữ liệu cần kiểm tra |

**Request mẫu**:
```javascript
// JavaScript AJAX call từ backup_new.blade.php:1332
$.ajax({
    type: 'POST',
    url: '/ajax/check-transfer-code',
    data: { transfer_code: $('#transfer_code_value').val() },
    dataType: 'json'
})
```

**Response thành công** (bot tìm thấy, không phải bot hiện tại):
```json
{
  "success": true,
  "data": {
    "id": 123,
    "transfer_code": "ABCD1234EFGH5678",
    "view_name": "アカウント名",
    ...
  }
}
```

**Response lỗi — mã nhập là bot hiện tại**:
```json
{
  "success": false,
  "message": "現在のアカウントのデータ受信コードは入力できません。別のアカウントのコードを入力してください。"
}
```

**Response lỗi — mã không tồn tại**:
```json
{
  "success": false,
  "message": "バックアップコードが存在しません。"
}
```

**HTTP Status**: Luôn trả về `200` kể cả khi có lỗi logic.

**Lỗi có thể xảy ra**:

| Case | Response |
|------|----------|
| `transfer_code` không tồn tại | `{ success: false, message: "バックアップコードが存在しません。" }` |
| `transfer_code` là của bot hiện tại | `{ success: false, message: "現在のアカウントの..." }` |

**Liên kết UI**: SCR-01 → button「登録」→ `#submit_search_transfer_code` click event

---

## Liên kết Endpoint ↔ Màn hình UI

| Màn hình | Action | Endpoint |
|----------|--------|----------|
| SCR-01: データコピー | Tải trang | EP-01 |
| SCR-01: データコピー → nhập mã + nhấn「登録」 | Kiểm tra mã (AJAX) | EP-03 |
| SCR-01: データコピー → nhấn「コピー実行」 | Đăng ký sao chép | EP-02 |
