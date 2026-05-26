# MCP Setup — Google Sheets qua Service Account

Hướng dẫn setup MCP local cho project, cho phép Claude đọc/ghi Google Sheet thông qua service account.

---

## Các bước

### Bước 1 — Tạo Google Cloud project (nếu chưa có)

1. Mở https://console.cloud.google.com
2. Góc trên trái → chọn project hiện tại → **New Project**
3. Đặt tên: `lme-mcp` (hoặc bất kỳ) → **Create**
4. Đợi ~30s để project tạo xong → switch vào project mới

### Bước 2 — Bật API cần thiết

1. Menu trái → **APIs & Services** → **Library**
2. Tìm và **Enable** lần lượt:
   - **Google Sheets API**
   - **Google Drive API**

### Bước 3 — Tạo Service Account

1. Menu trái → **IAM & Admin** → **Service Accounts**
2. **Create Service Account**
3. Điền:
   - Name: `lme-mcp-reader`
   - Description: `MCP reader for LME project spreadsheets`
4. **Create and Continue**
5. Grant role: **chọn "Viewer"** (hoặc bỏ qua, vì share sheet sẽ cấp quyền cụ thể sau)
6. **Done**

### Bước 4 — Tạo JSON key

1. Trong danh sách Service Accounts, click vào account vừa tạo (`lme-mcp-reader@...`)
2. Tab **Keys** → **Add Key** → **Create new key** → **JSON** → **Create**
3. Browser sẽ download 1 file `.json` (ví dụ `lme-mcp-xxxx.json`)

### Bước 5 — Đặt key vào project

1. Đổi tên file vừa download thành **`service-account.json`**
2. Copy vào folder: `credentials/service-account.json` (trong project này)
3. Verify đường dẫn: `lme-review-TCs/credentials/service-account.json`

> ⚠ **File này KHÔNG bao giờ được commit lên git**. `.gitignore` đã block sẵn `credentials/*.json`.

### Bước 6 — Lấy email của service account

Mở file `credentials/service-account.json`, tìm field `"client_email"`:

```json
{
  ...
  "client_email": "lme-mcp-reader@lme-mcp-xxxxxx.iam.gserviceaccount.com",
  ...
}
```

**Đây là email bạn sẽ share Google Sheet tới.**

### Bước 7 — Share Google Sheet với service account

1. Mở Google Sheet cần đọc (ví dụ file checklist LME)
2. Góc trên phải → **Share**
3. Paste email từ bước 6 vào ô thêm người
4. Quyền: **Viewer** (chỉ đọc) — đủ cho use case hiện tại
5. Bỏ tick "Notify people" (service account không check mail)
6. **Share**

### Bước 8 — (Tuỳ chọn) Giới hạn scope bằng Drive folder

Nếu muốn service account chỉ access đúng 1 folder Drive:
1. Tạo folder trên Drive, ví dụ "LME Shared with MCP"
2. Share folder đó với service account email
3. Copy folder ID từ URL (`drive.google.com/drive/folders/XXXX` → `XXXX`)
4. Paste vào `.mcp.json` field `DRIVE_FOLDER_ID`

Nếu không cần, để `DRIVE_FOLDER_ID` rỗng — service account access mọi file đã share với nó.

### Bước 9 — Khởi động lại Claude Code

Sau khi xong bước 5-7:
- Thoát Claude Code hiện tại
- Mở lại project → Claude Code sẽ tự load `.mcp.json`
- Chạy `/mcp` để verify `google-sheets` server đã kết nối

Nếu có lỗi, check:
- `credentials/service-account.json` tồn tại và đúng JSON format
- Sheet đã được share với đúng email service account
- `uvx` có trong PATH (`command -v uvx`)

---

## Test sau khi setup

Sau khi setup xong, hỏi Claude:

```
Đọc sheet <Google Sheet URL hoặc ID> — liệt kê các sheet con trong file này
```

Claude sẽ gọi tool của `mcp-google-sheets` để liệt kê.

---

## Troubleshooting

**Lỗi `403 Permission denied`**
→ Sheet chưa share với service account email. Verify lại Bước 7.

**Lỗi `File not found`**
→ Service account không được cấp quyền (hoặc ID sheet sai). Verify lại share.

**Lỗi `uvx: command not found`**
→ Cài `uv`: https://github.com/astral-sh/uv
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Lỗi `SERVICE_ACCOUNT_PATH not found`**
→ Path trong `.mcp.json` phải relative từ project root. Chạy Claude Code từ root project (`cd lme-review-TCs`).

---

## Cấu hình hiện tại

| File | Mục đích |
|---|---|
| [.mcp.json](../.mcp.json) | Config MCP server `google-sheets` |
| [.gitignore](../.gitignore) | Block `credentials/*.json` khỏi git |
| [credentials/](../credentials/) | Nơi lưu service account JSON (bạn tự drop vào) |

---

## Tại sao dùng Service Account thay vì OAuth?

| | Service Account | OAuth (như MCP claude.ai đang dùng) |
|---|---|---|
| Yêu cầu browser flow | ❌ Không | ✅ Có |
| Token hết hạn | ❌ Không | ✅ Có, phải refresh |
| Access scope | Chỉ files đã share với nó | Toàn bộ Drive của user |
| Email dùng để share | Email service account (cố định) | Email user (mỗi user khác) |
| Dùng cho team | ✅ 1 account dùng chung | ❌ Mỗi người 1 OAuth |

→ Service Account phù hợp với use case "account riêng để share file tới MCP".
