# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | KH #36202 |
| Reviewer (Leader) | `<member điền — Test Leader>` |
| Tester được review | `<member điền>` |
| Ngày review | 2026-05-08 |
| Version TCs | v1 (draft AI + verify Dev clarifications) |
| Vòng review | Round 1 |

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [x] **APPROVED WITH CHANGES** — Approve sau khi member bổ sung 4 TC GAP (F3 boundary, T2 link expired, T2 single-use, CL18 load-before-deploy). Không cần full re-review — Leader chỉ verify 4 TC mới ở round 2.
- [ ] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Coverage core của bug + 7 impacts F/T đã đầy đủ; spec reference + Dev clarifications đã được verify. 3 issue MAJOR đều thuộc dạng "thiếu chiều sâu regression" cho 2 impact High risk (F3 FE behavior change, T2 màn accept) — không phải BLOCKER vì root cause đã có TC verify. Member bổ sung 4 TC + tester run xong gửi tóm tắt là đủ.

---

## 2. Tóm tắt cho member

Bộ TCs khá tốt: cover đầy đủ bug root cause (TC001 reproduce E2E), 7 impact (F1-F4 + T1-T2) đều có TC verify, đã verify nhiều câu hỏi với Dev và áp dụng góc nhìn manual tester sau feedback. Có 3 điểm cần bổ sung cho hoàn thiện: **F3 thiếu boundary "tick all bot mix plan"** (chỉ có Pos + Neg validation), **T2 thiếu regression cho link expired (BR-001) và single-use (BR-002)**, và **CL18 thiếu test load-UI-trước-deploy-submit-sau** (case dễ xảy ra khi deploy gặp admin đang mở màn invite). Sau khi thêm 4 TC này → approve final.

---

## 3. Coverage Matrix

> File 04 không có cột Map to Impact — coverage suy luận từ Title/Precondition/Steps/Expected của mỗi TC. Một TC có thể cover nhiều impact (ví dụ TC025 cover F1+F2+T1).

| Impact | Loại | Priority | TCs cover (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause: bot standard mới chưa enforce limit 10) | Fix | — | TC001 | 1 | **OK** |
| F1 — `generateLinkInviteStaff` | Function | Direct | TC002, TC003, TC004, TC005, TC006, TC015, TC016, TC017, TC019, TC023, TC024, TC025 | 12 | **OK** (Pos+Neg+Bound đầy đủ + cover free/pro/legacy/multi-bot) |
| F2 — `acceptInviteStaff` | Function | Direct | TC003, TC007, TC008, TC009, TC022, TC023, TC025 | 7 | **OK** (Pos+Neg+Bound + race + check-at-accept) |
| F3 — `invite_staft.js` (FE only post selected) | Function | Direct | TC010, TC011 | 2 | **RISK** — chỉ Pos + Neg validation, **thiếu Boundary** "tick all" / "tick mix plan" để verify FE đúng hành vi với edge selection |
| F4 — `UserStaffBot` model | Function | Indirect | TC012, TC018 | 2 | **OK** (Regression cho count behavior) |
| T1 — Màn generate invite link admin | Feature | High | TC013, TC015, TC016, TC019, TC020, TC021, TC024, TC025 | 8 | **OK** |
| T2 — Màn accept bot của staff | Feature | High | TC014, TC020 | 2 | **RISK** — T2 là High risk nhưng chỉ có happy path (TC014) + compat (TC020). **Thiếu regression** cho 2 BR quan trọng: BR-001 (24h expired), BR-002 (single-use) |

### ORPHAN TCs (nếu có)

Không có ORPHAN. Tất cả 25 TC đều thuộc scope BUG / F* / T* hoặc 1 mục checklist LME (CL1, CL5, CL10, CL11, C.7).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

Không có.

### 4.2 Major (nên fix — đề nghị bổ sung 4 TC mới ở §5)

- **[MAJOR] GAP-F3-1**: F3 (`invite_staft.js`) là Direct impact thay đổi behavior từ "post all bot" → "post selected". Chỉ có 2 TC (TC010 Pos + TC011 Neg validation client-side). **Thiếu Boundary case** "tick toàn bộ bot mix plan" — risk: FE có thể bug khi user click "全てを選択" với account có > 10 bot. → Đề nghị thêm **TC-NEW-01**.
- **[MAJOR] GAP-T2-1**: T2 (Màn accept staff) là High risk feature. Chỉ có TC014 happy path + TC020 compat. Spec BR-001 nói invite URL hết hạn 24h, BR-002 nói single-use. **Thiếu regression** cho 2 BR này → bug fix có thể vô tình phá luồng error handling. → Đề nghị thêm **TC-NEW-02** (link expired) + **TC-NEW-03** (single-use after accept).
- **[MAJOR] GAP-CL18**: Checklist LME mục CL18 yêu cầu "luôn có case load UI trước, submit sau khi deploy không lock maintain". Bug fix liên quan timing check max staff → đặc biệt quan trọng với CL18: admin mở màn invite TRƯỚC deploy (khi count chưa update logic), submit SAU deploy (logic mới). Hiện không có TC nào cover. → Đề nghị thêm **TC-NEW-04**.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC011**: Test client-side validation OK, nhưng nên thêm 1 case API direct bypass (Postman gọi `/admin/ajax/generate-link-invite-staff` với toàn bộ bot có `selected=false`) → verify BE handle thế nào (trả error rõ hay create empty invite).
- **[MINOR] TC020**: Compatibility test chỉ repeat TC004 (error message). Nên cover thêm full flow (tạo invite + accept) trên ít nhất 1 combo browser/OS để verify UI không gãy ở các browser khác Chrome.
- **[MINOR] TC008 expected**: "per-bot hoặc tổng — TBD theo Dev" — sau Q5 Dev confirm "đúng rồi" nhưng vẫn để dạng tùy chọn. Member nên lock cụ thể (vd "1 message tổng liệt kê các bot bị skip") sau khi run thực tế quan sát UI.

### 4.4 Nit (gợi ý)

- **[NIT] TC013** happy path E2E hiện mix "1 standard mới + 1 pro". Nên thêm 1 happy path mix "1 standard cũ + 1 standard mới" để cover BR-006a vs BR-006b cùng lúc với T1 Reg.
- **[NIT] TC012** precondition vẫn dùng từ DB-perspective ("Đã invite + accept đủ 10 staff"). Có thể đơn giản hơn: "Bot standard có user chính + 10 staff hiển thị trong dashboard (count 10/10)". Steps đã OK.
- **[NIT]** Phân bố Type hơi nặng Boundary (28%) vì task về plan limit có nhiều edge case timing. OK trong context bug này, không cần điều chỉnh.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Title đã encode keyword để Leader/Claude suy luận impact (project đã drop cột Map to Impact).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact (chỉ để Leader review) |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | invite_staft.js boundary: click "全てを選択" với account có 5 bot mix plan → BE nhận đủ 5 bot ID đã active | Admin có 5 bot: 1 free post-2021-07-01 (sẽ bị hide), 1 free legacy, 2 standard cũ, 1 standard mới. Mở DevTools Network. | 1. Vào màn invite-staff.<br>2. Click button "全てを選択／解除" để tick all.<br>3. Inspect số bot hiển thị trong form (free post-2021-07-01 đã hide nên còn 4).<br>4. Submit, inspect Network payload. | Bước 3: chỉ 4 bot hiển thị (free post-2021 hide). Bước 4: request body chứa đúng 4 bot ID đã tick (không thiếu, không thừa, không gửi free post-2021). | Medium | Boundary | F3 |
| TC-NEW-02 | acceptInviteStaff: link đã quá 24h từ khi tạo → fail "有効期限を超えました" (BR-001) | Admin đã tạo invite link cho staff X cách đây > 24h (có thể fake bằng cách update `invite_staffs.created_at` lùi về hoặc test trên env có thể time-travel). | 1. Staff X mở link sau 24h.<br>2. Quan sát màn hiển thị. | Hiển thị message "有効期限を超えました。再度招待をしてもらってください。" Không vào màn accept, không tạo UserStaffBot. Bot count không thay đổi. | High | Negative | T2, F2 |
| TC-NEW-03 | acceptInviteStaff single-use: invite đã accept rồi → người khác mở lại fail "招待されたURLはすでに無効となっています" (BR-002) | Admin tạo invite link L cho staff X. Staff X đã accept thành công. | 1. Staff Y (khác X) mở cùng link L.<br>2. Quan sát màn hiển thị. | Hiển thị message "招待されたURLはすでに無効となっています。" Không cho Staff Y join. Bot count không tăng. | High | Negative | T2, F2 |
| TC-NEW-04 | CL18 — Load UI trước, submit sau (deploy timing): admin mở màn invite trước deploy fix, sau deploy thử submit | Trước deploy fix: admin mở màn invite với bot standard 9/10, để form pending chưa submit. Tab vẫn còn mở. Trong lúc đó deploy bug fix code. | 1. Sau deploy, admin click "Tạo invite link" trên tab cũ (form đã load trước deploy).<br>2. Trong lúc đó từ tab khác, có 1 staff khác accept invite cũ → bot full 10/10.<br>3. Submit form trên tab cũ. | Bước 3: BE check fresh state (10/10) → fail với message "Bot đã đạt giới hạn". KHÔNG tạo invite stale. KHÔNG nhảy lên 11/10 do form load lúc 9/10. (Verify check tại submit time, không cache state lúc load.) | Medium | Boundary | T1, F1 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] Cần update spec — chi tiết:
  - **Section**: [spec-features/admin/staff-management/feature-spec.md](../../spec-features/admin/staff-management/feature-spec.md) §5 Business Rules — BR-006
  - **Nội dung cần update**:
    1. **BR-006 cleanup**: Câu "Giới hạn này áp dụng qua `access_bot` (legacy). Chưa xác nhận có áp dụng cho invite URL flow qua `user_staff_bots` hay không." → cập nhật: "Sau bug fix KH #36202, limit cũng áp dụng cho Invite URL flow qua `user_staff_bots`. Logic check: filter `is_admin=0 AND status=1` (chỉ active). Pending invites không count."
    2. **BR-006b mới**: Thêm rule "Standard contract tạo trước 2023-05-01 đối xử như Pro (unlimited)" vào spec — hiện chỉ có trong file review, chưa có trong feature-spec gốc.
    3. **§9 Open Questions**: Câu hỏi "Giới hạn 10 staff (BR-006) có áp dụng cho invite URL flow không?" → đã được trả lời (có, sau fix), close question.
    4. **§3.4 Status enum**: Bổ sung note "Khi count for limit, chỉ count `status=1` (STATUS_ACCEPT). Pending (status=0) không count." — Dev confirm 2026-05-08.
  - **Người chịu trách nhiệm update**: Dev phụ trách bug fix + spec-compiler agent (next sync).

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — đối chiếu 03-dev-impact (BUG + F1-F4 + T1-T2). 5/7 impact OK; 2/7 RISK (F3, T2) → flag MAJOR §4.2.
- [x] **B. Chất lượng từng TC** — Title rõ ràng (chứa keyword function/feature), Precondition đủ, Steps tuần tự, Expected đo lường được. (TC008 expected hơi mơ hồ → MINOR.)
- [x] **C. Chất lượng bộ TC tổng thể** — 25 TC, không trùng lặp, không orphan. Tỷ lệ Type Pos 7 / Neg 5 / Bound 7 / Reg 6 hợp lý cho task plan-limit.
- [x] **D. Spec alignment** — TCs khớp spec staff-management (xem 02-spec-reference.md). Spec gốc cần update (xem §6).
- [x] **E. Hành chính** — TC ID format chuẩn TC001-TC025. Header file 04 còn placeholder `<member điền>` cho Tester/Ngày — member fill trước submit.
- [x] **F. Base checklist LME**:
  - [x] **F.1 Checklist web**:
    - A.1 Function checklist: CL1 (TC019) ✅ | CL5 (TC016) ✅ | CL10 (TC018) ✅ | CL11 (TC017) ✅ | **CL18 ❌** → MAJOR §4.2 | CL2/3/4 chưa cover (member tự đánh giá có cần không)
    - A.2 Non-function: Regression ✅ | Compatibility (TC020) ✅ | Security URLs N/A
  - [x] **F.2 Checklist job**: N/A (không chạm callback / Google sync)
  - [x] **F.3 Các tính năng chung**:
    - **C.7 Plan limits** (BẮT BUỘC vì task chính là plan limit) ✅ — 5 case: Tạo mới ✅, Copy N/A, Khôi phục soft-delete N/A (Dev confirm), 2 tab ✅, Double click ✅
    - C.7 3 server profile: TC020 cover Win+Mac. Member nên thêm test trên Dev/Production khi run.
    - C.1-C.6, C.8: N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<điền sau khi Leader verify draft AI>` | 2026-05-08 |
| Tester | (đã đọc & hiểu feedback) | `<điền sau khi Tester acknowledge>` |

---

## Phụ lục: Q&A trạng thái với Dev

Tổng kết các câu hỏi đã verify với Dev (xem chi tiết [02-spec-reference.md](02-spec-reference.md) và [04-tc-list.md](04-tc-list.md) header):

| Resolved | Drop / out-of-scope tester | Còn open |
|---|---|---|
| Q1 (10 hard-code), Q2 (chỉ count active), Q5 (TC008 OK), Q6 (no soft-delete), BR-006b (standard cũ = Pro), Bot downgrade, Remove role | Q3 (pro DB field), Q7 (REJECT mechanics), Q8 (audit log), Q9 (cutoff field name) | **Q4** (free legacy có bị limit 10?) — TC021 sẽ verify khi run |

Nếu khi run TC021 phát hiện free legacy bị áp limit → cân nhắc thêm 1 TC ghép limit + free legacy ở vòng 2.
