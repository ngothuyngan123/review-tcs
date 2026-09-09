# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #39172 — [JOB] Job retry sync form answer lên Google Sheet treo RUNNING với bản ghi cũ chưa có ID retry |
| Reviewer (Leader) | `<Leader ký>` (draft do `/review-tc` sinh) |
| Tester được review | Thanh Phương / thanhntp (TC sinh bởi lme-test-studio task 39) |
| Ngày review | 2026-07-30 |
| Version TCs | lme-test-studio task 39 (49 TC) |
| Vòng review | Round 1 |

> **Spec reference**: không có `02-spec-reference.md` → dùng `templates/LME-SYSTEM-SPEC.md` tổng (Form / INTG-SHEET / Job nền). Nhiều expected của TC ghi rõ "spec không định nghĩa → nguồn ticket 39172 + code".
>
> **Nguồn file 04**: TC do **lme-test-studio** sinh (không phải Sheet human), đã tự review (`[review-bổ-sung]`). Đây là bộ TC **chất lượng cao, tự-adversarial** — review của Leader tập trung vào **đối chiếu fix + xếp ưu tiên các phát hiện**, không phải sửa lỗi hình thức.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — *áp cho việc ĐÓNG TICKET*, **không** phải chất lượng TC.

**Lý do ngắn gọn**: **Chất lượng thiết kế TC = xuất sắc** (49 TC phủ đủ core bug + 2 luồng sync/delete + mọi nhánh skip/error + concurrency 4 kịch bản + boundary + đối chứng âm + migration + production — không có GAP so với dev-impact, còn vượt scope). **NHƯNG ticket chưa đủ điều kiện đóng** vì chính bộ TC đã nêu **4 câu hỏi chặn về việc fix có thật sự trọn không** (dọn bản ghi cũ đang treo? mốc hẹn retry NULL? job có được đăng ký chạy? TC đang đọc **khác commit** với fix trong Redmine) — tất cả đang `pending`/`blocked`/`skip`, chưa được Dev/Leader trả lời.

---

## 2. Tóm tắt cho member

Bộ TC (lme-test-studio) là bộ **tốt nhất từng review** cho nhóm job: có oracle đo được (đếm số dòng sheet + log, không "thấy bình thường"), đối chứng âm (salon/lesson, bảng dùng chung web↔Java), kiểm scope 2 bot trùng tên (DATA-DB-001), và tự bắt được các nhánh code fix có thể bỏ sót. Không cần viết lại gì. **Việc còn lại KHÔNG phải sửa TC mà là chốt 4 câu hỏi với Dev/Leader** (§4.1) và **chạy lại các TC `pending`/chưa chạy trên ĐÚNG commit fix `8752ddc` + trên production**. Cảnh báo lớn nhất: fix trong Redmine chỉ **chặn treo MỚI**, còn phần "chạy cho các bản ghi **cũ**" trong tiêu đề ticket (dọn bản ghi đang treo + bản ghi mốc-hẹn-NULL) **có thể chưa được xử lý** — phải xác nhận trước khi đóng.

---

## 3. Coverage Matrix

> Impact từ `03-dev-impact.md`. Fix = set `result_error_google_id` atomic khi reset NEW + persist `ResultErrorGoogle=RUNNING` trước khi mở lại bản ghi.

| Impact | Loại | Priority (suy luận) | TCs cover | # | Status |
|---|---|---|---|---|---|
| **BUG** — bản ghi cũ thiếu ID retry → treo RUNNING | Fix | High | NEW-1, NEW-11, NEW-2, NEW-12 | 4 | OK (⚠ NEW-11 nêu câu hỏi verify — §4.1) |
| **F1** — `updateStatusSyncAndErrorId` (mới) | Function | Direct | NEW-1, NEW-4, NEW-11, NEW-34 | 4 | OK |
| **F2** — `updateStatusDeleteAndErrorId` (mới) | Function | Direct | NEW-3, NEW-13, NEW-30, NEW-31, NEW-41 | 5 | OK |
| **F3** — `RetryErrorGoogleSheetTask.needRetryErrorGoogle` (persist RUNNING trước reset) | Function | Direct | NEW-5, NEW-18, NEW-20 | 3 | OK |
| **D1** — `form_answer_result.result_error_google_id` (UPDATE) | Data | — | NEW-1, NEW-4, NEW-11, NEW-46 | 4 | OK |
| **D2** — `ResultErrorGoogle.status` (RUNNING→SUCCESS) | Data | — | NEW-11, NEW-18, NEW-32, NEW-47 | 4 | OK (⚠ NEW-47 — dọn treo cũ) |
| **T1** — Job retry SYNC form answer → GSheet | Feature | High | NEW-1/2/11/12/15/34/35/36/37/38/39 + skip/error branches | ~25 | OK (vượt scope) |
| **T2** — Retry DELETE form answer | Feature | Medium | NEW-3, NEW-13, NEW-30, NEW-31, NEW-33, NEW-41 | 6 | OK |
| **T3** — Sync/retry đa luồng (race) | Feature | High | NEW-4, NEW-5, NEW-8/20, NEW-21, NEW-42, NEW-44 | 6 | OK |

### ORPHAN TCs
Không có TC lạc chủ đề. Bộ TC **vượt** scope dev-impact (test cả nhánh skip/error/multi-page/legacy-header) — với bug **treo do idempotency**, coverage rộng theo từng nhánh set-RUNNING là **đúng** (không phải over-coverage AP-5), vì bất kỳ nhánh nào set RUNNING mà không đóng đều tái tạo bug.

> **Không GAP nào so với dev-impact.** Vấn đề nằm ở tính đúng của **fix** (không phải thiếu TC) — xem §4.1.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** | **Race-condition / transaction** (atomic UPDATE + persist RUNNING trước reset) **+ JOB nền + shared-code** (bảng ResultErrorGoogle dùng chung web↔Java) **+ migration-legacy** (cột ID retry nullable thêm 2026-03-30). |
| **Trigger space cần cover** | CONC-001 4 kịch bản race; JOB đếm vào/ra + backoff; REG-SHARED rà cả nhánh web + Java; nhánh skip/error đóng bản ghi; boundary (retry count, mốc hẹn NULL); bản ghi cũ (ID retry NULL) vs mới. |
| **Số trigger cover** | Race: NEW-4/5/20/21/42/44 (✓ đủ 4 kịch bản + restart). JOB: NEW-15/34 (✓ đếm vào/ra). Shared: NEW-9/10/48 (✓ có nhánh web). Skip/error: NEW-25/26/27/28/29/30/31/32/33 (✓). Boundary: NEW-23/24 (✓). Cũ/mới: NEW-11/12 (✓). → **Coverage fix-shape: xuất sắc.** |
| **KH report dạng** | Có root cause cụ thể (Dev auto-detect, có code ref dòng 839-840). Không symptom-only. |
| **Alternative root causes** | Bộ TC đã tự tìm **2 biến thể treo khác** cùng ticket: (a) bản ghi đã ở RUNNING không được nhặt lại — NEW-18/47; (b) mốc hẹn retry NULL không bao giờ được nhặt — NEW-23. → xem §4.1. |
| **Anti-patterns** | **Không** dính AP-1..AP-6. Ngược lại bộ TC **chủ động chống** AP: có oracle đếm (chống AP "thấy bình thường"), đối chứng âm, kiểm scope DB 2 bot, tách cũ/mới (RULE-09). |

---

## 4. Issues phát hiện

### 4.1 Blocker (chặn ĐÓNG TICKET — cần Dev/Leader trả lời trước khi nghiệm thu)

> Đây **không phải lỗi TC** — là 4 câu hỏi về **fix/scope** mà bộ TC đã đúng khi nêu ra. Xếp ưu tiên cao nhất vì đều là rủi ro "ticket chưa fix trọn / bug còn treo trên production".

- **[BLOCKER] FIX-SCOPE / NEW-47 — dọn bản ghi CŨ đang treo `RUNNING`**: Fix (commit 8752ddc) chỉ **chặn phát sinh treo MỚI** (set ID retry khi reset về NEW). Job chỉ nhặt bản ghi `status = NEW/0`; các bản ghi **đã treo ở RUNNING/1 từ trước** sẽ **không bao giờ được nhặt lại** → vẫn treo vĩnh viễn. Tiêu đề ticket ghi rõ *"nếu chạy cho các bản ghi **cũ**"*. → **Hỏi Dev/Leader: phát hành có kèm script/migration dọn bản ghi treo cũ (đưa RUNNING→NEW hoặc đóng) không?** Nếu không → ticket chưa fix trọn. (NEW-47 hiện `skip`.)
- **[BLOCKER] FIX-SCOPE / NEW-23 — biến thể treo thứ 2: mốc hẹn retry NULL**: Điều kiện nhặt job dùng `mốc_hẹn_retry < now()`; cột này **nullable** và bản ghi đời cũ có thể để trống. Trong MySQL `NULL < now()` **không đúng** → bản ghi cũ mốc-hẹn-NULL **không bao giờ được nhặt**. Fix trong file 03 **không đề cập** mốc hẹn. → **Hỏi Dev: fix có set/điền mốc hẹn retry cho bản ghi cũ không? Điều kiện lọc có xử lý NULL không?** Nếu không → còn 1 dạng treo nữa. (NEW-23 `pass` nhưng expected ghi rõ cần leader chốt.)
- **[BLOCKER] LỆCH COMMIT — TC đọc code khác fix trong Redmine**: Redmine §5 ghi fix = commit **`8752ddc...`** / branch **`m_202607_retry_form_update_id_39172`**. Nhưng các "PHÁT HIỆN REVIEW" của TC đọc branch **`m_202606_sync-formanswer-multithread`** / commit **`6065e70b`** (NEW-19/22/25/29). → **Toàn bộ khẳng định code-level của TC (nhánh nào fix chạm/không chạm) phải RE-VERIFY trên đúng `8752ddc`.** Ví dụ NEW-11 lo "fix không ghi ID retry cho bản ghi cũ" — nhưng file 03 §2 nói fix **có** set `result_error_google_id` atomic → **NEW-11 nhiều khả năng ĐẠT trên 8752ddc**, cần chạy lại để xác nhận.
- **[BLOCKER] NEW-22 — job có thật sự được đăng ký chạy không**: TC không tìm thấy nơi khởi động `RetryErrorGoogleSheetTask` / `HandleFormAnswerSyncGoogleSheetTask` (ngoài chính 2 class), config `ENABLE_RETRY_ERROR_GOOGLE_SHEET` cũ **không còn**. Nếu job không chạy trên production → fix vô nghĩa. → **Hỏi Dev: job retry được start ở tiến trình/instance nào trên production?** Verify bằng NEW-45 (prod) — **hiện chưa chạy**.

### 4.2 Major (nên xử lý)

- **[MAJOR] TC `pending`/`blocked`/chưa chạy chưa được giải quyết**: NEW-19, NEW-29 (`pending` — nhánh code cần Dev xác nhận, phụ thuộc §4.1 lệch commit); NEW-21, NEW-48 (`blocked`); NEW-45 (production — **chưa chạy**), NEW-44 (staging/prd — **chưa chạy**), NEW-46/47 (`skip`). → Không được đóng ticket khi các TC trung tâm (NEW-45 prod verify, NEW-47 dọn dữ liệu) chưa có kết quả.
- **[MAJOR] Verify auto-fill chưa tick (01 + 03)**: `01-bug-task.md` và `03-dev-impact.md` đều `Auto-filled: 2026-07-30 by /new-task`, checkbox verify **chưa tick**. Đặc biệt: file 03 §5 chỉ có commit/branch — cần tester đọc lại Redmine xác nhận đúng commit fix (liên quan blocker lệch commit §4.1). → Tester tick sau khi đối chiếu.
- **[MAJOR] ENV-003 / RULE-08 — production chưa verify**: Job nền chạy **tách tiến trình trên production** (Catalog D), race + đăng ký job chỉ lộ ở prod. NEW-45 (prd) là TC bắt buộc theo RULE-08 nhưng **chưa chạy** → không được kết luận từ staging.

### 4.3 Minor

- **[MINOR] Mã 観点 `TOOL-*` không có trong framework**: `TOOL-OLDREC/AXIS/NEGCTRL/APPENDANCHOR/ERRHYG-001` là taxonomy riêng của lme-test-studio, không map được vào `framework/checklist-lme.md`. Không ảnh hưởng coverage (nội dung TC đúng), nhưng khi sync về Sheet human/đối chiếu quan điểm chuẩn cần map lại (VD TOOL-OLDREC → DATA-MIG-001/COMPAT-LEGACY-001; TOOL-ERRHYG → INTG-SHEET-001/JOB-001).
- **[MINOR] Định dạng khác canonical**: bộ TC 18 cột của lme-test-studio, không phải 16 cột canonical — chấp nhận (nguồn tool khác), không yêu cầu convert.

### 4.4 Nit

- **[NIT] Live MCP không áp dụng cho task này**: khác task filter #39121 (verify được option filter qua `guide_filter_structure`), đây là **job nền + Google Sheet sync backend** — LME MCP (UI) không kiểm chứng được internal job. Các khẳng định code-level phải verify bằng **đọc code `8752ddc`** (linect-service), không có shortcut qua MCP.
- **[NIT] NEW-7/NEW-6/NEW-8 đã bị thay** bởi NEW-15/NEW-34/NEW-20 (bản có oracle đo) — nên đánh dấu deprecated để tránh chạy trùng.

---

## 5. TCs đề xuất bổ sung

> Bộ TC đã **gần như đầy đủ** — phần lớn "việc cần làm" là **chạy lại trên đúng commit + trả lời câu hỏi**, không phải viết TC mới. Chỉ bổ sung 1 TC cụ thể hóa NEW-47 (khi Leader chốt scope dọn dữ liệu) + 1 checklist re-run.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATAMIG001-01 | DATA-MIG-001 | Normal | Script dọn bản ghi treo `RUNNING` cũ chạy đúng phạm vi (nếu có trong phát hành) | - Trên môi trường có N bản ghi `ResultErrorGoogle` loại form answer treo `RUNNING/1` từ trước fix (đếm trước)<br>- Xác nhận với Leader phát hành có kèm script dọn | 1. Đếm N bản ghi treo RUNNING (form answer) + thời điểm tạo<br>2. Chạy script dọn kèm phát hành<br>3. Đếm lại theo trạng thái<br>4. Chọn 3 bản ghi, verify câu trả lời cuối lên đúng sheet | N bản ghi treo RUNNING loại form answer, tạo trước ngày phát hành | - Sau dọn: số bản ghi treo RUNNING (form answer) về 0 (hoặc đúng số Leader chốt)<br>- KHÔNG chạm bản ghi salon/lesson<br>- 3 bản ghi mẫu kết thúc đúng + có dòng đúng trên sheet | Chưa test | | PRODUCTION | | | | Đã hỏi leader (scope dọn dữ liệu) | Cụ thể hóa **NEW-47**. **Chỉ chạy sau khi Leader xác nhận có script dọn** — nếu không có script, đây là bằng chứng ticket chưa fix phần "bản ghi cũ" |

### Checklist re-run bắt buộc (không phải TC mới — chạy lại trên đúng commit `8752ddc`)
- [ ] **NEW-11** (TC trung tâm) — verify bản ghi cũ được ghi `result_error_google_id` + đóng SUCCESS trên `8752ddc`.
- [ ] **NEW-19, NEW-29** — re-verify nhánh code trên `8752ddc` (không phải `6065e70b`); gỡ `pending`.
- [ ] **NEW-22 + NEW-45** — verify job được đăng ký + chạy trên **production**.
- [ ] **NEW-23** — chốt hành vi mốc-hẹn-retry NULL với Dev.
- [ ] **NEW-44, NEW-21, NEW-48** — chạy các case `blocked`/manual (restart/phát hành/bảng dùng chung).

---

## 6. Spec update needed

- [x] **Cần Leader cấp chuẩn** (không phải update spec code, mà bổ sung định nghĩa để đối chiếu):
  - **Ngưỡng số lần retry** (NEW-24 dùng 5 — từ code, chưa có spec).
  - **Biên hết hạn hợp đồng 7 ngày** (NEW-27 — con số từ đâu).
  - **Nhãn/thông báo tiếng Nhật** màn cài đặt liên kết khi hạ trạng thái (NEW-49 — chưa có trong spec).
  - **Hành vi kỳ vọng cho mốc-hẹn-retry NULL** và **bản ghi treo cũ** (NEW-23, NEW-47 — spec không định nghĩa, đang suy từ mục tiêu ticket).

---

## 7. Checklist đã chạy

- [x] A. Coverage — matrix §3; mọi impact OK, không GAP; bộ TC vượt scope
- [x] B. Chất lượng từng TC — cao (oracle đo được, precondition đầy đủ, expected cụ thể)
- [x] C. Chất lượng bộ TC tổng thể — Normal/Abnormal/Boundary cân đối; có đối chứng âm; RULE-09 cũ/mới
- [x] D. Spec alignment — nhiều expected "spec không định nghĩa → nguồn ticket+code"; cần Leader chốt (§6)
- [x] E. Hành chính — nguồn lme-test-studio (không canonical); auto-fill 01/03 chưa tick (§4.2)
- [x] F. Base quan điểm test LME
  - [x] F.1 — bảng dưới
  - [x] F.2 Catalog — C (MAP-GS-01..07 Google Spread, MAP-SEND job), D/D2 (job tách tiến trình production, ENV-003)
  - [x] F.3 RULE — RULE-01 (có Boundary NEW-23/24 ✓) · RULE-07/DATA-DB-001 (NEW-17/41 scope 2 bot ✓) · RULE-08 (**thiếu prod NEW-45 chưa chạy** — §4.2) · RULE-09 (NEW-12/37 cũ-mới ✓) · RULE-05 (NEW-34 tra rate limit Google ✓)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover | Kết luận |
|---|---|---|---|---|
| **CONC-001** (idempotency/race) | Cao | ◯ (fix race treo RUNNING) | NEW-4/5/20/8 (+21/42/44 restart) | **OK** ✅ đủ 4 kịch bản + oracle đếm |
| **JOB-001** (job nền + API ngoài) | Cao | ◯ (job retry Google) | NEW-15/34 (đếm vào/ra, backoff, rate limit) | **OK** ✅ |
| **INTG-SHEET-001** (đồng bộ sheet ngoài) | Cao | ◯ (ghi/xóa Google Sheet) | NEW-3/35/36/38/42 | **OK** ✅ |
| **INTG-HOOK-002** (callback không tới) | TB | ◯ nhẹ (Google trả lỗi/không phản hồi) | NEW-34/35 (lỗi tạm/vĩnh viễn) | OK |
| **REG-SHARED-001** (shared code) | Cao | ◯ (bảng ResultErrorGoogle dùng chung web↔Java) | NEW-9/10/**48** | OK (NEW-48 negative control — chờ chạy) |
| **DATA-DB-001** (WHERE scope) | Cao | ◯ (UPDATE có điều kiện) | NEW-17/41 (2 bot trùng tên) | **OK** ✅ |
| **DATA-MIG-001** (migration/bản ghi cũ) | Cao | ◯ (cột ID retry nullable, bản ghi đời cũ) | NEW-46/47 | **RISK** — NEW-47 (dọn treo cũ) `skip`, chặn (§4.1) |
| **STATE-CLEAN-001** (dọn khi hủy/hết hạn) | Cao | ◯ (nhánh bot xóa/hết hạn) | NEW-26/27/30 | OK |
| **COMPAT-LEGACY-001 / RULE-09** | Cao | ◯ (header sheet cũ/mới; bản ghi cũ/mới) | NEW-12/37 | OK |
| **ENV-003** (dev/staging/prod, job tách) | Cao | ◯ (job nền tách tiến trình prod) | NEW-22/45 | **RISK/GAP** — NEW-45 prod **chưa chạy** → [MAJOR] §4.2 |
| **FUNC-DATE-001** (mốc thời gian NULL/biên) | Cao | ◯ (mốc hẹn retry) | NEW-23 | **RISK** — biến thể treo NULL chưa chốt (§4.1) |
| **FUNC-004** (biên số lượng) | Cao | ◯ (ngưỡng retry) | NEW-24 | OK (nguồn ngưỡng cần Leader chốt) |
| **DATA-REF-001** (tham chiếu mất đối tượng) | Cao | ◯ (answer/page/form đã xóa) | NEW-14/31/40 | OK |
| **MSG-USER-001** (LINE user lifecycle) | Cao | ◯ (user đã xóa) | NEW-29 | RISK — `pending` (§4.1) |
| **SEC-002** (không lộ token) | Cao | ◯ (log nhánh lỗi xác thực) | NEW-28/36 (kèm kiểm log) | OK |
| **CONC-002** (re-sync toàn bộ + data mới) | Cao* | ◯ (sheet rỗng ghi lại toàn bộ) | NEW-42 | OK |
| **REG-RUN-001** (job chạy dở khi release) | Cao | ◯ (phát hành giữa job) | NEW-21/44 | RISK — cả 2 chưa chạy xong (§4.2) |

> KHÔNG dùng §4 checklist-lme (FORM-01/CHAT-01/ADM-*/TPL-01) để flag — RULE-11.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<chờ Leader verify draft>` | |
| Tester | thanhntp (đã đọc & hiểu feedback) | |

---

### Tóm tắt hành động (round 2)
1. **Leader trả lời 4 câu hỏi chặn (§4.1)**: (a) có script dọn bản ghi treo cũ không? (b) mốc-hẹn-retry NULL có được xử lý? (c) reconcile commit `8752ddc` vs `6065e70b`; (d) job có đăng ký chạy prod?
2. **Chạy lại trên đúng commit `8752ddc`** các TC `pending` (NEW-11/19/29/22) — nhiều khả năng NEW-11 ĐẠT vì fill 03 nói fix có ghi ID retry.
3. **Chạy các TC production/chưa chạy**: NEW-45 (prd), NEW-44, NEW-21, NEW-48.
4. **Tester tick verify auto-fill** ở 01 + 03 sau khi đối chiếu Redmine.
5. Bộ TC **KHÔNG cần viết lại** — chỉ map lại mã `TOOL-*` sang 観点 chuẩn nếu sync về Sheet human.
