# FA-012 Quản lý thẻ「タグ管理」 — API Spec

> Phân tích từ source code Laravel (`src/web/sns-line/`).
> Confidence: **Cao** — đọc trực tiếp từ route definitions và controller code.

---

## Danh sách Endpoints

### A. Web Routes — Trang hiển thị (prefix `/basic`, middleware: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`)

| EP | Method | URI | Controller@Action | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-01 | GET | `/basic/tag` | `Basic\TagController@index` | Trang danh sách tag (SCR-TAG-01) |
| EP-02 | GET | `/basic/tag/edit-tag/{id}` | `Basic\TagController@editTag` | Trang chỉnh sửa tag (SCR-TAG-03) |
| EP-03 | GET | `/basic/tag/copy-tag/{id}` | `Basic\TagController@copyTag` | Trang sao chép tag (SCR-TAG-03 chế độ copy) |
| EP-04 | GET | `/basic/tag/add` | `Basic\TagController@addTag` | Trang thêm tag mới (view cũ) |
| EP-05 | GET | `/basic/tag/removed` | `Basic\TagController@tagRemoved` | Trang danh sách tag đã xoá (SCR-TAG-04) |
| EP-06 | GET | `/basic/tag/edit/{id}` | `Basic\TagController@edit` | Trang edit tag (view cũ) |
| EP-07 | GET | `/basic/tag/friend-list/{id}` | `Basic\TagController@friendList` | Trang danh sách bạn bè có tag |
| EP-08 | GET | `tag/tag-member/{id}` | `Basic\TagController@member` | Trang thành viên của tag (view cũ) |

### B. AJAX Routes — v2 Tag API (prefix `/ajax/v2/tag`, middleware: `check_login`, `check_remember_token`)

| EP | Method | URI | Controller@Action | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-10 | GET | `/ajax/v2/tag` | `Basic\TagController@ajaxGetListTag` | Lấy danh sách tag (phân trang, lọc, sắp xếp) |
| EP-11 | DELETE | `/ajax/v2/tag` | `Basic\TagController@ajaxDeleteTags` | Xoá nhiều tag (soft delete) |
| EP-12 | POST | `/ajax/v2/tag/move-category` | `Basic\TagController@ajaxMoveCategory` | Di chuyển tag sang folder khác |
| EP-13 | POST | `/ajax/v2/tag/create-multiple` | `Basic\TagController@ajaxCreateMultipleTags` | Tạo nhiều tag cùng lúc |
| EP-14 | POST | `/ajax/v2/tag/sort-tag` | `Basic\TagController@ajaxSortTag` | Sắp xếp thứ tự tag |
| EP-15 | GET | `/ajax/v2/tag/get-tag-removed` | `Basic\TagController@getTagRemoved` | Lấy danh sách tag đã xoá |
| EP-16 | POST | `/ajax/v2/tag/restore-tag/{id}` | `Basic\TagController@restoreTag` | Khôi phục tag đã xoá |
| EP-17 | POST | `/ajax/v2/tag/validate-limit/{tag}` | `Basic\TagController@validateLimit` | Kiểm tra giới hạn số người trước khi lưu |

### C. AJAX Routes — v2 Tag Category API (prefix `/ajax/v2/tag/category`, middleware: `check_login`, `check_remember_token`)

| EP | Method | URI | Controller@Action | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-20 | GET | `/ajax/v2/tag/category` | `Basic\TagController@ajaxGetCategories` | Lấy danh sách folder tag |
| EP-21 | POST | `/ajax/v2/tag/category/create` | `Basic\TagController@ajaxCreateCategory` | Tạo folder mới |
| EP-22 | PUT | `/ajax/v2/tag/category/update/{category}` | `Basic\TagController@ajaxUpdateCategory` | Đổi tên folder |
| EP-23 | DELETE | `/ajax/v2/tag/category/{id}` | `Basic\TagController@ajaxDeleteCategory` | Xoá folder (soft delete, tags chuyển về 未分類) |
| EP-24 | POST | `/ajax/v2/tag/category/sort-category` | `Basic\TagController@ajaxSortTagCategory` | Sắp xếp thứ tự folder |

### D. AJAX Routes — Tag CRUD legacy (prefix `/ajax`, middleware: `check_login`, `check_remember_token`)

| EP | Method | URI | Controller@Action | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-30 | POST | `/ajax/save-tag` | `Basic\TagController@ajaxSaveTag` | Lưu tag (add/copy/edit — switch action) |
| EP-31 | POST | `/ajax/save-tag-csv` | `Basic\TagController@ajaxSaveTagCsv` | Import tag từ file CSV |
| EP-32 | POST | `/ajax/export-csv-edit` | `Basic\TagController@ajaxExportCsvEdit` | Xuất CSV mẫu cho import |
| EP-33 | GET | `/ajax/downloadCsvEdit` | `Basic\TagController@downloadCsvEdit` | Download file CSV đã xuất |
| EP-34 | POST | `/ajax/get-list-group-tag` | `Basic\TagController@ajaxGetListCategoryTag` | Lấy danh sách folder + tag (legacy — switch action) |
| EP-35 | POST | `/ajax/get-line-user-by-tag` | `Basic\TagController@ajaxGetLineUserByTag` | Lấy danh sách LINE users theo tag |
| EP-36 | POST | `/ajax/remove-line-users-from-tag` | `Basic\TagController@ajaxRemoveLineUsersFromTag` | Gỡ LINE users khỏi tag |
| EP-37 | POST | `/ajax/get-category-tag-list` | `Basic\TagController@getCategoryTagList` | Lấy tag theo category ID |

### E. Web Routes — Legacy CRUD (prefix `/basic`, middleware: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`)

| EP | Method | URI | Controller@Action | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-40 | POST | `/basic/add-category-tag` | `Basic\TagController@createCategoryTag` | Tạo folder tag (legacy) |
| EP-41 | GET | `/basic/delete-category-tag/{id}` | `Basic\TagController@deleteCategoryTag` | Xoá folder tag (legacy) |
| EP-42 | POST | `/basic/add-tag` | `Basic\TagController@createTag` | Tạo tag mới (legacy) |
| EP-43 | GET | `/basic/find-tag` | `Basic\TagController@findTag` | Tìm kiếm tag (legacy) |
| EP-44 | POST | `/basic/tag/delete-user` | `Basic\TagController@deleteUser` | Xoá liên kết user khỏi tag |
| EP-45 | POST | `/basic/tag/update` | `Basic\TagController@update` | Cập nhật tag (legacy form submit) |
| EP-46 | POST | `/basic/tag/delete` | `Basic\TagController@deleteTag` | Xoá tag (legacy form submit) |
| EP-47 | POST | `/basic/initDataInfoTag` | `Basic\TagController@initDataInfo` | Lấy data chi tiết tag + action settings |
| EP-48 | POST | `/basic/getFolder` | `Basic\TagController@getFolder` | Lấy danh sách folder (friend info kind) |

### F. Utility (không yêu cầu middleware chính)

| EP | Method | URI | Controller@Action | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-50 | GET | `/basic/tag/set-cookie` | `Basic\BasicController@folderSetCookie` | Lưu folder đang chọn vào cookie |

### G. API Routes — Mobile (prefix `/api/mobile`, middleware: `mobile-auth`)

| EP | Method | URI | Controller@Action | Mô tả |
|----|--------|-----|-------------------|-------|
| EP-60 | POST | `/api/get-list-tag-of-user-v2` | `Api\TagController@getTagOfUserV2` | Lấy tag của user (grouped by folder) |
| EP-61 | POST | `/api/get-list-tag-of-user` | `Api\TagController@getTagOfUser` | Lấy tag của user (flat list) |
| EP-62 | POST | `/api/remove-tag-of-user-v2` | `Api\TagController@removeTagOfUserV2` | Gỡ nhiều tag khỏi user |
| EP-63 | POST | `/api/remove-tag-of-user` | `Api\TagController@removeTagOfUser` | Gỡ 1 tag khỏi user |
| EP-64 | POST | `/api/get-list-folder-tag-by-bot-v2` | `Api\TagController@getListFolderTagByBotV2` | Lấy folder + tags (with nested tags) |
| EP-65 | POST | `/api/get-list-folder-tag-by-bot` | `Api\TagController@getListFolderTagByBot` | Lấy folder + count (without nested tags) |
| EP-66 | POST | `/api/get-list-tag-by-category` | `Api\TagController@getListTagByCategory` | Lấy tag theo category |
| EP-67 | POST | `/api/add-tag-for-user` | `Api\TagController@addTagForUser` | Thêm/xoá tag cho user (sync full) |

---

## Chi tiết Endpoints

### EP-10: GET `/ajax/v2/tag`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxGetListTag`
- **File**: `app/Http/Controllers/Basic/TagController.php:90`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Lấy danh sách tag của bot hiện tại, hỗ trợ lọc theo folder, tìm kiếm keyword, sắp xếp nhiều cột, phân trang.
- **Liên kết UI**: SCR-TAG-01 → Bảng danh sách tag chính

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `category_id` | Query | Integer | Không | ID folder lọc (0 = 未分類) | — |
| `keyword` | Query | String | Không | Từ khoá tìm kiếm theo tên tag | — |
| `type` | Query | String | Không | Nếu = `sort_item` thì chỉ select `id`, `name` | — |
| `limit` | Query | Integer | Không | Số tag mỗi trang (mặc định 15) | — |
| `unlimit` | Query | Boolean | Không | Nếu true, lấy tất cả không phân trang | — |
| `orders` | Query | Array | Không | Mảng sort: `orders[0][column]`, `orders[0][dir]` | column ∈ {`created_at`, `position`, `name`, `updated_at`}, dir ∈ {`ASC`, `DESC`} |

#### Request mẫu
```
GET /ajax/v2/tag?category_id=0&keyword=&type=&orders[0][column]=position&orders[0][dir]=DESC&limit=100&page=1
```

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success",
  "data": {
    "current_page": 1,
    "data": [
      {
        "id": 123,
        "bot_id": 456,
        "name": "新規友だち",
        "category_id": 0,
        "action_id": 789,
        "limit_action_id": null,
        "is_limit": 0,
        "limit": null,
        "count_user_tag": 42,
        "position": 10,
        "is_2th_apply": 0,
        "created_at": "2024-01-15 10:30:00",
        "updated_at": "2024-06-20 14:00:00",
        "action": {
          "id": 789,
          "details": [...]
        }
      }
    ],
    "last_page": 3,
    "per_page": 100,
    "total": 250
  }
}
```

#### Response lỗi
Không có xử lý lỗi rõ — nếu exception xảy ra, Laravel trả 500 mặc định.

---

### EP-11: DELETE `/ajax/v2/tag`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxDeleteTags`
- **File**: `app/Http/Controllers/Basic/TagController.php:124`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Soft delete nhiều tag cùng lúc. Kiểm tra backup trước khi xoá. Gỡ tag khỏi Landing pages liên quan. Dọn dẹp dữ liệu liên quan (filter, action details, tag_line_user, Elasticsearch).
- **Liên kết UI**: SCR-TAG-01 → Chọn checkbox + nút xoá ở toolbar bottom

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `ids` | Body | Array<Integer> | Có | Mảng ID tag cần xoá | — |

#### Request mẫu
```json
{
  "ids": [123, 456, 789]
}
```

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success"
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Bot đang trong quá trình backup/data copy | `{"status": false, "msg": "データコピー中は、データ不備を回避するために、編集不可能です。少し待ってから操作し直してください。"}` |
| 500 | Exception bất kỳ | `{"message": "{error_message}"}` |

---

### EP-12: POST `/ajax/v2/tag/move-category`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxMoveCategory`
- **File**: `app/Http/Controllers/Basic/TagController.php:169`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Di chuyển nhiều tag sang folder khác. Tag được di chuyển sẽ có position mới (max position + 1).
- **Liên kết UI**: SCR-TAG-01 → Chọn checkbox + nút di chuyển folder ở toolbar bottom

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `ids` | Body | Array<Integer> | Có | Mảng ID tag cần di chuyển | — |
| `folder_move_id` | Body | Integer | Có | ID folder đích (0 = 未分類) | — |

#### Request mẫu
```json
{
  "ids": [123, 456],
  "folder_move_id": 5
}
```

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success"
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Bot đang backup | `{"status": false, "msg": "データコピー中は..."}` |

---

### EP-13: POST `/ajax/v2/tag/create-multiple`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxCreateMultipleTags`
- **File**: `app/Http/Controllers/Basic/TagController.php:273`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Tạo nhiều tag cùng lúc (bulk insert). Kiểm tra trùng tên tag, bỏ qua tag name rỗng. Cập nhật trạng thái tutorial.
- **Liên kết UI**: SCR-TAG-01/SCR-TAG-02 → Dialog tạo mới cho phép nhập nhiều tên

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `tags` | Body | Array<Object> | Có | Mảng object chứa `name` | Tag name không được trùng tên đã tồn tại |
| `category_id` | Body | Integer | Không | ID folder (mặc định 0 = 未分類) | — |

#### Request mẫu
```json
{
  "tags": [
    {"name": "新規タグ1"},
    {"name": "新規タグ2"}
  ],
  "category_id": 5
}
```

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success",
  "first_tag_id": 789
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Tên tag đã tồn tại | `{"message": "そのタグ名はすでに利用されています"}` |

---

### EP-14: POST `/ajax/v2/tag/sort-tag`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxSortTag`
- **File**: `app/Http/Controllers/Basic/TagController.php:340`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Sắp xếp thứ tự tag (drag & drop).
- **Liên kết UI**: SCR-TAG-01 → Nút「並べ替え」(sort) tag panel

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `sort_ids` | Body | String | Có | Chuỗi ID tag phân cách bởi dấu phẩy | — |

#### Request mẫu
```json
{
  "sort_ids": "789,456,123"
}
```

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success"
}
```

---

### EP-15: GET `/ajax/v2/tag/get-tag-removed`
- **Controller**: `App\Http\Controllers\Basic\TagController@getTagRemoved`
- **File**: `app/Http/Controllers/Basic/TagController.php:1537`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Lấy danh sách tag đã xoá (soft deleted). Hỗ trợ sắp xếp và phân trang. Kèm tên người xoá.
- **Liên kết UI**: SCR-TAG-04 → Bảng tag đã xoá

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `order` | Query | String | Không | Cột sắp xếp | — |
| `dir` | Query | String | Không | Hướng sắp xếp: `ASC`/`DESC` | — |
| `limit` | Query | Integer | Không | Số tag mỗi trang (mặc định 15) | — |
| `page` | Query | Integer | Không | Trang hiện tại | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "success": true,
  "data": {
    "current_page": 1,
    "data": [
      {
        "id": 123,
        "name": "旧タグ",
        "bot_id": 456,
        "deleted_at": "2024-03-01 10:00:00",
        "user_id_del": 78,
        "username_del": "admin_user"
      }
    ],
    "last_page": 1,
    "per_page": 15,
    "total": 5
  }
}
```

---

### EP-16: POST `/ajax/v2/tag/restore-tag/{id}`
- **Controller**: `App\Http\Controllers\Basic\TagController@restoreTag`
- **File**: `app/Http/Controllers/Basic/TagController.php:1566`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Khôi phục tag đã xoá. Kiểm tra trùng tên trước khi restore. Nếu folder gốc đã bị xoá → khôi phục folder. Reset count_user_tag về 0.
- **Liên kết UI**: SCR-TAG-04 → Nút khôi phục trên dòng tag đã xoá

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `id` | Path | Integer | Có | ID tag cần khôi phục | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "success": true
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 404 | Tag không tìm thấy | Exception `Tag not found!` |
| 500 | Tên tag đã tồn tại (trùng tên tag active) | `{"success": false, "message": "そのタグ名はすでに利用されています"}` |

---

### EP-17: POST `/ajax/v2/tag/validate-limit/{tag}`
- **Controller**: `App\Http\Controllers\Basic\TagController@validateLimit`
- **File**: `app/Http/Controllers/Basic/TagController.php:1526`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Kiểm tra giới hạn người: nếu số người hiện tại > limit mới đặt → trả lỗi (trừ khi đang copy).
- **Liên kết UI**: SCR-TAG-03 → Kiểm tra trước khi lưu cài đặt giới hạn

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `tag` | Path | Integer (Tag model) | Có | ID tag (route model binding) | — |
| `is_limit` | Body | Boolean | Không | Có bật giới hạn không | — |
| `limit` | Body | Integer | Không | Số người giới hạn | — |
| `isCopy` | Body | Integer | Không | =1 nếu đang copy tag (bỏ qua kiểm tra) | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "passed"
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | count_user_tag > limit mới | `{"message": "入力した制限人数が、タグが付与された人数を下回っています。"}` |

---

### EP-20: GET `/ajax/v2/tag/category`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxGetCategories`
- **File**: `app/Http/Controllers/Basic/TagController.php:161`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Lấy danh sách folder tag (category kind=0) + số lượng tag 未分類 (category_id=0).
- **Liên kết UI**: SCR-TAG-01 → Sidebar folder panel

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success",
  "data": {
    "categories": [
      {
        "id": 1,
        "name": "最終編集",
        "kind": 0,
        "position": 5,
        "count": 175
      },
      {
        "id": 2,
        "name": "絞り込み条件",
        "kind": 0,
        "position": 4,
        "count": 2
      }
    ],
    "count_default": 4
  }
}
```

---

### EP-21: POST `/ajax/v2/tag/category/create`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxCreateCategory`
- **File**: `app/Http/Controllers/Basic/TagController.php:198`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Tạo folder tag mới. Kind cố định = 0 (tag). Position = max + 1.
- **Liên kết UI**: SCR-TAG-01 → Nút「フォルダ追加」

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `name` | Body | String | Có | Tên folder | — |

#### Request mẫu
```json
{
  "name": "新しいフォルダ"
}
```

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success",
  "item": {
    "id": 10,
    "bot_id": 456,
    "name": "新しいフォルダ",
    "kind": 0,
    "position": 6,
    "count": 0
  }
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Bot đang backup | `{"status": false, "msg": "データコピー中は..."}` |

---

### EP-22: PUT `/ajax/v2/tag/category/update/{category}`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxUpdateCategory`
- **File**: `app/Http/Controllers/Basic/TagController.php:266`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Đổi tên folder. Route model binding cho Category.
- **Liên kết UI**: SCR-TAG-01 → Menu context folder → Sửa tên

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `category` | Path | Integer (Category model) | Có | ID folder | Route model binding |
| `name` | Body | String | Có | Tên mới | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success"
}
```

---

### EP-23: DELETE `/ajax/v2/tag/category/{id}`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxDeleteCategory`
- **File**: `app/Http/Controllers/Basic/TagController.php:225`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Xoá folder (soft delete bằng `is_deleted=1`). Tags trong folder được chuyển về 未分類 (category_id=0) với position mới.
- **Liên kết UI**: SCR-TAG-01 → Menu context folder → Xoá

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `id` | Path | Integer | Có | ID folder cần xoá | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success"
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 500 | Bot đang backup | `{"status": false, "msg": "データコピー中は..."}` |
| 500 | Exception | `{"status": false, "msg": "\"保存に失敗しました\""}` |

---

### EP-24: POST `/ajax/v2/tag/category/sort-category`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxSortTagCategory`
- **File**: `app/Http/Controllers/Basic/TagController.php:328`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Sắp xếp thứ tự folder (drag & drop).
- **Liên kết UI**: SCR-TAG-01 → Nút「並べ替え」sidebar folder

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `sort_ids` | Body | String | Có | Chuỗi ID folder phân cách bởi dấu phẩy | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "message": "success"
}
```

---

### EP-30: POST `/ajax/save-tag`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxSaveTag`
- **File**: `app/Http/Controllers/Basic/TagController.php:1306`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Lưu tag — xử lý 3 action: `add_tag` (thêm mới), `copy_tag` (sao chép), `edit_tag` (chỉnh sửa). Kiểm tra trùng tên, lưu action settings, giới hạn người. Khi edit tên tag, cập nhật cả FormAnswerDetails liên quan.
- **Liên kết UI**: SCR-TAG-03 → Nút lưu trên trang edit/add/copy

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `action` | Body | String | Có | Loại thao tác: `add_tag`, `copy_tag`, `edit_tag` | — |
| `tag_id` | Body | Integer | Có (edit) | ID tag cần sửa | — |
| `tag_name` | Body | String | Có | Tên tag | Không được rỗng, không trùng tên tag khác |
| `category_id` | Body | Integer | Không | ID folder (mặc định 0) | — |
| `action_id` | Body | Integer | Không | ID action khi thêm tag | — |
| `limit_action_id` | Body | Integer | Không | ID action khi đạt giới hạn | — |
| `action_mode` | Body | Integer | Không | Chế độ action: 0 = chỉ lần đầu, 1 = mỗi lần | — |
| `is_limit` | Body | Boolean | Không | Có bật giới hạn người | — |
| `limit` | Body | Integer | Không | Số người giới hạn (khi is_limit = true) | — |
| `limit_action_mode` | Body | Integer | Không | Chế độ action giới hạn: 0 = chỉ lần đầu | — |

#### Request mẫu (edit_tag)
```json
{
  "action": "edit_tag",
  "tag_id": 123,
  "tag_name": "更新されたタグ",
  "category_id": 5,
  "action_id": 789,
  "limit_action_id": null,
  "action_mode": 0,
  "is_limit": false,
  "limit": null,
  "limit_action_mode": 0
}
```

#### Response mẫu (thành công) — HTTP 200
```json
{
  "status": true,
  "msg": ""
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | Tên rỗng (add/copy) | `{"status": false, "msg": "新しいタグ名を入力してください"}` |
| 200 | Tên trùng | `{"status": false, "msg": "そのタグ名はすでに利用されています"}` |
| 500 | Bot đang backup | `{"status": false, "msg": "データコピー中は..."}` |

---

### EP-31: POST `/ajax/save-tag-csv`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxSaveTagCsv`
- **File**: `app/Http/Controllers/Basic/TagController.php:1421`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Import tag từ file CSV. Hỗ trợ encoding SJIS-WIN và UTF-8. Tối đa 200 tag. Bỏ qua tên trùng. Tên tag bị cắt tối đa 50 ký tự.
- **Liên kết UI**: SCR-TAG-01 → Nút「CSV一括追加」

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `csv_file` | Body (multipart) | File | Có | File CSV chứa danh sách tên tag | MIME type phải là CSV-compatible |
| `folder_add_id` | Body | Integer | Không | ID folder đích | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "status": true,
  "msg": ""
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | File không phải CSV | `{"success": false, "message": "CSVファイルを選択してください。"}` |

---

### EP-32: POST `/ajax/export-csv-edit`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxExportCsvEdit`
- **File**: `app/Http/Controllers/Basic/TagController.php:1514`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Tạo file CSV mẫu trống với header「追加するタグ名を2行目から入力してください（最大200個まで）」
- **Liên kết UI**: SCR-TAG-01 → Download CSV template từ dialog import

#### Response mẫu (thành công) — HTTP 200
```json
{
  "file_name": "編集用CSV.csv"
}
```

---

### EP-33: GET `/ajax/downloadCsvEdit`
- **Controller**: `App\Http\Controllers\Basic\TagController@downloadCsvEdit`
- **File**: `app/Http/Controllers/Basic/TagController.php:1521`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Download file CSV đã được tạo bởi EP-32.

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `fileName` | Query | String | Có | Tên file CSV | — |

#### Response
Binary file download.

---

### EP-35: POST `/ajax/get-line-user-by-tag`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxGetLineUserByTag`
- **File**: `app/Http/Controllers/Basic/TagController.php:1239`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Lấy danh sách LINE users đã gán tag. Phân trang 50 users/trang. Hiển thị tên + avatar.
- **Liên kết UI**: EP-07 (SCR-TAG-05) → Bảng danh sách bạn bè có tag

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `id` | Body | Integer | Có | ID tag | — |
| `page` | Body | Integer | Không | Trang (mặc định 1) | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "status": true,
  "line_user_list": {
    "current_page": 1,
    "from": 1,
    "to": 2,
    "last_page": 2,
    "data": [
      {
        "id": 100,
        "name": "田中太郎",
        "avatar_url": "https://..."
      }
    ],
    "total": 85,
    "per_page": 50
  }
}
```

---

### EP-36: POST `/ajax/remove-line-users-from-tag`
- **Controller**: `App\Http\Controllers\Basic\TagController@ajaxRemoveLineUsersFromTag`
- **File**: `app/Http/Controllers/Basic/TagController.php:1270`
- **Middleware**: `check_login`, `check_remember_token`
- **Mô tả**: Gỡ nhiều LINE users khỏi tag. Giảm count_user_tag. Đồng bộ Elasticsearch.
- **Liên kết UI**: SCR-TAG-05 → Chọn users + nút xoá

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `list_line_user_id` | Body | Array<Integer> | Có | Mảng ID LINE user | — |
| `tag_id` | Body | Integer | Có | ID tag | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "status": true,
  "msg": ""
}
```

---

### EP-47: POST `/basic/initDataInfoTag`
- **Controller**: `App\Http\Controllers\Basic\TagController@initDataInfo`
- **File**: `app/Http/Controllers/Basic/TagController.php:1043`
- **Middleware**: `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`
- **Mô tả**: Lấy dữ liệu chi tiết tag kèm action settings. Nếu action = `copy_tag`, clone action trước khi trả về.
- **Liên kết UI**: SCR-TAG-03 → Load dữ liệu khi mở trang edit/copy

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `id` | Body | Integer | Có | ID tag | — |
| `action` | Body | String | Không | Nếu = `copy_tag` → clone action | — |

#### Response mẫu (thành công) — HTTP 200
```json
{
  "status": true,
  "data": {
    "id": 123,
    "name": "新規友だち",
    "bot_id": 456,
    "category_id": 5,
    "action_id": 789,
    "limit_action_id": null,
    "is_limit": 0,
    "limit": null,
    "is_2th_apply": 0,
    "count_user_tag": 42,
    "setting_actions": [...],
    "setting_limit_actions": []
  }
}
```

---

### EP-67: POST `/api/add-tag-for-user`
- **Controller**: `App\Http\Controllers\Api\TagController@addTagForUser`
- **File**: `app/Http/Controllers/Api/TagController.php:289`
- **Middleware**: `mobile-auth` (JWT)
- **Mô tả**: Thêm/xoá tag cho LINE user (đồng bộ full — so sánh tag cũ vs mới). Khi thêm tag: kiểm tra giới hạn, trigger action. Khi giới hạn đầy: trigger limit action thay vì thêm tag. Đồng bộ Elasticsearch.
- **Ghi chú quan trọng**: Gọi hàm `sendAction()` khi thêm tag có `action_id` → có thể trigger gửi tin nhắn, thêm bước, v.v.

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `botId` | Body | Integer | Có | ID bot | — |
| `lineUserId` | Body | Integer | Có | ID LINE user | — |
| `tagIds` | Body | Array<Integer> | Có | Mảng ID tag mới (full set — sẽ diff với tag cũ) | — |

---

## Middleware phân tích

| Middleware | Class | Mô tả | Áp dụng cho |
|-----------|-------|-------|------------|
| `basic_access` | `App\Http\Middleware\BasicAccess` | Kiểm tra quyền truy cập basic (user đã chọn bot) | EP-01→EP-08, EP-40→EP-48 |
| `https_protocol` | — | Đảm bảo HTTPS | EP-01→EP-08, EP-40→EP-48 |
| `is_expire` | `App\Http\Middleware\IsExpire` | Kiểm tra tài khoản hết hạn | EP-01→EP-08, EP-40→EP-48 |
| `check_remember_token` | `App\Http\Middleware\CheckRememberToken` | Kiểm tra remember token | Tất cả endpoints |
| `check_login` | `App\Http\Middleware\CheckLogin` | Kiểm tra đăng nhập (AJAX) | EP-10→EP-37 |
| `mobile-auth` | — | JWT authentication cho mobile app | EP-60→EP-67 |

---

## Liên kết UI ↔ API

| Màn hình | Action trên UI | Endpoint | Ghi chú |
|---------|--------|----------|---------|
| SCR-TAG-01 | Render trang danh sách | EP-01 | GET /basic/tag — trả view Blade |
| SCR-TAG-01 | Load danh sách tag | EP-10 | AJAX GET /ajax/v2/tag — phân trang, sắp xếp |
| SCR-TAG-01 | Load danh sách folder | EP-20 | AJAX GET /ajax/v2/tag/category |
| SCR-TAG-01 | Tạo folder mới | EP-21 | AJAX POST /ajax/v2/tag/category/create |
| SCR-TAG-01 | Đổi tên folder | EP-22 | AJAX PUT /ajax/v2/tag/category/update/{id} |
| SCR-TAG-01 | Xoá folder | EP-23 | AJAX DELETE /ajax/v2/tag/category/{id} |
| SCR-TAG-01 | Sắp xếp folder | EP-24 | AJAX POST /ajax/v2/tag/category/sort-category |
| SCR-TAG-01 | Tạo tag mới (quick) | EP-13 | AJAX POST /ajax/v2/tag/create-multiple |
| SCR-TAG-01 | Import CSV | EP-31 | AJAX POST /ajax/save-tag-csv |
| SCR-TAG-01 | Download CSV template | EP-32 + EP-33 | Export → Download |
| SCR-TAG-01 | Sắp xếp tag | EP-14 | AJAX POST /ajax/v2/tag/sort-tag |
| SCR-TAG-01 | Xoá tag (nhiều) | EP-11 | AJAX DELETE /ajax/v2/tag |
| SCR-TAG-01 | Di chuyển tag sang folder | EP-12 | AJAX POST /ajax/v2/tag/move-category |
| SCR-TAG-01 | Lưu folder cookie | EP-50 | GET /basic/tag/set-cookie |
| SCR-TAG-03 | Render trang edit | EP-02 | GET /basic/tag/edit-tag/{id} |
| SCR-TAG-03 | Render trang copy | EP-03 | GET /basic/tag/copy-tag/{id} |
| SCR-TAG-03 | Load dữ liệu tag | EP-47 | AJAX POST /basic/initDataInfoTag |
| SCR-TAG-03 | Validate giới hạn | EP-17 | AJAX POST /ajax/v2/tag/validate-limit/{tag} |
| SCR-TAG-03 | Lưu tag (add/edit/copy) | EP-30 | AJAX POST /ajax/save-tag |
| SCR-TAG-04 | Render trang đã xoá | EP-05 | GET /basic/tag/removed |
| SCR-TAG-04 | Load tag đã xoá | EP-15 | AJAX GET /ajax/v2/tag/get-tag-removed |
| SCR-TAG-04 | Khôi phục tag | EP-16 | AJAX POST /ajax/v2/tag/restore-tag/{id} |
| SCR-TAG-05 | Render trang bạn bè | EP-07 | GET /basic/tag/friend-list/{id} |
| SCR-TAG-05 | Load danh sách users | EP-35 | AJAX POST /ajax/get-line-user-by-tag |
| SCR-TAG-05 | Gỡ users khỏi tag | EP-36 | AJAX POST /ajax/remove-line-users-from-tag |
