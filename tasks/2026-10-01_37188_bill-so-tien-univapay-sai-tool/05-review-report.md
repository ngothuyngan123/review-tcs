# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #270 (round 1, `ai_fixbug_37188`) |
| Tổng số TC review | 38 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 10/14 mục có TC — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (2 file, +52/-4) | 9/14 điểm có TC — **CHƯA ĐỦ** |

**Kết luận**: 19/28 vùng ảnh hưởng đủ TC · 2 GAP · 5 RISK

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` + `F5 — changeTypePayment` (lối khách đổi kỳ thật, qua màn 「お支払い期間の変更」) | `dev-impact` | NEW-1, NEW-3, NEW-9, NEW-10, NEW-27, NEW-28, NEW-29 (đều dựng "đổi kỳ" bằng sửa thẳng dữ liệu) | **RISK** — không TC nào đổi kỳ qua màn thật giữa lúc tạo giao dịch và lúc nhận kết quả. Lối thật còn sinh trạng thái "đã đăng ký đổi kỳ, áp dụng từ lần thu sau" (dòng xám 「次回決済日：…から年払いに変更されます」, kho TC-BLP-155/162) mà cách sửa dữ liệu không tạo ra. Bằng chứng: NEW-29 actual đọc được 「年間一括払い 次回決済から月払いに変更する」 = trạng thái **chưa từng** đổi kỳ. Bug Studio #1459 có thể là hệ quả của setup này (xem C1/C2) | `[BLOCKER]` |
| G2 | Hạn hợp đồng · nhãn kỳ · chia 12 dòng sau khi nhận kết quả, khi kỳ bị đổi giữa chừng (`T1`; rủi ro #3 của Dev — "cố ý để ngoài phạm vi") | `diff code` | NEW-10 (chỉ ghi nhận, không chấm), NEW-1 (expected "hạn được đẩy tới kỳ kế tiếp" không nói +1 tháng hay +1 năm) | **GAP** (câu 5 — nhánh Dev nói "bất biến"): Studio actual của NEW-10 = thu tiền tháng 10.780 nhưng lý do thu `standard_year`, còn 365 ngày, chia 12 dòng × 898 (tổng 10.776 ≠ 10.780), dòng cha bị ẩn → NEW-30 actual: màn 紹介報酬 hiện 報酬額 = 177 (tính trên dòng con). Theo kho TC-BLP-162/155, đổi kỳ chỉ có hiệu lực **từ lần thu sau** → giao dịch tạo trước khi đổi phải mang nhãn + hạn của kỳ cũ. Không TC nào kiểm hạn hợp đồng theo quy tắc này. → §8 #2 | `[BLOCKER]` |
| G3 | `F1 — chargeUnivapayTransferBots` (thu tiền định kỳ bằng chuyển khoản) | `dev-impact` | không có | **GAP** — Dev kê hàm này ở mục 3, nhưng 38 TC chỉ đi luồng thẻ. Chưa ai xác nhận kết quả chuyển khoản có đi qua `handleCallbackBillJob` (dùng số tiền thực thu) hay không | `[MAJOR]` |
| G4 | Tên trường `charged_amount` / `requested_amount` trong payload Univapay thật (rủi ro #1 của Dev) | `diff code` | NEW-25 (manual, **chưa chạy**) | **RISK** — mọi TC callback (NEW-19/20/21/23…) dùng payload tự dựng nên chỉ chứng minh code đọc đúng tên trường **do tester đặt**. NEW-26 actual: môi trường test **không có** Univapay sandbox. Không có bằng chứng thì lớp 1/2 có thể không bao giờ chạy trên production | `[MAJOR]` |
| G5 | Trục "đổi gói sau khi tạo giao dịch" (`dev_impact`: đổi kỳ / gói / slot) | `diff code` | NEW-38 (**chưa chạy**) | **RISK** — trục kỳ (NEW-1/3) và trục slot (NEW-5) đã pass, trục gói 0 TC đã chạy | `[MAJOR]` |
| G6 | Nhánh callback ngoài phạm vi: change_card · change_sub_card · extend_contract · bill_again · bill_max_friend · new · upgrade_pro (`getUnivapayChargedAmount` được truyền chung) | `diff code` | NEW-31, NEW-32, NEW-33 | **RISK** (câu 5) — oracle chỉ là "giống bản release" + chèn 99.999 vào payload. Quy tắc mới của ticket ("số ghi nhận = số Univapay thực thu") chưa được kiểm ở các nhánh này, trong khi Dev tự ghi nhận **3 handler khác vẫn tính lại tiền theo hợp đồng** → có thể đang sai sẵn. → §8 #4 | `[MAJOR]` |
| G7 | Callback **thất bại**: số tiền bản ghi lỗi + `amount_payment` nay lấy theo `requested_amount` (hành vi đổi — override nằm trước nhánh thành công/thất bại, BotController:11565) | `diff code` | NEW-6 | **RISK** — NEW-6 pass nhưng expected chỉ "ghi nhận, báo leader", chưa có quy tắc. → §8 #3 | `[MAJOR]` |

- G4 · G5 · G7: TC đã có — **không đẻ TC trùng** (BƯỚC 5b). Việc phải làm: chạy NEW-25 (product) + NEW-38; cập nhật expected NEW-6 sau khi §8 #3 được chốt.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 24 quan điểm Trigger khớp task · 11 chưa cover đủ

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `ENV-003` | Cao | **RISK** — 0/38 TC chạy production. Kho TC-BLP-392: giá plan production khác dev/staging → mọi TC kiểm tiền phải chạy production (RULE-08). Xử lý: chạy NEW-37 + NEW-25 trên product + TC-JOB001-01 | `[MAJOR]` |
| Q2 | `JOB-001` | Cao | **GAP theo mã** — nội dung job chỉ có ở NEW-24 (mã lạ) và chỉ chạy local. Xử lý: đổi mã NEW-24 sang `JOB-001` + TC-JOB001-01 (job thật trên product) | `[BLOCKER]` |
| Q3 | `PAY-BATCH-001` | Cao | **RISK RULE-01** — theo mã chỉ có Abnormal (NEW-3, NEW-5); Normal (TC tái hiện ticket NEW-1) mang mã lạ, Boundary (NEW-7) mang `FUNC-004`. Xử lý: đổi mã NEW-1 → `PAY-BATCH-001`; TC-PAYBATCH001-01/02/03 bổ sung lối thật | `[MAJOR]` |
| Q4 | `PAY-CONFIRM-001` | Cao | **RISK RULE-01** — chỉ có Normal (NEW-4, NEW-17). Thiếu Abnormal (giao dịch thất bại không được sinh hoa hồng) + Boundary (số tiền không chia hết 12 → dòng con hoa hồng) | `[MAJOR]` |
| Q5 | `OUT-TRUTH-001` | Cao | **RISK RULE-01** — 3 TC đều Normal (NEW-28, NEW-29 fail, NEW-30). Thiếu Abnormal: bản ghi lỗi nay mang số tiền (G7) có bị hiện lên 決済履歴 không (kho TC-BLP-291: lịch sử bill FAIL không hiện ở màn user) | `[MAJOR]` |
| Q6 | `OUT-EXPORT-001` | Cao (nâng) | **RISK RULE-01** — chỉ NEW-35 Normal (tháng). Thiếu Boundary: lĩnh thu thư của giao dịch 2 năm (232.848) phải in 1 dòng, không tách 24 dòng | `[MAJOR]` |
| Q7 | `DATA-AUDIT-001` | Cao | **RISK** — `bot_life_cycle.data.amount` (D5) có hiển thị trong modal 操作履歴 (kho TC-BLP-225: modal có trường số tiền + kỳ hạn) nhưng không TC nào mở 操作履歴, chỉ kiểm dữ liệu "nhật ký" | `[MAJOR]` |
| Q8 | `REG-SHARED-001` | Cao | **RISK RULE-01** — chỉ Normal (NEW-31, NEW-32), oracle "giống release" (xem G6). Thiếu Boundary theo quy tắc nghiệp vụ | `[MAJOR]` |
| Q9 | `PAY-STATE-001` | Cao | **RISK** — chỉ NEW-37 (manual, **chưa chạy**). Đối soát 3 nơi là phép quyết định của ticket | `[MAJOR]` |
| Q10 | `NOTI-MAIL-001` | Cao (nâng) | **RISK** — chỉ NEW-36 (manual, **chưa chạy**) | `[MAJOR]` |
| Q11 | `INTG-HOOK-001` | Cao | **RISK RULE-01 theo mã** — chỉ Abnormal (NEW-9, NEW-14). Nội dung Normal có ở NEW-19 (`INTG-HOOK-002`), Boundary "callback tới rất trễ (hợp đồng đã sang chu kỳ khác)" nằm lẫn trong NEW-1. Xử lý: tách phần "callback rất trễ" của NEW-1 thành TC Boundary mang mã `INTG-HOOK-001` — không đẻ TC mới | `[MINOR]` |

- Đã loại khỏi phạm vi: `SYNC-APP-*` (kho FA-031 không có nhóm App mobile) · `PERM-*` (không đổi quyền) · `DATA-MIG-001` / `DATA-BACKUP-001` (không đổi cấu trúc bảng) · `PAY-PLAN-001` / `PAY-LIMIT-001` (không đổi gói/giới hạn) · màn phân bổ của admin portal nội bộ (kho MT-00b đang chờ chốt phạm vi).

---

## 3. TC trùng lặp nội dung

Đã rà 38 TC, không phát hiện trùng lặp. Các cặp gần giống đã xét và giữ lại: NEW-2 / NEW-18 (đối chứng âm ở 2 luồng khác nhau: bill_job vs recontractV2) · NEW-20 / NEW-23 biến thể 1 (thiếu trường vs trường = 0) · NEW-28 / NEW-37 (auto 1 màn vs manual đối soát 3 nơi) · NEW-11 / NEW-16 (qua màn thật vs payload không có số tiền).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-29 (fail, bug Studio #1459 High) | Nguồn của 「ご利用料金」 ở màn 契約詳細 | = số tiền lần thu gần nhất (`amount_payment`) — 10,780円 | `spec-features/admin/detail-contract/db/db-mapping.md:445/466/498`: 「ご利用料金」 = **Computed** từ `basic_fee` + plan + kỳ. Ngược lại `spec-features/admin/billing-plan/feature-spec.md:99/181/509/519`: = `bot_contracts.amount_payment`. **Spec tự mâu thuẫn 2 nơi** | (a) TC đúng, màn 契約詳細 phải đọc `amount_payment` → bug #1459 thật · (b) màn hiển thị giá theo kỳ là đúng thiết kế → NEW-29 sai expected, #1459 là false positive | `[MAJOR]` | Dev / PM |
| C2 | `CONF-KHO` | NEW-29 | Số tiền ở 契約詳細 khi kỳ đang hiển thị khác kỳ của lần thu gần nhất | 10,780円 (số đã thu) dù màn đang hiện 「年間一括払い」 | kho TC-BLP-155/156/162: "Số tiền ở màn list và màn detail hiển thị theo **GIÁ** của kỳ đang hiển thị". Kho TC-BLP-130 lại ghi "ご利用料金 khớp `amount_payment`" — 2 TC kho chỉ thống nhất khi kỳ không đổi | (a) NEW-29 đúng, kho TC-BLP-155/162 cần sửa · (b) kho đúng, NEW-29 sai expected. Lưu ý: tiền đề của NEW-29 dựng bằng sửa dữ liệu (G1) — chạy lại theo lối thật (TC-PAYBATCH001-01) thì cả 2 nguồn đều ra 10,780円, mâu thuẫn có thể tự biến mất | `[MAJOR]` | Leader |

**Đã rà**: 38 TC × `spec-features/admin/billing-plan/feature-spec.md` + `spec-features/admin/detail-contract/` + `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (nhóm Đổi kỳ thanh toán · Hợp đồng lại · Job bill định kỳ · Lịch sử thanh toán · Lịch sử thao tác) — phát hiện C1, C2.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | NEW-29 | TC fail; bug Studio #1459 (High, open) **chưa có ticket Redmine** (`redmine_id = null`, `bug_tickets` rỗng) | Chưa raise Redmine vội: chạy TC-PAYBATCH001-01 (lối thật) + chốt C1/C2 trước. Lối thật vẫn hiện 116,424円 → raise Redmine gắn #37188 |
| I2 | `[BLOCKER]` | NEW-27 | TC fail; bug Studio #1460 (Medium, open) **chưa có ticket Redmine**. Studio actual: phần fail là 2 dòng log in nguyên token (BotController:11998 `event callback univapay`, :11635 `univapay token`) **có từ trước bản fix** (`git show be034a2981^`); dòng cảnh báo lệch số tiền do fix thêm vào thì sạch | Raise ticket bảo mật **riêng** (lộ token trong log), không chặn #37188. Tách TC (xem I6) |
| I3 | `[MAJOR]` | Toàn bộ (RULE-08 / ENV-003) | 34/38 TC chạy ở **local**, 0 TC production; môi trường không có Univapay sandbox (NEW-26 actual) nên mọi kết quả thanh toán là payload giả lập. Task chạm **job nền + bill tiền** | Chạy NEW-25, NEW-36, NEW-37 + TC-JOB001-01 trên product trước khi đóng ticket |
| I4 | `[MAJOR]` | NEW-1, NEW-3, NEW-9, NEW-10, NEW-27, NEW-28, NEW-29, NEW-35, NEW-36 | Tiền đề "đổi kỳ / đổi slot sau khi tạo giao dịch" không ghi cách dựng; người khác không dựng lại được bằng thao tác màn hình (check 2). Thực tế runner sửa thẳng dữ liệu → trạng thái không có dòng xám đổi kỳ, khác lối thật (G1) | Ghi rõ cách dựng trong tiền đề; bổ sung lối thật bằng TC-PAYBATCH001-01/02 |
| I5 | `[MAJOR]` | NEW-1 | Expected "hạn hợp đồng được đẩy tới kỳ kế tiếp" không đo lường được — không nói +1 tháng hay +1 năm, đúng chỗ rủi ro nhãn kỳ (G2) | Ghi ngày hết hạn cụ thể theo quy tắc chốt ở §8 #2 |
| I6 | `[MAJOR]` | NEW-27 | Không atomic: gộp (a) nội dung dòng cảnh báo lệch do fix thêm và (b) toàn bộ log không chứa token — (b) fail vì code cũ, làm TC của fix bị đánh fail | Tách (b) thành TC riêng gắn ticket bảo mật ở I2 |
| I7 | `[MAJOR]` | NEW-6, NEW-10 | Expected không phân định Đạt / Không đạt ("ghi nhận và báo cáo cho leader, không tự kết luận") | Cập nhật expected sau khi §8 #2, #3 được chốt |
| I8 | `[MINOR]` | NEW-38 | Gắn `DATA-DB-001` nhưng nội dung là trục đổi gói của luồng thu định kỳ (`PAY-BATCH-001`); `DATA-DB-001` là phạm vi ghi giữa 2 hợp đồng (đã có NEW-8) | Đổi mã sang `PAY-BATCH-001` |
| I9 | `[NIT]` | NEW-24 | Studio actual: runner tạm đặt `is_active=0` cho 140 hợp đồng ngoài phạm vi rồi trả lại để job chỉ chạm 1 hợp đồng | Chỉ chấp nhận ở local; ghi rõ ở tiền đề là không làm cách này trên staging/product dùng chung |

---

## 6. TCs thừa / ngoài phạm vi task

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | NEW-34 | Test layer màn 決済履歴 cho **bản ghi cũ** — fix không chạm view, expected là "bản ghi cũ vẫn sai" (không kiểm hành vi nào của fix) | `spec_delta.files[]` chỉ có job + BotController; phạm vi dữ liệu cũ đã có NEW-26 thống kê | Chuyển sang checklist recover data (mục 5 file 03), không chạy mỗi vòng fix | `[NIT]` |

- Gate: NEW-34 **không** phải TC duy nhất cover REQ-009 / recover data (NEW-26 cover) → flag hợp lệ.

---

## 7. TCs đề xuất bổ sung (12)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (nhóm Đổi kỳ thanh toán · Hợp đồng lại · Job bill định kỳ thẻ/chuyển khoản · Lịch sử thanh toán · Lịch sử thao tác · Môi trường & regression · MT-13/MT-00b) |
| Vùng regression phát hiện từ kho | TC-BLP-155/162 (đổi kỳ áp dụng từ lần thu sau) · TC-BLP-225 (modal 操作履歴 có số tiền) · TC-BLP-291 (bill lỗi không hiện ở màn user) · TC-BLP-294 (tổng 12 dòng con = dòng cha) · TC-BLP-300 (chuyển khoản) · TC-BLP-307 (job monitor đối soát) · TC-BLP-392 (giá production khác) |
| Conflict expected vs kho | NEW-29 vs TC-BLP-155/162 → C2, đã đưa §4 + §8 |
| GAP dùng lại TC kho (không viết mới) | Không |
| Căn cứ TC regression `R<x>` | R1 ← kho TC-BLP-307 + `dev_impact` "giao dịch cũ … cần test lớp fallback" · R2 ← kho TC-BLP-294 + 03 D1 "các dòng chia 12 tháng cũng theo số này" |
| Xác nhận chống trùng | Đã đối chiếu 38 TC ở BƯỚC 0 + kho — **không TC đề xuất nào trùng**. G4 / G5 / G7 / Q9 / Q10 không đẻ TC vì đã có NEW-25 / NEW-38 / NEW-6 / NEW-37 / NEW-36 |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PAYBATCH001-01 | UI | PAY-BATCH-001 | Job bill định kỳ — thẻ | Normal | auto | Tất cả | Thu tiền định kỳ: khách đổi kỳ tháng sang năm qua màn お支払い期間の変更 trong lúc chờ kết quả thanh toán, số tiền ghi nhận vẫn là tiền tháng | Hợp đồng スタンダード 月払い, thanh toán thẻ Univapay, 次回決済日 là hôm nay, đơn giá cơ bản 10.780. Runner giữ lại kết quả thanh toán (charge_finished) của job, chưa trả về hệ thống. Đăng nhập owner của hợp đồng | 1. Chạy job thu tiền định kỳ hằng ngày, ghi lại 課金ID của giao dịch 10.780 vừa tạo. 2. Khi kết quả thanh toán chưa về, mở 契約情報・領収書 rồi vào 契約詳細 của hợp đồng. 3. Bấm 「次回決済から年払いに変更する」 và hoàn tất. 4. Xác nhận màn hiện dòng xám 「次回決済日：…から年払いに変更されます」. 5. Cho kết quả thanh toán thành công của đúng 課金ID đó về hệ thống. 6. Mở 決済履歴・領収書のダウンロード, mở chi tiết tháng, tìm dòng theo 課金ID. 7. Quay lại 契約詳細, đọc 「ご利用料金」 và 「お支払い期間」 | Đơn giá 10.780; số đã thu 10.780; số theo kỳ năm 116.424 | Dòng có 課金ID vừa ghi hiển thị 利用料 (税込) 10,780円. Màn 契約詳細: 「お支払い期間」 vẫn là 月払い kèm dòng xám đổi sang 年払い, 「ご利用料金」 10,780円 (税込). Không nơi nào hiển thị 116,424円 |  | Lấp G1 · thay cho tiền đề sửa thẳng dữ liệu của NEW-1 / NEW-29 · Đánh giá spec: kho TC-BLP-162 · Kết quả bước 7 dùng để phân xử C1/C2 và bug Studio #1459 · Evidence: ảnh 決済履歴 + 契約詳細 |
| TC-PAYBATCH001-02 | UI | PAY-BATCH-001 | Job bill định kỳ — thẻ | Abnormal | auto | Tất cả | Thu tiền định kỳ: khách đổi kỳ năm sang tháng qua màn お支払い期間の変更 trong lúc chờ kết quả thanh toán, số tiền ghi nhận vẫn là tiền năm | Hợp đồng スタンダード 年間一括払い, thanh toán thẻ Univapay, 次回決済日 là hôm nay, đơn giá cơ bản 10.780. Runner giữ lại kết quả thanh toán của job. Đăng nhập owner | 1. Chạy job thu tiền định kỳ, ghi lại 課金ID của giao dịch 116.424. 2. Khi kết quả chưa về, vào 契約詳細, bấm 「次回決済から月払いに変更する」 và hoàn tất (nhập thẻ nếu màn yêu cầu). 3. Xác nhận màn hiện dòng xám đổi sang 月払い. 4. Cho kết quả thanh toán thành công của 課金ID đó về. 5. Mở 決済履歴・領収書のダウンロード tìm dòng theo 課金ID. 6. Đọc 「ご利用料金」 ở 契約詳細 | Số đã thu 116.424; số theo kỳ tháng 10.780 | Dòng có 課金ID hiển thị 利用料 (税込) 116,424円, chỉ 1 dòng (không hiện 12 dòng phân bổ). 契約詳細: 「お支払い期間」 vẫn 年間一括払い kèm dòng xám, 「ご利用料金」 116,424円. Không nơi nào ghi 10,780円 cho giao dịch này |  | Lấp G1 · chiều ngược của ticket · Đánh giá spec: kho TC-BLP-155 · Evidence: ảnh 決済履歴 + 契約詳細 |
| TC-STATEDEP001-01 | UI | STATE-DEP-001 | Job bill định kỳ — thẻ | Boundary | auto | Tất cả | Đổi kỳ tháng sang năm trong lúc chờ kết quả thanh toán: hạn hợp đồng và nhãn kỳ của lần thu này phải theo kỳ tháng đã thu | Đã chạy xong TC-PAYBATCH001-01 trên cùng hợp đồng. Ghi lại 次回決済日 trước khi chạy job | 1. Mở 契約詳細, đọc 「次回決済日」 và 「お支払い期間」. 2. Mở modal 操作履歴 của hợp đồng, tìm bản ghi thanh toán của lần thu vừa rồi, đọc tiêu đề, số tiền, kỳ hạn. 3. Mở 決済履歴・領収書のダウンロード, đếm số dòng thuộc 課金ID của lần thu này. 4. Nếu tài khoản có người giới thiệu, mở 紹介報酬管理 đọc 「報酬額」 của lần thu này | 次回決済日 trước job ví dụ 2026/10/01; số đã thu 10.780 | 「次回決済日」 = ngày cũ + 1 tháng (vd 2026/11/01), KHÔNG phải + 1 năm. 操作履歴 có bản ghi 「スタンダードプラン　更新（毎月）」 số tiền 10,780円. 決済履歴 có đúng 1 dòng 10,780円 cho 課金ID này (không có dòng 898円). 「報酬額」 tính trên 10.780, không tính trên dòng con |  | Lấp G2 · Dev cố ý để ngoài phạm vi (rủi ro #3) — FAIL thì không chặn #37188 mà chuyển §8 #2 cho Leader quyết mở ticket · Đánh giá spec: kho TC-BLP-162 (đổi kỳ áp dụng từ lần thu sau) · Evidence: ảnh 契約詳細 + 操作履歴 + 決済履歴 |
| TC-STATEDEP001-02 | UI | STATE-DEP-001 | Job bill định kỳ — thẻ | Normal | auto | Tất cả | Sau lần thu tháng bị đổi kỳ giữa chừng, tới kỳ kế tiếp job phải thu theo kỳ năm đã đăng ký | Đã chạy xong TC-PAYBATCH001-01 và TC-STATEDEP001-01. Đưa ngày hệ thống tới đúng 「次回決済日」 mới | 1. Chạy job thu tiền định kỳ. 2. Cho kết quả thanh toán thành công về. 3. Mở 契約詳細 đọc 「お支払い期間」, 「ご利用料金」, 「次回決済日」. 4. Mở 決済履歴 tìm dòng của lần thu này | Đơn giá 10.780; giá năm 116.424 | Job tạo giao dịch 116.424. 「お支払い期間」 chuyển sang 年間一括払い, dòng xám biến mất, 「ご利用料金」 116,424円, 「次回決済日」 + 1 năm. 決済履歴 có 1 dòng 116,424円 |  | Lấp G2 · Đánh giá spec: kho TC-BLP-156 · Evidence: ảnh 契約詳細 + 決済履歴 |
| TC-PAYBATCH001-03 | API | PAY-BATCH-001 | Job bill định kỳ — chuyển khoản | Normal | auto | Tất cả | Thu tiền định kỳ bằng chuyển khoản: số tiền ghi nhận theo số Univapay báo đã thu, không tính lại theo hợp đồng | Hợp đồng スタンダード 年間一括払い, phương thức 銀行振込, job đã tạo giao dịch chuyển khoản 116.424 (màn hiện 入金待ち). Đăng nhập owner | 1. Ghi lại 課金ID của giao dịch chuyển khoản. 2. Gửi kết quả thanh toán thành công của 課金ID đó với số đã thu 116.424. 3. Mở 決済履歴 tìm dòng theo 課金ID. 4. Mở 契約詳細 đọc ステータス và 「ご利用料金」. 5. Lặp lại với một hợp đồng khác, lần này số đã thu trong kết quả là 116.430 (khác số hệ thống tính) | Số đã thu 116.424 và 116.430 | Lần 1: 決済履歴 hiện 116,424円, ステータス 正常. Lần 2: số ghi nhận là 116,430円 (số đã thu), không phải 116,424円. Không lỗi máy chủ ở cả 2 lần |  | Lấp G3 · Dev xác nhận trước: kết quả chuyển khoản có đi qua handleCallbackBillJob không — không đi qua thì lần 2 phải giữ cách tính cũ và đổi expected · RULE-08: số tiền thật đối chiếu ở NEW-37 trên product · Evidence: ảnh 決済履歴 |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Gia hạn hợp đồng | Boundary | manual | product | Gia hạn hợp đồng 1 năm: số tiền ghi nhận phải bằng số Univapay thực thu | Bot test trên production có hợp đồng đủ điều kiện 1年間の契約延長, thẻ thật. Có quyền xem dashboard Univapay. Đăng nhập owner | 1. Ở 契約詳細 thực hiện gia hạn hợp đồng 1 năm và hoàn tất thanh toán. 2. Mở 決済履歴, ghi 課金ID và 利用料 của dòng mới. 3. Mở modal 操作履歴, đọc bản ghi 「1年間の契約延長」. 4. Tra đúng 課金ID trên dashboard Univapay, đọc số đã thu. 5. Lập bảng 3 cột: 決済履歴 · 操作履歴 · Univapay | Hợp đồng スタンダード, giá production hiện hành | Cả 3 con số bằng nhau tuyệt đối |  | Lấp G6 · câu 5 — nhánh "giữ nguyên hành vi" phải có expected theo quy tắc, không chỉ "giống release" · Dev ghi nhận 3 handler còn tính lại tiền: FAIL thì mở ticket riêng (§8 #4) · manual vì môi trường production · Evidence: bảng đối chiếu + ảnh dashboard |
| TC-PAYCONFIRM001-01 | API | PAY-CONFIRM-001 | Job bill định kỳ — thẻ | Abnormal | auto | Tất cả | Thu tiền định kỳ thất bại: không được sinh hoa hồng giới thiệu và không gửi mail thưởng dù kết quả có số tiền yêu cầu thu | Hợp đồng スタンダード 月払い có người giới thiệu, đã có bản ghi hoa hồng trước đó. Giao dịch thu tiền 10.780 đã tạo. Ghi lại số dòng hoa hồng hiện có | 1. Gửi kết quả thanh toán thất bại với số đã thu 0 và số yêu cầu thu 10.780. 2. Đăng nhập người giới thiệu, mở 紹介報酬管理 lọc tháng hiện tại. 3. Kiểm hộp thư người giới thiệu. 4. Đếm lại số bản ghi hoa hồng của hợp đồng | Số đã thu 0; số yêu cầu thu 10.780 | Không sinh bản ghi hoa hồng mới, 紹介報酬管理 không có dòng mới cho lần thu này, không có mail thưởng |  | Lấp Q4 · hành vi đổi G7 (số yêu cầu thu nay được ghi vào bản ghi lỗi) · Đánh giá spec: Spec không ghi — chờ §8 #3 · Evidence: ảnh 紹介報酬管理 |
| TC-PAYCONFIRM001-02 | API | PAY-CONFIRM-001 | Job bill định kỳ — thẻ | Boundary | auto | Tất cả | Gói năm có người giới thiệu, số đã thu không chia hết cho 12: tổng 12 dòng phân bổ và tổng hoa hồng con phải bằng dòng cha | Hợp đồng スタンダード 年間一括払い có người giới thiệu, đã có bản ghi hoa hồng trước đó. Giao dịch thu tiền đã tạo | 1. Gửi kết quả thanh toán thành công với số đã thu 116.430. 2. Mở dữ liệu phân bổ tháng của lần thu (12 dòng con của lịch sử thanh toán) và cộng tay. 3. Cộng tay 12 dòng con của hoa hồng. 4. Mở 決済履歴 đọc dòng của 課金ID này | Số đã thu 116.430 (116.430 / 12 = 9.702,5) | Dòng cha lịch sử thanh toán 116.430, tổng 12 dòng con đúng 116.430. Dòng cha hoa hồng 116.430, tổng 12 dòng con hoa hồng đúng 116.430. 決済履歴 chỉ hiện 1 dòng 116,430円 |  | Lấp Q4 + R2 · regression · dẫn từ kho TC-BLP-294 + 03 D1 · Đánh giá spec: kho TC-BLP-294 · Evidence: bảng cộng tay + ảnh 決済履歴 |
| TC-OUTTRUTH001-01 | API | OUT-TRUTH-001 | Lịch sử thanh toán — theo tháng & lọc | Abnormal | auto | Tất cả | Thu tiền định kỳ thất bại: bản ghi lỗi mang số tiền không được hiện trên màn lịch sử thanh toán và không cộng vào tổng tháng | Hợp đồng スタンダード 月払い đang 正常. Ghi lại ご請求額 của tháng hiện tại ở 決済履歴. Giao dịch thu tiền 10.780 đã tạo | 1. Gửi kết quả thanh toán thất bại với số đã thu 0 và số yêu cầu thu 10.780. 2. Mở 決済履歴・領収書のダウンロード, đọc ご請求額 tháng hiện tại và mở chi tiết tháng. 3. Mở 契約詳細 đọc ステータス và 「ご利用料金」 | Số đã thu 0; số yêu cầu thu 10.780 | Chi tiết tháng không có dòng của 課金ID lỗi, ご請求額 tháng không đổi. 契約詳細 hiện ステータス 延滞中 |  | Lấp Q5 · hành vi đổi G7 · Đánh giá spec: kho TC-BLP-291 (lịch sử bill FAIL không hiện ở màn user) · Evidence: ảnh 決済履歴 trước/sau |
| TC-OUTEXPORT001-01 | API | OUT-EXPORT-001 | Tải lãnh thụ thư | Boundary | auto | Tất cả | Hợp đồng lại trả gộp 2 năm: lĩnh thu thư in đúng 1 dòng 232,848円 | Đã chạy xong NEW-13 (hợp đồng lại 年間払い + 2年分まとめて払い, thực thu 232.848). Đăng nhập owner | 1. Mở 決済履歴・領収書のダウンロード, mở chi tiết tháng chứa lần thanh toán. 2. Chọn 個別発行 cho dòng có 課金ID đó, tải lĩnh thu thư. 3. Làm lại bằng 一括ダウンロード | Thực thu 232.848 | Lĩnh thu thư in 1 dòng 232,848円, không tách 24 dòng 9,702円, không in 116,424円. Bản tải hàng loạt cho cùng số tiền |  | Lấp Q6 · Abnormal của quan điểm này gộp vào TC-OUTTRUTH001-01 (bản ghi lỗi không hiện thì không phát hành được) · Đánh giá spec: kho TC-BLP-208 · Evidence: file PDF |
| TC-DATAAUDIT001-01 | UI | DATA-AUDIT-001 | Lịch sử thao tác hợp đồng | Normal | auto | Tất cả | Hợp đồng lại đổi năm sang tháng: modal 操作履歴 ghi đúng số tiền tháng đã thu | Đã chạy xong NEW-11 (hợp đồng lại 年間一括払い sang 毎月払い, thực thu 10.780). Đăng nhập owner | 1. Mở 契約詳細 của hợp đồng, mở modal 操作履歴. 2. Tìm bản ghi hợp đồng lại mới nhất, đọc tiêu đề, số tiền, kỳ hạn, phương thức thanh toán | Thực thu 10.780 | Bản ghi tiêu đề 「スタンダードプラン　月払い再契約」, số tiền 10,780円, kỳ hạn 1 tháng, phương thức クレジットカード. Không hiển thị 116,424円 |  | Lấp Q7 · D5 bot_life_cycle.data.amount · Đánh giá spec: kho TC-BLP-225 · Nhóm UI vì phán quyết nằm ở màn (GROUP_MAP mặc định Data) · Evidence: ảnh modal 操作履歴 |
| TC-JOB001-01 | Job | JOB-001 | Job bill định kỳ — thẻ | Normal | manual | product | Lượt job thu tiền định kỳ đầu tiên sau deploy: job monitor bill tiền không báo lệch cho giao dịch mới | Bản fix đã deploy production. Có quyền xem kết quả job monitor bill tiền và dashboard Univapay | 1. Chờ lượt job thu tiền 06:30 đầu tiên sau deploy chạy xong. 2. Chạy job monitor bill tiền (khối Check bill tiền bot). 3. Chọn 3 giao dịch thu định kỳ mới (ưu tiên 1 hợp đồng năm, 1 hợp đồng tháng, 1 hợp đồng có người giới thiệu), đối chiếu 決済履歴 với dashboard Univapay | Giao dịch thật của lượt job | Job monitor không cảnh báo lệch cho giao dịch tạo sau deploy. 3 giao dịch được chọn có số trên 決済履歴 bằng số đã thu trên Univapay |  | Lấp R1 + Q1 + Q2 · regression · dẫn từ kho TC-BLP-307 · RULE-08 · manual vì môi trường production · Evidence: kết quả job monitor + bảng đối chiếu |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/detail-contract/db/db-mapping.md:445/466/498` vs `spec-features/admin/billing-plan/feature-spec.md:99/181/509/519` | Chốt 「ご利用料金」 ở màn 契約詳細 lấy từ đâu: số lần thu gần nhất (`amount_payment`) hay giá tính theo kỳ đang hiển thị. Quyết định này quyết luôn bug Studio #1459 thật hay giả | C1 `CONF-SPEC` ở §4 | Dev / PM |
| 2 | `kho-tcs/fa031` TC-BLP-130 vs TC-BLP-155/156/162 | Thống nhất expected "số tiền ở màn detail" khi kỳ đang hiển thị khác kỳ của lần thu gần nhất. Kèm quy tắc cho G2: giao dịch tạo **trước** khi đổi kỳ thì nhãn kỳ · hạn hợp đồng · chia 12 dòng theo kỳ cũ (kho: đổi kỳ áp dụng từ lần thu sau) hay theo kỳ mới. Theo kỳ cũ mà code đang theo kỳ mới → mở ticket tiếp (Dev đã để ngoài phạm vi) | C2 `CONF-KHO` ở §4 + G2 | Leader |
| 3 | `spec-features/admin/billing-plan/feature-spec.md` §8 (webhook `charge_finished`) | Bản ghi thanh toán **thất bại** mang số tiền nào (0 hay số yêu cầu thu) và callback thất bại có được ghi đè `amount_payment` không. Gộp vào kho MT-13 (callback muộn / ngược thứ tự — expected đang trống) | G7 | Leader / Dev |
| 4 | — (phạm vi ticket) | Quy tắc "số ghi nhận = số Univapay thực thu" có áp cho extend_contract · change_card · bill_again · bill_max_friend · new · upgrade_pro không. Dev ghi nhận 3 handler còn tính lại tiền nhưng chưa nêu tên → yêu cầu Dev liệt kê + mở ticket riêng | G6 | Leader / Dev |
| 5 | — (code có sẵn, phát hiện khi test) | NEW-7 actual: `calculateSaleEnterprise` gói おまとめ kỳ tháng **đúng 9 slot** trả về 0 (kẽ hở giữa nhánh < 9 và > 9, functions.php:9811-9834). Job dùng cùng công thức để tính tiền thu → Dev xác nhận hợp đồng 9 slot có bị thu 0 không | NEW-7 | Dev |
