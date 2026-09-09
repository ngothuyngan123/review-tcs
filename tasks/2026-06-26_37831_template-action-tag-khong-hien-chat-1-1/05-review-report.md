# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #37831 — [T11287][Template] Template gửi qua action không hiển thị ở chat 1:1 + tên template chứa `&` half-width hiển thị sai |
| Reviewer (Leader) | Claude (draft) — Leader verify |
| Tester được review | (TC fetch read-only từ Sheet human "Content: Hiển thị msg" 1612–1678) |
| Ngày review | 2026-06-26 |
| Version TCs | v1 (fetch từ Redmine Link TCs) |
| Vòng review | Round 1 |

> **Spec reference**: Không có `02-spec-reference.md` riêng — dùng `templates/LME-SYSTEM-SPEC.md` tổng (feature Template / Send message / Chat 1:1). Ghi note theo quy trình.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER + nhiều MAJOR, cần fix và review lại.

**Lý do ngắn gọn**: Bộ TC bám sát flow "edit action template → gửi lại" nhưng **(a)** không cover được yếu tố cốt lõi của root cause mới nhất (**cửa sổ cache 30s** — bug chỉ tái hiện khi update + gửi lại TRONG 30s); **(b)** thiếu hoàn toàn nhánh **Scenario/step_message** (F2) và **cross-invalidation template→action+step_message** (T3) — đều là impact Direct/High; **(c)** ticket có **2 root cause khác nhau cho cùng 1 triệu chứng** (cache 30s vs `array_diff` 1 chiều) nhưng TC chỉ phủ 1 hướng; **(d)** input auto-fill chưa được tester verify, mục 3 dev-impact trống.

---

## 2. Tóm tắt cho member

Bộ TC làm tốt **bug ②** (ký tự `&` full/half-width, HTML special chars, JP — 8 case khá đầy đủ) và có cấu trúc test ma trận tốt cho **bug ①** trên cả 3 kênh send (web / job / app). Tuy nhiên điểm chí mạng: root cause mới nhất là **cache source_message sống 30s**, nên mọi TC verify bug ① **bắt buộc phải nói rõ "gửi lại trong vòng 30s"** — hiện không TC nào ghi điều này, dễ test xong ra OK giả (cache tự hết hạn). Ngoài ra thiếu nhánh **Scenario (step_message)** và case **1 template dùng chung cho cả action lẫn step_message** — đúng phần Dev nói là rủi ro cao nhất. Cần bổ sung trước khi nhận test thật.

---

## 3. Coverage Matrix

> TC trong Sheet không có TC ID — map theo nhóm/case. Impact lấy từ `03-dev-impact.md` (bản chính #123773) + BUG① / BUG② từ `01`.

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG① — template action không hiện ở chat 1:1 (root cause cache 30s) | Fix | High | Nhóm 1: edit/thêm/xóa/sort/edit nội dung template con → gửi (web/job/app) | nhiều | **RISK** — không TC nào nêu **cửa sổ 30s**; thiếu nhánh scenario |
| BUG② — tên template `&` half-width hiển thị sai | Fix | Medium | Nhóm 2: full-width / half-width / mixed / HTML special / JP (8 case) | 8 | **RISK** — cover hiển thị tốt, NHƯNG bug② không có trong dev-impact chính #123773 → fix shape chưa verify được (xem §3.5 + 4) |
| F1 — ActionSourceMessageCache | Function | Direct | Nhóm 1 "Send action template bởi web/job" (edit→gửi) | nhiều | **RISK** — thiếu yếu tố timing 30s + thiếu test socket clear-cache thực sự fire |
| F2 — ScenarioSourceMessageCache | Function | Direct | — | **0** | **GAP** — range TC không có case nào gửi **scenario / step_message** |
| F3 — TemplateSourceMessageCache | Function | Direct | Nhóm 1 "Edit nội dung template con → gửi"; nhóm "kết hợp nhiều thao tác" | nhiều | **RISK** — không có case **template dùng chung cho action + step_message** (cross-invalidation) |
| D1 — (không có data update, chỉ clear cache) | Data | — | N/A | — | N/A |
| T1 — update rồi gửi lại **trong 30s** → chat 1:1 hiện đúng | Feature | High | Nhóm 1 (edit→gửi) | nhiều | **RISK** — thiếu mệnh đề "trong 30s" tường minh |
| T2 — KHÔNG update, gửi lại vẫn bình thường (regression) | Feature | Medium | "Verify refresh chat"; "Giữ nguyên các template con → send" | 2–3 | **RISK** — chưa có case gửi lại **sau khi cache hết hạn (>30s)** |
| T3 — update **template** → clear cache cả **action + step_message** | Feature | High | "kết hợp nhiều thao tác cùng lúc" (chỉ action) | ~1 | **GAP** — không verify lan sang step_message/scenario |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| Nhóm 2 (8 case `&`/half-width) | Hiển thị tên Template chứa `&` & half-width | Map **BUG②** (báo cáo KH) nhưng **KHÔNG map** F/D/T nào trong dev-impact chính #123773 (bản này không xử lý bug②) | **Giữ** (cover BUG②) — nhưng xác nhận với Dev fix bug② có nằm trong release đang test không; nếu không → tách ticket. |

> Không có ORPHAN dạng "lạc chủ đề / thừa" — toàn bộ TC đều thuộc scope BUG①/BUG②.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact #123773) | **Cache (invalidation)** — "job cache source_message 30s", "web khi update action/template/step_message **socket cho job để clear cache**" |
| Trigger space cần cover | (1) update **action** + gửi lại **trong 30s**; (2) update **template** + gửi lại trong 30s; (3) update **step_message/scenario** + gửi lại trong 30s; (4) **1 template dùng chung** cho action & step_message → update template phải clear cả 2; (5) regression: gửi lại **sau >30s** (cache tự hết hạn) vẫn đúng; (6) regression: **không update**, gửi lại bình thường; (7) race: update (socket clear-cache) **gần như đồng thời** với resend |
| Số trigger TCs hiện cover | **~2/7** — chỉ phủ (2) update template-action + (6) không update. Thiếu rõ ràng (1) timing-30s tường minh, (3) scenario, (4) cross-invalidation, (5) sau-30s, (7) race |
| KH report dạng | **Symptom-only** — KH chỉ thấy "template không hiển thị trên chat 1:1 admin (điện thoại vẫn nhận)", không nêu root cause |
| Alternative root causes cần verify | **CÓ — đã tồn tại thật trong ticket**: (a) cache source_message 30s (#123773, bản đang fix); (b) `array_diff` so sánh capture template **1 chiều** → reuse source_messages cũ thiếu capture khi danh sách mới là superset (cũ ⊂ mới) (#122460 AI auto-fix). Cùng 1 triệu chứng, 2 root cause → TC phải cover cả hướng (b): "**thêm template con mới rồi gửi lại**" |
| Anti-patterns dính | **AP-2** (symptom-only, 2 root cause); **AP-6** (mục 3 caller trống); một phần **AP-3** (regression T2 chỉ happy-path, thiếu edge >30s); **AP-4** (chưa chắc fix nào deploy — cache-clear #123773 hay symmetric-diff #122460) |

> Trigger space cover **2/7** < tổng → flag [BLOCKER] FIX-SHAPE ở §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE — GAP-1 (cửa sổ cache 30s)**: Root cause là cache source_message **sống 30s**; bug chỉ tái hiện khi **update + gửi lại TRONG 30s**. Không TC nào nêu ràng buộc timing này → tester rất dễ thao tác chậm (>30s, cache tự hết hạn) và kết luận **OK giả**. — *Fix*: mọi TC verify bug① phải thêm precondition/step **"gửi lại trong vòng < 30s kể từ lúc save"**, và bổ sung 1 TC đối chứng "gửi lại sau > 30s" (xem TC-NEW-01, TC-NEW-04).
- **[BLOCKER] GAP-2 (F2 ScenarioSourceMessageCache)**: Dev liệt kê `ScenarioSourceMessageCache` là function Direct impact nhưng **không có TC nào gửi scenario/step_message** trong range. — *Fix*: thêm TC gửi step_message của scenario sau khi edit (TC-NEW-02).
- **[BLOCKER] GAP-3 (T3 cross-invalidation template→action+step_message)**: Dev nhấn mạnh "update template phải clear cache cả action & step_message vì template dùng chung". Không có TC nào dựng **1 template được dùng đồng thời trong action VÀ step_message** rồi verify cả 2 kênh cập nhật. Đây là nhánh rủi ro cao nhất Dev tự nêu. — *Fix*: TC-NEW-03.
- **[BLOCKER] FIX-AMBIGUITY**: Đang tồn tại **2 bản fix với 2 root cause khác nhau** cho bug①: cache-clear (#123773, branch `m_202606_clear-cache-sourcemessage_37831`) và symmetric-diff `array_diff` (#122460, branch `ai_fixbug_37831`). Chưa rõ bản nào được deploy lên môi trường test. Nếu test sai bản → coverage matrix vô nghĩa. — *Fix*: Leader xác nhận với Dev branch/commit đang deploy **trước khi** giao test; nếu cả 2 cùng merge thì cần TC cho cả 2 root cause.

### 4.2 Major (nên fix)

- **[MAJOR] SYMPTOM-ONLY (AP-2) — GAP-4**: KH report symptom-only và ticket có **2 plausible root cause** cùng tạo triệu chứng "chat 1:1 hiện template cũ". TC hiện chỉ phủ hướng cache. Cần bổ sung hướng **"thêm template con MỚI (danh sách capture mở rộng, cũ ⊂ mới) rồi gửi lại"** để bắt root cause `array_diff` 1 chiều. — *Fix*: TC-NEW-05.
- **[MAJOR] AUTO-FILL CHƯA VERIFY (file 01)**: `01-bug-task.md` có `Auto-filled: 2026-06-26 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** → mô tả bug/steps có thể chưa được kiểm chứng. — *Fix*: tester đọc lại Redmine #37831 + 2 ảnh đính kèm, tick checkbox.
- **[MAJOR] AUTO-FILL CHƯA VERIFY (file 03)**: `03-dev-impact.md` `Auto-filled` chưa được tester tick → mapping F/D/T có thể chưa đủ. — *Fix*: tester verify + tick.
- **[MAJOR] AP-6 — Mục 3 dev-impact trống**: "Đã check và sửa các function caller" để trống → có thể còn function khác cùng pattern cache chưa được clear (vd: remind, broadcast, autoreply cũng dùng source_message cache?). — *Fix*: yêu cầu Dev list caller đã check; nếu có nguồn send khác dùng chung cache → mở rộng regression scope (C.2 — 12 nguồn job + 7 nguồn web).
- **[MAJOR] BUG② FIX-SHAPE chưa verify được**: Bug② (`&` half-width) chỉ được xử lý trong AI auto-fix #122460 (escaping `@json` ở 3 màn), **không có** trong dev-impact chính #123773. AI auto-fix còn cảnh báo "tên template từng bị lưu lặp `&amp;amp;` cần sửa lại 1 lần". Bộ TC nhóm 2 chỉ verify **hiển thị**, chưa verify **không double-encode khi LƯU**. — *Fix*: TC-NEW-06 + xác nhận bug② có deploy không.
- **[MAJOR] AP-3 — Regression T2 thiếu edge**: T2 (gửi lại không update) chỉ có "Verify refresh chat" happy-path; thiếu case **gửi lại sau khi cache hết hạn tự nhiên (>30s)** và case **reload trang chat sau khi clear cache**. — *Fix*: TC-NEW-04.
- **[MAJOR] Kết quả test sẵn có cho thấy regression chưa đóng**: Trong chính bộ TC, nhánh **"Thay đổi thứ tự template con → gửi" (Send action template bởi JOB)** đang **NG** (3 dòng) + liên kết **Bug Tester #37907**. Sort→gửi qua job vẫn lỗi ⇒ fix có thể chưa cover thao tác **sort** (chỉ cover add/edit nội dung). — *Fix*: xác nhận #37907 quan hệ với #37831; thêm TC sort→gửi trong 30s cho cả 3 kênh và đảm bảo pass trước khi approve.

### 4.3 Minor (có thể fix sau)

- **[MINOR]** TC trong Sheet **thiếu Expected tường minh** ở nhiều dòng (cột Expected trống, dựa vào merge của dòng đầu nhóm) → 2 tester có thể hiểu khác nhau. Nên ghi Expected cụ thể: "Chat 1:1 hiển thị nội dung template **mới nhất**, khớp 100% với nội dung phía LINE user".
- **[MINOR]** Đa số TC nhóm 1 (web) đang ở trạng thái "Test Bug" (chưa test) → version submit chưa có kết quả; cần chạy thực tế sau khi chốt fix.
- **[MINOR]** Thiếu Precondition rõ về **gói cước/account** và **tag/folder dùng để add action** (tham chiếu đúng case KH: tag `❌️面談｜不合格`, filter Lancers tag).

### 4.4 Nit (gợi ý)

- **[NIT]** Có thể gộp 3 khối web/job/app thành ma trận "kênh × thao tác" để tránh lặp 3 lần cùng case; thêm cột đánh dấu case nào bắt buộc "trong 30s".
- **[NIT]** Bổ sung CL-Func-23 (test cả template **có group** và **không group**) ngay tại tiêu đề nhóm để member không sót — hiện chỉ có 1 dòng "Check template đơn".

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` (hoặc Sheet) ở round tiếp theo. Đã viết theo góc nhìn manual tester (quan sát trên màn chat 1:1 / phía LINE user).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Cache 30s: edit action template rồi gửi lại **trong 30s** → chat 1:1 hiện nội dung mới | Tag A có action gửi template T (group). Friend F chưa add tag A. | 1. Add tag A cho F (lần 1) → F nhận T.<br>2. Vào edit nội dung 1 template con của T → Save.<br>3. **Trong vòng < 30s** kể từ lúc Save: remove rồi add lại tag A cho F (trigger gửi lại). | Màn chat 1:1 admin hiển thị **nội dung T mới nhất**, khớp với nội dung phía LINE user. (Trước fix: chat 1:1 hiện nội dung cũ.) | High | Positive (BUG①) | BUG①, F1, F3, T1 |
| TC-NEW-02 | Scenario step_message: edit template trong step rồi gửi lại trong 30s → chat 1:1 đúng | Scenario S có 1 step gửi template T. Friend F trong điều kiện trigger step. | 1. Trigger step gửi T cho F.<br>2. Edit nội dung T (hoặc step_message) → Save.<br>3. Trong < 30s: trigger lại step gửi cho F. | Chat 1:1 hiển thị nội dung step_message mới nhất (ScenarioSourceMessageCache đã được clear). | High | Positive (Regression) | F2, T3 |
| TC-NEW-03 | Cross-invalidation: 1 template dùng chung cho **action + step_message**, edit template → cả 2 kênh cập nhật | Template T được dùng đồng thời trong action của tag A và trong 1 step của scenario S. | 1. Gửi qua action (add tag A) và qua step scenario S cho F → ghi nhận nội dung.<br>2. Edit nội dung T → Save.<br>3. Trong < 30s: gửi lại qua **cả** action A **và** step S. | Chat 1:1 hiển thị nội dung T mới ở **cả** tin từ action **lẫn** tin từ step_message (update template clear cache cho cả ActionSourceMessageCache & ScenarioSourceMessageCache). | High | Positive (Regression) | F3, T3 |
| TC-NEW-04 | Regression: gửi lại **sau > 30s** (cache tự hết hạn) và case không update | Tag A có action gửi template T. | 1. Add tag A cho F → nhận T.<br>2. **Không** edit gì, đợi > 30s, add lại tag A.<br>3. Lặp với có-edit nhưng gửi lại sau > 30s. | Cả 2 case chat 1:1 hiển thị đúng nội dung hiện tại của T (không regress hành vi cũ khi cache đã hết hạn tự nhiên). | Medium | Regression | T2 |
| TC-NEW-05 | Alternative root cause: **thêm template con mới** (danh sách capture mở rộng) rồi gửi lại → chat 1:1 đủ nội dung | Tag A có action gửi template group T gồm 1 template con. | 1. Add tag A cho F → nhận T (1 con).<br>2. **Thêm** template con thứ 2 (và 3) vào T → Save.<br>3. Add lại tag A cho F. | Chat 1:1 hiển thị **đầy đủ** các template con (kể cả con mới thêm). (Bắt root cause `array_diff` 1 chiều: cũ ⊂ mới.) | High | Negative/Boundary (BUG① alt) | BUG①, F1 |
| TC-NEW-06 | Bug②: lưu tên template chứa `&` half-width **không bị double-encode** | Màn tạo/sửa group template. | 1. Đặt tên quản lý template = `A&B` (half-width).<br>2. Save → mở lại màn chi tiết → Save lần 2 → mở lại.<br>3. Kiểm tra list + detail + chat 1:1 (nếu hiển thị tên). | Tên luôn hiển thị `A&B`, **không** biến thành `&amp;` hay `&amp;amp;` sau nhiều lần lưu (verify cả hiển thị lẫn giá trị lưu DB không mã hoá lặp). | Medium | Boundary (BUG②) | BUG② |
| TC-NEW-07 | Sort template con → gửi lại trong 30s (đóng regression #37907) | Tag A action gửi template group T ≥ 3 con. | 1. Add tag A → nhận T.<br>2. Đổi thứ tự template con → Save.<br>3. Trong < 30s: gửi lại qua **cả 3 kênh** (web/job/app). | Chat 1:1 + LINE user hiển thị đúng **thứ tự mới**. (Hiện nhánh job đang NG — Bug Tester #37907.) | High | Regression | F1, T1 |
| TC-NEW-08 | Race: update (socket clear-cache) gần đồng thời với resend / multi-tab | 2 tab admin mở cùng template T. | 1. Tab A đang gửi lại template cho F.<br>2. Gần như đồng thời Tab B edit T → Save (bắn socket clear-cache).<br>3. Quan sát kết quả chat 1:1. | Không hiển thị nội dung cũ "kẹt" do race giữa socket clear-cache và resend (tham chiếu CL-Func-25 concurrent / response không theo thứ tự). | Medium | Boundary | F1, T1 |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec
- [ ] Cần update spec

> Ghi chú: hành vi "chat 1:1 admin hiển thị đúng nội dung template mới nhất" là **đúng kỳ vọng** sẵn có, không phải đổi spec. Chỉ là sửa lỗi cache. Tuy nhiên đề nghị PM ghi nhận **giới hạn vận hành**: tin gửi TRƯỚC khi deploy (đã lưu source_message cũ thiếu nội dung) sẽ không tự hiện lại (theo cảnh báo Dev/AI) — KH cần được thông báo.

---

## 7. Checklist đã chạy

- [x] A. Coverage — **FAIL** (GAP F2/T3, RISK F1/F3/T1/T2)
- [x] B. Chất lượng từng TC — Expected nhiều dòng trống (MINOR)
- [x] C. Chất lượng bộ TC tổng thể — thiếu nhánh scenario, thiếu race/concurrent
- [x] D. Spec alignment — OK (không mâu thuẫn spec)
- [x] E. Hành chính — TC fetch read-only, chưa có tester ký/version (chấp nhận với nguồn fetch)
- [x] F. Base checklist LME
  - [x] F.1 Web — **CL-Func-23** (template có/không group): cover một phần (chỉ "template đơn"). **CL-Func-25** (multi-tab/concurrent, response không theo thứ tự): **MISS** → TC-NEW-08. **CL-Func-2/3** (reload/chuyển tab): cover một phần qua "Verify refresh chat".
  - [x] F.2 Job — **B (job send)**: có nhánh "Send action template bởi job" nhưng đang có case NG (#37907). Không chạm Google sync (CLJ01 N/A).
  - [x] F.3 Tính năng chung — **C.2 Send message** là tâm điểm: cần phủ "trigger hiển thị trên chat 1:1 web + app" (có), "send template 2 case group/không group" (CL-Func-23, một phần), và rà các nguồn send khác dùng chung source_message cache (liên quan mục 3 trống). C.8 Sort: liên quan trực tiếp case NG #37907.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
