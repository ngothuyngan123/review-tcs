# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44186 — hàm downloadCsv trong CsvManagementController download ở csv bị lỗi security có thể download được file env` |
| Module / Màn hình | CSV管理 (CSV management) — nút 「CSVダウンロード」 ở tab エクスポート; endpoint `GET /basic/csv-management/download-csv` và `POST /basic/csv-management/export` trong `CsvManagementController` |

## Mô tả bug (bản dịch tiếng Việt)

<!-- issue.description rỗng — ticket thuộc tracker "Bug tự detect" (self-detected security), không có mô tả tự do của khách hàng. Toàn bộ nội dung điều tra nằm trong journal (Dev Studio), xem "Journal / note từ Redmine" bên dưới và `03-dev-impact.md`. -->

## Steps to reproduce

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
- [ ] Có log / request-response

<!-- issue.attachments rỗng — không có attachment trên Redmine. -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine theo format "Tái hiện bug" chuẩn — ticket là **self-detected security bug** (tracker "Bug tự detect", description trống), root cause + cách khai thác đã được Dev tự mô tả thẳng trong journal (xem file `03-dev-impact.md`).

- Bản chất lỗi: **Path traversal** (`fileName=/../.env&path_new=1` → tải được `.env` của ứng dụng) + **IDOR** (`csvExport` không lọc `bot_id` → lộ đường dẫn CSV của bot khác).
- Severity nghiệp vụ: rủi ro lộ secret (`.env`: DB, LINE, thanh toán, media...) — Dev đánh giá "Rủi ro thấp" cho **bản thân fix** (2 hàm chỉ đọc, có test), nhưng rủi ro **đã bị khai thác trước khi fix** chưa xác định được từ DB, cần Ops soát access log riêng (ngoài phạm vi task QA).
- Môi trường phát hiện: tự detect (không ghi rõ staging/production trong ticket).
- Có bug phụ phát sinh khi Test Studio chạy tự động: **#4026** — Dev xác nhận KHÔNG phải bug thật, chỉ là lỗi Console `PushManager.subscribe` do `VAPID_PUBLIC_KEY` không hợp lệ ở môi trường local (lỗi có sẵn từ lúc tải trang, không liên quan luồng CSV). Leader/Tester cân nhắc khi chấm Console error cho các TC của màn CSV管理 (đặc biệt case liên quan tới ca `NEW-15` ở Test Studio).
- Dev có đề xuất **ticket riêng** (ngoài phạm vi #44186) cho các hàm `downloadCsv` khác còn cùng pattern lỗi (nhận `fileName` trực tiếp từ client): `Basic\BookingEventController::downloadCsv`, `Admin\UserController::downloadCsv`/`downloadCsvUser`/`downloadCsvActive`/`downloadCsvInactive`, `Admin\AffiliateInfoController::downloadCsv`. **Không** thuộc phạm vi review/viết TC của task này — chỉ ghi nhận để Leader cân nhắc mở ticket riêng.

## Journal / note từ Redmine (nguyên văn)

**Journal #147823 — Dev Studio — 2026-10-23:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
`CsvManagementController::downloadCsv` lấy `fileName` từ query rồi nối thẳng vào `public_path()` (nhánh `path_new=1`) hoặc `public_path().'/storage/'` (nhánh `path_new=0`). Hàm không chuẩn hoá đường dẫn, không chặn `..`, không giới hạn thư mục và không đối chiếu bản ghi `csv_management` của bot hiện tại. Vì vậy user đăng nhập bất kỳ gửi `fileName=/../.env&path_new=1` sẽ tải được file `.env` của ứng dụng. Thêm một lỗi trong cùng luồng: `csvExport` tìm bản ghi theo `csv_id` mà không lọc `bot_id`, nên lộ được đường dẫn file CSV của bot khác.

Hướng sửa:
- D-1 downloadCsv lấy file theo csv_id của bot hiện tại thay vì fileName từ client
- D-2 JS exportCsv gọi download-csv bằng csv_id
- D-3 csvExport chỉ trả đường dẫn CSV của bot đang đăng nhập

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng nút 「CSVダウンロード」 của màn CSV管理: bản ghi kiểu cũ tải qua csv_id, bản ghi mới vẫn mở media URL như cũ. Link cũ dạng ?fileName=... sẽ ra 404. Không đổi DB và không đụng job export.
```

**Journal #147829 — Dev Studio — 2026-10-23:**

```
Dev handoff — 23/10 19:47 · nhánh ai_studio_fixbug_44186

Nguyên nhân:
`CsvManagementController::downloadCsv` lấy `fileName` từ query rồi nối thẳng vào `public_path()` (nhánh `path_new=1`) hoặc `public_path().'/storage/'` (nhánh `path_new=0`). Hàm không chuẩn hoá đường dẫn, không chặn `..`, không giới hạn thư mục và không đối chiếu bản ghi `csv_management` của bot hiện tại. Vì vậy user đăng nhập bất kỳ gửi `fileName=/../.env&path_new=1` sẽ tải được file `.env` của ứng dụng. Thêm một lỗi trong cùng luồng: `csvExport` tìm bản ghi theo `csv_id` mà không lọc `bot_id`, nên lộ được đường dẫn file CSV của bot khác.

Nội dung thay đổi:
- Màn CSV管理, /basic/csv-management/download-csv: chỉ nhận csv_id và tìm bản ghi của bot hiện tại. Id sai, không có, thuộc bot khác hoặc file đã mất thì ra trang 404. Tham số fileName và path_new bị bỏ qua.
- Màn CSV管理, nút 「CSVダウンロード」: bản ghi kiểu cũ mở download-csv?csv_id=<id>; bản ghi mới vẫn mở thẳng media như cũ.
- Màn CSV管理, API /basic/csv-management/export: chỉ trả đường dẫn file của bản ghi thuộc bot hiện tại; bot khác thì file_name rỗng.

File đã sửa (php-web):
  app/Http/Controllers/CsvManagementController.php |  32 ++--
  public/js/csv_management/csv_management.js       |   2 +-
  tests/Feature/CsvManagementDownloadGuardTest.php | 191 +++++++++++++++++++++++
  3 files changed, 215 insertions(+), 10 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi gói trong 2 hàm chỉ đọc của một màn, có test và đã kiểm chứng ngược trên code cũ. Rủi ro chính là JS cũ còn trong cache làm bản ghi kiểu cũ ra 404 cho tới khi reload.
- Nút 「CSVダウンロード」 màn CSV管理 (exportCsv trong csv_management.js) là nơi duy nhất gọi 2 endpoint đã sửa: cần test cả bản ghi kiểu cũ và kiểu mới.
- Link, bookmark hoặc tab cũ dạng download-csv?fileName=... sẽ ra 404 (chủ ý, vì đó là đường tấn công).
- Người dùng nhiều bot và staff: kết quả tải phụ thuộc bot đang chọn trong session.
- Job HandleExportCsv/HandleExportCsv2 và linect chỉ ghi cột file_name_new; code đã sửa chỉ đọc cột này, không đổi job, DB hay lme-ui.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Endpoint chỉ đọc file, không ghi hay làm hỏng dữ liệu DB, nên không có bản ghi cần recover. Rủi ro lộ bí mật (nếu đã bị khai thác) không xác định được từ DB; việc soát access log và đổi khoá thuộc vận hành (follow-up).

Lưu ý khi deploy:
- csv_management.js đã đổi nhưng không tăng sns-line.version: đội release cân nhắc tăng version khi đóng release (hoặc người dùng hard-reload) để trình duyệt nạp JS mới.

Việc cần người làm thêm (ngoài phạm vi task):
- Vận hành: soát access log web từ 2022-07 tới khi deploy bản sửa, tìm request /basic/csv-management/download-csv có fileName chứa '..'. Nếu có, đổi các khoá/mật khẩu trong .env (DB, LINE, thanh toán, media...).
- Đề xuất ticket riêng: Basic\BookingEventController::downloadCsv (/basic/booking_event/download-csv) và Admin\UserController::downloadCsv (/admin/account-management/download-csv) còn cùng mẫu đọc file local theo fileName của client, nên có cùng lỗ hổng path traversal.
- Rà và sửa ở ticket riêng các hàm downloadCsv khác còn cùng mẫu lỗi nhận fileName từ client: BookingEventController::downloadCsv và Admin\UserController::downloadCsv. Ngoài ra còn các route /admin/account-management/download-csv* và /admin/payment-management/download-csv.
- Ops soát access log của /basic/csv-management/download-csv có fileName chứa '..' hoặc '.env' để biết lỗ hổng đã bị khai thác chưa; nếu có thì xoay vòng (rotate) các secret trong .env.
- Bộ PHPUnit đầy đủ đang crash sẵn ở tests/Feature/ContractExpireServiceTest.php: class anonymous thiếu các method mới của BotRepositoryInterface. Cần sửa ở ticket riêng.
- Mở ticket bảo mật riêng cho các endpoint còn cùng lỗi tải file tuỳ ý: Basic\BookingEventController::downloadCsv (/basic/booking_event/download-csv), Admin\UserController::downloadCsv/downloadCsvUser/downloadCsvActive/downloadCsvInactive (/admin/account-management/download-csv*) và Admin\AffiliateInfoController::downloadCsv (/admin/payment-management/download-csv).
- Người vận hành soát access log production cho các request download-csv có fileName chứa '..' hoặc '.env' để biết lỗ hổng đã bị khai thác chưa; nếu có thì thay các secret trong .env.

Điểm cần test:
- Gọi download-csv?fileName=/../.env&path_new=1 và ?fileName=../../.env&path_new=0: nhận 404, không tải được file.
- Gọi download-csv?csv_id=<id của bot khác>: nhận 404.
- Gọi với csv_id=abc, csv_id[]=1 hoặc không có csv_id: nhận 404, không lỗi 500.
- POST /basic/csv-management/export với csv_id của bot khác: file_name trả về rỗng.
- Bản ghi kiểu cũ (chỉ file_name) của bot hiện tại: nút CSVダウンロード tải đúng file; nếu file đã mất thì ra 404.
- Bản ghi mới (file_name_new): nút CSVダウンロード vẫn mở media URL như trước; gọi tay ?csv_id= thì tải hoặc redirect đúng file.
- Staff được cấp quyền màn CSV管理 tải được CSV của bot đang chọn.
- Đổi bot rồi tải CSV của bot vừa chọn thì được; link CSV của bot trước thì ra 404.
- Hard-reload (Ctrl+F5) trước khi test vì JS không tăng version.

Branch: ai_studio_fixbug_44186
- sns-line: ai_studio_fixbug_44186 (nhánh gốc release_step_20260930_v2 @14f52839281b, commit 441e6f24b2ac828e742efd7660fbfa83d10ee53a)
```

**Journal #147891 — Dev Studio — 2026-10-24:**

```
Dev handoff — 24/10 09:22 · nhánh ai_studio_fixbug_44186

Nguyên nhân:
Lỗi Console mà #4026 báo đến từ script đăng ký push notification trong layout chung của web quản trị. Script này gọi pushManager.subscribe với VAPID_PUBLIC_KEY của môi trường, mà key đó không hợp lệ ở môi trường test local, nên trang nào dùng layout basic cũng báo lỗi ngay khi tải. Luồng tải CSV của ticket chạy đúng; nguyên nhân gốc của ticket (download-csv cho tải file tuỳ ý) vẫn như v1 và đã sửa.

Không có commit mới so với lần bàn giao trước (23/10 19:47): nhánh giữ nguyên commit đã bàn giao.

Bug automation Test Studio:
- Bug #4026 không phải bug: File CSV media vẫn tải đúng (SHA-256 khớp fixture). Lỗi PushManager.subscribe đã có từ lúc tải trang (preClickPageErrors), do VAPID_PUBLIC_KEY ở môi trường local không hợp lệ (vapidKeyValid:false). Script gây lỗi nằm trong layout chung, mà ticket không sửa. Nên chạy lại trên môi trường có key hợp lệ, hoặc bỏ qua lỗi có sẵn này khi chấm.

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi gói trong 2 hàm chỉ đọc của một màn, có test và đã kiểm chứng ngược trên code cũ. Rủi ro chính là JS cũ còn trong cache làm bản ghi kiểu cũ ra 404 cho tới khi reload.

Recover dữ liệu: Không cần recover — Lỗi chỉ do cấu hình môi trường test, không có dữ liệu bị ảnh hưởng. Bản sửa v1 chỉ đọc file và không ghi DB.

Việc cần người làm thêm (ngoài phạm vi task):
- Test Studio: cấu hình VAPID_PUBLIC_KEY hợp lệ cho môi trường local, hoặc thêm lỗi 'PushManager subscribe applicationServerKey is not valid' vào danh sách lỗi Console bỏ qua khi chấm, để các ca của màn dùng layout basic không bị đánh lỗi giả.
- Test Studio: chạy lại ca NEW-15 trên môi trường có VAPID_PUBLIC_KEY hợp lệ, hoặc bỏ qua riêng lỗi PushManager.subscribe khi chấm ca này.
- (Các việc vận hành/ticket riêng khác — xem journal #147829, không lặp lại.)

Điểm cần test (bổ sung so với v1):
- Chạy lại ca NEW-15 trên môi trường có VAPID_PUBLIC_KEY hợp lệ, hoặc bỏ qua riêng lỗi PushManager.subscribe khi chấm: bấm 「CSVダウンロード」 với bản ghi kiểu mới thì tab mới tải đúng file media và Console không có lỗi mới sau khi bấm.
- Đối chứng trên base chưa có fix, cùng môi trường: mở màn CSV管理 vẫn thấy lỗi PushManager như cũ.
- Các điểm kiểm thử của v1 (chặn ../.env, chặn csv_id của bot khác, tải bản ghi kiểu cũ) giữ nguyên.

Branch: ai_studio_fixbug_44186 (không đổi so với #147829)
```
