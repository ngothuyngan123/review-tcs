# FA-038 「友だち情報詳細」 (Friend Detail / My Page) — API Spec

> Mức độ tin cậy mặc định: **Cao** (nguồn: đọc trực tiếp routes + controllers Laravel). Các mục Thấp ghi rõ.

## 1. Tổng quan

| Thuộc tính | Giá trị |
|------------|---------|
| Tổng số endpoints | **37** (1 HTML + 36 AJAX) |
| Phân nhóm | Page Load (1) / Tab Data Load (5) / User Actions (12) / Sub-pages (4) / Init/legacy (6) / Cross-page actions (5) / Booking-File-Message helpers (4) |
| Portal | Admin LINE OA (`form.watermeru.com`) |
| Actors | Admin, Staff (cùng middleware) |
| Base routes file | `src/web/sns-line/routes/web.php` |
| Controllers chính | `Basic\FriendlistController`, `ChatController`, `Admin\BotController`, `Basic\StepMessageController`, `Basic\BookingEventController`, `Basic\BookingManagerController`, `Basic\BasicController` |

### 1.1 Middleware chung

Route `/basic/friendlist/my_page/{line_id}` và nhóm `/basic/*` được khai báo trong `routes/web.php:823`:

```php
Route::group(['prefix' => 'basic', 'middleware' => ['basic_access', 'https_protocol', 'is_expire', 'check_remember_token']], ...)
```

- `basic_access` — yêu cầu session Admin đăng nhập + bot đã chọn
- `https_protocol` — force HTTPS
- `is_expire` — kiểm tra gói dịch vụ còn hạn
- `check_remember_token` — kiểm tra remember_token khớp DB

Các route `/ajax/*` dưới mức nhóm `/basic` nhưng thường vẫn yêu cầu `basic_access` (tuỳ group wrapper). Các route `/ajax/get_data_*` khai báo ở cuối file (line ~3760+) nằm trong nhóm ngoài cùng (web middleware), nhưng tham chiếu `getBotId()` yêu cầu session Admin.

CSRF token được set sẵn trong view qua `<meta name="csrf-token">` và JS thêm vào header.

---

## 2. Bảng tóm tắt endpoints

### 2.1 Page Load

| EP | Method | URL | Controller@Method | Screen |
|----|--------|-----|-------------------|--------|
| EP-01 | GET | `/basic/friendlist/my_page/{line_id}` | `Basic\FriendlistController@mypage` | Trang HTML tổng |

### 2.2 Tab Data Load

| EP | Method | URL | Controller@Method | Screen |
|----|--------|-----|-------------------|--------|
| EP-02 | GET | `/ajax/get_data_my_page?type=common&user_id={id}` | `ChatController@getDataMyPage` (branch common) | SCR-FMP-01 基本情報 |
| EP-03 | GET | `/ajax/get_data_my_page?type=scenario&user_id={id}` | `ChatController@getDataMyPage` (branch scenario) | SCR-FMP-02 ステップ配信 |
| EP-04 | GET | `/ajax/get_data_remind_my_page?user_id={id}` | `ChatController@getDataRemindMyPage` | SCR-FMP-03 リマインド配信 |
| EP-05 | GET | `/ajax/get_data_form_answer_my_page?page={n}&user_id={id}` | `ChatController@getDataFormAnswerMyPage` | SCR-FMP-07 フォーム回答 |
| EP-06 | GET | `/basic/get_tag_in_category?type=tags&cat_id={id}&line_user_id={id}` | `ChatController@getTagInCat` | SCR-FMP-04 タグ (load tag list theo folder) |

### 2.3 User Actions — Header (toàn trang)

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-07 | POST | `/basic/line_user/update` (body `type=block`) | `Basic\FriendlistController@updateLineUser` | Block user |
| EP-08 | POST | `/basic/line_user/update` (body `type=deleteLineUser`) | `Basic\FriendlistController@updateLineUser` | Delete user (cascade cleanup) |
| EP-09 | POST | `/basic/friendlist/unblock-friend` | `Basic\FriendlistController@unblockFriend` | Unblock user (từ page detail của user đã block) |

### 2.4 User Actions — Tab 基本情報 (SCR-FMP-01)

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-10 | POST | `/admin/save_memo` | `Admin\BotController@saveLineUser` | Lưu memo (field 「メモ」) |
| EP-11 | POST | `/admin/save_custom_info` | `Admin\BotController@saveCustomInfo` | Lưu toàn bộ friend_info + custom fields + system fields (zip/district/township/building) |
| EP-12 | POST | `/basic/update_line_info` | `Basic\FriendlistController@updateLineInfo` | Cập nhật view_name / real_name / email / phone (legacy — có thể không còn dùng ở UI v2) |
| EP-13 | POST | `/basic/update_is_tester` | `Basic\FriendlistController@updateIsTester` | Đánh dấu user là tester (không gửi qua LINE API) |
| EP-14 | POST | `/ajax/save_setting_info_my_page` | `ChatController@saveSettingInfoMyPage` | Lưu cấu hình 「表示設定」 cho bảng 基本情報 / 友だち情報 (lưu ở `bots.setting_info_my_page`) |
| EP-15 | GET | `/ajax/initDataFriendInfo` | `Basic\FriendlistController@initDataFriendInfo` | Load config toàn bộ custom field (để render editor) |

### 2.5 User Actions — Tab ステップ配信 (SCR-FMP-02)

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-16 | POST | `/ajax/action_scenario_my_page` (action=`change`) | `ChatController@actionScenarioMyPage` | 「手動変更」 chuyển scenario |
| EP-17 | POST | `/ajax/action_scenario_my_page` (action=`cancel`) | `ChatController@actionScenarioMyPage` | 「強制停止」 dừng scenario |
| EP-18 | POST | `/get_list_step_my_page` | `Basic\StepMessageController@ajaxGetListStepMessageMyPage` | Load danh sách step trong scenario (khi chọn scenario để chuyển) |
| EP-19 | POST | `/basic/friendlist/my_page/save-scenario` | `Basic\FriendlistController@saveScenario` | Save scenario (variant cũ) — dùng ChatHelper.changeScenario |

### 2.6 User Actions — Tab リマインド配信 (SCR-FMP-03)

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-20 | POST | `/ajax/stopRemind` | `ChatController@stopRemind` | Stop reminder đang chạy (xóa record `user_event`) |

### 2.7 User Actions — Tab タグ (SCR-FMP-04)

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-21 | POST | `/basic/save_tag_line_user` | `ChatController@saveTagLine` (with `save_tag_my_page=1`) | 「登録」 lưu toàn bộ tag đã chọn (diff + add + remove) |
| EP-22 | POST | `/basic/add_tag` | `ChatController@add_tag` | Tạo tag mới nhanh từ tab タグ |
| EP-23 | POST | `/ajax/remove-tag-line-user-my-page` | `ChatController@removeTagLineUserMyPage` | Click chip trong bảng 「現在ついているタグ」 để gỡ 1 tag |

### 2.8 User Actions — Tab イベント予約 (SCR-FMP-05)

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-24 | POST | `/get_user_booking_calendar_list` | `Basic\BookingManagerController@ajaxGetUserBookingCalendarList` | Load list booking calendar của user |
| EP-25 | POST | `/get_booking_event_detail_by_id/{booking_id}` | `Basic\BookingEventController@ajaxGetUserBookingEventDetailById` | Lấy detail 1 booking event |

### 2.9 User Actions — Send message inline / File URL

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-26 | POST | `/basic/send_message` | `ChatController@sendMessage` | Gửi tin (text/template) từ trang chi tiết (legacy — method trả response error sớm, có thể dead-code) |
| EP-27 | POST | `/basic/friendlist/my_page/send-message` | `Basic\FriendlistController@sendMessage` | Gửi tin template (wrapper `ChatHelper.getTemplatesTest`) |
| EP-28 | POST | `/ajax/get-file-url` | `Basic\BasicController@getFileUrl` | Lấy URL file (signed URL cho image custom field) |

### 2.10 Sub-pages (truy cập từ link chi tiết — không phải 7 tabs chính)

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-29 | GET/POST | `/basic/frienslist/mypage/analyst_history/{line_user_id}` | `Basic\FriendlistController@urlMyPage` | Lịch sử click URL của user |
| EP-30 | GET | `/basic/frienslist/mypage/site_access_history/{line_user_id}` | `Basic\FriendlistController@siteAccessHistoryMyPage` | Lịch sử truy cập site script |
| EP-31 | GET | `/basic/frienslist/mypage/conversion/{line_user_id}` | `Basic\FriendlistController@conversionMyPage` | Lịch sử conversion |
| EP-32 | GET/POST | `/basic/frienslist/mypage/answer_form/{line_user_id}` | `Basic\FriendlistController@answerformMyPage` | Chi tiết form answer (view + AJAX) |

### 2.11 Bảng action friend / scenario (tương tác chéo — dùng ở modal filter)

| EP | Method | URL | Controller@Method | Purpose |
|----|--------|-----|-------------------|--------|
| EP-33 | POST | `/basic/friendlist/setting-scenario` | `Basic\FriendlistController@settingScenario` | Gán scenario cho user (dùng chung FA-013 danh sách) — chỉ liệt kê vì mypage_v2.blade cũng gọi được |
| EP-34 | POST | `/basic/friendlist/save-rich-menu` | `Basic\FriendlistController@saveRichMenu` | Gán rich menu cho user (gọi LINE API link richmenu) |
| EP-35 | POST | `/basic/friendlist/save-tag` | `Basic\FriendlistController@saveTag` | Gán 1 tag cho user (quick add) |
| EP-36 | POST | `/basic/friendlist/remove-tag` | `Basic\FriendlistController@removeTag` | Gỡ 1 tag |
| EP-37 | POST | `/basic/friendlist/send-action` | `Basic\FriendlistController@sendActionFriend` | Chạy 1 action lên user (dùng chung với list page) |

> **Ghi chú**: EP-33 → EP-37 dùng chung giữa trang list (FA-013) và mypage (FA-038) — trong FA-038 chúng được dùng khi user mở modal actions. EP-09 `unblock-friend` xuất hiện khi user đã block (view khác).

---

## 3. Chi tiết từng endpoint

---

### EP-01 — GET `/basic/friendlist/my_page/{line_id}`

| | |
|---|---|
| Route | `routes/web.php:957` |
| Controller | `Basic\FriendlistController@mypage` — `app/Http/Controllers/Basic/FriendlistController.php:1615` |
| Middleware | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` |

**Params (path)**:
- `line_id` (integer, required) — PK của `line_user`

**Flow**:
1. Lấy `bot_id` từ session (`getBotId()`).
2. Query `Conversation::getConversation` theo `bot_id + line_id` → 404 nếu không có.
3. Query `BotLineUser::getBotLineUserWithCondition` (`bot_id + line_user_id`) → redirect `/basic/chat-v3` nếu user không thuộc bot.
4. Gọi LINE Messaging API `BotController::getInfoFromLine($bot, $line)` để lấy displayName + pictureUrl mới nhất.
5. Nếu `displayName` khác `line_user.name` → UPDATE `line_user` + insert `SyncElasticsearch` (type=`update`).
6. Query special_status / last_msg từ `messages` / `conversation` bằng subquery raw.
7. `LineUser::getLineUserMyPage($line_id, $bot_id)` — lấy full line_info profile.
8. Load categorized templates + tags hiện gắn.
9. Return view `basic.friendlist.mypage_v2` với bindings: `line_info`, `conver_id`, `line_id`, `categorytags`, `special_status`, `conversation`.

**Response**: HTML view `mypage_v2.blade.php`.

**Screens**: SCR-FMP-01 → SCR-FMP-07 (tất cả tabs).

**Side effects**: 
- UPDATE `line_user.name` khi đồng bộ từ LINE
- INSERT `sync_elasticsearch` nếu name đổi — **DETECTED queue insert** (bảng `sync_elasticsearch` làm queue cho Spring Boot consumer)

---

### EP-02 — GET `/ajax/get_data_my_page?type=common`

| | |
|---|---|
| Route | `routes/web.php:3761` |
| Controller | `ChatController@getDataMyPage` (branch `type=common`) — `app/Http/Controllers/ChatController.php:4845` |
| Middleware | Web middleware + `getBotId()` yêu cầu session |

**Params (query)**:
| Tên | Kiểu | Bắt buộc | Ghi chú |
|-----|------|----------|---------|
| `type` | string | Yes | `common` (basic info) hoặc `scenario` (tab 2) |
| `user_id` | int | Yes | line_user.id |
| `page` | int | No | Paging (cho biến thể scenario history) |

**Response (type=common)**:
```json
{
  "success": true,
  "infoBasic": {
    "name_line": "[W] サポート/🌸",
    "time_follow": "2025-08-26 12:32:...",
    "last_time_message": "2026-03-21 10:44:...",
    "qr_code": "-",
    "aff": "-",
    "rich_menu": "-",
    "name_system": "Gamanda",
    "phone": "0333222111",
    "email": "ngan123@gmail.com",
    "birthday": null,
    "province": null,
    "zip_code": "",
    "district": "",
    "township": "",
    "building": "",
    "list_province": [...],
    "old_friend": 0
  },
  "listCycle": [...],
  "listOnce": [...],
  "accountPayment": "acct_xxx",
  "listBooking": [...],
  "dataSettingInfo": "{...}",
  "infoCustom": [
    {"id": 1, "name": "date 1", "type_data": 3, "newValue": null, "id_value": null, "valueOption": [...]},
    ...
  ]
}
```

**Tables read**: `line_user`, `bot_line_user`, `affiliaters`, `rich_menus`, `detail_landing_click`, `landing`, `conversation`, `bots`, `friend_information_value` (with `friend_information_setting_id IN (-7,-8,-9,-10)`), `friend_information_setting`, `strip_bot`, `s_cycle_order_history`, `s_order_history`, `b_user_booking`, `b_event_detail`, `b_slot`.

**Screens**: SCR-FMP-01 基本情報 (+ listCycle + listOnce dùng cho tab 購入履歴, listBooking dùng cho tab イベント予約 — UI tải chung 1 lần).

**Ghi chú quan trọng**: Response đã chứa sẵn data cho **Tab 購入履歴** (`listCycle`, `listOnce`, `accountPayment`) và **Tab イベント予約** (`listBooking`) — không có endpoint riêng cho 2 tab này, UI render từ data chung.

---

### EP-03 — GET `/ajax/get_data_my_page?type=scenario`

| | |
|---|---|
| Route | `routes/web.php:3761` |
| Controller | `ChatController@getDataMyPage` (branch `type=scenario`) — `ChatController.php:5006` |

**Params (query)**: `type=scenario`, `user_id`, `page`.

**Flow**:
1. `LineUser::getLineUserMyPage` lấy profile.
2. Query `scenario_lineuser` JOIN `scenario` → `scenarioRunning` (scenario đang chạy).
3. Query `scenario_step_time` (status=0, sort by send_time ASC) → `nextStepMessage`.
4. Tính `order` của step (thứ tự `N通目`) bằng cách query `step_message` theo scenario và so `step_mesage_id`.
5. Load template + buttons cho `templateNextStep`.
6. Query `step_message_history` (status IN [2,3,4]) → paginate(20) → `stepMessageHistory`.
7. Enrich mỗi history item: `name_scenario`, `order`, `stepMessage` (template + buttons).
8. `Scenario::getScenarioNotDeleteByBot` → list scenario để render modal chuyển.

**Response**:
```json
{
  "success": true,
  "userScenario": {...},
  "nextStepMessage": {...},
  "templateNextStep": {...},
  "stepMessageHistory": {"data": [...], "current_page": 1, "total": 86, "last_page": 18, "per_page": 5},
  "scenarioRunning": {"name_scenario": "test bug job update", "id_scenario": 12},
  "scenario": [...]
}
```

**Tables read**: `line_user`, `scenario_lineuser`, `scenario`, `scenario_step_time`, `step_message`, `template`, `tmp_button`, `buttons`, `tmp_introduction`, `tmp_location`, `step_message_history`, `category`.

**Screens**: SCR-FMP-02 ステップ配信 (pane trên + table 配信履歴).

---

### EP-04 — GET `/ajax/get_data_remind_my_page`

| | |
|---|---|
| Route | `routes/web.php:3762` |
| Controller | `ChatController@getDataRemindMyPage` — `ChatController.php:5120` |

**Params (query)**: `user_id`.

**Flow**:
1. Query `user_event` JOIN `events` theo `bot_id + user_id`.
2. Với mỗi event: query `event_times` → `time_finish`, query `event_step_time` (status < now, sort ASC) → `next_time_send`.
3. Enrich `messages` array từ `event_step.templates_id` (split comma → load Template).

**Response**:
```json
{"success": true, "listRemind": [{"id": 1, "event_id": 5, "event_name": "...", "time_finish": "...", "next_time_send": "...", "messages": [...]}, ...]}
```

**Tables read**: `user_event`, `events`, `event_times`, `event_step_time`, `event_step`, `template`, `tmp_button`, `buttons`, `category`.

**Screens**: SCR-FMP-03 リマインド配信.

---

### EP-05 — GET `/ajax/get_data_form_answer_my_page`

| | |
|---|---|
| Route | `routes/web.php:3763` |
| Controller | `ChatController@getDataFormAnswerMyPage` — `ChatController.php:5222` |

**Params (query)**: `page` (default 1), `user_id`.

**Flow**:
1. Query `form_answer_result` RIGHT JOIN `form_answer` theo `line_id + bot_id` → paginate(5).
2. Subquery: lấy `previous` (data câu trả lời trước đó của cùng form).
3. Enrich mỗi item: parse `data` JSON, convert `event_1` sang event_name, format `date_time`, phân loại `friend_info_file` (image/file), convert `address`.

**Response**:
```json
{"success": true, "data": {"current_page": 1, "total": N, "per_page": 5, "data": [{"id": ..., "form_id": ..., "data": [...], "previous": ...}]}}
```

**Tables read**: `form_answer_result`, `form_answer`, `form_answer_detail`, `event_times`, `events`.

**Screens**: SCR-FMP-07 フォーム回答.

---

### EP-06 — GET `/basic/get_tag_in_category`

| | |
|---|---|
| Route | `routes/web.php` (định nghĩa trong nhóm `/basic`) |
| Controller | `ChatController@getTagInCat` — `ChatController.php:3357` |

**Params (query)**:
| Tên | Kiểu | Bắt buộc | Ghi chú |
|-----|------|----------|---------|
| `type` | string | Yes | `tags` (hoặc `template`) |
| `cat_id` | int | Yes | `0` = 未分類, hoặc id folder |
| `line_user_id` | int | Yes | line_user.id |
| `botIdCurrent` | int | No | Override bot |

**Flow**:
1. Query `tags` LEFT JOIN `tag_line_user` ON tag_id, filter `tag_line_user.line_user_id = line_user_id`.
2. Thêm cột `is_selected` (CASE WHEN line_user_id matches THEN TRUE).
3. `listTagUserDefault`: tag của user thuộc category=0.
4. `listTagUser`: tag của user thuộc category ≠ 0, JOIN `category`.

**Response**:
```json
{"success": true, "data": [...], "listTagDefault": [...], "listTagUser": [...]}
```

**Tables read**: `tags`, `tag_line_user`, `category`.

**Screens**: SCR-FMP-04 タグ.

---

### EP-07 — POST `/basic/line_user/update` (type=block)

| | |
|---|---|
| Route | `routes/web.php:1932` |
| Controller | `Basic\FriendlistController@updateLineUser` (case `'block'`) — `FriendlistController.php:2018` |

**Body**:
| Tên | Kiểu | Bắt buộc | Ghi chú |
|-----|------|----------|---------|
| `type` | string | Yes | `block` |
| `line_id` | int | Yes | line_user.id |

**Flow** (case `block`):
1. UPDATE `bot_line_user` SET `is_blocked=1`.
2. UPDATE `conversation` SET `is_blocked=1, blocked_by=1, id_status=null, blocked_at=NOW()`.
3. Decrement `scenario.count_follow`, increment `scenario.count_unfinish` nếu có scenario running.
4. UPDATE `scenario_lineuser` SET `is_following=0`.
5. **DELETE `scenario_step_time` WHERE status=0** — clear queue gửi step.
6. Recount bot `count_user_unconfirm` + `last_time_count_user_confirm`.
7. Decrement `status_chat.count` nếu có.
8. INSERT record message kind `KIND_MESSAGE_BLOCK_FRIEND` (`msg_kind=19`?) với content `'ブロックしました'`.

**Response**: `{"success": true, "line_user_id": <id>}`.

**Side effects**: Xóa `scenario_step_time` = clear queue → **DETECTED queue delete** (bảng `scenario_step_time` là queue của Spring Boot scheduler).

**Screens**: Header button 「ブロック」.

---

### EP-08 — POST `/basic/line_user/update` (type=deleteLineUser)

| | |
|---|---|
| Route | `routes/web.php:1932` (chung route với EP-07) |
| Controller | `Basic\FriendlistController@updateLineUser` (case `'deleteLineUser'`) — `FriendlistController.php:2064`-2466 |

**Body**:
| Tên | Kiểu | Bắt buộc | Ghi chú |
|-----|------|----------|---------|
| `type` | string | Yes | `deleteLineUser` |
| `line_id` | int | Yes | line_user.id |

**Flow** (rất phức tạp — ~30 bảng liên quan):
1. `MobileNotify::delete` by line_user_id + bot_id → update `bots.count_app_notify`.
2. Update `bot_friend_statistic.count_user_followed` (decrement), `count_user_unfollowed` (decrement nếu block).
3. Nếu có `rich_menu_id` → call LINE API DELETE richmenu của user, UPDATE `bot_line_user` clear rich_menu_id.
4. Decrement `status_chat.count`.
5. DELETE `bot_line_user_item` (WHERE bot_line_user_id).
6. DELETE `auto_reply_history` JOIN `auto_reply` WHERE line_id + bot_id.
7. DELETE `user_button` JOIN `template` WHERE line_user_id + bot_id.
8. **INSERT `sync_elasticsearch` (type=`delete_line_user`)** — **DETECTED queue insert** (Spring Boot consumer sẽ xoá ES index).
9. DELETE `bot_line_user`, `conversation`.
10. Decrement `scenario.count_follow/count_stop/count_unfinish` theo `scenario_lineuser.is_following`.
11. DELETE `scenario_lineuser`, `scenario_step_time`.
12. DELETE `tag_line_user` + decrement `tags.count_user_tag`.
13. Decrement `form_answer.count_user_reply` cho mỗi form_id user đã reply.
14. DELETE `event_step_time` WHERE form_result_id.
15. UPDATE `form_answer_result.status_sync_deleted=0` rồi DELETE.
16. DELETE `user_open_formanswer`, `form_answer_user_accept`.
17. DELETE `b_user_booking` + decrement `b_plan_slot.remain_limit`, `b_slot.use_people`.
18. DELETE `calendar_salon_line_booking`, `event_step_time` (cho booking calendar salon).
19. DELETE `calendar_course_booking` + `calendarCourseBookingService.countTotalBookingStatus()` recompute.
20. DELETE `event_step_time` (cho booking calendar lesson).
21. DELETE `s_order_history`, `s_cycle_order_history`.
22. DELETE `user_event` (reminder).
23. DELETE `bc_user_booking` + gọi `gCalendar::deleteEventByBooking()` (Google Calendar API xóa event).
24. DELETE `event_step_time` (cho bc_user_booking).
25. DELETE `user_open_formanswer`, `conversion_result`, `step_message_history`.
26. DELETE `url_shorten`, `url_shorten_detail`, `detail_url_click`.
27. Decrement `friend_information_setting.total_user_has_value` cho mỗi custom field user có value.
28. DELETE `friend_information_value`.
29. Recompute `landing.total_user_click`, `total_user_friend`, `count_action_web`, `count_action` dựa trên `detail_landing_click` + `landing_history` + `collect_open_landing`.
30. DELETE `detail_landing_click`, `time_action_landing`, `collect_open_landing`.
31. Update `bots.count_user_unconfirm`.
32. `updateBadge($bot)` — recompute badge count.

**Response**: `{"success": true, "line_user_id": <id>}`.

**Side effects**: 
- Rất nhiều DELETE cascade (~30 bảng)
- **DETECTED queue insert** `sync_elasticsearch`
- **DETECTED external API call** LINE Messaging API (unlink richmenu), Google Calendar API (delete events)

**Screens**: Header button 「削除」.

---

### EP-09 — POST `/basic/friendlist/unblock-friend`

| | |
|---|---|
| Route | `routes/web.php:1923` |
| Controller | `Basic\FriendlistController@unblockFriend` |

**Body**: `listLineId` (array of int).

**Purpose**: Unblock 1+ user. Được gọi từ page detail của user đã block — không áp dụng trong flow chính FA-038 (user chưa block) nhưng vẫn có mặt trên file mypage_v2 chung.

**Response**: `{"success": true, ...}`.

---

### EP-10 — POST `/admin/save_memo`

| | |
|---|---|
| Route | `routes/web.php:443` |
| Controller | `Admin\BotController@saveLineUser` — `BotController.php:3473` |
| Middleware | `basic_access`, `admin_access`, `https_protocol`, `check_remember_token` (nhóm `/admin`) |

**Body**:
| Tên | Kiểu | Bắt buộc | Ghi chú |
|-----|------|----------|---------|
| `id` | int | No | bot_line_user.id (nếu có) |
| `memo` | string | Yes | Nội dung memo |
| `conversation_id` | int | No | Nếu không có `id`, dùng conversation_id → update `conversation.memo` |

**Flow**:
- Nếu có `id` → UPDATE `bot_line_user.memo`.
- Ngược lại → UPDATE `conversation.memo`.

**Response**: `{"success": true, "memo": "..."}`.

**Screens**: SCR-FMP-01 nút 「保存」 memo.

---

### EP-11 — POST `/admin/save_custom_info`

| | |
|---|---|
| Route | `routes/web.php:445` |
| Controller | `Admin\BotController@saveCustomInfo` — `BotController.php:3497` |

**Body**:
| Tên | Kiểu | Bắt buộc | Ghi chú |
|-----|------|----------|---------|
| `user_id` | int | Yes | line_user.id |
| `customInfo` | JSON string | Yes | Mảng custom field {id, value} |
| `custom_show_id` | JSON string | No | Danh sách field đang hiển thị |
| `type_action` | string | Yes | `my_page` (trigger đường nhánh) |
| `data_user` | JSON string | Yes | `{name_system, phone, email, birthday, province, zip_code, district, township, building}` |

**Flow**:
1. Validate `birthday` format (regex `Y-m-d` hoặc `Y/m/d`).
2. UPDATE `line_user` SET view_name, phone_number, email, birthday, province.
3. Gọi `settingEventTimeFriendInfo($lineID, 'd_4', $bot_id, $birthday)` — trigger reminder birthday.
4. Upsert `friend_information_value` cho các system field (id=-7 zip_code, -8 district, -9 township, -10 building).
5. Với mỗi custom field trong `customInfo` — upsert `friend_information_value` + increment `friend_information_setting.total_user_has_value` nếu user chưa có value.
6. Nếu `view_name` thay đổi → insert `sync_elasticsearch` (type=`update`).

**Response**: `{"success": true}` hoặc `{"success": false, "msg": "..."}`.

**Side effects**: 
- INSERT `sync_elasticsearch` khi đổi view_name — **DETECTED queue insert**
- Trigger `settingEventTimeFriendInfo` có thể INSERT `event_step_time` (scheduler queue) — **DETECTED queue insert**

**Screens**: SCR-FMP-01 inline edit custom field + save all.

---

### EP-12 — POST `/basic/update_line_info`

| | |
|---|---|
| Route | `routes/web.php:1991` |
| Controller | `Basic\FriendlistController@updateLineInfo` — `FriendlistController.php:1738` |

**Body (validation)**:
| Tên | Kiểu | Rule |
|-----|------|------|
| `line_id` | int | nullable |
| `view_name` | string | nullable, max:20 |
| `real_name` | string | nullable, max:20 |
| `email` | string | nullable, email |
| `phone_number` | string | nullable, regex `/(^\+?[0-9]{9,15}$)/u` |

**Flow**:
1. Phone: `0...` → `+81...`.
2. UPDATE `line_user` SET các field.
3. UPDATE `bot_line_user.phone_number`.

**Response**: `{"success": true}` / `{"success": false, "errors": {...}}`.

**Ghi chú**: Route name có typo `ufpdateLineInfo`. UI v2 dùng EP-11 là chính; EP-12 là legacy.

---

### EP-13 — POST `/basic/update_is_tester`

| | |
|---|---|
| Route | `routes/web.php:1993` |
| Controller | `Basic\FriendlistController@updateIsTester` — `FriendlistController.php:1805` |

**Body**: `line_id` (int), `is_tester` (0/1).

**Flow**: UPDATE `bot_line_user` SET is_tester.

**Response**: `{"success": true, "is_tester": 0|1}`.

---

### EP-14 — POST `/ajax/save_setting_info_my_page`

| | |
|---|---|
| Route | `routes/web.php:3791` |
| Controller | `ChatController@saveSettingInfoMyPage` — `ChatController.php:5304` |

**Body**: `dataInfo` (JSON string — cấu hình hiển thị).

**Flow**: UPDATE `bots.setting_info_my_page` = dataInfo. Setting áp dụng cho toàn bot (chung tất cả user), không per-user.

**Response**: `{"success": true}`.

**Screens**: Modal 「表示設定」 ở 2 bảng 基本情報 + 友だち情報.

---

### EP-15 — GET `/ajax/initDataFriendInfo`

| | |
|---|---|
| Route | `routes/web.php:3777` |
| Controller | `Basic\FriendlistController@initDataFriendInfo` — `FriendlistController.php:4035` |

**Flow**:
1. Query `friend_information_setting` WHERE bot_id, type_data IN (1,2,3,6), sort `order DESC, id DESC`.
2. Merge với `config('sns-line.info_default_info')` + `config('sns-line.info_default_info_address')` (system fields id âm).
3. Parse `setting_value` JSON → `valueOption`.

**Response**:
```json
{"success": true, "infoCustom": [{"id": -10, "name": "Building", ...}, {"id": -9, ...}, {"id": 1, "name": "date 1", "valueOption": [...]}, ...]}
```

---

### EP-16 / EP-17 — POST `/ajax/action_scenario_my_page`

| | |
|---|---|
| Route | `routes/web.php:3793` |
| Controller | `ChatController@actionScenarioMyPage` — `ChatController.php:5327` |

**Body**:
| Tên | Kiểu | Bắt buộc | Ghi chú |
|-----|------|----------|---------|
| `action` | string | Yes | `change` (chuyển) hoặc `cancel` (dừng) |
| `line_user_id` | int | Yes | |
| `scenario_id` | int | Yes khi action=change | 0 = không chuyển |
| `start_day` | int | No | Offset ngày bắt đầu |
| `start_time` | string | No | HH:mm:ss |
| `type` | int | No | 0 = null start_day/time |

**Flow**: Gọi `ChatHelper::changeScenario` với source `{trigger_type: 15001, from_id: Auth::id()}` — trigger_type `15001` = manual change từ my_page. Method `changeScenario`:
- UPDATE `scenario_lineuser.is_following=0` (scenario cũ).
- INSERT `scenario_lineuser` mới (nếu chuyển).
- INSERT `scenario_step_time` cho step đầu (status=0) — **DETECTED queue insert** (Spring Boot sender đọc).

**Response**: `{"success": true}`.

**Screens**: SCR-FMP-02 button 「手動変更」 (action=change) / 「強制停止」 (action=cancel, scenario_id=0).

---

### EP-18 — POST `/get_list_step_my_page`

| | |
|---|---|
| Route | `routes/web.php:2903` |
| Controller | `Basic\StepMessageController@ajaxGetListStepMessageMyPage` |

**Body**: `scenario_id`.

**Purpose**: Load danh sách step của scenario được chọn (để user pick vị trí bắt đầu).

**Response**: `{"steps": [{"id": ..., "name": ..., "start_day": ..., "start_time": ...}, ...]}`.

---

### EP-19 — POST `/basic/friendlist/my_page/save-scenario`

| | |
|---|---|
| Route | `routes/web.php:1929` |
| Controller | `Basic\FriendlistController@saveScenario` — `FriendlistController.php:2473` |

**Body**: `scenario_id`, `line_user_id`, `type`, `checkAll`, `scenarios` (array).

**Flow**: Loop `scenarios` → `ChatHelper::changeScenario` cho mỗi scenario. Dùng khi user có nhiều scenario và muốn update start_day/start_time của một trong số đó.

**Response**: `{"success": true, "msg": "...", "scenarioLineUser": ""}`.

---

### EP-20 — POST `/ajax/stopRemind`

| | |
|---|---|
| Route | `routes/web.php:3766` |
| Controller | `ChatController@stopRemind` — `ChatController.php:5206` |

**Body**: `id` (user_event.id).

**Flow**: DELETE `user_event` WHERE id.

**Response**: `{"success": true}`.

**Side effects**: Xóa record → Spring Boot reminder scheduler skip → **DETECTED queue delete**.

**Screens**: SCR-FMP-03 nút 停止 reminder.

---

### EP-21 — POST `/basic/save_tag_line_user`

| | |
|---|---|
| Route | `routes/web.php:1830` |
| Controller | `ChatController@saveTagLine` — `ChatController.php:3491` |

**Body**:
| Tên | Kiểu | Bắt buộc | Ghi chú |
|-----|------|----------|---------|
| `line_user_id` | int | Yes | |
| `tags_id` | array<int> | Yes | Tag IDs được chọn |
| `tags_delete` | array<int> | No | Tag IDs cần xóa (nếu không dùng `save_tag_my_page`) |
| `save_tag_my_page` | bool | No | `1` = flow my page (diff với allTagUser) |
| `listCategoryCheck` | array<int> | No | List category_id đang hiển thị (để biết phạm vi diff) |
| `botIdCurrent` | int | No | Override bot |
| `from` | string | No | Source trigger |

**Flow** (với `save_tag_my_page=1`):
1. Lấy `allTagUser` hiện có (trong category đang hiển thị).
2. Compute `tagDelete` = trong `allTagUser` nhưng không trong `tags_id`.
3. Với mỗi `tagDelete`: UPDATE `tags.count_user_tag` - exist_count; DELETE `tag_line_user`.
4. Với mỗi `tags_id`:
   - Check `tag_line_user` đã có chưa.
   - Check `tag.is_limit` — nếu limit đã đạt → chạy `ActionLimitTag::handleLimitActionTag` + `sendAction(limit_action_id)`.
   - Nếu chưa limit → INSERT `tag_line_user`, increment `tags.count_user_tag`, chạy `sendAction(action_id)` nếu tag có `action_id`.

**Response**: `{"success": true}`.

**Side effects**: `sendAction` → chạy 1 action (action_id) → có thể INSERT vào `action_schedules` / `scenario_step_time` — **DETECTED queue insert**.

**Screens**: SCR-FMP-04 button 「登録」.

---

### EP-22 — POST `/basic/add_tag`

| | |
|---|---|
| Route | `routes/web.php:1828` |
| Controller | `ChatController@add_tag` — `ChatController.php:3462` |

**Body (validation)**:
| Tên | Rule |
|-----|------|
| `name` | required, tags_exist:tags,name,bot_id,{bot_id}, min:1, max:50, string |
| `category_id` | int |

**Flow**: INSERT `tags` WHERE `bot_id + name + category_id`.

**Response**: `{"success": true, "data": {...}}` / `{"success": false, "msg": "タグ名を重複しています"}`.

---

### EP-23 — POST `/ajax/remove-tag-line-user-my-page`

| | |
|---|---|
| Route | `routes/web.php:3795` |
| Controller | `ChatController@removeTagLineUserMyPage` — `ChatController.php:5372` |

**Body**: `line_user_id`, `tag_id`.

**Flow**:
1. Count existing `tag_line_user` records. Nếu >0: DELETE + UPDATE `tags.count_user_tag--`.
2. **INSERT `sync_elasticsearch` type=`user_tag`** với data_sync = updated tag list — **DETECTED queue insert**.

**Response**: `{"success": true}`.

**Screens**: SCR-FMP-04 click chip trong bảng 「現在ついているタグ」.

---

### EP-24 — POST `/get_user_booking_calendar_list`

| | |
|---|---|
| Route | `routes/web.php:3111` |
| Controller | `Basic\BookingManagerController@ajaxGetUserBookingCalendarList` |

**Body**: `line_user_id`, paging/filter params.

**Purpose**: Load list booking calendar của user (cho modal detail booking trong tab イベント予約 hoặc tab 購入履歴 booking).

**Response**: `{"success": true, "data": [...]}` — list bookings với event info + slot info.

---

### EP-25 — POST `/get_booking_event_detail_by_id/{booking_id}`

| | |
|---|---|
| Route | `routes/web.php:2949` |
| Controller | `Basic\BookingEventController@ajaxGetUserBookingEventDetailById` |

**Params (path)**: `booking_id`.

**Purpose**: Lấy chi tiết 1 booking event để render modal.

**Response**: `{"success": true, "booking": {...}, "event": {...}, "slot": {...}}`.

---

### EP-26 — POST `/basic/send_message`

| | |
|---|---|
| Route | `routes/web.php:1789` |
| Controller | `ChatController@sendMessage` — `ChatController.php:1918` |

**Body**: `type`, `to_user`, `line_id`, `conversation`, `message`, `type_chat`, `from_app`, `is_shorten_url`...

**Flow** (ghi chú **quan trọng**): Method này trả response lỗi ngay ở đầu (`return response()->json(['success' => false, 'msg' => ...])` dòng 1927) — nghĩa là **endpoint đang bị disabled** ở phiên bản hiện tại. UI v2 không còn gọi endpoint này.

**Response**: `{"success": false, "msg": "送信に失敗しました..."}`.

---

### EP-27 — POST `/basic/friendlist/my_page/send-message`

| | |
|---|---|
| Route | `routes/web.php:1927` |
| Controller | `Basic\FriendlistController@sendMessage` — `FriendlistController.php:1958` |

**Body**: `line_user_id`, template fields.

**Flow**: Gọi `app()->ChatHelper->getTemplatesTest($request)` → gửi template test thông qua LINE API.

**Response**: `{"status": true, "msg": "送信しました。", "redirect_link": "..."}`.

---

### EP-28 — POST `/ajax/get-file-url`

| | |
|---|---|
| Route | `routes/web.php:3930` |
| Controller | `Basic\BasicController@getFileUrl` |

**Body**: `file_path` hoặc `key`.

**Purpose**: Lấy signed URL cho file (image custom field) stored ở S3/Backblaze.

**Response**: `{"url": "https://..."}`.

---

### EP-29 — GET/POST `/basic/frienslist/mypage/analyst_history/{line_user_id}`

| | |
|---|---|
| Route | `routes/web.php:1965` |
| Controller | `Basic\FriendlistController@urlMyPage` — `FriendlistController.php:1822` |

**Flow**:
- GET (không ajax): render view `basic.mypage.url`.
- POST + ajax: Query `url_shorten`, `url_shorten_detail` → count + rate click.

**Response (POST ajax)**: `{"success": true, "data": [...], "line_info": {...}, "url_total": N, "rate": %, "url_detail_total": M}`.

---

### EP-30 — GET `/basic/frienslist/mypage/site_access_history/{line_user_id}`

| | |
|---|---|
| Route | `routes/web.php:1967` |
| Controller | `Basic\FriendlistController@siteAccessHistoryMyPage` — `FriendlistController.php:1852` |

**Flow**:
- GET (không ajax): render view `basic.mypage.site_access_history`.
- GET + ajax: Query `site_script_history` → paginate.

**Response (ajax)**: `{"success": true, "history": {...pagination}}`.

---

### EP-31 — GET `/basic/frienslist/mypage/conversion/{line_user_id}`

| | |
|---|---|
| Route | `routes/web.php:1969` |
| Controller | `Basic\FriendlistController@conversionMyPage` — `FriendlistController.php:1869` |

**Flow**: Query `conversion` + `conversion_result` → count + rate + list conversion với `is_viewed`, `time_visited`.

**Response**: HTML view `basic.mypage.conversion`.

---

### EP-32 — GET/POST `/basic/frienslist/mypage/answer_form/{line_user_id}`

| | |
|---|---|
| Route | `routes/web.php:1971` |
| Controller | `Basic\FriendlistController@answerformMyPage` — `FriendlistController.php:1896` |

**Flow**:
- POST + ajax: Query `form_answer_result` → enrich (event → event_name, date_time format, file type).
- GET (view): count forms + render view `basic.mypage.answerform`.

**Response (POST ajax)**: `{"success": true, "form_result": [...]}`.

---

### EP-33 — POST `/basic/friendlist/setting-scenario`

Xem logic-spec.md mục Controller.

---

### EP-34 — POST `/basic/friendlist/save-rich-menu`

| | |
|---|---|
| Route | `routes/web.php:1951` |
| Controller | `Basic\FriendlistController@saveRichMenu` — `FriendlistController.php:1359` |

**Body**: `rich_menu_id`, `searchIDs` (array), `allUser`, `item_search`, `item_search_or`, `keyword`.

**Flow**:
1. Nếu `rich_menu_id != 0`: call LINE Messaging API POST `/v2/bot/user/{lineId}/richmenu/{richIdForLine}` với Bearer token bot → nếu 200 → UPDATE `bot_line_user.rich_menu_id`.
2. Nếu `rich_menu_id == 0`: check `rich_menus` default (status_rich=1, status_line=1). Nếu không có → call DELETE LINE API unlink. Nếu có → POST LINE API link default.

**Response**: `{"success": true}`.

**Side effects**: **External API call** LINE Messaging.

---

### EP-35 — POST `/basic/friendlist/save-tag`

| | |
|---|---|
| Route | `routes/web.php:1948` |
| Controller | `Basic\FriendlistController@saveTag` — `FriendlistController.php:1293` |

**Body**: `tag_id`, `searchIDs`, `allUser`, `item_search`, `item_search_or`, `keyword`.

**Flow**: Loop searchIDs → `addTags([tag_id], val, bot_id)` + `tag_line_user::updateOrCreate`. Nếu tag có `scenario_id` → trigger scenario change (qua helper).

**Response**: `{"success": true}`.

---

### EP-36 — POST `/basic/friendlist/remove-tag`

| | |
|---|---|
| Route | `routes/web.php:1953` |
| Controller | `Basic\FriendlistController@removeTag` — `FriendlistController.php:1507` |

**Body**: `tag_id`, `searchIDs`, `allUser`, filter params.

**Flow**: DELETE `tag_line_user` WHERE line_user_id IN (...) AND tag_id; decrement `tags.count_user_tag`.

**Response**: `{"success": true}`.

---

### EP-37 — POST `/basic/friendlist/send-action`

| | |
|---|---|
| Route | `routes/web.php:1949` |
| Controller | `Basic\FriendlistController@sendActionFriend` — `FriendlistController.php:864` |

**Body**: `action_id`, `searchIDs`, `allUser`, filter params.

**Flow**: 
- Với ids: `$this->helperService->sendAction($actionId, $val, $bot_id, null, 'friendList')`.
- Với allUser (> ngưỡng 200): Tạo `action_schedules` record để Spring Boot xử lý async — **DETECTED queue insert**.

**Response**: `{"success": true}`.

---

## 4. Error cases chung

| Status | Nguyên nhân | Response |
|--------|-------------|---------|
| 302 | Redirect `/login` nếu session hết hạn (middleware `basic_access`) | — |
| 302 | Redirect `/404` nếu `Conversation::getConversation` null (EP-01) | — |
| 302 | Redirect `/basic/chat-v3` nếu `bot_line_user` null (EP-01) | — |
| 200 | Catch Exception → `{"success": false, "msg": "..."}` | Hầu hết method đều có try-catch generic |
| 200 | Validation fail (EP-12, EP-22, EP-11 birthday) | `{"success": false, "errors"|"msg": ...}` |
| 500 | stopRemind exception (EP-20) | `{"success": false, "error": ..., "message": "登録できませんでした"}` |

---

## 5. Tổng hợp dấu hiệu queue/job

| Endpoint | Hành động → Queue | Consumer |
|----------|--------------------|---------|
| EP-01 (load) | INSERT `sync_elasticsearch` (update name) | Spring Boot ES sync |
| EP-07 (block) | DELETE `scenario_step_time` | Spring Boot scenario sender |
| EP-08 (delete) | INSERT `sync_elasticsearch` (delete_line_user) + DELETE `scenario_step_time` / `event_step_time` | Spring Boot ES + scheduler |
| EP-11 (save_custom_info) | INSERT `sync_elasticsearch` (update) + có thể INSERT `event_step_time` (birthday reminder) | Spring Boot |
| EP-16/17 (action_scenario_my_page) | INSERT `scenario_step_time` (status=0) khi change scenario | Spring Boot scenario sender |
| EP-19 (save-scenario) | Như EP-16/17 | Spring Boot |
| EP-20 (stopRemind) | DELETE `user_event` + cascade skip `event_step_time` | Spring Boot reminder sender |
| EP-21 (save_tag_line_user) | Có thể INSERT `action_schedules` / `scenario_step_time` khi tag có action_id | Spring Boot |
| EP-23 (remove-tag-line-user-my-page) | INSERT `sync_elasticsearch` (user_tag) | Spring Boot |
| EP-37 (send-action) | INSERT `action_schedules` khi allUser | Spring Boot action executor |
| EP-34 (save-rich-menu) | External LINE API | — |
| EP-08 (delete) | External LINE API (unlink rich menu) + Google Calendar API (delete event) | — |
