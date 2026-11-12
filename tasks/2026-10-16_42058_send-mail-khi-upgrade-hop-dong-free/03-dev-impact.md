# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT KHÔNG THEO FORMAT CHUẨN.** Redmine #42058 KHÔNG có section "Đánh giá ảnh hưởng" (1. Nguyên nhân / 2. Cách fix / 3. Caller / 4.1-4.3) trong Description. Nội dung dưới đây được `/new-task` **tổng hợp lại** từ 6 Journal AI-dev-report (format riêng: `■ 1 ĐÃ LÀM`, `■ 6 ĐIỂM AI TỰ QUYẾT` ở bản v1, và `D-1/D-2/...` ở các bản v2→v6) — xem nguyên văn đầy đủ ở `01-bug-task.md`. Mỗi bullet dưới đây giữ nguyên câu chữ Dev viết, chỉ xếp lại vào đúng mục của template.
> ⚠️ **BẮT BUỘC Tester/Leader đọc lại 6 Journal gốc** trước khi tick checkbox "Tester verify" — đây là bản dàn lại cấu trúc do AI làm, KHÔNG phải Dev tự điền đúng 4 mục chuẩn.
> ℹ️ Bổ sung: Studio task #365 (`task_get_context`) đã có 11 `requirements` REQ-001→REQ-011 do AI review tự rút ra từ spec + các Journal này — tham chiếu thêm khi cần đối chiếu coverage ở `/review-tc` (REQ-005, REQ-006, REQ-010 đang có **conflict chờ BA** giữa spec và nhánh Dev chọn).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Do Van Tu TuDV (assignee Redmine) — bản v1 (Journal #140604) ký tên "AI DEV"; các bản v2→v6 (2026-10-15) ký "Dev Studio" |
| Commit / Pull Request | `<chưa có PR link>`; commit v1 = `54eeb82085` (base `e34a46bcff`); commit v5/v6 = `7e7dc6fff9` |
| Branch | `ai-feature-42058` |
| Ngày submit đánh giá | 2026-10-06 (v1, Journal #140604) — update thêm 2026-10-15 (v2→v6, Journal #144361/144376/144402/144563/144626) |
| Auto-filled | 2026-10-16 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ đọc kỹ cảnh báo ở đầu file trước khi tick: nội dung dưới là bản AI dàn lại từ format journal khác chuẩn, không phải Dev tự điền đúng 4 mục.

---

## 1. Nguyên nhân

> Ticket là **Feature mới** (không phải bug) — trước #42058, hệ thống KHÔNG gửi mail cho 4 case thay đổi hợp đồng dưới đây. Mục "Nguyên nhân" ở đây là bối cảnh nghiệp vụ + các bug phát sinh trong quá trình implement (được tìm & sửa ở v2→v6).

**Bối cảnh nghiệp vụ** (chưa có mail, cần thêm):
1. upgrade hợp đồng (free => standard/pro)
2. upgrade hợp đồng (standard -> pro)
3. 再契約 (hợp đồng lại)
4. extend hợp đồng 1 năm

**Bug phát sinh & đã sửa trong quá trình implement:**
- Mail standard→pro vào spam (môi trường dev): "không phải lỗi code, vì hai loại mail gửi giống hệt nhau. Mail vào spam là do môi trường dev gửi bằng Gmail cá nhân tên 「iungo事務局」 và Gmail chấm theo nội dung." (Journal #144361, D-7 — **không sửa code**, nằm ngoài ticket: "kiểm cấu hình người gửi trên staging/production.")
- 契約期間 (kỳ hợp đồng) in sai trong mail upgrade-free và mail 再契約 chuyển khoản: "mail gửi khi tiền chưa về, nên hợp đồng vẫn mang hạn cũ, ngày hôm nay, hoặc ngày tạo hợp đồng gốc." (Journal #144376)
- **Bug #43221** — 再契約 gói 2 năm trả chuyển khoản nhưng hạn chỉ hiện 1 năm: "Màn 再契約 khi chọn chuyển khoản không gửi số năm lên server, nên server mặc định 1 năm, trong khi số tiền vẫn tính cho 2 năm. Ngoài ra, khi tiền về hệ thống luôn cộng 1 năm cho 再契約 chuyển khoản." (Journal #144563)
- Lưu sai hạn hợp đồng khi còn hạn: "khi hợp đồng còn hạn mà 再契約 gói 2 năm bằng chuyển khoản, hệ thống giữ nguyên hạn cũ trong DB tới khi tiền về. Hợp đồng đã hết hạn thì đã lưu đúng 2 năm." (Journal #144626)

## 2. Cách fix

**Bản v1 (Journal #140604, commit `54eeb82085`):**
- BR-C01 upgrade free→standard/pro/おまとめ (thẻ webhook · chuyển khoản `paymentBotSlotV2` · campaign `saveCampaign`)
- BR-C02 upgrade standard→pro (thẻ · chuyển khoản); おまとめ→pro **không gửi** (D-03 A)
- BR-C03 再契約 (thẻ `recontractV2`/`recontract` · chuyển khoản `recontractTransfer`/`recontract`) + QT-03 mua lại gói cho LOA có hợp đồng trả phí đã huỷ
- BR-C04 gia hạn 1 năm (thẻ `handleExtendContractSuccess` · chuyển khoản `extendContract`)
- BR-C05 gửi lúc đăng ký thành công; chuyển khoản chưa có số TK → `WAITING`, cron `recover:RecoverUpdateInfoUnivapay` gửi khi có
- BR-C06 lỗi mail không ảnh hưởng thanh toán (nuốt Throwable, status `ERROR`)
- BR-C07 chỉ chủ hợp đồng; email `univa_email` → `users.email` (QT-01 C)
- BR-C08 振込キャンセル / chuyển khoản thất bại → huỷ mail đang chờ (`cancelTransfer` 2 nhánh + webhook failed)
- QT-04 chống gửi trùng bằng 3 cột `contract_mail_*` trên `payment_histories` (migration)
- Feature flag `CONTRACT_CHANGE_MAIL_ENABLED` (mặc định `false`) + guard subject rỗng

**Bản v2 (Journal #144361):**
- D-1 Tên trong 4 mail luôn là username của chủ hợp đồng
- D-2 Người nhận là email UnivaPay của hợp đồng, trống thì email chủ hợp đồng
- D-3 Gia hạn chuyển khoản không còn lỗi khi hợp đồng thiếu email UnivaPay
- D-4 Đổi thẻ sang chuyển khoản tạo dòng chờ số tài khoản đúng
- D-5 Thêm test cho tên, người nhận, Staff, HTML/emoji và おまとめ
- D-6 Kiểm tĩnh hai chỗ sửa luồng thanh toán
- D-7 Ghi kết luận mail standard→pro vào spam, **không sửa code**

**Bản v3 (Journal #144376):**
- D-1 Tính lại 契約期間 cho mail upgrade free và 再契約 — "kỳ mới tính từ ngày đăng ký, cùng công thức hệ thống dùng khi tiền về: 1 năm, gói 2 năm thì 2 năm"
- D-2 Thêm test cho 3 trạng thái hợp đồng và gói 2 năm
- D-3 Chạy lại PHPUnit và harness so từng dòng 4 mail

**Bản v4 (Journal #144402):**
- D-1 Xoá cờ `CONTRACT_CHANGE_MAIL_ENABLED` trong config và service gửi mail (theo yêu cầu "tuanpa" — nội dung & subject đã đủ) → **4 mail tự gửi thật sau deploy, không còn công tắc tắt nhanh**
- D-2 Sửa test không còn phụ thuộc cờ
- D-3 Sửa harness và chạy lại kiểm tra
- D-4 Kiểm không còn chỗ nào dùng cờ và ghi vào bàn giao

**Bản v5 (Journal #144563 — fix bug #43221):**
- D-1 Màn 再契約 gửi số năm khi thanh toán chuyển khoản
- D-2 Tiền về thì cộng 2 năm cho gói 2 năm (trước đó luôn cộng 1 năm)
- D-3 Thêm test mail 再契約 gói 2 năm
- D-4 Kiểm tĩnh luồng đăng ký với gói 2 năm

**Bản v6 (Journal #144626, commit `7e7dc6fff9`):**
- D-3 再契約 chuyển khoản cho hợp đồng **còn hạn** lưu hạn mới (ngày đăng ký + 2 năm) **ngay khi đăng ký**, thay vì giữ hạn cũ tới khi tiền về
- D-4 振込キャンセル trả lại hạn cũ cho 再契約 đang chờ tiền
- D-5 Kiểm tĩnh hai chỗ sửa bằng script so trước/sau
- Dev tự nêu: "Đây là lựa chọn mặc định vì anh cho biết cách giữ hạn cũ là sai; nếu anh muốn kỳ mới nối tiếp hạn cũ thì báo để đổi." → Leader nên xác nhận lại nếu có khách hàng complaint về cách tính kỳ.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `RecoverUpdateInfoUnivapay.php` | cron recover job | Gửi mail trễ khi chuyển khoản nhận được số TK sau (BR-C05) |
| 2 | `ContractChangeMailRepositoryInterface.php` | repository mới | Chống gửi trùng qua 3 cột `contract_mail_*` (QT-04) |
| 3 | `BotController.php` + 11 file khác | commit `54eeb82085`, 14 file, +802/-0 | Dev KHÔNG liệt kê đủ tên 14 file — chỉ nêu 3/14 + "+11 more" |
| 4 | Màn 再契約 (JS) + webhook UnivaPay nhánh 再契約 chuyển khoản | commit `7e7dc6fff9` | Fix bug #43221 + lưu hạn mới khi đăng ký gói 2 năm (v5, v6) |

⚠️ **Input thiếu**: Dev không liệt kê đầy đủ tên 14 file trong commit `54eeb82085` (chỉ nêu 3/14 + "+11 more"); commit `7e7dc6fff9` cũng không kèm file list. Cần hỏi Dev hoặc đọc diff thật (`task_get_context` sections `spec_delta`/`dev_impact` trên Studio task #365 nếu có) trước khi kết luận coverage đủ ở BƯỚC 2 của `/review-tc`.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `paymentBotSlotV2` (webhook UnivaPay, thẻ) | — | Direct | Upgrade free→standard/pro (BR-C01) |
| F2 | `recontractV2` / `recontract` (webhook, thẻ) | — | Direct | 再契約 (BR-C03) — chỉ gửi mail ở nhánh **có charge** |
| F3 | `recontractTransfer` / `recontract` (chuyển khoản) | — | Direct | 再契約 (BR-C03) |
| F4 | `extendContract` (chuyển khoản) / `handleExtendContractSuccess` (thẻ) | — | Direct | Gia hạn 1 năm (BR-C04) |
| F5 | `cancelTransfer` (2 nhánh) + webhook failed | — | Direct | Huỷ mail đang chờ khi 振込キャンセル / chuyển khoản thất bại (BR-C08) |
| F6 | `saveCampaign` | — | Direct | おまとめ upgrade — nhưng おまとめ→pro **không gửi mail** (D-03 A) |
| F7 | `recover:RecoverUpdateInfoUnivapay` (cron) | `RecoverUpdateInfoUnivapay.php` | Direct | Gửi mail trễ khi chuyển khoản nhận đủ số TK (BR-C05) |
| F8 | Màn 再契約 (JS, chọn chuyển khoản) | — | Direct | v5 — phải gửi số năm lên server (fix bug #43221) |
| F9 | Logic cộng hạn hợp đồng khi tiền về (再契約 chuyển khoản) | — | Direct | v5 — cộng đúng số năm theo gói, trước đó luôn cộng 1 năm (fix bug #43221) |
| F10 | Logic lưu hạn hợp đồng lúc đăng ký 再契約 chuyển khoản (hợp đồng còn hạn) | — | Direct | v6 — lưu hạn mới ngay, giữ hạn cũ để trả lại nếu 振込キャンセル |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `payment_histories.contract_mail_type` / `.contract_mail_status` / `.contract_mail_sent_at` (3 cột mới, migration) | CREATE | Chống gửi trùng mail (QT-04); claim nguyên tử bằng `UPDATE ... WHERE contract_mail_status IS NULL` |
| D2 | Config subjects (4 mail) + 4 blade `emails/contract_change/{upgrade_free,upgrade_pro,recontract,extend_1_year}` | CREATE/UPDATE | Nội dung mail (REQ-001). Từ v4: KHÔNG còn cờ `CONTRACT_CHANGE_MAIL_ENABLED` — nội dung/subject gửi thẳng |
| D3 | `bot_contracts` (hạn hợp đồng / expire date) | UPDATE | 再契約 chuyển khoản gói 2 năm: lưu hạn mới ngay lúc đăng ký thay vì chờ tiền về (v6); 振込キャンセル trả lại hạn cũ (v6) |
| D4 | Dữ liệu 再契約 2 năm cũ (trước fix bug #43221) | — (chưa rõ có migrate lại không) | Dev tự nêu rủi ro: "dữ liệu 再契約 2 năm cũ đã bị ghi 1 năm" — ⚠️ **Input thiếu**: chưa rõ có script backfill lại data cũ hay không, cần hỏi Dev |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Upgrade hợp đồng free→standard/pro (FA-031), kể cả おまとめ | F1, F6, D1, D2 | Medium — mail hoàn toàn mới, có nhánh おまとめ không gửi dễ nhầm |
| T2 | Upgrade hợp đồng standard→pro | F1, D1, D2 | Low |
| T3 | 再契約 (hợp đồng lại) — kể cả QT-03 mua lại gói cho LOA đã huỷ | F2, F3, F8, F9, F10, D1, D3 | **High** — sửa 6 lần (v1→v6), đụng luồng thanh toán production, bug #43221 vừa tìm ra, còn D4 rủi ro data cũ |
| T4 | Extend hợp đồng 1 năm | F4, D1, D2 | Low |
| T5 | 振込キャンセル / chuyển khoản thất bại (huỷ mail đang chờ) | F5, D1, D3 | Medium |
| T6 | Đổi phương thức thanh toán (thẻ ↔ chuyển khoản) | Journal #144361 D-4 ("Đổi thẻ sang chuyển khoản tạo dòng chờ số tài khoản đúng") | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót — **đặc biệt 11/14 file chưa có tên ở commit `54eeb82085`**)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — **D4 cần Dev xác nhận có backfill data cũ không**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
