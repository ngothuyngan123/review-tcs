# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43212 — [Callback] Verify chữ ký webhook LINE (X-Line-Signature) cho /line/callback/add/{botId}` |
| Module / Màn hình | Callback nhận webhook LINE — endpoint `POST /line/callback/add/{botId}` (service `linect-service`, module `callback`, repo java-job). Không phải màn hình admin, không có UI end-user. |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Ticket gốc đã viết bằng tiếng Việt — giữ nguyên văn, không tóm tắt. Đây là ticket "Improve nội bộ" (hardening bảo mật), không phải bug khách hàng report, nên không có block 原文 JP / Section tái hiện riêng. -->

- LINE gửi webhook vào POST /line/callback/add/{botId}. Hiện endpoint này không verify request có thật sự đến từ LINE hay không.
- Controller nhận toàn bộ header và body gốc dạng byte[], chuyển xuống bước save callback. Không verify ở controller, để response trả về LINE không chậm.
- Verify ở bước save callback và đưa vào queue (jobInsertCallbackNew, và nhánh không dùng insert queue):
  + Dùng bots.channel_secret, lấy từ query bot sẵn có nên không thêm query.
  + So sánh constant-time.
- Khi verify không pass thì log #verifyLineSignature, gồm result, botId, keyCallback, webhookEventId và toàn bộ header. Giá trị Authorization / Cookie được che thành ***
- Đọc plan mode ở file đính kèm m_202610_verify_line_signature-before-code.md
- Tài liệu của LINE: https://developers.line.biz/en/docs/messaging-api/verify-webhook-signature/

## Steps to reproduce

<!-- Không có — ticket không phải bug khách hàng báo, không có bước tái hiện. -->

## Expected result

-

## Actual result

-

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact. Cụ thể: đây là ticket **Improve nội bộ** (Dev tự đề xuất hardening bảo mật webhook), không phải bug khách hàng report — Dev tự thiết kế qua 3 phiên bản (v1 → v2 → v3) rồi handoff bản cuối, không có "steps to reproduce" theo nghĩa thông thường.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

File thiết kế (plan mode, Dev đính kèm trong description — **nên đọc trước khi viết TC**, không phải ảnh/video/log):
- `m_202610_verify_line_signature-before-code.md` — https://redmine.melonglobal.net/attachments/download/34054/m_202610_verify_line_signature-before-code.md

## Ghi chú thêm của Leader

- Ticket thuộc tracker **Improve nội bộ** (hardening bảo mật), không phải bug khách hàng báo — không có ca lỗi cụ thể / dữ liệu định danh ca lỗi (đã bỏ section đó).
- Root cause + hướng fix do Dev tự thiết kế, trải qua 3 bản thiết kế trong journal (v1 #144448 → v2 #144620 → v3 #144654), rồi Dev handoff bản cuối ở Journal #145236 (2026-10-19) — đây là nguồn chính cho file 03.
- **3 mode cấu hình `LINE_WEBHOOK_SIGNATURE_MODE`** (config.properties server callback, cần restart app để áp dụng):
  - `0` = OFF (không verify)
  - `1` = LOG_ONLY (**mặc định** nếu không khai báo key — hành vi xử lý event KHÔNG đổi, chỉ log)
  - `2` = ENFORCE (bỏ event có chữ ký không hợp lệ — không lưu, không xử lý, vẫn trả 200 cho LINE)
  - Ghi sai định dạng (có khoảng trắng cuối dòng, không đúng 0/1/2) → app callback **không khởi động**.
- **2 nhánh lưu callback cần test riêng**: `jobInsertCallbackNew` (MODE BACKEND/BACKUP, dùng insert queue) và nhánh lưu trực tiếp trong `addCallback` (không dùng insert queue).
- Lỗi bất ngờ trong bước `checkLineSignature` (vd exception khi tính HMAC) → event vẫn được lưu & xử lý như trước khi có tính năng verify (không bị mất), có log `#checkLineSignature Exception` + báo Chatwork room exception (chống lặp tối đa 1 tin/60 giây) — đúng ở mọi mode kể cả ENFORCE.
- Header gốc được gỡ khỏi `CallbackEvent` ngay sau khi verify — field `requestHeaders` là transient, không được lộ trong log `#jobInsertCallbackNew` (JSON của CallbackEvent) hay `CallbackEvent.toString()`.
- Log `#verifyLineSignature` khi verify không pass phải che `Authorization` / `Proxy-Authorization` / `Cookie` thành `***`, không chứa channel secret.
- Nhánh code: `ai_studio_implement_43212` (gốc `release-callback-t09-2026` @14c120f4de27, commit 642e4b446406be410c2b8b8021eb6193fea4329b).
- ⚠️ Nhánh base `release-callback-t09-2026` đang thiếu dependency `com.squareup.retrofit2:converter-jackson:2.3.0` → `gradle compileJava` lỗi sẵn ở `RequestHelper`, **không do task này gây ra** — không phải thứ cần verify khi review TC của ticket này, chỉ cần biết để không nhầm là bug mới.
- Môi trường: test trên dev trước, verify ENFORCE cần restart app sau khi set `LINE_WEBHOOK_SIGNATURE_MODE=2`; theo kế hoạch deploy, prod sẽ giữ LOG_ONLY 2-3 ngày theo dõi log rồi mới bật ENFORCE — TC nên bao cả 3 mode trên môi trường test được.

## Journal / note từ Redmine (nguyên văn)

**Journal #144448 — Dev Studio — 2026-10-15:**

```
Dev Studio · Nội dung thực hiện

Đã viết thiết kế v1 cho việc verify chữ ký webhook LINE. Thiết kế làm theo plan đính kèm ticket và đã đối chiếu với code nhánh base. Controller chỉ chuyển toàn bộ header và body gốc xuống, việc verify nằm ở bước save callback (cả hai nhánh), dùng channel_secret của bot đã query sẵn nên không thêm query nào. Có cờ OFF / LOG_ONLY / ENFORCE, mặc định LOG_ONLY. Bổ sung so với plan: báo Chatwork khi verify gặp exception bất ngờ, và thêm unit test thuật toán. Không có câu hỏi chặn, có thể thực thi.

Hướng sửa:
- D-1 Thêm hằng số mode và cấu hình LINE_WEBHOOK_SIGNATURE_MODE (mặc định LOG_ONLY)
- D-2 Tạo class LineWebhookSignatureVerifier (verify HMAC-SHA256 constant-time, log header có che)
- D-3 Thêm field transient requestHeaders vào CallbackEvent, getter đánh @JsonIgnore
- D-4 Controller nhận HttpHeaders và body byte[], addCallback thêm tham số headers
- D-5 Thêm checkLineSignature và gọi ở jobInsertCallbackNew và nhánh không dùng insert queue
- D-6 Viết unit test JUnit 4 cho LineWebhookSignatureVerifier (không dùng DB)

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng luồng nhận webhook LINE ở hai nhánh save callback. Mặc định LOG_ONLY nên hành vi xử lý event không đổi. Rủi ro chính: bật ENFORCE khi DB lưu sai hoặc thiếu channel_secret thì event thật bị bỏ, nên phải theo dõi log LOG_ONLY trước khi bật.
```

**Journal #144620 — Dev Studio — 2026-10-15:**

```
Dev Studio · Nội dung thực hiện

Được, có thể giữ @RequestBody String như cũ mà verify vẫn đúng. Tôi đã mở bản thiết kế v2. Theo thư viện Spring đang dùng, body được decode bằng UTF-8, và LINE luôn gửi UTF-8, nên mã hoá lại thành byte UTF-8 sẽ ra đúng byte LINE đã ký. Bản v2 đưa controller về String, chỉ nhận thêm header. Bản v2 cũng gỡ header khỏi event ngay sau khi verify, theo gợi ý của review. Các phần khác của v1 giữ nguyên, có thể thực thi ngay.

Hướng sửa:
- D-7 Đưa controller về lại @RequestBody String, vẫn nhận thêm HttpHeaders
- D-8 Gỡ header khỏi CallbackEvent ngay trong checkLineSignature

Ảnh hưởng / rủi ro:
Chỉ sửa CallbackController và hàm checkLineSignature. Cách đọc body trở về giống hệt code cũ, nên rủi ro đổi nội dung callback_event.request không còn. Verify chữ ký vẫn đúng với webhook LINE (UTF-8).
```

**Journal #144654 — Dev Studio — 2026-10-15:**

```
Dev Studio · Nội dung thực hiện

Đã viết lại bản thiết kế v3, chỉ còn mục D-9 theo yêu cầu. Hàm checkLineSignature được bọc try/catch: khi lỗi thì ghi log, notify Chatwork (chống lặp 60 giây) và cho event đi tiếp như trước khi có verify, để event không bị mất hay không được save. Hai rủi ro không sửa vẫn được ghi trong tài liệu: lỗi khi tính HMAC vẫn trả kết quả sai chữ ký như v1, và cấu hình mode sai định dạng làm app không khởi động. Có thể thực thi ngay.

Hướng sửa:
- D-9 Bọc try/catch cho checkLineSignature, notify Chatwork và cho event đi tiếp khi lỗi

Ảnh hưởng / rủi ro:
Chỉ sửa hàm checkLineSignature. Luồng bình thường không đổi. Khi có lỗi bất ngờ, event được xử lý như trước khi có tính năng verify, kèm log và Chatwork.
```

**Journal #145236 — Dev Studio — 2026-10-19:**

```
Dev handoff — 16/10 08:58 · nhánh ai_studio_implement_43212

Tóm tắt:
Callback LME kiểm chữ ký X-Line-Signature của webhook LINE trước khi lưu callback_event, dùng channel secret của bot. Mặc định là LOG_ONLY: chữ ký sai hoặc thiếu chỉ ghi log #verifyLineSignature, event vẫn xử lý như cũ; ENFORCE (bật bằng cấu hình) mới bỏ event giả. Body vẫn đọc như code cũ, header được gỡ khỏi event sau khi verify, và lỗi bất ngờ khi kiểm chữ ký sẽ báo Chatwork rồi cho event đi tiếp. Khi test cần chú ý 3 mode, 2 nhánh lưu, nội dung callback_event.request của tin tiếng Nhật/emoji và việc che Authorization/Cookie trong log.

Nội dung thay đổi:
- Endpoint webhook POST /line/callback/add/{botId} (module callback): nhận thêm header gốc; cách đọc body, route và response 200 không đổi.
- Bước lưu callback (thread insert queue và nhánh lưu trực tiếp): verify HMAC-SHA256 bằng channel secret của bot, so sánh constant-time. Chữ ký sai/thiếu → log warn #verifyLineSignature (result, mode, isDrop, botId, keyCallback, webhookEventId, độ dài body, toàn bộ header; Authorization/Proxy-Authorization/Cookie che ***). Header được gỡ khỏi event sau khi verify.
- Lỗi bất ngờ trong bước kiểm chữ ký → log #checkLineSignature Exception + báo Chatwork room exception (tối đa 1 tin/60 giây); event vẫn lưu và xử lý ở mọi mode.
- Cấu hình mới LINE_WEBHOOK_SIGNATURE_MODE: 0 tắt, 1 chỉ log (mặc định), 2 bỏ event có chữ ký không hợp lệ (không lưu, không xử lý, vẫn trả 200).

File đã sửa (java-job):
  src/main/java/sns/line/ConfigFile.java             |   3 +
  .../sns/line/controller/CallbackController.java    |   6 +-
  .../line/helper/LineWebhookSignatureVerifier.java  | 116 +++++++++++++++++++++
  .../models/backenddb/entities/CallbackEvent.java   |  15 +++
  .../java/sns/line/task/HandlePostbackTask.java     |  57 +++++++++-
  src/main/java/sns/line/values/Constants.java       |  14 +++
  .../helper/LineWebhookSignatureVerifierTest.java   | 111 ++++++++++++++++++++
  7 files changed, 319 insertions(+), 3 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Mặc định LOG_ONLY nên hành vi xử lý không đổi; body đọc như cũ, không thêm query nào, và lỗi bất ngờ vẫn cho event đi tiếp. Event thật chỉ có thể mất khi bật ENFORCE mà bot thiếu hoặc sai secret.
- Toàn bộ luồng nhận webhook LINE (follow, unfollow, message, postback, unsend…): mọi event đều đi qua controller đã sửa.
- jobInsertCallbackNew (MODE BACKEND/BACKUP) và nhánh lưu trực tiếp trong addCallback: thêm bước verify ngay trước khi lưu.
- Log #jobInsertCallbackNew (JSON của CallbackEvent) và CallbackEvent.toString(): không được lộ header.
- Room Chatwork exception: có thêm tin #checkLineSignature Exception / #verifyLineSignature Exception (chỉ khi có lỗi, có chống lặp).
- Notify Chatwork multi-event: ở ENFORCE, request bị bỏ thì không có notify.

Migration / thay đổi dữ liệu:
- [Config · Sau deploy] Key tuỳ chọn LINE_WEBHOOK_SIGNATURE_MODE trong config.properties của server callback (0 OFF / 1 LOG_ONLY / 2 ENFORCE): Không bắt buộc khi deploy: không khai báo thì giá trị là 1 (LOG_ONLY). Khi muốn bật chặn: thêm dòng LINE_WEBHOOK_SIGNATURE_MODE=2 (đúng giá trị, không khoảng trắng cuối) vào config.properties của server callback rồi restart app.

Lưu ý khi deploy:
- Deploy không cần khai báo key (mặc định LOG_ONLY). Theo dõi log #verifyLineSignature và #checkLineSignature Exception 2–3 ngày; chỉ đặt LINE_WEBHOOK_SIGNATURE_MODE=2 rồi restart khi request thật không còn ra MISSING_SECRET/INVALID_SIGNATURE. Rollback: đặt 0 hoặc 1 rồi restart.
- Ghi giá trị đúng 0, 1 hoặc 2 (không có khoảng trắng cuối dòng): ghi sai định dạng sẽ làm app callback không khởi động, giống các key số khác.
- Build: base đang thiếu dependency converter-jackson cho RequestHelper (lỗi có sẵn, không do task này gây ra).

Việc cần người làm thêm (ngoài phạm vi task):
- Lỗi compile có sẵn trên nhánh base ở RequestHelper (thiếu thư viện converter-jackson) không do task này gây ra, cần người phụ trách build kiểm tra riêng.
- Khi deploy giữ mặc định LOG_ONLY, theo dõi log #verifyLineSignature và #checkLineSignature Exception 2-3 ngày, xử lý bot thiếu/sai channel_secret trước khi đặt LINE_WEBHOOK_SIGNATURE_MODE=2 (ENFORCE); giá trị phải ghi đúng 0/1/2, không có khoảng trắng, nếu không app sẽ không khởi động.
- Base release-callback-t09-2026 thiếu dependency com.squareup.retrofit2:converter-jackson:2.3.0 nên gradle compileJava lỗi ở RequestHelper; đội release nên bổ sung (ngoài phạm vi ticket).
- Sau 2–3 ngày chạy LOG_ONLY: thống kê log #verifyLineSignature theo botId và result, sửa channel_secret của các bot ra MISSING_SECRET/INVALID_SIGNATURE trước khi bật ENFORCE.

Điểm cần test:
- checkLineSignature gặp lỗi bất ngờ: event vẫn được save và xử lý, có log #checkLineSignature Exception, Chatwork tối đa 1 tin trong 60 giây; đúng ở cả 2 nhánh (có và không có insert queue) và mọi mode, kể cả ENFORCE
- Luồng bình thường không đổi: LOG_ONLY / ENFORCE / OFF như v1, v2; 8 unit test cũ pass
- LOG_ONLY (mặc định): event LINE thật (tiếng Nhật, emoji, sticker, postback, follow) xử lý bình thường, không có log #verifyLineSignature; callback_event.request giống như trước khi sửa.
- LOG_ONLY: POST giả không có hoặc sai X-Line-Signature → trả 200, log '#verifyLineSignature ... isDrop false' có đủ header; event vẫn lưu và vẫn xử lý.
- ENFORCE (LINE_WEBHOOK_SIGNATURE_MODE=2, restart): request giả → 200, log isDrop true, không có row callback_event mới; event LINE thật vẫn qua.
- OFF (=0): không verify, không có log #verifyLineSignature.
- Log lỗi hiện Authorization/Cookie là ***, không có channel secret; log #jobInsertCallbackNew không chứa header.
- Lỗi bất ngờ trong bước kiểm chữ ký (giả lập trên dev bằng debug): event vẫn lưu và xử lý, có log #checkLineSignature Exception, Chatwork tối đa 1 tin/60 giây.
- Kiểm cả server MODE BACKEND/BACKUP (insert queue) và MODE khác (lưu trực tiếp).
- Reissue channel secret rồi cập nhật bot → event sau verify OK mà không cần restart.
- So #addCallback runTime và #jobInsertCallbackNew done timeSave trước/sau: không tăng đáng kể.

Branch: ai_studio_implement_43212
- linect-service: ai_studio_implement_43212 (nhánh gốc release-callback-t09-2026 @14c120f4de27, commit 642e4b446406be410c2b8b8021eb6193fea4329b)
```
