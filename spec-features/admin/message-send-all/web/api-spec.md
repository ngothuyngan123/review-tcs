# API Spec — FA-008:「メッセージ配信」(Broadcast)

**Feature ID**: FA-008
**Portal**: Admin
**Ngày phân tích**: 2026-03-26
**Nguồn**: Laravel source code (`reverse-spec/src/web/sns-line/`)
**Controllers**: `BroadcastController` (2730 lines), `BroadcastV2Controller` (1054 lines)

---

## 1. Tổng quan Endpoints

### Page Routes (GET — trả về View)

| EP | Method | URL | Controller@Action | Mô tả | Middleware |
|----|--------|-----|-------------------|-------|------------|
| EP-01 | GET | `/basic/message-send-all` | `BroadcastController@index` | Danh sách broadcast (3 tabs) | web, auth, LogRequestMultipart |
| EP-02 | GET | `/basic/add-broadcast-v2` | `BroadcastV2Controller@addBroadcastV2` | Form tạo/chỉnh sửa broadcast (Bước 1 + 2) | web, auth, LogRequestMultipart |
| EP-03 | GET | `/basic/message-send-all/create/{id}` | `BroadcastController@create` | Form chỉnh sửa broadcast (legacy, Bước 2) | web, auth, LogRequestMultipart |
| EP-04 | GET | `/basic/message-send-all/copy/{id}` | `BroadcastController@createByCopy` | Form tạo broadcast từ bản sao | web, auth, LogRequestMultipart |
| EP-05 | GET | `/basic/message-send-all/use-templates/{id}` | `BroadcastController@createUsesTemplate` | Form tạo broadcast từ template | web, auth, LogRequestMultipart |
| EP-06 | GET | `/basic/message-send-all/broadcast-histories/{broadcast_id}` | `BroadcastController@broadcastHistories` | Xem lịch sử gửi broadcast | web, auth, LogRequestMultipart |
| EP-07 | GET | `/basic/message-send-all/pack-message/show/{broadcast_id}/{pack_id}` | `BroadcastController@showParkMessage` | Xem pack message trong broadcast | web, auth, LogRequestMultipart |

### AJAX Routes (POST/GET — trả về JSON)

| EP | Method | URL | Controller@Action | Mô tả | Route Name |
|----|--------|-----|-------------------|-------|------------|
| EP-10 | POST | `/ajax/save-broadcast-v2` | `BroadcastV2Controller@saveBroadcastV2` | Lưu broadcast (tạo/sửa/copy) | saveBroadcastV2 |
| EP-11 | POST | `/ajax/get-list-broadcast` | `BroadcastController@ajaxGetListBroadcastVer2` | Lấy danh sách broadcast theo tab | — |
| EP-12 | POST | `/ajax/get-detail-broadcast-v2` | `BroadcastV2Controller@getDetailBroadcastV2` | Lấy chi tiết 1 broadcast | getDetailBroadcastV2 |
| EP-13 | POST | `/ajax/get-data-preview-broadcast-v2` | `BroadcastV2Controller@getDataPreviewBroadcast` | Lấy dữ liệu preview broadcast | getDataPreviewBroadcast |
| EP-14 | GET | `/ajax/get-list-message-broadcast` | `BroadcastV2Controller@getListMessage` | Lấy danh sách messages trong broadcast | getListMessageBroadcast |
| EP-15 | POST | `/ajax/delete-multiple-broadcast` | `BroadcastV2Controller@deleteMutitpleBroadcast` | Xoá nhiều broadcast | deleteMultipleBroadcast |
| EP-16 | POST | `/ajax/copy-broadcast-v2` | `BroadcastV2Controller@copyBroadcastV2` | Sao chép broadcast | copyBroadcastV2 |
| EP-17 | POST | `/ajax/get-filter-number-broadcast` | `BroadcastController@getFilterNumber` | Tính lại số lượng người nhận | broadcast.getFilterNumber |
| EP-18 | POST | `/ajax/send-for-test-broadcast` | `BroadcastController@ajaxSendForTestBroadcast` | Gửi test broadcast (legacy) | broadcast.sendForTest |
| EP-19 | POST | `/ajax/send-for-test-broadcast-v3` | `BroadcastController@sendForTestBroadcastV3` | Gửi test broadcast (V3 — qua BroadcastService) | broadcast.sendForTestV3 |
| EP-20 | POST | `/ajax/init-create-broadcast` | `BroadcastController@ajaxInitCreateData` | Khởi tạo dữ liệu khi tạo broadcast | ajaxInitCreateData |
| EP-21 | POST | `/ajax/init-list-line-user-v2` | `BroadcastController@ajaxInitListLineUserData` | Tìm kiếm LINE users (cho test) | ajaxInitListLineUserData |
| EP-22 | POST | `/ajax/init-list-line-user-booking-v2` | `BroadcastController@ajaxInitListLineUserBooking` | Tìm kiếm LINE users booking | ajaxInitListLineUserBooking |
| EP-23 | POST | `/ajax/update-line-tester` | `BroadcastController@ajaxUpdateTesterLineData` | Cập nhật trạng thái tester | ajaxUpdateTesterLineData |
| EP-24 | POST | `/ajax/count-variable-send` | `BroadcastController@ajaxCountVariableSend` | Đếm số người nhận (legacy filter) | ajaxCountVariableSend |
| EP-25 | POST | `/ajax/broadcast/init-list-bots-profiles` | `BroadcastController@ajaxGetProfileOfBots` | Lấy danh sách profile người gửi | broadcast.ajaxGetProfileOfBots |
| EP-26 | POST | `/basic/broadcast/save-selected-profile-bot` | `BroadcastController@saveSelectedProfileBot` | Chọn profile người gửi | broadcast.saveSelectedProfileBot |
| EP-27 | POST | `/basic/broadcast/delete-set-profile-bot` | `BroadcastController@deleteProfilesBots` | Xoá profile người gửi | broadcast.deleteProfilesBots |
| EP-28 | POST | `/ajax/save-bot-profile-v2` | `BroadcastV2Controller@saveBotProfile` | Lưu profile người gửi (tạo/sửa) | saveBotProfileV2 |
| EP-29 | POST | `/ajax/sort-profile-v2` | `BroadcastV2Controller@sortProfileV2` | Sắp xếp thứ tự profiles | sortProfileV2 |
| EP-30 | POST | `/ajax/upload-file-bot-profile-broadcast` | `BroadcastV2Controller@uploadFile` | Upload avatar cho profile | broadcast.uploadFile |
| EP-31 | POST | `/basic/message-send-all/message-store` | `BroadcastController@messageStore` | Lưu message template (legacy) | broadcast.store |
| EP-32 | POST | `/basic/message-send-all/message-save` | `BroadcastController@updateMessage` | Cập nhật message template (legacy) | broadcast.updateMessage |
| EP-33 | POST | `/basic/message-send-all/store-broadcast` | `BroadcastController@storeBroadCast` | Lưu cài đặt broadcast (legacy: create/edit/copy) | broadcast.storeBroadcast |
| EP-34 | POST | `/ajax/broadcast/delete-message` | `BroadcastController@deleteMessage` | Xoá 1 message khỏi broadcast | broadcast.deleteMessage |
| EP-35 | POST | `/ajax/broadcast/create-message-by-template` | `BroadcastController@createMessageBytemplate` | Thêm message từ template vào broadcast | broadcast.createMessageByTemplate |
| EP-36 | POST | `/ajax/broadcast/clone-template-to-step-broadcast` | `BroadcastController@cloneStepBroadcastByTemplate` | Clone template thành step message | clone.template.to.step.broadcast |
| EP-37 | POST | `/ajax/remove-item-message-broadcast-v2` | `BroadcastV2Controller@removeItemMessageBroadcastV2` | Xoá message khỏi broadcast (V2) | saveBotProfileV2 |
| EP-38 | POST | `/ajax/save-action-broadcast` | `BroadcastV2Controller@saveActionBroadcastV2` | Xoá action khỏi broadcast | saveActionBroadcastV2 |
| EP-39 | POST | `/ajax/delete-action-detail-broadcast` | `BroadcastV2Controller@deleteItemAction` | Xoá 1 action detail khỏi broadcast | broadcast.deleteItemAction |
| EP-40 | GET | `/ajax/initDataFilterBroadcast` | `FriendlistController@initDataFilterBroadcast` | Khởi tạo dữ liệu filter cho broadcast | initDataFilterBroadcast |

---

## 2. Chi tiết Endpoints chính

### EP-01: GET `/basic/message-send-all` — Danh sách broadcast

**Controller**: `BroadcastController@index` (line 78-106)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `type` | query | string | Không | Tab hiển thị mặc định |

**Response**: HTML View `basic.broadcast.index_v2`

**Dữ liệu truyền vào view**:
- `scenario` — danh sách Scenario của bot
- `conversion` — danh sách Conversion của bot
- `statusObject` — danh sách StatusChat của bot
- `richMenus` — danh sách RichMenus (status_rich=1)
- `typeTab` — tab hiện tại

**Liên kết UI**: SCR-BC-01

---

### EP-02: GET `/basic/add-broadcast-v2` — Form tạo/chỉnh sửa broadcast

**Controller**: `BroadcastV2Controller@addBroadcastV2` (line 123-152)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `broadcast_id` | query | integer | Không | ID broadcast cần chỉnh sửa. Nếu không có → tạo mới |

**Logic**:
1. Nếu `broadcast_id` có giá trị → tìm broadcast thuộc bot hiện tại
2. Nếu không tìm thấy → redirect về `/basic/message-send-all`
3. Đếm tổng số `BotLineUser` (is_blocked=0) → truyền vào view làm `totalUser`

**Response**: HTML View `basic.broadcast.v2.edit-broadcast`

**Liên kết UI**: SCR-BC-02 (tạo mới), SCR-BC-04 (chỉnh sửa khi có broadcast_id)

---

### EP-10: POST `/ajax/save-broadcast-v2` — Lưu broadcast (CORE)

**Controller**: `BroadcastV2Controller@saveBroadcastV2` (line 154-417)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `broadcast_id` | body | integer | Không | ID broadcast (null = tạo mới) |
| `type` | body | string | Không | `'copy'` nếu sao chép |
| `name` | body | string | Có | Tiêu đề quản lý (管理用タイトル) |
| `status` | body | string | Có | `'draft'`, `'wait_to_send'` |
| `send_day` | body | string | Có | Ngày gửi (YYYY-MM-DD) |
| `send_time` | body | string | Có | Giờ gửi (HH:mm:ss) |
| `setting_send_message` | body | integer | Có | 0 = gửi ngay, 1 = đặt lịch |
| `profile_id` | body | integer | Không | ID profile người gửi |
| `action_id` | body | integer | Không | ID action (エルメアクション) |
| `arr_template_ids` | body | array | Không | Mảng template IDs cho messages |
| `count_filter` | body | integer | Không | Số lượng người nhận |
| `flag_setting_filter` | body | integer | Không | 0 = không filter, 1 = có filter |
| `filter_ids` | body | array | Không | Mảng filter IDs |
| `delivery_dates` | body | array | Không | Mảng ngày gửi bổ sung `[{send_day, send_time, id?}]` |

**Request mẫu**:
```json
{
  "broadcast_id": null,
  "name": "テスト配信",
  "status": "wait_to_send",
  "send_day": "2026-04-01",
  "send_time": "10:00:00",
  "setting_send_message": 1,
  "profile_id": 123,
  "action_id": null,
  "arr_template_ids": [456, 789],
  "count_filter": 150,
  "flag_setting_filter": 1,
  "filter_ids": [10, 11],
  "delivery_dates": [
    {"send_day": "2026-04-02", "send_time": "10:00:00"},
    {"send_day": "2026-04-03", "send_time": "10:00:00"}
  ]
}
```

**Logic chính**:
1. **Nếu `type == 'copy'`**: gọi `saveCopyBroadCastV2New()` → clone broadcast + templates + filters + children
2. **Validation**: `name` bắt buộc, `send_day` không rỗng/`0000:00:00`
3. **Profile**: nếu profile là default → set `profile_id = null`
4. **Tạo mới** (không có `broadcast_id`): tạo broadcast với `status = 'draft'`
5. **Cập nhật** (có `broadcast_id`):
   - Kiểm tra 5 phút rule: nếu < 5 phút trước giờ gửi → lỗi
   - Cập nhật fields, giữ nguyên status trừ khi `status == 'draft'`
   - Nếu `status == 'wait_to_send'` và có template/action → set `status = 'wait_to_send'`
6. **Delivery dates** (multi-schedule): tạo/cập nhật broadcast children với `parent_id`
   - Clone templates cho mỗi child
   - Clone actions cho mỗi child
   - Xoá children cũ không còn trong danh sách
7. **Filters**: copy filters từ parent sang children mới
8. **Tutorial**: cập nhật `bots_tutorial.status_send_all = 1`

**Response thành công**:
```json
{
  "status": true,
  "broadcastIdNew": 123
}
```

**Lỗi có thể xảy ra**:

| HTTP | Mô tả | Message |
|------|-------|---------|
| 200 | Thiếu tên | `管理用タイトルを入力してください` |
| 200 | Thiếu ngày gửi | `配信予定日時を入力してください` |
| 200 | < 5 phút trước gửi | `配信予定日時5分前からは配信内容の編集はできません。` |
| 500 | Server error | Exception message |

**Liên kết UI**: SCR-BC-02, SCR-BC-04

---

### EP-11: POST `/ajax/get-list-broadcast` — Lấy danh sách broadcast

**Controller**: `BroadcastController@ajaxGetListBroadcastVer2` (line 1286-1474)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `status` | body | string | Có | `'wait_to_send'`, `'draft'`, `'delivered'` |
| `action` | body | string | Không | `'delete'` → xoá broadcast trước khi lấy list |
| `broadcast_id` | body | integer | Không | ID broadcast cần xoá (khi action=delete) |
| `per_page` | body | integer | Không | Số items/trang |
| `order_by` | body | string | Không | Cột sort: `'send_datetime'`, `'created_at'`... |
| `sort_by` | body | string | Không | `'ASC'` hoặc `'DESC'` |
| `filter_month` | body | string | Không | `'YYYY-MM'` — lọc theo tháng (tab wait_to_send) |
| `filter_date_from` | body | string | Không | Ngày bắt đầu (tab delivered) |
| `filter_date_to` | body | string | Không | Ngày kết thúc (tab delivered) |
| `all_data` | body | boolean | Không | true = không lọc theo khoảng thời gian |

**Logic chính**:
1. **Xoá** (nếu `action == 'delete'`):
   - Kiểm tra 5 phút rule
   - Xoá templates liên quan (category_id = `-11` = broadcast category)
   - Xoá broadcast record
2. **Query**: lọc theo `status`:
   - `wait_to_send` → `status IN ('wait_to_send')`, lọc thêm theo `filter_month`
   - `delivered` → `status IN ('delivered', 'send_false')`, lọc theo `filter_date_from/to`
   - `draft` → `status IN ('draft', 'unregistered', 'not_delivery')`
3. **Sort**: mặc định `send_day DESC, send_time DESC, id DESC`
4. **Mỗi item**: bổ sung `delivery_dates` (children), `checkFilter`, `text_filter`, `profileBot`

**Response thành công**:
```json
{
  "status": true,
  "data": {
    "action": "init",
    "broadcast": [ /* paginated broadcast items */ ],
    "status": "wait_to_send",
    "total_page": 5,
    "next_page": 2,
    "current_page": 1
  }
}
```

**Liên kết UI**: SCR-BC-01 (3 tabs)

---

### EP-12: POST `/ajax/get-detail-broadcast-v2` — Chi tiết broadcast

**Controller**: `BroadcastV2Controller@getDetailBroadcastV2` (line 520-669)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `broadcast_id` | body | integer | Có | ID broadcast |

**Logic**:
1. Tìm broadcast theo `id` và `bot_id`
2. Kiểm tra `check_can_edit`: false nếu < 5 phút trước giờ gửi và status = `wait_to_send`
3. Lấy action details nếu có `action_id`
4. Lấy `delivery_dates` (children broadcasts)
5. Lấy filters (AND/OR) từ `filters_v2`
6. Lấy profile người gửi (hoặc default)
7. Lấy danh sách messages (templates) với buttons, item_records

**Response thành công**:
```json
{
  "status": true,
  "broadcast": {
    "id": 123,
    "name": "テスト配信",
    "status": "wait_to_send",
    "send_day": "2026-04-01",
    "send_time": "10:00",
    "check_can_edit": true,
    "delivery_dates": [...],
    "detail_action": [...],
    "checkFilter": 1,
    "filter_ids": [10, 11],
    "list_preview_filter": ["タグ: VIP"],
    "destination": "タグ: VIP",
    "profile_bot": {...},
    "arr_template_ids": [456, 789]
  },
  "messages": [...]
}
```

**Liên kết UI**: SCR-BC-04

---

### EP-15: POST `/ajax/delete-multiple-broadcast` — Xoá hàng loạt

**Controller**: `BroadcastV2Controller@deleteMutitpleBroadcast` (line 706-748)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `ids_delete` | body | array | Có | Mảng broadcast IDs |
| `status` | body | string | Có | Status tab hiện tại |

**Logic**:
1. Nếu `status == 'wait_to_send'`: kiểm tra 5 phút rule cho từng broadcast
2. Xoá templates liên quan (category_id = broadcast category)
3. Xoá broadcast records

**Response thành công**: `{ "status": true }`

**Lỗi**: `{ "status": false, "msg": "配信予定日時5分前からは配信内容の編集はできません。" }`

**Liên kết UI**: SCR-BC-01 (nút「一括削除」)

---

### EP-16: POST `/ajax/copy-broadcast-v2` — Sao chép broadcast

**Controller**: `BroadcastV2Controller@copyBroadcastV2` (line 860-964)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `broadcast_id` | body | integer | Có | ID broadcast gốc |

**Logic**:
1. Clone templates (giữ nguyên template có category_id >= 0, clone riêng templates category < 0)
2. Clone actions (nếu có)
3. Tạo broadcast mới với `status = 'draft'`
4. Clone filters
5. Clone children broadcasts

**Response thành công**: `{ "status": true, "broadcastId": 456 }`

---

### EP-17: POST `/ajax/get-filter-number-broadcast` — Tính lại số người nhận

**Controller**: `BroadcastController@getFilterNumber` (line 2511-2555)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `broadcast_id` | body | integer | Có | ID broadcast |

**Logic**:
1. Lấy filters AND/OR từ `filters_v2` (parent_type = 'broadcast')
2. Gọi `Conversation::advanceFilterPost()` → đếm `bot_line_user.id` distinct
3. Cập nhật `broadcast.filter_number` và `broadcast.filter_date`
4. Cũng cập nhật cho broadcast children (cùng `parent_id`)

**Response thành công**:
```json
{
  "success": true,
  "filterNumber": 150,
  "filterDate": "2026-03-26 10:30:00"
}
```

**Liên kết UI**: SCR-BC-02/04 (nút「再計算」)

---

### EP-18: POST `/ajax/send-for-test-broadcast` — Gửi test (legacy)

**Controller**: `BroadcastController@ajaxSendForTestBroadcast` (line 2187-2325)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `broadcastId` | body | integer | Có | ID broadcast |
| `tester_ids` | body | array | Có | Mảng LINE user IDs (testers) |
| `actionId` | body | integer | Không | Action ID để thực thi khi gửi |

**Logic**:
1. Với mỗi tester → lấy templates → build messages → gọi `createMultipleMessage()` (LINE API)
2. Giới hạn 5 messages/batch (LINE API limit)
3. Gửi xong → cập nhật `free_send_count`, `updateMessageSendCount`
4. Nếu có `actionId` → gọi `sendAction()` cho mỗi tester

**Response thành công**: `{ "success": true, "msg": "テストアカウントへ送信しました" }`

**Liên kết UI**: SCR-BC-04 (nút「プレビューとテスト」)

---

### EP-19: POST `/ajax/send-for-test-broadcast-v3` — Gửi test (V3)

**Controller**: `BroadcastController@sendForTestBroadcastV3` → `BroadcastService@sendTestBroadcast`

**Request Params**: giống EP-18

**Logic**: tương tự EP-18 nhưng sử dụng:
- `TemplateService::mergeListTemplate()` thay vì loop thủ công
- `MessageService::createMessageTypeV2()` thay vì `createMultipleMessage()`
- Ghi `msg_kind = KIND_MESSAGE_SEND_TEST`, `type = TYPE_MESSAGE_BROADCAST`

---

### EP-25: POST `/ajax/broadcast/init-list-bots-profiles` — Danh sách profile người gửi

**Controller**: `BroadcastController@ajaxGetProfileOfBots` (line 2388-2458)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `profile_id` | body | integer | Không | Profile đang chọn |

**Logic**:
1. Lấy profile hiện tại (hoặc tạo default nếu chưa có)
2. Lấy profiles của Admin (sorted by is_default DESC, position ASC)
3. Lấy profiles của Staff (is_default = 0)
4. Default profile → avatar = `bot.bot_image`

**Response thành công**:
```json
{
  "success": true,
  "data": [
    { "id": 1, "nick_name": "Bot Name", "avt_path": "/img/...", "is_default": 1, "position": 1 }
  ],
  "profiles_selected": { "id": 1, "nick_name": "Bot Name", "avt_path": "/img/..." }
}
```

**Liên kết UI**: SCR-BC-02/04 (「送信者名」→ nút「設定」)

---

### EP-26: POST `/basic/broadcast/save-selected-profile-bot` — Chọn profile người gửi

**Controller**: `BroadcastController@saveSelectedProfileBot` (line 2460-2476)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id_profile_bot` | body | integer | Có | ID profile được chọn |
| `broadcast_id` | body | integer | Có | ID broadcast |

**Logic**:
- Nếu profile là default → set `broadcast.profile_id = null` (sẽ dùng default)
- Nếu không phải default → set `broadcast.profile_id = id_profile_bot`

**Response**: `{ "success": true, "data": { /* profile */ } }`

---

### EP-28: POST `/ajax/save-bot-profile-v2` — Lưu profile người gửi

**Controller**: `BroadcastV2Controller@saveBotProfile` (line 42-99)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `botProfile.id` | body | integer | Không | ID profile (null = tạo mới) |
| `botProfile.nick_name` | body | string | Có | Tên hiển thị |
| `botProfile.avt_path` | body | string | Không | Đường dẫn avatar |

**Logic**:
- Tạo mới: insert với `user_id = Auth::user()->id`, `bot_id = getBotId()`
- Cập nhật: update theo `id`

**Response**: `{ "status": true, "botProfileNew": { /* profile */ } }`

---

### EP-34: POST `/ajax/broadcast/delete-message` — Xoá message khỏi broadcast

**Controller**: `BroadcastController@deleteMessage` (line 2142-2167)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `broadcast_id` | body | integer | Có | ID broadcast |
| `template_id` | body | integer | Có | ID template cần xoá |

**Logic**:
1. Kiểm tra broadcast chưa delivered/delivering
2. Xoá template_id khỏi `template_ids` (comma-separated)
3. Nếu không còn template → set `status = 'unregistered'`

---

### EP-37: POST `/ajax/remove-item-message-broadcast-v2` — Xoá message (V2)

**Controller**: `BroadcastV2Controller@removeItemMessageBroadcastV2` (line 1007-1034)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `broadcastId` | body | integer | Có | ID broadcast |
| `arr_template_ids` | body | array | Có | Mảng template IDs còn lại |

**Logic**:
1. Kiểm tra 5 phút rule
2. Cập nhật `broadcast.template_ids` = implode(arr_template_ids)

---

### EP-38: POST `/ajax/save-action-broadcast` — Xoá action khỏi broadcast

**Controller**: `BroadcastV2Controller@saveActionBroadcastV2` (line 1036-1053)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | body | integer | Có | ID broadcast |

**Logic**: Set `action_id = null` cho broadcast và tất cả children

---

### EP-39: POST `/ajax/delete-action-detail-broadcast` — Xoá 1 action detail

**Controller**: `BroadcastV2Controller@deleteItemAction` (line 966-1005)

**Request Params**:

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `action_id` | body | integer | Có | Action ID |
| `action_detail_id` | body | integer | Có | Action Detail ID |
| `broadcast_id` | body | integer | Có | Broadcast ID |

**Logic**:
1. Kiểm tra 5 phút rule
2. Xoá filter liên quan (parent_type='modal_action')
3. Xoá ActionDetail
4. Nếu không còn detail → set `broadcast.action_id = null`

---

## 3. Middleware

Tất cả routes sử dụng middleware chung:

| Middleware | Mô tả |
|-----------|-------|
| `web` | Session, CSRF, cookies |
| `NotifyChatworkRequestTimeSlow` | Log request chậm vào Chatwork |
| `LogRequestMultipart` | Log multipart request |

**Lưu ý**: Không có middleware access control riêng cho broadcast routes. Xác thực dựa trên session (Auth::user) và `getBotId()` (từ session).

---

## 4. Mapping Endpoint ↔ Màn hình UI

| Screen | Endpoints sử dụng |
|--------|-------------------|
| SCR-BC-01 (Danh sách) | EP-01, EP-11, EP-15, EP-16 |
| SCR-BC-02 (Tạo mới — Bước 1) | EP-02, EP-10, EP-20, EP-25, EP-40 |
| SCR-BC-03 (Filter dialog) | EP-40, EP-17 |
| SCR-BC-04 (Chỉnh sửa — Bước 2) | EP-02, EP-10, EP-12, EP-13, EP-14, EP-17, EP-18/19, EP-25, EP-26, EP-34/37, EP-38, EP-39 |
| SCR-BC-05 (Message editor) | EP-31, EP-32 (legacy) hoặc qua template-v2 routes |

---

## 5. Ghi chú quan trọng

### Hai phiên bản code song song
- **Legacy** (BroadcastController): `storeBroadCast`, `messageStore`, `updateMessage`, `ajaxSendForTestBroadcast` — sử dụng trực tiếp `createMultipleMessage()`, template_id/template_id_2/template_id_3
- **V2** (BroadcastV2Controller): `saveBroadcastV2`, `sendForTestBroadcastV3` — sử dụng `template_ids` (comma-separated), `BroadcastService`, `MessageService`
- UI hiện tại (SCR-BC-02/04) sử dụng V2 endpoints

### Background Job trigger
- Khi broadcast được lưu với `status = 'wait_to_send'` và `setting_send_message = 1`, Background Job (Spring Boot) sẽ poll bảng `broadcast` để tìm record cần gửi
- KHÔNG có explicit job dispatch trong Laravel code — dùng Database Polling Model
- Xem chi tiết tại `job/job-spec.md`

### Broadcast statuses (state machine)

```
draft/unregistered → (add templates) → not_delivery → (set schedule) → wait_to_send
                                                                            ↓
                                                                       delivering → delivered
                                                                            ↓
                                                                       send_false (lỗi gửi)
```

| Status | Ý nghĩa | Editable |
|--------|---------|----------|
| `draft` | Bản nháp (V2) | Có |
| `unregistered` | Chưa có message (legacy) | Có |
| `not_delivery` | Có message nhưng chưa đặt lịch (legacy) | Có |
| `wait_to_send` | Đã đặt lịch, chờ gửi | Có (trừ < 5 phút trước giờ gửi) |
| `delivering` | Đang gửi | Không |
| `delivered` | Đã gửi | Không |
| `send_false` | Gửi thất bại | Không |
