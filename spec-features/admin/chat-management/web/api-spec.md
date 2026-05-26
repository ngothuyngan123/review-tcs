# [FA-002] Quản lý chat — API Spec

> Phân tích từ source code Laravel (`src/web/`).
> Confidence: **Cao** — đọc trực tiếp từ code.

## Danh sách Endpoints

| EP | Method | URI | Controller@Action | Middleware | Mô tả |
|----|--------|-----|-------------------|-----------|-------|
| EP-01 | GET | `/basic/talk-list` | `Basic\TalkListController@index` | web, basic_access, https_protocol, is_expire, check_remember_token, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Hiển thị trang danh sách quản lý chat |
| EP-02 | POST | `/ajax/get-talk-list-v2` | `Basic\TalkListController@ajaxGetTalkListData` | web, check_login, check_remember_token, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy danh sách tin nhắn (AJAX, phân trang lazy load) |
| EP-03 | POST | `/ajax/get-detail-message-talk-list` | `Basic\TalkListController@getDetailMessageTalkList` | web, check_login, check_remember_token, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy chi tiết 1 tin nhắn (cho modal) |
| EP-04 | POST | `/ajax/talk-list-send-message` | `Basic\TalkListController@ajaxTalkSendMessage` | web, check_login, check_remember_token, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Gửi tin nhắn trả lời cho bạn bè LINE |
| EP-05 | POST | `/ajax/change-status-message` | `Basic\TalkListController@changeStatusMessage` | web, check_login, check_remember_token, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Thay đổi trạng thái xác nhận tin nhắn (đơn lẻ hoặc hàng loạt) |
| EP-06 | GET | `/ajax/talk-list/get-data-common-filter` | `Basic\TalkListController@ajaxGetDataCommonFilter` | web, check_login, check_remember_token, NotifyChatworkRequestTimeSlow, LogRequestMultipart | Lấy dữ liệu cho bộ lọc nâng cao (scenario, conversion, status chat) |

---

## Chi tiết Endpoints

### EP-01: GET `/basic/talk-list`
- **Controller**: `App\Http\Controllers\Basic\TalkListController@index`
- **File**: `app/Http/Controllers/Basic/TalkListController.php:48`
- **Middleware**: `web`, `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`
- **Mô tả**: Render trang Blade hiển thị giao diện quản lý chat. Truyền `startDate` và `endDate` (đều `null` mặc định) vào view `basic.talk_list.index`.
- **Liên kết UI**: SCR-TLK-01 → Trang danh sách tin nhắn chính

#### Request Parameters
Không có tham số. Trang tĩnh, dữ liệu được load AJAX sau khi render.

#### Response
HTML — Blade view `basic.talk_list.index` với `startDate = null`, `endDate = null`.

> **Ghi chú**: Code comment cho thấy trước đây `startDate` và `endDate` được mặc định 7 ngày gần nhất (`now - 7 days` đến `now`), nhưng đã bị tắt — hiện tại mặc định `null` (hiển thị toàn bộ). [Confidence: **Cao**]

---

### EP-02: POST `/ajax/get-talk-list-v2`
- **Controller**: `App\Http\Controllers\Basic\TalkListController@ajaxGetTalkListData`
- **File**: `app/Http/Controllers/Basic/TalkListController.php:61`
- **Middleware**: `web`, `check_login`, `check_remember_token`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`
- **Mô tả**: Lấy danh sách tin nhắn chat với bộ lọc, phân trang kiểu lazy load (offset-based). Hỗ trợ lọc theo trạng thái, khoảng thời gian, từ khóa tìm kiếm, và bộ lọc nâng cao. Truy vấn đa bảng tin nhắn (MessagesV2, Messages, MessagesPage2, MessagesOld theo năm).
- **Liên kết UI**: SCR-TLK-01 → Bảng dữ liệu danh sách tin nhắn (auto-load khi mở trang, scroll, đổi tab, lọc)

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `status` | Body | Array[Integer] | Không | Mảng trạng thái lọc. Giá trị: `0` = reception (chỉ tin nhận), `1` = send (bao gồm tin gửi), `4` = not_confirmed (chỉ tin chưa xác nhận) | Không có validation rule tường minh |
| `start_date` | Body | String (date) | Không | Ngày bắt đầu lọc. Format: `YYYY-MM-DD` | Không |
| `end_date` | Body | String (date) | Không | Ngày kết thúc lọc. Format: `YYYY-MM-DD` | Không |
| `condition_filter` | Body | String (JSON) | Không | JSON string chứa mảng điều kiện lọc nâng cao (tag, friend_name, day_add_friend, scenario, conversion, qr_code, qr_code_action, friend_info). Parse bằng `json_decode` | Không |
| `condition_message` | Body | Array[Integer] | Không | Mảng filter loại tin nhắn. Giá trị: `1` = button (hiển thị tin nhắn dạng【〇〇】), `2` = sticker (hiển thị sticker) | Không |
| `offset` | Body | Integer | Không | Vị trí bắt đầu (lazy load). Mặc định `0` | Không |
| `msg_table` | Body | String | Không | Tên bảng tin nhắn hiện tại (dùng cho phân trang qua nhiều bảng) | Không |
| `total_msg_send` | Body | Integer | Không | Tổng số tin nhắn đã gửi (tracking) | Không |
| `keyword_search` | Body | String | Không | Từ khóa tìm kiếm nội dung tin nhắn | Không |
| `lastMessageId` | Body | Integer | Không | ID tin nhắn cuối cùng đã load. Mặc định `0` | Không |
| `currentYear` | Body | Integer | Không | Năm hiện tại đang truy vấn (dùng cho sharding). Mặc định `0` | Không |
| `isLoadMsgNew` | Body | Integer | Không | Flag có load tin nhắn mới (bảng `messages_v2s`) không. `1` = có, `0` = không | Không |

#### Request mẫu
```json
{
  "status": [0],
  "start_date": null,
  "end_date": null,
  "condition_filter": null,
  "condition_message": null,
  "offset": 0,
  "msg_table": null,
  "total_msg_send": 0,
  "keyword_search": "",
  "lastMessageId": 0,
  "currentYear": 0,
  "isLoadMsgNew": 1
}
```

#### Response mẫu (thành công)
```json
{
  "status": true,
  "talk_list": {
    "items": [
      {
        "id": 12345,
        "conversation_id": 678,
        "msg_kind": 1,
        "msg_type": "text",
        "content": "Hh",
        "msg_created_at": "2026-03-24 13:30:00",
        "is_confirmed": 0,
        "is_message_new": 1,
        "is_blocked_conversation": 0,
        "line_user_id": "U1234567890",
        "name": "テスト'T",
        "avatar_user": "https://profile.line-scdn.net/...",
        "line_id": "U1234567890"
      }
    ],
    "status": [0],
    "totalMsg": 0,
    "offset": 100,
    "msg_table": null,
    "flagEnd": 1,
    "totalMsgSend": 0,
    "start_date": null,
    "end_date": null,
    "lastMessageId": 12345,
    "currentYear": 2026,
    "isLoadMsgNew": 0
  },
  "bot_name": "Bot name"
}
```

> **Ghi chú cấu trúc response**:
> - `items[].is_confirmed`: `0` = chưa xác nhận (未確認), `1` = đã xác nhận (確認済). Logic xác nhận dựa trên bảng `unconfirm_message` — nếu có record thì `0`, không có thì `1`. [Confidence: **Cao**]
> - `flagEnd`: `0` = còn dữ liệu ở bảng cũ hơn có thể load, `1` = đã hết hoặc còn dữ liệu trong cùng bảng. [Confidence: **Cao**]
> - `isLoadMsgNew`: `1` = vẫn đang load từ bảng `messages_v2s`, `0` = đã chuyển sang các bảng cũ. [Confidence: **Cao**]
> - `currentYear`: năm của bảng messages đang truy vấn — dùng cho sharded tables (messages, messages2020..2025). [Confidence: **Cao**]
> - Dữ liệu phân trang kiểu infinite scroll — mỗi lần load 100 records. [Confidence: **Cao**]

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | Exception xảy ra | `{"status": false, "msg": "{error message}"}` |

---

### EP-03: POST `/ajax/get-detail-message-talk-list`
- **Controller**: `App\Http\Controllers\Basic\TalkListController@getDetailMessageTalkList`
- **File**: `app/Http/Controllers/Basic/TalkListController.php:387`
- **Middleware**: `web`, `check_login`, `check_remember_token`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`
- **Mô tả**: Lấy chi tiết một tin nhắn cụ thể. Truy vấn từ bảng `messages_v2s`, xử lý replace_content (thay thế biến trong nội dung), hỗ trợ nhiều loại tin nhắn (text, audio, sticker, file, PDF, location, buttons, image map). Nếu tin nhắn có `source_message`, trả về danh sách capture templates.
- **Liên kết UI**: SCR-TLK-01 → Nút「詳細」→ Modal SCR-TLK-02

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `id_message` | Body | Integer | Có | ID tin nhắn cần xem chi tiết | Không có validation rule tường minh |

#### Request mẫu
```json
{
  "id_message": 12345
}
```

#### Response mẫu (thành công — tin nhắn text đơn giản)
```json
{
  "message": [
    {
      "id": 12345,
      "conversation_id": 678,
      "bot_id": 1,
      "msg_kind": 1,
      "type": 1,
      "content": "Hh",
      "created_at": "2026-03-24 13:30:00",
      "type_data": "msg"
    }
  ]
}
```

#### Response mẫu (thành công — tin nhắn có source_messages/templates)
```json
{
  "message": [
    {
      "id": 1,
      "type": 1,
      "content": "Nội dung template đã thay thế biến",
      "type_data": "template"
    }
  ]
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | Exception xảy ra | `{"status": false, "msg": "{error message}"}` |

> **Ghi chú**: Chỉ truy vấn bảng `messages_v2s` (tin nhắn mới). Không fallback sang bảng Messages legacy. Có thể không tìm thấy tin nhắn cũ. [Confidence: **Cao**]

---

### EP-04: POST `/ajax/talk-list-send-message`
- **Controller**: `App\Http\Controllers\Basic\TalkListController@ajaxTalkSendMessage`
- **File**: `app/Http/Controllers/Basic/TalkListController.php:176`
- **Middleware**: `web`, `check_login`, `check_remember_token`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`
- **Mô tả**: Gửi tin nhắn trả lời cho bạn bè LINE từ modal chi tiết. Tìm `LineUser` theo `line_id`, lấy `Conversation`, rồi gọi `MessageService::createMessageV2()` để tạo và gửi tin nhắn qua LINE API. Sau khi gửi thành công, cập nhật `free_send_count` của bot và tăng counter gửi tin.
- **Liên kết UI**: SCR-TLK-02 → Nút「送信」gửi tin nhắn trả lời

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `line_id` | Body | String | Có | LINE ID của người nhận (LINE user ID, vd: `U1234567890`) | Không có validation rule tường minh |
| `msg` | Body | String | Có | Nội dung tin nhắn trả lời (text) | Không có validation rule tường minh |

#### Request mẫu
```json
{
  "line_id": "U1234567890",
  "msg": "Cảm ơn bạn đã liên hệ!"
}
```

#### Response mẫu (thành công)
```json
{
  "success": true
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | Gửi LINE API thất bại | `{"success": false, "msg": "{LINE API error raw body}"}` |
| 200 | Bot free plan đạt giới hạn 1000 tin | `{"result": "error", "error_message": "配信数上限に達しています。こちらから契約内容を確認してください。", "error_code": "limit_max"}` |

> **Ghi chú side effects**: [Confidence: **Cao**]
> - Gọi LINE Push Message API qua `MessageService::createMessageV2()`
> - Tăng `bots.free_send_count` + 1 khi gửi thành công
> - Gọi `updateMessageSendCount()` — cập nhật bảng `summary_message_send` (type_chat = 1, tức Chat 1:1)
> - Ghi log action qua `addLogUserAction()`

---

### EP-05: POST `/ajax/change-status-message`
- **Controller**: `App\Http\Controllers\Basic\TalkListController@changeStatusMessage`
- **File**: `app/Http/Controllers/Basic/TalkListController.php:245`
- **Middleware**: `web`, `check_login`, `check_remember_token`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`
- **Mô tả**: Thay đổi trạng thái xác nhận tin nhắn. Hỗ trợ 2 mode: `simple` (chọn từng tin nhắn cụ thể) và `all` (tất cả tin nhắn khớp bộ lọc hiện tại). Trạng thái `1` = 確認済 (đã xác nhận), `2` = 未確認 (chưa xác nhận).
- **Liên kết UI**: SCR-TLK-01 → Khu vực「ステータス 一括変更」+ Nút「変更」

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `status` | Body | Integer | Có | Trạng thái mới: `1` = 確認済 (xoá unconfirm), `2` = 未確認 (tạo unconfirm) | Không |
| `type_action` | Body | String | Có | Kiểu thao tác: `"simple"` = chọn từng tin, `"all"` = tất cả theo bộ lọc | Không |
| `messages` | Body | Array[Integer] | Có (khi `type_action = "simple"`) | Mảng ID tin nhắn cần thay đổi | Không |
| `filter_status` | Body | Array[Integer] | Không (khi `type_action = "all"`) | Trạng thái lọc hiện tại (giống EP-02) | Không |
| `start_date` | Body | String (date) | Không (khi `type_action = "all"`) | Ngày bắt đầu lọc | Không |
| `end_date` | Body | String (date) | Không (khi `type_action = "all"`) | Ngày kết thúc lọc | Không |
| `condition_filter` | Body | String (JSON) | Không (khi `type_action = "all"`) | JSON string bộ lọc nâng cao | Không |
| `condition_message` | Body | Mixed | Không (khi `type_action = "all"`) | Filter loại tin nhắn | Không |
| `keyword_search` | Body | String | Không (khi `type_action = "all"`) | Từ khóa tìm kiếm | Không |

#### Request mẫu (simple — chọn từng tin)
```json
{
  "status": 1,
  "type_action": "simple",
  "messages": [12345, 12346, 12347]
}
```

#### Request mẫu (all — theo bộ lọc)
```json
{
  "status": 1,
  "type_action": "all",
  "filter_status": [0],
  "start_date": "2026-03-01",
  "end_date": "2026-03-24",
  "condition_filter": null,
  "condition_message": null,
  "keyword_search": null
}
```

#### Response mẫu (thành công)
```json
{
  "success": true
}
```

#### Response lỗi
Không có error response tường minh — exception sẽ trả về HTTP 500.

> **Ghi chú side effects**: [Confidence: **Cao**]
> - Khi `status = 1` (確認済): Xoá records trong `unconfirm_message` tương ứng
> - Khi `status = 2` (未確認): Tạo record mới trong `unconfirm_message` (nếu chưa có), cập nhật `is_confirmed = 0` trên bảng messages legacy
> - Cập nhật `conversation.confirm_count` (1 nếu còn unconfirm, 0 nếu hết)
> - Cập nhật `conversation.status_last_message` (1 nếu hết unconfirm, 0 nếu còn)
> - Cập nhật `bots.count_user_unconfirm` — đếm lại số conversation chưa xác nhận
> - Ghi `SyncElasticsearch` nếu `confirm_count` thay đổi
> - Gọi `updateBadge()` — gửi FCM notification cập nhật badge count trên mobile
> - Broadcast `InfoEvent` qua WebSocket — cập nhật realtime số lượng unconfirm, error, group confirm trên UI

---

### EP-06: GET `/ajax/talk-list/get-data-common-filter`
- **Controller**: `App\Http\Controllers\Basic\TalkListController@ajaxGetDataCommonFilter`
- **File**: `app/Http/Controllers/Basic/TalkListController.php:365`
- **Middleware**: `web`, `check_login`, `check_remember_token`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`
- **Mô tả**: Lấy dữ liệu cần thiết để hiển thị bộ lọc nâng cao: danh sách scenario (step), danh sách conversion, và danh sách status chat của bot hiện tại.
- **Liên kết UI**: SCR-TLK-03 → Modal filter nâng cao — cung cấp options cho bộ lọc「ステップ購読状況」,「コンバージョン」,「メッセージ確認状況」

#### Request Parameters
Không có tham số. Bot ID lấy từ session (`getBotId()`).

#### Response mẫu (thành công)
```json
{
  "status": true,
  "scenario": [
    {
      "id": 1,
      "name": "Welcome Scenario",
      "bot_id": 123
    }
  ],
  "conversion": [
    {
      "id": 1,
      "name": "Purchase Conversion"
    }
  ],
  "statusObject": [
    {
      "id": 1,
      "bot_id": 123,
      "name": "新規",
      "created_at": "2024-01-01 00:00:00"
    }
  ]
}
```

#### Response lỗi
| HTTP Code | Điều kiện | Response body |
|-----------|----------|--------------|
| 200 | Exception xảy ra | `{"status": false, "msg": "{error message}"}` |

---

## Middleware phân tích

| Middleware | Mô tả | Áp dụng cho |
|-----------|-------|------------|
| `web` | Session-based authentication mặc định của Laravel | Tất cả EP |
| `basic_access` | Kiểm tra quyền truy cập Basic portal (Admin/Staff) | EP-01 |
| `check_login` | Kiểm tra user đã đăng nhập | EP-02, EP-03, EP-04, EP-05, EP-06 |
| `check_remember_token` | Kiểm tra remember token hợp lệ | Tất cả EP |
| `https_protocol` | Chuyển hướng sang HTTPS nếu cần | EP-01 |
| `is_expire` | Kiểm tra tài khoản/bot chưa hết hạn | EP-01 |
| `NotifyChatworkRequestTimeSlow` | Log cảnh báo nếu request chậm | Tất cả EP |
| `LogRequestMultipart` | Log request multipart | EP-01 (và implicit qua web middleware group) |

> **Ghi chú**: Bot ID được lấy từ session qua helper `getBotId()` — tất cả endpoint đều phụ thuộc vào session có `current_bot_id`. Không có kiểm tra Staff permission riêng trong controller — quyền truy cập Talk List phụ thuộc vào middleware `basic_access` và cấu hình role Staff. [Confidence: **Trung bình**]

---

## Liên kết UI ↔ API

| Màn hình | Action | Endpoint | Ghi chú |
|---------|--------|----------|---------|
| SCR-TLK-01 | Load trang | EP-01 | Render HTML, dữ liệu load AJAX sau |
| SCR-TLK-01 | Load danh sách tin nhắn | EP-02 | Gọi ngay sau khi trang render, và khi scroll/thay đổi bộ lọc |
| SCR-TLK-01 | Tab「一覧」 | EP-02 | `status = [0]` (mặc định chỉ tin nhận) |
| SCR-TLK-01 | Tab「未確認のみ」 | EP-02 | `status = [0, 4]` (tin nhận + chỉ chưa xác nhận) |
| SCR-TLK-01 | Checkbox「返信を含める」 | EP-02 | `status = [0, 1]` (bao gồm cả tin gửi) |
| SCR-TLK-01 | Tìm kiếm「メッセージ検索」 | EP-02 | `keyword_search = "{từ khóa}"` |
| SCR-TLK-01 | Lọc khoảng thời gian | EP-02 | `start_date`, `end_date` |
| SCR-TLK-01 | Nút「変更」(thay đổi trạng thái) | EP-05 | `type_action = "simple"` với danh sách message IDs đã chọn |
| SCR-TLK-01 | Nút「詳細」 | EP-03 | Lấy chi tiết tin nhắn trước khi hiển thị modal |
| SCR-TLK-02 | Nút「送信」 | EP-04 | Gửi tin nhắn trả lời |
| SCR-TLK-03 | Mở modal filter | EP-06 | Lấy dữ liệu scenario, conversion, status cho dropdown |
| SCR-TLK-03 | Nút「保存」 | EP-02 | Gọi lại EP-02 với `condition_filter` chứa các điều kiện lọc |
