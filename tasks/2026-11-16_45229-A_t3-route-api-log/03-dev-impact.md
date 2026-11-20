# 03 — Đánh giá ảnh hưởng từ Dev

> **Lượt A — T3 (#45153 · #45161 · #45166 · #43708).** Dev không viết đánh giá ảnh hưởng riêng cho T3; nội dung dưới đây **ghép nguyên ý** từ 3 nguồn Dev đã bàn giao, không thêm suy luận:
> (1) journal ticket cha #45229 — handoff 06/11 (#152500) và các vòng 2→31 (dòng "Route/log/secret (T3)", "Ảnh hưởng", "Migration", "Lưu ý khi deploy");
> (2) Studio task #560 — `requirements` `REQ-T3-ROUTES` + `-01`→`-11` (Dev Studio viết);
> (3) Studio `spec_delta.diffStat` — 35 file thuộc T3 trong tổng 743 file của nhánh.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI implement) — task con Redmine #45233 `[PHP Web] T3` |
| Commit / Pull Request | Không có PR. Merge vào nhánh sprint qua `ai_studio_implement_45233` (các merge `4945ca48d68f`, `a7dbd969d531`, `a6a93579ce9f`, `204db8611d79`); bug Studio sửa thêm: `8626579150a9`, `3a83923444ea`, `b9d796ea56e2`, `38b7e71e8dc6`, `735c81a1bc84`, `b48bfabf7e94`, `cb0a6a81484a`, `a167c4a39551`, `76fd0f322022`, `9f4a54c5688d` |
| Branch | `ai_studio_implement_45229` (sns-line, gốc `release_staging_20261104`@`8877b06f2c11`) |
| Ngày submit đánh giá | 2026-11-06 (handoff) · cập nhật tới vòng 31 (2026-11-08) |
| Auto-filled | 2026-11-16 by `/review-tc` lượt A (ghép từ journal + Studio, không phải `/new-task`) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — đối chiếu mục 4 với journal #45229 + Studio `REQ-T3-ROUTES-*`.

---

## 1. Nguyên nhân

Theo 4 ticket (xem file 01): route quản trị / debug / log-viewer nằm trong khối public không middleware; nhóm route chỉ có `check_login` thiếu kiểm role; API nội bộ so key bằng `==` / `!=` (type juggling); `/api/notify/push-notify` không auth; log ghi password / OTP / session ID / token / key / chữ ký đúng; secret bên thứ ba viết cứng trong code.

## 2. Cách fix

Nguyên văn handoff 06/11: *"Route/log/secret (T3): khoảng 56 route public chuyển vào nhóm cần đăng nhập, xoá route debug/test và log-viewer; secret chuyển sang env; log không còn token/mật khẩu; staff bị thu hồi quyền bot bị chặn."*

Chi tiết theo Studio `REQ-T3-ROUTES` (Dev Studio viết):
- ~56 route public chuyển vào nhóm cần đăng nhập + `check_bot_member`; route public cần thiết vẫn public.
- Xoá route debug / test / command / log-viewer; `/admin/make_encode` chỉ còn `new_lp` / `getPaymentForm` với id số.
- API nội bộ kiểm `KEY_CERTIFICATION_API` an toàn: `hash_equals`, chỉ chuỗi khác rỗng; key rỗng ở server ⇒ từ chối + Chatwork; **giữ hợp đồng lỗi cũ**.
- `/api/upload_image_common` bắt buộc key theo cờ `UPLOAD_IMAGE_REQUIRE_KEY` + kiểm path / ext / ảnh thật.
- Log không ghi token / mật khẩu / secret (`SensitiveLogData` lọc body ở log request chậm; bỏ log key / channel token / reply token / token Google; đổi mật khẩu không ghi mật khẩu).
- `public/.htaccess` chặn thư mục rác `/root/`, `/Users/`, `/https:`.
- Secret chuyển sang env, không còn giá trị mặc định viết cứng; thiếu key ⇒ báo lỗi rõ, không 500, không dùng giá trị cũ.
- Xoá route trùng / chết không làm hỏng màn đang dùng.
- `/api/notify/push-notify` (#45407, PM 08/11): **đóng mặc định** — chỉ nhận IP trong `PUSH_NOTIFY_ALLOWED_IPS` hoặc khoá nội bộ; rỗng / không khớp, token thiếu / sai ⇒ 403, không tạo thông báo.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Middleware `check_bot_member` (`app/Http/Middleware/CheckBotMember.php` +53) | Áp trên nhóm ajax và nhóm sau đăng nhập | Journal: *"mọi request quản trị thêm một lần kiểm quyền bot — staff, System Admin, đổi bot"* |
| 2 | Màn quản trị dùng route đã chuyển nhóm | Không đổi code màn | `REQ-T3-ROUTES-03`: マイページ, bộ lọc, sales / đơn hàng, popup quảng cáo, đổi email bằng mã, mã xoá tài khoản, QR landing / URL; staff hợp lệ không bị chặn |
| 3 | Route public cần thiết | Giữ public | `REQ-T3-ROUTES-04`: LIFF, webhook LINE, form public, đăng ký affiliate, huỷ đơn LIFF, thanh toán booking |
| 4 | Job Java `LineModel.pushNotifyWeb` → `/api/notify/push-notify` | Không đổi job | Journal: job **không gửi khoá** ⇒ phụ thuộc `PUSH_NOTIFY_ALLOWED_IPS`; IP lấy theo TrustProxies |
| 5 | Job Java gọi API nội bộ (`KEY_CERTIFICATION_API`) | Không đổi job | Journal deploy: `KEY_CERTIFICATION_API` của web phải **trùng** key job đang gửi |
| 6 | Server ảnh gọi `/api/upload_image_common` | Không đổi server ảnh trong sprint | Journal deploy: bật `UPLOAD_IMAGE_REQUIRE_KEY=true` **sau khi** server ảnh lên bản mới |
| 7 | Composer: gỡ `laravel-log-viewer` | Thêm `symfony/html-sanitizer` | Journal: manifest `bootstrap/cache` cũ làm app không boot nếu không `package:discover` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | ~56 route `/ajax/*` quản trị chuyển vào `check_login` + `check_bot_member` | `routes/web.php` | Direct | AC-H10 · `REQ-T3-ROUTES-01` |
| F2 | Route quản trị lẻ + nhóm `/basic` thêm `check_login` (hide-popup-ads, push, mark-read, PayPal, scenario store/save, Stripe connect, download-img-info, b2 upload-url; /basic landing / backup / restore / url detail-click) | `routes/web.php` | Direct | `REQ-T3-ROUTES-02` |
| F3 | Middleware `check_bot_member` (staff · System Admin · đổi bot) | `CheckBotMember.php`, `Http/Kernel.php` | Direct | Journal handoff |
| F4 | Chặn staff bị thu hồi quyền | `BasicAccess.php` | Direct | AC-H7 · handoff |
| F5 | Xoá route debug / test / `/command` / component / log-viewer; `make_encode` chỉ 2 route | `routes/web.php` | Direct | AC-C3 · AC-L1 · #43708 · `REQ-T3-ROUTES-05` |
| F6 | Helper kiểm key API nội bộ (`hash_equals`, fail-closed + Chatwork) — áp cho callback/postback, socket-chat-event, download-media, setting-action-friend-info-date, remind, scenario, backup, delete-booking-event | `InternalApiKey.php` + 6 `Api/*Controller` | Direct | AC-C7 · `REQ-T3-ROUTES-06` |
| F7 | `/api/notify/push-notify` — allowlist IP hoặc khoá nội bộ, đóng mặc định | `NotifySettingController.php` | Direct | AC-H11 · #45407 |
| F8 | `/api/upload_image_common` — key theo cờ + path2 allow-list + ext + ảnh thật | `UploadImageCommonGuard.php` | Direct | `REQ-T3-ROUTES-07` |
| F9 | `/ajax/check-file-exist` đưa vào auth | `routes/web.php` | Direct | AC-L2 |
| F10 | Lọc dữ liệu nhạy cảm khỏi log (password, OTP, session ID, token, key, header Cookie) | `SensitiveLogData.php`, `AuthController`, `TwoFactorVerifyController`, `LoginMobileController`, `BasicAccess`, `ActiveAccount`, Remind/Scenario API | Direct | AUTH-H7 · AC-L2 · #45457 · `REQ-T3-ROUTES-08` |
| F11 | Không log chữ ký đúng / body khi chữ ký job sai | `ApiJobSignatureService.php` | Direct | AUTH-N6 |
| F12 | Secret chuyển sang env, bỏ default (Twilio, LINE Login client_secret, OpenAI, EMAIL_API_TOKEN) | `config/sns-line.php`, `Admin/UserController.php`, `config/open_ai.php`, `Mail/ActiveAccount.php`, `Mail/MailApiService.php`, `config/services.php` | Direct | AUTH-H6 · `REQ-T3-ROUTES-10` |
| F13 | Bật lại CSRF cho khối route quản trị | `VerifyCsrfToken.php` | Direct | AC-H10 "bật lại CSRF" |
| F14 | `public/.htaccess` chặn thư mục rác | `public/.htaccess` | Direct | `REQ-T3-ROUTES-09` |
| F15 | Xoá route trùng / chết (#491, `/basic/restore` #45371) | `routes/web.php`, `routes/api.php` | Direct | `REQ-T3-ROUTES-11` |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `.env` mới / bắt buộc: `KEY_CERTIFICATION_API` (trùng job), `PUSH_NOTIFY_ALLOWED_IPS`, `UPLOAD_IMAGE_REQUIRE_KEY`, `LINE_LOGIN_CLIENT_ID` / `LINE_LOGIN_CLIENT_SECRET`, `EMAIL_API_TOKEN` | CONFIG | Thứ tự deploy ở journal vòng 31 |
| D2 | Nội dung `storage/logs/laravel*.log` | UPDATE (format log) | Không còn giá trị nhạy cảm |
| D3 | Composer: bỏ `rap2hpoutre/laravel-log-viewer`, thêm `symfony/html-sanitizer`; `bootstrap/cache/packages.php` | MIGRATE (package) | Phải `package:discover` khi `--no-scripts` |
| D4 | `notification_pc` (bản ghi thông báo PC do push-notify tạo) | CREATE | Chỉ tạo khi caller hợp lệ |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn quản trị dùng route đã chuyển nhóm: マイページ, bộ lọc 友だちリスト / 一斉配信 / CSV管理, sales 商品一覧 / 注文編集 / 注文履歴詳細, 管理画面トップ (popup, header, thông báo), アカウント設定 (đổi email, xoá tài khoản), QRコードアクション / URL分析, データコピー, PayPal / Stripe connect, đăng ký push PC | F1, F2, F13, F15 | High |
| T2 | Trang / endpoint public phía LINE user: LIFF, webhook LINE, form public, đăng ký affiliate, huỷ đơn định kỳ LIFF, đặt chỗ / thanh toán booking | F1, F2 | High |
| T3 | Phân quyền: staff hợp lệ, staff bị thu hồi, System Admin, đổi bot | F3, F4 | High |
| T4 | Job Java gọi web: tin / postback LINE (callback/postback), chat realtime (socket-chat-event), tải media, action theo ngày 友だち情報, remind, scenario, backup, thông báo PC (アクション 「通知」) | F6, F7, D1 | High |
| T5 | Server ảnh upload qua `/api/upload_image_common` | F8, D1 | Medium |
| T6 | Chức năng dùng secret vừa chuyển env: LINE Login, Twilio, OpenAI, mail API (đăng ký / kích hoạt) | F12, D1 | High |
| T7 | Vận hành: log không lộ secret, `/error/logs` không còn | F5, F10, F11, D2, D3 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **chưa có danh sách ~56 route đã chuyển nhóm và 5 dòng xoá ở `routes/api.php`**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
