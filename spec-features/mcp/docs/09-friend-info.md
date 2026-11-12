# Friend Info Tools

> **Lưu ý về folder:** Các tool folder riêng cho friend info (`list_friend_info_folders`, `create_friend_info_folder`,
> `update_friend_info_folder`) đã được gộp vào bộ tool generic `create_folder` / `list_folders` / `update_folder` (dùng
> `type=friend_info`). Xem [28-folder.md](28-folder.md).

## 1. list_friend_info_fields

**Description:** Tool trả về danh sách các trường thông tin của friend (Friend Information Setting) kèm số user có dữ
liệu. 9 field đầu tiên là các built-in field với ID âm (-1 システム表示名, -2 携帯電話, -3 メールアドレス, -4 生年月日,
-6 都道府県名, -7 郵便番号, -8 市区町村名, -9 町名/番地, -10 建物名・部屋番号); còn lại là custom field từ
friend_information_setting (ID dương). Hỗ trợ optional filter `titles` (EXACT match trên field `title`,
case-insensitive, trim whitespace) áp dụng cho cả built-in và custom fields. Khi truyền `titles`, response trả thêm
`not_found_titles` cho các title không match field nào.

**Tool:** `list_friend_info_fields`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|-----------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| titles | Array of String | No | Mảng tiêu đề field EXACT (case-insensitive, trim). Áp dụng cho cả built-in (システム表示名,
携帯電話, メールアドレス, 生年月日, 都道府県名, 郵便番号, 市区町村名, 町名/番地, 建物名・部屋番号) và custom fields.
Multiple = OR. Partial KHÔNG match. |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|------------------|-----------------|--------------------------------|
| fields | Json Array | Array Object Friend Info Field |
| pagination | Json Object | Thông tin phân trang (currentPage, limit, total) |
| not_found_titles | Array of String | (Chỉ trả khi truyền `titles`) Các title không match field nào |

**Sub Object Friend Info Field:**
| Name | Type | Description |
|----------------------|-------------|----------------------------------------------------------------------------------|
| id | Long | ID của field (âm = built-in, dương = custom) |
| encoded_id | String | (Chỉ trả cho built-in field) Slug token của LME dùng trong `[FRIEND_INFO_<slug>]`:
system_name, phone, email, birthday, province, zip_code, district, township, building. Custom field KHÔNG có key này —
dùng thẳng `id` số trong `[FRIEND_INFO_<id>]` |
| title | String | Tên hiển thị của field |
| type_data | String | Loại dữ liệu ("select", "input", "calendar", "image", "file", "point") |
| group_id | Int | ID folder chứa field (0 nếu 未分類 hoặc built-in). Dùng làm `group_open` khi tạo action
friend_info trong broadcast. |
| total_user_has_value | Int | Số lượng friend có dữ liệu ở field này |
| setting_value | Json Object | (Chỉ trả cho custom field có cấu hình) Cấu hình đã lưu: action_mode + danh sách
option/threshold hiện có — dùng để copy khi gọi update_friend_info_field |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss). `null` với built-in field |

**Sub Object Setting Value:**
| Name | Type | Description |
|-----------------|------------|--------------------------------------------------------------|
| action_mode | String | Chế độ kích hoạt action đã lưu ("1" = 一度のみ, "2" = 何度でも稼働) |
| setting_actions | Json Array | Danh sách option/threshold đã lưu (Array Object Setting Action) |

**Sub Object Setting Action:**
| Name | Type | Description |
|-----------|--------|---------------------------------------------------------------|
| action_id | String | ID action chain gắn với option này (null nếu không có action) |
| value | String | Giá trị option (text của select / threshold của point ...) |
| id | Long | ID của option (giữ nguyên khi update để không mất liên kết dữ liệu friend) |

**Sample Output:**

```json
{
  "fields": [
    {
      "id": -1,
      "encoded_id": "system_name",
      "title": "システム表示名",
      "type_data": "input",
      "group_id": 0,
      "total_user_has_value": 12500,
      "created_at": null
    },
    {
      "id": 201,
      "title": "Số điện thoại",
      "type_data": "input",
      "group_id": 12,
      "total_user_has_value": 12500,
      "created_at": "2025-01-10 09:00:00"
    },
    {
      "id": 204,
      "title": "Giới tính",
      "type_data": "select",
      "group_id": 15,
      "total_user_has_value": 11000,
      "setting_value": {
        "action_mode": "1",
        "setting_actions": [
          { "action_id": null, "value": "Nam", "id": 301 },
          { "action_id": "1234", "value": "Nữ", "id": 302 }
        ]
      },
      "created_at": "2025-02-15 10:30:00"
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

## 2. get_field_friends

**Description:** Tool trả về danh sách friend có dữ liệu ở field cụ thể, có phân trang. Chấp nhận cả ID dương (custom
field) lẫn ID âm cho built-in field (-1, -2, -3, -4, -6, -7, -8, -9, -10).

**Tool:** `get_field_friends`

**Input:**
| Name | Type | Required | Description |
|----------|---------|----------|-----------------------------------------------------------------------------------------------|
| field_id | Long | Yes | ID của Friend Info Field. Custom: ID dương từ list_friend_info_fields. Built-in: ID âm (-1
システム表示名, -2 携帯電話, -3 メールアドレス, -4 生年月日, -6 都道府県名, -7 郵便番号, -8 市区町村名, -9 町名/番地,
-10 建物名・部屋番号) |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-------------|-------------|------------------------------|
| field_id | Long | ID của Field |
| field_title | String | Tên hiển thị của Field |
| pagination | Json Object | Thông tin phân trang |
| friends | Json Array | Array Object Friend |

**Sub Object Pagination:**
| Name | Type | Description |
|-------------|------|-----------------------------|
| currentPage | Int | Trang hiện tại |
| limit | Int | Số lượng record mỗi trang |
| total | Int | Tổng số friend có dữ liệu |

**Sub Object Friend:**
| Name | Type | Description |
|-------------------|--------|---------------------------------|
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| line_name | String | Tên hiển thị trên LINE |
| friend_info_value | String | Giá trị dữ liệu của friend tại field này (đường dẫn media được prepend host) |

**Sample Output:**

```json
{
  "field_id": 201,
  "field_title": "Số điện thoại",
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 12500
  },
  "friends": [
    {
      "lmessage_friend_id": 50001,
      "line_friend_id": "U1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6",
      "line_name": "Nguyen Van A",
      "friend_info_value": "0901234567"
    },
    {
      "lmessage_friend_id": 50002,
      "line_friend_id": "U2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7",
      "line_name": "Tran Thi B",
      "friend_info_value": "0912345678"
    },
    {
      "lmessage_friend_id": 50003,
      "line_friend_id": "U3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8",
      "line_name": "Le Van C",
      "friend_info_value": "0923456789"
    }
  ]
}
```

---

## 3. create_friend_info_field

**Description:** Tool tạo mới một Friend Information field và trả về id của nó. Không cần gọi form/init trước — mọi
option và default đã được mô tả trong params. `type_data` chọn loại field: 1=select (danh sách chọn), 2=input (text tự
do), 3=calendar (ngày), 4=image, 5=PDF, 6=point (số). Với 4/5 tool chỉ tạo placeholder cho field — friend upload file
thực tế qua my-page. `setting_actions` bắt buộc (non-empty) với type_data 1 và 6, chấp nhận `[]` với 3, để rỗng/bỏ qua
với 2/4/5. Để chạy action chain khi friend nhập giá trị: tạo chain bằng `create_action` trước rồi tham chiếu qua
`setting_actions[].actionId` — entry tham chiếu tới chính chain đó, nên sửa đổi sau này qua `update_action` cũng áp
dụng ở đây; inline `detailsAction` KHÔNG được chấp nhận. `action_mode`: 1 = kích hoạt một lần (lần nhập giá trị đầu
tiên), 2 = kích hoạt mỗi lần giá trị thay đổi (type_data 1/3/6). Bot đang backup → HTTP 500 MESSAGE_NOTIFY_BACKUP.

**Tool:** `create_friend_info_field`

**Input:**
| Name | Type | Required | Description |
|-----------------|----------------------------------|----------|------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| title | String | Yes | Tiêu đề field, không rỗng, tối đa 20 ký tự |
| folder_id | Long | Yes | Folder ID (friend-info folder, từ `list_folders(type=friend_info)`). 0 = 未分類. Khác 0
phải tồn tại và thuộc bot |
| type_data | Integer | Yes | Loại field: 1=select, 2=input, 3=calendar, 4=image, 5=PDF, 6=point. Không thể thay đổi
sau khi tạo (update_friend_info_field từ chối giá trị khác) |
| setting_actions | Array of FriendInfoSettingAction | No | Bắt buộc (non-empty) khi type_data ∈ {1,6}; type_data=3 chấp
nhận `[]` (không có trigger hẹn giờ); với {2,4,5} để rỗng hoặc bỏ qua |
| action_mode | Integer | No | Chế độ kích hoạt action: 1 = 一度のみ (chỉ lần nhập giá trị đầu), 2 = 何度でも稼働 (mỗi
lần giá trị thay đổi). Áp dụng cho type_data ∈ {1,3,6} — truyền tường minh cho các loại này (bỏ qua sẽ lưu null) |

**Sub Object FriendInfoSettingAction (mỗi phần tử của setting_actions):**
| Name | Type | Description |
|----------------|---------|--------------------------------------------------------------------------------|
| value | String | [type 1] text của option (≤50 ký tự). [type 6] threshold dạng chuỗi số (vd "100") |
| id | Long | [type 1] id option hiện có (chỉ dùng khi update option đã tồn tại) |
| dayOffset | Integer | [type 3] số nguyên ≥ 0 — số ngày offset của rule nhắc |
| recurrence | Integer | [type 3] chu kỳ lặp (bắt buộc): 1 = 月日 (tháng-ngày) → chạy MỖI NĂM vào tháng/ngày đó; 2 = 年月日 (năm-tháng-ngày) → chạy MỘT LẦN |
| offsetDirection | Integer | [type 3] hướng offset (bắt buộc): 1 = 前 (N ngày TRƯỚC ngày mốc); 2 = 後 (N ngày SAU ngày mốc) |
| time | String | [type 3] giờ nhắc, HH:mm 24h (vd "09:00") |
| actionId | Long | Tùy chọn — id action chain từ create_action; cách DUY NHẤT để gắn chain (ngữ nghĩa tham
chiếu — sửa qua update_action cũng áp dụng). Bỏ qua nếu entry chỉ là label |
| detailsAction | Array | KHÔNG chấp nhận — tạo chain bằng create_action rồi tham chiếu qua actionId |

**Validation (MCP layer):**

- `title` bắt buộc, không rỗng, tối đa 20 ký tự
- `folder_id` phải ≥ 0; khác 0 phải là kind=12 folder thuộc bot
- `type_data` phải là một trong {1,2,3,4,5,6}
- `setting_actions` bắt buộc (non-empty) khi type_data ∈ {1,6}; `[]` OK với 3; rỗng/bỏ qua với {2,4,5}
- `action_mode` nếu truyền phải là 1 hoặc 2
- `setting_actions[].actionId` phải là số dương và là chain tồn tại (verify qua backend trước khi forward)
- `setting_actions[].detailsAction` (inline chain) bị từ chối

**Output:** `{ "result": "ok", "data": { "success": true, "id": <field_id> }, "error": null }` — `data.id` = ID của field (verify live 2026-09-22)

**Sample Input:**

```json
{
  "bot_id": "y2kWN2",
  "title": "Giới tính",
  "folder_id": 33,
  "type_data": 1,
  "setting_actions": [
    { "value": "Nam" },
    { "value": "Nữ", "actionId": 1234 }
  ],
  "action_mode": 1
}
```

---

## 4. update_friend_info_field

**Description:** Tool cập nhật Friend Information field hiện có, kiểu full-state: `setting_actions[]` thay thế TOÀN BỘ
tập đã lưu — entry hiện có bị bỏ sót sẽ bị xóa, vì vậy đọc trạng thái hiện tại trước (`list_friend_info_fields` trả về
`setting_value` với id, value và action_id của từng option), copy, sửa phần cần thay đổi, rồi gửi lại tập đầy đủ. Giữ
`id` của từng option hiện có để giá trị friend đã nhập vẫn liên kết đúng. `type_data` không thể thay đổi sau khi tạo —
muốn đổi loại phải xóa field và tạo mới. Built-in field (ID âm) không thể cập nhật. Action chain tham chiếu qua
`setting_actions[].actionId` (từ create_action); inline `detailsAction` không được chấp nhận. Bot đang backup → HTTP
500 MESSAGE_NOTIFY_BACKUP.

**Tool:** `update_friend_info_field`

**Input:**
| Name | Type | Required | Description |
|-----------------|----------------------------------|----------|------------------------------------------------------------------------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| field_id | Long | Yes | Field ID cần update (số nguyên dương, từ list_friend_info_fields). Built-in field (ID âm
như -4 生年月日) không thể update qua MCP |
| title | String | Yes | Tiêu đề field, không rỗng, tối đa 20 ký tự (gửi lại title hiện tại nếu không đổi) |
| folder_id | Long | Yes | Folder ID. 0 = 未分類. Khác 0 phải tồn tại và thuộc bot. Gửi lại group_id hiện tại nếu
không di chuyển |
| type_data | Integer | Yes | Loại field: 1=select, 2=input, 3=calendar, 4=image, 5=PDF, 6=point. Bắt buộc và bất biến
— gửi đúng loại hiện tại của field; giá trị khác bị từ chối |
| setting_actions | Array of FriendInfoSettingAction | No | REPLACE-ALL — thay thế toàn bộ tập đã lưu (entry bị bỏ sót
sẽ bị xóa). Bắt buộc (non-empty) khi type_data ∈ {1,6}; `[]` OK với 3; rỗng/bỏ qua với {2,4,5}. Include `id` của từng
option hiện có (từ setting_value của list_friend_info_fields) |
| action_mode | Integer | No | 1 = chỉ lần nhập đầu, 2 = mỗi lần thay đổi. Áp dụng cho type_data ∈ {1,3,6} — gửi lại
giá trị hiện tại nếu muốn giữ (bỏ qua sẽ lưu null) |

(Cấu trúc từng phần tử `setting_actions` giống bảng **Sub Object FriendInfoSettingAction** ở tool
`create_friend_info_field`. Với chain: set `actionId` = id từ create_action, hoặc `action_id` hiện có của entry để giữ
nguyên.)

**Validation (MCP layer):**

- `field_id` phải là số nguyên dương, tồn tại và thuộc bot
- `type_data` không được khác giá trị hiện tại của field
- `title` bắt buộc, không rỗng, tối đa 20 ký tự
- `folder_id` ≥ 0; khác 0 phải là kind=12 folder thuộc bot
- `setting_actions` bắt buộc (non-empty) khi type_data ∈ {1,6}
- `setting_actions[].actionId` phải là chain tồn tại; inline `detailsAction` bị từ chối
- `action_mode` nếu truyền phải là 1 hoặc 2

**Output:** `{ "result": "ok", "data": { "success": true, "id": <field_id> }, "error": null }` — `data.id` = ID của field (verify live 2026-09-22)

**Sample Input:**

```json
{
  "bot_id": "y2kWN2",
  "field_id": 204,
  "title": "Giới tính",
  "folder_id": 15,
  "type_data": 1,
  "setting_actions": [
    { "value": "Nam", "id": 301 },
    { "value": "Nữ", "id": 302, "actionId": 1234 },
    { "value": "Khác" }
  ],
  "action_mode": 2
}
```
