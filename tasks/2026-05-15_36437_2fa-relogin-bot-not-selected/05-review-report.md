# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #36437 — Khi bật xác thực 2 lớp, logout -> login lại, đang chưa select bot đã chọn trước đó |
| Reviewer (Leader) | `<điền tên Leader>` |
| Tester được review | Ngọc Ánh (báo bug + chỉ định Link TCs Row 132~133, 163~165) |
| Ngày review | 2026-05-15 |
| Version TCs | v1 (fetched từ `[AI]TCs_UI` gid=10976066 rows 132-165) |
| Vòng review | Round 1 |

---

## 1. Verdict

- [ ] APPROVED
- [ ] APPROVED WITH CHANGES
- [x] **REJECTED**

**Lý do ngắn gọn**: Bộ 5 TCs hiện tại **KHÔNG cover bug root cause** (logout/login với 2FA + đã chọn bot trước → show bot đã chọn). Row 132/165 test case "không bật 2 lớp", Row 133 test "bật 2 lớp + chưa chọn bot" với expected TRỐNG, Row 163-164 (upgrade button) lạc chủ đề. Cần bổ sung ≥ 3 TCs mới + verify auto-fill input.

---

## 2. Tóm tắt cho member

Cảm ơn bạn đã chỉ định 5 dòng TCs trong sheet, format Link TCs rõ ràng — `/new-task` đã fetch về thành công. Tuy nhiên bộ TCs hiện tại có **2 điểm nghiêm trọng**: (1) **không có TC nào test đúng scenario của bug** (2FA + đã chọn bot trước → vào admin/home), và (2) **Row 163-164 là TC upgrade button**, không liên quan login/2FA. Cần thêm ≥ 3 TCs mới (xem §5) và Leader cần verify lại với Dev xem F2/F3 có thật bị ảnh hưởng không.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — Logout/login với 2FA + đã chọn bot trước → expect show admin/home bot đã chọn | Fix | — | (không có TC nào khớp scenario này — row 132/165 là "không 2 lớp", row 133 là "2 lớp + chưa chọn bot" expected trống) | **0** | **GAP — BLOCKER** |
| F1 — `authCodeLogin` (AuthController.php) | Function | Direct | Row 132 (login no-2FA, no-bot), Row 133 (login 2FA, no-bot, expected trống), Row 165 (login no-2FA, có-bot) — gián tiếp chạm function login | 3 | **RISK** (thiếu case quan trọng nhất: 2FA + đã chọn bot) |
| F2 — `getPlanLOA` (AuthController.php) | Function | Indirect | (không TC nào đề cập plan LOA) | **0** | **GAP** |
| F3 — `initDeliveryModalState` (AuthController.php) | Function | Indirect | (không TC nào đề cập delivery modal init) | **0** | **GAP** |
| D — (không có data update) | Data | — | N/A | N/A | OK |
| T1 — Login (đặc biệt: 2FA + đã chọn bot trước đó) | Feature | High | Row 132/133/165 chạm login nhưng KHÔNG có happy path end-to-end của "2FA + đã chọn bot" | **0** (cho scenario chính) | **GAP — BLOCKER** |

### ORPHAN TCs

| TC ID | Title (tóm tắt) | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| Row 163 | BTN アップグレード + gói Pro → tooltip "không upgrade được" | Test upgrade button, không liên quan login/2FA | **Remove khỏi scope review #36437** — chuyển sang task khác nếu cần regression upgrade button |
| Row 164 | BTN アップグレード + free/standard → upgrade allowed | Test upgrade button, không liên quan login/2FA | **Remove khỏi scope review #36437** |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] GAP-1** (Bug root cause): **Không có TC nào** verify scenario chính của bug #36437 — logout/login với 2FA + đã chọn bot trước đó → expect show admin/home của bot đã chọn (KHÔNG redirect về pre-select-bot list). Row 133 đúng "2 lớp" nhưng test case "chưa chọn bot" + expected để trống; row 165 đúng "đã chọn bot" nhưng "không 2 lớp". Bug fix có thể bỏ lọt → **MUST bổ sung TC-NEW-01** (xem §5).
- **[BLOCKER] GAP-2** (T1 High-risk feature): Không có happy path end-to-end cho "Login với 2FA + đã chọn bot" — đây chính là scenario user-facing High-risk theo dev impact 4.3. **MUST bổ sung TC-NEW-01 hoặc TC-NEW-05**.

### 4.2 Major (nên fix)

- **[MAJOR] Row 133 (Expected trống)**: TC test "2FA + chưa chọn bot" nhưng cột Expected để trống → TC không executable. **Fix**: fill expected (gợi ý: "Hiển thị màn list chưa select bot — admin/pre-select-bot", tương tự row 132).
- **[MAJOR] GAP-3** (F2 getPlanLOA Indirect): Không có regression test cho `getPlanLOA` sau khi sửa redirect. Nếu Dev confirm F2 thực sự bị ảnh hưởng → cần TC. Nếu KHÔNG ảnh hưởng → Dev cần update mục 4.1 trong dev impact để remove F2. **Đề xuất**: bổ sung TC-NEW-03 (regression plan info post-login) + verify với Dev.
- **[MAJOR] GAP-4** (F3 initDeliveryModalState Indirect): Tương tự GAP-3 — không có regression test cho delivery modal init. Cần TC-NEW-03 hoặc Dev xác nhận remove F3 khỏi 4.1.
- **[MAJOR] File 01 chưa được tester verify**: `01-bug-task.md` có field `Auto-filled: 2026-05-15 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick. **Yêu cầu** tester đọc lại Redmine #36437 (đặc biệt journal note + screenshot attachment) và tick checkbox trước khi review có giá trị.
- **[MAJOR] File 03 chưa được tester verify**: Tương tự — `03-dev-impact.md` auto-fill chưa được verify. F1/F2/F3 mapping (Direct/Indirect) là **AI suy luận**, chưa có Dev confirm. **Yêu cầu** tester verify với Dev `Tuấn Anh Trần`.
- **[MAJOR] ORPHAN Row 163-164** (BTN upgrade): 2 TCs này không liên quan login/2FA — lạc chủ đề review bug #36437. **Đề nghị** Leader/QA confirm có giữ làm regression smoke test hay không. Nếu giữ → cần thêm justification; nếu không → remove khỏi sync target để tránh nhiễu kết quả review.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Sheet `[AI]TCs_UI` dùng cấu trúc phân cấp**: child row inherit Feature/Category từ parent (cell trống không phải nghĩa là TC thiếu — cần đọc context). Khi review tiếp các bug khác từ sheet này, Leader cần lưu ý format này. **Đề xuất**: sheet team nên fill đủ Feature/Category vào mỗi row child để mỗi TC standalone, dễ review độc lập.
- **[MINOR] TC ID dùng `(row N)`**: TCs fetched dùng số dòng làm ID — không phải format TC-XXX-NNN chuẩn. Đây là hệ quả của sheet structure. Khi member viết TC mới (TC-NEW-01..) cho bug này, dùng format chuẩn của team.
- **[MINOR] Module / Môi trường phát hiện trong 01 còn placeholder** (`<chưa rõ — tester fill>`): Redmine không có thông tin này. Tester cần fill bằng cách hỏi báo cáo viên Ngọc Ánh hoặc check screenshot.
- **[MINOR] Section 3 trong 03-dev-impact.md trống** (caller đã check): Redmine chỉ có header, không có nội dung. Verify với Dev xem có thực sự đã check caller nào hay chưa, hay Dev quên fill.

### 4.4 Nit (gợi ý)

- **[NIT]** Có thể thêm TC test "Bật 2FA → chưa logout, lần đầu setup 2FA xong có redirect đúng overview của bot đã chọn không" (verify cách fix `redirect về overview` áp dụng đúng tất cả entry points của authCodeLogin).
- **[NIT]** Nếu có nhiều bot (≥ 2) và admin chọn bot B nhưng quay lại session cũ chọn bot A → check setting "default bot" được lưu ở đâu (session/cookie/DB). Bug có thể tái xuất hiện trong edge case này.

---

## 5. TCs đề xuất bổ sung

> Member copy vào sheet `[AI]TCs_UI` (hoặc tạo block mới) và update `04-tc-list.md`.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | 2FA + đã chọn bot trước → login lại trả về admin/home của bot đã chọn (verify bug fix #36437) | Admin tài khoản A đã chọn bot B làm default + đã bật xác thực 2 lớp + đang logout state | 1. Vào trang login<br>2. Nhập email + password tài khoản A<br>3. Nhập mã xác thực 2 lớp đúng<br>4. Submit | Sau khi login thành công, browser redirect đến URL `/admin/home` (hoặc overview của bot B); KHÔNG redirect đến `/admin/pre-select-bot` hay màn list bot. Header hiển thị tên bot B. | High | Positive (verify fix) | **BUG**, F1, T1 |
| TC-NEW-02 | 2FA + CHƯA chọn bot → login lại vẫn show pre-select-bot list (regression case "no-bot") | Admin tài khoản chưa chọn bot nào (manage 0 bot hoặc chưa pick default) + đã bật xác thực 2 lớp + logout state | 1. Login + nhập mã 2FA đúng | Sau login thành công, redirect đến `/admin/pre-select-bot` (màn list bot để admin chọn). KHÔNG redirect sai đến `/admin/home` rỗng (vì chưa có bot context). | High | Regression / Negative case (đảm bảo fix không break case "chưa chọn bot") | F1, T1 |
| TC-NEW-03 | Sau login 2FA + đã chọn bot: getPlanLOA + delivery modal khởi tạo đúng (regression F2 + F3) | Admin tài khoản A plan Standard, đã chọn bot B, đã bật 2FA, logout state | 1. Login + 2FA<br>2. Vào trang overview của bot B sau khi auto-redirect<br>3. Verify tooltip BTN アップグレード + badge số mess send | - BTN アップグレード hover → tooltip phù hợp với plan Standard ("Cho phép upgrade")<br>- Badge số mess send load đúng (delivery modal state init OK)<br>- Plan LOA banner hiển thị đúng | Medium | Regression | F2, F3, T1 |
| TC-NEW-04 | 2FA + nhập sai mã → vẫn ở màn 2FA, KHÔNG redirect | Admin tài khoản A đã bật 2FA + đã chọn bot B + logout state | 1. Login + password đúng<br>2. Nhập mã 2FA SAI<br>3. Submit | Hiển thị message lỗi 2FA. URL vẫn là trang nhập mã 2FA, KHÔNG redirect tới `/admin/home` hay `/admin/pre-select-bot`. | Medium | Negative | F1 |
| TC-NEW-05 | 2FA + nhiều bot (≥ 2), đã chọn bot B → login lại về đúng bot B (không phải bot A) (boundary) | Admin tài khoản manage 3 bots (A, B, C), default selection = B, đã bật 2FA | 1. Logout<br>2. Login + 2FA | Redirect đến overview của **bot B** (không phải bot A hay C). Header hiển thị "B". | High | Boundary | **BUG**, T1 |

---

## 6. Spec update needed (nếu có)

- [x] **Không cần update spec** — bug là behavior regression (fix redirect logic), không phải đổi spec.
- [ ] Cần update spec

> Tuy nhiên, nếu spec gốc có ghi "Sau login 2FA → redirect về `/admin/pre-select-bot`" (mâu thuẫn với fix mới "redirect về overview của bot đã chọn") → cần check `02-spec-reference.md` (hiện chưa có) hoặc spec gốc của module Login với 2FA. **Đề xuất**: member bổ sung `02-spec-reference.md` trích spec của flow Login + 2FA để xác nhận.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 Bug root cause: **FAIL** (GAP-1). A.2 Function: **PARTIAL** (F1 RISK, F2/F3 GAP). A.3 Data: N/A. A.4 Feature: **FAIL** (T1 GAP). A.5 ORPHAN: phát hiện row 163, 164.
- [x] **B. Chất lượng từng TC** — Row 132/165 OK (rõ ràng), Row 133 **FAIL** (expected trống), Row 163/164 OK nhưng orphan.
- [x] **C. Chất lượng bộ TC tổng thể** — KHÔNG đủ chiều: thiếu Positive cho scenario chính, thiếu Negative (sai mã 2FA), thiếu Boundary (nhiều bot). Tỷ lệ Pos/Neg/Boundary/Regression không phù hợp.
- [x] **D. Spec alignment** — Chưa có `02-spec-reference.md`. Dùng fallback LME-SYSTEM-SPEC.md. Đề xuất member trích spec Login + 2FA vào file 02.
- [x] **E. Hành chính** — TC ID format `(row N)` không chuẩn (do source từ sheet). Folder review đúng cấu trúc. Tester / version / link gốc trong file 04 chưa fill.
- [x] **F. Base checklist LME**:
  - [ ] F.1 Checklist web — **Verify thêm**: CL liên quan login flow (chưa có CL chuyên về login trong checklist-lme.md theo memory; tester confirm). Compatibility: Test login + 2FA trên **Win+Mac** + **Chrome/Firefox/Edge** + **mobile Android/iOS** (nếu admin portal support mobile) — đặc biệt vì bug liên quan redirect cookie/session.
  - [ ] F.2 Checklist job — N/A (không chạm job).
  - [x] F.3 Tính năng chung —
    - **C.7 Plan limits**: F2 = `getPlanLOA` chạm plan info → cần verify plan limits không bị regression (đã đề xuất ở TC-NEW-03).
    - Các C khác (C.1 Bill, C.2 Send message, C.3 Friend info, C.4 Tag, C.5 Google sheet, C.6 Calendar, C.8 Sort) — N/A.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!--
Notes from Claude /review-tc:
- File 02-spec-reference.md không có → fallback tham chiếu templates/LME-SYSTEM-SPEC.md (không có spec riêng cho 2FA login flow trong folder review).
- File 01 + 03 đều có "Auto-filled by /new-task" + checkbox Tester verify CHƯA tick → flag MAJOR.
- TCs fetched từ Redmine Link TCs (source B per /review-tc workflow), không phải /write-tc sinh ra.
- Coverage matrix tự suy luận từ Title/Scenario/Type của sheet, không có cột "Map to Impact".
- BLOCKER chính là GAP cho BUG root cause + T1 High-risk — đây là rủi ro bỏ lọt bug ra production nếu không bổ sung TC.
-->
