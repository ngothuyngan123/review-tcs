# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #36443 — [Item] Decision Univapay lỗi — màn quay lại trước khi bấm nút mua, chỉ single-shot product fail |
| Reviewer (Leader) | `<điền sau khi verify draft>` |
| Tester được review | `<chưa fill trong 04-tc-list.md>` |
| Ngày review | 2026-05-18 |
| Version TCs | v1 (fetched từ Sheet master) |
| Vòng review | Round 1 |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng + checklist LME, không có `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER + nhiều MAJOR, phải fix + review lại

**Lý do ngắn gọn**: (BLOCKER) Bộ TCs chỉ test **1 loại lỗi Univapay** (vượt max bill) — fix Dev là **generic error handler**, nếu không cover các error type khác (card declined, 3D Secure fail, insufficient funds, network timeout, expired card...) thì không verify được fix có catch generic hay chỉ handle 1 error code → có thể bỏ lọt scenario KH thực tế (KH chỉ report "màn quay lại", không nói rõ "vượt max"). (MAJOR) 2 file input 01+03 chưa verify auto-fill, mục 3 dev-impact trống, 4 boundary TC trống expected, 2 double-click + 2 "chưa get kết quả" thiếu steps, thiếu test Android+iPhone explicit.

---

## 2. Tóm tắt cho member

Bộ TCs cover được flow chính của bug (số tiền > max Univapay → message lỗi) cả case webhook + không webhook, cả single-shot + chu kỳ — đó là điểm mạnh. Nhưng có **gap nghiêm trọng**: chỉ test **1 loại lỗi** (vượt max), trong khi fix Dev là generic — nghĩa là không verify được fix có handle các Univapay error khác (card declined, 3D Secure, network timeout, expired card,...). KH gốc không nói rõ loại lỗi, chỉ thấy "màn quay lại" → có thể KH gặp error type khác, fix không cover thì bug original chưa fix. Ưu tiên fix theo thứ tự: (1) **bổ sung TCs cho ≥ 4 loại Univapay error** phổ biến, (2) tick 2 checkbox auto-fill 01+03, (3) clarify với Dev cách implement error handler (generic catch-all hay specific code), (4) fill expected cho 4 row boundary + steps cho 4 row double-click/timing.

---

## 3. Coverage Matrix

> File 04 dùng sheet outline schema (row 292-311), KHÔNG có cột TC ID rõ — mapping dưới đây dùng row number làm ID tạm. Suy luận từ Title / Step / Expected.

| Impact | Loại | Priority | TCs map (row #) | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause — Univapay return lỗi nhưng frontend không hiển thị message) | Fix | — | 295, 298, 302, 306 (chỉ test 1 error type = vượt max) | 4 | **RISK → GAP** — Fix là generic error handler. Bộ TCs chỉ verify với `AMOUNT_EXCEEDED`, không cover các Univapay error khác (xem §4.1 BLOCKER-1) |
| F1 — `paymentCreditCardItemV2Univapay` | Function | Direct | 293-308 (16 rows đi qua function này) | 16 | **OK** về số lượng — RISK về **chiều sâu** (xem §4.2) |
| D1 — _(k có)_ | Data | — | N/A — Dev confirm không chạm data | 0 | **OK (N/A)** |
| T1 — Bấm nút mua item, **case có webhook** | Feature | High | 300, 301, 302, 303, 304, 305, 306, 307, 308 | 9 | **OK** số lượng — RISK chiều sâu (expected trống 301/305, step trống 303/307/308) |
| Bonus — Case **không webhook** (regression, không thuộc 4.3 Dev) | Regression | — | 293, 294, 295, 296, 297, 298, 299 | 7 | **OK** — Nhưng nếu code path khác webhook thì Dev nên đưa vào 4.3 (xem §4.2 Major-3) |
| Bonus — **Stripe cover** (function khác) | Regression | — | 309, 310, 311 | 3 | **NIT** — Không thuộc fix scope (function `paymentCreditCardItemV2Univapay` không chạm Stripe). Xem §4.4 |

### ORPHAN TCs

| Row | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| 309-311 | Check cover bill tiền **stripe** | Không nằm trong F1/D1/T1 của Dev impact. Function fix là Univapay-specific, không chạm Stripe code path. | **Giữ** dưới dạng smoke regression — confirm member chủ ý hay nhầm scope. Nếu giữ → re-label rõ "Regression: verify Stripe flow không bị break by Univapay fix". |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] GAP-1: Bộ TCs chỉ test 1 loại lỗi Univapay (`AMOUNT_EXCEEDED`) — không cover các error type khác**. Dev fix là **generic** ("set error message return về frontend"), không phải fix riêng case "vượt max". Nhưng cả 4 TC verify message lỗi (rows 295/298/302/306) đều dùng cùng 1 trigger `bill = 500,001` → chỉ verify được 1 error code. Nếu implementation Dev là `if (error.code === 'AMOUNT_EXCEEDED') return error.message` (specific) thay vì `try-catch generic` → các error khác (card declined, 3D Secure fail, insufficient funds, expired card, network timeout, account suspended, duplicate transaction, 不正利用検知) vẫn silent fail = bug KH chưa fix triệt để. **KH gốc chỉ report hiện tượng "màn quay lại trước khi bấm nút mua", KHÔNG nói rõ là lỗi gì** — Dev đoán "vượt max" để tái hiện, nhưng KH thực tế có thể gặp error type hoàn toàn khác. **Action**: (a) hỏi Dev xác nhận implementation là generic catch hay specific code-check, (b) bổ sung ≥ 4 TC cho các Univapay error type phổ biến khác (xem §5 TC-NEW-06 → TC-NEW-09), (c) verify với account test Univapay sandbox dùng test card numbers của Univapay docs để trigger từng error type.

### 4.2 Major (nên fix)

- **[MAJOR] 01-bug-task.md — auto-fill chưa verify**: file có `Auto-filled: 2026-05-18 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. Tester đọc lại description Redmine + journal Thanh Phương để confirm: (a) steps reproduce có đúng KH gặp không (KH report không nói số tiền cụ thể — Dev tái hiện theo hướng "> max", có thể KH gặp case khác?), (b) field "Môi trường phát hiện" đang `<chưa rõ>` → fill từ thông tin Slack/Redmine.
- **[MAJOR] 03-dev-impact.md — auto-fill chưa verify**: tương tự, checkbox chưa tick. Cần tester confirm 4 mục (F1/D1/T1) đầy đủ chưa, không sót impact.
- **[MAJOR] 03-dev-impact mục 3 trống — caller chưa list**: Dev chỉ ghi heading "Đã check và sửa các function sử dụng đến function/data vừa sửa" nhưng không list function nào. Cần Dev confirm `paymentCreditCardItemV2Univapay` có caller khác không (vd có wrapper trong service layer hay được gọi từ controller khác?). Nếu có caller bị bỏ sót → có thể có function khác cũng trả lỗi univapay mà không hiển thị → cùng bug pattern.
- **[MAJOR] Rows 294, 297, 301, 305 — boundary `bill = 500,000` (= max) thiếu expected**: 4 rows này có step rõ (`mua item có set số tiền bill = 500,000`) nhưng cột Expected **TRỐNG**. Tester chạy xong không biết pass hay fail — đây là boundary CHÍNH XÁC (≤ vs <) mà Univapay xử lý có thể khác nhau. Hỏi Dev/Univapay docs xem `= max` là success hay fail, rồi fill expected.
- **[MAJOR] Rows 299, 308 — "check double click button mua" thiếu steps + expected**: 2 rows chỉ có col B = `check double click button mua`, các cột Precondition / Step / Expected đều **TRỐNG**. Đây là checklist LME CL5 (double-click) — phải có cách reproduce rõ + expected (vd: chỉ 1 request được gửi, không duplicate bill, message lỗi chỉ hiện 1 lần). Nếu để trống, tester sẽ skip hoặc test sai.
- **[MAJOR] Rows 303, 307 — "Check case bill tiền chưa get được kết quả bill ngay" thiếu cách reproduce**: Expected ghi link XD design mới (`https://xd.adobe.com/view/6d6b04be-0175-4ffe-a980-d57cf80ef7a9-3838/specs`) là tốt, nhưng KHÔNG có cách trigger "chưa get kết quả ngay". Cần ghi rõ: throttle network, force webhook delay từ Univapay test mode, hay disable webhook callback? Nếu không, tester không reproduce được scenario này.
- **[MAJOR] Compatibility — thiếu test Android + iPhone explicit**: KH gốc report `Cả Android và iPhone đều không được` (file 01). Bộ TCs hiện tại không tách 2 env này — tester có thể chỉ test 1 platform. Áp dụng checklist LME §A.2 Compatibility (Android + iOS bắt buộc). Đề nghị thêm note vào precondition của row 295/298/302/306 (4 TC verify bug fix) hoặc tách thành 2 TC mỗi platform.
- **[MAJOR] Member tự check `04-tc-list.md` — checklist LME tick thiếu căn cứ**: file 04 hiện chỉ tick `C.1 Bill tiền` ở §C — đúng, nhưng các mục Coverage check / §A / §B / §F.2 (Job callback — case webhook chính là callback flow) đều unchecked. Member cần rà lại — đặc biệt `B.1 Job callback` vì T1 explicit là "case có webhook" = callback flow.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC thiếu TC ID**: cả 19 rows chỉ có row number, không có ID dạng `TC001`. Khi sync lên Sheet master / khi reference trong report sẽ khó. Đề nghị member assign ID khi đưa vào round 2.
- **[MINOR] Member info trống trong 04**: `Tester viết TCs`, `Ngày submit` vẫn là placeholder `<member điền sau khi review>`. Fill trước khi submit round 2.
- **[MINOR] Outline schema không khớp 10-cột chuẩn**: sheet "Improve bill tiền univapay" dùng nested outline (col A→B→C→D→G→H, không có Type/Priority/Output note/Assignee). Member tham khảo `templates/04-tc-list.template.md` để bổ sung 4 cột còn thiếu nếu push lên master sheet mới — hoặc Leader confirm giữ schema cũ.
- **[MINOR] Row 300 status `OK` đơn lẻ**: chỉ row 300 (có webhook, bill 1 lần, 499,999, expected success) là `OK`, 18 rows còn lại `Not test`. Có thể member đã chạy thử 1 case smoke. Nếu vậy, ghi note ở Output (cột E/F hiện trống) — bao giờ chạy, environment nào.

### 4.4 Nit (gợi ý)

- **[NIT] Rows 309-311 Stripe regression**: function fix `paymentCreditCardItemV2Univapay` không chạm Stripe code path → không bắt buộc theo "root cause layer focus". Nếu member chủ ý smoke regression cho controller chung `SalesManagementV2Controller` → re-label title thành "Regression: Stripe flow không bị break bởi fix Univapay". Nếu không chủ ý → remove để bộ TC focus hơn.
- **[NIT] Thêm TC reproduce với exact data KH**: KH user `wings.nontitle@gmail.com`, bot `バリューオブスピーカー` có item single-shot fail. Nếu reproduce được trên staging với data tương đương (hoặc verify trực tiếp trên production sau deploy bằng dry-run) → thêm 1 TC mô tả flow KH gốc, không chỉ test theo "> max". KH có thể gặp case khác chưa được cover.
- **[NIT] Verify message lỗi UX business-friendly**: Dev fix là "Set error message return về frontend". Nhưng message có user-friendly không (vd: "Số tiền vượt giới hạn của Univapay") hay raw API error? Đề nghị thêm 1 TC verify CONTENT của message + có nút retry / nút quay lại không.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo (hoặc fill vào 4 row hiện đang trống thay vì thêm row mới).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Bill Univapay = max → verify pass/fail rõ ràng (fill 4 row boundary 294/297/301/305 đang trống expected) | Account Univapay test có max bill = 500,000. Item single-shot price = 500,000. | 1) Mở page item trên LINE app. 2) Bấm nút **Mua**. 3) Confirm decision Univapay. | (Cần hỏi Dev/check Univapay docs — `=` có vào `<= max` hay phải `< max`. Sau khi rõ → fill: success+redirect talklist HOẶC fail+message lỗi) | High | Boundary | BUG, F1, T1 |
| TC-NEW-02 | Double-click button Mua khi bill > max → verify không duplicate request + message lỗi 1 lần (fill row 299 + 308) | Account Univapay max 500K, item single-shot 500,001. | 1) Mở page item trên LINE app. 2) **Double-click rất nhanh** button Mua (interval < 500ms). 3) Confirm decision Univapay (nếu modal mở). | Chỉ 1 request `paymentCreditCardItemV2Univapay` được gửi (verify Network tab hoặc DB log). Message lỗi hiển thị **1 lần** (không stack 2 toast). User không bị charge double khi `< max` (case happy path: chỉ 1 bill thành công). | High | Boundary | F1, T1, **CL5** (double-click) |
| TC-NEW-03 | Bug reproduce trên cả Android + iPhone (compatibility — explicit theo KH report) | Account Univapay max 500K, item single-shot 500,001. Test trên LINE app Android + iPhone. | 1) Mở LINE app **Android** → page item → bấm Mua → confirm. 2) Lặp lại trên LINE app **iPhone**. | Cả 2 device đều hiển thị message lỗi (không silent fail, không tự đóng màn). UX message giống nhau giữa Android/iPhone. | High | Regression | BUG, T1, **§A.2 Compatibility** |
| TC-NEW-04 | Webhook timing — case Univapay trả webhook chậm, frontend không nhận kết quả ngay (fill row 303 + 307) | Account Univapay test có thể delay webhook (Univapay sandbox setting hoặc throttle network 3G slow). Item single-shot Univapay liên kết webhook. | 1) Throttle network LINE app xuống slow 3G (hoặc force Univapay sandbox delay webhook ≥ 5s). 2) Mở page item → bấm Mua → confirm. | Hiển thị màn thông báo theo design mới (XD link: https://xd.adobe.com/view/6d6b04be-0175-4ffe-a980-d57cf80ef7a9-3838/specs) — không quay về talklist ngay, có loading/polling state. Sau khi webhook về → cập nhật trạng thái success/fail tương ứng. | Medium | Boundary | T1, **B.1 Job callback** |
| TC-NEW-05 | Verify message lỗi business-friendly + có UX recovery (NIT — nên thêm) | Account Univapay max 500K, item single-shot 500,001. | 1) Mở page item → bấm Mua → confirm decision. 2) Quan sát message lỗi: content + UX. | Message lỗi: (a) **content** rõ ràng cho user (vd: "Số tiền vượt quá giới hạn cho phép của Univapay" — không phải raw `error_code: AMOUNT_EXCEEDED`), (b) có **nút quay lại / đóng** rõ, (c) không tự đóng. | Medium | Positive | BUG, T1 |
| **TC-NEW-06** | **Univapay error — Card declined (decline_code: card_declined)** | Account Univapay sandbox. Item single-shot bill < max. Dùng **test card number** Univapay sandbox cho case `declined` (vd `4000 0000 0000 0002` hoặc theo Univapay docs). | 1) Mở page item → bấm Mua. 2) Nhập test card declined. 3) Confirm decision. | Hiển thị **message lỗi** rõ ràng cho user (vd: "Thẻ bị từ chối, vui lòng dùng thẻ khác"). KHÔNG silent fail / KHÔNG quay về talklist im lặng. Frontend nhận được error từ `paymentCreditCardItemV2Univapay`. | High | Negative | BUG, F1, T1 |
| **TC-NEW-07** | **Univapay error — Insufficient funds (decline_code: insufficient_funds)** | Account Univapay sandbox. Test card cho case insufficient (theo Univapay docs). | 1) Mở page item → bấm Mua. 2) Nhập test card insufficient. 3) Confirm. | Message lỗi hiển thị, content business-friendly (vd: "Số dư không đủ"). | High | Negative | BUG, F1, T1 |
| **TC-NEW-08** | **Univapay error — Expired card (decline_code: expired_card)** | Test card hết hạn (Univapay sandbox). | 1) Mở page item → bấm Mua. 2) Nhập test card expired. 3) Confirm. | Message lỗi hiển thị (vd: "Thẻ đã hết hạn"). | High | Negative | BUG, F1, T1 |
| **TC-NEW-09** | **Univapay error — 3D Secure fail (`three_ds_failed` / authentication_failed)** | Account có bật 3D Secure. Test card require 3DS → user cancel hoặc nhập sai OTP. | 1) Mở page item → bấm Mua. 2) Nhập test card 3DS. 3) Ở màn 3DS, cancel hoặc nhập sai OTP. | Message lỗi hiển thị (vd: "Xác thực 3D Secure thất bại"). Không silent fail. | High | Negative | BUG, F1, T1 |
| **TC-NEW-10** | **Univapay error — Network timeout / API down (5xx response)** | Force network timeout (throttle / mock Univapay API trả 500 / 503). | 1) Throttle network LINE app hoặc mock Univapay sandbox trả 500. 2) Mở page item → bấm Mua → confirm. | Message lỗi hiển thị (vd: "Đã xảy ra lỗi, vui lòng thử lại"). KHÔNG quay về talklist im lặng. | Medium | Negative | BUG, F1, T1 |
| **TC-NEW-11** | **Generic catch-all — error type không biết trước (Univapay add error code mới trong tương lai)** | Mock Univapay trả 1 error code KHÔNG có trong list handler hiện tại (vd: `unknown_decline_reason`). | 1) Mock Univapay sandbox trả error code mới. 2) Bấm Mua → confirm. | Frontend vẫn hiển thị **1 message lỗi fallback** (vd: "Thanh toán thất bại, vui lòng liên hệ hỗ trợ"). KHÔNG silent fail dù error code chưa được handle riêng. | High | Boundary | BUG, F1, T1 — **verify implementation generic catch** |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec — đây là bug-fix surface message lỗi đã tồn tại từ Univapay API, không thay đổi business rule.
- [ ] Cần update spec

> Tuy nhiên Dev nên bổ sung vào docs internal: **mọi controller bill tiền (Univapay/Stripe/...) phải set error message return về frontend** — để tránh pattern bug tương tự ở các flow khác (item chu kỳ chưa fail, salon, lesson, event booking).

---

## 7. Checklist đã chạy

- [x] A. Coverage — pass cho BUG/F1/T1 (số lượng), risk chiều sâu (xem §4.2)
- [ ] B. Chất lượng từng TC — **FAIL**: 8/19 TC thiếu expected hoặc steps
- [x] C. Chất lượng bộ TC tổng thể — Positive/Negative/Boundary có, regression có, không trùng lặp rõ
- [x] D. Spec alignment — TC không mâu thuẫn spec
- [ ] E. Hành chính — **FAIL**: thiếu TC ID, thiếu tester name + ngày submit
- [ ] F. Base checklist LME
  - [ ] F.1 Checklist web — member chưa tick A.1 (CL5 double-click có TC nhưng trống — không pass), A.2 Compatibility thiếu (xem §4.2)
  - [ ] F.2 Checklist job — **B.1 Job callback** relevant (case webhook) nhưng member chưa tick
  - [x] F.3 Các tính năng chung — **C.1 Bill tiền** đã cover (item 1 lần + item chu kỳ)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
