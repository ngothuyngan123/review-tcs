# [FA-015] Quản lý thông tin bạn bè — API Spec

## Tổng quan
- **Tính năng**: FA-015 — Quản lý thông tin bạn bè (「友だち情報管理」)
- **Controller chính**: `Basic\FriendInformationController`
- **File**: `app/Http/Controllers/Basic/FriendInformationController.php` (1485 dòng)
- **Middleware chung**: `web`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`
- **Xác thực**: Session-based (cookie `folder_info_friend` lưu folder đang chọn)

---

## Danh sách Endpoints

| Mã | Method | URL | Mô tả | Màn hình |
|----|--------|-----|-------|----------|
| EP-01 | GET | `/basic/friend-information` | Trang danh sách thông tin bạn bè | SCR-FRI-01 |
| EP-02 | GET | `/basic/friend-information/add` | Trang tạo mới thông tin bạn bè | SCR-FRI-02/03/04/05 |
| EP-03 | GET | `/basic/friend-information/{id}` | Trang chỉnh sửa thông tin bạn bè | SCR-FRI-02/03/04/05 |
| EP-04 | GET | `/basic/friend-information/copy/{id}` | Trang sao chép thông tin bạn bè | SCR-FRI-02/03/04/05 |
| EP-05 | GET | `/basic/friend-information/item/{id}` | Trang danh sách câu trả lời theo info | SCR-FRI-08/09 |
| EP-06 | POST | `/ajax/init-information` | AJAX: lấy dữ liệu danh sách + thao tác CRUD folder/item | SCR-FRI-01 |
| EP-07 | POST | `/basic/initDataInfo` | AJAX: lấy chi tiết 1 setting info (cho form edit) | SCR-FRI-02/03/04/05 |
| EP-08 | POST | `/basic/initDataItemInfo` | AJAX: lấy danh sách bạn bè theo info | SCR-FRI-08/09 |
| EP-09 | POST | `/basic/save-setting-info-friend` | Lưu tạo mới / cập nhật thông tin bạn bè | SCR-FRI-02/03/04/05 |
| EP-10 | POST | `/basic/copy-setting-info-friend` | Sao chép thông tin bạn bè | SCR-FRI-01 |
| EP-11 | POST | `/basic/deleteFriendInfo` | Xoá dữ liệu câu trả lời (friend info values) | SCR-FRI-08/09 |
| EP-12 | POST | `/basic/getFolder` | Lấy danh sách folder | SCR-FRI-01 |
| EP-13 | POST | `/basic/friend-info-export-csv` | Xuất CSV danh sách bạn bè theo info | SCR-FRI-08/09 |
| EP-14 | GET | `/basic/friend-info/download-csv` | Download file CSV đã export | SCR-FRI-08/09 |
| EP-15 | GET | `/basic/get-friend-info` | Lấy danh sách info theo type (text, select, datetime) | Dùng bởi components khác |

---

## Chi tiết từng Endpoint

### EP-01: GET `/basic/friend-information` — Trang danh sách
- **Controller**: `FriendInformationController@index` (dòng 37)
- **Route name**: `friendInformationList`
- **Mức độ tin cậy**: **Cao**

**Logic xử lý:**
1. Lấy `bot_id` từ session (`getBotId()`)
2. Đọc cookie `folder_info_friend` để lấy folder đang chọn
3. Kiểm tra folder tồn tại trong bảng `category` (kind = 12 = `information_friend`)
4. Nếu folder không hợp lệ → reset về folder 0 (未分類)
5. Trả về view `basic.friend_information.index` với `folderCookie`

**Response:** HTML view (server-side rendered)

---

### EP-02: GET `/basic/friend-information/add` — Trang tạo mới
- **Controller**: `FriendInformationController@addInfo` (dòng 57)
- **Route name**: `create.info_friend`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `folderId` | query | integer | Không | ID folder ban đầu, validate trong bảng `category` |

**Logic xử lý:**
1. Kiểm tra `folderId` hợp lệ trong `category` (kind = 12, is_deleted = 0)
2. Nếu hợp lệ → gán folder, ngược lại → folder = 0

**Response:** HTML view `basic.friend_information.create`

---

### EP-03: GET `/basic/friend-information/{id}` — Trang chỉnh sửa
- **Controller**: `FriendInformationController@editInfo` (dòng 77)
- **Route name**: `edit.info_friend`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | path | integer/string | Có | ID của friend information setting. Hỗ trợ ID đặc biệt: -6, -7, -8, -9, -10 (default address info) |

**Logic xử lý:**
1. Nếu `id` KHÔNG thuộc [-6,-7,-8,-9,-10]: tìm trong `friend_information_setting`, fallback sang `action_info_friend_default`
2. Nếu không tìm thấy → redirect về `/basic/friend_information`
3. Trả về view `basic.friend_information.create` với `id_setting`, `folderCookie` = group_id

---

### EP-04: GET `/basic/friend-information/copy/{id}` — Trang sao chép
- **Controller**: `FriendInformationController@copyInfo` (dòng 105)
- **Route name**: `copy.info_friend`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | path | integer | Có | ID setting cần copy |

**Response:** HTML view `basic.friend_information.create` với `id_copy`

---

### EP-05: GET `/basic/friend-information/item/{id}` — Trang danh sách câu trả lời
- **Controller**: `FriendInformationController@listFriendByInfo` (dòng 187)
- **Route name**: `item.info_friend`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | path | integer/string | Có | ID friend information setting |

**Response:** HTML view `basic.friend_information.friend_by_info` (dữ liệu load qua AJAX EP-08)

---

### EP-06: POST `/ajax/init-information` — AJAX: CRUD tổng hợp + load dữ liệu
- **Controller**: `FriendInformationController@ajaxInitInformation` (dòng 484)
- **Route name**: `ajaxInitInformation`
- **Mức độ tin cậy**: **Cao**

Endpoint đa năng — dùng parameter `action` để xác định thao tác.

**Request params chung:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `action` | body | string | Có | Loại thao tác (xem bảng dưới) |
| `group_id` | body | integer | Không | ID folder đang chọn (-1 = default info, -2 = address info, 0 = 未分類, >0 = custom folder) |
| `cross` | body | boolean | Không | Dùng cross analysis mode cho group_id = -1 |

**Các action hỗ trợ:**

| Action | Mô tả | Params bổ sung |
|--------|-------|----------------|
| `addAndEditGroup` | Tạo hoặc đổi tên folder | `id` (int, null nếu tạo mới), `group_name` (string) |
| `deleteGroup` | Xoá folder + toàn bộ info items bên trong | `group_id` (int) |
| `renameGroup` | Đổi tên folder | `group_id` (int), `group_name` (string) |
| `deleteItem` | Xoá 1 info setting | `item_id` (int) |
| `deleteItems` | Xoá nhiều info settings | `item_ids` (array of int) |
| `moveItem` | Chuyển items sang folder khác | `item_ids` (array of int), `folder_move_id` (int) |
| `sortItem` | Sắp xếp thứ tự items | `sort_ids` (string, comma-separated), `sort_position` (string, comma-separated) |
| `sortFolder` | Sắp xếp thứ tự folder | `sort_ids` (string, comma-separated), `sort_position` (string, comma-separated) |

**Response thành công (JSON):**
```json
{
  "status": true,
  "groups": [
    {
      "id": 1,
      "name": "基本情報",
      "position": 5,
      "count": 4
    }
  ],
  "items": [
    {
      "id": 123,
      "title": "Type Select_EDIT",
      "type_data": 1,
      "group_id": 0,
      "order": 10,
      "total_user_has_value": 2,
      "created_at": "2025-03-07 10:00:00",
      "setting_value": "{...}"
    }
  ],
  "group_open": 0,
  "count_default": 28,
  "items_default": []
}
```

**Lỗi có thể xảy ra:**
| HTTP | Mô tả | Điều kiện |
|------|-------|-----------|
| 500 | `MESSAGE_NOTIFY_BACKUP` | Bot đang trong quá trình backup (BackupHistory status 0 hoặc 1) |
| 200 | `{"status": false, "msg": "..."}` | Exception xảy ra |

---

### EP-07: POST `/basic/initDataInfo` — AJAX: chi tiết 1 info setting
- **Controller**: `FriendInformationController@initDataInfo` (dòng 118)
- **Route name**: `initDataInfo`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | body | integer/string | Có | ID info setting. Hỗ trợ [-6,-7,-8,-9,-10] cho default address fields |

**Response thành công (JSON):**
```json
{
  "status": true,
  "data": {
    "id": 123,
    "bot_id": 1,
    "title": "Test Select",
    "type_data": 1,
    "group_id": 0,
    "setting_value": "{...}",
    "setting_actions": {
      "action_mode": 1,
      "setting_actions": [
        {
          "value": "Option A",
          "action_id": 456,
          "id": 789,
          "detailsAction": [
            {
              "type": "tag",
              "data": { "ids": [1, 2] },
              "active": false,
              "list_tags": [{ "id": 1, "name": "Tag1" }]
            }
          ]
        }
      ]
    }
  }
}
```

---

### EP-08: POST `/basic/initDataItemInfo` — AJAX: danh sách bạn bè theo info
- **Controller**: `FriendInformationController@initDataItemInfo` (dòng 288)
- **Route name**: `initDataItemInfo`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | body | integer/string | Có | ID info setting. Hỗ trợ 'd_1' ~ 'd_6', -6, '-6' cho default fields |

**Response thành công (JSON):**
```json
{
  "status": true,
  "data": [
    {
      "line_id": 100,
      "name": "テスト",
      "value": "2026-01-01",
      "email": "test@example.com"
    }
  ],
  "dataType": 3,
  "settingInfoTitle": "date 1"
}
```

**Default fields mapping:**
| ID | Field | Title JP | dataType |
|----|-------|----------|----------|
| `d_1` | `view_name` | システム表示名 | 2 |
| `d_2` | `phone_number` | 携帯電話 | 2 |
| `d_3` | `email` | メールアドレス | 2 |
| `d_4` | `birthday` | 生年月日 | 2 |
| `d_5` | `age` | 年齢 | 2 |
| `d_6` / `-6` | `province` | 都道府県名 | 1 |

---

### EP-09: POST `/basic/save-setting-info-friend` — Lưu tạo mới / cập nhật
- **Controller**: `FriendInformationController@saveSettingInfoFriend` (dòng 930)
- **Route name**: `item.info_friend.save`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | body | integer/string/null | Không | ID setting (null/empty = tạo mới, có giá trị = cập nhật). Hỗ trợ default IDs: 'd_1','d_2','d_3','d_6' |
| `title` | body | string | Có | Tên quản lý (管理名) |
| `group_id` | body | integer | Có | ID folder |
| `type_data` | body | integer | Có | Kiểu dữ liệu (1=select, 2=input, 3=calendar, 4=image, 5=file, 6=point) |
| `setting_actions` | body | JSON string | Không | Cấu hình action (cho type 1, 3, 6). Chuỗi JSON array objects |
| `action_mode` | body | integer | Không | 1 = 一度のみ (1 lần), 2 = 何度でも稼働 (nhiều lần) |

**Request mẫu (tạo mới type select):**
```json
{
  "id": null,
  "title": "Trạng thái",
  "group_id": 0,
  "type_data": 1,
  "action_mode": 1,
  "setting_actions": "[{\"value\":\"Active\",\"action_id\":null},{\"value\":\"Inactive\",\"action_id\":123}]"
}
```

**Response thành công:**
```json
{
  "status": true,
  "msg": "Success"
}
```

**Side effects quan trọng (khi update):**
1. **Cập nhật ActionDetail**: Nếu title thay đổi → cập nhật `action_detail.data` cho tất cả action type `friend_info` tham chiếu đến info này
2. **Cập nhật FriendInformationValue**: Nếu option_value thay đổi (type select) → cập nhật value trong `friend_information_value`
3. **Quản lý EventStep/EventStepTime** (type calendar = 3): Xoá event_step cũ, tạo mới, tính toán `sent_date_time` cho từng line user
4. **Cập nhật CalendarSettingSendForms / CalendarSalonSettingSendForms**: Nếu type select → cập nhật options
5. **Cập nhật FormAnswerDetails**: Nếu options thay đổi → cập nhật settings items trong form answers
6. **Cập nhật FilterV2**: Nếu type select → cập nhật filter data chứa info_search = id
7. **Reset action cho mode 何度でも稼働**: Nếu action_mode = 2 → set `action = null` trong `friend_information_value`
8. **Xoá orphan FriendInfoOptionSelects**: Options bị xoá khỏi form → xoá records + cập nhật total

**Lỗi có thể xảy ra:**
| HTTP | Mô tả | Điều kiện |
|------|-------|-----------|
| 500 | `MESSAGE_NOTIFY_BACKUP` | Bot đang backup |
| 200 | `{"status": false, "msg": "..."}` | Exception |

---

### EP-10: POST `/basic/copy-setting-info-friend` — Sao chép info
- **Controller**: `FriendInformationController@copySettingInfoFriend` (dòng 830)
- **Route name**: `item.info_friend.copy`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | body | integer | Có | ID info setting cần copy |

**Logic xử lý:**
1. Clone `friend_information_setting` (reset id, timestamps, total_user_has_value = 0)
2. Clone `actions` + `action_detail` cho mỗi setting_action
3. Clone `filter_v2` nếu action_detail có `has_filters = 1`
4. Tạo `friend_info_option_selects` mới nếu type = select (1)
5. Gán order = max(order) + 1

**Response thành công:**
```json
{
  "status": true,
  "msg": "Success",
  "id": 456
}
```

---

### EP-11: POST `/basic/deleteFriendInfo` — Xoá dữ liệu câu trả lời
- **Controller**: `FriendInformationController@deleteFriendInfo` (dòng 367)
- **Route name**: `deleteFriendInfo`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `lineIds` | body | array of integer | Có | Danh sách line_user IDs cần xoá value |
| `id` | body | integer/string | Có | ID info setting |

**Logic theo id:**
- `d_1` → set `line_user.view_name = null` + sync Elasticsearch
- `d_2` → set `line_user.phone_number = null`
- `d_3` → set `line_user.email = null`
- `d_4` → set `line_user.birthday = null` + xoá event_step_time
- `d_5` → set `line_user.age = null`
- `d_6`/`-6` → set `line_user.province = null`
- ID > 0 → xoá `friend_information_value` + giảm `total_user_has_value` + xoá event_step_time (nếu type = 3)
- ID < 0 (khác default) → xoá `friend_information_value`

**Response thành công:**
```json
{
  "status": true
}
```

---

### EP-12: POST `/basic/getFolder` — Lấy danh sách folder
- **Controller**: `FriendInformationController@getFolder` (dòng 473)
- **Route name**: `getFolder`
- **Mức độ tin cậy**: **Cao**

**Response thành công:**
```json
{
  "status": true,
  "groups": [
    {
      "id": 1,
      "bot_id": 100,
      "name": "基本情報",
      "kind": 12,
      "position": 5,
      "is_deleted": 0
    }
  ]
}
```

---

### EP-13: POST `/basic/friend-info-export-csv` — Xuất CSV
- **Controller**: `FriendInformationController@exportCsv` (dòng 191)
- **Route name**: `infoFriendListExportCSV`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | body | integer/string | Có | ID info setting |
| `lineIds` | body | array of integer | Không | Lọc theo line_user IDs (nếu null → xuất tất cả) |

**Logic theo id:**
- Default IDs (`d_1` ~ `d_6`, -6) → query từ `line_user` join `bot_line_user`
- Custom ID → query từ `friend_information_value` join `line_user`
- Dùng `Maatwebsite\Excel` (`ExportListFriendOfInfo`) để tạo file CSV
- File lưu tại `storage/app/public/list_friend_of_info_{timestamp}.csv`

**Response thành công:**
```json
{
  "file_name": "list_friend_of_info_1710000000.csv"
}
```

---

### EP-14: GET `/basic/friend-info/download-csv` — Download CSV
- **Controller**: `FriendInformationController@downloadCsv` (dòng 282)
- **Route name**: `basic.friend-info.download_csv`
- **Mức độ tin cậy**: **Cao**

**Request params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `fileName` | query | string | Có | Tên file từ EP-13 |

**Response:** File download (binary)

---

### EP-15: GET `/basic/get-friend-info` — Lấy danh sách info theo type
- **Controller**: `FriendInformationController@getFriendInfo` (dòng 1447)
- **Route name**: `getFriendInfo`
- **Mức độ tin cậy**: **Cao**

**Response thành công:**
```json
{
  "success": true,
  "data": {
    "text": [
      { "id": 10, "title": "Mô tả", "type_data": 2 }
    ],
    "select": [
      {
        "id": -6,
        "title": "都道府県",
        "setting_value": {
          "action_mode": 0,
          "setting_actions": [
            { "value": "北海道", "title": "北海道" }
          ]
        }
      }
    ],
    "datetime": [
      { "id": 20, "title": "Ngày sinh", "type_data": 3 }
    ]
  },
  "message": ""
}
```

**Ghi chú:** Endpoint này được các tính năng khác sử dụng (action settings, filter) để lấy danh sách friend info fields.

---

## Middleware áp dụng

| Middleware | Mô tả | Áp dụng |
|-----------|-------|---------|
| `web` | Session, CSRF, cookies | Tất cả endpoints |
| `NotifyChatworkRequestTimeSlow` | Thông báo Chatwork nếu request chậm | Tất cả endpoints |
| `LogRequestMultipart` | Log multipart requests | Tất cả endpoints |

**Ghi chú:** Không phát hiện middleware authorization riêng cho tính năng này (như policy hay gate). Kiểm soát truy cập qua session `bot_id` (hàm `getBotId()`). **Mức độ tin cậy**: **Trung bình** — có thể có middleware ở route group level chưa thấy trong index.

---

## Liên kết Endpoint ↔ Màn hình

| Màn hình | Endpoints sử dụng |
|----------|-------------------|
| SCR-FRI-01 (Danh sách) | EP-01 (load trang), EP-06 (AJAX load data + CRUD), EP-12 (load folders) |
| SCR-FRI-02/03/04/05 (Form tạo/sửa) | EP-02 (tạo), EP-03 (sửa), EP-07 (load data), EP-09 (lưu) |
| SCR-FRI-07 (Popup folder) | EP-06 (action=addAndEditGroup) |
| SCR-FRI-08/09 (Danh sách câu trả lời) | EP-05 (load trang), EP-08 (AJAX load data), EP-11 (xoá), EP-13+14 (export CSV) |

---

## API endpoints liên quan (Mobile)

Phát hiện thêm controller `Api\FriendInformationController` (`app/Http/Controllers/Api/FriendInformationController.php`, 1240 dòng) phục vụ mobile app:

| Method | URL | Action | Middleware |
|--------|-----|--------|-----------|
| POST | `/api/mobile/block-friend` | `blockFriend` | `api`, `mobile-auth` |
| POST | `/api/mobile/delete-friend` | `deleteFriend` | `api`, `mobile-auth` |
| POST | `/api/mobile/save-custom-info` | `saveCustomInfo` | `api`, `mobile-auth` |
| POST | `/api/mobile/save-custom-info-v2` | `saveCustomInfo2` | `api`, `mobile-auth` |
| POST | `/api/mobile/save-setting-info-my-page` | `saveSettingInfoMyPage` | `api`, `mobile-auth` |
| POST | `/api/mobile/save-show-custom-info` | `saveShowCustomInfo` | `api`, `mobile-auth` |

**Mức độ tin cậy**: **Cao** — phát hiện qua routes.md. Nội dung chi tiết chưa phân tích (nằm ngoài scope Admin portal).

---

## Endpoint CSV management liên quan

| Method | URL | Controller | Mô tả |
|--------|-----|-----------|-------|
| POST | `/ajax/init-friend-information-for-csv` | `CsvManagementController@ajaxInitFriendInformationForCsv` | Lấy danh sách friend info cho CSV import/export |

**Mức độ tin cậy**: **Cao** — phát hiện qua routes.md. Thuộc tính năng CSV Management, không phải FA-015 trực tiếp.
