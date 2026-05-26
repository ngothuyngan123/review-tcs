# FA-013 Danh sách bạn bè「友だちリスト」 — Logic Spec

> **Feature ID:** FA-013
> **Portal:** Admin
> **Controller chính:** `Basic\FriendlistController`
> **File:** `app/Http/Controllers/Basic/FriendlistController.php` (4329 dòng)
> **Ngày tạo:** 2026-03-25

---

## 1. Controllers & Actions

### FriendlistController
**File:** `app/Http/Controllers/Basic/FriendlistController.php`
**Namespace:** `App\Http\Controllers\Basic`

#### Constructor — Dependency Injection
```
TagRepositoryInterface          → $tagRepository
ScenarioRepositoryInterface     → $scenarioRepository
ConversionRepositoryInterface   → $conversionRepository
CategoryRepositoryInterface     → $categoryRepository
TemplateRepositoryInterface     → $templateRepository
FriendListRepositoryInterface   → $friendListRepository
BotRepositoryInterface          → $botRepository
LineUserRepositoryInterface     → $lineUserRepository
BotLineUserService              → $botLineUserService
HelperService                   → $helperService
MessageV2RepositoryInterface    → $messageV2Repository
ConversationRepositoryInterface → $conversationRepository
```
Thêm 2 property được khởi tạo trực tiếp:
- `$line_user_model = new LineUser()`
- `$category = new Category()`

**Tin cậy:** Cao — :109-138

---

#### 1.1 `index()` — Hiển thị trang chính (:181-245)

**Logic:**
1. Lấy `bot_id` từ session (`getBotId()`)
2. Đếm tổng bạn bè: `BotLineUser::where('bot_id', $bot_id)->where('is_blocked', 0)->count()`
3. Nếu có `tags_search` (CSV) → tách thành array, tìm tags qua `tagRepository->findById()`
4. Nếu có `scenario_search` → tìm scenarios qua `scenarioRepository->findById()`
5. Nếu có `conversion_search` → tìm conversions qua `conversionRepository->findById()`
6. Lọc bỏ params rỗng
7. Lấy danh sách rich menus đang active (`status_rich = 1`)
8. Lấy danh sách conversions, status chats
9. Return view `basic.friendlist.index` với tất cả dữ liệu

**Ghi chú:** View sẽ dùng Vue.js để load danh sách bạn bè qua AJAX (gọi EP-02 hoặc EP-03).

---

#### 1.2 `searchLineUser()` — Tìm kiếm theo keyword (:257-346)

**Logic:**
1. Join `bot_line_user` + `line_user` theo `line_user_id`
2. Lọc: `line_user.name LIKE '%keyword%'`, `is_blocked = 0`, `bot_id = current`
3. Phân trang thủ công: `offset = (page - 1) * 50`, `limit = 50`
4. Với mỗi user, lấy thêm:
   - Số scenario đang follow: `COUNT(scenario_lineuser) WHERE is_following = 1`
   - Tin nhắn mới nhất: `Conversation::frist()` rồi `Messages::orderBy('created_at', 'desc')->first()`
5. Return view Blade (partial) `basic.friendlist.result_search`

**Lưu ý:** Code có typo `frist()` thay vì `first()` — có thể là custom method hoặc bug. Dòng :280, :315.

---

#### 1.3 `sort()` — Sắp xếp danh sách (:348-557)

**Logic:**
- `value = 1` → `ORDER BY followed_at ASC` (ngày thêm tăng dần)
- `value = 2` → `ORDER BY followed_at DESC` (ngày thêm giảm dần)
- `value = 3` → Sắp xếp theo `created_at` (tin nhắn mới nhất) giảm dần, dùng `array_multisort()`
- Hỗ trợ keyword kết hợp
- Gọi stored procedure `SelectLastMessageByLineId(user_id, bot_id)` để lấy tin nhắn mới nhất
- Return JSON `{"bot_line_user": [...]}`

---

#### 1.4 `postFilterAdvance()` — Lọc nâng cao v2 (:2918-3071)

**Logic chính:**
1. Parse `item_search` (AND conditions) và `item_search_or` (OR conditions) từ JSON
2. Xử lý status_search, followed_to/followed_from → thêm vào itemsSearch
3. Kiểm tra `line_user_id_deleted` → gọi `checkFriendDeleted()` helper
4. Gọi `Conversation::advanceFilterPost()` — query builder phức tạp (xem mục Models)
5. Thêm các filter bổ sung:
   - `scenario_stop_id` → `whereRaw` subquery `scenario_lineuser.is_following = 2`
   - `scenario_unfinish_id` → `whereRaw` subquery `scenario_lineuser.is_following = 0`
   - `scenario_id_running` → `whereIn` line_user_ids từ `scenario_lineuser.is_following = 1`
   - `rich_menu_id` → `where bot_line_user.rich_menu_id`
6. Sắp xếp theo `followed_at` hoặc `last_time_message` nếu có
7. Select: `bot_line_id`, `followed_at`, `line_id`, `is_blocked`, `link_my_page`
8. `paginate(200)`
9. Bổ sung cho mỗi item: `name`, `email`, `view_name`, `avatar_url` (từ `LineUser`), `conver_id`, `new_msg`, `msg_created_at` (từ `Conversation`), `scenario_name` (từ `ScenarioLineuser`)
10. Return JSON `{"success": true, "data": paginated_data}`

**Ghi chú hiệu năng:** Bước 9 query N+1 — mỗi item trong page (tối đa 200) gọi 3 query riêng (LineUser, Conversation, ScenarioLineuser).

---

#### 1.5 `filterAdvance()` — Lọc nâng cao v1 (:2829-2917)

**Logic:** Tương tự 1.4 nhưng dùng `Conversation::advanceFilter()` (phiên bản cũ). Truyền params trực tiếp thay vì JSON.

---

#### 1.6 `mypage()` — Chi tiết bạn bè (:1609-1730)

**Logic (GET request):**
1. Lấy `line_id` từ route parameter
2. Tìm conversation: `Conversation::getConversation()` → nếu null → redirect 404
3. Kiểm tra `BotLineUser::getBotLineUserWithCondition()` → nếu null → redirect chat-v3
4. Đồng bộ thông tin từ LINE server qua `BotController::getInfoFromLine()`:
   - Cập nhật `line_user.name`, `avatar_url`, `status_message`
   - Nếu tên thay đổi → ghi `SyncElasticsearch`
5. Tính `special_status` (trạng thái xác nhận tin nhắn):
   - 0 = chưa xác nhận
   - 1 = đã xác nhận (tin nhắn cuối confirmed)
   - 2+ = trạng thái đặc biệt (custom)
6. Lấy `line_users` qua `LineUser::getLineUserMyPage()`
7. Lấy tags theo category (`getTags()`)
8. Return view `basic.friendlist.mypage_v2`

**Logic (AJAX request):**
- `action = 'list_message'` → `Messages::getListMessageConversation()` → JSON
- Khác → Lấy `ScenarioLineuser::getListScenarioLineUser()` → JSON

---

#### 1.7 `updateLineInfo()` — Cập nhật thông tin (:1732-1773)

**Validation rules:**
| Field | Rule | Message lỗi (JP) |
|-------|------|------------------|
| `line_id` | `nullable\|int` | — |
| `view_name` | `nullable\|max:20` | 「システム表示名を20文字以下で入力してください」 |
| `real_name` | `nullable\|max:20` | 「本名を20文字以下で入力してください」 |
| `email` | `nullable\|email` | — |
| `phone_number` | `nullable\|regex:/(^\+?[0-9]{9,15}$)/u` | 「9-15数字以内」 |

**Logic:**
1. Validate → return lỗi nếu fail
2. Chuyển đổi phone: `preg_replace("/^0/i", "+81", $phone_number)`
3. Update `line_user` table
4. Update `bot_line_user.phone_number`

---

#### 1.8 `updateLineUsersBlock()` — Block bạn bè (:1964-1991+)

**Logic:**
1. Nhận `conversationIds` (JSON array)
2. Với mỗi conversation chưa block (`is_blocked == 0`):
   - `BotLineUser.is_blocked = 1`
   - `Conversation.is_blocked = 1`, `blocked_by = 1`, `blocked_at = now()`
   - Dừng tất cả scenario: `ScenarioLineuser.is_following = 0`
   - Xoá `scenario_step_time` chưa gửi (`status = 0`)
3. Cập nhật `bots.count_user_unconfirm`
4. Gọi `updateBadge()`

---

#### 1.9 `unblockFriend()` — Bỏ block (:3170-3217)

**Logic:**
1. Với mỗi `lineUserId` trong `listLineId`:
   - Gọi LINE API `getProfile()` kiểm tra user còn follow không
   - **Nếu còn follow:** `is_blocked = 0`, tạo message unblock trong `messages_v2s`
   - **Nếu không còn follow:** giữ `is_blocked = 1` (user đã block phía LINE)
2. Cập nhật `bots.count_user_unconfirm`, gọi `updateBadge()`

**Business rule quan trọng:** Bỏ block chỉ thành công nếu user vẫn follow LINE OA. Nếu user đã block từ phía LINE, bỏ block admin-side không có tác dụng.

---

#### 1.10 `deleteUserBlock()` — Xoá bạn bè (:3219-3617)

**Logic cascade delete (chi tiết):**

| Bước | Bảng | Hành động |
|------|------|-----------|
| 1 | `bot_friend_statistic` | Giảm `count_user_followed` cho ngày followed_at. Nếu user bị user-block → giảm `count_user_unfollowed` |
| 2 | Rich menu | Gọi LINE API `DELETE .../richmenu` để unlink. Cập nhật `bot_line_user.rich_menu_id = null` |
| 3 | `bot_line_user_item` | Xoá items |
| 4 | `order_history`, `cycle_order_history` | Xoá lịch sử mua hàng |
| 5 | `mobile_notify` | Xoá notification, cập nhật `bots.count_app_notify` |
| 6 | `status_chat` | Giảm `count` nếu conversation có `id_status` |
| 7 | `auto_reply_history` | Xoá lịch sử auto reply |
| 8 | `user_button` | Xoá button interactions |
| 9 | `scenario_lineuser` | Giảm `scenario.count_follow/count_stop/count_unfinish` tuỳ `is_following`, rồi xoá |
| 10 | `sync_elasticsearch` | Ghi log delete |
| 11 | `bot_line_user` | Xoá record chính |
| 12 | `conversation` | Xoá conversation |
| 13 | `scenario_lineuser`, `scenario_step_time` | Xoá scheduling |
| 14 | `tag_line_user` | Giảm `tags.count_user_tag`, rồi xoá |
| 15 | `form_answer_result`, `user_open_formanswer`, `form_answer_user_accept` | Xoá form answers, giảm `form_answer.count_user_reply` |
| 16 | `event_step_time` | Xoá event step times liên quan form |
| 17 | `b_booking` | Xoá event bookings, cập nhật `b_plan_slot.remain_limit` và `b_slot.use_people` |
| 18 | `calendar_salon_line_booking` | Xoá salon bookings, xoá event_step_time liên quan |
| 19 | `calendar_course_booking` | Xoá lesson bookings, recalculate `countTotalBookingStatus()` |
| 20 | `event_step_time` | Xoá remaining event step times |
| 21 | `user_event` | Xoá user remind events |
| 22 | `friend_information_value` | Giảm `friend_information_setting.total_user_has_value`, rồi xoá |
| 23 | `bc_user_booking` | Xoá calendar bookings, gọi `gCalendarController::deleteEventByBooking()` |
| 24 | `url_shorten`, `url_shorten_detail`, `detail_url_click` | Xoá URL tracking data |
| 25 | `detail_landing_click` | Xoá landing click data, cập nhật `landing_history` và `landing` counters |
| 26 | `collect_open_landing` | Xoá landing scan data, cập nhật `landing_history.count_click*` |
| 27 | `time_action_landing` | Xoá landing action times |
| 28 | `conversion_result` | Xoá conversion results |
| 29 | `step_message_history` | Xoá step message history |
| 30 | `bots.count_user_unconfirm` | Cập nhật counter |

**Ghi chú:** Đây là hàm phức tạp nhất (gần 400 dòng). Xoá dữ liệu cascade từ ~20+ bảng.

---

#### 1.11 `deleteUserBlockAction()` — Xoá hàng loạt (:3618-4227)

**Logic:** Tương tự `deleteUserBlock()` nhưng lặp qua `line_user_id_list`. Mỗi user thực hiện cascade delete đầy đủ.

---

#### 1.12 `unHiddenFriend()` — Hiện lại bạn bè ẩn (:4228-4275)

**Logic:**
- `type = 1` → Hàng loạt: parse `listLineId` JSON array, update `conversation.is_hide = 0`
- `type != 1` → Đơn lẻ: update cho 1 line_id
- Sync Elasticsearch với type `is_hide`

---

#### 1.13 `sendActionFriend()` — Bulk action (:863-1286)

**Logic:**
1. Nếu có `searchIDs` và không phải `allUser`:
   - Lặp qua IDs → `HelperService::sendAction(actionId, lineUserId, botId, null, 'friendList')`
2. Nếu `allUser`:
   - Tìm tất cả users theo filter (dùng `Conversation::advanceFilter` hoặc `advanceFilterPost`)
   - Nếu tổng > 200 → **Tạo `ActionSchedule`** (background processing):
     - Tên: 「【自動生成】友だち一括アクション」
     - `next_running_day`: now + 2 giây
     - `end_date_type`: 'times', `number_of_repetitions`: 1
     - Tạo `FilterV2` records cho filter conditions
     - Cập nhật `action_schedules.filter_ids`
   - Nếu tổng <= 200 → gọi `sendAction()` trực tiếp

**Background job ghi chú:** Khi > 200 users, hệ thống tạo `ActionSchedule` → Spring Boot job xử lý. Message hiển thị cho user: 「対象の友だち数が200人以上の場合、処理に時間がかかる場合があります。」

---

#### 1.14 `saveTag()` — Gán tag (:1287-1351)

**Logic:**
- `tagLineUser::updateOrCreate()` — upsert record `tag_line_user`
- Gọi `addTags()` helper function (có thể trigger scenario gắn liền tag)
- Hỗ trợ cả selected users và all users (qua filter)

---

#### 1.15 `removeTag()` — Gỡ tag (:1501-1569)

**Logic:**
- Tìm `tag_line_user` records → giảm `tags.count_user_tag` → xoá records
- Hard delete (không soft delete)

---

#### 1.16 `saveRichMenu()` — Gán rich menu (:1353-1483)

**Logic:**
- Nếu `rich_menu_id != 0`: Gọi LINE API `POST .../richmenu/{richId}` để link
- Nếu `rich_menu_id == 0`:
  - Nếu có rich menu mặc định (status_rich=1, status_line=1): link rich menu mặc định
  - Nếu không: `DELETE .../richmenu` để unlink
- Update `bot_line_user.rich_menu_id`

---

#### 1.17 `ajaxGetListCategoryTemplate()` — Lấy templates (:1571-1607)

**Logic:**
- Lấy `categoryList` với `kind = 2` (template kind)
- Nếu `group_id = 0` → lấy category đầu tiên
- Lấy templates của category chọn
- Thêm category mặc định「未分類」(id=0)
- Return JSON

---

#### 1.18 `sendMessage()` — Gửi tin nhắn (:1952-1962)

**Logic:** Delegate cho `ChatHelper::getTemplatesTest()` — gửi tin nhắn từ template.

---

#### 1.19 `saveScenario()` — Lưu scenario mypage (:2466-2516)

**Logic:** Gọi `ChatHelper::changeScenario()` cho từng scenario trong request. Hỗ trợ thay đổi nhiều scenarios cùng lúc.

---

#### 1.20 `csvExport()` — Export CSV (:559-737)

**Logic:**
- Nếu `type_filter == 'old'`: dùng `Conversation::advanceFilter()`
- Nếu khác: dùng `Conversation::advanceFilterPost()`
- Lấy thêm tags, scenario name cho mỗi user
- Export qua `Maatwebsite\Excel` (`UserExport` class)
- Lưu file CSV tại `public/`, return JSON `{"file_name": "line_user_xxx.csv"}`

---

#### 1.21 `basicFilterFriend()` — Lọc cơ bản (:4302-4307)

**Logic:** Delegate hoàn toàn cho `BotLineUserService::getBasicAllFriend()`.

---

## 2. Models Eloquent

### 2.1 BotLineUser
**File:** `app/BotLineUser.php`
**Table:** `bot_line_user`
**Relationships:** `hasOne->LineUser`, `hasOne->Bots`

**Cách dùng trong controller:**
- Đếm tổng bạn bè: `WHERE bot_id = ? AND is_blocked = 0`
- Lọc bạn bè: join với `line_user`, `conversation`
- Block/unblock: update `is_blocked`
- Rich menu: update `rich_menu_id`

**Tin cậy:** Cao

---

### 2.2 LineUser
**File:** `app/LineUser.php`
**Table:** `line_user`

**Cách dùng:**
- Thông tin cơ bản: `name`, `email`, `view_name`, `real_name`, `phone_number`, `avatar_url`, `line_id`, `status_message`
- Update thông tin: `updateLineInfo()`
- Scope `LineInfo()` — join relationship
- Static `getLineUserMyPage()`, `getLineUserInfo()`

---

### 2.3 Conversation
**File:** `app/Conversation.php`
**Table:** `conversation`

**Static methods quan trọng:**

| Method | Mô tả |
|--------|-------|
| `advanceFilter()` | Filter v1 — nhận params trực tiếp (tags, scenarios, etc.) |
| `advanceFilterPost()` | Filter v2 — nhận `item_search` JSON với type-based filter system |
| `getListFriendBlock()` | Lấy bạn bè bị admin block (`blocked_by = 1`) |
| `getConversation()` | Tìm conversation theo condition |
| `getConversationRaw()` | Tương tự nhưng dùng selectRaw |

**Cột quan trọng:**
- `tb_line_user_id` — FK đến `line_user.id`
- `bot_id` — FK đến `bots.id`
- `is_blocked` — 0/1
- `blocked_by` — 0 = user block, 1 = admin block
- `blocked_at` — timestamp block
- `is_hide` — 0/1 (ẩn bạn bè)
- `datetime_hide` — timestamp ẩn
- `last_message` — nội dung tin nhắn cuối
- `last_time_message` — thời gian tin nhắn cuối
- `conversation_kind` — 0 = 1:1, 1 = group
- `line_id` — string (line_user.id dạng string)
- `id_status` — FK đến `status_chat.id`
- `status_last_message` — trạng thái xác nhận tin nhắn cuối

**Tin cậy:** Cao — đọc từ model :76-350 và :1698-1767

---

### 2.4 Conversation::advanceFilterPost() — Chi tiết logic (:227-350+)

**Mô tả:** Query builder phức tạp nhất của tính năng. Xây dựng query lọc bạn bè từ filter conditions AND/OR.

**Base query:**
- `BotLineUser::where('bot_id', $bot_id)->where('is_blocked', 0)`
- Nếu `useCross = true`: bỏ filter `is_blocked` (dùng cho cross analysis)
- Nếu `useDBReplicate = true`: dùng `BotLineUserReplicate` (read replica)

**Keyword search:** Tách keyword theo space, search OR trên: `line_user.name`, `line_user.email`, `line_user.view_name`

**Filter types (AND/OR):**

| Type | Logic |
|------|-------|
| `status_search` | Subquery `conversation` WHERE `status_last_message IN` hoặc `id_status IN` |
| `day_add_friend` | `bot_line_user.followed_at` between dates. Hỗ trợ 2 mode: date range (`day_filter_type=0`) và duration days (`day_filter_type=1`) |
| `tag` | Subquery `tag_line_user` |
| `friend_name` | `line_user.name LIKE` hoặc `line_user.view_name LIKE` |
| `friend_info` | Subquery `friend_information_value` theo `friend_information_setting_id` |
| `scenario` | Subquery `scenario_lineuser` |
| `conversion` | Subquery `conversion_result` |
| `qr_code` / `qr_code_action` | Subquery `detail_landing_click` |
| `new_old_friend` | `bot_line_user.is_new_friend` |
| `affiliater` | Subquery `aff_result` |
| `richmenu` | `bot_line_user.rich_menu_id IN` |

**Tin cậy:** Cao — :227-350

---

### 2.5 ScenarioLineuser
**File:** `app/ScenarioLineuser.php`
**Table:** `scenario_lineuser`

**Cách dùng:**
- `is_following`: 0 = chưa hoàn thành, 1 = đang follow, 2 = đã dừng
- Dùng để hiển thị tên scenario đang chạy trên danh sách bạn bè
- Block bạn bè → set `is_following = 0`

---

### 2.6 Tags / tagLineUser
**Files:** `app/Tags.php`, `app/tagLineUser.php`
**Tables:** `tags`, `tag_line_user`

**Cách dùng:**
- `tag_line_user`: bảng pivot liên kết tag ↔ line_user
- `tags.count_user_tag`: counter cache — được cập nhật thủ công khi add/remove tag
- Gán tag: `updateOrCreate()` + gọi `addTags()` helper
- Gỡ tag: hard delete + giảm counter

---

### 2.7 FilterV2
**File:** `app/FilterV2.php`
**Table:** `filter_v2`

**Cách dùng:**
- Lưu filter conditions cho `ActionSchedule` khi bulk action > 200 users
- Columns: `bot_id`, `parent_type`, `parent_id`, `operator` (and/or), `type`, `data` (JSON), `text_preview`

---

### 2.8 ActionSchedule
**File:** `app/ActionSchedule.php`
**Table:** `action_schedules`

**Cách dùng (trong sendActionFriend):**
- Tạo scheduled action khi bulk action > 200 users
- `name`: 「【自動生成】友だち一括アクション」
- `action_id`: ID action cần thực hiện
- `filter_ids`: CSV IDs của FilterV2 records
- `next_running_day`: now + 2 giây → Spring Boot job sẽ pick up

---

### 2.9 Các model khác sử dụng

| Model | Table | Vai trò trong tính năng |
|-------|-------|------------------------|
| `Bots` | `bots` | Thông tin bot, `count_user_unconfirm`, `count_app_notify` |
| `RichMenus` | `rich_menus` | Rich menu definitions |
| `Scenario` | `scenario` | Step scenario definitions, counter caches |
| `ScenarioStepTime` | `scenario_step_time` | Scheduled step deliveries |
| `Conversion` | `conversion` | Conversion tracking |
| `StatusChat` | `status_chat` | Custom chat statuses, counter cache |
| `Messages` / `MessagesV2` | `messages` / `messages_v2s` | Tin nhắn, lịch sử |
| `Category` | `category` | Category cho tags, templates |
| `Template` | `template` | Message templates |
| `FriendInformationSetting` | `friend_information_setting` | Custom field definitions |
| `FriendInformationValue` | `friend_information_value` | Custom field values per user |
| `BotFriendStatistic` | `bot_friend_statistic` | Thống kê follow/unfollow theo ngày |
| `BotLineUserItem` | `bot_line_user_item` | Items của user |
| `SyncElasticsearch` | `sync_elasticsearch` | Queue sync ES |
| `FormAnswer` / `FormAnswerResult` | `form_answer` / `form_answer_result` | Form answers |
| `Landing` / `DetailLandingClick` | `landing` / `detail_landing_click` | QR/Landing page tracking |
| `MobileNotify` | `mobile_notify` | Mobile push notifications |

---

## 3. Services / Repositories

### 3.1 HelperService
**File:** `app/Services/HelperService.php`
**Inject:** `$helperService`

**Method dùng:**
- `sendAction($actionId, $lineUserId, $botId, $params, $source)` — Thực hiện action cho 1 user. Dùng trong bulk action.

**Tin cậy:** Trung bình — chưa đọc nội dung chi tiết của method.

---

### 3.2 BotLineUserService
**File:** `app/Services/BotLineUserService.php`
**Inject:** `$botLineUserService`

**Method dùng:**
- `getBasicAllFriend($params)` — Lọc bạn bè cơ bản (EP-33)

**Tin cậy:** Trung bình — chưa đọc nội dung.

---

### 3.3 Repository Interfaces

| Interface | Dùng cho |
|-----------|---------|
| `TagRepositoryInterface` | `findById()` — tìm tags |
| `ScenarioRepositoryInterface` | `findById()`, `findByBot()` — tìm scenarios |
| `ConversionRepositoryInterface` | `findById()` — tìm conversions |
| `CategoryRepositoryInterface` | `getListCategoryWithBotAndKind()` — lấy categories |
| `TemplateRepositoryInterface` | `getTemplateByBotAndCategory()` |
| `FriendListRepositoryInterface` | Không thấy sử dụng trực tiếp trong code đọc được |
| `BotRepositoryInterface` | `findById()` — tìm bot |
| `LineUserRepositoryInterface` | `findById()` — tìm line user |
| `MessageV2RepositoryInterface` | `create()` — tạo message (unblock) |
| `ConversationRepositoryInterface` | `getConversationByBotIdAndLineId()`, `updateConversation()` |

---

## 4. Form Requests / Validation

Không sử dụng Form Request class riêng. Validation inline trong controller:

### `updateLineInfo()` (:1739-1760)
```php
$rules = [
    'line_id'      => 'nullable|int',
    'view_name'    => 'nullable|max:20',
    'real_name'    => 'nullable|max:20',
    'email'        => 'nullable|email',
    'phone_number' => 'nullable|regex:/(^\+?[0-9]{9,15}$)/u'
];
```

**Tin cậy:** Cao

---

## 5. Events / Listeners / Queued Jobs

### 5.1 Không phát hiện Events / Listeners trực tiếp
Controller không dispatch bất kỳ Laravel Event nào.

### 5.2 SyncElasticsearch (queue-like)
**Bảng:** `sync_elasticsearch`

Ghi record để background process sync dữ liệu lên Elasticsearch:
- Type `update` — khi cập nhật tên user (mypage)
- Type `delete_line_user` — khi xoá user
- Type `is_hide` — khi ẩn/hiện user

**Tin cậy:** Cao — phát hiện nhiều nơi trong code

### 5.3 ActionSchedule (background job)
Khi bulk action > 200 users → tạo `action_schedules` record → **Spring Boot job** pick up và xử lý.

**Cần kiểm tra thêm ở `/spec-job`:**
- Job nào đọc `action_schedules`?
- Logic xử lý filter_ids từ `filter_v2`?
- Retry/error handling?

---

## 6. Authorization (Policies, Gates)

### 6.1 Middleware
Tất cả routes dùng middleware: `web`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`

**Không có middleware phân quyền riêng** (như `admin_access` hay `basic_access`) — tính năng nằm trong nhóm routes `basic`, truy cập bởi tất cả users có session hợp lệ (Admin + Staff).

### 6.2 Bot ID Scope
Mọi query đều lọc theo `bot_id = getBotId()` — helper function lấy bot_id từ session. Đảm bảo isolation giữa các LINE OA accounts.

### 6.3 Staff permissions
**Chưa phát hiện** kiểm tra quyền staff riêng trong controller. Cần kiểm tra middleware stack đầy đủ và Blade views để xác nhận.

**Tin cậy:** Trung bình — chỉ đọc controller, chưa kiểm tra route middleware group.

---

## 7. Business Rules (tổng hợp)

### BR-01: Block types
- `blocked_by = 0` → User block (LINE user tự block OA) — Admin chỉ có thể xoá, không unblock
- `blocked_by = 1` → Admin block — Admin có thể unblock hoặc xoá
- **File:** `Conversation.php:1714` (admin block), `:3108` (user block)

### BR-02: Unblock verification
Khi bỏ block (admin-side), hệ thống kiểm tra user có còn follow trên LINE không bằng cách gọi LINE API `getProfile()`. Nếu user đã block từ phía LINE → giữ trạng thái block.
- **File:** `FriendlistController.php:3181-3203`

### BR-03: Hide/Unhide
- Bạn bè bị ẩn: `conversation.is_hide = 1`, `datetime_hide` ghi thời gian ẩn
- Hiện lại: set `is_hide = 0`, `datetime_hide = null`
- Bạn bè ẩn không xuất hiện trong danh sách chính (filter `is_hide != 1` ở view hoặc query)
- **File:** `:3120-3169` (get hidden), `:4228-4275` (unhide)

### BR-04: Page size
- Danh sách chính (filter v2): **200 items/page** — `:3036`
- Danh sách user block: **50 items/page** — `:3110`
- Search result: **50 items/page** — `:266-267`
- Danh sách hidden: **không phân trang** (get all) — `:3161`
- Danh sách admin block: **không phân trang** (get all) — `:1748`

### BR-05: Bulk action threshold
- Nếu tổng users > 200 → tạo ActionSchedule cho background processing
- Nếu <= 200 → xử lý trực tiếp
- **File:** `:927`, `:963`

### BR-06: Cascade delete
Xoá bạn bè cascade ~20+ bảng liên quan. Xem mục 1.10 chi tiết.
- **File:** `:3219-3617`

### BR-07: Phone number format
Số điện thoại bắt đầu bằng `0` sẽ được chuyển sang `+81` (format Nhật Bản).
- **File:** `:1761`

### BR-08: Scenario khi block
Khi block bạn bè, tất cả scenario đang chạy (`is_following = 1`) bị dừng (`is_following = 0`) và scheduled step times bị xoá.
- **File:** `:1980-1981`

### BR-09: Filter v1 vs v2
- v1 (`filterAdvance`): Dùng `Conversation::advanceFilter()` với params trực tiếp
- v2 (`postFilterAdvance`): Dùng `Conversation::advanceFilterPost()` với JSON-based filter items, hỗ trợ linh hoạt hơn
- Frontend hiện tại chủ yếu dùng v2

### BR-10: LINE API Integration
- `getProfile()` — kiểm tra user còn follow không (unblock)
- `POST .../richmenu/{id}` — link rich menu cho user
- `DELETE .../richmenu` — unlink rich menu
- **File:** `:3181` (getProfile), `:1379-1394` (richmenu)

### BR-11: Elasticsearch sync
Mọi thay đổi quan trọng (update tên, delete user, hide/unhide) đều ghi `sync_elasticsearch` để background process đồng bộ.
- **File:** `:1662-1671`, `:3347-3353`, `:4242-4251`

### BR-12: Stored Procedure
Hàm `sort()` gọi stored procedure `SelectLastMessageByLineId(user_id, bot_id)` để lấy tin nhắn mới nhất hiệu quả hơn.
- **File:** `:376`, `:405`, `:431`, `:477`, `:507`, `:533`

---

## 8. Helper Functions (global)

Các helper functions được gọi trong controller (định nghĩa tại `app/Helpers/functions.php`):

| Function | Mô tả |
|----------|-------|
| `getBotId()` | Lấy bot_id từ session hiện tại |
| `addTags($tagIds, $lineUserId, $botId)` | Gán tags cho user (có thể trigger scenario) |
| `addLogUserAction($action)` | Ghi log hành động user |
| `totalUserConfirmMessage($botId)` | Đếm tổng users có tin nhắn chưa xác nhận |
| `updateBadge($bot)` | Cập nhật badge notification |
| `getInfoFromLine($bot, $lineId)` | Gọi LINE API lấy profile |
| `checkFriendDeleted($lineUserId, $botId)` | Kiểm tra bạn bè đã xoá chưa |
| `getTotalNotifyExceptSystemAndBillCycle($botId)` | Đếm notifications |
| `is_image($path)` | Kiểm tra file có phải ảnh |
| `sortRankItems()` | Callback sắp xếp templates theo rank |
| `logDebug($msg, $context)` | Log debug với context |

**Tin cậy:** Trung bình — chỉ biết tên và cách gọi, chưa đọc implementation.

---

## 9. Tóm tắt phát hiện cho các bước tiếp theo

### Cho db-mapper (bước 5):
Các bảng chính cần mapping: `bot_line_user`, `line_user`, `conversation`, `scenario_lineuser`, `scenario_step_time`, `tag_line_user`, `tags`, `scenario`, `bot_friend_statistic`, `status_chat`, `filter_v2`, `action_schedules`, `friend_information_setting`, `friend_information_value`, `sync_elasticsearch`, `rich_menus`, `bots`

### Cho job-analyzer (bước 4):
- `ActionSchedule` — khi bulk action > 200 users → Spring Boot job xử lý
- `SyncElasticsearch` — background sync ES
- Stored procedure `SelectLastMessageByLineId` — có thể liên quan background job

### Shared components xác nhận:
- **SC-003 Friend Filter/Segment:** `Conversation::advanceFilterPost()` là core logic, dùng chung với nhiều tính năng khác (broadcast, auto-reply, etc.)
- **SC-002 Tag Selector:** `saveTag()`, `removeTag()` logic dùng chung
