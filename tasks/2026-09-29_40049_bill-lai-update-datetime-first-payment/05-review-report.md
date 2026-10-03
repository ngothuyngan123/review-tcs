# 05 — Review Report

> Draft cho Leader verify — chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) MCP LME TEST STUDIO — task #186 (round 1, branch `ai_fixbug_40049`) |
| Tổng số TC review | 25 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 7/16 mục có TC — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (4 file, +51/−30) | 5/11 điểm có TC — **CHƯA ĐỦ** |

**Kết luận**: 12/27 vùng ảnh hưởng đủ TC · 3 GAP · 2 RISK.

> Điểm mấu chốt: đoạn code Dev bỏ chỉ chạy khi **hợp đồng còn `status=1` (延滞中) và quá hạn HƠN 7 ngày**. Bộ TC hiện tại né hẳn trạng thái này — nhóm "giữ nguyên ngày" chỉ test **chưa quá 7 ngày** (NEW-9/10/11/12/21/22/23 — trước fix cũng đã giữ nguyên, nên pass cả trước lẫn sau fix), còn nhóm "quá 7 ngày" lại dùng **hợp đồng đã bị cưỡng chế hủy `status=3`** (NEW-4/5/6/24) — mà theo diff, `status=3` đi vào nhánh **ký lại → đặt ngày mới**. Kết quả: **không TC nào chứng minh được bug #40049 đã hết**.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` + `D1` + `F2` + `T1` — nút Bill lại trên hợp đồng 延滞中 (`status=1`) quá hạn >7 ngày, 3 phương thức; diff: bỏ ghi đè ở `billStripeContract` / `billTransferUnivapayContract` + handler `handleCallbackBillAgainCardSuccess` nhánh không cờ | dev-impact + diff code | không có (NEW-4/5/6/24 dùng `status=3`; NEW-22/23 chưa quá 7 ngày) | **GAP** — 0 TC tái hiện đúng điều kiện gây bug; thiếu cả biên 7 / 8 ngày quanh mốc code cũ | [BLOCKER] |
| G2 | `F1` — job `AutoPaymentJobUnivapay` phase 1–3 + `handleCallbackBillJob` bỏ ghi đè khi quá hạn >7 ngày | dev-impact + diff code | NEW-9, NEW-10, NEW-11, NEW-12, NEW-21 | **GAP** (nhánh bị sửa) — cả 5 TC đều "chưa quá 7 ngày" nên không đi qua đoạn code bị bỏ; 4/5 còn `skip` | [BLOCKER] |
| G3 | `T2` + câu 3 (hàm dùng chung) — handler callback Univapay nay **chỉ đặt ngày mới khi có cờ `isReContract`**, nhưng Dev chỉ gắn cờ ở `billCardUnivapayContract`. Các luồng khác cũng thu tiền thẻ Univapay: 再契約 (`reContractChangeCard`), đổi thẻ khi quá hạn (`changeCard` — spec §2.11 "quá hạn → charge luôn"), đăng ký thẻ phụ khi quá hạn | diff code | không có | **GAP** — 再契約 bằng thẻ Univapay có thể **mất** việc đặt lại ngày (trước đây "vô tình" đúng nhờ đoạn ghi đè vừa bị bỏ — chính Dev mô tả ở mục 2); đổi thẻ / thẻ phụ quá hạn >7 ngày chưa có TC | [BLOCKER] |
| G4 | `F4` + `D2` + `T3` — hệ quả Dev nêu: sau khi hồi phục hợp đồng quá hạn >7 ngày, kỳ kế tiếp bám lại ngày gốc → kỳ ngắn hơn 1 tháng nhưng thu trọn tháng | dev-impact + diff code | NEW-18 | **RISK** — expected "có thể ngắn hơn một tháng", không có ngày cụ thể; `needs-human-review`; chưa chạy | [MAJOR] |
| G5 | Rủi ro hồi quy Studio: nhánh ký lại Stripe (`status=3`) nay chạy thật sau khi sửa typo — áp cho **mọi** `status=3`, kể cả hợp đồng bị cưỡng chế hủy | diff code | NEW-1 vs NEW-4 / NEW-5 / NEW-6 / NEW-24 | **RISK** — 2 nhóm TC có expected ngược nhau cho cùng nhánh code (xem C1/C2 §4) → mất chuẩn Đạt/Không đạt | [MAJOR] |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 20 quan điểm có Trigger khớp task · 8 chưa cover đủ (Q1–Q8) · 11 quan điểm Cao thiếu loại case không ghi lý do (Q9) · ENV-003 / RULE-08 ghi ở §5.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `PAY-STATE-001` | Cao | **GAP** — 0 TC đối chiếu 3 nơi (màn chi tiết hợp đồng · lịch sử thanh toán · dashboard UnivaPay/Stripe) sau bill lại | [BLOCKER] |
| Q2 | `JOB-001` | Cao | **GAP** — TC job (NEW-8/9/10/11/21) mang mã `JOB-002` không có trong checklist → không tính; đề nghị đổi mã trên Studio (`testcase_update`) + TC mới ở G2 | [BLOCKER] |
| Q3 | `PAY-AMOUNT-001` | Cao | **GAP** — kỳ ngắn hơn 1 tháng nhưng thu trọn tháng (hệ quả G4) chưa có TC kiểm số tiền + ngày | [BLOCKER] |
| Q4 | `CONC-001` | Cao | **GAP** — bấm Bill lại 2 lần liên tiếp chưa có TC (NEW-15 chỉ là webhook trùng) | [BLOCKER] |
| Q5 | `STATE-001` | Cao | **GAP** — Univapay card: Dev nói trạng thái bị đặt lại 正常 **ngay sau khi tạo giao dịch**, trước khi callback về → ký lại mà callback thất bại có để hợp đồng nửa vời không? 0 TC | [BLOCKER] |
| Q6 | `DATA-DB-001` | Cao | **RISK** — không TC nào kiểm hợp đồng đối chứng (cùng tài khoản + tài khoản khác) không bị đổi お支払い開始日 | [BLOCKER] |
| Q7 | `OUT-TRUTH-001` | Cao | **RISK** — Dev kê 2 view hiển thị お支払い開始日 (`detail.blade.php` + `detail-bill-fail.blade.php`); NEW-16 chỉ kiểm màn thường, chưa kiểm màn hợp đồng 延滞中 | [MAJOR] |
| Q8 | `INTG-HOOK-002` | Trung bình | **RISK** — chỉ NEW-13 mang mã lạ `API-CONTRACT-001` → đề nghị đổi mã, không cần TC mới | [MAJOR] |
| Q9 | RULE-01 — `FUNC-001` · `REG-SHARED-001` · `OUT-TRUTH-001` · `DEPLOY-LIVE-001` · `FUNC-004` · `REG-RUN-001` · `DATA-DB-001` · `DATA-AUDIT-001` · `REG-SPEC-001` · `DATA-BACKUP-001` · `DATA-001` (+ `INTG-HOOK-001` thiếu Boundary) | Cao | **RISK** — mỗi mã chỉ 1 loại case, không ghi lý do. Phần quan trọng nhất (biên 7 ngày) đã lấp bằng TC-PAYSTATE001-05 / TC-JOB001-04; mã còn lại → member ghi lý do ở `Ghi chú` trên Studio | [MAJOR] |

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-21 (+ NEW-9 / NEW-10 / NEW-11) | NEW-12 → **gộp** | DUP-SUBSET | `REG-RUN-001` vs `JOB-002` khác mã nhưng cùng ý định · Normal · job bill định kỳ hợp đồng A đúng kỳ + B lỗi chưa quá 7 ngày · expected giữ T0 + Payment History không trùng. A = NEW-9/10/11, B = NEW-21 | [MINOR] |
| DUP-2 | NEW-4 / NEW-5 / NEW-6 | NEW-24 → **gộp** | DUP-SUBSET | cùng "cưỡng chế hủy → Bill lại → giữ T0"; NEW-24 chỉ thêm bước dựng trạng thái và không nói phương thức thanh toán | [MINOR] |

- **Gate đã chạy**: bỏ NEW-12 / NEW-24 không làm mất cover — NEW-12 thực chất không test "job đang chạy dở khi release" (nội dung đó do NEW-14 cover). Đổi sang **gộp**: giữ phần kiểm "Payment History không thiếu, không trùng" của NEW-12 vào NEW-21; NEW-24 giữ làm E2E cho **1 phương thức cụ thể** sau khi chốt C1/C2.
- DUP-2 phụ thuộc kết quả C1/C2 — nếu PM chốt "cưỡng chế hủy rồi thanh toán lại = hợp đồng lại" thì cả nhóm NEW-4/5/6/24 phải sửa expected.

---

## 4. Mâu thuẫn trong TCs

**Đã rà**: 25 TC × `spec-features/admin/detail-contract/feature-spec.md` (§2.11, §5.1, §7.3–7.4) + `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (nhóm 20, 21, 29, 31, 32 + MT-04) — **3 mâu thuẫn**.

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-TC` | NEW-1 / NEW-2 / NEW-3 vs NEW-4 / NEW-5 / NEW-6 (+ NEW-24, NEW-18) | Hợp đồng `status=3`, thanh toán lại thành công, cùng phương thức | NEW-1/2/3: お支払い開始日 = ngày thực hiện (D) | NEW-4/5/6: お支払い開始日 VẪN = T0 — TC phân biệt bằng **lý do hủy** (user hủy vs cưỡng chế hủy), nhưng theo Studio `dev_impact` code chỉ xét `status == 3` (Stripe sau khi sửa typo; `billCardUnivapayContract` đọc `status == 3` → gắn `isReContract`) | 1 trong 2 nhóm chắc chắn Không đạt: hoặc NEW-4/5/6 sai (code đúng ý PM) — hoặc code thiếu điều kiện `cancel_by` (TC đúng ý PM). Đụng thẳng root cause → đề nghị Leader xử như BLOCKER | [MAJOR] | PM + Dev |
| C2 | `CONF-KHO` | NEW-4 / NEW-5 / NEW-6 / NEW-24 | Thanh toán lại hợp đồng đã cưỡng chế hủy | Giữ T0 | TC-BLP-201: màn account 強制解約 chỉ có nút 「再契約へ進む」 · TC-BLP-215 "Hợp đồng lại → datetime_first_payment cập nhật thành ngày hiện tại" | TC sai (sau cưỡng chế hủy chỉ có đường 再契約 → đặt ngày mới là đúng) / kho cần update nếu PM chốt khác ở C1 | [MAJOR] | Leader |
| C3 | `CONF-KHO` | NEW-4 / NEW-5 / NEW-6 / NEW-12 (ghi chú "không dùng state status=1 + quá hạn >7 ngày") | Hợp đồng `status=1` còn tồn tại sau khi quá hạn >7 ngày không? | Không — quá hạn >7 ngày thì đã bị auto-cancel | TC-BLP-293: retry theo `status_payment_fail` 1 → +2 → +5 → +6 ngày, **chỉ lần 5** mới cưỡng chế hủy (≈ 13 ngày vẫn 延滞中). Kho MT-04 đang chờ quyết định; spec §7.3 Phase 4 lại ghi "REGISTERED + expired-7d" | TC đúng (hủy ở mốc 7 ngày) → đoạn code Dev bỏ gần như không chạy tới, phải hỏi hợp đồng 74140 đã đi đường nào / kho + spec cần thống nhất | [MAJOR] | Dev + Leader |

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | [BLOCKER] | Toàn bộ task #186 | Chỉ 3/25 TC `pass` (12%) — 6 `skip` (NEW-9/10/11/12/17/19), 15 chưa chạy; 16 TC `manual` (gồm toàn bộ TC lõi NEW-1…6, NEW-8, NEW-24) **chưa chạy lần nào** | Chạy lại sau khi sửa theo §1/§4; không kết luận "fix OK" từ 3 TC pass hiện tại (không TC nào trong đó chạm điều kiện gây bug) |
| I2 | [MAJOR] | Toàn bộ | RULE-08 / ENV-003 — bill tiền thật nhưng 4 TC đã chạy đều ở `local`; Studio: dev / staging / prd = 0 run | Mỗi đường thu tiền (thẻ Univapay qua callback, Stripe, chuyển khoản, job) cần ≥ 1 mẫu verify production (§7 đã đánh `product` cho 2 TC lõi) |
| I3 | [MAJOR] | NEW-11, G2 | `Input thiếu`: Dev bỏ ghi đè ở `chargeUnivapayTransferBots` (Phase 3), nhưng spec §7.3 Phase 3 chỉ lấy hợp đồng `status_payment=1` và tạo charge **trước hạn 30 ngày** → trạng thái nào đi vào nhánh "quá hạn >7 ngày" của Phase 3? | Hỏi Dev; chưa trả lời thì chưa đề xuất TC job chuyển khoản |
| I4 | [MAJOR] | Luồng callback Univapay (G3) | REG-SHARED-001 — Dev chưa kê những luồng nào tạo charge đi vào `handleCallbackBillAgainCardSuccess` và luồng nào gắn cờ `isReContract` (`reContractChangeCard`, `changeCard` khi quá hạn, đăng ký thẻ phụ khi quá hạn chỉ ghi "đã check") | Yêu cầu Dev liệt kê; kết quả quyết định expected của G3 |
| I5 | [MAJOR] | NEW-1…6, NEW-9…12, NEW-21…24 | Expected không đo được: "expired_date_contract được cập nhật theo rule hiện tại / theo flow phục hồi" — không có ngày cụ thể. Dev còn nêu lệch 1 ngày giữa `BillingService` (Univapay) và `calculateNextExpired*` (Stripe / chuyển khoản) | Ghi ngày hết hạn mong đợi cụ thể theo từng phương thức (vd T0 ngày 10 → …) |
| I6 | [MAJOR] | NEW-1 / NEW-2 / NEW-3 / NEW-4 / NEW-5 / NEW-6 / NEW-24 | Bước viết bằng tên endpoint / mã màn ("change-status-contract, không phải contract_revert", "Mở SCR-DC-02", "Bill lại theo flow phục hồi thanh toán") — tester không biết bấm nút nào. Riêng hợp đồng 強制解約, kho TC-BLP-201 cho thấy màn chỉ có nút 「再契約へ進む」 | Ghi tên nút + URL màn (/basic/detail-contract/{id}); sửa trên Studio rồi fetch lại |
| I7 | [MAJOR] | NEW-24, NEW-18, NEW-22, NEW-23 | Không dựng lại được: "Đưa dữ liệu/thời gian qua mốc quá hạn >7 ngày và chạy đúng xử lý auto-cancel", "Theo dõi/tính mốc billing", "Thực hiện/đợi flow bill lại phát sinh sau khi đổi Main card" (spec §2.11: đổi thẻ khi quá hạn → thu tiền ngay) | Nêu rõ cách dựng ngày quá hạn + thao tác nào sinh ra lần thu tiền |
| I8 | [MAJOR] | NEW-8 | Không atomic: "thẻ Stripe hoặc Univapay" — 2 đường ghi khác nhau (Stripe ghi ngay, Univapay ghi qua callback) | Tách 2 TC |
| I9 | [MAJOR] | NEW-17, NEW-25 | [AP-3] Tiền điều kiện không có hợp đồng quá hạn >7 ngày → dữ liệu dùng để test chưa từng bị ghi đè, TC pass cả trước fix | Dùng hợp đồng đã chạy TC-PAYSTATE001-01 làm dữ liệu vào |
| I10 | [MINOR] | NEW-25 | Có export CSV nhưng mã quan điểm là `DATA-001`, thiếu `OUT-EXPORT-001` | Thêm mã trên Studio |
| I11 | [NIT] | NEW-19 | Kiểm log `bot_life_cycles` — diff 4 file không chạm ghi log; chưa rõ ý định | Hỏi member: giữ làm regression hay chuyển sang bộ kho (TC-BLP-203) |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 25 TC — không có TC nào ngoài phạm vi task. (NEW-19 chưa chắc ý định → hỏi ở §5 I11, không flag.)

---

## 7. TCs đề xuất bổ sung (14)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (nhóm 17, 20, 21, 29, 31, 32; MT-04) |
| Vùng regression phát hiện từ kho | Nhóm 21 Hợp đồng lại (TC-BLP-209…215) · nhóm 29 Job bill thẻ (TC-BLP-291…293, 298) · nhóm 32 Ngày bill (TC-BLP-315, 319, 321) |
| Conflict expected vs kho | NEW-4/5/6/24 vs TC-BLP-215 / TC-BLP-201 → C2 · NEW-4/5/6/12 vs TC-BLP-293 → C3 — đã đưa §4 + §8 |
| GAP dùng lại TC kho (không viết mới) | **G3 (phần 再契約)** → dùng lại **TC-BLP-215** "Hợp đồng lại → datetime_first_payment cập nhật thành ngày hiện tại" — chạy trên branch fix, chọn **thẻ Univapay đã lưu** (đường callback đổi logic), thêm lượt thẻ mới ở step 2 |
| G5 | **Không đẻ TC** — expected phụ thuộc C1/C2 (không tự chọn bên). PM chốt xong → sửa expected NEW-4/5/6/24 trên Studio |
| Căn cứ TC regression `R<x>` | Không có TC R — rủi ro hồi quy Studio (nhánh ký lại Stripe) đã có NEW-1; vùng kho đã quy về G1–G4 |
| Xác nhận chống trùng | Đã đối chiếu 25 TC ở BƯỚC 0 + kho fa031 — không TC đề xuất nào trùng (TC hiện có đều "chưa quá 7 ngày" hoặc `status=3`) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PAYSTATE001-01 | UI | PAY-STATE-001 | Detail hợp đồng — standard/pro | Normal | manual | product | Bill lại thành công bằng thẻ Univapay cho hợp đồng 延滞中 quá hạn 9 ngày giữ nguyên お支払い開始日 | Bot standard trả bằng thẻ Univapay, お支払い開始日 2026年05月10日. Hạn thanh toán đã qua 9 ngày, hợp đồng vẫn 延滞中 (Dev chỉnh hạn ngay trước khi test, trước giờ job bill 06:30 để chưa bị cưỡng chế hủy). Thẻ chính đã đổi sang thẻ hợp lệ. Cùng tài khoản có 1 hợp đồng khác; 1 tài khoản khác cũng có hợp đồng 延滞中 | 1. Mở màn chi tiết hợp đồng (/basic/detail-contract/{id}) đang 延滞中, ghi lại お支払い開始日<br>2. Bấm nút thanh toán lại (Bill lại), chờ báo thành công<br>3. Tải lại màn chi tiết hợp đồng<br>4. Mở lịch sử thanh toán của hợp đồng<br>5. Mở dashboard UnivaPay xem giao dịch vừa tạo<br>6. Mở chi tiết 2 hợp đồng đối chứng | お支払い開始日 2026年05月10日; hạn thanh toán = hôm nay trừ 9 ngày; thẻ Univapay hợp lệ | Bước 1: màn 延滞中 hiện お支払い開始日 2026年05月10日<br>Bước 3: お支払い開始日 VẪN là 2026年05月10日, KHÔNG đổi sang hôm nay; trạng thái 正常<br>Bước 4: đúng 1 bản ghi thanh toán thành công mới, đúng số tiền plan<br>Bước 5: đúng 1 giao dịch Successful cùng số tiền<br>Bước 6: お支払い開始日 của 2 hợp đồng đối chứng không đổi | | Lấp G1 · Q1 · Q6 · Q7 · đường ghi thật = `handleCallbackBillAgainCardSuccess` nhánh không cờ `isReContract` · RULE-08 · manual vì môi trường production · Đánh giá spec: Spec không ghi (theo Expect ticket) · Evidence: screenshot màn trước/sau + lịch sử thanh toán + dashboard UnivaPay |
| TC-PAYSTATE001-02 | UI | PAY-STATE-001 | Detail hợp đồng — standard/pro | Normal | auto | Tất cả | Bill lại thành công bằng thẻ Stripe cho hợp đồng 延滞中 quá hạn 9 ngày giữ nguyên お支払い開始日 | Bot standard còn trả bằng thẻ Stripe (legacy), お支払い開始日 2026年05月10日. Hạn thanh toán đã qua 9 ngày, hợp đồng vẫn 延滞中. Thẻ Stripe đã đổi sang thẻ test hợp lệ | 1. Mở màn chi tiết hợp đồng đang 延滞中<br>2. Bấm nút thanh toán lại (Bill lại), chờ báo thành công<br>3. Tải lại màn chi tiết hợp đồng<br>4. Mở lịch sử thanh toán và dashboard Stripe | お支払い開始日 2026年05月10日; hạn thanh toán = hôm nay trừ 9 ngày; thẻ Stripe test hợp lệ | お支払い開始日 VẪN là 2026年05月10日; trạng thái 正常; đúng 1 bản ghi thanh toán mới và đúng 1 giao dịch Succeeded trên Stripe | | Lấp G1 · Q1 · diff: bỏ ghi đè trong `billStripeContract` (khác nhánh `status=3` đã sửa typo) · Đánh giá spec: Spec không ghi · Evidence: screenshot màn + Stripe |
| TC-PAYSTATE001-03 | UI | PAY-STATE-001 | Chuyển khoản — tạo & thông tin tài khoản | Normal | auto | Tất cả | Bill lại hợp đồng chuyển khoản quá hạn 9 ngày, chuyển khoản thành công vẫn giữ お支払い開始日 | Bot standard trả bằng chuyển khoản Univapay, お支払い開始日 2026年05月10日, hạn thanh toán đã qua 9 ngày, hợp đồng 延滞中, không có yêu cầu chuyển khoản đang chờ | 1. Mở màn chi tiết hợp đồng đang 延滞中<br>2. Bấm nút thanh toán lại (Bill lại), ghi lại số tài khoản chuyển khoản được tạo<br>3. Mô phỏng Univapay báo đã nhận tiền cho yêu cầu vừa tạo<br>4. Tải lại màn chi tiết hợp đồng và lịch sử thanh toán | お支払い開始日 2026年05月10日; hạn thanh toán = hôm nay trừ 9 ngày; số tiền chuyển đúng số tiền yêu cầu | Sau bước 2: trạng thái 入金待ち, お支払い開始日 vẫn 2026年05月10日<br>Sau bước 4: trạng thái 正常, お支払い開始日 VẪN là 2026年05月10日, lịch sử thanh toán có 1 bản ghi mới với ngày = ngày nhận tiền | | Lấp G1 · Q1 · diff: bỏ ghi đè trong `billTransferUnivapayContract` · Đánh giá spec: Spec không ghi · Evidence: screenshot 3 thời điểm |
| TC-PAYSTATE001-04 | UI | PAY-STATE-001 | Detail hợp đồng — standard/pro | Abnormal | auto | Tất cả | Bill lại thất bại bằng thẻ Univapay bị từ chối trên hợp đồng 延滞中 quá hạn 9 ngày không đổi お支払い開始日 | Như TC-PAYSTATE001-01 nhưng thẻ chính là thẻ test luôn bị từ chối | 1. Mở màn chi tiết hợp đồng đang 延滞中<br>2. Bấm nút thanh toán lại (Bill lại), chờ kết quả<br>3. Tải lại màn chi tiết hợp đồng và lịch sử thanh toán | Thẻ Univapay test bị từ chối; お支払い開始日 2026年05月10日 | Hiện thông báo thanh toán lỗi; trạng thái vẫn 延滞中; お支払い開始日 vẫn 2026年05月10日; hạn thanh toán không đổi; không có bản ghi thanh toán thành công mới | | Lấp G1 (Abnormal, RULE-01) · Đánh giá spec: Spec không ghi · Evidence: screenshot thông báo lỗi + màn chi tiết |
| TC-PAYSTATE001-05 | UI | PAY-STATE-001 | Detail hợp đồng — standard/pro | Boundary | auto | Tất cả | Bill lại thành công ở mốc quá hạn đúng 7 ngày và 8 ngày đều giữ nguyên お支払い開始日 | 2 hợp đồng thẻ Univapay đang 延滞中, cùng お支払い開始日 2026年05月10日: hợp đồng A quá hạn đúng 7 ngày, hợp đồng B quá hạn 8 ngày. Thẻ hợp lệ | 1. Bấm nút thanh toán lại (Bill lại) cho hợp đồng A, chờ thành công<br>2. Bấm nút thanh toán lại (Bill lại) cho hợp đồng B, chờ thành công<br>3. Mở chi tiết cả 2 hợp đồng | A: hôm nay trừ 7 ngày; B: hôm nay trừ 8 ngày | Cả A và B: お支払い開始日 VẪN là 2026年05月10日, trạng thái 正常, mỗi hợp đồng đúng 1 bản ghi thanh toán mới | | Lấp G1 · Q9 (biên mốc "quá hạn hơn 7 ngày" của code cũ) · Đánh giá spec: Spec không ghi · Evidence: screenshot 2 hợp đồng |
| TC-JOB001-01 | Job | JOB-001 | Job bill định kỳ — thẻ | Normal | manual | product | Job bill định kỳ thu lại thành công thẻ Univapay cho hợp đồng quá hạn 9 ngày giữ nguyên お支払い開始日 | Bot standard thẻ Univapay, お支払い開始日 2026年05月10日, các lần job trước đã lỗi, hợp đồng vẫn 延滞中 và đã quá hạn 9 ngày. Thẻ chính đã đổi sang thẻ hợp lệ trước giờ job | 1. Chờ job bill định kỳ lúc 06:30 chạy (hoặc Dev kích hoạt job)<br>2. Chờ Univapay báo kết quả thanh toán về<br>3. Mở chi tiết hợp đồng và lịch sử thanh toán<br>4. Mở dashboard UnivaPay | お支払い開始日 2026年05月10日; hạn thanh toán = hôm nay trừ 9 ngày | Trạng thái 正常; お支払い開始日 VẪN là 2026年05月10日; đúng 1 bản ghi thanh toán mới; đúng 1 giao dịch Successful trên UnivaPay | | Lấp G2 · Q2 · diff: Phase 2 + `handleCallbackBillJob` · phụ thuộc C3 (trạng thái này có tồn tại không) · RULE-08 · manual vì môi trường production · Evidence: log job + màn + dashboard |
| TC-JOB001-02 | Job | JOB-001 | Job bill định kỳ — thẻ | Normal | auto | Tất cả | Job bill định kỳ thu lại thành công thẻ Stripe cho hợp đồng quá hạn 9 ngày giữ nguyên お支払い開始日 | Bot standard thẻ Stripe (legacy), お支払い開始日 2026年05月10日, hợp đồng 延滞中 quá hạn 9 ngày, thẻ đã đổi sang thẻ test hợp lệ | 1. Kích hoạt job bill định kỳ<br>2. Mở chi tiết hợp đồng và lịch sử thanh toán | お支払い開始日 2026年05月10日; hạn thanh toán = hôm nay trừ 9 ngày | Trạng thái 正常; お支払い開始日 VẪN là 2026年05月10日; đúng 1 bản ghi thanh toán mới | | Lấp G2 · Q2 · diff: Phase 1 Stripe · Evidence: log job + màn |
| TC-JOB001-03 | Job | JOB-001 | Job hủy hợp đồng & retry | Abnormal | auto | Tất cả | Job bill định kỳ tiếp tục lỗi trên hợp đồng quá hạn 9 ngày không đổi お支払い開始日 | Như TC-JOB001-01 nhưng thẻ chính và thẻ phụ đều là thẻ test bị từ chối | 1. Kích hoạt job bill định kỳ<br>2. Mở chi tiết hợp đồng và lịch sử thanh toán | Thẻ bị từ chối; お支払い開始日 2026年05月10日 | お支払い開始日 vẫn 2026年05月10日 (dù sau job hợp đồng là 延滞中 hay 強制解約); không có bản ghi thanh toán thành công mới | | Lấp G2 (Abnormal, RULE-01) · trạng thái sau job phụ thuộc C3 nên expected chỉ phán trên お支払い開始日 · Evidence: log job + màn |
| TC-JOB001-04 | Job | JOB-001 | Job bill định kỳ — thẻ | Boundary | auto | Tất cả | Job bill định kỳ thu thành công ở mốc quá hạn đúng 7 ngày và 8 ngày đều giữ nguyên お支払い開始日 | 2 hợp đồng thẻ Univapay 延滞中, cùng お支払い開始日 2026年05月10日: A quá hạn đúng 7 ngày, B quá hạn 8 ngày. Thẻ hợp lệ | 1. Kích hoạt job bill định kỳ<br>2. Mở chi tiết cả 2 hợp đồng | A: hôm nay trừ 7 ngày; B: hôm nay trừ 8 ngày | Cả A và B: trạng thái 正常, お支払い開始日 VẪN là 2026年05月10日, mỗi hợp đồng đúng 1 bản ghi thanh toán mới | | Lấp G2 · Q9 · Evidence: log job + màn 2 hợp đồng |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Thẻ chính & thẻ phụ | Normal | auto | Tất cả | Đổi thẻ chính trên hợp đồng 延滞中 quá hạn 9 ngày, hệ thống thu tiền ngay và giữ nguyên お支払い開始日 | Bot standard thẻ Univapay, お支払い開始日 2026年05月10日, hợp đồng 延滞中 quá hạn 9 ngày | 1. Ở màn chi tiết hợp đồng, vào đổi thẻ chính, nhập thẻ test hợp lệ mới, lưu<br>2. Chờ báo thu tiền thành công<br>3. Mở chi tiết hợp đồng và lịch sử thanh toán | Thẻ Univapay test hợp lệ mới; お支払い開始日 2026年05月10日 | Thẻ chính hiển thị 4 số cuối thẻ mới; trạng thái 正常; お支払い開始日 VẪN là 2026年05月10日; đúng 1 bản ghi thanh toán mới | | Lấp G3 · câu 3 hàm dùng chung (callback Univapay) · spec §2.11 "đổi thẻ khi quá hạn → charge luôn" · chờ Dev trả lời §5 I4 · Evidence: screenshot màn + lịch sử |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | Thẻ chính & thẻ phụ | Normal | auto | Tất cả | Đăng ký thẻ phụ trên hợp đồng 延滞中 quá hạn 9 ngày, hệ thống thu tiền ngay và giữ nguyên お支払い開始日 | Bot standard thẻ Univapay, お支払い開始日 2026年05月10日, hợp đồng 延滞中 quá hạn 9 ngày, chưa có thẻ phụ, thẻ chính bị từ chối | 1. Ở màn chi tiết hợp đồng, đăng ký thẻ phụ bằng thẻ test hợp lệ<br>2. Chờ báo thu tiền thành công<br>3. Mở chi tiết hợp đồng và lịch sử thanh toán | Thẻ phụ Univapay test hợp lệ; お支払い開始日 2026年05月10日 | Thẻ phụ hiển thị 4 số cuối; trạng thái 正常; お支払い開始日 VẪN là 2026年05月10日; đúng 1 bản ghi thanh toán mới | | Lấp G3 · spec §2.11 "Sub card — nếu quá hạn → charge luôn khi đăng ký" · Evidence: screenshot màn + lịch sử |
| TC-PAYAMOUNT001-01 | Job | PAY-AMOUNT-001 | Ngày bill & expired_date | Boundary | auto | Tất cả | Kỳ thu tiền kế tiếp sau khi bill lại hợp đồng quá hạn 9 ngày quay về ngày 10 của お支払い開始日 | Hợp đồng tháng thẻ Univapay, お支払い開始日 2026年05月10日, đã bill lại thành công khi quá hạn 9 ngày (theo TC-PAYSTATE001-01) | 1. Ghi lại hạn thanh toán mới ở chi tiết hợp đồng ngay sau khi bill lại<br>2. Dev đưa ngày hệ thống tới hạn thanh toán đó và kích hoạt job bill định kỳ<br>3. Mở chi tiết hợp đồng và lịch sử thanh toán | お支払い開始日 2026年05月10日; ngày bill lại = hạn cũ cộng 9 ngày | Bước 3: hạn thanh toán mới rơi vào NGÀY 10 của tháng kế tiếp (kỳ này ngắn hơn 1 tháng); số tiền thu vẫn đúng giá 1 tháng; lịch sử thanh toán có đúng 1 bản ghi mới; お支払い開始日 vẫn 2026年05月10日 | | Lấp G4 · Q3 · expected theo mô tả Dev (dev_impact "kỳ kế tiếp bám ngày gốc nên ngắn hơn 1 tháng") — **PM chưa chốt** (§8 #4), chốt khác thì sửa expected · thay cho NEW-18 · Evidence: màn + lịch sử 2 kỳ |
| TC-CONC001-01 | UI | CONC-001 | Detail hợp đồng — standard/pro | Abnormal | auto | Tất cả | Bấm nút Bill lại 2 lần liên tiếp trên hợp đồng 延滞中 chỉ thu tiền 1 lần | Bot standard thẻ Univapay, お支払い開始日 2026年05月10日, hợp đồng 延滞中 quá hạn 9 ngày, thẻ hợp lệ | 1. Ở màn chi tiết hợp đồng, bấm nút thanh toán lại (Bill lại) 2 lần thật nhanh<br>2. Chờ xử lý xong, tải lại màn<br>3. Mở lịch sử thanh toán và dashboard UnivaPay | Thẻ hợp lệ; 2 lần bấm cách nhau dưới 1 giây | Chỉ 1 giao dịch trên UnivaPay và 1 bản ghi thanh toán mới; お支払い開始日 VẪN là 2026年05月10日; trạng thái 正常 | | Lấp Q4 · thiếu Normal/Boundary vì nhánh thường đã ở TC-PAYSTATE001-01, biên không áp dụng · Evidence: dashboard + lịch sử (đếm số bản ghi) |
| TC-STATE001-01 | UI | STATE-001 | Hủy hợp đồng & chờ hủy | Abnormal | auto | Tất cả | Ký lại hợp đồng đã hủy bằng thẻ Univapay bị từ chối không để hợp đồng ở trạng thái nửa vời | Bot standard thẻ Univapay đã bị hủy khi đang 延滞中 (trạng thái 解約済), お支払い開始日 2026年05月10日, thẻ chính là thẻ test bị từ chối | 1. Ở màn chi tiết hợp đồng, bấm nút hủy yêu cầu hủy hợp đồng để ký lại<br>2. Chờ Univapay báo kết quả thanh toán thất bại<br>3. Tải lại màn danh sách 契約情報 và màn chi tiết hợp đồng | Thẻ Univapay test bị từ chối; お支払い開始日 2026年05月10日 | Báo thanh toán lỗi; hợp đồng vẫn 解約済 (KHÔNG hiện 正常); お支払い開始日 vẫn 2026年05月10日; không có bản ghi thanh toán thành công | | Lấp Q5 · Dev mục 2: trạng thái bị đặt lại "đang hợp đồng" ngay sau khi tạo giao dịch, trước callback · nhãn JP của nút cần Dev xác nhận · Evidence: screenshot 2 màn |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `detail-contract/feature-spec.md` §5.1 + §2.11 | Hợp đồng bị **cưỡng chế hủy** (`cancel_by=0`) rồi thanh toán lại / 再契約: お支払い開始日 **đặt lại = hôm nay** hay **giữ nguyên**? Code hiện chỉ xét `status=3` | C1 CONF-TC | PM + Dev |
| 2 | kho `fa031` nhóm 21 (TC-BLP-215) | Theo quyết định #1: giữ TC-BLP-215 cho mọi `status=3`, hay tách user hủy / cưỡng chế hủy | C2 CONF-KHO | Leader |
| 3 | spec §7.3 Phase 4 + §7.4 · kho MT-04 / TC-BLP-293 | Hợp đồng `status=1` có còn tồn tại khi quá hạn >7 ngày không (auto-cancel ở mốc 7 ngày hay ở lần lỗi thứ 5)? Nếu không → đoạn code Dev bỏ không chạy tới, cần biết hợp đồng 74140 đã đi đường nào | C3 CONF-KHO | Dev + Leader |
| 4 | spec §5 Business Rules (chưa có rule nào cho `datetime_first_payment`, chỉ có mapping ở `db-mapping.md:465`) | Thêm BR: お支払い開始日 chỉ đặt khi mua mới / hợp đồng lại; và quy tắc kỳ thu tiền kế tiếp sau khi hồi phục hợp đồng quá hạn (kỳ ngắn hơn 1 tháng, thu trọn tháng — Dev đề xuất tách cột neo riêng) | BƯỚC 1 — spec thiếu BR · G4 | PM |
