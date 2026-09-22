# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40835 — Thêm timeout 5s khi request google sheet` |
| Module / Màn hình | `<chưa rõ — tester fill>` — Redmine không set category. Suy từ mô tả: lớp dịch vụ dùng chung `GoogleSheetService` (`app/Helpers/GoogleSheetService.php`), ảnh hưởng 4 tính năng gọi Google スプレッドシート: Form Builder (FA-011) · QR Code Action / Landing (FA-017) · Lesson / Calendar Booking (FA-019) · Salon Booking (FA-020) |

## Mô tả bug (bản dịch tiếng Việt)

Thêm timeout 5s khi request google sheet.

> ⚠️ Đây là ticket tracker **SpecImprove** (cải tiến spec), KHÔNG phải bug report từ khách hàng. Description Redmine chỉ có đúng 1 dòng trùng với tiêu đề — không có mô tả hiện tượng, không có steps, không có người báo lỗi.
>
> Bối cảnh kỹ thuật (lấy từ Journal #135755 — báo cáo AI Auto-fixbug, nguyên văn ở cuối file):
> Client HTTP dùng chung để gọi Google Sheet API được tạo mà **không khai báo timeout** → mặc định chờ vô hạn. Khi Google スプレッドシート phản hồi chậm hoặc treo, tiến trình web/job bị giữ cho tới khi PHP hoặc hàng đợi kill, **không sinh lỗi rõ ràng** để xử lý.

## Steps to reproduce

<!-- Ticket KHÔNG có Section "Tái hiện bug" — SpecImprove, không tái hiện bằng thao tác người dùng thường. -->

## Expected result

<!-- Ticket không ghi. -->

## Actual result

<!-- Ticket không ghi. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40835 KHÔNG có attachment nào. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — ticket dạng SpecImprove, không có Section "Tái hiện bug" (Steps / Expected / Actual trống). Root cause + cách fix do AI Auto-fixbug xác định và đã tự verify runtime (xem file 03). TCs nên tập trung **verify cách fix + regression impact**, không phải verify hiện tượng bug.

**Điều kiện tiên quyết để test:**

- Branch fix: `ai_fixbug_40835` (repo `sns-line`, nhánh gốc `release_step_20260827`, commit `5dab615d43`, đúng **1 file** thay đổi).
- Cần **mô phỏng được Google スプレッドシート treo / chậm** (IP không định tuyến, proxy delay, hoặc chặn `sheets.googleapis.com`) — đây là điều kiện bắt buộc của phần lớn TC; không dựng được thì không verify được fix.
- Cần **tài khoản Google thật đã liên kết** cho luồng normal (liên kết sheet / tạo sheet / ghi dữ liệu) để xác nhận không bị timeout oan.
- Ngưỡng cần đo quanh mốc **5 giây** (cả `connect_timeout` lẫn `timeout` tổng) → cần công cụ đo thời gian, không quan sát bằng mắt.

**Đánh đổi Dev đã nêu (Leader lưu ý khi duyệt kết quả test):**

- Request sheet đang mất **hơn 5 giây** (sheet rất lớn, mạng chậm, Google chậm) nay **thất bại thay vì chờ tới khi xong** — đúng ý ticket, nhưng cần theo dõi log đồng bộ biểu mẫu vài ngày sau khi lên.
- **Không thêm retry** (ticket không yêu cầu). Với job đồng bộ câu trả lời biểu mẫu, lỗi timeout không phải lỗi JSON của Google → rơi vào nhánh **không ghi bản ghi retry** (hành vi sẵn có), chỉ ghi log.
- Đường làm mới token chạy **ngầm bên trong thư viện Google** (`createAuthHttp`) dựng client riêng chỉ mang `base_uri`/`verify`/`proxy` nên **KHÔNG nhận timeout này** — mã vendor, không sửa → **vẫn còn khả năng treo ở nhánh này**.
- **Job Java** cũng gọi Google Sheet nhưng theo rule chỉ sửa PHP nên **chưa đụng** → luồng đồng bộ câu trả lời form phía Java không có timeout.
- Client Google khác (**Google カレンダー, Gmail**) cũng thiếu timeout theo cùng kiểu nhưng **ngoài phạm vi ticket** → là đối chứng âm, không phải GAP.

## Journal / note từ Redmine (nguyên văn)

**Journal #135755 — AI LME Fix bug — 2026-09-10:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Client HTTP dùng chung để gọi Google Sheet API được tạo mà không khai báo timeout, nên mặc định là chờ vô hạn. Google Sheet phản hồi chậm hoặc treo sẽ giữ tiến trình web/job cho tới khi bị PHP hoặc hàng đợi kill, không sinh lỗi rõ ràng để xử lý.

■ 2. CÁCH FIX
Khai báo timeout 5 giây (cả thời gian mở kết nối lẫn tổng thời gian một request) cho client HTTP dùng chung gọi Google Sheet API, đặt tại điểm tạo client duy nhất trong lớp dịch vụ Google Sheet. Nhờ đó mọi luồng gọi sheet (đồng bộ câu trả lời biểu mẫu, đặt lịch bài học, đặt lịch salon, trang đích/QR, tạo sheet, đổi tên sheet, làm mới token) đều dừng sau 5 giây thay vì chờ vô hạn. Quét ngang: các client Google khác (lịch Google, Gmail) cũng thiếu timeout theo cùng kiểu nhưng không phải Google Sheet nên để ngoài phạm vi ticket.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
GoogleSheetService::__construct (app/Helpers/GoogleSheetService.php) — nơi duy nhất tạo client HTTP cho Google Sheet
GoogleSheetService::getClient (app/Helpers/GoogleSheetService.php) — gắn client HTTP vào Google_Client
GoogleSheetService::getClientAuthFromAccessToken / createAuthClientFromAuthCode (app/Helpers/GoogleSheetService.php) — đều dùng lại getClient
GoogleSheetService::checkAccessToken (app/Helpers/GoogleSheetService.php) — làm mới access token qua cùng client HTTP
CalendarGoogleSheetService (app/Services/CalendarManagement/CalendarGoogleSheetService.php) — mọi client lấy từ GoogleSheetService
CalendarSalonGoogleSheetService (app/Services/CalendarSalon/CalendarSalonGoogleSheetService.php) — mọi client lấy từ GoogleSheetService
LandingGoogleSheetService (app/Services/Landing/LandingGoogleSheetService.php) — mọi client lấy từ GoogleSheetService
AddResultFormAnswerToGoogleSpreadSheet::getGoogleSheetClient (app/Jobs/AddResultFormAnswerToGoogleSpreadSheet.php) — job đồng bộ câu trả lời biểu mẫu
Google_Client::authorize + Google_AuthHandler_Guzzle6AuthHandler::attachToken (vendor) — xác nhận cấu hình timeout được giữ lại khi tạo client đã gắn token
Google_Http_REST::doExecute + Guzzle6HttpHandler::__invoke (vendor) — xác nhận request gửi không truyền option riêng nên dùng mặc định của client

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Helpers/GoogleSheetService.php
 • 4.2 Data ảnh hưởng:
   - Không có — thay đổi thuần cấu hình client HTTP, không đụng bảng hay cột nào
 • 4.3 Tính năng liên quan:
   - Form Builder (FA-011) — đồng bộ câu trả lời biểu mẫu sang Google Sheet nay dừng sau 5 giây thay vì treo
   - QR Code Action / Landing (FA-017) — đồng bộ số liệu trang đích/QR sang Google Sheet bị giới hạn 5 giây
   - Lesson / Calendar Booking (FA-019) — đồng bộ đặt lịch bài học sang Google Sheet bị giới hạn 5 giây
   - Salon Booking (FA-020) — đồng bộ đặt lịch salon sang Google Sheet bị giới hạn 5 giây

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: runtime-data
   Lệnh: php -l app/Helpers/GoogleSheetService.php: No syntax errors detected; Bootstrap Laravel + reflection trên client HTTP dùng chung: timeout=5, connect_timeout=5; Bootstrap Laravel + getClientAuthFromAccessToken(token giả) rồi Google_Client::authorize(): client sau khi gắn token vẫn timeout=5, connect_timeout=5 (chứng minh cấu hình không bị mất qua lớp auth của thư viện Google); Guzzle với đúng cấu hình này gọi IP không định tuyến: ném lỗi sau 5.03 giây (trước đây sẽ chờ vô hạn)
   Bằng chứng: Toàn bộ đường gọi Google Sheet trong sns-line đều lấy client qua GoogleSheetService::getInstance() (kiểm bằng git grep: chỉ 1 chỗ new Google_Client cho Sheets, không có lời gọi trực tiếp tới sheets.googleapis.com); Google_AuthHandler_Guzzle6AuthHandler::attachToken/attachCredentials dựng client mới từ $http->getConfig() nên giữ nguyên timeout; Guzzle6HttpHandler::__invoke gọi $client->send($request, []) — không option riêng, nên dùng mặc định của client

■ TỰ REVIEW (AI)
Thay đổi gói gọn trong 1 điểm tạo client HTTP duy nhất của Google Sheet nên phủ hết mọi luồng gọi sheet mà không cần sửa từng nơi gọi. Đã kiểm chứng bằng chạy thật rằng timeout được giữ lại sau khi thư viện Google dựng lại client kèm token, và request thật sự bị hủy ở mốc 5 giây.
 • Rủi ro / lưu ý khi test:
   - Request sheet đang mất hơn 5 giây (sheet rất lớn, mạng chậm, Google chậm) nay sẽ thất bại thay vì chờ tới khi xong — đây đúng là đánh đổi ticket yêu cầu, nhưng nên theo dõi log đồng bộ biểu mẫu vài ngày sau khi lên.
   - Ticket không yêu cầu thêm retry nên không thêm. Với job đồng bộ câu trả lời biểu mẫu, lỗi timeout không phải lỗi JSON của Google nên rơi vào nhánh không ghi bản ghi retry (hành vi sẵn có) — chỉ ghi log. Nếu muốn tự động thử lại khi timeout thì cần một ticket riêng.
   - Đường làm mới token chạy ngầm bên trong thư viện Google (createAuthHttp) dựng client riêng chỉ mang base_uri/verify/proxy nên KHÔNG nhận timeout này — thuộc mã vendor, không sửa. Đường làm mới token do code mình gọi (checkAccessToken) thì có timeout.
   - Phần job Java cũng gọi Google Sheet nhưng theo rule chỉ sửa PHP nên chưa đụng.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_40835 (nhánh gốc release_step_20260827, commit 5dab615d43, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 5 phút 39 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=6afe4b3c-1d06-48a8-beeb-6ba5a9137192
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=40835
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
