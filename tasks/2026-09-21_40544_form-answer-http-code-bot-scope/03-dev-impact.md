# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Đoàn Thị Bích Hảo |
| Commit / Pull Request | commit `8d4900408d` (repo `sns-line`) — Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=40544 |
| Branch | `ai_fixbug_40544` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-16 (journal #136752) |
| Auto-filled | `2026-09-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Các endpoint api/ajax của tính năng Tạo biểu mẫu trả HTTP code không đúng nghĩa:

- Lỗi nghiệp vụ (chưa kết bạn, hết lượt trả lời, trùng tên trang, còn item chẩn đoán) trả **200** nên trình duyệt coi là thành công.
- Thiếu tham số và không tìm thấy dữ liệu lại trả **500** như lỗi hệ thống.
- Nhiều khối `catch` trả **200/400** thay vì **500**.
- **Nặng nhất**: service trả thẳng đối tượng response rồi bị controller bọc lại nên mã lỗi bị nuốt hoàn toàn, client luôn nhận **200**.
- Phần lớn endpoint cũng **không kiểm tra tham số bắt buộc** nên thiếu tham số thì lặng lẽ không lưu hoặc vỡ ở tầng dưới.

## 2. Cách fix

**(a) Chuẩn hoá HTTP status** cho toàn bộ api/ajax của Tạo biểu mẫu theo quy ước `.claude/docs/api-error-code-rules.md`:

| Mã | Áp cho nhóm lỗi |
|---|---|
| **400** | Thiếu tham số / sai kiểu / không xác định được người trả lời |
| **403** | Vượt hạn mức gói; chưa kết bạn hoặc đã chặn bot |
| **404** | Không tìm thấy biểu mẫu / trang / thư mục / người dùng |
| **409** | Hết lượt trả lời; trùng tên trang; còn item chẩn đoán; đang sao chép dữ liệu |
| **410** | Biểu mẫu đã gỡ |
| **422** | Sai giá trị field (tên thư mục; tên trang được gửi lên nhưng rỗng; định dạng tệp) |
| **500** | Chỉ còn ở `catch`, và **không đẩy nội dung lỗi nội bộ ra cho người dùng cuối** |

- Sửa lỗi service trả đối tượng response bị controller bọc lại làm mất mã lỗi.
- Thêm kiểm tra tham số bắt buộc cho **8 endpoint ghi dữ liệu ở web** và **4 API mobile**.
- Cập nhật các handler JS đọc trạng thái nghiệp vụ từ nhánh `error`.

**(b) Refix vòng 1 (theo AI review)**:
- `updatePage` **không còn bắt buộc** `page_name` (endpoint dùng cho cập nhật từng phần `page_image`).
- Helper `validateRequestOrFail` đổi **422 → 400** ở cả 2 controller.
- JS `diagnostic_content.js` bắt khoảng **400-499** thay vì cứng 409/422.

**(c) Bổ sung theo yêu cầu human — mọi query phải ràng buộc theo bot đang đăng nhập**:

Thêm 3 helper dùng chung trong `Basic\FormAnswerController`: `findFormForCurrentBot` / `formIdsForCurrentBot` / `formNotFoundResponse` — đặt điều kiện `bot_id` **NGAY TRONG QUERY** theo `BE-coding-rules` mục 4.1, rồi chặn ở cửa vào các endpoint quản trị:

| Endpoint | Ghi chú của Dev |
|---|---|
| `store` | Chủ sở hữu form lấy từ **session** thay vì `bot_id` do client gửi |
| `save`, `saveV3` | Kèm ràng buộc trang/item về đúng form đang lưu |
| `ajaxGetFormAnswerList`, `ajaxGetFormAnswerListV3` | Khối **xoá lan sang bảng con** trước đây **không hề lọc bot** |
| `changePublicFormAnswer` | |
| `sortFormAnswer` | |
| `createFolder` | (đổi tên thư mục) |
| `copyFormanswer` | Trước đây lấy luôn `bot_id` của form nguồn → **copy được form bot khác** |
| `deleteListFormanswer` | Lọc danh sách id về form của bot |
| `restoreFormAnswer` | |
| `addPage` | |
| `saveMessageReply` | |
| `updatePage` | Tra chủ sở hữu qua `form_answer.bot_id` + loại khoá `id`/`bot_id`/`form_id` khỏi mass-assignment |
| `updateDiagnosticContentSettings` | |
| `stopItemRemind` | |
| Sắp xếp thư mục | |
| `apiDetailFormanswerResult` (API mobile) | Join `form_answer` để lọc theo `bot_id` — trước đây **đọc được kết quả trả lời của bot khác chỉ bằng id** |

- Không thuộc bot hiện tại → **404 với thông báo tiếng Nhật**.
- ⚠️ **CỐ Ý KHÔNG áp** cho nhóm endpoint **enduser** (`form-render/store`, `checking-next-page`, `open-formanswer`, `user-accept-form`, `init-formanswer-detail`, upload ảnh khi trả lời) vì đó là route công khai người trả lời form dùng, **không có bot trong session**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Dev kê theo danh sách function (mục 3 journal), không kèm cột "thay đổi/lý do" riêng.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FormAnswerService::checkingNextPage` — `app/Services/FormAnswer/FormAnswerService.php` | Sửa lỗi service trả JsonResponse bị controller bọc lại | Nơi lỗi "nuốt status" đã xảy ra thật, tài liệu quy ước ghi rõ |
| 2 | `FormAnswerService::storeRenderForm` — `app/Services/FormAnswer/FormAnswerService.php` | Chuẩn hoá status | Cùng anti-pattern |
| 3 | `FormAnswerController::checkingNextPage` — `Basic/FormAnswerController.php` | Chuẩn hoá status | Caller của (1) |
| 4 | `FormAnswerController::storeRenderForm` — `Basic/FormAnswerController.php` | Chuẩn hoá status | Caller của (2) |
| 5 | `FormAnswerController::userOpenFormanswer` — `Basic/FormAnswerController.php` | Chuẩn hoá status | Endpoint enduser (không áp ràng buộc bot) |
| 6 | `FormAnswerController::userAcceptFormAnswer` — `Basic/FormAnswerController.php` | Chuẩn hoá status | Endpoint enduser (không áp ràng buộc bot) |
| 7 | `FormAnswerController::initDetailForm` / `initDetailFormV3` — `Basic/FormAnswerController.php` | Chuẩn hoá status | Endpoint enduser (không áp ràng buộc bot) |
| 8 | `FormAnswerController::uploadImageFormAnswer` / `uploadImageFormAnswerRender` — `Basic/FormAnswerController.php` | Chuẩn hoá status (422 định dạng tệp) | Upload ảnh khi trả lời = enduser, không áp ràng buộc bot |
| 9 | `FormAnswerController::createFolder` / `deleteFolder` / `copyFormanswer` — `Basic/FormAnswerController.php` | Chuẩn hoá status + ràng buộc bot | `copyFormanswer` trước đây copy được form bot khác |
| 10 | `FormAnswerController::addPage` / `updatePage` / `updateDiagnosticContentSettings` — `Basic/FormAnswerController.php` | Chuẩn hoá status + ràng buộc bot + bỏ mass-assignment khoá | |
| 11 | `FormAnswerController::store` / `storeV3` / `saveV3` / `restoreFormAnswer` — `Basic/FormAnswerController.php` | Chuẩn hoá status + ràng buộc bot; `store` lấy chủ sở hữu từ session | |
| 12 | `FormAnswerController::validateRequestOrFail` — `Basic/FormAnswerController.php` | Helper validate required; refix vòng 1 đổi 422 → **400** | Dùng chung nhiều endpoint |
| 13 | `Api\FormAnswerController::validateRequestOrFail` + **4 API mobile** — `Api/FormAnswerController.php` | Validate required + `apiDetailFormanswerResult` join lọc `bot_id` | `apiGetFormAnswerList` **giữ nguyên** contract 200 + cờ permission |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev kê mục 4.1 theo **file thay đổi** (10 file), không theo function. Giữ nguyên danh sách Dev kê; danh sách endpoint cụ thể xem mục 2(c) và mục 3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Toàn bộ api/ajax quản trị Form answer (web) | `app/Http/Controllers/Basic/FormAnswerController.php` | Direct | Chuẩn hoá HTTP code + validate required + ràng buộc bot (16 endpoint ở mục 2c) |
| F2 | 4 API mobile Form answer + helper validate | `app/Http/Controllers/Api/FormAnswerController.php` | Direct | `apiDetailFormanswerResult` thêm join lọc `bot_id`; `apiGetFormAnswerList` **không đổi contract** |
| F3 | Service layer Form answer | `app/Services/FormAnswer/FormAnswerService.php` | Direct | Sửa lỗi service trả JsonResponse bị controller bọc lại (nuốt status) |
| F4 | JS màn trả lời form v3 | `public/js/form_answer/form_render_v3.js` | Direct | Thêm nhánh xử lý `error` |
| F5 | JS màn trả lời form (v1) | `public/js/form_answer/form_render.js` | Direct | Thêm nhánh xử lý `error` |
| F6 | JS màn tạo form | `public/js/form_answer/create.js` | Direct | Thêm nhánh xử lý `error` |
| F7 | JS màn danh sách form | `public/js/form_answer/index.js` | Direct | Thêm nhánh xử lý `error` (xoá / copy / khôi phục / thư mục / sort) |
| F8 | JS màn danh sách form v3 | `public/js/form_answer/index_v3.js` | Direct | Thêm nhánh xử lý `error` |
| F9 | JS cấu hình item của form v3 | `public/js/form_answer/v3/setting_form_items.js` | Direct | Thêm nhánh xử lý `error` |
| F10 | JS nội dung chẩn đoán v3 | `public/js/form_answer/v3/diagnostic_content.js` | Direct | Refix vòng 1: bắt khoảng **400-499** thay vì cứng 409/422 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(không có)* | — | Dev kê: "Không có - chỉ đổi mã HTTP trả về và thêm kiểm tra đầu vào, **không đụng dữ liệu đã lưu**". Không cần recover data (mục 5 journal). |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Form Builder (FA-011)** — toàn bộ api/ajax của màn tạo/sửa biểu mẫu và màn người dùng trả lời biểu mẫu: đổi mã HTTP, thêm kiểm tra tham số bắt buộc, cập nhật xử lý lỗi phía trình duyệt | F1–F10 | **High** (Dev chỉ kê 1 dòng duy nhất cho mục 4.3) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

## Lưu ý khi test (Dev tự nêu — journal mục "TỰ REVIEW")

1. ⚠️ **Cache JS**: trình duyệt giữ bản JS cũ sẽ rơi vào nhánh `error` mà không có xử lý. Dev **không tự bump version** trong `config/sns-line.php` theo rule dự án → cần đội release bump khi phát hành.
2. ⚠️ **API mobile `apiGetFormAnswerList` CỐ Ý không đổi contract** (vẫn 200 + cờ permission) vì app Flutter đang đọc cờ này.
3. ⚠️ **Ràng buộc bot đổi hành vi**: form/thư mục/trang không thuộc bot hiện tại nay trả **404** thay vì im lặng không đổi gì hoặc sửa nhầm. Nếu nghiệp vụ thật có **luồng nhiều bot dùng chung một form** (Dev chưa thấy trong code) thì phải xem lại.
4. ⚠️ **`updatePage`** tra chủ sở hữu qua **JOIN `form_answer.bot_id`**, KHÔNG dựa cột `bot_id` của bản ghi trang, để trang cũ có `bot_id` trống/lệch vẫn sửa được. **CHƯA đối chiếu được dữ liệu thật** (không kết nối được MySQL dev) — cần kiểm lại khi có DB.
5. ⚠️ **`store` (form v1)** đổi chủ sở hữu form mới từ `$request->bot_id` sang **session bot**. Blade `create` truyền đúng bot session nên luồng thật không đổi, nhưng nếu còn client nào gửi `bot_id` khác thì form sẽ về bot session.
6. ⚠️ **Verify chỉ mức lint** (`php -l` 3 file PHP + `node --check` 7 file JS) — **chưa chạy runtime**. Dev yêu cầu test tay: tạo / lưu / xoá / copy / khôi phục form, đổi tên thư mục, thêm-sửa trang, đặt/xoá ảnh nền trang v3.
