# Logic Spec — Shared Component: Modal Filter / 絞り込み (SC-003)

**Controller chính**: `Basic\FilterController`  
**File**: `src/web/sns-line/app/Http/Controllers/Basic/FilterController.php` (1101 dòng)  
**Model chính**: `FilterV2` — `src/web/sns-line/app/FilterV2.php` (1075 dòng)  
**Confidence tổng thể**: Cao

---

## 1. Tổng quan kiến trúc Filter

Hệ thống filter có **hai phiên bản** song song:

| Phiên bản | Endpoint | Model | Đặc điểm |
|-----------|---------|-------|---------|
| **V1** (cũ) | `EP-02 /ajax/filter/get-list-user` | Truy vấn trực tiếp (không lưu DB) | Filter đơn giản theo tên/tag/ngày/scenario/conversion; trả kết quả ngay |
| **V2** (mới) | `EP-03 save-filter-v2`, `EP-04 init-data-filter` | `FilterV2` → bảng `filters_v2` | Filter phức tạp, lưu trạng thái vào DB; hỗ trợ AND/OR; dùng cho hầu hết tính năng mới |

Filter V2 được thiết kế theo kiến trúc **parent–child**: mỗi filter rule được lưu thành 1 record trong `filters_v2`, liên kết với entity cha qua `parent_type` + `parent_id`.

---

## 2. FilterController — Mô tả từng Method

### 2.1 `ajaxGetListUserFilter` (L.41–197) — Filter V1

**Luồng xử lý**:
1. Lấy `bot_id` từ session (`getBotId()`)
2. Build query `line_user JOIN bot_line_user` với `bot_line_user.bot_id = $bot_id`
3. Apply từng filter param theo thứ tự:
   - **name_filter**: split bởi `config('filter.name_delimiter')`, tìm LIKE trong cột tương ứng `name_filter_type`
     - type 1: `line_user.display_name`
     - type 2: `line_user.real_name`
     - type 3: `bot_line_user.view_name`
   - **tag_filter**: JOIN `tag_line_user`, lọc theo tag IDs + `tag_filter_option` (OR/AND/NOT)
   - **from/to_date_filter**: `bot_line_user.created_at` trong khoảng
   - **scenario_filter**: JOIN `scenario_lineuser`, lọc theo `scenario_filter_option`
   - **conversion_filter**: JOIN `conversion_result`, lọc theo conversion IDs + option
   - **mark_filter**: `bot_line_user.is_mark` (1=marked, 2=not_marked → `= 0`)
4. Trả về danh sách `line_user` + `num_user_count`

**Side effects**: Không có (read-only).

**Tables truy vấn**: `line_user`, `bot_line_user`, `tag_line_user`, `scenario_lineuser`, `conversion_result`

---

### 2.2 `ajaxGetTagsAndConversions` (L.203–239) — Load dữ liệu cho filter modal

**Luồng xử lý**:
1. Lấy `bot_id`
2. Nếu có `group_id`: lấy tags theo group; nếu không: lấy tags category mặc định
3. Lấy conversions của bot (`Conversion::getListConversion($bot_id, 0)`)
4. Trả về kết hợp: groups_tag + items_default + items_tag + conversions

**Side effects**: Không có (read-only).

**Tables truy vấn**: `category`, `tags`, `conversion`

---

### 2.3 `initDataFilter` (L.290–829) — Load trạng thái filter V2

**Đây là method phức tạp nhất** — tải toàn bộ trạng thái filter đã lưu và enrich data để hiển thị trong modal.

**Luồng xử lý**:
1. Xác định `parentId`:
   - Nếu có `copy_id`: dùng `copy_id` làm `parentId` (để copy filter từ bản gốc)
   - Nếu không: dùng `parent_id` từ request
2. Xác định `parentType`, `richMenuRedirectId`, `richMenuItemId` từ request
3. Query `filters_v2` theo `parent_type + parent_id + bot_id + operator='and'` → `listFilterAnd`
4. Query `filters_v2` theo `parent_type + parent_id + bot_id + operator='or'` → `listFilterOr`
5. Với `filter-rich-menu-toggle`: thêm điều kiện `rich_menu_redirect_id + rich_menu_item_id`
6. Với mỗi filter record, enrich data theo `type` (xem Bảng Enrich Data bên dưới)
7. Tính `number_filter` và `line_user_ids` qua `Conversation::advanceFilterPost()`
   - **Ngoại lệ**: bỏ qua tính toán khi `parent_type` là `step_message` hoặc `filter_manager`
   - **Ngoại lệ**: không trả `line_user_ids` khi `parent_type` là `broadcast` hoặc `filter_manager`
   - `cross_analysis`: gọi `advanceFilterPost` với flag `isCountOnly=true` riêng
   - Nếu có `richmenuId`: thêm WHERE `bot_line_user.rich_menu_id = $richmenuId`
8. Nếu `copy_id` không rỗng: clear ID trong tất cả filter items (set `id = ''`) → khi save sẽ tạo bản ghi mới

**Bảng Enrich Data theo filter type**:

| `type` | Data được enrich thêm |
|--------|----------------------|
| `tag` | `list_tags`: [{id, name}] của các tag đã chọn; `items_default_tag`; `group_open_tag=0`; `tag_items=[]` |
| `day_add_friend` | Đảm bảo `day_filter_type` tồn tại (mặc định 0); đảm bảo `duration_day_start/end` hoặc `modal_from/to_filter` tồn tại |
| `conversion` | `conversion_search` convert từ string sang array; `list_tags`: [{id, name}]; `conversion_list`; `check_all` |
| `scenario` | `scenario_name`; `open_group` (group_id của scenario); `scenario_list` |
| `qr_code` / `qr_code_action` | `list_qrs`: array chi tiết QR code; `items_default_landing`; `default_check_all`; `group_open_landing=0` |
| `friend_info` | `selected_name`; `open_group` (folder_id); `selected_list` |
| `status_chat` | `selected_list`: [{id, name_status}] |
| `affiliate` | `selected_list`: [{id, username}] |

**Side effects**: Không có (read-only).

---

### 2.4 `saveFilterV2` (L.831–1081) — Lưu filter V2

**Luồng xử lý**:
1. Tính `filterNumber` (số bạn bè khớp) trừ khi `parent_type` là `step_message` hoặc `filter_manager`
2. Gọi `FilterV2::saveFilter()` để upsert các filter records
3. Thực hiện side effects tùy theo `parent_type`:

**Side effects theo parent_type**:

| `parent_type` | Side Effect |
|---------------|-------------|
| `broadcast` | Update `broadcasts.filter_number` + `broadcasts.filter_date`; copy filter sang tất cả broadcast con (`parent_id`) |
| `setting_rich_menu` | Tạo/tìm `setting_display_rich_menu_histories` với status DRAFT; dùng history ID làm parent |
| `filter-rich-menu-toggle` + `filter_action_type=preview-rich-switch` | Update `rich_menu_switch_items.filter_ids` |
| `calendar-course-setting-status-send-after-booking` | Update `calendar_courses.filter_number_send_after_booking` + `filter_id_send_after_booking` |
| `calendar-salon-course-setting-status-send-after-booking` | Update `calendar_salon_courses.filter_number` + `filter_id` |
| `calendar-salon-staff-setting-status-send-after-booking` | Update `calendar_salon_staffs.filter_number` + `filter_id` |
| `calendar-setting-show-booking-form` | Update `calendar_managements.filter_number_show_booking` + `filter_id_show_booking` |
| `filter-calendar-salon-booking` | Update `calendar_salons.filter_calendar_salon_ids` + `number_filter_salon` |
| `filter_remind_form` | Update `event_steps.is_use_filter_remind` (0 nếu empty, 1 nếu có filter) |

**Validation Broadcast** (trước khi lưu):
- Không cho sửa nếu broadcast đang `status=delivering`
- Không cho sửa nếu broadcast đã `status=delivered`
- Không cho sửa nếu thời điểm hiện tại trong vòng 5 phút trước `send_day + send_time`

**Logic copy filter sang broadcast con**: Sau khi save filter cho broadcast cha, tìm tất cả broadcast có `parent_id = parentId`, xóa filter cũ của chúng, rồi copy filter của cha sang mỗi broadcast con.

**Side effects**: Ghi vào `filters_v2`; update các bảng liên quan tùy `parent_type`.

---

### 2.5 `getDataTagFilter` (L.1083–1100) — Load tag theo group

**Luồng xử lý**:
1. Nếu `group_id` rỗng: lấy tags có `category_id=0`, sắp xếp `position DESC, id DESC`
2. Nếu có `group_id`: lấy tags có `category_id=group_id`, sắp xếp `position DESC, id DESC`
3. Đếm `count_default` = số tag có `category_id=0`
4. Lấy toàn bộ category list

**Side effects**: Không có (read-only).

---

### 2.6 `ajaxListRichMenu` (L.275–288), `ajaxListFormAnswerRichMenu` (L.241–254), `ajaxListTemplateRichMenu` (L.256–273)

Ba method đơn giản: lấy toàn bộ records theo `bot_id`, không có logic phức tạp.

- `ajaxListRichMenu`: trả `RichMenus` theo `bot_id`
- `ajaxListFormAnswerRichMenu`: trả `FormAnswer` theo `bot_id`
- `ajaxListTemplateRichMenu`: trả `Template` theo `bot_id`, lọc `category_id >= 0` và `in_park = 0`, sắp xếp `sortRankItems()`

---

## 3. FilterV2 Model

**File**: `src/web/sns-line/app/FilterV2.php`  
**Table**: `filters_v2`  
**Primary key**: `id`  
**Timestamps**: `created_at`, `updated_at`  
**Guard**: `$guarded = []` (mass assignable tất cả)

### 3.1 Schema bảng `filters_v2`

```sql
CREATE TABLE `filters_v2` (
  `id`                   int(10) UNSIGNED NOT NULL,
  `bot_id`               int(11) DEFAULT NULL,
  `parent_type`          varchar(255) DEFAULT NULL,
  `parent_id`            int(11) DEFAULT NULL,
  `operator`             varchar(100) DEFAULT NULL,  -- 'and' hoặc 'or'
  `type`                 varchar(255) DEFAULT NULL,  -- loại filter (tag/conversion/scenario/...)
  `data`                 text,                       -- JSON encode của filter data
  `text_preview`         text,                       -- Text preview hiển thị trên UI
  `created_at`           timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at`           timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `rich_menu_item_id`    int(11) DEFAULT NULL,
  `rich_menu_redirect_id` int(11) DEFAULT NULL
);
```

**Confidence Schema**: Cao (đọc trực tiếp từ `db/schema/tables/filters_v2.sql`)

### 3.2 Cột quan trọng

| Cột | Mô tả | Giá trị ví dụ |
|-----|-------|---------------|
| `bot_id` | Bot LINE OA sở hữu filter | 100 |
| `parent_type` | Loại entity cha | `broadcast`, `step_message`, `filter_manager`, v.v. |
| `parent_id` | ID của entity cha | ID của broadcast, calendar, v.v. |
| `operator` | Toán tử logic | `and` hoặc `or` |
| `type` | Loại điều kiện filter | `tag`, `conversion`, `scenario`, `day_add_friend`, `qr_code`, `qr_code_action`, `friend_info`, `status_chat`, `affiliate` |
| `data` | JSON chứa chi tiết điều kiện | `{"tags_search":[1,2],"tag_option":1}` |
| `text_preview` | Text hiển thị tóm tắt filter | `"タグ: VIP, Regular"` |
| `rich_menu_item_id` | Chỉ dùng cho `filter-rich-menu-toggle` | ID của rich menu item |
| `rich_menu_redirect_id` | Chỉ dùng cho `filter-rich-menu-toggle` | ID của rich menu redirect |

### 3.3 Static Methods của FilterV2

**`saveFilter($filterAnd, $filterOr, $parentType, $parentId, $richMenuRedirectId, $richMenuItemId)`** (L.18–328):
- Upsert filter records: nếu item có `id` → update; nếu không → tạo mới
- Xóa các filter records cũ không còn trong danh sách gửi lên
- Pre-process data trước khi lưu theo `type` (xem Bảng Pre-process bên dưới)
- Trả về `$arrIdFilter`: mảng IDs các filter đã lưu

**`saveFilterCrossAnalysis($filterAnd, $filterOr, $botId, $parentType, $idParent)`** (L.330–569):
- Luồng tương tự `saveFilter` nhưng **luôn INSERT mới** (không update)
- Không xóa records cũ
- Dùng riêng cho tính năng Cross Analysis

**`initDataFilter($parentId, $parentType, $copyId, $botId)`** (L.571–1034):
- Static version của `FilterController::initDataFilter` — cùng logic nhưng gọi từ code PHP khác (không phải HTTP request)
- Trả về array: `['item_search', 'item_search_or', 'number_filter', 'line_user_ids']`

**`deleteActionFilters($actionDetailIds)`** (L.1036–1040):
- Xóa filter có `parent_type='modal_action'` và `parent_id` trong danh sách `$actionDetailIds`

**`deleteActionFilterByAction($action_id)`** (L.1042–1047):
- Tìm tất cả `action_details` của action → xóa filter tương ứng

**`deleteActionFilterByActions($action_ids)`** (L.1049–1054):
- Batch xóa filters cho nhiều actions

**`cloneFilters($parentId, $newParentId, $parentType, $options)`** (L.1056–1074):
- Clone toàn bộ filter từ `parentId` sang `newParentId` (replicate records)
- Trả về mảng IDs của filters đã clone

**Bảng Pre-process data trước khi lưu** (áp dụng cho cả AND và OR):

| `type` | Pre-process |
|--------|-------------|
| `tag` | Bỏ qua nếu `tags_search` rỗng; unset `group_open_tag`, `list_tags`, `tag_items`, `items_default_tag`, `check_all` |
| `day_add_friend` | Cast `day_filter_type` sang int; nếu type=0 unset range; nếu type=1 unset duration |
| `qr_code` / `qr_code_action` | Bỏ qua nếu `qrs_search` rỗng; unset display fields |
| `conversion` | Bỏ qua nếu `conversion_search` rỗng; convert array sang string (implode ','); unset display fields |
| `friend_info` | Normalize day/month từ 1-9 → '01'-'09'; normalize `limit_date` → int 0/1; unset display fields |
| `scenario` | Bỏ qua nếu `scenario_search` rỗng; unset `scenario_list`, `open_group` |
| `status_chat` | Bỏ qua nếu `status_chat_search` rỗng; unset `selected_list` |
| `affiliate` | Bỏ qua nếu `affiliate_search` rỗng; unset `selected_list` |

---

## 4. Models liên quan và cách dùng

| Model | Table | Cách dùng trong Filter |
|-------|-------|------------------------|
| `Tags` | `tags` | Lấy tên tag theo ID; list tag theo bot/category |
| `Category` | `categories` | `getCategoryTagDefault()`, `getCategoryLandingDefault()`, `getListCategoryTag()` |
| `Conversion` | `conversions` | `getListConversion($bot_id, $folder_id)`; lấy tên conversion theo ID |
| `Scenario` | `scenarios` | Lấy tên + group_id của scenario; `getScenarioBot($bot_id, $folder_id)` |
| `Landing` | `landings` | Lấy chi tiết QR code theo IDs |
| `FriendInformationSetting` | `friend_information_settings` | Lấy tên trường thông tin bạn bè; `getFriendInfoSettingByFolderId()` |
| `StatusChat` | `status_chats` | Lấy danh sách status chat đã chọn |
| `Affiliaters` | `affiliaters` | Lấy danh sách affiliate đã chọn |
| `BroadCast` | `broadcasts` | Kiểm tra status; update filter_number/filter_date |
| `Conversation` | `conversations` | `advanceFilterPost()` — engine thực sự tính số bạn bè khớp filter |
| `RichMenus` | `rich_menus` | List rich menus theo bot |
| `RichMenuSwitchItem` | `rich_menu_switch_items` | Update `filter_ids` |
| `SettingDisplayRichMenuHistory` | `setting_display_rich_menu_histories` | Tạo bản nháp DRAFT cho rich menu setting |
| `CalendarCourse` | `calendar_courses` | Update filter_id sau save |
| `CalendarSalonCourse` | `calendar_salon_courses` | Update filter_id sau save |
| `CalendarSalonStaff` | `calendar_salon_staffs` | Update filter_id sau save |
| `CalendarManagement` | `calendar_managements` | Update filter_id_show_booking sau save |
| `CalendarSalon` | `calendar_salons` | Update filter_calendar_salon_ids sau save |
| `EventStep` | `event_steps` | Update `is_use_filter_remind` sau save |
| `FormAnswer` | `form_answers` | List form answers theo bot |
| `Template` | `templates` | List templates theo bot |
| `Bots` | `bots` | Lấy `domain_url_shorten` để build URL QR code |
| `ActionDetail` | `action_details` | Lấy action details cho QR code; dùng để xóa filter khi xóa action |

**Engine lọc chính**: `Conversation::advanceFilterPost($bot_id, $itemFilterAnd, $itemFilterOr, $keyword, false, [], true, $isCrossAnalysis)`

---

## 5. Các Config Values (filter.*)

File config: `config/filter.php` (suy luận từ usage trong code)

| Config key | Giá trị | Mô tả |
|------------|---------|-------|
| `filter.name_delimiter` | (chuỗi phân cách) | Delimiter để split `name_filter` thành nhiều từ tìm kiếm |
| `filter.name_filter_type.name` | `1` | Filter theo LINE登録名 (display_name) |
| `filter.name_filter_type.real_name` | `2` | Filter theo 本名 (real_name) |
| `filter.name_filter_type.view_name` | `3` | Filter theo システム表示名 (view_name trên bot) |
| `filter.tag_filter_option.or_filter` | `0` | Tag: bất kỳ 1 tag (OR) |
| `filter.tag_filter_option.and_filter` | `1` | Tag: tất cả tag (AND) |
| `filter.tag_filter_option.or_not_filter` | `2` | Tag: loại trừ bất kỳ tag nào (OR NOT) |
| `filter.tag_filter_option.and_not_filter` | `3` | Tag: loại trừ tất cả tag (AND NOT) |
| `filter.scenario_filter_option.apply_scenario` | `0` | Đang đăng ký scenario |
| `filter.scenario_filter_option.not_apply_scenario` | `1` | Không đăng ký scenario |
| `filter.scenario_filter_option.apply_scenario_with_start_day` | `2` | Đã gửi đến ngày X |
| `filter.scenario_filter_option.done_scenario` | `3` | Đã đọc xong scenario |
| `filter.scenario_filter_option.not_done_scenario` | `4` | Chưa đọc xong scenario |
| `filter.conversion_filter_option.or_filter` | `0` | Conversion: bất kỳ (OR) |
| `filter.conversion_filter_option.and_filter` | `1` | Conversion: tất cả (AND) |
| `filter.conversion_filter_option.or_not_filter` | `2` | Conversion: loại trừ bất kỳ (OR NOT) |
| `filter.conversion_filter_option.and_not_filter` | `3` | Conversion: loại trừ tất cả (AND NOT) |

Config bổ sung (từ `config('sns-line.*')`):

| Config key | Mô tả |
|------------|-------|
| `sns-line.info_default_info` | Danh sách trường thông tin bạn bè mặc định (id <= -1) |
| `sns-line.info_default_info_address` | Danh sách trường thông tin địa chỉ mặc định (id <= -7 hoặc 'd_6') |

**Confidence Config**: Cao (đọc trực tiếp từ code)

---

## 6. Business Rules quan trọng

### 6.1 V1 vs V2

- **Filter V1** (`ajaxGetListUserFilter`): Filter đơn giản, không lưu DB, chỉ trả danh sách bạn bè. Dùng cho Broadcast V1 và Friend List cũ.
- **Filter V2** (`initDataFilter` + `saveFilterV2`): Filter phức tạp có state, lưu vào `filters_v2`. Hỗ trợ nhiều điều kiện phức tạp (AND + OR), nhiều type filter. Dùng cho hầu hết tính năng từ V2 trở đi.

### 6.2 AND vs OR logic

- `operator='and'`: tất cả điều kiện AND phải thỏa mãn đồng thời
- `operator='or'`: ít nhất một điều kiện OR phải thỏa mãn
- Kết quả cuối: `(AND điều kiện 1) VÀ (AND điều kiện 2) VÀ ... VÀ (OR điều kiện A HOẶC OR điều kiện B HOẶC ...)`
- Engine: `Conversation::advanceFilterPost()` nhận cả hai mảng AND + OR để tính

### 6.3 Mark Filter Values

| Giá trị `mark_filter` | Ý nghĩa | Điều kiện SQL |
|----------------------|---------|---------------|
| `1` | Đã đánh dấu (marked) | `bot_line_user.is_mark = 1` |
| `2` | Chưa đánh dấu (not marked) | `bot_line_user.is_mark = 0` |
| không truyền / null | Không lọc theo mark | Không có điều kiện |

### 6.4 parent_type quyết định behavior

Giá trị `parent_type` là chìa khóa điều hướng toàn bộ logic:
- Quyết định có tính `filterNumber` không
- Quyết định có trả `line_user_ids` không
- Quyết định side effect nào được thực hiện sau khi save
- Quyết định cách query `filters_v2` (có thêm điều kiện `rich_menu_*` hay không)

### 6.5 Copy/Clone Filter

- **Copy via `copy_id`**: Khi `initDataFilter` nhận `copy_id`, load filter của bản gốc nhưng clear ID → khi user save sẽ tạo bản mới thay vì overwrite
- **Clone via `FilterV2::cloneFilters()`**: Copy toàn bộ filter records sang parent mới (dùng khi duplicate entity)
- **Cascade copy cho broadcast**: Khi save filter của broadcast cha, tự động copy sang tất cả broadcast con (`BroadCast.parent_id`)

### 6.6 Broadcast Protection

Trước khi cho phép save filter, kiểm tra trạng thái broadcast:
- `delivering`: đang phát — chặn hoàn toàn
- `delivered`: đã phát xong — chặn hoàn toàn
- Trong vòng 5 phút trước giờ gửi (`send_day + send_time - 6 phút <= now`): chặn nếu status không phải `draft`

### 6.7 friend_info type — ID đặc biệt

Trường thông tin bạn bè (`friend_info`) sử dụng hệ thống ID:
- ID > 0: `FriendInformationSetting` record tùy chỉnh của bot
- ID <= -1 và > -7: trường thông tin mặc định từ `config('sns-line.info_default_info')`
- ID <= -7 hoặc `= 'd_6'`: trường thông tin địa chỉ từ `config('sns-line.info_default_info_address')`
- Folder ID = -1: không thuộc folder nào (root)
- Folder ID = -2: nhóm địa chỉ mặc định

### 6.8 day_add_friend type — Hai chế độ

Filter theo ngày kết bạn có hai chế độ (`day_filter_type`):
- `day_filter_type = 0`: Khoảng thời gian (duration) — dùng `duration_day_start` + `duration_day_end` (số ngày)
- `day_filter_type = 1`: Khoảng ngày tuyệt đối — dùng `modal_from_filter` + `modal_to_filter` (date)

Khi lưu: chỉ lưu fields của chế độ đang dùng, unset fields của chế độ kia.

### 6.9 conversion_search — Lưu dạng string

Conversion IDs được lưu trong `data` dưới dạng **chuỗi phân cách bởi dấu phẩy** (implode ','). Khi đọc ra phải `explode(',', ...)` để convert sang array.

### 6.10 QR Code URL — Domain tùy chỉnh

Khi build URL cho QR code:
1. Ưu tiên `bots.domain_url_shorten` (domain tùy chỉnh của bot)
2. Nếu không có: dùng `env('URL_OUTSIDE_STEP')`
3. Lấy path từ `link_qr_code` (split '/', lấy segment 3 và 4)

### 6.11 setting_rich_menu — Parent ID thay đổi

Khi `parent_type = 'setting_rich_menu'`:
1. Tìm hoặc tạo `SettingDisplayRichMenuHistory` với `status = DRAFT`
2. **ParentID được đổi sang ID của history record** (không phải ID của rich menu)
3. Trả `parentIdNew` trong response để frontend cập nhật

---

## 7. Luồng gọi API theo tính năng

### 7.1 Luồng chuẩn khi mở modal filter

```
User click nút filter
  → Frontend gọi EP-04 initDataFilter (parent_type, parent_id)
  → Server trả item_search (AND) + item_search_or (OR) + number_filter
  → Frontend hiển thị modal với trạng thái đã lưu
  → User chỉnh sửa filter
  → Frontend gọi EP-03 saveFilterV2 
  → Server lưu vào filters_v2, tính lại number_filter
  → Server update entity cha nếu cần (broadcast, calendar, v.v.)
  → Frontend đóng modal, cập nhật số bạn bè hiển thị
```

### 7.2 Luồng lazy load tag

```
User click mở accordion nhóm tag trong modal
  → Frontend gọi EP-05 getDataTagFilter (group_id)
  → Server trả tags thuộc group
  → Frontend render danh sách tag
```

### 7.3 Luồng filter V1 (Broadcast cũ / Friend List)

```
User chọn điều kiện filter (tên, tag, ngày, scenario, conversion)
  → Frontend gọi EP-02 ajaxGetListUserFilter với các params
  → Server tính real-time, trả số lượng bạn bè + danh sách
  → Frontend cập nhật "X人" (số người)
```

### 7.4 Luồng copy filter

```
User click "コピー" (copy)
  → Frontend gọi EP-04 initDataFilter với copy_id = ID bản gốc
  → Server load filter của bản gốc, clear ID fields
  → User có thể chỉnh sửa, save sẽ tạo filter mới
```
