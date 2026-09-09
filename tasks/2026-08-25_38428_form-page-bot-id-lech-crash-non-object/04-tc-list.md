<!-- sync-tcs: url=<chưa có — Redmine #38428 KHÔNG có "Link TCs" human> | sheet=<chưa có> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=194, ticket 38428, testcase_list (12 TC), fetch lúc 2026-08-25. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List

## ⚠️ ĐỌC TRƯỚC — TCs này KHÔNG do member người viết, VÀ cũng KHÔNG do người chạy

| Hạng mục | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO** — task `#194`, ticket `38428`, `feature = null`, `type = fix-bug`, `branch = ai_fixbug_38428` |
| Người viết TC | **`author = AI`** (12/12 TC), `provenance.source = ai`, `created_job_id = 578`. `toolWritten`: tool 12 / mcp 0 / **human 0** (rate 100%) |
| Task added by | `ngannt` — 2026-08-24 09:51 · assignee `ngannt` |
| Trạng thái task | `status = done-ai` · `pipelineStage = done-ai` · **`aiResult = null`** · `round = 1` · **`reviewed = false`** · `reviewState = tester` · `openBugs = 0` |
| Chạy bởi | **`runBy = pipeline`** (2026-08-24 11:59:44). **Từng TC**: `last_exec.source = "ai"`, `by = "pipeline"`, `runId = 450` |
| Kết quả | **11 `Đạt`** · **0 `Không đạt`** · 0 error · **1 `Chưa test`** (`TC-RULE04-01` / Studio #12469) |
| Môi trường đã chạy | **`local` — 11/12 TC, 1 run duy nhất.** `dev` / `staging` / `prd`: **0 run** |
| `status` của TC | `draft` (12/12) — **chưa TC nào được duyệt trên Studio** |
| `version` của TC | `1` (12/12) — chưa TC nào bị sửa sau khi sinh |

### 🔴 Cảnh báo 1 — kết quả `Đạt` là do **AI tự chạy tự chấm**, chưa có người verify

Khác với các task Studio khác (nơi `last_exec.source = manual`, `by = <tên QA>`), ở task này **cả 11 kết quả `Đạt` đều có `source = "ai"` và `by = "pipeline"`**. Cộng với `reviewed = false` và `status = draft` toàn bộ, nghĩa là:

- **Không có bằng chứng con người đã thao tác** bất kỳ TC nào.
- **Evidence rỗng toàn bộ** (`testcase_list` không trả về evidence) → vi phạm **RULE-02** (TC `Đạt` bắt buộc có evidence).
- Dev cũng chỉ verify ở mức **`lint`** (`php -l`, xem [03-dev-impact.md](03-dev-impact.md) §6).

⇒ **Toàn bộ chuỗi bug này hiện chưa có một lần kiểm tra thủ công nào của con người.**

### 🔴 Cảnh báo 2 — RULE-08: bug xảy ra trên PRODUCTION nhưng test 11/12 ở `local`

Exception gốc bắn từ **production `s.lmes.jp`** (36 lần), và fix này **bắt buộc kèm 1 lần recover data trên production** (xem [03-dev-impact.md](03-dev-impact.md) §5). Nhưng:

- 11/12 TC chạy `env = local`; `envAuto` cho `dev` / `staging` / `prd` đều `runs = 0`.
- 9/12 TC gắn `env_tag = local-only`.
- **TC duy nhất nhắm production — `TC-RULE04-01` (Studio #12469, `env_scope = ["prd"]`, `exec_mode = manual`) — lại là TC DUY NHẤT `Chưa test`.** Đây chính là TC đếm số bản ghi lệch `bot_id` thật trên prod, tức **điều kiện bắt buộc của RULE-04 trước khi recover / đóng ticket vẫn chưa được làm.**

### 🟠 Cảnh báo 3 — TCs được sinh **TRƯỚC** khi QA bổ sung steps tái hiện

| Mốc | Thời điểm |
|---|---|
| Studio sinh 12 TC (`created_at`) | **2026-08-24 10:34 → 10:35** |
| Pipeline chạy 11 TC (`last_exec.at`) | **2026-08-24 11:59** |
| QA (`Ngô Thúy Ngần`) thêm steps tái hiện vào Redmine (journal #132977) | **2026-08-25 13:52** ← *sau* |

Steps repro của QA là: *mở 2 tab cùng màn detail form bot A → tab 1 chuyển sang bot B → tab 2 bấm nhanh nút 「プレビュー」*. Đối chiếu 12 TC: **không TC nào dùng kịch bản 2 tab, và không TC nào chạm nút 「プレビュー」.** TC gần nhất là `TC-OUTTRUTH001-01` (NEW-3) nhưng nó chuyển bot bằng session rồi bấm nút Lưu 「登録」/「保存」, không phải race 2 tab qua プレビュー.

> Ghi chú của `/new-task`: đây là quan sát đối chiếu input, **không phải** nội dung Studio. Việc kết luận GAP / severity thuộc về `/review-tc` — nhóm quan điểm liên quan là `CONC-003` (race ở tầng giao diện, nhiều tab cùng gọi API) và luồng preview `T4` ở [03-dev-impact.md](03-dev-impact.md) §4.3.

### 🟡 Mã quan điểm Studio KHÔNG có trong `framework/checklist-lme.md`

`/review-tc` sẽ **không map được coverage** cho 6/11 mã dưới đây (phủ 6/12 TC):

| Mã Studio | TC dùng | Vấn đề | Gợi ý mã tầng 1 gần nhất |
|---|---|---|---|
| `API-001` | TC-API001-01 | Không thuộc 80 quan điểm tầng 1 | **`PERM-002`** (không bypass quyền bằng API / URL trực tiếp) · `SEC-001` |
| `API-CONTRACT-001` | TC-APICONTRACT001-01 | Không thuộc tầng 1 | `FUNC-001` · `PERM-002` (đối chứng dương) |
| `TOOL-KNOW-002` | TC-TOOLKNOW002-01 | Không thuộc tầng 1 | `REG-SPEC-001` · `FUNC-SEQ-001` |
| `TOOL-OLDREC-001` | TC-TOOLOLDREC001-01 | Không thuộc tầng 1 | **`COMPAT-LEGACY-001`** (dữ liệu đời cũ chạy song song) · `DATA-MIG-001` |
| `RULE-01` | TC-RULE01-01 | **Đây là RULE, không phải mã quan điểm** — không hợp lệ ở cột "Mã quan điểm liên kết". RULE-01 = "pattern tối thiểu 3 TC" | Nội dung TC là biên trạng thái bot (`getBotId()=0`) → `FUNC-001` / nhóm `DATA-*` biên |
| `RULE-04` | TC-RULE04-01 | **Đây là RULE, không phải mã quan điểm.** RULE-04 = "xác nhận phạm vi khi recovery" | **`DATA-MIG-001`** · `ENV-*` (khác biệt production) |

5 mã còn lại khớp checklist tầng 1, **đều ưu tiên Cao**: `FUNC-001`, `DATA-DB-001`, `OUT-TRUTH-001`, `DATA-MIG-001`, `REG-SHARED-001`.

### Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | **Normal 8** · **Abnormal 3** · **Boundary 1** |
| `tc_group` | `ui` 7 · `api` 2 · `data` 3 |
| `exec_mode` | `auto` 11 · `manual` 1 (`TC-RULE04-01`) |
| `env_tag` | `local-only` 9 · `read-only` 3 |
| `env_scope` | `["all"]` 11 · `["prd"]` 1 |
| `screen` | Màn chỉnh sửa form `/basic/form-answer/edit/{id}` (5) · Recover `form_answer_page.bot_id` (3) · Form công khai `/form-answer/{unique_key}` LIFF (2) · Endpoint `POST /form-answer/save-v3/{id}` (2) |
| `requirement_keys` | REQ-001 (2) · REQ-002 (1) · REQ-003 (3) · REQ-004 (1) · REQ-005 (2) · REQ-006 (2) · REQ-007 (1) — **7/7 requirement đều có ít nhất 1 TC** |
| `temp_id` | NEW-1 → NEW-12 **liên tục, không khuyết** ⇒ không có TC bị xoá / gộp trong lúc AI sinh |
| `bug_tickets` | rỗng 12/12 (phù hợp: 0 TC fail) |

**RULE-01 (đối chiếu nhanh của `/new-task`)**: 5 quan điểm hợp lệ đều ưu tiên **Cao** nhưng **không quan điểm nào đủ bộ 3 `Normal + Abnormal + Boundary`** — `FUNC-001` có 2 Normal; `DATA-DB-001` / `OUT-TRUTH-001` / `DATA-MIG-001` / `REG-SHARED-001` mỗi mã 1 TC. `/review-tc` sẽ đánh giá mức độ.

### Ghi chú thêm

- `spec_status = null` cho 12/12 TC → cột "Trạng thái đánh giá spec" để trống. `priority`, `catalog`, `feature`, `kho_id`, `client_ref`, `origin`, `env_hint` cũng đều `null`.
- `spec_change = 1` cho 12/12 TC.
- Task-level `durationMs = 54872` (~55 giây) nhưng `runMinutes = 83.03` — 2 con số không khớp. Nếu cần đối chiếu lịch sử run thật, gọi `task_get_report(task_id=194)` (`testcase_list` chỉ trả `last_exec` của run cuối cùng).
- `test_viewpoint_selection = null` — Studio không lưu bước chọn quan điểm cho task này.

---

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | **`AI`** (LME TEST STUDIO, job #578) — người chạy: **`pipeline`** (không phải QA người) |
| Ngày submit | `2026-08-24` (TC created_at 10:34–10:35, run 11:59) |
| Version TCs | `round 1` (Studio) — `reviewed = false`, toàn bộ TC `status = draft` |
| Link TC gốc (nếu có) | Không có Sheet human. Nguồn duy nhất: Studio task `#194` |

---

## TC List

> **16 cột canonical.** Chép **nguyên văn** từ Studio (read-only) — muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại.
> `TC No.` do `/new-task` sinh theo quy ước repo; `id` + `temp_id` Studio giữ ở cột `Ghi chú` để trace ngược.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | FUNC-001 | Normal | Lưu form đúng bot, thêm trang mới — bot_id trang = bot sở hữu form | Đăng nhập admin của bot A. Đang mở đúng bot A (bot sở hữu form). Có 1 form thuộc bot A đang mở ở màn chỉnh sửa. | 1. Mở màn chỉnh sửa form của bot A (/basic/form-answer/edit/{id}) trên browser thật.<br>2. Bấm thêm một trang mới vào form (trang chưa từng lưu, chưa có id).<br>3. Nhập tên trang và nội dung tối thiểu hợp lệ.<br>4. Bấm nút Lưu 「登録」/「保存」. | form thuộc bot A; trang mới page_name = 'TC001_trang_moi' | Lưu thành công, không có alert lỗi. Trong DB, form_answer_page vừa tạo có bot_id = form_answer.bot_id (bot A) và form_id = id form. Màn hình phản ánh trang mới đã lưu. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12458 (NEW-1) · `tc_group=ui` · `exec_mode=auto` · `env_tag=local-only` · REQ-001 · spec_ids: TICKET-38428, diff hunk 2 · note Studio: "Kiểm 3 tầng: màn hình + DB form_answer_page.bot_id/form_id + phản hồi lưu. Trigger từ browser." · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-DATADB001-01 | DATA-DB-001 | Normal | Lưu form đúng bot, sửa trang hiện có — bot_id trang không bị ghi đè | Đăng nhập admin bot A, đang mở bot A. Có form thuộc bot A với ít nhất 1 trang ĐÃ lưu (có id), bot_id trang = bot A. | 1. Mở màn chỉnh sửa form của bot A trên browser thật.<br>2. Sửa nội dung một trang đã tồn tại (ví dụ đổi page_name).<br>3. Bấm nút Lưu 「登録」/「保存」.<br>4. Truy vấn lại form_answer_page của trang đó trong DB. | trang có id sẵn; đổi page_name = 'TC002_sua_trang' | Lưu thành công. bot_id của trang trong DB GIỮ NGUYÊN = bot A (không bị ghi đè bằng getBotId()). Nội dung page_name đã cập nhật. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12459 (NEW-2) · `tc_group=ui` · `exec_mode=auto` · `env_tag=local-only` · REQ-002 · spec_ids: TICKET-38428, diff hunk 2 · note Studio: "Chốt hành vi hunk 2: nhánh UPDATE không set bot_id/form_id. So sánh bot_id trước/sau save phải bằng nhau." · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Regression: tạo form mới nhiều trang, sửa và lưu — luồng lưu không đổi | Đăng nhập admin bot A, đang mở đúng bot A. | 1. Tạo mới một form thuộc bot A.<br>2. Thêm nhiều trang (>=2), nhập nội dung, thiết lập chuyển trang cơ bản.<br>3. Lưu form.<br>4. Mở lại form, sửa một trang, thêm một trang nữa, lưu lại.<br>5. Kiểm DB các trang. | form mới bot A với 3 trang | Toàn bộ thao tác lưu thành công như trước fix. Mọi form_answer_page có bot_id = bot A, form_id đúng, page_number liên tục. Không lỗi hồi quy. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12462 (NEW-5) · `tc_group=ui` · `exec_mode=auto` · `env_tag=local-only` · REQ-007 · **regression** · note Studio: "Bảo vệ hàm dùng chung saveV3. Lưu ý branch stale thiếu #37710/#38700 nếu test trực tiếp trên branch." ⚠️ cảnh báo branch stale — cần confirm trước khi test · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-OUTTRUTH001-01 | OUT-TRUTH-001 | Abnormal | Chặn lưu khi bot đang mở khác bot sở hữu form — hiện thông báo tài khoản đã chuyển | Admin có quyền trên nhiều bot. Mở màn chỉnh sửa 1 form thuộc bot A. Chuyển bot đang mở (session) sang bot B (B != A). | 1. Mở màn chỉnh sửa form của bot A trên browser thật.<br>2. Chuyển bot đang mở của session sang bot B, giữ nguyên trang chỉnh sửa form bot A đã load.<br>3. Chỉnh một chút nội dung rồi bấm nút Lưu 「登録」/「保存」.<br>4. Quan sát thông báo trên màn hình và kiểm DB. | form thuộc bot A, session bot = bot B | FE hiển thị alert 「アカウントが切り替わっているため保存できません。ページを再読み込みしてから、もう一度お試しください。」. Form KHÔNG được lưu: dữ liệu form A không thay đổi (rollback). Không phát sinh trang lệch bot_id. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12460 (NEW-3) · `tc_group=ui` · `exec_mode=auto` · `env_tag=local-only` · REQ-003 · spec_ids: TICKET-38428, diff hunk 1 · note Studio: "Kịch bản gốc gây corruption. Guard trả HTTP 500 JSON {status:false,msg}. Verify UI (alert) + DB (không ghi). Trigger từ browser thật." · ⚠️ **KHÔNG dùng kịch bản 2 tab + nút プレビュー như steps repro của QA** · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-RULE01-01 | RULE-01 ⚠️ *(là RULE, không phải mã quan điểm)* | Boundary | Chặn lưu khi session không gắn bot hợp lệ (bot đang mở = 0/khác owner) | Mở màn chỉnh sửa form thuộc bot A. Đưa session về trạng thái getBotId() không bằng bot A (chưa chọn bot / bot đang mở = 0). | 1. Mở màn chỉnh sửa form của bot A trên browser thật.<br>2. Đưa session về trạng thái không có bot đang mở hợp lệ (getBotId()=0).<br>3. Bấm nút Lưu 「登録」/「保存」.<br>4. Quan sát thông báo và kiểm DB. | form thuộc bot A, getBotId()=0 | Save bị chặn giống cross-bot: alert msg 「アカウントが切り替わっているため保存できません…」, HTTP 500 JSON {status:false}, DB form của bot A không thay đổi. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12461 (NEW-4) · `tc_group=ui` · `exec_mode=auto` · `env_tag=local-only` · REQ-003 · note Studio: "Biên trạng thái bot. Nếu không dựng được getBotId()=0 qua UI thì phủ ở TC api; nêu mismatch, không tự đổi sang API để pass." · ⚠️ mã quan điểm không hợp lệ — gợi ý `FUNC-001` / nhóm biên `DATA-*` · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-FUNC001-02 | FUNC-001 | Normal | LINE user mở form có trang bot_id đúng — render bình thường, không crash | Tồn tại form thuộc bot A đã lưu bằng luồng đã fix; trang page_number=1 có bot_id = bot A (= form_answer.bot_id). | 1. Mở URL công khai của form /form-answer/{unique_key} (ngữ cảnh LINE user/LIFF) trên browser.<br>2. Quan sát màn hình render form và trang đầu tiên. | form bot A, unique_key hợp lệ | Form render đầy đủ trang page_number=1, không xuất hiện lỗi 500 'Trying to get property id of non-object' (FormAnswerService dòng 171). | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12465 (NEW-8) · `tc_group=ui` · `exec_mode=auto` · `env_tag=read-only` · REQ-004 · spec_ids: TICKET-38428, source FormAnswerService.php:164-171 · note Studio: "Verify gián tiếp fix: render layer không sửa, an toàn đến từ bot_id trang đúng. Browser thật hoặc kiểm tĩnh route→service với dữ liệu seed." · ⚠️ note cho phép "kiểm tĩnh" thay browser thật — cần xác nhận thực tế đã chạy cách nào · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 ⚠️ *(không có ở tầng 1)* | Abnormal | Tái hiện bug: trang có bot_id lệch làm form công khai crash | Seed 1 form thuộc bot A nhưng trang page_number=1 có bot_id LỆCH (=0 hoặc =bot B), mô phỏng record cũ trước fix (chưa recover). | 1. Chuẩn bị dữ liệu: form_answer.bot_id = A, form_answer_page.page_number=1 có bot_id != A.<br>2. Mở URL công khai /form-answer/{unique_key} của form đó. | form A; trang page_number=1 bot_id = 0 (lệch) | Tái hiện đúng lỗi ticket: query WHERE bot_id=form.bot_id không thấy trang → $formPage=null → 'Trying to get property id of non-object' tại FormAnswerService.php:171 (HTTP 500). | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12466 (NEW-9) · `tc_group=ui` · `exec_mode=auto` · `env_tag=local-only` · REQ-005 · spec_ids: TICKET-38428, FormAnswerService.php:164-171, redmine journal 2026-07-02T10:21:03Z · note Studio: "Record CŨ giữ shape lỗi vẫn crash vì render layer KHÔNG được vá. TC tái hiện bug bắt buộc. Chỉ seed dữ liệu, không sửa source." · ⚠️ **Expected = vẫn crash 500** — mâu thuẫn với bản #124641 nói "thêm guard ở renderForm"; xem cảnh báo input #1 ở [03-dev-impact.md](03-dev-impact.md) · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-APICONTRACT001-01 | API-CONTRACT-001 ⚠️ *(không có ở tầng 1)* | Normal | Endpoint save-v3 đúng bot, tạo trang mới — page bot_id = form owner | Session admin với bot đang mở = bot A. Form_id thuộc bot A. | 1. Gửi POST /form-answer/save-v3/{form_id_của_bot_A} với session bot = bot A và payload chứa trang mới (không có id).<br>2. Ghi lại HTTP status/body.<br>3. Truy vấn form_answer_page vừa tạo. | form_id thuộc bot A; session bot = A; 1 trang mới | Request lưu thành công (không trả nhánh 500 guard). form_answer_page mới có bot_id = form_answer.bot_id (bot A) và form_id đúng. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12464 (NEW-7) · `tc_group=api` · `exec_mode=auto` · `env_tag=local-only` · REQ-001 · spec_ids: TICKET-38428, EP-saveV3, diff hunk 2 · note Studio: "Đối chứng dương cho guard: cùng bot thì qua và ghi đúng bot_id." · gợi ý mã tầng 1: `FUNC-001` / `PERM-002` · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-API001-01 | API-001 ⚠️ *(không có ở tầng 1)* | Abnormal | Endpoint save-v3 chặn cross-bot — trả JSON lỗi HTTP 500 và rollback | Có session admin hợp lệ với bot đang mở = bot B. Tồn tại form_id thuộc bot A (A != B). | 1. Gửi POST /form-answer/save-v3/{form_id_của_bot_A} với session bot = bot B (payload lưu form hợp lệ về shape).<br>2. Ghi lại HTTP status và body JSON.<br>3. Truy vấn DB form_answer_page và form_answer của form A. | form_id thuộc bot A; session getBotId()=bot B | HTTP 500, body JSON {status:false, msg:「アカウントが切り替わっているため保存できません。ページを再読み込みしてから、もう一度お試しください。」}. DB form A KHÔNG thay đổi (rollback). | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12463 (NEW-6) · `tc_group=api` · `exec_mode=auto` · `env_tag=local-only` · REQ-003 · spec_ids: TICKET-38428, EP-saveV3, diff hunk 1 · note Studio: "TC api tách riêng: guard nằm ở endpoint, chống bypass gọi trực tiếp. Input đúng shape mà bị chặn sạch." · gợi ý mã tầng 1: `PERM-002` / `SEC-001` · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-DATAMIG001-01 | DATA-MIG-001 | Normal | Query chẩn đoán các trang có bot_id lệch với bot sở hữu form | Truy cập DB (read-only) của môi trường cần kiểm. | 1. Chạy truy vấn: `SELECT fa.id form_id, fa.bot_id form_bot, fp.id page_id, fp.page_number, fp.bot_id page_bot FROM form_answer fa JOIN form_answer_page fp ON fp.form_id=fa.id WHERE fp.bot_id <> fa.bot_id`.<br>2. Đếm số bản ghi lệch và ghi lại danh sách. | không (chỉ đọc) | Truy vấn trả về đúng tập trang có bot_id != bot sở hữu form (các record cần recover). Sau fix không phát sinh bản ghi lệch mới. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12467 (NEW-10) · `tc_group=data` · `exec_mode=auto` · `env_tag=read-only` · REQ-006 · spec_ids: TICKET-38428, RULE-04, redmine journal 2026-07-02T11:20:18Z · note Studio: "RULE-04: xác định phạm vi thực tế trước khi recover/đóng ticket. Read-only." · ⚠️ **chạy ở `local` → chưa thoả RULE-04** (phạm vi thật là production, xem TC-RULE04-01) · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-TOOLOLDREC001-01 | TOOL-OLDREC-001 ⚠️ *(không có ở tầng 1)* | Normal | Khôi phục trang lệch bot_id rồi mở form — render đúng cho LINE user (cũ & mới song song) | Có sẵn 1 form (record cũ) với trang page_number=1 bot_id lệch. Có 1 form khác thuộc bot B không liên quan để đối chứng âm. | 1. Chạy recover: `UPDATE form_answer_page fp JOIN form_answer fa ON fp.form_id=fa.id SET fp.bot_id = fa.bot_id WHERE fp.bot_id <> fa.bot_id`.<br>2. Mở lại URL công khai /form-answer/{unique_key} của form vừa recover.<br>3. Kiểm tra form/bot B không liên quan trước và sau recover. | record cũ lệch; form đối chứng thuộc bot B | Sau recover, trang có bot_id = form owner; mở form công khai render bình thường, không còn crash dòng 171. Dữ liệu form/bot B KHÔNG bị thay đổi (đối chứng âm). Cả record cũ (đã recover) và mới (sau fix) cùng render đúng. | Đạt | | LOCAL | pipeline | 2026-08-24 | | | Studio #12468 (NEW-11) · `tc_group=data` · `exec_mode=auto` · `env_tag=local-only` · REQ-005 · spec_ids: TICKET-38428, redmine journal RECOVER DATA, RULE-09 · note Studio: "DATA-MIG-001 + đối chứng âm: WHERE khớp đúng scope trang lệch, không đụng bản ghi khác. Verify DB bot_id + render UI." · gợi ý mã tầng 1: `COMPAT-LEGACY-001` / `DATA-MIG-001` · ⚠️ query recover **chưa chạy trên production** · ⚠️ `last_exec.source=ai`, chưa có evidence |
| TC-RULE04-01 | RULE-04 ⚠️ *(là RULE, không phải mã quan điểm)* | Normal | Thống kê phạm vi record lệch trên production trước khi đóng ticket | Quyền truy cập read-only DB production (s.lmes.jp). Chỉ thực hiện bởi người có thẩm quyền. | 1. Trên production, chạy truy vấn đếm trang lệch bot_id (như TC chẩn đoán).<br>2. Đối chiếu số lượng thực tế với con số 6 ở DB dev.<br>3. Ghi nhận danh sách để quyết định recover trên prod. | không (chỉ đọc trên prod) | Có được số lượng và danh sách record lệch thực tế trên prod (có thể khác 6 của dev). Điều kiện bắt buộc trước khi recover/đóng ticket. | **Chưa test** | | **PRD (dự kiến)** | | | | | Studio #12469 (NEW-12) · `tc_group=data` · `exec_mode=manual` · `env_tag=read-only` · `env_scope=["prd"]` · REQ-006 · spec_ids: TICKET-38428, RULE-04, redmine description "36 lần cảnh báo" · note Studio: "Manual vì cần môi trường prod thật và quyền truy cập kiểm soát; read-only. Số record prod chưa xác nhận." · 🔴 **`last_exec = null` — TC production DUY NHẤT và cũng là TC DUY NHẤT chưa chạy; RULE-04 chưa thoả** |

---

## Requirements Studio (đối chiếu coverage với `03-dev-impact.md`)

| REQ | Tiêu đề | Category | Risk | TC phủ |
|---|---|---|---|---|
| REQ-001 | Lưu form cùng bot: trang tạo mới có bot_id = bot sở hữu form | ui | High | TC-FUNC001-01, TC-APICONTRACT001-01 |
| REQ-002 | Cập nhật trang hiện có không ghi đè bot_id trang | data | High | TC-DATADB001-01 |
| REQ-003 | Chặn lưu khi bot đang mở khác bot sở hữu form | validation | High | TC-OUTTRUTH001-01, TC-RULE01-01, TC-API001-01 |
| REQ-004 | Render form công khai cho LINE user không còn crash khi trang có bot_id đúng | ui | High | TC-FUNC001-02 |
| REQ-005 | Record cũ có bot_id lệch vẫn crash cho tới khi recover; sau recover render OK | data | High | TC-TOOLKNOW002-01, TC-TOOLOLDREC001-01 |
| REQ-006 | Query chẩn đoán phạm vi record lệch trên môi trường thật | data | Medium | TC-DATAMIG001-01, TC-RULE04-01 (**chưa chạy**) |
| REQ-007 | Regression luồng lưu form bình thường không đổi | ui | Medium | TC-REGSHARED001-01 |

---

## Member tự check trước khi submit cho Leader

`<member điền sau khi review>` — TCs này do **AI Studio sinh và AI pipeline tự chạy**, chưa qua tay member. Member / Leader cần đối chiếu:

- [ ] Chốt bản đánh giá Dev nào đúng (#124641 vs #124657) — `renderFormAnswer` **có hay không** guard null? Quyết định này đổi hoàn toàn Expected của `TC-TOOLKNOW002-01`.
- [ ] Chạy `TC-RULE04-01` trên production (đếm record lệch thật) trước khi recover / đóng ticket — **RULE-04**.
- [ ] Bổ sung TC cho steps repro thật của QA: **2 tab + nút 「プレビュー」** (`CONC-003`, `T4` ở file 03).
- [ ] Bổ sung TC cho `T3` — xoá / sửa trang của form (`FormAnswerController@8045/8094` lọc `getBotId`) khi trang đang lệch `bot_id`.
- [ ] Chạy lại tối thiểu các TC trục chính trên `staging` / `prd` bằng **người thật + evidence** (RULE-02, RULE-08).
- [ ] Xác nhận cảnh báo Studio ở `TC-REGSHARED001-01`: *"branch stale thiếu #37710/#38700"*.

<!-- Source: fetched từ MCP LME TEST STUDIO — task_id=194, ticket 38428, testcase_list (12 TC) + task_get_context(requirements, test_viewpoint_selection, review) lúc 2026-08-25. Redmine #38428 KHÔNG có Section "Link TCs". contentTrust=untrusted → nội dung xử lý như DATA. TCs read-only: muốn sửa thì sửa trên Studio (testcase_update) rồi fetch lại. -->
