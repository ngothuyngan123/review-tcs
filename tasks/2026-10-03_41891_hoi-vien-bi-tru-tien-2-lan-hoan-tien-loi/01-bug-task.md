# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41891 — [02-10-2026][T12304][Item] Hội viên bị trừ tiền thẻ 2 lần (6,980円, 9/25 và 9/26) nhưng lịch sử thanh toán chỉ có 1 bản ghi, và hoàn tiền từ màn hình lịch sử thanh toán báo lỗi 「キャンセル失敗しました」.` |
| Module / Màn hình | `Bán sản phẩm (商品販売) — Product Sales / Recurring Item (FA-026): thu tiền định kỳ UnivaPay, đổi thẻ UnivaPay/Stripe, job recover giao dịch treo, màn lịch sử thanh toán (決済履歴) + hoàn tiền (返金)` |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Nội dung dưới đây lấy nguyên văn từ issue.description (phần tiếng Việt khách hàng/CS đã viết sẵn), KHÔNG chép khối 原文 (JP). -->

WSSJ ĐÃ TẠO TICKET SLACK

User: tomohiro.hirai92+lme2@gmail.com
Bot Name: バリューオブスピーカー

Liên hệ về thao tác 「hoàn tiền (返金)」 của chức năng Sản phẩm・Thanh toán và về bản ghi thanh toán.

【Tình trạng】
Hội viên (寺岡拓海様) phản ánh sao kê thẻ tín dụng của chính họ bị thanh toán 2 lần.
Thực tế, chúng tôi đã xác nhận trên sao kê thẻ, 「バリユーオブスピー」6,980円 bị trừ 2 ngày liên tiếp 2026/9/25・9/26.

Trong khi đó, trên màn hình quản lý của Elme (lịch sử thanh toán), thanh toán của hội viên này chỉ ghi nhận 1 giao dịch ngày 2026/09/26 (số thanh toán 411193・6,980円), không thấy bản ghi của 2 giao dịch.

Ngoài ra, với hội viên này có dấu vết lỗi thanh toán phía UnivaPay vào 2026/08/25, phía chúng tôi không nắm được lúc đó có thực hiện thủ tục thay đổi như hủy・đăng ký lại hay không.

【Điều muốn xác nhận】
1. Vì sao trên màn hình quản lý chỉ ghi nhận 1 lần thanh toán nhưng thực tế bị trừ 2 lần (có tồn tại giao dịch không phản ánh trên màn hình quản lý không?)
2. Xử lý được thực hiện khi xảy ra lỗi thanh toán 2026/08/25 (hủy・đăng ký lại, v.v.) có khả năng liên quan đến việc thanh toán trùng lần này không?
3. Khi thử hoàn tiền giao dịch tương ứng (thanh toán ngày 2026/09/26, 6,980円, số thanh toán 411193) từ màn hình lịch sử thanh toán của 「Sản phẩm・Thanh toán」, chọn 「この画面から返金を行う」 rồi bấm 「決定」 thì hiện lỗi 「キャンセル失敗しました」 và hoàn tiền không hoàn tất. Về nguyên nhân của lỗi này
4. Cách chỉ hoàn tiền 1 lần thu trùng mà không hủy bản thân hợp đồng liên tục (subscription)

Mong được xác nhận. Xin cảm ơn.

Tên friend: 寺岡 拓海
Chức năng: Bán sản phẩm (商品販売)
Thời điểm phản hồi: 2026/10/02 15:58:06
Ảnh 1: data/screenshots/T12304_0.png
Ảnh 2: data/screenshots/T12304_1.jpg

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12304

Ticket Slack do OEM đăng — 管理番号 TY-12304

## Steps to reproduce

(trống — Redmine không có section "Tái hiện bug"/"Steps to reproduce" riêng; đây là báo cáo của CS/khách hàng, không phải bug report có steps rõ ràng)

## Expected result

(trống)

## Actual result

(trống)

⚠️ **Bug không tái hiện được trong Redmine theo format Steps/Expected/Actual** — root cause đã được Dev/AI xác định qua điều tra log (journal #139789, #139876) và đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (race condition job thu tiền ↔ job recover) + regression impact, dùng dữ liệu định danh ca lỗi bên dưới để dựng lại kịch bản.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.melonglobal.net/attachments/download/31315/screenshot1.png
- screenshot2.jpg — https://redmine.melonglobal.net/attachments/download/31316/screenshot2.jpg

(Log điều tra chi tiết — xem section "Journal / note từ Redmine" bên dưới, không phải file đính kèm riêng)

## Ghi chú thêm của Leader

- ⚠️ **Fix KHÔNG trọn vẹn** — Dev/AI chỉ fix nguyên nhân gây **double charge** (race giữa job thu định kỳ UnivaPay và job recover giao dịch treo). **Câu hỏi 3 của khách hàng (lỗi hoàn tiền 「キャンセル失敗しました」 ở `cancelOrderV2`) CHƯA được điều tra/fix** trong lần này — Dev tự ghi rõ "chưa sửa", cần laravel.log quanh 15:5x ngày 02/10 (`refundMoney`/`getRefundMoney`). TC verify luồng hoàn tiền này nên expect **vẫn còn lỗi** (hoặc đánh dấu known-issue), không expect đã fix.
- ⚠️ **Verify mức rất thấp** — Dev/AI chỉ chạy được `php -l` (lint cú pháp), KHÔNG chạy được test runtime (dev MySQL Connection refused, PHP container thiếu pdo_sqlite, `getOrderTimeout` gọi Eloquent trực tiếp). Toàn bộ 23 TC trên MCP LME TEST STUDIO (task #357) đều ở trạng thái **chưa chạy** (0 pass/0 fail/23 untested) tính đến lúc fetch — QA cần test thật kỹ, không có kết quả tham chiếu nào đã Pass.
- ⚠️ **Recover data cần làm TRƯỚC khi deploy lên môi trường test/thật** (theo ■5 RECOVER DATA của Dev):
  1. Hoàn tiền giao dịch UnivaPay `11f1b865-6655-100a-9a5d-c322190a8a44` (25/09, 6,980円) trực tiếp trên dashboard UnivaPay — charge này không gắn order nào nên không ảnh hưởng hợp đồng.
  2. Trước deploy, chạy: `SELECT id,bot_id,status_webhook,c_univapay_charge_id,c_strip_charge_id,updated_at FROM s_cycle_order_history WHERE status_webhook IN (0,3,4) AND (c_univapay_charge_id IS NOT NULL OR c_strip_charge_id IS NOT NULL)` — các hợp đồng kẹt từ 25/09 sẽ được job recover xử lý hàng loạt ngay sau deploy (có thể gửi tin "thanh toán xong" trễ); hợp đồng nào đang trỏ mã giao dịch cũ phải đối soát với UnivaPay trước.
  3. Hợp đồng `41884` (charge test 0円, không có module) sẽ bị job recover bỏ qua mỗi 5 phút kèm log — cần xử lý tay `status_webhook`.
  - Phạm vi ảnh hưởng: 1 hội viên (cycle `38266`) + các hợp đồng khác đang kẹt `status_webhook` 0/3/4 từ 25/09.
- Branch QA checkout: `sns-line: ai_fixbug_41891` (nhánh gốc `release_step_20260930_v2`, commit `7b8b977178`, 3 file) — đã push.
- Rủi ro Dev tự nêu cần lưu ý khi test: (a) lỗi mạng/5xx khi gọi charge UnivaPay sau khi đã NULL mã giao dịch cũ → cycle có thể kẹt ở status_webhook 0/3 với mã NULL, cả job thu lẫn job recover đều bỏ qua; (b) cycle đang trỏ mã giao dịch cũ do lỗi TRƯỚC ĐÂY (không phải do race lần này) vẫn có thể bị xử lý lại; (c) `cancelCycle` (auto-cancel sau 3 lần lỗi bill) truyền `c_univapay_charge_id` vào `cancelSubcriptionSale` — giá trị nay có thể NULL sau lần thu lỗi không có chargeId → cần regression nhẹ cho auto-cancel.
- Trên MCP LME TEST STUDIO đã có sẵn **task #357** (23 TC do AI sinh, round 1, status "running") — dùng làm input `04-tc-list.md` (xem file 04), KHÔNG cần `/write-tc` thêm trừ khi review phát hiện thiếu quan điểm.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `118292` |
| Friend | 寺岡拓海 — `detail_line_user` (line_user_id) = `54394321`; user liên hệ CS: `wings.nontitle@gmail.com` (khác email `tomohiro.hirai92+lme2@gmail.com` ghi trong description gốc — có thể là email test/nội bộ khác với email khách hàng, cần đối chiếu) |
| Đối tượng cấu hình | Item chu kỳ: `スタンダードコース`; `s_cycle_order_history.id = 38266`; order thật hiện có `411193` (6,980円, 2026/09/26); charge UnivaPay thật không gắn order `11f1b865-6655-100a-9a5d-c322190a8a44` (2026/09/25); charge đổi thẻ cũ bị xử lý nhầm `11f1a143-e6de…` (2026/08/26); hợp đồng lỗi riêng (crash job recover) `cycle 41884` (charge test 0円, không có module) |
| Thời điểm lỗi | 2026/09/25 07:15:07 (race giữa job thu + job recover) → 2026/09/26 (double bill tạo order 411193) → 2026/10/02 ~15:58 (lỗi hoàn tiền 「キャンセル失敗しました」 khi thử refund order 411193) |
| Đối chứng | Không có case đối chứng chạy đúng cho chính hội viên này; `cycle 41884` là 1 ca lỗi riêng khác (crash `Undefined index: module`) lặp lại từ 00:00 25/09, không liên quan trực tiếp khách hàng 寺岡拓海 nhưng cùng bị chặn bởi cùng 1 bug job recover |

## Journal / note từ Redmine (nguyên văn)

**Journal #139753 — Ngọc Ánh — 2026-10-02:**

```
user: wings.nontitle@gmail.com
bot_id: 118292
item chu kỳ: スタンダードコース
detail_line_user: 54394321
```

**Journal #139789 — Do Van Tu TuDV — 2026-10-02:**

```
Diễn biến ngày 9/25 lúc 07:15:07 (laravel log)
Dòng	Sự kiện
—	Job HandleSendActionTrialV2::billItemUnivapay set status_webhook=0 cho cycle 38266, lúc này c_univapay_charge_id vẫn là charge đổi thẻ cũ (HandleSendActionTrialV2.php:235)
≈ cùng lúc	RecoverPaymentUnivapayTimeout → getOrderTimeout query danh sách cycle có status_webhook IN (0,3,4) và nhặt được 38266 với charge ID cũ. Lần chạy lúc 07:10:07, 38266 chưa có trong danh sách
3835104	Job tạo charge thật 11f1b865-6655-100a-9a5d-c322190a8a44: 6,980円, sales_job, pending. Sau đó job lưu charge ID mới, nhưng danh sách của getOrderTimeout đã lấy xong trước đó
3835200	start cycle order without webhook from job CycleorderId: 38266
3835288	getOrderTimeout gọi Univapay với charge cũ 11f1a143-e6de…: module: sales_change_card, created_on: 2026-08-26T11:47:23Z, successful
3835294	Kiểm tra 15 phút dùng created_on của charge (8/26) nên lọt qua, rồi gọi callbackChangeCard với dữ liệu cũ
—	callbackChangeCard thấy status_webhook=0 nên set status_webhook = PROCESSED (SalesService.php:857-861)
3835444	Gửi cho hội viên tin 「決済が完了しました。」. Tin này dựa trên charge cũ
—	count_bill_error = null nên bỏ qua nhánh tạo/cập nhật order (SalesService.php:920). Không có order, c_expired_date không đổi
Sau thời điểm đó:

Webhook của charge thật: charge 11f1b865-6655… chỉ xuất hiện đúng 1 lần trong log, ở lúc tạo. Không có webhook nào cho charge này trong cả ngày 9/25, trong khi các webhook khác vẫn về đều (thêm 30 lần callbackJob sau 07:15:07). Kể cả nếu webhook có về, callbackJob cũng sẽ dừng ở end sales callbackJob because processed.
Job recover các lần sau: cycle đã ở status_webhook=1 nên không còn được nhặt lại.
Kết quả: charge thật ngày 9/25 thành công bên Univapay nhưng không có order nào.
Ngày 9/26: status_webhook=1 và c_expired_date (9/25 06:58:59) vẫn nhỏ hơn hiện tại, nên job bill thêm lần nữa và tạo order 411193.
Trả lời các câu KH hỏi
Câu 1: Có một giao dịch không hiện trên màn hình quản lý. Đó là charge Univapay 11f1b865-6655-100a-9a5d-c322190a8a44 (9/25, 6,980円), không gắn với order nào trong DB.
Câu 2: Có liên quan gián tiếp. Thẻ đổi ngày 8/26 sau lỗi 8/25 để lại c_univapay_charge_id trỏ tới charge đổi thẻ. Race ngày 9/25 đã xử lý lại đúng charge này.
Câu 4: Hoàn tiền charge 11f1b865-6655… trực tiếp trên dashboard Univapay. Charge này không gắn với order nào nên không ảnh hưởng hợp đồng chu kỳ.
Câu 3 (lỗi 「キャンセル失敗しました」 với order 411193): tôi chưa điều tra.
Hướng sửa (chưa sửa code)
billItemUnivapay: set c_univapay_charge_id = null cùng lúc với status_webhook=0. getOrderTimeout yêu cầu whereNotNull(charge_id) nên sẽ không nhặt cycle trong lúc đang charge.
getOrderTimeout: đọc lại cycle mới nhất trước khi xử lý, và bỏ qua charge có metadata.module khác sales_job, hoặc charge có created_on cũ hơn lần bill hiện tại.
Bug riêng: mỗi lần chạy (5 phút một lần), getOrderTimeout crash Undefined index: module ở SalesService.php:2648 tại cycle 41884. Đó là một charge test, số tiền 0, không có module. Lỗi lặp lại từ 00:00 ngày 9/25, nên các cycle xếp sau 41884 trong danh sách không bao giờ được recover. Cần dùng ?? null và try/catch cho từng item.
```

**Journal #139876 — AI LME Fix bug — 2026-10-03:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Race giữa job thu tiền định kỳ UnivaPay và job recover giao dịch treo (5 phút/lần). Job thu đặt hợp đồng sang trạng thái chờ webhook nhưng vẫn giữ mã giao dịch CŨ (lần đổi thẻ 26/08); job recover nhặt đúng lúc đó, hỏi UnivaPay giao dịch cũ (đã thành công từ lâu nên lọt kiểm tra 15 phút), xử lý lại nó rồi đánh dấu hợp đồng là đã xử lý. Giao dịch thật 25/09 vì vậy bị bỏ qua (webhook của nó cũng bị chặn do hợp đồng đã ở trạng thái đã xử lý), hạn thanh toán không được dời nên 26/09 job thu thêm lần nữa và tạo đơn 411193. Kèm lỗi riêng: job recover crash 'Undefined index: module' ở hợp đồng 41884 (charge test 0 yên) từ 25/09, khiến mọi hợp đồng xếp sau không bao giờ được recover.

■ 2. CÁCH FIX
Job thu định kỳ UnivaPay và 2 luồng đổi thẻ (UnivaPay, Stripe) nay xoá mã giao dịch cũ cùng lúc với đặt trạng thái chờ webhook, nên job recover không nhặt hợp đồng đang thu. Job recover đọc lại hợp đồng ngay trước khi xử lý và bỏ qua nếu trạng thái hoặc mã giao dịch đã đổi; bỏ qua (có log) giao dịch không có module thay vì crash; bọc try/catch từng bản ghi để 1 bản ghi lỗi không chặn các bản ghi sau. Câu 3 (lỗi hoàn tiền đơn 411193) chưa sửa — cần log hoàn tiền.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
HandleSendActionTrialV2::billItemUnivapay (job thu định kỳ UnivaPay 07:00)
SalesService::getOrderTimeout (recover:payment_univapay_timeout, 5 phút/lần)
SalesManagementV2Controller::changeCardUnivapay (đổi thẻ UnivaPay)
SalesManagementV2Controller::updatePaymentIntent (đổi thẻ Stripe)
SalesService::callbackJob / callbackChangeCard (bỏ qua khi status_webhook đã PROCESSED)
HandleWebhookUnivapay::handle (route theo metadata.module)
SalesManagementV2Controller::cancelOrderV2 (hoàn tiền 1 lần thu — chưa sửa)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Console/Commands/HandleSendActionTrialV2.php
   - app/Http/Controllers/Basic/SalesManagementV2Controller.php
   - app/Services/Sales/SalesService.php
 • 4.2 Data ảnh hưởng:
   - s_cycle_order_history.c_univapay_charge_id / c_strip_charge_id — được set NULL lúc bắt đầu thu/đổi thẻ, ghi lại ngay khi cổng trả mã giao dịch mới
   - s_cycle_order_history.status_webhook — job recover chỉ xử lý khi vẫn 0/3/4 và mã giao dịch không đổi
 • 4.3 Tính năng liên quan:
   - Product Sales / Recurring Item (FA-026) — thu tiền định kỳ UnivaPay, đổi thẻ (UnivaPay/Stripe), job recover giao dịch treo của hợp đồng định kỳ và đơn 1 lần

■ 5. RECOVER DATA
   ⚠ CÓ — (1) Hoàn tiền giao dịch UnivaPay 11f1b865-6655-100a-9a5d-c322190a8a44 (25/09, 6,980 yên) trực tiếp trên dashboard UnivaPay — không gắn đơn nào nên không ảnh hưởng hợp đồng. (2) TRƯỚC khi deploy: SELECT id,bot_id,status_webhook,c_univapay_charge_id,c_strip_charge_id,updated_at FROM s_cycle_order_history WHERE status_webhook IN (0,3,4) AND (c_univapay_charge_id IS NOT NULL OR c_strip_charge_id IS NOT NULL) — các hợp đồng kẹt sau cycle 41884 từ 25/09 sẽ được job recover xử lý ngay sau deploy (có thể gửi tin 'thanh toán xong' trễ); hợp đồng nào đang trỏ mã giao dịch cũ phải đối soát với UnivaPay trước. (3) Hợp đồng 41884 (charge test không có module) sẽ bị bỏ qua mỗi 5 phút kèm log — cần xử lý tay status_webhook. (phạm vi: 1 hội viên (cycle 38266) + các hợp đồng đang kẹt status_webhook 0/3/4)

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l 3 file: No syntax errors; Harness runtime KHÔNG chạy được: dev MySQL Connection refused, PHP container không có pdo_sqlite, getOrderTimeout gọi Eloquent trực tiếp
   Bằng chứng: Diễn biến log 25/09 07:15 do anh TuDV trích (Redmine #41891 note 2026-10-02 08:54): getOrderTimeout xử lý charge đổi thẻ cũ 11f1a143 (26/08) cho cycle 38266 → callbackChangeCard set PROCESSED → charge thật 11f1b865 không có order; HandleWebhookUnivapay::handle đọc metadata.module không có ?? nên charge thiếu module cũng không route được — bỏ qua là đúng

■ TỰ REVIEW (AI)
Sửa theo hướng anh TuDV đề xuất, có 2 điểm khác: (a) KHÔNG lọc 'chỉ module sales_job' vì job recover còn phải xử lý hợp đồng mua lần đầu (module sales) và đổi thẻ (sales_change_card) — thay bằng kiểm mã giao dịch hiện tại của hợp đồng phải trùng mã vừa đọc; (b) KHÔNG so created_on với 'lần bill hiện tại' vì không có cột nào lưu mốc bắt đầu lần thu (updated_at bị ghi lại khi lưu mã giao dịch mới nên dùng sẽ bỏ nhầm giao dịch thật). Câu 3 (lỗi hoàn tiền 411193) chưa điều tra được — cần laravel.log quanh 15:5x 02/10 ('refundMoney'/'getRefundMoney'); màn chi tiết hợp đồng đang nuốt message lỗi server trả về.
 • Rủi ro / lưu ý khi test:
   - Chưa test runtime (không có DB)
   - Hợp đồng đang kẹt từ 25/09 sẽ được recover hàng loạt ngay sau deploy — đối soát trước (xem needDataRecovery)
   - Nếu webhook của giao dịch mới về TRƯỚC khi lưu mã giao dịch (rất ngắn) thì callback vẫn xử lý bình thường vì callback không dựa vào c_univapay_charge_id
   - Hợp đồng đang trỏ mã giao dịch cũ do lỗi trước đây (không phải do race) vẫn có thể bị xử lý lại giao dịch cũ — đối soát dữ liệu

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41891 (nhánh gốc release_step_20260930_v2, commit 7b8b977178, 3 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 4 phút 53 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=ca67ac89-2895-4676-81b7-7c12b561f7af
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=41891
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
