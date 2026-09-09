# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38077 — Status authorized trả về khi bill univapay sẽ coi là trường hợp bill success` |
| Reviewer (Leader) | `<điền tên Leader>` |
| Tester được review | TC human có sẵn (Thanh Phương map qua Redmine) |
| Ngày review | 2026-06-24 |
| Version TCs | `fetched-v1` |
| Vòng review | Round 1 |

> **Spec reference**: không có `02-spec-reference.md` riêng → dùng `templates/LME-SYSTEM-SPEC.md` tổng. Logic nghiệp vụ univapay đối chiếu thêm với block spec ngay trong Sheet gốc ("Sửa bill tiền univapay dùng callback", row 1–2): logic status_webhook 0/1/2/3/4 + mốc 5 phút + job 15 phút.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER + nhiều MAJOR, cần fix/bổ sung và review lại.

**Lý do ngắn gọn**: Bộ 15 TCs cover tốt **happy-path của bug** (5 case `authorized` → success) nhưng (1) **trigger space status univapay chưa đủ** — chỉ test 3/~6 status, thiếu `pending/error/canceled` để chứng minh fix không phá nhánh khác; (2) **scope caller chưa xác nhận** — fix nằm ở 2 function timeout cùng pattern bug, chưa loại trừ salon/event/bot bill có cùng bug; (3) input 01/03 auto-fill **chưa được tester verify**.

---

## 2. Tóm tắt cho member

Bộ TC fetch được bám rất sát cấu trúc nghiệp vụ — đủ 3 status × các kịch bản booking/item, Expected chi tiết tới field DB (`status_webhook`, `payment_status`, `s_order_history`...), map sạch vào F1/F2 không có case lạc chủ đề. Điểm cần bổ sung trước khi đủ tin cậy: **(a)** thêm TC cho các status univapay còn lại (`pending/error/canceled`) để chắc fix `authorized` không vô tình đụng nhánh khác; **(b)** thêm TC race "timeout job đã chốt authorized=success rồi webhook thật mới tới"; **(c)** xác nhận với Dev xem salon/event/bot bill có dùng chung chỗ map status univapay không — nếu có thì đang thiếu TC.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — `authorized` coi là bill success | Fix | — | TC-L03, TC-L06, TC-I03, TC-I06, TC-I09 | 5 | **RISK** — chỉ verify status `authorized`; chưa chứng minh status khác không bị fix làm hỏng (xem §3.5) |
| F1 — `getBookingTimeout` (lesson) | Function | Direct `<Dev chưa confirm>` | TC-L01→TC-L06 | 6 | **RISK** — đủ 3 status nhưng precondition chưa nói rõ là nhánh **timeout >5p** (đúng chỗ fix) |
| F2 — `getOrderTimeout` (item/sales) | Function | Direct `<Dev chưa confirm>` | TC-I01→TC-I09 | 9 | **RISK** — như F1; cover thêm change-card (tốt) |
| D1 — Dev khai "Không có" | Data | — | (TCs vẫn assert DB: `payment_status`, `status_webhook`, `s_order_history`, `s_cycle_order_history`) | — | **Mâu thuẫn nhẹ** — 4.2 nói no data nhưng fix đổi record nào được giữ/update (xem [MINOR]) |
| T1 — Job cover webhook timeout booking **lesson** | Feature | High `<confirm>` | TC-L01→TC-L06 | 6 | OK (regression baseline Successful/Failed có) |
| T2 — Job cover webhook timeout bill **item** (chu kỳ + 1 lần) | Feature | High `<confirm>` | TC-I01→TC-I09 | 9 | OK |
| (nghi ngờ) Bill **salon / event / bot** timeout — cùng pattern? | Feature | `<chưa rõ>` | — | **0** | **GAP** nếu dùng chung code map status (xem [BLOCKER] FIX-SHAPE) |

### ORPHAN TCs

Không có. Cả 15 TCs đều thuộc scope BUG / F1 / F2 / T1 / T2.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Specific code check / status-mapping** — thêm `authorized` vào tập status coi là "bill thành công". KHÔNG phải generic catch-all. |
| Trigger space cần cover | (a) **Status enum univapay**: `pending / authorized / successful / failed / error / canceled` (≈6). (b) **Caller / loại bill** dùng chung chỗ map status: bot / item / salon / lesson / event (5). |
| Số trigger TCs hiện cover | Status: **3/~6** (successful, failed, authorized). Loại bill: **2/5** (lesson, item). |
| KH report dạng | **Không có KH report** — file 01 description trống, không Steps/Actual/Expected. Bug 100% do Dev đánh giá → không cross-check được từ phía KH. (Nặng hơn symptom-only.) |
| Alternative root causes cần verify | Từ KH: N/A (không có report). Từ fix: các status khác (`pending/error/canceled`) bị xử lý sai sau khi đổi mapping; nhánh **timeout** vs **webhook bình thường**; race timeout-job ↔ webhook thật. |
| Anti-patterns dính | **AP-6** (mục 3 caller chưa chi tiết/chưa confirm callers khác) · **AP-1 (một phần)** — không generic-catch nhưng trigger-space (status enum) thiếu giống bản chất AP-1 · **AP-2 (biến thể)** — không có KH report nên không thể đối chiếu root cause khác. |

> Trigger space cover < tổng (status 3/6, bill 2/5) → flag [BLOCKER] + [MAJOR] FIX-SHAPE ở §4.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / AP-6 — GAP-1 (scope caller chưa xác nhận)**: Fix được áp ở **2 function timeout độc lập cùng pattern** (`getBookingTimeout` ở CalendarCourseBookingService **và** `getOrderTimeout` ở SalesService). Việc cùng 1 bug xuất hiện ở 2 chỗ là tín hiệu mạnh rằng **các loại bill khác qua univapay (salon booking, event booking, bot) có thể có function timeout tương tự dính cùng bug** mà Dev chưa liệt kê (mục 3 dev-impact để trống/chưa chi tiết). — **Fix**: yêu cầu Dev (a) confirm chỗ interpret status univapay là **helper dùng chung** hay **lặp lại từng function**; (b) liệt kê đầy đủ mọi function timeout gọi tới nó. Nếu dùng chung / có function salon-event-bot cùng pattern → **bắt buộc thêm TC** (TC-NEW-04). Đọc PR `pull-requests/10449/diff` để verify fix shape thực tế.

- **[BLOCKER] FIX-SHAPE — GAP-2 (status space chưa đủ)**: Fix đổi mapping status → **bắt buộc verify các status univapay còn lại không bị fix làm sai**. TCs hiện chỉ test `successful/failed/authorized`. Thiếu đặc biệt **`pending`** (đang xử lý — KHÔNG được coi là success, phải để job quét tiếp / giữ booking) và **`error/canceled`**. Rủi ro: impl kiểu `status in (successful, authorized)` đúng cho authorized nhưng nếu lỡ gom nhầm `pending`/khác → mất booking hoặc chốt success sai. — **Fix**: thêm TC-NEW-01 (`pending`) + TC-NEW-02 (`error/canceled`) cho cả lesson và item.

### 4.2 Major (nên fix)

- **[MAJOR] AUTO-FILL chưa verify — `01-bug-task.md`**: Auto-filled `2026-06-24 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. Vì description Redmine trống, tester phải tự xác nhận lại bug/scope. — **Fix**: tester đọc lại Redmine #38077 + journals, điền Module/Môi trường, tick checkbox.
- **[MAJOR] AUTO-FILL chưa verify — `03-dev-impact.md`**: Auto-filled nhưng checkbox chưa tick; F1/F2 còn `Direct/Indirect <tester confirm>`, T1/T2 risk chưa chốt, mục 3 caller chưa chi tiết. F/D/T có thể chưa đủ → review chưa có giá trị tuyệt đối tới khi tick. — **Fix**: tester verify 4 mục với Dev, đặc biệt mục 3 + 4.2.
- **[MAJOR] FIX-SHAPE — timeout path chưa tường minh**: Function được fix là **getBookingTimeout / getOrderTimeout** = nhánh **webhook timeout (>5 phút) → job quét lại**. Precondition các TC ("job get kết quả bill chạy") chưa nói rõ đây là nhánh timeout (vs webhook tới bình thường). Nếu TC thực chạy nhánh webhook thường thì **không thật sự verify F1/F2**. — **Fix**: thêm precondition tường minh "webhook KHÔNG tới trong 5 phút → `status_webhook=4` → job timeout chạy → univapay trả `authorized`" (TC-NEW-05).
- **[MAJOR] WEBHOOK race / duplicate (TC-22, C.1, TC-21)**: Sau fix, job timeout chốt `authorized=success` (`status_webhook=1`, send action/remind, +counter receptions). Nếu **webhook thật tới sau đó** (success hoặc failed) → có double send action/remind? double cập nhật `total_booking/total_approve/total_request`? hoặc webhook=failed lật ngược booking đã chốt success? Chưa có TC. — **Fix**: thêm TC-NEW-03 (chuỗi timeout-job-chốt-authorized → webhook thật tới).
- **[MAJOR] C.1 Bill tiền — error/abnormal scenarios chưa đủ**: Theo checklist C.1 + TC-21/TC-22, fix chạm payment phải cover luồng ngoại lệ (retry / hủy giữa chừng / thanh toán trùng / charge sau khi hủy) và **toàn bộ pattern webhook** (normal/abnormal/exception/chưa nhận/trùng). Hiện chỉ có normal success/fail. — **Fix**: bổ sung theo §5 + đối chiếu C.1 error list.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Mâu thuẫn 4.2 "không có data" vs Expected có ghi DB write**: Dev khai D1=Không có, nhưng Expected của TCs verify hàng loạt field (`payment_status=1`, `status_webhook=1/2`, xóa/giữ record `s_order_history`, `s_cycle_order_history`, counter `calendar_course_receptions`). Bản chất fix đổi **record nào được giữ/update**. — **Fix**: tester xác nhận lại mục 4.2 với Dev; nếu thực có thay đổi data-state thì ghi vào D1 để coverage matrix đúng.
- **[MINOR] Type/Priority do AI suy luận**: 2 cột này không có trong Sheet gốc (đã ghi rõ trong file 04). Leader chốt lại trước khi dùng làm chuẩn phân bổ.
- **[MINOR] Module/Môi trường file 01 còn `<chưa rõ>`**: cần tester điền (Bill/Univapay; staging vs dev cho việc giả lập webhook).

### 4.4 Nit (gợi ý)

- **[NIT] Boundary mốc thời gian 5 phút / job 15 phút (TC-04, TC-07)**: cân nhắc TC biên webhook tới ngay sát mốc 5:00 (4:59 vs 5:01) để chắc nhánh timeout kích đúng lúc.
- **[NIT] C.2 friend block**: status=authorized→success có send message/action; nếu user đã block bot thì phải skip send. Có thể thêm 1 TC nhẹ (TC-NEW-06).
- **[NIT] i18n message JP**: Expected có chuỗi JP (`決済が完了しました。` ...) — verify hiển thị đúng phía line user.

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Job timeout — univapay status = `pending` → KHÔNG coi là success | Booking lesson **và** item tạo qua univapay; webhook không tới trong 5p (`status_webhook=4`); job timeout chạy | Job timeout query univapay, status trả về = `pending` (đang xử lý) | KHÔNG xóa, KHÔNG chốt success: `status_webhook` giữ nguyên (không =1), không send action/remind, không +counter; để job quét lại lần sau (theo logic 15p) | High | Boundary/Negative | BUG, F1, F2 |
| TC-NEW-02 | Job timeout — univapay status = `error` / `canceled` | Như trên | Job timeout query univapay, status = `error` (hoặc `canceled`) | Xử lý như fail: xóa booking/order tương ứng, send message fail, counter trả về đúng — KHÔNG bị nhận nhầm thành success | High | Negative | BUG, F1, F2 |
| TC-NEW-03 | Race — job timeout chốt `authorized`=success rồi webhook thật mới tới | Job timeout đã set `status_webhook=1` cho booking/order do nhận `authorized` | (1) Webhook thật tới = `successful`; (2) lặp lại với webhook thật = `failed` | Không double send action/remind, không double cập nhật `total_booking/total_approve/total_request`; case webhook=failed sau khi đã chốt success → xác định rõ hành vi (giữ hay revert) theo spec, không silent sai lệch DB | High | Boundary/Regression | T1, T2, BUG (TC-22) |
| TC-NEW-04 | Salon / Event / Bot bill — univapay `authorized` ở nhánh timeout | (Chỉ chạy sau khi Dev confirm có function timeout tương tự) bill salon/event/bot qua univapay; webhook timeout | Job timeout của salon/event/bot query univapay = `authorized` | Coi là bill success giống lesson/item (nếu dùng chung mapping). Nếu hành vi KHÁC → là bug bỏ lọt cùng pattern #38077 | High | Regression | GAP-1 (caller scope), C.1 |
| TC-NEW-05 | Verify đúng nhánh **timeout** (không phải webhook thường) cho case `authorized` | Booking/item; chủ động **không gửi webhook trong 5 phút** → `status_webhook=4` | Để job timeout `getBookingTimeout`/`getOrderTimeout` tự chạy → query univapay = `authorized` | Booking/order được GIỮ + update success (giống Expected TC-L03/TC-I03), chứng minh fix nằm đúng ở nhánh timeout | High | Positive | BUG, F1, F2 |
| TC-NEW-06 | Friend block — authorized success nhưng user đã block bot | User đã block bot; bill `authorized` chốt success qua job timeout | Job timeout chốt success → tới bước send message/action | Không send message/remind tới user đã block (theo C.2 friend block); phần DB vẫn update đúng | Low | Negative | C.2, T1/T2 |

---

## 6. Spec update needed

- [x] **Cần làm rõ spec (không phải update, mà bổ sung tài liệu hoá)** — bảng mapping **đầy đủ status univapay → hành động** (mỗi status trong `pending/authorized/successful/failed/error/canceled` ở cả nhánh webhook thường lẫn nhánh timeout) hiện chỉ nằm rải rác trong Sheet. Đề nghị Dev/PM chốt 1 bảng canonical để TCs bám theo.
  - Section: logic "Sửa bill tiền univapay dùng callback" (status_webhook 0/1/2/3/4 + mốc 5p/15p).
  - Nội dung cần update: liệt kê đủ status enum + hành động + phạm vi loại bill (bot/item/salon/lesson/event) dùng chung.
  - Người chịu trách nhiệm: Dev Thanh Phương (xác nhận từ PR 10449).

---

## 7. Checklist đã chạy

- [x] A. Coverage — build matrix (mechanical OK, không orphan) nhưng A.6 fix-shape lộ RISK/GAP.
- [x] B. Chất lượng từng TC — Title/Steps/Expected rõ, atomic; precondition timeout chưa tường minh (MAJOR).
- [x] C. Chất lượng bộ TC — tỷ lệ lệch về happy/baseline, thiếu negative status-space; Priority do AI suy luận.
- [x] D. Spec alignment — không có 02; đối chiếu block spec trong Sheet, không mâu thuẫn nhưng spec cần tài liệu hoá (§6).
- [x] E. Hành chính — TC fetched read-only, ID tự gán TC-L/TC-I; nguồn ghi rõ trong file 04.
- [x] F. Base checklist LME:
  - [x] F.1 Web — phần lớn không áp dụng (đây là job, không phải màn web mới). CL-Func-19 (trigger chat 1:1) có liên quan: Expected đã ghi "CHECK TRIGGER HIỂN THỊ TRÊN CHAT 1:1" ✔.
  - [x] F.2 Job — **B.1 Job callback ÁP DỤNG TRỰC TIẾP** (đây là job cover webhook/callback univapay). Sheet B.1 chưa có item chuẩn → dùng TC-22 (webhook patterns) + TC-21 (payment flows) ở §A.1+ làm chuẩn → còn thiếu (xem §4.2).
  - [x] F.3 C.1 Bill tiền ÁP DỤNG → error/abnormal scenarios + webhook duplicate chưa đủ (MAJOR). C.2 friend block (NIT).

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<điền>` | |
| Tester | (đã đọc & hiểu feedback) | |

<!-- Review tự động bởi /review-tc dựa trên 01 + 03 + 04. Draft để Leader verify. Các điểm BLOCKER cần Dev confirm (caller scope qua PR 10449 + status enum) trước khi chốt verdict cuối. -->
