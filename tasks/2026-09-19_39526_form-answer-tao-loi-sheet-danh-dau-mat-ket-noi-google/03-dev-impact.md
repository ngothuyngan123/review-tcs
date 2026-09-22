# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #39526 — Journal #129266 (AI LME Fix bug, 2026-08-19) + Journal #137196 (AI LME Fix bug, 2026-09-19, **bản mới nhất — dùng làm chuẩn**). Mô tả ticket không có section "Đánh giá ảnh hưởng"; nội dung lấy từ báo cáo AI auto-fixbug trong journal.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) · Assignee Redmine: Kim Cúc |
| Commit / Pull Request | sns-line: commit `8748629bbd` (2026-08-19) → `88307c747a` (2026-09-19, tự review v1). Không có link PR. |
| Branch | `ai_fixbug_39526` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | 2026-09-19 (bản cập nhật; bản đầu 2026-08-19) |
| Auto-filled | 2026-09-19 by /new-task |

> ⚠️ Journal #137196 mâu thuẫn: mục 2 ghi commit `88307c747a` **"CHƯA PUSH — cần push lại branch"**, mục Branch/Commit lại ghi **"[đã push]"**. Cần xác nhận với Dev trước khi test.
>
> ⚠️ Mục 6 VERIFY (`+5 dòng`, commit `8748629bbd`) chưa cập nhật theo commit `88307c747a` — mức verify chỉ là **lint**, không có unit test, không tái hiện trên dev.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Sau khi khách kết nối Google ở màn biểu mẫu, hệ thống ghi từng biểu mẫu vào bảng yêu cầu tạo bảng tính rồi để tiến trình nền chạy mỗi phút tạo file bảng tính cho từng biểu mẫu. Tiến trình nền này khi tạo file lỗi chỉ đánh dấu bản ghi yêu cầu là lỗi rồi thử lại tối đa 3 lần, và không đụng gì tới cờ liên kết Google của bot. Vì vậy khi liên kết Google có vấn đề (khoá truy cập hỏng/bị thu hồi, không đủ quyền), biểu mẫu vĩnh viễn không có mã bảng tính mà màn biểu mẫu vẫn báo đang liên kết bình thường — khách không hề biết để liên kết lại.

## 2. Cách fix

Sửa lại theo hướng dẫn của human (bỏ hoàn toàn hướng sửa ở FormAnswerController của lần trước): chỉ sửa tiến trình nền tạo file bảng tính cho biểu mẫu (CreateGoogleSheetFormAnswerCommand, chạy mỗi phút) — khi tạo file bảng tính lỗi thì ngoài việc đánh dấu bản ghi yêu cầu là lỗi như cũ, nay đánh dấu luôn bot mất liên kết Google, để màn biểu mẫu hiện cảnh báo mời khách liên kết lại thay vì im lặng bỏ qua. Thay đổi gọn trong khối bắt lỗi của vòng lặp, 1 file, 5 dòng.

[Tự review v1 — 2026-09-19] Thêm commit 88307c747a trong cùng job: khi tạo file bảng tính THÀNH CÔNG mà cờ liên kết đang bị đánh dấu mất (=0) thì bật lại (=1), theo đúng quy ước luồng web (FormAnswerController::store/saveV3 set cờ 1 khi createSheet thành công). Lý do: bản fix trước chỉ đặt cờ 0 khi lỗi và không có chỗ nào bật lại, nên một lỗi TẠM THỜI ở lượt thử đầu sẽ khiến khách thấy cảnh báo "mất liên kết Google" vĩnh viễn dù lượt thử lại sau đó tạo bảng tính thành công. Chỉ ghi DB khi cờ đang 0 nên không phát sinh thêm câu update mỗi phút. CHƯA PUSH — cần push lại branch.

**Rủi ro / lưu ý khi test (nguyên văn phần TỰ REVIEW của Dev):**
- Lỗi tạo bảng tính của MỘT biểu mẫu (ví dụ lỗi dữ liệu/tên bảng tính) sẽ đánh dấu cả bot mất liên kết. Đây đúng theo yêu cầu ticket; nếu muốn chặt hơn có thể chỉ đánh dấu khi hết lượt thử lại — cần human quyết định.
- Cờ liên kết không tự bật lại khi lần thử lại sau thành công (chỉ bật lại khi khách liên kết lại hoặc khi lưu biểu mẫu thành công ở luồng web). Ticket không yêu cầu phần này nên giữ nguyên, đã ghi để human xem xét. *(⚠️ ghi chú /new-task: ý này đã lỗi thời — commit `88307c747a` đã bổ sung bật lại cờ, nhưng Dev chưa xoá dòng này trong journal.)*
- Nhánh bot không còn khoá truy cập vẫn để bản ghi yêu cầu treo ở trạng thái đang xử lý (lỗi có sẵn, ngoài phạm vi ticket).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CreateGoogleSheetFormAnswerCommand::handle` (app/Console/Commands/CreateGoogleSheetFormAnswerCommand.php) | **Đã sửa** — khối bắt lỗi tạo file bảng tính (+ nhánh thành công bật lại cờ, commit `88307c747a`) | Điểm fix chính |
| 2 | `App\Console\Kernel::schedule` (app/Console/Kernel.php:197) | Không sửa | Xác nhận lệnh chạy mỗi phút |
| 3 | `FormAnswerController::redirectUriGoogleSheet` | Không sửa | Luồng kết nối Google: ghi biểu mẫu vào bảng yêu cầu tạo bảng tính, bật cờ liên kết |
| 4 | `FormAnswerController::googleSheetActive` | Không sửa | Đọc cờ liên kết để hiện cảnh báo mời liên kết lại |
| 5 | resources/views/basic/form_answer/modal/google_sheet_warning.blade.php | Không sửa | Popup cảnh báo mất liên kết |
| 6 | `FormAnswerController::storeV3` / `saveV3` / `copyFormanswer` | Lần trước có sửa, nay **ĐÃ HOÀN TÁC** theo hướng dẫn human | 3 luồng tạo bảng tính lúc lưu biểu mẫu |
| 7 | `FormAnswerController::index` (FormAnswerController.php:201) | Không sửa (tự review v1 bổ sung) | Màn biểu mẫu BẢN CŨ index_v2 cũng đọc cờ liên kết để hiện banner mời liên kết lại |
| 8 | app/Jobs/AddResultFormAnswerToGoogleSpreadSheet.php:437-471 | Không sửa (tự review v1 bổ sung) | Nguồn GHI cờ liên kết thứ hai (đồng bộ câu trả lời), chỉ đánh dấu mất liên kết với lỗi 401/UNAUTHENTICATED/400; là chuẩn phân loại lỗi sẵn có để đối chiếu |
| 9 | `FormAnswerController::cancelGoogsheet` (FormAnswerController.php:5512) | Không sửa (tự review v1 bổ sung) | Đọc trạng thái bản ghi yêu cầu tạo bảng tính để chặn huỷ liên kết |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CreateGoogleSheetFormAnswerCommand::handle` (job `form-answer:create-google-sheet`, chạy mỗi phút) | app/Console/Commands/CreateGoogleSheetFormAnswerCommand.php | Direct | File thay đổi duy nhất (Dev mục 4.1). Nhánh lỗi ⇒ cờ 0; nhánh thành công khi cờ đang 0 ⇒ cờ 1 |

<!-- /new-task: Dev chỉ kê 1 file ở mục 4.1. Các function đọc/ghi cùng cờ (FormAnswerController::googleSheetActive / index / redirectUriGoogleSheet, job AddResultFormAnswerToGoogleSpreadSheet) nằm ở mục 3, không được Dev đánh mã F. -->

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bots.google_sheet_status` | UPDATE | Đặt về 0 (mất liên kết) khi tiến trình nền tạo file bảng tính cho biểu mẫu bị lỗi; và (tự review v1) đặt lại 1 khi tạo bảng tính thành công mà cờ đang là 0. Không thêm/bớt bản ghi nào khác |
| D2 | `form_answer_connect_googles` (trạng thái/thông điệp/số lượt thử lại) | — (không đổi) | KHÔNG đổi bởi bản fix, giữ nguyên logic cũ |
| D3 | `form_answer.google_sheet_id` | — (gián tiếp) | Không đổi trực tiếp; gián tiếp: khách được mời liên kết lại nên luồng tạo bảng tính có thể chạy lại cho biểu mẫu còn thiếu |

Recover data: ✔ Không cần recover data.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Form Builder (FA-011) — tạo file bảng tính cho biểu mẫu sau khi kết nối Google: lỗi tạo file nay báo cho khách qua cảnh báo mất liên kết | F1, D1 | <Dev không ghi> |
| T2 | Google Spreadsheet linkage for Form (outside glossary) — cờ liên kết Google của bot dùng cho cảnh báo mời liên kết lại trên màn biểu mẫu | D1 | <Dev không ghi> |
| T3 | Màn biểu mẫu BẢN CŨ (index_v2, cùng Form Builder FA-011) — cũng đọc cờ liên kết để hiện banner mời liên kết lại (tự review v1 bổ sung) | D1 | <Dev không ghi> |
| T4 | Đồng bộ câu trả lời biểu mẫu sang Google Sheet (job AddResultFormAnswerToGoogleSpreadSheet) — dùng chung cờ nhưng KHÔNG đọc cờ trước khi ghi, nên đặt cờ 0 KHÔNG chặn đồng bộ câu trả lời (tự review v1 xác minh) | D1 | <Dev không ghi> |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
