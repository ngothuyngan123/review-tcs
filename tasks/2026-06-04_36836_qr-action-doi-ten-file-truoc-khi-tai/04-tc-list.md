<!-- sync-target: https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=412698763#gid=412698763 -->
# 04 — TC List (fetched từ Redmine #36836 Link TCs)

> ⚠️ **Đọc trước khi review:** Tab nguồn **"Improve 2026/05/13"** (gid 412698763) là bảng *Improve tracking 37 cột*, **KHÔNG** phải layout TC chuẩn 10 cột. Mapping cột đã áp dụng khi convert:
> - `B` (Main Function) → tiêu đề scenario (chỉ có ở dòng 242)
> - `C` (Sub1) → **Browser** (đưa vào Precondition)
> - `D` (Sub2) → **Setting "Ask where to save each file before downloading" ON/OFF** (đưa vào Precondition)
> - `E` (Sub３) → **Steps** (giữ verbatim)
> - `H` (Actual Result) → **Expected result** (giữ verbatim — cột này chứa nội dung kỳ vọng)
> - `TC ID` + `Title` do `/new-task` sinh (sheet không có cột TC ID; Title suy từ Browser + nội dung Steps). **Steps / Expected / Precondition giữ NGUYÊN giá trị cell.**
> - Browser/Setting ở các dòng nối tiếp là ô gộp (merged) trong sheet → đã carry-forward theo nhóm browser.
> - Dòng **241** trong sheet = nguyên văn đánh giá ảnh hưởng dev (đã đưa vào `03-dev-impact.md`), **không phải TC** → loại khỏi bảng dưới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` (sheet cột Assignee trống; journal Redmine do Ngọc Ánh ghi) |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=412698763#gid=412698763 (tab "Improve 2026/05/13", line 241~260) |

---

## TC List

> Bảng TC dùng **10 cột chuẩn team**. Khi `/sync-tc` push lên Google Sheet master, cột Status sẽ có dropdown 4 giá trị: `OK` / `NG` / `Not test` / `NG -> Đã fix`.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | [Chrome] Đổi tên + chọn nơi lưu trước khi tải (Save As, setting ON) | | | Browser Chrome; "Ask where to save each file before downloading" = ON | 1. Mở popup QRコード trên header.<br>2. Bấm nút tải QR.<br>3. Ở hộp thoại "Lưu thành", đổi tên file (vd qr-vip.png) + chọn thư mục khác Download mặc định.<br>4. Bấm Lưu. | Bước 2: hiện hộp thoại Save As của trình duyệt (không tự tải ngay như trước).<br>Bước 4: file QR được lưu đúng tên qr-vip.png + đúng thư mục đã chọn.<br>Mở file → đúng ảnh QR thêm bạn. | | | |
| TC002 | [Chrome] Double-click nút tải — không mở 2 picker | | | Browser Chrome; setting ON | 1. Mở popup QRコード.<br>2. Double-click nhanh nút tải QR. | Chỉ 1 hộp thoại Save As (hoặc 1 prompt) được mở; không bật 2 picker chồng nhau.<br>Hoàn tất 1 lần → chỉ 1 file được tải, không file trùng. | | | |
| TC003 | [Chrome] Đổi tên file ký tự đặc biệt / JP | | | Browser Chrome; setting ON | 1. Mở popup QRコード → bấm tải.<br>2. Đổi tên thành tên có ký tự đặc biệt / JP, vd QR テスト①.png.<br>3. Lưu. | File lưu với đúng tên (theo mức trình duyệt/OS cho phép), đuôi .png giữ nguyên, mở được.<br>Không lỗi JS / không treo picker. | | | |
| TC004 | [Chrome] Regression các màn tải file khác | | | Browser Chrome; setting ON | Truy cập được các màn => thực hiện chức nắng tải file | Mỗi màn vẫn tải file bình thường như trước fix | | | |
| TC005 | [Chrome] Tải lặp nhiều lần liên tiếp | | | Browser Chrome; setting ON | 1. Mở popup QRコード → tải QR (hoàn tất).<br>2. Tải lại lần 2, lần 3 liên tiếp.<br>3. Đóng/mở lại popup rồi tải tiếp. | Mỗi lần bấm tải đều mở lại Save As/prompt và tải đúng file.<br>Không bị "kẹt" sau lần đầu (state async không bị treo), không lỗi JS, không tải trùng ngoài ý muốn. | | | |
| TC006 | [Chrome] Đổi tên + chọn nơi lưu (setting OFF) | | | Browser Chrome; "Ask where to save each file before downloading" = OFF | 1. Mở popup QRコード trên header.<br>2. Bấm nút tải QR.<br>3. Ở hộp thoại "Lưu thành", đổi tên file (vd qr-vip.png) + chọn thư mục khác Download mặc định.<br>4. Bấm Lưu. | Bước 2: hiện hộp thoại Save As của trình duyệt (không tự tải ngay như trước).<br>Bước 4: file QR được lưu đúng tên qr-vip.png + đúng thư mục đã chọn.<br>Mở file → đúng ảnh QR thêm bạn. | | | |
| TC007 | [Edge] Đổi tên + chọn nơi lưu trước khi tải (Save As, setting ON) | | | Browser Edge; setting ON | 1. Mở popup QRコード trên header.<br>2. Bấm nút tải QR.<br>3. Ở hộp thoại "Lưu thành", đổi tên file (vd qr-vip.png) + chọn thư mục khác Download mặc định.<br>4. Bấm Lưu. | Bước 2: hiện hộp thoại Save As của trình duyệt (không tự tải ngay như trước).<br>Bước 4: file QR được lưu đúng tên qr-vip.png + đúng thư mục đã chọn.<br>Mở file → đúng ảnh QR thêm bạn. | | | |
| TC008 | [Edge] Double-click nút tải — không mở 2 picker | | | Browser Edge; setting ON | 1. Mở popup QRコード.<br>2. Double-click nhanh nút tải QR. | Chỉ 1 hộp thoại Save As (hoặc 1 prompt) được mở; không bật 2 picker chồng nhau.<br>Hoàn tất 1 lần → chỉ 1 file được tải, không file trùng. | | | |
| TC009 | [Edge] Đổi tên file ký tự đặc biệt / JP | | | Browser Edge; setting ON | 1. Mở popup QRコード → bấm tải.<br>2. Đổi tên thành tên có ký tự đặc biệt / JP, vd QR テスト①.png.<br>3. Lưu. | File lưu với đúng tên (theo mức trình duyệt/OS cho phép), đuôi .png giữ nguyên, mở được.<br>Không lỗi JS / không treo picker. | | | |
| TC010 | [Edge] Regression các màn tải file khác | | | Browser Edge; setting ON | Truy cập được các màn => thực hiện chức nắng tải file | Mỗi màn vẫn tải file bình thường như trước fix | | | |
| TC011 | [Edge] Tải lặp nhiều lần liên tiếp | | | Browser Edge; setting ON | 1. Mở popup QRコード → tải QR (hoàn tất).<br>2. Tải lại lần 2, lần 3 liên tiếp.<br>3. Đóng/mở lại popup rồi tải tiếp. | Mỗi lần bấm tải đều mở lại Save As/prompt và tải đúng file.<br>Không bị "kẹt" sau lần đầu (state async không bị treo), không lỗi JS, không tải trùng ngoài ý muốn. | | | |
| TC012 | [Edge] Đổi tên + chọn nơi lưu (setting OFF) | | | Browser Edge; "Ask where to save each file before downloading" = OFF | 1. Mở popup QRコード trên header.<br>2. Bấm nút tải QR.<br>3. Ở hộp thoại "Lưu thành", đổi tên file (vd qr-vip.png) + chọn thư mục khác Download mặc định.<br>4. Bấm Lưu. | Bước 2: hiện hộp thoại Save As của trình duyệt (không tự tải ngay như trước).<br>Bước 4: file QR được lưu đúng tên qr-vip.png + đúng thư mục đã chọn.<br>Mở file → đúng ảnh QR thêm bạn. | | | |
| TC013 | [Firefox] Đổi tên + chọn nơi lưu trước khi tải (fallback prompt, setting ON) | | | Browser Firefox; setting ON | 1. Mở popup QRコード trên header.<br>2. Bấm nút tải QR.<br>3. Ở hộp thoại "Lưu thành", đổi tên file (vd qr-vip.png) + chọn thư mục khác Download mặc định.<br>4. Bấm Lưu. | Bước 2: hiện hộp thoại Save As của trình duyệt (không tự tải ngay như trước).<br>Bước 4: file QR được lưu đúng tên qr-vip.png + đúng thư mục đã chọn.<br>Mở file → đúng ảnh QR thêm bạn. | | | |
| TC014 | [Firefox] Double-click nút tải — không mở 2 picker | | | Browser Firefox; setting ON | 1. Mở popup QRコード.<br>2. Double-click nhanh nút tải QR. | Chỉ 1 hộp thoại Save As (hoặc 1 prompt) được mở; không bật 2 picker chồng nhau.<br>Hoàn tất 1 lần → chỉ 1 file được tải, không file trùng. | | | |
| TC015 | [Firefox] Đổi tên file ký tự đặc biệt / JP | | | Browser Firefox; setting ON | 1. Mở popup QRコード → bấm tải.<br>2. Đổi tên thành tên có ký tự đặc biệt / JP, vd QR テスト①.png.<br>3. Lưu. | File lưu với đúng tên (theo mức trình duyệt/OS cho phép), đuôi .png giữ nguyên, mở được.<br>Không lỗi JS / không treo picker. | | | |
| TC016 | [Firefox] Regression các màn tải file khác | | | Browser Firefox; setting ON | Truy cập được các màn => thực hiện chức nắng tải file | Mỗi màn vẫn tải file bình thường như trước fix | | | |
| TC017 | [Firefox] Tải lặp nhiều lần liên tiếp | | | Browser Firefox; setting ON | 1. Mở popup QRコード → tải QR (hoàn tất).<br>2. Tải lại lần 2, lần 3 liên tiếp.<br>3. Đóng/mở lại popup rồi tải tiếp. | Mỗi lần bấm tải đều mở lại Save As/prompt và tải đúng file.<br>Không bị "kẹt" sau lần đầu (state async không bị treo), không lỗi JS, không tải trùng ngoài ý muốn. | | | |
| TC018 | [Firefox] Đổi tên + chọn nơi lưu (setting OFF) | | | Browser Firefox; "Ask where to save each file before downloading" = OFF | 1. Mở popup QRコード trên header.<br>2. Bấm nút tải QR.<br>3. Ở hộp thoại "Lưu thành", đổi tên file (vd qr-vip.png) + chọn thư mục khác Download mặc định.<br>4. Bấm Lưu. | Bước 2: hiện hộp thoại Save As của trình duyệt (không tự tải ngay như trước).<br>Bước 4: file QR được lưu đúng tên qr-vip.png + đúng thư mục đã chọn.<br>Mở file → đúng ảnh QR thêm bạn. | | | |
| TC019 | [Mac] Cross-browser Chrome/Edge/Firefox/Safari | | | Máy Mac; Chrome, Edge, Firefox, Safari | (Sheet không ghi steps — kiểm tra tổng hợp đa trình duyệt trên macOS) | Chrome/Edge: hiện Save As (đổi tên + chọn nơi lưu).<br>Firefox/Safari: hiện prompt đổi tên rồi tải qua blob URL.<br>Mọi browser đều tải được file QR hợp lệ, không lỗi JS | | | |

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). TC trong sheet phụ thuộc browser + setting OS "Ask where to save each file before downloading" → ghi rõ trong cột Precondition.

---

## Member tự check trước khi submit

> Sheet nguồn do reviewer paste, các checkbox dưới để **member verify lại** sau khi đối chiếu file 01 + 03.

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (luồng Save As đổi tên + chọn nơi lưu)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3 (các màn tải file dùng chung endpoint)
- [ ] Có cover nhánh **fallback** (browser không hỗ trợ File System Access API → prompt) — TC013–TC018 (Firefox), TC019 (Firefox/Safari)
- [ ] Có cover nhánh **Hủy** (AbortError / hủy prompt) — ⚠️ *sheet chưa có TC cho case này, xem ghi chú review bên dưới*

<!--
Source: fetched từ Redmine #36836 Link TCs, range A241:J260 tab "Improve 2026/05/13" (gid 412698763) lúc 2026-06-04 20:25.
KHÔNG sửa TCs này nếu chưa confirm với Leader.

Main Function (cell B241→B242, nguyên văn): "Check downloadQr(): popup QRコード header v2 → mở Save As cho đổi tên + chọn nơi lưu trước khi tải"

Gợi ý cho /review-tc (chưa áp dụng, để Leader cân nhắc — KHÔNG phải nội dung sheet):
- Mục 2 (cách fix) nêu rõ nhánh "Bấm Hủy ở hộp thoại (AbortError) hoặc hủy ở prompt → dừng, không tải" nhưng 19 TC trong sheet CHƯA có TC nào verify nhánh hủy → khả năng GAP cho cách-fix.
- Setting OFF (TC006/012/018): cần xác nhận expected khi "Ask where to save" = OFF có còn hiện Save As/prompt hay tải thẳng — expected trong sheet đang để giống hệt case ON, Leader nên review lại.
-->
