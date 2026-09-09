# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #36709 — [Form] Form「1Mアンケート」submit không reflect kết quả (T CLINIC) |
| Reviewer (Leader) | `<Leader fill>` |
| Tester được review | `<Tester fill — TCs gốc do team Form QA, file 04 fetch từ master sheet>` |
| Ngày review | 2026-05-26 |
| Version TCs | v1 (snapshot từ master sheet `Improve form 01/2025` range A1132:K1176) |
| Vòng review | Round 1 |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng (không có spec riêng cho task này — file 02 chưa được tạo).

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: 2 checkbox tester-verify (file 01 + 03) chưa tick → review chưa có giá trị. Mục 3 dev-impact rỗng (chỉ có heading). KH report symptom-only và bộ TC không cover alternative root cause. Thiếu TC concurrency (multi-tab save) + double-click save + explicit DB verification cho D1/D2 + legacy-corrupt-data submit case.

---

## 2. Tóm tắt cho member

Bộ TCs fetched từ master sheet đã có coverage tốt cho 6 feature impact (T1-T6) — đặc biệt **TC022 (row 1154) match đúng flow tái hiện trong Redmine journal**, và block TC016-TC028 cover khá đầy đủ các tổ hợp add/copy/delete page → save / reload-save. Tuy nhiên trước khi retest có 4 việc bắt buộc: (1) **tick 2 checkbox tester-verify** ở file 01 + 03 sau khi đọc lại Redmine; (2) **hỏi Dev bổ sung mục 3** (caller `removePage`, `checkingNextPage` đã check chưa?); (3) bổ sung **5 TC mới** ở mục §5 — concurrency, double-click, legacy corrupt data, explicit DB verify, alternative root cause; (4) **fill Type / Priority** cho 44 TCs (cột trống vì source sheet không có 2 trường này).

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause — flow Redmine journal #119442) | Fix | — | TC022 (chính xác), TC017/TC021 (gần đúng), TC016-TC028 (block bug reproduction) | 13 | **OK** |
| F1 — `FormAnswerService::addPage()` | Function | Direct | TC016, TC017, TC020, TC024, TC025, TC029, TC030, TC005 (qua copy=add) | 8 | **RISK** — thiếu negative (DB lỗi / lock conflict) + boundary (concurrent add) |
| F2 — `titlePageRight()` (FE render label) | Function | Direct | TC001-TC005 (Check hiển thị next page), TC010, TC011 | 7 | **RISK** — thiếu TC verify "render không mutate state" (gốc bug B3) |
| D1 — `form_answer_pages.next_page_type` | Data | UPDATE | TC016/expected mention next page → implicit; TC002 mô tả mapping | 2 (implicit) | **RISK** — chưa có TC explicit verify DB record value sau add/delete |
| D2 — `form_answer_pages.next_page_setting` | Data | UPDATE | TC016/expected "page không bị hiện next đến chính nó" → implicit; TC002 mô tả | 2 (implicit) | **RISK** — chưa có TC explicit verify DB column value (đặc biệt edge: legacy self-reference) |
| T1 — Thêm page mới | Feature | High | TC002, TC016, TC017, TC020, TC024, TC029, TC030 | 7 | **OK** |
| T2 — Xóa page | Feature | High | TC006-TC009 (rẽ nhánh), TC021-TC027 (bug block), TC035-TC038 (form đa page) | 14 | **OK** |
| T3 — Save form sau add/delete | Feature | High | Toàn bộ TC016-TC028 (đều có save), TC043 sanity | 14 | **OK** |
| T4 — Hiển thị label "Page tiếp theo" | Feature | Medium | TC001-TC005, TC010-TC011 | 7 | **OK** |
| T5 — Form submit public render | Feature | High | TC016 expected (submit không reset top), implicit toàn block bug | 13 (implicit) | **RISK** — chưa có TC seeded DB với data corrupt từ trước rồi submit (verify FE guard cứu được data lịch sử) |
| T6 — 分岐 type=2 (regression — không impact) | Feature | Low | TC011, TC013-TC015 | 4 | **OK** |

### ORPHAN TCs

Không phát hiện orphan rõ ràng. Vài TC nhìn thoáng có vẻ lạc chủ đề nhưng đều ràng buộc về với feature scope:

| TC ID | Title | Lý do "có vẻ orphan" | Hành động đề xuất |
|---|---|---|---|
| TC005 | Check copy page | Không chạm logic addPage trực tiếp | **Giữ** — copy page = clone state, đi qua cùng đường write `next_page_setting` như addPage |
| TC044 | Check account staff thao tác | Generic, không bug-specific | **Giữ** — cover CL1 (staff account) trong checklist LME |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Specific code change** (BE data-write + FE guard null + remove self-reference wrap + remove state mutation). KHÔNG phải generic catch. |
| Trigger space cần cover | (a) `addPage` với previous page = `END_FORM` → expect update sang `RIGHT_PAGE` + `setting={pageId}`. (b) `addPage` với previous page = `RIGHT_PAGE` (có setting cũ) → expect giữ nguyên. (c) `addPage` với previous page = rẽ nhánh (type=2) → expect giữ nguyên. (d) `titlePageRight()` với `next_page_setting=null` → return empty label. (e) `titlePageRight()` với page = last page → return empty (no wrap to index 0). (f) `titlePageRight()` invocation → **DB không thay đổi** (no state mutation). (g) `addPage` + concurrent admin (multi-tab) → DB consistent. |
| Số trigger TCs hiện cover | **5/7** — (a) cover qua TC002, TC016, TC029, TC030. (b) cover qua TC013 (sort 2 page setting next bên cạnh) + TC014. (c) cover qua TC015 + TC011. (d) implicit qua TC017/TC022 (reload không corrupt). (e) cover qua TC004 (chọn page cuối — không hiện selection). **(f) GAP** — không có TC verify render không mutate. **(g) GAP** — không có TC multi-tab concurrency. |
| KH report dạng | **Symptom-only** — KH chỉ thấy "submit không reflect, page reset về top". KHÔNG ghi error message / log / root cause. Dev tự tái hiện 1 root cause (self-reference setting). |
| Alternative root causes cần verify | (1) Race condition: 2 admin edit form cùng lúc, save song song → DB conflict tạo self-reference. (2) Form schema migration legacy: form cũ đã có corrupt data từ trước, deploy fix mới nhưng data cũ chưa migrate → FE guard có cứu được không? (3) JS exception trong submit handler (network error / payload sai) → cũng gây reset top, không reflect. (4) Backend `checkingNextPage` exception → response không đúng, submit bị render lại page hiện tại. |
| Anti-patterns dính | **AP-2** (Symptom-only KH report) — cần TC cover alternative root cause. **AP-6** (Mục 3 dev-impact trống) — Dev chỉ ghi heading "Đã check và sửa", không list caller cụ thể như `removePage`, `checkingNextPage`. **AP-4 partial** (Commit/PR link trống) — không verify được fix shape thực tế là specific vs generic. **KHÔNG dính** AP-1 (single-trigger generic-fix — vì đây là specific code change), AP-3 (happy-path-only regression — bộ TC có edge state), AP-5 (layer-downstream over-coverage — TC cover đúng layer BE+FE đã fix). |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] AUTO-FILL: 01 + 03 chưa được tester verify** — Cả 2 file `01-bug-task.md` và `03-dev-impact.md` được auto-fill từ Redmine bởi `/new-task` lúc 2026-05-26 nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. Review chưa có giá trị cho đến khi tester đọc lại Redmine #36709 (description + journal #119442) và xác nhận F/D/T mapping không sai/sót. — **Fix**: tester mở Redmine, đọc lại mục "Tái hiện bug" + "Đánh giá ảnh hưởng" + attachment, đối chiếu với 01 + 03, sửa nếu sai, tick checkbox.

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE: thiếu TC verify "render không mutate state" (trigger f)** — Bug B3 root cause là `titlePageRight()` mutate `page.next_page_setting = {...}` trong khi render. Fix đã bỏ dòng mutate này, nhưng KHÔNG có TC explicit nào verify "mở setting form → KHÔNG edit gì → reload → DB unchanged". TC017/TC022 implicit cover (vì nếu mutate xảy ra thì final submit fail), nhưng nếu có TC bỏ bước "reload" thì miss. — **Fix**: thêm TC-NEW-05 ở §5.

- **[MAJOR] FIX-SHAPE: thiếu TC multi-tab concurrency (trigger g)** — Fix chạm cả BE addPage và FE render. CL3 LME checklist yêu cầu "check chuyển tab setting". Bug có thể tái hiện ở dạng race condition: 2 admin (hoặc cùng 1 user 2 tab) edit form cùng lúc, save song song → DB không nhất quán. — **Fix**: thêm TC-NEW-01 ở §5.

- **[MAJOR] SYMPTOM-ONLY (AP-2): bộ TC không cover alternative root cause** — KH report symptom-only, Dev tái hiện 1 root cause. Cần ít nhất 1 TC verify alternative root cause cùng tạo symptom "submit reset top": (1) form đã có data corrupt từ trước (legacy schema migration); (2) JS exception trong submit handler; (3) backend `checkingNextPage` exception. — **Fix**: thêm TC-NEW-02, TC-NEW-06 ở §5. Hỏi Dev xác nhận `checkingNextPage` đã được defensive-check chưa.

- **[MAJOR] AP-6: Mục 3 dev-impact rỗng (chỉ heading)** — Dev không list rõ caller đã check. Mục 4.3 mention `removePage`, `checkingNextPage` nhưng mục 3 không xác nhận đã check 2 function này. Có thể có function cùng pattern bug (mutate state khi render) chưa được check/fix. — **Fix**: hỏi Dev (Thanh Phương) xác nhận đã check `removePage` (xử lý xóa page cuối → reset previous page về END_FORM) và `checkingNextPage` (BE submit handler) chưa.

- **[MAJOR] AP-4: Commit / Pull Request link trống** — File 03 ghi `<chưa có>` cho field "Commit / Pull Request". Không có PR link → không thể verify fix shape thực tế (specific check hay generic catch). Có khả năng impl thực tế đã handle thêm condition mà Dev không ghi vào mục 2. — **Fix**: yêu cầu Dev điền link PR vào file 03 trước khi merge.

- **[MAJOR] DB VERIFICATION (D1, D2): chỉ implicit qua user-visible behavior** — Không có TC nào explicit nói "verify DB record sau add/delete page" cho D1 (`next_page_type`) và D2 (`next_page_setting`). Bug root cause nằm ở DB state, nên kiểm DB level là chiều quan trọng. — **Fix**: thêm TC-NEW-04 ở §5.

- **[MAJOR] LEGACY CORRUPT DATA: thiếu backward-compat test** — Mục 4.3 dev-impact note "với page cuối có type=1 (data lịch sử corrupt), label giờ hiển thị '選択してください' thay vì wrap về page đầu". Tức Dev biết có form đã có data hỏng từ trước (như form 1Mアンケート của T CLINIC trước khi deploy). Fix có cứu được data cũ này không? **Bắt buộc** verify. — **Fix**: thêm TC-NEW-02 ở §5.

- **[MAJOR] CL5 LME — Double-click save** — Master sheet không có TC double-click cho flow add/save page. Fix chạm logic write DB → double-click có khả năng tạo state lỗi (duplicate record / partial write). — **Fix**: thêm TC-NEW-03 ở §5.

- **[MAJOR] Member tự check Base checklist LME trong file 04 đều CHƯA tick** — Toàn bộ checkbox §C trong "Member tự check trước khi submit" (Coverage check + Base checklist LME) chưa được tester tick. Cần tester rà từng mục trước khi review tiếp. — **Fix**: tester đọc file 04 mục cuối, tick các mục đã cover, để trống mục N/A.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC017-TC028 Expected = "(inherit từ TC016)"** — Block bug reproduction dùng Expected chung. Nếu reviewer hoặc tester chạy lẻ TC này mà không đọc TC016 thì miss criteria. Source sheet vốn ghi vậy (cell trống), không nên sửa. — **Fix**: khi /sync-tc push back lên master, ghi chú "see TC016" trong cột Note thay vì để trống.

- **[MINOR] TC029-TC042 + TC010 Expected hoàn toàn trống** — Master sheet trống thật. Tester chạy phải nhìn Title + Steps để tự suy expected. — **Fix**: tester run TC sẽ fill Actual Result + đề xuất Expected để leader confirm bổ sung vào master.

- **[MINOR] TC044 chỉ có Main Function, Steps + Expected trống** — "Check account staff thao tác" cần expand sub-steps (staff được phân quyền vs không). — **Fix**: tester expand thành 2 sub-TC khi run thực tế (đối chiếu CL1 LME).

- **[MINOR] Type + Priority cột trống cho cả 44 TCs** — Source sheet không có 2 trường này. Khó phân bổ Positive/Negative/Boundary/Regression và High/Medium/Low. — **Fix**: tester fill khi run (gợi ý: TC016-TC028 = Regression+High, TC022 = Positive+High, TC017/TC022 = Boundary+High vì test reload flow, TC044 = Negative+Medium).

### 4.4 Nit (gợi ý)

- **[NIT] Title TCs dùng tiếng Việt mix viết tắt** — Vài chỗ dùng "k" thay "không" (TC013: "2 page k có page nào là page cuối cùng"). Cosmetic, nhưng nếu /sync-tc push back master thì nên giữ tiếng Việt chuẩn.

- **[NIT] Sheet master "Bug Report #36709" cột J — value "Test bug"** — Convention team dùng "Test bug" để đánh dấu TC cần retest cho bug đó. Khi member chạy xong, value sẽ chuyển sang OK / NG. /review-tc giữ raw "Test bug" → /sync-tc khi push lại map sang Status enum.

- **[NIT] Environment compat (Win+Mac, Android+iOS) — Section A.2 LME** — Không phải fix browser-specific, nhưng form public render là LIFF (LINE in-app browser). Khuyến nghị retest TC016/TC022 trên cả Android LINE app + iOS LINE app.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo (table phụ bên dưới block fetched, KHÔNG chèn vào table chính vì TCs gốc là read-only snapshot từ master sheet).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | **Multi-tab concurrent save** — 2 tab cùng edit form 1 page, save gần như đồng thời | Form rẽ nhánh 1 page A, type=END_FORM. Mở 2 tab cùng URL setting form, cùng admin login. | (1) Tab 1: add page B → click Save. (2) Tab 2 (ngay sau): add page C → click Save. (3) Reload cả 2 tab → check setting form. (4) Open public link → submit answer. | DB nhất quán: 1 trong 2 tab báo conflict / save success theo logic team. Không có page nào lưu `next_page_setting` self-reference. Submit form vẫn reflect kết quả, không reset top. | High | Boundary | F1, D1, D2, T3, CL3 |
| TC-NEW-02 | **Legacy corrupt data submit** — submit form đã có self-reference từ trước fix (data lịch sử của T CLINIC trước deploy) | Seed DB record `form_answer_pages`: form X có page cuối với `next_page_type=1 (RIGHT_PAGE)` + `next_page_setting={"pageId":<chính nó>}`. Cố tình insert raw SQL để simulate data lịch sử. | (1) Mở setting form X → verify FE render label page cuối hiển thị `'選択してください'` (không wrap về index 0). (2) Mở public URL form X → nhập answer → submit. | (1) Setting form: label page cuối = `'選択してください'`, không crash JS. (2) Submit: kết quả reflect (không reset top) — FE guard cứu được data legacy. | High | Regression | F2, T4, T5 — verify backward-compat |
| TC-NEW-03 | **Double-click save** — click Save button rapidly khi add page | Form rẽ nhánh 1 page A. | (1) Add page B (chưa save). (2) Double-click button Save trong < 200ms. (3) Reload màn hình → check setting + check DB. | Chỉ 1 record write thành công, không có duplicate page B, không có state lỗi (no self-reference). | Medium | Boundary | F1, D1, D2, CL5 |
| TC-NEW-04 | **Explicit DB verification — addPage update previous page setting** | Form 1 page A: DB record `next_page_type=3 (END_FORM)`, `next_page_setting=null`. | (1) Add page B → save. (2) Truy vấn DB `SELECT next_page_type, next_page_setting FROM form_answer_pages WHERE form_id=X ORDER BY position`. | Row page A: `next_page_type=1 (RIGHT_PAGE)`, `next_page_setting='{"pageId":<B.id>}'`. Row page B: `next_page_type=3 (END_FORM)`, `next_page_setting=null`. | High | Positive | F1, D1, D2 — explicit DB verify, không qua UI |
| TC-NEW-05 | **titlePageRight() không mutate state** — render không side-effect | Form 1 page A type=END_FORM (sau khi B1+B2 đã xảy ra: thêm page → xóa). | (1) Mở setting form (không edit gì). (2) Chờ FE render xong. (3) KHÔNG click save. (4) Reload trang. (5) Check DB column `next_page_setting` của page A. | DB column `next_page_setting` của page A vẫn `null` (FE render không mutate state). | High | Regression | F2 — verify fix "bỏ dòng mutate state" |
| TC-NEW-06 | **Alternative root cause — BE checkingNextPage exception → submit reset top** | Form rẽ nhánh có data setup đúng. Mock BE response `checkingNextPage` trả exception / status 500. | (1) User mở public form. (2) Nhập answer + submit. (3) Quan sát hành vi page. | UX recovery rõ ràng: hiển thị error message business-friendly, không silent reset về top. Verify defensive handling phía FE submit. | Medium | Negative | BUG (alternative root cause), T5 |
| TC-NEW-07 | **Compat — submit form trên LINE in-app browser (LIFF)** | Form public link của bot T CLINIC. | (1) Mở link trong LINE app trên Android. (2) Submit. (3) Lặp lại trên iOS LINE app. | Cả 2 device đều submit reflect kết quả, không reset top. | Medium | Regression | T5, Non-function (Compatibility) |

> **Note thêm cho member**: TC-NEW-01 và TC-NEW-03 cũng cần hỏi Dev xem BE có lock optimistic / unique constraint trên `form_answer_pages` không — nếu không có thì 2 TC này có thể tái hiện ra bug khác. TC-NEW-02 cần phối hợp Dev cung cấp SQL seed để simulate legacy state.

---

## 6. Spec update needed

- [x] **Cần update spec** — chi tiết:
  - Section: Form answer / Setting rẽ nhánh (`templates/LME-SYSTEM-SPEC.md` mục Form, hoặc spec riêng `spec-features/admin/form-answer/`)
  - Nội dung cần update: Document rõ behavior label "Page tiếp theo" khi page cuối có `next_page_type=1` (data lịch sử corrupt) — bây giờ hiển thị `'選択してください'` thay vì wrap về page đầu (per mục 4.3 dev-impact).
  - Người chịu trách nhiệm update: Leader phối hợp Dev (Thanh Phương) — sau khi PR merge, update spec snapshot.

---

## 7. Checklist đã chạy

- [x] A. Coverage — done (matrix §3)
- [x] B. Chất lượng từng TC — done (đã rà §4 MINOR cho clarity / atomic / realistic)
- [x] C. Chất lượng bộ TC tổng thể — done (Type/Priority gap đã ghi §4.3, no duplicate, no orphan rõ ràng)
- [ ] D. Spec alignment — file 02 không tồn tại, dùng LME-SYSTEM-SPEC tổng. Note spec update ở §6.
- [x] E. Hành chính — done (TC IDs format chuẩn TC001-TC044, file 04 đúng folder review, version v1 đã điền)
- [x] F. Base checklist LME — done (rà §A.1-A.2, §B, §C — chi tiết dưới)
  - [x] F.1 Checklist web — **CL1 (staff)** TC044 cover; **CL2 (reload)** heavily covered (TC017/19/22/25/27/28/39/42); **CL3 (chuyển tab)** GAP → TC-NEW-01; **CL4 (thao tác liên tục)** cover (TC020/24/25/28); **CL5 (double-click)** GAP → TC-NEW-03; **CL7 (plan limits)** N/A (task không chạm plan); **CL8 (copy/preview)** TC005 cover; **CL11 (CRUD đúng account)** PARTIAL — không có TC verify bot khác không bị ảnh hưởng (Leader tự cân nhắc add hay không vì scope task hẹp); **CL15 (phân trang/scroll)** N/A vì task không chạm pagination; **CL18 (load UI trước, release sau)** N/A; **CL22 (upload file)** N/A. Non-function: Compatibility GAP → TC-NEW-07 cover LINE app cross-platform.
  - [x] F.2 Checklist job — B.1 callback **N/A**, B.2 sync Java (Form Google sheet) **N/A** vì fix không chạm sync logic. Note: form 1Mアンケート có Google Sheet linkage qua C.5 nhưng fix scope không chạm sync — confirm với Dev nếu có nghi ngờ.
  - [x] F.3 Các tính năng chung — C.1 Bill **N/A**, C.2 Send message **N/A**, C.3 Friend info **N/A**, C.4 Tag **N/A**, C.5 Google sheet (form-answer) — fix không chạm sync nhưng nếu form có sync setup thì retest 1 case sync sau deploy. C.6 Calendar **N/A**, C.7 Plan limits **N/A**, C.8 Sort — TC039-TC042 cover sort page within form.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<sẽ ký sau khi tester fix 9 issue MAJOR + 1 BLOCKER>` | |
| Tester | `<đã đọc & hiểu feedback>` | |

---

> **Next action chuỗi**:
> 1. Tester verify 2 checkbox (file 01 + 03) sau khi đối chiếu Redmine #36709.
> 2. Tester / Leader hỏi Dev (Thanh Phương) bổ sung mục 3 dev-impact (caller `removePage`, `checkingNextPage`) + cung cấp PR link.
> 3. Tester run 44 TCs fetched + viết thêm 7 TC ở §5 (table phụ trong file 04).
> 4. Round 2 review sau khi member commit fix.
