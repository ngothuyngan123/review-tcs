# [FA-015] Quản lý thông tin bạn bè — Logic Spec

## Tổng quan
- **Tính năng**: FA-015 — Quản lý thông tin bạn bè (「友だち情報管理」)
- **Controller chính**: `Basic\FriendInformationController`
- **File**: `app/Http/Controllers/Basic/FriendInformationController.php` (1485 dòng)
- **Không có Service layer riêng** — toàn bộ business logic nằm trong Controller + helper functions
- **Mức độ tin cậy tổng thể**: **Cao** (đọc trực tiếp từ source code)

---

## 1. Controllers + Actions

### Basic\FriendInformationController
**File**: `app/Http/Controllers/Basic/FriendInformationController.php`

| Method | Dòng | Route | Mô tả logic |
|--------|------|-------|-------------|
| `index()` | 37 | GET `/basic/friend-information` | Đọc cookie folder → validate → render view |
| `addInfo()` | 57 | GET `/basic/friend-information/add` | Validate folderId → render form tạo mới |
| `editInfo()` | 77 | GET `/basic/friend-information/{id}` | Tìm setting by id + bot_id → fallback `ActionInfoFriendDefault` → render form edit |
| `copyInfo()` | 105 | GET `/basic/friend-information/copy/{id}` | Load info → render form copy |
| `initDataInfo()` | 118 | POST `/basic/initDataInfo` | Load chi tiết setting + resolve action details (tag lists, scenario, richmenu) |
| `listFriendByInfo()` | 187 | GET `/basic/friend-information/item/{id}` | Render view danh sách câu trả lời |
| `exportCsv()` | 191 | POST `/basic/friend-info-export-csv` | Query data theo id type → export via Maatwebsite Excel |
| `downloadCsv()` | 282 | GET `/basic/friend-info/download-csv` | Download file CSV từ storage |
| `initDataItemInfo()` | 288 | POST `/basic/initDataItemInfo` | Load danh sách bạn bè + giá trị theo info setting |
| `deleteFriendInfo()` | 367 | POST `/basic/deleteFriendInfo` | Xoá giá trị info của bạn bè (default fields → null, custom → delete records) |
| `getFolder()` | 473 | POST `/basic/getFolder` | Query `category` where kind = 12 |
| `ajaxInitInformation()` | 484 | POST `/ajax/init-information` | Dispatcher: CRUD folder, CRUD items, sort, load data by group |
| `deleteDataFriendInfo()` | 820 | private | Xoá action_detail type 'friend_info' tham chiếu đến info bị xoá |
| `copySettingInfoFriend()` | 830 | POST `/basic/copy-setting-info-friend` | Deep clone: setting + actions + action_details + filters + option_selects |
| `saveSettingInfoFriend()` | 930 | POST `/basic/save-setting-info-friend` | Tạo/cập nhật setting + quản lý options, actions, event scheduling |
| `getFriendInfo()` | 1447 | GET `/basic/get-friend-info` | Lấy tất cả info settings theo bot, nhóm theo type (text, select, datetime) |

---

## 2. Models Eloquent

### FriendInformationSetting
- **File**: `app/FriendInformationSetting.php`
- **Table**: `friend_information_setting`
- **Guarded**: `[]` (mass assignment cho tất cả)
- **Timestamps**: Có

**Constants (type_data):**
| Constant | Giá trị | Ý nghĩa |
|----------|---------|---------|
| `TYPE_DATA_SELECT` | 1 | Kiểu lựa chọn (選択肢) |
| `TYPE_DATA_INPUT` | 2 | Kiểu mô tả văn bản (記述) |
| `TYPE_DATA_DATETIME` | 3 | Kiểu ngày tháng (年月日) |
| `TYPE_DATA_IMAGE` | 4 | Kiểu hình ảnh (画像) |
| `TYPE_DATA_FILE` | 5 | Kiểu PDF |
| `TYPE_DATA_POINT` | 6 | Kiểu điểm (ポイント) |

**Static methods:**
| Method | Dòng | Mô tả |
|--------|------|-------|
| `getNameById($id, $bot_id)` | 24 | Lấy title theo id + bot_id |
| `getFriendInfoSettingByFolderId($folder_id, $botId)` | 28 | Lấy danh sách settings theo folder. Hỗ trợ folder_id = -1 (default info), -2 (address info), >=0 (custom) |

**Ghi chú quan trọng**: `getFriendInfoSettingByFolderId()` (dòng 85-90) chỉ query `whereIn('type_data', [1, 2, 3, 6])` — loại trừ type 4 (image) và 5 (file) khỏi danh sách. **Mức độ tin cậy**: **Cao**

**Relationships**: Không khai báo explicit, nhưng được sử dụng qua `Category->friendInformationSetting()` (hasMany).

**Cột chính (suy luận từ code):**
| Cột | Kiểu | Mô tả | Nguồn |
|-----|------|-------|-------|
| `id` | int, PK | ID tự tăng | Code |
| `bot_id` | int, FK | ID bot (LINE OA account) | Code dòng 39, 84 |
| `title` | string | Tên quản lý (管理名) | Code dòng 951 |
| `type_data` | int | Kiểu dữ liệu (1-6) | Code dòng 948, constants |
| `group_id` | int | ID folder (category) | Code dòng 85, 952 |
| `order` | int | Thứ tự hiển thị | Code dòng 88, 674 |
| `setting_value` | text/JSON | Cấu hình actions (JSON string) | Code dòng 92, 1018 |
| `total_user_has_value` | int | Số người có giá trị | Code dòng 423, 805 |
| `created_at` | datetime | Ngày tạo | timestamps |
| `updated_at` | datetime | Ngày cập nhật | timestamps |

---

### FriendInformationValue
- **File**: `app/FriendInformationValue.php`
- **Table**: `friend_information_value`
- **Guarded**: `[]`
- **Timestamps**: Có

**Cột chính (suy luận từ code):**
| Cột | Kiểu | Mô tả | Nguồn |
|-----|------|-------|-------|
| `id` | int, PK | ID tự tăng | Code |
| `bot_id` | int, FK | ID bot | Code dòng 260 |
| `line_id` | int, FK | ID line_user | Code dòng 344 |
| `friend_information_setting_id` | int, FK | ID setting | Code dòng 261 |
| `friend_info_option_id` | int, FK | ID option select (cho type select) | Code dòng 984 |
| `value` | string | Giá trị đã ghi nhận | Code dòng 259, 344 |
| `action` | string/null | Trạng thái action đã thực thi | Code dòng 1151 |
| `created_at` | datetime | | timestamps |
| `updated_at` | datetime | | timestamps |

---

### FriendInfoOptionSelects
- **File**: `app/FriendInfoOptionSelects.php`
- **Table**: `friend_info_option_selects`
- **Guarded**: `[]`
- **Timestamps**: Có

**Cột chính (suy luận từ code):**
| Cột | Kiểu | Mô tả | Nguồn |
|-----|------|-------|-------|
| `id` | int, PK | ID tự tăng | Code dòng 970 |
| `bot_id` | int, FK | ID bot | Code dòng 890 |
| `friend_info_id` | int, FK | ID setting (friend_information_setting) | Code dòng 891 |
| `option_value` | string | Giá trị text của option | Code dòng 892 |
| `action_id` | int, FK | ID actions (bảng actions) | Code dòng 893 |

---

### ActionInfoFriendDefault
- **File**: `app/ActionInfoFriendDefault.php`
- **Table**: `action_info_friend_default`
- **Guarded**: `[]`
- **Timestamps**: Có

**Mục đích**: Lưu cấu hình action cho default info fields (vd: birthday `d_4`). Khi admin cấu hình action cho trường mặc định, dữ liệu lưu vào bảng này thay vì `friend_information_setting`.

**Cột chính (suy luận từ code):**
| Cột | Kiểu | Mô tả | Nguồn |
|-----|------|-------|-------|
| `id` | int, PK | | |
| `id_info` | string | ID default info (vd: 'd_4') | Code dòng 87, 125 |
| `bot_id` | int, FK | | Code dòng 87 |
| `setting_value` | text/JSON | Cấu hình actions | Suy luận từ flow |
| Các cột khác | | Tương tự FriendInformationSetting | Suy luận |

---

### SettingDisplayInfoFriendChat11
- **File**: `app/SettingDisplayInfoFriendChat11.php`
- **Table**: `setting_display_info_friend_chat11`
- **Guarded**: `[]`
- **Timestamps**: Có

**Mục đích**: Cấu hình hiển thị thông tin bạn bè trên giao diện chat 1:1. Khi xoá info setting → record tương ứng cũng bị xoá.

**Cột chính (suy luận từ code):**
| Cột | Kiểu | Mô tả | Nguồn |
|-----|------|-------|-------|
| `id_setting` | int | FK tới friend_information_setting.id | Code dòng 562, 609 |
| `bot_id` | int, FK | | Code dòng 562 |
| `type` | int | Loại setting (1 = friend info) | Code dòng 562 |

---

### Category (folder)
- **File**: `app/Category.php`
- **Table**: `category`

**Relationship với FriendInformationSetting:**
```php
// app/Category.php dòng 79
public function friendInformationSetting()
{
    return $this->hasMany('App\FriendInformationSetting', 'group_id', 'id');
}
```

**Static method:**
```php
// app/Category.php dòng 298
public static function getListInforFriendCategories($bot_id)
```
→ Query `category` LEFT JOIN `friend_information_setting` → đếm count items per folder, order by position DESC.

**category.kind = 12** (`config('sns-line.category_kind.information_friend')`) — phân biệt folder friend info với folder tag, template, v.v.

---

## 3. Services / Repositories

**Không có Service class riêng cho tính năng này.** Toàn bộ business logic nằm trực tiếp trong Controller.

**Helper functions liên quan** (file `app/Helpers/functions.php`):

| Function | Dòng | Mô tả |
|----------|------|-------|
| `getBotId()` | — | Lấy bot_id từ session |
| `addLogUserAction($action)` | — | Log hành động user |
| `sortRankItemsInfo($a, $b)` | 3544 | Sort items theo `order` DESC |
| `settingEventTimeFriendInfo($lineUserId, $friendInfoId, $botId, $date)` | 8535 | Tạo/cập nhật event_step_time cho action scheduling kiểu ngày tháng |
| `getNextDaySendTime($date)` | 11224 | Tính ngày gửi tiếp theo (cho action lặp hàng năm) |

**Mức độ tin cậy**: **Cao**

---

## 4. Form Requests / Validation

**Không sử dụng Form Request classes.** Validation được thực hiện trực tiếp trong controller:

| Validation | Vị trí | Mô tả |
|-----------|--------|-------|
| Folder tồn tại | `index()` dòng 46-53 | Query `category` where kind = 12, is_deleted = 0 |
| Folder hợp lệ khi tạo | `addInfo()` dòng 61-64 | Same check |
| Setting tồn tại | `editInfo()` dòng 84-91 | Query `FriendInformationSetting` + fallback `ActionInfoFriendDefault` |
| Bot đang backup | Nhiều methods | Check `BackupHistory` status ∈ [0, 1] → trả 500 |

**Validation phía client (JavaScript):**
- Tên quản lý: tối đa 20 ký tự (theo UI spec)
- Tên folder: tối đa 15 ký tự (theo UI spec)
- **Mức độ tin cậy**: **Trung bình** — chưa kiểm tra file JS/Blade

---

## 5. Events / Listeners / Queued Jobs

### Không phát hiện Events hoặc Listeners riêng cho tính năng này.

### Queued Jobs / Background Processing

**Phát hiện liên quan đến background job scheduling:**

Khi lưu setting kiểu `calendar` (type_data = 3) hoặc default birthday (`d_4`), controller tạo records trong `event_step` và `event_step_time` — đây là bảng mà **Spring Boot background job** đọc để gửi action tự động.

**Logic tạo event scheduling** (trong `saveSettingInfoFriend`, dòng 1044-1265):

1. **Xoá event_step cũ** cho friend_info_id này
2. **Tạo event_step mới** cho mỗi setting_action có action_id:
   ```
   event_step: {
     bot_id, type=3, friend_info_id, before_day, time_send,
     is_after_day, action_id, is_action_repeat, is_day_month
   }
   ```
3. **Tạo event_step_time** cho mỗi line_user có giá trị date:
   - Tính `sent_date_time` = date ± N ngày, lúc HH:mm
   - Nếu `option_compare1 = 1` (月日 mode) và thời gian đã qua → `addYear()` + `getNextDaySendTime()`
   - Nếu `option_compare2 = 1` → trước ngày (subDays), ngược lại → sau ngày (addDays)

**Ghi chú cho job-analyzer:** Bảng `event_step` (type = 3) + `event_step_time` là input cho Spring Boot job gửi action theo lịch. Cần phân tích job-side processing.

**Mức độ tin cậy**: **Cao**

---

### SyncElasticsearch

Khi xoá default field `d_1` (system_display / view_name), hệ thống insert record vào bảng `sync_elasticsearch`:
```php
// dòng 451
SyncElasticsearch::insertElasticsearch([
    'type' => config('sns-line.type_sync.update'),
    'line_user_id' => $lineId,
    'bot_id' => $bot_id,
    'data_sync' => json_encode($data_sync)
]);
```
→ Background process sẽ đồng bộ dữ liệu sang Elasticsearch.

**Mức độ tin cậy**: **Cao**

---

## 6. Authorization (Policies, Gates)

**Không phát hiện Policy hoặc Gate riêng cho tính năng này.**

Kiểm soát truy cập dựa trên:
1. **Session `bot_id`**: Mọi query đều filter theo `bot_id = getBotId()`. User chỉ thao tác được trên bot mà mình đang login.
2. **Backup lock**: Nhiều thao tác write kiểm tra `BackupHistory` — nếu bot đang backup thì chặn.
3. **Staff permissions**: Chưa phát hiện kiểm tra quyền Staff cụ thể cho tính năng này trong controller. **Mức độ tin cậy**: **Trung bình** — có thể kiểm tra ở middleware hoặc Blade view.

---

## 7. Business Rules (tổng hợp)

### BR-01: Hệ thống folder
- Folder lưu trong bảng `category` với `kind = 12` (`information_friend`)
- Folder mặc định (「未分類」) = `group_id = 0` — không phải record trong `category`, mà là convention
- Folder ID đặc biệt: `-1` = thông tin mặc định hệ thống, `-2` = thông tin địa chỉ
- Xoá folder → xoá toàn bộ info settings bên trong + values + options + display settings
- **File**: `FriendInformationController.php:542-569`
- **Mức độ tin cậy**: **Cao**

### BR-02: 6 kiểu dữ liệu (type_data)
| Giá trị | Config key | Tên JP | Có action? |
|---------|-----------|--------|-----------|
| 1 | `select` | 選択肢 | Có — action per option |
| 2 | `input` | 記述 | Không |
| 3 | `calendar` | 年月日 | Có — action scheduling |
| 4 | `image` | 画像 | Không rõ (bị loại khỏi query danh sách) |
| 5 | `file` | PDF | Không rõ (bị loại khỏi query danh sách) |
| 6 | `point` | ポイント | Có — action khi đạt ngưỡng |

**Ghi chú**: Type 4 (image) và 5 (file) bị `getFriendInfoSettingByFolderId()` loại khỏi `whereIn` (dòng 87). Nhưng `saveSettingInfoFriend()` không có check loại trừ → có thể tạo nhưng không hiển thị trong danh sách folder thông thường.
- **Mức độ tin cậy**: **Cao**

### BR-03: Cấu trúc setting_value (JSON)
```json
{
  "action_mode": 1,
  "setting_actions": [
    {
      "value": "Option text",
      "action_id": 123,
      "id": 456,
      "number": 5,
      "time": "16:40",
      "option_compare1": 1,
      "option_compare2": 1
    }
  ]
}
```

**Giải thích fields:**
| Field | Áp dụng type | Mô tả |
|-------|-------------|-------|
| `action_mode` | 1, 3, 6 | 1 = 一度のみ (1 lần), 2 = 何度でも稼働 (nhiều lần) |
| `value` | 1 (select) | Text hiển thị của option |
| `action_id` | 1, 3, 6 | FK tới bảng `actions` |
| `id` | 1 (select) | FK tới `friend_info_option_selects.id` |
| `number` | 3 (calendar) | Số ngày offset |
| `time` | 3 (calendar) | Giờ gửi (HH:mm) |
| `option_compare1` | 3 (calendar) | 1 = 月日 (tháng/ngày, lặp hàng năm), 2 = 年月日 (năm/tháng/ngày, 1 lần) |
| `option_compare2` | 3 (calendar) | 1 = 前 (trước), 2 = 後 (sau) |

- **Mức độ tin cậy**: **Cao**

### BR-04: Action mode và friend_information_value
- Khi `action_mode = 2` (何度でも稼働): cập nhật tất cả `friend_information_value.action = null` → reset để action có thể trigger lại
- Khi `action_mode = 1` (一度のみ): giữ nguyên → action chỉ trigger khi `action` field chưa có giá trị
- **File**: `FriendInformationController.php:1150-1152`
- **Mức độ tin cậy**: **Cao**

### BR-05: Sao chép info (deep clone)
Khi copy, hệ thống clone:
1. Record `friend_information_setting` (reset id, timestamps, total_user_has_value = 0)
2. Mỗi `actions` record → clone + gán action_id mới
3. Mỗi `action_detail` → clone với action_id mới
4. Mỗi `filter_v2` nếu `has_filters = 1` → clone qua `FilterV2::cloneFilters()`
5. Mỗi `friend_info_option_selects` (nếu type = select) → tạo mới với friend_info_id tạm = -1, sau cập nhật
6. `order` = max(order) + 1

- **File**: `FriendInformationController.php:830-928`
- **Mức độ tin cậy**: **Cao**

### BR-06: Xoá info setting cascade
Khi xoá 1 info setting (`deleteItem`):
1. Gọi `deleteDataFriendInfo()` → xoá `action_detail` type 'friend_info' tham chiếu đến info
2. Xoá `friend_information_value` theo setting_id
3. Xoá `friend_information_setting` record
4. Xoá `setting_display_info_friend_chat11` (hiển thị trên chat 1:1)
5. Xoá `friend_info_option_selects`

Khi xoá folder (`deleteGroup`):
- Tất cả bước trên cho mỗi info setting thuộc folder

- **File**: `FriendInformationController.php:590-636`
- **Mức độ tin cậy**: **Cao**

### BR-07: Backup lock
Mọi thao tác write (tạo/sửa/xoá folder, tạo/sửa/xoá item, copy, move) đều kiểm tra:
```php
$backuoHistory = BackupHistory::where('code', $bot->transfer_code)
    ->whereIn('status', [0, 1])->first();
if ($backuoHistory) {
    return response()->json(['status' => false, 'msg' => MESSAGE_NOTIFY_BACKUP], 500);
}
```
→ Nếu bot đang có backup đang chạy (status 0 = pending, 1 = processing) → chặn thao tác.

- **File**: `FriendInformationController.php:507, 544, 574, 593, 615, 639, 837, 937`
- **Mức độ tin cậy**: **Cao**

### BR-08: Event scheduling cho kiểu ngày tháng
Khi lưu setting type 3 (calendar):
1. Xoá `event_step_time` cũ
2. Xoá `event_step` cũ (type = 3, friend_info_id = id)
3. Tạo `event_step` mới cho mỗi action
4. Với mỗi line_user có giá trị date → tính `sent_date_time`:
   - `option_compare2 = 1` (前/trước): `date - N days`
   - `option_compare2 = 2` (後/sau): `date + N days`
   - Cộng thêm thời gian `HH:mm`
5. Nếu `sent_date_time` > now → insert `event_step_time`
6. Nếu `sent_date_time` <= now và `option_compare1 = 1` (月日): addYear() + getNextDaySendTime()

**event_step record:**
| Cột | Giá trị |
|-----|---------|
| `bot_id` | Bot ID |
| `type` | 3 (friend info date) |
| `friend_info_id` | ID setting hoặc 'd_4' |
| `before_day` | Số ngày offset |
| `time_send` | Giờ gửi HH:mm |
| `is_after_day` | 0 = trước, 1 = sau |
| `action_id` | FK → actions |
| `is_action_repeat` | 0 = 1 lần, 1 = nhiều lần |
| `is_day_month` | 1 = 月日 (lặp hàng năm), 0 = 年月日 (1 lần) |

- **File**: `FriendInformationController.php:1044-1265`
- **Mức độ tin cậy**: **Cao**

### BR-09: Cascading updates khi đổi tên option (type select)
Khi rename option value:
1. Cập nhật `friend_info_option_selects.option_value`
2. Cập nhật `friend_information_value.value` cho tất cả records có `friend_info_option_id` matching
3. Cập nhật `calendar_setting_send_forms.options` / `options_information_friend`
4. Cập nhật `calendar_salon_setting_send_forms` tương tự
5. Cập nhật `form_answer_details.settings.items`
6. Cập nhật `action_detail.data.content` cho actions tham chiếu option
7. Cập nhật `filter_v2.data.valueOption` + `selected_op` cho filters tham chiếu info

- **File**: `FriendInformationController.php:969-1406`
- **Mức độ tin cậy**: **Cao**

### BR-10: Default info fields (thông tin mặc định hệ thống)
Hệ thống có 2 nhóm fields mặc định (không lưu trong `friend_information_setting`):

**Nhóm 1 — Thông tin cơ bản** (group_id = -1):
| ID | Title | Field | Type |
|----|-------|-------|------|
| `d_1` | システム表示名 | `line_user.view_name` | 2 (text) |
| `d_2` | 携帯電話 | `line_user.phone_number` | 2 |
| `d_3` | メールアドレス | `line_user.email` | 2 |
| `d_4` | 生年月日 | `line_user.birthday` | 3 (date) |

**Nhóm 2 — Thông tin địa chỉ** (group_id = -2):
| ID | Title | Field | Type |
|----|-------|-------|------|
| `-7` | 郵便番号 | `zip_code` (friend_information_value) | 2 |
| `d_6` | 都道府県名 | `line_user.province` | 1 (select) |
| `-8` | 市区町村名 | `district` (friend_information_value) | 2 |
| `-9` | 町名/番地 | `township` (friend_information_value) | 2 |
| `-10` | 建物名・部屋番号 | `building` (friend_information_value) | 2 |

**Ghi chú**: `d_5` (年齢 / age) bị comment out trong config nhưng code vẫn hỗ trợ xoá (dòng 405-407).

- **File config**: `config/sns-line.php:751-920`
- **Mức độ tin cậy**: **Cao**

### BR-11: Đổi tên info → cập nhật ActionDetail
Khi title thay đổi, hệ thống tìm tất cả `action_detail` type = `'friend_info'` có data chứa info ID → cập nhật `data.name` thành title mới.
- **File**: `FriendInformationController.php:1023-1038`
- **Mức độ tin cậy**: **Cao**

### BR-12: Cookie lưu folder đang chọn
- Cookie name: `folder_info_friend`
- Format: JSON object `{ "{bot_id}": folder_id }`
- Path: `/basic/friend_information`
- Max age: 14400 phút (10 ngày)
- **File**: `FriendInformationController.php:40-53`
- **Mức độ tin cậy**: **Cao**

---

## 8. Bảng DB liên quan (tổng hợp)

| Bảng | Vai trò trong FA-015 | Model |
|------|----------------------|-------|
| `friend_information_setting` | Bảng chính — lưu cấu hình trường thông tin | `FriendInformationSetting` |
| `friend_information_value` | Lưu giá trị trường thông tin cho mỗi bạn bè | `FriendInformationValue` |
| `friend_info_option_selects` | Lưu danh sách options cho type select | `FriendInfoOptionSelects` |
| `action_info_friend_default` | Cấu hình action cho default fields (d_4 birthday) | `ActionInfoFriendDefault` |
| `category` | Folder (kind = 12) | `Category` |
| `setting_display_info_friend_chat11` | Cấu hình hiển thị trên chat 1:1 | `SettingDisplayInfoFriendChat11` |
| `line_user` | Thông tin bạn bè (default fields: view_name, phone, email, birthday, age, province) | `LineUser` |
| `bot_line_user` | Liên kết bot ↔ line_user | `BotLineUser` |
| `actions` | Action definitions | `Actions` |
| `action_detail` | Chi tiết action (type, data JSON) | `ActionDetail` |
| `event_step` | Cấu hình step scheduling (type = 3 cho friend info date) | `EventStep` |
| `event_step_time` | Lịch gửi action cụ thể cho từng user | — (dùng DB facade) |
| `filter_v2` | Bộ lọc tham chiếu friend info | `FilterV2` |
| `form_answer_details` | Chi tiết form answer liên kết friend info | `FormAnswerDetails` |
| `calendar_setting_send_forms` | Form gửi trong calendar lesson | `CalendarSettingSendForms` |
| `calendar_salon_setting_send_forms` | Form gửi trong calendar salon | `CalendarSalonSettingSendForms` |
| `backup_history` | Lịch sử backup (dùng cho backup lock) | `BackupHistory` |
| `sync_elasticsearch` | Queue đồng bộ Elasticsearch | `SyncElasticsearch` |
| `bots` | Thông tin bot | `Bots` |

---

## 9. Ghi chú cho bước tiếp theo

### Cho job-analyzer (bước 4):
- Bảng `event_step` (type = 3) + `event_step_time` chứa lịch gửi action tự động cho friend info kiểu ngày tháng
- Spring Boot job cần đọc `event_step_time` để gửi action khi đến `sent_date_time`
- Cần tìm job xử lý `event_step_time` trong source Spring Boot

### Cho db-mapper (bước 5):
- 17 bảng liên quan đã liệt kê ở mục 8
- Bảng chính: `friend_information_setting`, `friend_information_value`, `friend_info_option_selects`
- Bảng category dùng `kind = 12` để phân biệt folder friend info

### Điểm chưa rõ:
| # | Nội dung | Mức độ tin cậy |
|---|---------|---------------|
| 1 | Type 4 (image) và 5 (file) — có được lưu nhưng bị ẩn khỏi danh sách folder. Chưa rõ flow tạo/sửa chi tiết | **Trung bình** |
| 2 | Middleware authorization cho Staff — chưa phát hiện kiểm tra quyền cụ thể trong controller | **Trung bình** |
| 3 | Validation phía client (max length, required fields) — chưa kiểm tra JS/Blade | **Trung bình** |
| 4 | Export class `ExportListFriendOfInfo` — chưa đọc chi tiết format CSV output | **Trung bình** |
