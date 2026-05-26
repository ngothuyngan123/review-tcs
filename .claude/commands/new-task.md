---
description: Fetch Redmine issue → tạo folder task mới, auto-fill 01-bug-task.md + 03-dev-impact.md (+ 04-tc-list.md nếu Redmine có Link TCs). Bước CHUẨN BỊ INPUT, KHÔNG phải skill review/write.
argument-hint: <redmine-url>
---

Bạn là trợ lý cho QA chuẩn bị input task review từ Redmine. Sau khi chạy xong, **DỪNG** — KHÔNG tự gọi `/write-tc` hoặc `/review-tc`. Human sẽ tự gõ skill tiếp theo.

**Arguments:** `$ARGUMENTS`
- **arg1** = Redmine issue URL (BẮT BUỘC, vd `https://redmine.watermelon.vn/issues/36437`)

Nếu **arg1 trống** → DỪNG, in: "Cần Redmine URL. Cú pháp: `/new-task <redmine-url>`." KHÔNG được tự đoán URL.

---

### BƯỚC 1 — Parse URL + fetch Redmine

1. **Parse issue ID** từ URL — extract số sau `/issues/`. Vd `https://redmine.watermelon.vn/issues/36437` → `36437`. Nếu không match pattern `.+/issues/\d+` → DỪNG, in: "Redmine URL không hợp lệ, expect `<base>/issues/<số>`."

2. **Call MCP redmine** — nếu schema `mcp__redmine__redmine_request` chưa load, dùng `ToolSearch` query `select:mcp__redmine__redmine_request` trước:
   ```
   mcp__redmine__redmine_request(
     path="/issues/<id>.json",
     params={"include": "journals,attachments,relations"}
   )
   ```
   Nếu fail (401/403/404/server unreachable) → DỪNG, in lỗi + trỏ user đến [docs/REDMINE-SETUP.md](../../docs/REDMINE-SETUP.md). KHÔNG retry vô hạn.

---

### BƯỚC 2 — Tạo folder task

1. **Derive slug** từ `issue.subject`:
   - Strip Japanese chars (giữ JP nếu toàn bộ subject là JP thì transliterate đơn giản hoặc dùng issue_id làm slug).
   - Lowercase, replace whitespace/punctuation bằng `-`, collapse `-` liên tiếp, trim đầu/cuối.
   - Max 40 chars.

2. **Folder path**: `tasks/<YYYY-MM-DD hôm nay>_<issue_id>_<slug>/`.
   - Vd `tasks/2026-05-15_36437_form-page-mismatch/`.

3. Nếu folder **đã tồn tại**:
   - In cảnh báo: "⚠️ Folder `<path>` đã tồn tại — dùng folder cũ."
   - Khi ghi 01/03/04 (Bước 4) → check từng file:
     - Nếu file đã tồn tại + có nội dung → KHÔNG đè, ghi thành `.draft.md` (vd `01-bug-task.draft.md`) để user merge tay. In cảnh báo riêng cho mỗi file.

4. Nếu folder **chưa tồn tại** → tạo mới.

---

### BƯỚC 3 — Parse 3 section từ Redmine description

Description Redmine thường có 3 section (tiếng Việt hoặc Nhật). Dùng regex heuristic để locate. Note: Redmine description có thể là markdown HOẶC textile — giữ nguyên format gốc khi paste vào file output.

**Section A — Tái hiện bug** (optional)
- Trigger keywords: `Tái hiện bug`, `Tái hiện`, `再現手順`, `Steps to reproduce`, `Reproduce`.
- Nội dung dưới heading đó cho đến heading tiếp theo.
- Nếu KHÔNG tìm thấy section này → coi như "bug không tái hiện được".

**Section B — Đánh giá ảnh hưởng phía dev** (BẮT BUỘC theo workflow)
- Trigger keywords: `Đánh giá ảnh hưởng`, `Ảnh hưởng phía dev`, `Dev impact`, `影響範囲`, `影響評価`.
- Phải có cấu trúc 4 mục con: Nguyên nhân (`1.`), Cách fix (`2.`), Function caller đã check (`3.`), Đánh giá ảnh hưởng (`4.` với 4.1 function / 4.2 data / 4.3 feature).
- Parse từng mục con. Nếu format không match → vẫn lấy text raw, để user fill tay.

**Section C — Link TCs** (optional)
- Trigger keywords: `Link TCs`, `Link TC`, `TCs:`, `Test cases:`, kèm pattern URL Google Sheet + dòng `Row: <start>-<end>`.
- Format expected:
  ```
  Link TCs: https://docs.google.com/spreadsheets/d/<id>/edit?gid=<gid>
  Row: 2-50
  ```
- Parse `spreadsheet_id` từ URL (regex `/spreadsheets/d/([^/]+)/`).
- Parse `gid` từ URL (regex `[?&]gid=(\d+)`).
- Parse range từ `Row: <start>-<end>` → A1 notation `A<start>:J<end>` (giả định table TC chuẩn 10 cột).

---

### BƯỚC 4 — Ghi file `01-bug-task.md`

Theo `templates/01-bug-task.template.md`. Map từ Redmine response:

| Field template | Nguồn |
|---|---|
| `Bug ID / Ticket` | `#<issue.id> — <issue.subject>` |
| `Redmine URL` | `<arg1 raw>` |
| `Auto-filled` | `<YYYY-MM-DD hôm nay> by /new-task` |
| `Ngày báo cáo` | `issue.created_on` (chỉ phần date `YYYY-MM-DD`) |
| `Khách hàng / PM báo` | `issue.author.name` |
| `Module / Màn hình` | `issue.category.name` nếu có, fallback custom_fields (field "Module"/"Screen"), fallback `<chưa rõ — tester fill>` |
| `Priority` | `issue.priority.name` mapped: Normal/Low → Medium, High/Urgent/Immediate → High |
| `Môi trường phát hiện` | Parse regex từ description: `Production`/`Staging`/`Dev`/`step.lme.jp`/`staging.lme.jp`/`form.watermeru.com`. Fallback `<chưa rõ>` |
| `Mô tả bug` | `issue.description` giữ nguyên (KHÔNG diễn giải). Nếu có Section A (Tái hiện bug) tách ra Steps/Expected/Actual thì phần Mô tả bug chỉ chứa context chung phía trên Section A. |
| `Steps to reproduce` | Từ Section A. Parse sub-keywords: `Steps`, `Bước:`, `手順`. Nếu Section A không có → để trống. |
| `Expected result` | Từ Section A. Parse `Expected`, `Kết quả mong đợi`, `期待結果`. Để trống nếu không có. |
| `Actual result` | Từ Section A. Parse `Actual`, `Kết quả thực tế`, `現状`. Để trống nếu không có. |
| `Ảnh / video / log` | Checkbox tick nếu `issue.attachments` không rỗng. List URLs phía dưới section đó (Redmine attachment URL = `<base>/attachments/download/<id>/<filename>`). |
| `Tester verify auto-fill chính xác` | **unchecked** |

Nếu **Section A thiếu** (bug không tái hiện được):
- "Mô tả bug" = `issue.description` full text.
- "Steps to reproduce" / "Expected result" / "Actual result" để trống.
- Thêm note ở "Ghi chú thêm của Leader": `⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.`

---

### BƯỚC 5 — Ghi file `03-dev-impact.md`

Theo `templates/03-dev-impact.template.md`. Map từ Section B (Đánh giá ảnh hưởng):

| Field template | Nguồn |
|---|---|
| `Dev phụ trách` | Từ Section B nếu có ghi (regex `Dev`, `担当`), fallback `issue.assigned_to.name` nếu có, fallback `<chưa rõ>` |
| `Commit / Pull Request` | Parse URL Github/Gitlab/Bitbucket trong description hoặc journals. Fallback `<chưa có>` |
| `Branch` | Parse pattern `branch:` / `Branch:` trong Section B. Fallback `<chưa rõ>` |
| `Ngày submit đánh giá` | Tìm note/journal có mention Section B, lấy `created_on`. Fallback `<chưa rõ>` |
| `Auto-filled` | `<YYYY-MM-DD hôm nay> by /new-task` (thêm field này vào template, xem cập nhật template ở plan) |
| `1. Nguyên nhân` | Sub-section `1.` của Section B raw text |
| `2. Cách fix` | Sub-section `2.` raw text |
| `3. Đã check và sửa các function ...` | Sub-section `3.` raw text. Nếu Dev list dạng bảng → giữ markdown bảng. Nếu list dạng plain → convert sang bảng template (file/function/thay đổi/lý do). |
| `4.1. List function bị ảnh hưởng` | Sub-section `4.1` raw. Parse pattern `F1 / F2 / ...` nếu có. Giữ nguyên cột Direct/Indirect nếu Dev đã ghi. |
| `4.2. List data bị update` | Sub-section `4.2` raw. Parse `D1 / D2 / ...`. Giữ thao tác CREATE/UPDATE/DELETE/MIGRATE. |
| `4.3. List tính năng bị ảnh hưởng` | Sub-section `4.3` raw. Parse `T1 / T2 / ...`. Giữ High/Medium/Low risk. |
| `Tester verify auto-fill chính xác` (mới) | **unchecked** |

Nếu **Section B thiếu HOẶC parse fail toàn bộ**:
- Fill skeleton template với placeholder `<Input thiếu — Dev chưa cung cấp>`.
- Ghi cảnh báo lớn ở đầu file: `⚠️ INPUT THIẾU: Redmine #<id> chưa có "Đánh giá ảnh hưởng phía dev". /write-tc và /review-tc sẽ fail nếu chạy với input này. Yêu cầu Dev bổ sung trước khi tiếp tục.`

---

### BƯỚC 6 — Ghi file `04-tc-list.md` (chỉ khi có Section C)

**Nếu Section C tồn tại + parse thành công** `spreadsheet_id` + `gid` + `range`:

1. **Resolve tên tab** từ `gid`:
   ```
   mcp__google-sheets__list_sheets(spreadsheet_id=<id>)
   ```
   Tìm sheet có `sheetId == gid`. Nếu không match → in cảnh báo "Gid không thuộc Sheet này — skip file 04. Verify lại URL Sheet trong Redmine."

2. **Fetch TC rows**:
   ```
   mcp__google-sheets__get_sheet_data(
     spreadsheet_id=<id>,
     sheet=<tên tab resolve được>,
     range="A<start>:J<end>"
   )
   ```
   Nếu fail (403, 404, ...) → in cảnh báo (Sheet chưa share với service account / range sai), skip file 04, KHÔNG retry. Tiếp tục flow nhưng KHÔNG có file 04.

3. **Ghi file** `04-tc-list.md`:
   - Dòng 1: `<!-- sync-target: <URL Sheet đầy đủ có gid> -->`
   - Dòng 2-: heading + bảng TC theo `templates/04-tc-list.template.md`. Convert rows từ Sheet (mỗi row = 1 TC) sang format markdown bảng 10 cột (TC ID / Title / Type / Priority / Precondition / Steps / Expected result / Output note / Assignee / Status). Giữ NGUYÊN giá trị cell, KHÔNG sửa expected/title dù bug fix đổi behavior.
   - Section "Thông tin" / "Member tự check" để placeholder `<member điền sau khi review>`.
   - Cuối file, thêm note: `<!-- Source: fetched từ Redmine #<id> Link TCs, range A<start>:J<end> tab "<tên tab>" lúc <YYYY-MM-DD HH:MM>. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->`

4. Nếu file 04 **đã tồn tại** trong folder (case folder cũ) → ghi `04-tc-list.draft.md` thay vì đè.

**Nếu Section C không có HOẶC parse fail**:
- KHÔNG báo lỗi (đây là case bình thường — Redmine không bắt buộc có Link TCs).
- KHÔNG tạo file 04.
- In note ở summary cuối: "Redmine không có Link TCs. Nếu muốn `/review-tc`, chạy `/write-tc <folder>` trước để sinh draft TCs."

---

### BƯỚC 7 — In summary + DỪNG

In summary chuẩn:

```
✅ Created task folder: tasks/<YYYY-MM-DD>_<id>_<slug>/

Files populated:
- 01-bug-task.md       <auto-filled từ Redmine #<id>>
- 03-dev-impact.md     <auto-filled từ Redmine #<id>>
- 04-tc-list.md        <fetched N TCs từ Sheet "<tên tab>" range A<start>:J<end>>   # chỉ in khi có file này

⚠️ Verify required (BẮT BUỘC trước khi chạy skill tiếp theo):
1. Mở 01-bug-task.md → đọc description + steps → tick checkbox "Tester verify auto-fill chính xác".
2. Mở 03-dev-impact.md → đọc 4 mục → tick checkbox "Tester verify auto-fill chính xác".
3. (Nếu có) Mở 04-tc-list.md → verify TCs fetch đúng range.

Next step (human chọn 1, KHÔNG tự chain):
- /write-tc tasks/<folder>/     # nếu chưa có file 04 hoặc cần sinh bổ sung
- /review-tc tasks/<folder>/    # nếu đã có file 04 cần review

Warnings (nếu có):
- ⚠️ Bug không tái hiện được trong Redmine (file 01 Steps/Expected/Actual trống).
- ⚠️ INPUT THIẾU: Section "Đánh giá ảnh hưởng" trong Redmine.
- ⚠️ Sheet fetch fail: <lý do> — skip file 04.
- ⚠️ Folder đã tồn tại, ghi thành .draft.md: <list files>.
```

**SAU SUMMARY → DỪNG TUYỆT ĐỐI.** KHÔNG tự gọi `/write-tc` hoặc `/review-tc`. Đó là 2 skill độc lập, human gõ slash mới chạy.

---

### QUY TẮC

- KHÔNG bịa nội dung Redmine — chỉ dùng response từ MCP redmine.
- KHÔNG diễn giải lại description khi map vào 01/03 — paste nguyên văn.
- KHÔNG sửa TCs cũ fetch từ Sheet — TCs cũ là **read-only**, kể cả khi nghi không còn đúng sau fix.
- KHÔNG đè file đã có nội dung — ghi `.draft.md` để user merge tay.
- KHÔNG chain skill sau khi xong — DỪNG tại Bước 7.
- Redmine API key + Sheet credentials đọc từ `.env` / `credentials/` (đã setup). Nếu fail → trỏ docs setup, KHÔNG paste API key/secret vào output.

Bắt đầu bằng việc parse URL, gọi MCP redmine, rồi thực hiện tuần tự 7 bước.
