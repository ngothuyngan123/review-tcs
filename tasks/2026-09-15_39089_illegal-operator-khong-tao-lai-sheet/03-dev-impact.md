# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `8a7af0135a` (1 file, +12/−7). Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39089 |
| Branch | `ai_fixbug_39089` (repo `sns-line`, nhánh gốc `release_step_20260623`) — đã push |
| Ngày submit đánh giá | 2026-08-24 |
| Auto-filled | `2026-09-15 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi liên kết lại Google Spreadsheet cho form bằng **ĐÚNG tài khoản email đã dùng trước đó**, code reset các bản ghi lỗi đồng bộ với điều kiện lọc theo mốc thời gian liên kết cũ (cột `datetime_connect_google_sheet` của bot). Mốc này **có thể rỗng** (thao tác đổi kênh bot xoá cột thời gian nhưng vẫn giữ email tài khoản Google), khi đó câu truy vấn so sánh với giá trị rỗng nên hệ thống ném lỗi `Illegal operator and value combination.`

Lỗi này **không nằm trong khối bắt lỗi Google** nên cả hàm xử lý callback dừng giữa chừng: token đã lưu nhưng **chưa kịp tạo bản ghi yêu cầu tạo sheet**, nên tiến trình định kỳ không có gì để chạy và **form không được tạo lại spreadsheet**.

> Vị trí phát sinh theo stacktrace: `FormAnswerController.php:998` (cũ) — `where('created_at', '>=', $datetime_connect_google_sheet_old)` trong nhánh email trùng.
> Nguồn dữ liệu gây lỗi: `Admin/BotController.php:6596` đặt `datetime_connect_google_sheet = null` nhưng **KHÔNG xoá** `google_sheet_account_email`.

## 2. Cách fix

Sửa hàm xử lý callback liên kết Google Spreadsheet của form (`FormAnswerController::redirectUriGoogleSheet`):

- Tách truy vấn reset bản ghi lỗi đồng bộ ra **biến riêng**.
- **CHỈ áp điều kiện lọc theo mốc thời gian liên kết cũ khi mốc đó có giá trị**.
- Nếu mốc **rỗng** → **reset TOÀN BỘ** bản ghi lỗi đồng bộ sheet của bot để tiến trình định kỳ thử lại.

Nhờ đó luồng liên kết không còn ném lỗi, các bản ghi yêu cầu tạo sheet vẫn được tạo và form được tạo lại spreadsheet.

Dev ghi chú: đã quét tương tự trên **2 repo** — không còn chỗ nào so sánh mốc thời gian liên kết Google có thể rỗng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FormAnswerController::redirectUriGoogleSheet` — `app/Http/Controllers/Basic/FormAnswerController.php:966-1032` | **ĐÃ SỬA** | Nơi phát sinh lỗi — điều kiện lọc theo mốc thời gian rỗng |
| 2 | `FormAnswerController::edit_v2` nhánh unlink-google-sheet — `app/Http/Controllers/Basic/FormAnswerController.php:623-633` | Không sửa | Xoá email nhưng **giữ** mốc thời gian → không sinh lỗi |
| 3 | `Admin/BotController` — thao tác change bot ở màn 「LINE公式アカウント入れ替え」 — `app/Http/Controllers/Admin/BotController.php:6596` | Không sửa | Xoá mốc thời gian nhưng **GIỮ email** = **nguồn gốc dữ liệu gây lỗi** |
| 4 | `CreateGoogleSheetFormAnswerCommand::handle` — `app/Console/Commands/CreateGoogleSheetFormAnswerCommand.php:46-50` | Không sửa | Tiến trình định kỳ đọc bản ghi yêu cầu tạo sheet — **bị mất việc** do lỗi trên |
| 5 | `CalendarSalonController::redirectUriGoogleSheet` — `app/Http/Controllers/Basic/CalendarSalonController.php:2700-2740` | Không sửa | Không có logic reset theo mốc thời gian → không dính lỗi |
| 6 | `CalendarManagementController::redirectUriGoogleSheet` — `app/Http/Controllers/Basic/CalendarManagementController.php:585-625` | Không sửa | Không có logic reset theo mốc thời gian → không dính lỗi |

---

## 4. Đánh giá ảnh hưởng

> ⚠️ Dev báo cáo theo format Auto-fixbug (4.1 = **File thay đổi**, không phải list function). Mục 4.1 dưới đây được map lại theo quy ước repo: `F*` = function impact, giữ nguyên nội dung Dev cung cấp, **không tự thêm impact**.

### 4.1. List function bị ảnh hưởng

**Dev kê (4.1 File thay đổi):** `app/Http/Controllers/Basic/FormAnswerController.php`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FormAnswerController::redirectUriGoogleSheet` — callback OAuth liên kết Google Spreadsheet cho form | `app/Http/Controllers/Basic/FormAnswerController.php:966-1032` | Direct | **File duy nhất bị sửa** (+12/−7). Nhánh email trùng: bỏ điều kiện lọc theo mốc thời gian khi mốc rỗng |
| F2 | `CreateGoogleSheetFormAnswerCommand::handle` — tiến trình định kỳ tạo Google Sheet cho form answer | `app/Console/Commands/CreateGoogleSheetFormAnswerCommand.php:46-50` | Indirect | Không sửa code, nhưng **hành vi đổi**: trước fix không có bản ghi để chạy; sau fix có bản ghi yêu cầu tạo sheet → job tạo được spreadsheet |
| F3 | `Admin/BotController` — thao tác change bot ở màn 「LINE公式アカウント入れ替え」 | `app/Http/Controllers/Admin/BotController.php:6596` | Indirect (nguồn dữ liệu) | Không sửa. Là nơi tạo ra state gây lỗi (`datetime_connect_google_sheet = null` + giữ email) |

### 4.2. List data bị update khi fix bug

**Dev kê:** *Không có — fix chỉ đổi điều kiện lọc khi đọc; các cột được ghi (`result_error_googles.status` / `retry_time` / `next_time_retry`) giữ nguyên ý nghĩa.*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `result_error_googles.status` / `.retry_time` / `.next_time_retry` | UPDATE (reset) | Dev khẳng định **không đổi ý nghĩa cột**, chỉ đổi **phạm vi bản ghi được reset**: mốc thời gian rỗng → reset **toàn bộ** bản ghi lỗi sheet của bot (trước đây: ném lỗi) |
| D2 | `bots.datetime_connect_google_sheet` · `bots.google_sheet_account_email` | READ (điều kiện) | Không bị fix ghi. Là **input quyết định nhánh chạy** — cặp giá trị `email có` + `datetime null` là ca lỗi |
| D3 | Bản ghi **yêu cầu tạo sheet** cho form (do callback tạo sau khi reset) | CREATE | Trước fix: **không được tạo** vì hàm dừng giữa chừng. Sau fix: tạo bình thường → job định kỳ tạo spreadsheet |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

**Dev kê:** Form Builder (FA-011) + Google Sheet sync for form answers.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Form Builder (FA-011)** — luồng liên kết lại Google Spreadsheet cho form: chạy trọn vẹn thay vì lỗi giữa chừng; các form chưa có sheet được tạo lại spreadsheet | F1, D3 | High |
| T2 | **Google Sheet sync for form answers** (ngoài glossary) — bản ghi lỗi đồng bộ câu trả lời form được reset để tiến trình nền thử lại; khi thiếu mốc thời gian liên kết cũ thì **reset toàn bộ lỗi của bot** thay vì ném lỗi | F2, D1 | Medium |
| T3 | **Thao tác change bot ở màn 「LINE公式アカウント入れ替え」** → trạng thái sau đó của liên kết Google Sheet của form | F3, D2 | Medium (không sửa code, nhưng là bước dựng ca lỗi) |

---

## 5. Recover data (Dev kê)

✔ **Không cần recover data.**

## 6. Verify của Dev (mức: lint)

- `php -l app/Http/Controllers/Basic/FormAnswerController.php` → No syntax errors detected.
- `git diff --stat release_step_20260623...ai_fixbug_39089` → 1 file, +12/−7 (chỉ đúng file đã sửa).
- Bằng chứng trace: stacktrace ticket trỏ đúng dòng 998 (cũ); `git log -L` xác nhận điều kiện lọc theo mốc thời gian được thêm ở commit `5181bb8139` `[form] fix update email gg sheet` và **chưa từng có guard rỗng**.

> ⚠️ **Giới hạn verify của Dev** — cần lưu ý khi viết/review TC:
> - **KHÔNG tái hiện được trên dev** (cần luồng OAuth Google thật + DB dev đang tắt).
> - **KHÔNG truy vấn được DB dev** để đếm số bot dính lỗi (`host.docker.internal:3306 Connection refused`) → phạm vi ảnh hưởng thực tế chưa đo được.
> - Verify chỉ dừng ở mức **lint**, chưa có test chạy thật.
> - **Rủi ro Dev tự nêu**: mốc thời gian rỗng → job nền thử lại cả bản ghi lỗi **rất cũ** của bot → thêm lượt gọi Google API.
> - Dev **bỏ qua** một lỗi khác cùng hàm: nhánh không có code gọi `redirect()` mà thiếu `return` (ngoài phạm vi ticket).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
