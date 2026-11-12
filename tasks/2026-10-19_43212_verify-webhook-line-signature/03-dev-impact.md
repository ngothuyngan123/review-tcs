# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | `<chưa có — không tìm thấy link PR/commit review trong description/journal, chỉ có commit hash cuối branch>` |
| Branch | `ai_studio_implement_43212` (gốc `release-callback-t09-2026` @14c120f4de27, commit `642e4b446406be410c2b8b8021eb6193fea4329b`) |
| Ngày submit đánh giá | 2026-10-19 (Journal #145236 — bản handoff cuối, tổng hợp v1 #144448 + v2 #144620 + v3 #144654) |
| Auto-filled | 2026-10-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ Input thiếu: Redmine ticket này không viết theo khuôn 4 mục chuẩn (1. Nguyên nhân / 2. Cách fix / 3. Function caller / 4. Đánh giá ảnh hưởng) trong 1 section liền — nội dung được Dev trải ra qua 4 journal (v1 → v2 → v3 → handoff cuối). Nội dung dưới đây được **tổng hợp lại** từ cả 4 journal, giữ nguyên văn Dev viết, KHÔNG diễn giải thêm. Leader/tester nên đối chiếu lại journal gốc ở file 01 trước khi tick checkbox trên.

---

## 1. Nguyên nhân

LINE gửi webhook vào `POST /line/callback/add/{botId}`. Hiện endpoint này không verify request có thật sự đến từ LINE hay không — Controller nhận toàn bộ header và body gốc, chuyển thẳng xuống bước save callback mà không verify chữ ký (`X-Line-Signature`), nên request giả mạo (không phải từ LINE) vẫn được lưu và xử lý như event thật.

(Không verify ngay ở Controller để response trả về LINE không bị chậm — verify được dời xuống bước save callback.)

## 2. Cách fix

Tổng hợp 3 bản thiết kế (v1 → v2 → v3) + handoff cuối:

- **D-1** Thêm hằng số mode + cấu hình `LINE_WEBHOOK_SIGNATURE_MODE` (mặc định `LOG_ONLY` nếu không khai báo trong `config.properties`). 3 giá trị: `0`=OFF, `1`=LOG_ONLY, `2`=ENFORCE.
- **D-2** Tạo class `LineWebhookSignatureVerifier` — verify HMAC-SHA256 **constant-time** dùng `bots.channel_secret` (đã query sẵn, không thêm query), log header có che `Authorization`/`Proxy-Authorization`/`Cookie` thành `***`.
- **D-3** Thêm field `transient requestHeaders` vào `CallbackEvent`, getter đánh `@JsonIgnore` (v1) — sau đó ở v2 (**D-8**) đổi hướng: **gỡ header khỏi `CallbackEvent` ngay trong `checkLineSignature`** sau khi verify xong, không giữ lại trong object.
- **D-4** (v1) Controller đổi nhận `HttpHeaders` + body `byte[]`, `addCallback` thêm tham số `headers` → **D-7** (v2, ghi đè lại D-4): quay về `@RequestBody String` như code cũ (vẫn nhận thêm `HttpHeaders`) — lý do: Spring decode body bằng UTF-8, LINE luôn gửi UTF-8, mã hoá lại thành byte UTF-8 ra đúng byte LINE đã ký, nên **không cần đổi cách đọc body**, giảm rủi ro đổi `callback_event.request`.
- **D-5** Thêm hàm `checkLineSignature`, gọi ở cả 2 nhánh save callback: `jobInsertCallbackNew` (MODE BACKEND/BACKUP, dùng insert queue) **và** nhánh không dùng insert queue (lưu trực tiếp trong `addCallback`).
- **D-6** Viết unit test JUnit 4 cho `LineWebhookSignatureVerifier` (không dùng DB).
- **D-9** (v3) Bọc `try/catch` toàn bộ `checkLineSignature`: khi lỗi bất ngờ (exception khi tính HMAC, v.v.) → ghi log `#checkLineSignature Exception`, báo Chatwork room exception (chống lặp tối đa 1 tin/60 giây), và **cho event đi tiếp như trước khi có verify** (không mất event, không chặn save) — đúng ở mọi mode kể cả ENFORCE.

Khi chữ ký sai/thiếu (verify không pass): log warn `#verifyLineSignature` gồm `result`, `mode`, `isDrop`, `botId`, `keyCallback`, `webhookEventId`, độ dài body, toàn bộ header (che `Authorization`/`Proxy-Authorization`/`Cookie`). Ở mode `ENFORCE` (`isDrop=true`) → event **không được lưu, không xử lý**, nhưng vẫn trả `200` cho LINE. Ở mode `LOG_ONLY` (`isDrop=false`) → vẫn log nhưng event xử lý bình thường như cũ.

Rủi ro Dev tự đánh giá (không sửa, chỉ ghi nhận): (1) lỗi khi tính HMAC vẫn có thể trả kết quả sai chữ ký; (2) cấu hình mode sai định dạng (không đúng `0`/`1`/`2`, có khoảng trắng cuối dòng) làm app callback **không khởi động**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev không liệt kê riêng mục "function caller đã check" theo đúng khuôn mẫu — raw text suy từ file list ở Journal #145236 (Dev handoff). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `sns/line/ConfigFile.java` | +3 dòng | Thêm đọc config `LINE_WEBHOOK_SIGNATURE_MODE` |
| 2 | `sns/line/controller/CallbackController.java` | +6/-? dòng | Controller nhận thêm `HttpHeaders` gốc, giữ `@RequestBody String` như cũ (D-7) |
| 3 | `sns/line/helper/LineWebhookSignatureVerifier.java` | **File mới**, +116 dòng | Verify HMAC-SHA256 constant-time + build log che header nhạy cảm |
| 4 | `models/backenddb/entities/CallbackEvent.java` | +15 dòng | Field liên quan header cho bước verify (gỡ ngay sau khi verify — D-8) |
| 5 | `sns/line/task/HandlePostbackTask.java` | +57/-? dòng | Gọi `checkLineSignature` ở nhánh save callback (D-5) — cần xác nhận với Dev đây là nhánh `jobInsertCallbackNew` hay nhánh lưu trực tiếp (file list không ghi rõ, chỉ số dòng thay đổi lớn nhất trong các file sửa) |
| 6 | `sns/line/values/Constants.java` | +14 dòng | Thêm hằng số mode (OFF/LOG_ONLY/ENFORCE) + tag log |
| 7 | `helper/LineWebhookSignatureVerifierTest.java` | **File mới**, +111 dòng | Unit test JUnit 4 cho verifier (D-6), không dùng DB — Dev báo "8 unit test cũ pass" ở điểm cần test |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CallbackController.addCallback` (`POST /line/callback/add/{botId}`) | `CallbackController.java` | Direct | Nhận thêm `HttpHeaders` gốc; route, cách đọc body (`@RequestBody String`), response `200` **không đổi** |
| F2 | `LineWebhookSignatureVerifier` (verify HMAC-SHA256 constant-time) | `LineWebhookSignatureVerifier.java` (mới) | Direct | Dùng `bots.channel_secret` đã query sẵn; build log che `Authorization`/`Proxy-Authorization`/`Cookie` |
| F3 | `checkLineSignature` (gọi verifier, bọc try/catch D-9, log/Chatwork khi lỗi) | `HandlePostbackTask.java` (suy đoán — cần Dev xác nhận) | Direct | Gọi ở **cả 2 nhánh** save callback: `jobInsertCallbackNew` (insert queue, MODE BACKEND/BACKUP) và nhánh lưu trực tiếp trong `addCallback` |
| F4 | `CallbackEvent` (entity, gỡ header sau verify) | `CallbackEvent.java` | Direct | Header chỉ tồn tại tạm trong lúc verify, bị gỡ khỏi event trước khi log/lưu — không được lộ trong `CallbackEvent.toString()` hoặc log `#jobInsertCallbackNew` |
| F5 | Đọc cấu hình `LINE_WEBHOOK_SIGNATURE_MODE` | `ConfigFile.java`, `Constants.java` | Direct | Không khai báo → mặc định `1` (LOG_ONLY); sai định dạng → app không khởi động |
| F6 | Toàn bộ pipeline nhận webhook LINE (follow/unfollow/message/postback/unsend…) | nhiều module xử lý event | Indirect | Mọi event LINE đều đi qua `CallbackController` đã sửa + bước verify mới trước khi lưu |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `callback_event` (bảng lưu event webhook) | Không đổi schema, nhưng **ở mode ENFORCE + chữ ký sai/thiếu → row KHÔNG được INSERT** (event bị bỏ hoàn toàn) | Khác hành vi so với trước (trước đây luôn lưu) — chỉ xảy ra khi `LINE_WEBHOOK_SIGNATURE_MODE=2` |
| D2 | `config.properties` (server callback) | CREATE (key mới, optional) | `LINE_WEBHOOK_SIGNATURE_MODE=0/1/2`; không khai báo = mặc định `1`; sai format → app không khởi động |
| D3 | Log application — tag `#verifyLineSignature`, `#checkLineSignature Exception` | CREATE (log entry mới) | Chứa `result`/`mode`/`isDrop`/`botId`/`keyCallback`/`webhookEventId`/độ dài body/toàn bộ header (che 3 field nhạy cảm) — **không chứa channel_secret** |
| D4 | Chatwork room exception | CREATE (message mới, có điều kiện) | Chỉ gửi khi `checkLineSignature` gặp exception bất ngờ; chống lặp tối đa 1 tin / 60 giây |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Toàn bộ luồng nhận & xử lý webhook LINE (follow, unfollow, message, postback, unsend, …) qua `/line/callback/add/{botId}` | F1, F3, F6, D1 | Medium — mặc định LOG_ONLY nên hành vi KHÔNG đổi (risk thấp), nhưng khi set ENFORCE mà bot thiếu/sai `channel_secret` → **mất event thật** (risk cao cho nhánh này cụ thể, cần theo dõi log trước khi bật) |
| T2 | Job lưu callback nền — `jobInsertCallbackNew` (MODE BACKEND/BACKUP, insert queue) | F3, D1 | Medium — thêm bước verify ngay trước khi lưu, cần test riêng với nhánh lưu trực tiếp (không insert queue) để tránh lệch hành vi giữa 2 nhánh |
| T3 | Nội dung `callback_event.request` lưu lại (đặc biệt tin tiếng Nhật / emoji / sticker) | F1 (D-7: giữ `@RequestBody String` như cũ) | Low — Dev khẳng định cách đọc body không đổi, nhưng nên có TC regression xác nhận bytes UTF-8 giữ nguyên |
| T4 | Alerting/monitoring qua Chatwork room exception | F3, D4 | Low — chỉ thêm message mới khi có lỗi bất ngờ, có chống lặp; rủi ro spam thấp nhưng nên test đúng cơ chế chống lặp 60s |
| T5 | Performance endpoint callback (`addCallback` runTime, `jobInsertCallbackNew` timeSave) | F1, F2, F3 | Low — Dev yêu cầu so sánh thời gian trước/sau, kỳ vọng không tăng đáng kể (PERF regression) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **đặc biệt xác nhận F3/mục 3-#5: `checkLineSignature` gọi ở `HandlePostbackTask` hay module khác, và tên chính xác của 2 nhánh save callback**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
