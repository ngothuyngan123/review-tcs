# Welcome / Add-friend Greeting Tools

Nhóm tool cấu hình **あいさつメッセージ (welcome message)** — tin nhắn tự động gửi khi LINE user follow / re-follow /
unblock bot. Welcome message là 1 tin text cho mỗi trigger (giống màn web 友だち追加設定 V2). Tool riêng
`update_addfriend_setting_message` đã bị xoá khỏi code; param `setting_messages` (slot auto-send, ghi vào cột màn cũ)
đã bị gỡ khỏi `update_welcome_message` (#43015).

> Class: `McpWelcomeMessageTool`. Relay: `POST /mcp/get-welcome-message`, `POST /mcp/update-welcome-message` → LME
> `api/mobile/get-setting-add-friend-v2` / `api/mobile/save-setting-add-friend-v2`.

## 1. get_welcome_message

**Description:** Lấy welcome message hiện tại theo trigger type (`add_new`/`add_old`/`unblock`). Trả về action chain
ID, text message và danh sách action detail hiện tại. **Gọi trước `update_welcome_message`** để xem trạng thái hiện
tại trước khi sửa.

**Tool:** `get_welcome_message`

**Input:**
| Name | Type | Required | Description |
|--------|--------|----------|--------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string (từ list_bots) |
| type | String | Yes | Trigger type: `add_new` (follow lần đầu) / `add_old` (re-follow) / `unblock` (bỏ chặn). Mỗi type có message + action chain độc lập |

**Output:**
| Name | Type | Description |
|--------|-------------|--------------------------------------|
| result | String | `ok` khi thành công |
| data | Json Object | Payload — Sub Object Data |
| error | String | null khi thành công |

**Sub Object Data:**
| Name | Type | Description |
|--------------|------------|--------------------------------------|
| actionId | Long | ID action chain đang gắn với trigger type (null nếu chưa gắn) |
| message | String | Nội dung text welcome hiện tại (null nếu chưa cài) |
| detailAction | Json Array | Các action detail row thô của chain hiện tại (mỗi row gồm id, action_id, type, data{...}, is_edit_content, list_tags với type=tag...; shape tuỳ loại action). `[]` nếu chưa gắn chain |
| urlAddFriend | String | URL add friend của bot (dạng https://line.me/R/ti/p/...) |
| qrCode | String | URL ảnh QR code add friend của bot |

**Sample Output:**

```json
{
  "result": "ok",
  "data": {
    "actionId": null,
    "message": "友だち追加ありがとうございます！",
    "detailAction": [],
    "urlAddFriend": "https://line.me/R/ti/p/%40abc1234x",
    "qrCode": "https://media.example.com/media/qr_image/qr_add_friend_bot_528.png?v=1758000000"
  },
  "error": null
}
```

---

## 2. update_welcome_message

**Description:** Cập nhật welcome message cho 1 trigger type (`add_new`/`add_old`/`unblock`) — lời chào tự động gửi
khi LINE user follow / re-follow / unblock bot. Gọi `get_welcome_message` trước để xem trạng thái hiện tại.
**Text:** `message` ≤ 5000 ký tự; bỏ qua = giữ nguyên text hiện tại (tool tự đọc lại và gửi lại); `''` = xoá.
**Action chain:** `action_id` tham chiếu chain tạo bởi `create_action` — bỏ qua = giữ liên kết hiện tại; `0` = gỡ liên
kết (chain vẫn còn trong account); id dương = liên kết chain đó (là reference — các sửa đổi `update_action` sau này vẫn
áp dụng vào đây).

**Tool:** `update_welcome_message`

**Input:**
| Name | Type | Required | Description |
|----------------------|---------|----------|--------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string (từ list_bots) |
| type | String | Yes | `add_new` / `add_old` / `unblock` — mỗi type độc lập, update 1 type không ảnh hưởng type khác. Nếu user không nói rõ trigger → hỏi (show cả 3), KHÔNG mặc định add_new |
| message | String | No | Text body (≤ 5000 ký tự). Bỏ qua/null = giữ nguyên text hiện tại (tool tự đọc lại từ server và gửi lại). `''` = xoá message (server xoá template row bên dưới) |
| action_id | Long | No | Bỏ qua = giữ action chain hiện tại. `0` = gỡ liên kết (chain vẫn còn trong account). Id dương (từ create_action) = liên kết chain — reference, sửa bằng update_action sau này vẫn áp dụng. Detail type: tag / scenario / richmenu / text / bookmark / friend_info / block / handling_status / template |

**Output:**
| Name | Type | Description |
|--------|-------------|--------------------------------------|
| result | String | `ok` khi thành công |
| data | Json Object | Kết quả lưu — Sub Object Data |
| error | String | null khi thành công |

**Sub Object Data:**
| Name | Type | Description |
|-----------|---------|--------------------------------------|
| success | Boolean | true = lưu thành công; false = lỗi (khi đó có thêm key `error` chứa message) |
| type | String | Trigger type đã update |
| action_id | Long | ID action chain đang gắn sau khi update (không có key này nếu không gắn chain) |
| id | Long | ID row `add_friend_setting` của bot |

**Sample Output:**

```json
{
  "result": "ok",
  "data": {
    "success": true,
    "type": "add_new",
    "action_id": 456,
    "id": 12
  },
  "error": null
}
```
