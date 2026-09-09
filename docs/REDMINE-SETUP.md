# Redmine REST API Setup

Hướng dẫn setup kết nối Redmine cho project, cho phép Claude (qua `/new-task`) tự đọc issue Redmine và auto-fill `01-bug-task.md` + `03-dev-impact.md`.

> ⚠️ **Đổi từ 2026-09-09**: project **KHÔNG dùng MCP redmine nữa**. Thay bằng gọi thẳng **Redmine REST API** qua script [scripts/redmine_fetch.py](../scripts/redmine_fetch.py) với API key trong `.env`.
> Lợi ích: không cần `uvx` / MCP server chạy nền, không cần export env vào shell trước khi mở Claude Code, lỗi HTTP hiện rõ ràng (401/403/404) ngay trên terminal.
> Nếu `.mcp.json` cũ của bạn còn block `redmine` → xóa đi, không còn tác dụng.

---

## Các bước

### Bước 1 — Lấy API access key trên Redmine

1. Đăng nhập Redmine (vd `https://redmine.watermelon.vn`).
2. Góc trên phải → **My account** (アカウント).
3. Sidebar phải → **API access key** → click **Show** (hoặc **Reset** nếu chưa có).
4. Copy chuỗi key (40 ký tự hex).

> ⚠ Key này có quyền truy cập **mọi project user nhìn thấy được**. Đừng share, đừng commit.
> Nếu Redmine trả `403` ở mọi request → nhờ admin bật **Administration → Settings → API → Enable REST web service**.

### Bước 2 — Điền `.env`

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
   REDMINE_URL=https://redmine.watermelon.vn
   REDMINE_API_KEY=<40 ký tự hex copy ở Bước 1>
   ```
   - `REDMINE_URL` là **BASE URL** của Redmine, KHÔNG kèm `/projects/.../issues` path.
   - Không thêm dấu nháy quanh giá trị. Không có space sau `=`.
   - Redmine nội bộ dùng self-signed cert → thêm `REDMINE_VERIFY_SSL=0`.

> `.env` đã được `.gitignore` block — sẽ không commit. Chỉ commit `.env.example`.
> **Không cần load `.env` vào shell** — script đọc thẳng file. (Env var của shell nếu có thì được ưu tiên hơn `.env`.)

### Bước 3 — Verify kết nối

```bash
python scripts/redmine_fetch.py --check
```

In ra `OK - <base url> - dang nhap voi: <login> (<tên>)` là xong. Lỗi thì xem bảng [Troubleshooting](#troubleshooting).

---

## Script `scripts/redmine_fetch.py`

Chỉ dùng **stdlib Python** (`urllib`) — không cần cài thêm package.

```bash
# Fetch 1 issue → in digest markdown ra stdout
python scripts/redmine_fetch.py https://redmine.watermelon.vn/issues/36437

# Issue id thuần (lấy base URL từ REDMINE_URL trong .env)
python scripts/redmine_fetch.py 36437

# Kèm dump JSON gốc ra file (để parse lại, không phải đọc hết vào context)
python scripts/redmine_fetch.py 36437 --json "$TMPDIR/rm36437.json"

# Bỏ journals cho nhẹ
python scripts/redmine_fetch.py 36437 --no-journals

# Test kết nối + API key
python scripts/redmine_fetch.py --check
```

**stdout** = digest markdown, đủ để auto-fill file 01 + 03:

| Phần | Nội dung |
|---|---|
| Header | `# Redmine #<id> - <subject>` |
| Metadata | URL · Project · Tracker · Status · Priority · Author · Assignee · Created · Updated · Custom fields (chỉ field có giá trị) |
| Attachments | filename + filesize + `content_url` (link download trực tiếp) |
| Relations | `relates #xxx` / `blocks #xxx` … (nếu có) |
| `## Description (nguyen van)` | Description **giữ nguyên format gốc** (markdown hoặc textile) |
| `## Journals co notes (n)` | Chỉ journal **có `notes`** — journal chỉ đổi status/assignee bị loại |

**Exit code**: `0` OK · `2` thiếu config/tham số · `3` URL sai format · `4` lỗi HTTP (401/403/404/…) · `5` không kết nối được.

Endpoint gọi: `GET <base>/issues/<id>.json?include=journals,attachments,relations`, header `X-Redmine-API-Key`. **Chỉ đọc** — script không có đường ghi/sửa issue.

---

## Sử dụng với `/new-task`

```
/new-task https://redmine.watermelon.vn/issues/36317
```

Claude sẽ:
1. Parse issue ID `36317` từ URL.
2. Chạy `python scripts/redmine_fetch.py <url> --json <scratchpad>/redmine-36317.json`.
3. Tạo folder `tasks/<YYYY-MM-DD>_36317_<slug>/`, auto-fill `01-bug-task.md` + `03-dev-impact.md` (+ `04-tc-list.md` nếu Redmine có "Link TCs", hoặc fallback MCP LME TEST STUDIO).
4. **DỪNG** — tester verify lại nội dung auto-fill: đọc lại `01-bug-task.md` đối chiếu Redmine, tick checkbox "Tester verify auto-fill chính xác" ở `03-dev-impact.md`.

Sau khi verify xong → gõ skill tiếp theo (`/write-tc <folder>` hoặc `/review-tc <folder>`). `/write-tc` và `/review-tc` **không đụng Redmine**.

---

## Troubleshooting

| Triệu chứng | Nguyên nhân | Fix |
|---|---|---|
| `ERROR: Thieu REDMINE_API_KEY` | `.env` chưa tạo, hoặc còn giá trị mẫu `your-api-key-here` | Làm Bước 1 + 2. |
| `ERROR: Thieu REDMINE_URL` | `.env` thiếu base URL và arg truyền vào là số thuần | Điền `REDMINE_URL` vào `.env`, hoặc truyền URL issue đầy đủ. |
| `HTTP 401` | API key sai / đã reset | Lấy lại key (Bước 1) → cập nhật `.env`. |
| `HTTP 403` | Không có quyền vào project private, hoặc REST API bị tắt trên Redmine | Xin PM cấp quyền project; nhờ admin bật `Enable REST web service`. |
| `HTTP 404` | Issue không tồn tại, hoặc `REDMINE_URL` kèm path thừa | Verify URL đúng format `<base>/issues/<id>`; `REDMINE_URL` phải là gốc site. |
| `Response ... khong phai JSON` | URL redirect về trang login | Thường là key sai hoặc REST API tắt — như 401/403. |
| `Khong ket noi duoc ...` | Sai host / chưa bật VPN / mạng nội bộ | Mở URL Redmine bằng browser để verify; bật VPN nếu Redmine nội bộ. |
| Lỗi `CERTIFICATE_VERIFY_FAILED` | Redmine dùng self-signed cert | Thêm `REDMINE_VERIFY_SSL=0` vào `.env`. |
| `/mcp` không còn thấy server `redmine` | **Đúng như thiết kế** từ 2026-09-09 | Không dùng MCP redmine nữa — dùng script REST API. |

---

## Bảo mật

- ❌ KHÔNG commit `.env` (đã gitignore).
- ❌ KHÔNG paste API key vào chat / log / file / JSON dump.
- ❌ KHÔNG share `.env` qua Slack/Email — mỗi tester tự lấy key riêng từ Redmine UI.
- ✅ Reset API key khi nghi key bị lộ (Redmine: My account → API access key → Reset).
- ✅ Dump `--json` để ở **scratchpad**, không commit vào `tasks/`.

---

## Cấu hình hiện tại

| File | Mục đích |
|---|---|
| [scripts/redmine_fetch.py](../scripts/redmine_fetch.py) | Fetch issue qua REST API (stdlib, không cần package ngoài) |
| [.env.example](../.env.example) | Mẫu env vars để copy thành `.env` |
| [.gitignore](../.gitignore) | Block `.env` khỏi git |
| [.mcp.json](../.mcp.json) | Chỉ còn MCP `google-sheets` — **không còn** server `redmine` |

---

## Tham khảo

- Redmine REST API — Issues: https://www.redmine.org/projects/redmine/wiki/Rest_Issues
- Redmine REST API — Authentication: https://www.redmine.org/projects/redmine/wiki/Rest_api#Authentication
