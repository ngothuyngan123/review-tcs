# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Ngọc Ánh` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-09` |
| Auto-filled | `2026-06-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- Trang 契約情報・領収書 (bill/index) dùng hàm `getOverDueDay(contract)` để hiển thị ngày 強制解約 trong banner cảnh báo 決済エラー và trong cột 延滞中 của bảng danh sách hợp đồng
- Hàm này luôn tính `expired_date_contract + 7 ngày` bất kể phương thức thanh toán, kể cả khi user thanh toán bằng 銀行振込 (`payment_method == 2`)
- Trang 契約詳細 (bill/detail) dùng hàm `overdueDate()` với logic phân biệt: nếu 銀行振込 thì lấy `expired_date_bank_transfer` trực tiếp (không cộng 7 ngày)
- `expired_date_bank_transfer` là ngày hạn chót thực tế do phía bank/admin set, khác với `expired_date_contract + 7 ngày`, nên hai trang hiển thị ngày không khớp nhau

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Sửa hàm `getOverDueDay(contract)` trong `public/_assets/modules/bill/js/index.js` để phân biệt theo `payment_method`
- Nếu `payment_method == 2` (銀行振込): trả về `expired_date_bank_transfer` (định dạng YYYY/MM/DD), đồng nhất với logic của trang 契約詳細
- Nếu `payment_method == 1` (カード決済): giữ nguyên logic cũ là `expired_date_contract + 7 ngày`

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `getOverDueDay(contract)` — `public/_assets/modules/bill/js/index.js` | **Đã sửa**: thêm nhánh phân biệt `payment_method == 2` → trả về `expired_date_bank_transfer` | Root cause fix |
| 2 | `bill/index.blade.php:256` — gọi `getOverDueDay(contract_overdue)` trong banner cảnh báo 決済エラー (overdue_data loop) | Được fix gián tiếp qua hàm trên | Banner dùng chung `getOverDueDay` |
| 3 | `bill/index.blade.php:395` — gọi `getOverDueDay(contract)` trong cột danh sách hợp đồng khi `isContractOverDue(contract)` | Được fix gián tiếp qua hàm trên | Cột list dùng chung `getOverDueDay` |
| 4 | `overdueDate()` — `public/_assets/modules/bill/js/detail.js` (trang 契約詳細) | **Không sửa** | Logic đã đúng (đã phân biệt `payment_method`) |
| 5 | `overdueDate()` — `public/_assets/modules/bill/js/detail_bill_fail.js` (trang max-friend bill fail) | **Không sửa** | Logic riêng dùng `cardBillMaxFriend`, không liên quan |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getOverDueDay(contract)` | `public/_assets/modules/bill/js/index.js` | Direct | Thêm nhánh phân biệt `payment_method == 2` → `expired_date_bank_transfer`; `payment_method == 1` giữ nguyên `expired_date_contract + 7 ngày` |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | (không có) | — | Dev xác nhận: chỉ sửa logic hiển thị phía client, **không thay đổi DB hay API**. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Trang 契約情報・領収書 (bill/index) — banner cảnh báo 決済エラー ở đầu trang: ngày 強制解約 hiển thị đúng theo `expired_date_bank_transfer` cho user thanh toán 銀行振込 | F1 | Medium |
| T2 | Trang 契約情報・領収書 (bill/index) — cột danh sách hợp đồng, message 延滞中 inline (tương tự banner) | F1 | Medium |

> Dev xác nhận **KHÔNG ảnh hưởng** trang 契約詳細 (bill/detail) và trang detail-bill-fail (max-friend bill fail).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
