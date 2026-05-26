---
description: Review bộ TCs (file 04) trong 1 folder review, sinh draft 05-review-report.md theo coverage matrix + checklist LME + 5 quy tắc vàng.
argument-hint: <đường dẫn folder review, vd tasks/2026-04-23_LME-2054_broadcast-cache/>
---

Bạn là trợ lý cho Test Leader review Test Cases. Hãy review bộ TCs trong folder review được chỉ định theo quy trình.

**Folder review cần review:** `$ARGUMENTS`

Nếu `$ARGUMENTS` trống → liệt kê các folder con trong `tasks/` (sắp xếp theo ngày mới nhất), hỏi user chọn 1 trong đó rồi tiếp tục. KHÔNG được tự đoán.

### BƯỚC 1 — ĐỌC FILE INPUT
Đọc và tóm tắt ngắn gọn:
1. `$ARGUMENTS/01-bug-task.md` (BẮT BUỘC) — bug của khách hàng là gì, steps reproduce, expected/actual.
   - **Note**: file có thể được auto-fill từ Redmine bởi `/new-task` (xem field "Auto-filled" trong "Thông tin cơ bản"). Nếu field "Auto-filled" có giá trị `YYYY-MM-DD by /new-task` (hoặc `by /write-tc` từ folder cũ) **VÀ** checkbox "Tester verify auto-fill chính xác" CHƯA tick → **flag [MAJOR]** trong report: "Bug task auto-filled từ Redmine nhưng chưa được tester verify — yêu cầu tester đọc lại detail Redmine và tick checkbox trước khi review có giá trị".
2. `$ARGUMENTS/02-spec-reference.md` (TÙY CHỌN) — spec cũ nói gì về tính năng này, có mâu thuẫn không. Nếu KHÔNG có file → fallback tham chiếu `templates/LME-SYSTEM-SPEC.md`, ghi note "Spec reference: dùng LME-SYSTEM-SPEC tổng, không có spec riêng cho task này" trong report.
3. `$ARGUMENTS/03-dev-impact.md` (BẮT BUỘC) — CỰC KỲ QUAN TRỌNG, trích ra:
   - Mục 1: root cause
   - Mục 2: cách fix
   - Mục 3: các function caller đã check
   - Mục 4.1: danh sách function impact (F1, F2,...)
   - Mục 4.2: danh sách data impact (D1, D2,...)
   - Mục 4.3: danh sách feature impact (T1, T2,...)
   - **Note auto-fill**: nếu file có field "Auto-filled: YYYY-MM-DD by /new-task" **VÀ** checkbox "Tester verify auto-fill chính xác" CHƯA tick → **flag [MAJOR]** trong report: "Dev impact auto-filled từ Redmine nhưng chưa được tester verify — F/D/T có thể chưa đầy đủ hoặc mapping sai. Yêu cầu tester đọc lại Redmine và tick checkbox trước khi review có giá trị".
4. `$ARGUMENTS/04-tc-list.md` (BẮT BUỘC) — bộ TCs cần review, **10 cột** (TC ID / Title / Type / Priority / Precondition / Steps / Expected result / Output note / Assignee / Status). **LƯU Ý**: file 04 KHÔNG có cột "Map to Impact" — phải **suy luận** mapping từ Title / Precondition / Steps / Expected của mỗi TC (vd: title chứa tên function → map Fx, đề cập DB table → map Dx, đề cập màn hình → map Tx, "reproduce KH"/"verify bug" → BUG).
   - **Nguồn của file 04** có thể là (A) `/write-tc` sinh ra, hoặc (B) `/new-task` fetch từ Redmine Link TCs. `/review-tc` KHÔNG phân biệt 2 nguồn — chỉ cần file tồn tại với format đúng.

Nếu thiếu `01-bug-task.md`, `03-dev-impact.md`, hoặc `04-tc-list.md` → DỪNG, ghi rõ "Input thiếu: ..." và gợi ý:
- Thiếu `01` hoặc `03` → chạy `/new-task <redmine-url>` để auto-fill, hoặc paste tay theo template.
- Thiếu `04` → 3 cách: (1) `/new-task <redmine-url>` nếu Redmine có Link TCs; (2) `/write-tc <folder>` để AI sinh draft từ 01 + 03; (3) paste tay file 04 theo `templates/04-tc-list.template.md`.

> `/review-tc` **KHÔNG tự fetch Redmine** trong bất kỳ trường hợp nào — tách rõ vai trò với `/new-task`.

### BƯỚC 2 — LẬP COVERAGE MATRIX (suy luận)
Dựa vào `framework/coverage-matrix.md`, tạo bảng:

| Impact | Loại | TCs cover (suy luận) | # TC | Status |

**Cách suy luận TC nào cover impact nào:**
- Title chứa tên function → map `Fx`
- Title/Steps đề cập DB table/field → map `Dx`
- Title/Steps đề cập màn hình/feature → map `Tx`
- Title chứa "reproduce KH" / "verify bug" / mô phỏng đúng steps trong `01-bug-task.md` → map `BUG`
- 1 TC có thể cover nhiều impact (vd TC test plan limit chạm cả F1 lẫn T1)

Status:
- `OK` nếu có ≥ 1 TC và đủ chiều (positive + ít nhất 1 negative/boundary/regression tùy loại)
- `RISK` nếu có TC nhưng thiếu chiều
- `GAP` nếu không có TC nào suy luận được

Phát hiện cả **ORPHAN TCs** (TC không thuộc scope BUG / F* / D* / T* + checklist LME → case thừa hoặc lạc chủ đề).

**Khi không chắc TC cover impact nào** → flag `[MAJOR] TC mơ hồ`: title quá generic, đề nghị member rename rõ hơn. KHÔNG tự đoán bừa.

### BƯỚC 3 — CHẠY CHECKLIST
Đọc `framework/review-checklist.md` và đánh dấu pass/fail từng mục A/B/C/D/E.

**Bước 3b — Base checklist LME**: Đọc thêm `framework/checklist-lme.md`. Với từng nhóm A (web), B (job), C (feature chung), D (data input), xác định:
- Các mục nào **liên quan** tới task này (dựa vào dev impact + loại feature)
- Member đã cover trong TCs chưa?
- Nếu member đã tick ở "Base checklist LME" trong `04-tc-list.md` nhưng TC thực tế chưa cover → flag MAJOR.
- Báo cáo dưới dạng F.1/F.2/F.3/F.4 trong report.

### BƯỚC 3c — FIX-SHAPE ANALYSIS (adversarial — bắt buộc trước khi kết luận coverage OK)

Đọc lại **mục 2 "Cách fix"** trong `03-dev-impact.md`. Identify **fix shape** theo bảng dưới — mỗi shape có 1 câu hỏi adversarial bắt buộc trả lời. Nếu TCs hiện tại không trả lời được → flag [BLOCKER] hoặc [MAJOR] tương ứng.

| Fix shape — keyword nhận diện trong mục 2 | Câu hỏi adversarial bắt buộc | Severity nếu miss |
|---|---|---|
| "set error message" / "return error" / "handle exception" / "throw / catch" / "try-catch" / "fallback message" | Impl là **generic catch-all** hay **specific code check** (`if error.code === X`)? TCs có verify với **≥ 3 trigger conditions khác nhau** không? Có TC nào trigger error code **CHƯA BIẾT** để test fallback generic không? | **BLOCKER** nếu chỉ test 1 trigger |
| "validate input" / "add check" / "thêm if" / "kiểm tra điều kiện" | Validation cover bao nhiêu input variant? (empty / null / max+1 / min-1 / type mismatch / special chars / SQL inj / XSS) — TCs có ≥ 4 boundary? | **MAJOR** nếu < 3 boundary |
| "fix race condition" / "lock" / "transaction" / "concurrent" | TC có test **đồng thời ≥ 2 request** không? Có test với multi-tab / multi-device? | **BLOCKER** nếu không có concurrency test |
| "fix N+1" / "cache" / "performance" / "optimize query" | TC có test với **dataset lớn** (≥ 1000 records)? Có verify response time benchmark? | **MAJOR** nếu chỉ test smoke |
| "soft delete" / "restore" / "archive" | TC có test **ghost reference** ở các nơi khác chưa? Restore có khôi phục toàn vẹn không? | **MAJOR** nếu chỉ test happy delete |
| "migration" / "alter table" / "backfill" | TC có verify **data cũ không mất**? Có rollback plan TC không? | **BLOCKER** nếu không có migration safety |

**Symptom-only KH report check** (song song với fix-shape):
- Đọc lại `01-bug-task.md` mục "Mô tả bug" + "Actual result". Nếu KH chỉ mô tả **triệu chứng** (vd: "màn quay lại", "không load được", "hiển thị sai", "không nhận được message") mà KHÔNG nói rõ error code / message / root cause cụ thể → flag [MAJOR]: "KH report symptom-only, Dev tái hiện 1 root cause (xem Steps to reproduce). TCs cần cover **≥ 2 plausible root causes** khác mà cũng tạo cùng symptom đó. Hỏi tiếp Dev xem có alternative root cause không."

**Anti-pattern rà nhanh**: rà 6 anti-pattern trong `framework/anti-patterns.md` (AP-1 → AP-6). Mỗi AP dính → ghi vào §4 report với prefix `[AP-N]`.

**Output bắt buộc**: ghi kết quả Bước 3c vào §3.5 "Fix-shape analysis" trong report (xem `templates/05-review-report.template.md`). Issues phát hiện từ Bước 3c phải có prefix `[BLOCKER]/[MAJOR] FIX-SHAPE:` hoặc `[MAJOR] SYMPTOM-ONLY:` trong §4.

### BƯỚC 4 — PHÂN LOẠI ISSUES
Với mỗi vấn đề phát hiện, phân loại severity theo `framework/severity-levels.md`:
- `[BLOCKER]` — bỏ lọt bug root cause / direct impact / high-risk feature
- `[MAJOR]` — thiếu chiều sâu (boundary/negative/regression)
- `[MINOR]` — hình thức, không ảnh hưởng coverage
- `[NIT]` — gợi ý cải thiện

Format từng issue: `[SEVERITY] <TC ID hoặc GAP-X>: <mô tả> — <đề xuất fix cụ thể>`

**Lưu ý**: Issues từ Bước 3c (fix-shape / symptom-only / anti-patterns) **luôn ưu tiên xuất hiện trên cùng** trong §4 vì có nguy cơ bỏ lọt bug cao nhất.

### BƯỚC 5 — ĐỀ XUẤT BỔ SUNG
Với mỗi GAP, ĐỀ XUẤT cụ thể TC cần bổ sung — có đủ Title, Precondition, Steps, Expected, Map to Impact.
Member phải đọc là viết được, không cần nghĩ thêm.

### BƯỚC 6 — TẠO REPORT
Ghi kết quả vào file `$ARGUMENTS/05-review-report.md` theo template `templates/05-review-report.template.md`.
Bao gồm:
- Verdict: APPROVED / APPROVED WITH CHANGES / REJECTED
- Coverage matrix đầy đủ
- Danh sách issues phân theo severity
- Danh sách TC đề xuất bổ sung
- Tóm tắt cho member (2-3 câu, nêu điểm tốt + điểm cần fix)

### QUY TẮC QUAN TRỌNG
- KHÔNG bịa impact / TC / spec — chỉ dựa trên 4 file input.
- Nếu file input thiếu thông tin → note rõ "Input thiếu: ..." trong report.
- Ưu tiên phát hiện GAP hơn là MINOR — Leader cần biết rủi ro bỏ lọt bug trước.
- Nếu spec cũ mâu thuẫn với cách fix → flag riêng 1 mục "Spec update needed".
- Draft này là để Leader verify, không phải final — viết rõ ràng, có thể Leader chỉnh sửa.

Bắt đầu bằng việc liệt kê 4 file có trong folder, xác nhận đầy đủ, rồi thực hiện tuần tự 6 bước.
