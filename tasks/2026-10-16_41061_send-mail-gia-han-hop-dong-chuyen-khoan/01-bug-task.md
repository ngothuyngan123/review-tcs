# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #41061 qua `/new-task` (REST API, `scripts/redmine_fetch.py`) lúc 2026-10-16.
>
> ⚠️ **Đây là task Feature (yêu cầu tính năng mới), KHÔNG phải bug report** — Redmine ticket #41061, Tracker: Feature, Status: Đang fix. Không có section "Tái hiện bug" trong description → KHÔNG có Steps to reproduce / Expected / Actual kiểu tái hiện lỗi. Nội dung dưới đây là **mô tả yêu cầu nghiệp vụ** lấy nguyên văn từ description.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41061 — Send mail khi gia hạn hợp đồng thanh toán chuyển khoản ngân hàng (銀行振込決済) của UnivaPay cho gói thanh toán theo năm (年払い)` |
| Module / Màn hình | Billing / Contract — email tự động `MAIL-01` khi **gia hạn** hợp đồng bill năm bằng chuyển khoản ngân hàng (銀行振込 + 年間一括払い). Liên quan `admin/detail-contract` (SCR-DC-03, FA-031) — job `AutoPaymentJobUnivapay` + `RecoverUpdateInfoUnivapay`. |

## Mô tả yêu cầu (nguyên văn, đã có sẵn tiếng Việt + thuật ngữ JP)

**1. Mục tiêu**

Thêm chức năng gửi email tự động khi:
- User đang sử dụng L Message gói thanh toán năm (年間一括払い).
- Đến thời điểm trước 1 tháng khi hợp đồng hết hạn và cần gia hạn.
- Phương thức thanh toán là UnivaPay 銀行振込決済 (thanh toán chuyển khoản ngân hàng).

→ Hệ thống gửi email hướng dẫn chuyển khoản để user thực hiện gia hạn (gọi tắt **MAIL-01** trong các ghi chú Dev bên dưới).

**2. Người nhận email**

- Email đã đăng ký trong L Message.
- Dùng `${account_name}` làm tên người nhận.

**Subject:**
`【重要】L Message（エルメ）年間一括払い契約更新 振込口座のご案内`
(Quan trọng — Hướng dẫn tài khoản chuyển khoản khi gia hạn hợp đồng thanh toán năm L Message.)

**Nội dung email (nguyên văn template, JP):**

```
このメールはL Message（エルメ）にご登録のメールアドレス宛に
自動的に送信しております。
お振込情報をご確認のうえ、大切に保管してください。

${account_name} 様

いつもL Message（エルメ）をご利用いただき、
誠にありがとうございます。

──────────────────────────────
L Message（エルメ）年間一括払い
契約更新1ヶ月前になりました。
──────────────────────────────

継続してご利用いただくため、
下記の内容にてご契約更新のお振込みをお願いいたします。

お振込先口座は以下のとおりです。

────────────────────────────────
■ ご契約内容
[支払方法　　　] 銀行振込（年間一括払い）
[請求ID　　　　] ${charge_id}
[アカウント名　] ${account_name}
[ご利用プラン　] ${plan_name}
[更新後の契約期間] ${period_from} 〜 ${period_to}
[ご請求金額　　] ${amount}（税込）
────────────────────────────────
■ お振込先
[銀行名　　　　] ${bank_name}
[支店番号　　　] ${bank_branch_code}
[支店名　　　　] ${bank_branch_name}
[口座種別　　　] 普通
[口座番号　　　] ${bank_account_number}
[口座名義　　　] ｶ)ﾕﾆｳﾞｱﾍﾟｲｷﾔｽﾄ
[振込期日　　　] ${date}
────────────────────────────────

■ 注意事項
※ 振込手数料はお客様にてご負担いただきますようお願いいたします。
※ L Message（エルメ）利用料金は、株式会社ユニヴァ・ペイキャストの
　 提供する決済代行システムを利用して請求されます。
　 銀行振込でのお支払いの場合、振込先口座名義は
　 「ｶ)ﾕﾆｳﾞｱﾍﾟｲｷﾔｽﾄ」となります。
※ お振込名義はご登録名と異なっていても問題ございません。
※ 振込期限は ${date} までとなります。
※ 振込期日までに入金が確認できない場合、
　 契約更新のお申込みは無効となります。
　 土日を挟む場合など、入金確認に時間を要する場合がございますので
　 ご注意ください。
※ 振込期日を超過した場合は、再度ご契約（更新）操作をお願いいたします。
※ 入金確認は決済システム側で自動確認しておりますので、
　 過不足が発生している場合も入金完了になりませんのでご注意ください。
　 振込手数料を差し引いた金額をお振込みいただくと不足となります。
※ 行き違いで既にお振込済みの場合は、本メールは破棄してください。

■ お支払い方法の変更について
クレジットカードでの自動決済にご変更いただくと、
更新ごとのお振込手続きが不要になります。
ご希望の場合は管理画面よりお手続きいただけます。

────────────────────────────────
L Message（エルメ）お問い合わせ先
[運営会社] 株式会社ミショナ
[お問い合わせフォーム]
https://tayori.com/form/d9b1964430603d625888d28878a1bf6663f021cf
────────────────────────────────

※このメールは送信専用のため、
　このアドレスへご連絡いただいても返信できかねます。
　お問い合わせは上記のフォームよりお願いいたします。
```

**Bản dịch VN (do người tạo ticket cung cấp sẵn trong description, giữ nguyên văn — không phải Claude dịch):**

```
Email này được gửi tự động tới địa chỉ email đã đăng ký
với L Message (エルメ).

Vui lòng kiểm tra thông tin chuyển khoản và lưu giữ email này.

${account_name} kính gửi,

Xin cảm ơn Quý khách luôn sử dụng dịch vụ L Message (エルメ).

──────────────────────────────
Đã đến thời điểm trước 1 tháng gia hạn
hợp đồng thanh toán một lần theo năm L Message (エルメ).
──────────────────────────────

Để tiếp tục sử dụng dịch vụ,
vui lòng thực hiện chuyển khoản thanh toán gia hạn hợp đồng
theo thông tin dưới đây.

■ Thông tin hợp đồng
[Phương thức thanh toán] Chuyển khoản ngân hàng (thanh toán một lần theo năm)
[ID thanh toán          ] ${charge_id}
[Tên tài khoản          ] ${account_name}
[Gói sử dụng             ] ${plan_name}
[Thời hạn hợp đồng sau gia hạn] ${period_from} 〜 ${period_to}
[Số tiền thanh toán      ] ${amount} (đã bao gồm thuế)

■ Thông tin tài khoản chuyển khoản
[Tên ngân hàng           ] ${bank_name}
[Mã chi nhánh            ] ${bank_branch_code}
[Tên chi nhánh           ] ${bank_branch_name}
[Loại tài khoản          ] Tài khoản thường (普通)
[Số tài khoản            ] ${bank_account_number}
[Tên chủ tài khoản       ] ｶ)ﾕﾆｳﾞｱﾍﾟｲｷﾔｽﾄ
[Thời hạn chuyển khoản   ] ${date}

■ Lưu ý
※ Phí chuyển khoản do khách hàng chịu trách nhiệm thanh toán.
※ Phí sử dụng L Message (エルメ) được thu thông qua hệ thống thanh toán do
   Công ty Univapay cung cấp. Trong trường hợp thanh toán bằng chuyển khoản
   ngân hàng, tên chủ tài khoản nhận tiền sẽ là: 「ｶ)ﾕﾆｳﾞｱﾍﾟｲｷﾔｽﾄ」.
※ Tên người chuyển khoản không cần phải trùng với tên đăng ký.
※ Hạn chuyển khoản là đến ngày ${date}.
※ Nếu không xác nhận được việc thanh toán trước thời hạn chuyển khoản,
   yêu cầu gia hạn hợp đồng sẽ bị vô hiệu. Trong trường hợp có ngày nghỉ
   cuối tuần hoặc ngày lễ, thời gian xác nhận thanh toán có thể mất thêm
   thời gian, vui lòng lưu ý.
※ Nếu vượt quá thời hạn chuyển khoản, vui lòng thực hiện lại thao tác
   đăng ký gia hạn hợp đồng.
※ Việc xác nhận thanh toán được thực hiện tự động bởi hệ thống thanh toán.
   Nếu số tiền chuyển khoản bị thiếu hoặc thừa, thanh toán sẽ không được
   hoàn tất. Đặc biệt, nếu chuyển khoản số tiền đã trừ phí chuyển khoản
   ngân hàng, số tiền thanh toán sẽ bị thiếu.
※ Nếu Quý khách đã thực hiện chuyển khoản trước đó do email bị gửi trùng,
   vui lòng bỏ qua email này.

■ Thay đổi phương thức thanh toán
Nếu chuyển sang phương thức thanh toán tự động bằng thẻ tín dụng,
Quý khách sẽ không cần thực hiện thủ tục chuyển khoản mỗi lần gia hạn.
Nếu có nhu cầu, vui lòng thực hiện thay đổi trong màn hình quản lý.
```

**6. Danh sách variable cần support**

| Variable | Ý nghĩa | Nguồn dữ liệu dự kiến |
|---|---|---|
| `${account_name}` | Tên account | Account/User |
| `${charge_id}` | ID charge | UnivaPay charge |
| `${plan_name}` | Tên plan | Contract plan |
| `${period_from}` | Ngày bắt đầu hợp đồng mới | Contract |
| `${period_to}` | Ngày kết thúc hợp đồng mới | Contract |
| `${amount}` | Số tiền thanh toán（税込） | Charge |
| `${bank_name}` | Tên ngân hàng | UnivaPay |
| `${bank_branch_code}` | Mã chi nhánh | UnivaPay |
| `${bank_branch_name}` | Tên chi nhánh | UnivaPay |
| `${bank_account_number}` | Số tài khoản | UnivaPay |
| `${date}` | Ngày hết hạn chuyển khoản | Payment deadline |

Lưu ý: `ｶ)ﾕﾆｳﾞｱﾍﾟｲｷﾔｽﾄ` **không phải variable** → hard-code cố định trong template email.

**So sánh với email đăng ký mới (task anh em #41101)** — 2 template gần như giống nhau, chỉ khác câu chữ (xem `tasks/2026-10-16_41101_.../01-bug-task.md` mục "So sánh" để đối chiếu ngược lại).

Link task nội bộ (dev workflow, Chatwork): https://www.chatwork.com/#!rid147605079-2145016430893334528

## Steps to reproduce / Expected / Actual

Không áp dụng — đây là yêu cầu tính năng mới, không phải tái hiện bug. Xem "Mô tả yêu cầu" ở trên cho hành vi mong đợi (trigger + nội dung email).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response
- [x] Có file tài liệu đính kèm (không phải ảnh/video/log)

Attachment: `LMessage_年間一括払い契約更新_振込案内メール (1).md` — https://redmine.melonglobal.net/attachments/download/30557/LMessage_%E5%B9%B4%E9%96%93%E4%B8%80%E6%8B%AC%E6%89%95%E3%81%84%E5%A5%91%E7%B4%84%E6%9B%B4%E6%96%B0_%E6%8C%AF%E8%BE%BC%E6%A1%88%E5%86%85%E3%83%A1%E3%83%BC%E3%83%AB%20(1).md
(nghi là file request/spec gốc được Dev tham chiếu trong journal — chưa tải nội dung, mở link trên để đọc khi cần.)

## Ghi chú thêm của Leader

- **Feature flag `RENEWAL_TRANSFER_MAIL_ENABLED`** — mặc định `false`; thiếu `RENEWAL_TRANSFER_MAIL_EFFECTIVE_DATE` (ngày hiệu lực) thì cũng **KHÔNG gửi** (D-15, mặc định AN TOÀN cả 2 tham số rollout). Không có hồi tố cho hợp đồng có hạn chuyển khoản trước ngày hiệu lực.
- **Môi trường dev không có DB/Redis** theo báo cáo Dev → AI dev chỉ verify được compile/lint/static scan, **hành vi thật (migrate, gửi mail thật, 2 cron chồng lượt, đối soát lô đầu tiên) cần QA runtime** trên môi trường có DB — Journal tự đánh dấu `[VERIFY-04]`.
- ⚠️ **2 BLOCKING chưa xác nhận đã xử lý** (AI review độc lập 29/09/2026, ticket vẫn "New"/chưa Resolved tại thời điểm fetch 2026-10-16):
  1. **Selector chỉ dựa `status_payment=5`** (`ContractRenewalMailRepository.php:44-83`) — cột này còn được ghi ở 3 đường UI khác ngoài job (`BotController@paymentBotSlot` / `@paymentBotSlotV2` / `@handleCallbackPaymentCardSuccess`) → không có discriminator phân biệt "charge do job tạo" với "charge do UI tạo". Rủi ro: hợp đồng có số TK từ `paymentBotSlot` bị job đóng nhầm `request_get_bank_transfer` về `status=2` → `resolveAmount` null → defer 10 lần → `markFailed`.
  2. **`${amount}` không neo theo kỳ** (`ContractRenewalTransferMailService.php:373-394`) — `getOpenTransferRequest()` lấy row mới nhất có `status<>2`; nếu Phase 3 tái dùng row cũ (không tạo row mới) thì `amount` + `expired_date_bank_transfer` vẫn là của **kỳ trước**.
- ⚠️ Theo RULE-11, AI-review nội bộ (chưa qua ticket Resolved/Closed) **không phải bằng chứng đã fix** — phải hỏi lại Dev trạng thái 2 BLOCKING này trước khi viết TC kết luận Pass/Fail (xem thêm `03-dev-impact.md` mục 4.3).
- ⚠️ **Task anh em cùng sprint #41101** (mail đăng ký mới — お申し込み) sửa **CÙNG file** `RecoverUpdateInfoUnivapay.php` + `Kernel.php` → rủi ro xung đột merge giữa branch `ai-feature-41061` và `ai-feature-41101`. Cần hỏi Dev tình trạng merge trước khi chốt test.
- Journal #144586 (Tuan PA, 2026-10-15) chỉ ghi gọn: `job: mail:bank_transfer_guide` — có thể là note nội bộ về tên artisan command dùng chung với #41101, chưa rõ ý đầy đủ, cần hỏi lại tác giả nếu cần.
- Studio đã có task test #336 (`feature: detail-contract`, status `done-ai`, `aiResult=fail`, 61 TC do AI viết — 54 pass / 1 fail / 1 other / 5 chưa chạy, chạy chủ yếu ở `local` 1 lượt `staging`, 0 `prd`) — xem `04-tc-list.md`. **1 TC fail (`NEW-56`)** chưa gắn ticket bug — cần hỏi Dev/Leader trước khi review.

## Journal / note từ Redmine (nguyên văn)

**Journal #139307 — Do Van Tu TuDV — 2026-09-29:**

```
★ BÁO CÁO TIẾN ĐỘ AI DEV — #41061 Send mail khi gia hạn hợp đồng thanh toán chuyển khoản ngân hàng (銀行振込決済) của UnivaPay cho gói thanh toán theo năm (年払い)  (29/09/2026)
(Comment TỰ ĐỘNG do workflow AI implement sinh ra từ trạng thái thật của branch —
 không phải ý kiến cá nhân viết tay.)
════════════════════════════════════════════════

Branch: ai-feature-41061 · base: 131bde0f22 · HEAD: 405bdf673e
Sprint: sprint-2026-09 · UPDATE — FA-031 `admin/detail-contract` (bổ sung mail mới vào luồng charge chuyển khoản đã có)
Trạng thái: completed (100%) — Hoàn tất — đọc 3 nguồn còn thiếu (request.md · qa-spec · feedback/agent-requests) và đối chiếu với code

■ 1. ĐÃ LÀM
 • MAIL-01 「銀行振込 契約更新案内メール」 — gửi 1 mail cho mỗi kỳ gia hạn của hợp đồng năm (年間一括払い) trả bằng UnivaPay 銀行振込
 • Migration 4 cột cờ renewal_mail_* trên bot_contracts (QT-002 B — không tạo bảng hàng đợi)
 • ContractRenewalMailRepository + Interface + binding: selector §4, claim nguyên tử theo kỳ, gỡ claim mồ côi
 • ContractRenewalTransferMailService: guard G-01…G-06, dựng 11 biến, chống gửi trùng theo kỳ hợp đồng
 • Kênh gửi ContractRenewalTransferMail qua SMTP ADMIN_MAIL_* (QT-004 A)
 • Template emails.contract_renewal_transfer — nguyên văn khách duyệt (11 biến + 3 giá trị hardcode + 8 mục 注意事項)
 • Móc dispatchPending() vào AutoPaymentJobUnivapay (cuối lượt 06:30) và recover:RecoverUpdateInfoUnivapay (mỗi 5 phút); KHÔNG đụng Phase 3

■ 2. THAY ĐỔI CODE TRÊN BRANCH
 • 405bdf673e — feat(41061): update implementation — ContractRenewalTransferMailService.php (spec 2474113b4e2c0f5d) (1 file, +8/-2)
 • 814bbe9857 — feat(41061): update implementation — ContractRenewalTransferMailService.php (spec bea3ecff6d513882) (1 file, +14/-1)
 • 43249e1563 — feat(41061): update implementation — AutoPaymentJobUnivapay.php, RecoverUpdateInfoUnivapay.php, ContractRenewalMailRepositoryInterface.php +11 more (spec bea3ecff6d513882) (14 file, +788/-541)
 • ef2ee7420f — feat(41061): MAIL-01 銀行振込 契約更新案内メール — hàng đợi + phát mail (9 file, +892/-3)

■ 3. ĐÃ KIỂM TỚI ĐÂU
 • Checklist: 45 mục — pass 43 / manual 2
 • ⚠ Container dev KHÔNG có DB/Redis ⇒ chỉ verify tới mức compile/lint + kiểm tĩnh; hành vi thật cần QA runtime.

■ 4. CẦN QA RUNTIME / CÒN HỞ
Cần QA kiểm tay:
 • [TD-20] §7 Metric: đếm hợp đồng theo renewal_mail_status mỗi ngày (0/1/2/9)
 • [VERIFY-04] Verify runtime: migrate, gửi mail thật, 2 cron chồng lượt, đối soát lô đầu tiên

■ 5. KẾT QUẢ REVIEW AI ĐỘC LẬP
Đánh giá ẢNH HƯỞNG LAN (ripple) — BLOCKED · 🔴 2 blocking / 🟡 10 warning · chạy 29/09/2026
 • 🔴 BLOCKING — PHẢI xử lý trước khi merge:
   - [feature] Admin\BotController@paymentBotSlot · @paymentBotSlotV2 · @handleCallbackPaymentCardSuccess · bot_contracts.renewal_mail_*
     ↳ Selector MAIL-01 nhận diện hàng đợi CHỈ bằng status_payment=5, mà cột này được ghi ở 4 nơi: Phase 3 của job (in-scope) và 3 đường UI ngoài phạm vi. Không có cột nào ghi "charge do job tạo" nên không có discriminator. Hệ quả: (1) nhánh có số tài khoản của paymentBotSlot đóng TẤT CẢ request_get_bank_transfer về status=2 (BotController:8875, :9876) → resolveAmount null → defer 10 lần → markFailed + notifyChatwork "[410…
     ↳ vị trí: app/Repositories/Eloquents/ContractRenewalMailRepository.php:44-83 ↔ app/Http/Controllers/Admin/BotController.php:8510,9399,10107
     ↳ đề xuất: Phase 3 phải đánh dấu hàng đợi TƯỜNG MINH thay vì để Service suy diễn: trong đúng câu BotContracts::where(id)->update([... status_payment => 5 ...]) tại AutoPaymentJobUnivapay.php:1125-1141 thêm reset cờ mail cho kỳ này (renewal_mail_status=0, renewal_mail_sent_period=null, renewal_mail_attempts=0, renewal_mail_last_r…
   - [data] request_get_bank_transfer (bảng dùng chung) → biến ${amount} của MAIL-01
     ↳ Spec §4.1 yêu cầu amount = request_get_bank_transfer.amount "của kỳ này", nhưng getOpenTransferRequest() lấy row mới nhất có status<>2, không neo vào kỳ. Phase 3 (AutoPaymentJobUnivapay:1153-1167) chỉ TẠO row mới khi row mới nhất đã status=2; ngược lại DÙNG LẠI và chỉ update status — amount + expired_date_bank_transfer giữ của kỳ cũ. Đã grep toàn bộ writer status=2: chỉ có các endpoint UI (PointSettingController 387…
     ↳ vị trí: app/Services/ContractRenewalTransferMailService.php:373-394 + app/Repositories/Eloquents/ContractRenewalMailRepository.php:238-244
     ↳ đề xuất: Ưu tiên: lấy amount từ ROW CHA payment_histories khớp đúng charge kỳ này — where(univa_charge_id, $contract->univa_charge_id)->whereNull(id_parent)->value(amount). Phase 3 insert row cha với ĐỦ amount rồi mới sinh 12 row con có id_parent+number_bill (AutoPaymentJobUnivapay:1180-1220; cột id_parent/number_bill/univa_ch…
 • 🟡 WARNING — cần BA/TA xác nhận chấp nhận hay vá:
   • [data] bot_contracts (bảng nóng billing) — hiệu năng & lock — releaseStaleClaims() là UPDATE bot_contracts ... WHERE renewal_mail_status = 1 mà migration KHÔNG thêm index nào ⇒ full scan + row lock trên bảng billing, chạy mỗi 5 phút (Kernel:227) và cả lượt 06:3…
   • [feature] cron recover:RecoverUpdateInfoUnivapay (Kernel:227) — Schedule KHÔNG có withoutOverlapping() trong khi MAIL-01 gửi SMTP ĐỒNG BỘ trong tiến trình cron, tối đa BATCH_SIZE=200 mail/lượt ⇒ lượt chạy có thể vượt 5 phút và chồng lượt. claim() chống gửi trùng…
   • [feature] mail 振込先口座の発行完了 (SendMailUpdateAccountNumber) — Cùng một lượt cron gửi 2 mail cho CÙNG user, CÙNG thông tin ngân hàng, cách nhau vài giây: SendMailUpdateAccountNumber (dòng 100-101) rồi dispatchPending() → MAIL-01 (dòng 116). Spec không nói gì về…
   • [data] cột bot_contracts.release_date_transfer (ngưỡng cảnh báo 3 ngày) — defer() tính mốc cảnh báo từ release_date_transfer, nhưng cột này bị nhiều luồng ghi và cả reset null (PointSettingController 285/366/980/2319/2895, BotEnterPriseController 364, BotController 8469/93…
   • [feature] xử lý lỗi của 2 command gọi dispatchPending() — Chỉ catch (\Exception). PHP 7 \Error/\TypeError sẽ thoát ra. Ở AutoPaymentJobUnivapay nó là lệnh CUỐI handle() nên tiền đã xử lý xong (rủi ro thấp); ở RecoverUpdateInfoUnivapay nó nằm TRƯỚC log End v…
   • [feature] observability TD §7 — countByStatus() — countByStatus() khai báo trong interface + implement đầy đủ nhưng KHÔNG có caller nào trong app/ ⇒ code chết, và yêu cầu "theo dõi tồn đọng renewal_mail_status=0" của TD §7 chưa có command/endpoint/d…
   • [api] cấu hình deploy — 2 env mới — RENEWAL_TRANSFER_MAIL_ENABLED / RENEWAL_TRANSFER_MAIL_EFFECTIVE_DATE không được khai báo ở đâu trong repo (không có .env.example, không có entry config/) và đọc bằng env() lúc runtime. Rủi ro config:…
   • [data] migration ALTER bot_contracts (bảng nóng) + chưa verify runtime — Schema::table + ->after(release_date_transfer) buộc MySQL rebuild bảng (mất ALGORITHM=INSTANT của MySQL 8) trên bảng nóng của toàn bộ billing. Ngoài ra CHƯA verify được migration đã chạy trên DB dev:…
     … và 2 mục nữa (xem dashboard)

■ 6. ĐIỂM AI TỰ QUYẾT — CẦN BA/TA XÁC NHẬN
 • [D-02][medium] Render mail: giu nguyen bo cuc text bang white-space:pre-wrap
   → đã chọn: Bloc toan bo noi dung nguyen van trong mot <div style=white-space:pre-wrap> thay vi dung lai bo cuc card HTML kieu job_update_account_number_success.
   → căn cứ: BR-06, BR-07
 • [D-09][medium] QT-011 đã tự giải: status_payment=5 trong luồng chuyển khoản = chờ chuyển khoản
   → đã chọn: Selector lọc status_payment = 5 (hằng STATUS_PAYMENT_WAIT_TRANSFER) và guard G-05 đọc lại đúng giá trị này; KHÔNG dùng nhãn config sns-line.status_payment_bot_slot.bill_month (tên legacy, không phản ánh ngữ nghĩa ở luồng transfer).
   → căn cứ: TD §4 QT-011 / §9.1
 • [D-14][medium] Kênh gửi ADMIN_MAIL_* (QT-004 A) đi ngược tiền lệ mail billing trong code
   → đã chọn: Theo TD — gửi qua SMTP ADMIN_MAIL_* (pattern app/Mail/ActiveAccount.php), cô lập trong đúng 1 method để đổi kênh chỉ sửa 1 chỗ
   → căn cứ: TD §6 QT-004 (A)
 • [D-15][high] Mặc định AN TOÀN cho 2 tham số rollout: cờ bật = tắt, thiếu ngày hiệu lực = không gửi
   → đã chọn: RENEWAL_TRANSFER_MAIL_ENABLED mặc định false; RENEWAL_TRANSFER_MAIL_EFFECTIVE_DATE không đặt ⇒ KHÔNG gửi + log WARN mỗi lượt
   → căn cứ: TD §7 Rollout & Rollback
 • [D-20][medium] Thêm cơ chế gỡ claim mồ côi (renewal_mail_status kẹt ở 1) — TD không định nghĩa chuyển tiếp 1→0
   → đã chọn: dispatchPending() gọi releaseStaleClaims(30 phút) trước khi quét; mốc claim nhét vào renewal_mail_last_reason dạng claimed_at=Y-m-d H:i:s nên không phải thêm cột
   → căn cứ: TD §3 (5 trạng thái) / §4 Concurrency / §7 Observability
 • [D-21][high] BA REVERT phạm vi — thu code từ 6 luồng về 1 luồng gia hạn, bỏ 4 biến thể nội dung
   → đã chọn: Căn lại toàn bộ theo spec hiện hành: khoá chống trùng theo KỲ (renewal_mail_sent_period, datetime) thay cho univa_charge_id; selector status_payment=5 thay cho predicate is_wait_transfer; 1 template nguyên văn thay cho 4 biến thể; bỏ dự phòng amount_payment
   → căn cứ: task_status.md 2026-09-22 REVERT theo yêu cầu BA (anh PTN) · TD §3/§4 bản revert
 • [D-22][high] Selector TD §4 tự mâu thuẫn với cơ chế chống trùng §3 (giữ nguyên sau revert)
   → đã chọn: Ghi renewal_mail_sent_period ngay lúc CLAIM; selector nhận cả trạng thái terminal khi kỳ đã khác, thay vì đòi cứng renewal_mail_status IN (0)
   → căn cứ: TD §3 Cơ chế chống gửi trùng vs §4 Selector
 • [D-23][medium] ${amount} có thể là số tiền của kỳ TRƯỚC nếu Phase 3 tái dùng bản ghi request_get_bank_transfer cũ
   → đã chọn: Vẫn đọc đúng nguồn QT-003 (request_get_bank_transfer đang mở), KHÔNG tự thêm nguồn khác; ghi lại rủi ro để TA/QA xác minh
   → căn cứ: TD §4.1 QT-003
 • [D-25][medium] Không thêm index cho các cột selector — lệch BE-coding-rules §5 nhưng theo đúng TD §3
   → đã chọn: Giữ migration chỉ ADD COLUMN, KHÔNG tạo index cho renewal_mail_status / renewal_mail_sent_period / expired_date_bank_transfer / status_payment
   → căn cứ: .claude/docs/BE-coding-rules.md §5 (Index DB) vs technical-spec §3 Indexes
 • [D-26][medium] feedback/agent-requests.md AR-06 còn nói thiết kế dùng bảng send_mail_contract_renewals — mâu thuẫn TD §3
   → đã chọn: Theo Technical Spec §3 (QT-002 phương án B — 4 cột cờ trên bot_contracts), KHÔNG tạo bảng hàng đợi; AR-06 là ghi chú cũ chưa cập nhật
   → căn cứ: feedback/agent-requests.md AR-06 vs dev/technical-spec §3 (Updated from QT-002 B)
 • (+ 3 quyết định mức low — xem tab ⚖ Quyết định trên dashboard)

────────────────────────────────────────────────
Sinh tự động lúc 2026-09-29T13:43:58.455Z từ artifact của task "41061_send-mail-khi-gia-han-hop-dong-thanh-toa".

branch code: ai-feature-41101
```

**Journal #144586 — Tuan PA — 2026-10-15:**

```
job: 
mail:bank_transfer_guide
```
