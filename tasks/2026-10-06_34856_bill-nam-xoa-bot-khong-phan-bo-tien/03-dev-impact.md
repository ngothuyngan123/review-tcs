# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug (journal #133415) — ticket assignee: Ngô Thúy Ngần` |
| Commit / Pull Request | `<chưa có PR> — commit acdbc422d7` |
| Branch | `ai_fixbug_34856` (gốc `release_step_20260805`, repo `sns-line`, đã push origin) |
| Ngày submit đánh giá | `2026-08-28` |
| Auto-filled | `2026-10-06 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (journal #133415) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Hợp đồng bill năm khi thu tiền sẽ sinh sẵn 12 (hoặc 24) dòng phân bổ theo tháng, mỗi tháng job chạy 06:00 bật cờ hiển thị cho dòng tới hạn. Job này bắt buộc phải tra ra bản ghi hợp đồng của bot mới bật cờ, trong khi luồng xóa bot (hủy kết nối) và các luồng đổi slot/nâng gói lại xóa cứng bản ghi hợp đồng khỏi database. Hợp đồng biến mất nên job bỏ qua, các tháng còn lại của năm đã thu tiền vĩnh viễn không được phân bổ vào doanh thu.

## 2. Cách fix

Sửa job phân bổ hằng ngày (`job:updateFlagDisplayBillYearAffByMonthly`): tách điều kiện bật phân bổ ra hàm riêng `canDisplayMonthlyBill` dùng chung cho cả 2 vòng lặp (lịch sử thanh toán và hoa hồng affiliate); khi bản ghi hợp đồng đã bị xóa khỏi database mà dòng phân bổ vẫn có mã hợp đồng thì **VẪN bật phân bổ** cho tháng tới hạn (tiền cả năm đã thu), có ghi log riêng để truy vết. Hợp đồng còn tồn tại giữ nguyên điều kiện cũ (không phải gói miễn phí và còn hạn); dòng phân bổ không gắn hợp đồng thì vẫn bỏ qua như cũ. Yokoten: đã rà các job/report khác dùng cùng dữ liệu phân bổ — report doanh thu và affiliate không join bảng hợp đồng nên chỉ cần sửa 1 chỗ này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `UpdateFlagDisplayBillYearAffByMonthly::handle` — `app/Console/Commands/UpdateFlagDisplayBillYearAffByMonthly.php` | Sửa logic bật cờ, gọi hàm điều kiện mới | File duy nhất được sửa — chokepoint quyết định việc phân bổ |
| 2 | `UpdateFlagDisplayBillYearAffByMonthly::canDisplayMonthlyBill` (hàm mới) — cùng file | Hàm mới, dùng chung cho cả 2 vòng lặp (payment_histories + payment_detail_aff) | Tách điều kiện để xử lý case hợp đồng đã bị xóa |
| 3 | `Kernel::schedule` — job chạy 06:00 hằng ngày — `app/Console/Kernel.php:181` | Không đổi | Điểm trigger job, đã check không đổi lịch chạy |
| 4 | `BotController::botDelete` — luồng xóa bot, xóa cứng `bot_contracts` — `app/Http/Controllers/Admin/BotController.php:1212` | Không đổi | Nguồn phát sinh bug (xóa cứng hợp đồng), đã check không cần sửa luồng này |
| 5 | `RefundController::rollbackPlan` — cũng xóa cứng hợp đồng khi hoàn tiền — `app/Http/Controllers/Admin/RefundController.php:408` | Không đổi | Luồng khác cũng xóa cứng hợp đồng, cùng được hưởng lợi từ fix |
| 6 | `SupperAdminController` — report hoa hồng affiliate lọc theo `flag_display` — `app/Http/Controllers/Admin/SupperAdminController.php:235` | Không đổi | Đã check không join `bot_contracts` → bật cờ là hiện đủ số liệu |
| 7 | `MonthlyPaymentService::applyCommonFilter` — thống kê doanh thu tháng — `app/Services/MonthlyPaymentService.php` | Không đổi | Đã check không join `bot_contracts` |
| 8 | `Admin\UserController` — thống kê doanh thu theo tháng lọc `flag_display` — `app/Http/Controllers/Admin/UserController.php:188` | Không đổi | Đã check không join `bot_contracts` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `UpdateFlagDisplayBillYearAffByMonthly::handle` | `app/Console/Commands/UpdateFlagDisplayBillYearAffByMonthly.php` | Direct | Logic bật cờ chính, chạy cho cả 2 vòng lặp (payment_histories + payment_detail_aff) |
| F2 | `UpdateFlagDisplayBillYearAffByMonthly::canDisplayMonthlyBill` (hàm mới) | cùng file | Direct | Hàm điều kiện mới — thêm nhánh "hợp đồng đã bị xóa vẫn bật phân bổ" |
| F3 | `BotController::botDelete` | `app/Http/Controllers/Admin/BotController.php:1212` | Indirect | Luồng xóa bot — nguồn trigger bug, không sửa code nhưng là input của job |
| F4 | `RefundController::rollbackPlan` | `app/Http/Controllers/Admin/RefundController.php:408` | Indirect | Luồng hoàn tiền cũng xóa cứng hợp đồng — cùng pattern với F3, cần TC riêng vì có `status_refund` cần lọc đúng |
| F5 | `MonthlyPaymentService::applyCommonFilter` | `app/Services/MonthlyPaymentService.php` | Indirect | Đọc `flag_display` để tính doanh thu tháng — số liệu sẽ tăng sau fix |
| F6 | `SupperAdminController` (report hoa hồng affiliate) | `app/Http/Controllers/Admin/SupperAdminController.php:235` | Indirect | Đọc `flag_display` cho hoa hồng affiliate — số liệu sẽ tăng sau fix |
| F7 | `Admin\UserController` (thống kê doanh thu theo tháng) | `app/Http/Controllers/Admin/UserController.php:188` | Indirect | Đọc `flag_display` — số liệu sẽ tăng sau fix |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `payment_histories.flag_display` | UPDATE | Các dòng phân bổ tháng (`parent_month=0`, `remain_day>=365`) của hợp đồng **đã bị xóa** sẽ được bật `1` khi tới hạn |
| D2 | `payment_detail_aff.flag_display` + `payment_detail_aff.sub_amount` | UPDATE | Tương tự D1 cho hoa hồng affiliate — `sub_amount` tính lại theo công thức sẵn có (không đổi công thức) |

> ⚠️ Lưu ý vận hành (Dev tự note): các dòng tồn đọng từ trước (`payment_date` đã qua) sẽ được bật **hàng loạt ngay lần chạy job kế tiếp** sau khi release, làm doanh thu/hoa hồng của các tháng cũ trong báo cáo tăng lên đúng phần đã thu nhưng chưa phân bổ.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Monthly Payment Split (FS-010) — job phân bổ doanh thu bill năm theo tháng | F1, F2, D1, D2 | High |
| T2 | Payment History (FS-009) — lịch sử/thống kê thanh toán | D1, F5 | Medium |
| T3 | Affiliate Payment Mgmt (FS-013) — hoa hồng affiliate theo tháng | D2, F6 | Medium |
| T4 | Contract Plan & Payment (FA-031) — luồng hủy kết nối bot / hoàn tiền xóa cứng hợp đồng | F3, F4 | Low (chỉ là nguồn trigger, không đổi logic xóa) |

---

## Ghi chú vận hành & rủi ro khi test (theo Dev, journal #133415)

- **Chưa verify bằng data thật**: Dev không kết nối được DB dev (`host.docker.internal:3306` — Connection refused) nên chỉ test bằng reflection (`canDisplayMonthlyBill` qua Laravel bootstrap, 5 case giả lập: hợp đồng còn hạn=true, gói free=false, hết hạn=false, **hợp đồng đã bị xóa=true**, dòng không gắn hợp đồng=false — khớp mong đợi). **Chưa đếm được số dòng phân bổ "mồ côi" thực tế** trên DB → QA cần tự kiểm tra bằng dữ liệu thật.
- Đã xác nhận `bot_contracts` **không có cột `deleted_at`** (schema db-refined) → xóa là xóa cứng thật, bản ghi biến mất hoàn toàn (không phải soft-delete).
- Đã xác nhận report doanh thu (`MonthlyPaymentService`, `Admin\UserController`) và report affiliate (`SupperAdminController`) **chỉ lọc theo `flag_display`**, KHÔNG join `bot_contracts` → bật cờ là số liệu hiện đủ ngay, không cần sửa thêm ở tầng report.
- Rủi ro release: lần chạy job đầu tiên sau release sẽ bật hàng loạt dòng tồn đọng của các tháng đã qua → doanh thu/hoa hồng affiliate các tháng cũ tăng đột ngột trong báo cáo. Đúng mong đợi ticket, nhưng nên báo trước kế toán/PM; nếu chỉ muốn áp dụng từ nay về sau thì cần thêm mốc thời gian chặn (hiện fix **không** có mốc chặn này).
- Hợp đồng bị xóa do **hoàn tiền** (`RefundController::rollbackPlan`) cũng sẽ được phân bổ tiếp ở tầng job; các report hiện tại đều lọc `status_refund` nên không tính sai doanh thu — nhưng đây là điểm mong manh (report mới/sau này quên lọc `status_refund` sẽ lệch).
- Verify level Dev tự chạy: `lint` (`php -l` + `git diff --stat` xác nhận đúng 1 file, 48 thêm/18 xóa) — **chưa có integration test / chưa chạy job thật trên DB có data**.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
