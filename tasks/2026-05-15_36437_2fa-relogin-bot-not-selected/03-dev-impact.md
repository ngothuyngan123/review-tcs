# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Tuấn Anh Trần |
| Commit / Pull Request | `<chưa có — tester confirm>` |
| Branch | `<chưa rõ — tester fill>` |
| Ngày submit đánh giá | 2026-05-15 |
| Auto-filled | 2026-05-15 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Login xác thực 2 lớp nếu chọn bot trước đó rồi đang redirect về màn list bot.

## 2. Cách fix

- Sửa redirect về overview.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev không list cụ thể caller — verify với Dev có sót caller không trước khi viết TC. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<chưa rõ — Dev fill / hỏi Dev>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> **Lưu ý format**: Trong Redmine, Dev liệt kê 3 function dưới mục 4.1 nhưng không gán nhãn Direct/Indirect rõ. Tôi (AI) suy luận: `authCodeLogin` = Direct (chứa logic redirect bị sửa), 2 function còn lại cùng `AuthController.php` = Indirect (có thể bị ảnh hưởng do share state/session). Tester verify lại với Dev trước khi viết TC.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | authCodeLogin | app/Http/Controllers/AuthController.php | Direct | Function fix logic redirect 2FA |
| F2 | getPlanLOA | app/Http/Controllers/AuthController.php | Indirect | Cùng controller — Dev list ở mục 4.1, cần verify lại có thật bị ảnh hưởng |
| F3 | initDeliveryModalState | app/Http/Controllers/AuthController.php | Indirect | Cùng controller — Dev list ở mục 4.1, cần verify lại có thật bị ảnh hưởng |

### 4.2. List data bị update khi fix bug

> Dev confirm: "k có" (không có data nào bị update). Fix chỉ thay đổi flow redirect, không chạm DB / cache / session storage.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | (không có) | — | Dev confirm không có data update |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Login (đặc biệt: login với 2FA + đã chọn bot trước đó) | F1, F2, F3 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — **cần verify F2/F3 có thật bị ảnh hưởng không**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

<!-- Source: auto-filled từ Redmine #36437 journal note (by Ngọc Ánh, 2026-05-15T10:10:28Z) — Section "Đánh giá ảnh hưởng phía dev". -->
