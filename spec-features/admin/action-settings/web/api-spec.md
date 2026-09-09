# API Spec — SC-004 Action Settings (Modal アクション)

**Component:** SC-004 Action Settings  
**Phiên bản:** 2025-05-20  
**Nguồn:** `src/web/sns-line/routes/web.php`, `src/web/sns-line/app/Http/Controllers/Basic/ActionController.php`, `src/web/sns-line/public/js/select_action.js`  
**Độ tin cậy:** **Cao** (đọc trực tiếp từ routes + controller + JS)

---

## Tổng quan

Tất cả endpoints phục vụ SC-004 đều nằm trong route group `prefix: 'ajax'`, `middleware: ['check_login', 'check_remember_token']`.  
URL pattern đầy đủ: `/ajax/{endpoint}`.

---

## EP-01: Khởi tạo dữ liệu modal action

**Method:** `POST`  
**URL:** `/ajax/action/init-data`  
**Route name:** `action.save`  
**Controller:** `Basic\ActionController@initDataAction`  
**File:** `app/Http/Controllers/Basic/ActionController.php:70`

### Mục đích
Load toàn bộ dữ liệu cần thiết khi modal 「アクション」 mở ra — bao gồm danh sách action đã cấu hình, danh sách lựa chọn cho action_only types, và data cho từng action detail.

### Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `id` | integer | Không | ID của `t_actions` record. Nếu empty thì trả về dữ liệu rỗng (new action) |

### Response

```json
{
  "success": true,
  "action": { /* Actions model object hoặc [] */ },
  "type_ignore": ["scenario", "richmenu"],
  "form_answer": [{ "id": 1, "name": "フォーム名" }],
  "bookings": [{ "id": 1, "title": "イベント名" }],
  "conversions": [{ "id": 1, "name": "CV名" }],
  "products": [{ "id": 1, "name": "商品名" }],
  "action_only": { /* ActionDetail object hoặc {} */ },
  "action_detail": [ /* array ActionDetail objects */ ],
  "keywords": [{ "id": 1, "keyword": "キーワード" }],
  "dataFriendInfo": [
    {
      "name": "未分類",
      "friend_infos": [{ "id": 1, "hash_id": "abc123", /* ... */ }]
    },
    {
      "id": 5, "name": "カテゴリ名",
      "friend_infos": [/* ... */]
    }
  ]
}
```

### Logic xử lý đặc biệt

- `type_ignore`: mảng các type mà modal không nên hiển thị thêm (vì đã có) — áp dụng cho `scenario`, `richmenu`, `remind`
- `action_only`: nếu detail có type thuộc `['form_answer', 'booking', 'product_page', 'conversion', 'other_text', 'keywords', 'phone', 'email', 'add_friend']` → tách riêng thành `action_only`, không nằm trong `action_detail`
- Mỗi detail trong `action_detail` được enrich thêm data cho UI: `groups`, `group_items`, `selected_group_id`, `list_tags` tùy theo `type`
- Mỗi `friend_info` item được encode `hash_id` bằng Hashids

**Độ tin cậy:** **Cao**

---

## EP-02: Lưu action configuration

**Method:** `POST`  
**URL:** `/ajax/action/save`  
**Route name:** `action.save`  
**Controller:** `Basic\ActionController@saveAction`  
**File:** `app/Http/Controllers/Basic/ActionController.php:293`

### Mục đích
Endpoint chính — lưu toàn bộ action configuration khi user click 「保存」 trong modal. Xử lý cả create mới và update existing action.

### Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `id` | integer | Không | ID action hiện tại (nếu edit). Empty = tạo mới |
| `type` | string | Có | `type_action` của context (vd: `reply`, `broadcast_v2`, `button`, `richmenu`, v.v.) |
| `action_detail` | string (JSON) | Có | JSON serialize của mảng `actions` từ Vue — array các action item |
| `preview_add_tag` | string | Không | `'add_tag_preview'` nếu context là preview add tag |
| `tag_current_id` | integer | Không | ID tag khi `preview_add_tag = 'add_tag_preview'` |
| `tab` | integer | Không | Tab index (1=action_reply, 2=action_open) khi `type = 'formAnswer_setting_action'` |
| `formId` | integer | Không | ID FormAnswer khi `type = 'formAnswer_setting_action'` |
| `courseId` | integer | Không | ID CalendarCourse khi `type` thuộc booking calendar types |
| `staffId` | integer | Không | ID CalendarSalonStaff khi `type` thuộc salon staff types |

### `action_detail` JSON Structure

Mỗi item trong mảng có cấu trúc chung:
```json
{
  "id": null,
  "type": "tag",
  "change_filter": 1,
  "data": {
    "ids": [1, 2, 3],
    "action": 1,
    "filters": {
      "and": [],
      "or": []
    }
  }
}
```

Cấu trúc `data` tùy theo `type` — xem chi tiết tại `logic-spec.md`.

### Response

```json
{
  "success": true,
  "action_id": 42
}
```

Khi thất bại (backup đang chạy):
```json
{
  "success": false,
  "message": "MESSAGE_NOTIFY_BACKUP"
}
```

Khi broadcast đã scheduled (trong 5 phút):
```json
{
  "success": false,
  "message": "配信予定日時5分前からは配信内容の編集はできません。"
}
```

### Behavior phụ theo `type`

| `type` | Behavior phụ |
|--------|-------------|
| `formAnswer_setting_action` (tab=1) | Update `form_answers.action_reply_id` |
| `formAnswer_setting_action` (tab=2) | Update `form_answers.action_open_id` |
| `status-send-after-booking` | Update `calendar_courses.action_id_send_after_booking` |
| `status-send-approve-booking` | Update `calendar_courses.action_id_send_approve_booking` |
| `calendar-salon-status-send-after-booking` | Update `calendar_salon_courses.action_id_send_after_booking` |
| `calendar-salon-status-send-approve-booking` | Update `calendar_salon_courses.action_id_send_approve_booking` |
| `calendar-staff-status-send-after-booking` | Update `calendar_salon_staffs.action_id_send_after_booking` |
| `calendar-staff-status-send-approve-booking` | Update `calendar_salon_staffs.action_id_send_approve_booking` |

**Độ tin cậy:** **Cao**

---

## EP-03: Xóa action button

**Method:** `POST`  
**URL:** `/ajax/action/delete-action-button`  
**Route name:** `action.deleteActionButton`  
**Controller:** `Basic\ActionController@deleteActionButton`  
**File:** `app/Http/Controllers/Basic/ActionController.php:713`

### Mục đích
Xóa hoàn toàn 1 action record (gồm parent `t_actions` + tất cả `t_actions_detail` + filters liên quan). Được gọi khi user bỏ action khỏi button template, image map, v.v.

### Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `action_id` | integer | Có | ID của `t_actions` cần xóa |

### Response

```json
{ "success": true }
```

**Độ tin cậy:** **Cao**

---

## EP-04: Lấy danh sách scenarios (step) theo folder

**Method:** `POST`  
**URL:** `/ajax/get-data-for-step-action`  
**Route name:** `ajaxGetDataForStepAction`  
**Controller:** `Basic\ActionController@ajaxGetDataForStepAction`  
**File:** `app/Http/Controllers/Basic/ActionController.php:752`

### Mục đích
Khi user chọn folder trong combo-box ステップ — load danh sách scenarios và folders.

### Request Parameters

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `group_id` | integer | ID folder (category). 0 = 未分類 |

### Response

```json
{
  "status": true,
  "groups": [{ "id": 1, "name": "フォルダ名", "position": 10 }],
  "items": [{ "id": 1, "name": "シナリオ名" }],
  "selected_group_id": 0
}
```

**Độ tin cậy:** **Cao**

---

## EP-05: Lấy danh sách templates theo folder

**Method:** `POST`  
**URL:** `/ajax/get-data-for-template-action`  
**Route name:** `ajaxGetDateForTemplateAction`  
**Controller:** `Basic\ActionController@ajaxGetDateForTemplateAction`  
**File:** `app/Http/Controllers/Basic/ActionController.php:771`

### Mục đích
Khi user chọn folder trong combo-box テンプレート — load danh sách templates và folders.

### Request Parameters

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `group_id` | integer | ID folder (category). 0 = 未分類 |

### Response

```json
{
  "status": true,
  "groups": [{ "id": 1, "name": "フォルダ名", "position": 10 }],
  "items": [{ "id": 1, "name": "テンプレート名" }],
  "selected_group_id": 0
}
```

**Độ tin cậy:** **Cao**

---

## EP-06: Lấy danh sách rich menus theo folder

**Method:** `POST`  
**URL:** `/ajax/get-data-for-rich-menu-action`  
**Route name:** `ajaxGetDataForRichMenuAction`  
**Controller:** `Basic\ActionController@ajaxGetDataForRichMenuAction`  
**File:** `app/Http/Controllers/Basic/ActionController.php:733`

### Mục đích
Khi user chọn folder trong combo-box リッチメニュー — load danh sách rich menus và folders.

### Request Parameters

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `group_id` | integer | ID folder (category). 0 = 未分類 |

### Response

```json
{
  "status": true,
  "groups": [{ "id": 1, "name": "フォルダ名", "position": 10 }],
  "items": [{ "id": 1, "name": "リッチメニュー名" }],
  "selected_group_id": 0
}
```

**Độ tin cậy:** **Cao**

---

## EP-07: Lấy danh sách remind events theo folder

**Method:** `POST`  
**URL:** `/ajax/get-list-remind`  
**Route name:** `ajax.get.list.remind`  
**Controller:** `Basic\ActionController@ajaxGetReminds`  
**File:** `app/Http/Controllers/Basic/ActionController.php:247`

### Mục đích
Khi user chọn folder trong combo-box リマインド — load danh sách events (remind) và folders.

### Request Parameters

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `group_id` | integer\|null | ID folder (category event) |

### Response

```json
{
  "status": true,
  "groups": [{ "id": 1, "name": "フォルダ名", "kind": "event", "position": 5 }],
  "items": [{ "id": 1, "event_name": "イベント名" }],
  "selected_group_id": 0
}
```

**Độ tin cậy:** **Cao**

---

## EP-08: Lấy danh sách friend info fields theo folder

**Method:** `POST`  
**URL:** `/ajax/get-list-friend-info`  
**Route name:** `ajax.get.list.friend_info`  
**Controller:** `Basic\ActionController@ajaxGetFriendInfo`  
**File:** `app/Http/Controllers/Basic/ActionController.php:267`

### Mục đích
Khi user chọn folder trong combo-box 友だち情報 — load danh sách fields và folder list.

### Request Parameters

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `group_id` | integer\|null | ID folder. Giá trị đặc biệt: -1 = 基本情報, -2 = 国内住所 |

### Response

```json
{
  "status": true,
  "groups": [
    { "id": -1, "name": "基本情報" },
    { "id": -2, "name": "国内住所" },
    { "id": 5, "name": "カスタムグループ名" }
  ],
  "items": [
    { "id": 1, "title": "フィールド名", "type_data": 1, "setting_value": {} }
  ],
  "group_open": null
}
```

**Logic đặc biệt:** Khi `group_id == -1`, trả về system default fields (system_name, phone, email, birthday, age) với thống kê số lượng bạn bè có dữ liệu. Khi `group_id == -2`, trả về address fields (zip_code, province, district, township, building). **Độ tin cậy:** **Cao**

---

## EP-09: Lấy danh sách friend info categories

**Method:** `POST`  
**URL:** `/ajax/get-list-group-friend-info`  
**Route name:** `ajaxGetGroupFriendInfo`  
**Controller:** `Basic\ActionController@ajaxGetCategoriesByFriendInfo`  
**File:** `app/Http/Controllers/Basic/ActionController.php:287`

### Mục đích
Load danh sách tất cả folder của friend info (categories). Được gọi khi modal init để populate sidebar folder list.

### Request Parameters
Không có.

### Response
Trả về array categories từ `Category::getListInforFriendCategories($bot_id)`.

**Độ tin cậy:** **Cao**

---

## EP-10: Thêm tag mới trong modal action

**Method:** `POST`  
**URL:** `/ajax/save-add-tag-in-modal-action`  
**Route name:** `saveAddTag`  
**Controller:** `Basic\ActionController@saveAddTag`  
**File:** `app/Http/Controllers/Basic/ActionController.php:790`

### Mục đích
Khi user click 「タグ新規追加」 → nhập tên tag mới → click 「保存してアクションに設定に戻る」. Tạo tag mới và trả về kết quả.

### Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|-------|
| `tag_name` | string | Có | Tên tag mới (max 50 ký tự — enforced ở frontend) |
| `folder_id` | integer | Không | ID folder/category chứa tag. 0 = 未分類 |

### Response

Thành công:
```json
{ "status": true, "msg": "insert success" }
```

Thất bại (tag_name rỗng):
```json
{ "status": false, "msg": "新しいタグ名を入力してください" }
```

Thất bại (tên đã tồn tại):
```json
{ "status": false, "msg": "そのタグ名はすでに利用されています" }
```

**Độ tin cậy:** **Cao**

---

## EP-11: Lấy danh sách tags theo folder (cho action tag)

**Method:** `POST`  
**URL:** `/ajax/get-list-group-tag`  
**Route name:** `ajaxGetListCategoryTag`  
**Controller:** `Basic\TagController@ajaxGetListCategoryTag`

### Mục đích
Load danh sách tags và folders khi user chọn folder trong action type タグ.

### Request Parameters

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `group_id` | integer | ID folder tag. 0 = 未分類 |
| `action` | string | `'showGroup'` khi chọn folder |

### Response

```json
{
  "status": true,
  "groups": [{ "id": 1, "name": "タグフォルダ名" }],
  "tag_items": [{ "id": 1, "name": "タグ名" }],
  "items_default": [/* tags trong 未分類 */],
  "count_default": 5,
  "group_open": 0
}
```

**Độ tin cậy:** **Cao**

---

## EP-12: Lấy danh sách compliant statuses

**Method:** `POST`  
**URL:** `/ajax/init-status-chat`  
**Route name:** `ajaxGetStatusChat`  
**Controller:** `ChatController@ajaxGetStatusChat`

### Mục đích
Load danh sách 対応ステータス cho dropdown trong action type `compliant_status`. Được gọi khi Vue modal `created()` → `chooseCompliantStatus()`.

### Request Parameters
Không có.

### Response

```json
{
  "success": 1,
  "data": [
    { "id": 1, "name_status": "ステータス名" }
  ]
}
```

**Độ tin cậy:** **Cao** (xác nhận qua JS call tại `select_action.js:1087`)

---

## EP-13: Load filter data cho action

**Method:** `GET`  
**URL:** `/ajax/initDataFilterBroadcast`  
**Controller:** `Basic\BroadcastController` (hoặc FilterController)

### Mục đích
Khi user click 「絞込」 trên một action item — load filter đã lưu từ DB cho action detail đó. Chỉ gọi khi action chưa có filter data trong memory.

### Request Parameters

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `broadcastFilterId` | integer | ID của `t_actions_detail` |
| `parent_type` | string | `'modal_action'` |

### Response

```json
{
  "success": true,
  "broadcast_filter": [/* array filter conditions AND */],
  "broadcast_filter_or": [/* array filter conditions OR */]
}
```

**Độ tin cậy:** **Trung bình** (xác nhận qua JS call tại `select_action.js:350`, chưa đọc controller)

---

## EP-14: Bot data (plan type check)

**Method:** `POST`  
**URL:** `/ajax/get-bot-data`

### Mục đích
Kiểm tra plan type của bot để quyết định hiển thị filter button hay không. Được gọi khi Vue `created()`.

### Response

```json
{
  "plan_type": 1
}
```

`plan_type != 1` → filter button bị disabled (upgrade required). **Độ tin cậy:** **Trung bình**

---

## Tóm tắt URL mapping

| EP | Method | URL | Mục đích |
|----|--------|-----|---------|
| EP-01 | POST | `/ajax/action/init-data` | Load dữ liệu modal |
| EP-02 | POST | `/ajax/action/save` | Lưu action config |
| EP-03 | POST | `/ajax/action/delete-action-button` | Xóa action |
| EP-04 | POST | `/ajax/get-data-for-step-action` | Load scenarios theo folder |
| EP-05 | POST | `/ajax/get-data-for-template-action` | Load templates theo folder |
| EP-06 | POST | `/ajax/get-data-for-rich-menu-action` | Load rich menus theo folder |
| EP-07 | POST | `/ajax/get-list-remind` | Load remind events theo folder |
| EP-08 | POST | `/ajax/get-list-friend-info` | Load friend info fields theo folder |
| EP-09 | POST | `/ajax/get-list-group-friend-info` | Load friend info categories |
| EP-10 | POST | `/ajax/save-add-tag-in-modal-action` | Tạo tag mới inline |
| EP-11 | POST | `/ajax/get-list-group-tag` | Load tags theo folder |
| EP-12 | POST | `/ajax/init-status-chat` | Load compliant statuses |
| EP-13 | GET | `/ajax/initDataFilterBroadcast` | Load filter data |
| EP-14 | POST | `/ajax/get-bot-data` | Kiểm tra plan type |

**Lưu ý bảo mật:** Tất cả endpoints đều qua middleware `check_login` và `check_remember_token`. CSRF token được gửi qua header `X-CSRF-TOKEN`.
