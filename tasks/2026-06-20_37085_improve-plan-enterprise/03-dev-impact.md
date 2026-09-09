# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Phương` (người submit đánh giá) — assigned_to: Tuấn Anh Trần |
| Commit / Pull Request | `<chưa có>` |
| Branch | `feature/Task_Owner_Enterprise_37085` |
| Ngày submit đánh giá | `2026-06-16` |
| Auto-filled | `2026-06-20 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- không cần phải là owner vẫn thao tác được plan enterprise

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- sửa lại theo spec mới, phải là owner mới được thao tác với plan enterprise

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

> Dev gộp danh sách function/file đã check & sửa vào mục 4.1 bên dưới (giữ nguyên văn từ Redmine).

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Xem mục 4.1 | — | — |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

> Direct/Indirect: Dev không phân loại trong Redmine — list dưới là nguyên văn các function/file Dev đã check & sửa.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `isNotOwnerContractEnterprise()` | app/Helpers/functions.php | Direct | Hàm check quyền owner (backend) |
| F2 | `botDelete()` | app/Http/Controllers/Admin/BotController.php | Direct | Xóa bot khỏi slot |
| F3 | `index()` | app/Http/Controllers/Admin/BotEnterPriseController.php | Direct | Màn list bot enterprise |
| F4 | `addBotToSlot()` | app/Http/Controllers/Admin/UserController.php | Direct | Add bot vào slot |
| F5 | `detailContract()` | app/Http/Controllers/Basic/UserController.php | Direct | Màn detail hợp đồng |
| F6 | `confirmCancelView()` | app/Http/Controllers/V2/Bill/ListPageController.php | Direct | View confirm cancel |
| F7 | (CSS) | public/_assets/modules/bill/css/detail.css | Direct | Style màn detail hợp đồng |
| F8 | `isNotOwnerContractEnterprise()` (JS) | public/_assets/modules/bill/js/detail.js | Direct | Check quyền owner (frontend) |
| F9 | (View blade) | resources/views/basic/bill/detail.blade.php | Direct | Template màn detail hợp đồng |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Dev xác nhận: "Không có" data bị update khi fix |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

> Nguy cơ regression: Dev không phân loại High/Medium/Low trong Redmine — giữ nguyên văn.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | access màn list bot enterprise | F3 | `<chưa rõ — Dev chưa ghi>` |
| T2 | detail hợp đồng | F5, F8, F9 | `<chưa rõ — Dev chưa ghi>` |
| T3 | xóa bot | F2 | `<chưa rõ — Dev chưa ghi>` |
| T4 | add bot to slot | F4 | `<chưa rõ — Dev chưa ghi>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
