# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #42668 (Journal #143000/#143021 — v1, #143470/#143471 — v2) bằng `/new-task` lúc 2026-10-14.
>
> ⚠️ Dev Studio giao 2 vòng: **v1** (2026-10-12) xác định root cause gốc của #42668 + fix. **v2** (2026-10-13) **không đổi code** — chỉ phát hiện thêm 1 bug **KHÔNG liên quan** diff #42668 (API `/api/mobile/save-template` không lưu `管理名`/thư mục khi tạo mẫu tin mới qua API — lỗi có sẵn từ commit `0842c20356`, 2026-04-10) và đề nghị tách ticket riêng (`#42873`). Mục 1/2 dưới đây lấy nguyên nhân/cách fix gốc từ v1 (không đổi ở v2); mục 3/4 đã gộp thêm chi tiết v2 xác nhận.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (Redmine `assigned_to` để trống — fallback theo author journal đánh giá ảnh hưởng) |
| Commit / Pull Request | `<không có link PR>` — repo `sns-line`, nhánh gốc `release_step_20260930_v2` @`46765b418f67`, commit `69969a9c2da1e79d74819ac80cae0cfed6057c12` |
| Branch | `ai_studio_fixbug_42668` |
| Ngày submit đánh giá | `2026-10-13` (v2 — bản cuối; v1 nộp `2026-10-12`) |
| Auto-filled | `2026-10-14 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (Journal #143000/#143021/#143470/#143471) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Mẫu tin quick reply 「通知設定」 được lưu với ボタンテキスト (nhãn nút) rỗng qua màn soạn web (ngày 10/10, lúc 05:36 và 05:54). Server không kiểm nhãn trong `TemplateV2Service::saveButton`, nên lưu được. Bước kiểm ở FE (vee-validate rc7) có thể bị lọt: lỗi vừa được thêm lại bị xoá khi component vẽ lại, và `create-message.js` coi danh sách lỗi rỗng là hợp lệ. Khi auto-reply chạy, job đưa nhãn rỗng vào action quick reply nên LINE từ chối cả tin (`messages[0].quickReply.items[0].action -> "label" must be specified`), hiện mã lỗi 「エルメサポートまで」 cho khách.

`bot_id=179050`, `template_group_id=15908627&template_child_id=15908633`, `message_id=2273349419` (Journal #142497).

## 2. Cách fix

- **D-1** Thêm hàm kiểm nhãn nút rỗng dùng chung `TemplateV2Service::hasEmptyButtonLabel` trong `TemplateV2Service`.
- **D-2** Màn soạn web: từ chối lưu khi có nút trống nhãn → HTTP 422, câu báo 「ボタンテキストを入力してください。」, không lưu gì (kể cả tên/thư mục mẫu tin).
- **D-3** API app (`create-template`/`update-template`): chặn nhãn rỗng, giữ kiểu lỗi HTTP 200 sẵn có (`success=false`, key `error_message`).
- **D-4** `/api/mobile/save-template` (backend MCP dùng): chặn nhãn rỗng, trả 422 `success=false` (key `message`).
- Điều kiện chặn: `type=form`, `type_button` 1 (スタンダード) / 2 (カラー) / 4 (クイックリプライ), bất kỳ nút ở bất kỳ panel nào có label `null`/thiếu/mảng/chỉ khoảng trắng Unicode (bao gồm `　` toàn góc, NBSP, tab). Loại `画像` (3) và tin không phải form thì **không** bị kiểm, lưu như cũ.
- Biên đã có unit test: nhãn `'0'`, emoji ZWJ (`受け取る🙆‍♀️`), nhãn có khoảng trắng 2 đầu → hợp lệ.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TemplateV2Service::hasEmptyButtonLabel` — `app/Services/Templates/TemplateV2Service.php` | Hàm **mới**, dùng chung cho cả 3 lối lưu | Chặn tại 1 chỗ, tránh lệch logic giữa web/app/API |
| 2 | `TemplateV2Controller::saveTemplate` (web) — `app/Http/Controllers/Basic/TemplateV2Controller.php` | Gọi hàm check **trước** khi update `name`/`category_id` và trước `saveTemplateByType` | Web dùng **chung 1 endpoint** cho 5 ngữ cảnh: テンプレート/シナリオ/一斉配信/イベント/予約送信 |
| 3 | `Api\Mobile\TemplateMobileController` (`/api/mobile/create-template` · `update-template`, API app) — `.../Api/Mobile/TemplateMobileController.php` | Gọi hàm check, trả `success=false` + `error_message`, giữ HTTP 200 | Giữ nguyên shape lỗi cũ của API app (không đổi contract) |
| 4 | `Api\TemplateController::saveTemplate` (`/api/mobile/save-template`) — `app/Http/Controllers/Api/TemplateController.php` | Gọi hàm check, trả 422 `success=false` (key `message`) | Endpoint mà **backend MCP** (java-job, McpModel) dùng để tạo tin nút |
| 5 | `TemplateV2ServiceEmptyButtonLabelTest` (unit test mới) — `tests/Unit/TemplateV2ServiceEmptyButtonLabelTest.php` | Test biên: rỗng / khoảng trắng / `　` / tab / emoji ZWJ / nhãn `'0'` | Coverage cho hàm mới `hasEmptyButtonLabel` |

**v2 — phát hiện thêm (ngoài phạm vi fix #42668, KHÔNG đổi code):** `Api\TemplateController::saveTemplate` (`/api/mobile/save-template`) chỉ ghi `name`/`category_id` **TRƯỚC** khi lưu theo `template_child_id` client gửi — khi tạo mới, id này rỗng nên không bản ghi nào được cập nhật, mẫu tin tạo ra không có tên/thư mục. Lỗi có sẵn từ commit `0842c20356` (2026-04-10), không liên quan diff #42668. Dev đề nghị tách ticket riêng (`#42873`) — xem Ghi chú cuối file.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `TemplateV2Service::hasEmptyButtonLabel` (mới) | `app/Services/Templates/TemplateV2Service.php` | Direct | Dùng chung, gọi từ F2/F3/F4 |
| F2 | `TemplateV2Controller::saveTemplate` (web, `/ajax/template-v2/save-template`) | `app/Http/Controllers/Basic/TemplateV2Controller.php` | Direct | Chung endpoint cho template/scenario/sendAll/event/schedule_send |
| F3 | `Api\Mobile\TemplateMobileController` (`/api/mobile/create-template` · `update-template`) | `.../Api/Mobile/TemplateMobileController.php` | Direct | API app quản trị mobile — lỗi HTTP 200 `success=false` |
| F4 | `Api\TemplateController::saveTemplate` (`/api/mobile/save-template`) | `app/Http/Controllers/Api/TemplateController.php` | Direct | Backend MCP (AI tạo tin) dùng endpoint này — lỗi 422 |
| F5 | Job auto-reply (gửi tin quick reply) | `<không có trong diff — luồng job linect-service>` | Indirect | Không đổi code; mẫu tin cũ đã lưu nhãn rỗng trước fix vẫn lỗi khi gửi cho tới khi khách tự sửa |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `templates.name`, `templates.category_id` | UPDATE **bị chặn** (không ghi) khi nút trống nhãn | Web: 422 xảy ra TRƯỚC khi update tên/thư mục → DB phải giữ nguyên hoàn toàn |
| D2 | `tmp_buttons` / `buttons` (`label`) | CREATE/UPDATE **bị chặn** khi `label` rỗng/khoảng trắng | Chỉ áp dụng `type_button` 1 (スタンダード) / 2 (カラー) / 4 (クイックリプライ); loại 3 (画像) không bị chặn |
| D3 | Mẫu tin cũ đã tồn tại với `label` rỗng (production, trước fix) | Không có MIGRATE — dữ liệu cũ **giữ nguyên** | Không cần recover (khách production đã tự sửa 11/10); job gửi vẫn lỗi cho tới khi khách sửa nhãn các mẫu tin khác còn trống |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Soạn mẫu tin web — テンプレート / シナリオ / 一斉配信 / イベント / 予約送信 (dùng chung endpoint F2) | F2, D1, D2 | High — rủi ro chặn oan dữ liệu hợp lệ (nhãn `'0'`, emoji, carousel nhiều panel) trên **mọi** ngữ cảnh dùng chung màn soạn |
| T2 | API app quản trị mobile — tạo/sửa mẫu tin (`create-template`/`update-template`) | F3, D2 | Medium — đổi shape lỗi phải giữ HTTP 200/`success=false` như cũ |
| T3 | Backend MCP tạo mẫu tin qua `/api/mobile/save-template` (AI Studio / java-job dùng) | F4, D2 | Medium — nếu AI không gửi nhãn sẽ nhận 422 thay vì lưu mẫu tin hỏng (hành vi mới, cần QA biết để không coi là lỗi) |
| T4 | Job tự động trả lời (自動応答) / các job gửi tin dùng mẫu tin nút (quick reply, standard, color) | F5, D3 | High — liên quan trực tiếp bug gốc #42668: mẫu tin cũ trống nhãn vẫn làm job gửi lỗi cho tới khi được sửa; fix này **không** đổi code job |

---

## Ghi chú thêm (ngoài phạm vi #42668 — theo Dev v2)

- `#42873` (ticket riêng, chưa tạo tại thời điểm fetch): `/api/mobile/save-template` và `/api/mobile/create-template` tạo mẫu tin **độc lập** (không qua nhóm) không lưu `管理名`/thư mục — lỗi có sẵn, không do diff #42668 gây ra. Dev đề nghị: case test tạo mẫu tin qua API trong #42668 **chỉ kiểm nhãn/nội dung** (mở lại bằng id), **không kiểm** `管理名`/thư mục.
- FE vee-validate rc7 có thể xoá lỗi validate ngay sau khi mở mẫu tin (bấm 保存 ngay) — server đã chặn nên không mất an toàn dữ liệu, nhưng UX FE vẫn có thể hiện hộp thoại trống trước khi nhận lỗi 422. Cải tiến riêng, không thuộc phạm vi fix.
- Preview/placeholder hiện 「ボタン1」 khi nhãn rỗng → khách dễ tưởng đã đặt nhãn. Cải tiến riêng.
- CS/Dev cần quét các mẫu tin nút (loại 1/2/4) đang có `label` rỗng ở **bot khác** (ngoài bot ticket này) — các mẫu tin này vẫn lỗi khi job gửi cho tới khi khách tự sửa nhãn.
- Job gửi tin (linect-service) hiện xử lý nhãn rỗng khác web (web thay bằng `　`, job thì không) — đề xuất ticket riêng để đồng bộ, không thuộc phạm vi #42668.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
