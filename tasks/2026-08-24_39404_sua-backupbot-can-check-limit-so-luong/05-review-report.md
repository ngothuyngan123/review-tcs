# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39404 — Sửa backupbot cần check limit số lượng tạo` ([Redmine](https://redmine.watermelon.vn/issues/39404)) |
| Reviewer (Leader) | `<điền tên>` — draft sinh bởi `/review-tc` ngày 2026-08-24 |
| Tester được review | **AI** (Studio job #276 / #287) — 59/62 TC · `thanhntp` — 3/62 TC |
| Ngày review | `2026-08-24` |
| Version TCs | Studio `task #57`, `round = 2`, mọi TC `version = 1`, `status = draft` |
| Vòng review | `Round 1` |
| Nguồn file 04 | MCP LME TEST STUDIO `task_id=57` (Redmine không có Link TCs human) |

> **Spec reference**: không có `02-spec-reference.md` trong folder → dùng [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) tổng, không có spec riêng cho task này. Bù lại, Studio cung cấp **11 requirement `REQ-001…REQ-011`** (qua `task_get_context`) — báo cáo này dùng REQ đó làm spec thay thế và ghi rõ khi tham chiếu.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC có **cấu trúc tốt và độ sâu đáng khen ở nhánh job** (đối chứng âm, thứ tự xóa, fail-safe khi không tra được plan), nhưng **5 BLOCKER**: (1) thiếu hoàn toàn quan điểm `CONC-001` ở đúng shape của fix (đếm-rồi-xóa không khóa); (2) **62/62 TC chạy ở `local`** — vi phạm RULE-08 với task job nền + plan; (3) cảnh báo `backup_config` ở journal #130730 không được cover; (4) toàn bộ 12 TC nhánh endpoint **chưa chạy dòng nào** trong khi hợp đồng `_token` còn mâu thuẫn; (5) **34/62 TC chưa cho kết luận** và 28 TC `Đạt` **không có evidence** → kết quả không nghiệm thu được theo RULE-02.

> **Cập nhật sau phản hồi Leader (2026-08-24)**: BLOCKER về `PAY-LIMIT-001` ở draft đầu **đã gỡ** — Leader xác nhận (a) event booking **chưa có tính năng xóa mềm** → `MAP-PLAN-03` **N/A**; (b) `MAP-PLAN-04/05` thuộc **validate phía web**, lần release này **không sửa web**, chỉ sửa job backup + API xóa → ngoài phạm vi. 3 TC đề xuất tương ứng đã bỏ khỏi §5.

---

## 2. Tóm tắt cho member

Bộ TC này **mạnh hơn mặt bằng chung** ở nhánh job: nhóm `TOOL-NEGCTRL-001` (đối chứng âm: bot chứng / bot nguồn / event loại cũ không bị đụng) và `TC-JOB002-06` (không tra được plan thì hỏng an toàn, không xóa) là đúng tư duy adversarial mà một fix xóa dữ liệu cần có — giữ nguyên cách nghĩ này. `REG-SHARED-001` x3 đối chiếu điều kiện tính limit giữa web và job cũng bắt đúng chỗ dễ lệch nhất.

Vấn đề lớn nhất **không nằm ở việc thiếu ý tưởng test, mà ở 4 chỗ**: (a) fix này là "đếm rồi xóa" nhưng **không có TC nào chạy 2 luồng đồng thời** — đúng kịch bản `CONC-001` #4; (b) **regression các nhóm dữ liệu khác chỉ dừng ở mức đếm bản ghi** — TC-TOOLNEGCTRL001-04 rà 8 nhóm bằng cách đếm số và mở màn admin, còn **action / bill / conversion / site_script không có TC nào**, và **câu trả lời form (`form_answer`) 0/62 TC** dù nằm trong mapping `backup_config`; (c) **toàn bộ chạy ở `local`** trong khi task chạm job nền và gói cước — RULE-08 nói thẳng là không được kết luận từ môi trường này; (d) **hơn nửa bộ TC (34/62) chưa chạy** và 28 TC báo `Đạt` nhưng cột Evidence trống, nên con số `aiResult = pass` của Studio hiện chưa dùng làm bằng chứng nghiệm thu được.

Việc cần làm trước vòng 2: chạy nốt nhánh `api` (12 TC) sau khi chốt giá trị `_token`, bổ sung 16 TC ở §5, và chạy lại bộ smoke trên **staging + production** thay vì local.

---

## 3. Coverage Matrix

> Map **quan điểm** đọc thẳng ở cột `Mã quan điểm liên kết`; map **impact BUG/F/D/T** suy luận từ Tiêu đề / Tiền đề / Các bước / Kết quả mong đợi.
> Cột **Exec** = trạng thái chạy thực tế (`pass` / `skip` / `blocked`) — đưa vào matrix vì nó quyết định impact đó đã thực sự được verify hay mới chỉ *có TC trên giấy*.

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Exec (pass/skip/blocked) | Status |
|---|---|---|---|---|---|---|
| **BUG** — job clone `b_event_detail` không check limit theo plan | Fix | — | TC-FUNC001-01, TC-FUNC001-02, TC-FUNC001-03, TC-OUTTRUTH001-01 | 4 | 3 / 1 / 0 | **OK** |
| **F1** — `startBackup` (thêm lời gọi `checkLimitBEventDetail`) | Function | Direct | TC-FUNC001-01/02/03, TC-FUNCSEQ001-01, TC-JOB002-02, TC-JOB002-05 | 6 | 4 / 1 / 1 | **OK** |
| **F2** — `checkLimitBEventDetail` / `getLimitBEventDetail` / `isUserCreatedBeforeNewFreePlan` | Function | Direct | TC-RULE09-01/02, TC-FUNC004-02/03/04/05, TC-REGSHARED001-02, TC-FUNCDATE001-01, TC-JOB002-06, TC-NOVP-01, TC-NOVP-02 | 11 | 7 / 4 / 0 | **RISK** — toàn bộ nhánh **free mới** và **biên mốc 2021-07-01** đều `skip`; ⚠️ TC-REGSHARED001-01 (Studio #9365) **đã bị xóa khỏi Studio 2026-08-24** |
| **F3** — `clearBEventDetail` + `ISnslineService.clearBEventDetail` + `ClearBEventDetailResponse` | Function | Direct | TC-API001-01, TC-SEC001-01/02, TC-SEC002-01, TC-SECISO001-01, TC-SECINJECT001-01, TC-TOOLERRHYG001-01/02, TC-CONC001-01, TC-COMPATLEGACY001-01, TC-PERM002-01, TC-FUNC003-01, TC-JOB002-03/04, TC-JOB001-01, TC-DEPLOYLIVE001-01 | 16 | 0 / 12 / 4 | **GAP thực thi** — **0/16 TC cho kết luận nào**. Xem BLOCKER-4 |
| **F4** — `findIdNewEventByBotIdOrderByIdDesc`, `findContractTypeById`, `findCreatedAtById` | Function | Direct | TC-DATADB001-01, TC-FUNC004-03, TC-TOOLOLDREC001-01, TC-DATARETENTION001-01, TC-REGSHARED001-01/02, TC-FUNCDATE001-01, TC-JOB002-06 | 8 | 5 / 3 / 0 | **OK** |
| **D1** — `Constants.PlanLimit` (free 2 / standard 10 / mốc 2021-07-01) | Data | CREATE | TC-FUNC004-02/03/04/05, TC-RULE09-01/02, TC-FUNCDATE001-01, TC-REGSHARED001-02 | 8 | 4 / 4 / 0 | **RISK** — nhánh free (limit 2) chưa chạy |
| **D2** — `b_event_detail` bản ghi thừa bot đích (DELETE qua `api/clear_b_event_detail`) | Data | DELETE | TC-DATADB001-01, TC-DATAREF001-01/02/03, TC-TOOLNEGCTRL001-01/02/03/04/05, TC-DATARETENTION001-01, TC-NOVP-03 | 11 | 9 / 2 / 0 | **OK** — `WHERE` scope 2 tài khoản có TC-TOOLNEGCTRL001-01 |
| **T1** — Backup bot standard mới → còn đúng 10 | Feature | *(Dev không ghi)* | TC-FUNC001-02, TC-FUNC004-03, TC-OUTTRUTH001-01, TC-JOB002-02, TC-UI003-01 | 5 | 5 / 0 / 0 | **OK** |
| **T2** — Backup free mới → còn 2; plan cũ + pro **không** xóa | Feature | *(Dev không ghi)* | TC-FUNC001-03, TC-OUTTRUTH001-02, TC-FUNC004-04, TC-FUNC004-05, TC-RULE09-01, TC-RULE09-02, TC-REGSHARED001-02 | 7 | 2 / 5 / 0 | **RISK** — nhánh **pro + plan cũ** đã pass; nhánh **free mới** 0/4 chạy |
| **T3** — Event booking 「イベント予約」 của bot đích | Feature | *(Dev không ghi)* | TC-UI003-01, TC-OUTTRUTH001-01/02, TC-FUNC004-01, TC-DATAHIST001-01, TC-PERM001-01 | 6 | 5 / 1 / 0 | **OK** |
| **T4** — Phụ thuộc `api/clear_b_event_detail` bên sns-line | Feature | *(Dev không ghi)* | 12 TC nhóm `api` + TC-DEPLOYLIVE001-01/02, TC-JOB002-03/04, TC-JOB001-01, TC-OBS001-01 | 18 | 0 / 13 / 5 | **GAP thực thi** — 0/18 kết luận |

### Nhận xét matrix

- **Không có GAP thiết kế** ở tầng impact — mỗi F/D/T đều có ≥ 1 TC map được. Điểm yếu nằm ở **chiều sâu quan điểm** (§F.1), **độ phủ regression** (GAP-13) và **thực thi** (BLOCKER-4, BLOCKER-5), không ở việc thiếu TC cho impact.
- **F3 và T4 có 17-18 TC nhưng 0 kết luận** — coverage matrix mechanical sẽ tick `OK`, thực tế là vùng chưa được verify dòng nào. Đây đúng là cái bẫy mà [coverage-matrix.md](../../framework/coverage-matrix.md) §"Giới hạn" cảnh báo.

### ORPHAN TCs

| TC No. | Tiêu đề | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC-TOOLBRANCH001-01 | Xác minh đúng nhánh và commit của job trước khi chạy bộ kiểm thử | **Meta-TC / harness gate** (REQ-011) — verify môi trường test, không verify sản phẩm | **Giữ** nhưng tách sang mục "Điều kiện tiền đề của bộ TC", không đếm vào coverage |
| TC-DEPLOYLIVE001-02 | Xác minh endpoint xóa đã tồn tại bên web trước khi chạy nhóm endpoint | Như trên (REQ-011) | **Giữ** — tách khỏi bộ TC sản phẩm |
| TC-DATAMIG001-01 | Cấu trúc bảng không thay đổi sau khi triển khai | Verify điều Dev khẳng định **không** đụng (D1: "không có DDL/migration") | **Giữ** — hợp lệ như negative control cho D1 |
| TC-DATAMIG001-02 | Cấu hình danh sách bảng được copy không bị đổi | Như trên | **Giữ** — và **mở rộng** theo BLOCKER-3 + GAP-13 (journal #130730) |

> Không phát hiện TC lạc chủ đề thật sự. Không dính **AP-5** (layer-downstream over-coverage): mọi TC đều trace về code path Dev đã sửa hoặc về negative control có chủ đích.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Kết hợp 3 shape**: (a) **Validation / thêm check** — `checkLimitBEventDetail` đếm rồi so ngưỡng theo plan; (b) **Generic catch-all** — mục 3 ghi *"được bọc try/catch riêng… lỗi ở bước này không làm fail luồng backup"*; (c) **Shared logic** — điều kiện tính plan phải trùng logic web (`BookingEventDayManagementController`, `checkPlanFreeBotLimitFeature`) |
| **Trigger space cần cover** (shape b — generic catch) | 6: endpoint chưa deploy · endpoint 5xx · web timeout/không phản hồi · lỗi giữa chừng (xóa được một phần) · không tra được plan · **error code chưa biết (fallback)** |
| **Số trigger TCs hiện cover** | **5/6** — TC-DEPLOYLIVE001-01 · TC-JOB002-03 · TC-JOB001-01 · TC-JOB002-04 · TC-JOB002-06. **Thiếu**: unknown/không lường trước (VD endpoint trả 200 nhưng body báo lỗi, trả HTML thay JSON, trả `ClearBEventDetailResponse` sai schema) |
| **Trigger space cần cover** (shape a — validation) | Luồng vào chạm limit: **tạo mới ✓** · **copy/backup ✓** · **khôi phục data xóa mềm — N/A** *(Leader xác nhận event booking chưa có xóa mềm)* · **import/API tạo event trực tiếp ✗** · biên `0 / dưới / = / +1` ✓ (TC-FUNC004-02/03/04) |
| **Trigger space cần cover** (shape c — shared) | Danh sách nơi ảnh hưởng **do DEV cung cấp** — **KHÔNG có** (mục 3 chỉ khẳng định "1 caller duy nhất"). TC-REGSHARED001-02/03 tự dựng đối chiếu, nhưng không thay được danh sách của Dev — và **TC-REGSHARED001-01 (Studio #9365) đã bị xóa khỏi Studio 2026-08-24** |
| **KH report dạng** | **Có root cause cụ thể** — description là **yêu cầu đổi logic từ Dev lead**, nêu thẳng bảng/plan/limit/endpoint. **Không** phải symptom-only |
| **Alternative root causes cần verify** | N/A cho AP-2. Nhưng có **1 nhánh nguyên nhân song song chưa đóng**: journal #130730 (`backup_config` map sai cột `booking_event_id`) — nếu đúng thì tập bản ghi được clone/đếm/xóa khác hẳn đánh giá ở file 03 |
| **Anti-patterns dính** | **AP-6 ✔ dính** (mục 3 caller list rỗng) · **AP-4 ✔ dính một phần** (có commit hash `0022f93…` nhưng **không có PR URL** để đọc diff; TC-TOOLBRANCH001-01 giảm nhẹ nhưng cũng đang là TC chưa đủ để thay việc review diff) · **AP-1 ✘ không dính** (5 trigger ≥ 3) · **AP-2 ✘ không dính** · **AP-3 ✘ không dính** (regression T2 có edge state: TC-TOOLOLDREC001-01 bot vượt limit từ trước) · **AP-5 ✘ không dính** |

### Câu hỏi adversarial còn treo — Leader hỏi Dev trước vòng 2

1. **`checkLimitBEventDetail` có khóa/transaction không?** Fix là *đọc-đếm-rồi-xóa*. Nếu 2 job backup cùng chạy vào 1 bot đích, cả hai cùng thấy "vượt 5" và cùng xóa 5 → xóa mất 10. Có `SELECT … FOR UPDATE` / advisory lock / hàng đợi theo `bot_id` không?
2. ~~**`b_event_detail` có soft delete không?**~~ — **ĐÃ TRẢ LỜI (Leader, 2026-08-24)**: event booking **chưa có tính năng xóa mềm** → `MAP-PLAN-03` không áp dụng. Nếu sau này bổ sung xóa mềm thì phải mở lại câu hỏi này.
3. **`_token` cuối cùng là hằng nào?** Description ghi `ConfigFile.API_CERT_KEY`, journal đánh giá ghi `ConfigFile.API_SERVER_CERT`. Chốt trước khi chạy 12 TC nhánh `api`.
4. **Journal #130730 thuộc phạm vi ticket này không?** `backup_config` bảng `image_map_items` sai cột `booking_event_id` → `b_event_detail`.
5. **Việc xóa event có ghi lịch sử thao tác không?** Nếu có màn `操作履歴` cho event booking, job xóa dưới danh nghĩa ai?
6. **Bot nguồn lớn nhất thực tế có bao nhiêu event bản mới?** TC-JOB002-02 giả định 30 lần gọi endpoint tuần tự — cần con số thật để biết có timeout/rate-limit không.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-1 — `CONC-001` (Cao): fix "đếm rồi xóa" nhưng không có TC nào chạy 2 luồng đồng thời.**
  `CONC-001` yêu cầu **4 kịch bản**; bộ TC chỉ có **1** (TC-CONC001-01 — gọi lại endpoint với cùng id, tức idempotency tầng API). Thiếu đúng kịch bản #4 *"batch đa luồng cùng chạm 1 giới hạn dùng chung"* — chính là hình dạng của fix này. Rủi ro cụ thể: 2 backup đồng thời vào cùng bot đích → mỗi luồng đếm thấy vượt 5 → mỗi luồng xóa 5 → mất 10 bản ghi, trong đó có event có sẵn của khách.
  → **Bổ sung TC-CONC001-02/03/04** (§5). Song song **hỏi Dev câu 1** ở §3.5.

- **[BLOCKER] GAP-2 — RULE-08 / `ENV-003` (Cao): 62/62 TC chạy ở `env = local`, không TC nào ghi PRODUCTION.**
  Task chạm **job nền** (`BackupBotTask`) và **gói cước / hợp đồng** — cả hai đều nằm trong danh mục RULE-08 *"không được kết luận từ staging"* (huống chi local). [Catalog D `ENV-JOB`](../../framework/catalog-lme.md): dev/staging chạy **1 job all**, production tách **3 job độc lập** → tranh chấp giữa các job chỉ lộ ra trên production. Studio `envAuto` xác nhận `dev` 0 run · `staging` 0 run · `prd` 0 run; 55/62 TC gắn `env_tag = local-only`.
  → **Bổ sung TC-ENV003-01/02/03** (§5) + chạy lại bộ smoke job trên staging và production.

- **[BLOCKER] GAP-3 — Cảnh báo journal #130730 không được cover ở bất kỳ TC nào.**
  Ngày 2026-08-20 reporter ghi: *"CẢNH BÁO: backup_config bảng `image_map_items` cần sửa lại config đang bị sai cột `booking_event_id`"* với mapping `"booking_event_id":"b_event_detail"`. Journal này đến **15 ngày sau** báo cáo đánh giá ảnh hưởng và **không** xuất hiện trong mục 4.1/4.2/4.3 của `03-dev-impact.md`. Nếu config map sai, **tập bản ghi `b_event_detail` được clone — và do đó được đếm và bị xóa — khác với giả định của cả fix lẫn bộ TC**. TC gần nhất là TC-NOVP-03 (setting mở event trong richmenu/button/image map) và nó đang `skip`.
  → **Bổ sung TC-DATABACKUP001-02** (§5) + **chạy TC-NOVP-03** + hỏi Dev câu 4 ở §3.5.

- **[BLOCKER] GAP-4 — Nhánh endpoint (F3/T4, REQ-006 risk High): 0/16 TC cho kết luận, trong khi hợp đồng `_token` còn mâu thuẫn.**
  12/12 TC nhóm `api` = `skip`, 4 TC job xử lý lỗi = `blocked`. Đây là toàn bộ phần verify hợp đồng API, xác thực, và giới hạn phạm vi bot — đúng chỗ `SEC-001` / `SEC-ISO-001` / `PERM-002` / `SEC-INJECT-001`. Đồng thời `03-dev-impact.md` §5 ghi nhận mâu thuẫn chưa chốt: description nói `ConfigFile.API_CERT_KEY`, đánh giá nói `ConfigFile.API_SERVER_CERT`. Chạy 12 TC với hằng số sai sẽ cho kết quả sai cả hai chiều.
  → **Chốt `_token` (câu 3 §3.5) → chạy đủ 12 TC `api` → mới kết luận được F3/T4.**

- **[BLOCKER] GAP-5 — Kết quả không nghiệm thu được: 34/62 TC chưa cho kết luận + 28 TC `Đạt` không có evidence (RULE-02).**
  Studio báo `aiResult = pass`, `exec: pass 28 / fail 0 / other 34 / **untested 0**` — con số `untested = 0` dễ đọc nhầm thành "đã test hết", thực tế `other = 34` gồm **26 `skip` + 8 `blocked`** = **54,8% bộ TC chưa cho kết luận nào**. Với 28 TC `pass`: cột `Evidence thực tế` **trống toàn bộ** (payload `testcase_list` không trả về), `Ghi chú` không ghi **loại evidence bắt buộc**. RULE-02: *"Chỉ tick Đạt khi đã đính kèm đúng loại bằng chứng… Không chấp nhận 'đã xem, OK'"*. Thêm nữa 19/62 kết quả có `last_exec.source = ai` (pipeline AI chấm) dưới tên `thanhntp`.
  → Trước vòng 2: đính evidence cho 28 TC `pass`, hoặc hạ về `Chưa test`. Ghi rõ TC nào do người chạy, TC nào do pipeline.

### 4.2 Major (nên fix)

- **[MAJOR] RULE-01 — 16/20 quan điểm ưu tiên Cao thiếu ≥ 1 loại case, không TC nào ghi lý do.** Chỉ còn **`OUT-TRUTH-001`** đủ 3 loại (`REG-SHARED-001` đủ 3 loại ở thời điểm review, nhưng **mất TC Abnormal** sau khi Studio #9365 bị xóa ngày 2026-08-24 — xem §9). Chi tiết ở bảng §F.1. Đáng chú ý: `FUNC-001` (3 TC **toàn Normal**), `FUNC-004` (5 TC **toàn Boundary**), `SEC-001`/`SEC-002`/`SEC-ISO-001`/`PERM-001`/`PERM-002`/`CONC-001`/`JOB-001`/`COMPAT-LEGACY-001` (mỗi mã **chỉ Abnormal**). → Bổ sung, hoặc ghi lý do ở `Ghi chú` từng TC.
- **[MAJOR] AP-6 — mục 3 `03-dev-impact.md` không list caller thật.** Chỉ khẳng định *"method mới, chỉ có 1 caller duy nhất là `startBackup`"* mà không liệt kê caller **của chính `startBackup`**. Nếu `startBackup` có nhiều đường trigger (job schedule / retry / manual từ màn 「データコピー」) thì mỗi đường là một lần `checkLimitBEventDetail` chạy. → Yêu cầu Dev cung cấp danh sách (`REG-SHARED-001` bắt buộc điều này).
- **[MAJOR] AP-4 — không có PR URL, chỉ có commit hash `0022f93d066b9a949e275467cd4d5977e1b97f01`.** Không đọc được diff → không xác minh được fix là *validation cụ thể* hay *catch-all*, và không kiểm được có lock/transaction không. TC-TOOLBRANCH001-01 có grep source nhưng chỉ xác nhận "tìm thấy bước kiểm giới hạn", không thay được review diff. → Yêu cầu Dev cung cấp PR link.
- **[MAJOR] GAP-7 — `STATE-001` (Cao): thiếu TC job bị dừng đột ngột giữa 2 bước ghi dữ liệu.** Fix đặt `checkLimitBEventDetail` **sau** khi `backupHistory` đã set `STATUS_COMPLETED_BACKUP` → nếu job bị kill / restart / OOM / deploy ngay giữa 2 bước, lần copy vĩnh viễn ở trạng thái "hoàn tất" nhưng bot đích vượt limit mãi mãi, **không có cơ chế nào chạy lại**. TC-JOB002-04 chỉ cover endpoint lỗi, không cover job chết. → Bổ sung TC-STATE001-01 (§5).
- **[MAJOR] GAP-8 — `DATA-AUDIT-001` (Cao): không TC nào kiểm lịch sử thao tác khi job xóa event.** Event booking chứa lượt đặt chỗ của khách (TC-DATARETENTION001-01 nhắc "3 lượt đặt"). Job xóa dữ liệu này mà không rõ có ghi `操作履歴` không, ghi dưới danh nghĩa ai. → Bổ sung TC-DATAAUDIT001-01 (§5). *Leader xác nhận trước: spec có yêu cầu audit log cho event booking không — nếu không thì hạ xuống NIT.*
- **[MAJOR] GAP-9 — `DATA-BACKUP-001` (Cao) mới cover một nửa.** Trigger khớp tuyệt đối (*"chạm backup / copy bot"*). Có TC-TOOLNEGCTRL001-03/04 (event giữ lại đủ dữ liệu con; nhóm dữ liệu khác copy đủ), nhưng **thiếu điểm (3) của quan điểm: query DB đối chiếu TỪNG FIELD nguồn↔đích** — cụ thể **ngày lần đầu vs ngày tiếp theo không được trùng**, **path ảnh không có `//`**, **foreign key**. → Bổ sung TC-DATABACKUP001-01 (§5).
- **[MAJOR] GAP-13 — Regression các nhóm dữ liệu khác của backup mới ở mức *đếm bản ghi*, và 4 nhóm trong `backup_config` không có TC nào.** Cả bộ 62 TC chỉ có **đúng 1 TC** làm regression cho phần backup còn lại: TC-TOOLNEGCTRL001-04 — rà 8 nhóm (thư mục, tag, template, tin nhắn tự động, rich menu, kịch bản bước, thông tin bạn bè, biểu mẫu) bằng cách **đếm số bản ghi + mở màn admin**. Đối chiếu mapping `backup_config` ở journal #130730 (`template_id`, `action_id`, `form_answer_id`, `bill_id`, `booking_event_id`, `site_script_id`, `conversion_id`):
  - **`form_answer` (câu trả lời biểu mẫu) — 0/62 TC** dù nằm trong mapping. TC-TOOLNEGCTRL001-04 chỉ đếm *biểu mẫu*, không đếm *câu trả lời*.
  - **`action` (`t_actions`) — 0/62 TC** · **`bill` (`s_items`) — 0/62 TC** · **`conversion` — 0/62 TC** · **`site_script` — 0/62 TC**.
  - **Richmenu**: được đếm và mở màn admin, nhưng **không TC nào bấm thật trên LINE app** — vi phạm **RULE-06** với đúng nhóm dữ liệu user-facing nhất. TC gần nhất là TC-NOVP-03 và nó đang `skip` + không có mã quan điểm.
  → **Bổ sung TC-DATABACKUP001-03/04/05** (§5). *Không đặt BLOCKER vì đã có TC-TOOLNEGCTRL001-04 (`pass`) chốt được mức "không nhóm nào mất bản ghi"; đây là thiếu **chiều sâu và độ phủ**, không phải GAP trắng.*
- **[MAJOR] GAP-10 — `DATA-REF-001`: ghost reference chỉ cover richmenu/button/imagemap, và TC đó chưa chạy.** TC-NOVP-03 (do người viết) là TC ghost-reference mạnh nhất trong bộ nhưng đang `skip` và **không có mã quan điểm**. Chưa cover các đường tham chiếu khác tới event: **scenario step · auto reply · form action · tin nhắn đã lên lịch · conversion**. → Chạy TC-NOVP-03, gán mã `DATA-REF-001`, và bổ sung TC-DATAREF001-04 (§5).
- **[MAJOR] RULE-06 — TC-DATAREF001-02 dừng ở tầng job, không đi tới LINE app thật.** Expected ghi *"lượt chạy nhắc lịch sau đó… không gửi tin nhắn nhắc cho sự kiện đã bị xóa"* nhưng bước kiểm chỉ ở log/DB. Remind là output ra **LINE app** → phải verify trên thiết bị thật. Tương tự TC-OBS001-01 (notify chatwork) cần bằng chứng tin thật trong kênh.
- **[MAJOR] GAP-11 — `DATA-COUNT-001` (Cao): số đếm event chỉ đối chiếu 2/4 nguồn.** Quan điểm yêu cầu khớp **4 nguồn** (màn tóm tắt / màn chi tiết / CSV export / API). Bộ TC đối chiếu màn hình + DB, **không có CSV/API**. Ngoài ra TC-OUTTRUTH001-01 ghi *"tính cả các thư mục con nếu có"* — cách đếm event nằm trong thư mục con so với cách job đếm chưa được chốt. → Bổ sung TC-DATACOUNT001-01 (§5).
- **[MAJOR] GAP-12 — `PERF-LARGE-001`: chưa test ở quy mô khách hàng lớn nhất thực tế.** TC-JOB002-02 giả định 30 lần gọi endpoint tuần tự. Nếu bot nguồn thật có vài trăm event bản mới, số lần gọi tăng tuyến tính → nguy cơ timeout job / rate limit / nghẽn luồng. Quan điểm yêu cầu *"hỏi/tra số liệu khách hàng lớn nhất hiện tại"*. → Bổ sung TC-PERFLARGE001-01 (§5).
- **[MAJOR] 20/62 TC dùng mã quan điểm KHÔNG có trong `framework/checklist-lme.md` → coverage không map được.** `JOB-002` (6) · `TOOL-NEGCTRL-001` (5) · `TOOL-ERRHYG-001` (2) · `API-001` · `DATA-HIST-001` · `DATA-RETENTION-001` · `OBS-001` · `SEC-INJECT-001` · `TOOL-BRANCH-001` · `TOOL-OLDREC-001` (mỗi mã 1). Cộng 3 TC không có mã → **23/62 TC** nằm ngoài ma trận quan điểm chuẩn. Nội dung TC tốt, vấn đề là **truy vết**. → Map lại về mã tầng 1 (gợi ý: `JOB-002`→`JOB-001`, `TOOL-ERRHYG-001`→`FUNC-003`, `API-001`→`FUNC-001`, `SEC-INJECT-001`→`SEC-001`, `DATA-HIST-001`→`DATA-AUDIT-001`, `OBS-001`→`JOB-001`), hoặc theo **RULE-10** bổ sung chính thức các mã mới vào checklist tầng 1 kèm ID + ngày + nguồn bug.
- **[MAJOR] `Trạng thái đánh giá spec` trống 62/62.** Không TC nào ghi `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader` — trong khi **nhiều TC tự nhận là chưa chốt spec**: TC-COMPATLEGACY001-01 (*"CẦN NGƯỜI XÁC NHẬN kết quả đúng"*), TC-OUTTRUTH001-03, TC-FUNCDATE001-01 (*"hai giá trị là vùng cần đối chiếu kỹ"*), TC-PERM002-01. Đây đúng là nguy cơ tự suy diễn rồi cho Đạt. → Điền cột này; các TC trên phải là `Spec không ghi` + ghi rõ **đã hỏi ai**.
- **[MAJOR] Input thiếu — 2 nguồn spec chưa được đọc và không có TC nào tham chiếu.** (1) Ảnh `Screenshot 2026-07-28 201451.png` **dòng 22**, được description chỉ đích danh là nơi chứa mô tả chi tiết; (2) mốc *"staff bot free trước 11-11-2024 bot free được add 1 staff"* trong description, không xuất hiện ở bất kỳ đâu trong `03-dev-impact.md` lẫn 62 TC. → Leader mở ảnh, xác nhận dòng 22 có ràng buộc nào chưa được cover không.
- **[MAJOR] 3 TC do người viết thiếu toàn bộ metadata phân loại.** TC-NOVP-01/02/03 không có `viewpoint`, `case_type`, `tc_group` → không vào được ma trận quan điểm, không tính được RULE-01. Đáng tiếc vì nội dung 3 TC này thuộc nhóm sắc nhất bộ (plan nguồn ≠ đích; plan đổi giữa chừng; ghost reference richmenu). → Gán mã: TC-NOVP-01 → `PERM-003`/`FUNC-001` (Normal), TC-NOVP-02 → `PAY-PLAN-001` (Abnormal), TC-NOVP-03 → `DATA-REF-001` (Abnormal).

### 4.3 Minor (có thể fix sau)

- **[MINOR] RULE-02 — không TC nào ghi *loại* evidence bắt buộc ở `Ghi chú`.** Mỗi quan điểm ở tầng 1 quy định loại bằng chứng riêng (VD `DATA-DB-001` = ảnh query trước/sau kèm câu query trên 2 tài khoản; `JOB-001` = log job thấy retry + backoff). Cần ghi vào `Ghi chú` để QA biết phải chụp gì.
- **[MINOR] `RULE-04` và `RULE-09` bị dùng làm mã quan điểm** (TC-RULE04-01, TC-RULE09-01/02). Theo [checklist-lme §0.2](../../framework/checklist-lme.md), RULE là **quy định quy trình**, không phải quan điểm — không map vào ma trận coverage được. → Đổi: TC-RULE04-01 → `DATA-MIG-001` hoặc quan điểm phù hợp + ghi "phục vụ RULE-04" ở `Ghi chú`; TC-RULE09-01/02 → `COMPAT-LEGACY-001`.
- **[MINOR] `spec_status` / `priority` / `catalog` = `null` toàn bộ 62 TC.** Riêng `catalog = null` nghĩa là **không TC nào ghi nhận đã mở tầng 2** — vi phạm nguyên tắc 2 tầng (*"tick ◯ ở tầng 1 → bắt buộc mở catalog tầng 2"*).
- **[MINOR] TC-FUNC004-05 không atomic** — 1 TC chạy **4 tổ hợp** bảng chân trị (ngày tạo × cờ hợp đồng). Nếu 1 tổ hợp sai, kết quả TC là "Không đạt" nhưng không biết tổ hợp nào. Tương tự TC-FUNCDATE001-01 (4 giá trị biên) và TC-JOB002-06 (3 bộ). → Tách thành TC con.
- **[MINOR] Cột `Evidence thực tế` trống 62/62** do `testcase_list` không trả về trường này. Khi Leader cần đối chiếu bằng chứng, phải mở Studio trực tiếp — ghi chú giới hạn này vào quy trình.

### 4.4 Nit (gợi ý)

- **[NIT]** TC-TOOLBRANCH001-01 và TC-DEPLOYLIVE001-02 là **cổng chuẩn bị môi trường**, không phải TC sản phẩm. Tách sang mục "Điều kiện tiền đề của bộ TC" để tỉ lệ Normal/Abnormal/Boundary phản ánh đúng bộ TC thật.
- **[NIT]** Tỉ lệ loại case hiện tại **Normal 24 / Abnormal 25 / Boundary 10 / không gán 3** ≈ 39/40/16 — Abnormal cao hơn gợi ý 40/35/25 là **hợp lý** với task xóa dữ liệu, nhưng Boundary 16% hơi mỏng cho một task mà bản chất là **ngưỡng số lượng**. Tăng Boundary khi bổ sung TC ở §5.
- **[NIT]** Theo **RULE-11**, các quan điểm ở §4 checklist-lme (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) **không** được dùng để flag BLOCKER/MAJOR và **không** có mục nào khớp task này — ghi lại để Leader biết đã rà.
- **[NIT]** `TC-OUTTRUTH001-03` và `TC-OUTTRUTH001-04` mô tả **hành vi đã biết là gây khó chịu** (báo hoàn tất trước khi cắt xong; user thấy số vượt limit trong giây lát) và tự kết luận *"đúng thiết kế"*. Đây là điểm nên đưa lên PM quyết định UX, không nên để TC tự chốt.

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` ở round tiếp theo. **16 cột canonical**, `TC No.` không trùng TC đã có.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-CONC001-02 | CONC-001 | Normal | `checkLimitBEventDetail` chạy đơn luồng — số lần gọi `api/clear_b_event_detail` đúng bằng số bản ghi thừa, không thừa không thiếu | - Bot đích gói standard mới (`flag_contract_new = 1`), đang có 3 event bản mới có sẵn<br>- Bot nguồn có 12 event bản mới<br>- Bật log DEBUG cho `BackupBotTask`, chuẩn bị đếm request tới `api/clear_b_event_detail` | 1. Ghi lại danh sách id 3 event có sẵn của bot đích<br>2. Bật capture request tới `api/clear_b_event_detail` (proxy hoặc access log web)<br>3. Chạy 1 lần backup từ bot nguồn sang bot đích, chờ `STATUS_COMPLETED_BACKUP`<br>4. Đếm số request `clear_b_event_detail` đã bắt được và liệt kê `event_detail_id` của từng request<br>5. Query `SELECT id FROM b_event_detail WHERE bot_id=<bot đích> AND type_event_new=1 ORDER BY id` | 3 + 12 = 15 event; limit standard = 10; kỳ vọng xóa 5 | Đúng **5** request `clear_b_event_detail`, không có request lặp cùng `event_detail_id`. Bot đích còn đúng 10 bản ghi. 5 id bị xóa đều là id lớn nhất và đều thuộc 12 bản ghi vừa clone. 3 event có sẵn còn nguyên | Chưa test | | STAGING | | | | Spec ghi rõ (REQ-001, REQ-003) | Bổ sung theo review — baseline đơn luồng cho **GAP-1**, cover F1+F2+D2. Evidence bắt buộc: access log/proxy capture liệt kê từng request + kết quả query trước/sau |
| TC-CONC001-03 | CONC-001 | Abnormal | Hai job backup chạy **đồng thời** vào cùng 1 bot đích — không được xóa vượt quá số bản ghi thừa | - Bot đích gói standard mới, có 3 event bản mới có sẵn<br>- Hai bot nguồn A và B, mỗi bot 6 event bản mới<br>- Có khả năng enqueue 2 yêu cầu backup gần như cùng lúc (≤ 1s) vào cùng bot đích | 1. Ghi lại id + tên của 3 event có sẵn của bot đích<br>2. Enqueue backup A→đích và B→đích cách nhau dưới 1 giây<br>3. Chờ **cả hai** lần copy chuyển `STATUS_COMPLETED_BACKUP`<br>4. Đếm số event bản mới còn lại của bot đích<br>5. Đếm tổng số request `clear_b_event_detail` và kiểm có `event_detail_id` nào bị gửi 2 lần không<br>6. Đối chiếu 3 event có sẵn còn đủ không<br>7. Đọc log 2 luồng, ghi lại thời điểm mỗi luồng đếm và thời điểm mỗi luồng xóa | 3 + 6 + 6 = 15 event; limit = 10 | Bot đích còn **đúng 10** event bản mới — **không được ít hơn 10**. 3 event có sẵn còn nguyên. Không `event_detail_id` nào bị gửi xóa 2 lần. Nếu hệ thống không khóa, kết quả sẽ ra < 10 → **Không đạt**, raise ticket | Chưa test | | STAGING | | | | Spec không ghi — **đã hỏi Dev (câu 1 §3.5 report)** | Bổ sung theo review — **GAP-1 / BLOCKER-1**, `CONC-001` kịch bản #4 "batch đa luồng chạm limit chung". Evidence bắt buộc: log 2 luồng có timestamp đếm/xóa + query DB trước/sau |
| TC-CONC001-04 | CONC-001 | Boundary | Tạo event mới trên màn 「イベント予約」 **trong lúc** job đang ở giữa bước đếm và bước xóa | - Bot đích gói standard mới, đang có 9 event bản mới<br>- Bot nguồn có 2 event bản mới<br>- Có cách làm chậm bước xóa (delay endpoint ~30s) để mở cửa sổ thao tác | 1. Đặt endpoint `clear_b_event_detail` trả chậm ~30 giây<br>2. Chạy backup từ bot nguồn sang bot đích<br>3. Ngay khi log báo job đã đếm xong và bắt đầu gọi xóa, mở màn 「イベント予約」 của bot đích trên trình duyệt và tạo 1 event mới<br>4. Chờ job kết thúc<br>5. Đếm số event bản mới của bot đích và liệt kê id<br>6. F5 màn danh sách, đếm lại | 9 + 2 = 11 → xóa 1; user chèn thêm 1 event trong cửa sổ xóa | Kết quả cuối **không được vượt 10**. Event do user tạo tay hoặc bị chặn ngay lúc tạo (đã đủ 10), hoặc được tính vào lần đếm kế tiếp — nhưng tuyệt đối không để bot đích dừng ở 11. Ghi lại hành vi thật để Dev quyết định | Chưa test | | STAGING | | | | Spec không ghi — cần hỏi leader | Bổ sung theo review — **GAP-1**, giao thoa `CONC-001` × `MAP-PLAN-04`. Evidence bắt buộc: video thao tác + log job + query DB |
| TC-ENV003-01 | ENV-003 | Normal | Chạy backup vượt giới hạn **trên PRODUCTION** — 3 job độc lập vẫn cắt đúng về 10 | - Đã deploy commit `0022f93d…` lên production<br>- Cặp bot test **thật** trên production (`step.lme.jp`), bot đích gói standard mới<br>- Có quyền đọc log của **cả 3 job** production (callback / broadcast / scenario)<br>- ⚠️ Dùng bot test riêng, tuyệt đối không chạy trên bot khách hàng thật | 1. Ghi lại số event bản mới của bot đích trước khi chạy<br>2. Chạy backup từ bot nguồn sang bot đích trên production<br>3. Theo dõi log của **cả 3 job** production trong suốt quá trình<br>4. Chờ lần copy hoàn tất<br>5. Đếm số event bản mới còn lại + mở màn 「イベント予約」 đối chiếu<br>6. Ghi lại job nào thực sự thực thi bước `checkLimitBEventDetail` | Bot đích standard mới: 4 event sẵn có; bot nguồn 9 event → tổng 13, limit 10 | Bot đích còn đúng 10 event. Log ghi rõ **job nào** chạy bước kiểm giới hạn. **Không** có tranh chấp giữa 3 job (không có 2 job cùng chạy bước này cho cùng 1 bot). Màn danh sách hiển thị đúng 10 | Chưa test | | **PRODUCTION** | | | | Spec ghi rõ (REQ-001) | Bổ sung theo review — **GAP-2 / BLOCKER-2**, RULE-08 + `ENV-003` + Catalog D `ENV-JOB`. Evidence bắt buộc: log của cả 3 job production + screenshot màn 「イベント予約」 trên `step.lme.jp` |
| TC-ENV003-02 | ENV-003 | Abnormal | Endpoint xóa lỗi **trên production** — thông báo tới kênh trực thật và lần copy vẫn kết thúc | - Như TC-ENV003-01<br>- Có cách làm endpoint `api/clear_b_event_detail` trả lỗi trên production (hoặc phối hợp Dev chặn tạm)<br>- Mở sẵn kênh chatwork nhận notify | 1. Ghi lại thời điểm bắt đầu<br>2. Làm endpoint xóa trả lỗi<br>3. Chạy backup vượt giới hạn trên production<br>4. Chờ lần copy kết thúc, đọc trạng thái bản ghi lần copy<br>5. Kiểm kênh chatwork có nhận thông báo lỗi không, đọc nội dung<br>6. Đếm số event bản mới của bot đích | Bot đích standard mới, tổng 13 event sau copy | Lần copy vẫn kết thúc ở trạng thái hoàn tất, **không treo**. Bot đích còn 13 event (chưa cắt được) và điều này được ghi log rõ ràng. **Kênh chatwork nhận được thông báo thật**, nội dung nêu được server, bước lỗi và định danh bot/bản ghi | Chưa test | | **PRODUCTION** | | | | Spec ghi rõ (REQ-007) | Bổ sung theo review — **GAP-2**, RULE-06 (output cuối = tin chatwork thật) + `ENV-003`. Evidence bắt buộc: screenshot tin trong kênh chatwork + log job production |
| TC-ENV003-03 | ENV-003 | Boundary | Production 2 server loadbalance — chạy bộ case cơ bản theo **từng router** | - Như TC-ENV003-01<br>- Biết cách xác định và ghi lại `router id` của từng server production | 1. Xác định router id đang phục vụ, ghi lại<br>2. Chạy 1 lần backup vượt giới hạn, ghi kết quả + router id<br>3. Chuyển sang router còn lại (theo cách team đang dùng)<br>4. Chạy lại đúng kịch bản đó trên router thứ 2<br>5. So sánh kết quả 2 lần: số event còn lại, số lần gọi endpoint, log | Cùng 1 kịch bản: bot đích standard mới, tổng 13 event, limit 10 | Cả 2 router cho **cùng kết quả**: bot đích còn đúng 10 event, cùng số lần gọi endpoint. Không router nào bỏ qua bước kiểm giới hạn | Chưa test | | **PRODUCTION** | | | | Spec không ghi — cần hỏi leader | Bổ sung theo review — **GAP-2**, Catalog D `ENV-LB`. Evidence bắt buộc: log kèm router id của cả 2 lần chạy |
| TC-DATABACKUP001-01 | DATA-BACKUP-001 | Normal | Đối chiếu **từng field** nguồn↔đích cho 10 event được giữ lại — ngày lần đầu vs ngày tiếp theo, path ảnh, khóa ngoại | - Bot nguồn có 12 event bản mới, mỗi event có đủ setting phụ: ≥ 2 ngày tổ chức, ≥ 3 khung giờ, gói khung giờ, trường thông tin người đặt, ảnh đại diện, ngày lặp lại<br>- Bot đích gói standard mới, trống | 1. Query toàn bộ field của 12 event bản mới + bảng con ở bot nguồn, xuất ra file đối chiếu<br>2. Chạy backup sang bot đích, chờ hoàn tất (12 → cắt còn 10)<br>3. Query cùng bộ field cho 10 event còn lại ở bot đích<br>4. So sánh **từng field** nguồn↔đích<br>5. Kiểm riêng: **ngày lần đầu vs ngày tiếp theo có bị trùng nhau không**<br>6. Kiểm riêng: path ảnh của event/khung giờ **có dấu `//` thừa không**<br>7. Kiểm riêng: mọi khóa ngoại của bảng con trỏ đúng id event ở bot đích, **không trỏ ngược về id bot nguồn** | 12 event nguồn, mỗi event ≥ 2 ngày tổ chức + ≥ 3 khung giờ + ảnh | Mọi field của 10 event giữ lại khớp bản gốc. **Ngày lần đầu ≠ ngày tiếp theo** (không bị set trùng). **Không** path ảnh nào chứa `//`. Mọi khóa ngoại bảng con trỏ tới id event của **bot đích**, không còn tham chiếu tới id bot nguồn | Chưa test | | STAGING | | | | Spec ghi rõ (REQ-005) | Bổ sung theo review — **GAP-9 / MAJOR**, `DATA-BACKUP-001` điểm (3). Evidence bắt buộc: dán bảng đối chiếu query nguồn↔đích |
| TC-DATABACKUP001-02 | DATA-BACKUP-001 | Abnormal | Cấu hình `backup_config` bảng `image_map_items` cột `booking_event_id` — xác minh phạm vi bản ghi được clone đúng như giả định của fix | - Bot nguồn có ≥ 1 image map và ≥ 1 richmenu có button setting mở event booking<br>- Đọc được nội dung `backup_config` hiện hành trên môi trường test | 1. Dump nội dung `backup_config` và trích mapping của `image_map_items`, ghi lại giá trị `booking_event_id`<br>2. Đối chiếu với cảnh báo ở journal #130730 Redmine #39404: mapping đang là `"booking_event_id":"b_event_detail"`<br>3. Chạy backup từ bot nguồn sang bot đích<br>4. Query các bản ghi `image_map_items` ở bot đích, kiểm cột `booking_event_id` trỏ tới id nào<br>5. Kiểm id đó có tồn tại trong `b_event_detail` của **bot đích** không (hay còn trỏ về id bot nguồn)<br>6. Chạy tiếp kịch bản vượt giới hạn để job xóa event, rồi kiểm lại `image_map_items` | Bot nguồn: ≥ 1 image map trỏ event; bot đích standard mới vượt giới hạn sau copy | `image_map_items.booking_event_id` ở bot đích trỏ đúng id event **của bot đích**. Sau khi job xóa event thừa, không còn `image_map_items` nào trỏ tới event đã bị xóa. Nếu mapping config sai như journal cảnh báo → ghi nhận **Không đạt** và raise ticket riêng | Chưa test | | STAGING | | | | Spec không ghi — **đã hỏi Dev (câu 4 §3.5 report)** | Bổ sung theo review — **GAP-3 / BLOCKER-3**, journal #130730. Chạy kèm TC-NOVP-03. Evidence bắt buộc: dump `backup_config` + query `image_map_items` trước/sau |
| TC-DATABACKUP001-03 | DATA-BACKUP-001 | Normal | Richmenu được backup phải **hoạt động thật trên LINE app** của bot đích, không chỉ hiển thị đủ trên màn admin | - Bot nguồn có ≥ 2 richmenu (1 đang bật làm mặc định, 1 tắt), mỗi richmenu ≥ 3 vùng bấm với action khác loại: mở URL, gửi text, mở event booking<br>- Bot đích gói standard mới, trống<br>- Có tài khoản LINE **thật** đã kết bạn với OA của bot đích, test được trên **cả iOS và Android** | 1. Ghi lại số richmenu của bot nguồn, ảnh nền và từng vùng bấm kèm loại action<br>2. Chạy backup theo kịch bản vượt giới hạn để job có xóa event thừa, chờ hoàn tất<br>3. Đếm richmenu ở bot đích, mở màn richmenu đối chiếu ảnh nền và **từng vùng bấm + action** với bước 1<br>4. Xác nhận richmenu mặc định của bot đích đang được áp cho friend<br>5. Từ **LINE app thật trên iOS**, mở chat với OA bot đích, quan sát richmenu hiển thị<br>6. Bấm lần lượt từng vùng: vùng mở URL, vùng gửi text, vùng mở event booking<br>7. Lặp lại toàn bộ bước 5-6 trên **Android** | Bot nguồn: 2 richmenu × 3 vùng bấm (URL + text + event booking). Bot đích standard mới, tổng event sau copy = 13 (vượt 10) | Số richmenu, ảnh nền và toàn bộ vùng bấm ở bot đích khớp bot nguồn. Trên **LINE app thật cả iOS lẫn Android**: richmenu hiển thị đúng ảnh, bấm vùng mở URL ra đúng URL, vùng gửi text gửi đúng nội dung, vùng mở event booking mở đúng event **còn tồn tại**. Vùng nào trỏ tới event đã bị job xóa thì hành vi phải khớp TC-DATAREF001-04 — không trắng màn, không exception | Chưa test | | STAGING | | | | Spec ghi rõ (phạm vi backup) | Bổ sung theo review — **GAP-13**, regression nhóm **richmenu**. TC-TOOLNEGCTRL001-04 mới đếm bản ghi + mở màn admin, chưa tới output cuối (**RULE-06**). Evidence bắt buộc: screenshot LINE app iOS + Android khi bấm từng vùng, kèm screenshot màn richmenu admin |
| TC-DATABACKUP001-04 | DATA-BACKUP-001 | Normal | Biểu mẫu và **câu trả lời biểu mẫu** (`form_answer`) được backup đủ, và submit mới ở bot đích vẫn ghi nhận đúng | - Bot nguồn có ≥ 2 form, mỗi form đã có ≥ 5 câu trả lời submit từ trước, trong đó ≥ 1 form có action chạy sau submit<br>- Bot đích gói standard mới, trống<br>- Có tài khoản LINE thật đã kết bạn với OA của bot đích | 1. Ghi lại số form và **số câu trả lời của từng form** ở bot nguồn, kèm nội dung từng cột của 2 câu trả lời mẫu<br>2. Chạy backup theo kịch bản vượt giới hạn, chờ hoàn tất<br>3. Đếm số form ở bot đích và **đếm số câu trả lời của từng form**, đối chiếu bước 1<br>4. Mở màn danh sách câu trả lời của từng form ở bot đích, đối chiếu nội dung **từng cột** với 2 câu trả lời mẫu<br>5. Từ **LINE app thật**, mở link form của bot đích và submit 1 câu trả lời mới<br>6. Kiểm câu trả lời mới xuất hiện ở màn danh sách đáp án và action sau submit có chạy đúng không | Bot nguồn: 2 form × 5 câu trả lời. Bot đích standard mới, tổng event sau copy = 13 (vượt 10) | Số form và **số câu trả lời từng form** ở bot đích khớp đúng bot nguồn, nội dung từng cột khớp. Submit mới từ LINE app được ghi nhận đúng và action sau submit chạy. Việc job xóa event thừa **không làm mất hay lệch bản ghi `form_answer` nào** | Chưa test | | STAGING | | | | Spec ghi rõ (phạm vi backup) | Bổ sung theo review — **GAP-13**. `form_answer_id` nằm trong mapping `backup_config` (journal #130730) nhưng **0/62 TC** nhắc tới câu trả lời form. **RULE-06**. Evidence bắt buộc: bảng đối chiếu số câu trả lời nguồn↔đích + screenshot submit từ LINE app thật |
| TC-DATABACKUP001-05 | DATA-BACKUP-001 | Normal | Rà đủ **toàn bộ** nhóm dữ liệu khai báo trong `backup_config` — action, bill, conversion, site script không bị thiếu hay hỏng | - Dump được nội dung `backup_config` hiện hành trên môi trường test<br>- Bot nguồn có dữ liệu ở **mọi** nhóm khai báo trong config, tối thiểu: action (`t_actions`), item/bill (`s_items`), conversion, site script, template, form answer, event booking<br>- Bot đích gói standard mới, trống | 1. Dump `backup_config`, liệt kê **đầy đủ** danh sách nhóm được khai báo kèm bảng đích của từng nhóm<br>2. Với **từng** nhóm trong danh sách, đếm số bản ghi ở bot nguồn<br>3. Chạy backup theo kịch bản vượt giới hạn để job có xóa event thừa, chờ hoàn tất<br>4. Với **từng** nhóm, đếm lại ở bot đích và lập bảng đối chiếu nguồn↔đích<br>5. Mở màn hình tương ứng của mỗi nhóm ở bot đích, xác nhận mở được và nội dung đúng<br>6. Đánh dấu nhóm nào chưa được TC nào trong bộ 62 TC hiện có cover | Mapping `backup_config` theo journal #130730: `template_id→template`, `action_id→t_actions`, `form_answer_id→form_answer`, `bill_id→s_items`, `booking_event_id→b_event_detail`, `site_script_id→site_script`, `conversion_id→conversion` | Bảng đối chiếu phủ **100% nhóm** khai báo trong `backup_config`; mỗi nhóm có số bản ghi đích = nguồn và màn hình mở được bình thường. Không nhóm nào bị bỏ sót khỏi phạm vi kiểm. Nhóm nào lệch số hoặc lỗi màn → ghi **Không đạt** kèm tên nhóm và raise ticket | Chưa test | | STAGING | | | | Spec ghi rõ (phạm vi backup) | Bổ sung theo review — **GAP-13**. TC-TOOLNEGCTRL001-04 chỉ rà 8 nhóm; **action / bill / conversion / site_script = 0 TC**. Chạy kèm TC-DATABACKUP001-02 (cùng nguồn journal #130730). Evidence bắt buộc: dump `backup_config` + bảng đối chiếu đủ nhóm |
| TC-STATE001-01 | STATE-001 | Abnormal | Job bị dừng đột ngột **giữa** lúc set trạng thái hoàn tất và lúc chạy bước kiểm giới hạn | - Bot đích gói standard mới, bot nguồn đủ để tổng vượt giới hạn<br>- Có quyền kill tiến trình job hoặc restart service job<br>- Bật log đủ chi tiết để biết thời điểm `STATUS_COMPLETED_BACKUP` được set | 1. Chạy backup từ bot nguồn sang bot đích<br>2. Theo dõi log tới khi thấy `backupHistory` được set `STATUS_COMPLETED_BACKUP`<br>3. **Kill job ngay lập tức**, trước khi log xuất hiện dòng của `checkLimitBEventDetail`<br>4. Khởi động lại job<br>5. Đọc trạng thái bản ghi lần copy<br>6. Đếm số event bản mới của bot đích<br>7. Chờ thêm 1 chu kỳ job và đếm lại — xem có cơ chế nào tự phát hiện và chạy lại bước thiếu không<br>8. Lặp lại kịch bản bằng cách restart service thay vì kill | Bot đích 3 event sẵn có + bot nguồn 12 → tổng 15, limit 10 | Ghi lại hành vi thật. Rủi ro cần khẳng định: nếu bot đích **kẹt vĩnh viễn ở 15 event** mà lần copy vẫn báo hoàn tất và **không có cơ chế chạy lại** → đây là dữ liệu nửa vời, **Không đạt**, raise ticket. Nếu có cơ chế tự phát hiện thì phải cắt được về 10 ở chu kỳ sau | Chưa test | | STAGING | | | | Spec không ghi — cần hỏi leader | Bổ sung theo review — **GAP-7 / MAJOR**, `STATE-001` (≥2 bước ghi tuần tự, ngắt giữa chừng). Evidence bắt buộc: log có timestamp điểm kill + query DB sau restart + sau 1 chu kỳ |
| TC-DATAAUDIT001-01 | DATA-AUDIT-001 | Normal | Job xóa event thừa — lịch sử thao tác ghi đúng 1 bản ghi với đủ 4 thông tin | - Xác nhận trước với Leader/Dev: event booking có màn `操作履歴` / lịch sử thao tác không. Nếu không có → đánh dấu `N/A` kèm lý do<br>- Bot đích gói standard mới, sẽ bị cắt 3 event sau backup | 1. Ghi lại số dòng lịch sử thao tác hiện có của bot đích<br>2. Chạy backup khiến job xóa 3 event thừa<br>3. Mở màn lịch sử thao tác của bot đích<br>4. Đếm số dòng mới phát sinh<br>5. Với mỗi dòng, đọc đủ 4 thông tin: người thực hiện / thời gian / hành động / giá trị cũ→mới<br>6. Đối chiếu loại thao tác ghi nhận có đúng là "xóa" không (không được ghi thành "thêm mới") | Bot đích: 13 event sau copy, limit 10 → xóa 3 | Phát sinh đúng **3 dòng** lịch sử (hoặc 1 dòng tổng hợp nêu rõ 3 id — theo spec). Mỗi dòng đủ 4 thông tin, người thực hiện ghi nhận rõ là **hệ thống/job** chứ không để trống hay gán nhầm cho admin. Loại thao tác ghi đúng là **xóa** | Chưa test | | STAGING | | | | Spec không ghi — cần hỏi leader | Bổ sung theo review — **GAP-8 / MAJOR**, `DATA-AUDIT-001`. Evidence bắt buộc: screenshot/export bản ghi lịch sử sau thao tác |
| TC-DATAREF001-04 | DATA-REF-001 | Abnormal | Ghost reference mở rộng — scenario, auto reply, form action, tin đã lên lịch trỏ tới event bị job xóa | - Bot nguồn có event E được tham chiếu ở **cả 4 nơi**: 1 bước scenario có action mở E · 1 auto reply trả template chứa link E · 1 form có action sau submit mở E · 1 tin đã lên lịch chứa button mở E<br>- Bot đích gói standard mới, sau copy sẽ vượt giới hạn và E nằm trong nhóm bị xóa | 1. Ghi lại id của E ở bot nguồn và 4 nơi tham chiếu<br>2. Chạy backup sang bot đích, chờ hoàn tất và xác nhận bản sao của E đã bị job xóa<br>3. Mở màn scenario của bot đích → mở bước có action, quan sát hiển thị<br>4. Mở màn auto reply → mở template liên quan<br>5. Mở màn form → mở phần action sau submit<br>6. Mở màn tin đã lên lịch → mở tin chứa button<br>7. Từ LINE app thật, kích hoạt scenario và auto reply, bấm button trong tin<br>8. Chờ tin đã lên lịch tới giờ gửi và quan sát trên LINE app | 1 event E được tham chiếu ở 4 nơi; bot đích bị cắt và E bị xóa | Cả 4 màn admin **mở được bình thường, không trắng màn, không exception**, và hiển thị trạng thái tham chiếu đã mất một cách rõ ràng. Trên **LINE app thật**: bấm vào các điểm vào đó không dẫn tới màn lỗi trắng — hoặc chặn có thông báo, hoặc theo spec Dev chốt. Tin đã lên lịch gửi được, không làm hỏng cả lượt gửi | Chưa test | | STAGING | | | | Spec không ghi — cần hỏi leader | Bổ sung theo review — **GAP-10 / MAJOR**, `DATA-REF-001` + RULE-06. Mở rộng TC-NOVP-03 (mới chỉ richmenu/button/imagemap). Evidence bắt buộc: screenshot 4 màn admin + screenshot LINE app thật |
| TC-DATACOUNT001-01 | DATA-COUNT-001 | Normal | Số event sau khi cắt phải khớp giữa **4 nguồn** — màn danh sách, chi tiết/DB, CSV export và API | - Bot đích gói standard mới, sau backup còn đúng 10 event bản mới<br>- Bot đích có thêm event nằm trong **thư mục con** để kiểm cách đếm<br>- Có quyền export CSV và gọi API danh sách event | 1. Mở màn 「イベント予約」, đếm số event hiển thị (ghi rõ có tính event trong thư mục con không)<br>2. Query `SELECT COUNT(*) FROM b_event_detail WHERE bot_id=<đích> AND type_event_new=1`<br>3. Export CSV danh sách event, đếm số dòng dữ liệu<br>4. Gọi API danh sách event của bot đích, đếm số phần tử<br>5. Lập bảng đối chiếu 4 con số<br>6. Bấm vào con số đếm trên màn (nếu có) và xác nhận mở đúng danh sách tương ứng | 10 event active, trong đó 3 nằm trong 1 thư mục con; 2 event loại cũ (không tính) | **Cả 4 nguồn cùng ra 10.** Event loại cũ không bị tính vào. Cách đếm event trong thư mục con thống nhất giữa màn hình và job — nếu lệch thì ghi rõ và raise ticket vì job dùng phép đếm này để quyết định xóa | Chưa test | | STAGING | | | | Spec không ghi — cần hỏi leader | Bổ sung theo review — **GAP-11 / MAJOR**, `DATA-COUNT-001` (đối chiếu 4 nguồn + phép tính tay). Evidence bắt buộc: bảng đối chiếu 4 nguồn + file CSV + response API |
| TC-PERFLARGE001-01 | PERF-LARGE-001 | Boundary | Bot nguồn ở quy mô khách hàng lớn nhất thực tế — job không timeout, không mất bản ghi | - **Trước khi viết data**: tra số event bản mới lớn nhất của khách hàng thật hiện tại, ghi vào ô Dữ liệu test<br>- Bot nguồn dựng bằng hoặc lớn hơn con số đó<br>- Bot đích gói standard mới, trống<br>- Có quyền đọc log job và đếm request tới endpoint | 1. Ghi lại số event bản mới của bot nguồn và nguồn của con số quy mô<br>2. Bắt đầu đo thời gian, chạy backup sang bot đích<br>3. Theo dõi log job liên tục, ghi lại thời điểm bắt đầu và kết thúc bước kiểm giới hạn<br>4. Đếm tổng số request `clear_b_event_detail` gửi đi và số request trả lỗi<br>5. Đếm số event bản mới còn lại của bot đích<br>6. Kiểm tra: số bản ghi cần xóa = số xóa thành công + số ghi nhận lỗi<br>7. Kiểm job có bị timeout, có nghẽn luồng khiến job khác chờ không | `<điền số thật>` event bản mới ở bot nguồn (nguồn: khách hàng lớn nhất hiện tại); limit đích = 10 | Job **hoàn tất, không timeout, không treo**. Bot đích còn đúng 10 event. **Số bản ghi cần xóa = số xóa thành công + số vào hàng đợi lỗi** — không bản ghi nào biến mất khỏi thống kê. Ghi lại thời gian chạy bước kiểm giới hạn để đối chiếu ngưỡng chấp nhận được | Chưa test | | STAGING | | | | Spec không ghi — cần hỏi leader | Bổ sung theo review — **GAP-12 / MAJOR**, `PERF-LARGE-001` + `JOB-001` điểm (4) + Catalog D2 `JOB-02`. Evidence bắt buộc: số liệu quy mô kèm nguồn + thời gian chạy + bảng đối chiếu số bản ghi vào/ra |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — 4 điểm:

1. **Hằng số `_token` của `api/clear_b_event_detail`**
   - Section: `03-dev-impact.md` §5 + description Redmine #39404
   - Nội dung: description ghi `ConfigFile.API_CERT_KEY`, báo cáo đánh giá ghi `ConfigFile.API_SERVER_CERT` (giá trị của `KEY_CERTIFICATION_API`). Phải chốt **một** giá trị và sửa nơi còn lại.
   - Người chịu trách nhiệm: Dev (Văn Dũng Đinh / người implement)

2. **Phạm vi journal #130730 — `backup_config` / `image_map_items.booking_event_id`**
   - Section: `03-dev-impact.md` mục 4.1 / 4.2
   - Nội dung: xác định cảnh báo này thuộc ticket #39404 hay tách ticket riêng. Nếu thuộc → bổ sung vào 4.1/4.2/4.3 rồi review lại coverage.
   - Người chịu trách nhiệm: Dev + Leader

3. **Hành vi hiện tại: báo hoàn tất TRƯỚC khi cắt xong**
   - Section: spec màn 「データコピー」 + REQ-008
   - Nội dung: TC-OUTTRUTH001-03 và TC-OUTTRUTH001-04 ghi nhận màn hiện 「データコピーが完了しました」 trong khi bước cắt chưa chạy xong (hoặc đã lỗi) → user thấy số vượt giới hạn trong giây lát, và khi bước cắt lỗi thì user **không hề biết**. Cần PM chốt đây là hành vi chấp nhận được hay phải đổi.
   - Người chịu trách nhiệm: PM + Dev

4. **Lệch điều kiện tính plan giữa job và web**
   - Section: REQ-009
   - Nội dung: TC-REGSHARED001-03 nêu màn danh sách sự kiện **không xét** `users.created_at` còn job **có xét** mốc 2021-07-01. Cần chốt: giữ lệch này (và ghi vào spec) hay đồng bộ lại một trong hai phía.
   - Người chịu trách nhiệm: Dev + Leader

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ✓ · A.2 ✓ · A.3 ✓ · A.4 ✓ · A.5 ✓ (không có orphan thật) · **A.6 ✗** (fix-shape: thiếu concurrency + luồng khôi phục — xem §3.5)
- [ ] **B. Chất lượng từng TC** — B.1 ✓ (title/precond/steps/expected rõ, đo lường được — điểm mạnh của bộ này) · **B.2 ✗** (TC-FUNC004-05, TC-FUNCDATE001-01, TC-JOB002-06 không atomic) · B.3 ✓ · B.4 ✓
- [ ] **C. Chất lượng bộ TC** — tỉ lệ loại case hợp lý ✓ · không trùng lặp ✓ · **phân bố quan điểm ✗** (23/62 TC dùng mã ngoài tầng 1; `DATA-AUDIT-001` / `STATE-001` trống, `DATA-BACKUP-001` chỉ gián tiếp) · phân quyền ✓ (PERM-001/002) · responsive — N/A · i18n — N/A
- [x] **D. Spec alignment** — không có `02-spec-reference.md`, dùng REQ-001…011 của Studio thay thế. 4 điểm cần update spec ở §6
- [ ] **E. Hành chính** — TC No. đúng format ✓ · file đúng folder ✓ · **`Tester viết TCs` / version ✗** (tác giả thật là AI, cần ghi rõ; `Trạng thái đánh giá spec` trống 62/62)
- [ ] **F. Base quan điểm test LME**
  - [ ] **F.1 Quan điểm (tầng 1)** — bảng dưới. 4 quan điểm Cao **GAP hoàn toàn**, 15 quan điểm Cao vi phạm RULE-01
  - [ ] **F.2 Catalog (tầng 2)** — **✗ toàn bộ 62 TC có `catalog = null`**. A input — N/A (không có form nhập) · B UI ✓ (một phần, qua UI-003) · **C ✗** (khối `MAP-PLAN` ✓ sau khi ghi nhận loại trừ của Leader; **khối phạm vi backup rà thiếu 4 nhóm** — GAP-13; khối `MAP-CANCEL` chưa rà) · **D/D2 ✗** (`ENV-JOB` production 3 job, `ENV-LB` 2 router chưa test; D2 `JOB-01` rate limit / `JOB-02` retry-backoff chưa cover) · E media — N/A
  - [ ] **F.3 RULE quy trình** — **RULE-01 ✗** (15/20 quan điểm Cao) · **RULE-02 ✗** (28 TC `Đạt` không evidence) · RULE-03 — N/A (không có bảng ◯/× của member) · RULE-05 — N/A (không tích hợp bên thứ 3) · **RULE-06 ✗** (TC-DATAREF001-02, TC-OBS001-01 dừng ở log) · **RULE-07 ✓** (`WHERE` scope 2 tài khoản có TC-TOOLNEGCTRL001-01; verify DB đầy đủ) · **RULE-08 ✗** (62/62 chạy `local`) · **RULE-09 ✓** (plan cũ/mới song song: TC-RULE09-01/02, TC-FUNC004-05; event loại cũ/mới: TC-TOOLNEGCTRL001-05) · **RULE-12 ✗** (thiếu danh sách vùng ảnh hưởng do Dev cung cấp — AP-6)

### F.1 — Bảng quan điểm đối chiếu

> Ưu tiên lấy từ [checklist-lme.md](../../framework/checklist-lme.md) §2. Cột "TC cover" dùng `TC No.` đã sinh ở file 04.

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ mọi chức năng | TC-FUNC001-01/02/03 (**3 Normal**) | **RISK** — RULE-01: thiếu Abnormal + Boundary |
| `FUNC-003` | TB→Cao | ◯ endpoint nhận `event_detail_id` / `bot_id` | TC-FUNC003-01 (Boundary) | **RISK** — thiếu Normal + Abnormal |
| `FUNC-004` | Cao | ◯ giới hạn số lượng theo gói | TC-FUNC004-01/02/03/04/05 (**5 Boundary**) | **RISK** — RULE-01: thiếu Normal + Abnormal |
| `FUNC-DATE-001` | Cao | ◯ mốc `2021-07-01` so sánh ngày | TC-FUNCDATE001-01 (Boundary) | **RISK** — thiếu Normal + Abnormal |
| `FUNC-SEQ-001` | Trung bình | ◯ chạy copy 2 lần liên tiếp | TC-FUNCSEQ001-01 (Normal) | **OK** |
| `CONC-001` | **Cao** | ◯ **batch đa luồng chạm giới hạn dùng chung** | TC-CONC001-01 (Abnormal — chỉ idempotency API) | **GAP → [BLOCKER-1]** — thiếu 3/4 kịch bản |
| `DATA-001` | Cao | ◯ số event phản ánh ở nhiều màn | TC-OUTTRUTH001-01/02, TC-UI003-01, TC-DATAHIST001-01 | **OK** |
| `DATA-COUNT-001` | Cao | ◯ màn có số đếm event | TC-OUTTRUTH001-01, TC-FUNC004-01 | **RISK → [GAP-11]** — chỉ 2/4 nguồn |
| `DATA-REF-001` | Cao | ◯ xóa đối tượng đang được tham chiếu | TC-DATAREF001-01/02/03, TC-NOVP-03 | **RISK → [GAP-10]** — thiếu Boundary; ghost chỉ 3 đường; TC-NOVP-03 chưa chạy |
| `DATA-MIG-001` | Cao | ◯ Dev khẳng định không đổi cấu trúc → cần negative control | TC-DATAMIG001-01/02 (2 Normal) | **RISK** — RULE-01: thiếu Abnormal + Boundary |
| `DATA-BACKUP-001` | **Cao** | ◯ **chạm backup / copy bot** — trigger khớp tuyệt đối | TC-TOOLNEGCTRL001-03/04, TC-NOVP-03 (gián tiếp) | **RISK → [GAP-9] + [GAP-13]** — thiếu đối chiếu từng field nguồn↔đích; regression nhóm khác chỉ ở mức đếm bản ghi, 4 nhóm trong `backup_config` không có TC |
| `DATA-DB-001` | Cao | ◯ có DELETE | TC-DATADB001-01, TC-TOOLNEGCTRL001-01 (`WHERE` scope 2 bot) | **RISK** — RULE-01: thiếu Abnormal + Boundary |
| `DATA-AUDIT-001` | **Cao** | ◯ xóa dữ liệu có lượt đặt của khách | — | **GAP → [GAP-8]** *(Leader xác nhận spec có audit log cho event booking không)* |
| `DATA-CACHE-001` | Trung bình | × không đổi JS/asset, không dùng short link | — | × — hợp lệ |
| `PERM-001` | Cao | ◯ màn copy phân biệt gói | TC-PERM001-01 (Abnormal) | **RISK** — thiếu Normal + Boundary |
| `PERM-002` | Cao | ◯ endpoint xóa = thao tác nhạy cảm | TC-PERM002-01 (Abnormal, `skip`) | **RISK** — thiếu Normal + Boundary; chưa chạy |
| `PERM-003` | Cao | ◯ nhiều bot, có change bot | TC-TOOLNEGCTRL001-01/02, TC-SECISO001-01, TC-NOVP-01 | **OK** |
| `OUT-TRUTH-001` | Cao | ◯ thao tác có thông báo kết quả | TC-OUTTRUTH001-01/02 (N), -03 (A), -04 (B) | **OK** ✅ đủ 3 loại case |
| `UI-003` | Trung bình | ◯ màn danh sách + xử lý bất đồng bộ | TC-UI003-01 (Normal) | **OK** |
| `PAY-LIMIT-001` | Cao | ◯ giới hạn theo gói, **nhưng phạm vi release này chỉ gồm job + API** | TC-FUNC004-01/02/03/04/05, TC-RULE09-01/02, TC-REGSHARED001-02 | **OK — có loại trừ được ghi nhận** (Leader 2026-08-24): `MAP-PLAN-01` ✓ · `MAP-PLAN-02` ✓ · `MAP-PLAN-06` ✓ · `MAP-PLAN-03` **N/A** (chưa có xóa mềm) · `MAP-PLAN-04/05` **ngoài phạm vi** (validate phía web, lần này không sửa web) — **RULE-03 đã có lý do** |
| `PAY-PLAN-001` | Cao | ◯ plan bot đích có thể đổi | TC-NOVP-02 (không gán mã) | **RISK** — có TC nhưng không truy vết được |
| `PAY-STATE-001` | Cao | × không có giao dịch tiền trong luồng fix | — | × — hợp lệ |
| `STATE-001` | **Cao** | ◯ **≥2 bước ghi tuần tự** (copy → kiểm giới hạn) | TC-JOB002-04/05 (chỉ endpoint lỗi) | **GAP → [GAP-7]** — thiếu job chết giữa 2 bước |
| `STATE-CLEAN-001` | Cao | × không chạm hủy hợp đồng / ngắt kết nối | — | × — hợp lệ |
| `STATE-DEP-001` | Cao | ◯ remind của khung giờ bị xóa | TC-DATAREF001-02 | **RISK** — RULE-06: chưa tới LINE app thật |
| `REG-SHARED-001` | Cao | ◯ logic tính plan dùng chung web↔job | TC-REGSHARED001-03 (N), ~~-01 (A)~~ **đã bị xóa**, -02 (B) | **RISK** — mất TC **Abnormal** (Studio #9365 xóa 2026-08-24, xem §9) → vi phạm RULE-01; vẫn thiếu **danh sách nơi ảnh hưởng do Dev cung cấp** (AP-6) |
| `REG-RUN-001` | Cao | ◯ job đang chạy dở khi release | TC-DEPLOYLIVE001-01 (một phần) | **RISK** — chưa có TC job copy chạy dở **từ trước** release |
| `SEC-001` | Cao | ◯ endpoint chạm dữ liệu bot khác | TC-SEC001-01/02 (2 Abnormal, `skip`) | **RISK** — thiếu Normal + Boundary; chưa chạy |
| `SEC-002` | Cao | ◯ `_token` = credential | TC-SEC002-01 (Abnormal, `skip`) | **RISK** — thiếu Normal + Boundary; chưa chạy |
| `SEC-ISO-001` | Cao | ◯ cách ly dữ liệu giữa bot | TC-SECISO001-01 (Abnormal, `skip`) | **RISK** — thiếu Normal + Boundary; chưa chạy |
| `PERF-LARGE-001` | TB→Cao | ◯ số lần gọi endpoint tỉ lệ với số event | TC-JOB002-02 (30 lần, giả định) | **RISK → [GAP-12]** — chưa dùng quy mô thật |
| `ENV-003` | **Cao** | ◯ **job nền + gói cước** — không được × vì "staging pass" | — *(62/62 TC chạy `local`)* | **GAP → [BLOCKER-2]** |
| `JOB-001` | Cao | ◯ sửa job nền, gọi API theo lô | TC-JOB001-01 (Abnormal, `blocked`) | **RISK** — thiếu Normal + Boundary; chưa cover retry/backoff (Catalog D2 `JOB-02`) |
| `LIST-001` | Trung bình | ◯ màn danh sách event có thư mục/phân trang | TC-UI003-01 (một phần) | **RISK** — chưa test 4 góc (search/filter/pagination/click số đếm) |
| `BULK-001` | Cao | × không có bộ lọc + thao tác hàng loạt do user chọn | — | × — hợp lệ *(job xóa theo id, không theo filter user)* |
| `DEPLOY-ASSET-001` | Cao | × không sửa JS/CSS/font/icon | — | × — hợp lệ |
| `DEPLOY-LIVE-001` | Cao | ◯ release không lock maintain, job + web deploy lệch nhau | TC-DEPLOYLIVE001-01 (A), -02 (N) | **RISK** — thiếu Boundary |
| `COMPAT-LEGACY-001` | Cao | ◯ event loại cũ ⇄ bản mới; plan cũ ⇄ mới | TC-COMPATLEGACY001-01 (A), TC-TOOLNEGCTRL001-05, TC-RULE09-01/02 | **RISK** — RULE-01: thiếu Normal + Boundary (nội dung thì đã cover tốt) |
| `MSG-*` / `LIFF-ENTRY-001` / `MEDIA-*` / `FRIEND-001` / `INTG-*` / `SYNC-APP-001` / `NOTI-MAIL-001` / `OUT-EXPORT-001` | — | × không nằm trong phạm vi fix | — | × — hợp lệ |

**Tổng kết F.1**: **3 quan điểm Cao GAP hoàn toàn** (`CONC-001`, `ENV-003`, `DATA-AUDIT-001`) · `DATA-BACKUP-001` **RISK** (regression nhóm khác chỉ ở mức đếm) · **16 quan điểm Cao vi phạm RULE-01** · **1 quan điểm Cao đạt đủ 3 loại case** (`OUT-TRUTH-001`).

> `PAY-LIMIT-001` ở draft đầu bị chấm GAP/BLOCKER, **đã gỡ sau phản hồi Leader (2026-08-24)** — xem dòng tương ứng ở bảng trên.

---

## 9. Nhật ký thay đổi trên Studio (sau review)

### 9.1 Đã push 3 TC đề xuất lên Studio task #57

Theo yêu cầu Leader, 3 TC ở §5 đã được tạo trên MCP LME TEST STUDIO ngày **2026-08-24 03:41:10 UTC**:

| TC No. (report) | Studio ID | temp_id | client_ref | Quan điểm | Loại case | Lấp GAP |
|---|---|---|---|---|---|---|
| TC-CONC001-03 | **#12228** | NEW-67 | `REVIEW05-39404-CONC001-03` | `CONC-001` | Abnormal | GAP-1 / BLOCKER-1 |
| TC-DATABACKUP001-01 | **#12229** | NEW-68 | `REVIEW05-39404-DATABACKUP001-01` | `DATA-BACKUP-001` | Normal | GAP-9 |
| TC-DATABACKUP001-03 | **#12230** | NEW-69 | `REVIEW05-39404-DATABACKUP001-03` | `DATA-BACKUP-001` | Normal | GAP-13 |

- Cả 3 ghi nhận `author = ngannt@mcp`, `provenance.source = human`, `status = draft`, `last_exec = null` (Chưa test).
- `env_scope`: TC-CONC001-03 và TC-DATABACKUP001-01 = `local/dev/staging`; TC-DATABACKUP001-03 = `dev/staging` (bắt buộc LINE app thật, không chạy được ở local).
- 13 TC còn lại ở §5 **chưa push** — chờ Leader duyệt.

### 9.2 ⚠️ Phát hiện: 1 TC biến mất khỏi Studio trong lúc review

**TC-REGSHARED001-01 — Studio #9365 (temp `NEW-55`)** — *"Bot có nhiều bản ghi hợp đồng hoặc nhiều slot — loại hợp đồng job đọc phải trùng với loại hợp đồng màn hình đọc"* (`REG-SHARED-001`, Abnormal, `job`, `last_exec = skip`) — **không còn tồn tại**. `testcase_get_history(9365)` trả về `Không có TC #9365`.

Mốc thời gian đối chiếu được:

| Thời điểm (UTC) | Sự kiện |
|---|---|
| 2026-08-24 02:36:51 | Fetch TC list lần 1 — **62 TC, #9365 còn** |
| 2026-08-24 02:56:54 | Job `enrich-tc` (job:528, by `ngannt`) — sửa **3 TC**: #11139 v10→11, #11140 v4→5, #11151 v12→13 |
| 2026-08-24 03:41:10 | `testcase_create` tạo #12228/12229/12230 (**chỉ tạo, không xóa**) |
| 2026-08-24 03:41:38 | Fetch TC list lần 2 — **64 TC, #9365 đã mất** |

**Chưa xác định được thủ phạm.** `task_get_history(57)` **không ghi nhận sự kiện xóa nào**. Nội dung của #9365 cũng **không được gộp** vào 2 TC `REG-SHARED-001` còn lại (#9213 và #9372 đều giữ nguyên `version = 1`, `updated_at` không đổi).

**Hệ quả**: `REG-SHARED-001` (ưu tiên **Cao**) mất TC **Abnormal** duy nhất → từ **OK** (đủ 3 loại case) rơi xuống **RISK**, vi phạm RULE-01. Số quan điểm Cao vi phạm RULE-01 tăng **15 → 16**; số quan điểm Cao đạt đủ 3 loại case giảm **2 → 1**.

**Đề nghị Leader**: kiểm tra trực tiếp trên Studio hoặc hỏi người chạy job `enrich-tc` (job:528) xem #9365 bị xóa có chủ đích không. Nếu là xóa nhầm → khôi phục; nếu cố ý → cần 1 TC `REG-SHARED-001` loại Abnormal thay thế, vì đây là quan điểm bắt được lệch điều kiện tính plan giữa web và job (REQ-009).

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!-- Draft sinh bởi /review-tc ngày 2026-08-24 từ 3 file input (01, 03, 04) + framework/checklist-lme.md + framework/catalog-lme.md.
     Không có 02-spec-reference.md → dùng LME-SYSTEM-SPEC tổng + 11 REQ của Studio task #57.
     Đây là DRAFT cho Leader verify, không phải kết luận cuối. -->

