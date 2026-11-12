# Scenario Tools

> **Tool đã bị thay thế** (không còn expose qua MCP):
> - `create_scenario_folder` → dùng tool generic `create_folder` / `update_folder` với `type=scenario` — xem [28-folder.md](28-folder.md)
> - `save_scenario_step`, `save_scenario_step_template`, `add_existing_template_to_scenario_step` → gộp thành `create_scenario_step` / `update_scenario_step` (bên dưới)
> - `save_scenario_filter` → tạo filter mới: `create_filter`; sửa filter có sẵn: `update_filter` với `target='scenario'` (bắt buộc `filter_manager_id`) — xem [30-filter.md](30-filter.md)

## 1. list_scenarios

**Description:** Tool trả về danh sách Scenario của bot kèm thống kê số người đang follow, đã hoàn thành, và dừng giữa
chừng. Hỗ trợ optional filter `names` (EXACT, case-insensitive, trim whitespace) để resolve tên scenario → ID số —
cần trước khi gọi get_scenario_detail, update_scenario hoặc bất kỳ tool nào yêu cầu scenario_id. Khi truyền `names`,
response có thêm `not_found_names` cho các tên không match.

**Tool:** `list_scenarios`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|-------------------------------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Mảng tên scenario EXACT (case-insensitive, trim). Multiple = OR. Partial KHÔNG match. Khuyến nghị dùng khi user chỉ định tên cụ thể thay vì paginate |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-----------------|-----------------|-----------------------------------------------------------------------------------------------------|
| scenarios | Json Array | Array Object Scenario Summary |
| pagination | Json Object | Thông tin phân trang |
| not_found_names | Array of String | (Chỉ trả khi truyền `names` và có tên không match) Các tên không match scenario nào — confirm với user trước khi tiếp tục |

**Sub Object Scenario Summary:**
| Name | Type | Description |
|----------------|--------|--------------------------------------------------|
| id | Long | ID của Scenario |
| name | String | Tên Scenario |
| count_follow | Int | Số người đang follow scenario |
| count_stop | Int | Số người đã dừng/hoàn thành scenario |
| count_unfinish | Int | Số người chưa hoàn thành |
| folder_id | Long | ID folder chứa scenario (0 = 未分類) |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object Pagination:**
| Name | Type | Description |
|-------------|------|----------------------|
| currentPage | Int | Trang hiện tại |
| limit | Int | Số record mỗi trang |
| total | Int | Tổng số record |

**Sample Output (no `names` filter):**

```json
{
  "scenarios": [
    {
      "id": 3001,
      "name": "Welcome New Member",
      "count_follow": 2500,
      "count_stop": 10500,
      "count_unfinish": 2000,
      "folder_id": 15,
      "created_at": "2025-06-15 09:30:00"
    },
    {
      "id": 3002,
      "name": "Product Education Series",
      "count_follow": 1200,
      "count_stop": 5600,
      "count_unfinish": 1200,
      "folder_id": 0,
      "created_at": "2025-09-01 10:00:00"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2
  }
}
```

**Sample Output (with `names: ["Welcome New Member", "Typo Name"]`):**

```json
{
  "scenarios": [
    {
      "id": 3001,
      "name": "Welcome New Member",
      "count_follow": 2500,
      "count_stop": 10500,
      "count_unfinish": 2000,
      "folder_id": 15,
      "created_at": "2025-06-15 09:30:00"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 1
  },
  "not_found_names": ["Typo Name"]
}
```

---

## 2. get_scenario_detail

**Description:** Tool trả về chi tiết nhiều Scenario (truyền list ID) bao gồm danh sách từng step, nội dung template,
thời gian gửi, số người đã nhận, điều kiện lọc và action chain gắn với step.

**Tool:** `get_scenario_detail`

**Input:**
| Name | Type | Required | Description |
|--------------|--------|----------|-----------------------------------------------------------------------------------------------|
| scenario_ids | String | Yes | Danh sách ID Scenario cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |

**Output** (Array — mỗi phần tử là một Scenario Detail):
| Name | Type | Description |
|----------------|------------|------------------------------------------|
| id | Long | ID của Scenario |
| name | String | Tên Scenario |
| count_follow | Int | Số người đang follow scenario |
| count_stop | Int | Số người đã dừng/hoàn thành |
| count_unfinish | Int | Số người chưa hoàn thành |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)   |
| steps | Json Array | Array Object Step Message |

**Sub Object Step Message:**
| Name | Type | Description |
|-------------------|------------|--------------------------------------------------------------------------------------------------------------------------------|
| id | Long | ID của step |
| name | String | Tên step |
| order_number | Int | Thứ tự step |
| delay_type | String | Loại delay: `"date_based"` (theo ngày + giờ), `"immediate"` (ngay khi vào scenario), `"time_offset"` (sau khoảng thời gian giờ/phút) |
| start_day | Int | Số ngày delay (dùng cho delay_type="date_based")                                                                                 |
| start_time | String | delay_type="date_based": giờ gửi `HH:mm:ss`; delay_type="time_offset": offset dạng `giờ:phút:00` (vd `30:30:00` = 30 giờ 30 phút) |
| templates | Json Array | Danh sách template gửi |
| send_count | Int | Số message đã gửi |
| filter_manager_id | Long | ID nhánh filter gắn với step (null = không filter). Truyền vào `update_filter(target='scenario')` để sửa điều kiện |
| filters | Json Array | Danh sách filter điều kiện của nhánh |
| action_id | Long | ID action chain gắn với step (null = không có). Dùng với `update_action` để sửa chain |
| actions | Json Array | Danh sách action item trong chain |

**Sub Object Template:**
| Name | Type | Description |
|---------|--------|----------------------------------------------------------------------------------------------------------------|
| id | Long | ID của template |
| name | String | Tên template |
| type | String | Loại template (text/image/video/voice/form/...) |
| content | Object | Nội dung gửi (String cho text; URL đầy đủ cho image/video/voice; Array panel cho form; group được expand thành list template con) |

**Sub Object Filter:**
| Name | Type | Description |
|-----------------|--------|-------------------------------------------------|
| id | Long | ID của filter row |
| type | String | Loại filter (tag/friend_info/friend_name/...)   |
| operator | String | Nhóm điều kiện: `"and"` / `"or"` |
| preview_content | String | Nội dung mô tả filter (text hiển thị cho user) |

**Sub Object Action:**
| Name | Type | Description |
|-----------|--------|----------------------------------------------------------------------------------------------------|
| id | Long | ID action detail (t_actions_detail.id — dùng làm `details[].id` khi gọi update_action) |
| action_id | Long | ID action chain chứa item này |
| type | String | Loại action: tag / scenario / richmenu / text / bookmark / friend_info / block / handling_status / template |
| content | String | Mô tả action dạng text (tiếng Nhật, vd タグ「VIP」をつける) |
| data | Object | Raw data của action detail (JSON từ backend, chỉ trả khi parse được) |

**Sample Output:**

```json
[
  {
    "id": 3001,
    "name": "Welcome New Member",
    "count_follow": 2500,
    "count_stop": 10500,
    "count_unfinish": 2000,
    "created_at": "2025-06-15 09:30:00",
    "steps": [
      {
        "id": 6001,
        "name": "Welcome Message",
        "order_number": 1,
        "delay_type": "immediate",
        "start_day": 0,
        "start_time": null,
        "templates": [
          {
            "id": 101,
            "name": "Welcome Text",
            "type": "text",
            "content": "ようこそ！"
          },
          {
            "id": 102,
            "name": "Welcome Image",
            "type": "image",
            "content": "https://cdn.example.com/welcome.jpg"
          }
        ],
        "send_count": 15000,
        "filter_manager_id": 501,
        "filters": [
          {
            "id": 201,
            "type": "tag",
            "operator": "and",
            "preview_content": "VIP Members"
          }
        ],
        "action_id": 88,
        "actions": [
          {
            "id": 301,
            "action_id": 88,
            "type": "tag",
            "content": "タグ「Welcome Sent」をつける",
            "data": {
              "ids": ["12"],
              "action": 1
            }
          }
        ]
      },
      {
        "id": 6002,
        "name": "Introduction Day 1",
        "order_number": 2,
        "delay_type": "date_based",
        "start_day": 1,
        "start_time": "10:00:00",
        "templates": [
          {
            "id": 103,
            "name": "Day 1 Introduction",
            "type": "text",
            "content": "こんにちは！"
          }
        ],
        "send_count": 14800,
        "filter_manager_id": null,
        "filters": [],
        "action_id": null,
        "actions": []
      }
    ]
  }
]
```

---

## 3. create_scenario

**Description:** Tool tạo Scenario mới (chuỗi gửi tin theo bước). Validation: `name` bắt buộc, không rỗng, ≤20 ký tự,
không trùng tên scenario đang hoạt động trong bot. Nếu `folder_id` đặt (>0) → phải là folder kind=11 thuộc bot. Nếu
`next_scenario_id` đặt → phải là scenario hợp lệ thuộc bot.

**Tool:** `create_scenario`

**Input:**
| Name | Type | Required | Description |
|------------------|--------|----------|---------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| name | String | Yes | Tên Scenario, không rỗng, ≤20 ký tự, unique trong bot |
| folder_id | Long | No | ID folder (category kind=11, tạo qua `create_folder` type=scenario — xem [28-folder.md](28-folder.md)). Bỏ qua = 未分類 (0) |
| next_scenario_id | Long | No | ID scenario tiếp theo được kích hoạt sau khi hoàn thành (after_scenario_id_1) |

**Output:** envelope passthrough từ backend:

```json
{
  "result": "ok",
  "data": { "status": true, "data": { "id": 3001 }, "msg": "", "folderId": 0 },
  "error": null
}
```

- `data.data.id` = **scenario_id mới** — dùng cho `create_scenario_step` / `update_scenario` / `get_scenario_detail`.

---

## 4. update_scenario

**Description:** Tool cập nhật tên, folder và next scenario. Chỉ gửi field cần đổi — field bỏ trống **giữ nguyên** giá
trị hiện tại (endpoint ghi đè cả 3 field nên MCP đọc lại scenario từ DB rồi gửi đủ). `folder_id=0` = chuyển scenario
về 未分類 (root); `folder_id>0` = chuyển vào folder kind=11 đó. `next_scenario_id=0` = gỡ liên kết next-scenario;
`>0` = liên kết scenario đó (phải thuộc bot). Không có field nào để đổi → lỗi `Nothing to update`.

> Đổi 2026-09-25 (review H1): trước đây `name` / `folder_id` bắt buộc, `folder_id` 0/null = giữ folder (không về được
> root), và bỏ trống `next_scenario_id` là **xóa** liên kết — trong khi không tool nào trả giá trị hiện tại để gửi lại.

**Tool:** `update_scenario`

**Input:**
| Name | Type | Required | Description |
|------------------|--------|----------|--------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string |
| scenario_id | Long | Yes | ID Scenario cần cập nhật (số dương, thuộc bot) |
| name | String | No | Tên mới (≤20 ký tự, unique trong bot, loại trừ chính nó). Bỏ trống = giữ tên hiện tại |
| folder_id | Long | No | Bỏ trống = giữ folder hiện tại; `0` = về 未分類 (root); `>0` = folder kind=11 của bot |
| next_scenario_id | Long | No | Bỏ trống = giữ liên kết hiện tại; `0` = gỡ liên kết; `>0` = scenario kế tiếp (thuộc bot) |

**Output:** envelope passthrough từ backend: `{ "result": "ok", "data": { "status": true }, "error": null }`
(lỗi nghiệp vụ — vd tạo loop next-scenario — trả `data.status=false` kèm `data.msg`).

---

## 5. create_scenario_step

**Description:** Tool tạo step (timing slot) mới trong Scenario và trả về step_id. `delay_type` quyết định lịch gửi:
0 = gửi vào start_day + start_time; 1 = ngay khi friend vào scenario; 2 = sau khoảng thời gian (elapsed_hours = giờ
0–72, elapsed_minutes = phút 0–59). Sau khi lưu, server tự sắp xếp lại toàn bộ step theo (start_day, start_time, id).
Step trùng (delay_type, start_day, start_time, filter_manager_id) với step hiện có bị từ chối
(「設定した時間に配信するメッセージが既に存在しています。」). Tối đa 100 step/scenario. `action_id` (từ
`create_action` — xem [29-action.md](29-action.md)) gắn action chain chạy khi step phát — step **tham chiếu** chain
gốc, nên chỉnh sửa sau này qua `update_action` cũng áp dụng cho step. Thêm nội dung message sau đó bằng
`update_scenario_step` (section template hoặc template_id).

**Tool:** `create_scenario_step`

**Input:**
| Name | Type | Required | Description |
|-------------------|--------|----------|-------------------------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string |
| scenario_id | Long | Yes | ID Scenario (thuộc bot) |
| delay_type | Int | Yes | 0 = theo lịch (start_day + start_time); 1 = ngay lập tức; 2 = sau khoảng thời gian GIỜ+PHÚT (elapsed_hours/elapsed_minutes). Vd "72 giờ" → delay_type=2, elapsed_hours=72, elapsed_minutes=0 |
| start_day | Int | Cond | Số ngày delay (≥0). Bắt buộc khi delay_type=0; truyền 0 cho delay_type=1/2. start_day=0 + start_time=00:00 bị từ chối |
| start_time | String | Cond | delay_type=0 → 'H:mm'/'HH:mm'/'HH:mm:ss' (24h). Không dùng cho delay_type=1/2 |
| elapsed_hours | Int | Cond | Thành phần GIỜ khi delay_type=2 (0–72). Bắt buộc khi delay_type=2. 0 giờ 0 phút bị từ chối; max 72 giờ 0 phút |
| elapsed_minutes | Int | Cond | Thành phần PHÚT khi delay_type=2 (0–59). Bắt buộc khi delay_type=2 |
| filter_manager_id | Long | No | `filter_manager_id` trả về từ `create_filter`, hoặc filter có sẵn của scenario (get_scenario_detail steps[].filter_manager_id) — xem [30-filter.md](30-filter.md). Giới hạn đối tượng nhận step. Bỏ qua/0 = không filter |
| index | Int | No | Vị trí hiển thị step (0-based). Bỏ qua = thêm vào cuối |
| name | String | No | Tên step hiển thị (≤255 ký tự) |
| action_id | Long | No | ID action chain từ `create_action`, chạy khi step phát. Type cho phép trong step: tag, richmenu, bookmark, friend_info, block, handling_status (chain chứa type khác bị từ chối). Bỏ qua = không action |

**Sample Input:**

```json
{
  "bot_id": "mj3Kzx",
  "scenario_id": 3001,
  "delay_type": 0,
  "start_day": 1,
  "start_time": "10:00",
  "filter_manager_id": 501,
  "name": "Day 1 morning",
  "action_id": 88
}
```

**Output:** envelope passthrough từ backend:

```json
{
  "result": "ok",
  "data": { "success": true, "step_id": 9001 },
  "error": null
}
```

- `data.step_id` = **ID step mới** — dùng cho `update_scenario_step` (section template / template_id).
- Trùng lịch với step hiện có → `data.success=false` + `data.message` = 「設定した時間に配信するメッセージが既に存在しています。」.

---

## 6. update_scenario_step

**Description:** Tool cập nhật step hiện có. Gửi ít nhất một trong 3 section — field nào có mặt quyết định phần được
lưu; khi kết hợp sẽ chạy theo thứ tự **timing → template content**:

1. **TIMING** — `delay_type` + các field start tương ứng, tùy chọn `filter_manager_id` / `index` / `name` /
   `action_id`; ghi đè lịch gửi của step. Các field timing phụ (start_day/start_time/.../action_id) **bắt buộc đi kèm
   `delay_type`** — gửi thiếu delay_type sẽ bị từ chối.
   - `action_id`: bỏ qua = giữ chain hiện tại; 0 = gỡ liên kết (chain KHÔNG bị xóa); ID mới (từ `create_action`) =
     gắn lại step vào chain đó.
   - `filter_manager_id`: bỏ qua = giữ nhánh filter hiện tại; 0 = gỡ — **kèm xoá luôn filter**
     (row `filter_manager` + các điều kiện `filters_v2`) khi không còn step nào khác tham chiếu
     (nhánh nhiều step dùng chung filter thì chỉ gỡ khỏi step này, filter giữ nguyên); ID **khác** với ID hiện tại
     của step bị từ chối — muốn nhánh filter khác thì tạo step mới bằng `create_scenario_step`. Muốn đổi điều kiện
     của nhánh → dùng `update_filter(target='scenario')` với filter_manager_id hiện tại.
2. **TEMPLATE** — `template_name` + `template` (cả hai bắt buộc cùng nhau): tạo template riêng của step (bỏ
   `template.templateChildId`) hoặc sửa template hiện có (đặt `templateChildId` từ get_scenario_detail; type KHÔNG
   đổi được). **Nested array trong payload bị thay thế toàn bộ (REPLACE-ALL)** — gửi lại item không đổi để giữ.
   Khi `template.text.ogp.imageUrl` được đặt, server gửi HTTP request tới URL đó để kiểm tra kích thước ảnh.
   Nội dung template được validate giống `update_broadcast` / `create_*_template` (cả tạo mới lẫn sửa) — vd form
   Standard / Color: panel `text` bắt buộc (không rỗng, ≤ 60 ký tự); text: `content` 1–5000 ký tự; location: đủ
   title / address / latitude / longitude. (Trước 2026-09-26 section này không validate — panel thiếu text bị lưu
   `tmp_button.text = ''`.)
3. **TEMPLATE_ID** — gắn template có sẵn (từ list_templates) vào step theo **reference** (append id vào
   `step.template_ids`). Gắn lại id đã có trên step = không đổi gì (no-op); step dùng chung template nên sửa
   template sau đó **có** phản ánh vào step. Child template trong group template bị từ chối.

`template` và `template_id` KHÔNG được gửi cùng lúc.

**Tool:** `update_scenario_step`

**Input:**
| Name | Type | Required | Description |
|-------------------|--------|----------|-------------------------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string |
| scenario_id | Long | Yes | ID Scenario (thuộc bot) |
| step_id | Long | Yes | ID step cần cập nhật (từ get_scenario_detail, thuộc scenario) |
| delay_type | Int | No* | Switch của section TIMING — 0\|1\|2, cùng ý nghĩa với create_scenario_step. Bỏ qua (cùng các field timing khác) = không đổi lịch |
| start_day | Int | Cond | Số ngày delay (≥0). Bắt buộc khi delay_type=0; 0 cho delay_type=1/2 |
| start_time | String | Cond | delay_type=0 → 'H:mm'/'HH:mm'/'HH:mm:ss'. Không dùng cho delay_type=1/2 |
| elapsed_hours | Int | Cond | GIỜ cho delay_type=2 (0–72). Bắt buộc khi delay_type=2 |
| elapsed_minutes | Int | Cond | PHÚT cho delay_type=2 (0–59). Bắt buộc khi delay_type=2 |
| filter_manager_id | Long | No | Bỏ qua = giữ nhánh filter hiện tại; 0 = gỡ; ID khác hiện tại = bị từ chối |
| index | Int | No | Vị trí hiển thị step (0-based) |
| name | String | No | Tên step (≤255 ký tự) |
| action_id | Long | No | Bỏ qua = giữ chain hiện tại; 0 = gỡ liên kết; ID dương (từ create_action) = gắn lại chain. Type cho phép: tag, richmenu, bookmark, friend_info, block, handling_status |
| template_name | String | Cond | Tên template hiển thị (≤20 ký tự). Bắt buộc đi cùng `template` |
| template | Object | Cond | Payload template typed (Sub Object Template Payload bên dưới). Bắt buộc đi cùng `template_name`. 1 step chỉ có tối đa 1 template quick reply (#41643) |
| template_id | Long | Cond | ID template parent có sẵn (từ list_templates) để GẮN vào step (reference, dùng chung). Không gửi cùng `template`. Quy tắc tối đa 1 quick reply / step (group template tính cả con) |

\* Ít nhất một trong 3 section (timing / template / template_id) phải có mặt.

**Sub Object Template Payload** (`template` — cùng shape BroadcastMessage của create_broadcast):
| Name | Type | Required | Description |
|-----------------|--------|----------|--------------------------------------------------------------------------------------------------|
| type | String | Yes | text \| image \| location \| form (video/voice/stamp KHÔNG hỗ trợ cho step) |
| templateChildId | Long | No | CHỈ khi sửa — template_child_id hiện có (từ get_scenario_detail). Bỏ qua = tạo template mới |
| text | Object | Cond | [type=text] Payload text (TextTemplateData) |
| image | Object | Cond | [type=image] Payload ảnh (img_path = download_url từ get_file_params) |
| location | Object | Cond | [type=location] Payload vị trí |
| form | Object | Cond | [type=form] Payload form/carousel |

**Sample Input (đổi timing + giữ filter và action hiện có):**

```json
{
  "bot_id": "mj3Kzx",
  "scenario_id": 3001,
  "step_id": 6002,
  "delay_type": 0,
  "start_day": 2,
  "start_time": "09:30"
}
```

**Sample Input (thêm template text mới vào step):**

```json
{
  "bot_id": "mj3Kzx",
  "scenario_id": 3001,
  "step_id": 6002,
  "template_name": "Day 2 greeting",
  "template": {
    "type": "text",
    "text": {
      "content": "おはようございます！"
    }
  }
}
```

**Output:** Object gộp kết quả từng section đã chạy:
| Name | Type | Description |
|---------------|-----------------|-----------------------------------------------------------------------------------|
| timing | Object | (Khi có section timing) envelope `{ result: "ok", data: { success: true, step_id }, error: null }` |
| template | Object | (Khi có section template) envelope `{ result: "ok", data: { success: true }, error: null }` — backend không trả template_child_id; đọc lại bằng `get_scenario_detail` |
| template_copy | Object | (Khi có template_id) envelope `{ result: "ok", data: { success: true, message: "Create step message template success" }, error: null }` |
| _warnings | Array of String | (Chỉ khi có) Cảnh báo — vd chain action hiện có không load lại được nên bị gỡ khỏi step |

> **Add-friend greeting** (`update_addfriend_setting_message`) đã chuyển sang nhóm welcome-message — xem
> [27-welcome-message.md](27-welcome-message.md).
