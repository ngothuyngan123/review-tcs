# FA-012 Quản lý thẻ「タグ管理」 — Logic Spec

> Phân tích từ source code Laravel (`src/web/sns-line/`).
> Confidence: **Cao** — đọc trực tiếp từ code.

---

## Controllers

### 1. Basic\TagController
- **File**: `app/Http/Controllers/Basic/TagController.php` (1603 dòng)
- **Namespace**: `App\Http\Controllers\Basic`
- **Dependencies**: `CategoryRepositoryInterface` (inject qua constructor)

#### Action: index (EP-01)
- **Route**: GET `/basic/tag`
- **Chức năng**: Render trang danh sách tag chính (view Blade `basic.tag.v2.index`)
- **Luồng xử lý**:
  1. Lấy `bot_id` từ session qua `getBotId()`
  2. Đọc folder cookie `folder_tag` — xác định folder đang chọn
  3. Kiểm tra folder có tồn tại trong DB không (category kind=0, is_deleted=0)
  4. Nếu folder không tồn tại → reset cookie về 0 (未分類)
  5. Trả view với `folderCookie`, `scenario`, `conversion`, `richMenus` (đều rỗng — data load qua AJAX)
- **Gọi đến**: `Category::query()`, `getBotId()`, `Cookie::get()`, `Cookie::queue()`

#### Action: ajaxGetListTag (EP-10)
- **Route**: GET `/ajax/v2/tag`
- **Chức năng**: Lấy danh sách tag với bộ lọc, sắp xếp, phân trang
- **Luồng xử lý**:
  1. Lấy params: `category_id`, `keyword`, `type`, `limit`, `unlimit`, `orders`
  2. Query `Tag` model where `bot_id` = current bot
  3. Eager load `action.details` (relationship)
  4. Nếu `type` = `sort_item` → chỉ select `id`, `name`
  5. Nếu có `category_id` và không có `keyword` → filter theo folder
  6. Nếu có `keyword` → filter `name LIKE %keyword%` (bỏ qua category_id)
  7. Nếu có `orders` → sắp xếp theo cột cho phép: `created_at`, `position`, `name`, `updated_at`
  8. Nếu `unlimit` = true → `get()`, ngược lại → `paginate(limit ?? 15)`
- **Gọi đến**: `Tag` model (alias khác của `Tags`), `Actions` relationship

#### Action: ajaxDeleteTags (EP-11)
- **Route**: DELETE `/ajax/v2/tag`
- **Chức năng**: Soft delete nhiều tag. Dọn dẹp dữ liệu liên quan.
- **Luồng xử lý**:
  1. **Kiểm tra backup**: Tìm `BackupHistory` theo `bot.transfer_code` với status IN (0,1) → nếu có, chặn thao tác
  2. Gỡ tag khỏi Landing pages: `Landing::whereIn("tag_id", $ids)->update(["tag_id" => null])`
  3. Ghi nhận người xoá: `Tags::update(['user_id_del' => Auth::id(), 'count_user_tag' => 0])`
  4. Soft delete: `Tags::delete()` (SoftDeletes trait → set `deleted_at`)
  5. Với mỗi tag: gọi `$this->deletedDataTag($tagId)` để dọn dữ liệu phụ thuộc
- **Side effects**: Xoá `tag_line_user`, xoá `ActionLimitTag`, cập nhật `FilterV2`, cập nhật `ActionDetail`, sync Elasticsearch

#### Action: ajaxMoveCategory (EP-12)
- **Route**: POST `/ajax/v2/tag/move-category`
- **Chức năng**: Di chuyển tag sang folder khác
- **Luồng xử lý**:
  1. Kiểm tra backup
  2. Lấy max position của bot
  3. Với mỗi tag ID → update `category_id` = folder đích, `position` = max + 1
- **Gọi đến**: `Tags::where()->update()`

#### Action: ajaxCreateMultipleTags (EP-13)
- **Route**: POST `/ajax/v2/tag/create-multiple`
- **Chức năng**: Tạo nhiều tag cùng lúc (bulk insert)
- **Luồng xử lý**:
  1. Lấy mảng tag names từ request
  2. **Kiểm tra trùng tên**: `Tags::whereIn('name', $arrTagName)` → nếu có bất kỳ tag nào trùng → trả lỗi (dừng toàn bộ)
  3. Lấy max position trong folder
  4. Tạo mảng data insert với `bot_id`, `name`, `category_id`, `position` tăng dần, `count_user_tag` = 0
  5. Bulk insert: `Tags::insert($dataInsert)`
  6. Cập nhật tutorial status: `BotsTutorial::update(['status_tag' => 1])`
  7. Gọi `checkUpdateHasTutorial($botId)` → kiểm tra tutorial hoàn thành
- **Business rule**: Tên tag phải duy nhất trong cùng bot. Nếu 1 trong danh sách trùng → toàn bộ batch bị reject.

#### Action: ajaxSortTag (EP-14)
- **Route**: POST `/ajax/v2/tag/sort-tag`
- **Chức năng**: Sắp xếp tag theo thứ tự kéo thả
- **Luồng xử lý**:
  1. Parse `sort_ids` (chuỗi phân cách bởi dấu phẩy) thành mảng
  2. Với mỗi ID → update `position` = index + 1
- **Gọi đến**: `Tags::where('id', $id_sort)->update(['position' => $key + 1])`

#### Action: ajaxGetCategories (EP-20)
- **Route**: GET `/ajax/v2/tag/category`
- **Chức năng**: Lấy danh sách folder tag + số tag 未分類
- **Luồng xử lý**:
  1. Gọi `Category::getListCategoryTag()` — static method (chi tiết ở phần Model)
  2. Đếm tag có `category_id=0` (未分類): `Tags::countTags(['category_id' => 0, 'bot_id' => botId])`

#### Action: ajaxCreateCategory (EP-21)
- **Route**: POST `/ajax/v2/tag/category/create`
- **Chức năng**: Tạo folder tag mới
- **Luồng xử lý**:
  1. Kiểm tra backup
  2. Lấy max position của category kind=0
  3. Tạo record: `Category::create(['bot_id', 'name', 'kind' => 0, 'position' => max + 1])`
  4. Set `count = 0` cho response

#### Action: ajaxUpdateCategory (EP-22)
- **Route**: PUT `/ajax/v2/tag/category/update/{category}`
- **Chức năng**: Đổi tên folder
- **Luồng xử lý**: `$category->update(['name' => $request->input('name')])`
- **Ghi chú**: Sử dụng route model binding cho `Category`

#### Action: ajaxDeleteCategory (EP-23)
- **Route**: DELETE `/ajax/v2/tag/category/{id}`
- **Chức năng**: Xoá folder — soft delete bằng `is_deleted=1`, chuyển tags về 未分類
- **Luồng xử lý**:
  1. Kiểm tra backup
  2. Soft delete folder: `Category::update(['is_deleted' => 1])`
  3. Lấy tất cả tag trong folder
  4. **Chuyển tag về 未分類**: Update mỗi tag `category_id = 0`, `position = max + 1`
  5. **Lưu ý**: Hành vi v2 KHÔNG xoá tags — chỉ chuyển folder. Khác với legacy (`ajaxGetListCategoryTag` case `deleteGroup` — xoá tag luôn)
- **Business rule**: Xoá folder không mất tag — tag được bảo toàn, chỉ chuyển về 未分類

#### Action: ajaxSortTagCategory (EP-24)
- **Route**: POST `/ajax/v2/tag/category/sort-category`
- **Chức năng**: Sắp xếp folder
- **Luồng xử lý**: Parse `sort_ids` → update position cho mỗi category

#### Action: ajaxSaveTag (EP-30)
- **Route**: POST `/ajax/save-tag`
- **Chức năng**: Lưu tag — CRUD chính với switch action
- **Luồng xử lý**:
  1. Kiểm tra backup
  2. Switch theo `action`:
     - **`add_tag` / `copy_tag`**:
       a. Validate: tên không rỗng, tên không trùng
       b. Tạo tag mới với: `bot_id`, `name`, `category_id`, `action_id`, `limit_action_id`, `is_2th_apply`, `is_limit`, `limit`, `limit_action_mode`
       c. Set position = max + 1 trong cùng folder
     - **`edit_tag`**:
       a. So sánh tên cũ vs mới
       b. Nếu tên thay đổi: kiểm tra trùng tên, cập nhật `FormAnswerDetails` có `name='select2_5'` → đổi value trong JSON settings
       c. Update tag với dữ liệu mới
- **Side effects**: Khi edit tên tag → cập nhật tất cả form answer details có reference đến tên tag cũ
- **Gọi đến**: `Tags`, `FormAnswerDetails`, `Bots`, `BackupHistory`

#### Action: ajaxSaveTagCsv (EP-31)
- **Route**: POST `/ajax/save-tag-csv`
- **Chức năng**: Import tag từ file CSV
- **Luồng xử lý**:
  1. Validate MIME type (danh sách CSV MIME types)
  2. Đọc nội dung file, detect encoding (SJIS-WIN → UTF-8)
  3. Parse CSV, bỏ header row
  4. Giới hạn tối đa 200 tags
  5. Với mỗi tên: cắt 50 ký tự, bỏ qua nếu trùng hoặc rỗng
  6. Insert từng tag (reverse order): set `bot_id`, `name`, `category_id`, `position` tăng dần
  7. Cập nhật tutorial status
- **Business rules**:
  - Tối đa 200 tags/file
  - Tên tag tối đa 50 ký tự
  - Bỏ qua trùng tên (không báo lỗi)
  - Hỗ trợ file SJIS-WIN (tiếng Nhật) và UTF-8

#### Action: ajaxExportCsvEdit (EP-32)
- **Route**: POST `/ajax/export-csv-edit`
- **Chức năng**: Tạo file CSV mẫu trống
- **Luồng xử lý**: Sử dụng `CsvEditExport` class → tạo file CSV với 1 header row → lưu vào `public/`
- **Gọi đến**: `Excel::store(new CsvEditExport(null), '/public/編集用CSV.csv')`

#### Action: downloadCsvEdit (EP-33)
- **Route**: GET `/ajax/downloadCsvEdit`
- **Chức năng**: Download file CSV đã tạo
- **Luồng xử lý**: `response()->download(public_path() . '/storage/' . $fileName)`

#### Action: getTagRemoved (EP-15)
- **Route**: GET `/ajax/v2/tag/get-tag-removed`
- **Chức năng**: Lấy danh sách tag đã xoá (soft deleted)
- **Luồng xử lý**:
  1. Query `Tags::onlyTrashed()` (SoftDeletes scope) where `bot_id` = current
  2. Sắp xếp theo `order` + `dir` params
  3. Phân trang (mặc định 15)
  4. Nếu trang > 1 và rỗng → tự quay lại trang 1
  5. Với mỗi tag đã xoá: lấy `username_del` từ `User::find(user_id_del)`
- **Gọi đến**: `Tags::onlyTrashed()`, `User::find()`

#### Action: restoreTag (EP-16)
- **Route**: POST `/ajax/v2/tag/restore-tag/{id}`
- **Chức năng**: Khôi phục tag đã xoá
- **Luồng xử lý**:
  1. Tìm tag: `Tags::withTrashed()->where('id', $id)->where('bot_id', $botId)`
  2. Nếu không tìm thấy → throw 404
  3. **Kiểm tra trùng tên**: nếu đã có tag active cùng tên → trả lỗi
  4. Kiểm tra folder gốc: nếu folder đã bị `is_deleted=1` → khôi phục folder (set `is_deleted=0`)
  5. Restore tag: `Tags::restore()`
  6. Reset `count_user_tag = 0` (vì đã xoá `tag_line_user` khi delete)
- **Business rule**: Khôi phục tag reset số người về 0 vì liên kết tag-user đã bị xoá khi xoá tag

#### Action: validateLimit (EP-17)
- **Route**: POST `/ajax/v2/tag/validate-limit/{tag}`
- **Chức năng**: Kiểm tra giới hạn trước khi lưu
- **Luồng xử lý**: Nếu `count_user_tag > 0` VÀ `is_limit = true` VÀ `count_user_tag > limit` VÀ `isCopy != 1` → trả lỗi
- **Business rule**: Khi edit tag, không được đặt limit thấp hơn số người đã gán (trừ khi copy tag)

#### Action: editTag (EP-02)
- **Route**: GET `/basic/tag/edit-tag/{id}`
- **Chức năng**: Render trang chỉnh sửa tag (view `basic.tag.v2.edit`)
- **Luồng xử lý**:
  1. Lấy tag by ID. Nếu không tìm thấy → redirect `/basic/tag`
  2. Lấy danh sách folders, scenarios, rich menus cho bot
  3. Trả view với `getTag`, `folders`, `scenario`, `richMenus`, `id_setting`, `folderCookie`

#### Action: copyTag (EP-03)
- **Route**: GET `/basic/tag/copy-tag/{id}`
- **Chức năng**: Render trang copy tag (cùng view `basic.tag.v2.edit` nhưng với `id_copy`)
- **Luồng xử lý**: Tương tự editTag nhưng truyền `id_copy` thay vì `id_setting`

#### Action: friendList (EP-07)
- **Route**: GET `/basic/tag/friend-list/{id}`
- **Chức năng**: Render trang danh sách bạn bè của tag (view `basic.tag.friend_list`)
- **Luồng xử lý**: Lấy tag name, trả view với `tag_id` và `tagName`

#### Action: ajaxGetLineUserByTag (EP-35)
- **Route**: POST `/ajax/get-line-user-by-tag`
- **Chức năng**: Lấy danh sách LINE users có tag, phân trang
- **Luồng xử lý**:
  1. Tìm tag → nếu không tồn tại → redirect `/basic/tag`
  2. Tính tổng từ `count_user_tag` (denormalized field)
  3. Phân trang thủ công: limit 50, offset = (page - 1) * 50
  4. Với mỗi `tagLineUser` → lookup `LineUser::find()` để lấy `name`, `avatar_url`

#### Action: ajaxRemoveLineUsersFromTag (EP-36)
- **Route**: POST `/ajax/remove-line-users-from-tag`
- **Chức năng**: Gỡ nhiều users khỏi tag
- **Luồng xử lý**:
  1. Đếm `tagLineUser` cần xoá
  2. Giảm `count_user_tag` (decrement)
  3. Xoá records `tag_line_user`
  4. Sync Elasticsearch cho từng user bị gỡ
- **Side effects**: Update `sync_elasticsearch` table

#### Action: initDataInfo (EP-47)
- **Route**: POST `/basic/initDataInfoTag`
- **Chức năng**: Lấy chi tiết tag kèm action settings
- **Luồng xử lý**:
  1. Lấy tag by ID
  2. Lấy `action_id` → gọi `getActionDetailByActionId()` → trả về action details
  3. Lấy `limit_action_id` → gọi `getActionDetailByActionId()` → trả về limit action details
  4. Nếu `action == 'copy_tag'`: clone action qua `MessageTemplateController::cloneMutilpleAction()`
  5. Gắn `setting_actions` và `setting_limit_actions` vào response
- **Gọi đến**: `Tags`, `ActionDetail`, `Actions::initDataAction()`, `MessageTemplateController::cloneMutilpleAction()`

#### Private Method: deletedDataTag($id)
- **File**: `app/Http/Controllers/Basic/TagController.php:947`
- **Chức năng**: Dọn dẹp dữ liệu phụ thuộc khi xoá tag
- **Luồng xử lý**:
  1. **Cập nhật FilterV2**: Tìm filter type='tag' chứa tag ID → gỡ tag ID khỏi `data.tags_search` → nếu hết tag → xoá filter, nếu còn → cập nhật text preview
  2. **Cập nhật ActionDetail**: Tìm action detail type='tag' chứa tag ID → gỡ tag ID khỏi `data.ids` → nếu hết → xoá action detail (và xoá Action parent nếu không còn detail)
  3. **Xoá tag_line_user**: `DB::table('tag_line_user')->where('tag_id', $id)->delete()`
  4. **Xoá ActionLimitTag**: `ActionLimitTag::where('tag_id', $id)->delete()`
  5. **Sync Elasticsearch**: Với mỗi `tag_line_user` bị xoá → insert record `SyncElasticsearch`
- **Gọi đến**: `FilterV2`, `ActionDetail`, `Actions`, `tagLineUser`, `ActionLimitTag`, `SyncElasticsearch`

#### Private Method: getActionDetailByActionId($actionId, $ignoreFilter)
- **File**: `app/Http/Controllers/Basic/TagController.php:1089`
- **Chức năng**: Lấy chi tiết action (gồm nhiều action details)
- **Luồng xử lý**:
  1. Query `ActionDetail::where('action_id', $actionId)->get()`
  2. Với mỗi detail: parse data qua `Actions::initDataAction()`
  3. Nếu `ignoreFilter` → set filters rỗng, ngược lại load filter từ `FilterV2::initDataFilter()`
  4. Nếu detail type='tag' → kèm `list_tags` (Tag records)

#### Action: tagRemoved (EP-05)
- **Route**: GET `/basic/tag/removed`
- **Chức năng**: Render trang tag đã xoá (view `basic.tag.v2.tags_removed`)

#### Action: ajaxGetListCategoryTag (EP-34)
- **Route**: POST `/ajax/get-list-group-tag`
- **File**: `app/Http/Controllers/Basic/TagController.php:351`
- **Chức năng**: Legacy — đa năng, xử lý nhiều action qua switch statement
- **Actions hỗ trợ**: `addGroup`, `addAndEditGroup`, `addTag`, `deleteGroup`, `deleteTag`, `renameGroup`, `renameTag`, `searchByKeyWord`, `sortItem`, `sortFolder`, `moveItem`
- **Ghi chú**: Đây là API cũ (legacy v1), v2 API tách thành nhiều endpoint riêng. Vẫn hoạt động nhưng UI mới dùng v2.

---

### 2. Api\TagController
- **File**: `app/Http/Controllers/Api/TagController.php` (376 dòng)
- **Namespace**: `App\Http\Controllers\Api`
- **Mô tả**: API cho mobile app — quản lý tag-user assignment

#### Action: getTagOfUserV2 (EP-60)
- **Route**: POST `/api/get-list-tag-of-user-v2`
- **Chức năng**: Lấy tags đã gán cho user, grouped by folder
- **Luồng xử lý**:
  1. Join `tag_line_user` → `tags` → `category`
  2. Filter: `category.kind = 0` (tag), `category.is_deleted = 0`, `tags.deleted_at IS NULL`
  3. Order by `category.position DESC`, `tags.position DESC`
  4. Group by `category_name` → mảng `{category_name, tags: [{id, name}]}`
  5. Thêm folder 未分類 (category_id=0) vào đầu danh sách

#### Action: getTagOfUser (EP-61)
- **Route**: POST `/api/get-list-tag-of-user`
- **Chức năng**: Lấy tags đã gán cho user (flat list, không group)

#### Action: removeTagOfUserV2 (EP-62)
- **Route**: POST `/api/remove-tag-of-user-v2`
- **Chức năng**: Gỡ nhiều tags khỏi user
- **Luồng xử lý**:
  1. Với mỗi tag ID: tìm tag, đếm `tag_line_user` records
  2. Giảm `count_user_tag` → xoá `tag_line_user`
  3. Sync Elasticsearch

#### Action: removeTagOfUser (EP-63)
- **Route**: POST `/api/remove-tag-of-user`
- **Chức năng**: Gỡ 1 tag khỏi user (tương tự EP-62 cho single tag)

#### Action: getListFolderTagByBotV2 (EP-64)
- **Route**: POST `/api/get-list-folder-tag-by-bot-v2`
- **Chức năng**: Lấy danh sách folder + tags con (nested)
- **Luồng xử lý**:
  1. Query Category left join Tags → group by category → count tags
  2. Eager load `tags` relationship (select id, name, category_id; order position DESC)
  3. Thêm folder 未分類 với tags có `category_id=0`

#### Action: getListFolderTagByBot (EP-65)
- **Route**: POST `/api/get-list-folder-tag-by-bot`
- **Chức năng**: Lấy danh sách folder + count (không kèm tags con)

#### Action: getListTagByCategory (EP-66)
- **Route**: POST `/api/get-list-tag-by-category`
- **Chức năng**: Lấy tags theo category ID

#### Action: addTagForUser (EP-67)
- **Route**: POST `/api/add-tag-for-user`
- **Chức năng**: Đồng bộ tag cho user (full sync — thêm mới + xoá không còn)
- **Luồng xử lý**:
  1. Lấy danh sách tag hiện tại của user (`listTagOld`)
  2. Tính diff: `arrTagAdd = tagIds - listTagOld`, `arrTagDelete = listTagOld - tagIds`
  3. **Thêm tag** (với mỗi tag mới):
     a. Kiểm tra giới hạn: `count_user_tag + 1 <= limit` (atomic update)
     b. Nếu giới hạn đầy + `is_limit = true`:
        - Trigger `limit_action`: gọi `ActionLimitTag::handleLimitActionTag()` → nếu chưa trigger (mode=0, max 1 lần) → gọi `sendAction(limit_action_id, ...)`
        - Bỏ qua tag này (không thêm)
     c. Nếu chưa đầy: insert `tag_line_user`, tăng `count_user_tag`
     d. Nếu tag có `action_id` → gọi `sendAction(action_id, ...)` để trigger action tự động
  4. **Xoá tag** (với mỗi tag không còn): giảm `count_user_tag`, xoá `tag_line_user`
  5. Sync Elasticsearch
- **Side effects**: `sendAction()` có thể trigger: gửi tin nhắn LINE, thêm step message, thay Rich Menu, v.v.
- **Ghi chú quan trọng**: `sendAction()` gọi với `typeStartScenario = '6002'` → đánh dấu nguồn trigger từ tag assignment

---

## Models

### 1. Tags
- **File**: `app/Tags.php`
- **Bảng DB**: `tags`
- **Traits**: `SoftDeletes` (sử dụng `deleted_at`)
- **Guarded**: `[]` (không guarded — tất cả cột đều fillable)
- **Timestamps**: Có (`created_at`, `updated_at`)

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `category()` | belongsTo | `App\Category` | `category_id` | Folder chứa tag |
| `tagLine()` | hasMany | `App\tagLineUser` | `tag_id` → `id` | Liên kết tag-user |
| `scenario()` | hasOne | `App\Scenario` | `scenario_id` → `id` | Step message liên kết |
| `tempalte()` | hasOne | `App\Template` | `add_template_id` → `id` | Template tin nhắn liên kết |
| `richMenu()` | hasOne | `App\RichMenus` | `rich_menu_id` → `id` | Rich menu liên kết |

#### Static Methods
| Method | Mô tả | File:Line |
|--------|-------|-----------|
| `searchByKeyWordTag($group_id, $keyword)` | Tìm tag theo keyword trong folder, kèm count user | `Tags.php:44` |
| `getTemplatesToSend($add_tag_ids)` | Lấy templates liên kết với tags (cho gửi tin) | `Tags.php:94` |
| `getTagById($id)` | Lấy tag by ID hoặc mảng IDs | `Tags.php:111` |
| `changeTagsToNewBot($currentBot, $newBot)` | Chuyển tags sang bot khác (dùng cho backup/transfer) | `Tags.php:123` |
| `countTags($condition)` | Đếm tag theo condition | `Tags.php:132` |
| `getTagsInCategory($lineUserId, $botId, $categoryId)` | Lấy tags trong category, đánh dấu is_selected cho user | `Tags.php:143` |

### 2. Tag
- **File**: `app/Tag.php`
- **Bảng DB**: `tags` (cùng bảng với Tags — alias model)
- **Traits**: `SoftDeletes`
- **Ghi chú**: Model duplicate — cả `Tag` và `Tags` đều map vào bảng `tags`. `Tag` được dùng ở v2 endpoints, `Tags` ở legacy code.

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `tag_line_user()` | hasMany | `App\tagLineUser` | `tag_id` → `id` | Liên kết tag-user |
| `action()` | belongsTo | `App\Actions` | `action_id` → `id` | Action gắn với tag |

### 3. Category
- **File**: `app/Category.php`
- **Bảng DB**: `category`
- **Guarded**: `[]`
- **Ghi chú**: Model chung cho nhiều loại category — phân biệt bằng `kind`

#### Relationships liên quan đến Tag
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `tags()` | hasMany | `App\Tags` | `category_id` → `id` | Tags trong folder |
| `tagLine()` | hasManyThrough | `App\tagLineUser` via `App\Tags` | `category_id` → `tag_id` | Users qua tags trong folder |

#### Static Methods liên quan đến Tag
| Method | Mô tả | File:Line |
|--------|-------|-----------|
| `getListCategoryTag()` | Lấy danh sách folder tag (kind=0, is_deleted=0) kèm count tag | `Category.php:1334` |
| `getCategoryTagDefault($bot_id, $paginate)` | Lấy tag 未分類 (category_id=0) | `Category.php:965` |
| `getCategoryTagDefault2($bot_id, $paginate)` | Lấy tag 未分類 v2 (trả raw collection) | `Category.php:1004` |
| `getCategoryTagDefaultByKeyWord($bot_id, $keyword)` | Tìm tag 未分類 theo keyword | `Category.php:1028` |
| `getTagOfCategory($category, $paginate)` | Lấy tags trong folder kèm count user (legacy — count qua join) | `Category.php:1917` |
| `getTagOfCategory2($category, $paginate)` | Lấy tags trong folder v2 (đơn giản hơn) | `Category.php:1960` |
| `categoriesTags($line_id, $all, $botId)` | Lấy folders + tags cho user cụ thể (dùng ở chat) | `Category.php:1977` |
| `getAllCategoriesOfTag()` | Lấy tất cả folders + tags của bot | `Category.php:2002` |

### 4. tagLineUser
- **File**: `app/tagLineUser.php`
- **Bảng DB**: `tag_line_user`
- **Guarded**: `[]`
- **Timestamps**: Có
- **Mô tả**: Bảng pivot liên kết tag ↔ LINE user

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `tags()` | belongsTo | `App\Tags` | `tag_id` → `id` | Tag liên kết |

#### Static Methods
| Method | Mô tả |
|--------|-------|
| `getTagLineUser($tagId)` | Lấy danh sách LINE users có tag (join line_user để lấy line_id) |

### 5. ActionLimitTag
- **File**: `app/ActionLimitTag.php`
- **Bảng DB**: `action_limit_tags` (convention)
- **Guarded**: `[]`
- **Mô tả**: Tracking số lần trigger limit action cho từng tag-user

#### Static Methods
| Method | Mô tả | File:Line |
|--------|-------|-----------|
| `handleLimitActionTag($tag, $lineUserId)` | Xử lý limit action: tạo record nếu chưa có, kiểm tra mode (0=chỉ 1 lần) | `ActionLimitTag.php:11` |

### 6. SyncElasticsearch
- **File**: `app/SyncElasticsearch.php`
- **Bảng DB**: `sync_elasticsearch` (connection: `mysql_step_message`)
- **Mô tả**: Queue đồng bộ dữ liệu sang Elasticsearch. Insert record → background job xử lý.

---

## Services / Repositories

### CategoryRepositoryInterface
- **Inject vào**: `Basic\TagController` constructor
- **Ghi chú**: Được inject nhưng controller chủ yếu dùng `Category` static methods trực tiếp thay vì qua repository. Repository interface có thể là di sản từ architecture cũ.

### Helper Functions (Global)
- **File**: `app/Helpers/functions.php`

| Function | Mô tả | File:Line |
|----------|-------|-----------|
| `getBotId()` | Lấy `current_bot_id` từ Session | `functions.php:359` |
| `sendAction($action_id, $lineUserId, $botId, ...)` | Trigger action cho LINE user (gửi tin, thay Rich Menu, thêm step, v.v.) | `functions.php:7591` |
| `getTagLineUser($lineId, $bot_id)` | Lấy mảng tag IDs của user (cho Elasticsearch sync) | `functions.php:3850` |
| `addLogUserAction($action)` | Log hành động user | `functions.php:8813` |
| `checkUpdateHasTutorial($botId)` | Kiểm tra tutorial đã hoàn thành chưa | `functions.php:11056` |

---

## Form Requests / Validation

Controller **không sử dụng** FormRequest classes. Validation được thực hiện inline trong controller methods:

| Endpoint | Validation Logic | File:Line |
|----------|-----------------|-----------|
| EP-13 (create-multiple) | Kiểm tra tên tag trùng bằng `Tags::whereIn('name', $arrTagName)->count()` | `TagController.php:279` |
| EP-30 (save-tag add/copy) | Kiểm tra tên rỗng, tên trùng | `TagController.php:1325-1332` |
| EP-30 (save-tag edit) | Kiểm tra tên trùng khi thay đổi tên | `TagController.php:1360-1364` |
| EP-17 (validate-limit) | `count_user_tag > limit` khi bật giới hạn | `TagController.php:1528` |
| EP-16 (restore) | Kiểm tra tên trùng với tag active | `TagController.php:1575-1580` |
| EP-31 (CSV import) | MIME type check, encoding detect | `TagController.php:1428-1444` |

---

## Events / Listeners / Queued Jobs

Controller **không dispatch event hay queue job trực tiếp**. Tuy nhiên:

### Gián tiếp qua `sendAction()`
- **Trigger**: Khi thêm tag cho user (EP-67 addTagForUser) và tag có `action_id`
- **Hàm**: `sendAction($action_id, $lineUserId, $botId, null, '6002', true, [], null, null, null, $tagId)`
- **Chức năng**: Trigger chuỗi actions đã cấu hình cho tag — có thể bao gồm:
  - Gửi tin nhắn LINE
  - Thêm bước (step message)
  - Thay đổi Rich Menu
  - Thêm/gỡ tag khác
  - Gửi thông báo

### Gián tiếp qua `SyncElasticsearch::insertElasticsearch()`
- **Trigger**: Khi thêm/xoá tag-user relationship
- **Bảng**: `sync_elasticsearch` (DB connection: `mysql_step_message`)
- **Type**: `config('sns-line.type_sync.user_tag')`
- **Mô tả**: Insert record → background process (Spring Boot job) đọc và sync sang Elasticsearch
- **Điều kiện**: Chỉ chạy khi `env('API_KEY_ES')` có giá trị

---

## Authorization

| Quyền | Kiểm tra ở đâu | Logic | Ảnh hưởng |
|-------|----------------|-------|----------|
| `basic_access` | Middleware | Kiểm tra user đã đăng nhập và đã chọn bot (có `current_bot_id` trong session) | Chặn truy cập nếu chưa chọn bot — áp dụng cho web routes |
| `admin_access` | Không áp dụng cho Tag routes | — | — |
| `check_login` | Middleware | Kiểm tra user đã đăng nhập (cho AJAX routes) | Chặn AJAX request nếu chưa đăng nhập |
| `is_expire` | Middleware | Kiểm tra tài khoản hết hạn | Chặn truy cập nếu tài khoản expired — chỉ áp dụng cho web routes (EP-01→EP-08) |
| `check_remember_token` | Middleware | Kiểm tra remember token hợp lệ | Tất cả routes |
| `mobile-auth` | Middleware (JWT) | Xác thực JWT token từ mobile app | API routes (EP-60→EP-67) |
| Bot ownership | Controller inline | Mọi query đều filter `bot_id = getBotId()` | Chỉ thao tác trên tag/folder thuộc bot hiện tại |
| Backup lock | Controller inline | Kiểm tra `BackupHistory` status IN (0,1) trước mỗi thao tác write | Chặn CUD khi bot đang backup (data copy) |

**Ghi chú**: Không có Policy hoặc Gate riêng cho Tag. Phân quyền Staff vs Admin được xử lý ở middleware `basic_access` level, không có logic phân quyền chi tiết trong TagController.

---

## Business Rules tổng hợp

| # | Rule | Mô tả | Nơi implement | Confidence |
|---|------|-------|--------------|-----------|
| BR-01 | Tên tag duy nhất | Tên tag phải duy nhất trong cùng bot (bao gồm cả soft deleted nếu restore) | `TagController.php:279` (create-multiple), `:1329` (save-tag), `:1575` (restore) | **Cao** |
| BR-02 | Backup lock | Không cho phép CUD thao tác khi bot đang trong quá trình backup/data copy (BackupHistory status 0 hoặc 1) | Kiểm tra ở đầu mỗi write method | **Cao** |
| BR-03 | Folder 未分類 | Folder 未分類 (category_id=0) là folder mặc định, luôn tồn tại, không xoá được. Tag không thuộc folder nào sẽ vào đây. | Logic kiểm tra category_id=0 xuyên suốt | **Cao** |
| BR-04 | Xoá folder → chuyển tag | Khi xoá folder (v2), tag không bị xoá mà chuyển về 未分類. Lưu ý: legacy (`deleteGroup` action) xoá cả tag. | `TagController.php:240-256` (v2), `:456-477` (legacy) | **Cao** |
| BR-05 | Giới hạn số người | Tag có thể bật giới hạn (`is_limit=1`). Khi đạt limit, không thêm user nữa → trigger `limit_action` thay thế. | `Api\TagController.php:313-326` | **Cao** |
| BR-06 | Limit action mode | `limit_action_mode=0`: chỉ trigger limit action 1 lần/user. Tracking qua `ActionLimitTag`. | `ActionLimitTag.php:25` | **Cao** |
| BR-07 | Action mode (is_2th_apply) | `is_2th_apply=0`: action chỉ trigger lần đầu gán tag. `is_2th_apply=1`: trigger mỗi lần gán. | Xử lý trong `sendAction()` | **Trung bình** (logic nằm trong sendAction, chưa đọc chi tiết) |
| BR-08 | Soft delete 90 ngày | Tag xoá sẽ soft delete (set deleted_at), có thể khôi phục. Dữ liệu tag_line_user bị xoá ngay. | `TagController.php:143-144` (delete), `:1589-1590` (restore reset count=0) | **Cao** |
| BR-09 | CSV import limit | Tối đa 200 tags/file CSV. Tên tag tối đa 50 ký tự. Hỗ trợ SJIS-WIN encoding. Bỏ qua trùng tên. | `TagController.php:1460` (200 limit), `:1471` (50 chars) | **Cao** |
| BR-10 | Xoá tag → cleanup chain | Xoá tag → gỡ khỏi FilterV2, ActionDetail, Landing, tag_line_user, ActionLimitTag. Sync Elasticsearch. | `TagController.php:947-1041` (`deletedDataTag`) | **Cao** |
| BR-11 | Edit tên tag → update form answers | Khi đổi tên tag → cập nhật FormAnswerDetails (select2_5 items) có reference đến tên cũ | `TagController.php:1370-1390` | **Cao** |
| BR-12 | Restore tag → reset count | Khôi phục tag đã xoá sẽ reset `count_user_tag=0` vì `tag_line_user` đã bị xoá khi delete | `TagController.php:1590` | **Cao** |
| BR-13 | Restore tag → restore folder | Nếu folder gốc đã bị soft delete → tự động khôi phục folder khi restore tag | `TagController.php:1584-1588` | **Cao** |
| BR-14 | Category kind | Folder tag có `kind=0`. Config: `config('sns-line.category_kind.tag') = 0` | `config/sns-line.php:293` | **Cao** |
| BR-15 | Position ordering | Tag và folder đều dùng `position` (integer) để sắp xếp. Position = index + 1 khi drag sort. Tag mới nhận position = max + 1 trong folder. | Xuyên suốt controller | **Cao** |
| BR-16 | Elasticsearch sync | Đồng bộ tag data sang Elasticsearch khi thay đổi tag-user relationship. Chỉ chạy khi `API_KEY_ES` env có giá trị. Thông qua bảng `sync_elasticsearch` (DB khác: `mysql_step_message`). | Các method thêm/xoá tag_line_user | **Cao** |
| BR-17 | Tutorial tracking | Khi tạo tag đầu tiên, cập nhật `BotsTutorial.status_tag=1` và kiểm tra tutorial tổng thể. | `TagController.php:323-324` | **Cao** |
| BR-18 | Cookie folder preference | Folder đang chọn được lưu vào cookie `folder_tag` (JSON format, key = bot_id). Cookie expiry = 14400 phút (10 ngày). | `TagController.php:67-78` | **Cao** |
