# FA-017 — QR Code Action 「QRコードアクション」 — Logic Spec (Laravel)

> **Nguồn phân tích**: `src/web/sns-line/` — Laravel 5 / PHP 7.2
> **Controller chính**: `sns-line/app/Http/Controllers/Basic/QRCodeController.php` (3.966 dòng, 66 method)
> **Bảng chính**: `landing`
> **Trạng thái**: ui-spec.md chưa có → phân tích thuần từ routes + source code.

---

## 0. Tổng quan nghiệp vụ

「QRコードアクション」 (QR Code Action) cho phép Admin của một LINE Official Account tạo ra các **mã QR / link kết bạn có gắn hành động**. Khi LINE User quét mã hoặc mở link:

1. Trang LIFF `/landing-qr/{liffId}?uLand={code}` được mở → ghi nhận lượt quét vào `collect_open_landings`.
2. Trên mobile, trang tự chuyển hướng vào ứng dụng LINE để user kết bạn.
3. Sau khi kết bạn, hệ thống (Spring Boot job xử lý callback follow) ghi `detail_landing_click` và chạy **action** đã gắn với QR đó (gửi tin nhắn, gắn tag, chạy kịch bản…).
4. Số liệu được tổng hợp hằng ngày vào `landing_histories` bởi cron `statistic:landing_action`, và có thể đồng bộ lên Google Spreadsheet.

Tính năng có 5 nhóm cấu hình chính (tương ứng các tab ở màn hình edit v2):
- **基本設定** — tên, thư mục, trạng thái công khai
- **アクション設定** — action chạy khi quét, tin nhắn kèm theo, giới hạn tần suất
- **紹介設定** — trang & tin nhắn để bạn bè hiện tại giới thiệu bạn mới
- **QRコードOFF / 有効期限** — lịch bật/tắt QR theo thời gian
- **外部連携 / LP Poster** — nhúng HTML, callback, tham số `cid1..cid5`, và ma trận URL đo lường theo cặp (広告 × LP)

---

## 1. Controllers + Actions

### 1.1. `QRCodeController::__construct` — `QRCodeController.php:95-109`

Dependency injection qua constructor:

| Tham số | Interface / Class | Vai trò |
|---|---|---|
| `$messageV2Repository` | `App\Contracts\Repositories\MessageV2RepositoryInterface` | Tạo bản ghi bảng `messages_v2s` (model `App\MessagesV2`) |
| `$botLineUserRepository` | `App\Contracts\Repositories\BotLineUserRepositoryInterface` | Lấy tài khoản test (`getLineUserTest`) |
| `$messageService` | `App\Services\MessageService` | Gửi tin nhắn LINE (`createMessageV2`) |
| `$conversationRepository` | `App\Contracts\Repositories\ConversationRepositoryInterface` | Tra `conversation` theo bot + line id |
| `$templateService` | `App\Services\TemplateService` | Gửi tin nhắn từ template (`sendMessageAction`) |
| `$botRepository` | `App\Contracts\Repositories\BotRepositoryInterface` | Cập nhật `bots` (`updateBot`) |

Ngoài ra 3 service được inject **theo method** (method injection):
- `LandingCopyService` → `saveLandingV2` (`:196-199`)
- `PosterSettingService` → `storePosterConnectQrCode`, `getPosterConnectQrCode`, `getLandingPosterConnectQrCode`, `storeLandingPosterConnectQrCode`, `getLandingQrStep4Data` (`:3846-3930`)
- `PlanLimitGuard` (static) → `saveLandingV2`, `saveLanding`, `restoreQr`

---

### 1.2. `index()` — Màn hình danh sách — `QRCodeController.php:111-150`

**Các bước:**
1. `$bot_id = getBotId()` — lấy bot đang chọn từ session.
2. Tra `Bots` theo `id` + `is_deleted = 0`; rỗng ⇒ `redirect()->route('adminIndex')`.
3. `$liff_id` = `liff_app_id_booking` nếu có, ngược lại `liff_app_id`.
4. **Xác định cờ gói free mới** `$flagNewFreePlan`:
   - `= 1` nếu `users.created_at` của admin bot > `2021-07-01 00:00:01` **và** `bots.plan_type == 2`;
   - hoặc `bots.flag_contract_new == 1` **và** (`bot_contracts.contract_type == 'free'` hoặc `plan_type == 2`) — join `bot_contracts` ⨝ `bot_slots`.
5. **Đọc thư mục đang mở từ cookie** `folder_landing` (JSON `{bot_id: category_id}`). Kiểm tra category còn tồn tại với `kind = config('sns-line.category_kind.landing')` và `is_deleted = 0`; không hợp lệ ⇒ ghi lại cookie `folder_landing` với giá trị `0`, TTL **14.400 phút (10 ngày)**, path `/basic/landing`, domain = host hiện tại.
6. Đếm `qrCodeNumber` = số `landing` của bot còn sống (`deleted_at IS NULL`).
7. Render `basic.qr_code.v2.index`. Ba biến `$scenario`, `$conversion`, `$richMenus` được truyền nhưng **luôn là mảng rỗng** (`:145-147`) — dữ liệu thực nạp bằng AJAX.

**Side effect**: ghi cookie `folder_landing`.

---

### 1.3. `saveLandingV2(Request, LandingCopyService)` — Tạo / sao chép QR — `QRCodeController.php:196-420`

Đây là method quan trọng nhất của luồng tạo mới. Bao toàn bộ thân hàm trong `try/catch`.

**Các bước:**

| # | Bước | Chi tiết | Dòng |
|---|---|---|---|
| 1 | Lấy bot | `Bots::where('id', getBotId())->first()`; rỗng ⇒ 500 `Bot does not exist` | `:203-211` |
| 2 | **Kiểm giới hạn gói (trước insert)** | `checkPlanFreeBotLimitFeature($botDetail)` → `$flagNewFreePlan`. Nếu `= 1` và đã có ≥ 3 QR ⇒ 500 kèm 「現在のプランは利用できない機能です。アップグレードが必要になります。」 | `:213-226` |
| 3a | **Nhánh COPY** (`mode == 'copy'`) | `Landing::select(<58 cột whitelist>)->where('id', $request->input('id'))->first()` — **không lọc `bot_id`**. Clone 3 action (`action_id`, `user_introduction_action_id`, `action_limit_id`) qua `cloneAction()`; clone 2 template (`template_general_id`, `template_intro_id`) thành bản ghi `template` mới | `:234-277` |
| 3b | **Nhánh TẠO MỚI** | Tạo `template` mặc định cho tin nhắn giới thiệu với nội dung 「友だちご紹介ありがとうございます✨ ご紹介特典のクーポンをお受け取りください！」 | `:278-282` |
| 4 | Sinh mã QR duy nhất | `str_random(6)` → `checkRandomCodeLanding($code, $botId)` (đệ quy tới khi không trùng **trong phạm vi bot**) | `:284-286` |
| 5 | Dựng `link_qr_code` | `route('QRLanding', $liffId) . '?uLand=' . $code` | `:286` |
| 6 | Dựng `$settings` mặc định | Xem bảng "Giá trị mặc định khi tạo QR" bên dưới | `:294-317` |
| 7 | **Merge + insert** | `$settings = array_merge($settings, $newQrs); DB::table('landing')->insertGetId($settings)` — ⚠ mass assignment | `:318-320` |
| 8 | **Kiểm giới hạn gói (sau insert)** | `PlanLimitGuard::rollbackIfOverLimit(...)` — đếm lại, nếu bản ghi vừa tạo nằm ngoài hạn mức ⇒ `DB::table('landing')->where('id',...)->where('bot_id',...)->delete()` + trả 500 | `:321-338` |
| 9 | Cập nhật tutorial | `BotsTutorial::where('bot_id',...)->where('status_qr_code', 0)->update(['status_qr_code' => 1])` + `checkUpdateHasTutorial($botId)` | `:339-340` |
| 10 | Copy dữ liệu phụ (chỉ khi copy) | `$landingCopyService->copyLandingParameter()`, `copyLandingPoster()` — bọc try/catch riêng, lỗi chỉ log | `:341-348` |
| 11 | Đồng bộ thông báo | `syncNotifyNewItemForBot($botId, $idlanding, 'is_all_qrcode_new', 'when_adding_friends')` — thêm id QR vào cột `notify_setting.when_adding_friends` cho mọi user có cờ `is_all_qrcode_new` | `:350-351` |
| 12 | **Sinh ảnh QR code** | URL mã hoá = `https://line.me/R/app/{liff_app_id}?uLand={code}`. Dùng `BaconQrCode\Renderer\Image\Png` 300×300, ghi vào `public/{FOLDER_MEDIA}images/{user_id}/{bot_id}/landing/{timestamp}{rand6}_{landing_id}.png`, tạo thư mục mode `0777` nếu chưa có. Cập nhật `landing.path_landing` | `:353-377` |
| 13 | **Tạo Google Spreadsheet** (nếu có liên kết) | Nếu `landing_connect_google` của bot có `google_access_token`: lấy client, refresh token khi hết hạn, `createSheet($client, $settings['name'])`, lưu `landing.google_sheet_id`. Nếu `spreadsheetId` rỗng ⇒ log error + `notifyChatworkException`. Bọc try/catch riêng | `:379-417` |
| 14 | Trả về | `{"status": true, "id": <landing_id>}` | `:418-420` |

**Giá trị mặc định khi tạo QR** (`:294-317`):

| Cột | Giá trị |
|---|---|
| `bot_id` | `getBotId()` |
| `code` | random 6 ký tự, duy nhất trong bot |
| `link_qr_code` | `{app_url}/landing-qr/{liff_app_id}?uLand={code}` |
| `postback_type` | `0` |
| `type_open_url` | `0` |
| `postback_content` | `null` |
| `use_msg_new_friend` | `1` nếu `newQrs.action_with_friend == 1`, ngược lại `0` |
| `use_msg_old_friend`, `use_msg_unblock` | `0` |
| `action_type` | `2` (chạy nhiều lần) |
| `is_on_callback`, `is_on_html`, `is_on_param` | `0` |
| `text_over_time` | 「有効期間外です。」 |
| `created_at` | `Carbon::now()` |
| `intro_page_title` | 「友だち紹介キャンペーン」 |
| `intro_page_content` | HTML demo dài (「【これはデモテキストです】」…) |
| `intro_message` | 「【LINE友だち追加で特典GET】\n登録するだけで初回限定クーポンをプレゼント！」 |

---

### 1.4. `cloneAction(int $actionId): int` — `QRCodeController.php:422-445`

**Private helper.** Nhân bản một action đầy đủ:
1. `Actions::find($actionId)->toArray()`, bỏ `id`, đặt lại `created_at`/`updated_at` ⇒ `Actions::insertGetId()`.
2. Lấy toàn bộ `ActionDetail` của action gốc; với mỗi bản ghi: bỏ `id`, gán `action_id` mới, `bot_id = getBotId()`, đặt lại timestamps ⇒ `ActionDetail::insertGetId()`.
3. Nếu detail có `has_filters == 1` ⇒ `FilterV2::cloneFilters($old_detail_id, $new_detail_id, 'modal_action')`.

⚠ Không kiểm `bot_id` của action gốc.

---

### 1.5. `saveLanding(Request)` — Tạo QR bản v1 — `QRCodeController.php:447-566`

Tương tự `saveLandingV2` nhưng:
- Nhận từng field rời (không có `newQrs`) — xem danh sách ở api-spec EP-58.
- Mã `code` **do client gửi lên** (`$request->codeLanding`) — không sinh lại phía server ⇒ có thể trùng nếu client giả mạo.
- Khi `connect_aff == 1` ⇒ reset `connect_aff = 0` cho **toàn bộ** QR của bot trước khi insert (`:506-513`).
- Không tạo Google Sheet, không copy poster/parameter.
- Đã được bổ sung `PlanLimitGuard` (issue #39230 — comment tại `:458-461` giải thích route v1 vẫn sống nên phải chặn).
- `addLogUserAction("saveLanding")` hoặc `"saveCopyLanding"` tuỳ `$request->actionLanding`.

---

### 1.6. `saveEditLanding(Request, $id)` — `QRCodeController.php:637-685`

- **Validation duy nhất có ở tính năng này**: `$this->validate($request, ['name' => 'required|max:255'], ['name.required' => 'QRコードアクション名は必須です。'])`.
- Khi `connect_aff == 1` ⇒ reset `connect_aff = 0` cho mọi QR khác của bot.
- `Landing::where('id', $id)->update([...])` — ⚠ **không lọc `bot_id`**.
- `time_interval_action` chỉ được lưu khi `interval_action == 2`, ngược lại `null`.
- Thành công ⇒ `redirect()->route('landingIndex')`; exception ⇒ `redirect()->route('404')`.

---

### 1.7. `ajaxGetListQrs(Request)` — `QRCodeController.php:891-973`

**Query builder tuần tự:**
1. Base: `Landing::where('bot_id', $botId)->with('action.details')`.
2. `type == 'sort_item'` ⇒ `select(['id','name'])`.
3. `category_id` có **và** `keyword` không có ⇒ lọc theo category (giá trị `0` khớp cả `0` và `NULL`).
4. `keyword` có ⇒ `name LIKE %keyword%` (bỏ qua lọc category).
5. `action_with_friend` có ⇒ `whereIn`; giá trị `0` mở rộng thành `[1, 2]`.
6. `orders` ⇒ `orderBy` với **whitelist 8 cột**.
7. Luôn kết thúc bằng `orderBy('id', 'DESC')`.
8. `unlimit` ⇒ `get()`, ngược lại `paginate($limit ?? 15)`.

**Hậu xử lý mỗi item** (`:943-959`, bỏ qua khi `type == 'sort_item'`):
- `new_link_qr_code = env('URL_OUTSIDE_STEP') . 'landing-qr/' . $liffAppId . '?uLand=' . $code`
- `path_landing = $item->path_landing_with_domain` (accessor)

**Dữ liệu phụ trả kèm**: `landingConnectAsp` (QR duy nhất có `connect_aff = 1`, fallback `{id:0, name:'設定しない'}`), `qrCodeNumber`, `contractType` (join `bot_contracts` ⨝ `bot_slots`).

---

### 1.8. `ajaxUpdateBasicQrs(Request, Landing $qr)` — `QRCodeController.php:1013-1052`

1. Whitelist 6 trường: `status`, `name`, `category_id`, `action_id`, `user_introduction_action_id`, `action_limit_id`.
2. **Kiểm quyền**: `$qr->bot_id != getBotId()` ⇒ `HttpException(404, 'Qr not found!')`.
3. Ghi audit log qua `Log::info('updated basic landing qr', [...])` (old/new JSON).
4. **Logic đặc biệt** — chỉ khi payload chứa **duy nhất** `status`:

   | `status` | Điều kiện | `time_qr_off_status` |
   |---|---|---|
   | `0` | `use_limit_time` && `limit_start_time` && `limit_start_time > now` | `1` |
   | `0` | `use_limit_time` && `limit_start_time` && `limit_start_time <= now` | `0` |
   | `0` | không dùng giới hạn | `0` |
   | `1` | `use_limit_time` && `limit_start_time > now` | `1` |
   | `1` | `use_limit_time` && `limit_end_time > now` | `3` |
   | `1` | `use_limit_time` && `limit_end_time <= now` | `0` |
   | `1` | không dùng giới hạn | `0` |
5. `$qr->update($attributes)`.

---

### 1.9. `restoreQr(int $id)` — `QRCodeController.php:1334-1384`

1. Kiểm giới hạn gói **trước** khi restore (giống bước 2 của `saveLandingV2`).
2. `Landing::where('id',$id)->where('bot_id',$botId)->withTrashed()->first()`; rỗng ⇒ 404.
3. **Nếu thư mục cha đang bị xoá mềm (`category.is_deleted = 1`) ⇒ khôi phục luôn thư mục.**
4. `$landing->restore()` + `DetailLandingClick::where('landing_id',$id)->where('bot_id',$botId)->restore()`.
5. `PlanLimitGuard::rollbackIfOverTotal(...)` — đếm lại; vượt ⇒ xoá mềm lại cả landing và detail, trả 500.

---

### 1.10. `settingDetail`, `settingIntroduce`, `settingLimit` — `QRCodeController.php:1405-1507`

Ba method chung một khuôn:
1. `$request->only([...])` để whitelist trường.
2. `Log::info(...)` ghi old/new.
3. Xử lý riêng nội dung tin nhắn qua bảng `template` (chỉ `settingDetail` và `settingIntroduce`).
4. `$qr->update($attributes)`.

**Quy tắc xử lý template** (giống nhau ở cả hai):

| Điều kiện | Hành động |
|---|---|
| Nội dung `== ''` | `Template::where('id', $qr->template_xxx_id)->delete()` + set `$qr->template_xxx_id = null` (gán trên object, **không đưa vào `$attributes`** ⇒ dựa vào `$qr->update()` để persist thay đổi dirty) |
| Có nội dung + đã có template | `update(['content' => ..., 'update_timestamp' => time()])`, có lọc `bot_id` |
| Có nội dung + chưa có template | `Template::create(['bot_id', 'category_id' => -111222, 'position' => 0, 'type' => 'text', 'content'])` và gán id vào `$attributes['template_xxx_id']` |

`category_id = -111222` là **magic number đánh dấu template ẩn** (không hiển thị ở màn quản lý template).

`settingLimit` không đụng template; chỉ whitelist 7 trường và update. ⚠ **Không** cập nhật `time_qr_off_status` (khác `saveSettingQrOff`) ⇒ thay đổi lịch qua tab này sẽ không được cron `landing:qr-off:schedule` nhận (Mức độ tin cậy: Trung bình — suy luận từ so sánh 2 method).

---

### 1.11. `saveSettingQrOff($id, Request)` — `QRCodeController.php:3617-3675`

1. `addLogUserAction("saveSettingQrOff")`.
2. Tìm landing theo `id` + `bot_id`; rỗng ⇒ 404.
3. Dựng `$dataUpdate` với 7 trường: `type_display_off`, `data_display_off`, `use_limit_time`, `use_action_limit`, `use_limit_end_time`, `limit_start_time`, `limit_end_time`.
4. **Nếu bất kỳ trường thời gian nào thay đổi** (`limit_start_time`, `limit_end_time`, `use_limit_end_time`, `use_limit_time`) ⇒ `time_qr_off_status = 1` — đưa bản ghi vào hàng đợi của cron.
5. Ánh xạ `type_display_off`:

   | `type_display_off` | `is_use_url_over_time` | `text_over_time` | `url_over_time` |
   |---|---|---|---|
   | `1` (hiển thị text) | `0` | `data_display_off` | `null` |
   | `2` (redirect URL) | `1` | `null` | `data_display_off` |
   | `0` (chạy action) | không đổi | không đổi | không đổi |
6. Ghi log `'User updated'` với old/new.

---

### 1.12. `ajaxInitDataDetailV2(Request)` — Thống kê chi tiết — `QRCodeController.php:1849-2288`

Method dài nhất (440 dòng), phục vụ 3 tab của màn thống kê + xuất CSV.

#### Tab 1 — 「日別」(theo ngày) — `:1878-1993`
- Sinh dải ngày bằng `CarbonPeriod` từ `start_date` → `end_date`; tự phân trang thủ công (`array_slice`), trừ khi `type = download-csv` thì lấy toàn bộ.
- Sắp xếp: chỉ hỗ trợ `order = date` + `dir = DESC` ⇒ `array_reverse`.
- **Nguồn dữ liệu chính**: bảng tổng hợp `landing_histories` (do cron `statistic:landing_action` sinh) — **loại trừ ngày hôm nay** (`where('date', '!=', $now)`).
- **Ngày hôm nay** được tính realtime bằng `handleAttributeCurrentDay($landingId)` rồi cộng dồn vào tổng.
- Các chỉ số: `count_click`, `count_scan_friend_new`, `count_action`, `count_add_friend`, `count_add_friend_new`, và 3 biến thể `_distinct`.
- `type_count == 1` ⇒ dùng các cột `*_distinct`.

#### Tab 2 — 「友だち別」(theo bạn bè) — `:1994-2140`
- Query gốc trên `detail_landing_click`, lọc `landing_id` + `bot_id`, `is_old_friend != 2`.
- Mặc định loại các dòng `is_old_friend = 0 AND action = 1` (trừ khi `is_detail_day = 1`).
- Lọc theo `landing_url_ids` ⇒ join `landing_page_poster_url` theo `post_code`.
- Lọc `keyword` ⇒ join `line_user`, tìm trên `name` / `view_name`.
- **`total_block`** (số người đã block): join `conversation` (`is_blocked = 1`), chỉ tính người mà **lần kết bạn đầu tiên là qua QR này**. Dùng subquery pre-aggregate `first_other_add` (MIN `time_click` của `action = 2` ở landing khác) thay cho `whereNotExists` tương quan — comment code ghi rõ mục đích tránh O(n²) (`:2020-2027`).
- **Bộ chỉ số** tính bằng 11 biểu thức `COUNT(CASE WHEN ...)`:

  | Chỉ số | Điều kiện |
  |---|---|
  | `total_click` | mọi dòng |
  | `total_friend` | `action = 2` |
  | `total_new_friend` | `action = 2 AND is_old_friend = 0` |
  | `total_old_friend` | `(action = 1 AND is_old_friend = 1) OR (action = 2 AND is_old_friend = 3)` |
  | `total_unblock_friend` | `action = 2 AND is_old_friend = 1` |
  | `total_action` | `is_action_web IN (1, 2)` |
  | *(+ 5 biến thể `_distinct` theo `line_id`)* | |

  > ⚠ **Tên alias SQL ≠ tên key trong JSON response** (bổ sung theo V-23). Ánh xạ thật (`QRCodeController.php:2072-2082`, `:2283-2285`): alias `total_new_friend` → biến `$totalNewFriendTab2` → key **`total_new_friend_tab2`**; alias `total_unblock_friend` → `$totalUnblock` → key **`total_unblock`**; alias `total_old_friend` → key **`total_old_friend`** (giữ nguyên). Khi viết test hoặc client, dùng **tên key**, không dùng tên alias.
- `type_count == 1` ⇒ join subquery `latest_clicks` (MAX `time_click` theo `line_id`) để mỗi người chỉ còn 1 dòng.
- Cờ `is_blocked` của từng dòng được gán bằng cách đối chiếu với `DetailLandingClick::firstAddFriends()`.

#### Tab 3 — 「LP・広告別」— `:2141-2260`
- Query gốc trên `collect_open_landings`, yêu cầu `post_code IS NOT NULL` và `is_scan IN (1,2)`.
- LEFT JOIN `detail_landing_click` (`collect_id`), LEFT JOIN `landing_page_poster_url` (`code = post_code`), yêu cầu `landing_page_poster_url.id IS NOT NULL`.
- `GROUP BY date_scan, post_code`.
- Chỉ số: `count_scan`, `count_scan_distinct` (theo `device`), `count_action`, `count_action_distinct`, `count_friend`, `count_friend_distinct`.
- Tổng được tính bằng cách bọc query thành subquery rồi `SUM(...)` (`:2179-2189`).
- Mỗi dòng được gán thêm `poster_name` và `landing_name` từ quan hệ `poster.connectQrCode` / `poster.landingPage`.

#### Xuất CSV — `:2262-2275`
- `type == 'download-csv'` ⇒ chọn exporter theo tab: `DetailLandingClickExport` / `LandingListFriendExport` / `LandingPageUrlExport`.
- Chuyển encoding sang **SJIS** bằng `mb_convert_encoding` (phát hiện encoding nguồn tự động).
- Trả `Content-Type: text/csv; charset=Shift_JIS`, `Content-Disposition: attachment; filename="export.csv"`.

---

### 1.13. `handleAttributeCurrentDay(int $landingId): array` — `QRCodeController.php:2490-2531`

**Private.** Tính số liệu realtime của **ngày hôm nay** (vì cron chỉ tổng hợp tới hôm qua):
- Từ `detail_landing_click` (`whereDate('time_click', today)`): `count_scan`, `count_scan_friend_new`, `count_action`, `count_add_friend`, `count_add_friend_new`, `count_scan_distinct`, `count_action_distinct`, `count_add_friend_distinct`.
- Từ `collect_open_landings` (`date_scan = Ymd(today)`, và `(is_scan=1 AND type=PC) OR type=MOBILE`): `count_click`, `count_click_distinct`.

---

### 1.14. `countScan(Request, $id)` — Ghi nhận lượt quét (PUBLIC) — `QRCodeController.php:2300-2330`

1. `Landing::where('id', $id)->first()`; rỗng ⇒ `HttpException('Landing not found')` (⚠ truyền string vào tham số `$statusCode`).
2. `$type = $request->input('type') ?: 1`.
3. `$isScan = 1` khi `type == CollectOpenLanding::TYPE['MOBILE'] (2)` **hoặc** `request->device == 'pc'`; khi đó tăng `landing.total_user_click += 1`.
4. `CollectOpenLanding::create([bot_id (lấy từ landing, KHÔNG từ request), landing_id, ip (request->ip()), type, is_scan, date_scan (Ymd), device (= device_id), post_code])`.

⚠ Biến `$botId = $request->bot_id` được gán nhưng **không sử dụng** (`:2302`).

---

### 1.15. `qrLanding(Request, $liffId)` — Trang QR công khai — `QRCodeController.php:1643-1696`

1. Đọc `uLand`, `device`, `postcode`.
2. `Landing::where('code', $uLand)->first()` — ⚠ **tham số `$liffId` trên URL không được dùng để tra cứu**, chỉ dùng cho LINE nhận diện LIFF app. Landing rỗng ⇒ `redirect()->route('404')`.
3. `Bots::find($landing->bot_id)`; rỗng ⇒ `notifyChatworkChat11(...)` + `redirect()->route('404')`.
4. **Kiểm hạn hợp đồng**: nếu `plan_type == 1` và (`expired_date + 7 ngày < now` hoặc `bot_contracts.status == 3`) ⇒ `redirect()->route('410')`.
5. **Kiểm trạng thái QR** (`status == 0`):
   - `type_display_off == 2` ⇒ `redirect()->away($landing->data_display_off)`
   - `type_display_off == 1` ⇒ trả chuỗi HTML thô (mặc định 「現在、友だち追加は受け付けていません。」)
   - `type_display_off == 0` ⇒ **rơi xuống** render view bình thường (nhánh chạy action)
6. Render `basic.qr_code.qr_landing`.

**Phía client** (`resources/views/basic/qr_code/qr_landing.blade.php:66-115`):
- Sinh/đọc `device_id` từ cookie `device_scan_landing` (random 6 ký tự + timestamp, TTL 365 ngày).
- Phát hiện mobile bằng regex user-agent.
- Gọi EP-64 `POST /ajax/v2/landing/{id}/count-scan-qr-code`.
- Nếu là mobile ⇒ redirect `https://line.me/R/app/{liffId}&deviceId={deviceId}` (`params = url.split("/")[4]`).

---

### 1.16. `checkFriend(Request)` — Luồng kết bạn (PUBLIC) — `QRCodeController.php:2810-3389`

Method dài thứ hai (580 dòng). Dùng chung cho nhiều tính năng (`booking_calendar`, `product-*`, `booking_event`, `form_answer`, `calendar`, `calendar-salon`), không riêng QR.

**Giai đoạn 1 — Xác định trạng thái bạn bè** (`:2833-2840`):
```
Cần xử lý khi: line_user rỗng | conversation.is_blocked = 1 | bot_line_user rỗng | conversation rỗng
```

**Giai đoạn 2 — Tạo/khôi phục quan hệ** (`:2841-3013`), chỉ chạy khi `getInfoFromLine($bot, $lineId)` trả về profile:

| Bước | Xử lý | Chống race (issue #37711) |
|---|---|---|
| Tạo `line_user` | `insertGetId([line_id, name, status_message, avatar_url])` | Sau khi insert, tìm bản ghi cùng `line_id` có `id` nhỏ hơn; nếu có ⇒ **xoá bản vừa tạo**, dùng bản cũ |
| Tạo `bot_line_user` | Sinh `u_code` random 10 ký tự (vòng `do-while` kiểm trùng toàn hệ thống); `followed_at = now`, `is_blocked = 0` | Tương tự — xoá bản vừa tạo nếu trùng, set `$isDuplicateFriend = true` |
| Khôi phục `bot_line_user` bị block | Khi `is_blocked = 1` và `conversation.blocked_by = 0` ⇒ set `is_blocked = 0`, `followed_at = now` | — |
| Tạo `conversation` | `conversation_kind = 0`, `is_old_friend = 1`, `last_time_message = now` | Tương tự — xoá bản vừa tạo, set `$isDuplicateFriend = true` |
| Sau khi tạo conversation mới | Tạo bản ghi `messages_v2s` kind `KIND_MESSAGE_ADD_OLD_FRIEND`; `MobileNotifyService@insertNotifyOldFriend`; tăng `bot_friend_statistic.count_user_followed` (hoặc insert mới cho ngày hôm nay) | Chỉ chạy khi **không** trùng |
| Unblock conversation | Khi `is_blocked = 1` và `blocked_by = 0` ⇒ set `is_blocked = 0`, tạo bản ghi `messages_v2s`, tăng thống kê | — |

**Giai đoạn 3 — Chạy action kết bạn** (`:2996-3013`), chỉ khi `!$isDuplicateFriend && $isOldFriend`:
1. `LineUserAddFriendHistory::addHistory(['bot_id', 'line_user_id', 'landing_qr_id' => null, 'landing_qr_name' => null])`.
2. Nếu `add_friend_setting.template_add_old_id` có nội dung ⇒ `$this->templateService->sendMessageAction($bot, $lineUser, $conversationId, $message, ['table_name' => 'line_user_add_friend_history', 'history_id' => ...])`.
3. Nếu `add_friend_setting.action_old_id` ⇒ **`sendAction($actionOldId, $lineUserId, $botId, null, 1002, true, [], null, null, null, null, $historyId)`**.

**Giai đoạn 4 — Xử lý affiliate** (`:3014-3128`), khi không lấy được profile LINE và có `aff_id`:
- Kiểm `bot_setting_aff` (type 1) tồn tại, `bots.is_aff_view != 1`, `affiliaters.status_commission != 0`.
- Kiểm điều kiện kết thúc chương trình (`end_condition`): `1` = theo ngày giờ, `2` = theo số lượt được duyệt, `3` = theo tổng phí đã duyệt.
- Tính `aff_fee` từ `bot_duration_level_aff.duration` (JSON, chọn mức có `is_default = 1` hoặc mức có `date_start`/`time_start` đã đến).
- Tạo `aff_result` với `line_user_id = -1`, `is_deleted = -1`, `influx_kind = 0`, `influx_number = 1`, `type_link = 1`.

**Giai đoạn 5 — Dựng URL đích** (`:3129-3384`): switch theo `type`, sinh URL khác nhau cho trường hợp **đã là bạn** (dùng `Hashids::encode` + `u_code`) và **chưa là bạn** (dùng `https://line.me/R/app/{liff_app_id_booking|liff_app_id}?<param>=<id>`).

Nếu `botLineUser.is_blocked == 1` ⇒ trả `{status:false, url: bot.url_add_friend, is_friend:false}` (`:3131-3137`).

---

### 1.17. `pageIntro(Request)` — Trang giới thiệu (PUBLIC) — `QRCodeController.php:3391-3424`

1. `$codeLanding = $request->id` (**là `landing.code`**, không phải id số), `$uCode = $request->u_code`.
2. `BotLineUser::where('u_code', $uCode)->first()` — định danh người giới thiệu.
3. `Landing::where('code', $codeLanding)->where('bot_id', $botUser->bot_id)->first()`.
4. Dựng URL chia sẻ theo thứ tự ưu tiên: `bots.domain_url_shorten` → `env('URL_OUTSIDE_STEP')` → `landing.link_qr_code`.
5. `$messageEncoding = rawurlencode($intro_message) . "%0A" . urlencode($newUrl . '&u_code_intro=' . $uCode)` — chuỗi để nhúng vào link chia sẻ LINE.
6. Render `basic.qr_code.page_intro`.

---

### 1.18. Nhóm LP Poster — `QRCodeController.php:3818-3943`

| Method | Bước UI | Nghiệp vụ |
|---|---|---|
| `editLandingPoster` | Render | Chặn gói free (`isFreePlanBot()`), kiểm `bot_id`, render `basic.qr_code.v2.lp_poster` |
| `storePosterConnectQrCode` / `getPosterConnectQrCode` | Bước 1 | Quản lý danh sách 「広告名」 (`poster_connect_qrcode`) |
| `storeLandingPosterConnectQrCode` / `getLandingPosterConnectQrCode` | Bước 2 | Quản lý danh sách LP + URL (`landing_page_connect_qrcode`) |
| `getHashId` | Bước 3 | Trả `liff_app_id`, `URL_OUTSIDE_STEP`, `landing.code` để client tự dựng và render QR |
| `getLandingQrStep4Data` | Bước 4 | Trả ma trận URL đo lường đã gắn `uland` + `postcode` |

`isFreePlanBot()` (`:3945-3952`): `bots.plan_type == 2`; bot không tồn tại ⇒ `HttpException(404, 'Bot not found')`.

---

## 2. Models Eloquent

### 2.1. `App\Landing` — `sns-line/app/Landing.php`

| Thuộc tính | Giá trị |
|---|---|
| Table | `landing` |
| Primary key | `id` |
| `$guarded` | `[]` — **mọi cột đều mass-assignable** |
| `$timestamps` | `true` |
| Trait | `SoftDeletes` (cột `deleted_at`) |

**Hằng số:**
```php
QR_OFF_TYPE_DISPLAY_ACTION = 0;   // QR OFF → vẫn chạy action
QR_OFF_TYPE_DISPLAY_TEXT   = 1;   // QR OFF → hiển thị text
QR_OFF_TYPE_DISPLAY_URL    = 2;   // QR OFF → redirect URL
QR_OFF_USE_ACTION_LIMIT     = 1;
QR_OFF_NOT_USE_ACTION_LIMIT = 0;
ACTION_WITH_FRIEND = ['NEW_FRIEND' => 1, 'ALL_FRIEND' => 2];
```

**Relationships:**

| Tên | Loại | Đích | Khoá |
|---|---|---|---|
| `tags()` | hasOne | `App\Tags` | `id` ← `tag_id` |
| `scenario()` | hasOne | `App\Scenario` | `id` ← `scenario_id` |
| `template()` | hasOne | `App\Template` | `id` ← `template_id` |
| `action()` | belongsTo | `App\Actions` | `action_id` → `id` |
| `details()` | hasMany | `App\DetailLandingClick` | `landing_id` |
| `actions()` | hasMany | `App\ActionDetail` | `action_id` ← `action_id` (⚠ tên gây nhầm với `action()`) |
| `operator()` | belongsTo | `App\User` | `operator_id` → `id` |

**Accessor:**
- `getPathLandingWithDomainAttribute(): string` — nếu `path_landing` chứa chuỗi `qr_landing` **và** `APP_ENV === 'production'` ⇒ `env('URL_SERVER_MEDIA') . '/ext-media' . $path`; ngược lại `env('URL_SERVER_MEDIA') . $path`.

**Static:**
- `getNameById($id, $bot_id)` — trả `name`.
- `removeItemLanding(?int $landingId, ?int $botId)` — dọn sạch dữ liệu liên quan: `detail_landing_click->forceDelete()`, `collect_open_landings->delete()`, `landing_histories->delete()`. Cả 2 tham số rỗng ⇒ return sớm (chống xoá toàn bộ).

**Các cột chính của bảng `landing`** (nguồn `db/schema/tables/landing.sql`):

| Nhóm | Cột |
|---|---|
| Định danh | `id`, `bot_id`, `name`, `code`, `link_qr_code`, `path_landing`, `position`, `category_id` |
| Action | `action_type` (1 = 1 lần, 2 = nhiều lần), `action_id`, `action_with_friend` (1 = bạn mới, 2 = tất cả), `action_with_qrcode_normal`, `interval_action` (0/1/2), `time_interval_action` |
| Tin nhắn | `template_general_id`, `template_intro_id`, `template_recipient_intro_id`, `general_message`, `use_msg_new_friend`, `use_msg_old_friend`, `use_msg_unblock` |
| Giới thiệu | `user_introduction_action_id`, `user_recipient_intro_action_id`, `intro_page_title`, `intro_page_content`, `intro_message`, `use_user_intro_action_message`, `use_user_recipient_intro_message` |
| Trạng thái / lịch | `status` (0 = 非公開, 1 = 公開), `type_display_off`, `data_display_off`, `use_limit_time`, `limit_start_time`, `limit_end_time`, `use_limit_end_time`, `use_qr_page_over_time`, `use_action_limit`, `action_limit_id`, `is_use_url_over_time`, `text_over_time`, `url_over_time`, `time_qr_off_status` |
| Thiết kế QR | `setting_logo` (1/2/3), `path_logo`, `type_design_qr` (1..4), `color_qr`, `text_design_qr` |
| Liên kết ngoài | `is_on_param`, `is_on_html`, `is_on_callback`, `head_content`, `body_content`, `url_connect_qrcode_outside`, `url_callback`, `bill_type`, `postback_type`, `type_open_url`, `postback_content` |
| Affiliate | `connect_aff` |
| Google Sheet | `google_sheet_id` |
| Thống kê (denormalized) | `total_user_click`, `total_user_friend`, `count_action_web`, `count_action`, `count_scan_mobile`, `count_scan_pc`, `count_scan_distinct`, `count_unblock` |
| Audit | `created_at`, `updated_at`, `deleted_at`, `operator_id` |

### 2.2. `App\DetailLandingClick` — `sns-line/app/DetailLandingClick.php`
- Table `detail_landing_click`, `$guarded = []`, `SoftDeletes`, timestamps.
- `lineUser()` — hasOne `App\LineUser` (`line_id` ← `line_id`).
- `poster()` — belongsTo `App\LandingPagePosterUrl` (`post_code` → `code`).
- **Static scope `firstAddFriends(int $botId, int $landingId, array $lineIds, array $params = []): Builder`** — trả `line_id` + `MIN(time_click) as first_add_time` cho các bản ghi `action = 2`, group theo `line_id`, hỗ trợ lọc `keyword` (join `line_user`) và khoảng ngày (bỏ qua khi `get_all`). Dùng để xác định "lần kết bạn đầu tiên" phục vụ đếm block chính xác.
- **Cột nghiệp vụ quan trọng** (suy từ code — Mức độ tin cậy: Cao):

  | Cột | Ý nghĩa |
  |---|---|
  | `action` | `1` = chỉ mở/click (giá trị lúc INSERT bởi `LiffController.php:1226`), `2` = đã kết bạn (UPDATE bởi `LiffController.php:1325`, `:1411` hoặc Spring Boot `HandlePostbackTask`) |
  | `is_old_friend` | `0` = chưa từng có quan hệ với bot · `1` = đã có `bot_line_user`/`conversation` và **không** block · `2` = đang block (**trạng thái trung gian**, bị ghi đè thành `1`/`3` khi unblock — `LiffController.php:1667`; bị loại khỏi mọi thống kê bởi `is_old_friend != 2`) · `3` = là bạn trên LINE nhưng **chưa hiện trên エルメ**. ⚠ Nhãn hiển thị phụ thuộc **cặp** `(action, is_old_friend)` — xem mục 「**BR-29 — chi tiết**」. Comment schema `'0:no, 1:yes'` **đã lỗi thời** (mục 11, L-3) |
  | `is_action_web` | `0` = chưa chạy action · `1`/`2` = đã chạy action (mọi query dùng `IN (1,2)`); giá trị `2` do Spring Boot ghi. Comment schema `'0: no, 1: yes'` **đã lỗi thời** (mục 11, L-4) |
  | `qr_scan_from_device` | `1` = PC, `0` = mobile (dùng bởi cron thống kê). Ghi **duy nhất bởi Laravel** lúc INSERT — `LiffController.php:1234` (`$device ? 1 : 0`); Spring Boot **không** đụng tới cột này (`grep` trong `src/job/` = 0 kết quả) |
  | `collect_id` | FK tới `collect_open_landings.id` |
  | `device_id`, `post_code`, `time_click`, `time_action`, `is_landing_off`, `user_intro_id`, `popup_id`, `param_qrcode_connect_outside`, `email`, `bot_line_user_id` | |

### 2.3. `App\CollectOpenLanding` — `sns-line/app/CollectOpenLanding.php`
- `$guarded = []`; **table mặc định `collect_open_landings`**.
- `TYPE = ['PC' => 1, 'MOBILE' => 2]`.
- `detailLandingClick()` — hasOne `DetailLandingClick` (`collect_id` ← `id`).
- `detailLandingClick2()` — hasOne `DetailLandingClick` (`id` ← `detail_id`) — dùng khi query đã gom nhóm và select `max(detail_landing_click.id) as detail_id`.
- `poster()` — hasOne `LandingPagePosterUrl` (`code` ← `post_code`).
- Cột: `bot_id`, `landing_id`, `ip`, `type`, `is_scan`, `date_scan` (Ymd, kiểu chuỗi/số), `device`, `post_code`.

### 2.4. `App\LandingHistory` — `sns-line/app/LandingHistory.php`
- Table `landing_histories`, `$guarded = []`. Không relationship.
- Khoá logic: (`bot_id`, `landing_id`, `datestamp`).
- Cột số liệu: `date`, `count_click`, `count_click_distinct`, `count_scan`, `count_scan_distinct`, `count_scan_friend_new`, `count_action`, `count_action_distinct`, `count_add_friend`, `count_add_friend_new`, `count_add_friend_distinct`, `count_scan_pc`, `count_scan_pc_distinct`, `count_scan_mobile`, `count_scan_mobile_distinct`.

### 2.5. `App\LandingParameter` — `sns-line/app/LandingParameter.php`
- Table `landing_parameter`, `$guarded = []`, timestamps.
- `friendInformationSetting()` — hasOne `App\FriendInformationSetting` (`id` ← `friend_information_id`).
- Cột: `bot_id`, `landing_id`, `param_code` (`cid1`…`cid5`), `friend_information_id`.

### 2.6. `App\LandingConnectGoogle` — `sns-line/app/LandingConnectGoogle.php`
- Table `landing_connect_google`, `$guarded = []`.
- `STATUS = ['WAITING' => 0, 'PROCESSING' => 1, 'DONE' => 2, 'ERROR' => 3]` (`LandingConnectGoogle.php:13-18`).
- ⚠ **Dữ liệu thật có thêm giá trị `4` không khai báo trong `STATUS`** — 20 dòng dump: `2` = 11, **`4` = 8 (40%)**, `1` = 1. Xem rủi ro **R-17** (mục 9) về hệ quả nghiệp vụ. Nguồn ghi giá trị `4` chưa xác định trong `src/web/sns-line/app`. **Mức độ tin cậy về sự tồn tại: Cao; về ý nghĩa: Không xác định.**
- `landings()` — hasMany `Landing` theo `bot_id`.
- Cột: `bot_id`, `google_access_token` (JSON), `google_account_name`, `google_account_avatar`, `connect_time`, `status`.

### 2.7. Nhóm LP Poster

| Model | Table | Relationships |
|---|---|---|
| `App\PosterConnectQrCode` | `poster_connect_qrcode` | — (cột: `bot_id`, `landing_id`, `poster_name`) |
| `App\LandingPageConnectQrCode` | `landing_page_connect_qrcode` | — (cột: `bot_id`, `landing_id`, `landing_name`, `landing_url`) |
| `App\LandingPagePosterUrl` | `landing_page_poster_url` | `landingPage()` belongsTo `LandingPageConnectQrCode`; `connectQrCode()` belongsTo `PosterConnectQrCode`; `detailClicks()` hasMany `DetailLandingClick` (`post_code` ← `code`); `collectOpens()` hasMany `CollectOpenLanding` (`post_code` ← `code`) |

### 2.8. Model liên quan khác được dùng

`Bots`, `BotContracts`, `BotSlots`, `BotsTutorial`, `BotFriendStatistic`, `BotLineUser`, `BotSettingAff`, `BotSettingLevel`, `BotDurationLevelAff`, `Category` (kind = 10), `Template`, `Actions`, `ActionDetail`, `FilterV2`, `Tag`/`Tags`, `Scenario`, `RichMenus`, `LineUser`, `Conversation`, `MessagesV2`, `MessageError`, `AddFriendSetting`, `Affiliaters`, `AffResult`, `NotifySetting`, `User`, `Models\LineUserAddFriendHistory`, `FormAnswer`, `SItems`, `BEventDetail`, `BookingCalendar`, `CalendarManagement`, `CalendarSalon`, `SyncElasticsearch` (import nhưng **không dùng** trong controller).

---

## 3. Services / Repositories / Helpers

### 3.1. `App\Services\Landing\LandingCopyService` — `sns-line/app/Services/Landing/LandingCopyService.php`

| Method | Input | Output | Logic |
|---|---|---|---|
| `copyLandingParameter($newLandingId, $oldLandingId)` | 2 int | void | Lấy toàn bộ `landing_parameter` của (bot hiện tại, landing cũ), đổi `landing_id`, bỏ `id`, `insert()` hàng loạt (`:22-36`) |
| `copyLandingPoster($newLandingId, $oldLandingId)` | 2 int | void | Gọi lần lượt `copyPosterConnectQr` → `copyLandingPageConnectQr` → `PosterSettingService::saveLandingPagePosterUrl($newLandingId)` (`:38-43`) |
| `copyPosterConnectQr` | 2 int | void | Nhân bản `poster_connect_qrcode` (`:45-63`) |
| `copyLandingPageConnectQr` | 2 int | void | Nhân bản `landing_page_connect_qrcode` (`:65-84`) |

⚠ `copyLandingParameter` gọi `insert()` với mảng rỗng khi landing nguồn không có tham số — Laravel 5 xử lý được (no-op).

### 3.2. `App\Services\Landing\Poster\PosterSettingService` — `sns-line/app/Services/Landing/Poster/PosterSettingService.php`

| Method | Input | Output | Logic |
|---|---|---|---|
| `savePosterConnectQrCode($landingId, Request)` | | void | `updateOrCreate` từng 「広告名」 theo khoá (`bot_id`, `landing_id`, `id`); id cũ không còn trong payload ⇒ `removeLandingPagePosterUrlByPoster()` (`:167-192`) |
| `saveLandingPosterConnectQrCode($landingId, Request)` | | void | Tương tự cho `landing_page_connect_qrcode`; sau đó gọi `saveLandingPagePosterUrl()` (`:18-45`) |
| `saveLandingPagePosterUrl($landingId)` | int | void | **Sinh tích Descartes** `poster × landing_page`; mỗi cặp `updateOrCreate` một `landing_page_poster_url` với `code` sinh bởi `hashCodeLandingPagePosterUrl()` (`:47-79`) |
| `hashCodeLandingPagePosterUrl($botId, $landingId, $posterId, $lpId)` | 4 int | string | `Hashids::encode(sprintf('%s%s%s%s', ...))` — ⚠ nối chuỗi không có dấu phân tách ⇒ **có thể va chạm** (ví dụ `(1,12,3,4)` và `(11,2,3,4)` cùng cho `"11234"`) — Mức độ tin cậy: Cao (`:81-91`) |
| `getPosterConnectQrCodeByLandingId($landingId, ?array $select)` | | Collection | Mặc định select `id, poster_name`, lọc `bot_id` + `landing_id` (`:93-102`) |
| `getLandingsPageConnectQrByLandingId($landingId, ?array $select)` | | Collection | Mặc định select `id, landing_name, landing_url` (`:104-112`) |
| `getLandingQrStep4Data($landingId)` | int | array | Với mỗi poster, sinh danh sách LP kèm URL đã gắn `uland` + `postcode` (`:114-146`) |
| `parseLandingPosterUrl($url, $uland, $postcode)` | | string | `parse_url` → thêm/ghi đè query `uland`, `postcode` → dựng lại URL, giữ `fragment`. ⚠ Không kiểm `$parts['scheme']`/`['host']` ⇒ URL không có scheme sẽ gây `Undefined index` (`:148-165`) |
| `removeLandingPagePosterUrlByPoster($ids)` | array | void | `PosterConnectQrCode::destroy()` + xoá `landing_page_poster_url` liên quan (`:194-198`) |
| `removeLandingPagePosterUrlByLandingPage($ids)` | array | void | Tương tự cho `landing_page_connect_qrcode` (`:200-204`) |

### 3.3. `App\Services\PlanLimitGuard` — `sns-line/app/Services/PlanLimitGuard.php`

Chốt chặn giới hạn gói cho pattern "đếm rồi mới tạo" (issue #39230). Không dùng lock; đếm lại **sau** khi insert.

| Thành phần | Giá trị / mô tả |
|---|---|
| `LIMIT_MESSAGE` | 「上限に達したので、新しく追加できません。」 |
| `PLAN_MESSAGE` | 「現在のプランは利用できない機能です。アップグレードが必要になります。」 |
| `FEATURE_QR_CODE` | `'qr_code'` — hằng dùng cho tính năng này |
| `isOverLimit($query, $newId, $limit, $idColumn = 'id')` | Đếm số bản ghi cùng phạm vi có `id <= $newId` = "thứ tự" của bản ghi; thứ tự > hạn mức ⇒ thừa. `$limit === null` ⇒ không giới hạn. Lỗi đếm ⇒ trả `false` (giữ nguyên bản ghi) (`:100-120`) |
| `rollbackIfOverLimit(...)` | Gọi `isOverLimit`; nếu vượt ⇒ chạy callback `$rollback` (xoá bản ghi vừa tạo) rồi trả `true`. Dùng ở `saveLandingV2` (`:321`) và `saveLanding` (`:516`) |
| `rollbackIfOverTotal(...)` | Biến thể so tổng số bản ghi (không cần `newId`). Dùng ở `restoreQr` (`:1367`) |

**Nguyên tắc chọn bản ghi bị xoá**: bản có `id` **nhỏ hơn** (tạo trước) được giữ, bản `id` lớn hơn bị xoá — để 2 request đồng thời không cùng tự xoá.

### 3.4. `App\Services\Landing\LandingService` — `sns-line/app/Services/Landing/LandingService.php`
- Inject `App\Contracts\Repositories\LandingRepositoryInterface`.
- `getLandingsGroupedByFolder($botId)` → `[{folder_id, folder_name, landings: [{id, name}]}]`. Dùng bởi `Basic\LandingController@ajaxGroupedByFolder` (EP-61) — endpoint **dùng chung** cho picker QR ở các tính năng khác (kịch bản, action…). → Ứng viên **shared component**.

### 3.5. `App\Services\Landing\LandingGoogleSheetService` — `sns-line/app/Services/Landing/LandingGoogleSheetService.php`
- `insertDataToGoogleSheet($landing)` — lấy `landing_connect_google` theo `bot_id`, tự refresh access token khi hết hạn, tạo `Google_Service_Sheets`, gọi `executeInsert()` với dữ liệu lấy từ **`landing_histories`** (`:146`).
- Chỉ được gọi từ cron `landing:insert_google_sheet`, **không** từ controller.

### 3.6. Helper functions (`sns-line/app/Helpers/functions.php`)

| Helper | Dòng | Vai trò trong tính năng |
|---|---|---|
| `getBotId()` | — | Lấy bot đang chọn từ session — nền tảng của toàn bộ multi-tenant |
| `getCurrentUser()` | — | Lấy user id (dùng khi tạo đường dẫn thư mục ảnh QR) |
| `checkPlanFreeBotLimitFeature($bot)` | — | Trả `1` khi bot thuộc gói free "mới" bị giới hạn tính năng |
| `checkUpdateHasTutorial($botId)` | — | Cập nhật trạng thái hoàn thành tutorial |
| `syncNotifyNewItemForBot($botId, $itemId, 'is_all_qrcode_new', 'when_adding_friends')` | `:12005-12034` | Với mỗi `notify_setting` của bot: nếu cờ `is_all_qrcode_new` bật ⇒ thêm `landing_id` vào chuỗi CSV cột `when_adding_friends`; ngược lại loại bỏ |
| `sendAction($actionId, $lineUserId, $botId, ...)` | `:8056` | **Thực thi action** — xem mục 6 (ghi chú job-analyzer) |
| `addLogUserAction($name)` | — | Ghi log thao tác người dùng |
| `getInfoFromLine($bot, $lineId)` | — | Gọi LINE Profile API |
| `uploadFile($file, $prefix, $dir)` | — | Upload logo QR |
| `resizeImageToMaxSize($src, $dst, 2048)` | — | Resize logo |
| `notifyChatworkException($msg)` / `notifyChatworkChat11($msg)` | — | Cảnh báo qua Chatwork |
| `updateMessageSendCount($botId, $date, $n)` | — | Đếm tin nhắn đã gửi (dùng ở `quickSendQr`) |
| `returnResponseSendMessageV2(...)` | — | Chuẩn hoá response khi gửi tin thất bại |
| `getRouterBotInvite()` | `:4696` | Whitelist route của Staff theo `bot_role_access` ⨝ `access_feature` |
| `customeCreateFileLog(...)` | — | Ghi log cron vào file `job_crontab` |

### 3.7. `App\Category` (phần liên quan QR) — `sns-line/app/Category.php`

Thư mục QR dùng `kind = 10` (= `config('sns-line.category_kind.landing')`).

| Static method | Dòng | Logic |
|---|---|---|
| `getListCategoryLanding(array $params = [])` | `:1550-1582` | LEFT JOIN `landing` để đếm số QR mỗi thư mục (`count`), lọc `bot_id`, `is_deleted = 0`, `kind = 10`, `land.deleted_at IS NULL`; hỗ trợ lọc `keyword` và `action_with_friend` ngay trong điều kiện JOIN; sắp xếp `position DESC, id DESC` |
| `getCategoryLandingDefault($perPage = null)` | `:1640+` | Danh sách QR không thuộc thư mục (`category_id = 0` hoặc `NULL`), sắp `position ASC, id DESC`, kèm dựng `new_link_qr_code` theo `domain_url_shorten` / `URL_OUTSIDE_STEP` |
| `getCategoryLandingGroups($groupId, $perPage)` | — | Danh sách QR trong 1 thư mục |
| `getLandingOfCategory($category)` | `:1588+` | Danh sách QR + dựng URL rút gọn + format `created_at` dạng `Y.m.d` |

### 3.8. Exports (Maatwebsite Excel)

| Class | Dùng cho | Nguồn |
|---|---|---|
| `App\Exports\DetailLandingClickExport` | Tab 1 — CSV theo ngày | `QRCodeController.php:2264` |
| `App\Exports\LandingListFriendExport` | Tab 2 — CSV theo bạn bè | `QRCodeController.php:2265` |
| `App\Exports\LandingPageUrlExport` | Tab 3 — CSV theo LP/広告 | `QRCodeController.php:2266` |

---

## 4. Form Requests / Validation

**Không có FormRequest class riêng cho tính năng này.** Toàn bộ validation nằm inline trong controller. Bảng tổng hợp đầy đủ:

| Endpoint | Method | Rules | Message tuỳ chỉnh | Nguồn |
|---|---|---|---|---|
| EP-59 POST `/basic/landing/edit/{id}` | `saveEditLanding` | `name` → `required|max:255` | `name.required` → 「QRコードアクション名は必須です。」 | `:641-645` |
| EP-23 POST `.../setting-option` | `saveSettingOption` | `setting_logo` → `required|in:1,2,3`<br>`type_design_qr` → `required|in:1,2,3,4`<br>`color_qr` → `nullable|regex:/^#(?:[0-9a-fA-F]{3}){1,2}$/`<br>`text_design_qr` → `nullable`<br>*(khi có file)* `path_logo` → `image|mimes:jpeg,png,jpg,gif,svg|max:10240` | — | `:3507-3512`, `:3521-3523` |
| EP-26 POST `.../external-setting` | `saveExternalSetting` | `url_connect_qrcode_outside` → `nullable|url` (chỉ khi có giá trị, bọc try/catch) | Lỗi ⇒ HTTP **410** + 「有効なURLではありません。」 | `:3711-3719` |
| EP-30 POST `.../poster-connect-qr-code` | `storePosterConnectQrCode` | `poster_names` → `required|array` | — | `:3855-3857` |
| EP-32 POST `.../landing-url-qr-code` | `storeLandingPosterConnectQrCode` | `landing_connect_qr` → `required|array` | — | `:3901-3903` |

**Mọi endpoint còn lại không có validation server-side** — đặc biệt:
- EP-50 (tạo QR): `name` chỉ được kiểm ở client (`index.js:421-429`: bắt buộc, ≤ 50 ký tự).
- EP-06 (`update-basic`): `name` không giới hạn độ dài ở server.
- EP-11 (`setting-limit`): không kiểm `limit_end_time > limit_start_time` (chỉ client `mixins/setting_limit.js:83-91`).
- EP-10 (`setting-introduce`): `intro_message` không kiểm 500 ký tự dù cột DB là `varchar(500)`.

**Validation phía client** (vee-validate + kiểm thủ công):

| Màn hình / file JS | Quy tắc |
|---|---|
| `index.js:421-429` | Tên QR: bắt buộc 「管理名を入力してください」, ≤ 50 ký tự 「管理名は50文字以内で入力してください。」 |
| `mixins/setting_option.js:100-128` | Logo: chỉ `.png/.jpg/.jpeg`, ≤ 10 MB 「10MB以下のイベントバナーをアップしてください。」, kiểm kích thước qua `validateImageDimensions` |
| `mixins/setting_option.js:187-190` | `color_qr` phải khớp `/^#[0-9A-Fa-f]{6}$/i` |
| `mixins/setting_qr_off.js:169+` | Text OFF không được rỗng 「指定ページを入力してください。」; URL phải hợp lệ |
| `mixins/setting_external_link.js:194+` | URL ngoài phải parse được bởi `new URL()` 「有効なURLではありません。」 |
| `mixins/lp_poster/step1.js:78+` | 広告名 bắt buộc 「この広告名を入力してください。」, không trùng |
| `mixins/lp_poster/step2.js:30-40` | LP 管理名 không trùng 「この管理名はすでに登録されています。」 |
| `mixins/setting_detail.js:45` | Cảnh báo xác nhận khi chuyển `action_type` 2 → 1 |

---

## 5. Events / Listeners / Queued Jobs

**Không có Laravel Event / Listener / Queued Job (`dispatch()`, `ShouldQueue`) nào được dùng trong tính năng này.** (Mức độ tin cậy: Cao — đã grep toàn bộ controller và các service liên quan.)

Thay vào đó hệ thống dùng **Artisan Console Commands chạy theo cron** — xem mục 6.

---

## 6. Ghi chú cho job-analyzer

> ✅ **CÓ dấu hiệu background job rõ ràng.**

### 6.1. Laravel Console Commands (đăng ký trong `sns-line/app/Console/Kernel.php`)

| Signature | Class | Lịch chạy | Bảng ghi/đọc | Nguồn |
|---|---|---|---|---|
| `statistic:landing_action` | `App\Console\Commands\JobStatisticLanding` | `dailyAt('02:05')` (`Kernel.php:196`) | **Đọc** `landing`, `detail_landing_click`, `collect_open_landings` → **Ghi (`updateOrCreate`)** `landing_histories` | `app/Console/Commands/JobStatisticLanding.php` |
| `landing:insert_google_sheet` | `App\Console\Commands\JobInsertStatisticDataActionLandingToGoogleSheet` | `dailyAt('02:10')` (`Kernel.php:177`) | **Đọc** `landing` ⨝ `landing_connect_google` (status `DONE`, có token), `landing_histories`; **Ghi** `landing.google_sheet_id`; **đẩy dữ liệu lên Google Sheets API** | `app/Console/Commands/JobInsertStatisticDataActionLandingToGoogleSheet.php` + `app/Services/Landing/LandingGoogleSheetService.php` |
| `landing:qr-off:schedule` | `App\Console\Commands\HandleQrOffSchedule` | `everyMinute()` (`Kernel.php:199`) | **Đọc/Ghi** `landing` — bật/tắt `status` theo `limit_start_time` / `limit_end_time`, chuyển `time_qr_off_status` | `app/Console/Commands/HandleQrOffSchedule.php` |
| `landing:force-delete` | `App\Console\Commands\ForceDeleteQrLandingCommand` | `dailyAt('05:05')` (`Kernel.php:189`) | **Xoá cứng** `landing` và `detail_landing_click` của các QR đã xoá mềm > **90 ngày** | `app/Console/Commands/ForceDeleteQrLandingCommand.php` |

#### Chi tiết `JobStatisticLanding` (quan trọng nhất)
- `Landing::chunk(1000, ...)` — duyệt **toàn bộ** landing của toàn hệ thống (không lọc `bot_id`).
- Với mỗi landing, tổng hợp `detail_landing_click` của **hôm qua** (`whereDate('time_click', now()->subDay())` khi `$isAllStatistic = false`), `GROUP BY DATE(time_click)`, tính 12 chỉ số (`JobStatisticLanding.php:60-84`).
- Tổng hợp `collect_open_landings` với `date_scan >= '20250925'` (hardcode) và `(is_scan=1 AND type=PC) OR type=MOBILE`, `GROUP BY date_scan` (`:86-97`).
- `saveHistories()` — `updateOrCreate` vào `landing_histories` theo khoá (`bot_id`, `landing_id`, `datestamp`) — **2 lần cho cùng khoá** (một lần cho nhóm chỉ số từ `detail_landing_click`, một lần cho `count_click*` từ `collect_open_landings`) (`:100-137`).
- ⚠ Cột `qr_scan_from_device` được dùng để phân biệt PC/mobile trong job, nhưng **không thấy code Laravel nào ghi cột này** ⇒ khả năng cao do **Spring Boot job** ghi (cần job-analyzer xác nhận).

#### Cơ chế trạng thái của `HandleQrOffSchedule`

`landing.time_qr_off_status` là **cột hàng đợi** (queue-like column):

| Giá trị | Hằng số | Ý nghĩa |
|---|---|---|
| `0` | `UPDATED` | Đã xử lý xong |
| `1` | `READY_UPDATE` | Chờ cron xử lý (được set bởi `saveSettingQrOff` và `ajaxUpdateBasicQrs`) |
| `2` | `PENDING` | Cron đã nhặt, đang xử lý |
| `3` | `PROCESSING_END_TIME` | Đã bật QR, đang chờ tới `limit_end_time` để tắt |

Luồng: cron chạy mỗi phút → lấy các landing `use_limit_time = 1` và (`time_qr_off_status = 1` và `limit_start_time <= now`) hoặc (`time_qr_off_status = 3` và `use_limit_end_time = 1` và `limit_end_time <= now`) → đánh dấu `PENDING` hàng loạt → xử lý từng bản ghi, set `status = 1` (bật) hoặc `status = 0` (tắt) và cập nhật `time_qr_off_status`.

### 6.2. Spring Boot job (`src/job/linect-service`) — **liên quan trực tiếp**

Tồn tại các entity/repository/manager mang tên landing rõ ràng:

| File | Vai trò suy đoán |
|---|---|
| `src/job/linect-service/src/main/java/sns/line/helper/LandingManager.java` | **Xử lý chính** luồng landing khi nhận callback từ LINE |
| `.../models/linedb/entities/LandingQR.java` | Entity map bảng `landing` |
| `.../models/linedb/entities/DetailLandingClick.java` + `.../repository/DetailLandingClickRepository.java` + `.../readrepository/DetailLandingClickReadRepository.java` | **Ghi/đọc `detail_landing_click`** — đây là nơi bản ghi kết bạn qua QR được tạo |
| `.../models/linedb/entities/CollectOpenLanding.java` + `.../repository/CollectOpenLandingRepository.java` | Ghi/đọc `collect_open_landings` |
| `.../models/linedb/entities/LandingParameter.java` + `.../repository/LandingParameterRepository.java` | Đọc mapping `cid1..cid5` để ghi thông tin bạn bè khi kết bạn |
| `.../models/linedb/entities/TimeActionLanding.java` + `.../repository/TimeActionLandingRepository.java` | Quản lý khoảng cách thời gian chạy lại action (`interval_action`, `time_interval_action`) |
| `.../models/linedb/entities/LineUserAddFriendHistory.java` | Lịch sử kết bạn |
| `.../task/MappingDeviceTask.java` | Ghép `device_id` (cookie trang QR) với `line_user` — giải thích cách `detail_landing_click.device_id` được điền |
| `.../task/HandlePostbackTask.java` | Xử lý postback |
| `.../models/historydb/entities/SyncElasticsearch.java`, `.../models/SyncEsModel.java` | Đồng bộ Elasticsearch |
| `.../models/linedb/readrepository/LandingQRReadRepository.java` | Đọc cấu hình QR |
| `.../models/linedb/services/CrossModelService.java` | Xử lý cross-data |
| `.../threads/csv/HandleExportCsvTask.java`, `HandleImportCsvTask.java` | Export/import CSV có tham chiếu landing |
| `.../threads/changebot/ChangeBotJob.java` + `.../repository/ChangeBotDataCleanupRepository.java` | Dọn dữ liệu landing khi đổi bot |

**Kết luận cho job-analyzer** *(đã đính chính — xem V-03 trong `_internal/validation-report.md`)*: luồng "quét QR → kết bạn → chạy action → ghi thống kê chi tiết" được **chia làm 2 giai đoạn, KHÔNG nằm trọn ở Spring Boot**:

| Giai đoạn | Nơi xử lý | Việc làm | Nguồn |
|---|---|---|---|
| **G1 — Mở trang QR / LIFF** | **Laravel** `LiffController` | INSERT `collect_open_landings` (`LiffController.php:1207-1216`), INSERT `detail_landing_click` với `action = 1` (`:1222-1237`), tăng `landing.total_user_click` (`:1218-1220`) | Đọc trực tiếp source |
| **G2a — Kết bạn qua LIFF (đồng bộ)** | **Laravel** `LiffController` | UPDATE `detail_landing_click.action = 2` + `bot_line_user_id` (`:1325`, `:1411`), tăng `landing.total_user_friend` (`:1327`, `:1413`), UPDATE `is_old_friend` (`:1649`, ghi đè khi unblock tại `:1667`) | Đọc trực tiếp source |
| **G2b — Kết bạn qua webhook LINE (bất đồng bộ)** | **Spring Boot** `HandlePostbackTask` / `LandingManager` | UPDATE `detail_landing_click` (`action = 2`, `is_old_friend` **chỉ 0 hoặc 1**, `bot_line_user_id`, `is_action_web = 2`, `action_multi_capture_id`, `message_id`), UPDATE `collect_id` qua `MappingDeviceTask` | `DetailLandingClickRepository` (Spring Boot) **chỉ có lệnh UPDATE, không có INSERT** |
| **G3 — Tổng hợp / hiển thị** | **Laravel** | Cron `statistic:landing_action` ghi `landing_histories`; các endpoint EP-16/37/38/39/41 đọc số liệu | — |

> ⚠ **Điểm dễ hiểu nhầm**: Spring Boot **không bao giờ tạo mới** bản ghi `detail_landing_click`, và **không hề ghi** `collect_open_landings` (repository Java chỉ có **1 native SELECT**). Khi debug thiếu bản ghi, phải tìm ở **Laravel `LiffController`** trước.

### 6.3. Điểm gọi `sendAction()` từ Laravel trong tính năng này

- `QRCodeController.php:3013` — `sendAction($settingAddFriend->action_old_id, $lineUser->id, $bot->id, null, 1002, true, [], null, null, null, null, $lineUserHistory->id)` trong `checkFriend()`.
- `sendAction()` (`app/Helpers/functions.php:8056+`) chạy **đồng bộ** nhưng có side effect lan rộng: cập nhật `conversation` (bookmark/block), `bot_line_user`, `scenario_lineuser`, `scenario_lineuser_history`, `scenario_step_time`, gọi `FilterV2::initDataFilter`, `Conversation::advanceFilterPost`, và có thể ghi `sync_elasticsearch`.
- **Không** thấy ghi trực tiếp vào các bảng hàng đợi `action_line_users`, `callback_event`, `csv_management`, `broadcast`, `action_schedules` từ `QRCodeController`.
- `App\SyncElasticsearch` được `use` ở đầu controller (`QRCodeController.php:57`) nhưng **không hề được gọi** trong file.

### 6.4. Bảng dữ liệu chia sẻ giữa Laravel / job — ai TẠO, ai CẬP NHẬT, ai ĐỌC

> **Đã sửa theo V-03** (`_internal/validation-report.md` mục 6.H). Bảng cũ gán sai chủ thể ghi: nói `detail_landing_click` do Spring Boot ghi (thực tế Laravel **tạo**, Spring Boot chỉ **cập nhật**) và `collect_open_landings` do 「Laravel + Spring Boot」 (thực tế **chỉ Laravel**).

| Bảng / cột | Laravel **TẠO** (INSERT) | Laravel **CẬP NHẬT** (UPDATE) | Spring Boot **CẬP NHẬT** (UPDATE) | Đọc bởi (Laravel) |
|---|---|---|---|---|
| `landing_histories` | — | Cron `statistic:landing_action` (`JobStatisticLanding.php`) — **chỉ Laravel** | ❌ Không | EP-16 tab 1 (`QRCodeController.php:1913-1962`) |
| `detail_landing_click` | ✅ **`LiffController.php:1222-1237`** — `action = 1`, `is_old_friend = 0`, `time_click`, `qr_scan_from_device` (`:1234`), `device_id`, `is_landing_off`, `post_code`, `popup_id`, `user_intro_id` | ✅ `LiffController.php:1325`, `:1411` (`action = 2`, `bot_line_user_id`); `:1649` (`is_old_friend`, **bao gồm giá trị `2` và `3`**); `:1667` (ghi đè `2` → `1`/`3` khi unblock) | ✅ `HandlePostbackTask` (`action = 2`, `is_old_friend` **chỉ `0`/`1`**, `bot_line_user_id`), `is_action_web = 2` (`DetailLandingClickRepository.updateIsActionWebById`), `action_multi_capture_id`, `message_id`, `collect_id` (`MappingDeviceTask`) — **KHÔNG có lệnh INSERT nào** | EP-16 tab 2, EP-37, EP-38, EP-39, EP-41; cron A-1 |
| `collect_open_landings` | ✅ **CHỈ Laravel** — `QRCodeController@countScan` EP-64 (`:2318`) và `LiffController.php:1207-1216` (`type = 2`, `is_scan = 1`) | — | ❌ **Không ghi** — `CollectOpenLandingRepository` (Spring Boot) có **duy nhất 1 native SELECT** `findIdByDeviceAndLandingId`, gọi từ `MappingDeviceTask.java:49` | EP-16 tab 1 & tab 3, EP-37, EP-39; cron A-1 |
| `landing.status`, `landing.time_qr_off_status` | — | Cron `landing:qr-off:schedule` (`HandleQrOffSchedule.php`) — **chỉ Laravel** | ❌ Không | EP-02, EP-24 |
| `landing.total_user_click` | — | `LiffController.php:1218-1220`, `QRCodeController.php:2314-2316` (EP-64) | ❌ Không | EP-02, EP-16 |
| `landing.total_user_friend` | — | ✅ `LiffController.php:1327`, `:1413` | ✅ `LandingQRRepository` (native UPDATE) | EP-02 |
| `landing.google_sheet_id` | — | Cron `landing:insert_google_sheet` + EP-50 | ❌ Không | EP-49 |

**Mức độ tin cậy: Cao** — kết luận dựa trên đọc trọn vẹn `CollectOpenLandingRepository.java` (12 dòng, 1 query SELECT), `DetailLandingClickRepository.java` (chỉ `@Modifying` UPDATE), và `LiffController.php:1200-1670`. Xác nhận thêm: `grep -rn "qr_scan_from_device|qrScanFromDevice" src/job/` ⇒ **0 kết quả** ⇒ cột `qr_scan_from_device` **do Laravel ghi** (`LiffController.php:1234`), không phải Spring Boot.

---

## 7. Authorization

### 7.1. Cơ chế phân quyền

1. **Xác thực**: session Laravel (`Auth::check()`), thêm `check_remember_token` để vô hiệu session cũ sau khi đổi mật khẩu.
2. **Chọn bot (multi-tenant)**: `getBotId()` đọc từ session. Mọi truy vấn *nên* lọc theo `bot_id` này.
3. **Phân quyền Staff**: `BasicAccess` middleware — khi user không phải chủ bot (`bots.admin_id !== Auth::id()`), lấy `UserStaffBot` (theo `user_invite_id` + `bot_id` + `status = 1`) → `BotRoleAccess` ⨝ `access_feature` → whitelist tên route. Route hiện tại không có trong whitelist ⇒ redirect kèm lỗi 「この権限は許可されていません。」 (`BasicAccess.php:34-52`, `functions.php:4696-4726`).
4. **Route `landingIndex`** được seed vào `access_feature` với tên hiển thị 「流入アクション」 (`database/seeds/AccessFeatureSeeder.php:15-22`), cùng 3 route con `landing.create`, `landing.show`, `landing.edit`.
5. **Không có Policy / Gate** nào cho `Landing` (Mức độ tin cậy: Cao).

### 7.2. Ma trận kiểm quyền sở hữu `bot_id`

| Endpoint | Method | Kiểm `bot_id`? | Ghi chú |
|---|---|---|---|
| EP-02 `ajaxGetListQrs` | ✅ | `where('bot_id', $botId)` |
| EP-03 `ajaxDeleteQrs` | ✅ | `whereIn('id',$ids)->where('bot_id',$botId)` |
| EP-04 `ajaxMoveCategory` | ❌ | `Landing::whereIn('id',$ids)->update(...)` — `:1006-1007` |
| EP-06 `ajaxUpdateBasicQrs` | ✅ | Ném 404 nếu lệch — `:1018` |
| EP-07 `ajaxGetQrsRemoved` | ✅ | |
| EP-08 `restoreQr` | ✅ | |
| EP-09 `settingDetail` | ❌ | Route model binding không kiểm — `:1405` |
| EP-10 `settingIntroduce` | ❌ | `:1443` |
| EP-11 `settingLimit` | ❌ | `:1490` |
| EP-12 `updateConnectAsp` | ⚠ Một phần | Reset theo `bot_id` nhưng `$qr` không kiểm — `:1391-1393` |
| EP-13 `ajaxGetPreviewAction` | ❌ | `Landing::find($id)` — `:1519` |
| EP-14 `ajaxGetPreviewActionIntro` | ❌ | `:1559` |
| EP-16 `ajaxInitDataDetailV2` | ❌ | `Landing::select('id','name')->where('id',$id)` — `:1863` (nhưng các bảng thống kê **có** lọc `bot_id`) |
| EP-18 `ajaxCreateCategory` | ⚠ Một phần | Nhánh đổi tên theo `id` không lọc — `:1088-1091` |
| EP-19 `ajaxUpdateCategory` | ✅ | |
| EP-20 `ajaxDeleteCategory` | ✅ | |
| EP-21 `ajaxSortCategory` | ❌ | `Category::where('id',$id_sort)->update(...)` — `:1153` |
| EP-22 `getSettingAction` | ✅ | 404 `Qrcode not found` |
| EP-23 `saveSettingOption` | ✅ | |
| EP-24 `getLandingData` | ✅ | |
| EP-25 `saveSettingQrOff` | ✅ | |
| EP-26 `saveExternalSetting` | ✅ | |
| EP-27 `saveExternalParameters` | ❌ | `Landing::where(['id'=>$landingId])->update(...)` — `:3743-3747` |
| EP-28 `getExternalParameters` | ✅ | Lọc `bot_id` trên `landing_parameter` |
| EP-29…EP-33 (LP Poster) | ✅ | `PosterSettingService` luôn lọc `bot_id` |
| EP-34 `getHashId` | ❌ | `Landing::find($landingId)` — `:3936` |
| EP-35 `getLandingUrlFilter` | ✅ | |
| EP-37/38/39 (thống kê) | ✅ | Lọc `bot_id` trên bảng thống kê (nhưng không kiểm landing thuộc bot) |
| EP-42 `sortQRCode` | ❌ | `Landing::find($id)` rồi update — `:2712-2715` |
| EP-45 `savePreviewIntro` | ❌ | `Landing::where('id',$idLanding)` — `:3442` |
| EP-46 `editLandingV2` | ✅ | |
| EP-47 `editLandingPoster` | ✅ | |
| EP-48 `previewMessageScanQr` | ❌ | `Landing::find($id)` — `:1511` |
| EP-49 `showFriendClick` | ✅ | |
| EP-50 `saveLandingV2` (chế độ copy) | ❌ | `Landing::select(...)->where('id',$request->input('id'))` — `:245-247` |
| EP-53 `cancelGoogleSheet` | ❌ | `LandingConnectGoogle::where('id',$id)` — `:1288` |
| EP-56 `editLanding` | ✅ | |
| EP-59 `saveEditLanding` | ❌ | `Landing::where('id',$id)->update(...)` — `:657` |
| EP-60 `delete` (v1) | ❌ | `Landing::whereIn('id',$idLandings)->delete()` — `:1706` |
| EP-63…EP-69 (Public) | N/A | Không có khái niệm bot_id session |

### 7.3. Kiểm gói cước (plan gating)

| Kiểm tra | Áp dụng cho | Nguồn |
|---|---|---|
| `checkPlanFreeBotLimitFeature($bot) == 1` ⇒ tối đa **3 QR** | EP-50, EP-58, EP-08 | `:213-226`, `:462-473`, `:1339-1351` |
| `bots.plan_type == 2` (free) ⇒ **cấm** tính năng | EP-23 (thiết kế QR), EP-30/EP-32 (LP Poster ghi), EP-47 (màn LP Poster) | `:3518`, `:3849`, `:3896`, `:3824` |
| `bots.plan_type == 2` ⇒ trả dữ liệu rỗng | EP-33 | `:3921-3923` |
| Bot hết hạn > 7 ngày hoặc `bot_contracts.status = 3` | EP-63 (public) ⇒ redirect `410` | `:1670-1676` |

---

## 8. Business Rules

| ID | Quy tắc | Mức độ tin cậy | Nguồn |
|---|---|---|---|
| BR-01 | Mỗi QR có mã `code` random 6 ký tự (`str_random`), **duy nhất trong phạm vi 1 bot** (không phải toàn hệ thống) — sinh đệ quy tới khi không trùng | Cao | `QRCodeController.php:180-194`, `:284-286` |
| BR-02 | Link QR chuẩn hiển thị trên màn danh sách và màn sửa: `{env(URL_OUTSIDE_STEP)}landing-qr/{bots.liff_app_id}?uLand={landing.code}`. **KHÔNG dùng `domain_url_shorten`** — code ghi rõ comment 「không cần check domain_url_shorten: đã confirm anh Tư」. `domain_url_shorten` chỉ được ưu tiên ở `Category::getCategoryLandingDefault()` và `pageIntro()` (EP-65) | Cao | `:625-628` (EP-46), `:947-955` (EP-02), `:3403-3411` (EP-65) |
| BR-03 | Ảnh QR được sinh ngay khi tạo (BaconQrCode PNG 300×300), mã hoá URL `https://line.me/R/app/{liff_app_id}?uLand={code}`, lưu tại `{FOLDER_MEDIA}images/{user_id}/{bot_id}/landing/{ts}{rand}_{id}.png` | Cao | `:353-377` |
| BR-04 | Bot gói free "mới" (`checkPlanFreeBotLimitFeature = 1`) chỉ được tạo/khôi phục tối đa **3 QR**. Kiểm 2 lần: trước insert (thông báo thân thiện) và sau insert (`PlanLimitGuard`, xoá bản ghi thừa) | Cao | `:213-226`, `:321-338`, `:1339-1382` |
| BR-05 | Khi 2 request tạo QR đồng thời cùng lọt qua cửa kiểm: bản ghi `id` **nhỏ hơn** được giữ, bản `id` lớn hơn bị xoá và báo lỗi | Cao | `Services/PlanLimitGuard.php:100-120` |
| BR-06 | Chỉ **một** QR trong bot được `connect_aff = 1` (dùng cho luồng affiliate). Đặt QR mới ⇒ reset tất cả về `0` trước | Cao | `:1386-1403`, `:506-513`, `:646-653` |
| BR-07 | `status`: `0` = 非公開 (QR OFF), `1` = 公開. Khi OFF: `type_display_off = 0` ⇒ vẫn render trang (chạy action); `= 1` ⇒ hiển thị text; `= 2` ⇒ redirect URL | Cao | `:1678-1689`, `Landing.php:14-16` |
| BR-08 | Bật/tắt QR bằng tay từ danh sách sẽ tính lại `time_qr_off_status` theo lịch giới hạn hiện có (bảng ở mục 1.8) | Cao | `:1039-1050` |
| BR-09 | Lịch bật/tắt tự động do cron `landing:qr-off:schedule` (mỗi phút) thực thi qua cột trạng thái `time_qr_off_status` (`0` = xong, `1` = chờ, `2` = đang xử lý, `3` = chờ giờ kết thúc). **Bổ sung giá trị `NULL`**: schema `landing.sql:78` khai báo `time_qr_off_status tinyint(4) DEFAULT NULL` — **không có DEFAULT 0** — và `saveLandingV2` (`:294-317`) không gán cột này khi INSERT ⇒ **mọi QR mới tạo qua EP-50 đều có `NULL`**. `NULL` = 「chưa từng vào luồng lịch」, là **trạng thái hợp lệ**, không phải dữ liệu hỏng. Cron **không nhặt** bản ghi `NULL` (trong SQL `NULL = 1` cho `NULL`, không phải `TRUE`) ⇒ không gây lỗi runtime. Dữ liệu thật: `NULL` = **565/566**, `0` = **1**, không có dòng nào `1`/`2`/`3` (đối chiếu: `use_limit_time = 1` chỉ ở **2/566** dòng) | Cao | `Console/Commands/HandleQrOffSchedule.php:16-19, 52-66`, `db/schema/tables/landing.sql:78`, `QRCodeController.php:294-317`, `db/data/landing.sql` |
| BR-10 | Thay đổi lịch qua EP-25 (`qr-off`) sẽ đặt `time_qr_off_status = 1`; **thay đổi qua EP-11 (`setting-limit`) thì không** ⇒ cron sẽ không nhận | Trung bình | So sánh `:3644-3652` với `:1490-1507` |
| BR-11 | QR xoá mềm nằm trong thùng rác; cron `landing:force-delete` (05:05 hằng ngày) **xoá cứng** sau **90 ngày** | Cao | `Console/Commands/ForceDeleteQrLandingCommand.php:43-60` |
| BR-12 | Khôi phục QR sẽ **tự khôi phục thư mục cha** nếu thư mục đang bị xoá mềm | Cao | `:1358-1362` |
| BR-13 | Xoá thư mục ⇒ **xoá mềm toàn bộ QR bên trong** và `detail_landing_click` của chúng | Cao | `:1127-1147`, `:807-818` |
| BR-14 | Thư mục QR dùng `category.kind = 10`; `position` mới = `max(position) + 1` trong phạm vi bot | Cao | `:1096-1105`, `Category.php:1571` |
| BR-15 | Tin nhắn văn bản của QR được lưu thành bản ghi `template` ẩn với `category_id = -111222`, `type = 'text'`, `position = 0`. Nội dung rỗng ⇒ xoá template và set FK về `null` | Cao | `:1416-1435`, `:1459-1478`, `:280-282` |
| BR-16 | Sao chép QR (`mode = copy`) sẽ nhân bản: 3 action (`action_id`, `user_introduction_action_id`, `action_limit_id`) kèm bản ghi bảng `t_actions_detail` (model `App\ActionDetail`) và filter (`filters_v2`); 2 template; `landing_parameter`; `poster_connect_qrcode`; `landing_page_connect_qrcode`; và sinh lại `landing_page_poster_url` | Cao | `:234-277`, `:341-348`, `Services/Landing/LandingCopyService.php` |
| BR-17 | Sao chép QR **luôn sinh `code` mới** và **không** copy: `google_sheet_id`, `path_landing`, `position`, số liệu thống kê | Cao | `:238-244` (danh sách cột whitelist), `:284-286` |
| BR-18 | Bot lần đầu tạo QR ⇒ đánh dấu `bots_tutorial.status_qr_code = 1` | Cao | `:339-340` |
| BR-19 | Tạo QR mới ⇒ id QR được thêm vào cột `notify_setting.when_adding_friends` cho mọi user của bot có cờ `is_all_qrcode_new` bật | Cao | `:350-351`, `Helpers/functions.php:12005-12034` |
| BR-20 | Nếu bot đã liên kết Google, mỗi QR mới sẽ được tạo một Google Spreadsheet riêng ngay khi tạo. Lỗi tạo sheet **không** làm hỏng việc tạo QR (chỉ log + thông báo Chatwork) | Cao | `:379-417` |
| BR-21 | Không thể huỷ liên kết Google khi `landing_connect_google.status ∈ {WAITING(0), PROCESSING(1), ERROR(3)}` — thông báo chờ 3–5 phút. ⚠ Giá trị **`4`** (tồn tại thật ở 8/20 dòng) **không** nằm trong danh sách chặn ⇒ vẫn huỷ được — xem R-17 | Cao | `:1290-1296`; `db/data/landing_connect_google.sql` |
| BR-22 | Huỷ liên kết Google ⇒ xoá `google_sheet_id` của **toàn bộ** landing thuộc bot, kể cả bản đã xoá mềm (`withTrashed`) | Cao | `:1305` |
| BR-23 | Trang QR (`/landing-qr/{liffId}`) tra cứu bằng **`uLand`**, không dùng `{liffId}` trên path | Cao | `:1651-1653` |
| BR-24 | Truy cập trang QR khi bot trả phí đã hết hạn > 7 ngày (hoặc `bot_contracts.status = 3`) ⇒ HTTP redirect tới trang `410` | Cao | `:1666-1676` |
| BR-25 | Lượt mở trang QR được ghi vào `collect_open_landings`. `is_scan = 1` khi mở từ mobile (`type = 2`) hoặc tham số `device = pc`; chỉ khi đó mới tăng `landing.total_user_click` | Cao | `:2308-2325` |
| BR-26 | `device_id` được sinh ở client (random 6 ký tự + timestamp) và lưu cookie `device_scan_landing` TTL **365 ngày** — dùng để đếm unique theo thiết bị | Cao | `resources/views/basic/qr_code/qr_landing.blade.php:67-95` |
| BR-27 | Thống kê tab 1 lấy từ bảng tổng hợp `landing_histories` cho các ngày quá khứ, **ngày hôm nay tính realtime** từ `detail_landing_click` + `collect_open_landings` | Cao | `:1913-1917`, `:1963-1976`, `:2490-2531` |
| BR-28 | `type_count = 1` = đếm **unique** (theo `line_id` với dữ liệu bạn bè, theo `device` với dữ liệu quét); `type_count = 2` = đếm tất cả lượt | Cao | `:1981-1985`, `:2093-2100`, `:2349-2363` |
| BR-29 | Phân loại bạn bè 「友だちの種類」 trong `detail_landing_click` — xác định bằng **cặp** `(action, is_old_friend)`. **Xem bảng chi tiết ngay dưới bảng Business Rules** (mục 「BR-29 — chi tiết」). Tóm tắt: `(2,0)` = 「新規友だち」 · `(2,1)` = 「ブロックを解除した友だち」 · `(1,1)` = 「エルメ上の友だち」 · `(2,3)` = 「既存友だち」 · `(1,0)` = 「友だち追加なし (URL読込みのみ)」 · `is_old_friend = 2` bị loại khỏi mọi thống kê | Cao | `show_friend_click.blade.php:348-363`, `LandingListFriendExport.php:36-39`, `QRCodeController.php:2404-2409, :2420-2436`, `LiffController.php:1639-1649` |
| BR-30 | Số người đã block (`total_block`) chỉ tính những người mà **lần kết bạn đầu tiên** là qua chính QR này (so `MIN(time_click)` với các landing khác) | Cao | `:2018-2045`, `DetailLandingClick.php:31-54` |
| BR-31 | CSV xuất ra được chuyển sang encoding **Shift_JIS** với tên file `export.csv`; client đặt lại tên thành `detail_landing_click_{YYYYMMDDhhmmss}.csv` (tab1/tab2) hoặc `landing_page_url_...` (tab3) | Cao | `:2262-2275`, `detail.js:155-165` |
| BR-32 | LP Poster sinh **tích Descartes** giữa danh sách 「広告」 và danh sách 「LP」; mỗi cặp có một `post_code` duy nhất (`Hashids` của `botId+landingId+posterId+lpId`) để phân biệt nguồn truy cập | Cao | `Services/Landing/Poster/PosterSettingService.php:47-91` |
| BR-33 | URL đo lường LP Poster = URL của LP + query `uland={landing.code}&postcode={post_code}` (ghi đè nếu đã tồn tại) | Cao | `PosterSettingService.php:148-165` |
| BR-34 | Xoá một 「広告」hoặc một 「LP」khỏi danh sách ⇒ **xoá cứng** bản ghi đó và mọi `landing_page_poster_url` liên quan | Cao | `PosterSettingService.php:194-204` |
| BR-35 | LP Poster và tuỳ chọn thiết kế QR **không khả dụng** cho bot gói free (`plan_type = 2`) | Cao | `:3518`, `:3824`, `:3849`, `:3896`, `:3921` |
| BR-36 | Tham số ngoài: đúng **5 slot** `cid1`…`cid5`, mỗi slot map tới một `friend_information_setting`. Mỗi lần lưu đều `updateOrCreate` đủ 5 bản ghi (kể cả giá trị null) | Cao | `:3749-3762` |
| BR-37 | Cài đặt liên kết ngoài (EP-26) **reset `head_content`, `body_content`, `url_connect_qrcode_outside` về null** rồi mới gán lại từ request ⇒ gửi thiếu trường = xoá dữ liệu | Cao | `:3691-3697` |
| BR-38 | Gửi thử QR (`quickSendQr`) chỉ gửi cho các tài khoản test đã cấu hình; mỗi lần gửi thành công tăng `bots.free_send_count` và số tin nhắn trong ngày | Cao | `:1160-1226` |
| BR-39 | Trang giới thiệu bạn bè định danh người giới thiệu bằng `bot_line_user.u_code`; link chia sẻ được gắn `&u_code_intro={u_code}` | Cao | `:3391-3424` |
| BR-40 | Modal hướng dẫn action được ẩn vĩnh viễn theo **từng user** qua cột `users.hide_action_intro_modal` (lưu timestamp) | Cao | `:3954-3965`, `:620` |
| BR-41 | Sắp xếp thủ công QR (`sortQRCode`) cập nhật `position` nhưng **giữ nguyên `updated_at`** để không làm xáo trộn sắp xếp theo thời gian cập nhật | Cao | `:2708-2720` |
| BR-42 | Sắp xếp thư mục lưu `position` theo thứ tự client gửi (client đã **đảo ngược** mảng trước khi gửi vì query sắp xếp `position DESC`) | Cao | `:1149-1158`, `index.js:510-515`, `Category.php:1574` |
| BR-43 | Bộ lọc `action_with_friend = 0` được diễn giải là "tất cả" (`IN (1, 2)`) chứ không phải giá trị 0 | Cao | `:918-923`, `:1071-1076` |
| BR-44 | Khi lọc theo `keyword`, bộ lọc thư mục (`category_id`) **bị bỏ qua** — tìm kiếm luôn trên toàn bộ bot | Cao | `:903-917` |
| BR-45 | `interval_action = 2` ⇒ mới lưu `time_interval_action`, ngược lại `null` | Cao | `:498`, `:665` |
| BR-46 | Thư mục đang mở được ghi nhớ trong cookie `folder_landing` (JSON theo `bot_id`), TTL 14.400 phút, path `/basic/landing` | Cao | `:126-142`, `index.js:377-383` |

---

### BR-29 — chi tiết: phân loại bạn bè 「友だちの種類」

> ⚠ **Đã sửa theo V-01** (`_internal/validation-report.md` mục 6.A). Phiên bản trước của BR-29 **gán sai 2/4 nhãn**: gọi `(action=1, is_old_friend=1)` là 「既存友だち」 và tự đặt nhãn 「表示されない」 cho `(action=2, is_old_friend=3)`. Nguyên nhân: biểu thức `total_old_friend` tại `QRCodeController.php:2058` **gộp cả hai tổ hợp** vào một chỉ số tổng, và bản phân tích trước đã tách đôi biểu thức rồi suy diễn nhãn cho từng vế.

#### 1. Ngữ nghĩa gốc của cột `detail_landing_click.is_old_friend`

Nơi ghi quyết định ngữ nghĩa — `LiffController.php:1639-1649`:

| Giá trị | Điều kiện khi ghi | Ý nghĩa | Nguồn |
|---|---|---|---|
| `0` | Giá trị lúc INSERT | Chưa từng có quan hệ với bot | `LiffController.php:1231` (`'is_old_friend' => 0`) |
| `1` | Đã có `bot_line_user` hoặc `conversation`, **không** bị block | Đã là bạn và đã hiển thị trên エルメ | `LiffController.php:1641-1643` |
| `2` | Đã có `bot_line_user`/`conversation` **và** `is_blocked == 1` | **Trạng thái trung gian** — bị ghi đè thành `1` (hoặc `3`) ngay khi xử lý unblock | `LiffController.php:1645-1647`, ghi đè tại `:1667` |
| `3` | `$isOldFriendNotExist = true` — hệ thống phải **tạo mới** `bot_line_user`/`conversation` từ LINE | Là bạn trên LINE nhưng **chưa hiện trên エルメ** | `LiffController.php:1649`; cờ đặt tại `:1329`, `:1415` |

**Lưu ý**: Spring Boot chỉ ghi `is_old_friend` = `0` hoặc `1`. Giá trị `2` và `3` **chỉ do Laravel `LiffController` ghi**.

#### 2. Bảng tổ hợp `(action, is_old_friend)` → nhãn hiển thị → dữ liệu thật

Dữ liệu thật: `db/data/detail_landing_click.sql`, **1.062 dòng** (đếm lại độc lập bằng script parse INSERT — khớp 100% với validation-report).

| `(action, is_old_friend)` | Nhãn tab 2 「友だちの種類」 | Màu | Số dòng thật | Nguồn nhãn (`file:line`) |
|---|---|---|---|---|
| `(2, 0)` | 「新規友だち」 | `#08BF5A` | **120** | `show_friend_click.blade.php:348-351`; `LandingListFriendExport.php:36` |
| `(2, 1)` | 「ブロックを解除した友だち」 | `#222222` | **267** | `show_friend_click.blade.php:352-355`; `LandingListFriendExport.php:37` |
| `(1, 1)` | **「エルメ上の友だち」** *(KHÔNG phải 「既存友だち」)* | `#FEA600` | **386** | `show_friend_click.blade.php:356-359`; `LandingListFriendExport.php:38` |
| `(2, 3)` | **「既存友だち」** *(KHÔNG phải 「表示されない」)* | `#5799DB` | **127** | `show_friend_click.blade.php:360-363`; `LandingListFriendExport.php:39` |
| `(1, 0)` | 「友だち追加なし (URL読込みのみ)」 — mở URL nhưng chưa kết bạn; blade **không** render badge nào (không khớp nhánh `v-if`/`v-else-if` nào) | — | **152** | `show_friend_click.blade.php:348-363`; mặc định bị loại khỏi tab 2 bởi `whereRaw("NOT (is_old_friend = 0 AND action = 1)")` tại `QRCodeController.php:2006` |
| `(1, 2)` | *(không hiển thị)* — trạng thái block trung gian | — | **10** | Loại khỏi mọi thống kê bởi điều kiện `is_old_friend != 2` (`QRCodeController.php:2026` trên query gốc, `:2098` trong subquery `latest_clicks`) |

**Ràng buộc quan sát được trên dữ liệu thật** (xác nhận logic ghi ở `LiffController`):
- `is_old_friend = 3` **chỉ** đi cùng `action = 2` — **127/127** dòng.
- `is_old_friend = 2` **chỉ** đi cùng `action = 1` — **10/10** dòng.
- Không có tổ hợp nào rơi ngoài 6 dòng bảng trên.

#### 3. Vì sao dễ nhầm — chỉ số tổng 「既存友だち」 gộp 2 tổ hợp

`QRCodeController.php:2058` (và biến thể `_distinct` ở `:2064`):

```sql
COUNT(CASE WHEN (action = 1 AND is_old_friend = 1)
             OR (action = 2 AND is_old_friend = 3) THEN 1 END) as total_old_friend
```

⇒ Con số 「既存友だち」 ở đầu tab 2 = `386 + 127 = 513` (chế độ đếm tất cả), **không phải** chỉ nhóm 「既存友だち」 của cột badge. Đây là chỉ số **gộp** 「エルメ上の友だち」 + 「既存友だち」. Trả về client qua key `total_old_friend` (`:2284`).

#### 4. Ánh xạ sang 4 nhóm của tab 4 「分岐詳細」 (EP-38 `collectFriend`)

`QRCodeController.php:2404-2409` (hằng số) và `:2420-2436` (điều kiện lọc):

| Hằng số | Điều kiện SQL | Tương đương nhãn tab 2 | Số dòng thật |
|---|---|---|---|
| `NOT_SHOW = 1` | `is_old_friend = 3 AND action = 2` | 「既存友だち」 | 127 |
| `UN_BLOCK = 2` | `is_old_friend = 1 AND action = 2` | 「ブロックを解除した友だち」 | 267 |
| `FRIEND = 3` | `action = 1 AND is_old_friend = 1` | 「エルメ上の友だち」 | 386 |
| `NEW_FRIEND = 4` | `action = 2 AND is_old_friend = 0` | 「新規友だち」 | 120 |

> **Cảnh báo đặt tên**: hằng số `NOT_SHOW` và nhãn tab 4 「友だち登録済みでエルメには表示されていない」 mô tả **cùng nhóm** với nhãn tab 2 「既存友だち」. Tên hằng số trong code **không** phải nhãn hiển thị của tab 2 — đây chính là nguồn gốc của nhầm lẫn cũ.

**Mức độ tin cậy: Cao** — 4 nguồn code độc lập (blade UI, export CSV, query EP-38, nơi ghi ở `LiffController`) đều thống nhất, và khớp 100% với 1.062 dòng dữ liệu thật.

---

### Ghi chú bổ sung — quan hệ `landing.link_qr_code` ↔ `new_link_qr_code` (liên quan BR-02)

> Đã bổ sung theo V-19 / mục 6.K của validation-report. **Hai giá trị này KHÔNG xung đột trên UI.**

| Ngữ cảnh | Giá trị thực tế | Nguồn |
|---|---|---|
| **Cột DB `landing.link_qr_code`** | Giá trị **lịch sử**, sinh một lần lúc tạo QR: `route('QRLanding', $liffId) . '?uLand=' . $code` — có thể lỗi thời sau khi đổi bot/domain | `QRCodeController.php:286` |
| **EP-46 `editLandingV2`** (nguồn dữ liệu tab 「QRコード表示」, SCR-QRL-18) | Tính lại runtime rồi **ghi đè CẢ HAI thuộc tính**: `new_link_qr_code = link_qr_code = {env(URL_OUTSIDE_STEP)}landing-qr/{liff_app_id}?uLand={code}` | `QRCodeController.php:626-628` |
| **EP-02 `ajaxGetListQrs`** (nguồn `itemSelected` của modal 「アクションURL（QRコード）」, SCR-QRL-03) | Chỉ gán `new_link_qr_code` bằng **cùng công thức** đó | `QRCodeController.php:947-955` |
| **EP-24 `getLandingData`** | Cũng ghi đè cả hai, nhưng ghép lại từ segment 3–4 của `link_qr_code` cũ | `QRCodeController.php:3601-3605` |

⇒ Tab 「QRコード表示」 và modal SCR-QRL-03 hiển thị **cùng một chuỗi**. Giá trị chuẩn để Admin phát hành ra ngoài là `new_link_qr_code`. Không nơi nào trong hai màn này hiển thị giá trị DB thô. **Mức độ tin cậy: Cao.**

---

## 9. Rủi ro & vấn đề phát hiện được

| # | Vấn đề | Mức độ | Nguồn |
|---|---|---|---|
| R-01 | **Mass assignment không giới hạn** ở EP-50: `array_merge($settings, $newQrs)` rồi insert thẳng — client gửi được mọi cột của `landing` (kể cả `bot_id`) | Nghiêm trọng | `:318-320` |
| R-02 | **Thiếu kiểm `bot_id`** ở 17 endpoint (bảng mục 7.2) — cho phép đọc/sửa/xoá dữ liệu của bot khác nếu biết id | Nghiêm trọng | mục 7.2 |
| R-03 | **XSS**: `data_display_off` được trả về dưới dạng HTML thô không escape ở EP-63 | Nghiêm trọng | `:1687` |
| R-04 | **EP-69 `checkFriend` public không CSRF** — có thể ép hệ thống tạo bạn bè, gửi tin nhắn, chạy action | Nghiêm trọng | `:2810`, `routes/web.php:833` |
| R-05 | **EP-64 public không rate-limit** — có thể bơm số liệu `collect_open_landings` tuỳ ý | Cao | `:2300`, `routes/web.php:4068` |
| R-06 | Nhóm route POST `/basic/create-landing*`, `/basic/landing/edit/*`, `/basic/landing/delete` **thiếu middleware `basic_access`** ⇒ Staff bị chặn ở màn hình nhưng không bị chặn ở endpoint lưu | Cao | `routes/web.php:837` |
| R-07 | `Undefined variable $landingIds` trong `ajaxDeleteCategory` khi `group_id <= 0` | Trung bình | `:1127-1147` |
| R-08 | Route EP-43 `/ajax/init-data-sort-landing` trỏ tới method `QRCodeController@initDataSort` **không tồn tại** (`grep -c "function initDataSort"` = **0**) ⇒ `BadMethodCallException` → HTTP 500 nếu bị gọi. **Nhưng chưa gây lỗi trong vận hành**: không màn hình v2 nào gọi endpoint này. Nơi gọi duy nhất là JS v1 `public/js/qr_code/qr_code.js:135-138`, chỉ được nạp bởi view legacy `resources/views/basic/qr_code/index.blade.php:817` — mà controller **chỉ render `basic.qr_code.v2.index`** (`:149`), không bao giờ render view v1 ⇒ đường gọi đã chết. Đây là **nợ kỹ thuật**, không phải bug đang xảy ra | **Thấp** *(hạ từ Trung bình)* | `routes/web.php:2881`; `QRCodeController.php:149`; `public/js/qr_code/qr_code.js:138`; `basic/qr_code/index.blade.php:817` |
| R-09 | `orderBy` không whitelist ở EP-07 và EP-39 | Trung bình | `:1322-1324`, `:2566-2568` |
| R-10 | `hashCodeLandingPagePosterUrl` nối chuỗi id không phân tách ⇒ có thể va chạm `post_code` | Trung bình | `PosterSettingService.php:81-91` |
| R-11 | `EP-28 getExternalParameters` push trùng bản ghi khi `friend_information_id < 0` | Trung bình | `:3805-3813` |
| R-12 | `HttpException` được khởi tạo với tham số string (`new HttpException('Landing not found')`) ⇒ status code sai chuẩn | Thấp | `:2306`, `:2537` |
| R-13 | EP-52 nhận `state` (= `bot_id`) từ query string mà không đối chiếu bot đang đăng nhập | Cao | `:1258-1262` |
| R-14 | **Bug im lặng — lịch giới hạn không bao giờ chạy.** BR-10: lịch lưu qua tab 「有効期間の設定」 (EP-11 `setting-limit`) **không đặt `time_qr_off_status`**, trong khi EP-25 (`qr-off`) thì có. Cột này lại **không có DEFAULT** ở schema (`landing.sql:78`) ⇒ QR chưa từng lưu qua EP-25/EP-06 sẽ giữ `time_qr_off_status = NULL`. Điều kiện poll của cron (`HandleQrOffSchedule.php:52-66`) yêu cầu `time_qr_off_status = 1` hoặc `= 3` — trong SQL `NULL = 1` cho `NULL` (không phải `TRUE`) ⇒ **bản ghi không bao giờ được nhặt, cron không báo lỗi, không có tín hiệu nào trên UI**, trong khi cột 「有効期間」 ở SCR-QRL-01 **vẫn hiển thị khoảng thời gian** như thể lịch đang hoạt động. Đây là **bug của hệ thống**, spec ghi nhận đúng hiện trạng.<br>**Giảm nhẹ trên UI v2 hiện tại**: mục 「有効期間の設定」 (SCR-QRL-13) đã bị comment khỏi panel trái ⇒ **đường đi tới EP-11 trên UI đã bị vô hiệu hoá**, rủi ro chỉ còn hiện thực nếu gọi endpoint trực tiếp hoặc mở lại menu. Đối chiếu dữ liệu thật: `use_limit_time = 1` chỉ ở **2/566** dòng, `time_qr_off_status` = `NULL` ở **565/566** | Trung bình | So sánh `:1490-1507` (EP-11) với `:3644-3652` (EP-25); `HandleQrOffSchedule.php:52-66`; `db/schema/tables/landing.sql:78`; `db/data/landing.sql` |
| R-15 | Cron `JobStatisticLanding` duyệt **toàn bộ** bảng `landing` mỗi ngày không lọc bot, `chunk(1000)` — có thể chậm khi dữ liệu lớn | Trung bình | `JobStatisticLanding.php:48-53` |
| R-16 | `collect_open_landings` chỉ được cron tổng hợp từ `date_scan >= '20250925'` (hardcode) | Thấp | `JobStatisticLanding.php:87` |
| R-17 | **`landing_connect_google.status = 4` không được khai báo ở đâu.** Hằng số model chỉ có `WAITING(0) / PROCESSING(1) / DONE(2) / ERROR(3)` nhưng dữ liệu thật có **8/20 dòng (40%) mang giá trị `4`** (`2` = 11, `4` = 8, `1` = 1 — đếm lại từ dump). Hai hệ quả nghiệp vụ: (a) cron `landing:insert_google_sheet` chỉ lấy `status = DONE(2)` ⇒ **40% bot không bao giờ được đẩy dữ liệu lên Google Sheet**; (b) BR-21 chỉ chặn huỷ liên kết khi `status ∈ {0,1,3}` ⇒ `4` **vẫn cho phép** huỷ. Kết hợp lại: sheet ngừng cập nhật mà UI **không hiện thông báo nào**. Không tìm được nơi gán `= 4` trong `src/web/sns-line/app` ⇒ nguồn ghi chưa xác định | Trung bình | `LandingConnectGoogle.php:13-18`; `db/data/landing_connect_google.sql`; `:1290-1296` (BR-21) |
| R-18 | **Lỗi so sánh trong export CSV tab 2**: `LandingListFriendExport.php:39` viết `$data->action = 2` (một dấu `=`) thay vì `==` ⇒ đây là phép **gán**, biểu thức luôn `true`. Hệ quả: mọi dòng có `is_old_friend == 3` đều bị gán nhãn 「既存友だち」 bất kể `action`, và biến `$data->action` bị ghi đè thành `2` trong bộ nhớ. Trên dữ liệu hiện tại **vô hại** vì `is_old_friend = 3` chỉ tồn tại cùng `action = 2` (127/127 dòng), nhưng là bom hẹn giờ nếu ràng buộc đó thay đổi | Thấp | `app/Exports/LandingListFriendExport.php:39` |

---

## 10. Ứng viên Shared Component

| Thành phần | Lý do | Nguồn |
|---|---|---|
| **Modal cài đặt Action** (`setting_action`, `settingActionUrlModal`) | Dùng chung với broadcast, scenario, form, conversion, popup — biến JS toàn cục `setting_action` với `type_action = "qrcode"` | `mixins/setting_detail.js:71-78` |
| **Trang trung gian open-mobile / open-external-browser** (EP-67, EP-68, EP-69) | Dùng chung cho `booking_calendar`, `product-*`, `booking_event`, `form_answer`, `calendar`, `calendar-salon` | `:2722-3389` |
| **Landing picker** (`/basic/landings/grouped-by-folder`) | Service riêng `LandingService` được thiết kế "reusable across QR filter, scenario picker, etc." (comment trong code) | `app/Http/Controllers/Basic/LandingController.php:17-20` |
| **Quản lý thư mục (Category kind)** | Cùng khuôn với thư mục của template, form, scenario, popup — chỉ khác `kind` | `Category.php`, `:1059-1158` |
| **Liên kết Google Spreadsheet** | Cùng cơ chế với Form Answer (`Basic\FormAnswerController@redirectUriGoogleSheet` — `routes/web.php:1276`) | `:1228-1307` |
| **`PlanLimitGuard`** | Dùng chung cho 19 tính năng (richmenu, form, popup, event booking…) | `Services/PlanLimitGuard.php:71-89` |
| **Preview tin nhắn / action** (`handlePreviewMessageFromAction`) | Logic dựng preview template (kể cả template `group`) lặp lại ở nhiều controller | `:1575-1641` |

---

## 11. Ghi nhận — COMMENT schema trong DB đã lỗi thời (không phải lỗi spec)

> Bổ sung theo mục **L** của `_internal/validation-report.md`. Đây **không phải sai sót của tài liệu spec** mà là các `COMMENT` trong `CREATE TABLE` của database thật đã lạc hậu so với code và dữ liệu. Ghi lại ở đây vì chúng là **nguyên nhân gốc** gây hiểu nhầm khi reverse-engineer — đặc biệt `is_old_friend`, thủ phạm trực tiếp của lỗi BR-29 (V-01).

| # | Cột | COMMENT hiện có trong schema | Giá trị thật trong dữ liệu | Code xử lý | Kết luận |
|---|---|---|---|---|---|
| L-1 | `landing.action_with_qrcode_normal` | `'0: no execute, 2: execute'` (`db/schema/tables/landing.sql:26`) | `1` = 374, `0` = 192, **`2` = 0 dòng** | `DEFAULT '1'`; `RecoverLandingCommand:54-57` so sánh `== 1` | ❌ **Comment SAI** — miền giá trị thật là `0`/`1`, không phải `0`/`2` |
| L-2 | `landing.interval_action` | `'0: no set,1: set'` (`landing.sql:32`) | `0` = 556, `1` = 6, **`2` = 4** | BR-45 (`:498`, `:665`) và Spring Boot đều xử lý `2` | ❌ **Comment thiếu giá trị `2`** |
| L-3 | `detail_landing_click.is_old_friend` | `'0:no, 1:yes'` (`db/schema/tables/detail_landing_click.sql:13`) | `0` = 272, `1` = 653, **`2` = 10**, **`3` = 127** | `LiffController.php:1639-1649` ghi cả 4 giá trị; blade/CSV/EP-38 phân biệt 4 nhóm | ❌ **Comment thiếu `2` và `3`** — **đây là nguyên nhân gốc của V-01 (BR-29 sai)** |
| L-4 | `detail_landing_click.is_action_web` | `'0: no, 1: yes'` (`detail_landing_click.sql:16`) | `0` = 867, `1` = 129, **`2` = 66** | Mọi query dùng `is_action_web IN (1,2)` (`QRCodeController.php:2060`); Spring Boot gọi `updateIsActionWebById(2, id)` | ❌ **Comment thiếu `2`** |
| L-5 | `landing.type_open_url` | `'0: url, 1: formanswer, 2: product link, 3: booking, 4: site script, 5: conversion'` (`landing.sql:23`) | `0` = 431, `NULL` = 122, `2` = 5, `4` = 2, `1` = 2, **`6` = 2**, `3` = 1, `5` = 1 | Legacy v1 | ❌ **Comment thiếu `6`** |
| L-6 | `collect_open_landings.is_scan` | `'0: chưa scan, 1: scan'` (`db/schema/tables/collect_open_landings.sql:8`) | `0` = 301, `1` = 494, **`2` = 1** | EP-16 tab 3 lọc `is_scan IN (1,2)` | ❌ **Comment thiếu `2`** |
| L-7 | `callback_event.status` | Comment chỉ ghi `0/1/2/3` | Thực tế có 15+ giá trị (`3000`, `103`, `102`, `200`…) | Nhiều nguồn ghi (Spring Boot + 3 Laravel command + service webhook ngoài repo) | ❌ **Comment thiếu nghiêm trọng** — chi tiết ở `job/job-spec.md` |

**Khuyến nghị cho team dev/DBA** (ngoài phạm vi spec): cập nhật `COMMENT` của 7 cột trên trong database thật. Mọi giá trị 「thiếu」 ở bảng trên đều đã được xác nhận bằng **dữ liệu dump thật** (đếm lại độc lập) **và** bằng code xử lý — không phải phỏng đoán.

---

## 12. Lịch sử sửa đổi

### 2026-08-24 — `spec-fixer` áp dụng phán quyết của `spec-validator`

Nguồn chỉ đạo: `features/admin/qr-landing/_internal/validation-report.md` (mục 「Phân xử mâu thuẫn A–L」 và mục 7 「Danh sách vấn đề」). Toàn bộ khẳng định dưới đây đã được **xác minh lại độc lập** bằng cách đọc trực tiếp source và đếm lại dữ liệu dump trước khi sửa.

| Mã vấn đề | Mức độ | Vị trí trong file | Thay đổi đã áp dụng | Nguồn bằng chứng |
|---|---|---|---|---|
| **V-01** (mục A) | Nghiêm trọng | BR-29 + mục mới 「BR-29 — chi tiết」 | **Viết lại hoàn toàn** phân loại 「友だちの種類」. Sửa 2 nhãn sai: `(action=1, is_old_friend=1)` từ 「既存友だち」 → **「エルメ上の友だち」**; `(action=2, is_old_friend=3)` từ 「表示されない」 (nhãn tự đặt) → **「既存友だち」**. Bổ sung bảng 6 tổ hợp `(action, is_old_friend)` kèm số dòng dữ liệu thật, ngữ nghĩa gốc 4 giá trị của cột, giải thích vì sao `total_old_friend` gộp 2 tổ hợp, và ánh xạ sang 4 nhóm EP-38 | `show_friend_click.blade.php:348-363`; `LandingListFriendExport.php:36-39`; `QRCodeController.php:2006`, `:2026`, `:2058`, `:2404-2409`, `:2420-2436`; `LiffController.php:1231`, `:1639-1649`, `:1667`; đếm lại `db/data/detail_landing_click.sql` = 1.062 dòng: `(1,0)`=152, `(1,1)`=386, `(1,2)`=10, `(2,0)`=120, `(2,1)`=267, `(2,3)`=127 |
| **V-03** (mục H) | Nghiêm trọng | Mục 6.4 | **Thay toàn bộ bảng** bằng bảng phân biệt 「Laravel TẠO / Laravel CẬP NHẬT / Spring Boot CẬP NHẬT / Đọc bởi」. Đính chính: `detail_landing_click` do **Laravel `LiffController` TẠO** (`action = 1`), Spring Boot **chỉ UPDATE**; `collect_open_landings` **chỉ Laravel ghi**; `qr_scan_from_device` do **Laravel** ghi | `LiffController.php:1207-1237` (INSERT), `:1234` (`qr_scan_from_device`), `:1325`, `:1411`, `:1649`, `:1667`; `CollectOpenLandingRepository.java` (đọc trọn vẹn — **duy nhất 1 native SELECT**); `DetailLandingClickRepository.java` (chỉ `@Modifying` UPDATE); `grep -rn "qr_scan_from_device|qrScanFromDevice" src/job/` ⇒ **0 kết quả** |
| **V-01** (mục A) | Nghiêm trọng | Mục 2.2 — bảng 「Cột nghiệp vụ quan trọng」 của `DetailLandingClick` | Sửa mô tả enum `is_old_friend` (trước ghi `3` = 「表示されない」 — **nhãn tự đặt, sai**) thành 4 ngữ nghĩa gốc kèm nơi ghi; làm rõ nhãn hiển thị phụ thuộc **cặp** `(action, is_old_friend)`; bổ sung `action` và `is_action_web` với nơi ghi; ghi chú `qr_scan_from_device` **do Laravel ghi** | `LiffController.php:1226`, `:1231`, `:1234`, `:1325`, `:1411`, `:1639-1649`, `:1667` |
| **V-03** (mục H) | Nghiêm trọng | Mục 6.2 — kết luận | Thay câu 「luồng quét QR → kết bạn nằm ở Spring Boot」 bằng **bảng 4 giai đoạn G1/G2a/G2b/G3**, nêu rõ `is_old_friend = 2` và `= 3` **chỉ do Laravel ghi** (Spring Boot chỉ ghi `0`/`1`) | như trên |
| **V-07** (mục B) | Trung bình | BR-16, mục 1.2, mục 5.x | Sửa tên bảng: `action_detail` → **`t_actions_detail`** (BR-16, kèm chú thích model `App\ActionDetail`); `messages_v2` → **`messages_v2s`** (3 chỗ). **Giữ nguyên** tên class Eloquent `Actions`, `ActionDetail`, `MessagesV2` — đúng, không phải tên bảng | `Actions.php:10` (`t_actions`); `ActionDetail.php:10` (`t_actions_detail`); `MessagesV2.php:12` (`messages_v2s`); `ls db/schema/tables/` xác nhận có `t_actions.sql`, `t_actions_detail.sql`, `messages_v2s.sql`, **không có** `actions.sql` / `action_detail.sql` / `messages_v2.sql` |
| **V-19** (mục K) | Nhẹ | BR-02 + mục ghi chú mới sau bảng BR | Sửa BR-02: bỏ mệnh đề 「Nếu bot có `domain_url_shorten` thì thay bằng domain đó」 — code ghi rõ 「không cần check domain_url_shorten: đã confirm anh Tư」. Thêm mục 「Ghi chú bổ sung — quan hệ `link_qr_code` ↔ `new_link_qr_code`」 làm rõ **hai giá trị không xung đột**: EP-46 ghi đè `link_qr_code = new_link_qr_code` trước khi render | `QRCodeController.php:625-628` (EP-46, dòng comment tại `:625`), `:947-955` (EP-02), `:3601-3605` (EP-24), `:286` (giá trị lịch sử lúc tạo) |
| **V-09** (mục F) | Trung bình | BR-09 | Bổ sung giá trị **`NULL`** vào state machine `time_qr_off_status`: schema không có DEFAULT, `saveLandingV2` không gán ⇒ mọi QR mới đều `NULL`; `NULL` là **trạng thái hợp lệ**, cron không nhặt, **không gây lỗi runtime**. Kèm số liệu thật 565/566 | `db/schema/tables/landing.sql:78`; `HandleQrOffSchedule.php:52-66`; `QRCodeController.php:294-317`; `db/data/landing.sql` |
| **V-09** (mục F) | Trung bình | R-14 | Viết lại R-14 thành **「bug im lặng」**: lịch lưu qua EP-11 không bao giờ chạy vì `time_qr_off_status` giữ `NULL`, cron không báo lỗi, UI vẫn hiển thị 「有効期間」 bình thường. Bổ sung sắc thái giảm nhẹ: màn 「有効期間の設定」 (SCR-QRL-13) đã bị comment ⇒ **đường đi tới EP-11 trên UI v2 hiện tại đã bị vô hiệu hoá**. Giữ mức **Trung bình** theo đề nghị của validator | `:1490-1507` vs `:3644-3652`; `HandleQrOffSchedule.php:52-66`; `landing.sql:78` |
| **V-24** (mục I) | Nhẹ | R-08 | Xác nhận route sống + method không tồn tại; bổ sung 「**không màn hình v2 nào gọi** ⇒ chưa gây lỗi thực tế, chỉ là nợ kỹ thuật」 và **hạ mức từ Trung bình → Thấp**. **Phát hiện thêm**: nơi gọi duy nhất là JS v1 `public/js/qr_code/qr_code.js:135-138`, nạp bởi view legacy `basic/qr_code/index.blade.php:817` — mà controller chỉ render `basic.qr_code.v2.index` ⇒ đường gọi đã chết hoàn toàn | `routes/web.php:2881`; `grep -c "function initDataSort"` = **0**; `QRCodeController.php:149`; `public/js/qr_code/qr_code.js:138`; `basic/qr_code/index.blade.php:817` |
| **Mục L** | Nhẹ | **Mục 11 (mới)** | Thêm mục ghi nhận **7 COMMENT schema lỗi thời** (`action_with_qrcode_normal`, `interval_action`, `is_old_friend`, `is_action_web`, `type_open_url`, `is_scan`, `callback_event.status`) kèm giá trị thật, code xử lý và khuyến nghị cho DBA. Ghi rõ đây **không phải lỗi spec** mà là lỗi COMMENT trong DB — và `is_old_friend` chính là nguyên nhân gốc của V-01 | `db/schema/tables/landing.sql:23, 26, 32`; `detail_landing_click.sql:13, 16`; `collect_open_landings.sql:8` |

#### Sửa bổ sung — validation-report chỉ định cho chính file này (ngoài danh sách rút gọn)

| Mã vấn đề | Mức độ | Vị trí | Thay đổi | Nguồn bằng chứng |
|---|---|---|---|---|
| **V-10** (mục G) | Trung bình | Mục 2.6, BR-21, **R-17 (mới)** | Bổ sung giá trị `landing_connect_google.status = 4` (không khai báo trong hằng số `STATUS`) và 2 hệ quả nghiệp vụ: cron A-2 bỏ qua 40% bot; BR-21 không chặn huỷ liên kết ⇒ sheet ngừng cập nhật không báo lỗi | `LandingConnectGoogle.php:13-18`; đếm lại `db/data/landing_connect_google.sql` = 20 dòng: `2`=11, `4`=8, `1`=1; `:1290-1296` |
| **V-25** | Nhẹ | **R-18 (mới)** | Ghi nhận bug `LandingListFriendExport.php:39` dùng `=` thay `==` (gán thay vì so sánh) ⇒ điều kiện luôn `true`; hiện vô hại vì `is_old_friend = 3` chỉ tồn tại cùng `action = 2` (127/127) | `app/Exports/LandingListFriendExport.php:39` |
| **V-23** | Nhẹ | Mục 「Tab 2」 (bảng chỉ số) | Bổ sung ghi chú **tên alias SQL ≠ tên key JSON response**: `total_new_friend` → `total_new_friend_tab2`; `total_unblock_friend` → `total_unblock` | `QRCodeController.php:2072-2082`, `:2283-2285` |

#### Không sửa — nêu lý do

| Nội dung validator nhắc | Lý do giữ nguyên |
|---|---|
| `friend_info_value` → `friend_information_value` (V-07) | **Chuỗi này không xuất hiện trong `logic-spec.md`** (`grep` = 0 kết quả). Lỗi nằm ở `job-spec.md` và `db-hint.md` — ngoài phạm vi file này |
| `actions` → `t_actions` (mục B) | `logic-spec.md` **không dùng `actions` như tên bảng** ở bất kỳ đâu. Các chỗ `Actions`, `ActionDetail`, `App\Actions` đều là **tên class Eloquent** — đúng, giữ nguyên theo đúng lưu ý của validator |
| V-22 (backfill mã `SCR-QRL-xx` vào logic-spec) | Phụ thuộc V-02 (`db-mapping.md` phải sửa mã SCR trước). Validator xếp là 「Ưu tiên 2 — chạy lại `/spec-db`」, làm bây giờ sẽ phải làm lại |
| V-02, V-04, V-05, V-06, V-08, V-11…V-18, V-20, V-21, V-26 | Thuộc các file khác (`db-mapping.md`, `db-hint.md`, `job-spec.md`, `ui-spec.md`, `api-spec.md`) — ngoài phạm vi nhiệm vụ 「chỉ sửa `logic-spec.md`」 |

#### Phát hiện mới trong quá trình sửa

1. **R-08 chết hoàn toàn hơn validator mô tả**: validator kết luận 「không màn v2 nào gọi」. Kiểm thêm cho thấy **có** một nơi gọi — `public/js/qr_code/qr_code.js:138` — nhưng file JS đó chỉ được nạp bởi view legacy `resources/views/basic/qr_code/index.blade.php:817`, và `QRCodeController@index` (`:149`) **chỉ render `basic.qr_code.v2.index`**. Không có route nào trả về view v1 ⇒ endpoint hỏng thực sự không thể chạm tới.
2. **Xác nhận độc lập toàn bộ số liệu `detail_landing_click`**: parse lại 1.062 dòng INSERT bằng script riêng, 6 tổ hợp `(action, is_old_friend)` khớp **chính xác 100%** với con số của validation-report — củng cố phán quyết V-01.
3. **`landing_connect_google` chỉ có 20 dòng dữ liệu** — mẫu rất nhỏ. Tỉ lệ 「40% bot bị bỏ qua」 ở R-17 tương ứng 8/20 dòng, nên hiểu là **dấu hiệu cần điều tra trên production**, không phải thống kê đại diện.
