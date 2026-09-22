# API Spec — FA-014 「CSV管理」 (Quản lý CSV)

> Portal: **Admin (LINE OA)** — feature folder `features/admin/csv-management/`
> Nguồn: `src/web/sns-line` (Laravel 5 + PHP 7.2). Mọi đường dẫn dưới đây tương đối với thư mục đó.
> Controller chính: `app/Http/Controllers/CsvManagementController.php` (960 dòng)

---

## 1. Bảng tổng hợp endpoints

| ID | Method | URL | Mô tả | Controller@Method | Middleware | Xác thực |
|----|--------|-----|-------|-------------------|-----------|----------|
| EP-01 | `GET` | `/basic/csv-management` | Render trang chính (2 tab エクスポート / インポート) | `CsvManagementController@index` (`:57`) | `basic_access, https_protocol, is_expire, check_remember_token` | Có |
| EP-02 | `GET` | `/basic/csv-management/create-download-file` | Render form tạo mới 「エクスポートデータ作成」 | `CsvManagementController@createDownloadFile` (`:67`) | `basic_access, https_protocol, is_expire, check_remember_token` | Có |
| EP-03 | `GET` | `/basic/csv-management/edit-download-file/{id}` | Render form sửa | `CsvManagementController@editDownloadFile` (`:89`) | `basic_access, https_protocol, is_expire, check_remember_token` | Có |
| EP-04 | `GET` | `/basic/csv-management/copy-download-file/{id}` | Render form nhân bản 「コピー」 | `CsvManagementController@copyDownloadFile` (`:116`) | `basic_access, https_protocol, is_expire, check_remember_token` | Có |
| EP-05 | `POST` | `/ajax/init-csv-management` | Multiplex: nạp danh sách export + `sortItem` / `deleteItem` / `deleteItems` | `CsvManagementController@ajaxInitCsvManagement` (`:311`) | `check_login, check_remember_token` (group `ajax` — `routes/web.php:2485`) | Có (CSRF **được miễn** — `/ajax/*`) |
| EP-06 | `POST` | `/ajax/init-import-csv-management` | Nạp bảng 「インポート履歴」 | `CsvManagementController@ajaxInitImportCsvManagement` (`:602`) | `check_login, check_remember_token` | Có (CSRF miễn) |
| EP-07 | `POST` | `/ajax/init-friend-information-for-csv` | Nạp cây 「友だち情報」 theo phân loại | `CsvManagementController@ajaxInitFriendInformationForCsv` (`:216`) | `check_login, check_remember_token` | Có (CSRF miễn) |
| EP-08 | `POST` | `/ajax/get-list-group-tag-for-csv` | Nạp cây 「タグ」 theo nhóm | `CsvManagementController@ajaxGetListCategoryTag` (`:143`) | `check_login, check_remember_token` (`routes/web.php:2910`) | Có (CSRF miễn) |
| EP-09 | `POST` | `/ajax/csv-management/save-filter` | Lưu (tạo/sửa) định nghĩa export — nút 「この条件でCSVを作成・更新」 | `CsvManagementController@saveFilter` (`:428`) | ⚠ **KHÔNG có middleware xác thực** (`routes/web.php:4015`) | **Không** |
| EP-10 | `GET` | `/ajax/initDataFilterCsvManagement` | Nạp lại điều kiện lọc đã lưu (modal 絞り込み / màn 友だちリスト) | `Basic\FriendlistController@initDataFilterCsvManagement` (`:4536`) | ⚠ **KHÔNG có middleware xác thực** (`routes/web.php:3980`) | **Không** |
| EP-11 | `POST` | `/basic/csv-management/update-latest-information` | Nút 「最新情報に更新」 — đặt lại trạng thái để job build lại file | `CsvManagementController@updateLatestInformation` (`:941`) | `basic_access, https_protocol, is_expire, check_remember_token` | Có |
| EP-12 | `POST` | `/basic/csv-management/export` | Lấy tên file CSV đã sinh (bước 1 của 「CSVダウンロード」) | `CsvManagementController@csvExport` (`:386`) | `basic_access, https_protocol, is_expire, check_remember_token` | Có |
| EP-13 | `GET` | `/basic/csv-management/download-csv` | Tải file CSV/ZIP về (bước 2 của 「CSVダウンロード」) | `CsvManagementController@downloadCsv` (`:405`) | `check_login, check_remember_token` (`routes/web.php:1934`) | Có |
| EP-14 | `POST` | `/basic/csv-management/read_file_csv` | Đọc + validate file CSV upload (preview, chưa lưu) | `CsvManagementController@readFileCsv` (`:619`) | `basic_access, https_protocol, is_expire, check_remember_token` | Có |
| EP-15 | `POST` | `/basic/csv-management/save_file_csv` | Nút 「アップロード」 (`csvSave()`) — lưu file + tạo bản ghi lịch sử import | `CsvManagementController@saveFileCsv` (`:894`) | `basic_access, https_protocol, is_expire, check_remember_token` | Có |

**Khai báo route:** `routes/web.php:947, 949, 951, 953, 955, 957, 959, 961, 1934, 2910, 3018, 3020, 3022, 3980, 4015`.

> Không có endpoint riêng cho 「並べ替え」 hay 「一括削除」 — cả hai đi qua EP-05 với `action=sortItem` / `action=deleteItems`. Nút 「新規作成」 và menu 「コピー」 chỉ là `window.location.href` phía client (`public/js/csv_management/csv_management.js:253, 264`).

---

## 2. Chi tiết endpoints

### EP-01 — `GET /basic/csv-management`

Render view `csv_management.csv_management` (không truyền biến). Toàn bộ dữ liệu do Vue nạp qua EP-05 / EP-06.

- **Params:** không
- **Response:** HTML
- **Lỗi:** `Exception` bất kỳ → `Log::error` + `redirect()->route('404')` (`app/Http/Controllers/CsvManagementController.php:61-63`)

---

### EP-02 — `GET /basic/csv-management/create-download-file`

Render view `csv_management.create_download_file`.

| Biến truyền view | Nguồn |
|---|---|
| `scenario` | `ScenarioRepositoryInterface::findByBot($bot_id)` |
| `conversion` | `Conversion::select('name','id')->where('bot_id', $bot_id)` |
| `richMenus` | `RichMenus::where('bot_id', getBotId())->where('status_rich', 1)` |
| `bot_id` | `getBotId()` |
| `statusObject` | `StatusChat::where('bot_id', $bot_id)` |

- **Lỗi:** exception → redirect `404`

---

### EP-03 — `GET /basic/csv-management/edit-download-file/{id}`

Giống EP-02, thêm `csv_id = {id}` và `item = CsvManagement::where(['id' => $csvId])->first()` (`CsvManagementController.php:99`).

| Param | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `id` | route | int | Có | **Không có** — không kiểm tra tồn tại, không kiểm tra `bot_id` |

> ⚠ **IDOR**: truy vấn chỉ lọc theo `id`, không kèm `bot_id` → Admin của bot A xem được cấu hình export của bot B. Tin cậy: **Cao** (đọc trực tiếp `:99`).

---

### EP-04 — `GET /basic/csv-management/copy-download-file/{id}`

Giống EP-03 nhưng truyền `copy_id` thay cho `csv_id` (`:135`) → JS đặt `save_action` = tạo mới. Cùng lỗ hổng IDOR (`:128`).

---

### EP-05 — `POST /ajax/init-csv-management`

Endpoint đa năng, phân nhánh theo `action` (`:314`).

| Param | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `action` | body | string | Không | `initData` \| `sortItem` \| `deleteItem` \| `deleteItems`. Giá trị lạ → chỉ trả danh sách |
| `sort_ids` | body | string CSV | Khi `action=sortItem` | Danh sách id nối bằng `,` (JS đảo ngược thứ tự trước khi gửi) |
| `sort_position` | body | string CSV | Khi `action=sortItem` | Danh sách position nối bằng `,`, được `array_sort()` trước khi gán |
| `csv_id` | body | int | Khi `action=deleteItem` | |
| `csv_ids` | body | int[] | Khi `action=deleteItems` | Mảng id (checkbox chọn nhiều) |

**Không có FormRequest, không có rule Validator nào cho endpoint này.** (Tin cậy: **Cao**)

**Request mẫu**

```json
{ "action": "initData" }
```

```json
{ "action": "deleteItems", "csv_ids": [12, 15] }
```

```json
{ "action": "sortItem", "sort_ids": "15,12,9", "sort_position": "1,2,3" }
```

**Response thành công** (HTTP 200)

```json
{
  "status": true,
  "items": [
    {
      "id": 12,
      "bot_id": 3421,
      "name": "有効友だち_全件",
      "enable_filter_friend": 1,
      "enable_bot_block_friend": 0,
      "enable_friend_block_bot": 0,
      "line_user_ids": null,
      "total_line_user": 1287,
      "file_name": null,
      "file_name_new": "/media/csv/3421/export_12_20260901.csv",
      "filter_update_status": 30,
      "export_tags": "[\"18\",\"22\"]",
      "export_friend_info_setting_value": "[\"-1\",\"305\"]",
      "show_message_status": 1,
      "show_note": 0,
      "show_date_of_add_friend": 1,
      "show_reciprocal_status": 0,
      "show_date_of_last_message_received": 1,
      "show_running_step": 0,
      "show_qr_code": 0,
      "position": 3,
      "date_of_last_change_of_condition": "2026-09-01 10:22:31",
      "created_at": "2026-08-12 09:00:00",
      "updated_at": "2026-09-01 10:30:02"
    }
  ],
  "isAdd": true
}
```

- `items`: `CsvManagement::where(['bot_id' => $bot_id])->orderBy('position','DESC')` (`:355`) — **có** lọc `bot_id`.
- `isAdd`: `false` khi `bots.flag_contract_new == 1` và (`contract_type == 'free'` hoặc `bots.plan_type == 2`) và đã có ≥ 1 bản ghi (`:357-365`). Dùng để chặn nút 「新規作成」 / 「コピー」 phía client.

**Lỗi**

| HTTP | Body | Nguyên nhân |
|---|---|---|
| 200 | `{"status": false, "msg": "<exception message>"}` | Mọi `\Exception` (`:373-376`) — **rò rỉ thông báo lỗi nội bộ ra client** |

> ⚠ Nhánh `sortItem` (`:319-334`), `deleteItem` (`:336-346`), `deleteItems` (`:348-354`) **không kiểm tra `bot_id`** khi thao tác trên `csv_management` (chỉ `filters_v2` mới có `where('bot_id', $bot_id)`). Bot A có thể xoá / đổi thứ tự bản ghi của bot B. Tin cậy: **Cao**.
> ⚠ `DB::beginTransaction()` / `commit()` / `rollback()` đều bị comment (`:312`, `:366`, `:374`) → xoá `csv_management` và `filters_v2` **không nguyên tử**.

---

### EP-06 — `POST /ajax/init-import-csv-management`

| Param | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `action` | body | string | Không (không được dùng trong code) |

**Response**

```json
{
  "status": true,
  "history_upload_filter_items": [
    {
      "id": 88,
      "bot_id": 3421,
      "number_line_user": 120,
      "name": "friends_20260901.csv",
      "upload_status": 2,
      "friend_info_setting_ids": null,
      "tag_ids": null,
      "data": null,
      "path_file": "/media/csv/9912/3421/friends_20260901.csv",
      "message_error": null,
      "is_action_tag": 1,
      "is_action_info_friend": 0,
      "created_at": "2026-09-01 11:02:00",
      "updated_at": "2026-09-01 11:03:10"
    }
  ]
}
```

Truy vấn: `CsvFilterUploadHistory::where(['bot_id' => $bot_id])->orderBy('id','desc')` (`:606`) — có lọc `bot_id`.

**Lỗi:** 200 + `{"status": false, "msg": "..."}`

---

### EP-07 — `POST /ajax/init-friend-information-for-csv`

| Param | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `group_id` | body | int | Không | `-1` = nhóm mặc định `info_default_info`; `-2` = `info_default_info_address`; `>= 1` = `friend_information_setting.group_id`; `0` / rỗng = nhóm chưa phân loại |
| `arr_export_friend_info_setting_value` | body | JSON string (mảng id) | Không | Dùng ở màn sửa / nhân bản để dựng lại các mục đã chọn |

Có kiểm tra hợp lệ `group_id` theo `category.kind = information_friend`, `bot_id`, `is_deleted = 0`; nếu không hợp lệ → ép về `0` (`:229-240`).

**Response**

```json
{
  "status": true,
  "groups": [{ "id": 41, "name": "基本情報" }],
  "items": [{ "id": 305, "name": "会員番号", "group_id": 41 }],
  "group_open": 41,
  "count_default": 4,
  "items_default": [],
  "default_friend_info_for_edit_copy": []
}
```

**Lỗi:** 200 + `{"status": false, "msg": "..."}` (`:397-401`)

---

### EP-08 — `POST /ajax/get-list-group-tag-for-csv`

| Param | Vị trí | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|---|
| `group_id` | body | int | Không | `0` / rỗng = tag chưa phân nhóm |
| `arr_export_tags_id` | body | JSON string (mảng id) | Không | Dựng lại tag đã chọn khi sửa / nhân bản |

Kiểm tra `group_id` phải là `category` thuộc `bot_id` hiện tại, `kind = tag`, `is_deleted = 0`; sai → ép `0` (`:153-159`).

**Response**

```json
{
  "status": true,
  "groups": [{ "id": 18, "name": "属性" }],
  "tag_items": [{ "id": 221, "name": "VIP", "category_id": 18, "position": 5 }],
  "group_open": 18,
  "count_default": 12,
  "items_default": [],
  "default_tags_for_edit_copy": []
}
```

**Lỗi:** 200 + `{"status": false, "msg": "..."}` (`:233-235`)

> Endpoint này còn được dùng bởi 「クロス分析」 (`public/js/cross_analysis/create.js:241`) → ứng viên **shared component**.

---

### EP-09 — `POST /ajax/csv-management/save-filter` ⚠ (endpoint quan trọng nhất)

Gửi bằng `FormData` (multipart) từ `public/js/csv_management/create_download_file.js:456-486`.

| Param | Vị trí | Kiểu | Bắt buộc | Validation trong code |
|---|---|---|---|---|
| `save_action` | body | string | Có | `'edit'` → update; giá trị khác → create (`:499`) |
| `csv_id` | body | int | Khi `save_action='edit'` | Không kiểm tra tồn tại / `bot_id` |
| `csv_name` | body | string | **Có** | `empty($csvName)` → lỗi 「書き出し名（管理用）を入力してください。」 (`:445-447`). Giới hạn 50 ký tự **chỉ ở client** (`create_download_file.js:524-532`); server không giới hạn, cột DB `varchar(255)` |
| `type_filter_condition` | body | int | Có | `1` = 「有効友だち」 (lọc), `2` = 「ブロックした友だち」, `3` = 「ブロックされた友だち」 (`:462-497`). Giá trị khác → cả 3 cờ = 0 |
| `filter_data` | body | JSON string | Khi `type_filter_condition=1` | `{item_search, item_search_or, keyword}`; chỉ `item_search` / `item_search_or` được dùng (`:586-590`) |
| `arr_tag_id` | body | JSON string | — | Lưu nguyên chuỗi vào `export_tags` |
| `arr_id_friend_info_setting_value` | body | JSON string | — | Lưu nguyên chuỗi vào `export_friend_info_setting_value` |
| `arr_line_user_id` | body | JSON string | — | Chỉ dùng để `count()` → `total_line_user`; **không** lưu (`line_user_ids` luôn `null`) |
| `show_message_status` | body | 0/1 | — | 「ステータスメッセージ」 |
| `show_note` | body | 0/1 | — | 「個別メモ」 |
| `show_date_of_add_friend` | body | 0/1 | — | 「友だち追加日」 |
| `show_reciprocal_status` | body | 0/1 | — | 「対応マーク」 |
| `show_date_of_last_message_received` | body | 0/1 | — | 「最終メッセージ受信日時」 |
| `show_running_step` | body | 0/1 | — | 「配信中ステップ」 |
| `show_qr_code` | body | 0/1 | — | 「流入経路」 (tên cột lệch nghĩa so với nhãn UI) |

**Quy tắc bắt buộc chọn ít nhất 1 cột** (`:449-461`): nếu `arr_tag_id`, `arr_id_friend_info_setting_value` và **cả 7** cờ `show_*` đều rỗng → lỗi 「選択項目を選択してください」.

**Request mẫu** (multipart, mô tả dạng JSON)

```json
{
  "save_action": "create",
  "csv_id": "",
  "csv_name": "有効友だち_VIP",
  "type_filter_condition": "1",
  "filter_data": "{\"item_search\":[],\"item_search_or\":[],\"keyword\":\"\"}",
  "arr_tag_id": "[\"221\",\"222\"]",
  "arr_id_friend_info_setting_value": "[\"-1\",\"305\"]",
  "arr_line_user_id": "[\"U1a2b\",\"U9z8y\"]",
  "show_message_status": 1,
  "show_note": 0,
  "show_date_of_add_friend": 1,
  "show_reciprocal_status": 0,
  "show_date_of_last_message_received": 1,
  "show_running_step": 0,
  "show_qr_code": 0
}
```

**Response thành công**

```json
{ "success": true, "msg": "" }
```

Client nhận `success = true` → `window.location.href = '/basic/csv-management'`.

**Lỗi** (tất cả đều trả HTTP **200**)

| Body `msg` | Nguyên nhân | Vị trí |
|---|---|---|
| `書き出し名（管理用）を入力してください。` | `csv_name` rỗng | `:446` |
| `選択項目を選択してください` | Không chọn cột nào | `:460` |
| `現在のプランは利用できない機能です。アップグレードが必要になります。` | Gói free / `plan_type=2` và đã có ≥ 1 bản ghi | `:527-530` và `:578-581` (`PlanLimitGuard::PLAN_MESSAGE`) |
| `<exception message>` | Exception bất kỳ | `:600` |

> ⚠ **CẢNH BÁO BẢO MẬT (Nghiêm trọng)** — route khai báo ở `routes/web.php:4015`, chỉ nằm trong group `Route::middleware(['NotifyChatworkRequestTimeSlow'])` (`routes/web.php:81`). **Không có** `check_login` / `basic_access` / `check_remember_token`, và `/ajax/*` đã nằm trong `$except` của `app/Http/Middleware/VerifyCsrfToken.php:16` → **không cả CSRF token**. Kẻ tấn công chưa đăng nhập gọi được trực tiếp; `csv_id` truyền tay đi thẳng vào `CsvManagement::where('id', $csvId)->update([...])` (`:500`) **không lọc `bot_id`** → ghi đè cấu hình export của bot bất kỳ (kể cả set lại `bot_id`). Tin cậy: **Cao** (đọc trực tiếp route + middleware + query).

---

### EP-10 — `GET /ajax/initDataFilterCsvManagement`

| Param | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `csv_management_filter_id` | query | int | Không |

Trả về cấu trúc điều kiện lọc đã lưu trong `filters_v2` (`parent_type = 'csv_create_download_file'`, `parent_id = csv_management_filter_id`, `bot_id`, `operator = and` / `or`) — dùng để dựng lại modal 絞り込み và để màn 「友だちリスト」 hiển thị danh sách 対象人数 khi bấm link 「N人」 (JS ghi id vào `localStorage.csv_management_filter_id` rồi mở `/basic/friendlist` ở tab mới — `csv_management.js:800-806`).

- **Response:** JSON điều kiện lọc (cấu trúc chi tiết thuộc shared component SC-003 「絞り込みフィルター」).
- ⚠ **Cảnh báo bảo mật (Trung bình)**: route `routes/web.php:3980` cũng **không có middleware xác thực**. Query có `where('bot_id', $bot_id)` nên chỉ khai thác được khi session còn bot. Tin cậy: **Cao** cho phần thiếu middleware.

---

### EP-11 — `POST /basic/csv-management/update-latest-information`

Gọi từ **Web Worker** `public/js/csv_management/worker.js:32` (XHR thuần, có gửi header `X-CSRF-TOKEN`) để không chặn UI.

| Param | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `csv_id` | body (`application/x-www-form-urlencoded`) | int | Có | **Không có** |

**Hành vi:** `CsvManagement::where('id', $csvId)->update(['filter_update_status' => 20, 'date_of_last_change_of_condition' => now()])` (`:946-951`).

**Response**

```json
{ "status": true }
```

**Lỗi:** 200 + `{"status": false, "msg": "..."}`

> ⚠ Không lọc `bot_id` → có thể kích hoạt build lại file của bot khác. Tin cậy: **Cao**.

---

### EP-12 — `POST /basic/csv-management/export`

| Param | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `csv_id` | body | int | Có (không validate) |

**Hành vi** (`:386-403`): đọc `CsvManagement` theo `id`; nếu có `file_name_new` → tách path theo `/`, `urlencode` **phần tử index 4** rồi ghép lại; ngược lại dùng `file_name` và `urlencode` phần tử cuối. Nếu không tìm thấy bản ghi → `file_name = ""`.

**Response**

```json
{ "success": true, "msg": "", "file_name": "/media/csv/3421/export_12_20260901.csv", "path_new": 1 }
```

- `path_new = 1` → client mở thẳng `domainMediaCSV + file_name` (media server / CDN).
- `path_new = 0` → client gọi EP-13.

**Lỗi:** không bắt exception; `success` luôn `true`. Bản ghi không tồn tại → `file_name` rỗng (client vẫn mở tab trắng). Tin cậy: **Cao**.

> ⚠ Không lọc `bot_id` → lộ đường dẫn file CSV chứa dữ liệu bạn bè của bot khác.

---

### EP-13 — `GET /basic/csv-management/download-csv`

| Param | Vị trí | Kiểu | Bắt buộc |
|---|---|---|---|
| `fileName` | query | string | Có |
| `path_new` | query | 0/1 | Có |

**Hành vi** (`:405-426`):

- `path_new == 1`: nếu `file_exists(public_path() . $fileCsv)` → `response()->download(...)`; ngược lại `redirect(env('URL_SERVER_MEDIA') . $fileCsv . '?v=' . time())`.
- `path_new != 1`: `response()->download(public_path() . '/storage/' . $fileCsv)`.

**Response:** file binary (`Content-Disposition: attachment`) hoặc HTTP 302 sang media server.

**Lỗi:** file không tồn tại ở nhánh `path_new != 1` → `FileNotFoundException` (HTTP 500).

> ⚠ **CẢNH BÁO BẢO MẬT (Nghiêm trọng) — Path traversal / tải file tuỳ ý**: `fileName` lấy nguyên si từ query rồi nối vào `public_path()` mà **không** sanitize, **không** đối chiếu với `csv_management.file_name`, **không** kiểm tra `bot_id`. Chuỗi kiểu `../../.env` cho phép tải file bất kỳ trên server. Tin cậy: **Cao** (đọc trực tiếp `:407-425`).

---

### EP-14 — `POST /basic/csv-management/read_file_csv`

Upload preview (`csv_management.js:30`), gọi với `async: false`.

| Param | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `csv_file` | body (multipart) | file | Có | `$_FILES['csv_file']['type']` phải nằm trong whitelist 10 MIME (`:621-635`) — **chỉ dựa vào Content-Type do client khai báo**, không kiểm tra đuôi file, không giới hạn kích thước |

Whitelist MIME (`:622-634`): `text/csv`, `text/plain`, `application/csv`, `text/comma-separated-values`, `application/excel`, `application/vnd.ms-excel`, `application/vnd.msexcel`, `text/anytext`, `application/octet-stream`, `application/txt`.

**Xử lý** (`:637-849`):

1. `file_get_contents` → nếu rỗng → lỗi 「エラー」.
2. Nếu `mb_detect_encoding($csv, "sjis-win")` thành công → chuyển Shift-JIS → UTF-8.
3. Đọc từng dòng bằng `fgetcsv` từ `php://temp`:
   - **Dòng 0** = hàng tiêu đề kỹ thuật (`row0`), header khởi tạo `['line_id', 'name']`.
   - **Dòng 1** = hàng tiêu đề hiển thị; map nhãn tiếng Nhật → tên cột (bảng dưới).
   - **Từ dòng 2** = dữ liệu, `array_combine($header, $row2)` rồi `csvValidate()`.
4. Nếu `count($header) > count($row)` → dừng, trả `success = false`, `message = 'エラー'`.

**Bảng ánh xạ nhãn → cột** (config `config/sns-line.php:978-989` + hard-code `:740-778`)

| Nhãn CSV | Cột nội bộ |
|---|---|
| `ステータスメッセージ` | `status_message` |
| `個別メモ` | `memo` |
| `友だち追加日` | `followed_at` |
| `対応マーク` | `id_status` |
| `最終メッセージ受信日時` | `last_time_message` |
| `配信中ステップ` | `is_following` |
| `流入経路` | `landing_name` |
| `システム表示名` | `view_name` (bật `isShowAction`) |
| `携帯電話` | `phone_number` (bật `isShowAction`) |
| `メールアドレス` | `email` (bật `isShowAction`) |
| `生年月日` | `birthday` (bật `isShowAction`) |
| `年齢` | `age` (bật `isShowAction`) |
| `都道府県` | `province` (bật `isShowAction`) |
| `タグ_{id}` (trong dòng 0) | `tag_{id}` (bật `isShowAction`) |
| `友だち情報_{id}` (trong dòng 0) | `friend_info_setting_{id}` (bật `isShowAction`) |

**Validation từng dòng** — `csvValidate()` (`:857-892`): chỉ `line_id => required`; `phone_number` và `status_message` là `nullable`. Thông báo lỗi: `有効な:attributeではありません。`

**Response thành công**

```json
{
  "success": true,
  "data": {
    "csv_file_name": "friends_20260901.csv",
    "tag_ids": ["221", "222"],
    "friend_info_setting_ids": ["305"],
    "items": [
      { "line_id": "U1a2b", "name": "山田太郎", "memo": null, "tag_221": "1" }
    ]
  },
  "message": "",
  "totalUser": 120,
  "isShowAction": 1
}
```

- `isShowAction = 1` → client mở modal `#modalConfirmAction` hỏi có áp dụng tag / 友だち情報 hay không (`csv_management.js:49-52`).

**Lỗi**

| Body | Nguyên nhân |
|---|---|
| `{"success": false, "message": "CSVファイルを選択してください。"}` | Thiếu file hoặc MIME không hợp lệ (`:630`) |
| `{"success": false, "message": "エラー"}` | File rỗng, số cột không khớp, hoặc `success = false` cuối vòng lặp |
| `{"success": false, "message": "<lỗi validate>"}` | `csvValidate()` thất bại |
| `{"success": false, "message": "<exception>"}` | Exception |

---

### EP-15 — `POST /basic/csv-management/save_file_csv`

Nút 「アップロード」 → `csvSave()` (`csv_management.js:64-100`).

| Param | Vị trí | Kiểu | Bắt buộc | Validation |
|---|---|---|---|---|
| `csv_file` | body (multipart) | file | Có | Chỉ kiểm tra `empty($file)`; **không kiểm tra MIME lại** (whitelist chỉ chạy ở bước preview EP-14) |
| `totalUser` | body | int | Không | Ghi thẳng vào `csv_filter_upload_history.number_line_user` — **client tự khai, server không đối chiếu** |
| `actionTag` | body | 0/1 | Không | → `is_action_tag`, mặc định `0` |
| `actionInForFriend` | body | 0/1 | Không | → `is_action_info_friend`, mặc định `0` |

**Hành vi** (`:894-935`):

1. `$path = env('FOLDER_MEDIA') . 'media/csv/' . getCurrentUser() . '/' . getBotId() . '/'`
2. `uploadFile($file, '', $path)` → trả URL
3. `CsvFilterUploadHistory::create([...])` với `upload_status` để mặc định `1` (DEFAULT của cột) → **đưa vào hàng đợi job import**

**Response thành công**

```json
{ "success": true, "message": "インポートされました。" }
```

**Lỗi**

| Body | Nguyên nhân |
|---|---|
| `{"success": false, "message": "インポートされました。"}` | `$file` rỗng — ⚠ **bug**: `success=false` nhưng dùng đúng thông điệp thành công (`:903`) |
| `{"success": false, "message": "<exception>"}` | Exception (`:929-932`) |

---

## 3. Middleware áp dụng & cảnh báo bảo mật

### 3.1 Middleware theo nhóm route

| Nhóm route | Khai báo | Middleware |
|---|---|---|
| `prefix: basic` (EP-01…04, EP-11, EP-12, EP-14, EP-15) | `routes/web.php:882` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` |
| Group `check_login` (EP-13) | `routes/web.php:1877` | `check_login`, `check_remember_token` |
| `prefix: ajax` (EP-05…08) | `routes/web.php:2485` | `check_login`, `check_remember_token` |
| Top-level (EP-09, EP-10) | `routes/web.php:81` | **chỉ** `NotifyChatworkRequestTimeSlow` |

Alias middleware: `app/Http/Kernel.php:70, 75, 76, 77, 83`.

`basic_access` → `app/Http/Middleware/BasicAccess.php:27`: kiểm tra `Auth::check()`, `role` ∈ {−1, 0, 1, 2}, kiểm tra `bot_id` trong session, và với tài khoản Staff (`session('is_bot_invite')` hoặc `bots.admin_id !== Auth::id()`) kiểm tra tên route hiện tại có nằm trong `getRouterBotInvite()` — đây là cơ chế phân quyền Staff duy nhất áp dụng cho tính năng này (`BasicAccess.php:36-51`).

### 3.2 Bảng cảnh báo bảo mật

| # | Mức | Endpoint | Vấn đề | Vị trí |
|---|---|---|---|---|
| S-1 | **Nghiêm trọng** | EP-09 `/ajax/csv-management/save-filter` | Không có middleware xác thực; CSRF cũng bị miễn qua `/ajax/*`; `update()` không lọc `bot_id` | `routes/web.php:4015`, `app/Http/Middleware/VerifyCsrfToken.php:16`, `CsvManagementController.php:500` |
| S-2 | **Nghiêm trọng** | EP-13 `/basic/csv-management/download-csv` | Path traversal: `fileName` từ query nối thẳng vào `public_path()`, không sanitize, không đối chiếu DB, không kiểm `bot_id` | `CsvManagementController.php:405-426` |
| S-3 | **Cao** | EP-03, EP-04, EP-05 (delete/sort), EP-11, EP-12 | IDOR — mọi truy vấn `CsvManagement::where('id', ...)` đều thiếu `bot_id` | `:99, :128, :328, :341, :351, :387, :946` |
| S-4 | **Trung bình** | EP-10 `/ajax/initDataFilterCsvManagement` | Không có middleware xác thực (query vẫn có `bot_id` từ session) | `routes/web.php:3980` |
| S-5 | **Trung bình** | EP-14, EP-15 | Upload chỉ kiểm tra MIME do client khai báo, và chỉ ở bước preview; bước lưu không kiểm tra lại; không giới hạn dung lượng | `:621-635`, `:894-912` |
| S-6 | **Thấp** | Toàn bộ AJAX | Trả `$exception->getMessage()` về client (rò rỉ thông tin nội bộ) | `:373, :600, :930` |
| S-7 | **Thấp** | EP-15 | `totalUser` do client khai, ghi thẳng vào DB không đối chiếu số dòng thực tế | `:896, :917` |

---

## 4. Liên kết endpoint ↔ màn hình UI

| Màn hình | Mã | Endpoint sử dụng |
|---|---|---|
| Danh sách エクスポート | `SCR-CSV-01` | EP-01 (render), EP-05 (`initData` / `deleteItem` / `deleteItems`), EP-11 (「最新情報に更新」), EP-12 + EP-13 (「CSVダウンロード」), EP-10 (link 「N人」 → mở `/basic/friendlist`) |
| Tab インポート | `SCR-CSV-02` | EP-06 (bảng 「インポート履歴」), EP-14 (chọn file → preview), EP-15 (「アップロード」) |
| Form tạo 「エクスポートデータ作成」 | `SCR-CSV-03` | EP-02 (render), EP-08 (cây タグ), EP-07 (cây 友だち情報), EP-09 (「この条件でCSVを作成・更新」) |
| Form sửa | `SCR-CSV-04` | EP-03 (render), EP-08, EP-07, EP-10 (dựng lại điều kiện lọc), EP-09 (`save_action=edit`) |
| Modal 絞り込み (SC-003) | `SCR-CSV-05` | EP-10; các endpoint khác của shared component filter (`/ajax/init-data-filter`, `/ajax/filter/count-all-friend`…) — xem `features/shared/` |
| Modal 並べ替え | `SCR-CSV-06` | EP-05 (`action=sortItem`) |

> Form 「コピー」 (EP-04) dùng lại chính view/màn `SCR-CSV-03` (`csv_management.create_download_file`) với biến `copy_id`.

---

## 5. Chưa xác định

- Không tìm thấy endpoint **huỷ / dừng** một tiến trình export đang chạy (`filter_update_status = 88`). Tính năng 「CSVエクスポート（チャット）」 có (`/ajax/csv-export-chat/cancel` — `routes/web.php:3280`) nhưng thuộc feature khác.
- Không tìm thấy endpoint **xoá** bản ghi trong 「インポート履歴」 (`csv_filter_upload_history`) từ portal Admin.
- Không tìm thấy endpoint tải lại file đã import.
- Cột `csv_management.show_system_name` tồn tại trong DB nhưng mọi tham chiếu trong controller và JS đều **bị comment** (`:511`, `:557`, `create_download_file.js:466`) → cột 「システム表示名」 đã bị vô hiệu hoá phía export. Tin cậy: **Cao**.
