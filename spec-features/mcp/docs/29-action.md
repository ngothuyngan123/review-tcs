# Action Tools

Nhóm tool quản lý **action chain** độc lập, tái sử dụng được. Một action chain là danh sách các thao tác được thực thi
tuần tự lên friend khi được kích hoạt: gắn/gỡ tag, start/stop/resume scenario, hiện/ẩn rich menu, gửi text, gửi
template, set field friend-info, block, bookmark, đổi handling status.

Workflow điển hình: `create_action` → nhận `action_id` → gắn `action_id` vào object kích hoạt (tag, button template,
broadcast, friend-info field, scenario step, welcome message, autoreply, ...). Chain chưa gắn vào đâu thì không chạy.
Sửa chain sau này bằng `update_action`.

## 1. create_action

**Description:** Tool tạo action chain độc lập, tái sử dụng và trả về `action_id`. Chain được tạo ở trạng thái CHƯA
GẮN (unattached) — sau khi tạo, gắn `action_id` trả về vào object cần kích hoạt nó; chain không được gắn sẽ nằm không
được dùng. Mỗi item được validate theo từng type trước khi lưu, item không hợp lệ sẽ báo lỗi rõ ràng thay vì bị bỏ qua
im lặng (backend PHP vốn bỏ qua im lặng item sai format — lớp MCP chặn trước).

**Tool:** `create_action`

**Input:**
| Name | Type | Required | Description |
|---------|-----------------------|----------|---------------------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| type | String | Yes | Nhãn ngữ cảnh lưu trên chain (t_actions.type) — chọn theo domain dự định gắn, vd `'tag'` \| `'template'` \| `'broadcast_v2'`. Free text, ≤255 ký tự. Cố định khi tạo — update_action không đổi được |
| details | Array of DetailAction | Yes | Mảng action item typed, có thứ tự (không rỗng). Thực thi từ trên xuống khi chain phát |

**Sub Object DetailAction** (mỗi phần tử của `details`):
| Name | Type | Required | Description |
|---------------|---------|----------|--------------------------------------------------------------------------------------------------------------|
| id | Long | No | t_actions_detail.id hiện có — truyền khi update item có sẵn để giữ DB id. Bỏ qua khi tạo mới |
| actionId | Long | No | t_actions.id (chain ID) hiện có — truyền cho item đã tồn tại để tái sử dụng chain. Bỏ qua cho item mới |
| title | String | No | Tiêu đề hiển thị (vd タグ, シナリオ). Bỏ qua = dùng default theo type |
| type | String | Yes | Loại action: `tag` \| `scenario` \| `richmenu` \| `text` \| `bookmark` \| `friend_info` \| `block` \| `handling_status` \| `template` |
| active | Boolean | No | Item có active trong flow bình thường không (true/false) |
| isEditContent | Boolean | No | data.content có cho user sửa không (chủ yếu cho text/bookmark). Default false |
| data | Object | Yes | Payload typed theo type (Sub Object ActionData) — CHỈ điền nhóm field của `type` đã chọn |

**Sub Object ActionData** (điền đúng nhóm field theo `type`):
| Type | Field | Type | Description |
|------------------|----------------------|---------------|--------------------------------------------------------------------------------------------------|
| tag | ids | Array of Long | Các tag ID cần gắn/gỡ |
| tag | tagAction | String | `add` \| `remove` |
| tag | isSelectAll | Boolean | Áp dụng cho tất cả friend match. Default false |
| scenario | scenarioId | Long | Scenario ID (start/resume; bỏ qua cho stop) |
| scenario | scenarioAction | String | `stop` \| `start` \| `resume` |
| scenario | startDay | Int | Chỉ resume — ngày bắt đầu lại N (≥0) |
| scenario | scenarioName | String | Tên scenario (đặt khi user đưa tên; để trống khi đưa raw ID — server tự enrich) |
| richmenu | richmenuId | Long | Rich menu ID (show; bỏ qua cho hide) |
| richmenu | richmenuAction | String | `hide` \| `show` |
| richmenu | richmenuName | String | Tên rich menu (như scenarioName) |
| text | content | String | Nội dung text gửi đi, ≤5000 ký tự. Hỗ trợ token text (danh sách token nằm trong description của field `content` trong input schema) |
| bookmark | bookmarkAction | String | `add` \| `remove` |
| bookmark | bookmarkContent | String | Ghi chú bookmark (tùy chọn) |
| block | blockAction | String | `block` \| `unblock` \| `show` \| `hide` (show/hide = hiện lại/ẩn friend trong chat 1:1) |
| handling_status | handlingStatusId | Long | Status ID (bắt buộc cho attach; bỏ qua cho detach) |
| handling_status | handlingStatusAction | String | `attach` \| `detach` |
| handling_status | handlingStatusName | String | Tên status (như scenarioName) |
| template | templateId | Long | Template ID cần gửi. Card/carousel → dùng GROUP (parent) template id, KHÔNG dùng child id |
| template | templateName | String | Tên template (như scenarioName) |
| friend_info | friendInfo | Object | Cập nhật field friend-info (Sub Object FriendInfoData) |
| (chung) | selectedGroupId | String | [scenario\|richmenu\|template] Group ID dạng STRING từ response list_*. Để trống khi đưa raw ID |
| (chung) | isExpandGroup | Boolean | [scenario\|richmenu\|handling_status] Trạng thái expand UI. Default false |

**Sub Object FriendInfoData** (`data.friendInfo` khi type=friend_info):
| Name | Type | Required | Description |
|-----------|---------|----------|--------------------------------------------------------------------------------------------------------------------|
| fieldId | Long | Yes | Field ID. CUSTOM = số dương (từ list_friend_info_fields). BUILT-IN = số âm: -1 system_name, -2 phone, -3 email, -4 birthday, -6 prefecture, -7 postal, -8 city, -9 street, -10 building |
| fieldType | String | Cond | `select` \| `text` \| `date` \| `point`. Bắt buộc cho field CUSTOM; bỏ qua cho BUILT-IN (tự suy từ id) |
| op | String | Yes | Thao tác. select/text/date: `set` \| `clear` \| `today` (today = date only). point: `point_clear` \| `point_replace` \| `point_plus` \| `point_minus` |
| value | String | Cond | Giá trị set. set(text/select): chuỗi giá trị; set(date): 'YYYY-MM-DD'; point số cố định: số dạng chuỗi (vd "100"). Bỏ qua cho clear/today/point random |
| optionId | Long | Cond | CHỈ select custom + set — option id đã chọn (từ setting_actions[].id) |
| fieldName | String | No | Tên hiển thị field CUSTOM (từ list_friend_info_fields). Bỏ qua cho built-in hoặc để server enrich |
| groupOpen | Int | No | Folder id UI của field CUSTOM (group_id từ list_friend_info_fields). Bỏ qua cho built-in |
| isRandom | Boolean | No | CHỈ point — true để dùng số ngẫu nhiên trong [from, to] thay vì giá trị cố định. Default false |
| from | Int | Cond | Đầu khoảng random point. Bắt buộc khi isRandom=true |
| to | Int | Cond | Cuối khoảng random point. Bắt buộc khi isRandom=true |

**Validation (MCP layer, trước khi gọi LME):**

- `details` không rỗng; mỗi item validate required field theo type (thiếu → lỗi kèm hướng dẫn)
- `data.content` của item text ≤5000 ký tự
- Mọi entity ID tham chiếu (tag/scenario/richmenu/template/friend_info custom/handling_status) được kiểm tra quyền sở
  hữu bot; đồng thời server enrich các field hiển thị từ DB

**Sample Input:**

```json
{
  "bot_id": "mj3Kzx",
  "type": "tag",
  "details": [
    {
      "type": "tag",
      "data": {
        "ids": [12, 15],
        "tagAction": "add"
      }
    },
    {
      "type": "text",
      "data": {
        "content": "ご登録ありがとうございます！"
      }
    },
    {
      "type": "friend_info",
      "data": {
        "friendInfo": {
          "fieldId": 34,
          "fieldType": "point",
          "op": "point_plus",
          "value": "100"
        }
      }
    }
  ]
}
```

**Output:** envelope passthrough, `action_id` được surface lên top-level để client đọc một chỗ (verify live 2026-09-21).

**Sample Output:**

```json
{
  "result": "ok",
  "data": { "success": true, "action_id": 123 },
  "error": null,
  "action_id": 123
}
```

---

## 2. update_action

**Description:** Tool cập nhật action chain hiện có theo `action_id` — **FULL-STATE REPLACE (thay thế toàn bộ)**: mảng
`details` gửi lên THAY THẾ toàn bộ danh sách detail hiện có. **Detail hiện có mà không nằm trong mảng sẽ bị XÓA** (đây
không phải diff/merge). Muốn giữ item hiện có → gửi lại kèm detail `id` của nó; item không có `id` được insert mới.
`type` của chain cố định từ lúc tạo, không đổi được ở đây (tool tự fetch chain hiện có để lấy type + kiểm tra tồn
tại — chain không tồn tại → lỗi). Mỗi item vẫn được validate theo type trước khi lưu.

> ⚠️ **Cảnh báo REPLACE-ALL:** luôn build lại mảng `details` đầy đủ (vd từ `get_scenario_detail.steps[].actions` hoặc
> `get_tag_detail.setting_actions`) rồi chỉnh phần cần đổi. Gửi thiếu item = mất dữ liệu im lặng.

**Tool:** `update_action`

**Input:**
| Name | Type | Required | Description |
|-----------|-----------------------|----------|--------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| action_id | Long | Yes | ID chain cần update — giá trị `create_action` trả về, hoặc `action_id` lưu trên object đang gắn chain |
| details | Array of DetailAction | Yes | Danh sách detail THAY THẾ TOÀN BỘ (cùng format DetailAction như create_action). Item giữ/sửa → gửi kèm detail `id`; bỏ item = xóa; item không `id` = insert mới |

**Sample Input:**

```json
{
  "bot_id": "mj3Kzx",
  "action_id": 123,
  "details": [
    {
      "id": 301,
      "type": "tag",
      "data": {
        "ids": [12, 15],
        "tagAction": "add"
      }
    },
    {
      "type": "richmenu",
      "data": {
        "richmenuId": 7,
        "richmenuAction": "show"
      }
    }
  ]
}
```

**Output:** envelope như create_action, `action_id` được surface lên top-level.

**Sample Output:**

```json
{
  "result": "ok",
  "data": { "success": true, "action_id": 123 },
  "error": null,
  "action_id": 123
}
```
