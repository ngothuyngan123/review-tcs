# Filter Tools

Nhóm tool quản lý **friend-filter** (điều kiện lọc friend) dạng typed. Ngữ nghĩa grouping chung cho cả 2 tool:

- `filter_and` = nhóm AND — friend phải match **TẤT CẢ** điều kiện trong nhóm
- `filter_or` = nhóm OR — friend chỉ cần match **MỘT** điều kiện trong nhóm
- Kết quả cuối = **(nhóm AND) OR (nhóm OR)**
- Điều kiện đơn lẻ đặt vào `filter_and` (nhóm OR chỉ 1 phần tử là vô nghĩa)
- `create_filter` và `update_filter(target='scenario')`: ít nhất một trong `filter_and` / `filter_or` phải khác rỗng.
  `update_filter(target='broadcast' | 'autoreply')`: gửi `filter_and: []` + `filter_or: []` = xoá hết điều kiện

Schema chi tiết từng loại điều kiện nằm ngay trong **input schema typed** của 2 tool (record `FilterItem` + sub-object
per-type) — client nhận qua `tools/list`, không cần gọi guide. (2 guide tool `guide_filter_structure` /
`guide_filter_grouping` đã bị tắt từ 2026-09-18 sau khi filter được typed-hoá.)

## 1. create_filter

**Description:** Tool tạo saved filter độc lập (filter manager) từ các điều kiện typed và trả về `filter_manager_id`
(gắn vào step qua `create_scenario_step`) cùng `filter_ids`. Đây là cách **duy nhất** tạo filter cho scenario step; sửa
filter đã có dùng `update_filter(target=scenario)`. 11 loại điều kiện: tag, friend_name, day_add_friend, scenario, qr_code, friend_info,
bot_new_friend, status_search, conversion, affiliate, status_chat. Mọi entity ID tham chiếu trong điều kiện (tag,
scenario, conversion, ...) được kiểm tra quyền sở hữu bot trước khi lưu, đồng thời server enrich field hiển thị từ DB.

**Tool:** `create_filter`

**Input:**
| Name | Type | Required | Description |
|------------|---------------------|----------|--------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| filter_name | String | Yes | Tên filter, 1–10 ký tự. BẮT BUỘC (bỏ trống/quá 10 ký tự → lỗi validation). Hiện trong danh sách filter của scenario trên web. Dùng tên user đưa; nếu user không đưa → `絞込み条件` + (số filter branch scenario đang có + 1), vd `絞込み条件2` — số branch = số giá trị `steps[].filter_manager_id` khác 0 (không trùng) trong `get_scenario_detail` |
| filter_and | Array of FilterItem | Cond | Nhóm AND — TẤT CẢ phải match. Ít nhất một trong filter_and/filter_or khác rỗng |
| filter_or | Array of FilterItem | Cond | Nhóm OR — match MỘT là đủ. Cùng format với filter_and. Chỉ dùng khi có 2+ điều kiện nối bằng "hoặc" |

**Sub Object FilterItem** (mỗi phần tử của `filter_and` / `filter_or` — đặt `type` + đúng MỘT field data trùng tên type):
| Name | Type | Required | Description |
|--------------|--------|----------|------------------------------------------------------------------------------------------------------------------|
| id | Long | No | ID filter item hiện có (từ get_scenario_detail steps[].filters[].id) — truyền khi update nhánh có sẵn qua update_filter để sửa item in-place. Bỏ qua cho item mới |
| type | String | Yes | `tag` \| `friend_name` \| `day_add_friend` \| `scenario` \| `qr_code` \| `friend_info` \| `bot_new_friend` \| `status_search` \| `conversion` \| `affiliate` \| `status_chat` |
| tag | Object | Cond | [type=tag] Sub Object Tag Filter |
| friendName | Object | Cond | [type=friend_name] Sub Object Friend Name Filter |
| dayAddFriend | Object | Cond | [type=day_add_friend] Sub Object Day Add Friend Filter |
| scenario | Object | Cond | [type=scenario] Sub Object Scenario Filter |
| qrCode | Object | Cond | [type=qr_code] Sub Object QR Code Filter |
| friendInfo | Object | Cond | [type=friend_info] Sub Object Friend Info Filter |
| botNewFriend | Object | Cond | [type=bot_new_friend] Sub Object Bot New Friend Filter |
| statusSearch | Object | Cond | [type=status_search] Sub Object Status Search Filter |
| conversion | Object | Cond | [type=conversion] Sub Object Conversion Filter |
| affiliate | Object | Cond | [type=affiliate] Sub Object Affiliate Filter |
| statusChat | Object | Cond | [type=status_chat] Sub Object Status Chat Filter |

**Sub Object Tag Filter (`tag`):**
| Name | Type | Required | Description |
|-----------------|-----------------|----------|--------------------------------------------------------------------------------|
| tagsSearch | Array of Long | Yes | Các tag ID cần lọc (từ list_tags) |
| tagCondition | Int | No | 0=has_any \| 1=has_all \| 2=exclude_any \| 3=exclude_all. Default 0 |
| tagNames | Array of String | No | Tên tag tương ứng (copy 'name' từ list_tags — cho UI). Để [] nếu không biết |
| groupOpenTag | String | No | Folder ID của tag đầu tiên dạng string (từ `list_folders(type=tag)`). "0" nếu không biết |
| previewOriginal | String | No | Chuỗi hiển thị UI — tên tag nối bằng '・' |

**Sub Object Friend Name Filter (`friendName`):**
| Name | Type | Required | Description |
|------------|-----------------|----------|-------------------------------------------------------------------------------------------|
| keyword | String | Yes | Các mảnh tên cần tìm, cách nhau bằng space |
| searchFrom | Array of String | No | Field tìm: ["line_name"] \| ["system_name"] \| ["line_name","system_name"]. Default ["line_name"] |

**Sub Object Day Add Friend Filter (`dayAddFriend`):**
| Name | Type | Required | Description |
|------------------|--------|----------|-----------------------------------------------------|
| dayFilterType | String | Yes | `date_range` \| `duration` |
| addFromDate | String | Cond | [date_range] Ngày bắt đầu YYYY-MM-DD |
| addToDate | String | Cond | [date_range] Ngày kết thúc YYYY-MM-DD |
| durationDayStart | Int | Cond | [duration] Số ngày tối thiểu từ khi add friend (inclusive) |
| durationDayEnd | Int | Cond | [duration] Số ngày tối đa từ khi add friend (inclusive) |

**Sub Object Scenario Filter (`scenario`):**
| Name | Type | Required | Description |
|-------------------|--------|----------|--------------------------------------------------------------------------------------------|
| scenarioSearch | Long | Yes | Scenario ID (từ list_scenarios) |
| scenarioName | String | No | Tên scenario (copy từ list_scenarios — cho UI). Để trống nếu không biết |
| scenarioCondition | String | Yes | `subscribed` \| `not_subscribed` \| `sent_within_days` \| `completed` \| `not_completed` |
| numberOfDays | Int | Cond | Số ngày. Bắt buộc khi scenarioCondition=sent_within_days |

**Sub Object QR Code Filter (`qrCode`):**
| Name | Type | Required | Description |
|-------------|-----------------|----------|------------------------------------------------------------------------|
| qrsSearch | Array of Long | Yes | Các QR code ID (từ list_traffic_sources) |
| qrCondition | String | Yes | `scanned_any` \| `never_scanned` |
| qrNames | Array of String | No | Tên QR code (copy từ list_traffic_sources — cho UI). [] nếu không biết |

**Sub Object Friend Info Filter (`friendInfo`):**
| Name | Type | Required | Description |
|-------------------|-----------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| isDefault | Int | No | 1=field built-in (id<0) \| 0=field custom (id>0). Suy từ dấu của 'id' trong list_friend_info_fields |
| infoSearch | String | Yes | Field ID dạng string: 'd_1'..'d_6' cho cross field built-in, '-7'..'-10' cho address built-in, ID số dạng string cho field custom |
| title | String | No | Tiêu đề field (từ list_friend_info_fields 'title') — cho UI |
| typeData | Int | Yes | Loại dữ liệu field: 1=select \| 2=text \| 3=date \| 6=point |
| opCompare | String | Yes | Toán tử so sánh dạng chuỗi. text: '1'=contains,'2'=not_contains,'3'=starts_with,'4'=ends_with,'5'=has_value,'6'=no_value. point: '1'=eq,'2'=ne,'3'=gt,'4'=lt,'5'=gte,'6'=lte,'7'=has_value. date: '1'=exact,'2'=range,'3'=has_value. select: '1'=any_of,'2'=none_of,'3'=has_value,'4'=no_value |
| friendInfoId | Long | Cond | [select] ID số của field custom (từ list_friend_info_fields 'id'). Bắt buộc khi typeData=1 |
| friendInfoKeyword | String | Cond | [text] Keyword tìm. Chuỗi rỗng cho op has_value/no_value |
| point | String | Cond | [point] Giá trị point dạng chuỗi. Rỗng cho op has_value |
| selectedOp | Array of String | Cond | [select] Các giá trị option đã chọn (byte-exact từ setting_actions[].value trong list_friend_info_fields) |
| valueOption | Object | Cond | [select] Copy NGUYÊN VẸN tất cả item từ list_friend_info_fields setting_value.setting_actions |
| limitDate | Int | Cond | [date] 0=ngày chính xác \| 1=khoảng ngày |
| year / month / day | String | Cond | [date] Năm/tháng/ngày bắt đầu dạng chuỗi (vd '2024', '1'..'12', '1'..'31') |
| yearTo / monthTo / dayTo | String | Cond | [date][range] Năm/tháng/ngày kết thúc dạng chuỗi |

**Sub Object Bot New Friend Filter (`botNewFriend`):**
| Name | Type | Required | Description |
|-------------------|--------|----------|---------------------------|
| selectValueFriend | String | Yes | `new` \| `existing` |

**Sub Object Status Search Filter (`statusSearch`):**
| Name | Type | Required | Description |
|-----------------------|--------|----------|-------------------------------|
| statusSearchCondition | String | Yes | `confirm` \| `unconfirm` |

**Sub Object Conversion Filter (`conversion`):**
| Name | Type | Required | Description |
|---------------------|--------|----------|-------------------------------------------------------------------------------------|
| conversionSearch | String | Yes | Conversion ID dạng chuỗi phẩy, vd "1180" hoặc "1189,1190" (từ list_conversions) |
| conversionCondition | Mixed | No | INT 0=include \| STRING "1"=exclude. Default 0 |
| openGroup | Int | No | Category ID của conversion (từ list_conversions). 0 nếu chưa phân loại |
| previewOriginal | String | No | Chuỗi hiển thị UI — tên conversion nối lại |

**Sub Object Affiliate Filter (`affiliate`):**
| Name | Type | Required | Description |
|---------------------|---------------|----------|--------------------------------------------------|
| affiliateSearch | Array of Long | Yes | Các affiliate ID (từ list_affiliates) |
| affiliateFilterType | Mixed | No | INT 0=include \| STRING "1"=exclude. Default 0 |
| previewOriginal | String | No | Chuỗi hiển thị UI — tên affiliate nối lại |

**Sub Object Status Chat Filter (`statusChat`):**
| Name | Type | Required | Description |
|----------------------|---------------|----------|--------------------------------------------------|
| statusChatSearch | Array of Long | Yes | Các handling status ID (từ list_handling_statuses) |
| statusChatFilterType | Mixed | No | INT 0=include \| STRING "1"=exclude. Default 0 |
| previewOriginal | String | No | Chuỗi hiển thị UI — tên status nối lại |

**Sample Input:**

```json
{
  "bot_id": "mj3Kzx",
  "filter_name": "絞込み条件1",
  "filter_and": [
    {
      "type": "tag",
      "tag": {
        "tagsSearch": [12, 15],
        "tagCondition": 0
      }
    },
    {
      "type": "day_add_friend",
      "dayAddFriend": {
        "dayFilterType": "duration",
        "durationDayStart": 0,
        "durationDayEnd": 30
      }
    }
  ],
  "filter_or": []
}
```

**Output:** envelope passthrough + 2 handle được surface lên top-level để client đọc một chỗ (verify live 2026-09-22):

| Name | Type | Description |
|-------------------|---------------|--------------------------------------------------------------------------------------------------|
| filter_manager_id | Long | ID filter manager tái sử dụng — gắn vào step qua `create_scenario_step` (field `filter_manager_id`) |
| filter_ids | Array of Long | Các row id filters_v2 (backend có thể trả key `array_filter_id` — MCP chuẩn hoá surface thành `filter_ids`) |

**Sample Output:**

```json
{
  "result": "ok",
  "data": { "filter_manager_id": 555, "filter_ids": [901, 902] },
  "error": null,
  "filter_manager_id": 555,
  "filter_ids": [901, 902]
}
```

---

## 2. update_filter

**Description:** Tool thay thế friend-filter của một target hiện có — **REPLACE-ALL (thay thế toàn bộ)**: tập điều
kiện gửi lên trở thành TOÀN BỘ filter của target; **điều kiện đã lưu trước đó mà không có trong lần gọi này sẽ bị
xóa**, và nhóm không gửi (`filter_and` hoặc `filter_or`) thành rỗng.

- `target='scenario'`: sửa một filter **đã có** của scenario (`target_id` = scenario_id; `filter_manager_id` **bắt
  buộc** — lấy từ get_scenario_detail steps[].filter_manager_id, phải thuộc scenario này hoặc là filter của
  `create_filter` chưa gắn step nào; `filter_name` tuỳ chọn, bỏ trống = giữ tên hiện tại, ≤10 ký tự). Tool **không tạo
  mới**: muốn thêm nhánh filter, tạo bằng `create_filter` rồi gắn vào step qua `create_scenario_step`
  (xem [06-scenario.md](06-scenario.md)). Cần **ít nhất 1 điều kiện** — muốn bỏ filter khỏi step dùng
  `update_scenario_step(filter_manager_id=0)` kèm section timing. Mọi entity ID trong điều kiện được kiểm tra quyền sở
  hữu bot như `create_filter`.
- `target='broadcast'`: thay toàn bộ filter người nhận của một broadcast **còn sửa được** (`target_id` = broadcast_id;
  draft / unregistered, hoặc `wait_to_send` còn hơn 5 phút trước giờ gửi). `filter_name` / `filter_manager_id` bị bỏ qua.
- `target='autoreply'`: thay toàn bộ filter của một auto reply rule (`target_id` = autoreply_id; rule thuộc bot, chưa
  xoá) — gọi `/save-filter` với `parent_type='auto_reply'`. Từ 2026-09-26 đây là **đường duy nhất** sửa filter của auto
  reply (`update_autoreply` không còn nhận `filter_and` / `filter_or`; tạo mới vẫn inline trong `create_autoreply`).
  `filter_name` / `filter_manager_id` bị bỏ qua. Chấp nhận cả alias `auto_reply`.

**Xoá hết điều kiện (broadcast / autoreply):** gửi `filter_and: []` và `filter_or: []` (mọi nhóm gửi lên đều rỗng) →
target áp dụng cho mọi friend. Bỏ trống **cả hai** param → lỗi (tránh vô tình xoá sạch). Scenario không xoá hết qua tool
này.

**Quyền:** admin của bot dùng được mọi target; staff cần quyền tính năng của target — scenario **15**, broadcast **22**,
autoreply **25** (kiểm bằng key `update_scenario` / `edit_broadcast_info` / `update_autoreply` trong `TOOL_ACCESS_MAP`;
bản thân `update_filter` không có trong map).

> ⚠️ **Cảnh báo REPLACE-ALL:** muốn giữ điều kiện cũ phải gửi lại đầy đủ trong `filter_and`/`filter_or` — với
> scenario, item giữ lại nên kèm `id` (từ get_scenario_detail steps[].filters[].id) để update in-place.

**Tool:** `update_filter`

**Input:**
| Name | Type | Required | Description |
|-------------------|---------------------|----------|-----------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| target | String | Yes | Object cần thay filter: `scenario` \| `broadcast` \| `autoreply` |
| target_id | Long | Yes | ID target — scenario_id / broadcast_id / autoreply_id theo `target` |
| filter_name | String | No | [target=scenario] Tên hiển thị mới của filter, ≤10 ký tự. Bỏ trống = giữ tên hiện tại; broadcast / autoreply bỏ qua |
| filter_manager_id | Long | Cond | [target=scenario] **Bắt buộc** — ID filter cần ghi đè in-place (từ get_scenario_detail steps[].filter_manager_id); phải thuộc scenario này hoặc là filter của create_filter chưa gắn step. Broadcast / autoreply bỏ qua |
| filter_and | Array of FilterItem | Cond | Nhóm AND (cùng format FilterItem như create_filter). Gửi ít nhất một trong filter_and / filter_or; nhóm không gửi thành rỗng. Scenario: ≥ 1 điều kiện; broadcast / autoreply: `[]` + `[]` = xoá hết |
| filter_or | Array of FilterItem | Cond | Nhóm OR — cùng quy tắc gửi như filter_and |

**Sample Input (target=scenario — sửa filter có sẵn, giữ tên hiện tại):**

```json
{
  "bot_id": "mj3Kzx",
  "target": "scenario",
  "target_id": 3001,
  "filter_manager_id": 555,
  "filter_and": [
    {
      "type": "tag",
      "tag": {
        "tagsSearch": [12],
        "tagCondition": 0
      }
    }
  ],
  "filter_or": []
}
```

**Sample Input (target=broadcast — thay toàn bộ filter người nhận):**

```json
{
  "bot_id": "mj3Kzx",
  "target": "broadcast",
  "target_id": 1,
  "filter_and": [
    {
      "type": "bot_new_friend",
      "botNewFriend": {
        "selectValueFriend": "new"
      }
    }
  ],
  "filter_or": []
}
```

**Sample Input (target=autoreply — thay filter của rule):**

```json
{
  "bot_id": "mj3Kzx",
  "target": "autoreply",
  "target_id": 101,
  "filter_and": [
    {
      "type": "tag",
      "tag": {
        "tagsSearch": [12],
        "tagCondition": 0
      }
    }
  ]
}
```

**Sample Input (target=autoreply — xoá hết điều kiện, rule áp dụng cho mọi friend):**

```json
{
  "bot_id": "mj3Kzx",
  "target": "autoreply",
  "target_id": 101,
  "filter_and": [],
  "filter_or": []
}
```

**Output:** envelope passthrough `{ result, data, error }`.

**Lỗi validation:**
- target=scenario: thiếu `filter_manager_id` → hướng dẫn dùng `create_filter` + `create_scenario_step`; filter không
  thuộc bot / thuộc scenario khác / không phải filter scenario → lỗi; không có điều kiện nào → lỗi (gợi ý
  `update_scenario_step(filter_manager_id=0)`).
- target=broadcast / autoreply: bỏ trống cả `filter_and` lẫn `filter_or` → lỗi; broadcast không còn sửa được / rule không
  tồn tại hoặc không thuộc bot → lỗi.
- Mọi target: entity ID trong điều kiện không thuộc bot → lỗi; staff thiếu quyền tính năng của target → 403.
