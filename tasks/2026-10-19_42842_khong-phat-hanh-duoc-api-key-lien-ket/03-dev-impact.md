# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<không ghi tên cá nhân trong journal — journal author là "Dev Studio"; Redmine assigned_to: Kim Cúc>` |
| Commit / Pull Request | `<chưa có — không tìm thấy link PR/commit review, chỉ có branch + commit hash gốc>` |
| Branch | `ai_studio_fixbug_42842` (gốc `release_step_20260930_v2` @`c65e6e832037`, commit `d4bbc72274dc685138b769f8ba31066d4f7285f1`) |
| Ngày submit đánh giá | 2026-10-13 (Journal #143820 — "Dev handoff — v1", bản đầy đủ nhất; Journal #143744 cùng ngày là bản công bố nguyên nhân/hướng sửa sớm hơn, nội dung đã gộp vào #143820) |
| Auto-filled | 2026-10-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ Input thiếu / đặc biệt: Ticket này **không có khuôn 4 mục chuẩn** trong description — toàn bộ đánh giá nằm ở journal "Dev handoff — v1" (#143820, kèm bản công bố sớm hơn #143744). Quan trọng hơn: **nguyên nhân gốc của bug KHÔNG được xác định** — Dev tự nhận "Không xác định được" ở mục 1. Fix chỉ bổ sung hạ tầng chẩn đoán (log + retry + báo Chatwork), KHÔNG sửa logic phát hành API key thật sự. Mục 4 dưới đây được Leader/tester **tự suy ra** từ nội dung thay đổi + điểm cần test mà Dev liệt kê (Dev không tách riêng theo đúng khuôn F/D/T) — cần Leader xác nhận lại trước khi giao TC.

---

## 1. Nguyên nhân

Không xác định được. Câu 「APIキーの発行に失敗しました」 là câu mặc định của màn API連携, hiện ra cho **mọi** lỗi không phải lỗi nghiệp vụ: hết phiên, exception phía server, hoặc lỗi mạng. Support đã phát hành thành công trên **cùng tài khoản và bot** của khách, và không có log Laravel tương ứng (TungKS xác nhận) — nên không biết khách đã rơi vào trường hợp nào trong 3 trường hợp trên.

Theo yêu cầu của TungKS, hướng xử lý của task này là **thiết kế bổ sung phần ghi log frontend + retry** để lần sau (nếu khách gặp lại) có đủ thông tin chẩn đoán — **không phải fix root cause** vì root cause chưa biết.

## 2. Cách fix

Nội dung thay đổi (gộp từ #143744 + #143820, Dev handoff v1):

- **D-1** Thêm route public mới `POST /ajax/api-integration/report-client-error` nhận báo lỗi frontend của màn API連携 — không cần đăng nhập, giới hạn 10 lần/phút/user hoặc IP.
- **D-2** Controller + service mới (`ClientErrorReportService`) ghi log, **chặn trùng (10 phút)**, đẩy tin Chatwork qua job có sẵn (`SendJsErrorToChatwork`, dùng chung với báo lỗi màn đặt lịch event).
- **D-3** Thêm bộ báo lỗi + thu thập chẩn đoán xhr (HTTP status, error_code...) ở JS của màn API連携.
- **D-4** Bắt lỗi JS phát sinh trong **chính** JS của màn API連携 (qua `window.onerror`) và báo Chatwork — **KHÔNG** bắt được lỗi ném trong method Vue chạy từ event handler (Vue tự bắt, chỉ in `console.error`, không tới `window.onerror`).
- **D-5** Tự động gửi lại (retry) **1 lần** sau ~800ms khi request mất kết nối (status 0) — áp dụng cho: tải danh sách key, 👁 xem key, mở 操作履歴, phát hành, xoá. Nút giữ trạng thái khoá trong lúc chờ retry. Danh sách bị timeout 10 giây → **không** retry.
- **D-6** Báo Chatwork mỗi khi màn phải hiện câu lỗi chung (phát hành/lấy danh sách/xem/xoá/操作履歴), chặn trùng theo cùng 1 lỗi trong 10 phút.
- Nhánh retry đặc biệt (tránh double-action khi request thật ra đã thành công ở lần đầu, chỉ mất response):
  - **Phát hành**: lần retry báo trùng tên (`name_duplicated`) ⇒ hiểu là lần đầu **đã tạo key thành công** ⇒ hiện lỗi trùng tên inline như cũ **và tự tải lại danh sách** để key mới hiện ra (không tạo ra 2 key).
  - **Xoá**: lần retry nhận `404` **+ `error_code=resource_not_found`** (chặt hơn thiết kế gốc chỉ dựa vào 404, vì Handler chung có thể trả 404 cho exception bất kỳ) ⇒ hiểu là lần đầu **đã xoá thành công** ⇒ coi là xoá thành công (toast + key biến khỏi danh sách).
- Báo lỗi (log + Chatwork) **không được chứa full API key**.
- Migration/thay đổi dữ liệu: **không có** (Dev đã kiểm diff). Không cần recover dữ liệu — mỗi lượt phát hành chạy trong 1 transaction nên lần lỗi không ghi gì vào DB.
- Lưu ý deploy: `php artisan view:clear` (đổi Blade); bump `sns-line.version` (đổi JS, không tự bump nên tester phải Ctrl+F5 màn API連携khi test); queue worker connection `database` phải đang chạy thì tin Chatwork mới đi.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev không liệt kê riêng mục "function caller đã check" theo đúng khuôn mẫu — lấy từ file list ở Journal #143820 (Dev handoff). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Controllers/Basic/ApiIntegrationController.php` | +27 dòng | Gọi service ghi log lỗi; không đổi logic phát hành/xoá key hiện có |
| 2 | `ApiIntegration/ClientErrorReportService.php` | **File mới**, +101 dòng | Ghi log, chặn trùng 10 phút, đẩy job Chatwork |
| 3 | `public/_assets/modules/api_integration/js/index.js` | +446/-? dòng (thay đổi lớn nhất) | Thêm retry 1 lần sau 800ms cho mọi request của màn, bắt lỗi JS, thu thập chẩn đoán xhr, xử lý 2 nhánh retry đặc biệt (phát hành trùng tên / xoá 404) |
| 4 | `views/basic/api_integration/index.blade.php` | +5/-? dòng | Hỗ trợ hook báo lỗi JS mới |
| 5 | `routes/web.php` | +4 dòng | Thêm route public `POST /ajax/api-integration/report-client-error` nằm ngoài nhóm cần đăng nhập, cạnh route báo lỗi booking event — cần kiểm tên route không trùng |
| 6 | `ApiIntegrationClientErrorReportTest.php` | **File mới**, +159 dòng | Test cho route/service báo lỗi mới |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Toàn bộ thao tác màn API連携 (danh sách, tìm kiếm/lọc, 👁 xem key, phát hành, xoá, 操作履歴) | `index.js`, `ApiIntegrationController.php` | Direct | Mọi request đã chuyển sang hàm có retry 1 lần (~800ms) khi mất kết nối; nút khoá trong lúc chờ |
| F2 | `ClientErrorReportService` (ghi log + báo Chatwork lỗi frontend) | `ClientErrorReportService.php` (mới) | Direct | Chặn trùng 10 phút; KHÔNG chứa full API key trong log/Chatwork |
| F3 | Route public `POST /ajax/api-integration/report-client-error` | `routes/web.php`, `ApiIntegrationController.php` | Direct | Không cần đăng nhập; giới hạn 10 req/phút; dùng **chung bộ đếm throttle** với 👁 hiện key (30 lần/phút) và endpoint báo lỗi booking event |
| F4 | Bắt lỗi JS riêng màn API連携 (`window.onerror`) | `index.js` | Direct | KHÔNG bắt được lỗi ném trong method Vue chạy từ event handler (giới hạn thiết kế đã biết) |
| F5 | Nhánh retry phát hành (trùng tên ⇒ coi đã tạo) / retry xoá (404 + `resource_not_found` ⇒ coi đã xoá) | `index.js` | Direct | Rủi ro chính nếu sai: tạo key trùng hoặc báo xoá thành công nhầm |
| F6 | Job `SendJsErrorToChatwork` (dùng chung với báo lỗi màn đặt lịch event) | job có sẵn | Indirect | Thêm tin mới gắn tiền tố `[API連携]` — cần test không lẫn với tin booking event cũ |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | DB schema / bảng dữ liệu nghiệp vụ (API key) | **Không đổi** | Dev xác nhận đã kiểm diff — không có migration |
| D2 | Log Laravel (`laravel.log`) — dòng `[#42842][API連携] client error` | CREATE (log entry mới) | 1 log info (thành công sau retry) hoặc 1 log info + 1 log error (vẫn lỗi) tuỳ kịch bản; không chứa full API key |
| D3 | Chatwork room báo lỗi JS (dùng chung với báo lỗi màn đặt lịch event) | CREATE (message mới, có điều kiện) | Tiền tố `[API連携]`; chặn trùng cùng 1 lỗi trong 10 phút; chỉ gửi khi queue worker `database` đang chạy |
| D4 | Bộ đếm throttle (rate limit) route mới | Dùng chung counter với 👁 hiện key + endpoint báo lỗi booking event | Laravel 5.5 khoá throttle theo user/IP, không theo route — cần test không bị tính nhầm chéo giữa các endpoint |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Toàn bộ màn API連携 (danh sách/lọc, 👁, phát hành, xoá, 操作履歴) — luồng bình thường + lỗi nghiệp vụ (trùng tên, quá 10 key, tên rỗng/>50 ký tự) | F1, F5 | Medium — mọi request đổi sang hàm có retry; lỗi nghiệp vụ phải message y hệt cũ và KHÔNG gọi endpoint báo lỗi mới |
| T2 | Phát hành / xoá API key khi mất mạng (offline DevTools) ở các thời điểm khác nhau (lần 1 mất / lần 2 OK, cả 2 lần đều mất) | F1, F5 | High — đây là tính năng MỚI cốt lõi của fix; sai sẽ gây tạo trùng key hoặc báo xoá nhầm |
| T3 | Job `SendJsErrorToChatwork` + room Chatwork báo lỗi JS (dùng chung màn đặt lịch 予約イベント/booking event) | F6, D3 | Low — chỉ thêm tin mới có tiền tố riêng, nhưng cần test không lẫn/không spam giữa 2 nguồn lỗi |
| T4 | Rate limit (throttle) của route mới, 👁 hiện key, và endpoint báo lỗi booking event | F3, D4 | Medium — 3 endpoint dùng chung 1 bộ đếm theo Laravel 5.5 → cần test đúng ranh giới 10/phút và 30/phút không ảnh hưởng chéo |
| T5 | Nguyên nhân gốc bug (khách không phát hành được key) | — (chưa xác định) | **Không cải thiện bởi fix này** — vẫn có thể lặp lại; TC không thể "verify bug đã hết", chỉ verify cơ chế chẩn đoán (log + Chatwork) hoạt động đúng khi lặp lại |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix — **lưu ý: nguyên nhân gốc KHÔNG xác định được, chỉ verify được cơ chế chẩn đoán mới**
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
