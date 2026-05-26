# FA-003 Tự động trả lời「自動応答」— Logic Spec

> Phân tích từ source code Laravel (`src/web/`).
> Confidence: **Cao** — đọc trực tiếp từ code.

---

## Controllers

### Basic\ReplyController
- **File**: `app/Http/Controllers/Basic/ReplyController.php` (1085 dòng)
- **Namespace**: `App\Http\Controllers\Basic`
- **Dependency Injection**: `ScenarioRepositoryInterface` (constructor)

---

#### Action: index()
- **Route**: GET `/basic/reply` (EP-01)
- **Chức năng**: Hiển thị trang danh sách quy tắc tự động trả lời
- **Luồng xử lý**:
  1. Lấy `bot_id` từ session qua helper `getBotId()`
  2. Đọc cookie `folder_reply` → lấy `folderId` cho bot hiện tại
  3. Kiểm tra folder tồn tại trong bảng `category` (kind=reply, is_deleted=0)
  4. Nếu folder không tồn tại hoặc chưa set → reset về `0` (未分類), cập nhật cookie
  5. Trả về view `basic.reply.index` với `folderCookie`
- **Side effects**: Có thể ghi lại cookie `folder_reply` nếu folder không hợp lệ
- **Gọi đến**: `Category::query()`, `Cookie::queue()`
- **Tin cậy**: **Cao** — `ReplyController.php:53-69`

---

#### Action: create()
- **Route**: GET `/basic/reply/new` (EP-02)
- **Chức năng**: Hiển thị form tạo mới (hoặc chỉnh sửa/sao chép) quy tắc
- **Luồng xử lý**:
  1. Lấy `bot_id`, `reply_id`, `copy_id`, `group_id` từ request
  2. Nếu có `reply_id` → kiểm tra `AutoReply` tồn tại cho bot → nếu không tồn tại, redirect `/basic/reply`
  3. Lấy danh sách folders (Category kind=reply, is_deleted=0, bot_id)
  4. Lấy danh sách scenarios cho bot
  5. Lấy danh sách conversions cho bot
  6. Lấy danh sách Rich Menus đang hoạt động (`status_rich=1`)
  7. Lấy danh sách StatusChat cho bot
  8. Trả về view `basic.reply.create_v2`
- **Gọi đến**: `AutoReply`, `Category`, `ScenarioRepository`, `Conversion`, `RichMenus`, `StatusChat`
- **Tin cậy**: **Cao** — `ReplyController.php:75-110`

---

#### Action: edit()
- **Route**: GET `/basic/reply/edit/{item_id}` (EP-03)
- **Chức năng**: Hiển thị form chỉnh sửa quy tắc (flow legacy)
- **Luồng xử lý**:
  1. Lấy `item_id` từ URL path
  2. Tìm `AutoReply` theo id + bot_id → nếu không tồn tại, redirect `/basic/reply`
  3. Lấy danh sách folders, scenarios, templates (theo category)
  4. Nếu quy tắc có `add_tag_ids`/`remove_tag_ids` → load Tags tương ứng
  5. Nếu `reply_kind=2` (template) → load template để lấy `category_id`
  6. Load dữ liệu filter cũ (model `Filter`) → chuyển đổi sang array qua `Filter::convertFilterToEditArray()`
  7. Trả về view `basic.reply.edit`
- **Gọi đến**: `AutoReply`, `Category`, `Scenario`, `Tags`, `Template`, `Filter`
- **Tin cậy**: **Cao** — `ReplyController.php:231-279`

---

#### Action: store()
- **Route**: POST `/basic/reply/store` (EP-04)
- **Chức năng**: Tạo mới quy tắc tự động trả lời (flow legacy)
- **Luồng xử lý**:
  1. Ghi log action "create auto reply"
  2. Thu thập dữ liệu từ request: `group_id`, `type`, `rule_mix`, `step_to_change`, `is_active`, `only_once`, `use_reply`, `step_to_id`
  3. Gọi `validateAutoReplay()` — nếu có lỗi, redirect back
  4. **Kiểm tra backup**: Tìm `BackupHistory` đang chạy (status 0 hoặc 1) cho bot → nếu có, trả lỗi 500
  5. Xử lý reply_content:
     - `use_reply=1` (text): base64_encode nội dung text
     - `use_reply=2` (template): lưu template ID (`egg_id`)
  6. Xử lý scenario:
     - `scenario_type=1` (timer): lưu `scenario_day`, `scenario_time`
     - `scenario_type=0` (emergency): set day=0, time=null
  7. Xử lý tags: lưu `add_tag_ids`, `remove_tag_ids`
  8. Xử lý trigger time: lưu `day_of_week` (join bằng `;`), `start_time`, `end_time`
  9. Insert vào bảng `auto_reply` → lấy ID
  10. Cập nhật position = max position + 1 trong cùng category
  11. Xử lý keywords (nếu trigger=keyword):
      - **Kiểm tra trùng**: JOIN `auto_reply` + `keyword` → đếm keyword trùng trong bot
      - Nếu trùng → rollback, flash error
      - Nếu OK → `Keyword::updateOrCreate()` cho mỗi keyword
  12. `Filter::insertAutoReplyFilter()` — lưu filter legacy
  13. Redirect back với flash `success`
- **Side effects**: Tạo record `auto_reply`, tạo records `keyword`, tạo record `filters`
- **Gọi đến**: `AutoReply`, `Keyword`, `Filter`, `BackupHistory`, `Bots`
- **Tin cậy**: **Cao** — `ReplyController.php:116-225`

---

#### Action: save()
- **Route**: POST `/basic/reply/save` (EP-05)
- **Chức năng**: Cập nhật quy tắc đã tồn tại (flow legacy)
- **Luồng xử lý**:
  1. Tương tự `store()` nhưng:
     - Tìm `AutoReply::findOrFail($item_id)` thay vì insert
     - Cập nhật từng field
     - Xóa toàn bộ keyword cũ → tạo lại (`Keyword::where('auto_reply_id', $id)->delete()` + `Keyword::firstOrCreate()`)
     - Cập nhật hoặc tạo filter (kiểm tra `$reply_update->filter` tồn tại)
  2. Không kiểm tra keyword trùng khi update (khác với store)
- **Side effects**: Cập nhật record `auto_reply`, xóa/tạo records `keyword`, cập nhật/tạo record `filters`
- **Gọi đến**: `AutoReply`, `Keyword`, `Filter`
- **Tin cậy**: **Cao** — `ReplyController.php:285-429`

---

#### Action: ajaxGetListCategory()
- **Route**: POST `/ajax/get-list-group` (EP-06)
- **Chức năng**: Endpoint AJAX đa năng — xử lý 10+ actions cho quản lý danh sách
- **Luồng xử lý**:
  1. Lấy `bot_id`, `action` từ request
  2. Switch theo `action`:
     - **addAndEditGroup**: Kiểm tra backup → Tìm folder theo `id` → nếu tồn tại: rename, nếu không: insert mới vào `category` (kind=reply) → set position = max + 1
     - **deleteGroup**: Kiểm tra backup → Soft delete folder (`is_deleted=1`) → Soft delete tất cả `auto_reply` trong folder → Hard delete tất cả `keyword` liên quan
     - **renameGroup**: Kiểm tra backup → Update `name` của folder
     - **turnOnItem**: Update `auto_reply.is_stopped = 0`
     - **turnOffItem**: Update `auto_reply.is_stopped = 1`
     - **searchByKeyWord**: JOIN `auto_reply` + `keyword` → tìm theo keyword LIKE → trả kết quả riêng
     - **deleteItem**: Kiểm tra backup → Soft delete 1 auto_reply + hard delete keywords
     - **deleteItems**: Kiểm tra backup → Bulk soft delete + hard delete keywords
     - **sortItem**: Cập nhật `position` cho mỗi auto_reply theo thứ tự mới
     - **moveItem**: Cập nhật `category_id` + `position` cho các auto_reply được chọn
     - **sortFolder**: Cập nhật `position` cho mỗi folder theo thứ tự mới
  3. Sau switch: Lấy danh sách folders qua `Category::getListReplyCategories()`
  4. Lấy items theo folder hoặc items_default (category_id=0)
  5. Sort items theo position (DESC)
  6. Trả JSON response
- **Business rules quan trọng**:
  - Mọi thao tác modify đều kiểm tra `BackupHistory` trước
  - Xóa folder → cascade xóa tất cả quy tắc + keywords bên trong
  - Items trong folder 未分類 (category_id=0) luôn được trả riêng trong `items_default`
- **Gọi đến**: `Category`, `AutoReply`, `Keyword`, `Bots`, `BackupHistory`
- **Tin cậy**: **Cao** — `ReplyController.php:435-690`

---

#### Action: ajaxGetTemplateCategory()
- **Route**: POST `/ajax/get-list-template` (EP-10)
- **Chức năng**: Lấy danh sách template messages theo folder
- **Luồng xử lý**:
  1. Lấy `bot_id`
  2. `Category::getListTemplateCategories()` → danh sách folders template
  3. Với mỗi folder → `Category::getTemplateOfCategory()` → danh sách templates
  4. `Category::getTemplateDetailsOfCategoryDefault()` → templates chưa phân loại
  5. Sort theo position
- **Gọi đến**: `Category`, `Template`
- **Tin cậy**: **Cao** — `ReplyController.php:696-719`

---

#### Action: ajaxGetTagsCategory()
- **Route**: POST `/ajax/get-list-tags` (EP-11)
- **Chức năng**: Lấy danh sách tags theo folder
- **Luồng xử lý**:
  1. `Category::getListTagsCategories()` → danh sách folders tag
  2. Với mỗi folder → `Category::getTagsOfCategory()` → danh sách tags
  3. `Category::getCategoryTagDefault()` → tags chưa phân loại
  4. Đếm tags mặc định (`Tags::where('category_id', 0)`)
- **Gọi đến**: `Category`, `Tags`
- **Tin cậy**: **Cao** — `ReplyController.php:725-753`

---

#### Action: ajaxGetKeywordReply()
- **Route**: POST `/ajax/get-keyword-reply` (EP-09)
- **Chức năng**: Lấy toàn bộ auto-reply kèm keyword
- **Luồng xử lý**:
  1. Query `AutoReply` chưa bị xóa, sắp xếp theo `category_id`
  2. Với mỗi auto_reply → load keywords
  3. Nếu `reply_kind=1` (text) → base64_decode `reply_content`
  4. Trả mảng reply kèm keyword
- **Gọi đến**: `AutoReply`, `Keyword`
- **Tin cậy**: **Cao** — `ReplyController.php:806-829`

---

#### Action: initDataDetailAutoReply()
- **Route**: POST `/ajax/init-data-detail-auto-reply` (EP-07)
- **Chức năng**: Khởi tạo dữ liệu form V2 — tạo mới, chỉnh sửa, hoặc sao chép
- **Luồng xử lý**:
  1. Khởi tạo object `auto_reply` mặc định (tất cả giá trị = 0/null/empty)
  2. Nếu có `reply_id` (chỉnh sửa):
     - Load `AutoReply` → populate `auto_reply` object
     - Load danh sách `Keyword`
     - Nếu có `action_id` → load `Actions` + `ActionDetail` → gọi `Actions::initDataAction()` cho mỗi detail để enrich data (template name, tag names, scenario name...)
  3. Nếu có `copyId` (sao chép):
     - Load `AutoReply` gốc
     - Clone action qua `MessageTemplateController::cloneMutilpleAction()` → tạo bản sao `t_actions` + `t_actions_detail` + `filters_v2`
     - **Không** clone keywords (list_keyword trả về mặc định rỗng)
  4. Nếu không có keyword nào → trả 1 keyword rỗng mặc định
  5. Trả JSON: `data_reply`, `list_keyword`, `detail_action_reply`
- **Gọi đến**: `AutoReply`, `Keyword`, `Actions`, `ActionDetail`, `Tag`, `MessageTemplateController`
- **Tin cậy**: **Cao** — `ReplyController.php:831-927`

---

#### Action: saveDataDetailAutoReply()
- **Route**: POST `/ajax/save-data-detail-auto-reply` (EP-08)
- **Chức năng**: Lưu/cập nhật quy tắc (flow V2 — AJAX)
- **Luồng xử lý**:
  1. **Kiểm tra bot**: So sánh `botIdCurrent` (từ request) với `getBotId()` (từ session) → nếu khác, trả lỗi (đã đổi bot)
  2. **Kiểm tra backup**: Tìm `BackupHistory` đang chạy → nếu có, trả lỗi 500
  3. **Validate**:
     - Nếu `keyword_reaction_type=1` (setting keyword) → kiểm tra `list_keyword` không rỗng
     - Nếu `time_reaction_type=1` (setting time) → validate format `HH:mm`, kiểm tra end > start
  4. **Kiểm tra keyword trùng** (chỉ khi keyword mode):
     - Query toàn bộ keyword hiện có trong bot
     - So sánh từng keyword mới với keyword cũ
     - Nếu keyword mới (id rỗng) trùng → lỗi
     - Nếu keyword update (id có) nhưng đổi sang keyword đã tồn tại → lỗi
     - Trả về `arraySameWord` chứa index các keyword trùng
  5. **Lưu/Cập nhật AutoReply**:
     - Nếu có `reply_id` → `AutoReply::update()` (luôn set `is_stopped=0`)
     - Nếu không có → `AutoReply::create()` (set `position = max + 1`)
  6. **Lưu thời gian** (nếu time mode):
     - Update `start_time`, `end_time`, `day_of_week` (join bằng `;`)
  7. **Lưu keywords** (nếu keyword mode):
     - Với mỗi keyword: nếu có `id` → update, nếu không → create
     - Xóa keywords cũ không còn trong danh sách mới (`whereNotIn`)
     - Nếu không phải keyword mode → xóa tất cả keywords cũ
  8. **Lưu FilterV2**:
     - Parse `item_search` (AND) và `item_search_or` (OR) từ JSON
     - `FilterV2::saveFilter()` với `parent_type='auto_reply'`, `parent_id=auto_reply.id`
  9. Trả JSON success
- **Business rules quan trọng**:
  - Keyword trùng kiểm tra trên toàn bot (cross auto-reply)
  - Khi update, `is_stopped` luôn được reset về `0` (bật)
  - FilterV2 replace toàn bộ filter cũ (xóa cũ + tạo mới)
- **Gọi đến**: `AutoReply`, `Keyword`, `FilterV2`, `Bots`, `BackupHistory`
- **Tin cậy**: **Cao** — `ReplyController.php:929-1083`

---

#### Private: validateAutoReplay()
- **File**: `app/Http/Controllers/Basic/ReplyController.php:759`
- **Chức năng**: Validate dữ liệu form legacy (EP-04, EP-05)
- **Logic**:
  1. Nếu `trigger_kind=0` (keyword):
     - `rword` không được rỗng → lỗi: `'キーワードを1つ以上設定して下さい。'`
  2. Nếu `trigger_kind=1` (time):
     - `week` không được rỗng → lỗi: `'曜日は最低1つを選択して下さい。'`
     - `hour_from` bắt buộc → lỗi: `'時間帯(開始)は必須です。'`
     - `hour_to` bắt buộc → lỗi: `'時間帯(終了)は必須です。'`
     - Validate format HH:mm (regex)
     - Validate end > start → lỗi: `'時間帯を正しく指定して下さい。'`
  3. Nếu `use_reply=1` (text):
     - `reply` bắt buộc → lỗi: `'返信文は必須です。'`
     - `reply` tối đa 5000 chars → lỗi: `'返信文は5000文字以下にしてください。'`
  4. Nếu `use_reply=2` (template):
     - `egg_id` bắt buộc → lỗi: `'返信文は必須です。'`
- **Tin cậy**: **Cao** — `ReplyController.php:759-803`

---

### Basic\FilterController (liên quan SC-003)
- **File**: `app/Http/Controllers/Basic/FilterController.php` (1102 dòng)
- **Namespace**: `App\Http\Controllers\Basic`

#### Action: initDataFilter()
- **Route**: POST `/ajax/init-data-filter` (EP-13)
- **Chức năng**: Khởi tạo dữ liệu cho modal lọc đối tượng
- **Luồng xử lý**:
  1. Nhận `parent_id`, `parent_type`, `copy_id`
  2. Nếu có `parent_id`:
     - Query `FilterV2` theo `parent_type` + `parent_id` + `bot_id`
     - Tách thành 2 nhóm: `operator='and'` và `operator='or'`
  3. Với mỗi filter item, enrich data theo `type`:
     - `tag`: load tag names, items_default
     - `day_add_friend`: xử lý day_filter_type (khoảng ngày hoặc khoảng thời gian)
     - `conversion`: load conversion names, conversion_list
     - `scenario`: load scenario name, scenario_list
     - `qr_code`: load QR code details (landing pages)
     - `richmenu`: lưu richmenu ID
  4. Nếu `copy_id` → reset ID các filter items (để tạo bản mới)
  5. Trả JSON: `itemFilterAnd`, `itemFilterOr`, `numberFilter`
- **Gọi đến**: `FilterV2`, `Category`, `Tags`, `Conversion`, `Scenario`, `Landing`, `Template`, `Bots`
- **Tin cậy**: **Cao** — `FilterController.php:290-500+`

#### Action: ajaxGetListUserFilter()
- **Route**: POST `/ajax/filter/get-list-user` (EP-15)
- **Chức năng**: Lấy/đếm bạn bè theo điều kiện lọc
- **Luồng xử lý**:
  1. Build query trên `LineUser` JOIN `bot_line_user` (is_blocked=0)
  2. Áp dụng các filter:
     - `name_filter`: LIKE trên name/real_name/view_name
     - `tag_filter`: JOIN `tag_line_user` (AND/OR logic)
     - `from_date_filter`/`to_date_filter`: lọc theo ngày thêm bạn bè
     - `scenario_filter`: lọc theo step subscription
     - `conversion_filter`: lọc theo conversion status
     - `mark_filter`: lọc theo bookmark
  3. Trả danh sách + count
- **Gọi đến**: `LineUser`, `BotLineUser`, `Tags`
- **Tin cậy**: **Cao** — `FilterController.php:41-290`

---

### Basic\BasicController (liên quan cookie)
- **File**: `app/Http/Controllers/Basic/BasicController.php` (2715 dòng)
- **Namespace**: `App\Http\Controllers\Basic`

#### Action: folderSetCookie()
- **Route**: GET `/basic/reply/set-cookie` (EP-12)
- **Chức năng**: Lưu folder đang chọn vào cookie
- **Luồng xử lý**:
  1. Nhận `folder_id`, `type` từ query
  2. Switch theo `type`:
     - `reply`: đọc cookie `folder_reply` → so sánh → nếu khác → set cookie mới
  3. Cookie format: JSON `{bot_id: folder_id}`
  4. Cookie hạn: 14400 phút (10 ngày), path `/basic/reply`
- **Gọi đến**: `Cookie`
- **Tin cậy**: **Cao** — `BasicController.php:1900-1940`

---

### Admin\BotController (liên quan EP-14)
- **File**: `app/Http/Controllers/Admin/BotController.php` (11763 dòng)

#### Action: getBotData()
- **Route**: POST `/ajax/get-bot-data` (EP-14)
- **Chức năng**: Trả thông tin cơ bản bot
- **Luồng xử lý**:
  1. `Bots::where('id', $bot_id)->select("id", "plan_type")->first()`
  2. Trả JSON
- **Gọi đến**: `Bots`
- **Tin cậy**: **Cao** — `BotController.php:11337-11342`

---

## Models

### AutoReply
- **File**: `app/AutoReply.php`
- **Bảng DB**: `auto_reply`
- **Guard**: `$guarded = []` (mass assignable)
- **Timestamps**: Có (`created_at`, `updated_at`)

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `keywords()` | hasMany | `Keyword` | `auto_reply_id` | Danh sách keywords gắn với quy tắc |
| `filter()` | hasOne | `Filter` | `auto_reply_id` | Bộ lọc legacy (bảng `filters`) |

#### Scope Methods (static)
| Method | Mô tả | Gọi bởi |
|--------|-------|---------|
| `searchByKeyWord($group_id, $keyword)` | Tìm kiếm quy tắc theo keyword trong folder. JOIN `keyword` table, filter theo `is_deleted=0`, `category_id`, `bot_id`. Kết quả bao gồm: id, keyword display, group_name, day_of_week, time range, trigger info, reply content, tags, template name, scenario name, position, is_stopped, created_at, filter_preview_content | EP-06 (searchByKeyWord) |
| `getAutoMessagesCategoryDefault($keyword)` | Lấy quy tắc trong folder 未分類 (category_id=0). Hỗ trợ tìm theo keyword (LIKE). Format output tương tự `searchByKeyWord()` | EP-06 |
| `changeAutoReplysToNewBot($currentBot, $newBot)` | Chuyển quy tắc sang bot mới | Chức năng đổi bot |

#### Ghi chú quan trọng
- `reply_content` được base64_encode khi lưu (loại text), base64_decode khi hiển thị
- `day_of_week` lưu dạng string phân cách bằng `;` (vd: `"1;2;3;4;5"`)
- `add_tag_ids` và `remove_tag_ids` lưu dạng string phân cách bằng `,`
- **Tin cậy**: **Cao** — `app/AutoReply.php`

---

### Keyword
- **File**: `app/Keyword.php`
- **Bảng DB**: `keyword`
- **Guard**: `$guarded = []`
- **Timestamps**: Có

#### Relationships
Không khai báo explicit relationships.

#### Các cột chính (suy luận từ code)
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | int | Primary key |
| `auto_reply_id` | int | FK → `auto_reply.id` |
| `keyword` | string | Nội dung keyword |
| `logical` | int | Loại so khớp: `0` = 完全一致 (exact), `1` = 部分一致 (partial) |

- **Tin cậy**: **Cao** — `app/Keyword.php`, `ReplyController.php`

---

### Filter (Legacy)
- **File**: `app/Filter.php`
- **Bảng DB**: `filters`
- **Guard**: `$guarded = []`
- **Timestamps**: Có

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `autoReply()` | belongsTo | `AutoReply` | `auto_reply_id` | Quy tắc auto-reply liên quan |
| `smsSchedule()` | belongsTo | `SmsSchedules` | `sms_schedule_id` | SMS schedule liên quan |
| `broadcast()` | belongsTo | `BroadCast` | `broadcast_id` | Broadcast liên quan |

#### Static Methods
| Method | Mô tả |
|--------|-------|
| `insertAutoReplyFilter($request, $autoReplyId)` | Tạo filter cho auto-reply mới (flow legacy) |
| `convertFilterToEditArray($filter)` | Chuyển filter thành array cho form edit. Convert date format, load tag names, load conversion names |

#### Các cột chính (từ code)
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `auto_reply_id` | int | FK → auto_reply.id |
| `broadcast_id` | int | FK → broadcasts.id |
| `sms_schedule_id` | int | FK → sms_schedules.id |
| `name_filter` | string | Tên bạn bè cần lọc |
| `name_filter_type` | string | Loại lọc tên |
| `tag_filter` | string | Danh sách tag IDs (CSV) |
| `tag_filter_option` | string | Logic tag (AND/OR) |
| `from_date_filter` | date | Ngày bắt đầu |
| `to_date_filter` | date | Ngày kết thúc |
| `scenario_filter` | string | Scenario filter |
| `scenario_filter_option` | string | Logic scenario |
| `scenario_start_day_filter` | string | Ngày bắt đầu scenario |
| `conversion_filter` | string | Conversion IDs (CSV) |
| `conversion_filter_option` | string | Logic conversion |
| `mark_filter` | int | Bookmark filter |
| `filter_preview_content` | string | Nội dung hiển thị preview filter |

> **Ghi chú**: Model `Filter` là hệ thống filter **cũ** (legacy). Flow V2 sử dụng `FilterV2`.

- **Tin cậy**: **Cao** — `app/Filter.php`

---

### FilterV2
- **File**: `app/FilterV2.php`
- **Bảng DB**: `filters_v2`
- **Guard**: `$guarded = []`
- **Timestamps**: Có

#### Static Methods
| Method | Mô tả |
|--------|-------|
| `saveFilter($filterAnd, $filterOr, $parentType, $parentId, ...)` | Lưu điều kiện lọc. Xử lý từng item: validate theo type (tag, day_add_friend, qr_code, conversion, friend_info...), serialize data thành JSON, lưu vào DB. Xóa items cũ không còn trong danh sách mới |
| `cloneFilters($sourceId, $targetId, $parentType)` | Clone filter từ nguồn sang đích (dùng khi copy) |

#### Các cột chính (từ code)
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | int | Primary key |
| `bot_id` | int | FK → bots.id |
| `parent_type` | string | Loại đối tượng cha: `'auto_reply'`, `'broadcast'`, `'modal_action'`... |
| `parent_id` | int | ID đối tượng cha |
| `operator` | string | `'and'` hoặc `'or'` |
| `type` | string | Loại filter: `'tag'`, `'day_add_friend'`, `'scenario'`, `'qr_code'`, `'conversion'`, `'friend_info'`, `'name'`, `'mark'`, `'new_old_friend'`, `'richmenu'`, `'status_chat'`, `'affiliater'` |
| `data` | JSON text | Dữ liệu filter chi tiết (khác nhau theo type) |
| `text_preview` | string | Nội dung hiển thị preview |
| `rich_menu_redirect_id` | int | ID rich menu redirect (nullable) |
| `rich_menu_item_id` | int | ID rich menu item (nullable) |

#### 11 loại filter types
| Type | Mô tả | Data fields chính |
|------|-------|-------------------|
| `tag` | Lọc theo tag | `tags_search` (array IDs), `tag_option` (and/or) |
| `name` | Lọc theo tên bạn bè | `name_filter`, `name_filter_type` |
| `day_add_friend` | Lọc theo ngày thêm bạn bè | `day_filter_type` (0=khoảng thời gian, 1=số ngày), `modal_from_filter`, `modal_to_filter`, `duration_day_start`, `duration_day_end` |
| `scenario` | Lọc theo step subscription | `scenario_search` (ID), `scenario_option` |
| `qr_code` / `qr_code_action` | Lọc theo QR code | `qrs_search` (array IDs), `qr_option` |
| `conversion` | Lọc theo conversion | `conversion_search` (CSV IDs), `conversion_option` |
| `friend_info` | Lọc theo thông tin bạn bè | `friend_info_id`, `friend_info_type`, `value`, `limit_date`... |
| `mark` | Lọc theo bookmark | `mark_option` |
| `new_old_friend` | Lọc bạn bè mới/cũ | `new_old_option` |
| `status_chat` | Lọc theo trạng thái đối ứng | `status_chat_id` |
| `affiliater` | Lọc theo nguồn giới thiệu | `affiliater_id` |

- **Tin cậy**: **Cao** — `app/FilterV2.php:18-330`

---

### Category
- **File**: `app/Category.php`
- **Bảng DB**: `category`
- **Guard**: Không rõ (không đọc file)

#### Sử dụng trong auto-reply
| Method (static) | Mô tả | Tin cậy |
|-----------------|-------|---------|
| `getListReplyCategories($bot_id)` | Lấy danh sách folders loại reply (kind=1, is_deleted=0) | Cao — suy luận từ `ReplyController.php:661` |
| `getMessageOfCategory($category)` | Lấy danh sách auto-reply items trong 1 folder | Cao — suy luận từ `ReplyController.php:668` |
| `getListTemplateCategories($bot_id)` | Lấy folders template (kind=2) | Cao |
| `getTemplateOfCategory($category)` | Lấy templates trong folder | Cao |
| `getListTagsCategories($bot_id)` | Lấy folders tag (kind=0) | Cao |
| `getTagsOfCategory($category)` | Lấy tags trong folder | Cao |
| `getCategoryTagDefault()` | Lấy tags chưa phân loại (category_id=0) | Cao |
| `displayKeyword($item)` | Hiển thị keyword cho item | Cao |
| `displayTimer($day_of_week)` | Hiển thị ngày trong tuần | Cao |
| `getTagsName($tag_ids)` | Lấy tên tags từ danh sách IDs | Cao |
| `getTemplateName($template_id)` | Lấy tên template từ ID | Cao |
| `getScenario($scenario_id)` | Lấy tên scenario từ ID | Cao |

#### Category Kinds (config)
| Kind | Giá trị | Mô tả |
|------|---------|-------|
| tag | 0 | Folder tags |
| **reply** | **1** | **Folder auto-reply** |
| template | 2 | Folder templates |
| url | 3 | Folder URLs |
| landing | 10 | Folder landing pages |
| scenario | 11 | Folder scenarios |
| information_friend | 12 | Folder friend information |
| event_booking | 13 | Folder event booking |
| rich_menus | 17 | Folder rich menus |
| action_schedule | 20 | Folder action schedule |

- **Tin cậy**: **Cao** — `config/sns-line.php:292-309`

---

### Actions
- **File**: `app/Actions.php`
- **Bảng DB**: `t_actions`
- **Guard**: `$guarded = []`
- **Timestamps**: Có

#### Relationships
| Relationship | Kiểu | Model liên quan | FK | Mô tả |
|-------------|------|----------------|-----|-------|
| `details()` | hasMany | `ActionDetail` | `action_id` | Chi tiết các hành động |

#### Static Methods
| Method | Mô tả |
|--------|-------|
| `initDataAction($actionDetail, $jsonStr)` | Enrich data cho action detail theo type: template → thêm template_name, tag → thêm list_tags, scenario → thêm scenario_name, remind → thêm event info, friend_info → xử lý special cases |

- **Tin cậy**: **Cao** — `app/Actions.php`

---

### ActionDetail
- **File**: `app/ActionDetail.php`
- **Bảng DB**: `t_actions_detail`
- **Guard**: `$guarded = []`
- **Timestamps**: Có

#### Relationships
| Relationship | Kiểu | Model liên quan | FK | Mô tả |
|-------------|------|----------------|-----|-------|
| `tagLine()` | hasOne | `Actions` | `action_id` | Action cha |

#### Các cột chính (suy luận từ code)
| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | int | PK |
| `action_id` | int | FK → `t_actions.id` |
| `type` | string | Loại action: `'template'`, `'tag'`, `'scenario'`, `'text'`, `'remind'`, `'richmenu'`, `'bookmark'`, `'friend_info'`, `'status_chat'`, `'block'` |
| `data` | JSON text | Dữ liệu chi tiết của action (khác nhau theo type) |
| `bot_id` | int | FK → bots.id |
| `has_filters` | int | `1` nếu action detail có filter riêng |

#### 10 loại action types (tương ứng SCR-RPL-04)
| Type | Mô tả | Data structure |
|------|-------|---------------|
| `scenario` / `step` | Thêm vào/chuyển step delivery | `{id: scenario_id, type: 'emergency'/'timer', day: N, time: 'HH:mm'}` |
| `template` | Gửi template message | `{id: template_id}` |
| `text` | Gửi tin nhắn text | `{content: "text message"}` |
| `remind` | Thiết lập reminder | `{event_id: N}` |
| `tag` | Gán/gỡ tag | `{ids: [tag_ids], action: 'add'/'remove'}` |
| `richmenu` | Đổi Rich Menu | `{id: richmenu_id}` |
| `bookmark` | Gán bookmark | `{mark: 0/1}` |
| `friend_info` | Cập nhật thông tin bạn bè | `{friend_info_id: N, type: N, action: N, value: "..."}` |
| `status_chat` | Đổi trạng thái đối ứng | `{status_id: N}` |
| `block` | Block bạn bè | `{block: true}` |

- **Tin cậy**: **Cao** (type list), **Trung bình** (data structure — suy luận từ `Actions::initDataAction()`)

---

## Services / Repositories

### ScenarioRepositoryInterface
- **Inject vào**: `ReplyController` (constructor)
- **Method sử dụng**: `findByBot($bot_id)` — lấy danh sách scenarios cho bot
- **Tin cậy**: **Cao** — `ReplyController.php:49-52, 100`

### MessageTemplateController::cloneMutilpleAction()
- **File**: `app/Http/Controllers/Basic/MessageTemplateController.php:3910`
- **Chức năng**: Clone action (bảng `t_actions`) và tất cả action details (bảng `t_actions_detail`) sang bản mới. Cũng clone `FilterV2` nếu action detail có `has_filters=1`.
- **Luồng**:
  1. Tìm `Actions` theo ID → replicate → create bản mới
  2. Lấy tất cả `ActionDetail` của action → replicate mỗi detail → update `action_id` + `bot_id` → insert
  3. Nếu detail có `has_filters=1` → `FilterV2::cloneFilters()`
- **Dùng bởi**: `initDataDetailAutoReply()` khi copy auto-reply
- **Tin cậy**: **Cao** — `MessageTemplateController.php:3910-3938`

---

## Form Requests / Validation

Tính năng **không sử dụng** Laravel Form Request classes. Validation được thực hiện trực tiếp trong controller:

### Validation Flow Legacy (validateAutoReplay)
| Field | Điều kiện | Rule | Message lỗi |
|-------|----------|------|-------------|
| `rword[]` | `trigger_kind=0` (keyword) | Bắt buộc, tối thiểu 1 | `'キーワードを1つ以上設定して下さい。'` |
| `week[]` | `trigger_kind=1` (time) | Bắt buộc, tối thiểu 1 | `'曜日は最低1つを選択して下さい。'` |
| `hour_from` | `trigger_kind=1` | Bắt buộc | `'時間帯(開始)は必須です。'` |
| `hour_to` | `trigger_kind=1` | Bắt buộc | `'時間帯(終了)は必須です。'` |
| `hour_from`, `hour_to` | `trigger_kind=1` | Format HH:mm, end > start | `'時間帯を正しく指定して下さい。'` |
| `reply` | `use_reply=1` (text) | Bắt buộc | `'返信文は必須です。'` |
| `reply` | `use_reply=1` | Max 5000 ký tự UTF-8 | `'返信文は5000文字以下にしてください。'` |
| `egg_id` | `use_reply=2` (template) | Bắt buộc | `'返信文は必須です。'` |

### Validation Flow V2 (saveDataDetailAutoReply)
| Field | Điều kiện | Rule | Message lỗi |
|-------|----------|------|-------------|
| `list_keyword` | `keyword_reaction_type=1` | Bắt buộc, tối thiểu 1 | `'キーワードを1つ以上設定して下さい。'` |
| `start_time`, `end_time` | `time_reaction_type=1` | Format HH:mm, end > start | `'時間帯を正しく指定して下さい。'` |
| keyword uniqueness | `keyword_reaction_type=1` | Không trùng trong bot | `'キーワードは既に登録されています。'` |
| `botIdCurrent` | Luôn | = getBotId() | `'別のアカウントに切り替えたので、要求を処理できません。'` |

- **Tin cậy**: **Cao**

---

## Events / Listeners / Queued Jobs

Không phát hiện Events, Listeners, hoặc Queued Jobs trực tiếp trong code ReplyController. Tính năng auto-reply **không dispatch job** khi tạo/sửa quy tắc.

> **Ghi chú**: Việc **thực thi** auto-reply (khi LINE user gửi tin nhắn) được xử lý bởi hệ thống callback/webhook riêng — không nằm trong các controller đã phân tích. Có `BotAutoReplyController` (`app/Http/Controllers/BotAutoReplyController.php`, 50 dòng) với methods `settingAutoReplyMessage()` và `handlerAutoReplyMessage()` — đây có thể là nơi xử lý logic thực thi auto-reply khi nhận webhook từ LINE. Cần phân tích thêm trong bước job-analyzer nếu liên quan đến background job.

- **Tin cậy**: **Cao** (không có job trong CRUD), **Thấp** (logic thực thi auto-reply — chưa phân tích)

---

## Authorization

| Quyền | Kiểm tra ở đâu | Logic | Ảnh hưởng |
|-------|----------------|-------|----------|
| Session auth | `web` middleware group | User phải đăng nhập (session-based) | Tất cả endpoints — redirect login nếu chưa đăng nhập |
| Bot ownership | `getBotId()` helper | Lấy bot_id từ session, mọi query đều filter theo bot_id | Chỉ thao tác được với auto-reply thuộc bot đang active |
| Bot switch check | `saveDataDetailAutoReply()` | So sánh `botIdCurrent` (request) với `getBotId()` (session) | Ngăn lưu nếu đã đổi bot giữa chừng |
| Backup check | Các action modify | Kiểm tra `BackupHistory` status 0/1 | Chặn mọi thao tác modify khi bot đang backup |

> **Ghi chú**: Không phát hiện kiểm tra quyền Staff (Role/Permission). Tính năng auto-reply có thể bị giới hạn cho Staff qua cơ chế khác (middleware route group hoặc kiểm tra trong view). **Tin cậy**: Trung bình.

---

## Business Rules tổng hợp

| # | Rule | Mô tả | Nơi implement | Tin cậy |
|---|------|-------|--------------|---------|
| 1 | Keyword duy nhất trong bot | Mỗi keyword chỉ được đăng ký 1 lần trong toàn bộ bot (cross auto-reply). Kiểm tra khi tạo mới và cập nhật | `ReplyController.php:187-199` (legacy), `ReplyController.php:979-1006` (v2) | **Cao** |
| 2 | Backup lock | Không cho phép tạo/sửa/xóa khi bot đang trong quá trình backup | `ReplyController.php:143-149, 456-463, 491-498, 515-522, 569-576, 587-594, 621-629, 940-946` | **Cao** |
| 3 | Reply content encoding | Nội dung text reply được base64_encode khi lưu, base64_decode khi đọc | `ReplyController.php:153-154` (store), `AutoReply.php:56` (read) | **Cao** |
| 4 | Soft delete | Xóa auto-reply và folder sử dụng soft delete (`is_deleted=1`), nhưng xóa keywords sử dụng hard delete | `ReplyController.php:507-508, 580-582, 598-600` | **Cao** |
| 5 | Position ordering | Mỗi auto-reply có position trong folder. Tạo mới → position = max + 1. Sắp xếp → cập nhật position | `ReplyController.php:179-182, 978, 1033, 603-618` | **Cao** |
| 6 | Day of week format | Ngày trong tuần lưu dạng string phân cách bằng `;` (vd: `"1;2;3;4;5"`) | `ReplyController.php:174, 326, 1042` | **Cao** |
| 7 | Cascade delete folder | Xóa folder → soft delete tất cả auto-reply trong folder + hard delete keywords | `ReplyController.php:505-508` | **Cao** |
| 8 | V2 auto-enable | Khi lưu qua flow V2 (saveDataDetailAutoReply), `is_stopped` luôn reset về `0` (bật) | `ReplyController.php:1020, 1034` | **Cao** |
| 9 | Bot switch protection | Flow V2 kiểm tra bot hiện tại = bot khi mở trang. Ngăn lưu dữ liệu sai bot | `ReplyController.php:935-938` | **Cao** |
| 10 | Time validation | Giờ bắt đầu phải nhỏ hơn giờ kết thúc. Format HH:mm. Regex validate | `ReplyController.php:780-792, 959-972` | **Cao** |
| 11 | Copy action deep clone | Khi sao chép auto-reply, action được deep clone: tạo bản sao `t_actions` → `t_actions_detail` → `filters_v2` | `MessageTemplateController.php:3910-3938`, `ReplyController.php:877` | **Cao** |
| 12 | Checkbox「〇〇のメッセージには反応させない」 | Trường `is_no_reply_button` — khi `true`, quy tắc không phản ứng với tin nhắn từ nút reply (quick reply buttons). `〇〇` trong UI chỉ nút reply chứ không phải tên bot | `ReplyController.php:849, 892, 1021, 1035` | **Cao** |
| 13 | Filter dual system | Tính năng sử dụng 2 hệ thống filter song song: `Filter` (legacy, bảng `filters`) cho flow cũ và `FilterV2` (bảng `filters_v2`) cho flow V2 | `ReplyController.php:213, 1073` | **Cao** |
| 14 | Default folder (未分類) | category_id=0 là folder mặc định「未分類」. Không phải record trong bảng `category` — là convention | `AutoReply.php:93, ReplyController.php:672-675` | **Cao** |

---

## Config Constants (sns-line.php)

| Config key | Giá trị | Mô tả |
|-----------|---------|-------|
| `sns-line.category_kind.reply` | `1` | Kind cho folder auto-reply trong bảng category |
| `sns-line.trigger_kind.keyword` | `0` | Trigger bằng keyword |
| `sns-line.trigger_kind.time` | `1` | Trigger bằng thời gian |
| `sns-line.logical.and` | `0` | Logic AND cho keyword |
| `sns-line.logical.or` | `1` | Logic OR cho keyword |
| `sns-line.type_reaction.all` | `0` | Phản ứng tất cả tin nhắn |
| `sns-line.type_reaction.setting` | `1` | Phản ứng theo cài đặt (keyword/time) |
| `sns-line.use_reply.none` | `0` | Không có reply |
| `sns-line.use_reply.text` | `1` | Reply bằng text |
| `sns-line.use_reply.template` | `2` | Reply bằng template |
| `sns-line.scenario_type.emergency` | `0` | Chuyển step ngay lập tức |
| `sns-line.scenario_type.timer` | `1` | Chuyển step theo timer |
| `sns-line.response_number.only` | `0` | Chỉ phản ứng 1 lần |
| `sns-line.response_number.many` | `1` | Phản ứng nhiều lần |
| `sns-line.item_is_stopped.false` | `0` | Quy tắc đang bật |
| `sns-line.item_is_stopped.true` | `1` | Quy tắc đã tắt |
| `sns-line.is_deleted.false` | `0` | Chưa xóa |
| `sns-line.is_deleted.true` | `1` | Đã xóa (soft delete) |

- **Tin cậy**: **Cao** — `config/sns-line.php:268-326, 972-975`

---

## Điểm cần lưu ý cho bước tiếp theo

### Cho DB Mapper (bước 5)
- Bảng chính: `auto_reply`, `keyword`, `category`, `filters`, `filters_v2`, `t_actions`, `t_actions_detail`
- `auto_reply.reply_content` lưu base64 encoded text hoặc template ID
- `auto_reply.day_of_week` lưu string phân cách `;`
- `auto_reply.add_tag_ids` / `remove_tag_ids` lưu string phân cách `,`
- `category.kind=1` cho folders auto-reply

### Cho Job Analyzer (bước 4)
- **Không phát hiện background job** trong flow CRUD auto-reply
- `BotAutoReplyController` (`app/Http/Controllers/BotAutoReplyController.php`, 50 dòng) có thể chứa logic thực thi auto-reply khi nhận webhook LINE — cần kiểm tra
- Có thể có Spring Boot job xử lý matching keyword + trigger action khi nhận tin nhắn LINE
