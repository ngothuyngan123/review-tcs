# 03 — Đánh giá ảnh hưởng từ Dev

> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.
> Nguồn: Redmine #38668 — Journal #125584 (AI Auto-fixbug LME, 2026-07-10). Nội dung các mục 1 → 4 chép **nguyên văn** từ journal, không diễn giải lại.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — `<chưa rõ dev người review branch>` |
| Commit / Pull Request | commit `801925eb26` (6 file, repo `sns-line`) — `<chưa có link PR trong ticket>` |
| Branch | `ai_small_38668` (nhánh gốc `release_step_20260623`) — đã push |
| Ngày submit đánh giá | 2026-07-10 |
| Auto-filled | `2026-09-15 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi tạo Google Sheet cho QR Landing gặp lỗi tạm thời phía Google (503 UNAVAILABLE/backendError) thì tạo sheet thất bại ngay, không thử lại. Yêu cầu: lưu mã lỗi ngay khi tạo landing lỗi và ở job ghi sheet hàng ngày; retry bằng job nền, nhưng chỉ retry với lỗi server (code > 500).

## 2. Cách fix

Cơ chế retry tạo Google Sheet cho landing bằng **JOB nền** (KHÔNG đụng `GoogleSheetService`):

1. **MIGRATION** thêm 3 cột bảng `landing`: `google_sheet_retry_count` (int default 0), `google_sheet_error_code` (varchar 50), `google_sheet_error_message` (text) + index.
2. **Helper dùng chung** trên model `Landing`: `resolveGoogleSheetErrorCode` (suy mã lỗi từ exception: HTTP code `Google_Service_Exception` → reason → fallback) + `saveGoogleSheetError` (lưu code+msg, **KHÔNG** tăng retry_count) + hằng `GOOGLE_SHEET_RETRY_MIN_CODE = 500`.
3. **NGAY khi tạo landing lỗi** (`QRCodeController::saveLandingV2` catch) → lưu code+msg vào bảng landing.
4. **Job GHI Google Sheet landing HÀNG NGÀY** (`JobInsertStatisticDataActionLandingToGoogleSheet`, `landing:insert_google_sheet`) khi tạo sheet lỗi → cũng lưu code+msg.
5. **Job RETRY** `landing:retry-create-google-sheet` (`everyMinute` + `withoutOverlapping`): quét landing đã connect Google (status `DONE`) còn token, thiếu `google_sheet_id`, `retry_count < 5` **VÀ CHỈ khi** `google_sheet_error_code` là số **> 500** (lỗi server Google: 502/503/504) — lỗi 4xx/500/client (sai token, quyền) chỉ lưu code, **KHÔNG retry**; mỗi lần retry fail tăng `retry_count` (SQL atomic +1) + cập nhật code+msg, đủ 5 lần thì thôi; thành công thì lưu `google_sheet_id` + xoá dấu vết lỗi.

> Số lần retry **chỉ do job retry tăng** (luồng tạo landing + job daily chỉ ghi code, không tính là retry).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Landing::resolveGoogleSheetErrorCode` / `Landing::saveGoogleSheetError` / const `GOOGLE_SHEET_RETRY_MIN_CODE` — `app/Landing.php` | **MỚI** | Helper dùng chung cho 3 điểm ghi lỗi |
| 2 | `QRCodeController::saveLandingV2` | catch tạo sheet → gọi `Landing::saveGoogleSheetError` | Lưu mã lỗi ngay khi tạo landing lỗi |
| 3 | `JobInsertStatisticDataActionLandingToGoogleSheet::createSheetForLanding` | catch → gọi `Landing::saveGoogleSheetError` | Job ghi sheet hàng ngày cũng phải lưu mã lỗi |
| 4 | `LandingRetryCreateGoogleSheetCommand::handle` / `markFailure` | **MỚI** — query thêm điều kiện code REGEXP số > 500; `markFailure` tăng `retry_count`; dùng `Landing::resolveGoogleSheetErrorCode` | Job retry tối đa 5 lần, chỉ với lỗi server |
| 5 | `Kernel::schedule` — `app/Console/Kernel.php` | thêm `landing:retry-create-google-sheet` (`everyMinute` + `withoutOverlapping`) | Đăng ký lịch chạy job retry |
| 6 | Migration `add_google_sheet_retry_to_landing_table` | **MỚI** — 3 cột + index | Lưu retry_count / error_code / error_message |
| 7 | `GoogleSheetService::createSheet` | **KHÔNG đổi** (đã revert retry inline) | Giữ nguyên hành vi cho các caller khác (Form / Lesson / Salon) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev kê ở journal theo **file thay đổi**; function cụ thể xem mục 3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Landing::resolveGoogleSheetErrorCode` / `saveGoogleSheetError` + hằng `GOOGLE_SHEET_RETRY_MIN_CODE` | `app/Landing.php` | Direct | **Hàm dùng chung** — 3 điểm gọi (F2, F3, F4) |
| F2 | `QRCodeController::saveLandingV2` (catch tạo sheet: lưu code) | `app/Http/Controllers/Basic/QRCodeController.php` | Direct | Luồng tạo QR action / landing trên UI |
| F3 | `JobInsertStatisticDataActionLandingToGoogleSheet::createSheetForLanding` (catch tạo sheet: lưu code) | `app/Console/Commands/JobInsertStatisticDataActionLandingToGoogleSheet.php` | Direct | Job ghi thống kê landing lên Sheet hàng ngày |
| F4 | `LandingRetryCreateGoogleSheetCommand` (**mới**; job retry, lọc code > 500) | `app/Console/Commands/LandingRetryCreateGoogleSheetCommand.php` | Direct | Job retry `landing:retry-create-google-sheet` |
| F5 | `Kernel::schedule` (thêm schedule `everyMinute`) | `app/Console/Kernel.php` | Direct | Lịch chạy job nền, `withoutOverlapping` |
| F6 | Migration `add_google_sheet_retry_to_landing_table` (**mới**) | `database/migrations/2026_07_10_000001_add_google_sheet_retry_to_landing_table.php` | Direct | Phải chạy khi release |
| F7 | `GoogleSheetService::createSheet` | `app/Helpers/GoogleSheetService.php` | **KHÔNG đổi** | Dev verify `git diff` RỖNG — giữ hành vi cũ cho mọi caller khác |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `landing.google_sheet_retry_count` (int default 0), `landing.google_sheet_error_code` (varchar 50 null), `landing.google_sheet_error_message` (text null) + index `idx_landing_gsheet_retry_count` | MIGRATE (additive) | Không xoá/đổi dữ liệu cũ; **cần chạy migration khi release** |
| D2 | `landing.google_sheet_error_code` + `google_sheet_error_message` ghi từ **3 điểm** (tạo landing / job daily / job retry) | UPDATE | 3 điểm cùng ghi code+msg |
| D3 | `landing.google_sheet_retry_count` (chỉ job retry tăng, SQL atomic +1) · `landing.google_sheet_id` (ghi khi retry thành công, đồng thời xoá dấu vết lỗi) | UPDATE | `retry_count` KHÔNG tăng ở luồng tạo landing và job daily |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **QR Code Action / Landing (FA-017)** — tạo landing lỗi Google giờ lưu mã lỗi+msg vào bảng landing; job nền tự retry tối đa 5 lần (1'/lần) NHƯNG chỉ với lỗi server code > 500 | F1, F2, F4, F5, D1, D2, D3 | **High** |
| T2 | **Job ghi Google Sheet landing hàng ngày** (`landing:insert_google_sheet`) — khi tạo sheet lỗi cũng lưu code | F3, D2 | Medium |
| T3 | Form Builder (FA-011) / Lesson Booking (FA-019) / Salon Booking (FA-020) | F7 (`createSheet` không đổi) | **Dev khẳng định KHÔNG ảnh hưởng** — chỉ đụng luồng landing (QRCodeController + job landing); `createSheet` của service giữ nguyên hành vi cũ cho các caller khác |

---

## 5. Recover data (từ journal)

✔ Không cần recover data.

## 6. Verify của Dev (từ journal)

- **Mức:** lint (`php -l` 6 file: No syntax errors) + `git diff base -- app/Helpers/GoogleSheetService.php`: **RỖNG** (không đụng service).
- **Bằng chứng Dev đưa ra:**
  - Điều kiện retry code > 500 dùng `whereRaw REGEXP '^[0-9]+$'` + `CAST(... AS UNSIGNED) > 500` (`Landing::GOOGLE_SHEET_RETRY_MIN_CODE`) → chỉ retry lỗi server, bỏ qua 4xx/500/reason chữ.
  - Luồng tạo landing + job daily chỉ lưu code (không tăng `retry_count`); `retry_count` chỉ do job retry tăng nên "số lần retry" đúng nghĩa.
  - Job retry lọc `status = DONE` — tách khỏi `app:create-google-sheet` (WAITING/ERROR) → không tạo sheet trùng.
  - `retry_count` tăng SQL atomic (+1) + `withoutOverlapping` → an toàn khi chạy chồng.

## 7. Rủi ro / lưu ý khi test (Dev tự nêu)

- ⚠️ **Cần chạy migration khi release** (thêm 3 cột landing) — quên thì `saveGoogleSheetError` / job update cột chưa tồn tại sẽ **lỗi SQL**.
- ⚠️ Quy ước `code > 500` **loại cả HTTP 500** (internalError) và lỗi có **reason dạng chữ** (`backendError` khi HTTP code rỗng) khỏi retry — Dev nói "đúng theo yêu cầu"; nếu muốn gộp 500/reason chữ thì đổi `GOOGLE_SHEET_RETRY_MIN_CODE` + điều kiện REGEXP.
  - ⚠️ **Lưu ý cho Leader**: log lỗi trong chính ticket là `"code": 503` kèm `"reason": "backendError"` → case gốc vẫn retry được; nhưng nếu exception không có HTTP code mà chỉ có reason chữ `backendError` thì **không retry** — cần chốt với PO xem có đúng ý không.
- ⚠️ Landing tạo sheet thành công nhưng lưu `google_sheet_id` thất bại (hiếm) có thể **tạo sheet lần 2** ở run sau — cùng hành vi các job tạo sheet hiện có (lọc `whereNull google_sheet_id`).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
