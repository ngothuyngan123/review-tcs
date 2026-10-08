# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (auto-fixbug)` — điều tra ban đầu bởi `Do Van Tu TuDV` (journal #139789) |
| Commit / Pull Request | `7b8b977178` (3 file, không có link PR — chỉ có branch + commit hash) |
| Branch | `ai_fixbug_41891` (nhánh gốc: `release_step_20260930_v2`), repo `sns-line` — đã push |
| Ngày submit đánh giá | `2026-10-03` (journal #139876) |
| Auto-filled | `2026-10-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Race giữa job thu tiền định kỳ UnivaPay (`HandleSendActionTrialV2::billItemUnivapay`, chạy 07:00) và job recover giao dịch treo (`SalesService::getOrderTimeout`, chạy 5 phút/lần). Job thu đặt hợp đồng sang trạng thái chờ webhook (`status_webhook=0`) nhưng vẫn giữ mã giao dịch CŨ (lần đổi thẻ 26/08); job recover nhặt đúng lúc đó, hỏi UnivaPay giao dịch cũ (đã thành công từ lâu nên lọt kiểm tra 15 phút), xử lý lại nó rồi đánh dấu hợp đồng là đã xử lý (`PROCESSED`). Giao dịch thật 25/09 vì vậy bị bỏ qua (webhook của nó cũng bị chặn do hợp đồng đã ở trạng thái đã xử lý), hạn thanh toán không được dời nên 26/09 job thu thêm lần nữa và tạo đơn 411193.

Kèm lỗi riêng: job recover crash `Undefined index: module` ở hợp đồng 41884 (charge test 0 yên, không có module) từ 25/09, khiến mọi hợp đồng xếp sau trong danh sách không bao giờ được recover.

⚠️ **Câu hỏi 3 của khách hàng (lỗi hoàn tiền 「キャンセル失敗しました」 ở `cancelOrderV2`/order 411193) CHƯA được điều tra** trong đánh giá này — xem mục 2.

## 2. Cách fix

Job thu định kỳ UnivaPay và 2 luồng đổi thẻ (UnivaPay, Stripe) nay xoá mã giao dịch cũ (`c_univapay_charge_id`/`c_strip_charge_id` = NULL) **cùng lúc** với đặt trạng thái chờ webhook, nên job recover không còn nhặt nhầm hợp đồng đang thu. Job recover đọc lại hợp đồng ngay trước khi xử lý và bỏ qua nếu trạng thái hoặc mã giao dịch đã đổi; bỏ qua (có log) giao dịch không có `module` thay vì crash; bọc try/catch từng bản ghi để 1 bản ghi lỗi không chặn các bản ghi sau.

**Tự review của AI** (khác hướng đề xuất ban đầu của TuDV ở 2 điểm):
- (a) KHÔNG lọc "chỉ module sales_job" vì job recover còn phải xử lý hợp đồng mua lần đầu (module `sales`) và đổi thẻ (`sales_change_card`) — thay bằng kiểm mã giao dịch hiện tại của hợp đồng phải trùng mã vừa đọc.
- (b) KHÔNG so `created_on` với "lần bill hiện tại" vì không có cột nào lưu mốc bắt đầu lần thu (`updated_at` bị ghi lại khi lưu mã giao dịch mới nên dùng sẽ bỏ nhầm giao dịch thật).

⚠️ **Câu 3 (lỗi hoàn tiền đơn 411193) CHƯA SỬA** — Dev tự ghi rõ cần log hoàn tiền (`refundMoney`/`getRefundMoney` quanh 15:5x ngày 02/10) để điều tra tiếp; màn chi tiết hợp đồng đang nuốt message lỗi server trả về.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleSendActionTrialV2::billItemUnivapay` — `app/Console/Commands/HandleSendActionTrialV2.php` | Set `c_univapay_charge_id`/`c_strip_charge_id` = NULL cùng lúc set `status_webhook=0` (bot có webhook) hoặc `3` (bot không webhook); mã mới chỉ ghi lại sau khi cổng trả về chargeId | Tránh job recover nhặt đúng lúc hợp đồng đang thu (root cause) |
| 2 | `SalesService::getOrderTimeout` — `app/Services/Sales/SalesService.php` | Đọc lại trạng thái + mã giao dịch của hợp đồng ngay trước khi xử lý; bỏ qua (có log) nếu đã đổi so với lúc query ban đầu; bỏ qua (có log) charge thiếu `metadata.module` thay vì crash; bọc try/catch từng bản ghi (cả đơn 1 lần lẫn cycle) | Fix race + fix crash `Undefined index: module` (cycle 41884) chặn các bản ghi xếp sau |
| 3 | `SalesManagementV2Controller::changeCardUnivapay` — `app/Http/Controllers/Basic/SalesManagementV2Controller.php` (`POST /ajax/change-card-univapay/v2`) | Xoá mã giao dịch cũ khi bắt đầu thu lại hợp đồng đang lỗi bill (`count_bill_error` có giá trị, `c_expired_date < now`) | Đồng bộ cơ chế tránh race với luồng thu định kỳ |
| 4 | `SalesManagementV2Controller::updatePaymentIntent` — cùng file (`POST /ajax/update-payment-intent`) | Xoá mã giao dịch (PaymentIntent) cũ khi bắt đầu thu lại hợp đồng đang lỗi bill | Đồng bộ cơ chế tránh race (nhánh Stripe) |
| 5 | `SalesService::callbackJob` / `callbackChangeCard` | Không đổi logic — vẫn bỏ qua khi `status_webhook` đã `PROCESSED` | Đã check, không cần sửa thêm |
| 6 | `HandleWebhookUnivapay::handle` | Không đổi — vẫn route theo `metadata.module` | Đã check, không sửa |
| 7 | `SalesManagementV2Controller::cancelOrderV2` | **CHƯA SỬA** | Đây là hàm xử lý Câu 3 (lỗi hoàn tiền 「キャンセル失敗しました」) — Dev chưa điều tra/fix trong lần này |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandleSendActionTrialV2::billItemUnivapay` (job 07:00) | `app/Console/Commands/HandleSendActionTrialV2.php` | Direct | Luồng chính cần test kỹ: thu định kỳ thành công qua webhook → đúng 1 đơn, `number_payment` tăng, `c_expired_date` dời đúng chu kỳ, không thu lại ngày hôm sau |
| F2 | `SalesService::getOrderTimeout` (job `recover:payment_univapay_timeout`, 5 phút/lần) | `app/Services/Sales/SalesService.php` | Direct | Webhook không về: job recover phải chốt đơn sau ≥15 phút kể từ charge MỚI (không phải charge cũ); đúng 1 đơn; không gửi tin 「決済が完了しました。」dựa trên charge cũ |
| F3 | `SalesManagementV2Controller::changeCardUnivapay` (`POST /ajax/change-card-univapay/v2`) | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Direct | Đổi thẻ UnivaPay khi hợp đồng đang nợ kỳ → thu lại ngay bằng thẻ mới |
| F4 | `SalesManagementV2Controller::updatePaymentIntent` (`POST /ajax/update-payment-intent`) | cùng file | Direct | Đổi thẻ Stripe khi hợp đồng đang nợ kỳ → thu lại bằng PaymentIntent mới |
| F5 | `SalesService::callbackJob` / `callbackChangeCard` | cùng file | Indirect | Không đổi code nhưng hành vi phụ thuộc trực tiếp vào F1/F2 (chỉ xử lý khi mã giao dịch còn khớp) |
| F6 | `HandleWebhookUnivapay::handle` | (không rõ file cụ thể) | Indirect | Route theo `metadata.module`, không đổi — nhưng giờ phụ thuộc đúng charge nào được coi là "đang xử lý" |
| F7 | `SalesManagementV2Controller::cancelOrderV2` (hoàn tiền 1 lần thu) | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Indirect / **CHƯA FIX** | Liên quan trực tiếp Câu 3 của khách hàng (lỗi 「キャンセル失敗しました」) nhưng CHƯA được sửa trong lần này — chỉ nên verify "smoke mapping" (hoàn tiền trỏ đúng charge), KHÔNG kỳ vọng lỗi đã hết |
| F8 | `SalesService::cancelCycle` (auto-cancel sau 3 lần lỗi bill) → `cancelSubcriptionSale` | `app/Services/Sales/SalesService.php` | Indirect (rủi ro Dev tự nêu) | Truyền `c_univapay_charge_id` — giá trị nay có thể NULL sau lần thu lỗi không có chargeId → cần regression nhẹ cho auto-cancel |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `s_cycle_order_history.c_univapay_charge_id` / `c_strip_charge_id` | UPDATE | Set NULL lúc bắt đầu thu/đổi thẻ; ghi lại ngay khi cổng thanh toán trả mã giao dịch mới |
| D2 | `s_cycle_order_history.status_webhook` | UPDATE | Job recover chỉ xử lý khi vẫn `0/3/4` VÀ mã giao dịch không đổi so với lúc đọc danh sách |
| D3 | Recover data thủ công (môi trường test/thật trước deploy) | MIGRATE/manual | (1) Hoàn tiền charge UnivaPay `11f1b865-6655-100a-9a5d-c322190a8a44` (25/09, 6,980円) trực tiếp trên dashboard UnivaPay. (2) Query `s_cycle_order_history WHERE status_webhook IN (0,3,4) AND (c_univapay_charge_id IS NOT NULL OR c_strip_charge_id IS NOT NULL)` trước deploy — các hợp đồng kẹt sẽ được recover hàng loạt ngay sau deploy. (3) Hợp đồng `41884` (charge test 0円) cần xử lý tay `status_webhook`. Phạm vi: cycle `38266` + các hợp đồng khác đang kẹt |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Thu tiền định kỳ UnivaPay (Product Sales / Recurring Item — FA-026) | F1, D1, D2 | High — gây double charge trực tiếp nếu fix sai/thiếu |
| T2 | Đổi thẻ thanh toán (UnivaPay/Stripe) — màn LIFF đổi thẻ của friend | F3, F4, D1 | High |
| T3 | Job recover giao dịch treo (`recover:payment_univapay_timeout`) | F2, D2 | High — chạy mỗi 5 phút, ảnh hưởng toàn hệ thống (cả đơn 1 lần lẫn cycle) nếu logic sai |
| T4 | Hoàn tiền 1 lần thu (màn lịch sử thanh toán 「決済履歴」→「この画面から返金を行う」) | F7 | High — **CHƯA FIX**, Câu 3 của khách hàng vẫn còn lỗi 「キャンセル失敗しました」 |
| T5 | Auto-cancel hợp đồng sau 3 lần lỗi bill liên tiếp | F8 | Medium — rủi ro Dev tự nêu, cần regression nhẹ |
| T6 | Luồng recover dùng chung cho mua lần đầu (module `sales`) và đơn 1 lần | F2 | Medium — fix KHÔNG lọc riêng module `sales_job` nên phải test không phá luồng cũ |

---

## Bổ sung — `dev_impact` chi tiết từ MCP LME TEST STUDIO (`task_get_context`, task #357)

<!-- Lấy từ tab Thông tin của Studio — diff thật (diffAvailable=true), bổ sung các điểm chưa nêu rõ ở journal Redmine. -->

- Luồng chính cần test kỹ: thu định kỳ thành công qua webhook → đúng 1 đơn, `number_payment` tăng, `c_expired_date` dời đúng chu kỳ, không thu lại ngày hôm sau.
- Webhook không về: job recover phải chốt đơn sau ≥15 phút kể từ charge MỚI (không phải charge cũ), đúng 1 đơn, không gửi tin 「決済が完了しました。」dựa trên charge cũ.
- Hợp đồng từng đổi thẻ sau lỗi bill (`c_univapay_charge_id` trỏ charge `sales_change_card` cũ) là dữ liệu kích hoạt bug — cần seed record cũ kiểu này khi test (Studio gắn knowledge `TOOL-OLDREC-001`).
- Rủi ro MỚI (Studio tự suy từ diff, Dev chưa nêu trong journal): lỗi mạng/5xx khi gọi `chargeMoneyUnivapaySale` SAU KHI đã NULL mã giao dịch cũ → cycle có thể kẹt ở `status_webhook` 0/3 với mã NULL, cả job thu lẫn job recover đều bỏ qua (không ai nhặt lại được) → **cần TC cho case này**.
- Rủi ro CŨ còn lại (Dev/AI tự nêu): cycle đang ở `0/3/4` trỏ mã giao dịch cũ do lỗi TRƯỚC ĐÂY (không phải do race lần này) vẫn có thể bị xử lý lại.
- Một bản ghi lỗi (vd charge test 0円 không module) không còn chặn các bản ghi sau; sau deploy các hợp đồng kẹt từ 25/09 sẽ được recover hàng loạt (có thể gửi tin trễ).
- `cancelCycle` (auto-cancel sau 3 lần lỗi) truyền `c_univapay_charge_id` vào `cancelSubcriptionSale` — giá trị nay có thể NULL sau lần thu lỗi không có chargeId → cần regression nhẹ cho auto-cancel.
- Hoàn tiền đơn (`cancelOrderV2`) KHÔNG bị sửa; lỗi 「キャンセル失敗しました」 vẫn tồn tại.

**Diff thật** (`spec_delta`, task #357): `diffAvailable=true`, 3 file thay đổi, +206/-153 dòng:
- `app/Console/Commands/HandleSendActionTrialV2.php` (+9/-…)
- `app/Http/Controllers/Basic/SalesManagementV2Controller.php` (+13/-…)
- `app/Services/Sales/SalesService.php` (+337/-… tổng, phần lớn thay đổi nằm ở đây)

**12 `requirements` đã có sẵn trên Studio** (REQ-001 → REQ-012, risk High × 9 / Medium × 3) — dùng để đối chiếu coverage ở BƯỚC 2 của `/review-tc`, KHÔNG cần suy lại từ đầu. Đáng chú ý: `REQ-009` (regression luồng không đổi: mua lần đầu/đơn 1 lần), `REQ-011` (dữ liệu tồn trước deploy), `REQ-012` (hoàn tiền — ghi rõ "lỗi キャンセル失敗しました chưa fix", risk Low vì chỉ cần test smoke mapping, không test lại lỗi cũ).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ Đã xác nhận với Dev/PO: Câu 3 (lỗi hoàn tiền) đúng là **chưa fix** trong round này, không phải sót khỏi báo cáo
