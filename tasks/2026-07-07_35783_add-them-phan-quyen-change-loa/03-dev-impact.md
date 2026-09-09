# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Phương (người viết đánh giá ảnh hưởng) — assigned_to Redmine: Do Van Tu TuDV |
| Commit / Pull Request | `<chưa có>` (custom field "Commit Date" trống) |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | 2026-07-06 |
| Auto-filled | 2026-07-07 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- Spec change bỏ phân quyền change bot chỉ owner mới change được.

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Xóa phân quyền trong database.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Dev không liệt kê chi tiết — chỉ ghi mục "3. Đã check function/data">` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Không sửa (theo Dev) | | | Dev khẳng định không sửa function |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Dev ghi "k có">` | | ⚠️ Mâu thuẫn với mục 2 (cách fix = "Xóa phân quyền trong database"). Cần confirm với Dev bảng/record bị xóa. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Owner change bot (đổi LOA) | BUG | `<Dev chưa ghi mức risk>` |
| T2 | Staff cũ đã được phân quyền trước đó change bot | BUG | `<Dev chưa ghi mức risk>` |
| T3 | Staff chưa được phân quyền change bot | BUG | `<Dev chưa ghi mức risk>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

<!-- Nội dung gốc Section "Đánh giá ảnh hưởng" (journal Thanh Phương 2026-07-06, Redmine #35783) — paste nguyên văn để đối chiếu:
** Report ảnh hưởng dv:
1. Nguyên nhân
- Spec change bỏ phân quyền change bot chỉ owner mới change được
2. Cách fix:
- Xóa phân quyền trong database
3. Đã check function/data
4. Đánh giá ảnh hưởng
  4.1 List function
        - Không sửa
    4.2 List những data bị update khi fix bug
        - k có
    4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
        - Owner change bot
        - Staff cũ đã được phân quyền trước đó change bot
        - Staff chưa được phân quyền change bot
-->
