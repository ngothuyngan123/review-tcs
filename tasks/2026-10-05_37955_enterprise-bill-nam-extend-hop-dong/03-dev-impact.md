# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #37955 qua `/new-task` (2026-10-05), parse từ **Journal #133054 — AI LME Fix bug — 2026-08-26** (báo cáo AI auto-fixbug, không phải Dev người). Tester verify rồi tick checkbox dưới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (hệ thống Auto-fixbug LME) — không có Dev người được assign cụ thể trên journal` |
| Commit / Pull Request | `commit c20fe4780d (không có PR link, chỉ có branch/commit trên journal)` |
| Branch | `ai_fixbug_37955` (nhánh gốc `release_step_20260805`, repo `sns-line`) |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-10-05 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #133054 trên Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact) + mục 5 (Recover data).

---

## 1. Nguyên nhân

Khi hợp đồng đổi kỳ thanh toán từ tháng sang năm, hệ thống giữ kỳ cũ ở cột `bill_type_old` vì kỳ năm mới chỉ có hiệu lực từ lần thu tiền kế tiếp, và mọi màn hiển thị đều ưu tiên kỳ cũ này để tính tiền. Việc gia hạn hợp đồng thực chất đã thu tiền theo kỳ năm mới, nhưng luồng xử lý gia hạn thành công là luồng thu tiền DUY NHẤT quên xoá cờ kỳ cũ và quên cập nhật số tiền đã thu vào hợp đồng, nên màn chi tiết và lịch sử vẫn hiện giá bill tháng.

## 2. Cách fix

Sửa luồng gia hạn hợp đồng thành công trong `Admin/BotController`: sau khi thu tiền theo kỳ mới thì xoá cờ kỳ thanh toán cũ (`bill_type_old`) và cập nhật số tiền đã thu (`amount_payment`) của hợp đồng, áp dụng cho cả nhánh thẻ tín dụng (`handleExtendContractSuccess`) lẫn nhánh chuyển khoản ngân hàng; đồng thời bản ghi lịch sử gia hạn nhánh chuyển khoản lấy số tiền từ bản ghi thanh toán cha thay vì đọc số tiền cũ còn lưu trong đối tượng hợp đồng chưa refresh. Quét ngang xác nhận 3 luồng thu tiền còn lại (đổi thẻ, job thu định kỳ) đã xoá cờ kỳ cũ sẵn, chỉ luồng gia hạn bỏ sót.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotController::handleExtendContractSuccess` (app/Http/Controllers/Admin/BotController.php) | **Sửa** — thêm xoá `bill_type_old` + cập nhật `amount_payment` | Nhánh gia hạn bằng thẻ — nơi fix chính |
| 2 | `BotController::univapayCallback` — nhánh gia hạn chuyển khoản (app/Http/Controllers/Admin/BotController.php) | **Sửa** — thêm xoá `bill_type_old` + cập nhật `amount_payment` lấy từ bản ghi thanh toán cha | Nhánh gia hạn bằng chuyển khoản — nơi fix chính |
| 3 | `BotController::handleCallbackChangeCardSuccess` (app/Http/Controllers/Admin/BotController.php) | Không đổi — đối chiếu | Mẫu tham chiếu: luồng đổi thẻ đã xoá cờ đúng từ trước |
| 4 | `PointSettingController::extendContract` (app/Http/Controllers/PointSettingController.php) | Không đổi — đối chiếu | Luồng gia hạn, kiểm tra điểm gọi callback đúng |
| 5 | `PointSettingController::changeTypePayment` (app/Http/Controllers/PointSettingController.php) | Không đổi — đối chiếu | Nơi sinh cờ kỳ cũ `bill_type_old` khi đổi kỳ tháng→năm |
| 6 | `AutoPaymentJobUnivapay::chargeStripeBots` / `chargeUnivapayCardBots` (app/Console/Commands/AutoPaymentJobUnivapay.php) | Không đổi — đối chiếu | Job thu định kỳ — đã xoá cờ đúng từ trước, dùng làm đối chứng |
| 7 | `calculateSaleEnterprise` (app/Helpers/functions.php) | Không đổi — đối chiếu | Hàm tính giá theo bậc giảm giá おまとめ (ảnh hưởng số tiền hiển thị) |
| 8 | `getAmountContract` (public/_assets/modules/bill/js/detail.js) | Không đổi — đối chiếu | Hàm JS đọc số tiền hiển thị màn chi tiết, ưu tiên `bill_type_old` trước `contract_bill_type` |
| 9 | `detail.blade.php` mục ご利用料金 / お支払い期間 (resources/views/basic/bill/detail.blade.php) | Không đổi — đối chiếu | View hiển thị màn chi tiết hợp đồng |
| 10 | `payment_history/index.blade.php` cột số tiền (resources/views/basic/payment_history/index.blade.php) | Không đổi — đối chiếu | View cột số tiền màn lịch sử thanh toán |
| 11 | `state.blade.php` modal lịch sử hợp đồng (resources/views/basic/bill/modals/detail/state.blade.php) | Không đổi — đối chiếu | View modal chi tiết sự kiện gia hạn trong activity log |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BotController::handleExtendContractSuccess` | app/Http/Controllers/Admin/BotController.php | Direct | Nhánh gia hạn bằng thẻ — fix chính |
| F2 | `BotController::univapayCallback` (nhánh gia hạn chuyển khoản) | app/Http/Controllers/Admin/BotController.php | Direct | Nhánh gia hạn bằng chuyển khoản — fix chính, đồng thời đổi cách lấy amount cho bản ghi lịch sử |
| F3 | `getAmountContract` (JS) + view `detail.blade.php` / `payment_history/index.blade.php` / `state.blade.php` | public/_assets/modules/bill/js/detail.js + resources/views/basic/bill/** | Indirect | Không sửa code nhưng hành vi hiển thị đổi theo do dữ liệu nguồn (`bill_type_old`, `amount_payment`) thay đổi |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_contracts.bill_type_old` | UPDATE | Set `NULL` sau khi gia hạn thành công (trước đây giữ nguyên kỳ cũ) |
| D2 | `bot_contracts.amount_payment` | UPDATE | Cập nhật = số tiền thực thu kỳ năm (trước đây giữ số tiền của lần thu trước) |
| D3 | `bot_life_cycles.data.amount` | UPDATE | Bản ghi lịch sử gia hạn nhánh chuyển khoản nay lưu đúng số tiền thực thu (lấy từ bản ghi cha `payment_histories`, `parent_month = 1`) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Contract Plan & Payment (FA-031) — màn 契約詳細 (Chi tiết hợp đồng) | F1, F2, D1, D2 | High |
| T2 | Payment History (FS-009) — màn 決済履歴 (Lịch sử thanh toán) + modal lịch sử hợp đồng trong activity log | F2, D2, D3 | High |
| T3 | Màn danh sách hợp đồng 契約情報 (SCR-DC-01) | D1, D2 (gián tiếp — cùng dùng cột `bill_type_old`/`amount_payment` để hiển thị) | Medium — **Dev không tự kê mục này ở 4.1-4.3**, nhưng Studio đã bổ sung TC coverage riêng (xem `04-tc-list.md` NEW-6) vì màn danh sách dùng chung nguồn dữ liệu với màn chi tiết |

### 4.4. Recover data (dữ liệu cũ cần xử lý — nguyên văn mục 5 Journal #133054)

⚠ **CÓ** — Hợp đồng đã gia hạn TRƯỚC khi fix lên release vẫn còn `bill_type_old` khác NULL và `amount_payment` là số tiền kỳ cũ, nên vẫn hiển thị sai cho tới lần thu tiền định kỳ kế tiếp (lúc đó job mới tự xoá cờ). Cần rà và sửa dữ liệu cho các hợp đồng này.

- **Phạm vi**: lọc `bot_contracts` có `bill_type_old` khác NULL và có bản ghi `payment_histories` reason bắt đầu bằng `pay_year_fee_extend_` (`parent_month = 1`) phát sinh SAU thời điểm đổi kỳ.
- **Cách xử lý**: với các hợp đồng đó, set `bill_type_old = NULL` và `amount_payment` = số tiền của bản ghi gia hạn gần nhất.
- Hệ thống **KHÔNG tự chạy** lệnh cập nhật dữ liệu — cần dev/vận hành thực hiện trên môi trường thật sau khi release.
- Studio đã sinh sẵn 1 TC khảo sát (REQ-011, NEW-16, `tc_group=data`) để rà phạm vi hợp đồng cần Recover data trước khi đóng ticket — xem `04-tc-list.md`.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
