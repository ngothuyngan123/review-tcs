# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

> ⚠️ **NGUỒN**: note Auto-fixbug **#127882** (2026-08-03T08:06:42Z) — bản **MỚI NHẤT**, đã thay thế 2 note trước (#127877, #127878 lúc 07:49). Note mới ghi rõ **ĐÃ BỎ** hướng fix cũ (quy đổi trạng thái `authorized` → thành công ở job + webhook) vì "không phải nguyên nhân"; branch dựng lại chỉ còn **1 commit sửa 1 file**. **KHÔNG dùng nội dung 2 note cũ để viết TC.**

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — Redmine assigned_to: `Ngô Thúy Ngần` |
| Commit / Pull Request | Repo `sns-line`, commit `c9f1e6a091` (1 file, +18 dòng) — `<không có link Github/Gitlab trong Redmine>` |
| Branch | `ai_fixbug_39271` (nhánh gốc `release_step_20260623`) — đã push |
| Ngày submit đánh giá | `2026-08-03` (journal #127882, 08:06:42Z) |
| Auto-filled | `2026-08-05 by /new-task` |

Tham chiếu phiên AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=0d403621-5d69-4625-9515-0c5f1bba37be

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn §1 note #127882 -->

> Màn xác nhận mua sản phẩm định kỳ (thanh toán qua UnivaPay) không chặn thao tác mua khi giao dịch trước đó của CHÍNH khách đó với CHÍNH sản phẩm đó vẫn đang chờ kết quả từ cổng thanh toán (chưa nhận được phản hồi / quá thời gian chờ). Khách bấm mua lại trong lúc giao dịch cũ còn treo thì hệ thống vẫn nhận và tạo thêm một lần trừ tiền nữa cho cùng sản phẩm → thanh toán trùng.

## 2. Cách fix

<!-- Nguyên văn §2 note #127882 -->

> Chặn thanh toán chồng ở màn xác nhận mua sản phẩm qua UnivaPay: trước khi tính tồn kho và gọi cổng thanh toán, kiểm tra chính khách đó với chính sản phẩm đó có gói định kỳ đang hoạt động mà giao dịch còn ở trạng thái chờ xử lý (chưa nhận kết quả / hết thời gian chờ) hay không; nếu có thì dừng lại, trả lỗi và hiện cảnh báo 「決済処理を行っていますので、操作できません。」. Đã BỎ hướng sửa trước đó (quy đổi trạng thái 'đã ủy quyền' của UnivaPay thành thanh toán thành công ở job thu tiền định kỳ và webhook) vì không phải nguyên nhân — branch nay chỉ còn 1 commit sửa đúng 1 file.

**Chi tiết kỹ thuật Dev nêu ở §6 (bằng chứng)**:
- Bộ trạng thái "đang chờ" dùng hằng số `App\OrderHistory`: `STATUS_WEBHOOK_UNPROCESSED = 0` / `TIMEOUT = 3` / `TIMEOUT_WEBHOOK = 4` — cùng bộ mà job thu tiền định kỳ (`billItemUnivapay`) đang dùng để bỏ qua gói đang chờ kết quả.
- Guard dựa trên gói định kỳ **đang hoạt động** (`status_bill = 1`) của **cùng khách + cùng sản phẩm**.
- Guard đặt **trước** mọi lời gọi cổng thanh toán và **trước** khi tính tồn kho.
- Đường trả lỗi: route `/ajax/payment-credit-card-item-v2-univapay` → `confirm-order.js` nhánh `res.result != 'success'` → ẩn overlay, **bật lại nút mua**, `alert(res.error_message)`.
- Job `recover:payment_univapay_timeout` (`SalesService::getOrderTimeout`) đối soát và **gỡ trạng thái chờ sau 15 phút** → guard chỉ chặn trong thời gian ngắn.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn §3 note #127882, convert sang bảng. Cột "Thay đổi" theo đúng §4.1 (chỉ 1 file được sửa). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SalesManagementV2Controller::paymentCreditCardItemV2Univapay` — `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | **CÓ SỬA** — thêm guard chặn mua chồng | Điểm fix duy nhất; đặt trước tính tồn kho + gọi cổng thanh toán |
| 2 | `confirm-order.js` `nextStep` — `public/js/sales/v2/confirm-order.js` | Không sửa (đã check) | Nơi hiển thị `alert(error_message)` khi `res.result != 'success'` |
| 3 | `confirm-order.blade.php` — `resources/views/basic/sales/v2/order/confirm-order.blade.php` | Không sửa (đã check) | Nút mua nằm trong `v-show` nên luôn có trong DOM → không lỗi null khi bật lại nút |
| 4 | `CycleOrderHistory::createOrderPayment` — `app/CycleOrderHistory.php` | Không sửa (đã check) | Nơi tạo bản ghi thanh toán của gói định kỳ |
| 5 | `HandleSendActionTrialV2::billItemUnivapay` — `app/Console/Commands/HandleSendActionTrialV2.php` | Không sửa (đã check) | Tham chiếu bộ trạng thái chờ (`0 / 3 / 4`) mà guard dùng lại |
| 6 | `SalesService::getOrderTimeout` — `app/Services/Sales/SalesService.php` | Không sửa (đã check) | Job đối soát bù gỡ trạng thái chờ sau 15 phút |

---

## 4. Đánh giá ảnh hưởng

> ℹ️ Dev viết §4.1 dưới dạng **"File thay đổi"**, không đánh số `F1/F2` và không ghi cột Direct/Indirect. Mã `F* / D* / T*` bên dưới do `/new-task` gán để trace coverage theo quy ước repo — **nội dung giữ nguyên**, cột "Mức độ ảnh hưởng" suy từ việc file có bị sửa hay không (§3 + §4.1). Tester verify lại với Dev nếu nghi ngờ.

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn §4.1 note #127882: "File thay đổi: app/Http/Controllers/Basic/SalesManagementV2Controller.php" (đúng 1 file) -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `SalesManagementV2Controller::paymentCreditCardItemV2Univapay` — route `/ajax/payment-credit-card-item-v2-univapay` | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | **Direct** (file DUY NHẤT được sửa) | Thêm guard: nếu cùng khách + cùng sản phẩm có gói định kỳ `status_bill=1` mà `status_webhook ∈ {0,3,4}` → trả lỗi 「決済処理を行っていますので、操作できません。」 |
| F2 | `confirm-order.js` `nextStep` (hiển thị lỗi phía client) | `public/js/sales/v2/confirm-order.js` | Indirect (không sửa) | Nhánh `res.result != 'success'`: ẩn overlay + bật lại nút mua + `alert(error_message)` |
| F3 | `CycleOrderHistory::createOrderPayment` | `app/CycleOrderHistory.php` | Indirect (không sửa) | Không còn được gọi lần 2 khi guard chặn |
| F4 | `HandleSendActionTrialV2::billItemUnivapay` (job thu tiền định kỳ) | `app/Console/Commands/HandleSendActionTrialV2.php` | Indirect (không sửa — đã gỡ khỏi branch) | Hướng fix cũ từng sửa file này, note mới đã BỎ |
| F5 | `SalesService::getOrderTimeout` — job `recover:payment_univapay_timeout` | `app/Services/Sales/SalesService.php` | Indirect (không sửa — đã gỡ khỏi branch) | Gỡ trạng thái chờ sau 15 phút → điều kiện để guard nhả |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn §4.2 note #127882 -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `s_cycle_order_history.status_webhook` | **READ only** | Dev ghi rõ: "chỉ ĐỌC, dùng làm cờ 'đang chờ kết quả thanh toán' để chặn mua chồng; **fix không ghi thêm dữ liệu nào**". Giá trị chờ: `0` (chưa xử lý) / `3` (timeout) / `4` (timeout webhook) |
| D2 | `s_cycle_order_history.status_bill` | READ only | Điều kiện guard: gói định kỳ **đang hoạt động** (`= 1`) |

> ⚠️ **Khác biệt so với 2 note cũ**: note #127877/#127878 liệt kê thêm `s_cycle_order_history.c_expired_date`, `count_bill_error`, `s_order_history.status_order`, `bill_success_date` là **data bị GHI**. Note mới nhất **#127882 đã bỏ toàn bộ** phần đó (hướng fix cũ bị gỡ). Fix hiện tại **không WRITE data nào**.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn §4.3 note #127882 -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Single Product / Sales (FA-026)** — mua sản phẩm định kỳ qua UnivaPay: chặn thao tác mua khi giao dịch trước còn đang chờ kết quả | F1, D1, D2 | `<Dev không ghi mức — tester/Leader đánh giá>` |
| T2 | **Payment System Integration (FA-034)** — luồng thanh toán thẻ qua cổng UnivaPay ở màn xác nhận đơn | F1, F2 | `<Dev không ghi mức — tester/Leader đánh giá>` |

---

## 5. Recover data (từ §5 note #127882 — ngoài phạm vi code fix)

> ⚠ **CÓ** — Khách đã bị trừ tiền trùng trước khi có fix cần được đối soát và hoàn tiền thủ công (so lịch sử thanh toán LME với lịch sử giao dịch trên cổng UnivaPay), đồng thời huỷ gói định kỳ bị tạo dư nếu có. Việc này cần dữ liệu production nên do vận hành thực hiện; code fix không tự sửa dữ liệu cũ. (phạm vi: `s_cycle_order_history` + `s_order_history` của sản phẩm định kỳ thanh toán qua UnivaPay — ưu tiên kiểm khách của LOA 「[Hiroko公式]マナカード講師」 với sản phẩm 「マナフレンズ」)

## 6. Verify Dev đã làm (từ §6 note #127882)

| Hạng mục | Nội dung |
|---|---|
| Mức verify | **lint** (chưa chạy test thật) |
| Lệnh | `php -l app/Http/Controllers/Basic/SalesManagementV2Controller.php` → No syntax errors detected |
| Diff | `git diff --stat release_step_20260623...ai_fixbug_39271` → **1 file, +18 dòng** (branch đã dựng lại, không còn commit hướng fix sai) |
| Đọc mã | Route `/ajax/payment-credit-card-item-v2-univapay` là nơi **duy nhất** được gọi (grep `public/` + `resources/`) → `confirm-order.js` nhánh `res.result != 'success'` ẩn overlay, bật lại nút mua, `alert(res.error_message)`; nút nằm trong `v-show` nên luôn có trong DOM |
| ❌ **Không tái hiện được trên dev** | MySQL `host.docker.internal:3306` từ chối kết nối **và không có cửa hàng UnivaPay test** |

## 7. Rủi ro / lưu ý khi test (Dev tự nêu ở §TỰ REVIEW)

1. **Gói kẹt vĩnh viễn ở trạng thái chờ** — nếu webhook không về **và** job đối soát bù không chạy, khách **không mua lại được** sản phẩm đó cho tới khi trạng thái được gỡ. Bình thường job `recover:payment_univapay_timeout` xử lý sau **15 phút**.
2. **Stripe chưa có guard** — guard mới chỉ đặt ở luồng UnivaPay (`paymentCreditCardItemV2Univapay`); luồng thẻ **Stripe** của cùng màn xác nhận đơn **chưa có guard tương tự** (Dev ghi: ngoài phạm vi yêu cầu).
3. **Chưa tái hiện được trên dev** — verify dừng ở mức kiểm cú pháp + đọc mã.
4. *(từ note cũ, vẫn còn giá trị tham chiếu)* Chưa xác nhận được bằng dữ liệu production rằng khách 「マナフレンズ」 dính đúng trạng thái nào — ticket OEM chỉ 1 dòng, **không có mã đơn / ngày / ảnh**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm Leader nên hỏi Dev trước khi giao TC

- [ ] **Guard có chặn đúng phạm vi không?** — Điều kiện là "cùng khách + cùng sản phẩm". Khách mua **sản phẩm định kỳ KHÁC** trong lúc gói cũ đang treo có bị chặn nhầm không?
- [ ] **Sản phẩm 1 lần (single-shot)** có bị guard chạm tới không, hay chỉ áp cho sản phẩm định kỳ?
- [ ] **Bug gốc "trừ tiền trùng ở job thu tiền định kỳ"** (mô tả trong 2 note cũ: authorized bị coi là lỗi → hôm sau trừ lại) — note mới nói "không phải nguyên nhân". Vậy hiện tượng đó đã được fix ở ticket [#38077](../2026-06-24_38077_univapay-authorized-bill-success/) rồi, hay vẫn còn tồn tại? → quyết định có cần TC regression cho job thu tiền định kỳ hay không.
- [ ] **Env test**: có cửa hàng UnivaPay test trên staging không? Nếu không có, TC verify guard sẽ chạy ở đâu?
- [ ] Message lỗi 「決済処理を行っていますので、操作できません。」 hiển thị bằng **alert JS** — có yêu cầu UI khác (toast / inline) không?
