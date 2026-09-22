# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38668 — Create google sheet qrlanding fail do lỗi phía google` |
| Module / Màn hình | QR Code Action / Landing (FA-017) — màn danh sách QR action 「QRコードアクション（流入経路分析）」 + job ghi Google Sheet của landing |

## Mô tả bug (bản dịch tiếng Việt)

Khi tạo Google Sheet cho QR landing thì gặp lỗi phía Google và tạo sheet thất bại.

Ví dụ mã lỗi:

```
create sheet landing: 476592failed: {
  "error": {
    "code": 503,
    "message": "The service is currently unavailable.",
    "errors": [
      {
        "message": "The service is currently unavailable.",
        "domain": "global",
        "reason": "backendError"
      }
    ],
    "status": "UNAVAILABLE"
  }
```

2. Expect cần retry lại 5 lần.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — description chỉ có log lỗi mẫu. -->

1.
2.
3.

## Expected result

- Khi tạo Google Sheet cho landing gặp lỗi phía Google (503 UNAVAILABLE / backendError), hệ thống phải **retry lại 5 lần** thay vì fail ngay.

## Actual result

- Tạo sheet thất bại ngay ở lần đầu, không thử lại (log `create sheet landing: 476592failed: {... "code": 503 ...}`).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — log lỗi Google API dán trực tiếp trong description (Redmine **không có file attachment** nào).

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được chủ động** — lỗi 503 / backendError là lỗi tạm thời phía Google, không dựng lại theo ý muốn được. Root cause + cách fix đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cơ chế lưu mã lỗi + job retry** và regression luồng tạo landing, thay vì tái hiện lỗi Google thật.
- Ticket là **Bug tự detect** (phát hiện qua log hệ thống), không phải khách hàng/CS báo → không có bước tái hiện từ CS.
- Bug phụ thuộc **lỗi ngẫu nhiên phía Google** (503 UNAVAILABLE), không xảy ra 100% → muốn test nhánh lỗi phải ép lỗi (chặn mạng ra Google, token sai/hết hạn, hoặc set sẵn `google_sheet_error_code` trong DB).
- Fix có **migration thêm 3 cột bảng `landing`** + **job nền mới chạy mỗi phút** → bắt buộc chạy migration khi release; job nền + gọi Google API thật không kết luận được từ local (RULE-08).
- Trạng thái ticket lúc tạo folder: `Fix done - Đợi test` · Author: Do Van Tu TuDV · Assignee: Ngô Thúy Ngần · Created 2026-07-10, Updated 2026-08-20.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa có trong ticket>` |
| Friend | `<không liên quan>` |
| Đối tượng cấu hình | Landing ID `476592` (QR landing tạo sheet lỗi trong log mẫu) |
| Thời điểm lỗi | `<chưa có trong ticket — ticket tạo 2026-07-10>` |
| Đối chứng | `<chưa có>` — cần 1 landing tạo sheet thành công bình thường để so sánh |

## Journal / note từ Redmine (nguyên văn)

**Journal #125584 — AI LME Fix bug — 2026-07-10:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi tạo Google Sheet cho QR Landing gặp lỗi tạm thời phía Google (503 UNAVAILABLE/backendError) thì tạo sheet thất bại ngay, không thử lại. Yêu cầu: lưu mã lỗi ngay khi tạo landing lỗi và ở job ghi sheet hàng ngày; retry bằng job nền, nhưng chỉ retry với lỗi server (code > 500).

■ 2. CÁCH FIX
Cơ chế retry tạo Google Sheet cho landing bằng JOB nền (KHÔNG đụng GoogleSheetService). (1) MIGRATION thêm 3 cột bảng landing: google_sheet_retry_count (int default 0), google_sheet_error_code (varchar 50), google_sheet_error_message (text) + index. (2) Helper dùng chung trên model Landing: resolveGoogleSheetErrorCode (suy mã lỗi từ exception: HTTP code Google_Service_Exception → reason → fallback) + saveGoogleSheetError (lưu code+msg, KHÔNG tăng retry_count) + hằng GOOGLE_SHEET_RETRY_MIN_CODE=500. (3) NGAY khi tạo landing lỗi (QRCodeController::saveLandingV2 catch) → lưu code+msg vào bảng landing. (4) Job GHI Google Sheet landing HÀNG NGÀY (JobInsertStatisticDataActionLandingToGoogleSheet, landing:insert_google_sheet) khi tạo sheet lỗi → cũng lưu code+msg. (5) Job RETRY landing:retry-create-google-sheet (everyMinute + withoutOverlapping): quét landing đã connect Google (status DONE) còn token, thiếu google_sheet_id, retry_count<5 VÀ CHỈ khi google_sheet_error_code là số > 500 (lỗi server Google: 502/503/504) — lỗi 4xx/500/client (sai token, quyền) chỉ lưu code, KHÔNG retry; mỗi lần retry fail tăng retry_count (SQL atomic +1) + cập nhật code+msg, đủ 5 lần thì thôi; thành công thì lưu google_sheet_id + xoá dấu vết lỗi. Số lần retry chỉ do job retry tăng (luồng tạo landing + job daily chỉ ghi code, không tính là retry).

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
Landing::resolveGoogleSheetErrorCode / Landing::saveGoogleSheetError / const GOOGLE_SHEET_RETRY_MIN_CODE (MỚI, app/Landing.php)
QRCodeController::saveLandingV2 (catch tạo sheet → Landing::saveGoogleSheetError)
JobInsertStatisticDataActionLandingToGoogleSheet::createSheetForLanding (catch → Landing::saveGoogleSheetError)
LandingRetryCreateGoogleSheetCommand::handle (query thêm điều kiện code REGEXP số > 500) / markFailure (tăng retry_count) — dùng Landing::resolveGoogleSheetErrorCode
Kernel::schedule (landing:retry-create-google-sheet everyMinute withoutOverlapping)
Migration add_google_sheet_retry_to_landing_table (3 cột + index)
GoogleSheetService::createSheet — KHÔNG đổi (đã revert retry inline)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Landing.php (thêm helper resolveGoogleSheetErrorCode/saveGoogleSheetError + hằng số)
   - app/Http/Controllers/Basic/QRCodeController.php (catch tạo sheet: lưu code)
   - app/Console/Commands/JobInsertStatisticDataActionLandingToGoogleSheet.php (catch tạo sheet: lưu code)
   - app/Console/Commands/LandingRetryCreateGoogleSheetCommand.php (mới; job retry, lọc code > 500)
   - app/Console/Kernel.php (thêm schedule everyMinute)
   - database/migrations/2026_07_10_000001_add_google_sheet_retry_to_landing_table.php (mới)
 • 4.2 Data ảnh hưởng:
   - Bảng landing: THÊM 3 cột google_sheet_retry_count (int default 0), google_sheet_error_code (varchar 50 null), google_sheet_error_message (text null) + index idx_landing_gsheet_retry_count. Additive, không xoá/đổi dữ liệu cũ; cần chạy migration khi release.
   - 3 điểm ghi lỗi (tạo landing / job daily / job retry) cùng ghi code+msg vào landing; job retry còn tăng google_sheet_retry_count và ghi google_sheet_id khi thành công.
 • 4.3 Tính năng liên quan:
   - QR Code Action / Landing (FA-017) — tạo landing lỗi Google giờ lưu mã lỗi+msg vào bảng landing; job nền tự retry tối đa 5 lần (1'/lần) NHƯNG chỉ với lỗi server code > 500; job ghi sheet hàng ngày cũng lưu code khi tạo lỗi.
   - Form Builder (FA-011) / Lesson Booking (FA-019) / Salon Booking (FA-020) — KHÔNG ảnh hưởng: chỉ đụng luồng landing (QRCodeController + job landing); createSheet của service giữ nguyên hành vi cũ cho các caller khác.

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Landing.php: No syntax errors; php -l app/Http/Controllers/Basic/QRCodeController.php: No syntax errors; php -l app/Console/Commands/JobInsertStatisticDataActionLandingToGoogleSheet.php: No syntax errors; php -l app/Console/Commands/LandingRetryCreateGoogleSheetCommand.php: No syntax errors; php -l app/Console/Kernel.php + migration: No syntax errors; git diff base -- app/Helpers/GoogleSheetService.php: RỖNG (không đụng service)
   Bằng chứng: Điều kiện retry code > 500 dùng whereRaw REGEXP '^[0-9]+$' + CAST(...AS UNSIGNED) > 500 (Landing::GOOGLE_SHEET_RETRY_MIN_CODE) → chỉ retry lỗi server, bỏ qua 4xx/500/reason chữ.; Luồng tạo landing + job daily chỉ lưu code (không tăng retry_count); retry_count chỉ do job retry tăng nên 'số lần retry' đúng nghĩa.; Job retry lọc status=DONE — tách khỏi app:create-google-sheet (WAITING/ERROR) → không tạo sheet trùng.; retry_count tăng SQL atomic (+1) + withoutOverlapping → an toàn khi chạy chồng.

■ TỰ REVIEW (AI)
Lưu mã lỗi tạo Google Sheet vào bảng landing tại 3 điểm (tạo landing, job ghi sheet hàng ngày, job retry); job retry 1'/lần CHỈ retry lỗi server code > 500, dừng sau 5 lần. Không đụng GoogleSheetService. Migration additive 3 cột + index. Helper resolve/save gom về model Landing để 3 điểm dùng chung.
 • Rủi ro / lưu ý khi test:
   - Cần chạy migration khi release (thêm 3 cột landing) — quên thì saveGoogleSheetError/job update cột chưa tồn tại sẽ lỗi SQL.
   - Quy ước 'code > 500' loại cả HTTP 500 (internalError) và lỗi có reason chữ (backendError khi HTTP code rỗng) khỏi retry — đúng theo yêu cầu; nếu muốn gộp 500/reason chữ thì đổi GOOGLE_SHEET_RETRY_MIN_CODE + điều kiện REGEXP.
   - Landing tạo sheet thành công nhưng lưu google_sheet_id thất bại (hiếm) có thể tạo sheet lần 2 ở run sau — cùng hành vi các job tạo sheet hiện có (lọc whereNull google_sheet_id).

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_38668 (nhánh gốc release_step_20260623, commit 801925eb26, 6 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 2 phút 52 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=745ac356-104d-42d0-adc8-dd5d17f2e0da
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38668
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #125585 — AI LME Fix bug — 2026-07-10:** nội dung **trùng hoàn toàn** với Journal #125584 (hệ thống Auto-fixbug post 2 lần) — không chép lại.
