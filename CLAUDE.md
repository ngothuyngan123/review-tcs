# CLAUDE.md

Hướng dẫn Claude khi làm việc trong repo này. Đọc file này TRƯỚC khi thực hiện bất kỳ task nào.

## Bản chất project

Đây **KHÔNG phải codebase ứng dụng**. Đây là **framework tài liệu + workflow** để Test Leader review Test Cases (TCs) do member viết cho hệ thống LME (LINE Marketing Engine). Claude là tác nhân chính trong workflow review — xem [prompts/review-tc-prompt.md](prompts/review-tc-prompt.md).

Tổng quan workflow + cấu trúc thư mục đầy đủ: [README.md](README.md).

## Ngôn ngữ

- **Mặc định trả lời, viết report, comment bằng tiếng Việt.**
- Khi đọc spec gốc (LME-SYSTEM-SPEC, sheet checklist) có thuật ngữ tiếng Nhật — giữ nguyên thuật ngữ JP, có thể chú thích VN trong ngoặc.

## File canonical — luôn ưu tiên đọc

Trước khi suy luận hoặc tự viết, kiểm tra các file sau (theo thứ tự ưu tiên):

0. [.claude/commands/new-task.md](.claude/commands/new-task.md) — slash command `/new-task <redmine-url>`. **Bước CHUẨN BỊ INPUT** (KHÔNG phải skill review/write): fetch Redmine → tạo folder `tasks/<YYYY-MM-DD>_<id>_<slug>/` + auto-fill `01-bug-task.md` (từ Section "Tái hiện bug") + `03-dev-impact.md` (từ Section "Đánh giá ảnh hưởng") + `04-tc-list.md` (từ Section "Link TCs" + `Row: <start>-<end>` nếu Redmine có). DỪNG sau khi xong — KHÔNG tự chain `/write-tc` hoặc `/review-tc`.
1. [.claude/commands/review-tc.md](.claude/commands/review-tc.md) — slash command `/review-tc <folder>`. Quy trình review 6 bước cho Test Leader. **Operating instruction** khi user invoke `/review-tc` hoặc nhận task review TC. KHÔNG tự fetch Redmine — chỉ đọc folder.
2. [.claude/commands/write-tc.md](.claude/commands/write-tc.md) — slash command `/write-tc <folder>`. Quy trình 7 bước sinh `04-tc-list.md` từ bug + dev-impact + (option) TC cũ Sheet. **KHÔNG liên quan Redmine** — input (file 01 + 03) phải đã chuẩn bị từ trước (qua `/new-task` hoặc paste tay).
3. [.claude/commands/sync-tc.md](.claude/commands/sync-tc.md) — slash command `/sync-tc <folder>`. Push `04-tc-list.md` lên Google Sheet master. Wrapper cho `scripts/push_tc.py`. Setup: [docs/SYNC-TC-SETUP.md](docs/SYNC-TC-SETUP.md).
4. [framework/review-checklist.md](framework/review-checklist.md) — checklist tổng quát (A/B/C/D/E/F).
5. [framework/checklist-lme.md](framework/checklist-lme.md) — checklist riêng LME, **bắt buộc base** với mọi task LME.
6. [framework/coverage-matrix.md](framework/coverage-matrix.md) — format ma trận coverage.
7. [framework/severity-levels.md](framework/severity-levels.md) — định nghĩa severity.
8. [templates/LME-SYSTEM-SPEC.md](templates/LME-SYSTEM-SPEC.md) — spec tổng 38 features. **Tham chiếu section thay vì copy spec** vào file review.
9. [templates/](templates/) — 5 template `01` → `05`. Mọi file trong `tasks/<bug>/` phải bám đúng template.
10. [examples/sample-review/](examples/sample-review/) — ví dụ mẫu đầy đủ.
11. [docs/REDMINE-SETUP.md](docs/REDMINE-SETUP.md) — setup MCP Redmine để `/new-task` auto-fill `01-bug-task.md` + `03-dev-impact.md` (+ `04-tc-list.md` nếu có Link TCs) từ Redmine issue.
12. [docs/MCP-SETUP.md](docs/MCP-SETUP.md) — setup MCP Google Sheets (service account) để fetch TC cũ + push TC mới.

## Quy ước bắt buộc

### Tag impact (từ `03-dev-impact.md`)
- `F1, F2, ...` — function impact (mục 4.1)
- `D1, D2, ...` — data impact (mục 4.2)
- `T1, T2, ...` — feature impact (mục 4.3)
- `BUG` — root cause / cách fix

### Severity (dùng trong report)
`[BLOCKER]` / `[MAJOR]` / `[MINOR]` / `[NIT]` — định nghĩa ở [framework/severity-levels.md](framework/severity-levels.md).

### Coverage status
`OK` (đủ chiều) / `RISK` (có TC nhưng thiếu chiều) / `GAP` (không có TC).

### Folder review
`tasks/YYYY-MM-DD_<bug-id>_<slug>/` — bên trong chứa đúng 5 file `01-bug-task.md` → `05-review-report.md`.

## 5 quy tắc vàng khi review

Xem [§4 README.md](README.md#4-quy-tắc-vàng-khi-review) — bắt buộc đọc và áp dụng đầy đủ trước khi sinh report. Không lặp lại ở đây để tránh drift giữa 2 file.

## Ràng buộc khi sinh report

- **KHÔNG bịa** impact / TC / spec — chỉ dựa trên 4 file input trong folder review hiện tại.
- Input thiếu thông tin → ghi rõ `Input thiếu: ...` trong report, không đoán.
- Ưu tiên phát hiện `GAP` / `[BLOCKER]` hơn là `[MINOR]` / `[NIT]` — Leader cần thấy rủi ro bỏ lọt bug trước.
- Output là **draft cho Leader verify**, không phải final — viết rõ ràng, dễ chỉnh.
- Khi đề xuất TC bổ sung: phải đủ Title / Precondition / Steps / Expected / Map to Impact — member đọc là viết được.

## Bảo mật

- `credentials/*.json` (service account Google) — **KHÔNG BAO GIỜ** commit, không paste nội dung vào chat, không log ra file. Đã được gitignore.
- `.env` (Redmine API key, etc.) — **KHÔNG commit**. Đã được gitignore. Chỉ commit `.env.example`.
- `scripts/sync-tc.config.json` (chứa Sheet ID riêng) — đã gitignored. Chỉ commit file `.example.json`.
- `.claude/settings.local.json` cũng đã gitignored.

## MCP

Project có 2 MCP server cấu hình trong [.mcp.json](.mcp.json):
- **google-sheets** — `/new-task` fetch TC cũ từ Sheet (qua Link TCs trong Redmine); `/write-tc` fetch TC cũ tham chiếu; `/sync-tc` push TCs mới qua `scripts/push_tc.py`. Setup: [docs/MCP-SETUP.md](docs/MCP-SETUP.md).
- **redmine** — `/new-task <redmine-url>` fetch issue → auto-fill `01-bug-task.md` + `03-dev-impact.md` + (option) `04-tc-list.md`. Setup: [docs/REDMINE-SETUP.md](docs/REDMINE-SETUP.md).

Không tự chạy `uvx` / sửa `.mcp.json` / `.env` trừ khi user yêu cầu.

## Sub-repo `spec-features/`

[spec-features/](spec-features/) là **git sub-repo độc lập** (có `.git` riêng) chứa spec reverse-engineer 38 features. Không commit file ở đây từ repo cha. Khi cần spec chi tiết feature cụ thể, đọc `spec-features/admin/<feature>/feature-spec.md`.
