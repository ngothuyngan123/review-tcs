# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT KHÔNG ĐÚNG FORMAT CHUẨN**: Redmine #41061 **không có** section "Đánh giá ảnh hưởng phía dev" theo format chuẩn (1. Nguyên nhân / 2. Cách fix / 3. Function caller đã check / 4.1-4.2-4.3). Ticket là **task Feature**, Dev chỉ để lại **Journal #139307** — báo cáo tiến độ dạng AI-dev-workflow (không phải đánh giá viết tay theo template) — + **Journal #144586** (1 dòng, không rõ nghĩa đầy đủ). Nội dung dưới đây là **best-effort mapping** của `/new-task` từ Journal #139307 + đối chiếu `dev_impact`/`requirements` của MCP LME TEST STUDIO (task #336) — **PHẢI được Dev/Leader xác nhận lại** trước khi dùng làm input chính thức cho `/write-tc` hoặc `/review-tc`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Do Van Tu TuDV (`issue.assigned_to`) — báo cáo sinh bởi workflow AI dev, branch `ai-feature-41061` |
| Commit / Pull Request | Không có link PR trong Redmine. Commit trên branch: `405bdf673e`, `814bbe9857`, `43249e1563`, `ef2ee7420f` (base `131bde0f22`) |
| Branch | `ai-feature-41061` |
| Ngày submit đánh giá | 2026-09-29 (Journal #139307) |
| Auto-filled | 2026-10-16 by `/new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ do input không đúng format chuẩn (xem cảnh báo đầu file), checkbox này **đặc biệt quan trọng** — phải đọc lại Journal nguyên văn ở `01-bug-task.md` + hỏi Dev hiện trạng (2 bug BLOCKING + merge conflict với #41101 đã xử lý tới đâu) trước khi tick.

---

## 1. Nguyên nhân

<!-- Task Feature, không phải bug fix — không có "nguyên nhân lỗi". Mục này diễn giải LÝ DO cần feature. -->

Không áp dụng theo nghĩa "root cause bug". **Lý do cần feature** (từ Description §1): hiện tại khi hợp đồng năm (年間一括払い) bằng 銀行振込 (chuyển khoản) UnivaPay đến hạn gia hạn (trước 1 tháng), hệ thống **chưa** tự động gửi thông tin tài khoản chuyển khoản để khách thực hiện gia hạn → cần bổ sung email `MAIL-01` tự động trong luồng charge chuyển khoản đã có (Phase 3 không đổi).

## 2. Cách fix (triển khai)

<!-- Từ Journal ■1 ĐÃ LÀM -->

- MAIL-01 「銀行振込 契約更新案内メール」 — gửi 1 mail cho mỗi **kỳ gia hạn** của hợp đồng năm trả bằng UnivaPay 銀行振込.
- Migration thêm 4 cột cờ `renewal_mail_*` trên `bot_contracts` (QT-002 phương án B — **không** tạo bảng hàng đợi riêng, khác cách làm của task anh em #41101).
- `ContractRenewalMailRepository` + Interface + binding: selector (§4), claim nguyên tử theo kỳ, cơ chế gỡ claim mồ côi (`releaseStaleClaims`).
- `ContractRenewalTransferMailService`: guard G-01…G-06, dựng 11 biến, chống gửi trùng theo **kỳ hợp đồng** (`renewal_mail_sent_period`).
- Kênh gửi `ContractRenewalTransferMail` qua SMTP `ADMIN_MAIL_*` (QT-004 A).
- Template `emails.contract_renewal_transfer` — nguyên văn khách duyệt (11 biến + 3 giá trị hardcode + 8 mục 注意事項).
- Móc `dispatchPending()` vào `AutoPaymentJobUnivapay` (cuối lượt 06:30) và `recover:RecoverUpdateInfoUnivapay` (mỗi 5 phút); **không đụng Phase 3**.
- Feature flag `RENEWAL_TRANSFER_MAIL_ENABLED` (mặc định `false`) + `RENEWAL_TRANSFER_MAIL_EFFECTIVE_DATE` (thiếu = không gửi) — mặc định AN TOÀN cho rollout (D-15).
- BA đã REVERT phạm vi 1 lần (D-21): thu từ 6 luồng về 1 luồng gia hạn, bỏ 4 biến thể nội dung, đổi khoá chống trùng từ `univa_charge_id` sang theo **kỳ** (`renewal_mail_sent_period`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Từ Journal ■2 (commit list) + ■5 (ripple review) -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AutoPaymentJobUnivapay.php` | Gọi `dispatchPending()` cuối `handle()` | Trigger chính (job 06:30) — Phase 3 (charge) không đổi |
| 2 | `RecoverUpdateInfoUnivapay.php` | Gọi `dispatchPending()` sau khi cập nhật bank info | Trigger phụ (job 5 phút) — ⚠️ **cùng file task anh em #41101 cũng sửa** |
| 3 | `ContractRenewalMailRepository(Interface).php` + `ContractRenewalTransferMailService.php` | File mới, sửa nhiều lượt (4 commit) | Core logic selector/claim/send/guard |
| 4 | `ContractRenewalTransferMail.php` + `emails/contract_renewal_transfer.blade.php` | File mới | Mail + template — render bằng `white-space:pre-wrap` (D-02), chưa rõ có bị vỡ layout Outlook như bug FE-01 của #41101 không — **chưa thấy Journal #41061 tự nhận bug này, cần hỏi Dev** |
| 5 | `Admin\BotController@paymentBotSlot` / `@paymentBotSlotV2` / `@handleCallbackPaymentCardSuccess` | **KHÔNG sửa**, nhưng cùng ghi `bot_contracts.status_payment=5` mà selector MAIL-01 dùng để nhận diện hàng đợi | ⚠️ **BLOCKING #1** — không có discriminator phân biệt "charge do job tạo" vs "charge do UI tạo" (xem 4.3) |
| 6 | `request_get_bank_transfer` (writer `status=2` ở các endpoint UI: `PointSettingController`...) | **KHÔNG sửa** | ⚠️ **BLOCKING #2** — `getOpenTransferRequest()` không neo theo kỳ (xem 4.3) |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ContractRenewalTransferMailService::dispatchPending()` | `app/Services/ContractRenewalTransferMailService.php` | Direct | Entry point: gỡ claim kẹt → quét lô 200 → claim → guard G-01..G-06 → dựng 11 biến → gửi SMTP → ghi cờ |
| F2 | `ContractRenewalMailRepository` (selector, claim, release, `getOpenTransferRequest`, `releaseStaleClaims`) | `app/Repositories/Eloquents/ContractRenewalMailRepository.php` | Direct, nhưng **impact gián tiếp rộng** | ⚠️ BLOCKING #1 [HIGH]: selector dòng 44-83 chỉ lọc `status_payment=5`, không phân biệt nguồn ghi (job vs UI) |
| F3 | `AutoPaymentJobUnivapay::handle()` | `app/Console/Commands/AutoPaymentJobUnivapay.php` | Direct | Thêm gọi `dispatchPending()` cuối lượt; Phase 3 (charge gốc, dòng 1125-1220) không đổi code nhưng **là nguồn dữ liệu** mà selector + `${amount}` phụ thuộc |
| F4 | `RecoverUpdateInfoUnivapay::handle()` | `app/Console/Commands/RecoverUpdateInfoUnivapay.php` | Direct | Thêm gọi `dispatchPending()`; **cùng file task anh em #41101 sửa** → rủi ro merge |
| F5 | `Admin\BotController@paymentBotSlot` / `@paymentBotSlotV2` / `@handleCallbackPaymentCardSuccess` | `app/Http/Controllers/Admin/BotController.php` | Indirect (không sửa code, nhưng là nguồn ghi dữ liệu selector đọc) | ⚠️ BLOCKING #1: 3 đường UI này cũng ghi `status_payment=5` → có thể bị selector MAIL-01 hiểu nhầm là hàng đợi gia hạn |
| F6 | `countByStatus()` | Interface + Repository | Dead code | Khai báo đủ nhưng không có caller nào — yêu cầu TD §7 "theo dõi tồn đọng renewal_mail_status=0" chưa có command/endpoint đọc |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bot_contracts.renewal_mail_status` / `renewal_mail_sent_period` / `renewal_mail_attempts` / `renewal_mail_last_reason` | MIGRATE (ALTER, 4 cột mới, **không index**) | Bảng nóng billing; migration `Schema::table->after()` buộc MySQL rebuild bảng (mất `ALGORITHM=INSTANT`) — **chưa verify đã chạy trên DB dev** |
| D2 | `bot_contracts.status_payment` (đọc, không sửa) | READ | Selector MAIL-01 dựa cột này = 5; cột dùng chung với 3 đường UI khác (xem F5) |
| D3 | `request_get_bank_transfer` (bảng dùng chung) | READ (qua `getOpenTransferRequest()`) | ⚠️ BLOCKING #2: lấy row mới nhất `status<>2`, không neo theo kỳ → `${amount}` + `${date}` có thể là của kỳ cũ |
| D4 | `RENEWAL_TRANSFER_MAIL_ENABLED` / `RENEWAL_TRANSFER_MAIL_EFFECTIVE_DATE` (env/config) | CREATE | 2 feature flag rollout — **không có trong `.env.example` / `config/`**, đọc bằng `env()` runtime → rủi ro `config:cache` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Gia hạn hợp đồng năm chuyển khoản (`admin/detail-contract`, FA-031) | F1, F2, D1 | High (feature chính của task) |
| T2 | **3 flow thanh toán thẻ/callback trên UI** (`paymentBotSlot`, `paymentBotSlotV2`, `handleCallbackPaymentCardSuccess`) | F5, D2 — BLOCKING #1 | **High — CHƯA xác nhận đã fix.** Nếu không có discriminator, charge tạo từ UI có thể bị selector MAIL-01 hiểu nhầm → `resolveAmount` null → defer 10 lần → `markFailed` + cảnh báo Chatwork sai |
| T3 | Số tiền (`${amount}`) + hạn chuyển khoản (`${date}`) trong mail MAIL-01 | F2, D3 — BLOCKING #2 | **High — CHƯA xác nhận đã fix.** Có thể in sai số tiền/hạn của **kỳ trước** nếu `request_get_bank_transfer` không được tạo row mới cho kỳ hiện tại |
| T4 | Job thanh toán tự động UnivaPay (`AutoPaymentJobUnivapay` Phase 3 — charge/auto-cancel) | F3 | Medium — Journal khẳng định "KHÔNG đụng Phase 3" nhưng `dispatchPending()` chạy **cuối cùng trong cùng request**, lỗi `\Error`/`\TypeError` (không phải `\Exception`) sẽ thoát ra sau khi tiền đã xử lý xong (rủi ro thấp theo Dev tự đánh giá) |
| T5 | Mail sự cố khác cùng lượt cron (`SendMailUpdateAccountNumber` — 振込先口座の発行完了) | Journal ■5 warning | Medium — có thể gửi 2 mail cho cùng user, cùng thông tin ngân hàng, cách nhau vài giây trong cùng lượt `recover:RecoverUpdateInfoUnivapay` |
| T6 | Task anh em cùng sprint **#41101** (mail đăng ký mới — お申し込み) — đụng merge cùng `RecoverUpdateInfoUnivapay.php` + `Kernel.php` | Journal ■5 warning + 03-dev-impact #41101 mục T4 | High — rủi ro merge sai làm mất tính năng âm thầm (của 1 trong 2 task); #41101 đã audit chi tiết hơn (xem file đó) |
| T7 | Hiệu năng/lock bảng `bot_contracts` khi `releaseStaleClaims()` | D1 (không index) | Medium — `UPDATE ... WHERE renewal_mail_status = 1` full scan + row lock trên bảng billing nóng, chạy mỗi 5 phút + 1 lượt 06:30, không có `withoutOverlapping()` ở cron `RecoverUpdateInfoUnivapay` |
| T8 | Observability §7 — đếm hợp đồng theo `renewal_mail_status` mỗi ngày (TD-20) | F6 (dead code) | Low — yêu cầu metric chưa có nơi đọc, không chặn release nhưng Leader cần biết để không kỳ vọng dashboard có sẵn |

> **2 BUG mức BLOCKING do AI review nội bộ phát hiện 29/09/2026, CHƯA rõ tình trạng fix hiện tại** (ticket vẫn "New" tại 2026-10-16, không có journal nào xác nhận đã xử lý sau 29/09 ngoài 1 dòng không rõ nghĩa của Journal #144586 15/10): selector `status_payment=5` thiếu discriminator (T2) và `${amount}`/`${date}` không neo theo kỳ (T3). Theo RULE-11, AI-review nội bộ không phải bằng chứng đã fix — **phải hỏi Dev xác nhận trạng thái 2 bug này trước khi viết TC kết luận Pass/Fail**. Khớp với Studio: task #336 có `aiResult=fail`, 1 TC fail (`NEW-56` — chưa gắn ticket bug, nội dung về màn "お支払い方法の変更" giữ nguyên, có vẻ KHÔNG phải cùng 2 BLOCKING này) + 5 TC chưa chạy, trong đó `NEW-58` ("Còn sót yêu cầu chuyển khoản kỳ trước chưa đóng") đúng là TC nhằm vào BLOCKING #2 — **ưu tiên hỏi trạng thái TC này trước**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân / lý do feature) rõ ràng, đủ chi tiết để viết TC verify
- [ ] Mục 2 (cách implement) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót — **đặc biệt 3 flow UI ghi `status_payment=5` + task anh em #41101**)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC — **ưu tiên hỏi trạng thái 2 BLOCKING (T2/T3), TC `NEW-56` fail chưa gắn ticket bug, TC `NEW-58` chưa chạy, và merge #41101**
