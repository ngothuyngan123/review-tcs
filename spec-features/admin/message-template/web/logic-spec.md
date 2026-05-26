# Logic Spec — FA-010 Mẫu tin nhắn「テンプレート」

> **Mã tính năng:** FA-010
> **Ngày tạo:** 2026-03-26
> **Nguồn:** Source code Laravel — `MessageTemplateController.php` (4579 dòng), `TemplateV2Controller.php` (1484 dòng), `TemplateV2Service.php`, `Template.php`
> **Tin cậy chung:** **Cao** (đọc trực tiếp từ source code)

---

## 1. Controllers & Actions

### 1.1. MessageTemplateController (Legacy)

**File:** `app/Http/Controllers/Basic/MessageTemplateController.php` (4579 dòng)
**Namespace:** `App\Http\Controllers\Basic`

Đây là controller gốc xử lý toàn bộ CRUD template, quản lý folder, park template, media library, và image map. Không sử dụng Service layer — logic xử lý trực tiếp trong controller. **[Cao]**

#### Các method chính:

| Method | Dòng | Chức năng | Side Effects |
|--------|------|-----------|-------------|
| `index()` | :99 | Hiển thị danh sách template. Đọc folder từ cookie, load categories, trả view | Cookie read |
| `create()` | :142 | Hiển thị form tạo template mới. Load stickers, categories, scenarios, tags, events, rich menus, friend info | — |
| `store()` | :337 | Lưu template mới. Xử lý theo type (text/stamp/image/video/voice/form/question/location/introduction) | DB insert template, upload media, tạo URL tracking, tạo buttons/image map |
| `edit()` | :2101 | Hiển thị form sửa template. Load template + tất cả dữ liệu liên quan | — |
| `save()` | :2382 | Cập nhật template có sẵn. Reset relationships cũ → tạo lại theo dữ liệu mới | DB update, delete+recreate relationships |
| `ajaxInitTemplate()` | :2806 | Endpoint đa năng cho danh sách: CRUD folder, delete/move/sort template | DB CRUD category + template |
| `ajaxDelTemplate()` | :3134 | Xoá template (hard delete) + cascade xoá template con nếu type=group | DB delete template, send_random_message, template_mapping_tables |
| `copyTemplate()` | :4358 | Deep clone template via `cloneTemplate()` | DB insert (recursive) |
| `cloneTemplate()` | :4400 | Deep clone gồm: template, url_redirect, image_map, question, location, introduction, buttons. Group → clone đệ quy con | DB insert multiple tables |
| `getById()` | :3584 | Lấy chi tiết 1 template (JSON) với buttons, actions, open URL data | — |
| `createPark()` | :230 | Trang tạo/sửa park template | — |
| `ajaxUpdateOrCreatePark()` | :261 | Tạo hoặc cập nhật park template (type=group) | DB insert/update template |
| `showPark()` | :307 | Hiển thị nội dung park template | — |
| `ajaxInitParkTemplate()` | :3192 | Thao tác trên park: deleteItem, sortItem | DB delete/update template |
| `ajaxAddTemplatePark()` | :3254 | Clone template rồi thêm vào park (append ID vào content) | DB insert (deep clone) |
| `deleteTemplateInGroup()` | :4294 | Xoá template con khỏi group (xoá khỏi content + hard delete) | DB delete, update parent content |
| `getListTemplateChild()` | :4245 | Lấy danh sách template con của group (theo content IDs) | — |
| `getListTemplateSort()` | :3120 | Lấy danh sách template cho sắp xếp | — |
| `ajaxGetVideoLibrary()` | :3482 | Lấy thư viện video (paginate) | — |
| `ajaxGetVoiceLibrary()` | — | Lấy thư viện âm thanh | — |
| `ajaxGetImageLibrary()` | — | Lấy thư viện ảnh | — |
| `ajaxGetPdfLibrary()` | — | Lấy thư viện PDF | — |
| `ajaxChangeThumbHistory()` | :3426 | Đổi thumbnail video — upload file mới, resize 240x240 | File upload, DB update media |
| `initDataImageMap()` | :3824 | Lấy data image map: items, forms, products, bookings, scripts, conversions | — |
| `getDataPreviewAction()` | :3940 | Lấy preview actions trên image map | — |
| `getDataOpenUrl()` | :3786 | Lấy entities theo loại URL: FormAnswer, SItems, BEventDetail, SiteScript, Conversion, BookingCalendar | — |
| `ajaxGetListUrlRedirect()` | :2591 (legacy) | Lấy danh sách URL redirect với actions | — |
| `templatesDetail()` | :74 | Xem chi tiết template (view page) — nếu type=group, lấy từng template con | — |
| `deletedDataTemplate()` | :3774 | Dọn dẹp action_detail khi xoá template | DB delete ActionDetail |
| `resetRelationShipTemplate()` | :2765 | Xoá relationships cũ trước khi update (image_map, question, location, introduction, form buttons) | DB delete |
| `cloneMutilpleAction()` | :3910 | Clone action + action_details + filters | DB insert |

### 1.2. TemplateV2Controller (Mới)

**File:** `app/Http/Controllers/Basic/TemplateV2Controller.php` (1484 dòng)
**Namespace:** `App\Http\Controllers\Basic`
**Injected Services:** `TemplateV2Service`, `TemplateService`

Controller mới hơn, sử dụng Service layer cho logic phức tạp. Xử lý editor V2 (text, panel/button, media, stamp, location) và các tính năng mới (group template, delay message, quick reply). **[Cao]**

#### Các method chính:

| Method | Dòng | Chức năng | Side Effects |
|--------|------|-----------|-------------|
| `createMessage()` | :68 | Trang tạo message (V2 editor). Load forms, friend info, stickers, status objects | — |
| `createTemplate()` | :384 | Trang tạo/sửa template V2. Hỗ trợ context từ broadcast, scenario, event | — |
| `saveTemplate()` | :503 | Lưu template V2. Delegate sang `TemplateV2Service@saveTemplateByType()` | DB qua service |
| `createGroupTemplate()` | :705 | Trang tạo/sửa group template | — |
| `ajaxCreateGroup()` | :736 | Tạo/cập nhật group template. Delegate sang `TemplateV2Service@createTemplateGroup()` | DB insert/update |
| `edit()` | :577 | Sửa template — load full data, hỗ trợ clone (copy flag) | Clone actions nếu copy |
| `getDataText()` | :180 | Lấy data editor text: template content, friend info (basic, address, custom), LIFF ID | — |
| `getDataStamp()` | :312 | Lấy data editor sticker: sticker packages + selected content | — |
| `getDataLocation()` | :337 | Lấy data editor location: lat, lng, address | — |
| `getDataIntroduction()` | :997 | Lấy data editor introduction: template + tmp_introduction | — |
| `initDataButton()` | :129 | Lấy data khởi tạo Panel/Button: post_back types, reply methods, open URL types, friend info | — |
| `initDataMedia()` | :147 | Lấy data khởi tạo Media: post_back types, image map data | — |
| `initDataOpenUrl()` | :162 | Lấy data open URL theo type | — |
| `getDataPreview()` | :1021 | Lấy preview template via service | — |
| `getDataPreviewTemplateChild()` | :1308 | Lấy preview template con via service | — |
| `sendTestTemplate()` | :1050 | Gửi test template đến LINE user testers. Xử lý group (gửi lần lượt hoặc batch 5), delay message | LINE API call, DB update free_send_count, tạo SendRandomMessage |
| `sendTestTemplateV3()` | :1246 | Gửi test V3, delegate sang `TemplateService@sendTestTemplate()` | LINE API call |
| `updateDelayMessage()` | :1253 | Bật/tắt delay message (is_delay_message: 0/1) | DB update template |
| `saveSortTemplateChild()` | :1266 | Sắp xếp template con trong group (update position + content) | DB update template, step_message |
| `deleteMultipleTemplateChild()` | :1319 | Xoá nhiều template con. Update parent content, xoá send_random_message | DB delete + update |
| `ajaxInitListLineUserData()` | :1358 | Lấy danh sách LINE user tester (is_tester=1, is_blocked=0) | — |
| `ajaxSearchListLineUserData()` | :1398 | Tìm kiếm LINE user theo name/view_name. SimplePaginate 20 | — |
| `updateUserQuickReply()` | :1033 | Cập nhật trạng thái quick reply cho LINE user. Reset blocked users | DB update bot_line_user |
| `getListUserQuickReply()` | :1455 | Lấy danh sách user có quick reply enabled | — |
| `ajaxGetListUrlRedirect()` | :816 | Lấy URL redirect + actions + out_time_actions. Hỗ trợ clone actions | — |
| `ajaxMetadataUrl()` | :755 | Lấy metadata 1 URL (title max 10, description max 25 chars) | — |
| `ajaxMetadataUrlAll()` | :779 | Lấy metadata nhiều URLs. Cache từ template_url_redirect nếu có | — |
| `copyFile()` | :928 | Copy file media (dùng khi clone panel) via service | File copy |
| `cloneActionButton()` | :950 | Clone action buttons (danh sách panels) via service | DB insert |
| `createLocation()` | :356 | Helper tạo tmp_location | DB insert |
| `updateLocation()` | :370 | Helper cập nhật tmp_location | DB update |
| `cloneMutilpleAction()` | :966 | Clone action + details + filters | DB insert |

---

## 2. Models Eloquent

### 2.1. Template

**File:** `app/Template.php`
**Table:** `template`
**Timestamps:** `true` (created_at, updated_at)
**Guard:** `$guarded = ['url_image']` (mass assignable trừ url_image)

**Constants:**

| Constant | Giá trị | Mô tả |
|----------|---------|-------|
| `CATEGORY_SCHEDULE_SEND_CHAT_TEXT` | -1111 | Category ID cho schedule send |
| `TYPE_BUTTON_STANDARD` | 1 | Panel/Button loại Standard |
| `TYPE_BUTTON_COLOR` | 2 | Panel/Button loại Color |
| `TYPE_BUTTON_IMAGE` | 3 | Panel/Button loại Image |
| `TYPE_BUTTON_QUICK_REPLY` | 4 | Panel/Button loại Quick Reply |

**Relationships:** **[Cao]**

| Quan hệ | Kiểu | Model liên kết | FK | Mô tả |
|---------|------|---------------|-----|-------|
| `btn_templates()` | hasMany | TmpButton | template_id | Danh sách panels (button groups) |
| `btn_template()` | hasOne | TmpButton | template_id | Panel đầu tiên |
| `tmp_buttons()` | hasMany | TmpButton | template_id | Alias cho btn_templates |
| `Buttons()` | hasManyThrough | Buttons qua TmpButton | template_id → button_id | Tất cả buttons xuyên qua panels |
| `image_map()` | hasOne | ImageMap | template_id | Image map settings |
| `question()` | hasOne | TmpQuestion | template_id | Question template data |
| `location()` | hasOne | TmpLocation | template_id | Location data (lat, lng, address) |
| `introduction()` | hasOne | TmpIntroduction | template_id | Introduction data |
| `templateUrlRedirect()` | hasMany | TemplateUrlRedirect | template_id | URL redirect settings |

**Accessor:** `url_image` — computed từ `image_server + thumbnail_path`. **[Cao]**

**Static Methods:**

| Method | Mô tả |
|--------|-------|
| `searchByKeyWord($group_id, $keyword)` | Tìm template theo tên trong folder, join category, kèm buttons/question/location/introduction |
| `searchByTemplate($group_id, $keyword)` | Tìm tên template type=group |
| `getTemplateById($id)` | Lấy template theo ID (static) |
| `templatesInfo($id)` | Lấy full info template với left join tất cả bảng liên quan (image_map, tmp_location, tmp_button, tmp_introduction, tmp_question) |
| `updateStatusTemplateInPark($id, $status)` | Cập nhật trạng thái template trong park |

### 2.2. TemplateMappingTable

**File:** `app/TemplateMappingTable.php`
**Table:** `template_mapping_tables`
**Timestamps:** `true`
**Guard:** `$guarded = []`

Bảng mapping liên kết template với các bảng khác (vd: step_message). Dùng để propagate cập nhật khi template bị sửa/xoá. **[Cao]**

### 2.3. TemplateUrlRedirect

**File:** `app/TemplateUrlRedirect.php`
**Table:** `template_url_redirect`
**Timestamps:** `true`
**Guard:** `$guarded = []`

Lưu cấu hình URL redirect cho template text: URL hết hạn, action khi click, action khi hết hạn. **[Cao]**

### 2.4. Các model liên quan khác

| Model | File | Table | Mô tả |
|-------|------|-------|-------|
| `Category` | `app/Category.php` | `category` | Folder — `kind = config('sns-line.category_kind.template')` cho template folders |
| `TmpButton` | `app/TmpButton.php` | `tmp_button` | Panel trong template type=form (title, text, img_path, order) |
| `Buttons` | `app/Buttons.php` | `buttons` | Button trên panel (label, post_back, method, data, action_id, order) |
| `TmpLocation` | `app/TmpLocation.php` | `tmp_location` | Toạ độ vị trí (address, latitude, longitude) |
| `TmpIntroduction` | `app/TmpIntroduction.php` | `tmp_introduction` | Giới thiệu LINE (friend_name, display_pc) |
| `TmpQuestion` | `app/TmpQuestion.php` | `tmp_question` | Question template (2 câu trả lời: answer_one/two, postback, method, scenario, data) |
| `ImageMap` | `app/ImageMap.php` | `image_map` | Image map settings (img_width, img_height, img_alt) |
| `ImageMapItems` | `app/ImageMapItems.php` | `image_map_items` | Vùng clickable trên image map (action_type, url, coordinates) |
| `Sticker` | `app/Sticker.php` | `sticker` | LINE sticker (packageId, stickerId) |
| `StickerPackage` | `app/StickerPackage.php` | `sticker_package` | Package sticker LINE |
| `Media` | `app/Media.php` | `media` | Thư viện media (media_type, media_path, media_thumbnail) |
| `Url` | `app/Url.php` | `url` | URL tracking (url, bot_id, metadata) — **connection: mysql_url** |
| `Actions` | `app/Actions.php` | `t_actions` (suy luận) | Action container |
| `ActionDetail` | `app/ActionDetail.php` | `t_actions_detail` (suy luận) | Chi tiết action (type, data JSON) |
| `SendRandomMessage` | `app/SendRandomMessage.php` | `send_random_message` | Message delay/random gửi sau |
| `BotLineUser` | `app/BotLineUser.php` | `bot_line_user` | Quan hệ bot-LINE user (is_tester, is_blocked, is_quick_reply) |

---

## 3. Services / Repositories

### 3.1. TemplateV2Service

**File:** `app/Services/Templates/TemplateV2Service.php`
**Injected vào:** `TemplateV2Controller`

| Method | Mô tả |
|--------|-------|
| `saveTemplateByType($templateGroupId, $data, $actionType)` | Router method — gọi saveTemplate / saveScenario / saveSendAll / saveEvent / saveScheduleSendChat tuỳ actionType |
| `createTemplateGroup($data)` | Tạo/cập nhật group template (type=group). Set position, update BotsTutorial |
| `initDataButton()` | Lấy data khởi tạo editor Panel/Button (post_back types, reply methods, open URL types, friend info) |
| `initDataMedia($templateId)` | Lấy data khởi tạo editor Media (image map data, forms, products, events) |
| `getDataOpenUrl($type)` | Lấy entities theo loại open URL |
| `getDetailTemplateChild($id)` | Lấy chi tiết template con |
| `getDataPreview($type, $id)` | Lấy preview data |
| `getDataPreviewTemplateChild($id)` | Lấy preview template con |
| `copy($from, $folder)` | Copy file media |
| `cloneAction($actionId)` | Clone action + details |
| `uploadImageBtnV2(...)` | Upload ảnh cho button (resize, upload to media server) |

### 3.2. TemplateService

**File:** `app/Services/TemplateService.php`
**Injected vào:** `TemplateV2Controller`

Service chính xử lý logic gửi tin nhắn template qua LINE API. Method `sendTestTemplate()` được gọi bởi `sendTestTemplateV3()`. **[Cao]**

---

## 4. Form Requests / Validation

**Không sử dụng Form Request classes.** Validation được thực hiện trực tiếp trong controller methods. **[Cao]**

### Validation rules trong code:

| Controller | Method | Rule | File:Line |
|-----------|--------|------|-----------|
| MessageTemplateController | `store()` | `botIdCurrent != getBotId()` → reject | :346 |
| MessageTemplateController | `store()` | BackupHistory đang chạy → reject | :351 |
| MessageTemplateController | `store()` | Image map area: x,y >= 0, width,height >= 1, tất cả numeric | :366 |
| MessageTemplateController | `ajaxInitTemplate()` | group_id=0 → không cho xoá folder mặc định | :2890 |
| MessageTemplateController | `ajaxUpdateOrCreatePark()` | BackupHistory check | :274 |
| TemplateV2Controller | `saveTemplate()` | `data` field rỗng → reject | :508-520 |
| TemplateV2Controller | `ajaxCreateGroup()` | `template_name` null hoặc rỗng → reject | :739 |
| TemplateV2Service | `saveTemplateByType()` | botId rỗng → reject | :2506 |

---

## 5. Events / Listeners / Queued Jobs

### Không sử dụng Laravel Events/Listeners cho tính năng này. **[Cao]**

### Queued Jobs / Delayed Messages:

| Cơ chế | Mô tả | File:Line |
|--------|-------|-----------|
| `SendRandomMessage` | Khi template group có delay message enabled (`is_delay_message=1`), template con thứ 2 trở đi được lưu vào bảng `send_random_message` với `time_send` delay random 2-5 giây. Background job (Spring Boot) sẽ gửi sau | TemplateV2Controller.php:1117-1132 |

**Ghi chú job/queue:** Khi gửi test template group có delay:
1. Template con đầu tiên được gửi ngay qua LINE API
2. Các template con còn lại được lưu vào `send_random_message` với status=0
3. Background job (Java Spring Boot) poll bảng này và gửi khi đến `time_send`

---

## 6. Authorization (Policies, Gates)

**Không sử dụng Laravel Policies hoặc Gates.** **[Cao]**

### Cơ chế xác thực & phân quyền:

| Cơ chế | Mô tả | Tin cậy |
|--------|-------|---------|
| Session auth | User phải đăng nhập Admin portal. Middleware `web` đảm bảo session. | **Cao** |
| `getBotId()` | Helper function lấy bot_id từ session. Tất cả queries đều filter theo bot_id → user chỉ thấy template của bot mình | **Cao** |
| `getCurrentUser()` | Helper function lấy user_id từ session | **Cao** |
| Bot ID verification | `store()` kiểm tra `botIdCurrent == getBotId()` — ngăn submit form khi đã chuyển account | **Cao** |
| BackupHistory check | Nhiều method kiểm tra `BackupHistory` đang chạy → block thao tác sửa/xoá trong khi backup | **Cao** |
| Staff permission | **Không thấy** kiểm tra quyền staff trong controller. Staff access được kiểm tra ở middleware level (suy luận) | **Trung bình** |

---

## 7. Business Rules

### 7.1. Template Types

Template có nhiều loại, xác định bởi field `type` trong bảng `template`: **[Cao]**

| Type | Tên JP | Mô tả | Dữ liệu liên quan |
|------|--------|-------|-------------------|
| `text` | テキスト | Tin nhắn text thuần. Content lưu trong field `content` | `template_url_redirect` (URL tracking) |
| `stamp` | スタンプ | LINE sticker. Content = stickerId | — |
| `image` | 画像 | Ảnh. Content = image path. Có thể có image map | `image_map`, `image_map_items` |
| `video` | 動画 | Video. Content = video path (Dropbox) | `media` (thumbnail) |
| `voice` | 音声 | Âm thanh. Content = audio path | `media` |
| `form` | パネル・ボタン | Carousel/Flex với buttons | `tmp_button`, `buttons` |
| `question` | 質問 (legacy) | Template câu hỏi 2 lựa chọn | `tmp_question` |
| `location` | 位置情報 | Vị trí trên bản đồ | `tmp_location` |
| `introduction` | 紹介 (legacy) | Giới thiệu LINE OA | `tmp_introduction` |
| `group` | グループ | Container chứa nhiều template con. Content = comma-separated IDs | Template con (recursive) |

**Lưu ý:** Loại `question` và `introduction` là legacy, không xuất hiện rõ trên UI V2 nhưng vẫn được hỗ trợ trong code. **[Trung bình]**

### 7.2. Folder Management (Category)

- Folder sử dụng bảng `category` với `kind = config('sns-line.category_kind.template')`
- Folder mặc định「未分類」có `category_id = 0` — **không phải record trong bảng category**, mà là convention code
- Folder mặc định không thể xoá (`ajaxInitTemplate` action=deleteGroup kiểm tra group_id=0)
- Folder được lưu vào cookie (`folder_template`) với key = bot_id, expire 14400 phút (10 ngày)
- Khi xoá folder → tất cả template trong folder bị xoá (hard delete), group template → xoá đệ quy template con
- Folder sắp xếp bằng `position` field trong bảng `category`

**File:** `MessageTemplateController.php:2859-2911` (addGroup, deleteGroup, renameGroup) **[Cao]**

### 7.3. Template Creation Flow

1. **Tạo template mới (`store()`):**
   - Verify bot ID chưa đổi
   - Check BackupHistory
   - Validate image map areas (nếu có)
   - Tạo record trong bảng `template` với `position = max(position) + 1`
   - Xử lý theo type:
     - `text/stamp/question/location/introduction`: URL detection (`detectUrlInMessageTextV2`), normalize line breaks
     - `voice`: Upload media file, convert format, tạo record `media`
     - `video`: Upload media + thumbnail, upload to Dropbox, tạo record `media`
     - `image`: Upload + resize (nhiều size cho image map), upload to media server, tạo thumbnail 240x240
     - `form`: Tạo `tmp_button` (panels) + `buttons` cho mỗi panel, xử lý actions
   - Nếu thuộc park → cập nhật content của park template (append ID)
   - Nếu type=text → lưu URL redirect settings
   - Nếu có `line_id` → gửi ngay qua LINE API (`createUpdateAndSendMsg`)

   **File:** `MessageTemplateController.php:337-742` **[Cao]**

2. **Cập nhật template (`save()`):**
   - Load template bằng `findOrFail($id)`
   - Check BackupHistory
   - `resetRelationShipTemplate()` — xoá tất cả relationships cũ theo type
   - Tạo lại relationships mới (giống store nhưng update thay insert)
   - Redirect URL tuỳ context (scenario, broadcast, event, park)

   **File:** `MessageTemplateController.php:2382-2758` **[Cao]**

### 7.4. Template V2 Save Flow

- `saveTemplate()` nhận dữ liệu dưới dạng JSON string trong field `data`
- Update tên và folder nếu `actionType=template` và không có group
- Delegate sang `TemplateV2Service@saveTemplateByType()` — router xử lý theo actionType:
  - `template`: Lưu cho template list
  - `scenario`: Lưu cho step message scenario
  - `sendAll`: Lưu cho broadcast
  - `event`: Lưu cho event step
  - `schedule_send`: Lưu cho schedule send chat

**File:** `TemplateV2Controller.php:503-569`, `TemplateV2Service.php:2504-2527` **[Cao]**

### 7.5. Clone / Copy Template

Deep clone thực hiện qua `cloneTemplate()` — clone đệ quy: **[Cao]**

1. Replicate template record
2. Clone `action_video_id` (nếu có) → tạo action mới + action details + filters
3. Clone `template_url_redirect` → clone action + out_time_action cho mỗi URL
4. Theo type:
   - `image`: Clone `image_map` + `image_map_items` + actions trên mỗi item
   - `question`: Clone `tmp_question`
   - `location`: Clone `tmp_location`
   - `introduction`: Clone `tmp_introduction`
   - `form`: Clone `tmp_button` + `buttons` + actions trên mỗi button
   - `group`: Clone đệ quy tất cả template con (gọi lại `cloneTemplate`)
5. Set position = min(position) - 1 trong folder → template copy ở đầu danh sách

**File:** `MessageTemplateController.php:4400-4577` **[Cao]**

### 7.6. Delete Template

Xoá template là **hard delete** (không soft delete): **[Cao]**

1. Nếu type=group → hard delete tất cả template con (theo IDs trong content)
2. Hard delete template record
3. Cleanup: `deletedDataTemplate()` — xoá `ActionDetail` liên quan
4. Cleanup: Xoá `SendRandomMessage` pending (status=0) cho template bị xoá
5. Cleanup: Update `TemplateMappingTable` → update `step_message.update_timestamp`

**Xoá folder** → xoá tất cả template trong folder → cascade xoá template con của groups

**File:** `MessageTemplateController.php:2949-3007` (deleteItem/deleteItems), `:3134-3191` (ajaxDelTemplate), `:2880-2911` (deleteGroup) **[Cao]**

### 7.7. Send Test Template

Quy trình gửi test template đến LINE user: **[Cao]**

1. Lấy danh sách testers từ `BotLineUser` (is_tester=1, is_blocked=0)
2. Nếu không có tester → trả lỗi
3. Với mỗi tester:
   - Nếu template type=group:
     - Có delay (`is_delay_message=1`): Gửi template đầu tiên ngay, các template sau lưu vào `SendRandomMessage` với delay random 2-5s
     - Không delay: Gom messages thành batch 5 (LINE API limit), gửi qua `createMultipleMessage()`
   - Nếu template đơn: Gửi ngay qua `createMessage()`
4. Sau khi gửi thành công: `Bots.free_send_count += 1`, cập nhật message send count
5. Xử lý lỗi LINE API: rate limit, auth failure, other errors

**File:** `TemplateV2Controller.php:1050-1244` **[Cao]**

### 7.8. URL Detection & Redirect

Khi template type=text: **[Cao]**

1. `detectUrlInMessageTextV2()` — phát hiện URLs trong nội dung text (helper function)
2. Mỗi URL phát hiện được → tạo/cập nhật record trong bảng `url` (connection mysql_url)
3. Tạo `template_url_redirect` record liên kết template ↔ URL, chứa:
   - `action_id`: Action khi user click URL (trong thời hạn)
   - `out_time_action_id`: Action khi hết hạn
   - `url_redirect`: URL chuyển hướng khi hết hạn
   - `url_expired_message`: Thông báo khi hết hạn
   - `url_expired_time`: Thời điểm hết hạn (datetime cụ thể)
   - `duration_from_delivery`: Thời gian hết hạn tính từ lúc gửi (ngày)
   - `after_day_time`: Giờ hết hạn trong ngày

4. URL metadata: `getMetadataContent()` — lấy title, image, description từ URL (OGP)

**File:** `MessageTemplateController.php:784-861` (saveUrlDetect), `:743-783` (saveUrlMetaData) **[Cao]**

### 7.9. Panel/Button (type=form) Structure

Cấu trúc dữ liệu carousel/flex: **[Cao]**

```
Template (type=form, carousel_action_type)
  └── TmpButton[] (panels — title, text, img_path, order)
       └── Buttons[] (buttons — label, post_back, method, data, action_id, order)
```

**Button post_back types** (từ `TemplateV2Service@initDataButton`):

| Value | Tên JP | Mô tả |
|-------|--------|-------|
| 0 | 選択する | Chọn (default) |
| 1 | URLを開く | Mở URL |
| 2 | 電話をかけさせる | Gọi điện |
| 3 | 他のLOAの友だち追加ページを開く | Giới thiệu LINE OA |
| 4 | メールを送らせる | Gửi email |
| 5 | *(scenario — legacy)* | — |
| 6 | *(tag — legacy)* | — |
| 7 | *(event_time — legacy)* | — |
| 8 | 送信ボックスにテキストを入力 | Nhập text vào send box |
| 9 | 他のLOAのプロフィール画面を開く | Mở profile LINE OA |
| 10 | エルメで設定したページを開く | Mở trang Elme (form, product) |

**Button type_open_url** (khi post_back=10):

| Value | Tên JP | Mô tả |
|-------|--------|-------|
| 1 | フォーム作成 | Form |
| 2 | 商品販売ページ | Trang sản phẩm |
| 3 | イベント予約 | Đặt lịch sự kiện |
| 5 | コンバージョンで登録したページ | Trang conversion |
| 6 | カレンダー予約 | Đặt lịch calendar |
| 7 | サロン・面談予約 | Đặt lịch salon |
| 8 | レッスン予約 | Đặt lịch lesson |

**Panel sub-types** (từ `Template::TYPE_BUTTON_*`):

| Value | Constant | Tên JP | Mô tả |
|-------|----------|--------|-------|
| 1 | TYPE_BUTTON_STANDARD | スタンダード | Carousel tiêu chuẩn |
| 2 | TYPE_BUTTON_COLOR | カラーボタン | Button màu |
| 3 | TYPE_BUTTON_IMAGE | 画像 | Image carousel (có aspect ratio tính từ ảnh) |
| 4 | TYPE_BUTTON_QUICK_REPLY | クイックリプライ | Quick reply buttons |

**File:** `Template.php:20-23`, `TemplateV2Service.php:2562-2593` **[Cao]**

### 7.10. Image Map

Khi template type=image và `tmp_setting_image_map=1`: **[Cao]**

1. Upload ảnh gốc → resize theo config `sns-line.image_size` (nhiều kích thước)
2. Upload tất cả kích thước lên media server
3. Tạo `image_map` record (img_width, img_height, img_alt)
4. Tạo `image_map_items` — mỗi vùng clickable có:
   - `action_type`: 1=URL, 2=Text, 3=Phone, 4=LINE, 5=Email
   - `open_url_type`: 0=URL thường, 1=Form, 2=Product, 3=Event booking, 4=SiteScript, 5=Conversion
   - `url`, `action_id`, `form_answer_id`, `bill_id`, `booking_event_id`, `site_script_id`, `conversion_id`
   - Toạ độ vùng: x, y, width, height (validate >= 0, width/height >= 1)

**File:** `MessageTemplateController.php:359-375` (validation), `:3824-3908` (initDataImageMap) **[Cao]**

### 7.11. Media Upload Flow

Upload media qua nhiều cơ chế: **[Cao]**

1. **Direct upload** (`uploadMediaFile`): File upload → lưu local → upload to media server API (`callApiUpload`)
2. **From library** (`media_path`): Dùng path từ media library đã upload trước đó
3. **Base64** (`uploadImgBase64Api`): Upload ảnh base64 (cho panel images)
4. **Video to Dropbox** (`uploadFileDropbox`): Video được upload lên Dropbox, path Dropbox lưu vào content
5. **Thumbnail auto-generate**: Ảnh → resize 240x240, Video → user upload manual hoặc dùng default

**File:** `MessageTemplateController.php:890-1083` **[Cao]**

### 7.12. Backup Protection

Tất cả thao tác ghi (create, update, delete) đều kiểm tra `BackupHistory`: **[Cao]**

```php
$backuoHistory = BackupHistory::where('code', $bot->transfer_code)
    ->whereIn('status', [0, 1])->first();
if($backuoHistory){
    return response()->json(['status' => false, 'message' => MESSAGE_NOTIFY_BACKUP], 500);
}
```

Nếu đang có backup (status 0 hoặc 1) → block tất cả thao tác sửa đổi.

### 7.13. Friend Info Auto-Insert

Editor text hỗ trợ chèn biến tự động thông tin LINE user: **[Cao]**

| Code | Mô tả |
|------|-------|
| `[FRIEND_INFO_system_name]` | Tên hiển thị hệ thống |
| `[FRIEND_INFO_phone]` | Số điện thoại |
| `[FRIEND_INFO_email]` | Email |
| `[FRIEND_INFO_birthday]` | Ngày sinh |
| `[FRIEND_INFO_province]` | Tỉnh/thành phố |
| `[FRIEND_INFO_zip_code]` | Mã bưu chính |
| `[FRIEND_INFO_district]` | Quận/huyện |
| `[FRIEND_INFO_township]` | Phường/xã |
| `[FRIEND_INFO_building]` | Tòa nhà |
| `[FRIEND_INFO_{hashId}]` | Custom friend info (ID encoded bằng Hashids) |

**File:** `TemplateV2Controller.php:245-295`, `TemplateV2Service.php:2620-2665` **[Cao]**

### 7.14. Position Management

Template và folder sắp xếp bằng field `position`: **[Cao]**

- **Folder:** Tạo mới → `position = max(position) + 1` (hoặc `min(position) - 1` tuỳ method)
- **Template:** Tạo mới → `position = max(position) + 1`
- **Copy:** `position = min(position) - 1` → template copy ở đầu danh sách
- **Move:** Di chuyển sang folder khác → `position = min(position of target folder) - 1`
- **Sort:** Update position theo thứ tự mới (1, 2, 3...)
- **Sort child:** Update position + update parent content (comma-separated IDs)

### 7.15. Template trong context khác

Template không chỉ dùng độc lập mà còn được nhúng trong: **[Trung bình]**

| Context | Cách nhúng | Bảng liên kết |
|---------|-----------|---------------|
| Step Message (Scenario) | `step_message.template_ids` (comma-separated) | `template_mapping_tables` |
| Broadcast | `broadcast.template_ids` | — |
| Event Step | `event_step.templates_id` | — |
| Schedule Send Chat | Qua TemplateV2Service | — |
| Chat 1:1 | Gửi trực tiếp qua `ChatController@sendTemplate` | — |
| Action Detail | `action_detail.type='template'`, `data.id=template_id` | `t_actions_detail` |

Khi xoá template → cần cleanup các references trong `action_detail` (`deletedDataTemplate()`).

---

## 8. Helper Functions (Global)

| Function | Mô tả | Tin cậy |
|----------|-------|---------|
| `getBotId()` | Lấy bot_id từ session | **Cao** |
| `getCurrentUser()` | Lấy user_id từ session | **Cao** |
| `detectUrlInMessageTextV2($content, $bot)` | Phát hiện và chuyển đổi URL trong text | **Cao** |
| `getMetadataContent($url)` | Fetch OGP metadata từ URL | **Cao** |
| `callApiUpload($form_param, $path)` | Upload file lên media server | **Cao** |
| `uploadImgBase64Api($base64, $folder, $path)` | Upload ảnh base64 | **Cao** |
| `uploadThumbnailApi($file, $folder, $path, $size)` | Upload thumbnail với resize | **Cao** |
| `uploadFileDropbox($path, $type)` | Upload file lên Dropbox | **Cao** |
| `convertFile($url, $type)` | Chuyển đổi format file (video/audio) | **Cao** |
| `getDurationSeconds($path)` | Lấy duration file audio | **Cao** |
| `isBase64($string)` | Kiểm tra chuỗi là base64 | **Cao** |
| `checkFullUrl($url)` | Kiểm tra URL đầy đủ | **Cao** |
| `notifyChatwork($message)` | Gửi thông báo Chatwork | **Cao** |
| `addLogUserAction($action)` | Log hành động user | **Cao** |
| `createMessage(...)` | Tạo và gửi tin nhắn qua LINE API | **Cao** |
| `createMultipleMessage(...)` | Gửi nhiều tin nhắn cùng lúc (batch) | **Cao** |
| `updateMessageSendCount($botId, $date, $type)` | Cập nhật thống kê gửi tin | **Cao** |
| `sortRankItems()` | Callback sort cho usort (sort by position) | **Cao** |
| `checkExistsBtnQuickReply($content)` | Kiểm tra đã có quick reply button chưa | **Cao** |
| `checkUpdateHasTutorial($botId)` | Kiểm tra và cập nhật trạng thái tutorial | **Cao** |

---

## 9. Tổng kết kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                    Routes (web.php)                       │
│  /basic/message-template/*    /ajax/init-template        │
│  /basic/template-v2/*         /ajax/template-v2/*        │
│  /basic/park-template/*       /ajax/park-template/*      │
└──────────────┬──────────────────────┬────────────────────┘
               │                      │
    ┌──────────▼──────────┐  ┌────────▼──────────────┐
    │ MessageTemplate     │  │ TemplateV2             │
    │ Controller           │  │ Controller             │
    │ (4579 lines, legacy) │  │ (1484 lines, new)      │
    │ Direct DB access     │  │ Uses Services          │
    └──────────┬──────────┘  └────────┬──────────────┘
               │                      │
               │              ┌───────▼────────────┐
               │              │TemplateV2Service    │
               │              │TemplateService      │
               │              └───────┬────────────┘
               │                      │
    ┌──────────▼──────────────────────▼────────────────┐
    │                    Models                         │
    │  Template ──┬── TmpButton ── Buttons             │
    │             ├── TmpLocation                       │
    │             ├── TmpIntroduction                   │
    │             ├── TmpQuestion                       │
    │             ├── ImageMap ── ImageMapItems          │
    │             ├── TemplateUrlRedirect                │
    │             └── TemplateMappingTable               │
    │  Category (folders)                               │
    │  Actions ── ActionDetail ── FilterV2              │
    │  Sticker / StickerPackage                         │
    │  Media / Url / BotLineUser                        │
    │  SendRandomMessage (delayed messages → Java job)  │
    └──────────────────────────────────────────────────┘
               │
    ┌──────────▼──────────┐
    │   External APIs      │
    │  LINE Messaging API  │
    │  Media Server API    │
    │  Dropbox API         │
    │  Chatwork API        │
    └─────────────────────┘
```
