# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | KH #36303 (回答ID 28089) |
| Reviewer (Leader) | _<điền>_ |
| Tester được review | _<chưa rõ — Sheet không có cột Assignee fill>_ |
| Ngày review | 2026-05-12 |
| Version TCs | v1 (sheet `Quản lý hợp đồng` rows 1430-1448) |
| Vòng review | Round 1 |

> **Note đầu vào**:
> - **Input thiếu**: MCP Redmine fetch fail (401 auth) → `01-bug-task.md` được suy luận từ dev report trên sheet, **chưa verify nguyên văn Redmine 36303**. Tester cần verify lại trước khi review final.
> - **Spec reference**: Không có spec riêng — fallback `templates/LME-SYSTEM-SPEC.md`.
> - **Format file 04**: Sheet gốc dùng nested checklist (Main / Sub1 / Sub2 / ... / Step / Note), KHÔNG phải 10-column TC list chuẩn. Đã chuyển đổi best-effort thành 18 TCs (TC-01 → TC-18), nhưng nhiều cột Precondition/Steps rỗng vì sheet không có.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có **5 BLOCKER** + nhiều MAJOR. Cần fix và review lại Round 2.

**Lý do**: (1) TC-17 có expected khả năng **mâu thuẫn** với fix logic, (2) GAP hoàn toàn cho `detailContractBillMaxFriendError` + T3 max friend (Direct impact bị skip), (3) Không có TC reproduce ĐÚNG flow KH (Standard slot chưa connect bot), (4) GAP cho `authenticationBotContract` (F10), (5) 18/18 TCs đều thiếu Precondition + Steps cụ thể — không thể chạy lại.

---

## 2. Tóm tắt cho member

Bộ TC em viết đã bám được **khung phân quyền 2 chiều** (Staff có quyền / không có quyền) và phủ được hầu hết các **thao tác sub-card / change card / change bill type / hủy hợp đồng** — đây là phần coverage tốt. **Tuy nhiên, có 5 vấn đề BLOCKER cần fix trước khi merge**: (1) **TC-17 "Check own contract detail của staff"** đang ghi Expected = "Access denied", nhưng theo fix `nếu hợp đồng của chính mình → bỏ qua check quyền` thì phải Access được — em xem lại expected có sai không, hoặc title của TC cần làm rõ ngữ cảnh. (2) Thiếu **toàn bộ TC cho hợp đồng Max Friend** (`detailContractBillMaxFriendError` — F4/T3 trong dev impact, Direct impact). (3) Không có TC reproduce đúng case KH gốc: **Standard Plan slot chưa connect bot** + staff không có quyền màn point setting → hủy. (4) Thiếu TC cho `authenticationBotContract` (F10). (5) **18/18 TCs có cột Precondition + Steps rỗng** — sau 1 tuần em hoặc người khác không reproduce lại được. Em bổ sung 13 TC ở §5 + fix 4 lỗi trên rồi anh review lại Round 2.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — Reproduce KH 36303 (Standard slot chưa connect bot + staff không quyền → hủy) | Fix | — | _Không có TC ĐÚNG flow KH_ — TC-17 ambiguous | 0 | **GAP** |
| **F1** — `getRouteFromRoleAccess` | Function | Direct | TC-01, TC-09, TC-17, TC-18 (test routing-by-role gián tiếp) | 4 | RISK (thiếu boundary: contract states, role variants) |
| **F2** — `getRouterBotInvite` | Function | Indirect | _(không có TC)_ | 0 | **GAP** |
| **F3** — `detailContract` | Function | Direct | TC-01, TC-09, TC-17, TC-18 | 4 | RISK (thiếu boundary state contract) |
| **F4** — `detailContractBillMaxFriendError` | Function | Direct | _(không có TC)_ | 0 | **GAP — BLOCKER** |
| **F5** — `changeCard` | Function | Direct | TC-02, TC-10 | 2 | RISK (thiếu negative: card invalid, expired) |
| **F6** — `changeBillType` | Function | Direct | TC-07, TC-15 | 2 | RISK (thiếu boundary plan switch) |
| **F7** — `changePaymentMethod` | Function | Direct | TC-02/03, TC-10/11 | 4 | RISK (thiếu negative) |
| **F8** — `updateSubCard` | Function | Direct | TC-04/05, TC-12/13 | 4 | RISK |
| **F9** — `deleteSubCard` | Function | Direct | TC-06, TC-14 | 2 | RISK |
| **F10** — `authenticationBotContract` | Function | Direct | _(không có TC)_ | 0 | **GAP** |
| **D-** | Data | — | N/A (dev khẳng định không có data update) | N/A | N/A |
| **T1** — Phân quyền các màn | Feature | High | TC-01, TC-09, TC-17, TC-18 | 4 | RISK |
| **T2** — Detail hợp đồng | Feature | High | TC-01, TC-09, TC-17 | 3 | RISK |
| **T3** — Detail hợp đồng **max friend** | Feature | High | _(không có TC)_ | 0 | **GAP — BLOCKER** |
| **T4** — Change card | Feature | Medium | TC-02, TC-10 | 2 | OK |
| **T5** — Change phương thức thanh toán | Feature | Medium | TC-02/03, TC-10/11 | 4 | OK |
| **T6** — Change sub card (đăng ký + update) | Feature | Medium | TC-04/05, TC-12/13 | 4 | OK |
| **T7** — Xóa sub card | Feature | Medium | TC-06, TC-14 | 2 | OK |
| **T8** — Change type bill | Feature | Medium | TC-07, TC-15 | 2 | OK |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC-19 | "Check account staff" (row 1448) | Row rỗng — chỉ có Main="Check account staff" + Note="OK", không có Sub/Step/Expected | Xóa hoặc bổ sung nội dung. Nếu intended là 1 nhóm TCs về test với account staff (CL1 LME) thì cần list ra sub-TCs cụ thể. |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] TC-17**: Title "Check own contract detail của staff" — Expected = "Access denied". Theo fix mục 2 dev impact (`nếu hợp đồng của chính mình ko cần check quyền`) → vào contract của chính mình PHẢI access được. **Một trong 2 vấn đề**: (a) Expected ghi SAI (đáng lẽ Access được), hoặc (b) Title TC ambiguous — không rõ "own contract của staff" có nghĩa "contract của user đang login (staff role)" hay "contract của staff khác". Đây là TC core để verify fix → BLOCKER. **Fix**: Tester verify lại với dev, rename title rõ ràng (vd: `[F3] Own contract — owner login từ context bot khác mà mình staff không quyền — vào detail`), sửa Expected = "Access được hợp đồng thành công, hiển thị đầy đủ thao tác".

- **[BLOCKER] GAP-1 (BUG reproduce)**: Không có TC reproduce ĐÚNG flow KH 36303: **Standard Plan slot chưa connect bot** + user là **staff không có quyền màn point setting** cho bot kia → thao tác **hủy** contract. Đây là kịch bản gốc của KH, cần TC riêng để verify fix → BLOCKER. **Fix**: Bổ sung `TC-NEW-01` ở §5.

- **[BLOCKER] GAP-2 (F4 + T3)**: Hoàn toàn không có TC cho `detailContractBillMaxFriendError` / "Detail hợp đồng max friend". Dev đánh giá đây là **Direct impact + High risk regression** nhưng TCs skip 100%. Cần ít nhất: positive (access được) + reproduce bug equivalent + cover các thao tác sub-card/change card trên max friend contract. **Fix**: Bổ sung `TC-NEW-04` ở §5.

- **[BLOCKER] GAP-3 (F10)**: Không có TC cho `authenticationBotContract`. Function này authenticate scope contract với bot — liên quan trực tiếp tới logic permission/security. Có thể có lỗ hổng cross-bot access. **Fix**: Bổ sung `TC-NEW-05` ở §5.

- **[BLOCKER] Chất lượng TC**: 18/18 TCs có **Precondition + Steps rỗng**. Chỉ có 1 dòng action ngắn (vd "change card -> tranfer") ở cột Step/Note. Không thỏa B.1 (Rõ ràng), B.2 (Atomic) của review-checklist. Tester khác (hoặc bản thân member sau 1 tuần) không thể chạy lại. **Fix**: Mỗi TC phải có ít nhất: (a) Precondition đầy đủ (account A có contract X loại Y trạng thái Z; account A là staff bot W với role R), (b) Steps tuần tự numbered list, (c) Expected đo lường được (KHÔNG chỉ "thành công" — phải nói rõ field nào hiển thị, button nào enable, redirect đến URL nào).

### 4.2 Major (nên fix)

- **[MAJOR] TC-09 Expected có khả năng sai context**: "Check other bot contract detail của user" — Expected "Access được". Trong context Sub1 = "Staff không có quyền access hợp đồng" — nếu user đang login KHÔNG có quyền + contract đang xem KHÔNG phải own → theo fix `if (own) skip else check permission` → cần check quyền → không có → phải DENIED. Nhưng TC ghi Access được. **Mâu thuẫn lần 2** (tương tự TC-17). **Fix**: Verify lại với dev — có phải "user" ở đây ám chỉ "user đang login (= owner contract)" không, nếu vậy thì rename title cho rõ.

- **[MAJOR] GAP-4 (Plan types)**: Tất cả TCs test 1 plan implicit. Bug có thể có rule khác cho Free / Standard / Pro / Enterprise. Cần test matrix plan type × permission. **Fix**: Bổ sung `TC-NEW-10`.

- **[MAJOR] GAP-5 (Contract states)**: Không test contract states đa dạng: chưa connect bot / đã connect / expired / cancellation pending / trial. Bug gốc là "slot chưa connect" — edge case này critical. **Fix**: Bổ sung `TC-NEW-09`.

- **[MAJOR] GAP-6 (Role staff variants)**: Chỉ test 2 cấp "có quyền / không có quyền". Thực tế LME có nhiều role staff với permission khác nhau (chỉ chat, chỉ template, full admin trừ point setting). Bug 36303 specific là "không có quyền màn point setting" — cần test ít nhất role này riêng. **Fix**: Bổ sung `TC-NEW-08`.

- **[MAJOR] GAP-7 (CL11 — CRUD đúng account)**: Task chính về CRUD wrong account context → CL11 LME yêu cầu test 2 account có cùng data → verify update đúng account. Member chưa cover. **Fix**: Bổ sung `TC-NEW-07`.

- **[MAJOR] GAP-8 (A.2 Security — URL tampering)**: Bug về permission → cần test: (a) Gõ URL detail contract của user khác → denied, (b) Đổi param ID URL bằng contract user khác sau login → denied, (c) Staff không cấp quyền access URL → denied. Cả 3 đều thiếu. **Fix**: Bổ sung `TC-NEW-06`.

- **[MAJOR] GAP-9 (CL3 chuyển tab/bot context)**: Bug có root cause "đang lấy quyền theo bot đang select". Cần test: user vào detail contract → switch bot dropdown sang bot khác → behavior (refresh / kept state / redirect)? **Fix**: Bổ sung `TC-NEW-12`.

- **[MAJOR] GAP-10 (CL18 load UI + submit sau)**: User load detail contract → admin/system thay đổi role mid-session → user submit thao tác → expect xử lý lỗi đúng. **Fix**: Bổ sung `TC-NEW-13`.

- **[MAJOR] GAP-11 (C.1 Bill tiền — case delay callback)**: Task chạm change card / change bill type → CẦN cover delay callback bill tiền theo Checklist LME §C.1. **Fix**: Bổ sung `TC-NEW-11`.

- **[MAJOR] TC-18 ambiguous**: "Change từ có quyền → không có quyền" — không rõ scenario state change diễn ra ở đâu (admin-side / mid-session / reload sau). Steps + precondition rỗng. **Fix**: Tách thành 2-3 TCs với scenario cụ thể (vd: TC-18a "Reload sau khi mất quyền — access denied", TC-18b "Đang xem detail thì bị remove quyền mid-session — submit thao tác — response").

- **[MAJOR] TC-19 incomplete**: Row 1448 "Check account staff" để rỗng. **Fix**: Xóa hoặc bổ sung nội dung cụ thể (vd: rà CL1 LME — staff không phân quyền không access, staff phân quyền access tương đương account chính).

- **[MAJOR] Bộ TC mất cân đối Positive : Negative : Boundary : Regression**: 16 Positive / 2 Negative (TC-17, TC-18) / 0 Boundary / 0 Regression dedicated. Tỷ lệ chuẩn 30/25/25/20. **Fix**: Bổ sung các TC negative (card expired, sub card invalid) + boundary (max sub cards, contract expired tại thời điểm thao tác) + regression (verify owner full permission flow không bị ảnh hưởng).

### 4.3 Minor (có thể fix sau)

- **[MINOR] Title TC không chứa function name**: Toàn bộ titles dùng feature/action ngôn ngữ tự nhiên. Không có keyword F1-F10 / function name → khó map coverage. **Fix**: Rename mẫu: `[F3 detailContract] Owner login từ bot context khác — vào detail contract của chính mình`.

- **[MINOR] TC ID rỗng**: Sheet không có cột TC ID — tôi gán TC-01 → TC-19 cho convenience. Member nên fill TC ID chuẩn (vd `LME-36303-01`) trước khi sync sheet master.

- **[MINOR] Status = "OK" pre-fill toàn bộ**: Tất cả 18 rows đã có cột Note = "OK" trước khi test. Practice không đúng — Status nên empty trước test, fill sau.

- **[MINOR] Format sheet không tương thích 10 cột chuẩn**: Sheet đang dùng nested checklist (Main / Sub1-6 / Step / Note). Khi `/sync-tc` push, format này không map sang 10 cột. **Fix**: Sau khi member fix các blocker, copy sang format `04-tc-list.md` chuẩn (TC ID / Title / Type / Priority / Precondition / Steps / Expected / Output note / Assignee / Status).

- **[MINOR] Cell inherit (merge visual)**: TC-03 → TC-08, TC-10 → TC-16 inherit Sub1/Sub2 từ row trên. Khi sort/remove TC → mất context. **Fix**: Ghi đầy đủ Sub1/Sub2 mỗi row.

- **[MINOR] Typo "tranfer" → "transfer"** ở các Step.

### 4.4 Nit (gợi ý)

- **[NIT]** Có thể gộp TC-02 + TC-03 (change card ↔ transfer 2 chiều) thành 1 TC với matrix table 2x2 verify.
- **[NIT]** TC-08 (hủy hợp đồng) cần liên hệ CL20 LME: "Khi hủy hợp đồng phải clear richmenu + hủy schedule + QR code không action nữa". Hiện TC chỉ verify "hủy thành công" — đề nghị extend.
- **[NIT]** TC-04/05/06/12/13/14 (sub-card) có thể test thêm với scenario có > 5 sub card (max limit ngầm?).

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Tất cả TC sau đây phải có **Precondition + Steps đầy đủ** — không để rỗng.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| **TC-NEW-01** | Reproduce KH #36303 — Standard slot chưa connect, hủy contract từ staff context không quyền | (1) Tạo user A. A đăng ký 1 Standard Plan slot CHƯA kết nối bot.<br>(2) Mời A làm staff cho bot B (owner = user C), với role **không có quyền màn point setting**.<br>(3) Đăng nhập A, đảm bảo context đang chọn bot B (dropdown bot B). | 1) Vào menu Quản lý hợp đồng<br>2) Click vào Standard Plan slot chưa connect<br>3) Quan sát có vào được detail không<br>4) Click button **Hủy hợp đồng**<br>5) Confirm dialog → click OK | (a) Bước 3: Vào detail thành công, KHÔNG redirect ra với lỗi "không có quyền".<br>(b) Bước 5: Hủy thành công, contract chuyển trạng thái cancelled, KHÔNG báo lỗi.<br>(c) Reload màn list contract — slot Standard đó biến mất hoặc hiển thị "已解約". | High | Positive (reproduce) | BUG, F1, F3, T1, T2 |
| **TC-NEW-02** | Owner vào own contract — context default (chưa chọn bot) | Tạo user A, đăng ký Standard slot chưa connect. Login A, KHÔNG select bot nào (context global). | 1) Login user A<br>2) Vào Quản lý hợp đồng<br>3) Click detail Standard slot chưa connect | Access được hợp đồng, hiển thị đầy đủ button thao tác (change card / change bill type / hủy). | Medium | Regression | F1, F3, T2 |
| **TC-NEW-03** | Owner full quyền staff bot khác — verify regression mọi thao tác | (1) User A là owner Standard contract chưa connect.<br>(2) A là staff bot B với role **đầy đủ quyền (bao gồm point setting)**.<br>(3) Login A, context bot B. | 1) Vào detail contract<br>2) Lần lượt: change card → transfer → card → đăng ký sub card → change sub card → xóa sub card → change type bill → KHÔNG hủy | Mỗi thao tác đều thành công, DB lưu đúng, UI cập nhật đúng. Không có "không có quyền" alert. | High | Regression | F1, F3, F5, F6, F7, F8, F9, T1, T2, T4, T5, T6, T7, T8 |
| **TC-NEW-04** | Detail hợp đồng MAX FRIEND — owner từ staff context không quyền | (1) User A có contract **max friend** (có bot connected).<br>(2) A là staff bot B với role không có quyền.<br>(3) Login A, context bot B. | 1) Vào màn hợp đồng<br>2) Click vào contract max friend<br>3) Verify access<br>4) Test mọi thao tác: change card, change bill type, sub card | (a) Access được detail max friend contract.<br>(b) Mọi thao tác thành công.<br>(c) Verify `detailContractBillMaxFriendError` không trigger error path. | High | Positive | F4, T3 |
| **TC-NEW-05** | authenticationBotContract scope check | (1) User A là owner contract đã connect bot Y.<br>(2) A là staff bot Z. | 1) Login A, context bot Z<br>2) Truy cập detail contract gắn bot Y<br>3) Thử thao tác change card | Verify behavior phù hợp spec: nếu spec cho phép owner access bất kể context → access được. Nếu spec require context = bot connected → redirect / refresh context. **Verify với dev trước khi viết Expected chính xác.** | High | Functional | F10, T1 |
| **TC-NEW-06** | Security — URL tampering contract của user khác | (1) User A có contract X. User B có contract Y (cùng plan).<br>(2) Login user B. | 1) Login B, lấy URL detail contract Y từ session B (vd `/contract/Y_id`)<br>2) Đổi `Y_id` → `X_id` (contract của A)<br>3) Submit URL | Access denied — không xem được contract X. Verify cả 3 case: (a) URL detail, (b) URL change card, (c) URL hủy contract. | High | Negative (security) | F1, F10, T1 |
| **TC-NEW-07** | CL11 — CRUD đúng account context | (1) User A và User B đều có Standard Plan slot chưa connect, **cùng plan tier**.<br>(2) Login user A. | 1) A vào detail Standard slot của A<br>2) A change card<br>3) A hủy contract<br>4) Logout, login B<br>5) B kiểm tra contract của B | Contract của B **không bị ảnh hưởng** (card thanh toán không đổi, contract vẫn active). DB verify `WHERE user_id = A` đúng. | High | Negative (CRUD scope) | F3, F5, T1, T2 |
| **TC-NEW-08** | Role staff variants — matrix permission | Tạo bot B với owner C. Mời user A làm staff với từng role:<br>- R1: full admin<br>- R2: full trừ point setting (= scenario bug)<br>- R3: chỉ chat<br>- R4: chỉ template | Với từng role A login → context bot B → vào detail own contract: | A access được detail own contract trong **mọi role**, vì fix bỏ qua check quyền cho own contract. Verify với từng role R1, R2, R3, R4. | High | Positive matrix | F1, F2, T1 |
| **TC-NEW-09** | Contract states matrix — own contract permission | User A là owner các contracts với states khác nhau: (a) chưa connect, (b) connected active, (c) expired, (d) cancellation-pending, (e) trial. A là staff bot B không quyền. | Login A, context bot B → vào từng contract a-e | (a)(b)(d)(e): Access được, hiển thị thông tin contract + thao tác phù hợp state. (c) expired: Access được view-only, KHÔNG cho thao tác change. | High | Boundary | F3, F4, T2, T3 |
| **TC-NEW-10** | Plan types matrix — own contract permission | User A là owner contracts: Free / Standard / Pro / Enterprise / Max friend. A là staff bot B không quyền. | Login A, context bot B → vào từng contract per plan | Access được mọi plan type. Thao tác change card / change bill type / sub card thành công với plan có tính năng đó (Free có thể không có sub card). | High | Boundary | F3, F4, T2, T3, T4-T8 |
| **TC-NEW-11** | C.1 Bill tiền — delay callback từ payment gateway | User A là staff không quyền + owner Standard contract. | 1) A vào detail contract → change card<br>2) Simulate delay callback từ payment gateway (vd 30s)<br>3) Trong khoảng delay: A thao tác lại change card | Không double-charge, không tạo duplicate billing record. Verify state contract đúng sau khi callback về. | Medium | Boundary | F5, F7, T4, T5 |
| **TC-NEW-12** | CL3 — chuyển bot context khi đang xem detail contract | User A là owner Standard contract + staff bot B (không quyền) và staff bot C (có quyền). | 1) Login A, context bot B → vào detail Standard contract<br>2) Trong khi đang ở detail, click dropdown chuyển sang bot C | (a) Behavior phù hợp spec: refresh detail / redirect về list / kept state? **Verify với dev/PM.**<br>(b) Sau switch, vào lại detail → access bình thường (own contract). | Medium | Boundary | F1, F2, T1 |
| **TC-NEW-13** | CL18 — load before submit + role change mid-session | User A là staff bot B với quyền điểm setting. A đang ở detail contract của bot B (NOT own — owner là C). | 1) A load detail contract<br>2) Owner C remove quyền của A (admin-side)<br>3) Trên session A, A submit change card | (a) Submit failed với error rõ ràng (vd "Quyền của bạn đã thay đổi, vui lòng reload").<br>(b) Không corrupt data — card cũ vẫn nguyên. | Medium | Negative | F1, F5, T1, T4 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - **Section**: `templates/LME-SYSTEM-SPEC.md` — Quản lý hợp đồng / Phân quyền access detail contract
  - **Nội dung cần update**: Bổ sung rule mới do fix introduce: "Khi user vào màn detail contract, **ưu tiên check ownership trước**. Nếu user là owner của contract → bỏ qua check quyền bot (role-based). Chỉ check quyền bot nếu user KHÔNG phải owner." Áp dụng cho mọi thao tác: view detail / change card / change payment method / change bill type / update + delete sub card / hủy contract / contract max friend.
  - **Người chịu trách nhiệm update**: Dev assignee + PM.
  - **Câu hỏi cần dev clarify**:
    1. Logic ownership check dựa vào field nào (`contracts.user_id`? `contracts.owner_id`?)
    2. Có rule riêng cho **max friend contract** không (`detailContractBillMaxFriendError` được list nhưng dev report không nói khác biệt)?
    3. Khi contract đã connect bot Y, user là staff bot Y (không phải owner) → permission check thế nào? Vẫn check quyền hay coi như implicit owner?
    4. Có cache permission (Redis) không? Mid-session role change có invalidate ngay không?

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — FAIL: GAP F2, F4, F10, T3 + BUG reproduce thiếu
- [x] **B. Chất lượng từng TC** — FAIL: 18/18 thiếu Precondition + Steps + Expected đo lường được
- [x] **C. Chất lượng bộ TC** — FAIL: Ratio 16/2/0/0 (Positive/Negative/Boundary/Regression), thiếu role variants
- [x] **D. Spec alignment** — Flag spec update (mục 6)
- [x] **E. Hành chính** — FAIL: TC ID rỗng, Assignee rỗng, Status pre-fill OK, format sheet không 10 cột chuẩn
- [x] **F. Base checklist LME**:
  - [ ] **F.1 Checklist web** — chưa cover: CL1 (account staff đầy đủ — đang có nhưng sơ sài), CL3 (chuyển tab/bot), CL11 (CRUD đúng account), CL18 (load + submit sau), A.2 Security (URL tampering), A.2 Regression (effect range dev)
  - [x] **F.2 Checklist job** — N/A (task không chạm job)
  - [ ] **F.3 Các tính năng chung** — chưa cover §C.1 Bill tiền (delay callback + 5 loại bill — task chạm change card/bill type nên cần)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | 2026-05-12 |
| Tester | (đã đọc & hiểu feedback) | |
