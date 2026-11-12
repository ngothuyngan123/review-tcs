# Cross Analysis Tools

## 1. list_cross_analyses

**Description:** Tool trả về danh sách tất cả cấu hình Cross Analysis của bot, bao gồm loại hàng và số cột — để AI biết
các phân tích đang có và gọi tool detail/result phù hợp.

**Tool:** `list_cross_analyses`

**Input:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|------|------|-------------|
| crosslytics | Json Array | Array Object Crosslytics |
| pagination | Object | Thông tin phân trang — Sub Object Pagination |

**Sub Object Pagination:**
| Name | Type | Description |
|------|------|-------------|
| currentPage | Int | Trang hiện tại |
| limit | Int | Số record mỗi trang |
| total | Int | Tổng số record |

**Sub Object Crosslytics:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID của Cross Analysis |
| name | String | Tên phân tích |
| row_type | String | Loại hàng: `friend_info` = theo giá trị thông tin bạn bè / `tag` = theo tag / `follow_date` = theo
ngày kết bạn |
| column_count | Int | Số cột của phân tích |
| status | String | `published` = đã công khai / `draft` = bản nháp |
| last_updated | String | Thời điểm cập nhật gần nhất (format: yyyy-MM-dd HH:mm:ss) |

**Sample Output:**

```json
{
  "crosslytics": [
    {
      "id": 1,
      "name": "Phân tích theo vùng",
      "row_type": "friend_info",
      "column_count": 3,
      "status": "published",
      "last_updated": "2026-02-28 10:30:00"
    },
    {
      "id": 2,
      "name": "Phân tích theo tag VIP",
      "row_type": "tag",
      "column_count": 2,
      "status": "published",
      "last_updated": "2026-01-15 08:00:00"
    },
    {
      "id": 3,
      "name": "Draft phân tích mới",
      "row_type": "follow_date",
      "column_count": 0,
      "status": "draft",
      "last_updated": "2026-03-01 09:00:00"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 3
  }
}
```

---

## 2. get_cross_analysis_detail

**Description:** Tool trả về cấu hình đầy đủ của nhiều Cross Analysis, bao gồm loại hàng, filter tổng, cấu hình các cột
và danh sách ngày có dữ liệu kết quả — để AI hiểu cấu trúc trước khi gọi tool lấy kết quả.

**Tool:** `get_cross_analysis_detail`

**Input:**
| Name | Type | Required | Description |
|-----------|--------|----------|-------------|
| cross_ids | String | Yes | Danh sách ID Cross Analysis cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |

**Output:** Json Array — mỗi phần tử ứng với 1 ID trong `cross_ids`, cấu trúc:
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID của Cross Analysis |
| name | String | Tên phân tích |
| row_type | String | `friend_info` / `tag` / `follow_date` |
| row_setting | Object | Cấu hình hàng — Sub Object RowSetting (thay đổi tùy row_type) |
| total_filter | Json Array | Filter tổng áp dụng cho toàn bộ phân tích — Sub Object Filter |
| columns | Json Array | Danh sách cột — Sub Object Column |
| display_types | Json Array | Các loại count được hiển thị: `active_friend`, `friend_blocked`, `bot_blocked`, `total` |
| available_dates | Json Array | Danh sách ngày có dữ liệu kết quả (tối đa 7 ngày gần nhất, sắp giảm dần, format: yyyy-MM-dd) |

**Sub Object RowSetting — row_type = "friend_info":**
| Name | Type | Description |
|------|------|-------------|
| friend_info_id | Int | ID của friend information setting |
| friend_info_label | String | Tên hiển thị của field thông tin bạn bè |

**Sub Object RowSetting — row_type = "tag":**
| Name | Type | Description |
|------|------|-------------|
| tags | Json Array | Danh sách tên tag dùng làm hàng (String array) |

**Sub Object RowSetting — row_type = "follow_date":**
| Name | Type | Description |
|------|------|-------------|
| start_date | String | Ngày bắt đầu khoảng thời gian (format: yyyy-MM-dd) |
| end_date | String | Ngày kết thúc khoảng thời gian (format: yyyy-MM-dd) |

**Sub Object Column:**
| Name | Type | Description |
|------|------|-------------|
| name | String | Tên cột |
| filters | Json Array | Filter bổ sung của cột — Sub Object Filter (null nếu không có filter) |

**Sub Object Filter:**
| Name | Type | Description |
|------|------|-------------|
| id | Int | ID của filter |
| type | String | Loại filter (tag / friend_info / ...) |
| operator | String | Điều kiện kết hợp: `and` / `or` (giá trị thô từ DB) |
| preview_content | String | Nội dung mô tả filter (text hiển thị cho AI) |

**Sample Output:**

```json
[
  {
  "id": 1,
  "name": "Phân tích theo vùng",
  "row_type": "friend_info",
  "row_setting": {
    "friend_info_id": 42,
    "friend_info_label": "Địa chỉ"
  },
  "total_filter": [
    { "id": 901, "type": "tag", "operator": "and", "preview_content": "VIP Member" }
  ],
  "columns": [
    {
      "name": "Cột 1",
      "filters": [
        { "id": 902, "type": "tag", "operator": "and", "preview_content": "Mới đăng ký" }
      ]
    },
    {
      "name": "Cột 2",
      "filters": [
        { "id": 903, "type": "tag", "operator": "and", "preview_content": "Đã mua hàng" }
      ]
    },
    {
      "name": "Cột 3",
      "filters": null
    }
  ],
  "display_types": ["active_friend", "friend_blocked", "total"],
  "available_dates": ["2026-03-03", "2026-03-02", "2026-03-01", "2026-02-28"]
  }
]
```

---

## 3. get_cross_analysis_result

**Description:** Tool trả về bảng kết quả phân tích cross của một ngày cụ thể, gồm count bạn bè theo từng ô (hàng ×
cột) — để AI phân tích phân bố và so sánh theo thời gian.

**Tool:** `get_cross_analysis_result`

**Input:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| cross_id | Long | Yes | ID Cross Analysis lấy từ tool list_cross_analyses |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| date | String | No | Ngày cần lấy kết quả (format: yyyy-MM-dd). Không truyền = lấy ngày mới nhất có data |

**Output:**
| Name | Type | Description |
|------|------|-------------|
| cross_id | Int | ID Cross Analysis |
| date | String | Ngày của kết quả (format: yyyy-MM-dd). ⚠️ Trả chuỗi rỗng `""` khi cross chưa có dữ liệu ngày nào (verify live H14, 2026-09-21) |
| total_users | Int | Tổng số user thỏa mãn filter tổng |
| rows | Json Array | Danh sách hàng — Sub Object Row. Empty array (và total_users=0) nếu không có data ngày được chọn |

**Sub Object Row:**
| Name | Type | Description |
|------|------|-------------|
| label | String | Nhãn hàng: giá trị friend info / tên tag / date range string (e.g. "2024-01-01 ~ 2024-03-31") |
| cells | Json Array | Danh sách ô — Sub Object Cell. Ô đầu tiên luôn là cột `対象人数` (tổng số người của hàng), các ô sau ứng với từng cột của phân tích |

**Sub Object Cell:**
| Name | Type | Description |
|------|------|-------------|
| column | String | Tên cột (`対象人数` với ô đầu tiên) |
| total | Int | Tổng friend (có nếu `total` trong display_types) |
| active_friend | Int | Friend đang active — chưa block bot (có nếu `active_friend` trong display_types) |
| friend_blocked | Int | Friend đã block bot (có nếu `friend_blocked` trong display_types) |
| bot_blocked | Int | Bot đã block friend (có nếu `bot_blocked` trong display_types) |

> Các field count chỉ xuất hiện khi được bật trong `display_types` (xem tool `get_cross_analysis_detail`). `total` chỉ
> xuất hiện khi có từ 2 loại count trở lên được bật. Ô có tất cả count = 0 vẫn được trả về (không bỏ qua).

**Sample Output:**

```json
{
  "cross_id": 1,
  "date": "2026-03-03",
  "total_users": 1500,
  "rows": [
    {
      "label": "Hà Nội",
      "cells": [
        { "column": "対象人数", "total": 38, "active_friend": 35, "friend_blocked": 3 },
        { "column": "Cột 1", "total": 13, "active_friend": 12, "friend_blocked": 1 },
        { "column": "Cột 2", "total": 5,  "active_friend": 5,  "friend_blocked": 0 },
        { "column": "Cột 3", "total": 20, "active_friend": 18, "friend_blocked": 1 }
      ]
    },
    {
      "label": "TP.HCM",
      "cells": [
        { "column": "対象人数", "total": 12, "active_friend": 11, "friend_blocked": 1 },
        { "column": "Cột 1", "total": 4, "active_friend": 3, "friend_blocked": 1 },
        { "column": "Cột 2", "total": 8, "active_friend": 8, "friend_blocked": 0 },
        { "column": "Cột 3", "total": 0, "active_friend": 0, "friend_blocked": 0 }
      ]
    },
    {
      "label": "Đà Nẵng",
      "cells": [
        { "column": "対象人数", "total": 21, "active_friend": 19, "friend_blocked": 2 },
        { "column": "Cột 1", "total": 7, "active_friend": 7, "friend_blocked": 0 },
        { "column": "Cột 2", "total": 3, "active_friend": 2, "friend_blocked": 1 },
        { "column": "Cột 3", "total": 11, "active_friend": 10, "friend_blocked": 1 }
      ]
    }
  ]
}
```
