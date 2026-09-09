# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#36835 — [Bill tiền tool] Status 入金待ち nhưng nút Hủy chuyển khoản (振込キャンセル) không hiển thị` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<member điền — file 04 chưa có tên>` |
| Ngày review | `2026-06-03` |
| Version TCs | `v1 (fetch từ Sheet, read-only)` |
| Vòng review | `Round 1` |

> **Spec reference**: Không có `02-spec-reference.md` riêng cho task → dùng `templates/LME-SYSTEM-SPEC.md` tổng (feature Bill tiền / Quản lý hợp đồng). Note: spec tổng không mô tả chi tiết logic enable/disable button theo trạng thái hợp đồng — cần Dev/PM confirm business rule (xem §6).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER + nhiều MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Có **sai lệch nghiêm trọng** giữa symptom KH report (nút 振込キャンセル *không hiển thị*) và cách Dev tái hiện/fix (2 button *change* bị disable). Bộ TCs verify theo interpretation của Dev (enable button change) nhưng **không có TC nào verify đúng điều KH yêu cầu** → nguy cơ "fix nhưng KH vẫn thấy bug". Cộng thêm: mục 3 dev-impact trống, data-impact khai "Không có" trong khi fix có update data, thiếu chiều tháng→năm + negative test, và cả 01/03 auto-fill chưa được tester verify.

---

## 2. Tóm tắt cho member

Bộ TCs (fetch từ Sheet "Quản lý hợp đồng", Line 257-297) **phủ rất rộng các trạng thái hợp đồng** (mua mới / detail / upgrade / gia hạn / quá hạn) và verify được button change enable ở nhiều state — đây là điểm mạnh. Tuy nhiên có **1 vấn đề chặn**: KH report là "nút Hủy chuyển khoản (振込キャンセル) không hiển thị", còn TCs lại đi verify "button đổi năm→tháng / đổi phương thức được enable" — hai thứ khác nhau, cần confirm với Dev xem fix có thật sự giải quyết đúng cái KH thấy không. Ngoài ra cần bổ sung: 1 TC đúng flow KH + expected của KH, 1 negative test (button phải **giữ disabled** ở state không hợp lệ — fix "enable button" dễ bị over-enable), chiều **tháng→năm**, và check **ghost reference** của transfer đã hủy. Cuối cùng: nhớ tick 2 checkbox "Tester verify auto-fill" ở file 01 + 03 trước khi review có hiệu lực.

---

## 3. Coverage Matrix

> File 04 fetch nguyên trạng từ Sheet, **cấu trúc phân cấp** (Main/Sub → Expect), KHÔNG có TC ID/Type/Priority. Mapping dưới đây **suy luận** từ Main Function/Sub/Expect, tham chiếu bằng **số Row** trong Sheet.

| Impact | Loại | Priority | TCs map (suy luận — theo Row) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** (root: trạng thái chờ chuyển khoản disable button; fix: enable + hủy chuyển khoản trước) | Fix | — | R257-R291 (check button enable ở các state chờ chuyển khoản/chờ phát hành STK); R259 (hủy chuyển khoản thành công) | ~30 | **RISK** — verify "enable button change", KHÔNG verify đúng symptom KH (振込キャンセル hiển thị) → xem [BLOCKER] §4.1 |
| **F1** — `changeBillType()` (UserController) | Function | Direct | R257-R291 (change năm→tháng: 次回決済から月払いに変更する) | nhiều | **RISK** — chỉ năm→tháng; thiếu tháng→năm; thiếu negative |
| **F2** — `changePaymentMethod()` (UserController) | Function | Direct | R267-R272 (card→transfer: 銀行振込に変更する); R273-R278, R281 (transfer→card: クレジットカードに変更する) | nhiều | **RISK** — cả 2 chiều có; thiếu negative + delay callback |
| **F3** — `changeTypePayment()` (PointSettingController) | Function | Direct | (không phân biệt được từ UI — cùng button change) | ? | **RISK** — không có TC vào từ màn 次回決済 setting (entry point thứ 2) |
| **F4** — `changePaymentMethod()` (PointSettingController) | Function | Direct | (như F3) | ? | **RISK** — không tách được controller; có thể chưa test màn point setting |
| **F5** — `cancelTransfer()` (BotContracts.php) | Function | Direct | R259 (hủy chuyển khoản thành công); R260/R262/R264 (db: hủy change id transfer cũ); R274-R278 (change id transfer đã hủy) | vài | **RISK** — chỉ verify qua flow change; KHÔNG check ghost reference của transfer đã hủy |
| **F6** — view `detail.blade.php` | Function | Direct | R257-R291 (check GUI button enable/disable) | nhiều | **RISK** — chỉ verify "phải enable", thiếu verify "phải disabled khi state không hợp lệ" |
| **D (data)** — Dev khai "Không có" | Data | — | R268 (payment_method=2); R260/262/264 (db hủy change id transfer) | vài | **RISK** — Dev khai SAI: fix thực tế **update data** (xem [MAJOR] §4.2) |
| **T1** — Thay đổi phương thức thanh toán (card⇄transfer) | Feature | `<Dev chưa ghi risk>` | R267-R287 | nhiều | **RISK** — happy-path only; thiếu negative/edge + delay callback |
| **T2** — Thay đổi thời hạn thanh toán (năm→tháng, tháng→năm) | Feature | `<Dev chưa ghi risk>` | R257-R291 (chỉ năm→tháng) | nhiều | **GAP một chiều** — **tháng→năm KHÔNG có TC** |

### ORPHAN / TC chưa hoàn chỉnh

| TC (Row) | Title | Lý do | Hành động đề xuất |
|---|---|---|---|
| R294 | Check account staff | **Rỗng nội dung** (chỉ có Main Function, không steps/expected) | Member fill: staff có/không quyền truy cập màn detail HĐ + thao tác change (CL1) |
| R296-R297 | Change card information (メインカード情報を変更する → mở modal) | Không trực tiếp thuộc scope bug (hủy chuyển khoản / change năm-tháng / change phương thức) | Confirm: regression lân cận giữ lại, hay tách khỏi bộ TC của #36835 |
| R283-R284 | check khi bill failse / bill thành công → upgare lên plan pro | Bill callback khi upgrade — tangential, expected "đợi chốt" chưa rõ | Hoàn thiện expected hoặc tách sang scope upgrade |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Hybrid: Validation/UI-state enable + Cancel-transfer (soft-cancel) logic**. "Enable button" = nới điều kiện disable (validation). "Thực hiện logic hủy chuyển khoản trước" = soft-cancel pending transfer trước khi change. KHÔNG phải generic catch-all. |
| **Trigger space cần cover** | (a) Các trạng thái HĐ button **phải enable** (chờ chuyển khoản, chờ phát hành STK) — *đã cover*. (b) Các trạng thái button **phải GIỮ disabled** (đã thanh toán `status_payment∈{1,2}`, hoặc state không hợp lệ) — **chưa cover (negative)**. (c) 2 chiều change: năm↔tháng (**thiếu tháng→năm**), card↔transfer (đủ). (d) 2 entry point: bill detail (cover) vs màn point setting / 次回決済 (**chưa cover**). |
| **Số trigger TCs hiện cover** | Positive (enable) ~đủ rộng; Negative (disabled-khi-cần) = **0/?**; tháng→năm = **0**; point-setting entry = **0** |
| **KH report dạng** | **Symptom-only + DISCREPANCY** — KH nêu hiện tượng "nút 振込キャンセル không hiển thị", không nêu root cause; Dev/Kim Cúc tái hiện ra triệu chứng KHÁC (2 button change bị disable) |
| **Alternative root causes cần verify** | (1) 振込キャンセル là **chức năng riêng** mà KH muốn (hủy hẳn lệnh chuyển khoản đang chờ) — khác với "enable button change"; (2) button disable do điều kiện khác ngoài "trạng thái chờ chuyển khoản" (`univa_account_number`, `status_payment`, plan); (3) chỉ xảy ra ở một số plan/loại hợp đồng |
| **Anti-patterns dính** | **AP-2** (symptom-only + discrepancy), **AP-3** (happy-path-only regression), **AP-4** (PR link trống), **AP-6** (mục 3 trống); **AP-5 nhẹ** (nhiều TC dẫn bằng "check db") |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] SYMPTOM-ONLY/DISCREPANCY — GAP-1**: KH report literal *"nút Hủy chuyển khoản (振込キャンセル) không được hiển thị"* ở trạng thái 入金待ち, nhưng toàn bộ TCs + cách fix của Dev xoay quanh việc **enable 2 button change** (`次回決済から月払いに変更する`, `クレジットカードに変更する`). **Không có TC nào verify đúng expected của KH** (nút hủy/đổi khỏi chuyển khoản hiển thị & thao tác được trong 入金待ち). → Nguy cơ deploy xong KH vẫn thấy bug. **Fix**: (1) Hỏi Dev/PM xác nhận interpretation — "hủy chuyển khoản" của KH có phải được giải quyết qua flow change-phương-thức không, hay là một button/feature riêng? (2) Thêm **TC-NEW-01** mô phỏng đúng flow KH (HĐ năm, đang card → đổi sang chuyển khoản → status 入金待ち → quan sát màn detail) với expected theo đúng cái KH yêu cầu sau khi Dev confirm.

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE (over-enable) — GAP-2**: Fix là "enable button". Bộ TCs chỉ verify button **phải enable**, KHÔNG có TC negative verify button **phải GIỮ disabled** ở state không hợp lệ (vd `status_payment∈{1,2}` đã thanh toán, hoặc đã phát hành STK + đã nhập tiền). Fix nới điều kiện disable rất dễ over-enable. **Fix**: thêm **TC-NEW-02** (negative — button stays disabled).
- **[MAJOR] FIX-SHAPE (ghost reference) — GAP-3**: "Thực hiện logic hủy chuyển khoản trước" = soft-cancel pending transfer. TCs chỉ check `db: change id transfer đã hủy`, KHÔNG check **ghost reference** ở nơi khác (job phát hành số tài khoản còn chạy không? callback chuyển khoản cũ tạo bản ghi mồ côi không? màn list/lịch sử HĐ còn hiển thị transfer đã hủy không?). **Fix**: thêm **TC-NEW-04**.
- **[MAJOR] AP-6 — Mục 3 dev-impact TRỐNG**: Dev chỉ ghi heading "Đã check và sửa các function..." mà không list caller. Đặc biệt `changePaymentMethod()` xuất hiện ở **CẢ 2 controller** (UserController + PointSettingController) → có ≥ 2 entry point cùng pattern; mục 3 trống nghĩa là không biết còn màn nào khác cùng logic disable button. **Fix**: yêu cầu Dev list đầy đủ caller + các màn gọi đến button enable/disable này.
- **[MAJOR] AP-4 — PR link trống**: Mục "Commit / Pull Request" = `<chưa có>`. Không verify được fix là **blanket enable** (luôn enable) hay **conditional** (chỉ enable đúng state). Đây chính là gốc của GAP-2. **Fix**: yêu cầu Dev cung cấp PR link.
- **[MAJOR] Data-impact 4.2 khai SAI**: Dev ghi "Không có" data update, nhưng mục 2 (hủy chuyển khoản) + chính TCs (`payment_method=2`, `hủy change id transfer cũ`) cho thấy data **bị update**. → 4.2 thiếu, kéo theo thiếu D1/D2 và thiếu boundary/negative cho data. **Fix**: yêu cầu Dev bổ sung 4.2 (table/field bị update khi change phương thức + khi cancel transfer).
- **[MAJOR] T2 GAP một chiều**: TCs chỉ test **năm→tháng** (`次回決済から月払いに変更する`). Chiều **tháng→năm** (Dev list trong T2) không có TC. **Fix**: thêm **TC-NEW-03**.
- **[MAJOR] F3/F4 entry point thứ 2 chưa cover**: `changeTypePayment()`/`changePaymentMethod()` ở `PointSettingController` gợi ý có màn **次回決済 (point setting)** là entry point riêng. TCs chỉ thao tác từ màn bill detail. **Fix**: thêm **TC-NEW-05** (vào từ màn point setting).
- **[MAJOR] Bug task (01) auto-filled chưa verify**: File 01 `Auto-filled: 2026-06-03 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. Review chỉ có giá trị sau khi tester đọc lại Redmine #36835 (đặc biệt là sai lệch symptom ở [BLOCKER] §4.1) và tick checkbox.
- **[MAJOR] Dev-impact (03) auto-filled chưa verify**: File 03 `Auto-filled: 2026-06-03 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. F/D/T có thể chưa đầy đủ (đã thấy 4.2 khai sai, mục 3 trống) — yêu cầu tester verify + tick trước khi chốt.
- **[MAJOR] File 04 không đúng format 10 cột chuẩn**: Fetch nguyên trạng từ Sheet (cấu trúc phân cấp), thiếu **TC ID / Type / Priority / Precondition** → không đánh giá được phân bổ Positive/Negative/Boundary/Regression (mục C checklist), khó map mechanical, không trace được TC nào để member sửa. **Fix**: member convert sang format `templates/04-tc-list.template.md` (đặt TC ID, gán Type/Priority, tách Precondition rõ) trước round 2, HOẶC Leader chấp nhận review theo cấu trúc gốc + member cam kết bổ sung GAP.

### 4.3 Minor (có thể fix sau)

- **[MINOR] AP-5 — TCs dẫn bằng "check db"**: Rất nhiều TC expected là "check db: payment_method=2 / change id transfer đã hủy". Theo convention team (viết TC từ **góc nhìn manual tester** — quan sát UI), nên dẫn bằng cái tester **thấy trên màn** (status hiển thị, button state, message), đưa DB-check xuống làm verify phụ. Reframe khi convert sang 10 cột.
- **[MINOR] R294 rỗng**: "Check account staff" chưa có steps/expected (xem ORPHAN §3).
- **[MINOR] Typo trong nguồn**: `disiable`, `tranfer`, `failse`, `upgare`, `payment)method` — read-only nên KHÔNG sửa trực tiếp file 04, nhưng sửa lại khi convert sang format chuẩn.

### 4.4 Nit (gợi ý)

- **[NIT]** Khi convert sang 10 cột: gom nhóm TC theo **trạng thái hợp đồng** (Mua mới / Detail-card / Detail-transfer / Upgrade / Gia hạn / Quá hạn / Overdue) làm prefix Title để Leader map impact nhanh hơn.
- **[NIT]** R288 (job cancel HĐ quá hạn) liên quan **CL20 (hủy hợp đồng)** — cân nhắc bổ sung verify clear richmenu/schedule khi HĐ bị cancel.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` (bản convert) ở round tiếp theo. Expected của TC-NEW-01 chốt sau khi Dev confirm interpretation.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Verify đúng flow KH — 入金待ち của chuyển khoản, thao tác hủy/đổi khỏi chuyển khoản | HĐ năm, đang thanh toán card → đã đổi sang chuyển khoản (transfer); status = 入金待ち (chờ nhập tiền); `univa_account_number=null`, `status_payment∉{1,2}`, `payment_method=2` | 1. Vào màn detail hợp đồng. 2. Quan sát các nút thao tác liên quan chuyển khoản (振込キャンセル / đổi phương thức / đổi thời hạn). 3. Thực hiện thao tác hủy/đổi khỏi chuyển khoản. | **(Chốt sau khi Dev confirm)** Nút cho phép thoát khỏi trạng thái chuyển khoản hiển thị & enable; thao tác thành công; status cập nhật đúng — KHÔNG còn lặp lại đúng hiện tượng KH báo | High | Positive (BUG) | BUG, F2, F5 |
| TC-NEW-02 | Button change phải GIỮ disabled ở state không hợp lệ | HĐ ở state đã thanh toán (`status_payment∈{1,2}`) hoặc đã phát hành STK + đã nhập tiền | 1. Vào màn detail. 2. Quan sát button `次回決済から月払いに変更する` / `クレジットカードに変更する`. 3. Thử click. | Button đúng nghiệp vụ vẫn **disabled**, không cho thao tác sai (chống over-enable do fix) | High | Negative | F6, BUG |
| TC-NEW-03 | Change thời hạn tháng→năm khi đang chờ chuyển khoản | HĐ tháng, đang chờ chuyển khoản, button enable | 1. Vào detail. 2. Click button đổi tháng→năm. 3. Hoàn tất change. | Change tháng→năm thành công; payment/thời hạn cập nhật đúng; transfer cũ (nếu có) được hủy đúng | Medium | Positive | T2, F1 |
| TC-NEW-04 | Ghost reference sau khi hủy transfer (change transfer→card) | HĐ đang chờ chuyển khoản, có pending transfer change id | 1. Change transfer→card (nhập card). 2. Check job phát hành số tài khoản. 3. Check màn list + lịch sử HĐ. 4. Giả lập callback chuyển khoản cũ về sau. | Pending transfer bị hủy sạch: không job phát hành STK chạy tiếp; list/lịch sử không hiển thị transfer đã hủy; callback cũ KHÔNG tạo bản ghi mồ côi / không bill nhầm | High | Boundary/Regression | F5, D |
| TC-NEW-05 | Thao tác change từ màn 次回決済 (point setting) — entry point thứ 2 | HĐ đang chờ chuyển khoản; vào từ màn point setting (`PointSettingController`) | 1. Mở màn next-payment setting. 2. Thực hiện change năm→tháng / đổi phương thức. | Kết quả nhất quán với màn bill detail (button enable đúng, change thành công) | Medium | Regression | F3, F4 |
| TC-NEW-06 | Double click button change (CL5) | HĐ đang chờ chuyển khoản, button enable | 1. Double click nhanh `次回決済から月払いに変更する` (hoặc `クレジットカードに変更する`). | Không duplicate change id / không double bill / không tạo 2 transfer | Medium | Boundary | F1, F2, CL5 |
| TC-NEW-07 | Delay callback bill tiền sau change transfer→card (C.1) | Change transfer→card vừa thực hiện, callback card bill về trễ | 1. Thực hiện change. 2. Mô phỏng callback bill về sau delay. | Status hợp đồng cập nhật đúng khi callback về; không kẹt ở 入金待ち; không bill trùng | Medium | Boundary | T1, C.1 |
| TC-NEW-08 | Account staff truy cập + thao tác change (CL1) — hoàn thiện R294 | Staff được/không được phân quyền HĐ | 1. Login staff. 2. Vào màn detail HĐ. 3. Thử thao tác change. | Staff không quyền → không access; staff có quyền → thao tác như account chính | Low | Regression | CL1 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần làm rõ business rule (Dev/PM confirm trước khi chốt TCs)**:
  - **Rule enable/disable button theo trạng thái hợp đồng**: ở mỗi state (`status_payment`, `payment_method`, `univa_account_number`, có/chưa phát hành STK, plan) thì 3 nút `振込キャンセル` / `次回決済から月払いに変更する` / `クレジットカードに変更する` phải **enable hay disable**? Cần bảng quyết định để viết negative TC (TC-NEW-02) chính xác.
  - **Định nghĩa "Hủy chuyển khoản" mà KH muốn**: là button độc lập (`振込キャンセル`) hay được giải quyết gián tiếp qua flow đổi phương thức? (gốc của [BLOCKER] §4.1).
  - Người chịu trách nhiệm: Dev `Kieu Son Tung` + PM/CSS đã làm việc với KH.

---

## 7. Checklist đã chạy

- [x] A. Coverage — nhiều RISK/GAP (xem §3)
- [x] B. Chất lượng từng TC — thiếu Precondition/atomic do format Sheet phân cấp; TC dẫn bằng DB
- [x] C. Chất lượng bộ TC tổng thể — **không đánh giá được phân bổ Type/Priority** (file 04 thiếu 2 cột này); thiên về Positive/happy-path
- [x] D. Spec alignment — không có spec riêng; cần confirm business rule (§6)
- [x] E. Hành chính — file 04 thiếu tên tester + version; không đúng format 10 cột
- [x] F. Base checklist LME:
  - [x] F.1 Web — liên quan: **CL20** (hủy hợp đồng — R288 partial), **CL18** (load UI trước/submit sau — chưa cover), **CL5** (double click — chưa cover → TC-NEW-06), **CL2** (reload sau thao tác — partial), **CL1** (staff — R294 rỗng → TC-NEW-08). A.2 URLs đo lường bill success: cần regression (chưa cover).
  - [x] F.2 Job — **CLJ01** không trực tiếp (không chạm Google sync); job phát hành STK/cancel transfer thì liên quan → TC-NEW-04.
  - [x] F.3 Tính năng chung — **C.1 Bill tiền** liên quan trực tiếp (delay callback → TC-NEW-07; 5 loại bill không cần full vì scope là contract payment). **C.7 Plan limits** chạm nhẹ qua upgrade (R279-285) — không phải trọng tâm.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<Leader verify + ký>` | |
| Tester | (đã đọc & hiểu feedback) | |

---

> **Draft cho Leader verify** — không phải final. Ưu tiên xử lý [BLOCKER] §4.1 (confirm interpretation với Dev) trước, vì nó quyết định toàn bộ expected của bộ TC. Sau khi Dev confirm + cung cấp PR link + bổ sung mục 3/4.2, member convert file 04 sang format chuẩn và thêm 8 TC đề xuất.
