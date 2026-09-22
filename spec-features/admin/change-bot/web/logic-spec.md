# FA-044 — Change Bot / Đổi LINE Official Account (LOA変更) — Logic Spec

> **Nguồn phân tích (v2)**
> - Web: `src/web/sns-line` @ nhánh **`release_step_20260805`**, commit **`da839e26e4`** (2026-08-18)
> - Job: `src/job/linect-service` @ nhánh **`release-t07-2026`**, commit **`debe45bc`** (2026-08-13)
> - Ngày cập nhật spec: **2026-08-19**
>
> **Phạm vi**: `Ajax\ChangeBotController`, `App\Services\PlanLimitGuard`, model `ScheduleChangeBot`, view `change_bot_new/`, JS `change_new.js`, cùng nhánh đổi LOA (nay mồ côi) trong `BotController@step2CheckFriend`.
> Xem `web/api-spec.md` cho hợp đồng HTTP; file này mô tả logic nghiệp vụ, model, quy tắc, ranh giới với worker và cảnh báo.
>
> ⚠ **Tính năng ĐÃ HOÀN THIỆN và ĐANG CHẠY PRODUCTION.** Bản spec v1 kết luận sai điều ngược lại — xem mục **10. Nợ kỹ thuật & Cảnh báo**, nhóm (a) và (c).
>
> Mức tin cậy mặc định: **Cao** (đọc trực tiếp source).

---

## 1. Tổng quan luồng nghiệp vụ

Tính năng cho phép Admin đang vận hành một LINE Official Account (LOA) thay thế nó bằng một LOA khác, giữ nguyên dữ liệu bạn bè / kịch bản trong hệ thống LME.

Toàn bộ luồng chạy **trong một trang SPA** (`change_bot_new/index.blade.php` + `change_new.js`):

```
GET /admin/change-bots-new/{hash}                      (BotController@adminChangeNewBot)
      │
      │ GET  /admin/ajax/change-bot/init               → cờ campaign, reservation, tiến độ
      ▼
[campaign] → [select]  chọn immediate | scheduled
      │  goToInput()  (change_new.js:157) — đặt currentStep = 'input', KHÔNG rời trang
      ▼
[input]  nhập 4 credential LOA mới
      │  (nền) POST /admin/ajax/change-bot/set-webhook   debounce 600ms
      │  POST /admin/ajax/change-bot/validate            → thông tin OA + webhook_url
      ▼
[webhook] hiển thị Webhook URL để copy + hướng dẫn bật webhook
      │  POST /admin/ajax/change-bot/check-webhook       → xác nhận webhook đang bật
      ▼
[confirm] xem lại thông tin
      │  POST /admin/ajax/change-bot/execute             → INSERT schedule_change_bots
      ├─ type=immediate  → status = WAITING(1) → [processing]
      │                     GET /admin/ajax/change-bot/progress (poll 3s)
      └─ type=scheduled  → status = DRAFT(0)   → [reservation]
                              ├─ POST .../delete-reservation   → CANCEL(5)
                              └─ POST .../execute-reservation  → WAITING(1) → [processing]
```

Từ trạng thái `WAITING(1)` trở đi, xử lý được **worker Spring Boot `ChangeBotTask`** đảm nhận (xem mục 5 và 11).

---

## 2. Controllers & Actions

### 2.0 `Ajax\ChangeBotController::botCanChangeBot()` (private) — **MỚI [#39230]**
`src/web/sns-line/app/Http/Controllers/Ajax/ChangeBotController.php:26-37`

```php
private function botCanChangeBot($bot, $type = null)
{
    $isFreePlan = (int) $bot->plan_type === 2;
    if (!$isFreePlan) return true;                       // gói trả phí: không giới hạn
    if ($type === null || $type === ScheduleChangeBot::TYPE['SCHEDULED']) return false;
    return Carbon::now()->lt(Carbon::parse($bot->created_at)->addMonth()->endOfDay());
}
```

| Trường hợp | Kết quả |
|---|---|
| Bot **trả phí** (`plan_type != 2`) | `true` — không giới hạn |
| Bot **free** + `$type = null` (luồng chạy lịch đã đặt) | `false` |
| Bot **free** + `$type = SCHEDULED(2)` | `false` — free không được đặt lịch |
| Bot **free** + `$type = IMMEDIATE(1)` | `true` **chỉ khi** `now < bots.created_at + 1 tháng` (cuối ngày) |

- Comment trong code ghi rõ đây là **mirror** rule vốn chỉ tồn tại ở màn hình (`ChangeBotController@init` + `BotController@adminChangeBotSub`).
- Chú ý: hàm này dùng **`(int) $bot->plan_type === 2`** (đã ép kiểu), trong khi `init()` (`:59`, `:88`) và `adminChangeBotSub()` (`BotController.php:7307`) vẫn dùng so sánh nghiêm ngặt `$bot->plan_type === 2` chưa ép kiểu — xem TD-B03.

### 2.1 `Ajax\ChangeBotController@init`
`ChangeBotController.php:39-99`

1. `$botId = getBotId()` — đọc `Session::get('current_bot_id')` (`app/Helpers/functions.php:386-390`). **Không tin `bot_id` từ client.**
2. Khởi tạo `$reservation` rỗng mặc định (`:42`).
3. `Bots::where('id', $botId)->where('is_deleted', 0)->first()`; rỗng → `throw new HttpException(404, 'Bot not found')` (**early return**, `:43-44`).
4. Tính mảng `$status`: mặc định `[DRAFT, PROCESSING]`; nếu `type === 'change_sub'` thêm `DONE` (`:49-52`).
5. `ScheduleChangeBot::where('bot_id', $botId)->orderBy('id', 'DESC')->first()` — **`whereIn('status', $status)` vẫn bị comment** (`:54`) ⇒ `$status` là biến chết, truy vấn luôn lấy bản ghi mới nhất bất kể trạng thái.
6. `$campaignChangeBot = Carbon::parse($bot->created_at)->addMonth()->endOfDay()` (`:58`).
7. `$hasCampaign = $bot->plan_type === 2 && Carbon::now()->lt($campaignChangeBot)` (`:59`).
8. Nếu có `$schedule`: gọi 4 API LINE bằng **credential LOA MỚI đã lưu trong DB** để dựng khối `reservation` (`:62-82`); `$isProcessing = ($schedule->status === PROCESSING)`; `$progress = $schedule->progress`; `$scheduleId = $schedule->id`.
9. Trả JSON, **bao gồm nguyên object `$schedule`** (`:95`).

**Side effects**: không ghi DB; 4 HTTP request đồng bộ ra LINE mỗi lần gọi.

### 2.2 `Ajax\ChangeBotController@validateChannel`
`ChangeBotController.php:101-154`

1. `ChangeBotRequest` chạy trước thân method (validation + rule "channel_id chưa được kết nối").
2. `$params = $request->only([...4 credential])` (`:103`).
3. `lineChanelAccessToken($params)` → rỗng → early return 「入力した情報に誤りがありますので、…」 (`:105-106`).
4. `lineFollowers($channelAccessToken)` (`:108`).
5. `getLineInfoBot(...)` → rỗng → early return 「認証できませんでした。」 (`:111-112`); thiếu `userId` → early return 「入力した情報が間違っています。再確認してください。」 (`:114`).
6. `lineLoginAccessToken($params)` → rỗng → early return (`:117-118`).
7. `getLimitMessageLine(...)` → `planLOA(..., true)` → tên gói tiếng Nhật (`:120-121`).
8. **Tính `webhook_url`** (`:127`): `env('DOMAIN_ENDPOINT_WEBHOOK') . 'line/callback/add/0'`, fallback `url('line/callback/add/0')`.
9. Trả JSON kèm **channel access token thô của cả 2 channel** + secret dạng masked + `webhook_url`.

> **Khác bản v1**: đoạn `checkWebhook()` đã bị **gỡ khỏi method này** và tách ra `checkWebhookEnabled()`.

**Side effects**: chỉ đọc, không ghi DB. Vẫn **rò rỉ access token ra front-end** (xem TD-B01).

### 2.3 `Ajax\ChangeBotController@checkWebhookEnabled` — **MỚI**
`ChangeBotController.php:156-174`

1. `$request->only(['channel_id', 'channel_secret'])`; thiếu → early return 「入力情報が不足しています。」 (`:159-161`).
2. `lineChanelAccessToken(...)` → rỗng → early return 「入力した情報に誤りがありますので、入力情報を再度ご確認ください。」 (`:163-166`).
3. `checkWebhook($channelAccessToken)` → false → early return 「Webhookをオンにして下さい。 既にオンの場合は、一度オフにしてから再度オンに変更して下さい。」 (`:168-171`).
4. Trả `{"success": true}`.

**Side effects**: chỉ đọc (GET webhook endpoint trên LINE). Không dùng FormRequest ⇒ không có rule `max:500`.

### 2.4 `Ajax\ChangeBotController@setWebhook`
`ChangeBotController.php:176-194`

1. `$request->only(['channel_id', 'channel_secret'])`; thiếu → early return 「入力情報が不足しています。」 (`:179-181`).
2. `lineChanelAccessToken(...)` → rỗng → early return (`:183-186`).
3. `setWebhookUrl($channelAccessToken)` → false → early return 「Webhookエンドポイントの設定に失敗しました」 (`:188-191`).
4. Trả `{"success": true}`.

**Side effects**: **ghi cấu hình trên hệ thống LINE** (PUT webhook endpoint của LOA mới). Không ghi DB LME.

### 2.5 `Ajax\ChangeBotController@execute` — đường tạo bản ghi chính
`ChangeBotController.php:196-281`

1. `ChangeBotRequest` chạy trước (validation + rule trùng LOA).
2. `$botId = getBotId()`; `$request->input('bot_id') != $botId` → 404 (**early return**, `:199`).
3. `Bots::find($botId)`; rỗng hoặc `is_deleted` → 404 (`:200-201`).
4. `$attributes = $request->only([...4 credential mới])` (`:202`).
5. `$type = ScheduleChangeBot::TYPE[strtoupper($request->input('type'))]` (`:203`) — **không kiểm tra key tồn tại**.
6. **[#39230] Guard gói cước**: `!$this->botCanChangeBot($bot, $type)` → `logInfo('[#39230] changeBot.execute chan boi gioi han goi', [...])` + trả `{"success": false, "msg": "現在のプランは利用できない機能です。アップグレードが必要になります。"}` HTTP 200 (**early return**, `:208-218`).
7. **Pre-check chống trùng (BR-01)**: tìm bản ghi cùng `bot_id` với `status ∈ {DRAFT, WAITING, PROCESSING}`; có → `logInfo` + trả `{"success": false, "msg": "LOA変更処理中のため、…"}` (`:221-231`).
8. `ScheduleChangeBot::create([...])` — snapshot 4 credential **CŨ** từ `$bot` + 4 credential **MỚI** từ request; `status = DRAFT(0)` nếu `SCHEDULED`, `= WAITING(1)` nếu `IMMEDIATE`; `type = $type` (`:232-244`).
9. **[#39230] Chống race condition (post-check)**: `PlanLimitGuard::rollbackIfOverLimit($botId, PlanLimitGuard::FEATURE_CHANGE_BOT, <query active của bot>, $schedule->id, 1, fn => $schedule->delete())` (`:248-261`). Trả `true` ⇒ đã xoá bản vừa tạo ⇒ trả `{"success": false, "msg": "LOA変更処理中のため、…"}` (`:262-264`).
10. Nhánh `SCHEDULED` → trả khối `reservation` **hardcode** + object schedule (`:266-279`).
11. Nhánh `IMMEDIATE` → trả `{"processing": true, "schedule": ...}` (`:280`).

**Side effects**: INSERT 1 dòng `schedule_change_bots` (có thể bị DELETE lại ngay ở bước 9). **Không có `DB::transaction`** — chấp nhận được vì chỉ 1 write, và `PlanLimitGuard` được thiết kế để chạy **ngoài** transaction (xem mục 4).

### 2.6 `Ajax\ChangeBotController@progress`
`ChangeBotController.php:283-291`

1. Tìm schedule theo `bot_id` (session) **và** `schedule_id` (request) — scope kép, chống IDOR (`:286`).
2. Không tìm thấy → 404 `Schedule not found` (`:287`).
3. `status ∈ {ERROR, CANCEL}` → trả `{"success": false, "message": "ERROR", "message_error": ...}` (`:288`).
4. Ngược lại trả `progress`, `completed = (status === DONE)`, `confirm_data = null` (hardcode) (`:290`).

**Side effects**: chỉ đọc.

### 2.7 `Ajax\ChangeBotController@deleteReservation`
`ChangeBotController.php:294-303` (comment `/** TODO: replace with real DB deletion */` tại `:293`)

1. Tìm schedule theo `bot_id` + `schedule_id`; rỗng → 404 (`:297-298`).
2. **Không kiểm tra trạng thái nguồn** — gán thẳng `status = CANCEL(5)` rồi `save()` (`:299-300`).
3. Trả 「接続予約を削除しました」.

**Side effects**: UPDATE 1 dòng. Là soft-cancel, không xoá bản ghi (tên method gây hiểu nhầm).

### 2.8 `Ajax\ChangeBotController@executeReservation`
`ChangeBotController.php:306-343` (comment `/** TODO: replace with real execution logic */` tại `:305`)

1. `$botId = getBotId()`; `$bot = Bots::find($botId)`.
2. **[#39230] Guard gói cước**: `empty($bot) || !$this->botCanChangeBot($bot)` — gọi **không truyền `$type`** ⇒ mọi bot free bị chặn — → `logInfo` + trả 「現在のプランは利用できない機能です。アップグレードが必要になります。」 (`:310-317`).
3. Bot **không** được có bản ghi nào ở `WAITING`/`PROCESSING`; có → early return 「LOA変更処理中のため、…」 (`:318-319`).
4. Tìm schedule theo `bot_id` + `schedule_id`; rỗng → 404 (`:321-322`).
5. **BR-02'**: `Bots::where('channel_id', $schedule->channel_id_new)->where('is_deleted', 0)` — có → early return 「このLINE公式アカウントは、すでにL Messageに接続されています。…」 (`:325-328`).
6. **BR-03**: `ScheduleChangeBot::where('id', '<>', $schedule->id)->where('channel_id_new', ...)->where('channel_secret_new', ...)->whereIn('status', [WAITING, PROCESSING])` — có → early return 「LOA変更処理中のため、…」 (`:330-337`).
7. Gán `status = WAITING(1)` + `save()`; trả `{"processing": true}` (`:339-342`).

**Side effects**: UPDATE 1 dòng. **Không kiểm tra trạng thái nguồn phải là `DRAFT`** → vẫn có thể "hồi sinh" bản ghi `CANCEL`/`ERROR`/`DONE`.

### 2.9 `Admin\BotController@adminChangeNewBot`
`BotController.php:7256-7273`

1. `Hashids::decode($request->id)[0]` → `$botId` (null nếu hash sai) (`:7258`).
2. `Bots::find($botId)` (`:7259`).
3. **Guard bảo mật**: `$botId != getBotId() || empty($bot) || !$this->userCanAccessChangeBot($botId)` → `redirect('/basic/overview')` (`:7262-7264`).
4. Trả view `admin.bots.change_bot_new.index` với `bot_slot_id`, `type`, `typeChange`, `bot_id`, `username`, `hash_id`, `changeSuccess` (`:7271`).

> Dòng `return view('admin.bots.change_new_bots', ...)` của thế hệ cũ đã bị comment tại `:7272`.

### 2.10 `Admin\BotController@adminChangeBotSub` *(mồ côi)*
`BotController.php:7275-7299`

1. Cùng guard bảo mật (`:7281-7283`).
2. **Guard gói cước phía màn hình** (`:7286-7292`):
   - `$isFreePlan = $bot->plan_type === 2` (`:7288`)
   - `$hasCampaign = $isFreePlan && Carbon::now()->lt(Carbon::parse($bot->created_at)->addMonth()->endOfDay())` (`:7289`)
   - `if ($isFreePlan && ($typeChange === 'scheduled' || !$hasCampaign))` → view `admin.bots.change_bot_plan_blocked` (`:7290-7292`).
3. Trả view `admin.bots.bot_add_v3` (`:7298`).

> Method này **không còn đường vào từ UI** (xem api-spec mục 2). Vẫn giữ lại trong code.

### 2.11 `Admin\BotController@userCanAccessChangeBot` (private)
`BotController.php:7306-7316`

- Cho phép nếu `Bots::where('id', $botId)->where('admin_id', Auth::id())->exists()` (owner).
- Hoặc `UserStaffBot::where('bot_id', $botId)->where('user_invite_id', Auth::id())->where('status', UserStaffBot::STATUS_ACCEPT)->exists()` (staff đã accept lời mời).
- Comment trong code ghi rõ: "Mirror đúng rule của danh sách bot ở `BotV2Controller@getListBotFree`".

### 2.12 `Admin\BotController@step2CheckFriend` — nhánh đổi LOA *(mồ côi)*
`BotController.php:4738-...`, phần FA-044: `:4756-4830`

1. `$bot` = bot MỚI (`bot_id`), `$botOld` = bot CŨ (`botIdChange`) (`:4741-4742`, `:4790`).
2. Kiểm tra người dùng test đã kết bạn LOA mới qua `bot_line_user` + `landing_id` (`:4753`).
3. Nếu đã kết bạn **và** `botIdChange` có giá trị:
   - Gửi tin 「新規接続が完了しました！…」 qua `MessageService::createMessageV2` (`:4775`).
   - Tăng `bots.free_send_count` + `updateMessageSendCount(...)` (`:4777-4783`).
   - `bot_line_user.is_tester = 1`, `Landing::forceDelete()` + `Landing::removeItemLanding()` (`:4784-4787`).
   - `$type = ScheduleChangeBot::TYPE[strtoupper($request->input('type_change'))]` (`:4792`).
   - **Pre-check chống trùng** giống `execute()` (`:4795-4801`); có bản ghi active → `logInfo` + trả `{"success": false, "msg": "LOA変更処理中のため、…"}` (`:4817-4818`).
   - Không có → `ScheduleChangeBot::create([...])` với credential CŨ từ `$botOld`, credential MỚI từ `$bot` (đọc từ DB, không phải từ request) (`:4803-4814`).
4. Trả `{"success": true, "changeBot": true, "botIdChange": ..., "bot_id_new": ...}` (`:4822-4829`).

**Side effects**: gửi tin nhắn LINE thật, cập nhật `bots`, `bot_line_user`, `landing`, các bảng `messages*`, INSERT `schedule_change_bots`. **Không bọc `DB::transaction`. Không có guard `#39230`. Không dùng `PlanLimitGuard`.**

---

## 3. Models Eloquent

### 3.1 `App\ScheduleChangeBot`
`src/web/sns-line/app/ScheduleChangeBot.php` (29 dòng)

| Thuộc tính | Giá trị |
|-----------|---------|
| Bảng | `schedule_change_bots` (theo convention, không khai báo `$table`) |
| Kết nối | `mysql` (mặc định) |
| `$guarded` | `[]` (`:10`) — **cho phép mass assignment mọi cột** ⚠ |
| Timestamps | Bật (mặc định) |
| `TYPE` | `IMMEDIATE => 1`, `SCHEDULED => 2` (`:11-14`) |
| `STATUS` | `DRAFT => 0`, `WAITING => 1`, `PROCESSING => 2`, `DONE => 3`, `ERROR => 4`, `CANCEL => 5` (`:16-23`) |
| Accessor | `getCreatedAtAttribute(): string` → `Carbon::parse($this->attributes['created_at'])->format('Y-m-d H:i:s')` (`:25-28`) |

> ⚠ **Mass assignment**: `$guarded = []` khiến `create()`/`fill()` chấp nhận mọi cột, kể cả `status`, `progress`, `message_error`. Hiện các chỗ gọi đều dựng mảng thủ công nên chưa khai thác được, nhưng bất kỳ chỗ nào truyền thẳng `$request->all()` vào model này sẽ thành lỗ hổng.

> ⚠ **Accessor `created_at`**: `$schedule->created_at` **không còn là Carbon** mà là chuỗi đã format ⇒ mọi so sánh ngày phải `Carbon::parse()` lại (code đã làm ở `ChangeBotController.php:270`). Nếu `created_at` null thì `Carbon::parse(null)` trả về thời điểm hiện tại — sai âm thầm.

**Cấu trúc bảng** (từ `database/migrations/2026_04_17_125226_create_schedule_change_bots_table.php` + `2026_06_06_131356_add_message_error_to_schedule_change_bots_table.php`):

| Cột | Kiểu | Ghi chú |
|-----|------|---------|
| `id` | `increments` | PK |
| `bot_id` | int nullable | Bot **CŨ** đang được thay thế |
| `type` | tinyint nullable | comment `1: now, 2: schedule` |
| `channel_id` | varchar(500) nullable | Messaging API channel LOA **cũ** |
| `channel_secret` | varchar(500) nullable | **plaintext** |
| `channel_id_line_login` | varchar(500) nullable | LINE Login channel LOA cũ |
| `channel_secret_line_login` | varchar(500) nullable | **plaintext** |
| `channel_id_new` | varchar(500) nullable | Messaging API channel LOA **mới** |
| `channel_secret_new` | varchar(500) nullable | **plaintext** |
| `channel_id_line_login_new` | varchar(500) nullable | LINE Login channel LOA mới |
| `channel_secret_line_login_new` | varchar(500) nullable | **plaintext** |
| `status` | tinyint nullable | comment `0: draft, 1: waiting, 2: processing, 3: done, 4: error` (**thiếu `5: cancel`**) |
| `progress` | int nullable default 0 | Chỉ **worker** ghi |
| `message_error` | text nullable | ⚠ **KHÔNG bên nào ghi** — Laravel không ghi, và entity JPA `ScheduleChangeBot.java` (15 field) **không khai báo field `messageError`** nên worker cũng không ghi. Cột luôn NULL, xem cảnh báo bên dưới |
| `created_at` / `updated_at` | timestamp | |

> **Không có index** nào ngoài PK — các truy vấn `where('bot_id')`, `whereIn('status')`, `where('channel_id_new')` (BR-01/BR-03) sẽ full-scan khi bảng lớn. Mức tin cậy: **Cao** (migration không khai báo index).

### 3.2 `App\Bots`
`src/web/sns-line/app/Bots.php`

| Thuộc tính | Giá trị |
|-----------|---------|
| Bảng | `bots` |
| `$guarded` | `[]` — mass assignment mở |
| `$appends` | `['hash_botId']` — accessor `getHashBotIdAttribute()` trả `Hashids::encode(id)`, dùng cho URL `/admin/change-bots-new/{hash}` |

Cột được FA-044 dùng: `id`, `admin_id`, `is_deleted`, `plan_type` (2 = gói Free), `created_at`, `channel_id`, `channel_secret`, `channel_id_line_login`, `channel_secret_line_login`, `free_send_count`.

> Cột `bots.campaign_change_bot` (migration `2026_04_20_165013_add_campaign_change_bot_for_bots_table.php`) **không có code nào đọc/ghi** — logic campaign luôn tính lại từ `created_at + 1 tháng`. Cột chết.

### 3.3 `App\UserStaffBot`
Dùng trong `userCanAccessChangeBot()` — kiểm tra `bot_id`, `user_invite_id`, `status = STATUS_ACCEPT`.

---

## 4. Services — `App\Services\PlanLimitGuard` (**MỚI [#39230]**)

`src/web/sns-line/app/Services/PlanLimitGuard.php` (236 dòng, file mới ở nhánh này)

### Vấn đề mà service giải quyết
Toàn hệ thống dùng pattern `count() → so sánh → insert()`. Hai request song song (mở 2 tab bấm cùng lúc) cùng đọc `count` cũ nên cùng qua cửa ⇒ tạo vượt hạn mức gói. (Doc-block `:5-59`.)

### Cách làm — **không dùng khoá nào**
Doc-block ghi rõ: bản đầu dùng named lock MySQL `GET_LOCK` nhưng bị loại vì dễ degrade (lock gắn với connection; đổi connection / connection pool ⇒ lock biến mất âm thầm) và gây báo nhầm "đang có xử lý khác". **Bản hiện tại KHÔNG dùng named lock, KHÔNG `lockForUpdate` / `SELECT ... FOR UPDATE`, KHÔNG transaction.**

Cơ chế: giữ nguyên pre-check trước khi tạo, rồi **sau khi INSERT** chạy **một câu `count()` thường** để đếm lại; nếu bản ghi vừa tạo nằm ngoài hạn mức thì **xoá chính nó** và báo lỗi.

### API công khai

| Method | Chữ ký | Ý nghĩa |
|---|---|---|
| `isOverLimit($query, $newId, $limit, $idColumn = 'id')` | `:100-124` | Đếm số bản ghi cùng phạm vi có `id <= $newId` = **"thứ tự"** của bản ghi vừa tạo. `thứ tự > $limit` ⇒ bản ghi thừa. `$limit === null` hoặc `$newId <= 0` ⇒ trả `false` (không đụng vào). Lỗi query → `logError('[plan-limit] dem lai sau insert that bai')` + trả `false` (không xoá nhầm) |
| `isOverTotal($query, $limit)` | `:141-159` | Bản cho luồng **khôi phục** (restore soft-deleted): đếm **TỔNG** thay vì thứ tự theo id, vì bản khôi phục giữ id cũ |
| `rollbackIfOverTotal($botId, $feature, $query, $limit, callable $rollback)` | `:171-194` | Gọi `isOverTotal`; vượt → `logInfo('[plan-limit] vuot han muc goi sau khi khoi phuc -> huy khoi phuc')` + chạy `$rollback()` |
| `rollbackIfOverLimit($botId, $feature, $query, $newId, $limit, callable $rollback, $idColumn = 'id')` | `:208-235` | **Dùng bởi FA-044.** Gọi `isOverLimit`; vượt → `logInfo('[plan-limit] vuot han muc goi sau khi insert -> xoa ban ghi vua tao', [bot_id, feature, new_id, limit])` + chạy `$rollback()` trong `try/catch` (xoá hụt vẫn trả `true` nhưng `logError`), trả `true` ⇒ caller phải trả lỗi cho user |

### Quy tắc "ai bị xoá"
Xếp theo `id` tăng dần (auto-increment = thứ tự tạo): bản ghi **id nhỏ hơn (tạo TRƯỚC) được GIỮ**, bản ghi **id lớn hơn (tạo SAU) bị XOÁ**, và lỗi báo về đúng màn hình của request tạo sau. Thiết kế này tránh trường hợp "cả hai đều thấy vượt và cùng tự xoá" khi chỉ so tổng số. (Doc-block `:24-28`.)

### Giới hạn đã biết (ghi trong doc-block `:49-58`)
Vì bỏ hết khoá, câu `count()` là đọc thường. Trong MySQL InnoDB mức REPEATABLE READ, lệnh đọc thường chỉ thấy dữ liệu tại thời điểm SELECT đầu tiên của transaction ⇒ **nếu gọi BÊN TRONG `DB::beginTransaction()`**, bản ghi mà request song song commit sau đó sẽ không xuất hiện khi đếm lại ⇒ vẫn có thể lọt khi 2 transaction chồng hoàn toàn. **Ngoài transaction (trường hợp của FA-044) thì chặn được đầy đủ.**

### Hằng số

- `LIMIT_MESSAGE = '上限に達したので、新しく追加できません。'` (`:63`)
- `PLAN_MESSAGE = '現在のプランは利用できない機能です。アップグレードが必要になります。'` (`:66`)
- `FEATURE_CHANGE_BOT = 'change_bot'` (`:85`) — hằng số của FA-044, **chỉ dùng để ghi log**

**Các feature khác dùng chung service này** (hằng `FEATURE_*`, `:68-85`): `richmenu`, `image_richmenu`, `form_answer`, `csv_export`, `qr_code`, `popup`, `action_schedule`, `salon_calendar`, `salon_course`, `salon_staff`, `lesson_calendar`, `lesson_course`, `event_booking`, `item`, `cross`, `conversion`, `staff_management`, `change_bot`.
→ `PlanLimitGuard` là **shared component** cấp service (ứng viên đăng ký vào `features/shared/registry.md`). Mức tin cậy: **Cao**.

### Cách FA-044 dùng
`ChangeBotController.php:248-264` — `$limit = 1` (1 bot chỉ có 1 schedule active), phạm vi đếm = `ScheduleChangeBot::where('bot_id', $botId)->whereIn('status', [DRAFT, WAITING, PROCESSING])`, `$rollback = fn() => $schedule->delete()`.

> Lưu ý ngữ nghĩa: ở FA-044 "hạn mức gói" thực chất là **hạn mức đồng thời** (1 tiến trình đổi LOA tại một thời điểm), không phải hạn mức theo gói cước. Service được tái sử dụng cho mục đích chống race condition.

---

## 5. Form Requests / Validation

### `App\Http\Requests\ChangeBotRequest`
`src/web/sns-line/app/Http/Requests/ChangeBotRequest.php` (44 dòng), kế thừa `App\Http\Requests\BaseRequest`. Áp dụng cho **EP-04** và **EP-06**.

**`rules()`** (`:9-17`)

| Field | Rule |
|-------|------|
| `channel_id` | `required\|max:500` |
| `channel_secret` | `required\|max:500` |
| `login_channel_id` | `required\|max:500` |
| `login_channel_secret` | `required\|max:500` |

**`messages()`** (`:19-31`) — toàn bộ tiếng Nhật:

| Key | Message |
|-----|---------|
| `channel_id.required` | 「チャネルIDを入力してください」 |
| `channel_id.max` | 「チャネルIDは:max文字以内で入力してください」 |
| `channel_secret.required` | 「チャネルシークレットを入力してください」 |
| `channel_secret.max` | 「チャネルシークレットは:max文字以内で入力してください」 |
| `login_channel_id.required` | 「ログインチャネルIDを入力してください」 |
| `login_channel_id.max` | 「ログインチャネルIDは:max文字以内で入力してください」 |
| `login_channel_secret.required` | 「ログインチャネルシークレットを入力してください」 |
| `login_channel_secret.max` | 「ログインチャネルシークレットは:max文字以内で入力してください」 |

**`withValidator()`** (`:33-43`) — rule tuỳ biến chạy sau khi rule cơ bản pass:

```php
$botCheck = Bots::query()->where('channel_id', $this->channel_id)->where('is_deleted', 0)->first();
if ($botCheck) {
    $validator->errors()->add('channel_id',
        'このLINE公式アカウントは、すでにL Messageに接続されています。 ご不明な場合は、サポート窓口までお問い合わせください ');
}
```

**`authorize()`** (`BaseRequest.php:11-14`): luôn `true` — **không có kiểm tra quyền ở tầng FormRequest**.

**`failedValidation()`** (`BaseRequest.php:16-21`): ném `HttpResponseException` trả **HTTP 200** với body `{"success": false, "errors": {...}}` — không dùng 422.

> **Thiếu**: không validate `type` (`in:immediate,scheduled`), không validate `bot_id`, không validate `schedule_id`. `checkWebhookEnabled` và `setWebhook` không dùng FormRequest (chỉ `empty()` inline).

---

## 6. State machine

### `type` (`schedule_change_bots.type`)

| Giá trị | Hằng số | Ý nghĩa | Ai đặt |
|---------|---------|---------|--------|
| 1 | `TYPE['IMMEDIATE']` | Đổi ngay | `execute()` `ChangeBotController.php:203,243`; `step2CheckFriend()` `BotController.php:4792,4813` |
| 2 | `TYPE['SCHEDULED']` | Đặt lịch | như trên, với `'scheduled'` |

### `status` (`schedule_change_bots.status`)

| Giá trị | Hằng số | Ai ĐẶT (Laravel) | Ai ĐẶT (worker Spring Boot) | Ai ĐỌC (Laravel) |
|---------|---------|------------------|------------------------------|------------------|
| 0 | `DRAFT` | `execute()` khi `type = SCHEDULED` — `ChangeBotController.php:242`<br>`step2CheckFriend()` khi `type_change = scheduled` — `BotController.php:4813` | — | `init()` `:49-51`; pre-check `:223`; guard `PlanLimitGuard` `:252`; `step2CheckFriend` `:4797` |
| 1 | `WAITING` | `execute()` khi `type = IMMEDIATE` — `:242`<br>`step2CheckFriend()` khi `type_change = immediate` — `:4813`<br>`executeReservation()` `→ WAITING` — `:339` | — (đọc hàng đợi) | pre-check `:224`, `:318`, `:333`, `:4798`; guard `:253` |
| 2 | `PROCESSING` | ❌ **Không có dòng code Laravel nào gán** | ✅ **Worker `ChangeBotTask` / `ChangeBotJob`** | `init()` `:49-51,70`; pre-check `:225`, `:318`, `:333`, `:4799`; guard `:254`; JS `change_new.js:144` |
| 3 | `DONE` | ❌ **Không có** | ✅ **Worker** | `init()` `:51`; `progress()` `:290` (`completed`) |
| 4 | `ERROR` | ❌ **Không có** | ✅ **Worker** (`markError()` — **chỉ** `SET status = 4, updated_at = NOW()`, **không** ghi `message_error`) | `progress()` `:288`; JS `change_new.js:141-143` |
| 5 | `CANCEL` | `deleteReservation()` — `ChangeBotController.php:299` | — (hằng `STATUS_CANCEL` **không tồn tại** trong entity Java, xem ghi chú) | `progress()` `:288` |

### Cột `progress` và `message_error`
**Không có dòng code Laravel nào ghi** hai cột này — chỉ đọc (`init()` `:71`, `progress()` `:290`, `:288`).

- `progress`: worker ghi thật, 6 mốc `15 / 30 / 45 / 60 / 80 / 100` (xem `job/job-spec.md`).
- `message_error`: ⚠ **không bên nào ghi**. Cột có trong DB (migration `2026_06_06_131356`) nhưng entity JPA `ScheduleChangeBot.java` không khai báo field tương ứng, và `markError()` chỉ set `status = 4`. Laravel vẫn trả cột này cho FE tại `progress()` (`Ajax/ChangeBotController.php:288`) ⇒ **người dùng luôn nhận `null` khi job lỗi**, toast rơi về chuỗi fallback. Đây là lỗi nên báo cho team.

### Sơ đồ chuyển trạng thái

```
   execute() type=SCHEDULED                            deleteReservation()
   step2CheckFriend type_change=scheduled              (KHÔNG kiểm tra trạng thái nguồn)
        │                                                       │
        ▼                                                       ▼
     DRAFT(0) ──executeReservation() ChangeBotController:339──► WAITING(1) ─────► CANCEL(5)
        ▲                                                       ▲       │
        │                                                       │       │  ╔══════ ranh giới Laravel │ worker ══════╗
   execute() type=IMMEDIATE ────────────────────────────────────┘       └─►║  PROCESSING(2) ──► DONE(3)            ║
   step2CheckFriend type_change=immediate                                  ║              └──► ERROR(4) (message_error KHÔNG ghi)║
                                                                          ║  + ghi progress 0→100                  ║
                                                                          ╚═════════════════════════════════════════╝
```

### Ranh giới trách nhiệm Laravel ↔ worker

- **Laravel** chỉ tạo bản ghi và đặt các trạng thái `DRAFT(0)`, `WAITING(1)`, `CANCEL(5)`. Sau đó nó **chỉ đọc** (`progress()` polling).
- **Worker Spring Boot** `sns.line.task.ChangeBotTask` (`src/job/linect-service/src/main/java/sns/line/task/ChangeBotTask.java`) đọc hàng đợi bằng `repo.findTop50ByStatusOrderByIdAsc(ScheduleChangeBot.STATUS_WAITING)` (`ChangeBotTask.java:83`), thực thi qua `sns.line.threads.changebot.ChangeBotJob`, và là bên duy nhất đặt `PROCESSING(2)`, `DONE(3)`, `ERROR(4)` và ghi `progress`. ⚠ Worker **KHÔNG** ghi `message_error`: `ScheduleChangeBotRepository.markError()` chỉ chạy `SET status = 4, updated_at = NOW()`, và entity `ScheduleChangeBot.java` không có field `messageError` (15 field, cũng không khai báo `STATUS_CANCEL = 5`). Mức tin cậy: **Cao** (đã đọc trực tiếp `models/linedb/entities/ScheduleChangeBot.java:13-20` và `models/linedb/repository/ScheduleChangeBotRepository.java`).
- Phân tích chi tiết worker **không thuộc phạm vi file này** — thuộc `job/job-spec.md` (job-analyzer).
- ⚠ Entity Java khai báo `STATUS_DRAFT..STATUS_ERROR` nhưng **không có `STATUS_CANCEL`** — cần job-analyzer xác nhận worker xử lý thế nào với bản ghi bị Laravel chuyển sang `CANCEL(5)` khi đang chạy.

---

## 7. Business Rules

| ID | Quy tắc | Vị trí | Tin cậy |
|----|---------|--------|---------|
| **BR-01** | **Một bot chỉ có tối đa 1 schedule active** (active = `status ∈ {DRAFT(0), WAITING(1), PROCESSING(2)}`). Vi phạm → 「LOA変更処理中のため、変更できません。処理完了後に再度お試しください。」 + `logInfo` | `app/Http/Controllers/Ajax/ChangeBotController.php:221-231`; `app/Http/Controllers/Admin/BotController.php:4795-4818` | Cao |
| **BR-01b** | **[#39230] Chốt chặn sau INSERT (chống race condition)**: sau khi tạo, đếm lại số bản ghi active có `id <= id vừa tạo`; nếu `> 1` thì **xoá bản vừa tạo** và trả lỗi 「LOA変更処理中のため…」. Bản ghi tạo TRƯỚC được giữ | `app/Http/Controllers/Ajax/ChangeBotController.php:248-264`; `app/Services/PlanLimitGuard.php:100-124,208-235` | Cao |
| **BR-02** | **LOA mới không được trùng bot đang hoạt động**: không tồn tại `bots.channel_id = <channel_id mới>` với `is_deleted = 0`. Vi phạm → 「このLINE公式アカウントは、すでにL Messageに接続されています。…」 | `app/Http/Requests/ChangeBotRequest.php:33-43` (EP-04, EP-06); `app/Http/Controllers/Ajax/ChangeBotController.php:325-328` (EP-09) | Cao |
| **BR-03** | **LOA mới không được là target của reservation khác đang chờ/chạy**: không tồn tại `schedule_change_bots` khác có cùng (`channel_id_new`, `channel_secret_new`) và `status ∈ {WAITING, PROCESSING}` | `app/Http/Controllers/Ajax/ChangeBotController.php:330-337` | Cao |
| **BR-04** | **Không thực thi reservation khi bot đang có tiến trình chạy**: bot không được có bản ghi `WAITING`/`PROCESSING` | `app/Http/Controllers/Ajax/ChangeBotController.php:318-319` | Cao |
| **BR-05** | **Webhook của LOA mới phải đang bật** mới đi tiếp từ bước `webhook` sang `confirm`. `checkWebhook()` gọi `GET /v2/bot/channel/webhook/endpoint` và đọc cờ `active`. Vi phạm → 「Webhookをオンにして下さい。 既にオンの場合は、一度オフにしてから再度オンに変更して下さい。」 | `app/Http/Controllers/Ajax/ChangeBotController.php:168-171` (**đã chuyển từ `validateChannel` sang `checkWebhookEnabled`**); helper `app/Helpers/functions.php:4256-4278` | Cao |
| **BR-06** | **Credential Messaging API phải hợp lệ**: lấy được access token qua `POST /v2/oauth/accessToken` và `GET /v2/bot/info` trả object có `userId` | `app/Http/Controllers/Ajax/ChangeBotController.php:105-114` | Cao |
| **BR-07** | **Credential LINE Login phải hợp lệ**: lấy được access token bằng `client_credentials` với `login_channel_id`/`login_channel_secret` | `app/Http/Controllers/Ajax/ChangeBotController.php:117-118`; helper `app/Helpers/functions.php:5844-5868` | Cao |
| **BR-08** | **Điều kiện campaign**: `has_campaign = (bots.plan_type === 2) && (now < bots.created_at + 1 tháng, cuối ngày)` | `app/Http/Controllers/Ajax/ChangeBotController.php:58-59` | Cao |
| **BR-09** | **[#39230 — MỚI] Guard gói cước ở BACKEND**: bot trả phí không giới hạn; bot free (`plan_type = 2`) **chỉ được đổi NGAY** trong campaign 1 tháng kể từ `bots.created_at`, và **KHÔNG được dùng đặt lịch**. Vi phạm → 「現在のプランは利用できない機能です。アップグレードが必要になります。」 + `logInfo('[#39230] ...')`. Áp dụng ở `execute()` và `executeReservation()` | `app/Http/Controllers/Ajax/ChangeBotController.php:26-37` (`botCanChangeBot`), `:208-218` (`execute`), `:309-317` (`executeReservation`) | Cao |
| **BR-09b** | **Guard gói cước phía màn hình** (đã có từ trước, vẫn giữ): `adminChangeBotSub()` trả view `change_bot_plan_blocked` khi bot free chọn `scheduled` hoặc đã hết campaign; JS chặn chọn thẻ 「予約」 (`selectMethod`) | `app/Http/Controllers/Admin/BotController.php:7288-7292`; `public/_assets/modules/change_bots/js/change_new.js:153-155` | Cao |
| **BR-10** | **Quyền truy cập màn hình**: bot trong URL phải trùng bot đang chọn trong session (`getBotId()`), và user hiện tại phải là owner (`bots.admin_id`) hoặc staff đã accept (`user_staff_bots.status = STATUS_ACCEPT`) | `app/Http/Controllers/Admin/BotController.php:7262-7264`, `:7281-7283`, `:7306-7316` | Cao |
| **BR-11** | **Ánh xạ phương thức**: `immediate` → `type = 1`, `status` khởi tạo `WAITING(1)`; `scheduled` → `type = 2`, `status` khởi tạo `DRAFT(0)` | `app/Http/Controllers/Ajax/ChangeBotController.php:203,242`; `app/Http/Controllers/Admin/BotController.php:4792,4813` | Cao |
| **BR-12** | **Tên gói LOA suy ra từ quota tin nhắn LINE**: `< 200` → rỗng; `200–4999` → 「コミュニケーションプラン」; `5000–29999` → `Lite`; `>= 30000` → `Standard` | `app/Helpers/functions.php:4280-4300` (`planLOA` + `planLoaText`) | Cao |
| **BR-13** | **Số bạn bè hiển thị** = `followers - blocks`, lấy từ `GET /v2/bot/insight/followers?date=<hôm nay>` | `app/Http/Controllers/Ajax/ChangeBotController.php:80,134`; helper `app/Helpers/functions.php:5793-5818` | Cao |
| **BR-14** | **Webhook endpoint được ghi đè** thành `env('DOMAIN_ENDPOINT_WEBHOOK') . 'line/callback/add/0'` (fallback `url('line/callback/add/0')`); cùng chuỗi này được trả về FE ở trường `webhook_url` | `app/Helpers/functions.php:5824`; `app/Http/Controllers/Ajax/ChangeBotController.php:127` | Cao |
| **BR-15** | **Bot phải tồn tại và chưa bị xoá** (`bots.is_deleted = 0`) ở các endpoint ghi dữ liệu | `app/Http/Controllers/Ajax/ChangeBotController.php:43-44`, `:200-201` | Cao |
| **BR-16** | **Bản ghi lưu SNAPSHOT credential**: `execute()` chép 4 credential **cũ** từ `bots` và 4 credential **mới** từ request vào `schedule_change_bots` tại thời điểm tạo — worker dùng snapshot này, không đọc lại `bots` | `app/Http/Controllers/Ajax/ChangeBotController.php:232-244` | Cao |

---

## 8. Helpers & LINE API integration

Tất cả nằm trong `src/web/sns-line/app/Helpers/functions.php` (autoload qua `composer.json`).

| Helper | Dòng | Input | Output | Endpoint LINE | Xử lý lỗi |
|--------|------|-------|--------|---------------|-----------|
| `lineChanelAccessToken(array $params)` | `5869-5895` | `channel_id`, `channel_secret` | `string` access token (rỗng khi lỗi) | `POST https://api.line.me/v2/oauth/accessToken` (`grant_type=client_credentials`) | `try/catch` → `logError('get line channel access token error', [...])`, trả `''` |
| `lineLoginAccessToken($params = [])` | `5844-5868` | `login_channel_id`, `login_channel_secret` | `string` access token | `POST https://api.line.me/v2/oauth/accessToken` | `try/catch` → `logError('get line login token error')`. ⚠ Biến `$channelAccessTokenLineLogin` **chỉ khởi tạo BÊN TRONG `try`** — exception sớm ⇒ `return` chạm biến chưa định nghĩa (PHP Notice, và type hint `: string` ép về `''`) |
| `getLineInfoBot($channelAccessToken)` | `273-289` | access token | `array\|null` (`userId`, `displayName`, `basicId`, `pictureUrl`) | `GET https://api.line.me/v2/bot/info` | `try/catch` → `logError('call api get info bot add bot new error')`, trả `null` |
| `lineFollowers(string $token, string $date = '')` | `5793-5818` | access token, ngày (mặc định hôm nay `Ymd`) | `array` (`status`, `followers`, `targetedReaches`, `blocks`) | `GET https://api.line.me/v2/bot/insight/followers?date=YYYYMMDD` | `try/catch` → `logError`, trả mặc định `{status: "unready", followers: 0, targetedReaches: 0, blocks: 0}` |
| `getLimitMessageLine($token)` | `4235-4255` | access token | `int` quota (0 khi lỗi) | `GET https://api.line.me/v2/bot/message/quota` | `try/catch` → `logDebug`, trả `0` |
| `checkWebhook($token)` | `4256-4278` | access token | `bool` cờ `active` | `GET https://api.line.me/v2/bot/channel/webhook/endpoint` | `try/catch` → `logDebug`, trả `false` |
| `setWebhookUrl(string $accessToken)` | `5820-5843` | access token | `bool` | `PUT https://api.line.me/v2/bot/channel/webhook/endpoint` body `{"endpoint": "..."}` | `try/catch` → `logError('set webhook url error')`, trả `false` |
| `planLOA(int $limitMessage, bool $getText = false)` | `4280-4294` | quota | mã gói hoặc text tiếng Nhật | — (thuần tính toán) | — |
| `planLoaText(string $plan)` | `4296-...` | mã gói | 「コミュニケーションプラン」/`Lite`/`Standard`/`''` | — | — |
| `getBotId()` | `386-390` | — | `Session::get('current_bot_id')` | — | Trả `null` nếu chưa chọn bot |
| `getValue($key, $arr)` | `7341-7344` | key, array | giá trị hoặc `null` | — | ⚠ Dùng `array_key_exists` ⇒ **lỗi nếu `$arr` là `null`**; `init()` phòng bằng `?? []` (`:77-81`), `validateChannel()` không phòng nhưng đã early-return khi `$infoBot` rỗng |
| `logInfo($msg, $context = [])` / `logError(...)` | `11573-11574` | — | — | — | Wrapper của `logCommon()` |

**Đặc điểm chung**: mọi helper LINE đều "nuốt" exception và trả giá trị mặc định. Hệ quả: **lỗi mạng/timeout tới LINE bị nhầm thành "credential sai"** và hiện message 「入力した情報に誤りがありますので…」. Mức tin cậy: **Cao**.

---

## 9. Authorization

| Lớp bảo vệ | Áp dụng cho | Chi tiết |
|------------|-------------|----------|
| Middleware `admin_access` | EP-01…EP-09, EP-11 | `app/Http/Middleware/AdminAccess.php:23` — `Auth::check()` và `users.role ∈ {0, 1, 2, -1}`; ghi `user_access_bots` cho staff (`:34-55`) |
| Middleware `check_remember_token` | EP-01…EP-11 | Vô hiệu phiên khi mật khẩu đã đổi ở nơi khác |
| Middleware `check_login` | EP-10 | Xác thực phiên đăng nhập |
| Middleware `https_protocol` | EP-01…EP-09, EP-11 | **No-op** — thân hàm bị comment (`app/Http/Middleware/HttpsProtocol.php:18-20`) |
| CSRF (nhóm `web`) | mọi POST | FE gửi header `X-CSRF-TOKEN` |
| Kiểm tra ownership tường minh | EP-01, EP-02 | `$botId != getBotId()` + `userCanAccessChangeBot()` — `BotController.php:7262-7264`, `:7281-7283` |
| `userCanAccessChangeBot($botId)` | EP-01, EP-02 | Owner (`bots.admin_id = Auth::id()`) **hoặc** staff đã accept (`user_staff_bots.user_invite_id = Auth::id()` và `status = UserStaffBot::STATUS_ACCEPT`) — `BotController.php:7306-7316` |
| Scope theo session | EP-03, EP-07, EP-08, EP-09 | Mọi query bắt đầu bằng `where('bot_id', getBotId())` ⇒ **không thao tác được lên schedule của bot khác** |
| Kiểm tra tham số | EP-06 | `$request->input('bot_id') != getBotId()` → 404 |

**Không có** Laravel Policy / Gate / permission chi tiết theo custom role cho tính năng này. Mọi staff đã accept lời mời đều truy cập được — `userCanAccessChangeBot()` chỉ kiểm tra `STATUS_ACCEPT`, không kiểm tra quyền "change_bot". Mức tin cậy: **Cao**.

**Đánh giá IDOR**: các endpoint AJAX an toàn nhờ scope kép `bot_id` (session) + `schedule_id` (request). Rủi ro còn lại nằm ở việc "bot đang chọn trong session" do luồng khác quyết định, không thuộc tầng này.

---

## 10. Events / Queued Jobs (phía Laravel)

**Không có.** Tính năng **không** dispatch bất kỳ Laravel Job, Event, Listener, Notification hay Console Command nào.

- Grep `ScheduleChangeBot` / `schedule_change_bots` trên `app/`, `routes/`, `database/`, `config/` → chỉ khớp `app/ScheduleChangeBot.php`, `app/Http/Controllers/Ajax/ChangeBotController.php`, `app/Http/Controllers/Admin/BotController.php`.
- Không có entry trong `app/Console/Kernel.php`.
- Không có `dispatch()` / `Queue::push()` / `event()` trong `Ajax\ChangeBotController`.

Việc xử lý nền do **worker Spring Boot** đảm nhận (mục 6 + 12), không qua queue của Laravel. Mức tin cậy: **Cao**.

---

## 11. Nợ kỹ thuật & Cảnh báo

> Chia làm 3 nhóm để người đọc bản spec v1 biết cái gì đã thay đổi.

### (a) Vấn đề của bản cũ **ĐÃ ĐƯỢC VÁ** ở nhánh này

| # | Vấn đề cũ | Cách vá | Vị trí |
|---|-----------|---------|--------|
| FIX-01 | **Thiếu guard gói cước phía backend** — rule "bot free chỉ được đổi trong campaign 1 tháng, không được đặt lịch" chỉ nằm ở màn hình ⇒ POST thẳng endpoint là tạo được `ScheduleChangeBot` dù đã hết campaign | Thêm `botCanChangeBot()` và áp dụng ở `execute()` + `executeReservation()`; trả 「現在のプランは利用できない機能です。アップグレードが必要になります。」 + `logInfo('[#39230] ...')` | `ChangeBotController.php:26-37`, `:208-218`, `:309-317` |
| FIX-02 | **Race condition check-then-insert** ở BR-01 — 2 tab bấm cùng lúc vẫn tạo được 2 bản ghi active | Thêm chốt chặn đếm-lại-sau-INSERT `PlanLimitGuard::rollbackIfOverLimit()`; bản ghi tạo sau bị xoá, user nhận lỗi | `ChangeBotController.php:248-264`; `app/Services/PlanLimitGuard.php` |
| FIX-03 | **`execute()` trả lỗi ở key `msg` trong khi FE đọc `message`** ⇒ user không thấy thông báo lỗi nào | FE nay đọc `r.msg` và hiện toast | `public/_assets/modules/change_bots/js/change_new.js:299-302` |
| FIX-04 | **Bước `input`/`confirm` là code chết**, `goToInput()` redirect sang `/admin/change-bot-sub/...` | `goToInput()` nay đặt `this.currentStep = 'input'`; toàn bộ wizard chạy trong SPA; EP-04/EP-05/EP-06 trở lại là code sống | `change_new.js:157-161` |
| FIX-05 | Kiểm tra webhook nằm lẫn trong `validateChannel` khiến user phải nhập lại credential khi webhook chưa bật | Tách thành endpoint riêng `checkWebhookEnabled` + thêm màn hình `webhook` hiển thị/copy `webhook_url` để user bật webhook rồi bấm 「次へ」 | `ChangeBotController.php:156-174`; `change_new.js:239-257`; `index.blade.php:289` |

### (b) Vấn đề **VẪN CÒN**

| # | Vấn đề | Vị trí | Mức độ |
|---|--------|--------|--------|
| TD-B01 | `validateChannel()` trả **channel access token thô** của cả Messaging API và LINE Login xuống browser (`channel_access_token`, `channel_access_token_line_login`) trong khi UI không dùng tới | `ChangeBotController.php:136-137` | Nghiêm trọng (bảo mật) |
| TD-B02 | **Channel secret lưu plaintext** trong `schedule_change_bots` (4 cột `*_secret*`) và bị **trả nguyên vẹn ra front-end** vì `init()` serialize cả object `$schedule` | migration `2026_04_17_125226_...php`; `ChangeBotController.php:95`, `:232-244`, `:277` | Nghiêm trọng (bảo mật) |
| TD-B03 | So sánh nghiêm ngặt `$bot->plan_type === 2` **chưa ép kiểu** ở `init()` (`:59`, `:88`) và `adminChangeBotSub()` (`BotController.php:7288`). Nếu driver trả cột về dạng `string` (PDO emulate prepares) thì điều kiện luôn `false` ⇒ logic campaign / chặn màn hình im lặng thất bại. `botCanChangeBot()` đã ép `(int)` nên guard backend không bị ảnh hưởng | `ChangeBotController.php:59,88`; `BotController.php:7288` | Trung bình (**Trung bình** — phụ thuộc cấu hình PDO) |
| TD-B04 | `init()` vẫn có `->whereIn('status', $status)` **bị comment** ⇒ `$status` là biến chết, truy vấn luôn trả bản ghi mới nhất kể cả `CANCEL`/`ERROR`/`DONE`. FE phải chữa cháy bằng `if (data.schedule.status != 0 && != 2 …) currentStep = 'select'` | `ChangeBotController.php:54`; `change_new.js:144-148` | Nghiêm trọng |
| TD-B05 | `deleteReservation()` **không kiểm tra trạng thái nguồn** → set `CANCEL` được lên bản ghi đang `PROCESSING` (worker vẫn chạy) hoặc đã `DONE`. Entity Java lại **không có** hằng `STATUS_CANCEL` | `ChangeBotController.php:297-300`; `src/job/.../entities/ScheduleChangeBot.java:13-20` | Nghiêm trọng |
| TD-B06 | `executeReservation()` **không kiểm tra trạng thái nguồn phải là `DRAFT`** → có thể "hồi sinh" bản ghi `CANCEL(5)`/`ERROR(4)`/`DONE(3)` về `WAITING(1)` và cho worker chạy lại | `ChangeBotController.php:339-340` | Nghiêm trọng |
| TD-B07 | `setWebhook()` **ghi đè cấu hình webhook trên LINE Developers** của LOA mới chỉ dựa trên debounce 600ms khi gõ phím — không xác nhận, không FormRequest, không giới hạn tần suất | `ChangeBotController.php:176-194`; `change_new.js:175-194` | Nghiêm trọng |
| TD-B08 | `$type = ScheduleChangeBot::TYPE[strtoupper($request->input('type'))]` — **không validate `type`**. Thiếu hoặc sai giá trị → `Undefined index` → HTTP 500. Lưu ý: dòng này chạy **trước** guard `#39230` nên guard không cứu được | `ChangeBotController.php:203`; `BotController.php:4792` | Trung bình |
| TD-B09 | **Không có `DB::transaction`** ở bất kỳ endpoint nào. `execute()` chỉ 1 write nên chấp nhận được (và `PlanLimitGuard` cố ý được thiết kế để chạy ngoài transaction). Nhưng `step2CheckFriend()` ghi nhiều bảng (`messages*`, `bots`, `bot_line_user`, `landing`, `schedule_change_bots`) mà không bọc transaction | `ChangeBotController.php:232-264`; `BotController.php:4756-4820` | Trung bình (đã giảm so với v1) |
| TD-B10 | Mass assignment mở: `ScheduleChangeBot::$guarded = []` (`:10`) và `Bots::$guarded = []`. Chỗ gọi hiện tại dựng mảng thủ công nên chưa khai thác được | `app/ScheduleChangeBot.php:10`; `app/Bots.php` | Trung bình |
| TD-B11 | Bảng `schedule_change_bots` **không có index nào ngoài PK** — `where('bot_id')`, `whereIn('status')`, `where('channel_id_new')` full-scan. Càng đáng lo vì BR-01b thêm một câu `count()` nữa mỗi lần tạo | migration `2026_04_17_125226_...php` | Trung bình |
| TD-B12 | `init()` gọi **4 API LINE đồng bộ** mỗi lần load trang, không cache, không timeout tường minh | `ChangeBotController.php:66-69` | Trung bình |
| TD-B13 | Mọi helper LINE nuốt exception và trả giá trị mặc định ⇒ **lỗi mạng bị báo cho user thành "thông tin nhập sai"** | `app/Helpers/functions.php:4235-4278`, `5793-5895` | Trung bình |
| TD-B14 | `progress()` không phân biệt `ERROR` với `CANCEL` — cả hai trả `message: "ERROR"`; user tự huỷ đặt lịch vẫn có thể thấy thông báo lỗi | `ChangeBotController.php:288` | Thấp |
| TD-B15 | Accessor `getCreatedAtAttribute()` ép `created_at` thành chuỗi ⇒ mất kiểu Carbon; `Carbon::parse(null)` trả thời điểm hiện tại (sai âm thầm) | `app/ScheduleChangeBot.php:25-28` | Thấp |
| TD-B16 | `lineLoginAccessToken()` khởi tạo `$channelAccessTokenLineLogin` bên trong `try`; exception sớm → truy cập biến chưa định nghĩa | `app/Helpers/functions.php:5844-5868` | Thấp |
| TD-B17 | Comment cột `status` trong migration ghi thiếu `5: cancel` — schema không khớp code | migration `2026_04_17_125226_...php` | Thấp |
| TD-B18 | Cột `bots.campaign_change_bot` được migration tạo nhưng **không code nào dùng** — cột chết | migration `2026_04_20_165013_...php` | Thấp |
| TD-B19 | **Nợ kiến trúc**: tồn tại nhiều thế hệ code change-bot song song (xem `api-spec.md` mục 6) — `change_new_bot.blade.php`, `change_bots.blade.php`/`change_new_bots.blade.php`, `bot_add_v3` + `change-bot-sub`, và `change_bot_new/`. Nhánh này còn **mồ côi hoá** thêm EP-02 + nhánh đổi-LOA của `step2CheckFriend` mà không xoá code | `routes/web.php:208-223`, `:389,391`, `:3398-3400`; `BotController.php:4790-4820`, `:7275-7299` | Nghiêm trọng |
| TD-B20 | Nhánh đổi-LOA của `step2CheckFriend` **không có** guard `#39230` và **không dùng** `PlanLimitGuard` — nếu tương lai bật lại đường EP-02 thì hai lỗ hổng cũ quay lại | `BotController.php:4790-4820` | Trung bình |
| TD-B21 | Bảng `schedule_change_bots` **chưa có** trong dump `db/schema/tables/` của dự án reverse-spec → cần export lại DB trước khi chạy `/spec-db` | `db/index.md` | Thấp (quy trình) |

### (c) Comment / chuỗi hardcode **sót lại** — rác code, KHÔNG phải bằng chứng chưa hoàn thiện

> Tính năng đã chạy production. Các dấu vết dưới đây là tàn dư của giai đoạn prototype, cần dọn nhưng **không** làm sai hành vi hiện tại.

| # | Dấu vết | Vị trí | Ảnh hưởng thực tế |
|---|---------|--------|-------------------|
| TD-C01 | Comment `// Change Bot AJAX APIs (dummy)` ngay trên khối route | `routes/web.php:211` | **Không có** — các endpoint bên dưới đều là code thật, đang chạy. Chỉ gây hiểu nhầm khi đọc code (chính bản spec v1 đã bị lừa bởi dòng này) |
| TD-C02 | `/** TODO: replace with real DB deletion */` trên `deleteReservation()` | `ChangeBotController.php:293` | **Không có** — method vẫn UPDATE `status = CANCEL` thật. TODO chỉ nói về việc "xoá hẳn" thay vì soft-cancel |
| TD-C03 | `/** TODO: replace with real execution logic */` trên `executeReservation()` | `ChangeBotController.php:305` | **Không có** — việc "thực thi" là trách nhiệm của worker; method chỉ cần đẩy `status = WAITING` để worker nhận. TODO đã lỗi thời |
| TD-C04 | `init()` trả `campaign_countdown` hardcode `'06 日 15 時間 39 分'` | `ChangeBotController.php:89` | **Rất nhỏ** — FE ưu tiên `campaign_change_bot` để tự tính đồng hồ (`change_new.js:123`, `getRemainingSeconds()` `:436-447`); chuỗi này chỉ là fallback khi `campaign_change_bot` thiếu |
| TD-C05 | `execute()` nhánh `SCHEDULED` trả khối `reservation` hardcode: 「エルメ公式アカウント名」, `@lme_official`, 「コミュニケーションプラン」, `friend_count = 1240` | `ChangeBotController.php:271-275` | **Không có** — FE bỏ qua khối này, tự dựng `reservation` từ `confirmData` (`change_new.js:308-318`). Chỉ lộ chuỗi giả nếu ai đó gọi API trực tiếp |
| TD-C06 | `progress()` trả `'confirm_data' => null` hardcode | `ChangeBotController.php:290` | **Nhỏ** — modal hoàn tất không nhận dữ liệu LOA mới từ server; FE fallback `self.confirmData` sẵn có (`change_new.js:347`) |

---

## 12. Ghi chú cho job-analyzer

### Bảng hàng đợi
- **`schedule_change_bots`** — hàng đợi công việc đổi LOA. Worker đọc `status = WAITING(1)`, sắp xếp `id ASC`, batch 50 (`ChangeBotTask.java:83`).
- Cột consumer quan tâm: `status`, `progress`, `message_error`, `type`, `bot_id`, và 8 cột credential (`channel_id`, `channel_secret`, `channel_id_line_login`, `channel_secret_line_login`, `channel_id_new`, `channel_secret_new`, `channel_id_line_login_new`, `channel_secret_line_login_new`).
- Credential là **snapshot tại thời điểm tạo** (BR-16) — worker không nên đọc lại `bots` để lấy credential cũ.

### Trạng thái Laravel KHÔNG tự chuyển được (worker phải làm)

| Chuyển đổi | Bên chịu trách nhiệm |
|-----------|----------------------|
| `WAITING(1) → PROCESSING(2)` | **Worker** — không có code Laravel |
| `PROCESSING(2) → DONE(3)` | **Worker** |
| `PROCESSING(2) → ERROR(4)` (KHÔNG ghi `message_error`) | **Worker** |
| Ghi `progress` 0 → 100 | **Worker** — không có code Laravel nào ghi cột này |
| `DRAFT(0) → WAITING(1)` tự động khi tới hạn | **Chưa xác định.** Laravel chỉ có `executeReservation()` do user bấm tay; **không tìm thấy code Laravel nào tự đẩy `DRAFT` → `WAITING` theo thời gian**. Cần job-analyzer xác nhận worker có quét `DRAFT` (`type = 2`) hay không; nếu không thì "đặt lịch" thực chất là "lưu nháp chờ bấm tay" |

### Câu hỏi cần job-analyzer trả lời
1. Worker có xử lý `status = CANCEL(5)` không? Entity Java `ScheduleChangeBot.java:13-20` **không khai báo** `STATUS_CANCEL`, trong khi Laravel `deleteReservation()` set giá trị này (kể cả lên bản ghi đang `PROCESSING`) — xem TD-B05.
2. Worker có tự kích hoạt bản ghi `DRAFT(0)` với `type = SCHEDULED(2)` không (và theo mốc thời gian nào — bảng không có cột `scheduled_at`)?
3. Worker cập nhật những bảng nào của Laravel (dự đoán: `bots` 4 cột credential, `bot_line_user`, `line_users`, `conversations`, `chat_count`, `csv_management` — thấy `cleanupRepo.resetStatusChatCountByBotId()` và `cleanupRepo.resetCsvManagementByBotId()` tại `ChangeBotJob.java:270,305`)?
4. Worker có tự đặt lại webhook endpoint cho LOA mới không (Laravel đã làm qua EP-05, nhưng EP-05 chỉ chạy khi user gõ ở bước `input`)?
5. Cơ chế retry / backoff: `ChangeBotTask.java:72` có `sleep(ChangeBotConstants.ERROR_BACKOFF_MS)` — cần mô tả.

### Vị trí source worker
- `src/job/linect-service/src/main/java/sns/line/task/ChangeBotTask.java`
- `src/job/linect-service/src/main/java/sns/line/threads/changebot/ChangeBotJob.java`
- `src/job/linect-service/src/main/java/sns/line/models/linedb/entities/ScheduleChangeBot.java`
- `src/job/linect-service/src/main/java/sns/line/models/linedb/repository/ScheduleChangeBotRepository.java`
- Đăng ký task: `src/job/linect-service/src/main/java/sns/line/AppMain.java`
