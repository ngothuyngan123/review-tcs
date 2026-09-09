# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #36835 (journal "Dev đánh giá ảnh hưởng" của Kim Cúc, 2026-06-03) bởi `/new-task`.
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kieu Son Tung` (assigned_to; đánh giá được relay qua journal của Kim Cúc) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-03` |
| Auto-filled | `2026-06-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Dev. -->

- Trạng thái chờ chuyển khoản đang disable button.

## 2. Cách fix

<!-- Nguyên văn từ Dev. -->

- Enable button và thực hiện logic hủy chuyển khoản trước.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev chỉ ghi heading mục 3, KHÔNG liệt kê nội dung. -->

⚠️ **Input thiếu**: Dev không liệt kê chi tiết caller đã check ở mục 3. Hỏi lại Dev nếu nghi sót caller.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Dev chưa liệt kê>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn từ Dev, tag F1..F6. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `changeBillType()` | `app/Http/Controllers/Basic/UserController.php` | Direct | |
| F2 | `changePaymentMethod()` | `app/Http/Controllers/Basic/UserController.php` | Direct | |
| F3 | `changeTypePayment()` | `app/Http/Controllers/PointSettingController.php` | Direct | |
| F4 | `changePaymentMethod()` | `app/Http/Controllers/PointSettingController.php` | Direct | |
| F5 | `cancelTransfer()` | `app/BotContracts.php` | Direct | Logic hủy chuyển khoản |
| F6 | View màn detail hợp đồng | `resources/views/basic/bill/detail.blade.php` | Direct | Render enable/disable button |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn từ Dev. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Dev ghi "Không có" data bị update |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn từ Dev, tag T1..T2. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Thay đổi phương thức thanh toán (card ⇄ chuyển khoản) | F1, F2, F3, F4, F5, F6 | `<Dev chưa ghi risk>` |
| T2 | Thay đổi thời hạn thanh toán (năm → tháng, tháng → năm) | F1, F2, F3, F4, F6 | `<Dev chưa ghi risk>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (⚠️ Dev chưa liệt kê — hỏi lại Dev)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
