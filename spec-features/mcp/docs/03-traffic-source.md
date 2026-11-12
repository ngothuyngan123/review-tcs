# Traffic Source Tools

## 1. list_traffic_sources

**Description:** Tool trả về danh sách nguồn lưu lượng (traffic source) kèm thông tin thống kê cơ bản. Hỗ trợ optional
filter `names` (EXACT, case-insensitive, trim whitespace) để tìm traffic source theo tên đầy đủ. Khi truyền `names`,
response có thêm `not_found_names` chứa các tên không match traffic source nào.

**Tool:** `list_traffic_sources`

**Input:**
| Name | Type | Required | Description |
|-------|-----------------|----------|-----------------------------------------------------------------------------------|
| bot_id| String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Mảng tên traffic source EXACT (case-insensitive, trim). Multiple = OR. Partial KHÔNG
match. Khuyến nghị dùng khi user chỉ định tên cụ thể thay vì paginate. |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-----------------|-----------------|--------------------------------------|
| traffic_sources | Json Array | Array Object Traffic Source Summary |
| pagination | Json Object | Thông tin phân trang (currentPage, limit, total) |
| not_found_names | Array of String | (Chỉ trả khi truyền `names` và có tên không match) Các tên không match traffic
source nào — confirm với user trước khi tiếp tục |

**Sub Object Traffic Source Summary:**
| Name | Type | Description |
|------------------|------------|---------------------------------------------|
| id | Int | ID của traffic source |
| name | String | Tên traffic source |
| code | String | Mã code của traffic source — dùng cho token `[LANDING_INTRO_<code>]` và URL landing |
| total_user_click | Int | Tổng số lượt quét QR |
| total_user_friend| Int | Tổng số friend đã follow qua QR này |
| action_count | Int | Số người được action |
| live_time | Json Object| Thời gian hoạt động `{start, end}` — cả hai = null nếu không giới hạn thời gian |
| actions | Json Array | Danh sách action được thực thi — Sub Object Action |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)      |

**Sub Object Action:**
| Name | Type | Description |
|-----------|-------------|------------------------------------------------------------------|
| id | Long | ID của action detail |
| action_id | Long | ID nhóm action chứa action detail này |
| type | String | Loại action: `template` / `text` / `tag` / `scenario` / `richmenu` / `bookmark` / `friend_info` / `handling_status` / `block` / `remind` |
| content | String | Mô tả nội dung action (text tiếng Nhật, ví dụ: テンプレート「X」を送信, タグ「Y」をつける) |
| data | Json Object | (Optional) Cấu hình raw của action — key thay đổi theo loại action; bị bỏ qua nếu không parse được JSON |

**Sample Output (no `names` filter):**

```json
{
  "traffic_sources": [
    {
      "id": 1001,
      "name": "Summer Campaign 2026",
      "code": "SUMMER2026",
      "total_user_click": 5000,
      "total_user_friend": 3500,
      "action_count": 1000,
      "live_time": {
        "start": "2025-10-11 10:10:00",
        "end": "2025-10-20 10:10:00"
      },
      "actions": [
        {
          "id": 9001,
          "action_id": 700,
          "type": "template",
          "content": "テンプレート「Welcome Summer Campaign」を送信"
        },
        {
          "id": 9002,
          "action_id": 700,
          "type": "tag",
          "content": "タグ「Summer 2026」をつける"
        },
        {
          "id": 9003,
          "action_id": 700,
          "type": "scenario",
          "content": "ステップ「Welcome New Member」を開始"
        }
      ],
      "created_at": "2026-01-15 10:30:00"
    },
    {
      "id": 1002,
      "name": "Store Front QR",
      "code": "STOREQR01",
      "total_user_click": 12000,
      "total_user_friend": 9600,
      "action_count": 1022,
      "live_time": {
        "start": null,
        "end": null
      },
      "actions": [
        {
          "id": 9010,
          "action_id": 701,
          "type": "text",
          "content": "テキスト「Welcome to Store」を送信"
        }
      ],
      "created_at": "2025-06-20 09:00:00"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2
  }
}
```

**Sample Output (with `names: ["Summer Campaign 2026", "Typo Name"]`):**

```json
{
  "traffic_sources": [
    {
      "id": 1001,
      "name": "Summer Campaign 2026",
      "code": "SUMMER2026",
      "total_user_click": 5000,
      "total_user_friend": 3500,
      "action_count": 1000,
      "live_time": {
        "start": "2025-10-11 10:10:00",
        "end": "2025-10-20 10:10:00"
      },
      "actions": [],
      "created_at": "2026-01-15 10:30:00"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 1
  },
  "not_found_names": [
    "Typo Name"
  ]
}
```

---

## 2. get_traffic_source_detail

**Description:** Tool trả về chi tiết đầy đủ của nhiều traffic source, bao gồm các action và thống kê quét QR theo ngày
trong khoảng thời gian chỉ định (default: 1 năm gần nhất)

**Tool:** `get_traffic_source_detail`

**Input:**
| Name | Type | Required | Description |
|------------|--------|----------|-----------------------------------------------------|
| traffic_source_ids | String | Yes | Danh sách ID traffic source cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| from_date | String | No | Ngày bắt đầu (format: yyyy-MM-dd, default: 1 năm trước) |
| to_date | String | No | Ngày kết thúc (format: yyyy-MM-dd, default: hôm nay)|

**Output:** Json Array — mỗi phần tử ứng với 1 ID trong `traffic_source_ids`, cấu trúc:
| Name | Type | Description |
|-------------------|------------|--------------------------------------------|
| id | Int | ID của traffic source |
| name | String | Tên traffic source |
| code | String | Mã code của traffic source |
| link_qr_code | String | URL ảnh QR code |
| total_user_click | Int | Tổng số lượt quét QR |
| total_user_friend | Int | Tổng số friend đã follow |
| action_type | String | Loại action ("once": 1 lần, "multiple": nhiều lần) |
| action_with_friend| String | Áp dụng cho ("new_friend": new friend, "all": tất cả) |
| action_count | Int | Số người được action |
| actions | Json Array | Danh sách action được thực thi — Sub Object Action |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)     |
| scan_stats | Json Array | Array Object Daily Scan Stats |

**Sub Object Action:**
| Name | Type | Description |
|-----------|-------------|------------------------------------------------------------------|
| id | Long | ID của action detail |
| action_id | Long | ID nhóm action chứa action detail này |
| type | String | Loại action: `template` / `text` / `tag` / `scenario` / `richmenu` / `bookmark` / `friend_info` / `handling_status` / `block` / `remind` |
| content | String | Mô tả nội dung action (text tiếng Nhật, ví dụ: テンプレート「X」を送信, タグ「Y」をつける) |
| data | Json Object | (Optional) Cấu hình raw của action — key thay đổi theo loại action; bị bỏ qua nếu không parse được JSON |

**Sub Object Daily Scan Stats (from landing_histories):**
| Name | Type | Description |
|------------------------|--------|---------------------------------------|
| date | String | Ngày (format: yyyy-MM-dd)             |
| count_scan | Int | Số lượt quét trong ngày |
| count_scan_distinct | Int | Số lượt quét unique trong ngày |
| count_action | Int | Số lượt action trong ngày |
| count_action_distinct | Int | Số lượt action unique trong ngày |
| count_add_friend | Int | Số friend mới trong ngày |
| count_add_friend_new | Int | Số friend hoàn toàn mới trong ngày |
| count_scan_mobile | Int | Số lượt quét từ mobile |
| count_scan_pc | Int | Số lượt quét từ PC |
| count_click | Int | Số lượt click |

**Sample Output:**

```json
[
  {
    "id": 1001,
    "name": "Summer Campaign 2026",
    "code": "SUMMER2026",
    "link_qr_code": "https://cdn.example.com/qr/1001.png",
    "total_user_click": 5000,
    "total_user_friend": 3500,
    "action_type": "multiple",
    "action_with_friend": "all",
    "action_count": 1022,
    "actions": [
      {
        "id": 9001,
        "action_id": 700,
        "type": "template",
        "content": "テンプレート「Welcome Summer Campaign」を送信"
      },
      {
        "id": 9002,
        "action_id": 700,
        "type": "tag",
        "content": "タグ「Summer 2026」をつける"
      },
      {
        "id": 9003,
        "action_id": 700,
        "type": "scenario",
        "content": "ステップ「Welcome New Member」を開始"
      }
    ],
    "created_at": "2026-01-15 10:30:00",
    "scan_stats": [
      {
        "date": "2026-02-10",
        "count_scan": 150,
        "count_scan_distinct": 140,
        "count_action": 145,
        "count_action_distinct": 135,
        "count_add_friend": 105,
        "count_add_friend_new": 100,
        "count_scan_mobile": 120,
        "count_scan_pc": 30,
        "count_click": 50
      },
      {
        "date": "2026-02-09",
        "count_scan": 180,
        "count_scan_distinct": 165,
        "count_action": 170,
        "count_action_distinct": 155,
        "count_add_friend": 126,
        "count_add_friend_new": 120,
        "count_scan_mobile": 150,
        "count_scan_pc": 30,
        "count_click": 65
      }
    ]
  }
]
```
