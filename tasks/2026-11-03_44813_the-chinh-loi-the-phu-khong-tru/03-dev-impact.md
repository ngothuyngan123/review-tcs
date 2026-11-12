# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Redmine #44813 **không có** section "Đánh giá ảnh hưởng" theo format chuẩn 4 mục (1/2/3/4.1/4.2/4.3) — nội dung được AI/Dev ghi rải trong **4 journal** (điều tra gốc → hướng sửa → dev handoff cuối, qua 2 bản fix). File này **map lại** từ journal #150153 (điều tra), #150156 (Dev Studio bản 1), #150450 (Dev Studio — dev handoff cuối, bản 2, 2026-11-03) theo đúng khung template. Bản cuối (#150450) là bản code **đã thực sự merge** — ưu tiên dùng nội dung bản này cho mục 1-4; bản 1 (#150153/#150156) chỉ giữ để tham khảo lịch sử điều tra.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (ticket Redmine không có `assigned_to` cụ thể) |
| Commit / Pull Request | `<chưa có link PR — chỉ có commit base ghi trong journal>` |
| Branch | `ai_studio_fixbug_44813` (repo `sns-line`, nhánh gốc `release_step_20260930_v2` @`830d7f37fa20`, commit `68bb0b4b832b83d2884aba30080bb4eb899084a1`) |
| Ngày submit đánh giá | `2026-11-03` (Journal #150450, 15:07 — dev handoff bản cuối) |
| Auto-filled | `2026-11-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại 4 journal gốc trên Redmine (#150153 · #150156 · #150445 · #150450) và xác nhận mục 1-4 dưới đây map đúng, không sót impact (đặc biệt 3 luồng dấu chờ thu phụ phát hiện ở bản 2).

---

## 1. Nguyên nhân

Thu tiền định kỳ thẻ Univapay có 2 bước tách rời: **job** `AutoPaymentJobUnivapay::chargeUnivapayCardBots()` chỉ tạo charge (gọi API, nhận `201/pending` ngay); kết quả thật (**successful/failed**) Univapay trả về **bất đồng bộ qua webhook** `BotController::handleCallbackBillJob()` sau 0–3 giây (median 1s).

Khối fallback sang thẻ phụ ban đầu chỉ nằm **trong job**, và chỉ chạy khi lệnh gọi API tạo charge **lỗi ngay lúc gọi** (exception/khác 201) — biến `$charge` trong job luôn có giá trị khi API trả 201 (kể cả pending), nên không phân biệt được "tạo charge OK" với "charge sẽ fail". Trường hợp **thẻ chính bị từ chối (decline)** — phổ biến nhất — chỉ được báo về qua webhook, mà webhook (bản gốc) khi `status != successful` chỉ ghi nhận lỗi (tăng `status_payment_fail`, set `status_payment = 2`, mail, `BotLifeCycle BILL_ERROR`), **không có logic thử thẻ phụ**. Các lần retry (`status_payment_fail` 1→4) lặp lại đúng luồng job → luôn lại charge thẻ chính → luôn pending → thẻ phụ **không bao giờ được dùng** → sau 5 lần hợp đồng bị hủy (status = 3) dù thẻ phụ có thể vẫn thanh toán được.

Rà soát ở bản 2 (fix thực tế) phát hiện thêm 3 luồng khiến "dấu chờ thu thẻ phụ" (đặt ra để biết hợp đồng đang chờ job thu bù) bị **không xoá** hoặc **đặt sai**:
1. Bill max friend bằng thẻ mới ghi đè thẻ chính nhưng không đổi kỳ → dấu cũ có thể còn treo sai kỳ.
2. Thêm slot enterprise trừ thẻ chính thành công nhưng dấu vẫn còn (không bị xoá).
3. Webhook báo lỗi về muộn (sau khi hợp đồng đã sang kỳ mới / đã đổi thẻ) vẫn đặt dấu vào kỳ mới — sai ngữ cảnh.

Bug ảnh hưởng **tất cả hợp đồng có đăng ký thẻ phụ**, không riêng user TY-12584 (`bot_contract_id` 46521, standard/month, 10,780円, thẻ chính 1001 / thẻ phụ 1006).

## 2. Cách fix

Nội dung thay đổi (bản fix cuối, nhánh `ai_studio_fixbug_44813`):

1. **Job thu tiền định kỳ Univapay** (`AutoPaymentJobUnivapay`): hợp đồng bị từ chối thẻ chính được thu bằng thẻ phụ ở **lượt 2** (sau khoảng 30 giây) hoặc hôm sau; nếu dấu lệch kỳ thì job quay về thu thẻ chính (không dùng dấu cũ).
2. **Webhook kết quả bill định kỳ** (`handleCallbackBillJob`, `actionBill = bill_job`): khi thẻ chính hiện tại bị từ chối, hợp đồng quá hạn và **có** thẻ phụ → chỉ đánh dấu "chờ thu thẻ phụ" (log `wait job to charge sub card`), **chưa** ghi lỗi/mail/`決済エラー`/BotLifeCycle, **không** tự tạo charge ngay trong webhook (việc thu bù do job lượt 2 làm).
3. **Webhook failed về muộn** — hợp đồng đã sang kỳ mới hoặc đã đổi thẻ chính (customer id khác token hiện tại) → **không** đặt dấu, xử lý lỗi như luồng cũ (không coi là case thu bù).
4. **Màn bill max friend** (`acceptBillMaxFriendV2`): thanh toán bằng thẻ **mới** thành công → xoá dấu chờ thu thẻ phụ (`subcard_fallback_period = NULL`), kỳ đang nợ được thu luôn bằng thẻ mới. Thanh toán bằng thẻ **cũ** thành công → dấu giữ nguyên.
5. **Màn thêm slot enterprise**: thanh toán thẻ thành công → xoá dấu chờ thu thẻ phụ; thanh toán thẻ lỗi → dấu giữ nguyên, số slot giữ nguyên; nhánh chuyển khoản không đổi.
6. Thẻ phụ cũng lỗi, hoặc không có thẻ phụ → ghi lỗi như luồng cũ, **chỉ tính 1 lần lỗi** (chặn trừ trùng khi Univapay gửi lại event, chốt unique theo mã giao dịch qua bảng `univapay_webhook_processed`).

Nhánh `successful` của webhook (charge thành công bằng thẻ phụ) đã đúng từ trước — giữ nguyên.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AutoPaymentJobUnivapay.php` (job thu tiền định kỳ) | +82 dòng — thêm lượt 2 (chờ 30s) + đọc/ghi dấu `subcard_fallback_period` | Thu bù thẻ phụ khi dấu đang chờ; quay về thẻ chính khi dấu lệch kỳ |
| 2 | `Admin/BotController.php` — `handleCallbackBillJob()` | +82 dòng — nhánh lỗi mới khi thẻ chính bị từ chối + có thẻ phụ + quá hạn | Đặt dấu chờ thu thay vì ghi lỗi ngay; chặn đặt dấu khi webhook về muộn |
| 3 | `Admin/BotEnterPriseController.php` (thêm slot enterprise) | +2 dòng — xoá dấu khi thanh toán thẻ thành công | Tránh dấu treo khi hợp đồng đã được thu qua kênh khác |
| 4 | `PointSettingController.php` (bill max friend `acceptBillMaxFriendV2`) | +10 dòng — xoá/giữ dấu theo thẻ mới/cũ, đổi kỳ khi thẻ mới | Đồng bộ dấu với thực tế đã thu tiền qua bill max friend |
| 5 | Migration `2026_11_02_000000_add_subcard_fallback_period_to_bot_contracts.php` | +50 dòng — thêm cột `bot_contracts.subcard_fallback_period` (datetime nullable, không backfill) | Lưu trạng thái "đang chờ thu bù thẻ phụ" dùng chung cho job + webhook + 2 màn thanh toán |
| 6 | `AutoPaymentJobUnivapaySubcardFallbackTest.php` | +230 dòng (test mới) | Test job lượt 2 + quay về thẻ chính khi lệch kỳ |
| 7 | `SubcardFallbackPeriodClearTest.php` | +177 dòng (test mới) | Test xoá dấu ở bill max friend + thêm slot enterprise |
| 8 | `UnivapayBillJobSubcardFallbackTest.php` | +283 dòng (test mới) | Test webhook đặt dấu / không đặt dấu (webhook muộn, customer id cũ) |

⚠️ Dev ghi rõ: **chưa test trên Univapay thật** (chỉ unit/feature test nội bộ); migration chạy trên bảng billing đang có nhiều truy cập → cần lưu ý timing deploy.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `chargeUnivapayCardBots()` (job thu tiền định kỳ) | `app/Console/Commands/AutoPaymentJobUnivapay.php` | Direct | Thêm lượt 2 (chờ 30s) + đọc dấu `subcard_fallback_period`; job `job:check_auto_payment_univapay` (06:30 hằng ngày) chạy **lâu hơn** → phần chuyển khoản phía sau job chạy muộn hơn |
| F2 | `handleCallbackBillJob()` (webhook `actionBill = bill_job`) | `app/Http/Controllers/Admin/BotController.php` | Direct | Nhánh lỗi có điều kiện mới (đặt dấu thay vì ghi lỗi); ca **không thoả** điều kiện mới vẫn đi luồng ghi lỗi cũ (retry, huỷ cưỡng bức ở lỗi lần 5, mail bill lỗi, `BotLifeCycle BILL_ERROR`) |
| F3 | Thêm slot enterprise bằng thẻ | `app/Http/Controllers/Admin/BotEnterPriseController.php` | Direct | Xoá dấu khi thanh toán thẻ thành công; nhánh chuyển khoản không đổi |
| F4 | `acceptBillMaxFriendV2()` (bill max friend) | `app/Http/Controllers/PointSettingController.php` | Direct | Câu cập nhật thẻ hợp đồng sau khi trừ thành công có thêm 1 cột (`subcard_fallback_period`); bill bằng thẻ **cũ** thành công không đổi dấu |
| F5 | Retry bill job (lỗi lần 1→5, huỷ hợp đồng) | `AutoPaymentJobUnivapay.php` / `BotController.php` | Indirect | Hành vi retry/huỷ giữ nguyên cho case **không** đủ điều kiện fallback (không có thẻ phụ / thẻ phụ cũng lỗi) |
| F6 | Mail bill lỗi / BotLifeCycle `BILL_ERROR` | — | Indirect | Chỉ **trì hoãn** (không gửi ngay khi đang chờ thu bù), vẫn gửi khi thẻ phụ cũng lỗi hoặc không có thẻ phụ |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_contracts.subcard_fallback_period` | MIGRATE (thêm cột, datetime nullable, không backfill) | Dấu "đang chờ thu bù thẻ phụ"; đọc/ghi bởi job + webhook + bill max friend + thêm slot enterprise |
| D2 | `univapay_webhook_processed` | UPDATE (thêm dòng event `subcard_fallback`) | Chốt idempotent — chặn thu bù trùng khi Univapay gửi lại webhook event |
| D3 | `bot_contracts.status_payment_fail` / `status_payment` / `expired_retry_payment` | UPDATE (hành vi có điều kiện mới) | Không tăng ngay khi đang trong trạng thái chờ thu bù thẻ phụ (khác hành vi cũ) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Job thu tiền định kỳ Univapay (`job:check_auto_payment_univapay`) | F1, D1 | High — chạm trực tiếp luồng trừ tiền tự động hằng ngày; job chạy lâu hơn do thêm lượt 2 |
| T2 | Webhook kết quả bill định kỳ (`handleCallbackBillJob` / `bill_job`) | F2, D1, D2 | High — nhánh lỗi cũ (retry/huỷ/mail/BotLifeCycle) vẫn phải chạy đúng cho ca không thoả điều kiện fallback mới |
| T3 | Thanh toán phí bạn bè vượt mức (bill max friend) | F4, D1 | Medium — chỉ thêm 1 cột cập nhật, nhưng sai sót khiến dấu treo → job sau tự ý thu lại thẻ phụ dù đã thu tiền |
| T4 | Thêm slot hợp đồng gộp (enterprise) | F3, D1 | Medium — tương tự T3 |
| T5 | Huỷ hợp đồng / 契約詳細 (chi tiết hợp đồng) | F5, F6 | Medium — huỷ cưỡng bức sau lỗi lần 5 phải vẫn đúng khi không có thẻ phụ; hợp đồng có dấu đang chờ bị huỷ giữa chừng phải dừng thu bù |
| T6 | (Ngoài phạm vi task — Dev không fix) Webhook failed muộn ghi lỗi lên hợp đồng đã thanh toán lại; `HandleBillMaxFriend` (phí max friend kênh khác) có cùng lớp lỗi không thu bù thẻ phụ | Ghi chú Dev ở journal #150450 | Low/Info — Leader quyết có mở ticket riêng hay không, **không** thuộc scope test của #44813 |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
