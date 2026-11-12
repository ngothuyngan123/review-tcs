# Event Tools

## 1. list_events

**Description:** Tool trả về danh sách event top-level (type_event_new=1) của bot — dùng để resolve event title sang id
phục vụ build Event Booking URL (LIFF) referenced trong broadcast Quick Reply content. Hỗ trợ optional filter `titles` (
PARTIAL substring match trên field `title`, case-insensitive, trim). Response được sort theo `position`.

**Tool:** `list_events`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|--------------------------------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| titles | Array of String | No | Mảng pattern partial match (LIKE `%value%` trên `title`, case-insensitive, trim).
Multiple = OR. Ví dụ: `["新春", "Sale"]`           |

**Output:**
| Name | Type | Description |
|------------------|-----------------|----------------------------------------------------------------------------|
| events | Json Array | Array Object Event (sort theo `position`)                                  |
| not_found_titles | Array of String | (Chỉ trả khi truyền `titles`) Patterns không match event nào |

**Sub Object Event:**
| Name | Type | Description |
|-------|--------|----------------------|
| id | Int | ID của event |
| title | String | Tiêu đề event |

**Sample Output:**

```json
{
  "events": [
    {
      "id": 101,
      "title": "新春キャンペーン"
    },
    {
      "id": 102,
      "title": "Spring Sale 2026"
    },
    {
      "id": 103,
      "title": "Workshop Booking"
    }
  ]
}
```

**Sample Output (với `titles=["Sale", "missing"]`):**

```json
{
  "events": [
    {
      "id": 102,
      "title": "Spring Sale 2026"
    }
  ],
  "not_found_titles": [
    "missing"
  ]
}
```

**Notes:**

- Filter `titles` dùng **partial match** (LIKE `%value%`) — khác với các tool khác dùng EXACT match
- Không có pagination — trả về toàn bộ events (sort theo position)
- Chỉ trả về top-level events (`type_event_new=1`)
