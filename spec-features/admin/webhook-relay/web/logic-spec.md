# FA-047 — Chuyển tiếp Webhook 「Webhook転送」 — Logic Spec

> **Nguồn phân tích**
> - Web: `src/web/sns-line` @ **`release_step_20260930_v2`**, commit **`4d9d07d159`** (task #40044 + các bug #40520/#40528/#40529/#40530/#40531/#40533/#40728/#40762/#40763/#40764/#40792/#40888/#41030)
> - Job: `src/job/linect-service` @ **`release-t09-2026`**, commit **`be6ef546`** — chỉ grep nhẹ để xác định **cầu nối web → job**; logic gửi/retry thuộc `job/job-spec.md`.
> - Ngày phân tích: **2026-10-23**. Code-first, chưa quét live.
>
> Mọi đường dẫn file tương đối từ `src/web/sns-line/` trừ khi ghi rõ. Mức tin cậy mặc định **Cao**.
> Mã `BR-xx`, `QA-spec-xxx`, `D-xx`, `§x` xuất hiện trong ngoặc là **mã nội bộ team dev** trích từ comment source — giữ lại để tra cứu, KHÔNG phải mã của dự án này. Business rule của dự án đánh số ở mục 12.

---

## 0. Tóm tắt kiến trúc

```
                         ┌─────────────────────── WEB (Laravel) ───────────────────────┐
 Admin / Staff ─ UI ───► │ WebhookRelayController (EP-01…06) ─► WebhookRelayService      │
 「Webhook転送」          │      │                                 ├─ WebhookUrlValidator │
                         │      │                                 ├─ SettingRepository ──┼──► webhook_relay_setting  (R/W)
                         │      │                                 └─ ErrorRepository ────┼──◄ webhook_relay_error    (R)
                         │                                                               │
 LINE Platform ─ POST ─► │ BotController@callbackWebHook ─► storeCallbackEventRaw ───────┼──► callback_event (mysql_callback)
  /line/callback/add/{id}│                                     request = RAW body          │      status_sync = NULL (không set)
                         │                                                               │
 Thao tác tag / 友だち情報 │ ~13 điểm TagHistory::create / FriendInformationHistory::create┼──► tag_history, friend_info_history
 (web + Java)            │                                                               │      status_sync = NULL (không set)
                         └───────────────────────────────────────────────────────────────┘
                                                     │ (DB polling — KHÔNG có queue do web ghi)
                         ┌──────────────── JOB (linect-service, Java) ───────────────────┐
                         │ HandleForwardCallbackEventManager/Task  (kênh 1)              │
                         │ HandleForwardLmeEventManager/Task       (kênh 2)              │
                         │ HandleRetryWebhookRelayManager/Task     (retry)               │
                         │  đọc: setting + 3 bảng nguồn (status_sync IS NULL)            │
                         │  ghi: status_sync, webhook_relay_queue (retry), webhook_relay_error │
                         │  gửi: POST https → URL khách (kênh 2 gắn X-Lme-Signature = secret)│
                         └───────────────────────────────────────────────────────────────┘
```

**Điểm then chốt**: phía web **không gửi HTTP ra ngoài** và **không ghi hàng đợi**. Web chỉ (1) quản lý cấu hình + secret, (2) hiển thị lỗi do job ghi, (3) gián tiếp sinh dữ liệu nguồn (`callback_event`, `tag_history`, `friend_info_history`) qua các luồng nghiệp vụ sẵn có. Hàng đợi `webhook_relay_queue` từng do web INSERT nhưng **đã bị gỡ** ở #40763; nay bảng thuộc **job** (dùng làm retry queue). Mức tin cậy: **Cao** (`config/sns-line.php:1283-1289`, `app/Providers/RepositoryServiceProvider.php:559`, `database/migrations/2026_09_03_100100_create_webhook_relay_queue_table.php:10-24`, grep `webhook_relay_queue`/`WebhookRelayQueue` trong `app/` = 0 kết quả).

---

## 1. Mô hình 2 kênh

| | Kênh 1 — 「LINE公式アカウントデータ転送」 | Kênh 2 — 「L Messageデータ転送」 |
|---|---|---|
| Hằng số | `WebhookRelaySetting::CHANNEL_LINE = 1` (`app/Models/WebhookRelaySetting.php:43`) | `CHANNEL_LME = 2` (`:46`) |
| Mô tả UI | 「LINE公式アカウントが受信したイベントを、そのまま外部ツールへ転送します。」 (`public/js/admin/webhook-relay/webhook-relay.js:51`) | 「エルメ内で発生したイベントを外部ツールへ転送します。」 (`:58`) |
| Nguồn sự kiện | Webhook LINE gửi về LME → `callback_event.request` (body thô) | Sự kiện LME sinh: gắn/gỡ tag (`tag_history`), thay đổi 友だち情報 (`friend_info_history`) |
| URL đích | `webhook_relay_setting.endpoint_url` | `webhook_relay_setting.notify_endpoint_url` |
| Bật/tắt | `is_enabled` (0 「停止中」 / 1 「転送中」) | `notify_is_enabled` |
| Bộ đếm lỗi liên tiếp | `consecutive_failure_count` | `notify_consecutive_failure_count` |
| Tự tắt | `auto_disabled_at` — **không dùng Phase 1** | `notify_auto_disabled_at` — không dùng |
| Mốc 「最終更新」 | `errors_refreshed_at` | `notify_errors_refreshed_at` |
| Header xác thực | **KHÔNG** (quyết định BA — BR-02/QA-spec-028) | `X-Lme-Signature` = **chính secret plaintext** `whsec_…` (shared token, **không phải HMAC** — "Phương án A" chốt 2026-09-10: `linect-service/…/WebhookSignatureHelper.java:22-26, 79-82`; `linect-service/ai-plan_mode/task_40475_spec_job.md:205-207`) |
| Payload | Body LINE **nguyên trạng** (「加工せずそのまま」) | JSON `{"events":[…]}` LME dựng (9 field) |
| Lỗi hiển thị | `webhook_relay_error WHERE channel = 1` | `… channel = 2` |

Ánh xạ kênh → tên cột tập trung ở `WebhookRelaySetting::COLUMNS_BY_CHANNEL` (`WebhookRelaySetting.php:58-74`); `columnsFor($channel)` với kênh lạ **rơi về kênh LINE** (`:77-84`) — chỉ an toàn vì mọi đường gọi đã validate `channel ∈ {1,2}` trước.

Payload/header (`X-Lme-Signature`, `X-Lme-Delivery-Id`, `X-Lme-Timestamp`) là phần **job thực hiện**; web chỉ ghi chú hợp đồng ở `app/Models/WebhookRelaySetting.php:14-18` và `docs/api/webhook-relay-outbound-contract.md` (tài liệu này **đã lỗi thời một phần** — tự ghi chú ở `:6-24`; mục 4.1 "HMAC hex" **không được job hiện thực**). Mức tin cậy cho các dòng Payload/Header: **Cao** — đã đối chiếu code Java (`job/job-spec.md` §4.2, §5.3, §6.2).

---

## 2. Controllers

### WebhookRelayController
- **File**: `app/Http/Controllers/Admin/WebhookRelayController.php` (258 dòng)
- **Namespace**: `App\Http\Controllers\Admin`
- **Phụ thuộc**: `WebhookRelayService` (inject constructor, `:28-31`); model legacy `App\Bots`, `App\UserStaffBot` (dùng trực tiếp trong `canAccess`).
- **Hằng số**: `PERMISSION_KEY = 'webhookRelay'` (`:24`) — khoá quyền mức **màn**, không có quyền theo từng thao tác.

#### Action: index (EP-06)
- **Route**: GET `/admin/webhook-relay`
- **Luồng**: log entry → `$botId = (int) getBotId()` → rỗng hoặc `!canAccess()` ⇒ redirect `adminIndex` + lỗi 「この権限は許可されていません。」 (`:40-43`) → render view với `webhookRelayConfig` (URL 5 endpoint dựng bằng `route()`, `channels`, `docsUrl = env('WEBHOOK_RELAY_DOCS_URL','')`) (`:48-66`).
- Không còn truyền `botId` xuống client (#41030, `:62-64`).

#### Action: getConfig (EP-01)
- **Luồng**: log → `resolveBotId()` (403 JSON nếu sai) → `service->getConfig($botId)` → `{"success":true,"data":…}` (`:70-83`).

#### Action: save (EP-02)
- **Luồng**: Form Request `WebhookRelaySaveRequest` validate kiểu (chạy **trước** thân hàm) → log entry kèm `channel`, `endpoint_url`, `is_enabled` (`:91-95`) → `resolveBotId()` → `service->save($botId, (int) channel, ['endpoint_url','is_enabled'])` → `success=false` ⇒ **422**, ngược lại 200 (`:97-111`).

#### Action: regenerateSecret (EP-03)
- **Luồng**: log → `resolveBotId()` → `service->regenerateSecret()` → fail ⇒ 422 (`:115-130`).

#### Action: getErrors (EP-04)
- **Luồng**: log (`channel`, `refresh`) → `resolveBotId()` → `filter_var(channel, FILTER_VALIDATE_INT)` + `in_array([1,2], true)`; sai ⇒ 422 `INVALID_PARAM` (`:152-163`, bug #40533) → `refresh = FILTER_VALIDATE_BOOLEAN` (`:168`) → `service->getErrors($botId, $channel, $refresh)`.

#### Action: getSecret (EP-05)
- **Luồng**: log (không log giá trị) → `resolveBotId()` → `service->getPlainSecret()` → fail ⇒ 422; thành công gắn `Cache-Control: no-store` (`:180-195`).

#### Private: logEntry / resolveBotId / canAccess
- `logEntry()` (`:201-209`): `logInfo('[entity=WebhookRelaySetting] WebhookRelayController@{fn}', {user_id, bot_id, function, params})` — **params của EP-02 chứa `endpoint_url` nguyên văn** (xem SEC-05).
- `resolveBotId()` (`:214-232`): trả `int` khi hợp lệ, ngược lại log `permission denied` + JSON 403 `PERMISSION_DENIED`.
- `canAccess(int $botId)` (`:242-257`): xem mục 9.

### WebhookRelayDebugController
- **File**: `app/Http/Controllers/Api/WebhookRelayDebugController.php` (85 dòng)
- **Action decode($secret)** (EP-07, `:39-84`):
  1. Guard `APP_DEBUG` — **bị comment** (`:49-51`) ⇒ không có chốt chặn nào.
  2. `strpos($secret, 'whsec_') !== 0` ⇒ 400 `INVALID_SECRET_FORMAT` (`:56-62`).
  3. `service->findSettingByPlainSecret($secret)`: `chunkWithSecret(500)` duyệt **mọi** dòng `signing_secret` khác rỗng theo `id`, `Crypt::decrypt` từng dòng (lỗi giải mã ⇒ bỏ qua, không log), so `hash_equals`; khớp ⇒ dừng (`WebhookRelayService.php:390-422`).
  4. Không thấy ⇒ 404 `SECRET_NOT_FOUND`; thấy ⇒ 200 `{bot_id, plain_secret, signing_secret (ciphertext), secret_generated_at}`.

---

## 3. Services

### WebhookRelayService
- **File**: `app/Services/WebhookRelay/WebhookRelayService.php` (576 dòng)
- **Phụ thuộc**: `WebhookRelaySettingRepositoryInterface`, `WebhookRelayErrorRepositoryInterface`, `WebhookUrlValidator` (`:58-66`); facade `Crypt`, `DB`; `Carbon`.
- **Hằng số**: `ERROR_MESSAGES` (`:34-43`), `SECRET_ALPHABET` base62 (`:46`), `SECRET_RANDOM_LENGTH = 32` (`:49`), `LAST_UPDATED_FORMAT = 'Y/m/d H:i'` (`:52`).

#### Method: getConfig(int $botId): array — EP-01 (`:83-108`)
1. `ensureSecret($botId)` — bảo đảm bot có secret (có thể INSERT/UPDATE).
2. `touchLastUpdatedAt($botId, [1, 2])` — UPDATE 2 cột mốc = now (mọi lần mở màn).
3. Trả `channels[1] = {is_enabled, endpoint_url}`, `channels[2] = {is_enabled, endpoint_url, secret_masked}`, `has_secret`, `last_updated_at`.
- **Không** trả `error_count` (badge tab đã bỏ — BR-08 nội bộ vô hiệu, `:76`).
- **Side effects**: tối đa 1 INSERT/UPDATE (secret) + 1 UPDATE (mốc) + 1–2 dòng log mỗi lần mở màn.

#### Method: save(int $botId, int $channel, array $input): array — EP-02 (`:118-211`)
1. `$columns = columnsFor($channel)`; `endpointUrl = trim(...)`; `isEnabled = !empty(is_enabled)` (`:120-122`).
2. `urlValidator->validate($endpointUrl, $isEnabled)` → có mã lỗi ⇒ `['success'=>false,'errors'=>[buildError('endpoint_url', code)]]` (`:126-129`).
3. Closure `$persist` chạy trong `DB::transaction` (`:138-173`):
   - `lockByBot($botId)` = `SELECT … WHERE bot_id=? FOR UPDATE` (gap lock nhờ unique `uk_webhook_relay_setting_bot`).
   - `$attributes` **chỉ** gồm `{url-col: url|null, enabled-col: 0|1}` của kênh được gửi (`:142-145`).
   - Kênh chuyển **TẮT → BẬT** (hoặc dòng chưa tồn tại mà bật) ⇒ thêm `failure-col = 0`, `disabled-col = NULL` (`:149-152`).
   - `$before = auditSnapshot($setting)` (chỉ 4 cột URL/enabled).
   - Dòng chưa có ⇒ sinh secret `generateSecret()`, `signing_secret = Crypt::encrypt(plain)`, `secret_generated_at = now()` rồi `createForBot` (`:157-165`); có rồi ⇒ `updateForBot` + `findByBot` (`:167-169`).
4. `QueryException` mã 1062 (trùng unique — READ COMMITTED không có gap lock) ⇒ **chạy lại transaction 1 lần**; lỗi khác ⇒ ném lên (`:172-183`).
5. Audit log `[action=update][entity=WebhookRelaySetting][bot_id=…] webhook relay setting saved` với `user_id, bot_id, channel, ip, before, after` (`:186-193`) — **không có secret**, nhưng **có URL**.
6. Trả `data = {channel, is_enabled, endpoint_url, has_secret, secret_masked}` (`:199-210`).
- Comment `:195-197`: trước đây xoá cache của `WebhookRelayEnqueueService` — đã gỡ (#40763).

#### Method: regenerateSecret(int $botId): array — EP-03 (`:217-251`)
1. `findByBot` — không có dòng ⇒ `INVALID_PARAM` (field `secret`).
2. `generateSecret()` → `updateForBot(['signing_secret' => Crypt::encrypt(plain), 'secret_generated_at' => now])` — **không transaction, không khoá**.
3. Audit `[action=regenerate-secret]` (`user_id, bot_id, ip, regenerated_at`).
4. Trả `{secret_masked, secret_plain: null, regenerated_at (ISO-8601)}`.

#### Method: getErrors(int $botId, int $channel, bool $refresh): array — EP-04 (`:263-280`)
1. `errorRepository->getLatestForBotChannel($botId, $channel, 100)`.
2. `$refresh` ⇒ `touchLastUpdatedAt($botId, [$channel])[$channel]`; ngược lại `readLastUpdatedAt()`.
3. Trả `{channel, items: WebhookRelayErrorResource::collection(...)->resolve(), last_updated_at}`.

#### Method (private): touchLastUpdatedAt(int $botId, array $channels): array (`:293-339`)
- Ghi cột mốc của từng kênh = `Carbon::now()` (giờ **server**, không nhận từ client). Có dòng ⇒ UPDATE; chưa có ⇒ INSERT dòng chỉ chứa mốc, đụng 1062 thì UPDATE (`:310-326`). **Không khoá** (giá trị "lần xem gần nhất", ai thắng cũng đúng — `:306-309`). Log `[action=update]` kèm before/after. Trả `[kênh => 'Y/m/d H:i']`.

#### Method (private): readLastUpdatedAt(int $botId, int $channel): string (`:342-350`)
- Trả mốc đã format hoặc `''`.

#### Method: getPlainSecret(int $botId): array — EP-05 (`:357-374`)
- Không có dòng/secret ⇒ `INVALID_PARAM`. Có ⇒ log `[action=view-secret]` (user_id, bot_id, ip) rồi trả `decryptSecret()` (có thể `null` — BUG-01).

#### Method: findSettingByPlainSecret(string $plain) — EP-07 (`:390-422`)
- "TEST-ONLY" theo comment; quét toàn bảng. **Không bao giờ gọi trong luồng nghiệp vụ** (grep: caller duy nhất là `WebhookRelayDebugController.php:64`).

#### Method (private): ensureSecret(int $botId) (`:435-494`)
- Đã có secret ⇒ trả luôn (đường đọc thuần).
- Chưa có ⇒ transaction + `lockByBot`; nếu request song song vừa tạo xong ⇒ dùng lại, **không sinh đè** (`:452-454`); ngược lại INSERT (dòng mới chỉ có `signing_secret`, `secret_generated_at`; URL/switch giữ default TẮT) hoặc UPDATE dòng đã có mà thiếu secret (`:456-468`). 1062 ⇒ chạy lại 1 lần (`:471-482`). Tạo mới ⇒ audit `[action=init-secret]` (`:484-491`).
- Comment `:427-430`: chấp nhận GET có ghi vì idempotent; **lệch QA-spec-003** (spec cũ: secret sinh ở lần lưu đầu) — "cần BA xác nhận lại".

#### Method: maskSecret($plain) (`:499-511`)
- `null` nếu rỗng; ≤ 6 ký tự trả nguyên; còn lại 6 ký tự đầu + `str_repeat('•', len-6)`.

#### Method (private): generateSecret(): string (`:517-527`)
- `whsec_` + 32 ký tự lấy bằng `random_int(0, 61)` trên bảng `0-9a-zA-Z` (CSPRNG) ⇒ luôn 38 ký tự, ~190 bit entropy.

#### Method (private): decryptSecret($setting) (`:532-547`)
- `Crypt::decrypt` (Laravel 5.5: AES-256-CBC + MAC + `unserialize`); exception ⇒ `logError('cannot decrypt signing secret', {message})` + trả `null` — không làm sập màn.

#### Method (private): isDuplicateEntry / auditSnapshot / buildError (`:550-575`)
- `isDuplicateEntry`: `errorInfo[1] === 1062`.
- `auditSnapshot`: `{endpoint_url, is_enabled, notify_endpoint_url, notify_is_enabled}` — **không bao giờ gồm secret**.
- `buildError(field, code)`: `{field, error_code, message}`; code lạ ⇒ message `INTERNAL_ERROR`.

### WebhookUrlValidator
- **File**: `app/Services/WebhookRelay/WebhookUrlValidator.php` (166 dòng; #44660 thêm ~48 dòng cho luật webhook LME — số dòng dưới đây theo bản **trước** fix, chưa reverse-engineer lại). Dùng **chung** cho 2 kênh.
- `validate($url, bool $required)` (`:35-71` bản cũ) — **10 luật** (thêm luật 8 chặn webhook LME #44660, BR-11b), thứ tự và mã lỗi ở `api-spec.md` EP-02.
- `isLmeWebhookUrl()` (#44660, nhánh `ai_studio_fixbug_44660`): chuẩn hoá path (decode `%xx`, `\` / `%5C` → `/`, gộp `//`, rút gọn `.` / `..` không vượt gốc) rồi so khớp đoạn `/line/callback/add` — chặn vòng lặp LME→LME. Bản đầu `3ddf9d4c` sót `.` / `..` (#44843), vá ở `4d8510dcf8`, giữ ở HEAD `676e01b687`.
- `isDestinationAllowed()` (`:76-116`): `parse_url` → cổng (mặc định 443) phải = 443 → host bỏ `[]` → IP literal hoặc tên miền RFC 1123 → `resolveHost()` rỗng ⇒ **từ chối** (fail-closed, bug #40728, chốt 2026-09-09) → mọi IP phải `isPublicIp()`.
- `resolveHost()` (`:124-152`): IP literal trả chính nó; ngược lại `@dns_get_record($host, DNS_A + DNS_AAAA)`, rỗng thì `@gethostbyname`. **Đồng bộ, không timeout riêng** (BUG-08).
- `isPublicIp()` (`:158-165`): `FILTER_VALIDATE_IP` + `FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE`.
- Comment `:21-22, :120-122`: chặn lúc lưu **chưa đủ** (DNS rebinding) — job Java **bắt buộc** kiểm lại lúc gửi.

---

## 4. Form Requests & Resources

### WebhookRelaySaveRequest
- **File**: `app/Http/Requests/WebhookRelaySaveRequest.php` — **Dùng cho**: EP-02
- `authorize()` luôn `true` (`:24-28`) — quyền do controller kiểm.

| Field | Rules | Mô tả |
|-------|-------|-------|
| `channel` | `required\|integer\|in:1,2` | Kênh của tab đang mở |
| `endpoint_url` | `nullable\|string` | Luật nghiệp vụ ở `WebhookUrlValidator` |
| `is_enabled` | `required\|boolean` | Switch 「転送の状態」 |

- `failedValidation()` (`:42-52`) ném `HttpResponseException` 422 với shape `errors[{field:"request", error_code:"INVALID_PARAM", message:"エラーが発生しました。"}]` — không lộ chi tiết rule.
- Không có field `bot_id` (`:20`).

### WebhookRelayErrorResource
- **File**: `app/Http/Resources/WebhookRelayErrorResource.php` — **Dùng cho**: EP-04
- `id`, `occurred_at` (`Y/m/d H:i:s` hoặc `''`), `event_type` (string), `reason` (`WebhookRelayError::reasonText(error_code)`), `http_status` (string hoặc `null`) (`:17-31`). **Không** trả `error_code`, `queue_id`, `channel` ra client.

---

## 5. Models & Repositories

### WebhookRelaySetting
- **File**: `app/Models/WebhookRelaySetting.php` — **Bảng**: `webhook_relay_setting` (kết nối mặc định `mysql`)
- `$fillable` (`:24-40`): `bot_id, endpoint_url, is_enabled, consecutive_failure_count, auto_disabled_at, notify_endpoint_url, notify_is_enabled, notify_consecutive_failure_count, notify_auto_disabled_at, signing_secret, secret_generated_at, errors_refreshed_at, notify_errors_refreshed_at`.
- Hằng số: `CHANNEL_LINE=1`, `CHANNEL_LME=2`, `SECRET_PREFIX='whsec_'`, `SECRET_MASK_VISIBLE_LENGTH=6`, `URL_MAX_LENGTH=1024`, `COLUMNS_BY_CHANNEL` (`:43-74`).
- Không khai báo relationship, scope, mutator/accessor, `$hidden` hay `$casts` (`signing_secret` không bị ẩn khi `toArray()` — hiện không có chỗ nào serialize model ra client).

### WebhookRelayError
- **File**: `app/Models/WebhookRelayError.php` — **Bảng**: `webhook_relay_error`; `$timestamps = false` (`:15`).
- `$fillable`: `bot_id, channel, queue_id, occurred_at, event_type, error_code, http_status, created_at` (`:17-26`) — web **không bao giờ ghi** (comment `:9`: "Do job Spring Boot ghi; Laravel chỉ đọc").
- `DISPLAY_LIMIT = 100` (`:29`); `ERROR_MESSAGES` 7 mã (`:41-49`); `reasonText()` mã lạ ⇒ `OTHER` (`:55-62`).

### (Không có model `WebhookRelayQueue` phía web)
Model/repo/service enqueue đã xoá ở #40763 (commit `9d19573332`); binding repo bị gỡ (`RepositoryServiceProvider.php:559`).

### WebhookRelaySettingRepository (+ Interface)
- **Files**: `app/Repositories/Eloquents/WebhookRelaySettingRepository.php`, `app/Contracts/Repositories/WebhookRelaySettingRepositoryInterface.php`; binding `RepositoryServiceProvider.php:555-556`.

| Method | SQL tương đương | Dòng |
|---|---|---|
| `findByBot($botId)` | `SELECT * … WHERE bot_id=? LIMIT 1` | `:17-20` |
| `lockByBot($botId)` | `… WHERE bot_id=? LIMIT 1 FOR UPDATE` (chỉ gọi trong transaction) | `:28-31` |
| `createForBot($botId, $attrs)` | `INSERT` (gán `bot_id`) | `:33-38` |
| `updateForBot($botId, $attrs)` | `UPDATE … SET …, updated_at=now() WHERE bot_id=?` — ownership nằm trong WHERE | `:43-48` |
| `getChannelConfigForBot($botId, $channel)` | `SELECT {enabled}, {url} … WHERE bot_id=?` — **code chết** (không caller; phục vụ hot-path enqueue đã gỡ) | `:55-66` |
| `chunkWithSecret($size, $cb)` | `SELECT id, bot_id, signing_secret, secret_generated_at WHERE signing_secret IS NOT NULL AND signing_secret<>'' ORDER BY id` theo lô — **không lọc bot_id**, chỉ dùng cho EP-07 | `:75-82` |

### WebhookRelayErrorRepository (+ Interface)
- `getLatestForBotChannel($botId, $channel, $limit)`: `SELECT id, occurred_at, event_type, error_code, http_status WHERE bot_id=? AND channel=? ORDER BY occurred_at DESC, id DESC LIMIT ?` — khớp index `idx_webhook_relay_error_list (bot_id, channel, occurred_at)` (`WebhookRelayErrorRepository.php:21-29`).

---

## 6. Console Command

### AddAccessFeatureWebhookRelay — `php artisan access-feature:webhook-relay`
- **File**: `app/Console/Commands/AddAccessFeatureWebhookRelay.php` (168 dòng). Chạy **tay một lần** khi deploy (không lên lịch). Idempotent. **Không transaction**.
- Ghi bảng `access_feature`:
  1. Row cha `{name:'Webhook転送', url:'/admin/webhook-relay', parent:0, route:'webhookRelay', visible:1, menu_id, order}` — `menu_id`/`order` lấy theo mục 「LINE公式アカウント入れ替え」 (order + 1), không có thì `menu_id = 10` (nhóm 「システム設定」) và order cuối nhóm (`:79-104`).
  2. Bug #40528: nếu khe `order` bị chiếm ⇒ `increment('order')` mọi mục cùng nhóm có order ≥ khe (`:112-136`).
  3. 5 row con (route `webhookRelay.config|save|regenerateSecret|errors|secret`, `menu_id = NULL`, `visible = 0`, `parent = id cha`) (`:58-64, 138-161`) — **bắt buộc** để Staff `is_bot_invite` qua được whitelist của `AdminAccess`.
- **Không** tạo `bot_role_access` ⇒ mặc định chỉ owner (và Staff `is_admin=1`) dùng được; Admin tự tick quyền cho role Staff.

---

## 7. Migrations & schema (bảng mới, chưa có trong DB dump)

| Migration | Nội dung | Ghi chú |
|---|---|---|
| `2026_09_03_100000_create_webhook_relay_setting_table.php` | Tạo `webhook_relay_setting`: `id` PK, `bot_id` int, 2×(URL varchar 1024 null, enabled tinyint default 0, failure int default 0, auto_disabled datetime null), `signing_secret` varchar 1024 null, `secret_generated_at`, `errors_refreshed_at`, `notify_errors_refreshed_at`, timestamps; **UNIQUE `uk_webhook_relay_setting_bot (bot_id)`** (`:24-55`) | 1 dòng/bot. Không FK |
| `2026_09_03_100100_create_webhook_relay_queue_table.php` | Tạo `webhook_relay_queue`: `id` bigint, `bot_id`, `channel` tinyint, `callback_event_id` bigint unsigned null, `delivery_id` char(36), `event_type`, `payload` longtext null, `status` tinyint default 0, `attempt_count`, `next_attempt_at`, `locked_by`, `locked_at`, `created_at`, `processed_at`; index `idx_webhook_relay_queue_poll (status, next_attempt_at, id)`, `idx_webhook_relay_queue_bot (bot_id, created_at)` (`:40-63`) | File bị xoá ở `b7e27354f2` rồi **khôi phục 2026-09-16** (commit `35520634dc`) vì job cần bảng. **Web không ghi** (`:23-24`) |
| `2026_09_03_100200_create_webhook_relay_error_table.php` | Tạo `webhook_relay_error`: `id` bigint, `bot_id`, `channel` tinyint default 1, `queue_id` bigint unsigned null (= **id bản ghi nguồn**), `occurred_at`, `event_type`, `error_code` varchar 64, `http_status` smallint null, `created_at`; index `idx_webhook_relay_error_list (bot_id, channel, occurred_at)` (`:20-39`) | Job ghi, web đọc |
| `2026_09_09_000000_fix_queue_id_comment_on_webhook_relay_error.php` | Sửa COMMENT cột `queue_id` (bug #40762) bằng raw `ALTER … MODIFY` | `queue_id` = `callback_event.id` (kênh 1) / `tag_history.id` hoặc `friend_info_history.id` (kênh 2) |
| `2026_09_10_000000_add_status_sync_to_history_tables.php` | Thêm `status_sync TINYINT NULL` + index `idx_status_sync (status_sync, id)` vào **`tag_history`, `friend_info_history`** — `ALTER … ALGORITHM=INPLACE, LOCK=NONE` (`:32-61, 87-98`) | Cột cờ cho job kênh 2. Thay thế migration cũ `2026_09_05_000000_add_status_callback_to_history_tables` (đã xoá khỏi nhánh) |
| `2026_09_16_000000_add_errors_refreshed_at_to_webhook_relay_setting.php` | Thêm `errors_refreshed_at` (guard `hasColumn`) | #41030 |
| `2026_09_16_000100_widen_callback_event_id_on_webhook_relay_queue.php` | `callback_event_id` INT → BIGINT UNSIGNED | |
| `2026_09_16_000200_add_notify_errors_refreshed_at_to_webhook_relay_setting.php` | Thêm `notify_errors_refreshed_at` | #41030 tách theo kênh |

⚠ **Không có migration nào (cả web lẫn job) thêm `callback_event.status_sync` + index `(status_sync, id)`**, dù job kênh 1 quét `WHERE status_sync IS NULL` (`linect-service/…/CallbackEventRepository.java:43-48`). Comment Java trỏ tới `data/task_40475/migration_40475.sql` — file này **không tồn tại** trong repo job (`git ls-files` không thấy). Xem GAP-01.

---

## 8. Cầu nối Web → Job (queue bridge)

> Mô hình: **Database Polling trên bảng nguồn** (chốt ở #40475): job quét thẳng cột cờ `status_sync` trên 3 bảng nguồn, **không** qua bảng trung gian do web ghi. `webhook_relay_queue` hiện là **retry queue của job**.

### 8.1 Bảng ghi / đọc qua ranh giới

| Bảng | Kênh | Web ghi gì (điểm vào) | Cột trạng thái | Web có set cột trạng thái? | Job đọc (grep nhẹ) | Job ghi |
|---|---|---|---|---|---|---|
| `webhook_relay_setting` | 1, 2 | EP-01/02/03/04: URL, enabled, `signing_secret` (ciphertext Laravel Crypt), mốc 最終更新 | `is_enabled`, `notify_is_enabled` | Có | `WebhookRelaySettingManager` đọc URL/enabled + giải mã secret bằng `APP_KEY` | (theo hợp đồng) `consecutive_failure_count`, `notify_consecutive_failure_count` |
| `callback_event` (kết nối `mysql_callback`, `app/CallbackEvent.php:10-11`) | 1 | `BotController@storeCallbackEventRaw` (`app/Http/Controllers/Admin/BotController.php:2113-2148`): **1 bản ghi / 1 lần LINE gọi**, `request` = **body thô** (#40888), `type`/`line_id`/`webhook_event_id` lấy theo event đầu tiên khác `delivery` | `status_sync` (NULL = chưa forward); `status` (cột cũ cho xử lý postback) | **Không** (INSERT không có `status_sync`) | `findNotForwardYet`: `WHERE status_sync IS NULL AND status NOT IN (:notReady) ORDER BY id ASC LIMIT :limit` | `status_sync` (1 RUNNING, 2 DONE, 3 ERROR, 4 IGNORE, 5 RETRY — `linect-service/…/values/Constants.java:133-158`) |
| `tag_history` | 2 | 12 lời gọi `TagHistory::create` trong 6 file (vd `app/Helpers/functions.php:4254,4296`; `app/Services/HelperService.php:304,1062`; `app/Http/Controllers/Api/TagController.php:131,178,367,397`; `app/Http/Controllers/ChatController.php:4844,4905`; `app/Http/Controllers/Basic/ChatController.php:1130`; `app/Services/ConversationService.php:717`) + job cũng ghi | `status_sync` | **Không** (grep `status_sync` trong `app/` = 0 kết quả ngoài `status_sync_sheet/deleted`) | `SELECT * FROM tag_history WHERE status_sync IS NULL ORDER BY id ASC LIMIT :limit` | `status_sync` |
| `friend_info_history` | 2 | `FriendDetailFriendInfoRepository.php:373` (`FriendInformationHistory::create`) + helper `functions.php:12490` + job | `status_sync` | **Không** (`$fillable` không có cột này — `app/Models/FriendInformationHistory.php:93-107`) | tương tự `tag_history` | `status_sync` |
| `webhook_relay_queue` | 1, 2 | **KHÔNG** | `status` (0 chờ …) | — | `HandleRetryWebhookRelayManager/Task` | `HandleForwardCallbackEventTask.java:155-165` (`save`), `HandleForwardLmeEventTask.java:177` (`saveAll`) khi gửi lần đầu thất bại |
| `webhook_relay_error` | 1, 2 | **KHÔNG** (EP-04 chỉ đọc) | — | — | — | INSERT sau khi hết retry (1 sự cố = 1 dòng) |

Mức tin cậy: phía web **Cao**; cột/giá trị phía job **Cao** — đã được `job/job-spec.md` §2 xác nhận bằng code Java.

### 8.2 Kênh 1 — điểm vào webhook LINE (`Admin\BotController@callbackWebHook`)
- Route `POST /line/callback/add/{bot_id}` (`routes/web.php:2554`, name `callback-web-hook`), miễn CSRF (`VerifyCsrfToken.php:15`).
- Luồng (`BotController.php:2028-2073`):
  1. `$bot_id = route('bot_id')`; `empty($bot_id)` ⇒ trả 200 `{"status":"Ok"}` và **bỏ qua events** (`:2036-2039`) — `empty("0") === true` (đã ghi nhận ở FA-044); không ảnh hưởng relay vì không có bot id 0.
  2. Bot không tồn tại ⇒ 200 `{"success":false,"message":"Not have bot"}`.
  3. `bot_type == 0`: tính `$signature = base64(hmac_sha256(body, channel_secret))` **rồi tự validate chính nó** (`:2047-2054`) ⇒ **luôn đúng** — header `X-Line-Signature` **không bao giờ được đọc** (SEC-02). Có events ⇒ `storeCallbackEventRaw`; events rỗng (verify) ⇒ `bots.is_verify = 1`.
  4. `bot_type == 1`: không kiểm chữ ký; có events ⇒ `storeCallbackEventRaw` (`:2066-2072`).
- `storeCallbackEventRaw` (`:2113-2148`):
  - Chọn event đầu tiên khác `delivery`; **toàn `delivery` ⇒ không lưu** ⇒ không bao giờ được chuyển tiếp (`:2117-2127`).
  - Body > 65535 byte ⇒ chỉ `logError` (không nội dung), MySQL (strict=false) **cắt cụt** cột `request` TEXT ⇒ kênh 1 sẽ chuyển tiếp JSON hỏng (`:2129-2138`).
  - Lưu `{user_id: admin_id, bot_id, line_id, type, webhook_event_id, request: rawBody}` (`:2140-2147`).
- **Thay đổi so với spec FA-030/FA-044**: trên nhánh này web đã **lưu nguyên body** (không còn chỉ `$body[0]`, `$body[1]`) và **đã ghi `webhook_event_id`** (commit `c89b0a960c`, `bfdc2d8cf5` — #40888). Spec FA-030 cần cập nhật khi rà lại.
- Web **không đọc** `webhook_relay_setting` ở hot-path này: mọi webhook đều lưu `callback_event` như trước; việc lọc bot có bật relay hay không do job làm (đánh `status_sync = 4 IGNORE`).

### 8.3 Kênh 2 — sự kiện LME
- Web không có emitter riêng (đã xoá `WebhookNotifyEmitter`, helper `emitWebhookNotifyTags` — `docs/api/webhook-relay-outbound-contract.md:12-14`). Job đọc trực tiếp `tag_history` / `friend_info_history`.
- Hệ quả: **mọi** đường ghi 2 bảng này (cả web lẫn job — ví dụ hành động từ API công khai `TRIGGER_API = 15002`) đều trở thành nguồn kênh 2; ngược lại thay đổi tag/友だち情報 nào **không** ghi lịch sử thì không bao giờ được chuyển tiếp (job-analyzer cần liệt kê).

### 8.4 Rủi ro ở cầu nối (để job-analyzer xác minh)
- **R-B1 — backlog lịch sử**: cột `status_sync` thêm vào bảng sẵn có với default `NULL`; dòng mới web ghi cũng `NULL` ⇒ dòng lịch sử **không phân biệt được** với dòng mới. Job quét `ORDER BY id ASC` "để cursor tiến đều qua lịch sử, không nhảy cóc bỏ sót row cũ" (`CallbackEventRepository.java:41`) ⇒ lần chạy đầu sẽ duyệt **toàn bộ lịch sử**; nếu bot đang bật relay, sự kiện **cũ** có thể bị gửi ra ngoài. Cần kiểm job có so `created_at` với thời điểm bật kênh hay không. Mức tin cậy: **Trung bình**.
- **R-B2 — GAP-01** (thiếu migration `callback_event.status_sync`).
- **R-B3**: web và job dùng chung `APP_KEY` để giải mã secret — đổi `APP_KEY` phía web ⇒ job không giải được, web chỉ log và coi như chưa có secret (`WebhookRelayService.php:532-547`).

---

## 9. Authorization

| Quyền | Kiểm tra ở đâu | Logic | Ảnh hưởng |
|-------|----------------|-------|----------|
| Đăng nhập portal Admin | Middleware `admin_access` (`AdminAccess.php:23`) | `Auth::check()` và `users.role ∈ {0,1,2,-1}` | Chưa đăng nhập: page → `/logout`; AJAX → 401 JSON |
| Phiên hợp lệ | `check_remember_token` | `session.remember_token == users.remember_token_reset_pass` | Lệch ⇒ logout; AJAX nhận 200 `success:false` |
| Bot đang chọn | Controller `resolveBotId()` / `index()` | `bot_id = session('current_bot_id')`; rỗng ⇒ 403 / redirect | **Chống IDOR**: client không truyền được `bot_id` (`WebhookRelayController.php:17-19, 214-216`) |
| Sở hữu / thành viên bot | `canAccess()` (`:242-257`) | Owner: `bots.id = bot AND bots.admin_id = Auth::id()`; hoặc Staff: `user_staff_bots.bot_id = bot AND user_invite_id = Auth::id() AND status = 1 (STATUS_ACCEPT)` | Không thoả ⇒ 403 `PERMISSION_DENIED` (chặn cả trường hợp session bị đặt sai bot) |
| Quyền màn `webhookRelay` | `checkBotHasPermission('webhookRelay', $botId)` (`app/Helpers/functions.php:198-227`) | Không phải Staff ⇒ `true`. Staff `is_admin = 1` ⇒ `true`. Staff thường ⇒ cần `bot_role_access(bot_id, role_id, access_id = access_feature[route='webhookRelay'].id)` | Chưa chạy command hoặc chưa tick ⇒ 403 |
| Whitelist route Staff mời (`is_bot_invite`) | `AdminAccess.php:61-73` + `getRouterBotInvite()` (`functions.php:5044`) | Tên route phải thuộc row cha/con của `access_feature` mà role được cấp | Thiếu 5 row con ⇒ 302 + **xoá `current_bot_id` khỏi session** (mất bot đang chọn ở mọi màn) |
| Không phân quyền theo thao tác | — | Quyền mức **màn** (R-003): Staff được cấp làm được mọi việc gồm 「再生成」 và xem plaintext secret | BA đã chấp nhận (QA-spec-005, comment `AddAccessFeatureWebhookRelay.php:16-17`) |
| CSRF | Nhóm `web` | POST EP-02/EP-03 bắt buộc token (không nằm trong `$except`) | GET có side effect (EP-01, EP-04 `refresh=1`) không được CSRF che — mức ảnh hưởng thấp |
| Menu sidebar | `sidebar.blade.php:209-245` (trong `@if($bot)` `:79-247`) | **Không** kiểm quyền | Staff không có quyền vẫn thấy mục 「Webhook転送」, bấm vào bị redirect |
| EP-07 | Không có | Guard `APP_DEBUG` bị comment | **Ai cũng gọi được** (SEC-01) |

---

## 10. Secret 「署名シークレット」 — vòng đời, lưu trữ, chữ ký

| Khía cạnh | Chi tiết | Nguồn |
|---|---|---|
| Định dạng | `whsec_` + 32 ký tự base62 sinh bằng `random_int` ⇒ 38 ký tự | `WebhookRelayService.php:46-49, 517-527` |
| Phạm vi | 1 secret / bot, chỉ kênh LME dùng | `WebhookRelaySetting.php:11-12` |
| Thời điểm sinh | (a) lần mở màn đầu tiên (EP-01 `ensureSecret`), (b) lần lưu đầu tiên (EP-02, kể cả kênh LINE / trạng thái TẮT) — cái nào đến trước | `:435-494`, `:157-165` |
| Lưu trữ | `Crypt::encrypt()` (AES-256-CBC + HMAC-SHA256 MAC + `serialize`) bằng `APP_KEY` → cột `signing_secret` varchar(1024) (~244 ký tự). **Không plaintext, không hash** (phải giải mã được để ký) | `:161, 229, 458`; migration `:42` |
| Hiển thị | Mask 6 ký tự đầu (= đúng tiền tố `whsec_`) | `:499-511` |
| Xem plaintext | EP-05, luôn xem được, audit mỗi lần, throttle 10/phút, `no-store` | `:357-374`; `routes/web.php:668-669` |
| Tái tạo | EP-03; secret cũ **mất hiệu lực ngay**; FE `confirm` bắt buộc; không khoá đồng thời | `:217-251`; `webhook-relay.js:454-485` |
| Header xác thực | `X-Lme-Signature` = **chính secret plaintext** `whsec_…` (không HMAC, không phụ thuộc body) + `X-Lme-Timestamp` (epoch ms lúc gửi, **không được ký** ⇒ không chống replay) — **job gắn**. Hợp đồng web (`docs/api/webhook-relay-outbound-contract.md:177-202`) ghi `hex(HMAC-SHA256(body))` nhưng đã bị "Phương án A" (chốt 2026-09-10) ghi đè | `linect-service/…/WebhookSignatureHelper.java:22-26, 79-82`; `WebhookRelayApiClient.java:41-45`; `linect-service/ai-plan_mode/task_40475_spec_job.md:205-207` (Cao) |
| Log | Không chỗ nào log giá trị secret (controller, service, audit) | `WebhookRelayController.php:197-200`; `WebhookRelayService.php:555-564` |
| Ngoại lệ | EP-07 nhận plaintext trên **URL path** ⇒ lọt vào access log web server/proxy | `routes/api.php:443` |

---

## 11. State machines

### 11.1 Dòng cấu hình `webhook_relay_setting` (theo bot)
```
[Không có dòng] ──EP-01 ensureSecret──────────────► [Có dòng, có secret, 2 kênh TẮT, URL NULL]
       │        ──EP-02 lần đầu (create+secret)───► [Có dòng, có secret, kênh được lưu theo input]
       │        ──EP-04 refresh=1 (chỉ mốc)──────► [Có dòng, KHÔNG secret] ──EP-01──► [có secret]
       └ EP-03 / EP-05 trả 422 INVALID_PARAM
```
Dòng **không bao giờ bị xoá** bởi web (không có endpoint xoá; tắt kênh chỉ đổi cờ).

### 11.2 Trạng thái từng kênh
```
 停止中 (enabled=0) ──EP-02 is_enabled=1 (URL hợp lệ bắt buộc)──► 転送中 (enabled=1)
                     (reset failure_count=0, auto_disabled_at=NULL của ĐÚNG kênh)
 転送中 ──EP-02 is_enabled=0 (URL có thể rỗng)──► 停止中   (không reset bộ đếm)
 転送中 ──EP-02 is_enabled=1 (giữ bật)──► 転送中            (không reset bộ đếm)
```
Không có chuyển trạng thái tự động phía web; Phase 1 job **không** tự tắt kênh (BR-25 nội bộ, migration setting `:18`).

### 11.3 Secret
```
 NULL ──sinh lần đầu (EP-01/EP-02)──► S1 ──EP-03──► S2 ──EP-03──► S3 …   (Sn-1 mất hiệu lực ngay)
 Sx ──đổi APP_KEY──► "hỏng" (has_secret=true, mask=null) ──EP-03──► S mới
```

### 11.4 Mốc 「最終更新」 (mỗi kênh một cột)
- EP-01 (vào màn / F5) ⇒ cả 2 cột = now. EP-04 `refresh=1` ⇒ cột của kênh đó = now. Đổi tab ⇒ chỉ đọc. Giá trị dùng chung cho mọi người trong bot (không phải "đã xem" theo user, không ẩn lỗi cũ, không ảnh hưởng danh sách lỗi hay thông báo).

### 11.5 `status_sync` trên bảng nguồn (thuộc job — tham chiếu)
`NULL (mới/chưa xử lý) → 1 RUNNING → 2 DONE | 3 ERROR | 4 IGNORE (bot không bật relay) | 5 RETRY (đang nằm webhook_relay_queue)`; khởi động lại job đưa `1 → NULL` (`Constants.java:133-158`, `CallbackEventRepository.java:50-56`). Mức tin cậy: **Cao** (job-spec §2.2, §7.3).

---

## 12. Business Rules tổng hợp

| # | Rule | Mô tả | Nơi implement |
|---|------|-------|--------------|
| BR-01 | Bot lấy từ session | `bot_id` luôn = `session('current_bot_id')`; mọi truy vấn bảng relay có `WHERE bot_id` | `WebhookRelayController.php:40, 214-216`; `WebhookRelaySaveRequest.php:20`; `WebhookRelaySettingRepository.php:17-48` |
| BR-02 | Quyền 2 tầng | Owner (`bots.admin_id`) hoặc Staff đã chấp nhận (`status=1`) **và** `checkBotHasPermission('webhookRelay')` | `WebhookRelayController.php:242-257`; `functions.php:198-227` |
| BR-03 | Quyền mức màn | Không có quyền riêng cho 「再生成」/xem secret; Staff được cấp làm được tất cả | `WebhookRelayController.php:23-24`; `AddAccessFeatureWebhookRelay.php:16-20` |
| BR-04 | 1 cấu hình / bot | UNIQUE `bot_id`; chứa cả 2 kênh | migration setting `:54`; `WebhookRelaySetting.php:7-13` |
| BR-05 | Lưu chỉ một kênh | EP-02 chỉ ghi cặp cột của `channel` gửi lên; kênh kia giữ nguyên | `WebhookRelayService.php:141-145` |
| BR-06 | URL bắt buộc khi bật | Rỗng chỉ lỗi khi `is_enabled=1`; tắt + rỗng ⇒ lưu NULL | `WebhookUrlValidator.php:39-41`; `WebhookRelayService.php:124-126, 143` |
| BR-07 | Chỉ HTTPS | Phải bắt đầu `https://` (phân biệt hoa thường) | `WebhookUrlValidator.php:43-45` |
| BR-08 | Độ dài URL | ≤ 1024 ký tự (`mb_strlen`) | `WebhookUrlValidator.php:47-49`; `WebhookRelaySetting.php:55` |
| BR-09 | URL không có khoảng trắng | Chặn `\s` và U+3000 ở bất kỳ vị trí nào | `WebhookUrlValidator.php:55-57` |
| BR-10 | Cấu trúc URL & host hợp lệ | `FILTER_VALIDATE_URL` + host là IP literal hoặc tên miền RFC 1123 | `WebhookUrlValidator.php:62-64, 89-97` |
| BR-11 | Chỉ cổng 443 | Cổng khác ⇒ `URL_NOT_ALLOWED` | `WebhookUrlValidator.php:27, 83-86` |
| BR-11b | Không được là webhook LME (#44660) | Chuẩn hoá path (decode `%xx`, `\` / `%5C` → `/`, gộp `//`, rút gọn `.` / `..`), path chứa `/line/callback/add` ⇒ `URL_NOT_ALLOWED`. Mọi domain, mọi `bot_id`, không phân biệt hoa/thường; chạy trước DNS/SSRF; chỉ chặn lúc lưu (job không kiểm lại) | `WebhookUrlValidator.php` `isLmeWebhookUrl()` (nhánh `ai_studio_fixbug_44660` @`676e01b687`, #44660 + #44843) |
| BR-12 | Chống SSRF lúc lưu (fail-closed) | Host phải phân giải ra ≥ 1 IP và **mọi** IP phải public | `WebhookUrlValidator.php:104-113, 124-165` |
| BR-13 | Cho phép trùng URL giữa 2 kênh | Không kiểm trùng | `WebhookRelayService.php:124-125` |
| BR-14 | Validate URL cả khi tắt | URL không rỗng luôn bị kiểm luật 2–9 dù kênh tắt | `WebhookUrlValidator.php:37-71` |
| BR-15 | Reset bộ đếm khi bật lại | TẮT→BẬT ⇒ `failure_count = 0`, `auto_disabled_at = NULL` của đúng kênh | `WebhookRelayService.php:147-152` |
| BR-16 | Ghi cấu hình an toàn đồng thời | Transaction + `SELECT … FOR UPDATE`; trùng khoá 1062 ⇒ chạy lại 1 lần | `WebhookRelayService.php:134-183, 446-482`; `WebhookRelaySettingRepository.php:28-31` |
| BR-17 | Định dạng secret | `whsec_` + 32 ký tự base62 CSPRNG (38 ký tự) | `WebhookRelayService.php:45-49, 517-527` |
| BR-18 | Secret sinh sớm | Sinh ở lần mở màn đầu (EP-01) hoặc lần lưu đầu (EP-02), kể cả lưu kênh LINE/trạng thái TẮT; không bao giờ sinh đè khi đã có | `WebhookRelayService.php:157-165, 435-494` |
| BR-19 | Secret mã hoá khả nghịch | `Crypt::encrypt` + `APP_KEY`; không plaintext, không hash | `WebhookRelayService.php:161, 229, 458`; `WebhookRelaySetting.php:14-18` |
| BR-20 | Secret chỉ cho kênh LME | Kênh LINE không ký, không secret; UI chỉ hiện ô secret ở tab 2 | `WebhookRelaySetting.php:11-12`; `index.blade.php:82-109` |
| BR-21 | Chỉ trả bản mask trong luồng thường | EP-01/02/03 trả mask; plaintext chỉ qua EP-05 | `WebhookRelayService.php:101-103, 206-208, 244-247` |
| BR-22 | Xem plaintext có kiểm soát | Always-viewable; audit mỗi lần; throttle 10/phút; `Cache-Control: no-store`; FE không lưu storage | `WebhookRelayService.php:357-374`; `WebhookRelayController.php:194`; `routes/web.php:668-669`; `webhook-relay.js:12-13` |
| BR-23 | Tái tạo secret | Cần dòng cấu hình đã có; secret cũ mất hiệu lực ngay phía web, không ân hạn; FE confirm bắt buộc. ⚠ Job cache cấu hình 60s ⇒ kênh 2 còn gửi secret cũ tối đa ~60s (job-spec R-06) | `WebhookRelayService.php:213-251`; `webhook-relay.js:101, 454-485` |
| BR-24 | Không log secret, có audit thay đổi | Audit `user_id, bot_id, ip, before/after` (chỉ URL + enabled) cho lưu; audit riêng cho sinh/tái tạo/xem secret | `WebhookRelayService.php:186-193, 234-239, 364-368, 486-490, 556-564` |
| BR-25 | Danh sách lỗi theo kênh, 100 dòng | `WHERE bot_id, channel ORDER BY occurred_at DESC, id DESC LIMIT 100`; không phân trang/lọc | `WebhookRelayError.php:29`; `WebhookRelayErrorRepository.php:21-29` |
| BR-26 | `channel` của EP-04 nghiêm ngặt | Chỉ số nguyên trọn vẹn 1 hoặc 2 | `WebhookRelayController.php:152-163` |
| BR-27 | Dịch mã lỗi phía server | `error_code` → chuỗi JP; mã lạ ⇒ 「その他のエラー」; FE không tự map | `WebhookRelayError.php:41-62`; `WebhookRelayErrorResource.php:26-27` |
| BR-28 | Định dạng hiển thị lỗi | `occurred_at` `Y/m/d H:i:s`; `http_status` null ⇒ 「—」 | `WebhookRelayErrorResource.php:23, 29`; `index.blade.php:162-164` |
| BR-29 | Mốc 「最終更新」 server-side, tách kênh | Đóng mốc khi vào màn (cả 2) hoặc 「最新に更新」 (kênh hiện tại); đổi tab chỉ đọc; giờ server, format `Y/m/d H:i` | `WebhookRelayService.php:52, 78-92, 255-350` |
| BR-30 | Web không gửi ra ngoài, không ghi queue | Toàn bộ gửi/retry/ghi lỗi do job | `config/sns-line.php:1283-1289`; migration queue `:23-24` |
| BR-31 | Chỉ lưu lỗi cuối cùng | Không lưu lần gửi thành công; 1 request hỏng = 1 dòng (kênh 2: 1 dòng cho cả lô). Tổng tối đa **3 lần gửi** (1 lần đầu + 2 lần thử lại cách 1 phút) và **chỉ** thử lại khi timeout / HTTP ≥ 500; lỗi không-retry (`CONNECT_FAILED`, 4xx, 3xx, `INVALID_PAYLOAD`) ghi **ngay sau lần 1** — UI 「3回とも失敗したものだけ」 và comment migration lệch | `index.blade.php:169`; migration error `:10-11`; `linect-service/…/Constants.java:221-236`, `WebhookRelayResult.java:53-61` |
| BR-32 | Không tự tắt kênh (Phase 1) | Cột `auto_disabled_*` không ghi; web chỉ reset khi bật lại | migration setting `:18, 32, 38` |
| BR-33 | Tab mặc định & cảnh báo rời tab | Vào/F5 luôn tab 1; rời tab có thay đổi chưa lưu ⇒ confirm, huỷ thì quay lại, đồng ý thì bỏ thay đổi | `webhook-relay.js:35, 204-219`; `index.blade.php:12-13` |
| BR-34 | Kênh 1 chuyển tiếp body thô | `callback_event.request` lưu nguyên body LINE (1 bản ghi / lần gọi); request toàn `delivery` hoặc events rỗng **không** được lưu ⇒ không chuyển tiếp | `BotController.php:2075-2148, 2055-2058` |

**Tổng: 34 business rules.**

---

## 13. Các bảng đọc / ghi (phía web, trong phạm vi tính năng)

| Bảng | Kết nối | Thao tác | Bởi |
|---|---|---|---|
| `webhook_relay_setting` | mysql (mặc định) | SELECT, SELECT FOR UPDATE, INSERT, UPDATE | EP-01, EP-02, EP-03, EP-04 (refresh), EP-05 (SELECT), EP-07 (SELECT toàn bảng) |
| `webhook_relay_error` | mysql | SELECT | EP-04 |
| `webhook_relay_queue` | mysql | — (chỉ migration) | — |
| `bots` | mysql | SELECT | `canAccess` |
| `user_staff_bots` | mysql | SELECT | `canAccess`, `checkBotHasPermission`, `AdminAccess`, `getRouterBotInvite` |
| `access_feature` | mysql | SELECT; INSERT/UPDATE (command) | `checkBotHasPermission`; command `access-feature:webhook-relay` |
| `bot_role_access` | mysql | SELECT | `checkBotHasPermission`, `getRouterBotInvite` |
| `user_access_bot` | mysql | INSERT (1 lần/ngày/Staff) | middleware `AdminAccess` |
| `user_selected_bot` | mysql | DELETE (khi Staff không còn hợp lệ) | `getRouterBotInvite` |
| `users` | mysql | SELECT | auth, `check_remember_token` |
| `callback_event` | **mysql_callback** | INSERT | `BotController@callbackWebHook` (nguồn kênh 1, ngoài màn) |
| `tag_history`, `friend_info_history` | mysql | INSERT | nhiều luồng nghiệp vụ (nguồn kênh 2, ngoài màn) |

---

## 14. Bug & rủi ro bảo mật

### 14.1 Bảo mật

| Mã | Mức độ | Vấn đề | Bằng chứng | Tin cậy |
|---|---|---|---|---|
| **SEC-01** | **Cao** | **Endpoint debug `GET /api/webhook-decode/{secret}` mở công khai trên nhánh release**: guard `APP_DEBUG` bị comment lại sau khi đã sửa ở bug #40764. Không auth/session. Ai biết một plaintext secret (vd chính bên nhận webhook) lấy được `bot_id` nội bộ + ciphertext + `secret_generated_at`. Mỗi request quét & giải mã **toàn bộ** secret (O(N), lô 500) ⇒ vector **DoS** (chỉ throttle 20/phút/IP). Secret nằm trên URL path ⇒ ghi vào access log. Thông điệp lỗi tiếng Việt lộ ra ngoài | `WebhookRelayDebugController.php:44-51`; `routes/api.php:440-446`; commit `3f3c7ddf95` (2026-09-10, "comment debug") có trong `release_step_20260930_v2`, `release_staging_20260910` | Cao |
| **SEC-02** | **Cao** | **Xác thực chữ ký webhook LINE vô hiệu** (có từ 2019, nay bị khuếch đại bởi relay): `callbackWebHook` tự tính chữ ký từ body rồi so với chính nó, không đọc `X-Line-Signature`; `bot_type=1` không kiểm gì. Ai biết `bot_id` có thể POST sự kiện giả ⇒ được lưu `callback_event` ⇒ kênh 1 **chuyển tiếp nguyên văn, không ký** tới hệ thống khách — bên nhận không có cách nào phân biệt thật/giả | `BotController.php:2046-2072`; `webhook-relay-outbound-contract.md:43-47` | Cao |
| **SEC-03** | **Trung bình** | **Bypass SSRF lúc lưu**: `FILTER_FLAG_NO_PRIV_RANGE \| NO_RES_RANGE` trên PHP 7.2 **chấp nhận** IPv4-mapped IPv6 (`::ffff:127.0.0.1`, `::ffff:10.0.0.1`, `::ffff:169.254.169.254`) và các dải `100.64.0.0/10`, `198.18.0.0/15`, `224.0.0.0/4` (validator bổ sung: NAT64 `64:ff9b::/96` và 6to4 `2002::/16` nhúng IPv4 nội bộ, vd `64:ff9b::7f00:1`, `2002:7f00:1::1`, cũng lọt). `https://[::ffff:127.0.0.1]/x` qua được `FILTER_VALIDATE_URL` và nhánh IP literal ⇒ **lưu thành công**. Mức khai thác phụ thuộc kiểm tra lại phía job | `WebhookUrlValidator.php:89-97, 126-128, 158-165`; đã chạy thử `filter_var` bằng PHP 7.2.0 CLI cục bộ (cùng hàm, cùng cờ) | Cao (web) / Trung bình (tác động) |
| SEC-04 | Trung bình | DNS rebinding: chỉ kiểm lúc lưu; URL đã lưu không được kiểm lại phía web. Hợp đồng yêu cầu job kiểm lại + không theo redirect — **job-spec đã xác nhận job KHÔNG kiểm và để OkHttp mặc định đi theo redirect** (R-01..R-03) | `WebhookUrlValidator.php:21-22, 120-122`; contract `:238-240` | Cao (về thiếu phía web) |
| SEC-05 | Thấp–Trung bình | URL đích ghi **nguyên văn** vào log info (`logEntry` + audit `before/after`). URL webhook của Slack/Zapier/Make… thường **chứa token**; validator còn chấp nhận userinfo `https://user:pass@host/` ⇒ credential lưu DB và log plaintext | `WebhookRelayController.php:91-95, 201-209`; `WebhookRelayService.php:186-193, 556-564` | Cao |
| SEC-06 | Thấp | GET có side effect: EP-01 (sinh secret, ghi mốc), EP-04 `refresh=1` (ghi mốc) — không được CSRF che; ảnh hưởng chỉ là đổi mốc 「最終更新」 | `WebhookRelayService.php:83-92, 271-273` | Cao |
| SEC-07 | Thấp | Plaintext secret xem lại được vô hạn (always-viewable) bởi bất kỳ ai có quyền màn (kể cả Staff) — quyết định thiết kế D-03; có audit + throttle | `WebhookRelayService.php:352-356` | Cao |
| SEC-08 | Thấp | Menu sidebar không lọc quyền ⇒ Staff thấy mục rồi bị redirect | `sidebar.blade.php:79, 209-245` | Cao |
| SEC-09 | Thấp | Form Request chạy trước kiểm quyền ⇒ người không có quyền gửi payload sai nhận 422 thay vì 403 | `WebhookRelaySaveRequest.php:24-28`; `WebhookRelayController.php:89-100` | Cao |

Điểm **đã làm tốt** (ghi nhận): IDOR được chặn 2 lớp (session + kiểm owner/staff); CSRF cho POST; secret sinh bằng CSPRNG, mã hoá tại chỗ, không bao giờ log; mask không lộ ký tự ngẫu nhiên; `no-store` cho response plaintext; transaction + row lock chống tạo trùng/sinh secret đôi; `channel` validate nghiêm (#40533); URL fail-closed khi DNS lỗi (#40728); chặn payload rác (#40529/#40530/#40531).

### 14.2 Bug chức năng / vận hành

| Mã | Mức độ | Vấn đề | Bằng chứng | Tin cậy |
|---|---|---|---|---|
| BUG-01 | Trung bình | Ciphertext không giải mã được (đổi `APP_KEY`): `has_secret = true` nhưng `secret_masked = null`; EP-05 trả **200 `{"secret": null}`** ⇒ FE gán `secretPlain = null`, nút copy chép chuỗi `"null"`/rỗng mà vẫn báo 「コピーしました」. Cách thoát: bấm 「再生成」 | `WebhookRelayService.php:86, 103, 359-373, 532-547`; `webhook-relay.js:413-415, 423-430` | Cao (server) / Trung bình (hành vi clipboard) |
| BUG-02 | Thấp | `env('WEBHOOK_RELAY_DOCS_URL')` gọi trong controller ⇒ khi `php artisan config:cache` luôn trả rỗng ⇒ nút 「使い方を見る」 không làm gì (URL tài liệu cũng chưa được cấp — TODO QA-spec-002) | `WebhookRelayController.php:61`; `webhook-relay.js:595-602` | Cao |
| BUG-03 | Trung bình | `regenerateSecret` không transaction/khoá: 2 tab bấm gần nhau ⇒ 2 secret, tab đến trước hiển thị mask của secret **đã bị thay**; khách có thể copy secret chết | `WebhookRelayService.php:217-231` | Cao |
| BUG-04 | Thấp | Tra DNS đồng bộ (`dns_get_record`, `gethostbyname`) không timeout riêng trong request lưu ⇒ DNS chậm làm EP-02 treo, có thể kích hoạt cảnh báo `NotifyChatworkRequestTimeSlow` | `WebhookUrlValidator.php:124-152` | Cao |
| BUG-05 | Thấp | `CheckRememberToken` trả 200 với `errors` là **chuỗi**; ở EP-02 `applyServerErrors()` gọi `errors.forEach` trên chuỗi ⇒ TypeError trong callback `done` ⇒ không toast, có thể kẹt `isSaving` | `CheckRememberToken.php:31-40`; `webhook-relay.js:313-317, 346-362` | Trung bình |
| BUG-06 | Thấp | Chuỗi JP tạm: `URL_TOO_LONG`/`URL_NOT_ALLOWED` chưa chốt (QA-001); 「その他のエラー」 tạm (C-04); câu confirm rời tab chưa có wording BA. (「タイムアウト（10秒）」: **đã phân xử — khớp code job** `TIMEOUT_SECONDS = 10` (`linect-service/…/Constants.java:239`); TODO C-05 "15 giây" chỉ dựa trên tài liệu lỗi thời `docs/api/webhook-relay-outbound-contract.md:231` ⇒ không cần đổi chuỗi) | `WebhookRelayError.php:35-49`; `WebhookRelayService.php:37-39`; `webhook-relay.js:102-104` | Cao |
| BUG-07 | Thấp | Body webhook > 65535 byte bị cắt cụt ở `callback_event.request` (TEXT, strict=false) ⇒ kênh 1 chuyển tiếp JSON hỏng; chỉ có `logError` | `BotController.php:2129-2138` | Cao |
| BUG-08 | Thấp | Code chết / tài liệu lỗi thời: `getChannelConfigForBot()` không caller; `docs/api/webhook-relay-outbound-contract.md` vẫn mô tả web INSERT queue + 2 cờ ENV `WEBHOOK_RELAY_ENABLED`/`WEBHOOK_RELAY_NOTIFY_ENABLED` không còn được đọc | `WebhookRelaySettingRepository.php:50-66`; contract `:6-27, 285-292`; `config/sns-line.php:1283-1289` | Cao |
| BUG-09 | Thấp | Mỗi lần mở màn đều UPDATE `webhook_relay_setting` + 1–2 dòng log (vì đóng mốc 「最終更新」) — ghi DB không cần thiết cho thao tác đọc | `WebhookRelayService.php:89-92, 293-339` | Cao |

---

## 15. Logging & audit

| Sự kiện | Prefix log | Trường | Dòng |
|---|---|---|---|
| Vào mọi action | `[entity=WebhookRelaySetting] WebhookRelayController@{fn}` | user_id, bot_id, function, params (EP-02: channel, **endpoint_url**, is_enabled; EP-04: channel, refresh) | `WebhookRelayController.php:201-209` |
| Từ chối quyền | `… webhook relay permission denied` | user_id, bot_id | `:219-222` |
| Lưu cấu hình | `[action=update][entity=WebhookRelaySetting][bot_id=…] webhook relay setting saved` | user_id, bot_id, channel, ip, before, after | `WebhookRelayService.php:186-193` |
| Sinh secret lần đầu | `[action=init-secret]…` | user_id, bot_id, ip | `:486-490` |
| Tái tạo secret | `[action=regenerate-secret]…` | user_id, bot_id, ip, regenerated_at | `:234-239` |
| Xem plaintext | `[action=view-secret]…` | user_id, bot_id, ip | `:364-368` |
| Đóng mốc 最終更新 | `[action=update]… errors_refreshed_at, …` | user_id, bot_id, channels, before, after | `:328-334` |
| Giải mã lỗi | `logError … cannot decrypt signing secret` | message exception | `:541-543` |

---

## 16. Cấu hình / ENV

| Biến / config | Dùng ở | Ghi chú |
|---|---|---|
| `APP_KEY` | `Crypt::encrypt/decrypt` secret | **Phải giống hệt** giữa web và job (job tự giải mã). Không ghi giá trị |
| `APP_DEBUG` | Thiết kế để khoá EP-07 | **Hiện không được đọc** (guard bị comment) |
| `WEBHOOK_RELAY_DOCS_URL` | `WebhookRelayController.php:61` | Link 「使い方を見る」; đọc bằng `env()` trực tiếp (BUG-02) |
| `WEBHOOK_RELAY_ENABLED`, `WEBHOOK_RELAY_NOTIFY_ENABLED` | — | **Đã bỏ** (#40763); còn sót trong `.env` thì vô hại (`config/sns-line.php:1283-1289`) |

---

## 17. Gaps / điểm cần xác minh

| # | Nội dung | Ai xử lý | Tin cậy |
|---|---|---|---|
| GAP-01 | Không có migration thêm `callback_event.status_sync` + index `(status_sync, id)` ở cả 2 repo (file `data/task_40475/migration_40475.sql` được tham chiếu nhưng không tồn tại); cột `callback_event.webhook_event_id` cũng không có migration web. DB dump hiện tại (`db/schema/tables/callback_event.sql`) chưa có 2 cột này. Cần DBA xác nhận đã chạy tay trên production | DBA / job-analyzer | Cao |
| GAP-02 | Backlog lịch sử (R-B1): **job-spec trả lời: KHÔNG** — job không có mốc bắt đầu, phụ thuộc script recover gitignored (job-spec R-17, G-03) | DBA / vận hành | Trung bình |
| GAP-03 | Job có kiểm lại SSRF lúc gửi không? — **Đã đóng: KHÔNG** (không resolve/kiểm IP, không giới hạn cổng, OkHttp để mặc định follow redirect — `linect-service/…/WebhookRelayApiClient.java:63-68, 89-138`; job-spec R-01) | Dev job | Cao |
| GAP-04 | ~~Ký trên body thô hay `timestamp + "\n" + body`~~ — **Đã đóng: không ký HMAC**; `X-Lme-Signature` = secret thô (Phương án A, `linect-service/…/WebhookSignatureHelper.java:22-26, 79-82`). Còn lại là quyết định nghiệp vụ/bảo mật: giữ shared token hay quay lại HMAC + sửa wording UI 「署名を付与」 | BA / Leader Dev | Cao |
| GAP-05 | Production đang chạy commit nào — nếu có `3f3c7ddf95` thì EP-07 đang mở | Vận hành | Cao (code) |
| GAP-06 | 3 bảng `webhook_relay_*`, `tag_history`, `friend_info_history` chưa có trong DB dump; rows `access_feature` của `webhookRelay` chưa có trong data dump ⇒ cần export lại để db-mapper đối chiếu | db-mapper | Cao |
| GAP-07 | Danh sách đầy đủ đường ghi `tag_history`/`friend_info_history` (web + job) = phạm vi thực tế của kênh 2; thay đổi 友だち情報/tag nào không ghi lịch sử sẽ không được chuyển tiếp | job-analyzer | Trung bình |
| GAP-08 | Comment `WebhookRelayService.php:427-430` ghi lệch QA-spec-003 (thời điểm sinh secret) "cần BA xác nhận lại" | BA | Cao |
