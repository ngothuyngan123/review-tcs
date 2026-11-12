# Folder Tools

Bộ tool generic quản lý folder cho 5 domain, chọn domain qua param `type`. Thay thế các tool folder riêng từng domain
trước đây (`list_tag_folders`, `create_tag_folder`, `update_tag_folder`, `list_friend_info_folders`,
`create_friend_info_folder`, `update_friend_info_folder`, `list_autoreply_folders`, `create_autoreply_folder`,
`update_autoreply_folder`, `create_template_folder`, `update_template_folder`, `create_scenario_folder`). Mỗi nhánh
`type` được route tới đúng flow backend của domain đó nên hành vi và shape response khớp với domain.

Mapping `type` → `category.kind` trong DB:

| type | kind | Domain |
|-------------|------|------------------------|
| tag | 0 | Tag folder |
| autoreply | 1 | Auto-reply folder |
| template | 2 | Template folder |
| scenario | 11 | Scenario folder |
| friend_info | 12 | Friend Information folder |

## 1. create_folder

**Description:** Tool tạo folder mới cho bot. Param `type` chọn domain: tag | autoreply | template | scenario |
friend_info — request được route tới cùng flow backend với tool tạo folder của domain đó, nên hành vi và shape
response khớp domain. `name` bắt buộc: tối đa 20 ký tự với type=template, tối đa 15 ký tự với các type còn lại. Tên
folder trùng trong cùng domain bị từ chối trước khi gọi backend (ngoại lệ: friend_info — backend chấp nhận trùng tên).
Tool này chỉ tạo mới; đổi tên folder hiện có dùng `update_folder`.

**Tool:** `create_folder`

**Input:**
| Name | Type | Required | Description |
|--------|--------|----------|-------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| type | String | Yes | Domain của folder: `tag` \| `autoreply` \| `template` \| `scenario` \| `friend_info` |
| name | String | Yes | Tên folder. Không rỗng; tối đa 20 ký tự với type=template, tối đa 15 ký tự với các type khác |

**Validation (MCP layer):**

- `type` phải là một trong 5 giá trị (không phân biệt hoa/thường, trim)
- `name` không rỗng, ≤ 20 ký tự (template) / ≤ 15 ký tự (các type khác)
- Trùng tên folder trong cùng domain → từ chối (trừ friend_info)
- type=template: từ chối nếu bot đang ở trạng thái backup
- type=scenario: endpoint backend là dual-mode, tool luôn gửi `folder_id=""` để chỉ đi nhánh tạo mới

**Output:** pass-through response từ backend LME của từng domain:

| type | Shape response |
|-------------|-----------------------------------------------------------------|
| tag | Bọc envelope: `{ result, data: { message, item: { id, bot_id, name, kind, position, count } }, error }` (verify live FLD-C01, 2026-09-21 — không phải shape trần) |
| template | `{ success, folder_id }` |
| autoreply / scenario / friend_info | Pass-through LME (dạng `{ status, data: { ... } }`) |

**Sample Input:**

```json
{
  "bot_id": "y2kWN2",
  "type": "tag",
  "name": "Khách VIP"
}
```

**Sample Output (type=tag):**

```json
{
  "result": "ok",
  "data": {
    "message": "作成しました。",
    "item": {
      "id": 45,
      "bot_id": 528,
      "name": "Khách VIP",
      "kind": 0,
      "position": 5,
      "count": 0
    }
  },
  "error": null
}
```

---

## 2. list_folders

**Description:** Tool liệt kê folder của một domain cho bot; dùng để resolve tên folder → folder ID số trước các lời
gọi cần folder/category id. Param `type` chọn domain: tag | autoreply | template | scenario | friend_info. Shape
response khác nhau theo type (xem bảng Output).

**Tool:** `list_folders`

**Input:**
| Name | Type | Required | Description |
|--------|--------|----------|-------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| type | String | Yes | Domain cần liệt kê: `tag` \| `autoreply` \| `template` \| `scenario` \| `friend_info` |

**Output theo type:**

| type | Shape response |
|-------------|-------------------------------------------------------------------------------------------|
| tag | Bọc envelope: `{ result, data: { categories: [{id, name, kind, position, count}], count_default }, error }` — item có thêm field `kind`; count_default = số tag trong folder ảo 未分類 (category_id=0, không có DB record). (Verify live FLD-R01, 2026-09-21 — không phải shape trần) |
| autoreply | `{ folders: [{id, name, position, rule_count}], count_default }` — folder ảo 未分類 (id=0) luôn đứng đầu danh sách |
| friend_info | `{ folders: [...] }` — gồm các group built-in (未分類 id=0, 基本情報 id=-1, 国内住所 id=-2) rồi tới custom folder `{id, name, position, field_count}` |
| template | `{ folders: [{id, name, position}] }` — đọc trực tiếp từ bảng category (kind=2) |
| scenario | `{ folders: [{id, name, position}] }` — đọc trực tiếp từ bảng category (kind=11) |

**Sub Object folder built-in (chỉ type=friend_info):**
| Name | Type | Description |
|-------------|---------------|--------------------------------------------------------------------|
| id | Int | 0 = 未分類, -1 = 基本情報, -2 = 国内住所 |
| name | String | Tên group |
| field_count | Int | Số field trong group (未分類 = số custom field có group_id=0) |
| is_fixed | Boolean | (Chỉ 基本情報 / 国内住所) `true` — group cố định, không đổi tên được |
| field_ids | Array of Int | (Chỉ 基本情報 / 国内住所) ID các built-in field trong group ([-1,-2,-3,-4] / [-6,-7,-8,-9,-10]) |

**Sample Output (type=tag):**

```json
{
  "result": "ok",
  "data": {
    "categories": [
      { "id": 45, "name": "Khách VIP", "kind": 0, "position": 1, "count": 3 },
      { "id": 46, "name": "Chiến dịch hè", "kind": 0, "position": 2, "count": 8 }
    ],
    "count_default": 12
  },
  "error": null
}
```

**Sample Output (type=autoreply):**

```json
{
  "folders": [
    { "id": 0, "name": "未分類", "position": 0, "rule_count": 3 },
    { "id": 21, "name": "FAQ", "position": 1, "rule_count": 5 }
  ],
  "count_default": 3
}
```

**Sample Output (type=friend_info):**

```json
{
  "folders": [
    { "id": 0, "name": "未分類", "field_count": 2 },
    { "id": -1, "name": "基本情報", "field_count": 4, "is_fixed": true, "field_ids": [-1, -2, -3, -4] },
    { "id": -2, "name": "国内住所", "field_count": 5, "is_fixed": true, "field_ids": [-6, -7, -8, -9, -10] },
    { "id": 33, "name": "Khảo sát", "position": 1, "field_count": 3 }
  ]
}
```

**Sample Output (type=template / type=scenario):**

```json
{
  "folders": [
    { "id": 12, "name": "Khuyến mãi", "position": 1 },
    { "id": 13, "name": "Chăm sóc KH", "position": 2 }
  ]
}
```

---

## 3. update_folder

**Description:** Tool đổi tên folder hiện có của bot. Param `type` chọn domain: tag | autoreply | template | scenario |
friend_info. Folder phải tồn tại, thuộc bot và chưa bị xóa; `name` mới ghi đè tên hiện tại (tối đa 20 ký tự với
type=template, tối đa 15 với các type khác). Resolve tên folder → ID số bằng `list_folders` với cùng `type`. Với
type=friend_info chỉ custom folder (folder_id dương) đổi tên được — các group built-in (未分類 / 基本情報 / 国内住所)
là cố định.

**Tool:** `update_folder`

**Input:**
| Name | Type | Required | Description |
|-----------|--------|----------|-------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| type | String | Yes | Domain của folder: `tag` \| `autoreply` \| `template` \| `scenario` \| `friend_info` |
| folder_id | Long | Yes | Folder ID cần đổi tên (số nguyên dương, resolve qua `list_folders` cùng type) |
| name | String | Yes | Tên folder mới. Không rỗng; tối đa 20 ký tự với type=template, tối đa 15 ký tự với các type
khác |

**Validation (MCP layer):**

- `type` phải là một trong 5 giá trị
- `folder_id` phải là số nguyên dương; folder phải tồn tại đúng kind của type, thuộc bot, chưa bị xóa
- type=friend_info: folder_id ≤ 0 (group mặc định 未分類/基本情報/国内住所) bị từ chối
- `name` không rỗng, ≤ 20 ký tự (template) / ≤ 15 ký tự (các type khác)
- Trùng tên với folder khác trong cùng domain → từ chối (trừ friend_info)
- type=template: từ chối nếu bot đang ở trạng thái backup

**Output:** pass-through response từ backend LME của từng domain:

| type | Shape response |
|-------------|----------------------------------------------------|
| tag | `{ message, item: { ... } }` |
| template | `{ success, folder_id }` (TC-364 — KHÔNG trả về library dump) |
| autoreply / scenario / friend_info | Pass-through LME (dạng `{ status, data: { ... } }`) |

**Sample Input:**

```json
{
  "bot_id": "y2kWN2",
  "type": "friend_info",
  "folder_id": 33,
  "name": "Khảo sát 2026"
}
```
