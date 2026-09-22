# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38674 — [CSV][Cross-analysis] File download csv để trống 1 số cột trong khi dữ liệu khi export trên web đang là 0` |
| Module / Màn hình | Cross-analysis (クロス分析 — phân tích chéo) — màn kết quả 分析リスト, chức năng xuất CSV |

## Mô tả bug (bản dịch tiếng Việt)

Trên màn クロス分析 (cross-analysis), khi bảng kết quả có các ô giá trị = 0, file CSV tải về bị **để trống** ở 2 cột 対象人数 (số người đối tượng) và 合計 (tổng), trong khi trên web 2 cột này vẫn đang hiển thị giá trị 0.

Kỳ vọng: file CSV phải fill giá trị 0 vào 2 cột đó, đúng như đang hiển thị trên web.

Evidence (ảnh chụp màn hình do người báo cung cấp): https://prnt.sc/fwL60SHxU9Wn

## Steps to reproduce

1. Chuẩn bị màn cross-analysis có dữ liệu, giá trị các cột = 0.
2. User thực hiện export (CSV) → export done.
3. Open file download, check hiển thị nội dung file.

## Expected result

- Bước 3: file CSV hiển thị fill giá trị vào 2 cột 対象人数 và 合計 = `0`.

## Actual result

- Bước 3: nội dung file hiển thị 2 cột 対象人数 và 合計 **đang không có giá trị** (ô trống).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine attachments (0): không có file đính kèm trực tiếp trên ticket. -->

- Evidence link trong description: https://prnt.sc/fwL60SHxU9Wn (link ngoài, không phải attachment Redmine)

## Ghi chú thêm của Leader

- **Precondition bắt buộc**: 分析リスト phải có ít nhất 1 ô giá trị `0` trên bảng kết quả (vd trục cơ sở là tag chưa gắn cho bạn bè nào, hoặc 分析項目 có điều kiện lọc không khớp ai). Bảng phải đã tính xong (không còn trạng thái đang xử lý).
- **Chữ ký lỗi cần phân biệt**: theo phân tích của Dev, chỉ 2 cột 対象人数 và 合計 bị trống vì đẩy **số nguyên**; các cột 有効 / ブロック / 被ブロック đã được ép sang **chuỗi** nên vẫn hiện `0` bình thường. Khi tái hiện phải thấy đúng chữ ký này (2 ô trống + 3 ô có `0`) mới là đúng bug của ticket.
- **Không phải bug của ticket này**: nhãn 「ブロック」/「被ブロック」 bị hoán đổi so với tên field nội bộ (quirk đã ghi trong feature-spec) — web và CSV đọc giống nhau nên không kết luận là lỗi ở đây.
- **Ô null vẫn để trống sau fix** — đây là hành vi đúng, không phải bug tồn đọng. Chỉ ô giá trị `0` mới phải được ghi ra.
- **File CSV đã tải TRƯỚC khi fix vẫn giữ ô trống** — không cần và không được coi là bug tồn đọng.
- **Retention**: dữ liệu kết quả phân tích chỉ giữ **8 ngày** (feature-spec §7) → TC dùng 「更新履歴」 mốc cũ có thể không dựng được nếu quá hạn.
- Lỗi tái hiện **100%** khi có ô giá trị 0 (do cơ chế so sánh của thư viện, không phải lỗi xác suất).
- Môi trường phát hiện: ticket không ghi rõ env; bộ TC trên Studio hiện mới chỉ chạy ở `local`.
- Tracker Redmine = **Bug tự detect**; status hiện tại = **Fix done - Đợi test**.

## Journal / note từ Redmine (nguyên văn)

**Journal #133057 — AI LME Fix bug — 2026-08-26:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Lớp xuất CSV của màn Phân tích chéo không bật chế độ so sánh nghiêm ngặt, nên thư viện xuất Excel quyết định có ghi ô hay không bằng phép so sánh lỏng (giá trị khác null). Trong PHP số nguyên 0 được coi là bằng null, vì vậy mọi ô mang giá trị 0 bị bỏ qua và ra file thành ô trống. Hai cột Số người đối tượng và Tổng đang đẩy số nguyên nên bị trống; các cột còn lại trước đó đã được ép sang chuỗi nên vẫn hiện 0.

■ 2. CÁCH FIX
Bật so sánh nghiêm ngặt (WithStrictNullComparison) cho lớp xuất CSV của màn Phân tích chéo, nhờ đó ô có giá trị 0 được ghi thẳng vào file thay vì bị thư viện bỏ qua — 2 cột Số người đối tượng và Tổng nay hiện đúng 0 như trên web. Sửa tại gốc cơ chế ghi ô nên đúng cho mọi cột số của file này, không chỉ 2 cột đang lỗi. Quét ngang: cùng kiểu lỗi còn ở vài lớp xuất CSV khác (thống kê click landing, lịch sử đơn hàng, đặt chỗ) nhưng ngoài phạm vi ticket, chỉ ghi nhận.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
ExportCrossAnalysis::map / headings (app/Exports/ExportCrossAnalysis.php)
CrossAnalysisController::exportCsv (app/Http/Controllers/Basic/CrossAnalysisController.php:2178)
CrossAnalysisController::downloadCsv (app/Http/Controllers/Basic/CrossAnalysisController.php:2334)
Maatwebsite Sheet::appendRows + hasStrictNullComparison (vendor/maatwebsite/excel/src/Sheet.php:587,702)
PhpSpreadsheet Worksheet::fromArray (vendor/phpoffice/phpspreadsheet Worksheet.php:3067)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Exports/ExportCrossAnalysis.php
 • 4.2 Data ảnh hưởng:
   - Không có — fix chỉ đổi cách ghi ô ra file CSV, không đọc/ghi DB
 • 4.3 Tính năng liên quan:
   - Cross Analysis (FA-024) — xuất CSV bảng phân tích chéo: ô giá trị 0 nay được ghi ra file thay vì bỏ trống

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Exports/ExportCrossAnalysis.php: No syntax errors detected; Tái hiện cơ chế bằng PhpSpreadsheet thật trong vendor của repo: fromArray với strictNullComparison=false, hàng [row1, 0, 0, chuỗi 0] ra CSV thành row1 + 2 ô TRỐNG + 0; với strictNullComparison=true ra đủ row1,0,0,0; Kiểm tra lớp sau khi sửa: instanceof WithStrictNullComparison = true (Sheet::hasStrictNullComparison sẽ trả true)
   Bằng chứng: config/excel.php:45 strict_null_comparison = false (mặc định toàn hệ thống nên phải khai báo ở từng lớp export); PhpSpreadsheet Worksheet::fromArray dòng 3087 — nhánh không strict so sánh lỏng nên số nguyên 0 bị bỏ qua, không ghi ô; PHP 7.4: (0 khác null) = false, (chuỗi 0 khác null) = true — giải thích vì sao chỉ 2 cột đẩy số nguyên bị trống

■ TỰ REVIEW (AI)
Fix đúng gốc: nguyên nhân nằm ở phép so sánh khi thư viện ghi ô chứ không phải ở chỗ tính toán số liệu. Khai báo WithStrictNullComparison chỉ trên lớp export của màn Phân tích chéo (lớp này chỉ được dùng bởi CrossAnalysisController::exportCsv, đã grep xác nhận) nên phạm vi ảnh hưởng giới hạn trong đúng 1 file CSV, không đụng các export khác.
 • Rủi ro / lưu ý khi test:
   - Ô giá trị null vẫn bị bỏ qua như cũ nên không đổi hành vi ngoài mong đợi
   - Các cột trước đây đã ép sang chuỗi vẫn ra 0 y như cũ, không đổi kết quả
   - Dữ liệu đưa vào chỉ gồm chuỗi và số nguyên, không có kiểu boolean nên không sinh giá trị lạ trong file

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_38674 (nhánh gốc release_step_20260805, commit 18bee01948, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 5 phút 11 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=01fe5dbd-f1e9-4be7-8968-659f07f2cb00
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=38674
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
