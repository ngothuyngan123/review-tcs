# Form/Survey Tools

## 1. list_forms

**Description:** Tool trả về danh sách Form/Survey kèm thông tin thống kê cơ bản. Hỗ trợ optional filter `names` (EXACT
match trên `name` HOẶC `title`, case-insensitive, trim whitespace) để tìm form theo tên đầy đủ thay vì paginate. Khi
truyền `names`, response có thêm `not_found_names` chứa các tên không match form nào.

**Tool:** `list_forms`

**Input:**
| Name | Type | Required | Description |
|--------|-----------------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| names | Array of String | No | Mảng tên form EXACT (match trên field `name` HOẶC `title` — form khớp 1 trong 2 cột sẽ được trả; case-insensitive, trim). Multiple = OR. Partial KHÔNG match. |
| page | Integer | No | Số trang (default: 1) |
| limit | Integer | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-----------------|-----------------|---------------------------|
| forms | Json Array | Array Object Form Summary |
| pagination | Json Object | Thông tin phân trang (`currentPage`, `limit`, `total`) |
| not_found_names | Array of String | (Chỉ trả khi truyền `names`) Các tên không match form nào |

**Sub Object Form Summary:**
| Name | Type | Description |
|-----------------|--------|-------------------------------------------------------|
| id | Long | ID của Form/Survey |
| name | String | Tên Form/Survey |
| title | String | Tiêu đề Form/Survey |
| form_type | String | Loại form (`basic`: cơ bản, `division`: phân chia; `unknown` nếu giá trị khác) |
| unique_key | String | Mã unique key của Form |
| count_user_reply| Int | Số lượt user đã trả lời |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)             |

**Sample Output:**

```json
{
  "forms": [
    {
      "id": 2001,
      "name": "Customer Feedback Survey",
      "title": "Khảo sát ý kiến khách hàng",
      "form_type": "basic",
      "unique_key": "FEEDBACK2026",
      "count_user_reply": 1800,
      "created_at": "2026-01-10 09:00:00"
    },
    {
      "id": 2002,
      "name": "Member Registration Form",
      "title": "Đăng ký thành viên",
      "form_type": "basic",
      "unique_key": "REGISTER2025",
      "count_user_reply": 6200,
      "created_at": "2025-08-15 10:00:00"
    }
  ],
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2
  }
}
```

**Sample Output (with `names: ["Đăng ký thành viên", "Typo Name"]`):**

```json
{
  "forms": [
    {
      "id": 2002,
      "name": "Member Registration Form",
      "title": "Đăng ký thành viên",
      "form_type": "basic",
      "unique_key": "REGISTER2025",
      "count_user_reply": 6200,
      "created_at": "2025-08-15 10:00:00"
    }
  ],
  "pagination": { "currentPage": 1, "limit": 100, "total": 1 },
  "not_found_names": ["Typo Name"]
}
```

---

## 2. get_form_detail

**Description:** Tool trả về chi tiết đầy đủ của nhiều Form/Survey bao gồm cấu hình field theo trang, action và thống kê

**Tool:** `get_form_detail`

**Input:**
| Name | Type | Required | Description |
|---------|------|----------|-------------------------------|
| form_ids | String | Yes | Danh sách ID Form/Survey cách nhau bằng dấu phẩy, tối đa 100. Trùng sẽ bị bỏ qua. Ví dụ: "1,2,3" |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |

**Output** (Array — mỗi phần tử là một Form Detail):
| Name | Type | Description |
|--------------------|------------|---------------------------------------------|
| id | Long | ID của Form/Survey |
| name | String | Tên Form/Survey |
| title | String | Tiêu đề Form/Survey |
| description | String | Mô tả Form/Survey |
| form_type | String | Loại form (`basic`: cơ bản, `division`: phân chia; `unknown` nếu giá trị khác) |
| folder_id | Long | Folder chứa form (= `create_form_survey.folder_id`; 0 = ngoài folder). Vắng nếu null |
| unique_key | String | Mã unique key của Form |
| count_user_reply | Int | Số lượt user đã trả lời |
| actions_on_open | Json Array | Danh sách action khi mở form — Array Sub Object Action ([] nếu không có) |
| actions_on_reply | Json Array | Danh sách action khi submit form — Array Sub Object Action. Nếu form có message reply success, cuối mảng có thêm 1 phần tử `type: "text"` với `content` = nội dung message đó (`id`/`action_id` = null) |
| message_action | Json Object | **Reverse-map shape `UPDATE_MESSAGE_ACTION`** (verify). Keys (NON_NULL): `reply_message`, `use_reply_message`, `send_qa_copy`, `reply_frequency`(ONCE/EVERY_TIME), `reply_action_id`, `open_frequency`, `open_action_id`, `reminders[]`. Reminder lưu **theo form** nên trả list step phẳng (không gộp theo field_id): mỗi step `{id, timing_type(DAYS_BEFORE/HOURS_BEFORE), days_before, send_time, hours_before, minutes_before, message, action_id, use_filter}` |
| diagnostic | Json Object | **Reverse-map shape `UPDATE_DIAGNOSTIC`** (verify). Keys: `enabled`, `point_field_id`, `point_ranges[]` (`id`, `from_point`, `to_point`, `message`, `action_id`) |
| design | Json Object | **Reverse-map shape `UPDATE_DESIGN`** (verify) từ `form_answer_setting_common` + custom css/js. Sub-section: `header`, `heading`, `divider`, `question`, `button`, `css` (các `*_overwrite`/`apply_to_existing` write-only KHÔNG trả về) |
| settings | Json Object | **Reverse-map shape `UPDATE_SETTINGS`** (verify). Keys: `line_display_name`, `reply_limit`, `total_limit`, `not_public`, `confirm_page`, `after_submit`, `countdown`, `show_duration` |
| created_at | String | Ngày tạo (format: yyyy-MM-dd HH:mm:ss)      |
| pages | Json Array | Array Object Form Page (nhóm field theo trang) |

**Sub Object Action:**
| Name | Type | Description |
|-----------|-------------|------------------------------------------------------------------|
| id | Long | ID của action detail (null với phần tử text sinh từ message reply success) |
| action_id | Long | ID nhóm action chứa action detail này (null với phần tử text sinh từ message reply success) |
| type | String | Loại action: `template` / `text` / `richmenu` / `scenario` / `tag` / `bookmark` / `friend_info` / `handling_status` / `block` / `remind` / ... (giá trị khác được trả nguyên gốc) |
| content | String | Mô tả action dạng human-readable (tiếng Nhật), ví dụ: `タグ「VIP」をつける`, `テンプレート「Welcome」を送信` |
| data | Json Object | Raw data JSON của action (chỉ trả khi parse được — có thể vắng; cấu trúc phụ thuộc loại action) |

**Sub Object Form Page (from form_answer_page):**
| Name | Type | Description |
|--------------------|------------|---------------------------------------------|
| page_id | Long | ID của page |
| page_name | String | Tên page (ページ名, từ ADD_PAGE) — vắng nếu null |
| page_number | Int | Thứ tự page — vắng nếu null |
| button_submit_name | String | Text nút submit của page |
| image_header | String | URL ảnh header của page |
| button | Json Object | Thiết kế nút submit (shape giống thao tác UPDATE_BUTTON) — vắng nếu chưa cấu hình. Keys: `button_name`, `pattern`, `text_color`, `bg_color`, `font_weight`, `shadow` |
| next_page | Json Object | Điều hướng trang kế (shape giống thao tác SET_NEXT_PAGE) — vắng nếu không có. `mode`: `END`\|`PAGE`\|`BRANCH`; `PAGE` kèm `next_page_id`; `BRANCH` kèm `field_id` + `branches[]` (`option_label`, `next_page_id`) |
| fields | Json Array | Array Object Form Field |

**Sub Object Form Field (from form_answer_details):**
| Name | Type | Description |
|-------------|---------|----------------------------------------------------------|
| id | Long | ID của field |
| type | String | Loại field (text/email/phone/select/radio/checkbox/date) |
| name | String | Tên field (system)                                       |
| label | String | Label hiển thị |
| title | String | Tiêu đề field (vắng nếu không có)                        |
| help | String | Text hướng dẫn (vắng nếu không có)                       |
| rules | String | Validation rules |
| settings | String | Cấu hình field (JSON string)                             |
| position | Int | Thứ tự field trong page                                  |
| placeholder | String | Placeholder text (vắng nếu không có)                     |
| field | Json Object | **Reverse-map typed theo shape `FormSurveyField` của create/update_form_survey** — để kiểm chứng (verify) dữ liệu đã ghi. Chỉ chứa các key áp dụng cho `field_type` (NON_NULL): `field_type`, `label`, `help`, `placeholder`, `required`, `input_restriction`, `options[]`(+`point`/`end_date`/`end_time`), `display`, `record_mode`, `selection_limit`, `auto_add_other`, `file_type`, `link_friend_info`, `friend_info_id`, `default_date(_type)`, `record_time`, `terms`, `checkbox_text`, decorations (`content`/`image_url`/`video_url`/`html`/`sub_text`/`pattern`/`color`/`bg_color`/`text_color`/`font_*`/`text_align`/`width`), css classes. |

**Sample Output:**

```json
[
  {
  "id": 2001,
  "name": "Customer Feedback Survey",
  "title": "Khảo sát ý kiến khách hàng",
  "description": "Vui lòng cho chúng tôi biết ý kiến của bạn",
  "form_type": "basic",
  "unique_key": "FEEDBACK2026",
  "count_user_reply": 1800,
  "actions_on_open": [
    {
      "id": 101,
      "action_id": 55,
      "type": "tag",
      "content": "タグ「Opened Survey」をつける"
    }
  ],
  "actions_on_reply": [
    {
      "id": 102,
      "action_id": 56,
      "type": "template",
      "content": "テンプレート「Thank You Message」を送信"
    },
    {
      "id": 103,
      "action_id": 56,
      "type": "tag",
      "content": "タグ「Completed Survey」をつける"
    },
    {
      "id": null,
      "action_id": null,
      "type": "text",
      "content": "Cảm ơn bạn đã trả lời khảo sát!"
    }
  ],
  "created_at": "2026-01-10 09:00:00",
  "pages": [
    {
      "page_id": 301,
      "button_submit_name": "Gửi đánh giá",
      "image_header": "https://cdn.example.com/form/header.jpg",
      "fields": [
        {
          "id": 5001,
          "type": "radio",
          "name": "satisfaction",
          "label": "Bạn hài lòng với dịch vụ của chúng tôi không?",
          "rules": "required",
          "settings": "[\"Rất hài lòng\", \"Hài lòng\", \"Bình thường\", \"Không hài lòng\"]",
          "position": 1
        },
        {
          "id": 5002,
          "type": "text",
          "name": "feedback",
          "label": "Góp ý của bạn",
          "rules": null,
          "settings": null,
          "position": 2,
          "placeholder": "Nhập nội dung..."
        },
        {
          "id": 5003,
          "type": "email",
          "name": "email",
          "label": "Email liên hệ",
          "rules": "required|email",
          "settings": null,
          "position": 3,
          "placeholder": "example@email.com"
        }
      ]
    }
  ]
  }
]
```

---

## 3. get_form_responses

**Description:** Tool trả về danh sách câu trả lời của user cho form, có phân trang

**Tool:** `get_form_responses`

**Input:**
| Name | Type | Required | Description |
|-----------|--------|----------|------------------------------------------|
| form_id | Long | Yes | ID của Form/Survey |
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| page | Int | No | Số trang (default: 1)                    |
| limit | Int | No | Số lượng record mỗi trang (default: 100, max: 100) |

**Output:**
| Name | Type | Description |
|-------------|------------|--------------------------------------|
| form_id | Long | ID của Form/Survey |
| form_name | String | Tên Form/Survey |
| pagination | Json Object | Thông tin phân trang. LƯU Ý: `total` = số record trong trang hiện tại, KHÔNG phải tổng toàn bộ response của form |
| responses | Json Array | Array Object Form Response |

**Sub Object Form Response:**
| Name | Type | Description |
|----------------|------------|---------------------------------------------------|
| id | Long | ID của response |
| lmessage_friend_id | Long | ID nội bộ DB của friend (`line_user.id`) |
| line_friend_id | String | LINE UID thật (`"Uxxx"`) |
| line_name | String | Tên hiển thị trên LINE ("" nếu không resolve được) |
| answers | Json Array | Danh sách câu trả lời |
| duration | String | Thời gian trả lời (giây, dạng chuỗi)             |
| answered_at | String | Ngày giờ trả lời (format: yyyy-MM-dd HH:mm:ss)    |

**Sub Object Answer:**
| Name | Type | Description |
|----------|--------|--------------------|
| name | String | Tên field (system name) |
| type | String | Loại field (text/email/phone/select/radio/checkbox/date) |
| value | Object | Giá trị trả lời |

**Sample Output:**

```json
{
  "form_id": 2001,
  "form_name": "Customer Feedback Survey",
  "pagination": {
    "currentPage": 1,
    "limit": 100,
    "total": 2
  },
  "responses": [
    {
      "id": 90001,
      "lmessage_friend_id": 50001,
      "line_friend_id": "U1a2b3c4d5e6f7081920a1b2c3d4e5f60",
      "line_name": "Nguyen Van A",
      "answers": [
        {
          "name": "satisfaction",
          "type": "radio",
          "value": "Rất hài lòng"
        },
        {
          "name": "feedback",
          "type": "text",
          "value": "Dịch vụ rất tốt, nhân viên nhiệt tình"
        },
        {
          "name": "email",
          "type": "email",
          "value": "nguyenvana@email.com"
        }
      ],
      "duration": "125",
      "answered_at": "2026-02-10 15:30:00"
    },
    {
      "id": 90002,
      "lmessage_friend_id": 50002,
      "line_friend_id": "U2b3c4d5e6f708192a03b1c2d3e4f5061",
      "line_name": "Tran Thi B",
      "answers": [
        {
          "name": "satisfaction",
          "type": "radio",
          "value": "Hài lòng"
        },
        {
          "name": "feedback",
          "type": "text",
          "value": "Cần cải thiện thời gian giao hàng"
        },
        {
          "name": "email",
          "type": "email",
          "value": "tranthib@email.com"
        }
      ],
      "duration": "89",
      "answered_at": "2026-02-10 14:20:00"
    }
  ]
}
```

---

## 4. create_form_survey

**Description:** Tạo mới một Form/Survey (回答フォーム — form mà bạn bè điền qua public URL), tương ứng với màn hình
**「回答フォーム 新規作成」** trên web. Tool chỉ tạo "vỏ" form với các default giống web; câu hỏi/trang được thêm/sửa
sau bằng tool update. KHÔNG phải message template — muốn tạo message dạng card/carousel thì dùng `create_form_template`.

**Tool:** `create_form_survey`

**Input:**
| Name | Type | Required | Description |
|-----------|---------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| name | String | Yes | **管理名** (tên quản lý nội bộ, tối đa 50 ký tự) — hiển thị trong danh sách form của admin, **KHÔNG hiển thị cho người trả lời** (入力内容はお客様に表示されません) |
| title | String | Yes | **フォーム名** (tên form, tối đa 20 ký tự) — **hiển thị cho người trả lời** trên public form (入力内容がお客様に表示されます) |
| folder_id | Long | No | **フォルダ** — ID folder chứa form. Bỏ trống hoặc 0 = chưa phân loại (未分類, mặc định) |
| form_type | Integer | No | **タイプ選択** — loại form, **KHÔNG đổi được sau khi tạo** (あとから変更はできません): `1` = シンプルタイプ (đơn giản, form 1 trang — mặc định), `2` = 分岐タイプ (phân nhánh, trang trả lời rẽ nhánh theo nội dung câu trả lời) |

**Output:**
| Name | Type | Description |
|--------|------------|-------------|
| status | String/Int | Trạng thái xử lý từ backend |
| id | Long | ID của form vừa tạo (dùng cho các tool update) |
| code | String | Slug public URL của form — truy cập tại `form-render-v3/{code}` |

**Sample Input:**

```json
{
  "tool_name": "create_form_survey",
  "params": {
    "bot_id": "mj3Kzx",
    "name": "顧客アンケート管理",
    "title": "顧客満足度アンケート",
    "folder_id": 0,
    "form_type": 1
  }
}
```

**Sample Output:**

```json
{
  "status": 1,
  "id": 3050,
  "code": "aB3xY9"
}
```

---

## 5. update_form_survey

**Description:** Cập nhật một Form/Survey đã tạo (màn hình editor của web: フォーム編集 và các tab cấu hình). Payload
là **một mảng `items` các thao tác có `type`**, được **thực thi tuần tự theo thứ tự mảng**. Mỗi phần tử là 1 thao tác
(đặt ảnh tiêu đề, thêm/sửa/xóa field, sửa nút, quản lý page, thiết kế, cấu hình…) — phân biệt qua field `type`.
Field mới thêm được nối vào cuối page.

> Các `type` sẽ được bổ sung dần theo từng bước. Hiện tại đã định nghĩa: `HEADER_IMAGE`, `ADD_FIELD`,
> `UPDATE_FIELD`, `REMOVE_FIELD`, `UPDATE_BUTTON`, `ADD_PAGE`, `REMOVE_PAGE`, `SET_NEXT_PAGE`, `UPDATE_DESIGN`,
> `UPDATE_MESSAGE_ACTION`, `UPDATE_DIAGNOSTIC`, `UPDATE_SETTINGS`.

**Tool:** `update_form_survey`

**Input:**
| Name | Type | Required | Description |
|---------|----------------|----------|-------------|
| bot_id | String | Yes | Bot ID hash string lấy từ tool list_bots |
| form_id | Long | Yes | ID Form/Survey (từ list_forms hoặc id trả về của create_form_survey) |
| items | Array of Item | Yes | Danh sách item của form theo thứ tự hiển thị (xem **Sub Object Item**) |

**Sub Object Item:** mỗi item có 1 field chung `type` xác định loại, kèm các field riêng theo từng loại.

| Name | Type | Required | Description |
|------|---------------|----------|-------------|
| type | String (enum) | Yes | Loại item: `HEADER_IMAGE` (ảnh tiêu đề) / `ADD_FIELD` (thêm field) / `UPDATE_FIELD` (sửa field) / `REMOVE_FIELD` (xóa field) / `UPDATE_BUTTON` (sửa nút submit) / `ADD_PAGE` (thêm page) / `REMOVE_PAGE` (xóa page) / `SET_NEXT_PAGE` (điều hướng trang tiếp — 次のページ) / `UPDATE_DESIGN` (thiết kế chung — 共通デザイン設定) / `UPDATE_MESSAGE_ACTION` (メッセージ・アクション設定) / `UPDATE_DIAGNOSTIC` (診断コンテンツ) / `UPDATE_SETTINGS` (各種設定) |

---

### Item type: `HEADER_IMAGE` (ヘッダー画像 — ảnh tiêu đề)

Ảnh hiển thị trên cùng của page (tương ứng ô **「ヘッダー画像」** trong editor; mặc định 設定なし = chưa đặt). Ảnh đặt
**theo từng page** — lưu vào `form_answer_page.page_image`; đọc lại qua `get_form_detail` ở field `image_header`.

| Name | Type | Required | Description |
|-----------|--------|----------|-------------|
| type | String | Yes | Cố định `"HEADER_IMAGE"` |
| page_id | Long | No | ID page cần đặt ảnh (từ get_form_detail pages[].page_id). Bỏ trống = page đầu tiên |
| image_url | String | Yes | URL ảnh tiêu đề — dùng `download_url` trả về từ tool `get_file_params` (sau khi user upload ảnh qua MCP client) |

**Sample Input:**

```json
{
  "tool_name": "update_form_survey",
  "params": {
    "bot_id": "mj3Kzx",
    "form_id": 3050,
    "items": [
      {
        "type": "HEADER_IMAGE",
        "image_url": "https://media.example.com/upload/form/header_abc.png"
      }
    ]
  }
}
```

---

### Item type: `ADD_FIELD` (thêm field mới)

Thêm 1 field (câu hỏi hoặc trang trí) vào form — tương ứng modal **「項目を追加」** trên web. Field được nối vào
**cuối** page chỉ định.

| Name | Type | Required | Description |
|---------|--------|----------|-------------|
| type | String | Yes | Cố định `"ADD_FIELD"` |
| page_id | Long | No | ID page đích (từ `get_form_detail` pages[].page_id). Bỏ trống = page đầu tiên (スタートページ). Với form phân nhánh có nhiều page, chỉ định rõ page cần thêm |
| field | Object | Yes | Nội dung field (xem **Sub Object Field**) — KHÔNG có `field_id` |

### Item type: `UPDATE_FIELD` (sửa field có sẵn)

Sửa 1 field đang có trên form. Gửi **toàn bộ trạng thái mới** của field (các setting con như danh sách option bị
**ghi đè toàn bộ** theo payload — không phải diff).

| Name | Type | Required | Description |
|----------|--------|----------|-------------|
| type | String | Yes | Cố định `"UPDATE_FIELD"` |
| field_id | Long | Yes | ID field cần sửa (từ `get_form_detail` pages[].fields[].id) |
| field | Object | Yes | Trạng thái mới của field (xem **Sub Object Field**). `field_type` phải khớp loại hiện tại — không đổi được loại field |

### Item type: `REMOVE_FIELD` (xóa field)

Xóa 1 field khỏi form (soft delete — dữ liệu câu trả lời đã thu không mất).

| Name | Type | Required | Description |
|----------|--------|----------|-------------|
| type | String | Yes | Cố định `"REMOVE_FIELD"` |
| field_id | Long | Yes | ID field cần xóa (từ `get_form_detail` pages[].fields[].id) |

> ⚠️ Với form phân nhánh: nếu field bị xóa đang là **câu hỏi điều khiển phân nhánh** của page, cấu hình phân nhánh
> của page đó tự reset về "kết thúc form".

**Sample Input (thêm 2 field + sửa 1 field + xóa 1 field):**

```json
{
  "tool_name": "update_form_survey",
  "params": {
    "bot_id": "mj3Kzx",
    "form_id": 3050,
    "items": [
      {
        "type": "ADD_FIELD",
        "field": {
          "field_type": "NAME",
          "label": "お名前を入力してください",
          "required": true
        }
      },
      {
        "type": "ADD_FIELD",
        "field": {
          "field_type": "SELECT",
          "label": "ご興味のある商品は？",
          "required": true,
          "display": "radio",
          "record_mode": "tags",
          "options": [ { "label": "新商品" }, { "label": "キャンペーン" } ]
        }
      },
      {
        "type": "UPDATE_FIELD",
        "field_id": 5002,
        "field": {
          "field_type": "TEXT",
          "label": "ご意見をお聞かせください",
          "help": "任意でご記入ください",
          "required": false
        }
      },
      { "type": "REMOVE_FIELD", "field_id": 5003 }
    ]
  }
}
```

---

### Item type: `UPDATE_BUTTON` (sửa nút submit của page)

Sửa nút submit/chuyển trang ở cuối page — tương ứng khối **「ボタン」** trong editor (mặc định 回答する). Mỗi page
có 1 nút riêng.

| Name | Type | Required | Description |
|-------------|---------|----------|-------------|
| type | String | Yes | Cố định `"UPDATE_BUTTON"` |
| page_id | Long | No | ID page (từ get_form_detail pages[].page_id). Bỏ trống = page đầu tiên |
| button_name | String | Yes | **ボタンテキスト** — text hiển thị trên nút, **tối đa 30 ký tự**, bắt buộc. Default web: 回答する |
| pattern | Integer | No | **デザイン**: `1` (パターン① — nút nền đầy, default) / `2` (パターン②) |
| text_color | String | No | **文字色** `#RRGGBB` (default #5799DB) |
| bg_color | String | No | **背景色** `#RRGGBB` (default #EDF4FB) |
| font_weight | Integer | No | **文字の太さ**: `600` (đậm, default) / `300` (mảnh) |
| shadow | Boolean | No | **シャドウ** — đổ bóng nút. Default true |

```json
{ "type": "UPDATE_BUTTON", "button_name": "送信する", "pattern": 1, "text_color": "#FFFFFF", "bg_color": "#08BF5A" }
```

---

### Item type: `ADD_PAGE` (thêm page — form nhiều trang)

Thêm 1 page mới vào cuối form — tương ứng nút **「＋ページ追加」**. Dùng cho **分岐タイプ (form_type=2)**; form
シンプル chỉ có 1 page nên không dùng.

| Name | Type | Required | Description |
|-----------|--------|----------|-------------|
| type | String | Yes | Cố định `"ADD_PAGE"` |
| page_name | String | Yes | **ページ名** — tên page, **tối đa 10 ký tự** |

Hành vi (giống web):
- Page mới nối vào **cuối** (page_number = cuối + 1), 次のページ mặc định = **回答完了ページ** (kết thúc form).
- Nếu page cuối trước đó đang trỏ "回答完了ページ", nó tự chuyển sang trỏ tới page mới (nối chuỗi tuần tự).
- Tối đa **50 page**/form.
- Response nên trả `page_id` của page mới để dùng cho `ADD_FIELD` / `SET_NEXT_PAGE` tiếp theo.

```json
{ "type": "ADD_PAGE", "page_name": "ページ2" }
```

### Item type: `REMOVE_PAGE` (xóa page — form nhiều trang)

Xóa 1 page khỏi form kèm **toàn bộ field trong page đó**.

| Name | Type | Required | Description |
|---------|--------|----------|-------------|
| type | String | Yes | Cố định `"REMOVE_PAGE"` |
| page_id | Long | Yes | ID page cần xóa (từ get_form_detail pages[].page_id) |

Ràng buộc (giống web):
- **Page đầu tiên (スタートページ) không xóa được.**
- Các page khác đang điều hướng tới page bị xóa được tự sửa lại: đích phân nhánh theo câu trả lời → về 回答完了ページ;
  đích chuyển trang cố định → về 回答完了ページ.

```json
{ "type": "REMOVE_PAGE", "page_id": 302 }
```

---

### Item type: `SET_NEXT_PAGE` (điều hướng trang tiếp — 次のページ)

Cấu hình khối **「次のページ」** cuối mỗi page: sau khi bấm nút của page này thì đi đâu. Dùng cho **分岐タイプ**;
form シンプル luôn là 回答完了ページ.

| Name | Type | Required | Description |
|--------------|---------------|----------|-------------|
| type | String | Yes | Cố định `"SET_NEXT_PAGE"` |
| page_id | Long | No | ID page cần cấu hình. Bỏ trống = page đầu tiên |
| mode | String (enum) | Yes | `END` = 回答完了ページ (kết thúc form, default của page mới) / `PAGE` = chuyển tới 1 page cố định / `BRANCH` = phân nhánh theo câu trả lời |
| next_page_id | Long | No | **Bắt buộc khi mode=PAGE** — ID page đích |
| field_id | Long | No | **Bắt buộc khi mode=BRANCH** — ID câu hỏi điều khiển phân nhánh trên page này. Chỉ nhận câu hỏi **SELECT (単一選択, radio/dropdown) bắt buộc** |
| branches | Array | No | **Bắt buộc khi mode=BRANCH** — mảng `{option_label, next_page_id}`: mỗi lựa chọn của câu hỏi map tới 1 page đích. `next_page_id = 0` (hoặc null) = 回答完了ページ. Option không có trong mảng sẽ theo đích của phần tử đầu tiên |

Ràng buộc (giống web):
- `BRANCH` yêu cầu page có ít nhất 1 câu hỏi SELECT bắt buộc; CHECKBOX không phân nhánh được.
- `option_label` phải khớp label lựa chọn hiện tại của câu hỏi (server đối chiếu lại theo label khi lưu).
- Sau khi set BRANCH, câu hỏi `field_id` bị khóa: không đổi được required / không chuyển sang checkbox / xóa nó thì
  page reset về END.

```json
{
  "type": "SET_NEXT_PAGE",
  "page_id": 301,
  "mode": "BRANCH",
  "field_id": 5001,
  "branches": [
    { "option_label": "はい", "next_page_id": 302 },
    { "option_label": "いいえ", "next_page_id": 0 }
  ]
}
```

---

### Item type: `UPDATE_DESIGN` (thiết kế chung — 共通デザイン設定)

Cập nhật thiết kế chung của toàn form — tương ứng tab **共通デザイン設定** với 6 mục 設定項目. Ngữ nghĩa **PATCH
theo section**: chỉ section nào được truyền mới được cập nhật; field bỏ trống trong 1 section giữ giá trị hiện tại.
Áp dụng cho toàn form (không phân biệt page).

| Name | Type | Required | Description |
|----------|--------|----------|-------------|
| type | String | Yes | Cố định `"UPDATE_DESIGN"` |
| header | Object | No | Section **ヘッダー・背景** (xem bảng dưới) |
| heading | Object | No | Section **見出し** — thiết kế mặc định cho item HEADING |
| divider | Object | No | Section **区切り線** — thiết kế mặc định cho item DIVIDER |
| question | Object | No | Section **質問項目** — chữ câu hỏi + 補足 |
| button | Object | No | Section **ボタン** — thiết kế mặc định nút các page |
| css | Object | No | Section **CSS・JS設定** — CSS class + custom CSS/JS |

**Sub Object `header` (ヘッダー・背景):**
| Name | Type | Required | Description |
|--------------|---------|----------|-------------|
| image_url | String | No | **共通ヘッダー画像** — URL ảnh header chung (download_url từ get_file_params; web giới hạn ≤10MB). Page mới tạo sẽ lấy ảnh này làm mặc định; từng page có thể ghi đè bằng item `HEADER_IMAGE` |
| remove_image | Boolean | No | true = xóa ảnh header chung hiện tại |
| bg_color | String | No | **フォーム背景** — màu nền form `#RRGGBB` (default #FFFFFF) |

**Sub Object `heading` (見出し):**
| Name | Type | Required | Description |
|-------------------|---------|----------|-------------|
| pattern | Integer | No | **デザイン選択** `1`/`2`/`3` (default 1). Lưu ý: trên web chọn pattern sẽ tự đổi màu mặc định kèm theo — qua MCP hãy set màu tường minh |
| text_color | String | No | 文字色 `#RRGGBB` (default #FFFFFF) |
| bg_color | String | No | 背景色 (pattern 1) / 線色 (pattern 2,3) `#RRGGBB` (default #5799DB) |
| font_weight | Integer | No | `600` (đậm, default) / `300` (mảnh) |
| font_size | Integer | No | `24` (lớn, default của form mới) / `20` (vừa) / `16` (nhỏ) |
| text_align | String | No | `left` / `center` (default) / `right` |
| apply_to_existing | Boolean | No | **現在登録されているすべての見出しに、このデザインを適用（上書き）する** — true = ghi đè thiết kế này lên tất cả item HEADING đang có trên form. Default false |

**Sub Object `divider` (区切り線):**
| Name | Type | Required | Description |
|-------------------|---------|----------|-------------|
| pattern | Integer | No | **デザイン選択** `1` (nét liền) / `2` (nét đứt) / `3` (2 nét) (default 1) |
| color | String | No | **カラー設定** `#RRGGBB` (default #5799DB) |
| width | Integer | No | **線の長さ**: `350` (長い, default) / `250` (普通) / `150` (短い) |
| apply_to_existing | Boolean | No | true = ghi đè thiết kế này lên tất cả item DIVIDER đang có. Default false |

**Sub Object `question` (質問項目):** *(áp dụng chung cho mọi câu hỏi — không có toggle ghi đè)*
| Name | Type | Required | Description |
|-------------------|---------|----------|-------------|
| text_color | String | No | Màu chữ câu hỏi `#RRGGBB` (default #222222) |
| font_weight | Integer | No | `600` (default) / `300` |
| font_size | Integer | No | `18` / `16` (default) / `14` |
| help_color | String | No | Màu chữ 補足 `#RRGGBB` (default #222222) |
| help_font_weight | Integer | No | `600` / `300` (default) |
| help_font_size | Integer | No | `16` / `14` (default) / `12` |

**Sub Object `button` (ボタン):**
| Name | Type | Required | Description |
|-------------------|---------|----------|-------------|
| pattern | Integer | No | `1` (パターン①, default) / `2` (パターン②) |
| text_color | String | No | 文字色 `#RRGGBB` (default #5799DB) |
| bg_color | String | No | 背景色 `#RRGGBB` (default #EDF4FB) |
| font_weight | Integer | No | `600` (default) / `300` |
| shadow | Boolean | No | Đổ bóng. Default true |
| apply_to_existing | Boolean | No | true = ghi đè thiết kế này lên nút của **tất cả page** hiện có (kể cả nút trang xác nhận). Default false |

**Sub Object `css` (CSS・JS設定):**
| Name | Type | Required | Description |
|-------------------|---------|----------|-------------|
| heading_class | String | No | CSS class cho 見出し (title_class) |
| heading_sub_class | String | No | CSS class cho phụ đề 見出し (subtitle_class) |
| question_class | String | No | CSS class cho câu hỏi (question_class) |
| help_class | String | No | CSS class cho 補足 (subquestion_class) |
| dropdown_class | String | No | CSS class cho dropdown |
| radio_class | String | No | CSS class cho radio |
| checkbox_class | String | No | CSS class cho checkbox |
| divider_class | String | No | CSS class cho 区切り線 (line_class) |
| button_class | String | No | CSS class cho nút (button_class) |
| apply_to_existing | Boolean | No | true = áp các class trên vào tất cả item đang có (class_overwrite). Default false |
| custom_css | String | No | Custom CSS của form — áp vào public form |
| custom_js | String | No | Custom JS của form — áp vào public form |

```json
{
  "type": "UPDATE_DESIGN",
  "header": { "bg_color": "#F5F7FA", "image_url": "https://media.example.com/upload/form/common_header.png" },
  "divider": { "pattern": 2, "color": "#5799DB", "width": 350, "apply_to_existing": true },
  "question": { "text_color": "#222222", "font_size": 16 },
  "button": { "pattern": 1, "text_color": "#FFFFFF", "bg_color": "#08BF5A", "apply_to_existing": true }
}
```

---

### Item type: `UPDATE_MESSAGE_ACTION` (メッセージ・アクション設定)

Cập nhật tab **メッセージ・アクション設定** — message/action khi hoàn thành form, khi mở form, và リマインドメッセージ.
Ngữ nghĩa **PATCH**: chỉ field truyền lên mới được cập nhật.

| Name | Type | Required | Description |
|-------------------|---------|----------|-------------|
| type | String | Yes | Cố định `"UPDATE_MESSAGE_ACTION"` |
| reply_message | String | No | **回答完了時に送信するメッセージ** — message gửi cho friend ngay sau khi submit, **tối đa 5000 ký tự**. Hỗ trợ token `{name}` (tên hiển thị của friend) |
| use_reply_message | Boolean | No | Bật/tắt gửi message trên. Truyền reply_message mà bỏ trống field này = tự bật |
| send_qa_copy | Boolean | No | **質問と回答のコピーメッセージを送る** — gửi kèm bản copy toàn bộ câu hỏi + câu trả lời sau message trên. Default false |
| reply_frequency | String | No | **アクションの稼働回数** (khối hoàn thành): `ONCE` (1度のみ — chỉ chạy lần submit đầu) / `EVERY_TIME` (何度でも — chạy mọi lần) |
| reply_action_id | Long | No | **回答完了時アクション** — ID action chain (từ create_action) chạy khi friend submit. Truyền `0` = gỡ action |
| open_frequency | String | No | **アクションの稼働回数** (khối mở form): `ONCE` / `EVERY_TIME` |
| open_action_id | Long | No | **フォーム表示時アクション** — ID action chain chạy khi friend mở form. Truyền `0` = gỡ action |
| reminders | Array | No | **リマインドメッセージ** — cấu hình nhắc hẹn (xem bảng dưới). Step được lưu **theo form** (1 bộ step/form, không theo field) → mỗi phần tử REPLACE toàn bộ danh sách step của FORM. Chỉ gửi **1 phần tử** — gửi nhiều phần tử thì phần tử sau ghi đè phần tử trước |

**Sub Object Reminder** (1 phần tử = cấu hình cho 1 field REMINDER):
| Name | Type | Required | Description |
|----------|--------|----------|-------------|
| field_id | Long | Yes | ID field REMINDER trên form — chỉ dùng để **xác nhận** form có field REMINDER hợp lệ (step lưu theo form, không gắn riêng field này) |
| steps | Array | Yes | Danh sách step nhắc — **REPLACE toàn bộ** step hiện có của **form** (step không gửi sẽ bị xóa) |

**Sub Object Reminder Step:**
| Name | Type | Required | Description |
|----------------|---------|----------|-------------|
| id | Long | No | ID step khi sửa (bỏ trống = tạo mới) |
| timing_type | String | Yes | `DAYS_BEFORE` = 配信終了日の N日前 HH:mm に配信 / `HOURS_BEFORE` = 配信終了日の H時間M分前に配信 |
| days_before | Integer | No | Số ngày trước hạn (timing_type=DAYS_BEFORE) |
| send_time | String | No | Giờ gửi `HH:mm` (timing_type=DAYS_BEFORE) |
| hours_before | Integer | No | Số giờ trước hạn, 0–23 (timing_type=HOURS_BEFORE) |
| minutes_before | Integer | No | Số phút trước hạn, 0–59 (timing_type=HOURS_BEFORE). Tổng tối đa 23h59m |
| message | String | No | Nội dung nhắc, **tối đa 5000 ký tự** |
| action_id | Long | No | Action chain chạy khi tới giờ nhắc. **message hoặc action_id phải có ít nhất 1** |

> Lưu ý (theo cấu trúc DB web): reminder step được lưu **theo form** (1 bộ step/form) — `field_id` dùng để
> xác nhận field REMINDER hợp lệ; nếu form có nhiều field REMINDER thì chỉ gửi 1 phần tử `reminders`.
>
> **絞り込み (filter điều kiện gửi) của từng step**: response trả `results[].steps[]` (id của từng step đã lưu);
> dùng tool `update_filter` với `target='form_reminder'`, `target_id=<step id>` để đặt/thay filter cho step đó
> (`filter_and=[]` + `filter_or=[]` = xóa hết điều kiện → gửi cho tất cả).

```json
{
  "type": "UPDATE_MESSAGE_ACTION",
  "reply_message": "{name}様 \n\n回答を受け付けました。",
  "send_qa_copy": true,
  "reply_frequency": "ONCE",
  "reply_action_id": 810,
  "reminders": [
    {
      "field_id": 5010,
      "steps": [
        { "timing_type": "DAYS_BEFORE", "days_before": 1, "send_time": "10:00",
          "message": "明日が回答期限です。お忘れなく!" },
        { "timing_type": "HOURS_BEFORE", "hours_before": 3, "minutes_before": 0, "action_id": 811 }
      ]
    }
  ]
}
```

---

### Item type: `UPDATE_DIAGNOSTIC` (診断コンテンツ)

Cập nhật tab **診断コンテンツ** — chấm điểm câu hỏi DIAGNOSTIC và gửi kết quả theo dải điểm.

| Name | Type | Required | Description |
|----------------|---------|----------|-------------|
| type | String | Yes | Cố định `"UPDATE_DIAGNOSTIC"` |
| enabled | Boolean | No | Bật/tắt tính năng chẩn đoán. **Không tắt được khi form còn field DIAGNOSTIC** (web chặn) |
| point_field_id | Long | No | Friend info field **loại POINT** dùng lưu tổng điểm của friend (từ list_friend_info_fields) |
| point_ranges | Array | No | Dải điểm → phản hồi. **REPLACE toàn bộ** — dải không gửi sẽ bị xóa |

**Sub Object Point Range:**
| Name | Type | Required | Description |
|------------|---------|----------|-------------|
| id | Long | No | ID dải khi sửa (bỏ trống = tạo mới) |
| from_point | Integer | Yes | Điểm bắt đầu (bao gồm). Ràng buộc `from_point <= to_point`, **các dải không được chồng nhau** |
| to_point | Integer | Yes | Điểm kết thúc (bao gồm) |
| message | String | No | Message gửi khi tổng điểm rơi vào dải, **tối đa 5000 ký tự** |
| action_id | Long | No | Action chain chạy khi rơi vào dải. **message hoặc action_id phải có ít nhất 1** |

```json
{
  "type": "UPDATE_DIAGNOSTIC",
  "enabled": true,
  "point_field_id": 210,
  "point_ranges": [
    { "from_point": 0,  "to_point": 10, "message": "生活習慣の改善をおすすめします。" },
    { "from_point": 11, "to_point": 20, "message": "おおむね良好です!", "action_id": 812 }
  ]
}
```

---

### Item type: `UPDATE_SETTINGS` (各種設定)

Cập nhật tab **各種設定**. Ngữ nghĩa **PATCH theo khối**: chỉ khối truyền lên mới được cập nhật.

| Name | Type | Required | Description |
|-------------------|---------|----------|-------------|
| type | String | Yes | Cố định `"UPDATE_SETTINGS"` |
| line_display_name | String | No | **お客様に表示されるフォーム名 / フォーム名** — tên form hiển thị cho người trả lời trên màn hình talk LINE, **tối đa 20 ký tự** |
| system_name | String | No | **管理名** — tên quản lý nội bộ của form, **tối đa 50 ký tự** |
| line_talk_title | String | No | **LINEトーク画面表示 → タイトル** — tiêu đề link preview khi gửi URL form lên LINE talk, **tối đa 20 ký tự** |
| line_talk_description | String | No | **LINEトーク画面表示 → 説明** — mô tả link preview, **tối đa 50 ký tự** |
| reply_limit | Object | No | **回答制限** — giới hạn số lần trả lời mỗi friend |
| total_limit | Object | No | **回答数の上限** — giới hạn tổng số câu trả lời toàn form |
| not_public | Object | No | **非公開時の表示** — hiển thị khi form ở trạng thái không công khai (非公開) |
| confirm_page | Boolean | No | **回答確認ページ** — true = hiện trang xác nhận trước khi submit |
| after_submit | Object | No | **回答後ページ遷移設定** — trang sau khi submit |
| countdown | Object | No | **カウントダウンタイマー** |
| show_duration | Object | No | **回答時間表示** — đếm/hiển thị thời gian trả lời |

**Sub Object `reply_limit`:**
| Name | Type | Required | Description |
|----------------|---------|----------|-------------|
| enabled | Boolean | Yes | false = 何度でも (không giới hạn); true = giới hạn số lần |
| max_per_friend | Integer | No | Số lần trả lời tối đa mỗi friend (≥1) — bắt buộc khi enabled=true |
| over_display | String | No | Khi chạm giới hạn: `TEXT` (hiện message, default) / `URL` (chuyển trang) |
| message | String | No | Message khi chạm giới hạn, **tối đa 50 ký tự**. Default: あなたがこのフォームに回答できる上限に達しました。 |
| redirect_url | String | No | URL chuyển tới khi over_display=URL |

**Sub Object `total_limit`:**
| Name | Type | Required | Description |
|----------------|---------|----------|-------------|
| enabled | Boolean | Yes | true = giới hạn tổng số câu trả lời của cả form |
| max_total | Integer | No | Tổng số câu trả lời tối đa (≥1) — bắt buộc khi enabled=true |
| over_display | String | No | `TEXT` (default) / `URL` |
| message | String | No | Message khi đủ số lượng, **tối đa 50 ký tự** |
| redirect_url | String | No | URL chuyển tới khi over_display=URL |

**Sub Object `not_public`:**
| Name | Type | Required | Description |
|--------------|--------|----------|-------------|
| display | String | No | `TEXT` (hiện message, default) / `URL` (chuyển trang) |
| message | String | No | Message khi form非公開, **tối đa 50 ký tự**. Default: このフォームは回答を受け付けていません。 |
| redirect_url | String | No | URL chuyển tới khi display=URL |

**Sub Object `after_submit`:**
| Name | Type | Required | Description |
|--------------|--------|----------|-------------|
| mode | String | Yes | `RETURN_TO_TALK` = 回答後ページを表示せずにトーク画面に戻る (default của web) / `SHOW_PAGE` = hiện trang cảm ơn (kèm message) / `REDIRECT_URL` = chuyển tới URL chỉ định |
| message | String | No | Nội dung trang cảm ơn — dùng khi mode=SHOW_PAGE |
| redirect_url | String | No | URL đích — bắt buộc khi mode=REDIRECT_URL |

**Sub Object `countdown`:** (表示期限・カウントダウンタイマー — 3 tầng: 利用設定 → 期限設定 → タイマー設定)
| Name | Type | Required | Description |
|-----------------|---------|----------|-------------|
| enabled | Boolean | Yes | `false` = tắt; `true` = bật hạn hiển thị. **Lưu ý: đổi cấu hình timer khiến friend phải xác nhận lại form** |
| show_timer | Boolean | No | `false` (default) = chỉ đặt hạn (form tự khóa sau hạn, **không hiện đồng hồ**); `true` = hiện đồng hồ đếm ngược. Các field tạo kiểu timer bên dưới cần `show_timer=true` |
| deadline_type | String | No | Loại hạn: `DATE` (default — mốc ngày/giờ cố định) / `DURATION` (theo khoảng thời gian từ lúc mở form) / `ONE_TIME` (chỉ hiện 1 lần, không timer) |
| date | String | No | **[DATE]** Ngày đích `YYYY-MM-DD` — bắt buộc khi enabled=true & deadline_type=DATE |
| time | String | No | **[DATE]** Giờ đích `HH:mm` |
| duration_days | Integer | No | **[DURATION]** Số ngày từ lúc mở form — bắt buộc khi deadline_type=DURATION |
| duration_mode | String | No | **[DURATION]** `OFFSET` (kết thúc sau N ngày + H giờ M phút — dùng duration_hours/minutes) / `CLOCK` (kết thúc tại giờ đồng hồ ngày cuối — dùng duration_end_time). Default OFFSET |
| duration_hours | Integer | No | **[DURATION/OFFSET]** Số giờ 0–23 cộng thêm |
| duration_minutes | Integer | No | **[DURATION/OFFSET]** Số phút 0–59 cộng thêm |
| duration_end_time | String | No | **[DURATION/CLOCK]** Giờ kết thúc `HH:mm` ở ngày cuối |
| expired_message | String | No | Message khi hết giờ |
| expired_display | String | No | `TEXT` (default) / `URL` |
| expired_url | String | No | URL chuyển tới khi hết giờ (expired_display=URL) |
| timer_label | String | No | **[show_timer=true]** Nhãn timer (タイマー文言, vd 終了まであと). **Dùng chung cột `title_timer` với `show_duration.display_text` — set cái này đè cái kia** |
| pin_top | Boolean | No | **[show_timer=true]** `true` (default) = ghim timer ở đầu trang |
| precision | String | No | **[show_timer=true]** Độ chính xác: `CENTISECOND` (0.01s) / `SECOND` / `MINUTE`. Default CENTISECOND |
| text_color | String | No | **[show_timer=true]** Màu chữ timer `#RRGGBB` |
| bg_color | String | No | **[show_timer=true]** Màu nền timer `#RRGGBB` |

**Sub Object `show_duration`:**
| Name | Type | Required | Description |
|--------------|---------|----------|-------------|
| enabled | Boolean | Yes | Bật/tắt hiển thị thời gian trả lời cho người trả lời |
| display_text | String | No | Text hiển thị kèm, **tối đa 50 ký tự** — bắt buộc khi enabled=true. **Dùng chung cột `title_timer` với `countdown.timer_label` — set cái này đè cái kia** |

```json
{
  "type": "UPDATE_SETTINGS",
  "line_display_name": "満足度アンケート",
  "reply_limit": { "enabled": true, "max_per_friend": 1, "over_display": "TEXT",
                   "message": "既にご回答いただいています。" },
  "not_public": { "display": "URL", "redirect_url": "https://example.com/closed" },
  "confirm_page": true,
  "after_submit": { "mode": "SHOW_PAGE", "message": "ご回答ありがとうございました。" },
  "countdown": { "enabled": true, "show_timer": true, "deadline_type": "DATE",
                 "date": "2026-10-31", "time": "23:59", "expired_message": "受付は終了しました。",
                 "timer_label": "終了まであと", "pin_top": true, "precision": "SECOND",
                 "text_color": "#FFFFFF", "bg_color": "#08BF5A" }
}
```

---

### Sub Object Field

Mỗi field có field chung `field_type` xác định loại, kèm các field riêng theo loại. 3 nhóm giống modal 項目を追加:

**Nhóm 1 — 基本項目 (câu hỏi cơ bản):**
| field_type | Web | DB (type/name/typeoption) |
|---|---|---|
| `TEXT` | 短文回答 | text / text_8 / text |
| `TEXTAREA` | 長文回答 | text / text_8 / textarea |
| `DATE` | 日付・時刻 | date_time / date_time / '' |
| `SELECT` | 単一選択 | select / select2_5 / radio\|select |
| `CHECKBOX` | 複数選択 | select / select2_5 / checkbox |
| `FILE_UPLOAD` | ファイルアップロード | friend_info_file / friend_info_file |
| `DIAGNOSTIC` | 診断コンテンツ | diagnostic_content / diagnostic_content / radio\|checkbox |
| `REMINDER` | リマインド | reminder / reminder |
| `POLICY` | 規約の同意 | policy / policy |

**Nhóm 2 — よく使われる項目 (preset, tự link friend info system field):**
| field_type | Web | DB | friend_info_id cố định |
|---|---|---|---|
| `NAME` | 名前 | text_new / text_new / name | -1 (tên hiển thị) |
| `EMAIL` | メールアドレス | text_new / text_new / email | -3 (email) |
| `ADDRESS` | 国内住所 | address / address | -11 (địa chỉ) |
| `BIRTHDAY` | 生年月日 | date_time / date_time / birthday | -4 (ngày sinh) |
| `PHONE` | 電話番号 | text_new / text_new / phone_number | -2 (số điện thoại) |
| `GENDER` | 性別 | select / gender / radio\|select | auto-create 性別 lần đầu (update giữ liên kết hiện có) |

**Nhóm 3 — 装飾 (trang trí, không phải câu hỏi):**
| field_type | Web | DB |
|---|---|---|
| `HEADING` | 見出し | description_1 / description_1 / description |
| `TEXT_BLOCK` | テキスト | text_new / text_new / text |
| `IMAGE` | 画像 | upload_file / upload_file |
| `VIDEO` | 動画埋め込み | video / video |
| `DIVIDER` | 区切り線 | line / line |
| `CUSTOM_HTML` | カスタムHTML | custom_html / custom_html |

#### Field chung (áp dụng cho nhóm câu hỏi 1 + 2)

| Name | Type | Required | Description |
|-------------|---------|----------|-------------|
| field_type | String | Yes | Loại field (enum ở trên) |
| label | String | Yes | **質問文** — nội dung câu hỏi hiển thị, **tối đa 50 ký tự**, bắt buộc với mọi câu hỏi nhóm 1 + 2 (nhóm trang trí có quy định riêng — xem từng loại) |
| help | String | No | **補足** — text bổ trợ dưới câu hỏi, **tối đa 200 ký tự** |
| placeholder | String | No | Placeholder, **tối đa 50 ký tự** — chỉ TEXT/TEXTAREA/NAME/EMAIL/PHONE |
| required | Boolean | No | **必須/任意** — bắt buộc trả lời. Default `true` (giống web khi thêm mới) |
| css_question_class | String | No | **CSSクラス指定・質問文** — CSS class áp cho phần 質問文 của field này (câu hỏi + HEADING) |
| css_help_class | String | No | **CSSクラス指定・質問文補足** — CSS class áp cho phần 補足 của field này (câu hỏi + HEADING) |
| css_options_class | String | No | **CSSクラス指定** slot thứ 3 theo loại: lựa chọn (SELECT/CHECKBOX/GENDER/DIAGNOSTIC), ô nhập địa chỉ (ADDRESS), hoặc đường kẻ (DIVIDER) |

#### Chi tiết từng loại — nhóm câu hỏi cơ bản

**`TEXT` (短文回答) / `TEXTAREA` (長文回答):**
| Name | Type | Required | Description |
|---|---|---|---|
| input_restriction | String | No | **入力制限** — chỉ `TEXT` (TEXTAREA không có): `email` / `tel` / `kana` / `numeric` / `date_format`. Bỏ trống = không giới hạn. `tel` → validate 10–12 chữ số |
| link_friend_info | Boolean | No | **友だち情報に回答を記録 (tự tạo field mới)** — true = tự tạo friend info field từ câu hỏi này. Default false |
| friend_info_id | Long | No | Ghi vào friend info field **có sẵn**: -1 (tên hiển thị) / -2 (SĐT) / -3 (email) hoặc ID dương loại 記述 (từ list_friend_info_fields). Loại trừ lẫn nhau với link_friend_info |

**`DATE` (日付・時刻):**
| Name | Type | Required | Description |
|---|---|---|---|
| default_date_type | Integer | No | **デフォルト日付**: `1` = ngày hiện tại (default), `2` = ngày chỉ định (kèm default_date), `0` = để trống |
| default_date | String | No | Ngày chỉ định `YYYY-MM-DD` — dùng khi default_date_type=2 |
| record_time | Boolean | No | **時間の記録** — true = thu thêm giờ (HH:mm) ngoài ngày. Default false. **Bật true thì tính năng lưu vào friend info bên dưới KHÔNG dùng được** (web ẩn khối 友だち情報に回答を記録 — giá trị ngày+giờ không lưu vào field friend info loại ngày được) |
| link_friend_info | Boolean | No | **友だち情報に回答を記録 (tự tạo field mới)** — true = tự tạo 1 friend info field mới loại ngày-giờ từ câu hỏi này rồi lưu câu trả lời vào đó. Chỉ dùng khi record_time=false. Default false. Loại trừ lẫn nhau với friend_info_id |
| friend_info_id | Long | No | Lưu câu trả lời vào friend info field **có sẵn**. Chỉ dùng khi record_time=false. Giá trị hợp lệ (theo dropdown web): `-5` = field hệ thống **生年月日 (Ngày sinh)** — lưu ý mã là -5, khác preset BIRTHDAY dùng -4; hoặc **ID dương** của field friend info **loại ngày-giờ (日時タイプ)** do user tự tạo (lấy từ list_friend_info_fields — field loại khác không chọn được). Loại trừ lẫn nhau với link_friend_info |

**`SELECT` (単一選択):**
| Name | Type | Required | Description |
|---|---|---|---|
| display | String | No | **表示方法**: `radio` (nút radio, default) / `dropdown` (danh sách thả xuống) |
| options | Array | Yes | Danh sách lựa chọn, **tối đa 100**, mỗi option `{label}` — label bắt buộc, **không được trùng nhau** |
| record_mode | String | No | **回答情報の連携**: `none` (default) / `tags` (mỗi option gắn với 1 tag theo label — tag **chưa có sẽ tự tạo** khi friend trả lời, không cần tạo trước) / `friend_info` (ghi vào friend info) |
| link_friend_info / friend_info_id | | No | Khi record_mode=friend_info: tự tạo mới hoặc chọn field có sẵn — **friend_info_id phải đúng kiểu** (SELECT → field kiểu **select hoặc text**; sai kiểu, không tồn tại hoặc của bot khác → lỗi) |
| auto_add_other | Boolean | No | **その他自動追加** — tự thêm lựa chọn "その他" (nhập tự do). Chỉ khi record_mode=none. Default true trên web |

**`CHECKBOX` (複数選択):**
| Name | Type | Required | Description |
|---|---|---|---|
| options | Array | Yes | Tối đa **100** option `{label}`, label bắt buộc, không trùng |
| selection_limit | Object | No | **選択数の制限** `{from, to}` — số lựa chọn tối thiểu/tối đa, ràng buộc `0 <= from < to` |
| record_mode | String | No | Chỉ `none` / `tags`. **KHÔNG hỗ trợ friend_info** (nhiều lựa chọn không map được vào 1 field). Không có auto_add_other |

**`FILE_UPLOAD` (ファイルアップロード):**
| Name | Type | Required | Description |
|---|---|---|---|
| file_type | Integer | No | **ファイルの指定**: `1` = ảnh (≤10MB, default), `2` = video (≤200MB, .mov), `3` = âm thanh, `4` = PDF (≤50MB), `5` = không chỉ định |
| link_friend_info / friend_info_id | | No | **Chỉ khi file_type = 1 (ảnh) hoặc 4 (PDF)** |

**`DIAGNOSTIC` (診断コンテンツ):**
| Name | Type | Required | Description |
|---|---|---|---|
| display | String | No | `radio` (đơn chọn, default) / `checkbox` (nhiều chọn) |
| options | Array | Yes | Tối đa **100** option `{label, point}` — `point` (số nguyên, cho phép âm) là điểm cộng khi chọn, bắt buộc mỗi option |
| link_friend_info / friend_info_id | | No | **Chỉ khi display=radio** (field loại selection). Checkbox không link được |

> Cấu hình dải điểm chẩn đoán (診断結果: from_point–to_point → message/action) dùng item type `UPDATE_DIAGNOSTIC`.

**`REMINDER` (リマインド):**
| Name | Type | Required | Description |
|---|---|---|---|
| options | Array | Yes | Tối đa **100** option `{label, end_date, end_time}` — mỗi option là 1 mốc nhắc: label bắt buộc; `end_date` (YYYY-MM-DD, ≥ hôm nay) + `end_time` (HH:mm) = hạn đăng ký. **Sau khi save không đổi được date/time của option** |

> Nội dung message nhắc cấu hình bằng item type `UPDATE_MESSAGE_ACTION` (mục `reminders`).

**`POLICY` (規約の同意):** *(không có toggle required — luôn phải đồng ý mới submit)*
| Name | Type | Required | Description |
|---|---|---|---|
| label | String | Yes | **案内文** (tiêu đề hiển thị), tối đa **50** ký tự. Default web: ご利用規約 |
| terms | String | Yes | **規約** — nội dung điều khoản, tối đa **20.000** ký tự |
| checkbox_text | String | Yes | **チェックボックスの案内文**, tối đa **50** ký tự. Default web: 規約に同意します |

#### Chi tiết từng loại — nhóm preset (よく使われる項目)

Cả 6 preset tự link vào friend info system field (bảng nhóm 2) — **KHÔNG truyền link_friend_info/friend_info_id**.
Field dùng chung: label (≤50), help (≤200), required.

| field_type | Field riêng | Ghi chú |
|---|---|---|
| `NAME` | placeholder (≤50), input_restriction | Luôn ghi vào tên hiển thị hệ thống (-1) |
| `EMAIL` | placeholder (≤50) | Validate định dạng email; ghi vào -3 |
| `PHONE` | placeholder (≤50) | Validate 10–12 chữ số; ghi vào -2 |
| `BIRTHDAY` | default_date_type / default_date | Như DATE nhưng chỉ ngày (không time); ghi vào -4 |
| `ADDRESS` | address_placeholders (object, optional) | 5 ô con: zip_code / province / district / township / building — chỉ sửa được placeholder từng ô; building luôn optional, 4 ô còn lại required theo `required` của field; ghi vào -11 |
| `GENDER` | display (radio\|dropdown), options (default 男性/女性) | **Tự liên kết** friend info (auto-create 性別 lần đầu; update giữ liên kết hiện có) — KHÔNG set record_mode / link_friend_info / friend_info_id / auto_add_other |

#### Chi tiết từng loại — nhóm trang trí (装飾, không phải câu hỏi)

Nhóm này không có required/help/placeholder (trừ ghi chú riêng), không link friend info.

**`HEADING` (見出し):**
| Name | Type | Required | Description |
|---|---|---|---|
| label | String | Yes | Text tiêu đề, tối đa **50** ký tự |
| sub_text | String | No | Text phụ dưới tiêu đề, tối đa **200** ký tự |
| pattern | Integer | No | Kiểu thiết kế `1`/`2`/`3` (default 1) |
| text_color | String | No | Màu chữ `#RRGGBB` (default #FFFFFF) |
| bg_color | String | No | Màu nền (pattern 1) / màu kẻ (pattern 2,3) `#RRGGBB` (default theo 共通デザイン設定 — form mới: #5799DB) |
| font_weight | Integer | No | `600` (đậm, default) / `300` (mảnh) |
| font_size | Integer | No | `24` (lớn, default) / `20` (vừa) / `16` (nhỏ) |
| text_align | String | No | `left` / `center` (default) / `right` |

**`TEXT_BLOCK` (テキスト):**
| Name | Type | Required | Description |
|---|---|---|---|
| content | String | Yes | Nội dung text/HTML tự do (web dùng rich-text editor) — không giới hạn độ dài |

**`IMAGE` (画像):**
| Name | Type | Required | Description |
|---|---|---|---|
| image_url | String | Yes | URL ảnh — dùng `download_url` từ `get_file_params`. Web giới hạn png/jpg ≤ **10MB**, ≤10000px (server tự resize về tối đa 2048px) |
| is_full_width | Boolean | No | Hiển thị full chiều ngang màn hình. Default false |

**`VIDEO` (動画埋め込み):**
| Name | Type | Required | Description |
|---|---|---|---|
| video_url | String | Yes | **Chỉ nhận URL YouTube hoặc Vimeo** (không nhận mã nhúng iframe) |
| is_full_width | Boolean | No | Hiển thị full chiều ngang. Default false |

**`DIVIDER` (区切り線):**
| Name | Type | Required | Description |
|---|---|---|---|
| pattern | Integer | No | Kiểu đường kẻ `1`/`2`/`3` (default 1) |
| color | String | No | Màu `#RRGGBB` (default theo 共通デザイン設定 — form mới: #5799DB) |
| width | Integer | No | Độ dài: `350` (dài, default) / `250` (vừa) / `150` (ngắn) |

**`CUSTOM_HTML` (カスタムHTML):**
| Name | Type | Required | Description |
|---|---|---|---|
| label | String | Yes | Tiêu đề, tối đa **50** ký tự |
| html | String | Yes | Mã HTML/CSS tự do — không giới hạn độ dài, render nguyên trạng trên public form |

---

### Sample đầy đủ theo từng field_type

Mỗi sample là 1 phần tử `ADD_FIELD` trong mảng `items` (với `UPDATE_FIELD` chỉ cần thêm `field_id` cạnh `field`).

**Nhóm câu hỏi cơ bản:**

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "TEXT", "label": "会社名を入力してください", "help": "正式名称でご記入ください",
    "placeholder": "株式会社〇〇", "required": true,
    "link_friend_info": true } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "TEXT", "label": "フリガナ", "required": true,
    "input_restriction": "kana",
    "friend_info_id": 120 } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "TEXTAREA", "label": "ご意見・ご要望", "help": "自由にご記入ください",
    "placeholder": "こちらに入力", "required": false } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "DATE", "label": "ご来店希望日時", "required": true,
    "default_date_type": 0, "record_time": true } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "DATE", "label": "お申し込み日", "required": false,
    "default_date_type": 1,
    "friend_info_id": 130 } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "SELECT", "label": "ご興味のある商品は？", "required": true,
    "display": "radio", "record_mode": "tags",
    "options": [ { "label": "新商品" }, { "label": "キャンペーン" } ] } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "SELECT", "label": "どこで知りましたか？", "required": false,
    "display": "dropdown", "record_mode": "none", "auto_add_other": true,
    "options": [ { "label": "SNS" }, { "label": "友人の紹介" }, { "label": "検索" } ] } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "CHECKBOX", "label": "興味のあるジャンルを選んでください（2〜3個）", "required": true,
    "selection_limit": { "from": 2, "to": 3 }, "record_mode": "none",
    "options": [ { "label": "美容" }, { "label": "健康" }, { "label": "グルメ" }, { "label": "旅行" } ] } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "FILE_UPLOAD", "label": "身分証明書をアップロードしてください", "required": true,
    "file_type": 1, "link_friend_info": true } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "DIAGNOSTIC", "label": "朝食は毎日食べますか？", "required": true, "display": "radio",
    "options": [
      { "label": "毎日食べる", "point": 10 },
      { "label": "時々食べる", "point": 5 },
      { "label": "食べない", "point": 0 } ] } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "REMINDER", "label": "説明会の回をお選びください", "required": true,
    "options": [
      { "label": "第1回（10/15 14:00）", "end_date": "2026-10-14", "end_time": "18:00" },
      { "label": "第2回（10/22 14:00）", "end_date": "2026-10-21", "end_time": "18:00" } ] } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "POLICY", "label": "ご利用規約",
    "terms": "第1条（目的）本規約は…",
    "checkbox_text": "規約に同意します" } }
```

**Nhóm preset (よく使われる項目):**

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "NAME", "label": "お名前を入力してください", "required": true, "placeholder": "山田 太郎" } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "EMAIL", "label": "メールアドレスを入力してください", "required": true,
    "placeholder": "example@mail.com" } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "PHONE", "label": "電話番号を入力してください", "required": true, "placeholder": "09012345678" } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "BIRTHDAY", "label": "生年月日をご入力ください", "required": true, "default_date_type": 0 } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "ADDRESS", "label": "住所を入力して下さい", "required": true,
    "address_placeholders": {
      "zip_code": "1000001", "province": "東京都", "district": "千代田区",
      "township": "千代田1-1", "building": "〇〇ビル101" } } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "GENDER", "label": "性別を選択してください", "required": true,
    "display": "radio" } }
```

**Nhóm trang trí (装飾):**

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "HEADING", "label": "お客様情報", "sub_text": "以下の項目をご入力ください",
    "pattern": 1, "text_color": "#FFFFFF", "bg_color": "#5799DB",
    "font_weight": 600, "font_size": 24, "text_align": "center" } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "TEXT_BLOCK",
    "content": "<p>キャンペーン期間: <b>10月1日〜10月31日</b></p>" } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "IMAGE",
    "image_url": "https://media.example.com/upload/form/banner.png", "is_full_width": true } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "VIDEO",
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "is_full_width": false } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "DIVIDER", "pattern": 1, "color": "#08BF5A", "width": 350 } }
```

```json
{ "type": "ADD_FIELD", "field": {
    "field_type": "CUSTOM_HTML", "label": "アクセスマップ",
    "html": "<div class=\"map\"><iframe src=\"https://maps.example.com/embed\"></iframe></div>" } }
```

### Ví dụ luồng hoàn chỉnh — dựng form phân nhánh (2 call)

`ADD_PAGE` trả `page_id` mới trong response, nên phân nhánh trỏ tới page mới cần **call thứ 2** (hoặc lấy page_id
qua `get_form_detail`).

**Call 1** — dựng page 1 + tạo page 2:

```json
{
  "tool_name": "update_form_survey",
  "params": {
    "bot_id": "mj3Kzx",
    "form_id": 3050,
    "items": [
      { "type": "HEADER_IMAGE", "image_url": "https://media.example.com/upload/form/header.png" },
      { "type": "ADD_FIELD", "field": {
          "field_type": "SELECT", "label": "当日の参加方法をお選びください", "required": true,
          "display": "radio", "record_mode": "none", "auto_add_other": false,
          "options": [ { "label": "会場参加" }, { "label": "オンライン参加" } ] } },
      { "type": "UPDATE_BUTTON", "button_name": "次へ" },
      { "type": "ADD_PAGE", "page_name": "会場案内" }
    ]
  }
}
```

**Call 2** — (giả sử page 1 = 301, page mới = 302, câu hỏi SELECT = 5001) thêm field vào page 2 + set phân nhánh:

```json
{
  "tool_name": "update_form_survey",
  "params": {
    "bot_id": "mj3Kzx",
    "form_id": 3050,
    "items": [
      { "type": "ADD_FIELD", "page_id": 302, "field": {
          "field_type": "TEXT", "label": "同伴者のお名前", "required": false } },
      { "type": "UPDATE_BUTTON", "page_id": 302, "button_name": "回答する" },
      { "type": "SET_NEXT_PAGE", "page_id": 301, "mode": "BRANCH", "field_id": 5001,
        "branches": [
          { "option_label": "会場参加", "next_page_id": 302 },
          { "option_label": "オンライン参加", "next_page_id": 0 } ] },
      { "type": "SET_NEXT_PAGE", "page_id": 302, "mode": "END" }
    ]
  }
}
```

---

### Bảng limit tổng hợp (theo web)

| Hạng mục | Limit |
|---|---|
| 管理名 (name) / フォーム名 (title) | ≤ 50 / ≤ 20 ký tự |
| 質問文 / label / 案内文 | ≤ 50 ký tự, bắt buộc |
| 補足 (help) | ≤ 200 ký tự |
| Placeholder | ≤ 50 ký tự |
| Option mỗi câu hỏi chọn | ≤ 100, label không trùng |
| Checkbox 選択数制限 | 0 ≤ from < to |
| 規約 (POLICY terms) | ≤ 20.000 ký tự |
| Ảnh (IMAGE / HEADER_IMAGE) | png/jpg ≤ 10MB |
| File upload của người trả lời | ảnh 10MB / video 200MB (.mov) / PDF 50MB |
| Số page mỗi form | ≤ 50 |
| Tên page | ≤ 10 ký tự |
| Text nút (button_name) | ≤ 30 ký tự, bắt buộc |
| Số form (gói free) | ≤ 3 (server từ chối) |

### Áp dụng cho form phân nhánh (分岐タイプ)

Tài liệu này áp dụng chung cho cả 2 loại form:

- **シンプルタイプ (form_type=1)**: form 1 page — mọi item thao tác trên page đầu, không cần `page_id`.
- **分岐タイプ (form_type=2)**: form nhiều page — dùng `page_id` (từ `get_form_detail` pages[].page_id) để chỉ định
  page thao tác. Ràng buộc riêng:
  - Page đầu tiên (スタートページ) **không xóa được**; tối đa **50 page**/form.
  - Câu hỏi điều khiển phân nhánh của 1 page chỉ có thể là **SELECT (単一選択, radio/dropdown) bắt buộc**.
    CHECKBOX không dùng để phân nhánh được.
  - Field đang được dùng làm câu hỏi phân nhánh: **không đổi được required**, không chuyển display sang checkbox;
    `REMOVE_FIELD` field đó → phân nhánh của page reset về "kết thúc form".
  - Quản lý page bằng `ADD_PAGE` / `REMOVE_PAGE`; cấu hình luồng phân nhánh (đi đâu sau mỗi page) bằng
    `SET_NEXT_PAGE` (mode END / PAGE / BRANCH).
