# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43729 — [Security audit] - bảo mật hệ thống LME (sns-line) 2026-10-21` |
| Module / Màn hình | Đa màn hình/API — **security audit gồm nhiều lỗ hổng (SEC-05 → SEC-09)**: Webhook LINE PHP (`POST /line/callback/add/{bot_id}`) · Command auto-reply theo từ khoá (`HandleCallbackMessage.php`) · Đặt chỗ sự kiện LIFF (`MobileEventBookingController`) · Route Telecom (4 URL) · Chat realtime (node_serve socket + chat web/mobile web/app native) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine gốc đã là tiếng Việt — giữ nguyên văn, không diễn giải lại. -->

Hệ thống đang có nhiều lỗ hổng mức Nghiêm trọng, trong đó phần lớn người lạ không cần đăng nhập cũng khai thác được. Rủi ro thực tế gồm: lộ khóa thanh toán Stripe/Univapay và token LINE của khách hàng (shop), đọc toàn bộ file cấu hình máy chủ (mật khẩu DB), giả mạo trạng thái "đã thanh toán", xem trộm toàn bộ tin nhắn chat realtime, và xóa/sửa dữ liệu của shop khác.

Chi tiết các bug xem các subtask.

Gợi ý thứ tự fix: SEC-05 → SEC-08 → SEC-09 → SEC-06 → SEC-07
(SEC-05 nên đi trước SEC-06, vì khi webhook đã kiểm tra chữ ký thì người lạ không gửi tin nhắn giả được nữa, SQLi chỉ còn bị khai thác từ tài khoản bạn bè LINE thật.)

Branch: release_step_20260930_v2

## Steps to reproduce

<!-- Redmine description KHÔNG có section "Tái hiện bug" — đây là ticket cha tổng hợp nhiều lỗ hổng, description chỉ dẫn "xem các subtask". Redmine REST API không trả về children/relations cho ticket này nên không lấy được chi tiết từng subtask. Chi tiết nguyên nhân/cách fix/điểm cần test theo từng hạng mục nằm ở Journal #146764 (chép nguyên văn cuối file) + 03-dev-impact.md. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có attachment. -->

## Ghi chú thêm của Leader

- Priority: **Urgent** | Status: **Đang fix** | Tracker: Bug tự detect | Author/Assignee: Nguyen Ngoc Hai.
- Ticket cha gộp nhiều lỗ hổng an ninh (SEC-05..SEC-09, nhãn không được Dev map 1:1 vào Journal — chỉ có thứ tự fix đề xuất ở trên). Chi tiết điều tra/cách fix/điểm cần test thực tế nằm trong Journal #146764 (bản đầy đủ nhất, 2026-10-22 04:56) — xem nguyên văn bên dưới + `03-dev-impact.md`.
- Branch gốc: `release_step_20260930_v2` (base `d6c0a2653f63`) → nhánh fix: `ai_studio_fixbug_43729` (head commit `6abe854e10c1894bc9693ac737ce9098e999080a`).
- ⚠️ Trước khi deploy: cần thêm env `SOCKET_JWT_SECRET` cho web (Laravel) + cấu hình `node_serve/config.js` (`socketJwtSecret` cùng giá trị, `allowedOrigins`, `requireSocketToken: false` mặc định — chỉ bật cùng lúc với app #43809 lên store + force update).
- Dev note: bản sao DB điều tra không thấy dấu hiệu đã bị khai thác (không có booking quantity âm, không có split_payment) — nhưng **chưa kiểm production thật** (việc này nằm ngoài phạm vi task, giao cho vận hành).
- Ngoài phạm vi task (Dev ghi rõ, không cover bởi fix này — Leader cân nhắc mở ticket riêng): `plan_price` của thanh toán sự kiện lấy từ client (có thể tự hạ giá) · `rollbackChangeBookingConfirmFail` có lỗi IDOR (giảm chỗ đã dùng của slot bất kỳ) · `KEY_CERTIFICATION_API` bị ghi ra log ở `RichmenuApiController`/`ScenarioApiController` · webhook LINE ở Java callback (`cb.lme.jp`) chưa kiểm chữ ký · 5 test PHPUnit fail sẵn trên base (không liên quan fix này).

## Journal / note từ Redmine (nguyên văn)

**Journal #146708 — Dev Studio — 2026-10-22:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Các điểm nhận dữ liệu từ bên ngoài đều không kiểm dữ liệu đầu vào. Webhook PHP tự tính chữ ký từ chính body nên luôn hợp lệ. Auto-reply nối nguyên text tin nhắn vào SQL. Booking sự kiện dùng quantity do client gửi mà không validate. Callback Telecom chỉ kiểm rel=yes vì lời gọi kiểm IP đã bị xoá từ 2018-05-10. Server socket không xác thực và đẩy mọi tin vào room legacy_client.

Hướng sửa:
- D-1 Webhook LINE kiểm header X-Line-Signature và chặn nhánh bot Olioa
- D-2 Auto-reply dùng tham số SQL thay vì nối chuỗi
- D-3 Validate quantity khi đặt chỗ, đổi lịch và hoàn tác ở booking sự kiện
- D-4 Xoá 4 route Telecom
- D-5 Hotfix server socket: bỏ room legacy, khoá typing, giới hạn origin
- D-6 Các màn web còn sống gửi botCode và token khi kết nối socket
- D-7 PHP phát socket token: service, API mobile và endpoint web
- D-8 Node kiểm token và JS client tự lấy token mới; bắt buộc token sau cờ cấu hình

Ảnh hưởng / rủi ro:
Sửa webhook LINE ở PHP, auto-reply, các API đặt chỗ và thanh toán sự kiện công khai, route Telecom và toàn bộ chat realtime (node, web, API mobile). Rủi ro chính: chặn nhầm webhook thật nếu có relay làm đổi body hoặc header, và app bản cũ mất realtime. Trước khi deploy cần thêm env SOCKET_JWT_SECRET và cấu hình node.
```

**Journal #146764 — Dev Studio — 2026-10-22:**

```
Dev handoff — 22/10 11:55 · nhánh ai_studio_fixbug_43729

Nguyên nhân:
Các điểm nhận dữ liệu từ bên ngoài đều không kiểm dữ liệu đầu vào. Webhook PHP tự tính chữ ký từ chính body nên luôn hợp lệ. Auto-reply nối nguyên text tin nhắn vào SQL. Booking sự kiện dùng quantity do client gửi mà không validate. Callback Telecom chỉ kiểm rel=yes vì lời gọi kiểm IP đã bị xoá từ 2018-05-10. Server socket không xác thực và đẩy mọi tin vào room legacy_client.

Nội dung thay đổi:
- Webhook LINE POST /line/callback/add/{bot_id}: thiếu hoặc sai chữ ký X-Line-Signature → 401, không lưu event; bot Olioa (bot_type=1) → 403; nút Verify của LINE vẫn hoạt động.
- Auto-reply theo từ khoá (command xử lý callback tin nhắn): nội dung tin nhắn đi qua binding SQL, cách khớp từ khoá giữ nguyên.
- Trang đặt chỗ sự kiện (LIFF): đặt mới, đổi lịch, rollback đổi lịch từ chối số lượng không phải số nguyên ≥1 (HTTP 422 + 「予約数は、１以上入力してください」).
- Tắt 4 URL Telecom: /make_form_telecom/{id}, /customer/telecom_callback_tsudo.php, /customer/telecom_callback_keizoku.php, /customer/telecom_callback_fail → 404.
- node_serve (chat realtime): ngắt kết nối không có botCode, bỏ room legacy nhận tin của mọi bot, room typing chỉ theo định dạng bot_staff_{bot}_{hội thoại}, kiểm origin theo cấu hình, kiểm token (cờ requireSocketToken mặc định tắt).
- API mới POST /api/mobile/socket/token cho app (bot phải thuộc user) và POST /ajax/chat/socket-token cho web (bot theo session).
- Màn chat 1:1, chat nhóm, layout mobile web kết nối socket kèm botCode + token, tự lấy token mới mỗi 8 phút; bỏ đoạn script socket chết ở 3 header admin.

File đã sửa (php-web):
  app/Console/Commands/HandleCallbackMessage.php     |  14 +-
  app/Http/Controllers/Admin/BotController.php       |  21 +--
  .../Api/Mobile/SocketTokenMobileController.php     |  73 +++++++++
  .../Basic/MobileEventBookingController.php         |  99 +++++++++---
  .../Controllers/Basic/SocketTokenController.php    |  60 ++++++++
  .../Socket/SocketTokenSecretMissingException.php   |  10 ++
  app/Services/Socket/SocketTokenService.php         | 126 ++++++++++++++++
  config/sns-line.php                                |   3 +
  node_serve/config.example.js                       |   7 +
  node_serve/server.js                               | 161 +++++++++++++++++---
  public/js/chats/chat-v2.js                         |  11 +-
  public/js/chats/socket-auth.js                     | 122 +++++++++++++++
  public/js/mobile/chat.js                           |   3 +-
  resources/views/basic/chat/index.blade.php         |   1 +
  resources/views/chats/chat_group.blade.php         |   3 +-
  resources/views/chats/socket_auth.blade.php        |   8 +
  resources/views/layout/admin/header.blade.php      |   6 -
  resources/views/layout/admin_v2/header.blade.php   |   6 -
  resources/views/layout/v2/admin/header.blade.php   |   6 -
  resources/views/mobile/layout/index.blade.php      |   8 +-
  routes/api.php                                     |   3 +
  routes/web.php                                     |   9 +-
  tests/Feature/AutoReplyKeywordBindingTest.php      |  77 ++++++++++
  .../Feature/EventBookingQuantityValidationTest.php | 165 ++++++++++++++++++++
  tests/Feature/LineWebhookSignatureTest.php         | 160 ++++++++++++++++++++
  tests/Feature/SocketTokenTest.php                  | 167 +++++++++++++++++++++
  tests/Feature/TelecomRoutesRemovedTest.php         |  37 +++++
  tests/Support/RecordingConnection.php              | 132 ++++++++++++++++
  28 files changed, 1407 insertions(+), 91 deletions(-)

Đánh giá ảnh hưởng — Rủi ro trung bình: Chạm luồng nhận webhook của mọi bot và chat realtime; logic có test và kiểm chứng ngược trên base, nhưng chưa chạy với LINE, MySQL và app thật.
- Mọi bot nhận webhook qua PHP: nếu proxy/relay đổi body hoặc bỏ header thì webhook thật bị 401 — theo dõi log sau deploy.
- Command xử lý callback tin nhắn (auto-reply) chạy cho mọi bot — hồi quy từ khoá 'chứa'/'khớp chính xác'.
- Booking sự kiện: đặt mới, đổi lịch, slot đầy, thanh toán Stripe/Univapay của sự kiện (cùng hàm payment).
- Trang LP còn cấu hình Telecom (prod không còn LP nào bật) bấm thanh toán sẽ lỗi do route đã tắt.
- App mobile bản trước 2024-05-16 (không gửi botCode) mất realtime ngay; app hiện tại vẫn chạy khi cờ tắt.
- Màn chat web (1:1, nhóm, chat_11 mobile web): tin mới, typing indicator, xoá cache source_message.
- 3 layout header admin bỏ script socket chết — các trang dùng layout này không còn biến socket.

Migration / thay đổi dữ liệu:
- [Config · Trước deploy] Thêm biến môi trường SOCKET_JWT_SECRET cho web (khoá ký socket token): Sinh chuỗi ngẫu nhiên ≥32 byte (vd: openssl rand -hex 32), thêm SOCKET_JWT_SECRET=<giá trị> vào .env của web; nếu môi trường dùng config cache thì chạy php artisan config:cache.
- [Config · Khi deploy] Cập nhật node_serve/config.js trên server: socketJwtSecret, allowedOrigins, requireSocketToken: Thêm vào config.js của node_serve: socketJwtSecret: '<cùng giá trị SOCKET_JWT_SECRET>', allowedOrigins: ['<hostname APP_URL>', '<hostname URL_OUTSIDE_STEP>'], requireSocketToken: false; sau đó restart node_serve.

Recover dữ liệu: Không cần recover — Đây là lỗ hổng, dữ liệu chỉ hỏng khi có người cố ý khai thác. Bản sao DB không có dấu hiệu bị khai thác: không có booking quantity âm, không có split_payment. Kiểm tra trên production được ghi ở follow-up cho vận hành.

Lưu ý khi deploy:
- Không bump version asset: QA hard-reload các trang chat.
- Restart node_serve sau khi cập nhật server.js và config.js.
- Chỉ bật requireSocketToken khi app #43809 lên store cùng lúc bật force update.

Việc cần người làm thêm (ngoài phạm vi task):
- Thanh toán sự kiện: plan_price đang lấy từ client để tính số tiền gửi Stripe/Univapay, nên người dùng có thể tự hạ giá. Cần ticket riêng để server tự tính số tiền.
- rollbackChangeBookingConfirmFail cho người ngoài giảm số chỗ đã dùng của slot bất kỳ (lỗi IDOR): nên lấy slot và quantity từ booking trong DB. Cần ticket riêng.
- Vận hành kiểm tra trên production xem đã bị khai thác chưa: access log của route webhook và telecom_callback, các slot hoặc plan có counter âm, booking có quantity ≤ 0.
- Đổi KEY_CERTIFICATION_API: key đang bị ghi ra log ở RichmenuApiController và ScenarioApiController, và có trong config.properties của repo Java.
- Dọn code Telecom còn sót sau khi xoá route: các method trong Customers.php và view customers/telecom.blade.php.
- Sau khi bước bắt buộc token chạy ổn định: chuyển salt hashid chat_code ra .env và đổi salt mới.
- Trước khi deploy: thêm env SOCKET_JWT_SECRET cho web (Laravel) và điền cùng giá trị đó vào socketJwtSecret trong config của node_serve; điền allowedOrigins bằng domain web của từng môi trường. Nếu để trống, node sẽ không kiểm origin và chỉ ghi log cảnh báo.
- Bật requireSocketToken trong config node cùng lúc với force update app (#43809), sau khi bản app gửi token đã lên store.
- Sau deploy, xem log 401 của webhook LINE để chắc rằng không có relay nào làm đổi body hoặc bỏ header X-Line-Signature.
- Java callback (cb.lme.jp/line/callback/add/{bot_id}) cũng chưa kiểm chữ ký; theo HaiNN thì việc này thuộc ticket riêng.
- Cải tiến riêng phát hiện khi điều tra: payment() của booking sự kiện lấy plan_price từ client; rollbackChangeBookingConfirmFail có lỗi IDOR; KEY_CERTIFICATION_API đang bị ghi ra log.
- Kiểm log production xem đã có dấu hiệu khai thác các lỗ hổng SEC-05..09 hay chưa (bản sao DB điều tra không thấy dấu hiệu).
- 5 file PHPUnit đang fail sẵn trên base (BillingService, ChatMediaSizeValidation, ContractChangeMailService, ContractExpireService bị Fatal vì mock thiếu method của BotRepositoryInterface, Example) cần được sửa ở ticket khác.
- Vận hành điền allowedOrigins (hostname web của từng môi trường) vào node_serve/config.js; nếu để trống thì không kiểm origin.
- Bật requireSocketToken trên node_serve khi app #43809 lên store và bật force update.
- Webhook LINE ở Java callback (cb.lme.jp) vẫn chưa kiểm chữ ký — theo dõi ticket riêng đã chốt với HaiNN.
- Dọn các method Telecom còn sót trong Customers.php và trang customers/contruct.blade.php (route đã tắt).

Điểm cần test:
- Webhook: thiếu chữ ký hoặc chữ ký sai → 401 và không có callback_event mới. Webhook LINE thật (message, follow, postback) và nút Verify vẫn hoạt động. Bot Olioa → 403.
- Auto-reply: tin chứa ', \ hoặc ' OR SLEEP(5) -- → không lỗi SQL, không chậm. Keyword chứa và keyword khớp chính xác vẫn đúng với cả tiếng Nhật và emoji.
- Đặt chỗ sự kiện: number_order = -1, 0, 0.5, abc hoặc chuỗi SQL → 422 và counter không đổi. Đổi lịch hợp lệ trừ đúng số chỗ; slot đầy vẫn báo 「予約がいっぱいです…」.
- Telecom: 4 URL trả 404.
- Socket bước 1: kết nối không có botCode bị ngắt; join legacy_client, hashid bot khác hoặc chuỗi tuỳ ý → không nhận event; origin lạ bị từ chối, app không bị ảnh hưởng.
- Chat 1:1 web, chat nhóm và chat_11 mobile vẫn realtime (tin mới, typing, xoá cache source_message).
- Socket bước 2 (bật cờ): thiếu, sai hoặc hết hạn token → bị từ chối; token bot A kèm botCode bot B → chỉ nhận tin của bot A; reconnect sau hơn 10 phút vẫn được; API token với bot không có quyền → 403.
- Webhook LINE: gửi POST thiếu header X-Line-Signature hoặc chữ ký sai → 401, không có callback_event mới; tin nhắn, follow, postback thật từ LINE vẫn được nhận; nút Verify trên LINE Console vẫn thành công; bot Olioa → 403.
- Sau deploy xem log 'callbackWebHook invalid signature' để phát hiện webhook thật bị chặn (relay/proxy đổi body).
- Auto-reply trên staging: từ khoá 'chứa' và 'khớp chính xác', tiếng Nhật, emoji, tin có ' và \ và ' OR SLEEP(5) -- → trả lời đúng, không lỗi SQL, không chậm.
- Đặt chỗ sự kiện: sửa request number_order = -1, 0, 0.5, abc, '1)) or sleep(5) or ((1' → 422 với 「予約数は、１以上入力してください」, counter slot/plan không đổi; đặt mới/đổi lịch hợp lệ trừ đúng chỗ; slot đầy vẫn báo 「予約がいっぱいです…」.
- 4 URL Telecom trả 404.
- Chat 1:1, chat nhóm, chat_11 mobile web: tin mới, typing, xoá cache vẫn realtime; để trang mở hơn 10 phút rồi ngắt/nối mạng vẫn nối lại được.
- Mở 2 tab, đổi bot ở tab 2, chờ hơn 8 phút rồi ngắt mạng tab 1: ghi nhận hành vi realtime của tab 1 (xem R-1).
- Socket: kết nối không có botCode bị ngắt; origin lạ bị từ chối khi đã điền allowedOrigins; app mobile hiện tại vẫn realtime khi cờ tắt.
- API POST /api/mobile/socket/token: bot không thuộc user → 403, bot_id không phải số → 400, hợp lệ → socket_token, bot_code, expires_in=600.

Branch: ai_studio_fixbug_43729
- sns-line: ai_studio_fixbug_43729 (nhánh gốc release_step_20260930_v2 @d6c0a2653f63, commit 6abe854e10c1894bc9693ac737ce9098e999080a)
```
