# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43478 — Khi refund, plan sau khi hoàn là 解約 (đã hủy), update expired_date contract về ngày expired_date quá khứ` |
| Module / Màn hình | `System Admin 返金管理 (Quản lý hoàn tiền) › 新規作成 (tạo mới hoàn tiền) — lựa chọn 返金後のプラン (phương án sau khi hoàn) = 解約 (hủy hợp đồng)` |

## Mô tả bug (bản dịch tiếng Việt)

Khi thực hiện refund (hoàn tiền) và chọn 返金後のプラン (phương án sau khi hoàn) là 解約 (hủy hợp đồng), hệ thống không cập nhật `expired_date` trong bảng `bot_contracts` (cột `expired_date_contract`) và `expired_date` trong bảng `bots` về ngày quá khứ tương ứng — hạn cũ vẫn giữ nguyên ở tương lai.

Ví dụ:
- Hợp đồng bill theo năm → `expired_date` phải = `expired_date` hiện tại trừ 1 năm.
- Hợp đồng bill theo tháng → `expired_date` phải = `expired_date` hiện tại trừ 1 tháng.

<!-- Redmine không có section "Tái hiện bug" riêng (không có Steps/Expected/Actual tách bạch) — mô tả trên là nguyên văn description của issue, đã dịch sát. -->

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có file đính kèm trên Redmine. -->

## Ghi chú thêm của Leader

⚠️ Bug không có "Tái hiện bug" riêng trong Redmine — root cause + cách fix đã được Dev confirm trực tiếp qua 4 bản "Dev handoff" ở Journal (không qua Description). File `03-dev-impact.md` dùng **bản cuối (Journal #146314, 2026-10-21 17:25)** làm nguồn chính vì nó supersede 3 bản trước — 3 bản cũ giữ lại trong Journal note bên dưới để tham chiếu lịch sử thay đổi yêu cầu.

⚠️ **Yêu cầu đổi giữa chừng (quan trọng cho QA)**: bản 1/2 (19/10) fix đặt hạn hợp đồng/bot = **thời điểm hoàn tiền**. Mô tả ticket đổi lúc 21/10 → bản 3/4 đổi quy tắc thành **hạn hiện tại trừ 1 kỳ (năm hoặc tháng), KHÔNG muộn hơn thời điểm hoàn** (nếu trừ 1 kỳ vẫn ở tương lai so với thời điểm hoàn thì dùng thời điểm hoàn làm trần). Hạn hợp đồng rỗng hoặc dị thường → fallback dùng thời điểm hoàn + báo Chatwork cho đội dev (chỉ gửi sau khi lưu DB thành công).

⚠️ **Bug phụ phát sinh trong quá trình fix (#3638)**: bản 3 dùng `UPDATE bots ... WHERE id IN (SELECT bot_id FROM bot_slots WHERE bot_contract_id = ?)` — trên MySQL **trước 8.0.21** câu này chạy dạng dependent subquery, khóa toàn bảng `bots`. Bản 4 (cuối) đã sửa thành update theo đúng id bot của hợp đồng, không khóa cả bảng. Cần biết **version MySQL thật của môi trường test/prod** để quyết định có cần test riêng kịch bản lock này không (ENV-*).

⚠️ Liên quan ticket cha **#43426** (hợp đồng 99040): khách đã ký lại hợp đồng khi hạn cũ (bug) còn ở tương lai → thiếu dòng thanh toán ngày 17/10. Lệnh recover **KHÔNG** đụng hợp đồng này (điều kiện chọn loại trừ hợp đồng đã ký lại) — ticket cha xử lý tay riêng, ngoài phạm vi #43478.

⚠️ Status Redmine hiện tại: **Fix done - Đợi test**.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Hợp đồng dùng để điều tra (DB thật — Dev dùng làm acceptance set cho dry-run) | `1022, 1922` → **phải được** lệnh `refund:fix-cancel-expired-date` chọn (hoàn tiền 解約, chưa ký lại, hạn còn ở tương lai) |
| Hợp đồng loại trừ (dry-run KHÔNG được chọn) | `1893` — đã ký lại sau hoàn; `1571` — hạn đã qua (≤ thời điểm hoàn) |
| Ticket liên quan (xử lý tay, ngoài phạm vi) | `#43426` — hợp đồng `99040`, đã ký lại khi hạn cũ còn ở tương lai, thiếu dòng thanh toán 17/10 |
| Lệnh recover dữ liệu production | `php artisan refund:fix-cancel-expired-date --dry-run` (xem danh sách id + hạn cũ → hạn mới) rồi `php artisan refund:fix-cancel-expired-date` (chạy thật) — **chỉ chạy tay sau deploy**, không lên lịch; idempotent (chạy lại ra 0 dòng) |
| Backup trước khi recover | `bk_43478_bot_contracts` (id, expired_date_contract), `bk_43478_bots` (id, expired_date) — tạo từ danh sách id của bước dry-run |

## Journal / note từ Redmine (nguyên văn)

<!-- 4 journal Dev handoff đều có nội dung điều tra/cách fix giá trị — giữ nguyên văn để trace lịch sử thay đổi yêu cầu. Journal #146314 (bản cuối) là nguồn chính cho 03-dev-impact.md. -->

**Journal #145402 — Dev Studio — 2026-10-19:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Ở System Admin 返金管理, khi 返金後のプラン = 解約, hàm `Admin\RefundController::rollbackPlan` ghi đè mảng cập nhật chỉ còn status=3, cancel_by, user_id_cancel và date_cancel_contract, nên không cập nhật `bot_contracts.expired_date_contract` và `bots.expired_date`. Hợp đồng đã hoàn tiền vẫn giữ hạn cũ ở tương lai. Bản sửa #36143 (25/05/2026) đã thêm tính hạn mới cho các lựa chọn khác nhưng bỏ sót 解約. Hạn còn ở tương lai khiến callback ký lại (recontractV2) không tính kỳ mới và không ghi payment_histories.

Hướng sửa:
- D-1 Hoàn tiền sang 解約 thì đặt hạn hợp đồng và hạn bot về thời điểm hoàn
- D-2 Command recover refund:fix-cancel-expired-date có chế độ dry-run

Ảnh hưởng / rủi ro:
Chỉ đổi luồng System Admin 返金管理 khi chọn 解約: hợp đồng và bot hết hạn ngay tại thời điểm hoàn, nên khi khách ký lại sẽ được tính kỳ mới và ghi dòng thanh toán. Cần test lại các lựa chọn gói sau hoàn tiền khác để chắc không đổi. Lệnh recover sửa dữ liệu khách thật nên phải chạy dry-run trước.
```

**Journal #145417 — Dev Studio — 2026-10-19 (bị thay thế bởi #146060/#146314 — quy tắc hạn = thời điểm hoàn, KHÔNG còn đúng với yêu cầu cuối):**

```
Dev handoff — 19/10 17:40 · nhánh ai_studio_fixbug_43478

Nội dung thay đổi:
- 返金管理 › 新規作成, lựa chọn 解約: hợp đồng chuyển 解約 với ngày huỷ = ngày hết hạn = thời điểm hoàn; bot gắn hợp đồng hết hạn ngay tại thời điểm hoàn.
- Các lựa chọn 返金後のプラン khác: không đổi.
- Command mới php artisan refund:fix-cancel-expired-date [--dry-run] [--limit=N].

File đã sửa (php-web):
  .../Commands/FixRefundCancelExpiredDate.php        | 196 +++++++++++++++++++++
  app/Http/Controllers/Admin/RefundController.php    |   6 +-

Branch: ai_studio_fixbug_43478
- sns-line: ai_studio_fixbug_43478 (nhánh gốc release_step_20260930_v2 @d137c1851896, commit 29c2ad2572e10b73da91e067eaa93ea7cec59f67)
```

**Journal #146060 — Dev Studio — 2026-10-21 (đổi quy tắc hạn theo mô tả ticket mới; bị thay thế bởi #146314 — fix thêm bug khóa bảng #3638):**

```
Dev handoff — 21/10 11:58 · nhánh ai_studio_fixbug_43478

Nguyên nhân:
Mô tả mới của ticket (21/10) yêu cầu đưa hạn về ngày quá khứ bằng hạn hiện tại trừ 1 kỳ (năm hoặc tháng), thay cho thời điểm hoàn như bản đã giao.

Nội dung thay đổi:
- 返金管理 › 新規作成, lựa chọn 解約: hợp đồng chuyển 解約 (ngày huỷ = lúc hoàn); hạn hợp đồng và hạn bot = hạn hiện tại −1 năm (bill năm) hoặc −1 tháng (bill tháng), không muộn hơn lúc hoàn.
- Hạn hợp đồng rỗng hoặc kỳ lạ: dùng lúc hoàn và báo Chatwork cho đội dev.
- Command php artisan refund:fix-cancel-expired-date [--dry-run] [--limit=N]: lùi hạn theo cùng quy tắc (trần là thời điểm hoàn).

File đã sửa (php-web):
  app/BotContracts.php                               |  31 +++
  .../Commands/FixRefundCancelExpiredDate.php        | 224 +++++++++++++++++++++
  app/Http/Controllers/Admin/RefundController.php    |  22 +-

Branch: ai_studio_fixbug_43478
- sns-line: ai_studio_fixbug_43478 (nhánh gốc release_step_20260930_v2 @d137c1851896, commit 4ee41840d7ea938c1f468c42e830b88d7b1f1022)
```

**Journal #146314 — Dev Studio — 2026-10-21 (bản cuối — dùng làm nguồn cho 03-dev-impact.md):**

```
Dev handoff — 21/10 17:25 · nhánh ai_studio_fixbug_43478

Nguyên nhân:
Lệnh recover refund:fix-cancel-expired-date cập nhật bot bằng `UPDATE bots ... WHERE id IN (SELECT bot_id FROM bot_slots WHERE bot_contract_id = ?)` trong transaction của từng hợp đồng. Trên MySQL trước 8.0.21, câu này chạy dạng subquery phụ thuộc: nó quét và khoá toàn bộ bảng bots. Vì vậy chỉ một dòng bots không liên quan bị khoá cũng làm lệnh hết thời gian chờ và dừng ngay ở hợp đồng đầu tiên. Nguyên nhân gốc của ticket (hoàn tiền 解約 không đổi hạn) và quy tắc hạn trừ 1 kỳ giữ như bản 3.

Nội dung thay đổi:
- 返金管理 › 新規作成, lựa chọn 解約: hợp đồng chuyển 解約 (ngày huỷ = lúc hoàn). Hạn hợp đồng và hạn bot = hạn hiện tại −1 năm (bill năm) hoặc −1 tháng (bill tháng), không muộn hơn lúc hoàn.
- Hạn hợp đồng rỗng hoặc kỳ lạ: dùng lúc hoàn. Báo Chatwork cho đội dev chỉ gửi sau khi lưu thành công; lưu lỗi thì không gửi.
- Các lựa chọn 返金後のプラン khác: không đổi.
- Command php artisan refund:fix-cancel-expired-date [--dry-run] [--limit=N]: lùi hạn theo cùng quy tắc (trần là thời điểm hoàn) cho các hợp đồng đã hoàn tiền 解約 trước bản sửa mà vẫn giữ hạn cũ ở tương lai. Bot được cập nhật theo id, chỉ khoá đúng bot của hợp đồng (bug #3638). Chỉ chạy tay.

File đã sửa (php-web):
  app/BotContracts.php                               |  31 +++
  .../Commands/FixRefundCancelExpiredDate.php        | 233 +++++++++++++++++++++
  app/Http/Controllers/Admin/RefundController.php    |  33 ++-
  3 files changed, 296 insertions(+), 1 deletion(-)

Đánh giá ảnh hưởng — Rủi ro trung bình: Phần sửa ở màn admin nhỏ và harness phủ đủ nhánh. Nhưng thay đổi đụng hạn hợp đồng/bot, command recover ghi đè dữ liệu khách thật, và hành vi khoá trên MySQL 5.6 chưa chạy trên DB thật.
- Callback ký lại hợp đồng (recontract trong Admin\BotController) và BillingService: hạn đã qua ⇒ tính kỳ mới và ghi lịch sử thanh toán. Ký lại trong 7 ngày sau hạn mới thì nối tiếp chu kỳ cũ.
- Job job:check_auto_payment_univapay (06:30), phần xoá hợp đồng đã huỷ: hợp đồng hoàn tiền 解約 chưa gắn bot bị xoá ngay lần chạy sau.
- Job handle:bill_stripe (07:00): thu tiền định kỳ item của bot bị hoàn tiền 解約 dừng ngay hoặc sau tối đa 7 ngày.
- Bảng bots khi chạy command recover: các luồng ghi bots khác (job, màn admin) không còn bị chặn bởi khoá toàn bảng; chỉ bot của hợp đồng đang xử lý bị khoá trong thời gian ngắn.
- Model BotContracts: chỉ thêm hàm tĩnh mới, không đổi hàm cũ.
- Màn hiển thị hạn hợp đồng/bot đã huỷ (admin, trang hợp đồng của khách): hiện ngày quá khứ.
- Module job đọc bots.expired_date: bot hết hạn ngay sau khi hoàn tiền 解約 hoặc sau khi recover.

Migration / thay đổi dữ liệu:
- [Backup · Sau deploy] Sao lưu hạn của các hợp đồng/bot mà command recover sẽ sửa: Sau khi chạy dry-run, lấy danh sách id rồi chạy: CREATE TABLE bk_43478_bot_contracts AS SELECT id, expired_date_contract FROM bot_contracts WHERE id IN (<ids>); CREATE TABLE bk_43478_bots AS SELECT b.id, b.expired_date FROM bots b JOIN bot_slots bs ON bs.bot_id = b.id WHERE bs.bot_contract_id IN (<ids>);
- [Recover · Sau deploy] Lùi expired_date_contract và bots.expired_date (−1 kỳ, trần là thời điểm hoàn) cho hợp đồng đã hoàn tiền 解約 trước bản sửa: php artisan refund:fix-cancel-expired-date --dry-run (đối chiếu id và hạn mới, rồi làm bước backup) php artisan refund:fix-cancel-expired-date

Recover dữ liệu: Cần recover — Việc recover dữ liệu cũ vẫn cần như bản 3. Lệnh recover chưa được chạy trên production, nên lỗi khoá của #3638 chưa làm hỏng dữ liệu nào.
- Ảnh hưởng: bot_contracts.expired_date_contract của hợp đồng status=3, cancel_by=2 đã hoàn tiền 解約 vẫn còn hạn ở tương lai
- Ảnh hưởng: bots.expired_date của bot gắn slot các hợp đồng đó
- Khoảng thời gian: Từ khi có lựa chọn 解約 trên màn hoàn tiền (các commit ngày 17/04/2026) tới khi bản sửa được deploy
- Cách recover: Dùng lệnh refund:fix-cancel-expired-date đã sửa ở D-10. Chạy --dry-run và sao lưu hạn trước, rồi mới chạy thật. Lệnh idempotent: lần sau không chọn lại hợp đồng đã sửa.
- Ảnh hưởng tới khách: Không gửi gì tới khách. Chỉ đổi ngày hết hạn của hợp đồng đã hoàn tiền và đã huỷ. Sau bản sửa, lệnh không còn khoá cả bảng bots khi chạy.

Lưu ý khi deploy:
- Không cần xoá cache, không phụ thuộc thứ tự deploy với module khác.
- Command chỉ chạy tay sau deploy, không lên lịch; nên chạy giờ thấp điểm, chạy --dry-run và backup trước.

Việc cần người làm thêm (ngoài phạm vi task):
- Sau khi deploy: sao lưu hạn của các hợp đồng và bot trong danh sách dry-run, chạy `php artisan refund:fix-cancel-expired-date --dry-run`, rồi người phụ trách quyết định chạy thật.
- Ticket cha #43426 (hợp đồng 99040, đã ký lại): xử lý tay hạn hợp đồng và dòng thanh toán thiếu ngày 17/10.
- Hợp đồng đã hoàn tiền 解約 rồi sau đó bị huỷ lại bằng đường khác sẽ không được lệnh chọn. Gặp trường hợp như vậy thì xử lý tay.
- Đính chính báo cáo vòng 3: harness khi đó đạt 49/49 case chứ không phải 50/50 như đã ghi.

Điểm cần test:
- Chạy lại kịch bản #3638 trên MySQL 5.6, phiên khác giữ khoá BE2: E1/BE1 được sửa, lệnh dừng ở E2 với exit 1. Nhả khoá rồi chạy lại: chỉ xử lý E2.
- EXPLAIN câu UPDATE bots: truy cập theo PRIMARY, không còn DEPENDENT SUBQUERY.
- Hợp đồng không gắn bot: lệnh chạy bình thường, số bot cập nhật = 0.
- Hoàn tiền 解約 với hạn hợp đồng rỗng: lưu thành công và Chatwork gửi sau khi lưu; lưu lỗi thì không gửi.
- Command với hợp đồng có 2 bot hoặc slot trùng bot: cả 2 bot được lùi hạn, mỗi bot 1 lần.
- Giữ các điểm kiểm thử bản 3: năm −1 năm, tháng −1 tháng (31/3 ⇒ 28/2 hoặc 29/2), chặn trần ở lúc hoàn, ký lại sau hoàn có dòng lịch sử thanh toán, các lựa chọn 返金後のプラン khác không đổi; command dry-run, chạy 2 lần (lần 2 = 0).

Branch: ai_studio_fixbug_43478
- sns-line: ai_studio_fixbug_43478 (nhánh gốc release_step_20260930_v2 @d137c1851896, commit 1ce65d3996c6dbf0b797964d5d4efb3e8607f192)
```
