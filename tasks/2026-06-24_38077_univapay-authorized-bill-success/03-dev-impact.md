# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Phương` |
| Commit / Pull Request | `https://bitbucket.org/snstool/sns-line/pull-requests/10449/diff` |
| Branch | `bugs/fix_bug_step_20260624` |
| Ngày submit đánh giá | `2026-06-24` |
| Auto-filled | `2026-06-24 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- status charge của univapay trả về đang coi là chưa bill thành công.

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Status `authorized` đối xử (coi) đã bill thành công.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

<!-- Redmine: Dev không list riêng mục 3, các function liên quan trùng với 4.1. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `getBookingTimeout` — app/Services/CalendarManagement/CalendarCourseBookingService.php | `<chưa rõ — Dev chưa ghi chi tiết>` | Caller xử lý webhook timeout booking lesson |
| 2 | `getOrderTimeout` — app/Services/Sales/SalesService.php | `<chưa rõ — Dev chưa ghi chi tiết>` | Caller xử lý webhook timeout bill item |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getBookingTimeout` | app/Services/CalendarManagement/CalendarCourseBookingService.php | Direct / Indirect `<tester confirm>` | |
| F2 | `getOrderTimeout` | app/Services/Sales/SalesService.php | Direct / Indirect `<tester confirm>` | |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có | — | Dev xác nhận không có data bị update khi fix bug |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Job cover webhook timeout booking lesson | F1 | High / Medium / Low `<tester confirm>` |
| T2 | Job cover webhook timeout bill item chu kỳ + bill item 1 lần | F2 | High / Medium / Low `<tester confirm>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
