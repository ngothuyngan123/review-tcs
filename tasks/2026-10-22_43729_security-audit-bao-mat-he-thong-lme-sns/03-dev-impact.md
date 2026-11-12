# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Auto-fill lệch chuẩn**: Redmine description của #43729 KHÔNG có section "Đánh giá ảnh hưởng" theo đúng heading chuẩn (ticket cha chỉ mô tả tổng quan + "xem các subtask"). Toàn bộ nội dung dưới đây được parse từ **Journal #146764** (Dev Studio handoff, 2026-10-22 04:56 — bản đầy đủ nhất, supersede Journal #146708 là bản draft ngắn hơn cùng nội dung nguyên nhân). Leader/Tester **bắt buộc đọc lại Journal nguyên văn ở `01-bug-task.md`** trước khi tick checkbox verify.
>
> Mục 3 (caller đã check) Dev không ghi theo bảng chuẩn — thay vào đó journal cho diffstat file đã sửa + danh sách "Nội dung thay đổi" theo từng hạng mục D-1..D-8 (xem Journal #146708). Bảng dưới đây **suy luận mapping file ↔ hạng mục** từ nội dung journal (thứ tự đoạn văn "Nội dung thay đổi" khớp thứ tự D-1..D-8) — đây là suy luận của AI, không phải Dev ghi trực tiếp từng dòng, Leader nên xác nhận lại nếu nghi ngờ.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Nguyen Ngoc Hai (assigned_to Redmine) — nội dung đánh giá do "Dev Studio" (AI) sinh trên nhánh `ai_studio_fixbug_43729` |
| Commit / Pull Request | `<chưa có PR>` — branch `ai_studio_fixbug_43729`, base `release_step_20260930_v2@d6c0a2653f63`, head commit `6abe854e10c1894bc9693ac737ce9098e999080a` |
| Branch | `ai_studio_fixbug_43729` (base `release_step_20260930_v2`) |
| Ngày submit đánh giá | 2026-10-22 (Journal #146764, 04:56 UTC) |
| Auto-filled | 2026-10-22 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #146764 nguyên văn (file 01) và xác nhận mapping F/D/T dưới đây không sai lệch (đặc biệt mapping file ↔ D-1..D-8 là suy luận, không phải Dev ghi trực tiếp).

---

## 1. Nguyên nhân

Các điểm nhận dữ liệu từ bên ngoài đều không kiểm dữ liệu đầu vào:
- Webhook PHP tự tính chữ ký từ chính body nên luôn hợp lệ (không verify `X-Line-Signature` thật).
- Auto-reply (command xử lý callback tin nhắn) nối nguyên text tin nhắn vào SQL (SQL injection qua nội dung chat).
- Booking sự kiện dùng `quantity` do client gửi mà không validate.
- Callback Telecom chỉ kiểm `rel=yes` vì lời gọi kiểm IP đã bị xoá từ 2018-05-10.
- Server socket (chat realtime) không xác thực và đẩy mọi tin vào room `legacy_client` chung cho mọi bot.

## 2. Cách fix

(= "Nội dung thay đổi" trong Journal #146764, nguyên văn)

- **Webhook LINE** `POST /line/callback/add/{bot_id}`: thiếu hoặc sai header `X-Line-Signature` → 401, không lưu event; bot Olioa (`bot_type=1`) → 403; nút Verify của LINE Console vẫn hoạt động.
- **Auto-reply theo từ khoá** (command xử lý callback tin nhắn): nội dung tin nhắn đi qua binding SQL (parameterized query), cách khớp từ khoá ("chứa" / "khớp chính xác") giữ nguyên.
- **Đặt chỗ sự kiện (LIFF)**: đặt mới, đổi lịch, rollback đổi lịch từ chối `number_order` không phải số nguyên ≥ 1 → HTTP 422 + `「予約数は、１以上入力してください」`.
- **Telecom**: tắt 4 URL — `/make_form_telecom/{id}`, `/customer/telecom_callback_tsudo.php`, `/customer/telecom_callback_keizoku.php`, `/customer/telecom_callback_fail` → 404.
- **node_serve (chat realtime)**: ngắt kết nối không có `botCode`; bỏ room `legacy_client` (nhận tin mọi bot); room typing đổi định dạng `bot_staff_{bot}_{hội thoại}`; kiểm `origin` theo cấu hình; kiểm token (cờ `requireSocketToken` mặc định **tắt**).
- **API mới phát socket token**: `POST /api/mobile/socket/token` cho app (bot phải thuộc user) và `POST /ajax/chat/socket-token` cho web (bot theo session).
- **Client**: màn chat 1:1, chat nhóm, layout mobile web kết nối socket kèm `botCode` + token, tự lấy token mới mỗi 8 phút; bỏ đoạn script socket chết ở 3 header admin.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev không ghi bảng caller chuẩn — đây là diffstat nguyên văn (28 file, +1407/-91) kèm mapping SUY LUẬN sang hạng mục D-x (xem cảnh báo đầu file). -->

| # | Function / File | Thay đổi (+/-) | Lý do (D-x, suy luận từ nội dung thay đổi) |
|---|---|---|---|
| 1 | `app/Console/Commands/HandleCallbackMessage.php` | +14/-? (14 dòng) | D-2 — command xử lý callback tin nhắn / auto-reply, đổi sang SQL binding |
| 2 | `app/Http/Controllers/Admin/BotController.php` | 21 dòng | D-1 — kiểm `X-Line-Signature` + chặn bot Olioa ở webhook |
| 3 | `app/Http/Controllers/Api/Mobile/SocketTokenMobileController.php` (mới) | +73 | D-7 — endpoint phát socket token cho app mobile |
| 4 | `app/Http/Controllers/Basic/MobileEventBookingController.php` | 99 dòng | D-3 — validate `number_order`/quantity khi đặt/đổi lịch/rollback booking sự kiện |
| 5 | `app/Http/Controllers/Basic/SocketTokenController.php` (mới) | +60 | D-7 — endpoint phát socket token cho web (theo session) |
| 6 | `app/Exceptions/Socket/SocketTokenSecretMissingException.php` (mới) | +10 | D-7/D-8 — exception khi thiếu `SOCKET_JWT_SECRET` |
| 7 | `app/Services/Socket/SocketTokenService.php` (mới) | +126 | D-7 — service sinh/verify socket token (JWT) |
| 8 | `config/sns-line.php` | 3 dòng | D-7/D-8 — config hỗ trợ socket token |
| 9 | `node_serve/config.example.js` | 7 dòng | D-5 — mẫu config `socketJwtSecret`/`allowedOrigins`/`requireSocketToken` |
| 10 | `node_serve/server.js` | 161 dòng | D-5 + D-8 — hotfix socket (bỏ room legacy, khoá typing, giới hạn origin) + kiểm token |
| 11 | `public/js/chats/chat-v2.js` | 11 dòng | D-6 — client chat gửi `botCode` + token |
| 12 | `public/js/chats/socket-auth.js` (mới) | +122 | D-6/D-8 — JS client tự lấy token mới mỗi 8 phút |
| 13 | `public/js/mobile/chat.js` | 3 dòng | D-6 — mobile web client gửi `botCode` + token |
| 14 | `resources/views/basic/chat/index.blade.php` | 1 dòng | D-6 — include script socket-auth ở chat 1:1 |
| 15 | `resources/views/chats/chat_group.blade.php` | 3 dòng | D-6 — chat nhóm |
| 16 | `resources/views/chats/socket_auth.blade.php` (mới) | +8 | D-6 — partial view socket-auth |
| 17 | `resources/views/layout/admin/header.blade.php` | -6 | D-6 — bỏ script socket chết |
| 18 | `resources/views/layout/admin_v2/header.blade.php` | -6 | D-6 — bỏ script socket chết |
| 19 | `resources/views/layout/v2/admin/header.blade.php` | -6 | D-6 — bỏ script socket chết |
| 20 | `resources/views/mobile/layout/index.blade.php` | 8 dòng | D-6 — mobile web layout gửi botCode + token |
| 21 | `routes/api.php` | 3 dòng | D-7 — route API mới `socket/token` |
| 22 | `routes/web.php` | 9 dòng | D-4 (gỡ 4 route Telecom) + D-7 (route web `socket-token`) |
| 23-27 | `tests/Feature/{AutoReplyKeywordBindingTest, EventBookingQuantityValidationTest, LineWebhookSignatureTest, SocketTokenTest, TelecomRoutesRemovedTest}.php` (mới) | +77/+165/+160/+167/+37 | Test coverage cho D-1..D-5 (Dev tự viết, chạy pass trên base — chưa chạy LINE/MySQL/app thật) |
| 28 | `tests/Support/RecordingConnection.php` (mới) | +132 | Support cho test SQL binding (D-2) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Webhook LINE nhận callback (`POST /line/callback/add/{bot_id}`) | `BotController.php` | Direct | Mọi bot; relay/proxy đổi body hoặc bỏ header → 401 nhầm (Dev tự cảnh báo theo dõi log sau deploy) |
| F2 | Auto-reply theo từ khoá (command xử lý callback tin nhắn) | `HandleCallbackMessage.php` | Direct | Chạy cho mọi bot — đổi cách build SQL, giữ nguyên logic match 'chứa'/'khớp chính xác' |
| F3 | Đặt chỗ sự kiện (đặt mới / đổi lịch / rollback) + thanh toán sự kiện | `MobileEventBookingController.php` | Direct | Dùng chung hàm `payment()` với thanh toán Stripe/Univapay sự kiện |
| F4 | 4 route Telecom (callback thanh toán cũ) | `routes/web.php`, `Customers.php` (không sửa) | Direct | Gỡ hoàn toàn (404) — Dev note: prod không còn LP nào bật cấu hình Telecom |
| F5 | Socket server (chat realtime) — xác thực kết nối, room, origin | `node_serve/server.js` | Direct | Chạm toàn bộ chat 1:1, chat nhóm, mobile web, app native |
| F6 | Phát + verify socket token (JWT ngắn hạn) | `SocketTokenService.php`, `SocketToken(Mobile)Controller.php` | Direct (mới) | 2 endpoint mới: app mobile (bot phải thuộc user) và web (bot theo session) |
| F7 | Client chat tự gửi/refresh socket token | `chat-v2.js`, `socket-auth.js`, `mobile/chat.js`, các `*.blade.php` | Direct | App bản cũ (< 2024-05-16, không gửi `botCode`) mất realtime ngay khi deploy bước 1 |
| F8 | 3 layout header admin — bỏ script socket chết | `layout/{admin,admin_v2,v2/admin}/header.blade.php` | Indirect | Không còn biến `socket` ở các trang dùng layout này — rà regression nếu trang khác còn phụ thuộc |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `callback_event` (hoặc bảng lưu webhook event tương đương) | Chặn CREATE | Chữ ký sai/thiếu → không lưu event mới (trước đây luôn lưu vì tự tính chữ ký) |
| D2 | Không đổi schema | — | Chỉ đổi cách build query (string concat → parameter binding) |
| D3 | Bảng slot/counter của sự kiện (số chỗ còn lại) + `number_order`/quantity của booking | UPDATE được validate | Chặn `number_order` không phải số nguyên ≥1 trước khi trừ/hoàn counter |
| D4 | Không có data DB | — | Chỉ gỡ route, không chạm DB |
| D5 | Room socket (runtime, không persist DB) | Runtime only | Bỏ room `legacy_client`; room typing đổi key |
| D6 | **Config** — `SOCKET_JWT_SECRET` (.env web, cần thêm trước deploy) + `node_serve/config.js` (`socketJwtSecret`, `allowedOrigins`, `requireSocketToken`) | CREATE (config) | Migration thủ công — xem mục "Migration / thay đổi dữ liệu" ở Journal #146764 (file 01) |
| D7 | `socket_token` (JWT, không lưu DB — phát theo request, hết hạn `expires_in=600`) | Runtime only | Phát qua 2 API mới F6 |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Nhận webhook LINE (message / follow / postback / Verify) — mọi bot | F1, D1 | High — Dev tự đánh giá "Rủi ro trung bình" tổng thể nhưng đây là điểm chặn cứng (401), sai sẽ mất toàn bộ webhook |
| T2 | Auto-reply theo từ khoá | F2 | Medium — hồi quy match 'chứa'/'khớp chính xác', JP, emoji |
| T3 | Đặt chỗ sự kiện (đặt mới/đổi lịch/rollback) + thanh toán Stripe/Univapay sự kiện | F3, D3 | High — chạm cả validate input và counter/thanh toán tiền thật |
| T4 | Trang LP có cấu hình Telecom (nút thanh toán cũ) | F4 | Low — Dev note prod không còn LP nào bật, nhưng bấm vào sẽ lỗi do route tắt |
| T5 | Chat realtime — 1:1 web, chat nhóm, chat mobile web (`chat_11`), app native | F5, F6, F7 | High — ảnh hưởng toàn bộ chat, 2 bước deploy (bước 1: botCode bắt buộc; bước 2: token bắt buộc, cần đồng bộ app #43809) |
| T6 | App mobile bản cũ (< 2024-05-16, không gửi botCode) | F7 | Medium/High — mất realtime ngay ở bước 1, Dev đã lường trước |
| T7 | Trang admin dùng layout header (`admin`, `admin_v2`, `v2/admin`) | F8 | Low — chỉ mất biến `socket` chết, cần rà xem có trang nào còn phụ thuộc |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (mapping file↔D-x ở đây là **suy luận AI** — hỏi Dev nếu nghi ngờ sót, đặc biệt route Telecom không sửa `Customers.php` dù Dev note "dọn code còn sót" ngoài phạm vi task)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — lưu ý `KEY_CERTIFICATION_API` bị ghi log là vấn đề Dev nêu **ngoài phạm vi task này**, không nằm trong D1-D7
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] Đã đọc "Việc cần người làm thêm (ngoài phạm vi task)" ở Journal #146764 (file 01) — các mục IDOR `rollbackChangeBookingConfirmFail` và `plan_price` lấy từ client **KHÔNG được fix ở ticket này**, cần ticket riêng
