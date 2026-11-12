# Richmenu Tools

## 1. list_richmenus

**Description:** Tool trả về danh sách Richmenu kèm số friend đang hiển thị mỗi richmenu — dùng để tra richmenu_id từ tên
richmenu. Hỗ trợ optional filter `names` (EXACT, case-insensitive, trim whitespace) để tìm richmenu theo tên đầy đủ;
tên không match sẽ nằm trong `not_found_names`.

**Tool:** `list_richmenus`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Mảng tên richmenu EXACT (case-insensitive, trim). Multiple = OR. Partial KHÔNG match. Khuyến nghị dùng khi user chỉ định tên cụ thể thay vì paginate. |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-----------------|-----------------|-------------|
| richmenus | Json Array | Array Object Richmenu Summary |
| pagination | Json Object | Thông tin phân trang |
| not_found_names | Array of String | (Chỉ trả khi truyền `names`) Các tên không match richmenu nào — confirm với user trước khi tiếp tục |

**Sub Object Richmenu Summary:**
| Name | Type | Description |
|--------------|--------|-------------|
| id | Long | ID của Richmenu trong hệ thống |
| group_id | Long | ID của category/group chứa richmenu (0 nếu Uncategorized). Dùng làm `selected_group_id` khi tạo action richmenu trong broadcast. |
| name | String | Tên Richmenu |
| title_menu | String | Tiêu đề menu |
| width | Int | Chiều rộng richmenu (px) |
| height | Int | Chiều cao richmenu (px) |
| size | String | Kích thước dạng chuỗi `"{width} x {height}"` pixel (vd `"2500 x 1686"`, `"2500 x 843"`) — KHÔNG phải enum full/half/compact (verify live R04-01, 2026-09-21) |
| layout | String | Layout type: `SIX_AREAS` / `FOUR_AREAS_EQUAL` / `FOUR_AREAS_TOP_LARGE` / `THREE_AREAS` / `TWO_AREAS_VERTICAL` / `TWO_AREAS_HORIZONTAL` / `ONE_AREA_FULL` / `CUSTOM` / `THREE_AREAS_VERTICAL` / `TWO_AREAS_TOP_BOTTOM` / `TWO_AREAS_LEFT_RIGHT` / `ONE_AREA_CENTER` |
| url_image | String | URL ảnh richmenu |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |
| friend_count | Long | Số friend đang hiển thị richmenu này (is_blocked=0) |

**Sub Object Pagination:**
| Name | Type | Description |
|-------------|------|----------------------|
| currentPage | Int | Trang hiện tại |
| limit | Int | Số record mỗi trang |
| total | Int | Tổng số record |

**Sample Output (no `names` filter):**

```json
{
  "richmenus": [
    {
      "id": 4001,
      "group_id": 5,
      "name": "Main Menu",
      "title_menu": "Menu chính",
      "width": 2500,
      "height": 1686,
      "size": "full",
      "layout": "SIX_AREAS",
      "url_image": "https://cdn.example.com/richmenu/main.jpg",
      "created_at": "2025-03-01 10:00:00",
      "friend_count": 1250
    },
    {
      "id": 4002,
      "group_id": 5,
      "name": "VIP Member Menu",
      "title_menu": "Menu VIP",
      "width": 2500,
      "height": 1686,
      "size": "full",
      "layout": "FOUR_AREAS_EQUAL",
      "url_image": "https://cdn.example.com/richmenu/vip.jpg",
      "created_at": "2025-06-15 14:00:00",
      "friend_count": 380
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2
  }
}
```

**Sample Output (with `names: ["Main Menu", "Typo Name"]`):**

```json
{
  "richmenus": [
    {
      "id": 4001,
      "group_id": 5,
      "name": "Main Menu",
      "title_menu": "Menu chính",
      "width": 2500,
      "height": 1686,
      "size": "full",
      "layout": "SIX_AREAS",
      "url_image": "https://cdn.example.com/richmenu/main.jpg",
      "created_at": "2025-03-01 10:00:00",
      "friend_count": 1250
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

## 2. get_richmenu_detail

**Description:** Tool trả về chi tiết nhiều Richmenu bao gồm cấu hình từng vùng và thống kê số lần click từng vùng theo
ngày

**Tool:** `get_richmenu_detail`

**Input:**
| Name | Type | Required | Description |
|--------------|--------|----------|------------------------------------------------------------------------------------------|
| richmenu_ids | String | Yes | Danh sách ID Rich Menu cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| from_date | String | No | Ngày bắt đầu thống kê click (format: yyyy-MM-dd, default: 30 ngày trước)                |
| to_date | String | No | Ngày kết thúc thống kê click (format: yyyy-MM-dd, default: hôm nay)                     |

**Output** (Array — mỗi phần tử là một Richmenu Detail):
| Name | Type | Description |
|------------|------------|-------------|
| id | Long | ID của Richmenu trong hệ thống |
| name | String | Tên Richmenu |
| title_menu | String | Tiêu đề menu |
| width | Int | Chiều rộng (px) |
| height | Int | Chiều cao (px) |
| layout | String | Layout type: `SIX_AREAS` / `FOUR_AREAS_EQUAL` / `FOUR_AREAS_TOP_LARGE` / `THREE_AREAS` / `TWO_AREAS_VERTICAL` / `TWO_AREAS_HORIZONTAL` / `ONE_AREA_FULL` / `CUSTOM` / `THREE_AREAS_VERTICAL` / `TWO_AREAS_TOP_BOTTOM` / `TWO_AREAS_LEFT_RIGHT` / `ONE_AREA_CENTER` |
| url_image | String | URL ảnh richmenu |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |
| areas | Json Array | Array Object Richmenu Area |

**Sub Object Richmenu Area:**
| Name | Type | Description |
|------------------|------------|-------------|
| id | Long | ID của area |
| action_type | String | Loại action raw của vùng: `SHARE_TEXT` / `CAMERA` / `CAMERA_ROLL` / `SHARE_LOCATION` / `OPEN_PROFILE` / `OPEN_FRIEND` / `SETTING_CUSTOM` / `RICH` / `TEXT` / `EMAIL` / `PHONE` / `ACCOUNT_LINE` / `DELETE_RICH` / `URL` (có thể null) |
| type_open_url | String | Nhãn mô tả loại hành động đã resolve: `Share Text` / `Camera` / `Camera Roll` / `Share Location` / `Open Profile` / `Open Friend` / `Custom URL` / `Switch Rich Menu` / `Text Message` / `Email` / `Phone Call` / `LINE Account` / `Delete Rich Menu` / `Direct URL` / `Form` / `Product` / `Booking Event` / `Conversion` / `Booking Calendar` / `Salon Calendar` / `Lesson Calendar` / `LIFF Action (via action_id)` / `Other` |
| content_open_url | String | URL đầy đủ hoặc nội dung tương ứng với action (đã build sẵn LIFF/line.me URL khi áp dụng; null nếu không có) |
| switch_to_menu | String | Tên richmenu chuyển đến khi vùng có cấu hình switch richmenu (action_type=`RICH`); null nếu không |
| actions | Json Array | Danh sách action thực thi khi click — Array Sub Object Action ([] nếu không có) |
| x | Int | Tọa độ X góc trên trái của vùng (px) |
| y | Int | Tọa độ Y góc trên trái của vùng (px) |
| width | Int | Chiều rộng vùng (px) |
| height | Int | Chiều cao vùng (px) |
| total_clicks | Object | Số lượt click theo ngày trong khoảng from_date–to_date (key: `yyyy-MM-dd`, value: số lượt click dạng Long); {} nếu không có click |

**Sub Object Action:**
| Name | Type | Description |
|-----------|-------------|-------------|
| id | Long | ID của action detail |
| action_id | Long | ID nhóm action chứa action detail này |
| type | String | Loại action: `template` / `text` / `richmenu` / `scenario` / `tag` / `bookmark` / `friend_info` / `handling_status` / `block` / `remind` / ... (giá trị khác được trả nguyên gốc) |
| content | String | Mô tả action dạng human-readable (tiếng Nhật), ví dụ: `タグ「VIP」をつける`, `テンプレート「Welcome」を送信` |
| data | Json Object | Raw data JSON của action (chỉ trả khi parse được — có thể vắng; cấu trúc phụ thuộc loại action) |

**Sample Output:**

```json
[
  {
    "id": 4001,
    "name": "Main Menu",
    "title_menu": "Menu chính",
    "width": 2500,
    "height": 1686,
    "layout": "SIX_AREAS",
    "url_image": "https://cdn.example.com/richmenu/main.jpg",
    "created_at": "2025-03-01 10:00:00",
    "areas": [
      {
        "id": 7001,
        "action_type": "URL",
        "type_open_url": "Direct URL",
        "content_open_url": "https://example.com/products",
        "switch_to_menu": null,
        "actions": [],
        "x": 0,
        "y": 0,
        "width": 833,
        "height": 843,
        "total_clicks": {
          "2025-03-01": 150,
          "2025-03-02": 230,
          "2025-03-03": 95
        }
      },
      {
        "id": 7002,
        "action_type": "TEXT",
        "type_open_url": "Text Message",
        "content_open_url": "プロモーション情報",
        "switch_to_menu": null,
        "actions": [
          {
            "id": 301,
            "action_id": 88,
            "type": "template",
            "content": "テンプレート「Promotion Template」を送信"
          },
          {
            "id": 302,
            "action_id": 88,
            "type": "tag",
            "content": "タグ「Promotion Interest」をつける"
          }
        ],
        "x": 833,
        "y": 0,
        "width": 833,
        "height": 843,
        "total_clicks": {
          "2025-03-01": 120,
          "2025-03-02": 180,
          "2025-03-03": 75
        }
      }
    ]
  }
]
```
