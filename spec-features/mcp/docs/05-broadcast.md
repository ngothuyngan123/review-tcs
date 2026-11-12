# Broadcast Message Tools

Doc gộp toàn bộ tool broadcast (P3.5 tool-consolidation 2026-09-16): **`list_broadcasts`**,
**`list_broadcast_templates`**, **`create_broadcast`**, **`update_broadcast`**. Upload ảnh dùng cho
template: **`get_file_params`** — xem [11-chat.md](11-chat.md).

> **Lịch sử hợp nhất:** các tool broadcast cũ đã bị GỠ khỏi MCP, thay bằng `create_broadcast` (tạo) +
> `update_broadcast` (sửa — merged updater) + `update_filter(target=broadcast)` (sửa filter, REPLACE-ALL):
> `edit_broadcast_info`, `add_broadcast_template`, `edit_broadcast_template`, `edit_broadcast_filters`,
> `edit_broadcast_action`, `add_broadcast_schedule`; `delete_broadcast_template` (xoá template qua web admin).
> Toàn bộ `guide_broadcast_*` cũng đã disable — nội dung distill vào description + typed schema của tool.

Bố cục: **Read tools** (`list_broadcasts`, `list_broadcast_templates`) → **`create_broadcast`** (full spec:
template types, filter types, action, sample) → **`update_broadcast`**.

---

## list_broadcasts

**Description:** Tool trả về danh sách broadcast bao gồm thông tin cơ bản, nội dung gửi, điều kiện lọc và thống kê. Bắt
buộc truyền khoảng ngày (tối đa 3 tháng). Khi người dùng muốn EDIT broadcast, gọi tool này trước để resolve
`broadcast_id` theo tên/ngày/trạng thái — nếu nhiều kết quả khớp, liệt kê ra (id + name + status + send_day +
created_at) và hỏi người dùng chọn; không tự chọn.

**Tool:** `list_broadcasts`

**Input:**
| Name | Type | Required | Description |
|----------------|---------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool
`list_bots`                                                                                                         |
| from_date | String | Yes | Ngày bắt đầu (bắt buộc, format: `yyyy-MM-dd`). Tối đa 3 tháng từ
`to_date`                                                                       |
| to_date | String | Yes | Ngày kết thúc (bắt buộc, format: `yyyy-MM-dd`). Tối đa 3 tháng từ
`from_date`                                                                     |
| page | Integer | No | Số trang (default:
1)                                                                                                                              |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100)                                                                            |
| name | String | No | Lọc theo tên broadcast, tìm kiếm partial (LIKE `%value%`, case-INsensitive — xác nhận qua test BC-14/BC-15 ngày 2026-09-21, đóng C3/V3-3). Dùng để resolve
`broadcast_id` khi user nhắc tên |
| status | String | No | Lọc theo trạng thái logic: `draft` (=draft,unregistered) / `scheduled` (
=wait_to_send,delivering) / `sent` (=delivered,not_delivery,send_false). Dùng `draft` để tìm broadcast còn chỉnh sửa
được |
| send_day | String | No | Lọc EXACT theo ngày gửi (format:
`yyyy-MM-dd`)                                                                                                     |
| created_after | String | No | Lọc broadcast có `created_at >=` value (format: `yyyy-MM-dd HH:mm:ss` hoặc
`yyyy-MM-dd`)                                                          |
| created_before | String | No | Lọc broadcast có `created_at <=` value (format: `yyyy-MM-dd HH:mm:ss` hoặc
`yyyy-MM-dd`)                                                          |

**Output:**
| Name | Type | Description |
|------------|-------------|-----------------------------------|
| broadcasts | Json Array | Danh sách object Broadcast |
| pagination | Json Object | Thông tin phân trang |

**Sub Object Broadcast:**
| Name | Type | Description |
|----------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id | Long | ID của broadcast |
| name | String | Tên broadcast |
| status | String | Trạng thái DB: `draft` / `unregistered` / `wait_to_send` / `delivering` / `delivered` /
`not_delivery` / `send_false`                                              |
| send_day | String | Ngày gửi (format:
`yyyy-MM-dd`)                                                                                                                                      |
| send_time | String | Giờ gửi (format:
`HH:mm:ss`)                                                                                                                                         |
| send_count | Integer | Số message đã gửi (null nếu chưa
gửi)                                                                                                                               |
| template_count | Integer | Số lượng template trong broadcast |
| action_id | Long | ID của action group gắn với broadcast (null nếu không
có)                                                                                                            |
| templates | Json Array | Danh sách template gửi (mỗi item:
`{id, name, type, content}`)                                                                                                      |
| filter_number | Long | Số người đủ điều kiện filter |
| filters | Json Object | Điều kiện lọc phân nhóm theo toán tử: `{"and": [...], "or": [...]}`. Mỗi item gồm
`{id, type, data}`. Muốn sửa filter: build lại FULL state từ object này rồi gửi qua `update_filter(target=broadcast)` (REPLACE-ALL) |
| actions | Json Array | Danh sách action thực thi sau khi gửi. Mỗi item gồm `{type, data}` — chỉ để đọc/audit.
Muốn thay đổi: tạo action chain qua `create_action` rồi gắn qua `update_broadcast.action_id` (REPLACE toàn bộ set) |
| created_at | String | Ngày tạo (format:
`yyyy-MM-dd HH:mm:ss`)                                                                                                                             |
| parent_id | Long | Null với broadcast đơn lẻ hoặc broadcast cha của nhóm multi-schedule. Set = id của parent với
broadcast con trong nhóm multi-schedule |
| is_parent | Boolean | `true` khi broadcast này là parent của nhóm multi-schedule (có con trỏ đến id này). `false` nếu
không |

**Sub Object Template (trong `templates`):**
| Name | Type | Description |
|---------|--------|--------------------------------------------------------------------------------------------|
| id | Long | ID của template |
| name | String | Tên template |
| type | String | Loại template: `text` / `image` / `video` / `voice` / `form` / `location` / v.v. |
| content | Object | Nội dung template (chuỗi text với type=text, URL với type=image/video/voice, object JSON với
type=form/location) |

**Sub Object Filter Item (trong `filters.and[]` hoặc `filters.or[]`):**
| Name | Type | Description |
|------|--------|--------------------------------------------------------------------------------------------|
| id | Long | ID của filter |
| type | String | Loại filter: `tag` / `friend_info` / `conversion` / `affiliate` / `status_chat` / `scenario` /
`qr_code` / `friend_name` / `day_add_friend` / v.v. |
| data | Object | Dữ liệu filter dạng JSON object (parse từ `filters_v2.data`), **đã normalize về grammar AI-facing** (2026-09-22, `FilterWireNormalizer`): các field enum trả **string** (`tag_condition`, `scenario_condition`, `qr_condition`, `day_filter_type`, `type_data`/`op_compare`...) và key đổi về tên input (`search_from`, `select_value_friend`, `status_search_condition`). Có thể chứa thêm key UI (`active`, `default_check_all`, `preview_original`) — clone-ready cho `update_filter(target=broadcast)` |

**Bảng mapping `tag_condition` — 2 biểu diễn tuỳ ngữ cảnh (V3-1, cập nhật 2026-09-22):**

| Ngữ cảnh | Kiểu | Giá trị |
|---|---|---|
| **Output** `list_broadcasts.filters` (bảng này) + **Input** `create_broadcast.filters` (JSON-string) | string | `"has_any"` / `"has_all"` / `"exclude_any"` / `"exclude_all"` |
| **Input** `create_filter` / `update_filter` (typed, field `tagCondition`) | int | `0` / `1` / `2` / `3` |

> DB wire vẫn lưu int 0-3 (PHP so sánh số khi gửi) — MCP normalize 2 chiều: linect convert string→int khi ghi,
> `FilterWireNormalizer` convert int→string khi đọc.

**Sub Object Action Item (trong `actions`):**
| Name | Type | Description |
|------|--------|------------------------------------------------------------------------------------------------------|
| type | String | Loại action (giá trị AI-facing): `tag` / `scenario` / `richmenu` / `friend_info` / `block` /
`bookmark` / `handling_status` (DB lưu `compliant_status`, response map về `handling_status`) |
| data | Object | Dữ liệu action dạng JSON object (parse từ `t_actions_detail.data`). Chỉ để đọc — muốn thay đổi,
dùng `create_action` + `update_broadcast.action_id` |

**Sub Object Pagination:**
| Name | Type | Description |
|-------------|---------|--------------------|
| currentPage | Integer | Trang hiện tại |
| limit | Integer | Số record mỗi trang |
| total | Integer | Tổng số record trả về trong trang này |

**Sample Output:**

```json
{
  "broadcasts": [
    {
      "id": 5001,
      "name": "February Sale Announcement",
      "status": "delivered",
      "send_day": "2026-02-01",
      "send_time": "10:00:00",
      "send_count": 5180,
      "template_count": 3,
      "action_id": 101,
      "templates": [
        { "id": 201, "name": "Sale Banner", "type": "image", "content": "https://cdn.example.com/banner.jpg" },
        { "id": 202, "name": "February Promotion", "type": "form", "content": { "message_button": {} } }
      ],
      "filter_number": 5200,
      "filters": {
        "and": [
          { "id": 301, "type": "tag", "data": { "tags_search": [12, 15], "active": true, "tag_condition": 0, "default_check_all": false, "preview_original": "VIP Members" } }
        ],
        "or": []
      },
      "actions": [
        { "type": "tag", "data": { "tag_ids": [20], "tag_names": ["February Sale Received"], "action": 1 } }
      ],
      "created_at": "2026-01-30 14:20:00",
      "parent_id": null,
      "is_parent": false
    },
    {
      "id": 5002,
      "name": "Weekly Newsletter #5",
      "status": "wait_to_send",
      "send_day": "2026-02-05",
      "send_time": "09:00:00",
      "send_count": null,
      "template_count": 1,
      "action_id": null,
      "templates": [
        { "id": 203, "name": "Newsletter Week 5", "type": "form", "content": {} }
      ],
      "filter_number": 12000,
      "filters": { "and": [], "or": [] },
      "actions": [],
      "created_at": "2026-02-04 16:00:00",
      "parent_id": null,
      "is_parent": true
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2
  }
}
```

---

## list_broadcast_templates

**Description:** Trả về danh sách template con của một broadcast cụ thể (resolve `broadcast.template_ids` → các template
row). Mỗi item bao gồm `template_id`, `name`, `type`, `preview_text` (tối đa 50 ký tự) và `data` (full edit-body của
template). Gọi tool này TRƯỚC section template của `update_broadcast` để lấy `broadcast_template_id` cần edit
(xem [update_broadcast](#update_broadcast)). Nếu nhiều template khớp mô tả của user, liệt kê ra với
`preview_text` và hỏi user chọn; không tự chọn.

**Tool:** `list_broadcast_templates`

**Input:**
| Name | Type | Required | Description |
|--------------|--------|----------|-------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool `list_bots`                  |
| broadcast_id | Long | Yes | Numeric broadcast ID (lấy từ `list_broadcasts.broadcasts[].id`) |

**Output:**
| Name | Type | Description |
|----------------|-------------|--------------------------------------|
| broadcast_id | Long | ID của broadcast |
| broadcast_name | String | Tên broadcast |
| templates | Json Array | Danh sách template con của broadcast (theo thứ tự trong `template_ids`) |

**Sub Object Template Item (trong `templates`):**
| Name | Type | Description |
|--------------|--------|-------------------------------------------------------------------------------------------------------------------|
| template_id | Long | ID của template — dùng làm `broadcast_template_id` khi EDIT qua
`update_broadcast` (section template) |
| name | String | Tên template |
| type | String | Loại template — giá trị DB thô: `text` / `image` / `video` / `voice` / `media` / `form` /
`location`. Lưu ý: trong `data.type`, các loại media (image/video/voice) được gộp thành `media` |
| preview_text | String | Đoạn text xem trước (tối đa 50 ký tự). Với type=text: nội dung text. Với type=form: title
panel đầu tiên. Với type=location: địa chỉ. Các type khác (media): rỗng |
| data | Object | Full edit-body của template (envelope 18 keys — xem Sub Object bên dưới). Dùng làm nguồn tham
chiếu để build lại payload typed đầy đủ (full state) cho `update_broadcast.template` — KHÔNG gửi nguyên object này
(shape khác typed schema) |

**Sub Object `data` (envelope, chỉ section khớp `type` được fill):**
| Name | Type | Description |
|----------------------|--------|--------------------------------------------------------------------------------|
| type | String | Loại đã normalize: `text` / `form` / `media` / `location` |
| message_text | Object | [type=text] `{content, usePreviewUrl, keepRawUrl, numberActionUrlRedirect, urlSettings[]}`. Rỗng `{}` với type khác |
| message_button | Object | [type=form] Nội dung form/carousel (`list_panel[]` với buttons + detail_action). Rỗng `{}` với type khác |
| message_media | Object | [type=media] `{type_media, img_path, thumbnail_path, type_size, is_setting_image_map, image_map, imageMapItems[], ...}`. Rỗng `{}` với type khác |
| message_location | Object | [type=location] Nội dung vị trí. Rỗng `{}` với type khác |
| message_stamp | Object | Luôn rỗng `{}` (slot cố định của envelope) |
| message_introduction | Object | Luôn rỗng `{}` (slot cố định của envelope) |
| template_group_id | String | Luôn `"-11"` (routing broadcast) |
| template_child_id | String | ID của template dạng string (= `template_id`) |
| tmp_name | String | Luôn `"broadcast"` |
| action_type | String | Luôn `"sendAll"` |
| broadcastId | String | ID broadcast dạng string |
| scheduleSendId / conversationId / content / address / latitude / longitude | String | Luôn `""` (slot cố định của envelope) |

**Sample Output:**

```json
{
  "broadcast_id": 5001,
  "broadcast_name": "February Sale Announcement",
  "templates": [
    {
      "template_id": 201,
      "name": "Promo Text",
      "type": "text",
      "preview_text": "Hello! Check out our 20% discount today.",
      "data": {
        "type": "text",
        "message_button": {},
        "message_media": {},
        "message_stamp": {},
        "message_location": {},
        "message_text": {
          "content": "Hello! Check out our 20% discount today.",
          "usePreviewUrl": true,
          "keepRawUrl": false,
          "numberActionUrlRedirect": 1,
          "urlSettings": []
        },
        "message_introduction": {},
        "template_group_id": "-11",
        "template_child_id": "201",
        "tmp_name": "broadcast",
        "action_type": "sendAll",
        "broadcastId": "5001",
        "scheduleSendId": "",
        "conversationId": "",
        "content": "",
        "address": "",
        "latitude": "",
        "longitude": ""
      }
    },
    {
      "template_id": 202,
      "name": "February Promotion",
      "type": "form",
      "preview_text": "February Sale Details",
      "data": {
        "type": "form",
        "message_button": {
          "type_button": 1,
          "list_panel": [
            { "title": "February Sale Details", "text": "Check out our offers", "img_path": "", "buttons": [ { "...": "..." } ], "...": "..." }
          ],
          "...": "..."
        },
        "message_media": {},
        "message_stamp": {},
        "message_location": {},
        "message_text": {},
        "message_introduction": {},
        "template_group_id": "-11",
        "template_child_id": "202",
        "tmp_name": "broadcast",
        "action_type": "sendAll",
        "broadcastId": "5001",
        "scheduleSendId": "",
        "conversationId": "",
        "content": "",
        "address": "",
        "latitude": "",
        "longitude": ""
      }
    }
  ]
}
```

---

> Spec đầy đủ của tool `create_broadcast` sau đợt refactor **typed schema** (2026-09-16,
> [McpBroadcastTool.java](../src/main/java/solution/wssv/backendmcpline/mcp/McpBroadcastTool.java)).
> `templates` giờ là **typed record** (`BroadcastMessage` + các record trong `mcp/model/**`) — schema nằm ngay trong
> input schema của tool (client nhận qua `tools/list`, KHÔNG cần gọi guide). Riêng **`filters` vẫn là JSON-string** —
> condition object dùng cùng cấu trúc với `conditions` của `create_filter` / `update_filter` (typed schema, xem
> [30-filter.md](30-filter.md)); grammar per-type document tại [§5](#5-filter-types).
> Toàn bộ guide tool đã **disable** (`guide_broadcast_creation` / `guide_broadcast_images` / `guide_broadcast_audit` /
> `guide_template_structure` / `guide_action_structure` / `guide_text_content_tokens` / `guide_url_tokens`, và từ
> 2026-09-18 cả `guide_filter_structure` / `guide_filter_grouping`) — nội dung được distill vào description + typed
> schema của tool.

---

## 1. `create_broadcast`

**Tool:** `create_broadcast`

**Description (EN)**: Creates a new broadcast (message delivery) for a bot. The broadcast is always created
as a DRAFT (status `'unregistered'`) — this call never sends anything. The timing fields only record which send mode
the draft will use; registering the draft for actual delivery happens in the LME web UI, not through these tools.

SEND TIMING — 3 cases, detected from the fields you send: (1) send-now type → omit `send_day`, `send_time` and
`schedules` (the backend records the current Japan time; `setting_send_message` is stored as 0); (2) single
schedule → `send_day` + `send_time` (stored as 1); (3) multi-schedule → `schedules` array (max 11 = 1 original +
up to 10 children), omit `send_day`/`send_time`.

IMAGE SOURCE — every img_path must be a `download_url` returned by `get_file_params` (a file uploaded in this
conversation) or an image path already stored in this bot's template library (`list_templates` /
`get_template_detail`). Never invent an image URL and never paste an external one (Azure blob, OpenAI CDN, imgur,
picsum, self-hosted...) — LME cannot fetch those and the message breaks. If the user asks you to GENERATE an image,
stop and ask them to generate and attach the file first.

ZERO-INVENTION + VERIFY — fill only the fields the user explicitly asked for; leave everything else at its default.
Resolve names → ids with the matching `list_*` tool; never fabricate ids — every entity ID inside filters
(`tags_search`, `info_search`, `conversion_search`, `affiliate_search`, `status_chat_search`...) is ownership-checked
at submission and offenders are rejected with a 403 list. After creating, confirm the outcome from this tool's
response or `list_broadcasts` instead of assuming.

Post-send actions are attached **by reference**: pass `action_id` of a chain created with `create_action`. If a text
template carries `ogp.imageUrl`, the server makes one outbound HTTP HEAD request to that caller-provided URL to
validate the image size. The LIFF URL grammar and personalization tokens are embedded in the text `content` field's
schema description; filter condition objects use the same structure as `create_filter` / `update_filter` `conditions`
(typed schema).

### Send timing — 3 cases

| Case | Mô tả                                                     | Fields gửi                                                                                                                                 |
|------|-----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| 1    | **Send now** — user nói "gửi ngay" / không nhắc thời gian | OMIT `send_day`, `send_time`, `schedules` (backend tự fill giờ JP hiện tại; `setting_send_message=0`)                                      |
| 2    | **Schedule once** — user chỉ định 1 thời điểm             | `send_day` (yyyy-MM-dd) + `send_time` (HH:mm) (`setting_send_message=1`)                                                                   |
| 3    | **Schedule multiple** — user chỉ định nhiều thời điểm     | `schedules` typed array (tối đa **11 items** = 1 lịch gốc + tối đa 10 lịch bổ sung); OMIT top-level `send_day`/`send_time`                 |

> Backend tự nhận diện case từ field nào được gửi — KHÔNG cần truyền flag. Broadcast luôn tạo dạng **DRAFT**
> (`status='unregistered'`) — tool KHÔNG tự gửi; đăng ký gửi thật thực hiện trên LME web UI.

### Tool input params

| Name             | Type                      | Required | Description                                                                                                                                                                                                                                                                          |
|------------------|---------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `bot_id`         | String                    | Yes      | Bot ID hash string lấy từ `list_bots`                                                                                                                                                                                                                                                |
| `name`           | String                    | Yes      | Administrative title. **STRICT**: non-empty AND ≤ **20 chars**. Server hard-reject names >20 chars với `IllegalArgumentException`. Nếu user đưa tên dài hơn → hỏi user rút gọn TRƯỚC khi gọi                                                                                          |
| `send_day`       | String                    | No       | Ngày gửi (yyyy-MM-dd). Chỉ dùng cho Case 2                                                                                                                                                                                                                                           |
| `send_time`      | String                    | No       | Giờ gửi (HH:mm). Chỉ dùng cho Case 2                                                                                                                                                                                                                                                 |
| `schedules`      | List\<BroadcastSchedule\> | No       | Multi-schedule (Case 3). Typed list — mỗi item `{ "sendDay": "YYYY-MM-DD", "sendTime": "HH:mm" }` (Japan TZ). Mỗi item tạo 1 child broadcast. **Giới hạn: tối đa 11 items**. KHÔNG combine với top-level `send_day`/`send_time`                                                      |
| `templates`      | List\<BroadcastMessage\>  | Yes*     | Typed list message templates. **BẮT BUỘC ở runtime** — phải có ít nhất 1 (schema đánh dấu optional nhưng server reject nếu thiếu). Mỗi item set `type` (`text`\|`image`\|`video`\|`voice`\|`location`\|`form`) và fill ĐÚNG 1 payload field cùng tên. Tối đa 1 template quick reply (form `quick_reply` / `quick_reply_image`) mỗi broadcast. Xem [§4](#4-template-types-typed) |
| `action_id`      | Long                      | No       | ID của **action chain** tạo bằng `create_action` — gắn **theo tham chiếu** làm post-send action. Phải > 0. Xem [§6](#6-post-send-action--action_id)                                                                                                                                  |
| `filters`        | String (JSON)             | No       | **JSON string** `{"and":[...], "or":[...]}` — vẫn là JSON-string (chưa typed). Omit = gửi tất cả. Condition object cùng cấu trúc `conditions` của `create_filter`/`update_filter` ([30-filter.md](30-filter.md)). Xem [§5](#5-filter-types)                                          |

> ⚠️ **Không có action-only broadcast**: mọi broadcast PHẢI có ít nhất 1 template. Gửi chỉ `action_id` mà không có
> `templates` → server reject: *"templates is required and must contain at least 1 template"*.

> ⚠️ **Param `actions` (typed List\<BroadcastAction\>) KHÔNG còn tồn tại** trên `create_broadcast`. Post-send action
> giờ gắn qua `action_id` (tham chiếu chain của `create_action`) — xem [§6](#6-post-send-action--action_id).

---

## 2. Workflow chuẩn

🔒 **GOLDEN RULE — ZERO-INVENTION PRINCIPLE** (override mọi helpfulness instinct):

Mỗi field có **SEMANTIC PURPOSE rõ ràng** và **TRIGGER PHRASE cụ thể** mà user phải nói để enable nó. Nếu user
**KHÔNG** mention trigger đó → field giữ **default** (`null`, omit, hoặc server default) — hết.

AI **KHÔNG ĐƯỢC** "fill in" 1 field chỉ vì: (a) tên field nghe related với field user vừa nói, (b) "có default cho có"
là helpful, (c) "thường đi kèm với" field user nói, (d) "field empty trông sai sai". Rephrase: `<user nói X>` → set
**chỉ** X. `<user KHÔNG nói Y>` → để Y empty/omit. **Đừng aggregate, đừng duplicate, đừng extrapolate**.

**DUPLICATE-FIELD TRAP** — khi 2 field tên/nghĩa gần giống (vd `form.pcNotificationOrTitle` vs
`form.exceedClickMessage`, hoặc `image.altText` vs text `content`), user mention 1 field KHÔNG implies cả 2. Mỗi field
có trigger riêng — chỉ fill field nào user **explicitly** nói.

**Past incidents lost trust**: AI invent `'xem ngay'` label, AI invent exceed-click Vietnamese message, AI duplicate
メッセージタイトル text vào exceed-click message. Mỗi cái là 1 ZERO-INVENTION violation.

---

0. **IMAGE SOURCE** — Phân biệt RÕ 2 case trước khi quyết định next action:

   **CASE A — USER ĐÃ UPLOAD ẢNH** (ảnh đã attach trong chat hiện tại): proceed **NGAY trong CÙNG flow**. Call
   `get_file_params` với file đã attach → nhận `{download_url, file_id, file_name, mime_type}` (+ `img_width`,
   `img_height` cho ảnh) → tiếp tục `create_broadcast` trong cùng tool-invocation chain. **KHÔNG** yêu cầu user
   "re-upload" / "gọi lại" — ảnh đã sẵn sàng, chỉ cần consume.

   **CASE B — USER YÊU CẦU AI GENERATE ẢNH MỚI** và KHÔNG có file nào được attach: MCP tool KHÔNG generate ảnh được —
   chỉ consume ảnh đã upload. **STOP** và yêu cầu user generate ảnh (bằng công cụ tạo ảnh bất kỳ) rồi **attach file**
   vào chat, sau đó mới tiếp tục flow.

   **ANTI-PATTERN (cả 2 case)**: **KHÔNG** bypass bằng cách invent URL, copy external CDN link (Azure blob, OpenAI
   CDN, picsum, imgur, self-hosted URL), hay proceed với placeholder — các URL đó inaccessible từ LME. NEVER call
   `create_broadcast` cho template có ảnh khi `get_file_params` chưa trả về real `{download_url, file_id}`.

1. **TYPED SCHEMA — KHÔNG cần guide**: schema của `templates` (per-type payload, per-field description) nằm trong
   input schema của tool — client nhận tự động qua `tools/list`. Với `filters` (JSON-string): condition object dùng
   cùng cấu trúc `conditions` của `create_filter`/`update_filter` (typed schema, [30-filter.md](30-filter.md)) —
   shape per-type xem [§5](#5-filter-types).

2. **BẮT BUỘC KHI CÓ ẢNH/MEDIA** — Call `get_file_params` với file user attach. Trả về `{download_url, file_id,
   file_name, mime_type}`; với ảnh có thêm `img_width`/`img_height`. Giá trị duy nhất hợp lệ cho `imgPath` /
   `thumbnailPath` là `download_url` từ `get_file_params` (hoặc image path đã có sẵn trong template library của bot).

3. *(Optional)* Call `list_templates` / `get_template_detail` nếu cần tham chiếu template/image có sẵn.

4. **VERIFY IDs — ID-RESOLUTION RULE** (áp dụng cho mọi ID trong `filters` và trong action chain):
    - **User đưa TÊN** → call list tool tương ứng để resolve name → id, và fill field hiển thị (`tag_names`,
      `scenario_name`, `qr_names`, `preview_original`, ...):
        - `tag` → `list_tags(names:["AAAA","BB"])` (EXACT, case-insensitive, whitespace-trimmed; partial KHÔNG
          match). Response có `not_found_names` — confirm với user trước khi tiếp tục.
        - `scenario` → `list_scenarios`; `richmenu` → `list_richmenus`; `friend_info` →
          `list_friend_info_fields`; `conversion` → `list_conversions`; `affiliate` → `list_affiliates`;
          `status_chat` / `handling_status` → `list_handling_statuses`; `qr_code` → `list_traffic_sources`.
    - **User đưa RAW ID** → **SKIP list tool**; fill field ID và **ĐỂ TRỐNG** field hiển thị (`tag_names=[]`,
      `scenario_name=""`, `preview_original=""`...) — server validate ownership và **tự enrich** display name từ DB
      lúc submit.
    - **SERVER-SIDE VALIDATION**: mọi ID được ownership-check lúc submit. ID không thuộc bot → abort 403 kèm danh
      sách toàn bộ ID vi phạm group theo type — AI sửa 1 lần.

   > **STRICT NOT-FOUND RULE**: nếu bất kỳ item nào user mention KHÔNG tìm thấy trong list-tool response (tag trong
   > `not_found_names`, scenario name absent, ...) → DO NOT proceed. KHÔNG fabricate id, KHÔNG guess item tương tự,
   > KHÔNG silently substitute. STOP, báo lại item missing, đề xuất item gần nhất có tồn tại hoặc hỏi user chọn lại.

4.5. 🔍 **PRE-SUBMIT FIELD AUDIT** (trước MỌI `create_broadcast`) — enforce GOLDEN RULE:

Trước khi call, **walk** mọi giá trị **NON-EMPTY / NON-DEFAULT** trong payload (`templates[]`, `action_id`, `filters`,
top-level params) và verify **TỪNG GIÁ TRỊ** trace back được về 1 phrase **EXPLICIT** trong prompt gần nhất của user.

**HIGH-RISK PAIRS** cần audit explicit (đã gây past bugs):

- `form.pcNotificationOrTitle` vs `form.exceedClickMessage` — trigger khác nhau, NEVER duplicate.
- `form.pcNotificationOrTitle` (PC preview / メッセージタイトル) vs text `content` — khác nhau, NEVER duplicate.
- `image.altText` / `video.altText` (PC/notification preview) — KHÔNG phải message text.
- `button.label` — REQUIRED cho standard/color/quick_reply; **bị force empty** cho subtype image. NEVER invent
  placeholder như `'xem ngay'`.
- `panel.title` / `panel.text` — chỉ fill nếu user provide đúng đoạn text đó.
- `form.exceedActions` vs `buttons[].actions` — exceed action đặt ở **`exceedActions`** (form level), regular click
  action đặt ở `buttons[].actions`. Không lẫn.

Nếu audit phát hiện BẤT KỲ non-traceable value → **fix payload TRƯỚC khi submit**.

5. Call `create_broadcast` với `bot_id`, `name`, `templates` và (tuỳ chọn) `filters` / `action_id` / timing fields.
   Nếu template có ảnh, `imgPath` MUST equal `download_url` từ `get_file_params` ở step 2.
6. **SEND TIMING** — chọn 1 trong 3 case ở [§1](#1-create_broadcast).

---

## 3. Tham số chi tiết (từ tool description)

| Field            | Type                      | Description                                                                                                                                                                                                                                                                  |
|------------------|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `bot_id`         | String                    | Required — Bot ID hash string (từ `list_bots`)                                                                                                                                                                                                                               |
| `name`           | String                    | **REQUIRED** — Administrative title. Non-empty, ≤ 20 chars. Server reject tên dài hơn — hỏi user rút gọn trước khi gọi                                                                                                                                                       |
| `send_day`       | String                    | Optional — Send date (YYYY-MM-DD). Chỉ Case 2. Omit cho Case 1 (backend tự fill ngày JP hiện tại) và Case 3                                                                                                                                                                  |
| `send_time`      | String                    | Optional — Send time (HH:mm). Chỉ Case 2                                                                                                                                                                                                                                     |
| `schedules`      | List\<BroadcastSchedule\> | Optional — Typed list `{ "sendDay": "YYYY-MM-DD", "sendTime": "HH:mm" }`. Chỉ Case 3. Backend tạo 1 child broadcast per item. Max 11 = 1 gốc + 10 bổ sung. KHÔNG combine với `send_day`/`send_time`                                                                          |
| `templates`      | List\<BroadcastMessage\>  | **REQUIRED** — Typed list. Mỗi item set `type` (`text`\|`image`\|`video`\|`voice`\|`location`\|`form`) và fill ONLY payload field cùng tên. Per-type fields nằm trong input schema của tool. MCP layer tự build backend envelope. Ảnh: `imgPath` = `download_url` từ `get_file_params` |
| `action_id`      | Long                      | Optional — ID chain post-send action từ `create_action`. Broadcast **THAM CHIẾU** chain đó: steps được re-save in-place dưới cùng chain id, broadcast link tới chain → `update_action` sửa chain sau này áp dụng luôn cho broadcast. Step types cho phép: `tag`, `scenario`, `richmenu`, `friend_info`, `block`, `bookmark`, `handling_status` — chain chứa step `text` bị reject. `templates` vẫn required kể cả khi có `action_id` |
| `filters`        | String (JSON)             | Optional — JSON string `{"and":[...], "or":[...]}` — 2 array filter objects. `and` = AND-join (match ALL); `or` = OR-join (match ANY). Kết hợp: `(AND group) OR (OR group)`. Omit = target all users. Condition object cùng cấu trúc `conditions` của `create_filter`/`update_filter` ([30-filter.md](30-filter.md)) |

---

## 4. Template types (typed)

`templates` là array của **`BroadcastMessage`** — flat union (không anyOf): set `type` rồi fill **ĐÚNG 1** payload
field trùng tên với type. MCP layer (BroadcastTemplateDataBuilder + các standalone builder) tự build full backend
envelope (`template_group_id="-11"`, `tmp_name="broadcast"`, `action_type="sendAll"`, `broadcastId=""`, panel/button
keys đầy đủ...) — AI **KHÔNG còn phải hand-assemble** raw JSON (`message_button`, `list_panel`, `is_apply_title`,
per-key ordering... đã là chuyện của builder).

### Envelope `BroadcastMessage`

| Field             | Type                | Required | Description                                                                                                                                                                       |
|-------------------|---------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type`            | enum                | Yes      | `text` \| `image` \| `video` \| `voice` \| `location` \| `form` — chọn payload field nào được đọc. (image/video/voice cùng serialize về backend `data.type="media"` — builder tự set) |
| `templateChildId` | Long                | No       | **EDIT only** (dùng ở `update_broadcast` template section / `update_scenario_step`). Với `create_broadcast`: **OMIT**                                                             |
| `text`            | TextTemplateData    | (type=text)     | Payload text — [§4.1](#41-text--texttemplatedata)                                                                                                                          |
| `image`           | ImageTemplateData   | (type=image)    | Payload ảnh — [§4.2](#42-image--imagetemplatedata)                                                                                                                         |
| `video`           | VideoTemplateData   | (type=video)    | Payload video — [§4.3](#43-video--videotemplatedata)                                                                                                                       |
| `voice`           | VoiceTemplateData   | (type=voice)    | Payload audio — [§4.4](#44-voice--voicetemplatedata)                                                                                                                       |
| `location`        | LocationTemplateData| (type=location) | Payload vị trí — [§4.5](#45-location--locationtemplatedata)                                                                                                                |
| `form`            | FormTemplateData    | (type=form)     | Payload form/carousel — [§4.6](#46-form--formtemplatedata)                                                                                                                 |

> **Field name = camelCase** (JSON input): `imgPath`, `thumbnailPath`, `altText`, `usePreviewUrl`, `urlSettings`,
> `exceedClickMessage`... — khác snake_case của backend wire (builder tự convert).

### 4.1. `text` — `TextTemplateData`

| Field                     | Type                    | Required | Description                                                                                                                                                                                                                         |
|---------------------------|-------------------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `content`                 | string                  | Yes      | Message body 1–5000 chars. Hỗ trợ personalization tokens (`{name}`, `[remain to=YYYY-MM-DD]`, `[date add=N]`, `[date_format=FMT]`, `[FRIEND_INFO_<encoded_id>]`, server-side `{CURRENT_TS}`) + LIFF URL shortcuts — grammar embedded trong schema description của field |
| `usePreviewUrl`           | Boolean                 | No       | URL表示プレビュー cho **cả message**. `true` (default) = show; `false` = hide. Nếu user nói "tắt preview cho URL cụ thể" → dùng `urlSettings[].usePreviewUrl=false` thay vì field này                                                  |
| `keepRawUrl`              | Boolean                 | No       | `false` (default) = LME auto-shorten URL + track click; `true` = giữ URL nguyên văn (mất tracking, URL-tap action không chạy). **Chỉ set `true` khi user explicit** nói "URL gốc" / "không rút gọn" / "そのままのURL"                  |
| `urlSettings`             | List\<TextUrlSetting\>  | No       | Per-URL action/expiry/OGP settings — 1 entry per URL trong `content`. Null/empty = default (no action, no expiry, auto OGP)                                                                                                           |
| `urlActionMode`           | Integer                 | No       | アクション稼働設定: `1` (default) = action chạy 1 lần per friend (一度のみ稼働); `0` = chạy mỗi lần click (何度でも稼働). Chỉ set `0` khi cần repeat                                                                                     |

#### `TextUrlSetting` (per-URL)

| Field             | Type              | Required | Description                                                                                                                                                             |
|-------------------|-------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `url`             | string            | Yes      | URL đúng nguyên văn trong `content` mà setting này áp dụng                                                                                                              |
| `urlId`           | Long              | No       | **UPDATE only** — `id` của URL redirect record từ `get_template_detail`. Omit/0 khi create                                                                              |
| `actionId`        | Long              | No       | Shortcut tham chiếu chain `create_action` (tương đương `actions=[{actionId}]`). Nếu set cả 2 thì phải match                                                             |
| `outTimeActionId` | Long              | No       | Shortcut cho post-expiry action (tương đương `outTimeActions=[{actionId}]`)                                                                                             |
| `actions`         | List\<ActionRef\> | No       | Action chain khi user tap URL (trong hạn) — **đúng 1 entry `{actionId}`** tham chiếu chain của `create_action` (gắn theo tham chiếu). Inline action KHÔNG được chấp nhận |
| `expiry`          | TextUrlExpiry     | No       | 表示期限. Null = không expiry                                                                                                                                            |
| `outTimeActions`  | List\<ActionRef\> | No       | Action chain chạy sau khi URL hết hạn — đúng 1 entry `{actionId}`. Chỉ có hiệu lực khi `expiry` set                                                                      |
| `ogp`             | TextUrlOgp        | No       | Override OGP preview card. Null = backend auto-fetch OGP từ URL                                                                                                          |
| `usePreviewUrl`   | Boolean           | No       | Preview riêng cho URL này (LINEトーク画面表示)                                                                                                                            |

#### `TextUrlExpiry`

| Field         | Type    | Required | Description                                                                                              |
|---------------|---------|----------|--------------------------------------------------------------------------------------------------------------|
| `mode`        | enum    | Yes      | `specific_date` (hết hạn ngày cố định — cần `expiredDate`) \| `n_days` (N ngày sau delivery — cần `days`) |
| `expiredDate` | string  | (specific_date) | `yyyy-MM-dd`. KHÔNG set khi mode=`n_days`                                                         |
| `expiredTime` | string  | No       | `HH:mm` (chỉ specific_date; default `00:00`)                                                             |
| `days`        | Integer | (n_days) | Min 0 (0 = hết hạn cùng ngày gửi). KHÔNG set khi mode=`specific_date`                                    |
| `afterDayTime`| string  | No       | `HH:mm` (chỉ n_days; default `00:00`)                                                                    |
| `onExpired`   | object  | Yes (khi có expiry) | 期限到来後に表示するページ — đúng 1 trong 2: `message` (text page ≤5000 chars) hoặc `redirectUrl` (http(s) URL). Backend chỉ lưu expiry khi field này set |

#### `TextUrlOgp`

| Field         | Type   | Description                                                                                                                           |
|---------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `title`       | string | プレビュータイトル ≤ **10 chars**                                                                                                        |
| `description` | string | プレビューテキスト ≤ **25 chars**                                                                                                        |
| `imageUrl`    | string | プレビュー画像 — full `https://` URL. CREATE với ảnh mới: upload qua `get_file_params` rồi dùng URL trả về. ⚠️ Server thực hiện 1 HTTP HEAD tới URL này để validate (lý do tool có openWorldHint=true) |

**Example:**

```json
{
  "type": "text",
  "text": {
    "content": "Xem khuyến mãi: https://example.com/promo",
    "usePreviewUrl": true,
    "urlSettings": [
      { "url": "https://example.com/promo", "actions": [ { "actionId": 4321 } ] }
    ]
  }
}
```

> Validation: text message chạy chung chain validate với `create_text_template` (`TextDataValidator`) — check URL nằm
> trong `content`, expiry hợp lệ, `urlActionMode`, ngày của `[remain]` token...

### 4.2. `image` — `ImageTemplateData`

3 mode tap-zone quyết định bởi `layoutId` + `tapZones`:

- **Case 1 — no tap action**: omit cả `layoutId` lẫn `tapZones`.
- **Case 2 — predefined layout**: set `layoutId` (1–8) + `tapZones` (N entry theo thứ tự zone, KHÔNG cần
  x/y/width/height — builder tự tính bounds) + `imgWidth`/`imgHeight`.
- **Case 3 — manual zones**: `tapZones` với x/y/width/height explicit per zone; omit `layoutId`.

| Field           | Type                 | Required | Description                                                                                                                   |
|-----------------|----------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------|
| `imgPath`       | string               | Yes      | `download_url` từ `get_file_params`. KHÔNG dùng external URL                                                                  |
| `thumbnailPath` | string               | No       | Thumbnail download_url. Omit = reuse full image URL                                                                           |
| `altText`       | string               | No       | パソコン版・通知欄の表示テキスト, ≤ 400 chars                                                                                   |
| `layoutId`      | Integer              | Case 2   | 1=full, 2=vertical split (2 zones), 3=horizontal split (2), 4=3 horizontal strips, 5=2×2 grid (4), 6=1 wide top + 2 bottom (3), 7=1 top half + 2 quarter strips (3), 8=2×3 grid (6) |
| `tapZones`      | List\<ImageTapZone\> | Case 2/3 | 1 entry per clickable region                                                                                                  |
| `imgWidth`      | Double               | Case 2   | Pixel width — lấy từ `img_width` của `get_file_params`                                                                        |
| `imgHeight`     | Double               | Case 2   | Pixel height — lấy từ `img_height` của `get_file_params`                                                                      |

#### `ImageTapZone`

2 layer độc lập CÓ THỂ kết hợp (エルメアクション＋友だちアクション):

- **Friend action** (user trải nghiệm khi tap): `url` / `phone` / `lineId` / `email` / `inputText` / `loaProfileId` /
  `lmePage` — set **tối đa 1**.
- **LME action chain** (backend chạy server-side): `actions` = **đúng 1 entry `{actionId}`** (ActionRef →
  `create_action`).
- Chỉ `urlScheme` là exclusive với TẤT CẢ field action khác.
- **Empty zone hợp lệ**: omit hết action fields → zone trang trí không có hành vi tap.

| Field           | Type              | Description                                                                                                 |
|-----------------|-------------------|-----------------------------------------------------------------------------------------------------------------|
| `x`/`y`/`width`/`height` | Integer  | Case 3 (manual) only — pixel bounds. Omit cho Case 2                                                        |
| `url`           | string            | Mở URL khi tap                                                                                              |
| `phone`         | string            | Gọi điện (10–12 digits, no hyphens)                                                                         |
| `lineId`        | string            | Add friend LINE OA (bắt đầu bằng `@`)                                                                       |
| `email`         | string            | Mở mail client                                                                                              |
| `inputText`     | string            | Prefill chat input                                                                                          |
| `openInBrowser` | Boolean           | `true` = external browser (chỉ khi có `url`)                                                                |
| `urlExpiry`     | UrlExpiry         | Hạn URL (chỉ khi có `url`) — xem [§4.6 UrlExpiry](#urlexpiry-button--tap-zone)                              |
| `actions`       | List\<ActionRef\> | LME action chain — đúng 1 `{actionId}`                                                                      |
| `urlScheme`     | UrlSchemeData     | LINE URL scheme — exclusive với mọi field khác                                                              |
| `loaProfileId`  | string            | Mở profile LINE OA khác (bắt đầu bằng `@`)                                                                  |
| `lmePage`       | LmePageData       | Mở trang LME (FORM/PRODUCT/EVENT/CONVERSION/SALON/LESSON) — xem [§4.6 LmePageData](#lmepagedata-post_back10) |

**Example (Case 2 — layout 2 zones):**

```json
{
  "type": "image",
  "image": {
    "imgPath": "https://lme.../uploaded.jpg",
    "layoutId": 2,
    "imgWidth": 1024,
    "imgHeight": 768,
    "tapZones": [
      { "url": "https://example.com/left" },
      { "inputText": "Tôi quan tâm" }
    ]
  }
}
```

### 4.3. `video` — `VideoTemplateData`

| Field           | Type    | Required | Description                                                     |
|-----------------|---------|----------|---------------------------------------------------------------------|
| `videoPath`     | string  | Yes      | Video `download_url` từ `get_file_params`                       |
| `thumbnailPath` | string  | Yes      | Thumbnail image `download_url` từ `get_file_params`             |
| `duration`      | Integer | No       | Giây (default 0)                                                |
| `altText`       | string  | No       | パソコン版・通知欄の表示テキスト ≤ 400 chars                       |

### 4.4. `voice` — `VoiceTemplateData`

| Field      | Type    | Required | Description                               |
|------------|---------|----------|-----------------------------------------------|
| `audioPath` | string  | Yes      | Audio `download_url` từ `get_file_params` |
| `duration` | Integer | No       | Giây (default 0)                          |
| `altText`  | string  | No       | ≤ 400 chars                               |

### 4.5. `location` — `LocationTemplateData`

| Field       | Type   | Required | Description                                             |
|-------------|--------|----------|-------------------------------------------------------------|
| `title`     | string | Yes      | 位置情報タイトル 1–90 chars (vd `東京駅`)                 |
| `address`   | string | Yes      | 位置情報詳細 1–90 chars                                  |
| `latitude`  | string | Yes      | Numeric string, vd `"35.6812"`                          |
| `longitude` | string | Yes      | Numeric string, vd `"139.7671"`                         |

### 4.6. `form` — `FormTemplateData`

| Field                   | Type              | Required | Description                                                                                                                                                                                                 |
|-------------------------|-------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `subtype`               | enum              | Yes      | `standard` (ボタン型, type_button=1) \| `color` (カラーボタン型, 2) \| `image` (画像型, 3) \| `quick_reply` (text chips, 4) \| `quick_reply_image` (image chips, 4). User không nói rõ → **hỏi trước khi default** |
| `pcNotificationOrTitle` | string            | No*      | = `message_button.content` cũ, semantics theo subtype: **quick_reply** = chips header (REQUIRED, ≤5000); **quick_reply_image** = không dùng; **standard** = PC notification preview (optional, ≤400); **color/image** = メッセージタイトル (optional, ≤400) |
| `clickLimit`            | enum              | No       | `unlimited` (default, =0) \| `once_total` (=1) \| `once_per_panel` (=2) \| `once_per_button` (=3). KHÔNG áp dụng cho quick_reply / quick_reply_image (bị force 0)                                            |
| `exceedClickMessage`    | string            | No       | Reply text khi user tap vượt click limit (standard/color/image only). Để trống nếu user không chỉ định — server dùng default                                                                                 |
| `exceedActions`         | List\<ActionRef\> | No       | Action chain khi vượt click limit — **đúng 1 entry `{actionId}`** tham chiếu chain của `create_action` (gắn theo tham chiếu). Inline definition KHÔNG được chấp nhận. Standard/color/image only              |
| `panels`                | List\<FormPanel\> | Yes      | Carousel panels (1..10). Standard: 1 panel ≤4 buttons; 2+ panels ≤3 buttons/panel                                                                                                                            |

> ⚠️ **Exceed actions đổi cơ chế**: array inline `_action_when_exceed_click_inline` cũ KHÔNG còn — giờ dùng
> `exceedActions=[{actionId}]` tham chiếu chain của `create_action` (tạo chain trước rồi tham chiếu).

#### `FormPanel`

| Field              | Type               | Required | Description                                                                                                                                                       |
|--------------------|--------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `title`            | string             | No       | Standard/Color: panel title ≤40 chars. **IMAGE subtype — TERMINOLOGY SWAP**: user nói 'ラベル'/'label' → ghi vào ĐÂY, ≤10 chars (overlay label). Empty = không overlay |
| `text`             | string             | No       | Standard: body ≤60 chars **REQUIRED để render**; Color: ≤60 optional. **IMAGE subtype**: user nói 'タイトル'/'title' → ghi vào ĐÂY, ≤10 chars                       |
| `imgPath`          | string             | No/Yes   | Panel image `download_url`. Standard/Color: optional nhưng **all-or-none across panels** (panel nào cũng có hoặc không panel nào có). **REQUIRED** cho subtype `image` và `quick_reply_image` |
| `aspectRatio`      | string             | No       | Cho `quick_reply_image` / `image` (vd `'1/1'`, `'0.75/1'`) — tính từ `img_width`/`img_height` của `get_file_params`. Omit cho standard/color/quick_reply           |
| `typeSize`         | string             | No       | [image/color] `'large'` (default) \| `'middle'` \| `'small'`                                                                                                      |
| `titleBold`        | Boolean            | No       | [color] Bold title. Default false                                                                                                                                 |
| `textBold`         | Boolean            | No       | [color] Bold body. Default false (standard force true)                                                                                                            |
| `titleColor`       | string             | No       | Hex. IMAGE default `#FFFFFF`; Standard/Color default `#000000`                                                                                                    |
| `titleBackground`  | string             | No       | Hex. IMAGE default `#08BF5A` (luôn hex, không empty cho IMAGE); Standard/Color default `''`                                                                       |
| `textColor`        | string             | No       | Hex. IMAGE default `#FFFFFF`; Standard/Color default `#000000`                                                                                                    |
| `textBackground`   | string             | No       | Hex. IMAGE default `#5B5B5B`; Standard/Color default `''`                                                                                                         |
| `numberRowDisplay` | Integer            | No       | Buttons per row. Standard: luôn 1. Color: 1 hoặc 2. Image/quick_reply: 1. Default 1                                                                               |
| `buttons`          | List\<FormButton\> | Yes      | Panel buttons (Standard: max 4 khi 1 panel / 3 mỗi panel khi 2+; Color: max 4; Image: đúng 1; Quick Reply: chips)                                                 |

#### `FormButton`

2 layer độc lập CÓ THỂ kết hợp (エルメアクション＋友だちアクション, 併用可):

- **Friend action**: `url` / `phone` / `lineId` / `email` / `inputText` / `loaProfileId` / `lmePage` — tối đa 1.
- **LME action chain**: `actions` = đúng 1 `{actionId}` (ActionRef).
- `urlScheme` exclusive với tất cả.

Friend action priority (suy ra `post_back`): `phone`→2, `lineId`→3, `email`→4, `inputText`→8, `loaProfileId`→9,
`url`→1, `lmePage`→10, không set→0 (chỉ LME chain hoặc plain button).

| Field           | Type              | Description                                                                                                                                                      |
|-----------------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `label`         | string            | 1–20 chars. **REQUIRED** cho standard/color/quick_reply/quick_reply_image (QR chips: label là chip text — LINE tự gửi label text khi tap, không cần thêm action). **Bị ignore/force empty cho subtype image** (ảnh là click target). NEVER invent placeholder |
| `url`           | string            | Mở URL (post_back=1). Pass URL **as-is** — KHÔNG tự append query param (unique_key, form_id, booking_event_id...). Trang LME-hosted → dùng `lmePage` thay vì `url` |
| `phone`         | string            | Gọi điện, 10–12 digits no hyphens (post_back=2)                                                                                                                  |
| `lineId`        | string            | Add friend LINE OA, bắt đầu `@` (post_back=3)                                                                                                                    |
| `email`         | string            | Mở mail client (post_back=4). **KHÔNG support trên quick_reply/quick_reply_image**                                                                               |
| `inputText`     | string            | Prefill chat input (post_back=8)                                                                                                                                 |
| `openInBrowser` | Boolean           | `true` = external browser. Chỉ khi có `url`                                                                                                                      |
| `urlExpiry`     | UrlExpiry         | Hạn URL — chỉ khi có `url`                                                                                                                                       |
| `actions`       | List\<ActionRef\> | LME action chain server-side khi tap — **đúng 1 `{actionId}`** (chain từ `create_action`, tham chiếu — `update_action` sau này áp dụng luôn). Kết hợp được với mọi friend action |
| `urlScheme`     | UrlSchemeData     | LINE URLスキーム (flag_setting_action='2') — exclusive với TẤT CẢ field khác                                                                                       |
| `loaProfileId`  | string            | Mở profile LINE OA khác, bắt đầu `@`, không phải LINE ID của chính bot (post_back=9)                                                                             |
| `lmePage`       | LmePageData       | Mở trang LME đã cấu hình (post_back=10)                                                                                                                          |
| `labelColor`    | string            | [color subtype] Hex chữ button. Default `#FFFFFF`. Ignore cho standard                                                                                           |
| `labelBackground` | string          | [color subtype] Hex nền button. Default `#08BF5A`. Ignore cho standard                                                                                           |

#### `UrlExpiry` (button / tap zone)

| Field            | Type    | Description                                                                                                     |
|------------------|---------|-----------------------------------------------------------------------------------------------------------------|
| `mode`           | enum    | `SPECIFIC_DATE` (ngày cố định — cần `date`) \| `N_DAYS` (N ngày sau broadcast — cần `days`)                     |
| `date`           | string  | `YYYY-MM-DD` (mode=SPECIFIC_DATE)                                                                               |
| `days`           | Integer | ≥ 0 (0 = hết hạn cùng ngày gửi) (mode=N_DAYS)                                                                   |
| `time`           | string  | `HH:mm` — required cho cả 2 mode                                                                                |
| `expiredUrl`     | string  | Redirect URL sau hết hạn — set **1 trong 2** với `expiredMessage` (bắt buộc 1 khi có urlExpiry)                 |
| `expiredMessage` | string  | Text hiển thị sau hết hạn — set 1 trong 2 với `expiredUrl`                                                      |

#### `UrlSchemeData`

| Field  | Type | Description                                                                                                                                          |
|--------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type` | enum | `SHARE_OA` (1, data=@lineId) \| `SHARE_TEXT` (2, data=text) \| `CAMERA` (3) \| `CAMERA_ROLL` (4) \| `LOCATION` (5) \| `CUSTOM` (6, data=http(s) URL) |
| `data` | string | Required cho SHARE_OA / SHARE_TEXT / CUSTOM; omit cho CAMERA / CAMERA_ROLL / LOCATION                                                              |

#### `LmePageData` (post_back=10)

| Field  | Type | Description                                                                                                                                                          |
|--------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `type` | enum | `FORM` (1) \| `PRODUCT` (2) \| `EVENT` (3) \| `CONVERSION` (5) \| `SALON` (7) \| `LESSON` (8)                                                                        |
| `id`   | Long | Numeric ID entity — resolve qua `list_forms` / `list_products` / `list_events` / `list_conversions` / `list_salons` / `list_lesson_calendars`. User đưa raw ID → dùng luôn |

**Example (form standard, 1 panel 2 buttons):**

```json
{
  "type": "form",
  "form": {
    "subtype": "standard",
    "panels": [
      {
        "text": "Chọn ưu đãi của bạn",
        "buttons": [
          { "label": "Xem menu", "url": "https://example.com/menu" },
          { "label": "Đặt lịch", "lmePage": { "type": "SALON", "id": 12 } }
        ]
      }
    ]
  }
}
```

**Example (form image subtype — ảnh full click):**

```json
{
  "type": "form",
  "form": {
    "subtype": "image",
    "panels": [
      {
        "imgPath": "https://lme.../uploaded.jpg",
        "buttons": [ { "url": "https://example.com/campaign" } ]
      }
    ]
  }
}
```

### 4.7. Validation server-side (vẫn hard-enforce)

`BroadcastPayloadValidator` + tool-layer validate payload đã build — AI **không cần đếm ký tự** trước; vượt limit →
fail với message chỉ đúng field (`VALIDATION_ERROR: <field> ...`):

| Field                              | Limit                                                                    |
|------------------------------------|--------------------------------------------------------------------------|
| `name` (broadcast)                 | Non-empty, ≤ 20 chars                                                    |
| `templates`                        | ≥ 1 item (action-only broadcast bị reject); tối đa 1 quick reply         |
| `schedules`                        | ≤ 11 items                                                               |
| text `content`                     | Non-empty, ≤ 5000 chars                                                  |
| `button.label`                     | ≤ 20 chars; non-empty sau trim cho standard/color/QR; empty cho image    |
| `panel.title` (standard/color)     | ≤ 40 chars                                                               |
| `panel.text` (standard)            | REQUIRED, ≤ 60 chars                                                     |
| `panel.title`/`text` (image overlay)| Mỗi field ≤ 10 chars khi bật overlay                                    |
| `pcNotificationOrTitle`            | Standard/color/image ≤ 400 chars; quick_reply header REQUIRED ≤ 5000     |
| `exceedClickMessage`               | ≤ 400 chars                                                              |
| `altText` (image/video/voice)      | ≤ 400 chars                                                              |
| location `title`/`address`         | REQUIRED, ≤ 90 chars mỗi field                                           |
| Form button limits                 | Standard: 1 panel ≤4 / 2+ panels ≤3 mỗi panel; Color ≤4; Image đúng 1; Quick Reply 1 panel |
| Ảnh subtype color/image            | Tỉ lệ `height/width` ≤ 3 (ảnh quá dọc bị reject)                         |

**Error prefixes khi call fail** — relay verbatim cho user, đây là actionable signals:

- `VALIDATION_ERROR: <field> ...` — payload sai limit/shape; sửa field được chỉ rồi retry.
- `IMAGE_URL_EXPIRED: ...` — **STOP**, KHÔNG retry cùng URL, KHÔNG invent URL khác. Báo user attach lại ảnh → gọi
  `get_file_params` lấy fresh `download_url` → retry.
- `LME_REJECTED: <msg>` — 4xx parse được; show msg, hỏi user adjust.
- `LME_REJECTED_RAW: status=N body=...` — 4xx unparseable; show raw.
- `LME_SERVER_ERROR: status=5xx body=...` — lỗi server LME; bảo user thử lại sau, KHÔNG auto-retry.

---

## 5. Filter types

> `filters` là **JSON string** — param duy nhất của `create_broadcast` chưa typed. Condition object dùng cùng cấu
> trúc `conditions` của `create_filter`/`update_filter` (typed schema — [30-filter.md](30-filter.md)); section này là
> reference per-type đầy đủ. Shape này cũng dùng cho `update_filter(target=broadcast)` (REPLACE full state).

### 5.1. Filter grouping rules (đọc TRƯỚC `filter_types`)

#### Structure

| Field | Description                                                    |
|-------|----------------------------------------------------------------|
| `and` | array — Filters joined với AND. User phải match ALL filters    |
| `or`  | array — Filters joined với OR. User match nếu ANY filter match |

**Combined logic**: `WHERE (and[0] AND and[1] AND ...) OR (or[0] OR or[1] OR ...)`

#### Prompt mapping rules

- **HARD RULE** — Nếu final filter count == 1: ALWAYS put in `and[]`, NEVER in `or[]`. Single filter trong `or[]`
  semantic vô nghĩa và không match LME GUI default.
- Chỉ consider `or[]` khi có 2+ DIFFERENT filter objects joined by user's `'hoặc'/'or'/'または'` BETWEEN DIFFERENT
  filter types.
- VN `'và'` / EN `'and'` / JP `'かつ・と'` between DIFFERENT filter objects → `and` list.
- VN `'hoặc'` / EN `'or'` / JP `'または・もしくは'` between DIFFERENT filter objects → `or` list.
- WARNING: `'hoặc'` BÊN TRONG 1 tag filter (vd `'có tag A hoặc B'`) là INTERNAL OR của tag IDs (dùng
  `tag_condition='has_any'`) — vẫn là ONE filter trong `and[]`, KHÔNG split thành 2 filters.
- Single condition không có connector → put trong `and` (default).
- Mix cả hai (vd `'A AND B, OR C'`) → A và B vào `and`; C vào `or`.

#### Golden rule — tag merging

- GOLDEN RULE: Khi multiple tags cùng 1 intent → emit ONE filter với LONG `tags_search` list, NOT multiple filters mỗi 1
  tag.
- WRONG: `and:[{tag, has_any, [A]}, {tag, has_any, [B]}]` ← 2 filters, backend merge có thể corrupt.
- RIGHT: `and:[{tag, has_any, [A, B]}]` ← single filter, unambiguous.

**Intent-to-JSON shortcuts:**

| User intent                     | tag_condition | tags_search |
|---------------------------------|---------------|-------------|
| `'có A hoặc B hoặc C'`          | `has_any`     | `[A,B,C]`   |
| `'có cả A và B và C'`           | `has_all`     | `[A,B,C]`   |
| `'không có A, B, C nào cả'`     | `exclude_any` | `[A,B,C]`   |
| `'thiếu ít nhất 1 trong A,B,C'` | `exclude_all` | `[A,B,C]`   |

Mix semantics: nếu user muốn different conditions → USE DIFFERENT `tag_condition` trong separate filters. Vd
`'có VIP nhưng loại kẻ dính blacklist'` → `and:[{has_any,[VIP]}, {exclude_any,[BLACKLIST]}]`.

#### Forbidden patterns

- DO NOT put SINGLE filter trong `or[]`. Single filter ALWAYS go `and[]`.
- DO NOT emit multiple tag filters với SAME `tag_condition` trong SAME group (and/or). Collapse vào one filter với
  combined `tags_search`.
- DO NOT put same `tag_condition` trong cả `and` và `or` groups trừ khi intent thực sự cần (rare).
- DO NOT use arbitrary `tag_condition` values — chỉ 4 listed: `has_any`, `has_all`, `exclude_any`, `exclude_all`.

#### Examples

| User prompt                                                           | filters JSON                                                                                                                                                                         |
|-----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Gửi cho user có tag VIP VÀ là khách hàng cũ`                         | `and:[{type:tag, tags_search:[24933], tag_condition:'has_any'}, {type:'bot_new_friend', select_value_friend:'existing'}], or:[]`                                                     |
| `Gửi cho user có tag VIP HOẶC đã quét QR 10`                          | `and:[], or:[{type:tag, tags_search:[24933], tag_condition:'has_any'}, {type:'qr_code', qrs_search:[10], qr_condition:'scanned_any'}]`                                               |
| `User có CẢ tag A VÀ tag B, HOẶC user mới`                            | `and:[{type:tag, tags_search:[1,2], tag_condition:'has_all'}], or:[{type:'bot_new_friend', select_value_friend:'new'}]` (note: `'có cả'` → `has_all` với cả 2 tags trong ONE filter) |
| `Gửi cho user có tag1 HOẶC tag10, nhưng LOẠI user dính tag_blacklist` | `and:[{type:tag, tags_search:[18383,18376], tag_condition:'has_any'}, {type:tag, tags_search:[99999], tag_condition:'exclude_any'}], or:[]`                                          |
| `User KHÔNG CÓ tag A, B, C NÀO CẢ`                                    | `and:[{type:tag, tags_search:[1,2,3], tag_condition:'exclude_any'}], or:[]`                                                                                                          |
| `Gửi cho tất cả user (no filter)`                                     | omit `filters` parameter entirely — KHÔNG pass `filters`                                                                                                                             |

#### Constraints

- KHÔNG nest groups — flat 2-group only. `(A OR B) AND (C OR D)` is NOT supported.
- Each group max 1 `scenario` filter (LME limitation).
- Nếu cả `and` và `or` đều empty → omit `filters` parameter entirely thay vì pass `{and:[], or:[]}`.

---

### 5.2. Filter types — detailed

> **_ID_RESOLUTION_RULE (chung mọi type có ID)**: user đưa **TÊN** → gọi list tool tương ứng resolve name → id, fill
> field hiển thị. User đưa **RAW ID** → SKIP list tool; chỉ fill field ID, **để trống** field hiển thị
> (`tag_names=[]`, `scenario_name=""`, `qr_names=[]`, `preview_original=""`) — server validate ownership và tự
> enrich display fields từ DB lúc submit.
>
> **NO-ITEM RULE (chung)**: user KHÔNG chỉ định item nào (không tên, không ID) → **STOP và hỏi** user chọn. KHÔNG gọi
> list tool để tự chọn bừa / lấy toàn bộ ID.

#### `tag` (f1)

**Description**: Filter by tag.

| Field           | Description                                                                                                                                                                         |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `tags_search`   | array\<int\> — Tag IDs. Khi user nhắc multiple tags cùng intent, đặt ALL IDs vào single array — KHÔNG emit multiple tag filters cùng `tag_condition`                                |
| `tag_condition` | string — 1 trong 4 values: `has_any`, `has_all`, `exclude_any`, `exclude_all`                                                                                                       |
| `tag_names`     | array\<string\> — Tag names tương ứng `tags_search`. **OPTIONAL** — chỉ fill khi AI resolve ID từ tên qua `list_tags`. User đưa raw ID → pass `tag_names=[]` (server validate + enrich) |

`tag_condition` values:

- `has_any` → friends có ANY ONE tags (OR within tags). User says: `'có 1 trong các tag'`, `'có tag A hoặc B hoặc C'`.
- `has_all` → friends có ALL tags (AND within tags). User says: `'có cả A và B và C'`, `'có tất cả tag'`.
- `exclude_any` → EXCLUDE friends có ANY ONE tags. User says: `'không có A, B, C nào cả'`,
  `'loại trừ friend dính 1 trong các tag'`.
- `exclude_all` → EXCLUDE friends có ALL tags (friend missing at least one). User says: `'thiếu ít nhất 1 trong A,B,C'`,
  `'không có đủ cả A và B'`.

**Merging rule**: For ONE intent với multiple tags, emit ONE filter với `tags_search=[A,B,C]`. Splitting into multiple
filters cùng `tag_condition` trong cùng group là FORBIDDEN.

**Example single intent**:
`{type:'tag', tags_search:[24933,24934,24935], tag_condition:'has_any', tag_names:['VIP','NEW','GOLD']}`

**Example mixed intent**: `'có VIP nhưng loại BLACKLIST'` → 2 filters với DIFFERENT `tag_condition` trong cùng `'and'`
group: `[{has_any,[VIP]}, {exclude_any,[BLACKLIST]}]`.

---

#### `friend_name` (f2)

**Description**: Filter by display name (LIKE %keyword%). Server splits `keyword` by whitespace và OR's LIKE clauses
internally.

> IMPORTANT: For ANY `'name contains A or B / A,B / A hoặc B / A、B'` phrasing, ALWAYS send ONE filter với
> `keyword='A B'` (space-separated). DO NOT split into multiple `friend_name` filters under `'and'` — that produces
> AND semantics (rarely what user wants). Only split into multiple filters khi user EXPLICITLY says `'BOTH A AND B'`
> (rare).

| Field         | Description                                                                                                                                                                                           |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `keyword`     | string — Space-separated name fragments. Server normalizes `' or '` / `','` / `'、'` separators sang space, nhưng PREFER sending already-normalized space-separated. KHÔNG wrap fragments trong quotes |
| `search_from` | array\<string\> — Fields to search: `['line_name']` (LINE name only), `['system_name']` (system name only), `['line_name', 'system_name']` (DEFAULT)                                                  |

**`search_from` selection:**

- `['line_name']` — User explicitly mention LINE name (`'tên LINE'`, `'LINE name'`).
- `['system_name']` — User explicitly mention system name (`'tên hệ thống'`, `'system name'`).
- `['line_name', 'system_name']` — DEFAULT khi user chỉ nói `'tên là...'` hoặc `'có tên'`.

**Examples:**

- 2 names OR: `{keyword:'tanaka suzuki', search_from:['line_name','system_name']}`
- 3 names OR: `{keyword:'thom テスト yamada', search_from:['line_name']}`
- Single: `{keyword:'test', search_from:['line_name','system_name']}`

---

#### `day_add_friend` (f3)

**Description**: Filter by date user added bot as friend. Two modes: `date_range` (absolute dates) hoặc `duration` (
relative days ago).

**Strict rules:**

- ONLY include fields user EXPLICITLY mentioned. DO NOT auto-fill defaults.
- DO NOT set `add_to_date` = today trừ khi user said `'đến hôm nay'` / `'tới nay'` / `'until today'`.
- DO NOT set `duration_day_start` hoặc `duration_day_end` = `0` trừ khi user said.
- DO NOT emit empty string `""` either — omit key entirely nếu không mentioned.
- Mixing modes là FORBIDDEN — pick ONE of `date_range` hoặc `duration`.

**Mode `date_range`:**

| Field             | Description                                                                                                        |
|-------------------|--------------------------------------------------------------------------------------------------------------------|
| `day_filter_type` | `"date_range"` (required)                                                                                          |
| `add_from_date`   | string `YYYY-MM-DD` — OPTIONAL. Chỉ include khi user mention start date (`'từ ngày X'` / `'sau X'` / `'from X'`)   |
| `add_to_date`     | string `YYYY-MM-DD` — OPTIONAL. Chỉ include khi user mention end date (`'đến ngày Y'` / `'trước Y'` / `'until Y'`) |

**Mode `duration`:**

| Field                | Description                                                                                                             |
|----------------------|-------------------------------------------------------------------------------------------------------------------------|
| `day_filter_type`    | `"duration"` (required)                                                                                                 |
| `duration_day_start` | integer — OPTIONAL. Min days ago. Chỉ include khi user mention lower bound (`'trên X ngày'` / `'hơn X ngày'`)           |
| `duration_day_end`   | integer — OPTIONAL. Max days ago. Chỉ include khi user mention upper bound (`'trong X ngày gần đây'` / `'dưới X ngày'`) |

**Few-shot examples:**

| User prompt                                        | Filter                                                                                                        | Note                                       |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| `Gửi cho friend thêm từ ngày 2025-12-01`           | `{type:'day_add_friend', day_filter_type:'date_range', add_from_date:'2025-12-01'}`                           | User chỉ nói `'từ'` → CHỈ `add_from_date`  |
| `Gửi cho friend thêm trước ngày 2025-12-01`        | `{type:'day_add_friend', day_filter_type:'date_range', add_to_date:'2025-12-01'}`                             | User chỉ nói `'trước'` → CHỈ `add_to_date` |
| `Gửi cho friend thêm từ 2025-10-01 đến 2025-12-01` | `{type:'day_add_friend', day_filter_type:'date_range', add_from_date:'2025-10-01', add_to_date:'2025-12-01'}` | Có cả `'từ'` và `'đến'`                    |
| `Gửi cho friend thêm trên 7 ngày`                  | `{type:'day_add_friend', day_filter_type:'duration', duration_day_start:7}`                                   | CHỈ `duration_day_start`                   |
| `Gửi cho friend mới thêm trong 30 ngày gần đây`    | `{type:'day_add_friend', day_filter_type:'duration', duration_day_end:30}`                                    | CHỈ `duration_day_end`                     |
| `Gửi cho friend thêm từ 7 đến 30 ngày`             | `{type:'day_add_friend', day_filter_type:'duration', duration_day_start:7, duration_day_end:30}`              | Cả 2 fields                                |

---

#### `scenario` (f4)

**Description**: Filter by scenario subscription status — max 1 per AND/OR group. ID-RESOLUTION per
_ID_RESOLUTION_RULE: user đưa TÊN → `list_scenarios` resolve name → id, fill `scenario_name`. User đưa RAW ID → skip
`list_scenarios`; chỉ fill `scenario_search`, **để `scenario_name=""`** — server validate ownership + enrich từ DB.

| Field                | Description                                                                                                          |
|----------------------|------------------------------------------------------------------------------------------------------------------------|
| `scenario_search`    | int — Scenario ID. Resolve qua `list_scenarios` khi user đưa tên; raw ID → dùng trực tiếp                            |
| `scenario_name`      | string — Scenario name. Copy từ `list_scenarios` NẾU user đưa tên; **ĐỂ TRỐNG `""`** nếu user đưa raw ID (server enrich). Display-only |
| `scenario_condition` | string — 1 trong 5 values                                                                                            |
| `number_of_days`     | integer — Required khi `scenario_condition='sent_within_days'`                                                       |

`scenario_condition` values:

- `subscribed` → Friends đang chạy scenario. User says: `'đang chạy scenario'`.
- `not_subscribed` → Friends không subscribed (including never added và stopped). User says: `'không đăng ký'`,
  `'chưa được add'`, `'đã stop/dừng'`.
- `sent_within_days` → Friends được sent messages tới specific day. User says: `'được gửi msg đến ngày xxx'`. Requires
  `number_of_days`.
- `completed` → Friends đã complete scenario. User says: `'đã hoàn thành'`.
- `not_completed` → Friends chưa complete. User says: `'chưa hoàn thành'`.

**Example**:
`{type:'scenario', scenario_search:'42', scenario_name:'Welcome Flow', scenario_condition:'sent_within_days', number_of_days:7}`

**Strict rules:**

- **NO-ITEM rule**: user không chỉ định scenario nào (tên/ID) → STOP và hỏi. KHÔNG gọi `list_scenarios` để tự chọn
  hoặc fill nhiều ID.
- ID resolution per _ID_RESOLUTION_RULE ở trên.

---

#### `qr_code` (f5)

**Description**: Filter by QR code scan history.

| Field          | Description                                                                                                                          |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `qrs_search`   | array\<int\> — QR code IDs. Multiple QR cùng intent → ALL IDs trong single array                                                     |
| `qr_condition` | string — `scanned_any` hoặc `never_scanned`                                                                                          |
| `qr_names`     | array\<string\> — QR names. Copy từ `list_traffic_sources` NẾU user đưa tên; **`[]`** nếu user đưa raw IDs (server enrich lúc submit) |

`qr_condition` values:

- `scanned_any` → Friends có ≥1 of selected QR actions. User says: `'đã quét 1 trong các mã'`, `'quét QR A hoặc B'`.
- `never_scanned` → EXCLUDE friends có ≥1 of selected. User says: `'chưa quét mã nào'`, `'loại trừ user đã quét mã'`.

**Merging rule**: ONE intent multiple QR → ONE filter với `qrs_search=[A,B,C]`.

**Examples:**

- Single intent: `{type:'qr_code', qrs_search:[10,20], qr_condition:'scanned_any', qr_names:['QR Shop A','QR Shop B']}`
- Mixed intent: `'đã quét QR A nhưng loại người đã quét QR B'` → `[{scanned_any,[A]}, {never_scanned,[B]}]`.

**Strict rules:**

- **NO-ITEM rule**: user không chỉ định QR nào → STOP và hỏi. KHÔNG gọi `list_traffic_sources` lấy toàn bộ ID.
- ID resolution per _ID_RESOLUTION_RULE.

---

#### `friend_info` (f6)

**Description**: Filter by friend info field. ID-RESOLUTION per _ID_RESOLUTION_RULE cho **CUSTOM fields (id>0)**: user
đưa TÊN → `list_friend_info_fields` resolve name → id + type_data. User đưa RAW CUSTOM ID → skip list; fill
`info_search=<id>`, `is_default=0`, để `title=""`, `type_data=0`, `valueOption=[]` — server validate ownership và
**enrich title/type_data/valueOption từ DB** lúc submit. Với **BUILT-IN fields (id<0)** mapping bên dưới là
DETERMINISTIC (không cần list call).

DETECT built-in vs custom by `id` (NOT title — custom fields có thể share names với built-in):

- `id<0` → BUILT-IN (`is_default=1`)
- `id>0` → CUSTOM (`is_default=0`)

**BUILT-IN id-to-info_search mapping (2 groups):**

- (A) Cross fields `{-1,-2,-3,-4,-6}` → `'d_'` + abs(id) as quoted string. Vd `id=-4` → `"d_4"`.
- (B) Address fields `{-7,-8,-9,-10}` → KEEP NEGATIVE as quoted string. Vd `id=-7` → `"-7"` (NOT `"d_7"`).

**`type_data` string→int mapping từ list tool:**

- `'input'` → 2
- `'calendar'` → 3
- `'select'` → 1
- `'point'` → 6

> **SPECIAL `d_5` (Tuổi/age)**: built-in point-type (`type_data=6`) mà `list_friend_info_fields` **KHÔNG trả về** —
> khi user hỏi theo tuổi/age, build trực tiếp `is_default=1, info_search="d_5", type_data=6` không cần consult list.

> Bots thường tạo custom fields tên overlap với built-in (vd custom `'生年月日'` override system birthday). Rule
> id-based naturally handle: nếu list return `id>0` cho title đó, nó là custom.

#### Filter `friend_info` fields

| Field                             | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `is_default`                      | int — DERIVED từ `id`: id<0→1, id>0→0. EXCEPTION: hỏi theo tuổi → `is_default=1` trực tiếp (d_5 không có trong list)                                                                                                                                                                                                                                                                                                                                        |
| `info_search`                     | string\|int — (A) `id ∈ {-1,-2,-3,-4,-6}` → quoted `'d_'+abs(id)` (`d_1` display name, `d_2` phone, `d_3` email, `d_4` birthday, `d_6` prefecture). (B) `id ∈ {-7,-8,-9,-10}` → quoted str(id) keeping minus (`-7` zip, `-8` district, `-9` township, `-10` building). (C) `id>0` → numeric unquoted. (D) `'d_5'` (age, point) không có trong list — dùng trực tiếp khi user hỏi tuổi                                                                       |
| `title`                           | string — `title` field từ list. Raw custom ID → để `""` (server enrich)                                                                                                                                                                                                                                                                                                                                                                                     |
| `type_data`                       | int — From list's `typeData` STRING → int mapping. (Note: list trả built-in birthday là `typeData='calendar'`, NOT `'date'`.) d_5 (age) không có trong list → dùng `6` trực tiếp                                                                                                                                                                                                                                                                            |
| `op_compare`                      | STRING (quoted, e.g. `"1"`) — Comparison operator. MUST be quoted string, NOT unquoted int                                                                                                                                                                                                                                                                                                                                                                  |
| `active`                          | boolean — `true`                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `keyword`                         | string — Used cho text (type 2) khi `op_compare` 1/2/3/4. Empty `''` khi `op_compare` 5/6 và non-text types                                                                                                                                                                                                                                                                                                                                                 |
| `point`                           | string — Used cho point (type 6) khi `op_compare` 1..5. Empty khi 6/7 và non-point types                                                                                                                                                                                                                                                                                                                                                                    |
| `selected_op`                     | array\<string\> — Used cho select (type 1) khi `op_compare` 1/2. **Put ALL selected option values vào MỘT array** trong ONE filter record — KHÔNG split thành nhiều rows OR. Empty `[]` khi 3/4 và non-select types. **EXACT-MATCH RULE**: mỗi entry MUST byte-match một `setting_value.setting_actions[].value` từ `list_friend_info_fields` (no trim, no case-fold). Mismatch → STOP, hỏi user pick. Xem [§type_1_select](#type_1_select-typedataselect) |
| `valueOption`                     | array of `{action_id, value, id}` — Used cho select (type 1). Build bằng cách copy `setting_value.setting_actions[]` từ `list_friend_info_fields` **VERBATIM** — KEEP all 3 fields including `action_id` (usually `''`), `value`, `id`. **PRESERVE** `value` exact (no trim, no case-fold). Empty `[]` cho non-select types. Riêng `d_6` (prefecture): fixed list 47 tỉnh JP — xem type_1_select                                                            |
| `limit_date`                      | int — Used cho date (type 3). `0`=exact date, `1`=date range. `0` otherwise                                                                                                                                                                                                                                                                                                                                                                                 |
| `year` / `month` / `day`          | string — Date exact hoặc range start. Empty otherwise                                                                                                                                                                                                                                                                                                                                                                                                       |
| `year_to` / `month_to` / `day_to` | string — Date range end. Empty otherwise                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `preview_original`                | string — Empty `''`                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `friend_info_id`                  | the custom field `id` (numeric, unquoted) từ list                                                                                                                                                                                                                                                                                                                                                                                                           |

#### Type-specific rules

##### `type_2_text` (typeData='input')

When: built-in `d_1/d_2/d_3` (cross, id=-1/-2/-3), `-7..-10` (address), hoặc custom id>0.
`type_data`: `2`

| `op_compare` | Meaning                                                         |
|--------------|-----------------------------------------------------------------|
| `1`          | Exact match: `value = 'xxx'` (requires `keyword`)               |
| `2`          | Contains: `value LIKE '%xxx%'` (requires `keyword`)             |
| `3`          | Not exact: `value <> 'xxx'` (requires `keyword`)                |
| `4`          | Does not contain: `value NOT LIKE '%xxx%'` (requires `keyword`) |
| `5`          | HAS VALUE — `keyword` MUST be `''`                              |
| `6`          | NO VALUE — `keyword` MUST be `''`                               |

**Example custom**:
`{"type":"friend_info","active":true,"is_default":0,"info_search":1615,"title":"Số điện thoại","type_data":2,"op_compare":2,"keyword":"090","valueOption":[],"selected_op":[],"point":"","limit_date":0,"year":"","month":"","day":"","year_to":"","month_to":"","day_to":"","preview_original":""}`

**Example built-in**:
`{"type":"friend_info","active":true,"is_default":1,"info_search":"d_3","title":"Email","type_data":2,"op_compare":2,"keyword":"gmail.com",...}`

##### `type_6_point` (typeData='point')

When: `list_friend_info_fields` trả `typeData='point'` (custom, id>0). **Built-in `d_5` (Tuổi/age) KHÔNG được list
trả về** — user hỏi theo tuổi → dùng trực tiếp `is_default=1, info_search='d_5', type_data=6`.
`type_data`: `6`

| `op_compare` | Meaning                          |
|--------------|----------------------------------|
| `1`          | `= value` (requires `point`)     |
| `2`          | `>= value` (requires `point`)    |
| `3`          | `> value` (requires `point`)     |
| `4`          | `<= value` (requires `point`)    |
| `5`          | `< value` (requires `point`)     |
| `6`          | HAS VALUE — `point` MUST be `''` |
| `7`          | NO VALUE — `point` MUST be `''`  |

**Example custom**:
`{"type":"friend_info","active":true,"is_default":0,"info_search":888,"title":"Điểm tích luỹ","type_data":6,"op_compare":2,"point":"100","keyword":"",...}`

**Example built-in (tuổi ≥ 20)**:
`{"type":"friend_info","active":true,"is_default":1,"info_search":"d_5","title":"Tuổi","type_data":6,"op_compare":2,"point":"20","keyword":"",...}`

##### `type_3_date` (typeData='calendar')

When: built-in `d_4` (birthday, id=-4) hoặc custom date.
`type_data`: `3`

| `op_compare` | Meaning                                                                                                   |
|--------------|-----------------------------------------------------------------------------------------------------------|
| `1`          | Compare date. `limit_date=0` → exact (year/month/day). `limit_date=1` → range (+ year_to/month_to/day_to) |
| `2`          | HAS VALUE — all date fields MUST be `''`                                                                  |
| `3`          | NO VALUE — all date fields MUST be `''`                                                                   |

**Example custom**:
`{"type":"friend_info","active":true,"is_default":0,"info_search":885,"title":"Ngày sinh","type_data":3,"op_compare":1,"limit_date":0,"year":"2026","month":"10","day":"04","year_to":"","month_to":"","day_to":"",...}`

**Example built-in (range)**:
`{"type":"friend_info","active":true,"is_default":1,"info_search":"d_4","title":"Ngày sinh","type_data":3,"op_compare":1,"limit_date":1,"year":"1995","month":"01","day":"01","year_to":"1995","month_to":"12","day_to":"31",...}`

##### `type_1_select` (typeData='select')

When: built-in `d_6` (prefecture, id=-6) hoặc custom select.
`type_data`: `1`

| `op_compare` | Meaning                                        |
|--------------|------------------------------------------------|
| `1`          | IN selected (requires `selected_op` array)     |
| `2`          | NOT IN selected (requires `selected_op` array) |
| `3`          | HAS VALUE — `selected_op` MUST be `[]`         |
| `4`          | NO VALUE — `selected_op` MUST be `[]`          |

**Example custom (single option)**:
`{"type":"friend_info","active":true,"is_default":0,"info_search":883,"title":"Nghề nghiệp","type_data":1,"op_compare":1,"selected_op":["Option 1"],"valueOption":[{"action_id":"","value":"Option 1","id":503}],...}`

**Example custom (MULTI option — STRICT)**:
User filter: *"lọc friend đã chọn N info select 1 HOẶC N info select 2 HOẶC N info select 3"* → **ONE filter record**
với `selected_op` array chứa TẤT CẢ options, **KHÔNG** tách thành 3 friend_info rows.

`{"type":"friend_info","active":true,"is_default":0,"info_search":3981,"title":"N info select","type_data":1,"op_compare":1,"selected_op":["N info select 1","N info select 2","N info select 3"],"valueOption":[{"action_id":"","value":"N info select 1","id":4784},{"action_id":"","value":"N info select 2","id":4785},{"action_id":"","value":"N info select 3","id":4786}],"keyword":"","point":"","limit_date":0,...}`

**Example built-in (prefecture)**:
`{"type":"friend_info","active":true,"is_default":1,"info_search":"d_6","title":"Tỉnh/Thành phố","type_data":1,"op_compare":1,"selected_op":["福島県","茨城県"],"valueOption":["北海道","青森県",...47 tỉnh...],...}`

> **`d_6` HARDCODED RULE**: prefecture là BUILT-IN — KHÔNG gọi `list_friend_info_fields`. `valueOption` là **FIXED
> list 47 tỉnh Nhật** (`"北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"`)
> — copy VERBATIM vào `valueOption`. `selected_op` = subset user chọn, mỗi entry EXACT-MATCH (byte-for-byte) 1 trong
> 47 string. **LUÔN dùng tên tiếng Nhật** (`'東京都'`, `'大阪府'`...) — KHÔNG dịch sang EN/VN (NOT `'Tokyo'`). User
> nói `'Tokyo'` → map thành `'東京都'`. User nói city không nằm trong 47 → STOP, hỏi user clarify tên tỉnh JP.

> **STRICT multi-option rule**: Khi user filter theo NHIỀU option của CÙNG 1 select field → build **ONE friend_info
filter record** với tất cả options trong `selected_op` array. **NEVER** split thành nhiều filter records joined by OR.
>
> **ANTI-PATTERN (past bug)**: AI build
`filters.or = [{friend_info, info_search:3981, keyword:"N info select 1"}, {friend_info, info_search:3981, keyword:"N info select 2"}]` —
> sai vì: (a) select-type filters dùng `selected_op` array, **không phải `keyword`**; (b) multi-option phải là ONE record,
**không phải multiple OR'd records**. `filters_v2` table khi đó lưu 2 rows với `OR` op → mismatch với web (web lưu 1
> row).
>
> **STRICT setting_value rule (custom select)**: TRƯỚC khi build → `list_friend_info_fields(titles=[<field>])` → đọc
> `setting_value.setting_actions[]` → (a) `valueOption` = copy VERBATIM `[{action_id, value, id}]`; (b) `selected_op`
> mỗi entry byte-match `setting_actions[].value`. DB có thể lưu value chứa whitespace literal — NEVER trim/normalize.

---

#### `bot_new_friend` (f7)

**Description**: Filter by new vs existing friend.

| Field                 | Description                    |
|-----------------------|--------------------------------|
| `select_value_friend` | string — `'new' \| 'existing'` |

**Example**: `{type:'bot_new_friend', select_value_friend:'new'}`

---

#### `status_search` (f8)

**Description**: Filter by SCENARIO CONFIRMATION status (確認/未確認 — friend đã xác nhận flow scenario chưa).

> DO NOT confuse với `'status_chat'` filter — that one is for handling/response status (対応ステータス /
> `status_chat` table) and requires `status_chat.id`. This filter only takes `'confirm'` \| `'unconfirm'` — NO IDs,
> NO list call required.

| Field                     | Description                         |
|---------------------------|-------------------------------------|
| `status_search_condition` | string — `'unconfirm' \| 'confirm'` |

**Example**: `{type:'status_search', status_search_condition:'unconfirm'}`

---

#### `conversion` (f10)

**Description**: Filter friends by conversion access. ID-RESOLUTION per _ID_RESOLUTION_RULE: user đưa TÊN →
`list_conversions(bot_id)` resolve name → id, fill `preview_original` + `open_group`. User đưa RAW ID → skip
`list_conversions`; chỉ fill `conversion_search`, để `preview_original=""`, `open_group=0` — server validate ownership
và enrich `preview_original` (joined names) + `open_group` từ DB lúc submit.

> TYPES NOT UNIFORM: include uses INT `conversion_condition=0`; exclude uses STRING `conversion_condition="1"`.

| Field                  | Description                                                                                                         |
|------------------------|---------------------------------------------------------------------------------------------------------------------|
| `active`               | bool — always `true`                                                                                                |
| `conversion_search`    | string — `conversion.id` as STRING. Single: `"1180"`. Multiple (CSV): `"1189,1190"`. Friend matches if accessed ALL |
| `conversion_condition` | int\|string — INT `0` = include, STRING `"1"` = exclude                                                             |
| `open_group`           | int — `category.id` reference (từ `list_conversions.categories[].category_id`) — xem resolution rule bên dưới       |
| `preview_original`     | string — Single: just name (e.g. `'タイプ2'`). Multiple: join names with `'・'` (e.g. `'c2・c2 cop'`)                    |

**Examples:**

- Include single:
  `{type:'conversion', active:true, conversion_search:'456', conversion_condition:0, open_group:0, preview_original:'タイプ2'}`
- Exclude single:
  `{type:'conversion', active:true, conversion_search:'456', conversion_condition:'1', open_group:0, preview_original:'タイプ2'}`
- Include multi (same category):
  `{type:'conversion', active:true, conversion_search:'1189,1190', conversion_condition:0, open_group:6834, preview_original:'c2・c2 cop'}`
- Include multi (CROSS category — được phép): conv 1189 (category 6834) + conv 1196 (category 6835) →
  `open_group` có thể là 6834 **hoặc** 6835 — pick ANY non-zero:
  `{type:'conversion', active:true, conversion_search:'1189,1196', conversion_condition:0, open_group:6834, preview_original:'c2・コンバージョン4'}`
- Include multi (mix có uncategorized): conv 1189 (6834) + conv 1200 (category 0) → `open_group` MUST 6834 (non-zero):
  `{type:'conversion', active:true, conversion_search:'1189,1200', conversion_condition:0, open_group:6834, preview_original:'c2・root conv'}`
- Include multi (ALL uncategorized) → `open_group=0`:
  `{type:'conversion', active:true, conversion_search:'1200,1201', conversion_condition:0, open_group:0, preview_original:'conv root1・conv root2'}`

**Strict rules:**

- **NO-ITEM rule**: user không chỉ định conversion nào → STOP và hỏi. KHÔNG lấy toàn bộ ID.
- ID resolution per _ID_RESOLUTION_RULE (raw ID → `preview_original=""`, `open_group=0`, server enrich).
- `conversion_condition`: INT 0 include, STRING `"1"` exclude. DO NOT mix.
- `conversion_search` MUST be STRING (not int, not array). Multi = comma-separated NO spaces.
- **`open_group` resolution (cross-category ĐƯỢC PHÉP)**: (a) single conversion → category_id của nó; (b) multi cùng
  category → shared category_id; (c) multi KHÁC category → pick ANY ONE non-zero category_id (thứ tự không quan
  trọng) — **ưu tiên non-zero**: chỉ cần ≥1 conversion có category_id > 0 thì `open_group` PHẢI non-zero; (d) tất cả
  uncategorized (mọi category_id=0) → `open_group=0`.
- `preview_original`: Single = exact name. Multiple = names joined với `'・'` (Japanese middot). Order khớp
  `conversion_search`.

---

#### `affiliate` (f9)

**Description**: Filter friends by which affiliate referred them. ID-RESOLUTION per _ID_RESOLUTION_RULE: user đưa
TÊN/username → `list_affiliates(bot_id)` resolve → id, fill `preview_original`. User đưa RAW ID → skip
`list_affiliates`; chỉ fill `affiliate_search`, để `preview_original=""` — server validate + enrich.

> TYPES NOT UNIFORM: include INT `affiliate_filter_type=0`; exclude STRING `affiliate_filter_type="1"`.

| Field                   | Description                                                                                                              |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------|
| `active`                | bool — always `true`                                                                                                     |
| `affiliate_search`      | array of int — `affiliate.id` list. OR-joined                                                                           |
| `affiliate_filter_type` | int\|string — INT `0` = include, STRING `"1"` = exclude                                                                  |
| `preview_original`      | string — Single: username (e.g. `'phuongthanh_aff2'`). Multiple: join với `'・'` (e.g. `'Thanhntp_edit11ttttt・test aff'`) |

**Examples:**

- Include single:
  `{type:'affiliate', active:true, affiliate_search:[8], affiliate_filter_type:0, preview_original:'phuongthanh_aff2'}`
- Exclude single:
  `{type:'affiliate', active:true, affiliate_search:[11], affiliate_filter_type:'1', preview_original:'thanhntp142'}`
- Include multi:
  `{type:'affiliate', active:true, affiliate_search:[44,48], affiliate_filter_type:0, preview_original:'Thanhntp_edit11ttttt・test aff'}`

**Strict rules:**

- **NO-ITEM rule**: user không chỉ định affiliate nào → STOP và hỏi.
- ID resolution per _ID_RESOLUTION_RULE.
- `affiliate_filter_type`: INT 0 include, STRING `"1"` exclude.
- `affiliate_search` MUST array of int (e.g. `[8]` hoặc `[8,11]`) — kể cả 1 item.
- `preview_original`: Single = exact username. Multiple = usernames joined với `'・'` (Japanese middot, NOT comma, NOT
  space). Order khớp `affiliate_search`.

---

#### `status_chat` (f11)

**Description**: Filter friends by which handling (response) status (対応ステータス / `status_chat` table) is
currently attached.

> - DO NOT confuse với `'status_search'` filter — that one is scenario CONFIRMATION (`confirm/unconfirm`), no IDs.
> - DO NOT confuse với action `'handling_status'` (step trong action chain) — that ATTACHES/DETACHES status; this
>   FILTERS recipients by current status.

ID-RESOLUTION per _ID_RESOLUTION_RULE: user đưa TÊN → `list_handling_statuses(bot_id)` resolve name → id, fill
`preview_original`. User đưa RAW ID → skip list; chỉ fill `status_chat_search`, **để `preview_original=""`** — server
validate ownership và enrich từ DB lúc submit.

| Field                     | Description                                                                                                             |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `active`                  | bool — always `true`                                                                                                    |
| `status_chat_search`      | array of int — `status_chat.id` list. OR-joined                                                                         |
| `status_chat_filter_type` | int\|string — INT `0` = include (`Những friend có gắn 1 trong các status đã chọn`), STRING `"1"` = exclude (`Loại trừ`) |
| `preview_original`        | string — Single: name (e.g. `'3'`). Multiple: join với `'・'` (e.g. `'未対応・対応中'`)                                         |

**Examples:**

- Include single:
  `{type:'status_chat', active:true, status_chat_search:[4975], status_chat_filter_type:0, preview_original:'3'}`
- Exclude single:
  `{type:'status_chat', active:true, status_chat_search:[4926], status_chat_filter_type:'1', preview_original:'1'}`
- Include multi:
  `{type:'status_chat', active:true, status_chat_search:[4578,4579], status_chat_filter_type:0, preview_original:'未対応・対応中'}`

**Strict rules:**

- ID resolution per _ID_RESOLUTION_RULE (raw ID → `preview_original=""`, server enrich).
- `status_chat_filter_type`: INT 0 include, STRING `"1"` exclude.
- `status_chat_search` MUST array of int — kể cả 1 item.
- `preview_original`: Single = exact name từ `list_handling_statuses`. Multiple = names joined với `'・'`. Order khớp
  `status_chat_search`.

---

### 5.3. Filter disambiguation

| Pair                                                 | Phân biệt                                                                                                                                                                                                                                 |
|------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `status_search` vs `status_chat`                     | `status_search` = SCENARIO CONFIRMATION state (`confirm/unconfirm` string, no IDs, no list call). `status_chat` = HANDLING/RESPONSE STATUS (対応ステータス) attached to friend — requires `status_chat.id` từ `list_handling_statuses`      |
| `handling_status` (action) vs `status_chat` (filter) | `handling_status` (step trong action chain của broadcast / template detail_action) = ATTACH or DETACH status to user. `status_chat` (trong filter) = SELECT recipients by current attached status. Different concepts — never swap        |
| `tag` vs `status_chat`                               | `tag` = arbitrary multi-label admin attaches via `tag_users` (1 friend → many tags). `status_chat` = single response-status state per friend (1 friend → at most 1 active status_chat)                                                    |
| `conversion` vs `scenario`                           | `conversion` = friend đã access conversion URL (`list_conversions`). `scenario` = friend đang ở scenario nào (`list_scenarios`)                                                                                                           |

---

## 6. Post-send action — `action_id`

> **THAY ĐỔI LỚN so với bản cũ**: `create_broadcast` KHÔNG còn nhận array `actions` (typed
> `List<BroadcastAction>` flat `{type, data}`). Post-send action giờ gắn **theo tham chiếu** qua param **`action_id`**
> — ID của action chain tạo bằng tool **`create_action`**. (Tool cũ `edit_broadcast_action` cũng đã disable —
> consolidated vào `update_broadcast`.)

### Cơ chế REFERENCE (verified 2026-09-16)

1. MCP fetch chain qua `/mcp/get-action` — check tồn tại + bot scope + **per-type allowlist**.
2. Stamp chain id lên mọi detail row rồi forward làm `actions` — backend detect shared id, **re-save CÙNG chain
   in-place** (rows giữ DB id) và broadcast mới **link tới chain gốc**.
3. Hệ quả: `update_action` sửa chain sau này **áp dụng luôn** cho broadcast này (reference semantics, không phải
   copy). (Khác `update_broadcast` action section — bên đó là COPY semantics lên chain riêng của broadcast.)

### Ràng buộc

- `action_id` phải là **số dương** — id trả về từ `create_action`. Omit khi không có post-send action.
- **Step types cho phép trong chain**: `tag`, `scenario`, `richmenu`, `friend_info`, `block`, `bookmark`,
  `handling_status` (wire DB = `compliant_status`). Chain chứa step **`text`** (hoặc type ngoài allowlist, vd
  `template`) → reject: *"details[i].type='...' is not supported for broadcast post-send actions"*.
- `templates` vẫn REQUIRED kể cả khi có `action_id`.

### Flow chuẩn

1. `create_action(bot_id, type, details)` — `details` = array **`DetailAction`** typed:
   `{ type (required — tag | scenario | richmenu | text | bookmark | friend_info | block | handling_status | template),
   data (required — typed `ActionData`, fill ONLY field group của type đó: tag→`ids`/`tagAction`;
   scenario→`scenarioId`/`scenarioAction`/`startDay`/`scenarioName`; richmenu→`richmenuId`/`richmenuAction`/`richmenuName`;
   bookmark→`bookmarkAction`; block→`blockAction`; handling_status→`handlingStatusId`/`handlingStatusAction`/`handlingStatusName`;
   friend_info→`friendInfo` nested), title?, active?, isEditContent?, id?, actionId? }`. Với chain dùng cho broadcast →
   chỉ dùng 7 type trong allowlist ở trên. Response trả `action_id`.
2. `create_broadcast(..., action_id=<id>)`.
3. Muốn sửa action sau này → `update_action(action_id, details)` — **FULL-STATE replace** (details gửi lên thay thế
   toàn bộ; item thiếu = bị xoá; item giữ phải gửi kèm detail `id`).

> **Naming**: AI-facing token là `handling_status`; backend lưu `t_actions_detail.type='compliant_status'` (legacy
> wire value). Cả 2 đều được accept khi parse.

---

## 7. Sample requests

> Lưu ý: `filters` là **JSON string** — trong body JSON phải escape (ví dụ dưới viết dạng escaped string đúng như
> TestController / Postman nhận).

### Case 1 — Send now, text only, target VIP tag

```json
{
  "tool_name": "create_broadcast",
  "params": {
    "bot_id": "<hash>",
    "name": "Hello VIPs",
    "templates": [
      {
        "type": "text",
        "text": { "content": "Cảm ơn các bạn VIP!" }
      }
    ],
    "filters": "{\"and\":[{\"type\":\"tag\",\"tags_search\":[123],\"tag_condition\":\"has_any\",\"tag_names\":[\"VIP\"]}],\"or\":[]}"
  }
}
```

### Case 2 — Schedule once at 2026-05-07 10:00

```json
{
  "tool_name": "create_broadcast",
  "params": {
    "bot_id": "<hash>",
    "name": "Morning push",
    "send_day": "2026-05-07",
    "send_time": "10:00",
    "templates": [
      {
        "type": "text",
        "text": { "content": "おはようございます！" }
      }
    ]
  }
}
```

### Case 3 — Multi-schedule (typed `BroadcastSchedule` — key camelCase!)

```json
{
  "tool_name": "create_broadcast",
  "params": {
    "bot_id": "<hash>",
    "name": "Daily reminder x2",
    "schedules": [
      { "sendDay": "2026-05-07", "sendTime": "09:00" },
      { "sendDay": "2026-05-08", "sendTime": "09:00" }
    ],
    "templates": [
      {
        "type": "text",
        "text": { "content": "Daily reminder" }
      }
    ]
  }
}
```

### With post-send action — gửi xong gắn tag + bỏ handling status

Step 1 — tạo chain:

```json
{
  "tool_name": "create_action",
  "params": {
    "bot_id": "<hash>",
    "type": "broadcast_v2",
    "details": [
      { "type": "tag", "data": { "ids": [123], "tagAction": "add" } },
      { "type": "handling_status", "data": { "handlingStatusAction": "detach" } }
    ]
  }
}
```

→ response trả `action_id` (vd `4321`).

Step 2 — tạo broadcast tham chiếu chain:

```json
{
  "tool_name": "create_broadcast",
  "params": {
    "bot_id": "<hash>",
    "name": "Promo + tag + detach",
    "templates": [
      {
        "type": "text",
        "text": { "content": "Promo!" }
      }
    ],
    "action_id": 4321
  }
}
```

> Shape chi tiết của từng `details[].data` theo type nằm trong input schema typed của `create_action`
> (`DetailAction`/`ActionData`) — không thuộc scope file này.

### With image template

Step 1: gọi `get_file_params` với ảnh attach → `{download_url, file_id, img_width, img_height}`.

Step 2: dùng `download_url` làm `imgPath` trong typed payload:

```json
{
  "tool_name": "create_broadcast",
  "params": {
    "bot_id": "<hash>",
    "name": "Image campaign",
    "templates": [
      {
        "type": "image",
        "image": { "imgPath": "https://lme.../uploaded.jpg" }
      }
    ]
  }
}
```

Hoặc form subtype image (ảnh full-click):

```json
{
  "tool_name": "create_broadcast",
  "params": {
    "bot_id": "<hash>",
    "name": "Banner campaign",
    "templates": [
      {
        "type": "form",
        "form": {
          "subtype": "image",
          "panels": [
            {
              "imgPath": "https://lme.../uploaded.jpg",
              "buttons": [ { "url": "https://example.com/campaign" } ]
            }
          ]
        }
      }
    ]
  }
}
```

> ⚠️ `imgPath` PHẢI bằng `download_url` từ `get_file_params` ở step 1 — mọi URL khác đều invalid.

---

## 8. Output

Tool trả envelope passthrough từ backend: `{ "result": "ok", "data": { ...các field bảng dưới... }, "error": null }`
— các field chính nằm trong **`data`**:

| Name                   | Type   | Description                                                               |
|------------------------|--------|---------------------------------------------------------------------------|
| `id`                   | Int    | ID broadcast vừa tạo (parent)                                             |
| `child_ids`            | Array  | (Case 3) Danh sách ID child broadcast — mỗi `schedules` item 1 child      |
| `name`                 | String | Tên broadcast                                                             |
| `setting_send_message` | Int    | `0` = send-now, `1` = scheduled                                           |
| `created_at`           | String | yyyy-MM-dd HH:mm:ss                                                       |

> Confirm kết quả từ response này hoặc `list_broadcasts` (status, send_day, filter_number, template count) — chỉ báo
> user các giá trị thực trả về.

---

## 9. Notes / pitfalls

- **Templates đã typed** — AI KHÔNG còn build raw envelope (`message_button`, `list_panel`, `is_apply_*`, key
  ordering...). MCP layer (builders) tự sinh backend payload; AI chỉ fill typed fields (camelCase).
- **`actions` param không còn** — post-send action qua `action_id` (chain `create_action`, reference semantics).
  Action surfaces bên trong template (button `actions`, tap zone `actions`, URL `actions`, form `exceedActions`) cũng
  chỉ nhận **`{actionId}` (ActionRef)** — inline definition bị reject.
- **`filters` vẫn JSON-string** — validate shape server-side (`validateFilterChain`): required fields per type, enum
  values, non-empty list fields. Sai shape → validation error nêu rõ field/type sai.
- **Type mixing intentional trong filters** — include INT `0` / exclude STRING `"1"` cho
  `conversion_condition` / `affiliate_filter_type` / `status_chat_filter_type` (mirror web payload). DO NOT normalize.
- **`status_search` ≠ `status_chat`** — scenario confirmation vs handling status.
- **`handling_status` (action step) ≠ `status_chat` (filter)** — attach/detach vs select recipient. AI-facing token
  là `handling_status`; DB wire là `compliant_status`.
- **ID-resolution**: raw ID → không cần gọi list tool; server validate ownership (403 kèm list ID vi phạm group theo
  type) và enrich display fields từ DB. Tên → phải resolve qua list tool, check `not_found_names`.
- **Tag verify**: `list_tags(names:[...])` với EXACT match — check `not_found_names` trước khi gửi.
- **File upload**: 1 tool duy nhất `get_file_params` (các tool cũ `get_image_fileparams` / `get_audio_fileparams` /
  `get_video_fileparams` / `get_pdf_fileparams` đã disable — consolidated). Ảnh trả thêm `img_width`/`img_height`.
- **LIFF URL auto-resolve**: server tự đổi `?form_id=<N>` → `?unique_key=<key>` và placeholder `{LIFF}` → LIFF app id
  thật trong text content — AI không cần gọi `list_bots` trước để build form URL.
- **`ogp.imageUrl`** → server làm 1 HTTP HEAD validate URL (lý do openWorldHint=true).
- **Token server-side**: `{CURRENT_TS}` được server replace trước khi forward — đừng tự sinh timestamp.
- **Edit sau khi tạo**: dùng `update_broadcast` (info/template/schedules/action_id sections) và
  `update_filter(target=broadcast)` cho filters — các tool cũ `edit_broadcast_info` / `edit_broadcast_template` /
  `add_broadcast_template` / `edit_broadcast_filters` / `edit_broadcast_action` / `add_broadcast_schedule` /
  `delete_broadcast_template` đã disable. Xem [update_broadcast](#update_broadcast).
- **Error prefixes** (`VALIDATION_ERROR` / `IMAGE_URL_EXPIRED` / `LME_REJECTED` / `LME_REJECTED_RAW` /
  `LME_SERVER_ERROR`) — relay verbatim, xem [§4.7](#47-validation-server-side-vẫn-hard-enforce).


---

## Editable status — quy tắc chung

`update_broadcast` gọi `broadcastService.assertEditable(broadcast_id, bot_id)` trước khi chạy bất kỳ section nào:

| Status                                                     | Editable?                                         |
|------------------------------------------------------------|---------------------------------------------------|
| `draft` / `unregistered`                                   | ✅ Luôn được                                       |
| `wait_to_send`                                             | ✅ Chỉ khi còn **> 5 phút** đến giờ gửi (Japan TZ) |
| `delivering` / `delivered` / `not_delivery` / `send_false` | ❌ Server reject với `IllegalArgumentException`    |

> Với `wait_to_send` còn ≤ 5 phút: workaround DUY NHẤT là gọi `update_broadcast(send_day, send_time)` đẩy lịch
> ra xa hơn 5 phút rồi retry. KHÔNG có tool nào chuyển wait_to_send → draft.

---

## update_broadcast

**Description:** Tool cập nhật hợp nhất cho broadcast hiện có. Gửi bất kỳ tổ hợp nào của 5 section optional; các
section chạy theo **thứ tự cố định `info → schedules → template → template_id → action`** và **DỪNG ở lỗi đầu tiên** —
response chứa 1 key kết quả cho mỗi section đã chạy (`info`, `schedules`, `template`, `template_copy`, `action`). Nếu 1 section fail sau khi các
section trước đã thành công: thay đổi của các section trước **vẫn được lưu (không rollback)**, và response có thêm
`failed_section` (section bị lỗi), `error` (lý do), `sections_not_run` (các section phía sau bị bỏ qua) — sửa lỗi rồi
chỉ gửi lại section bị lỗi + các section chưa chạy. (Section đầu tiên đã fail thì trả lỗi thẳng, không có các key này.)

1. **info** — `name` / `send_day` / `send_time` / `setting_send_message` / `profile_id`: **ghi đè** các field đã lưu
   (chỉ gửi field cần đổi). `setting_send_message=0` (gửi ngay) → MCP tự set `send_day`/`send_time` = giờ Japan hiện
   tại — KHÔNG truyền kèm `send_day`/`send_time` (truyền kèm → lỗi validation). Gửi `send_day`/`send_time` = đặt lịch:
   không kèm `setting_send_message` thì MCP tự set `setting_send_message=1` (#41637); ngày giờ kết quả (phần không gửi
   giữ giá trị đang lưu) phải ở tương lai (Japan TZ), nếu không → lỗi validation.
2. **schedules** — **ADDITIVE**: mỗi item tạo 1 child broadcast độc lập, share templates của parent và copy
   filters/actions (tối đa 10/call; thời gian tương lai Japan TZ; duplicate trong list hoặc với schedule đã tồn tại bị
   reject).
3. **template** — 1 typed template payload: omit `broadcast_template_id` → **ADD** template mới; set
   `broadcast_template_id` (từ `list_broadcast_templates`) → **EDIT** template đó. Type không đổi được, và **các
   nested array (form buttons/detail_action, image-map items, text urls) bị REPLACE toàn bộ** — clone template hiện
   tại và gửi lại cả các phần không sửa. Khi payload có `ogp.imageUrl`, server thực hiện 1 HTTP HEAD request tới URL
   do caller cung cấp để kiểm tra kích thước ảnh. 1 broadcast chỉ có **tối đa 1 template quick reply** (form
   `quick_reply` / `quick_reply_image`) — thêm cái thứ 2 hoặc sửa template khác thành quick reply → lỗi (#41638).
4. **template_id** — copy 1 template có sẵn (từ `list_templates` — group template hoặc template đơn) vào broadcast,
   thành message mới ở cuối (#41645). Broadcast giữ bản copy riêng: sửa template gốc về sau KHÔNG ảnh hưởng broadcast;
   sửa bản copy bằng section template (`broadcast_template_id` lấy từ `list_broadcast_templates`). Không gửi cùng
   section template trong 1 call. Template con trong group → lỗi; áp dụng cả quy tắc 1 quick reply.
5. **action_id** — **REPLACE toàn bộ** post-send action set của broadcast bằng **COPY** các step của chain đó (tạo từ
   `create_action`). Step được copy vào chain riêng của broadcast, nên các sửa đổi `update_action` sau này trên chain
   nguồn **KHÔNG** lan sang broadcast này; `0` = xoá hết post-send actions.

Chỉ editable khi status là `draft`/`unregistered`, hoặc `wait_to_send` còn > 5 phút đến giờ gửi (Japan TZ). Filter của
broadcast update qua `update_filter(target=broadcast)`, không qua tool này. Sửa một broadcast đang ở `wait_to_send` sẽ **đổi thời điểm
người nhận LINE nhận tin** — chuyển sang `setting_send_message=0` thì MCP điền giờ JP hiện tại nên tin đi ngay.
Bản thân tool **không trực tiếp gửi** tin nào ra LINE.

**Tool:** `update_broadcast`

**Input:**
| Name | Type | Required | Description |
|---|---|---|---|
| bot_id | String | Yes | Bot ID hash string từ `list_bots` |
| broadcast_id | Long | Yes | Numeric broadcast id (từ `list_broadcasts.broadcasts[].id`) |
| name | String | No | [info] Tên quản trị mới (≤ 20 chars). Omit nếu không đổi |
| send_day | String | No | [info] Ngày gửi mới (`yyyy-MM-dd`). Gửi = chuyển sang đặt lịch (tự set `setting_send_message=1`); ngày giờ kết quả phải ở tương lai (Japan TZ). Omit nếu không đổi; không dùng cùng `setting_send_message=0` |
| send_time | String | No | [info] Giờ gửi mới (`HH:mm`). Gửi = chuyển sang đặt lịch (tự set `setting_send_message=1`); ngày giờ kết quả phải ở tương lai (Japan TZ). Omit nếu không đổi; không dùng cùng `setting_send_message=0` |
| setting_send_message | Integer | No | [info] `0` = gửi ngay — MCP server tự set `send_day`/`send_time` = giờ Japan hiện
tại (lịch cũ bị thay), nên KHÔNG truyền kèm `send_day`/`send_time` (truyền kèm → lỗi); `1` = đặt lịch — truyền
`send_day` + `send_time` (tương lai, Japan TZ). Bỏ trống mà có gửi `send_day`/`send_time` → tự set `1`. Chỉ ghi lại
send mode của draft — tool KHÔNG gửi gì |
| profile_id | Long | No | [info] ID profile người gửi mới (配信プロフィール) — numeric id của profile đã cấu hình
trên bot. Omit nếu không đổi; giá trị blank bị backend bỏ qua (skip-blank) |
| schedules | List&lt;BroadcastSchedule&gt; | No | [schedules] Danh sách typed các slot lịch cần **THÊM** — mỗi item
`{ sendDay: "YYYY-MM-DD", sendTime: "HH:mm" }`. 1–10 items/call; thời gian tương lai Japan TZ; không duplicate trong
list hoặc với schedule đã có. Mỗi item thành 1 child broadcast độc lập. Lịch đã có KHÔNG bị ghi đè ở đây — đổi lịch
hiện tại dùng section info (`send_day`/`send_time`) |
| template | BroadcastMessage | No | [template] 1 typed template payload. Set `type`
(`text`\|`image`\|`video`\|`voice`\|`location`\|`form`) và fill đúng field tương ứng. Không có `broadcast_template_id`
→ ADD template mới; có → EDIT template đó (type không đổi; nested array REPLACE toàn bộ — gửi lại cả item không sửa).
`img_path` của ảnh = `download_url` từ `get_file_params`. Tối đa 1 template quick reply mỗi broadcast |
| broadcast_template_id | Long | No | [template] `template_child_id` có sẵn cần EDIT (từ
`list_broadcast_templates.templates[].template_id`). Có = edit template đó; không có = payload `template` được ADD
mới. Chỉ có nghĩa khi đi kèm `template` |
| template_id | Long | No | [template_id] ID template có sẵn cần copy vào broadcast (từ `list_templates` — group template
hoặc template đơn; template con trong group bị từ chối). Bản copy thành message mới ở cuối; sửa template gốc sau này không
ảnh hưởng broadcast. Mỗi call thêm 1 bản copy. Không gửi cùng `template` / `broadcast_template_id` |
| action_id | Long | No | [action] ID dương của chain tạo bởi `create_action` → REPLACE toàn bộ post-send action set
bằng COPY các step của chain (chain nguồn độc lập — sửa `update_action` sau này không lan sang broadcast). `0` → xoá
hết post-send actions. Step types cho phép: `tag`, `scenario`, `richmenu`, `friend_info`, `block`, `bookmark`,
`handling_status` (step `text` bị reject) |

**BroadcastSchedule schema:**

| Name     | Type   | Required | Description                               |
|----------|--------|----------|-------------------------------------------|
| sendDay  | String | Yes      | Ngày gửi — format `YYYY-MM-DD` (Japan TZ) |
| sendTime | String | Yes      | Giờ gửi — format `HH:mm` (Japan TZ)       |

**BroadcastMessage schema:**

| Name            | Type                 | Required | Description                                                                                                             |
|-----------------|----------------------|----------|-------------------------------------------------------------------------------------------------------------------------|
| type            | TemplateContentType  | Yes      | Loại nội dung: `text` \| `image` \| `video` \| `voice` \| `location` \| `form`                                          |
| templateChildId | Long                 | No       | Selector EDIT — cùng ý nghĩa với `broadcast_template_id` (top-level). Set cả hai với giá trị khác nhau → reject. Omit khi ADD |
| text            | TextTemplateData     | No       | [type=text] Payload text                                                                                                |
| image           | ImageTemplateData    | No       | [type=image] Payload ảnh (Case 1 full image)                                                                            |
| video           | VideoTemplateData    | No       | [type=video] Payload video                                                                                              |
| voice           | VoiceTemplateData    | No       | [type=voice] Payload voice/audio                                                                                        |
| location        | LocationTemplateData | No       | [type=location] Payload vị trí                                                                                          |
| form            | FormTemplateData     | No       | [type=form] Payload form/carousel (standard \| color \| image \| quick_reply \| quick_reply_image)                      |

> Chỉ fill đúng 1 field payload tương ứng `type` — các field còn lại để null/omit. Cấu trúc chi tiết per-type nằm
> trong input schema của tool (client nhận qua `tools/list`); cấu trúc dùng chung với
> `create_broadcast.templates[]` — xem [create_broadcast](#1-create_broadcast).
>
> **ActionRef:** các action surface trong template (`form.panels[].buttons[].actions`, `form.exceedActions`,
> `image` tap zones `actions`, `text.urlSettings[].actions`/`outTimeActions`) chỉ nhận reference `{actionId}` — chain
> tạo từ `create_action`; server tự resolve + embed các step trước khi lưu.

**Validation trước khi chạy section (fail-fast, chưa mutate gì):**

- Không có section nào → reject `"Nothing to update"` (liệt kê 5 section + nhắc filter dùng `update_filter`)
- `broadcast_template_id` mà không có `template` → reject
- `template_id` cùng `template` → reject; `template_id` ≤ 0 → reject
- `name` > 20 chars → reject
- `action_id` âm → reject (`0` hợp lệ = clear)
- `schedules` sai shape/quá khứ/duplicate → reject
- `broadcast_template_id` ≠ `template.templateChildId` (cả hai cùng set) → reject conflict
- `setting_send_message` khác 0 / 1 → reject
- Sau đó: `validateBotAccess` + `assertEditable`; `template_id` phải là template trong `list_templates` (không phải con
  trong group / bản copy riêng); quy tắc **tối đa 1 quick reply** (section template khi payload là quick reply, và
  section template_id) — kiểm tra trước khi section nào chạy, nên call bị từ chối không lưu gì

**Semantics thứ tự + partial failure:**

- Section chạy theo thứ tự cố định: `info → schedules → template → template_id → action` (chỉ những section được gửi).
- Section fail đầu tiên → DỪNG. Nếu chưa section nào thành công → throw lỗi thô. Nếu đã có section thành công →
  response trả kết quả các section đã chạy + `failed_section` + `error` + `sections_not_run`.
- **Các section đã chạy KHÔNG rollback** — phần đã apply vẫn giữ trong DB. AI phải đọc `failed_section` để sửa và gọi
  lại CHỈ phần fail (không gửi lại các section đã thành công).

**🚨 REPLACE-ALL trong section template (khi EDIT):** backend ghi đè toàn bộ nested arrays, KHÔNG merge:

| Path                                      | Type áp dụng |
|-------------------------------------------|--------------|
| `form.panels[]` (list_panel)              | `form`       |
| `panels[].buttons[]` + `detail_action`    | `form`       |
| image-map items (tap zones)               | `image`      |
| `text.urlSettings[]`                      | `text`       |

**Rule**: `list_broadcast_templates` → đọc `data` của template hiện tại → build lại payload typed **FULL state**
(mọi panel/button/tap-zone/url không sửa cũng phải gửi lại) → mutate CHỈ phần user yêu cầu. Gửi thiếu = mất dữ liệu
im lặng (backend ghi đè 100%).

**Workflow chuẩn (get detail → build full state → update):**

1. `list_broadcasts` → resolve `broadcast_id` + verify status editable
2. (Section template EDIT) `list_broadcast_templates(broadcast_id)` → chọn item, lấy `template_id` làm
   `broadcast_template_id`, đọc `data` hiện tại
3. (Nếu có ảnh mới) `get_file_params` upload → lấy `download_url` → đặt vào `img_path`
4. (Section action) `create_action` trước → lấy `action_id` trả về
   (Section template_id) `list_templates` → lấy id template có sẵn cần gắn
5. Build payload: với template EDIT, dựng lại typed payload FULL state từ `data` clone, mutate chỉ field cần đổi
6. Gọi `update_broadcast` với các section cần thiết
7. Đọc response: mỗi section đã chạy có 1 key kết quả; nếu có `failed_section` → sửa phần fail, gọi lại chỉ phần đó

**Sample Input (đổi tên + thêm 2 lịch gửi):**

```json
{
  "bot_id": "y2kWN2",
  "broadcast_id": 5001,
  "name": "Sale T2 (final)",
  "schedules": [
    { "sendDay": "2026-10-01", "sendTime": "10:00" },
    { "sendDay": "2026-10-08", "sendTime": "10:00" }
  ]
}
```

**Sample Input (EDIT template text hiện có — full state):**

```json
{
  "bot_id": "y2kWN2",
  "broadcast_id": 5001,
  "broadcast_template_id": 201,
  "template": {
    "type": "text",
    "text": {
      "content": "Hello! Final 30% discount today only."
    }
  }
}
```

**Sample Input (gắn template có sẵn — copy template 3021 vào broadcast):**

```json
{
  "bot_id": "y2kWN2",
  "broadcast_id": 5001,
  "template_id": 3021
}
```

**Sample Input (chuyển broadcast gửi ngay sang đặt lịch — `setting_send_message` tự thành 1):**

```json
{
  "bot_id": "y2kWN2",
  "broadcast_id": 5001,
  "send_day": "2026-10-01",
  "send_time": "10:00"
}
```

**Sample Input (thay toàn bộ post-send actions bằng chain 777):**

```json
{
  "bot_id": "y2kWN2",
  "broadcast_id": 5001,
  "action_id": 777
}
```

**Output:**
| Name | Type | Description |
|---|---|---|
| info | Json Object | (Chỉ khi section info chạy) Response thô từ LME endpoint update-broadcast-info |
| schedules | Json Object | (Chỉ khi section schedules chạy) `{created: [...], failed: [...]}` — xem Sub Object bên dưới |
| template | Json Object | (Chỉ khi section template chạy) Response thô từ LME endpoint edit-broadcast-template |
| template_copy | Json Object | (Chỉ khi section template_id chạy) Response từ LME clone-template-to-broadcast — `data.template_id` = id bản copy mới trong broadcast |
| action | Json Object | (Chỉ khi section action chạy) Response thô từ LME endpoint edit-broadcast-action |
| failed_section | String | (Chỉ khi partial failure) Section bị fail: `info` / `schedules` / `template` / `template_copy` / `action` |
| error | String | (Chỉ khi partial failure) Error message của section fail |
| sections_not_run | Json Array | (Chỉ khi partial failure) Các section phía sau chưa chạy |

**Sub Object schedules.created[] item:**
| Name | Type | Description |
|---|---|---|
| send_day | String | Ngày gửi của child broadcast mới |
| send_time | String | Giờ gửi của child broadcast mới |
| id | Long | ID của child broadcast mới |
| parent_id | Long | ID broadcast cha |

**Sub Object schedules.failed[] item:**
| Name | Type | Description |
|---|---|---|
| send_day | String | Ngày gửi của item bị reject |
| send_time | String | Giờ gửi của item bị reject |
| error | String | Lý do LME reject (vd duplicate với schedule đã có) |

**Sample Output (thành công — info + schedules):**

```json
{
  "info": { "...": "LME response" },
  "schedules": {
    "created": [
      { "send_day": "2026-10-01", "send_time": "10:00", "id": 5101, "parent_id": 5001 },
      { "send_day": "2026-10-08", "send_time": "10:00", "id": 5102, "parent_id": 5001 }
    ],
    "failed": []
  }
}
```

**Sample Output (partial failure — info OK, template fail, action chưa chạy):**

```json
{
  "info": { "...": "LME response" },
  "failed_section": "template",
  "error": "VALIDATION_ERROR: message_button.list_panel[0].title exceeds max length",
  "sections_not_run": ["action"]
}
```

---

## Cross-references

- `get_file_params` (upload ảnh cho template): [11-chat.md](11-chat.md)
- Sửa filter broadcast: `update_filter(target=broadcast)` — REPLACE-ALL: [30-filter.md](30-filter.md)
- `list_templates` (template độc lập): [19-template.md](19-template.md)
- Handling status (filter/action): [20-handling-status.md](20-handling-status.md)
- Filter `affiliate`: [21-affiliate.md](21-affiliate.md) · filter `conversion`: [22-conversion.md](22-conversion.md) · filter `status_chat`: [24-status-chat-filter.md](24-status-chat-filter.md)
- Post-send action: tạo chain bằng `create_action` → gắn qua `action_id` ([29-action.md](29-action.md))
