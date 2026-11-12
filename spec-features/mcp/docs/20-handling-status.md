# Handling Status Tools

## 1. list_handling_statuses

**Description:** Tool trả về danh sách handling (response) status (対応ステータス / `status_chat`) đã cấu hình cho bot.
Mỗi item có `id` (raw int) và `name`. Gọi tool này để lấy `status_chat.id` thật TRƯỚC khi build action
`type: "handling_status"` trong action chain (typed `DetailAction`). Hỗ trợ optional filter `names` (EXACT match trên
name, case-insensitive, trim). Khi truyền `names`, response kèm `not_found_names`.

**Tool:** `list_handling_statuses`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Lọc theo tên handling status (EXACT match, case-insensitive, trim). Multiple values OR-joined. Partial KHÔNG match. Ví dụ: `["未対応", "対応中"]` |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-------------------|-----------------|-------------|
| handling_statuses | Json Array | Array Object Handling Status |
| pagination | Json Object | Thông tin phân trang |
| not_found_names | Array of String | (Chỉ trả khi truyền `names`) Các tên không match handling status nào |

**Sub Object Handling Status:**
| Name | Type | Description |
|------|--------|-------------|
| id | Int | ID của handling status (raw int, không hash) — dùng cho `data.handlingStatusId` trong action `handling_status` |
| name | String | Tên hiển thị (= cột `name_status`) |

> Chỉ trả các status đang active (`is_save = 1`), sort theo `position`.

**Sample Output:**

```json
{
  "handling_statuses": [
    { "id": 4578, "name": "未対応" },
    { "id": 4579, "name": "対応中" },
    { "id": 4580, "name": "ステータス NGAN" }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 3
  }
}
```

---

## 2. Cách dùng trong action chain (typed detail_action)

`handling_status` là 1 loại action trong action chain typed (`DetailAction[]`) — dùng bởi các tool
`create_action` / `update_action` (details), `create_tag` / `update_tag` (actions / limit_actions),
`update_welcome_message` (actions), `create_autoreply` / `update_autoreply` (actions),
`create_scenario_step` / `update_scenario_step` (actions).
Schema nằm ngay trong input schema của tool (field camelCase) — KHÔNG cần build JSON thô.

### Attach (gắn status) — `handlingStatusAction = "attach"`

- `handlingStatusId`: **bắt buộc** — `id` thật từ `list_handling_statuses`
- `handlingStatusName`: chỉ set khi user đưa TÊN (copy `name` từ list). User đưa raw ID → để trống, server tự enrich từ DB
- `isExpandGroup`: optional, default `false`

```json
{
  "type": "handling_status",
  "data": {
    "handlingStatusAction": "attach",
    "handlingStatusId": 4580,
    "handlingStatusName": "ステータス NGAN"
  }
}
```

### Detach (bỏ gắn status) — `handlingStatusAction = "detach"`

- Bỏ qua `handlingStatusId` / `handlingStatusName`

```json
{
  "type": "handling_status",
  "data": {
    "handlingStatusAction": "detach"
  }
}
```

> Backend vẫn lưu payload legacy `compliant_status` (attach: INT id + INT action `1` + `content` = name;
> detach: STRING `""` + STRING `"2"`) — MCP builder tự convert, AI không cần tự xử lý type mixing như trước.

> Broadcast: tool `edit_broadcast_action` đã bị disable — broadcast action giờ gắn qua action chain
> (`action_id` từ `create_action`) trong `create_broadcast` / `update_broadcast`.

> Filter: filter `type: "status_chat"` (lọc friend theo handling status hiện tại — xem
> [24-status-chat-filter.md](24-status-chat-filter.md)) cũng dùng `id` từ tool này (`status_chat_search`).
