# Auto Reply Tools

## 1. list_autoreplies

**Description:** Tool liệt kê các Auto Reply rule của bot và tra cứu rule ID theo keyword. Trả về id, danh sách keyword,
loại trigger, trạng thái và số lần đã reply (reply_count) của từng rule. Truyền `keywords[]` để lọc theo khớp một phần
(không phân biệt hoa thường) — dùng trước `get_autoreply_detail` hoặc bất kỳ call nào cần rule id. Rule
`trigger_by=any_message` (không có keyword) KHÔNG match filter keywords. Khi truyền `keywords`, response kèm
`not_found_keywords` cho các pattern không match rule nào.

**Tool:** `list_autoreplies`

**Input:**
| Name | Type | Required | Description |
|-------------|-----------------|----------|------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| keywords | Array of String | No | Mảng pattern PARTIAL match (contains, case-insensitive, trim) trên keyword của rule. Multiple = OR. Ví dụ: `["登録", "join"]`. Rule `trigger_by=any_message` (không có keyword) KHÔNG match |
| folder_id | Long | No | Folder ID để lọc rule theo folder (0 = 未分類/chưa phân loại). Nếu user đưa TÊN folder → resolve tên → id qua `list_folders(type=autoreply)` trước. Bỏ qua = trả rule của mọi folder |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|--------------------|-----------------|------------------------|
| auto_replies | Json Array | Array Object AutoReply |
| pagination | Json Object | Thông tin phân trang — Sub Object Pagination |
| not_found_keywords | Array of String | (Chỉ trả khi truyền `keywords` và có pattern không match rule nào) Danh sách pattern không match |

**Sub Object AutoReply:**
| Name | Type | Description |
|--------------|------------|-----------------------------------------------------------------------------------------------|
| id | Int | ID của Auto Reply rule |
| category_id | Long | Folder ID chứa rule (0 = 未分類/chưa phân loại) |
| trigger_by | String | Điều kiện trigger: `any_message` = reply với mọi tin nhắn / `keyword` = chỉ reply khi có keyword khớp |
| keywords | Json Array | Danh sách keyword — Sub Object Keyword. Nếu trigger_by = any_message → trả 1 phần tử label `{"id": null, "keyword": "全てのメッセージに反応", "match_type": null}` |
| time_mode | String | Chế độ thời gian: `always` = hoạt động 24/7 / `scheduled` = chỉ trong khung giờ được cài |
| time_setting | Object | Khung giờ và ngày hoạt động — Sub Object TimeSetting (null nếu time_mode = always)           |
| is_stopped | Boolean | Trạng thái: false=đang active, true=đã dừng |
| reply_count | Int | Tổng số lần rule đã được trigger |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)                                                       |

**Sub Object Keyword:**
| Name | Type | Description |
|------------|--------|--------------------------------------------------------------------------|
| id | Long | ID của keyword (null với label any_message) |
| keyword | String | Từ khóa trigger |
| match_type | String | Kiểu khớp: `exact` = khớp toàn phần / `partial` = khớp một phần (contains). null với label any_message |

**Sub Object TimeSetting:**
| Name | Type | Description |
|-------------|--------|--------------------------------------------------------------------------------|
| start_time | String | Giờ bắt đầu (format: HH:mm:ss)                                                |
| end_time | String | Giờ kết thúc (format: HH:mm:ss)                                               |
| day_of_week | String | Ngày hoạt động, semicolon-separated (1=T2, 2=T3, 3=T4, 4=T5, 5=T6, 6=T7, 7=CN) |

**Sub Object Pagination:**
| Name | Type | Description |
|-------------|------|---------------------|
| currentPage | Int | Trang hiện tại |
| limit | Int | Số record mỗi trang |
| total | Int | Tổng số record |

**Sample Output:**

```json
{
  "auto_replies": [
    {
      "id": 101,
      "category_id": 5,
      "trigger_by": "keyword",
      "keywords": [
        { "id": 9001, "keyword": "đăng ký", "match_type": "partial" },
        { "id": 9002, "keyword": "tham gia", "match_type": "partial" }
      ],
      "time_mode": "always",
      "time_setting": null,
      "is_stopped": false,
      "reply_count": 3420,
      "created_at": "2025-08-01 10:00:00"
    },
    {
      "id": 102,
      "category_id": 0,
      "trigger_by": "keyword",
      "keywords": [
        { "id": 9003, "keyword": "giờ mở cửa", "match_type": "exact" },
        { "id": 9004, "keyword": "open", "match_type": "partial" }
      ],
      "time_mode": "scheduled",
      "time_setting": {
        "start_time": "08:00:00",
        "end_time": "17:00:00",
        "day_of_week": "1;2;3;4;5"
      },
      "is_stopped": false,
      "reply_count": 890,
      "created_at": "2025-09-15 14:30:00"
    },
    {
      "id": 103,
      "category_id": 0,
      "trigger_by": "any_message",
      "keywords": [
        { "id": null, "keyword": "全てのメッセージに反応", "match_type": null }
      ],
      "time_mode": "scheduled",
      "time_setting": {
        "start_time": "18:00:00",
        "end_time": "08:00:00",
        "day_of_week": null
      },
      "is_stopped": true,
      "reply_count": 210,
      "created_at": "2025-07-20 09:00:00"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 3
  }
}
```

---

## 2. get_autoreply_detail

**Description:** Tool trả về chi tiết đầy đủ của nhiều Auto Reply rule cùng lúc, bao gồm logic kết hợp keyword, điều
kiện filter friend và các action thực thi sau khi reply.

**Tool:** `get_autoreply_detail`

**Input:**
| Name | Type | Required | Description |
|---------------|------|----------|------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| autoreply_ids | String | Yes | Danh sách ID Auto Reply rule cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |

**Output:** Array các object (mỗi object tương ứng 1 rule):
| Name | Type | Description |
|------------------------|------------|-----------------------------------------------------------------------------------------------|
| id | Int | ID của Auto Reply rule |
| trigger_by | String | `any_message` / `keyword`                                                                     |
| keywords | Json Array | Danh sách keyword đầy đủ — Sub Object Keyword. Nếu trigger_by = any_message → trả 1 phần tử label `{"id": null, "keyword": "全てのメッセージに反応", "match_type": null}` |
| keyword_logic | String | Cách kết hợp keyword: `any` = chỉ cần 1 keyword khớp (OR) / `all` = tất cả keyword phải khớp (AND) |
| time_mode | String | `always` / `scheduled`                                                                        |
| time_setting | Object | Sub Object TimeSetting (null nếu time_mode = always)                                         |
| is_stopped | Boolean | false=active, true=stopped |
| response_number | Int | Số lần phản hồi mỗi friend: 0 = không giới hạn (何度でも) / 1 = chỉ 1 lần (1度のみ) |
| reply_count | Int | Tổng số lần đã trigger |
| is_apply_active_friend | Boolean | true=chỉ áp dụng cho friend đang active (有効友だち), false=chỉ áp dụng cho friend bị block (ブロック友だち) |
| is_no_reply_button | Boolean | false=xử lý mọi tin nhắn, true=không auto-reply với tin nhắn phát sinh từ tap button |
| filters | Json Array | Điều kiện lọc friend — Sub Object Filter |
| actions | Json Array | Hành động thực thi sau khi reply — Sub Object Action |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)                                                       |

**Sub Object Keyword:**
| Name | Type | Description |
|------------|--------|--------------------------------------------------------------------------|
| id | Long | ID của keyword (null với label any_message) |
| keyword | String | Từ khóa trigger |
| match_type | String | `exact` = khớp toàn phần / `partial` = khớp một phần (contains). null với label any_message |

**Sub Object TimeSetting:**
| Name | Type | Description |
|-------------|--------|--------------------------------------------------------------------------------|
| start_time | String | Giờ bắt đầu (format: HH:mm:ss)                                                |
| end_time | String | Giờ kết thúc (format: HH:mm:ss)                                               |
| day_of_week | String | Ngày hoạt động, semicolon-separated (1=T2, 2=T3, 3=T4, 4=T5, 5=T6, 6=T7, 7=CN) |

**Sub Object Filter:**
| Name | Type | Description |
|-----------------|--------|-----------------------------------------------|
| id | Long | ID của filter |
| type | String | Loại filter (tag / friend_info / name / ...)  |
| operator | String | Điều kiện kết hợp (AND / OR)                 |
| preview_content | String | Nội dung mô tả filter (text hiển thị cho AI) |

**Sub Object Action:**
| Name | Type | Description |
|-----------|--------|-----------------------------------------------------------|
| id | Long | ID của action detail row |
| action_id | Long | ID của action chain chứa action này |
| type | String | Loại action: tag / scenario / richmenu / text / bookmark / friend_info / block / handling_status / template / remind |
| content | String | Text mô tả action bằng tiếng Nhật (ví dụ: タグ「VIP」をつける, ステップ「Welcome」を開始) |
| data | Object | Data thô của action, key tuỳ loại (ids, action, content, name, ...). Chỉ có key này khi parse được data |

**Sample Output:**

```json
[
  {
    "id": 101,
    "trigger_by": "keyword",
    "keywords": [
      { "id": 9001, "keyword": "đăng ký", "match_type": "partial" },
      { "id": 9002, "keyword": "tham gia", "match_type": "partial" }
    ],
    "keyword_logic": "any",
    "time_mode": "always",
    "time_setting": null,
    "is_stopped": false,
    "response_number": 1,
    "reply_count": 3420,
    "is_apply_active_friend": true,
    "is_no_reply_button": false,
    "filters": [
      {
        "id": 201,
        "type": "tag",
        "operator": "AND",
        "preview_content": "VIP Member"
      }
    ],
    "actions": [
      {
        "id": 501,
        "action_id": 300,
        "type": "tag",
        "content": "タグ「Đã đăng ký」をつける",
        "data": { "ids": ["123"], "action": 1 }
      },
      {
        "id": 502,
        "action_id": 300,
        "type": "scenario",
        "content": "ステップ「Welcome Sequence」を開始",
        "data": { "id": 45, "action": 2, "scenario_name": "Welcome Sequence" }
      }
    ],
    "created_at": "2025-08-01 10:00:00"
  }
]
```

---

## 3. get_autoreply_reply_history

**Description:** Tool trả về lịch sử các lần Auto Reply đã được trigger, có phân trang và lọc theo thời gian — để AI
phân tích tần suất, xu hướng và hiệu quả của các rule.

**Tool:** `get_autoreply_reply_history`

**Input:**
| Name | Type | Required | Description |
|---------------|--------|----------|--------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| autoreply_id | Long | Yes | ID rule (số dương, từ `list_autoreplies`). Lịch sử trả theo từng rule — không hỗ trợ lấy tất cả rule một lần. (Schema đã đổi sang required từ 2026-09-21 — trước đó khai optional gây hiểu lầm) |
| from_date | String | Yes | Ngày bắt đầu (bắt buộc, format: yyyy-MM-dd)                           |
| to_date | String | Yes | Ngày kết thúc (bắt buộc, format: yyyy-MM-dd)                          |
| page | Int | No | Số trang (default: 1)                                        |
| limit | Int | No | Số record mỗi trang (default: 100, max: 100)                            |

**Output:**
| Name | Type | Description |
|-------------|------------|-------------------------|
| total | Long | Tổng số record |
| page | Int | Trang hiện tại |
| limit | Int | Số record mỗi trang |
| total_pages | Int | Tổng số trang |
| histories | Json Array | Array Object History |

**Sub Object History:**
| Name | Type | Description |
|--------------------|--------|-------------------------------------------------|
| id | Long | ID history record |
| auto_reply_id | Long | ID rule đã trigger |
| lmessage_friend_id | Long | ID nội bộ của LINE user trong hệ thống (`line_user.id`) |
| line_friend_id | String | LINE UID thực của friend (dạng "Uxxxx...", null nếu chưa có) |
| line_name | String | Tên hiển thị của friend (null nếu chưa có tên) |
| created_at | String | Thời điểm reply (format: yyyy-MM-dd HH:mm:ss)  |

**Sample Output:**

```json
{
  "total": 3420,
  "page": 1,
  "limit": 100,
  "total_pages": 35,
  "histories": [
    {
      "id": 90001,
      "auto_reply_id": 101,
      "lmessage_friend_id": 50001,
      "line_friend_id": "U1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d",
      "line_name": "Nguyen Van A",
      "created_at": "2026-02-28 14:32:10"
    },
    {
      "id": 90002,
      "auto_reply_id": 101,
      "lmessage_friend_id": 50045,
      "line_friend_id": "U0f1e2d3c4b5a6978869504132231a0bf",
      "line_name": "Tran Thi B",
      "created_at": "2026-02-28 11:15:44"
    },
    {
      "id": 90003,
      "auto_reply_id": 101,
      "lmessage_friend_id": 50102,
      "line_friend_id": null,
      "line_name": null,
      "created_at": "2026-02-27 09:05:22"
    }
  ]
}
```

---

## 4. create_autoreply

**Description:** Tool tạo Auto Reply rule mới và trả về id của rule. Không cần gọi form/init trước — mọi lựa chọn và
default nằm ngay trong các field của `data_reply`. Truyền `action_id` (từ `create_action` — xem
[29-action.md](29-action.md)) để chạy action chain khi rule trigger — mỗi task nên tạo action riêng, KHÔNG dùng lại 1
action_id cho nhiều task (dùng chung chain → sửa action của task này sẽ đổi luôn task kia). `filter_and`/`filter_or`
giới hạn tập friend rule áp dụng (cấu trúc FilterItem — xem [30-filter.md](30-filter.md); sửa sau bằng `update_filter(target='autoreply')`). Rule tạo xong ở trạng thái
active; bật/tắt sau đó dùng field `status` của `update_autoreply` (mục 5).

**Tool:** `create_autoreply`

**Input:**
| Name | Type | Required | Description |
|--------------|---------------------|----------|------------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| copy_id | Long | No | ID rule nguồn để seed rule mới (copy phía server). Phải là rule thuộc bot, chưa xóa |
| data_reply | Object | Yes | Metadata của rule — Sub Object AutoReplyData |
| keywords | Array of Keyword | Cond | Danh sách keyword trigger — Sub Object Keyword. Bắt buộc (non-empty) khi data_reply.keywordReactionType=1 |
| action_id | Long | No | ID action chain từ create_action ([29-action.md](29-action.md)), chạy khi rule trigger. Được verify tồn tại trước khi link. Đây là input duy nhất để gắn chain (`data_reply.actionId` đã bỏ từ 2026-09-27). Mỗi task tạo 1 action riêng — không tái sử dụng |
| filter_and | Array of FilterItem | No | Nhóm điều kiện AND giới hạn friend áp dụng — cấu trúc FilterItem xem [30-filter.md](30-filter.md) |
| filter_or | Array of FilterItem | No | Nhóm điều kiện OR — cùng cấu trúc filter_and |

**Sub Object AutoReplyData (`data_reply`)** — field camelCase; field bỏ qua dùng giá trị default:
| Name | Type | Required | Description |
|---------------------|-----------------|----------|--------------------------------------------------------------------------------------------------------------|
| folderId | Integer | No | Folder ID chứa rule (0 = 未分類/chưa phân loại). create: default 0; update: bỏ trống = giữ folder hiện tại. `>0` phải là folder autoreply (kind=1) của bot. Tên folder → id: resolve qua `list_folders(type=autoreply)` |
| keywordReactionType | Integer | No | 0 = phản hồi MỌI tin nhắn (default) / 1 = chỉ phản hồi khi keyword khớp. =1 → keywords bắt buộc non-empty |
| keywordJoinMode | Integer | No | Cách kết hợp NHIỀU keyword ở mức rule (chỉ có nghĩa khi keywordReactionType=1): 0 = AND — TẤT CẢ keyword phải khớp (default) / 1 = OR — 1 keyword khớp là đủ. Khác với keywords[].matchMode (exact/partial cho TỪNG keyword) |
| timeReactionType | Integer | No | 0 = chạy 24/7 (default) / 1 = chỉ chạy trong khung giờ. =1 → startTime/endTime/dayOfWeek bắt buộc |
| responseMode | Integer | No | Số lần phản hồi mỗi friend: 0 = mỗi lần (何度でも) / 1 = chỉ 1 lần (1度のみ). Default 1. Quy tắc: keywordReactionType=0 → dùng 0; keywordReactionType=1 → dùng 1 trừ khi user muốn không giới hạn |
| isApplyActiveFriend | Integer | No | 1 = áp dụng cho friend đang active/有効友だち (default) / 0 = friend bị block/ブロック |
| isNoReplyButton | Boolean | No | false = xử lý mọi tin nhắn (default) / true = bỏ qua tin nhắn dạng 【...】 (phát sinh từ tap reply button LINE). Chỉ set true khi user yêu cầu rõ ràng |
| startTime | String | Cond | Giờ bắt đầu khung, format HH:mm (24h). Bắt buộc khi timeReactionType=1; khi =0 mà bỏ qua → tự điền giờ JST hiện tại |
| endTime | String | Cond | Giờ kết thúc khung, format HH:mm (24h). Bắt buộc khi timeReactionType=1 và phải > startTime — KHÔNG hỗ trợ khung qua đêm (vd 22:00–02:00) |
| dayOfWeek | Array of String | Cond | Ngày hoạt động ["1".."7"] (1=T2 .. 7=CN). Bắt buộc non-empty khi timeReactionType=1 |

**Sub Object Keyword (`keywords[]`):**
| Name | Type | Required | Description |
|-----------|---------|----------|------------------------------------------------------------------------------------------------------------------|
| id | Long | No | ID keyword row có sẵn — chỉ dùng ở update_autoreply để giữ row cũ; bỏ qua khi tạo mới |
| keyword | String | Yes | Text keyword cần khớp. ⚠️ Dài quá 30 ký tự sẽ bị CẮT còn 30 ký tự đầu (không báo lỗi) — cảnh báo trả trong `_warnings` |
| matchMode | Integer | No | Kiểu khớp CỦA keyword này: 0 = exact/khớp toàn phần (default) / 1 = partial/khớp một phần (contains). Schema cũng nhận alias `logical` / `match_type` / `matchType`. Lưu ý: get_autoreply_detail trả `match_type` dạng string ("exact"/"partial") — phải convert về 0/1 khi gửi lại |

**Validation (MCP layer, trước khi gọi LME):**

- `action_id` phải > 0 và tồn tại (verify qua backend get-action) — id sai → lỗi rõ ràng thay vì link mù
- `copy_id` (nếu truyền) phải là rule thuộc bot, chưa xóa
- Entity ID tham chiếu trong filter (tag, scenario, conversion, ...) được kiểm tra quyền sở hữu bot
- `keywordReactionType=1` → `keywords` bắt buộc non-empty
- **Keyword unique trong toàn bộ rule active của bot** (exact, case-sensitive, so sánh SAU trim + cắt 30 ký tự) —
  keyword đã dùng ở rule khác, hoặc trùng lặp ngay trong `keywords`, → 400
  `Duplicate keyword(s): '<keyword>' is already registered on autoreply_id=<id>...` (trước đây lỗi này nổ 500 — AR-F3)
- `timeReactionType=1` → startTime/endTime đúng format HH:mm, endTime > startTime, dayOfWeek non-empty "1".."7"

**Sample Input:**

```json
{
  "bot_id": "mj3Kzx",
  "data_reply": {
    "folderId": 5,
    "keywordReactionType": 1,
    "keywordJoinMode": 1,
    "timeReactionType": 1,
    "responseMode": 1,
    "isApplyActiveFriend": 1,
    "startTime": "09:00",
    "endTime": "18:00",
    "dayOfWeek": ["1", "2", "3", "4", "5"]
  },
  "keywords": [
    { "keyword": "đăng ký", "matchMode": 1 },
    { "keyword": "tham gia", "matchMode": 1 }
  ],
  "action_id": 300,
  "filter_and": [
    {
      "type": "tag",
      "tag": { "tagsSearch": [12], "tagCondition": 0 }
    }
  ]
}
```

**Output:** envelope passthrough từ backend save-autoreply (+ key MCP thêm):
| Name | Type | Description |
|-----------|-----------------|--------------------------------------------------------------------------------------------------|
| result | String | `ok` khi thành công |
| data | Json Object | Kết quả lưu: `{ "status": true, "data": { "id": <auto_reply_id> }, "msg": "" }` — **`data.data.id` = ID rule mới** |
| error | String | null khi thành công |
| _warnings | Array of String | (Chỉ có khi keyword >30 ký tự bị cắt) danh sách cảnh báo cắt keyword — message hiện sinh bằng tiếng Việt |

⚠️ `filter_and`/`filter_or` được lưu bằng call thứ 2 SAU khi rule tạo xong — nếu response backend không trả id rule
mới thì filter bị bỏ qua im lặng (không lỗi). Nên verify lại bằng `get_autoreply_detail` khi filter quan trọng; nếu
chưa được lưu thì đặt lại bằng `update_filter(target='autoreply')`.

**Sample Output:**

```json
{
  "result": "ok",
  "data": { "status": true, "data": { "id": 205 }, "msg": "" },
  "error": null
}
```

---

## 5. update_autoreply

**Description:** Tool update Auto Reply rule kiểu **FULL-STATE (gửi lại toàn bộ)**, đồng thời GỘP luôn chức năng đổi
trạng thái (thay cho tool change_status_autoreply cũ): gửi `status` MỘT MÌNH (ngoài bot_id/autoreply_id) → chỉ bật/tắt
rule, KHÔNG đụng nội dung và không cần data_reply; gửi `status` kèm field nội dung → nội dung lưu trước, status áp
sau (kết quả toggle nằm trong key `status_change` của response).

**Filter của rule KHÔNG sửa ở đây** — dùng `update_filter(target='autoreply', target_id=<autoreply_id>)` (xem
[30-filter.md](30-filter.md)); sửa riêng filter không cần gửi lại `data_reply`. (Đổi 2026-09-26: trước đây tool này nhận
`filter_and` / `filter_or` nhưng mọi lần sửa filter đều phải kèm `data_reply` full-state.)

> ⚠️ **Cảnh báo FULL-STATE:** `data_reply` và `keywords` THAY THẾ nội dung đã lưu — field bỏ qua trong data_reply
> quay về default (không giữ giá trị cũ), keyword không gửi lại sẽ MẤT. Luôn đọc `get_autoreply_detail` (mục 2)
> trước, dựng lại đầy đủ rồi chỉ sửa phần cần đổi. **Ngoại lệ `data_reply.folderId`:** bỏ trống = giữ folder hiện tại
> (`get_autoreply_detail` không trả folder); `0` = về 未分類 (đổi 2026-09-25 — review H3, trước đây bỏ trống = về 未分類).

**Tool:** `update_autoreply`

**Input:**
| Name | Type | Required | Description |
|---------------|---------------------|----------|-----------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| autoreply_id | Long | Yes | ID rule cần update. Phải tồn tại và thuộc bot |
| status | Boolean | No | true = bật rule, false = dừng rule. Gửi MỘT MÌNH → chỉ đổi trạng thái (status-only shortcut). Kèm field nội dung → áp SAU khi lưu nội dung. Bỏ qua = giữ nguyên trạng thái |
| data_reply | Object | Cond | Sub Object AutoReplyData — giống create_autoreply (mục 4). Bắt buộc khi update nội dung (mọi trường hợp trừ status-only). FULL-STATE: dựng lại từ get_autoreply_detail (trừ `folderId`: bỏ trống = giữ folder) |
| keywords | Array of Keyword | Cond | Sub Object Keyword — giống create_autoreply (mục 4). THAY THẾ toàn bộ keyword đã lưu; giữ `id` row cũ để update in-place. Bắt buộc non-empty khi keywordReactionType=1. Keyword unique trong bot (exact, case-sensitive, sau trim + cắt 30 ký tự): resend keyword của chính rule kèm `id` thì OK, keyword đang dùng ở rule khác → 400 `Duplicate keyword(s): ...` |
| action_id | Long | No | Bỏ qua = GIỮ action chain hiện tại của rule; `0` = gỡ link (chain vẫn còn trong account); id dương (từ create_action) = link sang chain đó (verify tồn tại trước) |

**Mapping khi dựng lại `data_reply` từ output `get_autoreply_detail` (mục 2):**

- `trigger_by`: "keyword" → keywordReactionType=1, "any_message" → 0
- `keyword_logic`: "all" → keywordJoinMode=0, "any" → keywordJoinMode=1
- `time_mode`: "scheduled" → timeReactionType=1; `time_setting.start_time` "HH:mm:ss" → startTime "HH:mm"; `day_of_week` "1;2;3" → dayOfWeek ["1","2","3"]
- keyword `match_type`: "exact" → matchMode=0, "partial" → matchMode=1
- `is_apply_active_friend` true/false → isApplyActiveFriend 1/0; `response_number` → responseMode; `is_no_reply_button` → isNoReplyButton
- `is_stopped` NGƯỢC với status: status=true (bật) ⇔ is_stopped=false
- folder: detail KHÔNG trả — bỏ trống `folderId` để giữ (folder hiện tại xem ở `list_autoreplies[].category_id`)

**Sample Input (status-only — chỉ dừng rule, không đụng nội dung):**

```json
{
  "bot_id": "mj3Kzx",
  "autoreply_id": 101,
  "status": false
}
```

**Sample Input (update nội dung full-state + gỡ action chain):**

```json
{
  "bot_id": "mj3Kzx",
  "autoreply_id": 101,
  "data_reply": {
    "folderId": 5,
    "keywordReactionType": 1,
    "keywordJoinMode": 1,
    "timeReactionType": 0,
    "responseMode": 1,
    "isApplyActiveFriend": 1
  },
  "keywords": [
    { "id": 9001, "keyword": "đăng ký", "matchMode": 1 },
    { "keyword": "membership", "matchMode": 0 }
  ],
  "action_id": 0
}
```

**Output:** envelope passthrough từ backend save-autoreply (+ key MCP thêm). Với status-only →
response là envelope passthrough của endpoint đổi trạng thái (không có key lưu nội dung):
| Name | Type | Description |
|---------------|-----------------|-----------------------------------------------------------------------------------------------|
| result | String | `ok` khi thành công |
| data | Json Object | Kết quả lưu nội dung: `{ "status": true, "data": { "id": <auto_reply_id> }, "msg": "" }` |
| error | String | null khi thành công |
| status_change | Object | (Chỉ có khi gửi `status` KÈM field nội dung) envelope kết quả toggle trạng thái — passthrough backend |
| _warnings | Array of String | (Chỉ có khi keyword >30 ký tự bị cắt) danh sách cảnh báo cắt keyword — message hiện sinh bằng tiếng Việt |

**Sample Output:**

```json
{
  "result": "ok",
  "data": { "status": true, "data": { "id": 205 }, "msg": "" },
  "error": null,
  "status_change": { "result": "ok", "data": { "success": true }, "error": null }
}
```
