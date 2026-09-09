# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Phương` (người submit đánh giá ảnh hưởng) |
| Commit / Pull Request | `https://bitbucket.org/snstool/sns-line/pull-requests/10420/diff` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-22` |
| Auto-filled | `2026-06-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- đang order theo id
- dropdown chọn bot không hoạt động

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- sửa order bug theo time access
- sửa dropdown list bot

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

> Dev chỉ ghi heading mục 3, không liệt kê bảng chi tiết. Các function liên quan được Dev liệt kê ở mục 4.1 bên dưới.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Dev chưa liệt kê chi tiết — xem 4.1>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `detailBot` | `app/Http/Controllers/Admin/SupperAdminController.php` | `<Dev chưa ghi Direct/Indirect>` | |
| F2 | `getAccessHistories` | `app/Http/Controllers/Admin/UserController.php` | `<Dev chưa ghi>` | |
| F3 | `exportCsvAccessHistory` | `app/Http/Controllers/Admin/UserController.php` | `<Dev chưa ghi>` | |
| F4 | (JS màn lịch sử access) | `public/js/admin/employees/access_histories.js` | `<Dev chưa ghi>` | dropdown chọn bot |
| F5 | (View màn lịch sử access) | `resources/views/admin/employee/access_histories.blade.php` | `<Dev chưa ghi>` | |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

> Dev ghi: **Không có**.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có (Dev confirm) | — | Fix chỉ đổi order + sửa dropdown, không update data |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lịch sử access bot (アクセス履歴) | F2, F4, F5 | `<Dev chưa ghi>` |
| T2 | Export CSV lịch sử access | F3 | `<Dev chưa ghi>` |
| T3 | Detail bot trong Supper Admin | F1 | `<Dev chưa ghi>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- ⚠️ Lưu ý cho Leader: Dev KHÔNG ghi cột Direct/Indirect ở 4.1 và mức risk ở 4.3 → cần confirm với Dev. Mục 3 (caller đã check) để trống — hỏi Dev đã rà callers của getAccessHistories/exportCsvAccessHistory chưa. -->
