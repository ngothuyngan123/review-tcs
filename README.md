# LME - Review TCs Project

Project hỗ trợ **Test Leader / QA member** viết + review Test Cases (TCs) cho LME bug fix task, dựa trên **4 input chuẩn hóa**:

1. **Nội dung bug task** — từ Redmine (AI auto-fill qua **REST API**, `scripts/redmine_fetch.py`) hoặc paste tay vào `01-bug-task.md`
2. **Đánh giá ảnh hưởng từ Dev** → `03-dev-impact.md`
3. **TCs cũ** tham chiếu (optional) — link Google Sheet (`?gid=` tab cụ thể) đã share edit cho service account → AI fetch read-only qua MCP google-sheets để tránh viết trùng
4. **Bộ quan điểm test của dự án (2 tầng, auto-load)** → [framework/checklist-lme.md](framework/checklist-lme.md) (tầng 1 — 81 quan điểm / 18 nhóm + 13 RULE) + [framework/catalog-lme.md](framework/catalog-lme.md) (tầng 2 — input / UI / bản đồ LME / môi trường / media)

---

## 1. Mục tiêu

- Chuẩn hóa quy trình review TCs fix bug, đảm bảo TCs:
  - **Cover đủ** root cause và cách fix của Dev
  - **Cover đủ** các function/data/tính năng bị ảnh hưởng
  - **Không thừa** case không liên quan, **không thiếu** case regression
  - **Phù hợp** với spec hiện tại (không conflict, có update spec nếu cần)
- Tạo output report review rõ ràng, có thể feedback trực tiếp cho member.

---

## 2. Cấu trúc thư mục

```
lme-review-TCs/
├── README.md                          # File này
├── templates/                         # Template chuẩn cho input/output
│   ├── LME-SYSTEM-SPEC.md             # ★ Tham chiếu spec tổng thể LME (38 features)
│   ├── 01-bug-task.template.md        # Template nội dung bug task
│   ├── 03-dev-impact.template.md      # Template đánh giá ảnh hưởng từ Dev
│   ├── 04-tc-list.template.md         # Template TCs do member viết
│   ├── 05-review-report.template.md   # Template report review của Leader
│   ├── 02-mcp-docs-review.template.md # Task MCP — review docs MCP (/review-docs-mcp)
│   └── 05-mcp-review-report.template.md # Task MCP — report review TC (/review-tc-mcp)
├── spec-features/                     # Spec đầy đủ (reverse-engineer) của từng feature
│   ├── index.md
│   ├── admin/<feature>/feature-spec.md
│   └── ...
├── .mcp.json                          # Config MCP Google Sheets (service account)
├── .gitignore                         # Block credentials/*.json
├── credentials/                       # Nơi drop service account JSON (gitignored)
├── docs/
│   ├── MCP-SETUP.md                   # Hướng dẫn setup service account + share sheet
│   └── REDMINE-SETUP.md               # Hướng dẫn setup Redmine REST API (API key trong .env)
├── .env.example                       # Mẫu REDMINE_URL + REDMINE_API_KEY (copy thành .env, gitignored)
├── scripts/
│   ├── redmine_fetch.py               # Fetch issue Redmine qua REST API (+ --download-attachments cho file đính kèm)
│   └── ...                            # push_tc / fetch_grid / parse_studio_tcs / build_indexes ...
├── framework/
│   ├── review-checklist.md            # Rubric cho Leader review TAY (skill KHÔNG đọc)
│   ├── checklist-lme.index.md         # ★ Index tự sinh — ĐỌC THAY cho checklist-lme.md
│   ├── catalog-lme.index.md           # ★ Index tự sinh — ĐỌC THAY cho catalog-lme.md
│   ├── checklist-lme.md               # ★ Tầng 1 — 81 quan điểm test LME + 13 RULE
│   ├── catalog-lme.md                 # ★ Tầng 2 — catalog A/B/C/D/D2/E (tri thức miền)
│   ├── coverage-matrix.md             # Ma trận coverage (impact ↔ TC)
│   ├── anti-patterns.md               # 6 anti-pattern khi viết TC
│   ├── mcp-rules.md                   # ★ Task MCP — 8 rule bắt buộc (bot A↔B, staff, limit Free, trùng tên, E2E prompt…)
│   └── severity-levels.md             # Phân loại mức độ issue khi review
├── .claude/commands/                  # Slash commands cho Claude Code
│   ├── new-task.md                    # /new-task — Fetch Redmine → tạo folder + auto-fill 01/03/(04)
│   ├── review-tc.md                   # /review-tc — Leader review TCs
│   ├── new-task-mcp.md                # /new-task-mcp — như /new-task, folder trong MCP/ + tải docs MCP
│   ├── review-docs-mcp.md             # /review-docs-mcp — review docs MCP vs spec → report cho Leader đọc
│   ├── write-tc-mcp.md                # /write-tc-mcp — viết TC MCP vào 04-tc-write.md (push Studio khi được yêu cầu)
│   ├── review-tc-mcp.md               # /review-tc-mcp — review TC MCP (tool × param + rule MCP + E2E prompt)
│   ├── write-tc.md                    # /write-tc — Member sinh draft TCs
│   └── sync-tc.md                     # /sync-tc — Push TCs lên Google Sheet master
├── prompts/                           # Tài liệu hướng dẫn dùng slash commands
│   ├── review-tc-prompt.md
│   └── write-tc-prompt.md
├── tasks/                           # Mỗi bug = 1 folder review
│   └── YYYY-MM-DD_<bug-id>_<slug>/
│       ├── 01-bug-task.md
│       ├── 03-dev-impact.md
│       ├── 04-tc-list.md
│       └── 05-review-report.md
├── MCP/                             # Task test MCP tool (từ 2026-10-14) — 1 task = 1 folder
│   └── YYYY-MM-DD_<id>_<slug>/
│       ├── 01-bug-task.md · 03-dev-impact.md
│       ├── 04-tc-list.md              # TC sync từ test tool về (không push lại)
│       ├── 04-tc-write.md             # /write-tc-mcp — TC AI viết (push khi human yêu cầu)
│       ├── 02-mcp-docs-review.md      # /review-docs-mcp — report docs cho Leader đọc (không lệnh nào đọc)
│       ├── 05-review-report.md        # /review-tc-mcp
│       └── _tool-inventory.md         # /review-docs-mcp — tool × param (docs nguồn ở spec-features/mcp/docs/)
└── examples/
    └── sample-review/                 # Ví dụ mẫu đầy đủ
```

### File quan trọng: [LME-SYSTEM-SPEC.md](templates/LME-SYSTEM-SPEC.md)

Tham chiếu spec tổng thể của hệ thống LME — tổng hợp 38 tính năng, shared components, BG jobs, external integrations, glossary JP↔VI. **Thay vì mỗi lần review phải tự trích spec**, member chỉ cần link đến section tương ứng trong file này. Xem §9 của file đó để biết cách dùng.

---

## 3. Workflow

Workflow chia làm **2 phase tách biệt**: chuẩn bị input → chọn skill review/write. Mỗi skill độc lập, **chỉ chạy khi human gõ slash**, KHÔNG tự chain.

### Phase 1 — Chuẩn bị input

**Cách A (có ticket Redmine — khuyên dùng):** chạy `/new-task <redmine-id>` — chỉ cần **ID** (vd `/new-task 40539`), URL đầy đủ vẫn nhận.
- AI chạy `python scripts/redmine_fetch.py <id|url>` (Redmine REST API, API key trong `.env`) + (option) MCP google-sheets, tạo folder `tasks/YYYY-MM-DD_<id>_<slug>/`, auto-fill:
  - `01-bug-task.md` ← Section "Tái hiện bug" (nếu Redmine có) + mô tả bug **dịch sang tiếng Việt** + Dữ liệu định danh ca lỗi + Journal Redmine.
  - `03-dev-impact.md` ← Section "Đánh giá ảnh hưởng phía dev" (BẮT BUỘC trong Redmine).
  - `04-tc-list.md` ← Section "Link TCs" + `Row: <start>-<end>` (OPTIONAL — fetch từ Google Sheet nếu Redmine có ghi).
- AI **DỪNG** sau khi xong. Setup: [docs/REDMINE-SETUP.md](docs/REDMINE-SETUP.md) + [docs/MCP-SETUP.md](docs/MCP-SETUP.md).
- Tester **bắt buộc verify** lại nội dung auto-fill trước khi sang Phase 2: đọc lại 01 đối chiếu Redmine, và tick checkbox "Tester verify auto-fill chính xác" ở 03 (file 01 rút gọn không còn checkbox này).

**Cách B (không có Redmine):** copy [examples/sample-review/](examples/sample-review/) vào `tasks/YYYY-MM-DD_<bug-id>_<slug>/`, paste tay:
- `01-bug-task.md` — paste nội dung task bug (mô tả dịch tiếng Việt, bỏ khối 原文 JP).
- `03-dev-impact.md` — paste đánh giá Dev (format 4 mục).
- `04-tc-list.md` (option) — TCs cũ nếu đã có.

### Phase 2 — Chọn skill (human gọi, KHÔNG tự chain)

Tùy theo task hiện tại có sẵn TCs hay chưa, chọn 1 trong 3:

- **`/write-tc <folder>`** — chưa có TCs hoặc cần bổ sung → AI đọc 01 + 03 + (option) 02 + (option) Old TCs Sheet → sinh draft `04-tc-list.md`. Member verify + chỉnh rồi submit cho Leader. Xem [prompts/write-tc-prompt.md](prompts/write-tc-prompt.md).
- **`/sync-tc <folder>`** — sau khi có 04 (do `/write-tc` sinh ra hoặc paste tay) → push lên Google Sheet master (mỗi task = 1 tab pre-created). Xem [docs/SYNC-TC-SETUP.md](docs/SYNC-TC-SETUP.md).
- **`/review-tc <folder> [ticket_id|task:<n>|<link Sheet>]`** — AI tự lấy bộ TC theo **3 nguồn ưu tiên, dừng ở nguồn đầu tiên có TC**: **MCP LME TEST STUDIO** → **link Google Sheet human cung cấp** → file `04-tc-list.md`; cả 3 không có → DỪNG hỏi human. Rồi đọc 01 + 03 + spec và sinh draft `05-review-report.md` **rút gọn — chỉ ghi phần thiếu**, **9 section**: §1 coverage **2 chiều kèm 2 dòng trả lời ĐỦ / CHƯA ĐỦ** (đánh giá ảnh hưởng Dev + diff code) · §2 quan điểm test còn thiếu · §3 TC trùng lặp · §4 **mâu thuẫn** (TC vs TC / vs `spec-features/` / vs `kho-tcs/`) · §5 issues khác · §6 **TC thừa / ngoài phạm vi task** · §7 TC bổ sung (GAP + quan điểm + regression AI đánh giá) · §8 spec update needed. Chiều `diff code` lấy thẳng từ tab Thông tin của Studio (`dev_impact` + `spec_delta`). Bảng coverage / bảng quan điểm vẫn chạy nhưng là nháp nội bộ, không ghi vào file. Leader verify + chỉnh. Xem [prompts/review-tc-prompt.md](prompts/review-tc-prompt.md).

### Luồng riêng cho task MCP (test MCP tool)

Task MCP **không** đi `/new-task` → `/review-tc`, mà đi luồng riêng, folder nằm trong `MCP/`. Docs MCP **không** tải về task — đọc chung ở `spec-features/mcp/docs/` (human cấp, 1 file / tính năng); thiếu docs tính năng → các lệnh review/write DỪNG, nhắc human add:

1. **`/new-task-mcp <id>`** — như `/new-task`, nhưng tạo folder `MCP/YYYY-MM-DD_<id>_<slug>/` và **lấy TC về `04-tc-list.md`** (Studio/Sheet). Không tải docs; chỉ cảnh báo nếu `spec-features/mcp/docs/` thiếu docs tính năng.

Sau đó rẽ 2 nhánh:

- **Studio/Sheet đã có TC** (file 04 có sẵn) → **`/review-tc-mcp <folder>`** — kiểm docs tính năng ở `spec-features/mcp/docs/` (thiếu → DỪNG), **đọc TC ở `04-tc-list.md`** (không fetch lại), review 2 hướng: **bám docs** (ma trận tool × param + 7 rule ở [framework/mcp-rules.md](framework/mcp-rules.md), có bước `get_*` verify sau khi tạo/sửa) + **E2E prompt** (ngôn ngữ tự nhiên qua ChatGPT/Claude — VN chính, JP đại diện; prompt chi tiết + chung) → `05-review-report.md` → `/sync-review-tc` push TC bổ sung (push xong tự refresh `04-tc-list.md` để lần review sau đọc được). **Không cần file 02.**
- **Studio chưa có TC** (phải viết mới) → **`/write-tc-mcp <folder>`** — kiểm docs tính năng ở `spec-features/mcp/docs/` (thiếu → DỪNG), đọc TC cũ ở `04-tc-list.md` để chống trùng, viết TC 2 hướng (bám docs + E2E prompt) vào file riêng `04-tc-write.md`; `/write-tc-mcp <folder> push` để đẩy lên Studio (luôn hỏi xác nhận) + tự refresh `04-tc-list.md`. Rồi `/review-tc-mcp`. `04-tc-list.md` chỉ chứa TC sync từ test tool về, không bao giờ push lại.

**`/review-docs-mcp <folder>`** (tuỳ chọn, dùng ở nhánh nào cũng được) — lập inventory tool × param (từ docs ở `spec-features/mcp/docs/`), rà docs **mâu thuẫn nội tại** · **trái `spec-features/`** · **thiếu so với spec** (kể cả 4 rule bắt buộc: bot A↔B, staff không quyền, limit bot Free, trùng tên quản lý) → `02-mcp-docs-review.md` = **report cho Leader đọc**. Không lệnh nào gate / đọc file 02; docs sai / thiếu thì Leader yêu cầu cập nhật docs ở `spec-features/mcp/docs/`.

Task chỉ gọi tới MCP như caller (vd filter dùng chung web / app / MCP) vẫn là task thường ở `tasks/`.

### Phase 3 — Gửi feedback (chỉ khi `/review-tc`)
Chia sẻ `05-review-report.md` cho member. Member fix TCs → review vòng 2 nếu cần.

---

## 4. Quy tắc vàng khi review

1. **Mọi impact Dev list ra ở mục 4.1/4.2/4.3 PHẢI có ít nhất 1 TC verify** — nếu không có, đó là **gap**. (File 04 không có cột Map to Impact; Leader/Claude suy luận từ Title/Steps/Expected của TC.)
2. **Mọi TC PHẢI thuộc scope** bug root cause / cách fix / 1 impact trong mục 4 / 1 quan điểm ◯ — nếu không, đó là **case thừa** hoặc **case lạc chủ đề**.
3. **Luôn có regression test** cho các tính năng ở mục 4.3.
4. **Luôn có ít nhất 1 negative/boundary case** cho data ở mục 4.2.
5. Nếu spec cũ mâu thuẫn với cách fix → **flag update spec** trong report.
6. **Mọi quan điểm có Trigger khớp task PHẢI có TC** — quan điểm ưu tiên **Cao** thiếu TC = `[BLOCKER]`. Quan điểm Cao có TC nhưng **thiếu 1 trong 3 loại case** (Normal/Abnormal/Boundary) mà không ghi lý do = `[MAJOR]` (**RULE-01**).
7. **Không dừng ở màn admin** — TC có output ra ngoài (LINE app / mobile app / Google / payment gateway / file export / email) phải verify tại **output cuối trên thiết bị hoặc hộp thư thật** (**RULE-06**). TC CRUD phải khớp **3 tầng**: DB + màn hình + output (**RULE-07**).

> **Title TC phải chứa keyword** giúp suy luận impact (tên function / DB table / màn hình). Title kiểu "test feature A" sẽ bị flag [MAJOR] vì Leader không suy luận được TC cover impact nào.
>
> **Quy trình 2 tầng**: đọc quan điểm ở [tầng 1](framework/checklist-lme.md) → mở đúng catalog ở [tầng 2](framework/catalog-lme.md) để lấy dữ liệu và vị trí cụ thể. **Bỏ bước hai là chỗ bug lọt.**

---

## 5. Sử dụng nhanh với Claude (slash commands)

Trong Claude Code (mở ở thư mục project root), gõ:

```
/new-task 40539
```

(ID thuần — base URL lấy từ `REDMINE_URL` trong `.env`. Gõ `/new-task` rồi enter, dán ID ở dòng dưới cũng được. Cần ticket ở Redmine khác → paste URL đầy đủ `https://<redmine>/issues/40539`.)

→ Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`), tạo folder `tasks/<YYYY-MM-DD>_<id>_<slug>/`, auto-fill `01-bug-task.md` + `03-dev-impact.md` + (option) `04-tc-list.md` từ Section "Link TCs" trong Redmine. Sau đó **DỪNG** — tester verify lại nội dung (tick checkbox ở file 03) trước khi sang skill tiếp theo.

```
/write-tc tasks/2026-04-23_LME-2054_broadcast-cache/
```

→ Claude đọc 01 + 02 (nếu có) + 03 + (option) fetch TC cũ qua MCP google-sheets → sinh draft `04-tc-list.md`. **Không liên quan Redmine** — input phải đã được chuẩn bị từ trước (qua `/new-task` hoặc paste tay).

```
/sync-tc tasks/2026-04-23_LME-2054_broadcast-cache/
```

→ Push `04-tc-list.md` lên Google Sheet master (append vào tab pre-created qua URL có gid). **Cần setup lần đầu:** xem [docs/SYNC-TC-SETUP.md](docs/SYNC-TC-SETUP.md).

```
/review-tc tasks/2026-04-23_LME-2054_broadcast-cache/
```

→ Claude tự lấy bộ TC (Studio → link Sheet bạn đưa → file 04), đọc `01` + `03` + spec, rồi sinh draft `05-review-report.md` (rút gọn: nguồn + số TC · GAP coverage 2 chiều dev-impact/diff code · quan điểm thiếu · TC trùng · issues · TC bổ sung). **Không tự fetch Redmine** (việc của `/new-task`), **không tự viết TC** (việc của `/write-tc`).

```
/new-task-mcp 39446
/review-docs-mcp MCP/2026-10-14_39446_mcp-tinh-nang-tao-formanswer/        # tuỳ chọn — report docs cho Leader đọc
/write-tc-mcp    MCP/2026-10-14_39446_mcp-tinh-nang-tao-formanswer/        # khi Studio chưa có TC
/write-tc-mcp    MCP/2026-10-14_39446_mcp-tinh-nang-tao-formanswer/ push   # đẩy 04-tc-write.md lên Studio + refresh 04-tc-list.md
/review-tc-mcp   MCP/2026-10-14_39446_mcp-tinh-nang-tao-formanswer/
```

→ Luồng task MCP (xem §3 "Luồng riêng cho task MCP"). `/write-tc-mcp` và `/review-tc-mcp` bám thẳng docs ở `spec-features/mcp/docs/`, **không cần** `02-mcp-docs-review.md`.

Gõ slash command **không kèm folder** → Claude sẽ liệt kê các folder con trong `tasks/` (lệnh MCP: `MCP/`) để bạn chọn (trừ `/new-task` / `/new-task-mcp` — cần ID ticket Redmine bắt buộc).

Định nghĩa command nằm ở [.claude/commands/](.claude/commands/), tài liệu hướng dẫn ở [prompts/](prompts/).
