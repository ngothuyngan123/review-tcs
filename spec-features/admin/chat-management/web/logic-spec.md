# [FA-002] Quản lý chat — Logic Spec

> Phân tích từ source code Laravel (`src/web/`).
> Confidence: **Cao** — đọc trực tiếp từ code.

## Controllers

### TalkListController
- **File**: `app/Http/Controllers/Basic/TalkListController.php` (501 dòng)
- **Namespace**: `App\Http\Controllers\Basic`
- **Dependencies** (inject qua constructor):
  - `ConversationRepositoryInterface` → `ConversationRepository`
  - `MessageService`

---

#### Action: index() — EP-01
- **Route**: GET `/basic/talk-list`
- **Chức năng**: Render trang Blade hiển thị giao diện quản lý chat
- **Luồng xử lý**:
  1. Gán `$startDate = null`, `$endDate = null`
  2. Trả về view `basic.talk_list.index` với compact startDate, endDate
- **Gọi đến**: Không gọi service/model — chỉ render view
- **Ghi chú**: Code comment cho thấy trước đây sử dụng `Carbon::now()->subDays(7)` cho `$startDate` — đã bị tắt. [Confidence: **Cao**, file:48-55]

---

#### Action: ajaxGetTalkListData() — EP-02
- **Route**: POST `/ajax/get-talk-list-v2`
- **Chức năng**: Lấy danh sách tin nhắn với bộ lọc và phân trang lazy load
- **Luồng xử lý**:
  1. Lấy `bot_id` từ session (`getBotId()`)
  2. Parse tham số: `status`, `start_date`, `end_date`, `condition_filter` (JSON decode), `condition_message`, `offset`, `msg_table`, `total_msg_send`, `keyword_search`, `lastMessageId`, `currentYear`, `isLoadMsgNew`
  3. Gọi `BotLineUser::makeDataTalkList()` — trả về mảng 8 phần tử [listMsg, totalMsg, offset, msg_table, flagEnd, totalMsgSend, currentYear, isLoadMsgNew]
  4. Với mỗi tin nhắn trong `listMsg`:
     - Truy vấn `Conversation` theo `conversation_id` → lấy `is_blocked`, `line_id`
     - Nếu không tìm thấy conversation → bỏ qua tin nhắn
     - Gán `is_blocked_conversation`, `line_user_id`
     - Truy vấn `UnconfirmMessage` theo `message_id`:
       - Có record + `is_confirmed = 0` → `item.is_confirmed = 0` (未確認)
       - Không có record → `item.is_confirmed = 1` (確認済)
     - Truy vấn `LineUser` theo `line_user_id` → gán `name`, `avatar_user`, `line_id`
     - Cập nhật `lastMessageId`
  5. Lấy `bot_name` từ `Bots::find(getBotId())`
  6. Trả JSON response với `talk_list` data object và `bot_name`
- **Gọi đến**: `BotLineUser::makeDataTalkList()`, `Conversation`, `UnconfirmMessage`, `LineUser`, `Bots`
- **Side effects**: Không có (read-only)
- [Confidence: **Cao**, file:61-130]

---

#### Action: ajaxTalkSendMessage() — EP-04
- **Route**: POST `/ajax/talk-list-send-message`
- **Chức năng**: Gửi tin nhắn text trả lời cho bạn bè LINE
- **Luồng xử lý**:
  1. Ghi log action: `addLogUserAction('ajaxTalkSendMessage')`
  2. Lấy `bot_id` từ session, tìm `Bots`
  3. Tìm `LineUser` theo `request->line_id` (WHERE `line_id = ?`)
  4. Tìm `Conversation` theo `tb_line_user_id = lineUser.id` và `bot_id`
  5. Tạo message object:
     - `msg_kind` = `MessagesV2::KIND_MESSAGE_BOT_SEND` (= 0)
     - `type` = `MessagesV2::TYPE_MESSAGE_TEXT` (= 1)
     - `content` = `request->msg`
     - `originalContent` = `request->msg`
  6. Gọi `MessageService::createMessageV2()` với `message`, `bot`, `lineUser`, `conversationId`, `is_count_sent=true`, `isUpdateLastMess=true`, `useSocket=true`
  7. Kiểm tra response:
     - `false` (thất bại) + bot free plan (plan_type=2) + free_send_count >= 1000 → trả lỗi `limit_max`
     - Thành công (`isSucceeded()`) → cập nhật `bots.free_send_count += 1`, gọi `updateMessageSendCount(bot_id, now, 1)` (type_chat=1 = Chat11)
     - Không thành công → trả `{"success": false, "msg": "{raw body}"}`
- **Gọi đến**: `Bots`, `LineUser`, `Conversation`, `MessageService::createMessageV2()`
- **Side effects**:
  - Gửi tin nhắn qua LINE Push Message API
  - Tạo record trong `messages_v2s`
  - Cập nhật `bots.free_send_count`
  - Cập nhật `summary_message_send` (type_chat=1)
  - Broadcast qua WebSocket (nếu `useSocket=true`)
- [Confidence: **Cao**, file:176-230]

---

#### Action: changeStatusMessage() — EP-05
- **Route**: POST `/ajax/change-status-message`
- **Chức năng**: Thay đổi trạng thái xác nhận tin nhắn (đơn lẻ hoặc hàng loạt)
- **Luồng xử lý**:
  1. Ghi log action: `addLogUserAction("changeStatusMessage TalkListController")`
  2. Lấy `status`, `type_action`, `botId`
  3. **Mode "simple"**: Lấy `messages` = mảng message IDs từ request
  4. **Mode "all"**:
     - Parse bộ lọc: `filter_status`, `start_date`, `end_date`, `condition_filter`, `condition_message`, `keyword_search`
     - Nếu có `condition_filter` → gọi `Conversation::advanceFilterPost()` để lấy danh sách `line_user_id` → tìm `conversation_id`
     - Gọi `BotLineUser::getMsgTalkList()` — truy vấn tất cả bảng messages (V2, Messages, Page2, Old) khớp bộ lọc → trả mảng message IDs
  5. **Xử lý từng message ID**:
     - Nếu `status = 1` (確認済): Xoá tất cả `UnconfirmMessage` theo danh sách message IDs (batch delete)
     - Tìm tin nhắn qua fallback chain: `MessagesV2` → `Messages` → `MessagesPage2` → `MessagesOld`
     - Nếu tìm thấy:
       - Nếu `status = 2` (未確認):
         - Cập nhật `message.is_confirmed = 0` (chỉ trên bảng legacy, không phải V2)
         - Tạo record `UnconfirmMessage` nếu chưa tồn tại
       - Đếm `UnconfirmMessage` theo `conversation_id`
       - Cập nhật `conversation.confirm_count` = 1 (nếu còn unconfirm) hoặc 0 (nếu hết)
       - Cập nhật `conversation.status_last_message` = 1 (hết unconfirm) hoặc 0 (còn unconfirm)
       - Nếu `confirm_count` thay đổi → ghi `SyncElasticsearch` (type = update)
  6. **Sau vòng lặp**:
     - Tính lại `count_user_unconfirm` → cập nhật `bots.count_user_unconfirm`
     - Gọi `updateBadge(bot)` — gửi FCM push notification cập nhật badge
     - Broadcast `InfoEvent` qua WebSocket — cập nhật realtime trên UI
- **Gọi đến**: `BotLineUser::getMsgTalkList()`, `Conversation::advanceFilterPost()`, `UnconfirmMessage`, `MessagesV2`, `Messages`, `MessagesPage2`, `MessagesOld`, `SyncElasticsearch`, `ConversationRepository::updateConversation()`, `Bots`
- **Side effects**:
  - INSERT/DELETE trên `unconfirm_message`
  - UPDATE trên `conversation` (confirm_count, status_last_message)
  - UPDATE trên `messages` (is_confirmed) — chỉ bảng legacy
  - UPDATE trên `bots` (count_user_unconfirm, last_time_count_user_confirm)
  - INSERT trên `sync_elasticsearch`
  - FCM push notification (badge update)
  - WebSocket broadcast (InfoEvent)
- [Confidence: **Cao**, file:245-363]

---

#### Action: ajaxGetDataCommonFilter() — EP-06
- **Route**: GET `/ajax/talk-list/get-data-common-filter`
- **Chức năng**: Lấy dữ liệu cho bộ lọc nâng cao
- **Luồng xử lý**:
  1. Lấy `bot_id` từ session
  2. Truy vấn `Scenario` WHERE `bot_id` → tất cả scenarios
  3. Truy vấn `Conversion` SELECT `name, id` WHERE `bot_id` → danh sách conversions
  4. Truy vấn `StatusChat` WHERE `bot_id` → danh sách trạng thái chat
  5. Trả JSON response
- **Gọi đến**: `Scenario`, `Conversion`, `StatusChat`
- **Side effects**: Không có (read-only)
- [Confidence: **Cao**, file:365-385]

---

#### Action: getDetailMessageTalkList() — EP-03
- **Route**: POST `/ajax/get-detail-message-talk-list`
- **Chức năng**: Lấy chi tiết một tin nhắn, xử lý replace content và decode media
- **Luồng xử lý**:
  1. Lấy `botId` từ session, `id_message` từ request
  2. Truy vấn `MessagesV2` WHERE `id = id_message` AND `bot_id = botId`
  3. Lấy `replace_content` (JSON array chứa cặp `rp_key` / `rp_value`)
  4. Kiểm tra `source_messages` relationship:
     - **Có source_message**:
       - Parse `list_capture_template_id` (comma-separated)
       - Truy vấn từng `CaptureTemplate`
       - Áp dụng `replace_content` lên nội dung template
       - Decode JSON content cho các loại: audio, buttons, sticker, location, introduction
       - Xử lý buttons: thay thế biến trong title/text
       - Gán `type_data = "template"` cho mỗi template
       - Return danh sách templates
     - **Không có source_message**:
       - Áp dụng `replace_content` lên nội dung tin nhắn (nếu type=text)
       - Decode JSON content cho: audio, sticker, file, PDF, location
       - Xử lý booking message types → chuyển thành text
       - Gán `type_data = "msg"`
       - Return mảng chứa 1 tin nhắn
  5. Trả JSON response
- **Gọi đến**: `MessagesV2`, `SourceMessage`, `CaptureTemplate`, `ConversationService::isJson()`
- **Side effects**: Không có (read-only)
- [Confidence: **Cao**, file:387-499]

---

#### Method: renderViewSetting() (nội bộ, không có route công khai)
- **File**: `app/Http/Controllers/Basic/TalkListController.php:136`
- **Chức năng**: Render view chi tiết cài đặt tin nhắn. Tìm URLs trong nội dung tin nhắn và lấy thống kê click.
- **Ghi chú**: Phương thức này không được sử dụng trực tiếp qua route nào trong Talk List flow — có thể là code legacy. [Confidence: **Trung bình**]

---

## Models

### BotLineUser
- **File**: `app/BotLineUser.php` (690 dòng)
- **Bảng DB**: `bot_line_user`
- **Connection**: `mysql` (mặc định)
- **Timestamps**: Không (`$timestamps = false`)

#### Relationships
| Relationship | Kiểu | Model liên quan | Foreign Key | Mô tả |
|-------------|------|----------------|------------|-------|
| `lineUser()` | hasOne | `LineUser` | `line_user_id` → `LineUser.id` | Thông tin LINE user |
| `bot()` | hasOne | `Bots` | `bot_id` → `Bots.id` | Bot sở hữu |
| `friendInformationValue()` | hasMany | `FriendInformationValue` | `line_user_id` → `line_id` | Giá trị thông tin bạn bè tuỳ chỉnh |

#### Static Methods quan trọng

##### `makeDataTalkList()` (file:18-124)
- **Mô tả**: Logic chính lấy danh sách tin nhắn cho Talk List
- **Input**: `$bot_id`, `$filter_status`, `$offset`, `$msg_table`, `$start_date`, `$end_date`, `$condition_message`, `$condition_filter`, `$keyword_search`, `$totalMsgSend`, `$currentYear`, `$isLoadMsgNew`
- **Output**: Array 8 phần tử `[listMsg, totalMsg, offset, msg_table, flagEnd, totalMsgSend, currentYear, isLoadMsgNew]`
- **Logic chi tiết**:
  1. Nếu có `condition_filter` → gọi `Conversation::advanceFilterPost()` → lấy `listConversation`
  2. Nếu filter "not_confirmed" (status=4) → lấy danh sách `messageUnConfirm` từ `UnconfirmMessage` (limit 1000)
  3. Ưu tiên load từ `MessagesV2` (bảng mới) trước:
     - Gọi `getListMessagesV2()` → offset/limit 100
  4. Nếu `MessagesV2` không đủ 100 records → chuyển sang bảng Messages legacy:
     - Gọi `getListMessages()` với `currentYear` → offset/limit phần còn thiếu
  5. Nếu vẫn không đủ → tìm `MessagesBotMapping` để xác định năm cũ hơn:
     - Giảm `currentYear` → truy vấn bảng messages của năm đó
  6. Trả kết quả kèm metadata phân trang (offset, flagEnd, currentYear, isLoadMsgNew)
- **Limit**: 100 records mỗi lần load
- **Max execution time**: 180 giây (set bằng `ini_set`)
- [Confidence: **Cao**]

##### `getListMessagesV2()` (private, file:223-288)
- **Bảng**: `messages_v2s` (connection `mysql_message`)
- **Loại trừ types**: START_REMIND (9), STOP_REMIND (10), SETTING_SCENARIO (6), STOP_SCENARIO (7)
- **Lọc theo status**:
  - `not_confirmed` (4): `WHERE id IN (messageUnConfirm) AND msg_kind = 1`
  - `reception` (0): `WHERE msg_kind = 1`
  - `send` (1): `WHERE msg_kind != KIND_MESSAGE_SCENARIO` (2)
- **Lọc theo condition_message**:
  - Mặc định ẩn tin nhắn dạng `【%】` và sticker
  - Nếu `condition_message` chứa `button` (1) → hiển thị tin nhắn dạng `【%】`
  - Nếu `condition_message` chứa `sticker` (2) → hiển thị sticker
- **Lọc thêm**: `keyword_search` (LIKE), `start_date`, `end_date` (date range)
- **Order**: DESC theo ID

##### `getListMessages()` (private, file:131-221)
- **Bảng**: Sharded theo năm — `messages` (year=0), `messages2020`..`messages2025`
- **Logic tương tự** `getListMessagesV2()` nhưng dùng model khác theo `currentYear`
- **Khác biệt**: Bảng legacy có trường `is_confirmed` và `message_from` trực tiếp

##### `getMsgTalkList()` (file:640-684)
- **Mô tả**: Lấy ALL message IDs khớp bộ lọc (dùng cho changeStatusMessage mode "all")
- **Logic**: Truy vấn song song 4 bảng (V2, Messages, Page2, Old), gom tất cả IDs vào 1 mảng
- **Cảnh báo hiệu năng**: Không có limit — có thể trả về rất nhiều IDs. [Confidence: **Cao**]

---

### MessagesV2
- **File**: `app/MessagesV2.php` (100 dòng)
- **Bảng DB**: `messages_v2s`
- **Connection**: `mysql_message`
- **Timestamps**: Có

#### Constants — Loại tin nhắn (type)
| Hằng số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `TYPE_MESSAGE_TEXT` | 1 | Tin nhắn văn bản |
| `TYPE_MESSAGE_IMAGE` | 2 | Hình ảnh |
| `TYPE_MESSAGE_VIDEO` | 3 | Video |
| `TYPE_MESSAGE_AUDIO` | 4 | Âm thanh (「音声」) |
| `TYPE_MESSAGE_STICKER` | 5 | Sticker/Stamp |
| `TYPE_MESSAGE_SETTING_SCENARIO` | 6 | Cài đặt scenario (hệ thống) |
| `TYPE_MESSAGE_STOP_SCENARIO` | 7 | Dừng scenario (hệ thống) |
| `TYPE_MESSAGE_START_REMIND` | 9 | Bắt đầu nhắc nhở (hệ thống) |
| `TYPE_MESSAGE_STOP_REMIND` | 10 | Dừng nhắc nhở (hệ thống) |
| `TYPE_MESSAGE_PDF` | 11 | File PDF |
| `TYPE_MESSAGE_FILE` | 12 | File (「ファイル」) |
| `TYPE_MESSAGE_LOCATION` | 13 | Vị trí (「位置情報」) |
| `TYPE_MESSAGE_BROADCAST` | 14 | Broadcast |
| `TYPE_MESSAGE_SCENARIO` | 15 | Scenario message |
| `TYPE_MESSAGE_TEMPLATE` | 16 | Template |
| `TYPE_MESSAGE_ACTION_FROM_BOOKING` | 19 | Booking action |
| `TYPE_MESSAGE_ACTION_FROM_BOOKING_SALON` | 20 | Booking salon action |
| `TYPE_MESSAGE_ACTION_FROM_BOOKING_LESSON` | 21 | Booking lesson action |
| `TYPE_MESSAGE_ACTION_FROM_FORM_ANSWER` | 22 | Form answer action |

#### Constants — Loại gửi (msg_kind)
| Hằng số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `KIND_MESSAGE_BOT_SEND` | 0 | Bot/Admin gửi (chat 1:1) |
| `KIND_MESSAGE_FRIEND_SEND` | 1 | Bạn bè LINE gửi (tin nhận) |
| `KIND_MESSAGE_SCENARIO` | 2 | Scenario tự động gửi |
| `KIND_MESSAGE_BROADCAST` | 3 | Broadcast gửi |
| `KIND_MESSAGE_SEND_TEST` | 6 | Gửi test |
| `KIND_MESSAGE_TEMPLATE` | 7 | Template gửi |
| `KIND_MESSAGE_EVENT` | 10 | Event gửi |
| `KIND_MESSAGE_ADD_NEW_FRIEND` | 12 | Thêm bạn mới |
| `KIND_MESSAGE_ADD_OLD_FRIEND` | 13 | Thêm bạn cũ (quay lại) |
| `KIND_MESSAGE_FRIEND_BLOCK` | 14 | Bạn bè chặn |
| `KIND_MESSAGE_DELETE_MESSAGE` | 18 | Xoá tin nhắn |

#### Relationships
| Relationship | Kiểu | Model liên quan | FK | Mô tả |
|-------------|------|----------------|-----|-------|
| `source_messages()` | hasOne | `SourceMessage` | `source_message_id` → `SourceMessage.id` | Nguồn gốc tin nhắn (template, action, etc.) |

#### Accessors
| Attribute | Mô tả |
|----------|-------|
| `convert_type_message` | Chuyển đổi type số → tên string (image, text, video, audio, sticker, file, location) |

---

### Messages (Legacy)
- **File**: `app/Messages.php`
- **Bảng DB**: `messages`
- **Connection**: `mysql_message`
- **Ghi chú**: Bảng tin nhắn cũ. Có trường `is_confirmed` và `message_from` trực tiếp (khác MessagesV2).

#### Relationships
| Relationship | Kiểu | Model liên quan | FK | Mô tả |
|-------------|------|----------------|-----|-------|
| `UnconfirmMessage()` | hasOne | `UnconfirmMessage` | `message_id` → `id` | Liên kết trạng thái xác nhận |

> **Ghi chú**: Messages được sharded theo năm. Các model tương tự: `Messages2020`, `Messages2021`, ..., `Messages2025`, `MessagesPage2`, `MessagesOld`. Mỗi model trỏ tới bảng riêng cùng cấu trúc. [Confidence: **Cao**]

---

### UnconfirmMessage
- **File**: `app/UnconfirmMessage.php` (18 dòng)
- **Bảng DB**: `unconfirm_message`
- **Connection**: `mysql` (mặc định)
- **Timestamps**: Có

#### Relationships
| Relationship | Kiểu | Model liên quan | FK | Mô tả |
|-------------|------|----------------|-----|-------|
| `conversation()` | hasOne | `Conversation` | `conversation_id` → `Conversation.id` | Conversation chứa tin nhắn chưa xác nhận |

#### Vai trò trong hệ thống
- Bảng tracking tin nhắn **chưa xác nhận** (未確認)
- Mỗi record = 1 tin nhắn chưa được Admin đánh dấu xác nhận
- Khi Admin đánh dấu「確認済」→ record bị **xoá**
- Khi Admin đánh dấu「未確認」→ record được **tạo mới**
- Dùng để đếm `confirm_count` trên `conversation` và `count_user_unconfirm` trên `bots`
- [Confidence: **Cao**]

---

### Conversation
- **File**: `app/Conversation.php`
- **Bảng DB**: `conversation`
- **Connection**: `mysql` (mặc định)
- **Timestamps**: Có

#### Relationships
| Relationship | Kiểu | Model liên quan | FK | Mô tả |
|-------------|------|----------------|-----|-------|
| `groupMembers()` | hasMany | `GroupMembers` | `conversation_id` → `id` | Thành viên nhóm |
| `lineUser()` | hasOne | `LineUser` | `tb_line_user_id` → `LineUser.id` | LINE user liên kết |

#### Các trường quan trọng cho Talk List
| Trường | Mô tả |
|--------|-------|
| `bot_id` | ID bot sở hữu conversation |
| `tb_line_user_id` | ID LineUser (FK → `line_user.id`) |
| `line_id` | LINE ID (string) |
| `is_blocked` | Conversation bị chặn: 0 = không, 1 = có |
| `confirm_count` | Số lượng tin nhắn chưa xác nhận: 0 = tất cả đã xác nhận, 1 = có tin chưa xác nhận |
| `status_last_message` | Trạng thái tin nhắn cuối: 0 = chưa xác nhận, 1 = đã xác nhận |
| `is_hide` | Ẩn conversation: 0 = hiện, 1 = ẩn |

#### Static Method: advanceFilterPost() (file:227)
- **Mô tả**: Xây dựng query lọc nâng cao trên bảng `bot_line_user` dựa trên nhiều điều kiện
- **Input**: `$bot_id`, `$item_search` (AND conditions), `$item_search_or` (OR conditions), `$keyword`, `$is_autoReply`, `$lineUserId`, `$useDBReplicate`, `$useCross`
- **Các loại filter hỗ trợ**:

| Filter type | Key trong JSON | Mô tả | Bảng/trường liên quan |
|------------|---------------|-------|----------------------|
| Tag | `tag` | Lọc theo tags đã gán. Hỗ trợ 4 điều kiện: ít nhất 1 tag (0), tất cả tags (1), không có tag nào (2), không đủ tất cả (3) | `tag_line_user.tag_id` |
| Tên bạn bè | `friend_name` | Tìm theo LINE name (`line_user.name`) và/hoặc system name (`line_user.view_name`). Hỗ trợ chọn checkbox tìm theo loại nào | `line_user.name`, `line_user.view_name` |
| Ngày thêm bạn | `day_add_friend` | Lọc theo `bot_line_user.followed_at`. 2 kiểu: chọn khoảng ngày (type=0) hoặc khoảng số ngày trước (type=1) | `bot_line_user.followed_at` |
| Step/Scenario | `scenario` | Lọc theo trạng thái subscribe scenario. 7 điều kiện: đang follow (0), không follow (1), đang ở ngày N (2), đã hoàn thành (3), chưa hoàn thành (4), đã dừng hoặc hoàn thành (5), đã dừng (6) | `scenario_lineuser` |
| Conversion | `conversion` | Lọc theo conversion results. 2 điều kiện: đã convert tất cả (0), chưa convert hết (1) | `conversion_result` |
| QR Code | `qr_code` | Lọc theo QR code đã quét. 4 điều kiện: ít nhất 1 (0), tất cả (1), không có (2), không đủ hết (3) | `detail_landing_click` |
| QR Code Action | `qr_code_action` | Lọc theo QR code action đã thực hiện (is_action_web=1 hoặc 2) | `detail_landing_click` |
| Thông tin bạn bè | `friend_info` | Lọc theo trường thông tin tuỳ chỉnh. Default fields: system_name (d_1), phone (d_2), email (d_3). So sánh: 完全一致 (1), 部分一致 (2), 完全一致を含まない (3), 部分一致を含まない (4), 情報登録あり (5), 情報登録なし (6) | `line_user.view_name`, `line_user.phone_number`, `line_user.email`, `friend_information_value` |
| Trạng thái | `status_search` | Lọc theo `status_last_message` hoặc `id_status` của conversation | `conversation` |

- **Max execution time**: 180 giây
- [Confidence: **Cao**, file:227-600+]

---

### LineUser
- **File**: `app/LineUser.php`
- **Bảng DB**: `line_user`
- **Connection**: `mysql` (mặc định)

#### Relationships
| Relationship | Kiểu | Model liên quan | FK | Mô tả |
|-------------|------|----------------|-----|-------|
| `botLineUser()` | hasMany | `BotLineUser` | `line_user_id` → `id` | Liên kết bot-user |
| `tag_line_user()` | hasMany | `tagLineUser` | `line_user_id` → `id` | Tags gán cho user |

#### Trường quan trọng
| Trường | Mô tả |
|--------|-------|
| `id` | ID nội bộ |
| `line_id` | LINE user ID (string, vd: "U1234567890") |
| `name` | Tên hiển thị LINE |
| `real_name` | Tên thật (nếu có) |
| `view_name` | Tên hệ thống (system name) |
| `avatar_url` | URL avatar |
| `email` | Email |
| `phone_number` | Số điện thoại |

---

### StatusChat
- **File**: `app/StatusChat.php` (13 dòng)
- **Bảng DB**: `status_chat`
- **Connection**: `mysql` (mặc định)
- **Mô tả**: Danh sách trạng thái chat tuỳ chỉnh do Admin tạo cho bot. Dùng trong bộ lọc nâng cao.

---

### MessagesBotMapping
- **File**: `app/MessagesBotMapping.php` (13 dòng)
- **Bảng DB**: `messages_bot_mapping`
- **Connection**: `mysql_message`
- **Mô tả**: Mapping giữa bot và các bảng messages sharded theo năm. Dùng để xác định năm nào có dữ liệu khi phân trang qua nhiều bảng.

---

### CaptureTemplate
- **File**: `app/CaptureTemplate.php`
- **Bảng DB**: `capture_templates`
- **Connection**: `mysql_message`
- **Mô tả**: Template tin nhắn đã capture (lưu lại). Dùng trong `getDetailMessageTalkList()` khi tin nhắn có `source_message`.

#### Constants — Loại template
| Hằng số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `TYPE_MESSAGE_TEXT` | 1 | Văn bản |
| `TYPE_MESSAGE_BUTTONS` | 2 | Buttons/Menu |
| `TYPE_MESSAGE_IMAGE` | 3 | Hình ảnh |
| `TYPE_MESSAGE_VIDEO` | 4 | Video |
| `TYPE_MESSAGE_AUDIO` | 5 | Âm thanh |
| `TYPE_MESSAGE_STICKER` | 6 | Sticker |
| `TYPE_MESSAGE_IMAGE_MAP` | 7 | Image map |
| `TYPE_MESSAGE_LOCATION` | 8 | Vị trí |
| `TYPE_MESSAGE_INTRODUCTION` | 9 | Giới thiệu |

---

### SourceMessage
- **File**: `app/SourceMessage.php`
- **Bảng DB**: `source_messages`
- **Connection**: `mysql_message`
- **Mô tả**: Lưu nguồn gốc tin nhắn (action from, detail action). Liên kết 1-1 với `MessagesV2`. Chứa `list_capture_template_id` (danh sách ID capture templates, comma-separated).

---

## Services

### MessageService
- **File**: `app/Services/MessageService.php`
- **Dependencies**: `MessageV2RepositoryInterface`, `ConversationRepositoryInterface`, `CaptureTemplateRepositoryInterface`, `SourceMessageRepositoryInterface`

#### Method: createMessageV2()
- **Mô tả**: Tạo và gửi tin nhắn text qua LINE Push Message API
- **Input**: `$message` (array), `$bot`, `$lineUser`, `$conversationId`, `$is_count_sent`, `$isUpdateLastMess`, `$useSocket`, `$mobileUserSelectId`, `$optionalParams`
- **Output**: LINE API response object (có method `isSucceeded()`, `getRawBody()`)
- **Logic chi tiết**:
  1. Kiểm tra bot không null
  2. Lấy tên LINE user (ưu tiên `real_name` > `name`)
  3. Auto-refresh LINE channel access token (`autoRefreshToken()`)
  4. Build LINE message object (`buildMessageV2()`)
  5. Push message qua LINE Bot SDK (`pushMessage()`)
  6. Handle tạo record trong DB (`handleCreateMessage()`)
  7. Broadcast qua WebSocket nếu `useSocket = true`
- **Side effects**:
  - Gọi LINE Push Message API
  - Tạo record trong `messages_v2s`
  - Cập nhật conversation
  - WebSocket broadcast
- [Confidence: **Cao**, file:41-78]

---

### ConversationService
- **File**: `app/Services/ConversationService.php`
- **Sử dụng trong**: EP-03 (`getDetailMessageTalkList`) — method `isJson()` kiểm tra string có phải JSON không

---

### ConversationRepository
- **File**: `app/Repositories/Eloquents/ConversationRepository.php` (100 dòng)
- **Implements**: `ConversationRepositoryInterface`

#### Method: updateConversation()
- **Mô tả**: Cập nhật conversation theo ID
- **Input**: `$conversationId`, `$data` (array)
- **Logic**: `Conversation::where('id', $conversationId)->update($data)`
- **Sử dụng trong**: EP-05 — cập nhật `confirm_count` và `status_last_message`

---

## Form Requests / Validation

> **Không có FormRequest classes** cho các endpoint của TalkListController. Tất cả validation được thực hiện inline trong controller (kiểm tra null/empty). Không có validation rules tường minh. [Confidence: **Cao**]

---

## Events & Listeners

### Event: InfoEvent
- **File**: `app/Events/InfoEvent.php`
- **Implements**: `ShouldBroadcast`
- **Trigger bởi**: `changeStatusMessage()` (EP-05)
- **Payload**:
  - `$totalUserConfirmMessage` — số conversation chưa xác nhận
  - `$totalErrorMessage` — số lỗi tin nhắn chưa xử lý
  - `$totalGroupConfirmMessage` — số group chưa xác nhận
  - `$botId` — ID bot
- **Channel**: `info`
- **Event name**: `total`

> **Ghi chú**: Event này broadcast realtime qua WebSocket (Pusher/Socket.IO) để cập nhật badge count trên giao diện Admin portal. [Confidence: **Cao**]

---

## Authorization

| Quyền | Kiểm tra ở đâu | Logic | Ảnh hưởng |
|-------|----------------|-------|----------|
| Truy cập Talk List page | Middleware `basic_access` | Kiểm tra user đã đăng nhập và có quyền truy cập Basic portal | Admin/Staff không có quyền sẽ bị redirect |
| Truy cập AJAX endpoints | Middleware `check_login` | Kiểm tra session đăng nhập hợp lệ | Trả 401/redirect nếu chưa đăng nhập |
| Bot ID scope | `getBotId()` (session) | Tất cả query đều filter theo `bot_id` từ session | Chỉ xem được tin nhắn của bot đang chọn |
| Hết hạn tài khoản | Middleware `is_expire` | Kiểm tra bot/tài khoản chưa hết hạn | Chỉ áp dụng cho EP-01 (trang chính) |

> **Ghi chú**: Không có kiểm tra permission cấp Staff (vd: Staff có quyền xem Talk List không, có quyền thay đổi trạng thái không). Quyền truy cập phụ thuộc hoàn toàn vào middleware `basic_access` và cấu hình role của Staff tại admin level. [Confidence: **Trung bình**]

---

## Business Rules tổng hợp

| # | Rule | Mô tả | Nơi implement | Confidence |
|---|------|-------|--------------|-----------|
| 1 | **Trạng thái xác nhận dựa trên unconfirm_message** | Tin nhắn được coi là「未確認」khi có record trong `unconfirm_message`. Khi đánh dấu「確認済」, record bị xoá (không phải cập nhật flag). Ngược lại, đánh dấu「未確認」sẽ tạo record mới. | `TalkListController@changeStatusMessage` (file:283-321) | **Cao** |
| 2 | **Messages sharding theo năm** | Tin nhắn được lưu trong nhiều bảng: `messages_v2s` (mới nhất), `messages` (mặc định), `messages2020`..`messages2025` (sharded theo năm), `messages_page2`, `messages_old` (legacy). Truy vấn ưu tiên V2 → Messages theo năm giảm dần. | `BotLineUser::makeDataTalkList()` (file:18-124) | **Cao** |
| 3 | **Phân trang lazy load, mỗi lần 100 records** | Không dùng pagination truyền thống. Client gửi `offset` + `currentYear` + `isLoadMsgNew` → server trả 100 records tiếp theo, có thể span qua nhiều bảng. `flagEnd` báo hiệu còn dữ liệu cũ hơn hay không. | `BotLineUser::makeDataTalkList()` (file:37,51-78) | **Cao** |
| 4 | **Mặc định ẩn tin nhắn dạng 【〇〇】 và sticker** | Nếu `condition_message` không chứa flag tương ứng, query tự động thêm `WHERE content NOT LIKE '【%】' AND type != 'sticker'`. User phải bật checkbox trong modal filter để xem. | `BotLineUser::getListMessagesV2()` (file:257-268) | **Cao** |
| 5 | **Giới hạn gửi tin miễn phí: 1000 tin** | Bot free plan (`plan_type = 2`) bị giới hạn 1000 tin nhắn gửi đi. Khi `free_send_count >= 1000` → trả lỗi `limit_max`. Counter tăng +1 mỗi lần gửi thành công. | `TalkListController@ajaxTalkSendMessage` (file:203-219) | **Cao** |
| 6 | **Sync Elasticsearch khi thay đổi trạng thái** | Khi `confirm_count` của conversation thay đổi → ghi record vào `sync_elasticsearch` để đồng bộ dữ liệu tìm kiếm. | `TalkListController@changeStatusMessage` (file:344-352) | **Cao** |
| 7 | **Badge update qua FCM + WebSocket** | Sau khi thay đổi trạng thái: cập nhật `bots.count_user_unconfirm`, gửi FCM push notification cập nhật badge trên mobile, broadcast `InfoEvent` qua WebSocket cập nhật realtime trên web. | `TalkListController@changeStatusMessage` (file:355-361) | **Cao** |
| 8 | **Filter nâng cao dùng chung logic Conversation::advanceFilterPost()** | Bộ lọc nâng cao (tag, friend_name, day_add_friend, scenario, conversion, qr_code, friend_info) sử dụng cùng method `advanceFilterPost()` — được dùng chung bởi nhiều tính năng (broadcast, friend list, talk list). Đây là shared component SC-003 (Friend Filter/Segment). | `Conversation::advanceFilterPost()` (file:227+) | **Cao** |
| 9 | **Chỉ tin nhắn từ bạn bè (msg_kind=1) khi lọc "reception"** | Tab mặc định「一覧」gửi `status=[0]` tương ứng config `reception`. Query thêm `WHERE msg_kind = 1` — chỉ hiển thị tin nhắn bạn bè gửi, không hiển thị tin bot/admin/scenario gửi. | `BotLineUser::getListMessagesV2()` (file:244-245) | **Cao** |
| 10 | **Checkbox「返信を含める」bao gồm tin gửi** | Khi check, client gửi `status=[0,1]`, tương ứng `reception` + `send`. Khi `send` có mặt, query dùng `WHERE msg_kind != KIND_MESSAGE_SCENARIO` thay vì `msg_kind = 1` — bao gồm tin bot gửi nhưng loại trừ scenario. | `BotLineUser::getListMessagesV2()` (file:249-252) | **Cao** |
| 11 | **Detail message chỉ từ MessagesV2** | `getDetailMessageTalkList()` chỉ truy vấn bảng `messages_v2s`. Tin nhắn cũ từ bảng legacy (messages, messagesPage2, messagesOld) sẽ không hiển thị được chi tiết. | `TalkListController@getDetailMessageTalkList()` (file:394-396) | **Cao** |

---

## Cấu hình liên quan (config/sns-line.php)

### status_talk_list
```php
'status_talk_list' => [
    'reception' => 0,    // Tin nhận (bạn bè gửi)
    'send' => 1,         // Tin gửi (bot/admin gửi)
    'follow' => 2,       // Follow events
    'notification' => 3,  // Notifications
    'not_confirmed' => 4  // Chưa xác nhận
]
```

### status_filter_message
```php
'status_filter_message' => [
    'button' => 1,   // Tin nhắn dạng【〇〇】(media markers)
    'sticker' => 2   // Sticker/Stamp
]
```

---

## Ghi chú kiến trúc quan trọng

### Message Tables Architecture
```
messages_v2s (mysql_message)          ← Tin nhắn MỚI NHẤT, ưu tiên query trước
    ↓ (nếu không đủ)
messages (mysql_message)              ← Tin nhắn mặc định (currentYear=0)
messages2025 (mysql_message)          ← Sharded theo năm 2025
messages2024 (mysql_message)          ← Sharded theo năm 2024
messages2023 (mysql_message)
messages2022 (mysql_message)
messages2021 (mysql_message)
messages2020 (mysql_message)
messages_page2 (mysql_message)        ← Tin nhắn cũ (page 2)
messages_old (mysql_message)          ← Tin nhắn cổ nhất

messages_bot_mapping (mysql_message)  ← Mapping bot ↔ năm có dữ liệu
```

### Confirm/Unconfirm Architecture
```
unconfirm_message ←→ conversation ←→ bots
       │                    │              │
       │ message_id         │ confirm_count│ count_user_unconfirm
       │ conversation_id    │ status_last_ │
       │ bot_id             │   message    │
       │                    │              │
    Tạo = 未確認         0 = all confirmed  Đếm conversations
    Xoá = 確認済         1 = has unconfirm  có confirm_count=1
```

### WebSocket/Realtime Flow
```
changeStatusMessage()
    → cập nhật DB
    → updateBadge() → FCM push notification → Mobile app badge
    → InfoEvent broadcast → WebSocket → Web UI badge/counter update
```
