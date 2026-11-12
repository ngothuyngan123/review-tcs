# Chat Conversation Tools

## 1. list_conversations

**Description:** Tool trả về danh sách các cuộc hội thoại chat của bot (paginated). Kết quả sắp xếp theo hội thoại
bookmark trước (`is_bookmark` DESC), rồi theo tin nhắn mới nhất (`last_time_message` DESC). Mỗi item có field
`position` (1-based, đánh số toàn cục qua các trang): position=1 là hội thoại có tin nhắn mới nhất. Hỗ trợ các filter:
tên (`line_names` — partial match trên cả tên LINE và tên hiển thị hệ thống), `confirm_status` (đã xác nhận/chưa xác
nhận), 対応状態 (`handling_status_names` / `handling_status_ids` — merge, OR), tag (`tag_names` / `tag_ids` — merge,
kết hợp theo `tag_mode`). Tên (names) là EXACT match (case-insensitive, trim) — tên không tồn tại trong bot → 400.
Các loại filter kết hợp AND với nhau. Mặc định chỉ trả hội thoại không bị ẩn (`is_hide=0`, gồm active + blocked);
truyền `conversation_hide=1` để chỉ lấy hội thoại đã ẩn, `2` để lấy tất cả.

**Tool:** `list_conversations`

**Input:**
| Name | Type | Required | Description |
|------------|-----------------|----------|------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| line_names | Array of String | No | Mảng pattern PARTIAL match (LIKE `%value%`, case-insensitive, trim) trên **cả**
tên LINE (`line_user.name`) **và** tên hiển thị hệ thống (`line_user.view_name`) — khớp 1 trong 2 là được. Multiple =
OR. Ví dụ: `["田中", "Nguyen"]`. Khi truyền, response có thêm `not_found_line_names` |
| confirm_status | Integer | No | 0 = chỉ hội thoại đã xác nhận/đã đọc (admin đã phản hồi — `confirm_count` = 0);
1 = chỉ hội thoại chưa xác nhận/chưa đọc (đang chờ phản hồi — `confirm_count` > 0). Bỏ qua = không filter theo chiều
này. Giá trị khác 0/1 → 400 |
| handling_status_names | Array of String | No | Mảng tên 対応状態 EXACT match (case-insensitive, trim). Ưu tiên hơn
`handling_status_ids` — user thường gọi theo tên. MCP resolve tên → ID phía server, merge với `handling_status_ids`
(deduped). Tên không tồn tại trong bot → 400 kèm danh sách tên thiếu. OR semantic |
| handling_status_ids | Array of Long | No | Mảng ID status_chat — dùng khi AI đã resolve ID từ
list_handling_statuses. Merge với `handling_status_names`. OR semantic. ID không thuộc bot hoặc inactive → 400 |
| tag_names | Array of String | No | Mảng tên tag EXACT match (case-insensitive, trim). Merge với `tag_ids` (deduped).
Tên không tồn tại → 400 kèm danh sách tên thiếu. Logic kết hợp theo `tag_mode` |
| tag_ids | Array of Long | No | Mảng tag ID — dùng khi AI đã resolve ID. Merge với `tag_names`. ID không thuộc bot
hoặc đã xóa → 400. Logic theo `tag_mode` |
| tag_mode | String | No | 'or' (default): friend có ít nhất 1 tag; 'and': friend có tất cả tag. Không phân biệt hoa
thường. Chỉ có ý nghĩa khi có filter tag |
| conversation_hide | Int | No | Bỏ qua (default) = chỉ hội thoại active. `1` = chỉ hội thoại **đã ẩn**. `2` = tất cả
(gồm cả đã ẩn — dùng khi tìm theo tên mà friend có thể nằm trong hội thoại ẩn). Giá trị khác 1/2 → 400 |
| page | Int | No | Số trang (default: 1)                    |
| limit | Int | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|----------------------|-----------------|--------------------------------|
| total | Int | Tổng số cuộc hội thoại |
| page | Int | Trang hiện tại |
| limit | Int | Số lượng record mỗi trang |
| total_pages | Int | Tổng số trang |
| conversations | Json Array | Array Object Conversation |
| not_found_line_names | Array of String | (Chỉ trả khi truyền `line_names`) Patterns không match conversation nào —
`line_names` 指定時のみ返却 |

**Sub Object Conversation:**
| Name | Type | Description |
|-------------------|--------|---------------------------------------------------------|
| position | Int | Thứ tự toàn cục 1-based qua các trang (position=1 = hội thoại có tin nhắn mới nhất). **Lưu ý**: hiện chỉ được gán khi gọi có ít nhất 1 filter; gọi không filter trả `null` |
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) — dùng cho `send_message` / `get_conversation_detail` / `update_conversation_handling_status` |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| line_name | String | Tên hiển thị trên LINE |
| system_name | String | Tên hiển thị hệ thống (`line_user.view_name`) — field riêng, null nếu chưa đặt |
| last_message | String | Nội dung tin nhắn cuối cùng |
| last_time_message | String | Thời gian tin nhắn cuối (format: yyyy-MM-dd HH:mm:ss)   |
| confirm_status | String | Trạng thái xác nhận: `"read"` (đã xác nhận — `confirm_count` = 0) hoặc `"unread"` (chưa xác nhận — `confirm_count` > 0) |
| handling_status_id | Long | ID trạng thái đối ứng (`status_chat.id`). null = chưa gán |
| handling_status_name | String | Tên trạng thái đối ứng (`status_chat.name_status`). null = chưa gán |

**Sample Output:**

```json
{
  "total": 5200,
  "page": 1,
  "limit": 100,
  "total_pages": 52,
  "conversations": [
    {
      "position": 1,
      "lmessage_friend_id": 50001,
      "line_friend_id": "U1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6",
      "line_name": "Nguyen Van A",
      "system_name": null,
      "last_message": "Cảm ơn bạn đã liên hệ!",
      "last_time_message": "2026-02-10 16:45:30",
      "confirm_status": "read",
      "handling_status_id": null,
      "handling_status_name": null
    },
    {
      "position": 2,
      "lmessage_friend_id": 50002,
      "line_friend_id": "U2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7",
      "line_name": "Tran Thi B",
      "system_name": "Anh B VIP",
      "last_message": "Tôi muốn hỏi về sản phẩm",
      "last_time_message": "2026-02-10 15:30:00",
      "confirm_status": "unread",
      "handling_status_id": 16638,
      "handling_status_name": "対応中"
    },
    {
      "position": 3,
      "lmessage_friend_id": 50003,
      "line_friend_id": "U3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8",
      "line_name": "Le Van C",
      "system_name": null,
      "last_message": "Đơn hàng của bạn đã được xử lý",
      "last_time_message": "2026-02-10 14:20:15",
      "confirm_status": "read",
      "handling_status_id": null,
      "handling_status_name": null
    }
  ]
}
```

---

## 2. get_conversation_detail

**Description:** Tool trả về lịch sử tin nhắn chat (paginated) của nhiều friend. Giới hạn độ sâu lịch sử theo loại
contract của bot: bot **free** = 180 ngày gần nhất, bot **trả phí** = 365 ngày gần nhất; `from_date` sớm hơn giới hạn
sẽ bị tự động kéo về (clamp) ngày sớm nhất cho phép. Không trả tin nhắn gửi lỗi (`messages_v2s.status = 2`), giống màn
chat web (`ChatController::refreshMessage`); `total` / `total_pages` tính trên số tin sau khi lọc.

**Tool:** `get_conversation_detail`

**Input:**
| Name | Type | Required | Description |
|--------------|------|----------|---------------------------------------------------------|
| lmessage_friend_ids | String | Yes | Danh sách `lmessage_friend_id` (ID nội bộ DB = `line_user.id`) cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| from_date | String | No | Ngày bắt đầu (format: yyyy-MM-dd). Default = ngày sớm nhất cho phép (180 ngày trước với bot free, 365 ngày trước với bot trả phí). Truyền sớm hơn giới hạn sẽ bị clamp |
| to_date | String | No | Ngày kết thúc (format: yyyy-MM-dd, default: hôm nay)    |
| page | Int | No | Số trang (default: 1)                                   |
| limit | Int | No | Số lượng record mỗi trang (default: 100, max: 100)      |

**Output:** (mỗi phần tử của array — 1 phần tử cho mỗi `lmessage_friend_id`)
| Name | Type | Description |
|--------------|------------|-----------------------------------------|
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| line_name | String | Tên hiển thị trên LINE |
| total | Int | Tổng số tin nhắn trong khoảng thời gian (không tính tin gửi lỗi `status = 2`) |
| page | Int | Trang hiện tại |
| limit | Int | Số lượng record mỗi trang |
| total_pages | Int | Tổng số trang |
| messages | Json Array | Array Object Message |

**Sub Object Message:**
| Name | Type | Description |
|---------------|-------------|----------------------------------------------------|
| message_id | Long | ID của tin nhắn |
| sender_type | String | Người gửi: `"user"` (friend) hoặc `"bot"` |
| sender_name | String | `sender_type="user"` → tên LINE của friend; `sender_type="bot"` do nhân viên gửi → username nhân viên; bot gửi tự động → null |
| message_type | String | Loại tin nhắn: `text` / `image` / `video` / `audio` / `sticker` / `scenario` / `stop_scenario` / `scenario_empty_step` / `start_remind` / `stop_remind` / `pdf` / `file` / `location` / `broadcast` / `template` / `event` / `action` / `action_from_booking` / `action_from_booking_salon` / `action_from_booking_lesson` / `unknown` |
| content | String hoặc Json Array | Nội dung tin nhắn. Thường là String (text, hoặc URL media đã prepend host). Với tin nhắn gửi từ template/broadcast (có capture templates), là mảng `[{type, content}]` — `type`: `text`/`buttons`/`image`/`video`/`audio`/`sticker`/`location`/`introduction`; `content` là text, URL hoặc JSON object tùy type |
| source | Json Object | Nguồn gửi tin nhắn (null nếu tin nhắn không có nguồn — vd từ user)              |
| sent_at | String | Thời gian gửi (format: yyyy-MM-dd HH:mm:ss)        |

**Sub Object Source:**
| Name | Type | Description |
|------|--------|-----------------------------------------------------------------------|
| type | String | Loại nguồn: `broadcast` / `scenario` / `template` / `action` / `event` (null nếu không xác định được) |
| name | String | Tên của nguồn |

**Sample Output:**

```json
[
  {
  "lmessage_friend_id": 50001,
  "line_friend_id": "U1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6",
  "line_name": "Nguyen Van A",
  "total": 156,
  "page": 1,
  "limit": 100,
  "total_pages": 2,
  "messages": [
    {
      "message_id": 800001,
      "sender_type": "bot",
      "sender_name": "Tanaka Yuki",
      "message_type": "text",
      "content": "Cảm ơn bạn đã liên hệ!",
      "source": null,
      "sent_at": "2026-02-10 16:45:30"
    },
    {
      "message_id": 800000,
      "sender_type": "user",
      "sender_name": "Nguyen Van A",
      "message_type": "text",
      "content": "Tôi muốn đặt hàng sản phẩm ABC",
      "source": null,
      "sent_at": "2026-02-10 16:44:15"
    },
    {
      "message_id": 799999,
      "sender_type": "bot",
      "sender_name": null,
      "message_type": "scenario",
      "content": [
        {
          "type": "text",
          "content": "Chào mừng bạn đến với chương trình thành viên!"
        },
        {
          "type": "image",
          "content": "https://lme.example.com/media/welcome.jpg"
        }
      ],
      "source": {
        "type": "scenario",
        "name": "Welcome New Member"
      },
      "sent_at": "2026-02-10 16:40:00"
    },
    {
      "message_id": 799997,
      "sender_type": "bot",
      "sender_name": null,
      "message_type": "image",
      "content": "https://lme.example.com/media/sale.jpg",
      "source": {
        "type": "broadcast",
        "name": "February Sale Announcement"
      },
      "sent_at": "2026-02-10 16:35:00"
    },
    {
      "message_id": 799996,
      "sender_type": "bot",
      "sender_name": null,
      "message_type": "action",
      "content": "Thông tin sản phẩm của bạn đây ạ",
      "source": {
        "type": "action",
        "name": "Product Info Action"
      },
      "sent_at": "2026-02-10 16:30:00"
    }
  ]
  }
]
```

---

## 3. send_message

**Description:** Tool gửi **1 tin nhắn** ngay lập tức tới 1 LINE user thật (chat 1:1) — bộ gửi hợp nhất (unified
sender). Mỗi lần gọi phải truyền **đúng 1 loại nội dung**, tool tự route theo field được truyền:

1. `text` — tin nhắn text thuần (kèm tùy chọn `shorten_url`).
2. `template_id` — gửi 1 template có sẵn; group template gửi tất cả sub-template trong 1 batch (kèm tùy chọn
   `edited_content` = text thay thế chỉ cho lần gửi này — template đã lưu KHÔNG bị sửa).
3. `media_items` — gửi file media theo URL, tối đa 5 items (kèm tùy chọn `text_before_media` = text gửi trước media; media +
   text tính chung vào giới hạn 5 message của LINE).

Truyền 0 hoặc từ 2 loại nội dung trở lên → 400. Param phụ phải đi đúng loại: `shorten_url` chỉ đi với `text`,
`edited_content` chỉ đi với `template_id`, `text_before_media` chỉ đi với `media_items` — sai kết hợp → 400.

Tin đã gửi **không thu hồi được**, và mỗi lần gọi lại sẽ gửi thêm 1 tin nữa — không retry lời gọi có thể đã thành
công. **Side effect**: nếu bot bật `is_confirm` (chat 1:1 phase 2), gửi thành công sẽ tự động confirm hội thoại
(`conversation.confirm_count` → 0, tương đương `list_conversations(confirm_status=0)` = đã đối ứng/đã đọc).

**Tool:** `send_message`

**Input:**
| Name | Type | Required | Description |
|--------------|--------|----------|-----------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| lmessage_friend_id | Long | Yes | ID nội bộ DB của friend (`line_user.id`) nhận tin, lấy từ `list_conversations` |
| text | String | No* | [loại text] Nội dung text cần gửi (1–5000 ký tự). Không kết hợp với `template_id` / `media_items` |
| shorten_url | Integer | No | [loại text] Flag 1\|0: `1` = rút gọn URL trong text (mặc định); `0` = giữ nguyên URL. Chỉ hợp lệ khi đi cùng `text` |
| template_id | Long | No* | [loại template] ID số của template có sẵn cần gửi (từ `list_templates`). Group template gửi tất cả sub-template trong 1 batch. Không kết hợp với `text` / `media_items`. Template phải thuộc bot |
| edited_content | String | No | [loại template] Text thay thế chỉ dùng cho **lần gửi này** — template đã lưu KHÔNG bị thay đổi (muốn sửa chính template thì dùng `update_text_template`). Placeholder như `{name}` vẫn được áp dụng. Chỉ hợp lệ khi đi cùng `template_id` |
| media_items | String | No* | [loại media] JSON array string, mỗi item `{"type","url"}`. type: `image`/`video`/`audio`/`voice`/`pdf`; `url` = `download_url` do `get_file_params` trả về (URL ngoài sẽ hết hạn hoặc LME không truy cập được). Tối đa 5 items. Không kết hợp với `text` / `template_id` |
| text_before_media | String | No | [loại media] Text gửi **trước** các file media. Chỉ hợp lệ khi đi cùng `media_items` — muốn gửi text đơn thuần thì dùng `text` |

\* Bắt buộc truyền đúng 1 trong 3: `text` / `template_id` / `media_items`.

**Cấu trúc `media_items`:**

```json
[
  {
    "type": "image",
    "url": "https://cdn.example.com/photo.jpg"
  },
  {
    "type": "pdf",
    "url": "https://cdn.example.com/doc.pdf"
  }
]
```

> **`url` lấy từ đâu**: upload file qua tool `get_file_params` (nhận mọi loại file — image/audio/video/pdf...) rồi
> dùng `download_url` trả về. **KHÔNG** dán URL CDN ngoài (Azure blob, OpenAI CDN, imgur...) — LME không truy cập
> được hoặc URL hết hạn.

**Output:**
| Name | Type | Description |
|---------|--------|-------------------------------|
| status | String | Chuỗi kết quả forward từ LME (dạng toString của response PHP); `"sent success"` nếu LME không trả response |

**Sample Output:**

```json
{
  "status": "{status=success}"
}
```

---

## 4. update_conversation_handling_status

**Description:** Tool cập nhật trạng thái đối ứng (対応状態) của một conversation trong chat 1:1. Dùng
`list_handling_statuses` để lấy ID trạng thái hợp lệ, `lmessage_friend_id` lấy từ `list_conversations`.
`handling_status_id` phải thuộc bot và đang active → nếu không → 400. Friend phải có conversation trong bot → nếu
không → 400.

**Tool:** `update_conversation_handling_status`

**Input:**
| Name | Type | Required | Description |
|---|---|---|---|
| bot_id | String | Yes | Bot ID hash string lấy từ list_bots |
| lmessage_friend_id | Long | Yes | Internal DB id của friend (từ field `lmessage_friend_id` trong list_conversations) |
| handling_status_id | Long | No | ID của trạng thái đối ứng (lấy từ list_handling_statuses). Bỏ qua, null hoặc `0` = xóa trạng thái hiện tại |

**Output:** envelope passthrough: `{ "result": "ok", "data": <response của endpoint web change-handling-status>, "error": null }`

---

## 5. get_file_params

**Description:** Tool nhận **1 file do MCP client upload** (mọi loại — image/audio/video/PDF...) và trả về object
`{download_url, file_id, file_name, mime_type, ...}` của file đó. Với file **ảnh** (mime_type `image/*` hoặc đuôi
file ảnh: jpg/jpeg/png/gif/webp/bmp), server đọc thêm kích thước pixel và bổ sung `img_width` / `img_height` — để
làm việc này server thực hiện 1 request http(s) ra ngoài tới `download_url` do client cung cấp. File không phải ảnh
được trả nguyên trạng. Thay thế 4 tool cũ `get_image_fileparams` / `get_audio_fileparams` / `get_video_fileparams` /
`get_pdf_fileparams` (đã gộp).

Dùng `download_url` trả về ở mọi chỗ cần URL media: `media_items[].url` của `send_message`, `imgPath`/`img_path`
trong image/form template (kèm `img_width`/`img_height` cho tap-zone layout), thumbnail... **KHÔNG** dán URL ngoài
(Azure blob, OpenAI CDN, imgur...) — hết hạn hoặc LME không truy cập được. Yêu cầu MCP client hỗ trợ upload file
(fileParams); nếu file được tạo bằng code interpreter, hiển thị cho user trước (dạng link download) để file được
upload lên storage và có `file_id`.

**Tool:** `get_file_params`

**Input:**
| Name | Type | Required | Description |
|------|-------------|----------|-------------|
| file | File Object | Yes | Object file đã upload do MCP client cung cấp (`{download_url, file_id, file_name?, mime_type?}`). Đính kèm file trong client — không tự build object này hoặc dán URL ngoài |

**Output:**
| Name | Type | Description |
|--------------|--------|-------------|
| download_url | String | URL tải file trên storage — dùng làm URL media trong các tool khác |
| file_id | String | ID file trên storage |
| file_name | String | Tên file (nếu client cung cấp) |
| mime_type | String | MIME type (nếu client cung cấp) |
| img_width | Int | (Chỉ file ảnh đọc được kích thước) Chiều rộng pixel |
| img_height | Int | (Chỉ file ảnh đọc được kích thước) Chiều cao pixel |

> Không đọc được kích thước ảnh (URL không phải http/https, ảnh lỗi...) → trả object nguyên trạng, không có
> `img_width`/`img_height`. Thiếu `download_url` (file chưa upload thành công) → 400.

**Sample Output:**

```json
{
  "download_url": "https://storage.example.com/files/abc123/photo.png",
  "file_id": "file-abc123",
  "file_name": "photo.png",
  "mime_type": "image/png",
  "img_width": 1024,
  "img_height": 768
}
```
