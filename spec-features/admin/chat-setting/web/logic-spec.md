# Logic Spec — FA-041 Cài đặt chat 「チャット設定」

> Dựa trên source `src/web/sns-line/` (Laravel 5.5). Reference tất cả bằng `file:line`.

## 1. Controllers & Actions

### 1.1. `Basic\BasicController@chatSetting`
- **File**: `src/web/sns-line/app/Http/Controllers/Basic/BasicController.php:2710-2713`
- **Logic**: trả view Blade `resources/views/basic/chat_setting.blade.php`. Không load data server-side — toàn bộ dữ liệu được load qua AJAX từ phía Vue.
- **Side effect**: không có.

### 1.2. `ChatController@getDataSettingChat`
- **File**: `src/web/sns-line/app/Http/Controllers/ChatController.php:3930-3948`
- **Logic**:
  1. Gọi helper `getBotId()` lấy `bot_id` từ session.
  2. `Bots::find($botId)` → nếu null → `redirect()->route('adminIndex')` (chú ý: AJAX endpoint mà redirect HTML → FE sẽ nhận 302 và JS không xử lý case này).
  3. Trả JSON với 10 field cấu hình (xem `api-spec.md` EP-02).
- **Bất thường**: JSON response nhưng fallback là redirect HTML.

### 1.3. `ChatController@saveSettingChat`
- **File**: `src/web/sns-line/app/Http/Controllers/ChatController.php:3950-3961`
- **Logic**:
  ```php
  public function saveSettingChat(Request $request){
      addLogUserAction("saveSettingChat");
      $botId = getBotId();
      Bots::where('id', $botId)->update($request->all());
      return response()->json(['success' => true, 'message' => '']);
  }
  ```
- **Side effect**: 1 UPDATE bảng `bots`.
- **⚠ Rủi ro bảo mật (Cao)**: Mass assignment không giới hạn — xem mục Business Rules #BR-03.
- **Không có** validation, không có try/catch, không có transaction.

### 1.4. `ChatController@ajaxGetStatusChatV2`
- **File**: `ChatController.php:624-638`
- **Logic**:
  - Filter theo `bot_id` từ session.
  - Order by `position ASC, id DESC`.
  - Paginate bằng `per_page` từ request (default 100).
- **Response**: `{success, data: {status: Paginator, hasMorePage}}`.

### 1.5. `ChatController@ajaxGetStatusChat` (legacy)
- **File**: `ChatController.php:612-622`
- **Logic**: giống 1.4 nhưng không phân trang.

### 1.6. `ChatController@ajaxSaveItemStatusV2`
- **File**: `ChatController.php:691-723`
- **Logic**:
  1. Duyệt `$request->input('data')` (mảng).
  2. Với mỗi item: nếu có `id` → UPDATE theo `(id, bot_id)`; nếu không → CREATE.
  3. Gán `position = $key` (index mảng bắt đầu từ 0).
  4. Gán `is_save = 1` (cờ không rõ ý nghĩa, luôn bằng 1).
  5. Log action qua `addLogUserAction("ajaxSaveItemStatus")` (⚠ cùng tên với EP-07).
- **Bất thường**: Không dùng transaction — code `DB::beginTransaction()` bị comment. Nếu fail giữa chừng → list inconsistent.
- **Không có** validation server-side.

### 1.7. `ChatController@ajaxSaveItemStatus` (legacy — lưu 1 item)
- **File**: `ChatController.php:654-689`
- **Logic đặc biệt**:
  - Create flow: `position` của các bản ghi cũ +=1 qua loop `foreach ($listStatus)` → rồi insert item mới ở `position=1`. Logic shift toàn bộ — O(N) update mỗi lần thêm.
  - Edit flow: UPDATE theo `(id, bot_id)`.
- **Bất thường**: `foreach` update từng record để shift thay vì 1 UPDATE bulk — performance kém.

### 1.8. `ChatController@ajaxSaveAllStatus` (legacy — có validate)
- **File**: `ChatController.php:725-770`
- **Validate server-side duy nhất** trong nhóm status endpoints:
  | Check | Line | Msg |
  |-------|------|-----|
  | `empty($item->name_status)` | `ChatController.php:734` | `ステータス必ず指定してください。` |
  | `mb_strlen > 10` | `ChatController.php:737` | `ステータス名は10文字以下にしてください。` |
  | `empty($item->color)` | `ChatController.php:740` | `カラー必ず指定してください。` |
- **Bất thường #2**: giới hạn 10 ký tự ở đây, nhưng UI v2 counter là 20, và EP-06 không check → 3 nguồn không nhất quán.

### 1.9. `ChatController@ajaxSortStatusChat` (legacy)
- **File**: `ChatController.php:771-787`
- **Logic**: Loop `$request->order`, update `position = $key + 1` cho từng id.
- **⚠ Thiếu filter `bot_id`** — rủi ro IDOR (xem Business Rules #BR-04).

### 1.10. `ChatController@ajaxDeleteItemStatus`
- **File**: `ChatController.php:789-826`
- **Logic**:
  1. Tìm `StatusChat` theo `(id, bot_id)` (⚠ `$dataStatus` được query rồi log, nhưng **không dùng để chặn** nếu null).
  2. `Conversation::where('bot_id', $botId)->where('id_status', $id)->get()` → danh sách hội thoại đang dùng status này.
  3. Loop → insert bản ghi `sync_elasticsearch` với `type = config('sns-line.type_sync.update')`, `data_sync = {"status_id": null}`.
  4. Hard DELETE `status_chat WHERE id = ? AND bot_id = ?`.
  5. Bulk UPDATE `conversation SET id_status = NULL WHERE bot_id = ? AND id_status = ?`.
- **Side effect**:
  - Xoá record `status_chat`.
  - SET NULL `conversation.id_status`.
  - Tạo nhiều bản ghi `sync_elasticsearch` → trigger background job re-index ES.
- **Không có** confirm/cảnh báo khi status đang được gán cho N conversation.

---

## 2. Models Eloquent

### 2.1. `App\StatusChat`
- **File**: `src/web/sns-line/app/StatusChat.php`
- **Table**: `status_chat`
- **Guarded**: `[]` → mass-assignable toàn bộ.
- **Timestamps**: `true`.
- **Relationships**: không khai báo. Thực tế dùng với `Conversation.id_status` (FK ngầm).
- **Schema suy ra từ migrations** (`2021_12_29_160218`, `2022_01_10_155502`, `2022_11_07_180737`):
  | Column | Type | Default | Ghi chú |
  |--------|------|---------|---------|
  | `id` | UNSIGNED INT AUTO | | PK |
  | `bot_id` | INT | | FK → `bots.id` (không constraint) |
  | `position` | INT | 0 | Thứ tự hiển thị |
  | `name_status` | VARCHAR(255) | | Tên status (UI giới hạn 20 ký tự, EP-08 validate 10) |
  | `color` | VARCHAR(255) | | Hex color (vd `#F44336`) |
  | `bg_status` | VARCHAR(255) | null | Màu nền chip |
  | `bg_choose` | VARCHAR(255) | null | Màu nền khi chọn |
  | `is_save` | TINYINT | 1 | Luôn bằng 1 trong code |
  | `count` | INT | 0 | Không thấy controller cập nhật — có thể do Spring Boot job đếm số conversation |
  | `created_at` / `updated_at` | TIMESTAMP | CURRENT_TIMESTAMP | |

### 2.2. `App\Bots`
- **File**: `src/web/sns-line/app/Bots.php`
- **Table**: `bots`
- **Guarded**: `[]` → ⚠ mass-assignable toàn bộ (xem BR-03).
- **Relationships khai báo**: `Individuals`, `landingPages`, `Affiliates`, `AffResults`, `affFee`, `bot_line_users`, `botServices`, ...
- **Các cột liên quan FA-041 (từ migrations và tham chiếu code)**:
  | Column | Type | Default | Nguồn migration | Dùng ở tab |
  |--------|------|---------|----------------|-----------|
  | `confirm_message_button` | TINYINT | 0 | `2021_12_31_165649_add_bots_to_users_table` | Tab 2 |
  | `confirm_message_autoreply` | TINYINT | 0 | `2021_12_31_165649` | Tab 2 (cũ, bị comment trong view) |
  | `confirm_message_stamp` | TINYINT | 0 | `2022_11_22_181942_add_col_setting_chat_bot_table` | Tab 2 |
  | `setting_shortcut` | TINYINT | 0 | `2022_11_22_181942` | Tab 3 (`0` Shift+Enter; `1` Enter) |
  | `confirm_message_user_send` | TINYINT | 0 | `2024_09_19_153216_add_column_chat_setting_to_bots` | Tab 2 toggle 1 |
  | `confirm_message_user_block_bot` | TINYINT | 0 | `2024_09_19_153216` | Tab 2 toggle 2 |
  | `preview_after_send` | TINYINT | 1 | `2024_09_19_153216` | Tab 5 |
  | `confirm_message_autoreply_all` | TINYINT | 0 | `2026_03_19_190550_add_col_confrim_autoreply_to_bots_table` | Tab 2 |
  | `confirm_message_autoreply_specified` | TINYINT | 0 | `2026_03_19_190550` | Tab 2 |
  | `is_shorten_url` | TINYINT | — | (từ bảng `bots`, migration khác — cột đã có trước) | Tab 4 |
  | `count_user_unconfirm` | INT | — | (cột đếm đã có sẵn) | (side effect của `confirm_message_user_send`) |
  | `last_time_count_user_confirm` | DATETIME | — | | |

### 2.3. `App\Conversation`
- **File**: `src/web/sns-line/app/Conversation.php`
- **Liên quan FA-041**: column `id_status` (FK ngầm → `status_chat.id`) bị cập nhật NULL khi xoá status (`ChatController.php:814`).

### 2.4. `App\SyncElasticsearch`
- **Dùng tại**: `ChatController.php:805` (insert để trigger re-index ES).
- **Ghi chú cho job-analyzer**: bảng queue đồng bộ ES — Spring Boot job có thể consume bảng này.

---

## 3. Services / Helpers / Repositories

### 3.1. Helper `getBotId()`
- Hàm global, trả về `bot_id` của bot đang được chọn trong session.
- Dùng xuyên suốt 10 controller methods của FA-041.

### 3.2. Helper `addLogUserAction($action)`
- Global log helper — ghi hoạt động user vào log nội bộ (không ảnh hưởng dữ liệu nghiệp vụ).

### 3.3. `SyncElasticsearch::insertElasticsearch()`
- **Dùng tại**: `ChatController.php:805`.
- **Vai trò**: đẩy event vào bảng `sync_elasticsearch` để background job đồng bộ dữ liệu tới Elasticsearch.
- **Payload**:
  ```php
  [
      'type' => config('sns-line.type_sync.update'),  // const int
      'line_user_id' => $conver->line_id,
      'bot_id' => $current_bot_id,
      'data_sync' => json_encode(['status_id' => null])
  ]
  ```

### 3.4. `ChatService` (consumer của `confirm_message_user_send`)
- **File**: `src/web/sns-line/app/Services/ChatService.php`
- **Các method dùng flag**: `ChatService.php:104, 170, 342` — Sau khi admin gửi tin nhắn thành công (LINE API OK), nếu `$bot->confirm_message_user_send == 1` → gọi `totalUserConfirmMessage($bot->id)` rồi `UPDATE bots SET count_user_unconfirm = ?, last_time_count_user_confirm = NOW() WHERE id = ?`.
- **Ngữ nghĩa**: flag `confirm_message_user_send` ở BE bị dùng như trigger **đếm lại** số unread thay vì "auto mark as read" như tên gợi ý. Semantic có thể khác — xem BR-05.

### 3.5. Helper `is_shorten_url` (Tab 4)
- **Dùng tại**: `app/Helpers/functions.php:7944`, `app/Helpers/ChatMessages.php` (nhiều chỗ: 2340, 2376, 2035, ...).
- **Vai trò**: Khi gửi tin nhắn trong 1:1 Chat mà có URL trong template → nếu `$bot->is_shorten_url == 1` → rút gọn URL qua hệ thống shorten của LME (xem FA-024). Cross-reference FA-024 URL Analysis.

### 3.6. Frontend usage `preview_after_send`
- **Dùng tại**: `public/js/chats/chat-v2.js:3237, 3244, 3250, 3584-3589`.
- **Vai trò**: Logic phía client — nếu `preview_after_send == 1` thì mở modal preview trước khi gọi API gửi. BE không ép buộc, hoàn toàn client-side check.

### 3.7. Frontend usage `setting_shortcut`
- **Dùng tại**: `public/js/chats/chat.js:4237` và `chat-v2.js:5689`.
- **Vai trò**: Client-side keybinding handler — `setting_shortcut == 1` → Enter submit; khác → Shift+Enter submit. Không ảnh hưởng server.

---

## 4. Form Requests / Validation

**KHÔNG CÓ FormRequest class nào** cho nhóm endpoints FA-041. Tìm kiếm:
```
grep ChatSetting | ChatStatus | StatusChat → app/Http/Requests/*  = không match
```

**Validation thực tế**:
| Endpoint | Server validation | Client validation |
|----------|-------------------|-------------------|
| EP-03 `save-data-setting` | Không có | Không có |
| EP-06 `save-item-status-v2` | Không có | `setting_color.js:52-60` — name_status không rỗng, ≤20 ký tự |
| EP-08 `save-all-status` (legacy) | Có (xem 1.8) | — |
| EP-10 `delete-item-status` | Chỉ check `bot_id` owner khi delete (không chặn khi không tìm thấy) | Modal confirm (xem UI) |

---

## 5. Events / Listeners / Queued Jobs

### 5.1. Laravel Queue/Job
- **Không phát hiện** `dispatch()`, `Queue::push()`, hay `ShouldQueue` trong chain code của FA-041.
- **Không có** Laravel Event/Listener cho `StatusChat` CRUD.

### 5.2. Background jobs ngoài Laravel (⚠ quan trọng cho job-analyzer)

#### 5.2.1. Auto-confirm khi LINE gửi webhook message (Spring Boot)
**Các flag không được Laravel consume:**
- `confirm_message_button`
- `confirm_message_stamp`
- `confirm_message_autoreply_all`
- `confirm_message_autoreply_specified`
- `confirm_message_user_block_bot`

**Grep toàn bộ `app/`** cho các tên này cho thấy chỉ `getDataSettingChat` và `saveSettingChat` (2 method) đụng vào. Không có controller/service/job nào của Laravel áp dụng logic mark-as-read dựa trên các flag này.

→ **Kết luận**: 5 flag trên phải được **Spring Boot job** đọc khi nhận LINE webhook (`callback`) và áp dụng logic đánh dấu `is_confirmed = 1` / `confirmed_at = NOW()` trên bảng messages.

**Ghi chú cho `job-analyzer`** (`src/job/`):
| Flag | Event LINE | Hành vi kỳ vọng |
|------|-----------|----------------|
| `bots.confirm_message_button` | webhook `message` dạng button/marker template | Đánh dấu confirmed ngay khi lưu message |
| `bots.confirm_message_stamp` | webhook `message` type = sticker | Đánh dấu confirmed |
| `bots.confirm_message_autoreply_all` | webhook `message` match auto-reply trigger「すべて」(FA-003) | Đánh dấu confirmed |
| `bots.confirm_message_autoreply_specified` | webhook `message` match auto-reply trigger「キーワード」(FA-003) | Đánh dấu confirmed |
| `bots.confirm_message_user_block_bot` | webhook `unfollow` / `block` event | Đánh dấu toàn bộ unread của line_user_id thành confirmed |

**Bảng cần kiểm tra**: `messages`, `messages_{year}` (sharded theo năm — xem `sns-line/CLAUDE.md` phần Database), cột khả dĩ: `is_confirmed`, `confirmed_at`, `read_at`.

**Entry point có thể**: `src/job/` controller nhận LINE webhook callback → xử lý theo type.

#### 5.2.2. Trigger re-index Elasticsearch khi xoá status
- Code Laravel insert vào bảng `sync_elasticsearch` (`ChatController.php:805`).
- Spring Boot job đọc bảng này, gọi ES API update document với `status_id = null`.
- Bảng: `sync_elasticsearch` (cần verify tên exact trong DB index).
- Trigger condition: `type = config('sns-line.type_sync.update')` và `data_sync.status_id = null`.

#### 5.2.3. Count user unconfirm (Laravel-side, không phải job)
- `confirm_message_user_send == 1` → ChatService tự UPDATE `bots.count_user_unconfirm` + `last_time_count_user_confirm` mỗi lần admin gửi message. Đồng bộ (synchronous), không qua queue.

---

## 6. Middleware & Authorization

### 6.1. Middleware applied
| Route nhóm | Middleware |
|-----------|-----------|
| `/basic/chat-setting` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` (group line 823 của `web.php`) |
| `/ajax/*` (tất cả endpoints AJAX của tính năng) | `check_login`, `check_remember_token` (group line 2324 của `web.php`) |

- `basic_access`: kiểm tra đã đăng nhập với role admin/staff của bot.
- `check_login`: kiểm tra session login cơ bản (không kiểm role).
- `is_expire`: kiểm tra gói bot chưa hết hạn.
- `check_remember_token`: kiểm tra remember_token cookie khớp.

### 6.2. Authorization cấp Staff permission
- **KHÔNG có** middleware hay kiểm tra permission custom role trong controller. Bất kỳ user nào đăng nhập bot (admin hoặc staff) đều có thể:
  - Xem tất cả setting (EP-02)
  - Đổi tất cả setting (EP-03)
  - CRUD status (EP-04..EP-10)
- UI spec FA-041 ghi: "Staff có quyền nếu custom role cho phép" — thực tế điều này **phải do FE ẩn menu** chứ không có BE enforcement. Cần cross-check với FA-036 Staff Management.
- **⚠ Flag #BR-06**: thiếu authorization cấp staff.

### 6.3. CSRF
- JS `chat_setting/index.js:1-6` set header `X-CSRF-TOKEN` cho mọi request. Laravel middleware `VerifyCsrfToken` áp dụng mặc định cho `web` group.

---

## 7. Business Rules

### BR-01 — Status thuộc về bot
- Mỗi `status_chat` có `bot_id`; query luôn filter theo `bot_id` khi list/update/delete (trừ EP-09).
- **Nguồn**: `ChatController.php:627, 668, 710, 755, 795, 813`.

### BR-02 — Xoá status = SET NULL conversations
- Khi xoá `status_chat`, tất cả `conversation.id_status` trỏ tới status đó được SET NULL (`ChatController.php:814-816`).
- Không có cascade constraint DB — cascade thủ công qua code.
- Không có cảnh báo UI/BE: status đang dùng vẫn xoá được.

### BR-03 — Mass assignment trên `bots` (Nghiêm trọng)
- `saveSettingChat` dùng `Bots::where('id', $botId)->update($request->all())` (`ChatController.php:3959`).
- `$guarded = []` ở model `Bots` (`Bots.php:15`).
- Không có FormRequest, không có validate.
- **Hậu quả**: client có thể gửi thêm bất kỳ field nào của bảng `bots` và được ghi đè (vd: `admin_id`, `plan_type`, `free_send_count`, `is_active`, `line_channel_secret`, ...).
- **Đề xuất**: whitelist qua FormRequest hoặc dispatch mapping rõ ràng.

### BR-04 — Thiếu `bot_id` filter ở EP-09 `sort-status-chat` (Trung bình)
- `ChatController.php:775-779`: loop update `position` theo `id` duy nhất, không kèm điều kiện `bot_id`.
- Nếu attacker biết `id` status của bot khác → có thể đổi `position` của status đó.
- **Đề xuất**: thêm `->where('bot_id', getBotId())`.

### BR-05 — Semantic flag `confirm_message_user_send`
- Tên flag gợi "auto mark as read when reply", nhưng code Laravel thực chất là trigger update counter unread (`ChatService.php:104`).
- Việc mark-as-read thực sự có thể do BE khác (Spring Boot) hoặc FE xử lý; hoặc flag có semantic kép. Cần job-analyzer verify.

### BR-06 — Không có authorization cấp Staff permission (Trung bình)
- BE chỉ kiểm tra đã login và thuộc bot, không kiểm custom role.
- Xem mục 6.2.

### BR-07 — Validation không nhất quán giữa các endpoints (Thấp)
- EP-06 (hiện dùng): không validate.
- EP-08 (legacy): validate `name_status` ≤ **10** ký tự.
- UI v2: counter **20** ký tự.
- → 3 nguồn validation không nhất quán. UI cho nhập tối đa 20 nhưng endpoint cũ sẽ reject > 10.

### BR-08 — Position bắt đầu từ 0 (EP-06) vs 1 (EP-07, EP-08, EP-09) (Thấp)
- EP-06 dùng index mảng `$key` trực tiếp → position đầu = 0.
- EP-07: position đầu = 1.
- EP-08: position = `$key + 1`.
- EP-09: position = `$key + 1`.
- → Nếu user vừa dùng UI v2 (EP-06), rồi vào UI cũ (FA-001) sort bằng EP-09, position sẽ bị thay đổi 1-based. Inconsistent.

### BR-09 — Không transaction khi save bulk status
- EP-06 (`ajaxSaveItemStatusV2`): `DB::beginTransaction()` bị comment — nếu fail giữa loop → một số item đã update, một số chưa.

### BR-10 — Hard delete, không soft delete
- `StatusChat::where(...)->delete()` (`ChatController.php:813`) — hard delete.
- Model không dùng `SoftDeletes` trait.

---

## 8. Files tham khảo chính (absolute)
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/routes/web.php:1648` — route view
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/routes/web.php:3019-3106` — routes AJAX
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/app/Http/Controllers/ChatController.php:612-826, 3930-3961` — toàn bộ logic controller
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/app/Http/Controllers/Basic/BasicController.php:2710-2713` — render view
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/app/StatusChat.php` — Model
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/app/Bots.php` — Model
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/app/Services/ChatService.php:104, 170, 342` — consumer `confirm_message_user_send`
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/database/migrations/2021_12_29_160218_create_status_chat_table.php`
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/database/migrations/2022_11_07_180737_add_position_status_chat_table.php`
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/database/migrations/2024_09_19_153216_add_column_chat_setting_to_bots.php`
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/database/migrations/2026_03_19_190550_add_col_confrim_autoreply_to_bots_table.php`
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/public/js/chat_setting/index.js` — FE tab 2-5
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/public/js/chat_setting/setting_color.js` — FE tab 1
- `c:/xampp/htdocs/lme-reveser-spec/src/web/sns-line/resources/views/basic/chat_setting.blade.php` — Blade view
