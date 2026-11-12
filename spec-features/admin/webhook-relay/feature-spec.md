# FA-047 — Chuyển tiếp Webhook 「Webhook転送」 (Webhook Relay)

**Mã**: FA-047 | **Portal**: Admin (LINE OA), Staff dùng chung giao diện nếu được cấp quyền | **Viết tắt màn hình**: `WHR` | **URL chính**: `GET /admin/webhook-relay` (route `webhookRelay`)
**Trạng thái tính năng**: **MỚI**, task web **#40044**, task job **#40475**; code có trên nhánh release của cả web lẫn job; **chưa xác minh đã bật trên production** (flag job mặc định TẮT — G-01) | **Trạng thái spec**: Hoàn thành **v1** (code-first) | **Ngày**: 2026-10-24

> 📎 **Hợp đồng contract-first (góc nhìn bên nhận)**: [`webhook/forward-contract-spec.md`](../../webhook/forward-contract-spec.md) — doc nhà cung cấp bản 1.0.0 / 16-09-2026 WSSJ (HTML gốc [`webhook/docs/webhook_v1_1104.html`](../../webhook/docs/webhook_v1_1104.html)). **§0 của file đó có bảng đối chiếu mâu thuẫn** với spec code-first này (quan trọng nhất: `X-Lme-Signature` doc ghi **secret thô / so sánh chuỗi** — KHỚP job thật "Phương án A", ĐÚNG hơn wording UI HMAC ở V-02). Dùng kèm khi review/write TC.

| Nguồn phân tích | Giá trị |
|-----------------|---------|
| Repo web | `src/web/sns-line` @ nhánh **`release_step_20260930_v2`**, commit **`4d9d07d159`** (task #40044 + bug fix #40520, #40528–#40531, #40533, #40728, #40762, #40763, #40764, #40792, #40888, #41030) |
| Repo job | `src/job/linect-service` @ nhánh **`release-t09-2026`**, commit **`be6ef546`** (task #40475) |
| Phương pháp | **Code-first hoàn toàn.** Session Playwright đã hết hạn nên **không có screenshot, DOM, network**. Spec dựng từ Blade (197 dòng) + JS Vue 2 (604 dòng) + CSS (148 dòng) + Controller / Service / Validator / FormRequest / Resource / Model / Repository / Migration / Artisan command (web) và Task Manager / Task / Repository / Entity / Helper (job Java) |
| Bằng chứng runtime | **Không có.** Mọi giá trị mẫu (vd `whsec_••••…`, `2026/10/23 10:32`, `https://example.com/webhook`) là **minh hoạ suy từ code**, không phải dữ liệu thật. 5/6 bảng cốt lõi **không có trong DB dump** |
| Spec con | [`ui/ui-spec.md`](ui/ui-spec.md) · [`web/api-spec.md`](web/api-spec.md) · [`web/logic-spec.md`](web/logic-spec.md) · [`job/job-spec.md`](job/job-spec.md) · [`db/db-mapping.md`](db/db-mapping.md) · [`_internal/db-hint.md`](_internal/db-hint.md) · [`_internal/shared-candidates.md`](_internal/shared-candidates.md) |
| Kiểm tra chéo | [`_internal/validation-report.md`](_internal/validation-report.md): **CẦN SỬA → ĐÃ SỬA PHẦN SPEC**. 24 vấn đề (4 Nghiêm trọng / 10 Trung bình / 10 Nhẹ), **18 đã áp dụng**, 13 mâu thuẫn đã phân xử bằng source; **6 Chờ user** (V-02, V-03, V-04 Nghiêm trọng; V-11, V-12, V-13 Trung bình) — user đã đồng ý compile tiếp, toàn bộ ghi ở §10.2 |
| Job spec | **Có** — 3 Task Manager + 1 cache manager (§7) |

**Quy ước mức tin cậy:** **Cao** = đọc trực tiếp source / migration / entity (chưa quan sát runtime). **Trung bình** = phụ thuộc component `lme-*` (submodule chưa clone), hành vi thư viện (OkHttp), cấu hình môi trường, hoặc suy luận. **Thấp** = chỉ thấy trong comment / tài liệu, không có code.

**Quy ước mã:** `SCR-WHR-xx`, `EP-xx`, `BR-xx` ở tài liệu này là mã **của dự án**. Comment source dùng hệ mã nội bộ của team dev (`SCR-01`, `BR-xx`, `QA-spec-xxx`, `D-0x`, `C-0x`…) — **không trùng nghĩa**, chỉ trích để tra chéo (bảng đối chiếu ở §12.1).

---

## 1. Tổng quan

### 1.1 ⚠ Điểm cần biết ngay

| # | Điểm | Hệ quả | Tham chiếu |
|:-:|------|-------|-----------|
| 1 | **Endpoint debug `GET /api/webhook-decode/{secret}` (EP-07) đang mở công khai** trên nhánh release: không auth, không session, không CSRF. Guard `if (!config('app.debug')) abort(404);` **bị comment** (commit `3f3c7ddf95`, 2026-09-10, "comment debug") dù comment ngay phía trên ghi "TUYỆT ĐỐI KHÔNG comment lại" | Ai có 1 plaintext secret (vd chính bên nhận webhook) tra được `bot_id` nội bộ + ciphertext + `secret_generated_at`. Mỗi request giải mã **toàn bộ** secret của mọi bot ⇒ vector DoS (chỉ throttle 20/phút/IP) | §6 EP-07, §9.2 #1, **V-03 (Chờ user)** |
| 2 | **`X-Lme-Signature` không phải chữ ký**: job gửi **chính secret thô `whsec_…`** ("Phương án A" chốt 2026-09-10). UI lại ghi 「X-Lme-Signature に署名を付与して送信します。…この値を検証すると」, hợp đồng web ghi `hex(HMAC-SHA256(body))` | Khách làm theo tài liệu (verify HMAC) sẽ **từ chối 100% request**; secret đi trong mọi request (lộ qua log/proxy phía nhận); `X-Lme-Timestamp` không được ký ⇒ không chống replay | §7.6, §9.2 #3, **V-02 (Chờ user)** |
| 3 | **Chưa nên bật flag chuyển tiếp trên production** khi còn 2 lỗ hổng hệ thống: (a) webhook LINE **không kiểm `X-Line-Signature`** ⇒ sự kiện giả được lưu và kênh 1 chuyển tiếp nguyên văn; (b) job **không chống SSRF lúc gửi** và để OkHttp **đi theo redirect** (mang theo secret) | Không sửa được bằng tài liệu; cần quyết định chặn rollout | §9.2 #2, #4, #5, #6, **V-04 (Chờ user)** |
| 4 | **Chỉ MỞ trang là đã GHI DB**: lần đầu tạo dòng `webhook_relay_setting` + sinh secret; **mọi lần** mở cập nhật `errors_refreshed_at`, `notify_errors_refreshed_at`, `updated_at`. Bấm 「最新に更新」 cũng ghi | Tester / người quét live **phải được user cho phép** trước khi mở màn trên môi trường thật (trái nguyên tắc chỉ đọc — CLAUDE.md §14). 「最終更新」 = "lần gần nhất có người xem / làm mới", **không** phải "lần có lỗi mới" | §2.2, §9.2 #30, §9.3 |
| 5 | **Web luôn bật, job có flag riêng mặc định TẮT** (`ENABLE_FORWARD_WEBHOOK_CALLBACK`, `ENABLE_FORWARD_WEBHOOK_LME` = `0`). Job đọc cấu hình qua **cache 60 giây** | Flag tắt: UI vẫn hiện 「転送中」 nhưng **không gửi gì và không có lỗi nào**. Flag bật: sự kiện trong ≤60s sau khi bật kênh bị **bỏ qua vĩnh viễn**; 「再生成」 secret thì kênh 2 còn gửi **secret cũ ≤60s** (trái cam kết 「secret cũ hết hiệu lực ngay」) | §1.6, §7.9, §9.2 #7, #12, **V-12 (Chờ user)** |
| 6 | **Phát lại lịch sử khi bật flag lần đầu**: job không có mốc bắt đầu; mọi dòng cũ của 3 bảng nguồn có `status_sync = NULL`. DB dump: 99,98% `callback_event` cũ ở **định dạng mảng** (không phải body LINE), có cả payload **Zalo / Meta**. Cột `callback_event.status_sync` + index `(status_sync, id)` **không có migration** ở cả 2 repo | Dữ liệu lịch sử / sai định dạng / của nền tảng khác có thể bị gửi ra hệ thống khách, không thu hồi được. Thiếu index ⇒ scanner full scan bảng nóng mỗi 200ms–1s | §9.2 #9, #10; G-02, G-03 |
| 7 | **Mô tả UI / hợp đồng lệch hành vi job**: 「最大3回まで再送…3回とも失敗したものだけをここに記録」 nhưng thực tế **tổng 3 lần gửi** (1 lần đầu + 2 lần thử lại), **chỉ** thử lại khi timeout / HTTP ≥ 500, lỗi khác ghi **ngay sau lần 1**; kênh 2 ghi **1 dòng lỗi cho cả lô ≤500 sự kiện**. Hợp đồng web "TIMEOUT ghi 408" nhưng job ghi `NULL` (UI 「—」) | Khách / người dùng hiểu sai mức đảm bảo giao hàng; tester kỳ vọng sai | §9.2 #14, #15; **V-11, V-13 (Chờ user)** |
| 8 | **Quyền Staff ở mức màn**: Staff được tick 「Webhook転送」 làm được **mọi** thao tác, kể cả xem plaintext và 「再生成」 secret. Menu hiện cho **mọi** user có bot (không lọc quyền); Staff không có quyền bấm vào bị đẩy về `/admin/home` **và mất luôn bot đang chọn** | Khác FA-046: ở đây Staff **cấp được quyền** (command đặt `menu_id`) | §1.4, §9.2 #29 |

### 1.2 Mục đích

Cho phép chủ LINE OA (và Staff được cấp quyền) cấu hình **chuyển tiếp dữ liệu sự kiện của bot sang URL HTTPS của công cụ bên ngoài**, qua **2 kênh độc lập**, mỗi kênh là 1 tab trên cùng 1 trang:

| | Kênh 1 — 「LINE公式アカウントデータ転送」 | Kênh 2 — 「L Messageデータ転送」 |
|---|---|---|
| Mô tả trên UI | 「LINE公式アカウントが受信したイベントを、そのまま外部ツールへ転送します。」 (`webhook-relay.js:51`) | 「エルメ内で発生したイベントを外部ツールへ転送します。」 (`:58`) |
| Giá trị `channel` | `1` (`WebhookRelaySetting::CHANNEL_LINE`) | `2` (`CHANNEL_LME`) |
| Nguồn sự kiện | Webhook LINE gửi tới LME → bảng `callback_event` (backenddb) | Thao tác **tag** (`tag_history`) và **thông tin bạn bè** (`friend_info_history`) ở bất kỳ đâu trong LME (linedb) |
| Nội dung gửi | Body webhook LINE **nguyên văn** (「加工せずそのまま」) | JSON `{"events":[…]}` do job dựng, gom lô theo bot |
| URL đích / công tắc | `endpoint_url` / `is_enabled` | `notify_endpoint_url` / `notify_is_enabled` |
| Header xác thực | **Không** (quyết định BA) | `X-Lme-Signature` = **secret thô** `whsec_…` |
| 「署名シークレット」 | Không có | Có (1 secret / bot) |
| Task Manager (job) | `HandleForwardCallbackEventManager` | `HandleForwardLmeEventManager` |

Mỗi tab gồm card 「転送先設定」 (bật/tắt + URL đích; tab 2 thêm secret) và card 「転送エラー」 (≤100 lỗi gần nhất **của chính kênh đó**). Nút 「保存する」 **chỉ lưu kênh của tab đang mở**.

**Phân chia trách nhiệm**: web **không gửi HTTP ra ngoài** và **không ghi hàng đợi**. Web chỉ (1) quản lý cấu hình + secret, (2) hiển thị lỗi do job ghi, (3) gián tiếp sinh dữ liệu nguồn qua các luồng nghiệp vụ có sẵn. Toàn bộ việc quét, gửi, thử lại, ghi lỗi do job Spring Boot đảm nhận (§7).

### 1.3 Đường vào tính năng

| Mục | Nội dung | Tin cậy |
|-----|---------|--------|
| Điểm vào | Sidebar Admin v2 (`layout/v2/admin/sidebar.blade.php`) → section 「機能関連」 → mục **「Webhook転送」** (icon SVG 3 nút nối nhau). Thứ tự thực tế: 「接続設定」 (`:177-187`) → 「API連携」 (`:189-207`, FA-046) → **「Webhook転送」** (`:209-245`). Comment code ghi "CHỐT QA-spec-001: mục nằm NGAY DƯỚI 「接続設定」", nhưng 「API連携」 (task #40041) chen vào giữa | Cao |
| Active / thu gọn | Class `active` khi `$routeCurrent == 'webhookRelay'`; sidebar thu gọn có tooltip 「Webhook転送」 | Cao |
| Điều kiện hiển thị | Chỉ khi đã chọn bot (`@if($bot)`, `:79`); **không** lọc theo quyền | Cao |
| URL | `GET /admin/webhook-relay`. 2 tab + 2 dialog native trên **1 route, 1 Vue instance** (`#webhook-relay-app`); tab không lưu vào URL / storage | Cao |
| Layout | `layout.admin.main` → sidebar v2; design system `lme-ui` (10 component: `lme-tab-horizontal`, `lme-title`, `lme-input`, `lme-switch`, `lme-status`, `lme-table`, `lme-toast`, `lme-button-default`, `lme-button-flat`, `lme-icon`) | Cao (khai báo) / Trung bình (hình dạng render) |
| Mục quyền Staff | 「Webhook転送」 trong nhóm 「システム設定」 ở màn phân quyền Staff (FA-035), đặt ngay sau 「LINE公式アカウント入れ替え」 | Cao (code) |

### 1.4 Actors

| Actor | Quyền truy cập | Thực tế với code hiện tại | Cơ sở |
|-------|---------------|--------------------------|-------|
| **Admin, chủ bot** (`bots.admin_id = Auth::id()`) | **Toàn quyền**: xem/sửa cả 2 kênh, xem/sao chép/「再生成」 secret, xem lỗi | Như thiết kế (`checkBotHasPermission` trả `true` khi không có dòng `user_staff_bots`) | `WebhookRelayController.php:242-257`; `functions.php:198-227`. **Cao** |
| **Staff `is_admin = 1`** | `checkBotHasPermission` = `true` ⇒ toàn quyền ở tầng controller | **Có thể vẫn bị middleware chặn**: `getRouterBotInvite()` chỉ xét `bot_role_access` theo `role_id`, không xét `is_admin`; đường chọn bot `BasicController.php:246-250` gắn `is_bot_invite = true` cho mọi non-owner (đường `StaffManagementController.php:1482-1487` thì không). Role chưa được tick ⇒ 302 + mất bot đang chọn | `functions.php:207-208, 5044-5094`; `AdminAccess.php:61-73`. **Cao (code)** / Trung bình (tuỳ đường vào — G-08) |
| **Staff thường** (`is_admin = 0`, `user_staff_bots.status = 1`) | **Mặc định KHÔNG có quyền.** Admin tick 「Webhook転送」 (nhóm 「システム設定」) cho role. Quyền mức **màn** (R-003 nội bộ): được cấp là làm được **mọi** thao tác, kể cả 「再生成」 và xem plaintext secret | Cấp được (command có đặt `menu_id`, khác FA-046) | `AddAccessFeatureWebhookRelay.php:9-20, 37-42, 83, 99`; `WebhookRelayController.php:234-241`. **Cao** |
| **Staff chưa được cấp** | Vẫn **thấy** menu; bấm vào ⇒ `AdminAccess` xoá `current_bot_id` + `is_bot_invite` khỏi session, redirect `/admin/home` + 「この権限は許可されていません。」 | — | `sidebar.blade.php:79, 209-245`; `AdminAccess.php:61-72`. **Cao** |
| **LINE User** | Không tương tác trực tiếp. Sự kiện của họ (webhook LINE, gắn/gỡ tag, thay đổi thông tin bạn bè) là **dữ liệu được chuyển tiếp** | — | **Cao** |
| **Công cụ bên ngoài** (hệ thống nhận) | Nhận `POST` tới 「転送先URL」; kênh 2 xác thực bằng **so sánh chuỗi** header `X-Lme-Signature` với secret; dedupe bằng `X-Lme-Delivery-Id` | — | `WebhookSignatureHelper.java:79-82`; `WebhookRelayApiClient.java:41-59`. **Cao** |

### 1.5 Phạm vi

**Bao gồm**
- 4 màn trên 1 route: SCR-WHR-01 (tab kênh 1, mặc định), SCR-WHR-02 (tab kênh 2), SCR-WHR-03 (confirm 「再生成」), SCR-WHR-04 (confirm rời tab khi chưa lưu).
- 7 endpoint: EP-01…EP-05 (AJAX), EP-06 (trang), EP-07 (debug, không có UI).
- Validate URL đích (10 luật — gồm luật chặn webhook LME #44660, chống SSRF lúc lưu), vòng đời 「署名シークレット」 (sinh, mã hoá, mask, xem, tái tạo), mốc 「最終更新」, phân quyền Staff, Artisan command `access-feature:webhook-relay`.
- Job Spring Boot: quét 3 bảng nguồn, gửi HTTP, thử lại, ghi lỗi; cache cấu hình.
- Điểm nhận webhook LINE `BotController@callbackWebHook` — **chỉ** phần ảnh hưởng tới kênh 1 (lưu body thô, không kiểm chữ ký).

**Không bao gồm**
- Nghiệp vụ xử lý webhook LINE của `HandlePostbackTask` (thuộc FA-030 / FA-041) — chỉ ghi nhận cột `status` ảnh hưởng điều kiện quét.
- Các luồng gắn/gỡ tag (FA-012, SC-004…) và thay đổi thông tin bạn bè (FA-015) — chỉ ghi nhận chúng là **nguồn sự kiện** kênh 2.
- Màn phân quyền Staff (FA-035) — chỉ ghi nhận mục quyền 「Webhook転送」.
- Tài liệu hợp đồng gửi khách (không có trong repo — G-07).

### 1.6 Trạng thái triển khai & cấu hình

- **Tính năng mới**. Migration `2026_09_03_100000…100200` tạo `webhook_relay_setting`, `webhook_relay_queue`, `webhook_relay_error`; `2026_09_10_000000` thêm `status_sync` vào `tag_history`, `friend_info_history`; `2026_09_16_*` thêm 2 cột mốc 「最終更新」 + nới `callback_event_id`. **Không có migration** cho `callback_event.status_sync` / `webhook_event_id` (G-02).
- **DB dump cũ hơn tính năng**: không có 5 bảng `webhook_relay_*`, `tag_history`, `friend_info_history`; `callback_event` thiếu `status_sync`, `webhook_event_id`; `access_feature` chưa có dòng `webhookRelay`.
- **Chưa biết** production đang chạy commit nào (EP-07), flag job bật chưa, command phân quyền chạy chưa (G-01).

**Cấu hình web** (không có feature flag — 3 cờ `WEBHOOK_RELAY_*` cũ đã bị gỡ ở #40763, `config/sns-line.php:1283-1289`):

| Biến | Dùng ở | Ghi chú |
|------|--------|--------|
| `APP_KEY` | `Crypt::encrypt/decrypt` secret | **Phải giống hệt** giữa web và job (`LARAVEL_APP_KEY`) |
| `WEBHOOK_RELAY_DOCS_URL` | `WebhookRelayController.php:61` (`env()` trực tiếp) | Link 「使い方を見る」; rỗng hoặc `config:cache` ⇒ nút không làm gì (BUG-02). URL chưa được cấp (TODO QA-spec-002) |
| `APP_DEBUG` | Thiết kế để khoá EP-07 | **Hiện không được đọc** (guard bị comment) |

**Cấu hình job** (`config.properties` ngoài repo, đọc qua `ConfigFile.java`):

| Khoá | Mặc định | Ý nghĩa |
|------|:-------:|---------|
| `ENABLE_FORWARD_WEBHOOK_CALLBACK` | `0` | Bật kênh 1 |
| `ENABLE_FORWARD_WEBHOOK_LME` | `0` | Bật kênh 2 |
| `NUMBER_THREAD_FORWARD_WEBHOOK_CALLBACK` / `_LME` | `10` / `10` | Số worker mỗi kênh |
| `NUMBER_THREAD_RETRY_FORWARD_WEBHOOK` | `5` | Worker thử lại (chung 2 kênh; tự bật khi một trong hai kênh bật) |
| `LARAVEL_APP_KEY` | rỗng | Giải mã `signing_secret`; thiếu ⇒ kênh 2 **vẫn gửi nhưng không có header** + Chatwork cảnh báo |
| Hằng số cứng (`Constants.java`) | — | `MAX_ATTEMPT = 3` (tính cả lần đầu), `RETRY_DELAY_MINUTES = 1`, `TIMEOUT_SECONDS = 10`, `MAX_EVENTS_PER_REQUEST = 1000` |

**Triển khai một lần**: `php artisan access-feature:webhook-relay` (idempotent, không transaction) tạo 1 dòng cha + 5 dòng con `access_feature`; không cấp sẵn cho role nào.

### 1.7 Kiến trúc tổng thể

```
                       ┌────────────────────────── WEB (Laravel) ──────────────────────────┐
 Admin / Staff ─ UI ─► │ WebhookRelayController (EP-01…06) ─► WebhookRelayService            │
 「Webhook転送」        │                                      ├─ WebhookUrlValidator (9 luật)│
                       │                                      ├─ SettingRepository ─────────┼─► webhook_relay_setting (R/W)
                       │                                      └─ ErrorRepository ───────────┼─◄ webhook_relay_error   (R)
 LINE ─ POST ────────► │ BotController@callbackWebHook ─► storeCallbackEventRaw ─────────────┼─► callback_event (backenddb, request = body thô)
 Thao tác tag / 友だち情報 │ TagHistory::create / FriendInformationHistory::create (+ job Java) ─┼─► tag_history, friend_info_history
                       └─────────────────────────────────────────────────────────────────────┘
                                         │ DB polling trên cột status_sync (không có queue do web ghi)
                       ┌────────────────────────── JOB (linect-service) ────────────────────┐
                       │ WebhookRelaySettingManager  (cache toàn bảng setting, 60s)          │
                       │ HandleForwardCallbackEventManager/Task   (kênh 1)                    │
                       │ HandleForwardLmeEventManager/Task        (kênh 2)                    │
                       │ HandleRetryWebhookRelayManager/Task      (thử lại, chung 2 kênh)     │
                       │  ghi: status_sync, webhook_relay_queue (retry), webhook_relay_error, │
                       │       bộ đếm lỗi liên tiếp                                           │
                       │  gửi: POST https → URL khách (kênh 2 kèm X-Lme-Signature = secret)   │
                       └──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Các màn hình & Luồng xử lý end-to-end

### 2.0 Bảng tổng hợp màn hình

| Mã | Tên màn hình | Loại | Điều kiện hiển thị | Mã trong comment dev | Endpoint |
|----|-------------|------|-------------------|---------------------|----------|
| **SCR-WHR-01** | Tab 「LINE公式アカウントデータ転送」 (kênh 1) | Trang / tab — **mặc định** | `activeTab === 1` (luôn = 1 khi vào / F5) | `SCR-01` | EP-06, EP-01, EP-02, EP-04 |
| **SCR-WHR-02** | Tab 「L Messageデータ転送」 (kênh 2) | Trang / tab | `activeTab === 2` | `SCR-02` | EP-02, EP-04, EP-05, EP-03 |
| **SCR-WHR-03** | Xác nhận tái tạo 「署名シークレット」 | Dialog native `window.confirm` | Bấm 「再生成」 ở SCR-WHR-02 | `BR-03` (nội bộ) | EP-03 |
| **SCR-WHR-04** | Xác nhận rời tab khi chưa lưu | Dialog native `window.confirm` | Đổi tab khi tab đang rời có thay đổi chưa lưu | `BR-22` (nội bộ) | (EP-04 lần đầu mở tab mới) |

Không có screenshot (G-06). File: `resources/views/admin/webhook-relay/index.blade.php`, `public/js/admin/webhook-relay/webhook-relay.js`, `public/css/admin/webhook-relay/webhook-relay.css`.

### 2.1 Tiền đề: middleware và kiểm quyền (EP-01…EP-06)

Thứ tự thực tế: nhóm `web` (EncryptCookies, StartSession, ShareErrorsFromSession, **VerifyCsrfToken**, SubstituteBindings) → `NotifyChatworkRequestTimeSlow` → `admin_access` → `https_protocol` (thân hàm đã comment, không làm gì) → `check_remember_token` (+ `throttle:10,1` riêng EP-05) → kiểm quyền **trong controller**. Global middleware có `TrimStrings`, `ConvertEmptyStringsToNull`.

| # | Kiểm tra | Nơi | Không đạt |
|:-:|---------|-----|----------|
| 1 | Đã đăng nhập và `users.role ∈ {0, 1, 2, -1}` | `AdminAccess.php:23, 91-109` | Trang: 302 → `/logout`. AJAX: 401 「ログインが必要です。」 / 403 「この操作を行う権限がありません。」 |
| 2 | Staff dạng `is_bot_invite`: tên route ∈ `getRouterBotInvite()` (dòng cha + 5 dòng con `access_feature` của role) | `AdminAccess.php:61-73`; `functions.php:5044-5094` | 302 → `/admin/home` + **xoá `current_bot_id`, `is_bot_invite` khỏi session** + 「この権限は許可されていません。」 |
| 3 | `session.remember_token == users.remember_token_reset_pass` | `CheckRememberToken.php:26-40` | Logout; AJAX nhận **200** `success:false` 「ログイン情報が変更されましたので、再度ログインしてください。」 |
| 4 | CSRF (EP-02, EP-03 là POST; `/admin/webhook-relay/*` **không** nằm trong `$except`) | `VerifyCsrfToken.php:14-54` | 419 |
| 5 | (Chỉ EP-05) ≤ 10 request/phút/user | `routes/web.php:668-669` | 429 → toast 「エラーが発生しました。」 |
| 6 | Controller: có `current_bot_id` trong session | `WebhookRelayController.php:40-43, 214-216` | Trang: 302 `/admin/home` + lỗi; AJAX: 403 `PERMISSION_DENIED` |
| 7 | Controller `canAccess()`: owner (`bots.admin_id`) **hoặc** Staff `user_staff_bots.status = 1` | `:242-257` | như #6 |
| 8 | `checkBotHasPermission('webhookRelay', $botId)` | `functions.php:198-227` | như #6 |

Side effect chung: `admin_access` INSERT `user_access_bot` 1 lần/ngày cho Staff (`AdminAccess.php:35-55`) — không phải logic riêng FA-047. `bot_id` **không bao giờ** nhận từ client (chống IDOR 2 lớp: session + `canAccess`).

---

### 2.2 Khung trang chung (SCR-WHR-01 và SCR-WHR-02)

```
Webhook転送  [使い方を見る]
┌ card 1 ───────────────────────────────────────────────────────────────┐
│ [LINE公式アカウントデータ転送] [L Messageデータ転送]   ← lme-tab-horizontal │
│ 転送先設定                                                             │
│ {mô tả kênh}                                                           │
│ 転送の状態   (switch) ● 転送中 / ● 停止中                              │
│ 転送先URL *  [https://example.com/webhook______] (520px)               │
│ (chỉ tab 2) 署名シークレット [whsec_••••••••] [mắt] [sao chép] [⟳ 再生成] │
│             ⓘ リクエストヘッダー X-Lme-Signature に署名を付与して…       │
├───────────────────────────────────────────────────────────────────────┤
│                     [ 保存する ] (160px, NGOÀI tabpanel)                │
└───────────────────────────────────────────────────────────────────────┘
┌ card 2 「転送エラー」 ──────────────────────────────────────────────────┐
│ 「{tên tab}」で転送に失敗したデータを新しい順に最大100件まで表示します。  │
│ 最終更新: 2026/10/23 10:32                              [⟳ 最新に更新] │
│ 発生日時 ⇅ │ イベント種別 │ エラー内容 (badge đỏ) │ エラーコード      │
│ ⓘ 転送に失敗した場合は自動で最大3回まで再送を試みます。…              │
└───────────────────────────────────────────────────────────────────────┘
```
(Wireframe suy từ Blade + CSS — tin cậy Trung bình về hình dạng.)

- Header: tiêu đề 「Webhook転送」; nút 「使い方を見る」 (`lme-button-flat`, icon `book1`) mở `docsUrl` ở tab mới — **env rỗng thì bấm không có tác dụng**, nút vẫn hiện như hoạt động (UI-07).
- Hai tab cùng **1 Vue instance**, cùng nút 「保存する」 và **cùng 1 instance `lme-table`** (chỉ đổi `data-source`). **Không có badge số lỗi trên tab** (thiết kế v2 đã bỏ).
- Đang nạp cấu hình (EP-01): **không có loading indicator**, form hiển thị giá trị mặc định cho tới khi API trả về (`isLoadingConfig` không bind vào template — dẫn tới UI-01).

#### Luồng 1: Mở màn (kể cả lần đầu, bot chưa cấu hình)

| # | User action | UI | API | Business logic | DB | Response | UI update |
|:-:|------------|----|-----|----------------|----|----------|-----------|
| 1 | Bấm 「Webhook転送」 ở sidebar | Sidebar | **EP-06** `GET /admin/webhook-relay` | Chuỗi §2.1 → `index()`: `getBotId()` + `canAccess()`; sai ⇒ redirect `adminIndex` | SELECT `bots`, `user_staff_bots`, `access_feature`, `bot_role_access`; INSERT `user_access_bot` (Staff, 1 lần/ngày) | HTML + `window.WEBHOOK_RELAY_CONFIG` = `{endpoints{config,save,regenerateSecret,errors,secret}, channels{line:1,lme:2}, docsUrl}` | Render, `activeTab = 1`, form mặc định (tắt / URL rỗng / 「停止中」) |
| 2 | (tự động, `mounted`) | — | **EP-01** `GET /config` | `getConfig()`: `ensureSecret()` — chưa có secret ⇒ transaction + `SELECT … FOR UPDATE`, sinh `whsec_` + 32 base62, `Crypt::encrypt`; request song song đã tạo ⇒ dùng lại, không sinh đè; 1062 ⇒ chạy lại 1 lần → `touchLastUpdatedAt([1,2])` | **Lần đầu**: INSERT `webhook_relay_setting` (`bot_id`, `signing_secret`, `secret_generated_at`; 2 kênh giữ default TẮT, URL NULL) hoặc UPDATE secret nếu dòng thiếu secret. **Mọi lần**: UPDATE `errors_refreshed_at`, `notify_errors_refreshed_at`, `updated_at` = now. Log audit `[action=init-secret]`, `[action=update]` | 200 `{last_updated_at{1,2}, channels{1:{is_enabled,endpoint_url}, 2:{…, secret_masked}}, has_secret}` | Điền 2 tab, lưu `savedState`; ô secret tab 2 = `whsec_` + 32 `•` |
| 3 | (sau EP-01) | — | **EP-04** `GET /errors?channel=1` | `getErrors(refresh=false)`: đọc mốc đang lưu | SELECT `webhook_relay_error` WHERE `bot_id`, `channel = 1` ORDER BY `occurred_at DESC, id DESC` LIMIT 100; SELECT `errors_refreshed_at` | 200 `{channel, items[], last_updated_at}` | Bảng lỗi tab 1 (hoặc 「転送エラーはありません」); 「最終更新: Y/m/d H:i」 = giờ vừa mở |

Lỗi: EP-01 403 ⇒ toast 「この権限は許可されていません。」 + 3 giây sau về `/admin/home`; lỗi khác ⇒ toast 「エラーが発生しました。」 (form giữ mặc định — nguy cơ UI-01).

---

### 2.3 SCR-WHR-01: Tab 「LINE公式アカウントデータ転送」 (kênh 1 — mặc định)

| # | Label JP | Loại | Bắt buộc | Mặc định | Placeholder | Validation FE | Validation server |
|:-:|---------|------|:-------:|---------|------------|--------------|-------------------|
| 1 | 「転送の状態」 | `lme-switch` + `lme-status` (「転送中」 xanh `#52C41A` / 「停止中」 xám `#D9D9D9`) | Luôn có giá trị | Tắt | — | — | `is_enabled required\|boolean` |
| 2 | 「転送先URL」 | `lme-input` md, 520px, prop `required` (dấu `*` — Trung bình) | **Chỉ khi bật** | Rỗng | 「https://example.com/webhook」 | Sau `trim()`: rỗng + bật ⇒ 「転送先URLを入力してください。」; không bắt đầu `https://` (phân biệt hoa thường) ⇒ 「httpsで始まるURLを入力してください。」 | 9 luật `WebhookUrlValidator` (BR-06…BR-14); không có `maxlength` trên input |

- Badge đổi **ngay khi gạt switch** (phản ánh giá trị chưa lưu — UI-05); gạt switch **không** tự lưu.
- Không có trường secret ở tab này (kênh LINE không ký).
- Lỗi inline (`:error-message`) **không tự xoá** khi sửa URL — chỉ xoá ở lần bấm lưu kế tiếp hoặc khi đổi tab (UI-04).

#### Luồng 2: Bật chuyển tiếp kênh 1 (happy path, kèm hiệu lực ở job)

| # | User action | UI | API | Business logic | DB | Job | UI update |
|:-:|------------|----|-----|----------------|----|-----|-----------|
| 1 | Gạt switch 「転送の状態」 | SCR-WHR-01 | — | — | — | — | Badge 「転送中」 (chưa lưu) |
| 2 | Nhập 「転送先URL」 `https://…` (cổng 443, host public, phân giải DNS được) | SCR-WHR-01 | — | — | — | — | — |
| 3 | Bấm 「保存する」 | Footer card 1 | — | FE validate luật 1–2; sai ⇒ lỗi inline, **không gửi** | — | — | — |
| 4 | (hợp lệ) | — | **EP-02** `POST /save` `{channel:1, endpoint_url:<trim>, is_enabled:1}` (+ `X-CSRF-TOKEN`) | FormRequest (`channel in:1,2`, `is_enabled boolean`, `endpoint_url nullable\|string`) → `resolveBotId()` → `save()`: `WebhookUrlValidator` 9 luật (tra DNS **đồng bộ**) → `DB::transaction` + `lockByBot` (`FOR UPDATE`) → chỉ gán cột kênh 1; TẮT→BẬT ⇒ reset bộ đếm; chưa có dòng ⇒ INSERT kèm secret; 1062 ⇒ chạy lại 1 lần → audit `[action=update]` (before/after, **có URL**) | UPDATE (hoặc INSERT) `webhook_relay_setting`: `endpoint_url`, `is_enabled = 1`, `consecutive_failure_count = 0`, `auto_disabled_at = NULL`, `updated_at`. **Không đụng** cột `notify_*` | — | 200 `{channel, is_enabled, endpoint_url, has_secret, secret_masked}` → toast 「保存しました」, **ở lại màn**, cập nhật `savedState` |
| 5 | (≤ 60 giây sau) | — | — | — | — | `WebhookRelaySettingManager` nạp lại cache toàn bảng | (không hiển thị). Sự kiện LINE trong khoảng này bị đánh `IGNORE` vĩnh viễn (R-06) |
| 6 | (LINE gửi webhook) | — | — | — | `callback_event` | Chuỗi kênh 1 (§2.8.1) | Thành công: không có gì trên UI. Thất bại: 1 dòng ở 「転送エラー」 tab 1 (§2.7) |

#### Luồng 3, 4, 5: Lưu thất bại / tắt kênh

| Tình huống | Bắt ở đâu | HTTP / `error_code` | Thông báo | DB |
|-----------|-----------|--------------------|-----------|----|
| Bật + URL rỗng | FE | — (không gửi) | Inline 「転送先URLを入力してください。」 | — |
| URL không bắt đầu `https://` (kể cả `HTTPS://` — UI-16) | FE | — | Inline 「httpsで始まるURLを入力してください。」 | — |
| URL > 1024 ký tự (`mb_strlen`) | Server | 422 `URL_TOO_LONG` | Inline 「転送先URLは1024文字以内で入力してください。」 (chuỗi tạm — QA-001) | — |
| Có khoảng trắng (kể cả U+3000) / sai cấu trúc / host ngoài RFC 1123 / cổng ≠ 443 / DNS không phân giải / IP nội bộ-reserved | Server | 422 `URL_NOT_ALLOWED` | Inline **cùng 1 câu** 「このURLは転送先に指定できません。」 (chuỗi tạm; 5 lý do không phân biệt — UI-17) | — |
| `channel` / `is_enabled` sai kiểu (gọi trực tiếp) | FormRequest | 422 `INVALID_PARAM`, `field = request` | Toast 「エラーが発生しました。」 | — |
| Mất quyền | Controller | 403 `PERMISSION_DENIED` | Toast 「この権限は許可されていません。」 → 3s về `/admin/home` | — |
| 5xx / mạng / 401 / `CheckRememberToken` 200 | — | — | **Không có thông báo nào** (UI-02, BUG-05) | — |
| **Tắt kênh** (switch tắt, URL có thể rỗng) | — | 200 | 「保存しました」 | `is_enabled = 0`; URL rỗng lưu `NULL`; **không** reset bộ đếm. Job ngừng gửi trong ≤60s; sự kiện đang chờ thử lại → `IGNORE`, **không** hiện ở danh sách lỗi |

Lưu ý: URL **không rỗng** luôn bị kiểm luật 2–10 **kể cả khi tắt** (BR-14) — gồm luật chặn webhook LME (BR-11b). Hai kênh được phép trùng URL.

---

### 2.4 SCR-WHR-02: Tab 「L Messageデータ転送」 (kênh 2)

Cùng 2 trường như SCR-WHR-01 (switch + URL riêng của kênh 2, cùng bộ luật và chuỗi lỗi), thêm:

| # | Label JP | Loại | Giá trị | Nguồn |
|:-:|---------|------|--------|------|
| 3 | 「署名シークレット」 | `lme-input disabled` 520px (read-only) + 3 nút | Mask: `whsec_` + 32 `•` (6 ký tự đầu giữ lại = đúng tiền tố ⇒ **mọi secret có cùng bản mask**); plaintext: `whsec_` + 32 ký tự `[0-9A-Za-z]` (38 ký tự). **Đã sinh sẵn từ lần đầu mở màn** | `index.blade.php:83-109`; `WebhookRelayService.php:499-527` |

| Nút | Hiển thị | Disabled khi | Hành vi |
|-----|---------|-------------|---------|
| Hiện/ẩn | Icon `eye-outlined` ↔ `eye-close-outlined`, **không text / tooltip / aria-label** (UI-12) | `!hasSecret` | Lần đầu ⇒ EP-05 lấy plaintext; sau đó dùng cache trong bộ nhớ trang |
| Sao chép | Icon `file-copy-outlined` (không tooltip) | `!hasSecret` | Copy **plaintext** (gọi EP-05 nếu chưa cache) → toast 「コピーしました」 / 「コピーに失敗しました」 |
| 「再生成」 | Text + icon `reload-outlined` | `!hasSecret \|\| isRegenerating` | Mở SCR-WHR-03 |

Ghi chú dưới ô (icon `info-circle-filled`): 「リクエストヘッダー X-Lme-Signature に署名を付与して送信します。外部ツール側でこの値を検証すると、エルメからの送信であることを確認できます。」 — ⚠ wording lệch hành vi job (header là secret thô — UI-22, V-02).

| Trạng thái ô secret | Biểu hiện |
|--------------------|-----------|
| Có secret (bình thường) | Mask, 3 nút enabled |
| Đang hiện plaintext | Secret thật; **không reset khi đổi tab** (UI-11) |
| `has_secret = false` | Ô rỗng, 3 nút disabled (gần như không xảy ra vì EP-01 tự sinh) |
| Secret không giải mã được (đổi `APP_KEY`) | `has_secret = true`, `secret_masked = null` ⇒ ô **rỗng** nhưng 3 nút **enabled** (BUG-01) |

#### Luồng 6: Xem / sao chép secret

| # | User action | API | Business logic | DB | Response | UI update |
|:-:|------------|-----|----------------|----|----------|-----------|
| 1 | Bấm icon mắt (lần đầu) | **EP-05** `GET /secret` (`throttle:10,1`) | `getPlainSecret()`: không có dòng/secret ⇒ 422 `INVALID_PARAM`; có ⇒ log audit `[action=view-secret]` (user_id, bot_id, ip — **file log**, không phải bảng) → `decryptSecret()` (lỗi ⇒ `null`, không làm sập màn) | SELECT `webhook_relay_setting.signing_secret` | 200 `{secret}` + `Cache-Control: no-store` | Ô hiện plaintext; icon đổi `eye-close-outlined` |
| 2 | Bấm icon mắt lần nữa | — | — | — | — | Về mask, không gọi server |
| 3 | Bấm sao chép | EP-05 (nếu chưa cache) | như bước 1 | như bước 1 | như bước 1 | `navigator.clipboard.writeText` → fallback `<textarea>` ẩn + `execCommand('copy')` → toast |
| 4 | Lưu thành công / 「再生成」 thành công | — | — | — | — | Xoá cache plaintext, về mask |

Vượt 10 lần/phút ⇒ 429 ⇒ toast 「エラーが発生しました。」. Bộ đếm throttle Laravel 5.5 khoá theo `sha1(user id)` ⇒ **dùng chung** với `throttle:30,1` của FA-046 (Trung bình). Secret không giải mã được ⇒ EP-05 trả `{secret: null}`, nút copy chép chuỗi `"null"` mà vẫn báo 「コピーしました」 (UI-20).

#### Luồng 2b: Bật chuyển tiếp kênh 2

Như Luồng 2 với `channel: 2`, ghi `notify_endpoint_url`, `notify_is_enabled`, reset `notify_consecutive_failure_count`, `notify_auto_disabled_at` (TẮT→BẬT); **không đụng** `endpoint_url` / `is_enabled`. Lưu thành công còn đưa ô secret về mask + xoá cache plaintext. Hiệu lực ở job ≤60s; sau đó mọi thao tác tag / thông tin bạn bè của bot được gửi theo lô kèm `X-Lme-Signature` (§2.8.2).

---

### 2.5 SCR-WHR-03: Xác nhận tái tạo 「署名シークレット」

`window.confirm` native (không phải `lme-modal` — khác FA-044/045/046, UI-13). Nội dung (nguyên văn, comment yêu cầu đúng design): 「署名シークレットを再生成します。外部ツール側の設定も更新が必要です。よろしいですか？」. Nút OK / Cancel theo ngôn ngữ trình duyệt (Thấp).

#### Luồng 7: Tái tạo secret

| # | User action | API | Business logic | DB | Job | UI update |
|:-:|------------|-----|----------------|----|-----|-----------|
| 1 | Bấm 「再生成」 | — | — | — | — | Mở SCR-WHR-03 |
| 2a | Cancel | — | — | — | — | Không đổi gì |
| 2b | OK | **EP-03** `POST /regenerate-secret` | `regenerateSecret()`: không có dòng ⇒ 422 `INVALID_PARAM`; sinh secret mới → `updateForBot` (**1 câu UPDATE, không transaction, không khoá** — BUG-03) → audit `[action=regenerate-secret]` | UPDATE `signing_secret` (ciphertext mới), `secret_generated_at`, `updated_at` | Cache setting còn ciphertext cũ ≤60s ⇒ kênh 2 **vẫn gửi secret cũ** tới lần nạp sau (R-06, V-12) | 200 `{secret_masked, secret_plain: null, regenerated_at}` → ô về mask (trông **y hệt** trước — UI-03), **không toast**, xoá cache plaintext |
| 3 | Người dùng phải bấm sao chép để lấy secret mới và cập nhật bên công cụ ngoài | EP-05 | | | | |

Phía web tuyên bố "secret cũ hết hiệu lực ngay, không ân hạn" (QA-spec-017). Thực tế ở job: tối đa ~60 giây gửi secret cũ; nếu bên nhận đã đổi sang secret mới và trả 401 ⇒ `UNAUTHORIZED` **không retry** ⇒ mất lô sự kiện đó.

---

### 2.6 SCR-WHR-04: Xác nhận rời tab khi chưa lưu

`window.confirm`: 「保存していない変更があります。タブを切り替えると変更内容は破棄されます。よろしいですか？」 — comment ghi design chưa cấp wording, **cần BA xác nhận**.

#### Luồng 8: Đổi tab

| # | Điều kiện / action | Kết quả |
|:-:|-------------------|--------|
| 1 | Tab đang rời có thay đổi chưa lưu (`isDirty`: switch khác giá trị đã lưu, hoặc URL sau `trim()` khác) | Hiện SCR-WHR-04 |
| 2 | Cancel | `activeTab` đặt lại tab cũ ở `$nextTick`; giữ thay đổi đang sửa |
| 3 | OK, hoặc không có thay đổi | Khôi phục giá trị đã lưu cho tab vừa rời (xoá lỗi inline) → lần đầu mở tab mới ⇒ EP-04 `channel=<tab mới>` (không `refresh`, **không đổi mốc**) → reset cuộn bảng lỗi về đầu (#40792) |

Chỉ bảo vệ khi **đổi tab**; rời trang (sidebar, F5, đóng tab) **không** cảnh báo (UI-06).

---

### 2.7 Card 「転送エラー」 (chung 2 tab, dữ liệu theo kênh đang mở)

| Cột | Header JP | Rộng | Hiển thị | Nguồn |
|-----|----------|:---:|---------|------|
| `occurred_at` | 「発生日時」 (sortable client-side) | 200 | `Y/m/d H:i:s`; = lúc job **bỏ cuộc**, giờ JVM | `webhook_relay_error.occurred_at` |
| `event_type` | 「イベント種別」 | 180 | Monospace, **không dịch**: kênh 1 = `type` LINE (`message`, `follow`…, `unknown` nếu NULL); kênh 2 = `tag` \| `friend_info` | `event_type` |
| `reason` | 「エラー内容」 | 280 | Badge `lme-status` đỏ `#FF4D4F`; chuỗi JP do **server** map từ `error_code` (§3.8.5) | `error_code` → `reasonText()` |
| `http_status` | 「エラーコード」 | 140 | Số; `NULL` ⇒ 「—」 (không nhận được response) | `http_status` |

- Mô tả: 「「{tên tab}」で転送に失敗したデータを新しい順に最大100件まで表示します。」. Rỗng: 「転送エラーはありません」.
- Ghi chú cuối: 「転送に失敗した場合は自動で最大3回まで再送を試みます。3回とも失敗したものだけをここに記録します。表示は直近100件までです。これより古いエラーは表示されません。成功した送信は記録していません。」 — ⚠ lệch hành vi job (UI-21, V-11).
- Không có action trên dòng, không phân trang, không lọc/tìm. Không có cột/trạng thái "đang chờ thử lại".

#### Luồng 9: Xem và làm mới lỗi

| # | User action | API | Business logic | DB | UI update |
|:-:|------------|-----|----------------|----|-----------|
| 1 | (mở màn / lần đầu mở tab) | EP-04 `?channel=X` | Đọc mốc đang lưu | SELECT 100 dòng `channel = X` | Bảng mới → cũ |
| 2 | Bấm tiêu đề 「発生日時」 | — | Sort client-side so sánh **chuỗi** `Y/m/d H:i:s` trên ≤100 dòng đã tải; chỉ phản hồi cột này | — | Đảo thứ tự |
| 3 | Bấm 「最新に更新」 (disabled khi `isLoadingErrors`) | EP-04 `?channel=X&refresh=1` | `touchLastUpdatedAt([X])` (không khoá; bot chưa có dòng ⇒ INSERT dòng chỉ chứa mốc) | UPDATE `errors_refreshed_at` hoặc `notify_errors_refreshed_at` + `updated_at`; SELECT 100 dòng | Bảng nạp lại; 「最終更新」 = giờ server, chỉ kênh X |
| 4 | Lỗi tải | — | — | — | Toast 「エラーが発生しました。」, giữ dữ liệu cũ |

Bảng **không có trạng thái loading** ⇒ trong lúc tải (và khi lần tải đầu lỗi) hiện 「転送エラーはありません」, dễ hiểu nhầm (UI-08). Mốc 「最終更新」 dùng chung cho mọi người trong bot, không ẩn lỗi cũ.

---

### 2.8 Luồng nền end-to-end: từ sự kiện tới bảng 「転送エラー」

#### 2.8.1 Kênh 1 — webhook LINE

| # | Tác nhân | Hành động | DB | Ghi chú |
|:-:|---------|-----------|----|--------|
| 1 | LINE → web `POST /line/callback/add/{bot_id}` (`callback-web-hook`, miễn CSRF) | `BotController@callbackWebHook`: `empty($bot_id)` ⇒ bỏ qua; `bot_type = 0` **tự tính chữ ký từ body rồi tự so với chính nó** (không đọc `X-Line-Signature` — SEC-02); `bot_type = 1` không kiểm; events rỗng ⇒ `bots.is_verify = 1` | `storeCallbackEventRaw`: INSERT `callback_event` (backenddb) `{user_id, bot_id, line_id, type, webhook_event_id, request = body thô}`, `status = 0`, `status_sync = NULL`. Toàn sự kiện `delivery` ⇒ **không lưu**. Body > 65.535 byte ⇒ bị **cắt cụt** (BUG-07) | 1 dòng / 1 lần LINE gọi; `type` = sự kiện đầu tiên khác `delivery` |
| 2 | `HandlePostbackTask` (ngoài FA-047) | Xử lý nghiệp vụ | UPDATE `status` 0 → 2 / 3…10 / 11 | |
| 3 | Scanner kênh 1 (200ms–1s) | `SELECT * … WHERE status_sync IS NULL AND status NOT IN (0,1,100,101) ORDER BY id LIMIT 500`; phân loại: `status ∈ {11,111}` (trùng) ⇒ IGNORE; `isCallbackChannelReady(bot)` ⇒ forward; còn lại ⇒ IGNORE | Bulk UPDATE `status_sync = 4` (IGNORE) / `= 1` (RUNNING) **trước** khi đẩy queue in-memory | Chờ queue ≤200; cache chưa sẵn sàng thì chờ |
| 4 | Worker kênh 1 (10 luồng) | Gate lại (vừa tắt ⇒ `status_sync = 4`); body = `request` nguyên văn (rỗng ⇒ `INVALID_PAYLOAD`); `deliveryId = UUID` → `POST endpoint_url` | — | Header: `Content-Type: application/json; charset=utf-8`, `Accept`, `X-Lme-Timestamp` (epoch ms lúc gửi), `X-Lme-Delivery-Id`. **Không** `X-Lme-Signature`, không chuyển `X-Line-Signature` gốc |
| 5a | | 2xx | `status_sync = 2`; reset `consecutive_failure_count` | |
| 5b | | Timeout / HTTP ≥ 500 | `status_sync = 5` **trước**, rồi INSERT `webhook_relay_queue` (`channel 1`, `payload = body`, `attempt_count 1`, `next_attempt_at = now + 1 phút`) | INSERT queue lỗi ⇒ quay về 5c |
| 5c | | Lỗi khác (`CONNECT_FAILED`, 4xx, 3xx không follow, `INVALID_PAYLOAD`) | `status_sync = 3`; INSERT `webhook_relay_error`; `consecutive_failure_count + 1` | Ghi **ngay sau lần 1** |
| 6 | Retry (§2.8.3) | | | |
| 7 | Web EP-04 | Đọc 100 dòng `channel = 1` | | Hiện ở tab 1 |

#### 2.8.2 Kênh 2 — sự kiện tag / thông tin bạn bè

| # | Tác nhân | Hành động | DB | Ghi chú |
|:-:|---------|-----------|----|--------|
| 1 | Mọi luồng thay đổi tag / 友だち情報 (UI, API `/do_action`, scenario / action Java, import CSV…) | `TagHistory::create` (12 lời gọi trong 6 file web) / `FriendInformationHistory::create` + Java `HistoryHelper` | INSERT `tag_history` / `friend_info_history`, `status_sync = NULL` | Thay đổi **không** ghi lịch sử ⇒ không bao giờ được chuyển tiếp (G-09). `friend_info_history` chỉ ghi khi giá trị đổi |
| 2 | 2 scanner (tag, friend info) | `SELECT * … WHERE status_sync IS NULL ORDER BY id LIMIT 500`; tách IGNORE theo `isLmeChannelReady`; resolve `line_user.line_id` cả lô 1 query; dựng `WebhookLmeEvent` | Bulk UPDATE `status_sync = 4` / `= 1` | Không có cột chờ nghiệp vụ ⇒ gửi ngay; queue ≤50 lô |
| 3 | Gom lô | Theo bot (mỗi bot 1 URL), giữ thứ tự id, cắt ≤1000 (thực tế ≤500); **tag và friend info không bao giờ chung 1 request** | — | |
| 4 | Worker kênh 2 (10 luồng) | Gate lại; payload `{"events":[…]}` (Jackson); `X-Lme-Signature = buildHeaderValue(setting)` (secret thô; `null` ⇒ log error, **vẫn gửi**); 1 `deliveryId` cho cả lô → `POST notify_endpoint_url` | — | Header như kênh 1 + `X-Lme-Signature` |
| 5a | | 2xx | `status_sync = 2` cả lô; reset `notify_consecutive_failure_count` | |
| 5b | | Timeout / ≥ 500 | `status_sync = 5` cả lô; INSERT **N dòng** `webhook_relay_queue` cùng `delivery_id`, `payload` = JSON từng phần tử | |
| 5c | | Lỗi khác | `status_sync = 3`; **1 dòng** `webhook_relay_error` cho cả lô (sự kiện đầu làm đại diện: `queue_id`, `event_type`); counter + 1 | Bảng lỗi không phản ánh số sự kiện mất |

#### 2.8.3 Thử lại (chung 2 kênh)

| # | Hành động | DB |
|:-:|-----------|----|
| 1 | Retry scanner (5s rảnh / 200ms có việc): `SELECT delivery_id … WHERE status = 0 AND next_attempt_at <= NOW() GROUP BY delivery_id ORDER BY MIN(id) LIMIT 50` → `claimByDeliveryId` (`UPDATE … SET status = 1 WHERE delivery_id = ? AND status = 0`) | `webhook_relay_queue.status` 0 → 1 |
| 2 | Gate theo kênh: không sẵn sàng ⇒ queue `4 IGNORE`, nguồn `status_sync = 4`, **không ghi lỗi** | |
| 3 | Dựng body bằng nối chuỗi payload đã lưu (giữ nguyên byte); URL + secret lấy theo **cấu hình hiện tại**; `attemptNo = attempt_count + 1`; **cùng `delivery_id`** | |
| 4a | 2xx ⇒ queue `2 DONE` (`processed_at`), nguồn `status_sync = 2`, reset counter | |
| 4b | Retryable và `attemptNo < 3` ⇒ queue `0`, `attempt_count = attemptNo`, `next_attempt_at = NOW() + 1 phút` (giờ DB) | |
| 4c | Còn lại ⇒ queue `3 FAILED`, nguồn `status_sync = 3`, **1 dòng** `webhook_relay_error`, counter + 1 | |

Vòng đời tối đa 1 sự kiện hỏng ≈ 2 phút + thời gian chờ timeout của 3 lần gọi + ≤5s trễ quét ⇒ lỗi có thể retry xuất hiện ở 「転送エラー」 sau **~2 phút**, lỗi không-retry xuất hiện **ngay**.

---

### 2.9 Luồng 10: Staff không có quyền và các trạng thái toàn trang

| Trạng thái | Biểu hiện | Tin cậy |
|-----------|-----------|--------|
| Chưa chọn bot | Redirect `/admin/home` + 「この権限は許可されていません。」 | Cao |
| Staff chưa được cấp (bấm menu) | `AdminAccess` chặn route ⇒ **xoá `current_bot_id` + `is_bot_invite`** ⇒ `/admin/home` + 「この権限は許可されていません。」 ⇒ mất bot đang chọn | Cao |
| Mất quyền khi đang ở màn (AJAX 403 từ controller) | Toast 「この権限は許可されていません。」 → 3 giây sau `/admin/home` | Cao |
| Session hết hạn khi đang ở màn | AJAX có thể nhận 401 JSON (JS chỉ xử lý riêng 403) ⇒ toast chung 「エラーが発生しました。」, hoặc **không có thông báo** với thao tác lưu; không chuyển trang đăng nhập | Trung bình (G-12) |
| Modal chặn toàn cục của layout | Nhóm `#modalWebhookOff`, `#modalWebhookONCallbackFail`… (FA-030 / FA-044) có thể che trang khi kết nối LOA lỗi | Trung bình |

### 2.10 Sequence tổng thể web ↔ DB ↔ job ↔ endpoint bên thứ 3

```mermaid
sequenceDiagram
  autonumber
  actor A as Admin hoặc Staff
  participant UI as Màn Webhook転送 (Vue)
  participant W as Laravel WebhookRelayController
  participant S as webhook_relay_setting
  participant L as LINE Platform
  participant CB as Laravel callbackWebHook và luồng tag, friend info
  participant SRC as Bảng nguồn callback_event, tag_history, friend_info_history
  participant CM as WebhookRelaySettingManager (cache 60s)
  participant J as Job scanner và worker
  participant X as Endpoint bên thứ 3
  participant Q as webhook_relay_queue
  participant E as webhook_relay_error

  A->>UI: Mở trang
  UI->>W: GET /config (EP-01)
  W->>S: ensureSecret lần đầu + đóng mốc 最終更新 2 kênh (GHI DB)
  W-->>UI: Cấu hình 2 kênh + secret mask
  A->>UI: Bật switch, nhập URL, bấm 保存する
  UI->>W: POST /save (EP-02) channel=X
  W->>W: WebhookUrlValidator 10 luật (chặn webhook LME + tra DNS)
  W->>S: UPDATE cột của đúng 1 kênh (transaction + FOR UPDATE)
  W-->>UI: 200, toast 保存しました
  CM->>S: findAll mỗi 60s
  Note over CM,J: Cấu hình mới có hiệu lực ở job sau tối đa 60s
  L->>CB: POST webhook (nguồn kênh 1)
  CB->>SRC: INSERT callback_event, status_sync NULL
  Note over CB,SRC: Kênh 2 - thao tác tag hoặc friend info INSERT *_history
  J->>SRC: SELECT status_sync IS NULL LIMIT 500
  J->>CM: Gate - kênh bật, URL có, bot hợp lệ?
  alt Không sẵn sàng
    J->>SRC: status_sync = 4 IGNORE
  else Sẵn sàng
    J->>SRC: status_sync = 1 RUNNING
    J->>X: POST (kênh 1 body thô, kênh 2 events + X-Lme-Signature)
    alt HTTP 2xx
      J->>SRC: status_sync = 2 DONE, reset bộ đếm
    else Timeout hoặc HTTP 5xx
      J->>SRC: status_sync = 5 RETRY
      J->>Q: INSERT attempt 1, next = +1 phút
      J->>X: Thử lại tối đa 2 lần, cùng X-Lme-Delivery-Id
      alt Thành công ở lần 2 hoặc 3
        J->>Q: status = 2 DONE
        J->>SRC: status_sync = 2
      else Hết lượt
        J->>Q: status = 3 FAILED
        J->>SRC: status_sync = 3
        J->>E: INSERT 1 dòng, bộ đếm + 1
      end
    else Lỗi khác (kết nối, 4xx, 3xx)
      J->>SRC: status_sync = 3 ERROR
      J->>E: INSERT 1 dòng ngay, bộ đếm + 1
    end
  end
  A->>UI: Xem 転送エラー hoặc bấm 最新に更新
  UI->>W: GET /errors?channel=X&refresh=1 (EP-04)
  W->>S: Đóng mốc 最終更新 kênh X (GHI DB)
  W->>E: SELECT 100 dòng mới nhất của kênh X
  W-->>UI: Bảng lỗi
```

### 2.11 Flow diagram giao diện

```mermaid
flowchart TD
    A[Sidebar Webhook転送] --> B{EP-06: có bot + có quyền?}
    B -- Không --> X[Redirect /admin/home<br/>この権限は許可されていません。]
    B -- Có --> C[Render, activeTab = 1]
    C --> D[EP-01 GET /config<br/>tạo secret nếu chưa có<br/>đóng mốc 最終更新 cả 2 kênh]
    D --> E[EP-04 GET /errors?channel=1]
    E --> T1[SCR-WHR-01 tab kênh 1]
    T1 -- bấm tab 2 --> G{Tab 1 có thay đổi chưa lưu?}
    G -- Có --> M4[SCR-WHR-04 confirm]
    M4 -- Cancel --> T1
    M4 -- OK --> R[Khôi phục giá trị đã lưu tab 1]
    G -- Không --> R
    R --> LL{Tab 2 đã nạp lỗi?}
    LL -- Chưa --> E2[EP-04 GET /errors?channel=2] --> T2
    LL -- Rồi --> T2[SCR-WHR-02 tab kênh 2]
    T1 -- 保存する --> V{Validate FE kênh tab đang mở}
    T2 -- 保存する --> V
    V -- Lỗi --> VE[Lỗi inline dưới 転送先URL]
    V -- OK --> SV[EP-02 POST /save]
    SV -- 422 URL --> VE
    SV -- 422 INVALID_PARAM --> TE[Toast エラーが発生しました。]
    SV -- 200 --> OK[Toast 保存しました, ở lại màn]
    SV -- 403 --> P[Toast この権限は許可されていません。<br/>3s về /admin/home]
    T2 -- mắt hoặc sao chép --> SEC[EP-05 GET /secret lần đầu] --> SC[Hiện plaintext hoặc コピーしました]
    T2 -- 再生成 --> M3[SCR-WHR-03 confirm]
    M3 -- OK --> RG[EP-03 POST /regenerate-secret<br/>ô về mask, không toast]
    M3 -- Cancel --> T2
    T1 -- 最新に更新 --> RF[EP-04 refresh=1<br/>đóng mốc kênh đang mở]
    T2 -- 最新に更新 --> RF
```

### 2.12 Danh mục thông báo

| Loại | Thông điệp JP | Khi nào |
|------|--------------|--------|
| Toast success | 「保存しました」 | EP-02 thành công |
| Toast success | 「コピーしました」 | Copy secret thành công (kể cả khi chép chuỗi `"null"` — UI-20) |
| Toast error | 「コピーに失敗しました」 | Clipboard API và `execCommand` đều thất bại |
| Toast error | 「エラーが発生しました。」 | EP-01 lỗi; EP-04 lỗi (giữ dữ liệu cũ); EP-05 lỗi / 429; EP-03 lỗi; EP-02 `INVALID_PARAM` |
| Toast error | 「この権限は許可されていません。」 | Mọi AJAX HTTP 403 ⇒ 3 giây sau `/admin/home` |
| Inline (ô URL) | 「転送先URLを入力してください。」 / 「httpsで始まるURLを入力してください。」 / 「転送先URLは1024文字以内で入力してください。」 / 「このURLは転送先に指定できません。」 | `URL_REQUIRED` / `URL_NOT_HTTPS` / `URL_TOO_LONG` / `URL_NOT_ALLOWED` (2 chuỗi cuối tạm — QA-001) |
| Badge 「エラー内容」 | 7 chuỗi — xem §3.8.5 | Theo `error_code` |
| Confirm | SCR-WHR-03, SCR-WHR-04 | §2.5, §2.6 |
| Trang khác | 「この権限は許可されていません。」 (qua `$errors` ở `/admin/home`) | Mở trang khi chưa chọn bot / không có quyền |
| Rỗng | 「転送エラーはありません」 | 0 dòng lỗi (và cả lúc đang tải — UI-08) |

---

## 3. Data Model

### 3.1 Bảng liên quan

| Bảng | DB | Vai trò | Web | Job | Có trong dump? |
|------|----|--------|-----|-----|:---:|
| **`webhook_relay_setting`** | linedb | Cấu hình 2 kênh (1 dòng/bot) + secret + 2 mốc 「最終更新」 | SELECT, FOR UPDATE, INSERT, UPDATE | `findAll` mỗi 60s; UPDATE 2 bộ đếm | ❌ |
| **`webhook_relay_error`** | linedb | Nguồn card 「転送エラー」 | **Chỉ SELECT** (EP-04) | **Chỉ INSERT** | ❌ |
| **`webhook_relay_queue`** | linedb | Hàng đợi **thử lại** của job (chỉ chứa sự kiện gửi hỏng lần 1) | **Không đụng** (không có model) | INSERT, UPDATE | ❌ |
| `callback_event` | **backenddb** (`mysql_callback`) | Nguồn kênh 1 | INSERT (`callbackWebHook`, `storeFakeCallbackEvent`) | SELECT + UPDATE `status_sync` | ✅ nhưng **thiếu** `status_sync`, `webhook_event_id` |
| `tag_history` | linedb | Nguồn kênh 2 (`tag`) | INSERT (nhiều luồng) | SELECT + UPDATE `status_sync` | ❌ |
| `friend_info_history` | linedb | Nguồn kênh 2 (`friend_info`) | INSERT | SELECT + UPDATE `status_sync` | ❌ |
| `bots` | linedb | Owner (`admin_id`); gate job (`is_deleted`, hạn dùng) | SELECT | SELECT (cache 2 phút) | ✅ |
| `bot_contracts` | linedb | Gate job (`status = 3` đã huỷ HĐ) | — | SELECT | ✅ |
| `user_staff_bots` | linedb | Staff (`status`, `is_admin`, `role_id`) | SELECT | — | ✅ |
| `access_feature` | linedb | 1 dòng cha + 5 dòng con route `webhookRelay*` | SELECT; command INSERT/UPDATE `order` | — | ✅ (chưa có dòng FA-047) |
| `bot_role_access` | linedb | Cấp quyền theo role | SELECT | — | ✅ |
| `user_access_bot` | linedb | Log truy cập Staff (middleware chung) | INSERT | — | ✅ |
| `user_selected_bot` | linedb | Bot đang chọn (DELETE khi Staff mất hiệu lực) | DELETE | — | ✅ (không có trong `db/index.md`) |
| `users` | linedb | `role`, `remember_token_reset_pass` | SELECT | — | ✅ |
| `line_user` | linedb | `line_id` → `line_friend_id` (kênh 2) | — | SELECT | ✅ |

Chỉ tham chiếu qua ID trong payload, không bị truy vấn: `tags` (`tag_id`), `friend_information_setting` (`field_id`). **Không có FK nào** — mọi quan hệ là logic.

### 3.2 `webhook_relay_setting` (1 dòng / bot)

Model `App\Models\WebhookRelaySetting` (13 cột `$fillable`, không `$casts`, không `$hidden`); entity `WebhookRelaySetting.java`. Cột không tiền tố = kênh 1, tiền tố `notify_` = kênh 2 (`COLUMNS_BY_CHANNEL`, `WebhookRelaySetting.php:58-74`; kênh lạ rơi về kênh 1).

| Cột | Kiểu | Null / Default | Kênh | Ý nghĩa | Ai ghi → ai đọc |
|-----|------|---------------|:---:|---------|----------------|
| `id` | int unsigned AI | PK | — | | — |
| `bot_id` | int | NOT NULL, **UNIQUE** `uk_webhook_relay_setting_bot` | — | Từ session | Web / web, job (key cache) |
| `endpoint_url` | varchar(1024) | NULL | 1 | 「転送先URL」 (trim, `''` → NULL) | EP-02 → EP-01, job |
| `is_enabled` | tinyint | 0 | 1 | 「転送の状態」 0 停止中 / 1 転送中 | EP-02 → EP-01, gate job |
| `consecutive_failure_count` | int | 0 | 1 | Số lần bỏ cuộc liên tiếp (metric) | Job +1/reset, web reset khi TẮT→BẬT → **không ai đọc** |
| `auto_disabled_at` | datetime | NULL | 1 | Tự tắt kênh — **không dùng Phase 1** | Web chỉ ghi NULL → không ai đọc |
| `notify_endpoint_url` | varchar(1024) | NULL | 2 | 「転送先URL」 | EP-02 → EP-01, job |
| `notify_is_enabled` | tinyint | 0 | 2 | 「転送の状態」 | EP-02 → EP-01, gate job |
| `notify_consecutive_failure_count` | int | 0 | 2 | Metric | như kênh 1 |
| `notify_auto_disabled_at` | datetime | NULL | 2 | Không dùng | như kênh 1 |
| `signing_secret` | varchar(1024) | NULL | 2 | Ciphertext `Crypt::encrypt('whsec_'+32)` (~244 ký tự; AES-256-CBC + MAC + `serialize`). **Không plaintext, không hash** | EP-01/02/03 → EP-01/02/03/05/07, job giải mã |
| `secret_generated_at` | datetime | NULL | 2 | Lần sinh / tái tạo gần nhất | Web → **chỉ EP-07** |
| `errors_refreshed_at` | datetime | NULL | 1 | 「最終更新」 tab 1 (#41030) | EP-01, EP-04 `refresh=1` → EP-01, EP-04. Entity JPA **không map** |
| `notify_errors_refreshed_at` | datetime | NULL | 2 | 「最終更新」 tab 2 | như trên |
| `created_at`, `updated_at` | timestamp | NULL | — | `updated_at` đổi ở **mọi lần mở màn** (DBM-05); job UPDATE native không đổi | Web → không ai đọc |

### 3.3 `webhook_relay_error`

Model `App\Models\WebhookRelayError` (`$timestamps = false`, `DISPLAY_LIMIT = 100`, `ERROR_MESSAGES` 7 khoá; web **không bao giờ ghi**); entity `WebhookRelayError.java` (`occurred_at = created_at = LocalDateTime.now()` giờ JVM).

| Cột | Kiểu | Null / Default | Ý nghĩa | UI |
|-----|------|---------------|---------|----|
| `id` | bigint unsigned AI | PK | | row-key |
| `bot_id` | int | NOT NULL | | lọc (session) |
| `channel` | tinyint | default **1** | 1 / 2 | lọc theo tab |
| `queue_id` | bigint unsigned | NULL | **Id bản ghi bảng nguồn** (tên gây hiểu nhầm): `callback_event.id` (ch.1) / `tag_history.id` hoặc `friend_info_history.id` của sự kiện **đầu lô** (ch.2) | — |
| `occurred_at` | datetime | NOT NULL | Lúc job **bỏ cuộc** (không phải lúc sự kiện phát sinh) | 「発生日時」 |
| `event_type` | varchar(255) | NOT NULL | ch.1 `callback_event.type` (NULL → `unknown`); ch.2 `tag` / `friend_info` | 「イベント種別」 |
| `error_code` | varchar(64) | NOT NULL | Mã nội bộ (§3.8.5) | 「エラー内容」 |
| `http_status` | smallint | NULL | NULL = không có response (kể cả timeout phía LME) | 「エラーコード」 |
| `created_at` | datetime | NULL | = `occurred_at` (trùng lặp) | — |

Index `idx_webhook_relay_error_list (bot_id, channel, occurred_at)` phục vụ đúng câu EP-04 (`ORDER BY occurred_at DESC, id DESC LIMIT 100`, không filesort). **Không có cơ chế dọn** (QA-008).

### 3.4 `webhook_relay_queue` (chỉ job)

Không có model web (đã xoá ở #40763); entity `WebhookRelayQueue.java` (không map `locked_by`, `locked_at`). `delivery_id` là **khoá gom lô**.

| Cột | Kiểu | Ý nghĩa thực tế |
|-----|------|----------------|
| `id` | bigint unsigned AI | Thứ tự dựng lại `events[]` |
| `bot_id` | int | |
| `channel` | tinyint, default 1 | 1 / 2 |
| `callback_event_id` | bigint unsigned NULL | **Id bảng nguồn cho cả 3 bảng** (tên lỗi thời) |
| `delivery_id` | char(36) | UUID header `X-Lme-Delivery-Id`, giữ qua 3 lần thử. ⚠ **Không index trong migration Laravel** |
| `event_type` | varchar(255) | Suy ra bảng nguồn |
| `payload` | longtext NULL | ch.1: nguyên body; ch.2: JSON **1 phần tử** `events[]` |
| `status` | tinyint, default 0 | 0 WAITING · 1 SENDING · 2 DONE · 3 FAILED · **4 IGNORE** |
| `attempt_count` | tinyint, default 0 | Số lần **đã** gửi (dòng mới = 1, tối đa 3) |
| `next_attempt_at` | datetime NULL | Lần 1: giờ JVM + 1 phút; lần sau: `NOW()` DB + 1 phút |
| `locked_by`, `locked_at` | — | **Cột chết** (DDL job bỏ) |
| `created_at`, `processed_at` | datetime NULL | Điều tra; không ai đọc |

Index (migration): `idx_webhook_relay_queue_poll (status, next_attempt_at, id)`, `idx_webhook_relay_queue_bot (bot_id, created_at)` (chờ job purge chưa tồn tại). DDL của job (gitignored) thêm `idx_webhook_relay_queue_delivery (delivery_id)` và bỏ `locked_*` ⇒ **2 DDL khác nhau** (DBM-01).

### 3.5 Bảng nguồn (cột liên quan)

| Bảng | Cột dùng cho relay | Ghi chú |
|------|-------------------|--------|
| `callback_event` (backenddb) | `id` (→ `queue_id`), `bot_id` (gate), `type` (→ `event_type`), `request` text (**payload kênh 1**, ≤65.535 byte), `status` (điều kiện quét), `status_sync` (cờ, **chỉ có ở entity + kế hoạch job**), `webhook_event_id` (không dùng cho relay) | `id` int(10) unsigned. `line_id`, `webhook_event_id`, `status_sync` **không có migration** |
| `tag_history` | `id` int unsigned (→ `queue_id`), `bot_id`, `line_user_id` (→ `lmessage_friend_id`), `tag_id`, `action` (1 add / 2 remove), `status_sync` + `idx_status_sync (status_sync, id)` | Không gửi `tag_name`, `trigger_*`, `created_at` (QA-014) |
| `friend_info_history` | `id` bigint unsigned, `bot_id`, `line_user_id`, `friend_information_setting_id` (→ `field_id`), `action` (1 create / 2 update / 3 clear), `new_value` (→ `value`), `status_sync` + index | Không gửi `old_value`, tên, trigger |

### 3.6 Ma trận CRUD theo tác nhân

| Tác nhân | `webhook_relay_setting` | `webhook_relay_error` | `webhook_relay_queue` | `callback_event` | `tag_history` / `friend_info_history` |
|---------|------------------------|----------------------|----------------------|------------------|--------------------------------------|
| EP-06 trang | — | — | — | — | — |
| EP-01 `GET /config` | R + **C/U** (secret lần đầu, 2 mốc, `updated_at`) | — | — | — | — |
| EP-02 `POST /save` | R (FOR UPDATE) + C/U (cột 1 kênh) | — | — | — | — |
| EP-03 `POST /regenerate-secret` | R + U (`signing_secret`, `secret_generated_at`) | — | — | — | — |
| EP-04 `GET /errors` | R (mốc); **C/U** khi `refresh=1` | R (100 dòng) | — | — | — |
| EP-05 `GET /secret` | R | — | — | — | — |
| EP-07 `GET /api/webhook-decode/{secret}` | R **toàn bảng** | — | — | — | — |
| Web `callbackWebHook` / `storeFakeCallbackEvent` | — | — | — | **C** | — |
| Web / job: luồng tag, 友だち情報 | — | — | — | — | **C** |
| `WebhookRelaySettingManager` (60s) | R toàn bảng | — | — | — | — |
| `HandleForwardCallbackEvent*` | U (bộ đếm kênh 1) | C | C | R + U `status_sync` | — |
| `HandleForwardLmeEvent*` | U (bộ đếm kênh 2) | C | C | — | R + U `status_sync` (+ R `line_user`) |
| `HandleRetryWebhookRelay*` | U (bộ đếm) | C | R + U | U `status_sync` | U `status_sync` |
| `HandlePostbackTask` (ngoài FA-047) | — | — | — | U `status` | — |

### 3.7 ER Diagram

Quan hệ đều là **logic** (không FK). `callback_event` ở **backenddb**, còn lại ở **linedb** ⇒ không transaction nào bao trùm 2 phía (R-10).

```mermaid
erDiagram
    bots ||..o| webhook_relay_setting : "bot_id (UNIQUE, 1 dòng/bot)"
    bots ||..o{ webhook_relay_error : "bot_id"
    bots ||..o{ webhook_relay_queue : "bot_id"
    bots ||..o{ callback_event : "bot_id (backenddb)"
    bots ||..o{ tag_history : "bot_id"
    bots ||..o{ friend_info_history : "bot_id"
    bots ||..o{ bot_contracts : "bot_id (gate job)"
    bots ||..o{ user_staff_bots : "bot_id"
    user_staff_bots }o..|| bot_role_access : "bot_id + role_id"
    bot_role_access }o..|| access_feature : "access_id (route webhookRelay)"
    access_feature ||..o{ access_feature : "parent (5 route con)"
    callback_event ||..o{ webhook_relay_error : "queue_id (channel 1)"
    tag_history ||..o{ webhook_relay_error : "queue_id (channel 2, tag, id đầu lô)"
    friend_info_history ||..o{ webhook_relay_error : "queue_id (channel 2, friend_info, id đầu lô)"
    callback_event ||..o| webhook_relay_queue : "callback_event_id (channel 1)"
    tag_history ||..o| webhook_relay_queue : "callback_event_id (channel 2, tag)"
    friend_info_history ||..o| webhook_relay_queue : "callback_event_id (channel 2, friend_info)"
    line_user ||..o{ tag_history : "line_user_id"
    line_user ||..o{ friend_info_history : "line_user_id"
    tags ||..o{ tag_history : "tag_id"
    friend_information_setting ||..o{ friend_info_history : "friend_information_setting_id"

    webhook_relay_setting {
        int id PK
        int bot_id UK
        varchar endpoint_url "kênh 1"
        tinyint is_enabled "kênh 1"
        int consecutive_failure_count "metric"
        varchar notify_endpoint_url "kênh 2"
        tinyint notify_is_enabled "kênh 2"
        int notify_consecutive_failure_count "metric"
        varchar signing_secret "ciphertext"
        datetime secret_generated_at
        datetime errors_refreshed_at "最終更新 kênh 1"
        datetime notify_errors_refreshed_at "最終更新 kênh 2"
    }
    webhook_relay_error {
        bigint id PK
        int bot_id
        tinyint channel
        bigint queue_id "id bảng nguồn"
        datetime occurred_at
        varchar event_type
        varchar error_code
        smallint http_status
    }
    webhook_relay_queue {
        bigint id PK
        int bot_id
        tinyint channel
        bigint callback_event_id "id bảng nguồn"
        char delivery_id "không index ở migration"
        varchar event_type
        longtext payload
        tinyint status "0-4"
        tinyint attempt_count
        datetime next_attempt_at
    }
    callback_event {
        int id PK
        int bot_id
        varchar type
        text request "body kênh 1"
        int status
        tinyint status_sync "chỉ entity"
    }
    tag_history {
        int id PK
        int bot_id
        int line_user_id
        int tag_id
        tinyint action
        tinyint status_sync
    }
    friend_info_history {
        bigint id PK
        int bot_id
        int line_user_id
        int friend_information_setting_id
        tinyint action
        varchar new_value
        tinyint status_sync
    }
```

### 3.8 Enum & state machine

#### 3.8.1 Kênh và trạng thái kênh

| `channel` | Hằng số | Tab | Bộ cột setting |
|:--------:|--------|-----|---------------|
| 1 | `CHANNEL_LINE` | 「LINE公式アカウントデータ転送」 | không tiền tố |
| 2 | `CHANNEL_LME` | 「L Messageデータ転送」 | `notify_*` + `signing_secret` |

| `is_enabled` / `notify_is_enabled` | Hiển thị | Job |
|:--:|---------|-----|
| 0 (default) | 「停止中」 `#D9D9D9` | Sự kiện → `status_sync = 4` |
| 1 | 「転送中」 `#52C41A` | Sẵn sàng **nếu** URL không rỗng **và** bot `is_deleted = 0`, không hết hạn > 7 ngày, hợp đồng chưa huỷ |

```
 停止中 (0) ──EP-02 is_enabled=1, URL hợp lệ bắt buộc──► 転送中 (1)   (reset failure_count = 0, auto_disabled_at = NULL của ĐÚNG kênh)
 転送中 ──EP-02 is_enabled=0 (URL có thể rỗng)──► 停止中             (không reset bộ đếm)
 転送中 ──EP-02 giữ bật──► 転送中                                      (không reset)
 Không có chuyển trạng thái tự động (Phase 1 không auto-disable)
```

#### 3.8.2 Dòng cấu hình và secret

```
[Không có dòng] ──EP-01 ensureSecret──────────► [Có dòng, có secret, 2 kênh TẮT, URL NULL]
       │        ──EP-02 lần đầu (INSERT+secret)► [Có dòng, có secret, kênh được lưu theo input]
       │        ──EP-04 refresh=1 (chỉ mốc)────► [Có dòng, KHÔNG secret] ──EP-01──► [có secret]
       └ EP-03 / EP-05 ⇒ 422 INVALID_PARAM
Secret: NULL ──sinh lần đầu──► S1 ──EP-03──► S2 ──EP-03──► S3 …  (web: Sn-1 hết hiệu lực ngay; job: ≤60s)
        Sx ──đổi APP_KEY──► "hỏng" (has_secret=true, mask=null) ──EP-03──► S mới
Dòng không bao giờ bị xoá bởi web (không có endpoint xoá).
```

#### 3.8.3 `status_sync` trên 3 bảng nguồn (không hiện trên UI)

| Giá trị | Hằng số | Ý nghĩa | Ai đặt |
|:------:|--------|---------|-------|
| NULL | — | Chưa xử lý (mặc định INSERT; **dữ liệu lịch sử trước tính năng cũng NULL**) | Web / `HistoryHelper`; job reset `1 → NULL` khi khởi động |
| 1 | `STATUS_SYNC_RUNNING` | Đã nạp queue in-memory / đang gửi | Scanner |
| 2 | `STATUS_SYNC_DONE` | Bên nhận trả 2xx | Worker / retry |
| 3 | `STATUS_SYNC_ERROR` | Bỏ cuộc, đã ghi `webhook_relay_error` | Worker / retry |
| 4 | `STATUS_SYNC_IGNORE` | Kênh tắt, bot hết hạn / xoá, webhook trùng | Scanner / worker / retry |
| 5 | `STATUS_SYNC_RETRY` | Đang chờ trong `webhook_relay_queue` | Worker |

```mermaid
stateDiagram-v2
  [*] --> NULL: INSERT (web hoặc HistoryHelper)
  NULL --> IGNORE_4: scanner - kênh tắt, bot hết hạn/xoá, webhook trùng
  NULL --> RUNNING_1: scanner - kênh bật
  RUNNING_1 --> NULL: khởi động lại job
  RUNNING_1 --> IGNORE_4: worker - kênh vừa bị tắt
  RUNNING_1 --> DONE_2: 2xx lần 1
  RUNNING_1 --> RETRY_5: timeout hoặc 5xx lần 1
  RUNNING_1 --> ERROR_3: lỗi không-retry, payload rỗng, ghi queue lỗi
  RETRY_5 --> DONE_2: 2xx lần 2 hoặc 3
  RETRY_5 --> ERROR_3: hết lượt hoặc lỗi không-retry
  RETRY_5 --> IGNORE_4: kênh tắt trong lúc chờ
  DONE_2 --> [*]
  ERROR_3 --> [*]
  IGNORE_4 --> [*]
```

Kênh 1: dòng có `status ∈ {0, 1, 100, 101}` ở nguyên `NULL` tới khi `HandlePostbackTask` xử lý xong. ⚠ Trạng thái trung gian `30/31` (media), `50` (image-map, postback giả do web ghi) **không bị loại**; giá trị lạ `3000` (14,3% dump), `200`, `102`, `103` được coi là "đã xử lý" (DBM-04).

#### 3.8.4 `webhook_relay_queue.status` (không hiện trên UI)

```mermaid
stateDiagram-v2
  [*] --> WAITING_0: worker INSERT (attempt 1, next +1 phút)
  WAITING_0 --> SENDING_1: retry scanner claimByDeliveryId
  SENDING_1 --> WAITING_0: timeout/5xx và attempt nhỏ hơn 3
  SENDING_1 --> WAITING_0: khởi động lại job
  SENDING_1 --> DONE_2: 2xx
  SENDING_1 --> FAILED_3: hết 3 lần, lỗi không-retry, body rỗng
  SENDING_1 --> IGNORE_4: kênh tắt hoặc bot hết hạn
  DONE_2 --> [*]
  FAILED_3 --> [*]
  IGNORE_4 --> [*]
```

Comment migration chỉ liệt kê `0..3` (thiếu `4 IGNORE` — ME-09).

#### 3.8.5 `error_code` ↔ 「エラー内容」 ↔ 「エラーコード」

| `error_code` (job ghi) | Điều kiện | `http_status` | Retry? | 「エラー内容」 | 「エラーコード」 |
|-----------------------|----------|--------------|:-----:|---------------|-----------------|
| `CONNECT_FAILED` | `UnknownHost`, `Connect`, `NoRouteToHost`, `SSL`, `IOException` khác | NULL | **Không** | 「接続できませんでした」 | 「—」 |
| `NOT_FOUND` | HTTP 404 | 404 | Không | 「転送先が見つかりません」 | 404 |
| `UNAUTHORIZED` | HTTP 401 / 403 | 401 / 403 | Không | 「認証エラー」 | 401 / 403 |
| `TIMEOUT` | Hết 10s một pha phía LME (`SocketTimeoutException`, `InterruptedIOException`) | **NULL** | Có | 「タイムアウト（10秒）」 | 「—」 |
| `TIMEOUT` | Bên nhận **trả về** 408 / 504 | 408 / 504 | Có | 「タイムアウト（10秒）」 | 408 / 504 |
| `UNAVAILABLE` | HTTP 503 | 503 | Có | 「転送先が一時的に応答できません」 | 503 |
| `SERVER_ERROR` | HTTP ≥ 500 khác (trừ 503, 504) | 5xx | Có | 「転送先でエラーが発生しました」 | 5xx |
| `HTTP_ERROR` | HTTP khác (3xx không follow, 4xx còn lại) | mã thật | Không | 「その他のエラー」 (web rơi về khoá `OTHER`) | mã thật |
| `UNKNOWN` | Exception không phải IO | NULL | Không | 「その他のエラー」 | 「—」 |
| `INVALID_PAYLOAD` | URL / body rỗng | NULL | Không | 「その他のエラー」 | 「—」 |
| `OTHER` | **Không có writer** (khoá fallback phía web) | — | — | 「その他のエラー」 (chuỗi tạm — C-04 nội bộ) | — |

Chuỗi 「タイムアウト（10秒）」 **khớp** timeout thật của job (đã phân xử M-01). "15 giây" và "TIMEOUT ghi 408" chỉ tồn tại ở tài liệu hợp đồng / comment migration lỗi thời (V-13).

#### 3.8.6 Hành động nguồn → `events[].action` (kênh 2)

| Bảng | `action` DB | `events[].action` |
|------|:----------:|-------------------|
| `tag_history` | 1 / 2 / khác | `add` / `remove` / `add` |
| `friend_info_history` | 1 create / 2 update | `set` (kèm `value = new_value`) |
| `friend_info_history` | 3 clear | `clear` (không có `value`) |

### 3.9 Lệch DDL / migration ↔ entity và cột chết (quan trọng)

| Mã | Điểm | Hệ quả | Mức |
|----|------|-------|-----|
| ME-16 / C-02 | `callback_event.status_sync`, `webhook_event_id` **không có migration** (web lẫn job); DDL chỉ ở script gitignored `data/task_40475/migration_40475.sql` | Môi trường thiếu cột ⇒ job kênh 1 lỗi; thiếu index `(status_sync, id)` ⇒ full scan bảng nóng | **Cao** (triển khai) |
| ME-06 / C-03 | `webhook_relay_queue`: migration Laravel **không** có index `delivery_id`, còn `locked_*`; DDL job có index, bỏ `locked_*` | 4 câu `WHERE delivery_id = ?` full scan trên bảng không bao giờ được dọn; môi trường tạo bảng bằng script job rồi `migrate` có thể lỗi "table exists" | **Cao** (hiệu năng) |
| ME-01 | 2 cột mốc 「最終更新」 không map trong entity | Không ảnh hưởng (job không cần) | Thấp |
| ME-04 | Comment entity "job chưa giải mã được secret" | Lỗi thời — job đã giải mã | Thấp |
| ME-07 / ME-08 / ME-09 / ME-11 / ME-12 | Comment migration: `callback_event_id` NULL với ch.2; `payload` NULL với ch.1; `status 0..3`; "TIMEOUT = 408"; "chỉ ghi sau 3 lượt" | Đều **sai** so với code job | Trung bình (gây hiểu nhầm) |
| §10.1 db-mapping | Cột chết / một chiều: `auto_disabled_at` ×2 (chỉ ghi NULL), bộ đếm lỗi ×2 (không ai đọc — không UI, không cảnh báo), `secret_generated_at` (chỉ EP-07), `locked_*`, `webhook_relay_error.queue_id` / `created_at`, `getChannelConfigForBot()` (code chết) | Metric "lỗi liên tiếp" tồn tại nhưng **vô dụng** với người dùng | Thấp |

---

## 4. Field Traceability Matrix

Hướng: **Đọc** (DB → UI), **Ghi** (UI → DB), **Lọc** (tham số WHERE), **Computed** (suy ra / logic). Không mục nào đối chiếu được sample data (bảng không có trong dump). Mã BR tham chiếu §5.

| # | UI element (tham số / khoá response) | Màn hình | DB Table.Column | Hướng | Validation | Business Rule |
|:-:|-------------------------------------|---------|-----------------|-------|-----------|---------------|
| 1 | Switch 「転送の状態」 kênh 1 (`channels[1].is_enabled` / `is_enabled`) | SCR-WHR-01 | `webhook_relay_setting.is_enabled` | Đọc (EP-01) / Ghi (EP-02) | `required\|boolean` → `!empty()` → 0/1 | BR-05, BR-15, BR-42 |
| 2 | Badge 「転送中」/「停止中」 kênh 1 | SCR-WHR-01 | `is_enabled` (theo giá trị switch **chưa lưu**) | Computed (client) | — | BR-05 (UI-05) |
| 3 | Input 「転送先URL」 kênh 1 (`endpoint_url`) | SCR-WHR-01 | `webhook_relay_setting.endpoint_url` varchar(1024) | Đọc / Ghi (trim, `''` → NULL) | FE luật 1–2; server 9 luật | BR-06…BR-14, BR-35 |
| 4 | (ẩn) `channel = 1` | SCR-WHR-01 | Chọn bộ cột không tiền tố (`COLUMNS_BY_CHANNEL[1]`) | Computed | `required\|integer\|in:1,2` | BR-05 |
| 5 | Switch 「転送の状態」 kênh 2 | SCR-WHR-02 | `notify_is_enabled` | Đọc / Ghi | như #1 | BR-05, BR-15, BR-42 |
| 6 | Badge kênh 2 | SCR-WHR-02 | `notify_is_enabled` (chưa lưu) | Computed (client) | — | BR-05 |
| 7 | Input 「転送先URL」 kênh 2 | SCR-WHR-02 | `notify_endpoint_url` | Đọc / Ghi | như #3; cho phép trùng kênh 1 | BR-06…BR-14, BR-35 |
| 8 | (ẩn) `channel = 2` | SCR-WHR-02 | Chọn bộ cột `notify_*` | Computed | như #4 | BR-05 |
| 9 | Ô 「署名シークレット」 mask (`secret_masked`, `has_secret`) | SCR-WHR-02 | `signing_secret` (giải mã → 6 ký tự đầu + `•`) | Đọc (Computed) | `has_secret = !empty(signing_secret)` | BR-17, BR-19, BR-20, BR-21 |
| 10 | Icon mắt — plaintext (EP-05 `secret`) | SCR-WHR-02 | `signing_secret` (giải mã) | Đọc + audit (file log) | `throttle:10,1`; `no-store` | BR-22, BR-37 |
| 11 | Icon sao chép | SCR-WHR-02 | `signing_secret` (EP-05 nếu chưa cache) | Đọc | như #10 | BR-22, BR-37, BR-38 |
| 12 | 「再生成」 → OK | SCR-WHR-02 / 03 | `signing_secret`, `secret_generated_at`, `updated_at` | Ghi (UPDATE) | Cần dòng tồn tại (422); confirm bắt buộc | BR-17, BR-23 |
| 13 | Cột 「発生日時」 (`occurred_at`) | SCR-WHR-01 / 02 | `webhook_relay_error.occurred_at` | Đọc (`Y/m/d H:i:s`) | Sort client-side | BR-25, BR-28, BR-40 |
| 14 | Cột 「イベント種別」 (`event_type`) | SCR-WHR-01 / 02 | `webhook_relay_error.event_type` (← `callback_event.type` / `tag` / `friend_info`) | Đọc | — | BR-28, BR-49 |
| 15 | Cột 「エラー内容」 (`reason`) | SCR-WHR-01 / 02 | `webhook_relay_error.error_code` → `reasonText()` | Đọc (Enum, server map) | Mã lạ → `OTHER` | BR-27 |
| 16 | Cột 「エラーコード」 (`http_status`) | SCR-WHR-01 / 02 | `webhook_relay_error.http_status` | Đọc (NULL → 「—」) | — | BR-28 |
| 17 | row-key (`id`) | SCR-WHR-01 / 02 | `webhook_relay_error.id` | Đọc | — | BR-25 |
| 18 | Lọc theo tab (`channel` query) | SCR-WHR-01 / 02 | `webhook_relay_error.bot_id` (session), `channel` | Lọc | `FILTER_VALIDATE_INT` + `in_array([1,2], strict)` | BR-01, BR-25, BR-26 |
| 19 | 「最終更新」 kênh 1 (`last_updated_at`) | SCR-WHR-01 | `webhook_relay_setting.errors_refreshed_at` | Đọc / Ghi (now, `Y/m/d H:i`; NULL → 「—」) | — | BR-29 |
| 20 | 「最終更新」 kênh 2 | SCR-WHR-02 | `notify_errors_refreshed_at` | Đọc / Ghi | — | BR-29 |
| 21 | 「最新に更新」 (`refresh=1`) | SCR-WHR-01 / 02 | UPDATE mốc của kênh + SELECT 100 dòng | Ghi + Đọc | `FILTER_VALIDATE_BOOLEAN` | BR-29 |
| 22 | Trạng thái rỗng 「転送エラーはありません」 | SCR-WHR-01 / 02 | 0 dòng `webhook_relay_error` | Đọc (Aggregated) | — | BR-25 (UI-08) |
| 23 | Badge 「接続できませんでした」 | SCR-WHR-01 / 02 | `error_code = 'CONNECT_FAILED'`, `http_status` NULL | Đọc (Enum) | — | BR-27, BR-47 |
| 24 | Badge 「転送先が見つかりません」 | SCR-WHR-01 / 02 | `'NOT_FOUND'`, 404 | Đọc (Enum) | — | BR-27 |
| 25 | Badge 「認証エラー」 | SCR-WHR-01 / 02 | `'UNAUTHORIZED'`, 401 / 403 | Đọc (Enum) | — | BR-27, BR-23 |
| 26 | Badge 「タイムアウト（10秒）」 | SCR-WHR-01 / 02 | `'TIMEOUT'`, NULL hoặc 408 / 504 | Đọc (Enum) | — | BR-27, BR-48 |
| 27 | Badge 「転送先でエラーが発生しました」 | SCR-WHR-01 / 02 | `'SERVER_ERROR'`, 5xx trừ 503/504 | Đọc (Enum) | — | BR-27 |
| 28 | Badge 「転送先が一時的に応答できません」 | SCR-WHR-01 / 02 | `'UNAVAILABLE'`, 503 | Đọc (Enum) | — | BR-27 |
| 29 | Badge 「その他のエラー」 | SCR-WHR-01 / 02 | `'HTTP_ERROR'` / `'UNKNOWN'` / `'INVALID_PAYLOAD'` (+ `OTHER` không writer) | Đọc (Enum fallback) | — | BR-27 |
| 30 | Mục quyền 「Webhook転送」 (màn phân quyền Staff — FA-035) | (ngoài FA-047) | `access_feature` (cha `route='webhookRelay'` + 5 con), `bot_role_access` | Đọc | — | BR-02, BR-03 |
| 31 | Nút 「使い方を見る」 | Khung trang | — (env `WEBHOOK_RELAY_DOCS_URL`) | — | — | BR-36 |

**Ghi ngầm** (không có element riêng trên UI):

| # | Tác nhân | DB Table.Column | Hướng | Ràng buộc | Business Rule |
|:-:|---------|-----------------|-------|----------|---------------|
| H-01 | Mở trang (EP-01) lần đầu | `webhook_relay_setting`: `bot_id`, `signing_secret`, `secret_generated_at`, `created_at` | Ghi (INSERT / UPDATE) | Transaction + `FOR UPDATE`; không sinh đè | BR-16, BR-18 |
| H-02 | Mở trang (EP-01) **mọi lần** | `errors_refreshed_at`, `notify_errors_refreshed_at`, `updated_at` | Ghi (UPDATE) | Không khoá | BR-29 |
| H-03 | 「保存する」 TẮT→BẬT | `consecutive_failure_count` / `notify_*` = 0; `auto_disabled_at` / `notify_*` = NULL | Ghi | Chỉ đúng kênh | BR-15 |
| H-04 | 「保存する」 khi chưa có dòng | INSERT kèm `signing_secret`, `secret_generated_at` (kể cả lưu kênh 1 / trạng thái TẮT) | Ghi | | BR-18 |
| H-05 | Mọi request (Staff) | `user_access_bot` | Ghi (INSERT) | 1 lần/ngày | (chung, không thuộc FA-047) |
| H-06 | LINE webhook | `callback_event` (backenddb) | Ghi (INSERT) | Bỏ qua request toàn `delivery` | BR-34 |
| H-07 | Thao tác tag / 友だち情報 | `tag_history`, `friend_info_history` | Ghi (INSERT) | — | BR-45 |
| H-08 | Job scanner / worker / retry | `*.status_sync` (3 bảng nguồn) | Ghi (UPDATE native) | Entity `insertable/updatable = false` | BR-42, BR-43 |
| H-09 | Job worker (lần 1 hỏng timeout/5xx) | `webhook_relay_queue` (INSERT), retry UPDATE `status`, `attempt_count`, `next_attempt_at`, `processed_at` | Ghi | Claim nguyên tử theo `delivery_id` | BR-47 |
| H-10 | Job bỏ cuộc | `webhook_relay_error` (INSERT) + bộ đếm lỗi +1 | Ghi | 1 dòng / request hỏng | BR-31, BR-49 |
| H-11 | `php artisan access-feature:webhook-relay` | `access_feature` (1 cha + 5 con; có thể `increment('order')` các mục cùng nhóm) | Ghi | Idempotent, không transaction | BR-02 |

---

## 5. Business Rules

BR-01…BR-34 giữ **đúng số hiệu** của `web/logic-spec.md` §12 (BR-11b là luật chèn thêm #44660, nằm giữa BR-11 và BR-12, đồng bộ cả 2 file). BR-35…BR-41 là quy tắc FE / UI bổ sung từ `ui/ui-spec.md`; BR-42…BR-50 là quy tắc job bổ sung từ `job/job-spec.md`. ⚠ `BR-xx` trong comment source là mã **nội bộ** dev, khác nghĩa (§12.1).

| # | Quy tắc | Mô tả hợp nhất (UI + code + DB + job) | Tầng | Nguồn | Tin cậy |
|---|--------|-------------------------------------|------|------|--------|
| BR-01 | Bot lấy từ session | `bot_id = session('current_bot_id')`; client không gửi được; mọi truy vấn bảng relay có `WHERE bot_id` | BE | `WebhookRelayController.php:17-19, 40, 214-216`; `WebhookRelaySettingRepository.php:17-48` | Cao |
| BR-02 | Quyền 2 tầng | Owner **hoặc** Staff `status = 1`, **và** `checkBotHasPermission('webhookRelay')`. Staff `is_bot_invite` còn phải qua whitelist route (6 dòng `access_feature` do command tạo) | BE | `WebhookRelayController.php:242-257`; `functions.php:198-227, 5044-5094`; `AdminAccess.php:61-73` | Cao (code) / Trung bình (Staff `is_admin = 1` tuỳ đường vào bot) |
| BR-03 | Quyền mức màn | Không có quyền riêng cho 「再生成」 / xem plaintext; Staff được cấp làm được tất cả (BA chấp nhận — QA-spec-005, R-003 nội bộ). Command **không** cấp sẵn cho role nào | BE | `WebhookRelayController.php:23-24`; `AddAccessFeatureWebhookRelay.php:16-20` | Cao |
| BR-04 | 1 cấu hình / bot | UNIQUE `bot_id`; 1 dòng chứa cả 2 kênh; web không bao giờ xoá dòng | DB | migration setting `:54`; `WebhookRelaySetting.php:7-13` | Cao |
| BR-05 | Lưu chỉ 1 kênh | EP-02 chỉ ghi cặp cột của `channel` gửi lên; kênh kia giữ nguyên; FE gửi kênh của tab đang mở | BE + FE | `WebhookRelayService.php:141-145`; `webhook-relay.js:293-311` | Cao |
| BR-06 | URL bắt buộc khi bật | Rỗng chỉ lỗi khi `is_enabled = 1`; tắt + rỗng ⇒ lưu NULL | FE + BE | `WebhookUrlValidator.php:39-41`; `WebhookRelayService.php:124-126, 143` | Cao |
| BR-07 | Chỉ HTTPS | Bắt đầu đúng `https://` (phân biệt hoa thường) | FE + BE | `WebhookUrlValidator.php:43-45`; `webhook-relay.js:285` | Cao |
| BR-08 | Độ dài URL | ≤ 1024 ký tự (`mb_strlen`), khớp `varchar(1024)` | BE + DB | `WebhookUrlValidator.php:47-49`; `WebhookRelaySetting.php:55` | Cao |
| BR-09 | Không khoảng trắng | Chặn `\s` và U+3000 ở mọi vị trí | BE | `WebhookUrlValidator.php:55-57` | Cao |
| BR-10 | Cấu trúc URL & host | `FILTER_VALIDATE_URL` + host là IP literal hoặc tên miền RFC 1123 | BE | `:62-64, 89-97` | Cao |
| BR-11 | Chỉ cổng 443 | Không ghi cổng hoặc `:443` | BE | `:27, 83-86` | Cao |
| BR-11b | Không được là webhook LME (#44660) | Sau khi chuẩn hoá path (decode `%xx`, `\` / `%5C` → `/`, gộp `//`, rút gọn `.` / `..`), path chứa `/line/callback/add` ⇒ `URL_NOT_ALLOWED`. Mọi domain, mọi `bot_id`, không phân biệt hoa/thường; áp cả khi kênh tắt; chạy **trước** DNS/SSRF (luật 8 ở `api-spec.md`). Chặn vòng lặp LME→LME. ⚠ Chỉ chặn **lúc lưu ở web** — job không kiểm lại, cấu hình cũ trỏ webhook LME vẫn được chuyển tiếp (follow-up #43730 + ticket job) | BE | `WebhookUrlValidator.php` `isLmeWebhookUrl()` (nhánh `ai_studio_fixbug_44660` @`676e01b687`) | Cao (code) — phạm vi mọi domain chờ PO (REQ-008) |
| BR-12 | Chống SSRF lúc lưu (fail-closed) | Host phải phân giải (A + AAAA, fallback `gethostbyname`) ra ≥ 1 IP và **mọi** IP phải public (`NO_PRIV_RANGE \| NO_RES_RANGE`). Chỉ kiểm **lúc lưu**; job không kiểm lại (R-01) | BE | `:104-113, 124-165` | Cao (logic) — bị thủng bởi SEC-03 |
| BR-13 | Cho phép trùng URL giữa 2 kênh | Không kiểm trùng | BE | `WebhookRelayService.php:124-125` | Cao |
| BR-14 | Validate URL cả khi tắt | URL không rỗng luôn qua luật 2–9 | BE | `WebhookUrlValidator.php:37-71` | Cao |
| BR-15 | Reset bộ đếm khi bật lại | TẮT→BẬT (hoặc dòng chưa có mà bật) ⇒ `failure_count = 0`, `auto_disabled_at = NULL` của đúng kênh | BE | `WebhookRelayService.php:147-152` | Cao |
| BR-16 | Ghi cấu hình an toàn đồng thời | Transaction + `SELECT … FOR UPDATE`; trùng khoá 1062 ⇒ chạy lại transaction 1 lần (áp dụng EP-01 `ensureSecret` và EP-02) | BE + DB | `WebhookRelayService.php:134-183, 446-482` | Cao |
| BR-17 | Định dạng secret | `whsec_` + 32 ký tự base62 bằng `random_int` (CSPRNG, ~190 bit) = 38 ký tự | BE | `:45-49, 517-527` | Cao |
| BR-18 | Secret sinh sớm | Sinh ở lần mở màn đầu (EP-01) hoặc lần lưu đầu (EP-02, kể cả lưu kênh 1 / TẮT) — cái nào trước; không bao giờ sinh đè. Lệch QA-spec-003 (sinh ở lần lưu đầu) — chờ BA | BE | `:157-165, 427-494` | Cao |
| BR-19 | Secret mã hoá khả nghịch | `Crypt::encrypt` bằng `APP_KEY` (job giải mã cùng khoá); không plaintext, không hash | BE | `:161, 229, 458`; `WebhookSignatureHelper.java:115-146` | Cao |
| BR-20 | Secret chỉ cho kênh 2 | Kênh 1 không ký, không secret; ô secret chỉ ở tab 2 | BE + FE | `WebhookRelaySetting.php:11-12`; `index.blade.php:82-109` | Cao |
| BR-21 | Chỉ trả mask trong luồng thường | EP-01/02/03 trả mask (6 ký tự đầu + `•` ⇒ không lộ ký tự ngẫu nhiên nào); plaintext chỉ qua EP-05 | BE | `WebhookRelayService.php:101-103, 206-208, 244-247, 499-511` | Cao |
| BR-22 | Xem plaintext có kiểm soát | Always-viewable (D-03 nội bộ); audit mỗi lần; `throttle:10,1`; `Cache-Control: no-store`; FE không lưu storage | BE + FE | `:357-374`; `WebhookRelayController.php:194`; `routes/web.php:668-669` | Cao |
| BR-23 | Tái tạo secret | Cần dòng đã có; FE confirm bắt buộc; web: secret cũ mất hiệu lực ngay, không ân hạn (QA-spec-017). ⚠ Job cache 60s ⇒ kênh 2 còn gửi secret cũ ≤60s (V-12) | BE + FE | `WebhookRelayService.php:213-251`; `webhook-relay.js:101, 454-485`; `WebhookRelaySettingManager.java:28` | Cao |
| BR-24 | Không log secret, có audit | Audit `user_id, bot_id, ip, before/after` (chỉ URL + enabled) khi lưu; audit riêng init / regenerate / view secret — **file log**, không có bảng audit | BE | `:186-193, 234-239, 364-368, 486-490, 556-564` | Cao |
| BR-25 | Danh sách lỗi theo kênh, 100 dòng | `WHERE bot_id, channel ORDER BY occurred_at DESC, id DESC LIMIT 100`; không phân trang / lọc | BE | `WebhookRelayError.php:29`; `WebhookRelayErrorRepository.php:21-29` | Cao |
| BR-26 | `channel` của EP-04 nghiêm ngặt | Chỉ số nguyên trọn vẹn 1 hoặc 2 (`"01"`, `"1abc"`, `""` bị từ chối) (#40533) | BE | `WebhookRelayController.php:152-163` | Cao |
| BR-27 | Dịch mã lỗi phía server | `error_code` → chuỗi JP; mã lạ ⇒ 「その他のエラー」; FE không tự map, không nhận `error_code` | BE | `WebhookRelayError.php:41-62`; `WebhookRelayErrorResource.php:26-27` | Cao |
| BR-28 | Định dạng hiển thị lỗi | `occurred_at` `Y/m/d H:i:s`; `http_status` NULL ⇒ 「—」; `event_type` nguyên văn | BE + FE | `WebhookRelayErrorResource.php:23-29`; `index.blade.php:154-164` | Cao |
| BR-29 | Mốc 「最終更新」 server-side, tách kênh | Đóng mốc khi vào màn (cả 2 kênh) hoặc 「最新に更新」 (kênh hiện tại); đổi tab chỉ đọc; giờ server, `Y/m/d H:i`; dùng chung cho mọi người trong bot (#41030) | BE | `WebhookRelayService.php:52, 78-92, 255-350` | Cao |
| BR-30 | Web không gửi ra ngoài, không ghi queue | Toàn bộ gửi / retry / ghi lỗi do job; web không đọc `status_sync` | BE | `config/sns-line.php:1283-1289`; migration queue `:23-24` | Cao |
| BR-31 | Chỉ lưu lỗi cuối cùng | Không lưu lần gửi thành công; 1 request hỏng = 1 dòng (kênh 2: 1 dòng cho cả lô). Tổng tối đa **3 lần gửi** (1 + 2, cách 1 phút), **chỉ** thử lại khi timeout / HTTP ≥ 500; lỗi không-retry ghi **ngay sau lần 1** — lệch wording UI (V-11) | Job | `Constants.java:221-236`; `WebhookRelayResult.java:53-61`; `index.blade.php:169` | Cao |
| BR-32 | Không tự tắt kênh (Phase 1) | Cột `auto_disabled_*` không ghi; job chỉ tăng / reset bộ đếm; web chỉ reset khi bật lại | Job + BE | migration setting `:18, 32, 38`; `WebhookRelaySettingRepository.java:11-14` | Cao |
| BR-33 | Tab mặc định & cảnh báo rời tab | Vào / F5 luôn tab 1; rời tab có thay đổi chưa lưu ⇒ confirm; Cancel quay lại, OK bỏ thay đổi | FE | `webhook-relay.js:35, 193-233`; `index.blade.php:12-13` | Cao |
| BR-34 | Kênh 1 chuyển tiếp body thô | `callback_event.request` lưu nguyên body LINE (1 dòng / lần gọi, #40888); request toàn `delivery` hoặc events rỗng **không** được lưu ⇒ không chuyển tiếp | BE | `BotController.php:2055-2058, 2075-2148` | Cao |
| BR-35 | Validate URL phía client | Trim; chỉ kiểm luật 1–2 (rỗng-khi-bật, `https://`); sai thì không gửi; lỗi inline không tự xoá khi sửa (chỉ xoá khi lưu lại / đổi tab) | FE | `webhook-relay.js:273-291` | Cao |
| BR-36 | Hành vi nút lưu & trợ giúp | 「保存する」 luôn hiện ở cả 2 tab, `:disabled="isSaving"` + chặn double-submit, **không** disable khi không có thay đổi hoặc khi đang nạp cấu hình; thành công ở lại màn + toast + cập nhật `savedState`. 「使い方を見る」 mở `docsUrl` tab mới, rỗng ⇒ không làm gì | FE | `index.blade.php:43-46, 114-117`; `webhook-relay.js:293-340, 595-602` | Cao |
| BR-37 | Cache plaintext secret phía client | Lấy lazy qua EP-05 ở lần đầu cần; giữ trong state Vue (không storage); xoá sau lưu / tái tạo; chế độ hiện **không** reset khi đổi tab | FE | `webhook-relay.js:12-13, 75, 322-328, 365-421, 466-478` | Cao |
| BR-38 | Sao chép secret | `navigator.clipboard.writeText` → fallback `<textarea>` ẩn + `execCommand('copy')`; toast thành công / thất bại | FE | `webhook-relay.js:423-448` | Cao |
| BR-39 | Xử lý 403 AJAX | Mọi AJAX nhận 403 ⇒ toast 「この権限は許可されていません。」 ⇒ `setTimeout` 3s ⇒ `/admin/home`; các mã khác ⇒ toast chung (lưu thì không có fallback) | FE | `webhook-relay.js:580-593` | Cao |
| BR-40 | Sort client-side | Chỉ cột 「発生日時」; so sánh chuỗi; trên ≤100 dòng đã tải; `order` thiếu ⇒ `desc`; không gọi server | FE | `webhook-relay.js:559-578` | Cao |
| BR-41 | Hiển thị menu | Mục 「Webhook転送」 hiện với mọi user khi có bot đang chọn — không kiểm quyền, không có feature flag web | Blade | `sidebar.blade.php:79, 209-245` | Cao |
| BR-42 | Gate chuyển tiếp của job | Kênh "sẵn sàng" ⇔ setting tồn tại + kênh bật + URL không rỗng **và** bot tồn tại, `is_deleted = 0` (loại cả bot tạm `= 2`), không hết hạn > 7 ngày, hợp đồng chưa huỷ (`bot_contracts.status ≠ 3`). Gate chạy ở scanner, worker và retry | Job | `WebhookRelaySettingManager.java:61-96`; `Bot.java:288-300` | Cao |
| BR-43 | Kênh 1 chờ LME xử lý xong | Chỉ quét `callback_event.status NOT IN (0,1,100,101)` — chuyển tiếp **sau** `HandlePostbackTask`, bất kể kết quả nghiệp vụ; `status ∈ {11,111}` (webhook trùng) ⇒ IGNORE | Job | `CallbackEventRepository.java:43-48`; `HandleForwardCallbackEventManager.java:151-159`; `Constants.java:175-216` | Cao |
| BR-44 | Hợp đồng gửi kênh 1 | `POST endpoint_url`, body = `callback_event.request` nguyên văn (không parse, không bọc); header `Content-Type`, `Accept`, `X-Lme-Timestamp` (epoch ms lúc gửi), `X-Lme-Delivery-Id`; **không** ký, **không** chuyển `X-Line-Signature` gốc. Bên nhận phân biệt bot qua chính URL | Job | `HandleForwardCallbackEventTask.java:25, 73-129, 175-184`; `WebhookRelayApiClient.java:99-112` | Cao |
| BR-45 | Hợp đồng gửi kênh 2 | `{"events":[…]}`, mỗi phần tử: `lmessage_friend_id`, `line_friend_id` (null nếu line_user đã xoá), `type` (`tag`/`friend_info`), `action`, `tag_id` (tag) hoặc `field_id` + `value` (friend info, bỏ `value` khi `clear`); không có `option_id`. Gom theo bot + bảng nguồn, giữ thứ tự id, ≤1000 (thực tế ≤500); tag và friend info không chung request | Job | `WebhookLmeEvent.java:17-147`; `HandleForwardLmeEventManager.java:204-367` | Cao (code) / Trung bình (hợp đồng chính thức — G-07) |
| BR-46 | `X-Lme-Signature` = secret thô | Giá trị header = secret đã giải mã `whsec_…` (Phương án A), không phụ thuộc body; cache giải mã theo ciphertext; thiếu / sai `LARAVEL_APP_KEY` ⇒ **vẫn gửi không header** | Job | `WebhookSignatureHelper.java:22-26, 79-110`; `HandleForwardLmeEventTask.java:101-105` | Cao |
| BR-47 | Cơ chế thử lại | Giãn cố định 1 phút (không backoff); giữ **cùng `delivery_id`** qua 3 lần (at-least-once, bên nhận tự dedupe); URL + secret lấy theo cấu hình **hiện tại**; tắt kênh / bot hết hạn trong lúc chờ ⇒ IGNORE, không ghi lỗi; `CONNECT_FAILED` không retry; OkHttp `retryOnConnectionFailure(false)` | Job | `HandleRetryWebhookRelayTask.java:78-146`; `WebhookRelayApiClient.java:47-67` | Cao |
| BR-48 | Timeout & tiêu chí thành công | 10 giây cho **mỗi pha** connect / write / read, **không** có `callTimeout`; thành công = HTTP 200–299, không đọc body phản hồi; lỗi đọc ≤500 ký tự body để log | Job | `WebhookRelayApiClient.java:63-68, 116-127` | Cao |
| BR-49 | Ghi lỗi & bộ đếm | Khi bỏ cuộc: INSERT 1 dòng `webhook_relay_error` (`occurred_at` = giờ JVM lúc bỏ cuộc; kênh 2 đại diện bằng sự kiện đầu lô) + `consecutive_failure_count`/`notify_*` + 1; thành công ⇒ reset 0 (có guard `<> 0`) | Job | `HandleForwardLmeEventTask.java:200-222`; `WebhookRelaySettingRepository.java:19-38` | Cao |
| BR-50 | Độ trễ & đảm bảo giao hàng | Cấu hình web có hiệu lực ở job sau ≤60s (bot ≤2 phút); sự kiện bị IGNORE **không gửi bù**; **không đảm bảo thứ tự** (QA-006); at-least-once; chỉ an toàn khi chạy **1 instance** job | Job | `WebhookRelaySettingManager.java:28, 98-118`; `BotManager.java:18`; `WebhookRelayQueue.java:30-31` | Cao |

---

## 6. API Endpoints

### 6.1 Danh sách

Xác thực bằng **session cookie** portal (không token) cho EP-01…EP-06. Route ở `routes/web.php:659-670` (group `/admin`, `:105`) và `routes/api.php:440-446`. `src/web/index/routes.md` sinh từ nhánh cũ nên **không chứa** các route này (G-14).

| EP | Method | URI | Route name | Controller@Action | Middleware riêng | Mô tả | Màn hình |
|----|--------|-----|-----------|-------------------|-----------------|-------|---------|
| EP-01 | GET | `/admin/webhook-relay/config` | `webhookRelay.config` | `Admin\WebhookRelayController@getConfig` | — | Cấu hình 2 kênh + secret mask. **GET có ghi DB** (secret lần đầu + đóng mốc 2 kênh) | SCR-WHR-01/02 (mounted) |
| EP-02 | POST | `/admin/webhook-relay/save` | `webhookRelay.save` | `@save` | FormRequest `WebhookRelaySaveRequest`, CSRF | Lưu URL + bật/tắt của **1** kênh | SCR-WHR-01/02 「保存する」 |
| EP-03 | POST | `/admin/webhook-relay/regenerate-secret` | `webhookRelay.regenerateSecret` | `@regenerateSecret` | CSRF | Tái tạo secret (không trả plaintext) | SCR-WHR-02 → 03 |
| EP-04 | GET | `/admin/webhook-relay/errors?channel=1\|2[&refresh=1]` | `webhookRelay.errors` | `@getErrors` | — | 100 lỗi gần nhất của 1 kênh; `refresh=1` đóng mốc kênh đó | SCR-WHR-01/02 card 「転送エラー」 |
| EP-05 | GET | `/admin/webhook-relay/secret` | `webhookRelay.secret` | `@getSecret` | **`throttle:10,1`** | Plaintext secret + audit, `no-store` | SCR-WHR-02 (mắt / sao chép) |
| EP-06 | GET | `/admin/webhook-relay` | `webhookRelay` | `@index` | — | Render trang + `window.WEBHOOK_RELAY_CONFIG` | SCR-WHR-01 |
| **EP-07** | GET | `/api/webhook-decode/{secret}` | `webhookRelay.debugDecode` | `Api\WebhookRelayDebugController@decode` | nhóm `api` (chỉ `bindings`), **`throttle:20,1`** | **DEBUG** — tra ngược plaintext secret → `bot_id` + ciphertext. **KHÔNG xác thực, mở ở mọi môi trường** | Không có UI |

Middleware chung EP-01…EP-06: `web`, `NotifyChatworkRequestTimeSlow`, `admin_access`, `https_protocol` (no-op), `check_remember_token` (§2.1). URL endpoint AJAX không viết cứng trong JS — controller dựng bằng `route()`.

### 6.2 Định dạng response & lỗi chung

| Loại | Body | HTTP |
|------|------|------|
| Thành công | `{"success": true, "data": {...}}` | 200 |
| Lỗi nghiệp vụ (EP-02…05) | `{"success": false, "errors": [{"field", "error_code", "message"}]}` | 422 |
| Thiếu quyền (EP-01…05) | `{"success": false, "error_code": "PERMISSION_DENIED", "message": "この権限は許可されていません。"}` | 403 |
| Chưa đăng nhập (AJAX) | `{"success":false,"data":null,"message":"ログインが必要です。",…}` | 401 |
| `users.role` không hợp lệ | `{"success":false,…,"message":"この操作を行う権限がありません。"}` | 403 |
| Đổi mật khẩu ở phiên khác | `{"result":false,"status":false,"success":false,"message":"ログイン情報が変更されましたので、再度ログインしてください。",…}` (`errors` là chuỗi ⇒ FE TypeError — BUG-05) | **200** |
| Staff `is_bot_invite` không có route trong whitelist | Redirect `/admin/home` + xoá bot khỏi session | 302 |
| CSRF hỏng (POST) | Trang lỗi `TokenMismatchException` | 419 |
| `QueryException` khác 1062 | Exception Handler mặc định | 500 |

| `error_code` | `field` | HTTP | Thông điệp JP |
|---|---|---|---|
| `URL_REQUIRED` | `endpoint_url` | 422 | 「転送先URLを入力してください。」 |
| `URL_NOT_HTTPS` | `endpoint_url` | 422 | 「httpsで始まるURLを入力してください。」 |
| `URL_TOO_LONG` | `endpoint_url` | 422 | 「転送先URLは1024文字以内で入力してください。」 (tạm) |
| `URL_NOT_ALLOWED` | `endpoint_url` | 422 | 「このURLは転送先に指定できません。」 (tạm) |
| `INVALID_PARAM` | `request` / `channel` / `secret` | 422 | 「エラーが発生しました。」 |
| `PERMISSION_DENIED` | — | 403 | 「この権限は許可されていません。」 |
| `INTERNAL_ERROR` | — | — | Chỉ fallback của `buildError()`, không có đường sinh trực tiếp |

Thứ tự kiểm ở EP-02: FormRequest chạy **trước** controller ⇒ người không có quyền gửi payload sai nhận 422 thay vì 403 (SEC-09).

### 6.3 Chi tiết rút gọn

> Request / response mẫu đầy đủ xem [`web/api-spec.md`](web/api-spec.md) §3.

**EP-01** `GET /config` — không tham số. 200: `data.last_updated_at{"1","2"}` (`Y/m/d H:i` hoặc `''`), `data.channels{"1":{is_enabled,endpoint_url}, "2":{is_enabled,endpoint_url,secret_masked}}`, `data.has_secret`. Side effect: `ensureSecret` + `touchLastUpdatedAt([1,2])`.

**EP-02** `POST /save` (form-urlencoded, `X-CSRF-TOKEN`) — `channel` (`required|integer|in:1,2`), `is_enabled` (`required|boolean`), `endpoint_url` (`nullable|string` + 9 luật nghiệp vụ, dừng ở lỗi đầu tiên). 200: `data{channel, is_enabled, endpoint_url, has_secret, secret_masked}` (đọc lại từ DB). Lỗi: 422 (§6.2), 403, 419, 500.

**EP-03** `POST /regenerate-secret` — không tham số nghiệp vụ. 200: `data{secret_masked, secret_plain: null, regenerated_at (ISO-8601)}`. 422 `INVALID_PARAM` (`field = secret`) khi bot chưa có dòng.

**EP-04** `GET /errors` — `channel` (bắt buộc, số nguyên trọn vẹn 1|2), `refresh` (`FILTER_VALIDATE_BOOLEAN`, giá trị lạ ⇒ false). 200: `data{channel, items[{id, occurred_at, event_type, reason, http_status}], last_updated_at}`. **Không** trả `error_code`, `queue_id`, `channel` từng dòng. 422 `INVALID_PARAM` (`field = channel`).

**EP-05** `GET /secret` — 200 `data{secret}` (38 ký tự) + `Cache-Control: no-store`; **200 `{secret: null}`** khi giải mã lỗi (BUG-01); 422 khi chưa có dòng / secret; 429 khi vượt 10/phút.

**EP-06** `GET /admin/webhook-relay` — render view, truyền `webhookRelayConfig{endpoints, channels{line:1,lme:2}, docsUrl}`; không còn truyền `botId` (#41030). 302 về `/admin/home` khi không có bot / không qua `canAccess()`; 302 `/logout` khi chưa đăng nhập.

**EP-07** `GET /api/webhook-decode/{secret}` ⚠ **DEBUG, đang mở**
- Ràng buộc route `[A-Za-z0-9_\-]+`; controller yêu cầu tiền tố `whsec_` (400 `INVALID_SECRET_FORMAT`, thông điệp **tiếng Việt** lộ ra ngoài).
- `findSettingByPlainSecret`: `chunkWithSecret(500)` duyệt **mọi** dòng có secret (không lọc `bot_id`), `Crypt::decrypt` từng dòng, so `hash_equals` ⇒ O(số bot có secret) mỗi request.
- 200 `{bot_id, plain_secret, signing_secret (ciphertext), secret_generated_at}`; 404 `SECRET_NOT_FOUND`; 429 > 20/phút/IP.
- Guard `if (!config('app.debug')) abort(404);` **bị comment** (`WebhookRelayDebugController.php:49-51`); comment route `routes/api.php:440` vẫn ghi "chỉ sống khi APP_DEBUG=true" — **sai so với code**. Commit `3f3c7ddf95` có trong `release_step_20260930_v2` và `release_staging_20260910`.
- Secret nằm trên **URL path** ⇒ lọt vào access log web server / proxy.

**Endpoint ngoài màn có liên quan**: `POST /line/callback/add/{bot_id}` (`routes/web.php:2554`, `BotController@callbackWebHook`) — điểm vào dữ liệu kênh 1 (§2.8.1).

---

## 7. Background Jobs

### 7.1 Vì sao cần job & kiểu giao tiếp

Gọi HTTP sang bên thứ 3 (timeout 10s/pha, tối đa 3 lần gửi cách 1 phút) không thể chạy trong request PHP nhận webhook LINE (LINE yêu cầu trả 200 nhanh) hay request thao tác tag. Toàn bộ việc chuyển tiếp do worker `linect-service` đảm nhận.

**Kiểu giao tiếp: DB polling trên bảng nguồn** — Laravel **không ghi hàng đợi nào** (nhánh INSERT `webhook_relay_queue` đã gỡ ở #40763). Job quét thẳng cột cờ `status_sync` trên `callback_event`, `tag_history`, `friend_info_history`; `webhook_relay_queue` chỉ là **hàng đợi thử lại** do chính job ghi. Không message broker, không scheduler annotation — vòng lặp `while(true)` + `Thread.sleep` theo khuôn `StoppableTask`.

### 7.2 Thành phần & luồng

| Thành phần | Flag | Luồng | Nhiệm vụ | File |
|-----------|------|:----:|---------|------|
| `WebhookRelaySettingManager` | Bật khi 1 trong 2 kênh bật | 1 | Nạp **toàn bộ** `webhook_relay_setting` vào map (volatile) mỗi **60s**; lần đầu đồng bộ trong `init()`; nạp lỗi giữ map cũ + Chatwork; `isReady()` chặn scanner tới lần nạp đầu thành công; gate dùng chung (BR-42) | `helper/WebhookRelaySettingManager.java` |
| `HandleForwardCallbackEventManager` | `ENABLE_FORWARD_WEBHOOK_CALLBACK` | 1 scanner + 10 worker | Kênh 1 | `threads/webhook/HandleForwardCallbackEventManager.java` + `…Task.java` |
| `HandleForwardLmeEventManager` | `ENABLE_FORWARD_WEBHOOK_LME` | 2 scanner + 10 worker | Kênh 2 | `threads/webhook/HandleForwardLmeEventManager.java` + `…Task.java` |
| `HandleRetryWebhookRelayManager` | Bật khi 1 trong 2 kênh bật | 1 scanner + 5 worker | Thử lại cả 2 kênh | `threads/webhook/HandleRetryWebhookRelayManager.java` + `…Task.java` |
| **Tổng mặc định** | | **31 luồng** | Trên `Executors.newCachedThreadPool()` dùng chung toàn app (không giới hạn) | `AppMain.java:196-210, 319-330` |

Queue scanner → worker là `LinkedList` + `synchronized` (không phải `BlockingQueue`); worker rảnh `sleep(2000)`.

### 7.3 Polling

| Scanner | Câu quét | Batch | Nhịp nghỉ |
|---------|----------|:----:|-----------|
| Kênh 1 | `SELECT * FROM callback_event WHERE status_sync IS NULL AND status NOT IN (0,1,100,101) ORDER BY id ASC LIMIT 500` | 500 | 200ms nếu đủ 500; 1000ms nếu ít hơn; 1s nếu cache chưa sẵn sàng hoặc queue > 200; 10s nếu exception |
| Kênh 2 — tag | `SELECT * FROM tag_history WHERE status_sync IS NULL ORDER BY id ASC LIMIT 500` | 500 | Như trên, ngưỡng queue > 50 **lô** |
| Kênh 2 — friend info | `SELECT * FROM friend_info_history WHERE status_sync IS NULL ORDER BY id ASC LIMIT 500` | 500 | Như trên |
| Retry | `SELECT delivery_id FROM webhook_relay_queue WHERE status = 0 AND next_attempt_at <= NOW() GROUP BY delivery_id ORDER BY MIN(id) ASC LIMIT 50` | 50 delivery | 200ms có việc; 5s rảnh; 1s nếu queue > 50; 10s nếu exception |

Thông lượng trần mỗi scanner ≈ 500 dòng / 200ms ≈ **2.500 dòng/giây**; vượt trần thì độ trễ tăng không giới hạn. Quét theo `delivery_id` để không cắt đôi lô kênh 2.

### 7.4 Processing chain

Chi tiết từng bước ở §2.8.1 (kênh 1), §2.8.2 (kênh 2), §2.8.3 (retry). Tóm tắt:

```
Kênh 1: callback_event (status đã xử lý) → scanner: IGNORE / RUNNING (bulk) → worker: gate → POST body thô
        → 2xx DONE | timeout/≥500 RETRY + INSERT queue | lỗi khác ERROR + INSERT error
Kênh 2: *_history → 2 scanner: IGNORE / resolve line_id / RUNNING (bulk) → gom lô theo bot (≤1000)
        → worker: gate → POST {"events":[…]} + X-Lme-Signature → như kênh 1 (N dòng queue / 1 dòng error cho cả lô)
Retry:  queue WAITING → claim SENDING → gate → POST lại (cùng delivery_id, URL/secret hiện tại)
        → DONE | hẹn lại (+1 phút, tối đa tới lần 3) | FAILED + INSERT error | IGNORE
```

### 7.5 Ma trận kết cục

| Kết quả gọi HTTP | `status_sync` nguồn | `webhook_relay_queue` | `webhook_relay_error` | Bộ đếm lỗi |
|------------------|:------------------:|-----------------------|:---------------------:|------------|
| 2xx ở lần 1 | `2` | — | — | reset 0 |
| Timeout / ≥500 ở lần 1 | `5` | INSERT `status 0, attempt 1` | — | — |
| Lỗi khác ở lần 1 (`CONNECT_FAILED`, 4xx, 3xx không follow, `INVALID_PAYLOAD`) | `3` | — | 1 dòng | +1 |
| 2xx ở lần 2 / 3 | `2` | `2 DONE` | — | reset 0 |
| Timeout / ≥500 ở lần 2 | `5` (giữ) | `0`, `attempt 2`, hẹn +1 phút | — | — |
| Bất kỳ lỗi ở lần 3, hoặc lỗi không-retry ở lần 2 | `3` | `3 FAILED` | 1 dòng | +1 |
| Kênh tắt / bot hết hạn trước khi gửi | `4` | `4 IGNORE` (nếu đang ở retry) | — | — |

### 7.6 HTTP outbound

| Hạng mục | Hành vi thực tế | Tin cậy |
|----------|-----------------|--------|
| Method / body | `POST`, `application/json; charset=utf-8`; kênh 1 body thô, kênh 2 `{"events":[…]}` | Cao |
| `X-Lme-Timestamp` | Epoch **mili giây lúc gửi** (không phải lúc phát sinh), lấy mới mỗi lần thử; **không được ký** ⇒ không chống replay | Cao |
| `X-Lme-Delivery-Id` | UUID, giữ nguyên qua 3 lần thử ⇒ bên nhận dedupe | Cao |
| `X-Lme-Signature` | **Chỉ kênh 2**; giá trị = **secret thô** `whsec_…` (không HMAC, không phụ thuộc body). Hợp đồng web `docs/api/webhook-relay-outbound-contract.md:177-202` (HMAC hex) **lỗi thời** | Cao |
| Timeout | 10s mỗi pha connect / write / read; không `callTimeout` ⇒ tổng có thể > 10s | Cao |
| Thành công | HTTP 200–299; không đọc body | Cao |
| Redirect | OkHttp mặc định **đi theo** 301/302/303 (đổi POST → GET, bỏ body), không theo 307/308 với POST; header tuỳ biến (gồm `X-Lme-Signature`) **được giữ** khi đổi host, kể cả hạ HTTPS → HTTP. 2 client khác trong repo (`RequestHelper`, `NotifyUtils`) đều tắt redirect | Trung bình (phiên bản OkHttp bắc cầu — G-04) |
| SSRF lúc gửi | **Không kiểm** (không resolve IP, không chặn dải nội bộ, không giới hạn cổng) — web ghi chú job "BẮT BUỘC kiểm lại lúc gửi" nhưng không được hiện thực | Cao |
| Log | Có: id nguồn, bot, delivery_id, attempt, HTTP status, thời gian, kích thước body, **URL đích ở mọi request**, ≤500 ký tự body lỗi. Không: body request, giá trị secret | Cao |

### 7.7 Xử lý lỗi, phục hồi, dừng

| Tình huống | Xử lý |
|-----------|-------|
| Exception ở vòng quét | Log + Chatwork + `sleep(10s)`, luồng không chết (không giới hạn tần suất Chatwork) |
| Exception lọt khỏi `actionForward` / `actionRetry` | Log + Chatwork + `sleep(60s)`; **sự kiện đang xử lý bị bỏ dở** ở `RUNNING` / `SENDING` tới lần khởi động sau (R-09) |
| Ghi `webhook_relay_queue` thất bại | Chuyển sang ghi lỗi luôn (`failWithoutRetry`) |
| Ghi `webhook_relay_error` / cập nhật queue trong retry thất bại | Chỉ log, nuốt exception |
| Thiếu / sai `LARAVEL_APP_KEY` | Log + Chatwork 「Kênh 2 forward không có chữ ký!」 lúc khởi động; **vẫn gửi** không header |
| Khởi động | `resumeStuckRow()`: `status_sync 1 → NULL` (3 bảng), queue `1 → 0` — reset **mọi** dòng, chỉ đúng khi 1 instance |
| Dừng | `requestStop()` cho 3 manager, chờ tối đa 300s; request HTTP đang chạy được làm xong; phần tử còn trong queue in-memory trả về ở lần khởi động sau. `kill -9` giữa lúc gọi HTTP ⇒ có thể gửi trùng (R-08) |

### 7.8 Liên kết thao tác web → hiệu lực ở job

| Thao tác web | Trường thay đổi | Độ trễ ở job | Người dùng thấy |
|-------------|----------------|-------------|----------------|
| Mở màn (EP-01) | Tạo dòng + secret; 2 mốc | ≤60s | Không đổi hành vi job (2 kênh mặc định TẮT) |
| Bật + lưu URL kênh 1 / kênh 2 (EP-02) | `is_enabled` / `notify_is_enabled`, URL; reset bộ đếm | ≤60s | Sự kiện **mới** được chuyển tiếp; sự kiện trong khoảng trễ bị IGNORE, **không gửi bù** |
| Tắt kênh | `is_enabled = 0` | ≤60s | Ngừng gửi; sự kiện đang chờ retry → IGNORE, **không** hiện ở danh sách lỗi |
| Đổi URL | `endpoint_url` / `notify_endpoint_url` | ≤60s | Lần thử lại của sự kiện cũ **cũng** đi tới URL mới |
| 「再生成」 (EP-03) | `signing_secret` | ≤60s | Job còn gửi secret cũ tới 60s (R-06) |
| Thao tác tag / thông tin bạn bè (bất kỳ đâu) | INSERT `*_history` | ~1–3s | Bên thứ 3 nhận `{"events":[…]}` |
| LINE gửi webhook | INSERT `callback_event` → `HandlePostbackTask` đổi `status` | Vài giây (sau khi LME xử lý) | Bên thứ 3 nhận nguyên body LINE |
| Xem 「転送エラー」 (EP-04) | Đọc `webhook_relay_error` | Lỗi không-retry: ngay; lỗi retry: ~2 phút | Bảng 4 cột |

### 7.9 Rủi ro triển khai liên quan job (tóm tắt — chi tiết §9.2)

- Flag job mặc định TẮT ⇒ web vẫn cho bật kênh ⇒ 「転送中」 giả (§9.2 #12).
- Bật flag lần đầu ⇒ cày qua toàn bộ lịch sử `status_sync IS NULL` (§9.2 #9); cần chạy script recover (gitignored `data/task_40475/recover_40475.sql`) **trước** khi bật.
- Thiếu `callback_event.status_sync` / index ⇒ lỗi hoặc full scan (§9.2 #10).
- Chạy > 1 instance ⇒ gửi trùng (§9.2 #20).

---

## 8. Phụ thuộc chéo (Cross-references)

### 8.1 Shared components đã đăng ký

**FA-047 không dùng shared component nào trong registry** (SC-001 Template Message, SC-002 Tag Selector, SC-003 Friend Filter/Segment, SC-004 Action Settings, SC-005 Rich Text / Message Editor, SC-006 Delivery Target Selector, SC-007 Schedule/Timer Settings). Ghi chú: kênh 2 chuyển tiếp **sự kiện** gắn tag nhưng UI không có bộ chọn tag (không phải SC-002); các hành động 「アクション設定」 (SC-004) gắn tag / đổi thông tin bạn bè **là nguồn sự kiện** kênh 2 vì chúng ghi `tag_history` / `friend_info_history` (Trung bình — G-09).

### 8.2 Ứng viên shared component (đã ghi ở `features/shared/pending-refs.md`, mục FA-046 + FA-047)

| Ứng viên | Vị trí ở FA-047 | Dùng chung với | Trạng thái đề xuất |
|---------|----------------|---------------|-------------------|
| **Masked Credential Field** (che mặc định + mắt lấy plaintext lazy qua API có audit + throttle + sao chép; FA-047 thêm 「再生成」 có confirm) | SCR-WHR-02 「署名シークレット」 (mask `whsec_` + 32 `•`, throttle 10/phút) | **FA-046** SCR-API-01 cột 「APIキー」 (prefix + 12×• + last4, throttle 30/phút); liên quan FA-044 SCR-CHB-03 (đã comment). Khác biệt: FA-046 có `lme-tooltip` + `aria-label`, FA-047 **không** (UI-12) | **Cao**, đủ 2 tính năng cùng release — đề xuất tạo SC |
| **Copy-to-clipboard Field** | SCR-WHR-02 nút sao chép (`webhook-relay.js:423-448`) | FA-044, FA-045, FA-017, FA-030, FA-046. Biến thể: giá trị bí mật **lấy lazy từ server** trước khi ghi clipboard | Đã đủ điều kiện; gom 1 SC |
| **Risk Confirm Modal** | **Không dùng** — 「再生成」 dùng `window.confirm` native | FA-044, FA-045, FA-046 (`lme-modal` + `lme-button-risk`) | Ghi nhận **ngoại lệ / không nhất quán** của FA-047 (UI-13) |
| **lme-ui Design System** | 10 component; lần đầu ghi nhận `lme-tab-horizontal` (emit `input` trước `select`), `lme-switch`, `lme-status`, `lme-table` (`sortable`, `@sort-change`, `empty-text`, `max-height`, slot `cell-{key}`), `lme-title` | FA-045, FA-046 | Đề xuất gom 1 SC; nguồn tham chiếu: `resources/views/component-base/*` |
| Enable Switch + Status Badge 「転送の状態」 | SCR-WHR-01/02 | Chưa thấy ở spec khác (`chat_setting_v2.blade.php` có `lme-switch` — chưa đối chiếu) | Thấp, chờ xác nhận |
| Error Log Card có 「最終更新」 + 「最新に更新」 | Card 「転送エラー」 | (trùng nhãn với Header Delivery Counter FA-030, khác bản chất) | Thấp |
| Unsaved-change Guard khi đổi tab | `webhook-relay.js:193-233` | Có thể có ở FA-041 (8 tab) | Thấp |
| AJAX Permission-denied Handler (403 → toast → 3s → `/admin/home`) | `webhook-relay.js:580-593` | Chưa có handler dùng chung trong hệ thống | Thấp |

Không dùng: Pagination 「N件表示」 (giới hạn cứng 100), Date Range Picker, Step Indicator. Modal chặn toàn cục `#modalWebhook*` của layout có thể xuất hiện (không phải SC).

### 8.3 Tính năng liên quan

| Tính năng | Quan hệ |
|----------|---------|
| **FA-030 「ホーム」** | Chung điểm vào `BotController@callbackWebHook`, bảng `callback_event`, job `HandlePostbackTask` (quyết định `status` mà scanner kênh 1 chờ). ⚠ **Spec FA-030 cần cập nhật**: trên nhánh này web đã lưu **nguyên body** (không còn chỉ `$body[0]`, `$body[1]`) và **đã ghi `webhook_event_id`** (#40888, commit `c89b0a960c`, `bfdc2d8cf5`) ⇒ phát hiện "dedup inert" của FA-030 có thể đã được khắc phục ở nhánh mới. Lỗ hổng không kiểm `X-Line-Signature` (SEC-02) đã có từ 2019, nay bị **khuếch đại** bởi kênh 1 |
| **FA-044 「LINE公式アカウント入れ替え」** | (1) Mốc neo vị trí menu quyền: command đặt 「Webhook転送」 ngay sau mục này (dump chưa có mục ⇒ rơi về `order = 42` cuối nhóm 「システム設定」 — DBM-11). (2) `empty("0")` short-circuit ở `callbackWebHook` trong cửa sổ đổi bot ⇒ sự kiện bị bỏ qua thì cũng không bao giờ được chuyển tiếp. (3) Đổi LOA xoá `callback_event WHERE bot_id` ⇒ `webhook_relay_error.queue_id` có thể trỏ tới dòng đã xoá (DBM-13). (4) Khuôn Risk Confirm Modal |
| **FA-012 「タグ管理」** (+ mọi luồng gắn/gỡ tag) | `tag_history` là nguồn sự kiện kênh 2 (`type = tag`, `tag_id`) |
| **FA-015 「友だち情報管理」** (+ màn chi tiết bạn bè) | `friend_info_history` là nguồn sự kiện kênh 2 (`type = friend_info`, `field_id = friend_information_setting_id`). Payload chỉ có `set` / `clear` (thiếu `today`, `point_*`… — R-13) |
| **FA-046 「API連携」** | Cùng release; mục sidebar ngay trên; cùng mẫu Masked Credential + Copy. Khác: FA-047 **cấp được quyền Staff** (command đặt `menu_id`), FA-046 thì không. `throttle:10,1` (EP-05) và `throttle:30,1` (reveal FA-046) **dùng chung bộ đếm theo user**. Public API của FA-046 (`/do_action`, `TRIGGER_API`) ghi lịch sử ⇒ hệ thống ngoài gọi API sẽ **nhận lại notify của chính mình** qua kênh 2 (vòng phản hồi R-23) |
| **FA-035 「スタッフ管理」** | Màn phân quyền role: mục 「Webhook転送」 nhóm 「システム設定」 (dòng `access_feature` cha có `menu_id`) |
| **「接続設定」** `/admin/setting-bot/{id}` (**chưa có mã FA** — không gán FA-036, vì FA-036 trong index = 「マイページ」 `/admin/setting`) | Mục sidebar liền trước (cách 「API連携」). Không có liên kết dữ liệu trực tiếp với FA-047 |
| **FA-041 「チャット設定」** | Chung `HandlePostbackTask` / `callback_event`; có thể dùng chung mẫu Unsaved-change Guard / `lme-switch` (chưa đối chiếu) |
| **FA-045 「新規LOA接続」 v5** | Khuôn `lme-ui` + Risk Confirm Modal; bot tạm `is_deleted = 2` bị gate job loại (BR-42) |
| **System Admin 「他社webhook管理」** (`/admin/revenue/webhook-competitors`, task #33865, bảng `webhook_competitors`, cột `bots.tool_webhook_endpoint`; portal System Admin **chưa quét**, chưa có mã FS) | **Không có liên kết code** (grep `WebhookRelay`/`webhook_relay` trong controller / service / command của màn này = 0). Chỉ cùng chủ đề webhook: màn đó theo dõi LOA trỏ webhook LINE sang công cụ đối thủ; FA-047 cho phép giữ LME làm webhook chính và chuyển tiếp ra ngoài. Ghi nhận để tránh nhầm lẫn |
| Middleware chung `admin_access` / Sidebar Admin v2 / layout `layout.admin.main` | Hạ tầng chung; side effect `user_access_bot`; modal chặn toàn cục |

### 8.4 Hệ thống ngoài

| Hệ thống | Quan hệ |
|---------|---------|
| Công cụ bên ngoài của khách (endpoint HTTPS) | Nhận dữ liệu; phải dedupe theo `X-Lme-Delivery-Id`, xác thực kênh 2 bằng so chuỗi `X-Lme-Signature` |
| LINE Platform | Nguồn kênh 1 |
| Chatwork | Cảnh báo exception job; `NotifyChatworkRequestTimeSlow` (EP-02 tra DNS đồng bộ có thể kích hoạt) |

---

## 9. Bảo mật & Bug

### 9.1 Các hạng mục bảo mật ĐẠT

| Hạng mục | Kết quả | Bằng chứng |
|---------|--------|-----------|
| IDOR | **Đạt** — 2 lớp: `bot_id` chỉ từ session + `canAccess()` owner/Staff | `WebhookRelayController.php:17-19, 214-257` |
| CSRF cho POST | **Đạt** — EP-02/03 không nằm trong `$except` | `VerifyCsrfToken.php:14-54` |
| Sinh secret | **Đạt** — CSPRNG `random_int`, ~190 bit | `WebhookRelayService.php:517-527` |
| Lưu secret | **Đạt** — mã hoá tại chỗ, không plaintext; mask không lộ ký tự ngẫu nhiên | `:161, 229, 458, 499-511` |
| Secret trong log | **Đạt** — web và job không log giá trị secret | `WebhookRelayService.php:555-564`; `WebhookSignatureHelper.java:106-109` |
| Cache response plaintext | **Đạt** — `Cache-Control: no-store` ở EP-05 | `WebhookRelayController.php:194` |
| Race tạo dòng / sinh secret đôi | **Đạt** — transaction + row lock + retry 1062 | `WebhookRelayService.php:134-183, 446-482` |
| Validate `channel` | **Đạt** — số nguyên trọn vẹn (#40533) | `WebhookRelayController.php:152-163` |
| URL fail-closed khi DNS lỗi | **Đạt** (#40728) — nhưng xem SEC-03 | `WebhookUrlValidator.php:104-107` |
| Rate limit xem plaintext | **Có** (10/phút/user) | `routes/web.php:668-669` |

### 9.2 Vấn đề tồn tại (đã gộp trùng, xếp theo mức độ)

Mã gốc: `SEC-xx` / `BUG-xx` = logic-spec §14; `R-xx` = job-spec §10; `UI-xx` = ui-spec "Bất thường"; `DBM-xx` = db-mapping §14; `V-xx` = validation-report.

| # | Mức độ | Vấn đề | Mã gốc | Bằng chứng | Tin cậy | Đề xuất |
|:-:|-------|-------|-------|-----------|--------|--------|
| 1 | **Nghiêm trọng** (bảo mật) | **Endpoint debug EP-07 mở công khai**: không auth/session; tra ngược plaintext secret → `bot_id` + ciphertext + `secret_generated_at`; mỗi request giải mã toàn bộ secret (DoS O(N)); secret nằm trên URL path (lọt access log); thông điệp lỗi tiếng Việt lộ ra ngoài | SEC-01, R-15 (phần debug), V-03 | `WebhookRelayDebugController.php:44-51`; `routes/api.php:440-446` (comment `:440` sai); `Kernel.php:45-48`; commit `3f3c7ddf95` | Cao (code) / chưa rõ production (G-01) | Bỏ comment guard **hoặc** xoá route + controller; kiểm bản deploy |
| 2 | **Nghiêm trọng** (bảo mật) | **Job không chống SSRF lúc gửi + đi theo redirect**: DNS rebinding hoặc endpoint trả 302 tới `169.254.169.254` / `10.x` ⇒ server job gửi request vào mạng nội bộ; HTTP status hiện ở 「エラーコード」 ⇒ có thể dò dịch vụ nội bộ. Kế hoạch job tự liệt kê là P0 còn mở | R-01, SEC-04, D-08, M-06, V-04 | `WebhookRelayApiClient.java:63-68, 89-138`; `WebhookUrlValidator.php:21-22`; `ai-plan_mode/task_40475_spec_job.md:213-215` | Cao (thiếu kiểm) / Trung bình (redirect của thư viện) | `followRedirects(false)` + `followSslRedirects(false)`; resolve + kiểm IP / cổng 443 lúc gửi |
| 3 | **Nghiêm trọng** (nghiệp vụ / bảo mật) | **Cơ chế xác thực kênh 2 mâu thuẫn 3 nguồn**: UI 「署名を付与…この値を検証」, hợp đồng web HMAC hex, job gửi **secret thô**. Khách verify HMAC ⇒ từ chối 100%; secret đi trong mọi request (ai đọc log/proxy phía nhận là giả mạo được); `X-Lme-Timestamp` không ký ⇒ không chống replay | V-02, UI-22, R-14a, R-15, M-05, GAP-04 | `WebhookSignatureHelper.java:22-26, 79-82`; `index.blade.php:107`; contract `:177-202` | Cao | Quyết định V-02 (§10.2) |
| 4 | **Cao** (bảo mật) | **Webhook LINE không kiểm `X-Line-Signature`**: `bot_type = 0` tự tính rồi tự so; `bot_type = 1` không kiểm; header không lưu. Ai biết `bot_id` (số tuần tự) có thể POST sự kiện giả ⇒ lưu `callback_event` ⇒ kênh 1 chuyển tiếp nguyên văn, không ký — bên nhận không phân biệt được | SEC-02, R-05, M-08, V-04 | `BotController.php:2046-2054, 2066-2072`; `routes/web.php:2554`; `VerifyCsrfToken.php:15` | Cao | Verify `X-Line-Signature` thật trước khi bật kênh 1 |
| 5 | **Cao** (bảo mật) | **Redirect mang `X-Lme-Signature` (secret thô) sang host khác**, kể cả hạ HTTPS → HTTP | R-02 | `WebhookRelayApiClient.java:99-114` | Trung bình | Như #2 |
| 6 | **Cao** (mất dữ liệu im lặng) | **301/302/303 ⇒ GET không body**; đích cuối trả 2xx ⇒ job ghi `DONE`, không có dòng lỗi | R-03 | `WebhookRelayApiClient.java:114-120` | Trung bình | Như #2; coi 3xx là lỗi |
| 7 | **Cao** (sai lệch dữ liệu) | **Cache cấu hình 60s**: (a) bật kênh ⇒ sự kiện ≤60s đầu IGNORE vĩnh viễn; (b) tắt ⇒ vẫn gửi ≤60s; (c) đổi URL ⇒ gửi URL cũ ≤60s; (d) 「再生成」 ⇒ còn gửi secret cũ ≤60s, bên nhận 401 ⇒ `UNAUTHORIZED` không retry ⇒ mất lô. Trạng thái bot cache 2 phút | R-06, V-07, V-12, M-10, BR-23 | `WebhookRelaySettingManager.java:28, 98-118`; `BotManager.java:18`; `WebhookRelayService.php:213-216` | Cao | Quyết định V-12 (§10.2) |
| 8 | **Cao** (khả dụng) | **Nghẽn dây chuyền do 1 endpoint chết**: mỗi timeout giữ 1 worker ≥10s (không giới hạn tổng); 10 worker + queue FIFO chung **mọi bot**; queue > 200 thì scanner dừng ⇒ 1 bot lưu lượng cao trỏ URL treo làm chậm **tất cả** bot. Không cô lập theo bot, không circuit breaker, không auto-disable | R-04 | `HandleForwardCallbackEventManager.java:35, 48, 62-64, 91-98`; `WebhookRelayApiClient.java:63-68` | Cao | `callTimeout`, hàng đợi theo bot, circuit breaker |
| 9 | **Cao** (rủi ro triển khai) | **Phát lại lịch sử khi bật flag**: không mốc bắt đầu; dữ liệu cũ `status_sync = NULL`; dump: 99,98% `callback_event` dạng mảng cũ, có payload Zalo / Meta ⇒ có thể gửi ra ngoài dữ liệu lịch sử, sai định dạng LINE, của nền tảng khác — không thu hồi được. Script recover gitignored | R-17, DBM-03, R-B1, GAP-02 | `HandleForwardCallbackEventManager.java:27-28`; `ai-plan_mode/task_40475_spec_job.md:275-284`; db-mapping §5.4 | Cao (dump) / Trung bình (production) | Chạy recover (đánh `status_sync = 4` dữ liệu cũ) **trước** khi bật; cân nhắc mốc `created_at ≥ thời điểm bật kênh` (G-03) |
| 10 | **Cao** (rủi ro triển khai) | **DDL thiếu / lệch**: `callback_event.status_sync`, `webhook_event_id` + index `(status_sync, id)` không có migration ở cả 2 repo; `webhook_relay_queue` có 2 DDL (bản Laravel thiếu index `delivery_id`, còn `locked_*`) ⇒ full scan bảng nóng / bảng không dọn | GAP-01, G-02, DBM-01, DBM-02, ME-06, ME-16, C-02, C-03 | `CallbackEventRepository.java:30-48`; `WebhookRelayQueueRepository.java:36-77`; `task_40475_retry_queue.md:81-90` | Cao (code) / Trung bình (production) | Đưa DDL vào migration; DBA `SHOW CREATE TABLE` (G-02) |
| 11 | **Cao** (xác suất thấp) | **Ghi đè cấu hình thật bằng giá trị mặc định**: không khoá form khi EP-01 chưa trả về; bấm 「保存する」 sớm ⇒ gửi `is_enabled = 0`, URL rỗng ⇒ tắt chuyển tiếp + xoá URL đã lưu | UI-01 | `webhook-relay.js:87, 143-176, 294-311`; `index.blade.php:116` | Cao | Disable nút / form khi `isLoadingConfig` |
| 12 | **Trung bình** (nghiệp vụ / vận hành) | **「転送中」 giả khi flag job tắt**: web không có flag, luôn cho bật kênh; job mặc định `ENABLE_FORWARD_WEBHOOK_* = 0` ⇒ không quét, không gửi, **không ghi lỗi** ⇒ người dùng tưởng đang chuyển tiếp; dữ liệu tồn đọng `status_sync = NULL` dồn lại cho lần bật flag (#9). Bảng lỗi cũng không có trạng thái "đang chờ thử lại" | (tổng hợp của compiler từ job-spec §1.3, `config/sns-line.php:1283-1289`, db-mapping §11.2; G-01) | `ConfigFile.java:144-146, 325-326`; `AppMain.java:319-330` | Cao (code) / Trung bình (production) | Đồng bộ thời điểm mở menu với bật flag; hoặc hiện cảnh báo khi job chưa hoạt động |
| 13 | **Trung bình** (bảo mật) | **Bypass SSRF lúc lưu**: `NO_PRIV_RANGE \| NO_RES_RANGE` (PHP 7.2) chấp nhận IPv4-mapped IPv6 (`::ffff:127.0.0.1`, `::ffff:169.254.169.254`), `100.64.0.0/10`, `198.18.0.0/15`, `224.0.0.0/4`, NAT64 `64:ff9b::7f00:1`, 6to4 `2002:7f00:1::1` — `https://[::ffff:127.0.0.1]/x` lưu thành công. Nguy hiểm khi kết hợp #2 | SEC-03, V-21, M-06 | `WebhookUrlValidator.php:89-97, 126-128, 158-165`; chạy `filter_var` PHP 7.2.0 CLI | Cao (validator) / Trung bình (tác động) | Chặn tường minh các dải; chuẩn hoá IPv6 nhúng IPv4 |
| 14 | **Trung bình** | **Wording 「最大3回まで再送…3回とも失敗したものだけを記録」 lệch**: tổng 3 lần gửi (1 + 2); chỉ retry timeout / ≥500; lỗi khác ghi ngay sau lần 1 | UI-21, R-14b, X-07, DBM-D11, V-08, V-11 | `index.blade.php:169`; `Constants.java:221-223`; `WebhookRelayResult.java:53-61` | Cao | Quyết định V-11 (§10.2) |
| 15 | **Trung bình** | **Kênh 2: 1 dòng lỗi cho cả lô ≤500 sự kiện** (`queue_id` / `event_type` của sự kiện đầu) ⇒ bảng lỗi không phản ánh số sự kiện mất, không truy được các sự kiện còn lại | R-14c, 02-N1 | `HandleForwardLmeEventTask.java:200-217`; `HandleRetryWebhookRelayTask.java:202-205` | Cao | Ghi số sự kiện / danh sách id; hoặc nêu rõ trên UI |
| 16 | **Trung bình** | **Lỗi mạng tạm thời không retry**: mọi `IOException` (connection reset, keep-alive chết, SSL chập chờn, DNS lỗi tạm) ⇒ `CONNECT_FAILED` ⇒ bỏ cuộc sau 1 lần | R-07 | `WebhookRelayResult.java:53-61`; `WebhookRelayApiClient.java:67, 182-188` | Cao (logic) / Trung bình (tần suất) | Cho `CONNECT_FAILED` vào nhóm retryable |
| 17 | **Trung bình** | **Gửi trùng với `delivery_id` khác** (bên nhận không dedupe được): job bị kill giữa lúc gọi HTTP, hoặc 2xx xong nhưng UPDATE `status_sync = 2` lỗi ⇒ kẹt RUNNING ⇒ khởi động lại gửi với UUID mới | R-08 | `HandleForwardCallbackEventTask.java:94, 101`; `HandleForwardCallbackEventManager.java:135-144` | Cao | Sinh `delivery_id` xác định từ id nguồn |
| 18 | **Trung bình** | **Row kẹt tới lần restart**: exception trong `actionForward` để RUNNING; lỗi nuốt ở retry để SENDING; NPE do race cache (`getSetting()` đọc trước gate) | R-09, R-21 | `HandleForwardCallbackEventTask.java:62-66, 77-78`; `HandleRetryWebhookRelayTask.java:148-168` | Cao (logic) / Thấp (xác suất NPE) | Phục hồi theo thời gian khi job đang chạy |
| 19 | **Trung bình** | **Mất sự kiện khi crash giữa "đánh RETRY" và "INSERT queue"** (2 DB khác nhau, không transaction): `status_sync = 5` không có dòng queue, không bị `resumeStuckRow` đụng tới ⇒ treo vĩnh viễn, không dòng lỗi | R-10 | `HandleForwardCallbackEventTask.java:152-165`; `HandleForwardLmeEventTask.java:163-177` | Cao (logic) / Thấp (xác suất) | Job dọn `status_sync = 5` mồ côi |
| 20 | **Trung bình** | **Chỉ an toàn 1 instance**: scanner không giành dòng nguyên tử; `resumeStuckRow` reset mọi RUNNING/SENDING ⇒ 2 tiến trình cùng bật flag (chồng lấn khi deploy, tiến trình "mode BACKEND") gửi trùng | R-11 | `CallbackEventRepository.java:43-61`; `WebhookRelayQueueRepository.java:79-88` | Cao (code) / Thấp (phụ thuộc deploy) | Xác nhận vận hành (G-10) |
| 21 | **Trung bình** | **Body webhook > 65.535 byte bị cắt cụt** (`callback_event.request` TEXT, `strict = false`) ⇒ kênh 1 gửi JSON hỏng; chỉ có `logError` | R-12, BUG-07 | `BotController.php:2129-2138`; `HandleForwardCallbackEventTask.java:185-191` | Cao | Đổi kiểu cột / kiểm JSON trước khi gửi |
| 22 | **Trung bình** | **Hợp đồng kênh 2 chưa đủ**: friend info chỉ `set`/`clear` (không có `today`, `point_*`); không `option_id`; gửi `tag_id` đơn trong khi plan ghi `tag_ids[]`; `line_friend_id` có thể null; `field_id` âm/dương chưa chốt (QA-015) | R-13, G-07 | `WebhookLmeEvent.java:36-37, 75, 114-120`; `task_40475_spec_job.md:110, 172, 264` | Cao (code) / Trung bình (hợp đồng thật) | Đối chiếu tài liệu gửi khách |
| 23 | **Trung bình** (hiệu năng) | **Khuếch đại đọc/ghi bảng nóng**: mọi dòng của **mọi** bot (đa số không dùng tính năng) bị `UPDATE status_sync = 4`; `SELECT *` kéo cả `request` ≤64KB của 500 dòng kể cả dòng sẽ IGNORE | R-16 | `HandleForwardCallbackEventManager.java:111-113, 162-164`; `HandleForwardLmeEventManager.java:214-217, 269-272` | Cao (code) / Trung bình (tác động) | Lọc theo bot có bật trước khi `SELECT *` |
| 24 | **Trung bình** | **Câu quét kênh 1 không loại trạng thái trung gian** `30/31` (media), `50` (postback giả do web ghi) ⇒ có thể forward trước khi LME xử lý xong; giá trị lạ `3000` (14,3% dump), `200`, `102`, `103` coi là đã xử lý; 68 dòng kẹt `status = 1` trong dump nằm mãi ở dải `NULL` ⇒ mỗi vòng đọc lại | DBM-04 | db-mapping §9.7; `HandlePostbackTask.java:206, 248-255`; `UserController.php:3202-3209` | Trung bình | Liệt kê tường minh trạng thái "đã xử lý" |
| 25 | **Trung bình** | **Secret không giải mã được (đổi `APP_KEY`)**: ô rỗng nhưng nút enabled; EP-05 trả 200 `{secret: null}` ⇒ copy chuỗi `"null"` + 「コピーしました」; job cũng không giải mã ⇒ gửi không header. Cách thoát: 「再生成」 | BUG-01, UI-20, R-B3 | `WebhookRelayService.php:86, 103, 359-373, 532-547`; `webhook-relay.js:409-416, 423-430` | Cao (server) / Trung bình (clipboard) | Trả lỗi rõ ràng + gợi ý tái tạo |
| 26 | **Trung bình** | **「再生成」 không khoá**: 2 tab bấm gần nhau ⇒ 2 secret; tab đến trước hiển thị mask của secret đã bị thay; khách có thể copy secret chết | BUG-03 | `WebhookRelayService.php:217-231` | Cao | Transaction + `FOR UPDATE` |
| 27 | **Trung bình** | **Lưu thất bại im lặng**: 5xx / mạng / 401 ⇒ không thông báo, nút chỉ bật lại; `CheckRememberToken` trả 200 với `errors` là chuỗi ⇒ `errors.forEach` TypeError ⇒ có thể kẹt `isSaving` | UI-02, BUG-05 | `webhook-relay.js:313-317, 333-363, 583-593`; `CheckRememberToken.php:31-40` | Cao / Trung bình (BUG-05) | Fallback toast cho mọi lỗi |
| 28 | **Trung bình** (UX) | **「再生成」 không có phản hồi thị giác**: không toast; mask trước/sau giống hệt | UI-03 | `webhook-relay.js:466-478`; `WebhookRelaySetting.php:49, 52` | Cao | Toast + hiển thị thời điểm tái tạo |
| 29 | **Trung bình** | **Menu hiện cho Staff không có quyền**; bấm vào ⇒ xoá bot đang chọn khỏi session. Staff `is_admin = 1` có thể bị chặn tuỳ đường vào bot | UI-18, SEC-08, V-14, M-13 | `sidebar.blade.php:79, 209-245`; `AdminAccess.php:61-72`; `functions.php:5044-5094` | Cao | Lọc menu theo quyền |
| 30 | **Trung bình** (dữ liệu) | **GET có ghi DB**: mở màn tạo dòng + secret, đóng mốc 2 kênh, đổi `updated_at` mỗi lần; 「最終更新」 chỉ là "lần xem gần nhất" chung bot; `updated_at` mất ý nghĩa "lần đổi cấu hình"; không được CSRF che (ảnh hưởng chỉ là đổi mốc). Thời điểm sinh secret lệch QA-spec-003 | UI-19, SEC-06, BUG-09, DBM-05, GAP-08 | `WebhookRelayService.php:83-92, 293-339, 427-494` | Cao | Tách "xem" và "đóng mốc"; BA chốt thời điểm sinh secret |
| 31 | **Thấp – Trung bình** (bảo mật) | **URL đích ghi nguyên văn vào log** (web `logEntry` + audit before/after; job log mọi request). URL Slack / Zapier / Make… thường chứa token; validator chấp nhận `https://user:pass@host/` | SEC-05, R-20 | `WebhookRelayController.php:91-95, 201-209`; `WebhookRelayService.php:186-193`; `WebhookRelayApiClient.java:117-126` | Cao | Che query string / userinfo khi log |
| 32 | **Thấp** (bảo mật) | Plaintext secret **xem lại vô hạn** bởi bất kỳ ai có quyền màn (kể cả Staff) — quyết định D-03 nội bộ, có audit + throttle; chế độ hiện plaintext không reset khi đổi tab, giữ trong bộ nhớ tới khi reload | SEC-07, UI-11 | `WebhookRelayService.php:352-356`; `webhook-relay.js:75, 204-233` | Cao | Cân nhắc quyền riêng cho xem / tái tạo |
| 33 | **Thấp** | **Múi giờ**: `occurred_at`, `created_at`, `next_attempt_at` lần 1 = giờ JVM (không cấu hình TZ); lần sau = `NOW()` DB; web hiển thị nguyên giá trị với app TZ `Asia/Tokyo` | R-18, DBM-06 | `WebhookRelayError.java:61-72`; `WebhookRelayQueue.java:107-108`; `config/app.php:68` | Trung bình | Xác nhận TZ (G-11) |
| 34 | **Thấp** | **Không dọn dữ liệu** `webhook_relay_queue`, `webhook_relay_error` (QA-008); endpoint chết lâu ⇒ mỗi sự kiện kênh 1 sinh 1 dòng queue + 1 dòng lỗi; UI chỉ hiện 100 | R-19, DBM-09 | — | Cao | Job purge (index `idx_webhook_relay_queue_bot` đã chờ sẵn) |
| 35 | **Thấp** | 「使い方を見る」 **không làm gì** khi env rỗng; `env()` gọi trong controller ⇒ `config:cache` luôn rỗng | BUG-02, UI-07 | `WebhookRelayController.php:61`; `webhook-relay.js:595-602` | Cao (code) / Trung bình (env) | Đưa vào `config/`; ẩn nút khi rỗng (như FA-046) |
| 36 | **Thấp** | Tra DNS **đồng bộ, không timeout riêng** trong EP-02 ⇒ DNS chậm làm treo request, có thể kích hoạt cảnh báo Chatwork | BUG-04 | `WebhookUrlValidator.php:124-152` | Cao | Timeout DNS |
| 37 | **Thấp** | **Chuỗi JP tạm chưa chốt**: `URL_TOO_LONG`, `URL_NOT_ALLOWED` (QA-001), 「その他のエラー」 (C-04 nội bộ), câu confirm rời tab; xác nhận dùng `window.confirm` thay `lme-modal` | BUG-06, UI-13 | `WebhookRelayService.php:37-39`; `WebhookRelayError.php:35-49`; `webhook-relay.js:100-104` | Cao | BA chốt wording (G-13) |
| 38 | **Thấp** (UX) | Nhóm hành vi UI nhỏ: lỗi inline không tự xoá (UI-04); badge theo switch chưa lưu (UI-05); không cảnh báo rời trang (UI-06); bảng không có loading, hiện 「転送エラーはありません」 khi đang tải / lỗi (UI-08); cờ `isLoadingErrors` dùng chung 2 kênh (UI-09); sort chỉ trên ≤100 dòng, mũi tên có thể giữ trạng thái cũ khi đổi tab (UI-10); nút icon không tooltip / `aria-label` (UI-12); 「イベント種別」 không dịch (UI-15); `HTTPS://` viết hoa bị từ chối (UI-16); 5 lý do từ chối chung 1 câu, input không `maxlength` (UI-17) | UI-04, 05, 06, 08, 09, 10, 12, 15, 16, 17 | ui-spec "Bất thường" | Cao / Trung bình (UI-08, UI-10) | Sửa theo từng mục |
| 39 | **Thấp** | 3 mã job (`HTTP_ERROR`, `UNKNOWN`, `INVALID_PAYLOAD`) gộp chung 「その他のエラー」; khoá `OTHER` không có writer — chỉ phân biệt được nhờ 「エラーコード」 có/không giá trị | DBM-08, X-04, M-03 | `Constants.java:285-290`; `WebhookRelayError.php:41-62` | Cao | Thêm chuỗi riêng |
| 40 | **Thấp** | Form Request chạy trước kiểm quyền ⇒ người không có quyền gửi payload sai nhận 422 thay vì 403 | SEC-09 | `WebhookRelaySaveRequest.php:24-28` | Cao | — |
| 41 | **Thấp** | Không FK: `queue_id` có thể trỏ dòng đã xoá (đổi LOA xoá `callback_event`); dòng setting của bot đã xoá không bị dọn (job chặn bằng gate); `checkBotHasPermission` không lọc `user_staff_bots.status` (an toàn ở FA-047 nhờ `canAccess`, nhưng helper dùng chung) | DBM-13, DBM-14 | `CallbackEventRepository.java:28`; `functions.php:202-205` | Trung bình / Cao | — |
| 42 | **Thấp** (đã chấp nhận) | Không đảm bảo thứ tự (`unfollow` có thể tới trước `follow` — QA-006); vòng phản hồi khi hệ thống ngoài gọi `/do_action` (D-08 nội bộ) | R-22, R-23 | `HandleForwardCallbackEventManager.java:62-64`; `WebhookLmeEvent.java:17-32` | Cao | Ghi rõ trong tài liệu gửi khách |
| 43 | **Thông tin** | Code chết + tài liệu / comment nguồn lỗi thời (hợp đồng outbound §2, §4.1, §5; comment migration queue/error; entity; plan job; `routes/api.php:440`; `db/index.md`); `menu_id`/`order` khác thiết kế trên DB tương đương dump; kiểu `trigger_type_start` lệch | BUG-08, D-01…D-08, ME-04/07/08/09/11/12, DBM-D09…D14, DBM-10, DBM-11, DBM-12 | §12.2 | Cao | Dev cập nhật comment / tài liệu |
| 44 | **Thông tin** | Đã phân xử: 「タイムアウト（10秒）」 **khớp** code (10s/pha); "15 giây" chỉ ở tài liệu lỗi thời — **không phải lỗi** | UI-14, X-01, M-01, DBM-07 | `Constants.java:239`; `WebhookRelayApiClient.java:63-68` | Cao | Xoá TODO C-05 nội bộ |

### 9.3 Lưu ý cho tester

- ⚠ **Chỉ mở trang là ghi DB** (tạo dòng + secret lần đầu; cập nhật 2 mốc + `updated_at` mỗi lần; 「最新に更新」 cũng ghi). Trên môi trường thật cần user cho phép trước (CLAUDE.md §14). Kỳ vọng 「最終更新」 = giờ mở màn, không phải giờ có lỗi.
- Phải bật flag job (`ENABLE_FORWARD_WEBHOOK_CALLBACK` / `_LME`) thì mới có gửi / có lỗi; flag tắt thì 「転送中」 không có tác dụng. Chờ **≥60 giây** sau khi lưu trước khi bắn sự kiện thử (sự kiện trong 60s đầu bị bỏ qua vĩnh viễn).
- Trước khi bật flag trên môi trường có dữ liệu cũ: xác nhận đã chạy script recover (không thì nhận lại toàn bộ lịch sử).
- Kênh 2: bên nhận phải so **chuỗi** `X-Lme-Signature` với secret (không phải HMAC). Sau 「再生成」, trong ≤60s vẫn nhận secret cũ.
- Lỗi retry (timeout, 5xx) hiện ở 「転送エラー」 sau **~2 phút** (3 lần gửi); lỗi 4xx / không kết nối hiện **ngay** sau 1 lần. Timeout phía LME ⇒ 「エラーコード」 = 「—」 (không phải 408).
- Kênh 2: 1 lô thất bại = **1 dòng** lỗi dù chứa tới 500 sự kiện; 「イベント種別」 là của sự kiện đầu.
- Sau 「再生成」 ô secret trông y hệt và không có toast (UI-03) — xác minh bằng cách bấm mắt.
- Throttle xem secret 10 lần/phút/user, **dùng chung bộ đếm** với reveal của FA-046.
- Kiểm thử Staff: chưa tick quyền ⇒ redirect + mất bot đang chọn; đã tick ⇒ làm được mọi thao tác kể cả 「再生成」.
- Đổi tab khi có thay đổi chưa lưu ⇒ confirm; rời trang bằng sidebar / F5 thì **không** cảnh báo.
- URL `http://`, `HTTPS://`, cổng ≠ 443, IP nội bộ, host không tồn tại đều bị từ chối (4 lý do cuối cùng 1 thông điệp); nhưng `https://[::ffff:127.0.0.1]/` **được lưu** (SEC-03).
- **Không** gọi EP-07 trên môi trường thật nếu chưa được phép (endpoint đang mở, mỗi lần gọi giải mã toàn bộ secret).

---

## 10. Gaps và Unknowns

### 10.1 Gaps

| # | Gap / điểm chưa rõ | Mức ảnh hưởng | Nguồn | Cách xử lý đề xuất |
|---|-------------------|:------------:|------|-------------------|
| G-01 | **Trạng thái production**: commit đang deploy (EP-07 có mở?), giá trị 2 flag + số luồng + `LARAVEL_APP_KEY` của job, env `WEBHOOK_RELAY_DOCS_URL`, command `access-feature:webhook-relay` đã chạy chưa | Cao | logic GAP-05; job G-01; val G-1; ui #2 | Vận hành xác nhận; tìm log khởi động `Config enable: ENABLE_FORWARD_WEBHOOK_*` |
| G-02 | **DDL thực tế**: `callback_event.status_sync` / `webhook_event_id` + index `(status_sync, id)`; `webhook_relay_queue` theo DDL nào (index `delivery_id`, `locked_*`); `status_sync` của 2 bảng history đã chạy online DDL; dòng `access_feature` `webhookRelay*` (`menu_id`, `order`, đủ 5 con) | Cao | logic GAP-01, GAP-06; job G-02; db C-02, C-03, §11.3 | DBA `SHOW CREATE TABLE`; export lại dump + tách bảng (CLAUDE.md §5) rồi `/spec-db webhook-relay` |
| G-03 | Bước recover (đánh `status_sync = 4` dữ liệu cũ) đã / sẽ chạy trước khi bật flag chưa; script gitignored | Cao | logic GAP-02; job G-03; val G-3 | Đếm `status_sync IS NULL` dữ liệu cũ trước khi bật |
| G-04 | Phiên bản OkHttp thực tế (quyết định hành vi redirect của #2, #5, #6) | Trung bình | job G-06; val G-4 | `./gradlew dependencies \| grep okhttp` |
| G-05 | Phiên bản PHP production (SEC-03 kiểm trên PHP 7.2.0 cục bộ) | Thấp | val G-5 | Kiểm phiên bản server |
| G-06 | **Không có runtime / screenshot**; submodule `public/lme-ui` chưa clone (dấu `*`, vị trí lỗi inline, icon sort, toast tự ẩn, tab active); **mở trang là ghi DB** ⇒ quét live cần user cho phép | Trung bình | val G-6; ui "Điểm chưa rõ" #1 | User quyết định; `git submodule update --init` (chỉ đọc) |
| G-07 | Hợp đồng kênh 2 chính thức gửi khách (`tag_id` vs `tag_ids[]`, 7 action friend info, `field_id` âm/dương, `option_id`) | Trung bình | job G-07; val G-7 | Đối chiếu tài liệu 1.0.0 gửi khách |
| G-08 | Đường vào bot nào Staff `is_admin = 1` dùng trong thực tế (quyết định có bị middleware chặn) | Trung bình | ui #6; val G-8 | Kiểm runtime với tài khoản Staff |
| G-09 | **Phạm vi thực tế kênh 2**: mọi đường thay đổi tag / thông tin bạn bè có đều ghi `tag_history` / `friend_info_history`? (`friend_info_history` chỉ ghi khi giá trị đổi — gán lại cùng giá trị có phải sự kiện?) | Trung bình | logic GAP-07; job G-08, G-09 | Rà các chỗ ghi `tags_users` / `friend_information_*` không kèm history; hỏi BA |
| G-10 | Số tiến trình job cùng bật flag (R-11) | Trung bình | job G-04 | Xác nhận vận hành |
| G-11 | Múi giờ JVM so với MySQL, `serverTimezone` JDBC | Thấp | job G-05 | So `occurred_at` với log job |
| G-12 | Session hết hạn: AJAX nhận 401 JSON hay 302 → `/logout` (jQuery parse lỗi)? `lme-table` có giữ trạng thái sort khi đổi `data-source`? | Thấp | ui #7, #8 | Kiểm runtime |
| G-13 | Wording / chuỗi chưa chốt: `URL_TOO_LONG`, `URL_NOT_ALLOWED` (QA-001), 「その他のエラー」, confirm rời tab; thời điểm sinh secret lệch QA-spec-003 | Thấp | ui #3, #4; logic GAP-08 | BA chốt |
| G-14 | **Index source cũ**: `src/web/index/routes.md` sinh từ nhánh cũ, không có route `webhookRelay*` / `webhookCompetitors` (agent sau grep index sẽ không thấy) | Thấp | (compiler phát hiện) | `python3 src/web/index/generate-indexes.py` |
| G-15 | **Mâu thuẫn còn sót giữa tài liệu** (không đổi kết luận): (a) `job-spec.md` §2.1 ghi `tag_history` được Laravel ghi ở "≈43 file", `logic-spec.md` §8.1 đếm lại **12 lời gọi `TagHistory::create` trong 6 file** (cách đếm khác, chưa kiểm hết — V-24); (b) `features/admin/index.md` (và mô tả task) ghi menu "ngay dưới 「接続設定」", code thực tế đặt **sau 「API連携」**; (c) `features/shared/pending-refs.md` gắn 「接続設定」 là FA-036, index ghi FA-036 = 「マイページ」; (d) ký hiệu trùng nhau: `C-04` (TODO chuỗi của dev) vs `C-04` (cảnh báo dump của db-mapping), `D-03`/`D-05`/`D-08` (quyết định nội bộ dev) vs `D-01…D-08` (lệch tài liệu của job-spec) — đọc theo §12.1 | Thấp | V-24; ui #9; FA-046 G-09 | Đồng bộ khi sửa spec con / index lần sau; spec này dùng số liệu của logic-spec và vị trí theo code |
| G-16 | Tài liệu / comment nguồn lỗi thời (hợp đồng outbound, comment migration, entity, plan job, `routes/api.php:440`) — ngoài phạm vi spec | Thấp | val G-9; §12.2 | Đề xuất dev web / job cập nhật |

### 10.2 Câu hỏi chờ user (từ validation-report §9 — user đã cho compile tiếp, chưa có quyết định)

| Mã | Mức | Câu hỏi | Bằng chứng | Đề xuất | Ai quyết | Nếu chưa quyết |
|----|-----|--------|-----------|--------|---------|----------------|
| **V-02** | **Nghiêm trọng** | Kênh 2 giữ **"shared token"** (secret thô trong `X-Lme-Signature`) hay chuyển sang **HMAC**? Sửa wording 「署名を付与…この値を検証すると」 và tài liệu gửi khách theo lựa chọn | Job: `WebhookSignatureHelper.java:22-26, 79-82` (Phương án A, chốt 2026-09-10, `task_40475_spec_job.md:205-207`); UI: `index.blade.php:107`; hợp đồng web: `docs/api/webhook-relay-outbound-contract.md:177-202` (HMAC hex) | **(a)** Giữ Phương án A ⇒ đổi wording UI thành "gửi kèm secret, so sánh chuỗi", cập nhật hợp đồng gửi khách, khuyến nghị bên nhận không log header; **hoặc (b)** quay lại HMAC (helper `toHex()` còn sẵn) + ký cả `X-Lme-Timestamp` để chống replay. Khuyến nghị **(b)** nếu chưa có khách tích hợp | BA / Leader Dev | Khách tích hợp theo tài liệu sẽ verify thất bại 100%; secret tiếp tục đi thô trong mọi request |
| **V-03** | **Nghiêm trọng** | Khoá / xoá endpoint debug `GET /api/webhook-decode/{secret}` (EP-07)? Production có đang chạy commit `3f3c7ddf95` không? | `WebhookRelayDebugController.php:44-51` (guard bị comment); `routes/api.php:440-446`; `Kernel.php:45-48` (nhóm `api` chỉ `bindings`); commit `3f3c7ddf95` (tudv, 2026-09-10) có trong `release_step_20260930_v2`, `release_staging_20260910` | Bỏ comment guard **ngay** (hoặc xoá route + controller vì chỉ phục vụ test tay); sửa comment `routes/api.php:440`; rà access log xem endpoint đã bị gọi chưa | Dev web / Vận hành | Ai có 1 secret đều tra được `bot_id` + ciphertext; DoS bằng request lặp |
| **V-04** | **Nghiêm trọng** | Có **chặn bật `ENABLE_FORWARD_WEBHOOK_*` trên production** tới khi sửa: (1) verify `X-Line-Signature` thật ở `callbackWebHook` (SEC-02); (2) job `followRedirects(false)` + `followSslRedirects(false)` + kiểm IP / cổng lúc gửi (R-01…R-03)? | `BotController.php:2046-2054, 2066-2072`; `WebhookRelayApiClient.java:63-68, 89-138`; đối chứng `RequestHelper.java:35-39`, `NotifyUtils.java:148-152` đều tắt redirect | Chặn bật flag cho tới khi xong (2); (1) nên làm trước khi bật **kênh 1**. Kèm checklist #9, #10 (recover dữ liệu cũ, DDL `status_sync`) | Leader Dev / Bảo mật | Sự kiện giả bị chuyển tiếp như thật; server job có thể bị dùng để gọi vào mạng nội bộ; secret lộ qua redirect |
| **V-11** | Trung bình | Wording 「自動で最大3回まで再送を試みます。3回とも失敗したものだけをここに記録します。」: sửa UI hay đổi hành vi job? | UI: `index.blade.php:169`; job: `Constants.java:221-223` (`MAX_ATTEMPT = 3` tính cả lần đầu), `WebhookRelayResult.java:53-61` (chỉ TIMEOUT / ≥500), `HandleForwardCallbackEventTask.java:115-119` | Sửa wording cho đúng: "tối đa 3 lần gửi (2 lần gửi lại) khi hết thời gian chờ hoặc lỗi máy chủ; các lỗi khác được ghi ngay" — hoặc thêm `CONNECT_FAILED` vào nhóm retry (#16) | BA | Người dùng hiểu sai mức đảm bảo; tester kỳ vọng sai thời điểm lỗi xuất hiện |
| **V-12** | Trung bình | Độ trễ cache 60s: chấp nhận + sửa cam kết QA-spec-017 (「secret cũ hết hiệu lực ngay」), hay bổ sung cơ chế làm mới cache? | `WebhookRelaySettingManager.java:28, 98-118`; `WebhookSignatureHelper.java:54-58, 91-105`; `WebhookRelayService.php:195-197, 213-215` | Ngắn hạn: ghi rõ trên UI / tài liệu "có hiệu lực trong vòng 1 phút". Dài hạn: web ghi cờ / version, job đọc trực tiếp setting của bot khi gate (bỏ IGNORE oan ở lần bật kênh); với secret có thể chấp nhận secret cũ trong cửa sổ ân hạn ở phía khách | BA / Dev job | Mất sự kiện ≤60s đầu khi bật kênh; mất lô khi bên nhận đã đổi secret |
| **V-13** | Trung bình | TIMEOUT: job tự điền `http_status = 408` theo hợp đồng "chốt 2026-09-09", hay sửa hợp đồng + comment migration theo code (`NULL` ⇒ 「—」)? | Hợp đồng `docs/api/webhook-relay-outbound-contract.md:254, 268-274`; migration `create_webhook_relay_error_table.php:31-34`; job `WebhookRelayApiClient.java:128-136` (`fail(null, …)`) | Giữ code (NULL = "không có response" có nghĩa hơn), sửa hợp đồng + comment migration + xoá TODO C-05 | Leader Dev | Tài liệu và dữ liệu thật mâu thuẫn; test viết theo hợp đồng sẽ fail |

---

## 11. Chất lượng Spec

### 11.1 Metrics

| Nhóm | Chỉ số |
|------|-------|
| Màn hình | **4** (SCR-WHR-01…04: 2 tab + 2 dialog native) trên **1** route trang |
| Endpoint | **7** (EP-01…05 AJAX, EP-06 trang, EP-07 debug). UI gọi 6/6 có trong spec; 7/7 có controller / logic |
| Luồng | 10 luồng UI (Luồng 1–10, cùng số với ui-spec) + 3 luồng nền (kênh 1, kênh 2, retry) + 1 sequence tổng thể + 1 flowchart + 3 state machine |
| Field Traceability | **31** hàng UI + **11** hàng ghi ngầm |
| Coverage UI ↔ DB (db-hint → db-mapping) | **57** mục: 52 map + 5 N/A ⇒ **91,2%** thô / **100%** trừ N/A. Tin cậy: **Cao 48 (92,3%)** · Trung bình 4 (7,7%: quyền P-1, P-2; queue S-3; `callback_event` S-4) · Thấp 0. ⚠ Không mục nào đối chiếu sample data |
| Coverage cột 3 bảng chính | 13/39 (33,3%) — đặc trưng kiến trúc (queue + metric thuộc job), không phải thiếu sót |
| Business rules | **50** (BR-01…34 từ logic-spec + BR-35…41 FE/UI + BR-42…50 job): **Cao 48** · hỗn hợp Cao/Trung bình 2 (BR-02, BR-45) · Thấp 0. 100% có `file:line` |
| Bảng DB | **15** (3 primary + 3 nguồn + 9 phụ); 5/6 bảng cốt lõi không có trong dump; `callback_event` thiếu 2 cột job dùng |
| Job | 3 Task Manager + 1 cache manager, 31 luồng mặc định, 2 flag (mặc định tắt), 2 state machine, 10 mã lỗi |
| Thông báo | 19 mục (5 toast, 4 lỗi inline, 7 chuỗi 「エラー内容」, 2 confirm, 1 lỗi trang) |
| Phát hiện bảo mật / bug | **77 mã gốc** (9 SEC + 9 BUG + 23 R + 22 UI + 14 DBM) gộp thành **44 mục** §9.2: **Nghiêm trọng 3 · Cao 8 · Trung bình 19 · Thấp–TB 1 · Thấp 11 · Thông tin 2**. Kèm 8 lệch tài liệu (D-01…D-08) + 18 đối chiếu migration↔entity (ME) |
| Kiểm tra bảo mật đạt | 10/10 hạng mục §9.1 |
| Gaps | **16** (G-01…G-16), trong đó 3 mức Cao (production, DDL, recover) và 1 mục gom mâu thuẫn tài liệu còn sót (G-15) |
| Câu hỏi chờ user | **6** (V-02, V-03, V-04 Nghiêm trọng; V-11, V-12, V-13 Trung bình) |

### 11.2 Kết quả validation

| Hạng mục | Kết quả |
|---------|--------|
| Kết luận | **CẦN SỬA → ĐÃ SỬA PHẦN SPEC** (validation-report 2026-10-24) |
| Vấn đề | 24: **4 Nghiêm trọng / 10 Trung bình / 10 Nhẹ**. **18 đã áp dụng** (V-01 cơ chế `X-Lme-Signature`; V-05…V-10, V-14; V-15…V-24). **6 Chờ user** (§10.2) — user đã cho compile tiếp |
| Mâu thuẫn đã phân xử bằng source | 13 (M-01 timeout 10s; M-02 TIMEOUT → NULL; M-03 `OTHER`; M-04 tên bảng staff; M-05 secret thô; M-06 SSRF; M-07 EP-07 mở; M-08 không verify chữ ký LINE; M-09 kiến trúc web↔job; M-10 cache 60s; M-11 retry 1+2; M-12 giới hạn & throttle; M-13 Staff `is_admin`) — spec này dùng **kết luận đã phân xử** làm chuẩn |
| Phát hiện bảo mật nghiêm trọng | SEC-01, SEC-02/R-05, SEC-03 (mở rộng NAT64, 6to4), R-01, R-02, R-03, R-04, R-06 — **tất cả XÁC NHẬN**, không bị bác bỏ |
| Spot-check của compiler | Đọc lại source ở `4d9d07d159` / `be6ef546`: guard EP-07 bị comment (`WebhookRelayDebugController.php:49-51`) và comment route `routes/api.php:440` vẫn ghi "chỉ sống khi APP_DEBUG=true"; wording `index.blade.php:107, 169`; `BotController.php:2046-2054` (tự tính rồi tự so chữ ký); thứ tự sidebar 「接続設定」→「API連携」→「Webhook転送」 (`sidebar.blade.php:174-209`); `AddAccessFeatureWebhookRelay.php:83, 99` (có `menu_id`); `config/sns-line.php:1283-1289` (web không còn flag); job `WebhookSignatureHelper.buildHeaderValue` trả secret thô, `MAX_ATTEMPT = 3`, `RETRY_DELAY_MINUTES = 1`, `TIMEOUT_SECONDS = 10`, OkHttp không tắt redirect, `RELOAD_INTERVAL_MILLIS = 60000`. **Tất cả khớp**. Phát hiện thêm: màn System Admin 「他社webhook管理」 không có liên kết code với FA-047; index `routes.md` thiếu route (G-14) |

| Spec con | Đánh giá | Ghi chú |
|---------|---------|---------|
| UI spec | **Cao** (nội dung) / Trung bình (hình ảnh) | 4/4 màn, nhãn JP spot-check 0 sai lệch, 10 luồng, 22 bất thường UI; không screenshot (G-06) |
| API spec | **Cao** | 7/7 EP, request / response mẫu, bảng lỗi theo HTTP, middleware đầy đủ |
| Logic spec | **Cao** | 34 BR có `file:line`; cầu nối web → job; 9 SEC + 9 BUG |
| Job spec | **Cao** | Queue / state machine / processing chain / retry / error handling khớp source; 23 rủi ro + 8 lệch tài liệu |
| DB mapping | **Cao** (cấu trúc) / Trung bình (dữ liệu) | Coverage 100% trừ N/A; 5/6 bảng cốt lõi chỉ có migration + entity, không có data (G-02) |
| Cross-reference | **Trung bình – Cao** | 0 SC đã đăng ký; 8 ứng viên (Masked Credential Field đủ điều kiện cùng FA-046); 4 mâu thuẫn tài liệu nhỏ còn sót (G-15) |

---

## 12. Phụ lục

### 12.1 Mã tham chiếu nội bộ trong comment code (chỉ để tra chéo)

| Mã nội bộ (comment dev) | Ý nghĩa | Tương ứng trong spec này |
|------------------------|---------|------------------------|
| `SCR-01` / `SCR-02` | Tab kênh LINE / tab kênh LME | SCR-WHR-01 / SCR-WHR-02 |
| `EP-01` … `EP-05` (web) | `config` / `save` / `regenerate-secret` / `errors` / `secret` | **Trùng** EP-01…EP-05 của dự án; trang = EP-06, debug = EP-07 |
| `BR-02` / `QA-spec-028` | Secret chỉ thuộc kênh LME, kênh LINE không ký | BR-20, BR-44 |
| `BR-03` | Confirm khi tái tạo, đúng nguyên văn | SCR-WHR-03 |
| `BR-05`, `BR-19` | Tối đa 100 lỗi; lỗi tách theo kênh | BR-25 |
| `BR-07` | 「保存する」 luôn hiện ở cả 2 tab | BR-36 |
| `BR-08` | Badge số lỗi trên tab — **đã bỏ** | — |
| `BR-09` / `QA-spec-005` / `D-05` | Staff có thể được cấp quyền màn | BR-02, BR-03 |
| `BR-22` / `QA-spec-030` | Chỉ lưu kênh tab đang mở + cảnh báo rời tab | BR-05, BR-33 |
| `BR-25` / `QA-spec-009` | Không tự tắt kênh khi lỗi | BR-32 |
| `QA-spec-001` | Vị trí menu "ngay dưới 「接続設定」" | §1.3 (thực tế sau 「API連携」) |
| `QA-spec-002` | URL 「使い方を見る」 chưa cấp | BR-36, BUG-02 |
| `QA-spec-003` | Mặc định tắt / thời điểm sinh secret (code đã lệch) | BR-18, G-13 |
| `QA-spec-004` / `D-03` | Secret xem lại được bất cứ lúc nào | BR-22 |
| `QA-spec-012` | Định dạng 「発生日時」, mới → cũ | BR-28 |
| `QA-spec-014` | Lưu xong ở lại màn + toast | BR-36 |
| `QA-spec-015` | Luôn mở tab 1 khi vào / F5 | BR-33 |
| `QA-spec-017` | Secret cũ hết hiệu lực ngay | BR-23, V-12 |
| `QA-spec-026` / `QA-001` / `RR-02` | URL bắt buộc khi bật; ≤1024; chống SSRF, cổng 443; chuỗi lỗi tạm | BR-06…BR-12 |
| `R-003` | Quyền mức màn, không theo action | BR-03 |
| `W-011` | 2 ô URL cùng nhãn, phân biệt bằng tab | §2.4 |
| `C-04` (TODO dev) | 「その他のエラー」 chuỗi tạm | §3.8.5 (khác `C-04` cảnh báo dump trong db-mapping) |
| `C-05` (TODO dev) | "Timeout thật 15 giây" — **dựa trên tài liệu lỗi thời** | §9.2 #44 |
| `QA-003` / `QA-006` / `QA-008` / `QA-011` / `QA-014` / `QA-015` (job) | Nhịp poll; không đảm bảo thứ tự; không dọn dữ liệu; gate bot hết hạn > 7 ngày; field không đưa vào payload; `field_id` âm/dương | §7.3, BR-50, #34, BR-42, BR-45, #22 |
| `D-08` (quyết định job) | Chấp nhận vòng phản hồi `/do_action` | #42 |
| `RR-06` (job) | Phát lại lịch sử | #9 |
| "Phương án A" (job, 2026-09-10) | `X-Lme-Signature` = secret thô | BR-46, V-02 |
| `#40763` | Gỡ enqueue phía web + 3 cờ env | BR-30 |
| `#40888` | Lưu nguyên body + `webhook_event_id` vào `callback_event` | BR-34 |
| `#41030` | 「最終更新」 lưu server, tách theo kênh | BR-29 |
| `#40792` | Reset cuộn bảng khi đổi tab | §2.6 |
| `#40533`, `#40728`, `#40764` | `channel` nghiêm ngặt; DNS fail-closed; guard debug (đã bị comment lại) | BR-26, BR-12, #1 |

### 12.2 Lệch tài liệu / comment nguồn ↔ code (đề xuất dev cập nhật)

| Mã | Vị trí | Nói | Thực tế |
|----|-------|-----|--------|
| D-01 | Migration `webhook_relay_queue` `:26-35, 47-55` | Laravel INSERT; job `WebhookRelayTask` poll; ch.1 `payload` NULL; `status 0..3`; `locked_*` chống trùng | Web không ghi; job tự INSERT khi lỗi lần 1; `payload` luôn có; có `status = 4`; không dùng `locked_*`; không có class `WebhookRelayTask` |
| D-02 | Migration queue `:47` + widen `:25` | `callback_event_id` NULL với ch.2 | Ch.2 = id `tag_history` / `friend_info_history` |
| D-03 | Migration error `:31-34` | TIMEOUT ghi 408 do job tự điền | NULL (V-13) |
| D-04 | Entity `WebhookRelaySetting.java:60` | Job chưa giải mã được secret | Đã giải mã |
| D-05 | Javadoc `WebhookRelayResult.java:6` | "Đã gộp cả các lần retry" | Mỗi result = 1 lần gọi |
| D-06 | Plan job `task_40475_spec_job.md` | Poll 500ms; quét `status IN (2,102)`; N dòng lỗi / lô; `tag_ids[]` | 200/1000ms; `NOT IN (0,1,100,101)`; 1 dòng / lô; `tag_id` đơn |
| D-07 | `Constants.java:195-200` | Hằng số status `CallbackEvent` không còn `final` | Vẫn `final` trên nhánh này |
| D-08 | `WebhookUrlValidator.php:21-22, 121-122` | Job PHẢI kiểm lại lúc gửi | Không kiểm (R-01) |
| DBM-D09 | `fix_queue_id_comment…php:12-14` | `webhook_relay_queue` "không còn dùng" | Đang là retry queue |
| DBM-D10 | `WebhookRelaySetting.java:16` | "Tự tắt kênh do web quyết định" | Web cũng không tự tắt |
| DBM-D11 | Migration error `:10-11`; `WebhookRelayError.java:12` | Chỉ ghi sau 3 lượt | Lỗi không-retry ghi sau 1 lần |
| DBM-D12 | `callback_event.status` comment | `0..3` | ≥ 17 giá trị |
| DBM-D13 | `Constants.java:269` | Mã lỗi "map 1-1 với 6 message" | Web 7 chuỗi, job 9 mã |
| — | `routes/api.php:440` | EP-07 "chỉ sống khi APP_DEBUG=true" | Mở ở mọi môi trường |
| — | `docs/api/webhook-relay-outbound-contract.md` §2, §4.1, §5, `:231, 254, 285-292` | Web INSERT queue; HMAC hex; timeout 15s; TIMEOUT 408; 2 cờ env | Tất cả lỗi thời |
| — | `db/index.md` | Data ở `db/data/tables/`; 308 bảng | Thực tế `db/data/{table}.sql`; 310 file schema (thiếu `user_selected_bot`) |

### 12.3 Lịch sử phiên bản

| Phiên bản | Ngày | Nội dung |
|----------|------|---------|
| v1 | 2026-10-24 | Bản tổng hợp đầu tiên, code-first trên web `release_step_20260930_v2` (`4d9d07d159`) + job `release-t09-2026` (`be6ef546`), sau validation-report (CẦN SỬA → ĐÃ SỬA PHẦN SPEC; 6 mục Chờ user ghi ở §10.2 theo quyết định compile tiếp của user) |
