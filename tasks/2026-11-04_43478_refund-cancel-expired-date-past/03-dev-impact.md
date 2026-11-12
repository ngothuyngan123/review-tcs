# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Nguồn: Redmine #43478 **không có section "Đánh giá ảnh hưởng" trong Description** — nội dung này nằm trong **4 Journal "Dev handoff"** (xem nguyên văn ở `01-bug-task.md`). File này parse **bản cuối — Journal #146314 (2026-10-21 17:25)** vì nó supersede 3 bản trước (bản 1/2 đặt hạn = thời điểm hoàn — đã bị thay bằng quy tắc trừ 1 kỳ ở bản 3; bản 3 có bug khóa bảng `bots` #3638 — đã fix ở bản 4).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Nguyen Ngoc Hai (assignee Redmine)` — Journal viết bởi `Dev Studio` (AI dev agent) |
| Commit / Pull Request | `<chưa có link PR>` — repo `sns-line`, commit cuối `1ce65d3996c6dbf0b797964d5d4efb3e8607f192` |
| Branch | `ai_studio_fixbug_43478` (nhánh gốc `release_step_20260930_v2` @`d137c1851896`) |
| Ngày submit đánh giá | `2026-10-21` (Journal #146314, 17:25) — bản 1: 2026-10-19, bản 2/3: 2026-10-21 (11:58) |
| Auto-filled | `2026-11-04 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại 4 Journal "Dev handoff" ở `01-bug-task.md` và xác nhận hiểu đúng: (a) quy tắc hạn cuối cùng là **trừ 1 kỳ, trần = thời điểm hoàn** (không phải "= thời điểm hoàn" như bản 1/2); (b) bug khóa bảng #3638 đã được fix ở bản 4.

---

## 1. Nguyên nhân

Ở System Admin 返金管理 (Quản lý hoàn tiền), khi chọn 返金後のプラン (phương án sau khi hoàn) = **解約** (hủy hợp đồng), hàm `Admin\RefundController::rollbackPlan` **chỉ** chuyển hợp đồng sang trạng thái đã hủy (`status=3`, `cancel_by`, `user_id_cancel`, `date_cancel_contract`) — **không** cập nhật `bot_contracts.expired_date_contract` và `bots.expired_date`. Hạn cũ vẫn giữ nguyên ở tương lai.

Hệ quả: khi khách ký lại hợp đồng, callback `recontractV2` (trong `Admin\BotController`) không tính được kỳ mới và không ghi `payment_histories` — vì logic ký lại chỉ kích hoạt khi hạn hiện tại đã ở quá khứ.

Bối cảnh: bản sửa #36143 (25/05/2026) đã thêm tính hạn mới cho các lựa chọn 返金後のプラン khác nhưng **bỏ sót nhánh 解約**.

Mô tả ticket đổi lúc 21/10 → quy tắc hạn chốt cuối: **hạn hiện tại trừ 1 kỳ** (năm nếu bill năm, tháng nếu bill tháng), **trần = thời điểm hoàn** (nếu trừ 1 kỳ vẫn ở tương lai so với lúc hoàn → dùng thời điểm hoàn). Hạn hợp đồng rỗng/dị thường → fallback dùng thời điểm hoàn.

Nguyên nhân phụ phát sinh trong quá trình fix (**bug #3638**, phát hiện ở bản 3): lệnh recover `UPDATE bots ... WHERE id IN (SELECT bot_id FROM bot_slots WHERE bot_contract_id = ?)` — trên MySQL **trước 8.0.21** chạy dạng dependent subquery, khóa toàn bảng `bots`, khiến lệnh timeout nếu có 1 dòng `bots` không liên quan đang bị khóa bởi phiên khác.

## 2. Cách fix

- **`Admin\RefundController::rollbackPlan`** (nhánh 解約): sau khi set `status=3`/`cancel_by`/`date_cancel_contract`, tính hạn mới = hạn hiện tại − 1 kỳ (năm/tháng theo loại bill), chặn trần ở thời điểm hoàn (`min(hạn − 1 kỳ, thời điểm hoàn)` theo hướng không được muộn hơn thời điểm hoàn), ghi vào `bot_contracts.expired_date_contract` **và** `bots.expired_date` (qua `bot_slots`). Hạn rỗng/dị thường → dùng thời điểm hoàn. Báo Chatwork cho đội dev — **chỉ gửi sau khi lưu DB thành công**, lưu lỗi thì không gửi.
- **`app/BotContracts.php`**: thêm 1 hàm tĩnh mới tính hạn lùi 1 kỳ theo loại bill (năm/tháng) + áp trần thời điểm hoàn — tái dùng ở cả `RefundController` và command recover. Không đổi hàm cũ.
- **Command mới `php artisan refund:fix-cancel-expired-date [--dry-run] [--limit=N]`** (`app/Console/Commands/FixRefundCancelExpiredDate.php`): quét hợp đồng đã hoàn tiền 解約 **trước** bản sửa mà vẫn còn hạn ở tương lai, áp cùng quy tắc trừ 1 kỳ/trần thời điểm hoàn. `--dry-run` chỉ in danh sách id + hạn cũ → hạn mới, không ghi. Idempotent (chạy lại ra 0 dòng vì sau khi sửa hạn ≤ thời điểm hoàn thì không còn khớp điều kiện lọc). **Bản 4 fix thêm #3638**: update bảng `bots` theo đúng id bot của hợp đồng (không dùng subquery `WHERE id IN (SELECT ...)`), tránh khóa toàn bảng. Lệnh chỉ chạy tay sau deploy, không lên lịch.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Admin\RefundController::rollbackPlan` (`app/Http/Controllers/Admin/RefundController.php`, +33/−1) | Có — nhánh 解約 tính + ghi hạn mới | Root cause chính của ticket |
| 2 | `app/BotContracts.php` (+31) | Có — thêm hàm tĩnh mới | Hàm dùng chung tính hạn trừ 1 kỳ cho cả màn hoàn tiền và command recover |
| 3 | `app/Console/Commands/FixRefundCancelExpiredDate.php` (233 dòng, file mới) | Có — command recover dữ liệu cũ, bản 4 fix cách update bảng `bots` | Dọn dữ liệu production để lại từ trước bản sửa |
| 4 | Callback ký lại hợp đồng `recontractV2` (`Admin\BotController`) + `BillingService` | Không đổi code — Dev confirm đã check | Hạn đã lùi về quá khứ sẽ kích hoạt tính kỳ mới + ghi `payment_histories`; ký lại trong 7 ngày sau hạn mới thì nối tiếp chu kỳ cũ |
| 5 | Job `job:check_auto_payment_univapay` (06:30) — phần xóa hợp đồng đã hủy | Không đổi code — hành vi thay đổi gián tiếp | Hợp đồng hoàn tiền 解約 chưa gắn bot bị xóa ở lần chạy **kế tiếp** (trước đây phải đợi tới hạn cũ ở tương lai) |
| 6 | Job `handle:bill_stripe` (07:00) | Không đổi code — hành vi thay đổi gián tiếp | Thu tiền định kỳ item của bot bị hoàn tiền 解約 dừng ngay hoặc chậm nhất 7 ngày (thay vì chờ tới hạn cũ) |
| 7 | Thu tiền gói tự động (chỉ query hợp đồng `status=1`) | Không đổi — Dev confirm không bị đụng | Không trừ tiền lại hợp đồng vừa hoàn (hợp đồng đã `status=3`) |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Admin\RefundController::rollbackPlan` (nhánh 解約) | `app/Http/Controllers/Admin/RefundController.php` | Direct | Root cause fix — tính + ghi hạn mới (trừ 1 kỳ, trần = thời điểm hoàn); fallback hạn rỗng/dị thường dùng thời điểm hoàn + báo Chatwork sau khi lưu |
| F2 | Hàm tĩnh mới tính hạn trừ 1 kỳ | `app/BotContracts.php` | Direct | Dùng chung cho F1 và F3; chỉ thêm hàm mới, không đổi hàm cũ |
| F3 | Command `refund:fix-cancel-expired-date` | `app/Console/Commands/FixRefundCancelExpiredDate.php` | Direct | Recover dữ liệu production cũ; bản 4 sửa cách update `bots` (fix #3638 khóa bảng) |
| F4 | Callback ký lại hợp đồng `recontractV2` / `BillingService` | `Admin\BotController` | Indirect | Hạn đã lùi về quá khứ ⇒ tính kỳ mới + ghi `payment_histories`; ký lại trong 7 ngày sau hạn mới nối tiếp chu kỳ cũ, quá 7 ngày tính từ ngày ký |
| F5 | Job dọn hợp đồng đã hủy | `job:check_auto_payment_univapay` (06:30) | Indirect | Hợp đồng hoàn tiền 解約 chưa gắn bot bị xóa sớm hơn (lần chạy kế tiếp thay vì đợi hạn cũ) |
| F6 | Job thu tiền định kỳ Stripe | `handle:bill_stripe` (07:00) | Indirect | Dừng thu tiền item của bot hoàn tiền 解約 ngay hoặc chậm nhất 7 ngày |
| F7 | Màn hiển thị hạn hợp đồng/bot đã hủy | Admin + trang hợp đồng khách | Indirect | Hiện ngày quá khứ thay vì ngày tương lai |
| F8 | Module job đọc `bots.expired_date` | `linect-service` | Indirect | Bot hết hạn sớm hơn; **Dev tự ghi nhận "hành vi gửi tin chưa kiểm chứng chi tiết"** — cần QA chủ động test thêm, không coi là đã check |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_contracts.expired_date_contract` | UPDATE | Hợp đồng hoàn tiền 解約 (mới + recover cũ): lùi về hạn hiện tại − 1 kỳ, trần = thời điểm hoàn; fallback thời điểm hoàn nếu hạn rỗng/dị thường |
| D2 | `bots.expired_date` | UPDATE | Cùng quy tắc D1, áp cho bot gắn qua `bot_slots.bot_contract_id`; bản 4 update theo đúng id bot (không còn subquery toàn bảng) |
| D3 | `payment_histories` | CREATE (gián tiếp) | Khi khách ký lại sau khi hạn đã lùi về quá khứ — ghi dòng thanh toán mới (mục tiêu chính của ticket) |
| D4 | Dữ liệu production cũ (hợp đồng hoàn tiền 解約 trước bản sửa, hạn còn ở tương lai) | RECOVER (UPDATE qua command) | Phạm vi: từ khi có lựa chọn 解約 trên màn hoàn tiền (commit 17/04/2026) tới lúc deploy bản sửa. **Cần backup** `bk_43478_bot_contracts` / `bk_43478_bots` trước khi chạy thật; lệnh idempotent |
| D5 | Không gửi gì tới khách (Dev confirm) | — | Chỉ đổi ngày hết hạn của hợp đồng đã hoàn tiền + đã hủy; hợp đồng đã trả tiền kỳ mới không bị đụng |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | System Admin 返金管理 › 新規作成 (tạo mới hoàn tiền, chọn 解約) | F1, D1, D2 | Medium — thay đổi hành vi ngay khi hoàn tiền; các lựa chọn 返金後のプラン khác Dev confirm "không đổi" nhưng cần verify không regress |
| T2 | Ký lại hợp đồng (再契約/recontractV2) sau hoàn tiền 解約 | F4, D1, D2, D3 | **High** — mục tiêu chính của ticket; có nhánh "ký lại trong 7 ngày sau hạn mới" vs "quá 7 ngày" cần phân biệt |
| T3 | Job dọn hợp đồng hủy không bot (`check_auto_payment_univapay` 06:30) | F5 | Medium — thời điểm xóa hợp đồng/slot trống đổi sớm hơn |
| T4 | Job thu tiền định kỳ Stripe (`handle:bill_stripe` 07:00) | F6 | Medium — dừng thu tiền sớm hơn với bot bị hoàn 解約 |
| T5 | Lệnh recover dữ liệu cũ `refund:fix-cancel-expired-date` | F3, D4 | **High** — ghi đè dữ liệu khách thật trên production; cần dry-run + backup; có fix bug khóa bảng #3638 (MySQL < 8.0.21) chưa chạy thật trên prod |
| T6 | Module job `linect-service` đọc `bots.expired_date` (gửi tin) | F8 | **Chưa rõ** — Dev tự nhận "chưa kiểm chứng chi tiết", QA cần tự test, không coi là RISK thấp mặc định |
| T7 | Màn hiển thị hạn hợp đồng/bot đã hủy (admin + trang khách) | F7 | Low |
| T8 | Ticket cha #43426 (hợp đồng 99040, đã ký lại khi hạn cũ còn ở tương lai) | D4 (loại trừ) | **Ngoài phạm vi #43478** — lệnh recover không đụng, Dev xác nhận xử lý tay riêng; không đẻ TC ở đây |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
