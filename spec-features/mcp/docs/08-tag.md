# Tag Tools

> **Lưu ý về folder:** Các tool folder riêng cho tag (`list_tag_folders`, `create_tag_folder`, `update_tag_folder`) đã
> được gộp vào bộ tool generic `create_folder` / `list_folders` / `update_folder` (dùng `type=tag`). Xem
> [28-folder.md](28-folder.md).

## 1. list_tags

**Description:** Tool liệt kê tag và tra cứu tag_id theo tên (read-only). Gọi tool này khi cần tag_id mà chỉ biết tên
tag. Truyền `names[]` để tra tên → id (exact match, case-insensitive); tên không match trả trong `not_found_names`.
Mỗi tag trả về id, name, số user đang mang tag, và thông tin giới hạn số user. Bỏ `names[]` để duyệt toàn bộ tag.

**Tool:** `list_tags`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|-----------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Mảng tên tag EXACT (case-insensitive, trim). Multiple = OR. Partial KHÔNG match. Ví dụ:
`["VIP Member", "Summer 2026"]` |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-----------------|-----------------|-------------------------------------------------------------------------------|
| tags | Json Array | Array Object Tag |
| pagination | Json Object | Thông tin phân trang |
| not_found_names | Array of String | (Chỉ trả khi truyền `names`) Các tên không match tag nào |

**Sub Object Tag:**
| Name | Type | Description |
|----------------|--------|--------------------------------------------------------------------------|
| id | Long | ID của Tag |
| name | String | Tên Tag |
| count_user_tag | Int | Số lượng user được gắn tag này |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |
| is_limit | String | Giới hạn số user: `"制限する"` (có giới hạn) hoặc `"制限しない"` (không) |
| limit | Int | Số user tối đa được gắn tag (0 nếu không đặt giới hạn) |

**Sub Object Pagination:**
| Name | Type | Description |
|-------------|------|---------------------------|
| currentPage | Int | Trang hiện tại |
| limit | Int | Số lượng record mỗi trang |
| total | Int | Tổng số tag match |

**Sample Output:**

```json
{
  "tags": [
    {
      "id": 101,
      "name": "VIP Member",
      "count_user_tag": 2500,
      "created_at": "2025-03-01 10:00:00",
      "is_limit": "制限する",
      "limit": 3000
    },
    {
      "id": 102,
      "name": "Summer 2026",
      "count_user_tag": 3500,
      "created_at": "2026-01-15 10:30:00",
      "is_limit": "制限しない",
      "limit": 0
    },
    {
      "id": 103,
      "name": "Promotion Interest",
      "count_user_tag": 8200,
      "created_at": "2025-06-20 09:00:00",
      "is_limit": "制限しない",
      "limit": 0
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

## 2. get_tag_friends

**Description:** Tool trả về danh sách friend được gắn tag, có phân trang

**Tool:** `get_tag_friends`

**Input:**
| Name | Type | Required | Description |
|--------|---------|----------|------------------------------------------|
| tag_id | Long | Yes | ID của Tag (lấy từ list_tags) |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|------------|-------------|-------------------------|
| tag_id | Long | ID của Tag |
| tag_name | String | Tên Tag |
| pagination | Json Object | Thông tin phân trang |
| friends | Json Array | Array Object Friend Tag |

**Sub Object Pagination:**
| Name | Type | Description |
|-------------|------|-----------------------------------------------|
| currentPage | Int | Trang hiện tại |
| limit | Int | Số lượng record mỗi trang |
| total | Int | Số friend trả về trong trang hiện tại |

**Sub Object Friend Tag:**
| Name | Type | Description |
|--------------|--------|--------------------------------------------|
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| line_name | String | Tên hiển thị trên LINE |
| added_at | String | Ngày gắn tag (format: yyyy-MM-dd HH:mm:ss) |

**Sample Output:**

```json
{
  "tag_id": 101,
  "tag_name": "VIP Member",
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 3
  },
  "friends": [
    {
      "lmessage_friend_id": 50001,
      "line_friend_id": "U1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6",
      "line_name": "Nguyen Van A",
      "added_at": "2026-02-10 14:30:00"
    },
    {
      "lmessage_friend_id": 50002,
      "line_friend_id": "U2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7",
      "line_name": "Tran Thi B",
      "added_at": "2026-02-09 10:15:00"
    },
    {
      "lmessage_friend_id": 50003,
      "line_friend_id": "U3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8",
      "line_name": "Le Van C",
      "added_at": "2026-02-08 16:45:00"
    }
  ]
}
```

---

## 3. create_tag

**Description:** Tool tạo tag cho bot — 2 chế độ, truyền đúng MỘT trong `name` / `names`:

1. **SINGLE** — `name`: tạo 1 tag, tùy chọn kèm folder, giới hạn số user, và action chain gắn qua `action_id` /
   `limit_action_id`.
2. **BULK** — `names` với 2+ phần tử: tạo nhiều tag đơn giản trong MỘT lần gọi, tất cả cùng một folder (mảng 1 phần tử
   được xử lý như `name`). ALL-OR-NOTHING: nếu BẤT KỲ tên nào đã tồn tại là tag active trong bot → cả batch bị từ chối,
   không insert một phần. 1–20 tên mỗi lần gọi; tên rỗng và tên trùng trong mảng bị từ chối trước. Các param
   action/limit KHÔNG được hỗ trợ ở chế độ bulk (giới hạn backend) — tạo tag đơn giản trước, rồi gắn chain từng cái qua
   `update_tag`.

`action_id` / `limit_action_id` link chain đã tạo bởi `create_action` theo THAM CHIẾU: tag lưu lại các step hiện tại
của chain lên CÙNG chain id, nên các sửa đổi sau này qua `update_action` sẽ áp dụng cho tag này (một chain có thể được
share bởi nhiều parent — sửa chain ảnh hưởng tất cả).

Tiền đề: tên folder → resolve thành folder_id qua `list_folders(type=tag)`; chain id lấy từ `create_action` (được
verify quyền sở hữu bot trước khi link).

**Tool:** `create_tag`

**Input:**
| Name | Type | Required | Description |
|-------------------|-----------------|----------|------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| name | String | No* | [SINGLE] Tên tag (管理名) — truyền đúng một trong `name`/`names`. Không rỗng, tối đa 50 ký
tự, không chứa \n/\r/\t, unique trong bot (case-insensitive) |
| names | Array of String | No* | [BULK] Mảng tên tag đơn giản (1–20). Tất cả cùng một `folder_id`. All-or-nothing khi
trùng tên tag đã có. Không kết hợp với `name` hoặc các param action/limit |
| folder_id | Integer | No | Folder ID (default 0 = 未分類 virtual folder, không có DB record). Resolve tên folder → ID
qua `list_folders(type=tag)` |
| repeat_action | Integer (0\|1) | No | 0 = action chỉ kích hoạt lần gắn tag đầu tiên (default), 1 = kích hoạt mỗi lần gắn |
| is_limit | Boolean | No | Bật giới hạn số user. Default false. Nếu true → `user_limit` phải là số nguyên dương |
| user_limit | Integer | No | Số user tối đa được gắn tag này. Bắt buộc khi is_limit=true |
| limit_action_mode | Integer (0\|1) | No | 0 = limit action kích hoạt 1 lần/user khi đạt giới hạn (default), 1 = mỗi lần |
| action_id | Long | No | [SINGLE] ID của action chain (từ create_action) chạy khi tag được gắn. Link theo THAM
CHIẾU — sửa chain qua update_action sẽ áp dụng cho tag này. Bỏ qua nếu tag không có action |
| limit_action_id | Long | No | [SINGLE] ID của action chain (từ create_action) chạy khi đạt giới hạn số user. Cùng ngữ
nghĩa tham chiếu với action_id. Chỉ dùng khi is_limit=true (ngược lại bị bỏ qua) |

**Validation (MCP layer, kiểm tra trước khi gọi LME):**

- Truyền đúng MỘT trong `name` / `names`
- Mỗi tên: không rỗng, tối đa 50 ký tự sau trim, không chứa \n/\r/\t, không trùng tag active đã có (case-insensitive)
- Nếu `is_limit=true` thì `user_limit` phải > 0
- Nếu `folder_id > 0` thì folder phải tồn tại (kind=0) và thuộc bot
- `action_id` / `limit_action_id` phải là số dương và là chain tồn tại thuộc bot (verify qua backend trước khi link)
- BULK: 1–20 tên, không có param action/limit nào được set

**Output:** (verify live 2026-09-22)

- SINGLE: `{ "result": "ok", "data": { "success": true, "tag_id": <Long> }, "error": null }` (`tag_id` được MCP layer
  bổ sung bằng cách tra DB theo tên nếu LME không trả về)
- BULK: envelope tương tự + `count` được MCP surface top-level:
  `{ "result": "ok", "data": { ... }, "error": null, "count": N }`

**Sample Input (SINGLE):**

```json
{
  "bot_id": "y2kWN2",
  "name": "VIP Member",
  "folder_id": 45,
  "is_limit": true,
  "user_limit": 3000,
  "action_id": 1234
}
```

**Sample Input (BULK):**

```json
{
  "bot_id": "y2kWN2",
  "names": ["春", "夏", "秋", "冬"],
  "folder_id": 45
}
```

---

## 4. get_tag_detail

**Description:** Tool trả về cấu hình đầy đủ của một tag, bao gồm action chain (`setting_actions`) và limit-action
chain (`setting_limit_actions`). `action_id` / `limit_action_id` trong response là ID của action CHAIN: để sửa các step
của chain dùng `update_action` (REPLACE-ALL chi tiết chain); để gắn lại / gỡ chain khỏi tag dùng `update_tag` với
`action_id` / `limit_action_id`. `update_tag` không còn nhận mảng action inline.

**Tool:** `get_tag_detail`

**Input:**
| Name | Type | Required | Description |
|--------|--------|----------|--------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| tag_id | Long | Yes | Tag ID (số nguyên dương). Tag phải thuộc bot và chưa bị xóa |

**Output:**

⚠️ Response lồng **2 lớp `data`** (verify live H06, 2026-09-21) — payload tag nằm ở `data.data.*`, KHÔNG phải `data.*`:

`{ status, data: { status, data: { id, name, bot_id, category_id, action_id, limit_action_id, is_limit, limit, is_2th_apply, count_user_tag, setting_actions: [...], setting_limit_actions: [...] } } }`

---

## 5. update_tag

**Description:** Tool cập nhật cấu hình tag hiện có (tên, folder, cài đặt giới hạn, action chain đã link). Gọi
`/ajax/save-tag` với `action=edit_tag` (chế độ edit của cùng endpoint với create_tag).

Chỉ gửi field cần đổi — field bỏ trống **giữ nguyên** giá trị hiện tại (endpoint ghi đè mọi setting nên MCP đọc lại tag
từ DB rồi gửi đủ). Muốn đưa về mặc định thì gửi tường minh: `folder_id=0` (未分類), `repeat_action=0`,
`limit_action_mode=0`, `is_limit=false`. Không có field nào để đổi → lỗi `Nothing to update`. (Đổi 2026-09-25 —
review H2: trước đây bỏ trống = reset về mặc định, vd chỉ đổi tên cũng làm tag về 未分類 và tắt giới hạn.)

Action chain được link theo ID (từ `create_action`): `action_id` — BỎ QUA (omit) = giữ nguyên chain hiện tại của tag;
`0` = gỡ chain khỏi tag (chain không bị xóa); `>0` = link chain đó theo THAM CHIẾU (tag lưu lại các step hiện tại của
chain lên CÙNG chain id — sửa đổi sau này qua `update_action` áp dụng cho tag này). `limit_action_id` hoạt động tương
tự cho limit chain và chỉ được giữ khi `is_limit=true` — set `is_limit=false` sẽ gỡ limit chain. Để thay đổi chính các
STEP, dùng `update_action` (thay đổi ảnh hưởng mọi parent share chain đó).

**Tool:** `update_tag`

**Input:**
| Name | Type | Required | Description |
|-------------------|----------------|----------|------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| tag_id | Long | Yes | Tag ID (số nguyên dương). Phải tồn tại và thuộc bot |
| name | String | No | Tên tag mới, không rỗng, tối đa 50 ký tự, không chứa \n/\r/\t. Unique trong bot. Bỏ trống = giữ tên hiện tại |
| folder_id | Integer | No | Bỏ trống = giữ folder; `0` = 未分類; `>0` = folder tag (kind=0) của bot |
| repeat_action | Integer (0\|1) | No | 0 = chỉ lần đầu, 1 = mỗi lần. Bỏ trống = giữ |
| is_limit | Boolean | No | Bỏ trống = giữ trạng thái giới hạn; `true` = bật (dùng `user_limit`, bỏ trống thì dùng số hiện tại); `false` = tắt + gỡ limit chain |
| user_limit | Integer | No | Số user tối đa (> 0, ≥ số user đang mang tag). Bỏ trống = giữ số hiện tại. Khi giới hạn đang tắt phải gửi kèm `is_limit=true` |
| limit_action_mode | Integer (0\|1) | No | 0 = 1 lần/user, 1 = mỗi lần. Bỏ trống = giữ |
| action_id | Long | No | Điều khiển link chain gắn tag: omit = giữ chain hiện tại; 0 = gỡ chain khỏi tag (chain
không bị xóa); >0 = link chain của create_action theo tham chiếu |
| limit_action_id | Long | No | Cùng ngữ nghĩa omit / 0 / >0 như action_id nhưng cho limit chain (chạy khi đạt giới hạn).
Chỉ được giữ khi is_limit=true — is_limit=false gỡ limit chain |

**Validation (MCP layer):**

- `tag_id` phải thuộc bot và chưa bị xóa
- `name` (nếu gửi): không rỗng, tối đa 50 ký tự, không chứa \n/\r/\t
- `repeat_action` / `limit_action_mode` (nếu gửi): 0 hoặc 1
- `user_limit` (nếu gửi): > 0 và không nhỏ hơn số user hiện đang mang tag; bật lại giới hạn đang tắt mà DB chưa có số
  (= 0) → lỗi, yêu cầu gửi `user_limit`
- Gửi `user_limit` khi giới hạn đang / sẽ tắt → lỗi (`is_limit=false` kèm `user_limit`, hoặc giới hạn đang tắt mà không
  gửi `is_limit=true`)
- Không có field nào để đổi → lỗi `Nothing to update`
- Nếu `folder_id > 0` thì folder phải tồn tại (kind=0) và thuộc bot
- Chain id được verify quyền sở hữu bot trước khi link

**Output:** `{ "result": "ok", "data": { "success": true, "tag_id": <Long> }, "error": null }` (verify live 2026-09-22)

**Sample Input:**

```json
{
  "bot_id": "y2kWN2",
  "tag_id": 101,
  "name": "VIP Member 2026",
  "folder_id": 45,
  "action_id": 0
}
```
