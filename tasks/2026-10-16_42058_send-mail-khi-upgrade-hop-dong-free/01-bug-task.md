# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #42058 bằng `/new-task` (REST API, `scripts/redmine_fetch.py`) — 2026-10-16.
> ⚠️ Đây là ticket **Feature** (Tracker: Feature, không phải Bug) — không có "Tái hiện bug" theo nghĩa thông thường. Steps/Expected/Actual để trống, xem "Ghi chú thêm của Leader" bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42058 — Send mail khi upgrade hợp đồng (free => standard/pro), standard -> pro, hợp đồng lại, extend hợp đồng 1 năm` |
| Module / Màn hình | FA-031 (契約プラン・決済情報) + FA-032 (新規アカウント追加) — theo Journal #140604. Studio feature tag: `detail-contract`. 4 case nghiệp vụ: upgrade free→standard/pro, upgrade standard→pro, 再契約 (hợp đồng lại), extend hợp đồng 1 năm. |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine đã ở tiếng Việt, paste nguyên văn, KHÔNG diễn giải lại. -->

Send mail cho user với các case:
1. upgrade hợp đồng (free => standard/pro)
2. upgrade hợp đồng ( standard -> pro)
3. hợp đồng lại
4. extend hợp dồng 1 năm

Link html: https://docs.missiona.co/wssj/file-20261001-150020.html
wssj
#fpKJLeFZd4DA4e

> Ghi chú: Link html ở trên (prototype nội dung mail) trả 401 lúc Dev implement — xem Journal #140604 mục "TODO còn treo". 4 attachment đính kèm Redmine (xem mục "Ảnh / video / log" bên dưới) nhiều khả năng là bản nội dung đã resolve cho từng case; Leader/Tester nên đọc 4 file này trước khi review mail content (REQ-008 trên Studio).

## Steps to reproduce

<!-- Không có — ticket Feature, không phải bug reproduction. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response
- [x] Có attachment spec nội dung mail (4 file `.md`, KHÔNG phải screenshot/video/log — là nội dung mail từng case)

Attachments (4):
- Hợp đồng lại.md — https://redmine.melonglobal.net/attachments/download/31449/H%E1%BB%A3p%20%C4%91%E1%BB%93ng%20l%E1%BA%A1i.md
- extend hợp đồng 1 năm.md — https://redmine.melonglobal.net/attachments/download/31450/extend%20h%E1%BB%A3p%20%C4%91%E1%BB%93ng%201%20n%C4%83m.md
- upgrade từ standard len pro.md — https://redmine.melonglobal.net/attachments/download/31451/upgrade%20t%E1%BB%AB%20standard%20len%20pro.md
- Upgrade từ free lên standardpro.md — https://redmine.melonglobal.net/attachments/download/31452/Upgrade%20t%E1%BB%AB%20free%20l%C3%AAn%20standardpro.md

## Ghi chú thêm của Leader

**Leader chốt 2026-10-16 (mục đích + phạm vi cover):**
- Mục đích: gửi mail đúng mẫu khi UnivaPay **tạo số tài khoản thành công** cho hợp đồng **bill năm, chuyển khoản**, 4 luồng: nâng free → trả phí · スタンダード → プロ · 再契約 · gia hạn 1 năm.
- (1) Chưa có số tài khoản → chưa gửi; có số tài khoản (kể cả tạo chậm qua job) → gửi. Mỗi mail thay đúng biến. Đủ 4 mẫu, không vào Spam ở Gmail / Yahoo / Hotmail / Outlook.
- (2) Sau tạo số tài khoản và sau chuyển khoản thành công: kiểm trạng thái trên UnivaPay, `expired_date`, Detail hợp đồng 契約詳細, Lịch sử thao tác 操作履歴 đúng nội dung từng luồng.
- (3) Có lịch sử bill ở màn 決済履歴・領収書のダウンロード cho từng luồng.
- Nội dung 4 mail (+ mẫu gốc 元（契約更新）): file HTML Leader gửi = bản lưu của Link html `docs.missiona.co/wssj/file-20261001-150020.html`.

- ⚠️ Ticket không có "Tái hiện bug" — root cause/cách fix nằm ở đánh giá ảnh hưởng tái tạo từ Journal (xem file `03-dev-impact.md`, có cảnh báo riêng về format không chuẩn).
- Feature flag `CONTRACT_CHANGE_MAIL_ENABLED` (mặc định tắt lúc đầu) đã bị **XOÁ** ở bản v4 (Journal #144402) theo yêu cầu "tuanpa" — sau deploy, 4 mail **tự gửi thật cho khách ngay**, không còn công tắc tắt nhanh. Đây là điểm rủi ro cao cần Leader lưu ý khi release.
- Bug liên quan #43221 (再契約 gói 2 năm trả chuyển khoản nhưng hạn chỉ hiện 1 năm) được tìm & fix trong chính luồng implement #42058 (Journal #144563, #144626) — đã có TC trên Studio map `bug #43221`.
- Mail standard→pro bị rơi vào spam trên môi trường dev: Dev kết luận KHÔNG phải lỗi code (do gửi test bằng Gmail cá nhân "iungo事務局"), không sửa code — xem Journal #144361 mục D-7. Cấu hình người gửi trên staging/production nằm ngoài ticket.
- Round hiện tại trên Studio: round 5, `aiResult=fail`, `reviewState=tester`, `openBugs=4` — còn 4 bug đang mở gắn với task Studio #365 (xem file `04-tc-list.md` cột ticket bug của từng TC).
- Mọi thao tác CHỈ đụng luồng chuyển khoản (振込) — luồng thanh toán bằng thẻ không có mail mới (ngoại trừ gửi lúc đăng ký thành công qua webhook thẻ ở v1, xem file 03).

## Journal / note từ Redmine (nguyên văn)

**Journal #140604 — Do Van Tu TuDV — 2026-10-06:**

```
★ BÁO CÁO TIẾN ĐỘ AI DEV — #42058 Send mail khi upgrade hợp đồng (free => standard/pro), standard -> pro, hợp đồng lại, extend hợp đồng 1 năm  (06/10/2026)
(Comment TỰ ĐỘNG do workflow AI implement sinh ra từ trạng thái thật của branch —
 không phải ý kiến cá nhân viết tay.)
════════════════════════════════════════════════

Branch: ai-feature-42058 · base: e34a46bcff · HEAD: 54eeb82085
Sprint: sprint-2026-09 · UPDATE — FA-031 (契約プラン・決済情報) + FA-032 (新規アカウント追加): thêm mail thông báo, không đổi UI
Trạng thái: completed (100%) — Hoàn tất — trigger mail 4 case + chờ/huỷ chuyển khoản; nội dung mail chờ REQ-001 (flag mặc định TẮT)

■ 1. ĐÃ LÀM
 • BR-C01 upgrade free→standard/pro/おまとめ (thẻ webhook · chuyển khoản paymentBotSlotV2 · campaign saveCampaign)
 • BR-C02 upgrade standard→pro (thẻ · chuyển khoản); おまとめ→pro không gửi (D-03 A)
 • BR-C03 再契約 (thẻ recontractV2 / recontract · chuyển khoản recontractTransfer / recontract) + QT-03 mua lại gói cho LOA có hợp đồng trả phí đã huỷ
 • BR-C04 gia hạn 1 năm (thẻ handleExtendContractSuccess · chuyển khoản extendContract)
 • BR-C05 gửi lúc đăng ký thành công; chuyển khoản chưa có số TK → WAITING, cron recover:RecoverUpdateInfoUnivapay gửi khi có
 • BR-C06 lỗi mail không ảnh hưởng thanh toán (nuốt Throwable, status ERROR)
 • BR-C07 chỉ chủ hợp đồng; email univa_email → users.email (QT-01 C)
 • BR-C08 振込キャンセル / chuyển khoản thất bại → huỷ mail đang chờ (cancelTransfer 2 nhánh + webhook failed)
 • QT-04 chống gửi trùng bằng 3 cột contract_mail_* trên payment_histories (migration)
 • Feature flag CONTRACT_CHANGE_MAIL_ENABLED (mặc định false) + guard subject rỗng

■ 2. THAY ĐỔI CODE TRÊN BRANCH
 • 54eeb82085 — feat(42058): update implementation — RecoverUpdateInfoUnivapay.php, ContractChangeMailRepositoryInterface.php, BotController.php +11 more (spec c4644cfefaf7be9c) (14 file, +802/-0)

■ 3. ĐÃ KIỂM TỚI ĐÂU
 • Checklist: 20 mục — pass 18 / manual 1 / fail 1
 • ⚠ Container dev KHÔNG có DB/Redis ⇒ chỉ verify tới mức compile/lint + kiểm tĩnh; hành vi thật cần QA runtime.

■ 4. CẦN QA RUNTIME / CÒN HỞ
Cần QA kiểm tay:
 • [TD-16] Idempotency: 1 lần đăng ký = đúng 1 mail (webhook gửi lại / cron chạy lại / song song)
Mục CHƯA ĐẠT (cố ý để mở, chờ chốt/làm tiếp):
 • [TD-19] 4 template emails/contract_change/{upgrade_free,upgrade_pro,recontract,extend_1_year} — nội dung nguyên văn Link html (REQ-001)
TODO còn treo vì spec chưa chốt:
 • REQ-001 nội dung mail (件名 + 本文) 4 case — Link html 401 → Human nhập $SECRET_PROTOTYPE_AUTH hoặc dán nội dung; điền config subjects + 4 blade rồi mới bật CONTRACT_CHANGE_MAIL_ENABLED · chặn: release
 • Migration chưa chạy trên DB dev (container không kết nối MySQL host) → php artisan migrate trước khi deploy code · chặn: runtime

■ 6. ĐIỂM AI TỰ QUYẾT — CẦN BA/TA XÁC NHẬN
 • [D-01][high] QT-04: chống gửi trùng bằng CỘT MỚI trên payment_histories thay vì bảng contract_change_mails
   → đã chọn: Thêm 3 cột contract_mail_type/contract_mail_status/contract_mail_sent_at vào payment_histories (dòng cha parent_month=1 của charge); claim nguyên tử bằng UPDATE ... WHERE contract_mail_status IS NULL; KHÔNG tạo bảng contract_change_mails, bỏ cột context/error_message/to_email (tính lại lúc gửi, lỗi ghi log)
   → căn cứ: qa-technical QT-04 vs TD §3
 • [D-02][medium] Case KHÔNG có dòng payment_histories (campaign EP-24) — gửi thẳng, không ghi cờ
   → đã chọn: Gửi mail trực tiếp không có bookkeeping; chống trùng dựa guard sẵn có bots.has_campaign về 0 sau lần lưu đầu. Kết quả gửi chỉ ghi log contract_change_mail.*. (Đính chính 2026-10-06: 再契約 thẻ recontractV2 chỉ charge khi hợp đồng đã quá hạn nên LUÔN có dòng payment — không thuộc case này; service vẫn có nhánh gửi thẳng phòng dữ liệu lệch)
   → căn cứ: QT-04 + TD §2 Transaction & Idempotency
 • [D-03][medium] QT-01: email người nhận = bot_contracts.univa_email, rỗng thì users.email của chủ hợp đồng
   → đã chọn: Resolve recipient theo (C): univa_email → fallback users.email (admin_id của hợp đồng); cả hai rỗng → status SKIPPED_NO_EMAIL
   → căn cứ: qa-technical QT-01 vs TD §2 notify()
 • [D-04][medium] QT-03: mua lại gói cho LOA có hợp đồng trả phí ĐÃ HUỶ (status=3) qua màn chọn gói → gửi mail 再契約
   → đã chọn: resolveMailType: actionBill=new + bot_id_upgrade + hợp đồng cũ status=3 và contract_type≠free → recontract (ưu tiên trước nhánh upgrade_free)
   → căn cứ: qa-technical QT-03 vs TD §1 «Không gắn mail»
 • [D-05][high] Nội dung mail (REQ-001, Link html 401) chưa có — template placeholder + feature flag TẮT
   → đã chọn: Tạo 4 blade emails/contract_change/* chỉ có khung + marker TODO(REQ-001), subject trong config để rỗng; service chỉ gửi khi CONTRACT_CHANGE_MAIL_ENABLED=true VÀ subject khác rỗng → không thể vô tình gửi mail rỗng. Human phải dán nguyên văn Link html rồi mới bật flag
   → căn cứ: spec §CR-05 / TD §2 Mail templates, §7 Rollout
 • [D-11][medium] 再契約 thẻ (EP-23 reContractChangeCard) khi hợp đồng CHƯA quá hạn — không charge, không qua webhook → KHÔNG gửi mail
   → đã chọn: Chỉ gửi mail 再契約 ở nhánh có charge (webhook recontractV2) đúng bảng hook TD §1; nhánh không charge (khôi phục hợp đồng chờ huỷ/đã huỷ còn hạn) giữ nguyên, không mail
   → căn cứ: TD §1 bảng hook C-03 · D-04 (A)
 • (+ 6 quyết định mức low — xem tab ⚖ Quyết định trên dashboard)

────────────────────────────────────────────────
Sinh tự động lúc 2026-10-06T11:08:47.000Z từ artifact của task "42058_free-standard-pro".
```

**Journal #144361 — Dev Studio — 2026-10-15:**

```
Dev Studio · Nội dung thực hiện

Câu hỏi về mail vào spam đã xong, dựa trên hai file .eml anh gửi trong chat. Kết luận vẫn giữ: không phải lỗi code, vì hai loại mail gửi giống hệt nhau. Mail vào spam là do môi trường dev gửi bằng Gmail cá nhân tên 「iungo事務局」 và Gmail chấm theo nội dung. Bản v2 không còn câu hỏi nào chờ người trả lời; các mục sửa 6 bug QA sẵn sàng thực thi. Việc còn lại nằm ngoài ticket: kiểm cấu hình người gửi trên staging/production.

Hướng sửa:
- D-1 Tên trong 4 mail luôn là username của chủ hợp đồng
- D-2 Người nhận là email UnivaPay của hợp đồng, trống thì email chủ hợp đồng
- D-3 Gia hạn chuyển khoản không còn lỗi khi hợp đồng thiếu email UnivaPay
- D-4 Đổi thẻ sang chuyển khoản tạo dòng chờ số tài khoản đúng
- D-5 Thêm test cho tên, người nhận, Staff, HTML/emoji và おまとめ
- D-6 Kiểm tĩnh hai chỗ sửa luồng thanh toán
- D-7 Ghi kết luận mail standard→pro vào spam, không sửa code

Ảnh hưởng / rủi ro:
Phần mail vào spam không đổi code. Các mục khác giữ như v2: đổi cách lấy tên và người nhận trong 4 mail; sửa nhỏ hai chỗ trong luồng gia hạn và đổi phương thức thanh toán. Cần test hồi quy hai luồng đó; chưa kiểm được runtime.
```

**Journal #144376 — Dev Studio — 2026-10-15:**

```
Dev Studio · Nội dung thực hiện

Bản v3 sửa mục review yêu cầu: kỳ hợp đồng (契約期間) trong mail nâng từ free và mail 再契約 bằng chuyển khoản đang in sai. Lý do: mail gửi khi tiền chưa về, nên hợp đồng vẫn mang hạn cũ, ngày hôm nay, hoặc ngày tạo hợp đồng gốc. Mail sẽ in kỳ mới tính từ ngày đăng ký, cùng công thức hệ thống dùng khi tiền về: 1 năm, gói 2 năm thì 2 năm. Thêm test cho 3 trường hợp review đã tái hiện; các phần khác giữ nguyên.

Hướng sửa:
- D-1 Tính lại 契約期間 cho mail upgrade free và 再契約
- D-2 Thêm test cho 3 trạng thái hợp đồng và gói 2 năm
- D-3 Chạy lại PHPUnit và harness so từng dòng 4 mail

Ảnh hưởng / rủi ro:
Chỉ đổi dòng 契約期間 trong mail nâng từ free và mail 再契約 bằng chuyển khoản; luồng thanh toán và hợp đồng không đổi. Rủi ro: lệch vài ngày khi khách chuyển khoản muộn so với ngày đăng ký. Chưa kiểm được runtime.
```

**Journal #144402 — Dev Studio — 2026-10-15:**

```
Dev Studio · Nội dung thực hiện

Bản v4 bỏ cờ CONTRACT_CHANGE_MAIL_ENABLED theo yêu cầu của tuanpa, nên sau khi deploy 4 mail hướng dẫn chuyển khoản tự gửi, không cần bật cấu hình. Cờ này chỉ có từ lúc chưa có nội dung mail; nay nội dung và subject đã đủ. Các điều kiện khác giữ nguyên: chỉ chuyển khoản, đã có số tài khoản, đủ dữ liệu. Đổi lại sẽ không còn công tắc tắt nhanh; muốn dừng gửi phải revert hoặc deploy lại.

Hướng sửa:
- D-1 Xoá cờ trong config và service gửi mail
- D-2 Sửa test không còn phụ thuộc cờ
- D-3 Sửa harness và chạy lại kiểm tra
- D-4 Kiểm không còn chỗ nào dùng cờ và ghi vào bàn giao

Ảnh hưởng / rủi ro:
Chỉ bỏ điều kiện cờ trong config và service gửi mail. Sau deploy, mail gửi thật cho khách ngay mà không còn công tắc tắt nhanh. Nội dung và điều kiện gửi khác không đổi.
```

**Journal #144563 — Dev Studio — 2026-10-15:**

```
Dev Studio · Nội dung thực hiện

Đã tìm ra nguyên nhân bug #43221: 再契約 gói 2 năm trả chuyển khoản nhưng hạn chỉ hiện 1 năm. Màn 再契約 khi chọn chuyển khoản không gửi số năm lên server, nên server mặc định 1 năm, trong khi số tiền vẫn tính cho 2 năm. Ngoài ra, khi tiền về hệ thống luôn cộng 1 năm cho 再契約 chuyển khoản. Bản v5 sửa cả hai chỗ; mail tự in đúng 2 năm vì quy tắc tính kỳ đã có sẵn. Phần giao diện và webhook cần QA chạy lại trên môi trường test.

Hướng sửa:
- D-1 Màn 再契約 gửi số năm khi thanh toán chuyển khoản
- D-2 Tiền về thì cộng 2 năm cho gói 2 năm
- D-3 Thêm test mail 再契約 gói 2 năm
- D-4 Kiểm tĩnh luồng đăng ký với gói 2 năm

Ảnh hưởng / rủi ro:
Đụng màn 再契約 (JS) khi trả chuyển khoản và nhánh 再契約 chuyển khoản của webhook UnivaPay. Gói 1 năm và luồng thẻ không đổi hành vi. Rủi ro: trình duyệt dùng bản JS cũ nếu không tăng version; dữ liệu 再契約 2 năm cũ đã bị ghi 1 năm. Chưa kiểm được runtime.
```

**Journal #144626 — Dev Studio — 2026-10-15:**

```
Dev Studio · Nội dung thực hiện

Đã tìm ra chỗ lưu sai hạn: khi hợp đồng còn hạn mà 再契約 gói 2 năm bằng chuyển khoản, hệ thống giữ nguyên hạn cũ trong DB tới khi tiền về. Hợp đồng đã hết hạn thì đã lưu đúng 2 năm. Bản v6 sửa để ngay lúc đăng ký đã lưu hạn mới (ngày đăng ký + 2 năm, khớp với mail và với lúc tiền về), đồng thời giữ hạn cũ để trả lại nếu khách bấm 振込キャンセル. Đây là lựa chọn mặc định vì anh cho biết cách giữ hạn cũ là sai; nếu anh muốn kỳ mới nối tiếp hạn cũ thì báo để đổi.

Hướng sửa:
- D-1 Chạy lại kiểm tra trên commit 7e7dc6fff9
- D-2 Ghi bàn giao cho #43221 và 8 bug automation
- D-3 再契約 chuyển khoản cho hợp đồng còn hạn lưu hạn mới ngay khi đăng ký
- D-4 振込キャンセル trả lại hạn cũ cho 再契約 đang chờ tiền
- D-5 Kiểm tĩnh hai chỗ sửa bằng script so trước/sau

Ảnh hưởng / rủi ro:
Đụng hai chỗ trong luồng thanh toán đang chạy production: lúc đăng ký 再契約 chuyển khoản cho hợp đồng còn hạn, và lúc 振込キャンセル hợp đồng đang chờ tiền của 再契約. Các luồng khác giữ nguyên. Rủi ro: lệch hạn nếu thao tác huỷ không trả lại đủ hạn cũ; cần test hồi quy huỷ chuyển khoản, gia hạn và đổi phương thức thanh toán.
```
