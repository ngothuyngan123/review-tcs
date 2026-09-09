# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #38263 — [27-06-2026][T11392][Form] Khách báo action khi hiển thị form không hoạt động |
| Reviewer (Leader) | Claude (draft) — Leader verify |
| Tester được review | Ngọc Ánh (TCs nguồn Sheet "Improve 2026.05") |
| Ngày review | 2026-06-27 |
| Version TCs | v1 (fetched từ Sheet) |
| Vòng review | Round 1 |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng (Form Builder / FA-011), không có `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR/BLOCKER, cần fix + review lại

**Lý do ngắn gọn**: Luồng bug cốt lõi (action loại "chỉ lần đầu" khi mở form lần đầu) **có** TC map mechanical, nhưng (1) bộ TC **không** đặt precondition đúng bối cảnh gây regression — **multi-capture** (tính năng 08/05/2026 chính là thủ phạm); (2) có expected result **bỏ ngỏ** ("Text case này đang để là gì?") → không đo được pass/fail; (3) file 01 + 03 auto-fill từ Redmine nhưng **chưa tester verify**; (4) KH report **symptom-only** chưa cover alternative root cause.

---

## 2. Tóm tắt cho member

Bộ TC bám khá sát cấu trúc tính năng action form (1 page / rẽ nhánh × open/trả lời × 1 lần/nhiều lần × lần đầu/lần sau) — đây là điểm tốt, đã cover được behavior "lần đầu send / lần sau không send" của action loại "chỉ lần đầu" chính là chỗ bug. Tuy nhiên rủi ro bỏ lọt nằm ở **bối cảnh tái hiện**: regression do tính năng **multi-capture** gây ra, nên TC verify fix **bắt buộc** chạy trên form đang bật multi-capture (xem §3.5 + TC-NEW-01). Ngoài ra cần dọn các expected còn để dấu hỏi và xác nhận lại 2 file input auto-fill trước khi review có giá trị chính thức.

---

## 3. Coverage Matrix

> File 04 là sheet **phân cấp** (không có TC ID/Type/Priority). Reviewer gán nhãn tham chiếu theo đường dẫn phân cấp để map.

**Nhãn tham chiếu TC** (đường dẫn cột Main Function → … → Case):
- `R1` = 1page › Action open form › check action **1 lần** › **lần đầu** → *Luôn send action chung*
- `R2` = 1page › Action open form › check action **1 lần** › **lần sau** → *Không send action*
- `R3` = 1page › Action open form › check action **nhiều lần** › lần đầu/lần sau
- `R4` = 1page › Action open form › **check multi action** (nội dung send)
- `R5` = 1page › **Action khi trả lời form** › (multi action / text riêng / 1 lần / nhiều lần)
- `R6` = **form rẽ nhánh** › Action open form › (multi/1 lần/nhiều lần)
- `R7` = form rẽ nhánh › Action khi trả lời form › (…)
- `R8` = **Check form không set action**
- `R9` = **Regression**: các action khác của form chạy bình thường

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — action "chỉ lần đầu" phải send khi mở form lần đầu | Fix | — | R1 (+ R6 cho form rẽ nhánh) | 2 | **RISK** — thiếu precondition multi-capture (bối cảnh gây bug) |
| F1 — `userOpenFormanswer` (`FormAnswerController.php`) | Function | Direct | R1, R2, R3, R4, R6, R8 | 6 | **RISK** — chưa cover bối cảnh multi-capture + thiếu friend-block/edge |
| D1 — (không có data thay đổi) | Data | — | N/A (Dev xác nhận không đổi data) | — | OK (không cần TC data) |
| T1 — Form action open lần đầu (loại "chỉ lần đầu"), risk **High** | Feature | High | R1, R2, R6 | 3 | **RISK** — happy path, thiếu edge (multi-capture, friend đã mở trước, friend block) |
| T2 — Form action "mọi lần" (else branch, không đổi), risk Low | Feature | Low | R3, R6(nhiều lần), R9 | 3 | OK (regression else branch) |

### ORPHAN / Over-coverage TCs

| TC ID | Title | Lý do | Hành động đề xuất |
|---|---|---|---|
| R5, R7 | Action **khi trả lời form** (on submit) | Fix chỉ chạm luồng **mở form** (`userOpenFormanswer`); luồng trả lời form không bị chạm code (AP-5 over-coverage) | **Giữ** nhưng re-label là *Regression* (nice-to-have), hạ Priority. KHÔNG tính là cover cho BUG/T1. |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Condition-ordering / state fix** — lưu cờ `isFirstOpenForm` TRƯỚC khi nạp lại record lượt mở, rồi dùng cờ thay vì biến đã bị ghi đè. (Không phải generic catch-all.) |
| Trigger space cần cover | (a) Form **bật multi-capture** + mở **lần đầu** → action "chỉ lần đầu" **phải send**; (b) cùng form + mở **lần sau** → **không** send; (c) action loại "mọi lần" + multi-capture → send mọi lần; (d) form **không** multi-capture (nếu là toggle) → vẫn đúng; (e) friend **đã từng mở** form trước đợt fix → behavior sau fix. |
| Số trigger TCs hiện cover | ~2/5 — R1 (lần đầu send) + R2 (lần sau không send) cover (a)(b) **nhưng KHÔNG khẳng định form đang ở chế độ multi-capture** → không chắc tái hiện đúng bug. (c) cover bởi R3. (d)(e) **chưa cover**. |
| KH report dạng | **Symptom-only** — KH chỉ nói "フォーム表示時アクションが作動しない" (action khi hiển thị form không chạy), không nêu loại action / error / điều kiện. |
| Alternative root causes cần verify | (1) Form của KH có thể là loại "chỉ lần đầu" và friend **đã mở trước đó** → đúng spec là không send (kỳ vọng KH lệch). (2) `action_open_id` null / chưa set action. (3) Action có set nhưng loại "mọi lần" mà KH tưởng là lần đầu. → Hỏi Dev: form T11392 cấu hình action loại nào, friend Rio đã mở form lần nào trước chưa. |
| Anti-patterns dính | **AP-2** (symptom-only KH report), **AP-5** (over-coverage luồng trả lời form — R5/R7), nhẹ **AP-3** (regression happy-path, precondition không có edge state), **AP-4 phần PR link** (mục PR để `<chưa có link PR>`, chỉ có commit hash → khó verify fix shape thực tế bằng diff). |

> Trigger space cover < tổng (đặc biệt thiếu **bối cảnh multi-capture** = chính nguyên nhân regression) → flag **[BLOCKER] FIX-SHAPE** ở §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-1**: Không có TC nào đặt precondition **form đang bật multi-capture** (tính năng 08/05/2026) — đây **chính là** điều kiện gây regression theo mục 1 dev-impact. R1 verify "mở lần đầu → send action" nhưng nếu form test KHÔNG ở chế độ multi-capture thì TC vẫn pass mà **không tái hiện được bug gốc**. → **Bổ sung TC-NEW-01** (form multi-capture + action "chỉ lần đầu" + mở lần đầu → action phải send). Đồng thời **hỏi Dev**: multi-capture là toggle hay luôn bật từ 08/05? Nếu toggle → cần thêm cả case bật/tắt.

### 4.2 Major (nên fix)

- **[MAJOR] SYMPTOM-ONLY / R1**: KH report chỉ mô tả triệu chứng ("action khi hiển thị form không hoạt động"), Dev tái hiện **1 root cause** (multi-capture ghi đè cờ). Cần cover **≥ 2 plausible root cause** cùng tạo symptom này (xem §3.5 alternative root causes) — đặc biệt case "friend **đã mở form trước đó**" (action "chỉ lần đầu" đúng spec là không send — phân biệt bug thật vs kỳ vọng lệch). → **Bổ sung TC-NEW-02**. Hỏi Dev cấu hình thực tế của form T11392.
- **[MAJOR] R2, R5-các-case "lần sau"**: Expected result **bỏ ngỏ** — ghi nguyên văn *"Hiển thị lịch sử send action form ở detail user: Text case này đang để là gì?"*. Đây là **câu hỏi chưa chốt**, tester không xác định được pass/fail. → Member chốt expected: khi mở lần sau (action chỉ lần đầu) thì **lịch sử send action ở detail line user hiển thị gì** (không có bản ghi mới? hay vẫn hiển thị bản ghi lần đầu?). Confirm với spec FA-011.
- **[MAJOR] Auto-fill chưa verify (file 01)**: `01-bug-task.md` có `Auto-filled: 2026-06-27 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. → Tester đọc lại Redmine #38263 (description + 2 screenshot) và tick trước khi review có giá trị.
- **[MAJOR] Auto-fill chưa verify (file 03)**: `03-dev-impact.md` cũng `Auto-filled by /new-task`, checkbox **chưa tick** → F1/T1/T2 mapping có thể chưa đủ. Tester đọc lại journal "AI LME Fix bug" và tick.
- **[MAJOR] C.2 Send message — friend block (GAP-2)**: Action mở form = **send message** tới line user. Chưa có TC case **friend đã block bot** → mở form → action không được send (không lỗi). → Bổ sung (xem TC-NEW-03).

### 4.3 Minor (có thể fix sau)

- **[MINOR] Format TC**: Bộ TC dạng phân cấp Sheet, không có **TC ID / Type / Priority / Precondition / Steps tường minh**. Do nguồn là sheet human của team nên chấp nhận, nhưng đề nghị khi sync chuẩn hóa tối thiểu **Precondition** (loại form, loại action, multi-capture on/off, friend đã/chưa mở) để TC chạy lặp được.
- **[MINOR] AP-5 over-coverage (R5, R7)**: Luồng "Action khi trả lời form" không bị fix chạm — nên re-label *Regression / nice-to-have*, đừng tính là cover cho BUG.
- **[MINOR] CL-Func-1 (staff account)**: Khối #38263 không có case **acc staff** (khối #38226 có). Nếu màn detail line user / lịch sử action có phân quyền staff → bổ sung 1 smoke.

### 4.4 Nit (gợi ý)

- **[NIT] AP-4 / PR link**: Mục "Commit / Pull Request" mới có commit `c782c2a7af`, chưa có link PR → khó verify fix shape bằng diff. Xin Dev link PR để confirm fix là tách cờ (không phải sửa cách khác).
- **[NIT] TC-14 cross-platform**: Action hiển thị ở **chat 1:1 web + app**. Đề nghị verify đối chiếu song song Web ↔ App (R4 mới ghi chung "chat 1:1", chưa tách web/app rõ).
- **[NIT] CL-Func-18**: Cân nhắc 1 case "mở sẵn form phía line user **trước** khi deploy fix → sau deploy mở/submit" (load UI trước, action sau).

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` round tiếp theo. Title chứa keyword để Leader map impact.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Action "chỉ lần đầu" send khi mở form lần đầu — **form BẬT multi-capture** (tái hiện regression #38263) | Form (1 page) có set action open loại "chỉ chạy lần đầu"; **multi-capture đang BẬT**; friend chưa từng mở form này | 1. Friend mở/hiển thị form lần đầu qua link LINE | Action "chỉ lần đầu" **được send** tới line user; lịch sử send action hiển thị ở detail line user; nội dung action đúng | High | Positive / Regression | BUG, F1, T1 |
| TC-NEW-02 | Phân biệt bug vs spec — friend **đã mở form trước đó**, action "chỉ lần đầu" | Form action "chỉ lần đầu", multi-capture bật; friend **đã mở form ≥ 1 lần** trước đó | 1. Friend mở lại form lần 2+ | **KHÔNG** send action (đúng spec "chỉ lần đầu"); xác nhận đây là behavior đúng, không phải bug | High | Boundary | T1, BUG (alt root cause / symptom-only) |
| TC-NEW-03 | Mở form khi friend **đã block bot** — action không send, không lỗi | Friend đã block bot; form có action open "chỉ lần đầu" | 1. (Mô phỏng) friend mở form khi đang block | Action **không** được send (friend block); hệ thống **không** văng lỗi; record lượt mở xử lý bình thường | Medium | Negative | F1, C.2 (send message / friend block) |
| TC-NEW-04 | Multi-capture vẫn ghi nhận đúng lượt mở sau fix | Form bật multi-capture, action "chỉ lần đầu" | 1. Friend mở form nhiều lần liên tiếp | Lượt mở được ghi nhận đầy đủ (multi-capture không bị fix làm hỏng); action "chỉ lần đầu" chỉ send ở lần đầu | Medium | Regression | F1, T2 |
| TC-NEW-05 | Đối chiếu hiển thị action Web ↔ App (chat 1:1) | Action open vừa send cho friend | 1. Mở chat 1:1 trên **Web**; 2. Mở chat 1:1 trên **App** | Nội dung action + lịch sử send hiển thị **giống nhau** ở Web và App | Low | Regression | T1, TC-14 |

---

## 6. Spec update needed

- [x] Không cần update spec (fix khôi phục đúng behavior FA-011 — action "chỉ lần đầu" send khi mở form lần đầu)
- [ ] Cần update spec
  - ⚠️ **Cần chốt 1 điểm spec mơ hồ** (không phải update, mà là làm rõ): khi mở form **lần sau** với action "chỉ lần đầu" — **lịch sử send action ở detail line user hiển thị thế nào?** (liên quan expected bỏ ngỏ ở §4.2). Member confirm với Leader/Dev rồi điền vào expected.

---

## 7. Checklist đã chạy

- [x] A. Coverage (A.1–A.6, gồm fix-shape adversarial §3.5)
- [x] B. Chất lượng từng TC (B.1 Expected bỏ ngỏ — fail; format thiếu Precondition/Type/Priority)
- [x] C. Chất lượng bộ TC tổng thể (over-coverage R5/R7; thiếu Web↔App, staff)
- [x] D. Spec alignment (1 điểm cần làm rõ — §6)
- [x] E. Hành chính (TC không có ID chuẩn — [MINOR])
- [x] F. Base checklist LME
  - [x] F.1 Web — liên quan: **CL-Func-17** (setting action, partial), **CL-Func-19** (trigger chat 1:1, partial cover qua "lịch sử send action"), **CL-Func-18** (load UI trước/submit sau — [NIT] gợi ý), **CL-Func-1** (staff — [MINOR] thiếu)
  - [x] F.2 Job — không chạm callback/Google sync trực tiếp (fix ở controller mở form). N/A
  - [x] F.3 Tính năng chung — **C.2 Send message** (action = send msg): partial; **thiếu case friend block** → [MAJOR] GAP-2. C.5 Google sheet không liên quan (fix luồng mở, không phải answer sync).

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
