# Logic Spec — FA-014 「CSV管理」 (Quản lý CSV)

> Portal: **Admin (LINE OA)** — feature folder `features/admin/csv-management/`
> Nguồn: `src/web/sns-line` (Laravel 5 + PHP 7.2). Mọi đường dẫn tương đối với thư mục đó.

---

## 1. Tổng quan luồng nghiệp vụ

Tính năng gồm 2 luồng độc lập:

**Luồng EXPORT (エクスポート)** — Laravel **không** trực tiếp sinh file CSV. Laravel chỉ:
1. Lưu **định nghĩa export** (tên, đối tượng, cột cần xuất, điều kiện lọc) vào bảng `csv_management`.
2. Đặt `filter_update_status` về giá trị "cần xử lý" (`1` khi tạo mới, `20` khi cập nhật / bấm 「最新情報に更新」).
3. Background job (Spring Boot `HandleExportCsvManager`, hoặc Laravel command `handle:export_csv` ở môi trường cũ) **poll** bảng, sinh file, ghi lại `file_name_new` + `total_line_user` + `filter_update_status = 30`.
4. Người dùng bấm 「CSVダウンロード」 → Laravel chỉ đọc lại `file_name_new` / `file_name` và trả file.

**Luồng IMPORT (インポート)** — cũng bàn giao cho job:
1. `readFileCsv()` chỉ **parse + validate preview** trong request, không ghi DB.
2. `saveFileCsv()` upload file lên storage rồi tạo bản ghi `csv_filter_upload_history` với `upload_status = 1` (mặc định cột).
3. Job `HandleImportCsv` poll `upload_status = 1`, đọc file, ghi dữ liệu bạn bè / tag / 友だち情報, cập nhật `upload_status`.

---

## 2. Controllers + Actions

**File:** `app/Http/Controllers/CsvManagementController.php` — 960 dòng, namespace `App\Http\Controllers`, kế thừa `Controller`.

**Constructor** (`:51-54`): inject `ScenarioRepositoryInterface` → thuộc tính `$this->scenarioRepository`. Đây là dependency duy nhất được inject qua constructor.

**Imports đáng chú ý** (`:5-42`): `App\CsvManagement`, `App\CsvFilterUploadHistory`, `App\FilterV2`, `App\Bots`, `App\BotContracts`, `App\Category`, `App\Tags`, `App\FriendInformationSetting`, `App\Conversation`, `App\Conversion`, `App\RichMenus`, `App\StatusChat`, `App\Services\PlanLimitGuard`, `App\Exports\CsvManagementExport`, `Maatwebsite\Excel\Facades\Excel`, `Illuminate\Support\Facades\Validator`.

> Ghi chú: `CsvManagementExport`, `Excel`, `UserExport`, `ExportListFriendOfInfo`, `LINEBot`, `Hashids`, `Messages`, `ActionSchedule`, `ScenarioLineuser`… được `use` nhưng **không dùng** trong bất kỳ method nào còn hoạt động → tàn dư của phiên bản export đồng bộ cũ. Tin cậy: **Cao**.

### 2.1 `index(Request $request)` — `:57-65`
- Trả `view('csv_management.csv_management', [])`.
- Không truy vấn DB, không kiểm tra quyền bổ sung.
- Side effect: không.
- Lỗi: `Exception` → `Log::error('messages:' . $e->getMessage())` + `redirect()->route('404')`.

### 2.2 `createDownloadFile(Request $request)` — `:67-87`
- Nạp dữ liệu cho các bộ lọc trong form: `scenario` (repository), `conversion`, `richMenus` (`status_rich = 1`), `statusObject` (`StatusChat`), tất cả đều lọc theo `getBotId()`.
- Trả `view('csv_management.create_download_file', [...])`.
- **Không** kiểm tra hạn mức gói ở đây → nút 「新規作成」 bị chặn ở client bằng cờ `isAdd` (EP-05), server chỉ chặn ở `saveFilter()`.

### 2.3 `editDownloadFile(Request $request)` — `:89-114`
- Giống 2.2 + `$item = CsvManagement::where(['id' => $csvId])->first()` (`:99`).
- Truyền thêm `csv_id`, `item` vào view.
- ⚠ **Thiếu `bot_id` trong truy vấn** → IDOR. Cũng không xử lý trường hợp `$item === null` (view sẽ nhận `null`).

### 2.4 `copyDownloadFile(Request $request)` — `:116-141`
- Giống 2.3, nhưng truyền `copy_id` thay `csv_id` (`:135`) → JS hiểu là "tạo mới với dữ liệu sao chép".
- Cùng vấn đề IDOR (`:128`).

### 2.5 `ajaxGetListCategoryTag(Request $request)` — `:143-236`
Nạp cây tag cho modal chọn cột 「複数選択項目 → タグ」.
- Validate `group_id`: phải là `Category` thuộc `bot_id`, `kind = config('sns-line.category_kind.tag')`, `is_deleted = 0`; sai → ép `0` (`:153-159`).
- `group_id` rỗng/`0` → trả `items_default` = tag chưa phân nhóm; ngược lại → `tag_items` của nhóm đó.
- `count_default = Tags::countTags(['category_id' => 0, 'bot_id' => $bot_id])`.
- Nếu có `arr_export_tags_id` (màn sửa/copy) → dựng `default_tags_for_edit_copy` bằng cách quét **toàn bộ** category rồi merge (`:207-224`) — **N+1 query** theo số nhóm tag. Tin cậy: **Cao**.
- Side effect: không.

### 2.6 `ajaxInitFriendInformationForCsv(Request $request)` — `:216-403`
Nạp cây 「友だち情報」 cho modal chọn cột.
- `group_id = -1` → danh sách cứng `config('sns-line.info_default_info')`; `-2` → `config('sns-line.info_default_info_address')`; `>= 1` → `FriendInformationSetting` theo `group_id` + `bot_id`; còn lại → nhóm `group_id = 0`.
- Validate `group_id` theo `Category.kind = information_friend`; sai và không thuộc {−1, −2} → ép `0` (`:229-240`).
- `arr_export_friend_info_setting_value` → dựng `default_friend_info_for_edit_copy`, cũng **N+1** theo category (`:379-388`).

### 2.7 `ajaxInitCsvManagement(Request $request)` — `:311-378`
Action đa nhiệm cho màn danh sách. **Đây là action duy nhất thực hiện sửa/xoá danh sách.**

| `action` | Logic | Vị trí |
|---|---|---|
| `sortItem` | Tách `sort_ids` và `sort_position` bằng `,`, `array_sort($sort_position)`, rồi lặp `CsvManagement::where('id', $id_sort)->update(['position' => $sort_position[$key]])` | `:319-334` |
| `deleteItem` | `CsvManagement::where(['id' => $csvId])->delete()` + xoá `FilterV2` với `parent_type='csv_create_download_file'`, `parent_id=$csvId`, `bot_id=$bot_id` | `:336-346` |
| `deleteItems` | `CsvManagement::whereIn('id', $csvIds)->delete()` + xoá `FilterV2` tương ứng (`whereIn parent_id`) | `:348-354` |
| (mặc định) | Chỉ nạp danh sách | — |

Sau khi xử lý action, luôn nạp lại:
- `items = CsvManagement::where(['bot_id' => $bot_id])->orderBy('position', 'DESC')->get()` (`:355`)
- `isAdd` — tính hạn mức gói (`:357-365`), xem Business Rule BR-05.

**Side effects:** ghi log `addLogUserAction("ajaxInitCsvManagement")` (`:316`); `Log::info` / `Log::debug` rất nhiều (bao gồm `json_encode($dataCsv)` toàn bộ bản ghi trước khi xoá — ⚠ ghi dữ liệu nghiệp vụ vào log).

**Vấn đề:**
- ⚠ Không lọc `bot_id` khi sort/delete `csv_management`.
- ⚠ Transaction bị comment (`:312`, `:366`, `:374`) → có thể xoá `csv_management` thành công nhưng `filters_v2` còn sót.
- ⚠ File CSV đã sinh trên đĩa **không được xoá** khi xoá bản ghi → rác storage. Tin cậy: **Cao**.

### 2.8 `csvExport(Request $request)` — `:386-403`
Trả về đường dẫn file cho client. Logic `urlencode`:
- Có `file_name_new`: `explode('/')` rồi `urlencode` **phần tử index 4** (giả định cấu trúc path cố định `"" / media / csv / {bot_id} / {file}`). ⚠ Nếu path nông hơn → `Undefined offset` (PHP 7.2 chỉ Notice, giá trị `null`).
- Không có `file_name_new`: `urlencode` phần tử cuối của `file_name`.
- Không bắt exception, luôn trả `success = true`.

### 2.9 `downloadCsv(Request $request)` — `:405-426`
Trả file theo `fileName` + `path_new` từ query. Xem cảnh báo S-2 trong api-spec.
- `path_new == 1` & file tồn tại local → `response()->download(public_path() . $fileCsv)`.
- `path_new == 1` & không tồn tại → `redirect(env('URL_SERVER_MEDIA') . $fileCsv . '?v=' . time())` (fallback sang media server / OVH).
- `path_new != 1` → `response()->download(public_path() . '/storage/' . $fileCsv)` (đường dẫn cũ, trước khi có `file_name_new`).

### 2.10 `saveFilter(Request $request)` — `:428-604` ⭐ (action cốt lõi)

Thứ tự xử lý:

1. `addLogUserAction("saveFilter")` (`:431`).
2. Đọc `csv_name`, `csv_id`, `save_action`, `type_filter_condition`; khởi tạo 3 cờ đối tượng = 0.
3. **Validate thủ công** (không dùng FormRequest):
   - `csv_name` rỗng → trả 「書き出し名（管理用）を入力してください。」 (`:445-447`).
   - Không chọn bất kỳ tag / 友だち情報 / cờ `show_*` nào → 「選択項目を選択してください」 (`:449-461`).
4. **Xác định tập LINE user theo `type_filter_condition`** (`:462-497`):
   - `1` 「有効友だち」: `enable_filter_friend = 1`; `arrLineUserId = json_decode($request->arr_line_user_id)` (danh sách do client gửi lên từ kết quả modal lọc).
   - `2` 「ブロックした友だち」: `enable_bot_block_friend = 1`; server tự truy vấn `Conversation::getConversationBlocked($currentBotId, ['conversation.line_id as id'], 1)`.
   - `3` 「ブロックされた友だち」: `enable_friend_block_bot = 1`; `Conversation::getConversationBlocked($currentBotId, [...], 0)`.
5. **Nhánh EDIT** (`save_action == 'edit'` và `csv_id` không rỗng) — `:499-524`: `CsvManagement::where('id', $csvId)->update([...])` với `filter_update_status = 20`, `date_of_last_change_of_condition = now()`, `line_user_ids = null`, `total_line_user = count($arrLineUserId)`.
6. **Nhánh CREATE** — `:525-583`:
   - Kiểm tra hạn mức gói **trước khi insert** (`:531-539`).
   - `position = (bản ghi có position lớn nhất của bot)->position + 1`, mặc định `1` (`:541-542`).
   - `CsvManagement::create([...])` với `filter_update_status = 1`.
   - Kiểm tra hạn mức **lần hai sau khi insert** bằng `PlanLimitGuard::rollbackIfOverLimit(...)`, callback xoá bản ghi vừa tạo nếu vượt (`:568-582`). Comment trong code ghi rõ đây là fix cho ticket `#39230` (race condition khi mở nhiều tab).
7. **Lưu điều kiện lọc**: chỉ khi `enable_filter_friend == 1` → `FilterV2::saveFilter($filterData['item_search'], $filterData['item_search_or'], 'csv_create_download_file', $csvId)` (`:585-590`).
8. Trả `{success: true, msg: ''}`.

**Side effects:** insert/update `csv_management`; insert/update/delete `filters_v2`; ghi log user action.

**Vấn đề:**
- ⚠ Transaction bị comment (`:434`, `:592`, `:598`) → nếu `FilterV2::saveFilter()` ném exception, bản ghi `csv_management` đã tồn tại nhưng không có điều kiện lọc → job sẽ export sai tập bạn bè.
- ⚠ `update()` nhánh edit không lọc `bot_id` và còn **set lại** `bot_id = $currentBotId` → chiếm quyền bản ghi của bot khác.
- ⚠ `date_of_last_change_of_condition` bị gán **hai lần** trong cùng mảng update (`:509` và `:522`) — vô hại nhưng là code smell.
- ⚠ `total_line_user` với `type_filter_condition = 1` được tính từ mảng do **client** gửi → không đáng tin; job sẽ tính lại và ghi đè (xem mục 8).

### 2.11 `ajaxInitImportCsvManagement(Request $request)` — `:602-616`
Trả toàn bộ `csv_filter_upload_history` của bot, sắp xếp `id desc`. Có lọc `bot_id`. **Không phân trang** → bảng lịch sử lớn dần theo thời gian sẽ nặng. Tin cậy: **Cao**.

### 2.12 `readFileCsv(Request $request)` — `:619-849`
Parse file CSV upload thành mảng `items` để preview, kèm `tag_ids` / `friend_info_setting_ids` phát hiện được từ header. Xem chi tiết ánh xạ header trong api-spec EP-14.
- **Không ghi DB.**
- Đặc thù định dạng: file export của hệ thống có **2 dòng tiêu đề** — dòng 0 chứa mã kỹ thuật (`タグ_{id}`, `友だち情報_{id}`), dòng 1 chứa nhãn hiển thị tiếng Nhật.
- Tự phát hiện encoding Shift-JIS (`sjis-win`) và chuyển sang UTF-8 (`:653-657`).
- Cờ `isShowAction = 1` khi file có cột tag / 友だち情報 / thông tin cá nhân → client hỏi xác nhận có ghi đè các dữ liệu đó không.
- ⚠ Toàn bộ file được nạp vào RAM (`file_get_contents` + `php://temp`) → file lớn có nguy cơ vượt `memory_limit`.

### 2.13 `convertHeaderId($text)` — `:851-854` (private)
`substr($text, strpos($text, "_") + 1)` — tách id từ chuỗi dạng `タグ_221` → `221`.

### 2.14 `csvValidate($data)` — `:857-892` (private)
Validate 1 dòng CSV bằng `Validator::make()`. Xem mục 5.

### 2.15 `saveFileCsv(Request $request)` — `:894-935`
- `addLogUserAction("saveFileCsv CSV management")` (`:898`).
- `$path = env('FOLDER_MEDIA') . 'media/csv/' . getCurrentUser() . '/' . getBotId() . '/'` (`:906`).
- `uploadFile($file, '', $path)` (helper `app/Helpers/functions.php:531`) → trả URL tương đối.
- `CsvFilterUploadHistory::create([bot_id, number_line_user, name, path_file, is_action_tag, is_action_info_friend])` — **không truyền `upload_status`**, cột lấy DEFAULT `1` → **đây chính là hành động enqueue job import**. Tin cậy: **Cao**.
- ⚠ File được lưu **trước** khi validate lại; nội dung đã parse ở EP-14 **không** được gửi kèm (cột `data` để `null`) → job sẽ đọc lại file từ `path_file`.

### 2.16 `updateLatestInformation(Request $request)` — `:941-958`
- `addLogUserAction("updateLatestInformation")`.
- `CsvManagement::where('id', $csvId)->update(['filter_update_status' => 20, 'date_of_last_change_of_condition' => now()])`.
- **Đây là hành động enqueue job export lại** (trạng thái `20` = `STATUS_RELOAD`).
- Được gọi từ **Web Worker** để không chặn UI (`public/js/csv_management/worker.js`).
- ⚠ Không lọc `bot_id`; không kiểm tra bản ghi có đang ở trạng thái `88` (đang chạy) hay không → bấm liên tục có thể reset trạng thái của job đang chạy.

### 2.17 `initDataFilterCsvManagement(Request $request)` — **KHÔNG thuộc `CsvManagementController`**

> ⚠ **Bổ sung (V-11)**: endpoint **EP-10** `GET /ajax/initDataFilterCsvManagement` phục vụ FA-014 nhưng **nằm ngoài** `CsvManagementController`.

- **Controller thực tế**: `App\Http\Controllers\Basic\FriendlistController@initDataFilterCsvManagement` — `app/Http/Controllers/Basic/FriendlistController.php:4536`.
- **Vai trò**: trả về cấu trúc điều kiện lọc đã lưu trong `filters_v2` (`parent_type = 'csv_create_download_file'`, `parent_id = csv_management_filter_id`, `bot_id`, `operator = and`/`or`) — dùng để dựng lại modal 「絞り込み」 và để màn 「友だちリスト」 hiển thị danh sách 対象人数 khi người dùng bấm link 「N人」 ở SCR-CSV-01 (JS ghi id vào `localStorage.csv_management_filter_id` rồi mở `/basic/friendlist` ở tab mới — `public/js/csv_management/csv_management.js:803-811`).
- **Chi tiết logic không thuộc phạm vi FA-014** — đây là phần của **shared component SC-003 「絞り込みフィルター」**; xem `features/shared/friend-filter/shared-spec.md`.
- Tin cậy: **Cao** (đọc trực tiếp source).

---

## 3. Models Eloquent

### 3.1 `App\CsvManagement` — `app/CsvManagement.php`

```
protected $table = 'csv_management';
protected $primaryKey = 'id';
protected $guarded = [];      // KHÔNG có $fillable → mass-assignment mở hoàn toàn
public $timestamps = true;
```

- **Không** có relationship, scope, accessor/mutator, cast nào được khai báo. Model "trống".
- ⚠ `$guarded = []` cho phép gán mọi cột kể cả `id`, `bot_id`, `filter_update_status`, `file_name_new` — kết hợp với việc `saveFilter()` chỉ gán tường minh nên chưa bị khai thác trực tiếp, nhưng là rủi ro. Tin cậy: **Cao**.

**Cột bảng `csv_management`** (`db/schema/tables/csv_management.sql`)

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `id` | int unsigned | PK |
| `bot_id` | int | Bot sở hữu |
| `enable_filter_friend` | int, def 0 | `1` = đối tượng 「有効友だち」 (có điều kiện lọc) |
| `enable_bot_block_friend` | int, def 0 | `1` = 「ブロックした友だち」 |
| `enable_friend_block_bot` | int, def 0 | `1` = 「ブロックされた友だち」 |
| `line_user_ids` | text | **Luôn `null`** ở phiên bản hiện tại (`:507`, `:548`) — tàn dư |
| `total_line_user` | int, def 0 | 「対象人数」 hiển thị trên danh sách |
| `name` | varchar(255) | 「書き出し名（管理用）」 |
| `file_name` | varchar(255) | Đường dẫn file **cũ** (dưới `public/storage/`) |
| `file_name_new` | varchar(255) | Đường dẫn file **mới** (dưới `public` + `FOLDER_MEDIA`), có thể là `.zip` |
| `filter_update_status` | int, def 1 | Trạng thái hàng đợi — xem mục 8 |
| `export_tags` | text | JSON mảng id tag cần xuất |
| `export_friend_info_setting_value` | text | JSON mảng id 友だち情報 cần xuất |
| `show_system_name` | int, def 0 | 「システム表示名」 — **đã vô hiệu hoá** (mọi tham chiếu bị comment) |
| `show_message_status` | int, def 0 | 「ステータスメッセージ」 |
| `show_note` | int, def 0 | 「個別メモ」 |
| `show_date_of_add_friend` | int, def 0 | 「友だち追加日」 |
| `show_reciprocal_status` | int, def 0 | 「対応マーク」 |
| `show_date_of_last_message_received` | int, def 0 | 「最終メッセージ受信日時」 |
| `show_running_step` | int, def 0 | 「配信中ステップ」 |
| `show_qr_code` | int, def 0 | 「流入経路」 (tên cột lệch nghĩa nhãn UI) |
| `position` | int | Thứ tự hiển thị (sort DESC) |
| `date_of_last_change_of_condition` | datetime | 「最終条件設定」 |
| `created_at` / `updated_at` | timestamp | 「作成日」 |

### 3.2 `App\CsvFilterUploadHistory` — `app/CsvFilterUploadHistory.php`

```
protected $table = 'csv_filter_upload_history';
protected $primaryKey = 'id';
protected $guarded = [];
public $timestamps = true;
```
Cũng là model trống, không relationship/scope/cast.

**Cột bảng `csv_filter_upload_history`**

| Cột | Kiểu | Ý nghĩa |
|---|---|---|
| `id` | int unsigned | PK |
| `bot_id` | int | Bot sở hữu |
| `number_line_user` | int | Số dòng do **client** khai (`totalUser`) |
| `name` | varchar(255) | Tên file gốc |
| `upload_status` | int, def 1 | Trạng thái hàng đợi import — xem mục 8 |
| `friend_info_setting_ids` | text | JSON id 友だち情報 (luồng V1, hiện Laravel để `null`) |
| `tag_ids` | text | JSON id tag (luồng V1, hiện `null`) |
| `data` | text | Dữ liệu đã parse (luồng V1, hiện `null`) |
| `path_file` | varchar(255) | Đường dẫn file đã upload (luồng V2 — luồng đang dùng) |
| `message_error` | text | ⚠ **Cột chết — KHÔNG thành phần nào ghi cột này** (đính chính V-02). Grep Laravel (`app/`, `resources/`, `public/`) = **0 writer**; grep Java = **0 writer** (`setMessageError` không được gọi ở đâu — entity chỉ có getter/setter tại `CsvFilterUploadHistory.java:47-48`); **không UI nào đọc**. Dump: **0/302 bản ghi** có giá trị. Cùng nhóm di sản luồng V1 với `data` / `tag_ids` / `friend_info_setting_ids`. Tin cậy: **Cao** |
| `is_action_tag` | tinyint, def 0 | `1` = áp dụng tag từ file |
| `is_action_info_friend` | tinyint, def 0 | `1` = áp dụng 友だち情報 từ file |
| `created_at` / `updated_at` | timestamp | |

### 3.3 Models phụ được đọc (chỉ đọc, không ghi)

| Model | Bảng | Dùng ở đâu |
|---|---|---|
| `App\Bots` | `bots` | `flag_contract_new`, `plan_type` — kiểm tra hạn mức (`:359`, `:533`) |
| `App\BotContracts` | `bot_contracts` (join `bot_slots`) | Lấy `contract_type` (`:361`, `:535`) |
| `App\Category` | `category` | Nhóm tag / nhóm 友だち情報 |
| `App\Tags` | `tags` | Danh sách tag |
| `App\FriendInformationSetting` | `friend_information_setting` | Danh sách trường 友だち情報 |
| `App\Conversation` | `conversation` | `getConversationBlocked()` — lấy line_id bị block |
| `App\Conversion` | `conversion` | Dữ liệu cho modal filter |
| `App\RichMenus` | `rich_menus` | Dữ liệu cho modal filter (`status_rich = 1`) |
| `App\StatusChat` | `status_chat` | 「対応マーク」 cho modal filter |
| `App\FilterV2` | `filters_v2` | Lưu / xoá điều kiện lọc |

---

## 4. Services / Repositories / Helpers

### 4.1 `App\Services\PlanLimitGuard`
- Hằng liên quan: `FEATURE_CSV_EXPORT = 'csv_export'` (`app/Services/PlanLimitGuard.php:71`), `PLAN_MESSAGE` (`:66`).
- `rollbackIfOverLimit($botId, $feature, $query, $newId, $limit, callable $rollback, $idColumn = 'id')` (`:208`): nếu bản ghi `newId` nằm ngoài `limit` bản ghi đầu tiên của `$query` → ghi log `[plan-limit]` và gọi `$rollback()` (xoá bản ghi vừa tạo), trả `true`.
- Trong `saveFilter()`: `$csvLimit = 1` khi gói free / `plan_type = 2`, ngược lại `null` (không giới hạn).

### 4.2 `App\FilterV2` (static helper trên model)
- `FilterV2::saveFilter($filterAnd, $filterOr, $parentType, $parentId, $richMenuRedirectId = null, $richMenuItemId = null)` — `app/FilterV2.php:18`.
- Tự lấy `bot_id = getBotId()` bên trong (`:19`).
- Ghi mỗi điều kiện thành 1 bản ghi `filters_v2` với `parent_type = 'csv_create_download_file'`, `parent_id = csv_management.id`, `operator = 'and' | 'or'`, `type` (vd `tag`), `text_preview` (chuỗi hiển thị), `data` (JSON điều kiện).
- Các bản ghi cũ không còn trong danh sách sẽ bị xoá (cơ chế `$arrIdFilter`).
- Đây là **shared component SC-003 「絞り込みフィルター」** dùng chung với broadcast, step message, action schedule, cross analysis…

### 4.3 `ScenarioRepositoryInterface`
- Inject qua constructor; chỉ dùng `findByBot($bot_id)` để nạp danh sách kịch bản cho modal filter.

### 4.4 Helpers toàn cục (`app/Helpers/functions.php`)

| Helper | Dòng | Vai trò |
|---|---|---|
| `getBotId()` | `:386` | Lấy `bot_id` hiện hành từ session |
| `getCurrentUser()` | `:4906` | Lấy user id hiện hành (dùng làm segment path upload) |
| `uploadFile($file, $fileName, $dir)` | `:531` | Upload file lên storage, trả URL |
| `addLogUserAction($action)` | `:9380` | Ghi log hành động người dùng |
| `getRouterBotInvite()` | `:4696` | Danh sách route name mà Staff được truy cập |

---

## 5. Form Requests / Validation

**Không có FormRequest nào** cho tính năng này (`app/Http/Requests/` không chứa lớp liên quan CSV). Toàn bộ validation là thủ công trong controller.

### 5.1 Validation `saveFilter()` (`:445-461`)

| Rule | Thông báo | Vị trí |
|---|---|---|
| `csv_name` không rỗng | `書き出し名（管理用）を入力してください。` | `:446` |
| Ít nhất 1 trong: `arr_tag_id`, `arr_id_friend_info_setting_value`, 7 cờ `show_*` | `選択項目を選択してください` | `:460` |

Giới hạn 50 ký tự cho `csv_name` **chỉ tồn tại phía client** (`public/js/csv_management/create_download_file.js:524-532`, thông báo `書き出し名を50文字以下で入力してください`). Server không kiểm tra → có thể lưu tới 255 ký tự. Tin cậy: **Cao**.

### 5.2 Validation upload CSV

**Kiểm tra file** (`readFileCsv`, `:621-635`): whitelist 10 MIME dựa trên `$_FILES['csv_file']['type']` — giá trị này do trình duyệt gửi, **không đáng tin**. Không kiểm tra extension, không giới hạn size, không dùng `Validator` của Laravel.

**Kiểm tra từng dòng** — `csvValidate()` (`:857-892`):

```
$rule['line_id']        = 'required';
$rule['phone_number']   = 'nullable';
$rule['status_message'] = 'nullable';
```

Messages: `required` / `regex` / `in` → `有効な:attributeではありません。`; `phone_number.regex` → `有効な電話番号ではありません。`

Attributes (nhãn hiển thị lỗi): `line_id` → `ユーザーID`, `name` → `LINE登録名`, `real_name` → `本名`, `view_name` → `システム表示名`, `status_msg` → `ステータスメッセージ`, `status` → `表示状態`, `phone_number` → `電話番号`, `is_blocked` → `ユーザーブロック`.

> ⚠ Thực chất chỉ có **1 rule hiệu lực** (`line_id` required); `nullable` không kiểm tra gì. Các message `regex`/`in` và attribute khác là tàn dư của bộ rule cũ đã bị gỡ. Không có validate định dạng ngày (`birthday`, `followed_at`), số (`age`), email. Tin cậy: **Cao**.

---

## 6. Events / Listeners / Queued Jobs

- **Không** có Laravel Event / Listener nào được dispatch trong tính năng này.
- **Không** dùng Laravel Queue (`dispatch()`, `ShouldQueue`) — cơ chế hàng đợi là **polling trên cột trạng thái trong DB** (xem mục 8).
- Các Artisan Command liên quan (đăng ký trong `app/Console/Kernel.php:96-98`, **không** có lịch `schedule()` → chạy như daemon vòng lặp `while(true)` qua supervisor, hoặc đã được thay thế bởi Spring Boot):

| Command | Signature | File | Vai trò |
|---|---|---|---|
| `HandleExportCsv` | `handle:export_csv` | `app/Console/Commands/HandleExportCsv.php:36` | Poll `filter_update_status IN (1, 20)` → sinh CSV/ZIP |
| `HandleExportCsv2` | `handle:export_csv2` | `app/Console/Commands/HandleExportCsv2.php:36` | Biến thể v2 |
| `HandleImportCsv` | `handle:import_csv` | `app/Console/Commands/HandleImportCsv.php:41` | Poll `upload_status = 1` → nhập dữ liệu |
| `HandleUpdateLatestInformationCsv` | `handle:update_latest_information_csv` | `app/Console/Commands/HandleUpdateLatestInformationCsv.php:20` | Poll `filter_update_status = 10` → tính lại `total_line_user` rồi đặt về `20` |

Command khác không đăng ký lịch nhưng liên quan: `RecoverCountLineUserCsvManagement`, `recoverLastUpdateCSV`, `HandleUpdateLatestInformationCsv` (khôi phục dữ liệu sự cố).

---

## 7. Authorization

- **Không có Policy, không có Gate** nào cho `CsvManagement`. Tin cậy: **Cao** (không tìm thấy tham chiếu trong `app/Providers/AuthServiceProvider.php` hay controller).
- Phân quyền dựa hoàn toàn vào **middleware `basic_access`** (`app/Http/Middleware/BasicAccess.php:27`):
  - Yêu cầu `Auth::check()` và `Auth::user()->role` ∈ {−1, 0, 1, 2}.
  - Yêu cầu có `bot_id` trong session.
  - **Với Staff**: khi `session('is_bot_invite')` là true, hoặc khi `Bots::find($current_bot_id)->admin_id !== Auth::id()` → lấy `getRouterBotInvite()` (danh sách route name được phép của custom role) và kiểm tra `in_array(Route::currentRouteName(), $routeList)`; không có quyền → redirect về `adminIndex` với lỗi 「この権限は許可されていません。」 (`BasicAccess.php:36-51`).
  - Ghi nhận truy cập Staff vào `user_access_bot` mỗi ngày một lần (`BasicAccess.php:53-74`).
- **Route name cần cấp quyền cho Staff**: `csvManagement`, `createDownloadFile`, `editDownloadFile`, `copyDownloadFile` — được liệt kê trong `$arraySidebar3` của sidebar (`resources/views/layout/basic/sidebar.blade.php:43`, `layout/admin/sidebar.blade.php:55`, `layout/admin_v2/sidebar.blade.php:55`) và menu 「CSV管理」 hiển thị/ẩn theo `in_array('csvManagement', $routeListAccess)` (`layout/basic/sidebar.blade.php:400-401`).
- ⚠ **Lỗ hổng phân quyền Staff**: các route AJAX (`ajaxInitCsvManagement`, `cMExportCSV`, `basic.csv_management.download_csv`, `ajax.cMSaveFilter`…) **không nằm** trong `$arraySidebar3` và không đi qua `basic_access` với cùng cơ chế kiểm tra route-name (`/ajax/*` chỉ có `check_login`). Staff bị ẩn menu 「CSV管理」 vẫn có thể gọi thẳng API để đọc, sửa, xoá và tải file CSV. Tin cậy: **Cao**.

---

## 8. Bàn giao cho background job ⭐

> Đây là input then chốt cho bước `job-analyzer`.

### 8.1 EXPORT — bảng hàng đợi `csv_management`

**Laravel ghi vào bảng:** `csv_management` (model `App\CsvManagement`).

| Thời điểm | Thao tác | Cột trạng thái | Giá trị | Cột thời gian | Vị trí |
|---|---|---|---|---|---|
| Tạo mới (「この条件でCSVを作成・更新」) | `CsvManagement::create()` | `filter_update_status` | **`1`** | `date_of_last_change_of_condition = now()`, `created_at`/`updated_at` tự động | `CsvManagementController.php:565` |
| Cập nhật (sửa định nghĩa) | `update()` | `filter_update_status` | **`20`** | `date_of_last_change_of_condition = now()` | `:522` (và `:509`) |
| Bấm 「最新情報に更新」 | `update()` | `filter_update_status` | **`20`** | `date_of_last_change_of_condition = now()` | `:949` |

Ngoài `filter_update_status`, Laravel còn đặt `total_line_user = count($arrLineUserId)` và `line_user_ids = null` — job sẽ **tính lại và ghi đè** `total_line_user`.

**Bảng giá trị `filter_update_status`** (thống nhất giữa PHP và Java)

| Giá trị | Hằng Java | Ý nghĩa | Ai ghi |
|---|---|---|---|
| `1` | `CsvManagement.STATUS_NEW` | Mới tạo — chờ job | Laravel `saveFilter()` (create) |
| `2` | `CsvManagement.STATUS_IN_QUEUE` | Đã nạp vào queue trong bộ nhớ job | Job (Spring Boot) |
| `10` | — | Chờ tính lại `total_line_user` (nhánh cũ). ⚠ **4/208 bản ghi thật đang kẹt vĩnh viễn** | **KHÔNG thành phần nào ghi** — writer đã bị gỡ khỏi codebase hiện hành; chỉ còn **reader** `HandleUpdateLatestInformationCsv.php:48`, mà command này **không được `schedule()`** (`app/Console/Kernel.php:98` chỉ đăng ký) |
| `20` | `CsvManagement.STATUS_RELOAD` | Cần build lại — chờ job | Laravel `saveFilter()` (edit) + `updateLatestInformation()` |
| `30` | `CsvManagement.STATUS_DONE` | Hoàn tất — UI mới bật nút 「最新情報に更新」/「CSVダウンロード」 | Job |
| `40` | `CsvManagement.STATUS_FAILURE` | Thất bại | Job (Spring Boot) |
| `88` | `CsvManagement.STATUS_RUNNING` | Đang xử lý — UI hiển thị 「作成中」 | Job |
| `99` | — | **Marker khoá “đã nhận / đang xử lý” — KHÔNG phải trạng thái lỗi**: đặt **TRƯỚC** khối `try` (`HandleUpdateLatestInformationCsv.php:56-59`); xong việc → về `20` (`:130, :146, :162`); chỉ kẹt lại nếu command ném exception (`:157` dùng `continue`, không reset). Dump: **0 bản ghi** | Command Laravel `handle:update_latest_information_csv` |

Nguồn hằng số: `src/job/linect-service/src/main/java/sns/line/models/linedb/entities/CsvManagement.java:13-18`; đối chiếu PHP: `app/Console/Commands/HandleExportCsv.php:65-77, 375, 383`, `HandleUpdateLatestInformationCsv.php:48, 58, 130`.

**Cơ chế poll của Spring Boot** (`src/job/linect-service/.../threads/csv/HandleExportCsvManager.java:31-46`):
- Khi khởi động: nạp lại các bản ghi `status IN (2, 88)` (khôi phục sau restart).
- Vòng lặp: `findAllByFilterUpdateStatusIn([1, 20])` → đẩy vào queue; queue rỗng → `sleep(2000ms)`.
- Bật/tắt bằng feature flag `ENABLE_HANDLE_EXPORT_CSV` (`ConfigFile.java:109, 269`; kích hoạt tại `AppMain.java:237`).
- `HandleExportCsvTask` đặt `STATUS_RUNNING (88)` khi bắt đầu (`:70`), `STATUS_DONE (30)` khi xong (`:270`), `STATUS_FAILURE (40)` khi lỗi (`:56`).
- Repository ghi kết quả: `UPDATE csv_management SET file_name_new = ?, filter_update_status = ?, total_line_user = ? WHERE id = ?` (`CsvManagementRepository.java:26`).

**Nơi ghi file CSV**

> ⚠ **ĐÍNH CHÍNH phạm vi (V-08 + V-09)**: trước đây mục này mô tả triển khai Laravel command *"dùng làm mốc cho job Java"* — **sai**. Job Java **không** theo mốc đó: không nén ZIP và dùng quy ước tên file khác. Phải tách bạch **2 tác nhân sinh file**.

**(a) Luồng HIỆN HÀNH — job Spring Boot `HandleExportCsvTask`** (tin cậy: **Cao**)
- Tên file: `cleanString({tên}) + "_" + {csv_management.id} + "_" + yyyyMMddHHmmss + ".csv"` — **14 chữ số** (`threads/csv/HandleExportCsvTask.java:74`).
- Encoding: **SHIFT-JIS** (`openWrite(path, "SHIFT-JIS")` — `HandleExportCsvTask.java:165`).
- **Luôn đúng 1 file `.csv`, KHÔNG nén ZIP** — grep `zip` trong `HandleExportCsvTask.java` = **0 kết quả**.
- Đường dẫn ghi vào DB: cột `file_name_new`, qua `CsvManagementRepository.java:26`.
- **Bằng chứng dữ liệu thật**: **94/208 bản ghi** có `file_name_new` dạng `_{14 số}.csv`, mới nhất **2026-04-15**. Củng cố thêm: `filter_update_status = 40` (chỉ Java mới ghi — `HandleExportCsvTask.java:56`) có **18 bản ghi thật** → Java đang là tác nhân chạy trên production.

**(b) Luồng CŨ — Laravel command `handle:export_csv` / `handle:export_csv_2`** (tin cậy: **Cao**; **đã ngừng sinh file mới**)
- Tên file: `{tên đã làm sạch}_{csv_management.id}_{Ymd}.csv` — **8 chữ số** (`HandleExportCsv.php:89`, `HandleExportCsv2.php:89`).
- Thư mục vật lý: `public_path() . env('FOLDER_MEDIA') . 'csv/' . {bot_id}` (tạo bằng `mkdir(..., 0777, true)` nếu chưa có).
- Đường dẫn ghi vào DB (`file_name_new`): `env('FOLDER_MEDIA') . 'csv/' . {bot_id} . '/' . {fileName}`.
- **Nén ZIP — CHỈ ở đây, chỉ lúc SINH file, KHÔNG phải lúc download**: khi `count($files) > 1` → `new \ZipArchive()`, `file_name_new = {zipNameDb}{csvName}.zip`, các file `.csv` thành phần bị `unlink` (`HandleExportCsv.php:352-380`). `HandleExportCsv2.php:314, 338` **không** có nhánh ZIP.
- **Bằng chứng dữ liệu thật**: **65/208 bản ghi** dạng `_{8 số}.csv`, dừng ở **2024-07-29**; **2/208 bản ghi** đuôi `.zip`, cả hai `created_at = 2023-04-28`.

**(c) Hai quy ước cổ ở cột `file_name`** (thế hệ cũ nhất, **không tác nhân nào hiện sinh ra**): `{tên}_{unix_ts}.csv` — **6 bản ghi**, 13/07/2022; `{tên}_{id}_{YmdH}.csv` — **3 bản ghi**, 14/07/2022. Tổng cộng **4 thế hệ đặt tên file**.

**(d) Lúc DOWNLOAD — không nén, không sinh file**: `downloadCsv()` (`CsvManagementController.php:405-426`) chỉ `response()->download()` nguyên file có sẵn; grep `zip` trong controller / `public/js/csv_management/` / `resources/views/csv_management/` = **0 kết quả**. Endpoint vẫn phải phục vụ 2 file `.zip` di sản.
- **Không dùng S3**. Khi file không tồn tại trên node hiện tại, `downloadCsv()` fallback sang media server qua `env('URL_SERVER_MEDIA')` (`:421`) → hạ tầng có nhiều node chia sẻ thư mục media. Tin cậy: **Trung bình** (suy từ code fallback, chưa xác nhận cấu hình hạ tầng).

**Job đọc gì để build file:** `csv_management.{enable_filter_friend, enable_bot_block_friend, enable_friend_block_bot, export_tags, export_friend_info_setting_value, show_*}` + các bản ghi `filters_v2` với `parent_type = 'csv_create_download_file'` và `parent_id = csv_management.id`.

### 8.2 IMPORT — bảng hàng đợi `csv_filter_upload_history`

**Laravel ghi vào bảng:** `csv_filter_upload_history` (model `App\CsvFilterUploadHistory`).

| Thời điểm | Thao tác | `upload_status` | Vị trí |
|---|---|---|---|
| Bấm 「アップロード」 | `CsvFilterUploadHistory::create([...])` — **không truyền** `upload_status` → lấy DEFAULT | **`1`** | `CsvManagementController.php:911-918` |

Cột Laravel ghi: `bot_id`, `number_line_user` (từ client), `name` (tên file gốc), `path_file` (URL từ `uploadFile()`), `is_action_tag`, `is_action_info_friend`. Các cột `data`, `tag_ids`, `friend_info_setting_ids` để `null` → job đi theo **nhánh V2** (đọc lại file từ `path_file`).

**Đường dẫn file import:** `env('FOLDER_MEDIA') . 'media/csv/' . {user_id} . '/' . {bot_id} . '/'` + tên file do `uploadFile()` sinh (`:906-907`). Job đọc bằng `public_path($csv->path_file)`.

**Bảng giá trị `upload_status`** (`app/Console/Commands/HandleImportCsv.php`)

| Giá trị | Ý nghĩa | Ai ghi | Vị trí |
|---|---|---|---|
| `1` | `STATUS_WAIT` — mới upload, chờ job | Laravel (DEFAULT cột) | `:69` (điều kiện poll) |
| `100` | `STATUS_IN_QUEUE` — đã nạp vào queue trong bộ nhớ job | **CHỈ Spring Boot** — `HandleImportCsvManager.java:63` (ghi cho cả lô rồi `saveAll()`), hằng số `CsvFilterUploadHistory.java:13`. Laravel **không ghi, không poll** | — (không tồn tại ở PHP) |
| `77` | `STATUS_RUNNING` — đang xử lý | Laravel command (`:79`) và Spring Boot (`HandleImportCsvTask.java`) | `:79` |
| `2` | `STATUS_DONE` — hoàn tất | Laravel command (`:101, 108, 118`); ⚠ **Spring Boot đặt `2` ở MỌI nhánh kết thúc, kể cả khi `readFileCSVV2()` ném exception** (`HandleImportCsvTask.java:79-80, :99-100`) | `:101, 108, 118` |
| `103` | Lỗi | ⚠ **CHỈ Laravel command `handle:import_csv` (luồng cũ, khối `catch`)** — Java **không bao giờ** ghi giá trị này (grep `103` trong `src/job` = 0 kết quả). Dump: **2/302 bản ghi**, cả hai `created_at = 2023-02-01`; **không có bản ghi mới nào** từ đó đến bản ghi mới nhất 2026-04-18 | `:130` |

> ⚠ **Cách blade render** (`resources/views/csv_management/csv_management.blade.php:383-384`) chỉ có **2 nhánh**: `upload_status == 2` → 「完了済」; `v-else` → 「作業中」.
> → `1`, `100`, `77`, `103` đều hiển thị 「作業中」; riêng `103` hiển thị 「作業中」 **vĩnh viễn** (2 bản ghi thật).
> → Ở **luồng Java hiện hành** còn tệ hơn: import **thất bại** vẫn về `2` → UI hiển thị 「**完了済**」, tức **báo sai thành công** (V-03).
> → Nguy cơ kẹt ở `100`: nếu tắt flag `ENABLE_HANDLE_IMPORT_CSV` khi còn bản ghi ở `100` thì Java không nhặt lại, Laravel command chỉ poll `1` nên bỏ qua, UI 「作業中」 vĩnh viễn và **không có UI retry**. Dump `100` = **0 bản ghi** → chưa xảy ra. Tin cậy: **Cao**.

**Cơ chế poll:** `CsvFilterUploadHistory::query()->where('upload_status', 1)->first()`; rỗng → `sleep(10)` (`HandleImportCsv.php:69-74`). Spring Boot có bản tương ứng bật bằng flag `ENABLE_HANDLE_IMPORT_CSV` (`ConfigFile.java:110, 270`; `AppMain.java:240`).

**Side effect của job import:** ghi `line_user` / `bot_line_user` / `tag_line_user` / `friend_information_value`, cập nhật `bots.count_user_unconfirm` và `bots.last_time_count_user_confirm` (`HandleImportCsv.php:95-99`).

> ⚠ **ĐÍNH CHÍNH (V-02)** — trước đây mục này khẳng định *"ghi lỗi từng dòng vào `csv_filter_upload_history.message_error`"*: **SAI**. **Không thành phần nào ghi cột này** — grep Laravel = **0 writer** (khối `catch` tại `HandleImportCsv.php:126-133` chỉ ghi `['upload_status' => 103]`), grep Java = **0 writer** (`setMessageError` không tồn tại), **không UI nào đọc**; dump **0/302 bản ghi** có giá trị. Cột chết, cùng nhóm di sản V1 với `data` / `tag_ids` / `friend_info_setting_ids`. Hệ quả: **không có thông điệp lỗi nào đến được người dùng** — lỗi chỉ tồn tại trong log4j / Chatwork room. Tin cậy: **Cao**.

### 8.3 Ánh xạ trạng thái → UI

| `filter_update_status` | Hiển thị trên `SCR-CSV-01` | Nguồn |
|---|---|---|
| `30` và `total_line_user > 0` | Nút 「最新情報に更新」 + 「CSVダウンロード」 | `resources/views/csv_management/csv_management.blade.php:309-311` |
| `30` và `total_line_user == 0` | Nút 「最新情報に更新」 + badge 「作成中」 (disabled) | `:312` |
| Khác `30` (1, 2, 20, 40, 88) | Cả hai nút disabled, badge 「作成中」 | `:314-317` |

> ⚠ Trạng thái `40` (FAILURE) **không được phân biệt** trên UI — người dùng thấy mãi 「作成中」 khi job lỗi. Tin cậy: **Cao**.
>
> ⚠ **Định lượng + tình tiết tăng nặng (V-04)**: dump có **18/208 bản ghi ở `40`** cộng **4 bản ghi ở `10`** → **22/208 (10,6%) đang hiển thị 「作成中」 sai sự thật**. Ở nhánh `v-else` (`:314-317`), nút 「最新情報に更新」 **CŨNG bị disabled** → người dùng **không có bất kỳ cách nào từ UI** để kích hoạt build lại. Đây là **bế tắc chức năng**, không chỉ là hiển thị gây nhầm lẫn. Tin cậy: **Cao**.

---

## 9. Business Rules tổng hợp

| ID | Quy tắc | Nguồn |
|---|---|---|
| BR-01 | 「書き出し名（管理用）」 bắt buộc nhập; rỗng → chặn lưu | `app/Http/Controllers/CsvManagementController.php:445-447` |
| BR-02 | Giới hạn 50 ký tự cho 「書き出し名」 **chỉ áp dụng phía client**; server chấp nhận tới 255 ký tự | `public/js/csv_management/create_download_file.js:524-532`; `db/schema/tables/csv_management.sql` (`name varchar(255)`) |
| BR-03 | Phải chọn ít nhất một cột xuất (tag, 友だち情報, hoặc 1 trong 7 cờ `show_*`) | `CsvManagementController.php:449-461` |
| BR-04 | Ba đối tượng loại trừ nhau: `type_filter_condition` 1/2/3 → đúng một trong `enable_filter_friend` / `enable_bot_block_friend` / `enable_friend_block_bot` bằng 1 | `CsvManagementController.php:462-497` |
| BR-05 | Gói **free** (`bots.flag_contract_new = 1` và (`bot_contracts.contract_type = 'free'` hoặc `bots.plan_type = 2`)) chỉ được tạo **1** định nghĩa export; vượt → 「現在のプランは利用できない機能です。アップグレードが必要になります。」 | `CsvManagementController.php:357-365` (cờ `isAdd`), `:531-539` (chặn trước insert), `:568-582` (rollback sau insert — ticket #39230) |
| BR-06 | Danh sách export sắp xếp theo `position DESC`; bản ghi mới nhận `position = max(position của bot) + 1`, mặc định 1 | `CsvManagementController.php:355`, `:541-542` |
| BR-07 | Xoá định nghĩa export → xoá kèm mọi bản ghi `filters_v2` có `parent_type='csv_create_download_file'` và `parent_id` tương ứng (nhưng **không** xoá file CSV trên đĩa, và **không** trong transaction) | `CsvManagementController.php:336-354` |
| BR-08 | Điều kiện lọc chỉ được lưu khi `enable_filter_friend = 1`; hai đối tượng block khác tự truy vấn từ `conversation` tại thời điểm lưu | `CsvManagementController.php:585-590`, `:471-497` |
| BR-09 | Nút 「CSVダウンロード」 chỉ bật khi `filter_update_status = 30` **và** `total_line_user > 0`; mọi trạng thái khác hiển thị 「作成中」 | `resources/views/csv_management/csv_management.blade.php:309-317` |
| BR-10 | Bấm 「最新情報に更新」 chỉ đặt `filter_update_status = 20` + cập nhật `date_of_last_change_of_condition`; việc build file do job đảm nhiệm | `CsvManagementController.php:946-951` |
| BR-11 | Upload CSV gồm 2 bước tách rời: preview (`read_file_csv`, không ghi DB) → lưu (`save_file_csv`, ghi file + enqueue). Người dùng có thể đổi file giữa 2 bước mà server không phát hiện | `CsvManagementController.php:619` và `:894` |
| BR-12 | File CSV import phải có **2 dòng tiêu đề**: dòng 0 chứa mã kỹ thuật (`タグ_{id}`, `友だち情報_{id}`), dòng 1 chứa nhãn tiếng Nhật | `CsvManagementController.php:668-790` |
| BR-13 | Mỗi dòng dữ liệu bắt buộc có `line_id` (cột 「ユーザーID」); thiếu → dừng toàn bộ file, trả lỗi 「有効なユーザーIDではありません。」 | `CsvManagementController.php:864, 887` |
| BR-14 | Nếu số cột của một dòng ít hơn header → dừng parse, trả 「エラー」 (không import từng phần) | `CsvManagementController.php:794-800` |
| BR-15 | File Shift-JIS (`sjis-win`) được tự động chuyển sang UTF-8 khi đọc | `CsvManagementController.php:653-657` |
| BR-16 | Khi file có cột tag / 友だち情報 / thông tin cá nhân (`isShowAction = 1`), client hiển thị modal xác nhận; kết quả gửi lên thành `is_action_tag` / `is_action_info_friend` để job quyết định có ghi đè hay không | `CsvManagementController.php:732, 744-777`, `public/js/csv_management/csv_management.js:49-52`, `:70-71` |
| BR-17 | 「インポート履歴」 hiển thị **toàn bộ** lịch sử của bot, không phân trang, sắp theo `id DESC` | `CsvManagementController.php:606` |
| BR-18 | Định nghĩa export cũ dùng `file_name` (dưới `public/storage/`), định nghĩa mới dùng `file_name_new` (dưới `public` + `FOLDER_MEDIA`); cờ `path_new` phân biệt hai đường dẫn tải | `CsvManagementController.php:388-399`, `:407-425` |
| BR-19 | Nếu file không tồn tại trên node hiện tại, hệ thống redirect sang media server `env('URL_SERVER_MEDIA')` | `CsvManagementController.php:419-422` |
| BR-20 | Cột 「システム表示名」 (`show_system_name`) đã bị vô hiệu hoá — mọi tham chiếu trong controller và JS đều bị comment, nhưng cột vẫn tồn tại trong DB | `CsvManagementController.php:511, 557`; `public/js/csv_management/create_download_file.js:466` |
| BR-21 | Menu 「CSV管理」 chỉ hiện với Staff có route name `csvManagement` trong danh sách quyền; các route AJAX **không** được bảo vệ bởi cơ chế này | `resources/views/layout/basic/sidebar.blade.php:400-401`, `app/Http/Middleware/BasicAccess.php:36-51` |

---

## 10. Vấn đề kỹ thuật & nợ kỹ thuật (tổng hợp)

| # | Mức | Vấn đề | Vị trí |
|---|---|---|---|
| T-1 | Nghiêm trọng | `saveFilter()` không có middleware xác thực + CSRF miễn + update không lọc `bot_id` | `routes/web.php:4015`, `CsvManagementController.php:500` |
| T-2 | Nghiêm trọng | `downloadCsv()` path traversal — `fileName` từ query nối thẳng vào `public_path()` | `CsvManagementController.php:405-426` |
| T-3 | Cao | IDOR ở `editDownloadFile`, `copyDownloadFile`, `deleteItem(s)`, `sortItem`, `csvExport`, `updateLatestInformation` | `:99, :128, :328, :341, :351, :387, :946` |
| T-4 | Cao | Toàn bộ `DB::beginTransaction()/commit()/rollback()` bị comment ở cả `ajaxInitCsvManagement` và `saveFilter` | `:312, :366, :374, :434, :592, :598` |
| T-5 | Cao | `$guarded = []` trên cả hai model, không có `$fillable` | `app/CsvManagement.php:10`, `app/CsvFilterUploadHistory.php:10` |
| T-6 | Trung bình | Xoá định nghĩa export không xoá file CSV trên đĩa → rác storage tăng dần | `:336-354` |
| T-7 | Trung bình | Validate upload chỉ dựa trên MIME client khai; bước lưu không kiểm tra lại; không giới hạn dung lượng | `:621-635`, `:894-912` |
| T-8 | Trung bình | Toàn bộ file CSV nạp vào RAM khi parse (`file_get_contents` + `php://temp`) | `:646-651` |
| T-9 | **Nghiêm trọng** (nâng từ Trung bình — V-04) | Trạng thái `40` (FAILURE) không được phản ánh trên UI — **18/208 bản ghi ở `40`** + **4 bản ghi ở `10`** = **22/208 (10,6%) hiển thị 「作成中」 sai sự thật**. Ở nhánh `v-else`, nút 「最新情報に更新」 **cũng bị disabled** → **không có đường retry từ UI** (bế tắc chức năng). Tin cậy: **Cao** | `csv_management.blade.php:314-317` |
| T-10 | Trung bình | N+1 query khi dựng `default_tags_for_edit_copy` và `default_friend_info_for_edit_copy` (lặp theo số category) | `:207-224`, `:379-388` |
| T-11 | Thấp | Trả `$exception->getMessage()` ra client ở mọi AJAX | `:233, :373, :400, :600, :930` |
| T-12 | Thấp | `saveFileCsv()` trả `success=false` kèm thông điệp thành công 「インポートされました。」 khi thiếu file | `:903` |
| T-13 | Thấp | `date_of_last_change_of_condition` bị gán trùng trong cùng mảng `update()` | `:509` và `:522` |
| T-14 | Thấp | `csvExport()` giả định cứng path có ≥ 5 phần tử khi `urlencode($pathArray[4])` | `:390-392` |
| T-15 | Thấp | Nhiều `use` không dùng (`Excel`, `CsvManagementExport`, `UserExport`, `LINEBot`, `Hashids`…) — tàn dư export đồng bộ | `:5-42` |
| T-16 | Thấp | `Log::debug(json_encode($dataCsv))` ghi toàn bộ bản ghi nghiệp vụ vào log trước khi xoá | `:340, :351` |
| T-17 | Thấp | `csvValidate()` chỉ còn 1 rule hiệu lực; các message/attribute khác là tàn dư | `:857-892` |

---

## 11. Chưa xác định

- Cột `csv_management.line_user_ids` luôn được set `null` ở phiên bản hiện tại — chưa rõ job Spring Boot có ghi lại hay không (cần `job-analyzer` xác nhận).
- ~~Ý nghĩa chính xác của `filter_update_status = 10`~~ → **ĐÃ XÁC ĐỊNH — Tin cậy: Cao** (nâng từ Thấp, theo V-01). `10` là **trạng thái mồ côi có thật**: **không thành phần nào trong codebase hiện hành GHI** giá trị này (writer đã bị gỡ — grep toàn Laravel chỉ thấy các nơi ghi `1`/`20`/`30`/`88`/`99`; Java `CsvManagement.java:13-18` không có `10`); chỉ còn **reader duy nhất** `HandleUpdateLatestInformationCsv.php:48`, mà command `handle:update_latest_information_csv` **không được `schedule()`** (`app/Console/Kernel.php:98` chỉ đăng ký). Spring Boot poll `IN (1,20)` / `IN (2,88)` nên không nhặt. **Dump: 4/208 bản ghi thật đang kẹt** → blade render `v-else` → 「作成中」 vĩnh viễn, cả 2 nút disabled → **không có đường thoát từ UI**. Đây là **bug sản phẩm**, không phải thiếu sót của spec.
- Không xác định được các Laravel command `handle:export_csv` / `handle:import_csv` còn chạy song song với Spring Boot hay đã ngừng hẳn — `app/Console/Kernel.php` chỉ đăng ký (`:96-98`) mà không có `schedule()`, nên chúng chỉ chạy nếu được supervisor gọi trực tiếp. Cần đối chiếu cấu hình triển khai. Tin cậy: **Trung bình**.
- Giá trị thực tế của `env('FOLDER_MEDIA')` và `env('URL_SERVER_MEDIA')` (không có trong repo) — ảnh hưởng đường dẫn tuyệt đối của file CSV.
