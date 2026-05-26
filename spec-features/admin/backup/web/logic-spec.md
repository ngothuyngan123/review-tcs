# FA-033「データコピー」— Logic Spec

**Feature**: データコピー (Data Copy)
**Portal**: Admin
**Ngày tạo**: 2026-03-30
**Nguồn**: `app/Http/Controllers/Basic/BasicController.php`, `app/Http/Controllers/Admin/BotController.php`, `app/BackupHistory.php`

---

## 1. Controllers & Actions

---

### 1.1 `Basic\BasicController@backup` (GET `/basic/backup`)

**File**: `app/Http/Controllers/Basic/BasicController.php:1230`

**Mô tả logic**:
1. Lấy `botId` từ session (`getBotId()` → `Session::get('current_bot_id')`)
2. Lấy `userId` từ Auth (`Auth::id()`)
3. Truy vấn song song nhiều collections để render trang:
   - Tags + folder tags của bot hiện tại
   - Scenarios của bot
   - Templates + folder templates (loại trừ `in_park=1`)
   - Form answers + folder form answers
   - Auto replies + folder auto replies (kèm xử lý keyword qua `autoReplyRepository->handleReplyFirstKeywords`)
   - Rich menus
   - Events (remind list)
   - BEventDetail (booking list)
   - BackupHistory (lịch sử sao chép — sắp xếp mới nhất trước)
   - `plan_type` của bot
4. Render view `basic.backup_new`

**Side effects**: Không có — chỉ đọc.

**Validation**: Không có validation input.

**Plan type check** (client-side, JavaScript):
- Nếu `plan_type == 2` (free plan) → hiện alert → redirect về `/admin/home`
- Logic này nằm ở **JavaScript trong blade template**, KHÔNG phải server-side

```javascript
// backup_new.blade.php:1001
var plan_type_check = $('#plan_type').val();
if(plan_type_check == 2){
    alert('現在のプランは利用できない機能です。アップグレードが必要になります。');
    window.location.href = '/admin/home';
    return false;
}
```

---

### 1.2 `Basic\BasicController@backupStore` (POST `/basic/backup/export-zip`)

**File**: `app/Http/Controllers/Basic/BasicController.php:1277`

**Mô tả logic**:

```
try {
  1. Lấy transfer_code từ request
  2. Lấy currentBot + botId từ session
  3. Gọi botRepository->checkExistTransferCode(transferCode) → tìm bot đích
  4. Validate transfer_code (required + exists:bots)
     - Nếu fail → redirect back với errors + input
  5. Nếu botTransfer tồn tại:
     - Tạo BackupHistory { bot_id, code, line_account, status=0 }
  6. Redirect back
} catch Exception {
  Log error → redirect back
}
```

**Business Rule quan trọng**:
- Validation `exists:bots` kiểm tra `transfer_code` tồn tại trong bảng `bots` (cột `transfer_code`)
- Khi validation pass nhưng `checkExistTransferCode` trả về null: bản ghi BackupHistory **không được tạo** (silent skip)
- Khi tạo `BackupHistory`, `status=0` (BACKUP_CREATING) — quá trình copy thực tế được thực hiện bởi background job (xem phần Jobs bên dưới)
- `line_account` được lấy từ `botTransfer->view_name` (tên hiển thị của LOA đích)

**Validation rules**:

| Field | Rule | Thông báo JP |
|-------|------|-------------|
| `transfer_code` | `required` | `が必要です。` |
| `transfer_code` | `exists:bots` | `バックアップコードが存在しません。` |

---

### 1.3 `Admin\BotController@checkTransferCode` (POST `/ajax/check-transfer-code`)

**File**: `app/Http/Controllers/Admin/BotController.php:5940`

**Mô tả logic**:
1. Log user action (`addLogUserAction("checkTransferCode")`)
2. Lấy `transfer_code` từ request
3. Gọi `botRepository->checkExistTransferCode(transferCode)` → tra cứu bot
4. Nếu bot tồn tại:
   - Kiểm tra `bot->id == getBotId()` (không cho nhập mã của chính mình)
   - Trả về JSON `{ success: true, data: $bot }`
5. Nếu không tồn tại → trả về JSON `{ success: false, message: '...' }`

**Luồng UI sau AJAX**:
- Thành công: hiện row「コピー先アカウント名」(`#line_account_search`), điền `view_name` vào input disabled, set `transfer_code` vào hidden input của form
- Thất bại: `alert(data.message)`

---

## 2. Models Eloquent

---

### 2.1 `BackupHistory`

**File**: `app/BackupHistory.php`
**Table**: `backup_history`

**Schema**:
```sql
CREATE TABLE `backup_history` (
  `id`           int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `bot_id`       int(11) NOT NULL,           -- Bot thực hiện sao chép (bot nguồn)
  `code`         varchar(255) NOT NULL,       -- Mã nhận dữ liệu (transfer_code của bot đích)
  `line_account` varchar(255) NOT NULL,       -- Tên hiển thị của LOA đích
  `status`       int(11) NOT NULL DEFAULT '0', -- Trạng thái (xem bên dưới)
  `created_at`   timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`   timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Constants**:
```php
const BACKUP_CREATING = 0;  // Đang chờ / đang xử lý
const BACKUP_PENDING  = 1;  // Đang xử lý (pending)
```

**Status values** (từ code và template):

| Giá trị | Tên constant | Hiển thị UI | Mô tả |
|---------|-------------|-------------|-------|
| 0 | `BACKUP_CREATING` | `処理中` | Vừa tạo, chờ xử lý |
| 1 | `BACKUP_PENDING` | `処理中` | Đang xử lý |
| 2 | — | `処理完了済` | Hoàn thành |
| 3 | — | `処理完了済` | Thất bại / hoàn thành |
| 4 | — | `処理中` | Trạng thái xử lý khác |

> **Xác nhận từ blade**: `$item->status == 0 || $item->status == 1 || $item->status == 4 ? '処理中' : '処理完了済'`

**Relationships**: Không có Eloquent relationship được định nghĩa (dùng direct query).

**Guarded**: `[]` — tất cả columns đều mass-assignable.

---

### 2.2 `Bots` (liên quan)

**File**: `app/Bots.php`
**Table**: `bots`

**Columns liên quan**:
```sql
`view_name`     varchar(128) DEFAULT NULL,    -- Tên hiển thị của LOA
`transfer_code` varchar(16) DEFAULT NULL,     -- Mã nhận dữ liệu (unique per bot)
`plan_type`     int(11) NOT NULL DEFAULT '1'  COMMENT '1: standard 2: free'
```

---

## 3. Repositories

---

### 3.1 `BotRepository@checkExistTransferCode`

**File**: `app/Repositories/Eloquents/BotRepository.php:141`

```php
public function checkExistTransferCode($transferCode)
{
    return $this->model->where('transfer_code', $transferCode)
                       ->whereNotNull('transfer_code')
                       ->first();
}
```

**Mô tả**: Tìm bot theo `transfer_code`. Chỉ trả về bot nếu `transfer_code` không NULL. Trả về `null` nếu không tìm thấy.

---

## 4. Background Jobs (Cờ xử lý thực tế)

**Quan sát quan trọng**: Phương thức `backupStore` chỉ tạo bản ghi `BackupHistory` với `status=0`. **Quá trình sao chép dữ liệu thực tế (copy data) được thực hiện bởi background jobs** — KHÔNG trong web request.

**Bằng chứng**:
- `RichMenuService@isRunningBackup()` (`app/Services/V2/RichMenuService.php:54`) kiểm tra `BackupHistory` có status `[0, 1]` để block các thao tác write trong khi đang backup
- Nhiều controller (PopupAjaxController, EventAjaxController) kiểm tra `BackupHistory` status `[0, 1]` trước khi cho phép thao tác tạo/sửa/xóa dữ liệu

**Cơ chế block**:
```php
// Mẫu pattern trong PopupAjaxController.php:80, EventAjaxController.php:61
$backuoHistory = BackupHistory::where('code', $bot->transfer_code)
    ->whereIn('status', [0, 1])
    ->first();
if ($backuoHistory) {
    return response()->json(['status' => false, ...]);
}
```

> **Lưu ý**: Các class Jobs trong `app/Jobs/` không có file nào xử lý backup trực tiếp (dựa trên tìm kiếm). Quá trình copy có thể được xử lý bởi Spring Boot background jobs đọc từ bảng `backup_history` (Database Polling Model) — cần xác minh thêm ở `/rs-spec-job`.

**Giả thuyết về lifecycle của job**:
```
[Web] backupStore → INSERT backup_history (status=0)
                ↓
[Spring Boot Job polling]
    → Đọc backup_history WHERE status IN (0,1)
    → Thực hiện copy data (scenario, template, tag, auto-reply, ...)
    → UPDATE backup_history SET status=2 (Done) hoặc status=3 (Failure)
```

---

## 5. Authorization / Access Control

| Điều kiện | Xử lý |
|-----------|-------|
| Chưa đăng nhập | Redirect về trang login (middleware `web`) |
| `plan_type = 2` (free plan) | Alert + redirect `/admin/home` (JavaScript client-side) |
| Nhập mã của chính bot hiện tại | AJAX trả về lỗi: `"現在のアカウントのデータ受信コードは入力できません。..."` |
| Bot đích đang trong quá trình backup nhận | Không block ở endpoint này; block ở các feature khác |

---

## 6. Business Rules (tổng hợp)

| Rule ID | Rule | Nguồn |
|---------|------|-------|
| BR-01 | Mỗi bot có một `transfer_code` duy nhất (varchar 16) dùng làm mã nhận dữ liệu | `db/schema/tables/bots.sql:61` |
| BR-02 | Không thể sao chép dữ liệu sang chính bot hiện tại (tự copy) | `BotController.php:5947` |
| BR-03 | Free plan (`plan_type=2`) không được dùng tính năng データコピー | `backup_new.blade.php:1002` |
| BR-04 | Khi LOA đang nhận dữ liệu (backup status 0 hoặc 1), các thao tác write trên LOA đó bị block | `PopupAjaxController.php:80`, `EventAjaxController.php:61`, `RichMenuService.php:61` |
| BR-05 | Dữ liệu được sao chép bao gồm: ステップ配信, テンプレート, タグ, 自動応答, フォーム作成, リッチメニュー, イベント予約, リマインド配信, 友だち情報, アクションスケジュール実行, 対応ステータス, 友だち追加時設定, コンバージョン | `backup_new.blade.php:232-233` |
| BR-06 | Dữ liệu KHÔNG được sao chép (ngoài danh sách BR-05) phải được cài đặt thủ công | `backup_new.blade.php:235` |
| BR-07 | Lịch sử sao chép hiển thị tất cả records của bot hiện tại, sắp xếp mới nhất trước | `BasicController.php:1270` |
| BR-08 | Status 0, 1, 4 hiển thị「処理中」; các status khác (2, 3) hiển thị「処理完了済」| `backup_new.blade.php:317` |
| BR-09 | Khi nhập mã nhận dữ liệu, hệ thống phải xác nhận tên LOA đích trước khi cho phép thực hiện copy (2-step: 「登録」→ 「コピー実行」) | `backup_new.blade.php:1331-1363` |
| BR-10 | Quá trình sao chép thực tế không diễn ra synchronous trong web request — web chỉ tạo bản ghi `backup_history` để background job xử lý | `BasicController.php:1303`, `RichMenuService.php:54` |

---

## 7. Form & UI Logic (client-side)

**Flow 2 bước trong backup_new.blade.php**:

```
Bước 1: User nhập mã → nhấn「登録」
  → AJAX POST /ajax/check-transfer-code
  → Thành công: hiện row「コピー先アカウント名」, điền tên account
  → Thất bại: alert lỗi

Bước 2: User xác nhận tên account → nhấn「コピー実行」
  → LoadingOverlay hiện
  → Submit form #backup_data (POST /basic/backup/export-zip)
  → Server tạo BackupHistory record → redirect back
```

**Hidden input**: `<input type="hidden" value="" name="transfer_code">` — được set bởi JavaScript sau khi AJAX thành công (`$('input[name="transfer_code"]').val(data.data.transfer_code)`).

**Backup form ID**: `#backup_data` — POST to `route('backup.store')`.

---

## 8. Confidence Levels

| Thông tin | Độ tin cậy | Nguồn |
|-----------|-----------|-------|
| Controller logic (backup + backupStore) | Cao | Đọc trực tiếp source code |
| checkTransferCode logic | Cao | Đọc trực tiếp source code |
| BackupHistory model schema | Cao | `db/schema/tables/backup_history.sql` + model file |
| Status values (0,1,4 = 処理中) | Cao | Blade template + constants |
| Background job xử lý copy thực tế | Trung bình | Suy luận từ pattern + isRunningBackup check; cần xác minh job Spring Boot |
| Dữ liệu copy là toàn bộ (không chọn lọc) | Trung bình | Các checkbox trong blade đều bị comment out ({{-- ... --}}); form hiện tại không có checkbox chọn lọc |
