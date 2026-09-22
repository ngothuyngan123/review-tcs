# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `sns-line` commit `5dab615d43` (1 file) · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=40835 |
| Branch | `ai_fixbug_40835` (nhánh gốc `release_step_20260827`) — đã push lên origin |
| Ngày submit đánh giá | `2026-09-10` (Journal #135755) |
| Auto-filled | `2026-09-11 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Client HTTP dùng chung để gọi Google Sheet API được tạo mà **không khai báo timeout**, nên mặc định là **chờ vô hạn**. Google Sheet phản hồi chậm hoặc treo sẽ giữ tiến trình web/job cho tới khi bị PHP hoặc hàng đợi kill, **không sinh lỗi rõ ràng** để xử lý.

## 2. Cách fix

Khai báo timeout **5 giây** (cả thời gian mở kết nối `connect_timeout` lẫn tổng thời gian một request `timeout`) cho client HTTP dùng chung gọi Google Sheet API, đặt tại **điểm tạo client duy nhất** trong lớp dịch vụ Google Sheet.

Nhờ đó mọi luồng gọi sheet đều dừng sau 5 giây thay vì chờ vô hạn:
- đồng bộ câu trả lời biểu mẫu
- đặt lịch bài học (lesson booking)
- đặt lịch salon
- trang đích / QR
- tạo sheet
- đổi tên sheet
- làm mới token

**Quét ngang (Dev tự ghi):** các client Google khác (**lịch Google, Gmail**) cũng thiếu timeout theo cùng kiểu nhưng không phải Google Sheet nên **để ngoài phạm vi ticket**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `GoogleSheetService::__construct` — `app/Helpers/GoogleSheetService.php` | **CÓ SỬA** — thêm `timeout=5`, `connect_timeout=5` | Nơi **duy nhất** tạo client HTTP cho Google Sheet |
| 2 | `GoogleSheetService::getClient` — `app/Helpers/GoogleSheetService.php` | Không sửa (chỉ check) | Gắn client HTTP vào `Google_Client` |
| 3 | `GoogleSheetService::getClientAuthFromAccessToken` / `createAuthClientFromAuthCode` — `app/Helpers/GoogleSheetService.php` | Không sửa (chỉ check) | Đều dùng lại `getClient` |
| 4 | `GoogleSheetService::checkAccessToken` — `app/Helpers/GoogleSheetService.php` | Không sửa (chỉ check) | Làm mới access token qua cùng client HTTP |
| 5 | `CalendarGoogleSheetService` — `app/Services/CalendarManagement/CalendarGoogleSheetService.php` | Không sửa (chỉ check) | Mọi client lấy từ `GoogleSheetService` |
| 6 | `CalendarSalonGoogleSheetService` — `app/Services/CalendarSalon/CalendarSalonGoogleSheetService.php` | Không sửa (chỉ check) | Mọi client lấy từ `GoogleSheetService` |
| 7 | `LandingGoogleSheetService` — `app/Services/Landing/LandingGoogleSheetService.php` | Không sửa (chỉ check) | Mọi client lấy từ `GoogleSheetService` |
| 8 | `AddResultFormAnswerToGoogleSpreadSheet::getGoogleSheetClient` — `app/Jobs/AddResultFormAnswerToGoogleSpreadSheet.php` | Không sửa (chỉ check) | Job đồng bộ câu trả lời biểu mẫu |
| 9 | `Google_Client::authorize` + `Google_AuthHandler_Guzzle6AuthHandler::attachToken` (vendor) | Không sửa (chỉ check) | Xác nhận cấu hình timeout **được giữ lại** khi tạo client đã gắn token |
| 10 | `Google_Http_REST::doExecute` + `Guzzle6HttpHandler::__invoke` (vendor) | Không sửa (chỉ check) | Xác nhận request gửi **không truyền option riêng** nên dùng mặc định của client |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev chỉ ghi **"4.1 File thay đổi"**, KHÔNG kê bảng function `F1/F2/...`. Bảng dưới do `/new-task` suy từ mục 3 (danh sách function Dev đã check) — **tester verify lại trước khi dùng làm base coverage**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `GoogleSheetService::__construct` (điểm tạo client HTTP duy nhất) | `app/Helpers/GoogleSheetService.php` | **Direct** — file duy nhất thay đổi | Thêm `timeout=5` + `connect_timeout=5` |
| F2 | `GoogleSheetService::getClient` / `getClientAuthFromAccessToken` / `createAuthClientFromAuthCode` | `app/Helpers/GoogleSheetService.php` | Indirect | Nhận client đã có timeout |
| F3 | `GoogleSheetService::checkAccessToken` (làm mới access token do code mình gọi) | `app/Helpers/GoogleSheetService.php` | Indirect | **CÓ** timeout |
| F4 | `CalendarGoogleSheetService` (lesson booking) | `app/Services/CalendarManagement/CalendarGoogleSheetService.php` | Indirect | Mọi client lấy từ `GoogleSheetService` |
| F5 | `CalendarSalonGoogleSheetService` (salon booking) | `app/Services/CalendarSalon/CalendarSalonGoogleSheetService.php` | Indirect | Mọi client lấy từ `GoogleSheetService` |
| F6 | `LandingGoogleSheetService` (landing / QR) | `app/Services/Landing/LandingGoogleSheetService.php` | Indirect | Mọi client lấy từ `GoogleSheetService` |
| F7 | `AddResultFormAnswerToGoogleSpreadSheet::getGoogleSheetClient` (job đồng bộ câu trả lời form) | `app/Jobs/AddResultFormAnswerToGoogleSpreadSheet.php` | Indirect | Timeout không sinh bản ghi retry (hành vi sẵn có) |
| F8 | `Google_AuthHandler_Guzzle6AuthHandler::createAuthHttp` — nhánh **thư viện tự làm mới token** | vendor (`google/apiclient`) | **KHÔNG nhận timeout** | ⚠️ Dev tự nêu: client nội bộ chỉ mang `base_uri`/`verify`/`proxy` → **vẫn có thể treo vô hạn**. Mã vendor, không sửa |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** | — | Dev ghi nguyên văn: "thay đổi thuần cấu hình client HTTP, không đụng bảng hay cột nào" |

> ⚠️ Tuy không có data **bị fix sửa**, nhưng timeout làm **thay đổi kết quả ghi data** ở các luồng đồng bộ: bản ghi trên Google Sheet có thể **không được ghi** khi timeout, trong khi data gốc phía LME vẫn còn → **lệch đồng bộ**. Đây là vùng cần TC, không phải "không ảnh hưởng data".

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Form Builder (FA-011)** — đồng bộ câu trả lời biểu mẫu sang Google Sheet nay dừng sau 5 giây thay vì treo | F1, F7 | High |
| T2 | **QR Code Action / Landing (FA-017)** — đồng bộ số liệu trang đích/QR sang Google Sheet bị giới hạn 5 giây | F1, F6 | High |
| T3 | **Lesson / Calendar Booking (FA-019)** — đồng bộ đặt lịch bài học sang Google Sheet bị giới hạn 5 giây | F1, F4 | High |
| T4 | **Salon Booking (FA-020)** — đồng bộ đặt lịch salon sang Google Sheet bị giới hạn 5 giây | F1, F5 | High |

---

## Ghi chú bổ sung từ Dev (mục 5 / 6 / tự review — không có trong template gốc)

**5. RECOVER DATA:** ✔ Không cần recover data.

**6. VERIFY (Dev tự chạy, mức `runtime-data`):**
- `php -l app/Helpers/GoogleSheetService.php` — No syntax errors detected
- Bootstrap Laravel + reflection trên client HTTP dùng chung: `timeout=5`, `connect_timeout=5`
- Bootstrap Laravel + `getClientAuthFromAccessToken(token giả)` rồi `Google_Client::authorize()`: client sau khi gắn token **vẫn** `timeout=5`, `connect_timeout=5` (chứng minh cấu hình không mất qua lớp auth của thư viện Google)
- Guzzle với đúng cấu hình này gọi IP không định tuyến: **ném lỗi sau 5.03 giây** (trước đây chờ vô hạn)
- `git grep`: chỉ **1 chỗ** `new Google_Client` cho Sheets, không có lời gọi trực tiếp tới `sheets.googleapis.com`

**Rủi ro / lưu ý khi test (Dev tự nêu — 4 điểm):**

| # | Rủi ro | Ảnh hưởng tới TC |
|---|---|---|
| R1 | Request sheet đang mất **> 5 giây** (sheet rất lớn, mạng chậm, Google chậm) nay **thất bại** thay vì chờ xong | Cần TC đo thời gian ghi dữ liệu lớn để biết ngưỡng 5s có cắt nhầm thao tác hợp lệ không |
| R2 | **Không thêm retry.** Job đồng bộ câu trả lời biểu mẫu: lỗi timeout ≠ lỗi JSON của Google → rơi vào nhánh **không ghi bản ghi retry** (hành vi sẵn có), chỉ ghi log | Cần TC xác nhận hành vi retry/không-retry sau timeout, và log đủ truy vết |
| R3 | Nhánh **thư viện tự làm mới token** (`createAuthHttp`) dựng client riêng **KHÔNG nhận timeout** — mã vendor, không sửa | ⚠️ **Fix có thể chưa phủ hết**. Cần TC chạy thật với token hết hạn để xác minh nhánh này còn treo không → treo thì báo Dev |
| R4 | **Job Java** cũng gọi Google Sheet nhưng theo rule chỉ sửa PHP nên **chưa đụng** | Luồng đồng bộ form phía Java không có timeout — cần xác nhận không regression + ghi nhận GAP ngoài phạm vi |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ bảng F1–F8 do `/new-task` suy ra, Dev KHÔNG tự kê
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — ⚠️ Dev ghi "không có data", cần cân nhắc lệch đồng bộ Sheet
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
