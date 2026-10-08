# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | `e73e25a4cca161ce3baef1284f4d342522bd6918` |
| Branch | `m_202609_fix_salon_csv_41972` |
| Ngày submit đánh giá | 2026-10-03 |
| Auto-filled | 2026-10-05 by /new-task (nguồn: Journal #139898 — Thanh Duy Nguyen — 2026-10-03) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (Journal #139898) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- `HandleExportSalonCalendarTask.convertToStringLine` bọc giá trị trong `"..."` nhưng không escape dấu `"` => tên LINE user (vd `つか咲"き`) hoặc title sự kiện Google có `"` làm lệch cột khi mở CSV.
- Cùng method còn `replaceAll("null","")` trên cả dòng đã ghép => cắt luôn chữ "null" nằm trong dữ liệu thật (vd `Nullpo`, `null@gmail.com`). Lỗi này có ở cả `HandleExportCsvTask`.

## 2. Cách fix

- Sửa `convertToStringLine` ở 2 file: escape `"` thành `""` cho từng giá trị (file salon chưa có), ô null hoặc đúng bằng chuỗi `"null"` thành rỗng, bỏ `replaceAll("null","")` ở cuối dòng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `convertToStringLine` là **private**, signature không đổi — 2 caller trong `HandleExportSalonCalendarTask` (header + data) | Không cần sửa caller | Chỉ đổi logic nội bộ của method, caller chỉ gọi và nhận string đã build |
| 2 | 2 caller trong `HandleExportCsvTask` (`writeCsv`) | Không cần sửa caller | Tương tự trên |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `convertToStringLine` | `HandleExportSalonCalendarTask` | Direct | Job CSV lịch sử sync salon ↔ Google Calendar |
| F2 | `convertToStringLine` | `HandleExportCsvTask` | Direct | Job CSV danh sách bạn bè — cùng bug, cùng cách fix |

### 4.2. List data bị update khi fix bug

<!-- Dev ghi: "Không có (chỉ sửa code, file CSV đã xuất trước đó không đổi)" -->

Không có. File CSV đã xuất trước khi deploy bản fix **không** tự động thay đổi — phải xuất lại mới có dữ liệu đúng.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | CSV lịch sử sync salon ↔ Google Calendar (cả 2 chiều) — test friend có `"` trong tên/view name, sự kiện Google có `"` trong tiêu đề, mở Excel kiểm tra không lệch cột | F1 | High |
| T2 | CSV danh sách bạn bè — friend chưa từng nhắn tin (cột 最終メッセージ受信日時 phải rỗng) và friend không có ngày sinh (cột 年齢 phải rỗng); 2 cột này trước đây dựa vào `replaceAll` để xoá "null" | F2 | High |
| T3 | CSV danh sách bạn bè — friend có chữ "null" trong tên/email (vd `null@gmail.com`): sau fix phải **giữ nguyên**, trước fix bị cắt | F2 | Medium |
| T4 | CSV danh sách bạn bè — bỏ chọn cột 対応マーク / 流入経路 rồi xuất: các cột còn lại không lệch và không hiện chữ "null" | F2 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
