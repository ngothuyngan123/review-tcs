# FA-046 — Liên kết API 「API連携」 — API Spec

> **Nguồn phân tích**
> - Web: `src/web/sns-line` @ nhánh **`release_step_20260930_v2`**, commit **`4d9d07d159`** — task nội bộ **#40041** (tính năng mới), có các bản vá #40298, #40333.
> - Job: `src/job/linect-service` @ nhánh **`release-t09-2026`**, commit **`be6ef546`** — chỉ dùng để xác nhận ranh giới (KHÔNG có code xử lý API key).
> - Ngày phân tích: **2026-10-23**
>
> **Phạm vi**: màn quản trị API key trong portal Admin/Staff (`/basic/api-integration`) — 1 trang Blade + 5 endpoint AJAX. Bản thân **Public API** dùng API key (`/v1/*`) và job hết hạn key **KHÔNG nằm trong source đã clone** — xem mục 7.
>
> Mức tin cậy mặc định: **Cao** (đọc trực tiếp source). Các điểm khác ghi rõ.
>
> Index `src/web/index/routes.md` sinh từ nhánh cũ, không chứa route này → route được đọc trực tiếp ở `routes/web.php:1017-1030`.

---

## 1. Nhóm route & middleware thực tế

```php
// app/Providers/RouteServiceProvider.php:54-58 — mọi route web.php đi qua nhóm 'web'
Route::middleware('web')->namespace($this->namespace)->group(base_path('routes/web.php'));

// routes/web.php:84
Route::middleware(['NotifyChatworkRequestTimeSlow'])->group(function () {
  // routes/web.php:917
  Route::middleware(['LogRequestMultipart'])->group(function () {
    // routes/web.php:964
    Route::group(['prefix' => 'basic', 'middleware' => ['basic_access', 'https_protocol', 'is_expire', 'check_remember_token']], function () {
      // routes/web.php:1020-1030
      Route::group(['prefix' => 'api-integration'], function () { ... });
    });
  });
});
```

→ URL thật có tiền tố **`/basic/api-integration`**. Chuỗi middleware đầy đủ (theo thứ tự): `web` (EncryptCookies, StartSession, ShareErrorsFromSession, **VerifyCsrfToken**, SubstituteBindings — `app/Http/Kernel.php:35-43`) → `NotifyChatworkRequestTimeSlow` → `LogRequestMultipart` → `basic_access` → `https_protocol` → `is_expire` → `check_remember_token` (+ `throttle:30,1` riêng cho EP-05).

Global middleware (`app/Http/Kernel.php:21-27`) có **`TrimStrings`** và **`ConvertEmptyStringsToNull`** — ảnh hưởng tới validate `name` của EP-03 (xem EP-03).

> Comment ở `routes/web.php:1018` nói phân quyền do "`basic_access` + `access_feature`" xử lý — **không tồn tại middleware alias `access_feature`** trong `app/Http/Kernel.php`. `access_feature` là **tên bảng** mà `basic_access` đọc gián tiếp qua helper `getRouterBotInvite()` (xem mục 4).

---

## 2. Danh sách Endpoints

| EP | Method | URI | Route name | Controller@Action | Middleware riêng | Mã nội bộ dev | Mô tả |
|----|--------|-----|-----------|-------------------|-----------------|---------------|-------|
| EP-01 | GET | `/basic/api-integration` | `apiIntegration` | `Basic\ApiIntegrationController@index` | — | (SCR-01) | Render trang 「API連携」 (Blade) |
| EP-02 | GET | `/basic/api-integration/keys` | `apiIntegration.keys` | `Basic\ApiIntegrationController@getKeys` | — | EP-S01 | Danh sách API key của bot (lọc keyword/status, không phân trang) |
| EP-03 | POST | `/basic/api-integration/keys` | `apiIntegration.keys.store` | `Basic\ApiIntegrationController@issueKey` | — (FormRequest `IssueApiKeyRequest`) | EP-S02 | Phát hành key mới — trả **full key** (HTTP 201) |
| EP-04 | DELETE | `/basic/api-integration/keys/{id}` | `apiIntegration.keys.destroy` | `Basic\ApiIntegrationController@deleteKey` | `where id [0-9]+` | EP-S03 | Xoá mềm key |
| EP-05 | GET | `/basic/api-integration/keys/{id}/reveal` | `apiIntegration.keys.reveal` | `Basic\ApiIntegrationController@revealKey` | `where id [0-9]+`, **`throttle:30,1`** | EP-S04 | Trả full key của 1 dòng (hiện / copy) — có ghi audit |
| EP-06 | GET | `/basic/api-integration/logs` | `apiIntegration.logs` | `Basic\ApiIntegrationController@getLogs` | — | EP-S05 | 「操作履歴」 — log 発行/削除/無効, phân trang |

Nguồn: `routes/web.php:1020-1030`. Tất cả middleware chung: `web`, `NotifyChatworkRequestTimeSlow`, `LogRequestMultipart`, `basic_access`, `https_protocol`, `is_expire`, `check_remember_token`.

**Xác thực**: session cookie Laravel (đăng nhập portal Admin). Không có token/API key cho các endpoint này. **Bot scope** luôn lấy từ session `current_bot_id` qua `getBotId()` (`app/Helpers/functions.php:389-393`) — **không endpoint nào nhận `bot_id` từ request** (`ApiIntegrationController.php:20, 67, 90, 115, 136, 153`).

**Định dạng response chung**:
- Thành công: `{"success": true, "data": {...}}` hoặc `{"success": true, "message": "..."}`.
- Lỗi nghiệp vụ (`ApiIntegrationException::render`, `app/Exceptions/ApiIntegration/ApiIntegrationException.php:49-56`): `{"success": false, "error_code": "<mã>", "message": "<JP>"}` + HTTP status tương ứng. Handler chặn exception này **trước** nhánh `app.debug` (`app/Exceptions/Handler.php:124-126`) nên mã lỗi luôn giữ nguyên ở mọi môi trường.

---

## 3. Chi tiết Endpoints

### EP-01: GET `/basic/api-integration`
- **Controller**: `App\Http\Controllers\Basic\ApiIntegrationController@index` (`ApiIntegrationController.php:52-60`)
- **Middleware**: chung (mục 2)
- **Mô tả**: Render view `basic.api_integration.index` (`resources/views/basic/api_integration/index.blade.php`) kèm 4 component: `issue_modal`, `issued_modal`, `delete_modal`, `history_drawer` (`index.blade.php:328-331`). View không có dữ liệu key — danh sách tải bằng AJAX (EP-02) ở `mounted` (`public/_assets/modules/api_integration/js/index.js:220-225`).
- **Liên kết UI**: SCR-API-01 (`index`) — vào từ menu sidebar 「API連携」 (`resources/views/layout/v2/admin/sidebar.blade.php:189-207`).

#### Dữ liệu truyền cho view
| Biến | Nguồn | Mô tả |
|------|-------|-------|
| `maxKeysPerBot` | `config('api_integration.max_keys_per_bot', 10)` → env `API_INTEGRATION_MAX_KEYS_PER_BOT` | Đưa vào `window.API_INTEGRATION_CONFIG.maxKeysPerBot` (`index.blade.php:371`) — **JS không dùng tới** (Cao — grep `index.js` không thấy) |
| `docsUrl` | `config('api_integration.docs_url', '')` → env `API_INTEGRATION_DOCS_URL` | Rỗng ⇒ ẩn nút 「使い方を見る」 (`index.blade.php:44`); có ⇒ mở tab mới (`index.js:554-555`) |

`window.API_INTEGRATION_CONFIG.urls` (`index.blade.php:362-373`) chứa URL của EP-02/03/06 (sinh bằng `route()`) và base `/basic/api-integration/keys` cho EP-04/05 (JS nối `/{id}` và `/{id}/reveal`).

#### Response lỗi (do middleware)
| HTTP | Điều kiện | Kết quả |
|------|-----------|---------|
| 302 → `logout` | Chưa đăng nhập / `users.role` ngoài {-1,0,1,2} | `BasicAccess.php:31, 189-191` |
| 302 → `adminIndex` + 「この権限は許可されていません。」 | Staff mà role chưa được cấp màn 「API連携」 — với code hiện tại là **mọi Staff** (không cấp được qua màn phân quyền, xem mục 4) | `BasicAccess.php:38-51` |
| 302 → `adminIndex` | Session chưa có `current_bot_id` | `BasicAccess.php:187` |
| 302 → `pointSettings` / `/admin/home` | Bot hết hạn hợp đồng / bot không tồn tại | `IsExpire.php` |

---

### EP-02: GET `/basic/api-integration/keys`
- **Controller**: `ApiIntegrationController@getKeys` (`ApiIntegrationController.php:65-83`) → `ApiKeyService@getKeyList` (`ApiKeyService.php:57-81`) → `ApiKeyRepository@getAllForBot` (`ApiKeyRepository.php:36-91`)
- **Mô tả**: Lấy **toàn bộ** key chưa xoá của bot hiện tại (không phân trang — #40333, vì tối đa 10 key/bot), lọc theo tên và trạng thái, mới nhất lên đầu. **Không bao giờ trả full key** — chỉ dạng che.
- **Liên kết UI**: SCR-API-01 (`index`) — tải khi mở trang, khi gõ ô tìm kiếm 「キー名を入力して検索」 (debounce / Enter), khi đổi dropdown trạng thái, sau khi phát hành/xoá thành công, nút 「再試行」 (`index.js:336-…, 436-456`). Timeout phía FE 10 giây (`index.js:25`).

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|-----------|-------|-----------|
| `keyword` | Query | String | Không | Tìm theo `api_keys.name` (LIKE `%kw%`, đã escape `%`, `_`, `\`) | Không validate; trim; rỗng ⇒ không lọc (`ApiKeyRepository.php:65-70`) |
| `status` | Query | String | Không | `all` \| `active` \| `expired` | Giá trị lạ ⇒ `all` (không báo lỗi) — `ApiIntegrationController.php:247-250` |

> `page`/`per_page` **không còn được nhận** (#40333, `ApiIntegrationController.php:71-73`).

#### Request mẫu
```
GET /basic/api-integration/keys?keyword=予約&status=active
X-Requested-With: XMLHttpRequest
X-CSRF-TOKEN: <token>
```

#### Response mẫu (thành công — HTTP 200)
```json
{
  "success": true,
  "data": {
    "keys": [
      {
        "id": 12,
        "name": "予約システム連携",
        "key_masked": "lme_live_sk_••••••••••••a1b2",
        "scope": "full",
        "scope_label": "全権限",
        "status": "active",
        "expires_at": "2026/11/22",
        "last_used_at": null,
        "issued_by": "suzuki（主管理者）"
      }
    ],
    "total_items": 1
  }
}
```

| Field | Nguồn | Ghi chú |
|-------|-------|--------|
| `key_masked` | `key_prefix` + 12 × 「•」 + `key_last4` (`ApiKey.php:124-127`) | 28 ký tự |
| `scope` / `scope_label` | `scope` 1→`full`/「全権限」, 2→`read`/「読み取り専用」 (`ApiKey.php:50-65`) | |
| `status` | `active` \| `expired` — suy từ `status = 2` **hoặc** `expires_at < now` (`ApiKey.php:104-119`) | Không phụ thuộc job hết hạn |
| `expires_at` | `Y/m/d` hoặc `null` (= 無期限) | FE hiện chữ mờ 「無期限」 (`index.blade.php:213`) |
| `last_used_at` | `Y/m/d H:i` hoặc `null` | FE hiện 「未使用」 (`index.blade.php:225`). **Web không bao giờ ghi cột này** → luôn `null` trừ khi hệ thống ngoài cập nhật |
| `issued_by` | `users.username` hiện tại + 「（vai trò hiện tại）」; fallback snapshot `created_by_name`; fallback 「システム（自動）」 (`ApiKeyService.php:398-419`) | |
| `total_items` | `count(keys)` sau khi lọc | |

#### Response lỗi
| HTTP | Điều kiện | Body |
|------|----------|------|
| 302 | Middleware chặn (xem EP-01) | Redirect HTML — FE rơi vào nhánh fail, hiện 「APIキーの取得に失敗しました」 |
| 200 | `check_remember_token`: mật khẩu đã đổi ở phiên khác | `{"result":false,"status":false,"success":false,"message":"ログイン情報が変更されましたので、再度ログインしてください。",...}` (`CheckRememberToken.php`) |
| 404 / 401 | Exception bất ngờ khi `APP_DEBUG=false` (vd lỗi DB) — Handler đổi mọi exception AJAX thành HTTP **404 nếu HTTPS, 401 nếu HTTP** | `{"status":false,"error":{"code":<status>,"message":"<getMessage()>"}}` (`Handler.php:152-170`) — **Trung bình** |

---

### EP-03: POST `/basic/api-integration/keys`
- **Controller**: `ApiIntegrationController@issueKey` (`ApiIntegrationController.php:88-108`) → `ApiKeyService@issue` (`ApiKeyService.php:95-208`)
- **FormRequest**: `App\Http\Requests\ApiIntegration\IssueApiKeyRequest` (`authorize()` = true)
- **Mô tả**: Phát hành API key mới cho bot hiện tại. Trong 1 transaction có khoá hàng `bots`: kiểm tra trùng tên + ngưỡng 10 key → sinh key → insert `api_keys` + insert `api_key_logs` (action 発行). Trả **full key 1 lần** trong response, header `Cache-Control: no-store` (`ApiIntegrationController.php:106-107`).
- **Liên kết UI**: SCR-API-02 (`issue_modal` 「APIキーを発行」) nút 「発行する」 (`issue_modal.blade.php:58`, `index.js:573-648`); thành công ⇒ đóng modal, mở SCR-API-03 (`issued_modal` 「APIキーを発行しました」), toast 「APIキーを発行しました」, tải lại danh sách (EP-02).

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation (thứ tự thực tế) |
|-------|--------|------|-----------|-------|---------------------------|
| `name` | Body (form-urlencoded) | String | Có | 「キー名」 | FormRequest: `present\|string` (msg `name.present` = 「キー名を入力してください。」). Service: trim → rỗng ⇒ `name_required`; `mb_strlen > 50` ⇒ `name_too_long`; trùng tên (trong transaction) ⇒ `name_duplicated` |
| `scope` | Body | String | Có | `full` (全権限) \| `read` (読み取り専用) | FormRequest `required\|in:full,read` (「権限を選択してください。」/「権限の値が不正です。」); service kiểm tra lại (`ApiKeyService.php:113-115`) |
| `expiry_preset` | Body | String | Có | `1` (1日) \| `7` (1週間) \| `30` (30日) \| `unlimited` (無期限) | FormRequest `required\|in:1,7,30,unlimited` (「有効期限を選択してください。」/「有効期限の値が不正です。」); service kiểm tra lại theo `config('api_integration.expiry_presets')` (`ApiKeyService.php:116-118`) |

FE mặc định: `name=''`, `scope='full'`, `expiry_preset='30'` (`index.js:120`). FE tự validate trước khi gửi: tên rỗng sau `trim()` ⇒ 「キー名を入力してください。」; `length > 50` ⇒ 「キー名は50文字以内で入力してください。」 (`index.js:583-593`).

> ⚠ **Đường validate tên rỗng thực tế** (Cao): `TrimStrings` + `ConvertEmptyStringsToNull` biến `name=""`/`"   "` thành `null` ⇒ rule `string` của FormRequest **fail trước** service ⇒ lỗi `nameRequired()` của service **không bao giờ chạm tới qua HTTP**. Message FormRequest = `validation.string` tiếng Nhật 「nameには文字を指定してください。」 (`resources/lang/ja/validation.php:89`, locale `ja` — `config/app.php:81`, không có alias attribute `name`) — **chỉ hiện khi `APP_DEBUG=true`** (inline dưới 「キー名」); production nhận 404/401 (dòng `ValidationException` bên dưới) ⇒ alert fallback 「APIキーの発行に失敗しました」. Chỉ xảy ra khi bypass FE.

#### Request mẫu
```
POST /basic/api-integration/keys
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-CSRF-TOKEN: <token>
X-Requested-With: XMLHttpRequest

name=予約システム連携&scope=read&expiry_preset=7
```

#### Response mẫu (thành công — HTTP 201, `Cache-Control: no-store`)
```json
{
  "success": true,
  "data": {
    "id": 13,
    "api_key": "lme_live_sk_3f9c0a7e5b1d4c2a8e6f0b9d7c5a3e1f",
    "name": "予約システム連携",
    "scope": "read",
    "scope_label": "読み取り専用",
    "expires_at": "2026/10/30"
  }
}
```
- `api_key`: `lme_live_sk_` + 32 ký tự hex (44 ký tự) — `ApiKeyCipher.php:30-35`.
- `expires_at`: `Y/m/d` của (hôm nay + N ngày) — giờ thật lưu DB là `23:59:59`; `null` khi `unlimited`.

#### Response lỗi
| HTTP | `error_code` | Điều kiện | `message` |
|------|-------------|----------|-----------|
| 422 | `name_required` | Tên rỗng sau trim (thực tế khó chạm — xem ⚠ trên) | 「キー名を入力してください。」 |
| 422 | `name_too_long` | `mb_strlen(name) > 50` | 「キー名は50文字以内で入力してください。」 |
| 422 | `invalid_parameter` | scope / expiry_preset sai (chỉ khi lọt qua FormRequest — thực tế không xảy ra) | 「権限の値が不正です。」 / 「有効期限の値が不正です。」 |
| 409 | `name_duplicated` | Đã có key **chưa xoá** cùng tên trong bot (so sánh theo collation `utf8mb4_unicode_ci`) | 「同じキー名が既に存在します。別の名前を入力してください。」 |
| 409 | `key_limit_reached` | Số key chưa xoá (kể cả 無効) ≥ `max_keys_per_bot` | 「発行できるAPIキーは10件までです。不要なキーを削除してから発行してください。」 (số lấy từ config) |
| 422 (debug) / **404 hoặc 401** (prod) | — | FormRequest fail (`ValidationException`) | `APP_DEBUG=true`: `{"message":"The given data was invalid.","errors":{"scope":["権限の値が不正です。"]}}`. `APP_DEBUG=false`: Handler không xử lý riêng `ValidationException` ⇒ rơi vào nhánh AJAX `Handler.php:152-170` ⇒ `{"status":false,"error":{"code":500,"message":"The given data was invalid."}}` với HTTP 404 (HTTPS)/401 — **Trung bình** (FE nhánh `xhr.status === 422` ở `index.js:637` không bao giờ chạy ở prod) |
| 401 | — | CSRF token hết hạn (`TokenMismatchException` + AJAX) | `{"success":false,"status":false,"msg":"セッションの有効期限が切れました。再度ログインしてください。","code":"SESSION_EXPIRED"}` (`Handler.php:110-118`) |
| 404 / 401 | — | Thiếu/ sai env `API_KEY_PEPPER` hoặc `API_KEY_ENC_KEY` ⇒ `RuntimeException` (`ApiKeyCipher.php:116-147`) | `{"status":false,"error":{"code":500,"message":"[#40041] Thiếu API_KEY_PEPPER — ..."}}` — **lộ thông điệp nội bộ** (xem logic-spec mục Bảo mật) |

FE xử lý (`index.js:620-647`): `name_duplicated`/`name_required`/`name_too_long` ⇒ lỗi inline dưới ô 「キー名」, modal giữ nguyên; `key_limit_reached` ⇒ alert trong modal; còn lại ⇒ alert 「APIキーの発行に失敗しました」 hoặc `body.message`.

---

### EP-04: DELETE `/basic/api-integration/keys/{id}`
- **Controller**: `ApiIntegrationController@deleteKey` (`ApiIntegrationController.php:113-129`) → `ApiKeyService@deleteKey` (`ApiKeyService.php:220-267`)
- **Mô tả**: Xoá mềm key (`is_deleted=1`, `deleted_at`, `deleted_by_user_id`) + ghi `api_key_logs` action 削除 trong 1 transaction. Xoá được cả key đang 無効. Theo nghiệp vụ, "liên kết đang dùng key sẽ dừng ngay" — hiệu lực thực tế phụ thuộc Public API bên ngoài (`ApiKeyService.php:258-259`).
- **Liên kết UI**: SCR-API-04 (`delete_modal` 「APIキーを削除します」) nút 「削除する」 (`delete_modal.blade.php:38`, `index.js:675-…`); mở từ icon xoá ở cột 「操作」 của SCR-API-01. Thành công ⇒ đóng modal, toast 「APIキーを削除しました」, tải lại EP-02; thất bại ⇒ giữ modal + hiện lỗi.

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|-----------|-------|-----------|
| `id` | Path | Integer | Có | `api_keys.id` | Route regex `[0-9]+` (`routes/web.php:1024`); service lọc `bot_id` + `is_deleted=0` |

#### Request mẫu
```
DELETE /basic/api-integration/keys/13
X-CSRF-TOKEN: <token>
X-Requested-With: XMLHttpRequest
```

#### Response mẫu (thành công — HTTP 200)
```json
{ "success": true, "message": "APIキーを削除しました" }
```

#### Response lỗi
| HTTP | `error_code` | Điều kiện | `message` |
|------|-------------|----------|-----------|
| 404 | `resource_not_found` | Key không tồn tại / thuộc bot khác / đã xoá; hoặc bị xoá đồng thời (UPDATE trả 0 hàng — không ghi log lần 2) | 「対象のAPIキーが見つかりません。」 |
| 404 / 401 | — | `id` không phải số ⇒ không khớp route (`NotFoundHttpException`) | JSON chung của Handler (`Handler.php:152-170`) |
| 401 | — | CSRF hết hạn | như EP-03 |

---

### EP-05: GET `/basic/api-integration/keys/{id}/reveal`
- **Controller**: `ApiIntegrationController@revealKey` (`ApiIntegrationController.php:134-146`) → `ApiKeyService@revealKey` (`ApiKeyService.php:278-308`) → `ApiKeyCipher@decrypt` (`ApiKeyCipher.php:89-111`)
- **Middleware riêng**: `throttle:30,1` (30 request/phút) — `routes/web.php:1026-1028`
- **Mô tả**: Giải mã AES-256-GCM và trả full key của 1 dòng. Mỗi lần gọi thành công ghi 1 bản ghi audit vào **`bot_activity_logs`** (`action_type='api_key'`, `action_name='reveal'`, `new_value` = JSON `{"api_key_id":..,"name":..}`) — KHÔNG ghi `api_key_logs`. Không chặn key 無効 (chỉ chặn key đã xoá). Header `Cache-Control: no-store`.
- **Liên kết UI**: SCR-API-01 (`index`) — cột 「APIキー」: icon 👁 「APIキーを表示する」 (`toggleReveal`, `index.js:471-496`) và icon copy 「APIキーをコピー」 (`copyKey`, `index.js:499-519` — nếu chưa từng hiện thì gọi EP-05 rồi mới copy). FE cache full key theo `id` trong phiên trang ⇒ mỗi dòng chỉ gọi 1 lần.

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|-----------|-------|-----------|
| `id` | Path | Integer | Có | `api_keys.id` | Regex `[0-9]+`; lọc `bot_id` + `is_deleted=0` |

#### Request mẫu
```
GET /basic/api-integration/keys/12/reveal
X-Requested-With: XMLHttpRequest
```

#### Response mẫu (thành công — HTTP 200, `Cache-Control: no-store`)
```json
{ "success": true, "data": { "api_key": "lme_live_sk_3f9c0a7e5b1d4c2a8e6f0b9d7c5a3e1f" } }
```

#### Response lỗi
| HTTP | `error_code` | Điều kiện | `message` |
|------|-------------|----------|-----------|
| 404 | `resource_not_found` | Key không tồn tại / bot khác / đã xoá | 「対象のAPIキーが見つかりません。」 |
| 503 | `decrypt_failed` | `openssl_decrypt` trả false/rỗng (sai khoá, khoá đã xoay, dữ liệu hỏng) — có `logError` kèm id (không kèm key) | 「APIキーを復号できませんでした。」 |
| 429 (debug) / **404 hoặc 401** (prod) | — | Vượt 30 lần/phút. Laravel 5.5 ném `HttpException(429, 'Too Many Attempts.')`; với `APP_DEBUG=false` Handler đổi thành JSON chung `{"status":false,"error":{"code":429,"message":"Too Many Attempts."}}` HTTP 404/401 | FE hiện 「APIキーの表示に失敗しました」 / 「コピーに失敗しました」 — **Trung bình** (vendor Laravel không có trong repo để xác nhận) |
| 404 / 401 | — | Thiếu env `API_KEY_ENC_KEY` ⇒ `RuntimeException` | JSON chung, lộ message nội bộ |

---

### EP-06: GET `/basic/api-integration/logs`
- **Controller**: `ApiIntegrationController@getLogs` (`ApiIntegrationController.php:151-167`) → `ApiKeyService@getOperationLogs` (`ApiKeyService.php:319-354`) → `ApiKeyLogRepository@paginateForBot` (`ApiKeyLogRepository.php:23-34`)
- **Mô tả**: Lịch sử thao tác 「操作履歴」 của bot từ bảng **`api_key_logs`** (3 loại 発行/削除/無効), mới nhất lên đầu, gồm cả log của key đã xoá. **Không gồm** sự kiện xem lại key (reveal) — sự kiện đó nằm ở `bot_activity_logs`.
- **Liên kết UI**: SCR-API-05 (`history_drawer` 「操作履歴」) — mở bằng nút 「操作履歴」 trên SCR-API-01 (`index.blade.php:55`), dropdown lọc loại thao tác, nút 「もっと見る」 (`history_drawer.blade.php:72`, `index.js:722-760`). FE luôn gửi `per_page=20`.

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|-----------|-------|-----------|
| `action` | Query | String | Không | `all` \| `issue` \| `delete` \| `revoke` | Giá trị lạ ⇒ `all` (`ApiIntegrationController.php:255-258`) |
| `page` | Query | Integer | Không | Trang | `(int)`; ≤ 0 ⇒ 1 (`:260-265`) |
| `per_page` | Query | Integer | Không | Số dòng/trang | Phải thuộc `[10,20,30,50,100]` (`config('api_integration.per_page_options')`), khác ⇒ `list_per_page` = 20 (`:270-278`) |

#### Request mẫu
```
GET /basic/api-integration/logs?action=all&page=1&per_page=20
```

#### Response mẫu (thành công — HTTP 200)
```json
{
  "success": true,
  "data": {
    "logs": [
      {
        "id": 31,
        "action": "delete",
        "action_label": "削除",
        "key_name": "テスト用",
        "detail": "一覧から削除しました",
        "operator_name": "suzuki（主管理者）",
        "created_at": "2026/10/23 14:05"
      },
      {
        "id": 30,
        "action": "issue",
        "action_label": "発行",
        "key_name": "テスト用",
        "detail": "権限：全権限 ／ 有効期限：2026/11/22",
        "operator_name": "suzuki（主管理者）",
        "created_at": "2026/10/23 13:58"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total_items": 2,
      "total_pages": 1,
      "has_next": false
    }
  }
}
```
- `action`/`action_label`: 1→`issue`/「発行」, 2→`delete`/「削除」, 3→`revoke`/「無効」 (`ApiKeyLog.php:56-66`).
- `created_at`: `Y/m/d H:i`.
- Log 無効 (revoke): `operator_name` dự kiến 「システム（自動）」, do hệ thống ngoài ghi — web không tạo.

#### Response lỗi
Không có lỗi nghiệp vụ riêng; chỉ lỗi middleware/Handler chung như EP-02. FE: toast 「操作履歴の取得に失敗しました」.

---

## 4. Middleware phân tích

| Middleware | Mô tả | Áp dụng cho |
|-----------|-------|------------|
| `web` group (`Kernel.php:35-43`) | Cookie mã hoá, session, **VerifyCsrfToken** (danh sách `$except` trong `VerifyCsrfToken.php:14-54` **không** miễn `/basic/*` ⇒ POST/DELETE bắt buộc `X-CSRF-TOKEN`; FE gửi header này ở mọi request — `index.js:42-53`) | EP-01…06 |
| `NotifyChatworkRequestTimeSlow` | Gửi cảnh báo Chatwork khi request chậm; không log body/response | EP-01…06 |
| `LogRequestMultipart` | Chỉ log URL khi `Content-Type` multipart — không áp dụng thực tế | EP-01…06 |
| `basic_access` (`app/Http/Middleware/BasicAccess.php`) | Bắt buộc đăng nhập (`users.role ∈ {-1,0,1,2}`); nếu user **không phải chủ bot** (`bots.admin_id ≠ Auth::id()`) hoặc session `is_bot_invite` ⇒ route name phải nằm trong `getRouterBotInvite()` (route của `access_feature` được cấp cho role qua `bot_role_access`, kèm route con) — không đạt ⇒ redirect 302 `adminIndex` 「この権限は許可されていません。」. Side effect: ghi `user_access_bot` (bảng số ít — `app/UserAccessBot.php:11`) 1 lần/ngày cho user có hàng `user_staff_bots` | EP-01…06 |
| `https_protocol` | Thân hàm đã comment out — **không làm gì** | EP-01…06 |
| `is_expire` | Bảo trì / bot không tồn tại / hợp đồng hết hạn ⇒ redirect | EP-01…06 |
| `check_remember_token` | Mật khẩu đã reset ở nơi khác ⇒ logout; AJAX trả 200 `success:false` + 「ログイン情報が変更されましたので、再度ログインしてください。」 | EP-01…06 |
| `throttle:30,1` | 30 request/phút. Laravel 5.5: khoá limiter = `sha1(user id)` (theo **user**, không theo session/route như comment ghi "30 lần/phút/session") — **Trung bình** | EP-05 |

**Quyền Staff**: command `php artisan access-feature:api-integration` (`app/Console/Commands/AddAccessFeatureApiIntegration.php`) thêm vào bảng `access_feature` 1 dòng cha `apiIntegration` (`name='API連携'`, `visible=1`) và 5 dòng con (`visible=0`) cho EP-02…06. **Theo thiết kế**, Admin cấp quyền màn 「API連携」 cho role ⇒ staff được dùng **toàn bộ 6 endpoint** (không tách quyền xem/phát hành/xoá/hiện key).

> ⚠ **Thực tế với code hiện tại (Cao)**: dòng cha được insert **không có `menu_id`** (`AddAccessFeatureApiIntegration.php:56-63`) trong khi màn phân quyền Staff (`Admin\UserController@getSettingRoleAccess`, FA-035) chỉ liệt kê `access_feature WHERE menu_id = <nhóm> AND parent = 0` (`UserController.php:3780-3783`) ⇒ mục 「API連携」 **không xuất hiện để tick**; cấp tay vào `bot_role_access` sẽ bị `addSettingRoleAccess` xoá-insert lại (`:3881`, `:3926`) ở lần lưu kế tiếp ⇒ **hiện chỉ chủ bot gọi được EP-01…06**; mọi Staff nhận 302 `adminIndex`. So sánh: `AddAccessFeatureWebhookRelay.php:83, 92-100` có đặt `menu_id`. Xem logic-spec R-15, db-mapping DB-02.

---

## 5. Liên kết UI ↔ API

| Màn hình (mã ui-spec) | Blade | Action trên UI | Endpoint | Ghi chú |
|----------------------|-------|---------------|----------|---------|
| SCR-API-01 | `index.blade.php` | Mở trang qua menu 「API連携」 | EP-01 → EP-02 | Tải danh sách khi `mounted` |
| SCR-API-01 | `index.blade.php` | Ô tìm 「キー名を入力して検索」 / dropdown 「すべてのステータス・有効・無効（期限切れ）」 / 「再試行」 | EP-02 | `keyword`, `status` |
| SCR-API-01 | `index.blade.php` | Icon 👁 「APIキーを表示する」 | EP-05 | Ghi audit `bot_activity_logs`; cache FE |
| SCR-API-01 | `index.blade.php` | Icon copy 「APIキーをコピー」 | EP-05 (nếu chưa cache) | Copy cũng sinh audit 「APIキー表示」 |
| SCR-API-01 | `index.blade.php` | Nút 「使い方を見る」 | — | Link ngoài `docsUrl`; ẩn nếu rỗng |
| SCR-API-02 | `components/issue_modal.blade.php` | Nút 「発行する」 | EP-03 | Form 「キー名」「権限」「有効期限」 |
| SCR-API-03 | `components/issued_modal.blade.php` | Hiển thị full key + nút copy | (dữ liệu từ response EP-03) | Không gọi API thêm |
| SCR-API-04 | `components/delete_modal.blade.php` | Nút 「削除する」 | EP-04 | |
| SCR-API-05 | `components/history_drawer.blade.php` | Mở drawer 「操作履歴」 / lọc 「すべての操作・発行・削除・無効」 / 「もっと見る」 | EP-06 | `per_page=20` |

---

## 6. Endpoint liên quan ngoài màn này

| Endpoint | Liên quan | Ghi chú |
|----------|----------|--------|
| Timeline 「アクティビティログ」 (tab 「操作履歴」) của màn **「接続設定」** `GET /admin/setting-bot/{id}` (`resources/views/admin/setting-bot/index.blade.php:2, 233, 269`; dữ liệu qua route `settingBot.history` (`routes/web.php:657`) → `Admin\SettingBotController@getHistory` → `SettingBotService::getBotHistoryLogs`, `app/Services/SettingBotService.php:14-60`). Comment source gọi là "timeline アカウント設定" (`BotActivityLog.php:37`) — tên không chính thức | Hiển thị bản ghi audit reveal của EP-05 với tiêu đề 「APIキー表示」, nhãn 「API連携」, giá trị = tên key (`BotActivityLog.php:38,46`; `BotActivityLogResource.php:50-57`) | Thuộc tính năng cài đặt bot, không thuộc FA-046 |

---

## 7. Gap — phần KHÔNG có trong source đã clone

> ✅ **Cập nhật 2026-11-04**: hợp đồng Public API `/v1/*` (phần "không có trong source" dưới đây) đã có **tài liệu nhà cung cấp** — xem [`api-public/public-api-spec.md`](../../../api-public/public-api-spec.md) (contract-first, bản 1.2.0 / 28-09-2026, WSSJ→Missiona; bản HTML gốc [`api-public/docs/api_v1_1104.html`](../../../api-public/docs/api_v1_1104.html)). Format `lme_live_sk_`, HMAC `key_lookup_hash`, scope, idempotency ở doc **khớp** bằng chứng migration bên dưới. Doc là **oracle expected cho TC** nhưng vẫn chưa verify được bằng code runtime.

| Hạng mục | Bằng chứng tồn tại (chỉ ở comment / migration) | Kết quả grep | Confidence |
|---------|----------------------------------------------|-------------|-----------|
| **Public API `/v1/*`** dùng API key (EP-09/EP-10/EP-11, vd `messages.push`) | `config/api_integration.php:8-9` ("API công khai `/v1/*` do job Java implement"); `create_api_idempotency_keys_table.php:7-13` | Không có route `/v1` liên quan trong `routes/*.php`; không có code ở `src/job/linect-service` (grep `ApiKey`, `api_key_logs`, `lme_live`, `X-LME-Channel-Id` — chỉ trùng `EsService.java:80` header Elasticsearch, không liên quan) | Cao (về việc vắng mặt) |
| Middleware xác thực `api_signature_auth` (header `X-LME-Channel-Id`, ký bằng key giải mã) | `BotRepositoryInterface.php:44-49`, `BotRepository.php:249-261` (`findActiveByChannelId` — **không có nơi gọi**); `ApiKeyCipher.php:83` ("từ Phase 2 — middleware xác thực chữ ký") | Không có class/alias middleware | Cao |
| Job hết hạn `ApiKeyExpireTask` (chuyển `status=2`, ghi `revoked_at`, ghi log 無効 với 「システム（自動）」) | `ApiKey.php:100`, `ApiKeyRepository.php:72-73`, `create_api_key_logs_table.php:11` | Không có ở web lẫn job repo; `app/Console/Kernel.php` không schedule gì liên quan | Cao |
| Job dọn `ApiIdempotencyCleanupTask` | `create_api_idempotency_keys_table.php:12` | Không có | Cao |
| Cập nhật `api_keys.last_used_at` | `create_api_keys_table.php:32` | Không có code ghi | Cao |

→ Cần thu thập thêm source service Public API (có thể là repo/branch Java khác) để hoàn thiện spec phần tiêu thụ key.
