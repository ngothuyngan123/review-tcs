# URL Tools

## 1. list_urls

**Description:** Tool trả về danh sách URL tracking kèm thống kê gửi, tỷ lệ mở và tỷ lệ click. Hỗ trợ optional filter
`names` (EXACT, case-insensitive, trim whitespace) để tìm URL theo tên đầy đủ. Khi truyền `names`, response có thêm
`not_found_names` chứa các tên không match URL nào.

**Tool:** `list_urls`

**Input:**
| Name | Type | Required | Description |
|-------|-----------------|----------|-----------------------------------------------------------------------------------|
| bot_id| String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Mảng tên URL (campaign name) EXACT (case-insensitive, trim). Multiple = OR. Partial
KHÔNG match. Khuyến nghị dùng khi user chỉ định tên cụ thể thay vì paginate. |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-----------------|-----------------|----------------------|
| urls | Json Array | Array Object URL |
| pagination | Json Object | Thông tin phân trang (currentPage, limit, total) |
| not_found_names | Array of String | (Chỉ trả khi truyền `names` và có tên không match) Các tên không match URL nào —
confirm với user trước khi tiếp tục |

**Sub Object URL:**
| Name | Type | Description |
|-------------------|--------|------------------------------------------------|
| id | Int | ID của URL |
| name | String | Tên URL |
| url | String | Đường dẫn URL gốc |
| send_count | Int | Số lượng lần gửi URL |
| view_count | Int | Số lượt xem/mở |
| open_rate | Float | Tỷ lệ mở/xem (view_count / send_count * 100, làm tròn 1 chữ số thập phân) |
| unique_click | Int | Số lượt click duy nhất |
| unique_click_rate | Float | Tỷ lệ click duy nhất (unique_click / send_count * 100, làm tròn 1 chữ số thập phân) |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)         |

**Sample Output (no `names` filter):**

```json
{
  "urls": [
    {
      "id": 301,
      "name": "Summer Sale Landing Page",
      "url": "https://example.com/summer-sale",
      "send_count": 10000,
      "view_count": 6500,
      "open_rate": 65.0,
      "unique_click": 4200,
      "unique_click_rate": 42.0,
      "created_at": "2026-01-15 10:00:00"
    },
    {
      "id": 302,
      "name": "Product Catalog",
      "url": "https://example.com/products",
      "send_count": 25000,
      "view_count": 18000,
      "open_rate": 72.0,
      "unique_click": 12500,
      "unique_click_rate": 50.0,
      "created_at": "2025-06-01 09:00:00"
    },
    {
      "id": 303,
      "name": "Member Registration",
      "url": "https://example.com/register",
      "send_count": 8000,
      "view_count": 5200,
      "open_rate": 65.0,
      "unique_click": 3800,
      "unique_click_rate": 47.5,
      "created_at": "2025-08-20 14:30:00"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 3
  }
}
```

**Sample Output (with `names: ["Summer Sale Landing Page", "Typo Name"]`):**

```json
{
  "urls": [
    {
      "id": 301,
      "name": "Summer Sale Landing Page",
      "url": "https://example.com/summer-sale",
      "send_count": 10000,
      "view_count": 6500,
      "open_rate": 65.0,
      "unique_click": 4200,
      "unique_click_rate": 42.0,
      "created_at": "2026-01-15 10:00:00"
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

## 2. get_url_detail

**Description:** Tool trả về chi tiết của nhiều URL bao gồm lịch sử mở của từng friend trong khoảng thời gian chỉ định

**Tool:** `get_url_detail`

**Input:**
| Name | Type | Required | Description |
|-----------|--------|----------|---------------------------------------------------------|
| url_ids | String | Yes | Danh sách ID URL cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| from_date | String | No | Ngày bắt đầu (format: yyyy-MM-dd, default: 1 năm trước) |
| to_date | String | No | Ngày kết thúc (format: yyyy-MM-dd, default: hôm nay)    |
| page | Int | No | Số trang (default: 1)                                   |
| limit | Int | No | Số lượng record mỗi trang (default: 20, max: 100)    |

**Output:** Json Array — mỗi phần tử ứng với 1 ID trong `url_ids`, cấu trúc:
| Name | Type | Description |
|-------------------|------------|------------------------------------------------|
| id | Int | ID của URL |
| name | String | Tên URL |
| url | String | Đường dẫn URL gốc |
| send_count | Int | Số lượng lần gửi URL |
| view_count | Int | Số lượt xem/mở |
| open_rate | Float | Tỷ lệ mở/xem (view_count / send_count * 100) |
| unique_click | Int | Số lượt click duy nhất |
| unique_click_rate | Float | Tỷ lệ click duy nhất (unique_click / send_count * 100) |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)         |
| pagination | Json Object | Thông tin phân trang (currentPage, limit, total). Lưu ý: `total` = số record open_history của trang hiện tại |
| open_history | Json Array | Array Object URL Open History |

**Sub Object URL Open History:**
| Name | Type | Description |
|--------------|--------|---------------------------------------------|
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| line_name | String | Tên hiển thị trên LINE |
| opened_at | String | Ngày giờ mở (format: yyyy-MM-dd HH:mm:ss)   |

**Sample Output:**

```json
[
  {
    "id": 301,
    "name": "Summer Sale Landing Page",
    "url": "https://example.com/summer-sale",
    "send_count": 10000,
    "view_count": 6500,
    "open_rate": 65.0,
    "unique_click": 4200,
    "unique_click_rate": 42.0,
    "created_at": "2026-01-15 10:00:00",
    "pagination": {
      "currentPage": 1,
      "limit": 20,
      "total": 3
    },
    "open_history": [
      {
        "lmessage_friend_id": 50001,
        "line_friend_id": "U1a2b3c4d5e6f7081920a1b2c3d4e5f60",
        "line_name": "Nguyen Van A",
        "opened_at": "2026-02-10 15:30:45"
      },
      {
        "lmessage_friend_id": 50002,
        "line_friend_id": "U2b3c4d5e6f708192a03b1c2d3e4f5061",
        "line_name": "Tran Thi B",
        "opened_at": "2026-02-10 14:22:30"
      },
      {
        "lmessage_friend_id": 50003,
        "line_friend_id": "U3c4d5e6f708192a0b1c2d3e4f5061728",
        "line_name": "Le Van C",
        "opened_at": "2026-02-10 12:15:00"
      }
    ]
  }
]
```
