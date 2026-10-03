# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #40049 (journal "AI LME Fix bug" #132021, 2026-08-21) bởi `/new-task` ngày 2026-09-29. **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Ngô Thúy Ngần` (assigned_to) / AI LME Fix bug (auto-fixbug) |
| Commit / Pull Request | `sns-line` commit `53b9fafc9f` (theo mục BRANCH/COMMIT — 4 file) — **mâu thuẫn với mục VERIFY** ghi `git diff --stat ... : đúng 2 file` — xem ⚠️ ở "Ghi chú thêm" |
| Branch | `ai_fixbug_40049` (nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | `2026-08-21` (Journal #132021) |
| Auto-filled | `2026-09-29 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Luồng thu tiền hợp đồng có một đoạn: nếu hợp đồng đã quá hạn hơn 7 ngày thì ghi đè ngày thanh toán lần đầu (`datetime_first_payment`) thành ngày hiện tại. Khi bill lỗi rồi bill lại thành công vài ngày sau, hợp đồng rơi đúng vào nhánh này nên ngày thanh toán lần đầu bị nhảy sang ngày bill lại. Đây là cột dùng để hiển thị "Ngày bắt đầu thanh toán" trên màn hợp đồng và để đếm hợp đồng trả phí mới trong thống kê doanh thu năm, nên bị sai theo.

## 2. Cách fix

Sửa tiếp theo AI review vòng 2: thống nhất hành vi **ký lại hợp đồng** (khi hợp đồng đã hết hạn/bị huỷ, nay bill lại thành công) cho cả 3 phương thức thanh toán (Stripe / Univapay card / Univapay chuyển khoản):

- Bỏ đoạn ghi đè `datetime_first_payment` khi hợp đồng quá hạn >7 ngày (nguyên nhân gốc), áp dụng cho cả job thu tiền tự động và nút "Bill lại".
- Luồng thẻ **Univapay** ghi dữ liệu ở handler nhận kết quả thanh toán, nơi không còn đọc được trạng thái đã huỷ (trạng thái bị đặt lại thành "đang hợp đồng" ngay sau khi tạo giao dịch). Nay hàm thu tiền thẻ Univapay đọc trạng thái **TRƯỚC khi tạo giao dịch**, gửi kèm cờ "ký lại hợp đồng" trong `metadata` giao dịch; handler đọc cờ này: có cờ → đặt lại `datetime_first_payment` = hôm nay + tính chu kỳ mới từ hôm nay (giống nhánh ký lại của thẻ Stripe/chuyển khoản); không có cờ (bill lại hợp đồng đang chạy) → giữ nguyên ngày cũ.
- Bổ sung khai báo cờ mới vào danh sách trường metadata gửi sang cổng thanh toán (danh sách cố định, không khai báo thì trường bị bỏ).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê nguyên văn 18 function ở Journal #132021 mục ■3, KHÔNG phân biệt rõ hàm nào sửa trực tiếp vs chỉ check. Cột "Thay đổi" dưới đây suy từ mục 4.1 (chỉ 2 file AutoPaymentJobUnivapay.php + PointSettingController.php được khai là "file thay đổi"). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AutoPaymentJobUnivapay::chargeStripeBots` / `::chargeUnivapayCardBots` / `::chargeUnivapayTransferBots` — `app/Console/Commands/AutoPaymentJobUnivapay.php` | Bỏ đoạn ghi đè `datetime_first_payment` khi quá hạn >7 ngày | 3 luồng job thu tiền tự động (job bill định kỳ), cùng thuộc file thay đổi |
| 2 | `AutoPaymentJobUnivapay::calculateNextExpiredDateRetry` — cùng file | Đã check | Liệt kê trong ■3 nhưng không có mô tả thay đổi riêng |
| 3 | `PointSettingController::billStripeContract` / `::billTransferUnivapayContract` / `::billCardUnivapayContract` / `::billAgainContract` — `app/Http/Controllers/PointSettingController.php` | Bỏ đoạn ghi đè `datetime_first_payment` khi quá hạn >7 ngày; riêng `billStripeContract` còn sửa lỗi gõ sai tên cột trạng thái để nhánh ký lại hợp đồng chạy đúng | Nút "Bill lại" — 4 hàm theo phương thức thanh toán, cùng thuộc file thay đổi |
| 4 | `PointSettingController::changeStatusContract` / `::changeCard` / `::reContractChangeCard` | Đã check | Liệt kê trong ■3 (luồng đổi trạng thái / đổi thẻ hợp đồng) |
| 5 | `PointSettingController::calculateNextExpiredDate` / `::calculateNextExpiredYear` | Không sửa — đã có guard quá hạn 7 ngày riêng | Dev xác nhận không làm đổi ngày hết hạn của chính lần thu tiền hiện tại |
| 6 | `BillingService::nextExpiredDate` / `::nextExpiredDateByYear` — `app/Services/BillingService.php` | Không sửa — đã có guard quá hạn 7 ngày riêng | Đã check, tương tự #5 |
| 7 | `BotController::handleCallbackBillJob` — `app/Http/Controllers/Admin/BotController.php` | ⚠️ Nghi có sửa (mục 2 + TỰ REVIEW nhắc "2 handler nhận kết quả thanh toán Univapay" được sửa để đọc cờ ký lại hợp đồng) nhưng **KHÔNG** có trong ■4.1 "File thay đổi" | Mâu thuẫn nội dung journal — xem ⚠️ ở "Ghi chú thêm" |
| 8 | `BotController::paymentBotSlot` / `::paymentBotSlotV2` | Đã check | Liệt kê trong ■3 |
| 9 | `AnnualStatisticsService::computePaidContracts` — `app/Services/AnnualStatisticsService.php` | Không sửa (hưởng theo fix) | Đếm hợp đồng trả phí mới theo `datetime_first_payment` |
| 10 | `ExportBotStaffHistoryCsv::handle` — `app/Console/Commands/ExportBotStaffHistoryCsv.php` | Không sửa (hưởng theo fix) | File xuất lịch sử nhân viên theo bot lấy ngày hợp đồng từ cột này |
| 11 | `resources/views/basic/bill/detail.blade.php` / `detail-bill-fail.blade.php` | Không sửa | Dòng hiển thị "Ngày bắt đầu thanh toán" — chỉ hưởng data đúng hơn, không đổi logic hiển thị |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `chargeStripeBots` / `chargeUnivapayCardBots` / `chargeUnivapayTransferBots` | `app/Console/Commands/AutoPaymentJobUnivapay.php` | Direct | Job thu tiền tự động (3 phương thức) — bỏ đoạn ghi đè `datetime_first_payment` khi quá hạn >7 ngày |
| F2 | `billStripeContract` / `billTransferUnivapayContract` / `billCardUnivapayContract` / `billAgainContract` | `app/Http/Controllers/PointSettingController.php` | Direct | Nút "Bill lại" (3 phương thức); `billStripeContract` còn sửa lỗi gõ sai tên cột trạng thái |
| F3 | Handler nhận kết quả thanh toán Univapay (`handleCallbackBillJob` và tương tự — theo mục 2/TỰ REVIEW) | `app/Http/Controllers/Admin/BotController.php` (suy đoán từ ■3) | Direct (⚠️ chưa xác nhận — không có trong ■4.1 File thay đổi gốc) | Đọc cờ "ký lại hợp đồng" từ `metadata` giao dịch (refix vòng 2) — **cần hỏi lại Dev xác nhận file/hàm cụ thể** |
| F4 | `calculateNextExpiredDate` / `calculateNextExpiredYear` (PointSettingController) + `nextExpiredDate` / `nextExpiredDateByYear` (BillingService) | `PointSettingController.php` / `BillingService.php` | Indirect | Đã check, có guard quá hạn 7 ngày RIÊNG — không đổi cách tính hạn của lần thu tiền hiện tại |
| F5 | `computePaidContracts` | `app/Services/AnnualStatisticsService.php` | Indirect | Đếm hợp đồng trả phí mới theo `datetime_first_payment`, hết đếm nhầm hợp đồng cũ thành mới |
| F6 | `ExportBotStaffHistoryCsv::handle` | `app/Console/Commands/ExportBotStaffHistoryCsv.php` | Indirect | File xuất lịch sử nhân viên theo bot — lấy ngày hợp đồng từ cột bị sửa |
| F7 | View hiển thị "Ngày bắt đầu thanh toán" | `resources/views/basic/bill/detail.blade.php`, `detail-bill-fail.blade.php` | Indirect (display only) | Không đổi logic hiển thị, chỉ hưởng data đúng hơn |

### 4.2. List data bị update khi fix bug

> **Không thêm/sửa/xoá column nào.** Thay đổi là **giá trị được ghi** khi hợp đồng bị bill lỗi rồi bill lại thành công (quá hạn >7 ngày).

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_contracts.datetime_first_payment` | UPDATE (thay đổi hành vi ghi) | Job bill lại + nút "Bill lại" của hợp đồng **đang chạy** (chưa huỷ/chưa hết hạn) KHÔNG ghi đè nữa — giữ giá trị cũ. Chỉ **mua mới hợp đồng** hoặc **ký lại hợp đồng** (đã huỷ/hết hạn) mới đặt ngày mới = hôm nay |
| D2 | `bot_contracts.expired_date_contract` | Không đổi cách tính ở **lần thu tiền hiện tại** | Từ **kỳ kế tiếp**, hợp đồng vừa hồi phục sau khi quá hạn >7 ngày sẽ quay về đúng ngày thu tiền của hợp đồng gốc (một kỳ ngắn hơn 1 tháng), thay vì neo theo ngày bill lại như trước — **PM cần confirm trade-off này** |
| D3 | `annual_revenue_statistics.paid_contracts` | Hưởng theo D1 | Đếm hợp đồng trả phí mới theo `datetime_first_payment` — hết bị đếm nhầm hợp đồng cũ thành hợp đồng mới |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Contract Plan & Payment (FA-031) — màn hợp đồng: "Ngày bắt đầu thanh toán" hiển thị đúng ngày mua hợp đồng ban đầu; job thu tiền định kỳ và nút "Bill lại" không ghi đè nữa | F1, F2, D1 | High |
| T2 | Ký lại hợp đồng (hợp đồng đã huỷ/hết hạn, bill lại) — cả 3 phương thức Stripe / Univapay card / Univapay chuyển khoản | F2, F3, D1 | High |
| T3 | Payment History (FS-009) | D2 | Medium — dữ liệu lịch sử thanh toán không đổi, nhưng ngày thu tiền của kỳ kế tiếp sau khi hồi phục hợp đồng quá hạn sẽ bám ngày hợp đồng gốc |
| T4 | Annual Revenue Statistics (outside glossary) | F5, D3 | Medium |
| T5 | User / Account List (FS-003) — export lịch sử nhân viên theo bot | F6, D1 | Low |

---

## Ghi chú thêm (từ Dev)

- **5. Recover data:** ⚠ **CÓ** — Fix chỉ chặn từ thời điểm release trở đi. Các hợp đồng đã bị ghi đè trước đó vẫn đang mang `datetime_first_payment` sai và cần recover thủ công (hợp đồng `74140` đã được chị Ngần recover về `2026-05-08 07:18`). Cách dò: các hợp đồng từng có lần thu tiền lỗi rồi thành công (`payment_histories` / `bot_life_cycles` có bản ghi lỗi thanh toán) mà `datetime_first_payment` lớn hơn `date_add_contract` một cách bất thường; đối chiếu với bản ghi thanh toán đầu tiên trong `payment_histories` để lấy lại ngày đúng. Phạm vi: `bot_contracts.datetime_first_payment` của các hợp đồng trả phí từng bill lỗi rồi bill lại thành công sau khi quá hạn >7 ngày; kéo theo phải chạy lại `annual_revenue_statistics` nếu số liệu đã bị lệch.
- **6. Verify (mức Dev đã làm):** Mức **lint only** — `php -l` 2 file sửa: không lỗi syntax; `git diff --stat release_step_20260805...ai_fixbug_40049`: đúng **2 file**, 21 thêm / 19 bớt. **Không chạy PHPUnit** (code nằm trong Command + Controller phụ thuộc DB + cổng thanh toán, không thuộc `app/Services`/`app/Helpers`). Bằng chứng: không kết nối được MySQL dev nên không dump được data hợp đồng 74140 để đối chiếu; kết luận dựa trên đọc code 3 luồng job + 3 hàm bill lại; không fetch được origin (thiếu secret Bitbucket) — làm việc trên bản release local `release_step_20260805` tại commit `8b64f07bfa`.
- ⚠️ **Mâu thuẫn cần hỏi lại Dev trước khi chốt coverage (BƯỚC 2 review)**: mục ■4.1 "File thay đổi" chỉ khai **2 file** (`AutoPaymentJobUnivapay.php`, `PointSettingController.php`) và mục ■6 VERIFY xác nhận `git diff --stat` cũng ra **2 file**; nhưng mục BRANCH/COMMIT ghi commit có **4 file**, và mục ■2 (Cách fix) + TỰ REVIEW mô tả rõ **2 handler nhận kết quả thanh toán Univapay** (`BotController`) cũng được sửa để đọc cờ "ký lại hợp đồng" từ metadata (refix vòng 2). Nghi ngờ ■4.1 chưa được cập nhật sau refix vòng 2 → **danh sách file/function thay đổi ở trên có thể THIẾU** `BotController.php` (và 1 file khác chưa rõ). Cần Dev xác nhận lại đủ 4 file trước khi chốt diff code impact.
- **Hệ quả cần PM xác nhận** (chưa fix trong ticket này): sau khi hồi phục một hợp đồng quá hạn >7 ngày, kỳ thu tiền **kế tiếp** sẽ ngắn hơn 1 tháng (quay về đúng ngày thu tiền gốc) do cột `datetime_first_payment` đang đóng luôn vai trò mốc neo ngày thu tiền. Muốn giữ cả hai (hiển thị đúng + chu kỳ tròn tháng) cần tách mốc neo ra cột riêng — cần migration, ngoài phạm vi ticket.
- **Tác dụng phụ của fix (Stripe)**: sửa lỗi gõ sai tên cột trạng thái trong hàm thu tiền thẻ Stripe khiến nhánh **ký lại hợp đồng chạy thật lần đầu** (trước đây luôn rơi vào nhánh else). Dev đã đối chiếu: ngày hết hạn tính ra bằng nhau ở cả hai nhánh cho hợp đồng đã huỷ, chỉ khác ở chỗ `datetime_first_payment` được đặt lại đúng như mong đợi.
- **Code chết (không dọn trong ticket này)**: trong `PointSettingController::billCardUnivapayContract` (nút "Bill lại" của Univapay card), cả hai nhánh sau khi tạo giao dịch đều thoát sớm nên đoạn cập nhật `datetime_first_payment` phía dưới là **code chết** — sửa ở đó không có tác dụng lúc chạy thật. Điểm ghi thật nằm ở handler nhận kết quả thanh toán (`BotController::handleCallbackBillAgainCardSuccess`, `handleCallbackBillJob`).
- **Refix vòng 2 — rủi ro cần QA chú ý**: cờ "ký lại hợp đồng" đi qua `metadata` của giao dịch Univapay → phụ thuộc cổng thanh toán trả lại nguyên metadata trong webhook (rủi ro thấp — các trường metadata khác như `actionBill`, `botContractId` đã hoạt động theo cùng cơ chế). Giao dịch tạo **trước khi deploy** không có trường này → handler rơi vào nhánh giữ nguyên ngày cũ (an toàn, không ghi sai). Ngày hết hạn khi ký lại của luồng Univapay tính bằng `BillingService` (hết hạn = trước ngày cùng kỳ tháng sau 1 ngày) trong khi Stripe/chuyển khoản dùng `calculateNextExpired*` cũ (đúng ngày cùng kỳ tháng sau) — lệch 1 ngày là khác biệt **sẵn có** giữa 2 bộ hàm, không phát sinh từ fix này, ngoài phạm vi ticket.
- Không tái hiện được trên môi trường dev (không kết nối MySQL dev + không được gọi cổng thanh toán thật) — QA cần verify trên môi trường test được với thẻ lỗi (RULE-08 — bill tiền).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **đặc biệt xác nhận lại ⚠️ mâu thuẫn 2 file vs 4 file ở "Ghi chú thêm"**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
