# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #37645 — Journal #131642 (AI LME Fix bug, 2026-08-21), báo cáo **AI Auto-fixbug LME**.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `f50f62c6e5` (3 file) — repo `sns-line`, đã push. Không có link PR trong ticket. |
| Branch | `ai_fixbug_37645` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | 2026-08-21 |
| Auto-filled | `2026-09-14 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn liên kết Google Spreadsheet của QR code action chỉ dựa vào việc token lưu trong cơ sở dữ liệu có rỗng hay không để quyết định hiển thị. Khi khách vào tài khoản Google gỡ quyền truy cập, token cũ vẫn còn trong cơ sở dữ liệu nên màn vẫn hiện đang kết nối, không có cảnh báo hay nút liên kết lại. Các tính năng khác (form trả lời, đặt lịch) có cờ báo lỗi kết nối để hiện cảnh báo, riêng QR code action không có cờ nào tương đương.

## 2. Cách fix

Sửa theo AI review vòng 1: khi phát hiện quyền Google bị gỡ, màn KHÔNG thay thế khối tài khoản đang kết nối nữa mà giữ nguyên toàn bộ giao diện cũ (gồm nút Googleアカウントの接続を解除する) và chỉ hiện THÊM một hộp thoại cảnh báo đè lên màn — đúng mẫu đã có ở màn đặt lịch và form trả lời: tiêu đề Googleスプレッドシートの連携が解除されました, nút 再連携する và lựa chọn 再連携せずにこの画面を閉じる. Controller tách riêng đường dẫn liên kết lại (google_sheet_auth_url_reconnect) khỏi biến google_sheet_auth_url cũ, nên hai điều kiện hiển thị sẵn có trong blade giữ nguyên hành vi như trước khi sửa; nhờ vậy khách vẫn bấm được hủy liên kết để xóa cả mã bảng tính cũ trước khi liên kết bằng tài khoản Google khác.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn mục ■ 3 của journal (Dev list dạng plain, convert sang bảng). Cột "Thay đổi" journal KHÔNG ghi rõ cho từng function.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `QRCodeController::linkGoogle` — `app/Http/Controllers/Basic/QRCodeController.php` | `<Dev không ghi rõ>` — file nằm trong danh sách 4.1 (đã sửa) | Điểm hiển thị màn liên kết; tách `google_sheet_auth_url_reconnect` khỏi `google_sheet_auth_url` |
| 2 | `QRCodeController::redirectUriGoogleSheet` — `app/Http/Controllers/Basic/QRCodeController.php` | `<Dev không ghi rõ>` | Đường quay về sau khi cấp quyền lại |
| 3 | `QRCodeController::cancelGoogleSheet` — `app/Http/Controllers/Basic/QRCodeController.php` | `<Dev không ghi rõ>` | Giữ được thao tác hủy liên kết khi đang bị gỡ quyền |
| 4 | `LandingGoogleSheetService::isConnectionRevoked` — `app/Services/Landing/LandingGoogleSheetService.php` | `<Dev không ghi rõ>` — file nằm trong danh sách 4.1 (đã sửa) | Hàm phát hiện trạng thái bị gỡ quyền |
| 5 | `LandingGoogleSheetService::insertDataToGoogleSheet` — `app/Services/Landing/LandingGoogleSheetService.php` | `<Dev không ghi rõ>` | Luồng ghi dữ liệu vào spreadsheet, dùng chung service |
| 6 | `GoogleSheetService::getClientAuthFromAccessToken` — `app/Helpers/GoogleSheetService.php` | `<Dev không ghi rõ>` | Nơi gọi refresh token tới Google (bắt `ClientException` = đã gỡ quyền) |
| 7 | `link_google.blade.php` — `resources/views/basic/qr_code/v2/link_google.blade.php` | Thêm modal cảnh báo đè lên màn, giữ nguyên khối UI cũ | Hiển thị cảnh báo + 2 lựa chọn 再連携する / 再連携せずにこの画面を閉じる |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Journal ghi mục 4.1 dưới dạng **"File thay đổi"** (3 file), không tách theo function và không ghi cột Direct/Indirect.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | QR code action — màn liên kết Google Spreadsheet (controller) | `app/Http/Controllers/Basic/QRCodeController.php` | Direct | File thay đổi. Liên quan `linkGoogle` / `redirectUriGoogleSheet` / `cancelGoogleSheet` (mục 3) |
| F2 | Service kiểm tra trạng thái liên kết Google của landing | `app/Services/Landing/LandingGoogleSheetService.php` | Direct | File thay đổi. Liên quan `isConnectionRevoked` / `insertDataToGoogleSheet` (mục 3) |
| F3 | View màn liên kết Google Spreadsheet của QR code action | `resources/views/basic/qr_code/v2/link_google.blade.php` | Direct | File thay đổi — thêm modal cảnh báo |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `landing_connect_google.google_access_token` | **READ-ONLY** | Nguyên văn Dev: *"Không có — chỉ đọc `landing_connect_google.google_access_token` để kiểm tra, không ghi/sửa dữ liệu"* |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Journal không ghi mức High/Medium/Low.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | QR Code Action / Landing (**FA-017**) — màn liên kết Google Spreadsheet của QR code action nay phát hiện được trạng thái đã bị gỡ quyền và hiện cảnh báo liên kết lại | F1, F2, F3, D1 | `<Dev không ghi mức>` |

---

## 5. Recover data (nguyên văn journal)

✔ Không cần recover data

## 6. Verify của Dev (nguyên văn journal)

- **Mức**: `lint`
- **Lệnh**:
  - `php -l app/Http/Controllers/Basic/QRCodeController.php`: No syntax errors detected
  - `php -l app/Services/Landing/LandingGoogleSheetService.php`: No syntax errors detected
  - Blade compile (`BladeCompiler::compileString`) + `php -l` file biên dịch: No syntax errors detected
  - ⚠️ **Chưa chạy được kiểm chứng runtime**: dev DB/web `host.docker.internal` không kết nối được (Connection refused)
- **Bằng chứng**: Bảng `landing_connect_google` (share/db/db-refined) không có cột nào đánh dấu kết nối bị gỡ — khác với `bots.google_sheet_status` (form) và `calendar_management`/`calendar_salon.google_sheet_status` (đặt lịch) nên màn QR code action không thể biết trạng thái gỡ quyền; `vendor/google/auth` `OAuth2::fetchAuthToken` gọi Guzzle với `http_errors` mặc định — Google trả 400 `invalid_grant` khi refresh token bị thu hồi sẽ ném `ClientException`, nên đã bắt riêng `ClientException` = đã gỡ quyền.

## 7. Tự review của AI + rủi ro khi test (nguyên văn journal)

Refix vòng 1 theo reviewer: không thay khối UI đang kết nối, chỉ thêm modal cảnh báo + giữ nút hủy liên kết; bám đúng mẫu cảnh báo sẵn có của đặt lịch/form trả lời.

**Rủi ro / lưu ý khi test:**
- Mỗi lần mở màn liên kết Google phát sinh 1 lệnh gọi làm mới token tới Google — màn cấu hình ít truy cập nên chấp nhận được.
- Trường hợp lỗi mạng tạm thời được coi là vẫn kết nối để tránh báo nhầm, đổi lại lúc đó chưa cảnh báo ngay.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

> ⚠️ **Lưu ý cho Leader khi verify**: mục 4.1 của journal là **danh sách file**, không phải danh sách function → F1/F2 gộp nhiều function trong 1 dòng. Mục 4.3 chỉ có **1 dòng** (chính màn đang fix) — journal không kê tính năng sibling nào, trong khi mục 3 có nhắc `insertDataToGoogleSheet` (luồng ghi dữ liệu vào spreadsheet) và `GoogleSheetService::getClientAuthFromAccessToken` (helper dùng chung với form trả lời / đặt lịch). Cân nhắc hỏi Dev trước khi giao TC.
