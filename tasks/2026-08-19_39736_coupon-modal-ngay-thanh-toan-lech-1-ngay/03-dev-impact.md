# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #39736 — journal **#129280** (`AI LME Fix bug`, 2026-08-19T04:13:13Z), báo cáo **AI AUTO-FIXBUG**.
> ⚠️ Đây là đánh giá do **AI sinh tự động**, KHÔNG phải Dev người viết. Leader nên verify kỹ mục 3 + 4.1 (caller) trước khi giao TC.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | commit `8ef593df85` (không có link Github/Gitlab trong Redmine). Phiên AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=1f396d2b-6482-4710-af6b-444b09fb0442 · Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=39736 |
| Branch | `ai_small_39736` (repo `sns-line`, nhánh gốc `release_step_20260805`, 3 file) — đã push |
| Ngày submit đánh giá | `2026-08-19` |
| Auto-filled | `2026-08-19 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "■ 1. NGUYÊN NHÂN" của journal #129280 -->

Modal nhập mã coupon hiển thị câu "ngày thanh toán tiếp theo được gia hạn tới ..." nhưng giá trị máy chủ trả về lại là NGÀY HẾT HẠN hợp đồng mới. Hàm tính gia hạn luôn trả về cuối ngày LIỀN TRƯỚC mốc thanh toán kế, còn dòng ngày thanh toán tiếp theo trên chính màn chi tiết hợp đồng lại lấy ngày hết hạn + 1 ngày. Vì vậy modal coupon luôn hiện sớm hơn đúng 1 ngày (ví dụ của khách: hiện 2026/09/26 trong khi ngày thanh toán tiếp theo phải là 2026/09/27).

## 2. Cách fix

<!-- Nguyên văn mục "■ 2. CÁCH FIX" của journal #129280 -->

Bổ sung trường ngày thanh toán tiếp theo (= ngày hết hạn hợp đồng mới + 1 ngày) vào kết quả trả về của hai API kiểm tra và áp dụng mã coupon, đồng thời cho hai modal xác nhận/thành công hiển thị trường mới này thay vì ngày hết hạn (đổi tên biến hiển thị thành `couponNextPaymentDate` cho đúng nghĩa). Không đổi logic tính ngày gia hạn cũng như dữ liệu ghi vào hợp đồng. Quét ngang: màn Cài đặt điểm cũng hiển thị nhãn ngày thanh toán tiếp theo bằng ngày hết hạn thô (cùng kiểu lệch 1 ngày) nhưng nằm ngoài phạm vi ticket nên chỉ ghi nhận.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN", convert sang bảng template. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `UserController::checkCouponCode` — `app/Http/Controllers/Admin/UserController.php` | Có — bổ sung trường ngày thanh toán tiếp theo vào response | API bước "kiểm tra mã coupon", nguồn dữ liệu cho modal xác nhận |
| 2 | `UserController::applyCouponCode` — `app/Http/Controllers/Admin/UserController.php` | Có — bổ sung trường ngày thanh toán tiếp theo vào response | API bước "áp dụng mã coupon", nguồn dữ liệu cho modal thành công |
| 3 | `BillingService::nextExpiredDate` — `app/Services/BillingService.php` | **Không sửa** (chỉ đọc) | Hàm tính gia hạn — kết thúc bằng `$nextBillDate->subDay()->endOfDay()` ⇒ trả về cuối ngày liền TRƯỚC mốc thanh toán kế |
| 4 | `checkCouponCode` / `confirmCouponCode` / `openModalInputCoupon` — `public/_assets/modules/bill/js/detail.js` | Có — hiển thị trường mới `couponNextPaymentDate` thay vì ngày hết hạn | JS điều khiển 2 modal coupon |
| 5 | `expiredDateContract` — `public/_assets/modules/bill/js/detail.js` | **Không sửa** (mốc đối chiếu) | `moment(expired_date_contract).add(1, day)` — công thức dòng "Ngày thanh toán tiếp theo" trên cùng màn |
| 6 | Modal coupon bước xác nhận + thành công — `resources/views/basic/bill/detail.blade.php` | Có — đổi biến hiển thị | View render 2 modal |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- ⚠️ Mục "■ 4.1" của báo cáo AI chỉ liệt kê FILE thay đổi (3 file), KHÔNG liệt kê function theo format F1/F2. Bảng dưới suy từ mục 3 + 4.1; Leader verify lại. -->

**Nguyên văn 4.1 — File thay đổi:**
- `app/Http/Controllers/Admin/UserController.php`
- `public/_assets/modules/bill/js/detail.js`
- `resources/views/basic/bill/detail.blade.php`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | API `checkCouponCode` (bước kiểm tra mã) | `app/Http/Controllers/Admin/UserController.php` | Direct | Thêm field ngày thanh toán tiếp theo vào response; field cũ `new_expired_date` **vẫn giữ**, không xoá |
| F2 | API `applyCouponCode` (bước áp dụng mã) | `app/Http/Controllers/Admin/UserController.php` | Direct | Như F1 |
| F3 | JS `checkCouponCode` / `confirmCouponCode` / `openModalInputCoupon` | `public/_assets/modules/bill/js/detail.js` | Direct | Đổi sang render biến `couponNextPaymentDate` |
| F4 | Modal coupon — bước **xác nhận** & bước **thành công** | `resources/views/basic/bill/detail.blade.php` | Direct | 2 modal hiển thị ngày |
| F5 | `BillingService::nextExpiredDate` | `app/Services/BillingService.php` | Indirect — **không sửa code** | Logic tính gia hạn giữ nguyên ⇒ job thanh toán tự động không bị chạm |
| F6 | JS `expiredDateContract` (dòng "Ngày thanh toán tiếp theo" trên màn detail) | `public/_assets/modules/bill/js/detail.js` | Indirect — **không sửa code** | Mốc đối chiếu để verify modal khớp với dòng trên màn |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục "■ 4.2 Data ảnh hưởng" -->

> **Dev khẳng định: Không có** — không thêm/sửa câu lệnh ghi DB nào; `bot_contracts.expired_date_contract` và `bots.expired_date` vẫn được cập nhật y như trước.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_contracts.expired_date_contract` | UPDATE — **không đổi so với trước fix** | Giá trị gia hạn ghi vào hợp đồng KHÔNG đổi; chỉ ngày *hiển thị* trên modal đổi |
| D2 | `bots.expired_date` | UPDATE — **không đổi so với trước fix** | Như D1 |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục "■ 4.3 Tính năng liên quan". Cột "Nguy cơ regression" Dev KHÔNG ghi → để `<Dev không ghi>`, Leader tự đánh giá. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Contract Plan & Payment (FA-031)** — màn chi tiết hợp đồng | F1, F2, F3, F4 | `<Dev không ghi>` — Dev mô tả: "chỉ đổi ngày hiển thị trong modal nhập mã coupon, các mốc ngày khác giữ nguyên" |
| T2 | **Coupon Code Issue (FS-015)** — luồng áp dụng mã coupon phía người dùng | F1, F2, D1, D2 | `<Dev không ghi>` — Dev mô tả: "giá trị gia hạn ghi vào hợp đồng không đổi, chỉ sửa ngày xem trước/xác nhận" |

---

## Phụ lục — các mục còn lại của báo cáo AI (nguyên văn)

### ■ 5. RECOVER DATA
✔ Không cần recover data

### ■ 6. VERIFY
- **Mức:** lint
- **Lệnh:** `php -l app/Http/Controllers/Admin/UserController.php`: No syntax errors; `php -l resources/views/basic/bill/detail.blade.php`: No syntax errors; `node --check public/_assets/modules/bill/js/detail.js`: OK; Mô phỏng lại công thức `nextExpiredDate` bằng Carbon: hết hạn cũ 2026-08-26 + neo ngày 27 → hết hạn mới 2026-09-26 23:59:59 → hiển thị mới **2026/09/27** (cũ 2026/09/26) — khớp đúng con số khách báo; **Không viết unit test**: thay đổi nằm ở controller + view, không thuộc `app/Services|app/Helpers` (logic tính ngày không bị sửa).
- **Bằng chứng:** `BillingService::nextExpiredDate` kết thúc bằng `$nextBillDate->subDay()->endOfDay()` ⇒ kết quả là cuối ngày liền TRƯỚC mốc thanh toán kế; `detail.js expiredDateContract()` = `moment(expired_date_contract).add(1, day)` — dòng Ngày thanh toán tiếp theo trên cùng màn dùng công thức này; Spec **FS-015 BR-09** (`share/spec/spec-features/system-admin/coupon-management/feature-spec.md:175`) xác nhận: kết quả = cuối ngày liền trước mốc thanh toán kế.

### ■ TỰ REVIEW (AI)
Sửa đúng nguyên nhân gốc: nhãn hiển thị là ngày thanh toán tiếp theo nhưng giá trị lấy là ngày hết hạn hợp đồng. Cách sửa thêm trường riêng có ngữ nghĩa rõ ràng ở phía máy chủ thay vì cộng ngày rải rác ở giao diện, tránh lặp lại lỗi cũ **#39383** (tái dùng hàm có sẵn độ lệch). Không đụng logic tính gia hạn nên không ảnh hưởng job thanh toán tự động.

**Rủi ro / lưu ý khi test (Dev tự nêu):**
- Trình duyệt giữ bản JS cũ sẽ không có biến mới — thực tế script nạp kèm `?v=config(sns-line.version)` nên phát hành mới sẽ tự đổi đường dẫn, rủi ro thấp.
- Trường cũ `new_expired_date` vẫn được trả về (không xoá) để không phá bên gọi khác nếu có; hiện chỉ modal này dùng.
- **Màn Cài đặt điểm còn cùng kiểu lệch 1 ngày — cần ticket riêng**, đã ghi ở phần quét ngang.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ báo cáo do AI sinh, danh sách caller có thể chưa đủ
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ AI chỉ liệt kê file, bảng F1–F6 là do `/new-task` suy từ mục 3
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — ⚠️ Dev KHÔNG chấm mức nguy cơ regression
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
