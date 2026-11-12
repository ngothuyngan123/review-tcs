# FA-046 — Liên kết API 「API連携」 — Logic Spec

> **Nguồn phân tích**
> - Web: `src/web/sns-line` @ nhánh **`release_step_20260930_v2`**, commit **`4d9d07d159`** — task #40041 (+ #40298, #40333, IMP-03)
> - Job: `src/job/linect-service` @ nhánh **`release-t09-2026`**, commit **`be6ef546`** — không có code liên quan
> - Ngày phân tích: **2026-10-23**
>
> Mức tin cậy mặc định: **Cao** (đọc trực tiếp source). Điểm suy luận ghi rõ **Trung bình**/**Thấp**.
>
> Mã nội bộ của team dev xuất hiện trong comment (`EP-S01…S05`, `SCR-01…05`, `BR-xx`, `D-xx`, `T-xx`, `QA-xxx`, "Technical Spec §x") được giữ trong cột ghi chú để đối chiếu; spec này dùng hệ ID dự án (`EP-01…06`, `SCR-API-01…05`, `BR-01…`). Mã `BR-xx` của dự án **không trùng nghĩa** với `BR-xx` nội bộ.

---

## 1. Tổng quan nghiệp vụ

Màn 「API連携」 cho phép Admin (và Staff được cấp quyền) **quản lý API key của 1 LINE bot** để hệ thống bên ngoài gọi Public API của LME. Web chỉ lo phần **quản trị key**: phát hành, xem lại, xoá, xem lịch sử. Việc **xác thực request bằng key**, **ghi nhận lần dùng cuối**, **tự vô hiệu khi hết hạn** và **chống trùng (idempotency)** thuộc một service bên ngoài **không có trong source** (mục 12).

### Vòng đời API key

```
           [EP-03 phát hành]
                  │  status=1 (有効), is_deleted=0, expires_at = hôm nay+N ngày 23:59:59 | NULL
                  ▼
        ┌──────────────────┐   expires_at < now (hiển thị tức thì, web tự suy)   ┌──────────────────┐
        │  有効 (active)    │ ─────────────────────────────────────────────────▶ │ 無効 (expired)    │
        │  status=1        │   job ngoài ApiKeyExpireTask: status=2, revoked_at, │ status=2 hoặc    │
        └──────────────────┘   log 無効 「システム（自動）」  (KHÔNG có trong src)   │ expires_at<now   │
                  │                                                              └──────────────────┘
                  │ [EP-04 xoá]                                                         │ [EP-04 xoá]
                  ▼                                                                     ▼
        ┌─────────────────────────────────────────────────────────────────────────────────────┐
        │ Đã xoá: is_deleted=1, deleted_at, deleted_by_user_id — biến mất khỏi danh sách,     │
        │ không reveal/xoá lại được (404); log vẫn hiển thị trong 「操作履歴」                  │
        └─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Controllers & Actions

### `App\Http\Controllers\Basic\ApiIntegrationController`
- **File**: `app/Http/Controllers/Basic/ApiIntegrationController.php` (279 dòng)
- **Phụ thuộc**: `ApiKeyService` (inject constructor, `:44-47`); dùng trực tiếp `UserStaffBot`, `Bots`, `Auth` trong `resolveOperatorName` (vi phạm nhẹ quy ước "DB qua repository" của dự án — không ảnh hưởng chức năng).
- Controller **mỏng**, không try/catch — lỗi nghiệp vụ ném `ApiIntegrationException` (tự render JSON).

#### Action: `index` — EP-01
- **Route**: GET `/basic/api-integration` (`apiIntegration`)
- **Luồng**: trả view `basic.api_integration.index` với `maxKeysPerBot` (config, mặc định 10) và `docsUrl` (config, mặc định rỗng) (`:52-60`).

#### Action: `getKeys` — EP-02 (EP-S01)
- **Luồng** (`:65-83`):
  1. `botId = getBotId()` (session).
  2. `keyword` = query `keyword` (string, mặc định `''`); `status` = `normalizeStatusFilter()` ⇒ `all|active|expired`.
  3. `ApiKeyService::getKeyList(botId, keyword, status)`.
  4. Trả `{"success":true,"data":{keys, total_items}}` HTTP 200.

#### Action: `issueKey` — EP-03 (EP-S02)
- **Luồng** (`:88-108`):
  1. FormRequest `IssueApiKeyRequest` validate kiểu/enum.
  2. Gọi `ApiKeyService::issue(botId, name, scope, expiry_preset, Auth::id(), resolveOperatorName(botId))`. Giá trị mặc định nếu thiếu input: `scope='full'`, `expiry_preset='30'` (không xảy ra vì FormRequest `required`).
  3. Trả HTTP **201** + `Cache-Control: no-store`.

#### Action: `deleteKey` — EP-04 (EP-S03)
- **Luồng** (`:113-129`): `ApiKeyService::deleteKey((int)$id, botId, Auth::id(), resolveOperatorName(botId))` → `{"success":true,"message":"APIキーを削除しました"}`.

#### Action: `revealKey` — EP-05 (EP-S04)
- **Luồng** (`:134-146`): `ApiKeyService::revealKey((int)$id, botId, Auth::id())` → `{"success":true,"data":{"api_key":...}}` + `Cache-Control: no-store`.

#### Action: `getLogs` — EP-06 (EP-S05)
- **Luồng** (`:151-167`): chuẩn hoá `action` (`normalizeActionFilter`), `page` (`normalizePage`), `per_page` (`normalizePerPage`) → `ApiKeyService::getOperationLogs()`.

#### Private: `resolveOperatorName($botId)` (`:192-242`)
Dựng chuỗi người thao tác **snapshot** ghi vào `api_keys.created_by_name` và `api_key_logs.operator_name`:
1. Không đăng nhập ⇒ 「システム（自動）」 (`ApiKey::OPERATOR_SYSTEM`).
2. Tìm `user_staff_bots` (`user_invite_id = Auth::id()`, `bot_id`, `status = 1`) lấy `role_id`.
3. Tên = `users.username` (trim) của user đăng nhập; rỗng ⇒ 「システム（自動）」.
4. Không có hàng staff nhưng `bots.admin_id = Auth::id()` ⇒ `role_id = 0` (chủ bot).
5. Không suy được vai trò ⇒ trả tên trần.
6. Kết quả 「<username>（<vai trò>）」 với vai trò từ `UserStaffBot::getRoleName()` (`app/UserStaffBot.php:30-37`): 0 「主管理者」, 1 「副管理人」, 2 「運用者」, khác 「サポート」. Dùng ngoặc **full-width** `（）` (`:28-29`).
7. Cắt tên để tổng độ dài ≤ 255 ký tự (giữ nguyên phần vai trò) (`:234-239`).

> Docblock `:177-178` còn mô tả "staff dùng `user_staff_bots.staff_name`" — **lỗi thời**, code thực tế (`:214-215`) dùng `users.username`.

#### Private: chuẩn hoá tham số
| Method | Dòng | Quy tắc |
|--------|------|--------|
| `normalizeStatusFilter` | `:247-250` | `active`/`expired` giữ nguyên, còn lại ⇒ `all` |
| `normalizeActionFilter` | `:255-258` | `issue`/`delete`/`revoke` giữ nguyên, còn lại ⇒ `all` |
| `normalizePage` | `:260-265` | `(int)`, ≤ 0 ⇒ 1 |
| `normalizePerPage` | `:270-278` | thuộc `per_page_options` `[10,20,30,50,100]` ⇒ giữ; khác ⇒ `list_per_page` (20) |

---

## 3. Models

### `App\Models\ApiKey`
- **File**: `app/Models/ApiKey.php` — **Bảng**: `api_keys` — `timestamps = true`
- **Fillable** (`:18-39`): `bot_id, name, key_prefix, key_last4, key_lookup_hash, key_cipher, key_cipher_iv, key_cipher_tag, key_enc_version, scope, status, expiry_preset, expires_at, last_used_at, revoked_at, created_by_user_id, created_by_name, deleted_by_user_id, deleted_at, is_deleted`
- **Casts** (`:41-47`): `bot_id, scope, status, key_enc_version, is_deleted` ⇒ integer. `expires_at`, `last_used_at` **không** cast date (xử lý bằng `strtotime`).
- **Không dùng** trait `SoftDeletes` — soft delete thủ công qua cờ `is_deleted`.
- **Relationships**: không khai báo (join thủ công trong repository).

#### Hằng số
| Hằng | Giá trị | Ý nghĩa |
|------|--------|--------|
| `SCOPE_FULL` / `SCOPE_READ` | 1 / 2 | 「全権限」 / 「読み取り専用」 (`:50-51, 62-65`) |
| `SCOPE_API_VALUES` | 1⇒`full`, 2⇒`read` | Giá trị contract API (`:57-60`) |
| `STATUS_ACTIVE` / `STATUS_EXPIRED` | 1 / 2 | 「有効」 / 「無効」 (chỉ do hết hạn) (`:54-55`) |
| `EXPIRY_PRESET_LABELS` | `1`⇒「1日」, `7`⇒「1週間」, `30`⇒「30日」, `unlimited`⇒「無期限」 | (`:67-72`) — không được dùng ở backend |
| `OPERATOR_SYSTEM` | 「システム（自動）」 | (`:75`) |

#### Methods / Accessors
| Method | Kiểu | Mô tả |
|--------|------|-------|
| `apiScopeValue()` | Helper | `scope` ⇒ `full`/`read`; giá trị lạ ⇒ `full` (`:82-87`) |
| `resolveScopeFromApiValue($v)` (static) | Helper | `read` ⇒ 2, còn lại ⇒ 1 (`:92-95`) |
| `isExpired()` | Helper | `status == 2` **hoặc** (`expires_at` không rỗng và `< time()`) (`:104-111`) |
| `displayStatus()` | Helper | `expired` / `active` (`:116-119`) |
| `maskedKey()` | Helper | `key_prefix` + 12 × 「•」 + `key_last4` (`:124-127`) |

### `App\Models\ApiKeyLog`
- **File**: `app/Models/ApiKeyLog.php` — **Bảng**: `api_key_logs` — `timestamps = false` (chỉ có `created_at`, code tự set)
- **Fillable**: `bot_id, api_key_id, action, key_name, detail, operator_user_id, operator_name, created_at`
- **Casts**: `bot_id, api_key_id, action` ⇒ integer

| Hằng | Giá trị |
|------|--------|
| `ACTION_ISSUE` / `ACTION_DELETE` / `ACTION_REVOKE` | 1 「発行」 / 2 「削除」 / 3 「無効」 (`:37-39, 62-66`) |
| `ACTION_API_VALUES` | 1⇒`issue`, 2⇒`delete`, 3⇒`revoke` (`:56-60`) |
| `DETAIL_DELETE` | 「一覧から削除しました」 (hiện hành, `:48`) |
| `DETAIL_DELETE_LEGACY` | 「検証完了のため削除しました」 (cũ, chỉ dùng cho command recover, `:54`) |

Methods: `actionFromApiValue()` (static, `:71-76`), `actionApiValue()` (`:78-83`), `actionLabel()` (`:85-90`).

### `App\Models\BotActivityLog` (bảng có sẵn, được mở rộng)
- **File**: `app/Models/BotActivityLog.php` — **Bảng**: `bot_activity_logs` — `guarded = []`
- **Bổ sung cho #40041**: `TYPE_API_KEY = 'api_key'` (`:17`), `ACTION_REVEAL_API_KEY = 'reveal'` (`:27`), tiêu đề 「APIキー表示」 (`:38`), nhãn category 「API連携」 (`:46`).
- **Relationship**: `operator()` belongsTo `App\User` (FK `operator_id`) (`:50-53`).
- `log($botId, $operatorId, $actionType, $actionName, $old, $new)` — `create()` 1 dòng (`:67-77`).

### `App\Http\Resources\BotActivityLogResource`
- Với `action_name = 'reveal'`: decode JSON `new_value` và chỉ hiện `name` của key; `oldValue = null` (`:50-57`). Dùng ở timeline 「アクティビティログ」 (tab 「操作履歴」) của màn **「接続設定」** `/admin/setting-bot/{id}` (`resources/views/admin/setting-bot/index.blade.php:2, 233, 269`; `SettingBotService::getBotHistoryLogs`, `app/Services/SettingBotService.php:14-60`) — **không** dùng ở màn API連携. (Comment source `BotActivityLog.php:37` gọi là "timeline アカウント設定" — tên không chính thức; tiêu đề màn thật là 「接続設定」.)

---

## 4. Services

### `App\Services\ApiIntegration\ApiKeyService`
- **File**: `app/Services/ApiIntegration/ApiKeyService.php` (453 dòng)
- **Phụ thuộc**: `ApiKeyRepositoryInterface`, `ApiKeyLogRepositoryInterface`, `ApiKeyCipher` (binding ở `app/Providers/RepositoryServiceProvider.php:541-549`)

#### Method: `getKeyList($botId, $keyword, $status)` (`:57-81`)
- **Output**: `['keys' => [presentKey(...)...], 'total_items' => count]`
- **Logic**: gọi `ApiKeyRepository::getAllForBot` → map từng dòng qua `presentKey()` (`:362-375`): `id, name, key_masked, scope, scope_label, status, expires_at (Y/m/d|null), last_used_at (Y/m/d H:i|null), issued_by`.
- `presentIssuer()` (`:398-419`): ưu tiên `users.username` **hiện tại** (join theo `created_by_user_id`) + vai trò **hiện tại** trong bot (`user_staff_bots.role_id` status=1, hoặc `bots.admin_id` ⇒ 0); user bị xoá/NULL ⇒ snapshot `created_by_name`; rỗng ⇒ 「システム（自動）」. (Yêu cầu đổi 2026-09-10.)

#### Method: `issue($botId, $name, $scope, $expiryPreset, $operatorUserId, $operatorName)` (`:95-208`)
- **Logic chi tiết**:
  1. `name = trim(name)`; rỗng ⇒ `nameRequired` (422); `mb_strlen > 50` ⇒ `nameTooLong` (422) (`:104-112`).
  2. `scope ∉ {full, read}` ⇒ `invalidParameter('権限の値が不正です。')`; `expiry_preset ∉ keys(config expiry_presets)` ⇒ `invalidParameter('有効期限の値が不正です。')` (`:113-118`).
  3. `DB::transaction` (`:125-182`):
     1. `lockBotRow(botId)` — `SELECT … FROM bots WHERE id = ? FOR UPDATE` ⇒ tuần tự hoá mọi lượt phát hành của cùng bot (chống 2 tab bấm đồng thời).
     2. `existsNameForBot` ⇒ `nameDuplicated` (409).
     3. `countActiveRowsForBot >= max_keys_per_bot` ⇒ `keyLimitReached` (409).
     4. Sinh plaintext (`generatePlainKey`), mã hoá (`encrypt`), tính `expires_at` (`resolveExpiresAt`).
     5. Insert `api_keys` (`:146-163`): `key_prefix='lme_live_sk_'`, `key_last4 = 4 ký tự cuối`, `key_lookup_hash`, `key_cipher/iv/tag` (base64), `key_enc_version`, `scope` (1/2), `status=1`, `expiry_preset`, `expires_at`, `created_by_user_id`, `created_by_name` (snapshot), `is_deleted=0`.
     6. Insert `api_key_logs` action=1, `key_name`, `detail = '権限：' + 「全権限|読み取り専用」 + ' ／ 有効期限：' + (Y/m/d | 「無期限」)`, `operator_user_id`, `operator_name`, `created_at = now` (`:166-176`).
  4. `logInfo` CRUD **không chứa plaintext** (chỉ name/scope/expiry/expires_at) (`:187-196`).
  5. Trả `id, api_key (plaintext), name, scope, scope_label, expires_at (Y/m/d|null)` (`:200-207`).
- **Side effects**: 1 dòng `api_keys`, 1 dòng `api_key_logs`; khoá hàng `bots` trong thời gian transaction.

#### Method: `deleteKey($id, $botId, $operatorUserId, $operatorName)` (`:220-267`)
1. `findForBot(id, botId)` (lọc `is_deleted=0`) ⇒ không có ⇒ `resourceNotFound` (404).
2. `DB::transaction`: `softDeleteForBot` (UPDATE … WHERE id, bot_id, is_deleted=0) ⇒ 0 hàng ⇒ 404 (bị xoá đồng thời, không ghi log lần 2); insert `api_key_logs` action=2, `detail = 「一覧から削除しました」` (`:236-256`).
3. `logInfo` before/after (`:260-264`).
- Không kiểm tra trạng thái ⇒ xoá được cả key 無効.

#### Method: `revealKey($id, $botId, $operatorUserId)` (`:278-308`)
1. `findForBot` ⇒ 404 nếu không có.
2. `cipher->decrypt($apiKey)` ⇒ lỗi ⇒ `decryptFailed` (503).
3. `BotActivityLog::log(botId, (int)operatorUserId, 'api_key', 'reveal', null, json{api_key_id, name})` — audit mỗi lần xem (QA-018), **không** trong transaction, **không** qua repository.
4. Trả `['api_key' => plaintext]`.
- Không chặn key 無効 / hết hạn.

#### Method: `getOperationLogs($botId, $action, $page, $perPage)` (`:319-354`)
- `action='all'` ⇒ không lọc; còn lại map sang 1/2/3 → `ApiKeyLogRepository::paginateForBot` → map `id, action, action_label, key_name, detail, operator_name, created_at (Y/m/d H:i)` + `pagination {page, limit, total_items, total_pages, has_next}` (`:425-434`).

#### Private: `resolveExpiresAt($expiryPreset)` (`:442-452`)
- `unlimited` ⇒ `NULL`; còn lại ⇒ `date('Y-m-d', strtotime('+N days')) . ' 23:59:59'` theo timezone app **Asia/Tokyo** (`config/app.php:68`). Ví dụ phát hành 2026-10-23 10:00 với 「1日」 ⇒ hết hạn **2026-10-24 23:59:59** (thực tế ~38 giờ).

### `App\Services\ApiIntegration\ApiKeyCipher`
- **File**: `app/Services/ApiIntegration/ApiKeyCipher.php` (148 dòng)

| Method | Dòng | Logic |
|--------|------|-------|
| `generatePlainKey()` | `:30-35` | `config key_prefix` (`lme_live_sk_`, 12 ký tự) + `bin2hex(random_bytes(16))` (32 hex, 128 bit entropy) ⇒ 44 ký tự. CSPRNG. |
| `lookupHash($plain)` | `:43-46` | `hash_hmac('sha256', plain, PEPPER)` ⇒ 64 hex, lưu `key_lookup_hash` (UNIQUE). Web chỉ ghi, không tra cứu. |
| `encrypt($plain)` | `:54-80` | AES-256-GCM, IV ngẫu nhiên 12 byte mỗi bản ghi, tag 16 byte, AAD rỗng; trả base64 `cipher/iv/tag` + `version = config key_enc_version`. Lỗi ⇒ `RuntimeException`. |
| `decrypt(ApiKey)` | `:89-111` | `openssl_decrypt` với **khoá hiện hành** (không chọn khoá theo `key_enc_version`). Lỗi ⇒ `logError` (id, bot_id, version — không có key) + `decryptFailed` (503). |
| `encryptionKey()` | `:116-133` | env `API_KEY_ENC_KEY` = base64 của đúng 32 byte; thiếu/sai ⇒ `RuntimeException`. |
| `pepper()` | `:138-147` | env `API_KEY_PEPPER`; thiếu ⇒ `RuntimeException`. |

---

## 5. Repositories

### `App\Repositories\Eloquents\ApiKeyRepository` (implements `ApiKeyRepositoryInterface`)
- **File**: `app/Repositories/Eloquents/ApiKeyRepository.php` — **không** extends `BaseRepositories` (khác quy ước dự án, không ảnh hưởng chức năng).

| Method | Dòng | SQL tương đương |
|--------|------|----------------|
| `getAllForBot($botId, $kw, $status)` | `:36-91` | `SELECT api_keys.*, users.username AS issuer_username, usb.role_id AS issuer_role_id, bots.admin_id AS bot_admin_id FROM api_keys LEFT JOIN users ON users.id = api_keys.created_by_user_id LEFT JOIN user_staff_bots usb ON usb.user_invite_id = api_keys.created_by_user_id AND usb.bot_id = ? AND usb.status = 1 LEFT JOIN bots ON bots.id = api_keys.bot_id WHERE api_keys.bot_id = ? AND api_keys.is_deleted = 0 [AND api_keys.name LIKE '%kw%'] [status filter] ORDER BY api_keys.id DESC` |
| — filter `active` | `:75-79` | `AND status = 1 AND (expires_at IS NULL OR expires_at >= NOW)` |
| — filter `expired` | `:80-87` | `AND (status = 2 OR (expires_at IS NOT NULL AND expires_at < NOW))` |
| `countActiveRowsForBot($botId)` | `:93-100` | `SELECT COUNT(*) FROM api_keys WHERE bot_id = ? AND is_deleted = 0` (không lọc status) |
| `existsNameForBot($botId, $name)` | `:102-111` | `EXISTS … WHERE bot_id = ? AND is_deleted = 0 AND name = ?` (so sánh theo collation, không BINARY) |
| `findForBot($id, $botId)` | `:113-120` | `WHERE id = ? AND bot_id = ? AND is_deleted = 0 LIMIT 1` |
| `create(array)` | `:122-125` | INSERT |
| `softDeleteForBot($id, $botId, $uid)` | `:127-139` | `UPDATE api_keys SET is_deleted = 1, deleted_at = NOW, deleted_by_user_id = ?, updated_at = NOW WHERE id = ? AND bot_id = ? AND is_deleted = 0` |
| `lockBotRow($botId)` | `:141-144` | `SELECT * FROM bots WHERE id = ? LIMIT 1 FOR UPDATE` |

> Nếu `user_staff_bots` có >1 hàng accept cho cùng (user, bot) thì LEFT JOIN nhân bản dòng key — **Thấp** (phụ thuộc dữ liệu).

### `App\Repositories\Eloquents\ApiKeyLogRepository`
| Method | Dòng | SQL / mục đích |
|--------|------|---------------|
| `paginateForBot($botId, $action, $page, $perPage)` | `:23-34` | `WHERE bot_id = ? [AND action = ?] ORDER BY id DESC` + `paginate` (COUNT + LIMIT/OFFSET) |
| `create(array)` | `:36-39` | INSERT |
| `countDeleteLogsByDetail($d)` / `updateDeleteLogsDetail($from, $to)` | `:41-49, 61-66` | `WHERE action = 2 AND detail = ?` — chỉ dùng cho command recover, **toàn hệ thống, không lọc bot** |

### `App\Repositories\Eloquents\BotRepository::findActiveByChannelId` — **code chết**
- `app/Repositories/Eloquents/BotRepository.php:249-261`: `WHERE channel_id = ? AND is_deleted = 0` — comment ghi dành cho middleware `api_signature_auth` (header `X-LME-Channel-Id`) nhưng **không có nơi gọi** và middleware đó không tồn tại.

---

## 6. Form Requests

### `App\Http\Requests\ApiIntegration\IssueApiKeyRequest`
- **File**: `app/Http/Requests/ApiIntegration/IssueApiKeyRequest.php` — **Dùng cho**: EP-03 — `authorize()` = `true` (phân quyền giao cho `basic_access`).

| Field | Rules | Message JP tuỳ biến |
|-------|-------|--------------------|
| `name` | `present\|string` | `name.present` 「キー名を入力してください。」 (không có message riêng cho `string`) |
| `scope` | `required\|in:full,read` | 「権限を選択してください。」 / 「権限の値が不正です。」 |
| `expiry_preset` | `required\|in:1,7,30,unlimited` | 「有効期限を選択してください。」 / 「有効期限の値が不正です。」 |

**Thứ tự kiểm tra thực tế khi phát hành**:
1. FE (`index.js:583-593`): trim rỗng → >50 ký tự (đếm theo đơn vị UTF-16 của JS).
2. Global middleware `TrimStrings` + `ConvertEmptyStringsToNull` (`app/Http/Kernel.php:24-25`).
3. FormRequest: `name` present + string (chuỗi rỗng đã thành `null` ⇒ fail tại đây), `scope`, `expiry_preset`.
4. Service: rỗng → >50 (mb_strlen) → scope → expiry → (khoá bot) → trùng tên → ngưỡng key.

> Lưu ý: PHP `trim()` (cả `TrimStrings` lẫn service) **không cắt khoảng trắng full-width 「　」(U+3000)** ⇒ gọi API trực tiếp với tên chỉ gồm 「　」 vẫn được chấp nhận; FE thì chặn được vì `String.prototype.trim()` của JS có cắt U+3000. Mức độ: Thấp.

---

## 7. Exceptions & render lỗi

### `App\Exceptions\ApiIntegration\ApiIntegrationException`
- **File**: `app/Exceptions/ApiIntegration/ApiIntegrationException.php` — có `render()` trả `{"success":false,"error_code","message"}` (`:49-56`).
- `app/Exceptions/Handler.php:124-126` gọi `render()` **trước** nhánh `app.debug` và nhánh AJAX chung ⇒ mã lỗi giữ nguyên ở production.

| Factory | `error_code` | HTTP | Message | Dòng |
|---------|-------------|------|---------|------|
| `nameRequired()` | `name_required` | 422 | 「キー名を入力してください。」 | `:60-63` |
| `nameTooLong()` | `name_too_long` | 422 | 「キー名は50文字以内で入力してください。」 | `:65-68` |
| `nameDuplicated()` | `name_duplicated` | 409 | 「同じキー名が既に存在します。別の名前を入力してください。」 | `:70-73` |
| `keyLimitReached($max)` | `key_limit_reached` | 409 | 「発行できるAPIキーは{max}件までです。不要なキーを削除してから発行してください。」 | `:75-82` |
| `invalidParameter($msg)` | `invalid_parameter` | 422 | mặc định 「パラメータが不正です。」 | `:84-87` |
| `resourceNotFound()` | `resource_not_found` | 404 | 「対象のAPIキーが見つかりません。」 | `:89-92` |
| `decryptFailed()` | `decrypt_failed` | 503 | 「APIキーを復号できませんでした。」 | `:94-97` |

### Exception khác (Handler chung)
- `TokenMismatchException` + AJAX ⇒ 401 `SESSION_EXPIRED` (`Handler.php:110-118`).
- `APP_DEBUG=true` ⇒ `parent::render` chuẩn Laravel (`:128-130`).
- `APP_DEBUG=false` + AJAX ⇒ mọi exception khác (kể cả `ValidationException`, `HttpException 429`, `RuntimeException`, `QueryException`) ⇒ `{"status":false,"error":{"code":<FlattenException status>,"message":$e->getMessage()}}` với HTTP **404 nếu HTTPS / 401 nếu không** (`:152-170`). **Trung bình** (phụ thuộc giá trị `APP_DEBUG` môi trường).

---

## 8. Cấu hình & biến môi trường

File `config/api_integration.php`:

| Key | Env | Mặc định | Dùng ở | Ghi chú |
|-----|-----|---------|--------|--------|
| `enabled` | `API_INTEGRATION_ENABLED` | `false` | **Không nơi nào** | Comment nói "tắt thì màn ẩn khỏi menu" — **chưa được thực thi**: menu sidebar (`sidebar.blade.php:189-207`) và route luôn hoạt động |
| `max_keys_per_bot` | `API_INTEGRATION_MAX_KEYS_PER_BOT` | 10 | Service, view | |
| `key_prefix` | — | `lme_live_sk_` | Cipher, Service | |
| `pepper` | `API_KEY_PEPPER` | `''` | `ApiKeyCipher::pepper` | Bắt buộc khi phát hành |
| `encryption_key` | `API_KEY_ENC_KEY` | `''` | `ApiKeyCipher::encryptionKey` | base64 của 32 byte, tách khỏi `APP_KEY` |
| `key_enc_version` | `API_KEY_ENC_VERSION` | 1 | Chỉ ghi vào DB | Decrypt không dùng ⇒ xoay khoá chưa hỗ trợ thực sự |
| `docs_url` | `API_INTEGRATION_DOCS_URL` | `''` | View | Rỗng ⇒ ẩn 「使い方を見る」 |
| `reveal_rate_limit_per_minute` | — | 30 | **Không nơi nào** | Route hardcode `throttle:30,1` |
| `list_per_page` / `per_page_options` | — | 20 / `[10,20,30,50,100]` | `normalizePerPage` (chỉ EP-06) | |
| `expiry_presets` | — | `{'1':1,'7':7,'30':30,'unlimited':null}` | Service | |

Không ghi giá trị thật của biến môi trường trong spec.

---

## 9. State machine

### `api_keys.status`
| Giá trị | Nhãn | Ai đặt | Ghi chú |
|---------|------|--------|--------|
| 1 | 「有効」 | Web khi phát hành (`ApiKeyService.php:157`) | |
| 2 | 「無効」 | **Chỉ hệ thống ngoài** (`ApiKeyExpireTask` — không có trong src) | Web không bao giờ ghi 2 |

### Trạng thái hiển thị (`displayStatus`)
`expired` ⇔ `status = 2` **OR** `expires_at < now`; ngược lại `active`. Bộ lọc SQL ở repository khớp đúng logic này (tại đúng giây `expires_at = now` cả hai đều coi là active).

### `api_keys.is_deleted`
`0 → 1` một chiều qua EP-04; không có khôi phục.

### `api_key_logs.action`
1 発行 (web, EP-03) · 2 削除 (web, EP-04) · 3 無効 (hệ thống ngoài). UNIQUE `(api_key_id, action)` ⇒ mỗi key tối đa 1 log mỗi loại.

---

## 10. Events / Queued Jobs / Commands

- **Events / Listeners / Queued Jobs**: **không có**. Toàn bộ xử lý đồng bộ trong request.
- **Schedule**: `app/Console/Kernel.php` không lên lịch command nào của tính năng (Kernel chỉ `load(__DIR__.'/Commands')` tại `:282`).
- **Artisan commands (chạy tay, 1 lần)**:

| Command | File | Tác dụng |
|---------|------|---------|
| `access-feature:api-integration` | `app/Console/Commands/AddAccessFeatureApiIntegration.php` | Insert vào `access_feature`: 1 dòng cha (`name='API連携'`, `url='/basic/api-integration'`, `route='apiIntegration'`, `parent=0`, `visible=1`) + 5 dòng con (`visible=0`, `parent=<id cha>`) cho các route AJAX. Idempotent (bỏ qua route đã có). |
| `api-integration:recover-delete-detail [--dry-run]` | `app/Console/Commands/RecoverApiKeyLogDeleteDetail.php` | Đổi `api_key_logs.detail` của log 削除 từ 「検証完了のため削除しました」 sang 「一覧から削除しました」 trên **toàn hệ thống**. Idempotent. |

- **Background job Spring Boot**: không có trong `src/job/linect-service` ⇒ **không tạo `job-spec.md`** cho tính năng này ở thời điểm hiện tại (xem mục 12).

---

## 11. Authorization

| Quyền | Kiểm tra ở đâu | Logic | Ảnh hưởng |
|-------|---------------|-------|----------|
| Đăng nhập portal | `BasicAccess.php:31, 189-191` | `Auth::check()` và `users.role ∈ {-1,0,1,2}` | Không đạt ⇒ redirect `logout` |
| Bot hiện tại | `getBotId()` từ session; `BasicAccess` | Mọi truy vấn lọc `bot_id` của session | Không có bot ⇒ redirect `adminIndex` |
| Chủ bot (Admin) | `BasicAccess.php:44-45` | `bots.admin_id = Auth::id()` ⇒ không kiểm route | Dùng được toàn bộ EP-01…06 |
| Staff (bot invite) | `BasicAccess.php:36-51` + `getRouterBotInvite()` (`app/Helpers/functions.php:5044-5130`) | Route name phải thuộc danh sách route của `access_feature` được gán cho `role_id` của staff trong `bot_role_access` (kèm route con `parent = id cha`, `menu_id IS NULL`) | Được cấp 「API連携」 ⇒ dùng **cả 6 endpoint** (xem, phát hành, xoá, hiện full key, lịch sử). Không được cấp ⇒ redirect 302 `adminIndex` 「この権限は許可されていません。」 (AJAX nhận HTML, FE báo lỗi chung). **⚠ Với code hiện tại không cấp được quyền này qua màn phân quyền ⇒ mọi Staff đều rơi vào nhánh bị chặn** (R-15) |
| Hiển thị menu | `sidebar.blade.php:14-27, 189-207` | Hiện khi có `$bot`; **không** kiểm `routeListAccess` (biến được tính ở `:14-27` nhưng không dùng cho các mục 「機能関連」) / feature flag | Staff chưa được cấp vẫn thấy menu nhưng bị chặn khi bấm — **Cao** (đọc trực tiếp Blade) |
| Hết hạn hợp đồng | `IsExpire` | Bot hết hạn ⇒ redirect `pointSettings` | |
| Đổi mật khẩu ở phiên khác | `CheckRememberToken` | Logout | |
| `IssueApiKeyRequest::authorize` | FormRequest | Luôn `true` | — |

---

## 12. Business Rules tổng hợp

| # | Rule | Mô tả | Nơi implement | Confidence |
|---|------|------|---------------|-----------|
| BR-01 | Phạm vi bot theo session | Mọi thao tác dùng `current_bot_id` trong session; không nhận `bot_id` từ client | `ApiIntegrationController.php:67,90,115,136,153`; `functions.php:389-393` | Cao |
| BR-02 | Tên key bắt buộc, ≤ 50 ký tự | Trim; rỗng ⇒ lỗi; `mb_strlen > 50` ⇒ lỗi 「キー名は50文字以内で入力してください。」 | `ApiKeyService.php:104-112`; FE `index.js:583-593`; cột `name varchar(50)` | Cao |
| BR-03 | Tên không trùng trong bot | Chỉ so với key **chưa xoá** (tên của key đã xoá được dùng lại); so sánh theo collation ⇒ không phân biệt hoa/thường | `ApiKeyRepository.php:102-111`; `ApiKeyService.php:133-135` | Cao |
| BR-04 | Tối đa 10 key/bot | Đếm **mọi** key chưa xoá, kể cả 「無効」 ⇒ phải xoá key hết hạn mới phát hành thêm; ngưỡng cấu hình qua env | `ApiKeyRepository.php:93-100`; `ApiKeyService.php:120,137-140`; `config/api_integration.php:17` | Cao |
| BR-05 | Phát hành tuần tự theo bot | Kiểm tra trùng tên + ngưỡng nằm trong transaction có `SELECT … FOR UPDATE` hàng `bots` | `ApiKeyService.php:125-140`; `ApiKeyRepository.php:141-144` | Cao |
| BR-06 | Quyền (scope) | 「全権限」 (`full`, 1) hoặc 「読み取り専用」 (`read`, 2); mặc định UI 全権限. Web chỉ lưu — việc áp quyền đọc/ghi do Public API ngoài | `ApiKey.php:50-65,92-95`; `IssueApiKeyRequest.php:26` | Cao (lưu) / Thấp (áp dụng) |
| BR-07 | Hạn dùng theo preset | 4 mức 「1日」「1週間」「30日」「無期限」 (không có date picker); mặc định 30日 | `config/api_integration.php:42-47`; `IssueApiKeyRequest.php:27` | Cao |
| BR-08 | Mốc hết hạn 23:59:59 | `expires_at = (hôm nay + N ngày) 23:59:59` giờ server (Asia/Tokyo); 無期限 ⇒ `NULL`; server tự tính, không nhận ngày từ client | `ApiKeyService.php:442-452`; `config/app.php:68` | Cao |
| BR-09 | Định dạng key | `lme_live_sk_` + 32 hex (`random_bytes(16)`) — 44 ký tự | `ApiKeyCipher.php:30-35` | Cao |
| BR-10 | Không lưu plaintext | Lưu `key_prefix`, `key_last4`, `key_lookup_hash` (HMAC-SHA256 + pepper, UNIQUE), `key_cipher` (AES-256-GCM, IV ngẫu nhiên 12B, tag 16B), `key_enc_version` | `ApiKeyService.php:146-163`; `ApiKeyCipher.php:43-80`; migration `create_api_keys_table.php:21-27,41` | Cao |
| BR-11 | Full key chỉ lộ ở 2 nơi | Response phát hành (EP-03) và reveal (EP-05), đều `Cache-Control: no-store`; danh sách chỉ trả dạng che `prefix + 12×• + last4` | `ApiIntegrationController.php:106-107,144-145`; `ApiKey.php:124-127`; `ApiKeyService.php:356-375` | Cao |
| BR-12 | Xem lại key | Cho phép với mọi key chưa xoá (kể cả 無効); mỗi lần xem ghi audit `bot_activity_logs` (`api_key`/`reveal`, JSON id+name) — hiện ở timeline 「アクティビティログ」 của màn 「接続設定」, **không** ở drawer 「操作履歴」 của FA-046 | `ApiKeyService.php:278-308`; `BotActivityLog.php:17,27,38,46` | Cao |
| BR-13 | Giới hạn tần suất reveal | 30 lần/phút (theo user — Laravel 5.5) | `routes/web.php:1026-1028` | Cao (giá trị) / Trung bình (khoá theo user) |
| BR-14 | Xoá mềm, hiệu lực ngay | `is_deleted=1`, `deleted_at`, `deleted_by_user_id`; không khôi phục; xoá được key 無効; xoá lặp ⇒ 404, không ghi log trùng | `ApiKeyRepository.php:127-139`; `ApiKeyService.php:228-256` | Cao |
| BR-15 | Log phát hành chụp cấu hình | `detail = 「権限：<scope> ／ 有効期限：<Y/m/d|無期限>」` | `ApiKeyService.php:166-176` | Cao |
| BR-16 | Log xoá | `detail = 「一覧から削除しました」` (chuỗi cũ 「検証完了のため削除しました」 được sửa bằng command) | `ApiKeyLog.php:48,54`; `ApiKeyService.php:244-255` | Cao |
| BR-17 | Log 無効 do hệ thống | action 3, `operator_name` 「システム（自動）」 — web không tạo | `ApiKeyLog.php:39`; `ApiKey.php:75`; migration logs `:11` | Trung bình |
| BR-18 | Mỗi key tối đa 1 log mỗi loại | UNIQUE `(api_key_id, action)` | migration `create_api_key_logs_table.php:30` | Cao |
| BR-19 | 「操作履歴」 | Nguồn `api_key_logs` theo bot; mới nhất trước (`id DESC`); gồm log của key đã xoá; lọc `all/issue/delete/revoke`; phân trang `per_page` ∈ {10,20,30,50,100} (mặc định 20), FE 「もっと見る」 | `ApiKeyLogRepository.php:23-34`; `ApiIntegrationController.php:151-167,255-278` | Cao |
| BR-20 | Trạng thái hiển thị | 「無効」 nếu `status=2` hoặc đã quá `expires_at` — không phụ thuộc job | `ApiKey.php:104-119`; `ApiKeyRepository.php:72-87` | Cao |
| BR-21 | Danh sách key | Không phân trang (tối đa 10); tìm `name LIKE %kw%` (escape ký tự đặc biệt); lọc trạng thái (giá trị lạ ⇒ all); mới nhất trước | `ApiKeyRepository.php:36-91`; `ApiIntegrationController.php:247-250` | Cao |
| BR-22 | 「発行者」 trên danh sách | `users.username` **hiện tại** + 「（vai trò hiện tại）」; user mất ⇒ snapshot `created_by_name`; rỗng ⇒ 「システム（自動）」 | `ApiKeyService.php:398-419` | Cao |
| BR-23 | Tên người thao tác snapshot | 「username（主管理者｜副管理人｜運用者｜サポート）」, chủ bot không có hàng staff ⇒ 主管理者; cắt tên để ≤ 255 ký tự | `ApiIntegrationController.php:192-242`; `UserStaffBot.php:30-37` | Cao |
| BR-24 | 「最終利用」 | Hiển thị `last_used_at` (Y/m/d H:i) hoặc 「未使用」 — web không cập nhật | `ApiKeyService.php:372`; `index.blade.php:225` | Cao |
| BR-25 | Nút 「使い方を見る」 | Chỉ hiện khi cấu hình `docs_url` | `ApiIntegrationController.php:58`; `index.blade.php:44` | Cao |
| BR-26 | Phân quyền theo màn | Staff cần role được cấp 「API連携」 (`access_feature.route='apiIntegration'`); cấp là được toàn bộ thao tác. **Hiện không cấp được qua màn phân quyền** (dòng cha thiếu `menu_id`) ⇒ thực tế chỉ chủ bot dùng được — R-15 | `AddAccessFeatureApiIntegration.php:32-63`; `functions.php:5044-5130`; `BasicAccess.php:36-51`; `UserController.php:3780-3783, 3881` | Cao |

---

## 13. Bảng DB đọc / ghi (cho db-mapper)

> 3 bảng mới **chưa có trong DB dump** (`db/schema/tables/`) — schema lấy từ migration.

| Bảng | Đọc | Ghi | Ở đâu | Ghi chú |
|------|-----|-----|-------|--------|
| `api_keys` | ✔ | ✔ INSERT (EP-03), UPDATE soft delete (EP-04) | `ApiKeyRepository` | Migration `2026_08_24_100001_create_api_keys_table.php`; cột `last_used_at`, `revoked_at`, `status=2` chỉ hệ thống ngoài ghi |
| `api_key_logs` | ✔ (EP-06) | ✔ INSERT action 1/2; UPDATE `detail` (command recover) | `ApiKeyLogRepository` | Migration `…_100002_…`; action 3 hệ thống ngoài ghi |
| `api_idempotency_keys` | ✘ | ✘ | — | Migration `…_100003_…` — web chỉ tạo bảng; dữ liệu thuộc Public API ngoài |
| `bot_activity_logs` | ✘ (ở màn này) | ✔ INSERT audit reveal (EP-05) | `BotActivityLog::log` | Đọc bởi timeline 「アクティビティログ」 màn 「接続設定」 |
| `bots` | ✔ (`admin_id`, khoá FOR UPDATE) | ✘ | `ApiKeyRepository::lockBotRow`, `getAllForBot` (join); `resolveOperatorName`; middleware | |
| `users` | ✔ (`username`) | ✘ | `getAllForBot` (join `created_by_user_id`), `Auth::user()` | Bảng `users` không có cột `name` |
| `user_staff_bots` | ✔ (`role_id`, `status=1`) | ✘ | `getAllForBot` (join), `resolveOperatorName`, `getRouterBotInvite` | |
| `access_feature` | ✔ (middleware) | ✔ (command `access-feature:api-integration`) | `getRouterBotInvite`, command | |
| `bot_role_access` | ✔ | ✘ | `getRouterBotInvite` | |
| `user_access_bot` | ✘ | ✔ (1 lần/ngày/user có hàng `user_staff_bots`) | `BasicAccess.php:55-75` | Side effect chung của middleware. Tên bảng **số ít** (`app/UserAccessBot.php:11`) |

### Schema tóm tắt (từ migration)
- **`api_keys`**: `id` PK; `bot_id` int; `name` varchar(50); `key_prefix` varchar(12); `key_last4` varchar(4); `key_lookup_hash` char(64) **UNIQUE** `uk_api_keys_lookup`; `key_cipher` varchar(255); `key_cipher_iv` varchar(32); `key_cipher_tag` varchar(32); `key_enc_version` tinyint=1; `scope` tinyint=1; `status` tinyint=1; `expiry_preset` varchar(16)='30'; `expires_at`, `last_used_at`, `revoked_at` datetime NULL; `created_by_user_id` int NULL; `created_by_name` varchar(255)=''; `deleted_by_user_id` int NULL; `deleted_at` datetime NULL; `is_deleted` tinyint=0; `created_at`/`updated_at`. Index: `idx_api_keys_bot_list (bot_id,is_deleted,id)`, `idx_api_keys_bot_name (bot_id,name)` (không unique vì soft delete), `idx_api_keys_expire_scan (status,expires_at)`. Không FK.
- **`api_key_logs`**: `id` PK; `bot_id` int; `api_key_id` unsigned int; `action` tinyint; `key_name` varchar(50); `detail` varchar(500)=''; `operator_user_id` int NULL (NULL = hệ thống); `operator_name` varchar(255); `created_at` timestamp DEFAULT CURRENT_TIMESTAMP. Index `idx_api_key_logs_bot (bot_id,id)`; UNIQUE `uk_api_key_logs_action (api_key_id,action)`.
- **`api_idempotency_keys`**: `id` bigint PK; `api_key_id`; `bot_id`; `idempotency_key` varchar(255); `endpoint` varchar(64); `request_hash` char(64); `status` tinyint (0 đang xử lý / 1 xong); `response_code` smallint NULL; `response_body` mediumtext NULL; timestamps. UNIQUE `uk_idem (api_key_id,idempotency_key)`; index `idx_idem_cleanup (created_at)`.
- Charset/collation kết nối: `utf8mb4` / `utf8mb4_unicode_ci`, `strict => false` (`config/database.php:50-53`).

---

## 14. Bảo mật — kết quả kiểm tra

| Hạng mục | Kết quả | Bằng chứng |
|---------|--------|-----------|
| IDOR | **Đạt** — mọi truy vấn theo `id` đều kèm `bot_id` (session) + `is_deleted=0` trong WHERE, không find-rồi-check | `ApiKeyRepository.php:113-120,127-139`; `ApiKeyLogRepository.php:25` |
| CSRF | **Đạt** — `/basic/*` không nằm trong `$except`; FE gửi `X-CSRF-TOKEN` | `VerifyCsrfToken.php:14-54`; `index.js:51` |
| Plaintext key trong log ứng dụng | **Đạt** — `logInfo`/`logError` chỉ ghi id/name/scope; middleware không log body response | `ApiKeyService.php:187-196,260-264,305`; `ApiKeyCipher.php:101-105` |
| Cache response chứa key | **Đạt** — `Cache-Control: no-store` ở EP-03, EP-05 | `ApiIntegrationController.php:106-107,144-145` |
| Sinh key | **Đạt** — CSPRNG `random_bytes`, 128 bit | `ApiKeyCipher.php:34` |
| Mã hoá | **Đạt** — AES-256-GCM, IV ngẫu nhiên mỗi bản ghi, khoá tách riêng khỏi `APP_KEY` | `ApiKeyCipher.php:54-80` |
| Race condition phát hành | **Đạt** — khoá hàng `bots` trong transaction | `ApiKeyService.php:131` |
| XSS | **Đạt** — Vue binding, không `v-html`/`{!! !!}` trong view tính năng | grep `resources/views/basic/api_integration/` |
| Rate limit reveal | **Có** (30/phút) | `routes/web.php:1028` |
| Transaction | Phát hành + log, xoá + log trong transaction; audit reveal **ngoài** transaction (chấp nhận được) | |

### Bug / rủi ro phát hiện

| # | Mức độ | Mô tả | Bằng chứng | Confidence |
|---|-------|------|-----------|-----------|
| R-01 | **Cao** (rủi ro rollout — thống nhất với ui-spec B-01; mức thực tế phụ thuộc Public API `/v1/*` đã chạy production chưa) | **Feature flag `API_INTEGRATION_ENABLED` không được thực thi**: comment nói tắt flag thì ẩn màn, nhưng không có code nào đọc `api_integration.enabled` — menu và route luôn bật kể cả khi Public API chưa sẵn sàng (người dùng phát hành key không dùng được) | `config/api_integration.php:13-14`; `sidebar.blade.php:189-207`; grep không có `api_integration.enabled` | Cao |
| R-02 | **Trung bình** (theo thiết kế) — **hiện đang tiềm ẩn** | **Không tách quyền chi tiết**: staff được cấp màn 「API連携」 có thể xem full key của **mọi** key (kể cả key do 主管理者 phát hành), phát hành, xoá. Audit reveal có ghi nhưng không chặn. Với code hiện tại staff **không cấp được** quyền này qua UI (R-15) ⇒ rủi ro chỉ thành hiện thực khi R-15 được sửa, hoặc khi có người insert tay `bot_role_access` (tồn tại tới lần lưu phân quyền kế tiếp) | `AddAccessFeatureApiIntegration.php:41-47`; `ApiKeyService.php:286-303` | Cao |
| R-03 | **Trung bình** | Ở production (`APP_DEBUG=false`), lỗi không phải `ApiIntegrationException` (FormRequest `ValidationException`, `throttle` 429, `RuntimeException` thiếu env, lỗi DB) bị Handler đổi thành HTTP **404/401** với body chung ⇒ (a) FE không nhận ra 422/429 — mọi lỗi này hiện câu fallback của màn; (b) **lộ `$e->getMessage()`** trong body JSON (`error.message`) — vd 「[#40041] Thiếu API_KEY_PEPPER — cần đặt biến môi trường…」 hoặc thông điệp SQL kèm bindings. FE **không hiển thị** `error.message` (chỉ đọc `body.message` — `index.js:782-789`) nên chỉ thấy qua DevTools/proxy. Kể cả `QueryException` khi INSERT `api_keys`, bindings chỉ chứa `key_lookup_hash`/`key_cipher*`/`key_last4` — **không có plaintext key** | `Handler.php:128-170`; `ApiKeyCipher.php:121-143`; `ApiKeyService.php:146-163` | Cao (code) / Trung bình (phụ thuộc `APP_DEBUG` môi trường) |
| R-04 | Thấp | **Xoay khoá chưa hỗ trợ**: `key_enc_version` được ghi nhưng `decrypt()` luôn dùng khoá hiện hành ⇒ đổi `API_KEY_ENC_KEY` làm mọi key cũ reveal lỗi 503 `decrypt_failed` (và Public API ngoài — nếu cần giải mã để kiểm chữ ký — cũng hỏng) | `ApiKeyCipher.php:78,89-98` | Cao |
| R-05 | Thấp | Reveal là **GET có side effect** (ghi audit); về lý có thể bị kích hoạt bằng thẻ `<img>` để tạo bản ghi audit giả — không lộ key do SOP. Khả thi thấp: cookie phiên không đặt `same_site` (`config/session.php:195` = `null`) ⇒ trình duyệt hiện đại áp mặc định Lax / chặn cookie bên thứ ba nên request cross-site không mang phiên; chỉ trang **cùng site** mới kích hoạt được | `routes/web.php:1026`; `ApiKeyService.php:295-303`; `config/session.php:195` | Trung bình (phụ thuộc trình duyệt) |
| R-06 | Thấp | Throttle Laravel 5.5 khoá theo `sha1(user id)` — **dùng chung bộ đếm** với route khác có `throttle` (vd `routes/web.php:667-669` `throttle:10,1` của webhook-relay); comment "/session" không chính xác | `routes/web.php:1025-1028` | Trung bình |
| R-07 | Thấp | Lỗi `name_required` của service **không thể chạm qua HTTP**: tên rỗng bị `ConvertEmptyStringsToNull` đổi thành `null` ⇒ FormRequest `string` fail trước, message mặc định 「nameには文字を指定してください。」 (`resources/lang/ja/validation.php:89`; không phải 「キー名を入力してください。」) — **chỉ thấy khi `APP_DEBUG=true`**; production rơi vào R-03 ⇒ alert fallback 「APIキーの発行に失敗しました」. FE chặn trước nên người dùng thường không gặp | `Kernel.php:24-25`; `IssueApiKeyRequest.php:25`; `ApiKeyService.php:107-109` | Cao |
| R-08 | Thấp | Tên chỉ gồm khoảng trắng full-width 「　」 lọt qua server (PHP `trim` không cắt U+3000) — chỉ khi gọi trực tiếp | `ApiKeyService.php:104` | Cao |
| R-09 | Thấp | Kiểm tra trùng tên theo `utf8mb4_unicode_ci` ⇒ ngoài hoa/thường, còn coi **hiragana = katakana, ハ = パ = バ, full-width = half-width** là trùng (vd 「パパ」 trùng 「ハハ」), và các emoji khác nhau cũng có thể bị coi là bằng nhau — có thể gây 409 khó hiểu cho người dùng Nhật | `ApiKeyRepository.php:104-110`; `config/database.php:51` | Trung bình (phụ thuộc collation thật của bảng) |
| R-10 | Thấp | `config/database.php` đặt `strict => false` ⇒ comment về lỗi MySQL 1406 ở controller không đúng môi trường thực; dữ liệu tràn cột sẽ bị cắt im lặng (đã có cắt tên ở code nên không xảy ra) | `ApiIntegrationController.php:32-37`; `config/database.php:53` | Trung bình |
| R-11 | Thấp | Menu 「API連携」 hiện cho mọi staff kể cả chưa được cấp quyền (không kiểm `routeListAccess`) ⇒ bấm vào bị redirect kèm lỗi. Cộng với R-15 ⇒ hiện **mọi** staff đều thấy menu và đều bị chặn | `sidebar.blade.php:14-27, 189-207` | Cao |
| R-12 | Thông tin | Config `reveal_rate_limit_per_minute` không được dùng (route hardcode); `maxKeysPerBot` truyền xuống JS nhưng JS không dùng (không disable nút 発行 khi đủ 10 key — dựa vào 409) | `config/api_integration.php:35`; `index.blade.php:371` | Cao |
| R-13 | Thông tin | Phân trang 「もっと見る」 dùng OFFSET + `id DESC` ⇒ nếu có log mới chen vào giữa 2 lần tải, trang sau có thể lặp 1 dòng | `ApiKeyLogRepository.php:32-33`; `index.js:733-736` | Trung bình |
| R-14 | Thông tin | Comment/doc lỗi thời: `routes/web.php:1018` nhắc middleware `access_feature` (không tồn tại); docblock `resolveOperatorName` nhắc `staff_name` (code dùng `username`) | | Cao |
| R-15 | **Trung bình** | **Staff không thể được cấp quyền 「API連携」 qua màn phân quyền** (FA-035 「スタッフ管理」). Command insert dòng cha `access_feature` **không có `menu_id`** (`NULL`) trong khi `UserController@getSettingRoleAccess` chỉ liệt kê `WHERE menu_id = <index nhóm config('sns-line.access_feature')> AND parent = 0` ⇒ mục không hiện để tick; `addSettingRoleAccess` xoá toàn bộ `bot_role_access` của bot rồi insert lại theo form ⇒ quyền cấp tay vào DB bị xoá ở lần lưu kế tiếp. Không có cơ chế tự cấp nào khác (danh sách auto-grant khi tạo bot ở `Admin\BotController` không có `apiIntegration`; cờ 「新機能追加時に自動でチェックを入れる」 chỉ lưu `setting_new_feature`, không được đọc để cấp quyền). Trái docblock command (`:16` "để hiện trong màn cấp quyền") và khác tiền lệ `AddAccessFeatureWebhookRelay` (đặt `menu_id`). Hệ quả: **chỉ chủ bot dùng được tính năng**; R-02 hiện tiềm ẩn. Cùng phát hiện với db-mapping DB-02 | `AddAccessFeatureApiIntegration.php:16, 56-63`; `UserController.php:3780-3783, 3881, 3926`; `AddAccessFeatureWebhookRelay.php:83, 92-100`; `BotController.php:5224-5250` | Cao (code) — chưa xác minh runtime |
| R-16 | Thấp | Mọi lỗi nghiệp vụ `ApiIntegrationException` (409 trùng tên / đủ 10 key, 404, 422, 503) bị **report như lỗi hệ thống**: class kế thừa `Exception`, không có `report()`, không nằm trong `$dontReport` ⇒ `Handler::report` ghi log error và — khi `APP_ENV` là `staging`/`production` — gọi **đồng bộ** `notifyChatwork` (file ném lỗi `ApiIntegrationException.php` không thuộc danh sách loại trừ `VerifyCsrfToken.php`/`FormRequest.php`/`UrlGenerationException.php`) ⇒ nhiễu kênh cảnh báo + tăng độ trễ response lỗi | `Handler.php:27-29, 48-56, 285-297`; `ApiIntegrationException.php:12` | Cao (code) / Trung bình (hiệu ứng runtime) |

---

## 15. Gap — phần nằm ngoài source

| Hạng mục | Trạng thái | Ảnh hưởng spec |
|---------|-----------|---------------|
| Public API `/v1/*` tiêu thụ API key (xác thực theo `X-LME-Channel-Id` + chữ ký bằng key giải mã, áp `scope`, idempotency qua `api_idempotency_keys`) | Không có ở `src/web` (chỉ comment + `BotRepository::findActiveByChannelId` chưa dùng) và không có ở `src/job/linect-service` | Chưa spec được: cách xác thực, áp quyền 読み取り専用, cập nhật `last_used_at`, hiệu lực "ngay lập tức" khi xoá/hết hạn |
| Job `ApiKeyExpireTask` (chuyển `status=2`, `revoked_at`, ghi log 無効 「システム（自動）」) | Không có | Hiển thị trạng thái vẫn đúng nhờ web tự suy từ `expires_at`, nhưng drawer 「操作履歴」 sẽ **không có log 無効** cho tới khi job tồn tại |
| Job `ApiIdempotencyCleanupTask` | Không có | Bảng `api_idempotency_keys` không được dọn |
| Technical Spec nội bộ (`sprints/.../40041/...`) | Không đọc trong phạm vi agent này | Có thể bổ sung ngữ cảnh BR nội bộ |

---

## 16. Ghi chú cho các agent sau

- **job-analyzer**: hiện **không có** job liên quan trong `src/job/linect-service` (nhánh `release-t09-2026`). Nếu sau này có repo Public API/Job khác, cần tìm: `ApiKeyExpireTask`, `ApiIdempotencyCleanupTask`, logic ghi `api_keys.last_used_at`, `revoked_at`, `api_key_logs.action=3`.
- **db-mapper**: 3 bảng mới chưa có trong dump — dùng schema mục 13; `bot_activity_logs` có cột `action_type` mới giá trị `api_key` và `action_name` `reveal`.
- **ui-parser / validator**: map màn hình theo blade — SCR-API-01 `index`, SCR-API-02 `issue_modal`, SCR-API-03 `issued_modal`, SCR-API-04 `delete_modal`, SCR-API-05 `history_drawer` (trùng thứ tự `SCR-01…05` trong comment source).
