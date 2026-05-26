# Logic Spec — FA-035: Quản lý nhân viên (スタッフ管理)

**Tính năng:** FA-035  
**Portal:** Admin  
**Ngày phân tích:** 2026-05-07  
**Mức độ tin cậy tổng thể:** Cao (đọc trực tiếp từ source code)

---

## 1. Controllers

### 1.1 `Admin\StaffManagementController`
**File:** `app/Http/Controllers/Admin/StaffManagementController.php`

Controller chính cho luồng mời staff mới (invite URL flow). Xử lý toàn bộ lifecycle của lời mời từ khi tạo đến khi staff chấp nhận.

#### Actions

| Action | Method | Mô tả |
|--------|--------|-------|
| `inviteStaff` | GET | Render trang thêm staff, kiểm tra quyền |
| `editStaff` | GET | Render trang chỉnh sửa staff theo `staffBotId` |
| `getDataInviteStaff` | GET | Lấy danh sách bots để chọn khi mời/edit staff |
| `generateLinkInviteStaff` | POST | Tạo invite URL, lưu DB, tạo `UserStaffBot` pending |
| `userAccessLinkInviteStaff` | GET | Xử lý khi staff truy cập invite URL |
| `markUserVisitedLinkInvite` | POST | Đánh dấu staff đã truy cập link (accessed=1) |
| `getDetailInviteStaffByCode` | GET | Lấy chi tiết lời mời để hiển thị modal |
| `acceptInviteStaff` | POST | Staff xác nhận chấp nhận lời mời |
| `getStaffByBot` | GET | Danh sách staff phân trang theo bot |
| `getStaffAllByBot` | GET | Toàn bộ staff đã accept theo bot |
| `getListBotOwnership` | GET | Danh sách bots admin có quyền quản lý staff |
| `editListBotOfStaff` | POST | Cập nhật role/bot cho staff đã có |
| `deleteStaffBot` | POST | Xóa staff khỏi bot |
| `saveSortStaff` | POST | Lưu thứ tự staff sau drag-drop |
| `setBotInvite` | POST | Thiết lập session khi chọn bot (đăng nhập vào bot context) |

#### Dependencies (Inject)
- `FirebaseService` — đăng ký/hủy đăng ký Firebase push notification topics

---

### 1.2 `Admin\UserController`
**File:** `app/Http/Controllers/Admin/UserController.php`

Controller lớn chứa nhiều tính năng. Phần liên quan đến FA-035:

| Action | Method | Mô tả |
|--------|--------|-------|
| `employeesManagement` | GET | Render trang danh sách staff (employees_management_v2) |
| `settingRoleAccess` | GET | Render trang cài đặt quyền |
| `getSettingRoleAccess` | GET (AJAX) | Lấy cấu hình quyền + danh sách features + bots |
| `addSettingRoleAccess` | POST | Lưu cấu hình quyền thao tác |
| `accessHistories` | GET | Render trang lịch sử đăng nhập |
| `getAccessHistories` | GET (AJAX) | Lấy dữ liệu lịch sử đăng nhập phân trang |
| `exportCsvAccessHistory` | GET | Export CSV lịch sử đăng nhập |
| `getListBotAccess` | POST | Lấy danh sách bots + trạng thái access của user |
| `addEmployee` | POST | (Legacy) Tạo employee với password trực tiếp |
| `formEditEmployee` | GET | (Legacy) Form edit employee |
| `editEmployee` | POST | (Legacy) Lưu chỉnh sửa employee |
| `deleteEmployee` | POST | (Legacy) Xóa employee khỏi DB |
| `updateModalSetting` | POST (AJAX) | Tắt popup hướng dẫn (is_not_show_popup_staff=1) |

---

## 2. Models Eloquent

### 2.1 `UserStaffBot`
**File:** `app/UserStaffBot.php`  
**Table:** `user_staff_bots`  
**Mức độ tin cậy:** Cao

```php
class UserStaffBot extends Model
{
    protected $table = 'user_staff_bots';
    protected $guarded = [];

    const STATUS_NO_ACTION = 0;  // Chưa xử lý — invite đã tạo nhưng staff chưa accept
    const STATUS_ACCEPT = 1;     // Đã accept — staff đang hoạt động
    const STATUS_REJECT = 2;     // Đã reject (khi link bị đánh dấu visited)

    // Relationships
    staff() → belongsTo(User, 'user_invite_id')  // Người được mời (staff)
    role()  → belongsTo(Role, 'role_id')          // Loại quyền
}
```

**Columns quan trọng (suy luận từ code):**
| Cột | Mô tả |
|-----|-------|
| `bot_id` | Bot thuộc về |
| `user_id` | Admin owner của bot |
| `user_invite_id` | ID của người được mời (sau khi accept = user thực) |
| `user_staff_id` | ID bản ghi `UserStaff` tracking |
| `invite_staff_id` | ID bản ghi `InviteStaff` |
| `role_id` | ID quyền (0=admin, 1=副管理者, 2=運用者, 3=サポート) |
| `staff_name` | Tên hiển thị của staff |
| `is_admin` | 1 nếu là chủ bot (Admin), 0 nếu là staff được mời |
| `position` | Vị trí hiển thị (cao hơn = hiển thị trên) |
| `status` | 0=NO_ACTION, 1=ACCEPT, 2=REJECT |
| `last_time_login` | Lần đăng nhập cuối vào bot context |

---

### 2.2 `InviteStaff`
**File:** `app/InviteStaff.php`  
**Table:** `invite_staffs`  
**Mức độ tin cậy:** Cao

Lưu thông tin invite URL. Một bản ghi = một lần phát hành URL.

**Columns quan trọng (suy luận từ code):**
| Cột | Mô tả |
|-----|-------|
| `user_id` | Admin tạo invite |
| `code` | Mã ngẫu nhiên 8 ký tự, unique |
| `bot_role` | JSON — array `[{bot_id, role_id, user_id_root}]` |
| `link` | Full URL invite |
| `staff_name` | Tên staff đặt khi tạo invite |
| `is_confirmed` | 0 = chưa dùng, 1 = đã dùng (chỉ dùng được 1 lần) |
| `type` | 1 = invite staff, 2 = change bot owner |
| `created_at` | Dùng để tính hết hạn 24h |

---

### 2.3 `UserStaff`
**File:** `app/UserStaff.php`  
**Table:** `user_staffs`  
**Mức độ tin cậy:** Cao

Bảng tracking mối quan hệ admin-staff (không phải per-bot).

**Columns quan trọng (suy luận từ code):**
| Cột | Mô tả |
|-----|-------|
| `user_id` | Admin owner |
| `user_invite_id` | Staff được mời |
| `invite_staff_id` | ID bản ghi InviteStaff |
| `position` | Vị trí trong danh sách staff của admin |
| `accessed` | 0 = chưa truy cập link lần 2, 1 = đã truy cập |

---

### 2.4 `UserAccessBot`
**File:** `app/UserAccessBot.php`  
**Table:** `user_access_bot`  
**Mức độ tin cậy:** Cao

Ghi lại mỗi lần staff đăng nhập vào bot context.

**Columns:**
| Cột | Mô tả |
|-----|-------|
| `bot_id` | Bot được truy cập |
| `staff_id` | ID user đăng nhập |
| `staff_name` | Tên staff tại thời điểm đăng nhập |
| `time_access` | Thời điểm đăng nhập (format: Y/m/d H:i qua accessor) |
| `ip` | Địa chỉ IP |
| `user_staff_bot_id` | FK → `user_staff_bots.id` |

**Relationships:**
- `staff()` → `belongsTo(User, 'staff_id')`
- `staffBot()` → `belongsTo(UserStaffBot, 'user_staff_bot_id')`

**Accessor đặc biệt:**
```php
getTimeAccessAttribute() → format('Y/m/d H:i')
```

---

### 2.5 `BotRoleAccess`
**File:** `app/BotRoleAccess.php`  
**Table:** `bot_role_access`  
**Mức độ tin cậy:** Cao

Lưu quyền thao tác: mỗi bản ghi = một role có quyền với một access_feature trong một bot.

**Columns:**
| Cột | Mô tả |
|-----|-------|
| `admin_id` | Admin owner của bot |
| `bot_id` | Bot áp dụng |
| `role_id` | 1=副管理者, 2=運用者, 3=サポート |
| `access_id` | FK → `access_feature.id` |

**Relationships:**
- `role()` → `belongsTo(Role, 'role_id')`
- `accessFeature()` → `belongsTo(AccessFeature, 'access_id')`

---

### 2.6 `AccessFeature`
**File:** `app/AccessFeature.php`  
**Table:** `access_feature`  
**Mức độ tin cậy:** Cao

Danh sách các chức năng có thể phân quyền.

**Columns quan trọng (suy luận từ code):**
| Cột | Mô tả |
|-----|-------|
| `id` | Primary key |
| `name` | Tên chức năng (tiếng Nhật) |
| `menu_id` | Thuộc menu group nào (map với config `sns-line.access_feature`) |
| `parent` | 0 = menu item gốc, >0 = sub-item (FK tự tham chiếu) |

---

### 2.7 `Role`
**File:** `app/Role.php`  
**Table:** `role`  
**Mức độ tin cậy:** Cao

| ID | Tên (suy luận) | Mô tả |
|----|----------------|-------|
| 0 | (chủ bot) | Admin gốc — is_admin=1 |
| 1 | 副管理者 | Sub-admin — toàn quyền trừ xóa account |
| 2 | 運用者 | Operator — quyền vận hành |
| 3 | サポート | Support — quyền hạn chế |

---

### 2.8 `SettingNewFeature`
**File:** `app/SettingNewFeature.php`  
**Table:** `setting_new_features` (inferred)  
**Mức độ tin cậy:** Trung bình (tên table không xác nhận trực tiếp)

Cài đặt "自動チェック" — khi có tính năng mới thêm vào hệ thống, tự động cấp quyền cho role tương ứng.

**Columns:**
| Cột | Mô tả |
|-----|-------|
| `user_id` | Admin ID |
| `bot_id` | Bot ID |
| `is_role_1` | Auto-grant cho 副管理者 |
| `is_role_2` | Auto-grant cho 運用者 |
| `is_role_3` | Auto-grant cho サポート |

---

## 3. Business Rules quan trọng

### BR-001: Invite URL hết hạn sau 24 giờ
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:213`

```php
if (strtotime($inviteStaff->created_at) + 86400 < time()) {
    return redirect()->route($routerRedirect)->with(['error_message' => '有効期限を超えました。...']);
}
```
- URL chỉ hợp lệ trong 24 giờ tính từ `invite_staffs.created_at`
- Nếu hết hạn → lỗi "有効期限を超えました。再度招待をしてもらってください。"

---

### BR-002: Invite URL chỉ dùng được 1 lần
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:508`

```php
$inviteStaff->update(['is_confirmed' => 1]);
```
- Sau khi staff accept → `is_confirmed = 1`
- Lần truy cập tiếp theo bất kỳ ai → lỗi "招待されたURLはすでに無効となっています"
- Cũng kiểm tra `user_staffs.accessed = 1` để block người đã truy cập link lần 2

---

### BR-003: Không cho phép người cùng link nhận 2 lần bởi 2 người khác nhau
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:472-488`

```php
$isUserOtherAccept = UserStaffBot::query()
    ->where('user_invite_id', '<>', Auth::id())
    ->where('invite_staff_id',  $inviteStaff->id)
    ->whereIn('bot_id', $listIdBotNew)
    ->exists();
```
- Nếu phát hiện user khác đã accept cùng invite → xóa bản ghi vừa tạo và trả lỗi
- Đảm bảo một invite URL chỉ có một staff nhận

---

### BR-004: Chỉ Admin mới truy cập được tính năng quản lý staff
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:40-43`, `UserController.php:3685`

```php
$checkPermission = checkBotHasPermission('staff-management.inviteStaff', $bot_id);
if (!$checkPermission) {
    return redirect()->route('adminIndex')->withErrors(['この権限は許可されていません。']);
}
```
- Sử dụng helper `checkBotHasPermission()` để kiểm tra quyền theo route name
- Staff (role > 0) không có quyền truy cập các trang quản lý staff

---

### BR-005: Free plan không thể thêm staff
**Mức độ tin cậy:** Trung bình  
**Source:** `StaffManagementController.php:85-87` (getDataInviteStaff), `UserController.php:3379-3382`

```php
->where('plan_type', '<>', 2)  // Loại bỏ free plan
```
và:
```php
if ($userDate > $newPlanDate && $value->plan_type == 2) {
    $value['freePlan'] = 1;
}
```
- Bots có `plan_type = 2` (free) được đánh dấu `freePlan = 1`
- Bots free tạo sau `2021-07-01` bị ẩn khỏi form invite
- UI hiển thị cảnh báo「フリープラン場合、スタッフの追加はできません」
- **Lưu ý:** Bots free tạo trước `2021-07-01` vẫn cho phép staff (legacy)

---

### BR-006: Standard plan giới hạn 10 staff per bot
**Mức độ tin cậy:** Cao  
**Source:** `UserController.php:3428-3438`

```php
if($flag_contract_new == 1 && ($contractType == 'standard')){
    $countItem = AccessBot::where('bot_id', $bot_id)->count();
    $isAdd = ($countItem < 10);
}
```
- Áp dụng cho `addEmployee` (legacy flow)
- Bot có `flag_contract_new = 1` và `contract_type = 'standard'` → tối đa 10 staff
- Vượt giới hạn → lỗi "スタンダードプランの上限に達しています。プロプランへの変更が必要..."

---

### BR-007: Admin tự động được tạo bản ghi UserStaffBot khi truy cập danh sách
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:527-546`

```php
$isExistsStaffAdmin = UserStaffBot::query()
    ->where('bot_id', $botId)->where('user_id', $adminIdBot)->where('is_admin', 1)->exists();
if (!$isExistsStaffAdmin) {
    UserStaffBot::create([..., 'is_admin' => 1, 'role_id' => 0]);
}
```
- Khi `getStaffByBot` được gọi, nếu admin chưa có bản ghi `UserStaffBot` → tự tạo với `is_admin = 1`
- Đảm bảo admin luôn xuất hiện trong danh sách staff

---

### BR-008: Position của Admin luôn cao nhất
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:173-181`, `saveSortStaff`

```php
UserStaffBot::query()
    ->where(['bot_id' => $bot['bot_id'], 'user_id' => $bot['user_id_root'], 'is_admin' => 1])
    ->update(['position' => $maxPosition + 1]);
```
- Khi thêm staff mới → position của admin được đẩy lên +1 so với staff mới
- Khi sort → admin luôn được gán `count(ids) + 1` (cao nhất)
- Danh sách sắp xếp theo `position DESC` → admin luôn hiển thị cuối (hoặc đầu tùy UI rendering)

---

### BR-009: Cấu hình quyền theo từng bot, không phải toàn admin
**Mức độ tin cậy:** Cao  
**Source:** `UserController.php:3817-3866`

```php
BotRoleAccess::where('bot_id', $botId)->delete();
// ...
$dataSave[] = ['admin_id' => $bot->admin_id, 'bot_id' => $botId, 'role_id' => ..., 'access_id' => ...];
```
- Mỗi bot có cấu hình quyền riêng biệt
- Khi lưu: xóa toàn bộ cũ → insert batch mới (không update từng dòng)

---

### BR-010: Ghi log BotLifeCycle khi thêm/xóa staff
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:411-422`, `StaffManagementController.php:676-689`

- Khi staff accept invite → log `BotLifeCycle.type = 24 (ADD_STAFF)`
- Khi xóa staff → log `BotLifeCycle.type = 25 (DELETE_STAFF)`
- Log bao gồm: `staff_id`, `staff_name`, `staff_email`

---

### BR-011: Hủy Firebase notification khi xóa staff
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:663-668`

```php
$tokens = UserFirebaseToken::query()->where('user_id', $userStaff->user_invite_id)->pluck('firebase_token')->toArray();
if (!empty($tokens)) {
    $this->firebaseService->unSubscribeTopic($userStaff->bot_id, $tokens);
}
```
- Khi xóa staff → hủy đăng ký Firebase topic cho tất cả thiết bị của staff đó

---

### BR-012: Ghi lại `last_time_login` khi chọn bot context
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:977-984`

```php
UserStaffBot::query()
    ->where(['bot_id' => $botId, 'user_invite_id' => Auth::id()])
    ->update(['last_time_login' => now()]);
```
- Mỗi lần `setBotInvite` được gọi → cập nhật `last_time_login` trong `user_staff_bots`
- Trường này hiển thị trong cột「最終ログイン」của bảng danh sách

---

### BR-013: Không ghi log access history khi đăng nhập từ admin panel
**Mức độ tin cậy:** Cao  
**Source:** `StaffManagementController.php:985-994`

```php
if(!session('is_login_from_admin')){
    UserAccessBot::create([...]);
}
```
- Nếu session `is_login_from_admin` đang active → không tạo bản ghi `UserAccessBot`
- Phân biệt đăng nhập bình thường vs đăng nhập từ admin panel (system admin impersonation)

---

## 4. Authorization & Middleware

### Middleware áp dụng

| Middleware | Mô tả |
|-----------|-------|
| `admin_access` | Kiểm tra user đã xác thực và là Admin/Staff |
| `https_protocol` | Redirect HTTP → HTTPS |
| `check_remember_token` | Kiểm tra remember token còn hợp lệ |

### Permission check function
**File:** `app/Helpers/functions.php:197`

```php
function checkBotHasPermission($feature, $bot_id) {
    $permission = true;
    // ... kiểm tra quyền theo route name và bot_id
}
```
- Được dùng trong `inviteStaff` và `settingRoleAccess`
- Nếu staff không có quyền → redirect về adminIndex với error message

### Staff Management Permission
**File:** `app/Helpers/functions.php:4306`

```php
function getListBotIdStaffManagement($userId, $routeName = null) {
    $arrayBotId = Bots::where('admin_id', $userId)->where('is_deleted', 0)->pluck('id')->toArray();
    // ...
}
```
- Lấy danh sách bots mà user có quyền quản lý staff
- Nếu có `routeName` → lọc thêm theo quyền của route đó
- Dùng trong nhiều actions: `inviteStaff`, `getListBotOwnership`, `employeesManagement`, `getSettingRoleAccess`

---

## 5. Services

### `FirebaseService`
**File:** `app/Services/FirebaseService.php`  
**Inject vào:** `StaffManagementController`

| Method | Mô tả |
|--------|-------|
| `subscribeTopic($botId, $tokens)` | Đăng ký nhận notification cho bot khi staff được thêm |
| `unSubscribeTopic($botId, $tokens)` | Hủy đăng ký khi staff bị xóa |

- Token lấy từ `UserFirebaseToken.firebase_token` theo `user_id`

---

## 6. Config

### `config/sns-line.php` — `access_feature`
**Mức độ tin cậy:** Cao  
**Source:** `config/sns-line.php:1187`

Mảng định nghĩa cấu trúc menu cho bảng quyền trong SCR-EMP-03:
```php
'access_feature' => [
    // menu_id => 'Tên menu nhóm (tiếng Nhật)'
    // Ví dụ: 0 => 'メッセージ配信', 1 => 'フレンド管理', ...
]
```
- Key là `menu_id` map với `AccessFeature.menu_id`
- Value là tên nhóm hiển thị trên bảng quyền

---

## 7. Hai Flow song song: Legacy vs Invite URL

| Tiêu chí | Legacy Flow | Invite URL Flow (mới) |
|---------|------------|----------------------|
| Endpoint | POST `/employees-management/add` | POST `/ajax/generate-link-invite-staff` |
| Model tạo | `User` (tài khoản mới) | `InviteStaff` + `UserStaffBot` (pending) |
| Staff có tài khoản chưa | Chưa cần | Phải có tài khoản LME trước |
| Xác thực | Admin nhập thông tin | Staff tự đăng nhập qua invite URL |
| Quyền per bot | `AccessBot` table | `UserStaffBot` table |
| Đang sử dụng | Không rõ (có thể legacy) | Đây là UI hiện tại (SCR-EMP-02) |

**Ghi chú:** Cả 2 flow vẫn tồn tại trong code. Trang UI hiện tại (`employees-management-v2`) sử dụng Invite URL Flow. Legacy flow (`addEmployee`) vẫn có route nhưng có thể không còn được sử dụng qua UI.

---

## 8. Điểm cần chú ý / Rủi ro

| # | Vấn đề | Mức độ | Ghi chú |
|---|--------|--------|---------|
| 1 | `deleteEmployee` xóa hẳn user khỏi DB | Cao | `DB::table('users')->delete()` — không soft-delete |
| 2 | `addSettingRoleAccess` xóa toàn bộ quyền cũ rồi insert mới | Trung bình | Không có transaction bao bọc batch insert |
| 3 | `acceptInviteStaff` kiểm tra "user khác đã accept" sau khi đã insert | Trung bình | Race condition nhỏ khi 2 người cùng click cùng lúc |
| 4 | CSV export encode Shift-JIS hardcode | Thấp | Không flexible nếu cần UTF-8 CSV |
| 5 | Tham số `now` trong get-access-histories không rõ ràng | Thấp | Khác với `now_export` trong export, cùng logic nhưng tên khác |
