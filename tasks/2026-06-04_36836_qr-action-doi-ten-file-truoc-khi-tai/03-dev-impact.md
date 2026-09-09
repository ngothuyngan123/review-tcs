# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Do Van Tu TuDV` (assigned_to Redmine; Section B không ghi rõ dev) |
| Commit / Pull Request | `<chưa có>` (Redmine không có link commit/PR; custom field "Commit Date" trống) |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-04` (journal Ngọc Ánh) |
| Auto-filled | `2026-06-04 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- Đây là yêu cầu cải tiến spec (không phải bug). Theo logic cũ, khi bấm nút tải QR ở popup QRコード trên header, file QR được tải xuống ngay lập tức, không cho người dùng đổi tên file hay chọn nơi lưu.
- Code cũ tạo sẵn link download với tên file lấy từ đường dẫn ảnh rồi tự động click tải, nên không có bước cho người dùng can thiệp tên/đường dẫn lưu.

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Chuyển hàm `downloadQr()` sang async và bổ sung hộp thoại "Lưu thành" của trình duyệt qua File System Access API (`window.showSaveFilePicker`) để cho phép đổi tên file + chọn nơi lưu trước khi tải. Picker được mở ngay trong cú click (trước khi gọi AJAX) để giữ user-gesture.
- Sau khi AJAX trả dữ liệu base64, giải mã thành Blob: nếu trình duyệt hỗ trợ và người dùng đã chọn file → ghi thẳng vào file đó (đã đổi tên + chọn nơi lưu).
- Trường hợp trình duyệt không hỗ trợ Save As → fallback dùng `window.prompt` cho nhập/đổi tên file rồi tải bằng blob URL như cũ.
- Bấm Hủy ở hộp thoại (AbortError) hoặc hủy ở prompt → dừng, không tải.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `downloadQr()` — nút tải trong popup QRコード ở header v2 (`header-content.blade.php`) | Đây là caller DUY NHẤT của `downloadQr()` | Không có caller khác bị ảnh hưởng |
| 2 | Endpoint AJAX `/ajax/download-file-chat11` | KHÔNG sửa (chỉ thay đổi logic client xử lý response) | Endpoint còn dùng ở các màn khác (qr_code v2, chat-v2, setting add friend) nhưng những nơi đó có hàm tải riêng → đã check, không ảnh hưởng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `downloadQr()` | `public/js/layout_v2_header.js` | Direct | Hàm được sửa: async + `window.showSaveFilePicker` + fallback `window.prompt` |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Chỉ sửa logic client-side cách tải file, không ghi/đổi dữ liệu DB hay API (nguyên văn Dev: "k có") |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Tải QR code thêm bạn (QRコードアクション) từ popup QRコード trên header v2 | F1 | Medium (suy luận — Dev liệt kê là tính năng bị ảnh hưởng, không ghi mức) |
| T2 | Các màn dùng chung endpoint `/ajax/download-file-chat11`: qr_code v2, chat-v2, setting add friend | Mục 3 | Low (Dev đã check — các màn này có hàm tải riêng, endpoint không sửa) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- Ghi chú parse:
- Nguồn: journal của Ngọc Ánh trên Redmine #36836 (created_on 2026-06-04T04:17:39Z) — chứa cả "Tái hiện bug", "Đánh giá ảnh hưởng phía dev", "Link TCs".
- Mục 2 (cách fix) là điểm cần cover kỹ: fix kiểu generic theo browser capability (có/không hỗ trợ File System Access API) → cần test ≥ 2 nhánh (hỗ trợ Save As vs. fallback prompt) + nhánh hủy (AbortError / hủy prompt). TC trong file 04 đã cover Chrome/Edge (Save As) + Firefox/Safari (fallback prompt).
-->
