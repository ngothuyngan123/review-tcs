# 01 — Bug Task từ khách hàng

> **Lượt A của sprint #45229** — nhóm **T3. Route public, debug, API nội bộ, log và secret** (task con Redmine #45233). Folder cha: [tasks/2026-11-16_45229_sprint-fix-bug-bao-mat-hieu-nang-php-web/](../2026-11-16_45229_sprint-fix-bug-bao-mat-hieu-nang-php-web/). Nội dung lấy từ Redmine (`scripts/redmine_fetch.py`) ngày 2026-11-16.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45229 (lượt A) — T3: #45153 · #45161 · #45166 · #43708` |
| Module / Màn hình | Hạ tầng route + middleware (`routes/web.php`, `routes/api.php`, `check_login` / `check_bot_member` / `basic_access`), API nội bộ do job Java gọi (`KEY_CERTIFICATION_API`), `/api/notify/push-notify` (FA-006 通知設定), `/api/upload_image_common` (server ảnh), log ứng dụng `laravel.log`, secret trong config. Studio: task **#560** (task cha) — T3 không có task con trên Studio. |

## Mô tả bug (bản dịch tiếng Việt)

3 ticket #45153 / #45161 / #45166 đến từ **báo cáo quét bảo mật tĩnh sns-line ngày 2026-11-03** trên nhánh cũ `release_step_20260930_v2` — số dòng code ghi trong ticket là của nhánh cũ, phải tìm lại theo tên hàm/route. Ticket gốc ghi: *"Không ghi cách khai thác trong ticket; chi tiết khai thác xem báo cáo gốc nội bộ."*

### #45153 — [Security] T04 · Route public / debug / thiếu middleware (5 lỗi: 1 Critical, 3 High, 1 Low) — Priority Immediate

- **Ticket liên quan:** #42431, #40468.
- **Hướng sửa chung:** rà toàn bộ khối route public: chuyển route quản trị vào `check_login` + `basic_access`, chỉ để lại route thật sự public (LIFF, webhook, landing); xoá `/command`, route test/debug; bật lại gate `app.debug`.

| Mã | Mức | Vị trí (nhánh cũ) | Mô tả | Cách sửa |
|---|---|---|---|---|
| AC-C3 | Critical | `RunTestCommandController.php:71`, `dd($e)` ở `:83`; route `GET /command`, `GET /command/help` (web.php:4259-4262), không middleware | Các điều kiện chặn nối bằng `&&` nên chỉ cần `type` khác rỗng là qua. Các `type` gồm `auto_payment`, `delete_landing`, `delete_richmenu`… Khi chưa đăng nhập, `dd($e)` in ra stack trace | Xoá route; nếu cần giữ thì đặt sau `supper_admin`, đổi logic sang `\|\|`, bỏ `dd` |
| AC-H10 | High | `ajax/scenario/create-folder` (4063), `/ajax/init-data-list-bot` (4153 → `UserController@initDataListBot`, update `Bots::find($id)` bất kỳ), `bill-item-*`, `csv-management/save-filter`, `friendlist/my_page/*` | ~40 route AJAX quản trị nằm trong khối public, miễn CSRF | Chuyển cả khối vào `check_login` + `basic_access`; **bật lại CSRF**. Trùng một phần: 3 route lọc friend public đã ở #42431; các route còn lại chưa có ticket |
| AC-H11 | High | `routes/api.php:423` → `NotifySettingController@pushNotification` | `/api/notify/push-notify` không có auth: tạo thông báo PC cho userId/botId bất kỳ (dùng được để phishing) | #40468 (Java) bỏ việc gọi API này; khi xong có thể xoá luôn route |
| AC-H7 | High | `web.php:1974-2357` và `2582-3752` | Nhóm route chỉ có `check_login`, không áp `BasicAccess` (nơi enforce route theo role) → staff bị giới hạn hoặc đã bị thu hồi quyền vẫn gọi được, miễn `current_bot_id` còn trong session | Áp `basic_access`, hoặc một middleware kiểm tra bot membership nhẹ hơn |
| AC-L1 | Low | `updateTable` (web.php:3863, chạy `Schema::table` ALTER), `/test-curl` (3835), `/haitest/...` (3821), `/admin/make_encode` (258, open redirect), `/sendmail`, `/component`, `/layout-basic` … | Route test / debug public | (gộp theo hướng sửa chung) |

### #45161 — [Security] T12 · API nội bộ (KEY_CERTIFICATION_API) (2 lỗi: 1 Critical, 1 Low) — Priority Immediate

- **Ticket liên quan:** #44046, #43729.
- **Hướng sửa chung:** helper chung `is_string` + `hash_equals` cho mọi API dùng key; không log key; đưa `check-file-exist` vào auth.

| Mã | Mức | Vị trí (nhánh cũ) | Mô tả | Cách sửa |
|---|---|---|---|---|
| AC-C7 | Critical | `Api/CallbackPostbackApiController.php:79` (`==`), `Api/ChatEventApiController.php:17`, `Api/MediaApiController.php:20`, `Api/SettingActionDateApiController.php:17` (`!=`); route `/api/callback/postback`, `/api/socket-chat-event`, `/api/download-media`, `/api/setting-action-friend-info-date` (public) | Bypass `KEY_CERTIFICATION_API` bằng JSON boolean (type juggling): `{"token": true}` bằng (`==`) với mọi chuỗi không rỗng → replay callback gửi tin LINE từ bot tenant, inject chat event qua socket, đặt lịch step cho friend bất kỳ | `is_string($token) && hash_equals((string) config(...), $token)` |
| AC-L2 | Low | `/ajax/check-file-exist` (web.php:4249, public); `Api/RemindApiController.php:53`, `Api/ScenarioApiController.php:27` | Oracle kiểm tra file tồn tại; log nguyên `KEY_CERTIFICATION_API` khi xác thực thất bại | check-file-exist được #44046 đề xuất ticket riêng; log key được #43729 nêu ở khuyến nghị — cả hai chưa có ticket |

### #45166 — [Security] T17 · Log & secret (3 lỗi: 1 High, 2 Medium) — Priority High

- **Ticket liên quan:** #43725, #39108, #39152.
- **Hướng sửa chung:** rotate + chuyển secret sang `.env`, bỏ default trong `env()`; helper log lọc password/code/token/session ID; không log expected signature.

| Mã | Mức | Vị trí (nhánh cũ) | Mô tả | Cách sửa |
|---|---|---|---|---|
| AUTH-H6 | High | `config/sns-line.php:393-394` (Twilio sid/token) · `Admin/UserController.php:2890` (LINE Login client_secret; `:2876` comment) · `config/open_ai.php:3` (default `sk-…`) · `app/Mail/ActiveAccount.php:566`, `app/Mail/MailApiService.php:143` (default `EMAIL_API_TOKEN`) · `routes/web.php:4230` (comment Stripe test key) · `public/js/template_v2/messages/location.js:26` (Google Maps key — key public, cần kiểm đã giới hạn referrer chưa) | Credential bên thứ ba hard-code trong repo | Rotate toàn bộ, chuyển sang `.env`, bỏ giá trị default trong `env()`. #43725 xử lý file credential JSON; Twilio + LINE Login client_secret chưa có ticket |
| AUTH-H7 | Medium (cũ High) | `AuthController.php:880, 1143, 1439` (`Log::debug($request->all())` chứa `password_regist`); `TwoFactorVerifyController.php:231-232`, `UserService.php:91-92` (code); `app/Mail/ActiveAccount.php:399, 434`; `BasicAccess.php:88/134/170` (`session()->getId()`); slow-log `'data'=>$request->all()` ở BasicAccess, CheckLogin, MobileAuthenticate; `UserController.php:5145` (LINE access_token); `LoginMobileController.php:103` | Password, OTP, session ID, token bị ghi vào log | Lọc password/code/token trước khi log; không log session ID. #39108/#39152 là log token khác (Firebase, channel token) |
| AUTH-N6 | Medium | `app/Services/ApiJobSignatureService.php:28-38` (log signature/nonce/body), `:95`, `:103` (`'expected'` khi chữ ký sai) | Khi chữ ký sai, server log ra chữ ký đúng của request đó, còn nonce chỉ được lưu khi thành công → ai đọc được log có thể giả mạo request job cho user bất kỳ trong khoảng tolerance | Không bao giờ log expected signature hay body |

### #43708 — Trang xem log `/error/logs` mở công khai – xem, tải, xóa file bất kỳ — Priority Normal

- **Loại:** lộ thông tin bí mật. **Mức tin cậy:** Confirmed.
- **Tác động:** xem toàn bộ `laravel.log` (token, PII, request thanh toán). Tham số `?dl=` / `?del=` của gói log-viewer nhận đường dẫn tuyệt đối → tải `.env`, xóa file / xóa dấu vết.
- **Vị trí code:** `routes/web.php:81` (middleware `https_protocol` rỗng).
- **Cách sửa:** gỡ route hoặc đặt sau `supper_admin` + chặn IP; nâng cấp gói.

## Steps to reproduce

<!-- Ticket bảo mật không ghi bước khai thác. Bước kiểm chứng tương đương (đối chiếu requirement Studio REQ-T3-ROUTES-*): -->

1. **AC-C3 / AC-L1 / #43708**: chưa đăng nhập, mở thẳng `/command?type=…`, `/updateTable`, `/test-curl`, `/sendmail`, `/component`, `/admin/make_encode?…`, `/error/logs` (kèm `?dl=` / `?del=`).
2. **AC-H10**: chưa đăng nhập, gửi POST tới route `/ajax/*` quản trị (vd `/ajax/init-data-list-bot`, `/ajax/scenario/create-folder`, `/ajax/csv-management/save-filter`).
3. **AC-H11**: từ ngoài gửi POST `/api/notify/push-notify` với `botId` / `userId` bất kỳ.
4. **AC-H7**: staff đã bị chủ thu hồi quyền bot, dùng lại phiên cũ gọi route trong nhóm chỉ có `check_login`.
5. **AC-C7**: gửi JSON `{"token": true}` (hoặc `_token`) tới 1 trong 4 API nội bộ.
6. **AC-L2 / AUTH-H7 / AUTH-N6**: đăng ký / đăng nhập / 2FA / đổi mật khẩu / gửi request job ký sai → tìm giá trị nhạy cảm trong `storage/logs/laravel*.log`.
7. **AUTH-H6**: tìm key bên thứ ba viết cứng trong repo.

## Expected result

- Route debug / test / `/command` / log-viewer: **404**; `/admin/make_encode` chỉ còn 2 màn LP với id số.
- Route quản trị: khách nhận **401 JSON** 「ログインが必要です。再度ログインしてください。」 (ajax) hoặc **302** về đăng nhập; không đọc / ghi dữ liệu. Route public cần thiết (LIFF, webhook LINE, form public, đăng ký affiliate, huỷ đơn LIFF, thanh toán booking) **vẫn public**.
- Staff bị thu hồi quyền: bị chặn ngay; staff hợp lệ không bị chặn.
- API nội bộ: chỉ nhận chuỗi key khớp tuyệt đối (`hash_equals`), server chưa cấu hình key → từ chối hết + Chatwork; giữ hợp đồng lỗi cũ.
- `/api/notify/push-notify`: chỉ nhận IP trong `PUSH_NOTIFY_ALLOWED_IPS` hoặc khoá nội bộ hợp lệ (đóng mặc định, PM chốt 08/11).
- Log không chứa password / OTP / session ID / token / key / chữ ký đúng.
- Secret đọc từ `.env`, không còn giá trị mặc định viết cứng.

## Actual result

- Như mô tả từng mã lỗi ở trên (trên nhánh cũ `release_step_20260930_v2`).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- 4 ticket gốc không có attachment. -->

## Ghi chú thêm của Leader

- ⚠️ Số dòng code trong 3 ticket #4515x là của nhánh cũ — Dev đã tìm lại theo tên route/hàm trên `release_staging_20261104`.
- Quyết định đã chốt trong sprint (journal #45229): **push-notify đóng mặc định** (PM 08/11, #45407) — allowlist rỗng / không khớp và token thiếu / sai ⇒ 403. Job Java (`LineModel.pushNotifyWeb`) **không gửi khoá** ⇒ phụ thuộc hoàn toàn vào `PUSH_NOTIFY_ALLOWED_IPS`; IP lấy theo TrustProxies (`$request->ip()`), sai cấu hình proxy cũng làm job bị 403.
- Rotate secret thật + dọn log cũ chứa token là **ticket riêng ngoài sprint** (journal vòng 31: "Việc cần người làm thêm").
- Bug Studio phát sinh trong lúc test T3 (đã sửa theo journal): #45370 (đăng ký affiliater công khai bị chặn) · #45371 (route chết `/basic/restore` 500) · #45390 (đăng ký không báo lỗi khi thiếu `EMAIL_API_TOKEN`) · #45405 · #45406 (đổi thứ tự bot không thuộc quyền) · #45407 (push-notify) · #45427 · #45428 (thông báo hết phiên) · #45457 (log ghi header Cookie). Còn mở: **#45985** (LINE Login callback 500 — `ArgumentCountError`, có sẵn ở base, status `New`).
- Môi trường đã chạy trên Studio: **100% `local`**.

## Journal / note từ Redmine (nguyên văn)

<!-- 4 ticket con không có journal có notes. Ghi chú Dev liên quan T3 nằm ở journal của ticket cha #45229 — trích ở 03-dev-impact.md. -->
