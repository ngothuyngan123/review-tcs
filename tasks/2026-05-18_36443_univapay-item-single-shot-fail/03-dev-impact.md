# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #36443 (journal #118514 — Thanh Phương 2026-05-18) bằng `/new-task`. Tester verify rồi tick checkbox bên dưới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Phương (từ journal #118514) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | 2026-05-18 |
| Auto-filled | 2026-05-18 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Paste nguyên văn từ Redmine. -->

- Khi bấm nút mua, gặp lỗi từ univapay nhưng chưa hiển thị message lỗi cho user.

## 2. Cách fix

<!-- Paste nguyên văn từ Redmine. -->

- Set error message return về cho frontend để hiển thị.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Redmine không có nội dung chi tiết cho mục 3. Dev chỉ ghi heading, không list caller. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu — Dev chưa list caller cụ thể>` | | |

> ⚠️ Mục 3 trống — Dev chỉ ghi heading "Đã check và sửa các function sử dụng đến function/data vừa sửa" nhưng không list caller. Leader cần hỏi lại Dev có function nào khác gọi `paymentCreditCardItemV2Univapay` cần update không, hoặc đây là điểm fix isolated chỉ trong 1 function controller.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `paymentCreditCardItemV2Univapay` | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Direct | Function fix chính — set error message return về frontend khi Univapay trả lỗi |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | _(k có)_ | — | Dev confirm không có data nào bị chạm |

> Dev ghi nguyên văn: "k có" (không có data nào bị update khi fix bug).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Bấm nút mua item, **case có webhook** (item single-shot via Univapay) | F1 | High — flow chính của fix, cần verify cả happy path + lỗi từ Univapay được surface |

> Dev ghi nguyên văn ở mục 4.3: "bấm nút mua item, case có webhook".

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **⚠️ Hiện tại mục 3 TRỐNG, cần Dev confirm**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — **⚠️ Cần check thêm: case bill chu kỳ (subscription) cũng dùng cùng controller không? Case không webhook? Double-click button?**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
