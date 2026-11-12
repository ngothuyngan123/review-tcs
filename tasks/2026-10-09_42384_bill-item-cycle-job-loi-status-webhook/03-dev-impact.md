# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (hệ thống Auto-fixbug)` |
| Commit / Pull Request | `sns-line: commit 50c254e430 (git diff --stat release_step_20260930_v2...ai_small_42384: 2 file, +30/-1)` |
| Branch | `ai_small_42384` (nhánh gốc `release_step_20260930_v2`) |
| Ngày submit đánh giá | `2026-10-08` (journal cuối #141828) |
| Auto-filled | `2026-10-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

<!--
⚠️ Redmine #42384 KHÔNG có description dạng "Đánh giá ảnh hưởng phía dev" chuẩn — nội dung dưới đây được ghép từ journal cuối cùng (#141828) của hệ thống "AI LME Fix bug" (auto-fixbug), là journal đầy đủ nhất sau 3 lượt revision (#141253 → #141592 → #141828) cùng ngày 2026-10-08. Giữ nguyên văn mục 1-4 từ journal #141828.
-->

---

## 1. Nguyên nhân

Job thu tiền định kỳ sản phẩm (bill item) qua UnivaPay: ở nhánh thu đồng bộ (không chờ webhook) hoặc khi gọi thu bị từ chối ngay (không có charge ID), sau khi có kết quả job luôn đặt status_webhook của hợp đồng định kỳ = 1 (đã xử lý) bất kể thu thành công hay lỗi; còn khi lỗi lấy thông tin thẻ thì không cập nhật status_webhook (giữ giá trị của kỳ trước). Luồng nhận webhook (callbackJob) thì đặt đúng 2 (lỗi) khi thu lỗi nên 2 luồng lệch nhau.

## 2. Cách fix

Job thu định kỳ bill item UnivaPay: khi thu lỗi (thu đồng bộ trả lỗi/failed, hoặc gọi thu bị từ chối không có charge ID) đặt status_webhook hợp đồng = 2 (lỗi) thay vì luôn = 1; thu thành công vẫn = 1. Khi lỗi lấy thông tin thẻ cũng đặt = 2 qua hàm mới `CycleOrderHistory::markPaymentError` (UPDATE có điều kiện, không đè hợp đồng đang chờ kết quả thanh toán của lượt khác như màn đổi thẻ). Quét ngang: màn đổi thẻ UnivaPay cũng ghi 1 khi thu lỗi — khác luồng, ghi yokoten **ngoài scope**.

[#42450] `CycleOrderHistory::claimPendingPayment` thêm `$cycle->syncOriginal()` sau `refresh()`: `refresh()` của Laravel 5.5 không đồng bộ original nên update status_webhook về đúng giá trị trước claim (HĐ đang lỗi 2 thu lại lỗi → 2; HĐ 1 thu OK → 1) bị Eloquent bỏ qua, hợp đồng kẹt ở 3 (bot không webhook)/0 (bot webhook).

[#42499] Điều tra, **KHÔNG sửa code**: màn đổi thẻ UnivaPay (bot có webhook, kết quả còn chờ) cố ý giữ nguyên `count_bill_error` (vd 1) vì callback webhook đổi thẻ (`SalesService::callbackChangeCard`) chỉ chốt kết quả khi `count_bill_error` còn giá trị (thu OK → NULL, thu lỗi → +1), và job xử lý quá hạn webhook (`getOrderTimeout` #41974) coi `count_bill_error=NULL` là charge đổi thẻ đã chốt. Nếu reset ở nhánh chờ thì webhook về sẽ bỏ qua, khách đã bị trừ tiền nhưng hợp đồng không gia hạn. Đề nghị Dev/PO xác nhận và trả lời Redmine #42499 là đúng thiết kế.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleSendActionTrialV2::billItemUnivapay` (`app/Console/Commands/HandleSendActionTrialV2.php`) | Sửa: đặt `status_webhook` = 2 khi thu lỗi (thay vì luôn 1) | Root cause chính của bug |
| 2 | `CycleOrderHistory::claimPendingPayment` / `markPaymentError` (`app/CycleOrderHistory.php`) | Sửa: thêm hàm `markPaymentError` (UPDATE có điều kiện cho nhánh lỗi lấy thông tin thẻ) + thêm `syncOriginal()` sau `refresh()` trong `claimPendingPayment` (fix kèm #42450) | Đảm bảo update `status_webhook` không bị Eloquent bỏ qua, không đè hợp đồng đang chờ của lượt khác |
| 3 | `SalesService::callbackJob` (`app/Services/Sales/SalesService.php`) | Không sửa — chỉ đối chiếu | Đối chiếu luồng webhook đặt ERROR khi lỗi, để thống nhất 2 luồng |
| 4 | `SalesService::getOrderTimeout` (`app/Services/Sales/SalesService.php`) | Không sửa — chỉ đối chiếu | Chỉ nhặt status 0/3/4, ERROR (2) không bị nhặt → không ảnh hưởng |
| 5 | `SalesManagementV2Controller::cancelCycleOrder` / `changeCardUnivapay` / mua lại (`app/Http/Controllers/Basic/SalesManagementV2Controller.php`) | Không sửa — chỉ đối chiếu | Chỉ chặn khi status 0/3/4, ERROR (2) xử lý như 1 (không chặn) → không ảnh hưởng |
| 6 | view `cycle-history-detail.blade.php` / `list-order-history.blade.php` | Không sửa — chỉ đối chiếu | Đọc `status_webhook` của `order_history`, không phải của hợp đồng (`s_cycle_order_history`) → không ảnh hưởng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandleSendActionTrialV2::billItemUnivapay` | `app/Console/Commands/HandleSendActionTrialV2.php` | Direct | Job thu định kỳ bill item UnivaPay — đổi logic set `status_webhook` khi lỗi |
| F2 | `CycleOrderHistory::markPaymentError` (hàm mới) | `app/CycleOrderHistory.php` | Direct | UPDATE có điều kiện cho nhánh lỗi lấy thông tin thẻ, không đè hợp đồng đang chờ thanh toán của lượt khác |
| F3 | `CycleOrderHistory::claimPendingPayment` | `app/CycleOrderHistory.php` | Direct | Thêm `syncOriginal()` sau `refresh()` — ảnh hưởng toàn bộ nơi gọi hàm này, gồm cả màn đổi thẻ UnivaPay (`changeCardUnivapay`, dùng chung) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `s_cycle_order_history.status_webhook` | UPDATE | Job thu định kỳ UnivaPay thu lỗi nay ghi 2 (lỗi) thay vì 1. Mọi chỗ đọc chỉ phân biệt nhóm đang chờ (0/3/4) với còn lại nên 2 được xử lý giống 1 (không chặn thu lại kỳ sau, không chặn huỷ/đổi thẻ). **Không cần recover data.** |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Single Product / Sales (FA-026) — Job thu tiền định kỳ hợp đồng sản phẩm qua UnivaPay (`HandleSendActionTrialV2::billItemUnivapay`) | F1, D1 | Medium — khi thu lỗi `status_webhook` = 2 (lỗi) thay vì 1; thu thành công, số lần lỗi, đơn lỗi, action/tin nhắn báo lỗi, tự huỷ hợp đồng **KHÔNG đổi** |
| T2 | Single Product / Sales (FA-026) — Job thu tiền định kỳ hợp đồng sản phẩm qua UnivaPay, nhánh hợp đồng ĐANG lỗi (2) hoặc đã xử lý (1) thu lại kỳ sau | F3, D1 | Medium — `status_webhook` nay ghi đúng kết quả (2/1) thay vì kẹt ở trạng thái chờ 3/0 (do fix kèm #42450) |
| T3 | Single Product / Sales (FA-026) — Màn đổi thẻ UnivaPay (`SalesManagementV2Controller::changeCardUnivapay`, dùng chung `CycleOrderHistory::claimPendingPayment`) | F3 | Low — các lệnh `$cycle->update` sau claim (`c_univapay_charge_id`, `count_bill_error`, `status_webhook=4`) nay so với giá trị DB sau claim — kết quả hiện tại không đổi (các giá trị này luôn khác giá trị trước claim) |

**KHÔNG ảnh hưởng** (theo Dev): job thu định kỳ Stripe (`HandleBillStripe`), luồng nhận webhook `callbackJob`, hiển thị lịch sử đơn hàng (đọc `status_webhook` của đơn, không phải hợp đồng).

**Chưa kết luận — cần Leader/Dev/PO xác nhận riêng** (không thuộc scope fix #42384, chỉ ghi nhận từ điều tra #42499): màn đổi thẻ UnivaPay cố ý giữ `count_bill_error` ở nhánh chờ webhook — có thể ảnh hưởng kỳ vọng của TC `NEW-18` trên test tool. **Không tự kết luận đúng/sai, chờ xác nhận.**

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] Xác nhận riêng với Dev/PO về kết luận #42499 (count_bill_error ở nhánh chờ webhook) trước khi review TC `NEW-18`
