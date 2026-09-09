# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kieu Son Tung` (assigned_to) — đánh giá submit bởi `Hạnh Nguyễn` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `fix/Task_Detail_Friend_Sort_Item_38206` |
| Ngày submit đánh giá | `2026-06-26` |
| Auto-filled | `2026-06-26 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- detail friend đang sort theo id

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- sort theo position giống màn list

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

> Redmine: heading mục 3 để trống (Dev không liệt kê riêng) — xem mục 4.1.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Dev không liệt kê riêng — xem 4.1>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `fetchCurrentTags()` | `public/_assets/modules/my_page/mixins/tag-mixin.js` | Direct | |
| F2 | `ajaxTagEditModal()` | `app/Http/Controllers/Basic/FriendlistController.php` | Direct | |
| F3 | `getFoldersByBot()` | `app/Repositories/Eloquents/LandingRepository.php` | Indirect | |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Dev ghi rõ "Không có" (chỉ đổi logic sort khi đọc, không update data) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | modal edit tag (màn detail friend) | F1, F2 | `<Dev chưa ghi>` |
| T2 | filter tag (màn detail friend) | F2 | `<Dev chưa ghi>` |
| T3 | filter qr (màn detail friend) | F3 | `<Dev chưa ghi>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

> ⚠️ **Điểm cần verify với Dev (discrepancy giữa 2 input):** Đánh giá ảnh hưởng trong **Redmine journal** (file này) chỉ liệt kê phạm vi **tag + qr** với 3 function (F1–F3). Nhưng bản đánh giá nhúng trong **TC Sheet (file 04, row 755)** lại rộng hơn — thêm **richmenu** (sort ASC ngược màn list DESC) và function thứ 4 `getRichmenuFilterFolders()` (`app/Repositories/Eloquents/FriendDetailRepository.php`), cùng "filter richmenu". TC Sheet (row 784–796) thực tế đã cover cả richmenu. → Cần xác nhận với Dev phạm vi fix thực sự có chạm **richmenu** không; nếu có thì bổ sung F4 + T4 (richmenu) vào mục 4.1/4.3 trước khi `/review-tc`.
