# FA-011 — Logic Spec: Tạo biểu mẫu「フォーム作成」

## Controllers

### FormAnswerController (Basic)

- **File**: `app/Http/Controllers/Basic/FormAnswerController.php`
- **Namespace**: `App\Http\Controllers\Basic`
- **Dependencies (inject qua constructor)**:
  - `TemplateService`
  - `MessageService`
  - `BotRepositoryInterface`
  - `MessageV2RepositoryInterface`
  - `FormAnswerSettingCommonService`
  - `FormAnswerService`
  - `ConversationRepositoryInterface`
  - `LineUserRepositoryInterface`
  - `BotLineUserRepositoryInterface`

#### Phương thức chính

##### `index_v3(Request $request)` — line 184
- Lấy bot hiện tại; kiểm tra plan; lấy Google Sheet auth URL nếu chưa kết nối
- Đọc cookie `folder_form_answer` để xác định thư mục active (key = bot_id)
- Nếu cookie không hợp lệ (folder bị xóa) → reset về `0` (未分類)
- Truyền vào view: `flagNewFreePlan`, `formAnswerNumber`, `google_sheet_auth_url`, `list_folder`, `folderId`

##### `editV3(Request $request)` — line 734
- Tải form theo `id` và `bot_id`
- Tải `FormAnswerSettingCommon` (hoặc tạo mới nếu chưa có)
- Tải `FormAnswerDetails` và `FormAnswerPage` (sắp xếp theo page_number)
- Xử lý `makeDataEditV3()` cho từng item:
  - Tạo `idTmp` để frontend dùng (tránh dùng id thật)
  - Gán thông tin button/page mặc định từ settingCommon nếu page chưa có giá trị riêng
- Xử lý `next_page_setting` cho form phân nhánh: mapping từ `form_detail_id` → `idTmp`
- Gán `detail_actions_open` và `detail_actions_reply` (từ `action_open_id`, `action_reply_id`)
- **Business rule**: Nếu không có trang nào → tạo trang ảo (スタートページ) từ data cũ

##### `storeV3(Request $request)` — line 6928
- **Validation**: BackupHistory check + Free plan limit (≤ 3 forms)
- **Tạo form**:
  - `unique_key`: 6 ký tự random, đệ quy kiểm tra unique (`randomFormCodeRecursion()`)
  - Insert vào bảng `form_answer` với defaults:
    - `color = #08BF5A`
    - `bg_color_button = #EDF4FB`, `text_color_button = #5799DB`
    - `reply_kind = 0` (cho phép trả lời nhiều lần)
    - `reply_use_url = 2`
    - `message_reply_success = "{name}様 \n\n回答を受け付けました。"`
    - `reply_text = "あなたがこのフォームに回答できる上限に達しました。"`
    - `position` = max position hiện có + 1
  - Cập nhật `notify_setting.answer_form` nếu `is_all_form_new=1`
  - Gọi `saveDefaultSettingCommon($form_id)` → tạo `form_answer_setting_common`
  - Tạo `form_answer_page` đầu tiên (スタートページ, `next_page_type=3`)
  - Nếu có `attr`: tạo `form_answer_details` với validation rules (email, kana, tel, numeric)

##### `saveV3(Request $request)` — line 1242
- **DB Transaction**
- Cập nhật `form_answer.group_id` và `using_old_version=0`
- Upsert `form_answer_setting`
- Với mỗi page trong `pages`:
  - Xử lý `next_page_setting` (form phân nhánh): mapping label → pageId
  - Upsert `form_answer_page`
  - Với mỗi form item:
    - Upload ảnh base64 nếu cần (`uploadImageBase64()`)
    - Upsert `form_answer_details` với đầy đủ thuộc tính
    - **Nếu `is_link_friend_info=1`**: upsert `friend_information_setting` và `friend_info_option_selects`
    - **Nếu item thay đổi option**: xóa `FriendInformationValue` và `FriendInfoOptionSelects` không còn dùng
  - Cập nhật `next_page_form_detail_id` cho page sau khi có ID thực
- Gọi `deleteOptionItemRemind()` cho remind items đã xóa
- **Side effect**: Nếu bot có Google token và form chưa có sheet → tạo Google Spreadsheet

##### `showFormResultV3(Request $request, int $id)` — line 4534
- GET: Render view
- POST (AJAX):
  - Query `form_answer_result` với filter ngày, phân trang
  - Với mỗi result: gán `view_name`, `name`, tính `point` từ `diagnostic_content` items
  - Xử lý hiển thị datetime (nhiều format: year/month/day hoặc date string)
  - Lấy `dataRemind` từ `form_answer_item_remind`

##### `ajaxGetFormAnswerListV3(Request $request)` — line 3462
- Xử lý `action=deleteItem`: Cascade soft-delete form + tất cả bảng con
  - Bảng bị xóa: `form_answer_details`, `form_answer_result` (force delete), `form_answer_setting`, `form_answer_page`, `form_answer_setting_common`, `form_answer_point_setting`, `form_answer_user_accept`
  - Xóa event steps, reset rich menu items
  - Ghi `user_id_del = Auth::id()`
- Xử lý `action=sortFolder`: cập nhật `position` trong `form_answer_folder`
- Trả về danh sách form (paginate 20) kèm danh sách folder với count

##### `googleSheetActive()` — line 7184
- Kiểm tra `bots.google_sheet_access_token` và `bots.google_sheet_status`
- Trả về `active: true/false` và URL re-connect nếu cần

##### `restoreFormAnswer(int $id)` — line 7328
- **DB Transaction**
- Kiểm tra giới hạn plan miễn phí trước khi restore
- Restore: `form_answer` + tất cả bảng liên quan + `form_answer_folder`

---

## Services

### FormAnswerService

- **File**: `app/Services/FormAnswer/FormAnswerService.php`
- **Dependencies**: `FormAnswerRepository`, `BotRepository`, `FormAnswerSettingCommonRepository`, `FormAnswerPageRepository`, `MessageService`, `TemplateService`, `FormAnswerDetailRepository`

#### Phương thức chính

##### `renderFormAnswer($request)` — line 84
- Tìm form theo `unique_key`
- Kiểm tra hạn hợp đồng bot (expired_date + 7 ngày)
- Decode `line_id` từ Hashids `user_link` connection
- Kiểm tra giới hạn trả lời (`reply_kind`): 0 = nhiều lần, 1 = 1 lần, 2 = giới hạn số lần
- Gọi `renderFormDetail()` cho từng trang
- Xử lý countdown timer

##### `storeRenderForm($request)` — line 767 (thực tế trong service)
- Xác thực LINE user (Hashids decode hoặc line_id thô)
- Kiểm tra `conversation` tồn tại (người dùng phải là bạn bot)
- Tính `duration_time_reply` từ `date_open_form`
- Xử lý từng item trong `frm`:
  - Text input → cập nhật `line_user` hoặc `friend_information_value`
  - Checkbox/radio → gắn tag
  - Datetime → xử lý format
  - File upload → lưu file
- Insert `form_answer_result` với `data` JSON
- Gọi `sendActionAfterReply()` → gửi action + message
- Gọi `sendActionPoint()` nếu có diagnostic content
- Push mobile notify

##### `sendActionAfterReply()` — line 1939
- Kiểm tra `action_reply_type`:
  - `1` (1 lần): chỉ gửi nếu `count_reply=0`
  - Khác: gửi mỗi lần
- Gọi `sendMessageReply()`, `genMessage()`, `sendAction()`

##### `genMessage()` — line 1961
- Nếu `is_send_gen_message=1`: tạo nội dung tin nhắn Q&A copy từ data câu trả lời
- Xử lý các loại value: address (map), datetime, file URL, text

##### `addActionRemind()` — line 2085
- Tạo `form_answer_item_remind` cho remind items
- Gắn event step time

### FormAnswerSettingCommonService

- **File**: `app/Services/FormAnswer/FormAnswerSettingCommonService.php`

#### `saveDefaultSettingCommon($formId)` — line 355
- Tạo `form_answer_setting_common` với defaults:
  - Background color: `#FFFFFF`
  - Button pattern, color, font-weight, shadow defaults
  - Heading/divider defaults

#### `saveFormAnswerSettingCommon($request)` — line 33
- Xử lý upload ảnh header (file hoặc base64)
- Upsert `form_answer_setting_common`
- Áp dụng setting common cho tất cả pages nếu được chọn

---

## Models

### FormAnswer

- **File**: `app/FormAnswer.php`
- **Table**: `form_answer`
- **Traits**: `SoftDeletes`
- **Relationships**:
  - `form_details()`: hasMany `FormAnswerDetails` (form_id)
  - `pages()`: hasMany `FormAnswerPage` (form_id)
  - `setting_common()`: belongsTo `FormAnswerSettingCommon` (id → form_id)
- **Accessors**:
  - `getCreatedAtAttribute()`: format `Y.m.d`
  - `getSettingPageConfirmAttribute()`: decode JSON hoặc trả về default từ `setting_common`
- **Static**: `changeFormAnswersToNewBot()`, `getNameById()`

### FormAnswerPage

- **File**: `app/FormAnswerPage.php`
- **Table**: `form_answer_page`
- **Traits**: `SoftDeletes`
- **Constants**:
  - `NEXT_PAGE_TYPE_SETTING = 2` (phân nhánh theo câu trả lời)
  - `NEXT_PAGE_TYPE_END_FORM = 3` (kết thúc form)

### FormAnswerDetails

- **File**: `app/FormAnswerDetails.php`
- **Table**: `form_answer_details`
- **Traits**: `SoftDeletes`
- **Các trường quan trọng**:
  - `type`: loại item (text_8, date_time, select_1, checkbox, upload_file, event_1, diagnostic_content, v.v.)
  - `name`: tên định danh (short_name, phone, email, address, diagnostic_content, event_1...)
  - `rules`: JSON `{"required": true/false, "email": true, "regex": "pattern"...}`
  - `settings`: JSON cấu hình selectable/optionable
  - `page_id`: FK → form_answer_page
  - `friend_info_id`: FK → friend_information_setting (hoặc -1 đến -6 cho system fields)
  - `in_tag`: 1 = kết quả gắn tag
  - `in_tag_and_friend`: gắn tag và ghi vào friend info
  - `is_link_friend_info`: 1 = tạo/cập nhật friend_information_setting
  - `is_display_info_friend`: 1 = hiển thị giá trị bạn bè đã có

### FormAnswerResult

- **File**: `app/FormAnswerResult.php`
- **Table**: `form_answer_result`
- **Traits**: `SoftDeletes`
- **Trường quan trọng**:
  - `data`: JSON array các câu trả lời `[{type, name, value, point...}]`
  - `line_id`: FK → line_user.id
  - `duration_time_reply`: thời gian hoàn thành form (format MM:SS)
  - `status_sync_sheet`: 0 = chưa sync Google Sheets, 1 = đã sync

### FormAnswerSetting

- **File**: `app/FormAnswerSetting.php`
- **Table**: `form_answer_setting`
- **Traits**: `SoftDeletes`
- **Cài đặt**: `tag_id`, `template_id`, `scenario_id`, `scenario_start_day`, `scenario_start_time`
- Quan hệ: 1 form → 1 setting (upsert theo `form_id`)

### FormAnswerSettingCommon

- **File**: `app/FormAnswerSettingCommon.php`
- **Table**: `form_answer_setting_common`
- **Traits**: `SoftDeletes`
- Lưu cài đặt thiết kế: `image_header`, `bg_color`, `button_pattern`, `button_color`, `button_bg_color`, `button_font_weight`, `button_shadow`, v.v.

### FormAnswerFolder

- **File**: `app/FormAnswerFolder.php`
- **Table**: `form_answer_folder`
- **Traits**: `SoftDeletes`
- **Trường**: `bot_id`, `name`, `position`

### FormAnswerPointSetting

- **File**: `app/FormAnswerPointSetting.php`
- **Table**: `form_answer_point_setting`
- **Traits**: `SoftDeletes`
- Lưu cài đặt điểm cho diagnostic content

### FormAnswerUserAccept

- **File**: `app/FormAnswerUserAccept.php`
- **Table**: `form_answer_user_accept`
- **Traits**: `SoftDeletes`
- **Trường**: `line_user_id`, `form_id`, `count_reply`, `is_update`
- Theo dõi số lần trả lời của từng LINE user với từng form

### FormAnswerItemRemind

- **File**: `app/FormAnswerItemRemind.php`
- **Table**: `form_answer_item_remind`
- **Traits**: `SoftDeletes`
- Lưu thông tin nhắc lịch liên kết với câu trả lời form

### FormAnswerConnectGoogle

- **File**: `app/FormAnswerConnectGoogle.php`
- **Table**: `form_answer_connect_google`
- **Trạng thái**: `STATUS['PROCESSING']`, `STATUS['WAITING']`, `STATUS['ERROR']`
- Lưu queue kết nối Google Sheets: `bot_id`, `form_id`, `name`, `status`, `retry_error`

---

## Jobs (Background)

### AddResultFormAnswerToGoogleSpreadSheet

- **File**: `app/Jobs/AddResultFormAnswerToGoogleSpreadSheet.php`
- **Implements**: `ShouldQueue`
- **Queue**: `googleFormAnswer` (connection: `database`)
- **Mục đích**: Ghi kết quả câu trả lời form vào Google Spreadsheet
- **Lưu ý**: Hiện tại đã bị comment out trong code (`FormAnswerService.php:1515`). Google Sheets sync có thể đang được xử lý theo cơ chế khác (qua `form_answer_connect_google` table và `ResultErrorGoogle`).
- **Mức độ tin cậy**: **Trung bình** (job tồn tại nhưng dispatch bị comment)

---

## Business Rules

### 1. Giới hạn plan miễn phí
- Free plan: tối đa 3 form active
- Kiểm tra tại `storeV3()` và `restoreFormAnswer()`
- `checkPlanFreeBotLimitFeature($bot)` → trả về `1` nếu đang dùng gói giới hạn

### 2. Unique key của form
- 6 ký tự random từ `randomFormCodeRecursion()` (line 6676)
- Đệ quy kiểm tra unique trong bảng `form_answer`
- Dùng cho URL công khai: `/basic/form-answer/form-render-v3/{unique_key}`

### 3. Trả lời form
- `reply_kind = 0`: cho phép trả lời nhiều lần
- `reply_kind = 1`: chỉ 1 lần (kiểm tra qua `form_answer_result` count)
- `reply_kind = 2`: giới hạn số lần (xem `FormAnswerUserAccept`)
- Khi `reply_kind=1` và user đã trả lời → response `"status": "false_reply_kind"` kèm `message` (`reply_text`)

### 4. Điều kiện là bạn bè
- Khi submit form, user phải có `conversation` với bot (`conversation.tb_line_user_id`, `bot_id`, `is_blocked=0`)
- Nếu chưa phải bạn bè → response `"status": "false_friend"` kèm `msg = bot.url_add_friend`

### 5. Ghi thông tin bạn bè khi submit
- Nếu câu hỏi có `friend_info_id`:
  - `-1`: cập nhật `line_user.view_name`
  - `-2`: cập nhật `line_user.phone_number`
  - `-3`: cập nhật `line_user.email`
  - `-6`: cập nhật `line_user.province`
  - ID dương: cập nhật `friend_information_value`
- Trigger `SyncElasticsearch` khi cập nhật `view_name`

### 6. Backup lock
- Khi bot đang trong quá trình backup (`BackupHistory.status IN (0, 1)`)
- Các thao tác tạo/sửa/xóa form bị từ chối với `MESSAGE_NOTIFY_BACKUP`

### 7. Soft delete form
- Form bị xóa không bị xóa vật lý ngay
- Sau **90 ngày** kể từ `deleted_at` → tự động xóa vật lý (theo UI spec)
- Khi soft-delete: `user_id_del` ghi lại người xóa, `count_user_reply` reset về 0

### 8. Google Sheets integration
- Mỗi form có thể được kết nối với 1 Google Spreadsheet (`form_answer.google_sheet_id`)
- Khi tạo form mới: nếu bot đã kết nối Google → tự động tạo sheet mới
- Khi token hết hạn: tự động refresh token qua `refresh_token`
- `form_answer_connect_google` theo dõi trạng thái đồng bộ từng form
- `ResultErrorGoogle` ghi lại lỗi đồng bộ với retry logic

### 9. Using old version
- `form_answer.using_old_version = 1`: form dùng UI cũ (v1/v2)
- `using_old_version = 0`: form dùng UI mới (v3)
- Khi lưu bất kỳ thay đổi nào qua v3 API → set `using_old_version=0`
- Khi preview form v1 nhưng `using_old_version=0` → redirect sang v3

### 10. Form phân nhánh (分岐タイプ)
- `form_type = 2` (分岐)
- Mỗi trang có `next_page_type`:
  - `2 = NEXT_PAGE_TYPE_SETTING`: phân nhánh theo câu trả lời của `next_page_form_detail_id`
  - `3 = NEXT_PAGE_TYPE_END_FORM`: kết thúc form
- `next_page_setting`: JSON array `[{value: "label", pageId: N}]` mapping option → trang tiếp
- Khi lưu: rebuild `next_page_setting` từ danh sách option hiện tại (đảm bảo nhất quán)

### 11. Validation rules câu hỏi
- `rules` JSON trong `form_answer_details`:
  - `required: true/false`
  - `email: true` (kiểu email)
  - `regex_kana: "^[ァ-ヶー　 ]+"` (katakana)
  - `regex: "^[0-9]{10,12}"` (số điện thoại)
  - `numeric: true`

### 12. Form item với link friend info
- Khi `is_link_friend_info=1` và `friend_info_type` xác định:
  - Tạo/cập nhật `friend_information_setting` cho bot
  - Nếu loại select (`type_data=1`): upsert `friend_info_option_selects`, dọn dẹp options cũ
  - Cập nhật `total_user_has_value` trong `friend_information_setting`

---

## Phụ thuộc ngoài

### Google Sheets API
- **Service**: `app/Helpers/GoogleSheetService.php`
- **Thư viện**: Google API Client (PHP)
- **Scopes**: `spreadsheets`, `userinfo.profile`, `userinfo.email`
- **Luồng OAuth**:
  1. GET `/basic/redirect-google-sheet` (sau khi user cho phép)
  2. Controller: `redirectUriGoogleSheet()` — lưu access token vào `bots.google_sheet_access_token`
  3. Tạo `FormAnswerConnectGoogle` records để sync các form hiện có

### LINE API
- Gửi tin nhắn sau khi submit form qua `MessageService`
- Gửi action (tag, step message, template...) qua `sendAction()` helper

### Hashids
- Encode/decode LINE user ID cho URL công khai
- Connection: `user_link`
- Dùng để bảo vệ line_user.id không bị lộ trong URL
