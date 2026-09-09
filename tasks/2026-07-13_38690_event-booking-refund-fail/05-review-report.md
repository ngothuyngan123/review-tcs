# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38690 — [Event booking] Thao tác refund bị "refund fail"` |
| Reviewer (Leader) | `<Leader ký>` (draft sinh bởi `/review-tc`) |
| Tester được review | `Thanh Phương` |
| Ngày review | `2026-07-13` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: không có `02-spec-reference.md` → dùng `templates/LME-SYSTEM-SPEC.md` tổng (feature Event Booking / FA-021). Không có spec riêng cho luồng refund của task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ 5 TC **chỉ có case Normal (happy path)** — không có TC Abnormal/Boundary nào, trong khi bug gốc chính là **luồng lỗi báo sai** ("refund fail" giả). Fix dùng phân nhánh `if prefix == 'ch' → charge, else → payment_intent`; **nhánh `else` là giả định chưa được verify** (Dev tự ghi rủi ro này) nhưng không có TC nào chạm. Đây là task **bill tiền** (RULE-08) nên không được kết luận từ staging.

---

## 2. Tóm tắt cho member

Điểm tốt: bộ TC đã bám đúng điểm mấu chốt nhất của fix — **test song song nhánh cũ (`ch_`) và nhánh mới (`pi_`)** (TC001 + TC002), đúng tinh thần RULE-09 / `COMPAT-LEGACY-001`; và đã giữ 2 TC regression cho luồng UnivaPay + option "chỉ refund LME" để chắc nhánh không bị chạm vẫn chạy. Expected cũng đi đủ 3 tầng (DB `status_payment=2` → màn admin → dashboard Stripe), đây là điều nhiều bộ TC khác thiếu.

Điểm cần fix: cả 5 TC đều là **Normal**. Bug này sinh ra từ **luồng lỗi**, nên phải có TC cho lỗi thật: refund lại booking đã refund, Stripe timeout/5xx, error code lạ → verify message hiển thị **đúng nguyên nhân**, không "báo thành công giả" và không đổ raw error ra GUI. Ngoài ra cần 1 TC boundary cho `strip_charge_id` **rỗng/NULL/prefix lạ** (vì code rơi vào nhánh `else` = coi như `pi_`), 1 TC double-click nút refund, và tối thiểu 1 TC chạy **trên production** vì đây là luồng tiền.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — refund fail với booking PaymentIntent (`pi_`) | Fix | — | TC002 | 1 | **RISK** — chỉ Normal; TC002 lại đang có Actual "chưa tạo được lịch sử" + Status trống ⇒ chưa có kết quả |
| F1 — `refundMoneyBookingEvent` (file duy nhất bị sửa) | Function | Direct | TC001, TC002, TC003, TC004, TC005 | 5 | **RISK** — có Normal cho mọi nhánh, nhưng 0 Abnormal / 0 Boundary / 0 concurrency |
| F2 — `StripePayment::refundMoney` (nhánh `ch_`) | Function | Indirect | TC001 | 1 | **RISK** — Normal only, không có case Stripe trả lỗi |
| F3 — `StripePayment::refundMoneyPaymentIntent` (nhánh `pi_`) | Function | Indirect | TC002 | 1 | **RISK** — Normal only, không có case Stripe trả lỗi |
| D1 — `b_user_booking.strip_charge_id` (READ — quyết định nhánh refund) | Data | — | TC001 (`ch_`), TC002 (`pi_`) | 2 | **RISK** — chỉ 2 giá trị "đẹp"; **không có boundary**: NULL / rỗng / prefix khác (`py_`…) — đúng chỗ nhánh `else` của fix |
| D2 — `b_user_booking.status_payment` / `refund_date` / `reason_refund` (UPDATE) | Data | — | TC001–TC005 (chỉ check `status_payment=2`) | 5 | **RISK** — không TC nào verify `refund_date` / `reason_refund`; không có TC kiểm `WHERE` scope trên 2 tài khoản/2 booking |
| T1 — Event Booking (FA-021) — thao tác refund ở màn quản lý booking | Feature | `<Dev không ghi risk>` | TC001–TC005 | 5 | **RISK** — happy path đủ, nhưng không có regression ở trạng thái lỗi/biên; chưa có TC production (RULE-08) |

### ORPHAN TCs

Không có TC lạc chủ đề.

| TC ID | Title | Nhận xét | Hành động đề xuất |
|---|---|---|---|
| TC004, TC005 | Refund UnivaPay (+ option chỉ refund LME) | Dev ghi rõ "không đụng nhánh UnivaPay" → **không phải TC verify fix**, nhưng nằm trong cùng function `refundMoneyBookingEvent` bị sửa | **Giữ** — re-label `Type = Regression` (không tính vào RULE-01 của quan điểm Cao) |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Specific code check** — phân nhánh theo tiền tố: `if strip_charge_id bắt đầu 'ch' → refundMoney (charge)` **else** `→ refundMoneyPaymentIntent (payment_intent)`. Kèm yếu tố **Validation** (kiểm tiền tố) và **COMPAT nhánh cũ/mới**. |
| **Trigger space cần cover** | Giá trị của `strip_charge_id`: (1) `ch_…` charge cũ · (2) `pi_…` PaymentIntent mới · (3) **NULL / chuỗi rỗng** · (4) **prefix khác** (Stripe còn sinh charge id `py_…` cho non-card; id legacy/import) · (5) id hợp lệ nhưng **charge đã refund** · (6) id thuộc **tài khoản Stripe khác**. Kèm error scenario của gateway (§3 phụ lục `checklist-lme.md`): already_refunded / amount / network timeout-5xx / **unknown code**. |
| **Số trigger TCs hiện cover** | **2 / 6** (chỉ `ch_` và `pi_`) · error scenario: **0 / 4** |
| **KH report dạng** | **Symptom-only** — file 01 chỉ ghi `GUI hiển thị lỗi "refund fail"`, **không có** error code / message gốc từ Stripe. |
| **Alternative root causes cần verify** | Cùng symptom "refund fail" có thể đến từ: charge **đã bị refund** trước đó · số tiền refund > available balance · charge chưa capture · API key / account Stripe sai · network timeout. Dev mới confirm **1** root cause (prefix `pi_`). ⇒ Cần hỏi Dev: log lỗi Stripe gốc của ticket là gì? |
| **Anti-patterns dính** | **AP-2** (symptom-only KH report) · **AP-3** (happy-path-only regression: T1 chỉ có TC precondition sạch) · **AP-4** (mục "Commit / Pull Request" **trống** → không verify được `startsWith('ch')` là 2 ký tự hay `'ch_'` 3 ký tự, và không thấy code xử lý khi id rỗng) |

> **Câu hỏi adversarial chưa được TCs trả lời:**
> 1. Dev **chỉ kiểm DB dev** (5 bản ghi `ch_` + 5 bản ghi `pi_`). Trên **production** cột `strip_charge_id` còn giá trị nào khác không (NULL, rỗng, `py_`, id import từ hệ cũ)? Mọi giá trị đó sau fix đều rơi vào nhánh `else` → gọi `refundMoneyPaymentIntent` → **fail lần nữa, đúng cái bug đang fix**.
> 2. Khi Stripe refund **thất bại thật**, GUI hiện gì và `status_payment` có bị update nhầm sang 2 không? Không có TC nào trả lời — trong khi đây chính là class bug của ticket.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE — GAP-01 (`D1`, `FUNC-004`)**: Nhánh `else` của fix mặc định "không phải `ch` thì là `pi_`" — **Dev tự ghi đây là giả định** nhưng bộ TC không có case nào ngoài `ch_`/`pi_`. Nếu production có `strip_charge_id` **NULL / rỗng / prefix khác** thì refund vẫn fail y như cũ.
  → **Fix**: bổ sung **TC-NEW-01** (id rỗng/NULL) + **TC-NEW-02** (thống kê `SELECT LEFT(strip_charge_id,3), COUNT(*) ... GROUP BY 1` trên **production**, RULE-04 — xác nhận phạm vi trước khi kết luận), và yêu cầu Dev handle tường minh case id rỗng thay vì rơi vào `else`.

- **[BLOCKER] FIX-SHAPE — GAP-02 (`PAY-STATE-001`, `OUT-TRUTH-001`, `SEC-002`)**: **0/5 TC là Abnormal**. Không có TC nào cho refund **thất bại thật** (đã refund rồi / charge chưa capture / Stripe 5xx-timeout / **error code chưa biết**). Bug gốc là "báo lỗi sai" ⇒ sau fix phải chứng minh: (a) lỗi thật → message **đúng nguyên nhân**, business-friendly, **không lộ raw error/payment id**; (b) lỗi thật → **KHÔNG** update `status_payment=2` (không "báo thành công giả").
  → **Fix**: bổ sung **TC-NEW-03 → TC-NEW-05** (dùng test card / mock Stripe sandbox theo §3 phụ lục `checklist-lme.md`).

- **[BLOCKER] `CONC-001` — GAP-03**: Không có TC **double-click nút refund** / thao tác refund cùng 1 booking trên **2 tab**. Đây là nút thực thi hành động **tiền**, Stripe không tự idempotent nếu app không khóa ⇒ rủi ro **refund 2 lần** hoặc ghi lịch sử trùng.
  → **Fix**: bổ sung **TC-NEW-06**, evidence = **số lần refund thực tế đếm từ Stripe dashboard + DB**, không chấp nhận "đã thử, thấy bình thường".

- **[BLOCKER] `REG-SHARED-001` — GAP-04**: Dev **không cung cấp danh sách nơi ảnh hưởng**. Mục 2 nói fix "áp đúng pattern đã dùng ở `SalesManagementV2Controller`" ⇒ pattern `pi_` vs `ch_` là **vấn đề hệ thống**, không riêng event booking. Theo Catalog C `MAP-PAY-01`, LME có **6 luồng bill tiền**: bill bot · item mua 1 lần · item chu kỳ · **salon** · **lesson** · event booking. Cặp **Salon / Lesson / Booking Event** là điểm bug lặp lại đã biết.
  → **Fix**: yêu cầu Dev **grep toàn repo** các nơi gọi `refundMoney(` và trả lời: luồng nào còn refund theo charge mà data đã có `pi_`? Nếu có → là bug riêng cần ticket. Bổ sung **TC-NEW-10** cho các luồng Dev confirm.

### 4.2 Major (nên fix)

- **[MAJOR] Verify auto-fill chưa tick (file 01 + 03)**: cả hai file đều `Auto-filled: 2026-07-13 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. F/D/T trong report này suy từ journal AI Auto-fixbug, chưa có người xác nhận ⇒ **review chỉ có giá trị sau khi tester tick**.
- **[MAJOR] SYMPTOM-ONLY (AP-2)**: KH/reporter chỉ ghi `GUI hiển thị lỗi "refund fail"` — không có error code Stripe. Dev tái hiện **1** root cause. Hỏi Dev: **log Stripe gốc của ticket** là error code nào? TCs cần cover **≥ 2 plausible root causes** (xem §3.5).
- **[MAJOR] RULE-08 / `ENV-003` (`ENV-PAY`)**: đây là task **bill tiền** — Catalog D ghi rõ **không được kết luận từ staging** (staging dùng account Stripe test, production account thật). Cả 5 TC không ghi env production.
  → Bổ sung **TC-NEW-09**: smoke refund `pi_` trên **production** + **đối soát bản ghi dashboard Stripe thật**.
- **[MAJOR] RULE-01 (`PAY-STATE-001` — ưu tiên Cao)**: chỉ có Normal, thiếu **Abnormal + Boundary**, **không ghi lý do**.
- **[MAJOR] `DATA-DB-001` — thiếu kiểm `WHERE` scope**: task có UPDATE (`status_payment`, `refund_date`, `reason_refund`) nhưng không có TC tạo **2 booking trùng ở 2 tài khoản/2 bot** rồi refund 1 bên và query DB xác nhận bên kia **không đổi**.
  → *Ghi chú severity*: rule gốc xếp mục này **BLOCKER**; hạ xuống MAJOR vì fix **không chạm câu UPDATE** (Dev ghi "logic update DB không đổi") — Leader có thể nâng lại nếu muốn giữ nguyên rule.
- **[MAJOR] `DATA-AUDIT-001`**: TC có check "lịch sử booking hiển thị ở detail friend" (tốt) nhưng (a) chỉ từ **1 nguồn** (web admin) — chưa rà multi action / job; (b) **TC002 — chính là TC verify bug — đang có Actual result "chưa tạo được lịch sử" và Status TRỐNG**. Phải làm rõ: là **chưa test được** hay **lịch sử KHÔNG được ghi** (nếu là (2) thì đây là bug thứ 2, cùng vùng với #38312 lịch sử action của event booking).
- **[MAJOR] `PAY-AMOUNT-001`**: không TC nào đối chiếu **số tiền refund** (full/partial) giữa số tính tay ↔ bản ghi Stripe ↔ màn admin. Expected mới dừng ở "bill tiền trên stripe đã được refund".
- **[MAJOR] AP-4 — thiếu PR link**: mục "Commit / Pull Request" chỉ có commit hash `64cdcfdce5`, **không có link PR/diff** ⇒ không verify được fix shape thật (`startsWith('ch')` 2 ký tự vs `'ch_'` 3 ký tự; có handle id rỗng không). Yêu cầu Dev cung cấp link diff.
- **[MAJOR] TC thiếu cột `Type` / `Priority` / `Steps`**: Sheet không có 3 cột này ⇒ không đếm được RULE-01 và member/tester khác khó reproduce (TC003–TC005 không có bước thao tác nào). Đề nghị bổ sung tối thiểu `Type` + `Priority`.
- **[MAJOR] `FUNC-001` / RULE-06 — Input thiếu**: không có thông tin refund có **gửi mail / tin LINE thông báo** cho user booking không. Nếu có → Expected phải đi tới output cuối (hộp thư / LINE app thật), không dừng ở màn admin. **Hỏi Dev/PM để chốt.**

### 4.3 Minor (có thể fix sau)

- **[MINOR] RULE-02 — evidence**: cột Output note trống ở TC001, TC003–TC005. Mỗi TC phải ghi loại evidence bắt buộc (VD: "Evidence: screenshot Stripe dashboard bản ghi refund + query DB trước/sau").
- **[MINOR] TC003 mơ hồ**: "refund chọn option chỉ refund LME, không refund trên stripe" **không ghi rõ** booking là `ch_` hay `pi_`. Sau fix, nhánh chọn API khác nhau ⇒ nên tách 2 case (xem TC-NEW-11).
- **[MINOR] TC ID**: Sheet không có cột TC ID, đang định danh bằng số row (296–300). Khó trace khi Sheet thêm/xóa dòng.

### 4.4 Nit (gợi ý)

- **[NIT] Branch chưa chốt**: Dev ghi fix nằm trên `ai_small_38690` (độc lập) nhưng ticket có parent #26684; nếu #26684 đang mở có branch `ai_small_26684` thì commit phải chuyển sang đó. **QA cần confirm branch nào được deploy lên staging trước khi run TC.**
- **[NIT] Verify của Dev mới ở mức `lint`** (`php -l`) — không có unit test / integration test cho 2 nhánh refund. Toàn bộ gánh nặng verify đang đổ lên manual QA.
- **[NIT] `INTG-HOOK-001`**: input không có bằng chứng LME có nhận webhook `charge.refunded` từ Stripe hay không ⇒ chưa flag. Nếu có → cần TC webhook trùng/trễ. Hỏi Dev.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Mọi TC đều chạy ở màn **Quản lý booking event** (admin), trừ TC-NEW-09 (production).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Refund booking Stripe có `strip_charge_id` rỗng / NULL — không được rơi vào nhánh PaymentIntent | Booking event có bill Stripe nhưng `b_user_booking.strip_charge_id` = NULL hoặc chuỗi rỗng (VD booking thanh toán fail trước đó, hoặc data import cũ) | 1. Mở màn quản lý booking event → chọn booking đó<br>2. Bấm refund (có tick refund trên Stripe)<br>3. Quan sát GUI + query DB `b_user_booking` | GUI báo lỗi **rõ nguyên nhân** ("booking không có mã thanh toán Stripe hợp lệ"), **KHÔNG** gọi Stripe với id rỗng, **KHÔNG** update `status_payment=2`; không văng exception 500 | High | Boundary | `D1`, `F1`, `FUNC-004` |
| TC-NEW-02 | Xác nhận phạm vi giá trị `strip_charge_id` trên **production** (RULE-04) | Quyền query DB production (read-only) | 1. Chạy `SELECT LEFT(strip_charge_id,3) AS p, COUNT(*) FROM b_user_booking GROUP BY p`<br>2. Đối chiếu với 2 nhánh code (`ch` / else)<br>3. Nếu xuất hiện prefix ngoài `ch_`/`pi_` (VD `py_`) → tạo booking mẫu prefix đó và refund | Chỉ tồn tại 2 prefix `ch_` và `pi_`. Nếu có prefix thứ 3 → **báo Dev ngay**: nhánh `else` sẽ refund fail y như bug cũ | High | Boundary | `D1`, `BUG`, `FUNC-004` |
| TC-NEW-03 | Refund lại booking **đã được refund** (`charge_already_refunded`) | Booking `pi_` đã refund thành công (từ TC002) | 1. Bấm refund lần 2 trên chính booking đó<br>2. Quan sát GUI + DB + Stripe dashboard | GUI báo lỗi đúng nguyên nhân ("giao dịch đã được hoàn tiền"); Stripe **không** phát sinh refund thứ 2; `status_payment` không đổi; lịch sử không ghi trùng | High | Negative | `PAY-STATE-001`, `OUT-TRUTH-001`, `F1` |
| TC-NEW-04 | Refund khi Stripe timeout / trả 5xx | Booking `pi_` chưa refund. Dùng Stripe sandbox mock lỗi hoặc chặn outbound tới `api.stripe.com` giữa lúc bấm refund | 1. Bấm refund<br>2. Chờ response<br>3. Query DB + kiểm Stripe dashboard | GUI hiện lỗi (timeout/kết nối), **KHÔNG** báo success giả, `status_payment` **KHÔNG** = 2; không có refund treo bên Stripe. Có UX recovery (thử lại được) | High | Negative | `PAY-STATE-001`, `OUT-TRUTH-001`, `INTG-*` |
| TC-NEW-05 | Refund gặp **error code chưa handle** → fallback message + không lộ raw error | Mock Stripe trả error code lạ (VD `account_suspended`) | 1. Bấm refund<br>2. Đọc message trên GUI<br>3. Mở DevTools console + response API | Hiện **message business-friendly chung**, không phải raw Stripe error; **không lộ** payment id / API key / stack trace (`SEC-002`); không silent fail | High | Negative | `PAY-STATE-001`, `SEC-002` |
| TC-NEW-06 | Double-click / 2 tab cùng refund 1 booking — chỉ được xử lý 1 lần | Booking `pi_` chưa refund, mở màn quản lý booking trên 2 tab | 1. Tab 1 + Tab 2 cùng bấm refund gần như đồng thời (và test riêng: double-click nhanh 1 nút)<br>2. Đếm số bản ghi refund trên Stripe dashboard<br>3. Query DB `b_user_booking` + bảng lịch sử | Stripe chỉ có **1** refund; DB `status_payment=2` 1 lần, `refund_date` 1 giá trị; lần thứ 2 bị chặn/báo xung đột. **Evidence: số lần refund thực tế đếm từ Stripe + DB** | High | Boundary | `CONC-001`, `F1`, `D2` |
| TC-NEW-07 | `WHERE` scope — refund booking ở tài khoản A không đụng booking trùng ở tài khoản B | 2 bot/2 tài khoản, mỗi bên 1 booking event trùng tên + trùng ngày, đều có bill Stripe `pi_` | 1. Query DB ghi lại `status_payment` cả 2 booking<br>2. Refund booking của tài khoản A<br>3. Query lại DB cả 2 booking | Chỉ booking A đổi `status_payment=2` + `refund_date` + `reason_refund`; booking B **không đổi** field nào. **Evidence: ảnh query trước/sau kèm câu query** | High | Boundary | `DATA-DB-001`, `D2` |
| TC-NEW-08 | Số tiền refund đúng — đối chiếu Stripe ↔ màn admin ↔ tính tay | Booking `pi_` có số tiền cụ thể (VD 5.500 JPY, có thuế) | 1. Ghi lại số tiền booking trên màn admin<br>2. Refund<br>3. Mở Stripe dashboard xem số tiền refund thực tế<br>4. Query DB `refund_date`, `reason_refund` | Số tiền refund trên Stripe = số tiền booking (khớp phép tính tay); `refund_date` đúng thời điểm thao tác, `reason_refund` lưu đúng lý do đã nhập | High | Positive | `PAY-AMOUNT-001`, `D2` |
| TC-NEW-09 | Smoke refund `pi_` trên **PRODUCTION** + đối soát Stripe thật (RULE-08) | Booking thật/booking test trên production có bill Stripe `pi_`, đã hẹn trước với PM | 1. Refund trên `step.lme.jp`<br>2. Đối soát bản ghi trên dashboard Stripe **account thật**<br>3. Query DB production | Refund success; bản ghi Stripe production khớp số tiền + trạng thái; `status_payment=2`. **Evidence bắt buộc: screenshot Stripe production** (Catalog D — `ENV-PAY`: bill tiền không kết luận từ staging) | High | Positive | `ENV-003`, `T1`, `BUG` |
| TC-NEW-10 | Regression — luồng refund Stripe của **salon / lesson / item** với booking `pi_` | Dev đã cung cấp danh sách nơi gọi `refundMoney(`. Chuẩn bị bill `pi_` ở từng luồng Dev confirm | 1. Với mỗi luồng: thực hiện refund Stripe<br>2. Quan sát GUI + Stripe dashboard | Refund success ở mọi luồng. **Nếu luồng nào báo "refund fail" với `pi_` ⇒ cùng bug #38690, mở ticket riêng ngay** | High | Regression | `REG-SHARED-001`, `MAP-PAY-01` |
| TC-NEW-11 | Refund option "chỉ refund LME, không refund gateway" với booking **`pi_`** (bổ sung nhánh mới cho TC003) | Booking event có bill Stripe `pi_` | 1. Bấm refund, chọn option chỉ refund LME<br>2. Query DB + kiểm Stripe dashboard | `status_payment=2`, lịch sử ghi đúng; Stripe **KHÔNG** phát sinh refund; không gọi `refundMoneyPaymentIntent` | Medium | Positive | `F1`, `D2`, `T1` |
| TC-NEW-12 | Lịch sử booking sau refund — đủ 4 thông tin, cho **cả `ch_` và `pi_`** | Booking `ch_` và booking `pi_` đều vừa refund | 1. Mở detail friend → tab lịch sử booking<br>2. Đối chiếu bản ghi lịch sử với thao tác vừa làm | Mỗi refund sinh **đúng 1** bản ghi lịch sử, đủ: người thực hiện / thời gian / hành động (refund, không phải "thêm mới") / giá trị cũ→mới. **Làm rõ Actual "chưa tạo được lịch sử" của TC002** | High | Positive | `DATA-AUDIT-001`, `D2`, `T1` |

---

## 6. Spec update needed

- [x] **Không cần update spec** — fix là sửa lỗi implementation, không đổi behavior đặc tả (refund vẫn phải success như spec Event Booking / FA-021).
- Tuy nhiên **cần Dev/PM chốt 2 điểm chưa có trong input** (không phải spec change, là **input thiếu**):
  1. Refund có gửi **mail / tin LINE** thông báo cho user booking không? (quyết định RULE-06)
  2. LME có nhận **webhook `charge.refunded`** từ Stripe không? (quyết định `INTG-HOOK-001`)

---

## 7. Checklist đã chạy

- [x] A. Coverage — **fail** (A.1 RISK · A.2/A.3 thiếu negative+boundary · A.6 fix-shape fail)
- [x] B. Chất lượng từng TC — **fail** (B.1: TC003–TC005 không có Steps; Expected TC001/TC002 gộp 3 mục đích ⇒ B.2 atomic fail)
- [x] C. Chất lượng bộ TC — **fail** (tỷ lệ Positive 100% / Negative 0% / Boundary 0%)
- [x] D. Spec alignment — pass (không mâu thuẫn spec)
- [x] E. Hành chính — **fail** (thiếu TC ID, Type, Priority; checkbox verify auto-fill chưa tick ở file 01 + 03)
- [x] F. Base quan điểm test LME
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — đã mở **C.7 Bill tiền** (`MAP-PAY-01/02`) + **Catalog D** (`ENV-PAY`, `ENV-HOOK`) + **§3 phụ lục error scenarios payment gateway**
  - [x] F.3 RULE — RULE-01 ✗ · RULE-02 ✗ · RULE-04 ✗ (chưa xác nhận phạm vi trên production) · RULE-05 (chưa có bằng chứng tra spec Stripe mới nhất) · RULE-07 △ (có DB nhưng thiếu WHERE scope) · RULE-08 ✗ · RULE-09 ✓

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `COMPAT-LEGACY-001` | Cao | ◯ — data có 2 đời (`ch_` cũ / `pi_` mới) | TC001 + TC002 | **OK** ✓ *(điểm mạnh nhất của bộ TC)* |
| `FUNC-001` | Cao | ◯ — luồng chính refund | TC001–TC005 | **RISK** — chưa rõ output cuối chuỗi (mail/LINE) |
| `PAY-STATE-001` | Cao | ◯ — giao dịch tiền, đổi trạng thái thanh toán | TC001–TC005 (Normal) | **RISK → BLOCKER** — 0 Abnormal (§3 phụ lục: 0/4 error type) |
| `OUT-TRUTH-001` | Cao | ◯ — thao tác có thông báo kết quả; bug gốc là **báo lỗi sai** | — | **GAP → BLOCKER** |
| `CONC-001` | Cao | ◯ — nút thực thi hành động tiền | — | **GAP → BLOCKER** |
| `REG-SHARED-001` | Cao | ◯ — bug pattern `pi_` có thể tồn tại ở luồng refund khác | — | **GAP → BLOCKER** |
| `DATA-DB-001` | Cao | ◯ — có UPDATE (`status_payment`, `refund_date`) | TC001–TC005 (chỉ `status_payment`) | **RISK → MAJOR** (thiếu `WHERE` scope 2 tài khoản) |
| `DATA-AUDIT-001` | Cao | ◯ — đổi trạng thái thanh toán | TC001, TC003–TC005 (lịch sử ở detail friend) | **RISK → MAJOR** (1 nguồn; TC002 chưa có kết quả) |
| `PAY-AMOUNT-001` | Cao | ◯ — refund có số tiền | — | **GAP → MAJOR** |
| `ENV-003` (RULE-08) | Cao | ◯ — **bill tiền** (Catalog D `ENV-PAY`) | — | **GAP → MAJOR** (không TC nào trên production) |
| `FUNC-004` | Cao | ◯ — biên của `strip_charge_id` (rỗng/prefix lạ) | — | **GAP → BLOCKER** (gộp vào GAP-01) |
| `SEC-002` | Cao | ◯ — xử lý payment, có màn lỗi | — | **GAP → MAJOR** (gộp vào TC-NEW-05) |
| `PAY-ABANDON-001` | Cao | ◯ — đóng tab giữa lúc refund | — | **GAP → MAJOR** *(gợi ý: gộp vào TC-NEW-04, verify không để refund treo)* |
| `INTG-HOOK-001` | Cao | **?** — chưa có bằng chứng LME nhận webhook `charge.refunded` | — | **Chưa kết luận** — hỏi Dev (§6) |
| `PERM-001` / `PERM-002` | Cao | × — fix không chạm route/phân quyền refund | — | × (lý do: mục 4.1 chỉ 1 file controller, không đổi middleware/route — RULE-03 đã ghi lý do) |
| `MSG-*` / `LIFF-ENTRY-001` / `MEDIA-*` / `FRIEND-001` | Cao | × — fix không gửi tin, không sinh link LINE user, không chạm media/friend info | — | × (lý do như trên) |
| `DEPLOY-ASSET-001` | Cao | × — fix chỉ đụng PHP controller, **không** sửa JS/CSS/font | — | × (nếu release kèm build asset khác → Leader bật lại) |
| `PERF-LARGE-001` | TB | × — refund là thao tác đơn lẻ, không xử lý lô | — | × |

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
