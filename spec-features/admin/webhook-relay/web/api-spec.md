# FA-047 — Chuyển tiếp Webhook 「Webhook転送」 — API Spec

> **Nguồn phân tích**
> - Web: `src/web/sns-line` @ nhánh **`release_step_20260930_v2`**, commit **`4d9d07d159`** (task gốc #40044, các bug fix #40520/#40528/#40529/#40530/#40531/#40533/#40728/#40762/#40763/#40764/#40792/#41030)
> - Job (chỉ để xác định ranh giới trách nhiệm, không trace sâu): `src/job/linect-service` @ nhánh **`release-t09-2026`**, commit **`be6ef546`**
> - Ngày phân tích: **2026-10-23**. Phương pháp: **code-first** (session hết hạn, chưa quét live).
>
> **Phạm vi**: màn 「Webhook転送」 (`/admin/webhook-relay`) + 5 endpoint AJAX của màn + 1 endpoint DEBUG ở `routes/api.php`. Điểm vào webhook LINE (`Admin\BotController@callbackWebHook`) **không thuộc** tính năng này nhưng là nguồn dữ liệu của kênh 1 — mô tả ở `logic-spec.md` mục 8.
>
> **Quy ước mã EP**: `EP-01…EP-05` **trùng đúng** mã nội bộ trong comment source (`WebhookRelayController`, `WebhookRelayService`, `routes/web.php:665-667`) để tra cứu chéo. Hai endpoint không có mã nội bộ được đánh tiếp: `EP-06` (trang HTML), `EP-07` (debug).
>
> Mức tin cậy mặc định: **Cao** (đọc trực tiếp source). Chỗ nào khác được ghi rõ.

---

## 1. Prefix & nhóm route — xác định thực tế

```php
// src/web/sns-line/routes/web.php:84
Route::middleware(['NotifyChatworkRequestTimeSlow'])->group(function () {
    // routes/web.php:105
    Route::group(['prefix' => '/admin', 'middleware' => ['admin_access', 'https_protocol', 'check_remember_token']], function () {
        // routes/web.php:659-670
        // Webhook転送 (task #40044) — 2 tab = 2 kênh nằm trên CÙNG 1 route, bot lấy từ session
        Route::group(['prefix' => 'webhook-relay'], function () {
            Route::get('/', ...);                    // :661
            Route::get('/config', ...);              // :662
            Route::post('/save', ...);               // :663
            Route::post('/regenerate-secret', ...);  // :664
            Route::get('/errors', ...);              // :666
            Route::get('/secret', ...)->middleware('throttle:10,1'); // :668-669
        });
    }); // :671
});
```

Toàn bộ `routes/web.php` được nạp với nhóm middleware `web` (`app/Providers/RouteServiceProvider.php:56`) ⇒ có session + CSRF. URL thật = `/admin` + `/webhook-relay` + path.

Endpoint debug nằm ở **`routes/api.php:440-446`**, **ngoài mọi group** của file đó; file được nạp với `prefix('api')` + middleware `api` (`RouteServiceProvider.php:70-73`), mà nhóm `api` chỉ có `bindings` (`app/Http/Kernel.php:45-48`, `throttle:60,1` bị comment) ⇒ **không session, không auth, không CSRF**.

| Khai báo | URL thật | Route name | JS gọi (bằng chứng) |
|---|---|---|---|
| `webhook-relay/` (`web.php:661`) | `/admin/webhook-relay` | `webhookRelay` | sidebar `resources/views/layout/v2/admin/sidebar.blade.php:213,230` |
| `webhook-relay/config` (`:662`) | `/admin/webhook-relay/config` | `webhookRelay.config` | `public/js/admin/webhook-relay/webhook-relay.js:147` |
| `webhook-relay/save` (`:663`) | `/admin/webhook-relay/save` | `webhookRelay.save` | `webhook-relay.js:303-312` |
| `webhook-relay/regenerate-secret` (`:664`) | `/admin/webhook-relay/regenerate-secret` | `webhookRelay.regenerateSecret` | `webhook-relay.js:465` |
| `webhook-relay/errors` (`:666`) | `/admin/webhook-relay/errors` | `webhookRelay.errors` | `webhook-relay.js:528-533` |
| `webhook-relay/secret` (`:668`) | `/admin/webhook-relay/secret` | `webhookRelay.secret` | `webhook-relay.js:407` |
| `/webhook-decode/{secret}` (`api.php:443`) | `/api/webhook-decode/{secret}` | `webhookRelay.debugDecode` | **Không có** — chỉ gọi tay khi test |

URL các endpoint AJAX **không viết cứng trong JS**: controller dựng bằng `route()` rồi truyền xuống view qua biến `window.WEBHOOK_RELAY_CONFIG` (`WebhookRelayController.php:48-66`, `index.blade.php:194`).

---

## 2. Danh sách Endpoints

| EP | Method | URI | Route name | Controller@Action | Middleware | Xác thực / phạm vi | Mô tả | Mã nội bộ |
|----|--------|-----|-----------|-------------------|-----------|--------------------|-------|-----------|
| EP-01 | GET | `/admin/webhook-relay/config` | `webhookRelay.config` | `Admin\WebhookRelayController@getConfig` | web, `NotifyChatworkRequestTimeSlow`, `admin_access`, `https_protocol`, `check_remember_token` | Session; `bot_id` từ session; owner hoặc Staff có quyền màn | Cấu hình 2 kênh + secret đã mask. **Có ghi DB** (sinh secret lần đầu + đóng mốc 「最終更新」 cả 2 kênh) | EP-01 |
| EP-02 | POST | `/admin/webhook-relay/save` | `webhookRelay.save` | `Admin\WebhookRelayController@save` | như EP-01 (+ CSRF) | như EP-01 | Lưu URL đích + bật/tắt của **một** kênh (kênh của tab đang mở) | EP-02 |
| EP-03 | POST | `/admin/webhook-relay/regenerate-secret` | `webhookRelay.regenerateSecret` | `Admin\WebhookRelayController@regenerateSecret` | như EP-01 (+ CSRF) | như EP-01 | Tái tạo 「署名シークレット」 (kênh LME), secret cũ mất hiệu lực ngay | EP-03 |
| EP-04 | GET | `/admin/webhook-relay/errors?channel=1\|2[&refresh=1]` | `webhookRelay.errors` | `Admin\WebhookRelayController@getErrors` | như EP-01 | như EP-01 | 100 lỗi chuyển tiếp gần nhất của một kênh; `refresh=1` đóng mốc 「最終更新」 kênh đó | EP-04 |
| EP-05 | GET | `/admin/webhook-relay/secret` | `webhookRelay.secret` | `Admin\WebhookRelayController@getSecret` | như EP-01 + **`throttle:10,1`** | như EP-01 | Trả **plaintext** secret (xem/copy), ghi audit, `Cache-Control: no-store` | EP-05 |
| EP-06 | GET | `/admin/webhook-relay` | `webhookRelay` | `Admin\WebhookRelayController@index` | như EP-01 | như EP-01 (sai quyền → redirect) | Render trang (Vue mount `#webhook-relay-app`) | — |
| EP-07 | GET | `/api/webhook-decode/{secret}` | `webhookRelay.debugDecode` | `Api\WebhookRelayDebugController@decode` | `api` (`bindings`), **`throttle:20,1`** | **KHÔNG CÓ** — guard `APP_DEBUG` đang bị comment ⇒ **mở ở mọi môi trường** | Tra ngược plaintext secret → `bot_id` + ciphertext đang lưu | — (DEBUG) |

> ⚠ **EP-07 đang mở công khai trên nhánh release** — xem chi tiết EP-07 và `logic-spec.md` mục 14 (SEC-01). Mức tin cậy: **Cao** (`WebhookRelayDebugController.php:49-51`, commit `3f3c7ddf95` "comment debug", 2026-09-10, có mặt trong `release_step_20260930_v2` và `release_staging_20260910`).

---

## 3. Chi tiết Endpoints

### EP-01: GET `/admin/webhook-relay/config`

- **Controller**: `App\Http\Controllers\Admin\WebhookRelayController@getConfig` — `WebhookRelayController.php:70-83`
- **Service**: `WebhookRelayService::getConfig()` — `app/Services/WebhookRelay/WebhookRelayService.php:83-108`
- **Mô tả**: nạp cấu hình của **cả hai kênh** khi mở màn (gọi đúng 1 lần trong `mounted()` → `loadConfig()`, `webhook-relay.js:131-176`). Trả secret **đã mask** (chỉ kênh LME) và mốc 「最終更新」 vừa được đóng cho cả 2 kênh.
- **Liên kết UI**: SCR-WHR-01 / SCR-WHR-02 — khởi tạo toàn trang: switch 「転送の状態」 + ô 「転送先URL」 của 2 tab, ô 「署名シークレット」 (tab 「L Messageデータ転送」), nhãn 「最終更新」 của card 「転送エラー」. Thành công → JS gọi tiếp EP-04 cho tab 1 (`webhook-relay.js:168`).
- **Side effects (GET có ghi DB)** — Mức tin cậy Cao:
  1. `ensureSecret()` (`WebhookRelayService.php:435-494`): bot chưa có `signing_secret` ⇒ trong transaction + `SELECT … FOR UPDATE` tạo dòng `webhook_relay_setting` (hoặc update dòng chưa có secret) với `signing_secret = Crypt::encrypt(whsec_…)`, `secret_generated_at = now()`; ghi log audit `[action=init-secret]`. Đã có secret ⇒ chỉ đọc.
  2. `touchLastUpdatedAt($botId, [1, 2])` (`:293-339`): **mỗi lần mở màn** `UPDATE webhook_relay_setting SET errors_refreshed_at = now(), notify_errors_refreshed_at = now(), updated_at = now() WHERE bot_id = ?` + log `[action=update]`.

#### Request Parameters

Không có. `bot_id` lấy từ `session('current_bot_id')` (`getBotId()`, `app/Helpers/functions.php:389-393`), **không nhận từ request** (`WebhookRelayController.php:214-216`).

#### Request mẫu
```
GET /admin/webhook-relay/config
X-Requested-With: XMLHttpRequest
```

#### Response mẫu (thành công — 200)
```json
{
  "success": true,
  "data": {
    "last_updated_at": { "1": "2026/10/23 10:32", "2": "2026/10/23 10:32" },
    "channels": {
      "1": { "is_enabled": true,  "endpoint_url": "https://example.com/line-webhook" },
      "2": { "is_enabled": false, "endpoint_url": null,
             "secret_masked": "whsec_••••••••••••••••••••••••••••••••" }
    },
    "has_secret": true
  }
}
```
- Khoá `channels` / `last_updated_at` là số kênh (`1` = LINE, `2` = LME) — PHP mảng khoá 1,2 ⇒ JSON object.
- `secret_masked` = 6 ký tự đầu + `•` cho phần còn lại (`maskSecret`, `WebhookRelayService.php:499-511`; `WebhookRelaySetting::SECRET_MASK_VISIBLE_LENGTH = 6`). Vì tiền tố `whsec_` dài đúng 6 ký tự nên **bản mask không lộ ký tự ngẫu nhiên nào**.
- `has_secret = !empty(signing_secret)` (`:86`) — có thể `true` trong khi `secret_masked = null` nếu giải mã thất bại (đổi `APP_KEY`) — xem `logic-spec.md` BUG-01.
- Bot chưa từng lưu: `is_enabled = false`, `endpoint_url = null` (dòng mới chỉ có secret, `:432-433`).

#### Response lỗi
| HTTP | Điều kiện | Response body |
|------|----------|--------------|
| 403 | Không có bot trong session, không phải owner/Staff đã chấp nhận, hoặc Staff chưa được cấp quyền màn `webhookRelay` (`WebhookRelayController.php:214-232`) | `{"success":false,"error_code":"PERMISSION_DENIED","message":"この権限は許可されていません。"}` |
| 401 | Chưa đăng nhập, request AJAX (`AdminAccess.php:95-106`) | `{"success":false,"data":null,"message":"ログインが必要です。","msg":"ログインが必要です。"}` |
| 403 | Đăng nhập nhưng `users.role` ∉ {0,1,2,-1} (`AdminAccess.php:23,96-99`) | `{"success":false,"data":null,"message":"この操作を行う権限がありません。","msg":"…"}` |
| 200 (`success:false`) | `remember_token` session lệch DB (đổi mật khẩu ở nơi khác) — `CheckRememberToken.php:26-40` | `{"result":false,"status":false,"success":false,"message":"ログイン情報が変更されましたので、再度ログインしてください。",…}` |
| 302 | Staff dạng `is_bot_invite` mà route `webhookRelay.config` **không có** trong whitelist `getRouterBotInvite()` (chưa chạy command `access-feature:webhook-relay`) — middleware **xoá luôn** `current_bot_id` khỏi session (`AdminAccess.php:61-72`) | Redirect `/admin/home` |
| 500 | `QueryException` khác lỗi trùng khoá 1062 (`WebhookRelayService.php:473-479`) | Exception Handler mặc định |

FE: `success=false` hoặc lỗi khác 403 → toast 「エラーが発生しました。」; 403 → toast 「この権限は許可されていません。」 rồi sau 3 giây chuyển `/admin/home` (`webhook-relay.js:149-151, 583-593`).

---

### EP-02: POST `/admin/webhook-relay/save`

- **Controller**: `WebhookRelayController@save` — `WebhookRelayController.php:89-112`
- **Form Request**: `App\Http\Requests\WebhookRelaySaveRequest` (`app/Http/Requests/WebhookRelaySaveRequest.php`)
- **Service**: `WebhookRelayService::save()` — `WebhookRelayService.php:118-211`; validator `WebhookUrlValidator::validate()` — `app/Services/WebhookRelay/WebhookUrlValidator.php:35-71`
- **Mô tả**: lưu **chỉ** kênh của tab đang mở (`channel`) — cột của kênh còn lại **không bị đụng** (`WebhookRelayService.php:141-145`). Lần lưu đầu tiên của bot (chưa có dòng) **sinh luôn secret** dù đang lưu kênh LINE hoặc lưu ở trạng thái TẮT (`:157-165`).
- **Liên kết UI**: SCR-WHR-01 / SCR-WHR-02 — nút 「保存する」 ở footer card 「転送先設定」 (`index.blade.php:115-117`), áp cho tab đang đứng (「LINE公式アカウントデータ転送」 hoặc 「L Messageデータ転送」).

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `channel` | Body (form) | Integer | Có | `1` = 「LINE公式アカウントデータ転送」, `2` = 「L Messageデータ転送」 | `required\|integer\|in:1,2` (`WebhookRelaySaveRequest.php:33`) |
| `is_enabled` | Body | Boolean (`0`/`1`) | Có | Switch 「転送の状態」 (「転送中」/「停止中」) | `required\|boolean` (`:35`) |
| `endpoint_url` | Body | String / null | Không | 「転送先URL」 | Form Request: `nullable\|string` (`:34`). Luật nghiệp vụ ở `WebhookUrlValidator` (bảng dưới) |
| `_token` / header `X-CSRF-TOKEN` | Header | String | Có | CSRF — JS gắn từ `<meta name="csrf-token">` (`webhook-relay.js:23-30`) | `VerifyCsrfToken` (route **không** nằm trong `$except`, `VerifyCsrfToken.php:14-54`) |

Luật của 「転送先URL」 — chạy theo đúng thứ tự, dừng ở lỗi đầu tiên (`WebhookUrlValidator.php:35-71`). Chuỗi đã `trim()` (cộng thêm middleware toàn cục `TrimStrings` + `ConvertEmptyStringsToNull`, `Kernel.php:24-25`):

| # | Luật | `error_code` | Thông điệp JP (`WebhookRelayService::ERROR_MESSAGES`, `:34-43`) | Dòng |
|---|------|-------------|--------------------------------|------|
| 1 | Rỗng: lỗi **chỉ khi** `is_enabled = 1`; tắt + rỗng ⇒ hợp lệ, lưu `NULL` | `URL_REQUIRED` | 「転送先URLを入力してください。」 | `:39-41` |
| 2 | Phải bắt đầu đúng chuỗi `https://` (phân biệt hoa thường) | `URL_NOT_HTTPS` | 「httpsで始まるURLを入力してください。」 | `:43-45` |
| 3 | `mb_strlen` ≤ 1024 | `URL_TOO_LONG` | 「転送先URLは1024文字以内で入力してください。」 (⏳ chuỗi tạm, TODO QA-001) | `:47-49` |
| 4 | Không chứa ký tự trắng (kể cả U+3000) | `URL_NOT_ALLOWED` | 「このURLは転送先に指定できません。」 (⏳ chuỗi tạm) | `:55-57` |
| 5 | `filter_var(FILTER_VALIDATE_URL)` | `URL_NOT_ALLOWED` | như trên | `:62-64` |
| 6 | Host: IP literal hoặc tên miền RFC 1123 `^[A-Za-z0-9]([A-Za-z0-9\-.]*[A-Za-z0-9])?$` | `URL_NOT_ALLOWED` | như trên | `:89-97` |
| 7 | Cổng: không ghi hoặc **= 443** | `URL_NOT_ALLOWED` | như trên | `:83-86` |
| 8 | **Không được là webhook của chính LME** (#44660): chuẩn hoá path (decode `%xx`, đổi `\` / `%5C` → `/`, gộp `//` liền nhau, rút gọn đoạn `.` / `..` không vượt gốc) rồi so khớp theo **ranh giới đoạn path** — path chứa `/line/callback/add` ⇒ từ chối. Áp cho **mọi domain**, **mọi `bot_id`**, **không phân biệt hoa/thường**; chạy **sau** kiểm cú pháp/host/cổng và **trước** DNS/SSRF | `URL_NOT_ALLOWED` | 「このURLは転送先に指定できません。」 (⏳ chuỗi tạm) | `WebhookUrlValidator.php` `isLmeWebhookUrl()` (nhánh `ai_studio_fixbug_44660` @`676e01b687`, #44660 + bug con #44843) |
| 9 | Phân giải DNS (A + AAAA, fallback `gethostbyname`) phải ra ≥ 1 IP (**fail-closed**) | `URL_NOT_ALLOWED` | như trên | `:104-107, 124-152` |
| 10 | **Mọi** IP phân giải ra phải "public" (`FILTER_FLAG_NO_PRIV_RANGE \| FILTER_FLAG_NO_RES_RANGE`) | `URL_NOT_ALLOWED` | như trên | `:109-113, 158-165` |

Luật 2–10 chạy **cả khi kênh đang tắt** nếu ô URL không rỗng. Hai kênh **được phép trùng URL** (`WebhookRelayService.php:124-125`). Phía client chỉ kiểm luật 1–2 (`webhook-relay.js:273-291`) — luật 8 (webhook LME) **chỉ** có ở server, màn không chặn trước khi gửi.

> ⚠ Luật 10 có lỗ hổng: IPv4-mapped IPv6 (`https://[::ffff:127.0.0.1]/`) và các dải `100.64.0.0/10`, `198.18.0.0/15`, `224.0.0.0/4` **lọt qua** — đã kiểm bằng PHP 7.2 CLI cục bộ. Xem `logic-spec.md` SEC-03.

> ⚠ Luật 8 (webhook LME) được thêm ở #44660 — số dòng chính xác trong `WebhookUrlValidator.php` **chưa reverse-engineer vào spec này**, vị trí trong thứ tự luật lấy theo bàn giao dev (journal #149214 / #150058). Bản đầu (`3ddf9d4c`) chưa rút gọn `.` / `..` ⇒ sót `/line/./callback/add` (bug con #44843), đã vá ở `4d8510dcf8` và giữ ở HEAD `676e01b687`. Phạm vi chặn theo **mọi domain + mọi vị trí path** còn **chờ PO chốt** (Studio REQ-008) — tool ngoài có path chứa `/line/callback/add` cũng bị chặn.

#### Request mẫu
```
POST /admin/webhook-relay/save
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-CSRF-TOKEN: {token}
X-Requested-With: XMLHttpRequest

channel=2&endpoint_url=https%3A%2F%2Fexample.com%2Flme-events&is_enabled=1
```

#### Response mẫu (thành công — 200)
```json
{
  "success": true,
  "data": {
    "channel": 2,
    "is_enabled": true,
    "endpoint_url": "https://example.com/lme-events",
    "has_secret": true,
    "secret_masked": "whsec_••••••••••••••••••••••••••••••••"
  }
}
```
`is_enabled` / `endpoint_url` đọc lại từ DB sau khi ghi (`WebhookRelayService.php:199-210`). FE: toast 「保存しました」, ở lại màn, cập nhật `savedState`, xoá plaintext secret đang cache (`webhook-relay.js:319-331`).

#### Response lỗi
| HTTP | Điều kiện | Response body |
|------|----------|--------------|
| 422 | Form Request fail (`channel` sai, thiếu `is_enabled`, `endpoint_url` không phải chuỗi) — `WebhookRelaySaveRequest.php:42-52` | `{"success":false,"errors":[{"field":"request","error_code":"INVALID_PARAM","message":"エラーが発生しました。"}]}` |
| 422 | Vi phạm luật URL (bảng trên) — `WebhookRelayController.php:107-109` | `{"success":false,"errors":[{"field":"endpoint_url","error_code":"URL_NOT_HTTPS","message":"httpsで始まるURLを入力してください。"}]}` |
| 403 | Như EP-01 (`PERMISSION_DENIED`) | như EP-01 |
| 419 | Thiếu/sai CSRF token | Trang lỗi Laravel `TokenMismatchException` |
| 401 / 200 `success:false` / 302 | Như EP-01 (AdminAccess / CheckRememberToken / whitelist Staff) | như EP-01 |
| 500 | `QueryException` khác 1062; trùng khoá 1062 thì **chạy lại transaction 1 lần** (`WebhookRelayService.php:172-183`) | Exception Handler |

> Thứ tự kiểm: Form Request chạy **trước** controller ⇒ người **không có quyền** gửi payload sai vẫn nhận **422** chứ không phải 403 (`WebhookRelaySaveRequest.php:24-28` luôn `true`). Mức ảnh hưởng thấp.
>
> FE hiển thị: lỗi `INVALID_PARAM`/`field=request` → toast; lỗi khác → tô đỏ dưới ô 「転送先URL」 của tab hiện tại (`webhook-relay.js:346-363`).

---

### EP-03: POST `/admin/webhook-relay/regenerate-secret`

- **Controller**: `WebhookRelayController@regenerateSecret` — `WebhookRelayController.php:115-130`
- **Service**: `WebhookRelayService::regenerateSecret()` — `WebhookRelayService.php:217-251`
- **Mô tả**: sinh secret mới `whsec_` + 32 ký tự base62, ghi đè `signing_secret` (mã hoá) + `secret_generated_at`. **Secret cũ hết hiệu lực ngay, không ân hạn** theo web (`:213-215`) — ⚠ job cache cấu hình 60s nên kênh 2 còn gửi secret cũ tối đa ~60s (`linect-service/…/WebhookRelaySettingManager.java:28`; job-spec R-06). Không trả plaintext (`secret_plain: null`, `:245-247`). Audit `[action=regenerate-secret]` (`:234-239`). **Không** khoá dòng / không transaction (1 câu UPDATE).
- **Liên kết UI**: SCR-WHR-02 (tab 「L Messageデータ転送」) — nút 「再生成」 cạnh ô 「署名シークレット」 (`index.blade.php:100-103`) → hộp xác nhận SCR-WHR-03. FE bắt buộc `window.confirm('署名シークレットを再生成します。外部ツール側の設定も更新が必要です。よろしいですか？')` (`webhook-relay.js:101, 460`); nút disabled khi `!hasSecret || isRegenerating`.

#### Request Parameters
Không có tham số nghiệp vụ (chỉ CSRF token). Không cần tham số kênh — secret chỉ thuộc kênh LME.

#### Request mẫu
```
POST /admin/webhook-relay/regenerate-secret
X-CSRF-TOKEN: {token}
X-Requested-With: XMLHttpRequest
```

#### Response mẫu (thành công — 200)
```json
{
  "success": true,
  "data": {
    "secret_masked": "whsec_••••••••••••••••••••••••••••••••",
    "secret_plain": null,
    "regenerated_at": "2026-10-23T10:35:12+09:00"
  }
}
```
FE: cập nhật `secretMasked`, xoá `secretPlain` đang cache; lần bấm xem/copy kế tiếp gọi EP-05 (`webhook-relay.js:466-478`).

#### Response lỗi
| HTTP | Điều kiện | Response body |
|------|----------|--------------|
| 422 | Bot chưa có dòng `webhook_relay_setting` (`WebhookRelayService.php:219-223`) | `{"success":false,"errors":[{"field":"secret","error_code":"INVALID_PARAM","message":"エラーが発生しました。"}]}` |
| 403 / 401 / 419 / 302 | Như EP-02 | như EP-02 |

---

### EP-04: GET `/admin/webhook-relay/errors`

- **Controller**: `WebhookRelayController@getErrors` — `WebhookRelayController.php:136-174`
- **Service**: `WebhookRelayService::getErrors()` — `WebhookRelayService.php:263-280`; repo `WebhookRelayErrorRepository::getLatestForBotChannel()` — `app/Repositories/Eloquents/WebhookRelayErrorRepository.php:21-29`; resource `WebhookRelayErrorResource` — `app/Http/Resources/WebhookRelayErrorResource.php:17-31`
- **Mô tả**: 100 bản ghi lỗi gần nhất của **một** kênh:
  `SELECT id, occurred_at, event_type, error_code, http_status FROM webhook_relay_error WHERE bot_id = ? AND channel = ? ORDER BY occurred_at DESC, id DESC LIMIT 100` — không phân trang, không lọc thêm. Bảng do **job Java ghi**, web chỉ đọc.
  `refresh=1` ⇒ đóng mốc 「最終更新」 = giờ server cho đúng kênh đó (UPDATE `errors_refreshed_at` hoặc `notify_errors_refreshed_at`; bot chưa có dòng thì INSERT dòng chỉ chứa mốc — `:310-326`). Không có `refresh` ⇒ chỉ đọc mốc đang lưu.
- **Liên kết UI**: SCR-WHR-01 / SCR-WHR-02 — card 「転送エラー」 (`index.blade.php:121-173`):
  - sau EP-01 (tab 1, không `refresh`) — `webhook-relay.js:168`;
  - lần đầu đổi sang tab chưa nạp (không `refresh`) — `:224-226`;
  - nút 「最新に更新」 (`refresh=1`) — `index.blade.php:136-139`, `webhook-relay.js:492-494`.

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `channel` | Query | Integer | Có | `1` = LINE, `2` = LME | `filter_var(FILTER_VALIDATE_INT)` (chỉ nhận chuỗi số nguyên trọn vẹn — `"1; DROP"`, `"1abc"`, `""`, `"01"` đều bị từ chối) + `in_array([1,2], strict)` — `WebhookRelayController.php:152-163` (bug #40533) |
| `refresh` | Query | Boolean | Không | `1` chỉ khi bấm 「最新に更新」 | `FILTER_VALIDATE_BOOLEAN` (`:168`); giá trị lạ ⇒ `false` |

#### Request mẫu
```
GET /admin/webhook-relay/errors?channel=1&refresh=1
X-Requested-With: XMLHttpRequest
```

#### Response mẫu (thành công — 200)
```json
{
  "success": true,
  "data": {
    "channel": 1,
    "items": [
      { "id": 9812, "occurred_at": "2026/10/22 15:04:05", "event_type": "message",
        "reason": "タイムアウト（10秒）", "http_status": null },
      { "id": 9790, "occurred_at": "2026/10/22 14:58:41", "event_type": "follow",
        "reason": "接続できませんでした", "http_status": null }
    ],
    "last_updated_at": "2026/10/23 10:36"
  }
}
```
- `occurred_at`: `Y/m/d H:i:s`, không kèm thứ (`WebhookRelayErrorResource.php:23`).
- `event_type`: kênh 1 = `type` LINE nguyên văn; kênh 2 = `tag` \| `friend_info` (`:24-25`).
- `reason`: chuỗi JP map từ `error_code` (`WebhookRelayError::reasonText`, `app/Models/WebhookRelayError.php:41-62`); mã lạ ⇒ 「その他のエラー」.
- `http_status`: chuỗi hoặc `null` (FE hiển thị 「—」, `index.blade.php:162-164`).
- `last_updated_at`: chuỗi `Y/m/d H:i` hoặc `''` (chưa có mốc ⇒ FE giữ 「—」).

Bảng `error_code` → 「エラー内容」 (`WebhookRelayError.php:41-49`):

| `error_code` | 「エラー内容」 | `http_status` (theo code job) |
|---|---|---|
| `CONNECT_FAILED` | 「接続できませんでした」 | NULL |
| `NOT_FOUND` | 「転送先が見つかりません」 | 404 |
| `UNAUTHORIZED` | 「認証エラー」 | 401 / 403 |
| `TIMEOUT` | 「タイムアウト（10秒）」 — **khớp** timeout thật của job (10 giây/pha — `linect-service/…/Constants.java:239`, `WebhookRelayApiClient.java:63-68`) | **NULL** khi job hết giờ chờ; 408 / 504 chỉ khi bên nhận trả về |
| `SERVER_ERROR` | 「転送先でエラーが発生しました」 | 5xx trừ 503, 504 |
| `UNAVAILABLE` | 「転送先が一時的に応答できません」 | 503 |
| `HTTP_ERROR` / `UNKNOWN` / `INVALID_PAYLOAD` / mã lạ → khoá `OTHER` | 「その他のエラー」 (⏳ chuỗi tạm C-04) | mã thật (`HTTP_ERROR`) / NULL. Job **không bao giờ ghi `OTHER`** |

Cột `http_status` đã đối chiếu code Java `linect-service/…/WebhookRelayApiClient.java:128-190` (Mức tin cậy: **Cao**). Hợp đồng `src/web/sns-line/docs/api/webhook-relay-outbound-contract.md:231, 254, 264-275` (timeout 15s, TIMEOUT ghi 408) **không khớp code job** — xem `db/db-mapping.md` X-01, X-02.

#### Response lỗi
| HTTP | Điều kiện | Response body |
|------|----------|--------------|
| 422 | `channel` thiếu / không phải số nguyên trọn vẹn / ngoài {1,2} | `{"success":false,"errors":[{"field":"channel","error_code":"INVALID_PARAM","message":"エラーが発生しました。"}]}` |
| 403 / 401 / 302 | Như EP-01 | như EP-01 |

---

### EP-05: GET `/admin/webhook-relay/secret`

- **Controller**: `WebhookRelayController@getSecret` — `WebhookRelayController.php:180-195`
- **Service**: `WebhookRelayService::getPlainSecret()` — `WebhookRelayService.php:357-374`
- **Middleware thêm**: `throttle:10,1` (`routes/web.php:668-669`) — tối đa 10 request/phút; Laravel 5.5 gom theo user đã đăng nhập (`sha1(user id)`).
- **Mô tả**: giải mã và trả **plaintext** secret. Chính sách 「always-viewable」 (D-03 / QA-spec-004): xem lại được bất cứ lúc nào; **mỗi lần gọi ghi audit** `[action=view-secret]` (user_id, bot_id, ip). Response gắn header `Cache-Control: no-store` (`:194`).
- **Liên kết UI**: SCR-WHR-02 (tab 「L Messageデータ転送」) — icon con mắt (xem/ẩn) và icon copy cạnh 「署名シークレット」 (`index.blade.php:94-99`). Chỉ gọi ở **lần đầu** cần plaintext; sau đó dùng giá trị cache trong state Vue (không lưu storage) — `webhook-relay.js:366-421`.

#### Request Parameters
Không có.

#### Response mẫu (thành công — 200)
```json
{ "success": true, "data": { "secret": "whsec_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" } }
```
(giá trị minh hoạ — luôn đúng 38 ký tự: `whsec_` + 32 ký tự base62)

#### Response lỗi
| HTTP | Điều kiện | Response body |
|------|----------|--------------|
| 422 | Bot chưa có dòng hoặc `signing_secret` rỗng (`WebhookRelayService.php:359-362`) | `{"success":false,"errors":[{"field":"secret","error_code":"INVALID_PARAM","message":"エラーが発生しました。"}]}` |
| 200 (`secret: null`) | Có ciphertext nhưng giải mã lỗi (đổi `APP_KEY`) — `decryptSecret()` trả `null` (`:532-547`) | `{"success":true,"data":{"secret":null}}` ⚠ BUG-01 |
| 429 | Vượt 10 request/phút | Response throttle mặc định Laravel (`Too Many Attempts.`) — Mức tin cậy Trung bình về body |
| 403 / 401 / 302 | Như EP-01 | như EP-01 |

---

### EP-06: GET `/admin/webhook-relay`

- **Controller**: `WebhookRelayController@index` — `WebhookRelayController.php:36-67`
- **View**: `resources/views/admin/webhook-relay/index.blade.php` (layout `layout.admin.main`, title 「Webhook転送」) + `public/js/admin/webhook-relay/webhook-relay.js` + `public/css/admin/webhook-relay/webhook-relay.css`
- **Mô tả**: render trang. Không đọc DB ngoài kiểm tra quyền. Truyền xuống view **một** biến `webhookRelayConfig`:
  ```json
  {
    "endpoints": { "config": ".../admin/webhook-relay/config", "save": ".../save",
                   "regenerateSecret": ".../regenerate-secret", "errors": ".../errors", "secret": ".../secret" },
    "channels": { "line": 1, "lme": 2 },
    "docsUrl": ""
  }
  ```
  `docsUrl` = `env('WEBHOOK_RELAY_DOCS_URL', '')` (`:61`) — link nút 「使い方を見る」 (⚠ gọi `env()` trong controller: khi `config:cache` sẽ luôn rỗng — BUG-02).
- **Liên kết UI**: SCR-WHR-01 — vào từ sidebar mục 「Webhook転送」 (ngay dưới 「接続設定」/「API連携」, `sidebar.blade.php:209-245`; menu hiện cho **mọi** user có bot, không lọc theo quyền).

#### Response lỗi
| HTTP | Điều kiện | Kết quả |
|------|----------|---------|
| 302 | Không có bot trong session hoặc không qua `canAccess()` (`:40-43`) | Redirect `route('adminIndex')` = `/admin/home` kèm lỗi 「この権限は許可されていません。」 |
| 302 | Chưa đăng nhập (request duyệt web) | Redirect `/logout` (`AdminAccess.php:109`) |

---

### EP-07: GET `/api/webhook-decode/{secret}` — ⚠ ENDPOINT DEBUG

- **Controller**: `App\Http\Controllers\Api\WebhookRelayDebugController@decode` — `app/Http/Controllers/Api/WebhookRelayDebugController.php:39-84`
- **Service**: `WebhookRelayService::findSettingByPlainSecret()` — `WebhookRelayService.php:390-422`; repo `WebhookRelaySettingRepository::chunkWithSecret()` — `WebhookRelaySettingRepository.php:75-82` (**không lọc `bot_id`**)
- **Route**: `routes/api.php:440-446`, ràng buộc `secret` = `[A-Za-z0-9_\-]+`, `throttle:20,1` (theo IP vì không có user).
- **Mục đích thiết kế**: hỗ trợ test tay hợp đồng giải mã secret với `linect-service` — đưa plaintext đang hiển thị, nhận lại ciphertext đang nằm trong DB.
- **Bảo vệ thiết kế**: `if (!config('app.debug')) abort(404);` — **ĐANG BỊ COMMENT** (`:49-51`). Comment ngay phía trên (`:44-48`) ghi rõ đây là bug #40764 đã sửa và "TUYỆT ĐỐI KHÔNG comment lại", nhưng commit `3f3c7ddf95` (tudv, 2026-09-10, message "comment debug") comment lại, và commit này **có trong** `release_step_20260930_v2` + `release_staging_20260910`.
- **Hệ quả**: endpoint **sống ở mọi môi trường, không auth, không session**. Mỗi request (khớp tiền tố) quét **toàn bộ** dòng có secret theo lô 500 và `Crypt::decrypt` từng dòng — O(số bot có secret).
- **Liên kết UI**: không có.

#### Request Parameters
| Param | Vị trí | Kiểu | Bắt buộc? | Mô tả | Validation |
|-------|--------|------|----------|-------|-----------|
| `secret` | Path | String | Có | Plaintext `whsec_…` | Regex route `[A-Za-z0-9_\-]+`; controller yêu cầu bắt đầu bằng `whsec_` (`:56-62`) |

#### Response mẫu (200)
```json
{
  "success": true,
  "data": {
    "bot_id": 12345,
    "plain_secret": "whsec_…",
    "signing_secret": "eyJpdiI6Ij…(ciphertext base64 ~244 ký tự)",
    "secret_generated_at": "2026-09-15 11:20:00"
  }
}
```

#### Response lỗi
| HTTP | Điều kiện | Response body |
|------|----------|--------------|
| 400 | Không bắt đầu bằng `whsec_` | `{"success":false,"code":"INVALID_SECRET_FORMAT","msg":"secret phải bắt đầu bằng \"whsec_\"."}` (thông điệp tiếng Việt, lộ ra ngoài) |
| 404 | Không dòng nào giải mã ra plaintext này | `{"success":false,"code":"SECRET_NOT_FOUND","msg":"Không có bot nào đang dùng secret này (đã bị 再生成 hoặc sai APP_KEY?)."}` |
| 404 | `secret` chứa ký tự ngoài regex | Route not found |
| 429 | > 20 request/phút/IP | Throttle mặc định |

---

## 4. Danh mục mã lỗi nghiệp vụ (shape `errors[]`)

Shape chung cho EP-02…EP-05: `{"success":false,"errors":[{"field": "...","error_code":"...","message":"..."}]}`; EP-01…EP-05 khi thiếu quyền dùng shape phẳng `{"success":false,"error_code":"PERMISSION_DENIED","message":"..."}` (`WebhookRelayController.php:224-228`).

| `error_code` | `field` | HTTP | Thông điệp JP | Nơi sinh |
|---|---|---|---|---|
| `URL_REQUIRED` | `endpoint_url` | 422 | 「転送先URLを入力してください。」 | `WebhookUrlValidator.php:40` |
| `URL_NOT_HTTPS` | `endpoint_url` | 422 | 「httpsで始まるURLを入力してください。」 | `:44` |
| `URL_TOO_LONG` | `endpoint_url` | 422 | 「転送先URLは1024文字以内で入力してください。」 (tạm) | `:48` |
| `URL_NOT_ALLOWED` | `endpoint_url` | 422 | 「このURLは転送先に指定できません。」 (tạm) | `:56, 63, 67` |
| `INVALID_PARAM` | `request` / `channel` / `secret` | 422 | 「エラーが発生しました。」 | `WebhookRelaySaveRequest.php:46-50`; `WebhookRelayController.php:155-162`; `WebhookRelayService.php:222, 361` |
| `PERMISSION_DENIED` | — | 403 | 「この権限は許可されていません。」 | `WebhookRelayController.php:224-228` |
| `INTERNAL_ERROR` | — | — | 「エラーが発生しました。」 | Chỉ là fallback của `buildError()` (`WebhookRelayService.php:566-575`), không có đường nào sinh trực tiếp |

---

## 5. Middleware phân tích

| Middleware | Class / nguồn | Áp dụng cho | Chức năng |
|-----------|---------------|------------|----------|
| `web` (nhóm) | `Kernel.php:35-43` | EP-01…EP-06 | EncryptCookies, StartSession, ShareErrorsFromSession, **VerifyCsrfToken**, SubstituteBindings. `/admin/webhook-relay/*` **không** nằm trong `$except` (`VerifyCsrfToken.php:14-54`) ⇒ EP-02/EP-03 (POST) được bảo vệ CSRF |
| `NotifyChatworkRequestTimeSlow` | `routes/web.php:84` | EP-01…EP-06 | Cảnh báo Chatwork khi request chậm (EP-02 có tra DNS đồng bộ — có thể kích hoạt) |
| `admin_access` | `App\Http\Middleware\AdminAccess` (`Kernel.php:69`) | EP-01…EP-06 | Yêu cầu đăng nhập + `users.role ∈ {0,1,2,-1}` (`AdminAccess.php:23`); ghi `user_access_bot` lần đầu trong ngày cho Staff (`:35-55`); Staff dạng `is_bot_invite` chỉ được vào route có trong `getRouterBotInvite()` (`:61-73`) — cần 6 dòng `access_feature` do command `access-feature:webhook-relay` tạo; AJAX chưa đăng nhập → 401/403 JSON (`:95-107`) |
| `https_protocol` | `HttpsProtocol` (`Kernel.php:75`) | EP-01…EP-06 | **No-op** — thân hàm redirect HTTPS bị comment (`HttpsProtocol.php:18-20`) |
| `check_remember_token` | `CheckRememberToken` (`Kernel.php:83`) | EP-01…EP-06 | So `session('remember_token')` với `users.remember_token_reset_pass`; lệch ⇒ logout; AJAX nhận **200** `success:false` (`CheckRememberToken.php:26-40`) |
| `throttle:10,1` | `ThrottleRequests` | EP-05 | Giới hạn xem plaintext secret 10 lần/phút/user |
| `api` (nhóm) | `Kernel.php:45-48` | EP-07 | Chỉ `bindings` — không session/auth/CSRF |
| `throttle:20,1` | `ThrottleRequests` | EP-07 | 20 request/phút/IP |

Kiểm tra quyền **trong controller** (không phải middleware) cho EP-01…EP-06: `resolveBotId()` / `canAccess()` (`WebhookRelayController.php:214-257`) — chi tiết ở `logic-spec.md` mục 9.

---

## 6. Liên kết UI ↔ API

> Mã SCR theo `ui/ui-spec.md`: **SCR-WHR-01** = tab 「LINE公式アカウントデータ転送」 (mặc định), **SCR-WHR-02** = tab 「L Messageデータ転送」, **SCR-WHR-03** = confirm tái tạo secret, **SCR-WHR-04** = confirm rời tab khi chưa lưu. Hai tab là **hai kênh trên cùng một trang** (`activeTab` 1/2, luôn khởi tạo = 1, không nhớ tab — `index.blade.php:12-13`, `webhook-relay.js:35`), không phải 2 route.

| Màn hình / khu vực | Action trên UI | Endpoint | Ghi chú |
|---------|--------|----------|---------|
| SCR-WHR-01 (sidebar 「Webhook転送」) | Mở trang / F5 | EP-06 | Sai quyền → redirect `/admin/home` |
| SCR-WHR-01 / 02 — toàn trang | `mounted()` | EP-01 → EP-04 (`channel=1`) | EP-01 **ghi DB**: sinh secret lần đầu, đóng mốc 「最終更新」 cả 2 kênh |
| SCR-WHR-01 ↔ SCR-WHR-02 (thanh tab), SCR-WHR-04 | Đổi tab lần đầu sang tab chưa nạp | EP-04 (`channel` của tab mới, không `refresh`) | Có thay đổi chưa lưu ⇒ SCR-WHR-04 `confirm('保存していない変更があります。タブを切り替えると変更内容は破棄されます。よろしいですか？')` (chuỗi chưa được BA chốt, `webhook-relay.js:102-104`); không gọi API |
| SCR-WHR-01 / 02 — card 「転送先設定」, nút 「保存する」 | Lưu kênh của tab đang mở | EP-02 | Client validate rỗng-khi-bật + `https://` trước |
| SCR-WHR-02 — 「署名シークレット」 icon con mắt | Xem plaintext | EP-05 (lần đầu) | Lần sau dùng cache trong state |
| SCR-WHR-02 — 「署名シークレット」 icon copy | Copy plaintext | EP-05 (nếu chưa cache) | Toast 「コピーしました」/「コピーに失敗しました」 |
| SCR-WHR-02 — nút 「再生成」 → SCR-WHR-03 | Tái tạo secret | EP-03 | Native `confirm` bắt buộc; Huỷ ⇒ không gọi |
| SCR-WHR-01 / 02 — card 「転送エラー」, nút 「最新に更新」 | Nạp lại lỗi tab đang đứng | EP-04 (`refresh=1`) | Đóng mốc 「最終更新」 chỉ kênh đó |
| SCR-WHR-01 / 02 — bảng 「転送エラー」, cột 「発生日時」 | Sort | — | Sort **client-side** trên tối đa 100 dòng đã nạp (`webhook-relay.js:560-578`) |
| SCR-WHR-01 — header, nút 「使い方を見る」 | Mở tài liệu | — | `window.open(docsUrl)`; `docsUrl` rỗng ⇒ không làm gì (TODO QA-spec-002) |
| (không có UI) | Test tay hợp đồng secret | EP-07 | Endpoint debug — phải khoá/xoá trước production |

---

## 7. Điểm chưa rõ / cần xác minh (phần API)

| # | Nội dung | Mức tin cậy hiện tại |
|---|---------|---------------------|
| 1 | Production có đang chạy commit `3f3c7ddf95` (EP-07 mở) hay không — cần kiểm tra bản deploy thực tế | Cao (về code), chưa rõ về triển khai |
| 2 | Chuỗi JP cho `URL_TOO_LONG`, `URL_NOT_ALLOWED`, 「その他のエラー」, câu confirm rời tab — đều đang tạm. (「タイムアウト（10秒）」: **đã phân xử — khớp code job 10s**, TODO C-05 dựa trên tài liệu lỗi thời) | Cao (đã có TODO trong code) |
| 3 | Body response 429 của throttle Laravel 5.5 (thư mục `vendor/` không có trong repo clone) | Trung bình |
| 4 | ~~Giá trị `http_status` do job ghi cho từng `error_code`~~ — **Đã đóng**: đối chiếu code Java (`WebhookRelayApiClient.java:128-190`, job-spec §6.4) | Cao |
