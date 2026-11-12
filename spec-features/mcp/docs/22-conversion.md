# Conversion Tools

## 1. list_conversions

**Description:** Tool trả về danh sách conversion của bot, group theo category. Gọi tool này TRƯỚC khi build broadcast
filter `type: "conversion"` — `conversion_search` phải chứa `conversion.id` thật, `open_group` phải là `category.id`, và
`preview_original` là `name` của conversion.

> Quan hệ DB: `conversion.group_id = category.id` (chỉ category có `kind = 15`).

**Tool:** `list_conversions`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|-------------------------------------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Lọc theo tên conversion (EXACT match, case-insensitive, trim). Multiple values
OR-joined. Ví dụ: `["c2", "c2 cop"]` |
| page | Integer | No | Số trang theo **category group** (default:
1)                                                               |
| limit | Integer | No | Số category mỗi trang (default: 100, max: 100)                                                                        |

> Pagination áp dụng level **category** (mỗi category trả full conversion bên trong, không split).

**Output:**
| Name | Type | Description |
|-----------------|-------------|--------------------------------------------------------------------------------------|
| categories | Json Array | Array Object Conversion Category Group |
| pagination | Json Object | Thông tin phân trang theo category |
| not_found_names | Json Array | (Optional) Names trong filter không match — chỉ xuất hiện khi truyền `names`        |

**Sub Object Conversion Category Group:**
| Name | Type | Description |
|---------------|-------------|-------------------------------------------------------------------|
| category_id | Int | ID của category (raw int) — dùng cho `open_group` trong filter |
| category_name | String | Tên category |
| conversions | Json Array | Array Object Conversion thuộc category này |

**Sub Object Conversion:**
| Name | Type | Description |
|------------|--------|-----------------------------------------------------------------------------------------------|
| id | Int | ID của conversion (raw int) — dùng cho `conversion_search` trong filter (convert sang STRING) |
| name | String | Tên conversion — dùng cho `preview_original` trong filter |
| unique_key | String | Key của token `[CONVERSION_<unique_key>]` trong text content (= cột `conversion.unique_key`) |

> Conversion không thuộc category nào → gom vào group `category_id = 0`, `category_name = "(Uncategorized)"`.

**Sample Output:**

```json
{
  "categories": [
    {
      "category_id": 6834,
      "category_name": "Group A",
      "conversions": [
        { "id": 1189, "name": "c2", "unique_key": "abc123" },
        { "id": 1190, "name": "c2 cop", "unique_key": "def456" }
      ]
    },
    {
      "category_id": 6835,
      "category_name": "タイプ2",
      "conversions": [
        { "id": 456, "name": "Conv X", "unique_key": "ghi789" }
      ]
    }
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

Sau khi `list_conversions`, dùng `id` + `name` + `category_id` trong filter `type: "conversion"`:

### Include single — `conversion_condition = 0` (INT)

Lọc friend đã access conversion đã chọn.

```json
{
  "type": "conversion",
  "active": true,
  "conversion_search": "456",
  "conversion_condition": 0,
  "open_group": 6835,
  "preview_original": "Conv X"
}
```

### Exclude single — `conversion_condition = "1"` (STRING)

**Loại trừ** friend đã access conversion đã chọn.

```json
{
  "type": "conversion",
  "active": true,
  "conversion_search": "456",
  "conversion_condition": "1",
  "open_group": 6835,
  "preview_original": "Conv X"
}
```

### Multiple conversions (CSV)

Multiple conversion **được phép khác category**. Friend match nếu đã access **TẤT CẢ** các conversion đã chọn.

```json
{
  "type": "conversion",
  "active": true,
  "conversion_search": "1189,1190",
  "conversion_condition": 0,
  "open_group": 6834,
  "preview_original": "c2・c2 cop"
}
```

**Quy tắc resolve `open_group`:**

- (a) Single conversion → `open_group` = `category_id` của conversion đó.
- (b) Multiple cùng category → `open_group` = `category_id` chung.
- (c) Multiple KHÁC category → chọn **1 `category_id` khác 0 bất kỳ** trong số các conversion đã chọn (chọn cái nào
  cũng được). Nếu có ít nhất 1 conversion có category → `open_group` PHẢI khác 0 (ưu tiên category thật thay vì 0).
- (d) Tất cả conversion đều uncategorized (`category_id = 0`) → `open_group = 0`.

**Field rules:**
| Field | Type | Note |
|------------------------|-----------------|------------------------------------------------------------------------------------------|
| `active`               | bool | Always
`true`                                                                            |
| `conversion_search`    | string | `conversion.id` dạng STRING. Single: `"1180"`. Multiple: CSV `"1189,1190"` (no
spaces). |
| `conversion_condition` | int \| string | **INT `0`** = include / **STRING `"1"`** = exclude (type
mixing)                         |
| `open_group`           | int | `category.id` tham chiếu — resolve theo quy tắc (a)–(d) ở trên. Khác category ĐƯỢC
PHÉP.  |
| `preview_original`     | string | Tên conversion. Single: just name. Multiple: join names với `・` (Japanese
middot)        |

> **Type mixing**: include = INT 0, exclude = STRING "1" — đúng theo payload web frontend.
> **conversion_search luôn STRING** — kể cả 1 id cũng phải là `"1180"` không phải `1180`.

**ID resolution:**

- User đưa TÊN → gọi `list_conversions(bot_id)` resolve name → id, copy `name` vào `preview_original`, resolve
  `open_group` theo quy tắc (a)–(d).
- User đưa RAW ID → bỏ qua `list_conversions`; chỉ fill `conversion_search`, để `preview_original = ""` và
  `open_group = 0` — server validate ownership và tự enrich `preview_original` (join names) + `open_group` từ DB khi
  submit.
- User KHÔNG chỉ định conversion nào → DỪNG và hỏi lại; KHÔNG gọi list rồi fill toàn bộ ID.
