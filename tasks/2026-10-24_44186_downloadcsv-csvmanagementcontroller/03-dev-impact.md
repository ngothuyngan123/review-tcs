# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (journal #147823 / #147829 / #147891 trên Redmine; issue không có assignee riêng) |
| Commit / Pull Request | `<chưa có link PR>` — chỉ có tên branch + commit nền, xem dòng Branch |
| Branch | `ai_studio_fixbug_44186` (nhánh gốc `release_step_20260930_v2` @`14f52839281b`, commit `441e6f24b2ac828e742efd7660fbfa83d10ee53a`) |
| Ngày submit đánh giá | `2026-10-23` (bản đầy đủ #147829), cập nhật bổ sung `2026-10-24` (#147891 — không có commit mới, chỉ clarify bug #4026 không liên quan) |
| Auto-filled | `2026-10-24 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

`CsvManagementController::downloadCsv` lấy `fileName` từ query rồi nối thẳng vào `public_path()` (nhánh `path_new=1`) hoặc `public_path().'/storage/'` (nhánh `path_new=0`). Hàm không chuẩn hoá đường dẫn, không chặn `..`, không giới hạn thư mục và không đối chiếu bản ghi `csv_management` của bot hiện tại. Vì vậy user đăng nhập bất kỳ gửi `fileName=/../.env&path_new=1` sẽ tải được file `.env` của ứng dụng.

Thêm một lỗi trong cùng luồng: `csvExport` tìm bản ghi theo `csv_id` mà không lọc `bot_id`, nên lộ được đường dẫn file CSV của bot khác (IDOR).

→ 2 lỗ hổng độc lập trong cùng 1 luồng màn CSV管理: (1) path traversal ở `downloadCsv`, (2) IDOR ở `csvExport`.

## 2. Cách fix

- **D-1**: `downloadCsv` lấy file theo `csv_id` của bot hiện tại thay vì `fileName` từ client. Tham số `fileName` và `path_new` từ client bị **bỏ qua hoàn toàn**.
  - `csv_id` sai / không có / thuộc bot khác / file đã mất → trang **404**.
  - Bản ghi kiểu cũ (chỉ `file_name`) → mở `download-csv?csv_id=<id>`, đọc từ `public_path().'/storage/'.file_name`.
  - Bản ghi kiểu mới (`file_name_new`) → ưu tiên file local nếu có; không có file local → **302 redirect** sang media server; vẫn mở thẳng media URL như luồng cũ ở phía FE.
- **D-2**: JS `exportCsv` (`csv_management.js`) gọi `download-csv` bằng `csv_id` (không còn gửi `fileName`).
- **D-3**: `csvExport` (API `/basic/csv-management/export`) chỉ trả đường dẫn file của bản ghi **thuộc bot đang đăng nhập** (`where bot_id = getBotId()`); bot khác → `file_name` trả về **rỗng** (vẫn HTTP 200, `success=true`).

File đã sửa (php-web):
```
app/Http/Controllers/CsvManagementController.php |  32 ++--
public/js/csv_management/csv_management.js       |   2 +-
tests/Feature/CsvManagementDownloadGuardTest.php | 191 +++++++++++++++++++++++
3 files changed, 215 insertions(+), 10 deletions(-)
```

Migration / thay đổi dữ liệu: **không có** (Dev đã kiểm diff). `csv_management.js` đổi nhưng **không tăng `sns-line.version`** → cần **hard-reload (Ctrl+F5)** để nạp JS mới khi test, và đội release cân nhắc bump version lúc deploy.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `exportCsv` (`public/js/csv_management/csv_management.js`) | Đổi tham số gọi `download-csv` từ `fileName`/`path_new` sang `csv_id` | Dev xác nhận đây là **nơi duy nhất** gọi 2 endpoint đã sửa trên màn CSV管理 — không còn caller nào khác dùng `fileName`/`path_new` |
| 2 | `HandleExportCsv` / `HandleExportCsv2` (job nền) | Không đổi | Job chỉ **ghi** cột `file_name_new`; code đã sửa chỉ **đọc** cột này → không đụng job, DB hay lme-ui |

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CsvManagementController::downloadCsv` (`GET /basic/csv-management/download-csv`) | `app/Http/Controllers/CsvManagementController.php` | Direct | Đổi hoàn toàn input nhận (bỏ `fileName`/`path_new`, chỉ nhận `csv_id`); thêm check `bot_id` hiện tại |
| F2 | `CsvManagementController::csvExport` (`POST /basic/csv-management/export`) | `app/Http/Controllers/CsvManagementController.php` | Direct | Thêm filter `bot_id` hiện tại; bot khác → `file_name` rỗng thay vì lộ path |
| F3 | `exportCsv` (nút 「CSVダウンロード」) | `public/js/csv_management/csv_management.js` | Direct | Đổi payload gọi `download-csv`: `csv_id` thay cho `fileName`/`path_new` |

### 4.2. List data bị update khi fix bug

<!-- Dev xác nhận KHÔNG có migration / thay đổi dữ liệu (đã kiểm diff) — cả 2 hàm sửa đều chỉ ĐỌC, không ghi DB. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `csv_management` (bảng DB) | READ-ONLY (không CREATE/UPDATE/DELETE/MIGRATE) | Trước fix: đọc `fileName` thẳng từ filesystem, không query DB. Sau fix: bắt buộc query bảng này theo `csv_id` + `bot_id` trước khi trả file — nên một bản ghi thiếu/sai `bot_id` trong DB sẽ đổi hành vi (404 thay vì tải được) |
| D2 | File JS asset `csv_management.js` trên CDN/cache browser | Không đổi version (`sns-line.version`) | Rủi ro release: browser cache JS cũ vẫn gọi `fileName`/`path_new` → nhận 404 cho tới khi hard-reload |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn CSV管理 — nút 「CSVダウンロード」, bản ghi kiểu cũ (chỉ `file_name`) | F1, D1 | Medium — nhánh mới hoàn toàn (query theo `csv_id`+`bot_id` thay vì đọc file trực tiếp), cần test cả path đúng và path lỗi (404) |
| T2 | Màn CSV管理 — nút 「CSVダウンロード」, bản ghi kiểu mới (`file_name_new`) | F1 | Low — Dev khẳng định luồng này **không đổi** (vẫn mở media URL như cũ), nhưng cần verify lại vì endpoint chung đã sửa |
| T3 | Link/bookmark/tab cũ dạng `download-csv?fileName=...&path_new=...` | F1 | By-design — **chủ ý** trả 404 (đây chính là đường tấn công cũ); không phải regression nhưng cần verify đã thực sự chặn |
| T4 | API `/basic/csv-management/export` khi gọi chéo bot (nhiều bot / staff) | F2 | Medium — hành vi đổi từ "lộ path của bot khác" (lỗi bảo mật) sang "trả rỗng"; FE phải xử lý được `file_name=''` mà không lỗi |
| T5 | *(Ngoài phạm vi task — chỉ ghi nhận)* Các hàm `downloadCsv` khác cùng pattern lỗi: `BookingEventController::downloadCsv`, `Admin\UserController::downloadCsv*`, `Admin\AffiliateInfoController::downloadCsv` | — | Dev đề xuất ticket riêng, **không** fix trong #44186 — KHÔNG viết TC cho các endpoint này ở task này |

<!-- Ghi chú thêm: Dev đánh giá tổng thể "Rủi ro thấp" cho CHÍNH bản fix (2 hàm chỉ đọc, đã có PHPUnit CsvManagementDownloadGuardTest). Rủi ro bảo mật CÒN LẠI (lỗ hổng đã bị khai thác trước khi fix hay chưa) thuộc về vận hành (soát access log + rotate secret), ngoài phạm vi review TC. -->
