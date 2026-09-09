# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37606 — [Info friend] Click trường thông tin bạn bè 「予約済みのプラン」 báo lỗi` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<member điền>` (TCs fetch từ Sheet "test fix bug" rows 229–243) |
| Ngày review | `2026-06-16` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng — không có `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR, cần fix và review lại.

**Lý do ngắn gọn**: Bộ TCs **bao phủ tốt** root cause + nhánh cascade xóa tag + concurrency + restore. Nhưng (1) input `01`/`03` auto-fill từ Redmine **chưa được tester verify** → review chỉ là provisional; (2) guard F1 được Dev tuyên bố "chặn crash cho **mọi đường cascade**" nhưng TCs chỉ tạo orphan qua **đúng 1 đường (xóa tag)**; (3) chưa verify orphan reference thực sự bị **dọn sạch** ở D1/D2 + các surface hiển thị khác (CL17 / C.3); (4) vài expected trống.

---

## 2. Tóm tắt cho member

Bộ TCs làm tốt phần khó nhất: cover đủ các biến thể orphan action (xóa đầu/giữa/cuối/nhiều/hết), có cả case không-orphan, friend-info-không-action, **concurrency 2 user** (TC011) và **restore tag** (TC010) — đây là những chiều dễ bỏ sót. Cần bổ sung 3 điểm: (a) làm rõ **orphan được tạo bằng cách nào** trong TC001–007 và thêm 1 TC orphan sinh từ **đường cascade khác xóa tag** (vì đây mới đúng tình huống KH gặp trên production); (b) verify **đã dọn sạch** action mồ côi (quan sát qua UI: không còn ở detail + modal action + modal filter), không chỉ "màn không báo lỗi"; (c) fill expected cho TC012–014. Trước khi review có giá trị, tester đọc lại Redmine #37606 + screenshot rồi tick 2 checkbox "Tester verify auto-fill" ở file 01 và 03.

---

## 3. Coverage Matrix

> Suy luận mapping từ Title/Steps/Expected (file 04 không có cột Map to Impact).

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — orphan `action_id` → đọc property trên `null` → crash màn friend info | Fix | — | TC001, TC002, TC003, TC004, TC005, TC006, TC007 | 7 | **OK** |
| **F1** — `initDataInfo` (guard `if(!empty($action))`) | Function | Direct | TC001–007, TC011, TC014 | 9 | **RISK** — chỉ test orphan tạo từ đường xóa tag; chưa test orphan từ nguồn khác (claim "mọi đường cascade") |
| **F2** — `deletedDataTag` (dọn orphan khi xóa tag) | Function | Direct | TC008, TC009, TC010 | 3 | **OK** |
| **F3** — `cleanOrphanFriendInfoActionRef` (helper dọn orphan) | Function | Direct | TC008, TC009, TC010 | 3 | **RISK** — verify qua UI "không lỗi"; chưa verify reference thực sự bị xóa |
| **D1** — `friend_info_option_selects.action_id` (set null) | Data | — | TC008 (gián tiếp) | 1 | **RISK** — chưa verify trạng thái data sau xóa tag |
| **D2** — `friend_information_setting.setting_value` JSON (xóa action_id mồ côi) | Data | — | TC001, TC008 (gián tiếp) | 2 | **RISK** — "không hiển thị action_id ở detail" gợi ý đã dọn, nhưng chưa cover các surface khác |
| **T1** — QL thông tin bạn bè (mở/sửa trường Lựa chọn có action) | Feature | High | TC001–007, TC011, TC012, TC013, TC014 | 12 | **OK** (regression date/point + staff có cover) |
| **T2** — QL tag (xóa tag dọn thêm orphan friend info) | Feature | Medium | TC008, TC009, TC010 | 3 | **OK** |

### ORPHAN TCs

| TC ID | Title | Lý do | Hành động đề xuất |
|---|---|---|---|
| TC012 | friend info **date** | KHÔNG orphan — là regression cho field type khác (date có thể gắn action). Hợp lệ. | **Giữ** — nhưng fill expected (đang trống). |
| TC013 | friend info **point** | Tương tự TC012. | **Giữ** — fill expected. |

→ Không có TC lạc chủ đề thực sự. TC012/013 là regression cho các field type khác cùng pattern → hợp lệ, chỉ thiếu expected.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **2 tầng**: (1) **Add-check / null-guard** tại `initDataInfo` (`if(!empty($action))`); (2) **Soft-delete / orphan-cleanup** tại `deletedDataTag` + helper. KHÔNG phải generic catch-all error handler. |
| Trigger space cần cover | Trạng thái orphan của trường select: orphan 1 action (đầu/giữa/cuối), orphan nhiều, orphan hết, không orphan, không có action. **+ Nguồn sinh orphan**: xóa tag (đã cover) vs **cascade khác** (xóa scenario/richmenu/template — Dev ghi rõ "guard chặn crash cho mọi đường") + **orphan có sẵn trên production** (case KH thực tế). |
| Số trigger TCs hiện cover | Trạng thái orphan: **6/6 OK** (TC001–007). Nguồn sinh orphan: **1/≥2** — chỉ đường xóa tag. |
| KH report dạng | **Symptom-only** ("xuất hiện lỗi", KH không nêu error code). Dev **match được** error message `Trying to get property 'details' of non-object` + truy vết code + tiền lệ guard ConversionController/QRCodeController → root cause **đủ tin cậy**, nhưng Dev **không tái hiện trực tiếp** (Dev DB không có data bot ULUM). |
| Alternative root causes cần verify | initDataInfo có thể còn **null-read khác** nếu cấu hình trường select hỏng kiểu khác (vd tham chiếu tag/filter dangling trong option) → cùng symptom "click → lỗi". Hỏi Dev xác nhận. |
| Anti-patterns dính | **AP-2** (symptom-only, mức nhẹ — Dev có error message thật), **AP-4** (mục Commit/PR chỉ có branch+commit, không có PR diff link — mức nhẹ, reviewer checkout `ai_fixbug_37606` verify được). KHÔNG dính AP-1 (không phải generic-catch single-trigger). |

> Fix KHÔNG phải generic-catch → không trigger BLOCKER fix-shape. Gap chính: **nguồn sinh orphan chỉ test 1 đường** → RISK trên F1, nâng thành MAJOR vì F1 là tầng chặn crash cho đúng case KH production.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- _Không có BLOCKER._ Root cause được cover trực tiếp (TC001–007), fix không phải generic-catch nên không có gap trigger-space kiểu AP-1.

### 4.2 Major (nên fix → trigger REJECTED)

- **[MAJOR] AUTO-FILL chưa verify — `01-bug-task.md`**: file auto-filled `2026-06-16 by /new-task`, checkbox "Tester verify auto-fill chính xác" **chưa tick**. Review chỉ provisional. → Tester đọc lại Redmine #37606 (description + screenshot attachment 26863) xác nhận steps/actual đúng rồi tick checkbox.
- **[MAJOR] AUTO-FILL chưa verify — `03-dev-impact.md`**: tương tự, checkbox chưa tick → mapping F1/F2/F3/D1/D2/T1/T2 chưa được tester xác nhận đầy đủ. → Tick sau khi đọc lại journal AI AUTO-FIXBUG.
- **[MAJOR] FIX-SHAPE (nguồn orphan)**: TC001–007 không nói rõ **orphan `action_id` được tạo bằng cách nào**; toàn bộ nhánh "xóa action" (TC008–010) chỉ tạo orphan qua **xóa tag**. Dev tuyên bố guard F1 "chặn crash cho **mọi đường cascade**" + case KH là **orphan có sẵn từ nguồn không rõ trên production**. → (a) Làm rõ precondition TC001–007 (orphan tạo thế nào); (b) thêm TC-NEW-01 tạo orphan từ **đường cascade khác xóa tag** (xóa scenario/richmenu/template làm Action bị xóa) hoặc inject orphan trực tiếp giống production.
- **[MAJOR] DATA dọn orphan chưa verify (D1/D2 + CL17)**: TC008–010 chỉ verify UI "màn không báo lỗi, hiển thị detail". Chưa verify action mồ côi **thực sự bị dọn** ở `friend_info_option_selects.action_id` (set null) + `friend_information_setting.setting_value` JSON. CL17 yêu cầu check **màn list / detail / preview action không lỗi** sau khi xóa hết action. → Bổ sung TC-NEW-02 quan sát qua UI: action mồ côi không còn xuất hiện ở **detail + modal action + modal filter** của trường đó (không chỉ màn detail friend info).
- **[MAJOR] SYMPTOM-ONLY (AP-2)**: KH chỉ báo "xuất hiện lỗi". Dù Dev match được 1 error message, `initDataInfo` có thể còn null-read khác nếu cấu hình trường select hỏng kiểu khác (tham chiếu tag/filter dangling) → cùng symptom. → Hỏi Dev có alternative root cause / null-read khác trong initDataInfo không; nếu có → thêm TC-NEW-03.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC012 / TC013 (friend info date / point)**: expected **trống** trong sheet gốc → member fill expected đo lường được (vd: "trường date/point có action mồ côi → màn không báo lỗi, hiển thị detail, action mồ côi không hiển thị").
- **[MINOR] TC014 (account staff)**: expected trống → fill theo CL1: "staff được phân quyền → mở detail không lỗi giống account chính; staff KHÔNG quyền → bị từ chối access".
- **[MINOR] Cột Type / Priority / Precondition trống toàn bộ TC**: member điền Type (Positive/Negative/Boundary/Regression) + Priority để Leader đánh giá phân bổ chiều (hiện không thấy nhãn Negative/Boundary rõ ràng).
- **[MINOR] AP-4 — Commit/PR**: mục "Commit / Pull Request" chỉ có branch `ai_fixbug_37606` + commit `7c5ed6562a`, không có PR diff link. Reviewer checkout branch verify được fix shape thực tế → không block, nhưng nên đính link diff.

### 4.4 Nit (gợi ý)

- **[NIT] Compatibility / App**: friend info còn hiển thị ở **My page app mobile** (C.3 — Admin app). Trường select có action mồ côi mở ở app có crash không? Cân nhắc 1 smoke test nếu app dùng chung API.
- **[NIT] Title TC dài**: giữ keyword nhưng có thể rút gọn phần lặp "Check mở trường Lựa chọn 「予約済みのプラン」".

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Guard chặn crash với orphan sinh từ đường cascade **khác xóa tag** | Trường friend info Lựa chọn gắn 1 action; action này bị xóa do xóa **scenario/richmenu/template** chứa nó (KHÔNG qua xóa tag) — hoặc inject `action_id` mồ côi trực tiếp giống data production | 1. Gắn action vào option của trường select<br>2. Xóa nguồn cascade khác (scenario/richmenu/template) làm action bị xóa<br>3. Mở detail trường friend info đó | - Màn **không báo lỗi**, hiển thị detail<br>- Action mồ côi **không hiển thị**<br>- Các action còn tồn tại hiển thị bình thường | High | Boundary / Regression | BUG, F1 |
| TC-NEW-02 | Verify orphan reference **đã được dọn** ở các surface hiển thị (CL17) | Trường select có action gắn, trường này xuất hiện ở **modal multi-action** + **modal filter** | 1. Xóa tag → action bị xóa theo<br>2. Mở **modal action** và **modal filter** có chứa trường này<br>3. Mở lại **detail** trường friend info | - Cả 3 nơi **không lỗi**<br>- Action mồ côi **không còn xuất hiện** ở modal action / filter / detail<br>- (nếu có quyền DB) `friend_info_option_selects.action_id`=null + `setting_value` JSON không còn action_id mồ côi | High | Regression | D1, D2, F3, T1, CL17 |
| TC-NEW-03 | initDataInfo với **dangling reference type khác** (alternative root cause) | (Sau khi Dev confirm) Trường select có 1 tham chiếu khác bị dangling — vd tag/filter trong option đã bị xóa | 1. Tạo trạng thái dangling reference khác action_id<br>2. Mở detail trường friend info | - Màn **không crash / không alert** ngay khi vào | Medium | Negative | BUG, F1 |
| TC-NEW-04 | Regression CL17 — màn **list** friend info sau khi xóa hết action | Trường select đã xóa hết action gắn | 1. Mở `/basic/friend-information` (list)<br>2. Mở `/basic/friend-information/item/{id}` | - Cả 2 màn **không lỗi**, hiển thị bình thường | Medium | Regression | T1, CL17 |

---

## 6. Spec update needed

- [x] Không cần update spec — đây là bug fix (null-guard + orphan cleanup), không đổi business rule. Behavior sau fix: trường select có action mồ côi → hiển thị bình thường, bỏ qua action mồ côi.
- [ ] Cần update spec

> Lưu ý yokoten (Dev ghi): orphan có thể sinh từ các đường cascade khác (scenario/richmenu/template) — guard đọc đã chặn crash, nhưng vá gốc các đường đó là **ticket riêng**. Leader cân nhắc tạo ticket yokoten.

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG OK; A.2 F1 RISK (nguồn orphan), F2/F3 OK; A.3 D1/D2 RISK (chưa verify data dọn); A.4 T1/T2 OK; A.5 không có orphan thật; A.6 fix-shape đã chạy (§3.5)
- [x] B. Chất lượng từng TC — Title có keyword tốt; expected TC012–014 trống (MINOR); Type/Priority trống (MINOR)
- [x] C. Chất lượng bộ TC — có concurrency (TC011) + restore (TC010); thiếu nhãn Negative/Boundary rõ ràng
- [x] D. Spec alignment — không mâu thuẫn spec
- [x] E. Hành chính — TC fetch từ Sheet, tester chưa ký (file 04 placeholder)
- [x] F. Base checklist LME:
  - [x] **F.1 Checklist web** — **CL17** (setting action xóa): partial — verify GUI detail OK, thiếu list/modal + DB (xem TC-NEW-02/04). **CL1** (staff): TC014 OK. **CL2** (reload không lỗi): implied, nên thêm bước reload. **CL10** (update/delete impact): TC008–010 OK. A.2 Security: N/A (không có URL mới). Compatibility Win/Mac: chưa đề cập (NIT).
  - [x] **F.2 Checklist job** — N/A (fix ở controller web + tag delete, không chạm job sync Google).
  - [x] **F.3 Các tính năng chung** — **C.3 Friend info**: chỉ cover màn friend-information detail; thiếu các surface khác (modal action/filter, chat right bar, my page, app — xem TC-NEW-02 + NIT app). **C.4 Tag**: xóa tag cover (TC008–010). C.1/C.2/C.5/C.7/C.8: N/A.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
