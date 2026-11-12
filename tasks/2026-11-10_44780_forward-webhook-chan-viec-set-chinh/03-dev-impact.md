# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #44780 (6 journal "Dev Studio", 2026-10-30 → 2026-11-05) — issue **không có section "Đánh giá ảnh hưởng"** theo heading chuẩn, nội dung tổng hợp lại từ các journal bàn giao AI dev (không phải paste tay theo format 4 mục gốc). Tester cần đọc lại `01-bug-task.md` (mục Journal) để đối chiếu nguyên văn trước khi tick checkbox dưới đây.
> **Code cuối cùng tính tới thời điểm fetch (2026-11-05, không có commit mới sau đó):** `linect-service@d0c0b3fa3c077dbc4d6657e2bea9a698d376e0e0` (nhánh `ai_studio_fixbug_44780`, base `release-t09-2026@1690e2aab80c`).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Đoàn Thị Bích Hảo (assignee Redmine) — journal kỹ thuật do actor "Dev Studio" (AI dev) viết |
| Commit / Pull Request | Không có link PR; commit cuối `linect-service@d0c0b3fa3c077dbc4d6657e2bea9a698d376e0e0` (xem lịch sử 5 commit qua các vòng ở mục 1 bên dưới) |
| Branch | `ai_studio_fixbug_44780` (base `release-t09-2026@1690e2aab80c`) |
| Ngày submit đánh giá | 2026-11-05 (bản bàn giao cuối, Journal #151281) — bản đầu 2026-10-30 (#149840/#149861) |
| Auto-filled | 2026-11-10 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại toàn bộ 6 journal "Dev Studio" ở `01-bug-task.md` và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact) — đặc biệt phần redirect 3xx (#45099/#5018) chỉ xuất hiện từ journal #151096, không có ở journal đầu.

---

## 1. Nguyên nhân

Worker forward Kênh 1 (`HandleForwardCallbackEventTask`) và job thử lại (`HandleRetryWebhookRelayTask`) gửi nguyên body callback LINE tới `endpoint_url` mà **không kiểm tra URL đích**. Nếu khách đặt URL forward là chính webhook LME (`/line/callback/add/{bot_id}`) — của chính bot hoặc **bot khác** — request quay lại callback của LME, bị ghi thành `callback_event` mới rồi job lại forward tiếp → vòng lặp; từ khi web có #43730 (kiểm `X-Line-Signature`) thì mỗi event thành 1 lỗi 401 thay vì vòng lặp vô hạn.

Nguyên nhân mở rộng qua các vòng vá (lịch sử giữ nguyên để Leader thấy rõ phạm vi đã đổi):
- **Vòng 1 (commit `e6db3513`)**: chỉ chặn khi URL đích là webhook LME của **chính bot** forward (hàm `isLmeWebhookUrlOfBot` so `isSameBotId`). Leader yêu cầu mở rộng (Journal #150917 — Văn Dũng Đinh): "sửa chặn cả set webhook bot khác".
- **Vòng 3 (commit `23be2526b`)**: mở rộng chặn URL LME của **mọi bot** (không chỉ chính bot). Lúc này phát sinh bug con **#45094** (Redmine) / **#4978** (Test Studio) — do QA test ở vòng 1, các dạng viết lệch `./`, `..`, `\` trong path (id chính bot) chưa bị chặn — đã vá bằng cách parse URL qua OkHttp (cùng thư viện gửi) trước khi so khớp.
- **Vòng 4 (commit `d0c0b3fa3c07`)**: phát hiện 2 lỗ hổng khác — (a) `WebhookRelayApiClient.CLIENT` (OkHttp dùng chung Kênh 1+2) **không tắt follow-redirect**, nên đích trả 301/302/303 bị tự động đi theo bằng GET rỗng và ghi **thành công sai** theo mã 200 của đích cuối — lách được chốt chặn URL nếu đích bên thứ 3 redirect về webhook LME; (b) chốt chặn URL cũ đòi path đúng 4 đoạn nên dạng `/index.php/line/callback/add/{id}` (Laravel vẫn nhận) bị lọt. 2 lỗi này tương ứng bug con **#45099** (Redmine) / **#5018** (Test Studio).
- Giá trị default của `ConfigFile.DOMAIN_ENDPOINT_WEBHOOK` sai domain (`cb.lme.jp` thay vì domain callback thật `cb.lmes.jp`) — phát hiện ngay từ vòng 1, giữ nguyên fix tới bản cuối.
- **Ghi chú quan trọng cho QA**: ticket Redmine con #45099 tại thời điểm fetch (2026-11-10) còn trạng thái `New` — KHÔNG phải vì code chưa sửa, mà vì lượt QA test trước đó chạy trên commit `23be2526` (bản trước khi vá redirect). Dev đã xác nhận code không đổi từ vòng 4 (`d0c0b3fa3c07`) qua vòng 5/6; cần test lại đúng commit này rồi mới đóng #45099.

## 2. Cách fix

- **D-1**: Default `ConfigFile.DOMAIN_ENDPOINT_WEBHOOK` = `https://cb.lmes.jp` khi `config.properties` không khai key này (trước đây default sai `cb.lme.jp`).
- **D-2/D-3**: Job forward Kênh 1 (`HandleForwardCallbackEventTask`) — nếu URL đích trên domain LME (`DOMAIN_ENDPOINT_WEBHOOK` hoặc domain web `HOST_SNSLINE`) có path `/line/callback/add/{đoạn bất kỳ}` (kể cả `/index.php/...`, biến thể `./`, `..`, `\`, `//`, `%2F`, host viết hoa / có `.` cuối, có port, có query) ⇒ event đánh **IGNORE** (`status_sync=4`), không gửi HTTP, không ghi lỗi, không tăng `consecutive_failure_count`. Áp dụng cho webhook của **mọi bot** (chính bot và bot khác).
- **D-4**: Job retry Kênh 1 (`HandleRetryWebhookRelayTask`) kiểm lại URL hiện tại theo cùng quy tắc ở mỗi lần thử lại ⇒ queue + event nguồn IGNORE nếu URL đã bị đổi thành webhook LME giữa chừng.
- **D-5** (từ vòng 4): `WebhookRelayApiClient.CLIENT` tắt `followRedirects`/`followSslRedirects` ⇒ đích trả 301/302/303/307/308 ghi lỗi ngay (`http_status` = mã 3xx thật, `error_code=HTTP_ERROR`), không đi theo `Location`, không retry. Client này **dùng chung cho cả Kênh 1 và Kênh 2** (lần gửi đầu + retry) — nên thay đổi này ảnh hưởng cả 2 kênh, dù rule chặn URL LME (D-2/D-3/D-4) chỉ áp cho Kênh 1.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleForwardCallbackEventTask` (Kênh 1, lần gửi đầu) | Thêm check `isLmeWebhookUrl` trước khi forward (D-2/D-3) | Chặn vòng lặp / ghi sai bot |
| 2 | `HandleRetryWebhookRelayTask` (Kênh 1, retry) | Thêm check tương tự trước khi gửi lại (D-4) | Đồng bộ rule với lần gửi đầu |
| 3 | `WebhookRelayApiClient` (client OkHttp dùng chung Kênh 1 + Kênh 2) | Tắt `followRedirects`/`followSslRedirects` (D-5) | Redirect 3xx không còn tự thành "thành công" |
| 4 | `WebhookRelaySettingManager` (hàm nhận diện URL LME) | Hàm chốt chặn mở rộng qua 3 vòng: chính bot → mọi bot → cả `/index.php` + biến thể lệch | Dùng chung cho cả forward lẫn retry Kênh 1 |
| 5 | `ConfigFile.DOMAIN_ENDPOINT_WEBHOOK` | Default đổi `cb.lme.jp` → `cb.lmes.jp` (D-1) | Default cũ sai domain callback thật |

Dev xác nhận **KHÔNG đổi hành vi hiện có** ở: `HandleForwardLmeEventTask` (Kênh 2 forward, dùng chung `actionForward`) — vẫn forward bình thường, chỉ bị ảnh hưởng gián tiếp bởi D-5 (redirect 3xx); `actionRetry` Kênh 2 — tương tự; `ChangeBotJob` và `HandleCheckStatusConnectBotAndTool` — đọc `DOMAIN_ENDPOINT_WEBHOOK` nhưng chỉ đổi hành vi ở môi trường **không khai** key này trong `config.properties`.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandleForwardCallbackEventTask` (Kênh 1, lần gửi đầu) | `.../webhook/HandleForwardCallbackEventTask.java` | Direct | Thêm chặn IGNORE theo URL LME (D-2/D-3) |
| F2 | `HandleRetryWebhookRelayTask` (Kênh 1, retry) | `.../webhook/HandleRetryWebhookRelayTask.java` | Direct | Thêm chặn IGNORE (D-4) |
| F3 | `WebhookRelayApiClient` (client OkHttp dùng chung Kênh 1 + Kênh 2) | `.../threads/webhook/WebhookRelayApiClient.java` | Direct | Tắt follow-redirect 3xx (D-5) |
| F4 | `WebhookRelaySettingManager` (hàm nhận diện URL LME) | `.../line/helper/WebhookRelaySettingManager.java` | Direct | Hàm chốt chặn mới/mở rộng qua 3 vòng |
| F5 | `ConfigFile.DOMAIN_ENDPOINT_WEBHOOK` | `src/main/java/sns/line/ConfigFile.java` | Direct | Đổi default domain (D-1) |
| F6 | `HandleForwardLmeEventTask` (Kênh 2, forward) | (dùng chung `WebhookRelayApiClient`) | Indirect | KHÔNG áp rule chặn URL LME, nhưng 3xx giờ thành lỗi (`転送エラー`) thay vì tự "thành công" theo redirect |
| F7 | `HandleRetryWebhookRelayTask` nhánh Kênh 2 (retry, dùng chung `actionRetry`) | (dùng chung `WebhookRelayApiClient`) | Indirect | Tương tự F6 — 3xx ở lần thử lại ghi lỗi, không retry tiếp |
| F8 | `ChangeBotJob` (set/gỡ webhook LINE khi đổi kênh) | (đọc `DOMAIN_ENDPOINT_WEBHOOK`) | Indirect | Chỉ đổi hành vi khi `config.properties` **KHÔNG** khai `DOMAIN_ENDPOINT_WEBHOOK` |
| F9 | `HandleCheckStatusConnectBotAndTool` | (đọc `DOMAIN_ENDPOINT_WEBHOOK`) | Indirect | Tương tự F8 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `callback_event.status_sync` | UPDATE (thêm case mới) | Thêm giá trị `4=IGNORE` (trước có `2=DONE`, `3=lỗi`); redirect 3xx giờ ghi `status_sync=3` (lỗi) thay vì `2` (thành công sai như trước) |
| D2 | `webhook_relay_queue` | UPDATE (thêm case mới) | Queue retry đánh IGNORE khi URL đổi thành webhook LME ở lần thử lại |
| D3 | `webhook_relay_error` | UPDATE (thêm case mới) | Thêm case lỗi `http_status=3xx`, `error_code=HTTP_ERROR` cho redirect (trước đây không ghi lỗi vì tự thành công) |
| D4 | `config.properties` (`DOMAIN_ENDPOINT_WEBHOOK`) | Không đổi schema, chỉ đổi default trong code | Prod cần kiểm đã khai đúng `https://cb.lmes.jp` chưa — nếu thiếu, job tự dùng default mới |

Dev xác nhận: **không có migration / thay đổi dữ liệu** (đã kiểm diff); **không cần recover** — tính năng forward webhook (`#40475`, release-t09-2026, 2026-09-04) **chưa deploy production**, chỉ tồn tại ở nhánh `release-t09-2026` + `ai_studio_fixbug_44780`.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | `Webhook転送` Kênh 1 (「LINE公式アカウントデータ転送」) — forward callback LINE sang URL khách khai, cả lần gửi đầu & retry | F1, F2, F4, D1, D2, D3 | **High** — core logic đổi hành vi (thêm IGNORE + lỗi redirect), chưa qua production |
| T2 | `Webhook転送` Kênh 2 (「L Messageデータ転送」) — forward event LME, forward & retry | F3, F6, F7, D1, D3 | Medium — KHÔNG áp rule chặn URL LME, nhưng redirect 3xx giờ thành lỗi thay vì "thành công" ngầm như trước (hồi quy cần test) |
| T3 | Đổi kênh LINE của bot (`ChangeBotJob` — set/gỡ webhook LINE) | F8 | Low — chỉ đổi ở env thiếu khai `DOMAIN_ENDPOINT_WEBHOOK` |
| T4 | Kiểm trạng thái kết nối bot-tool (`HandleCheckStatusConnectBotAndTool`) | F9 | Low — tương tự T3 |
| T5 | Regression đối với 2 bug con đã raise trong quá trình fix: `#45094`/Test Studio `#4978` (biến thể `./`, `..`, `\`) và `#45099`/Test Studio `#5018` (redirect 3xx) | F1, F2, F3, F4 | Medium — **phải re-test đúng commit cuối `d0c0b3fa3c07`**, không phải `23be2526` (bản trước khi vá redirect) — nguồn gốc khiến `#45099` còn `New` trên Redmine dù code đã sửa |
| T6 | Việc cần làm thêm, **ngoài phạm vi ticket #44780** (không tạo TC ở đây, chỉ ghi nhận): validate URL webhook LME ngay tại màn web `Webhook転送` khi lưu cấu hình — **đã có ticket riêng #44660** (`tasks/2026-11-03_44660_forward-callback-chan-webhook-lme/`); Kênh 2 chưa áp rule chặn URL LME — Dev ghi nhận rủi ro còn mở, chưa có ticket; chuỗi lỗi JP riêng cho redirect 3xx trên màn `転送エラー` — spec chưa chốt, hiện dùng mã chung `HTTP_ERROR` | — | N/A (ngoài scope) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
