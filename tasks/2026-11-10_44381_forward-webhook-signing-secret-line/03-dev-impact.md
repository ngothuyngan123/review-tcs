# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #44381 bằng `/new-task` (2026-11-10). Redmine **không có** section "Đánh giá ảnh hưởng" theo format chuẩn (1./2./3./4.1/4.2/4.3) trong `description` — ticket này đi qua 3 vòng kế hoạch + Dev handoff (Journal #149841 → #153437). Nội dung dưới đây **tổng hợp từ vòng cuối** (Journal #153437, 09/11 17:25 — xem nguyên văn ở [01-bug-task.md](01-bug-task.md)), có đối chiếu các vòng trước để không bỏ sót impact đã nêu nhưng không còn đúng ở vòng cuối (ghi rõ trong Ghi chú).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI) — assignee Redmine: Đoàn Thị Bích Hảo (`haodtb`) |
| Commit / Pull Request | sns-line (web) commit `6c2b2ccb881274da1030e97863c660dce41ae534` · linect-service (job) commit `b7b30713aa1880aa43e5c8964c6521a26f5fa2cd` — không có PR link trong journal |
| Branch | `ai_studio_implement_44381` (sns-line nhánh gốc `release_step_20260930_v2`; linect-service nhánh gốc `release-t09-2026`) |
| Ngày submit đánh giá | 2026-11-09 (Journal #153437, 17:25 — vòng cuối) |
| Auto-filled | 2026-11-10 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại toàn bộ journal Dev handoff (đặc biệt Journal #153437 — vòng cuối) và xác nhận bảng 4.1/4.2/4.3 dưới đây không sót impact.

---

## 1. Nguyên nhân

Kênh LINE (`LINE公式アカウントデータ転送`) của màn `Webhook転送` **không có secret ký riêng** → job forward webhook phía kênh LINE không gửi được header xác thực (`X-Lme-Signature`) cho bên nhận, khác với kênh L Message (`L Messageデータ転送`) đã có secret ký (`signing_secret`) từ trước (feature cũ #40475/#40543).

Trong quá trình triển khai, Dev còn phát hiện thêm 2 vấn đề kỹ thuật phụ cần sửa cùng:
- Race condition: 2 request đồng thời trên bot **chưa có dòng cấu hình** → MySQL deadlock (1213) / trùng khoá (1062) → lỗi `500` (bug `#45605`/`#5102`/`#5141`).
- API `再生成` (regenerate secret) khi bot chưa có dòng cấu hình trả `422` thay vì tự tạo cấu hình rồi sinh secret (bug `#45606`/`#5102`).
- Cảnh báo log khi kênh LINE gửi không có chữ ký bị chặn 1 lần/bot/giờ — sai so với spec yêu cầu log WARN **mỗi lần** gửi/retry (bug `#5455`).

## 2. Cách fix

**Thiết kế cuối (chốt 09/11, theo quyết định của Tu — người phụ trách):**

- **DB**: thêm 2 cột `line_signing_secret` (varchar 1024, NULL) và `line_secret_generated_at` (datetime, NULL) vào bảng `webhook_relay_setting` (migration `2026_10_30_000000_add_line_signing_secret_to_webhook_relay_setting.php`).
- **Màn `Webhook転送` tab `LINE公式アカウントデータ転送`**: thêm khối `署名シークレット` (mask `whsec_…`, nút xem/mắt, copy, `再生成` có confirm) — độc lập hoàn toàn với tab `L Message` (tách theo kênh qua param `channel`: `1`=LINE, `2`=L Message). Khối luôn hiện, 3 nút luôn bật kể cả khi `転送の状態` tắt.
- **5 API JSON** của màn (`EP-01` GET `/admin/webhook-relay/config`, `EP-02` POST `/admin/webhook-relay/save`, `EP-03` POST `/admin/webhook-relay/regenerate-secret`, `EP-04` GET `/admin/webhook-relay/errors`, `EP-05` GET `/admin/webhook-relay/secret`):
  - `EP-03`/`EP-05` bắt buộc param `channel` (1 hoặc 2); thiếu/sai → `422 「エラーが発生しました。」`.
  - Bot **chưa có dòng cấu hình** gọi `EP-03`/mở màn (`EP-01`)/lưu lần đầu (`EP-02`) → **tạo dòng cấu hình kèm sinh đủ 2 secret trước**, rồi mới xử lý tiếp (sinh lại kênh được chọn nếu là `EP-03`) → trả **`200`** (không còn `422`/`500`).
  - Race-condition fix: tạo dòng **trước** (ngoài transaction), chỉ `lock` dòng đã tồn tại; gặp deadlock (`1213`)/trùng khoá (`1062`) → retry tối đa 3 lần. Áp dụng cho mở màn, lưu lần đầu, `再生成`.
  - Lỗi ngoài dự kiến ở cả 5 API → `500 INTERNAL_ERROR` (log + Chatwork, không lộ SQL/secret).
  - Staff bot mời thiếu quyền → `403` JSON (qua middleware `AdminAccess`, không redirect).
- **Thuật toán ký (đổi quan trọng nhất)**: `X-Lme-Signature` = **HMAC-SHA256(body, secret)**, hex thường 64 ký tự, áp dụng cho **CẢ 2 kênh** — tức **đổi hành vi kênh L Message đang chạy production** (trước đây gửi secret thô, nay HMAC). Lần gửi đầu và mọi lần retry đều ký lại trên đúng body thực tế gửi đi.
- Kênh LINE không ký được (chưa có secret / giải mã lỗi / thiếu `LARAVEL_APP_KEY`): vẫn gửi request không header; **mỗi lần gửi/retry** ghi 1 dòng log WARN kèm bot + kênh + lý do; Chatwork báo tối đa 1 tin/bot/giờ (thiếu APP_KEY thì không Chatwork theo bot).
- Lệnh `php artisan webhook-relay:backfill-line-secret [--dry-run] [--chunk=500]`: sinh secret kênh LINE cho bot đã cấu hình `Webhook転送` trước release; chạy lại không ghi đè secret đã có; lỗi → báo Chatwork + `exit 1`.
- Log lỗi (khi endpoint trả lỗi) che giá trị chữ ký / chuỗi `whsec_…`, cắt tối đa 200 ký tự.
- Độ trễ hiệu lực secret mới sau `再生成`: tối đa **~60 giây** (job cache cấu hình 60s) — **giữ nguyên** như kênh L Message, không đổi thành realtime (quyết định Tu 09/11 — bug `#45607`/`#5103` **không phải bug**).

**Đã sửa trong vòng lặp (không còn là risk, nhưng vẫn là vùng cần test regression):**
`#45605`/`#5102`/`#5141` (deadlock/gap lock khi tạo dòng đồng thời) · `#45606`/`#5102` (422→200 khi `再生成` không có dòng) · `#5455` (WARN mỗi lần gửi/retry, không còn throttle 1/giờ cho log — chỉ Chatwork giữ throttle).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `WebhookRelayService` (`app/Services/WebhookRelay/WebhookRelayService.php`) | Tách logic theo `channel`, đổi thứ tự tạo dòng/lock + retry deadlock | Service dùng chung cho cả 2 tab — đây là nơi duy nhất gọi từ `webhook-relay.js` |
| 2 | `WebhookSignatureHelper` (Java, `threads/webhook/WebhookSignatureHelper.java`) | Đổi từ ký secret thô → HMAC-SHA256; log WARN mỗi lần không ký được | Nơi gọi: `HandleForwardLmeEventTask`, `HandleRetryWebhookRelayTask` (kênh L Message) + manager/task kênh LINE |
| 3 | `HandleForwardCallbackEventManager` / `HandleForwardCallbackEventTask` (job kênh LINE) | Gắn header HMAC theo secret kênh LINE | Caller của `WebhookSignatureHelper` cho kênh LINE |
| 4 | `HandleForwardLmeEventTask` (job kênh L Message) | Đổi từ hàm ký 1 tham số (secret thô) sang HMAC | Hành vi kênh L Message **đổi** — cần test hồi quy kỹ |
| 5 | `HandleRetryWebhookRelayTask` (job retry cả 2 kênh) | Ký lại HMAC trên body dựng lại khi retry | Đảm bảo chữ ký khớp đúng body gửi lại, không dùng body cache cũ |
| 6 | `WebhookRelayApiClient` (Java) | Gắn header `X-Lme-Signature` mới | Caller cuối cùng trước khi gửi HTTP ra ngoài |
| 7 | Entity `WebhookRelaySetting.java` (job) | Map thêm cột `line_signing_secret` | Cache setting (`findAll`, reload 60s) phụ thuộc migration đã chạy |
| 8 | `AdminAccess` middleware (PHP) | Trả `403` JSON cho route có cờ `json_api` | Middleware dùng chung — chạm luôn 3 route `ajax.monthlyBill.*` của màn `月次決済` (ngoài phạm vi chính nhưng cùng middleware) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Màn `Webhook転送` tab LINE — khối `署名シークレット` (view/copy/`再生成`) | `public/js/admin/webhook-relay/webhook-relay.js`, `resources/views/admin/webhook-relay/index.blade.php` | Direct | Feature mới hoàn toàn |
| F2 | `EP-03` POST `/admin/webhook-relay/regenerate-secret` | `WebhookRelayController.php` | Direct | Auto-tạo cấu hình khi chưa có dòng; trả `200` (trước `422`) |
| F3 | `EP-05` GET `/admin/webhook-relay/secret` (xem secret) | `WebhookRelayController.php` | Direct | Bắt buộc `channel`; thiếu/sai → `422` |
| F4 | `EP-01` GET `/admin/webhook-relay/config` (mở màn) | `WebhookRelayController.php` | Direct | Race-condition-safe; trả mask cả 2 kênh |
| F5 | `EP-02` POST `/admin/webhook-relay/save` (lưu) | `WebhookRelayController.php` | Direct | Nhánh tạo dòng mới sinh 2 secret cùng lúc |
| F6 | `EP-04` GET `/admin/webhook-relay/errors` (`転送エラー`, `最新に更新`) | `WebhookRelayController.php` | Indirect | Có thể tạo dòng cấu hình **không** secret — cần bổ sung khi mở màn sau |
| F7 | Middleware `AdminAccess` | `app/Http/Middleware/AdminAccess.php` | Direct | 403 JSON cho 5 route `Webhook転送` + 3 route `ajax.monthlyBill.*` (màn `月次決済`, dùng chung middleware — ngoài phạm vi chính) |
| F8 | Lệnh `artisan webhook-relay:backfill-line-secret` | `app/Console/Commands/BackfillWebhookRelayLineSecret.php` | Direct | Chạy tay 1 lần khi deploy; `--dry-run` chỉ đếm |
| F9 | `WebhookRelaySettingRepository` (Eloquent) | `Repositories/Eloquents/WebhookRelaySettingRepository.php` | Direct | Đổi thứ tự tạo dòng/khoá, retry deadlock tối đa 3 lần |
| F10 | Job forward kênh LINE | `webhook/HandleForwardCallbackEventManager.java`, `HandleForwardCallbackEventTask.java` | Direct | HMAC-SHA256 theo secret kênh LINE, lần đầu + retry |
| F11 | Job forward kênh L Message | `threads/webhook/HandleForwardLmeEventTask.java` | **Direct (đổi hành vi production)** | Secret thô → HMAC-SHA256 — breaking change với khách ngoài đang verify kiểu cũ |
| F12 | Job retry webhook (cả 2 kênh) | `webhook/HandleRetryWebhookRelayTask.java` | Direct | Ký lại HMAC trên body dựng lại khi retry |
| F13 | `WebhookSignatureHelper` (Java) | `threads/webhook/WebhookSignatureHelper.java` | Direct | Tính HMAC-SHA256; log WARN mỗi lần gửi/retry không ký được; Chatwork throttle 1/bot/giờ |
| F14 | `WebhookRelayApiClient` (Java) | `threads/webhook/WebhookRelayApiClient.java` | Direct | Gắn header `X-Lme-Signature` mới vào request gửi đi |
| F15 | Entity job `WebhookRelaySetting.java` | `linedb/entities/WebhookRelaySetting.java` | Direct | Map thêm cột `line_signing_secret`; cache `findAll` reload 60s phụ thuộc migration |
| F16 | Endpoint debug `/api/webhook-decode` (chỉ `APP_DEBUG`) | — | Indirect (gap đã biết) | Vẫn chỉ tra secret kênh L Message — **không** dùng để kiểm secret kênh LINE; Dev tự nêu, không fix trong task |
| F17 | `HandlePostbackTask.java` | — | Indirect | Dev liệt kê file bị sửa (5 dòng) nhưng không giải thích rõ lý do trong journal — **hỏi lại Dev nếu nghi ngờ sót impact** |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `webhook_relay_setting.line_signing_secret` (varchar 1024, NULL) | MIGRATE (ADD COLUMN) | `database/migrations/2026_10_30_000000_add_line_signing_secret_to_webhook_relay_setting.php` |
| D2 | `webhook_relay_setting.line_secret_generated_at` (datetime, NULL) | MIGRATE (ADD COLUMN) | Cùng migration D1 |
| D3 | `webhook_relay_setting` — backfill secret LINE cho bot cũ | CREATE/UPDATE | Chỉ ghi cột đang NULL/rỗng, **không đè** dữ liệu cũ; không rollback được |
| D4 | Cache setting phía job (`findAll`, reload 60s) | READ (gián tiếp) | Phụ thuộc migration đã chạy xong **trước** khi job lên — thiếu cột → job dừng forward cả 2 kênh |
| D5 | `docs/api/webhook-relay-outbound-contract.md` | UPDATE (tài liệu) | HMAC cho 2 kênh, `X-Lme-Timestamp` cho 2 kênh, trễ ≤60s — **đã cập nhật trong code**, nhưng `spec-features/FA-051` (sub-repo) có thể **chưa khớp** → đối chiếu khi review |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn `Webhook転送` tab LINE (tính năng mới) | F1, F2, F3, F4, F5, F9 | High — feature mới + nhiều API + race condition đã có 3 bug con |
| T2 | Màn `Webhook転送` tab L Message (hồi quy) | F9, F11, F13, D4 | **High** — đổi hợp đồng header đang chạy **production**, breaking change cho khách ngoài tích hợp kênh L Message |
| T3 | Job forward/retry cả 2 kênh | F10, F11, F12, F13, F14, D4 | High — core của task; sai thứ tự deploy làm dừng forward cả 2 kênh |
| T4 | Phân quyền Staff — 5 route `Webhook転送` + 3 route `ajax.monthlyBill.*` (màn `月次決済`) | F7 | Medium — side-effect ngoài phạm vi chính do dùng chung middleware |
| T5 | Danh sách `転送エラー` / `最新に更新` (EP-04) | F6 | Medium — có thể tạo dòng cấu hình thiếu secret, cần verify bổ sung khi mở màn sau |
| T6 | Lệnh backfill (vận hành 1 lần khi deploy) | F8, D3 | Medium — không rollback được, sai thứ tự chạy ảnh hưởng dữ liệu |
| T7 | Endpoint debug `/api/webhook-decode` | F16 | Low — gap đã biết, Dev không fix trong task này (nêu ở §8 nếu cần) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót — đặc biệt F17 `HandlePostbackTask.java`)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
