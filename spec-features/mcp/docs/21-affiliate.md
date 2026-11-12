# Affiliate Tools

## 1. list_affiliates

**Description:** Tool trả về danh sách affiliate thuộc cùng admin với bot. Gọi tool này TRƯỚC khi build broadcast
filter `type: "affiliate"` — `affiliate_search` phải chứa `affiliate.id` thật và `preview_original` phải là `username`
từ list này.

**Tool:** `list_affiliates`

**Input:**
| Name | Type | Required | Description |
|-----------|-----------------|----------|----------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| usernames | Array of String | No | Lọc theo username (EXACT match, case-insensitive, trim). Multiple values OR-joined.
Ví dụ: `["phuongthanh_aff2"]` |
| page | Integer | No | Số trang (default:
1)                                                                                          |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100)                                                                       |

**Output:**
| Name | Type | Description |
|---------------------|-------------|----------------------------------------------------------------------------------------------------|
| affiliates | Json Array | Array Object Affiliate |
| pagination | Json Object | Thông tin phân trang |
| not_found_usernames | Json Array | (Optional) Usernames trong filter `usernames` không match — chỉ xuất hiện khi
truyền `usernames`  |

**Sub Object Affiliate:**
| Name | Type | Description |
|----------|--------|-------------------------------------------------------------------------------------|
| id | Int | ID của affiliate (raw int, không hash) — dùng cho `affiliate_search` trong filter |
| username | String | Username — dùng cho `preview_original` trong filter |
| email | String | Email |

**Sample Output:**

```json
{
  "affiliates": [
    { "id": 8,  "username": "phuongthanh_aff2", "email": "phuongthanh@example.com" },
    { "id": 11, "username": "thanhntp142",      "email": "thanhntp@example.com" }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2
  }
}
```

---

## 2. Cách dùng trong broadcast filter

Sau khi `list_affiliates`, dùng `id` + `username` trong filter `type: "affiliate"`:

### Include — `affiliate_filter_type = 0` (INT)

Lọc friend được giới thiệu **bởi 1 trong các** affiliate đã chọn.

```json
{
  "type": "affiliate",
  "active": true,
  "affiliate_search": [8],
  "affiliate_filter_type": 0,
  "preview_original": "phuongthanh_aff2"
}
```

### Exclude — `affiliate_filter_type = "1"` (STRING)

**Loại trừ** friend được giới thiệu bởi 1 trong các affiliate đã chọn.

```json
{
  "type": "affiliate",
  "active": true,
  "affiliate_search": [11],
  "affiliate_filter_type": "1",
  "preview_original": "thanhntp142"
}
```

### Multiple affiliates

```json
{
  "type": "affiliate",
  "active": true,
  "affiliate_search": [44, 48],
  "affiliate_filter_type": 0,
  "preview_original": "Thanhntp_edit11ttttt・test aff"
}
```

> Khi nhiều affiliate: `preview_original` = các username **join bằng `・`** (Japanese middot, U+30FB) — KHÔNG phải dấu
> phẩy, KHÔNG phải khoảng trắng. Thứ tự username phải khớp thứ tự id trong `affiliate_search`.

**Field rules:**
| Field | Type | Note |
|------------------------|-----------------|-------------------------------------------------------------------------------|
| `active`               | bool | Always `true`                                                                 |
| `affiliate_search`     | array of int | `affiliate.id` từ `list_affiliates`. OR-joined. |
| `affiliate_filter_type`| int \| string | **INT `0`** = include / **STRING `"1"`** = exclude (type
mixing)              |
| `preview_original`     | string | Single = username. Multi = các username join bằng `・` (middot)               |

> **Type mixing**: include = INT 0, exclude = STRING "1" — đúng theo payload web frontend.

**ID resolution:**

- User đưa TÊN/username → gọi `list_affiliates(bot_id)` resolve name → id, copy `username` vào `preview_original`.
- User đưa RAW ID → bỏ qua `list_affiliates`; chỉ fill `affiliate_search`, để `preview_original = ""` — server
  validate ownership và tự enrich `preview_original` từ DB khi submit.
- User KHÔNG chỉ định affiliate nào → DỪNG và hỏi lại; KHÔNG gọi list rồi fill toàn bộ ID.
