# CSV Manager Tools

## 1. list_csv_managements

**Description:** Tool trả về danh sách CSV Management kèm thông tin filter và link download

**Tool:** `list_csv_managements`

**Input:**
| Name  | Type    | Required | Description                                            |
|-------|---------|----------|--------------------------------------------------------|
| bot_id| String  | Yes      | Bot ID hash string lấy từ tool list_bots               |
| page  | Integer | No       | Số trang (default: 1)                                  |
| limit | Integer | No       | Số lượng record mỗi trang (default: 100, max: 100)  |

**Output:**
| Name           | Type        | Description                 |
|----------------|-------------|-----------------------------|
| csvManagements | Json Array  | Array Object CSV Management (lưu ý: key dạng camelCase) |
| pagination     | Json Object | Thông tin phân trang (currentPage, limit, total). Lưu ý: `total` = số record của trang hiện tại |

**Sub Object CSV Management:**
| Name | Type | Description |
|-----------------|------------|------------------------------------------------|
| id | Int | ID của CSV Management |
| name | String | Tên CSV Management |
| total_line_user | Int | Số lượng user trong CSV |
| filters | Json Array | Danh sách điều kiện filter (xem Sub Object Filter Item) |
| download_url | String | Link download file CSV |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss) |

**Sub Object Filter Item:**
| Name | Type | Description |
|-----------------|--------|------------------------------------------------------|
| id | Int | ID của filter |
| type | String | Loại filter (ví dụ: `tag`, `friend_info`) |
| operator | String | Toán tử: `include` / `exclude` (map từ giá trị DB `and` / `or`) |
| preview_content | String | Nội dung preview của điều kiện filter |

**Sample Output:**

```json
{
  "csvManagements": [
    {
      "id": 5001,
      "name": "VIP Members Export",
      "total_line_user": 2500,
      "filters": [
        { "id": 801, "type": "tag", "operator": "include", "preview_content": "VIP Member" },
        { "id": 802, "type": "tag", "operator": "include", "preview_content": "Premium" },
        { "id": 803, "type": "friend_info", "operator": "include", "preview_content": "Số điện thoại" },
        { "id": 804, "type": "friend_info", "operator": "include", "preview_content": "Email" }
      ],
      "download_url": "https://cdn.example.com/csv/vip_members_2026.csv",
      "created_at": "2026-02-01 10:00:00"
    },
    {
      "id": 5002,
      "name": "Monthly Active Users",
      "total_line_user": 8500,
      "filters": [
        { "id": 811, "type": "tag", "operator": "include", "preview_content": "Active User" },
        { "id": 812, "type": "friend_info", "operator": "include", "preview_content": "Email" },
        { "id": 813, "type": "friend_info", "operator": "include", "preview_content": "Ngày sinh" }
      ],
      "download_url": "https://cdn.example.com/csv/active_users_jan_2026.csv",
      "created_at": "2026-01-15 09:30:00"
    },
    {
      "id": 5003,
      "name": "Survey Respondents",
      "total_line_user": 1800,
      "filters": [
        { "id": 821, "type": "tag", "operator": "include", "preview_content": "Completed Survey" },
        { "id": 822, "type": "friend_info", "operator": "include", "preview_content": "Số điện thoại" },
        { "id": 823, "type": "friend_info", "operator": "include", "preview_content": "Email" }
      ],
      "download_url": "https://cdn.example.com/csv/survey_2025.csv",
      "created_at": "2025-12-20 14:00:00"
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

## 2. get_csv_management_detail

**Description:** Tool trả về chi tiết CSV Management bao gồm tên cột và dữ liệu CSV dạng mảng 2 chiều (tiết kiệm dung lượng). Dữ liệu được stream theo dòng, chỉ đọc các dòng thuộc trang hiện tại.

**Tool:** `get_csv_management_detail`

**Input:**
| Name   | Type    | Required | Description                                           |
|--------|---------|----------|-------------------------------------------------------|
| csv_id | String  | Yes      | ID của CSV Management (chuỗi số)                      |
| bot_id | String  | Yes      | Bot ID hash string (từ list_bots)                     |
| page   | Int     | No       | Số trang (default: 1)                                 |
| limit  | Int     | No       | Số lượng record mỗi trang (default: 100, tối đa: 100) |

**Output:**
| Name            | Type           | Description                                                      |
|-----------------|----------------|------------------------------------------------------------------|
| id              | Int            | ID của CSV Management                                            |
| name            | String         | Tên CSV Management                                               |
| total_line_user | Int            | Tổng số user trong CSV                                           |
| pagination      | Json Object    | Thông tin phân trang (currentPage, limit, total). `total` = tổng số dòng data của file CSV |
| filters         | Json Array     | Danh sách điều kiện filter (xem Sub Object Filter Item bên trên) |
| download_url    | String         | Link download file CSV                                           |
| created_at      | String         | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)                          |
| csv_columns     | Json Array     | Mảng tên các cột (lấy từ dòng 2 của file CSV, dòng 1 bị bỏ qua). ⚠️ Server tải `download_url` mà KHÔNG xác thực nội dung — nếu URL trỏ tới trang không hợp lệ (vd trang login), `csv_columns`/`csv_data` sẽ chứa HTML thô (vd `["<html lang=ja>"]`, verify live H12, 2026-09-21). Client nên kiểm tra dấu hiệu HTML trước khi dùng |
| csv_data        | Json 2D Array  | Mảng 2 chiều dữ liệu CSV của trang hiện tại (mỗi row là 1 mảng giá trị) |

**Sample Output:**

```json
{
  "id": 190,
  "name": "VIP Members Export",
  "total_line_user": 2500,
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2500
  },
  "filters": [
    { "id": 801, "type": "tag", "operator": "include", "preview_content": "VIP Member" },
    { "id": 802, "type": "friend_info", "operator": "include", "preview_content": "登録日が2024-05-15〜2024-07-19" }
  ],
  "download_url": "https://go.lmes.jp/msg_template/csv/29/export_190.csv",
  "created_at": "2025-09-11 16:20:23",
  "csv_columns": [
    "ユーザーID",
    "LINE表示名",
    "タグ_アンケート回答_エルメ利用状況",
    "タグ_エルグラム?配信済み"
  ],
  "csv_data": [
    ["U9dc1fa43ed1aaa3a83c951600dadba4a", "takahiro", "0", "1"],
    ["U52933aede3880e87a3a3b74b5f259f1a", "けん", "1", "0"],
    ["U2989156ad6ccc4667406029cfa17338b", "@@M@j", "1", "0"]
  ]
}
```
