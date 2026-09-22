# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Nguồn: **AI Auto-fixbug LME** (Journal #125998 / #125999 Redmine #38783 — 2 journal trùng nội dung), KHÔNG phải Dev người viết.
> Mục 4.1 chỉ liệt kê **file thay đổi**, không có function-level impact; mục 3 chỉ 1 dòng plain-text, không có bảng caller. Mục 4.2 khai "không có data ảnh hưởng". Leader cần đối chiếu **diff thật** (branch `ai_small_38783`, commit `17792c55ff`, 1 file) trước khi chốt coverage.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI Auto-fixbug LME (assignee ticket: Kim Cúc) |
| Commit / Pull Request | commit `17792c55ff` (repo `sns-line`) — `<chưa có link PR>` |
| Branch | `ai_small_38783` (nhánh gốc `release_step_20260623`, 1 file) — đã push origin |
| Ngày submit đánh giá | 2026-07-14 |
| Auto-filled | `2026-09-17 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Trong hàm `ajaxCouponManagement` (màn quản lý phát hành mã coupon), điều kiện lọc theo khoảng ngày dùng nhầm toán tử `&` (bitwise AND) thay vì `&&` (logical AND). Vì `&` có độ ưu tiên cao hơn `&&` nên PHP hiểu là `$type_filter==0 && ($start_date & $end_date)`; hai chuỗi ngày bị ép về số nguyên rồi AND theo bit → kết quả sai, khiến bộ lọc khoảng ngày gần như không kích hoạt đúng. Lặp lại cho cả nhánh `$type_filter==1`. Ngoài ra còn sót dòng comment dead code `// DB::rollback();` trong khối `catch`.

## 2. Cách fix

Đổi toán tử `&` (bitwise) thành `&&` (logical) ở **2 điều kiện `.when()`** lọc khoảng ngày trong `ajaxCouponManagement`:
- nhánh `type_filter == 0` — lọc theo `created_at` (≈ dòng 9490, tương ứng radio 「発行日」)
- nhánh `type_filter == 1` — lọc theo `datetime_use` (≈ dòng 9492, tương ứng radio 「使用日」)

để điều kiện **chỉ kích hoạt khi cả `start_date` và `end_date` đều có giá trị**. Đồng thời xoá dòng comment dead code `// DB::rollback();` trong khối `catch` của hàm này.

**Yokoten:** quét toàn app không thấy chỗ nào khác dùng cùng pattern `&` sai.

**Verify của AI:** mức `lint` — `php -l app/Http/Controllers/Admin/UserController.php: No syntax errors detected`. Bằng chứng: precedence PHP `&` cao hơn `&&` nên `$a && $b & $c` == `$a && ($b & $c)`; fix đổi thành `$a && $b && $c` như ý định ban đầu.

**Recover data:** ✔ Không cần recover data.

**Tự review (AI):** "Fix tối thiểu đúng root cause: đổi `&` → `&&` ở 2 điều kiện lọc khoảng ngày + xoá dead code. Không ảnh hưởng logic khác trong hàm." · Rủi ro khi test AI tự đánh giá: *"Không có rủi ro đáng kể — chỉ sửa toán tử điều kiện, hành vi lọc trở về đúng thiết kế"*.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- AI chỉ ghi 1 dòng plain-text (tên hàm vừa sửa), KHÔNG liệt kê caller. Convert sang bảng template, cột "Thay đổi" điền theo mục 2. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ajaxCouponManagement` — `app/Http/Controllers/Admin/UserController.php` (≈ dòng 9468–9492) | Đổi `&` → `&&` ở 2 điều kiện `.when()` lọc khoảng ngày; xoá `// DB::rollback();` trong `catch` | Chính là hàm chứa root cause |

> ⚠️ **Input thiếu:** AI **không liệt kê caller** của `ajaxCouponManagement` (ai gọi endpoint này: view blade nào, JS nào, có endpoint nào khác dùng chung query builder không) và **không nêu đã check các màn/nhánh khác dùng chung hàm** (`type_display = 0` tab 未使用者). Leader cần hỏi lại hoặc đọc diff/route để xác nhận.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- AI chỉ khai "File thay đổi", không khai function-level. Bảng dưới suy từ mục 2 + 3, đánh tag theo quy ước repo. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ajaxCouponManagement` — nhánh `type_filter == 0` (lọc `created_at` / 発行日) | `app/Http/Controllers/Admin/UserController.php` | Direct | Điều kiện `.when()` đổi `&` → `&&` |
| F2 | `ajaxCouponManagement` — nhánh `type_filter == 1` (lọc `datetime_use` / 使用日) | `app/Http/Controllers/Admin/UserController.php` | Direct | Điều kiện `.when()` đổi `&` → `&&` |
| F3 | Khối `catch` của `ajaxCouponManagement` | `app/Http/Controllers/Admin/UserController.php` | Direct | Xoá comment dead code `// DB::rollback();` — không đổi hành vi runtime, nhưng phải xác nhận `catch` vẫn trả response đúng |

> **Input thiếu:** AI **không khai** ảnh hưởng tới các nhánh còn lại cùng hàm (`type_display` = tab 未使用者 / 使用済み, sort, phân trang, export nếu có). Đây là **cùng 1 hàm** nên nằm trong vùng regression dù AI không kê.

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** | — | AI khai: *"Không có — chỉ sửa logic điều kiện query, không đổi schema/dữ liệu"*. Fix chỉ đổi **điều kiện đọc** (`whereDate` trên `coupon_management.created_at` / `.datetime_use`), không ghi DB. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Coupon Code Issue (FS-015)** — màn quản lý mã coupon `/admin/coupon-management`, tab 「使用済み」: bộ lọc khoảng ngày theo 発行日 (`created_at`) | F1 | Medium — hành vi lọc **thay đổi so với trước fix** (trước: điều kiện gần như không kích hoạt đúng; sau: lọc thật) |
| T2 | **Coupon Code Issue (FS-015)** — cùng màn, bộ lọc theo 使用日 (`datetime_use`) | F2 | Medium — như T1 |
| T3 | Các nhánh khác của cùng màn quản lý mã coupon (tab 未使用者, sắp xếp, phân trang, nhánh không lọc khi clear ngày) | F1, F2, F3 | Low — **AI không kê**, Leader bổ sung vì dùng chung endpoint `ajaxCouponManagement` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ **hiện đang thiếu**, AI không liệt kê caller
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ AI chỉ khai file, F1–F3 là do repo suy ra
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
