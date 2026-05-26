# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | KH #36365 (回答ID 10833) |
| Reviewer (Leader) | _<điền>_ |
| Tester được review | _<chưa rõ — Sheet không có cột Assignee fill>_ |
| Ngày review | 2026-05-13 |
| Version TCs | v1 (sheet `Testcase` rows 965-973) |
| Vòng review | Round 1 |

> **Note đầu vào**:
> - **Input thiếu**: MCP Redmine fetch fail (env vars chưa load) → `01-bug-task.md` suy luận từ dev report trên sheet, **chưa verify nguyên văn Redmine 36365**. Tester verify lại trước khi review final.
> - **Spec reference**: Không có spec riêng — fallback `templates/LME-SYSTEM-SPEC.md`.
> - **Format file 04**: Sheet dùng nested checklist (Main / Sub1-5 / Expected / Note), KHÔNG phải 10-column TC list chuẩn. Đã convert best-effort thành 7 TCs (TC-01 → TC-07). TC-02→TC-06 + TC-07 có cell rỗng vì sheet visual inherit.

---

## 1. Verdict

- [ ] **APPROVED**
- [x] **APPROVED WITH CHANGES** — Approve sau khi member bổ sung **6 TC** (positive + regression + DB-state + reload + edit-step + notify-chatwork) ở §5 + fix 3 vấn đề chất lượng (Expected rỗng / Note ambiguous / TC-07 incomplete). Có thể không cần review lại Round 2 nếu member fix đầy đủ.
- [ ] REJECTED

**Lý do**: Bộ TC v1 đã làm tốt phần **matrix negative case** (3 loại step × 2 trạng thái filter = 6 TCs), cover được flow KH gốc ở TC-03. **Tuy nhiên thiếu**: (1) Positive happy regression sau fix (tạo step với filter còn tồn tại → ok), (2) Regression send lifecycle (scenario chạy step → KHÔNG duplicate — đây là bug gốc), (3) DB state verify sau fail, (4) Reload behavior theo msg JP, (5) Edit step (`updateScenarioStep` có cùng vấn đề?), (6) Notify chatwork sau khi xóa try/catch.

---

## 2. Tóm tắt cho member

Bộ TC em viết gọn và bám sát flow KH — matrix 3 loại step (send ngay / sau ngày / sau giờ) × 2 case (1 filter / 2 filter) đầy đủ, TC-03 reproduce chính xác case KH gốc. **Tuy nhiên thiếu 3 nhóm critical**: (a) **Positive happy** — tạo step với filter còn tồn tại sau fix có thành công không? 6/6 TCs đều là negative, chưa có TC nào catch nếu fix introduce regression "tạo step bị fail luôn vì validate sai". (b) **Regression send lifecycle** — bug gốc là duplicate send, em chỉ test "không có msg gửi khi tạo step fail", chưa có TC verify "scenario chạy step bình thường (filter còn tồn tại) → gửi đúng 1 lần". (c) **Edit step (`updateScenarioStep`)** — dev chỉ list `createScenarioStep` nhưng cần hỏi dev có cùng vấn đề không. Em bổ sung 6 TC ở §5 + fix 3 lỗi chất lượng (Expected rỗng cho TC-02→TC-06, Note ambiguous "bug#36366→36370", TC-07 incomplete) là duyệt.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — Reproduce KH (2 tab, xóa filter tab 1, tạo step "send sau XX giờ" tab 2) | Fix | — | TC-03 (1 filter) + TC-06 (2 filter) — match flow KH | 2 | **OK** |
| **F1** — `createScenarioStep` | Function | Direct | TC-01..06 (test negative validation) — **thiếu positive happy + DB state verify** | 6 | **RISK** |
| **T1** — Tạo mới step message | Feature | High | TC-01..06 | 6 | **RISK** (thiếu positive + regression send + reload behavior) |
| _Hidden T2_ — **Send message lifecycle** (bug gốc duplicate) | Feature (suy ra) | High | TC-01..06 verify ngầm "không có msg gửi sau fail", **thiếu** verify "không duplicate khi success" | 0 dedicated | **GAP** |
| _Hidden F2_ — `updateScenarioStep` (edit step) | Function (suy ra) | _<chưa rõ>_ | — | 0 | **GAP** (cần verify dev) |
| _Hidden_ — Notify chatwork | Behavior change | Medium | — | 0 | **GAP** |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC-07 | "Check account staff" (row 973) | Row rỗng — chỉ có Main = "Check account staff", các cột khác trống | Bổ sung sub-content (CL1 — staff không phân quyền không access modal scenario; staff phân quyền tạo step được) HOẶC xóa nếu không scope. |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] GAP-1 (Positive happy + DB verify)**: Toàn bộ 6 TCs là Negative (test validation fail). **KHÔNG có TC nào verify**: tạo step với filter còn tồn tại → thành công + DB tạo record `scenario_step` + `scenario_step_time` đúng + line user nhận đúng 1 message. Đây là regression test bắt buộc cho function `createScenarioStep` (F1) — Direct impact. Theo `severity-levels.md`, "GAP coverage cho function Direct impact" = BLOCKER. **Fix**: Bổ sung `TC-NEW-01` + `TC-NEW-09` ở §5.

- **[BLOCKER] GAP-2 (Send message lifecycle — regression bug gốc)**: KH bug là "ステップ配信 gửi 2 lần (duplicate)". TCs hiện tại verify "không có msg gửi khi step fail" — đây là check phụ. **Thiếu**: TC verify "scenario chạy step với filter còn tồn tại → message gửi đúng 1 lần, KHÔNG duplicate ở mốc time `01時間00分後` (và các mốc khác)". Đây chính là verify bug gốc đã fix. **Fix**: Bổ sung `TC-NEW-02` ở §5.

- **[BLOCKER] TC-02, TC-03, TC-05, TC-06 Expected rỗng**: Sheet visual inherit từ TC-01 / TC-04 → khi tester khác chạy hoặc khi reorder/remove dòng → mất context. 4/6 TC core không có expected rõ ràng → không reproducible. **Fix**: Member ghi đầy đủ Expected vào mỗi row (sheet) hoặc convert sang format 10-column standalone.

### 4.2 Major (nên fix)

- **[MAJOR] GAP-3 (Edit step — `updateScenarioStep`)**: Dev report chỉ list `createScenarioStep`. Function `updateScenarioStep` (edit step đã tồn tại trong scenario) có thể có cùng vấn đề filter check khi edit + filter bị xóa. **Fix**: Verify với dev — nếu có bug tương tự, bổ sung `TC-NEW-04` (edit step với filter đã xóa).

- **[MAJOR] GAP-4 (Reload behavior theo msg JP)**: Msg `フィルターが削除されたため、画面を再読み込みしてください` hướng dẫn user reload. Cần TC verify: sau khi user reload, GUI load fresh list filter (filter đã xóa biến mất khỏi dropdown) → user chọn filter còn lại hoặc tạo filter mới → tạo step thành công. **Fix**: Bổ sung `TC-NEW-06`.

- **[MAJOR] GAP-5 (CL11 — Cross-staff filter delete)**: Bug context là multi-tab cùng user. Edge case quan trọng: staff A đang tạo step, staff B (cùng bot, có quyền edit filter) xóa filter → A submit → behavior? CL11 LME yêu cầu CRUD đúng account context. **Fix**: Bổ sung `TC-NEW-05`.

- **[MAJOR] GAP-6 (CL5 Double click submit)**: Button submit tạo step có check double click chưa? Nếu user double-click rapid → có thể tạo 2 step duplicate ngay cả khi filter còn tồn tại. Đây là duplicate-prevention regression test. **Fix**: Bổ sung `TC-NEW-07`.

- **[MAJOR] GAP-7 (Notify chatwork — behavior change)**: Dev report mention "Xóa try/catch để notify chatwork". Đây là **behavior change** cần TC verify: khi exception xảy ra (filter đã xóa) → chatwork channel nhận notify đúng (với payload bot_id / scenario_id / error message). **Fix**: Bổ sung `TC-NEW-08`.

- **[MAJOR] Note column ambiguous**: TC-02 → TC-06 Note ghi "bug#36366" → "bug#36370". Không rõ ý nghĩa:
  - Nếu là **bug ID Redmine** mới (5 bug related): cần verify với member tickets đã tạo chưa, có ảnh hưởng scope review không.
  - Nếu là **TC ID member tự đặt**: dùng format trùng với bug Redmine → confusing, dễ nhầm. Đề nghị đổi sang format `TC-36365-01` hoặc `TC-01`...
  - **Fix**: Member confirm với Leader trước khi push sheet master.

- **[MAJOR] Bộ TC mất cân đối Positive/Negative/Boundary/Regression**: 6 Negative / 0 Positive / 0 Boundary / 0 Regression. Tỷ lệ chuẩn 30/25/25/20. Bổ sung TC positive + regression như đề xuất §5.

- **[MAJOR] Steps + Precondition sơ sài**: Toàn bộ TC chỉ có 2-3 dòng action ngắn (vd "Tab 1 xóa filter / Tab 2 tạo step"). Thiếu precondition đầy đủ (bot ID, scenario ID, friend test, filter type — basic filter / advanced filter / friend info filter). Thiếu post-condition / cleanup. **Fix**: Mỗi TC phải có Precondition block đầy đủ + Steps numbered list.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Title TC không chứa keyword `createScenarioStep`**: Khó map sang F1. Đề nghị rename `[F1 createScenarioStep][1 filter] Tab 1 xóa filter → Tab 2 tạo step send sau XX giờ — expect error msg JP`.

- **[MINOR] TC ID rỗng**: Sheet không có cột TC ID — tôi tạm gán TC-01 → TC-07. Member fill TC ID chuẩn team trước khi sync sheet master.

- **[MINOR] Status pre-fill "OK" toàn bộ**: 6 TCs đã có cột Note ghi "bug#xxxxx" + cột tận cùng "OK" trước khi test. Đề nghị: Status để empty trước test, fill sau khi run.

- **[MINOR] Format sheet không 10 cột chuẩn**: Sheet dùng nested checklist. Sau khi member fix các blocker, convert sang `04-tc-list.md` chuẩn (10 cột) trước khi sync.

- **[MINOR] DB verify mơ hồ**: TC-01 expected mention "check db: bảng `filter_manage`" — chưa nói verify gì cụ thể (filter có `is_deleted=1`? hay không tồn tại record? hoặc verify `scenario_step.filter_id` không reference filter đã xóa?). **Fix**: Ghi rõ field + giá trị expected.

### 4.4 Nit (gợi ý)

- **[NIT]** Expected có thể tách thành block: (a) UI behavior, (b) DB state (table + field + value), (c) Send queue (`message_send_history` / `scenario_step_time`), (d) LINE user receive — giúp tester check từng layer.

- **[NIT]** Có thể thêm TC mobile/responsive: modal tạo step hoạt động trên Android/iOS web hoặc app admin không (CL Compatibility).

- **[NIT]** Đề xuất thêm matrix variant filter type: basic filter / friend info filter / tag filter — vì `filter_manage` có thể support nhiều loại filter, behavior validate có thể khác.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Tất cả TC phải có Precondition + Steps đầy đủ.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| **TC-NEW-01** | `createScenarioStep` happy — tạo step với filter còn tồn tại, send sau XX giờ | (1) Bot test có 1 scenario active.<br>(2) Tạo 1 filter manager (basic filter) trong scenario đó. | 1) Mở modal tạo step trong scenario<br>2) Chọn loại "send sau XX giờ", nhập `01 giờ 00 phút`<br>3) Chọn filter vừa tạo<br>4) Submit | (a) Tạo step **thành công**, modal đóng<br>(b) Step hiển thị trong list step của scenario<br>(c) DB `scenario_step`: có record mới với `filter_id` đúng, `start_time = 01:00`<br>(d) Không có msg lỗi JP | High | Positive | F1, T1, BUG |
| **TC-NEW-02** | Regression send — scenario chạy step với filter còn tồn tại → message gửi đúng 1 lần (NOT duplicate) | (1) Setup TC-NEW-01 (đã tạo step send sau 1 giờ với filter).<br>(2) Friend test "さや" match filter, đang start scenario.<br>(3) Mock time hoặc chờ đủ 1 giờ. | 1) Chờ tới mốc time 01時間00分後<br>2) Quan sát LINE app của friend "さや"<br>3) Check DB `message_send_history` filter theo `scenario_step_id` + `friend_id` | (a) LINE friend "さや" nhận đúng **1 message** ở mốc 01時間00分後<br>(b) DB `message_send_history` chỉ có 1 record cho step này<br>(c) `scenario_step_time.send_time` cập nhật đúng, `is_send = 1` | High | Regression | T1, BUG, C.2 |
| **TC-NEW-03** | TOCTOU race — filter bị xóa giữa thời điểm check và insert | (1) 2 tab cùng login, cùng bot.<br>(2) 1 filter manager active. | 1) Tab 2: mở modal tạo step, chọn filter, nhập step info nhưng **chưa submit**<br>2) Tab 1: xóa filter<br>3) Tab 2: submit ngay (dev/QA simulate race nếu cần) | (a) Tab 2 submit fail → msg JP `フィルターが削除されたため、画面を再読み込みしてください`<br>(b) DB không có scenario_step orphan<br>(c) Chatwork nhận notify exception (nếu race trúng) | Medium | Boundary | F1, T1 |
| **TC-NEW-04** | `updateScenarioStep` — Edit step đã tồn tại, filter bị xóa | (1) Scenario có step active với filter X.<br>(2) Mở 2 tab edit cùng step. | 1) Tab 1: xóa filter X<br>2) Tab 2: edit step (thay đổi message body hoặc time), submit | (a) Submit fail → msg JP tương tự<br>(b) DB step KHÔNG bị update<br>(c) **Hoặc** nếu dev không fix `updateScenarioStep` → flag BUG mới | High | Negative | F1 (+`updateScenarioStep`), T1 |
| **TC-NEW-05** | Cross-staff filter delete (CL11) | (1) Bot test có 2 staff A và B (cả 2 có quyền edit scenario + filter).<br>(2) 1 filter active. | 1) Staff A login tab 1, mở modal tạo step<br>2) Staff B login tab 2 (browser khác), xóa filter đó<br>3) Staff A submit tạo step | (a) Staff A submit fail → msg JP<br>(b) Verify chỉ filter của bot này bị ảnh hưởng, filter của bot khác không bị ảnh hưởng | Medium | Negative | F1, T1, CL11 |
| **TC-NEW-06** | Reload theo hướng dẫn msg JP — load fresh state | (1) Setup TC-01 (đã fail tạo step do filter xóa).<br>(2) User đang ở modal/màn với msg JP hiển thị. | 1) User reload page (F5)<br>2) Mở lại modal tạo step<br>3) Quan sát dropdown filter<br>4) Chọn filter còn lại (hoặc tạo mới) → submit | (a) Sau reload, dropdown filter KHÔNG còn filter đã xóa<br>(b) Tạo step với filter còn lại thành công<br>(c) GUI không còn cảnh báo msg JP | High | Positive | F1, T1, CL2 |
| **TC-NEW-07** | CL5 — Double click submit tạo step | (1) 1 scenario + 1 filter active. | 1) Mở modal tạo step, fill info<br>2) Click button submit **2 lần liên tiếp** rapid | (a) Chỉ tạo **1 step** trong DB, KHÔNG duplicate<br>(b) Hoặc button được disable sau click đầu | Medium | Boundary | F1, T1, CL5 |
| **TC-NEW-08** | Notify chatwork khi exception (sau remove try/catch) | (1) Setup tạo race: filter sẽ bị xóa giữa các bước.<br>(2) Chatwork channel debug có người watch. | 1) Tạo race condition trigger validate fail (TC-NEW-03)<br>2) Sau khi user nhận msg JP → check chatwork channel | (a) Chatwork channel có message notify với context: bot_id, scenario_id, error message, stack trace<br>(b) Format notify đúng convention team (verify với dev) | Medium | Functional | F1, Behavior change |
| **TC-NEW-09** | DB state verify sau tạo step fail (filter xóa) | (1) Setup TC-01 trước khi submit fail.<br>(2) Note count records trước. | 1) Submit tạo step → fail msg JP<br>2) Query DB sau fail:<br>  - `SELECT COUNT(*) FROM scenario_step WHERE filter_id = <filter_xoa_id>`<br>  - `SELECT COUNT(*) FROM scenario_step_time WHERE filter_id = <filter_xoa_id>`<br>  - `SELECT COUNT(*) FROM message_send_history WHERE scenario_step_id IN (<step_id mới>)` | (a) Cả 3 query đều return **0 record mới** (không có record orphan)<br>(b) Count tương tự trước submit, không tăng | High | Negative (DB state) | F1, T1 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - **Section**: `templates/LME-SYSTEM-SPEC.md` — Scenario / Step message → Modal tạo step → Filter manager
  - **Nội dung cần update**:
    1. Bổ sung validation rule: "Server **MUST** validate `filter_id` còn tồn tại (`filter_managers` table, không bị soft-delete / hard-delete) trước khi insert `scenario_step`. Nếu không tồn tại → return error + msg `フィルターが削除されたため、画面を再読み込みしてください`."
    2. Định nghĩa lifecycle filter khi đang in-use (có cảnh báo trước khi xóa? Hay xóa silent?).
    3. Notify chatwork rule khi exception xảy ra.
  - **Người chịu trách nhiệm update**: Dev assignee + PM.
  - **Câu hỏi cần dev clarify** (impact direct lên TCs):
    1. Validate ở layer nào (controller / service / model)? Có dùng DB transaction để giảm TOCTOU race?
    2. Filter có soft-delete hay hard-delete? Logic check dùng `WHERE id = ?` hay `WHERE id = ? AND is_deleted = 0`?
    3. `updateScenarioStep` có cùng validation chưa?
    4. Có cascade behavior khi xóa filter trong khi có step đang dùng?
    5. Notify chatwork payload chính xác là gì?

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — RISK: thiếu positive happy + send regression + edit step + DB verify
- [x] **B. Chất lượng từng TC** — FAIL: 4/6 TC có Expected rỗng (inherit), thiếu Precondition đầy đủ, Steps sơ sài
- [x] **C. Chất lượng bộ TC** — FAIL: Ratio 0/6/0/0 (Positive/Negative/Boundary/Regression)
- [x] **D. Spec alignment** — Flag spec update (mục 6)
- [x] **E. Hành chính** — FAIL: TC ID rỗng, Assignee rỗng, Status pre-fill OK, Note column ambiguous, format sheet không 10 cột
- [x] **F. Base checklist LME**:
  - [ ] **F.1 Checklist web** — chưa cover: CL2 (reload sau save), CL5 (double click submit), CL11 (CRUD đúng account context), CL18 (load + submit sau — phần đã có ngầm qua multi-tab, nhưng reload behavior thiếu)
  - [x] **F.2 Checklist job** — N/A (task không chạm job sync)
  - [ ] **F.3 Các tính năng chung** — chưa cover **§C.2 Send message** (regression bug gốc duplicate send) — đây là gap critical

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | 2026-05-13 |
| Tester | (đã đọc & hiểu feedback) | |
