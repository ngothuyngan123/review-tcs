# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #44381 bằng `/new-task` (2026-11-10). Đây là ticket **Feature** (không phải Bug) — không có section "Tái hiện bug" trong Redmine, Steps/Expected/Actual để trống theo quy định.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44381 — [Tính năng forward webhook] Bổ sung mục chữ ký 署名シークレット cho phần forward webhook phía Line` |
| Module / Màn hình | Màn `Webhook転送` (forward webhook) — tab `LINE公式アカウントデータ転送` (kênh LINE) và tab `L Messageデータ転送` (kênh L Message) |

## Mô tả bug (bản dịch tiếng Việt)

Hiện tại tính năng forward webhook phía LINE (`LINE公式アカウントデータ転送`) không có phần chữ ký `署名シークレット` (secret ký) như bên forward webhook LME (kênh L Message).

=> Cần bổ sung thêm.

⚠️ Đây là ticket **Feature** — Redmine không có section "Tái hiện bug" (không phải lỗi tái hiện được, mà là yêu cầu bổ sung tính năng còn thiếu). Toàn bộ nội dung "thiết kế / cách làm" nằm ở các journal Dev handoff — xem file [03-dev-impact.md](03-dev-impact.md) và phần Journal nguyên văn bên dưới.

## Steps to reproduce

<!-- N/A — ticket Feature, không có bug để tái hiện. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- webhook-1.png — https://redmine.melonglobal.net/attachments/download/37792/webhook-1.png

## Ghi chú thêm của Leader

- Ticket đã đi qua **3 vòng kế hoạch + dev handoff** (30/10, 06/11, 09/11×2) — hành vi cuối cùng (chốt ngày 09/11 17:25, Journal #153437) **khác** 2 vòng đầu ở điểm quan trọng:
  - Vòng 1 (30/10 – 06/11): kênh LINE gửi **secret thô** (giống cách kênh L Message "đang làm" tại thời điểm đó) trong header `X-Lme-Signature`.
  - Vòng 2 (09/11 14:32 – 09/11 17:25, theo quyết định của Tu ngày 09/11): đổi sang **HMAC-SHA256(body, secret)** cho **CẢ 2 kênh** (LINE và L Message) — tức là **đổi luôn hành vi kênh L Message đang chạy production** (trước đây header = secret thô, giờ = HMAC).
  - **Khi viết/review TC, bám theo hành vi vòng cuối (HMAC cho cả 2 kênh)** — không dùng mô tả "secret thô" ở các journal cũ.
- Độ trễ hiệu lực secret mới sau `再生成`: tối đa **~60 giây** (do job cache cấu hình 60s) — áp dụng cho cả 2 kênh, Dev xác nhận giữ nguyên như kênh L Message (không sửa thành realtime).
- Thứ tự deploy **bắt buộc**: `migration → deploy web → chạy lệnh backfill → deploy job`. Job lên trước migration sẽ làm dừng forward **cả 2 kênh**.
- Trước khi deploy job: CS/BA phải báo khách đang tích hợp kênh L Message rằng `X-Lme-Signature` đổi từ secret thô sang HMAC-SHA256, và cập nhật trang `使い方を見る` — đây là thay đổi **breaking** với khách hàng ngoài đang verify theo cách cũ.
- Nhiều bug con đã phát sinh và được fix ngay trong quá trình triển khai (xem chi tiết Journal #153313 / #153437):
  - `#45605` / `#5102`: deadlock MySQL khi 2 request mở màn đồng thời trên bot chưa có config → đã sửa (tạo dòng trước, khoá sau, retry tối đa 3 lần).
  - `#45606` / `#5102`: gọi `再生成` khi bot chưa có cấu hình trả `422` (sai) → đã sửa thành tạo cấu hình + trả `200`.
  - `#45607` / `#5103`: **không phải bug** — độ trễ ≤60s sau `再生成` là hành vi được chấp nhận (theo quyết định Tu 09/11), **BA cần cập nhật spec BR-C01-4/CON-T1 và TC `NEW-48`** cho khớp.
  - `#5141`: gap lock khi tạo dòng đồng thời → đã sửa (tạo dòng ngoài transaction trước, chỉ lock dòng đã tồn tại).
  - `#5455`: log cảnh báo (WARN) khi kênh LINE gửi không có chữ ký bị chặn 1 lần/bot/giờ (sai so với spec — spec yêu cầu WARN **mỗi lần gửi/retry**) → đã sửa; chỉ **Chatwork** mới giữ throttle 1 tin/bot/giờ.
- **Việc cần người khác làm thêm (ngoài phạm vi code task, Leader cần theo dõi)**:
  - BA cập nhật spec `FA-051` xác nhận quyết định cũ (#40475/#40543 dùng secret thô) đã bị thay bằng HMAC cho cả 2 kênh (HieuTM, 06/11).
  - BA cập nhật spec `#44381` (`BR-C01-4`, `CON-T1`) + testcase `NEW-48` theo quyết định trễ ≤60s (Tu, 09/11).
  - CS/BA sửa trang `使い方を見る` (`lme.jp/manual/api_webhook/`) hướng dẫn verify HMAC cho cả 2 kênh, và CS phải báo khách đang tích hợp kênh L Message **trước khi deploy job** (đổi hợp đồng header).
  - Dev tự ghi nhận: `docs/api/webhook-relay-outbound-contract.md` đã được Dev cập nhật trong code, nhưng spec `FA-051` ở `spec-features/` (sub-repo) vẫn ghi sai (HMAC) so với hành vi cũ — cần đối chiếu lại khi review (file 03 + §4/§8 report sẽ dùng `spec-features/` làm nguồn, không dùng docs trong code).
  - Đội build: `build.gradle` của `linect-service` thiếu khai báo dependency `converter-jackson` — compile lỗi sẵn trên base, không phải do task này (ghi nhận ngoài phạm vi).
- `/review-tc` sẽ cần đọc kỹ `spec-features/` của feature forward webhook (nếu có) để đối chiếu — tên mã `FA-051` được Dev nhắc tới trong journal.

## Dữ liệu định danh ca lỗi

<!-- Ticket Feature, không có ca lỗi cụ thể của khách hàng — bỏ section theo quy định. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #149841 — Dev Studio — 2026-10-30:**

```
Dev Studio · Kế hoạch chia task con

Ticket chạm cả web lẫn job nên tôi chia thành 2 task con: T1 web và T2 job. T1 thêm khối 「署名シークレット」 vào tab LINE, mỗi kênh có secret riêng (2 cột DB mới), API xem/copy/tạo lại phải gửi kèm kênh, và có lệnh backfill cho bot cũ. T2 cho job kênh LINE gửi kèm header X-Lme-Signature. Spec ghi header là chữ ký HMAC, nhưng kênh LME đang gửi secret thô. Theo câu trả lời "làm giống kênh LME", tôi cho kênh LINE gửi cùng kiểu với kênh LME. Không có câu hỏi chặn, kế hoạch sẵn sàng để chốt.

Task con (làm lần lượt):
- T1 [PHP Web] Secret riêng cho kênh LINE: DB, API, màn Webhook転送 và lệnh backfill
- T2 [Java Job] Job forward kênh LINE gửi kèm header X-Lme-Signature bằng secret kênh LINE

Ảnh hưởng / rủi ro:
Chỉ màn 「Webhook転送」 (cả 2 tab) và job forward 2 kênh; cần test hồi quy tab L Message (xem/copy/再生成/lưu) và hợp đồng giải mã secret giữa web và job. Thứ tự phát hành: migration → web → backfill → job; FA-051 chưa lên production nên nên đi cùng đợt.
```

**Journal #151739 — Dev Studio — 2026-11-06:**

```
Dev handoff — 06/11 09:48 · nhánh ai_studio_implement_44381

Tóm tắt:
Màn 「Webhook転送」 nay có khối 「署名シークレット」 ở cả tab 「LINE公式アカウントデータ転送」, mỗi kênh một secret riêng; job forward kênh LINE gửi kèm header X-Lme-Signature (giá trị = secret kênh LINE, giống cách kênh L Message đang làm). Khi test chú ý nhất: 再生成/xem/copy ở tab nào chỉ được đụng secret của tab đó, tab L Message phải giữ nguyên hành vi. Deploy bắt buộc đúng thứ tự migration → web → backfill → job; job lên trước migration sẽ làm dừng forward cả 2 kênh.

Nội dung thay đổi:
- Màn Webhook転送, tab LINE: thêm khối 「署名シークレット」 (mask whsec_…, nút mắt, copy, 「再生成」 có confirm, ghi chú X-Lme-Signature), luôn hiện và nút luôn bật kể cả khi 転送の状態 tắt.
- Mỗi kênh một secret: 「再生成」 tab LINE không đổi secret tab L Message và ngược lại; đổi tab thì ô secret trở về dạng mask.
- Bot đã cấu hình trước release: secret kênh LINE tự sinh khi mở màn hoặc khi bấm xem/copy; secret L Message đang có không đổi.
- API EP-03 (再生成) và EP-05 (xem secret) bắt buộc tham số channel = 1 hoặc 2, thiếu/sai trả 422 「エラーが発生しました。」; EP-01 trả thêm secret mask của kênh LINE; 保存 lần đầu sinh secret cho cả 2 kênh.
- Lệnh mới php artisan webhook-relay:backfill-line-secret [--dry-run] [--chunk=500] sinh secret kênh LINE cho bot cũ (chạy tay một lần, lỗi thì báo Chatwork và exit 1).
- Job forward kênh LINE (lần gửi đầu và retry lần 2, 3) gắn X-Lme-Signature bằng secret kênh LINE; không ký được thì vẫn gửi không header, log WARN và báo Chatwork tối đa 1 lần/giờ/bot.
- Job khởi động thiếu LARAVEL_APP_KEY: log lỗi + Chatwork cho kênh LINE (như kênh L Message), job vẫn chạy.

Đánh giá ảnh hưởng — Rủi ro trung bình: Thay đổi 2 module có ràng buộc thứ tự deploy (job phụ thuộc cột mới của web) và chạm luồng secret dùng chung với tab L Message đang chạy; logic đã soát và harness chữ ký đạt nhưng chưa verify runtime.
- Tab L Message của màn Webhook転送: dùng chung service, khối giao diện và state (đã đổi sang theo kênh) ⇒ test lại xem/copy/再生成/保存.
- EP-02 保存: nhánh tạo row nay sinh 2 secret; response trả mask secret của kênh vừa lưu.
- Job forward kênh L Message (HandleForwardLmeEventTask dùng hàm 1 tham số) và retry kênh L Message: header vẫn phải lấy từ signing_secret.
- Entity job WebhookRelaySetting map cột line_signing_secret ⇒ cache setting (findAll, reload 60s) phụ thuộc migration; thiếu cột thì cả 2 kênh dừng forward.
- Endpoint debug /api/webhook-decode (chỉ khi APP_DEBUG) vẫn chỉ tra secret kênh L Message — không dùng được để kiểm secret kênh LINE.
- Trình duyệt còn JS cũ (cache) gọi EP-03/EP-05 không channel ⇒ 422 cho tới khi nạp JS mới.

Migration / thay đổi dữ liệu:
- [Schema · Trước deploy] Thêm cột line_signing_secret varchar(1024) NULL và line_secret_generated_at datetime NULL vào webhook_relay_setting (module web) — database/migrations/2026_10_30_000000_add_line_signing_secret_to_webhook_relay_setting.php: php artisan migrate --force
- [Dữ liệu · Khi deploy] Sinh secret kênh LINE (line_signing_secret) cho các bot đã có cấu hình Webhook転送 trước release (module web) — app/Console/Commands/BackfillWebhookRelayLineSecret.php: php artisan webhook-relay:backfill-line-secret --dry-run / php artisan webhook-relay:backfill-line-secret — không rollback được, backup: Không ghi đè dữ liệu cũ (chỉ ghi cột đang NULL/rỗng). Tuỳ chọn trước khi chạy: mysqldump <db> webhook_relay_setting > webhook_relay_setting_before_44381.sql

Lưu ý khi deploy:
- Thứ tự bắt buộc: chạy migration → deploy web → chạy lệnh backfill → deploy job (linect-service).
- Đổi config('sns-line.version') khi deploy web để trình duyệt nạp webhook-relay.js mới (JS cũ gọi EP-03/EP-05 thiếu channel sẽ bị 422).
- Secret sau 「再生成」 có hiệu lực ở job trong tối đa ~60 giây (cache setting), giống kênh L Message.
- Bỏ qua backfill thì job log WARN mỗi event của bot chưa có secret LINE và gửi không header.
- CS/BA cập nhật trang 「使い方を見る」 cho kênh LINE.

Việc cần người làm thêm (ngoài phạm vi task):
- Tài liệu docs/api/webhook-relay-outbound-contract.md (web) và spec-features FA-051 đang ghi X-Lme-Signature là HMAC trong khi job kênh LME gửi secret thô — người phụ trách spec cần thống nhất lại mô tả.
- CS/BA sửa trang 「使い方を見る」 (lme.jp/manual/api_webhook/) mục 'kênh LINE không ký' thành hướng dẫn kiểm header cho cả 2 kênh trước khi bật tính năng.
- Có thể đóng REQ-003 trong sprint 44381: nơi gọi API xem/tạo lại secret chỉ là webhook-relay.js; nơi gọi WebhookSignatureHelper là HandleForwardLmeEventTask, HandleRetryWebhookRelayTask (và manager kênh LME).
- Sửa docs/api/webhook-relay-outbound-contract.md §4.1 và bảng §4 cho khớp job: X-Lme-Signature là secret thô (không HMAC) và kênh 1 cũng có X-Lme-Timestamp.
- Đội build kiểm build.gradle của linect-service: RequestHelper dùng retrofit2 converter-jackson nhưng dependency không được khai (compile sạch trên base đang lỗi).
- Cân nhắc thêm Feature test PHPUnit cho WebhookRelayService (lazy-fill secret theo kênh, backfill idempotent) khi có DB test.
- Nếu muốn chuyển X-Lme-Signature sang HMAC thật cho cả 2 kênh: mở ticket riêng (đổi cả web contract và job).

Điểm cần test: (xem đầy đủ trong journal gốc trên Redmine #44381 — đã được gộp vào "Điểm cần test" của vòng cuối #153437 bên dưới)

Branch: ai_studio_implement_44381
- sns-line: ai_studio_implement_44381 (nhánh gốc release_step_20260930_v2 @303a131b9c03, commit 3ba833911c418792210f7590eca8ff4d80b1cd0c)
- linect-service: ai_studio_implement_44381 (nhánh gốc release-t09-2026 @be6ef546aedb, commit 15202447093a6765e63aeacdd04b8bdfa8787718)
```

**Journal #153270 — Dev Studio — 2026-11-09:**

```
Dev Studio · Kế hoạch chia task con

Kế hoạch v2 thêm bug #5141 vào T1. Khi hai request mở màn cùng lúc trên bot chưa có dòng cấu hình, cả hai cùng khoá rồi cùng chèn dòng nên MySQL báo deadlock. Code chỉ bắt lỗi trùng khoá nên trả 500. Cách sửa: tạo dòng trước rồi mới khoá để lấp secret, có thử lại tối đa 3 lần khi gặp deadlock, áp cho mở màn, lưu lần đầu và 再生成. Các phần đã chốt giữ nguyên: 再生成 khi chưa có dòng, test web, đọc secret LINE mới nhất ở job, và HMAC cho cả 2 kênh. Kế hoạch sẵn sàng để chốt.

Ảnh hưởng / rủi ro:
Phần web đổi thứ tự tạo dòng và khoá ở các đường tạo cấu hình lần đầu (mở màn, lưu lần đầu, 再生成, xem secret), cần test lại khi gọi song song. Phần job đổi header của cả hai kênh sang HMAC và thêm một truy vấn theo khoá UNIQUE cho mỗi request kênh LINE. Tool khách đang so header với secret ở kênh L Message sẽ hết khớp khi deploy.
```

**Journal #153313 — Dev Studio — 2026-11-09:**

```
Dev handoff — 09/11 14:32 · nhánh ai_studio_implement_44381

Tóm tắt:
Màn 「Webhook転送」 có secret riêng cho từng kênh. Job forward webhook gửi X-Lme-Signature là HMAC-SHA256 (hex thường, 64 ký tự) của đúng body gửi đi, cho cả kênh LINE và kênh L Message, ở lần đầu và khi retry. Vòng này sửa 「再生成」 khi bot chưa có cấu hình (nay trả 200) và lỗi 500 khi mở màn đồng thời, kèm test PHPUnit phía web. Khi test, chú ý nhất: HMAC(body nhận được, secret trên màn) phải khớp header ở cả 2 kênh; kênh L Message đổi hành vi so với bản đang chạy; sau 「再生成」 có thể trễ tới 60 giây.

Nội dung thay đổi:
- Màn 「Webhook転送」 tab 「LINE公式アカウントデータ転送」: khối 「署名シークレット」 riêng (xem/copy/再生成), độc lập với tab L Message.
- API 「再生成」 (POST /admin/webhook-relay/regenerate-secret): bot chưa có cấu hình ⇒ tạo cấu hình kèm secret 2 kênh rồi sinh lại kênh được chọn, trả 200 + secret_masked (trước đây 422).
- API mở màn (GET /admin/webhook-relay/config) và lưu lần đầu (POST /admin/webhook-relay/save): request đồng thời trên bot chưa có cấu hình đều trả 200, cùng secret mỗi kênh, DB chỉ 1 dòng.
- 5 API JSON của màn: lỗi ngoài dự kiến trả 500 INTERNAL_ERROR (log + Chatwork, không lộ SQL/secret); Staff thiếu quyền nhận 403 JSON thay vì bị chuyển trang.
- Nút 「保存する」 gặp lỗi server/mạng: hiện toast 「エラーが発生しました。」.
- Lệnh php artisan webhook-relay:backfill-line-secret [--dry-run]: sinh secret kênh LINE cho bot cấu hình trước release, chạy lại không ghi đè.
- Job forward kênh LINE và kênh L Message (lần gửi đầu): X-Lme-Signature = HMAC-SHA256(body, secret của tab tương ứng).
- Job retry webhook (cả 2 kênh): ký lại HMAC trên body dựng lại bằng secret của kênh.
- Log lỗi khi endpoint trả lỗi: che chữ ký và chuỗi whsec_…, tối đa 200 ký tự; kênh LINE không ký được vẫn gửi không header, cảnh báo tối đa 1 lần/bot/giờ.
- Tài liệu hợp đồng gửi ra ngoài: HMAC cho 2 kênh, X-Lme-Timestamp cho 2 kênh, secret mới có hiệu lực trễ ≤60s.

Bug QA con:
- #45605 đã sửa (commit sns-line@88a795fb143d): Tạo dòng cấu hình (kèm 2 secret) ngoài transaction trước, chỉ khoá dòng đã có; deadlock 1213/trùng khoá 1062 thì thử lại tối đa 3 lần. Hai request mở màn đồng thời đều trả 200, cùng secret, DB 1 dòng.
- #45606 đã sửa (commit sns-line@88a795fb143d): 「再生成」 khi bot chưa có cấu hình: tạo dòng kèm secret 2 kênh rồi sinh lại kênh được chọn, trả 200 + secret_masked thay vì 422 (theo technical-spec EP-03 bước 4).
- #45607 không đổi code: ngày 09/11 Tu (người phụ trách) chọn giữ độ trễ ≤60s như kênh L Message (job cache cấu hình 60s); tài liệu hợp đồng đã ghi. Cần người phụ trách Reject bug và BA cập nhật BR-C01-4/CON-T1 và TC NEW-48.

Bug automation Test Studio:
- Bug #5102 đã sửa (commit sns-line@88a795fb143d): EP-03 khi bot chưa có dòng: tạo dòng kèm 2 secret rồi sinh lại kênh yêu cầu, trả 200 + secret_masked.
- Bug #5103 không phải bug: Theo quyết định ngày 09/11 của Tu (người phụ trách), phương án B: kênh LINE giữ cache cấu hình 60s như kênh L Message, chấp nhận trễ ≤60s sau 「再生成」. Tài liệu hợp đồng (docs/api/webhook-relay-outbound-contract.md mục 3) đã ghi; spec/TC cần cập nhật theo.
- Bug #5141 đã sửa (commit sns-line@88a795fb143d): Tạo dòng trước rồi mới khoá dòng đã có (không còn gap lock), retry 1213/1062 tối đa 3 lần; test PHPUnit phủ 1213 và 1062.

Đánh giá ảnh hưởng — Rủi ro trung bình: Logic web có test và đột biến, chữ ký có harness độc lập; nhưng hợp đồng kênh L Message đang chạy bị đổi, cần deploy đúng thứ tự web → job, và chưa verify runtime với MySQL/job thật.
- Tab 「L Messageデータ転送」: dùng chung service/API với tab LINE — mở màn, lưu, xem/copy/再生成 secret LME không được đổi secret kênh LINE và ngược lại.
- Danh sách 「転送エラー」 và 「最新に更新」 (EP-04): có thể tạo dòng cấu hình không secret; mở màn sau đó phải bổ sung đủ secret 2 kênh.
- Middleware AdminAccess (dùng chung): Staff bot mời thiếu quyền gọi route có cờ json_api (5 route Webhook転送 và 3 route ajax.monthlyBill.* của màn 月次決済) nhận 403 JSON thay vì chuyển về trang chủ; route khác không đổi.
- Job forward kênh L Message và job retry: đổi giá trị header của kênh đang chạy production — bên nhận so secret thô sẽ thấy sai.
- Bảng webhook_relay_setting thêm 2 cột; entity job đọc cột mới ⇒ job lên trước migration sẽ không nạp được cấu hình và ngừng forward cả 2 kênh.
- Module callback có bản sao code forward nhưng không khởi động các manager này ⇒ không bị ảnh hưởng.

Migration / thay đổi dữ liệu:
- [Schema · Trước deploy] Thêm cột line_signing_secret varchar(1024) NULL và line_secret_generated_at datetime NULL vào webhook_relay_setting — database/migrations/2026_10_30_000000_add_line_signing_secret_to_webhook_relay_setting.php: php artisan migrate --force
- [Dữ liệu · Khi deploy] Sinh secret kênh LINE cho các bot đã cấu hình Webhook転送 trước release: php artisan webhook-relay:backfill-line-secret --dry-run / php artisan webhook-relay:backfill-line-secret
- [Thao tác tay · Trước deploy] CS báo khách kênh L Message và sửa trang 「使い方を見る」: X-Lme-Signature đổi sang HMAC-SHA256 của body: 1. CS gửi thông báo cho khách đang tích hợp kênh L Message về cách verify mới (lowercase hex HMAC-SHA256(body thô, secret)). 2. BA/CS sửa trang 「使い方を見る」 theo docs/api/webhook-relay-outbound-contract.md mục 4.1. — không rollback được, backup: Không có dữ liệu bị ghi; lưu bản trang 「使い方を見る」 cũ trước khi sửa.

Lưu ý khi deploy:
- Thứ tự: migration → deploy web → chạy backfill → deploy job. Job lên trước migration sẽ dừng forward cả 2 kênh.
- Trước khi deploy job: CS báo khách đang dùng kênh L Message và sửa trang 「使い方を見る」 (header đổi từ secret thô sang HMAC).
- Đội release đổi config('sns-line.version') để trình duyệt nạp webhook-relay.js mới (agent không tự bump).
- Không phát hành tài liệu hợp đồng cho khách trước khi job HMAC lên.

Việc cần người làm thêm (ngoài phạm vi task):
- Trước khi deploy job: CS/BA báo các khách đã tích hợp kênh L Message rằng X-Lme-Signature đổi từ secret thô sang chữ ký HMAC, và cập nhật trang 「使い方を見る」 cách kiểm chữ ký cho cả 2 kênh.
- Người phụ trách spec ghi vào spec FA-051 rằng quyết định dùng secret thô của #40475 / #40543 đã được thay bằng HMAC (HieuTM, 06/11).
- BA cập nhật spec #44381 (BR-C01-4, CON-T1) và TC NEW-48 theo quyết định Tu 09/11: secret mới có hiệu lực trễ tối đa 60 giây cho cả 2 kênh; người phụ trách chốt đề xuất sửa F-6/I-2 của kế hoạch cha.
- CS báo khách đang tích hợp kênh L Message và sửa trang 「使い方を見る」: X-Lme-Signature đổi từ secret thô sang HMAC-SHA256 của body, trước khi deploy job.
- Đội build bổ sung converter-jackson vào build.gradle của linect-service (compileJava lỗi sẵn từ base).

Branch: ai_studio_implement_44381
- sns-line: ai_studio_implement_44381 (nhánh gốc release_step_20260930_v2 @303a131b9c03, commit 6c2b2ccb881274da1030e97863c660dce41ae534)
- linect-service: ai_studio_implement_44381 (nhánh gốc release-t09-2026 @be6ef546aedb, commit 0b8e7b69462363dd22933f82590aeae332186bad)
```

**Journal #153396 — Dev Studio — 2026-11-09:**

```
Dev Studio · Kế hoạch chia task con

Kế hoạch v3 mở lại T2 (job) để sửa bug #5455: hiện cảnh báo gửi không chữ ký ở kênh LINE bị chặn 1 lần/bot/giờ, trong khi spec yêu cầu mỗi lần gửi không ký đều có log WARN kèm bot, kênh và lý do. Cách sửa: log WARN ở mọi lần gửi và retry, chỉ tin Chatwork còn chặn lặp 1 tin/bot/giờ để không spam. Kế hoạch cũng cập nhật theo quyết định của Tu ngày 09/11: kênh LINE chấp nhận trễ tối đa 60s sau 「再生成」, phần này không đổi code. T1 (web) không phải làm lại.

Ảnh hưởng / rủi ro:
Chỉ đổi cách ghi log/Chatwork khi job gửi kênh LINE mà không có chữ ký; header, body, retry và web không đổi. Rủi ro: bot lỗi kéo dài sinh thêm 1 dòng WARN cho mỗi event, tức log tăng tối đa gấp đôi và chỉ khi đang lỗi.
```

**Journal #153437 — Dev Studio — 2026-11-09 (vòng cuối — bám theo vòng này khi viết/review TC):**

```
Dev handoff — 09/11 17:25 · nhánh ai_studio_implement_44381

Tóm tắt:
Màn 「Webhook転送」 có secret riêng cho từng kênh. Job forward webhook gửi X-Lme-Signature là HMAC-SHA256 (hex thường, 64 ký tự) của đúng body gửi đi, cho cả kênh LINE và kênh L Message, ở lần đầu và khi retry. Vòng này: kênh LINE không ký được thì mỗi lần gửi/retry đều có log WARN kèm bot và lý do; Chatwork vẫn chỉ 1 tin/bot/giờ. Khi test, chú ý nhất: HMAC(body nhận được, secret trên màn) phải khớp header ở cả 2 kênh; kênh L Message đổi hành vi so với bản đang chạy; sau 「再生成」 có thể trễ tới 60 giây.

Nội dung thay đổi:
- Màn 「Webhook転送」 tab 「LINE公式アカウントデータ転送」: khối 「署名シークレット」 riêng (xem/copy/再生成), độc lập với tab L Message.
- API 「再生成」 (POST /admin/webhook-relay/regenerate-secret): bot chưa có cấu hình ⇒ tạo cấu hình kèm secret 2 kênh rồi sinh lại kênh được chọn, trả 200 + secret_masked.
- API mở màn (GET /admin/webhook-relay/config) và lưu lần đầu: request đồng thời trên bot chưa có cấu hình đều trả 200, cùng secret mỗi kênh, DB 1 dòng.
- 5 API JSON của màn: lỗi ngoài dự kiến trả 500 INTERNAL_ERROR (log + Chatwork, không lộ SQL/secret); Staff thiếu quyền nhận 403 JSON thay vì bị chuyển trang.
- Nút 「保存する」 gặp lỗi server/mạng: hiện toast 「エラーが発生しました。」.
- Lệnh php artisan webhook-relay:backfill-line-secret [--dry-run]: sinh secret kênh LINE cho bot cấu hình trước release, chạy lại không ghi đè.
- Job forward kênh LINE, kênh L Message (lần đầu) và job retry (cả 2 kênh): X-Lme-Signature = HMAC-SHA256(body, secret của tab tương ứng).
- Job kênh LINE không ký được (chưa có secret, giải mã lỗi, thiếu APP_KEY): vẫn gửi không header; mỗi lần gửi/retry có 1 dòng WARN kèm bot, kênh, lý do; Chatwork tối đa 1 tin/bot/giờ, thiếu APP_KEY thì không Chatwork theo bot.
- Log lỗi khi endpoint trả lỗi: che chữ ký và chuỗi whsec_…, tối đa 200 ký tự.
- Tài liệu hợp đồng gửi ra ngoài: HMAC cho 2 kênh, X-Lme-Timestamp cho 2 kênh, secret mới có hiệu lực trễ ≤60s.

Bug automation Test Studio:
- Bug #5455 đã sửa (commit linect-service@b7b30713aa18): Kênh LINE gửi không ký: mỗi lần gửi đầu và mỗi lần retry đều ghi WARN kèm bot, kênh LINE và lý do; bộ chặn 1 giờ/bot nay chỉ áp cho tin Chatwork (thiếu APP_KEY thì không Chatwork theo bot).

Đánh giá ảnh hưởng — Rủi ro trung bình: Vòng này chỉ đổi cách ghi log/Chatwork khi không ký được; nhưng cả gói đổi hợp đồng kênh L Message đang chạy, cần deploy đúng thứ tự web → job và chưa verify runtime với job/MySQL thật.
- Tab 「L Messageデータ転送」: dùng chung service/API với tab LINE — thao tác secret ở một tab không được đổi secret tab kia.
- Danh sách 「転送エラー」 và 「最新に更新」: có thể tạo dòng cấu hình không secret; mở màn sau đó phải bổ sung đủ secret 2 kênh.
- Middleware AdminAccess (dùng chung): Staff bot mời thiếu quyền gọi route có cờ json_api (5 route Webhook転送, 3 route ajax.monthlyBill.* của màn 月次決済) nhận 403 JSON thay vì chuyển về trang chủ.
- Job forward kênh L Message và job retry: đổi giá trị header của kênh đang chạy production — bên nhận so secret thô sẽ thấy sai.
- Log job forward kênh LINE: bot thiếu secret hoặc APP_KEY lệch sinh 1 WARN cho mỗi event (trước đây 1 WARN/bot/giờ) — theo dõi dung lượng log nếu chưa backfill.
- Bảng webhook_relay_setting thêm 2 cột; entity job đọc cột mới ⇒ job lên trước migration sẽ ngừng forward cả 2 kênh.
- Module callback có bản sao code forward nhưng không khởi động các manager này ⇒ không bị ảnh hưởng.

Migration / thay đổi dữ liệu:
- [Schema · Trước deploy] Thêm cột line_signing_secret varchar(1024) NULL và line_secret_generated_at datetime NULL vào webhook_relay_setting — database/migrations/2026_10_30_000000_add_line_signing_secret_to_webhook_relay_setting.php: php artisan migrate --force
- [Dữ liệu · Khi deploy] Sinh secret kênh LINE cho các bot đã cấu hình Webhook転送 trước release: php artisan webhook-relay:backfill-line-secret --dry-run / php artisan webhook-relay:backfill-line-secret
- [Thao tác tay · Trước deploy] CS báo khách kênh L Message và sửa trang 「使い方を見る」: X-Lme-Signature đổi sang HMAC-SHA256 của body — không rollback được, backup: Không có dữ liệu bị ghi; lưu bản trang 「使い方を見る」 cũ trước khi sửa.

Lưu ý khi deploy:
- Thứ tự: migration → deploy web → chạy backfill → deploy job. Job lên trước migration sẽ dừng forward cả 2 kênh; bỏ backfill thì mỗi event kênh LINE của bot thiếu secret sinh 1 WARN.
- Trước khi deploy job: CS báo khách đang dùng kênh L Message và sửa trang 「使い方を見る」 (header đổi từ secret thô sang HMAC).
- Đội release đổi config('sns-line.version') để trình duyệt nạp webhook-relay.js mới (agent không tự bump).
- Không phát hành tài liệu hợp đồng cho khách trước khi job HMAC lên.

Việc cần người làm thêm (ngoài phạm vi task):
- Cập nhật technical-spec #44381 (job bước 1, CON-T1) và testcase liên quan theo quyết định trễ ≤60s của Tu (09/11).
- Báo khách/CS và sửa trang 「使い方を見る」 trước khi deploy job, vì kênh L Message đổi từ secret thô sang HMAC (việc còn treo từ v2).
- BA cập nhật spec #44381 (BR-C01-4, CON-T1) và TC NEW-48 theo quyết định Tu 09/11: secret mới có hiệu lực trễ tối đa 60 giây cho cả 2 kênh.
- CS báo khách đang tích hợp kênh L Message và sửa trang 「使い方を見る」: X-Lme-Signature đổi từ secret thô sang HMAC-SHA256 của body, trước khi deploy job.
- Đội build bổ sung converter-jackson vào build.gradle của linect-service (compileJava lỗi sẵn từ base).

Điểm cần test:
- AC-13: bot chưa có secret kênh LINE, gửi 2 event cách nhau vài giây ⇒ 2 request không header, 2 dòng WARN có bot + lý do "chưa có secret kênh LINE", chỉ 1 tin Chatwork
- AC-13b: secret giải mã lỗi ⇒ WARN mỗi lần gửi/retry lý do "giải mã lỗi"; ERROR giải mã 1 lần/ciphertext; Chatwork 1 tin/bot/giờ
- Retry không ký cũng có WARN
- Thiếu LARAVEL_APP_KEY ⇒ WARN mỗi lần, không Chatwork theo bot
- Request có ký không sinh WARN; kênh LME không đổi hành vi
- AC-8 sửa: sau 「再生成」 tab LINE, trong ≤60s lần gửi/retry ký bằng secret mới
- Bot bật forward LINE nhưng chưa có secret kênh LINE: gửi 2 event cách nhau vài giây ⇒ 2 request không header, log job có 2 dòng WARN '#reportLineUnsigned … - bot <id> - channel LINE … chưa có secret kênh LINE', chỉ 1 tin Chatwork.
- Lô retry kênh LINE của bot thiếu secret: mỗi lần retry có thêm WARN kèm bot và lý do; không có tin Chatwork thứ hai trong 1 giờ.
- Secret LINE giải mã lỗi (ciphertext hỏng/APP_KEY lệch): mỗi lần gửi có WARN lý do 'giải mã lỗi', ERROR giải mã chỉ 1 lần, Chatwork 1 tin/bot/giờ.
- Bot có secret LINE hợp lệ: request có X-Lme-Signature = HMAC-SHA256(body, secret tab LINE), không có WARN #reportLineUnsigned.
- Kênh L Message: header = HMAC-SHA256(payload, secret tab L Message), lần đầu và retry; không có thay đổi log ở vòng này.
- Hồi quy web: 再生成 khi bot chưa có cấu hình trả 200; 2 request mở màn đồng thời đều 200, DB 1 dòng; backfill chạy 2 lần lần 2 không ghi.

Branch: ai_studio_implement_44381
- sns-line: ai_studio_implement_44381 (nhánh gốc release_step_20260930_v2 @303a131b9c03, commit 6c2b2ccb881274da1030e97863c660dce41ae534)
- linect-service: ai_studio_implement_44381 (nhánh gốc release-t09-2026 @be6ef546aedb, commit b7b30713aa1880aa43e5c8964c6521a26f5fa2cd)
```
