# FA-003 Tự động trả lời「自動応答」— API Spec

> Phân tích từ source code Laravel (`src/web/`).
> Confidence: **Cao** — đọc trực tiếp từ code.

---

## Danh sách Endpoints

| EP | Method | URI | Controller@Action | Middleware | Mô tả |
|----|--------|-----|-------------------|-----------|-------|
| EP-01 | GET | `/basic/reply` | `Basic\ReplyController@index` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Hiển thị trang danh sách quy tắc tự động trả lời |
| EP-02 | GET | `/basic/reply/new` | `Basic\ReplyController@create` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Hiển thị form tạo mới quy tắc |
| EP-03 | GET | `/basic/reply/edit/{item_id}` | `Basic\ReplyController@edit` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Hiển thị form chỉnh sửa quy tắc |
| EP-04 | POST | `/basic/reply/store` | `Basic\ReplyController@store` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart, ... | Lưu quy tắc tự động trả lời mới (flow cũ - legacy) |
| EP-05 | POST | `/basic/reply/save` | `Basic\ReplyController@save` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart, ... | Cập nhật quy tắc đã tồn tại (flow cũ - legacy) |
| EP-06 | POST | `/ajax/get-list-group` | `Basic\ReplyController@ajaxGetListCategory` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Quản lý folder + lấy danh sách quy tắc (AJAX multi-action) |
| EP-07 | POST | `/ajax/init-data-detail-auto-reply` | `Basic\ReplyController@initDataDetailAutoReply` | web, NotifyChatworkRequestTimeSlow | Khởi tạo dữ liệu form tạo/sửa quy tắc (flow mới v2) |
| EP-08 | POST | `/ajax/save-data-detail-auto-reply` | `Basic\ReplyController@saveDataDetailAutoReply` | web, NotifyChatworkRequestTimeSlow | Lưu/cập nhật quy tắc tự động trả lời (flow mới v2) |
| EP-09 | POST | `/ajax/get-keyword-reply` | `Basic\ReplyController@ajaxGetKeywordReply` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy toàn bộ danh sách auto-reply kèm keyword |
| EP-10 | POST | `/ajax/get-list-template` | `Basic\ReplyController@ajaxGetTemplateCategory` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy danh sách template messages theo folder |
| EP-11 | POST | `/ajax/get-list-tags` | `Basic\ReplyController@ajaxGetTagsCategory` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy danh sách tags theo folder |
| EP-12 | GET | `/basic/reply/set-cookie` | `Basic\BasicController@folderSetCookie` | web, NotifyChatworkRequestTimeSlow | Lưu trạng thái folder đang mở vào cookie |
| EP-13 | POST | `/ajax/init-data-filter` | `Basic\FilterController@initDataFilter` | web, NotifyChatworkRequestTimeSlow | Khởi tạo dữ liệu cho modal lọc đối tượng (shared SC-003) |
| EP-14 | POST | `/ajax/get-bot-data` | `Admin\BotController@getBotData` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy thông tin bot/LINE OA (id, plan_type) |
| EP-15 | POST | `/ajax/filter/get-list-user` | `Basic\FilterController@ajaxGetListUserFilter` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Đếm/lấy danh sách bạn bè theo điều kiện lọc |
| EP-16 | POST | `/ajax/filter/save-filter-v2` | `Basic\FilterController@saveFilterV2` | web, NotifyChatworkRequestTimeSlow | Lưu điều kiện lọc (FilterV2) |

---

## Chi tiết Endpoints

### EP-01: GET `/basic/reply`
- **Controller**: `Basic\ReplyController@index`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:53`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Route Name**: `basicReply`
- **Mô tả**: Hiển thị trang danh sách quy tắc tự động trả lời. Đọc cookie `folder_reply` để xác định folder đang được chọn.
- **Liên kết UI**: SCR-RPL-01 → Trang danh sách tự động trả lời

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| (không có) | — | — | — | Dữ liệu danh sách được tải qua AJAX EP-06 | — |

#### Response
- **Kiểu**: Blade view `basic.reply.index`
- **Dữ liệu truyền vào view**:
  - `folderCookie` (int): ID folder đang được chọn (từ cookie), mặc định `0` (未分類)
- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:53-69`

---

### EP-02: GET `/basic/reply/new`
- **Controller**: `Basic\ReplyController@create`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:75`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Route Name**: `addItemReply`
- **Mô tả**: Hiển thị form tạo mới quy tắc tự động trả lời. Hỗ trợ sao chép (copy) từ quy tắc khác.
- **Liên kết UI**: SCR-RPL-02 → Form tạo mới

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `group_id` | Query | Integer | Không | ID folder để gán quy tắc mới, mặc định `0` | — |
| `reply_id` | Query | Integer | Không | ID quy tắc đang chỉnh sửa (dùng trong URL `/basic/reply/new?reply_id=X` — flow tạo mới kiểu cũ, kiểm tra tồn tại) | Phải tồn tại trong `auto_reply` với cùng `bot_id` |
| `copy_id` | Query | Integer | Không | ID quy tắc cần sao chép | — |

#### Response
- **Kiểu**: Blade view `basic.reply.create_v2`
- **Dữ liệu truyền vào view**:
  - `group` (Collection): Danh sách folders thuộc bot
  - `group_id` (int): ID folder đã chọn
  - `scenario` (Collection): Danh sách step delivery thuộc bot
  - `conversion` (array): Danh sách conversion (id, name) thuộc bot
  - `reply_id` (int|null): ID quy tắc nếu chỉnh sửa
  - `copy_id` (int|null): ID quy tắc nếu sao chép
  - `richMenus` (Collection): Danh sách Rich Menus đang hoạt động (`status_rich = 1`)
  - `statusObject` (Collection): Danh sách trạng thái đối ứng
  - `bot_id` (int): ID bot hiện tại
- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:75-110`

---

### EP-03: GET `/basic/reply/edit/{item_id}`
- **Controller**: `Basic\ReplyController@edit`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:231`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Route Name**: `editItemReply`
- **Mô tả**: Hiển thị form chỉnh sửa quy tắc (flow cũ — legacy, sử dụng view `basic.reply.edit`). Nếu quy tắc không tồn tại hoặc không thuộc bot hiện tại → redirect về `/basic/reply`.
- **Liên kết UI**: SCR-RPL-02 → Form chỉnh sửa (legacy flow)

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `item_id` | Path | Integer | Có | ID quy tắc cần chỉnh sửa | Phải tồn tại trong `auto_reply` với cùng `bot_id` |

#### Response
- **Kiểu**: Blade view `basic.reply.edit`
- **Redirect**: `/basic/reply` nếu quy tắc không tồn tại
- **Dữ liệu truyền**: `group`, `auto_reply`, `scenario`, `categories_template`, `items_template`, `items_default`, `items_add_tag`, `items_remove_tag`, `template_group`, `filter`
- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:231-279`

---

### EP-04: POST `/basic/reply/store`
- **Controller**: `Basic\ReplyController@store`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:116`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart, ...`
- **Route Name**: `storeItemReply`
- **Mô tả**: Tạo mới quy tắc tự động trả lời (flow legacy — form POST truyền thống). Kiểm tra backup đang chạy, validate, insert vào `auto_reply`, tạo keywords nếu có, tạo filter.
- **Liên kết UI**: SCR-RPL-02 → Nút「登録」(flow cũ)

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `group_id` | Body | Integer | Có | ID folder (category) | — |
| `type` | Body | Integer | Có | Loại trigger: `0` = keyword, `1` = time | `trigger_kind` config |
| `rule_mix` | Body | Integer | Có | Logic keyword: `0` = AND, `1` = OR | — |
| `step_to_change` | Body | Integer | Không | Loại scenario: `0` = emergency, `1` = timer | — |
| `is_active` | Body | Integer | Có | Trạng thái hoạt động: `0` = bật, `1` = tắt | `item_is_stopped` config |
| `only_once` | Body | Integer | Có | Số lần phản ứng: `0` = chỉ 1 lần, `1` = nhiều lần | `response_number` config |
| `use_reply` | Body | Integer | Có | Loại phản hồi: `0` = none, `1` = text, `2` = template | `use_reply` config |
| `step_to_id` | Body | Integer | Không | ID scenario (step delivery) cần chuyển | — |
| `reply` | Body | String | Có (khi `use_reply=1`) | Nội dung text phản hồi. Tối đa 5000 ký tự | max 5000 chars (UTF-8) |
| `egg_id` | Body | Integer | Có (khi `use_reply=2`) | ID template message phản hồi | — |
| `step_to_date` | Body | Integer | Không | Ngày delay (khi `scenario_type=timer`) | — |
| `step_to_time` | Body | String | Không | Giờ delay (khi `scenario_type=timer`) | — |
| `add_tag_ids` | Body | String | Không | Danh sách ID tags cần gán, phân cách bằng dấu `,` | — |
| `remove_tag_ids` | Body | String | Không | Danh sách ID tags cần gỡ | — |
| `week[]` | Body | Array | Có (khi `type=1`) | Danh sách ngày trong tuần (0-6 hoặc string) | Tối thiểu 1 ngày |
| `hour_from` | Body | String | Có (khi `type=1`) | Giờ bắt đầu, format `H:i` | Regex `HH:mm` |
| `hour_to` | Body | String | Có (khi `type=1`) | Giờ kết thúc, format `H:i` | Regex `HH:mm`, phải > hour_from |
| `rword[]` | Body | Array | Có (khi `type=0`) | Danh sách keyword | Tối thiểu 1 keyword, không trùng trong bot |
| `rmatch_type[]` | Body | Array | Có (khi `type=0`) | Loại so khớp cho mỗi keyword (index tương ứng) | — |
| `name_filter`, `tag_filter`, ... | Body | Mixed | Không | Dữ liệu filter (legacy) — xem Filter model | — |

#### Response (thành công)
- **Kiểu**: Redirect back with flash `success`
- **Message**: `'登録しました。'`

#### Response lỗi
| HTTP Code | Điều kiện | Response |
|-----------|----------|----------|
| 302 | Validation thất bại (thiếu keyword/time) | Redirect back với flash `errors` (mảng message tiếng Nhật) |
| 302 | Keyword đã tồn tại trong bot | Redirect back: `'キーワードは既に登録されています。'` |
| 500 | Bot đang trong quá trình backup | JSON `{"success": false, "message": MESSAGE_NOTIFY_BACKUP}` |
| 302 | Exception | Redirect back: `'Server Occured!'` |

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:116-225`

---

### EP-05: POST `/basic/reply/save`
- **Controller**: `Basic\ReplyController@save`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:285`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart, ...`
- **Route Name**: `saveItemReply`
- **Mô tả**: Cập nhật quy tắc đã tồn tại (flow legacy). Tương tự EP-04 nhưng update thay vì insert.
- **Liên kết UI**: SCR-RPL-02 → Nút「登録」khi chỉnh sửa (flow cũ)

#### Request Parameters
Giống EP-04, thêm:

| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `item_id` | Body | Integer | Có | ID quy tắc cần cập nhật | Phải tồn tại trong `auto_reply` |

#### Response
Giống EP-04.

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:285-429`

---

### EP-06: POST `/ajax/get-list-group`
- **Controller**: `Basic\ReplyController@ajaxGetListCategory`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:435`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Route Name**: `ajaxGetListCategory`
- **Mô tả**: Endpoint AJAX đa năng — xử lý nhiều hành động khác nhau dựa trên param `action`. Quản lý folder, bật/tắt quy tắc, xóa, sắp xếp, di chuyển, tìm kiếm.
- **Liên kết UI**: SCR-RPL-01 → Toàn bộ thao tác trên danh sách

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `action` | Body | String | Có | Tên hành động cần thực hiện (xem bảng actions bên dưới) | — |
| `group_id` | Body | Integer | Tuỳ action | ID folder hiện tại | — |

#### Các actions hỗ trợ

| Action | Params bổ sung | Mô tả |
|--------|---------------|-------|
| `addAndEditGroup` | `id` (int), `group_name` (string) | Tạo mới hoặc đổi tên folder. Nếu `id` tồn tại → rename, nếu không → create |
| `deleteGroup` | `group_id` (int) | Xóa folder (soft delete `is_deleted=1`) + xóa tất cả quy tắc trong folder + xóa keywords |
| `renameGroup` | `group_id` (int), `group_name` (string) | Đổi tên folder |
| `turnOnItem` | `item_id` (int) | Bật quy tắc (`is_stopped = 0`) |
| `turnOffItem` | `item_id` (int) | Tắt quy tắc (`is_stopped = 1`) |
| `searchByKeyWord` | `keyword` (string), `group_id` (int) | Tìm kiếm quy tắc theo keyword trong folder |
| `deleteItem` | `item_id` (int) | Xóa 1 quy tắc (soft delete `is_deleted=1`) + xóa keywords |
| `deleteItems` | `item_ids` (array[int]) | Xóa nhiều quy tắc (bulk delete) + xóa keywords |
| `sortItem` | `sort_ids` (string, CSV), `sort_position` (string, CSV) | Sắp xếp lại thứ tự quy tắc (kéo thả) |
| `moveItem` | `item_ids` (array[int]), `folder_move_id` (int) | Di chuyển nhiều quy tắc sang folder khác |
| `sortFolder` | `sort_ids` (string, CSV), `sort_position` (string, CSV) | Sắp xếp lại thứ tự folders |

#### Response mẫu (thành công)
```json
{
  "status": true,
  "groups": [
    {
      "id": 1,
      "name": "Folder A",
      "bot_id": 123,
      "kind": 1,
      "position": 1,
      "items_count": 5
    }
  ],
  "items_default": [
    {
      "id": 10,
      "keyword": "こんにちは",
      "group_name": "未分類",
      "day_of_week": "月,火,水",
      "time": "09:00~18:00",
      "trigger_kind": 0,
      "logical": 0,
      "reply_kind": 1,
      "reply_content": "ようこそ",
      "position": 1,
      "is_stopped": 0,
      "created_at": "2024.01.15",
      "keyword_reaction_type": 0,
      "time_reaction_type": 0,
      "action_id": 5,
      "filter_preview_content": null
    }
  ],
  "items": [],
  "group_open": 0,
  "count_default": 3
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response |
|-----------|----------|----------|
| 500 | Bot đang backup (cho các action modify) | `{"success": false, "msg": MESSAGE_NOTIFY_BACKUP}` |
| 200 | Exception | `{"status": false, "msg": "error message"}` |

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:435-690`

---

### EP-07: POST `/ajax/init-data-detail-auto-reply`
- **Controller**: `Basic\ReplyController@initDataDetailAutoReply`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:831`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Route Name**: `reply.init_data_detail_auto_reply`
- **Mô tả**: Khởi tạo dữ liệu cho form tạo/sửa/sao chép quy tắc (flow v2). Trả về dữ liệu quy tắc, danh sách keyword, chi tiết action.
- **Liên kết UI**: SCR-RPL-02 → Load dữ liệu khi vào form tạo/sửa

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `id` | Body | Integer | Không | ID quy tắc cần load (chỉnh sửa) | — |
| `copyId` | Body | Integer | Không | ID quy tắc cần sao chép | — |
| `category_id` | Body | Integer | Không | ID folder mặc định khi tạo mới | — |

#### Response mẫu (thành công — tạo mới)
```json
{
  "success": true,
  "data_reply": {
    "keyword_reaction_type": 0,
    "logical": 0,
    "time_reaction_type": 0,
    "response_number": 0,
    "action_id": null,
    "category_id": 0,
    "start_time": null,
    "end_time": null,
    "day_of_week": [],
    "is_no_reply_button": false
  },
  "list_keyword": [
    {
      "id": null,
      "keyword": "",
      "logical": 0
    }
  ],
  "detail_action_reply": []
}
```

#### Response mẫu (thành công — chỉnh sửa)
```json
{
  "success": true,
  "data_reply": {
    "is_apply_active_friend": 1,
    "keyword_reaction_type": 1,
    "logical": 0,
    "time_reaction_type": 0,
    "response_number": 1,
    "action_id": 45,
    "category_id": 3,
    "start_time": "09:00",
    "end_time": "18:00",
    "day_of_week": ["1", "2", "3", "4", "5"],
    "is_no_reply_button": false
  },
  "list_keyword": [
    {
      "id": 12,
      "keyword": "こんにちは",
      "logical": 0
    }
  ],
  "detail_action_reply": [
    {
      "id": 100,
      "action_id": 45,
      "type": "template",
      "data": { "id": 88, "template_name": "挨拶メッセージ" },
      "active": false
    }
  ]
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response |
|-----------|----------|----------|
| 200 | Quy tắc không tồn tại (reply_id hoặc copy_id) | `{"success": false, "redirect": "/basic/reply"}` |
| 200 | Exception | `{"success": false}` |

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:831-927`

---

### EP-08: POST `/ajax/save-data-detail-auto-reply`
- **Controller**: `Basic\ReplyController@saveDataDetailAutoReply`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:929`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Route Name**: `reply.save_data_detail_auto_reply`
- **Mô tả**: Lưu/cập nhật quy tắc tự động trả lời (flow v2 — AJAX). Xử lý tạo mới hoặc cập nhật dựa trên `id`. Kiểm tra keyword trùng, validate thời gian, lưu FilterV2.
- **Liên kết UI**: SCR-RPL-02 → Nút「登録」(flow v2)

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `id` | Body | Integer | Không | ID quy tắc (nếu update). Null = tạo mới | — |
| `copy_id` | Body | Integer | Không | ID quy tắc nguồn (sao chép) | — |
| `botIdCurrent` | Body | Integer | Có | ID bot tại thời điểm mở trang (kiểm tra chưa đổi bot) | Phải = bot hiện tại |
| `data_reply` | Body | JSON string | Có | Dữ liệu quy tắc (xem bảng dưới) | — |
| `list_keyword` | Body | JSON string | Có (khi keyword mode) | Mảng keyword objects `[{id, keyword, logical}]` | Tối thiểu 1 keyword nếu `keyword_reaction_type=1` |
| `item_search` | Body | JSON string | Không | Mảng điều kiện lọc AND (FilterV2) | — |
| `item_search_or` | Body | JSON string | Không | Mảng điều kiện lọc OR (FilterV2) | — |

**Cấu trúc `data_reply` (JSON):**

| Field | Kiểu | Mô tả |
|-------|------|-------|
| `category_id` | int | ID folder |
| `keyword_reaction_type` | int | `0` = phản ứng tất cả, `1` = phản ứng theo keyword đã cài |
| `logical` | int | Logic keyword: `0` = AND, `1` = OR |
| `time_reaction_type` | int | `0` = luôn phản ứng (24/7), `1` = theo lịch trình |
| `response_number` | int | `0` = chỉ 1 lần, `1` = nhiều lần |
| `action_id` | int\|null | ID action (từ bảng `t_actions`) |
| `is_apply_active_friend` | int | `1` = áp dụng bạn bè đang hoạt động, `0` = bạn bè đã block |
| `is_no_reply_button` | bool | `true` = không phản ứng với tin nhắn từ nút reply. Đây là checkbox「〇〇のメッセージには反応させない」|
| `start_time` | string\|null | Giờ bắt đầu `HH:mm` (khi `time_reaction_type=1`) |
| `end_time` | string\|null | Giờ kết thúc `HH:mm` (khi `time_reaction_type=1`) |
| `day_of_week` | array[string] | Mảng ngày trong tuần (khi `time_reaction_type=1`) |

#### Response mẫu (thành công)
```json
{
  "success": true,
  "msg": ""
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response |
|-----------|----------|----------|
| 200 | Bot khác với bot đang mở trang | `{"success": false, "msg": "別のアカウントに切り替えたので、要求を処理できません。"}` |
| 500 | Bot đang backup | `{"success": false, "msg": MESSAGE_NOTIFY_BACKUP}` |
| 200 | Thiếu keyword | `{"success": false, "msg1": "キーワードを1つ以上設定して下さい。", "msg2": ""}` |
| 200 | Thời gian không hợp lệ | `{"success": false, "msg1": "", "msg2": "時間帯を正しく指定して下さい。"}` |
| 200 | Keyword đã tồn tại | `{"success": false, "msg": "キーワードは既に登録されています。", "arraySameWord": [0, 2]}` |
| 200 | Exception | `{"success": false, "msg": "error message"}` |

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:929-1083`

---

### EP-09: POST `/ajax/get-keyword-reply`
- **Controller**: `Basic\ReplyController@ajaxGetKeywordReply`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:806`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lấy toàn bộ danh sách auto-reply chưa bị xóa kèm keyword. Dùng cho mục đích kiểm tra keyword trùng hoặc hiển thị tổng quan.
- **Liên kết UI**: SCR-RPL-01 hoặc nội bộ (kiểm tra trùng keyword)

#### Request Parameters
Không có (chỉ dùng `bot_id` từ session).

#### Response mẫu
```json
{
  "status": true,
  "reply": [
    {
      "id": 1,
      "bot_id": 123,
      "category_id": 0,
      "trigger_kind": 0,
      "logical": 0,
      "is_stopped": 0,
      "reply_kind": 1,
      "reply_content": "decoded text content",
      "keyword": [
        { "id": 1, "auto_reply_id": 1, "keyword": "こんにちは", "logical": 0 }
      ]
    }
  ]
}
```

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:806-829`

---

### EP-10: POST `/ajax/get-list-template`
- **Controller**: `Basic\ReplyController@ajaxGetTemplateCategory`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:696`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Route Name**: `ajaxGetTemplateCategory`
- **Mô tả**: Lấy danh sách template messages phân theo folder. Dùng cho dropdown chọn template trong form tạo/sửa.
- **Liên kết UI**: SCR-RPL-02 → Chọn template phản hồi (flow cũ)

#### Response mẫu
```json
{
  "status": true,
  "groups": [ { "id": 1, "name": "Folder Template A" } ],
  "items": [ [ { "id": 10, "name": "Greeting", "type": "text" } ] ],
  "items_default": [ { "id": 20, "name": "Default Template" } ]
}
```

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:696-719`

---

### EP-11: POST `/ajax/get-list-tags`
- **Controller**: `Basic\ReplyController@ajaxGetTagsCategory`
- **File**: `app/Http/Controllers/Basic/ReplyController.php:725`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Route Name**: `ajaxGetTagsCategory`
- **Mô tả**: Lấy danh sách tags phân theo folder. Dùng cho chọn tag gán/gỡ trong form tạo/sửa.
- **Liên kết UI**: SCR-RPL-02 → Chọn tag (flow cũ)

#### Response mẫu
```json
{
  "status": true,
  "groups": [ { "id": 1, "name": "Tag Folder A" } ],
  "items": [ [ { "id": 5, "name": "VIP", "bot_id": 123 } ] ],
  "items_default": [ { "id": 10, "name": "Default Tag" } ],
  "group_open": 0,
  "count_default": 3
}
```

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/ReplyController.php:725-753`

---

### EP-12: GET `/basic/reply/set-cookie`
- **Controller**: `Basic\BasicController@folderSetCookie`
- **File**: `app/Http/Controllers/Basic/BasicController.php:1900`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Route Name**: `replySetCookie`
- **Mô tả**: Lưu folder đang mở vào cookie `folder_reply`. Cookie có thời hạn 14400 phút (10 ngày). Dùng khi người dùng click chọn folder trong sidebar.
- **Liên kết UI**: SCR-RPL-01 → Click folder trong sidebar

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `folder_id` | Query | Integer | Có | ID folder cần lưu | — |
| `type` | Query | String | Có | Loại cookie: `"reply"` | — |

#### Response
- **Kiểu**: Empty response with `Set-Cookie` header
- **Cookie**: `folder_reply` = JSON `{bot_id: folder_id}`, path `/basic/reply`, 14400 phút

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/BasicController.php:1900-1940`

---

### EP-13: POST `/ajax/init-data-filter`
- **Controller**: `Basic\FilterController@initDataFilter`
- **File**: `app/Http/Controllers/Basic/FilterController.php:290`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Route Name**: `initDataFilter`
- **Mô tả**: Khởi tạo dữ liệu cho modal lọc đối tượng (shared component SC-003). Trả về danh sách điều kiện AND/OR đã lưu, cùng dữ liệu phụ trợ (tags, scenarios, conversions, QR codes...).
- **Liên kết UI**: SCR-RPL-03 → Modal lọc đối tượng「絞り込み」

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `parent_id` | Body | Integer | Có | ID đối tượng cha (auto_reply ID) | — |
| `parent_type` | Body | String | Có | Loại đối tượng cha: `"auto_reply"` | — |
| `copy_id` | Body | Integer | Không | ID nếu đang sao chép | — |
| `richMenuRedirectId` | Body | Integer | Không | ID rich menu redirect (không áp dụng cho auto-reply) | — |
| `richMenuItemId` | Body | Integer | Không | ID rich menu item (không áp dụng cho auto-reply) | — |

#### Response mẫu
```json
{
  "success": true,
  "data": {
    "itemFilterAnd": [
      {
        "id": 5,
        "type": "tag",
        "preview": "タグ: VIP",
        "tags_search": [1, 2],
        "list_tags": [{"id": 1, "name": "VIP"}]
      }
    ],
    "itemFilterOr": [],
    "numberFilter": 1
  }
}
```

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/FilterController.php:290-500+` (đọc đoạn đầu)

---

### EP-14: POST `/ajax/get-bot-data`
- **Controller**: `Admin\BotController@getBotData`
- **File**: `app/Http/Controllers/Admin/BotController.php:11337`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Mô tả**: Lấy thông tin cơ bản của bot — `id` và `plan_type`. Dùng để kiểm tra loại gói dịch vụ (ảnh hưởng đến tính năng khả dụng).
- **Liên kết UI**: SCR-RPL-02 → Load khi vào form để kiểm tra plan

#### Request Parameters
Không có (dùng `bot_id` từ session).

#### Response mẫu
```json
{
  "id": 123,
  "plan_type": 1
}
```

- **Tin cậy**: **Cao** — `app/Http/Controllers/Admin/BotController.php:11337-11342`

---

### EP-15: POST `/ajax/filter/get-list-user`
- **Controller**: `Basic\FilterController@ajaxGetListUserFilter`
- **File**: `app/Http/Controllers/Basic/FilterController.php:41`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow, LogRequestMultipart`
- **Route Name**: `ajaxGetListUserFilter`
- **Mô tả**: Lấy danh sách hoặc đếm số bạn bè phù hợp điều kiện lọc. Dùng cho hiển thị「対象人数」(số người phù hợp) trong form tạo/sửa.
- **Liên kết UI**: SCR-RPL-02 → Hiển thị「対象人数」

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `name_filter` | Body | String | Không | Tên bạn bè cần lọc | — |
| `name_filter_type` | Body | String | Không | Loại lọc tên (name/real_name/view_name) | — |
| `tag_filter` | Body | String | Không | Danh sách tag IDs, phân cách `,` | — |
| `tag_filter_option` | Body | String | Không | Logic tag: AND/OR | — |
| (+ các filter khác) | Body | Mixed | Không | Xem FilterController | — |

- **Tin cậy**: **Cao** — `app/Http/Controllers/Basic/FilterController.php:41-290`

---

### EP-16: POST `/ajax/filter/save-filter-v2`
- **Controller**: `Basic\FilterController@saveFilterV2`
- **File**: `app/Http/Controllers/Basic/FilterController.php`
- **Middleware**: `web, NotifyChatworkRequestTimeSlow`
- **Route Name**: `save_filter_v2`
- **Mô tả**: Lưu điều kiện lọc FilterV2 (shared component SC-003). Được gọi khi nhấn「保存」trong modal lọc.
- **Liên kết UI**: SCR-RPL-03 → Nút「保存」trong modal filter

- **Tin cậy**: **Trung bình** — route xác nhận từ index, chưa đọc chi tiết method body

---

## Middleware phân tích

| Middleware | Mô tả | Áp dụng cho |
|-----------|-------|------------|
| `web` | Session, CSRF, cookies — middleware group chuẩn Laravel | Tất cả EP |
| `NotifyChatworkRequestTimeSlow` | Ghi log cảnh báo nếu request xử lý chậm (gửi thông báo Chatwork) | Tất cả EP |
| `LogRequestMultipart` | Ghi log request multipart (upload file) | EP-01~06, EP-09~12, EP-14~15 |

> **Ghi chú**: Không phát hiện middleware kiểm tra quyền (authorization) riêng cho tính năng auto-reply. Xác thực dựa trên session chung của web middleware group (user đã login). Kiểm tra `bot_id` qua helper `getBotId()` từ session. **Tin cậy**: Cao.

---

## Ghi chú hai flow (Legacy vs V2)

Tính năng tự động trả lời có **2 flow song song**:

### Flow Legacy (form POST truyền thống)
- **Tạo**: EP-02 (view create_v2) → EP-04 (store via form POST)
- **Sửa**: EP-03 (view edit) → EP-05 (save via form POST)
- **Dữ liệu filter**: Sử dụng model `Filter` (bảng `filters`)
- **Đặc điểm**: Form submit truyền thống, redirect back

### Flow V2 (AJAX)
- **Init data**: EP-07 (initDataDetailAutoReply)
- **Lưu**: EP-08 (saveDataDetailAutoReply)
- **Dữ liệu filter**: Sử dụng model `FilterV2` (bảng `filters_v2`)
- **Đặc điểm**: Full AJAX, không reload trang, hỗ trợ copy, sử dụng Action Settings (SC-004)

> **Suy luận**: Flow V2 là flow hiện tại đang được sử dụng (view `create_v2`), flow Legacy vẫn tồn tại trong code nhưng có thể không còn được sử dụng trên giao diện mới. **Tin cậy**: Trung bình.

---

## Liên kết UI ↔ API

| Màn hình | Action | Endpoint | Ghi chú |
|---------|--------|----------|---------|
| SCR-RPL-01 | Load danh sách | EP-06 (action: mặc định) | Tải danh sách quy tắc + folders |
| SCR-RPL-01 | Chọn folder sidebar | EP-12 (set-cookie) + EP-06 | Lưu cookie → tải lại danh sách |
| SCR-RPL-01 | Bật/tắt quy tắc | EP-06 (action: turnOnItem/turnOffItem) | Toggle trạng thái |
| SCR-RPL-01 | Xóa 1 quy tắc | EP-06 (action: deleteItem) | Soft delete |
| SCR-RPL-01 | Xóa nhiều quy tắc | EP-06 (action: deleteItems) | Bulk soft delete |
| SCR-RPL-01 | Sắp xếp | EP-06 (action: sortItem) | Kéo thả |
| SCR-RPL-01 | Di chuyển folder | EP-06 (action: moveItem) | Bulk move |
| SCR-RPL-01 | Tìm kiếm | EP-06 (action: searchByKeyWord) | Tìm theo keyword |
| SCR-RPL-01 | Tạo/sửa/xóa folder | EP-06 (action: addAndEditGroup/renameGroup/deleteGroup) | CRUD folder |
| SCR-RPL-01 | Click「新規作成」| EP-02 | Navigate đến form tạo mới |
| SCR-RPL-02 | Load form data | EP-07 + EP-14 | Init data quy tắc + init data bot |
| SCR-RPL-02 | Lưu quy tắc | EP-08 | AJAX save (flow v2) |
| SCR-RPL-02 | Lấy templates | EP-10 | Dropdown chọn template (flow cũ) |
| SCR-RPL-02 | Lấy tags | EP-11 | Dropdown chọn tag (flow cũ) |
| SCR-RPL-02 |「対象人数」| EP-15 | Đếm số bạn bè phù hợp filter |
| SCR-RPL-03 | Load filter data | EP-13 | Init modal lọc đối tượng |
| SCR-RPL-03 |「保存」| EP-16 | Lưu điều kiện lọc |
| SCR-RPL-04 | (Action Settings) | Shared SC-004 | Action được lưu qua bảng `t_actions` + `t_actions_detail` |
