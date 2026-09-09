# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine bởi `/new-task` — parse Section "Đánh giá ảnh hưởng" (journal #126891). Tester verify rồi tick checkbox.
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Tuấn Anh Trần |
| Commit / Pull Request | `<chưa có — Redmine không có link PR>` |
| Branch | `fix/Task_Redirect_Bill_Success_38957` |
| Ngày submit đánh giá | 2026-07-22 |
| Auto-filled | 2026-07-29 by /new-task |

> **Nguyên văn đánh giá từ Redmine (journal #126891, Tuấn Anh Trần — 2026-07-22):**
> ```
> 1. Nguyên nhân
> • khi mua thành công đang next sang step success mà không redirect đến màn success
>
> 2. Cách fix
> • redirect đến màn success sau đó back lại step success
>
> 3. Đã check function/data
> • resources/views/basic/payment_bot_success.blade.php
> • created(), univapayTokenHandler() (file: public/js/admin/bill_tool/index.js)
>
> 4. Đánh giá ảnh hưởng
> • mua slot mới(standard, pro, gói năm, gói tháng), upgrade pro
>
> 5. Recover data
> ✔ Không cần
>
> branch: fix/Task_Redirect_Bill_Success_38957
> ```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi mua thành công đang **next thẳng sang step success mà không redirect đến màn success** (router bill success).

## 2. Cách fix

**Redirect đến màn success trước, sau đó back lại step success.**

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê ở mục "3. Đã check function/data". Đây là các file/function bị chạm khi fix. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `resources/views/basic/payment_bot_success.blade.php` | `<Dev không ghi chi tiết thay đổi>` | View màn bill success — nơi render sau khi thanh toán |
| 2 | `created()` — `public/js/admin/bill_tool/index.js` | `<Dev không ghi chi tiết>` | Xử lý sau khi tạo bill thành công (điều hướng step success) |
| 3 | `univapayTokenHandler()` — `public/js/admin/bill_tool/index.js` | `<Dev không ghi chi tiết>` | Handler token thanh toán Univapay |

> ⚠️ **Input cần verify:** Dev liệt kê function **đã sửa** nhưng KHÔNG liệt kê rõ **caller khác** của `created()` / `univapayTokenHandler()` (các luồng bill/thanh toán khác cùng dùng step success). Leader nên xác nhận mục 3 đã cover đủ caller trước khi giao TC (rủi ro regression sibling flow).

---

## 4. Đánh giá ảnh hưởng

> Dev gộp toàn bộ đánh giá vào **1 dòng** ("mua slot mới (standard, pro, gói năm, gói tháng), upgrade pro") — không tách theo function / data / feature. Các mục 4.1–4.3 dưới đây được map lại từ mục 3 + mục 4 gốc, có flag rõ chỗ suy luận.

### 4.1. List function bị ảnh hưởng

<!-- Suy từ mục 3 (Dev không tự liệt kê riêng 4.1). -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `created()` | `public/js/admin/bill_tool/index.js` | Direct | Thêm bước redirect sang router success trước khi vào step success |
| F2 | `univapayTokenHandler()` | `public/js/admin/bill_tool/index.js` | Direct | Handler token Univapay — cùng luồng thanh toán thành công |
| F3 | View `payment_bot_success.blade.php` | `resources/views/basic/` | Direct | Màn bill success được render/redirect |

### 4.2. List data bị update khi fix bug

<!-- Dev ghi mục 5 "Recover data: ✔ Không cần" ⇒ không có thay đổi data. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Không có>` | — | Dev ghi **"Recover data: ✔ Không cần"** (mục 5). Fix thuần luồng redirect/điều hướng front-end, không đụng DB. Tester verify lại nếu redirect có kèm ghi bill/slot. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Từ mục 4 gốc "mua slot mới (standard, pro, gói năm, gói tháng), upgrade pro" + 4 router *_success ở description. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Mua slot mới — gói **standard** (tháng: `/monthly/standard_success`, năm: `/yearly/standard_success`) | F1, F3 | Medium |
| T2 | Mua slot mới — gói **pro** (tháng: `/monthly/pro_success`, năm: `/yearly/pro_success`) | F1, F3 | Medium |
| T3 | **Upgrade lên pro** | F1, F2, F3 | Medium |
| T4 | Luồng thanh toán **Univapay** (token handler) sau mua thành công | F2 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (⚠️ Dev CHƯA liệt kê caller khác của `created()`/`univapayTokenHandler()` — hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: có thực sự không ghi bill/slot khi redirect không?)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** (redirect fail / back 2 lần / refresh giữa chừng / thanh toán fail)
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
