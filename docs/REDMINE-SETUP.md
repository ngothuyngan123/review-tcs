# Redmine MCP Setup

Hướng dẫn setup MCP Redmine cho project, cho phép Claude (qua `/write-tc`) tự đọc issue Redmine và auto-fill `01-bug-task.md`.

---

## Các bước

### Bước 1 — Lấy API access key trên Redmine

1. Đăng nhập Redmine (vd `https://redmine.lme.jp`).
2. Góc trên phải → **My account** (アカウント).
3. Sidebar phải → **API access key** → click **Show** (hoặc **Reset** nếu chưa có).
4. Copy chuỗi key (40 ký tự hex).

> ⚠ Key này có quyền truy cập **mọi project user nhìn thấy được**. Đừng share, đừng commit.

### Bước 2 — Set env vars

1. Copy file mẫu:
   ```powershell
   # PowerShell
   Copy-Item .env.example .env
   ```
   ```bash
   # Bash
   cp .env.example .env
   ```
2. Mở `.env` và điền:
   ```
   REDMINE_URL=https://redmine.example.com
   REDMINE_API_KEY=your-api-key-here
   ```
   - `REDMINE_URL` là **BASE URL** của Redmine (vd `https://redmine.example.com`), KHÔNG kèm `/projects/.../issues` path.
   - Không thêm dấu nháy quanh giá trị. Không có space sau `=`.

> `.env` đã được `.gitignore` block — sẽ không commit. Chỉ commit `.env.example`.

### Bước 3 — Load env vars vào shell trước khi mở Claude Code

Claude Code expand `${REDMINE_URL}` và `${REDMINE_API_KEY}` trong `.mcp.json` từ env của shell đang chạy nó. Phải load `.env` vào shell trước khi launch Claude Code.

**PowerShell** — load `.env` mỗi lần mở terminal:

```powershell
# Load từng dòng KEY=VALUE
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
    [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
  }
}

# Mở Claude Code SAU khi load env
claude
```

(Có thể bỏ snippet này vào `$PROFILE` để auto-load khi vào folder project.)

**Bash / WSL**:

```bash
set -a; source .env; set +a
claude
```

### Bước 4 — Verify MCP redmine kết nối

1. Mở Claude Code trong root project: `claude` (sau khi đã load env ở Bước 3).
2. Gõ `/mcp` → verify thấy `redmine` server status `connected`.
3. Hỏi Claude (test connection): `Dùng MCP redmine, get_issue cho issue ID <số có thật> rồi cho tôi xem subject + author.`

Claude sẽ gọi tool `redmine__get_issue` và trả về dữ liệu Redmine.

---

## Sử dụng với `/write-tc`

Sau khi setup xong, truyền Redmine URL làm argument thứ 2:

```
/write-tc tasks/2026-05-12_KH-36317_form-page-mismatch/ https://redmine.lme.jp/issues/36317
```

Claude sẽ:
1. Parse issue ID `36317` từ URL.
2. Call `redmine__get_issue(issue_id=36317, include="journals,attachments")`.
3. Auto-fill `01-bug-task.md` (template `templates/01-bug-task.template.md`).
4. DỪNG, yêu cầu user verify field `Auto-filled` + tick checkbox "Tester verify auto-fill chính xác" trước khi sang bước tiếp.

Sau khi tester verify xong → invoke lại `/write-tc <folder>` (không cần Redmine URL nữa) để chạy Bước 1-7 (sinh `04-tc-list.md`).

---

## Troubleshooting

| Triệu chứng | Nguyên nhân | Fix |
|---|---|---|
| `/mcp` không thấy `redmine` server | `uvx mcp-redmine` không cài được | Verify `uvx --version`. Nếu chưa có → `pip install uv` hoặc xem [uv install](https://github.com/astral-sh/uv). |
| Server `redmine` status `failed` | Env vars chưa expand | Verify `$env:REDMINE_URL` (PowerShell) hoặc `echo $REDMINE_URL` (Bash) có giá trị. Nếu trống → chưa load `.env`, xem Bước 3. |
| Tool call trả `401 Unauthorized` | API key sai | Verify key trong `.env` đúng (40 ký tự hex). Reset key trong Redmine → cập nhật `.env`. |
| Tool call trả `403 Forbidden` | User không có quyền xem issue (project private) | Hỏi PM cấp quyền vào project tương ứng. |
| Tool call trả `404 Not Found` | Issue ID không tồn tại / URL sai | Verify URL Redmine có format `<base>/issues/<id>`. |
| `.env` đã load nhưng `${REDMINE_URL}` vẫn không expand trong `.mcp.json` | Claude Code đã start trước khi load env | Thoát Claude Code → load env → khởi động lại. |

---

## Bảo mật

- ❌ KHÔNG commit `.env` (đã gitignore).
- ❌ KHÔNG paste API key vào chat / log / file.
- ❌ KHÔNG share `.env` qua Slack/Email — mỗi tester tự lấy key riêng từ Redmine UI.
- ✅ Reset API key khi nghi key bị lộ (Redmine: My account → API access key → Reset).

---

## Cấu hình hiện tại

| File | Mục đích |
|---|---|
| [.mcp.json](../.mcp.json) | Config MCP server `redmine` (đọc `${REDMINE_URL}` + `${REDMINE_API_KEY}` từ env) |
| [.env.example](../.env.example) | Mẫu env vars để copy thành `.env` |
| [.gitignore](../.gitignore) | Block `.env` khỏi git |

---

## Tham khảo

- MCP Redmine server: https://pypi.org/project/mcp-redmine/ (hoặc package tương đương — verify version trong `.mcp.json`).
- Redmine REST API: https://www.redmine.org/projects/redmine/wiki/Rest_api
