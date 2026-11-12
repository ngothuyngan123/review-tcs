# Status Chat Filter (broadcast filter)

Filter recipient của broadcast theo `status_chat` (対応ステータス) đang gắn cho friend.

> Khác với **action** `handling_status` (step trong action chain — gắn/bỏ status; DB wire lưu `compliant_status` —
> xem [20-handling-status.md](20-handling-status.md)). Filter này chỉ để **lọc recipient**, không thay đổi status.

**ID-resolution rule:** user đưa **TÊN** status → gọi [`list_handling_statuses`](20-handling-status.md) resolve name
→ `id`, fill `preview_original`. User đưa **RAW ID** → **skip** `list_handling_statuses`; chỉ fill
`status_chat_search`, để `preview_original=""` — server validate ownership và tự enrich `preview_original` từ DB lúc
submit.

---

## Schema

| Field                     | Type          | Note                                                             |
|---------------------------|---------------|------------------------------------------------------------------|
| `type`                    | string        | Hằng số `"status_chat"`                                          |
| `active`                  | bool          | Always `true`                                                    |
| `status_chat_search`      | array of int  | `status_chat.id` (từ `list_handling_statuses` khi resolve tên). OR-joined |
| `status_chat_filter_type` | int \| string | **INT `0`** = include / **STRING `"1"`** = exclude (type mixing) |
| `preview_original`        | string        | Single = `name_status`. Multi = các name join bằng `・` (middot). Raw ID → để `""` (server enrich) |

---

## Include — `status_chat_filter_type = 0` (INT)

Lọc friend **đang có gắn 1 trong các** status đã chọn.

```json
{
  "type": "status_chat",
  "active": true,
  "status_chat_search": [4975],
  "status_chat_filter_type": 0,
  "preview_original": "3"
}
```

## Exclude — `status_chat_filter_type = "1"` (STRING)

**Loại trừ** friend đang có gắn 1 trong các status đã chọn.

```json
{
  "type": "status_chat",
  "active": true,
  "status_chat_search": [4926],
  "status_chat_filter_type": "1",
  "preview_original": "1"
}
```

## Multiple statuses

```json
{
  "type": "status_chat",
  "active": true,
  "status_chat_search": [4578, 4579],
  "status_chat_filter_type": 0,
  "preview_original": "未対応・対応中"
}
```

> Multi: `preview_original` = các name **join bằng `・`** (middot, U+30FB) — KHÔNG phải dấu phẩy, KHÔNG phải khoảng
> trắng. Thứ tự phải khớp `status_chat_search`.

> **Type mixing**: include = INT `0`, exclude = STRING `"1"` — đúng theo payload web frontend.
