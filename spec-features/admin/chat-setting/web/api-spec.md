# API Spec — FA-041 Cài đặt chat 「チャット設定」

> Trích xuất từ `routes/web.php` và `app/Http/Controllers/ChatController.php`, `app/Http/Controllers/Basic/BasicController.php` của Laravel `src/web/sns-line/`.

## Bối cảnh middleware

| Route | Group | Middleware áp dụng |
|-------|-------|--------------------|
| `GET /basic/chat-setting` | `web.php:823` → prefix `basic` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` |
| `GET|POST /ajax/*` | `web.php:2324` → prefix `ajax` | `check_login`, `check_remember_token` |

Toàn bộ route đều yêu cầu đã đăng nhập (session). Các route AJAX kiểm tra CSRF token qua header `X-CSRF-TOKEN` (xem `public/js/chat_setting/index.js:4`). Không có bước authorization kiểm tra Staff permission trong controller; việc lọc theo `bot_id` được thực hiện bằng helper `getBotId()` lấy từ session.

## Danh sách Endpoints

| # | Method | URL | Controller@Method | Middleware | Màn hình |
|---|--------|-----|-------------------|-----------|----------|
| EP-01 | GET | `/basic/chat-setting` | `Basic\BasicController@chatSetting` | basic_access, https_protocol, is_expire, check_remember_token | SCR-CST-01..07 (render view) |
| EP-02 | GET | `/ajax/initial/get-data-setting` | `ChatController@getDataSettingChat` | check_login, check_remember_token | Tab 2, 3, 4, 5 (load flags) |
| EP-03 | POST | `/ajax/save-data-setting` | `ChatController@saveSettingChat` | check_login, check_remember_token | Tab 2, 3, 4, 5 (save flags) |
| EP-04 | GET | `/ajax/init-status-chat-v2` | `ChatController@ajaxGetStatusChatV2` | check_login, check_remember_token | SCR-CST-01 (list status có phân trang) |
| EP-05 | POST | `/ajax/init-status-chat` | `ChatController@ajaxGetStatusChat` | check_login, check_remember_token | SCR-CST-01 (list đầy đủ — legacy) |
| EP-06 | POST | `/ajax/save-item-status-v2` | `ChatController@ajaxSaveItemStatusV2` | check_login, check_remember_token | SCR-CST-02 (lưu toàn bộ list sau add/edit/sort) |
| EP-07 | POST | `/ajax/save-item-status` | `ChatController@ajaxSaveItemStatus` | check_login, check_remember_token | SCR-CST-02 (legacy — lưu 1 item) |
| EP-08 | POST | `/ajax/save-all-status` | `ChatController@ajaxSaveAllStatus` | check_login, check_remember_token | SCR-CST-02 (legacy — lưu all, có validate) |
| EP-09 | POST | `/ajax/sort-status-chat` | `ChatController@ajaxSortStatusChat` | check_login, check_remember_token | SCR-CST-01 (drag-drop sort — legacy) |
| EP-10 | POST | `/ajax/delete-item-status` | `ChatController@ajaxDeleteItemStatus` | check_login, check_remember_token | SCR-CST-01 (xoá status) |

> Theo JS `setting_color.js` và `index.js`, UI hiện tại chỉ thực sự gọi: **EP-02, EP-03, EP-04, EP-06, EP-10**. Các endpoint EP-05, EP-07, EP-08, EP-09 tồn tại nhưng dùng ở view cũ (`chat_basic.blade.php`) — giữ lại để tài liệu đầy đủ.

---

## EP-01 · GET `/basic/chat-setting`

**Mục đích**: Render trang Blade `basic.chat_setting` (gồm 6 tab).

**Controller**: `Basic\BasicController::chatSetting()` (file `src/web/sns-line/app/Http/Controllers/Basic/BasicController.php:2710-2713`)

```php
public function chatSetting()
{
    return view('basic.chat_setting');
}
```

- **Request**: không tham số.
- **Response**: HTML view.
- **Lỗi**: 302 redirect đến `login` nếu thiếu session (qua `basic_access` middleware); 302 đến trang báo hết hạn nếu `is_expire` trigger.

**Liên kết màn hình**: SCR-CST-01 (mặc định tab 1), SCR-CST-02, SCR-CST-03, SCR-CST-04, SCR-CST-05, SCR-CST-06, SCR-CST-07 — tất cả các tab trên cùng 1 trang SPA Vue.

---

## EP-02 · GET `/ajax/initial/get-data-setting`

**Mục đích**: Load giá trị hiện tại cho tab 2 (auto-confirm), tab 3 (shortcut), tab 4 (shorten URL), tab 5 (preview).

**Controller**: `ChatController::getDataSettingChat()` (file `src/web/sns-line/app/Http/Controllers/ChatController.php:3930-3948`)

- **Request params**: không có.
- **Auth scope**: `bot_id` hiện tại lấy từ session qua `getBotId()`.
- **Logic**: `SELECT * FROM bots WHERE id = :botId`, nếu không tìm thấy → redirect `route('adminIndex')`.

**Response mẫu (200 OK)**:
```json
{
  "success": true,
  "data_setting": {
    "confirm_message_button": 0,
    "confirm_message_autoreply": 0,
    "confirm_message_autoreply_all": 0,
    "confirm_message_autoreply_specified": 0,
    "confirm_message_stamp": 0,
    "setting_shortcut": 0,
    "is_shorten_url": 1,
    "confirm_message_user_send": 1,
    "confirm_message_user_block_bot": 0,
    "preview_after_send": 1
  }
}
```

**Mapping field → UI tab**:
| Field | Tab | Ghi chú |
|-------|-----|---------|
| `confirm_message_button` | Tab 2 — checkbox 「【〇〇】メッセージ」 | Tin nhắn dạng button/marker |
| `confirm_message_stamp` | Tab 2 — checkbox「スタンプ」 | |
| `confirm_message_autoreply_all` | Tab 2 — checkbox「[すべてのメッセージに反応] のメッセージ」 | Trigger FA-003 all-reply |
| `confirm_message_autoreply_specified` | Tab 2 — checkbox「[設定したキーワードに反応] のメッセージ」 | Trigger FA-003 keyword |
| `confirm_message_autoreply` | (ẩn — comment out trong view mới) | Cờ cũ |
| `confirm_message_user_send` | Tab 2 — toggle「返信時の自動確認済み変更」 | |
| `confirm_message_user_block_bot` | Tab 2 — toggle「ブロックされた友だちの自動確認済み変更」 | |
| `setting_shortcut` | Tab 3 — radio | `0`: Shift+Enter gửi; `1`: Enter gửi |
| `is_shorten_url` | Tab 4 — toggle | |
| `preview_after_send` | Tab 5 — toggle | |

**Lỗi có thể**:
| HTTP | Kịch bản | Response |
|------|----------|----------|
| 302 | Session hết hạn | Redirect `/login` (middleware) |
| 302 | `bot_id` session không tồn tại trong DB | Redirect `adminIndex` |
| 500 | Exception không bắt | Laravel trả HTML error page |

---

## EP-03 · POST `/ajax/save-data-setting`

**Mục đích**: Lưu các flag của tab 2-5.

**Controller**: `ChatController::saveSettingChat(Request $request)` (file `src/web/sns-line/app/Http/Controllers/ChatController.php:3950-3961`)

**Request body** (form-urlencoded hoặc JSON — client dùng jQuery `$.ajax` mặc định form-urlencoded). JS chia 4 loại `type` khi gửi nhưng backend KHÔNG đọc `type` — dùng `$request->all()` trực tiếp:

- **type=1** (Tab 2 auto-confirm):
```json
{
  "confirm_message_button": 0,
  "confirm_message_stamp": 1,
  "confirm_message_autoreply": 0,
  "confirm_message_autoreply_all": 1,
  "confirm_message_autoreply_specified": 0,
  "confirm_message_user_send": 1,
  "confirm_message_user_block_bot": 0
}
```
- **type=2** (Tab 3 shortcut):
```json
{ "setting_shortcut": 1 }
```
- **type=3** (Tab 4 shorten URL):
```json
{ "is_shorten_url": 1 }
```
- **type=4** (Tab 5 preview):
```json
{ "preview_after_send": 0 }
```

**Logic (code thực tế — chú ý)**:
```php
public function saveSettingChat(Request $request){
    addLogUserAction("saveSettingChat");
    $botId = getBotId();
    Bots::where('id', $botId)->update($request->all());   // ⚠ mass assignment
    return response()->json(['success' => true, 'message' => '']);
}
```

**Response thành công (200 OK)**:
```json
{ "success": true, "message": "" }
```

**Validation / Form Request**: **KHÔNG CÓ**. Không có FormRequest class, không có `$request->validate()`, không có whitelist field. Toàn bộ input được truyền thẳng vào `update()`.

**⚠ Vấn đề bảo mật lớn (mass assignment)**:
- Model `App\Bots` khai báo `protected $guarded = [];` (file `src/web/sns-line/app/Bots.php:15`) → không bảo vệ field nào.
- Kết hợp `Bots::where('id', $botId)->update($request->all())` → client có thể gửi bất kỳ cột nào trong bảng `bots` (vd `admin_id`, `plan_type`, `free_send_count`, `is_active`, `is_shorten_url` ở các bảng khác) và được ghi đè.
- Cần flag đỏ cho `spec-validator` và báo cáo security.

**Lỗi có thể**:
| HTTP | Kịch bản | Response |
|------|----------|----------|
| 200 | Thành công | `{success: true, message: ""}` |
| 419 | CSRF token sai | Laravel response CSRF mismatch |
| 302 | Chưa đăng nhập | Redirect login |
| 500 | DB exception | Laravel trả error (code không có try/catch) |

**Liên kết màn hình**: SCR-CST-03, SCR-CST-04, SCR-CST-05, SCR-CST-06 (tab 2-5).

---

## EP-04 · GET `/ajax/init-status-chat-v2`

**Mục đích**: Lấy danh sách response status (tab 1) — hỗ trợ phân trang; cũng dùng để load full list phục vụ sort modal.

**Controller**: `ChatController::ajaxGetStatusChatV2(Request $request)` (file `src/web/sns-line/app/Http/Controllers/ChatController.php:624-638`)

**Request query params**:
| Tên | Vị trí | Kiểu | Bắt buộc | Mặc định | Ghi chú |
|-----|--------|------|---------|----------|---------|
| `page` | query | int | Không | 1 | Laravel pagination |
| `per_page` | query | int | Không | 100 | Khi UI gọi cho sort modal: không truyền → lấy 100; khi gọi cho phân trang: truyền `per_page` (UI spec nói mặc định 10) |

**Logic**:
```php
$current_bot_id = getBotId();
$statusObject = StatusChat::query()
    ->where('bot_id', $current_bot_id)
    ->orderBy('position', 'asc')
    ->orderBy('id', 'desc')
    ->paginate($request->per_page ?? 100);
```

**Response thành công (200 OK)**:
```json
{
  "success": true,
  "data": {
    "status": {
      "current_page": 1,
      "data": [
        {
          "id": 101,
          "bot_id": 42,
          "position": 1,
          "name_status": "見込みあり",
          "color": "#F44336",
          "bg_status": "#FDEBE9",
          "bg_choose": "#F44336",
          "is_save": 1,
          "count": 0,
          "created_at": "...",
          "updated_at": "..."
        }
      ],
      "first_page_url": "...",
      "from": 1,
      "last_page": 1,
      "last_page_url": "...",
      "next_page_url": null,
      "path": "...",
      "per_page": 10,
      "prev_page_url": null,
      "to": 5,
      "total": 5
    },
    "hasMorePage": false
  }
}
```

**Lỗi có thể**:
| HTTP | Kịch bản | Response |
|------|----------|----------|
| 200 | Exception bất kỳ | `{success: false, msg: "get ajaxGetStatusChat fail"}` (code log `Log::error($e)` rồi trả fail status HTTP 200) |

**Liên kết màn hình**: SCR-CST-01.

---

## EP-05 · POST `/ajax/init-status-chat`

**Mục đích**: Legacy — lấy toàn bộ status không phân trang.

**Controller**: `ChatController::ajaxGetStatusChat(Request $request)` (file `src/web/sns-line/app/Http/Controllers/ChatController.php:612-622`)

- **Request**: không tham số.
- **Logic**: `StatusChat::where('bot_id', $current_bot_id)->orderBy('position','asc')->orderBy('id','desc')->get()`
- **Response**: `{success: true, data: [...array of StatusChat...]}`
- **Dùng ở**: view `chat_basic.blade.php` (FA-001 1:1 Chat) để load dropdown status.

---

## EP-06 · POST `/ajax/save-item-status-v2`

**Mục đích**: Lưu toàn bộ list status (hiện dùng cho mọi thao tác: add, edit, sort — client gửi cả mảng mỗi lần).

**Controller**: `ChatController::ajaxSaveItemStatusV2(Request $request)` (file `src/web/sns-line/app/Http/Controllers/ChatController.php:691-723`)

**Request body**:
```json
{
  "data": [
    {
      "id": 101,
      "name_status": "見込みあり",
      "color": "#F44336",
      "bg_status": "#FDEBE9",
      "bg_choose": "#F44336"
    },
    {
      "id": null,
      "name_status": "新しい",
      "color": "#4CAF50",
      "bg_status": "#E8F5E9",
      "bg_choose": "#4CAF50"
    }
  ]
}
```

Fields mỗi item:
| Tên | Kiểu | Bắt buộc | Validation server | Ghi chú |
|-----|------|---------|-------------------|---------|
| `id` | int|null | Không | — | Nếu có → update; nếu null → create |
| `name_status` | string | Có (client validate ≤20 ký tự) | **KHÔNG** | UI counter 0/20 |
| `color` | string | Có (client) | **KHÔNG** | Hex color chính |
| `bg_status` | string | Có (client) | **KHÔNG** | Màu nền chip |
| `bg_choose` | string | Có (client) | **KHÔNG** | Màu nền khi chọn |

**Logic (quan trọng)**:
```php
foreach ($request->input('data') as $key => $colorItem) {
    $settings = [
        'bot_id' => $current_bot_id,
        'name_status' => $colorItem['name_status'],
        'color' => $colorItem['color'],
        'bg_status' => $colorItem['bg_status'],
        'bg_choose' => $colorItem['bg_choose'],
        'position' => $key,           // index mảng = position
        'is_save' => 1
    ];
    if ($colorItem['id']) {
        StatusChat::where('id', $colorItem['id'])
            ->where('bot_id', $current_bot_id)
            ->update($settings);
    } else {
        StatusChat::create($settings);
    }
}
```

**Response thành công**: `{ "success": true }`

**Response lỗi**: `{ "success": false, "msg": "update fail" }` (HTTP 200)

**⚠ Các điểm bất thường**:
1. Validation trên server **không có** — chỉ JS client validate (`setting_color.js:52-60`).
2. `position` = index mảng bắt đầu từ 0 → record đầu tiên có `position=0`, khác với EP-08 `ajaxSaveAllStatus` (bắt đầu từ 1).
3. Không dùng transaction (commented out `DB::beginTransaction()`) — nếu fail giữa chừng → inconsistent state.

---

## EP-07 · POST `/ajax/save-item-status` (legacy — không dùng ở UI v2)

**Controller**: `ChatController::ajaxSaveItemStatus` (`ChatController.php:654-689`).

**Request**:
```json
{
  "id": 101,
  "name_status": "見込みあり",
  "color": "#F44336",
  "bg_status": "#FDEBE9",
  "bg_choose": "#F44336"
}
```

**Logic**:
- Nếu có `id` → update 1 record.
- Nếu không có `id` → shift toàn bộ list position +1 rồi insert item mới ở `position=1` (insert đầu).

**Response**: `{success: true, data: StatusChat}` hoặc `{success: false, msg: 'update fail'}`

---

## EP-08 · POST `/ajax/save-all-status` (legacy)

**Controller**: `ChatController::ajaxSaveAllStatus` (`ChatController.php:725-770`).

**Có validation server** (chỉ endpoint này có):
| Điều kiện | Message lỗi |
|-----------|-------------|
| `name_status` rỗng | 「ステータス必ず指定してください。」 |
| `mb_strlen(name_status) > 10` | 「ステータス名は10文字以下にしてください。」 (chú ý: giới hạn 10 — khác với counter UI hiện tại là 20!) |
| `color` rỗng | 「カラー必ず指定してください。」 |

**⚠ Bất thường #2**: Giới hạn `name_status` trên EP-08 là **10 ký tự** trong khi UI v2 hiển thị counter 20 và EP-06 không kiểm tra gì. Không nhất quán.

---

## EP-09 · POST `/ajax/sort-status-chat` (legacy)

**Controller**: `ChatController::ajaxSortStatusChat` (`ChatController.php:771-787`).

**Request**:
```json
{ "order": [ {"id":101}, {"id":103}, {"id":102} ] }
```

**Logic**: cập nhật `position` = index+1 cho từng id.

**⚠ Không filter theo `bot_id`** → về nguyên tắc, admin có thể đổi `position` của status thuộc bot khác nếu biết id. Tuy nhiên UI lấy id từ list đã filter bot_id nên khó exploit qua UI, nhưng là lỗ hổng authorization tiềm ẩn.

---

## EP-10 · POST `/ajax/delete-item-status`

**Mục đích**: Xoá 1 status.

**Controller**: `ChatController::ajaxDeleteItemStatus(Request $request)` (`ChatController.php:789-826`).

**Request**:
```json
{ "id": 101 }
```

**Logic**:
1. Tìm status theo `id + bot_id`.
2. Lấy toàn bộ `Conversation` có `id_status = id AND bot_id = current_bot_id`.
3. Với mỗi conversation → `SyncElasticsearch::insertElasticsearch([...])` với `status_id: null` (queue re-index ES).
4. `StatusChat::where('id', $id)->where('bot_id', $botId)->delete()` (hard delete).
5. `Conversation::where('bot_id', $botId)->where('id_status', $id)->update(['id_status' => null])` (SET NULL các hội thoại đang gán).

**Response thành công**: `{ "success": true }`

**Không có confirm dialog server-side** và **không có cảnh báo** nếu status đang được gán cho conversation — cứ xoá thẳng rồi set NULL.

**Side effect quan trọng (ghi chú cho job-analyzer)**: tạo bản ghi vào bảng `sync_elasticsearch` để background job đồng bộ lại ES.

---

## Liên kết Endpoint ↔ Màn hình

| Màn hình | Endpoints |
|----------|-----------|
| SCR-CST-01 (list status) | EP-04 (load), EP-10 (delete), EP-06 (save sau sort/edit) |
| SCR-CST-02 (modal thêm/sửa) | EP-06 (submit) |
| SCR-CST-03 (tab 2 auto-confirm) | EP-02 (load), EP-03 (save với `type=1`) |
| SCR-CST-04 (tab 3 shortcut) | EP-02 (load), EP-03 (save với `type=2`) |
| SCR-CST-05 (tab 4 shorten URL) | EP-02 (load), EP-03 (save với `type=3`) |
| SCR-CST-06 (tab 5 preview) | EP-02 (load), EP-03 (save với `type=4`) |
| SCR-CST-07 (tab 6 FAQ) | Không có API call |

## Tham khảo client-side (xác nhận endpoint thực dùng)
- `public/js/chat_setting/index.js` — tab 2-5 (EP-02, EP-03)
- `public/js/chat_setting/setting_color.js` — tab 1 (EP-04, EP-06, EP-10)
