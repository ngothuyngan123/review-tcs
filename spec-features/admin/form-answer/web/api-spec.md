# FA-011 — API Spec: Tạo biểu mẫu「フォーム作成」

## Tổng quan Endpoints

| EP | Method | URL | Mô tả | Auth |
|----|--------|-----|-------|------|
| EP-01 | GET | `/basic/form-answer` | Trang danh sách form (index v3) | basic_access, is_expire |
| EP-02 | GET | `/basic/form-answer/edit/{id}` | Trang editor form v3 | basic_access, is_expire |
| EP-03 | GET | `/basic/form-answer/common-design-setting/{id}` | Trang cài đặt thiết kế chung | basic_access, is_expire |
| EP-04 | POST | `/basic/form-answer/store-v3` | Tạo form mới (v3) | basic_access, is_expire |
| EP-05 | POST | `/basic/form-answer/save-v3/{id}` | Lưu toàn bộ nội dung form (v3) | basic_access, is_expire |
| EP-06 | POST | `/basic/form-answer/update-other-settings/{id}` | Cập nhật cài đặt khác (各種設定) | basic_access, is_expire |
| EP-07 | POST | `/basic/form-answer/update-form-system/{id}` | Cập nhật thông tin hệ thống form (管理名, フォルダ) | basic_access, is_expire |
| EP-08 | POST | `/basic/form-answer/update-settings-style/{id}` | Cập nhật cài đặt giao diện | basic_access, is_expire |
| EP-09 | POST | `/basic/form-answer/{id}/save-setting-common` | Lưu cài đặt thiết kế chung (共通デザイン設定) | basic_access, is_expire |
| EP-10 | GET | `/basic/form-answer/{id}` | Lấy dữ liệu chi tiết form (JSON API) | basic_access, is_expire |
| EP-11 | GET | `/basic/form-answer/{id}/get-form-page` | Lấy danh sách trang của form | basic_access, is_expire |
| EP-12 | GET | `/basic/form-answer/{id}/get-form-of-page/{pageId}` | Lấy danh sách item của 1 trang | basic_access, is_expire |
| EP-13 | GET | `/basic/form-answer/{id}/get-setting-common` | Lấy cài đặt thiết kế chung | basic_access, is_expire |
| EP-14 | GET | `/basic/form-answer/v3/result/{id}` | Trang xem kết quả trả lời (GET: render view, POST: lấy dữ liệu) | basic_access, is_expire |
| EP-15 | POST | `/basic/form-answer/v3/result/{id}` | Lấy dữ liệu danh sách câu trả lời (AJAX + phân trang) | basic_access, is_expire |
| EP-16 | GET | `/basic/form-answer/removed` | Trang danh sách form đã xóa | basic_access, is_expire |
| EP-17 | GET | `/basic/form-answer/link-google` | Trang kết nối Google Sheets | basic_access, is_expire |
| EP-18 | POST | `/ajax/get-list-form-answer-v3` | Lấy danh sách form + folder (AJAX) | basic_access, is_expire |
| EP-19 | GET | `/ajax/download-answer/{id}` | Tải CSV kết quả trả lời | basic_access, is_expire |
| EP-20 | GET | `/ajax/google-sheet-active` | Kiểm tra trạng thái kết nối Google Sheets | basic_access, is_expire |
| EP-21 | POST | `/ajax/change-public-form-answer` | Bật/tắt trạng thái công khai form | basic_access, is_expire |
| EP-22 | GET | `/basic/form-answer/form-render/{slug}/{line_id?}` | Hiển thị form công khai (v1 — legacy) | Không cần auth |
| EP-23 | GET | `/basic/form-answer/form-render-v3/{slug}/{line_id?}` | Hiển thị form công khai (v3) | Không cần auth |
| EP-24 | POST | `/basic/form-answer/form-render/store` | Submit câu trả lời form (v1 — legacy) | Không cần auth |
| EP-25 | POST | `/basic/form-answer/form-render-v3/store` | Submit câu trả lời form (v3) | Không cần auth |
| EP-26 | POST | `/ajax/form-answer/create-folder` | Tạo / đổi tên thư mục | basic_access, is_expire |
| EP-27 | POST | `/ajax/form-answer/delete-folder` | Xóa thư mục | basic_access, is_expire |
| EP-28 | POST | `/ajax/form-answer/move-folder` | Chuyển form sang thư mục khác | basic_access, is_expire |
| EP-29 | POST | `/ajax/form-answer/delete-list-formanswer` | Xóa nhiều form (bulk delete) | basic_access, is_expire |
| EP-30 | POST | `/ajax/sort-form-answer` | Sắp xếp thứ tự form | basic_access, is_expire |
| EP-31 | GET | `/ajax/get-form-answer-removed` | Lấy danh sách form đã xóa (AJAX) | check_login |
| EP-32 | POST | `/ajax/restore-form-answer/{id}` | Khôi phục form đã xóa | check_login |
| EP-33 | POST | `/basic/form-answer/v3/save-setting-remind` | Lưu cài đặt remind | basic_access, is_expire |
| EP-34 | POST | `/basic/form-answer/v3/get-list-step-remind` | Lấy danh sách step remind | basic_access, is_expire |
| EP-35 | POST | `/basic/form-answer/v3/save-point-setting` | Lưu cài đặt điểm chẩn đoán | basic_access, is_expire |
| EP-36 | POST | `/basic/form-answer/v3/saveMessageReply` | Lưu cài đặt tin nhắn sau submit | basic_access, is_expire |
| EP-37 | POST | `/basic/form-answer/v3/getSettingAction` | Lấy cài đặt action | basic_access, is_expire |
| EP-38 | PUT | `/basic/form-answer/v3/change-action-open/{form}` | Cập nhật action khi mở form | basic_access, is_expire |
| EP-39 | POST | `/basic/form-answer/{id}/add-page` | Thêm trang mới (form phân nhánh) | basic_access, is_expire |
| EP-40 | POST | `/basic/form-answer/{id}/sort-page` | Sắp xếp thứ tự trang | basic_access, is_expire |
| EP-41 | POST | `/basic/form-answer/quickSendForm` | Quick test — gửi form cho tester | basic_access, is_expire |
| EP-42 | GET | `/basic/form-answer/detail-result/{form_id}/{form_result_id}` | Chi tiết 1 câu trả lời | basic_access, is_expire |
| EP-43 | POST | `/basic/form-answer/diagnostic-content-settings/{id}` | Cập nhật cài đặt chẩn đoán | basic_access, is_expire |

---

## Chi tiết Endpoints

### EP-01: GET `/basic/form-answer` — Danh sách form

- **Controller**: `Basic\FormAnswerController@index_v3`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:184`
- **Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`
- **Logic**:
  - Lấy bot hiện tại từ `getBotId()`
  - Kiểm tra `flagNewFreePlan` (gói miễn phí giới hạn tính năng)
  - Kiểm tra `google_sheet_access_token` → nếu chưa có, tạo URL xác thực Google
  - Đọc cookie `folder_form_answer` để biết thư mục đang active
  - Lấy danh sách thư mục từ `form_answer_folder`
- **Response**: View `basic.form_answer.index_v3`
- **Mức độ tin cậy**: **Cao**

---

### EP-04: POST `/basic/form-answer/store-v3` — Tạo form mới (v3)

- **Controller**: `Basic\FormAnswerController@storeV3`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:6928`
- **Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`
- **Request body** (form-data / JSON):

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `form_name` | string | Tên form hiển thị với khách hàng (「フォーム名」) |
| `system_name` | string | Tên quản lý (「管理名」) |
| `folder_id` | int | ID thư mục (0 = 未分類) |
| `form_type` | int | Loại form: 1 = シンプル, 2 = 分岐 |
| `attr` | JSON array | Danh sách câu hỏi ban đầu (từ lựa chọn nhanh) |

- **Validation**:
  - Kiểm tra BackupHistory (đang backup → từ chối)
  - Kiểm tra plan miễn phí: nếu `flagNewFreePlan == 1` và `countForm >= 3` → từ chối
- **Logic**:
  1. Tạo `unique_key` random (6 ký tự, đệ quy đảm bảo unique)
  2. Insert `form_answer` với giá trị mặc định (màu `#08BF5A`, `reply_kind=0`, `reply_use_url=2`)
  3. Cập nhật `notify_setting.answer_form` nếu bot có cấu hình notify
  4. Gọi `formAnswerSettingCommonService->saveDefaultSettingCommon($form_id)` để tạo setting thiết kế mặc định
  5. Tạo `form_answer_page` đầu tiên (スタートページ)
  6. Nếu `attr` không rỗng: tạo `form_answer_details` cho từng câu hỏi ban đầu
- **Response** (JSON):

```json
{"status": true, "msg": "Successfully", "id": 123, "code": "Nm6wtb"}
```

- **Lỗi**:
  - `500`: backup đang chạy → `MESSAGE_NOTIFY_BACKUP`
  - `500`: vượt giới hạn plan miễn phí
  - `500`: exception → `"保存に失敗しました"`
- **Mức độ tin cậy**: **Cao**

---

### EP-05: POST `/basic/form-answer/save-v3/{id}` — Lưu nội dung form (v3)

- **Controller**: `Basic\FormAnswerController@saveV3`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:1242`
- **Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`
- **Request body**:

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `folder_id` | int | ID thư mục |
| `pages` | JSON array | Mảng các trang, mỗi trang chứa `attr` (page metadata + `forms` array) |
| `remindDeletedItem` | array | Danh sách remind item cần xóa |
| `tag_id`, `template_id`, `scenario_id` | int | Cài đặt action sau submit |

- **Logic** (DB transaction):
  1. Cập nhật `form_answer.group_id`, `using_old_version=0`
  2. Upsert `form_answer_setting`
  3. Với mỗi page:
     - Upsert `form_answer_page` (tên trang, button, CSS, loại trang tiếp theo)
     - Xử lý `next_page_setting` cho form phân nhánh (mapping option → pageId)
     - Với mỗi form item: upsert `form_answer_details` (type, title, rules, settings JSON)
     - Nếu `is_link_friend_info=1`: upsert `friend_information_setting` và `friend_info_option_selects`
  4. Xử lý remind deleted items
  5. Nếu có `google_sheet_access_token` và form chưa có `google_sheet_id` → tạo Google Spreadsheet mới
- **Response** (JSON):

```json
{
  "status": true,
  "msg": "Successfully",
  "id": 123,
  "code": "Nm6wtb",
  "formEditId": [...],
  "selectableEdit": {...}
}
```

- **Mức độ tin cậy**: **Cao**

---

### EP-06: POST `/basic/form-answer/update-other-settings/{id}` — Cài đặt khác (各種設定)

- **Controller**: `Basic\FormAnswerController@updateOtherSettings`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:7834`
- **Request body**: `data` (object) — chứa các trường như `option_show_timer`, `date_timer_count_down`, `time_timer_count_down`, `setting_page_confirm`, v.v.
- **Logic**:
  - Nếu timer thay đổi → cập nhật `form_answer_user_accept.is_update=1` (yêu cầu người dùng xác nhận lại)
  - Encode `setting_page_confirm` thành JSON
  - Nếu `option_show_timer=0` → clear date/time timer
  - Loại bỏ các trường nhạy cảm (`setting_common`, `pages`, `action_reply_id`, `system_name`...)
  - Update `form_answer`
- **Response**: `{"success": true}`
- **Mức độ tin cậy**: **Cao**

---

### EP-07: POST `/basic/form-answer/update-form-system/{id}` — Cập nhật thông tin hệ thống

- **Controller**: `Basic\FormAnswerController@updateFormSystem`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:7877`
- **Request body**: `data` (object) — `system_name`, `line_name`, `group_id`
- **Logic**: Map `system_name` → `name`, update `form_answer`
- **Response**: `{"success": true}`
- **Mức độ tin cậy**: **Cao**

---

### EP-09: POST `/basic/form-answer/{id}/save-setting-common` — Lưu thiết kế chung

- **Controller**: `Basic\FormAnswerController@saveSettingCommon`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:914`
- **Logic**: Gọi `FormAnswerSettingCommonService->saveFormAnswerSettingCommon($request)`, sau đó set `form_answer.using_old_version=0`
- **Response**: `{"success": true, "data": settingCommon_object}`
- **Mức độ tin cậy**: **Cao**

---

### EP-14/15: GET/POST `/basic/form-answer/v3/result/{id}` — Xem kết quả trả lời

- **Controller**: `Basic\FormAnswerController@showFormResultV3`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:4534`
- **GET**: Render view `basic.form_answer.form_result_v3`
- **POST (AJAX)**: Lấy dữ liệu phân trang câu trả lời

**POST Request params**:

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `date_start` | string | Ngày bắt đầu lọc (Y-m-d) |
| `date_end` | string | Ngày kết thúc lọc (Y-m-d) |
| `order` | string | Cột sắp xếp |
| `dir` | string | Hướng sắp xếp (asc/desc) |
| `paginate` | int | Số item/trang (mặc định 15) |

**POST Response** (JSON):

```json
{
  "success": true,
  "result": {
    "data": [
      {
        "id": 1,
        "created_at": "...",
        "line_id": 123,
        "data": [{type, name, value, ...}],
        "duration_time_reply": "00:09",
        "view_name": "田中太郎",
        "point": 2,
        "dataRemind": [...]
      }
    ],
    "current_page": 1,
    "last_page": 5,
    "total": 100
  },
  "date_start": "...",
  "date_end": "..."
}
```

- **Mức độ tin cậy**: **Cao**

---

### EP-18: POST `/ajax/get-list-form-answer-v3` — Danh sách form + folder

- **Controller**: `Basic\FormAnswerController@ajaxGetFormAnswerListV3`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:3462`
- **Request params**:

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `action` | string | `deleteItem` = xóa form; `sortFolder` = sắp xếp folder |
| `id` | int | ID form (khi action=deleteItem) |
| `folder_id` | int | Folder đang active |
| `keyword` | string | Từ khóa tìm kiếm theo tên |
| `field` | string | Cột sắp xếp |
| `order_by` | string | Hướng sắp xếp |
| `page` | int | Số trang (nếu có → paginate 20 items) |
| `type` | string | `sort` = lấy toàn bộ để sắp xếp |

- **Logic**:
  - `action=deleteItem`: soft-delete form, cascade xóa details/result/setting/page/setting_common/point_setting/user_accept, xóa event steps, reset rich menu items
  - `action=sortFolder`: cập nhật `position` trong `form_answer_folder`
  - Truy vấn danh sách form với JOIN `form_answer_setting`, theo folder đang active
  - Count folder với số form trong mỗi folder
- **Response** (JSON):

```json
{
  "status": true,
  "data": {
    "items": { paginated list of form_answer },
    "list_folder": [...],
    "count_default": 5,
    "folder_active": 0,
    "form_count": 10
  }
}
```

- **Mức độ tin cậy**: **Cao**

---

### EP-19: GET `/ajax/download-answer/{id}` — Tải CSV

- **Controller**: `Basic\FormAnswerController@downloadViewer`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:4099`
- **Response**: File CSV download
- **Mức độ tin cậy**: **Cao**

---

### EP-20: GET `/ajax/google-sheet-active` — Trạng thái Google Sheets

- **Controller**: `Basic\FormAnswerController@googleSheetActive`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:7184`
- **Logic**: Kiểm tra `bots.google_sheet_access_token` và `bots.google_sheet_status`
- **Response** (JSON):

```json
{"active": true, "re_connection": null}
```

- Nếu chưa active: `re_connection` chứa URL xác thực lại OAuth
- **Mức độ tin cậy**: **Cao**

---

### EP-21: POST `/ajax/change-public-form-answer` — Bật/tắt công khai

- **Controller**: `Basic\FormAnswerController@changePublicFormAnswer`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:3612`
- **Request**: `id` (int), `is_public` (int: 0|1)
- **Logic**: Update `form_answer.is_public`
- **Response**: `{"success": true}`
- **Mức độ tin cậy**: **Cao**

---

### EP-22/23: GET `/basic/form-answer/form-render[-v3]/{slug}` — Form công khai

- **Controller**: `Basic\FormAnswerController@renderForm` (v1) / `@renderFormV3` (v3)
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:1752` / `1985`
- **Middleware**: Không yêu cầu auth
- **URL params**: `{slug}` = unique_key của form; `{line_id?}` = encoded LINE user ID (Hashids)
- **Query params**: `mode=preview` để xem preview
- **Logic (v3 — qua FormAnswerService)**:
  - Tìm form theo `unique_key`
  - Kiểm tra hạn hợp đồng bot
  - Nếu có `line_id`: decode Hashids → tìm LineUser → kiểm tra đã trả lời chưa (`reply_kind`)
  - Lấy dữ liệu trang và form items, gắn giá trị bạn bè nếu `is_display_info_friend=1`
  - Khi `mode=preview` (v1): nếu form dùng v3 → redirect sang v3
- **Response**: View form công khai
- **Mức độ tin cậy**: **Cao**

---

### EP-24/25: POST `/basic/form-answer/form-render[-v3]/store` — Submit form

- **Controller**: `Basic\FormAnswerController@storeRenderForm` (v1) / `@storeRenderFormV3` (v3 qua FormAnswerService)
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:2145` / `3350`
- **Middleware**: Không yêu cầu auth
- **Request params**:

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `form_id` | int | ID form |
| `line_id` | string | Encoded LINE user ID (Hashids) |
| `user_id` | string | LINE user ID thô (nếu không có line_id) |
| `frm` | array | Mảng câu trả lời [{id, type, name, value}] |
| `date_open_form` | datetime | Thời điểm mở form (để tính thời gian trả lời) |

- **Logic**:
  1. Xác thực LINE user (decode Hashids hoặc tìm theo line_id)
  2. Kiểm tra `conversation` tồn tại (bạn bè của bot)
  3. Kiểm tra `reply_kind=1` và đã trả lời chưa → từ chối nếu vi phạm
  4. Xử lý từng câu trả lời:
     - Ghi giá trị vào `friend_information_value` nếu câu hỏi có `friend_info_id`
     - Xử lý tag (câu hỏi `in_tag=1`)
     - Xử lý datetime, file upload
  5. Insert `form_answer_result` với dữ liệu JSON
  6. Gửi action sau submit (`sendActionAfterReply`)
  7. Gửi tin nhắn phản hồi (`sendMessageReply`, `genMessage`)
  8. Gửi action điểm chẩn đoán nếu có
  9. Gửi mobile notify
- **Response** (JSON):

```json
{"status": true, "msg": "success"}
```

- **Lỗi**:
  - `"status": "false_friend"` → người dùng chưa là bạn bè của bot
  - `"status": "false_reply_kind"` → đã trả lời (giới hạn 1 lần)
- **Mức độ tin cậy**: **Cao**

---

### EP-31: GET `/ajax/get-form-answer-removed` — Danh sách form đã xóa

- **Controller**: `Basic\FormAnswerController@getFormAnswerRemoved`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:7307`
- **Middleware**: `check_login`, `check_remember_token`
- **Response**: Danh sách form đã soft-delete (paginated), kèm `username_del`
- **Mức độ tin cậy**: **Cao**

---

### EP-32: POST `/ajax/restore-form-answer/{id}` — Khôi phục form

- **Controller**: `Basic\FormAnswerController@restoreFormAnswer`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:7328`
- **Logic** (DB transaction):
  1. Kiểm tra giới hạn plan miễn phí (≤ 3 form trên free plan)
  2. Restore `form_answer`, `form_answer_details`, `form_answer_setting`, `form_answer_page`, `form_answer_point_setting`, `form_answer_setting_common`, `form_answer_user_accept`
  3. Restore `form_answer_folder` của form đó
- **Response**: `{"success": true}`
- **Mức độ tin cậy**: **Cao**

---

### EP-26: POST `/ajax/form-answer/create-folder` — Tạo/đổi tên thư mục

- **Controller**: `Basic\FormAnswerController@createFolder`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:5665`
- **Request**: `folder_name` (string), `folder_id` (int, optional)
- **Logic**: Nếu `folder_id` rỗng → insert mới, cập nhật position. Nếu có `folder_id` → update tên.
- **Response**: `{"success": true, "list_folder": [...]}`
- **Mức độ tin cậy**: **Cao**

---

### EP-29: POST `/ajax/form-answer/delete-list-formanswer` — Xóa nhiều form

- **Controller**: `Basic\FormAnswerController@deleteListFormanswer`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:6793`
- **Request**: `item_ids` (array of int)
- **Logic**: Cascade soft-delete, ghi `user_id_del`, reset rich menu items
- **Response**: `{"status": true, "message": "delete formanswer success"}`
- **Mức độ tin cậy**: **Cao**

---

### EP-41: POST `/basic/form-answer/quickSendForm` — Quick test

- **Controller**: `Basic\FormAnswerController@quickSendForm`
- **File**: `app/Http/Controllers/Basic/FormAnswerController.php:7221`
- **Request**: `formId` (int), `lineIds` (array)
- **Logic**: Gửi URL form qua LIFF cho tester account (botLineUserRepository)
- **Response**: `{"success": true, "msg": "..."}` hoặc lỗi nếu không có test account
- **Mức độ tin cậy**: **Cao**
