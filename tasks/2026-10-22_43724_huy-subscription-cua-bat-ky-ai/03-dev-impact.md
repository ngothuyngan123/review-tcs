# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio |
| Commit / Pull Request | `<chưa có PR>` — commit `ed709c409dbba9cc62dd4b3b310abd741c26fc69` (vòng 1) · `d9c85776ee65634fdf5c7e9e059167039a65fc90` (vòng 2) |
| Branch | `ai_studio_fixbug_43724` (nhánh gốc `release_step_20260930_v2` @`4ae243379f82`) |
| Ngày submit đánh giá | 2026-10-22 |
| Auto-filled | 2026-10-22 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ Input của ticket này **KHÔNG** có section "Đánh giá ảnh hưởng" theo format chuẩn — nội dung đánh giá nằm trong **2 journal Dev Studio** (xem nguyên văn ở `01-bug-task.md`). Đã gộp 2 vòng fix (bảo mật + counter) vào 4 mục dưới đây.

---

## 1. Nguyên nhân

**Vòng 1 — lỗ hổng bảo mật (nguyên nhân chính của ticket):**
Route `/ajax/mobile/cancel-cycle-order` (V2, trang 解約 khách) và `/ajax/cancel-cycle-order` (V1) là route công khai, `/ajax/*` được miễn CSRF. Bản vá #40699 chỉ so bot của hợp đồng với bot trong session **khi có session**; request không đăng nhập bỏ qua mọi kiểm tra rồi huỷ theo `cycle_order_id` gửi lên. Request trang khách chỉ có `cycle_order_id` (số tự tăng), không có gì định danh khách → lần lượt từng id là huỷ được hợp đồng của mọi bot.

**Vòng 2 — bug phụ phát sinh trong QA vòng 1 (`#43899`–`#43904`, Test Studio `#3771`–`#3775`):**
Hàm dùng chung `sendActionOrderItem('cancel', …)` tự cộng `count_action_cancel` thêm 1 trước khi gửi action 解約時. Mọi nơi gọi trong luồng huỷ hợp đồng lại cộng 1 lần nữa → mỗi lần huỷ có action, bộ đếm tăng **2** thay vì 1. Lỗi có từ trước, không do bản vá vòng 1; `#42198` đã sửa đúng lỗi này ở luồng đổi thẻ nhưng chưa sửa ở luồng huỷ.

## 2. Cách fix

**Vòng 1:**
- D-1: V2 `cancelCycleOrder` — không có session thì bắt buộc `u_code` đúng chủ hợp đồng.
- D-2: Trang 解約 (khách) gửi kèm `u_code` khi gọi API huỷ.
- D-3: V1 `cancelCycleOrder` — thêm đúng kiểm tra như D-1.

**Vòng 2:**
- Bỏ phần `+1` lặp ở **7 nơi gọi** `sendActionOrderItem('cancel')` (hàm đã tự `+1`) → mỗi lần huỷ có action tăng đúng 1. Áp dụng cho mọi luồng huỷ có action: trang khách V2, API không-session (V1/V2), admin chi tiết V2, 一括解約, admin V1, và các luồng tự huỷ khi thanh toán lỗi (đổi thẻ V1 lỗi ≥3 lần, webhook UnivaPay, cron thu tiền Stripe, cron trial).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SalesManagementController.php` (V1 `cancelCycleOrder`) | Thêm kiểm tra `u_code` khi không có session; bỏ `+1` lặp `count_action_cancel` | D-3 (vòng 1) + vòng 2 |
| 2 | `SalesManagementV2Controller.php` (V2 `cancelCycleOrder`) | Thêm kiểm tra `u_code` khi không có session; bỏ `+1` lặp `count_action_cancel` | D-1 (vòng 1) + vòng 2 |
| 3 | `public/js/sales/v2/page-cancel.js` | Gửi kèm `u_code` khi gọi API huỷ | D-2 (vòng 1) |
| 4 | `app/Services/Sales/SalesService.php` | Bỏ `+1` lặp `count_action_cancel` | vòng 2 |
| 5 | `app/Console/Commands/HandleBillStripe.php` | Bỏ `+1` lặp `count_action_cancel` (tự huỷ khi lỗi thanh toán — cron Stripe) | vòng 2 |
| 6 | `app/Console/Commands/HandleSendActionTrialV2.php` | Bỏ `+1` lặp `count_action_cancel` (cron trial 07:00) | vòng 2 |
| 7 | `.../Basic/SalesStripePaymentController.php` | Bỏ `+1` lặp `count_action_cancel` | vòng 2 |
| 8 | `tests/Feature/CancelCycleOrderOwnerTest.php` (mới, 268 dòng) | Test coverage cho cả 2 vòng fix (harness Dev tự chạy) | regression |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `cancelCycleOrder` V2 (`/ajax/mobile/cancel-cycle-order`) | `SalesManagementV2Controller.php` | Direct | Thêm check `u_code` chủ hợp đồng khi không session + sửa counter |
| F2 | `cancelCycleOrder` V1 (`/ajax/cancel-cycle-order`) | `SalesManagementController.php` | Direct | Thêm check `u_code` chủ hợp đồng khi không session + sửa counter |
| F3 | Trang 解約 khách V2 (nút huỷ) | `public/js/sales/v2/page-cancel.js` | Direct | Gửi kèm `u_code`; **phụ thuộc version JS mới tới browser** (cache LINE) |
| F4 | `sendActionOrderItem('cancel', …)` — 7 nơi gọi | `SalesService.php`, `HandleBillStripe.php`, `HandleSendActionTrialV2.php`, `SalesStripePaymentController.php`, 2 controller V1/V2 | Direct | Bỏ `+1` lặp, hàm dùng chung không đổi logic |
| F5 | Màn admin chi tiết đơn định kỳ V2 (`/ajax/sales/cancel-cycle-order`, cùng hàm với F1) | `SalesManagementV2Controller.php` | Indirect | Có session → không vào nhánh check `u_code` mới, nhưng dùng chung hàm đã sửa counter → **cần test hồi quy** |
| F6 | 一括解約 (huỷ hàng loạt ở danh sách V2) | `SalesManagementV2Controller.php` | Indirect | Dùng chung hàm V2 → counter đổi |
| F7 | Màn hợp đồng quản trị V1 (`cycle_order_history`, `edit_cycle_order`) | `SalesManagementController.php` | Indirect | Có session → hành vi check không đổi, nhưng counter đổi |
| F8 | `changeCardItem` V2 (`/ajax/change-card-item/v2`) | `SalesManagementV2Controller.php` | **Không sửa** | Dev ghi nhận lỗ hổng tương tự (tra `cycle_id` không kiểm chủ hợp đồng) — đề nghị **mở ticket riêng**, NGOÀI phạm vi #43724 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_line_user_item.count_action_cancel` | UPDATE (logic) | Sửa tăng đúng 1 thay vì 2 mỗi lần huỷ có action; Dev xác nhận **không cần recover** dữ liệu cũ (giá trị 2 vs 1 cho cùng kết quả vì chỉ so với 0, không màn nào hiển thị, java-job/java-mcp/app mobile không đọc cột này) |
| D2 | Trạng thái hợp đồng (`status_contract` / trạng thái 解約) qua nhánh check owner mới | UPDATE (logic, không migration) | Request không hợp lệ (không session, `u_code` sai/bot khác/đã chặn) sẽ **không còn** làm đổi trạng thái này |
| — | Migration / DB schema | Không có | Dev xác nhận "đã kiểm diff" cả 2 vòng |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Trang 解約 (huỷ hợp đồng) của khách — web + LIFF | F1, F3, D2 | High |
| T2 | API huỷ hợp đồng không đăng nhập (V1 + V2 mobile) | F1, F2, D2 | High |
| T3 | Màn admin chi tiết hợp đồng V2 (SCR-BIL-19) + 一括解約 | F5, F6, D1 | Medium |
| T4 | Màn quản trị hợp đồng V1 (`cycle_order_history`, `edit_cycle_order`) | F7, D1 | Medium |
| T5 | Tự huỷ hợp đồng khi thanh toán lỗi (đổi thẻ V1 lỗi ≥3 lần, webhook UnivaPay, cron `handle:bill_stripe`, cron trial 07:00) | F4, D1 | Medium — không tái hiện được trên môi trường test theo Dev, chỉ theo dõi log `job_crontab` |
| T6 | `changeCardItem` V2 (lỗ hổng tương tự F8, **chưa fix**) | F8 | Ghi nhận risk, **ngoài phạm vi task** — không đưa vào coverage TC của #43724 |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
