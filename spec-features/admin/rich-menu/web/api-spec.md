# FA-004 Rich Menu「リッチメニュー」 — API Spec

## Tổng quan
- **Tính năng**: FA-004 Rich Menu
- **Controllers chính**:
  - `V2\RichMenuController` — `app/Http/Controllers/V2/RichMenuController.php` (918 dòng)
  - `Basic\UserController` — `app/Http/Controllers/Basic/UserController.php` (4906 dòng, phần rich menu)
- **Service**: `App\Services\V2\RichMenuService` — `app/Services/V2/RichMenuService.php`
- **Middleware chung**: `web`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`

---

## Danh sách Endpoints

| EP | Method | URL | Mô tả | Controller | Màn hình |
|----|--------|-----|-------|-----------|----------|
| EP-01 | GET | `/basic/rich-menu` | Trang danh sách Rich Menu (HTML) | `Basic\UserController@richMenu` | SCR-RCM-01 |
| EP-02 | GET | `/basic/rich-menu/edit/{id}` | Trang chỉnh sửa Rich Menu (HTML) | `Basic\UserController@editRichMenuForm` | SCR-RCM-03~06 |
| EP-03 | GET | `/basic/rich-menu/create` | Trang tạo mới Rich Menu (HTML) | `Basic\UserController@editRichMenuForm` | SCR-RCM-03 |
| EP-04 | GET | `/ajax/rich-menu/list/{folderId}` | Lấy danh sách Rich Menu theo folder | `V2\RichMenuController@getListRichMenu` | SCR-RCM-01 |
| EP-05 | GET | `/ajax/folder/rich-menu` | Lấy danh sách folder Rich Menu | `V2\RichMenuController@getListFolderData` | SCR-RCM-01 |
| EP-06 | POST | `/ajax/folder/rich-menu/add` | Tạo/sửa folder | `V2\RichMenuController@addRichMenuFolder` | SCR-RCM-01 |
| EP-07 | POST | `/ajax/folder/rich-menu/sort` | Sắp xếp thứ tự folder | `V2\RichMenuController@sortListFolderData` | SCR-RCM-01 |
| EP-08 | POST | `/ajax/rich-menu/quick-create` | Tạo nhanh Rich Menu (modal) | `V2\RichMenuController@quickAddRichMenu` | SCR-RCM-02 |
| EP-09 | POST | `/ajax/rich-menu/upload-image` | Upload ảnh + cập nhật template | `V2\RichMenuController@saveRichMenuImageUpload` | SCR-RCM-03 |
| EP-10 | POST | `/basic/rich-menu/save` | Lưu Rich Menu mới (full data) | `Basic\UserController@saveNewRichMenu` | SCR-RCM-03~06 |
| EP-11 | POST | `/basic/rich-menu/update` | Cập nhật Rich Menu (full data) | `Basic\UserController@updateRichMenu` | SCR-RCM-03~06 |
| EP-12 | POST | `/ajax/rich-menu/list/sort` | Sắp xếp thứ tự Rich Menu | `V2\RichMenuController@sortListRichMenu` | SCR-RCM-01 |
| EP-13 | POST | `/ajax/rich-menu/move-folder` | Di chuyển Rich Menu sang folder khác | `V2\RichMenuController@moveRichMenu` | SCR-RCM-01 |
| EP-14 | POST | `/ajax/rich-menu/copy` | Sao chép Rich Menu | `V2\RichMenuController@copyRichMenu` | SCR-RCM-01 |
| EP-15 | POST | `/ajax/rich-menu/delete` | Xoá Rich Menu (soft delete) | `V2\RichMenuController@deleteRichMenu` | SCR-RCM-01 |
| EP-16 | POST | `/ajax/rich-menu/delete-category/{id}` | Xoá folder | `V2\RichMenuController@deleteCategory` | SCR-RCM-01 |
| EP-17 | GET | `/basic/rich-menu/setting-display/{id}` | Trang hiển thị/dừng Rich Menu (HTML) | `Basic\UserController@settingDisplayRichMenu` | SCR-RCM-07 |
| EP-18 | POST | `/ajax/get-rich-menu/setting` | Lấy cài đặt Rich Menu cho màn display/stop | `V2\RichMenuController@ajaxGetRichMenuSetting` | SCR-RCM-07 |
| EP-19 | POST | `/ajax/rich-menu/save-setting-display` | Lưu cài đặt hiển thị Rich Menu | `V2\RichMenuController@saveSettingDisplayRichmenu` | SCR-RCM-07 |
| EP-20 | POST | `/ajax/rich-menu/save-setting-stop` | Lưu cài đặt dừng Rich Menu | `V2\RichMenuController@saveSettingStopRichmenu` | SCR-RCM-07 |
| EP-21 | GET | `/ajax/rich-menu/setting-display-history` | Lấy lịch sử hiển thị/dừng | `V2\RichMenuController@settingDisplayHistories` | SCR-RCM-08 |
| EP-22 | DELETE | `/ajax/rich-menu/setting-display-history/{item}` | Xoá 1 bản ghi lịch sử | `V2\RichMenuController@deleteSettingDisplayHistoryRichMenu` | SCR-RCM-08 |
| EP-23 | GET | `/basic/rich-menu/setting-display-history` | Trang lịch sử hiển thị (HTML) | `Basic\UserController@settingDisplayHistoryRichMenu` | SCR-RCM-08 |
| EP-24 | GET | `/ajax/rich-menu/data-statistic/{richMenu}` | Thống kê số lần tap theo ngày | `V2\RichMenuController@dataStatistic` | SCR-RCM-01 |
| EP-25 | GET | `/basic/rich-menu/removed` | Trang danh sách đã xoá (HTML) | `V2\RichMenuController@removed` | SCR-RCM-01 |
| EP-26 | GET | `/ajax/rich-menu-remove` | Lấy danh sách Rich Menu đã xoá | `V2\RichMenuController@initRichMenuRemoved` | SCR-RCM-01 |
| EP-27 | POST | `/ajax/rich-menu-restore` | Khôi phục Rich Menu đã xoá | `V2\RichMenuController@restoreRichmenuRemove` | SCR-RCM-01 |
| EP-28 | POST | `/ajax/init-data-setting-action-richmenu` | Lấy action details cho Rich Menu item | `Basic\UserController@ajaxInitSettingAction` | SCR-RCM-05 |
| EP-29 | POST | `/ajax/richmenu/delete-switch-rich-menu` | Xoá cài đặt chuyển đổi Rich Menu | `V2\RichMenuController@deleteSwitchRichMenu` | SCR-RCM-05 |
| EP-30 | POST | `/basic/rich-menu/display-rich-menu-user` | Hiển thị Rich Menu cho user (legacy) | `Basic\UserController@displayRichMenuUser` | SCR-RCM-07 |
| EP-31 | POST | `/basic/rich-menu/hide-rich-menu-user` | Ẩn Rich Menu cho user (legacy) | `Basic\UserController@hideRichMenuUser` | SCR-RCM-07 |
| EP-32 | POST | `/basic/rich-menu/set-rich-menu-all-user` | Đặt Rich Menu làm mặc định cho tất cả | `Basic\UserController@setRichMenuAllUser` | SCR-RCM-07 |
| EP-33 | POST | `/basic/rich-menu/delete-rich-all-user` | Xoá Rich Menu mặc định | `Basic\UserController@deleteRichMenuAllUser` | SCR-RCM-07 |
| EP-34 | GET | `/basic/rich-menu/filter-friend/{id}` | Xem danh sách bạn bè theo filter hiển thị | `V2\RichMenuController@filterFriend` | SCR-RCM-07 |
| EP-35 | PUT | `/basic/v2/rich-menu/{richMenu}` | Cập nhật thông tin cơ bản Rich Menu | `Basic\UserController@saveBasicRichMenu` | SCR-RCM-03 |
| EP-36 | GET | `/basic/rich-menu/detail-click/{id}` | Trang thống kê click chi tiết (HTML) | `Basic\UserController@detailClickRichMenu` | SCR-RCM-01 |
| EP-37 | POST | `/ajax/richmenu/copy-action-rich-item` | Sao chép action từ item khác | `Basic\UserController@copyActionRichItem` | SCR-RCM-05 |
| EP-38 | POST | `/basic/rich-menu/getActionDetail` | Lấy chi tiết action của Rich Menu | `Basic\UserController@getActionDetail` | SCR-RCM-05 |
| EP-39 | POST | `/basic/rich-menu/delete-rich-menus` | Xoá nhiều Rich Menu (legacy) | `Basic\UserController@deleteRichMenus` | SCR-RCM-01 |
| EP-40 | POST | `/basic/rich-menu/delete-group-rich-menu` | Xoá group Rich Menu (legacy) | `Basic\UserController@deleteGroupRichMenus` | SCR-RCM-01 |

---

## Chi tiết Endpoints

### EP-04: GET `/ajax/rich-menu/list/{folderId}`
**Mô tả**: Lấy danh sách Rich Menu theo folder, hỗ trợ filter, sort, pagination
**Controller**: `V2\RichMenuController@getListRichMenu` (dòng 51-97)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `folderId` | URL path | int | Có | ID folder (0 = 未分類) |
| `filter[keyword]` | query | string | Không | Tìm theo tên quản lý (LIKE) |
| `sorter[]` | query | array | Không | Mảng `{column, dir}`. Mặc định: `position DESC, created_at DESC` |
| `limit` | query | int | Không | Số item/trang. Nếu không truyền → lấy tất cả |

#### Response thành công (200)
```json
{
  "status": true,
  "data": {
    "data": [
      {
        "id": 1,
        "group_id": 0,
        "name": "メインメニュー",
        "url_image": "msg_template/media/images/.../richmenu_xxx.jpg",
        "open_date": null,
        "close_date": null,
        "created_at": "2024-01-01 00:00:00",
        "updated_at": "2024-01-01 00:00:00",
        "status": 1,
        "step_active": 4,
        "width": 2500,
        "height": 1686,
        "count_line_user": 150,
        "rich_menu_items": [...]
      }
    ],
    "current_page": 1,
    "last_page": 1,
    "per_page": 100,
    "total": 5
  }
}
```

#### Ghi chú
- `count_line_user`: đếm `bot_line_user` có `rich_menu_id` = id này và `is_blocked = 0`
- Khi `filter[keyword]` có giá trị → bỏ qua `folderId`, tìm toàn bộ

---

### EP-05: GET `/ajax/folder/rich-menu`
**Mô tả**: Lấy danh sách folder Rich Menu
**Controller**: `V2\RichMenuController@getListFolderData` (dòng 116-145)
**Mức tin cậy**: **Cao**

#### Response thành công (200)
```json
{
  "data": [
    {"id": 0, "name": "未分類", "is_default": 1, "position": 0, "count": 3},
    {"id": 5, "name": "キャンペーン", "is_default": 0, "position": 1, "count": 2}
  ]
}
```

#### Ghi chú
- Folder mặc định「未分類」luôn ở đầu danh sách với `id = 0`
- `count`: số Rich Menu trong folder (bảng `rich_menus` theo `group_id`)
- Folder lấy từ bảng `category` qua `Category::getListRichMenusCategories()`

---

### EP-06: POST `/ajax/folder/rich-menu/add`
**Mô tả**: Tạo mới hoặc sửa tên folder
**Controller**: `V2\RichMenuController@addRichMenuFolder` (dòng 185-224)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|-----------|-------|
| `name` | body | string | Có | `required\|string\|max:15` | Tên folder |
| `id` | body | int | Không | `nullable\|integer` | Nếu có → sửa tên; không → tạo mới |

#### Lỗi
| HTTP | Mô tả |
|------|-------|
| 200 | `{"status": false, "message": "フォルダ名を入力してください。"}` — tên trống |
| 200 | `{"status": false, "message": MESSAGE_NOTIFY_BACKUP}` — đang backup |

---

### EP-07: POST `/ajax/folder/rich-menu/sort`
**Mô tả**: Sắp xếp lại thứ tự folder
**Controller**: `V2\RichMenuController@sortListFolderData` (dòng 147-183)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|-----------|-------|
| `order` | body | array | Có | `required\|array` | Mảng IDs theo thứ tự mới |

---

### EP-08: POST `/ajax/rich-menu/quick-create`
**Mô tả**: Tạo nhanh Rich Menu từ modal (SCR-RCM-02)
**Controller**: `V2\RichMenuController@quickAddRichMenu` (dòng 302-358)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|-----------|-------|
| `rich_menu_name` | body | string | Có | `required\|string\|max:50` | Tên quản lý |
| `folder_id` | body | int | Có | `required\|integer` | ID folder |
| `is_top_folder` | body | bool | Không | `nullable\|boolean` | Thêm ở đầu folder (true) hoặc cuối (false) |
| `rich_menu_id` | body | int | Không | `nullable\|integer` | Nếu có → cập nhật tên/folder thay vì tạo mới |

#### Business logic
- Kiểm tra plan giới hạn: free plan chỉ được tạo tối đa 2 Rich Menu
- Kiểm tra trùng tên (duplicate name) trong cùng bot
- `title_menu` mặc định: `'◀︎ お問合せ／メニュー ▲'`
- Position tính dựa trên `is_top_folder`: true → max+1, false → min-1

#### Lỗi
| HTTP | Mô tả |
|------|-------|
| 200 | `{"status": false, "message": "現在のプランは利用できない機能です..."}` — free plan đã đạt giới hạn |
| 200 | `{"status": false, "message": "その管理名はすでに利用されています"}` — trùng tên |
| 200 | `{"status": false, "message": "管理名を入力してください"}` — tên trống |

---

### EP-09: POST `/ajax/rich-menu/upload-image`
**Mô tả**: Upload ảnh Rich Menu hoặc cập nhật template type
**Controller**: `V2\RichMenuController@saveRichMenuImageUpload` (dòng 762-825)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | body | int | Có | Rich Menu ID |
| `imageUrl` | body (file) | file | Có (nếu newImage) | File ảnh upload |
| `size` | body | JSON string | Có | `{"width": 2500, "height": 1686, "size": "large"}` |
| `newImage` | body | bool | Không | Có ảnh mới hay không |
| `update_template_type` | body | bool | Không | Nếu true → chỉ cập nhật template, không upload ảnh |
| `template_type` | body | int | Không | Loại template (1-9) |

#### Validation
- Kích thước ảnh: chỉ chấp nhận 2500x1686 hoặc 2500x843
- Dung lượng: tối đa 10MB
- Khi height = 843 → `template_type` tự động = 9
- Khi height = 1686 → `template_type` tự động = 1
- Upload ảnh → `step_active` = 2
- Cập nhật template → `step_active` = 3, xoá toàn bộ `rich_menu_items` cũ

---

### EP-10: POST `/basic/rich-menu/save`
**Mô tả**: Lưu Rich Menu mới (full data — tất cả steps)
**Controller**: `Basic\UserController@saveNewRichMenu` (dòng 742-941+)
**Mức tin cậy**: **Cao**

#### Request (multipart/form-data)
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `richMenuItems` | body | array/JSON | Có | Danh sách items (areas) với action config |
| `richMenuName` | body | string | Có | Tên quản lý |
| `titleMenu` | body | string | Không | Text hiển thị trên menu bar |
| `imageUrl` | body | file | Có (nếu model=image) | File ảnh |
| `size` | body | JSON string | Có | `{"width":2500,"height":1686,"size":"large"}` |
| `status` | body | int | Có | 0=ẩn, 1=hiện khi mở chat |
| `model` | body | string | Có | `"image"` |
| `timeDisplay` | body | int | Không | 0=không hẹn giờ, 1=có hẹn giờ |
| `startDate`, `startTime` | body | string | Không | Ngày/giờ bắt đầu hiển thị |
| `endDate`, `endTime` | body | string | Không | Ngày/giờ kết thúc hiển thị |
| `groupId` | body | int | Không | Folder ID |
| `chatBar` | body | string | Không | — |

#### Side effects
- Tạo record trong `rich_menus`
- Tạo records trong `rich_menu_items` cho từng area
- Tạo `actions` và `action_details` cho mỗi item có action
- **Gọi LINE API**: `POST https://api.line.me/v2/bot/richmenu` để tạo Rich Menu trên LINE
- **Upload ảnh lên LINE**: `POST https://api-data.line.me/v2/bot/richmenu/{richMenuId}/content`
- **Tạo/cập nhật alias**: `POST https://api.line.me/v2/bot/richmenu/alias`
- Cập nhật `rich_menu_id` (LINE Rich Menu ID) vào bảng `rich_menus`
- Ghi `richmenu_update_history` nếu là update

---

### EP-11: POST `/basic/rich-menu/update`
**Mô tả**: Cập nhật Rich Menu (full data — tất cả steps)
**Controller**: `Basic\UserController@updateRichMenu` (dòng 1172-1366)
**Mức tin cậy**: **Cao**

#### Request
Tương tự EP-10, thêm:
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | body | int | Có | Rich Menu ID cần cập nhật |
| `newImage` | body | int | Không | 0=không đổi ảnh, 1=ảnh mới |
| `template_type` | body | int | Không | Loại layout template |
| `is_top_folder` | body | bool | Không | — |

#### Side effects
- Cập nhật `rich_menus`
- Xoá `rich_menu_items` cũ không còn trong danh sách mới
- Xoá `detail_click_rich_menu` của items bị xoá
- **Gọi LINE API** tạo lại Rich Menu trên LINE (xoá cũ, tạo mới)
- Set `step_active = 4`

---

### EP-14: POST `/ajax/rich-menu/copy`
**Mô tả**: Sao chép Rich Menu
**Controller**: `V2\RichMenuController@copyRichMenu` (dòng 360-410)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|-----------|-------|
| `rich_menu_id` | body | int | Có | `required\|integer` | ID Rich Menu cần copy |
| `rich_menu_name` | body | string | Có | `required\|string\|max:50` | Tên cho bản copy |
| `folder_id` | body | int | Có | `required\|integer` | Folder đích |
| `is_top_folder` | body | bool | Không | `nullable\|boolean` | Vị trí trong folder |

#### Side effects
- Copy ảnh Rich Menu sang file mới
- Copy toàn bộ `rich_menu_items`, `actions`, `action_details`
- Clone `filter_v2` nếu action có filter
- Gọi LINE API tạo Rich Menu mới trên LINE
- `status_line = 0` (không tự động hiển thị bản copy)

---

### EP-15: POST `/ajax/rich-menu/delete`
**Mô tả**: Xoá Rich Menu (soft delete)
**Controller**: `V2\RichMenuController@deleteRichMenu` (dòng 412-448)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|-----------|-------|
| `rich_menu_ids` | body | array | Có | `required\|array` | Mảng IDs cần xoá |

#### Side effects
- Soft delete `rich_menus` và `rich_menu_items`
- Ghi `richmenu_update_history` với `is_updated = 5`
- Xoá `action_details` liên quan (type=richmenu, action=2)
- Xoá `richmenu_switch_item` tham chiếu đến Rich Menu bị xoá
- Xoá `detail_click_rich_menu` thống kê
- Xoá `setting_display_rich_menu_histories` lịch sử hiển thị

---

### EP-18: POST `/ajax/get-rich-menu/setting`
**Mô tả**: Lấy thông tin Rich Menu cho màn hiển thị/dừng
**Controller**: `V2\RichMenuController@ajaxGetRichMenuSetting` (dòng 607-644)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | body | int | Có | Rich Menu ID |

#### Response thành công (200)
```json
{
  "status": true,
  "data": {
    "id": 1,
    "name": "メインメニュー",
    "url_image": "...",
    "status_line": 0,
    "status_rich": 0,
    "count_line_user": 150
  },
  "allFriend": 500,
  "isAccessFilter": true
}
```
- `count_line_user`: đếm `bot_line_user` có `rich_menu_id` này và `is_blocked = 0`
- `allFriend`: tổng số bạn bè qua `Conversation::advanceFilterPost`
- `isAccessFilter`: quyền truy cập filter

---

### EP-19: POST `/ajax/rich-menu/save-setting-display`
**Mô tả**: Lưu cài đặt hiển thị Rich Menu cho bạn bè
**Controller**: `V2\RichMenuController@saveSettingDisplayRichmenu` (dòng 645-686)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | body | int | Có | Rich Menu ID |
| `idHistory` | body | int | Không | ID lịch sử (nếu sửa lịch đã đặt) |
| `type_filter` | body | int | Có | 0=tất cả, 1=chọn riêng |
| `filter_ids` | body | array | Không | Mảng filter IDs (khi type_filter=1) |
| `history` | body | object | Có | `{date, time, type, filter_id}` |

#### Side effects
- Cập nhật `rich_menus.status_link = 1`
- Tạo/cập nhật `setting_display_rich_menu_histories` với `action = SHOW (1)`, `status = WAITING (1)`
- Khi `history.type = 1` (ngay lập tức) → `date_setting = now()`
- Khi `history.type = 2` (đặt lịch) → `date_setting = date + time`
- **Background job sẽ xử lý**: Bản ghi history với status WAITING sẽ được job quét và thực thi khi đến thời gian

---

### EP-20: POST `/ajax/rich-menu/save-setting-stop`
**Mô tả**: Lưu cài đặt dừng Rich Menu
**Controller**: `V2\RichMenuController@saveSettingStopRichmenu` (dòng 687-730)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | body | int | Có | Rich Menu ID |
| `history` | body | object | Có | `{date, time, type}` |

#### Validation
- Không thể dừng Rich Menu đang là mặc định (`status_line = 1`)

#### Side effects
- Cập nhật `rich_menus.status_link = 2`, `is_updated = 2`
- Tạo `setting_display_rich_menu_histories` với `action = STOP (2)`

---

### EP-21: GET `/ajax/rich-menu/setting-display-history`
**Mô tả**: Lấy lịch sử hiển thị/dừng (phân trang, filter)
**Controller**: `V2\RichMenuController@settingDisplayHistories` (dòng 855-886)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `start_date` | query | string | Không | Lọc từ ngày |
| `end_date` | query | string | Không | Lọc đến ngày |
| `actions` | query | int/array | Không | Lọc theo action (1=show, 2=stop) |
| `status` | query | int/array | Không | Lọc theo status (1=waiting, 2=processing, 3=done) |
| `per_page` | query | int | Không | Số item/trang (mặc định 10) |
| `order` | query | object | Không | `{column, dir}` — column: `created_at` hoặc `date_setting` |

---

### EP-24: GET `/ajax/rich-menu/data-statistic/{richMenu}`
**Mô tả**: Thống kê số lần tap theo ngày và area
**Controller**: `V2\RichMenuController@dataStatistic` (dòng 450-490)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `richMenu` | URL path | int | Có | Rich Menu ID |
| `start_date` | query | string | Không | Mặc định: 16 ngày trước |
| `end_date` | query | string | Không | Mặc định: hôm nay |
| `page` | query | int | Không | Trang hiện tại |
| `per_page` | query | int | Không | Số item/trang (mặc định 10) |
| `order` | query | string | Không | `"day"` |
| `dir` | query | string | Không | `"ASC"` / `"DESC"` |
| `download_csv` | query | bool | Không | Nếu true → trả về file CSV (Shift_JIS) |

#### Response thành công (200)
```json
{
  "success": true,
  "data": { "...rich_menu data + rich_menu_items..." },
  "detailClick": [
    {"day": "2024-01-01", "data": [10, 5, 3]}
  ],
  "countTotal": [150, 80, 45],
  "pagination": {"total": 16, "from": 1, "to": 10, "last_page": 2, "per_page": 10, "current_page": 1}
}
```

---

### EP-26: GET `/ajax/rich-menu-remove`
**Mô tả**: Lấy danh sách Rich Menu đã xoá (soft deleted)
**Controller**: `V2\RichMenuController@initRichMenuRemoved` (dòng 495-522)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `per_page` | query | int | Không | Mặc định 5 |
| `dir` | query | string | Không | Sắp xếp `deleted_at`, mặc định `DESC` |

#### Response
- Danh sách Rich Menu đã soft delete, kèm `username_del` (ai đã xoá)
- `isAdd`: boolean — còn được phép tạo thêm Rich Menu không (free plan limit = 2)

---

### EP-27: POST `/ajax/rich-menu-restore`
**Mô tả**: Khôi phục Rich Menu đã xoá
**Controller**: `V2\RichMenuController@restoreRichmenuRemove` (dòng 535-606)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `richmenu_id` | body | int | Có | ID Rich Menu cần khôi phục |

#### Side effects
- Restore Rich Menu và items từ soft delete
- Kiểm tra trùng tên trước khi restore
- Restore folder nếu folder đã bị xoá (`is_deleted`)
- **Gọi LINE API** tạo lại Rich Menu trên LINE + upload ảnh + tạo alias

---

### EP-32: POST `/basic/rich-menu/set-rich-menu-all-user`
**Mô tả**: Đặt/gỡ Rich Menu làm mặc định cho tất cả bạn bè
**Controller**: `Basic\UserController@setRichMenuAllUser` (dòng 1943-2006)
**Mức tin cậy**: **Cao**

#### Request
| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | body | int | Có | Rich Menu ID (truyền rỗng → gỡ mặc định) |

#### Side effects
- Nếu `id` có giá trị:
  - Reset `status_line = 0` cho tất cả Rich Menu của bot
  - Set `status_line = 1, status_link = 1, is_updated = 3` cho Rich Menu chọn
  - Ghi `richmenu_update_history` với `is_updated = 3`
- Nếu `id` rỗng:
  - Gỡ Rich Menu mặc định hiện tại (`status_line = 0, status_link = 2, is_updated = 4`)
  - Ghi `richmenu_update_history` với `is_updated = 2`

---

## Bảng `richmenu_update_history` — Mã `is_updated`

| Giá trị | Ý nghĩa |
|---------|---------|
| 2 | Ẩn/dừng Rich Menu |
| 3 | Đặt làm mặc định |
| 4 | Gỡ mặc định |
| 5 | Xoá Rich Menu |

**Mức tin cậy**: **Cao** — đọc trực tiếp từ code

---

## Ghi chú về Background Jobs

Tính năng Rich Menu ghi dữ liệu vào bảng `richmenu_update_history` với `status = 0` (chờ xử lý). Bảng `setting_display_rich_menu_histories` có `status = WAITING (1)` → `PROCESSING (2)` → `DONE (3)`. Đây là dấu hiệu rõ ràng có **background job (Spring Boot)** quét và xử lý:
1. **Đồng bộ Rich Menu sang LINE**: Dựa trên `richmenu_update_history.status` — job đọc bản ghi status=0, thực hiện gọi LINE API (link/unlink Rich Menu cho user), rồi cập nhật status
2. **Đặt lịch hiển thị/dừng**: Dựa trên `setting_display_rich_menu_histories.status` — job quét bản ghi WAITING khi `date_setting` đến hạn, thực thi hiển thị/dừng, cập nhật status sang DONE

**→ Cần phân tích tiếp trong bước job-analyzer (bước 4)**
