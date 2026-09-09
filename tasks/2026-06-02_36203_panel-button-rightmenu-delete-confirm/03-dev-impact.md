# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kim Cúc (theo journal đánh giá 2026-05-23); assigned_to: AI CSS` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-05-23` |
| Auto-filled | `2026-06-02 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

`<Input thiếu — Dev để trống mục "1. Nguyên nhân" trong journal đánh giá>`

Suy luận từ mục 2 (cách fix) + mô tả KH:
- ① Panel right-side menu (icon 3 chấm để sort/xóa) bị che do CSS — khi panel ở sát mép phải, menu render ra ngoài vùng nhìn nên phải dịch panel mới thấy.
- ② Hành động delete panel chỉ 1 click là xóa ngay, **chưa có** modal confirm (đây là cải tiến UX, không phải lỗi logic).

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Sửa CSS để chỉnh **panel right-side menu** (cho hiển thị được mà không cần dịch panel).
- Thêm **modal xóa**, sửa JS thêm hàm **confirm xóa** (anh Tư bảo lấy modal theo component).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

`<Input thiếu — Dev để trống mục 3 trong journal. Cần hỏi Dev: hàm confirm xóa mới thêm có dùng chung component modal nào? Component modal đó còn được nơi nào khác gọi (regression)?>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. (Dev list theo file, không theo function.) -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | CSS template create (panel right-side menu) | `public/css/template_v2/create.css` | Direct | Fix ① — hiển thị menu panel |
| F2 | JS button (panel + confirm xóa) | `public/js/template_v2/messages/button.js` | Direct | Fix ② — thêm hàm confirm xóa |
| F3 | Blade component button | `resources/views/basic/template_v2/components/button.blade.php` | Direct | Markup modal xóa / panel |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<không có>` | — | Dev ghi rõ "k có" — fix chỉ chạm CSS/JS/Blade, không đụng data layer |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn hình add/edit template button (Panel/Button) | F1, F2, F3 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

> ⚠️ **Lưu ý cho Leader:** Mục 1 (nguyên nhân) và mục 3 (caller đã check) bị **bỏ trống** trong journal đánh giá. Đặc biệt mục 3: fix ② thêm modal/hàm confirm xóa dùng "modal theo component" → cần xác nhận component modal dùng chung không gây regression cho các nơi khác gọi cùng component.
