# API Spec — FA-010 Mẫu tin nhắn「テンプレート」

> **Mã tính năng:** FA-010
> **Ngày tạo:** 2026-03-26
> **Nguồn:** Source code Laravel — `MessageTemplateController.php`, `TemplateV2Controller.php`, `TemplateV2Service.php`, routes index
> **Tin cậy chung:** **Cao** (đọc trực tiếp từ source code)

---

## 1. Tổng quan Endpoints

### 1.1. Page Routes (trả về HTML view)

| EP | Method | URL | Controller@Method | Middleware | Mô tả | Màn hình |
|----|--------|-----|-------------------|------------|-------|----------|
| EP-01 | GET | `/basic/message-template` | `MessageTemplateController@index` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Danh sách template | SCR-TMT-01 |
| EP-02 | GET | `/basic/message-template/add` | `MessageTemplateController@create` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Trang tạo template mới (editor legacy) | SCR-TMT-04~10 |
| EP-03 | GET | `/basic/message-template/edit/{id}` | `MessageTemplateController@edit` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Trang sửa template (editor legacy) | SCR-TMT-04~10 |
| EP-04 | GET | `/basic/message-template/set-cookie` | `BasicController@folderSetCookie` | web, NotifyChatworkRequestTimeSlow | Lưu folder đang chọn vào cookie | SCR-TMT-01 |
| EP-05 | GET | `/basic/template-v2/add-template` | `TemplateV2Controller@createTemplate` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Trang tạo/sửa template (editor V2) | SCR-TMT-04~10 |
| EP-06 | GET | `/basic/template-v2/create-group` | `TemplateV2Controller@createGroupTemplate` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Trang tạo/sửa group template | — |
| EP-07 | GET | `/basic/template-v2/create-message` | `TemplateV2Controller@createMessage` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Trang tạo message (V2 editor) | SCR-TMT-04~10 |
| EP-08 | GET | `/basic/template-v2/create-message-text` | `TemplateV2Controller@createMessageText` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Component text editor (V2) | SCR-TMT-04 |
| EP-09 | GET | `/basic/park-template/add` | `MessageTemplateController@createPark` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Trang tạo park template (group) | — |
| EP-10 | GET | `/basic/park-template/edit/{id}` | `MessageTemplateController@createPark` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Trang sửa park template (group) | — |
| EP-11 | GET | `/basic/park-template/show/{id}` | `MessageTemplateController@showPark` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Xem nội dung park template | — |
| EP-12 | GET | `/basic/templates/detail/{template_id}` | `MessageTemplateController@templatesDetail` | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Chi tiết template (preview) | — |

### 1.2. AJAX Endpoints — CRUD & Quản lý danh sách

| EP | Method | URL | Controller@Method | Mô tả | Màn hình |
|----|--------|-----|-------------------|-------|----------|
| EP-20 | POST | `/ajax/init-template` | `MessageTemplateController@ajaxInitTemplate` | Khởi tạo / làm mới danh sách template + folder CRUD | SCR-TMT-01 |
| EP-21 | POST | `/basic/message-template/add` | `MessageTemplateController@store` | Lưu template mới (legacy) | SCR-TMT-02 |
| EP-22 | POST | `/basic/message-template/save/{id}` | `MessageTemplateController@save` | Cập nhật template có sẵn (legacy) | SCR-TMT-04~10 |
| EP-23 | POST | `/ajax/delete-template` | `MessageTemplateController@ajaxDelTemplate` | Xoá 1 template | SCR-TMT-01 |
| EP-24 | POST | `/ajax/template/copy` | `MessageTemplateController@copyTemplate` | Sao chép template | SCR-TMT-01 |
| EP-25 | GET | `/ajax/get-template-sort` | `MessageTemplateController@getListTemplateSort` | Lấy danh sách template để sắp xếp | SCR-TMT-01 |
| EP-26 | GET | `/ajax/message-template/{template_id}` | `MessageTemplateController@getById` | Lấy chi tiết 1 template (JSON) | SCR-TMT-06 |

### 1.3. AJAX Endpoints — TemplateV2 (Editor mới)

| EP | Method | URL | Controller@Method | Mô tả | Màn hình |
|----|--------|-----|-------------------|-------|----------|
| EP-30 | POST | `/ajax/template-v2/save-template` | `TemplateV2Controller@saveTemplate` | Lưu/cập nhật template (V2) | SCR-TMT-04~10 |
| EP-31 | POST | `/ajax/template-v2/save-group` | `TemplateV2Controller@ajaxCreateGroup` | Tạo/cập nhật group template (V2) | — |
| EP-32 | POST | `/ajax/template-v2/save-sort-child` | `TemplateV2Controller@saveSortTemplateChild` | Sắp xếp template con trong group | — |
| EP-33 | POST | `/ajax/template-v2/delete-multiple-template-child` | `TemplateV2Controller@deleteMultipleTemplateChild` | Xoá nhiều template con | — |
| EP-34 | POST | `/ajax/template-v2/clone-action-button` | `TemplateV2Controller@cloneActionButton` | Clone action buttons | SCR-TMT-06 |
| EP-35 | POST | `/ajax/template-v2/copy-file` | `TemplateV2Controller@copyFile` | Copy file media (khi clone panel) | SCR-TMT-06 |
| EP-36 | POST | `/ajax/template-v2/update-delay-message` | `TemplateV2Controller@updateDelayMessage` | Bật/tắt delay message | — |

### 1.4. AJAX Endpoints — Lấy dữ liệu editor

| EP | Method | URL | Controller@Method | Mô tả | Màn hình |
|----|--------|-----|-------------------|-------|----------|
| EP-40 | GET | `/ajax/template-v2/get-data` | `TemplateV2Controller@getDataText` | Lấy data cho editor Text | SCR-TMT-04 |
| EP-41 | GET | `/ajax/template-v2/get-data-stamp` | `TemplateV2Controller@getDataStamp` | Lấy data cho editor Sticker | SCR-TMT-09 |
| EP-42 | GET | `/ajax/template-v2/get-data-location` | `TemplateV2Controller@getDataLocation` | Lấy data cho editor Location | SCR-TMT-10 |
| EP-43 | GET | `/ajax/template-v2/get-data-introduction` | `TemplateV2Controller@getDataIntroduction` | Lấy data cho editor Introduction | — |
| EP-44 | GET | `/ajax/template-v2/get-data-preview` | `TemplateV2Controller@getDataPreview` | Lấy preview template | SCR-TMT-01 |
| EP-45 | GET | `/ajax/template-v2/get-data-preview-template-child` | `TemplateV2Controller@getDataPreviewTemplateChild` | Lấy preview template con | — |
| EP-46 | GET | `/ajax/template-v2/init-data-button` | `TemplateV2Controller@initDataButton` | Lấy data khởi tạo cho editor Panel/Button | SCR-TMT-06 |
| EP-47 | GET | `/ajax/template-v2/init-data-media` | `TemplateV2Controller@initDataMedia` | Lấy data khởi tạo cho editor Media | SCR-TMT-08 |
| EP-48 | GET | `/ajax/template-v2/init-data-open-url` | `TemplateV2Controller@initDataOpenUrl` | Lấy danh sách open URL types | SCR-TMT-06 |

### 1.5. AJAX Endpoints — URL Redirect & Metadata

| EP | Method | URL | Controller@Method | Mô tả | Màn hình |
|----|--------|-----|-------------------|-------|----------|
| EP-50 | POST | `/ajax/get-list-url-redirect` | `MessageTemplateController@ajaxGetListUrlRedirect` | Lấy danh sách URL redirect (legacy) | SCR-TMT-05 |
| EP-51 | POST | `/ajax/template-v2/get-list-url-redirect-text` | `TemplateV2Controller@ajaxGetListUrlRedirect` | Lấy danh sách URL redirect (V2) | SCR-TMT-05 |
| EP-52 | POST | `/ajax/template/get-data-open-url` | `MessageTemplateController@getDataOpenUrl` | Lấy danh sách entities theo loại URL mở | SCR-TMT-06 |
| EP-53 | POST | `/ajax/template-v2/get-metadata-url` | `TemplateV2Controller@ajaxMetadataUrl` | Lấy metadata 1 URL (title, image, description) | SCR-TMT-04 |
| EP-54 | POST | `/ajax/template-v2/get-metadata-url-all` | `TemplateV2Controller@ajaxMetadataUrlAll` | Lấy metadata nhiều URLs | SCR-TMT-04 |

### 1.6. AJAX Endpoints — Image Map

| EP | Method | URL | Controller@Method | Mô tả | Màn hình |
|----|--------|-----|-------------------|-------|----------|
| EP-55 | POST | `/ajax/template/image-map/init-data` | `MessageTemplateController@initDataImageMap` | Lấy data image map | SCR-TMT-08 |
| EP-56 | POST | `/ajax/template/image-map/get-data-preview-action` | `MessageTemplateController@getDataPreviewAction` | Lấy preview action trên image map | SCR-TMT-08 |

### 1.7. AJAX Endpoints — Media Library

| EP | Method | URL | Controller@Method | Mô tả | Màn hình |
|----|--------|-----|-------------------|-------|----------|
| EP-60 | POST | `/ajax/get-image-library` | `MessageTemplateController@ajaxGetImageLibrary` | Lấy thư viện ảnh (phân trang) | SCR-TMT-08 |
| EP-61 | POST | `/ajax/get-video-library` | `MessageTemplateController@ajaxGetVideoLibrary` | Lấy thư viện video (phân trang) | SCR-TMT-08 |
| EP-62 | POST | `/ajax/get-voice-library` | `MessageTemplateController@ajaxGetVoiceLibrary` | Lấy thư viện âm thanh (phân trang) | SCR-TMT-08 |
| EP-63 | POST | `/ajax/get-pdf-library` | `MessageTemplateController@ajaxGetPdfLibrary` | Lấy thư viện PDF | SCR-TMT-04 |
| EP-64 | POST | `/ajax/change-thumbnail-history` | `MessageTemplateController@ajaxChangeThumbHistory` | Thay đổi thumbnail video | SCR-TMT-08 |

### 1.8. AJAX Endpoints — Test & LINE User

| EP | Method | URL | Controller@Method | Mô tả | Màn hình |
|----|--------|-----|-------------------|-------|----------|
| EP-70 | POST | `/ajax/template-v2/send-test-template` | `TemplateV2Controller@sendTestTemplate` | Gửi test template đến LINE user | SCR-TMT-01 |
| EP-71 | POST | `/ajax/template-v2/send-test-template-v3` | `TemplateV2Controller@sendTestTemplateV3` | Gửi test template V3 | SCR-TMT-01 |
| EP-72 | POST | `/ajax/template-v2/init-list-line-user-v2` | `TemplateV2Controller@ajaxInitListLineUserData` | Lấy danh sách LINE user (tester) | SCR-TMT-01 |
| EP-73 | POST | `/ajax/template-v2/search-list-line-user-v2` | `TemplateV2Controller@ajaxSearchListLineUserData` | Tìm kiếm LINE user | SCR-TMT-01 |
| EP-74 | POST | `/ajax/template-v2/update-user-quick-reply` | `TemplateV2Controller@updateUserQuickReply` | Cập nhật trạng thái quick reply cho user | — |
| EP-75 | GET | `/ajax/template-v2/get-list-user-quick-reply` | `TemplateV2Controller@getListUserQuickReply` | Lấy danh sách user quick reply | — |

### 1.9. AJAX Endpoints — Park Template (Group)

| EP | Method | URL | Controller@Method | Mô tả | Màn hình |
|----|--------|-----|-------------------|-------|----------|
| EP-80 | POST | `/ajax/park-template/add` | `MessageTemplateController@ajaxUpdateOrCreatePark` | Tạo/cập nhật park template | — |
| EP-81 | POST | `/ajax/init-park-template` | `MessageTemplateController@ajaxInitParkTemplate` | Init danh sách park template | — |
| EP-82 | POST | `/ajax/add-template-park` | `MessageTemplateController@ajaxAddTemplatePark` | Thêm template vào park (clone + thêm) | — |
| EP-83 | GET | `/basic/park-template/list-template/{template_parent_id}` | `MessageTemplateController@getListTemplateChild` | Lấy danh sách template con của group | — |
| EP-84 | POST | `/ajax/park-template/delete-child` | `MessageTemplateController@deleteTemplateInGroup` | Xoá template con khỏi group | — |

### 1.10. Các endpoint liên quan khác

| EP | Method | URL | Controller@Method | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-90 | POST | `/basic/send-template-v2` | `ChatController@sendTemplate` | Gửi template qua chat 1:1 |
| EP-91 | POST | `/basic/upload-pdf-template` | `MediaController@uploadPdfTemplate` | Upload PDF cho template text |
| EP-92 | POST | `/ajax/action-redirect/save` | `MessageTemplateController@saveActionRedirect` | Lưu action redirect URL |

---

## 2. Chi tiết Endpoints chính

### EP-20: POST `/ajax/init-template` — Khởi tạo / thao tác danh sách

**Mô tả:** Endpoint đa năng — vừa lấy danh sách template, vừa thực hiện các thao tác CRUD trên folder và template thông qua tham số `action`. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `action` | body | string | Có | Loại thao tác (xem bảng bên dưới) |
| `group_id` | body | integer | Không | ID folder đang xem |
| `keyword` | body | string | Không | Từ khoá tìm kiếm |
| `page` | body | integer | Không | Trang (nếu có → paginate 20) |
| `group_name` | body | string | Điều kiện | Tên folder (cho addGroup, renameGroup) |
| `id` | body | integer | Điều kiện | ID folder (cho addAndEditGroup) |
| `item_id` | body | integer | Điều kiện | ID template (cho deleteItem) |
| `item_ids` | body | array | Điều kiện | Mảng ID template (cho deleteItems, moveItem) |
| `folder_move_id` | body | integer | Điều kiện | ID folder đích (cho moveItem) |
| `sort_ids` | body | string | Điều kiện | IDs sắp xếp, phân cách bằng dấu phẩy (cho sortItem, sortFolder) |
| `sort_position` | body | string | Điều kiện | Cờ kích hoạt sort |

**Bảng action:**

| Action | Mô tả | Params bắt buộc |
|--------|-------|-----------------|
| `addGroup` | Thêm folder mới | `group_name` |
| `addAndEditGroup` | Tạo hoặc sửa folder | `id`, `group_name` |
| `deleteGroup` | Xoá folder (soft delete) + xoá template bên trong | `group_id` |
| `renameGroup` | Đổi tên folder | `group_id`, `group_name` |
| `searchByKeyWord` | Tìm kiếm template theo tên | `keyword`, `group_id` |
| `deleteItem` | Xoá 1 template | `item_id` |
| `deleteItems` | Xoá nhiều template | `item_ids` |
| `moveItem` | Di chuyển template sang folder khác | `item_ids`, `folder_move_id` |
| `sortItem` | Sắp xếp thứ tự template | `sort_ids`, `sort_position` |
| `sortFolder` | Sắp xếp thứ tự folder | `sort_ids`, `sort_position` |
| *(mặc định/null)* | Chỉ lấy danh sách | `group_id` |

**Response thành công (200):**
```json
{
  "status": true,
  "groups": [
    { "id": 1, "name": "フォルダ名", "bot_id": 123, "position": 1, "kind": 3 }
  ],
  "items": [
    { "id": 10, "name": "テンプレート名", "type": "text", "content": "...", "category_name": "フォルダ名", "created_at": "2024.01.01", "thumbnail_path": "...", "position": 1 }
  ],
  "items_default": [...],
  "group_open": 0,
  "count_default": 5,
  "template_sort": []
}
```

**Lỗi có thể xảy ra:**

| HTTP | Mã lỗi | Mô tả |
|------|--------|-------|
| 200 | `status: false` | Đang backup → `msg: MESSAGE_NOTIFY_BACKUP` |
| 200 | `status: false` | Xoá folder mặc định (id=0) → `msg: "Cannot delete"` |
| 200 | `status: false` | Exception → `msg: <error message>` |

---

### EP-21: POST `/basic/message-template/add` — Lưu template mới (legacy)

**Mô tả:** Tạo template mới — xử lý tất cả các loại (text, stamp, image, video, voice, form, question, location, introduction). **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `botIdCurrent` | body | integer | Có | ID bot hiện tại (verify không đổi account) |
| `tmp_name` | body | string | Có | Tên quản lý template |
| `tmp_type` | body | string | Có | Loại: `text`, `stamp`, `image`, `video`, `voice`, `form`, `question`, `location`, `introduction` |
| `tmp_category` | body | integer | Có | ID folder (0 = 未分類) |
| `tmp_content` | body | string | Có | Nội dung chính (text content hoặc media path) |
| `tmp_is_shorten_url` | body | integer | Không | Dùng URL rút gọn (0/1) |
| `tmp_media` | body | file | Điều kiện | File media (image/video/voice) |
| `media_path` | body | string | Điều kiện | Path media từ library |
| `thumbnail_path` | body | string | Điều kiện | Path thumbnail |
| `send_now` | body | integer | Không | Gửi ngay (category = -botId) |
| `line_id` | body | integer | Không | ID LINE user để gửi ngay |
| `isTester` | body | integer | Không | Cờ tester |
| `park_id` | body | integer | Không | ID park/group template cha |
| `park_id_copy` | body | integer | Không | ID park khi copy |
| `urls_detect` | body | JSON string | Không | Danh sách URL phát hiện trong text |
| `urls_detect_metadata` | body | JSON string | Không | Metadata các URL |
| `number_action_url_redirect` | body | integer | Không | Số lần action URL redirect |
| `tmp_buttons` | body | array | Điều kiện | Dữ liệu buttons (cho type=form) |
| `carousel_action_type` | body | string | Điều kiện | Loại action carousel |
| `alt_text_button` | body | string | Điều kiện | Alt text cho button carousel |
| `action_image_map` | body | array | Điều kiện | Settings image map (cho type=image) |
| `tmp_setting_image_map` | body | integer | Điều kiện | Bật image map (0/1) |
| `action_video_id` | body | integer | Không | ID action video |

**Response thành công (200):**
```json
{
  "success": true,
  "error": "",
  "message": "登録しました",
  "redirect_url": null
}
```

**Lỗi có thể xảy ra:**

| HTTP | Mã lỗi | Mô tả |
|------|--------|-------|
| 200 | `success: false` | Bot đã chuyển account: `"別のアカウントに切り替えたので、要求を処理できません。"` |
| 200 | `status: false` | Đang backup: `MESSAGE_NOTIFY_BACKUP` |
| 200 | `success: false` | Image map area settings sai: `"エリア{N}: 領域設定が間違っています。再度確認してください。"` |
| 200 | `success: false` | Upload ảnh thất bại: `"Upload image to serve fail"` |
| 500 | `success: false` | Exception |

---

### EP-30: POST `/ajax/template-v2/save-template` — Lưu template (V2)

**Mô tả:** Endpoint lưu template cho editor V2. Dữ liệu gửi dưới dạng JSON string trong field `data`. Delegate sang `TemplateV2Service@saveTemplateByType()`. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `data` | body | JSON string | Có | Toàn bộ dữ liệu template (JSON) |
| `action_type` | body | string | Không | Loại action: `template` (mặc định), `scenario`, `sendAll`, `event`, `schedule_send` |
| `templateName` | body | string | Không | Tên template (update khi action_type=template và không có group) |
| `folderId` | body | integer | Không | ID folder (update khi action_type=template và không có group) |

**JSON data (bên trong field `data`):**

| Key | Kiểu | Mô tả |
|-----|------|-------|
| `template_group_id` | integer | ID group template cha |
| `template_child_id` | integer | ID template con (null = tạo mới) |
| *(các field khác tuỳ loại template)* | — | Xử lý bởi service |

**Response thành công (200):**
```json
{
  "success": true,
  "actionType": "template",
  "error_message": ""
}
```

**Lỗi có thể xảy ra:**

| HTTP | Mã lỗi | Mô tả |
|------|--------|-------|
| 200 | `success: false` | Data rỗng: `"Data template empty"` |
| 200 | `success: false` | Gần thời gian phát sóng: `"配信予定日時5分前からは配信内容の編集はできません。"` |
| 200 | `success: false` | Lỗi lưu: `"Save template error"` |

---

### EP-23: POST `/ajax/delete-template` — Xoá template

**Mô tả:** Xoá 1 template theo ID. Nếu template là group → xoá tất cả template con. Cập nhật `template_mapping_tables` và `send_random_message`. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `idTemp` | body | integer | Có | ID template cần xoá |

**Response thành công (200):**
```json
{ "status": true }
```

---

### EP-24: POST `/ajax/template/copy` — Sao chép template

**Mô tả:** Deep clone template bao gồm tất cả dữ liệu liên quan (buttons, image map, URL redirect, actions, location, introduction, question). Template group sẽ clone đệ quy tất cả template con. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `template_id` | body | integer | Có | ID template gốc cần copy |

**Response thành công (200):**
```json
{
  "success": true,
  "type": "text",
  "template_id": 456,
  "message": "Create step message template success"
}
```

---

### EP-70: POST `/ajax/template-v2/send-test-template` — Gửi test template

**Mô tả:** Gửi template test đến các LINE user tester đã chọn. Hỗ trợ group template (gửi lần lượt) và delay message. Gọi LINE Messaging API qua `ChatHelper`. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `template_id` | body | integer | Có | ID template cần test |
| `tester_ids` | body | array | Có | Mảng ID LINE user tester |
| `botIdCurrent` | body | integer | Không | ID bot hiện tại |

**Response thành công (200):**
```json
{
  "success": true,
  "msg": "テスターに送信しました"
}
```

**Lỗi có thể xảy ra:**

| HTTP | Mã lỗi | Mô tả |
|------|--------|-------|
| 200 | `success: false` | Không có tester: `"テストアカウントが設定されていません"` |
| 200 | `success: false` | LINE API rate limit: `"配信数上限に達しています。こちらから契約内容を確認してください。"` |
| 200 | `success: false` | LINE auth fail: `"LINE公式アカウント凍結、もしくは..."` |
| 200 | `success: false` | Gửi thất bại: `Config::get('sns-line.send_fail_msg_screen_chat')` |

---

### EP-72: POST `/ajax/template-v2/init-list-line-user-v2` — Lấy danh sách LINE user tester

**Mô tả:** Lấy danh sách LINE user có cờ `is_tester=1` và chưa bị block. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `page` | body | integer | Không | Trang (chưa dùng, pagination bị comment) |

**Response thành công (200):**
```json
{
  "status": true,
  "items_test": [
    {
      "id": 1,
      "name": "LINE User Name",
      "avatar_url": "https://...",
      "view_name": "Display Name",
      "is_tester": 1,
      "line_user_id": 123,
      "is_quick_reply": 0
    }
  ]
}
```

---

### EP-73: POST `/ajax/template-v2/search-list-line-user-v2` — Tìm kiếm LINE user

**Mô tả:** Tìm kiếm LINE user theo tên. Phân trang 20 items/trang (SimplePaginate). **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `keyword` | body | string | Không | Từ khoá tìm kiếm (name hoặc view_name) |

**Response thành công (200):**
```json
{
  "status": true,
  "items": [...],
  "last_page": 0
}
```

---

### EP-40: GET `/ajax/template-v2/get-data` — Lấy data editor Text

**Mô tả:** Lấy dữ liệu template text bao gồm: template content, danh sách friend info (cho chèn biến tự động), open URL data, LIFF ID. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `template_id` | query | integer | Có | ID template |

**Response thành công (200):**
```json
{
  "id": null,
  "template": { "id": 10, "name": "テスト", "type": "text", "content": "..." },
  "liff_id": "1234-abcd",
  "dataFriendInfo": [
    { "id": 0, "name": "未分類", "friend_information_setting": [...] },
    { "id": -1, "name": "基本情報", "friend_information_setting": [
      { "id": "sys", "title": "表示名", "field": "system_display", "code_friend_info": "[FRIEND_INFO_system_name]" }
    ]}
  ],
  ...
}
```

---

### EP-46: GET `/ajax/template-v2/init-data-button` — Lấy data editor Panel/Button

**Mô tả:** Lấy dữ liệu khởi tạo cho editor Panel/Button: post_back types, reply methods, open URL types, friend info, URL schema types, chi tiết template. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `template_id` | query | integer | Không | ID template (null nếu tạo mới) |

**Response thành công (200):**
```json
{
  "success": true,
  "post_back": { "0": "選択する", "1": "URLを開く", "10": "エルメで設定したページを開く", "8": "送信ボックスにテキストを入力", "9": "他のLOAのプロフィール画面を開く", "3": "他のLOAの友だち追加ページを開く", "2": "電話をかけさせる", "4": "メールを送らせる" },
  "reply_method": { "0": "テキストで返信", "1": "テンプレートで返信" },
  "type_open_url": { "1": "フォーム作成", "6": "カレンダー予約", "3": "イベント予約", "2": "商品販売ページ", "5": "コンバージョンで登録したページ", "7": "サロン・面談予約", "8": "レッスン予約" },
  "dataFriendInfo": [...],
  "typeUrlSchema": [...],
  "template": { ... },
  "data_open_url": { ... },
  "line_id": "LINE_BOT_ID"
}
```

---

### EP-41: GET `/ajax/template-v2/get-data-stamp` — Lấy data editor Sticker

**Mô tả:** Lấy danh sách sticker packages và stickers, cùng với content template đang chỉnh sửa. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `template_id` | query | integer | Có | ID template |

**Response thành công (200):**
```json
{
  "template": { "content": "1234" },
  "sticker": { "1": [100, 101, 102], "2": [200, 201] },
  "stickerPackage": [{ "id": 1, "name": "ムーンスペシャル" }]
}
```

---

### EP-42: GET `/ajax/template-v2/get-data-location` — Lấy data editor Location

**Mô tả:** Lấy dữ liệu location đã lưu (latitude, longitude, address). **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `template_id` | query | integer | Có | ID template |

**Response thành công (200):**
```json
{
  "template": { "content": "..." },
  "tmpLocation": { "template_id": 10, "address": "東京都渋谷区", "latitude": 35.6580, "longitude": 139.7016 }
}
```

---

### EP-31: POST `/ajax/template-v2/save-group` — Tạo/cập nhật group template (V2)

**Mô tả:** Tạo hoặc cập nhật group template. Delegate sang `TemplateV2Service@createTemplateGroup()`. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `template_name` | body | string | Có | Tên group template |
| `template_id` | body | integer | Không | ID (null = tạo mới) |
| `folder_id` | body | integer | Có | ID folder |
| `content` | body | string | Không | IDs template con (comma-separated) |

**Response thành công (200):**
```json
{
  "success": true,
  "redirect_url": "/basic/template-v2/create-group?template_id=123"
}
```

---

### EP-80: POST `/ajax/park-template/add` — Tạo/cập nhật park template

**Mô tả:** Tạo hoặc cập nhật park template (loại group). Park template là container chứa nhiều template con. **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `template_id` | body | integer | Không | ID park (null = tạo mới) |
| `template_name` | body | string | Có | Tên park template |
| `folder_id` | body | integer | Có | ID folder |
| `content` | body | string | Không | IDs template con (comma-separated) |

**Response thành công (200):**
```json
{
  "success": true,
  "error": "",
  "message": "登録しました",
  "redirect_url": "/basic/park-template/edit/123"
}
```

---

### EP-52: POST `/ajax/template/get-data-open-url` — Lấy danh sách entities theo loại URL

**Mô tả:** Lấy danh sách entities tuỳ theo loại (form, product, event, site script, conversion, booking). **[Cao]**

**Request:**

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `type` | body | integer | Có | Loại: 1=Form, 2=Product, 3=Event, 4=SiteScript, 5=Conversion, 6=Booking |

**Response thành công (200):**
```json
{
  "success": true,
  "data": [{ "id": 1, "name": "Contact Form" }]
}
```

---

## 3. Middleware áp dụng

| Middleware | Áp dụng cho | Mô tả |
|-----------|-------------|-------|
| `web` | Tất cả routes | Session, CSRF, authentication |
| `NotifyChatworkRequestTimeSlow` | Tất cả routes | Log request chậm lên Chatwork |
| `LogRequestMultipart` | Hầu hết routes | Log multipart request |
| *(thêm middleware khác cho store/save)* | EP-21, EP-22 | Route store và save có middleware bổ sung (xem routes index: `...`) **[Trung bình]** |

**Xác thực:** Session-based auth — user phải đăng nhập Admin portal. Hàm `getBotId()` lấy bot_id từ session hiện tại. Hàm `getCurrentUser()` lấy user_id. **[Cao]**

---

## 4. Liên kết Endpoint ↔ Màn hình UI

| Màn hình | Endpoints chính | Ghi chú |
|----------|----------------|---------|
| SCR-TMT-01 (Danh sách) | EP-01, EP-20, EP-23, EP-24, EP-25, EP-44, EP-70, EP-71, EP-72, EP-73 | EP-20 là endpoint chính chứa tất cả thao tác |
| SCR-TMT-02 (Dialog tạo mới) | EP-21 hoặc EP-30 | Dialog JS gọi store (legacy) hoặc save-template (V2) |
| SCR-TMT-03 (Thêm folder) | EP-20 (action=addGroup) | Dùng chung endpoint init-template |
| SCR-TMT-04 (Editor Text) | EP-40, EP-21/EP-30, EP-53, EP-54 | |
| SCR-TMT-05 (URL/Action) | EP-50, EP-51 | |
| SCR-TMT-06 (Editor Panel) | EP-26, EP-46, EP-48, EP-52, EP-34, EP-35 | |
| SCR-TMT-07 (Panel Detail) | *(cùng endpoint lưu template)* | |
| SCR-TMT-08 (Editor Media) | EP-47, EP-55, EP-56, EP-60, EP-61, EP-62, EP-64 | |
| SCR-TMT-09 (Editor Sticker) | EP-41 | |
| SCR-TMT-10 (Editor Location) | EP-42 | |
