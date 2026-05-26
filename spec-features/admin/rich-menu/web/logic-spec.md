# FA-004 Rich Menu「リッチメニュー」 — Logic Spec

## Tổng quan
- **Tính năng**: FA-004 Rich Menu
- **Controllers**:
  - `V2\RichMenuController` — `app/Http/Controllers/V2/RichMenuController.php`
  - `Basic\UserController` — `app/Http/Controllers/Basic/UserController.php`
- **Service**: `App\Services\V2\RichMenuService` — `app/Services/V2/RichMenuService.php`
- **Helper functions**: `app/Helpers/functions.php` (hàm `buildAreaRichmenu`, `createRichmenuLine`)

---

## 1. Controllers & Actions

### 1.1 V2\RichMenuController
**File**: `app/Http/Controllers/V2/RichMenuController.php` (918 dòng)
**Dependency injection**: `RichMenuService`
**Mức tin cậy**: **Cao**

| Method | Dòng | Logic chính |
|--------|------|-------------|
| `getListRichMenu()` | 51 | Query `rich_menus` theo `bot_id`, filter keyword (LIKE name), sort theo `position DESC`, paginate. Eager load `rich_menu_items`. Count `bot_line_user` (is_blocked=0) |
| `checkLimitBotPlan()` | 99 | Delegate sang `RichMenuService::isLimitedBotPlan()` |
| `getListFolderData()` | 116 | Lấy `Category` theo kind=rich_menus + thêm folder「未分類」(id=0) ở đầu. Đếm rich_menus theo group_id |
| `sortListFolderData()` | 147 | Kiểm tra backup đang chạy → cập nhật position folders qua `CategoryService::updatePosition()` |
| `addRichMenuFolder()` | 185 | Validate name (max:15). Nếu id → update, không → create qua `CategoryService` |
| `sortListRichMenu()` | 226 | Tương tự sortListFolderData nhưng cho rich_menus |
| `moveRichMenu()` | 264 | Cập nhật `group_id` cho danh sách rich_menu_ids, giữ nguyên `updated_at` |
| `quickAddRichMenu()` | 302 | Kiểm tra limit plan → validate trùng tên → tạo hoặc update quick. Mặc định `title_menu = '◀︎ お問合せ／メニュー ▲'` |
| `copyRichMenu()` | 360 | Kiểm tra limit plan → validate trùng tên → delegate `RichMenuService::copyRichMenu()` |
| `deleteRichMenu()` | 412 | Kiểm tra backup → delegate `RichMenuService::deleteRichMenu()` |
| `dataStatistic()` | 450 | Tính thống kê tap theo ngày/area, hỗ trợ export CSV (Shift_JIS encoding) |
| `initRichMenuRemoved()` | 495 | Query `rich_menus` onlyTrashed, paginate. Thêm username_del |
| `restoreRichmenuRemove()` | 535 | Kiểm tra limit plan → kiểm tra trùng tên → restore soft delete → restore folder nếu cần → **gọi LINE API** tạo lại Rich Menu |
| `ajaxGetRichMenuSetting()` | 607 | Lấy thông tin Rich Menu + đếm line_user + đếm tổng bạn bè qua filter |
| `saveSettingDisplayRichmenu()` | 645 | Cập nhật `status_link=1` → ghi `setting_display_rich_menu_histories` (action=SHOW) |
| `saveSettingStopRichmenu()` | 687 | Kiểm tra không phải mặc định → cập nhật `status_link=2, is_updated=2` → ghi history (action=STOP) |
| `handleSettingDisplayHistory()` | 732 | Private. Tạo/cập nhật bản ghi `setting_display_rich_menu_histories` |
| `deleteCategory()` | 751 | Di chuyển tất cả rich_menus về「未分類」(group_id=0) → xoá category |
| `saveRichMenuImageUpload()` | 762 | 2 chế độ: (1) update_template_type → đổi template, xoá items, step_active=3; (2) upload ảnh → validate kích thước/dung lượng → resize → lưu file → step_active=2 |
| `deleteSwitchRichMenu()` | 827 | Xoá `filter_v2` và `richmenu_switch_item` cho Rich Menu switch cụ thể |
| `settingDisplayHistories()` | 855 | Query `setting_display_rich_menu_histories` với filter date/action/status, sắp xếp, paginate. Eager load `richMenu:id,name` |
| `deleteSettingDisplayHistoryRichMenu()` | 888 | Xoá 1 bản ghi history, kiểm tra bot_id match |
| `filterFriend()` | 896 | Trang danh sách bạn bè theo history hiển thị. Paginate 100 items. View `filter_friend` |

### 1.2 Basic\UserController (phần Rich Menu)
**File**: `app/Http/Controllers/Basic/UserController.php`
**Dependency injection**: `RichMenuService`, `BotRepositoryInterface`, `UserRepositoryInterface`, `MessageService`
**Mức tin cậy**: **Cao**

| Method | Dòng | Logic chính |
|--------|------|-------------|
| `richMenu()` | 243 | Render view `basic.rich_menu.v2.index` |
| `editRichMenuForm()` | 176 | Nếu có id → load rich menu từ DB. Xoá filter orphan (rich_menu_item_id < 0). Tính flagNewFreePlan dựa trên ngày tạo account vs 2021-07-01. Render view `basic.rich_menu.v2.create` |
| `saveNewRichMenu()` | 742 | Kiểm tra empty items → kiểm tra plan limit → kiểm tra backup → tạo `rich_menus` → lưu ảnh (resize nếu >1MB) → tạo `rich_menu_items` cho mỗi area → **gọi LINE API** tạo Rich Menu → upload ảnh → tạo alias |
| `updateRichMenu()` | 1172 | Tương tự saveNew, nhưng cập nhật. Nếu id chưa tồn tại → tạo mới qua quickAdd. Xoá items/click_detail cũ không còn. set `step_active = 4`. **Gọi LINE API** tạo lại |
| `hideRichMenuUser()` | 1877 | Kiểm tra không phải mặc định → set `status_rich=0, status_link=2` → ghi `richmenu_update_history (is_updated=2)` |
| `displayRichMenuUser()` | 1925 | Set `status_rich=1, status_link=1` |
| `setRichMenuAllUser()` | 1943 | Đặt/gỡ mặc định. Nếu đặt: reset all status_line=0, set target status_line=1 + is_updated=3. Nếu gỡ: set status_line=0 + is_updated=4. Ghi richmenu_update_history |
| `deleteRichMenuAllUser()` | 2008 | Gỡ mặc định: status_line=0, status_link=2, is_updated=4 |
| `ajaxInitSettingAction()` | 227 | Load `action_details` theo action_id, init data cho mỗi action. Nếu type=tag → load danh sách tags |
| `settingDisplayRichMenu()` | 4591 | Render view `basic.rich_menu.v2.setting_display` |
| `saveBasicRichMenu()` | 4602 | **Lưu ý: method này rỗng** — `$request->only([])` trả về mảng rỗng → không cập nhật gì |
| `settingDisplayHistoryRichMenu()` | 4615 | Render view `basic.rich_menu.v2.setting_display_history` |

---

## 2. Models Eloquent

### 2.1 RichMenus
**File**: `app/RichMenus.php`
**Table**: `rich_menus`
**Mức tin cậy**: **Cao**

| Thuộc tính | Mô tả |
|-----------|-------|
| `$table` | `rich_menus` |
| `$guarded` | `[]` (mass assignable) |
| `$timestamps` | `true` |
| SoftDeletes | Có (`deleted_at`) |

**Relationships**:
| Tên | Kiểu | Model liên kết | FK |
|-----|------|---------------|-----|
| `rich_menu_items()` | hasMany | `RichMenuItems` | `rich_id` |
| `botLineUser()` | hasMany | `BotLineUser` | `rich_menu_id` |

**Scopes**:
| Scope | Logic |
|-------|-------|
| `scopeIgnoreRichNoneSetting` | `whereNotNull('rich_menu_id')->where('step_active', 4)` — chỉ lấy Rich Menu đã hoàn thành và có LINE rich_menu_id |

**Static methods**:
| Method | Logic |
|--------|-------|
| `getNameById($id, $bot_id)` | Trả về tên Rich Menu theo id và bot_id |

### 2.2 RichMenuItems
**File**: `app/RichMenuItems.php`
**Table**: `rich_menu_items`
**Mức tin cậy**: **Cao**

| Thuộc tính | Mô tả |
|-----------|-------|
| `$table` | `rich_menu_items` |
| `$guarded` | `[]` |
| SoftDeletes | Có |

**Relationships**:
| Tên | Kiểu | Model liên kết | FK |
|-----|------|---------------|-----|
| `rich_menus()` | belongsTo | `RichMenus` | `rich_menu_id` |
| `formAnswer()` | hasOne | `FormAnswer` | `id` ← `form_answer_id` |
| `tag()` | hasOne | `Tags` | `id` ← `tag_id` |
| `autoReply()` | hasOne | `AutoReply` | `id` ← `keyword_id` |

**Cột quan trọng (từ code)**:
- `rich_id`: FK → `rich_menus.id`
- `bot_id`: FK → `bots.id`
- `action_type`: kiểu action (`RICH`, `TEXT`, `EMAIL`, `TEL`, `URL`, ...)
- `x`, `y`, `width`, `height`: toạ độ vùng tap (đã nhân 3 khi lưu)
- `action_id`: FK → `actions.id`
- `type_open_url`, `content_open_url`: cấu hình URL/action
- `type_bill_product`: loại sản phẩm (cho action mở trang bán hàng)
- `sort`: thứ tự area
- `form_answer_id`, `tag_id`, `keyword_id`: FK cho các loại action cụ thể

### 2.3 SettingDisplayRichMenuHistory
**File**: `app/SettingDisplayRichMenuHistory.php`
**Table**: `setting_display_rich_menu_histories`
**Mức tin cậy**: **Cao**

**Constants**:
```php
ACTION = ['SHOW' => 1, 'STOP' => 2]
TYPE = ['NOW' => 1, 'TIMER' => 2]
STATUS = ['WAITING' => 1, 'PROCESSING' => 2, 'DONE' => 3, 'DRAFT' => 4]
```

**Relationships**:
| Tên | Kiểu | Model liên kết | FK |
|-----|------|---------------|-----|
| `richMenu()` | belongsTo | `RichMenus` | `rich_id` |

**Cột quan trọng (từ code)**:
- `bot_id`, `rich_id`, `date_setting`, `action`, `status`, `filter_id`, `type`

### 2.4 RichMenuSwitchItem
**File**: `app/RichMenuSwitchItem.php`
**Table**: `richmenu_switch_item`
**Mức tin cậy**: **Cao**

**Cột quan trọng (từ code)**:
- `bot_id`, `richmenu_parent_id`, `richmenu_item_id`, `richmenu_switch_id`

### 2.5 RichMenuFilterFriend
**File**: `app/RichMenuFilterFriend.php`
**Table**: `rich_menu_filter_friends` (convention)
**Mức tin cậy**: **Cao**

**Relationships**:
| Tên | Kiểu | Model liên kết | FK |
|-----|------|---------------|-----|
| `lineUser()` | belongsTo | `LineUser` | `line_id` |

**Cột quan trọng (từ code)**:
- `rich_display_history_id`: FK → `setting_display_rich_menu_histories.id`
- `line_id`: FK → `line_users`

### 2.6 Các models liên quan (không thuộc FA-004 nhưng được sử dụng)
| Model | Table | Vai trò trong Rich Menu |
|-------|-------|------------------------|
| `Category` | `category` | Folder/nhóm phân loại Rich Menu (`kind = rich_menus`) |
| `Actions` | `actions` | Bảng action chung — liên kết action config cho mỗi area |
| `ActionDetail` | `action_details` | Chi tiết action: type, data (JSON), has_filters |
| `BotLineUser` | `bot_line_user` | Mapping user ↔ bot, có `rich_menu_id` để biết user đang xem Rich Menu nào |
| `DetailClickRichMenu` | `detail_click_rich_menu` | Log mỗi lần user tap vào area |
| `FilterV2` | `filter_v2` | Filter cho Rich Menu switch và action filter |
| `Bots` | `bots` | Thông tin bot (plan_type, channel_access_token, liff_app_id) |
| `BackupHistory` | `backup_history` | Kiểm tra backup đang chạy → chặn thao tác sửa/xoá |

---

## 3. Services

### 3.1 RichMenuService
**File**: `app/Services/V2/RichMenuService.php` (475 dòng)
**Dependencies**: `CategoryService`
**Mức tin cậy**: **Cao**

| Method | Dòng | Logic |
|--------|------|-------|
| `isLimitedBotPlan($limit=2)` | 40 | Free plan + đã có >= 2 Rich Menu → trả true |
| `isRunningBackup()` | 54 | Kiểm tra `backup_history` có status CREATING hoặc PENDING |
| `updateFolderPosition($ids, $order)` | 67 | Delegate sang `CategoryService::updatePosition('category', ...)` |
| `updateFolder($name, $id)` | 76 | Nếu id → update category, không → create category với kind=rich_menus |
| `updateQuickRichMenu($id, $name, $folderId)` | 88 | Validate trùng tên → update name + group_id |
| `getPositionRichMenu($isTop, $groupId)` | 109 | isTop=true → max(position)+1, false → min(position)-1 |
| `quickAddRichMenu($name, $folderId, $isTop)` | 123 | Validate trùng tên → tạo rich_menus record |
| `updateRichMenuPosition($ids, $order)` | 143 | Delegate sang `CategoryService::updatePosition('rich_menus', ...)` |
| `moveRichMenu($ids, $folderId)` | 152 | Update group_id, position tăng dần, giữ nguyên updated_at |
| `validateDuplicateRichMenuName($name)` | 168 | Lấy tất cả name trong bot → kiểm tra trùng → throw Exception nếu trùng |
| `copyRichMenu($oldId, $name, $folderId, $isTop)` | 177 | Clone rich_menus + rich_menu_items + actions + action_details + filter_v2. Copy file ảnh. Gọi LINE API tạo Rich Menu mới |
| `deleteRichMenu($ids, $isForceDelete)` | 292 | Soft delete rich_menus + items. Ghi richmenu_update_history. Xoá action_details liên quan. Xoá switch_items, click_detail, display_history |
| `deletedDataRichMenu($id)` | 335 | Dọn dẹp dữ liệu liên quan khi xoá: action_details (type=richmenu), richmenu_switch_item, detail_click_rich_menu, setting_display_rich_menu_histories |
| `calculateStatistic($richId, $start, $end, $params)` | 350 | Đếm DetailClickRichMenu theo ngày/area. Hỗ trợ pagination trên listDay. Trả về data cho biểu đồ + tổng tap mỗi area |
| `deleteCategory($cat)` | 425 | Di chuyển tất cả rich_menus (kể cả trashed) về group_id=0 → xoá category |
| `resizeImage($imageInfo, $id)` | 431 | Resize ảnh xuống <1MB (nén quality dần). Lưu file JPG vào `msg_template/media/images/{admin_id}/{bot_id}/rich-menu/` |

---

## 4. Helper Functions (Global)

### 4.1 `buildAreaRichmenu()`
**File**: `app/Helpers/functions.php:10390`
**Mức tin cậy**: **Trung bình** — chưa đọc chi tiết toàn bộ hàm

**Vai trò**: Xây dựng mảng `areas` (bounds + actions) cho LINE Rich Menu API từ danh sách `richMenuItems`.

**Logic chính** (suy luận từ cách sử dụng):
- Duyệt qua từng item → tạo/update record `rich_menu_items` trong DB
- Build `bounds` (toạ độ vùng tap)
- Build `actions` (loại action theo actionType: RICH → richmenuswitch, TEXT → message/uri, EMAIL → uri, TEL → uri, URL → uri)
- Trả về `['arrayItemId' => [...], 'actions' => [...], 'bounds' => [...]]`

### 4.2 `createRichmenuLine()`
**File**: `app/Helpers/functions.php:10807`
**Mức tin cậy**: **Cao**

**Vai trò**: Tạo Rich Menu trên LINE platform qua API.

**Luồng xử lý**:
1. Build payload cho LINE API: `size`, `selected`, `name`, `chatBarText`, `areas`
2. `POST https://api.line.me/v2/bot/richmenu` → nhận `richMenuId`
3. Upload ảnh: `POST https://api-data.line.me/v2/bot/richmenu/{richMenuId}/content` (image/jpeg)
4. Cập nhật `rich_menus.rich_menu_id` = richMenuId từ LINE
5. Quản lý alias: kiểm tra alias tồn tại → update hoặc create mới
   - Alias format: `{PREFIX_ALIAS_ID_RICHMENU}-{rich_menu.id}`
   - API: `POST https://api.line.me/v2/bot/richmenu/alias` hoặc `POST https://api.line.me/v2/bot/richmenu/alias/{aliasId}`

---

## 5. Validation Rules

### Tạo Rich Menu
| Field | Rule | Source |
|-------|------|--------|
| `rich_menu_name` | required, string, max:50 | `V2\RichMenuController@quickAddRichMenu:316` |
| `folder_id` | required, integer | `V2\RichMenuController@quickAddRichMenu:317` |
| `is_top_folder` | nullable, boolean | `V2\RichMenuController@quickAddRichMenu:318` |
| Trùng tên | throw Exception | `RichMenuService::validateDuplicateRichMenuName` |
| Free plan limit | max 2 Rich Menu | `RichMenuService::isLimitedBotPlan` |

### Upload ảnh
| Field | Rule | Source |
|-------|------|--------|
| Kích thước | 2500x1686 hoặc 2500x843 | `V2\RichMenuController@saveRichMenuImageUpload:793` |
| Dung lượng | max 10MB | `V2\RichMenuController@saveRichMenuImageUpload:797` |

### Folder
| Field | Rule | Source |
|-------|------|--------|
| `name` | required, string, max:15 | `V2\RichMenuController@addRichMenuFolder:190` |

---

## 6. Authorization

**Mức tin cậy**: **Trung bình** — không tìm thấy Policy/Gate riêng cho Rich Menu

- Không có FormRequest classes riêng cho Rich Menu
- Không có Policy classes cho RichMenus model
- Xác thực dựa trên session (middleware `web`) + helper `getBotId()` để scope theo bot hiện tại
- `checkAccessFilter($botId)` kiểm tra quyền truy cập filter nâng cao
- Kiểm tra backup đang chạy (`isRunningBackup()`) chặn mọi thao tác sửa/xoá
- Plan restriction: free plan giới hạn 2 Rich Menu

---

## 7. Events / Listeners / Queued Jobs

**Mức tin cậy**: **Trung bình**

Không phát hiện Event/Listener Laravel dispatch trực tiếp trong code Rich Menu. Tuy nhiên, phát hiện cơ chế **queue table** rõ ràng:

### 7.1 Bảng `richmenu_update_history`
- **Ghi bởi**: `deleteRichMenu`, `hideRichMenuUser`, `setRichMenuAllUser`, `deleteRichMenuAllUser`, `restoreRichmenuRemove`
- **Cột chính**: `bot_id`, `richmenu_id`, `rich_menu_id_current`, `rich_menu_id_old`, `is_updated`, `status`
- **Status column**: `status = 0` (chờ xử lý)
- **is_updated values**: 2=ẩn, 3=đặt mặc định, 4=gỡ mặc định, 5=xoá
- **→ Background job (Spring Boot) quét bảng này**, thực hiện gọi LINE Messaging API để link/unlink Rich Menu cho từng user

### 7.2 Bảng `setting_display_rich_menu_histories`
- **Ghi bởi**: `saveSettingDisplayRichmenu`, `saveSettingStopRichmenu`
- **Status flow**: `WAITING (1)` → `PROCESSING (2)` → `DONE (3)`
- **Cột chính**: `bot_id`, `rich_id`, `date_setting`, `action` (1=show, 2=stop), `status`, `filter_id`, `type` (1=now, 2=timer)
- **→ Background job quét bảng này**, khi `date_setting` đến hạn → thực thi hiển thị/dừng Rich Menu

### 7.3 Cột `rich_menus.queue_richmenu_id`
- Phát hiện trong `copyRichMenu` (dòng 219): `queue_richmenu_id => null` khi copy
- Gợi ý có queue/job xử lý Rich Menu image → set cột này

**→ Cần phân tích Spring Boot source (`src/job/`) trong bước job-analyzer để xác nhận chi tiết**

---

## 8. Business Rules (tổng hợp)

### BR-01: Giới hạn plan
- Free plan (`plan_type = 2` hoặc contract_type = 'free'): tối đa 2 Rich Menu
- Áp dụng khi: tạo mới, copy, restore
- **Source**: `RichMenuService::isLimitedBotPlan()` (dòng 40-52)

### BR-02: Trùng tên quản lý
- Tên quản lý (`name`) phải duy nhất trong cùng bot
- Kiểm tra khi: tạo mới, copy, restore, update quick
- **Source**: `RichMenuService::validateDuplicateRichMenuName()` (dòng 168-175)

### BR-03: Backup đang chạy → chặn thao tác
- Khi `backup_history` có status CREATING hoặc PENDING → không cho tạo/sửa/xoá/sort
- **Source**: `RichMenuService::isRunningBackup()` (dòng 54-65)

### BR-04: Rich Menu mặc định không thể dừng
- Rich Menu có `status_line = 1` (mặc định) → không cho phép ẩn hoặc đặt lịch hiển thị
- **Source**: `hideRichMenuUser:1889`, `saveSettingStopRichmenu:696`, `setRichMenuAllUser:1964`

### BR-05: Step workflow
- `step_active` theo dõi bước hiện tại: 1=upload ảnh, 2=chọn area, 3=action, 4=hoàn thành
- Upload ảnh mới → reset step_active = 2
- Đổi template → reset step_active = 3, xoá tất cả items
- Lưu đầy đủ (save/update) → set step_active = 4
- Rich Menu chỉ được coi là hoàn chỉnh khi `step_active = 4` và `rich_menu_id IS NOT NULL`
- **Source**: `scopeIgnoreRichNoneSetting` (RichMenus.php:31), `saveRichMenuImageUpload:807`

### BR-06: Toạ độ area nhân 3
- Khi lưu `rich_menu_items`, toạ độ x/y/width/height từ frontend được **nhân 3** trước khi lưu DB
- Lý do: frontend hiển thị ảnh thu nhỏ (1/3 kích thước gốc)
- **Source**: `saveNewRichMenu:899-902`

### BR-07: Ảnh resize xuống 1MB
- LINE API yêu cầu ảnh Rich Menu dưới 1MB
- Upload ảnh > 1MB → nén quality dần (giảm 5% mỗi lần) cho đến khi < 1MB hoặc quality < 50%
- **Source**: `updateRichMenu:1273-1298`, `RichMenuService::resizeImage()` (dòng 431-474)

### BR-08: Rich Menu alias trên LINE
- Mỗi Rich Menu có alias dạng `{PREFIX_ALIAS_ID_RICHMENU}-{id}`
- Alias dùng cho tính năng Rich Menu switch (chuyển đổi menu khi tap area)
- Khi tạo/cập nhật → kiểm tra alias tồn tại → update hoặc create
- **Source**: `createRichmenuLine()` (functions.php:10868-10920)

### BR-09: Action types trong Rich Menu area
- `RICH`: richmenuswitch — chuyển sang Rich Menu khác qua alias
- `TEXT`: message hoặc uri (nếu có action_id → mở LIFF app)
- `EMAIL`: uri (mở email, nếu có action_id → mở LIFF app)
- `TEL`: suy luận tương tự (gọi điện)
- `URL`: mở URL trực tiếp
- Mỗi item có thể có `action_id` → liên kết bảng `actions` + `action_details` cho Friend Action (SC-004)
- **Source**: `saveNewRichMenu:910-934`

### BR-10: Soft delete và restore
- Xoá Rich Menu: soft delete `rich_menus` + `rich_menu_items`
- Restore: kiểm tra trùng tên → restore records → restore folder nếu bị xoá → gọi LINE API tạo lại
- Restore cũng bị giới hạn plan (free plan max 2)
- **Source**: `deleteRichMenu()`, `restoreRichmenuRemove()`

### BR-11: Đặt lịch hiển thị/dừng
- Type=1 (NOW): `date_setting = now()` → job xử lý ngay
- Type=2 (TIMER): `date_setting = date + time` → job xử lý khi đến hạn
- Có thể chọn hiển thị cho: tất cả bạn bè (`type_filter=0`) hoặc chọn riêng (`type_filter=1` + `filter_ids`)
- **Source**: `handleSettingDisplayHistory()` (dòng 732-750)

---

## 9. Bảng DB sử dụng (tổng hợp)

| Bảng | Vai trò trong Rich Menu | Ghi/Đọc |
|------|------------------------|---------|
| `rich_menus` | Bảng chính | Đọc/Ghi |
| `rich_menu_items` | Các area (vùng tap) | Đọc/Ghi |
| `category` | Folder phân loại (kind=rich_menus) | Đọc/Ghi |
| `actions` | Action config chung | Đọc/Ghi |
| `action_details` | Chi tiết action (type, data JSON) | Đọc/Ghi |
| `bot_line_user` | Mapping user ↔ Rich Menu hiện tại | Đọc |
| `detail_click_rich_menu` | Log tap area | Đọc/Ghi |
| `richmenu_update_history` | Queue xử lý đồng bộ LINE (background job) | Ghi |
| `setting_display_rich_menu_histories` | Lịch sử và lịch hẹn hiển thị/dừng | Đọc/Ghi |
| `richmenu_switch_item` | Config chuyển đổi Rich Menu | Đọc/Ghi |
| `rich_menu_filter_friends` | Danh sách bạn bè theo filter hiển thị | Đọc |
| `filter_v2` | Filter cho switch và action | Đọc/Ghi |
| `bots` | Thông tin bot, plan, token | Đọc |
| `backup_history` | Kiểm tra backup đang chạy | Đọc |
| `users` | Thông tin user (admin_id, username) | Đọc |
| `bot_contracts` + `bot_slots` | Kiểm tra plan/contract | Đọc |

---

## 10. Liên kết LINE API

| API | Method | URL | Sử dụng khi |
|-----|--------|-----|------------|
| Tạo Rich Menu | POST | `https://api.line.me/v2/bot/richmenu` | Save, Update, Copy, Restore |
| Upload ảnh Rich Menu | POST | `https://api-data.line.me/v2/bot/richmenu/{id}/content` | Save, Update, Copy, Restore |
| Lấy alias info | GET | `https://api.line.me/v2/bot/richmenu/alias/{aliasId}` | Save, Update |
| Cập nhật alias | POST | `https://api.line.me/v2/bot/richmenu/alias/{aliasId}` | Save, Update (alias đã tồn tại) |
| Tạo alias | POST | `https://api.line.me/v2/bot/richmenu/alias` | Save, Update (alias chưa tồn tại) |

**Mức tin cậy**: **Cao** — đọc trực tiếp từ `createRichmenuLine()` trong `functions.php`

**Lưu ý**: Các thao tác link/unlink Rich Menu cho từng LINE user (hiển thị/dừng) được xử lý bởi **background job**, không phải trong Laravel code. Background job đọc từ `richmenu_update_history` và `setting_display_rich_menu_histories`.
