# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38428` — [AI][Bug Exception] Trying to get property '..' of non-object (FormAnswerService.php:171) |
| Reviewer (Leader) | `<Test Leader — verify draft này>` |
| Tester được review | **`AI`** (LME TEST STUDIO job #578) — task added by `ngannt` |
| Ngày review | `2026-08-25` |
| Version TCs | `round 1` (Studio), toàn bộ TC `status = draft`, `version = 1` |
| Vòng review | `Round 1` |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO task #194** (nguồn 1 — mặc định) |
| Ticket · task_id · round · branch | `38428` · `#194` · round `1` · `ai_fixbug_38428` |
| Thời điểm fetch | `2026-08-25` (task_list + testcase_list + task_get_context + **task_get_report** + review_list_comments) |
| Tổng số TC review | **12** |
| File 04 trong repo vs Studio | **Khớp** — file 04 được sinh từ chính Studio task #194 trong cùng session (12/12 TC, `temp_id` NEW-1→NEW-12 trùng khớp). **Không** có STALE-INPUT. |
| Comment vòng review trước | `review_list_comments(194)` → **rỗng** — đây là vòng review đầu tiên, không có issue cũ đã đóng cần tránh raise lại |

### Cảnh báo bắt buộc từ metadata Studio

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | **11/12 pass (91.7%)** · 0 fail · 0 skip · 0 error · **1 chưa chạy** | `OK` (≥ 80%) — nhưng xem #3/#4 |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **Không có TC fail/error.** `bug_tickets` rỗng 12/12, `openBugs = 0` | `OK` |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | **PROD 0 · STAGING 0 · DEV 0 · LOCAL 11** (run #450, 2026-08-24 11:18→11:59). TC production duy nhất (`TC-RULE04-01`) **chưa chạy** | **`[MAJOR]`** |
| 4 | Ai chạy (`last_exec.source` / `by`) | **100% `source = ai`, `by = pipeline`.** `task_get_report` xác nhận `manual.results = []`, `manual.totals` tất cả `0` — **KHÔNG có một lần chạy tay nào của người** | **`[MAJOR]`** |
| 5 | Tác giả TC (`author` / `provenance.source`) | **100% `author = AI`**, `provenance.source = ai`, `created_job_id = 578`; `toolWritten` human = 0. `reviewState = tester`, `reviewed = false` (chưa `done`) | **`[MAJOR]`** |
| 6 | Mã quan điểm Studio KHÔNG có trong `checklist-lme.md` | **6 mã / 6 lượt TC**: `API-001`, `API-CONTRACT-001`, `TOOL-KNOW-002`, `TOOL-OLDREC-001` (không thuộc tầng 1) + `RULE-01`, `RULE-04` (là **RULE**, không phải mã quan điểm) | **`[MINOR]`** — 6 TC này không được tính là cover ở §7 F.1 |

**Bổ sung từ `task_get_report`** (không có trong `testcase_list`, là dữ liệu quyết định của review này):

- **`artifacts: []` cho cả 11/11 kết quả** → **evidence rỗng tuyệt đối**, vi phạm **RULE-02**.
- **Độ phủ spec do chính Studio tự chấm: `covered 0 / partial 12 / none 0`** — Studio **không** coi TC nào là phủ đủ. Dòng writeback về Redmine cũng ghi *"Độ phủ spec: 0/12 covered"*.
- **`durationMs` cho thấy cách chạy thật**: `TC-FUNC001-02` (**734 ms**) và `TC-TOOLKNOW002-01` (**288 ms**) chạy ở tầng HTTP, không mở browser thật (đối chiếu: TC browser thật mất 7 700–19 700 ms). **Đây KHÔNG phải issue** — màn form công khai là **code không bị chạm** trong lần fix này, kiểm ở tầng HTTP là đủ để chứng minh query tìm được trang. Chỉ lưu ý nhỏ: Expected ghi *"render đầy đủ trang"* nhưng bằng chứng thu được là HTTP 200 — nên hạ Expected về đúng thứ đo được (xem `[MINOR]` §4.3).
- **`TC-TOOLKNOW002-01` actual ghi `line171Marker=false`** — runner **không xác nhận được** lỗi rơi đúng dòng 171, nhưng TC vẫn được chấm `pass` dù Expected nêu đích danh `FormAnswerService.php:171`.
- **`TC-DATAMIG001-01` actual ghi "Tổng trang lệch hiện có trong DB = 7"** — Dev khai **6**. Con số 7 lại bị chính run này làm nhiễu (`TC-TOOLKNOW002-01` seed thêm bản ghi lệch) ⇒ **không dùng được để ước lượng phạm vi**, và phạm vi production vẫn là ẩn số.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ 12 TC phủ tốt **cơ chế ghi** (saveV3) nhưng **không có một TC nào tái hiện đúng kịch bản của khách/QA** — race 2 tab + nút 「プレビュー」 — tức chính đường trigger sinh ra bug; đồng thời bỏ trống toàn bộ nhóm quan điểm **đồng thời (CONC/SEC-ISO)**, **release không lock maintain** và **xoá/sửa trang khi `bot_id` lệch**. Cộng thêm: 100% kết quả `Đạt` do AI tự chạy tự chấm ở `local`, **0 evidence**, **0 lần chạy tay**, trong khi đây là bug **production** bắt buộc kèm recover data trên production.

---

## 2. Tóm tắt cho member

Bộ TC này mạnh hơn mặt bằng chung ở 3 điểm: **có TC tái hiện bug** (`TC-TOOLKNOW002-01`), **có đối chứng âm** khi recover (`TC-TOOLOLDREC001-01` kiểm form bot B không bị đụng), và **tách riêng tầng API** để chống bypass (`TC-API001-01`) — đây đúng là cách nghĩ mình muốn thấy.

Vấn đề lớn nhất không nằm ở TC nào viết sai, mà ở chỗ **kịch bản thật của bug chưa được test**: QA mô tả bug xảy ra khi mở **2 tab** rồi bấm nhanh nút **「プレビュー」**, còn 12 TC lại chuyển bot **tuần tự** rồi bấm nút Lưu. Hai luồng này đi qua code path khác nhau — guard mới có chặn được luồng プレビュー hay không thì hiện **chưa ai biết**. Kế đến là môi trường: bug bắn từ production `s.lmes.jp` và phải chạy query recover trên production, nhưng 11/12 TC chỉ chạy `local` và TC production duy nhất thì chưa chạy.

Việc cần làm trước vòng 2: bổ sung nhóm TC race 2 tab + プレビュー, chạy lại các TC trục chính **bằng tay trên staging/production kèm evidence**, và chốt với Dev câu hỏi ở §6 (guard trả HTTP 500 hay 403).

---

## 3. Coverage Matrix

> Impact lấy từ [03-dev-impact.md](03-dev-impact.md) §4.1/4.2/4.3. Cột `Exec` = số TC `pass` / tổng TC cover (nguồn Studio run #450).

| Impact | Loại | Priority Dev | TCs cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|---|
| **BUG** — saveV3 ghi đè `form_answer_page.bot_id` bằng `getBotId()` | Fix | — | TC-TOOLKNOW002-01 (tái hiện crash), TC-OUTTRUTH001-01 (kịch bản corruption), TC-DATADB001-01 (không ghi đè) | 3 | 3/3 | **RISK** — cover đúng *cơ chế*, nhưng **không TC nào mô phỏng steps repro thật** (2 tab + プレビュー) → vi phạm checklist **A.1** |
| **F1** — `FormAnswerController::saveV3` | Function | **Direct** | TC-FUNC001-01, TC-DATADB001-01, TC-OUTTRUTH001-01, TC-RULE01-01, TC-APICONTRACT001-01, TC-API001-01, TC-REGSHARED001-01 | 7 | 7/7 | **OK** (đủ Normal + Abnormal + Boundary) — nhưng chỉ ở `local` |
| **F2** — `FormAnswerService::renderFormAnswer` | Function | Indirect | TC-FUNC001-02, TC-TOOLKNOW002-01 | 2 | 2/2 | **OK** — hàm **không bị sửa code**; 2 TC verify hệ quả dữ liệu là đủ. *(Còn 1 điểm nhỏ: `TC-TOOLKNOW002-01` ghi `line171Marker=false` — §4.2)* |
| **F3** — FE `setting_form_items.js` `.done`/`.fail` | Function | Indirect | TC-OUTTRUTH001-01, TC-RULE01-01 | 2 | 2/2 | **RISK** — actual chỉ ghi alert rút gọn 「アカウントが切り替わっている…」, chưa đối chiếu **nguyên văn** message; chưa có TC verify **thao tác lại sau khi reload** (đúng thứ message hướng dẫn user làm) |
| **F4** — `FormAnswerController@8045/8094` xoá trang (lọc `getBotId`) | Function | Indirect *(chưa Dev đánh giá ở bản mới nhất)* | — | **0** | — | **GAP** |
| **F5** — `FormAnswerController::store` (dòng 811) | Function | Không ảnh hưởng | — | 0 | — | **N/A** — Dev khai không ghi DB; **không** tính là GAP (tránh over-test layer không chạm code) |
| **D1** — `form_answer_page.bot_id` (UPDATE không còn ghi đè) | Data | — | TC-DATADB001-01, TC-FUNC001-01, TC-APICONTRACT001-01, TC-REGSHARED001-01 | 4 | 4/4 | **OK** |
| **D2** — `form_answer_page.form_id` (UPDATE không còn ghi đè) | Data | — | TC-FUNC001-01, TC-REGSHARED001-01 (chỉ verify lúc **CREATE**) | 2 | 2/2 | **RISK** — **không TC nào** verify `form_id` **giữ nguyên khi UPDATE** trang (TC-DATADB001-01 chỉ so `bot_id`) |
| **D3** — `form_answer_page.bot_id` data cũ lệch (MIGRATE / recover) | Data | — | TC-DATAMIG001-01, TC-TOOLOLDREC001-01, TC-RULE04-01 *(chưa chạy)* | 3 | 2/3 | **RISK** — recover chỉ chạy `local`; **idempotent / rollback / mẫu dữ liệu cũ nhiều nguồn** chưa test; phạm vi prod chưa biết |
| **D4** — Schema | Data | Không đổi | — | 0 | — | **N/A** |
| **T1** — Form Builder (FA-011), màn `/basic/form-answer/edit/{id}` | Feature | **High** | TC-REGSHARED001-01, TC-FUNC001-01, TC-DATADB001-01, TC-OUTTRUTH001-01, TC-RULE01-01 | 5 | 5/5 | **RISK** — regression chỉ chạy **trạng thái sạch** (`AP-3`): không có form nhiều trang đang lệch `bot_id`, không có form ở trạng thái biên (0 trang / max trang) |
| **T2** — Màn trả lời biểu mẫu công khai `/form-answer/{unique_key}` | Feature | **High** | TC-FUNC001-02, TC-TOOLKNOW002-01, TC-TOOLOLDREC001-01 | 3 | 3/3 | **RISK** — đủ chiều về **code** (màn này không bị sửa, chỉ đọc dữ liệu). Rủi ro còn lại thuần về **dữ liệu + môi trường**: cả 3 TC dùng bản ghi tự seed trên `local`, chưa có bản ghi lệch **thật trên production** nào được mở lại sau recover |
| **T3** — Xoá / sửa trang của form khi `bot_id` lệch | Feature | Medium *(chưa Dev đánh giá)* | — | **0** | — | **GAP** |
| **T4** — Preview form (nút 「プレビュー」) | Feature | Medium | — | **0** | — | **GAP** — đây là nút trong **steps repro của QA** |

### ORPHAN TCs

**Không có TC orphan.** Cả 12 TC đều map được về BUG / F* / D* / T*.

Đã cân nhắc và **loại bỏ** khả năng flag `AP-5` (over-coverage tầng downstream) cho `TC-FUNC001-02` và `TC-TOOLKNOW002-01`: 2 TC này chạm `renderFormAnswer` — hàm **không bị sửa code** — nhưng chúng verify **hệ quả dữ liệu** (đúng thứ khách nhìn thấy) chứ không verify logic của hàm đó, nên là hợp lệ, **không đề nghị remove**.

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape nhận diện được** (từ [03-dev-impact.md](03-dev-impact.md) §2) — fix này có **3 shape chồng nhau**, không phải 1:

| # | Shape | Keyword khớp trong mục 2 | Câu hỏi adversarial | Trả lời từ bộ TC hiện tại |
|---|---|---|---|---|
| **S1** | **Validation / add check** | *"đầu saveV3: nếu bot đang mở khác bot sở hữu form thì rollback + trả JSON lỗi"* | Cover bao nhiêu input variant? Có test **server-side**? Đủ luồng vào (create / edit / **copy** / import / API)? | Server-side **CÓ** (`TC-API001-01` gọi thẳng endpoint) ✅. Variant: bot khác ✅, `getBotId()=0` ✅, **`form_id` không tồn tại / form đã xoá ❌** (REQ-003 của Studio ghi rõ *"(hoặc form không tồn tại)"* nhưng **0 TC**). Luồng vào: chỉ nút Lưu — **thiếu luồng 「プレビュー」 và luồng copy form** ❌ |
| **S2** | **Race condition / transaction** | *"rollback"*; và bản chất bug = tranh chấp giữa **bot của session** và **bot sở hữu form** | Đủ **4 kịch bản CONC-001**? Evidence có **đếm số lần xử lý thực tế**? | **0/4 kịch bản.** Không TC nào double-click, không TC nào **2 tab cùng user**, không TC nào 2 user sửa 1 form, không TC nào batch. `TC-OUTTRUTH001-01` chuyển bot **tuần tự** rồi mới bấm Lưu — đó **không phải** race ❌ |
| **S3** | **Migration / backfill** | *"Data cũ 6 form bot_id lệch cần chạy recover 1 lần"* + query `UPDATE … WHERE fp.bot_id <> fa.bot_id` | Data cũ không mất? Mẫu từ **nhiều nguồn/thời điểm**? Nhánh cũ chạy song song nhánh mới? Migration **chạy lại được** (idempotent)? Có dry-run / rollback? | Cũ ⇄ mới song song **CÓ** (`TC-TOOLOLDREC001-01`) ✅. Đối chứng âm **CÓ** ✅. Dry-run (query chẩn đoán trước) **CÓ** (`TC-DATAMIG001-01`) ✅. **Idempotent ❌** (không TC nào chạy recover lần 2). **Rollback ❌**. **Mẫu dữ liệu cũ nhiều nguồn/thời điểm ❌** (chỉ 1 bản ghi seed). **Phạm vi production ❌** |

> Ngoài ra `saveV3` là **hàm dùng chung** của toàn bộ luồng lưu form ⇒ kích hoạt thêm `REG-SHARED-001`: yêu cầu **danh sách nơi ảnh hưởng do Dev cung cấp**. Dev mục 4.1 chỉ liệt kê **file thay đổi** (1 file), không phải danh sách nơi ảnh hưởng — xem `[MAJOR] AP-6'` ở §4.2.

### Symptom-only KH report check

**KHÔNG dính.** File 01 mục "Actual result" có **error message + file + số dòng cụ thể** (`Trying to get property 'id' of non-object … FormAnswerService.php171`), và QA cung cấp steps tái hiện chính xác. Đây là ticket auto-detect từ exception, không phải KH mô tả triệu chứng mơ hồ ⇒ **không** flag `AP-2`, **không** yêu cầu cover "≥ 2 plausible root cause".

### Anti-pattern

| AP | Dính? | Ghi chú |
|---|---|---|
| **AP-1** Single-trigger generic-fix | **Một phần** | Guard là **specific check** (`getBotId() != form.bot_id`), không phải generic catch ⇒ áp quy tắc "specific code check → cover **từng** condition". Thiếu condition *form không tồn tại* → §4.2 |
| **AP-2** Symptom-only KH report | **Không** | Có error message + line number + steps repro chính xác (xem trên) |
| **AP-3** Happy-path-only regression | **DÍNH** | T1 chỉ regression ở trạng thái sạch; T2 chỉ form `bot_id` đúng; T3/T4 = 0 TC → §4.1 |
| **AP-4** Specific code-check disguised as generic | **DÍNH** | Mục "Commit / Pull Request" **không có link PR** (chỉ commit hash `aebc144d44` + link dashboard nội bộ). Cộng với **3 bản báo cáo AI mâu thuẫn** về việc `renderFormAnswer` có guard null hay không ⇒ **không thể verify fix shape thực tế** → §4.2 |
| **AP-5** Layer-downstream over-coverage | **Không** | Đã cân nhắc và loại — xem §3 ORPHAN |
| **AP-6** Mục 3 dev-impact trống | **Biến thể** | Mục 3 **không trống**, nhưng **thoái lui giữa 2 bản**: bản #124641 có `@8045/8094` (xoá trang) + `store`, bản #124657 **đã bỏ** ⇒ caller list bị thu hẹp mà không nêu lý do → §4.2 |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE S2 / GAP-1 — `CONC-001` + `CONC-003` + `SEC-ISO-001`: 0 TC cho kịch bản đồng thời, trong khi bug repro CHÍNH LÀ race 2 tab.**
  Steps repro của QA (file 01): *mở 2 tab cùng màn detail form bot A → tab 1 chuyển sang bot B → tab 2 bấm nhanh 「プレビュー」*. Không TC nào trong 12 TC dùng 2 tab. `TC-OUTTRUTH001-01` chuyển bot **tuần tự** — code path khác: khi chuyển bot tuần tự, tab còn lại được load lại/đồng bộ session; còn khi 2 tab song song, tab 2 giữ **DOM + token của bot A** nhưng session server đã là bot B. **Guard mới đọc `getBotId()` từ session — chưa ai chứng minh nó chặn được đúng luồng này.**
  → Bổ sung `TC-CONC003-01/02/03` + `TC-SECISO001-01` (§5). Evidence bắt buộc: **video thao tác 2 tab** + screenshot Network tab thể hiện thứ tự request/response.

- **[BLOCKER] GAP-2 / T4 — nút 「プレビュー」 không có TC nào, dù nó nằm trong steps repro.**
  Theo QA, プレビュー **vừa save vừa mở màn preview**. Nếu nút này gọi endpoint khác `save-v3` (hoặc gọi `save-v3` rồi redirect), guard mới có thể **không nằm trên đường đi của nó** ⇒ bug vẫn tái phát sau khi deploy. Đây là rủi ro "fix xong bug vẫn còn".
  → Bổ sung `TC-CONC003-02` + `TC-FUNC001-03` (§5). **Trước khi test, hỏi Dev: 「プレビュー」 gọi endpoint nào?**

- **[BLOCKER] GAP-3 — `DEPLOY-LIVE-001` (Cao ★): recover data chạy trên production KHÔNG bật maintain mà không có TC nào phủ.**
  Query recover là `UPDATE` chạy thẳng trên production trong lúc **LINE user đang mở form**. Quan điểm này yêu cầu đúng kịch bản: mở sẵn form phía LINE user → chạy recover → **không reload**, bấm submit → phải lưu result / ghi Google Spread / chạy action form đầy đủ, **không exception 500, không lưu nửa vời**. Hiện **0 TC**.
  → Bổ sung `TC-DEPLOYLIVE001-01/02` (§5). Đồng thời §6 yêu cầu chốt **thứ tự deploy fix ↔ chạy recover**.

- **[BLOCKER] AP-3 / GAP-4 / F4 + T3 — xoá / sửa trang khi `bot_id` đang lệch: 0 TC.**
  Bản #124641 của Dev ghi `FormAnswerController@8045/8094` (xoá trang lọc `getBotId`) là *"hệ quả cùng gốc, không sửa"* — nghĩa là **trang lệch `bot_id` có thể không xoá/sửa được**, chủ form bị kẹt cho tới khi recover. Bản #124657 **đã bỏ dòng này** mà không nêu lý do ⇒ rủi ro bị xoá khỏi tầm nhìn.
  → Bổ sung `TC-DATAREF001-01/02` (§5), test **cả trước và sau** recover.

### 4.2 Major (nên fix)

- **[MAJOR] 0.6#4 + 0.6#5 + RULE-02 — toàn bộ 11 kết quả `Đạt` do AI tự chạy tự chấm, `artifacts` rỗng 100%.**
  `task_get_report` xác nhận `manual.results = []` và mọi result có `artifacts: []`. Dev cũng chỉ verify mức `lint`. ⇒ **Chuỗi bug này chưa có một lần kiểm tra thủ công nào của con người**, và không có bằng chứng nào có thể kiểm chứng lại. `reviewed = false`, TC toàn bộ `status = draft`.
  → Chạy tay lại tối thiểu các TC trục chính (`TC-FUNC001-01`, `TC-OUTTRUTH001-01`, `TC-API001-01`, `TC-TOOLOLDREC001-01`) **kèm evidence**, rồi mới chuyển `reviewState`.

- **[MAJOR] 0.6#3 + `ENV-003` / RULE-08 — 11/12 TC chạy `local`, 0 TC production, trong khi đây là bug production.**
  Exception phát sinh trên **production `s.lmes.jp`** (36 lần) và fix này bắt buộc kèm **câu `UPDATE` recover chạy thẳng trên production** ⇒ `ENV-003` trigger BẮT BUỘC và **không được đánh × với lý do "local đã pass"**. `TC-RULE04-01` — TC production duy nhất — **chưa chạy**, nên **RULE-04 chưa thoả**: chưa ai biết production có bao nhiêu bản ghi lệch.
  → Chạy `TC-RULE04-01` trên production **trước** khi recover và **trước** khi đóng ticket.

- **[MAJOR] TC-DATAMIG001-01 — con số phạm vi đang mâu thuẫn và bị nhiễu bởi chính test.**
  Actual của run #450 ghi *"Tổng trang lệch hiện có trong DB = 7"*, Dev khai **6**. Chênh lệch này nhiều khả năng do `TC-TOOLKNOW002-01` seed thêm 1 bản ghi lệch trong cùng run ⇒ **query chẩn đoán bị nhiễm dữ liệu test**, không dùng để ước lượng phạm vi được. TC vẫn được chấm `pass`.
  → Tách TC chẩn đoán ra **run riêng, trên DB sạch**, và chốt lại con số. Bổ sung `TC-DATAMIG001-02` (idempotent) ở §5.

- **[MAJOR] TC-TOOLKNOW002-01 — chấm `pass` dù `line171Marker=false`.**
  Expected nêu đích danh `FormAnswerService.php:171`, nhưng runner tự ghi `line171Marker=false` (không xác nhận được vị trí lỗi) mà vẫn `pass`. ⇒ TC "tái hiện bug" chưa chứng minh được nó tái hiện **đúng** lỗi trong ticket, chỉ chứng minh có HTTP 500.
  → Sửa trên Studio (`testcase_update`) để Expected gắn với bằng chứng lấy được (log/stack trace thật), hoặc hạ Expected về "HTTP 500 + stack trace chứa `FormAnswerService`".

- **[MAJOR] `COMPAT-LEGACY-001` — chưa lấy mẫu bản ghi cũ THẬT cho nhánh UPDATE mới.**
  *(Đã thu hẹp sau feedback: chiều "link cũ `step3.lmes.jp` ⇄ `s.lmes.jp`" **không áp dụng** — fix không chạm routing/domain phía LINE user.)*
  Phần còn lại vẫn hợp lệ vì nằm **trên đúng code path bị sửa**: quan điểm này yêu cầu lấy bản ghi tạo **trước** thay đổi rồi **mở → sửa → lưu lại**. Nhánh UPDATE của `saveV3` vừa bị đổi (bỏ `bot_id`/`form_id` khỏi payload), nhưng mọi TC hiện có đều thao tác trên form **do chính test tạo mới**. Chưa form cũ thật nào đi qua nhánh UPDATE mới.
  → Bổ sung `TC-COMPATLEGACY001-01` (§5) — lấy ≥ 3 form tạo ở 3 thời điểm khác nhau.

- **[MAJOR] FIX-SHAPE S1 — thiếu condition `form_id` không tồn tại / form đã xoá.**
  REQ-003 của chính Studio định nghĩa guard là *"khi `getBotId()` != `form_answer.bot_id` **(hoặc form không tồn tại)**"*. Bộ TC cover 2 condition đầu, **bỏ trống condition thứ 3**. Đây là nhánh dễ sinh **exception mới** (truy cập property của `null` — cùng họ với chính bug đang fix).
  → Bổ sung `TC-FUNC001-04` (§5).

- **[MAJOR] `FUNC-SEQ-001` — không TC nào verify "reload rồi thao tác lại", dù đó là hướng dẫn trong chính message lỗi.**
  Message mới nói với user 「ページを再読み込みしてから、もう一度お試しください」. Không TC nào thực hiện đúng chỉ dẫn đó để chứng minh **sau khi reload thì lưu được**. Nếu sau reload vẫn bị chặn (vd session vẫn giữ bot cũ) thì user rơi vào **deadlock**.
  → Bổ sung `TC-FUNCSEQ001-01` (§5).

- **[MAJOR] `PERM-003` — cách ly dữ liệu đa tài khoản LINE OA chỉ được kiểm gián tiếp.**
  Toàn bộ bug xoay quanh **change bot**, nhưng TC chỉ verify "chặn lưu chéo bot". Chưa có TC verify sau khi change bot thì **danh sách form / trang của bot A và bot B vẫn độc lập** (trigger BẮT BUỘC của `PERM-003` khi có chức năng change bot).
  → Bổ sung `TC-PERM003-01` (§5).

- **[MAJOR] `DATA-DB-001` (Cao ★) — WHERE scope mới được kiểm cho query recover, chưa kiểm cho chính `saveV3`.**
  `TC-TOOLOLDREC001-01` có đối chứng âm bot B cho câu `UPDATE` recover ✅. Nhưng **RULE-07** yêu cầu: tạo bản ghi **trùng tên ở 2 tài khoản** → update ở A → query DB xác nhận **B không đổi**. Không TC nào làm việc này cho luồng `saveV3`. Ngoài ra "khoá mồ côi" — vốn **chính là hình dạng của bug này** (trang mồ côi không thuộc bot nào) — không có TC kiểm dọn/nhận diện.
  → Bổ sung `TC-DATADB001-02/03` (§5). *(Chưa nâng BLOCKER vì đã có 1 TC kiểm WHERE scope trên 2 tài khoản ở luồng recover.)*

- **[MAJOR] AP-4 — không có link PR + 3 bản báo cáo AI mâu thuẫn ⇒ không verify được fix shape thật.**
  Mục "Commit / Pull Request" chỉ có commit hash, không có diff review được. Bản #124641 nói *"Bỏ guard null ở renderForm"* và đồng thời mục 3 nói *"thêm guard"*; bản #124657 nói *"không sửa"*. **Expected của `TC-TOOLKNOW002-01` (vẫn crash 500) chỉ đúng nếu bản #124657 đúng.**
  → Yêu cầu Dev cung cấp diff của `aebc144d44` và chốt dứt điểm (xem §6).

- **[MAJOR] AP-6' — caller list bị thu hẹp giữa 2 bản báo cáo mà không nêu lý do.**
  `@8045/8094` (xoá trang) và `store` (dòng 811) có ở bản #124641, biến mất ở bản #124657. `REG-SHARED-001` yêu cầu **danh sách nơi ảnh hưởng do Dev cung cấp** — hiện mục 4.1 chỉ có "file thay đổi".
  → Yêu cầu Dev cung cấp danh sách đầy đủ **mọi nơi gọi `getBotId()` trong luồng form**, rồi test từng nơi (RULE-12).

- **[MAJOR] RULE-01 — 5/5 quan điểm hợp lệ ưu tiên **Cao** đều thiếu loại case, không TC nào ghi lý do.**
  `FUNC-001`: 2 Normal / 0 Abnormal / 0 Boundary · `DATA-DB-001`: 1 Normal · `OUT-TRUTH-001`: 1 Abnormal / 0 Normal / 0 Boundary · `DATA-MIG-001`: 1 Normal · `REG-SHARED-001`: 1 Normal. Cột `Ghi chú` không TC nào giải thích vì sao thiếu.
  → Bổ sung theo §5, hoặc ghi lý do vào Studio.

- **[MAJOR] BƯỚC 1 — checkbox "Tester verify auto-fill chính xác" CHƯA tick ở cả `01-bug-task.md` và `03-dev-impact.md`.**
  Cả 2 file đều có `Auto-filled: 2026-08-25 by /new-task`. Auto-fill từ Redmine **chưa được tester verify** ⇒ F/D/T dùng để dựng coverage matrix ở §3 có thể thiếu hoặc map sai, và **toàn bộ review này kế thừa rủi ro đó**.
  → Tester đọc lại Redmine #38428 (đặc biệt 3 journal auto-fixbug) và tick checkbox trước khi report này có giá trị nghiệm thu.

### 4.3 Minor (có thể fix sau)

- **[MINOR] 0.6#6 — 6/12 TC dùng mã quan điểm không map được về `checklist-lme.md`.**
  `API-001`, `API-CONTRACT-001`, `TOOL-KNOW-002`, `TOOL-OLDREC-001` không thuộc 80 quan điểm tầng 1; `RULE-01` và `RULE-04` là **RULE**, không hợp lệ ở cột "Mã quan điểm liên kết". 6 TC này **không được tính là cover** ở §7 F.1.
  → Map lại trên Studio: `API-001`→`PERM-002` · `API-CONTRACT-001`→`FUNC-001` · `TOOL-OLDREC-001`→`COMPAT-LEGACY-001` · `RULE-04`→`DATA-MIG-001` · `RULE-01`→`FUNC-001` · `TOOL-KNOW-002`→`REG-SPEC-001`.

- **[MINOR] RULE-02 — không TC nào ghi **loại evidence bắt buộc** ở cột `Ghi chú`.**
  12/12 TC có `note` mô tả ý đồ test nhưng không nêu cần chụp/lưu gì làm bằng chứng.

- **[MINOR] D2 — `form_answer_page.form_id` chưa có TC verify riêng khi UPDATE.**
  `TC-DATADB001-01` chỉ so `bot_id` trước/sau. `form_id` cũng là field định danh bị tách khỏi payload UPDATE trong cùng hunk 2 ⇒ nên verify cùng cách.

- **[MINOR] F3 — alert message chỉ được đối chiếu rút gọn.**
  Actual ghi 「アカウントが切り替わっている…」 (cắt bằng `…`), chưa đối chiếu **nguyên văn** chuỗi trong Expected.

### 4.4 Nit (gợi ý)

- **[NIT] `TC-REGSHARED001-01`** — note Studio cảnh báo *"branch stale thiếu #37710/#38700 nếu test trực tiếp trên branch"*. Nên confirm branch `ai_fixbug_38428` đã rebase lên release mới nhất trước khi chạy regression, tránh fail giả.
- **[NIT] `DATA-AUDIT-001`** — quan điểm này **không trigger** (form page không thuộc nhóm dữ liệu nhạy cảm: khách hàng / thanh toán / phân quyền / tag). Tuy nhiên câu `UPDATE` recover chạy thẳng trên production **không để lại vết audit** — gợi ý log lại danh sách `page_id` trước/sau khi recover để về sau còn truy được.
- **[NIT] `DATA-BACKUP-001`** — fix không thêm/đổi bảng, không chạm backup/copy bot ⇒ đánh × hợp lệ. Chỉ lưu ý nếu sau này có chức năng **copy bot**: `form_answer_page.bot_id` là field phải remap.
- **[NIT] RULE-11** — không có mục nào ở §4 `checklist-lme.md` ("quan điểm chưa đủ bằng chứng") được dùng để flag BLOCKER/MAJOR trong report này.

---

## 5. TCs đề xuất bổ sung

> **19 TC** lấp các GAP ở §3 và §7 F.1. Viết từ **góc nhìn manual tester** (thao tác UI + quan sát), member copy thẳng vào `04-tc-list.md` round 2.
> Ưu tiên chạy trước 5 TC chặn merge: `TC-CONC003-01`, `TC-CONC003-02`, `TC-FUNC001-03`, `TC-DATAMIG001-03`, `TC-DATAREF001-01`.
>
> ⚠️ **Round 1 feedback (2026-08-26)** — đã **bỏ 4 TC**: `TC-LIFFENTRY001-01/02/03` và TC "mở form bằng link cũ `step3.lmes.jp``". Lý do: lần fix này chỉ chạm `FormAnswerController::saveV3` (tầng ghi), **không chạm code phía LINE user** — màn form công khai, cơ chế LIFF entry và routing domain đều không đổi. Test sâu các chiều đó là over-test tầng downstream (`AP-5`). 2 TC `TC-COMPATLEGACY001-*` được giữ và đánh số lại vì chúng chạy trên **nhánh UPDATE của `saveV3`** — đúng code bị sửa.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-CONC003-01 | CONC-003 | Abnormal | Race 2 tab: tab 1 đổi sang bot B, tab 2 bấm 「プレビュー」 — tái hiện đúng steps QA | - Account admin có quyền trên ≥ 2 bot (bot A, bot B)<br>- Bot A có 1 form đã lưu, có ≥ 1 trang<br>- Dùng cùng 1 browser, cùng session | 1. Mở màn chi tiết form của bot A, nhân đôi tab để có 2 tab cùng URL.<br>2. Ở tab 1, dùng menu chuyển tài khoản sang bot B, đợi màn load xong.<br>3. Quay lại tab 2 (vẫn đang hiển thị form bot A, chưa reload), bấm ngay nút 「プレビュー」.<br>4. Quan sát tab 2: có alert không, màn preview mở ra gì.<br>5. Mở lại form bot A ở tab mới, đếm số trang và xem tên trang. | form bot A: 1 trang tên `スタート`; bot B là bot khác chủ | Tab 2 hiển thị thông báo tài khoản đã chuyển, **không** mở màn preview lỗi 404 và **không** lưu gì. Mở lại form bot A: vẫn đúng 1 trang, tên trang vẫn `スタート` — không phát sinh trang lệch bot. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-1 + GAP-2** (BUG / T4). Đây là steps repro nguyên văn của QA ở file 01. Evidence bắt buộc: **video quay 2 tab** + screenshot tab Network của tab 2. Trước khi chạy: hỏi Dev 「プレビュー」 gọi endpoint nào |
| TC-CONC003-02 | CONC-003 | Abnormal | Race 2 tab: tab 1 đổi bot, tab 2 bấm nút Lưu 「登録」 (đối chứng với luồng プレビュー) | Như TC-CONC003-01 | 1. Mở 2 tab cùng màn chi tiết form bot A.<br>2. Tab 1: chuyển sang bot B.<br>3. Tab 2: sửa tên 1 trang rồi bấm 「登録」.<br>4. Quan sát thông báo ở tab 2.<br>5. Mở lại form bot A, kiểm tên trang. | đổi tên trang thành `TC_race_luu` | Hiện thông báo tài khoản đã chuyển, không lưu. Tên trang vẫn là giá trị cũ. **Kết quả phải giống hệt TC-CONC003-01** — nếu 2 luồng ra kết quả khác nhau thì guard chưa phủ luồng プレビュー. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-1/GAP-2**. Cặp đối chứng với TC-CONC003-01 để lộ ra luồng nào chưa được guard bảo vệ. Evidence: video 2 tab |
| TC-CONC003-03 | CONC-003 | Boundary | Race sát ranh: bấm 「プレビュー」 ở tab 2 **trong lúc** tab 1 đang chuyển bot (chưa load xong) | Như TC-CONC003-01, thêm: bật DevTools Network throttling `Slow 3G` ở tab 1 | 1. Mở 2 tab cùng màn chi tiết form bot A.<br>2. Tab 1: bật throttling Slow 3G, bấm chuyển sang bot B.<br>3. **Ngay khi tab 1 còn đang loading**, sang tab 2 bấm 「プレビュー」.<br>4. Đợi cả 2 tab load xong, quan sát kết quả từng tab.<br>5. Kiểm lại form bot A: số trang, tên trang, và trang có bot lệch không. | throttling Slow 3G ở tab 1 | Không xảy ra trạng thái nửa vời: hoặc lưu đúng bot A, hoặc bị chặn có thông báo. **Tuyệt đối không** tạo trang thuộc bot khác/không thuộc bot nào. Mở form bot A vẫn bình thường. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-1** (biên thời gian của race). Evidence: video + screenshot Network thể hiện thứ tự response |
| TC-SECISO001-01 | SEC-ISO-001 | Abnormal | Mở form của bot A và bot B trên 2 tab, thao tác xen kẽ — dữ liệu không dính chéo | - Admin có quyền bot A và bot B<br>- Mỗi bot có 1 form riêng, đặt **trùng tên** để dễ phát hiện nhầm | 1. Tab 1: mở form của bot A. Tab 2: mở form của bot B.<br>2. Thao tác xen kẽ nhanh: sửa trang ở tab 1 → sửa trang ở tab 2 → lưu tab 1 → lưu tab 2.<br>3. Mở lại lần lượt 2 form, đối chiếu nội dung từng trang.<br>4. Mở màn form công khai của cả 2 form. | 2 form trùng tên `お問い合わせ`, mỗi bot 1 cái | Nội dung 2 form độc lập hoàn toàn, không có trang của bot này xuất hiện ở form bot kia. Cả 2 form công khai mở bình thường. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-1** (`SEC-ISO-001` Cao — multi-session cùng user). Đặt trùng tên là chủ ý để lộ nhầm lẫn. Evidence: screenshot 2 form sau thao tác |
| TC-COMPATLEGACY001-01 | COMPAT-LEGACY-001 | Normal | Form tạo **trước** thời điểm phát sinh lỗi: mở → sửa → lưu lại vẫn đúng bot | - Lấy ≥ 3 form được tạo ở **3 thời điểm khác nhau** trước 2026-07-01 (nhờ Leader chọn mẫu thật trên môi trường)<br>- Đang mở đúng bot sở hữu từng form | 1. Với từng form mẫu: mở màn chi tiết form.<br>2. Sửa nhẹ 1 trang (đổi tên trang).<br>3. Bấm Lưu.<br>4. Mở màn form công khai của form đó.<br>5. Lặp lại cho cả 3 form. | 3 form cũ từ 3 thời điểm khác nhau | Cả 3 form: lưu thành công, mở màn công khai hiển thị bình thường, không form nào rơi vào trạng thái trang lệch bot. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp `[MAJOR]` `COMPAT-LEGACY-001`** + bù `DATA-MIG-001` (mẫu dữ liệu cũ **nhiều nguồn / nhiều thời điểm** — hiện chỉ có 1 bản ghi seed). Evidence: ảnh 3 form sau khi lưu |
| TC-COMPATLEGACY001-02 | COMPAT-LEGACY-001 | Abnormal | Form đã recover và form tạo mới sau fix cùng chạy song song — cả 2 đều đúng | - 1 form thuộc nhóm đã bị lệch `bot_id` và **đã chạy recover**<br>- 1 form tạo mới hoàn toàn sau khi deploy fix | 1. Mở màn công khai của form đã recover, xem trang đầu.<br>2. Mở màn công khai của form mới, xem trang đầu.<br>3. Vào admin sửa và lưu lại từng form.<br>4. Mở lại màn công khai của cả 2. | 1 form cũ đã recover + 1 form mới | Cả 2 form hiển thị và lưu bình thường ở mọi bước, không form nào quay lại trạng thái lỗi. | Chưa test | | **PRODUCTION** | | | | Đã hỏi leader | **Lấp `[MAJOR]` `COMPAT-LEGACY-001`** — "cũ & mới song song" ở dữ liệu thật (TC-TOOLOLDREC001-01 hiện chỉ làm điều này trên `local` với data tự seed) |
| TC-DEPLOYLIVE001-01 | DEPLOY-LIVE-001 | Abnormal | Mở sẵn form phía LINE user **trước** khi chạy recover, submit sau khi recover mà không reload | - Form thuộc nhóm đang lệch `bot_id`, **chưa** recover<br>- Đã thống nhất thời điểm chạy query recover | 1. Trên điện thoại, mở màn form công khai (form còn lỗi hoặc form bình thường cùng bot) và **giữ nguyên, không reload**.<br>2. Người có quyền chạy query recover trên môi trường đó.<br>3. Quay lại điện thoại, **không reload**, điền và bấm gửi.<br>4. Kiểm bản ghi trả lời trên admin + màn hình điện thoại. | form đang mở trước khi recover | Hoặc gửi thành công và admin nhận đủ bản ghi, hoặc báo lỗi rõ ràng yêu cầu tải lại. **Không** exception 500, **không** lưu nửa vời (bản ghi thiếu trường). | Chưa test | | **PRODUCTION** | | | | Đã hỏi leader | **Lấp GAP-3**. Recover là `UPDATE` chạy trên prod không bật maintain trong khi user đang mở form. Evidence: ảnh màn điện thoại + bản ghi admin + log request |
| TC-DEPLOYLIVE001-02 | DEPLOY-LIVE-001 | Abnormal | Admin mở sẵn màn chỉnh sửa form trước khi deploy fix, bấm Lưu sau khi deploy mà không reload | - Màn chi tiết form của bot A mở sẵn **trước** thời điểm deploy | 1. Mở màn chi tiết form bot A, **không** reload.<br>2. Deploy bản fix lên môi trường.<br>3. Không reload, sửa 1 trang rồi bấm Lưu.<br>4. Quan sát thông báo, sau đó reload và kiểm lại nội dung trang. | JS/trang đang là bản trước deploy | Hoặc lưu đúng, hoặc báo lỗi rõ ràng. Không lưu nửa vời, không tạo trang lệch bot. Sau reload, nội dung trang đúng với thao tác vừa rồi (nếu báo lưu thành công). | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-3** — client cũ gọi server mới. Evidence: screenshot màn cũ + kết quả sau submit |
| TC-DATAREF001-01 | DATA-REF-001 | Abnormal | Xoá / sửa trang của form đang có `bot_id` lệch (**trước** recover) | - 1 form có trang `bot_id` lệch, **chưa** recover<br>- Đang mở đúng bot sở hữu form | 1. Mở màn chi tiết form đó trên admin.<br>2. Quan sát: các trang có hiển thị đủ không.<br>3. Thử đổi tên 1 trang rồi lưu.<br>4. Thử xoá 1 trang.<br>5. Ghi lại chính xác thông báo/hành vi ở mỗi bước. | form đang lệch `bot_id` | Hành vi phải **rõ ràng và nhất quán**: hoặc thao tác được, hoặc báo lỗi dễ hiểu. **Không** màn trắng, **không** exception, **không** xoá nhầm trang của form khác. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-4** (F4 + T3). Bản #124641 của Dev nói `@8045/8094` lọc `getBotId` "không sửa" ⇒ nghi trang lệch không xoá/sửa được. Evidence: ảnh từng bước + ảnh danh sách trang trước/sau |
| TC-DATAREF001-02 | DATA-REF-001 | Normal | Xoá / sửa trang của chính form đó **sau** khi recover | - Cùng form ở TC-DATAREF001-01, đã chạy recover | 1. Mở lại màn chi tiết form sau recover.<br>2. Đổi tên 1 trang, lưu.<br>3. Xoá 1 trang, lưu.<br>4. Mở màn form công khai kiểm hiển thị.<br>5. Kiểm form của bot khác không bị ảnh hưởng. | cùng form, sau recover | Sửa và xoá trang đều thành công. Màn công khai hiển thị đúng số trang còn lại. Form của bot khác giữ nguyên. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-4** — cặp đối chứng với TC-DATAREF001-01, chứng minh recover thật sự gỡ được tình trạng kẹt |
| TC-DATAREF001-03 | DATA-REF-001 | Normal | Copy form → các trang của bản sao thuộc đúng bot sở hữu | - Đang mở bot A, có 1 form nhiều trang<br>- Chức năng copy form khả dụng | 1. Ở màn danh sách form của bot A, copy 1 form có ≥ 2 trang.<br>2. Mở form bản sao, kiểm đủ số trang và nội dung.<br>3. Sửa 1 trang của bản sao rồi lưu.<br>4. Mở màn form công khai của **bản sao**.<br>5. Mở màn công khai của **form gốc** để đối chứng. | form gốc 3 trang | Bản sao có đủ 3 trang, thuộc đúng bot A, sửa/lưu bình thường. Màn công khai của **cả bản sao lẫn form gốc** đều hiển thị đúng, độc lập nhau. | Chưa test | | STAGING | | | | Đã hỏi leader | Bổ sung theo `DATA-REF-001` — luồng **copy** là đường vào chưa được guard kiểm (§3.5 S1). Nếu copy cũng lấy `bot_id` từ session thì đây là biến thể chưa fix của cùng bug |
| TC-FUNC001-03 | FUNC-001 | Normal | Luồng chuẩn: bấm 「プレビュー」 khi đang đúng bot — lưu được và preview hiển thị đúng | - Đang mở đúng bot A<br>- Form bot A có ≥ 2 trang | 1. Mở màn chi tiết form của bot A.<br>2. Sửa nội dung 1 trang.<br>3. Bấm 「プレビュー」.<br>4. Quan sát màn preview mở ra: đủ trang, đúng nội dung vừa sửa chưa.<br>5. Quay lại admin, reload, kiểm nội dung đã lưu. | sửa tiêu đề trang 1 thành `TC_preview_ok` | Màn preview mở đúng, hiển thị nội dung `TC_preview_ok` vừa sửa. Sau reload màn admin, nội dung đã được lưu đúng. Không lỗi 404/500. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp GAP-2** (T4) — đối chứng dương của luồng プレビュー. Không có TC này thì không biết luồng プレビュー vốn hoạt động thế nào để so với TC-CONC003-01 |
| TC-FUNC001-04 | FUNC-001 | Abnormal | Lưu form vừa bị xoá ở tab khác — báo lỗi rõ ràng, không văng exception | - Admin mở màn chi tiết form bot A ở tab 1<br>- Cùng account mở danh sách form ở tab 2 | 1. Tab 1: mở màn chi tiết form X, để nguyên.<br>2. Tab 2: xoá form X khỏi danh sách.<br>3. Tab 1: **không reload**, sửa 1 trang rồi bấm Lưu.<br>4. Quan sát thông báo ở tab 1. | form X bị xoá ở tab khác | Hiện thông báo lỗi rõ ràng (form không còn tồn tại / yêu cầu tải lại). **Không** màn trắng, **không** exception 500 kiểu "property of non-object", không tạo bản ghi mồ côi. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp `[MAJOR]` FIX-SHAPE S1** — REQ-003 của Studio ghi guard cũng phải xử lý *"form không tồn tại"* nhưng 0 TC. Đây là nhánh dễ sinh exception cùng họ với bug đang fix |
| TC-FUNCSEQ001-01 | FUNC-SEQ-001 | Normal | Sau khi bị chặn vì đổi bot: tải lại trang rồi thao tác lại — phải lưu được | - Đã thực hiện xong TC-CONC003-02 (vừa bị chặn với thông báo tài khoản đã chuyển) | 1. Ở tab vừa bị chặn, làm **đúng** hướng dẫn trong thông báo: tải lại trang.<br>2. Quan sát màn sau khi tải lại thuộc bot nào.<br>3. Chuyển về đúng bot sở hữu form, mở lại form.<br>4. Sửa 1 trang rồi bấm Lưu.<br>5. Reload kiểm nội dung. | thao tác lại sau reload | Sau khi làm theo hướng dẫn, user **lưu được bình thường**, không bị chặn lặp lại. Nội dung sửa được lưu đúng. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp `[MAJOR]` `FUNC-SEQ-001`** — message mới bảo user 「ページを再読み込みしてから、もう一度お試しください」 nhưng chưa TC nào chứng minh làm theo thì thoát được. Nếu vẫn bị chặn ⇒ user deadlock |
| TC-PERM003-01 | PERM-003 | Normal | Sau khi chuyển bot, danh sách form và trang của 2 bot vẫn độc lập | - Admin có quyền bot A và bot B<br>- Mỗi bot có ≥ 2 form, trong đó có 1 cặp **trùng tên** | 1. Đang ở bot A, ghi lại danh sách form (tên + số trang từng form).<br>2. Chuyển sang bot B, ghi lại danh sách form tương tự.<br>3. Chuyển ngược lại bot A, đối chiếu với ghi chép bước 1.<br>4. Mở 1 form ở mỗi bot, đếm số trang.<br>5. Mở màn công khai của cặp form trùng tên. | 1 cặp form trùng tên `お問い合わせ` ở 2 bot | Danh sách form của mỗi bot không đổi sau khi chuyển qua lại. Cặp form trùng tên hiển thị đúng nội dung riêng của từng bot ở cả admin lẫn màn công khai. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp `[MAJOR]` `PERM-003`** (Cao — trigger BẮT BUỘC vì có chức năng change bot). Trùng tên là chủ ý để lộ nhầm lẫn |
| TC-DATADB001-02 | DATA-DB-001 | Abnormal | Lưu form ở bot A không đụng tới form trùng tên của bot B | - Bot A và bot B mỗi bên có 1 form **trùng tên**, mỗi form 2 trang **trùng tên trang** | 1. Ghi lại nội dung 2 trang của form bot B (chụp màn).<br>2. Sang bot A, sửa cả 2 trang của form bot A rồi lưu.<br>3. Chuyển sang bot B, mở form bot B.<br>4. Đối chiếu từng trang với ảnh chụp bước 1.<br>5. Mở màn công khai của form bot B. | 2 form trùng tên `お問い合わせ`, trang trùng tên `スタート` | Form bot B **không thay đổi gì**: tên trang, nội dung, số trang y hệt bước 1. Màn công khai của form bot B hiển thị bình thường. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp `[MAJOR]` `DATA-DB-001`** — **RULE-07** yêu cầu tạo bản ghi trùng tên ở **2 tài khoản** để kiểm phạm vi `WHERE` của luồng `saveV3` (hiện chỉ kiểm cho câu recover). Evidence: ảnh trước/sau của form bot B |
| TC-DATADB001-03 | DATA-DB-001 | Boundary | Xoá hết trang của form rồi lưu — không để lại trang mồ côi | - Form bot A có 3 trang | 1. Mở màn chi tiết form bot A.<br>2. Xoá lần lượt các trang cho tới khi còn ít nhất có thể theo ràng buộc màn hình.<br>3. Lưu form.<br>4. Mở lại form, đếm số trang hiển thị.<br>5. Mở màn form công khai. | form 3 trang → xoá còn tối thiểu | Số trang hiển thị khớp đúng thao tác, không còn trang "ẩn" nào sót lại. Màn công khai mở bình thường, không 404/500 do trang mồ côi. | Chưa test | | STAGING | | | | Đã hỏi leader | **Lấp `[MAJOR]` `DATA-DB-001`** — chiều "khoá mồ côi", chính là hình dạng của bug này (trang không thuộc bot nào). Evidence: ảnh danh sách trang trước/sau + ảnh màn công khai |
| TC-DATAMIG001-02 | DATA-MIG-001 | Boundary | Chạy query recover **lần thứ 2** — không đổi thêm bản ghi nào (idempotent) | - Đã chạy recover lần 1 xong<br>- Có quyền chạy query trên môi trường đó | 1. Sau lần recover thứ nhất, chạy lại query chẩn đoán để đếm số trang còn lệch.<br>2. Chạy lại **đúng** câu recover lần 2.<br>3. Ghi lại số bản ghi bị ảnh hưởng ở lần 2.<br>4. Mở lại vài form đã recover, kiểm hiển thị. | chạy recover 2 lần liên tiếp | Lần 1 sau recover: query chẩn đoán trả về **0 bản ghi lệch**. Lần 2 chạy recover: **0 bản ghi bị đổi**. Các form đã recover vẫn mở bình thường. | Chưa test | | **PRODUCTION** | | | | Đã hỏi leader | **Lấp `[MAJOR]`** — `DATA-MIG-001` yêu cầu migration **chạy lại được**. Chạy nhầm 2 lần là tình huống thật hay xảy ra khi thao tác tay trên prod. Evidence: ảnh kết quả query cả 2 lần (kèm câu query) |
| TC-DATAMIG001-03 | DATA-MIG-001 | Abnormal | Đếm phạm vi trên DB **sạch** (không có dữ liệu do test seed) | - DB không chứa bản ghi lệch do test tự tạo<br>- Quyền read-only | 1. Xác nhận môi trường không còn dữ liệu seed của các TC trước (hoặc dùng snapshot sạch).<br>2. Chạy query chẩn đoán đếm trang lệch.<br>3. Ghi lại con số và danh sách `form_id`.<br>4. Đối chiếu với con số Dev khai (6) và con số run #450 ghi (7). | không (chỉ đọc) | Ra được con số **đáng tin**, giải thích được chênh lệch 6 ⇄ 7, và danh sách `form_id` cụ thể để quyết định recover. | Chưa test | | **PRODUCTION** | | | | Đã hỏi leader | **Lấp `[MAJOR]` TC-DATAMIG001-01** — con số 7 ở run #450 bị nhiễm bởi bản ghi mà `TC-TOOLKNOW002-01` tự seed. **RULE-04** yêu cầu phạm vi phải chốt được trước khi đóng ticket |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần chốt / update spec** — 4 điểm:

1. **`renderFormAnswer` cuối cùng CÓ hay KHÔNG guard null?**
   - Nguồn mâu thuẫn: journal #124641 mục 2 *"Bỏ guard null ở renderForm (thừa sau khi fix gốc)"* nhưng mục 3 ghi *"thêm guard"*; journal #124657 ghi *"điểm crash gốc, **không sửa**"*.
   - **Vì sao chặn được review**: Expected của `TC-TOOLKNOW002-01` là *"vẫn crash HTTP 500"* — chỉ đúng nếu bản #124657 đúng. Nếu thực tế có guard thì TC này **Expected sai** và kết quả `Đạt` là sai.
   - Người chịu trách nhiệm: Dev auto-fixbug / Leader — yêu cầu cung cấp **diff của commit `aebc144d44`**.

2. **Guard chặn lưu chéo bot trả HTTP 500 — đúng hay nên là 4xx?**
   - Đây là **lỗi thao tác của user**, không phải lỗi hệ thống. Trả `500` khiến: (a) `PERM-002` kỳ vọng `403` không khớp; (b) **rủi ro chính hệ thống check-exception lại bắn ticket auto-detect mới lên room `SNSLineException`** — đúng cơ chế đã sinh ra ticket #38428 này.
   - ⚠️ Cần Dev xác nhận: response `500` do `return response()->json(...)` có bị exception detector bắt không. Nếu có → **fix này tự sinh nguồn ticket rác**.
   - Người chịu trách nhiệm: Dev + người vận hành check-exception.

3. **Thứ tự và thời điểm: deploy fix ↔ chạy query recover trên production.**
   - Chưa tài liệu nào chốt chạy recover **trước hay sau** deploy, và có bật maintain không. Điều này quyết định `TC-DEPLOYLIVE001-01/02` chạy thế nào.
   - Người chịu trách nhiệm: Leader + Dev.

4. **Spec màn form công khai: trang không tìm thấy thì hiển thị gì?**
   - File 01 ghi Actual là **404**; exception là **500**. Sau fix, form cũ chưa recover sẽ ra 404 hay 500 hay màn báo lỗi thân thiện? Chưa spec nào định nghĩa.
   - `02-spec-reference.md` **không tồn tại** trong folder ⇒ review này fallback [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md). Đề nghị bổ sung file 02 cho feature Form Answer.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 **FAIL** (không TC nào mô phỏng đúng steps repro file 01) · A.2 PASS cho F1, **FAIL** cho F4 · A.3 PASS cho D1, RISK cho D2/D3 · A.4 **FAIL** cho T3/T4 · A.5 PASS (không orphan) · A.6 **FAIL** (xem §3.5)
- [x] **B. Chất lượng từng TC** — PASS. Title có keyword, precondition dựng được, steps tuần tự, Expected đo lường được (giá trị `bot_id`/HTTP code cụ thể). Trừ `TC-TOOLKNOW002-01` (Expected gắn số dòng nhưng runner không xác nhận được).
- [x] **C. Chất lượng bộ TC** — **FAIL**. Tỷ lệ Normal/Abnormal/Boundary = **8/3/1** (67% / 25% / 8%), lệch xa gợi ý 40/35/25 — thiếu nghiêm trọng Boundary, trong khi bản chất task là **validation + race + migration** (đáng lẽ Abnormal/Boundary phải nhiều hơn). Không có TC trùng lặp.
- [x] **D. Spec alignment** — **FAIL**. `02-spec-reference.md` không tồn tại; 4 điểm cần chốt ở §6; `TC-TOOLKNOW002-01` có Expected mâu thuẫn giữa 2 bản báo cáo Dev.
- [x] **E. Hành chính** — RISK. File 04 đúng folder, đúng 16 cột. Nhưng: `TC No.` gốc Studio dùng `temp_id` (NEW-n) không theo format repo (đã map lại khi ghi file 04); 6 mã quan điểm không hợp lệ (§4.3); **checkbox verify auto-fill của file 01 và 03 chưa tick**.
- [x] **F. Base quan điểm test LME**
  - [x] **F.1** — bảng dưới
  - [x] **F.2 Catalog (tầng 2)** — **A** (input): không áp dụng, fix không đổi ô nhập · **B** (UI): `UIC` cho nút Lưu/プレビュー + multi-tab — **chưa rà**, là gốc của GAP-1/GAP-2 · **C** (bản đồ LME): khối **phân quyền / đa bot (change bot)** — **chưa duyệt hết** (`PERM-003`); khối **ma trận LIFF** = × *(không chạm code phía LINE user)* · **D/D2** (môi trường): chạm **domain `s.lmes.jp`** ⇒ RULE-08 áp dụng, **0 TC production** ❌ · **E** (media): không áp dụng
  - [x] **F.3 RULE** — RULE-01 ❌ (§4.2) · RULE-02 ❌ (evidence rỗng 12/12) · RULE-03 n/a · RULE-04 ❌ (chưa đếm prod) · RULE-05 n/a (không tích hợp bên thứ 3) · RULE-06 n/a *(fix không chạm output ra ngoài — màn phía LINE user không đổi code)* · RULE-07 ⚠️ (có verify DB, thiếu 2-tài-khoản cho `saveV3`) · RULE-08 ❌ · RULE-09 ⚠️ *(chiều "link cũ ⇄ mới" n/a; còn thiếu mẫu bản ghi cũ thật đi qua nhánh UPDATE mới)* · RULE-12 ⚠️ (thiếu danh sách vùng ảnh hưởng từ Dev)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` — Luồng chính đúng đặc tả | **Cao** | ◯ luôn bắt buộc | TC-FUNC001-01, TC-FUNC001-02 | **RISK** — 2 Normal, 0 Abnormal, 0 Boundary (**RULE-01**); RULE-06 chưa tới output cuối |
| `FUNC-SEQ-001` — Thao tác liên tiếp & reload | Trung bình | ◯ message lỗi yêu cầu user reload rồi làm lại | — | **GAP** → `[MAJOR]` |
| `CONC-001` — 1 hành động chỉ xử lý 1 lần | **Cao** | ◯ nút thực thi quan trọng + nhiều tab | — | **GAP** → **`[BLOCKER]`** |
| `CONC-003` ★ — Race tầng giao diện | **Cao** (nâng: nhiều tab cùng gọi API) | ◯ **chính là steps repro** | — | **GAP** → **`[BLOCKER]`** |
| `SEC-ISO-001` — Cách ly dữ liệu đa phiên | **Cao** | ◯ 2 tab cùng user | — | **GAP** → **`[BLOCKER]`** |
| `LIFF-ENTRY-001` ★ — Điểm vào link phía LINE user | **Cao** | **×** — fix chỉ chạm `saveV3` (tầng ghi); màn form công khai, LIFF entry và routing domain **không đổi code** | TC-FUNC001-02, TC-TOOLKNOW002-01 | **N/A** *(lý do đã ghi — RULE-03). Gỡ khỏi BLOCKER theo feedback round 1* |
| `COMPAT-LEGACY-001` ★ — Cũ & mới song song | **Cao** | ◯ **một phần** — chiều "link cũ ⇄ mới" **×** (không chạm domain); chiều "bản ghi tạo trước → mở/sửa/**lưu lại**" ◯ vì đi qua nhánh UPDATE vừa sửa | — *(mọi TC đều dùng form do test tự tạo)* | **GAP** → `[MAJOR]` |
| `DEPLOY-LIVE-001` ★ — Release không lock maintain | **Cao** | ◯ recover `UPDATE` chạy trên prod khi user đang mở form | — | **GAP** → **`[BLOCKER]`** |
| `DATA-REF-001` — Reference integrity (xoá/copy) | **Cao** | ◯ trang được form tham chiếu; có copy form | — | **GAP** → **`[BLOCKER]`** *(F4/T3)* |
| `DATA-DB-001` ★ — WHERE scope + khoá mồ côi | **Cao** | ◯ BẮT BUỘC (có UPDATE) | TC-DATADB001-01, TC-TOOLOLDREC001-01 *(chỉ cho câu recover)* | **RISK** → `[MAJOR]` — thiếu 2-tài-khoản cho `saveV3`, thiếu chiều mồ côi |
| `DATA-MIG-001` — Migration dữ liệu cũ | **Cao** | ◯ recover data 1 lần | TC-DATAMIG001-01, TC-TOOLOLDREC001-01, *TC-RULE04-01 (chưa chạy)* | **RISK** → `[MAJOR]` — thiếu idempotent / rollback / mẫu nhiều nguồn |
| `PERM-003` — Cách ly đa tài khoản LINE OA | **Cao** | ◯ BẮT BUỘC (có change bot) | *(gián tiếp qua TC-OUTTRUTH001-01)* | **RISK** → `[MAJOR]` |
| `PERM-002` — Không bypass bằng API/URL | **Cao** | ◯ gọi thẳng endpoint | TC-API001-01, TC-APICONTRACT001-01 | **OK** — nhưng trả `500` thay vì `403` (§6 điểm 2) |
| `OUT-TRUTH-001` — UI khớp trạng thái thật | **Cao** | ◯ thao tác lưu có thông báo kết quả | TC-OUTTRUTH001-01 | **RISK** — 1 Abnormal, 0 Normal, 0 Boundary (**RULE-01**) |
| `REG-SHARED-001` — Shared code | **Cao** | ◯ `saveV3` dùng chung | TC-REGSHARED001-01 | **RISK** → `[MAJOR]` — thiếu danh sách vùng ảnh hưởng từ Dev; regression chỉ trạng thái sạch (AP-3) |
| `ENV-003` ★ — Khác biệt dev/staging/prod | **Cao** | ◯ chạm domain `s.lmes.jp` | — *(11/12 TC ở `local`)* | **GAP** → `[MAJOR]` **RULE-08** |
| `UI-003` — Loading / rỗng / lỗi | Trung bình → Cao *(rủi ro false success)* | ◯ có nhánh báo lỗi mới | TC-OUTTRUTH001-01, TC-RULE01-01 | **OK** |
| `DATA-AUDIT-001` — Audit log | **Cao** | **×** — form page không thuộc nhóm dữ liệu nhạy cảm (khách hàng / thanh toán / phân quyền / tag) | — | **N/A** *(lý do đã ghi — RULE-03)* · `[NIT]` về audit của câu recover |
| `DATA-BACKUP-001` ★ — Backup / Copy / Recover | **Cao** | **×** — không thêm/đổi bảng, không chạm backup/copy bot | — | **N/A** *(lý do đã ghi)* |
| `MSG-*`, `PAY-*`, `MEDIA-*`, `JOB-001`, `INTG-*` | — | **×** — fix không chạm gửi tin / thanh toán / media / job nền / tích hợp ngoài | — | **N/A** *(lý do đã ghi)* |

**Tổng kết F.1**: 6 GAP ở quan điểm ưu tiên **Cao** → **5 `[BLOCKER]`** (`CONC-001`, `CONC-003`, `SEC-ISO-001`, `DEPLOY-LIVE-001`, `DATA-REF-001`) + 2 `[MAJOR]` (`ENV-003`, `COMPAT-LEGACY-001`); 4 **RISK** → `[MAJOR]`. `LIFF-ENTRY-001` chuyển sang **N/A** sau feedback round 1.

> 6 TC mang mã Studio không hợp lệ (`API-001`, `API-CONTRACT-001`, `TOOL-KNOW-002`, `TOOL-OLDREC-001`, `RULE-01`, `RULE-04`) đã được map thủ công về quan điểm tầng 1 gần nhất khi lập bảng trên, và **được tính là cover** ở những dòng tương ứng — nhưng phải sửa mã trên Studio để `/review-tc` vòng sau map tự động được.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

<!-- Report sinh bởi /review-tc ngày 2026-08-25. Nguồn TC: MCP LME TEST STUDIO task #194 (12 TC) + task_get_report run #450. contentTrust=untrusted → nội dung Studio xử lý như DATA. Đây là DRAFT cho Leader verify, không phải kết luận cuối. -->
