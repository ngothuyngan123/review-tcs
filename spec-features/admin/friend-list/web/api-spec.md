# FA-013 Danh sách bạn bè「友だちリスト」 — API Spec

> **Feature ID:** FA-013
> **Portal:** Admin
> **Controller chính:** `Basic\FriendlistController`
> **File:** `app/Http/Controllers/Basic/FriendlistController.php` (4329 dòng)
> **Ngày tạo:** 2026-03-25

---

## 1. Tổng quan Endpoints

| Mã | Method | URL | Mô tả | Controller@Method | Màn hình |
|----|--------|-----|--------|--------------------|----------|
| EP-01 | GET | `/basic/friendlist` | Trang chính danh sách bạn bè | `index` | SCR-FRL-01 |
| EP-02 | POST | `/basic/friendlist/post-advance-filter-v2` | Lọc nâng cao (v2) — trả JSON danh sách | `postFilterAdvance` | SCR-FRL-01, SCR-FRL-02 |
| EP-03 | GET | `/basic/friendlist/advance-filter` | Lọc nâng cao (v1 cũ) — trả JSON danh sách | `filterAdvance` | SCR-FRL-01 |
| EP-04 | POST | `/basic/friendlist/result_search` | Tìm kiếm bạn bè theo keyword | `searchLineUser` | SCR-FRL-01 |
| EP-05 | GET | `/basic/friendlist/sort` | Sắp xếp danh sách bạn bè | `sort` | SCR-FRL-01 |
| EP-06 | GET | `/basic/friendlist/my_page/{line_id}` | Trang chi tiết bạn bè | `mypage` | SCR-FRL-03 |
| EP-07 | GET | `/basic/friendlist/hidden` | Trang bạn bè đang ẩn | `hidden` | SCR-FRL-04 |
| EP-08 | POST | `/basic/friendlist/get-friend-hidden` | Lấy danh sách bạn bè đang ẩn (JSON) | `getFriendlistHiden` | SCR-FRL-04 |
| EP-09 | GET | `/basic/friendlist/user-block` | Trang bạn bè bị user block | `userBlock` | SCR-FRL-05 |
| EP-10 | POST | `/basic/friendlist/get-friend-user-block` | Lấy danh sách bạn bè bị user block (JSON) | `getFriendListUserBlock` | SCR-FRL-05 |
| EP-11 | GET | `/basic/friendlist/block` | Trang bạn bè bị admin block | `block` | SCR-FRL-06 |
| EP-12 | POST | `/basic/friendlist/get-friend-block` | Lấy danh sách bạn bè bị admin block (JSON) | `getFriendListBlock` | SCR-FRL-06 |
| EP-13 | POST | `/basic/friendlist/unblock-friend` | Bỏ block bạn bè (admin block) | `unblockFriend` | SCR-FRL-06 |
| EP-14 | POST | `/ajax/friendlist/delete-user-block` | Xoá 1 bạn bè (bất kỳ trang block/hidden) | `deleteUserBlock` | SCR-FRL-04/05/06 |
| EP-15 | POST | `/ajax/friendlist/delete-multiple-user-block` | Xoá hàng loạt bạn bè | `deleteUserBlockAction` | SCR-FRL-04/05/06 |
| EP-16 | POST | `/basic/friendlist/unhidden-friend` | Hiện lại bạn bè đang ẩn | `unHiddenFriend` | SCR-FRL-04 |
| EP-17 | POST | `/basic/friendlist/send-action` | Thực hiện bulk action (gọi action) | `sendActionFriend` | SCR-FRL-01 |
| EP-18 | POST | `/basic/friendlist/save-tag` | Gán tag hàng loạt | `saveTag` | SCR-FRL-01 |
| EP-19 | POST | `/basic/friendlist/remove-tag` | Gỡ tag hàng loạt | `removeTag` | SCR-FRL-01 |
| EP-20 | POST | `/basic/friendlist/setting-scenario` | Gán step scenario hàng loạt | `settingScenario` | SCR-FRL-01 |
| EP-21 | POST | `/basic/friendlist/save-rich-menu` | Gán rich menu hàng loạt | `saveRichMenu` | SCR-FRL-01 |
| EP-22 | POST | `/ajax/get-list-group-template-friendlist` | Lấy danh sách category + template | `ajaxGetListCategoryTemplate` | SCR-FRL-01 |
| EP-23 | POST | `/basic/friendlist/export` | Export CSV bạn bè | `csvExport` | SCR-FRL-01 |
| EP-24 | GET | `/basic/friendlist/download-csv` | Tải file CSV đã export | `downloadCsv` | SCR-FRL-01 |
| EP-25 | GET | `/basic/friendlist/import` | Trang import CSV | `getImportCSV` | SCR-FRL-01 |
| EP-26 | POST | `/basic/friendlist/read_file_csv` | Đọc file CSV upload | `readFileCsv` | SCR-FRL-01 |
| EP-27 | POST | `/basic/friendlist/save_file_csv` | Lưu dữ liệu từ CSV | `saveFileCsv` | SCR-FRL-01 |
| EP-28 | POST | `/basic/update_line_info` | Cập nhật thông tin bạn bè | `updateLineInfo` | SCR-FRL-03 |
| EP-29 | POST | `/basic/friendlist/my_page/save-scenario` | Lưu scenario cho bạn bè (mypage) | `saveScenario` | SCR-FRL-03 |
| EP-30 | POST | `/basic/friendlist/my_page/send-message` | Gửi tin nhắn cho bạn bè (mypage) | `sendMessage` | SCR-FRL-03 |
| EP-31 | POST | `/basic/line_users/block` | Block bạn bè (admin-side, 1 hoặc nhiều) | `updateLineUsersBlock` | SCR-FRL-03 |
| EP-32 | POST | `/ajax/get-bot-data` | Lấy dữ liệu bot hiện tại | `Admin\BotController@getBotData` | Chung |
| EP-33 | GET | `/basic/friend-list/basic-filter-friend` | Lọc bạn bè cơ bản (API service) | `basicFilterFriend` | SCR-FRL-01 |
| EP-34 | POST | `/ajax/remove-hide-friend` | Hiện lại 1 bạn bè ẩn (per-row) | `removeHideFriend` | SCR-FRL-04 |
| EP-35 | POST | `/basic/update_is_tester` | Đánh dấu bạn bè là tester | `updateIsTester` | SCR-FRL-03 |

### Middleware chung
Tất cả endpoints sử dụng middleware: `web`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`

---

## 2. Chi tiết từng Endpoint

### EP-01: GET `/basic/friendlist` — Trang chính danh sách bạn bè

**Mô tả:** Render view Blade trang chính `basic.friendlist.index`. Truyền dữ liệu ban đầu gồm richMenus, scenarios, conversions, totalFriend, statusObjects cho frontend Vue.

**Request params (query string):**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `tags_search` | query | string (CSV) | Không | Danh sách tag IDs phân cách bởi dấu phẩy |
| `scenario_search` | query | string (CSV) | Không | Danh sách scenario IDs |
| `conversion_search` | query | string (CSV) | Không | Danh sách conversion IDs |
| `checkbox_name` | query | string (CSV) | Không | Tên checkbox filter |
| `rich_menu_id` | query | int | Không | Lọc theo rich menu |
| `scenario_stop_id` | query | int | Không | Lọc theo scenario đang dừng |
| `scenario_id_running` | query | int | Không | Lọc theo scenario đang chạy |
| `scenario_unfinish_id` | query | int | Không | Lọc theo scenario chưa hoàn thành |
| `line_user_id_deleted` | query | int | Không | ID bạn bè vừa xoá (dùng cho UI notification) |

**Response:** HTML (Blade view `basic.friendlist.index`)

**Dữ liệu truyền sang view:**
- `richMenus`: Danh sách rich menu đang active (`status_rich = 1`)
- `totalFriend`: Tổng số bạn bè không bị block (`is_blocked = 0`)
- `get_scenario` / `scenario`: Danh sách scenario của bot
- `params_request`: Tham số filter hiện tại
- `conversion`: Danh sách conversion
- `statusObject`: Danh sách trạng thái chat tuỳ chỉnh
- `lineUserIdDeleted`: ID vừa xoá

**Tin cậy:** Cao — đọc trực tiếp từ source code :181-245

---

### EP-02: POST `/basic/friendlist/post-advance-filter-v2` — Lọc nâng cao v2

**Mô tả:** Endpoint lọc chính dùng cho trang friend list. Sử dụng `Conversation::advanceFilterPost()` với hệ thống filter AND/OR linh hoạt. Trả JSON phân trang (200 items/page).

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `item_search` | body | JSON string (array) | Không | Danh sách điều kiện AND — mỗi item có `type`, `active`, và data tuỳ thuộc type |
| `item_search_or` | body | JSON string (array) | Không | Danh sách điều kiện OR |
| `keyword` | body | string | Không | Từ khoá tìm kiếm (tên LINE, email, system name) |
| `sort_followed_at_increase` | body | string (asc/desc) | Không | Sắp xếp theo ngày thêm bạn bè |
| `sort_last_time_increase` | body | string (asc/desc) | Không | Sắp xếp theo tin nhắn mới nhất |
| `rich_menu_id` | body | int | Không | Lọc theo rich menu ID |
| `status_search` | body | int/string | Không | Lọc theo trạng thái xác nhận (0=未確認, 1=確認済み, hoặc custom status ID) |
| `followed_to` | body | string (date) | Không | Ngày thêm bạn bè — đến |
| `followed_from` | body | string (date) | Không | Ngày thêm bạn bè — từ |
| `scenario_stop_id` | body | int | Không | Lọc bạn bè có scenario đang dừng |
| `scenario_id_running` | body | int | Không | Lọc bạn bè có scenario đang chạy |
| `scenario_unfinish_id` | body | int | Không | Lọc bạn bè có scenario chưa hoàn thành |
| `line_user_id_deleted` | body | int | Không | Kiểm tra bạn bè vừa xoá |
| `is_cross` | body | string ("true"/"false") | Không | Bật chế độ cross analysis (bao gồm cả bạn bè bị block) |
| `connect_db_replicate` | body | boolean | Không | Dùng DB replica nếu có |

**Filter item types (trong `item_search` / `item_search_or`):**

| Type | Mô tả | Dữ liệu |
|------|-------|---------|
| `tag` | Lọc theo tag | `tag_id`, `condition` |
| `friend_name` | Lọc theo tên bạn bè | `keyword` |
| `day_add_friend` | Lọc theo ngày thêm | `modal_from_filter`, `modal_to_filter`, `day_filter_type`, `duration_day_start`, `duration_day_end` |
| `scenario` | Lọc theo step subscription | `scenario_id`, `condition` |
| `qr_code` / `qr_code_action` | Lọc theo QR code | `landing_id` |
| `conversion` | Lọc theo conversion | `conversion_id`, `condition` |
| `status_search` | Lọc theo trạng thái xác nhận | `status_search[]` |
| `friend_info` | Lọc theo thông tin tuỳ chỉnh | `friend_info_id`, `condition`, `value` |
| `affiliater` | Lọc theo affiliator | `affiliater_id` |
| `new_old_friend` | Lọc bạn bè mới/cũ | `friend_type` |
| `richmenu` | Lọc theo rich menu | `id[]` |

**Response thành công (200):**
```json
{
  "success": true,
  "data": {
    "current_page": 1,
    "data": [
      {
        "bot_line_id": 123,
        "followed_at": "2022-09-21 12:00:00",
        "line_id": 456,
        "is_blocked": 0,
        "link_my_page": "/basic/friendlist/my_page/456",
        "name": "テスト(Tan)",
        "email": "d1s@gmail.com",
        "view_name": "kin2",
        "avatar_url": "https://...",
        "conver_id": 789,
        "new_msg": "最新メッセージ内容",
        "msg_created_at": "2026-02-27 10:00:00",
        "scenario_action": 0,
        "scenario_name": ""
      }
    ],
    "per_page": 200,
    "total": 24,
    "last_page": 1
  }
}
```

**Lỗi có thể:**

| HTTP | Mô tả |
|------|-------|
| 200 | `{"success": false, "error": "message"}` — lỗi query hoặc exception |

**Tin cậy:** Cao — đọc trực tiếp từ source code :2918-3071

---

### EP-03: GET `/basic/friendlist/advance-filter` — Lọc nâng cao v1 (cũ)

**Mô tả:** Phiên bản cũ của lọc nâng cao, sử dụng `Conversation::advanceFilter()`. Vẫn hoạt động nhưng được thay thế bởi EP-02 v2. Phân trang 200 items/page.

**Request params (query string):** Tương tự EP-02 nhưng format khác — truyền `tags_search[]`, `scenario_search[]`, `conversion_search[]` dạng array objects thay vì JSON string.

**Response:** Tương tự EP-02 (`{"success": true, "data": paginated_results}`).

**Tin cậy:** Cao — :2829-2917

---

### EP-04: POST `/basic/friendlist/result_search` — Tìm kiếm bạn bè

**Mô tả:** Tìm kiếm bạn bè theo keyword (tên LINE). Trả view Blade `basic.friendlist.result_search`. Phân trang 50 items/page.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `keyword` | body | string | Không | Từ khoá tìm kiếm theo tên LINE (`line_user.name`) |
| `page` | query | int | Không | Trang hiện tại (mặc định 1) |

**Response:** HTML (Blade view `basic.friendlist.result_search`)

**Logic:**
- Join `bot_line_user` với `line_user` theo `line_user_id`
- Lọc `name LIKE '%keyword%'` và `is_blocked = 0`
- Lấy thêm số scenario đang follow và tin nhắn mới nhất (gọi stored procedure `SelectLastMessageByLineId`)
- Phân trang thủ công: offset + limit = 50

**Tin cậy:** Cao — :257-346

---

### EP-05: GET `/basic/friendlist/sort` — Sắp xếp danh sách

**Mô tả:** Sắp xếp danh sách bạn bè theo tiêu chí. Trả JSON.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `value` | query | int | Có | Loại sắp xếp: 1 = ngày thêm tăng dần, 2 = ngày thêm giảm dần, 3 = tin nhắn mới nhất giảm dần |
| `keyword` | query | string | Không | Từ khoá tìm kiếm kết hợp |

**Response (200):**
```json
{
  "bot_line_user": [
    {
      "b_id": 1,
      "line_user_id": 456,
      "followed_at": "2022-09-21",
      "is_blocked": 0,
      "bot_id": 1,
      "l_id": 456,
      "line_id": "Uf1234...",
      "name": "テスト",
      "status_message": "...",
      "avatar_url": "https://...",
      "content": "最新メッセージ",
      "created_at": "2026-02-27 10:00:00",
      "type": "text",
      "count": {"count": 0}
    }
  ]
}
```

**Tin cậy:** Cao — :348-557

---

### EP-06: GET `/basic/friendlist/my_page/{line_id}` — Chi tiết bạn bè

**Mô tả:** Trang chi tiết bạn bè. Hỗ trợ cả GET (render view) và AJAX request (trả JSON).

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `line_id` | path | int | Có | ID bạn bè trong bảng `line_user` |
| `action` | body (AJAX) | string | Không | `"list_message"` — lấy danh sách tin nhắn |
| `dipslay_message` | body (AJAX) | array | Không | Loại tin nhắn hiển thị |
| `page` | body (AJAX) | int | Không | Trang tin nhắn |

**Response GET:** HTML (Blade view `basic.friendlist.mypage_v2`) với dữ liệu:
- `line_info`: Thông tin bạn bè (join `line_user` + `bot_line_user`)
- `categorytags`: Danh sách tag theo category
- `special_status`: Trạng thái xác nhận tin nhắn (0/1/2+)
- `conversation`: Thông tin conversation

**Response AJAX (action=list_message):**
```json
{
  "success": true,
  "messages": [...]
}
```

**Response AJAX (khác):**
```json
{
  "success": true,
  "scenario": [...]
}
```

**Side effects:**
- Đồng bộ thông tin từ LINE server (tên, avatar) qua `BotController::getInfoFromLine()`
- Cập nhật `line_user` nếu tên thay đổi
- Ghi `SyncElasticsearch` nếu tên thay đổi và có `API_KEY_ES`

**Tin cậy:** Cao — :1609-1730

---

### EP-07: GET `/basic/friendlist/hidden` — Trang bạn bè ẩn

**Mô tả:** Render view `basic.friendlist.hidden`. Chỉ trả HTML, dữ liệu load qua AJAX (EP-08).

**Tin cậy:** Cao — :252-255

---

### EP-08: POST `/basic/friendlist/get-friend-hidden` — Lấy danh sách bạn bè ẩn

**Mô tả:** Trả JSON danh sách bạn bè đang ẩn (`is_hide = 1`), lọc theo khoảng thời gian.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `start_date` | body | string (date) | Không | Ngày bắt đầu lọc |
| `end_date` | body | string (date) | Không | Ngày kết thúc lọc |

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "line_id": "Uf1234...",
      "is_hide": 1,
      "datetime_hide": "2026/03/06 16:21:06",
      "name": "Tung テスト",
      "real_name": null,
      "avatar_url": "https://...",
      "view_name": "Tung",
      "bot_line_id": 123,
      "updated_at": "2026-03-06",
      "conver_id": 456
    }
  ],
  "botId": 1
}
```

**Logic:**
- Join `conversation` + `line_user` + `bot_line_user`
- Lọc `conversation.is_hide = 1`, `conversation_kind IN [0,1]`
- Lọc theo `datetime_hide` nếu có start_date/end_date
- Sắp xếp theo `datetime_hide` giảm dần

**Tin cậy:** Cao — :3120-3169

---

### EP-09: GET `/basic/friendlist/user-block` — Trang bạn bè bị user block

**Mô tả:** Render view `basic.friendlist.user_block`.

**Tin cậy:** Cao — :3084-3087

---

### EP-10: POST `/basic/friendlist/get-friend-user-block` — Lấy danh sách bạn bè bị user block

**Mô tả:** Trả JSON danh sách bạn bè bị user block (`is_blocked = 1, blocked_by = 0`). Phân trang 50 items/page.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `start_date` | body | string (date) | Không | Ngày bắt đầu lọc |
| `end_date` | body | string (date) | Không | Ngày kết thúc lọc |

**Response (200):**
```json
{
  "success": true,
  "data": {
    "current_page": 1,
    "data": [
      {
        "id": 1,
        "line_user_id": 456,
        "blocked_at": "2026-03-03 18:11:11",
        "avatar_url": "https://...",
        "name": "テスト",
        "view_name": "-"
      }
    ],
    "per_page": 50,
    "total": 3
  },
  "botId": 1
}
```

**Logic:**
- Join `conversation` + `line_user`
- Lọc `conversation.is_blocked = 1`, `conversation.blocked_by = 0` (0 = blocked bởi user)
- Sắp xếp theo `blocked_at` giảm dần

**Tin cậy:** Cao — :3089-3118

---

### EP-11: GET `/basic/friendlist/block` — Trang bạn bè bị admin block

**Mô tả:** Render view `basic.friendlist.block`.

**Tin cậy:** Cao — :247-250

---

### EP-12: POST `/basic/friendlist/get-friend-block` — Lấy danh sách bạn bè bị admin block

**Mô tả:** Trả JSON danh sách bạn bè bị admin block (`is_blocked = 1, blocked_by = 1`). Sử dụng `Conversation::getListFriendBlock()`.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `start_date` | body | string (date) | Không | Ngày bắt đầu lọc |
| `end_date` | body | string (date) | Không | Ngày kết thúc lọc |

**Response:** Array JSON (không phân trang):
```json
[
  {
    "id": 1,
    "name": "テスト",
    "real_name": null,
    "avatar_url": "https://...",
    "view_name": "Tung",
    "bot_line_id": 123,
    "updated_at": "2026-03-01",
    "blocked_at": "2026-03-01 12:00:00",
    "line_id": 456,
    "conver_id": 1,
    "followed_at": "2022-09-21",
    "link_my_page": "/basic/friendlist/my_page/456",
    "new_msg": "最新メッセージ",
    "msg_type": "text",
    "msg_created_at": "2026-02-27 10:00:00",
    "is_blocked": 1,
    "scenario_action": 0
  }
]
```

**Logic (Conversation::getListFriendBlock):**
- Join `conversation` + `line_user` + `bot_line_user`
- Lọc `bot_line_user.is_blocked = 1`, `conversation.is_blocked = 1`, `conversation.blocked_by = 1` (1 = admin block)
- `conversation_kind = 0` (1:1 conversation)
- Sắp xếp theo `blocked_at` giảm dần

**Tin cậy:** Cao — :3073-3082, Conversation.php:1698-1750

---

### EP-13: POST `/basic/friendlist/unblock-friend` — Bỏ block bạn bè

**Mô tả:** Bỏ block bạn bè bị admin block. Hỗ trợ nhiều bạn bè cùng lúc.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `listLineId` | body | array[int] | Có | Danh sách line_user IDs cần bỏ block |

**Response (200):** `{"success": true}`

**Response lỗi (500):** `{"success": false}`

**Logic & Side effects:**
1. Kiểm tra bạn bè còn follow trên LINE không (gọi LINE API `getProfile`)
2. Nếu còn follow → set `is_blocked = 0` trên `bot_line_user` và `conversation`, tạo message unblock trong `messages_v2s`
3. Nếu không còn follow → giữ `is_blocked = 1` (user đã block ở phía LINE)
4. Cập nhật `count_user_unconfirm` trên bảng `bots`
5. Gọi `updateBadge()` cập nhật badge

**Tin cậy:** Cao — :3170-3217

---

### EP-14: POST `/ajax/friendlist/delete-user-block` — Xoá 1 bạn bè

**Mô tả:** Xoá hoàn toàn 1 bạn bè khỏi hệ thống. Cascade delete toàn bộ dữ liệu liên quan.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | body | int | Có | line_user ID cần xoá |

**Response (200):** `{"success": true}`

**Response lỗi (500):** `{"success": false, "msg": "error message"}`

**Cascade delete (chi tiết tại logic-spec.md):**
- `bot_line_user`, `bot_line_user_item`, `conversation`, `scenario_lineuser`, `scenario_step_time`
- `tag_line_user`, `form_answer_result`, `user_open_formanswer`, `form_answer_user_accept`
- `b_booking` (event bookings), `calendar_salon_line_booking`, `calendar_course_booking`
- `event_step_time`, `user_event`, `friend_information_value`
- `bc_user_booking`, `order_history`, `cycle_order_history`, `mobile_notify`
- `url_shorten`, `url_shorten_detail`, `detail_url_click`, `detail_landing_click`
- `auto_reply_history`, `user_button`, `step_message_history`, `conversion_result`
- Unlink rich menu via LINE API
- Sync Elasticsearch delete
- Cập nhật thống kê: `bot_friend_statistic`, `landing`, `landing_history`, `scenario.count_*`, `tags.count_user_tag`, `status_chat.count`

**Tin cậy:** Cao — :3219-3617

---

### EP-15: POST `/ajax/friendlist/delete-multiple-user-block` — Xoá hàng loạt

**Mô tả:** Xoá hàng loạt bạn bè. Logic tương tự EP-14 nhưng lặp qua danh sách.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `line_user_id_list` | body | array[int] | Có | Danh sách line_user IDs cần xoá |

**Response:** Tương tự EP-14.

**Tin cậy:** Cao — :3618-4227

---

### EP-16: POST `/basic/friendlist/unhidden-friend` — Hiện lại bạn bè ẩn

**Mô tả:** Hiện lại bạn bè đang ẩn. Hỗ trợ 2 mode: đơn lẻ và hàng loạt.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `type` | body | int | Có | 1 = hàng loạt, khác = đơn lẻ |
| `listLineId` | body | string (JSON) hoặc string | Có | Nếu type=1: JSON array line_ids. Nếu khác: single line_id |

**Response (200):** `{"success": true}`

**Logic:**
- Set `conversation.is_hide = 0`, `conversation.datetime_hide = null`
- Sync Elasticsearch (`type: is_hide`)

**Tin cậy:** Cao — :4228-4275

---

### EP-17: POST `/basic/friendlist/send-action` — Thực hiện bulk action

**Mô tả:** Gọi action (từ hệ thống Action Settings) cho bạn bè đã chọn hoặc toàn bộ kết quả filter. Nếu > 200 bạn bè, tạo `ActionSchedule` để xử lý background.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `action_id` | body | int | Có | ID của action cần thực hiện |
| `searchIDs` | body | array/string | Không | Danh sách line_user IDs đã chọn |
| `allUser` | body | boolean | Không | `true` = áp dụng cho toàn bộ kết quả filter |
| `type_filter` | body | string | Không | `"old"` = dùng filter v1, khác = dùng filter v2 |
| `item_search` | body | JSON string | Không | Điều kiện filter AND (khi allUser=true) |
| `item_search_or` | body | JSON string | Không | Điều kiện filter OR |
| `keyword` | body | string | Không | Từ khoá tìm kiếm |
| (+ nhiều filter params khác) | | | | Tương tự EP-02 |

**Response (200):** `{"success": true}`

**Logic:**
- Nếu có `searchIDs` và không phải `allUser` → gọi `HelperService::sendAction()` cho từng user
- Nếu `allUser` và tổng > 200 → tạo `ActionSchedule` (tên: 「【自動生成】友だち一括アクション」), background job sẽ xử lý
- Nếu `allUser` và tổng <= 200 → gọi `sendAction()` trực tiếp

**Ghi chú job:** Khi tổng > 200 bạn bè, tạo record `action_schedules` → **Spring Boot job sẽ xử lý**. Cần kiểm tra thêm ở `/spec-job`.

**Tin cậy:** Cao — :863-1286

---

### EP-18: POST `/basic/friendlist/save-tag` — Gán tag hàng loạt

**Mô tả:** Gán tag cho bạn bè đã chọn hoặc toàn bộ kết quả filter.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `tag_id` | body | int | Có | ID tag cần gán |
| `searchIDs` | body | array[int] | Không | Danh sách line_user IDs |
| `allUser` | body | boolean | Không | `true` = áp dụng toàn bộ |
| `item_search` | body | JSON string | Không | Điều kiện AND |
| `item_search_or` | body | JSON string | Không | Điều kiện OR |
| `keyword` | body | string | Không | Từ khoá |

**Response (200):** `{"success": true}` hoặc `{"success": false}`

**Logic:**
- `updateOrCreate` bản ghi `tag_line_user` cho mỗi user
- Gọi helper function `addTags()` (có thể trigger scenario liên kết tag)

**Tin cậy:** Cao — :1287-1351

---

### EP-19: POST `/basic/friendlist/remove-tag` — Gỡ tag hàng loạt

**Mô tả:** Gỡ tag khỏi bạn bè đã chọn hoặc toàn bộ.

**Request params:** Tương tự EP-18.

**Logic:**
- Xoá record `tag_line_user` (hard delete)
- Giảm `tags.count_user_tag` cho mỗi user

**Tin cậy:** Cao — :1501-1569

---

### EP-20: POST `/basic/friendlist/setting-scenario` — Gán step scenario hàng loạt

**Mô tả:** Đăng ký step scenario cho bạn bè.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `scenario_id` | body | int | Có | ID scenario |
| `start_day` | body | int | Không | Ngày bắt đầu (offset) |
| `start_time` | body | string (HH:MM:SS) | Không | Giờ bắt đầu |
| `searchIDs` | body | array/string | Không | Danh sách IDs |
| `allUser` | body | boolean | Không | Toàn bộ |
| `item_search` | body | JSON string | Không | Điều kiện AND |
| `item_search_or` | body | JSON string | Không | Điều kiện OR |

**Response (200):** `{"success": true}` hoặc `{"success": false}`

**Logic:** Gọi `ChatHelper::changeScenario()` cho từng user.

**Tin cậy:** Cao — :813-862

---

### EP-21: POST `/basic/friendlist/save-rich-menu` — Gán rich menu hàng loạt

**Mô tả:** Thay đổi rich menu cho bạn bè. Gọi LINE API để link/unlink rich menu.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `rich_menu_id` | body | int | Có | ID rich menu (0 = reset về mặc định) |
| `searchIDs` | body | array[int] | Không | Danh sách IDs |
| `allUser` | body | boolean | Không | Toàn bộ |
| `item_search` | body | JSON string | Không | Điều kiện AND |
| `item_search_or` | body | JSON string | Không | Điều kiện OR |

**Response (200):** `{"success": true}` hoặc `{"success": false}`

**Side effects:** Gọi LINE API:
- `POST https://api.line.me/v2/bot/user/{lineId}/richmenu/{richMenuId}` — link rich menu
- `DELETE https://api.line.me/v2/bot/user/{lineId}/richmenu` — unlink rich menu

**Tin cậy:** Cao — :1353-1483

---

### EP-22: POST `/ajax/get-list-group-template-friendlist` — Lấy category + templates

**Mô tả:** Lấy danh sách category template (kind=2) và template chi tiết cho friend list.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `group_id` | body | int | Không | Category ID (0 = lấy category đầu tiên) |

**Response (200):**
```json
{
  "status": true,
  "groups": [...],
  "items": [...],
  "group_open": 0,
  "count_default": 5,
  "items_default": [...]
}
```

**Tin cậy:** Cao — :1571-1607

---

### EP-28: POST `/basic/update_line_info` — Cập nhật thông tin bạn bè

**Mô tả:** Cập nhật thông tin bạn bè (system name, real name, email, phone) từ trang chi tiết.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation |
|-----|--------|------|----------|-----------|
| `line_id` | body | int | Có | `nullable\|int` |
| `view_name` | body | string | Không | `nullable\|max:20` |
| `real_name` | body | string | Không | `nullable\|max:20` |
| `email` | body | string | Không | `nullable\|email` |
| `phone_number` | body | string | Không | `nullable\|regex:/(^\+?[0-9]{9,15}$)/u` |

**Response (200):** `{"success": true}` hoặc `{"success": false, "errors": {...}}`

**Logic:**
- Validate với custom messages (JP): `phone_number.regex → '9-15数字以内'`
- Chuyển đổi phone: `0xxx → +81xxx`
- Update `line_user` + `bot_line_user.phone_number`

**Tin cậy:** Cao — :1732-1773

---

### EP-31: POST `/basic/line_users/block` — Block bạn bè (admin-side)

**Mô tả:** Admin block 1 hoặc nhiều bạn bè. Dùng từ trang chi tiết hoặc bulk action.

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `conversationIds` | body | JSON string (array) | Có | Danh sách conversation IDs cần block |

**Response (200):** `{"success": true}`

**Logic:**
1. Set `bot_line_user.is_blocked = 1`
2. Set `conversation.is_blocked = 1`, `blocked_by = 1` (1 = admin), `blocked_at = now()`
3. Dừng tất cả scenario đang chạy cho user đó (`is_following = 0`)
4. Xoá `scenario_step_time` chưa gửi
5. Cập nhật `count_user_unconfirm`, gọi `updateBadge()`

**Tin cậy:** Cao — :1964-1991

---

### EP-33: GET `/basic/friend-list/basic-filter-friend` — Lọc bạn bè cơ bản

**Mô tả:** API lọc bạn bè cơ bản, delegate sang `BotLineUserService::getBasicAllFriend()`.

**Request params:** Tuỳ theo BotLineUserService.

**Response:** JSON từ service.

**Tin cậy:** Trung bình — chỉ thấy delegation, chưa đọc service chi tiết. :4302-4307

---

### EP-34: POST `/ajax/remove-hide-friend` — Hiện lại 1 bạn bè ẩn

**Mô tả:** Hiện lại 1 bạn bè ẩn (per-row action trên SCR-FRL-04).

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `lineUserId` | body | string/int | Có | line_user ID |

**Response (200):** `{"success": true}`

**Logic:** Set `conversation.is_hide = 0`, `datetime_hide = null`. Sync Elasticsearch.

**Tin cậy:** Cao — :4276-4300

---

### EP-35: POST `/basic/update_is_tester` — Đánh dấu tester

**Mô tả:** Đánh dấu bạn bè là tester (dùng cho testing).

**Request params:**

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `line_id` | body | int | Có | line_user ID |
| `is_tester` | body | int | Có | 0 hoặc 1 |

**Response (200):** `{"success": true, "is_tester": 1}`

**Tin cậy:** Cao — :1799-1814

---

## 3. Liên kết Endpoint ↔ Màn hình

| Màn hình | Endpoints sử dụng |
|----------|-------------------|
| SCR-FRL-01 (Danh sách chính) | EP-01, EP-02, EP-03, EP-04, EP-05, EP-17, EP-18, EP-19, EP-20, EP-21, EP-22, EP-23, EP-24, EP-25, EP-26, EP-27, EP-32, EP-33 |
| SCR-FRL-02 (Modal lọc nâng cao) | EP-02 (submit filter) |
| SCR-FRL-03 (Chi tiết bạn bè) | EP-06, EP-28, EP-29, EP-30, EP-31, EP-35 |
| SCR-FRL-04 (Bạn bè ẩn) | EP-07, EP-08, EP-14, EP-15, EP-16, EP-34 |
| SCR-FRL-05 (Bạn bè bị user block) | EP-09, EP-10, EP-14, EP-15 |
| SCR-FRL-06 (Bạn bè bị admin block) | EP-11, EP-12, EP-13, EP-14, EP-15 |
