# Logic Spec — FA-028 「配信エラー」 (Lỗi phát hành / Error message)

- **Portal**: Admin (LINE OA)
- **Nguồn**: Laravel 5 + PHP 7.2 — `src/web/sns-line/`
- **Mức độ tin cậy tổng thể**: **Cao** (đọc trực tiếp controller, model, job, config, view, JS)

---

## 1. Controllers và Actions

> **Phạm vi mục này**: hai controller dưới đây **chỉ đọc, cập nhật và xoá** bảng `message_error` — chúng **không sinh** bản ghi lỗi. Nguồn sinh dữ liệu nằm ở nơi khác (Spring Boot + **11 lệnh `create()` trong 7 file** phía Laravel) — xem **§2.4**, **BR-25** và **BR-26**.
> Ngoại lệ duy nhất trong 2 controller: `Basic\SalesManagementV2Controller` cũng ghi `message_error` (`:4506`) nhưng thuộc tính năng khác, không thuộc FA-028.

### 1.1. `Basic\MessageErrorController` (v2 — controller chính)

File: `app/Http/Controllers/Basic/MessageErrorController.php` (1.067 dòng)

| Method | Dòng | Vai trò | Side effects |
|--------|------|---------|--------------|
| `index()` | `:52-60` | Render view `basic.error_list.v2.index`, truyền `config('sns-line.table_error_code')` | Không |
| `getListHistorySend(Request)` | `:61-155` | Lấy danh sách tab 「再送済み履歴」 — truy vấn **trực tiếp `sending_schedule_setting`** | Không |
| `ajaxGetMessageError(Request)` | `:157-343` | Lấy danh sách chính theo tab × nguồn; uỷ quyền cho `getListHistorySend()` khi tab = `history_send` | Không (chỉ đọc) |
| `getEndCode($message_error)` — private | `:345-376` | Suy mã lỗi 001–007/`other` từ chuỗi `error_message` bằng `strpos` | Không |
| `checkIsJson($content)` — private | `:378-382` | Kiểm tra content có phải JSON | Không |
| `getDataPreviewMessage(Request)` | `:384-529` | Dựng dữ liệu modal 「エラーメッセージ詳細」 | Không |
| `handleMessageErrorFromSourceMessage(int)` — private | `:531-554` | Dựng preview từ `source_messages` (kịch bản nhiều bong bóng) | Không |
| `handleMessageErrorFromTemplate(array)` — private | `:556-575` | Dựng preview từ danh sách `template_id` | Không |
| `handleMessageErrorFromMessage($message)` — private | `:577-692` | Convert 1 bản ghi `messages`/`messages_v2s` sang object `Template` để preview | Không |
| `getActionDetailByActionId($actionId)` | `:694-711` | Lấy chi tiết action — **public nhưng không có route**, chỉ gọi nội bộ | Không |
| `ajaxDeleteErrorMessage(Request)` | `:713-805` | Xoá bản ghi lỗi (tab `unconfirm`) hoặc huỷ đăng ký gửi lại (2 tab còn lại) | **Có** — xem §8 |
| `splitDomain($url)` — private | `:807-822` | Tách `image_server` và path từ URL ảnh | Không |
| `covertDisplayPC($is_display_pc)` | `:824-831` | Trả nhãn mặc định 「メッセージをご確認ください」 | Không |
| `saveSettingErrorMessage(Request)` | `:833-981` | Đăng ký gửi lại / gửi ngay / xoá **1 bản ghi** | **Có** — xem §8 |
| `saveSettingErrorMessageAll(Request)` | `:983-1051` | Thao tác hàng loạt; dispatch queued job khi `selectAll = true` | **Có** — xem §8 |
| `updateTimeSend(array, string)` — private | `:1053-1066` | Chỉ cập nhật `send_time` cho lịch đã đăng ký (tab `registered_send`) | **Có** |

**Import không sử dụng** (mức tin cậy **Cao**, kiểm tra bằng grep toàn file): `App\Events\InfoEvent` (`:39`), `Vinkla\Hashids\Facades\Hashids` (`:48`), `App\MessagesOld` (`:19`), `App\MessagesPage2` (`:20`), `App\SendingScheduleSetting` — có dùng, `App\Services\ConversationService` (dùng 1 lần tại `:679`), `App\Services\Templates\TemplateV2Service` (dùng tại `:558`, `:601`). Các model `Actions`, `ActionDetail`, `DetailActionSlot`, `ImageMap`, `ImageMapItems`, `TmpButton`, `TmpIntroduction`, `TmpLocation`, `Conversion`, `Tag`, `Category`, `Bots` chủ yếu phục vụ các private helper dựng preview.

#### Logic chi tiết `ajaxGetMessageError()` (`:157-343`)

1. Đọc `error_tab`, `error_type`, `per_page` từ request — **không validate** (`:159-161`).
2. Nếu `error_tab == 'history_send'` → chuyển hướng sang `getListHistorySend()` và return sớm (`:163-165`).
3. Query gốc trên `message_error` (`:168-170`):
   - `bot_id = getBotId()`
   - `status != MessageError::STATUS_HANDLED['WAITING']` (tức `!= 1`) — loại bỏ bản ghi đang chờ job xử lý
   - `error_message NOT IN (' Failed to send messages', 'Failed to send messages')` — loại lỗi rác không có nội dung tiếng Nhật
4. Lọc theo nguồn (`:172-179`) — xem bảng ánh xạ trong api-spec §3.2.
5. Lọc theo tab (`:181-217`):
   - `registered_send`: LEFT JOIN `sending_schedule_setting`, `is_sent = 0`, `send_type = 1`, sort `send_time ASC`
   - `history_send`: (nhánh này thực tế **không bao giờ chạy** vì đã return ở bước 2 — **dead code**, tin cậy **Cao**)
   - mặc định (`unconfirm`): `sending_schedule_id IS NULL`
6. `$totalNotRetry` = đếm bản ghi có `status NOT IN (100, 101)` — số bản ghi được phép tick chọn (`:219-220`).
7. Phân trang `paginate($perPage)` với `orderByDesc('id')` + eager load `lineUser` (`:221`).
8. Chỉ khi tab = `unconfirm` mới tính 4 badge `totalXxxUnConfirm` bằng 4 query `count()` riêng biệt (`:223-234`) → **N+4 query, không cache** (tin cậy **Cao**).
9. Vòng lặp làm giàu từng bản ghi (`:238-338`) — xem §3 về cơ chế bảng messages phân mảnh.
10. Trả JSON kèm `PaginationResource` (`:340-342`).

#### Logic chi tiết `getListHistorySend()` (`:61-155`)

- Nguồn dữ liệu **đảo hẳn**: `SendingScheduleSetting::query()->select('*', 'type_error as type')` (`:69-72`).
- Lọc `bot_id`, `type_error` theo `error_type`, `is_sent = 1` (`:83-84`).
- **Sort mâu thuẫn**: `orderBy('send_time','asc')` tại `:84` bị ghi đè bởi `orderByDesc('id')` tại `:87` — thứ tự thực tế là theo `id` giảm dần. Tin cậy **Cao**.
- Nội dung tin nhắn **chỉ** lấy từ `Template` qua `template_ids` (`:108-110`) — không dò các bảng `messages*`.
- Các `totalXxxUnConfirm` trả về **hard-code `0`** (`:149-152`) → badge không hiển thị ở tab này.

#### Logic chi tiết `saveSettingErrorMessage()` (`:833-981`)

```
1. Đọc type, date_send, time_send, message_error_id                     :834-837
2. $messageError = MessageError::find($message_error_id)                :843   ← KHÔNG lọc bot_id
3. $message = MessagesV2::find(message_id) ?? Messages::find(message_id) :844-847
4. NẾU $messageError->error_code == '006' → return status:false + 「テンプレート内に…」 :849-854
5. Tách template_ids thành captureTempIds + templateIds                 :860-862
   (Template::handleTempIdAndCaptureTempId — prefix "cap" → capture)
6. NẾU (type 1|2) VÀ chưa có sending_schedule_id VÀ templateIds rỗng
   → clone template mới từ message: Template::cloneTemplateFromMessage() :864-868
   NGƯỢC LẠI → dùng lại templateIds cũ
7. Ghép thêm template clone từ capture: CaptureTemplate::cloneTemplateFromCapture() :870-873
8. Tính lại error_end_code từ error_message                              :875-877
9. type == 1 → updateOrCreate sending_schedule_setting (send_type=1, is_sent=0,
   send_time = strtotime("$date_send $time_send:00") * 1000)             :880-910
   rồi update message_error: sending_schedule_id, is_confirmed=1, template_ids
   type == 2 → tương tự nhưng send_type=2, send_time = time()*1000       :911-941
   type == 3 → xoá template clone (category_id = -222), xoá row lịch,
               xoá message_error (CÓ lọc bot_id)                         :942-960
10. return {status: true}                                                :962-966
```

**Không có `DB::beginTransaction()`** — các lệnh `DB::beginTransaction()` / `DB::commit()` / `DB::rollback()` đều bị comment (`:879`, `:962`, `:975`). Tin cậy **Cao**. Hệ quả: nếu lỗi giữa chừng, có thể còn `sending_schedule_setting` mồ côi hoặc `template` clone rác.

#### Logic chi tiết `saveSettingErrorMessageAll()` (`:983-1051`)

```
$time = type==1 ? "$date_send $time_send:00" : Carbon::now()             :994

NHÁNH A — selectAll == 'true' :996-1029
  Query DB::table('message_error') where bot_id, status NOT IN (100,101)
  + lọc errorType, + lọc errorTab (join sending_schedule_setting)
  ├─ errorTab == 'registered_send'
  │    → lấy list id → updateTimeSend() → return (chỉ đổi giờ gửi)       :1013-1017
  └─ còn lại
       → UPDATE message_error SET status = 1 (WAITING), date_send = "$date_send $time_send:00"  :1026-1029
       → dispatch(new SettingScheduleMessageErrorJob(botId, type, errorTab, errorType))
         ->onConnection('database')                                       :1030

NHÁNH B — selectAll != 'true' :1031-1035
  ├─ errorTab == 'registered_send' → updateTimeSend(ids, $time) → return  :1032
  └─ SendingScheduleSetting::handleScheduleMsgErrors(botId, ids, type, date_send, time_send)  :1034

Cuối: cập nhật cache lastErrorMessage{botId} TTL 5 phút                   :1038-1040
```

> **Cơ chế 2 tốc độ (Cao)**: chọn thủ công vài bản ghi → xử lý **đồng bộ** ngay trong request. Chọn "tất cả" → đánh dấu `status = WAITING` rồi **đẩy sang queue** để tránh timeout. Đây chính là lý do `ajaxGetMessageError()` loại bỏ bản ghi có `status = WAITING` khỏi danh sách (`:169`) — bản ghi đang chờ job sẽ tạm biến mất khỏi UI.

---

### 1.2. `Basic\ErrorListController` (v1 — legacy)

File: `app/Http/Controllers/Basic/ErrorListController.php` (1.867 dòng)

| Method | Dòng | Trạng thái | Ghi chú |
|--------|------|-----------|---------|
| `__construct(...)` | `:51-61` | Hoạt động | Inject `TemplateRepositoryInterface`, `ImageMapRepositoryInterface`, `MessageRepositoryInterface`; gán `$this->chat_class = app()->ChatHelper` |
| `getCount()` | `:63-69` | Không có route | Đếm message `has_error = 1` trong 7 ngày gần nhất |
| `index(Request)` | `:71-135` | **Chỉ redirect** | `return redirect()->route('errorListV2');` ngay dòng `:74` → toàn bộ ~60 dòng phía dưới là **dead code** (bao gồm logic tự sửa `error_message` theo `plan_type` và quota LINE API) |
| `renderViewSetting(Request)` | `:137-186` | Hoạt động | Đánh dấu `is_confirmed = 1`; dò URL trong nội dung, lấy thống kê click từ `Url`; dispatch `InfoEvent` khi request AJAX (`:172-174`) |
| `setting(Request)` | `:189-231` | Hoạt động | Xoá message ở bảng phân mảnh + xoá `message_error`; cập nhật `notify_setting.app_total_msg_error` & `chat_work_total_msg_error` |
| `findUrlInMessage($message)` — private | `:233-242` | Helper | Regex bóc URL |
| `sendMessageChecked(Request)` | `:244-467` | Hoạt động | Đặt lịch gửi lại (v1) — build message theo `type` (`text`/`image`/`audio`/`video`/…) |
| `resendAll(Request)` | `:469-600` | Hoạt động | Gửi lại đồng bộ nhiều message qua LINE API |
| `sendMessageById($id, $tableNumber, $errorMessage)` — private | `:602-1731` | Helper khổng lồ (~1.130 dòng) | Dựng payload LINE cho mọi loại tin nhắn rồi gọi LINE Messaging API |
| `getDurationOfWav* ` | `:1733-1742` | Helper | Tính độ dài file audio |
| `sendMessage(Request)` | `:1744-1828` | Hoạt động | Gửi lại 1 message đồng bộ; thành công thì `free_send_count + 1`, `updateMessageSendCount(botId, today, 3)`, tạo lại bản ghi `messages` sạch, xoá bản gốc + xoá `message_error` |
| `settingMessages(Request)` | `:1830-1853` | Hoạt động | Xoá hàng loạt ở cả 3 bảng `messages`, `messages_page_2`, `messages_old` + `message_error` |
| `updateLastTimeShowError(Request)` | `:1855-1866` | **Hoạt động, v2 vẫn dùng** | Cập nhật `bots.last_time_show_message_error` + cache |

> **Khác biệt kiến trúc quan trọng (Cao)**: v1 gửi lại **đồng bộ ngay trong HTTP request** (gọi LINE API trực tiếp trong `sendMessageById`). v2 **không gọi LINE API** — chỉ ghi bản ghi vào `sending_schedule_setting` để Spring Boot job xử lý.

---

## 2. Models Eloquent

### 2.1. `App\MessageError` — `app/MessageError.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| `$table` | `message_error` |
| `$primaryKey` | `id` |
| `$guarded` | `[]` (mass-assignment mở hoàn toàn) |
| `$timestamps` | `true` |
| Connection | mặc định (`mysql`) |

**Hằng số** (`app/MessageError.php:14-28`)

| Hằng số | Giá trị | Ý nghĩa |
|---------|---------|---------|
| `TYPE_OTHER` | `1` | Loại khác |
| `TYPE_CHAT11` | `2` | 「1:1チャット」 |
| `TYPE_SEND_ALL` | `3` | 「メッセージ配信」 (broadcast) |
| `TYPE_STEP` | `4` | 「ステップ配信」 (step/scenario) |
| `TYPE_TEMPLATE` | `5` | Template — gộp vào 「その他メッセージ」 |
| `TYPE_REMIND` | `6` | Nhắc lịch — gộp vào 「その他メッセージ」 |
| `STATUS_HANDLED['WAITING']` | `1` | Đang chờ queued job xử lý |
| `STATUS_HANDLED['DONE']` | `2` | Job đã tạo lịch xong |
| `STATUS_RETRY_WAIT` | `100` | Đang chờ retry — **không cho tick chọn / xoá** |
| `STATUS_RETRY_SENDING` | `101` | Đang gửi lại — **không cho tick chọn / xoá** |

**Hai giá trị `status` chỉ tồn tại phía Spring Boot** (`src/job/linect-service/src/main/java/sns/line/values/MessageErrorConstants.java:4-7`) — **không** được khai báo trong `app/MessageError.php`:

| Hằng số (Java) | Giá trị | Ý nghĩa | Hệ quả phía Laravel |
|----------------|---------|---------|---------------------|
| `STATUS_RETRY_INQUEUE` | `102` | Đã được job đẩy vào hàng đợi retry | Không nằm trong `whereNotIn([100, 101])` → **vẫn tick chọn / xoá được** dù đang được job xử lý |
| `STATUS_RETRY_ERROR` | `103` | Retry thất bại | **Trạng thái kẹt vĩnh viễn** — job chỉ poll `status = 100`, không bao giờ nhặt lại bản ghi `103`; Laravel cũng không có luồng nào đưa nó về `100` |

> Mức độ tin cậy: **Cao** cho giá trị hằng số (đọc trực tiếp file Java); **Trung bình** cho đánh giá "kẹt vĩnh viễn" (suy luận từ điều kiện poll, chưa kiểm chứng runtime).
> Tổng hợp: `message_error.status` thực tế nhận **7 giá trị** — `0` (mặc định), `1` (WAITING), `2` (DONE), `100`, `101`, `102`, `103`.

**Relationships**

| Tên | Loại | Khoá | Dòng |
|-----|------|------|------|
| `lineUser()` | `belongsTo(LineUser::class, 'line_id', 'id')` | `message_error.line_id` → `line_user.id` | `:29-31` |
| `scheduleSend()` | `belongsTo(SendingScheduleSetting::class, 'sending_schedule_id', 'id')` | | `:33-35` |

**Không có** scope, accessor, mutator, cast. Tin cậy **Cao**.

**Schema `message_error`** (`db/schema/tables/message_error.sql`)

| Cột | Kiểu | Ý nghĩa |
|-----|------|---------|
| `id` | `int unsigned` | PK |
| `message_id` | `int` | ID tin nhắn gốc ở một trong các bảng `messages*` |
| `line_id` | `int` | FK → `line_user.id` (đặt tên gây nhầm với LINE userId) |
| `bot_id` | `int` | FK → `bots.id` |
| `error_message` | `text` | Nội dung lỗi (tiếng Nhật, có thể chứa HTML `<a>`) |
| `is_confirmed` | `int` (mặc định `0`) | Đã xác nhận / đã đăng ký gửi lại |
| `error_code` | `varchar(32)` (mặc định `'unknow'`) | Mã lỗi kỹ thuật (`reach_limit_line`, `reach_limit_line_loaded`, `006`, …) |
| `duration` | `int` | Độ dài audio/video |
| `sending_schedule_id` | `int unsigned` | FK → `sending_schedule_setting.id`; `NULL` = chưa đăng ký gửi lại |
| `error_end_code` | `varchar(50)` | Mã hiển thị `001`–`007`/`other` |
| `type` | `tinyint` (mặc định `1`) | Comment DB: `1: other, 2: chat11, 3: send all, 4: scenario` |
| `parent_id` | `int` | ID broadcast (type=3) hoặc step_message (type=4) |
| `template_ids` | `varchar(256)` | CSV id template; phần tử dạng `cap_{id}` là capture template |
| `status` | `tinyint` (mặc định `0`) | Comment DB chỉ ghi `1: waiting, 2: done`. Thực tế còn 4 giá trị retry **chỉ có trong code**: `100` RETRY_WAIT, `101` RETRY_SENDING (`app/MessageError.php:26-27`), `102` RETRY_INQUEUE, `103` RETRY_ERROR (`sns/line/values/MessageErrorConstants.java:4-7`) |
| `date_send` | `timestamp` | Thời điểm gửi lại mong muốn (do batch ghi) |
| `retry_count` | `int` | Số lần đã retry |
| `created_at` / `updated_at` | `timestamp` | |

### 2.2. `App\SendingScheduleSetting` — `app/SendingScheduleSetting.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| `$table` | `sending_schedule_setting` |
| `$guarded` | `[]` |
| Connection | mặc định (`mysql`) |

**Relationships**: `lineUser()` → `belongsTo(LineUser::class, 'line_user_id', 'id')` (`:15-17`)

**Static methods (đây là nơi tập trung nghiệp vụ, không phải controller)**

| Method | Dòng | Mô tả |
|--------|------|-------|
| `handleScheduleMsgErrors(int $botId, array $messageErrorIds, int $type, string $dateSend = '', string $timeSend = '')` | `:19-127` | Xử lý hàng loạt: lặp từng `message_error_id`, bỏ qua bản ghi không tồn tại hoặc `error_code == '006'`; nếu `$dateSend`/`$timeSend` rỗng thì **lấy từ `message_error.date_send`** (đường đi của queued job); clone template; tạo/cập nhật `sending_schedule_setting` với `is_sent = -1`; gọi `pushSchedule()` |
| `pushSchedule(int $msgErrId, int $scheduleId, string $templateIds)` | `:129-141` | Cập nhật `message_error` (`sending_schedule_id`, `is_confirmed=1`, `template_ids`, `status = DONE`) **chỉ khi `sending_schedule_id` đang NULL**; nếu update thành công → set `sending_schedule_setting.is_sent = 0` (mở khoá cho Spring Boot job); nếu thất bại → **xoá row lịch vừa tạo** và `notifyChatwork('Đặt lịch resend msg error bị lỗi, ID: …')` |
| `getEndCode($message_error)` | `:143-174` | **Bản sao y hệt** `MessageErrorController::getEndCode()` — code trùng lặp |

> **Giá trị `is_sent = 8` — `STATUS_EXPIRED_BOT` (Cao)**: khai báo tại `src/job/linect-service/src/main/java/sns/line/models/linedb/entities/SendingScheduleSetting.java:10`. Spring Boot `SendingScheduleTask` gán giá trị này khi bot **không tồn tại hoặc đã hết hạn gói quá 7 ngày** (`bot == null || bot.isExpiredOver7Day()`), rồi `continue` bỏ qua bản ghi (`SendingScheduleTask.java:47-53`).
> Hệ quả trên UI: bản ghi `is_sent = 8` **trở nên vô hình — không thuộc tab nào**. Tab 「再送登録済み」 lọc `is_sent = 0`, tab 「再送済み履歴」 lọc `is_sent = 1`, còn `message_error` tương ứng vẫn giữ `sending_schedule_id` khác `NULL` nên cũng không xuất hiện ở tab 「未確認エラー」 (`MessageErrorController.php:181-217`). Mức độ tin cậy: **Cao** (giá trị + điều kiện gán), **Trung bình** (đánh giá "vô hình" — suy luận từ 3 điều kiện lọc).

> **Cơ chế `is_sent = -1` (Cao, quan trọng)**: đường đi qua `handleScheduleMsgErrors()` cố tình ghi `is_sent = -1` trước, rồi mới chuyển về `0` trong `pushSchedule()`. Spring Boot `SendingScheduleTask` chỉ quét `is_sent = 0` (`IS_WAIT_SEND`), nên `-1` đóng vai trò **khoá tạm** ngăn job cướp bản ghi trước khi `message_error` được liên kết xong. Ngược lại, đường đi trực tiếp qua `saveSettingErrorMessage()` (`MessageErrorController.php:889`, `:920`) ghi thẳng `is_sent = 0` — **không có khoá này** → tồn tại khe hở race condition ngắn (mức độ tin cậy: **Trung bình** cho phần đánh giá rủi ro, **Cao** cho phần đọc giá trị).

**Schema `sending_schedule_setting`** (`db/schema/tables/sending_schedule_setting.sql`)

| Cột | Kiểu | Ý nghĩa |
|-----|------|---------|
| `id` | `int unsigned` | PK |
| `bot_id` | `int unsigned` | FK → `bots.id` |
| `line_user_id` | `int unsigned` | FK → `line_user.id` (nhận giá trị từ `message_error.line_id`) |
| `send_type` | `tinyint` | Comment DB: `1 (send schedule), 2 (send now)` |
| `send_time` | `bigint` | **Epoch millisecond** (`strtotime(...) * 1000`) |
| `template_ids` | `varchar(255)` | CSV id template đã clone |
| `action_id` | `int` | Luôn `null` trong luồng này (`$actionId = null`) |
| `is_sent` | `tinyint` | `0` = chờ gửi (`IS_WAIT_SEND`), `1` = đã gửi (`IS_SENT_SUCCESS`), `-1` = đang khoá tạm (chỉ Laravel ghi, xem ghi chú dưới), **`8` = bot hết hạn** (`STATUS_EXPIRED_BOT`) |
| `parent_id` | `int` | Copy từ `message_error.parent_id` |
| `type_error` | `tinyint` | Copy từ `message_error.type` |
| `error_end_code` | `varchar(50)` | Copy từ `message_error.error_end_code` |
| `time_send_error` | `datetime` | Copy từ `message_error.created_at` — thời điểm phát sinh lỗi ban đầu |
| `message_error_id` | `int` | FK ngược → `message_error.id` |
| `created_at` / `updated_at` | `timestamp` | |

### 2.3. Các model phụ

| Model | Bảng | Connection | Vai trò trong tính năng |
|-------|------|-----------|------------------------|
| `App\LineUser` | `line_user` | `mysql` | Tên + avatar người nhận trên bảng lỗi |
| `App\Template` | `template` | `mysql` | Nội dung tin nhắn gửi lại; template clone có `category_id = -222` |
| `App\CaptureTemplate` | `capture_templates` | `mysql` | Template dạng capture (`cap_{id}` trong `template_ids`) — tên bảng khai báo tại `app/CaptureTemplate.php:10` |
| `App\SourceMessage` | `source_messages` | `mysql` | Nguồn tin nhắn nhiều bong bóng — tên bảng khai báo tại `app/SourceMessage.php:10` |
| `App\BroadCast` | `broadcast` | `mysql` | Tên chiến dịch cho lỗi `type = 3` |
| `App\StepMessage` | `step_message` | `mysql` | Tên step cho lỗi `type = 4` |
| `App\Scenario` | `scenario` | `mysql` | Tên kịch bản (qua `StepMessage::scenario`) |
| `App\Bots` | `bots` | `mysql` | `last_time_show_message_error`, `free_send_count`, `plan_type` |
| `App\NotifySetting` | `notify_setting` | `mysql` | `app_total_msg_error`, `chat_work_total_msg_error` (chỉ v1 cập nhật) |

---

### 2.4. Nguồn sinh bản ghi `message_error` phía Laravel

> **Điểm kiến trúc dễ hiểu nhầm**: hai controller ở §1 **chỉ đọc và cập nhật** `message_error`. Không được suy ra rằng toàn bộ dữ liệu do Spring Boot sinh. Thực tế bảng `message_error` có **hai nguồn ghi song song**:
>
> - **(a) Spring Boot** — `SentMessageHelper.saveMessageError()`, cho các tin nhắn gửi qua background job.
> - **(b) Laravel** — **11 lệnh `create()` nằm trong 7 file**, cho các tin nhắn gửi **đồng bộ ngay trong request / trong cron command**.
>
> Mục này liệt kê nguồn (b), chia thành **hai nhóm**: §2.4.1 nhóm luồng gửi tin chính (6 lệnh, 2 file) và §2.4.4 nhóm bản sao cục bộ (5 lệnh, 5 file). Mức độ tin cậy: **Cao** (census bằng `grep -rn "MessageError::query()->create(\|MessageError::create(" app/`, sau đó đọc từng vị trí).
>
> Lưu ý: `MessageErrorController.php:396` dùng `new MessageError()` nhưng **không bao giờ `save()`** — chỉ dựng object tạm trong bộ nhớ để trả DTO cho tab 「再送済み履歴」, nên không tính là vị trí ghi.

#### 2.4.1. Nhóm (a) — luồng gửi tin chính: 6 lệnh trong 2 file

| # | Hàm / method | File:dòng (lệnh `create`) | Có guard loại trừ type 3/4/6? | Ghi chú |
|---|--------------|---------------------------|-------------------------------|---------|
| W-1 | `createMessage()` | `app/Helpers/functions.php:3033` | **Có** — `functions.php:3028-3032` | Hàm khai báo tại `functions.php:2632`; `'type'` gán tại `:3040` |
| W-2 | `createMessageError()` | `app/Helpers/functions.php:3182` | **KHÔNG** | Hàm khai báo tại `functions.php:3121`; `'type'` gán tại `:3189`. Ghi được **mọi** giá trị type |
| W-3 | `createMultipleMessage()` | `app/Helpers/functions.php:3602` | **Có** — `functions.php:3597-3601` | Hàm khai báo tại `functions.php:3197`; `'type'` gán tại `:3609` |
| W-4 | `createMessageSendTest()` | `app/Helpers/functions.php:8024` | **Có** — `functions.php:8019-8023` | Hàm khai báo tại `functions.php:7663`; `'type'` gán tại `:8031` |
| W-5 | `MessageService::handleErrorMessage()` | `app/Services/MessageService.php:386` (nhánh `if`) và **`:398` (nhánh `else`)** | **Có nhưng có nhánh `else`** — `MessageService.php:381-385` | Method khai báo tại `MessageService.php:343`; `'type'` gán tại `:393` (if) và `:404` (else) |

> **Đính chính quan trọng so với giả thiết "Laravel chỉ ghi type 1/2/5"**: giả thiết đó **chỉ đúng cho W-1, W-3, W-4**. Hai vị trí còn lại ghi được cả type 3/4/6:
> - **W-2** không có guard nào — đọc toàn bộ thân hàm `functions.php:3121-3196` không thấy điều kiện loại trừ.
> - **W-5** có guard nhưng kèm nhánh `else` tại `MessageService.php:397-407`: khi type **thuộc** `{3, 4, 6}` thì **vẫn tạo bản ghi**, chỉ khác ở chỗ **bỏ trống `message_id`** (không truyền khoá này) và lấy `template_ids` từ `$optionalParams['templateError']` thay vì `null`.
>
> ⇒ Kết luận đúng: **Laravel ghi được mọi giá trị `type` từ 1 đến 6**; riêng type 3/4/6 chỉ đi qua W-2 và W-5-else, và bản ghi sinh ra từ W-5-else **có `message_id = NULL`**. Mức độ tin cậy: **Cao**.
> Hệ quả nghiệp vụ: bản ghi thiếu `message_id` sẽ không dò được nội dung ở bước 1–3 của thuật toán §3.2, nên cột nội dung trên UI dựa hoàn toàn vào `template_ids`.

#### 2.4.2. Cơ chế guard (W-1, W-3, W-4, W-5)

```php
$typeMessageError = !empty($optionalParams['type_message_error'])
    ? $optionalParams['type_message_error'] : 1;

if (
    $typeMessageError != MessageError::TYPE_SEND_ALL &&   // != 3
    $typeMessageError != MessageError::TYPE_STEP   &&     // != 4
    $typeMessageError != MessageError::TYPE_REMIND        // != 6
) { MessageError::query()->create([...]); }
```

Nguồn: `app/Helpers/functions.php:3028-3032` (bản gốc), lặp lại y hệt tại `:3597-3601`, `:8019-8023`, `app/Services/MessageService.php:381-385`.

**Ý nghĩa phân vai**: type 3 (`TYPE_SEND_ALL` — 「メッセージ配信」), type 4 (`TYPE_STEP` — 「ステップ配信」) và type 6 (`TYPE_REMIND`) là các luồng gửi **hàng loạt / theo lịch** do Spring Boot đảm nhiệm; Laravel cố tình **không** ghi trùng bản ghi lỗi cho chúng ở 3 helper phổ biến nhất, tránh nhân đôi dữ liệu. Mức độ tin cậy: **Cao** (đọc code) / **Trung bình** (diễn giải ý đồ thiết kế).

Một quy tắc phụ đi kèm ở cả 5 vị trí: nếu `type_message_error == 5` (`TYPE_TEMPLATE`) thì **ép `parent_id = null`** — `functions.php:3025-3027`, `:3178-3180`, `:3593-3595`, `:8013-8015`, `MessageService.php:375-377`.

#### 2.4.3. Các vị trí truyền `type_message_error`

Toàn hệ thống có **53 vị trí** truyền tham số `type_message_error` (grep `app/` trừ `functions.php`), phân bố theo giá trị:

| Giá trị truyền | Số vị trí | Nhóm UI 「配信エラー」 tương ứng |
|----------------|-----------|--------------------------------|
| `TYPE_CHAT11` (2) | 17 | 「1:1チャット」 |
| `TYPE_OTHER` (1) | 13 | 「その他メッセージ」 |
| `TYPE_REMIND` (6) | 11 | 「その他メッセージ」 |
| `TYPE_STEP` (4) | 4 | 「ステップ配信」 |
| `TYPE_SEND_ALL` (3) | 2 | 「メッセージ配信」 |
| `TYPE_TEMPLATE` (5) | 2 | 「その他メッセージ」 |

**Các vị trí tiêu biểu trong Controllers**

| Controller:dòng | Giá trị |
|-----------------|---------|
| `app/Http/Controllers/Api/ChatController.php:735`, `:989`, `:1130`, `:4988`, `:5111`, `:5313` | `TYPE_CHAT11` |
| `app/Http/Controllers/ChatController.php:1366`, `:1527`, `:1957` | `TYPE_CHAT11` |
| `app/Http/Controllers/Admin/BotController.php:4771`, `:5200` | `TYPE_CHAT11` |
| `app/Http/Controllers/Basic/FormAnswerController.php:6933` | `TYPE_CHAT11` |
| `app/Http/Controllers/Basic/QRCodeController.php:1203` | `TYPE_CHAT11` |
| `app/Http/Controllers/Basic/BroadcastController.php:2204` | `TYPE_SEND_ALL` |
| `app/Http/Controllers/Basic/StepMessageController.php:1244`, `:1293` | `TYPE_STEP` |
| `app/Http/Controllers/Api/Mobile/ScenarioMobileController.php:1521` | `TYPE_STEP` |
| `app/Http/Controllers/Api/RemindApiController.php:124` | `TYPE_REMIND` |
| `app/Http/Controllers/Api/BookingEventController.php:1049` | `TYPE_REMIND` |
| `app/Http/Controllers/Basic/BookingEventController.php:2558` | `TYPE_REMIND` |
| `app/Http/Controllers/Basic/BookingEventDayController.php:4345` | `TYPE_REMIND` |
| `app/Http/Controllers/Basic/FormAnswerController.php:2731` | `TYPE_REMIND` |
| `app/Http/Controllers/Basic/MobileEventBookingController.php:2751` | `TYPE_REMIND` |
| `app/Http/Controllers/Basic/TalkListController.php:218` | `TYPE_OTHER` |
| `app/Http/Controllers/Basic/UserController.php:3577` | `TYPE_OTHER` |
| `app/Http/Controllers/LiffController.php:1977` | `TYPE_OTHER` |
| `app/Http/Controllers/Basic/TemplateV2Controller.php:1242` | `TYPE_TEMPLATE` |

**Các vị trí tiêu biểu trong Services**

| Service:dòng | Giá trị |
|--------------|---------|
| `app/Services/ChatService.php:162`, `:223`, `:301` | `TYPE_CHAT11` |
| `app/Services/TemplateService.php:3055` | `TYPE_CHAT11` |
| `app/Services/BroadcastService.php:67` | `TYPE_SEND_ALL` |
| `app/Services/StepMessageService.php:78` | `TYPE_STEP` |
| `app/Services/Events/EventService.php:377` | `TYPE_REMIND` |
| `app/Services/EventBooking/EventBookingService.php:1134` | `TYPE_REMIND` |
| `app/Services/FormAnswer/FormAnswerService.php:1560` | `TYPE_REMIND` |
| `app/Services/HelperService.php:550` | `TYPE_REMIND` |
| `app/Services/Templates/TemplateService.php:96` | `TYPE_REMIND` |
| `app/Services/FormAnswer/FormAnswerService.php:2098`, `:2214`, `:2246` | `TYPE_OTHER` |
| `app/Services/CalendarManagement/CalendarCourseBookingService.php:1346`, `:1475` | `TYPE_OTHER` |
| `app/Services/CalendarSalon/CalendarSalonLineBookingService.php:4643` | `TYPE_OTHER` |
| `app/Services/EventBooking/EventBookingService.php:163` | `TYPE_OTHER` |
| `app/Services/Sales/SalesService.php:91` | `TYPE_OTHER` |
| `app/Services/HelperService.php:889`, `app/Services/TemplateService.php:3134` | `TYPE_OTHER` |
| `app/Services/TemplateService.php:2674` | `TYPE_TEMPLATE` |

> **Lưu ý cho `db-mapper` / `job-analyzer`**: các vị trí truyền `TYPE_SEND_ALL` / `TYPE_STEP` / `TYPE_REMIND` **không tự động** sinh bản ghi `message_error` — còn tuỳ helper mà chúng gọi (xem bảng W-1…W-5). Nếu đi qua W-1/W-3/W-4 thì bị guard chặn hoàn toàn.

#### 2.4.4. Nhóm (b) — bản sao `createMessage()` cục bộ: 5 lệnh trong 5 file

Ngoài luồng chính, còn **5 lệnh `create()`** nằm rải rác ở tầng sales, console command và một command khôi phục dữ liệu. Đây **không phải** lỗi thanh toán — bốn trong số đó nằm bên trong các **bản sao copy-paste của hàm `createMessage()`**, xử lý đúng loại lỗi gửi tin LINE như luồng chính (bắt các chuỗi lỗi LINE API 「You have reached your monthly limit.」, 「Authentication failed…」), chỉ khác là được gọi từ ngữ cảnh bán hàng / thanh toán / cron.

| # | Vị trí lệnh `create()` | Hàm bao | Truyền `type`? | Có guard? | Ghi `error_code` / `error_end_code`? |
|---|------------------------|---------|----------------|-----------|--------------------------------------|
| W-6 | `app/Services/Sales/SalesService.php:2108` | `createMessage()` — `SalesService.php:1754` | **Không** | **Không** | **Không ghi cả hai** |
| W-7 | `app/Http/Controllers/Basic/SalesManagementV2Controller.php:4506` | `createMessage()` — `SalesManagementV2Controller.php:4140` | **Không** | **Không** | **CÓ ghi cả hai** (`:4510-4511`) |
| W-8 | `app/Console/Commands/HandleBillStripe.php:1259` | `createMessage()` — `HandleBillStripe.php:906` | **Không** | **Không** | **Không ghi cả hai** |
| W-9 | `app/Console/Commands/HandleSendActionTrialV2.php:1262` | `createMessage()` — `HandleSendActionTrialV2.php:909` | **Không** | **Không** | **Không ghi cả hai** |
| W-10 | `app/Console/Commands/Recover.php:257` | `addRecoverErrorList()` — `Recover.php:251` | **Không** | **Không** | **Không ghi cả hai** |

> **Đính chính so với giả thiết "cả 5 vị trí đều thiếu `error_code`/`error_end_code`"**: giả thiết này **sai ở W-7**. `SalesManagementV2Controller.php:4493-4512` có `switch` gán đầy đủ `$errorCode` + `$errorEndCode` (`'004'`, `'005'`, `'unknow'/'other'`, …) và truyền cả hai vào `create()`. Chỉ **4 vị trí W-6, W-8, W-9, W-10** mới thực sự thiếu. Mức độ tin cậy: **Cao** (đọc trực tiếp cả 5 vị trí).

**Đặc điểm chung của nhóm (b)** — xác minh trực tiếp từng vị trí, mức độ tin cậy **Cao**:

| Đặc điểm | Hệ quả |
|----------|--------|
| **Không vị trí nào truyền `'type'`** | Rơi về giá trị mặc định của schema `type tinyint NOT NULL DEFAULT '1'` = `TYPE_OTHER` ⇒ mọi bản ghi nhóm này đều hiện ở nguồn 「その他メッセージ」 |
| **Không vị trí nào có guard** `type ∉ {3, 4, 6}` | Không liên quan thực tế, vì `type` luôn là `1` |
| **W-6, W-8, W-9, W-10 thiếu `error_code` + `error_end_code`** | Hai hệ quả dây chuyền — xem dưới |

**Hệ quả kép của việc thiếu `error_code` / `error_end_code`** (áp dụng cho W-6, W-8, W-9, W-10):

1. **Trên UI**: `error_end_code` để `NULL` ⇒ `ajaxGetMessageError()` gọi `getEndCode($error_message)` runtime (`MessageErrorController.php:316-318`). Chuỗi lỗi mà nhóm này sinh ra (「配信数上限に達しています。こちらから契約内容を確認してください。」) **không khớp mẫu nào** trong 7 mẫu của `getEndCode()` ⇒ luôn trả `'other'` ⇒ hiển thị dòng fallback 「上記以外の場合」 / 「サポート専用LINE公式アカウントまでお問い合わせください。」. Mức độ tin cậy: **Cao** (đối chiếu chuỗi tại `SalesService.php:2096-2099` với 7 mẫu tại `MessageErrorController.php:349-355`).
2. **Trên background job**: `error_code` để `NULL` ⇒ task `HandleGetMessageError` **không bao giờ nhặt được** các bản ghi này, vì nó poll bằng `findFirstByErrorCode(MessageError.REACH_LIMIT_LINE)` với hằng số `"reach_limit_line"` (`src/main/java/sns/line/task/HandleGetMessageError.java:33`; hằng số tại `models/linedb/entities/MessageError.java:12`). Task này chính là nơi gọi LINE API lấy quota rồi **nâng cấp** bản ghi thành mã `001`/`002`/`003` kèm `error_code = 'reach_limit_line_loaded'`. Mức độ tin cậy: **Cao**.

⇒ Dù bản chất là lỗi chạm hạn mức LINE, các bản ghi W-6/W-8/W-9/W-10 **vĩnh viễn kẹt ở mã `other`**. Đây là lời giải thích cho tỉ lệ bản ghi rơi vào fallback 「上記以外の場合」 cao bất thường mà `db-mapper` quan sát được. Mức độ tin cậy: **Trung bình** (suy luận nhân quả; chưa đối chiếu số liệu thực tế theo từng nguồn ghi).

**Riêng W-10 (`Recover.php:257`) khác bản chất**: nằm trong `addRecoverErrorList()` (`Recover.php:251-268`) — một command **backfill/khôi phục dữ liệu**, quét `Messages::where('has_error', 1)` rồi tái tạo bản ghi `message_error` từ tin nhắn cũ, **giữ nguyên `created_at` / `updated_at` / `is_confirmed` gốc**. Không phải luồng gửi tin runtime. Mức độ tin cậy: **Cao**.

#### 2.4.5. Rủi ro nghiệp vụ của nhóm (b)

> **Đính chính một cách hiểu sai phổ biến**: nhóm (b) **không phải** "lỗi thanh toán / bán hàng lẫn vào bảng lỗi gửi tin". Đọc mã tại `SalesService.php:2085-2107`, `HandleBillStripe.php:1236-1258`, `HandleSendActionTrialV2.php:1239-1261` cho thấy cả ba đều bắt **chuỗi lỗi trả về từ LINE Messaging API** (「You have reached your monthly limit.」, 「Authentication failed. Confirm that the access token…」) — tức đúng là **lỗi gửi tin LINE**, chỉ phát sinh trong ngữ cảnh thông báo bán hàng / thanh toán / cron. Việc Admin bấm 「すぐに再送する」 trên chúng là **hợp lệ về mặt nghiệp vụ**. Mức độ tin cậy: **Cao**.

Các rủi ro thực sự, xếp theo mức độ:

| Rủi ro | Mô tả | Mức |
|--------|-------|-----|
| Mã lỗi sai lệch | W-6/W-8/W-9/W-10 kẹt vĩnh viễn ở `other` (xem BR-26) ⇒ Admin không nhận được hướng dẫn nâng cấp gói dù nguyên nhân thật là chạm hạn mức LINE | **Trung bình** |
| Gửi lại tin nhắn rất cũ | Bản ghi do `Recover.php:257` backfill giữ nguyên `created_at` gốc (có thể nhiều năm trước) nhưng vẫn hiện ở tab 「未確認エラー」 như lỗi thường. Bấm 「すぐに再送する」 sẽ gửi lại nội dung đã lỗi thời tới người dùng LINE | **Trung bình** |
| Trôi lệch do copy-paste | 4 bản sao `createMessage()` cục bộ không đồng bộ với bản gốc `functions.php:2632`: thiếu tham số `$optionalParams`, nên **mọi cải tiến sau này** (guard type, `template_ids`, `parent_id`, `error_end_code`) đều không lan tới chúng | **Trung bình** |
| Không phân biệt được nguồn ghi | Bảng `message_error` không có cột nào ghi lại vị trí sinh bản ghi ⇒ không thể lọc/thống kê theo nguồn để khoanh vùng sự cố | **Thấp** |

---

## 3. Cơ chế bảng `messages` phân mảnh theo năm — **điểm nghiệp vụ trọng yếu**

Hệ thống lưu tin nhắn ở **nhiều bảng, thậm chí nhiều database connection khác nhau**. `message_error.message_id` chỉ là con số — không kèm thông tin bảng — nên code phải **dò tuần tự**.

### 3.1. Bản đồ model → bảng → connection

| Model | Bảng | Connection | Nguồn |
|-------|------|-----------|-------|
| `App\MessagesV2` | `messages_v2s` | `mysql_message` | `app/MessagesV2.php:11-12` |
| `App\Messages` | `messages` | `mysql_message` | `app/Messages.php:13-14` |
| `App\MessagesPage2` | `messages_page_2` | `mysql_message` | `app/MessagesPage2.php:12-13` |
| `App\MessagesOld` | `messages_old` | `mysql_message` | `app/MessagesOld.php:12-13` |
| `App\Messages2020` | `messages_2020` | **`mysql_db_ovh`** | `app/Messages2020.php:13-14` |
| `App\Messages2021` | `messages_2021` | `mysql_db_ovh` | `app/Messages2021.php` |
| `App\Messages2022` | `messages_2022` | `mysql_db_ovh` | `app/Messages2022.php` |
| `App\Messages2023` | `messages_2023` | `mysql_db_ovh` | `app/Messages2023.php` |
| `App\Messages2024` | `messages_2024` | `mysql_db_ovh` | `app/Messages2024.php` |
| `App\Messages2025` | `messages_2025` | `mysql_db_ovh` | `app/Messages2025.php:13-14` |

→ **3 kho dữ liệu**: DB chính (`mysql`), DB tin nhắn nóng (`mysql_message`), DB lưu trữ theo năm (`mysql_db_ovh`). Tin cậy **Cao**.

### 3.2. Thuật toán chọn bảng trong v2 (`MessageErrorController.php:240-283`)

```
NẾU message_error.template_ids RỖNG:                                  :239
   1. Thử MessagesV2::where('id', message_id)->first()   (messages_v2s)  :240
      → nếu thấy: type_message = convert_type_message, replace_content
   2. Nếu rỗng → Messages::where('id', message_id)->first()  (messages)  :242
      → nếu thấy: type_message = type, replace_content
   3. Nếu VẪN rỗng → CHỌN BẢNG THEO NĂM:                                :249-274
        $yearData = Carbon::parse(message_error.created_at)->format('Y')
        switch ($yearData):
          2020 → Messages2020    2021 → Messages2021
          2022 → Messages2022    2023 → Messages2023
          2024 → Messages2024    2025 → Messages2025
          (mặc định: không có model → $modelMessage = null → bỏ qua)
        $contentMessage = $modelMessage->where('id', message_id)->first()
NGƯỢC LẠI (đã có template_ids):                                        :285
   Lấy nội dung từ Template::whereIn('id', explode(',', template_ids))->first()
```

**Tiêu chí chọn bảng theo năm**: dựa trên **`message_error.created_at`** — tức năm phát sinh lỗi, chứ không phải năm tạo tin nhắn. Tin cậy **Cao**.

### 3.3. Điểm cần lưu ý

| Vấn đề | Mô tả | Tin cậy |
|--------|-------|---------|
| Hard-code danh sách năm | `switch` chỉ liệt kê 2020–2025. Lỗi phát sinh từ **2026 trở đi** rơi vào nhánh mặc định → `$modelMessage = null` → không tìm được nội dung → cột nội dung trên UI **rỗng** | **Cao** (`MessageErrorController.php:249-274`) |
| Truy vấn chéo connection | Bước 3 truy vấn sang `mysql_db_ovh` — mỗi bản ghi có thể phát sinh 3 query trên 2 database khác nhau, **trong vòng lặp foreach** không eager load | **Cao** |
| v1 dùng bộ bảng khác | `ErrorListController` chỉ dò `Messages` → `MessagesPage2` → `MessagesOld` (`:120-126`), **không** đụng tới `MessagesV2` hay bảng theo năm | **Cao** |
| `table_number` chỉ có ở v1 | `MessageRepository::findById()` (`app/Repositories/Eloquents/MessageRepository.php:36-…`) gắn `table_number` = `1` (messages), `2` (messages_page_2), `3` (messages_old) để các hàm `Messages::updateMessagesMultipleTable()` / `deleteMessageMultipleTable()` biết ghi vào bảng nào. v2 **không dùng** cơ chế này | **Cao** |
| Bảng nào giữ nội dung để gửi lại | Khi đăng ký gửi lại, nội dung được **clone sang bảng `template`** (`category_id = -222`) — từ đó trở đi bản gửi lại **không phụ thuộc** bảng `messages*` nữa | **Cao** |

---

## 4. Services / Repositories

| Thành phần | File | Dùng ở đâu | Vai trò |
|-----------|------|-----------|---------|
| `App\Services\Templates\TemplateV2Service` | `app/Services/Templates/TemplateV2Service.php` | `MessageErrorController.php:558`, `:601` | Dựng dữ liệu preview template cho modal chi tiết |
| `App\Services\ConversationService` | `app/Services/ConversationService.php` | `MessageErrorController.php:679` — `ConversationService::isJson()` | Kiểm tra nội dung có phải JSON |
| `App\Contracts\Repositories\MessageRepositoryInterface` | impl: `app/Repositories/Eloquents/MessageRepository.php` | Inject vào `ErrorListController::__construct()` (`:51-61`) | `findById($id)` dò 3 bảng `messages`/`messages_page_2`/`messages_old` và gắn `table_number` |
| `App\Contracts\Repositories\TemplateRepositoryInterface` | | `ErrorListController` | Thao tác template khi gửi lại (v1) |
| `App\Contracts\Repositories\ImageMapRepositoryInterface` | | `ErrorListController` | Dựng payload image map khi gửi lại (v1) |
| `App\Helpers\ChatMessages`, `App\Helpers\PostbackActionBuilder` | | `ErrorListController` | Build payload LINE (v1) |
| `App\Services\Templates\FlexMessageService`, `QuickReplyService` | | `ErrorListController` | Build flex message / quick reply (v1) |
| `App\Http\Resources\PaginationResource` | `app/Http/Resources/PaginationResource.php` | EP-02 | Chuẩn hoá phân trang: `total_item_page`, `currentPage`, `perPage`, `totalPages`, `totalRecord` |

**Helper functions** (`app/Helpers/functions.php`)

| Hàm | Dòng | Vai trò |
|-----|------|---------|
| `getBotId()` | `:386-390` | Đọc `Session::get('current_bot_id')` — **nền tảng của toàn bộ phân tách dữ liệu theo bot** |
| `getBotIdInScope($botIdCurrent)` | `:397-…` | Bản an toàn hơn, kiểm tra bot có thuộc phạm vi user; **tính năng này không dùng** |
| `lastErrorMessage($botId)` | `:4227-4233` | Lấy `created_at` của lỗi chưa xác nhận mới nhất (`is_confirmed = 0`, loại trừ `Failed to send messages`) |
| `addLogUserAction($action)` | `:9380` | Ghi log hành động — gọi ở `ajaxDeleteErrorMessage` (`:714`), `sendMessage` (`:1747`), `resendAll` (`:475`), `settingMessages` (`:1834`) |
| `notifyChatwork($message)` | `:8898` | Cảnh báo Chatwork khi `pushSchedule()` thất bại |
| `getLimitMessageLine($token)` | `:4236-…` | Gọi LINE API `/v2/bot/message/quota` — chỉ dùng ở dead code của `ErrorListController::index()` |

**Static helper trên model**

| Method | File | Vai trò |
|--------|------|---------|
| `Template::handleTempIdAndCaptureTempId(array $ids)` | `app/Template.php:382-392` | Tách CSV `template_ids`: phần tử khớp `/^cap/` → `captureTempIds` (lấy phần sau dấu `_`), còn lại → `templateIds` |
| `Template::cloneTemplateFromMessage($message)` | `app/Template.php:394-…` | Clone nội dung từ `messages`/`messages_v2s` sang bản ghi `template` mới với `category_id = -222`; nếu message có `source_message_id` thì clone từ capture template |
| `CaptureTemplate::cloneTemplateFromCapture(array $ids)` | `app/CaptureTemplate.php` | Clone capture template sang template mới |

> **Ý nghĩa `category_id = -222` (Cao)**: giá trị sentinel đánh dấu "template hệ thống sinh ra để phục vụ gửi lại", **không hiển thị trong danh mục template của Admin**, và bị xoá khi Admin xoá bản ghi lỗi (`MessageErrorController.php:948-952`, `SendingScheduleSetting.php:113-117`).

---

## 5. Form Requests / Validation

**Không tồn tại FormRequest nào cho tính năng này.** Kiểm chứng: không có class nào trong `app/Http/Requests/` được import bởi 2 controller; cả hai controller đều đọc thẳng `$request->xxx` và không gọi `$this->validate()` / `Validator::make()`. Tin cậy **Cao**.

Toàn bộ kiểm tra đầu vào nằm ở JavaScript:

| Kiểm tra | Nội dung | Nguồn |
|----------|----------|-------|
| Thời điểm gửi lại ở quá khứ (modal 1 bản ghi) | Nếu `type == 1` và `date_send time_send` < hiện tại → `confirm('再送日時に現在時刻より前の時間が設定されています。 登録を押すと即時配信となりますがよろしいですか？')`; đồng ý → **đổi `type` thành `2`** (gửi ngay) | `public/js/error_list/modal-detail-message.js:92-97` |
| Thời điểm gửi lại ở quá khứ (thao tác hàng loạt) | Cùng logic | `public/js/error_list/index_v2.js:354-360` |
| Xác nhận xoá | `confirm('1件の再送登録済みメッセージを削除しますがよろしいですか？')` (và biến thể theo số lượng) | `public/js/error_list/index_v2.js:276-284` |
| Chặn tick bản ghi đang retry | `select_all` computed chỉ gom bản ghi có `status != 100 && status != 101` | `public/js/error_list/index_v2.js:36-52`, hằng số `:1-2` |
| Giá trị `per_page` | Chỉ 3 lựa chọn `100 / 200 / 500` | `public/js/error_list/index_v2.js:7-9` |

**Rủi ro (Trung bình)**: mọi ràng buộc trên đều bỏ qua được bằng cách gọi API trực tiếp — server sẽ chấp nhận `per_page` bất kỳ, `date_send`/`time_send` sai định dạng (`strtotime` trả `false` → `send_time = 0` → job gửi ngay lập tức).

---

## 6. Events / Listeners

| Event | Dispatch tại | Payload | Ghi chú |
|-------|-------------|---------|---------|
| `App\Events\InfoEvent` | `ErrorListController::renderViewSetting()` — `app/Http/Controllers/Basic/ErrorListController.php:172-174` (chỉ khi `$request->ajax()`) | `totalUserConfirmMessage(botId)`, `totalErrorMessage(botId)`, `totalGroupConfirmMessage(botId)`, `botId` | Broadcast realtime cập nhật badge số lỗi |
| `App\Events\InfoEvent` | **Không dispatch trong `MessageErrorController`** — chỉ được `use` ở dòng `:39` rồi bỏ không | — | Tin cậy **Cao** (grep toàn file chỉ ra 1 dòng import) |

---

## 7. Authorization

| Cơ chế | Trạng thái | Ghi chú |
|--------|-----------|---------|
| Policy / Gate | **Không có** | Không tìm thấy `authorize()`, `Gate::`, `can()` trong 2 controller |
| Phân tách theo bot | Qua `getBotId()` (session) + điều kiện `where('bot_id', ...)` trong từng query | Không nhất quán — xem bảng dưới |
| Phân quyền Staff | **Không kiểm tra trong controller** | Việc ẩn/hiện menu 「配信エラー」 phụ thuộc middleware `basic_access` và cấu hình role ở tầng menu, không có kiểm tra ở tầng action. Tin cậy **Trung bình** |

**Kiểm tra `bot_id` theo endpoint**

| Endpoint | Lọc `bot_id`? | Vị trí |
|----------|---------------|--------|
| EP-02 `ajaxGetMessageError` | Có | `MessageErrorController.php:168` |
| EP-02 `getListHistorySend` | Có | `MessageErrorController.php:73` |
| EP-03 `getDataPreviewMessage` | **Không** | `MessageErrorController.php:396`, `:405` — `find()` trần |
| EP-04 `saveSettingErrorMessage` (`type=1`, `type=2`) | **Không** | `MessageErrorController.php:843` |
| EP-04 `saveSettingErrorMessage` (`type=3`) | Có | `MessageErrorController.php:942`, `:958` |
| EP-05 `saveSettingErrorMessageAll` (`selectAll=true`) | Có | `MessageErrorController.php:997` |
| EP-05 `saveSettingErrorMessageAll` (danh sách id) | **Không** ở tầng controller | `handleScheduleMsgErrors()` dùng `find($id)` trần (`SendingScheduleSetting.php:22`); chỉ nhánh `type=3` mới lọc `bot_id` (`:104`) |
| EP-05 `updateTimeSend` | **Không** | `MessageErrorController.php:1055-1061` |
| EP-06 `ajaxDeleteErrorMessage` | Có | `MessageErrorController.php:766`, `:769` |
| EP-07 `updateLastTimeShowError` | Có (dùng `getBotId()` trực tiếp) | `ErrorListController.php:1856-1859` |

→ **Rủi ro IDOR mức Trung bình** ở EP-03, EP-04 (`type=1/2`), EP-05 (đường không `selectAll`): biết ID bản ghi lỗi của bot khác là có thể đọc chi tiết hoặc đặt lịch gửi lại cho bot đó. Mức độ tin cậy của phát hiện: **Cao** (đọc trực tiếp code); mức độ khai thác thực tế: **Trung bình** (chưa kiểm chứng runtime).

---

## 8. Business Rules

| # | Quy tắc | Nguồn |
|---|---------|-------|
| BR-01 | Bản ghi lỗi có `error_message` bằng `'Failed to send messages'` hoặc `' Failed to send messages'` **bị ẩn khỏi mọi danh sách** (lỗi rác không có nội dung tiếng Nhật) | `app/Http/Controllers/Basic/MessageErrorController.php:169`; `app/Jobs/SettingScheduleMessageErrorJob.php:47`; `app/Helpers/functions.php:4231` |
| BR-02 | Bản ghi đang chờ queued job (`status = 1 / WAITING`) **bị ẩn khỏi danh sách** cho tới khi job xử lý xong | `MessageErrorController.php:169` |
| BR-03 | Bản ghi ở trạng thái `status = 100` (RETRY_WAIT) hoặc `101` (RETRY_SENDING) **không được tick chọn, không được xoá, không được thao tác hàng loạt** | Client: `public/js/error_list/index_v2.js:36-52`; Server: `MessageErrorController.php:220`, `:723`, `:769`, `:773`, `:998` |
| BR-04 | Bản ghi có `error_code = '006'` (「テンプレート内にメッセージが登録されていないため送信ができませんでした」) **không được phép gửi lại** — trả lỗi ở thao tác đơn từ modal `SCR-ERR-05`, bị `continue` bỏ qua ở thao tác hàng loạt từ `SCR-ERR-06` | `MessageErrorController.php:849-854`; `app/SendingScheduleSetting.php:26-28` |
| BR-05 | Ba tab phân biệt bằng trạng thái liên kết lịch: `unconfirm` (`SCR-ERR-01`) = `sending_schedule_id IS NULL`; `registered_send` (`SCR-ERR-02`) = có lịch với `is_sent = 0` và `send_type = 1`; `history_send` (`SCR-ERR-03`) = có lịch với `is_sent = 1`. Bản ghi có `is_sent = 8` (bot hết hạn) **không thuộc màn hình nào** | `MessageErrorController.php:181-217`; `SendingScheduleSetting.java:10` |
| BR-06 | Tab 「再送済み履歴」 đọc **trực tiếp từ `sending_schedule_setting`**, không đi qua `message_error` — vì bản ghi lỗi có thể đã bị Spring Boot job xoá sau khi gửi lại thành công | `MessageErrorController.php:61-155`; `src/job/linect-service/src/main/java/sns/line/task/SendingScheduleTask.java:98` |
| BR-07 | Nhóm 「その他メッセージ」 = mọi `type` **không thuộc** `{2, 3, 4}` — tức bao gồm `1` (other), `5` (template), `6` (remind) | `MessageErrorController.php:178`, `app/MessageError.php:14-22` |
| BR-08 | `send_time` lưu bằng **epoch millisecond**: `strtotime("$date_send $time_send:00") * 1000` (đặt lịch) hoặc `time() * 1000` (gửi ngay) | `MessageErrorController.php:884`, `:915`; `app/SendingScheduleSetting.php:65`, `:88` |
| BR-09 | Khi đăng ký gửi lại lần đầu (chưa có `sending_schedule_id` và `template_ids` rỗng), nội dung tin nhắn được **clone sang bảng `template` với `category_id = -222`**; các lần sau tái sử dụng template đã clone | `MessageErrorController.php:864-873`; `app/Template.php:394-…` |
| BR-10 | Template clone (`category_id = -222`) bị **xoá cùng** khi Admin xoá bản ghi lỗi (`type = 3`) | `MessageErrorController.php:948-952`; `app/SendingScheduleSetting.php:113-117` |
| BR-11 | `template_ids` là CSV; phần tử có tiền tố `cap_` trỏ tới `capture_templates`, các phần tử còn lại trỏ tới `template` | `app/Template.php:382-392` |
| BR-12 | Xoá ở tab 「未確認エラー」 (`SCR-ERR-01`) = **xoá hẳn** `message_error`. Xoá ở 2 tab còn lại (`SCR-ERR-02`, `SCR-ERR-03`) = **huỷ đăng ký gửi lại**: xoá row `sending_schedule_setting`, reset `message_error.sending_schedule_id = NULL` và `is_confirmed = 0`, **giữ nguyên bản ghi lỗi**. Xác nhận qua modal `SCR-ERR-06` | `MessageErrorController.php:765-790` |
| BR-13 | Ở tab 「再送登録済み」 (`SCR-ERR-02`), thao tác hàng loạt qua modal 「再送タイミング変更」 (`SCR-ERR-06`) **chỉ cập nhật `send_time`** (dời giờ gửi) chứ không tạo lịch mới | `MessageErrorController.php:1013-1017`, `:1032`, `:1053-1066`; `modal-setting-schedule-all.blade.php:36` |
| BR-14 | Khi chọn "tất cả" (`selectAll = true`) ở tab khác `registered_send`: hệ thống set `status = WAITING` + `date_send` cho toàn bộ bản ghi khớp lọc, rồi **đẩy sang queued job** để tránh timeout | `MessageErrorController.php:1026-1030` |
| BR-15 | `pushSchedule()` chỉ liên kết lịch khi `message_error.sending_schedule_id` đang `NULL` (khoá chống double-booking); thất bại → xoá row lịch vừa tạo và cảnh báo Chatwork | `app/SendingScheduleSetting.php:129-141` |
| BR-16 | `error_end_code` được suy ra từ `error_message` bằng so khớp chuỗi tiếng Nhật; tính lại runtime nếu cột DB rỗng; **không khớp mẫu nào → `'other'`** | `MessageErrorController.php:345-376`; `app/SendingScheduleSetting.php:143-174` |
| BR-17 | Tab 「エラー原因一覧」 (`SCR-ERR-04`) hiển thị bảng mã lỗi gồm **7 mã 001–007 + `other`** = 8 dòng, render tĩnh từ config, **không gọi API** | `config/sns-line.php:1099-1132`; `public/js/error_list/index_v2.js:91-93` |
| BR-18 | Badge số lỗi trên 4 nút nguồn **chỉ hiển thị ở tab 「未確認エラー」** (`SCR-ERR-01`); hiển thị `99+` khi ≥ 100. Ở `SCR-ERR-02` và `SCR-ERR-03` badge luôn ẩn (server trả `0`) | `MessageErrorController.php:223-234`, `:149-152`; `resources/views/basic/error_list/v2/index.blade.php:82-113` |
| BR-19 | Nội dung tin nhắn được dò theo thứ tự `messages_v2s` → `messages` → bảng `messages_{năm}` chọn theo năm của `message_error.created_at` (2020–2025) | `MessageErrorController.php:240-283` |
| BR-20 | Sau mỗi thao tác xoá / đặt lịch hàng loạt, cache `lastErrorMessage{botId}` được ghi lại với TTL **5 phút** để badge thông báo cập nhật | `MessageErrorController.php:793-795`, `:1038-1040`; `ErrorListController.php:1860-1862` |
| BR-21 | `/basic/error-list` (v1) **luôn redirect** sang `/basic/error-list-v2` — màn hình v1 không còn truy cập được | `ErrorListController.php:74` |
| BR-22 | Khi gửi lại thành công ở luồng v1: `bots.free_send_count + 1`, gọi `updateMessageSendCount(botId, today, 3)`, tạo bản ghi `messages` sạch (`has_error = 0`), xoá bản gốc và xoá `message_error` | `ErrorListController.php:1787-1820` |
| BR-23 | Luồng v1 đồng bộ `notify_setting.app_total_msg_error` và `chat_work_total_msg_error` = số `message_error` có `is_confirmed = 0`; **luồng v2 không làm việc này** | `ErrorListController.php:224-225`, `:1817-1818`, `:1846-1847` |
| BR-24 | Không có transaction ở bất kỳ thao tác ghi nào của v2 — `DB::beginTransaction()`/`commit()`/`rollback()` đều bị comment | `MessageErrorController.php:722`, `:794`, `:879`, `:962`, `:975`, `:992`, `:1037`, `:1046` |
| BR-25 | Bản ghi `message_error` có **hai nguồn sinh**: Spring Boot (`SentMessageHelper.saveMessageError()`) cho luồng gửi qua job, và Laravel cho luồng gửi đồng bộ. Phía Laravel có **11 lệnh `create()` nằm trong 7 file**, chia 2 nhóm: **(a)** 6 lệnh thuộc luồng gửi tin chính (`functions.php` ×4, `MessageService.php` ×2) — trong đó 4 lệnh có **guard loại trừ `type ∈ {3, 4, 6}`** để tránh ghi trùng với job, còn `createMessageError()` không guard và nhánh `else` của `MessageService` vẫn ghi type 3/4/6 nhưng **bỏ trống `message_id`**; **(b)** 5 lệnh trong các bản sao `createMessage()` cục bộ ở tầng sales/console — **không truyền `type`** nên luôn rơi về mặc định `1`. ⇒ **Laravel ghi được cả 6 giá trị `type`**. Quy tắc phụ: `type == 5` (`TYPE_TEMPLATE`) luôn bị ép `parent_id = null` | Guard: `app/Helpers/functions.php:3028-3032`, `:3597-3601`, `:8019-8023`, `app/Services/MessageService.php:381-385`. Không guard: `functions.php:3182`. Nhánh `else`: `MessageService.php:397-407`. Nhóm (b): `Services/Sales/SalesService.php:2108`, `Basic/SalesManagementV2Controller.php:4506`, `Console/Commands/HandleBillStripe.php:1259`, `Console/Commands/HandleSendActionTrialV2.php:1262`, `Console/Commands/Recover.php:257`. Ép `parent_id`: `functions.php:3025-3027`, `:3178-3180`, `:3593-3595`, `:8013-8015`, `MessageService.php:375-377`. Chi tiết §2.4 |
| BR-26 | Bản ghi sinh từ `SalesService.php:2108`, `HandleBillStripe.php:1259`, `HandleSendActionTrialV2.php:1262`, `Recover.php:257` **không ghi `error_code` lẫn `error_end_code`** ⇒ (1) `getEndCode()` chạy runtime không khớp mẫu nào nên luôn trả `'other'` → UI hiện fallback 「上記以外の場合」; (2) task Spring Boot `HandleGetMessageError` poll theo `error_code = 'reach_limit_line'` nên **không bao giờ nhặt được** chúng để nâng cấp thành mã `001`/`002`/`003`. Dù bản chất là lỗi chạm hạn mức LINE, chúng kẹt vĩnh viễn ở mã `other`. **Ngoại lệ**: `SalesManagementV2Controller.php:4506` **có** ghi đủ hai cột nên không dính lỗi này | `SalesService.php:2096-2099` vs 7 mẫu tại `MessageErrorController.php:349-355`; `HandleGetMessageError.java:33`; `models/linedb/entities/MessageError.java:12`; `SalesManagementV2Controller.php:4493-4512` |

---

## 9. Dấu hiệu background job (dành cho agent `job-analyzer`)

### 9.1. Laravel Queued Job

| Hạng mục | Giá trị |
|----------|---------|
| Class | `App\Jobs\SettingScheduleMessageErrorJob` |
| File | `app/Jobs/SettingScheduleMessageErrorJob.php` (94 dòng) |
| Traits | `Dispatchable`, `InteractsWithQueue`, `Queueable`, `SerializesModels`; implements `ShouldQueue` |
| Dispatch tại | `app/Http/Controllers/Basic/MessageErrorController.php:1030` |
| Cú pháp dispatch | `dispatch(new SettingScheduleMessageErrorJob($botId, $type, $errorTab, $errorType))->onConnection('database')` |
| Connection queue | **`database`** → bảng `jobs` (Laravel queue driver database) |
| Queue name | Mặc định (`default`) — không gọi `onQueue()` |
| Payload | `int $botId`, `int $type` (1/2/3), `string $errorTab`, `string $errorType` |
| Điều kiện dispatch | Chỉ khi `selectAll == 'true'` **và** `errorTab != 'registered_send'` |

**Logic `handle()`** (`app/Jobs/SettingScheduleMessageErrorJob.php:41-92`):

1. Query `message_error` với `bot_id`, `status = STATUS_HANDLED['WAITING']` (= 1), loại `Failed to send messages` (`:42-46`).
2. Lọc `type` theo `errorType` (`:47-55`) và join `sending_schedule_setting` lọc theo `errorTab` (`:57-67`).
3. Đếm tổng, chia lô `limit = 1000`, `maxTurn = ceil(count / 1000)` để tránh vòng lặp vô hạn (`:68-75`).
4. Mỗi lô gọi `SendingScheduleSetting::handleScheduleMsgErrors($botId, $ids, $type)` — **không truyền `dateSend`/`timeSend`**, nên hàm này tự đọc `message_error.date_send` (`app/SendingScheduleSetting.php:31-32`). Đây chính là lý do controller phải `UPDATE message_error SET date_send = ...` **trước khi** dispatch.
5. Kết quả: ghi hàng loạt row vào `sending_schedule_setting`.

> **Bug tiềm ẩn (Trung bình)**: vòng `while` tại `:76-91` dùng `$lastErrorMessage->id` cố định (lấy 1 lần trước vòng lặp tại `:74`) và **không cập nhật con trỏ sau mỗi lô** — mỗi turn lấy lại cùng tập `id <= $lastErrorMessage->id`. Vòng lặp chỉ dừng nhờ `$maxTurn` hoặc nhờ các bản ghi đã đổi `status` sang `DONE` nên rơi khỏi điều kiện `status = WAITING`. Cần `job-analyzer` xác minh hành vi thực tế.

### 9.2. Bảng queue được ghi → cầu nối sang Spring Boot

| Bảng | Ghi bởi | Đọc bởi | Cột khoá |
|------|---------|---------|----------|
| **`sending_schedule_setting`** | `MessageErrorController::saveSettingErrorMessage()` (`:891`, `:930`); `SendingScheduleSetting::handleScheduleMsgErrors()` (`:76`, `:99`); `updateTimeSend()` (`:1058-1062`) | **Spring Boot** `SendingScheduleTask` | `is_sent` (`0` = chờ gửi, `1` = đã gửi, `-1` = khoá tạm), `send_time` (epoch ms), `send_type` |
| `jobs` (Laravel queue, connection `database`) | `dispatch(...)->onConnection('database')` | Laravel queue worker | — |

### 9.3. Consumer phía Spring Boot (đã xác định)

| Hạng mục | Đường dẫn |
|----------|-----------|
| Task | `src/job/linect-service/src/main/java/sns/line/task/SendingScheduleTask.java` |
| Entity | `src/job/linect-service/src/main/java/sns/line/models/linedb/entities/SendingScheduleSetting.java` |
| Repository | `src/job/linect-service/src/main/java/sns/line/models/linedb/repository/SendingScheduleSettingRepository.java` |
| Đăng ký repository | `src/job/linect-service/src/main/java/sns/line/models/ShareDbRepository.java` |
| Tham chiếu khác | `src/job/linect-service/src/main/java/sns/line/threads/notify/HandleWebpushTask.java` |

Hành vi quan sát được (mức tin cậy **Cao**, đọc trực tiếp `SendingScheduleTask.java`):

| Bước | Dòng | Nội dung |
|------|------|----------|
| 1 | `:42` | `findTop100ByIsSentAndSendTimeLessThanEqual(SendingScheduleSetting.IS_WAIT_SEND, System.currentTimeMillis())` — lấy tối đa **100 bản ghi/lượt** đến hạn gửi |
| 2 | `:51` | `updateIsSent(item.getIsSent(), item.getId())` — đánh dấu đang xử lý |
| 3 | `:67` | `findBotAndLineUserConversation(botId, lineUserId)` — dựng conversation để gửi |
| 4 | `:96` | `save(item)` — cập nhật trạng thái sau khi gửi |
| 5 | `:98` | `messageErrorRepository.removeById(item.getMessageErrorId())` — **xoá bản ghi `message_error`** sau khi gửi lại thành công |

> Bước 5 giải thích BR-06: tab 「再送済み履歴」 phải đọc từ `sending_schedule_setting` vì `message_error` tương ứng đã bị job xoá.

### 9.4. Các điểm ghi khác đáng theo dõi

| Vị trí | Bảng/đích | Ghi chú |
|--------|-----------|---------|
| `MessageErrorController.php:793-795`, `:1038-1040`; `ErrorListController.php:1860-1862` | Cache key `lastErrorMessage{botId}` (TTL 5 phút) | Không phải queue, nhưng ảnh hưởng badge thông báo |
| `ErrorListController.php:1857-1859` | `bots.last_time_show_message_error` | Mốc so sánh để hiện badge lỗi mới |
| `ErrorListController.php:224-225`, `:1817-1818`, `:1846-1847` | `notify_setting.app_total_msg_error`, `notify_setting.chat_work_total_msg_error` | Nguồn cho push notification app + thông báo Chatwork — **chỉ luồng v1 cập nhật** |
| `ErrorListController.php:1789-1791` | `bots.free_send_count` | Đếm số tin miễn phí đã dùng (v1) |
| `ErrorListController.php:1794` | `updateMessageSendCount($botId, today, 3)` | Cập nhật thống kê số tin đã gửi (v1) |
| `app/SendingScheduleSetting.php:139` | `notifyChatwork(...)` | Cảnh báo vận hành khi liên kết lịch thất bại |
| `ErrorListController.php:172-174` | `event(new InfoEvent(...))` | Broadcast realtime cập nhật badge (v1) |
| Không phát hiện | `action_line_users`, `sync_elasticsearch`, `broadcast` (ghi), `sendAction()` | Tính năng này **không** ghi vào các queue table đó. Tin cậy **Cao** (grep 2 controller + model + job) |

---

## 10. Tổng kết kỹ thuật

| Hạng mục | Kết luận | Tin cậy |
|----------|----------|---------|
| Controller chính | `Basic\MessageErrorController` (v2) — 15 method, 6 method có route | **Cao** |
| Controller legacy | `Basic\ErrorListController` — vẫn còn 7 route nhưng UI v2 chỉ dùng `updateLastTimeShowError` | **Cao** |
| Bảng DB chính | `message_error` (nguồn lỗi), `sending_schedule_setting` (hàng đợi gửi lại) | **Cao** |
| Nguồn sinh `message_error` | **Hai nguồn**: Spring Boot `SentMessageHelper.saveMessageError()` + **11 lệnh `create()` trong 7 file** phía Laravel — nhóm (a) 6 lệnh luồng gửi tin chính (`functions.php` ×4, `MessageService.php` ×2, có 53 vị trí gọi truyền `type_message_error`), nhóm (b) 5 lệnh trong bản sao `createMessage()` cục bộ ở sales/console (không truyền `type` → luôn `= 1`). Xem §2.4, BR-25, BR-26 | **Cao** |
| Bảng DB phụ | `template` (`category_id = -222`), `capture_templates`, `source_messages`, `line_user`, `broadcast`, `step_message`, `scenario`, `bots`, `notify_setting`, và 10 bảng `messages*` trên 3 connection | **Cao** |
| Background job | **Có** — `SettingScheduleMessageErrorJob` (Laravel, queue `database`) và `SendingScheduleTask` (Spring Boot, poll bảng `sending_schedule_setting`) | **Cao** |
| Queue table cầu nối | **`sending_schedule_setting`** | **Cao** |
| Validation | **Không có** ở tầng server | **Cao** |
| Transaction | **Không có** ở v2 (đều bị comment) | **Cao** |
| Authorization | Không Policy/Gate; phân tách bot bằng `getBotId()` nhưng **thiếu ở EP-03, EP-04 (type 1/2), EP-05 (đường list)** | **Cao** (phát hiện) / **Trung bình** (mức nghiêm trọng thực tế) |
