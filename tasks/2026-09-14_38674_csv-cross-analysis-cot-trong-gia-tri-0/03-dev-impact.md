# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | commit `18bee01948` (1 file) — Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=38674 |
| Branch | `ai_fixbug_38674` (repo `sns-line`, nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | 2026-08-26 (Journal #133057) |
| Auto-filled | `2026-09-14 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Lớp xuất CSV của màn Phân tích chéo không bật chế độ so sánh nghiêm ngặt, nên thư viện xuất Excel quyết định có ghi ô hay không bằng phép so sánh lỏng (giá trị khác null). Trong PHP số nguyên 0 được coi là bằng null, vì vậy mọi ô mang giá trị 0 bị bỏ qua và ra file thành ô trống. Hai cột Số người đối tượng (対象人数) và Tổng (合計) đang đẩy số nguyên nên bị trống; các cột còn lại trước đó đã được ép sang chuỗi nên vẫn hiện 0.

**Bằng chứng Dev đưa ra:**
- `config/excel.php:45` — `strict_null_comparison = false` (mặc định toàn hệ thống nên phải khai báo ở từng lớp export).
- PhpSpreadsheet `Worksheet::fromArray` dòng 3087 — nhánh không strict so sánh lỏng nên số nguyên 0 bị bỏ qua, không ghi ô.
- PHP 7.4: `(0 != null)` = false, `("0" != null)` = true — giải thích vì sao chỉ 2 cột đẩy số nguyên bị trống.

## 2. Cách fix

Bật so sánh nghiêm ngặt (`WithStrictNullComparison`) cho lớp xuất CSV của màn Phân tích chéo, nhờ đó ô có giá trị 0 được ghi thẳng vào file thay vì bị thư viện bỏ qua — 2 cột 対象人数 và 合計 nay hiện đúng 0 như trên web. Sửa tại gốc cơ chế ghi ô nên đúng cho **mọi cột số** của file này, không chỉ 2 cột đang lỗi.

**Quét ngang (Dev ghi nhận, NGOÀI phạm vi ticket — chỉ ghi nhận, chưa fix):** cùng kiểu lỗi còn ở vài lớp xuất CSV khác — thống kê click landing, lịch sử đơn hàng, đặt chỗ.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ExportCrossAnalysis::map` / `headings` — `app/Exports/ExportCrossAnalysis.php` | **CÓ SỬA** — thêm `implements WithStrictNullComparison` + import tương ứng | Lớp export chứa root cause: quyết định ghi ô bằng so sánh lỏng |
| 2 | `CrossAnalysisController::exportCsv` — `app/Http/Controllers/Basic/CrossAnalysisController.php:2178` | Không sửa | Nơi **duy nhất** khởi tạo `ExportCrossAnalysis` (Dev đã grep xác nhận) |
| 3 | `CrossAnalysisController::downloadCsv` — `app/Http/Controllers/Basic/CrossAnalysisController.php:2334` | Không sửa | Bước tải file về sau khi sinh — không chạm cơ chế ghi ô |
| 4 | `Maatwebsite Sheet::appendRows` + `hasStrictNullComparison` — `vendor/maatwebsite/excel/src/Sheet.php:587,702` | Không sửa (vendor) | Nơi đọc interface `WithStrictNullComparison` để truyền cờ xuống PhpSpreadsheet |
| 5 | `PhpSpreadsheet Worksheet::fromArray` — `vendor/phpoffice/phpspreadsheet .../Worksheet.php:3067` | Không sửa (vendor) | Nhánh so sánh lỏng ở dòng 3087 chính là chỗ ô 0 bị bỏ qua |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ExportCrossAnalysis` (class export CSV phân tích chéo) | `app/Exports/ExportCrossAnalysis.php` | Direct | File **duy nhất** thay đổi trong commit `18bee01948` |
| F2 | `CrossAnalysisController::exportCsv` (EP-23 `POST /ajax/cross-analysis/export-csv`) | `app/Http/Controllers/Basic/CrossAnalysisController.php:2178` | Indirect | Caller duy nhất của F1 — hợp đồng response (`file_name`, `file_url`) không đổi |
| F3 | `CrossAnalysisController::downloadCsv` | `app/Http/Controllers/Basic/CrossAnalysisController.php:2334` | Indirect | Luồng tải file sau khi sinh |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | **Không có** — Dev khẳng định fix chỉ đổi cách ghi ô ra file CSV, không đọc/ghi DB. Không cần recover data. |

> ⚠️ Lưu ý cho reviewer: **artifact file CSV** trên storage (`media/csv/<admin_id>/<bot_id>/crossAnalysis_<timestamp>.csv`) là output bị đổi nội dung — Dev không kê ở 4.2 vì không phải data DB.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Cross Analysis (FA-024) — xuất CSV bảng phân tích chéo: ô giá trị 0 nay được ghi ra file thay vì bỏ trống | F1, F2 | Dev đánh giá: phạm vi giới hạn trong đúng 1 file CSV, không đụng export khác |

**Rủi ro / lưu ý khi test (Dev tự nêu):**
- Ô giá trị `null` vẫn bị bỏ qua như cũ nên không đổi hành vi ngoài mong đợi.
- Các cột trước đây đã ép sang chuỗi vẫn ra `0` y như cũ, không đổi kết quả.
- Dữ liệu đưa vào chỉ gồm chuỗi và số nguyên, không có kiểu boolean nên không sinh giá trị lạ trong file.

**Mức verify của Dev: `lint`** (`php -l` + tái hiện cơ chế bằng PhpSpreadsheet thật trong vendor) — **chưa chạy test hành vi end-to-end trên môi trường thật**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TCs
