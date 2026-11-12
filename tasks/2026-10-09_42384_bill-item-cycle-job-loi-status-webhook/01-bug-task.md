# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42384 — Khi bill item chu kỳ job bill lỗi đang không chuyển trạng thái status webook về error` |
| Module / Màn hình | `Single Product / Sales (FA-026) — Job thu tiền định kỳ hợp đồng sản phẩm (bill item) qua UnivaPay` |

## Mô tả bug (bản dịch tiếng Việt)

=> expect chuyển trạng thái status webhook về error

<!-- Description Redmine gốc chỉ có 1 dòng ngắn trên. Không có section "Tái hiện bug" (再現手順) riêng — nội dung nguyên nhân/cách fix nằm trong 3 journal "AI LME Fix bug" (xem file 03-dev-impact.md), không phải trong description. -->

## Steps to reproduce

<!-- Redmine không có section Steps to reproduce / 再現手順 riêng. -->

1.
2.
3.

## Expected result

- Khi job thu tiền định kỳ bill item qua UnivaPay thu lỗi → `status_webhook` của hợp đồng định kỳ (`s_cycle_order_history`) phải chuyển về `2` (error), giống luồng webhook (`callbackJob`).

## Actual result

- (Trước fix) Job thu đồng bộ (không chờ webhook) hoặc gọi thu bị từ chối ngay (không có charge ID): sau khi có kết quả job luôn đặt `status_webhook` = `1` (đã xử lý) bất kể thu thành công hay lỗi. Khi lỗi lấy thông tin thẻ thì không cập nhật `status_webhook` (giữ giá trị kỳ trước). → 2 luồng (job đồng bộ vs webhook) lệch nhau.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có attachment nào trên Redmine #42384. -->

## Ghi chú thêm của Leader

- Ticket hiện tại **không có description/steps đầy đủ** — toàn bộ nội dung điều tra + fix nằm trong 3 journal của hệ thống **AI Auto-fixbug** ("AI LME Fix bug"), xem nguyên văn ở `03-dev-impact.md`.
- Bug được fix qua 3 lượt revision cùng ngày 2026-10-08 (journal #141253 → #141592 → #141828), journal sau bổ sung thêm cho journal trước — **dùng journal #141828 (lượt cuối, đầy đủ nhất) làm nội dung chính thức**.
- Liên quan đến 2 ticket khác được dẫn chiếu trong journal (không thuộc scope #42384, chỉ để tham khảo):
  - **#42450** — `CycleOrderHistory::claimPendingPayment` thêm `$cycle->syncOriginal()` sau `refresh()` (Laravel 5.5 `refresh()` không đồng bộ original → update `status_webhook` bị Eloquent bỏ qua, hợp đồng kẹt ở status chờ `3`/`0`). Fix này gộp chung commit với #42384.
  - **#42499** — AI điều tra (KHÔNG sửa code): màn đổi thẻ UnivaPay cố ý giữ `count_bill_error` ở nhánh chờ webhook (để `callbackChangeCard` + `getOrderTimeout` xử lý đúng). Dev/PO cần xác nhận đây là đúng thiết kế — **có thể ảnh hưởng kỳ vọng của TC `NEW-18`** trên test tool (xem journal #141828 nguyên văn).
- Môi trường: Dev **không verify được** trên dev (MySQL dev `host.docker.internal:3306` connection refused) — chỉ verify bằng lint (`php -l`) + đối chiếu code tĩnh với `callbackJob`. **Chưa có bằng chứng chạy thực tế** → TC cần test kỹ cả 2 nhánh (thu đồng bộ lỗi, gọi thu bị từ chối không có charge ID, lỗi lấy thông tin thẻ).
- Status Redmine hiện tại: `Fix done - Đợi test`.

## Dữ liệu định danh ca lỗi

<!-- Ticket không có ca lỗi cụ thể (bot_id / friend / thời điểm) — chỉ có mô tả logic chung. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #141253 — AI LME Fix bug — 2026-10-08:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Job thu tiền định kỳ sản phẩm (bill item) qua UnivaPay: ở nhánh thu đồng bộ (không chờ webhook) hoặc khi gọi thu bị từ chối ngay (không có charge ID), sau khi có kết quả job luôn đặt status_webhook của hợp đồng định kỳ = 1 (đã xử lý) bất kể thu thành công hay lỗi; còn khi lỗi lấy thông tin thẻ thì không cập nhật status_webhook (giữ giá trị của kỳ trước). Luồng nhận webhook (callbackJob) thì đặt đúng 2 (lỗi) khi thu lỗi nên 2 luồng lệch nhau.

■ 2. CÁCH FIX
Job thu định kỳ bill item UnivaPay: khi thu lỗi (thu đồng bộ trả lỗi/failed, hoặc gọi thu bị từ chối không có charge ID) đặt status_webhook hợp đồng = 2 (lỗi) thay vì luôn = 1; thu thành công vẫn = 1. Khi lỗi lấy thông tin thẻ cũng đặt = 2 qua hàm mới CycleOrderHistory::markPaymentError (UPDATE có điều kiện, không đè hợp đồng đang chờ kết quả thanh toán của lượt khác như màn đổi thẻ). Quét ngang: màn đổi thẻ UnivaPay cũng ghi 1 khi thu lỗi — khác luồng, ghi yokoten ngoài scope.

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/CycleOrderHistory.php: OK; php -l app/Console/Commands/HandleSendActionTrialV2.php: OK; Kiểm Laravel 5.5 có Model::syncOriginalAttribute (HasAttributes.php:929): có; git diff --stat release_step_20260930_v2...ai_small_42384: 2 file, +30/-1
   Bằng chứng: MySQL dev host.docker.internal:3306 Connection refused — không chạy được query kiểm chứng/tái hiện trên dev; Đối chiếu code: callbackJob (luồng webhook) đặt STATUS_WEBHOOK_ERROR khi statusPayment != successful; job đồng bộ đặt cứng PROCESSED

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_42384 (nhánh gốc release_step_20260930_v2, commit da4556a50a, 2 file)  [đã push]
────────────────────────────────────────────────
(xem đầy đủ mục 3/4/5 + tự review ở file 03-dev-impact.md; journal này đã được thay thế bởi #141592 → #141828)
```

**Journal #141592 — AI LME Fix bug — 2026-10-08:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST (bổ sung #42450)
Cách fix thêm: [#42450] CycleOrderHistory::claimPendingPayment thêm $cycle->syncOriginal() sau refresh(): refresh() của Laravel 5.5 không đồng bộ original nên update status_webhook về đúng giá trị trước claim (HĐ đang lỗi 2 thu lại lỗi → 2; HĐ 1 thu OK → 1) bị Eloquent bỏ qua, hợp đồng kẹt ở 3 (bot không webhook)/0 (bot webhook).

BRANCH / COMMIT: sns-line: ai_small_42384 (nhánh gốc release_step_20260930_v2, commit 50c254e430, 2 file) [đã push]
────────────────────────────────────────────────
(xem đầy đủ mục 1-6 + tự review ở file 03-dev-impact.md; journal này đã được thay thế bởi #141828)
```

**Journal #141828 — AI LME Fix bug — 2026-10-08:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST (bổ sung điều tra #42499)
Thêm: [#42499] Điều tra, KHÔNG sửa code: màn đổi thẻ UnivaPay (bot có webhook, kết quả còn chờ) cố ý giữ nguyên count_bill_error (vd 1) vì callback webhook đổi thẻ (SalesService::callbackChangeCard) chỉ chốt kết quả khi count_bill_error còn giá trị (thu OK → NULL, thu lỗi → +1), và job xử lý quá hạn webhook (getOrderTimeout #41974) coi count_bill_error=NULL là charge đổi thẻ đã chốt. Nếu reset ở nhánh chờ thì webhook về sẽ bỏ qua, khách đã bị trừ tiền nhưng hợp đồng không gia hạn. Đề nghị Dev/PO xác nhận và trả lời Redmine #42499 là đúng thiết kế.

TỰ REVIEW (AI) — rủi ro/lưu ý khi test:
   - Nhánh lỗi lấy thông tin thẻ: nếu status đã là 2 thì MySQL trả affected=0 (giá trị không đổi) — chỉ ảnh hưởng giá trị trả về, không ảnh hưởng dữ liệu
   - Màn đổi thẻ UnivaPay còn cùng pattern (yokoten ngoài scope)
   - #42499 kết luận đúng thiết kế, không sửa code — cần Dev/PO xác nhận kỳ vọng của test case NEW-18 (reset count_bill_error ở nhánh chờ webhook sẽ phá callbackChangeCard + getOrderTimeout)

BRANCH / COMMIT: sns-line: ai_small_42384 (nhánh gốc release_step_20260930_v2, commit 50c254e430, 2 file) [đã push]
────────────────────────────────────────────────
(đây là journal cuối, đầy đủ nhất — nội dung mục 1-6 đầy đủ chép sang 03-dev-impact.md)
```
