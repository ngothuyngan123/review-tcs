# FA-007 — Tin nhắn chào mừng: API Spec

## Tổng quan

| Thuộc tính | Giá trị |
|-----------|---------|
| Mã tính năng | FA-007 |
| Tên tính năng | Tin nhắn chào mừng (「あいさつメッセージ」) |
| Controller chính | `Basic\SettingAddFriendController` |
| Controller phụ | `Basic\ScenarioController` |
| Mức độ tin cậy chung | **Cao** — phân tích trực tiếp từ source code Laravel |

---

## Danh sách Endpoints

| Mã | Method | URL | Mô tả | Màn hình liên quan |
|----|--------|-----|-------|--------------------|
| EP-01 | GET | `/basic/setting-add-friend` | Trang cấu hình bạn mới | SCR-SAF-01 |
| EP-02 | GET | `/basic/setting-add-friend-old` | Trang cấu hình bạn cũ | SCR-SAF-02 |
| EP-03 | GET | `/basic/setting-add-friend-unblock` | Trang cấu hình hủy chặn | SCR-SAF-03 |
| EP-04 | GET | `/basic/get-setting-add-friend-v2` | API load cấu hình (JSON) | SCR-SAF-01/02/03 |
| EP-05 | POST | `/basic/save-setting-add-friend-v2` | API lưu cấu hình (JSON) | SCR-SAF-01/02/03 |
| EP-06 | POST | `/basic/update-setting-add-friend` | API cũ — cập nhật action_new/old (JSON) | (legacy) |
| EP-07 | POST | `/ajax/init-data-setting-add-friend` | AJAX load action cũ (JSON) | (legacy) |
| EP-08 | GET | `/ajax/setting-add-friend/get-message-preview/{typeSetting}` | Preview message (JSON) | (legacy) |
| EP-09 | GET | `/ajax/setting-add-friend/remove-message/{typeSetting}` | Xóa message (JSON) | (legacy) |

> **Ghi chú**: EP-06 đến EP-09 là các endpoint legacy từ phiên bản cũ. Phiên bản V2 hiện tại dùng EP-04 và EP-05.

---

## Chi tiết Endpoints

---

### EP-01: GET `/basic/setting-add-friend`

**Mô tả**: Render trang HTML cấu hình tin nhắn chào mừng bạn mới.

**Route name**: `settingAddFriend`

**Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`

**Middleware mô tả**:
- `basic_access`: Kiểm tra đăng nhập và role (role = 0/1/-1/2), kiểm tra bot trong session, kiểm tra phân quyền Staff nếu là staff account
- `is_expire`: Kiểm tra gói dịch vụ chưa hết hạn — nếu hết hạn redirect sang `/basic/point-settings`
- `https_protocol`: Đảm bảo kết nối HTTPS
- `check_remember_token`: Kiểm tra remember token hợp lệ

**Controller**: `Basic\SettingAddFriendController@settingAddFriendNew`

**Request params**: Không có

**Response**: HTML view `basic.setting_add_friend.setting-add-friend-new`

**Data truyền vào view**:
| Tên | Kiểu | Mô tả |
|-----|------|-------|
| `richMenus` | array | Danh sách rich menu (hiện để rỗng `[]`) |
| `scenario` | array | Danh sách scenario (hiện để rỗng `[]`) |
| `statusObject` | Collection | Danh sách trạng thái chat từ bảng `status_chat` theo `bot_id` |
| `conversion` | array | Dữ liệu conversion (hiện để rỗng `[]`) |
| `type` | string | `'add_new'` (cố định) |

**Màn hình**: SCR-SAF-01

**Mức độ tin cậy**: **Cao**

---

### EP-02: GET `/basic/setting-add-friend-old`

**Mô tả**: Render trang HTML cấu hình tin nhắn chào mừng bạn cũ.

**Route name**: `settingAddFriendOld`

**Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`

**Controller**: `Basic\SettingAddFriendController@settingAddFriendOld`

**Request params**: Không có

**Response**: HTML view `basic.setting_add_friend.setting-add-friend-old`

**Data truyền vào view**:
| Tên | Kiểu | Mô tả |
|-----|------|-------|
| `richMenus` | array | `[]` |
| `scenario` | array | `[]` |
| `statusObject` | Collection | Danh sách trạng thái chat theo `bot_id` |
| `conversion` | array | `[]` |
| `type` | string | `'add_old'` (cố định) |

**Màn hình**: SCR-SAF-02

**Mức độ tin cậy**: **Cao**

---

### EP-03: GET `/basic/setting-add-friend-unblock`

**Mô tả**: Render trang HTML cấu hình tin nhắn khi bạn bè hủy chặn.

**Route name**: `settingAddFriendUnblock`

**Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`

**Controller**: `Basic\SettingAddFriendController@settingAddFriendUnblock`

**Request params**: Không có

**Response**: HTML view `basic.setting_add_friend.setting-add-friend-unblock`

**Data truyền vào view**:
| Tên | Kiểu | Mô tả |
|-----|------|-------|
| `richMenus` | array | `[]` |
| `scenario` | array | `[]` |
| `statusObject` | Collection | Danh sách trạng thái chat theo `bot_id` |
| `conversion` | array | `[]` |
| `type` | string | `'unblock'` (cố định) |

**Màn hình**: SCR-SAF-03

**Mức độ tin cậy**: **Cao**

---

### EP-04: GET `/basic/get-setting-add-friend-v2`

**Mô tả**: API JSON load cấu hình tin nhắn chào mừng. Được gọi bằng AJAX khi trang khởi tạo (hàm `getAddFriend()` trong JS).

**Route name**: `getSettingAddFriend`

**Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`

**Controller**: `Basic\SettingAddFriendController@getSettingAddFriend`

**Request — Query Params**:
| Tên | Bắt buộc | Kiểu | Giá trị hợp lệ | Mô tả |
|-----|----------|------|----------------|-------|
| `type` | Có | string | `add_new` / `add_old` / `unblock` | Loại cấu hình cần tải |

**Logic xử lý**:
1. Lấy `bot_id` từ session
2. Tìm bản ghi `AddFriendSetting` theo `bot_id`
3. Nếu không tìm thấy → tự động tạo mới `AddFriendSetting` với `bot_id`
4. Theo `type`, lấy `action_id` và `template_id` tương ứng:
   - `add_new` → `action_new_id`, `template_add_new_id`
   - `add_old` → `action_old_id`, `template_add_old_id`
   - `unblock` → `action_id_unblock`, `template_unblock_id`
5. Lấy nội dung tin nhắn từ bảng `template` theo `template_id`
6. Load chi tiết action từ bảng `t_actions_detail`
7. Lấy `url_add_friend` từ bảng `bots`
8. Tạo URL QR code từ media server (`URL_SERVER_MEDIA` + `FOLDER_MEDIA` + path)

**Response — JSON**:
```json
{
  "actionId": 123,
  "message": "Nội dung tin nhắn text (hoặc null nếu chưa cấu hình)",
  "detailAction": [
    {
      "id": 1,
      "action_id": 123,
      "type": "tag",
      "data": { ... },
      "list_tags": [ ... ],
      "is_edit_content": false
    }
  ],
  "urlAddFriend": "https://line.me/R/ti/p/%40573thndt",
  "qrCode": "https://media.server.com/ext-media/qr_image/qr_add_friend_bot_456.png?v=1716345600"
}
```

**Response fields**:
| Field | Kiểu | Mô tả |
|-------|------|-------|
| `actionId` | int/null | ID action LME đang được cấu hình |
| `message` | string/null | Nội dung tin nhắn văn bản |
| `detailAction` | array | Mảng chi tiết các action (từ `t_actions_detail`) |
| `urlAddFriend` | string/null | URL bạn bè từ LINE (`bots.url_add_friend`) |
| `qrCode` | string | URL hình ảnh QR code |

**Màn hình**: SCR-SAF-01, SCR-SAF-02, SCR-SAF-03

**Mức độ tin cậy**: **Cao**

---

### EP-05: POST `/basic/save-setting-add-friend-v2`

**Mô tả**: API JSON lưu cấu hình tin nhắn chào mừng. Được gọi bằng AJAX khi Admin click nút 「保存」.

**Route name**: `saveSettingAddFriend`

**Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`

**Controller**: `Basic\SettingAddFriendController@saveSettingAddFriend`

**Request — POST body** (form data hoặc JSON):
| Tên | Bắt buộc | Kiểu | Giá trị hợp lệ | Mô tả |
|-----|----------|------|----------------|-------|
| `type` | Có | string | `add_new` / `add_old` / `unblock` | Loại cấu hình cần lưu |
| `actionId` | Không | int/null | ID của action | ID action LME đã chọn |
| `message` | Không | string | Tối đa 5,000 ký tự | Nội dung tin nhắn text |
| `botIdCurrent` | Có | int | ID bot | Bot ID để kiểm tra tránh ghi nhầm khi đổi bot |

**Bảo vệ bot-switch**: Nếu `bot_id` session khác `botIdCurrent` trong request → trả về lỗi JSON:
```json
{ "success": false, "message": "別のアカウントに切り替えたので、要求を処理できません。" }
```

**Logic xử lý**:
1. Kiểm tra `bot_id` session == `botIdCurrent` request (bảo vệ bot-switch)
2. Tìm `AddFriendSetting` theo `bot_id`
3. Xử lý template tin nhắn (hàm `handleMessageTemplate`):
   - Nếu `message` rỗng → xóa template cũ (nếu có), set `templateId = null`
   - Nếu `message` không rỗng → upsert bản ghi `template` với `category_id = -1212`, `type = 'text'`
4. Theo `type`, cập nhật hoặc tạo `AddFriendSetting`:
   - `add_new` → cập nhật `action_new_id`, `template_add_new_id`
   - `add_old` → cập nhật `action_old_id`, `template_add_old_id`
   - `unblock` → cập nhật `action_id_unblock`, `template_unblock_id`
5. Sử dụng `updateOrCreate` với `bot_id` làm key tìm kiếm

**Response — JSON thành công**:
```json
{ "success": true }
```

**Response — JSON lỗi**:
```json
{ "success": false, "message": "エラーメッセージ" }
```

**Màn hình**: SCR-SAF-01, SCR-SAF-02, SCR-SAF-03

**Mức độ tin cậy**: **Cao**

---

### EP-06: POST `/basic/update-setting-add-friend` (Legacy)

**Mô tả**: API cũ — chỉ cập nhật `action_new_id` và `action_old_id` (không có `unblock`, không có `message`). Có thể không còn được dùng trong UI V2.

**Route name**: `updateSettingAddFriend`

**Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`

**Controller**: `Basic\ScenarioController@updateSettingAddFriend`

**Request — POST body**:
| Tên | Bắt buộc | Kiểu | Mô tả |
|-----|----------|------|-------|
| `botIdCurrent` | Có | int | Bot ID kiểm tra |
| `action_new_id` | Không | int/null | Action ID cho bạn mới |
| `action_old_id` | Không | int/null | Action ID cho bạn cũ |

**Response**: `{ "success": true/false, "error": "..." }`

**Mức độ tin cậy**: **Cao** (source code rõ ràng, nhưng khả năng là endpoint legacy)

---

### EP-07: POST `/ajax/init-data-setting-add-friend` (Legacy)

**Mô tả**: AJAX khởi tạo dữ liệu action cũ (chỉ cho `action_new_id` và `action_old_id`).

**Route name**: `reply.init_data_setting_add_friend`

**Controller**: `Basic\ScenarioController@initDataSettingAddFriend`

**Request**: Không có params (dùng `bot_id` từ session)

**Response — JSON**:
```json
{
  "success": true,
  "action_new_id": 123,
  "action_old_id": 456,
  "detail_action_new": [ ... ],
  "detail_action_old": [ ... ]
}
```

**Mức độ tin cậy**: **Cao** (source code rõ ràng, endpoint legacy)

---

### EP-08: GET `/ajax/setting-add-friend/get-message-preview/{typeSetting}` (Legacy)

**Mô tả**: Preview tin nhắn từ `sent_templates_new_friend` / `sent_templates_old_friend` (dữ liệu cũ dạng JSON array trong `add_friend_setting`).

**Route name**: `scenario.getMessagePreview`

**Controller**: `Basic\ScenarioController@getMessagePreview`

**Request — URL params**:
| Tên | Kiểu | Giá trị | Mô tả |
|-----|------|---------|-------|
| `typeSetting` | string | `new` / `old` | Loại cài đặt |

**Response**:
```json
{ "success": true, "messages": [ ... ] }
```

**Mức độ tin cậy**: **Cao** (source code rõ ràng, endpoint legacy)

---

### EP-09: GET `/ajax/setting-add-friend/remove-message/{typeSetting}` (Legacy)

**Mô tả**: Xóa một tin nhắn khỏi danh sách `sent_templates_*` (dữ liệu cũ).

**Route name**: `scenario.removeMessageSetting`

**Controller**: `Basic\ScenarioController@removeMessageSetting`

**Request — URL params + Query**:
| Tên | Kiểu | Mô tả |
|-----|------|-------|
| `typeSetting` | string | `new` / `old` |
| `msg` | int | Vị trí message cần xóa (1, 2, 3) |

**Mức độ tin cậy**: **Cao** (source code rõ ràng, endpoint legacy)

---

## Mapping Endpoint ↔ Màn hình

| Màn hình | URL | Endpoints được gọi |
|----------|-----|---------------------|
| SCR-SAF-01 (bạn mới) | `/basic/setting-add-friend` | EP-01 (page load) → EP-04 (AJAX init, `type=add_new`) → EP-05 (save, `type=add_new`) |
| SCR-SAF-02 (bạn cũ) | `/basic/setting-add-friend-old` | EP-02 (page load) → EP-04 (AJAX init, `type=add_old`) → EP-05 (save, `type=add_old`) |
| SCR-SAF-03 (hủy chặn) | `/basic/setting-add-friend-unblock` | EP-03 (page load) → EP-04 (AJAX init, `type=unblock`) → EP-05 (save, `type=unblock`) |
| SCR-SAF-04 (tab test) | Cùng với SCR-SAF-01/02/03 | Không có API riêng — là tab trên cùng trang |
| SCR-SAF-05 (modal action) | Modal trên SCR-SAF-01/02/03 | Endpoint của SC-004 Action Settings (không thuộc FA-007 trực tiếp) |

---

## Lưu ý về phiên bản API

Tính năng này có **2 phiên bản song song**:

| Phiên bản | Endpoints | Đặc điểm |
|-----------|-----------|----------|
| V2 (hiện tại) | EP-01 đến EP-05 | Dùng `SettingAddFriendController`, lưu 1 text message + 1 action per type |
| V1 (legacy) | EP-06 đến EP-09 | Dùng `ScenarioController`, lưu tối đa 3 template messages, không hỗ trợ `unblock` |

V1 legacy vẫn còn route định nghĩa nhưng có thể không còn được gọi từ UI V2.
