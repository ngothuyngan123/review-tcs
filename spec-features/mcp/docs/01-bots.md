# Bot Tools

## 1. list_bots

**Description:** Tool trả về danh sách bot của user. Hỗ trợ optional filter `view_names` (EXACT match trên field
`view_name`, case-insensitive, trim whitespace) để tìm bot theo tên hiển thị đầy đủ. Khi truyền `view_names`, response
kèm `not_found_view_names` cho các tên không match bot nào.

**Tool:** `list_bots`

**Input:**
| Name | Type | Required | Description |
|------------|-----------------|----------|----------------------------------------|
| view_names | Array of String | No | Mảng tên hiển thị bot EXACT (case-insensitive, trim). Multiple = OR. Partial KHÔNG
match. |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|----------------------|-----------------|------------------------------------|
| bots | Json Array | Array Object Bot |
| pagination | Json Object | Thông tin phân trang |
| not_found_view_names | Array of String | (Chỉ trả khi truyền `view_names`) Các tên không match bot nào |

**Sub Object Bot:**
| Name | Type | Description |
|------------------------|--------|------------------------------------------|
| id | String | ID mã hóa (hash) của bot |
| line_id | String | LINE ID của bot (LINE Channel/OA ID, có thể null) |
| view_name | String | Tên hiển thị của bot |
| total_friend | Int | Tổng số friend của bot |
| total_friend_active | Int | Tổng số friend đang follow |
| total_friend_blocked | Int | Tổng số friend đang block |
| created_at | String | Ngày tạo bot (format: yyyy-MM-dd HH:mm:ss) |
| liff_app_id | String | LIFF App ID (có thể null) |
| liff_app_id_booking | String | LIFF App ID dành cho booking (có thể null) |

**Sample Output:**

```json
{
  "bots": [
    {
      "id": "abc123xyz",
      "line_id": "@xyz789",
      "view_name": "My Shop Official",
      "total_friend": 51231,
      "total_friend_active": 34231,
      "total_friend_blocked": 12312,
      "created_at": "2025-01-15 10:30:00",
      "liff_app_id": "1234567890-abcdefgh",
      "liff_app_id_booking": null
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 1
  }
}
```
