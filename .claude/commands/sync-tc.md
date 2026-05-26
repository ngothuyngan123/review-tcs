---
description: Push TCs từ folder review APPEND vào tab Google Sheet user đã pre-create (URL có gid).
argument-hint: <đường dẫn folder review, vd tasks/2026-05-07_KH-36202_staff-limit-bot-standard/>
---

User muốn sync TCs từ `04-tc-list.md` lên Google Sheet **đã được user pre-create tab và chỉ định URL có `?gid=<tab_id>`**. Script APPEND TCs xuống row trống đầu tiên trong tab đó. KHÔNG tạo tab mới.

**Folder review cần sync:** `$ARGUMENTS`

Nếu `$ARGUMENTS` trống → liệt kê các folder con trong `tasks/` (sắp xếp theo ngày mới nhất), hỏi user chọn 1 trong đó rồi tiếp tục. KHÔNG được tự đoán.

### BƯỚC 1 — Pre-flight check
Verify TRƯỚC khi chạy script. Nếu fail, DỪNG và hướng dẫn user fix:

- `$ARGUMENTS/04-tc-list.md` tồn tại → nếu không, gợi ý chạy `/write-tc $ARGUMENTS` trước.
- `04-tc-list.md` có dòng `<!-- sync-target: <URL có gid> -->` ở đầu file → nếu không:
  - Hỏi user URL đầy đủ (có `?gid=<số>` trỏ tới tab pre-created)
  - Add HTML comment vào dòng 1 của file 04: `<!-- sync-target: <URL> -->`
- `scripts/sync-tc.config.json` tồn tại → nếu không, hướng dẫn `Copy-Item scripts/sync-tc.config.example.json scripts/sync-tc.config.json`.
- `credentials/google-service-account.json` tồn tại → nếu không, trỏ user đến [docs/MCP-SETUP.md](../../docs/MCP-SETUP.md).

### BƯỚC 2 — Chạy push script

**Default** (đọc URL từ HTML comment trong 04-tc-list.md):
```
uv run scripts/push_tc.py $ARGUMENTS
```

**Override target** — khi user muốn push vào tab khác (URL có gid khác):
```
uv run scripts/push_tc.py $ARGUMENTS --spreadsheet "https://docs.google.com/spreadsheets/d/<id>/edit?gid=<tab_id>"
```

**Precedence**: CLI `--spreadsheet` > HTML comment trong 04-tc-list.md > config fallback `spreadsheet_id`.

URL **bắt buộc có `gid`**. Nếu thiếu → script die với hướng dẫn user mở tab cụ thể trong Sheet để Google tự thêm gid vào URL.

Trước khi chạy: kiểm tra stderr in dòng `Target: spreadsheet=<id> gid=<gid>` và `Resolved tab: '<tên tab>'` — confirm đúng tab user mong muốn. Nếu sai → cancel + sửa URL trong HTML comment.

### BƯỚC 3 — Báo kết quả + xử lý lỗi

**Success**:
```
OK: appended N TCs to tab '<tên tab>' starting at row <start_row> (1 header + N data rows)
URL: https://docs.google.com/spreadsheets/d/<id>/edit?gid=<gid>
```

Forward URL cho user. Nhắc:
- TC mới được APPEND xuống dưới (không đè data cũ). Block bắt đầu từ row `<start_row>` gồm 1 header + N rows.
- Lần sync thứ 2 sẽ tiếp tục append xuống nữa (tạo block mới sau dữ liệu hiện có).
- Cột Status có dropdown auto-apply trên block mới.

**Lỗi thường gặp:**

| Stderr chứa | Nguyên nhân | Hướng dẫn user |
|---|---|---|
| `Target URL has no 'gid'` | URL thiếu `?gid=<số>` | Mở Sheet, click vào tab cần sync → copy URL từ địa chỉ trình duyệt (sẽ có `gid` tự động) → update HTML comment |
| `No tab found with gid=<n>` | Tab bị xóa, hoặc gid không thuộc Sheet này | Verify lại URL. Script in danh sách tab + gid hợp lệ trong stderr. |
| `403 Permission denied` | Sheet chưa share với service account / share quyền Viewer | Mở Sheet → Share → paste email từ `credentials/google-service-account.json` field `client_email`, quyền **Editor**. (Hoặc share folder Drive chứa Sheet.) |
| `No target spreadsheet resolved` | Cả CLI args, HTML comment, config đều thiếu | Truyền `--spreadsheet <URL>`, hoặc add HTML comment vào 04-tc-list.md |
| `Config not found` | Chưa copy từ example | `Copy-Item scripts/sync-tc.config.example.json scripts/sync-tc.config.json` |
| `Credentials not found` | Chưa setup service account | Trỏ đến `docs/MCP-SETUP.md` |
| `No TCs found` | File 04 không có bảng TC valid | Verify format bảng `\| TC ID \| Title \| ...` chuẩn template |

### QUY TẮC
- KHÔNG sửa file `04-tc-list.md` trong quá trình sync (trừ trường hợp ở Bước 1 phải add HTML comment nếu thiếu — có hỏi user trước).
- KHÔNG hard-code Sheet ID hay credentials trong file commit-được. Tất cả nằm trong `scripts/sync-tc.config.json` (gitignored) và `credentials/` (gitignored).
- KHÔNG tạo tab mới trong Sheet. User phải pre-create tab và share URL có gid.
- KHÔNG xóa / sửa data cũ trong tab. Script chỉ APPEND xuống dưới.
- Nếu user yêu cầu sửa column format → mở `scripts/sync-tc.config.json` và sửa array `columns`. Chi tiết source keys: [docs/SYNC-TC-SETUP.md](../../docs/SYNC-TC-SETUP.md).
