# Logic Spec — SC-004 Action Settings (Modal アクション)

**Component:** SC-004 Action Settings  
**Phiên bản:** 2025-05-20  
**Nguồn:** `src/web/sns-line/app/Http/Controllers/Basic/ActionController.php`, `src/web/sns-line/app/Services/ActionDataModalService.php`, `src/web/sns-line/app/Actions.php`, `src/web/sns-line/app/ActionDetail.php`, `src/web/sns-line/public/js/select_action.js`  
**Độ tin cậy tổng thể:** **Cao**

---

## 1. Controllers

### 1.1 ActionController

**File:** `app/Http/Controllers/Basic/ActionController.php`  
**Namespace:** `App\Http\Controllers\Basic`

**Dependencies inject qua constructor:**
- `TemplateRepository` — truy vấn template theo category
- `EventStepTimeRepositoryInterface` — xử lý remind event times
- `ActionDataModalService` — service chứa logic query cho modal
- `CategoryRepositoryInterface` — truy vấn categories

**Public methods:**

| Method | Route | Mô tả |
|--------|-------|-------|
| `initDataAction(Request)` | POST `/ajax/action/init-data` | Load toàn bộ data cho modal |
| `saveAction(Request)` | POST `/ajax/action/save` | Lưu action config |
| `deleteActionButton(Request)` | POST `/ajax/action/delete-action-button` | Xóa action + details |
| `ajaxGetReminds(Request)` | POST `/ajax/get-list-remind` | Load remind events theo folder |
| `ajaxGetFriendInfo(Request)` | POST `/ajax/get-list-friend-info` | Load friend info fields |
| `ajaxGetCategoriesByFriendInfo()` | POST `/ajax/get-list-group-friend-info` | Load friend info categories |
| `ajaxGetDataForRichMenuAction(Request)` | POST `/ajax/get-data-for-rich-menu-action` | Load rich menus |
| `ajaxGetDataForStepAction(Request)` | POST `/ajax/get-data-for-step-action` | Load scenarios |
| `ajaxGetDateForTemplateAction(Request)` | POST `/ajax/get-data-for-template-action` | Load templates |
| `saveAddTag(Request)` | POST `/ajax/save-add-tag-in-modal-action` | Tạo tag mới inline |

---

### 1.2 ActionDataModalService

**File:** `app/Services/ActionDataModalService.php`  
**Namespace:** `App\Services`

Service được inject vào `ActionController`. Chứa query logic cho từng loại data modal cần.

**Methods:**

| Method | Mô tả |
|--------|-------|
| `getGroupsAndItemsOfRichMenu($groupId)` | Query categories kind=rich_menus + RichMenus theo group_id |
| `getGroupsAndItemsOfStep($groupId)` | Query categories kind=scenario + Scenarios theo group_id |
| `getGetReminds($groupId)` | Query categories kind=event + Events theo group_id |
| `getTemplateActionData($groupId)` | Query categories kind=2 + Templates theo category_id |
| `getFriendActionData($groupId)` | Query friend info fields; xử lý đặc biệt group_id=-1 (基本情報), -2 (国内住所) |

---

## 2. Models và DB Tables

### 2.1 Actions (t_actions)

**File:** `app/Actions.php`  
**Table:** `t_actions`

```sql
CREATE TABLE `t_actions` (
  `id` int(10) UNSIGNED NOT NULL,
  `parent_id` int(11) NOT NULL,
  `type` varchar(255) NOT NULL,
  `update_timestamp` bigint(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Columns:**
- `id` — Primary key
- `parent_id` — ID của parent record (ít được dùng trực tiếp — thường lookup qua foreign key ở bảng cha)
- `type` — Context type của action (vd: `reply`, `broadcast_v2`, `button`, `richmenu`, v.v.)
- `update_timestamp` — Unix timestamp khi cập nhật

**Relationship:**
```php
public function details()
{
    return $this->hasMany('App\ActionDetail', 'action_id', 'id');
}
```

**Được tham chiếu bởi nhiều bảng:**
- `auto_reply.action_id` → tạo action cho auto reply
- `broadcast.action_id` → action broadcast
- `tags.action_id` → action preview add tag
- `form_answers.action_reply_id`, `form_answers.action_open_id`
- `calendar_courses.action_id_send_after_booking`, `.action_id_send_approve_booking`
- `calendar_salon_courses.action_id_send_after_booking`, `.action_id_send_approve_booking`
- `calendar_salon_staffs.action_id_send_after_booking`, `.action_id_send_approve_booking`
- `buttons.action_id`, image map items, v.v.

**Độ tin cậy:** **Cao**

---

### 2.2 ActionDetail (t_actions_detail)

**File:** `app/ActionDetail.php`  
**Table:** `t_actions_detail`

```sql
CREATE TABLE `t_actions_detail` (
  `id` int(10) UNSIGNED NOT NULL,
  `action_id` int(11) NOT NULL,
  `bot_id` int(11) DEFAULT NULL,
  `type` varchar(255) NOT NULL,
  `data` text NOT NULL,
  `embed_regex_text` varchar(255) DEFAULT NULL,
  `has_filters` tinyint(4) NOT NULL DEFAULT '0',
  `update_timestamp` bigint(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Columns:**
- `action_id` — FK → `t_actions.id`
- `bot_id` — Bot owner
- `type` — Action type: `scenario`, `template`, `text`, `remind`, `tag`, `richmenu`, `bookmark`, `friend_info`, `compliant_status`, `block`, `form_answer`, `booking`, `product_page`, `conversion`, `other_text`, `keywords`, `phone`, `email`, `add_friend`
- `data` — JSON string chứa config của action (cấu trúc khác nhau theo type)
- `embed_regex_text` — Regex embed trong text content (dùng cho URL detection)
- `has_filters` — 0 = không có filter, 1 = có filter (dùng để hiển thị badge 「絞込 設定済」)

**Relationship:**
```php
public function tagLine()
{
    return $this->hasOne('App\Actions', 'id', 'action_id');
}
```

**Độ tin cậy:** **Cao**

---

### 2.3 FilterV2 (filters_v2)

**File:** `app/FilterV2.php`  
**Table:** `filters_v2`

Filter được lưu liên kết với từng `t_actions_detail` khi `parent_type = 'modal_action'` và `parent_id = action_detail.id`.

**Relevant columns:**
- `parent_type` — `'modal_action'`
- `parent_id` — ID của `t_actions_detail`
- `operator` — `'and'` hoặc `'or'`
- `type` — Loại filter condition
- `text_preview` — Text hiển thị preview

---

## 3. Action Data Format (JSON trong `t_actions_detail.data`)

Mỗi action type lưu JSON với cấu trúc riêng:

### 3.1 type = `scenario`

```json
{
  "action": 1,
  "id": 0,
  "start_day": 0,
  "scenario_name": "",
  "selected_group_id": 0
}
```

| Field | Giá trị | Mô tả |
|-------|---------|-------|
| `action` | 1=停止, 2=開始/再開, 3=途中から | Loại thao tác |
| `id` | integer | ID scenario (0 nếu action=1) |
| `start_day` | integer | Ngày bắt đầu (chỉ khi action=3) |
| `scenario_name` | string | Cache tên scenario |

**Lưu ý:** Khi `action=1` → force `id=0`, `start_day=0`. Khi `action=2` → force `start_day=0`.

---

### 3.2 type = `template`

```json
{
  "id": 5,
  "template_name": "テンプレート名",
  "group_id": 2,
  "selected_group_id": 2
}
```

---

### 3.3 type = `text`

```json
{
  "content": "テキスト内容 (max 5000 chars)"
}
```

**Lưu ý:** Khi save, `content` được xử lý qua `detectUrlInMessageTextV2($data['content'], $bot)` để detect URLs và tạo tracking links.

---

### 3.4 type = `remind`

```json
{
  "id": 10,
  "type": 1,
  "remind_name": "イベント名",
  "event_id": 3,
  "event_date": "2025-06-01",
  "event_start_time": "10:00",
  "selected_group_id": 0
}
```

| Field | Giá trị | Mô tả |
|-------|---------|-------|
| `type` | 1=配信開始, 0=配信停止 | |
| `event_id` | integer | ID của Events (remind event) |
| `id` | integer | ID của EventTimes record được tạo (-1 nếu type=0) |

**Logic đặc biệt:** Khi save type=1, tạo `EventTimes` record mới (hoặc dùng existing nếu đã có cùng event_id/date/time). Sau đó gọi `createEventStepTime($event_id, $event_time_id)`.

---

### 3.5 type = `tag`

```json
{
  "ids": [1, 2, 3],
  "action": 1
}
```

| Field | Giá trị | Mô tả |
|-------|---------|-------|
| `ids` | array int | Mảng ID tags được chọn |
| `action` | 1=つける, 2=はずす | Gán hay bỏ tag |

**Validation khi save:** Lọc bỏ các id null/empty trước khi insert.

---

### 3.6 type = `richmenu`

```json
{
  "id": 7,
  "action": 2,
  "richmenu_name": "リッチメニュー名",
  "selected_group_id": 0
}
```

| Field | Giá trị | Mô tả |
|-------|---------|-------|
| `action` | 1=表示停止, 2=表示する | |
| `id` | integer | ID RichMenu (0 nếu action=1) |

---

### 3.7 type = `bookmark`

```json
{
  "action": 1
}
```

| `action` | Mô tả |
|---------|-------|
| 1 | ブックマークする |
| 2 | ブックマークを外す |

---

### 3.8 type = `friend_info`

```json
{
  "id": 5,
  "name": "フィールド名",
  "type": 2,
  "action": 2,
  "content": "入力値",
  "action_content": null,
  "is_random": 0,
  "from": "",
  "to": "",
  "group_open": 0
}
```

| Field | Mô tả |
|-------|-------|
| `id` | ID của `friend_information_settings` record. Giá trị âm = system fields (-1=system_name, -2=phone, -3=email, -4=birthday, -6=都道府県) |
| `type` | Data type: 1=選択肢, 2=記述, 3=年月日, 6=ポイント |
| `action` | Thao tác (xem bảng bên dưới) |
| `content` | Giá trị nhập |
| `action_content` | Option ID khi type=1 + action=2 (FriendInfoOptionSelects.id) |
| `is_random` | 0=指定, 1=ランダム (chỉ khi type=6) |
| `from`, `to` | Range khi ランダム (chỉ khi type=6 + is_random=1) |

**Action values theo type:**
| `type` | `action` | Mô tả |
|--------|---------|-------|
| 1 (選択肢) | 1 | 情報を削除 |
| 1 (選択肢) | 2 | 情報を登録 |
| 2 (記述) | 1 | 情報を削除 |
| 2 (記述) | 2 | 情報を登録 |
| 3 (年月日) | 1 | 情報を削除 |
| 3 (年月日) | 2 | 指定日付を登録 |
| 3 (年月日) | 3 | 当日日付を登録 |
| 6 (ポイント) | 0 (UI) / 1 (DB) | 情報を削除 |
| 6 (ポイント) | 1 (UI) / 2 (DB) | ポイント登録（上書き） |
| 6 (ポイント) | 2 (UI) / 2 (DB) | ポイントプラス |
| 6 (ポイント) | 3 (UI) / 2 (DB) | ポイントマイナス |

**Lưu ý quan trọng về type=6 (Point) — conversion UI↔DB:**
- UI `action=0` → DB `action=1` (delete point → mapped to action=1)
- UI `action=1,2,3` → DB `action=2` + `action_content=UI_action` (1,2,3)
- Khi load về: DB `action=1` → UI `action=0`; DB `action=2` → UI `action=action_content`

**Lưu ý type=1 (選択肢):**
- Khi save: tìm `FriendInfoOptionSelects` theo `friend_info_id` + `option_value` → lưu ID vào `action_content`

---

### 3.9 type = `compliant_status`

```json
{
  "id": 3,
  "action": 1,
  "content": "ステータス名"
}
```

| Field | Mô tả |
|-------|-------|
| `action` | 1=ステータスをつける, 2=ステータスを外す |
| `id` | ID của `StatusChat` record (chỉ khi action=1) |
| `content` | Cache tên status. Khi action=2 → set content="" |

---

### 3.10 type = `block`

```json
{
  "action": 1
}
```

| `action` | Mô tả |
|---------|-------|
| 1 | ブロックする |
| 2 | ブロック解除 |
| 3 | 表示 |
| 4 | 非表示 |

---

### 3.11 Action-Only Types (không kết hợp được với action khác)

| type | JSON data | Mô tả |
|------|-----------|-------|
| `form_answer` | `{"id": 1}` | ID FormAnswer |
| `booking` | `{"id": 1}` | ID BEventDetail |
| `product_page` | `{"id": 1}` | ID SItems (product) |
| `conversion` | `{"id": 1}` | ID Conversion |
| `other_text` | `{"content": "テキスト"}` | Text LINE user phải gửi |
| `keywords` | `{"id": 1}` | ID Keyword (auto reply keyword) |
| `phone` | `{"content": "0901234567"}` | Số điện thoại |
| `email` | `{"content": "user@example.com"}` | Email address |
| `add_friend` | `{"id": "@lineId"}` | LINE ID cho add friend page |

---

## 4. Action Execution Flow (Data Flow)

### 4.1 Flow cấu hình (User → DB)

```
User tương tác modal
    ↓
Vue state: actions[] array được update
    ↓
User click 「保存」
    ↓
Frontend validation (vee-validate + custom JS)
    ↓
POST /ajax/action/save
    data: { id, type, action_detail: JSON.stringify(actions) }
    ↓
ActionController@saveAction
    ├── Nếu id empty (new): INSERT t_actions → get new id
    │   → foreach action_detail: INSERT t_actions_detail
    └── Nếu id exists (edit):
        ├── foreach action_detail:
        │   ├── detailId empty: INSERT t_actions_detail
        │   └── detailId exists: UPDATE t_actions_detail
        └── DELETE t_actions_detail WHERE id NOT IN (saved ids)
    ↓
    Nếu change_filter=1:
        FilterV2::saveFilter(filter_and, filter_or, 'modal_action', detail_id)
        UPDATE t_actions_detail.has_filters = (0 hoặc 1)
    ↓
    Behavior phụ theo type (update FK ở bảng cha)
    ↓
Response: { success: true, action_id: X }
    ↓
Frontend cập nhật parent component với action_id mới
```

### 4.2 Flow load (DB → Modal)

```
Trang cha trigger mở modal
    ↓
Set setting_action.action_id = existing_action_id (hoặc '')
    ↓
Modal open event → setting_action.initDataAction()
    ↓
POST /ajax/action/init-data { id: action_id }
    ↓
ActionController@initDataAction
    ├── Load Actions + ActionDetail records
    ├── Enrich từng detail (thêm groups, group_items, tên cache)
    ├── Tách action_only (type thuộc type_only list)
    └── Load danh sách lựa chọn (form_answers, bookings, conversions, products, keywords, friend_info)
    ↓
Response → Vue state được cập nhật:
    actions = action_detail array
    action_only = action_only object
    form_answers, bookings, conversions, products, keywords, friend_info = dropdowns
```

---

## 5. Frontend Validation Logic

**Framework:** `vee-validate` (RC7 — version cũ)  
**Config:** `select_action.js:1-20` — locale=ja, strict=true

### 5.1 Validation rules theo action type

| Action type | Field name | Rule |
|-------------|-----------|------|
| scenario | `step_id_{indexAction}` | required (khi action != 1) |
| template | `template_id_{indexAction}` | required |
| text | `text_content_add_{indexAction}` | required, max:5000 |
| remind | `remind_ids_{indexAction}` | required |
| remind | `remind_date_ids_{indexAction}` | required (khi type=1) |
| remind | `remind_time_ids_{indexAction}` | required (khi type=1) |
| tag | `tag_ids_{indexAction}` | required |
| richmenu | `rich_menu_{indexAction}` | required (khi action=2) |
| bookmark | `bookmark_{indexAction}` | required |
| friend_info | `friend_info_{indexAction}` | required |
| compliant_status | `compliant_status_{indexAction}` | required |
| compliant_status | `compliant_id_{indexAction}` | required (khi action=1) |
| action_only (form_answer) | `form_answer` | required |
| action_only (booking) | `booking` | required |
| action_only (product_page) | `product_page` | required |
| action_only (conversion) | `conversion` | required |
| action_only (keywords) | `keywords` | required |
| action_only (phone) | `phone_number` | custom validator |
| action_only (email) | `email` | email format |

### 5.2 Custom validation (ngoài vee-validate)

JS tại `select_action.js:1195–1223` kiểm tra thêm:
- `friend_info` type=2, action=2: content phải không rỗng
- `friend_info` type=3, action=2: content (date) phải không rỗng
- `friend_info` type=6, action=2: content (point) phải > 0

`flagError` được set = 1 nếu fail → không submit.

---

## 6. Context Modes (`type_action`)

`type_action` được set từ trang cha vào Vue data `setting_action.type_action` trước khi mở modal. Ảnh hưởng:

1. **Ẩn action buttons trong sidebar** — xem bảng bên dưới
2. **Chọn save handler** — nút 「保存」 gọi method khác nhau
3. **Merge tag visibility** — một số merge tag chỉ hiện theo context

### Sidebar buttons ẩn theo `type_action`

| `type_action` | Button ẩn |
|--------------|-----------|
| `step_message` | ステップ, テンプレート, テキスト |
| `broadcast_v2` | テンプレート, テキスト |
| `richmenu` | リッチメニュー |
| `bookmark` | ブックマーク |
| Booking calendar types (danh sách `listActionNotShowRemind`) | リマインド |

**`listActionNotShowRemind` (từ `select_action.js:199`):**
```
calendar_notify_full, calendar_notify_not_full,
setting_message_booking, setting_message_booking_request,
setting_message_booking_approve, setting_message_booking_deny,
setting_message_cancel_booking, setting_message_cancel_request,
setting_message_cancel_approve, setting_message_cancel_deny,
status-send-after-booking, preview-calendar, event_step_calendar,
calendar_salon_notify_full, calendar_salon_notify_not_full,
setting_message_booking_salon (và các variants salon),
event_step_calendar_salon,
calendar-salon-status-send-after-booking,
calendar-staff-status-send-after-booking,
calendar-staff-status-send-approve-booking,
calendar-salon-status-send-approve-booking
```

### Save handlers theo `type_action`

| `type_action` | JS Method | PHP endpoint |
|--------------|-----------|--------------|
| default (hầu hết) | `saveSettingAction()` | POST `/ajax/action/save` |
| `button` | `saveSettingActionButton()` | Cùng endpoint, cập nhật `buttons.action_id` |
| `image_map` | `saveSettingActionImageMap()` | Cùng endpoint, cập nhật imageMap state |
| `video` | `saveSettingActionVideo()` | Cùng endpoint, cập nhật video action_id |
| `formAnswer_setting_action` | `saveSettingActionFormAnswer()` | Cùng endpoint + update `form_answers.action_reply_id/action_open_id` |
| `formAnswer_diagnostic_content` | `saveSettingActionFormAnswer()` | Cùng endpoint |
| `add_friend_new` | `saveSettingAction()` | Cùng endpoint |

---

## 7. Filter Per Action

### 7.1 Storage
Mỗi `t_actions_detail` có thể có nhiều filter conditions lưu trong `filters_v2`:
- `parent_type = 'modal_action'`
- `parent_id = t_actions_detail.id`
- `operator = 'and'` hoặc `'or'`

### 7.2 Save filter logic
Khi `change_filter=1` trong một action item (user đã touch filter):
1. `FilterV2::saveFilter(filter_and, filter_or, 'modal_action', action_detail_id)`
2. Sau đó UPDATE `t_actions_detail.has_filters = 0 hoặc 1`

### 7.3 Delete filter logic
Khi xóa action detail (không còn trong list):
```php
FilterV2::where('parent_type', 'modal_action')
    ->whereIn('parent_id', $deleted_detail_ids)
    ->delete();
ActionDetail::where(...)->delete();
```

### 7.4 UI indicator
- `has_filters = 0` → button 「絞込 未設定」(class `btn-sns-line-light`)
- `has_filters = 1` → button 「絞込 設定済」(class `btn-sns-line-primary-bg`)
- JS cũng check in-memory `data.filters.and/or` array length để override

---

## 8. Tag Creation Inline

### 8.1 Flow
1. User click 「タグ新規追加」 → sub-modal `#modalAddTagModalAction` mở, main modal `#settingActionUrlModal` đóng
2. User chọn folder + nhập tên (max 50 chars — watch ở Vue, không validate server)
3. User click 「保存してアクションに設定に戻る」 → `saveAddTag()` → POST `/ajax/save-add-tag-in-modal-action`
4. Backend: check tên empty, check duplicate name trong bot → INSERT vào `tags`
5. Response success → đóng sub-modal, mở lại main modal, gọi `initDataTag(group_id)` để refresh tag list

### 8.2 DB Insert
```php
DB::table('tags')->insertGetId([
    'bot_id' => $botId,
    'name' => $request->tag_name,
    'category_id' => $request->folder_id,
    'action_id' => NULL,
    'is_2th_apply' => 0,
    'created_at' => Carbon::now()
]);
// Sau đó: update position = max(position) + 1
```

---

## 9. Action Deletion Flow

### 9.1 Xóa 1 action item trong list (frontend)
`removeItemAction(index)` trong Vue:
- Xóa khỏi `actions[]` array
- Nếu type thuộc `type_ignore` → xóa khỏi `type_ignore[]`
- Không gọi API — chỉ xóa khi user save lại

### 9.2 Xóa toàn bộ action (button context)
`deleteActionButton(action_id)` → POST `/ajax/action/delete-action-button`:
- `Buttons::update(['action_id' => null])`
- `FilterV2::deleteActionFilterByAction($actionId)` — xóa tất cả filters
- `ActionDetail::where('action_id', $actionId)->delete()`
- `Actions::where('id', $actionId)->delete()`

### 9.3 Xóa khi save empty action list
Nếu `action_detail` array empty khi save (type = `conversion_list`):
- Xóa tất cả filters liên quan
- Xóa tất cả `t_actions_detail`
- Cập nhật `conversions.action_id = null`
- Dispatch `DeleteActionInSourceMessage` job để cleanup async

---

## 10. Giới hạn và Constraints

| Giới hạn | Giá trị | Nguồn | Độ tin cậy |
|---------|---------|-------|-----------|
| Max ký tự text action | 5,000 | Blade + vee-validate | **Cao** |
| Max ký tự tag name (inline) | 50 | Vue watch + backend implicit | **Cao** |
| Số lượng action tối đa | Không giới hạn rõ ràng | Không tìm thấy constant | **Thấp** |
| `action_only` và `actions[]` | Loại trừ nhau | Logic UI (action_only zone riêng) | **Cao** |
| Duplicate `scenario`/`richmenu`/`remind` | Chỉ 1 per config | `type_ignore` list | **Cao** |
| Broadcast edit timeout | 5 phút trước send | `saveAction` check | **Cao** |
| Backup in progress | Block edit | `BackupHistory` check | **Cao** |

---

## 11. Điểm cần điều tra thêm

1. **`ajaxGetRichMenu` method** — Trong routes có `Route::post('/get-list-rich-menu', 'Basic\ActionController@ajaxGetRichMenu')` nhưng code controller (`ActionController.php`) chỉ có `ajaxGetDataForRichMenuAction` — có thể là method không tồn tại hoặc thuộc controller khác.
2. **`DeleteActionInSourceMessage` Job** — Background job được dispatch khi xóa action empty. Cần `/spec-job` để phân tích.
3. **`createEventStepTime` helper** — Hàm helper xử lý remind event steps. Logic chưa rõ.
4. **`detectUrlInMessageTextV2` helper** — Xử lý URL detection trong text action. Cần đọc để biết format lưu.
5. **`getListInforFriendCategories`** — Static method trên model Category — chưa đọc implementation.
6. **Execution của actions** — Logic thực thi actions khi trigger (gửi tin, auto reply, v.v.) nằm ở Spring Boot jobs, chưa phân tích.
