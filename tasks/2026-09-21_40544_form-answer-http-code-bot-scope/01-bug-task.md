# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40544 — Form answer` |
| Module / Màn hình | Form Builder (FA-011) — toàn bộ api/ajax của màn **Tạo biểu mẫu** (フォーム作成) + màn người dùng trả lời biểu mẫu + 4 API mobile của Form answer |

## Mô tả bug (bản dịch tiếng Việt)

> Description Redmine đã viết bằng tiếng Việt — chép nguyên văn, không diễn giải lại.

```
Sửa lại http code cho đúng ý nghĩa với các api, ajax
validate required đầu vào

Mọi query đều PHẢI ràng buộc theo bot đang đăng nhập
```

Ticket do Kieu Son Tung tạo với tracker `Bug API` — là **yêu cầu chuẩn hoá kỹ thuật**, gồm 3 yêu cầu:

1. Chuẩn hoá HTTP status code cho toàn bộ api/ajax của tính năng Form answer theo đúng ngữ nghĩa.
2. Bổ sung validate tham số bắt buộc (required) ở đầu vào.
3. **Mọi query phải ràng buộc theo bot đang đăng nhập** (chống IDOR — đọc/sửa/xoá dữ liệu của bot khác).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket là yêu cầu chuẩn hoá, không kèm ca lỗi cụ thể. -->

## Expected result

<!-- (trống — bảng mã HTTP kỳ vọng cho từng nhóm lỗi nằm ở mục 2 "Cách fix" của 03-dev-impact.md) -->

## Actual result

<!-- (trống) -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40544 không có attachment nào. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** (không có section "Tái hiện bug", Steps/Expected/Actual trống). Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** + **regression impact**.

- Ticket do **AI AUTO-FIXBUG** xử lý (journal #136752, 2026-09-16), status hiện tại `Fix done - Đợi test`, assignee **Đoàn Thị Bích Hảo**.
- Branch để QA checkout: **`ai_fixbug_40544`** (repo `sns-line`, nhánh gốc `release_step_20260827`, commit `8d4900408d`, 10 file).
- ⚠️ **Mức verify của Dev chỉ dừng ở lint** (`php -l` + `node --check`) — **KHÔNG chạy được runtime** (container không có DB/app LME dựng sẵn). Toàn bộ hành vi phải test tay.
- ⚠️ **Cache JS phía trình duyệt**: 7 file JS đã sửa. Trình duyệt còn giữ bản JS cũ sẽ rơi vào nhánh `error` mới mà không có xử lý. Dev **không tự bump version** trong `config/sns-line.php` theo rule dự án → cần đội release bump khi phát hành. **Khi test phải hard-reload / clear cache.**
- ⚠️ **Thay đổi hành vi có chủ đích** (không phải regression): form / thư mục / trang **không thuộc bot đang đăng nhập** nay trả **404 + thông báo tiếng Nhật**, thay vì trước đây im lặng không đổi gì hoặc sửa nhầm dữ liệu bot khác.
- ⚠️ **Phạm vi CỐ Ý loại trừ**:
  - Nhóm endpoint **enduser** (`form-render/store`, `checking-next-page`, `open-formanswer`, `user-accept-form`, `init-formanswer-detail`, upload ảnh khi trả lời) **KHÔNG** áp ràng buộc bot — là route công khai người trả lời form dùng, không có bot trong session.
  - API mobile `apiGetFormAnswerList` **giữ nguyên contract 200 + cờ permission** vì app Flutter đang đọc cờ này.
- ⚠️ **Điểm Dev tự đánh dấu chưa chắc chắn**:
  - `updatePage` tra chủ sở hữu qua JOIN `form_answer.bot_id` (không dựa cột `bot_id` của bản ghi trang) để trang cũ có `bot_id` trống/lệch vẫn sửa được — **chưa đối chiếu được dữ liệu thật**.
  - `store` (form v1) đổi chủ sở hữu form mới từ `$request->bot_id` sang **bot trong session**. Blade `create` truyền đúng bot session nên luồng thật không đổi, nhưng client nào gửi `bot_id` khác thì form sẽ về bot session.
  - Nếu nghiệp vụ thật có luồng **nhiều bot dùng chung một form** (Dev chưa thấy trong code) thì phải xem lại toàn bộ ràng buộc bot.
- Môi trường test: ticket chưa ghi rõ.

## Journal / note từ Redmine (nguyên văn)

**Journal #136752 — AI LME Fix bug — 2026-09-16:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Các endpoint api/ajax của tính năng Tạo biểu mẫu trả HTTP code không đúng nghĩa: lỗi nghiệp vụ (chưa kết bạn, hết lượt trả lời, trùng tên trang, còn item chẩn đoán) trả 200 nên trình duyệt coi là thành công; thiếu tham số và không tìm thấy dữ liệu lại trả 500 như lỗi hệ thống; nhiều khối catch trả 200/400 thay vì 500. Nặng nhất: service trả thẳng đối tượng response rồi bị controller bọc lại nên mã lỗi bị nuốt hoàn toàn, client luôn nhận 200. Phần lớn endpoint cũng không kiểm tra tham số bắt buộc nên thiếu tham số thì lặng lẽ không lưu hoặc vỡ ở tầng dưới.

■ 2. CÁCH FIX
Chuẩn hoá HTTP status cho toàn bộ api/ajax của Tạo biểu mẫu theo quy ước .claude/docs/api-error-code-rules.md: thiếu tham số/sai kiểu/không xác định được người trả lời → 400; vượt hạn mức gói và chưa kết bạn/đã chặn bot → 403; không tìm thấy biểu mẫu/trang/thư mục/người dùng → 404; hết lượt trả lời, trùng tên trang, còn item chẩn đoán, đang sao chép dữ liệu → 409; biểu mẫu đã gỡ → 410; sai giá trị field (tên thư mục, tên trang được gửi lên nhưng rỗng, định dạng tệp) → 422; catch chỉ còn 500 và không đẩy nội dung lỗi nội bộ ra cho người dùng cuối. Sửa lỗi service trả đối tượng response bị controller bọc lại làm mất mã lỗi. Thêm kiểm tra tham số bắt buộc cho 8 endpoint ghi dữ liệu ở web và 4 API mobile. Cập nhật các handler JS đọc trạng thái nghiệp vụ từ nhánh error. [Refix vòng 1 theo AI review] updatePage không còn bắt buộc page_name (endpoint dùng cho cập nhật từng phần page_image) và helper validateRequestOrFail đổi 422 → 400 ở cả 2 controller, JS diagnostic_content.js bắt khoảng 400-499 thay vì cứng 409/422. [Bổ sung theo yêu cầu human: mọi query phải ràng buộc theo bot đang đăng nhập] Thêm 3 helper dùng chung trong Basic\FormAnswerController (findFormForCurrentBot / formIdsForCurrentBot / formNotFoundResponse) đặt điều kiện bot_id NGAY TRONG QUERY theo BE-coding-rules mục 4.1, rồi chặn ở cửa vào của các endpoint quản trị: store (chủ sở hữu form lấy từ session thay vì bot_id do client gửi), save, saveV3 (kèm ràng buộc trang/item về đúng form đang lưu), ajaxGetFormAnswerList + ajaxGetFormAnswerListV3 (khối xoá lan sang bảng con trước đây không hề lọc bot), changePublicFormAnswer, sortFormAnswer, createFolder (đổi tên thư mục), copyFormanswer (trước đây lấy luôn bot_id của form nguồn nên copy được form bot khác), deleteListFormanswer (lọc danh sách id về form của bot), restoreFormAnswer, addPage, saveMessageReply, updatePage (tra chủ sở hữu qua form_answer.bot_id + loại khoá id/bot_id/form_id khỏi mass-assignment), updateDiagnosticContentSettings, stopItemRemind và sắp xếp thư mục; API mobile apiDetailFormanswerResult join form_answer để lọc theo bot_id (trước đây đọc được kết quả trả lời của bot khác chỉ bằng id). Không thuộc bot khác → 404 với thông báo tiếng Nhật. CỐ Ý không áp cho nhóm endpoint enduser (form-render/store, checking-next-page, open-formanswer, user-accept-form, init-formanswer-detail, upload ảnh khi trả lời) vì đó là route công khai người trả lời form dùng, không có bot trong session.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
FormAnswerService::checkingNextPage (app/Services/FormAnswer/FormAnswerService.php)
FormAnswerService::storeRenderForm (app/Services/FormAnswer/FormAnswerService.php)
FormAnswerController::checkingNextPage (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::storeRenderForm (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::userOpenFormanswer (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::userAcceptFormAnswer (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::initDetailForm / initDetailFormV3 (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::uploadImageFormAnswer / uploadImageFormAnswerRender (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::createFolder / deleteFolder / copyFormanswer (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::addPage / updatePage / updateDiagnosticContentSettings (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::store / storeV3 / saveV3 / restoreFormAnswer (app/Http/Controllers/Basic/FormAnswerController.php)
FormAnswerController::validateRequestOrFail (app/Http/Controllers/Basic/FormAnswerController.php)
Api\FormAnswerController::validateRequestOrFail + 4 API mobile (app/Http/Controllers/Api/FormAnswerController.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/FormAnswerController.php
   - app/Http/Controllers/Api/FormAnswerController.php
   - app/Services/FormAnswer/FormAnswerService.php
   - public/js/form_answer/form_render_v3.js
   - public/js/form_answer/form_render.js
   - public/js/form_answer/create.js
   - public/js/form_answer/index.js
   - public/js/form_answer/index_v3.js
   - public/js/form_answer/v3/setting_form_items.js
   - public/js/form_answer/v3/diagnostic_content.js
 • 4.2 Data ảnh hưởng:
   - Không có - chỉ đổi mã HTTP trả về và thêm kiểm tra đầu vào, không đụng dữ liệu đã lưu
 • 4.3 Tính năng liên quan:
   - Form Builder (FA-011) - toàn bộ api/ajax của màn tạo/sửa biểu mẫu và màn người dùng trả lời biểu mẫu: đổi mã HTTP, thêm kiểm tra tham số bắt buộc, cập nhật xử lý lỗi phía trình duyệt

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l cho 3 file PHP đã sửa: OK; node --check cho 7 file JS đã sửa: OK; Đối chiếu từng thay đổi với bảng mã chuẩn tại .claude/docs/api-error-code-rules.md muc 1 + cây quyết định muc 2; Rà từng endpoint đổi 200 -> 4xx, tìm handler JS gọi nó và bổ sung nhánh error tương ứng (checklist muc 6 cua tai lieu quy uoc)
   Bằng chứng: Tài liệu quy ước .claude/docs/api-error-code-rules.md có sẵn trong repo, muc 5 liệt kê đúng các anti-pattern đang tồn tại trong Form answer (user_id and line_id empty tra 500, Line user does not exist tra 500, loi nghiep vu tra 200, service tra JsonResponse bi controller boc lai); Tài liệu ghi rõ lỗi nuốt status đã xảy ra thật tại FormAnswerService::checkingNextPage - đã xác nhận lại trong code và sửa; Không chạy được runtime trong container (không có DB/app của LME dựng sẵn cho form answer), mức verify dừng ở lint + đối chiếu tài liệu quy ước

■ TỰ REVIEW (AI)
Chuẩn hoá mã HTTP theo tài liệu quy ước sẵn có, giữ nguyên shape body để không phải sửa nhiều phía trình duyệt. Vòng refix 1: gỡ ràng buộc page_name làm hỏng luồng ảnh nền trang v3 + đưa lỗi thiếu tham số về 400. Bổ sung theo yêu cầu human: rà lại toàn bộ endpoint trong phạm vi ticket và ràng buộc bot đang đăng nhập ngay trong query (BE-coding-rules 4.1) — đây là nhóm lỗi IDOR có thật, nặng nhất là 2 nhánh deleteItem xoá dữ liệu con theo form_id thô và copyFormanswer nhận bot_id từ chính form nguồn.
 • Rủi ro / lưu ý khi test:
   - Trình duyệt còn giữ bản JS cũ trong cache sẽ rơi vào nhánh error mà không có xử lý. Theo rule dự án KHÔNG tự bump version trong config/sns-line.php - cần đội release bump khi phát hành.
   - CỐ Ý KHÔNG đổi contract của API mobile apiGetFormAnswerList (vẫn 200 kèm cờ permission) vì app Flutter đang đọc cờ này.
   - Ràng buộc bot mới thêm sẽ đổi hành vi ở các ca trước đây âm thầm chạy: form/thư mục/trang không thuộc bot hiện tại nay trả 404 thay vì im lặng không đổi gì hoặc sửa nhầm. Nếu nghiệp vụ thật có luồng nhiều bot dùng chung một form (chưa thấy trong code) thì phải xem lại.
   - updatePage tra chủ sở hữu qua JOIN form_answer.bot_id chứ KHÔNG dựa vào cột bot_id của bản ghi trang, để trang cũ có bot_id trống/lệch vẫn sửa được. CHƯA đối chiếu được dữ liệu thật (MySQL dev trên host không kết nối được từ container) - cần kiểm lại khi có DB.
   - store (form v1) đổi chủ sở hữu form mới từ $request->bot_id sang session bot. Blade create truyền đúng bot của session nên luồng thật không đổi, nhưng nếu còn client nào gửi bot_id khác thì form sẽ về bot session.
   - Chưa chạy được kiểm thử runtime trong container, mức verify dừng ở php -l + node --check + đối chiếu tài liệu quy ước. Cần test tay: tạo/lưu/xoá/copy/khôi phục form, đổi tên thư mục, thêm-sửa trang, đặt/xoá ảnh nền trang v3.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_40544 (nhánh gốc release_step_20260827, commit 8d4900408d, 10 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 3 phút 23 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=d2e1ec56-3a60-4dd5-bd1f-01c12be2dec5
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=40544
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
