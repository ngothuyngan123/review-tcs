---
description: Sinh draft 04-tc-list.md từ bug + dev-impact + spec, bám đúng template + 80 quan điểm test LME (2 tầng quan điểm/catalog) + 12 RULE + 5 quy tắc vàng. Đối chiếu TC cũ (Studio/Sheet/file 04) + kho-tcs để không viết trùng. Cho QA member dùng trước khi submit cho Leader.
argument-hint: <folder review>
---

Bạn là trợ lý cho QA member viết Test Cases. Hãy sinh draft TCs cho bug fix task trong folder review được chỉ định theo quy trình.

**Arguments:** `$ARGUMENTS`
- **arg1** = đường dẫn folder review (BẮT BUỘC, vd `tasks/2026-05-12_KH-36317_form-page-mismatch/`)

Nếu **arg1 trống** → liệt kê các folder con trong `tasks/` (sắp xếp theo ngày mới nhất), hỏi user chọn 1 trong đó rồi tiếp tục. KHÔNG được tự đoán.

> **Prereq**: `/write-tc` không fetch Redmine. Nếu folder thiếu `01-bug-task.md` hoặc `03-dev-impact.md` → chạy `/new-task <redmine-url>` trước để auto-fill, HOẶC paste tay từ Dev. `/write-tc` chỉ tập trung sinh TCs từ input đã chuẩn bị sẵn.

### BƯỚC 1 — ĐỌC INPUT
Đọc và tóm tắt ngắn gọn:
1. `<folder>/01-bug-task.md` (BẮT BUỘC) — bug là gì, steps reproduce, expected/actual.
   - File 01 là bản **rút gọn** (2026-09-05): chỉ có `Bug ID / Ticket` · `Module / Màn hình` · Mô tả bug (**bản dịch tiếng Việt**, không còn khối 原文 JP) · Steps · Expected · Actual · Attachment · Ghi chú Leader · Dữ liệu định danh ca lỗi · Journal Redmine. **KHÔNG còn** field `Auto-filled` / `Môi trường phát hiện` / `Priority` và **KHÔNG còn** checkbox "Tester verify" → không check verify gate ở file 01.
   - **Môi trường lỗi** (nếu cần): đọc ở `Ghi chú thêm của Leader`; không ghi ở đó → coi như chưa rõ, ghi `Môi trường test` của TC theo RULE-08 + note cần confirm.
   - **`Dữ liệu định danh ca lỗi`** (nếu có) là nguồn dựng `Điều kiện tiền đề` + `Dữ liệu test/input` của TC — ưu tiên dùng ID thật ở đây thay vì bịa dữ liệu mới.
   - **Nếu file CHƯA tồn tại** → DỪNG, in: "Cần `01-bug-task.md`. Có 2 cách: (1) chạy `/new-task <redmine-url>` để auto-fill từ Redmine; (2) paste tay theo `templates/01-bug-task.template.md`."
2. **Spec** — đọc thẳng từ nguồn, **KHÔNG tạo `02-spec-reference.md`** (đã bỏ khỏi bộ file chuẩn; folder cũ còn file này thì vẫn dùng được). **Thứ tự ưu tiên** (dừng ở nguồn đầu tiên trả lời được "hành vi ĐÚNG của chức năng này là gì"):

   | # | Nguồn | Cách dùng |
   |---|---|---|
   | 1 | [`spec-features/<feature>/feature-spec.md`](../../spec-features/) | Spec reverse-engineer từ source LME — lấy **Business rules** gốc. Tra mã màn hình `FA-xxx` → tên thư mục feature ở bảng feature [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) (file tổng dùng làm **mục lục**, không còn là nguồn spec chính). |
   | 2 | Spec ngoài (Confluence / Google Docs / …) | **Chỉ khi human dán link hoặc nội dung trực tiếp trong lệnh.** **KHÔNG tự đi tìm, KHÔNG WebFetch.** |

   - Ghi note ở Bước 7 đã dùng nguồn spec nào (link section cụ thể).
   - ⚠️ **KHÔNG WebFetch https://lme.jp/manual/** (bỏ từ 2026-09-08) — spec chỉ đọc trong [spec-features/](../../spec-features/); không có ở đó thì coi như **không có spec**, không đi tìm nguồn web thay thế.
   - **Không nguồn nào có spec** cho chức năng → mọi TC liên quan ghi `Trạng thái đánh giá spec` = `Spec không ghi` + nêu **cần hỏi ai** ở `Ghi chú`, và đưa vào cảnh báo Bước 7. **KHÔNG tự bịa business rule.**
   - Mọi **business rule** đọc được phải có ≥ 1 TC verify.
3. `<folder>/03-dev-impact.md` (BẮT BUỘC) — trích đầy đủ:
   - Mục 1: root cause
   - Mục 2: cách fix (chú ý migration / change DB / change API contract)
   - Mục 3: function caller đã check
   - Mục 4.1: function impact (F1, F2,... + nhãn Direct/Indirect)
   - Mục 4.2: data impact (D1, D2,... + loại CREATE/UPDATE/DELETE/MIGRATE)
   - Mục 4.3: feature impact (T1, T2,... + nhãn High/Medium/Low risk)
   - **Nếu file có field "Auto-filled: YYYY-MM-DD by /new-task"** → check checkbox "Tester verify auto-fill chính xác":
     - **CHƯA tick** → KHÔNG dừng. Vẫn tiếp tục viết TCs bình thường, nhưng GHI NHẬN để in cảnh báo ở Bước 7: "⚠️ File 03 auto-fill chưa được tester verify (checkbox 'Tester verify auto-fill chính xác' chưa tick) — impact F/D/T chưa được người xác nhận, member nên verify lại đánh giá ảnh hưởng + TCs trước khi submit."
     - **Đã tick** → tiếp tục (không cảnh báo).

Nếu thiếu `01-bug-task.md` hoặc `03-dev-impact.md` → DỪNG, ghi rõ "Input thiếu: ... — chạy `/new-task <redmine-url>` để auto-fill hoặc paste tay từ Dev." trước khi viết TC.

#### 1.4a — Sync target URL (BẮT BUỘC hỏi URL)

**Mỗi task = 1 URL Google Sheet RIÊNG, có `?gid=<tab_id>` trỏ tới tab user pre-create.** AI sẽ ghi TCs vào CHÍNH TAB ĐÓ (append xuống dưới row có data sẵn) khi user chạy `/sync-tc` sau này. KHÔNG tạo tab mới.

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

- **URL thiếu gid hoặc user skip toàn bộ** → DỪNG, yêu cầu cung cấp URL đầy đủ (không thể chạy `/sync-tc` sau này nếu thiếu gid).
- Lưu lại `sync_url` (URL đầy đủ có gid) để Bước 7 ghi HTML comment.

> ⚠️ `sync_url` là **đích ghi TC mới**, KHÔNG phải nguồn TC cũ. Nguồn TC cũ xử lý riêng ở 1.4b.

#### 1.4b — TC cũ tham chiếu: 3 nguồn theo thứ tự ưu tiên

> Cùng thứ tự với [`/review-tc` BƯỚC 0](review-tc.md): **(1)** MCP LME TEST STUDIO → **(2)** link Google Sheet do human cung cấp → **(3)** `04-tc-list.md` sẵn có trong folder.
> **Dừng ở nguồn ĐẦU TIÊN lấy được TC** — không fetch nguồn dưới, không gộp, không đối chiếu chéo. In rõ nguồn đang dùng + tổng số TC cũ đọc được.

**Nguồn 1 — MCP LME TEST STUDIO** (mặc định, luôn thử trước):
- Ticket lấy từ tên folder `tasks/<YYYY-MM-DD>_<ticket>_<slug>/` hoặc field `Bug ID / Ticket` trong `01-bug-task.md`.
- `ToolSearch` → `select:mcp__claude_ai_MCP_LME_TEST_STUDIO__task_list,mcp__claude_ai_MCP_LME_TEST_STUDIO__testcase_list`, rồi `task_list(ticket_id=<ticket>)` → `testcase_list(task_id=<id>, limit=100)`.
- Payload **vượt token limit** → parse bằng `python scripts/parse_studio_tcs.py <tool-result file> --ticket <ticket> --task <task_id> --out <scratchpad>/ref-tcs-studio-<task_id>.md`, **chỉ đọc digest ở stdout**, KHÔNG nạp tool-result vào context.
  ⚠️ File tham chiếu ghi ra **scratchpad**, KHÔNG ghi vào `tasks/<folder>/` — folder review chỉ chứa đúng 4 file `01` · `03` · `04` · `05`. Đây là TC **đọc để tránh viết trùng**, không phải sản phẩm của task.
- Task đã có TC trên Studio → **cảnh báo ở Bước 7**: "task #<id> đã có `<n>` TC trên Studio — TC sinh mới chỉ là **delta**; cân nhắc `/review-tc` thay vì viết mới."
- 0 task / 0 TC / MCP chưa authorize → in lý do, sang nguồn 2.

**Nguồn 2 — link Google Sheet do human cung cấp** (tab TC cũ đã hỏi ở 1.4a, hoặc link khác user đưa):
```
mcp__google-sheets__get_sheet_data(
  spreadsheet_id=<extract từ URL>,
  sheet=<tên tab TC cũ>,
  range=<range nếu có, null nếu không>
)
```
- Sheet dùng cấu trúc cây `Main Function / Sub1..Sub5` có ô gộp → **BẮT BUỘC** `python scripts/fetch_grid.py <spreadsheet_id> <out.json> "<tên tab>"` (`values.get` thuần làm sai phân cấp). File `.xlsx` trên Drive → `python scripts/fetch_xlsx.py`.
- Fetch lỗi (403 / sheet not found / gid sai) → báo user (Sheet chưa share service account / tên tab sai), KHÔNG retry vô hạn, sang nguồn 3.
- User nói không có TC cũ → bỏ qua nguồn 2, sang nguồn 3.

**Nguồn 3 — `<folder>/04-tc-list.md` sẵn có** (round trước / member đã viết tay / snapshot do `/new-task` ghi): đọc thẳng, dùng làm TC cũ tham chiếu.

**Cả 3 nguồn đều không có** → không có TC cũ tham chiếu; tiếp tục viết TC bình thường, ghi note ở Bước 7.

> ⚠️ File 04 **luôn phải đọc ở 1.4c**, kể cả khi đã dừng ở nguồn 1 hoặc 2 — vì nó vừa là nguồn tham chiếu, vừa là **file đích sẽ được append**. Việc "dừng ở nguồn đầu tiên" chỉ áp dụng cho việc chọn **bộ TC cũ tham chiếu**, không miễn cho việc đọc file đích.

Sau khi lấy được TC cũ, **trích lọc** các TC **liên quan scope task hiện tại** (so với F/D/T trong `03-dev-impact.md`):
- Map title TC cũ → impact F/D/T nào nếu có dấu hiệu (tên function, table, feature).
- Note TC cũ nào **đã cover** impact nào, TC cũ nào **không liên quan**.
- TC cũ **có thể không còn đúng** sau fix (vd fix đổi validation behavior) → **KHÔNG sửa TC cũ**; ghi cảnh báo riêng để output ở Bước 7.

**TC cũ là READ-ONLY ở mọi nguồn** — chỉ đọc để tránh viết lặp. Nội dung trích lọc giữ trong working memory cho Bước 3, 4, 6 — KHÔNG paste raw toàn bộ vào file 04.

#### 1.4c — Đọc FILE ĐÍCH `04-tc-list.md` (BẮT BUỘC, luôn chạy)

`/write-tc` **KHÔNG BAO GIỜ ghi đè** `04-tc-list.md` và **không sinh** `04-tc-list.draft.md`. Chế độ ghi quyết định ở đây:

| Tình trạng `<folder>/04-tc-list.md` | Chế độ | Xử lý |
|---|---|---|
| **Chưa tồn tại** | `CREATE` | Bước 7 ghi file mới đầy đủ (header + Thông tin + bảng TC + Member tự check). |
| **Đã tồn tại** (bất kể do ai ghi: member, `/new-task`, round trước) | `APPEND` | Bước 7 **chỉ chèn thêm dòng TC còn thiếu** vào cuối bảng TC hiện có. Giữ nguyên 100% dòng cũ, header, config `sync-tcs`/`source`/`sync-target`, section `Thông tin`, section `Member tự check`. |

Ở chế độ `APPEND`, trích ra từ file đích (giữ trong working memory):
1. **Toàn bộ TC đã có** → đây là tập chống trùng bắt buộc ở Bước 3f + Bước 6 (so theo **4 yếu tố**, không so chuỗi).
2. **Số thứ tự lớn nhất của từng `TC No.` theo mã quan điểm** → TC mới đánh số **tiếp nối**, không đánh lại từ `01`. VD file đã có `TC-REGSHARED001-01` … `-06` → TC mới bắt đầu `TC-REGSHARED001-07`.
3. **Format bảng đang dùng** (16 cột canonical hay 10 cột cũ trước 2026-07-16) → TC append **bám đúng format đang có của file**, KHÔNG convert file cũ sang format mới.
4. Dòng đầu file có sẵn `<!-- sync-target: ... -->` / `<!-- sync-tcs: ... -->` / `<!-- source: ... -->` chưa → quyết định ở Bước 7 có chèn `sync-target` hay không.

In ra trước khi sang Bước 2: `Chế độ ghi: CREATE | APPEND (<n> TC đã có, format <16 cột | 10 cột cũ>)`.


### BƯỚC 2 — CHỌN QUAN ĐIỂM TEST (tầng 1) + MỞ CATALOG (tầng 2)

**80 quan điểm / 18 nhóm + 12 RULE**. Quy trình **2 tầng, bắt buộc đủ 2 bước** (bỏ bước 2 là chỗ bug lọt):

> ⚡ **Đọc INDEX, KHÔNG nạp toàn văn 2 file gốc** (574 + 375 dòng ≈ 37k token):
> 1. [framework/checklist-lme.index.md](../../framework/checklist-lme.index.md) — 80 dòng `Mã · Ưu tiên · Catalog · Nhóm · Trigger · Dòng`. Đủ để duyệt ◯/× ở **2a**.
> 2. `sed -n '58,73p' framework/checklist-lme.md` — 12 RULE, đọc đủ.
> 3. Chỉ với các mã đã đánh **◯**: `sed -n '<Dòng>p' framework/checklist-lme.md` để lấy `Kiểm tra` + `Evidence`.
> 4. [framework/catalog-lme.index.md](../../framework/catalog-lme.index.md) §2 — tra ngược `quan điểm ◯ → mục catalog phải mở` + số dòng, rồi `sed` đúng vùng đó ở **2b**.
>
> 2 file index là **output tự sinh** bởi `scripts/build_indexes.py`. Nghi index cũ → chạy `python scripts/build_indexes.py --verify`.

**2a — Duyệt tầng 1, đánh ◯ / ×.** Với **từng** quan điểm, đọc dòng **Trigger** ("khi nào bắt buộc chọn") rồi quyết định:
- `◯` = áp dụng cho task này.
- `×` = không áp dụng → **BẮT BUỘC ghi lý do** (RULE-03). Quan điểm ưu tiên **Cao** đánh × với lý do mơ hồ → ghi vào cảnh báo Bước 7 để Leader duyệt.
- Một số quan điểm **luôn ◯**: `FUNC-001`. Các quan điểm có Trigger dạng "BẮT BUỘC khi..." → chỉ cần task khớp điều kiện là **không được đánh ×**.
- Suy ra ◯/× từ: root cause + cách fix (mục 2 file 03), F/D/T impact, loại feature. VD: fix chạm upload ảnh → `MEDIA-001` + `MEDIA-IMG-001` + `MEDIA-CLEAN-001` + `ENV-003`; fix chạm gửi tin có filter → `MSG-001` + `BULK-001`; fix có UPDATE/DELETE → `DATA-DB-001` (không bao giờ × được).

**2b — Với mỗi ◯, mở đúng catalog** — tra ở §2 của [catalog-lme.index.md](../../framework/catalog-lme.index.md) rồi `sed -n '<Dòng>p' framework/catalog-lme.md`:
- **Catalog A** (21 kiểu input) → lấy nguyên 3 cột Normal / Abnormal / Boundary thành TC.
- **Catalog B** (15 thành phần UI) → lấy thuộc tính & hành vi phải kiểm.
- **Catalog C** (bản đồ LME) → **duyệt HẾT khối tương ứng**: 21 đường gửi tin · 9 nơi hiển thị + 11 nơi update friend info · tag · Google Spread · 25 màn sort · 5 case plan limit · bill tiền · danh sách dọn dẹp khi hủy hợp đồng · ma trận LIFF · phân quyền.
- **Catalog D / D2** (khác biệt môi trường + job) → **RULE-08**: media / domain / job / loadbalance / bill tiền **không được kết luận từ staging**.
- **Catalog E** (media) → giới hạn dung lượng theo **nơi sử dụng** (chat 1:1 ≠ friend info) + ma trận tính năng × thao tác.

**Output bước này** (giữ trong working memory, in tóm tắt ở Bước 7): danh sách `<mã quan điểm> ◯/× | ưu tiên | catalog đã mở`. Đây là nguồn để lập ma trận TC ở Bước 3.

### BƯỚC 3 — LẬP MA TRẬN TC TỐI THIỂU

Bộ TC phải thỏa **đồng thời** 2 nguồn yêu cầu:

**3a — RULE-01 (pattern tối thiểu theo quan điểm):**

| Ưu tiên quan điểm (◯) | Yêu cầu tối thiểu |
|---|---|
| **Cao** | **≥ 3 TC: Normal + Abnormal + Boundary** (đủ cả 3). Thiếu 1 trong 3 → **bắt buộc ghi lý do** ở cột `Ghi chú` (VD "quan điểm không có khái niệm biên") |
| **Trung bình / Thấp** | ≥ 1 Normal, khuyến khích thêm Abnormal |

> **Cột `Loại case` của file 04 dùng ĐÚNG 3 giá trị canonical**: `Normal` / `Abnormal` / `Boundary`. **Không còn** Positive/Negative/Regression. TC verify tính năng cũ không hỏng (impact T*, nhóm quan điểm REG-* / COMPAT-LEGACY-001) xếp vào `Normal` (luồng cũ chạy đúng) hoặc `Abnormal` (điều kiện lỗi cũ) và **ghi chữ `regression` ở cột `Ghi chú`** — regression KHÔNG phải 1 loại case riêng.

**3b — Coverage theo impact (từ `03-dev-impact.md`):**

| Nguồn | Yêu cầu tối thiểu |
|---|---|
| BUG (root cause) | ≥ 1 TC verify trực tiếp bug, mô phỏng đúng steps reproduce trong `01-bug-task.md` |
| F1, F2,... Direct | mỗi function ≥ 1 Normal + 1 Abnormal + 1 Boundary |
| F1, F2,... Indirect | mỗi function ≥ 1 TC verify không hỏng (`Normal`, Ghi chú = `regression`) |
| D1, D2,... | mỗi data ≥ 1 verify giá trị (`Normal`) + 1 `Boundary` (null/empty/max) + 1 `Abnormal` (invalid type, nếu áp dụng) |
| T1, T2,... High risk | mỗi feature ≥ 1 TC đi full happy path end-to-end (`Normal`, Ghi chú = `regression`) |
| T1, T2,... Medium/Low | mỗi feature ≥ 1 smoke test |
| Mỗi quan điểm ◯ ở Bước 2 | thỏa RULE-01 ở bảng 3a |

**3c — RULE-06 (output cuối chuỗi):** mọi TC có output ra ngoài (LINE app, mobile app, Google, payment gateway, file export, email) → Expected result **phải verify tại output cuối trên thiết bị/hộp thư thật**, KHÔNG dừng ở màn admin. TC dừng ở "màn hình hiển thị đúng" khi có output cuối chuỗi = TC thiếu.

**3d — RULE-07 (verify 3 tầng):** mọi TC CRUD → Expected phải khớp **3 nơi**: DB + màn hình + output/thông báo. Với UPDATE/DELETE: có TC tạo bản ghi **trùng tên ở 2 tài khoản** để kiểm chứng `WHERE` scope (`DATA-DB-001`).

#### 3e — Reuse TC cũ (chỉ khi Bước 1.4b lấy được TC cũ)

**Nguyên tắc**: TC cũ giữ nguyên 100% — AI KHÔNG sửa, KHÔNG override, KHÔNG ghi đè. Chỉ dùng TC cũ làm reference để tránh viết lặp.

Với mỗi ô yêu cầu tối thiểu trong bảng trên, check đối chiếu với TC cũ đã trích ở Bước 1.4b — so theo **ý định test**, KHÔNG so chuỗi ký tự (định nghĩa trùng ở 3f):

- **Đã cover đủ ở TC cũ** → KHÔNG sinh TC mới trùng. Track nội bộ: "F1 Normal: đã có ở sheet cũ TC<id>/<title>".
- **Đã cover một phần** (vd có Normal nhưng thiếu Abnormal) → chỉ sinh phần thiếu.
- **TC cũ không liên quan scope task** → bỏ qua, không động đến.
- **TC cũ có thể không còn đúng sau fix** (vd fix đổi validation behavior) → vẫn KHÔNG sửa TC cũ. Liệt kê vào danh sách cảnh báo "⚠️ TC cũ nghi sai sau fix" để output ở Bước 7 cho member tự verify thủ công.

Mục tiêu: bộ TC mới ở file 04 chỉ chứa **delta** (bug + impact mới chưa được cover ở TC cũ), KHÔNG chép lại regression suite cũ, KHÔNG override TC cũ.

#### 3f — Đối chiếu kho TCs + định nghĩa TC trùng (BẮT BUỘC, trước khi sinh TC)

**Định nghĩa TC trùng** — dùng chung với [`/review-tc` BƯỚC 4b](review-tc.md). 2 TC là trùng khi cùng bộ **4 yếu tố**, dù câu chữ khác nhau:

`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `điều kiện tiền đề tương đương` → cho ra `kết quả mong đợi` tương đương.

**Đọc kho TCs của tính năng** trong [kho-tcs/](../../kho-tcs/) trước khi viết:

1. **Tìm file kho**: `ls kho-tcs/*.md` → khớp mã màn hình `FA-xxx` của task (tra mã ở bảng feature [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md)). Tên file dạng `<mã>-<tên VN bỏ dấu>-<tên JP>.md`, VD `kho-tcs/fa012-quanlythe-タグ管理.md`.
   Kho **chưa có** tính năng này → ghi note ở Bước 7 ("kho-tcs chưa có `FA-xxx` — không đối chiếu được"), vẫn tiếp tục viết TC.
2. **Đọc có chọn lọc, KHÔNG nạp cả file vào context** (mỗi file 350–810 dòng):
   `grep -n "^## \|^### " <file>` lấy danh sách nhóm chức năng → `grep -n "<từ khoá chức năng bị ảnh hưởng>" <file>` → `sed -n` đọc đúng vùng đó.
3. Dùng kho trả lời **3 câu hỏi**:

   | Câu hỏi | Xử lý |
   |---|---|
   | **Phạm vi ảnh hưởng** — TC kho nào chạm cùng chức năng / cùng bảng dữ liệu với `F*`/`D*`/`T*` của task? | Nhóm TC kho đó là **vùng regression**. Chưa TC nào (mới lẫn cũ) cover → sinh TC regression, `Ghi chú` ghi `regression — dẫn từ <ID kho>`. |
   | **Conflict expected** — TC sắp viết có `Kết quả mong đợi` **mâu thuẫn** TC kho không? | **KHÔNG tự chọn bên.** Vẫn viết TC theo cách fix ở file 03, nhưng `Trạng thái đánh giá spec` = `Spec không ghi`, `Ghi chú` ghi `⚠️ conflict với <ID kho>: "<expected kho>"`, và đưa vào cảnh báo Bước 7 + note đầu file 04 để Leader/Dev chốt. |
   | **Đã có sẵn** — TC kho đã cover đúng ô yêu cầu này chưa? | Có → **KHÔNG viết TC mới trùng**; track nội bộ "đã có ở kho `<ID kho>`" và liệt kê ở Bước 7. |

   ⚠️ Kho dùng **12 cột riêng** (`ID` = `TC-<PREFIX>-<nn>`), KHÁC 16 cột canonical của file 04 → chỉ **dẫn chiếu ID + tên case**, KHÔNG copy nguyên dòng kho vào file 04.

### BƯỚC 4 — SINH TC THEO TEMPLATE
Output theo format `templates/04-tc-list.template.md` — bám **ĐÚNG sheet canonical "7. Ví dụ test case"** ([Bảng quan điểm test — HỢP NHẤT ELME v1.0](https://docs.google.com/spreadsheets/d/1IijLnq0gLZDFxOMWOYxXafz1Wnzv3W0g/edit?gid=1251796928#gid=1251796928)). Bảng TC có **16 cột**:

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |

Quy tắc:
- **TC No.**: `TC-<mã quan điểm bỏ dấu gạch>-<nn>`, đánh lại từ `01` cho **mỗi** quan điểm. VD `MSG-002` → `TC-MSG002-01/-02/-03`; `DATA-COUNT-001` → `TC-DATACOUNT001-01`. **KHÔNG** dùng TC001/TC002 nữa.
  - ⚠️ **Chế độ `APPEND`** (file 04 đã có TC — xem 1.4c): số thứ tự **tiếp nối** số lớn nhất của cùng mã quan điểm trong file đích, KHÔNG đánh lại từ `01`. VD file đã có `TC-MSG001-01/-02` → TC mới là `TC-MSG001-03`. Trùng `TC No.` với dòng đã có = lỗi, phải sửa trước khi ghi.
- **Mã quan điểm liên kết**: mã tầng 1 mà TC cụ thể hóa (VD `PERM-002`). **BẮT BUỘC** — đây là cột để Leader/`/review-tc` map coverage.
- **Loại case**: **CHỈ 3 giá trị** `Normal` / `Abnormal` / `Boundary`. **KHÔNG có Regression** — TC verify tính năng cũ không hỏng xếp vào `Normal` (luồng cũ chạy đúng) hoặc `Abnormal` (điều kiện lỗi cũ), và ghi chữ `regression` ở **Ghi chú**.
- **Tiêu đề test case**: mô tả MỤC ĐÍCH cụ thể + **chứa keyword** giúp Leader suy luận impact (tên function / DB table / màn hình). VD: "generateLinkInviteStaff: bot standard 10/10 → fail" → Leader nhận ra ngay map F1.
- **Điều kiện tiền đề**: account, data seed, feature flag, timezone — **đầy đủ**, người khác đọc dựng được env. Mỗi ý 1 dòng bắt đầu bằng `- `, dùng `<br>` xuống dòng.
- **Các bước thực hiện**: tuần tự, đánh số 1./2./3., dùng `<br>` để xuống dòng trong bảng.
- **Dữ liệu test/input**: giá trị input cụ thể + **phép tính tay** nếu TC có số đếm/tỷ lệ (VD `5 friend, 3 người mở` / `Phép tính tay: 3/5 = 60%`). Không "data dummy" — dùng giá trị nghiệp vụ hợp lý.
- **Kết quả mong đợi**: **đo lường được** — giá trị cụ thể, không "hiển thị đúng". VD: "Broadcast gửi đến 200 friends". Áp dụng **RULE-06** (đi tới output cuối chuỗi) + **RULE-07** (khớp DB + màn hình + output).
- **Kết quả thực thi**: **CHỈ** `Đạt` / `Không đạt` / `Chưa test`. Draft luôn ghi `Chưa test`.
- **Evidence thực tế**: **để trống** trong draft (QA paste link/ảnh sau khi test, BẮT BUỘC khi Đạt). *Loại* evidence bắt buộc của quan điểm (RULE-02) ghi ở **Ghi chú**.
- **Môi trường test**: `STAGING` (mặc định) / `DEV` / `PRODUCTION`. **RULE-08**: TC nhóm media / domain / job / loadbalance / bill tiền → ghi `PRODUCTION`.
- **Người thực hiện** / **Ngày thực hiện** / **Số ticket bug**: **để trống** trong draft. QA fill sau khi run.
- **Trạng thái đánh giá spec**: **CHỈ** `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. Spec không định nghĩa hành vi → chọn `Spec không ghi` + ghi rõ **đã hỏi ai** ở Ghi chú. **KHÔNG tự suy diễn rồi cho Đạt.**
- **Ghi chú**: loại evidence bắt buộc (RULE-02) · lý do nếu quan điểm Cao thiếu 1 trong 3 loại case (RULE-01) · cảnh báo escalate · đánh dấu `regression` · liên kết quan điểm khác.

Tỷ lệ gợi ý cho cả bộ TC: `Normal` ~40% / `Abnormal` ~35% / `Boundary` ~25% (điều chỉnh theo bản chất task — task phân quyền/validation thì Abnormal + Boundary sẽ nhiều hơn).

> **KHÔNG có cột Priority** — độ ưu tiên suy ra từ **ưu tiên của mã quan điểm** ở tầng 1, nên không lặp lại trong bảng.
>
> **KHÔNG có cột "Map to Impact"** — coverage map qua cột `Mã quan điểm liên kết` + keyword trong `Tiêu đề test case`. Track mapping impact (BUG/F/D/T) nội bộ để verify ở Bước 6, ghi vào **Ghi chú** nếu cần làm rõ, KHÔNG thêm cột mới.

### BƯỚC 5 — FILL CÁC SECTION KHÁC CỦA FILE 04
Theo template, ngoài bảng TC, file `04-tc-list.md` còn:
- **Thông tin** (Tester / ngày / version / link gốc): để placeholder `<member điền>` cho member tự fill, không bịa tên.
- **Member tự check** (Coverage check + Base checklist LME): tick các mục Claude đã đảm bảo, để trống các mục member cần verify thủ công.

### BƯỚC 6 — SELF-CHECK TRƯỚC KHI XUẤT
Trước khi ghi file, tự track mapping nội bộ (impact + quan điểm → TC nào cover) và verify:
- [ ] Mọi impact F/D/T trong `03-dev-impact.md` ĐỀU có ≥ 1 TC verify (không sót — kể cả từ TC mới HOẶC TC cũ đã cover)
- [ ] **Mọi quan điểm ◯ ưu tiên Cao có đủ 3 loại case** (`Normal` + `Abnormal` + `Boundary`) — thiếu 1 loại phải có lý do ghi ở cột `Ghi chú` (RULE-01)
- [ ] **Mọi TC có `Mã quan điểm liên kết`** và `TC No.` đúng format `TC-<mã quan điểm bỏ gạch>-<nn>`
- [ ] **Mọi TC có `Trạng thái đánh giá spec`**; case `Spec không ghi` đã ghi rõ **đã hỏi ai** ở `Ghi chú` (không tự suy diễn)
- [ ] **Mọi TC có `Kết quả thực thi` = `Chưa test`** và `Evidence thực tế` để trống trong draft
- [ ] **Mọi quan điểm đánh × đều có lý do** (RULE-03); × ở quan điểm Cao → đưa vào cảnh báo Bước 7
- [ ] **Mọi TC có output ra ngoài đều verify tới output cuối chuỗi** (LINE app / app / Google / gateway / file / mail) — RULE-06
- [ ] **Mọi TC CRUD verify đủ 3 tầng** (DB + màn hình + output); có TC kiểm `WHERE` scope trên 2 tài khoản nếu task có UPDATE/DELETE — RULE-07
- [ ] **Mọi TC đều có `Ghi chú` ghi loại evidence bắt buộc** (RULE-02)
- [ ] Mọi TC có Title/Steps đủ rõ để Leader suy luận impact (tên function / DB / feature có trong title)
- [ ] BUG có ít nhất 1 TC riêng (TC đó có từ "reproduce" hoặc tả đúng flow KH)
- [ ] Mỗi T trong 4.3 có ≥ 1 TC verify không hỏng (Ghi chú = `regression`)
- [ ] Mỗi D trong 4.2 có ≥ 1 `Abnormal` hoặc `Boundary`
- [ ] Catalog tương ứng mỗi quan điểm ◯ **đã được mở và duyệt hết** (Catalog C: duyệt hết khối, không lấy 1-2 dòng đại diện)
- [ ] KHÔNG có TC nào lạc chủ đề (mọi TC thuộc scope BUG / Fx / Dx / Tx hoặc 1 quan điểm ◯)
- [ ] **Rà trùng 4 chiều** theo **4 yếu tố** ở Bước 3f (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected` tương đương):
  - [ ] TC mới KHÔNG trùng **nhau** trong chính bộ vừa sinh — 2 ô yêu cầu dẫn tới cùng 1 TC thì gộp làm 1, `Ghi chú` ghi cả 2 lý do
  - [ ] **(chế độ `APPEND`)** TC mới KHÔNG trùng **TC đã có trong chính `04-tc-list.md`** (đọc ở 1.4c) — đây là chiều **dễ sót nhất** vì file đích thường chính là nguồn TC cũ; trùng thì bỏ, track "đã có ở file 04 `<TC No.>`"
  - [ ] TC mới KHÔNG trùng **TC cũ** đã cover (nguồn ở Bước 1.4b)
  - [ ] TC mới KHÔNG trùng **TC kho** `kho-tcs/` (Bước 3f) — trùng thì bỏ, track "đã có ở kho `<ID kho>`"
- [ ] **(chế độ `APPEND`)** Không `TC No.` nào của TC mới trùng `TC No.` đã có trong file đích; số thứ tự tiếp nối đúng theo từng mã quan điểm
- [ ] **(chế độ `APPEND`)** TC mới bám **đúng format bảng đang có** của file đích (16 cột canonical hay 10 cột cũ), không trộn 2 format
- [ ] KHÔNG có TC nào "override" / "sửa" / "ghi đè" TC cũ hoặc TC kho — đều là read-only
- [ ] TC có `Kết quả mong đợi` **mâu thuẫn TC kho** đã ghi `⚠️ conflict với <ID kho>` ở `Ghi chú` + đưa vào cảnh báo Bước 7 (không tự chọn bên)

Nếu fail bất kỳ mục nào → bổ sung TC hoặc đặt lại Title rõ hơn trước khi xuất.

### BƯỚC 7 — GHI FILE

Đích **luôn** là `<folder>/04-tc-list.md`. **KHÔNG BAO GIỜ ghi đè**, **KHÔNG** sinh `04-tc-list.draft.md` / `.studio.md` / `.sheet.md`. Chế độ đã xác định ở **1.4c**:

**Chế độ `CREATE`** (file chưa tồn tại) — ghi file mới đầy đủ theo `templates/04-tc-list.template.md`: dòng `sync-target` → heading → `Thông tin` → bảng TC → `Member tự check`.

**Chế độ `APPEND`** (file đã tồn tại) — chỉ **chèn thêm dòng** vào **cuối bảng TC hiện có**:
- Giữ nguyên **từng ký tự** của: dòng comment đầu file (`sync-tcs` / `source` / `sync-target`), heading, mọi dòng TC cũ, section `Thông tin`, section `Member tự check`.
- Chèn **ngay trước dòng trống kết thúc bảng** một dòng đánh dấu rồi tới các dòng TC mới:
  ```
  <!-- +++ bổ sung YYYY-MM-DD by /write-tc — <n> TC · lấp: <danh sách impact/quan điểm> +++ -->
  ```
- Mỗi dòng TC mới ghi thêm ở cột `Ghi chú`: `bổ sung YYYY-MM-DD by /write-tc`.
- **Không có TC nào cần bổ sung** (mọi ô yêu cầu ở Bước 3 đã được TC sẵn có / TC cũ / TC kho cover) → **KHÔNG ghi file**, in: "Không có TC nào cần bổ sung — `04-tc-list.md` giữ nguyên `<n>` TC. Chi tiết ô yêu cầu nào đã được cover bởi TC nào: ...".
- File đích dùng **10 cột cũ** (task trước 2026-07-16) → TC append viết **đúng 10 cột đó**, KHÔNG convert file sang 16 cột, KHÔNG trộn 2 format trong 1 bảng. Ghi cảnh báo `[NIT]` ở tóm tắt.

**Sync target metadata** (dùng `sync_url` lưu ở Bước 1.4a): chèn HTML comment ở **dòng đầu tiên** của file 04 (trước cả heading), đúng 1 dòng:
```
<!-- sync-target: <sync_url đầy đủ có gid> -->
```
Vd: `<!-- sync-target: https://docs.google.com/spreadsheets/d/1z8QfSl.../edit?gid=2004892297 -->`

- Chế độ `CREATE` → **bắt buộc** chèn dòng này.
- Chế độ `APPEND` → file đã có dòng `sync-target` rồi thì **giữ nguyên, không sửa, không thêm dòng thứ hai**. `sync_url` mới khác `sync-target` đang có → **KHÔNG tự đổi**, in cảnh báo hỏi human chốt đích push.
- Chế độ `APPEND` mà file **chưa** có `sync-target` (VD file do `/new-task` ghi, chỉ có `sync-tcs` + `source`) → chèn `sync-target` vào **dòng đầu**, đẩy các comment cũ xuống, không xoá dòng nào.

`/sync-tc` (qua `scripts/push_tc.py`) sẽ đọc comment này, parse `spreadsheet_id` + `gid`, lookup tab tương ứng, và APPEND TCs vào row trống đầu tiên trong tab đó. **Không tạo tab mới.**

Sau khi ghi, in tóm tắt:
- **Chế độ ghi**: `CREATE` (file mới) hoặc `APPEND` (`<n>` TC đã có → `+<m>` TC bổ sung → tổng `<n+m>`); hoặc `KHÔNG GHI` (không có TC nào cần bổ sung)
- Tổng số TC sinh ra
- Phân bố theo `Loại case` (Normal / Abnormal / Boundary) + số TC có Ghi chú `regression`
- **Bảng quan điểm đã duyệt**: `<mã> ◯/× | ưu tiên | # TC | catalog đã mở` — liệt kê **đầy đủ quan điểm ◯**, và **các quan điểm × ở mức Cao kèm lý do** (Leader cần duyệt lý do này theo RULE-03)
- Internal coverage track (BUG / F* / D* / T* — Claude tự note để Leader verify, KHÔNG ghi vào file)
- **Nguồn TC cũ đã dùng** (Studio task #<id> / Sheet `<tab>` / file 04 sẵn có / không có) + vì sao không dùng nguồn ưu tiên cao hơn
- (Nếu có TC cũ) Số TC cũ **đã reuse** (không sinh trùng) — list ngắn gọn theo `<id/title TC cũ> → reuse|skip(out-of-scope)`
- **Đối chiếu kho TCs**: file kho đã đọc (hoặc "kho chưa có `FA-xxx`") · vùng regression phát hiện từ kho · TC kho đã dùng lại thay vì viết mới (`<ID kho>`) · conflict expected vs kho
- **Nguồn spec đã dùng** cho hành vi đúng: `spec-features/<feature>` / spec ngoài human đưa / **không có nguồn nào**
- Sync target: `<sync_url>` đã ghi vào HTML comment.
- Cảnh báo (nếu có):
  - "Input thiếu..."
  - "Spec không rõ về..."
  - "TC cũ fetch lỗi..." (ghi rõ nguồn nào lỗi vì lý do gì)
  - "⚠️ TC cũ nghi sai sau fix: <list id> — member tự verify thủ công" (TC cũ giữ nguyên, không sửa)
  - "⚠️ Task #<id> đã có <n> TC trên Studio — cân nhắc `/review-tc` thay vì viết mới"
  - "⚠️ Conflict expected với kho TCs: <TC mới> vs <ID kho> — cần Leader/Dev chốt hành vi đúng"
  - "⚠️ Không tìm được spec trong `spec-features/` cho <chức năng> — TCs ghi `Spec không ghi`, member phải hỏi trước khi kết luận Đạt"

### QUY TẮC QUAN TRỌNG
- KHÔNG bịa impact / spec / business rule — chỉ dùng nội dung trong file input + spec đọc ở `spec-features/` (Bước 1).
- **TC cũ và TC kho là read-only** — KHÔNG sửa, KHÔNG override expected dù bug fix đổi behavior; nghi sai thì cảnh báo ở Bước 7.
- **`04-tc-list.md` chỉ được THÊM, không được ĐÈ và không được SỬA dòng cũ** — kể cả khi TC cũ trong file nghi sai sau fix. Nghi sai → ghi cảnh báo ở Bước 7 cho member tự xử lý. `/write-tc` **không sinh file `04-*` nào khác**; file tham chiếu (nếu cần) ghi ra scratchpad.
- **Dừng ở nguồn TC cũ đầu tiên có kết quả** (Bước 1.4b) — không gộp TC từ 2 nguồn, không đối chiếu chéo.
- **Không tự chọn bên khi expected mâu thuẫn** (TC mới vs TC kho / TC cũ) — viết theo cách fix, đánh dấu conflict, đẩy lên Leader/Dev.
- KHÔNG bịa tên member, ngày submit, link Sheet — để placeholder.
- Steps phải **realistic** — precondition tạo được trong môi trường test thật. Tránh "data dummy", dùng giá trị nghiệp vụ hợp lý (VD: tag tên "VIP" thay vì "test").
- Nếu spec cũ (mục 02) mâu thuẫn với cách fix (mục 03) → ghi note ở đầu file 04: "⚠️ Spec conflict: ... — cần Leader confirm trước khi finalize TC".
- Output là **DRAFT cho member verify**, không phải final. Member phải đọc lại từng TC, điều chỉnh data, rồi mới submit cho Leader.

Bắt đầu bằng việc liệt kê file input có trong folder, xác nhận đầy đủ tiền điều kiện, hỏi `sync_url` (1.4a) → lấy TC cũ theo 3 nguồn ưu tiên (1.4b) → **đọc file đích `04-tc-list.md` để chốt chế độ `CREATE`/`APPEND` (1.4c)**, rồi thực hiện tuần tự 7 bước.
