# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39089 — Exception Illegal operator and value combination. => không tạo lại sheet khi connect` |
| Module / Màn hình | Form Builder (FA-011) — luồng liên kết Google Spreadsheet cho form (callback OAuth `FormAnswerController::redirectUriGoogleSheet`) |

## Mô tả bug (bản dịch tiếng Việt)

Hệ thống ném exception `Illegal operator and value combination.` khi xử lý callback liên kết Google Spreadsheet cho form ⇒ **không tạo lại sheet khi connect**.

Log lỗi (nguyên văn từ ticket):

```
Illegal operator and value combination. {"exception":"[object] (InvalidArgumentException(code: 0): Illegal operator and value combination. at /var/www/html/sns-line/vendor/laravel/framework/src/Illuminate/Database/Query/Builder.php:591)
[stacktrace]
#0 /var/www/html/sns-line/vendor/laravel/framework/src/Illuminate/Database/Query/Builder.php(501): Illuminate\\Database\\Query\\Builder->prepareValueAndOperator(NULL, '>=', false)
#1 /var/www/html/sns-line/vendor/laravel/framework/src/Illuminate/Database/Eloquent/Builder.php(226): Illuminate\\Database\\Query\\Builder->where('created_at', '>=', NULL)
#2 /var/www/html/sns-line/app/Http/Controllers/Basic/FormAnswerController.php(998): Illuminate\\Database\\Eloquent\\Builder->where('created_at', '>=', NULL)
#3 [internal function]: App\\Http\\Controllers\\Basic\\FormAnswerController->redirectUriGoogleSheet(Object(Illuminate\\Http\\Request))
```

Diễn giải theo stacktrace: truy vấn `where('created_at', '>=', NULL)` — so sánh với mốc thời gian liên kết Google cũ (`datetime_connect_google_sheet` của bot) khi giá trị này rỗng.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket thuộc tracker "Bug tự detect", sinh từ log exception. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — stacktrace nằm ngay trong Description (không có file attachment)

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — ticket thuộc tracker **Bug tự detect** (sinh từ log exception), không có steps / expected / actual. Root cause đã được Dev (AI Auto-fixbug) confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.
- **Điều kiện tiên quyết để dựng ca lỗi** (suy từ mục 1 + 3 của Dev — cần verify lại khi test):
  1. Bot đã từng liên kết Google Spreadsheet cho form bằng email Google `A` → bot có `google_sheet_account_email = A` và `datetime_connect_google_sheet` có giá trị.
  2. Thực hiện **thao tác change bot ở màn 「LINE公式アカウント入れ替え」** (code: `Admin/BotController` dòng 6596): thao tác này **xoá `datetime_connect_google_sheet` (= null)** nhưng **GIỮ nguyên `google_sheet_account_email = A`** → đây là nguồn dữ liệu gây lỗi.
  3. Vào form → liên kết lại Google Spreadsheet bằng **ĐÚNG email `A`** (trùng email cũ → rơi vào nhánh có điều kiện lọc theo mốc thời gian) → exception.
- **Cần OAuth Google thật** để chạy luồng callback — Dev ghi rõ *không tái hiện được trên dev* (DB dev tắt + cần luồng OAuth Google thật). Test phải làm trên môi trường có Google OAuth hoạt động.
- Dev **không truy vấn được DB dev** để đếm số bot dính lỗi → kết luận dựa trên đọc code + stacktrace. Chưa có số liệu phạm vi ảnh hưởng thực tế.
- **Rủi ro Dev tự nêu khi test**: khi mốc thời gian liên kết cũ rỗng, tiến trình nền sẽ thử lại **cả các bản ghi lỗi đồng bộ rất cũ** của bot đó → phát sinh thêm lượt gọi Google API. Dev khẳng định không mất / ghi sai dữ liệu, bản ghi nào lỗi thật sẽ quay lại trạng thái lỗi như cũ.
- Dev tự ghi nhận **bỏ qua một lỗi nhỏ khác cùng hàm**: nhánh không có code gọi `redirect()` mà thiếu `return` — ngoài phạm vi ticket, chưa fix.
- Status Redmine: **Fix done - Đợi test**. Branch: `ai_fixbug_39089` (repo sns-line).

## Journal / note từ Redmine (nguyên văn)

**Journal #132552 — AI LME Fix bug — 2026-08-24:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi liên kết lại Google Spreadsheet cho form bằng ĐÚNG tài khoản email đã dùng trước đó, code reset các bản ghi lỗi đồng bộ với điều kiện lọc theo mốc thời gian liên kết cũ (cột datetime_connect_google_sheet của bot). Mốc này có thể rỗng (thao tác đổi kênh bot xoá cột thời gian nhưng vẫn giữ email tài khoản Google), khi đó câu truy vấn so sánh với giá trị rỗng nên hệ thống ném lỗi Illegal operator and value combination. Lỗi này không nằm trong khối bắt lỗi Google nên cả hàm xử lý callback dừng giữa chừng: token đã lưu nhưng chưa kịp tạo bản ghi yêu cầu tạo sheet, nên tiến trình định kỳ không có gì để chạy và form không được tạo lại spreadsheet.

■ 2. CÁCH FIX
Sửa hàm xử lý callback liên kết Google Spreadsheet của form (FormAnswerController::redirectUriGoogleSheet): tách truy vấn reset bản ghi lỗi đồng bộ ra biến riêng và CHỈ áp điều kiện lọc theo mốc thời gian liên kết cũ khi mốc đó có giá trị; nếu mốc rỗng thì reset toàn bộ bản ghi lỗi đồng bộ sheet của bot để tiến trình định kỳ thử lại. Nhờ đó luồng liên kết không còn ném lỗi, các bản ghi yêu cầu tạo sheet vẫn được tạo và form được tạo lại spreadsheet. Quét tương tự trên 2 repo: không còn chỗ nào so sánh mốc thời gian liên kết Google có thể rỗng.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
FormAnswerController::redirectUriGoogleSheet (app/Http/Controllers/Basic/FormAnswerController.php:966-1032 — nơi phát sinh lỗi, đã sửa)
FormAnswerController::edit_v2 nhánh unlink-google-sheet (app/Http/Controllers/Basic/FormAnswerController.php:623-633 — xoá email nhưng giữ mốc thời gian, không sinh lỗi)
Admin/BotController thiết lập đổi kênh bot (app/Http/Controllers/Admin/BotController.php:6596 — xoá mốc thời gian nhưng GIỮ email = nguồn gốc dữ liệu gây lỗi)
CreateGoogleSheetFormAnswerCommand::handle (app/Console/Commands/CreateGoogleSheetFormAnswerCommand.php:46-50 — tiến trình định kỳ đọc bản ghi yêu cầu tạo sheet, bị mất việc do lỗi trên)
CalendarSalonController::redirectUriGoogleSheet (app/Http/Controllers/Basic/CalendarSalonController.php:2700-2740 — không có logic reset theo mốc thời gian, không dính lỗi)
CalendarManagementController::redirectUriGoogleSheet (app/Http/Controllers/Basic/CalendarManagementController.php:585-625 — không có logic reset theo mốc thời gian, không dính lỗi)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/FormAnswerController.php
 • 4.2 Data ảnh hưởng:
   - Không có — fix chỉ đổi điều kiện lọc khi đọc; các cột được ghi (result_error_googles.status/retry_time/next_time_retry) giữ nguyên ý nghĩa
 • 4.3 Tính năng liên quan:
   - Form Builder (FA-011) — luồng liên kết lại Google Spreadsheet cho form: chạy trọn vẹn thay vì lỗi giữa chừng, các form chưa có sheet được tạo lại spreadsheet
   - Google Sheet sync for form answers (outside glossary) — bản ghi lỗi đồng bộ câu trả lời form được reset để tiến trình nền thử lại; khi thiếu mốc thời gian liên kết cũ thì reset toàn bộ lỗi của bot thay vì ném lỗi

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Basic/FormAnswerController.php: No syntax errors detected; git diff --stat release_step_20260623...ai_fixbug_39089: 1 file, +12/-7 (chỉ đúng file đã sửa)
   Bằng chứng: Stacktrace ticket trỏ đúng dòng 998 (cũ) = where('created_at','>=',$datetime_connect_google_sheet_old) trong nhánh email trùng; git log -L xác nhận điều kiện lọc theo mốc thời gian được thêm ở commit 5181bb8139 '[form] fix update email gg sheet' và chưa từng có guard rỗng; Nguồn dữ liệu gây lỗi: Admin/BotController.php:6596 đặt datetime_connect_google_sheet = null nhưng KHÔNG xoá google_sheet_account_email → lần liên kết lại cùng email rơi vào nhánh else và so sánh với giá trị rỗng; Không truy vấn được DB dev để đếm số bot dính (host.docker.internal:3306 Connection refused) — kết luận dựa trên đọc code + stacktrace; Không tái hiện được trên dev (cần luồng OAuth Google thật + DB dev đang tắt)

■ TỰ REVIEW (AI)
Fix tối thiểu, đúng root cause theo stacktrace: chỉ bọc điều kiện lọc theo mốc thời gian bằng kiểm tra rỗng, không đổi luồng OAuth, không đổi phần tạo bản ghi yêu cầu tạo sheet. Khi mốc thời gian rỗng thì reset toàn bộ bản ghi lỗi đồng bộ sheet của bot — đúng ý đồ ban đầu (liên kết lại để các câu trả lời lỗi được đồng bộ lại) và là lựa chọn an toàn vì không biết mốc cũ. Đã bỏ qua một lỗi nhỏ khác cùng hàm (nhánh không có code: gọi redirect() mà thiếu return) vì ngoài phạm vi ticket và không liên quan root cause.
 • Rủi ro / lưu ý khi test:
   - Khi mốc thời gian liên kết cũ rỗng, tiến trình nền sẽ thử lại cả các bản ghi lỗi rất cũ của bot đó → phát sinh thêm vài lượt gọi Google API; không mất/ghi sai dữ liệu, lỗi nào hỏng thật sẽ quay lại trạng thái lỗi như cũ
   - Không tái hiện được trên dev (cần OAuth Google thật, DB dev đang tắt) — độ tin cậy dựa trên stacktrace khớp chính xác dòng code và đường dữ liệu đã truy được

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_39089 (nhánh gốc release_step_20260623, commit 8a7af0135a, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 5 phút 30 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=3a3fd1cd-0477-4ed6-9b51-778a68be2a7e
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39089
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
