# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT KHÔNG ĐÚNG FORMAT CHUẨN**: Redmine #41101 **không có** section "Đánh giá ảnh hưởng phía dev" theo format chuẩn (1. Nguyên nhân / 2. Cách fix / 3. Function caller đã check / 4.1-4.2-4.3). Ticket là **task Feature**, Dev chỉ để lại **Journal #139306** — báo cáo tiến độ dạng AI-dev-workflow (không phải đánh giá viết tay theo template). Nội dung dưới đây là **best-effort mapping** của `/new-task` từ Journal đó — **PHẢI được Dev/Leader xác nhận lại** trước khi dùng làm input chính thức cho `/write-tc` hoặc `/review-tc`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Do Van Tu TuDV (`issue.assigned_to`) — báo cáo sinh bởi workflow AI dev, branch `ai-feature-41101` |
| Commit / Pull Request | Không có link PR trong Redmine. Commit trên branch: `0015571c08`, `7ffda75716`, `01b841561d` (base `131bde0f22`). ⚠️ Journal còn ghi "1 file thay đổi CHƯA COMMIT trong worktree" tại thời điểm báo cáo (29/09) |
| Branch | `ai-feature-41101` |
| Ngày submit đánh giá | 2026-09-29 (Journal #139306) |
| Auto-filled | 2026-10-16 by `/new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ do input không đúng format chuẩn (xem cảnh báo đầu file), checkbox này **đặc biệt quan trọng** — phải đọc lại Journal nguyên văn ở `01-bug-task.md` + hỏi Dev hiện trạng (3 bug HIGH + merge conflict với #41061 đã xử lý tới đâu) trước khi tick.

---

## 1. Nguyên nhân

<!-- Task Feature, không phải bug fix — không có "nguyên nhân lỗi". Mục này diễn giải LÝ DO cần feature. -->

Không áp dụng theo nghĩa "root cause bug". **Lý do cần feature** (từ Description §1): hiện tại khi khách hàng đăng ký mới hợp đồng bằng 銀行振込 (chuyển khoản) + 年間一括払い (bill năm), hệ thống **chưa** tự động gửi thông tin tài khoản chuyển khoản cho khách → cần bổ sung email `MAIL-01` tự động sau khi đăng ký thành công.

## 2. Cách fix (triển khai)

<!-- Từ Journal ■1 ĐÃ LÀM -->

- Bảng hàng đợi mới `send_mail_bank_transfer_guides` + Model + Repository + Interface + binding `RepositoryServiceProvider`.
- Enqueue `MAIL-01` trong `BotController@paymentBotSlotV2` nhánh 銀行振込 (bọc try/catch, lỗi mail không hỏng đăng ký — BR-05); phủ cả luồng UnivaPay trả số TK trễ.
- Artisan command mới `mail:bank_transfer_guide` + schedule `everyMinute`: claim PROCESSING, batch 200, retry tối đa 5, tự giải phóng dòng kẹt > 15 phút.
- Blade view mới `emails.bank_transfer_guide` — 11 biến + 3 giá trị cố định.
- Chặn `MAIL-EX-01` (email gia hạn cũ) ở `RecoverUpdateInfoUnivapay` cho đúng nhóm hợp đồng đăng ký mới (BR-15) — **nhưng AI review nội bộ phát hiện guard sai scope, xem §4.3 BUG BE-01/BR-01 bên dưới**.
- Feature flag `MAIL_BANK_TRANSFER_GUIDE_ENABLED` (mặc định `false`) chặn ở bước enqueue.
- Guard 7 biến bắt buộc rỗng → đánh `EXPIRED`, không gửi, không retry (D-08).
- BR-12: đóng (`EXPIRED`) dòng hàng đợi CŨ của cùng hợp đồng khi đăng ký lại → chặn gửi 2 `MAIL-01` trùng nhau (D-11).
- Chặn race condition: dòng bị supersede giữa lúc đang xử lý thì không gửi (`currentStatus` check trước `sendMailApi`, D-13).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Từ Journal ■2 (commit list) + ■3 (static_scan_L27, interface_impl) -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotController@paymentBotSlotV2` | Thêm enqueue `MAIL-01` nhánh 銀行振込 | Trigger chính của feature |
| 2 | `RecoverUpdateInfoUnivapay.php` | Thêm guard chặn `MAIL-EX-01` cho hợp đồng đã có `MAIL-01` active | BR-15/BR-16 — ⚠️ guard bị AI review đánh HIGH (scope sai, xem 4.3) |
| 3 | `SendMailBankTransferGuideCommand.php` (mới) + `Kernel.php` | Command mới + đăng ký schedule `everyMinute` | Consumer xử lý hàng đợi |
| 4 | `SendMailBankTransferGuideRepository(Interface).php` + `BankTransferGuideMailService.php` | File mới, sửa 3 lượt (interface/repo/service) | Core logic enqueue/claim/send/supersede |
| 5 | `emails/bank_transfer_guide.blade.php` | View mới | Nội dung email — ⚠️ bị AI review đánh HIGH (vỡ layout Outlook, xem 4.3) |
| 6 | `MailApiService` (dùng chung, có sẵn) | **KHÔNG sửa** (quyết định D-09) | Service gửi mail dùng chung, nuốt lỗi transport — chấp nhận hạn chế đã biết |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BotController@paymentBotSlotV2` — enqueue MAIL-01 | `app/Http/Controllers/BotController.php` | Direct | Trigger khi đăng ký mới hợp đồng 銀行振込 + 年間一括払い |
| F2 | `RecoverUpdateInfoUnivapay` — guard chặn MAIL-EX-01 | `app/Console/Commands/RecoverUpdateInfoUnivapay.php` | Direct, nhưng **impact gián tiếp RẤT RỘNG** | ⚠️ BE-01/BR-01 [HIGH]: guard `hasActiveGuideForContract()` chỉ lọc `bot_contract_id` + `status<>EXPIRED`, KHÔNG phân biệt theo giao dịch (`univa_charge_id`) → hợp đồng từng nhận `MAIL-01` (status `SENT`/`ERROR` không đổi suốt đời hợp đồng) sẽ KHÔNG BAO GIỜ nhận lại `MAIL-EX-01` ở các flow khác |
| F3 | `mail:bank_transfer_guide` command (consumer hàng đợi) | `app/Console/Commands/SendMailBankTransferGuideCommand.php` + `Kernel.php` | Direct | Chạy mỗi phút, claim batch 200, retry 5 lần |
| F4 | `BankTransferGuideMailService` | file mới | Direct | Enqueue / send / supersede / guard biến thiếu |
| F5 | `MailApiService::sendMailApi` (dùng chung, không sửa) | có sẵn | Indirect | D-09: nuốt lỗi transport → dòng hàng đợi có thể bị đánh SENT dù email không tới thật |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `send_mail_bank_transfer_guides` (bảng mới) | CREATE (migration) | Hàng đợi gửi MAIL-01: status WAITING/PROCESSING/SENT/ERROR/EXPIRED, `univa_charge_id`, `attempts` |
| D2 | `bot_contracts` (`contract_bill_type` / `pending_contract_bill_type` / `payment_method`, …) | READ | Dùng để check điều kiện trigger (D-01) + lấy data hiển thị email; KHÔNG update trực tiếp bởi feature này |
| D3 | `MAIL_BANK_TRANSFER_GUIDE_ENABLED` (env/config) | CREATE | Feature flag, mặc định `false` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đăng ký mới hợp đồng bill năm chuyển khoản (`bot-add` bước 3, FA-032) | F1, D1 | High (feature chính của task) |
| T2 | **Email gia hạn `MAIL-EX-01`** cho 5 flow: `extendContract` (gia hạn thủ công), `changePaymentMethod`, `billTransferUnivapayContract`, `acceptBillMaxFriendV2`, `paymentAddSlotEnterprise` | F2 (bug BE-01/BR-01 HIGH) | **High — regression im lặng đã biết, CHƯA xác nhận đã fix.** Hợp đồng đã nhận `MAIL-01` sẽ không bao giờ nhận `MAIL-EX-01` ở các flow này. `RecoverUpdateInfoUnivapay` là điểm gửi `MAIL-EX-01` duy nhất còn sống |
| T3 | Hiển thị email `MAIL-01` trên client mail — đặc biệt **Outlook for Windows desktop** | F4 (bug FE-01 HIGH) | High — layout dựa `white-space:pre-wrap`, không `<br>`/MSO fallback → 62 dòng gộp thành 1 đoạn, mất hết 9 khối `■` |
| T4 | Task anh em cùng sprint **#41061** (mail gia hạn 契約更新) — đụng merge cùng `RecoverUpdateInfoUnivapay.php` + `Kernel.php` | Journal ■5 ripple BLOCKING + ■6 D-14 | High — rủi ro merge sai làm mất tính năng âm thầm (của 1 trong 2 task) |
| T5 | Job hàng đợi `send_mail_bank_transfer_guides` — concurrency 2 tiến trình cùng claim | Journal ■5 ripple (`claimBatch` read-modify-write không whereIn status) | Medium — BR-03 "đúng 1 email" có thể vi phạm nếu lượt chạy > 15 phút chồng lấn |
| T6 | Nhánh nâng cấp free→trả phí bằng chuyển khoản (`action_bill=new` + `bot_id_upgrade`, FA-032) | Journal ■5 ripple | Medium — `contract_bill_type` giữ gói CŨ, kỳ mới ở `pending_*`; D-01 cố ý chấp nhận cả `pending_contract_bill_type` |

> **3 bug mức HIGH do AI review nội bộ phát hiện 26/29-09-2026, CHƯA rõ tình trạng fix hiện tại** (ticket vẫn "Đang fix" tại 2026-10-16; journal tự ghi "bản implement còn sửa tiếp SAU lượt review này"): `BE-01`/`BR-01` (regression MAIL-EX-01, T2) và `FE-01` (vỡ layout Outlook, T3). Theo RULE-11, AI-review nội bộ không phải bằng chứng đã fix — **phải hỏi Dev xác nhận trạng thái 3 bug này trước khi viết TC kết luận Pass/Fail**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân / lý do feature) rõ ràng, đủ chi tiết để viết TC verify
- [ ] Mục 2 (cách implement) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót — **đặc biệt task anh em #41061**)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC — **ưu tiên hỏi trạng thái BE-01/BR-01/FE-01 và merge #41061**
