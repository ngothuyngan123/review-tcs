# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40049 — [Job bill tiền tool] Sau khi job bill false => Bill lại success thì bị update datetime_first_payment làm hiển thị sai ngày thanh toán lần đầu` |
| Module / Màn hình | Contract Plan & Payment (FA-031) — bill tool / màn hợp đồng (hiển thị "Ngày bắt đầu thanh toán"); job bill tiền tự động (`AutoPaymentJobUnivapay`) + nút Bill lại (`PointSettingController`) |

## Mô tả bug (bản dịch tiếng Việt)

Nội dung report gốc (đã là tiếng Việt, giữ nguyên văn):

Hiện tượng: Sau khi job bill false => Bill lại success thì bị update `datetime_first_payment` làm hiển thị sai ngày thanh toán lần đầu.

Expect: Ngày thanh toán lần đầu chỉ update khi mua mới hợp đồng / hợp đồng lại.

**Diễn giải chi tiết (theo Journal #132021 — AI LME Fix bug):** Luồng thu tiền hợp đồng có một đoạn: nếu hợp đồng đã quá hạn hơn 7 ngày thì ghi đè `datetime_first_payment` thành ngày hiện tại. Khi bill lỗi rồi bill lại thành công vài ngày sau, hợp đồng rơi đúng vào nhánh này nên ngày thanh toán lần đầu bị nhảy sang ngày bill lại. Cột này dùng để hiển thị "Ngày bắt đầu thanh toán" trên màn hợp đồng và để đếm hợp đồng trả phí mới trong thống kê doanh thu năm, nên bị sai theo.

## Steps to reproduce

<!-- Redmine không có Section "Tái hiện bug" dạng step-by-step — tracker "Bug tự detect", report chỉ gồm ca lỗi cụ thể (account/contract_id/bot_id, xem "Dữ liệu định danh ca lỗi") + Hiện tượng/Expect. -->

## Expected result

- Ngày thanh toán lần đầu (`datetime_first_payment`) chỉ update khi **mua mới hợp đồng** hoặc **ký lại hợp đồng** (hợp đồng đã hết hạn/hủy, ký lại). KHÔNG update khi bill lại (job bill tiền chạy lỗi → bill lại thành công) của hợp đồng đang chạy bình thường.

## Actual result

- Sau khi job bill tiền tự động chạy lỗi (false) rồi hợp đồng được **bill lại thành công**, `datetime_first_payment` bị ghi đè sang ngày bill lại → hiển thị sai "Ngày bắt đầu thanh toán" trên màn hợp đồng, và làm lệch số liệu hợp đồng trả phí mới trong thống kê doanh thu năm.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- `bill-tool-1.png` — https://redmine.watermelon.vn/attachments/download/29208/bill-tool-1.png

## Ghi chú thêm của Leader

- ⚠️ **Bug không có Section "Tái hiện bug" dạng step-by-step** (tracker `Bug tự detect`) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** + **regression impact**, không cần tái hiện y nguyên ca lỗi gốc.
- ⚠️ **RULE-08 — bill tiền**: đây là tính năng thanh toán thật (job tự động + nút Bill lại + callback cổng thanh toán). Dev tự nhận **không tái hiện được trên dev** (không kết nối MySQL dev, không được gọi cổng thanh toán thật) — verify mức lint only. QA cần chuẩn bị mẫu verify ở môi trường có thể trigger thật (staging/product tuỳ khả năng dựng thẻ lỗi).
- ⚠️ **Data cũ đã bị ghi sai trước fix vẫn còn sai** — cần recover thủ công theo hướng dẫn ở file 03 (mục "Ghi chú thêm — Recover data"). Hợp đồng `74140` đã được chị Ngần recover `datetime_first_payment` về `2026-05-08 07:18` (Journal #130700).
- ⚠️ **Hệ quả cần PM xác nhận** (Dev tự nêu, chưa fix trong ticket này): sau khi hồi phục một hợp đồng quá hạn trên 7 ngày, kỳ thu tiền **kế tiếp** sẽ quay về đúng ngày thu tiền của hợp đồng gốc → kỳ đó **ngắn hơn 1 tháng** (khách trả trọn tháng cho một kỳ ngắn hơn). Trước đây ngày thu tiền bị dời hẳn sang ngày bill lại. Đây là hệ quả trực tiếp của việc giữ nguyên ngày thanh toán lần đầu.
- ⚠️ **Refix vòng 2 (Univapay card)** — nhánh ký lại hợp đồng của thẻ Univapay giờ đọc trạng thái hợp đồng **TRƯỚC khi tạo giao dịch**, gửi kèm cờ "ký lại hợp đồng" qua `metadata` giao dịch; handler nhận kết quả thanh toán đọc cờ này để quyết định có đặt lại `datetime_first_payment` hay không. Phụ thuộc việc cổng thanh toán trả lại nguyên `metadata` trong webhook (rủi ro thấp — các trường metadata khác như `actionBill`, `botContractId` đã hoạt động theo cùng cơ chế).
- ⚠️ **Tác dụng phụ của fix (thẻ Stripe)**: Dev sửa lỗi gõ sai tên cột trạng thái trong hàm thu tiền thẻ Stripe → nhánh ký lại hợp đồng **CHẠY THẬT LẦN ĐẦU** (trước đây luôn rơi vào nhánh else do lỗi gõ sai). Cần test kỹ nhánh ký lại hợp đồng của Stripe.
- 3 phương thức thanh toán liên quan đến fix: **thẻ Stripe**, **thẻ Univapay**, **chuyển khoản Univapay** (transfer).
- Branch fix: `ai_fixbug_40049` (nhánh gốc `release_step_20260805`, commit `53b9fafc9f`, 4 file) — đã push lên `sns-line`.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `146045` |
| Account (user) | `company@globalvogue.cloud` |
| contract_id | `74140` (`bot_contracts.id`) |
| Đối tượng cấu hình | `bot_contracts.datetime_first_payment` của hợp đồng `74140` — bị ghi đè sai; đã recover về `2026-05-08 07:18` (Journal #130700) |
| Thời điểm lỗi | `<không ghi rõ trong Redmine>` |
| Đối chứng | `<chưa có — Dev không tái hiện được trên dev (không kết nối MySQL dev + không gọi cổng thanh toán thật)>` |

## Journal / note từ Redmine (nguyên văn)

**Journal #130700 — Ngô Thúy Ngần — 2026-08-20:**

```
Hiện tại Ngần đã recover datetime_first_payment  của hợp đồng này về 2026-05-08 7:18
```

**Journal #132021 — AI LME Fix bug — 2026-08-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Luồng thu tiền hợp đồng có một đoạn: nếu hợp đồng đã quá hạn hơn 7 ngày thì ghi đè ngày thanh toán lần đầu thành ngày hiện tại. Khi bill lỗi rồi bill lại thành công vài ngày sau, hợp đồng rơi đúng vào nhánh này nên ngày thanh toán lần đầu bị nhảy sang ngày bill lại. Đây là cột dùng để hiển thị Ngày bắt đầu thanh toán trên màn hợp đồng và để đếm hợp đồng trả phí mới trong thống kê doanh thu năm, nên bị sai theo.

■ 2. CÁCH FIX
Sửa tiếp theo AI review vòng 2: thống nhất hành vi ký lại hợp đồng (nút Huỷ yêu cầu huỷ khi hợp đồng đã hết hạn) cho cả 3 phương thức thanh toán. Luồng thẻ Univapay ghi dữ liệu ở handler nhận kết quả thanh toán, nơi đó không còn đọc được trạng thái đã huỷ (trạng thái bị đặt lại thành đang hợp đồng ngay sau khi tạo giao dịch), nên trước đây nó chỉ vô tình đặt lại ngày thanh toán lần đầu nhờ đoạn ghi đè quá hạn vừa bị bỏ. Nay hàm thu tiền thẻ Univapay đọc trạng thái TRƯỚC khi tạo giao dịch rồi gửi kèm cờ ký lại hợp đồng trong metadata; handler đọc cờ này: có cờ thì đặt lại ngày thanh toán lần đầu = hôm nay và tính chu kỳ mới từ hôm nay (giống nhánh ký lại của thẻ Stripe và chuyển khoản), không có cờ (bill lại hợp đồng đang chạy) thì giữ nguyên ngày cũ như vòng trước. Bổ sung khai báo cờ mới vào danh sách trường metadata gửi sang cổng thanh toán vì danh sách này cố định, không khai thì trường bị bỏ.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
AutoPaymentJobUnivapay::chargeStripeBots (app/Console/Commands/AutoPaymentJobUnivapay.php)
AutoPaymentJobUnivapay::chargeUnivapayCardBots (app/Console/Commands/AutoPaymentJobUnivapay.php)
AutoPaymentJobUnivapay::chargeUnivapayTransferBots (app/Console/Commands/AutoPaymentJobUnivapay.php)
AutoPaymentJobUnivapay::calculateNextExpiredDateRetry (app/Console/Commands/AutoPaymentJobUnivapay.php)
PointSettingController::billStripeContract (app/Http/Controllers/PointSettingController.php)
PointSettingController::billTransferUnivapayContract (app/Http/Controllers/PointSettingController.php)
PointSettingController::billCardUnivapayContract (app/Http/Controllers/PointSettingController.php)
PointSettingController::billAgainContract (app/Http/Controllers/PointSettingController.php)
PointSettingController::changeStatusContract (app/Http/Controllers/PointSettingController.php)
PointSettingController::changeCard (app/Http/Controllers/PointSettingController.php)
PointSettingController::reContractChangeCard (app/Http/Controllers/PointSettingController.php)
PointSettingController::calculateNextExpiredDate / calculateNextExpiredYear (app/Http/Controllers/PointSettingController.php)
BillingService::nextExpiredDate / nextExpiredDateByYear (app/Services/BillingService.php)
BotController::handleCallbackBillJob (app/Http/Controllers/Admin/BotController.php)
BotController::paymentBotSlot / paymentBotSlotV2 (app/Http/Controllers/Admin/BotController.php)
AnnualStatisticsService::computePaidContracts (app/Services/AnnualStatisticsService.php)
ExportBotStaffHistoryCsv::handle (app/Console/Commands/ExportBotStaffHistoryCsv.php)
resources/views/basic/bill/detail.blade.php (dòng hiển thị Ngày bắt đầu thanh toán)
resources/views/basic/bill/detail-bill-fail.blade.php (dòng hiển thị Ngày bắt đầu thanh toán)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Console/Commands/AutoPaymentJobUnivapay.php
   - app/Http/Controllers/PointSettingController.php
 • 4.2 Data ảnh hưởng:
   - bot_contracts.datetime_first_payment — từ nay job thu tiền và nút Bill lại ghi lại đúng giá trị cũ (không đổi giá trị); chỉ mua mới hợp đồng / ký lại hợp đồng mới đặt ngày mới
   - bot_contracts.expired_date_contract — KHÔNG đổi cách tính ở lần thu tiền hiện tại; nhưng từ kỳ kế tiếp, hợp đồng vừa hồi phục sau khi quá hạn trên 7 ngày sẽ quay về đúng ngày thu tiền của hợp đồng gốc (một kỳ ngắn hơn một tháng), thay vì neo theo ngày bill lại như trước
   - annual_revenue_statistics.paid_contracts — đếm hợp đồng trả phí mới theo datetime_first_payment nên hết bị đếm nhầm hợp đồng cũ thành hợp đồng mới
 • 4.3 Tính năng liên quan:
   - Contract Plan & Payment (FA-031) — màn hợp đồng và thanh toán: Ngày bắt đầu thanh toán hiển thị đúng ngày mua hợp đồng ban đầu; job thu tiền định kỳ và nút Bill lại không ghi đè nữa
   - Payment History (FS-009) — dữ liệu lịch sử thanh toán không đổi, nhưng ngày thu tiền của các kỳ kế tiếp sau khi hồi phục hợp đồng quá hạn sẽ bám ngày hợp đồng gốc
   - Annual Revenue Statistics (outside glossary) — thống kê số hợp đồng trả phí mới theo năm dựa trên ngày thanh toán lần đầu nên không còn bị lệch
   - User / Account List (FS-003) — file xuất lịch sử nhân viên theo bot lấy ngày hợp đồng từ cột này nên cũng hết sai

■ 5. RECOVER DATA
   ⚠ CÓ — Fix chỉ chặn từ thời điểm release trở đi. Các hợp đồng đã bị ghi đè trước đó vẫn đang mang ngày thanh toán lần đầu sai và cần recover thủ công (hợp đồng 74140 đã được chị Ngần recover về 2026-05-08 07:18). Cách dò: các hợp đồng từng có lần thu tiền lỗi rồi thành công (payment_histories / bot_life_cycles có bản ghi lỗi thanh toán) mà datetime_first_payment lớn hơn ngày tạo hợp đồng date_add_contract một cách bất thường; đối chiếu với bản ghi thanh toán đầu tiên trong payment_histories để lấy lại ngày đúng. (phạm vi: bảng bot_contracts (cột datetime_first_payment) của các hợp đồng trả phí từng bill lỗi rồi bill lại thành công sau khi quá hạn trên 7 ngày; kéo theo phải chạy lại thống kê hợp đồng trả phí mới theo năm (annual_revenue_statistics) nếu số liệu đã bị lệch.)

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Console/Commands/AutoPaymentJobUnivapay.php: No syntax errors detected; php -l app/Http/Controllers/PointSettingController.php: No syntax errors detected; git diff --stat release_step_20260805...ai_fixbug_40049: đúng 2 file, 21 thêm / 19 bớt; Không chạy PHPUnit: code sửa nằm trong Command và Controller phụ thuộc DB + cổng thanh toán, không thuộc app/Services hay app/Helpers
   Bằng chứng: Không kết nối được MySQL dev (host.docker.internal:3306 Connection refused) nên không dump được dữ liệu hợp đồng 74140 để đối chiếu; kết luận dựa trên đọc code 3 luồng job + 3 hàm bill lại; Không fetch được origin (thiếu secret Bitbucket trong phiên này) — làm việc trên bản release local release_step_20260805 tại commit 8b64f07bfa; BillingService::nextExpiredDate và PointSettingController::calculateNextExpiredDate đã tự có guard quá hạn 7 ngày riêng, nên bỏ đoạn ghi đè không làm đổi ngày hết hạn của chính lần thu tiền này

■ TỰ REVIEW (AI)
Diff bỏ đoạn ghi đè ngày thanh toán lần đầu ở 6 luồng thu tiền lại của hợp đồng đang chạy (job thu tiền tự động + nút Bill lại + 2 handler nhận kết quả thanh toán Univapay), không đụng số tiền, không đụng cách gọi cổng thanh toán, không đụng cách tính ngày hết hạn của chính lần thu tiền đó (cả BillingService lẫn calculateNextExpiredDate đều đã có guard quá hạn 7 ngày riêng). Nhánh ký lại hợp đồng (trạng thái đã huỷ) vẫn đặt ngày mới đúng như mong đợi của ticket cho cả 3 phương thức: thẻ Stripe phải sửa lỗi gõ sai tên cột trạng thái thì nhánh này mới chạy; thẻ Univapay ghi dữ liệu ở handler nhận kết quả thanh toán (nơi không còn đọc được trạng thái đã huỷ) nên được truyền cờ ký lại hợp đồng qua metadata của giao dịch (refix vòng 2).
 • Rủi ro / lưu ý khi test:
   - Hệ quả cần PM xác nhận: sau khi hồi phục một hợp đồng quá hạn trên 7 ngày, kỳ thu tiền KẾ TIẾP sẽ quay về đúng ngày thu tiền của hợp đồng gốc nên kỳ đó ngắn hơn một tháng (khách trả trọn tháng cho một kỳ ngắn). Trước đây ngày thu tiền bị dời hẳn sang ngày bill lại. Đây là hệ quả trực tiếp của yêu cầu giữ nguyên ngày thanh toán lần đầu, vì cột này đang đóng luôn vai trò mốc neo ngày thu tiền. Nếu muốn giữ cả hai (hiển thị đúng và chu kỳ tròn tháng) thì phải tách mốc neo ra một cột riêng — việc này cần thêm migration nên chưa làm trong ticket.
   - Sửa lỗi gõ sai tên cột trạng thái trong hàm thu tiền thẻ Stripe làm nhánh ký lại hợp đồng chạy thật (trước đây luôn rơi vào nhánh else). Đã đối chiếu: ngày hết hạn tính ra bằng nhau ở cả hai nhánh cho hợp đồng đã huỷ (đều là hôm nay cộng một chu kỳ), nên chỉ khác ở chỗ ngày thanh toán lần đầu được đặt lại đúng như mong đợi.
   - Không tái hiện được trên môi trường dev (không kết nối được MySQL dev, và không được phép gọi cổng thanh toán thật) — cần QA verify trên môi trường test với thẻ lỗi.
   - Các hợp đồng đã bị ghi sai trước đây vẫn sai cho tới khi recover dữ liệu.
   - Ghi chú phạm vi (theo AI review vòng 1): trong hàm thu tiền thẻ Univapay của nút Bill lại (PointSettingController::billCardUnivapayContract), cả hai nhánh sau khi tạo giao dịch đều thoát sớm nên đoạn cập nhật ngày thanh toán lần đầu phía dưới là CODE CHẾT — sửa ở đó không có tác dụng lúc chạy thật. Điểm ghi thật của luồng thẻ Univapay nằm ở handler nhận kết quả thanh toán (BotController::handleCallbackBillAgainCardSuccess và handleCallbackBillJob) và đã được sửa. Không dọn code chết trong ticket này vì ngoài phạm vi.
   - Refix vòng 2 — điểm cần QA chú ý: cờ ký lại hợp đồng đi qua metadata của giao dịch Univapay, tức phụ thuộc việc cổng thanh toán trả lại nguyên metadata trong webhook (các trường metadata khác như actionBill, botContractId đã hoạt động theo đúng cơ chế này nên rủi ro thấp). Giao dịch tạo TRƯỚC khi deploy không có trường này thì handler rơi vào nhánh giữ nguyên ngày cũ — an toàn, không ghi sai. Ngoài ra ngày hết hạn khi ký lại của luồng thẻ Univapay tính bằng BillingService (chuẩn mới, hết hạn = trước ngày cùng kỳ tháng sau 1 ngày) trong khi thẻ Stripe / chuyển khoản dùng hàm cũ calculateNextExpired* (đúng ngày cùng kỳ tháng sau) — lệch 1 ngày là khác biệt SẴN CÓ giữa hai bộ hàm của 2 file, không phát sinh từ fix này; thống nhất 2 bộ hàm là việc riêng, ngoài phạm vi ticket.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_40049 (nhánh gốc release_step_20260805, commit 53b9fafc9f, 4 file)  [đã push]
```
