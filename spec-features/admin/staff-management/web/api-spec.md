# API Spec — FA-035: Quản lý nhân viên (スタッフ管理)

**Tính năng:** FA-035  
**Portal:** Admin  
**Controllers chính:**  
- `app/Http/Controllers/Admin/StaffManagementController.php`  
- `app/Http/Controllers/Admin/UserController.php`  
**Ngày phân tích:** 2026-05-07  
**Mức độ tin cậy tổng thể:** Cao (đọc trực tiếp từ source code)

---

## 1. Tổng quan các Endpoints

| EP | Method | URL | Controller@Action | Middleware | Màn hình |
|----|--------|-----|-------------------|------------|---------|
| EP-01 | GET | `/admin/employees-management` | `Admin\UserController@employeesManagement` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-01 |
| EP-02 | GET | `/admin/invite-staff` | `Admin\StaffManagementController@inviteStaff` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-02 |
| EP-03 | GET | `/admin/setting-role-access` | `Admin\UserController@settingRoleAccess` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-03 |
| EP-04 | GET | `/admin/access-histories` | `Admin\UserController@accessHistories` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-04 |
| EP-05 | GET | `/admin/ajax/get-list-bot-ownership` | `Admin\StaffManagementController@getListBotOwnership` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-01 (dropdown bot) |
| EP-06 | GET | `/admin/ajax/get-list-staff-by-bot` | `Admin\StaffManagementController@getStaffByBot` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-01 (bảng staff) |
| EP-07 | GET | `/admin/ajax/get-list-staff-all-by-bot` | `Admin\StaffManagementController@getStaffAllByBot` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-01 (sort modal / filter) |
| EP-08 | GET | `/admin/get-data-invite-staff` | `Admin\StaffManagementController@getDataInviteStaff` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-02 (load bot list) |
| EP-09 | POST | `/admin/ajax/generate-link-invite-staff` | `Admin\StaffManagementController@generateLinkInviteStaff` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-02 (phát hành URL mời) |
| EP-10 | GET | `/ajax/get-setting-role-access` | `Admin\UserController@getSettingRoleAccess` | (ajax group, không xác định middleware cụ thể) | SCR-EMP-03 (load quyền) |
| EP-11 | POST | `/admin/setting-role-access/edit` | `Admin\UserController@addSettingRoleAccess` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-03 (lưu quyền) |
| EP-12 | GET | `/admin/get-access-histories` | `Admin\UserController@getAccessHistories` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-04 (load dữ liệu) |
| EP-13 | GET | `/admin/export-csv-access-history` | `Admin\UserController@exportCsvAccessHistory` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-04 (export CSV) |
| EP-14 | POST | `/admin/ajax/save-sort-staff` | `Admin\StaffManagementController@saveSortStaff` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-05 (lưu thứ tự) |
| EP-15 | POST | `/admin/ajax/delete-staff-bot` | `Admin\StaffManagementController@deleteStaffBot` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-01 (xóa staff) |
| EP-16 | POST | `/admin/ajax/edit-list-bot-of-staff` | `Admin\StaffManagementController@editListBotOfStaff` | `admin_access`, `https_protocol`, `check_remember_token` | SCR-EMP-02 (chỉnh sửa staff) |
| EP-17 | GET | `/admin/access-link-invite-staff/{code}` | `Admin\StaffManagementController@userAccessLinkInviteStaff` | `admin_access`, `https_protocol`, `check_remember_token` | Landing page xác nhận lời mời |
| EP-18 | GET | `/admin/ajax/get-detail-invite-staff-by-code` | `Admin\StaffManagementController@getDetailInviteStaffByCode` | `admin_access`, `https_protocol`, `check_remember_token` | Modal xác nhận lời mời |
| EP-19 | POST | `/admin/ajax/accept-invite-staff` | `Admin\StaffManagementController@acceptInviteStaff` | `admin_access`, `https_protocol`, `check_remember_token` | Modal xác nhận lời mời |
| EP-20 | POST | `/ajax/employees-management/get-list-bot-access` | `Admin\UserController@getListBotAccess` | (không thuộc nhóm admin_access) | SCR-EMP-02 (load bot access) |
| EP-21 | POST | `/admin/employees-management/add` | `Admin\UserController@addEmployee` | `admin_access`, `https_protocol`, `check_remember_token` | (legacy — thêm employee trực tiếp) |
| EP-22 | POST | `/admin/employees-management/delete/{id}` | `Admin\UserController@deleteEmployee` | `admin_access`, `https_protocol`, `check_remember_token` | (legacy — xóa employee) |

---

## 2. Chi tiết từng Endpoint

---

### EP-01 — GET `/admin/employees-management`
**Controller:** `Admin\UserController@employeesManagement`  
**Màn hình:** SCR-EMP-01  
**Mức độ tin cậy:** Cao

**Mô tả:** Render trang danh sách staff. Server-side render (blade view).

**Request Params:** Không có params bắt buộc.

**Logic server:**
- Kiểm tra `User.is_not_show_popup_staff` và `User.date_show_popup_staff` để quyết định có hiển thị popup hướng dẫn hay không
- Lấy danh sách employees qua `userRepository->getUsersByAdmin($userId)`
- Lấy danh sách roles từ `Role::all()`
- Lấy danh sách bots của admin qua `getListBotId($userId, 'settingRoleAccess')`
- Kiểm tra `plan_type` của bot: bot có `plan_type = 2` và `created_at > 2021-07-01` được đánh dấu `freePlan = 1`

**Response:** HTML view `admin.employee.employees_management_v2`

---

### EP-02 — GET `/admin/invite-staff`
**Controller:** `Admin\StaffManagementController@inviteStaff`  
**Màn hình:** SCR-EMP-02  
**Mức độ tin cậy:** Cao

**Mô tả:** Render trang thêm staff mới.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bot_id` | Query | int | Không | Bot ID mặc định |

**Logic server:**
- Gọi `checkBotHasPermission('staff-management.inviteStaff', bot_id)` — nếu không có quyền → redirect về adminIndex với lỗi
- Lấy `Role::all()` để điền danh sách quyền

**Response:** HTML view `admin.employee.invite_staft`  
**Lỗi:** Redirect về adminIndex nếu không có quyền

---

### EP-03 — GET `/admin/setting-role-access`
**Controller:** `Admin\UserController@settingRoleAccess`  
**Màn hình:** SCR-EMP-03  
**Mức độ tin cậy:** Cao

**Mô tả:** Render trang cài đặt quyền thao tác.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bot_id` | Query | int | Không | Bot ID (mặc định: getBotId()) |

**Logic server:**
- Gọi `checkBotHasPermission('settingRoleAccess', $botId)` — nếu không có quyền → redirect về adminIndex
- Render view trống (data load qua Ajax EP-10)

**Response:** HTML view `admin.setting_role_access_v2`

---

### EP-04 — GET `/admin/access-histories`
**Controller:** `Admin\UserController@accessHistories`  
**Màn hình:** SCR-EMP-04  
**Mức độ tin cậy:** Cao

**Mô tả:** Render trang lịch sử đăng nhập.

**Logic server:**
- Lấy danh sách bots của admin qua `getListBotId($adminId)`
- Truyền danh sách bots vào view để điền dropdown

**Response:** HTML view `admin.employee.access_histories`

---

### EP-05 — GET `/admin/ajax/get-list-bot-ownership`
**Controller:** `Admin\StaffManagementController@getListBotOwnership`  
**Màn hình:** SCR-EMP-01 (dropdown chọn bot)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lấy danh sách bots mà admin có quyền quản lý staff.

**Request Params:** Không có params.

**Logic server:**
- Lấy `adminId` từ `Auth::id()`
- Gọi `getListBotIdStaffManagement($adminId, 'employeesManagement')` — lọc theo quyền `employeesManagement`
- Query bots theo danh sách ID, loại bỏ các bot đã xóa (`is_deleted = 0`), sắp xếp theo `order ASC`, `id DESC`

**Response JSON:**
```json
{
  "bots": [
    {
      "id": 46607,
      "view_name": "N booking standard Y",
      "bot_image": "...",
      "plan_type": 1,
      "created_at": "2021-01-01 00:00:00"
    }
  ],
  "botId": 46607
}
```

---

### EP-06 — GET `/admin/ajax/get-list-staff-by-bot`
**Controller:** `Admin\StaffManagementController@getStaffByBot`  
**Màn hình:** SCR-EMP-01 (bảng danh sách staff)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lấy danh sách staff phân trang theo bot.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bot_id` | Query | int | Có | ID của bot cần xem staff |
| `per_page` | Query | int | Không | Số bản ghi mỗi trang (mặc định: 50) |
| `page` | Query | int | Không | Số trang (mặc định: 1) |

**Logic server:**
- Nếu `bot_id` rỗng → trả về `userStaffs: []`
- Kiểm tra và tự động tạo bản ghi `UserStaffBot` cho Admin (is_admin=1) nếu chưa tồn tại
- JOIN `user_staff_bots` ↔ `users` (qua `user_invite_id`) ↔ `role` (qua `role_id`)
- Sắp xếp theo `position DESC`
- Phân trang theo `per_page`

**Response JSON (Laravel Pagination):**
```json
{
  "userStaffs": {
    "data": [
      {
        "user_id": 123,
        "staff_bot_id": 456,
        "user_invite_id": 123,
        "username": "テスト：ゴー・トゥイ・ガン",
        "email": "ngothuyngan123@gmail.com",
        "role_id": 0,
        "role_name": "主管理者",
        "last_time_login": "2026-04-21 19:47:00",
        "is_admin": 1,
        "staff_name": "テスト：ゴー・トゥイ・ガン",
        "status": 1,
        "bot_id": 46607
      }
    ],
    "current_page": 1,
    "per_page": 50,
    "total": 1
  }
}
```

---

### EP-07 — GET `/admin/ajax/get-list-staff-all-by-bot`
**Controller:** `Admin\StaffManagementController@getStaffAllByBot`  
**Màn hình:** SCR-EMP-01 (modal sort, filter panel), SCR-EMP-04 (panel lọc theo staff)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lấy toàn bộ staff của bot (không phân trang), chỉ lấy status = ACCEPT.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bot_id` | Query | int | Có | ID của bot |

**Logic server:**
- Lọc `user_staff_bots` theo `bot_id` và `status = 1` (STATUS_ACCEPT)
- Sắp xếp theo `position DESC`

**Response JSON:**
```json
{
  "userStaffs": [...]
}
```

---

### EP-08 — GET `/admin/get-data-invite-staff`
**Controller:** `Admin\StaffManagementController@getDataInviteStaff`  
**Màn hình:** SCR-EMP-02 (load danh sách bot để chọn)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lấy danh sách bots để điền form mời staff, kèm thông tin role nếu đang edit staff.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `user_invite_id` | Query | int | Không | ID của staff đang edit (khi edit, không phải invite mới) |
| `user_id` | Query | int | Không | ID của admin owner (khi edit) |

**Logic server:**
- Gọi `getListBotIdStaffManagement($user->id, routeName)` — nếu có `user_invite_id` thì routeName = null
- Loại bỏ bots có `is_deleted = 1` và `plan_type = 2` (free plan)
- Nếu có `user_invite_id`: load `UserStaffBot` để pre-fill role đã chọn
- Gán `selected = 0` và `role_id = 1` mặc định cho mỗi bot

**Response JSON:**
```json
{
  "bot_role": [
    {
      "id": 46607,
      "bot_image": "...",
      "view_name": "N booking standard Y",
      "bot_name": "...",
      "selected": 0,
      "role_id": 1
    }
  ]
}
```

---

### EP-09 — POST `/admin/ajax/generate-link-invite-staff`
**Controller:** `Admin\StaffManagementController@generateLinkInviteStaff`  
**Màn hình:** SCR-EMP-02 (click「招待用URLを発行」)  
**Mức độ tin cậy:** Cao

**Mô tả:** Tạo invitation URL ngẫu nhiên và lưu vào DB.

**Request Params (JSON body):**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `staff_name` | Body | string | Có | Tên staff được mời |
| `bot_role` | Body | JSON string | Có | Array chứa các bot đã chọn và role tương ứng. Mỗi phần tử: `{id, selected, role_id}` |

**Logic server:**
1. Sinh mã `code` ngẫu nhiên 8 ký tự, đảm bảo duy nhất trong `invite_staffs`
2. Lọc các bot có `selected = true/1/'1'/'true'`
3. Với mỗi bot được chọn: lấy `admin_id` của bot từ bảng `bots`
4. Tạo bản ghi `InviteStaff` với `code`, `bot_role (JSON)`, `link`, `staff_name`
5. Với mỗi bot: tạo bản ghi `UserStaffBot` trạng thái `STATUS_NO_ACTION (0)`, cập nhật `position` của admin lên `maxPosition + 1`
6. Link = `url('admin/access-link-invite-staff/' + code)`

**Response JSON:**
```json
{
  "success": true,
  "link": "https://lme.jp/admin/access-link-invite-staff/AbCdEfGh"
}
```

**Lỗi:**
```json
{
  "success": false,
  "error_message": "..."
}
```

---

### EP-10 — GET `/ajax/get-setting-role-access`
**Controller:** `Admin\UserController@getSettingRoleAccess`  
**Màn hình:** SCR-EMP-03 (load bảng quyền)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lấy cấu hình quyền hiện tại theo bot, cùng danh sách features và bots.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bot_id` | Query | int | Không | ID bot cần xem quyền (mặc định: getBotId() hoặc bot đầu tiên trong list) |

**Logic server:**
1. Lấy danh sách bots của admin (loại bỏ free plan tạo sau 2024-11-11)
2. Đọc cấu hình menu từ `config('sns-line.access_feature')`
3. Với mỗi menu → lấy `AccessFeature` (parent = 0) → với mỗi feature lấy `BotRoleAccess` theo `access_id` và `bot_id` → map `role_1/role_2/role_3`
4. Lấy `SettingNewFeature` cho bot (tạo mới nếu chưa có) — cài đặt tự động cấp quyền tính năng mới

**Response JSON:**
```json
{
  "listFeature": {
    "メッセージ配信": [
      {
        "id": 1,
        "name": "一斉配信",
        "role_1": 1,
        "role_2": 0,
        "role_3": 0,
        "featureChilds": []
      }
    ]
  },
  "newFeature": {
    "is_role_1": false,
    "is_role_2": false,
    "is_role_3": false
  },
  "listBot": [...],
  "bot_id": 46607
}
```

---

### EP-11 — POST `/admin/setting-role-access/edit`
**Controller:** `Admin\UserController@addSettingRoleAccess`  
**Màn hình:** SCR-EMP-03 (click「保存する」)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lưu cấu hình quyền thao tác cho bot.

**Request Params (Form data):**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bot_id` | Body | int | Có | ID bot |
| `access1` | Body | array | Không | Map `access_id => 1` cho role 1 (副管理者). Key 0 là toggle toàn bộ |
| `access2` | Body | array | Không | Map `access_id => 1` cho role 2 (運用者). Key 0 là toggle toàn bộ |
| `access3` | Body | array | Không | Map `access_id => 1` cho role 3 (サポート). Key 0 là toggle toàn bộ |

**Logic server:**
1. Kiểm tra `bot_id` thuộc về admin hiện tại — nếu không → redirect về employeesManagement
2. Cập nhật `SettingNewFeature` (is_role_1/2/3 từ key 0 của access arrays)
3. Xóa toàn bộ `BotRoleAccess` cũ của bot
4. Batch insert `BotRoleAccess` mới theo từng role
5. Bỏ qua key = 0 (đó là toggle toàn bộ, không phải access_id)

**Response JSON:**
```json
{"status": true}
```
**HTTP 200** khi thành công, **HTTP 500** khi lỗi.

---

### EP-12 — GET `/admin/get-access-histories`
**Controller:** `Admin\UserController@getAccessHistories`  
**Màn hình:** SCR-EMP-04 (load bảng lịch sử)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lấy lịch sử đăng nhập của staff theo các bộ lọc, phân trang.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bot_id` | Query | int | Không | ID bot |
| `start_time` | Query | date (YYYY-MM-DD) | Không | Ngày bắt đầu lọc |
| `end_time` | Query | date (YYYY-MM-DD) | Không | Ngày kết thúc lọc |
| `keyword` | Query | string | Không | Tìm theo IP hoặc tên staff (LIKE search) |
| `now` | Query | any | Không | Nếu có giá trị → lọc chỉ ngày hôm nay |
| `staffs` | Query | array[int] | Không | Danh sách staff_id để lọc |
| `limit` | Query | int | Có | Số bản ghi mỗi trang |
| `page` | Query | int | Không | Số trang (mặc định: 1) |

**Logic server:**
- JOIN `user_access_bot` ↔ `user_staff_bots` (qua `user_staff_bot_id`) — chỉ lấy các record có `user_staff_bots.id NOT NULL`
- Áp dụng từng điều kiện lọc theo `when()`
- Nếu `is_admin = 1` → lấy tên thật từ bảng `users` (thay vì dùng `staff_name`)
- Sắp xếp theo `id DESC`

**Response JSON:**
```json
{
  "success": true,
  "data": {
    "data": [
      {
        "id": 1,
        "bot_id": 46607,
        "staff_id": 123,
        "staff_name": "テスト：ゴー・トゥイ・ガン",
        "time_access": "2026/05/01 10:00",
        "ip": "192.168.1.1"
      }
    ],
    "current_page": 1,
    "per_page": 100,
    "total": 0
  }
}
```

---

### EP-13 — GET `/admin/export-csv-access-history`
**Controller:** `Admin\UserController@exportCsvAccessHistory`  
**Màn hình:** SCR-EMP-04 (click「CSV」)  
**Mức độ tin cậy:** Cao

**Mô tả:** Xuất lịch sử đăng nhập ra file CSV (encoding Shift-JIS).

**Request Params:** Tương tự EP-12 (cùng bộ lọc, nhưng dùng `now_export` thay vì `now`).

**Logic server:**
- Cùng query logic với EP-12 nhưng không phân trang (lấy toàn bộ)
- Tạo file CSV tại `public/msg_template/access-histories-bot/{timestamp}.csv`
- Header CSV: `アクセス日時`, `スタッフ名`, `IPアドレス`
- Encode sang Shift-JIS (`mb_convert_encoding`)

**Response JSON:**
```json
{
  "status": true,
  "file": "msg_template/access-histories-bot/1234567890.csv"
}
```

---

### EP-14 — POST `/admin/ajax/save-sort-staff`
**Controller:** `Admin\StaffManagementController@saveSortStaff`  
**Màn hình:** SCR-EMP-05 (click「変更を保存」)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lưu thứ tự hiển thị staff sau khi drag-drop.

**Request Params (Form data):**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `ids` | Body | string (CSV) | Có | Danh sách `user_staff_bot.id` cách nhau bằng dấu phẩy, theo thứ tự mới |
| `bot_id` | Body | int | Có | ID bot |

**Logic server:**
- Parse `ids` thành array
- Update `position` theo thứ tự đảo ngược (phần tử đầu = position = total)
- Cập nhật position của admin (is_admin=1) lên `count(ids) + 1`

**Response JSON:**
```json
{"status": true}
```

---

### EP-15 — POST `/admin/ajax/delete-staff-bot`
**Controller:** `Admin\StaffManagementController@deleteStaffBot`  
**Màn hình:** SCR-EMP-01 (nút xóa trong cột「操作」)  
**Mức độ tin cậy:** Cao

**Mô tả:** Xóa staff khỏi bot (xóa bản ghi UserStaffBot).

**Request Params (Form data):**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `staff_bot_id` | Body | int | Có | ID bản ghi `user_staff_bots` |
| `user_invite_id` | Body | int | Không | ID của staff (để check xem có phải tự xóa mình không) |

**Logic server:**
- Lấy thông tin `UserStaffBot` trước khi xóa
- Xóa bản ghi (`UserStaffBot::destroy`)
- Nếu `user_invite_id == Auth::id()` → xóa session `current_bot_id` và `is_bot_invite`
- Hủy đăng ký Firebase topic cho staff bị xóa
- Ghi log `BotLifeCycle::addState` với type `DELETE_STAFF`

**Response JSON:**
```json
{"status": true}
```

---

### EP-16 — POST `/admin/ajax/edit-list-bot-of-staff`
**Controller:** `Admin\StaffManagementController@editListBotOfStaff`  
**Màn hình:** SCR-EMP-02 (khi chỉnh sửa staff đã có)  
**Mức độ tin cậy:** Cao

**Mô tả:** Cập nhật danh sách bot và role cho staff đã tồn tại.

**Request Params (Form data):**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bot_role` | Body | array | Có | Array các `{user_staff_bot_id, role_id}` |
| `staff_name` | Body | string | Không | Tên mới của staff |
| `user_invite_id` | Body | int | Không | ID của staff |
| `staff_name_old` | Body | string | Không | Tên cũ (dùng khi `staff_name` rỗng) |

**Response JSON:**
```json
{"success": true}
```

---

### EP-17 — GET `/admin/access-link-invite-staff/{code}`
**Controller:** `Admin\StaffManagementController@userAccessLinkInviteStaff`  
**Màn hình:** Landing page khi staff click invite URL  
**Mức độ tin cậy:** Cao

**Mô tả:** Xử lý khi staff click vào invite URL.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `code` | URL path | string(8) | Có | Mã mời ngẫu nhiên 8 ký tự |

**Logic server:**
- Tìm `InviteStaff` theo `code` — không tồn tại → redirect adminIndex
- Nếu `is_confirmed = 1` → lỗi "URLは無効" redirect
- Nếu `user_id != currentUser` (người khác dùng URL):
  - Kiểm tra hết hạn 24h (`created_at + 86400 < time()`) → lỗi "有効期限を超えました"
  - Kiểm tra đã truy cập URL lần 2 → lỗi "既に操作しました"
- Nếu `user_id == currentUser` (chính admin tạo invite) → redirect thẳng adminIndex
- Redirect về adminIndex với session params: `user_access_link_invite=true`, `code_invite=code`, `type_invite`

**Response:** Redirect (HTTP 302)

---

### EP-18 — GET `/admin/ajax/get-detail-invite-staff-by-code`
**Controller:** `Admin\StaffManagementController@getDetailInviteStaffByCode`  
**Màn hình:** Modal xác nhận lời mời  
**Mức độ tin cậy:** Cao

**Mô tả:** Lấy thông tin chi tiết lời mời để hiển thị modal xác nhận.

**Request Params:**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `code` | Query | string | Có | Mã mời |

**Logic server:**
- Lấy `InviteStaff` theo code
- Tìm các bots trong lời mời chưa thuộc về người dùng hiện tại
- Tạo bản ghi `UserStaff` nếu chưa có (tracking trạng thái xác nhận)

**Response JSON:**
```json
{
  "success": true,
  "invite_staff": {...},
  "user_staff_id": 1,
  "bots": [{"id": 46607, "role_id": 1, "user_staff_id": 1, ...}]
}
```

---

### EP-19 — POST `/admin/ajax/accept-invite-staff`
**Controller:** `Admin\StaffManagementController@acceptInviteStaff`  
**Màn hình:** Modal xác nhận lời mời  
**Mức độ tin cậy:** Cao

**Mô tả:** Staff xác nhận chấp nhận lời mời — chính thức trở thành staff của bot.

**Request Params (JSON body):**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `bots` | Body | array | Có | Danh sách bots đồng ý tham gia |
| `code` | Body | string | Có | Mã mời |

**Logic server:**
1. Kiểm tra `InviteStaff` tồn tại, chưa confirmed, chưa hết hạn 24h
2. Xóa session `user_access_link_invite`, `code_invite`
3. Với mỗi bot:
   - Nếu đã accept → skip
   - Cập nhật `UserStaffBot` virtual → status `STATUS_ACCEPT`, gán `user_invite_id`, `staff_name`
   - Ghi log `BotLifeCycle::addState` type `ADD_STAFF`
4. Kiểm tra không có user khác đã accept cùng lời mời (tránh dùng link 2 lần bởi 2 người khác nhau)
5. Đăng ký Firebase topic cho các bots mới
6. Cập nhật `InviteStaff.is_confirmed = 1`

**Response JSON:**
```json
{"success": true}
```
Hoặc lỗi:
```json
{"success": false, "error_message": "招待されたURLはすでに無効となっています。..."}
```

---

### EP-20 — POST `/ajax/employees-management/get-list-bot-access`
**Controller:** `Admin\UserController@getListBotAccess`  
**Màn hình:** SCR-EMP-02 (load danh sách bot với trạng thái checked)  
**Mức độ tin cậy:** Cao

**Mô tả:** Lấy danh sách bots kèm trạng thái access của một user cụ thể (dùng khi edit employee).

**Request Params (Form data):**
| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|---------|-------|
| `id` | Body | int | Có | ID của user (staff) cần xem |

**Response JSON:**
```json
{
  "success": true,
  "allBotNew": {
    "46607": {
      "id": 46607,
      "view_name": "...",
      "checked": true,
      "accessNumber": 1,
      "freePlan": 0
    }
  }
}
```

---

### EP-21 — POST `/admin/employees-management/add` (Legacy)
**Controller:** `Admin\UserController@addEmployee`  
**Mức độ tin cậy:** Cao

**Mô tả:** Thêm employee cũ (tạo tài khoản user mới trực tiếp với password). **Đây là flow cũ**, flow mới dùng invite URL (EP-09).

**Validation:**
- `username`: required
- `password`: required
- `email`: required, email format, unique trong bảng `users`

**Logic:** Tạo user mới với `role = 2`, `admin_id = userId`, bcrypt password, tạo `AccessBot` records.

---

### EP-22 — POST `/admin/employees-management/delete/{id}` (Legacy)
**Controller:** `Admin\UserController@deleteEmployee`  
**Mức độ tin cậy:** Cao

**Mô tả:** Xóa employee (xóa hẳn user khỏi DB). **Flow cũ**.

**Logic:** Xóa user khỏi `users`, xóa toàn bộ `AccessBot` của user.

---

## 3. Liên kết Endpoint ↔ Màn hình

| Màn hình | Endpoints được gọi |
|----------|-------------------|
| SCR-EMP-01 (Danh sách Staff) | EP-01 (render), EP-05 (load bots), EP-06 (load staff table), EP-15 (xóa staff) |
| SCR-EMP-02 (Thêm Staff) | EP-02 (render), EP-08 (load bots), EP-09 (phát hành URL) |
| SCR-EMP-03 (Cài đặt quyền) | EP-03 (render), EP-10 (load quyền), EP-11 (lưu quyền) |
| SCR-EMP-04 (Lịch sử đăng nhập) | EP-04 (render), EP-12 (load data), EP-13 (export CSV) |
| SCR-EMP-05 (Modal sort) | EP-07 (load staff list), EP-14 (lưu thứ tự) |
| Modal xác nhận invite (Staff side) | EP-17 (access link), EP-18 (get detail), EP-19 (accept) |
