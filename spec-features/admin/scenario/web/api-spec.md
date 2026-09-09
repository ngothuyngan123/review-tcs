# API Spec — FA-009: Phát hành theo bước (ステップ配信)

## Tổng quan Endpoints

| # | Method | URL | Controller@Method | Mô tả |
|---|--------|-----|-------------------|-------|
| EP-01 | GET | /basic/scenario | ScenarioController@index | Danh sách scenario (trang chủ) |
| EP-02 | POST | /basic/scenario | ScenarioController@store | Tạo scenario mới |
| EP-03 | PUT/PATCH | /basic/scenario/{scenario} | ScenarioController@update | Cập nhật tên/folder/next scenario |
| EP-04 | DELETE | /basic/scenario/{scenario} | ScenarioController@destroy | Xoá scenario và toàn bộ dữ liệu |
| EP-05 | GET | /basic/scenario/{scenario}/edit | ScenarioController@edit | Form edit scenario (cũ, hiện ít dùng) |
| EP-06 | GET | /basic/scenario/pack-template/show/{scenario_id}/{pack_id} | ScenarioController@showPark | Hiển thị template pack để chọn |
| EP-07 | GET | /scenario-setting | ScenarioController@setting | Trang cài đặt scenario (cũ) |
| EP-08 | GET | /scenario-users | ScenarioController@getListFriendByScenarioId | Lấy danh sách LINE user theo scenario/step |
| EP-09 | POST | /basic/scenario-check-delete | ScenarioController@scenarioCheckDelete | Kiểm tra xem scenario có step nào chưa |
| EP-10 | GET | /basic/scenario/copy/{scenario} | ScenarioController@copyScenario | Nhân bản (copy) một scenario |
| EP-11 | POST | /basic/scenario-setting | ScenarioController@updateSetting | Cập nhật cài đặt liên kết scenario – add friend |
| EP-12 | GET | /step-message/list-message/{scenario} | StepMessageController@listMessage | Trang danh sách step message (view cũ) |
| EP-13 | GET | /step-message/scenario-message/{scenario} | StepMessageController@scenarioMessage | Trang thiết kế step scenario (view chính) |
| EP-14 | GET | /step-message/preview-scenario-message/{scenario} | StepMessageController@previewScenarioMessage | Trang preview step scenario |
| EP-15 | GET | /step-message/create/{scenario}/{scenario_step_id} | StepMessageController@create | Form tạo/clone message trong step |
| EP-16 | GET | /step-message/edit/{step_message}/{template_id} | StepMessageController@edit | Form sửa message trong step |
| EP-17 | GET | /step-message-template-child/{scenarioId}/{stepId}/{templateId} | StepMessageController@templateChildStep | Xem danh sách template con bên trong group template |
| EP-18 | POST | /basic/step-message/store/{scenario} | StepMessageController@store | Lưu (tạo mới) nội dung message cho step |
| EP-19 | POST | /scenario/delete-set-profile-bot | StepMessageController@deleteProfilesBots | Xoá profile bot khỏi step message |
| EP-20 | POST | /step-message/save-selected-profile-bot | StepMessageController@saveSelectedProfileBot | Chọn profile gửi tin cho step |
| EP-21 | POST | /save-data-scenario | StepMessageController@saveDataScenario | Lưu tên/folder/next scenario từ trang scenario-message |
| EP-22 | POST | /mark-close-alert | StepMessageController@markCloseAlert | Đánh dấu đã xem alert thêm step/message |
| EP-23 | POST | /add-friend/update-setting-message | ScenarioController@updateSettingMessage | Cập nhật tin nhắn gửi khi thêm bạn |
| EP-24 | GET | /add-friend/setting-message/{typeSetting} | ScenarioController@settingMessage | Form tạo tin nhắn add-friend |
| EP-25 | GET | /add-friend/edit-setting-message/{typeSetting} | ScenarioController@editSettingMessage | Form sửa tin nhắn add-friend |
| EP-26 | POST | /update-setting-add-friend | ScenarioController@updateSettingAddFriend | Cập nhật cài đặt hành động khi thêm bạn |

Middleware chung: `['basic_access', 'https_protocol', 'is_expire', 'check_remember_token']`

---

## Chi tiết Endpoints

### EP-01: GET /basic/scenario — Danh sách scenario
**Controller**: `Basic\ScenarioController@index`
**Mô tả**: Trả về trang danh sách tất cả scenario của bot đang active.

#### Logic
1. Lấy `bot_id` hiện tại qua helper `getBotId()`.
2. Lấy tất cả `Scenario` theo `bot_id`.
3. Đọc `folder_scenario` cookie (JSON) để xác định folder đang active (`folderId`).
4. Kiểm tra `Category` có tồn tại theo `folderId`; nếu không hợp lệ, reset về `0`.
5. Set lại cookie nếu cần.

#### Response
View: `basic.scenario.scenario_index`
- `scenario`: Collection — toàn bộ scenarios của bot
- `folderId`: int — ID folder đang active (0 = không có folder)

---

### EP-02: POST /basic/scenario — Tạo scenario mới
**Controller**: `Basic\ScenarioController@store`
**Mô tả**: Tạo một scenario mới (AJAX).

#### Request Body
| Field | Type | Required | Validation | Mô tả |
|-------|------|----------|------------|-------|
| `name` | string | Có | `required\|max:20` | Tên scenario |
| `botIdCurrent` | int | Có | — | Bot ID xác nhận chéo |
| `select_folder_create` | int | Không | — | ID folder muốn đặt scenario vào |
| `next_scenario` | int | Không | — | ID scenario tiếp theo |
| `flag_position` | int/null | Không | — | Nếu có: thêm vào đầu danh sách; không có: thêm vào cuối |

#### Validation
- `name` required, max 20 ký tự. Lỗi: `「ステップ名を入力して下さい。」`
- `botIdCurrent` phải khớp với `getBotId()` hiện tại
- Không được trong trạng thái backup/transfer (`BackupHistory` status 0 hoặc 1)

#### Response (200 OK)
```json
{
  "success": true,
  "folderId": 0,
  "scenarioId": 123
}
```
#### Response (lỗi 500)
```json
{ "success": false, "msg": "..." }
```

---

### EP-03: PUT/PATCH /basic/scenario/{scenario} — Cập nhật scenario
**Controller**: `Basic\ScenarioController@update`
**Mô tả**: Đổi tên, folder, và next-scenario (AJAX).

#### Request Body
| Field | Type | Mô tả |
|-------|------|-------|
| `name_edit` | string | Tên mới (required) |
| `botIdCurrent` | int | Bot ID xác nhận chéo |
| `scenario_id` | int | ID scenario cần update |
| `next_scenario_edit` | int | ID scenario tiếp theo mới |
| `select_folder_edit` | int | ID folder mới |

#### Fields được update trong DB
`name`, `after_scenario_id_1`, `group_id`, `delay_type_1=0`, `after_start_day_1=null`, `after_start_time_1=null`, `from_1=null`, `to_1=null`

#### Response (200 OK)
```json
{ "success": true, "folderId": 0 }
```

---

### EP-04: DELETE /basic/scenario/{scenario} — Xoá scenario
**Controller**: `Basic\ScenarioController@destroy`
**Auth Request**: `OwnerGetScenario` (kiểm tra bot_id chủ sở hữu)
**Mô tả**: Xoá scenario và cascade toàn bộ dữ liệu liên quan.

#### Cascade khi xoá
1. Xoá `scenario_step_time` theo step IDs
2. Xoá toàn bộ `step_message` của scenario
3. Xoá bản ghi `scenario`
4. Xoá `scenario_lineuser` của bot
5. Xoá `step_message_history` của bot
6. Xoá `filter_v2` có `data` chứa scenario ID (type=scenario)
7. Xoá `action_detail` có `data.id` = scenario ID (type=scenario)

#### Response (200 OK)
```json
{ "redirect_uri": "/basic/scenario", "folderId": 0 }
```

---

### EP-08: GET /scenario-users — Danh sách LINE user theo scenario/step
**Controller**: `Basic\ScenarioController@getListFriendByScenarioId`
**Mô tả**: Trả về view danh sách LINE user đang/đã đăng ký vào scenario, hoặc đã nhận một step cụ thể.

#### Query Params
| Param | Mô tả |
|-------|-------|
| `scenarioId` | ID scenario |
| `stepId` | ID step (nếu có → lấy user đã nhận step đó) |
| `senderID` | ID sender (nếu có → lấy user theo tin nhắn) |
| `userCount` | `'start'` hoặc `'stop'` — loại thống kê |
| `page` | Trang (phân trang) |
| `type_data` | Thêm filter (tuỳ chọn) |

#### Response
View: `basic.scenario.list_friend_user`
- `type`: 0=danh sách bạn, 1=đã nhận step, 3=đã xem tin
- `total`, `page`, `currentPage`: phân trang
- `data`: mảng LINE user

---

### EP-09: POST /basic/scenario-check-delete — Kiểm tra trước khi xoá
**Controller**: `Basic\ScenarioController@scenarioCheckDelete`

#### Request Body
| Field | Type | Mô tả |
|-------|------|-------|
| `scenario_id` | int | ID scenario cần kiểm tra |

#### Response (200 OK)
```json
{ "result": true }
```

---

### EP-10: GET /basic/scenario/copy/{scenario} — Copy scenario
**Controller**: `Basic\ScenarioController@copyScenario`
**Auth Request**: `OwnerGetScenario`
**Mô tả**: Nhân bản toàn bộ scenario bao gồm step messages, templates, filters, actions.

#### Query Params
| Param | Mô tả |
|-------|-------|
| `scenarioId` | ID scenario nguồn |
| `next_scenario` | ID next scenario cho bản copy |

#### Logic copy
1. Tạo Scenario mới với tên `{tên cũ}のコピー`
2. Copy toàn bộ `FilterManager` và `FilterV2` liên kết
3. Với mỗi `StepMessage`: clone templates (nếu `category_id < 0`), clone Actions, clone FilterManager mapping
4. Tạo `TemplateMappingTable` cho mỗi template mới

#### Response (200 OK)
```json
{ "status": true, "scenario_id": 456 }
```

---

### EP-12: GET /step-message/list-message/{scenario} — Trang danh sách step message (view cũ)
**Controller**: `Basic\StepMessageController@listMessage`
**Auth Request**: `OwnerGetScenario`

View: `basic.step_message.index_v2`
Dữ liệu truyền: `scenario`, `scenarioId`, `categories`, `scenarioFilter`, `conversion`, `statusObject`, `richMenus`

---

### EP-13: GET /step-message/scenario-message/{scenario} — Trang thiết kế step scenario
**Controller**: `Basic\StepMessageController@scenarioMessage`
**Auth Request**: `OwnerGetScenario`
**Mô tả**: Trang chính để thiết kế timeline các step và quản lý message.

View: `basic.step_message.scenario_message`
Kiểm tra alert thêm step/message: `SettingAlert::checkExistsKey('add_step')`, `checkExistsKey('add_message')`
Truyền thêm: `checkExistsAlertMessage`, `checkExistsAlertStep`, `categoryOfScenNext`, `next_scen_name`

---

### EP-14: GET /step-message/preview-scenario-message/{scenario} — Preview
**Controller**: `Basic\StepMessageController@previewScenarioMessage`
View: `basic.step_message.preview_scenario_message`
Logic tương tự EP-13.

---

### EP-15: GET /step-message/create/{scenario}/{scenario_step_id} — Form tạo message
**Controller**: `Basic\StepMessageController@create`
**Auth Request**: `OwnerGetScenario`
**Mô tả**: Form tạo template content cho một step. Hỗ trợ action `clone_template` để nhân bản template group.

View: `basic.step_message.create`
Dữ liệu truyền: `ownScenario`, `scenario`, `categories`, `categoriesSelect`, `stickers`, `stickerPackage`, `groups_template`, `items_template`, `items_template_default`, `richMenus`, `tags`, `events`, `categoryFriendIfo`, `friendInfoDefault`, `liff_id`

---

### EP-16: GET /step-message/edit/{step_message}/{template_id} — Form sửa message
**Controller**: `Basic\StepMessageController@edit`
**Mô tả**: Form chỉnh sửa template đã có của một step.

View: `basic.step_message.create` (cùng view với create, action='edit')

---

### EP-17: GET /step-message-template-child/{scenarioId}/{stepId}/{templateId} — Template con
**Controller**: `Basic\StepMessageController@templateChildStep`
**Mô tả**: Hiển thị danh sách template con bên trong một group template của step.

View: `basic.step_message.v2.list-template-child`
- Đọc `template.content` (danh sách template ID cách nhau bởi dấu phẩy)
- Load từng template con với relationships: `btn_template`, `introduction`, `location`, `buttons`

---

### EP-18: POST /basic/step-message/store/{scenario} — Lưu nội dung message
**Controller**: `Basic\StepMessageController@store`
**Auth Request**: `OwnerGetScenario`
**Mô tả**: Tạo template mới và gắn vào step message. Hỗ trợ tester mode (gửi thử trực tiếp không lưu).

#### Request Body (multipart/form-data)
| Field | Mô tả |
|-------|-------|
| `scenario_step_id` | ID step cần gắn message |
| `botIdCurrent` | Bot ID xác nhận chéo |
| `tmp_type[]` | Mảng loại template: `text`, `image`, `voice`, `video`, `form`, `group`, `stamp`, `question`, `location`, `introduction` |
| `tmp_content[]` | Nội dung text tương ứng |
| `tmp_is_shorten_url[]` | Rút gọn URL hay không |
| `template_id` | Template ID clone nếu có |
| `is_tester` | Nếu có và không phải `'undefined'`: chế độ gửi thử |
| `tester_ids` | Danh sách line_user_id gửi thử |
| `rich_menu_id` | Rich menu ID đính kèm |
| `tmp_media[]` | File upload (hình ảnh, voice, video) |
| `action_image_map[]` | Cài đặt vùng image map (JSON) |
| `urls_detect[]` | URL phát hiện trong text (JSON) |

#### Logic
1. Với mỗi `tmp_type[key]`: tạo template mới trong bảng `template` (`category_id = -111`)
2. Cập nhật `step_message.template_ids` (nối thêm ID mới, phân cách bởi dấu phẩy)
3. Tạo `template_mapping_table` cho mỗi template mới
4. Nếu tester mode: gửi tin nhắn thử qua `ChatHelper::tester()`, không lưu vào template_ids

#### Response (200 OK — lưu thành công)
```json
{ "success": true, "error": "", "message": "", "redirect_uri": "/step-message/list-message/{scenario}" }
```

#### Response (200 OK — gửi thử thành công)
```json
{ "success": true, "error": "", "message": "メッセージが送信されました。", "redirect_uri": "" }
```

---

### EP-20: POST /step-message/save-selected-profile-bot — Chọn profile gửi
**Controller**: `Basic\StepMessageController@saveSelectedProfileBot`
**Mô tả**: Chọn profile bot (tên/avatar) sẽ hiển thị khi gửi message của step.

#### Request Body
| Field | Mô tả |
|-------|-------|
| `id_profile_bot` | ID profile bot muốn chọn |
| `step_message_id` | ID step message |

#### Logic
- Nếu profile chọn là `is_default = 1` → set `step_message.profile_id = null` (dùng profile mặc định)
- Ngược lại → set `step_message.profile_id = id_profile_bot`

---

### EP-21: POST /save-data-scenario — Lưu tên/folder/next scenario
**Controller**: `Basic\StepMessageController@saveDataScenario`
**Mô tả**: Lưu nhanh thông tin cơ bản của scenario từ trang thiết kế step.

#### Request Body
| Field | Mô tả |
|-------|-------|
| `scenario_id` | ID scenario |
| `name` | Tên mới |
| `group_id` | ID folder |
| `after_scenario_id_1` | ID scenario tiếp theo |

---

### EP-22: POST /mark-close-alert — Đánh dấu đã xem alert
**Controller**: `Basic\StepMessageController@markCloseAlert`

#### Request Body
| Field | Mô tả |
|-------|-------|
| `key` | Key alert: `'add_step'` hoặc `'add_message'` |

#### Logic
Tạo bản ghi `setting_alert` với `user_id` hiện tại và `key`.

---

### EP-23: POST /add-friend/update-setting-message — Cập nhật tin nhắn add friend
**Controller**: `Basic\ScenarioController@updateSettingMessage`
**Mô tả**: Cập nhật (hoặc tạo mới) template tin nhắn gửi cho bạn mới/cũ khi add friend.

#### Request Body
| Field | Mô tả |
|-------|-------|
| `typeSetting` | `'new'` hoặc `'old'` |
| `botIdCurrent` | Bot ID xác nhận chéo |
| `flagMsgSetting` | Số lượng messages: 1, 2, hoặc 3 |
| `tmp_type[]` | Mảng loại template |
| `tmp_content[]` | Nội dung |
| `tmp_is_shorten_url[]` | Rút gọn URL |
| `template_id`, `template_id_2`, `template_id_3` | ID template hiện có (nếu update) |
| `ids` | Danh sách line_user_id gửi thử |

#### Logic
- Nếu template đã tồn tại → `handlerUpdateTemplate()` → update
- Nếu chưa có → `handlerCreateTemplate()` → tạo mới
- Lưu JSON `{template_id, template_id_2, template_id_3}` vào `add_friend_setting.sent_templates_new_friend` hoặc `sent_templates_old_friend`

---

### EP-26: POST /update-setting-add-friend — Cài đặt action add friend
**Controller**: `Basic\ScenarioController@updateSettingAddFriend`
**Mô tả**: Cập nhật action (action_new_id, action_old_id) được thực thi khi người dùng thêm bot vào LINE.

#### Request Body
| Field | Mô tả |
|-------|-------|
| `botIdCurrent` | Bot ID xác nhận chéo |
| `action_new_id` | ID action cho bạn mới |
| `action_old_id` | ID action cho bạn cũ |

---

## Các AJAX endpoints bổ sung (phát hiện trong code, không có trong danh sách route ban đầu)

| Method | URL (dự đoán) | Controller@Method | Mô tả |
|--------|--------------|-------------------|-------|
| POST | /basic/scenario/ajax-get-list | ScenarioController@ajaxGetListScenario | Lấy danh sách scenario + thao tác sort/delete/move/folder AJAX |
| POST | /basic/scenario/ajax-get-all | ScenarioController@ajaxGetAllListScenario | Lấy tất cả scenario trong folder |
| POST | /basic/scenario/create-step | ScenarioController@createScenarioStep | Tạo/update step trong scenario |
| POST | /basic/scenario/delete-step | ScenarioController@deleteScenarioStep | Xoá một step |
| POST | /basic/scenario/save-sort | ScenarioController@saveSortStepMessage | Lưu thứ tự template trong step |
| POST | /step-message/ajax-get-list-v2 | StepMessageController@ajaxGetListStepMessageV2 | Lấy danh sách step messages (JSON) |
| POST | /step-message/get-list-v3 | StepMessageController@getListStepMessageV3 | Lấy step messages v3 (có filter, phân trang) |
| POST | /step-message/delete | StepMessageController@deleteStepMessage | Xoá một message khỏi step |
| POST | /step-message/create-by-template | StepMessageController@createStepMessageByTemplate | Thêm template vào step từ thư viện |
| POST | /step-message/clone-by-template | StepMessageController@cloneStepMessageByTemplate | Clone template vào step |
| POST | /step-message/save-setting-richmenu | StepMessageController@saveSettingRichmenu | Gán rich menu cho step |
| POST | /step-message/ajax-list-tag-filter | StepMessageController@ajaxListTagFilter | Lấy danh sách tag để filter |
| POST | /step-message/save-filter-tag | StepMessageController@saveFilterTag | Lưu filter tag cho step |
| POST | /step-message/send-test | StepMessageController@ajaxSendStepMessageTest | Gửi test step message |
| POST | /step-message/send-test-v3 | StepMessageController@sendStepMessageTestV3 | Gửi test step message (v3) |
| GET | /step-message/get-selected-tags | StepMessageController@getSelectedTags | Lấy tag đã chọn cho step |
| POST | /step-message/save-common | StepMessageController@saveCommonStepMessage | Lưu filter chung cho scenario |
| POST | /step-message/delete-filter | StepMessageController@deleteFilterManager | Xoá filter manager và cascade |
| POST | /step-message/get-preview-filter | StepMessageController@getDataPreviewFilter | Preview filter đang áp dụng |
| POST | /step-message/get-profiles | StepMessageController@ajaxGetProfileOfBots | Lấy danh sách profile bot |
| POST | /step-message/init-data-v2 | StepMessageController@initDataV2 | Khởi tạo data trang scenario-message |
| POST | /step-message/save-template-child-sort | StepMessageController@saveSortTemplateChild | Lưu thứ tự template con |
| POST | /step-message/delete-template-child | StepMessageController@deleteTemplateChild | Xoá template con khỏi group |
| GET | /step-message/get-list-by-category | StepMessageController@getListScenarioByCategory | Lấy scenario theo folder |
