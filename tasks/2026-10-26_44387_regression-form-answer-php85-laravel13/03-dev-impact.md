# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Nguồn khác chuẩn** — ticket #44387 không có section "Đánh giá ảnh hưởng phía dev" dạng Dev tự viết (đây là subtask QA tách từ #43845, không phải 1 bug fix). File này được **tổng hợp từ MCP LME TEST STUDIO `task_id=507`** (ticket #43845 — task nâng cấp PHP8.5/Laravel13 lớn, 21 task con), lọc lấy phần liên quan **Form Answer**:
> - `task_get_context(task_id=507, sections=["requirements","dev_impact","spec_delta"])` → 183 requirements tổng, lọc 14 cái liên quan Form Answer (theo keyword `form`/`フォーム`/`survey`/`回答`) + 47 file trong `spec_delta.files` (1480 file tổng) khớp đường dẫn `*Form*`/`*form_answer*`.
> - Dev impact tổng (13 dòng, KHÔNG tách riêng theo feature) giữ nguyên ở mục 1 — chỉ 1 dòng (bàn giao #15, TrustProxies) trực tiếp nhắc tới Form Answer qua hạ tầng chung (proxy/IP/https/URL tuyệt đối), còn lại là hạ tầng dùng chung toàn hệ thống.
> - **Leader/Tester PHẢI verify lại** — mapping F*/D*/T* dưới đây do AI suy ra từ danh sách file diff + requirement, KHÔNG phải Dev tự kê.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (pipeline, task #43845 / Studio task_id=507) |
| Commit / Pull Request | `<chưa có — tra theo bản bàn giao mới nhất của #43845 khi chạy test>` |
| Branch | `ai_studio_implement_43845` (release ref: `release_step_20260930_v2`) |
| Ngày submit đánh giá | `<chưa rõ — Studio task_id=507 updated_at 2026-10-25>` |
| Auto-filled | `2026-10-26 by /new-task` (tổng hợp từ MCP LME TEST STUDIO `task_id=507`, KHÔNG phải parse Redmine section chuẩn) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ checklist này giả định input từ Redmine Section B; ở đây nguồn là Studio `task_get_context`. Tester vẫn phải đọc lại đầy đủ mục 1→4 trước khi tick, đặc biệt verify danh sách 47 file + 14 requirement có sót gì không (có thể còn requirement/file Form Answer không chứa từ khóa `form` mà script lọc bỏ sót).

---

## 1. Nguyên nhân

Không phải 1 root cause đơn lẻ — đây là hệ quả của việc nâng framework (Laravel 5.5/PHP 7.2 → Laravel 13/PHP 8.5) trong 1 lần release cho toàn bộ module PHP Web (`sns-line`), áp dụng cho mọi tính năng kể cả Form Answer. Các điểm hạ tầng chung (Dev Studio ghi ở `dev_impact` của Studio task_id=507, 13 dòng) có khả năng chạm Form Answer:

- **Bàn giao #15** (gộp base `303a131b9c`): `TrustProxies` thêm IP `142.91.106.63` — ảnh hưởng IP khách/https/URL tuyệt đối khi request qua proxy tin cậy; request **không** qua proxy tin cậy phải bỏ qua `X-Forwarded-*`. → Form Answer trang trả lời phía khách (public, truy cập qua LIFF/URL ngoài) đi qua proxy này, ảnh hưởng tới domain/https của link form, link Google OAuth callback, link trong mail.
- **Phần nâng cấp bàn giao #1** (khung Laravel 13, phiên/cookie đổi 1 lần, Google apiclient, Symfony Mailer, Flysystem 3): Form Answer dùng Google apiclient cho tích hợp Google Spreadsheet, dùng Mailer khi gửi thử Gmail, dùng Flysystem khi lưu file upload của câu trả lời.
- **IDOR/SSRF vá từ bàn giao trước**: danh sách vá gồm nhiều màn dùng chung, Form Answer KHÔNG được nêu tên trực tiếp trong dòng này — cần đối chiếu riêng khi review.

14 requirement (trong tổng 183) của Studio `task_id=507` liên quan trực tiếp/giao Form Answer:

| req_key | risk | Nội dung |
|---|---|---|
| REQ-T4-05 | High | Form Blade `Input::` → `old()`/`request()`: giữ giá trị đã nhập khi lỗi validate + tham số query. 54 chỗ đổi (phần lớn Blade toàn hệ thống, Form Answer là 1 trong các màn dùng Blade form) |
| REQ-T7-01 | High | Step message HTML/tham số form như cũ, ký tự `& < "`, upload multipart, lỗi validate giữ chữ — Form Collective viết lại HTML thuần (màn step message, không phải Form Answer, nhưng dùng chung hạ tầng Form/Collective — kiểm chéo) |
| REQ-T7-03 | Medium | Doanh thu v2 xuất CSV không lỗi 419 — token form xuất CSV viết lại (hạ tầng CSRF token form dùng chung, Form Answer cũng có export CSV) |
| REQ-T9-04 | High | CSRF: POST từ LIFF/landing nhúng/**form answer** khác domain vẫn nhận; form không token bị chặn 419; ajax hết phiên 401 `SESSION_EXPIRED` (`PreventRequestForgery`, giữ 39 route `$except`) |
| REQ-T9-05 | Medium | Validate: ảnh base64 hỏng không 500, SVG nơi cho phép, rule email, câu lỗi 422 tiếng Nhật — áp dụng cho upload file câu trả lời Form Answer |
| REQ-T13-02 | High | **Form answer**/đặt lịch ghi Google Sheets đúng cột (Sheets form answer theo cấu trúc riêng); Gmail gửi thử tiêu đề tiếng Nhật |
| REQ-T21-02 | Medium | Màn Basic: tải CSV form có ô select thiếu settings, report tin text có dấu `"`, chi tiết talk list, error list hiển thị như cũ |
| REQ-T23-03 | Medium | **Form answer**, popup, thông báo app, mail tài khoản, export (PB-T23-3) như cũ |
| REQ-SEC-01 | High | Kiểm quyền bot (#43715): đổi bot qua URL không quyền bị chặn; upload **form khách** chỉ nhận đuôi cho phép |
| REQ-RG-BKG-03 | Medium | **Hồi quy: Form answer** — mở màn chính đủ dữ liệu, không 500/console; luồng chính tạo/sửa→lưu→mở lại; tìm/lọc/phân trang/sao chép/xoá/xuất nếu có |
| REQ-H335-03 | High | Tổng/trung bình/tỉ lệ dùng `LegacyMath` trùng production — bổ sung điểm **form chẩn đoán** checkbox + thập phân (`FormAnswerService.php:1495-1515,1766`) |
| REQ-H375-03 | Low | Trang 「メッセージ設定」 mở được, link form dùng LIFF đặt lịch (không phải Form Answer, nhưng cùng cơ chế link LIFF) |
| REQ-B3B97-09 | Medium | **Form khách** nhận thêm đuôi ảnh/video/âm thanh (trừ `svg`/`svgz`) — (#43715) |

## 2. Cách fix

Không áp dụng theo nghĩa "fix 1 bug" — đây là nâng cấp framework. Cách triển khai (tóm tắt theo requirement liên quan trên): đổi `Input::` → `old()`/`request()`; viết lại Form Collective bằng HTML thuần; `PreventRequestForgery` giữ danh sách route except cho LIFF/form answer khác domain; validate ảnh base64/SVG qua FormRequest; sửa `FormAnswerService.php` (dòng 1495-1515, 1766) cho phần tính điểm chẩn đoán dùng `LegacyMath`; vá quyền bot + đuôi file upload theo #43715.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Studio task_id=507 không trả về bảng caller riêng cho Form Answer — chỉ có spec_delta.files (danh sách file trong diff). Liệt kê 47 file Form Answer tìm được, Leader/Tester cần tự xác nhận caller nếu nghi ngờ sót. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `app/Services/FormAnswer/FormAnswerService.php` | Có trong diff — dòng 1495-1515, 1766 sửa tính điểm chẩn đoán (`LegacyMath`) | REQ-H335-03 |
| 2 | `app/Http/Controllers/Basic/FormAnswerController.php` | Có trong diff | Controller chính màn Form Answer admin |
| 3 | `app/Http/Controllers/Api/FormAnswerController.php` | Có trong diff | API app cho Form Answer |
| 4 | `app/FormAnswerConnectGoogle.php` | Có trong diff | Google apiclient nâng version — OAuth callback |
| 5 | `app/Jobs/InsertIntoGoogleSpreadSheetFormAnswer.php` + `.../AddResultFormAnswerToGoogleSpreadSheet.php` | Có trong diff | Job đồng bộ Google Sheets |
| 6 | `app/FriendInformationValue.php` + `FriendInformationValueReplicate.php` + `app/Models/FriendInformationHistory.php` | Có trong diff | Friend info bị update khi có câu trả lời mới |
| 7 | `app/Rules/ServiceUrlFormat.php` | Có trong diff | Validate rule dùng chung (URL service, có thể áp link Form Answer) |
| 8 | 39 file Blade `views/basic/form_answer/*` + `content_form*.blade.php` (xem đủ ở mục 4.1 F8) | Có trong diff | Form Collective → HTML thuần / `old()`/`request()` |

(Đầy đủ 47 file — xem mục 4.1 bên dưới, nhóm theo F1–F10.)

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Form Answer — CRUD/setting/list/folder (admin) | `app/FormAnswer.php`, `FormAnswerPage.php`, `FormAnswerSetting.php`, `FormAnswerSettingCommon.php`, `FormAnswerFolder.php`, `FormAnswerPointSetting.php`, `FormAnswerUserAccept.php`, `Http/Controllers/Basic/FormAnswerController.php`, `Services/FormAnswer/FormAnswerService.php`, `Services/FormAnswer/FormAnswerSettingCommonService.php`, `Eloquents/FormAnswerRepository.php` | Direct | Core — tạo/sửa/list/folder/cài đặt điểm |
| F2 | Form Answer — kết quả trả lời, remind | `FormAnswerDetails.php`, `FormAnswerResult.php`, `FormAnswerItemRemind.php`, `Observers/FormAnswerItemRemindObserver.php` | Direct | Màn kết quả + remind |
| F3 | Export CSV kết quả | `Exports/FormAnswerExport.php`, `Exports/FormAnswerSpecialExport.php` | Direct | REQ-T21-02 (CSV) |
| F4 | Google Sheets integration | `FormAnswerConnectGoogle.php`, `Jobs/InsertIntoGoogleSpreadSheetFormAnswer.php`, `Jobs/.../AddResultFormAnswerToGoogleSpreadSheet.php`, `Commands/CreateGoogleSheetFormAnswerCommand.php` | Direct | REQ-T13-02 — Google apiclient nâng version |
| F5 | Xóa/khôi phục form | `Commands/ForceDeleteFormAnswerCommand.php`, `Commands/RecoverFormAnswerV3Command.php` | Direct | Job dọn/khôi phục |
| F6 | API app (mobile) | `Http/Controllers/Api/FormAnswerController.php` | Direct | API app liên quan Form Answer |
| F7 | Friend info update từ câu trả lời | `FriendInformationSetting.php`, `FriendInformationSettingReplicate.php`, `FriendInformationValue.php`, `FriendInformationValueReplicate.php`, `FriendDetailFormAnswerService.php`, `Models/FriendInformationHistory.php`, `Http/Controllers/Api/FriendInformationController.php`, `Basic/FriendInformationController.php` | Indirect | Câu trả lời ghi vào thông tin bạn bè + lịch sử |
| F8 | Views/Blade render form (admin + public) | `views/basic/form_answer/form_render.blade.php`, `form_result.blade.php`, `form_result_v3.blade.php`, `index_v3.blade.php`, `v3/form_render.blade.php`, `v3/form_render_preview.blade.php`, `views/basic/scenario/content_form_message.blade.php`, `views/basic/broadcast/content_form.blade.php`, `views/layout/broadcast/content_form.blade.php` | Direct | `Input::` → `old()`/`request()`; CSS/JS/preview |
| F9 | Validate URL rule | `Rules/ServiceUrlFormat.php` | Indirect | Dùng chung nhiều màn, áp cả link Form Answer |
| F10 | Khác (liên quan gián tiếp) | `CalendarSalonSettingSendForms.php`, `CalendarSettingSendForms.php`, `Commands/HandleUpdateLatestInformationCsv.php`, `tests/Feature/LegacyPerPageFormResultTest.php`, `views/admin/payment/payment_form.blade.php` | Indirect | Test có sẵn (`LegacyPerPageFormResultTest`) cần chạy lại |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `form_answers`, `form_answer_pages`, `form_answer_settings`, `form_answer_folders` | Không MIGRATE (spec không đổi) — chỉ code đọc/ghi qua Eloquent nâng version | Kiểm không đổi field/charset |
| D2 | `form_answer_results` / `form_answer_details` | UPDATE (ghi kết quả trả lời mới) | Liên quan tính điểm chẩn đoán (REQ-H335-03) |
| D3 | `form_answer_item_reminds` | UPDATE/CREATE | Remind job |
| D4 | `friend_information_values` + `friend_information_history` | CREATE/UPDATE | Ghi khi câu trả lời cập nhật thông tin bạn bè |
| D5 | Google Spreadsheet (external, qua Google apiclient mới) | CREATE/UPDATE (ghi hàng mới / tạo sheet) | REQ-T13-02 — RULE-08: không kết luận integration ngoài từ local/staging |
| D6 | File upload câu trả lời (Flysystem 3) | CREATE | Đổi thư viện lưu file — kiểm đường dẫn/quyền file không đổi |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Form builder (tạo/sửa/list/folder/xóa/khôi phục form) | F1, F5, D1 | Medium |
| T2 | Trang trả lời phía khách (LIFF + web, nhập/submit, giới hạn trả lời, upload file) | F8, F9, D6, REQ-T9-04/T9-05 | High (CSRF cross-domain + validate upload vừa đổi) |
| T3 | Kết quả trả lời, chi tiết, tính điểm/chẩn đoán, remind, xuất CSV | F2, F3, D2, D3, REQ-H335-03 | High (LegacyMath tính điểm là điểm nóng PHP8 — xem php-upgrade-checklist A3) |
| T4 | Liên kết Google Spreadsheet + job tạo sheet/đồng bộ | F4, D5, REQ-T13-02 | High (RULE-08 — bắt buộc test ở env có prd/thật, Google apiclient đổi version) |
| T5 | Cập nhật thông tin bạn bè + lịch sử + action phát sinh từ câu trả lời | F7, D4 | Medium |
| T6 | API app liên quan trực tiếp Form Answer | F6 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix — ⚠️ đây là tổng hợp AI từ Studio, không phải Dev tự viết, Leader cần đối chiếu lại với bản bàn giao #43845 thật
- [ ] Mục 2 (cách fix) có thể trace về code — mới trace qua `spec_delta.files` (danh sách file diff), chưa đọc nội dung diff thật
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — danh sách 47 file có thể sót (lọc bằng từ khóa `form`/`フォーム`, không đọc toàn bộ 1480 file diff)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
