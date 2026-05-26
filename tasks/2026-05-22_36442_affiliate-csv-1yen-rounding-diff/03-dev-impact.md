# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ — Kim Cúc submit qua Redmine journal, verify Dev thực sự là ai>` |
| Commit / Pull Request | `<chưa có — tester confirm>` |
| Branch | `<chưa rõ — tester fill>` |
| Ngày submit đánh giá | 2026-05-21 |
| Auto-filled | 2026-05-22 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Trên màn hình admin số tiền `報酬額` (tiền hoa hồng) được **làm tròn xuống** (floor), còn khi download csv thì số tiền đang được **làm tròn với số gần nhất** (round-to-nearest).

→ Có sự lệch **1円** giữa GUI admin và CSV xuất ra ở những user có phần lẻ amount (vd ¥15,557.5, ¥18,627.6, ¥12,382.6, ¥3,810.8).

## 2. Cách fix

Ở **frontend màn hình admin** và **download csv**: làm tròn với **số gần nhất** (round-to-nearest, thay vì floor ở GUI).

→ Sau fix: cả 2 đầu (GUI + CSV) cùng dùng cùng 1 quy tắc làm tròn → khớp số.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> ⚠️ Dev chỉ ghi tiêu đề mục 3, **không liệt kê** function caller cụ thể đã check. Tester nên verify với Dev xem có function nào khác (vd job tổng hợp doanh số, page export khác) cũng dùng cùng logic floor → có thể sót.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<chưa rõ — Dev fill / hỏi Dev>` | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev liệt kê 2 function (không gán nhãn Direct/Indirect). Cả 2 đều là điểm sửa Direct (1 frontend, 1 backend export). Tôi (AI) suy luận: cả 2 = Direct vì đều chứa logic làm tròn được sửa.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | (FE) Hàm render amount cột 報酬額 | `public/_assets/modules/supper_admin/js/affiliater.js` | Direct | Frontend JS render amount trên màn 代理店報酬 — đổi từ floor sang round-to-nearest |
| F2 | `exportCsvV2` | `app/Http/Controllers/Admin/AffiliateInfoController.php` | Direct | Backend controller xuất CSV 振込用CSV — đổi quy tắc làm tròn cho khớp FE |

### 4.2. List data bị update khi fix bug

> Dev confirm: "k có" — fix chỉ thay đổi logic làm tròn trên FE render + BE export, **không chạm DB / migration / cache**. Source-of-truth số amount (bảng `payment_detail_aff`, field `amount * rate / 100 - sub_amount`) giữ nguyên decimal.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | (không có) | — | Dev confirm không có data update. Source data `payment_detail_aff.amount` raw giữ nguyên — chỉ logic làm tròn ở display/export đổi. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> ⚠️ Dev ghi "màn hình admin 商品決済" và "export csv 振込用CSV tại màn 商品決済" — nhưng bug context là "代理店報酬" (affiliate reward). **Verify với Dev**: 商品決済 và 代理店報酬 có phải cùng 1 màn không, hay Dev gõ nhầm. Tôi (AI) giữ nguyên text Dev viết và thêm 2 row dự đoán.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn hình admin 商品決済 (Dev viết — verify có phải = 代理店報酬 không) | F1 | Medium |
| T2 | Export CSV 振込用CSV tại màn 商品決済 (Dev viết — verify scope) | F2 | High |
| T3 | (Dự đoán theo bug context) Màn admin 代理店報酬 — hiển thị tổng amount theo kỳ | F1 | High |
| T4 | (Dự đoán theo bug context) Tổng số tiền 振込金額 cuối trang admin 代理店報酬 | F1 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **verify cụ thể quy tắc làm tròn (Math.round? toFixed? PHP round() mode?) để TC boundary cover được halfway (vd .5)**
- [ ] Mục 3 đã check đủ caller — **Dev chưa list cụ thể, cần hỏi lại**
- [ ] Mục 4.1 không thiếu function — **verify có job batch nào tính tổng hoa hồng theo kỳ cũng dùng floor không** (vd job sinh bảng thống kê, job thông báo amount cho đại lý)
- [ ] Mục 4.2 không thiếu data — Dev confirm "k có"; verify có log/audit trail nào ghi lại amount sau làm tròn không
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** — **verify scope 商品決済 vs 代理店報酬 với Dev**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

<!-- Source: auto-filled từ Redmine #36442 journal #118957 (by Kim Cúc, 2026-05-21T08:26:41Z) — Section "Dev đánh giá ảnh hưởng". -->
