# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44813 — [31-10-2026] [TY-12584] [Bill tiền tool] Thẻ chính lỗi thanh toán nhưng thẻ phụ không bị trừ` |
| Module / Màn hình | Bill tiền tool — thu tiền định kỳ hợp đồng Univapay (thẻ chính + thẻ phụ), webhook kết quả bill job, màn `契約詳細` (chi tiết hợp đồng) |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-12584.
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1793406611960409
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12584

Tôi đã đăng ký thẻ tín dụng chính (4 số cuối：1001) và thẻ phụ (4 số cuối：1006).
Ngày 10/31 thanh toán bằng thẻ chính (1001) bị lỗi.
Tuy nhiên thanh toán bằng thẻ phụ lại không được thực hiện.
Xin cho biết lý do.

## Steps to reproduce

<!-- Ticket không có section "Tái hiện bug" riêng — xem cảnh báo ở "Ghi chú thêm của Leader". -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.melonglobal.net/attachments/download/38271/SnapCrab_NoName_2026-10-31_9-28-7_No-00.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trên **Card test** của Univapay — Journal #150445 (Kim Cúc, 2026-11-03): "Card test không tái hiện được, tại vì lúc Fail univapay trả về luôn trạng thái fail" (nghĩa là test card trả fail đồng bộ ngay khi tạo charge, khác hành vi thật của Univapay production — API trả `201/pending`, kết quả thật trả **bất đồng bộ qua webhook** sau 0–3s). Root cause đã được Dev confirm qua điều tra log thật (Journal #150153) + đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact, không cố tái hiện lại bug gốc bằng card test thông thường.

Root cause đã qua 3 lần đánh giá / fix (xem file 03):
- **Bản 1** (Journal #150153, AI Reader) — phát hiện gốc: fallback thẻ phụ trong job chỉ chạy khi API tạo charge lỗi ngay; thẻ bị từ chối (decline) báo về qua webhook thì không có fallback.
- **Bản Dev Studio v1** (Journal #150156) — hướng sửa: webhook thu bù thẻ phụ khi thẻ chính bị từ chối + chốt mỗi charge lỗi chỉ thu bù 1 lần.
- **Bản 2 / handoff cuối** (Journal #150450, 2026-11-03 15:07, nhánh `ai_studio_fixbug_44813`) — bản fix thực tế đã merge code, bổ sung thêm 3 luồng xoá/giữ dấu chờ thu phụ (bill max friend, thêm slot enterprise, webhook muộn). **File 03 bám theo bản handoff cuối này.**

Lưu ý khi test:
- `bot_contract_id` ca lỗi gốc = **46521**, hợp đồng `standard / month`, 10,780円.
- Migration `bot_contracts.subcard_fallback_period` (datetime nullable, không backfill) phải chạy **trước** deploy code; server chạy cron job và server nhận webhook Univapay phải lên code mới **cùng lúc** (hoặc server job lên trước) — lên lệch thứ tự thì hợp đồng bị đánh dấu nhưng job cũ không thu thẻ phụ và cũng không ghi lỗi.
- Ngoài phạm vi task (Dev liệt kê riêng, không fix trong ticket này): webhook failed về muộn sau khi khách đã thanh toán lại vẫn ghi lỗi (lỗi có sẵn ở base); bill phí max friend (`HandleBillMaxFriend`) có cùng lớp lỗi không thu bù thẻ phụ; các hợp đồng có thẻ phụ đã bị huỷ cưỡng bức do bug cũ từ 02/2026 — người phụ trách quyết khôi phục từng ca riêng; hợp đồng 46521 của khách cần kiểm trạng thái + thu lại thủ công bằng thẻ phụ 1006.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — tra theo admin_id 63791>` |
| Friend | `<N/A — đây là ca bill tiền hợp đồng, không phải friend LINE>` |
| Đối tượng cấu hình | `bot_contract_id = 46521` (standard/month, 10,780円) — user harrel.0504@gmail.com (admin_id 63791), thẻ chính 1001 (Amex, token `11f10623-0c76-1510-bcf9-375bce8c5bab`), thẻ phụ 1006 |
| Thời điểm lỗi | `2026/10/31 06:43:13` (job `job_crontab_2026-10-30.log`) — charge id `11f1d3e1-be57-3fca-8555-af8f69abd670`, API Univapay trả `201 / status: pending` |
| Đối chứng | Không có — Dev ghi "bug ảnh hưởng tất cả hợp đồng có đăng ký thẻ phụ", không riêng user này |

## Journal / note từ Redmine (nguyên văn)

**Journal #150153 — AI Reader AI Reader — 2026-11-02:**

```
h2. Điều tra nguyên nhân

*User*: harrel.0504@gmail.com (admin_id 63791) — bot_contract_id *46521* (standard / month, 10,780円), thẻ chính 1001 (Amex), thẻ phụ 1006.

h3. 1. Log job bill (job_crontab_2026-10-30.log)

<pre>
06:43:13 check bill money contract bot - univapay card: 46521
06:43:13 AutoChargeByJob - UnivapayCard-> 46521 -> amount: 10780 - current expired: 2026-10-29 23:59:59 - next expired: 2026-11-29 23:59:59
06:43:13 univapay token: 11f10623-0c76-1510-bcf9-375bce8c5bab   ← token THẺ CHÍNH
06:43:14 call api payment univapay201
06:43:14 status: pending
06:43:14 unvivapay card charge data: 11f1d3e1-be57-3fca-8555-af8f69abd670
</pre>

→ Job chỉ tạo charge bằng thẻ chính, API Univapay trả *201 / status = pending*. Không có lần charge nào bằng thẻ phụ.

h3. 2. Nguyên nhân trong code

*(a) Job* @app/Console/Commands/AutoPaymentJobUnivapay.php@ — @chargeUnivapayCardBots()@ (L709-717):

<pre><code class="php">
$charge = $this->univapayPayment->chargeMoneyUnivapayJob(... token thẻ chính ...);
if (!$charge) {
    $subcard = SubcardBotContract::where('bot_contract_id', ...)->first();
    if ($subcard) { /* charge thẻ phụ */ }
}
</code></pre>

@chargeMoneyUnivapayJob()@ (@app/Helpers/UnivapayPayment.php@) trả về charge id ngay khi API trả HTTP 201, kể cả khi charge còn @pending@. Kết quả thật (successful / failed) Univapay trả *bất đồng bộ qua webhook*.
→ @$charge@ luôn có giá trị khi tạo charge OK, nên khối thẻ phụ *chỉ chạy khi gọi API tạo charge bị exception / khác 201*. Trường hợp thẻ bị từ chối (decline) không đi vào khối này.

*(b) Webhook* @app/Http/Controllers/Admin/BotController.php@ — @handleCallbackBillJob()@ (actionBill = @bill_job@):
Khi @status != successful@ chỉ ghi nhận lỗi: tăng @status_payment_fail@, set @status_payment = 2@, set @expired_retry_payment@, gửi mail bill lỗi, BotLifeCycle BILL_ERROR. *Không có logic charge lại bằng thẻ phụ.*

*(c) Retry* (status_payment_fail 1→4) đi lại đúng luồng job ở (a) → lại charge thẻ chính, lại nhận pending → thẻ phụ *không bao giờ được dùng*. Sau 5 lần hợp đồng bị hủy (status = 3) dù thẻ phụ có thể vẫn thanh toán được.

h3. 3. Thời gian webhook trả về

Đo trên laravel-2026-10-24.log (78 callback bill_job) và laravel-2026-10-071.log: callback về sau *0–3 giây* (median 1s) kể từ @created_on@ của charge, kể cả charge @failed@ (1–2s).

h3. Kết luận

Thẻ phụ chỉ được dùng khi lệnh tạo charge thẻ chính lỗi ngay lúc gọi API. Trường hợp thẻ chính bị từ chối (failed qua webhook) — trường hợp phổ biến nhất — không có luồng fallback sang thẻ phụ. Bug ảnh hưởng *tất cả hợp đồng có đăng ký thẻ phụ*, không riêng user này.

_Lưu ý_: log laravel ngày 30/10 không có log webhook (server nhận callback khác), nên cần check thêm trên Univapay dashboard trạng thái / error code của charge @11f1d3e1-be57-3fca-8555-af8f69abd670@ và DB @bot_contracts@ id 46521 (status_payment_fail, error_code), @subcard_bot_contract@ (bot_contract_id = 46521).

h2. Cách fix (đề xuất)

Xử lý fallback thẻ phụ trong *webhook* @handleCallbackBillJob()@:

# Khi @actionBill = bill_job@ và @status = failed@:
** Lấy @SubcardBotContract@ theo @bot_contract_id@ + @admin_id@.
** Nếu có thẻ phụ *và* charge vừa lỗi là của thẻ chính (@metadata.univapayCustomerId != subcard.univa_customer_id@) → gọi @chargeMoneyUnivapayJob()@ bằng token/customer của thẻ phụ (actionBill vẫn @bill_job@), *chưa* tăng @status_payment_fail@, không gửi mail lỗi, return.
** Nếu không có thẻ phụ, hoặc charge lỗi chính là charge thẻ phụ, hoặc tạo charge thẻ phụ bị lỗi ngay → xử lý lỗi như hiện tại (tăng status_payment_fail, mail, BotLifeCycle...).
# Nhánh successful hiện đã xử lý đúng khi charge bằng thẻ phụ (giữ nguyên token thẻ chính, dùng token thẻ phụ để ghi lịch sử) → không cần sửa.
# Giữ khối fallback hiện tại trong job (trường hợp gọi API lỗi ngay).
# Log rõ: @charge main failed → fallback sub card@ (bot_contract_id, last4 main/sub, charge_id) để trace.

*Ảnh hưởng*: chỉ luồng bill định kỳ thẻ Univapay (job @AutoPaymentJobUnivapay@ + callback @bill_job@). Cần test: (1) thẻ chính OK; (2) thẻ chính failed + có thẻ phụ OK; (3) thẻ chính failed + thẻ phụ failed → tính 1 lần lỗi; (4) thẻ chính failed + không có thẻ phụ; (5) retry lần 2–5.

*Xử lý cho user hiện tại*: sau khi xác nhận trạng thái hợp đồng 46521, có thể bill lại thủ công bằng thẻ phụ 1006.
```

**Journal #150156 — Dev Studio — 2026-11-02:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Thu tiền định kỳ thẻ Univapay có 2 bước: job AutoPaymentJobUnivapay chỉ tạo charge, kết quả thật do webhook handleCallbackBillJob nhận sau. Khối thu bù thẻ phụ chỉ nằm trong job và chỉ chạy khi gọi API tạo charge bị lỗi ngay; thẻ bị từ chối thì API vẫn trả 201 pending nên job không thu bù. Webhook nhận failed thì chỉ ghi lỗi, không thử thẻ phụ; các lần retry lặp lại y hệt nên thẻ phụ không bao giờ được dùng và sau 5 lần hợp đồng bị huỷ.

Hướng sửa:
- D-1 Webhook thu tiền định kỳ thu bù bằng thẻ phụ khi charge thẻ chính bị từ chối
- D-2 Chốt mỗi charge lỗi chỉ được thu bù thẻ phụ một lần

Ảnh hưởng / rủi ro:
Chỉ đổi webhook Univapay của thu tiền định kỳ gói (actionBill bill_job); job, bill max friend, chuyển khoản, bill lại thủ công không đổi. Rủi ro chính là trừ trùng thẻ phụ khi Univapay gửi lại event, đã chặn bằng chốt unique theo mã giao dịch; cần test kỹ các ca tiền (thẻ phụ OK/lỗi, retry, gửi lại event, hợp đồng năm).
```

**Journal #150445 — Kim Cúc — 2026-11-03:**

```
Thao tác tái hiện: Card test không tái hiện được, tại vì lúc Fail univapay trả về luôn trạng thái fail
```

**Journal #150450 — Dev Studio — 2026-11-03:**

```
Dev handoff — 03/11 15:07 · nhánh ai_studio_fixbug_44813

Nguyên nhân:
Nguyên nhân gốc của ticket không đổi: thẻ chính bị từ chối chỉ được báo về qua webhook, mà webhook không thu bù thẻ phụ. Rà soát bản 2 tìm ra 3 luồng mà dấu chờ thu thẻ phụ không được xoá hoặc bị đặt sai. Thứ nhất, bill max friend bằng thẻ mới ghi đè thẻ chính nhưng không đổi kỳ. Thứ hai, thêm slot enterprise trừ thẻ chính thành công nhưng dấu vẫn còn. Thứ ba, webhook báo lỗi về muộn đặt dấu vào kỳ mới.

Nội dung thay đổi:
- Job thu tiền định kỳ thẻ Univapay: hợp đồng bị từ chối thẻ chính được thu bằng thẻ phụ ở lượt 2 (sau khoảng 30 giây) hoặc hôm sau; nếu dấu lệch kỳ thì quay về thu thẻ chính.
- Webhook kết quả bill định kỳ: khi thẻ chính hiện tại bị từ chối, hợp đồng quá hạn và có thẻ phụ thì chỉ đánh dấu chờ thu thẻ phụ, chưa ghi lỗi/mail/決済エラー và không tự tạo charge.
- Webhook failed về muộn (hợp đồng đã sang kỳ mới hoặc đã đổi thẻ chính) thì không đánh dấu, xử lý như trước khi sửa.
- Màn bill max friend: thanh toán bằng thẻ mới thành công thì xoá dấu chờ thu thẻ phụ, kỳ đang nợ được thu bằng thẻ mới.
- Màn thêm slot enterprise: thanh toán bằng thẻ thành công thì xoá dấu chờ thu thẻ phụ.
- Thẻ phụ cũng lỗi hoặc không có thẻ phụ: ghi lỗi như cũ, chỉ tính 1 lần.

File đã sửa (php-web):
  app/Console/Commands/AutoPaymentJobUnivapay.php    |  82 +++++-
  app/Http/Controllers/Admin/BotController.php       |  82 ++++++
  .../Controllers/Admin/BotEnterPriseController.php  |   2 +
  app/Http/Controllers/PointSettingController.php    |  10 +-
  ...dd_subcard_fallback_period_to_bot_contracts.php |  50 ++++
  .../AutoPaymentJobUnivapaySubcardFallbackTest.php  | 230 +++++++++++++++++
  tests/Feature/SubcardFallbackPeriodClearTest.php   | 177 +++++++++++++
  .../Feature/UnivapayBillJobSubcardFallbackTest.php | 283 +++++++++++++++++++++
  8 files changed, 910 insertions(+), 6 deletions(-)

Đánh giá ảnh hưởng — Rủi ro trung bình: Thay đổi chạm tới tiền của khách, gồm job, webhook và 2 màn thanh toán. Đã có test và kiểm chứng ngược nhưng chưa thử trên Univapay thật; migration chạy trên bảng billing đang có nhiều truy cập.
- Job job:check_auto_payment_univapay (06:30 hằng ngày): có thêm lượt 2 và chờ 30 giây nên chạy lâu hơn; phần chuyển khoản phía sau chạy muộn hơn.
- Webhook Univapay nhánh bill_job: nhánh lỗi có điều kiện mới; ca không thoả đi luồng ghi lỗi cũ (retry, huỷ cưỡng bức ở lỗi lần 5, mail bill lỗi, BotLifeCycle BILL_ERROR).
- Bill max friend (acceptBillMaxFriendV2): câu cập nhật thẻ hợp đồng sau khi trừ thành công có thêm 1 cột; bill bằng thẻ cũ không đổi.
- Thêm slot enterprise bằng thẻ: câu cập nhật số slot/số tiền có thêm 1 cột; nhánh chuyển khoản không đổi.
- Bảng bot_contracts có thêm cột subcard_fallback_period; bảng chốt univapay_webhook_processed có thêm dòng event subcard_fallback.

Migration / thay đổi dữ liệu:
- [Schema · Trước deploy] Thêm cột bot_contracts.subcard_fallback_period (datetime nullable, không backfill) — database/migrations/2026_11_02_000000_add_subcard_fallback_period_to_bot_contracts.php: php artisan migrate --force

Recover dữ liệu: Không cần recover — Cột subcard_fallback_period mới thêm ở bản 2 và chưa deploy, nên chưa có dòng dữ liệu nào bị đặt dấu sai. Việc khôi phục các hợp đồng bị huỷ do bug gốc là follow-up đã ghi từ trước.

Lưu ý khi deploy:
- Chạy migration trước khi deploy code (webhook, job và 2 màn thanh toán ghi/đọc cột mới).
- Server chạy cron job và server nhận webhook Univapay phải lên code mới cùng lúc (hoặc server job lên trước). Nếu chỉ webhook lên trước, hợp đồng sẽ bị đánh dấu nhưng job cũ không thu thẻ phụ và cũng không ghi lỗi.

Việc cần người làm thêm (ngoài phạm vi task):
- Lỗi có sẵn ở base, không do fix này gây ra: webhook báo thẻ từ chối về muộn sau khi khách đã thanh toán lại vẫn ghi lỗi thanh toán cho hợp đồng đã trả tiền. Nên mở ticket riêng nếu muốn chặn.
- Webhook failed về muộn sau khi khách đã thanh toán lại vẫn đi luồng ghi lỗi cũ (lỗi có sẵn ở base, không do fix này): cần ticket riêng nếu muốn bỏ qua hẳn webhook muộn.
- Khi deploy: chạy migration cột subcard_fallback_period trước (giờ thấp điểm, tránh 06:30), rồi lên server job và server webhook cùng lúc.
- Webhook failed về muộn ghi lỗi lên hợp đồng đã thanh toán (hành vi có sẵn ở base): cân nhắc mở ticket riêng.
- Bill phí max friend (HandleBillMaxFriend) có cùng lớp lỗi không thu bù thẻ phụ: mở ticket riêng.
- Hợp đồng có thẻ phụ đã bị huỷ cưỡng bức do bug từ 02/2026: người phụ trách quyết khôi phục từng ca (query trong docs/investigation/v1.md).
- Hợp đồng 46521 của khách (TY-12584): kiểm tra trạng thái, thu lại thủ công bằng thẻ phụ 1006 nếu cần và trả lời khách.

Điểm cần test:
- Các điểm kiểm thử của bản 1–2 giữ nguyên.
- Đang có dấu, khách bill max friend bằng thẻ mới thành công → dấu về NULL, job lần sau trừ thẻ chính mới.
- Đang có dấu, thêm slot enterprise bằng thẻ thành công → dấu về NULL, job lần sau trừ thẻ chính.
- Webhook failed về khi hợp đồng đã sang kỳ mới (đã đổi thẻ hoặc thanh toán lại) → không đặt dấu, có log lý do.
- Webhook failed của thẻ chính cũ sau khi khách đã đổi thẻ chính (customer id khác) → không đặt dấu.
- Đang có dấu, khách đổi thẻ / thanh toán lại / gia hạn → kỳ đổi, job xoá dấu và trừ thẻ chính (đã đúng từ bản 2, kiểm lại hồi quy).
- Hợp đồng có thẻ phụ, quá hạn, thẻ chính bị từ chối: webhook đặt dấu (log 'wait job to charge sub card'), job thu thẻ phụ, không trừ trùng.
- Đang có dấu, bill max friend bằng thẻ mới thành công: subcard_fallback_period = NULL, thẻ chính hợp đồng là thẻ mới; job lần sau trừ thẻ chính mới.
- Đang có dấu, bill max friend bằng thẻ cũ: dấu giữ nguyên, job thu thẻ phụ.
- Đang có dấu, admin enterprise thêm slot bằng thẻ thành công: dấu = NULL; thêm slot thẻ lỗi: dấu giữ nguyên.
- Webhook failed bill_job cho hợp đồng đã sang kỳ mới: không đặt dấu, log reason=contract_not_overdue, không có dòng subcard_fallback trong univapay_webhook_processed.
- Webhook failed với customer id thẻ chính cũ (đã đổi thẻ): không đặt dấu, log reason=not_current_main_card.

Branch: ai_studio_fixbug_44813
- sns-line: ai_studio_fixbug_44813 (nhánh gốc release_step_20260930_v2 @830d7f37fa20, commit 68bb0b4b832b83d2884aba30080bb4eb899084a1)
```
