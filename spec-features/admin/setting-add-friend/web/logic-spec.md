# FA-007 — Tin nhắn chào mừng: Logic Spec

## Tổng quan

| Thuộc tính | Giá trị |
|-----------|---------|
| Mã tính năng | FA-007 |
| Tên tính năng | Tin nhắn chào mừng (「あいさつメッセージ」) |
| Mức độ tin cậy chung | **Cao** — phân tích trực tiếp từ source code Laravel |

---

## Controllers

### 1. `Basic\SettingAddFriendController`

**File**: `app/Http/Controllers/Basic/SettingAddFriendController.php`

**Không extends** class nào (không kế thừa base controller).

**Imports**:
- `App\ActionDetail`
- `App\Actions`
- `App\AddFriendSetting`
- `App\Bots`
- `App\StatusChat`
- `App\Tag`
- `App\Template`

**Methods**:

| Method | Visibility | Mô tả |
|--------|-----------|-------|
| `settingAddFriendNew(Request $request)` | public | Render trang bạn mới |
| `settingAddFriendOld(Request $request)` | public | Render trang bạn cũ |
| `settingAddFriendUnblock(Request $request)` | public | Render trang hủy chặn |
| `saveSettingAddFriend(Request $request)` | public | API lưu cấu hình V2 |
| `getSettingAddFriend(Request $request)` | public | API load cấu hình V2 |
| `handleMessageTemplate($templateId, $message, $botId)` | private | Xử lý tạo/cập nhật/xóa template text |
| `getActionDetailByActionId($actionId)` | package | Load chi tiết action kèm tag info |

---

### 2. `Basic\ScenarioController` (legacy methods liên quan)

**File**: `app/Http/Controllers/Basic/ScenarioController.php`

**Các methods liên quan đến FA-007** (legacy):

| Method | Visibility | Mô tả |
|--------|-----------|-------|
| `updateSettingAddFriend(Request $request)` | public | Cập nhật action_new_id / action_old_id (V1) |
| `initDataSettingAddFriend(Request $request)` | public | Load action data cũ cho V1 |
| `getMessagePreview(Request $request)` | package | Preview messages từ sent_templates (V1) |
| `removeMessageSetting(Request $request)` | package | Xóa message từ sent_templates (V1) |

---

## Models Eloquent

### 1. `AddFriendSetting`

**File**: `app/AddFriendSetting.php`

**Bảng DB**: `add_friend_setting`

**Timestamps**: `created_at`, `updated_at` (int(11) — dạng Unix timestamp)

**Guarded**: `[]` (không có cột bị guarded — tất cả fillable)

**Relationships**:
| Method | Kiểu | Target | FK | Mô tả |
|--------|------|--------|-----|-------|
| `new_scenario()` | `belongsTo` | `App\Scenario` | `new_scenario_id` | Scenario bạn mới (V1) |
| `old_scenario()` | `belongsTo` | `App\Scenario` | `old_scenario_id` | Scenario bạn cũ (V1) |

**Static methods**:
- `getAddFriendSettingByBot($bot_id)`: Join với bảng `scenario` qua `main_scenario_id`, trả về bản ghi đầu tiên

**Các cột quan trọng**:
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `bot_id` | int(11) | FK → bảng `bots` |
| `action_new_id` | int(11) | FK → `t_actions.id` — action bạn mới (V2) |
| `action_old_id` | int(11) | FK → `t_actions.id` — action bạn cũ (V2) |
| `action_id_unblock` | int(11) | FK → `t_actions.id` — action hủy chặn (V2) |
| `template_add_new_id` | int(11) | FK → `template.id` — tin nhắn bạn mới (V2) |
| `template_add_old_id` | int(11) | FK → `template.id` — tin nhắn bạn cũ (V2) |
| `template_unblock_id` | int(11) | FK → `template.id` — tin nhắn hủy chặn (V2) |
| `sent_templates_new_friend` | varchar(500) | JSON array template IDs bạn mới (V1) |
| `sent_templates_old_friend` | varchar(500) | JSON array template IDs bạn cũ (V1) |
| `new_scenario_id` | int(11) | Scenario bạn mới (V1) |
| `old_scenario_id` | int(11) | Scenario bạn cũ (V1) |
| `action_add_old_friend` | tinyint(4) | Flag action bạn cũ (V1) |

---

### 2. `Template`

**File**: `app/Template.php`

**Bảng DB**: `template`

**Timestamps**: Có (`timestamps = true`)

**Guarded**: `['url_image']`

**Relationships**:
| Method | Kiểu | Target | Mô tả |
|--------|------|--------|-------|
| `btn_templates()` | `hasMany` | `App\TmpButton` | Buttons của template |
| `Buttons()` | `hasManyThrough` | `App\Buttons` qua `App\TmpButton` | Buttons chi tiết |
| `image_map()` | `hasOne` | `App\ImageMap` | Image map đính kèm |
| `question()` | `hasOne` | `App\TmpQuestion` | Question đính kèm |
| `location()` | `hasOne` | `App\TmpLocation` | Location đính kèm |
| `introduction()` | `hasOne` | `App\TmpIntroduction` | Introduction đính kèm |

**Constants liên quan**:
- `CATEGORY_SCHEDULE_SEND_CHAT_TEXT = -1111`

**Constant đặc biệt của FA-007**:
- Tin nhắn chào mừng được lưu vào `template` với `category_id = -1212` (giá trị đặc biệt để phân biệt khỏi template thông thường)

---

### 3. `Actions`

**File**: `app/Actions.php`

**Bảng DB**: `t_actions`

**Relationships**:
| Method | Kiểu | Target | Mô tả |
|--------|------|--------|-------|
| `details()` | `hasMany` | `App\ActionDetail` | Chi tiết các action trong nhóm |

**Static methods**:
- `initDataAction($detail, $isEdit)`: Khởi tạo data cho action detail (parse JSON data của từng action item)

---

### 4. `ActionDetail`

**File**: `app/ActionDetail.php`

**Bảng DB**: `t_actions_detail`

**Guarded**: `[]`

---

### 5. `Bots`

**File**: `app/Bots.php`

**Bảng DB**: `bots`

**Cột liên quan đến FA-007**:
- `url_add_friend`: URL thêm bạn LINE (được trả về trong EP-04)

---

### 6. `StatusChat`

**File**: `app/StatusChat.php`

**Bảng DB**: `status_chat`

**Vai trò trong FA-007**: Được truyền vào view để hỗ trợ modal action (loại action 「対応ステータス」 trong SC-004)

---

### 7. `Tag`

**File**: `app/Tag.php`

**Bảng DB**: `tags`

**Vai trò trong FA-007**: Được load khi action detail có `type = 'tag'` để trả về tên tag đầy đủ

---

## Business Rules

### BR-01: Tự động tạo AddFriendSetting nếu chưa có

**Mức độ tin cậy**: **Cao**

Khi `getSettingAddFriend` được gọi, nếu chưa có bản ghi cho bot:
```php
$setting = AddFriendSetting::query()->where('bot_id', $botId)->first();
if (empty($setting)) $setting = AddFriendSetting::create(['bot_id' => $botId]);
```
→ Tự động khởi tạo bản ghi rỗng. Điều này đảm bảo API không bị lỗi khi bot mới chưa có cấu hình.

---

### BR-02: Kiểm tra Bot ID khi lưu (Bot-Switch Protection)

**Mức độ tin cậy**: **Cao**

Cả EP-05 (`saveSettingAddFriend`) và EP-06 (`updateSettingAddFriend`) đều kiểm tra:
```php
if ($botId != $botIdCurrent) {
    return response()->json(['success' => false, 'message' => '別のアカウントに切り替えたので、要求を処理できません。']);
}
```
→ Tránh trường hợp user đổi bot trong khi đang soạn thảo, nhấn Save lại ghi vào bot sai.

---

### BR-03: Lưu tin nhắn vào bảng `template` riêng với `category_id = -1212`

**Mức độ tin cậy**: **Cao**

```php
$template = Template::query()->updateOrCreate(
    ['id' => $templateId],
    [
        'bot_id' => $botId,
        'category_id' => -1212,
        'type' => 'text',
        'content' => $message,
        'update_timestamp' => time()
    ]
);
```
- `category_id = -1212` là giá trị đặc biệt phân biệt với template thông thường
- Chỉ lưu một template text duy nhất per bot per type (không phải array như V1)
- `type = 'text'` — chỉ hỗ trợ tin nhắn plain text trong V2

---

### BR-04: Xóa template khi tin nhắn rỗng

**Mức độ tin cậy**: **Cao**

```php
if ($message == '') {
    Template::where('id', $templateId)->delete();
    return null;
}
```
→ Khi Admin xóa toàn bộ nội dung textarea và save → template cũ bị xóa khỏi DB, `template_*_id` được set về `null`.

---

### BR-05: `updateOrCreate` với `bot_id` làm key tìm kiếm

**Mức độ tin cậy**: **Cao**

Mỗi bot chỉ có **một bản ghi** trong `add_friend_setting`. Khi lưu, sử dụng `updateOrCreate` theo `bot_id`:
```php
AddFriendSetting::query()->updateOrCreate(
    ['bot_id' => $botId],
    ['action_new_id' => $actionId, 'template_add_new_id' => $templateId]
);
```
→ 3 loại cấu hình (bạn mới / bạn cũ / hủy chặn) đều nằm trong **cùng một hàng** của bảng.

---

### BR-06: QR Code được tạo từ media server

**Mức độ tin cậy**: **Cao**

```php
$qrCode = env('URL_SERVER_MEDIA') . env('FOLDER_MEDIA') . 'qr_image/qr_add_friend_bot_' . $botId . '.png?v=' . time();
```
- QR code không được tạo on-the-fly trong PHP — chỉ đọc file ảnh đã được tạo sẵn từ media server
- Tham số `?v=` (timestamp) là cache-busting để đảm bảo load ảnh mới nhất
- Có logic đặc biệt trong comment về `FOLDER_MEDIA`:
  - Nếu `FOLDER_MEDIA == '/ext-media-bak/'` → dùng `/ext-media-step/` thay thế
  - (Được comment out trong source code — logic này ở Vue template)

---

### BR-07: Load chi tiết action kèm thông tin tag

**Mức độ tin cậy**: **Cao**

Khi action detail có `type == 'tag'`:
```php
$value->list_tags = Tag::whereIn('id', $data->ids)->get()->toArray();
```
→ Tự động load tên tag đầy đủ để hiển thị trong UI. Đây là behavior chung cho SC-004 Action Settings.

---

### BR-08: Phân biệt type → tên cột trong DB

**Mức độ tin cậy**: **Cao**

| Giá trị `type` request | Cột action | Cột template |
|------------------------|------------|--------------|
| `add_new` | `action_new_id` | `template_add_new_id` |
| `add_old` | `action_old_id` | `template_add_old_id` |
| `unblock` | `action_id_unblock` | `template_unblock_id` |

---

### BR-09: Phân quyền theo Middleware

**Mức độ tin cậy**: **Cao**

`BasicAccess` middleware kiểm tra:
- User phải đã đăng nhập (`Auth::check()`)
- Role phải là 0, 1, -1, hoặc 2
- Bot phải tồn tại trong session
- Nếu là bot-invite type: chỉ được truy cập route list đặc biệt
- Nếu là Staff (`checkExistsUserStaffBot()`): kiểm tra Staff có quyền với bot này

`IsExpire` middleware kiểm tra:
- Bot phải tồn tại (`bots` table)
- Gói dịch vụ chưa hết hạn (nếu `ENABLE_PAYPAL=true`)

---

## Validation Rules

**Mức độ tin cậy**: **Trung bình** — không có Laravel FormRequest riêng, validation chủ yếu ở frontend.

| Field | Rule | Nguồn |
|-------|------|-------|
| `message` | Tối đa 5,000 ký tự | Từ UI (counter hiển thị `x/5,000`) |
| `type` | Phải là `add_new` / `add_old` / `unblock` | Implicit từ switch-case trong controller |
| `botIdCurrent` | Phải trùng với `getBotId()` session | Explicit check trong controller |

Không có validation middleware/FormRequest riêng cho FA-007. Controller sẽ xử lý lỗi qua `try-catch` và trả về HTTP 500 nếu có exception.

---

## Helper Functions

### `getBotId()`

**File**: `app/Helpers/functions.php:359`

```php
function getBotId() {
    $current_bot_id = Session::get('current_bot_id');
    return $current_bot_id;
}
```
→ Lấy `bot_id` hiện tại từ PHP session. Đây là cơ chế chính để biết admin đang làm việc với LINE OA nào.

### `addLogUserAction($action)`

**File**: `app/Helpers/functions.php:8826`

→ Ghi log hành động người dùng. Được gọi trong `updateSettingAddFriend` với tham số `"updateSettingAddFriend"`.

---

## Views

| View | Template file |
|------|---------------|
| SCR-SAF-01 | `resources/views/basic/setting_add_friend/setting-add-friend-new.blade.php` |
| SCR-SAF-02 | `resources/views/basic/setting_add_friend/setting-add-friend-old.blade.php` |
| SCR-SAF-03 | `resources/views/basic/setting_add_friend/setting-add-friend-unblock.blade.php` |
| Modal 友だち情報 | `resources/views/basic/setting_add_friend/modal_friend_information.blade.php` |
| Preview Action | `resources/views/basic/setting_add_friend/preview-action-herme.blade.php` |

Views sử dụng **Vue.js** kết hợp Blade. Các AJAX call được thực hiện qua jQuery `$.ajax`.

**JS files**:
- `public/js/setting-add-friend/setting-add-friend-new.js` — logic Vue cho trang V2

---

## Luồng dữ liệu

```
[Browser khởi tạo]
    → GET /basic/setting-add-friend (EP-01)
        → Controller query StatusChat (for action modal)
        → Render Blade template
        → Vue mount, tự động gọi getAddFriend()
    
    → GET /basic/get-setting-add-friend-v2?type=add_new (EP-04)
        → Tìm AddFriendSetting theo bot_id session
        → Nếu chưa có: tạo mới AddFriendSetting
        → Load Template (text message) theo template_add_new_id
        → Load ActionDetail[] theo action_new_id
        → Load Bots.url_add_friend
        → Tạo QR URL từ env config
        → Response JSON

[User nhập và lưu]
    → User nhập message / chọn action (qua SC-004 modal)
    → Click 「保存」
    → POST /basic/save-setting-add-friend-v2 (EP-05)
        → Check bot_id session == botIdCurrent
        → Tìm AddFriendSetting theo bot_id
        → handleMessageTemplate(): upsert/delete Template
        → updateOrCreate AddFriendSetting (cập nhật action_id + template_id)
        → Response { success: true }
    → UI hiển thị toast 「保存しました」
```

---

## Ghi chú cho Job Analyzer

**Không phát hiện code liên quan queue/job trong FA-007 controller**.

Tuy nhiên, cần lưu ý: tin nhắn chào mừng được **gửi thực tế** khi có sự kiện LINE webhook (bạn bè thêm/quay lại/hủy chặn). Logic gửi tin nhắn và thực thi action có thể nằm trong:
- Laravel (webhook handler) hoặc
- Spring Boot job (xử lý hàng đợi tin nhắn)

Cần kiểm tra Spring Boot source code để xác nhận liệu gửi tin nhắn 「あいさつメッセージ」 có đi qua job queue không.

**Gợi ý tìm kiếm trong Spring Boot**:
- Tìm từ khóa: `add_friend`, `addFriend`, `greeting`, `welcome_message`, `add_friend_setting`
- Tìm class xử lý LINE webhook event `follow`, `unfollow`, `join`
