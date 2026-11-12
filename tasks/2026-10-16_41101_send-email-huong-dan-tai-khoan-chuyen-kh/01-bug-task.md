# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #41101 qua `/new-task` (REST API, `scripts/redmine_fetch.py`) lúc 2026-10-16.
>
> ⚠️ **Đây là task Feature (yêu cầu tính năng mới), KHÔNG phải bug report** — Redmine ticket #41101, Tracker: Feature, Status: Đang fix. Không có section "Tái hiện bug" trong description → KHÔNG có Steps to reproduce / Expected / Actual kiểu tái hiện lỗi. Nội dung dưới đây là **mô tả yêu cầu nghiệp vụ** lấy nguyên văn từ description.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41101 — Send email hướng dẫn tài khoản chuyển khoản ngân hàng khi đăng ký mới plan bill năm` |
| Module / Màn hình | Billing / Contract — email tự động `MAIL-01` khi đăng ký mới hợp đồng bill năm bằng chuyển khoản ngân hàng (銀行振込 + 年間一括払い). Liên quan `bot-add` bước 3 (đăng ký mới, FA-032) + `admin/detail-contract` (SCR-DC-03, FA-031). |

## Mô tả yêu cầu (nguyên văn, đã có sẵn tiếng Việt + thuật ngữ JP)

**1. Mục tiêu task**

Hiện tại khi khách hàng đăng ký mới L Message bằng phương thức:
- Thanh toán chuyển khoản ngân hàng (銀行振込決済)
- Gói thanh toán một lần theo năm (年間一括払い)

thì cần bổ sung chức năng: sau khi khách hàng đăng ký thành công, hệ thống **tự động gửi email hướng dẫn thông tin chuyển khoản**.

Email này dùng để cung cấp: thông tin hợp đồng, thông tin số tiền cần chuyển, thông tin tài khoản nhận tiền của UnivaPay, hạn chuyển khoản.

**2. Trigger gửi email**

Điều kiện gửi — khi đồng thời:

| Điều kiện | Giá trị |
|---|---|
| Payment method | 銀行振込 (Bank transfer) |
| Billing type | 年間一括払い (Annual payment) |
| Flow | Đăng ký mới hợp đồng |

→ Gửi email hướng dẫn chuyển khoản (gọi tắt **MAIL-01** trong các ghi chú Dev bên dưới).

**Subject:**
`【重要】L Message（エルメ）年間一括払い お申し込み 振込口座のご案内`
(Quan trọng — Hướng dẫn tài khoản chuyển khoản khi đăng ký thanh toán một lần theo năm L Message.)

**Nội dung email (nguyên văn template):**

```
=========================================================
このメールはL Message（エルメ）にご登録のメールアドレス宛に
自動的に送信しております。
お振込情報をご確認のうえ、大切に保管してください。
=========================================================

${account_name} 様

この度はL Message（エルメ）にお申し込みいただき、
誠にありがとうございます。

──────────────────────────────
L Message（エルメ）年間一括払い
お申し込みを受け付けいたしました。
──────────────────────────────

ご利用を開始いただくため、
下記の内容にてお振込みをお願いいたします。
お振込先口座は以下のとおりです。

────────────────────────────────
■ ご契約内容
[支払方法　　　] 銀行振込（年間一括払い）
[請求ID　　　　] ${charge_id}
[アカウント名　] ${account_name}
[ご利用プラン　] ${plan_name}
[ご契約期間　　] ${period_from} 〜 ${period_to}
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
※ 振込期日までに入金が確認できない場合、お申し込みは無効となります。
　 土日を挟む場合など、入金確認に時間を要する場合がございますので
　 ご注意ください。
※ 振込期日を超過した場合は、再度お申し込み操作をお願いいたします。
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

**4. Variable cần support**

| Variable | Nội dung |
|---|---|
| `${account_name}` | Tên người đăng ký / Account name |
| `${charge_id}` | ID thanh toán |
| `${plan_name}` | Tên plan |
| `${period_from}` | Ngày bắt đầu hợp đồng |
| `${period_to}` | Ngày kết thúc hợp đồng |
| `${amount}` | Số tiền thanh toán（税込） |
| `${bank_name}` | Tên ngân hàng |
| `${bank_branch_code}` | Mã chi nhánh |
| `${bank_branch_name}` | Tên chi nhánh |
| `${bank_account_number}` | Số tài khoản |
| `${date}` | Hạn chuyển khoản |

Lưu ý: `ｶ)ﾕﾆｳﾞｱﾍﾟｲｷﾔｽﾄ` **không phải variable** → hard-code cố định trong template email.

**So sánh với email gia hạn (Renewal email — task anh em #41061)** — task này dùng lại gần như toàn bộ nội dung email gia hạn, chỉ khác:

| Vị trí | Email gia hạn | Email đăng ký mới (task này) |
|---|---|---|
| Subject | 年間一括払い契約更新 振込口座のご案内 | 年間一括払い お申し込み 振込口座のご案内 |
| Greeting | いつもご利用いただきありがとうございます | この度はお申し込みいただきありがとうございます |
| Lead text | 契約更新1ヶ月前になりました | お申し込みを受け付けいたしました |
| Nội dung dẫn | 継続してご利用いただくため、ご契約更新のお振込みを | ご利用を開始いただくため、お振込みを |
| Contract period label | 更新後の契約期間 | ご契約期間 |
| Khi chưa thanh toán | 契約更新のお申込みは無効 | お申し込みは無効 |
| Quá hạn | 再度ご契約（更新）操作 | 再度お申し込み操作 |

Link task nội bộ (dev workflow): https://missiona-tools.vercel.app/lme-dev/tickets/a402f508-3140-4dce-a64b-e66c66f2793e

## Steps to reproduce / Expected / Actual

Không áp dụng — đây là yêu cầu tính năng mới, không phải tái hiện bug. Xem "Mô tả yêu cầu" ở trên cho hành vi mong đợi (trigger + nội dung email).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response
- [x] Có file tài liệu đính kèm (không phải ảnh/video/log)

Attachment: `0c0c8241-5bc7-41d3-bd8c-e9cc753ab6e0.md` — https://redmine.melonglobal.net/attachments/download/30602/0c0c8241-5bc7-41d3-bd8c-e9cc753ab6e0.md
(nghi là file request/spec gốc được Dev tham chiếu trong journal — `request.md`; chưa tải nội dung, mở link trên để đọc khi cần.)

## Ghi chú thêm của Leader

- **Feature flag `MAIL_BANK_TRANSFER_GUIDE_ENABLED`** — mặc định `false`. Sau deploy, phải set env flag này = `true` thì enqueue mail mới chạy (chặn ở bước ENQUEUE, không chặn consumer — dòng đã enqueue trước khi tắt flag vẫn được gửi).
- **Môi trường dev không có DB/Redis** theo báo cáo Dev → AI dev chỉ verify được compile/lint/static scan, **hành vi thật (DB, job chạy, gửi mail thật) cần QA runtime** trên môi trường có DB.
- ⚠️ **Task anh em cùng sprint #41061** (mail gia hạn/renewal — 契約更新) sửa **CÙNG file** `RecoverUpdateInfoUnivapay.php` + `Kernel.php` → rủi ro xung đột merge. Cần hỏi Dev tình trạng merge 2 branch (`ai-feature-41101` vs `ai-feature-41061`) trước khi chốt test.
- ⚠️ Ticket đang ở trạng thái **"Đang fix"** (chưa Resolved/Closed) tại thời điểm fetch (2026-10-16). Journal #139306 (29/09/2026) ghi nhận **3 bug mức HIGH do AI review nội bộ phát hiện CHƯA xác nhận đã fix** — xem chi tiết đầy đủ trong Journal bên dưới, đã rút gọn vào `03-dev-impact.md` mục 4.3. Theo RULE-11 các phát hiện AI-review nội bộ (chưa qua ticket Resolved/Closed) **không được dùng để tự kết luận đã fix hay chưa** — cần hỏi lại Dev trạng thái hiện tại.
- Studio đã có task test #335 (`feature: detail-contract`, status `tc-ready`, 56 TC do AI viết, 47 pass / 0 fail / 7 skip / 2 chưa chạy) — xem `04-tc-list.md`.

## Journal / note từ Redmine (nguyên văn)

**Journal #139306 — Do Van Tu TuDV — 2026-09-29:**

```
★ BÁO CÁO TIẾN ĐỘ AI DEV — #41101 Send email hướng dẫn tài khoản chuyển khoản ngân hàng khi đăng ký mới plan bill năm  (29/09/2026)
(Comment TỰ ĐỘNG do workflow AI implement sinh ra từ trạng thái thật của branch —
 không phải ý kiến cá nhân viết tay.)
════════════════════════════════════════════════

Branch: ai-feature-41101 · base: 131bde0f22 · HEAD: 0015571c08
Sprint: sprint-2026-09 · UPDATE — FA-032 (`admin/bot-add`) + FA-031 (`admin/detail-contract`); email MAIL-01 hiện chưa feature nào sở hữu (QA-spec-008)
Trạng thái: completed (100%) — Hoàn tất lượt 6 — xác minh spec KHÔNG đổi (chỉ fingerprint đổi), đọc feedback/, audit va chạm task anh em #41061, sửa CONV-01 theo reviewer

■ 1. ĐÃ LÀM
 • Bảng hàng đợi `send_mail_bank_transfer_guides` (TD §3) + Model + Repository + Interface + binding RepositoryServiceProvider
 • Enqueue MAIL-01 trong `BotController@paymentBotSlotV2` nhánh 銀行振込 — đúng BR-01, bọc try/catch nên lỗi mail không làm hỏng đăng ký (BR-05); phủ cả luồng B (UnivaPay trả số TK trễ)
 • Artisan command MỚI `mail:bank_transfer_guide` + schedule `everyMinute` (QA-technical-003/004): claim PROCESSING, batch 200, retry 5, giải phóng dòng kẹt >15 phút
 • Blade view MỚI `emails.bank_transfer_guide` — 11 biến + 3 giá trị cố định, nội dung verbatim theo request.md, bố cục gom khối (QA-spec-007)
 • Chặn MAIL-EX-01 ở `RecoverUpdateInfoUnivapay` cho đúng nhóm hợp đồng đăng ký mới (BR-15) — giữ nguyên 7 flow ngoài phạm vi (BR-16/RK-06)
 • Feature flag `MAIL_BANK_TRANSFER_GUIDE_ENABLED` (mặc định false) chặn ở bước enqueue (TD §7)
 • Guard §4 「Khi thiếu」: 7 biến bắt buộc ngoài nhóm ngân hàng rỗng ⇒ EXPIRED, KHÔNG gửi email (rà soát lượt 2)
 • Tín hiệu §7 Observability 「Backlog WAITING」: đếm dòng WAITING cũ hơn 30 phút, cảnh báo khi kéo dài >60 phút (rà soát lượt 3)
 • BR-12: đóng (EXPIRED) dòng hàng đợi của lần đăng ký TRƯỚC khi cùng hợp đồng đăng ký lại — chặn gửi 2 MAIL-01 trùng nhau; 請求ID đọc từ snapshot của chính dòng (rà soát lượt 4)
 • Chốt chặn race: dòng bị supersede giữa lúc đang xử lý thì KHÔNG gửi (`currentStatus` trước `sendMailApi`) (rà soát lượt 5)
 • Repository extend `BaseRepositories` đúng BE-coding-rules §1, gỡ `private $model` tránh che property lớp cha (sửa theo review CONV-01, lượt 6)

■ 2. THAY ĐỔI CODE TRÊN BRANCH
 • 0015571c08 — feat(41101): update implementation — SendMailBankTransferGuideRepositoryInterface.php, SendMailBankTransferGuideRepository.php, BankTransferGuideMailService.php (spec a41802f6b0383ca8) (3 file, +89/-1)
 • 7ffda75716 — feat(41101): update implementation — SendMailBankTransferGuideRepositoryInterface.php, SendMailBankTransferGuideRepository.php, BankTransferGuideMailService.php (spec a41802f6b0383ca8) (3 file, +107/-1)
 • 01b841561d — feat(41101): update implementation — RecoverUpdateInfoUnivapay.php, SendMailBankTransferGuideCommand.php, Kernel.php +9 more (spec a41802f6b0383ca8) (12 file, +1209/-17)
 • ⚠ Còn 1 file thay đổi CHƯA COMMIT trong worktree (chưa lên origin).

■ 3. ĐÃ KIỂM TỚI ĐÂU
 • php_lint: 11/11 file sạch (đo lại 2026-09-28)
 • blade_compile: BladeCompiler 5.5 thật + php -l file sinh ra: sạch
 • email_verbatim: render thật rồi so THẲNG với request.md (yêu cầu gốc của khách, KHÔNG qua bản chép spec §6): thân email 62/62 dòng non-empty + subject + 11 biến (tên & thứ tự) khớp byte-for-byte
 • behaviour_harness: implementations/41101_.../verify-harness.php — 42/42 pass (đo lại 2026-09-28)
 • static_scan_L27: lớp A (check-php-calls) + B (use/PSR-4) không lỗi MỚI; lớp C N/A (blade không @include/@extends); lớp D N/A (không endpoint mới)
 • interface_impl: interface ↔ repository đủ 8/8 method; repository extends BaseRepositories, chỉ ghi đè model()
 • pre_existing_warnings: $this->addLog() (12 chỗ) + token BasicController trong comment — đã có sẵn trên HEAD 131bde0f22, không do task này
 • Checklist: 72 mục — pass 63 / manual 9
 • ⚠ Container dev KHÔNG có DB/Redis ⇒ chỉ verify tới mức compile/lint + kiểm tĩnh; hành vi thật cần QA runtime.

■ 4. CẦN QA RUNTIME / CÒN HỞ
Cần QA kiểm tay:
 • [JOB-12] §4 — Gửi thành công → status = SENT + sent_at = now(); lỗi → attempts++, status = ERROR, message = <lỗi>; hết 5 lần giữ ERROR
 • [SEC-02] §7 — Số tài khoản ảo KHÔNG ghi ra log ứng dụng (log chỉ id dòng hàng đợi + mã lỗi)
 • [OPS-03] §7 Observability — tín hiệu 「Backlog WAITING」: đếm dòng WAITING có created_at cũ hơn 30 phút; kéo dài > 1 giờ ⇒ cảnh báo vận hành (nghi UnivaPay không phát hành tài khoản — RK-03)
 • [CONV-08] BE-coding-rules §4.1 — Ownership check (bot_id/user_id) cho entity nhận id từ request; endpoint có middleware phù hợp
 • [CONV-09] Server-side validation cho input mới (Form Request cho endpoint, validate argument cho command)
 • [CONV-10] BE-coding-rules §5 — N+1 / eager load / batch khi command quét nhiều record
 • [CONV-13] LUẬT runtime-verify-migrations — migration phải được xác nhận đã chạy trên DB dev, không chỉ php -l
 • [CONV-18] dev-review-checklist §Frontend — base component lme-*, không font-family trong page CSS, icon <icon>, disabled prop
 • [MERGE-01] Audit va chạm với task anh em cùng sprint đụng chung vùng code (phát hiện từ feedback/agent-requests.md)

■ 5. KẾT QUẢ REVIEW AI ĐỘC LẬP
Review code 4 chiều — PASS (95/100) · chạy 26/09/2026
 • Theo chiều: Backend 26/27 (96) · Frontend 12/13 (92) · Business Rules 18/19 (95) · Checklist 61/62 (98)
 • Còn 4 mục CHƯA ĐẠT (3 mức HIGH):
   • [BE-01][HIGH] BR-16/RK-06: hasActiveGuideForContract() chỉ lọc bot_contract_id + status<>EXPIRED ⇒ dòng SENT chặn MAIL-EX-01 VĨNH VIỄN cho mọi flow sau trên cùng hợp đồng (gia hạn, đổi phương thức thanh toán, bill transfer, max friend, enterprise). Kịch bản: KH đăng ký mới… — app/Repositories/Eloquents/SendMailBankTransferGuideRepository.php:68-74
   • [BR-01][HIGH] (Cùng defect với BE-01) BR-16 không đạt — phạm vi 「thay thế」 rò rỉ sang 7 flow ngoài task trên cùng hợp đồng. Đúng rủi ro RK-06 mà chính spec đã cảnh báo. impl-report §2.3 khẳng định '7 flow không bị đụng tới' là KHÔNG đúng cho hợp đồng đã từng nhận MAIL-01 — app/Console/Commands/RecoverUpdateInfoUnivapay.php:101
   • [FE-01][HIGH] Email vỡ bố cục trên Outlook for Windows desktop (engine Word không hỗ trợ white-space) — 62 dòng gộp thành 1 đoạn dính liền, mất hết 9 khối ■ và mọi dòng [ラベル] 値. Layout chỉ dựa white-space:pre-wrap, grep: 0 hit <br>, 0 hit MSO conditional ⇒ không có fallbac… — resources/views/emails/bank_transfer_guide.blade.php:44
   • [CONV-01][LOW] Repository mới không extends BaseRepositories (BE-coding-rules §1). Thuần convention, runtime không ảnh hưởng — chỉ 4/94 repo trong repo này extend base ⇒ khuyến nghị sửa doc cho khớp thực tế. Model app/Models + $fillable + binding provider đều ĐÚNG — app/Repositories/Eloquents/SendMailBankTransferGuideRepository.php:13
 • + 24 cảnh báo mức thấp (xem tab 📋 Review trên dashboard).
 • ⚠ Bản implement còn được sửa tiếp SAU lượt review này (implement 28/09/2026 > review 26/09/2026) — vài mục ở trên có thể đã vá; phải chạy lại review mới chốt được.

Đánh giá ẢNH HƯỞNG LAN (ripple) — BLOCKED · 🔴 1 blocking / 🟡 11 warning · chạy 29/09/2026
 • 🔴 BLOCKING — PHẢI xử lý trước khi merge:
   - [feature] MAIL-EX-01 — extendContract (gia hạn thủ công), changePaymentMethod, billTransferUnivapayContract, acceptBillMaxFriendV2, paymentAddSlotEnterprise
     ↳ Guard chỉ lọc bot_contract_id + status<>EXPIRED ⇒ dòng SENT(=1)/ERROR(=2) nằm lại VĨNH VIỄN vẫn tính là active. bot_contracts dùng lại suốt đời hợp đồng (PointSettingController.php:2308 UPDATE chính row đó). Hệ quả: hợp đồng đã nhận MAIL-01 thì không bao giờ nhận MAIL-EX-01 nữa ở mọi flow ⇒ RK-06/BR-16 (regression im lặng). Nặng hơn: RecoverUpdateInfoUnivapay là điểm gửi MAIL-EX-01 DUY NHẤT còn sống (AutoPaymentJobU…
     ↳ vị trí: app/Repositories/Eloquents/SendMailBankTransferGuideRepository.php:76-82 (gọi từ app/Console/Commands/RecoverUpdateInfoUnivapay.php:101)
     ↳ đề xuất: Scope guard theo đúng giao dịch đã sinh ra MAIL-01: thêm tham số $univaChargeId vào hasActiveGuideForContract (interface + repo + service), where(univa_charge_id, $contract->univa_charge_id) + whereIn(status,[WAITING,ERROR,PROCESSING]); recover gọi hasActiveGuideForContract($contract->id, $contract->univa_charge_id).…
 • 🟡 WARNING — cần BA/TA xác nhận chấp nhận hay vá:
   • [feature] Merge release: branch ai-feature-41061 sửa CÙNG use + __construct của RecoverUpdateInfoUnivapay.php — [NEW 2026-09-29] Quét 30 worktree: ai-feature-41061 (HEAD 405bdf673e, 4 commit, 10 file) là branch DUY NHẤT cũng sửa RecoverUpdateInfoUnivapay.php, và sửa đúng cùng vùng dòng: cùng chèn use App\Servi…
   • [feature] 17 command scheduled sau dòng 225 — gồm recover:RecoverUpdateInfoUnivapay (232), recover:payment_univapay_timeout (226)… — [NEW 2026-09-29] Verify bằng source Laravel 5.5.50: ScheduleRunCommand::handle() lặp dueEvents() TUẦN TỰ rồi $event->run() (dòng 52-59); Event::run() → runCommandInForeground() → (new Process(...))->…
   • [data] send_mail_bank_transfer_guides (BR-03 đúng 1 email) — claimBatch() là read-modify-write 2 bước (pluck rồi update) và câu UPDATE KHÔNG có whereIn(status,[WAITING,ERROR]). (1) Lượt chạy >15 phút ⇒ releaseStaleProcessing(15) của lượt sau trả dòng lượt trướ…
   • [feature] attempts / MAX_ATTEMPTS=5 + alert ERROR của technical-spec §7 — MailApiService::sendMailApi KHÔNG throw khi gửi thất bại (sendMailApiChild catch RequestException; sendMailDefault catch \Throwable rồi fallback). Service coi không-throw = thành công và set SENT/sen…
   • [data] Thứ tự deploy §7 + notifyChatwork + migration chưa verify runtime — processQueue() chạm bảng mới ngay câu releaseStaleProcessing và KHÔNG kiểm isEnabled() (isEnabled() chỉ được gọi ở dòng 143) ⇒ nếu code lên trước migration hoặc môi trường nào thiếu bảng thì command…
   • [feature] FA-032 nhánh nâng cấp free→trả phí bằng chuyển khoản (action_bill=new + bot_id_upgrade) — Nhánh tạo hợp đồng MỚI nhưng contract_bill_type gán theo HĐ cũ (hoặc null), kỳ mới ở pending_contract_bill_type; isYearlyBillContract() cố ý chấp nhận cột pending_* nên nhánh được enqueue MAIL-01 và…
   • [data] send_mail_bank_transfer_guides.attempts — $attempts = (int) $row->attempts + 1 — read-modify-write từ bản $row chụp lúc claim, không phải SQL attempts = attempts + 1. An toàn khi claim được tôn trọng (1 consumer) nhưng nếu xảy ra IMP-02/IMP-…
   • [feature] Task em 41061 (ai-feature-41061) — MAIL-01 契約更新 gia hạn — [CẬP NHẬT 2026-09-29] Run #2 ghi 41061 "chưa implement" — SAI: nó đã có branch ai-feature-41061 (HEAD 405bdf673e, 4 commit, 10 file) với hàng đợi riêng bằng 4 cột cờ renewal_mail_* trên bot_contracts…
     … và 3 mục nữa (xem dashboard)

■ 6. ĐIỂM AI TỰ QUYẾT — CẦN BA/TA XÁC NHẬN
 • [D-01][high] BR-01 điều kiện #3 «flow đăng ký mới» = action_bill="new"; kỳ 年間 chấp nhận cả pending_contract_bill_type
   → đã chọn: Enqueue khi action_bill==="new" (tạo bot_contracts mới trong request) AND type_bill==="year". Kiểm kỳ 年間 qua contract_bill_type HOẶC pending_contract_bill_type — vì nhánh nâng cấp bằng chuyển khoản (action_bill=new + bot_id_upgrade) CỐ Ý giữ contract_bill_type = gói CŨ cho tới khi tiền vào, kỳ/gói mới nằm ở pending_contract_*. Mọi action khác (upgrade_pro/extend_contract/recontract/bill_max_friend/change_card/bill_job…) KHÔNG enqueue.
   → căn cứ: BR-01 · technical-design §2 bảng «Điều kiện enqueue» (E-028/E-030/E-032)
 • [D-02][medium] ${account_name} = users.username của chủ hợp đồng (admin_id)
   → đã chọn: Lấy users.username theo bot_contracts.admin_id, resolve TẠI THỜI ĐIỂM GỬI (không snapshot) — cùng bản ghi user đã dùng để lấy email người nhận.
   → căn cứ: common-spec §4 «Tên tài khoản của hợp đồng» · E-018 «Tên người đăng ký / Account name» · U-08
 • [D-03][medium] Hợp đồng không còn hợp lệ lúc gửi → đặt EXPIRED (không gửi, không retry)
   → đã chọn: Dòng hàng đợi chuyển EXPIRED + log cảnh báo + notifyChatwork khi: không tìm thấy bot_contracts, hợp đồng đã huỷ (status=3), đã đổi sang thẻ (payment_method≠2), hoặc không còn là 年間一括払い.
   → căn cứ: technical-design §4 bước 3 «Kiểm tra điều kiện gửi»
 • [D-05][high] Feature flag MAIL_BANK_TRANSFER_GUIDE_ENABLED mặc định FALSE — sau deploy tính năng CHƯA chạy
   → đã chọn: config("sns-line.mail_bank_transfer_guide_enabled") đọc env MAIL_BANK_TRANSFER_GUIDE_ENABLED, default false. Flag chặn đúng ở bước ENQUEUE. Ops phải: (1) chạy migration → (2) deploy code → (3) set env = true mới có mail.
   → căn cứ: technical-spec §7 Rollout & Rollback
 • [D-06][medium] QA-spec-011 còn OPEN — code theo safe default HẸP (chỉ hợp đồng đăng ký mới)
   → đã chọn: Điều kiện chặn MAIL-EX-01 trong RecoverUpdateInfoUnivapay bám ĐÚNG hàng đợi của task (send_mail_bank_transfer_guides, status≠EXPIRED). TUYỆT ĐỐI không xoá lời gọi gửi MAIL-EX-01 ⇒ 7 flow ngoài phạm vi giữ nguyên hành vi.
   → căn cứ: QA-spec-011 (OPEN) · BR-15/BR-16 · RK-06
 • [D-08][medium] Biến bắt buộc ngoài nhóm ngân hàng bị rỗng → EXPIRED, KHÔNG gửi email (bổ sung lượt rà soát 2)
   → đã chọn: Thêm guard missingRequiredParams() kiểm 7 biến account_name/charge_id/plan_name/period_from/period_to/amount/date ngay trước khi gửi. Thiếu bất kỳ biến nào ⇒ markExpired("contract data incomplete: <tên biến>") + notifyChatwork, KHÔNG gửi và KHÔNG retry.
   → căn cứ: common-spec §4 cột 「Khi thiếu」 = 「Không gửi email — dữ liệu hợp đồng lỗi」
 • [D-09][medium] MailApiService NUỐT lỗi gửi ⇒ retry/ERROR của §4 chỉ bắt được lỗi render/DB, không bắt được lỗi transport
   → đã chọn: GIỮ NGUYÊN MailApiService, không sửa. Chấp nhận: lỗi SMTP/mail-API bị nuốt ⇒ dòng hàng đợi vẫn được đánh SENT dù email có thể không tới. Ghi nhận là hạn chế đã biết thay vì tự ý sửa file dùng chung.
   → căn cứ: technical-spec §4 bước 7 «Lỗi → attempts++, status = ERROR, message = <lỗi>»
 • [D-11][high] BR-12 bị vi phạm: cùng 1 hợp đồng đăng ký lại ⇒ 2 dòng hàng đợi ⇒ khách nhận 2 MAIL-01 giống hệt. Đã vá bằng supersede
   → đã chọn: Sau mỗi lần enqueue THÀNH CÔNG, gọi supersedePendingForContract(contractId, newRowId) đóng (EXPIRED) mọi dòng WAITING/ERROR/PROCESSING còn lại của cùng hợp đồng, message «superseded by a newer registration of the same contract». Kèm theo: 請求ID của email đọc từ snapshot univa_charge_id của CHÍNH dòng hàng đợi (fallback về hợp đồng nếu dòng không có).
   → căn cứ: BR-12 (E-061) «mỗi hợp đồng tối đa 1 đơn chuyển khoản đang chờ ⇒ không phát sinh nhiều MAIL-01 song song» · BR-03 · technical-spec §3 (cột univa_charge_id = «charge id của lần đăng ký này»)
 • [D-12][medium] Feature flag chỉ chặn ENQUEUE, consumer KHÔNG kiểm flag — chọn theo §7 bullet 1, không theo câu rollback
   → đã chọn: Giữ nguyên: flag off ⇒ không enqueue dòng mới, nhưng dòng ĐÃ enqueue vẫn được consumer gửi bình thường.
   → căn cứ: technical-spec §7 Rollout bullet 1 (flag «chặn ở bước enqueue») vs §7 Rollback («tắt flag … dòng WAITING còn lại sẽ tự EXPIRED sau hạn chuyển khoản»)
 • [D-13][medium] Bịt kẽ hở của chính bản vá BR-12: dòng bị supersede GIỮA LÚC đang xử lý vẫn gửi
   → đã chọn: Thêm currentStatus($id) + chốt chặn ngay TRƯỚC MailApiService::sendMailApi: nếu dòng đã bị đánh EXPIRED thì bỏ qua, ghi log 「Skip send, row superseded while processing」, không gửi.
   → căn cứ: BR-12 (E-061) · technical-spec §4 Concurrency
 • [D-14][high] Task anh em #41061 (mail gia hạn) sửa CÙNG 2 file với tôi — merge sẽ xung đột, giải sai là mất tính năng im lặng
   → đã chọn: KHÔNG đổi code của 41101 để né xung đột (constructor injection là đúng pattern và chính 41061 cũng làm vậy). Thay vào đó báo human chính xác chỗ đụng + cách hợp nhất đúng.
   → căn cứ: feedback/agent-requests.md mục 「Có thể có task anh em trong cùng sprint」 · RK-06
 • (+ 5 quyết định mức low — xem tab ⚖ Quyết định trên dashboard)

────────────────────────────────────────────────
Sinh tự động lúc 2026-09-29T13:43:49.833Z từ artifact của task "41101_send-email-huong-dan-tai-khoan-chuyen-kh".

branch code: ai-feature-41101
```
