# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kieu Son Tung` (assigned_to) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-12` |
| Auto-filled | `2026-06-13 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Redmine #37396 journal (Kim Cúc, 2026-06-12) -->

- Khi tạo landing bị missing `google_sheet_id`.

## 2. Cách fix

<!-- Nguyên văn từ Redmine -->

- Khi chạy job ghi data hàng ngày, check những bot đã liên kết Google Sheet mà có landing bị missing `google_sheet_id` thì sẽ tạo sheet mới và insert data.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- ⚠️ Dev KHÔNG liệt kê nội dung mục 3 trong Redmine (chỉ có tiêu đề). Tester hỏi lại Dev nếu nghi sót caller. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Dev chưa cung cấp>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn 4.1 từ Redmine -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `createSheetForLanding()` | `app/Console/Commands/JobInsertStatisticDataActionLandingToGoogleSheet.php` | Direct | Tạo sheet mới cho landing thiếu `google_sheet_id` |
| F2 | `handle()` | `app/Console/Commands/JobInsertStatisticDataActionLandingToGoogleSheet.php` | Direct | Entry point job ghi data landing hàng ngày |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn 4.2 từ Redmine: "Không có" -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có (theo Dev) | — | ⚠️ Lưu ý: cách fix có mô tả "tạo sheet mới và insert data" + "google_sheet_id được cập nhật vào landing" (theo expected TC) → tester cân nhắc xác minh lại với Dev xem field `landing.google_sheet_id` có thực sự bị UPDATE không. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn 4.3 từ Redmine -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Job ghi data landing hàng ngày (sync data lên Google Sheet) | F1, F2 | `<Dev chưa ghi mức độ>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ Dev để trống mục 3
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — ⚠️ kiểm tra lại field `google_sheet_id`
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
