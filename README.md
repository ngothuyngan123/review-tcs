# LME - Review TCs Project

Project hỗ trợ **Test Leader / QA member** viết + review Test Cases (TCs) cho LME bug fix task, dựa trên **4 input chuẩn hóa**:

1. **Nội dung bug task** — từ Redmine (AI auto-fill qua **REST API**, `scripts/redmine_fetch.py`) hoặc paste tay vào `01-bug-task.md`
2. **Đánh giá ảnh hưởng từ Dev** → `03-dev-impact.md`
3. **TCs cũ** tham chiếu (optional) — link Google Sheet (`?gid=` tab cụ thể) đã share edit cho service account → AI fetch read-only qua MCP google-sheets để tránh viết trùng
4. **Bộ quan điểm test của dự án (2 tầng, auto-load)** → [framework/checklist-lme.md](framework/checklist-lme.md) (tầng 1 — 80 quan điểm / 18 nhóm + 12 RULE) + [framework/catalog-lme.md](framework/catalog-lme.md) (tầng 2 — input / UI / bản đồ LME / môi trường / media)

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
│   └── 05-review-report.template.md   # Template report review của Leader
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
│   ├── redmine_fetch.py               # Fetch issue Redmine qua REST API (thay MCP redmine)
│   └── ...                            # push_tc / fetch_grid / parse_studio_tcs / build_indexes ...
├── framework/
│   ├── review-checklist.md            # Rubric cho Leader review TAY (skill KHÔNG đọc)
│   ├── checklist-lme.index.md         # ★ Index tự sinh — ĐỌC THAY cho checklist-lme.md
│   ├── catalog-lme.index.md           # ★ Index tự sinh — ĐỌC THAY cho catalog-lme.md
│   ├── checklist-lme.md               # ★ Tầng 1 — 80 quan điểm test LME + 12 RULE
│   ├── catalog-lme.md                 # ★ Tầng 2 — catalog A/B/C/D/D2/E (tri thức miền)
│   ├── coverage-matrix.md             # Ma trận coverage (impact ↔ TC)
│   ├── anti-patterns.md               # 6 anti-pattern khi viết TC
│   └── severity-levels.md             # Phân loại mức độ issue khi review
├── .claude/commands/                  # Slash commands cho Claude Code
│   ├── new-task.md                    # /new-task — Fetch Redmine → tạo folder + auto-fill 01/03/(04)
│   ├── review-tc.md                   # /review-tc — Leader review TCs
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
└── examples/
    └── sample-review/                 # Ví dụ mẫu đầy đủ
```

### File quan trọng: [LME-SYSTEM-SPEC.md](templates/LME-SYSTEM-SPEC.md)

Tham chiếu spec tổng thể của hệ thống LME — tổng hợp 38 tính năng, shared components, BG jobs, external integrations, glossary JP↔VI. **Thay vì mỗi lần review phải tự trích spec**, member chỉ cần link đến section tương ứng trong file này. Xem §9 của file đó để biết cách dùng.

---

## 3. Workflow

Workflow chia làm **2 phase tách biệt**: chuẩn bị input → chọn skill review/write. Mỗi skill độc lập, **chỉ chạy khi human gõ slash**, KHÔNG tự chain.

### Phase 1 — Chuẩn bị input

**Cách A (có Redmine URL — khuyên dùng):** chạy `/new-task <redmine-url>`.
- AI chạy `python scripts/redmine_fetch.py <url>` (Redmine REST API, API key trong `.env`) + (option) MCP google-sheets, tạo folder `tasks/YYYY-MM-DD_<id>_<slug>/`, auto-fill:
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
- **`/review-tc <folder> [ticket_id|task:<n>|<link Sheet>]`** — AI tự lấy bộ TC theo **3 nguồn ưu tiên, dừng ở nguồn đầu tiên có TC**: **MCP LME TEST STUDIO** → **link Google Sheet human cung cấp** → file `04-tc-list.md`; cả 3 không có → DỪNG hỏi human. Rồi đọc 01 + 03 + spec và sinh draft `05-review-report.md` **rút gọn — chỉ ghi phần thiếu**: §1 coverage GAP theo 2 chiều (đánh giá ảnh hưởng Dev + diff code) · §2 quan điểm test còn thiếu · §3 TC trùng lặp · §4 issues · §5 TC bổ sung. Chiều `diff code` lấy thẳng từ tab Thông tin của Studio (`dev_impact` + `spec_delta`). Bảng coverage / bảng quan điểm vẫn chạy nhưng là nháp nội bộ, không ghi vào file. Leader verify + chỉnh. Xem [prompts/review-tc-prompt.md](prompts/review-tc-prompt.md).

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
/new-task https://redmine.lme.jp/issues/12345
```

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

Gõ slash command **không kèm folder** → Claude sẽ liệt kê các folder con trong `tasks/` để bạn chọn (trừ `/new-task` — cần URL Redmine bắt buộc).

Định nghĩa command nằm ở [.claude/commands/](.claude/commands/), tài liệu hướng dẫn ở [prompts/](prompts/).
