# API Spec — Shared Component: Modal Filter / 絞り込み (SC-003)

**Controller chính**: `Basic\FilterController`  
**File**: `src/web/sns-line/app/Http/Controllers/Basic/FilterController.php` (1101 dòng)  
**Middleware**: `auth` (toàn bộ route đều yêu cầu xác thực)  
**Confidence tổng thể**: Cao

---

## Danh sách Endpoints

| EP | Method | URL | Controller@Method | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-01 | POST | `/ajax/filter/get-list-tags-and-conversions` | `Basic\FilterController@ajaxGetTagsAndConversions` | Lấy danh sách tag categories + tags + conversions cho modal filter |
| EP-02 | POST | `/ajax/filter/get-list-user` | `Basic\FilterController@ajaxGetListUserFilter` | Lấy danh sách bạn bè theo bộ lọc V1 (filter cũ) |
| EP-03 | POST | `/ajax/filter/save-filter-v2` | `Basic\FilterController@saveFilterV2` | Lưu bộ lọc V2 và tính số bạn bè khớp |
| EP-04 | POST | `/ajax/init-data-filter` | `Basic\FilterController@initDataFilter` | Khởi tạo dữ liệu filter V2 khi mở modal |
| EP-05 | POST | `/ajax/get-list-group-tag-filter` | `Basic\FilterController@getDataTagFilter` | Lấy danh sách tag theo group (category) |
| EP-06 | POST | `/ajax/get-list-rich-menu` | `Basic\FilterController@ajaxListRichMenu` | Lấy danh sách rich menu của bot |
| EP-07 | POST | `/ajax/get-list-form-answer-rich-menu` | `Basic\FilterController@ajaxListFormAnswerRichMenu` | Lấy danh sách form answers (dùng cho rich menu filter) |
| EP-08 | POST | `/ajax/get-list-template-rich-menu` | `Basic\FilterController@ajaxListTemplateRichMenu` | Lấy danh sách templates (dùng cho rich menu filter) |

---

## Chi tiết từng Endpoint

### EP-01 — Lấy Tags & Conversions cho filter

**Method**: `POST`  
**URL**: `/ajax/filter/get-list-tags-and-conversions`  
**Route name**: `ajaxGetTagsAndConversions`  
**Controller@Method**: `Basic\FilterController@ajaxGetTagsAndConversions` (L.203-239)

#### Request Parameters

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `group_id` | body | int | Không | ID nhóm tag (category). Nếu không truyền: lấy tag không phân nhóm |

#### Response JSON

```json
{
  "status": true,
  "groups_tag": [
    { "id": 1, "name": "Nhóm A" }
  ],
  "items_default": [
    { "id": 0, "name": "未分類", "count": 5 }
  ],
  "group_open": 0,
  "count_default": 10,
  "items_tag": [
    { "id": 1, "name": "Tag VIP", "bot_id": 100 }
  ],
  "conversions": [
    { "id": 1, "name": "Conversion A" }
  ]
}
```

**Ghi chú**:
- `items_default`: tag categories (từ `Category::getCategoryTagDefault()`)
- `groups_tag`: danh sách category từ `Category::getListCategoryTag()`
- `items_tag`: tags thuộc group_id, lọc theo `bot_id`
- `conversions`: tất cả conversion của bot (từ `Conversion::getListConversion($bot_id, 0)`)

**Confidence**: Cao

**Context sử dụng**: Dùng khi mở modal filter để load danh sách tag và conversion để người dùng chọn.

---

### EP-02 — Lấy danh sách bạn bè theo filter V1

**Method**: `POST`  
**URL**: `/ajax/filter/get-list-user`  
**Route name**: `ajaxGetListUserFilter`  
**Controller@Method**: `Basic\FilterController@ajaxGetListUserFilter` (L.41-197)

#### Request Parameters

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `name_filter` | body | string | Không | Tên bạn bè (nhiều từ ngăn cách bằng delimiter từ config `filter.name_delimiter`) |
| `name_filter_type` | body | int | Không | Loại tên: `1`=LINE登録名, `2`=本名, `3`=システム表示名 |
| `tag_filter` | body | array/string | Không | Danh sách tag ID để lọc |
| `tag_filter_option` | body | int | Không | `0`=OR (bất kỳ tag), `1`=AND (tất cả tag), `2`=OR NOT, `3`=AND NOT |
| `from_date_filter` | body | date | Không | Ngày kết bạn từ (Y-m-d) |
| `to_date_filter` | body | date | Không | Ngày kết bạn đến (Y-m-d) |
| `scenario_filter` | body | int | Không | ID scenario để lọc |
| `scenario_filter_option` | body | int | Không | `0`=đang đăng ký, `1`=không đăng ký, `2`=gửi đến ngày X, `3`=đã đọc xong, `4`=chưa đọc xong |
| `scenario_start_day_filter` | body | date | Không | Ngày bắt đầu scenario (dùng khi `scenario_filter_option=2`) |
| `conversion_filter` | body | array/string | Không | Danh sách conversion ID |
| `conversion_filter_option` | body | int | Không | `0`=OR, `1`=AND, `2`=OR NOT, `3`=AND NOT |
| `mark_filter` | body | int | Không | Lọc theo trạng thái đánh dấu: `1`=marked, `2`=not_marked |

#### Response JSON

```json
{
  "status": true,
  "line_user": [
    {
      "id": 123,
      "display_name": "Yamada Taro",
      "picture_url": "https://...",
      "...": "..."
    }
  ],
  "num_user_count": 42
}
```

**Ghi chú**:
- Join `line_user` + `bot_line_user`, lọc theo `bot_id` hiện tại
- Tables truy vấn: `line_user`, `bot_line_user`, `tag_line_user`, `scenario_lineuser`, `conversion_result`, `conversation`
- Đây là filter **V1** (cũ) — dùng cho các tính năng chưa migrate sang filter V2

**Confidence**: Cao

**Context sử dụng**: Broadcast filter V1, friend list filter V1 — các tính năng dùng bộ lọc đơn giản (chưa dùng V2).

---

### EP-03 — Lưu bộ lọc V2

**Method**: `POST`  
**URL**: `/ajax/filter/save-filter-v2`  
**Route name**: `save_filter_v2`  
**Controller@Method**: `Basic\FilterController@saveFilterV2` (L.831-1081)

#### Request Parameters

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `parent_type` | body | string | Có | Context sử dụng filter (xem bảng parent_type bên dưới) |
| `parent_id` | body | int | Có* | ID của entity cha (broadcast ID, calendar ID, v.v.) — có thể null cho một số `parent_type` |
| `item_search` | body | JSON string | Không | Mảng filter điều kiện AND (JSON encode) |
| `item_search_or` | body | JSON string | Không | Mảng filter điều kiện OR (JSON encode) |
| `keyword` | body | string | Không | Keyword tìm kiếm bổ sung |
| `richMenuRedirectId` | body | int | Không | ID rich menu redirect (chỉ dùng khi `parent_type=filter-rich-menu-toggle`) |
| `richMenuItemId` | body | int | Không | ID rich menu item (chỉ dùng khi `parent_type=filter-rich-menu-toggle`) |
| `filter_action_type` | body | string | Không | `preview-rich-switch` — cập nhật `filter_ids` vào `rich_menu_switch_items` |

**Bảng giá trị `parent_type` được hỗ trợ**:

| Giá trị | Entity | Ghi chú |
|---------|--------|---------|
| `broadcast` | Broadcast | Lưu filter vào broadcast + broadcast con, update `filter_number`, `filter_date` |
| `broadcast-v2` | Broadcast V2 | Tương tự broadcast |
| `step_message` | Step message | KHÔNG tính `filterNumber` (bỏ qua count) |
| `filter_manager` | Filter Manager | KHÔNG tính `filterNumber` |
| `cross_analysis` | Cross Analysis | Dùng `advanceFilterPost` với flag `cross_analysis=true` |
| `action_schedule` | Action Schedule | Không cần `parent_id` |
| `calendar-course-setting-status-send-after-booking` | Calendar Course | Update `filter_number_send_after_booking`, `filter_id_send_after_booking` |
| `calendar-salon-course-setting-status-send-after-booking` | Salon Course | Update `filter_number`, `filter_id` |
| `calendar-salon-staff-setting-status-send-after-booking` | Salon Staff | Update `filter_number`, `filter_id` |
| `calendar-setting-show-booking-form` | Calendar Management | Update `filter_number_show_booking`, `filter_id_show_booking` |
| `filter-calendar-salon-booking` | Salon | Update `filter_calendar_salon_ids`, `number_filter_salon` |
| `filter_remind_form` | Event Step | Update `is_use_filter_remind` (0 hoặc 1) |
| `setting_rich_menu` | Rich Menu | Tạo/tìm `SettingDisplayRichMenuHistory` với status DRAFT, dùng ID history làm `parent_id` |
| `filter-rich-menu-toggle` | Rich Menu Switch | Filter riêng theo `rich_menu_redirect_id` + `rich_menu_item_id` |

#### Response JSON

```json
{
  "success": true,
  "msg": "",
  "number_filter": 150,
  "filter_date": "2024-01-15 10:30:00",
  "preview_filter_broadcast": null,
  "line_user_ids": [
    { "line_user_id": "Uxxxxxxxx" }
  ],
  "array_filter_id": [1, 2, 3],
  "parentIdNew": 42
}
```

**Ghi chú**:
- `number_filter`: số lượng bạn bè khớp filter
- `preview_filter_broadcast`: chỉ có giá trị khi broadcast — `"全員"` (delivered/delivering không filter) hoặc `"未設定（全員）"` (draft không filter)
- `line_user_ids`: chỉ trả về khi `parent_type` khác `broadcast` và `filter_manager`
- `array_filter_id`: danh sách IDs của filter records đã lưu vào `filters_v2`
- `parentIdNew`: ID của parent sau khi xử lý (có thể khác `parent_id` nếu `parent_type=setting_rich_menu`)

**Lỗi đặc biệt**:
- Broadcast đang delivering: `{ "success": false, "msg": "配信処理中です。編集できません。" }`
- Broadcast đã delivered: `{ "success": false, "msg": "既に配信済のため変更できません。" }`
- Broadcast trong vòng 5 phút trước giờ gửi: `{ "success": false, "msg": "配信予定日時5分前からは配信内容の編集はできません。" }`

**Confidence**: Cao

**Context sử dụng**: Tất cả tính năng dùng filter V2 — broadcast, calendar, rich menu, filter manager, cross analysis, action schedule, step message.

---

### EP-04 — Khởi tạo dữ liệu filter V2 (load trạng thái đã lưu)

**Method**: `POST`  
**URL**: `/ajax/init-data-filter`  
**Route name**: `initDataFilter`  
**Controller@Method**: `Basic\FilterController@initDataFilter` (L.290-829)

#### Request Parameters

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `parent_type` | body | string | Có | Context sử dụng (cùng danh sách với EP-03) |
| `parent_id` | body | int | Có* | ID của entity cha |
| `copy_id` | body | int | Không | ID bản gốc khi copy — nếu có thì load filter của `copy_id`, clear ID trong response (để tạo mới khi save) |
| `richMenuRedirectId` | body | int | Không | ID rich menu redirect (cho `filter-rich-menu-toggle`) |
| `richMenuItemId` | body | int | Không | ID rich menu item (cho `filter-rich-menu-toggle`) |
| `richmenuId` | body | int | Không | ID rich menu để filter thêm theo `bot_line_user.rich_menu_id` |

#### Response JSON

```json
{
  "success": true,
  "msg": "",
  "item_search": [
    {
      "id": 1,
      "type": "tag",
      "preview": "タグ: VIP, Regular",
      "tags_search": [10, 20],
      "list_tags": [
        { "id": 10, "name": "VIP" },
        { "id": 20, "name": "Regular" }
      ],
      "items_default_tag": [...],
      "group_open_tag": 0,
      "tag_items": [],
      "active": true
    }
  ],
  "item_search_or": [...],
  "number_filter": 75,
  "line_user_ids": [
    { "line_user_id": "Uxxxxxxxx" }
  ],
  "richmenuId": null
}
```

**Ghi chú**:
- `item_search`: mảng filter điều kiện AND đã lưu, đã được enrich data (tag names, scenario names, v.v.)
- `item_search_or`: mảng filter điều kiện OR đã lưu
- Mỗi filter item được enrich thêm thông tin display tùy theo `type` (xem Logic Spec)
- `number_filter` và `line_user_ids` KHÔNG tính khi `parent_type` là `step_message` hoặc `filter_manager`
- `line_user_ids` KHÔNG trả về khi `parent_type` là `broadcast` hoặc `filter_manager`

**Confidence**: Cao

**Context sử dụng**: Gọi khi mở modal filter để load trạng thái filter đã lưu từ lần trước.

---

### EP-05 — Lấy danh sách tag theo group

**Method**: `POST`  
**URL**: `/ajax/get-list-group-tag-filter`  
**Route name**: `ajaxGetListCategoryTag`  
**Controller@Method**: `Basic\FilterController@getDataTagFilter` (L.1083-1100)

#### Request Parameters

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `group_id` | body | int | Không | ID nhóm tag. Nếu không truyền hoặc rỗng: lấy tag có `category_id=0` (未分類) |

#### Response JSON

```json
{
  "tags": [
    { "id": 1, "name": "VIP", "bot_id": 100, "category_id": 0, "position": 5 }
  ],
  "groups": [
    { "id": 1, "name": "Nhóm A" }
  ],
  "count_default": 3,
  "group_open": 0
}
```

**Ghi chú**:
- `tags`: lọc theo `bot_id` + `category_id`, sắp xếp `position DESC, id DESC`
- `groups`: từ `Category::getListCategoryTag()` — toàn bộ category tag của hệ thống
- `count_default`: số tag có `category_id=0` (未分類)
- `group_open`: echo lại `group_id` đã nhận (0 nếu không truyền)

**Confidence**: Cao

**Context sử dụng**: Lazy load tag theo group khi người dùng expand accordion trong modal filter.

---

### EP-06 — Lấy danh sách Rich Menu

**Method**: `POST`  
**URL**: `/ajax/get-list-rich-menu`  
**Route name**: `ajaxListRichMenu`  
**Controller@Method**: `Basic\FilterController@ajaxListRichMenu` (L.275-288)

#### Request Parameters

Không có parameters.

#### Response JSON

```json
{
  "list_rich_menu": [
    { "id": 1, "name": "Rich Menu A", "bot_id": 100 }
  ]
}
```

**Confidence**: Cao

**Context sử dụng**: Load danh sách rich menu để filter bạn bè theo rich menu đang áp dụng. Dùng trong filter type `rich_menu`.

---

### EP-07 — Lấy danh sách Form Answers (cho Rich Menu filter)

**Method**: `POST`  
**URL**: `/ajax/get-list-form-answer-rich-menu`  
**Route name**: `ajaxListFormAnswerRichMenu`  
**Controller@Method**: `Basic\FilterController@ajaxListFormAnswerRichMenu` (L.241-254)

#### Request Parameters

Không có parameters.

#### Response JSON

```json
{
  "list_form_answer": [
    { "id": 1, "bot_id": 100, "name": "Form Answer A" }
  ]
}
```

**Confidence**: Cao

**Context sử dụng**: Dùng trong rich menu filter để chọn form answer làm điều kiện hiển thị rich menu.

---

### EP-08 — Lấy danh sách Templates (cho Rich Menu filter)

**Method**: `POST`  
**URL**: `/ajax/get-list-template-rich-menu`  
**Route name**: `ajaxListTemplateRichMenu`  
**Controller@Method**: `Basic\FilterController@ajaxListTemplateRichMenu` (L.256-273)

#### Request Parameters

Không có parameters.

#### Response JSON

```json
{
  "list_template": [
    { "id": 1, "name": "Template A", "bot_id": 100, "category_id": 1, "in_park": 0 }
  ]
}
```

**Ghi chú**:
- Lọc template có `category_id >= 0` và `in_park = 0` (không phải template hệ thống)
- Sắp xếp theo hàm `sortRankItems()` (helper function)

**Confidence**: Cao

**Context sử dụng**: Dùng trong rich menu filter để chọn template làm điều kiện hiển thị rich menu.

---

## Endpoint bổ sung (từ BroadcastController)

### EP-09 — Lưu filter cho Broadcast (V1 style)

**Method**: `POST`  
**URL**: `/basic/message-send-all/store-broadcast`  
**Controller@Method**: `BroadcastController@storeBroadcast` (hoặc tương đương)  
**Tham số đặc biệt**: `action=save_filter`

**Ghi chú**: Broadcast có một luồng lưu filter riêng qua `store-broadcast` với `action=save_filter` — khác với EP-03. Cần xác minh thêm từ BroadcastController.

**Confidence**: Trung bình
