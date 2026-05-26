# FA-038 「友だち情報詳細」 (Friend Detail / My Page) — Logic Spec

> Mức độ tin cậy mặc định: **Cao** (đọc trực tiếp source). Suy luận business rule từ pattern code đánh dấu **Trung bình**.

## 1. Tổng quan kiến trúc

| Lớp | Vai trò | Vị trí |
|-----|---------|--------|
| Routes | Khai báo URL → Controller | `src/web/sns-line/routes/web.php` (~3,980 dòng) |
| Controllers | Nhận request, validate, gọi services/models, trả response | `app/Http/Controllers/Basic/`, `app/Http/Controllers/Admin/`, `app/Http/Controllers/ChatController.php` |
| Helpers (App service container) | `ChatHelper` (registered via `app("ChatHelper")`) chứa logic core: `changeScenario`, `getTemplatesTest`, `sendShortUrl` | `app/Helpers/ChatMessages.php` (binding ChatHelper) |
| Services | `HelperService` (sendAction), `CalendarCourseBookingService` (recompute booking count), `MessageV2Repository` (insert message kind block) | `app/Services/` |
| Repositories | `BotRepository`, `LineUserRepository`, `MessageV2Repository` | `app/Repositories/` |
| Models (Eloquent) | Wrapper bảng DB | `app/Models/` và `app/` (some legacy) |
| External APIs | LINE Messaging API (richmenu link/unlink), Google Calendar API (delete events khi xóa user) | Guzzle Client, gCalendarController |
| Async/Queue tables | `sync_elasticsearch`, `scenario_step_time`, `event_step_time`, `action_schedules`, `user_event` | Spring Boot consumer ngoài scope |

**Pattern điển hình**:
- Controllers dày — chứa cả validation inline (`Validator::make`) và truy vấn DB trực tiếp qua model facades.
- Side effects nhiều: 1 endpoint thường update vài bảng + insert vào queue table + gọi external API.
- Cảnh báo: phương thức `updateLineUser` (case `deleteLineUser`) dài ~400 dòng (line 2064–2466) — vi phạm SRP, khó maintain.
- Lỗi xử lý generic: hầu hết method bọc try-catch tổng + log + trả `{"success": false}`.

---

## 2. Controllers

### 2.1 `Basic\FriendlistController`
**File**: `src/web/sns-line/app/Http/Controllers/Basic/FriendlistController.php` (4337 dòng).

Methods liên quan FA-038:

| Method | Line | Mục đích | Models / Services dùng |
|--------|------|----------|------------------------|
| `mypage` | 1615 | Render trang HTML chi tiết bạn | Conversation, BotLineUser, LineUser, Bots, BotController::getInfoFromLine, SyncElasticsearch, ScenarioLineuser, ScenarioStepTime, Category, Template, Tags |
| `updateLineUser` | 2009 | Switch xử lý `block` / `deleteLineUser` (theo `request->type`) | BotLineUser, Conversation, ScenarioLineuser, Scenario, Bots, MobileNotify, BotFriendStatistic, RichMenus (LINE API), StatusChat, BotLineUserItem, AutoReplyHistory, UserButton, SyncElasticsearch, BBooking, BPlanSlot, BSlot, CalendarSalonLineBooking, EventStepTime, CalendarCourseBooking, OrderHistory, CycleOrderHistory, BCUserBooking, gCalendarController, FriendInformationValue, FriendInformationSetting, DetailLandingClick, Landing, LandingHistory, CollectOpenLanding, TimeActionLanding, FormAnswer, FormAnswerResult, FormAnswerUserAccept, MessageV2Repository |
| `updateLineUsersBlock` | 1970 | Block hàng loạt theo `conversationIds` (gọi từ list view; bỏ qua trong scope FA-038) | Conversation, BotLineUser, ScenarioLineuser, Bots |
| `unblockFriend` | (~1924) | Unblock 1+ user | Conversation, BotLineUser |
| `updateLineInfo` | 1738 | Update view_name/email/phone (legacy) | LineUser, BotLineUser, Validator |
| `updateIsTester` | 1805 | Toggle is_tester | BotLineUser |
| `mypageURL` (`urlMyPage`) | 1822 | Sub-page URL analytics | UrlShorten, UrlShortenDetail, App\Url, LineUser |
| `siteAccessHistoryMyPage` | 1852 | Sub-page site access | SiteScriptHistory, LineUser |
| `conversionMyPage` | 1869 | Sub-page conversion | Conversion, ConversionResult, line_user_model |
| `answerformMyPage` | 1896 | Sub-page form answer detail | FormAnswerResult, EventTimes, Events |
| `sendMessage` | 1958 | Gửi template từ detail page | ChatHelper |
| `saveScenario` | 2473 | Update scenarios state cho line user | ChatHelper, Scenario, ScenarioLineuser |
| `settingScenario` | 814 | Gán scenario qua Conversation::advanceFilterPost | ChatHelper, Conversation |
| `sendActionFriend` | 864 | Chạy action lên friend(s) | HelperService, BotsProfiles, Conversation::advanceFilter, ActionSchedule (queue) |
| `saveTag` | 1293 | Gán tag (quick) | tagLineUser, Tag, addTags() |
| `saveRichMenu` | 1359 | Link rich menu LINE API | RichMenus, BotLineUser, LineUser, Guzzle Client |
| `removeTag` | 1507 | Gỡ tag bulk | Tags, tag_line_user (DB raw) |
| `initDataFriendInfo` | 4035 | Load config custom field + system fields | FriendInformationSetting, config('sns-line.info_default_info'), config('sns-line.info_default_info_address') |
| `ajaxGetFolderList` | 4213 | Lấy folder list của custom field (kind=information_friend) | Category, FriendInformationSetting |
| `ajaxGetFriendInfoByFolderId` | 4230 | Lấy field theo folder | FriendInformationSetting |

#### `mypage` (line 1615)
- Bảo vệ: 404 khi không có conversation; redirect `/basic/chat-v3` khi không có bot_line_user.
- **External call**: `BotController::getInfoFromLine($bot, $line)` — gọi LINE Messaging API `/v2/bot/profile/{userId}` để đồng bộ avatar + display name realtime.
- **Side effect**: nếu name đổi → INSERT `sync_elasticsearch` (Spring Boot consumer sẽ update ES index).

#### `updateLineUser` (line 2009)
Cấu trúc switch theo `request->type`:
- `case 'block'` (line 2018-2063): clean scenario_step_time queue, update bot_line_user.is_blocked, conversation.blocked_at, scenario count_follow/count_unfinish, insert message kind BLOCK_FRIEND.
- `case 'deleteLineUser'` (line 2064-2466): cascade cleanup ~30 bảng (xem api-spec EP-08).

Cuối hàm: `updateBadge($bot)` recompute badge count.

#### `saveTag` (line 1293) vs ChatController `saveTagLine` (line 3491)
Hai endpoint khác nhau:
- `saveTag` (FA-013 list page) — gán **1 tag** theo `tag_id` cho tập searchIDs.
- `saveTagLine` (FA-038 mypage tab タグ) — gán **bộ tags** theo `tags_id[]` với logic diff.

### 2.2 `ChatController`
**File**: `src/web/sns-line/app/Http/Controllers/ChatController.php` (6506 dòng).

Methods liên quan FA-038:

| Method | Line | Mục đích | Models dùng |
|--------|------|----------|-------------|
| `getDataMyPage` | 4845 | Branch `common` (basic info + listCycle + listOnce + listBooking + infoCustom) hoặc `scenario` (current scenario + history) | LineUser, BotLineUser, Affiliaters, RichMenus, DetailLandingClick, Landing, Conversation, Bots, FriendInformationValue, FriendInformationSetting, StripBot, CycleOrderHistory, OrderHistory, BBooking, BEventDetail, BSlot, ScenarioLineuser, Scenario, ScenarioStepTime, StepMessage, Template, TmpButton, Buttons, TmpIntroduction, TmpLocation, StepMessageHistory, Category |
| `getDataRemindMyPage` | 5120 | Tab リマインド配信 | user_event (DB raw), events, EventTimes, EventStep, Template |
| `getDataFormAnswerMyPage` | 5222 | Tab フォーム回答 | FormAnswerResult, FormAnswer, FormAnswerDetail, EventTimes, Events |
| `getTagInCat` | 3357 | Tab タグ — load tag list theo folder + status `is_selected` | Tags, tag_line_user, Category |
| `add_tag` | 3462 | Tạo tag mới (validation `tags_exist` rule custom) | Tags |
| `saveTagLine` | 3491 | Save tags từ tab タグ (diff add/remove + handle tag limit) | tagLineUser, Tags, ActionLimitTag, HelperService |
| `saveScenario` | 3610 | Endpoint `/basic/save_scenario_line` (chat 1-1) — không thuộc FA-038 chính | ChatHelper, ScenarioStepTime, StepMessage |
| `sendMessage` | 1918 | Endpoint `/basic/send_message` (đang disabled — return ngay đầu method) | (no-op) |
| `saveSettingInfoMyPage` | 5304 | Save `bots.setting_info_my_page` | Bots |
| `actionScenarioMyPage` | 5327 | Manual change/cancel scenario từ mypage tab ステップ配信 | ChatHelper |
| `removeTagLineUserMyPage` | 5372 | Remove 1 tag (chip click) + sync ES | tagLineUser, Tags, SyncElasticsearch |
| `stopRemind` | 5206 | Stop reminder cho user (delete user_event) | user_event (DB raw) |

### 2.3 `Admin\BotController`
**File**: `src/web/sns-line/app/Http/Controllers/Admin/BotController.php`.

| Method | Line | Mục đích | Models dùng |
|--------|------|----------|-------------|
| `saveLineUser` | 3473 | Save memo (vào `bot_line_user.memo` hoặc `conversation.memo`) | BotLineUser, Conversation |
| `saveCustomInfo` | 3497 | Save toàn bộ custom info + system fields địa chỉ + line_user profile | LineUser, FriendInformationValue, FriendInformationSetting, SyncElasticsearch (qua settingEventTimeFriendInfo helper) |

### 2.4 `Basic\StepMessageController`
| Method | Mục đích |
|--------|----------|
| `ajaxGetListStepMessageMyPage` | Load list step của 1 scenario (cho modal manual change) |

### 2.5 `Basic\BookingEventController` / `Basic\BookingManagerController`
| Method | Mục đích |
|--------|----------|
| `ajaxGetUserBookingEventDetailById` | Detail 1 booking event |
| `ajaxGetUserBookingCalendarList` | List booking calendar của user |

### 2.6 `Basic\BasicController`
| Method | Mục đích |
|--------|----------|
| `getFileUrl` | Trả signed URL cho file (image custom field) |

---

## 3. Models / Eloquent

Vị trí: `src/web/sns-line/app/Models/` và một số `src/web/sns-line/app/*.php` (legacy).

### 3.1 Models trung tâm (user)

| Model | Bảng DB | Vai trò |
|-------|---------|---------|
| `LineUser` | `line_user` | Profile LINE (line_id LINE platform, view_name, name, real_name, phone_number, email, birthday, province) |
| `BotLineUser` | `bot_line_user` | Liên kết bot ↔ line_user (memo, is_blocked, is_tester, rich_menu_id, affiliater_id, followed_at, phone_number) |
| `BotLineUserItem` | `bot_line_user_items` | (Item meta) — bị xóa khi delete user |
| `Conversation` | `conversation` | Hội thoại (is_blocked, blocked_at, blocked_by, last_time_message, id_status, is_old_friend, is_hide) |
| `Bots` | `bots` | Bot config (channel_access_token, count_user_unconfirm, count_app_notify, setting_info_my_page, free_send_count, plan_type) |

### 3.2 Models scenario (tab ステップ配信)

| Model | Bảng | Vai trò |
|-------|------|---------|
| `ScenarioLineuser` | `scenario_lineuser` | Subscription user × scenario (is_following: 1=running, 0=stopped, 2=finished) |
| `Scenario` | `scenario` | Định nghĩa scenario (name, count_follow, count_stop, count_unfinish) |
| `ScenarioStepTime` | `scenario_step_time` | **Queue gửi step**: status=0 chưa gửi, send_time là thời điểm scheduler gửi (Spring Boot consume) |
| `StepMessage` | `step_message` | Định nghĩa step trong scenario (start_day, start_time, template_ids comma-separated) |
| `StepMessageHistory` | `step_message_history` | Log lịch sử gửi step (status: 2=success, 3=error, 4=filtered_out) |

### 3.3 Models reminder (tab リマインド配信)

| Model | Bảng | Vai trò |
|-------|------|---------|
| `user_event` (DB raw) | `user_event` | Subscription reminder per user × event |
| `Events` | `events` | Event/reminder definition |
| `EventTimes` | `event_times` | Time slot của event |
| `EventStep` | `event_step` | Step trong event |
| `EventStepTime` | `event_step_time` | **Queue gửi step event** (Spring Boot consume) |

### 3.4 Models tag (tab タグ)

| Model | Bảng | Vai trò |
|-------|------|---------|
| `Tags` / `Tag` | `tags` | Tag definition (name, category_id, is_limit, limit, count_user_tag, action_id, limit_action_id, scenario_id) |
| `tagLineUser` | `tag_line_user` | M-to-M user × tag (is_deleted soft) |
| `Category` | `category` | Folder tag (kind=`information_friend`) |
| `ActionLimitTag` | (helper) | Xử lý logic khi tag limit |

### 3.5 Models event booking (tab イベント予約)

| Model | Bảng | Vai trò |
|-------|------|---------|
| `BBooking` | `b_user_booking` | Booking user × event (status, plan_slot_id, slot_id, quantity) |
| `BEventDetail` | `b_event_detail` | Event definition (title, type) |
| `BSlot` | `b_slot` | Slot thời gian (date_start_from, time_start, use_people, type_event) |
| `BPlanSlot` | `b_plan_slot` | Plan tickets per slot (remain_limit) |
| `CalendarSalonLineBooking` | `calendar_salon_line_booking` | Booking salon style |
| `BCUserBooking` | `bc_user_booking` (hoặc `b_c_user_booking`) | Booking calendar lesson |
| `CalendarManagement` | `calendar_management` | Lesson calendar definition |
| `CalendarCourseBooking` | `calendar_course_booking` | Booking course lesson |

### 3.6 Models purchase (tab 購入履歴)

| Model | Bảng | Vai trò |
|-------|------|---------|
| `OrderHistory` | `s_order_history` | Đơn hàng đơn lẻ (item_id, line_user_id, cycle_order_id) |
| `CycleOrderHistory` | `s_cycle_order_history` | Đơn hàng định kỳ |
| `s_items` (raw join) | `s_items` | Sản phẩm (is_product_new) |
| `StripBot` | `strip_bot` | Cấu hình Stripe bot (account_live_id) |

### 3.7 Models form answer (tab フォーム回答)

| Model | Bảng | Vai trò |
|-------|------|---------|
| `FormAnswer` | `form_answer` | Form definition (name, title, count_user_reply) |
| `FormAnswerResult` | `form_answer_result` | Câu trả lời (form_id, line_id, data JSON, status_sync_deleted) |
| `FormAnswerDetail` | `form_answer_detail` | Chi tiết câu hỏi |
| `FormAnswerUserAccept` | `form_answer_user_accept` | User chấp nhận form |
| `user_open_formanswer` (raw) | `user_open_formanswer` | Tracking thời gian xem form |

### 3.8 Models custom field

| Model | Bảng | Vai trò |
|-------|------|---------|
| `FriendInformationSetting` | `friend_information_setting` | Định nghĩa custom field (name, type_data, order, setting_value JSON, total_user_has_value) |
| `FriendInformationValue` | `friend_information_value` | Value per user × field (line_id, friend_information_setting_id, value) — pattern EAV |

**System fields** (id âm hardcoded):
- `-7` zip_code
- `-8` district  
- `-9` township
- `-10` building

Còn một số default trong config: `config('sns-line.info_default_info')` (id ≥ -6, ví dụ `-1` name, `-2` system_display_name, `-4` birthday, `-6` province).

### 3.9 Models richmenu / landing / messaging

| Model | Bảng | Vai trò |
|-------|------|---------|
| `RichMenus` | `rich_menus` | Rich menu definition (rich_menu_id LINE platform) |
| `Landing` | `landing` | QR landing page |
| `DetailLandingClick` | `detail_landing_click` | Click history |
| `LandingHistory` | `landing_history` | Aggregated landing stats per day |
| `CollectOpenLanding` | `collect_open_landing` | Open tracking per device per day |
| `TimeActionLanding` | `time_action_landing` | Action time tracking |
| `Affiliaters` | `affiliaters` | Affiliater info |
| `MessagesV2` | `messages` (sharded by year `messages2025`, ...) | Chat messages |
| `Template` / `TmpButton` / `Buttons` / `TmpIntroduction` / `TmpLocation` | `template`, `tmp_button`, `buttons`, `tmp_introduction`, `tmp_location` | Template messaging |

### 3.10 Models async / queue

| Model | Bảng | Vai trò |
|-------|------|---------|
| `SyncElasticsearch` | `sync_elasticsearch` | Queue job sync ES (Spring Boot consume) — type: `update`, `delete_line_user`, `user_tag`, `is_hide` |
| `ActionSchedule` | `action_schedules` | Queue chạy action async (cho > 200 friends) |
| `MobileNotify` | `mobile_notify` | App notification (delete khi xóa user) |
| `AutoReplyHistory` | `auto_reply_history` | Lịch sử auto reply (delete khi xóa user) |
| `UserButton` | `user_button` | Click history button (delete khi xóa user) |
| `Conversion` / `ConversionResult` | `conversion`, `conversion_result` | Conversion tracking |
| `BotFriendStatistic` | `bot_friend_statistic` | Daily statistic count followers |
| `StatusChat` | `status_chat` | Chat status với count user |
| `Url` / `UrlShorten` / `UrlShortenDetail` / `DetailUrlClick` | `url`, `url_shorten`, `url_shorten_detail`, `detail_url_click` | URL shortener tracking |
| `SiteScriptHistory` | `site_script_history` | Site access tracking |

---

## 4. Services / Helpers

### 4.1 `ChatHelper` (binding `app("ChatHelper")`)
- File: `app/Helpers/ChatMessages.php` (binding tại ServiceProvider).
- Methods quan trọng:
  - `changeScenario($scenario_id, $line_user_id, $bot_id, $params_time, $is_stop, $from, $is_skip_filter, $is_skip_action, $is_test, $source)` — core logic chuyển scenario:
    - UPDATE `scenario_lineuser.is_following=0` cho scenario cũ.
    - INSERT `scenario_lineuser` mới (is_following=1).
    - INSERT `scenario_step_time` với `status=0` cho step đầu (queue cho Spring Boot).
    - Nếu `$is_stop=true` → chỉ stop, không chuyển.
    - Source `{trigger_type: 15001}` = manual từ my_page.
  - `getTemplatesTest($request)` — gửi template test qua LINE Messaging API.
  - `sendShortUrl`, `sendShortUrlAutore` — convert long URL → short URL (cho text message).

### 4.2 `HelperService`
- File: `app/Services/HelperService.php`.
- Method `sendAction($actionId, $line_user_id, $bot_id, $extras, $from, $is_count, $params, $reception_id, $eventStepTimeId, $sourceFrom, $tag_id)`:
  - Đọc `action.kind` → routing tới các sub-actions (gửi message, gán tag, chuyển scenario, gọi richmenu, ...).
  - Có thể INSERT vào `action_schedules` hoặc `scenario_step_time`.

### 4.3 `MessageV2Repository`
- Tạo record `messages` (sharded year). Dùng cho message kind BLOCK_FRIEND khi block user.

### 4.4 `gCalendarController`
- File: `app/Http/Controllers/gCalendarController.php`.
- Method `deleteEventByBooking($userBookingCalendar)` — gọi Google Calendar API DELETE event sync.

### 4.5 Helper functions (autoloaded)
- `getBotId()` — lấy bot id từ session.
- `getCurrentUser()` — Auth::id().
- `addLogUserAction($action)` — INSERT `activity_logs` (audit trail).
- `addTags(array $tagIds, $line_user_id, $bot_id)` — wrapper INSERT `tag_line_user` + cập nhật count.
- `getTotalNotifyExceptSystemAndBillCycle($botId)` — count notify cho `bots.count_app_notify`.
- `totalUserConfirmMessage($botId)` — count user chưa đọc msg.
- `updateBadge($bot)` — recompute badge.
- `updateMessageSendCount($bot_id, $date, $type)` — daily count.
- `is_image($path)` — phân loại file image.
- `settingEventTimeFriendInfo($lineID, $type, $bot_id, $value)` — trigger reminder dựa theo field birthday/d_4.

### 4.6 Service Providers
- `ChatHelper` được bind trong AppServiceProvider (singleton).
- `\Vinkla\Hashids\Facades\Hashids` — encode order ID.

---

## 5. Form Requests / Validation

**Không có FormRequest riêng** cho FA-038. Validation inline qua `Validator::make`:

| Endpoint | Field validation |
|----------|------------------|
| EP-12 `updateLineInfo` | `line_id: nullable\|int`, `view_name: nullable\|max:20`, `real_name: nullable\|max:20`, `email: nullable\|email`, `phone_number: nullable\|regex:/^\+?[0-9]{9,15}$/u` |
| EP-22 `add_tag` | `name: required\|tags_exist:tags,name,bot_id,{bot_id}\|min:1\|max:50\|string` |
| EP-11 `saveCustomInfo` | `birthday` regex `Y-m-d` hoặc `Y/m/d` (inline check) |

Custom validation rule `tags_exist` được đăng ký trong `app/Providers/ValidatorServiceProvider.php` (suy luận).

---

## 6. Events / Listeners

Không thấy `Event::dispatch()` trực tiếp trong các method FA-038. Side effects được xử lý **đồng bộ** trong controller (không qua Laravel Event/Listener pattern).

Cơ chế async dùng cho FA-038 là **DB queue tables** (Spring Boot consumer):
| Bảng queue | Producer (controller method) | Consumer |
|-----------|------------------------------|----------|
| `sync_elasticsearch` | `mypage` (update name), `updateLineUser` (block + delete), `removeTagLineUserMyPage`, `saveCustomInfo` (đổi view_name) | Spring Boot ES sync job |
| `scenario_step_time` | `actionScenarioMyPage`, `saveScenario` (insert); `updateLineUser` block/delete (delete) | Spring Boot scenario sender |
| `event_step_time` | (delete in `updateLineUser`) | Spring Boot reminder sender |
| `action_schedules` | `sendActionFriend` (allUser), `saveTagLine` (sendAction trigger) | Spring Boot action executor |
| `user_event` | (delete in `stopRemind`) | Spring Boot reminder sender (skip nếu không có) |

---

## 7. Authorization

- Tất cả endpoints yêu cầu `basic_access` middleware → user phải có session Laravel hợp lệ.
- `bot_id` lấy từ session (`getBotId()`) — cùng pattern: user chỉ thao tác trên bot đang chọn. Nếu cố thao tác user của bot khác → query `WHERE bot_id = currentBotId` sẽ không match → trả `success: false` hoặc 404.
- Không có check role-based explicit cho Admin vs Staff trong controller — hệ thống dựa vào permission ở UI level (button hidden) và middleware `basic_access` cùng `is_expire`. Permission Staff cụ thể được lưu ở `user_permission_basic` (bảng) — kiểm tra phía frontend.

---

## 8. Business Rules

### BR-01 — Khi block user (EP-07)
- Set `bot_line_user.is_blocked=1`, `conversation.is_blocked=1, blocked_by=1, blocked_at=NOW()`.
- Decrement `scenario.count_follow` và increment `scenario.count_unfinish` cho scenario đang chạy.
- UPDATE `scenario_lineuser.is_following=0`.
- **DELETE `scenario_step_time` WHERE status=0** — clear các step đã queue chưa gửi.
- INSERT message kind `KIND_MESSAGE_BLOCK_FRIEND` vào conversation với content `'ブロックしました'` (audit).
- Recompute `bots.count_user_unconfirm`.

### BR-02 — Khi delete user (EP-08) — cascade ~30 bảng
- Quy trình thứ tự (xem chi tiết EP-08):
  1. Xóa notify (mobile_notify) → recompute `bots.count_app_notify`.
  2. Decrement `bot_friend_statistic.count_user_followed/unfollowed`.
  3. Unlink rich menu trên LINE platform (Guzzle DELETE LINE API), clear `bot_line_user.rich_menu_id`.
  4. Decrement `status_chat.count`.
  5. Delete `bot_line_user_item`, `auto_reply_history`, `user_button`.
  6. **INSERT `sync_elasticsearch` type=`delete_line_user`** (Spring Boot xóa ES doc).
  7. Delete `bot_line_user`, `conversation`.
  8. Decrement scenario counts + delete `scenario_lineuser`, `scenario_step_time`.
  9. Decrement `tags.count_user_tag` + delete `tag_line_user`.
  10. Decrement `form_answer.count_user_reply` + delete form answers + `event_step_time` (form_result_id).
  11. Delete event/booking: `b_user_booking` + decrement `b_plan_slot.remain_limit`, `b_slot.use_people`; `calendar_salon_line_booking` + `event_step_time`; `calendar_course_booking` + recompute booking status; `bc_user_booking` + Google Calendar API DELETE event.
  12. Delete order: `s_order_history`, `s_cycle_order_history`.
  13. Delete reminder: `user_event`, các `event_step_time` còn lại.
  14. Delete tracking: `user_open_formanswer`, `conversion_result`, `step_message_history`, `url_shorten`, `url_shorten_detail`, `detail_url_click`.
  15. Decrement `friend_information_setting.total_user_has_value` + delete `friend_information_value`.
  16. Recompute `landing.total_user_click/total_user_friend/count_action_web/count_action` + `landing_history` + `collect_open_landing` + delete `detail_landing_click`, `time_action_landing`.
  17. Recompute `bots.count_user_unconfirm`, `updateBadge`.
- **Không có rollback transaction** — nếu lỗi giữa chừng → DB inconsistent.

### BR-03 — Update memo (EP-10)
- Nếu có `id` (bot_line_user.id) → UPDATE `bot_line_user.memo`.
- Nếu chỉ có `conversation_id` → UPDATE `conversation.memo`.
- Hai cột memo độc lập (theo design, có thể không sync) — **Trung bình**.

### BR-04 — Custom field EAV pattern (EP-11)
- Bảng định nghĩa: `friend_information_setting` (name, type_data, order, setting_value).
- Bảng value: `friend_information_value` (line_id, friend_information_setting_id, value).
- 1 record per user × field.
- Khi user lần đầu có value cho field → increment `total_user_has_value` của field.
- Khi user clear value (null) → DELETE record.
- Type data IN (1=text, 2=number, 3=date, 6=select) → query `initDataFriendInfo` chỉ lấy 4 type này; type khác (4=image, 5=address...) xử lý tách.

### BR-05 — System fields hardcoded id âm
- `-7` zip_code
- `-8` district  
- `-9` township
- `-10` building
- (config) `-1` name, `-2` system_display_name, `-4` birthday, `-6` province
- Lưu cùng bảng `friend_information_value` với `friend_information_setting_id` âm.
- UI render trong section riêng (vùng địa chỉ).

### BR-06 — Tag với scenario_id auto-trigger
- Khi gán tag (EP-21 hoặc EP-35) có `tag.scenario_id != null` → trigger `ChatHelper::changeScenario` chuyển user sang scenario tương ứng.
- Khi gán tag có `tag.action_id != null` → `HelperService::sendAction(action_id)` chạy action liên kết.

### BR-07 — Tag limit
- Field `tags.is_limit=1` + `tags.limit` → max user gán tag.
- Khi đạt limit → không gán nữa, chạy `tag.limit_action_id` (alternative action).
- Logic check: `WHERE count_user_tag + 1 <= limit` (atomic update via `whereRaw`).

### BR-08 — Manual scenario change creates queue (EP-16)
- `actionScenarioMyPage` action=`change` → `ChatHelper::changeScenario`:
  - Source `{trigger_type: 15001, from_id: Auth::id()}` = manual từ my_page.
  - INSERT `scenario_step_time` (status=0) cho step đầu của scenario mới — **queue cho Spring Boot scheduler**.

### BR-09 — Force stop scenario (EP-17)
- `actionScenarioMyPage` action=`cancel` (scenario_id=0) → `changeScenario(0, ...)`:
  - UPDATE `scenario_lineuser.is_following=0` cho scenario hiện tại.
  - Không INSERT `scenario_step_time` mới.

### BR-10 — Save rich menu calls LINE API (EP-34)
- Có 2 nhánh:
  - `rich_menu_id != 0`: POST LINE API `/v2/bot/user/{lineId}/richmenu/{richIdForLine}` Bearer token → check 200 → UPDATE `bot_line_user.rich_menu_id`.
  - `rich_menu_id == 0`: tìm default richmenu (`status_rich=1, status_line=1`):
    - Không có default → DELETE LINE API unlink + clear `rich_menu_id`.
    - Có default → POST LINE API link default + set `rich_menu_id=default.id`.
- Nếu LINE API throw exception → log + bỏ qua (continue) — UI có thể không phản ánh state thực.

### BR-11 — Send message inline (EP-26 disabled)
- `/basic/send_message` đã bị disable hardcode (return ngay đầu method). UI v2 không gọi endpoint này nữa cho mypage; cần dùng `sendMessage` của FriendlistController (EP-27) hoặc chuyển sang trang chat.

### BR-12 — Tab data overlap
- EP-02 (`type=common`) trả về **đồng thời**:
  - infoBasic (cho SCR-FMP-01).
  - listCycle, listOnce, accountPayment (cho SCR-FMP-06 購入履歴).
  - listBooking (cho SCR-FMP-05 イベント予約).
- → Tab 購入履歴 và イベント予約 **không có endpoint riêng**, dùng dữ liệu chung. Khi user chuyển tab — chỉ JS show/hide, không AJAX lại.

### BR-13 — Scenario history pagination
- EP-03 (`type=scenario`) paginate `step_message_history` 20/trang.
- Status filter: `IN [2, 3, 4]` = 配信済み (2), 配信エラー (3), 絞り込み配信対象外 (4) — **Trung bình** (suy luận từ enum).
- Tính `通数` (order) bằng cách load tất cả step (sort by start_day, start_time) rồi tìm index của `step_mesage_id` trong list — O(n²) khi nhiều history.

### BR-14 — Form answer pagination
- EP-05 paginate 5/trang.
- Subquery `previous`: lấy data của result trước đó cùng form (so sánh thay đổi).
- Render đặc biệt:
  - `event_1`: convert event_time_id → event_name.
  - `date_time`: format từ object {date, time} hoặc {year, month, day, time}.
  - `friend_info_file`: phân loại image vs file dựa vào `is_image()`.
  - `address`: convert object → array.

### BR-15 — sync_elasticsearch insert pattern
- Khi update profile, delete user, gán/gỡ tag, hide/unhide → INSERT `sync_elasticsearch` với:
  ```php
  ['type' => config('sns-line.type_sync.X'), 'line_user_id', 'bot_id', 'data_sync' => json_encode($delta)]
  ```
- Spring Boot consumer đọc bảng này (polling), update ES index, mark processed.
- Chỉ insert khi `env('API_KEY_ES')` được set.

### BR-16 — Display name LINE refresh
- EP-01 (`mypage`) call LINE API mỗi lần load → đồng bộ display name + avatar mới nhất (không cache phía Laravel).
- Hệ quả: load detail tốn 1 round-trip LINE API.

### BR-17 — Memo storage tách rời
- Memo có thể lưu ở 2 bảng tùy luồng:
  - `bot_line_user.memo` (chính) khi gọi `/admin/save_memo` với `id`.
  - `conversation.memo` khi chỉ có `conversation_id`.
- Có thể không sync — bug tiềm năng.

### BR-18 — Action `addLogUserAction`
- Hầu hết endpoint POST gọi `addLogUserAction("...")` để log audit vào `activity_logs`. Pattern: log message phải mô tả chính xác hành động (vd `"updateLineUser friendlist"`).

### BR-19 — Sub-pages truy cập độc lập
- 4 sub-pages (EP-29 → EP-32) có route riêng `/basic/frienslist/mypage/...` (lưu ý typo `frienslist` thay vì `friendlist`) — chấp nhận cả GET (render view) và POST (return AJAX). Không thuộc 7 tabs chính nhưng có thể link từ trang detail thông qua nút riêng (chưa snapshot UI).

### BR-20 — Avatar URL từ LINE CDN
- `LineUser::getLineUserMyPage` xử lý avatar dựa trên 2 prefix CDN: `PATH_PROFILE_V1` (`profile.line-scdn.net`) và `PATH_PROFILE_V2` (`sprofile.line-scdn.net`) — fallback.

### BR-21 — Permission Staff (chưa rõ ràng)
- Code controller không kiểm tra explicit role Staff → mọi user có session đều xem được mypage.
- Permission rất có thể được kiểm tra ở **frontend** (Blade ẩn nút) hoặc **middleware riêng** (chưa thấy trong route group). **Mức độ tin cậy: Thấp** — cần kiểm tra `user_permission_basic` (bảng) khi spec validation.

---

## 9. Ghi chú detect queue/job

| Producer (FA-038) | Bảng | Type / Action | Spring Boot job dự kiến |
|-------------------|------|---------------|--------------------------|
| EP-01 mypage (đồng bộ name) | `sync_elasticsearch` | type=`update` | ES sync consumer |
| EP-07 block | `scenario_step_time` (DELETE status=0) | — | Scenario step sender skip |
| EP-08 deleteLineUser | `sync_elasticsearch` | type=`delete_line_user` | ES sync consumer (delete index) |
| EP-08 deleteLineUser | `scenario_step_time`, `event_step_time` (DELETE) | — | Sender skip |
| EP-08 deleteLineUser (gọi LINE/Google API) | — | — | (đồng bộ trong request) |
| EP-11 saveCustomInfo (đổi view_name) | `sync_elasticsearch` | type=`update` | ES sync consumer |
| EP-11 saveCustomInfo (birthday) | `event_step_time` (INSERT qua `settingEventTimeFriendInfo`) | — | Reminder sender |
| EP-16/17/19 actionScenarioMyPage / saveScenario | `scenario_step_time` (INSERT status=0) | — | Scenario step sender |
| EP-20 stopRemind | `user_event` (DELETE) | — | Reminder sender skip |
| EP-21 saveTagLine (tag có action_id) | `action_schedules` hoặc `scenario_step_time` (qua `sendAction`) | — | Action executor |
| EP-23 removeTagLineUserMyPage | `sync_elasticsearch` | type=`user_tag` | ES sync consumer |
| EP-37 sendActionFriend (allUser ≥ 200) | `action_schedules` | — | Action executor batch |

→ Khi spec phần job (`/spec-job`), cần phân tích Spring Boot consumer cho 5 bảng queue: `sync_elasticsearch`, `scenario_step_time`, `event_step_time`, `action_schedules`, và scheduler đọc `user_event`.
