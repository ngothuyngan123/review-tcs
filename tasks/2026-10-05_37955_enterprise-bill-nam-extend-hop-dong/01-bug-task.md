# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine qua `/new-task 37955` (2026-10-05). File này chỉ giữ thông tin cần để viết/review TC — metadata Redmine (ngày báo cáo, priority, URL...) tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37955 — [Detail hợp đồng] Enterprise bill tháng chuyển sang bill năm sau đó extend hợp đồng => Màn detail và lịch sử đang hiện số tiền bill tháng` |
| Module / Màn hình | `Bill hợp đồng — 契約詳細 Chi tiết hợp đồng (FA-031 Contract Plan & Payment) + 決済履歴 Lịch sử thanh toán (FS-009 Payment History)` |

## Mô tả bug (bản dịch tiếng Việt)

Hợp đồng Enterprise (gói おまとめ割引 — bó nhiều khung bot) đang ở kỳ thanh toán THÁNG, được đổi sang kỳ NĂM (qua màn 「お支払い期間の変更」). Kỳ năm mới chỉ có hiệu lực từ lần thu tiền kế tiếp nên hệ thống tạm giữ kỳ cũ ở cờ `bill_type_old`. Sau đó hợp đồng được **gia hạn** (「契約期間を1年延長する」) — về nghiệp vụ đây chính là lần thu tiền theo kỳ NĂM mới. Nhưng màn 「契約詳細」 (chi tiết hợp đồng) và màn 「決済履歴」 (lịch sử thanh toán) vẫn hiện **số tiền của kỳ THÁNG** thay vì số tiền kỳ NĂM vừa thu.

Mô tả gốc trên Redmine (nguyên văn): "Expect: Hiện đúng số tiền bill năm"

## Steps to reproduce

1.
2.
3.

> ⚠️ Redmine không có section "Tái hiện bug" theo format chuẩn (Steps/Expected/Actual) — chỉ có 1 dòng mô tả kỳ vọng. Kịch bản lỗi đầy đủ được suy từ tiêu đề ticket + root cause ở `03-dev-impact.md` mục 1, KHÔNG phải steps do QA/khách hàng tái hiện tay. AI auto-fixbug cũng xác nhận **không tái hiện được bằng dữ liệu runtime** (không kết nối được DB dev), kết luận dựa trên đọc code — xem Journal #133054 bên dưới.

## Expected result

- Màn 「契約詳細」 hiện đúng **số tiền bill NĂM** (đúng theo mô tả gốc Redmine).
- (Suy từ root cause) Màn 「契約詳細」 và 「決済履歴」 phải hiện số tiền + kỳ thanh toán khớp với số tiền NĂM thực thu sau khi gia hạn, kỳ 「年間一括払い」, không còn dòng chú thích "kỳ năm chỉ áp dụng từ lần thu tới".

## Actual result

- Màn 「契約詳細」 và lịch sử (「決済履歴」) đang hiện **số tiền của kỳ THÁNG** (sai) — theo đúng tiêu đề ticket, do mọi điểm hiển thị tiền đều ưu tiên đọc cờ kỳ cũ `bill_type_old` thay vì số tiền đã thu thực tế.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- 2026_06_20_17_01_17_契約詳細.png — https://redmine.melonglobal.net/attachments/download/27280/2026_06_20_17_01_17_%E5%A5%91%E7%B4%84%E8%A9%B3%E7%B4%B0.png
- 2026_06_20_17_01_34_契約詳細.png — https://redmine.melonglobal.net/attachments/download/27281/2026_06_20_17_01_34_%E5%A5%91%E7%B4%84%E8%A9%B3%E7%B4%B0.png

## Ghi chú thêm của Leader

- Ticket liên quan: Journal #132267 (2026-08-21) tham chiếu **Feature #37085** — có thể là tính năng nền (đổi kỳ thanh toán) liên quan trực tiếp đến luồng gây bug này; Leader nên kiểm tra Feature #37085 nếu cần hiểu thêm context đổi kỳ.
- Nút 「契約期間を1年延長する」 (gia hạn) chỉ hiện khi `contract_bill_type == 'year'` — đúng khớp kịch bản ticket: phải đổi tháng→năm xong mới gia hạn được, không reproduce được nếu hợp đồng đang ở kỳ tháng gốc.
- Status Redmine hiện tại: **Fix done - Đợi test**. Branch/commit đã có sẵn (xem `03-dev-impact.md`).
- Trạng thái Dev không tái hiện bug bằng dữ liệu runtime (lỗi kết nối DB dev) — tất cả đánh giá dựa trên đọc code + đối chiếu chéo các luồng thu tiền khác. TCs nên tập trung verify cách fix bằng dữ liệu dựng tay + **Recover data** cho các hợp đồng cũ (xem mục 5 trong Journal #133054 / `03-dev-impact.md`).
- Redmine không có "Link TCs" → bộ TC gốc cho review được fetch từ **MCP LME TEST STUDIO** (task #217, 18 TC do AI sinh) — xem `04-tc-list.md`.

## Journal / note từ Redmine (nguyên văn)

**Journal #133054 — AI LME Fix bug — 2026-08-26:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi hợp đồng đổi kỳ thanh toán từ tháng sang năm, hệ thống giữ kỳ cũ ở cột bill_type_old vì kỳ năm mới chỉ có hiệu lực từ lần thu tiền kế tiếp, và mọi màn hiển thị đều ưu tiên kỳ cũ này để tính tiền. Việc gia hạn hợp đồng thực chất đã thu tiền theo kỳ năm mới, nhưng luồng xử lý gia hạn thành công là luồng thu tiền DUY NHẤT quên xoá cờ kỳ cũ và quên cập nhật số tiền đã thu vào hợp đồng, nên màn chi tiết và lịch sử vẫn hiện giá bill tháng.

■ 2. CÁCH FIX
Sửa luồng gia hạn hợp đồng thành công trong Admin/BotController: sau khi thu tiền theo kỳ mới thì xoá cờ kỳ thanh toán cũ (bill_type_old) và cập nhật số tiền đã thu (amount_payment) của hợp đồng, áp dụng cho cả nhánh thẻ tín dụng (handleExtendContractSuccess) lẫn nhánh chuyển khoản ngân hàng; đồng thời bản ghi lịch sử gia hạn nhánh chuyển khoản lấy số tiền từ bản ghi thanh toán cha thay vì đọc số tiền cũ còn lưu trong đối tượng hợp đồng chưa refresh. Quét ngang xác nhận 3 luồng thu tiền còn lại (đổi thẻ, job thu định kỳ) đã xoá cờ kỳ cũ sẵn, chỉ luồng gia hạn bỏ sót.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
BotController::handleExtendContractSuccess (app/Http/Controllers/Admin/BotController.php)
BotController::univapayCallback - nhánh gia hạn chuyển khoản (app/Http/Controllers/Admin/BotController.php)
BotController::handleCallbackChangeCardSuccess - mẫu tham chiếu đã xoá cờ đúng (app/Http/Controllers/Admin/BotController.php)
PointSettingController::extendContract (app/Http/Controllers/PointSettingController.php)
PointSettingController::changeTypePayment - nơi sinh cờ kỳ cũ (app/Http/Controllers/PointSettingController.php)
AutoPaymentJobUnivapay::chargeStripeBots / chargeUnivapayCardBots - job thu định kỳ đã xoá cờ (app/Console/Commands/AutoPaymentJobUnivapay.php)
calculateSaleEnterprise (app/Helpers/functions.php)
getAmountContract (public/_assets/modules/bill/js/detail.js)
detail.blade.php muc ご利用料金 / お支払い期間 (resources/views/basic/bill/detail.blade.php)
payment_history/index.blade.php cot so tien (resources/views/basic/payment_history/index.blade.php)
state.blade.php modal lich su hop dong (resources/views/basic/bill/modals/detail/state.blade.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/BotController.php
 • 4.2 Data ảnh hưởng:
   - bot_contracts.bill_type_old — được set NULL sau khi gia hạn thành công (trước đây giữ nguyên kỳ cũ)
   - bot_contracts.amount_payment — được cập nhật bằng số tiền thực thu của lần gia hạn (trước đây giữ số tiền của lần thu trước)
   - bot_life_cycles.data.amount — bản ghi lịch sử gia hạn nhánh chuyển khoản nay lưu số tiền thực thu
 • 4.3 Tính năng liên quan:
   - Contract Plan & Payment (FA-031) — màn chi tiết hợp đồng hiện đúng tiền và kỳ thanh toán sau khi gia hạn
   - Payment History (FS-009) — màn lịch sử thanh toán và bản ghi lịch sử gia hạn hiện đúng số tiền đã thu

■ 5. RECOVER DATA
   ⚠ CÓ — Hợp đồng đã gia hạn TRƯỚC khi fix lên release vẫn còn bill_type_old khác NULL và amount_payment là số tiền kỳ cũ, nên vẫn hiển thị sai cho tới lần thu tiền định kỳ kế tiếp (lúc đó job mới tự xoá cờ). Cần rà và sửa dữ liệu cho các hợp đồng này. (phạm vi: Lọc bot_contracts có bill_type_old khác NULL và có bản ghi payment_histories reason bắt đầu bằng pay_year_fee_extend_ (parent_month = 1) phát sinh SAU thời điểm đổi kỳ; với các hợp đồng đó set bill_type_old = NULL và amount_payment = số tiền của bản ghi gia hạn gần nhất. Worker KHÔNG tự chạy lệnh cập nhật dữ liệu — cần dev/vận hành thực hiện trên môi trường thật sau khi release.)

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Admin/BotController.php: No syntax errors detected; git diff --stat origin/release_step_20260805...ai_fixbug_37955: 1 file changed, 22 insertions(+), 2 deletions(-) — chỉ đúng file đã sửa; Không chạy PHPUnit: fix nằm ở Controller, không thuộc app/Services hay app/Helpers nên không có unit test thuần logic tương ứng
   Bằng chứng: Không kết nối được DB dev (host.docker.internal:3306 Connection refused) nên KHÔNG tái hiện được bằng dữ liệu runtime; kết luận dựa trên đọc code và đối chiếu chéo các luồng thu tiền; Nút gia hạn chỉ hiện khi contract_bill_type == 'year' (resources/views/basic/bill/detail.blade.php) — khớp đúng kịch bản ticket: đổi tháng sang năm xong mới gia hạn được; Mọi điểm hiển thị tiền đều ưu tiên kỳ cũ: detail.js getAmountContract, download_invoice.js, bill/index.blade.php, payment_history/index.blade.php đều dùng bill_type_old trước contract_bill_type; Đối chiếu: handleCallbackChangeCardSuccess và AutoPaymentJobUnivapay đều xoá bill_type_old khi thu tiền theo kỳ mới; chỉ luồng gia hạn thiếu; amount_payment được cập nhật ở tất cả handler thanh toán khác (thu định kỳ, thu lại, đổi thẻ) — riêng gia hạn không cập nhật nên bản ghi lịch sử gia hạn snapshot lại số tiền cũ

■ TỰ REVIEW (AI)
Fix tối giản, tự chứa trên release: chỉ thêm 2 cột vào các lệnh cập nhật hợp đồng sẵn có ở 2 nhánh gia hạn (thẻ và chuyển khoản) và sửa 1 chỗ đọc số tiền cũ khi ghi lịch sử. Không đổi công thức tính tiền, không đổi giao diện, không thêm lời gọi API. Ngữ nghĩa xoá cờ kỳ cũ được xác nhận bằng 3 luồng thu tiền khác trong hệ thống vốn đã làm đúng như vậy.
 • Rủi ro / lưu ý khi test:
   - Sau fix, ngay khi gia hạn xong màn chi tiết sẽ chuyển sang hiển thị kỳ năm và giá năm, mất dòng ghi chú kỳ mới sẽ áp dụng từ lần thu kế tiếp — đây là hiển thị đúng theo thực tế đã thu tiền, nhưng QA nên xác nhận lại kỳ vọng nghiệp vụ
   - Ở nhánh chuyển khoản, số tiền lấy từ bản ghi thanh toán cha (parent_month = 1) theo mã giao dịch; nếu dữ liệu cũ thiếu bản ghi cha thì rơi về bản ghi tìm được ban đầu như hành vi cũ
   - Hợp đồng đã gia hạn trước khi release fix vẫn hiển thị sai cho tới lần thu tiền kế tiếp — xem mục cần recover dữ liệu

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_37955 (nhánh gốc release_step_20260805, commit c20fe4780d, 1 file) [đã push]
```
