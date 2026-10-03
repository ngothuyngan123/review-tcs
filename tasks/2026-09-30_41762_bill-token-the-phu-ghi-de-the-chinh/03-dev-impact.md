# 03 — Đánh giá ảnh hưởng từ Dev

<!-- Nguồn: Journal #139403 — AI LME Fix bug — 2026-09-30 (báo cáo AI AUTO-FIXBUG, ghi nguyên văn theo nội dung journal Redmine #41762). -->

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Ngô Thúy Ngần (assignee ticket)` — fix do AI Auto-fixbug LME sinh, chưa có Dev người review lại trong journal |
| Commit / Pull Request | `commit a326f28ed3` (không có link PR trong Redmine) |
| Branch | `sns-line: ai_fixbug_41762` (nhánh gốc `release_step_20260827`, 3 file, đã push) |
| Ngày submit đánh giá | `2026-09-30` |
| Auto-filled | `2026-09-30 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Token thẻ dùng để thu tiền định kỳ của hợp đồng bị ghi đè bằng token của THẺ PHỤ. Khi thu tiền tháng thất bại với thẻ chính, job tự thu bù bằng thẻ phụ (đúng thiết kế), nhưng webhook Univapay xử lý kết quả lại lưu luôn token thẻ phụ vào hợp đồng, trong khi 4 số cuối hiển thị vẫn là thẻ chính. Từ kỳ sau, mọi lần thu tiền đều trừ thẻ phụ và thẻ chính không bao giờ được thử lại — đúng hiện tượng khách hỏi (hiển thị thẻ chính 2019 nhưng ngày 20/9 lại trừ thẻ phụ 5190). Hai lối vào khác ghi đè y hệt: đăng ký/đổi thẻ phụ khi hợp đồng đang quá hạn hoặc chưa thanh toán, và tái ký hợp đồng chọn trả bằng thẻ phụ.

⚠ **ĐÍNH CHÍNH sau tự review v2**: lối vào thứ 3 (tái ký hợp đồng chọn thẻ phụ) KHÔNG thể gây hiện tượng của ticket — FE chỉ gửi `select_card=4` khi hợp đồng KHÔNG CÒN thẻ chính (`univa_last_four_card` rỗng, `recontract.js:131-137`, nơi gửi duy nhất `:150`), trái với ticket (khách vẫn thấy thẻ chính 2019). **Hai lối vào thật là webhook `bill_job` và đăng ký/đổi thẻ phụ lúc quá hạn.**

## 2. Cách fix

Chặn 3 chỗ ghi token thẻ phụ vào hợp đồng để token trên hợp đồng luôn là thẻ chính:
1. Webhook xử lý kết quả thu tiền định kỳ — tách biến riêng cho token thẻ đã thực thu (chỉ dùng để lấy thông tin thẻ ghi lịch sử) và bỏ việc ghi token đó vào hợp đồng, kèm log khi kỳ đó thu bằng thẻ phụ.
2. Đăng ký/đổi thẻ phụ khi hợp đồng quá hạn — bỏ ghi token thẻ phụ vào hợp đồng (lần thu đã truyền token trực tiếp, callback của luồng này vốn cũng cố ý không ghi thông tin thẻ lên hợp đồng).
3. Tái ký hợp đồng — chỉ ghi token khi KHÔNG chọn thẻ phụ, đúng như khối cập nhật khác trong cùng hàm đã làm.

Quét ngang: còn 1 chỗ cùng họ ở luồng gia hạn hợp đồng chọn thẻ phụ (ghi cả token + 4 số cuối nên hiển thị đổi theo, khác hiện tượng của ticket) — **chỉ ghi nhận, đề xuất ticket riêng, KHÔNG nằm trong phạm vi fix này**.

**TỰ REVIEW v2 (commit a326f28ed3)**: bản fix gốc dùng guard chỉ dựa `select_card`/thẻ phụ nên ở nhánh hợp đồng KHÔNG CÒN thẻ chính (`univa_last_four_card` rỗng — vd hợp đồng từng đổi sang 銀行振込 nên token hiện là token CHUYỂN KHOẢN) đã để hợp đồng mang token vô dụng vĩnh viễn: job thu tiền vẫn pick lên (cần `token != null` + `payment_method=1`, mà cả 2 chỗ vẫn set `payment_method=1`) rồi charge thất bại mỗi kỳ (+60s sleep + 2 notifyChatwork) mới thu bù thẻ phụ; token NULL thì bị `whereNotNull` loại hẳn ⇒ không bao giờ thu tiền nữa. Đã siết điều kiện thành "chỉ giữ token thẻ chính khi hợp đồng THỰC SỰ còn thẻ chính" tại 2 lối vào `reContractChangeCard` (`PointSettingController:1509`) và `createSubCard` (`UserController:4948`), kèm `logInfo` ghi vết khi nhận token vừa thu làm token định kỳ. Hợp đồng còn thẻ chính vẫn giữ nguyên hành vi fix gốc (không ghi đè).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotController::handleCallbackBillJob` (app/Http/Controllers/Admin/BotController.php) | Có sửa | Xử lý kết quả webhook thu tiền định kỳ — nguồn ghi đè token chính bằng token phụ |
| 2 | `BotController::univapayCallback` (app/Http/Controllers/Admin/BotController.php) | Có sửa | Callback chung Univapay, cùng luồng với #1 |
| 3 | `BotController::handleCallbackChangeCardSuccess` (app/Http/Controllers/Admin/BotController.php) | Có sửa | Callback khi đổi thẻ phụ thành công |
| 4 | `UserController::createSubCard` (app/Http/Controllers/Basic/UserController.php) | Có sửa | Đăng ký thẻ phụ khi hợp đồng quá hạn — lối vào ghi đè thứ 2, đã siết guard ở tự review v2 |
| 5 | `UserController::updateSubCard` / `deleteSubCard` / `detailContract` (app/Http/Controllers/Basic/UserController.php) | Đã check, không sửa | Caller liên quan tới thẻ phụ, xác nhận không ghi đè token hợp đồng |
| 6 | `PointSettingController::reContractChangeCard` (app/Http/Controllers/PointSettingController.php) | Có sửa | Tái ký hợp đồng chọn thẻ phụ — đã siết guard ở tự review v2 |
| 7 | `PointSettingController::changeCard` (app/Http/Controllers/PointSettingController.php) | Đã check, không sửa | Đổi thẻ chính, không liên quan token thẻ phụ |
| 8 | `PointSettingController::extendContract` (app/Http/Controllers/PointSettingController.php) | Đã check, KHÔNG sửa (cố ý để ngoài phạm vi) | Gia hạn hợp đồng chọn thẻ phụ vẫn ghi đè cả token + 4 số cuối — khác hiện tượng ticket, đề xuất ticket riêng |
| 9 | `AutoPaymentJobUnivapay::handle` (app/Console/Commands/AutoPaymentJobUnivapay.php) | Đã check, không sửa | Job cron gọi tới luồng charge, không trực tiếp ghi token |
| 10 | `HandleBillMaxFriend::handle` (app/Console/Commands/HandleBillMaxFriend.php) | Đã check, không sửa | Đọc token hợp đồng để charge phí vượt hạn mức bạn bè — bị ảnh hưởng gián tiếp (thẻ bị trừ đổi) |
| 11 | `UnivapayPayment::chargeMoneyUnivapayJob` (app/Helpers/UnivapayPayment.php) | Đã check, không sửa | Hàm charge dùng chung, gửi `transaction_token_id` lên Univapay — bằng chứng: thẻ bị trừ phụ thuộc DUY NHẤT vào token |
| 12 | `BotEnterPriseController::paymentAddSlotEnterprise` (app/Http/Controllers/Admin/BotEnterPriseController.php:281) | Đã check, không sửa — bổ sung sau tự review v2 | Thêm slot gói おまとめ/EP, charge bằng token hợp đồng ⇒ bị ảnh hưởng gián tiếp |
| 13 | `UserService` (app/Services/UserService.php:127-140) | Đã check, không sửa — bổ sung sau tự review v2 | Đổi email tài khoản: PATCH token trên Univapay theo token hợp đồng ⇒ bị ảnh hưởng gián tiếp |
| 14 | `RecoverUpdateInfoUnivapay` (app/Console/Commands/RecoverUpdateInfoUnivapay.php:65) | Đã kiểm, KHÔNG bị ảnh hưởng — bổ sung sau tự review v2 | Cron 5 phút, lọc `payment_method=2` (chuyển khoản) nên không đụng luồng thẻ |
| 15 | `BotContracts::getBotNeedChargeByUnivapayCard` (app/BotContracts.php:39-49) | Đã check, không sửa — bổ sung sau tự review v2 | Điều kiện lọc hợp đồng cần thu (`whereNotNull univa_transaction_token` + `payment_method=1`) — quyết định hợp đồng có được job thu tiền hay không, liên quan trực tiếp tới nguy cơ "token null bị loại vĩnh viễn" mà tự review v2 đã sửa |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `handleCallbackBillJob` / `univapayCallback` / `handleCallbackChangeCardSuccess` | app/Http/Controllers/Admin/BotController.php | Direct | Webhook Univapay — điểm ghi đè token gốc |
| F2 | `createSubCard` | app/Http/Controllers/Basic/UserController.php | Direct | Đăng ký thẻ phụ lúc quá hạn — điểm ghi đè token thứ 2, đã siết guard v2 |
| F3 | `reContractChangeCard` | app/Http/Controllers/PointSettingController.php | Direct | Tái ký hợp đồng chọn thẻ phụ — đã siết guard v2 |
| F4 | `AutoPaymentJobUnivapay::handle`, `chargeMoneyUnivapayJob`, `getBotNeedChargeByUnivapayCard` | app/Console/Commands + app/Helpers + app/BotContracts.php | Indirect | Job thu tiền định kỳ — hành vi chọn/charge token đổi theo dữ liệu do F1-F3 ghi ra |
| F5 | `billAgainContract` / `billCardUnivapayContract` / `changeStatusContract`, `HandleBillMaxFriend::handle`, `paymentAddSlotEnterprise`, `UserService` (đổi email) | PointSettingController.php, HandleBillMaxFriend.php, BotEnterPriseController.php, UserService.php | Indirect | Đều đọc token hợp đồng để charge/PATCH — thẻ bị trừ đổi từ phụ → chính sau fix |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_contracts.univa_transaction_token` | UPDATE (hành vi ghi thay đổi, schema không đổi) | Sau fix cột này giữ đúng token thẻ chính. **CÁC HỢP ĐỒNG CŨ đã bị ghi đè trước fix vẫn đang trỏ thẻ phụ** — token thẻ chính cũ KHÔNG phục hồi được từ DB, phải lấy lại từ Univapay theo `univa_customer_id` hoặc nhờ khách đăng ký lại thẻ chính (xem mục RECOVER DATA bên dưới) |
| D2 | `subcard_bot_contracts` | Chỉ đọc, không đổi | — |
| D3 | `bot_life_cycle.data.last4_card_main` | Không đổi hành vi | Vẫn ghi 4 số cuối của thẻ ĐÃ THỰC THU (thẻ phụ nếu kỳ đó thu bù) |
| D4 | `bot_contracts.billing_address` | UPDATE — **KHÔNG nằm trong phạm vi fix nhưng cùng khối update bị chạm** | Tái ký chọn thẻ phụ (`PointSettingController:1504`) và đăng ký thẻ phụ lúc quá hạn (`UserController:4949`) vẫn ghi `billing_address` của THẺ PHỤ vào hợp đồng; cột nguồn `subcard_bot_contracts.billing_address` nullable nên có thể xoá trắng địa chỉ hợp đồng. **Cần BA chốt** (địa chỉ nào lên hoá đơn khi trả bằng thẻ phụ) |
| D5 | `payment_histories.univapay_transaction_token` / `last_four_card` | Không đổi hành vi | Token đọc từ `$botContract` in-memory = thẻ chính, `last_four_card` = thẻ đã thực thu ⇒ 1 dòng lịch sử mang 2 thẻ khác nhau — đây chính là dấu vết để ops biết kỳ nào thu bù bằng thẻ phụ |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Contract Plan & Payment (FA-031) — thu tiền định kỳ phí tool; màn Chi tiết hợp đồng (đăng ký/đổi thẻ phụ) + tái ký hợp đồng | F1, F2, F3, D1 | High |
| T2 | Payment System Integration (FA-034) — webhook Univapay xử lý kết quả charge của job thu tiền định kỳ (`actionBill=bill_job`) | F1, D1 | High |
| T3 | **CRON thu tiền định kỳ `job:check_auto_payment_univapay`** (Kernel.php:186, daily 06:30) — BỀ MẶT THAY ĐỔI QUAN TRỌNG NHẤT: mỗi kỳ nay luôn thử thẻ chính trước rồi mới thu bù thẻ phụ | F4, D1 | High — Dev nhấn mạnh RETEST PHẢI PHỦ 1 KỲ JOB, không chỉ 3 màn web |
| T4 | Thanh toán lại / đổi trạng thái hợp đồng (FA-031) — `billAgainContract` → `billCardUnivapayContract` (PointSettingController:3061), `changeStatusContract` (:884) | F5, D1 | Medium — trên hợp đồng từng bị ghi đè, nay trừ THẺ CHÍNH thay vì thẻ phụ |
| T5 | Phí vượt hạn mức bạn bè 従量課金 (FA-031) — `HandleBillMaxFriend:132` (nhánh `is_old_bill_max_friend=0`), `acceptBillMaxFriendV2:3387` | F5, D1 | Medium |
| T6 | Thêm slot gói おまとめ/Enterprise (liên quan FS-011 EP一覧) — `paymentAddSlotEnterprise:281` | F5, D1 | Medium |
| T7 | Đổi email tài khoản (đồng bộ Univapay) — `UserService:127-140` PATCH `/tokens/{token}` | F5, D1 | Low-Medium |
| T8 | Lịch sử thanh toán 決済一覧 (FS-009) | D5 | Low — mỗi dòng `payment_histories` mang token THẺ CHÍNH nhưng `last_four_card` của THẺ THỰC THU, cần retest hiển thị màn lịch sử |

---

## 5. Recover data (bổ sung từ Dev — không thuộc 4 mục chuẩn nhưng bắt buộc đọc trước khi test)

⚠ **CÓ** — Hợp đồng nào đã bị ghi đè trước khi có fix thì vẫn đang trỏ token thẻ phụ, **fix không tự sửa dữ liệu cũ**.

Query rà hợp đồng bị lệch:
```sql
SELECT bc.id, bc.univa_last_four_card, s.univa_last_four_card
FROM bot_contracts bc
JOIN subcard_bot_contracts s ON s.bot_contract_id = bc.id
WHERE bc.univa_transaction_token = s.univa_transaction_token AND bc.status = 1;
-- thêm điều kiện bc.univa_last_four_card <> s.univa_last_four_card để lấy đúng nhóm bị lệch giữa token và 4 số cuối đang hiển thị
```

LƯU Ý: token thẻ chính cũ đã bị ghi đè nên **KHÔNG phục hồi được từ DB** — phải lấy lại transaction token của thẻ chính từ Univapay theo `bot_contracts.univa_customer_id` (4 số cuối thẻ chính vẫn còn ở `bot_contracts.univa_last_four_card` để đối chiếu), hoặc nhờ khách bấm "thay đổi thẻ thanh toán" đăng ký lại thẻ chính.

Riêng ticket này (thẻ chính 2019 / thẻ phụ 5190) cần ops kiểm hợp đồng của `lme@compass-bodymake.co.jp` theo câu SELECT trên để xác nhận đúng nhóm bị ghi đè trước khi trả lời khách.

Phạm vi: `bot_contracts` (cột `univa_transaction_token`) của các hợp đồng có thẻ phụ và đã từng thu bù bằng thẻ phụ / đăng ký thẻ phụ lúc quá hạn / tái ký bằng thẻ phụ.

## 6. Verify — mức Dev đã đạt được (bổ sung từ Dev)

- **Mức**: lint (chưa chạy test thực tế bằng dữ liệu thật)
- **Lệnh**: `php -l` cho cả 3 file sửa → No syntax errors; `git diff --stat release_step_20260827...ai_fixbug_41762`: 3 file, +23/-7
- **Bằng chứng suy luận (KHÔNG phải kết quả chạy thật)**:
  - `UnivapayPayment::chargeMoneyUnivapayJob` gửi `transaction_token_id=$token` lên `api.univapay.com/charges` — thẻ bị trừ phụ thuộc DUY NHẤT vào token, `customer_id` chỉ nằm trong metadata ⇒ ghi đè token = đổi thẻ bị trừ
  - `BotController::handleCallbackChangeCardSuccess` cố ý KHÔNG ghi thông tin thẻ lên hợp đồng khi `actionBill=change_sub_card` (`$dataUpdate = []`) và khi recontractV2 có `selectCard=4` — bằng chứng thiết kế: thanh toán bằng thẻ phụ không được thay thẻ chính của hợp đồng
  - `PointSettingController::reContractChangeCard` đã có khối "Khac sub-card thi update" (`select_card != 4`) cho lần cập nhật sau charge, nhưng lần cập nhật TRƯỚC charge lại thiếu guard đó
  - Màn đăng ký thẻ phụ ghi rõ: メインカードの決済が失敗した場合に自動的にサブカードで決済を行います (thẻ phụ chỉ dùng khi thẻ chính lỗi)
- **Không kiểm chứng được bằng dữ liệu thật**: MySQL dev `host.docker.internal:3306` Connection refused; hợp đồng của khách nằm ở DB production
- **Rủi ro Dev tự nêu**:
  - Sau fix, hợp đồng có thẻ chính thật sự không dùng được sẽ bị thử-và-lỗi thẻ chính mỗi kỳ rồi mới thu bù thẻ phụ (đúng thiết kế, không tăng `status_payment_fail` vì lần thu bù thành công), nhưng sẽ có thêm request bị từ chối ở Univapay mỗi kỳ
  - Dữ liệu cũ không tự phục hồi (xem mục 5)
  - `extendContract` chọn trả bằng thẻ phụ (dòng ~2201/2225) vẫn thay thẻ chính bằng thẻ phụ — **cố ý để ngoài phạm vi** fix này

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
