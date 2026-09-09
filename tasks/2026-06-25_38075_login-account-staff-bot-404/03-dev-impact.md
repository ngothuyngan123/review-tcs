# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine bởi `/new-task` (parse Section "Đánh giá ảnh hưởng dev" trong journal). Tester verify rồi tick checkbox.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Tuấn Anh Trần` (assigned_to) |
| Commit / Pull Request | `<chưa có — Redmine chưa cung cấp link PR>` |
| Branch | `fix/Task_Basic_Access_Staff` |
| Ngày submit đánh giá | `2026-06-25` |
| Auto-filled | `2026-06-25 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- User đang select vào bot mà mình không còn là staff.

## 2. Cách fix

- Redirect về màn list bot.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Redmine: mục 3 có heading nhưng Dev KHÔNG liệt kê nội dung. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu — Dev chưa liệt kê caller đã check>` | | |

> ⚠️ Mục 3 trong Redmine để trống (chỉ có heading). Leader nên hỏi Dev: đã check những caller nào của `handle()` / `getRouterBotInvite()` chưa, để chắc không sót regression.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `handle()` | `app/Http/Middleware/BasicAccess.php` | Direct | Middleware check login/quyền access bot |
| F2 | `getRouterBotInvite()` | `app/Helpers/functions.php` | Direct | Helper resolve router/redirect khi select bot |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có | — | Dev xác nhận fix không update data (chỉ thay đổi luồng redirect) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Login account staff | F1, F2 | `<Dev không ghi mức risk — Leader đánh giá>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **lưu ý**: "list bot" (file 03) vs `/admin/pre-select-bot` (TCs Sheet), xác nhận target redirect
- [ ] Mục 3 đã check đủ caller — **HIỆN TRỐNG**, hỏi lại Dev
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng login staff
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
