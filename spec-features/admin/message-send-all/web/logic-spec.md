# Logic Spec — FA-008:「メッセージ配信」(Broadcast)

**Feature ID**: FA-008
**Portal**: Admin
**Ngày phân tích**: 2026-03-26
**Nguồn**: Laravel source code (`reverse-spec/src/web/sns-line/`)

---

## 1. Controllers + Actions

### 1.1 BroadcastController

**File**: `app/Http/Controllers/Basic/BroadcastController.php` (2730 lines)
**Namespace**: `App\Http\Controllers\Basic`
**Dependency**: `BroadcastService` (injected via constructor)

#### index() — Hiển thị danh sách broadcast
- **File:line**: `BroadcastController.php:78-106`
- **Logic**: Query `RichMenus` (status_rich=1), `Scenario`, `Conversion`, `StatusChat` cho bot hiện tại → trả view
- **Side effects**: Không

#### storeBroadCast() — Lưu cài đặt broadcast (legacy, multi-action)
- **File:line**: `BroadcastController.php:373-557`
- **Logic**:
  - Switch theo `action`:
    - **`create`**: Tạo broadcast mới với `status = 'unregistered'`
      - Nếu `setting_time_send == 1` → dùng `b_send_day`, `b_send_time` (validate format ngày)
      - Nếu không → dùng `Carbon::now()`
      - Đếm `filter_number` qua `Conversation::advanceFilterPost()`
    - **`copy`**: Sao chép broadcast
      - Clone templates qua `copyTemplate()`
      - Clone filters (FilterV2)
      - Tính lại `filter_number`
    - **`edit`**: Cập nhật thời gian gửi
      - Nếu `status == 'not_delivery'` và có schedule → chuyển `status = 'wait_to_send'`
    - **`save_rich_menu`**: Cập nhật rich_menu_id
    - **`switch_status`**: Chuyển status `not_delivery → wait_to_send`
    - **`save_filter`**: Lưu filter (legacy Filter model)
- **Validation**:
  - Kiểm tra broadcast chưa `delivered`/`delivering`
  - `checkFormatDate()` cho ngày gửi
- **Side effects**: Tạo/cập nhật record `broadcast`, `filters_v2`

#### messageStore() — Lưu message template vào broadcast (legacy)
- **File:line**: `BroadcastController.php:263-371`
- **Logic**:
  1. Kiểm tra `botIdCurrent` khớp bot session → nếu khác → lỗi「別のアカウントに切り替えたので、要求を処理できません。」
  2. Kiểm tra broadcast chưa `delivered`/`delivering`
  3. Validate ImageMap settings (x, y, width, height phải hợp lệ)
  4. Gọi `handlerCreateTemplate()` → tạo Template record
  5. Thêm `template_id` vào `broadcast.template_ids`
  6. Cập nhật status: `unregistered → wait_to_send` (nếu có schedule) hoặc `→ not_delivery`
  7. Nếu `is_tester == 1`: gửi test message cho testers
- **Validation**: Bot ID match, ImageMap area validation
- **Side effects**: Insert `template`, update `broadcast`

#### updateMessage() — Cập nhật message template (legacy)
- **File:line**: `BroadcastController.php:640-921`
- **Logic**:
  1. **5 phút rule**: Nếu broadcast `wait_to_send` và < 5 phút trước giờ gửi → lỗi
  2. Kiểm tra `delivered`/`delivering` → không cho sửa
  3. Switch theo `tmp_type`:
    - `text/stamp`: Xử lý URL detection qua `detectUrlInMessageTextV2()`, replace `\r\n → \n`
    - `group`: Copy park template content
    - `question`: Cập nhật question relationships
    - `location`: Cập nhật location
    - `introduction`: Cập nhật introduction
    - `voice`: Upload audio file, tính duration
    - `video`: Upload video + thumbnail, upload to Dropbox
    - `image`: Upload image + thumbnail, xử lý ImageMap nếu có
    - `form`: Cập nhật carousel buttons
  4. Xử lý URL detect & URL redirect
  5. Nếu `is_tester == 1`: gửi test message
- **Side effects**: Update `template`, `image_map`, `image_map_items`, `url`, `template_url_redirect`

#### ajaxGetListBroadcastVer2() — Danh sách broadcast phân trang
- **File:line**: `BroadcastController.php:1286-1474`
- **Logic**:
  1. **Xoá** (action=delete):
     - Kiểm tra 5 phút rule (6 phút thực tế trong code: `subMinutes(6)`)
     - Xoá templates category broadcast (`category_id = config('sns-line.category_broadcast')`)
     - Xoá broadcast record
  2. **Query**:
     - `wait_to_send`: `status IN ('wait_to_send')`, filter by month
     - `delivered`: `status IN ('delivered', 'send_false')`, filter by date range
     - `draft`: `status IN ('draft', 'unregistered', 'not_delivery')`
  3. **Sort**: mặc định DESC theo send_day, send_time, id
  4. **Enrich mỗi item**:
     - `delivery_dates`: children broadcasts (parent_id)
     - `checkFilter`: kiểm tra có filter trong `filters_v2`
     - `text_filter`: `'設定済み'` nếu có filter, `'未設定（全員）'` nếu chưa
     - `profileBot`: profile người gửi (hoặc default)
     - `number_send`: `send_count` nếu delivered, rỗng nếu chưa
- **Lưu ý**: Code dùng `subMinutes(6)` nhưng UI hiện「5分前」— thực tế buffer thêm 1 phút

#### getFilterNumber() — Tính lại số người nhận
- **File:line**: `BroadcastController.php:2511-2555`
- **Logic**:
  1. Lấy filters AND + OR từ `filters_v2` (parent_type='broadcast')
  2. Gọi `Conversation::advanceFilterPost($bot_id, AND, OR, null, false, [], true)`
  3. Count distinct `bot_line_user.id`
  4. Cập nhật `broadcast.filter_number`, `broadcast.filter_date`
  5. Cũng cập nhật cho children broadcasts (cùng `parent_id`)
- **Hàm quan trọng**: `Conversation::advanceFilterPost()` — xử lý 11 loại filter, join nhiều bảng

#### ajaxSendForTestBroadcast() — Gửi test broadcast (legacy)
- **File:line**: `BroadcastController.php:2187-2325`
- **Logic**:
  1. Lấy broadcast → templates → build messages
  2. Template type `group`: giải nén content (comma-separated IDs) → lấy từng child template
  3. **LINE API limit**: Gom tối đa 5 messages/batch → gọi `createMultipleMessage()` cho mỗi batch
  4. `createMultipleMessage()` → gọi LINE Messaging API Push Message
  5. Nếu thành công → `free_send_count + 1`, `updateMessageSendCount()`
  6. Nếu thất bại → `createMessageError()` → ghi vào bảng `message_errors`
  7. Nếu có `actionId` → `sendAction()` cho mỗi tester → thực thi action (tag, step, rich menu...)
- **Side effects**: Gửi message LINE, update `bots.free_send_count`, insert `messages`/`messages_v2`, insert `message_errors`

#### sendForTestBroadcastV3() — Gửi test (V3, delegate to Service)
- **File:line**: `BroadcastController.php:2327-2331`
- **Logic**: Delegate toàn bộ cho `BroadcastService@sendTestBroadcast`
- **Cải tiến so với legacy**: Sử dụng `TemplateService::mergeListTemplate()`, `MessageService::createMessageTypeV2()`

#### ajaxGetProfileOfBots() — Danh sách profile người gửi
- **File:line**: `BroadcastController.php:2388-2458`
- **Logic**:
  1. Lấy profile đang chọn (hoặc default)
  2. Nếu chưa có default profile → tạo mới từ `bot.view_name`, `bot.bot_image`
  3. Lấy profiles Admin (sorted: is_default DESC → position ASC → id DESC)
  4. Lấy profiles Staff (is_default = 0)
  5. Default profile luôn dùng `bot.bot_image` làm avatar
- **Lưu ý**: Profile default phản ánh LINE OA settings, không phải custom profile

#### ajaxInitCreateData() — Khởi tạo dữ liệu tạo broadcast
- **File:line**: `BroadcastController.php:1039-1091`
- **Logic**: Lấy tag groups, tag items, scenarios, đếm `number_send` (tổng bot_line_user không bị block)

#### ajaxCountVariableSend() — Đếm người nhận (legacy filter)
- **File:line**: `BroadcastController.php:1097-1127`
- **Logic**: Join `bot_line_user` với `scenario_lineuser` và `tag_line_user` → count distinct

#### ajaxInitListLineUserData() — Tìm kiếm LINE users
- **File:line**: `BroadcastController.php:955-987`
- **Logic**: Tìm theo `name` hoặc `view_name` + lấy danh sách testers (`is_tester=1`)

#### ajaxUpdateTesterLineData() — Toggle trạng thái tester
- **File:line**: `BroadcastController.php:1022-1037`
- **Logic**: Update `bot_line_user.is_tester` và reset `is_quick_reply = 0`

#### deleteMessage() — Xoá message khỏi broadcast
- **File:line**: `BroadcastController.php:2142-2167`
- **Logic**: Xoá template_id khỏi `template_ids`. Nếu hết → `status = 'unregistered'`

#### createMessageByTemplate() — Thêm message từ template
- **File:line**: `BroadcastController.php:2557-2605`
- **Logic**:
  1. Kiểm tra 5 phút rule
  2. Thêm template_id vào `template_ids`
  3. **Quick Reply**: nếu template cuối là ButtonQuickReply → giữ nó ở cuối

#### broadcastHistories() — Lịch sử gửi
- **File:line**: `BroadcastController.php:2670-2729`
- **Logic**: Query `messages_v2` theo `source_message_id`, join `conversation` + `line_user` → hiển thị người nhận

---

### 1.2 BroadcastV2Controller

**File**: `app/Http/Controllers/Basic/BroadcastV2Controller.php` (1054 lines)
**Namespace**: `App\Http\Controllers\Basic`

#### addBroadcastV2() — Form tạo/chỉnh sửa
- **File:line**: `BroadcastV2Controller.php:123-152`
- **Logic**: Lấy broadcast nếu có `broadcast_id`, đếm `totalUser` → trả view

#### saveBroadcastV2() — Lưu broadcast (CORE V2)
- **File:line**: `BroadcastV2Controller.php:154-417`
- **Logic** (xem chi tiết trong api-spec EP-10)
- **Business rules quan trọng**:
  - `name` bắt buộc
  - `send_day` bắt buộc (không phải `0000:00:00`)
  - Profile default → `profile_id = null`
  - Tạo mới luôn bắt đầu với `status = 'draft'`
  - **Multi-schedule (delivery_dates)**:
    - Tạo child broadcasts với `parent_id = broadcastIdNew`
    - Clone templates cho mỗi child (templates category -11 → clone, khác → share)
    - Clone actions cho mỗi child
    - Xoá children không còn trong danh sách mới
  - **Filter sync**: copy filters từ parent sang children mới
  - Cập nhật `bots_tutorial.status_send_all = 1` (tutorial tracking)

#### getDetailBroadcastV2() — Chi tiết broadcast
- **File:line**: `BroadcastV2Controller.php:520-669`
- **Logic**:
  - `check_can_edit`: false nếu status=`wait_to_send` và < 5 phút trước giờ gửi
  - Load action details, delivery dates, filters, profile, messages

#### getListMessage() — Danh sách messages trong broadcast
- **File:line**: `BroadcastV2Controller.php:671-704`
- **Logic**: Lấy templates từ `template_ids`, load buttons, item_records cho type 'group'

#### deleteMutitpleBroadcast() — Xoá hàng loạt
- **File:line**: `BroadcastV2Controller.php:706-748`
- **Logic**: Kiểm tra 5 phút rule cho `wait_to_send`, xoá templates + broadcast

#### copyBroadcastV2() — Sao chép broadcast
- **File:line**: `BroadcastV2Controller.php:860-964`
- **Logic**: Clone broadcast, templates, actions, filters, children → status = 'draft'

#### deleteItemAction() — Xoá action detail
- **File:line**: `BroadcastV2Controller.php:966-1005`
- **Logic**: Kiểm tra 5 phút rule, xoá filter + ActionDetail, nếu hết detail → nullify action_id

#### removeItemMessageBroadcastV2() — Cập nhật template list
- **File:line**: `BroadcastV2Controller.php:1007-1034`
- **Logic**: Kiểm tra 5 phút rule, cập nhật `template_ids` + `update_timestamp`

#### saveActionBroadcastV2() — Xoá action khỏi broadcast
- **File:line**: `BroadcastV2Controller.php:1036-1053`
- **Logic**: Set `action_id = null` cho broadcast + children

#### saveBotProfile() — Lưu profile người gửi
- **File:line**: `BroadcastV2Controller.php:42-99`
- **Logic**: Tạo mới hoặc cập nhật BotsProfiles

#### sortProfileV2() — Sắp xếp profiles
- **File:line**: `BroadcastV2Controller.php:101-121`
- **Logic**: Update `position` theo thứ tự mảng `arr_sort_profile`

#### uploadFile() — Upload avatar
- **File:line**: `BroadcastV2Controller.php:31-39`
- **Logic**: Upload file → `uploadThumbnail()` → resize 240x240

---

## 2. Models Eloquent

### 2.1 BroadCast

**File**: `app/BroadCast.php` (79 lines)
**Table**: `broadcast`
**Connection**: mysql
**Timestamps**: true
**Guarded**: `[]` (mass assignment không giới hạn)

**Relationships**:

| Relationship | Type | Model | FK (local→foreign) |
|-------------|------|-------|---------------------|
| `template()` | hasOne | Template | id → template_id |
| `template2()` | hasOne | Template | id → template_id_2 |
| `template3()` | hasOne | Template | id → template_id_3 |
| `rich_menus()` | hasOne | RichMenus | id → rich_menu_id |
| `filter()` | hasOne | Filter | broadcast_id |
| `profileBot()` | belongsTo | BotsProfiles | profile_id → id |
| `sourceMessage()` | belongsTo | SourceMessage | id → broadcast_id |

**Static method**: `createBroadcast($bot_id, $template_id, $request)` — tạo broadcast (legacy)

**Cột quan trọng** (suy luận từ code):

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | int (PK) | |
| `bot_id` | int (FK) | Bot sở hữu |
| `name` | string | Tiêu đề quản lý (V2) |
| `status` | string | draft, unregistered, not_delivery, wait_to_send, delivering, delivered, send_false |
| `send_day` | date | Ngày gửi |
| `send_time` | time | Giờ gửi |
| `setting_send_message` | int | 0=gửi ngay, 1=đặt lịch |
| `template_id` | int (FK) | Template chính (legacy) |
| `template_id_2` | int (FK) | Template 2 (legacy) |
| `template_id_3` | int (FK) | Template 3 (legacy) |
| `template_ids` | text | Comma-separated template IDs (V2) |
| `tag_id` | text | Comma-separated tag IDs (legacy filter) |
| `scenario_id` | int (FK) | Scenario filter (legacy) |
| `rich_menu_id` | int (FK) | Rich menu gắn kèm |
| `profile_id` | int (FK) | Profile người gửi (null = default) |
| `action_id` | int (FK) | Action thực thi khi gửi |
| `parent_id` | int (FK) | Parent broadcast (multi-schedule) |
| `kind` | string | Loại broadcast |
| `filter_number` | int | Số người nhận dự kiến |
| `filter_date` | datetime | Thời điểm tính filter |
| `send_count` | int | Số người đã gửi thực tế |
| `update_timestamp` | int | Unix timestamp cập nhật cuối |
| `created_at` | timestamp | |
| `updated_at` | timestamp | |

### 2.2 FilterV2

**File**: `app/FilterV2.php`
**Table**: `filters_v2`
**Connection**: mysql

**Cột quan trọng** (suy luận từ code):

| Cột | Mô tả |
|-----|-------|
| `id` | PK |
| `parent_id` | ID của broadcast (hoặc entity khác) |
| `parent_type` | `'broadcast'`, `'broadcast-v2'`, `'modal_action'` |
| `bot_id` | Bot ID |
| `operator` | `'and'` hoặc `'or'` |
| `type` | Loại filter (tag, friend_name, friend_add_date, step...) |
| `data` | JSON — dữ liệu filter chi tiết |
| `text_preview` | Text hiển thị preview |

**Static methods**:
- `cloneFilters($oldId, $newId, $parentType)` — clone filters
- `deleteActionFilterByActions($actionIds)` — xoá filter theo action

### 2.3 BotsProfiles

**File**: `app/BotsProfiles.php`
**Table**: `bots_profiles`
**Connection**: mysql

**Cột quan trọng**:

| Cột | Mô tả |
|-----|-------|
| `id` | PK |
| `bot_id` | Bot ID |
| `user_id` | User (Admin/Staff) ID |
| `nick_name` | Tên hiển thị |
| `avt_path` | Đường dẫn avatar |
| `is_default` | 1=profile mặc định (= LINE OA name), 0=custom |
| `position` | Thứ tự sắp xếp |

### 2.4 Template

**File**: `app/Template.php`
**Table**: `template`
**Connection**: mysql

**Cột quan trọng** (broadcast-related):

| Cột | Mô tả |
|-----|-------|
| `id` | PK |
| `bot_id` | Bot ID |
| `name` | Tên template |
| `type` | text, image, video, voice, stamp, form, question, location, introduction, group |
| `content` | Nội dung (text content, media path, hoặc comma-separated IDs cho group) |
| `category_id` | `-11` = broadcast template, `>=0` = shared template |
| `is_shorten_url` | Có rút gọn URL không |
| `image_server` | URL server media |
| `thumbnail_path` | Đường dẫn thumbnail |
| `position` | Thứ tự |
| `carousel_action_type` | Kiểu action carousel (cho type form) |
| `rate_image_button` | Tỷ lệ image (cho form) |
| `duration` | Thời lượng (audio/video) |
| `action_video_id` | Action khi tap video |
| `number_action_url_redirect` | Số action URL redirect |

**Relationships**: question, buttons, btn_templates, location, introduction, templateUrlRedirect

### 2.5 SourceMessage

**File**: `app/SourceMessage.php`
**Table**: `source_messages`
**Connection**: mysql_message

Liên kết broadcast → message delivery tracking.

### 2.6 MessagesV2

**File**: `app/MessagesV2.php`
**Table**: `messages_v2s`
**Connection**: mysql_message

**Constants**:
- `TYPE_MESSAGE_BROADCAST` — type cho broadcast message
- `KIND_MESSAGE_BROADCAST` — msg_kind cho broadcast
- `KIND_MESSAGE_SEND_TEST` — msg_kind cho test send

---

## 3. Services / Repositories

### 3.1 BroadcastService

**File**: `app/Services/BroadcastService.php` (127 lines)

**Dependencies** (injected):
- `ConversationRepositoryInterface`
- `TemplateRepositoryInterface`
- `MessageService`
- `BotRepositoryInterface`
- `BroadcastRepositoryInterface`
- `TemplateService`
- `LineUserRepositoryInterface`

**Methods**:

#### sendTestBroadcast($request)
- **File:line**: `BroadcastService.php:53-126`
- **Logic**:
  1. Lấy broadcast, bot, profile
  2. Nếu không có profile → lấy default profile
  3. Build message metadata: `msg_kind`, `profile_send`, `type`, `broadcastId`, `versionId`, `name`, `sendDate`
  4. Với mỗi tester:
     - Lấy conversation
     - `TemplateService::mergeListTemplate()` → mảng messages
     - Chunk thành batches 5 messages
     - `MessageService::createMessageTypeV2()` → gửi qua LINE API
     - Nếu thành công: `free_send_count + 1`, `updateMessageSendCount`
     - Nếu có actionId: `sendAction()`
  5. Nếu thất bại: trả error response

### 3.2 Conversation (Model as query builder)

**Hàm quan trọng**: `Conversation::advanceFilterPost($bot_id, $filterAnd, $filterOr, ...)`
- Xử lý 11 loại filter: tag, friend_name, friend_add_date, step_subscription, qr_code_action, conversion, confirmation_status, friend_info, response_status, affiliate, new_existing_friend
- Join nhiều bảng: `bot_line_user`, `tag_line_user`, `scenario_lineuser`, `line_user`...
- Trả về query builder → caller gọi `count()` hoặc `get()`

---

## 4. Form Requests / Validation

**Không sử dụng FormRequest** — validation được thực hiện inline trong controller methods:

| Rule | Vị trí | Mô tả |
|------|--------|-------|
| `botIdCurrent != getBotId()` | messageStore:275, updateMessage:651 | Kiểm tra bot không bị switch |
| `name` required | saveBroadcastV2:199 | Tiêu đề quản lý bắt buộc |
| `send_day` required | saveBroadcastV2:180 | Ngày gửi bắt buộc |
| Status check | messageStore:278, updateMessage:654 | Không cho sửa broadcast `delivered`/`delivering` |
| 5 phút rule | updateMessage:656-661, saveBroadcastV2:251 | Không cho sửa < 5 phút trước giờ gửi |
| ImageMap area | messageStore:293, updateMessage:783 | x≥0, y≥0, width≥1, height≥1, tất cả numeric |
| `checkFormatDate()` | storeBroadCast:401 | Validate format ngày |

---

## 5. Events / Listeners / Queued Jobs

### Không có Laravel Queue Jobs trực tiếp
- Broadcast KHÔNG dispatch job trong Laravel
- Sử dụng **Database Polling Model**: Laravel insert/update record `broadcast` với `status = 'wait_to_send'`
- **Spring Boot Job** poll bảng `broadcast` mỗi ~5 giây → tìm records cần gửi → xử lý gửi hàng loạt

### Side Effects khi gửi test
- `sendAction($actionId, $lineUserId, ...)` — gọi helper function `app/Helpers/functions.php`
  - Thực thi action detail: gán tag, thay đổi rich menu, trigger step, ghi conversion...
- `createMultipleMessage(...)` / `createMessageTypeV2(...)` — gửi message qua LINE Messaging API
- `updateMessageSendCount($botId, $date, $type)` — cập nhật counter
- `createMessageError(...)` — ghi lỗi gửi message

### Tutorial tracking
- `BotsTutorial::status_send_all = 1` khi tạo broadcast đầu tiên (BroadcastV2Controller:276)
- `checkUpdateHasTutorial($botId)` — kiểm tra và cập nhật tutorial progress

---

## 6. Authorization (Access Control)

### Middleware level
- Không có middleware access control riêng (như `staff_access` hay `admin_access`) cho broadcast routes
- Xác thực dựa trên `Auth::user()` + `getBotId()` (session)

### Data-level authorization
- **Bot isolation**: Mọi query đều filter theo `bot_id = getBotId()` (từ session)
- **Broadcast ownership**: Kiểm tra `broadcast.bot_id == getBotId()` trước khi truy cập
- **Profile visibility**: Admin thấy tất cả profiles (admin + staffs), Staff chỉ thấy profiles của mình

### Staff access
- Staff có thể tạo/chỉnh sửa broadcast (không có check riêng trong code)
- Quyền Staff được quản lý ở middleware layer chung (`RoleAccess`, `AccessFeature`) — không phải trong broadcast controller
- Profile người gửi: Staff chỉ có thể tạo profile cho mình (`user_id = Auth::user()->id`)

---

## 7. Business Rules (tổng hợp từ code)

### BR-01: Broadcast Status Lifecycle
**Nguồn**: `BroadcastController.php:351-357`, `BroadcastV2Controller.php:256-268`

```
[Tạo mới] → draft/unregistered
    ↓ (thêm template + có schedule)
wait_to_send
    ↓ (Background Job xử lý)
delivering → delivered / send_false
```

- `draft` (V2) = `unregistered` + `not_delivery` (legacy)
- Chuyển `draft → wait_to_send` khi có templates VÀ có schedule/action
- `delivering`, `delivered` → không thể sửa/xoá

### BR-02: 5 phút rule (edit lock)
**Nguồn**: `BroadcastController.php:656-661`, `BroadcastV2Controller.php:251-253`, `BroadcastV2Controller.php:534`

- Broadcast `wait_to_send` không thể sửa/xoá nếu thời gian gửi - hiện tại < 5 phút
- **Thực tế trong code**: `subMinutes(6)` (buffer thêm 1 phút)
- Áp dụng cho: edit, delete single, delete multiple, add/remove message, add/remove action

### BR-03: Multi-schedule (delivery_dates)
**Nguồn**: `BroadcastV2Controller.php:281-378`

- 1 broadcast có thể gửi vào nhiều thời điểm khác nhau (tối đa 10 — từ UI spec)
- Thời điểm đầu tiên = broadcast chính
- Các thời điểm bổ sung = child broadcasts (`parent_id = broadcast.id`)
- Children clone templates và actions từ parent
- Templates có `category_id >= 0` (shared) → không clone, chỉ reference
- Templates có `category_id < 0` (broadcast-specific, `-11`) → clone

### BR-04: Template management
**Nguồn**: `BroadcastController.php:306-349`, `BroadcastV2Controller.php:229-234`

- Broadcast V2 sử dụng `template_ids` (comma-separated string)
- 6 loại message: text, image, video, voice, stamp, form (panel+button)
- Thêm 3 loại composite: group (pack message), question, introduction, location
- **Quick Reply**: template ButtonQuickReply luôn ở cuối danh sách `template_ids`
- **LINE API limit**: tối đa 5 messages/batch khi gửi

### BR-05: Profile người gửi
**Nguồn**: `BroadcastController.php:2388-2458`, `BroadcastV2Controller.php:206-209`

- Default profile = LINE Official Account (bot_image, view_name)
- Custom profiles: Admin/Staff có thể tạo nhiều profiles
- Khi chọn default → `broadcast.profile_id = null`
- Khi xoá profile đang dùng → fallback về default (set profile_id = null)

### BR-06: Filter V2 (Lọc đối tượng)
**Nguồn**: `BroadcastController.php:2517-2534`

- Sử dụng `filters_v2` table (parent_type = 'broadcast')
- Hỗ trợ AND + OR conditions
- 11 loại filter (xem ui-spec SCR-BC-03)
- `Conversation::advanceFilterPost()` xử lý logic filter phức tạp
- `filter_number` = kết quả đếm → lưu vào broadcast + children

### BR-07: Copy broadcast
**Nguồn**: `BroadcastV2Controller.php:790-858`, `BroadcastV2Controller.php:860-964`

- Clone toàn bộ: broadcast record, templates, actions, filters, children
- Templates shared (category_id >= 0) → giữ nguyên reference
- Templates broadcast-specific (category_id < 0) → clone qua `cloneTemplate()`
- Actions → clone qua `cloneAction()` (clone cả action_detail + filter)
- Status bản copy = `'draft'`

### BR-08: Bot switch check (legacy)
**Nguồn**: `BroadcastController.php:275-277`, `BroadcastController.php:651-653`

- Kiểm tra `botIdCurrent` (từ form) == `getBotId()` (từ session)
- Phòng trường hợp user switch bot ở tab khác trong khi đang sửa broadcast
- Message lỗi: 「別のアカウントに切り替えたので、要求を処理できません。」

### BR-09: URL handling trong text message
**Nguồn**: `BroadcastController.php:697`, `BroadcastController.php:871-886`

- `detectUrlInMessageTextV2($content, $bot)` — detect URLs trong text
- URL được rút gọn (shorten) để tracking
- `is_shorten_url` flag — cho phép tắt URL tracking
- URL detect metadata → lưu vào `url` table
- Template URL redirect → lưu vào `template_url_redirect` table

### BR-10: Message gửi không thay đổi sau khi delivered
**Nguồn**: `BroadcastController.php:278-285`, `BroadcastController.php:664-671`

- Broadcast `delivering` → lỗi「配信処理中です。編集できません。」
- Broadcast `delivered` → lỗi「既に配信済のため変更できません。」
- Áp dụng cho tất cả operations: edit, delete, add/remove message

---

## 8. Helper Functions quan trọng

| Function | File | Mô tả |
|----------|------|-------|
| `getBotId()` | `app/Helpers/functions.php` | Lấy bot ID từ session |
| `getCurrentUser()` | `app/Helpers/functions.php` | Lấy user ID hiện tại |
| `addLogUserAction($action)` | `app/Helpers/functions.php` | Ghi log hành động user |
| `detectUrlInMessageTextV2($content, $bot)` | `app/Helpers/functions.php` | Detect và xử lý URL trong text |
| `createMultipleMessage(...)` | `app/Helpers/functions.php` | Gửi multiple messages qua LINE API |
| `sendAction($actionId, ...)` | `app/Helpers/functions.php` | Thực thi action (tag, step, rich menu...) |
| `cloneTemplate($templateId)` | `app/Helpers/functions.php` | Clone template + relationships |
| `updateMessageSendCount($botId, $date, $type)` | `app/Helpers/functions.php` | Cập nhật counter gửi message |
| `createMessageError(...)` | `app/Helpers/functions.php` | Ghi lỗi gửi message |
| `checkFormatDate($date)` | `app/Helpers/functions.php` | Validate format ngày |
| `checkTemplateIsButtonQuickReply($templateId)` | `app/Helpers/functions.php` | Kiểm tra template có phải QuickReply không |
| `notifyChatwork($message)` | `app/Helpers/functions.php` | Gửi thông báo Chatwork |
| `uploadThumbnail($file, $path, $size)` | `app/Helpers/functions.php` | Upload + resize thumbnail |
| `uploadThumbnailApi(...)` | `app/Helpers/functions.php` | Upload thumbnail qua API server |
| `uploadFileDropbox($content, $type)` | `app/Helpers/functions.php` | Upload file lên Dropbox |
| `checkUpdateHasTutorial($botId)` | `app/Helpers/functions.php` | Cập nhật tutorial progress |

---

## 9. Background Job Trigger Points

Các điểm trong code **trigger Background Job** (thông qua Database Polling — Spring Boot poll bảng `broadcast`):

| Trigger | Code Location | Điều kiện |
|---------|--------------|-----------|
| Tạo broadcast scheduled | `BroadcastV2Controller.php:262-264` | `status = 'wait_to_send'` + có template/action |
| Edit broadcast → set schedule | `BroadcastController.php:503-504` | `not_delivery → wait_to_send` |
| Multi-schedule child | `BroadcastV2Controller.php:326-331` | Mỗi delivery_date → `status = 'wait_to_send'` |

**⚠️ Ghi chú cho job-analyzer**: Spring Boot job cần poll bảng `broadcast` tìm records có:
- `status = 'wait_to_send'`
- `send_day + send_time <= NOW()`
- Xử lý: đổi status → `delivering`, gửi messages, đổi → `delivered` hoặc `send_false`
