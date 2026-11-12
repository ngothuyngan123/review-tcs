# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #44780 qua `/new-task` (REST API, `scripts/redmine_fetch.py`).
> ⚠️ Issue Redmine **không có mục "Tái hiện bug"** riêng — tracker `SpecImprove`, đây là task hardening phía Dev (phát hiện/mở rộng từ nội bộ, không phải report của khách hàng cụ thể). Toàn bộ nội dung điều tra + thay đổi nằm trong 6 journal "Dev Studio" (quy trình bàn giao AI dev, 2026-10-30 → 2026-11-05), chép nguyên văn ở cuối file này.
> ⚠️ **Liên quan ticket #44660** (`tasks/2026-11-03_44660_forward-callback-chan-webhook-lme/`) — #44660 xử lý chặn **phía WEB** (validate khi LƯU cấu hình Webhook転送), #44780 xử lý chặn **phía JOB** (khi FORWARD request thật — `HandleForwardCallbackEventTask` / `HandleRetryWebhookRelayTask`, java-job). 2 ticket cùng tính năng gốc `Webhook転送`/forward webhook (#40475), nên khi viết/review TC cần đối chiếu 2 folder để tránh trùng + đảm bảo đủ 2 lớp (web chặn lưu + job chặn forward).

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44780 — [JOB] Forward webhook chặn việc set chính webhook của LME vào url forward callback bên mình` |
| Module / Màn hình | Job forward webhook Kênh 1 (`HandleForwardCallbackEventTask` — 「LINE公式アカウントデータ転送」) + job thử lại (`HandleRetryWebhookRelayTask`); gián tiếp chạm Kênh 2 (`HandleForwardLmeEventTask` — 「L Messageデータ転送」) qua client HTTP dùng chung (java-job, không phải màn web) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- issue.description gốc đã là tiếng Việt kỹ thuật, giữ nguyên văn (không tóm tắt). -->

`HandleForwardCallbackEventTask`
- `DOMAIN_ENDPOINT_WEBHOOK` sửa default value cho đúng: `http://cb.lmes.jp`
- `String webhookUrl = ConfigFile.DOMAIN_ENDPOINT_WEBHOOK + "/line/callback/add/" + bot.getId();`
- Kiểm tra nếu `webhookUrl` tự forward chính bot đó thì chặn không forward và ignore

=> sửa chặn cả set webhook bot khác. Check nếu url webhook của bot khác thì cũng chặn.

(Yêu cầu mở rộng phạm vi — Journal #150917, Văn Dũng Đinh, 2026-11-03: "sửa chặn cả set webhook bot khác. check nếu url webhook của bot khác thì cũng chặn")

## Steps to reproduce

<!-- Không có section riêng trong Redmine — suy ra từ "Điểm cần test" ở các journal Dev Studio (bản cuối, #151096/#151281, commit d0c0b3fa3c077dbc4d6657e2bea9a698d376e0e0). -->

1. Bot A bật forward webhook Kênh 1 (「LINE公式アカウントデータ転送」), đặt URL forward là webhook LME của **chính bot A** hoặc của **bot B khác** (dạng `{DOMAIN_ENDPOINT_WEBHOOK hoặc HOST_SNSLINE}/line/callback/add/{id bất kỳ}`, kể cả biến thể `/index.php/...`, `./`, `..`, `\`, `//`, `%2F`, host viết hoa/có `.` cuối, có query, port).
2. Gửi tin LINE tới bot A để trigger callback event → job forward Kênh 1 chạy.
3. (Biến thể) Để event đang chờ retry (đích 3rd-party trả 5xx/timeout) rồi đổi URL forward sang webhook LME giữa chừng → job retry Kênh 1 chạy lại.
4. (Biến thể redirect) Đích forward (bên thứ 3 hoặc Kênh 2) trả HTTP 301/302/303/307/308 với `Location` trỏ về webhook LME.

## Expected result

- Case 1-3 (URL đích là webhook LME của chính bot hoặc bot khác, mọi biến thể path/host): event bị đánh **IGNORE** (`callback_event.status_sync = 4`), **không gửi HTTP**, không ghi `webhook_relay_error`, không tăng `consecutive_failure_count`. Áp dụng cho cả lần gửi đầu và các lần retry (Kênh 1).
- Case 4 (redirect 3xx): job **không tự đi theo `Location`** — ghi lỗi ngay với `http_status` = mã 3xx thật, `error_code = HTTP_ERROR`, không retry. Áp dụng cho **cả Kênh 1 và Kênh 2** (lần đầu + retry), vì dùng chung HTTP client.
- URL bên thứ ba hợp lệ (không phải webhook LME, không redirect 3xx) → forward/retry bình thường như cũ (`status_sync = 2` khi 2xx).
- Khi `config.properties` không khai `DOMAIN_ENDPOINT_WEBHOOK` → job dùng default mới `https://cb.lmes.jp` (trước đây sai là `cb.lme.jp`).

## Actual result

- **Trước fix (code nền #40475, chưa có vòng nào của #44780):** job forward nguyên body callback LINE tới mọi `endpoint_url` mà không kiểm URL đích → nếu khách đặt chính webhook LME (của chính bot hoặc bot khác) thì request quay lại callback LME, bị lưu thành `callback_event` mới rồi job lại forward tiếp → **vòng lặp**; từ khi web có #43730 (kiểm `X-Line-Signature`) thì mỗi event thành 1 lỗi 401 thay vì vòng lặp vô hạn, nhưng vẫn là hành vi sai.
- **Giữa các vòng fix** (xem journal), lần lượt phát sinh + đã vá các lỗi con:
  - Vòng 1 (#149861, chặn chính bot) → QA raise mở rộng yêu cầu chặn cả bot khác (Journal #150917).
  - Vòng 3 (#150929, 23be2526b) chặn thêm bot khác, nhưng **chưa tắt redirect ở HTTP client** → đích trả 301/302/303 bị OkHttp tự đi theo bằng GET rỗng, ghi **thành công sai** theo mã 200 của đích cuối, lách được chốt chặn URL nếu đích bên thứ 3 redirect về webhook LME → bug con **#45094** (Redmine) / **#4978** (Test Studio automation).
  - Vòng 4 (#151096, d0c0b3fa3c07) vá redirect + mở rộng chặn `/index.php/...` → bug con **#45099** (Redmine) / **#5018** (Test Studio automation) — xác nhận đã sửa, nhưng #45099 trên Redmine còn trạng thái `New` vì QA mới test ở bản code cũ (23be2526, trước khi vá redirect) nên hệ thống AI dev liên tục mở lại bản nháp (#151145, #151281) dù code không đổi từ v4.
- **Code cuối cùng** (tính tới 2026-11-05, không có commit mới sau d0c0b3fa3c07): đã cover đủ 2 yêu cầu gốc (chặn chính bot + bot khác) + 2 bug con redirect/`/index.php` nêu trên.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

(`Attachments (0)` — Redmine #44780 không có file đính kèm.)

## Ghi chú thêm của Leader

- Tracker `SpecImprove`, Status hiện tại `Đang fix` (tại thời điểm fetch 2026-11-10). Priority `Normal`.
- Tính năng forward webhook (`#40475`, release-t09-2026, 2026-09-04) **chưa deploy lên production** — toàn bộ job forward Kênh 1/Kênh 2 chỉ tồn tại ở nhánh `release-t09-2026` + nhánh fix `ai_studio_fixbug_44780`. Không có dữ liệu thật bị ảnh hưởng, không cần recover.
- Dev lưu ý khi deploy: nên deploy #44780 **cùng lúc hoặc sau** bản web có **#43730** (kiểm `X-Line-Signature`) — nếu deploy #44780 trước mà chưa có #43730, các URL forward lọt qua chốt chặn (host LME cũ ngoài config, dạng viết lệch chưa lường tới) có thể vẫn tạo vòng lặp thay vì chỉ ra lỗi 401.
- Dev đề xuất (ngoài phạm vi ticket này, cần ticket riêng — tham khảo thêm **#44660** đã mở riêng cho phần web):
  - Validate ở màn web 「Webhook転送」 để chặn/báo khách ngay khi nhập URL là webhook LME, thay vì job âm thầm IGNORE không ai biết → **đây chính là nội dung ticket #44660**.
  - Kênh 2 (`L Messageデータ転送`) hiện **không** bị áp rule chặn URL LME (chỉ Kênh 1) — Dev ghi nhận là rủi ro còn mở ("cân nhắc mở ticket riêng"), chưa có ticket.
  - Spec `Webhook転送` còn thiếu chuỗi thông báo tiếng Nhật riêng cho lỗi redirect 3xx trên màn 「転送エラー」 — hiện job dùng mã lỗi chung `HTTP_ERROR`.
  - Base nhánh `release-t09-2026` thiếu dependency `com.squareup.retrofit2:converter-jackson:2.3.0` nên `compileJava` lỗi — vấn đề build/release, ngoài phạm vi ticket.
- Bug con cần đối chiếu khi viết/review TC (không phải phạm vi test riêng của #44780, nhưng liên quan trực tiếp code đã sửa):
  - **#45094** (Redmine) / **#4978** (Test Studio) — regression `./`, `..`, `\` khi path chứa id chính bot → đã vá, giữ ở code cuối.
  - **#45099** (Redmine, còn `New` tại thời điểm fetch) / **#5018** (Test Studio, đã đạt) — redirect 301/302/303/307/308 không được tự đi theo → đã vá ở `d0c0b3fa3c077dbc4d6657e2bea9a698d376e0e0`; **Leader lưu ý: nếu còn test lại #45099, phải test trên code `d0c0b3fa3`, không phải `23be2526` (bản trước khi vá redirect)** — đây là nguyên nhân Dev bị hệ thống mở lại bản nháp nhiều lần dù code không đổi.

## Journal / note từ Redmine (nguyên văn)

**Journal #149840 — Dev Studio — 2026-10-30:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Worker forward Kênh 1 (HandleForwardCallbackEventTask) và job thử lại (HandleRetryWebhookRelayTask) gửi nguyên body callback LINE tới endpoint_url mà không kiểm tra URL đích. Nếu khách nhập chính webhook LME của bot (/line/callback/add/{botId}), request sẽ quay về callback của LME. Web hiện tại tự tính chữ ký nên lưu request này thành callback_event mới, rồi job lại forward tiếp, tạo vòng lặp. Khi web có #43730 thì mỗi event thành một lỗi 401. Ngoài ra, giá trị mặc định của DOMAIN_ENDPOINT_WEBHOOK trong ConfigFile là cb.lme.jp, khác với domain callback thật là cb.lmes.jp.

Hướng sửa:
- D-1 Sửa giá trị mặc định của DOMAIN_ENDPOINT_WEBHOOK thành https://cb.lmes.jp
- D-2 Thêm hàm nhận diện URL là webhook LME của chính bot
- D-3 Worker Kênh 1 bỏ qua (IGNORE) khi URL đích là webhook LME của chính bot
- D-4 Job thử lại Kênh 1 cũng bỏ qua URL trỏ về chính LME

Ảnh hưởng / rủi ro:
Chỉ thay đổi luồng forward webhook Kênh 1 (lần gửi đầu và lần thử lại); bot đặt URL bên thứ ba không bị ảnh hưởng. Giá trị mặc định mới chỉ có tác dụng khi config.properties không khai DOMAIN_ENDPOINT_WEBHOOK; khi đó ChangeBotJob và HandleCheckStatusConnectBotAndTool sẽ dùng cb.lmes.jp. Chỉ sửa ở nhánh job, không đụng module callback.
```

**Journal #149861 — Dev Studio — 2026-10-30:**

```
Dev handoff — 30/10 14:25 · nhánh ai_studio_fixbug_44780

Nguyên nhân:
Worker forward Kênh 1 (HandleForwardCallbackEventTask) và job thử lại (HandleRetryWebhookRelayTask) gửi nguyên body callback LINE tới endpoint_url mà không kiểm tra URL đích. Nếu khách nhập chính webhook LME của bot (/line/callback/add/{botId}), request sẽ quay về callback của LME. Web hiện tại tự tính chữ ký nên lưu request này thành callback_event mới, rồi job lại forward tiếp, tạo vòng lặp. Khi web có #43730 thì mỗi event thành một lỗi 401. Ngoài ra, giá trị mặc định của DOMAIN_ENDPOINT_WEBHOOK trong ConfigFile là cb.lme.jp, khác với domain callback thật là cb.lmes.jp.

Nội dung thay đổi:
- Job forward webhook Kênh 1: khi URL đích là {domain LME}/line/callback/add/{id của chính bot} thì event được đánh IGNORE, không gửi HTTP, không ghi lỗi, không tăng bộ đếm lỗi. Phép so bỏ qua http/https, / cuối, chữ hoa trong host, port và query; domain gồm domain callback và domain web.
- Job retry webhook Kênh 1: lần thử 2 và 3 kiểm lại URL hiện tại; nếu URL đã bị đổi thành webhook của chính bot thì cả queue lẫn event nguồn đều đánh IGNORE.
- Cấu hình job: khi config.properties không khai DOMAIN_ENDPOINT_WEBHOOK thì default là https://cb.lmes.jp (trước đây là https://cb.lme.jp).

File đã sửa (java-job):
  src/main/java/sns/line/ConfigFile.java             |  4 +-
  .../line/helper/WebhookRelaySettingManager.java    | 49 ++++++++++++++++++++++
  .../webhook/HandleForwardCallbackEventTask.java    |  8 ++++
  .../webhook/HandleRetryWebhookRelayTask.java       |  8 ++++
  4 files changed, 67 insertions(+), 2 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chốt chặn chỉ khớp đúng URL webhook của chính bot và không thêm query DB. Default config chỉ có tác dụng khi config.properties thiếu key.
- Forward Kênh 1 tới URL bên thứ ba: dùng chung hàm actionForward, cần kiểm vẫn forward, retry và ghi lỗi như cũ.
- Retry Kênh 2: dùng chung actionRetry; chốt chặn mới chỉ áp cho Kênh 1, cần kiểm Kênh 2 không đổi.
- ChangeBotJob (set/gỡ webhook LINE khi đổi kênh) và HandleCheckStatusConnectBotAndTool (kiểm trạng thái kết nối) đọc DOMAIN_ENDPOINT_WEBHOOK; hành vi chỉ đổi ở môi trường không khai key.
- Bảng callback_event.status_sync và webhook_relay_queue có thêm một trường hợp IGNORE mới, schema không đổi.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Tính năng forward webhook chỉ có từ release-t09-2026 (commit #40475 ngày 2026-09-04), nhánh này chưa deploy. DB điều tra không có bảng của tính năng nên chưa có dữ liệu nào bị ảnh hưởng.

Lưu ý khi deploy:
- Kiểm config.properties của job production có khai DOMAIN_ENDPOINT_WEBHOOK đúng https://cb.lmes.jp (không có / cuối); nếu không khai thì job sẽ dùng default mới.
- Nên deploy job forward (#40475 và ticket này) cùng lúc hoặc sau web có #43730 (kiểm X-Line-Signature), để các URL forward về LME khác (bot khác, URL viết lệch) không thành vòng lặp.

Việc cần người làm thêm (ngoài phạm vi task):
- Nên thêm validate ở màn web 「Webhook転送」 (php-web) để không cho lưu URL forward là webhook LME (/line/callback/add/...); làm ở một ticket riêng cho module web.
- Kênh 2 (L Messageデータ転送) cũng có thể bị đặt URL trỏ về webhook LME. Hiện việc này không gây vòng lặp nhưng sinh dữ liệu rác hoặc lỗi; cân nhắc mở ticket riêng.
- Base release-t09-2026 thiếu dependency com.squareup.retrofit2:converter-jackson:2.3.0 cho RequestHelper.java nên compileJava lỗi; đội release cần kiểm build.gradle hoặc libs của nhánh.
- Phía web: validate ở màn 「Webhook転送」, không cho lưu endpoint_url là URL webhook LME (/line/callback/add/...) để khách được báo ngay, thay vì event bị bỏ qua mà không ai biết.
- Cân nhắc chặn cả trường hợp forward sang webhook LME của bot khác (A→B, B→A có thể tạo vòng lặp khi web chưa có #43730).

Điểm cần test:
- URL forward là https://cb.lmes.jp/line/callback/add/{id của chính bot}: status_sync=4, không có HTTP request, không có row webhook_relay_error, có log IGNORE.
- Các biến thể http://, dấu / cuối, host viết hoa, có query, domain HOST_SNSLINE: đều bị IGNORE.
- URL webhook LME của bot khác và URL bên thứ ba hợp lệ: forward bình thường (status_sync=2).
- URL không parse được: giữ hành vi cũ (lỗi trả về từ API client).
- Có row Kênh 1 đang chờ thử lại rồi đổi URL thành webhook của chính bot: ở lần thử kế tiếp, queue thành IGNORE và nguồn có status_sync=4; thử lại Kênh 2 không đổi.
- config.properties không khai DOMAIN_ENDPOINT_WEBHOOK: giá trị dùng là https://cb.lmes.jp.
- Compile java-job thành công.
- Bot test bật 「LINE公式アカウントデータ転送」 với URL https://cb.lmes.jp/line/callback/add/{id chính bot}, gửi tin LINE: callback_event.status_sync=4, không có request forward, không có row webhook_relay_error, consecutive_failure_count không tăng, số callback_event không tăng liên tục.
- Các biến thể vẫn bị chặn: http://, có / cuối, host viết hoa, có ?query, có :443, URL trên domain web (HOST_SNSLINE).
- URL webhook LME của bot khác và URL bên thứ ba vẫn forward bình thường (status_sync=2).
- Retry: endpoint bên thứ ba trả 5xx để event vào webhook_relay_queue, sau đó đổi URL thành webhook của chính bot: lần thử tiếp theo queue thành IGNORE, event nguồn status_sync=4, không gửi.
- Kênh 2 (thông báo sự kiện LME) gửi và retry như cũ.
- Đổi kênh LINE của bot (ChangeBotJob) ở môi trường có khai DOMAIN_ENDPOINT_WEBHOOK: URL webhook set lên LINE giữ nguyên như trước.

Branch: ai_studio_fixbug_44780
- linect-service: ai_studio_fixbug_44780 (nhánh gốc release-t09-2026 @1690e2aab80c, commit e6db3513fa70d3e913d99a6d80125928b71d81b4)
```

**Journal #150917 — Văn Dũng Đinh — 2026-11-03:**

```
sửa chặn cả set webhook bot khác. check nếu url webhook của bot khác thì cũng chặn
```

**Journal #150929 — Dev Studio — 2026-11-03:**

```
Dev handoff — 03/11 19:24 · nhánh ai_studio_fixbug_44780

Nguyên nhân:
Yêu cầu được mở rộng: phải chặn mọi webhook LME chứ không chỉ webhook của chính bot. Hàm chốt chặn `WebhookRelaySettingManager.isLmeWebhookUrlOfBot` chỉ trả true khi id trong URL bằng id của bot đang forward (`isSameBotId`). Vì vậy khi bot A đặt URL là webhook LME của bot B, job vẫn forward event của A sang callback của B. Hậu quả: event bị ghi sai bot hoặc lỗi 401, và có thể lặp vòng A→B→A.

Nội dung thay đổi:
- Job forward webhook Kênh 1: URL đích trên domain LME (DOMAIN_ENDPOINT_WEBHOOK hoặc domain web HOST_SNSLINE) có path /line/callback/add/{đoạn bất kỳ} ⇒ event IGNORE, không gửi HTTP, không ghi lỗi, không tăng bộ đếm lỗi. Vòng 3 mở rộng chặn sang cả webhook của bot khác.
- Job retry webhook Kênh 1: lần thử lại kiểm lại URL hiện tại theo cùng quy tắc ⇒ queue và event nguồn IGNORE.
- Cấu hình job: khi config.properties không khai DOMAIN_ENDPOINT_WEBHOOK thì default là https://cb.lmes.jp (trước đây là https://cb.lme.jp).

Bug QA con:
- #45094 đã sửa (commit linect-service@46ca8ec8a804): Vòng 2 parse URL bằng OkHttp nên ./, .., \ được chuẩn hoá giống request thật trước khi so ⇒ IGNORE. Vòng 3 (23be2526b) giữ nguyên phần này và chặn thêm mọi id. Lượt QA trước test trên code vòng 1 (e6db3513).

Bug automation Test Studio:
- Bug #4978 đã sửa (commit linect-service@46ca8ec8a804): Chốt chặn parse URL bằng OkHttp (cùng thư viện gửi), nên ./, .., \, // và số 0 đầu id đều được nhận ra ⇒ IGNORE. Commit vòng 3 23be2526b giữ nguyên phần này; harness review v3 đạt các ca này.

File đã sửa (java-job):
  src/main/java/sns/line/ConfigFile.java             |  4 +-
  .../line/helper/WebhookRelaySettingManager.java    | 60 ++++++++++++++++++++++
  .../webhook/HandleForwardCallbackEventTask.java    |  9 ++++
  .../webhook/HandleRetryWebhookRelayTask.java       |  8 +++
  4 files changed, 79 insertions(+), 2 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ chặn khi host là domain LME và path đúng dạng webhook LME; không có trường hợp hợp lệ nào cần forward vào callback LME. Không thêm query DB, chỉ đổi hàm chốt chặn và 2 lối gửi Kênh 1.
- Forward Kênh 1 tới URL bên thứ ba (dùng chung actionForward): vẫn forward, retry và ghi lỗi như cũ.
- Retry Kênh 2 (dùng chung actionRetry): chốt chặn chỉ áp cho Kênh 1, Kênh 2 không đổi.
- ChangeBotJob (set/gỡ webhook LINE khi đổi kênh) và HandleCheckStatusConnectBotAndTool cùng đọc DOMAIN_ENDPOINT_WEBHOOK: chỉ đổi hành vi ở môi trường không khai key này.
- Bảng callback_event.status_sync và webhook_relay_queue: thêm trường hợp IGNORE mới, schema không đổi.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Tính năng forward webhook (#40475) chỉ có trên release-t09-2026, chưa deploy production, nên chưa có dữ liệu thật bị forward sai.

Lưu ý khi deploy:
- Kiểm config.properties của job production có khai DOMAIN_ENDPOINT_WEBHOOK = https://cb.lmes.jp; nếu không khai thì job dùng default mới.
- Nên deploy cùng lúc hoặc sau bản web có #43730 (kiểm X-Line-Signature), để các dạng còn lọt (/index.php/..., host LME cũ ngoài config) chỉ ra lỗi 401 chứ không thành vòng lặp.

Việc cần người làm thêm (ngoài phạm vi task):
- Nên thêm validate ở màn cài đặt forward trên web để báo khách ngay khi nhập URL webhook LME (job chỉ âm thầm IGNORE).
- Khi QA trên môi trường test: thử bot A trỏ webhook_relay_setting tới /line/callback/add/{bot B}, kiểm tra ra status_sync=4 và không có webhook_relay_error (chưa kiểm thử chạy thật trong container).
- Kiểm tra config prod DOMAIN_ENDPOINT_WEBHOOK/HOST_SNSLINE đúng domain LME thật, vì host cũ ngoài config (vd. cb.lme.jp) không được nhận diện.
- Bên web: validate URL Kênh 1 ở màn cài đặt, từ chối URL webhook LME để khách biết ngay thay vì event bị IGNORE âm thầm (module web, ngoài ticket này).
- Kiểm config.properties của job production có khai DOMAIN_ENDPOINT_WEBHOOK = https://cb.lmes.jp.

Điểm cần test:
- Bot A đặt URL = webhook LME của bot B ⇒ IGNORE (status_sync=4), không gửi HTTP, không ghi webhook_relay_error.
- Cũng IGNORE: /add/{A} (chính bot), /add/0, /add/{id không tồn tại}, /add/777abc, /add/+777, /add/0{B}; các dạng lệch của v2 (./, .., \, //, %2F, host viết hoa hoặc có . cuối, / cuối, query, port, http://) với id bot khác; host HOST_SNSLINE.
- Vẫn gửi bình thường: host khác (obs.test, cb.lmes.jp.evil.test, cb.lmes.jp@other.test), /line/callback/add/{B}/extra, /line/callback/add/ (thiếu id), /Line/Callback/Add/{B}, /line/callback/redirect-login.
- Retry Kênh 1 khi URL đã đổi sang webhook của bot khác ⇒ queue IGNORE, event nguồn status_sync=4; Kênh 2 không đổi.
- Compile java-job.
- Bot A đặt URL Kênh 1 = webhook LME của bot B (https://{DOMAIN_ENDPOINT_WEBHOOK}/line/callback/add/{B}) ⇒ event IGNORE (status_sync=4), không có request HTTP, không có webhook_relay_error.
- Các URL sau đều bị IGNORE: /add/{A}, /add/0, /add/999999999, /add/777abc, /add/+{B}, /add/0{B}; các dạng viết lệch ./, .., \, //, %2F, host viết hoa hoặc có . cuối, / cuối, query, port, http:// với id bot B; host HOST_SNSLINE.
- Các URL sau vẫn được gửi: URL bên thứ ba, cb.lmes.jp.evil.test, cb.lmes.jp@other.test, /add/{B}/extra, /add/ (thiếu id), /Line/Callback/Add/{B}, /line/callback/redirect-login.
- Retry Kênh 1: event đang chờ retry, đổi URL sang webhook bot khác ⇒ queue IGNORE và event nguồn status_sync=4. Retry Kênh 2 không đổi.
- Hồi quy #45094 / Test Studio #4978: 3 dạng ./, .., \ với id chính bot ⇒ IGNORE.
- config.properties không khai DOMAIN_ENDPOINT_WEBHOOK ⇒ job dùng default https://cb.lmes.jp.

Branch: ai_studio_fixbug_44780
- linect-service: ai_studio_fixbug_44780 (nhánh gốc release-t09-2026 @1690e2aab80c, commit 23be2526b2c63db789610ea222ed53c25f5137c8)
```

**Journal #151096 — Dev Studio — 2026-11-04:**

```
Dev handoff — 04/11 11:23 · nhánh ai_studio_fixbug_44780

Nguyên nhân:
Client OkHttp dùng chung của job forward (`WebhookRelayApiClient.CLIENT`) không tắt chế độ tự đi theo chuyển hướng. Với POST nhận 301/302/303, OkHttp tự gửi tiếp một GET rỗng tới Location rồi trả về mã 200 của đích cuối, nên job ghi thành công; spec thì quy định 3xx là thất bại và không đi theo redirect. Nhờ đó đích bên thứ ba có thể chuyển hướng về webhook LME mà lách được chốt chặn URL. Ngoài ra chốt chặn đòi path đúng 4 đoạn, nên dạng /index.php/line/callback/add/{id} (Laravel vẫn nhận) bị lọt.

Nội dung thay đổi:
- Job forward webhook Kênh 1 và Kênh 2 (lần đầu và retry): đích trả 301/302/303/307/308 ⇒ ghi lỗi ngay (http_status = mã 3xx, error_code=HTTP_ERROR), không đi theo Location, không retry. Trước đây 301/302/303 bị đi theo bằng GET và ghi thành công.
- Job forward Kênh 1: URL đích trên domain LME có path /line/callback/add/{đoạn bất kỳ} ⇒ event IGNORE, không gửi HTTP, không ghi lỗi. Áp cho webhook của mọi bot, kể cả khi URL bắt đầu bằng /index.php hoặc viết lệch (./, .., \, //, %2F, host viết hoa hay có . cuối).
- Job retry Kênh 1: kiểm lại URL hiện tại theo cùng quy tắc ⇒ queue và event nguồn IGNORE.
- Cấu hình job: khi config.properties không khai DOMAIN_ENDPOINT_WEBHOOK thì default là https://cb.lmes.jp (trước đây là https://cb.lme.jp).

Bug QA con:
- #45099 đã sửa (commit linect-service@d0c0b3fa3c07): Client forward tắt followRedirects/followSslRedirects. Nay 301/302 ghi lỗi HTTP_ERROR với đúng http_status, không gửi GET tới Location, không ghi thành công và không retry.

Bug automation Test Studio:
- Bug #5018 đã sửa (commit linect-service@d0c0b3fa3c07): Client forward không còn đi theo redirect: 301/302/303/307/308 đều ghi lỗi HTTP_ERROR với đúng mã HTTP và không retry. Harness review gọi client thật tới server cục bộ: server chỉ nhận 1 POST, không có GET tới Location.

File đã sửa (java-job):
  src/main/java/sns/line/ConfigFile.java             |  4 +-
  .../line/helper/WebhookRelaySettingManager.java    | 64 ++++++++++++++++++++++
  .../webhook/HandleForwardCallbackEventTask.java    |  9 +++
  .../webhook/HandleRetryWebhookRelayTask.java       |  8 +++
  .../threads/webhook/WebhookRelayApiClient.java     |  3 +
  5 files changed, 86 insertions(+), 2 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi client chỉ là tắt redirect theo đúng spec, và client này chỉ dùng cho tính năng forward chưa release. Chốt URL chỉ chặn rộng thêm đúng dạng /index.php trên domain LME. Không thêm query DB.
- Forward Kênh 2 (HandleForwardLmeEventTask) dùng chung client: không đi theo redirect nữa, đích trả 3xx thành lỗi hiện trên 「転送エラー」.
- Retry cả 2 kênh (HandleRetryWebhookRelayTask) dùng chung client: lần thử lại gặp 3xx thì ghi lỗi, không retry tiếp. Chốt URL LME chỉ áp cho Kênh 1.
- Forward Kênh 1 tới URL bên thứ ba trả 2xx: vẫn forward, retry và ghi lỗi như cũ.
- ChangeBotJob và HandleCheckStatusConnectBotAndTool đọc DOMAIN_ENDPOINT_WEBHOOK: chỉ đổi hành vi ở môi trường không khai key này.
- Bảng callback_event.status_sync, webhook_relay_queue, webhook_relay_error: có thêm trường hợp IGNORE và lỗi 3xx, schema không đổi.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Tính năng forward webhook (#40475) chưa release lên production, nên chưa có dữ liệu thật nào bị ghi thành công sai.

Lưu ý khi deploy:
- Kiểm config.properties của job production có khai DOMAIN_ENDPOINT_WEBHOOK = https://cb.lmes.jp; nếu không khai thì job dùng default mới.
- Nên deploy cùng lúc hoặc sau bản web có #43730 (kiểm X-Line-Signature), để host LME cũ ngoài config (vd. cb.lme.jp) nếu còn lọt thì chỉ ra lỗi 401.

Việc cần người làm thêm (ngoài phạm vi task):
- Spec 「Webhook転送」 cần chốt chuỗi tiếng Nhật cho lỗi chuyển hướng (3xx) trên màn 「転送エラー」; hiện job ghi mã chung HTTP_ERROR.
- Khi QA trên môi trường test: cho đích Kênh 1 và Kênh 2 trả 301/302, kiểm tra status_sync=3, có webhook_relay_error với đúng http_status và error_code=HTTP_ERROR, không có GET tới Location (chưa thử chạy thật trong container).
- Spec còn chờ chốt chuỗi lỗi riêng cho redirect; hiện 3xx dùng mã chung HTTP_ERROR — khi spec chốt thì cần ticket riêng nếu muốn mã/thông báo mới.
- Kiểm tra config prod DOMAIN_ENDPOINT_WEBHOOK/HOST_SNSLINE đúng domain LME thật, vì host cũ ngoài config (vd. cb.lme.jp) không được nhận diện.
- Bên web: validate URL Kênh 1 ở màn cài đặt, từ chối URL webhook LME để khách biết ngay thay vì event bị IGNORE âm thầm (module web, ngoài ticket này).
- Spec: chốt thông báo riêng cho lỗi chuyển hướng 3xx trên màn 「転送エラー」 (hiện dùng mã chung HTTP_ERROR).
- Kiểm config.properties của job production có khai DOMAIN_ENDPOINT_WEBHOOK = https://cb.lmes.jp.

Điểm cần test:
- Kênh 1, đích trả 301/302/303 (Location về webhook LME bot B hoặc host bất kỳ) ⇒ chỉ 1 POST, không có GET tới Location; status_sync=3, webhook_relay_error có http_status 301/302/303, error_code HTTP_ERROR, không retry.
- 307/308 vẫn báo lỗi như cũ; đích trả 2xx vẫn DONE.
- Kênh 2, đích trả 301/302 ⇒ ghi lỗi, không đi theo; đích trả 2xx vẫn thành công.
- Retry lần 2–3 (sau timeout/5xx) mà đích trả 302 ⇒ ghi lỗi, không đi theo.
- IGNORE, không gửi HTTP: {domain LME}/index.php/line/callback/add/{id}, kể cả khi kèm ./, //, / cuối hoặc id của bot khác.
- Vẫn gửi: /INDEX.PHP/line/callback/add/{id}, /index.php/line/callback/add/{id}/x, /foo/line/callback/add/{id}.
- Các ca của v1–v3 vẫn đạt; compile java-job.
- Kênh 1, đích trả 301/302/303 (Location về webhook LME bot B hoặc host bất kỳ): job chỉ gửi 1 POST, không có GET tới Location; status_sync=3, webhook_relay_error.http_status=301/302/303, error_code=HTTP_ERROR; không retry.
- 307/308: lỗi HTTP_ERROR như cũ. Đích trả 2xx: vẫn DONE. Đích trả 5xx hoặc timeout: vẫn retry lần 2–3.
- Kênh 2: đích trả 301/302 ⇒ lỗi, không đi theo redirect; đích 2xx vẫn thành công.
- Retry (lần 2–3 sau timeout/5xx) mà lần sau đích trả 302 ⇒ ghi lỗi, không đi theo.
- IGNORE (không gửi HTTP): https://{domain LME}/index.php/line/callback/add/{id}, kèm ./, //, / cuối, id bot khác, host HOST_SNSLINE.
- Vẫn gửi: /INDEX.PHP/line/callback/add/{id}, /index.php/line/callback/add/{id}/x, /foo/line/callback/add/{id}, /index.php/... trên host khác.
- Hồi quy v1–v3: webhook LME của chính bot và bot khác, các dạng ./, .., \ (#45094) ⇒ IGNORE.

Branch: ai_studio_fixbug_44780
- linect-service: ai_studio_fixbug_44780 (nhánh gốc release-t09-2026 @1690e2aab80c, commit d0c0b3fa3c077dbc4d6657e2bea9a698d376e0e0)
```

**Journal #151145 — Dev Studio — 2026-11-04:**

```
Dev handoff — 04/11 13:36 · nhánh ai_studio_fixbug_44780

Nguyên nhân:
Client forward WebhookRelayApiClient.CLIENT dùng mặc định của OkHttp là tự đi theo 301/302/303. Khi đó POST bị đổi thành GET rỗng gửi tới Location, và mã 200 của đích cuối được ghi thành thành công, trái spec (chỉ 2xx là thành công, không đi theo redirect). Lỗi có từ code nền #40475. Bản sửa đã có ở v4 (d0c0b3fa3), còn QA test trên 23be2526 là bản trước khi sửa.

Không có commit mới so với lần bàn giao trước (04/11 11:23): nhánh giữ nguyên commit đã bàn giao.

Nội dung thay đổi:
- Job forward Kênh 1 và Kênh 2 (lần đầu và retry): khi đích trả 301/302/303/307/308, job ghi lỗi với http_status là mã 3xx và error_code=HTTP_ERROR, không gửi request tới Location, không retry. Trước đây 301/302/303 bị đi theo bằng GET và được ghi thành công.
- Job forward Kênh 1: URL đích trên domain LME có path /line/callback/add/{đoạn bất kỳ} thì event bị IGNORE (status_sync=4), không gửi HTTP. Áp dụng cả cho dạng /index.php/..., ./, .., \, //, %2F, host viết hoa hoặc có dấu . cuối, và cho webhook của mọi bot.
- Job retry Kênh 1: kiểm lại URL hiện tại theo cùng quy tắc; nếu là webhook LME thì queue và event nguồn bị IGNORE.
- Cấu hình job: khi không khai DOMAIN_ENDPOINT_WEBHOOK, default là https://cb.lmes.jp (trước đây là https://cb.lme.jp).

Bug QA con:
- #45099 đã sửa (commit linect-service@d0c0b3fa3c07): Client forward đã tắt followRedirects/followSslRedirects. 301/302 nay ghi lỗi HTTP_ERROR với đúng http_status, không gửi GET tới Location và không ghi thành công. QA đã test trên 23be2526 là bản trước khi sửa, nhờ test lại trên d0c0b3fa3.

File đã sửa (java-job):
  src/main/java/sns/line/ConfigFile.java             |  4 +-
  .../line/helper/WebhookRelaySettingManager.java    | 64 ++++++++++++++++++++++
  .../webhook/HandleForwardCallbackEventTask.java    |  9 +++
  .../webhook/HandleRetryWebhookRelayTask.java       |  8 +++
  .../threads/webhook/WebhookRelayApiClient.java     |  3 +
  5 files changed, 86 insertions(+), 2 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Code không đổi so với vòng 4 đã được duyệt. Thay đổi ở client chỉ là tắt redirect theo spec, và client này chỉ dùng cho tính năng forward chưa release.
- Forward Kênh 2 (HandleForwardLmeEventTask) dùng chung client: 3xx nay thành lỗi và hiện trên 「転送エラー」.
- Retry của cả 2 kênh (HandleRetryWebhookRelayTask): 3xx ở lần thử lại được ghi lỗi, không retry tiếp. Chốt URL LME chỉ áp cho Kênh 1.
- Forward Kênh 1 tới URL bên thứ ba trả 2xx/5xx/timeout: forward, retry và ghi lỗi như cũ.
- ChangeBotJob và HandleCheckStatusConnectBotAndTool đọc DOMAIN_ENDPOINT_WEBHOOK: chỉ đổi hành vi ở môi trường không khai key này.
- Bảng callback_event.status_sync, webhook_relay_queue, webhook_relay_error: có thêm trường hợp IGNORE và lỗi 3xx, schema không đổi.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Tính năng forward (#40475) chưa phát hành lên production, chỉ mới test local, nên chưa có dữ liệu thật bị ghi sai.

Lưu ý khi deploy:
- Kiểm config.properties của job production có khai DOMAIN_ENDPOINT_WEBHOOK=https://cb.lmes.jp. Nếu không khai, job dùng default mới.
- Nên deploy cùng lúc hoặc sau bản web có #43730 (kiểm X-Line-Signature).

Việc cần người làm thêm (ngoài phạm vi task):
- QA/Test Studio chạy lại test redirect của #45099 trên job@d0c0b3fa3, rồi đóng ticket Redmine #45099 nếu đạt
- QA test lại #45099 trên job@d0c0b3fa3 (không phải 23be2526), gồm test hồi quy Kênh 2 và retry khi đích trả 3xx (giờ ghi lỗi HTTP_ERROR, đúng spec BR-15).
- Build gốc của nhánh base release-t09-2026 thiếu dependency converter-jackson nên compileJava đang lỗi; cần sửa riêng, ngoài ticket này.

Điểm cần test:
- Kênh 1, đích trả 301/302/303 với Location trỏ về /line/callback/add/{B}: Job chỉ gửi 1 POST, không có GET tới Location; status_sync=3, lỗi forward ghi đúng http_status với mã HTTP_ERROR, không retry
- 307/308 vẫn ghi lỗi HTTP_ERROR; đích trả 2xx vẫn ghi thành công (DONE)
- Kênh 2 và retry gặp 3xx: ghi lỗi, không đi theo redirect
- Kênh 1: đích trả 301/302, Location trỏ về /line/callback/add/{B}. Mong đợi: đích chỉ nhận 1 POST, không có GET tới Location; status_sync=3; webhook_relay_error có http_status 301/302 và error_code=HTTP_ERROR; không tạo queue retry. Test trên job d0c0b3fa3.
- 303/307/308 và 3xx không có Location: ghi lỗi HTTP_ERROR, không đi theo redirect.
- Đích trả 2xx: vẫn DONE (status_sync=2).
- Kênh 2 và retry gặp 3xx: ghi lỗi, không đi theo redirect.
- Kênh 1 với URL /line/callback/add/{id} hoặc /index.php/line/callback/add/{id} trên domain LME: IGNORE (status_sync=4), không gửi HTTP.

Branch: ai_studio_fixbug_44780
- linect-service: ai_studio_fixbug_44780 (nhánh gốc release-t09-2026 @1690e2aab80c, commit d0c0b3fa3c077dbc4d6657e2bea9a698d376e0e0)
```

**Journal #151281 — Dev Studio — 2026-11-05:**

```
Dev handoff — 05/11 11:09 · nhánh ai_studio_fixbug_44780

Nguyên nhân:
Client forward từng tự đi theo redirect 301/302/303 rồi ghi thành công theo mã 200 của đích cuối. Lỗi này đã được sửa ở d0c0b3fa3 (v4). Bản nháp bị mở lại chỉ vì issue con #45099 trên Redmine còn New: QA mới test trên bản cũ 23be2526, trước khi sửa.

Không có commit mới so với lần bàn giao trước (04/11 13:36): nhánh giữ nguyên commit đã bàn giao.

Nội dung thay đổi:
- Job forward Kênh 1 và Kênh 2 (lần đầu và retry): đích trả 301/302/303/307/308 thì job ghi lỗi (http_status là mã 3xx, error_code=HTTP_ERROR), không gửi request tới Location, không retry. Trước đây 301/302/303 bị đi theo bằng GET và được ghi là thành công.
- Job forward Kênh 1: URL đích trên domain LME có path /line/callback/add/{đoạn bất kỳ} thì event bị IGNORE (status_sync=4), không gửi HTTP. Áp dụng cả cho các dạng /index.php/..., ./, .., \, //, %2F, host viết hoa hoặc có dấu . cuối, và cho webhook của mọi bot.
- Job retry Kênh 1: kiểm lại URL hiện tại theo cùng quy tắc; nếu là webhook LME thì queue và event nguồn bị IGNORE.
- Cấu hình job: khi không khai DOMAIN_ENDPOINT_WEBHOOK, default là https://cb.lmes.jp (trước đây là https://cb.lme.jp).

Bug QA con:
- #45099 đã sửa (commit linect-service@d0c0b3fa3c07): Client forward đã tắt followRedirects/followSslRedirects. 301/302 nay ghi lỗi HTTP_ERROR với đúng http_status, không gửi GET tới Location và không ghi thành công. QA mới test trên 23be2526 (bản trước khi sửa), nhờ test lại trên d0c0b3fa3.

File đã sửa (java-job):
  src/main/java/sns/line/ConfigFile.java             |  4 +-
  .../line/helper/WebhookRelaySettingManager.java    | 64 ++++++++++++++++++++++
  .../webhook/HandleForwardCallbackEventTask.java    |  9 +++
  .../webhook/HandleRetryWebhookRelayTask.java       |  8 +++
  .../threads/webhook/WebhookRelayApiClient.java     |  3 +
  5 files changed, 86 insertions(+), 2 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Code không đổi so với vòng 4/5 đã được duyệt. Thay đổi ở client chỉ là tắt redirect theo spec, và client này chỉ dùng cho tính năng forward chưa release.
- Forward Kênh 2 (HandleForwardLmeEventTask) dùng chung client: 3xx nay thành lỗi hiện trên 「転送エラー」.
- Retry của cả 2 kênh (HandleRetryWebhookRelayTask): 3xx ở lần thử lại được ghi lỗi, không retry tiếp. Chốt URL LME chỉ áp cho Kênh 1.
- Forward Kênh 1 tới URL bên thứ ba trả 2xx/5xx/timeout: forward, retry và ghi lỗi như cũ.
- ChangeBotJob và HandleCheckStatusConnectBotAndTool đọc DOMAIN_ENDPOINT_WEBHOOK: chỉ đổi hành vi ở môi trường không khai key này.
- Bảng callback_event.status_sync, webhook_relay_queue, webhook_relay_error: có thêm trường hợp IGNORE và lỗi 3xx, schema không đổi.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Tính năng forward chưa phát hành lên production, nên không có dữ liệu thật bị ghi sai.

Lưu ý khi deploy:
- Kiểm config.properties của job production có khai DOMAIN_ENDPOINT_WEBHOOK=https://cb.lmes.jp. Nếu không khai, job dùng default mới.
- Nên deploy cùng lúc hoặc sau bản web có #43730 (kiểm X-Line-Signature).

Việc cần người làm thêm (ngoài phạm vi task):
- QA/Test Studio test lại #45099 trên job@d0c0b3fa3 rồi cập nhật trạng thái trên Redmine (Resolved/Closed nếu đạt). Nếu #45099 còn New, hệ thống có thể lại mở bản nháp mới dù không có gì để sửa.
- QA test lại #45099 trên job@d0c0b3fa3 (3xx chỉ 1 POST, ghi HTTP_ERROR; 2xx thành công), test hồi quy Kênh 2 và retry, rồi cập nhật trạng thái #45099 trên Redmine để server không mở lại bản nháp.
- Build gốc của nhánh base release-t09-2026 thiếu dependency converter-jackson nên compileJava đang lỗi; cần sửa riêng, ngoài ticket này.
- QA/Test Studio test lại #45099 trên job d0c0b3fa3, rồi cập nhật trạng thái Redmine #45099 (đóng nếu đạt, hoặc gửi bằng chứng mới nếu lỗi còn tái hiện) để server không mở lại bản nháp không đổi code.

Điểm cần test:
- Test lại #45099 trên job@d0c0b3fa3: đích Kênh 1 trả 301/302/303 thì chỉ có 1 POST, không có GET tới Location, ghi lỗi HTTP_ERROR với đúng mã 3xx; đích trả 2xx vẫn ghi thành công
- Hồi quy Kênh 2 và retry khi gặp 3xx: ghi lỗi, không đi theo redirect
- Kênh 1: đích trả 301/302, Location trỏ về /line/callback/add/{B}. Mong đợi: đích chỉ nhận 1 POST, không có GET tới Location; status_sync=3; webhook_relay_error có http_status 301/302 và error_code=HTTP_ERROR; không có retry. Test trên job d0c0b3fa3.
- 303/307/308 và 3xx không có Location: ghi lỗi HTTP_ERROR, không đi theo redirect.
- Đích trả 2xx: vẫn DONE (status_sync=2).
- Kênh 2 và retry gặp 3xx: ghi lỗi, không đi theo redirect.
- Kênh 1 với URL /line/callback/add/{id} hoặc /index.php/line/callback/add/{id} trên domain LME: IGNORE (status_sync=4), không gửi HTTP.

Branch: ai_studio_fixbug_44780
- linect-service: ai_studio_fixbug_44780 (nhánh gốc release-t09-2026 @1690e2aab80c, commit d0c0b3fa3c077dbc4d6657e2bea9a698d376e0e0)
```
