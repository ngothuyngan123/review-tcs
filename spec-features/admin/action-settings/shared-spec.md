# SC-004 Action Settings — Shared Component Spec

**Mã:** SC-004  
**Tên:** Action Settings (Modal アクション)  
**Phiên bản:** 2025-05-20  
**Trạng thái:** ĐẠT validation  
**Độ tin cậy tổng thể:** **Cao** (source code + DB schema + sample data xác nhận)

---

## 1. Tổng quan

SC-004 là shared modal component 「アクション」 cho phép Admin/Staff cấu hình một hoặc nhiều hành động tự động được thực thi khi một sự kiện xảy ra (người dùng nhấn nút, gửi tin nhắn, đáp lại auto-reply, v.v.).

**Đặc điểm chính:**
- Hỗ trợ **multi-action**: nhiều hành động xếp thứ tự trong cùng 1 cấu hình
- Mỗi action có thể kèm **bộ lọc riêng** 「絞込」 — chỉ áp dụng cho nhóm bạn bè thỏa điều kiện
- Tách biệt **10 action types kết hợp** (main) và **9 action-only types** (không thể kết hợp với nhau)
- Chỉ **lưu cấu hình** — không tự trigger job. Execution nằm ở Spring Boot jobs (chưa phân tích)

**Actors:**
- **Admin** — toàn quyền cấu hình
- **Staff** — tùy quyền được phân công

**Scope:** Component chỉ chịu trách nhiệm lưu config vào `t_actions` + `t_actions_detail`. Việc thực thi các actions khi có trigger event thuộc về Spring Boot background jobs.

### Các tính năng sử dụng SC-004

| Tính năng | FA code | Ngữ cảnh dùng |
|-----------|---------|--------------|
| Chat 1:1 | FA-001 | Action khi chat |
| Auto Reply | FA-003 | Action khi keyword match |
| Broadcast/Step Message | FA-004 | Action khi deliver |
| Scenario (step delivery) | FA-009 | Action per step |
| Rich Menu | FA-010 | Action per button |
| URL Tracking | FA-012 | Action khi click link |
| Form Answer | FA-013 | Action khi submit form |
| Bookmark | FA-014 | Action bookmark event |
| Action Schedule | FA-015 | Action theo lịch |

---

## 2. Variants

Component tồn tại ở **3 variants** tương ứng 3 file Blade:

| Variant | File Blade | Modal Title JP | DOM ID | Trường hợp dùng |
|---------|-----------|----------------|--------|----------------|
| **V1** (Legacy) | `modal_setting_action.blade.php` | 「友だち一括操作」 | `#settingActionUrlModal` | Bulk action từ Friend List. 4 tabs cố định. Không hỗ trợ multi-action. |
| **V2** (Main) | `modal_select_action.blade.php` | 「アクション」 | `#settingActionUrlModal` (trong `#vue_modal_action`) | Full action modal — sidebar trái + panel phải. Hỗ trợ multi-action + filter per action. **Đây là version chính.** |
| **V3** (Pro Edit) | `modal_select_action_pro.blade.php` | 「アクション編集」 | `#settingActionUrlModal` | Chỉnh sửa action đã tạo. Bố cục tương tự V2, thêm section 「設定されたアクション」ở trên. |

**V1 khác biệt:** 4 tabs cố định (テンプレート送信, ステップ, タグ, リッチメニュー), dùng jQuery truyền thống, không có Vue reactivity, không hỗ trợ filter per action.

**V3 khác biệt:** Phần scenario/template/remind dùng PHP foreach + dropdown cũ thay vì Vue combo-box; label dùng 【】 bracket (V2 dùng không có bracket).

---

## 3. Action Types — V2 Đầy đủ

### 3.1 Main Action Types (kết hợp được)

| # | Type Key | Tên JP | Giới hạn | Điều kiện hiển thị | Tables tham chiếu |
|---|---------|--------|---------|-------------------|-----------------|
| 1 | `scenario` | 「ステップ」 | Tối đa 1 per config | Ẩn khi `type_action == 'step_message'` | `scenario`, `category` (kind=11) |
| 2 | `template` | 「テンプレート」 | Không giới hạn | Ẩn khi `type_action` là `'broadcast_v2'` hoặc `'step_message'` | `template`, `category` (kind=2) |
| 3 | `text` | 「テキスト」 | Không giới hạn | Ẩn khi `type_action` là `'broadcast_v2'` hoặc `'step_message'` | Inline trong `data` |
| 4 | `remind` | 「リマインド」 | Tối đa 1 per config | Ẩn khi `type_action` thuộc `listActionNotShowRemind` (20+ values) | `events`, `event_times`, `category` (kind=18) |
| 5 | `tag` | 「タグ」 | Không giới hạn | Luôn hiển thị | `tags`, `category` (kind=0) |
| 6 | `richmenu` | 「リッチメニュー」 | Tối đa 1 per config | Ẩn khi `type_action == 'richmenu'` | `rich_menus`, `category` (kind=17) |
| 7 | `bookmark` | 「ブックマーク」 | Không giới hạn | Ẩn khi `type_action == 'bookmark'` | Inline trong `data` |
| 8 | `friend_info` | 「友だち情報」 | Không giới hạn | Luôn hiển thị | `friend_information_setting`, `friend_info_option_selects`, `action_info_friend_default`, `category` (kind=12) |
| 9 | `compliant_status` | 「対応ステータス」 | Không giới hạn | Luôn hiển thị | `status_chat` |
| 10 | `block` | 「ブロック・非表示」 | Không giới hạn | Luôn hiển thị | Inline trong `data` |

**Giới hạn `type_ignore`:** `scenario`, `richmenu`, `remind` — sau khi đã thêm 1 item thuộc các type này, button tương ứng trong sidebar bị disable. **Độ tin cậy:** **Cao**

### 3.2 Action-Only Types (không kết hợp được)

Hiển thị ở zone riêng phía trên sidebar. `action_only` và `actions[]` loại trừ nhau — không thể tồn tại đồng thời.

| # | Type Key | Tên JP | Cấu hình | JSON data |
|---|---------|--------|----------|-----------|
| 1 | `form_answer` | 「フォーム作成」 | Select từ danh sách form | `{"id": 1}` → `form_answer.id` |
| 2 | `booking` | 「イベント予約」 | Select từ danh sách booking | `{"id": 1}` → `b_event_detail.id` |
| 3 | `product_page` | 「商品ページ」 | Select từ danh sách sản phẩm | `{"id": 1}` → product table id (**Trung bình** — tên bảng chưa confirm) |
| 4 | `conversion` | 「CV登録ページ」 | Select từ danh sách conversion | `{"id": 1}` → conversion table id (**Trung bình** — tên bảng chưa confirm) |
| 5 | `other_text` | 「テキストを送信させる」 | Textarea max 5000 ký tự | `{"content": "テキスト"}` |
| 6 | `keywords` | 「キーワードを送信させる」 | Select từ danh sách keyword | `{"id": 1}` → keyword table id (**Trung bình** — tên bảng chưa confirm) |
| 7 | `phone` | 「電話をかけさせる」 | Input số điện thoại | `{"content": "0901234567"}` |
| 8 | `email` | 「メールを送る」 | Input email | `{"content": "user@example.com"}` |
| 9 | `add_friend` | 「友だち追加ページを開く」 | Input LINE ID (`@abc123`) | `{"id": "@lineId"}` |

---

## 4. Context Modes (`type_action`)

Tham số `type_action` được truyền từ trang cha vào Vue data (`setting_action.type_action`). Quyết định: (1) action buttons nào hiển thị trong sidebar, (2) nút 「保存」 gọi method nào.

| `type_action` | Mô tả ngữ cảnh | Action bị ẩn | Save handler |
|--------------|----------------|-------------|-------------|
| `reply` | Auto-reply action | (không ẩn đặc biệt) | `saveSettingAction()` |
| `broadcast_v2` | Broadcast v2 action | テンプレート, テキスト | `saveSettingAction()` |
| `step_message` | Step message action | ステップ, テンプレート, テキスト | `saveSettingAction()` |
| `richmenu` | Rich menu button action | リッチメニュー | `saveSettingAction()` |
| `bookmark` | Bookmark action | ブックマーク | `saveSettingAction()` |
| `booking_event_day` | Event booking day | リマインド (in listActionNotShowRemind) | `saveSettingAction()` |
| `booking_event_day_plan` | Event booking day plan | リマインド | `saveSettingAction()` |
| `bill_item_v2` | Bill/product action | (không ẩn sidebar — hiện thêm merge tag 商品決済) | `saveSettingAction()` |
| `button` | Template button action | — | `saveSettingActionButton()` |
| `image_map` | Image map area action | — | `saveSettingActionImageMap()` |
| `video` | Video action | — | `saveSettingActionVideo()` |
| `formAnswer_setting_action` | Form answer action | — | `saveSettingActionFormAnswer()` |
| `formAnswer_diagnostic_content` | Form diagnostic | — | `saveSettingActionFormAnswer()` |
| `add_friend_new` | Add friend action | — | `saveSettingAction()` |
| `preview-chat11` | 1:1 chat preview | — | Nút 「保存」 bị disabled |

**`listActionNotShowRemind`** (danh sách đầy đủ — nguồn `select_action.js:199`):
`calendar_notify_full`, `calendar_notify_not_full`, `setting_message_booking`, `setting_message_booking_request`, `setting_message_booking_approve`, `setting_message_booking_deny`, `setting_message_cancel_booking`, `setting_message_cancel_request`, `setting_message_cancel_approve`, `setting_message_cancel_deny`, `status-send-after-booking`, `preview-calendar`, `event_step_calendar`, `calendar_salon_notify_full`, `calendar_salon_notify_not_full`, `setting_message_booking_salon` (và các variants salon), `event_step_calendar_salon`, `calendar-salon-status-send-after-booking`, `calendar-staff-status-send-after-booking`, `calendar-staff-status-send-approve-booking`, `calendar-salon-status-send-approve-booking`. **Độ tin cậy:** **Cao**

---

## 5. Luồng xử lý End-to-End

### 5.1 Load Data Flow (DB → Modal)

```
Trang cha trigger mở modal
    │  set hidden inputs: #action_idx, #plan_key, #button_tab_id, v.v.
    │  set Vue data: setting_action.action_id = existing_id (hoặc '')
    │  set Vue data: setting_action.type_action = 'reply' / 'broadcast_v2' / ...
    ▼
Modal open event → Vue created() hook
    ├── POST /ajax/get-bot-data (EP-14) → kiểm tra plan_type → quyết định hiển thị filter button
    ├── POST /ajax/init-status-chat (EP-12) → load danh sách 対応ステータス
    └── POST /ajax/action/init-data (EP-01) { id: action_id }
            ↓
        ActionController@initDataAction
            ├── Load t_actions + t_actions_detail records
            ├── Enrich từng detail: thêm groups, group_items, tên cache
            ├── Tách action_only (type thuộc type_only list) ra riêng
            └── Load danh sách dropdown: form_answers, bookings, products, conversions, keywords, friend_info
            ↓
        Response → Vue state:
            actions[]    = action_detail array (main actions)
            action_only  = action_only object (nếu có)
            Dropdowns    = form_answers, bookings, products, conversions, keywords, dataFriendInfo
    ▼
Modal render: sidebar trái + panel phải với actions đã load
```

### 5.2 Save Data Flow (Modal → DB)

```
User click 「保存」
    ▼
Frontend validation (vee-validate RC7 + custom JS)
    │  Nếu fail → hiển thị lỗi, không submit
    ▼
POST /ajax/action/save (EP-02)
    { id, type, action_detail: JSON.stringify(actions) }
    ▼
ActionController@saveAction
    ├── Check backup đang chạy → return error nếu có
    ├── Check broadcast trong 5 phút tới → return error nếu có
    ├── id empty (new) → INSERT t_actions → get new id
    │       └── foreach action_detail → INSERT t_actions_detail
    └── id exists (edit):
            ├── foreach action_detail:
            │   ├── detail.id empty → INSERT t_actions_detail
            │   └── detail.id exists → UPDATE t_actions_detail
            └── DELETE t_actions_detail WHERE id NOT IN (saved ids)
                └── FilterV2::delete WHERE parent_type='modal_action' AND parent_id IN (deleted ids)
    ▼
    Nếu action item có change_filter=1:
        FilterV2::saveFilter(filter_and, filter_or, 'modal_action', detail_id)
        UPDATE t_actions_detail.has_filters = 0 hoặc 1
    ▼
    Behavior phụ theo type (update FK ở bảng cha):
        - formAnswer_setting_action → update form_answers.action_reply_id / action_open_id
        - status-send-after-booking → update calendar_courses.action_id_send_after_booking
        - (xem đầy đủ EP-02 api-spec.md)
    ▼
Response: { success: true, action_id: 42 }
    ▼
Frontend cập nhật parent component với action_id mới
```

### 5.3 Filter per Action Flow

```
User click 「絞込 未設定」 trên action item
    ▼
openModalFilter(indexAction)
    ├── Nếu action chưa có filter data trong memory:
    │   GET /ajax/initDataFilterBroadcast (EP-13)
    │       { broadcastFilterId: action_detail_id, parent_type: 'modal_action' }
    │   → load filter conditions từ filters_v2
    └── Nếu đã có → dùng data in-memory
    ▼
Modal filter (SC-003 Friend Filter) mở
    ▼
User cấu hình filter conditions → xác nhận
    ▼
Filter data được lưu vào action item in-memory
action.change_filter = 1 (đánh dấu cần save filter)
    ▼
Button đổi thành 「絞込 設定済」
    ▼
Khi user click 「保存」 của main modal → filter được gửi trong action_detail JSON
    → FilterV2::saveFilter() tại backend → UPDATE has_filters = 1
```

### 5.4 Add Tag Inline Flow

```
User click [タグ新規追加] trong action type タグ
    ▼
Sub-modal #modalAddTagModalAction mở (main modal đóng tạm)
    ▼
User chọn folder + nhập tên tag (max 50 ký tự — watch Vue)
    ▼
Click 「保存してアクションに設定に戻る」
    ▼
POST /ajax/save-add-tag-in-modal-action (EP-10)
    { tag_name, folder_id }
    ▼
ActionController@saveAddTag
    ├── Check tên rỗng → error
    ├── Check tên trùng trong bot → error
    └── INSERT tags { bot_id, name, category_id=folder_id, action_id=NULL }
        UPDATE position = max(position) + 1
    ▼
Response success → đóng sub-modal, mở lại main modal
    → gọi initDataTag(group_id) để refresh tag list
    ▼
Tag mới xuất hiện trong list để chọn
```

---

## 6. Data Model

### 6.1 Bảng cốt lõi

**`t_actions`** — Container cho bộ action settings. Data size: 8.8MB.

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | int UNSIGNED PK | Primary key |
| `parent_id` | int | Luôn = 0 trong thực tế. FK ngược được lưu ở bảng cha. |
| `type` | varchar(255) | Context type: `richmenu`, `auto_reply`, `button`, `qrcode`, v.v. (21+ values) |
| `update_timestamp` | bigint | Unix timestamp cập nhật |

**`t_actions_detail`** — Chi tiết từng action item (1 `t_actions` có nhiều records). Data size: 14.7MB.

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | int UNSIGNED PK | Primary key |
| `action_id` | int | FK → `t_actions.id` |
| `bot_id` | int NULL | Bot owner (có thể NULL ở record cũ) |
| `type` | varchar(255) | Action type: 19 values (xem mục 3) |
| `data` | text | JSON config — cấu trúc khác nhau theo type |
| `embed_regex_text` | varchar(255) NULL | Regex embed URL cho URL tracking detection |
| `has_filters` | tinyint | 0=không có filter, 1=có filter |

### 6.2 Bảng filter

**`filters_v2`** — Điều kiện lọc (絞込) cho từng action detail. Data size: 17.8MB.

Khi `parent_type = 'modal_action'` → `parent_id = t_actions_detail.id`.

| Cột | Mô tả |
|-----|-------|
| `parent_type` | `'modal_action'` |
| `parent_id` | FK → `t_actions_detail.id` |
| `operator` | `'and'` hoặc `'or'` |
| `type` | Loại filter: `friend_name`, `tag`, `scenario`, `friend_info`, `day_add_friend`, `qr_code`, `conversion`, `status_search`... |
| `data` | JSON config condition |
| `text_preview` | Text preview hiển thị |

### 6.3 Bảng lookup (được share với các tính năng khác)

| Bảng | category.kind | Dùng cho action type | Data size |
|------|--------------|---------------------|-----------|
| `scenario` | 11 | `scenario` | 300KB |
| `template` | 2 | `template` | 1.8MB |
| `rich_menus` | 17 | `richmenu` | 207KB |
| `tags` | 0 | `tag` | 245KB |
| `events` | 18 | `remind` | 187KB |
| `event_times` | — | `remind` (datetime) | 213KB |
| `friend_information_setting` | 12 | `friend_info` | 627KB |
| `friend_info_option_selects` | — | `friend_info` type=選択肢 | 199KB |
| `action_info_friend_default` | — | `friend_info` system fields | — |
| `status_chat` | — | `compliant_status` | 801KB |
| `category` | (universal) | Folder cho tất cả | 509KB |

### 6.4 ER Diagram

```mermaid
erDiagram
    t_actions {
        int id PK
        int parent_id
        varchar type
        bigint update_timestamp
    }

    t_actions_detail {
        int id PK
        int action_id FK
        int bot_id
        varchar type
        text data
        varchar embed_regex_text
        tinyint has_filters
        bigint update_timestamp
    }

    filters_v2 {
        int id PK
        int bot_id
        varchar parent_type
        int parent_id FK
        varchar operator
        varchar type
        text data
        text text_preview
    }

    scenario { int id PK; int bot_id; varchar name; int group_id FK }
    template { int id PK; int bot_id; varchar name; int category_id FK }
    rich_menus { int id PK; int bot_id; varchar name; int group_id FK; timestamp deleted_at }
    tags { int id PK; int bot_id; varchar name; int category_id FK; int action_id FK; timestamp deleted_at }
    events { int id PK; int bot_id; varchar event_name; int category_id FK }
    event_times { int id PK; int event_id FK; int bot_id; date event_date; varchar event_start_time }
    friend_information_setting { int id PK; int bot_id; varchar title; int group_id FK; int type_data }
    friend_info_option_selects { int id PK; int bot_id; int friend_info_id FK; varchar option_value }
    status_chat { int id PK; int bot_id; varchar name_status; tinyint is_save }
    category { int id PK; int bot_id; int kind; varchar name; int position }
    action_info_friend_default { int id PK; varchar id_info; int bot_id; varchar title; int type_data }

    t_actions ||--o{ t_actions_detail : "has many"
    t_actions_detail ||--o{ filters_v2 : "parent_type=modal_action"
    t_actions_detail }o--o| scenario : "data.id (scenario)"
    t_actions_detail }o--o| template : "data.id (template)"
    t_actions_detail }o--o| rich_menus : "data.id (richmenu)"
    t_actions_detail }o--o{ tags : "data.ids[] (tag)"
    t_actions_detail }o--o| events : "data.event_id (remind)"
    t_actions_detail }o--o| event_times : "data.id (remind)"
    t_actions_detail }o--o| friend_information_setting : "data.id (friend_info)"
    t_actions_detail }o--o| friend_info_option_selects : "data.action_content (friend_info+選択肢)"
    t_actions_detail }o--o| status_chat : "data.id (compliant_status)"
    scenario }o--o| category : "group_id kind=11"
    template }o--o| category : "category_id kind=2"
    rich_menus }o--o| category : "group_id kind=17"
    tags }o--o| category : "category_id kind=0"
    events }o--o| category : "category_id kind=18"
    friend_information_setting }o--o| category : "group_id kind=12"
    friend_info_option_selects }o--|| friend_information_setting : "friend_info_id"
```

---

## 7. Field Traceability Matrix

| # | UI Element | Action Type | DB Table.Column | Mapping Type | Confidence | Ghi chú |
|---|-----------|------------|----------------|-------------|-----------|---------|
| 1 | Select 配信設定 | scenario | `t_actions_detail.data.action` (1/2/3) | Enum | **Cao** | 1=停止, 2=開始/再開, 3=途中から |
| 2 | Combo-box ステップ選択 | scenario | `scenario.id`, `scenario.name` | FK + cache | **Cao** | data.id, data.scenario_name |
| 3 | Input 日目 | scenario | `t_actions_detail.data.start_day` | INT | **Cao** | Chỉ khi action=3 |
| 4 | Folder picker (scenario) | scenario | `category.id`, `category.name` (kind=11) | FK | **Cao** | |
| 5 | Radio/combo テンプレート | template | `template.id`, `template.name` | FK + cache | **Cao** | data.id, data.template_name |
| 6 | Folder picker (template) | template | `category.id` (kind=2) | FK | **Cao** | |
| 7 | Textarea テキスト | text | `t_actions_detail.data.content` | Text (max 5000) | **Cao** | Xử lý qua detectUrlInMessageTextV2 |
| 8 | Merge tag [LINE_NAME] | text | Inline trong content | Replace string | **Cao** | |
| 9 | Merge tag [FRIEND_INFO_{hash}] | text | `friend_information_setting.id` (Hashids) | Hash ID → FK | **Cao** | |
| 10 | Select 配信設定 | remind | `t_actions_detail.data.type` (1/0) | Enum | **Cao** | 1=配信開始, 0=配信停止 |
| 11 | Combo-box リマインド選択 | remind | `events.id`, `events.event_name` | FK + cache | **Cao** | data.event_id, data.remind_name |
| 12 | Date picker | remind | `event_times.event_date` | Date YYYY-MM-DD | **Cao** | |
| 13 | Time picker | remind | `event_times.event_start_time` | Time HH:MM | **Cao** | |
| 14 | Checkbox list タグ | tag | `tags.id`, `tags.name` | FK many-to-many | **Cao** | data.ids = array |
| 15 | Select タグ操作 | tag | `t_actions_detail.data.action` (1/2) | Enum | **Cao** | 1=つける, 2=はずす |
| 16 | Button タグ新規追加 | tag | `tags` INSERT | Create | **Cao** | EP-10 |
| 17 | Select 表示設定 | richmenu | `t_actions_detail.data.action` (1/2) | Enum | **Cao** | 1=表示停止, 2=表示する |
| 18 | Combo-box リッチメニュー選択 | richmenu | `rich_menus.id`, `rich_menus.name` | FK + cache | **Cao** | |
| 19 | Radio ブックマーク | bookmark | `t_actions_detail.data.action` (1/2) | Enum | **Cao** | 1=する, 2=外す |
| 20 | Combo-box 友だち情報 field | friend_info | `friend_information_setting.id`, `.title` | FK + cache | **Cao** | ID âm = system fields |
| 21 | Select action (type=1) | friend_info | `t_actions_detail.data.action` | Enum | **Cao** | 1=削除, 2=登録 |
| 22 | Radio option (type=1, action=2) | friend_info | `friend_info_option_selects.id` → data.action_content | FK | **Cao** | |
| 23 | Textarea (type=2, action=2) | friend_info | `t_actions_detail.data.content` | Text | **Cao** | |
| 24 | Date picker (type=3, action=2) | friend_info | `t_actions_detail.data.content` | Date | **Cao** | |
| 25 | Radio ランダム/指定 (type=6) | friend_info | `t_actions_detail.data.is_random` (0/1) | Bool | **Cao** | |
| 26 | Input ポイント 指定 | friend_info | `t_actions_detail.data.content` | INT | **Cao** | |
| 27 | Input from/to ランダム | friend_info | `t_actions_detail.data.from`, `.to` | INT | **Cao** | |
| 28 | Select 対応ステータス設定 | compliant_status | `t_actions_detail.data.action` (1/2) | Enum | **Cao** | |
| 29 | Select ステータス | compliant_status | `status_chat.id`, `.name_status` | FK + cache | **Cao** | data.id, data.content |
| 30 | Radio ブロック action | block | `t_actions_detail.data.action` (1/2/3/4) | Enum | **Cao** | 1=ブロック, 2=解除, 3=表示, 4=非表示 |
| 31 | Button 「絞込」 | Tất cả | `filters_v2` WHERE parent_type='modal_action' | 1-nhiều | **Cao** | |
| 32 | Badge 「設定済」 | Tất cả | `t_actions_detail.has_filters` | Bool | **Cao** | |
| 33 | Select フォーム | form_answer | `form_answer.id`, `.name` | FK | **Cao** | action-only |
| 34 | Select 予約 | booking | `b_event_detail.id`, `.title` | FK | **Cao** | action-only |
| 35 | Select 商品 | product_page | product table.id | FK | **Trung bình** | Tên bảng chưa xác nhận |
| 36 | Select コンバージョン | conversion | conversion table.id | FK | **Trung bình** | Tên bảng chưa xác nhận |
| 37 | Select キーワード | keywords | keyword table.id | FK | **Trung bình** | Tên bảng chưa xác nhận |

---

## 8. API Endpoints

Tất cả endpoints thuộc route group `prefix: 'ajax'`, middleware `check_login` + `check_remember_token`. CSRF qua header `X-CSRF-TOKEN`.

| EP | Method | URL | Mục đích | Controller | Confidence |
|----|--------|-----|---------|-----------|-----------|
| EP-01 | POST | `/ajax/action/init-data` | Load toàn bộ data khi modal mở | `Basic\ActionController@initDataAction` | **Cao** |
| EP-02 | POST | `/ajax/action/save` | Lưu action config (create/update) | `Basic\ActionController@saveAction` | **Cao** |
| EP-03 | POST | `/ajax/action/delete-action-button` | Xóa hoàn toàn 1 action (gồm details + filters) | `Basic\ActionController@deleteActionButton` | **Cao** |
| EP-04 | POST | `/ajax/get-data-for-step-action` | Load scenarios theo folder | `Basic\ActionController@ajaxGetDataForStepAction` | **Cao** |
| EP-05 | POST | `/ajax/get-data-for-template-action` | Load templates theo folder | `Basic\ActionController@ajaxGetDateForTemplateAction` | **Cao** |
| EP-06 | POST | `/ajax/get-data-for-rich-menu-action` | Load rich menus theo folder | `Basic\ActionController@ajaxGetDataForRichMenuAction` | **Cao** |
| EP-07 | POST | `/ajax/get-list-remind` | Load remind events theo folder | `Basic\ActionController@ajaxGetReminds` | **Cao** |
| EP-08 | POST | `/ajax/get-list-friend-info` | Load friend info fields theo folder | `Basic\ActionController@ajaxGetFriendInfo` | **Cao** |
| EP-09 | POST | `/ajax/get-list-group-friend-info` | Load friend info categories | `Basic\ActionController@ajaxGetCategoriesByFriendInfo` | **Cao** |
| EP-10 | POST | `/ajax/save-add-tag-in-modal-action` | Tạo tag mới inline | `Basic\ActionController@saveAddTag` | **Cao** |
| EP-11 | POST | `/ajax/get-list-group-tag` | Load tags theo folder | `Basic\TagController@ajaxGetListCategoryTag` | **Cao** |
| EP-12 | POST | `/ajax/init-status-chat` | Load compliant statuses | `ChatController@ajaxGetStatusChat` | **Cao** |
| EP-13 | GET | `/ajax/initDataFilterBroadcast` | Load filter data cho action | Controller chưa xác nhận | **Trung bình** |
| EP-14 | POST | `/ajax/get-bot-data` | Kiểm tra plan type (filter eligibility) | Chưa xác nhận | **Trung bình** |

Chi tiết request/response format: xem `web/api-spec.md`.

---

## 9. Business Rules

### 9.1 Giới hạn action

| Giới hạn | Giá trị | Confidence |
|---------|---------|-----------|
| Max ký tự text action | 5,000 ký tự | **Cao** |
| Max ký tự tên tag inline | 50 ký tự | **Cao** |
| Max số actions per config | Không giới hạn rõ ràng (không tìm thấy constant) | **Thấp** |
| Số lần xuất hiện `scenario` | Tối đa 1 (type_ignore) | **Cao** |
| Số lần xuất hiện `richmenu` | Tối đa 1 (type_ignore) | **Cao** |
| Số lần xuất hiện `remind` | Tối đa 1 (type_ignore) | **Cao** |
| `action_only` và `actions[]` | Loại trừ nhau | **Cao** |

### 9.2 Filter eligibility

- `plan_type != 1` → filter button bị disabled (cần upgrade plan)
- Kiểm tra qua EP-14 `/ajax/get-bot-data` khi Vue `created()`
- Khi filter có data: `t_actions_detail.has_filters = 1` → badge 「絞込 設定済」 hiển thị

### 9.3 Context mode exclusions

- `step_message` → ẩn ステップ, テンプレート, テキスト (chỉ còn タグ, リッチメニュー, ブックマーク, 友だち情報, 対応ステータス, ブロック, リマインド)
- `broadcast_v2` → ẩn テンプレート, テキスト
- `richmenu` → ẩn リッチメニュー (không cho phép nested richmenu action)
- `bookmark` → ẩn ブックマーク (không cho phép nested bookmark action)
- Booking calendar contexts (20+ types) → ẩn リマインド

### 9.4 Point type — UI↔DB conversion (quan trọng)

Đây là conversion không tường minh giữa UI và DB cho `friend_info` type=6 (ポイント):

| UI `action` | DB `action` | DB `action_content` | Mô tả |
|------------|------------|-------------------|-------|
| 0 | 1 | NULL | 情報を削除 |
| 1 | 2 | 1 | ポイント登録（上書き） |
| 2 | 2 | 2 | ポイントをプラス（＋） |
| 3 | 2 | 3 | ポイントをマイナス（－） |

**Khi load từ DB:** `db.action=1` → `ui.action=0`; `db.action=2` → `ui.action=db.action_content`. **Độ tin cậy:** **Cao**

### 9.5 System friend info — ID âm

Các system default friend info fields dùng ID âm trong `t_actions_detail.data.id`:

| ID âm | Field | Bảng nguồn |
|-------|-------|-----------|
| -1 | system_name (システム表示名) | `action_info_friend_default` (id_info='d_1') |
| -2 | phone (携帯電話) | `action_info_friend_default` (id_info='d_2') |
| -3 | email (メールアドレス) | `action_info_friend_default` (id_info='d_3') |
| -4 | birthday (生年月日) | `action_info_friend_default` (id_info='d_4') |
| -6 | 都道府県 | `action_info_friend_default` (id_info='d_6') |

Custom fields dùng ID dương từ `friend_information_setting.id`. **Độ tin cậy:** **Cao**

### 9.6 URL detection trong text action

Khi save action type=`text`, `content` được xử lý qua `detectUrlInMessageTextV2($data['content'], $bot)`:
- Detect URLs trong nội dung text
- Tạo tracking links
- Có thể ghi regex vào `t_actions_detail.embed_regex_text`

**Độ tin cậy:** **Trung bình** (xác nhận từ code call, chưa đọc implementation của hàm helper)

### 9.7 Remind — tạo EventTimes record

Khi save action type=`remind` với `type=1` (配信開始):
1. Tìm `event_times` khớp với `event_id + event_date + event_start_time`
2. Nếu chưa có → INSERT `event_times` mới
3. Sau đó gọi `createEventStepTime($event_id, $event_time_id)`
4. `data.id = event_times.id` (lưu vào JSON)

**Độ tin cậy:** **Cao**

### 9.8 Xóa action — cascade

Khi xóa hoàn toàn action (EP-03):
1. `FilterV2::deleteActionFilterByAction($actionId)` — xóa tất cả filters
2. `ActionDetail::where('action_id', $actionId)->delete()` — xóa details
3. `Actions::where('id', $actionId)->delete()` — xóa parent

Khi save với empty action_detail (context=`conversion_list`):
- Dispatch `DeleteActionInSourceMessage` job (Spring Boot async)

### 9.9 Broadcast edit timeout

Khi save action liên quan đến broadcast đã scheduled trong vòng 5 phút:
- Response: `{ success: false, message: "配信予定日時5分前からは配信内容の編集はできません。" }`

**Độ tin cậy:** **Cao**

---

## 10. Integration Guide

### 10.1 Embed component vào tính năng mới

**Bước 1 — Include Blade partials:**
```php
// Trong view của tính năng
@include('layout.modal_setting.modal_select_action')
// Hoặc V3 (pro edit):
@include('layout.modal_setting.modal_select_action_pro')
```

**Bước 2 — Pass required variables từ controller:**

Controller cần chuẩn bị và pass vào view:
```php
// Dữ liệu cần thiết để modal hoạt động
$scenario       // Collection scenarios
$templates      // Collection templates + groups
$richMenus      // Collection rich menus
$tags           // Collection tags + groups
$friendInfos    // Collection friend info fields
$statusSettings // Collection status_chat
// Optional (tùy context):
$listRemind     // Collection remind events (V3)
```

**Bước 3 — Truyền context qua hidden inputs (trước khi mở modal):**
```javascript
// Trước khi trigger modal mở, set các hidden inputs:
$('#action_idx').val(index);
$('#plan_key').val(planKey);
$('#button_tab_id').val(tabId);
// v.v. tùy type_action
```

**Bước 4 — Khởi tạo Vue component:**
```javascript
// Set type_action trước khi mở modal
setting_action.type_action = 'reply'; // hoặc type tương ứng
setting_action.action_id = existingActionId || '';

// Trigger modal open (Vue sẽ tự gọi EP-01)
$('#settingActionUrlModal').modal('show');
```

**Bước 5 — Handle save callback:**

Sau khi save thành công, `setting_action` emit event với `action_id`. Tính năng cha cần:
```javascript
// Lắng nghe event hoặc handle qua saveSettingAction() completion
// action_id mới được trả về → lưu vào state của tính năng cha
parentFeature.action_id = response.action_id;
```

**Bước 6 — Xử lý delete (khi cần):**

Nếu tính năng cần xóa toàn bộ action:
```javascript
// POST /ajax/action/delete-action-button (EP-03)
$.post('/ajax/action/delete-action-button', { action_id: id });
```

### 10.2 Chọn variant phù hợp

| Tình huống | Variant | File |
|-----------|---------|------|
| Tạo/cấu hình action mới từ đầu | **V2** | `modal_select_action.blade.php` |
| Chỉnh sửa action đã tồn tại | **V3** | `modal_select_action_pro.blade.php` |
| Bulk action từ Friend List | **V1** | `modal_setting_action.blade.php` |

### 10.3 Bảng tham chiếu bảng cha

Sau khi save, tính năng cha lưu `t_actions.id` vào FK của mình:

| Tính năng | Bảng | Cột FK |
|-----------|------|-------|
| Auto Reply | `auto_reply` | `action_id` |
| Form Answer | `form_answers` | `action_reply_id`, `action_open_id` |
| Lesson Calendar | `calendar_courses` | `action_id_send_after_booking`, `action_id_send_approve_booking` |
| Salon Booking | `calendar_salon_courses` | `action_id_send_after_booking`, `action_id_send_approve_booking` |
| Salon Staff | `calendar_salon_staffs` | `action_id_send_after_booking`, `action_id_send_approve_booking` |
| Template Button | `buttons` | `action_id` |
| Tag (preview action) | `tags` | `action_id` |
| Action Schedule | `action_schedules` | `action_id` |

---

## 11. Cross-References

### 11.1 Shared components phụ thuộc

| Component | Mã | Quan hệ |
|-----------|-----|---------|
| Friend Filter | SC-003 | SC-004 gọi SC-003 khi user click 「絞込」 per action. Filter data lưu trong `filters_v2` với `parent_type='modal_action'`. |

### 11.2 Tính năng sử dụng SC-004

SC-004 được tham chiếu bởi các tính năng Admin thông qua FK trong bảng cha:

**Đã xác nhận (từ DB cross-feature usage):**
- FA-001: Chat 1:1 (chat 1 on 1)
- FA-003: Auto Reply (`auto_reply.action_id`)
- FA-004: Broadcast/Step Message
- FA-009: Scenario — step delivery
- FA-010: Rich Menu (`rich_menu_items` action config)
- FA-012: URL Tracking (`url_redirect` context)
- FA-013: Form Answer (`form_answers.action_reply_id`, `form_answers.action_open_id`)
- FA-014: Bookmark
- FA-015: Action Schedule (`action_schedules.action_id`)
- FA-016: Lesson Calendar (`calendar_courses.action_id_*`)
- FA-017: Salon Booking (`calendar_salon_courses.action_id_*`, `calendar_salon_staffs.action_id_*`)

---

## 12. Gaps và Unknowns

Tổng hợp từ validation-report — các vấn đề còn tồn đọng:

### Trung bình (cần điều tra trước khi implement)

| # | Vấn đề | Cách giải quyết |
|---|--------|----------------|
| M-01 | 3 action-only types chưa xác nhận tên bảng DB: `product_page` (s_items?), `conversion` (conversions?), `keywords` (auto_reply_keywords?) | Tra `db/index.md` với từ khóa `s_items`, `products`, `conversions`, `keywords` |

### Nhẹ (ghi nhận, ít ảnh hưởng)

| # | Vấn đề | Ghi chú |
|---|--------|---------|
| L-01 | EP-01 và EP-02 cùng có `Route name: action.save` — có thể lỗi ghi chép | Kiểm tra lại routes file; EP-01 có thể là `action.initData` |
| L-02 | EP-14 `get-bot-data` không được giải thích trong Logic Spec | Logic plan check (plan_type != 1 → filter disabled) chưa fully documented |
| L-03 | `ajaxGetRichMenu` method trong routes có thể không tồn tại trong controller | Xác minh method name — có thể là `ajaxGetDataForRichMenuAction` |
| L-04 | Sample data `remind` type trong DB chỉ có `id` và `remind_name` — thiếu `event_id`, `event_date`, `event_start_time` | Có thể do record cũ không đầy đủ. Format mới đã documented. |
| L-05 | `bill_item_v2` context mode không được liệt kê trong Logic Spec bảng sidebar buttons ẩn | Không ẩn sidebar button — chỉ hiện thêm merge tag 商品決済 |
| L-06 | `bot_line_user` fields khi execute richmenu/block action chưa documented | Cần `/spec-job` để phân tích Spring Boot jobs |
| L-07 | `t_actions.parent_id` — luôn = 0 hay có ngoại lệ? | DB Mapping ghi nhận "thường = 0" nhưng chưa xác nhận tuyệt đối |

### Ngoài scope (cần `/spec-job`)

- **Execution logic:** Cách Spring Boot jobs thực thi các actions khi có trigger event (gửi tin nhắn theo scenario, apply tag, update friend_info, v.v.)
- **`DeleteActionInSourceMessage` Job:** Background job được dispatch khi xóa action empty — chưa phân tích
- **`createEventStepTime` helper:** Logic tạo/merge EventTimes record cho remind action — chưa rõ hoàn toàn

---

## 13. Chất lượng Spec

### Metrics

| Hạng mục | Số lượng | Confirmed | Coverage |
|---------|---------|---------|---------|
| Main action types | 10 | 10/10 | 100% |
| Action-only types | 9 | 6/9 (3 tên bảng chưa xác nhận) | 67% |
| API endpoints | 14 | 12/14 Cao, 2/14 Trung bình | 86% Cao |
| DB tables documented | 12 | 12/12 | 100% |
| JSON formats (sample data) | 10 main + 9 action-only | 10/10 main confirmed | 100% main |
| Context modes | 15+ | 15/15 | 100% |
| UI↔DB field mapping | 37 rows | 34/37 Cao, 3/37 Trung bình | 92% Cao |

### Nguồn và độ tin cậy

| Nguồn | Loại thông tin | Độ tin cậy |
|-------|--------------|-----------|
| Laravel source code (`ActionController.php`, `ActionDataModalService.php`, Blade templates) | Controllers, DB models, UI structure | **Cao** |
| `select_action.js` | Frontend logic, validation, context modes | **Cao** |
| DB schema (`t_actions`, `t_actions_detail`, lookup tables) | Schema chính xác | **Cao** |
| DB sample data | JSON format thực tế trong production | **Cao** |
| `config/sns-line.php` | `category.kind` values | **Cao** |
| JS call traces (EP-13, EP-14) | Endpoint discovery | **Trung bình** |
| UI observation + suy luận | 3 action-only table names | **Trung bình** |

---

_Spec này được tổng hợp bởi spec-compiler agent. Ngày: 2025-05-20._  
_Input: `ui/ui-spec.md`, `web/api-spec.md`, `web/logic-spec.md`, `db/db-mapping.md`, `_internal/validation-report.md`_  
_Xem chi tiết: các file spec riêng trong thư mục `features/shared/action-settings/`_
