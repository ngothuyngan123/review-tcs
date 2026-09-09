# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Nguồn: báo cáo AI AUTO-FIXBUG** (journal Redmine #128945 / #128946 ngày 2026-08-13, user `AI LME Fix bug`) — **không phải Dev người viết**. Mức verify Dev tự khai chỉ là `lint`, **chưa chạy trên trình duyệt thật**.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — QA nhận: `Ngô Thúy Ngần` |
| Commit / Pull Request | commit `233c4ae7b2` (repo `sns-line`) — không có link Github/Gitlab. Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=39592 |
| Branch | `ai_small_39592` (nhánh gốc `release_step_20260805`) — đã push lên origin |
| Ngày submit đánh giá | `2026-08-13` |
| Auto-filled | `2026-08-13 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn từ journal Redmine.

Biên lai PDF được dựng bằng cách chụp lại chính khối HTML `#invoice_page_x` trên trang (html2canvas + jsPDF). Sau khi nhận dữ liệu mới, mixin biên lai gán dữ liệu rồi gọi hàm chờ phần tử `#invoice_pdf` — nhưng đó là khối BAO NGOÀI luôn có sẵn trong trang, nên hàm chờ kết thúc ngay lập tức, chưa qua vòng vẽ lại của Vue. Các trang biên lai bên trong lại dùng `v-show` nên sau lần tải trước vẫn nằm nguyên trong trang (chỉ bị ẩn) kèm nội dung CŨ, khiến thư viện chụp trúng bảng kê của lần tải trước. Vì vậy tải biên lai tháng 7 xong rồi chuyển sang tháng 6 tải tiếp thì file PDF vẫn ra bảng kê tháng 7, dù dữ liệu máy chủ trả về đã đúng tháng 6. Lần tải ĐẦU TIÊN sau khi mở trang luôn đúng vì lúc đó các trang biên lai chưa tồn tại nên hàm chờ buộc phải đợi Vue vẽ xong.

## 2. Cách fix

> Nguyên văn từ journal Redmine.

Giữ NGUYÊN cả 2 lời gọi `waitForElement` (kể cả selector `#invoice_pdf` ở `handleResponsePdf` và `#invoice_page_x` ở `generateCanvas`), chỉ thêm điều kiện cần để nó chờ đúng thứ:

1. Template biên lai đổi `v-show` sang `v-if` để khối trang biên lai bị huỷ hẳn sau mỗi lần tải thay vì chỉ bị ẩn;
2. `handleResponsePdf` tắt hiển thị trước rồi đợi một vòng `$nextTick` cho Vue xoá xong khối cũ, sau đó mới gán dữ liệu mới và gọi `waitForElement` như cũ.

Nhờ vậy khi bắt đầu chụp, trang biên lai chắc chắn KHÔNG còn node của lần tải trước, nên hàm chờ trong `generateCanvas` buộc phải đợi Vue vẽ lại từ dữ liệu mới rồi mới chụp — đúng như lần tải đầu tiên vốn luôn ra đúng tháng. Đồng thời bịt luôn trường hợp lần tải trước hỏng giữa chừng làm khối biên lai còn sót lại trong trang.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `handleResponsePdf` — `public/_assets/modules/bill/js/mixins/invoices.js` | **CÓ SỬA** — tắt hiển thị + `$nextTick` trước khi gán data mới | Điểm fix chính: bảo đảm node cũ bị huỷ trước khi chờ/chụp |
| 2 | `waitForElement` — `public/_assets/modules/bill/js/mixins/invoices.js` | GIỮ NGUYÊN, không sửa | Cơ chế chờ vốn đúng, chỉ bị vô hiệu vì node cũ còn trong DOM |
| 3 | `downloadPdf` / `generateCanvas` — `public/_assets/modules/bill/js/mixins/invoices.js` | GIỮ NGUYÊN, không sửa | Đã có sẵn `waitForElement('#invoice_page_'+i)` |
| 4 | `invoice_pdf` template — `resources/views/basic/payment_history/invoice_pdf.blade.php` | **CÓ SỬA** — `v-show` → `v-if` | Huỷ hẳn node trang biên lai sau mỗi lần tải |
| 5 | `downloadInvoices` / `remoteLoadData` / `remoteHandleResponse` — `public/js/payment_history/index.js` | Đã check, không sửa | Caller của mixin ở màn Lịch sử thanh toán |
| 6 | `downloadInvoices` — `public/_assets/modules/bill/js/detail.js` | Đã check, không sửa | Màn Chi tiết hợp đồng dùng chung mixin |
| 7 | `Basic\UserController::ajaxPaymentHistories` / `handleTotalPagePdf` — `app/Http/Controllers/Basic/UserController.php` | Đã check, không sửa | Tầng dữ liệu + tính số trang; xác nhận lỗi nằm ở tầng hiển thị |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Mục 4.1 của báo cáo AI ghi **"File thay đổi"** chứ không ghi function — bảng dưới do `/new-task` map lại từ mục 2 + 3, **tester verify lại với Dev**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `handleResponsePdf` | `public/_assets/modules/bill/js/mixins/invoices.js` | Direct | Sửa trực tiếp — thêm bước tắt hiển thị + `$nextTick` |
| F2 | Template `invoice_pdf` (khối `#invoice_page_x`) | `resources/views/basic/payment_history/invoice_pdf.blade.php` | Direct | `v-show` → `v-if` — vòng đời node đổi hoàn toàn |
| F3 | `generateCanvas` / `waitForElement` / `downloadPdf` | `public/_assets/modules/bill/js/mixins/invoices.js` | Indirect | Không sửa code nhưng **hành vi runtime đổi** (nay thực sự phải chờ Vue render) |
| F4 | `downloadInvoices` / `remoteLoadData` / `remoteHandleResponse` | `public/js/payment_history/index.js` | Indirect | Caller màn Lịch sử thanh toán, dùng mixin đã sửa |
| F5 | `downloadInvoices` | `public/_assets/modules/bill/js/detail.js` | Indirect | Caller màn Chi tiết hợp đồng, dùng chung mixin + template |

**Diff thực tế Dev khai**: 2 file, +18 / −6 dòng.

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | **Dev khai: Không có.** Chỉ đổi thứ tự dựng lại giao diện phía trình duyệt, không truy vấn thêm và không ghi dữ liệu |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Payment History (FS-009)** — 「決済履歴・領収書のダウンロード」 (`/basic/payment-history`): tải biên lai hàng loạt (`一括ダウンロード`) và tải từng dòng (`個別発行`) | F1, F2, F3, F4 | High |
| T2 | **Contract Plan & Payment (FA-031)** — màn Chi tiết hợp đồng (`/basic/detail-contract/{id}`): nút 「過去決済分の領収書ダウンロード」, include cùng template + dùng chung mixin nên **cũng được sửa theo** | F1, F2, F3, F5 | High |

---

## 5. Recover data (từ báo cáo AI)

✔ Không cần recover data.

## 6. Verify Dev đã chạy (từ báo cáo AI)

| Hạng mục | Nội dung |
|---|---|
| Mức verify | **`lint`** — ⚠️ chỉ lint, **không** chạy runtime |
| Lệnh đã chạy | `php -l ...invoice_pdf.blade.php` → No syntax errors · `node --check ...invoices.js` → OK · `grep waitForElement` → còn đủ 4 chỗ · `git diff --stat` → 2 file, 18 thêm 6 bớt |
| **Chưa verify được** | Bằng trình duyệt thật — container không có trình duyệt, không kết nối được MySQL dev (`host.docker.internal:3306` Connection refused) |

**Bằng chứng Dev đưa ra** (nguyên văn, rút gọn): `generateCanvas` đã có sẵn `waitForElement('#invoice_page_'+i)` — cơ chế chờ đúng vốn tồn tại, chỉ bị vô hiệu vì `v-show` để node cũ nằm lại trong DOM · Lần tải đầu tiên luôn đúng vì lúc đó `#invoice_page_x` chưa tồn tại nên hàm chờ phải poll 30ms tới khi Vue vẽ xong · `waitForElement` chạy `check()` ĐỒNG BỘ ở lần đầu nên chỉ có tác dụng khi phần tử đang thực sự vắng mặt · html2canvas 0.4.1 (bản CDN) chụp trực tiếp phần tử DOM sống, không nhân bản trước · `handleTotalPagePdf` trả về 1 ngay cả khi 0 bản ghi nên `#invoice_page_1` luôn xuất hiện, không có nguy cơ chờ hết 5 giây.

## 7. Rủi ro / lưu ý khi test (Dev tự nêu — nguyên văn)

1. **Chưa chạy được trên trình duyệt trong container** — QA cần thử: tải tháng A rồi đổi sang tháng B tải tiếp mà **KHÔNG tải lại trang**, cả tải hàng loạt lẫn tải từng dòng, và trường hợp biên lai nhiều trang (trên 10 giao dịch).
2. Đổi `v-show` sang `v-if` khiến khối biên lai bị dựng lại mỗi lần tải; danh sách rất dài trên máy yếu có thể dựng lâu hơn chút nhưng vẫn nằm trong **5 giây chờ** của `waitForElement`.
3. Biên lai nhiều trang **vẫn còn lỗi có sẵn về thứ tự trang** (các trang được chụp song song, trang mới được thêm ngay trong lúc chụp) — **không thuộc phạm vi ticket**, cần theo dõi riêng.
4. File tĩnh đi kèm **tham số phiên bản** (`config sns-line.version`) — khi lên bản vá cần bảo đảm phiên bản được tăng để trình duyệt khách không dùng lại bản JS cũ trong bộ nhớ đệm. ⚠️ Commit fix **KHÔNG** thay đổi giá trị config đó.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ báo cáo gốc chỉ ghi *file*, bảng F1–F5 là map lại, cần confirm
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — ⚠️ Dev khai "không có data"; nhưng **file PDF gửi khách chính là output cần verify**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm Leader cần chất vấn

- Mức verify của Dev chỉ là **`lint`** — chưa có một lần chạy thật nào. Toàn bộ rủi ro runtime dồn sang QA.
- Fix chạm **vòng đời DOM** (`v-show` → `v-if`) ở template dùng chung 2 màn → regression phải chạy **cả 2 màn** (T1 + T2), không suy ra từ 1 màn.
- **Rủi ro cache JS bản cũ** (mục 7.4) là rủi ro *release*, không phải rủi ro code — nếu quy trình deploy không tăng `sns-line.version`, KH F5 thường vẫn dính bug. Cần chốt với Dev/DevOps trước khi release.
- Lỗi **thứ tự trang biên lai nhiều trang** được Dev khai là *lỗi có sẵn ngoài phạm vi* — Leader quyết định có tách ticket riêng không.
