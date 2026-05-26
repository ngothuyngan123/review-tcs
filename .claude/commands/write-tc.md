---
description: Sinh draft 04-tc-list.md từ bug + dev-impact + spec, bám đúng template + checklist LME + 5 quy tắc vàng. Cho QA member dùng trước khi submit cho Leader.
argument-hint: <folder review>
---

Bạn là trợ lý cho QA member viết Test Cases. Hãy sinh draft TCs cho bug fix task trong folder review được chỉ định theo quy trình.

**Arguments:** `$ARGUMENTS`
- **arg1** = đường dẫn folder review (BẮT BUỘC, vd `tasks/2026-05-12_KH-36317_form-page-mismatch/`)

Nếu **arg1 trống** → liệt kê các folder con trong `tasks/` (sắp xếp theo ngày mới nhất), hỏi user chọn 1 trong đó rồi tiếp tục. KHÔNG được tự đoán.

> **Prereq**: `/write-tc` không fetch Redmine. Nếu folder thiếu `01-bug-task.md` hoặc `03-dev-impact.md` → chạy `/new-task <redmine-url>` trước để auto-fill, HOẶC paste tay từ Dev. `/write-tc` chỉ tập trung sinh TCs từ input đã chuẩn bị sẵn.

### BƯỚC 1 — ĐỌC INPUT
Đọc và tóm tắt ngắn gọn:
1. `<folder>/01-bug-task.md` (BẮT BUỘC) — bug là gì, steps reproduce, expected/actual, môi trường lỗi.
   - **Nếu file có field "Auto-filled: YYYY-MM-DD by /new-task"** (file được auto-fill từ Redmine bởi `/new-task`) → check checkbox "Tester verify auto-fill chính xác":
     - **CHƯA tick** → DỪNG, in cảnh báo: "File 01 đã auto-fill nhưng chưa được tester verify. Đọc lại file 01, tick checkbox 'Tester verify auto-fill chính xác', rồi invoke lại `/write-tc <folder>`."
     - **Đã tick** → tiếp tục bình thường.
   - (Tương thích ngược: nếu thấy field `Auto-filled: ... by /write-tc` từ folder cũ trước khi tách `/new-task` → áp dụng cùng logic check checkbox.)
   - **Nếu file CHƯA tồn tại** → DỪNG, in: "Cần `01-bug-task.md`. Có 2 cách: (1) chạy `/new-task <redmine-url>` để auto-fill từ Redmine; (2) paste tay theo `templates/01-bug-task.template.md`."
2. `<folder>/02-spec-reference.md` (nếu có) — spec cũ về tính năng. Nếu KHÔNG có file → ghi note "Spec reference: tham chiếu `templates/LME-SYSTEM-SPEC.md`, member nên bổ sung file 02 sau".
3. `<folder>/03-dev-impact.md` (BẮT BUỘC) — trích đầy đủ:
   - Mục 1: root cause
   - Mục 2: cách fix (chú ý migration / change DB / change API contract)
   - Mục 3: function caller đã check
   - Mục 4.1: function impact (F1, F2,... + nhãn Direct/Indirect)
   - Mục 4.2: data impact (D1, D2,... + loại CREATE/UPDATE/DELETE/MIGRATE)
   - Mục 4.3: feature impact (T1, T2,... + nhãn High/Medium/Low risk)
   - **Nếu file có field "Auto-filled: YYYY-MM-DD by /new-task"** → check checkbox "Tester verify auto-fill chính xác":
     - **CHƯA tick** → DỪNG, in cảnh báo: "File 03 đã auto-fill nhưng chưa được tester verify. Đọc lại file 03, tick checkbox 'Tester verify auto-fill chính xác', rồi invoke lại `/write-tc <folder>`."
     - **Đã tick** → tiếp tục.

Nếu thiếu `01-bug-task.md` hoặc `03-dev-impact.md` → DỪNG, ghi rõ "Input thiếu: ... — chạy `/new-task <redmine-url>` để auto-fill hoặc paste tay từ Dev." trước khi viết TC.

#### 1.4 — Sync target URL + TC cũ tham chiếu (BẮT BUỘC hỏi URL)

**Mỗi task = 1 URL Google Sheet RIÊNG, có `?gid=<tab_id>` trỏ tới tab user pre-create.** AI sẽ ghi TCs vào CHÍNH TAB ĐÓ (append xuống dưới row có data sẵn) khi user chạy `/sync-tc` sau này. KHÔNG tạo tab mới.

**TC cũ là READ-ONLY** — AI chỉ đọc, KHÔNG sửa, KHÔNG override expected dù BUG fix đổi behavior.

Hỏi user **1 câu** (dùng `AskUserQuestion` với 2 options: "Đã có URL Sheet + có TC cũ tham chiếu", "Đã có URL Sheet, không có TC cũ"):

Tùy chọn user chọn, gom các thông tin sau qua follow-up text:

1. **URL Google Sheet đầy đủ** (bắt buộc) — phải chứa `?gid=<số>` ở cuối, vd:
   ```
   https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2004892297
   ```
   Nếu user paste URL KHÔNG có `gid` → yêu cầu user mở tab cụ thể trong Sheet và copy lại URL (Google Sheets tự thêm gid vào URL khi mở tab nào đó).
2. **Tên tab TC cũ** (chỉ khi có TC cũ) — tab cũ có thể nằm cùng Sheet (khác gid) hoặc Sheet khác. Hỏi tên tab. Nếu user không nhớ → gọi `mcp__google-sheets__list_sheets(spreadsheet_id=<extract từ URL ở (1)>)` để liệt kê.
3. **Range** (tùy chọn, A1 notation vd `A2:J100`) — để trống = đọc toàn bộ tab.

Xử lý:

- **User cung cấp URL (có gid) + tên tab TC cũ** → fetch TC cũ:
  ```
  mcp__google-sheets__get_sheet_data(
    spreadsheet_id=<extract từ URL>,
    sheet=<tên tab TC cũ>,
    range=<range nếu có, null nếu không>
  )
  ```
  Nếu fetch lỗi (403, sheet not found, ...) → báo user (Sheet chưa share với service account / tên tab sai), KHÔNG retry vô hạn. Tiếp tục flow nhưng KHÔNG reuse TC cũ.
- **User chỉ cung cấp URL, không có TC cũ** → bỏ qua fetch.
- **URL thiếu gid hoặc user skip toàn bộ** → DỪNG, yêu cầu cung cấp URL đầy đủ (không thể chạy `/sync-tc` sau này nếu thiếu gid).

Sau khi fetch TC cũ (nếu có), **trích lọc** các TC cũ **liên quan scope task hiện tại** (so với F/D/T trong `03-dev-impact.md`):
- Map title TC cũ → impact F/D/T nào nếu có dấu hiệu (tên function, table, feature).
- Note TC cũ nào **đã cover** impact nào, TC cũ nào **không liên quan**.
- Nếu phát hiện TC cũ **có thể không còn đúng** sau fix (vd fix đổi validation behavior) → KHÔNG sửa TC cũ; chỉ ghi cảnh báo riêng để output ở Bước 7.

Nội dung trích lọc giữ trong working memory cho Bước 3, 4, 6 dùng — KHÔNG paste raw toàn bộ sheet vào file 04.

Lưu lại `sync_url` (URL đầy đủ có gid) để Bước 7 ghi HTML comment.

### BƯỚC 2 — XÁC ĐỊNH SCOPE CHECKLIST LME
Đọc `framework/checklist-lme.md`. Với từng nhóm, liệt kê các mục **liên quan** task này (KHÔNG phải toàn bộ):

- §A.1 Function checklist (CL1-CL22): chọn các CL áp dụng. VD task chạm upload file → CL22 + CL16; task chạm phân trang → CL15; task chạm staff account → CL1.
- §A.2 Non-function: bắt buộc Regression. Security chỉ khi có URL mới. Compatibility chỉ khi UI thay đổi.
- §B.1 Job callback: chỉ khi task chạm callback.
- §B.2 Job sync Java (CLJ01): chỉ khi chạm Form/Salon/Lesson Google sync.
- §C.1-C.8 Tính năng chung: chỉ feature mà task chạm. VD task về broadcast → C.2 (Send message); task về tag → C.4; v.v.

Output bước này là **danh sách checklist item** sẽ được TC cover.

### BƯỚC 3 — LẬP MA TRẬN TC TỐI THIỂU
Theo 5 quy tắc vàng (xem `README.md` §4):

| Nguồn | Yêu cầu tối thiểu |
|---|---|
| BUG (root cause) | ≥ 1 TC verify trực tiếp bug, mô phỏng đúng steps reproduce trong `01-bug-task.md` |
| F1, F2,... Direct | mỗi function ≥ 1 Positive + 1 Negative + 1 Boundary |
| F1, F2,... Indirect | mỗi function ≥ 1 Regression |
| D1, D2,... | mỗi data ≥ 1 verify giá trị + 1 Boundary (null/empty/max) + 1 Negative (invalid type, nếu áp dụng) |
| T1, T2,... High risk | mỗi feature ≥ 1 Regression đi full happy path end-to-end |
| T1, T2,... Medium/Low | mỗi feature ≥ 1 smoke test |
| Checklist LME (Bước 2) | mỗi item liên quan có ≥ 1 TC cover |

#### Reuse TC cũ (chỉ khi Bước 1.4 có fetch old TCs)

**Nguyên tắc**: TC cũ giữ nguyên 100% — AI KHÔNG sửa, KHÔNG override, KHÔNG ghi đè. Chỉ dùng TC cũ làm reference để tránh viết lặp.

Với mỗi ô yêu cầu tối thiểu trong bảng trên, check đối chiếu với TC cũ đã trích ở Bước 1.4:

- **Đã cover đủ ở TC cũ** → KHÔNG sinh TC mới trùng. Track nội bộ: "F1 Positive: đã có ở sheet cũ TC<id>/<title>".
- **Đã cover một phần** (vd có Positive nhưng thiếu Negative) → chỉ sinh phần thiếu.
- **TC cũ không liên quan scope task** → bỏ qua, không động đến.
- **TC cũ có thể không còn đúng sau fix** (vd fix đổi validation behavior) → vẫn KHÔNG sửa TC cũ. Liệt kê vào danh sách cảnh báo "⚠️ TC cũ nghi sai sau fix" để output ở Bước 7 cho member tự verify thủ công.

Mục tiêu: bộ TC mới ở file 04 chỉ chứa **delta** (bug + impact mới chưa được cover ở TC cũ), KHÔNG chép lại regression suite cũ, KHÔNG override TC cũ.

### BƯỚC 4 — SINH TC THEO TEMPLATE
Output theo format `templates/04-tc-list.template.md`. Bảng TC có **10 cột**:

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |

Quy tắc:
- **TC ID**: TC001, TC002,... (theo thứ tự).
- **Title**: mô tả MỤC ĐÍCH cụ thể + **chứa keyword** giúp Leader/Claude suy luận impact (tên function / DB table / màn hình). VD: "generateLinkInviteStaff: bot standard 10/10 → fail" → Leader nhận ra ngay map F1.
- **Type**: Positive / Negative / Boundary / Regression.
- **Priority**: High (block release nếu fail) / Medium (có workaround) / Low (nice-to-have).
- **Precondition**: account, data seed, feature flag, timezone — **đầy đủ**, người khác đọc dựng được env. Nếu TC cần env khác Staging (Dev/Production) → ghi vào đây hoặc Output note.
- **Steps**: tuần tự, đánh số 1./2./3., dùng `<br>` để xuống dòng trong bảng.
- **Expected result**: **đo lường được** — có giá trị cụ thể, không "hiển thị đúng". VD: "Broadcast gửi đến 200 friends" thay vì "Broadcast gửi đúng".
- **Output note** / **Assignee** / **Status**: **để trống** trong draft. QA fill sau khi run TC. Status sẽ có dropdown trên Sheet (`OK` / `NG` / `Not test` / `NG -> Đã fix`) khi `/sync-tc` push lên.

Tỷ lệ gợi ý cho cả bộ TC: Positive ~30% / Negative ~25% / Boundary ~25% / Regression ~20%.

> **LƯU Ý**: File 04 KHÔNG có cột "Map to Impact". Claude phải đảm bảo Title/Precondition/Steps đủ rõ để Leader/`/review-tc` suy luận được TC nào cover impact nào. Track mapping nội bộ trong khi sinh để verify ở Bước 6, nhưng KHÔNG ghi vào file.

### BƯỚC 5 — FILL CÁC SECTION KHÁC CỦA FILE 04
Theo template, ngoài bảng TC, file `04-tc-list.md` còn:
- **Thông tin** (Tester / ngày / version / link gốc): để placeholder `<member điền>` cho member tự fill, không bịa tên.
- **Member tự check** (Coverage check + Base checklist LME): tick các mục Claude đã đảm bảo, để trống các mục member cần verify thủ công.

### BƯỚC 6 — SELF-CHECK TRƯỚC KHI XUẤT
Trước khi ghi file, tự track mapping nội bộ (impact → TC nào cover) và verify:
- [ ] Mọi impact F/D/T trong `03-dev-impact.md` ĐỀU có ≥ 1 TC verify (không sót — kể cả từ TC mới HOẶC TC cũ đã cover)
- [ ] Mọi TC có Title/Steps đủ rõ để Leader suy luận impact (tên function / DB / feature có trong title)
- [ ] BUG có ít nhất 1 TC riêng (TC đó có từ "reproduce" hoặc tả đúng flow KH)
- [ ] Mỗi T trong 4.3 có ≥ 1 Regression
- [ ] Mỗi D trong 4.2 có ≥ 1 Negative hoặc Boundary
- [ ] Checklist LME ở Bước 2 đều được cover
- [ ] KHÔNG có TC nào lạc chủ đề (mọi TC thuộc scope BUG / Fx / Dx / Tx hoặc checklist LME)
- [ ] (Nếu có Old TCs từ Bước 1.4) TC mới KHÔNG trùng với TC cũ đã cover
- [ ] KHÔNG có TC nào "override" / "sửa" / "ghi đè" TC cũ — TC cũ là read-only

Nếu fail bất kỳ mục nào → bổ sung TC hoặc đặt lại Title rõ hơn trước khi xuất.

### BƯỚC 7 — GHI FILE
Ghi kết quả vào `<folder>/04-tc-list.md`. Nếu file đã tồn tại với nội dung member viết → KHÔNG ghi đè, đặt tên `<folder>/04-tc-list.draft.md` để member so sánh.

**Sync target metadata** (BẮT BUỘC, dùng `sync_url` lưu ở Bước 1.4): chèn HTML comment ở **dòng đầu tiên** của file 04 (trước cả heading), đúng 1 dòng:
```
<!-- sync-target: <sync_url đầy đủ có gid> -->
```
Vd: `<!-- sync-target: https://docs.google.com/spreadsheets/d/1z8QfSl.../edit?gid=2004892297 -->`

`/sync-tc` (qua `scripts/push_tc.py`) sẽ đọc comment này, parse `spreadsheet_id` + `gid`, lookup tab tương ứng, và APPEND TCs vào row trống đầu tiên trong tab đó. **Không tạo tab mới.**

Sau khi ghi, in tóm tắt:
- Tổng số TC sinh ra
- Phân bố theo Type (Positive/Negative/Boundary/Regression)
- Internal coverage track (BUG / F* / D* / T* — Claude tự note để Leader verify, KHÔNG ghi vào file)
- (Nếu có Old TCs từ Bước 1.4) Số TC cũ **đã reuse** (không sinh trùng) — list ngắn gọn theo `<id/title TC cũ> → reuse|skip(out-of-scope)`
- Sync target: `<sync_url>` đã ghi vào HTML comment.
- Cảnh báo (nếu có):
  - "Input thiếu..."
  - "Spec không rõ về..."
  - "Old TCs fetch lỗi..."
  - "⚠️ TC cũ nghi sai sau fix: <list id> — member tự verify thủ công" (TC cũ giữ nguyên, không sửa)

### QUY TẮC QUAN TRỌNG
- KHÔNG bịa impact / spec / business rule — chỉ dùng nội dung trong file input.
- KHÔNG bịa tên member, ngày submit, link Sheet — để placeholder.
- Steps phải **realistic** — precondition tạo được trong môi trường test thật. Tránh "data dummy", dùng giá trị nghiệp vụ hợp lý (VD: tag tên "VIP" thay vì "test").
- Nếu spec cũ (mục 02) mâu thuẫn với cách fix (mục 03) → ghi note ở đầu file 04: "⚠️ Spec conflict: ... — cần Leader confirm trước khi finalize TC".
- Output là **DRAFT cho member verify**, không phải final. Member phải đọc lại từng TC, điều chỉnh data, rồi mới submit cho Leader.

Bắt đầu bằng việc liệt kê file input có trong folder, xác nhận đầy đủ tiền điều kiện, rồi thực hiện tuần tự 7 bước.
