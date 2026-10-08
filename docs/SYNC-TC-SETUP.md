# Sync TCs lên Google Sheet — Setup

Hướng dẫn dùng `/sync-tc <folder>` để push TCs từ `04-tc-list.md` lên Google Sheet **đã được user pre-create tab và chỉ định URL có `?gid=<tab_id>`**.

**Strategy**: APPEND. Script tìm row trống đầu tiên (cột A) trong tab, ghi header + TCs từ đó xuống. Mỗi lần sync = 1 block mới. KHÔNG tạo tab mới, KHÔNG xóa data cũ.

## Tiền điều kiện

- ✅ Service account đã setup → xem [MCP-SETUP.md](MCP-SETUP.md) bước 1-6
- ✅ `credentials/google-service-account.json` đã tồn tại
- ✅ `uv` đã cài (xem [MCP-SETUP.md](MCP-SETUP.md) Troubleshooting)
- ✅ Service account có quyền Editor trên Sheet (hoặc folder Drive chứa Sheet)

## Setup lần đầu (1 lần / repo)

### Bước 1 — Tạo file config

```powershell
Copy-Item scripts/sync-tc.config.example.json scripts/sync-tc.config.json
```

Để nguyên placeholder `spreadsheet_id` (giá trị thực sẽ paste per-task qua HTML comment). Có thể tùy chỉnh `columns` nếu muốn đổi format cột.

> ⚠️ File `sync-tc.config.json` đã gitignored.

### Bước 2 — Share quyền cho service account

1. Lấy email service account: mở `credentials/google-service-account.json` → field `client_email`
2. Share **folder Drive** chứa Sheet (cách dễ nhất — tất cả Sheet trong folder tự kế thừa quyền): mở folder Drive → Share → paste email service account → quyền **Editor**

Hoặc share từng Sheet riêng lẻ.

## Per task workflow (mỗi task)

### Bước 1 — Tạo tab mới trong Sheet

Trong Sheet bạn quản lý cho task này (có thể là 1 Sheet riêng / 1 Sheet chung):
1. Tạo 1 tab mới (đặt tên theo convention của bạn, vd `KH-36202` hoặc `2026-05-07_staff-limit`)
2. Click vào tab đó, copy URL từ thanh địa chỉ:
   ```
   https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit?gid=<TAB_ID>
                                                          ^^^^^^^^^^
                                                          gid của tab
   ```

### Bước 2 — Thêm sync target vào file 04

Mở `tasks/<folder>/04-tc-list.md`, chèn HTML comment ở **dòng 1**:

```markdown
<!-- sync-target: https://docs.google.com/spreadsheets/d/1z8Qf.../edit?gid=2004892297 -->

# 04 — TC List ...
```

Nếu user chạy `/write-tc` để sinh draft thì AI sẽ tự hỏi URL ở Bước 1.4 và chèn comment này tự động.

### Bước 3 — Sync

```
/sync-tc tasks/2026-05-07_KH-36202_staff-limit-bot-standard/
```

Hoặc chạy script trực tiếp:

```powershell
uv run scripts/push_tc.py tasks/2026-05-07_KH-36202_staff-limit-bot-standard/
```

Override URL ad-hoc (không sửa file 04):

```powershell
uv run scripts/push_tc.py tasks/.../ --spreadsheet "https://docs.google.com/spreadsheets/d/<id>/edit?gid=<tab_id>"
```

Output success:
```
Folder: 2026-05-07_KH-36202_staff-limit-bot-standard
Bug ID: KH-36202 | Date: 2026-05-07 | TCs: 28
Target: spreadsheet=1z8QfSl... gid=2004892297
  source: HTML comment in 04-tc-list.md
Resolved tab: 'KH-36202_v1' (gid=2004892297)
Next empty row: 1 → writing header at A1
OK: appended 28 TCs to tab 'KH-36202_v1' starting at row 1 (1 header + 28 data rows)
     Applied dropdown on: Status (rows 2-230)
URL: https://docs.google.com/spreadsheets/d/.../edit?gid=2004892297
```

## Re-sync (sau khi sửa file 04)

Chạy lại `/sync-tc` → script tìm row trống đầu tiên SAU block cũ và append block mới xuống.

Ví dụ:
- Lần 1: ghi vào row 1-29 (1 header + 28 TCs)
- Sửa file 04 (thêm/sửa TC)
- Lần 2: ghi vào row 30-58 (1 header + 28 TCs mới)

Tab sẽ chứa nhiều block lịch sử. User scroll xuống xem version mới nhất. Data cột Status / Assignee / Output note của block cũ **giữ nguyên** (không bị đè).

## Precedence

Sync target được resolve theo thứ tự:

1. CLI `--spreadsheet <URL>`
2. HTML comment `<!-- sync-target: <URL> -->` trong 04-tc-list.md
3. Config fallback `spreadsheet_id` trong `scripts/sync-tc.config.json` (chỉ hoạt động nếu URL có gid)

URL **bắt buộc có `?gid=<số>`**. Thiếu gid → script die.

## Custom column format

File `scripts/sync-tc.config.json` array `columns` định nghĩa cột Sheet. Mỗi item có 1 trong 3 mode:

```json
// Mode 1 — dynamic: lấy từ TC field
{ "header": "Title", "source": "title" }

// Mode 2 — static: lấy từ metadata (folder name / file header)
{ "header": "Bug ID", "source": "bug_id", "static": true }

// Mode 3 — empty: cell trống cho QA fill thủ công
{ "header": "Assignee", "empty": true }

// Mode 3 + dropdown: cell trống nhưng có data validation dropdown
{ "header": "Status", "empty": true, "dropdown": ["OK", "NG", "Not test"] }
```

### Source keys động (Mode 1 — 1 row / 1 TC)

`push_tc.py` đọc bảng TC trong file 04 **theo tên header**, nhận cả 3 format: **14 cột** (chuẩn từ 2026-10-07) · **16 cột canonical** · **10 cột cũ**. Key không có trong format của file → ô trống. Bảng ánh xạ đầy đủ: `TC_FIELD_HEADERS` trong `scripts/push_tc.py`.

| Source | Header 14 cột | Header 16 cột | Header 10 cột cũ |
|---|---|---|---|
| `tc_id` | ID | TC No. | TC ID |
| `title` | Tên case | Tiêu đề test case | Title |
| `type` | Loại case | Loại case | Type |
| `group` | Nhóm | — | — |
| `viewpoint` | Mã quan điểm | Mã quan điểm liên kết | — |
| `screen` | Màn hình/chức năng | — | — |
| `exec_mode` | Chạy | — | — |
| `environment` | Phạm vi ENV | Môi trường test | Environment |
| `precondition` | Tiền điều kiện | Điều kiện tiền đề | Precondition |
| `steps` | Các bước thực hiện (giữ `
` xuống dòng từ `<br>`) | Các bước thực hiện | Steps |
| `data_input` | Dữ liệu nhập | Dữ liệu test/input | — |
| `expected` | Kết quả mong đợi | Kết quả mong đợi | Expected result |
| `result` | Kết quả thực thi | Kết quả thực thi | — |
| `spec_status` | — (nằm trong Ghi chú) | Trạng thái đánh giá spec | — |
| `note` | Ghi chú | Ghi chú | — |
| `priority` | — | — | Priority |
| `map_to_impact` | — | — | Map to Impact |

### Source keys static (Mode 2 — giá trị giống nhau cho mọi row)

Set `"static": true`:

| Source | Lấy từ |
|---|---|
| `bug_id` | tên folder review |
| `date` | tên folder review (date prefix) |
| `slug` | tên folder review (slug suffix) |
| `tester` | header file 04 → "Tester viết TCs" |
| `submit_date` | header file 04 → "Ngày submit" |
| `version` | header file 04 → "Version TCs" |
| `link_goc` | header file 04 → "Link TC gốc (nếu có)" |

### Format mặc định (`sync-tc.config.example.json`)

**14 cột — giống file 04 / §7 report** (đổi 2026-10-07 từ 10 cột cũ):

| # | Header | Mode | Nguồn |
|---|---|---|---|
| 1 | ID | dynamic | `tc_id` |
| 2 | Nhóm | dynamic | `group` |
| 3 | Mã quan điểm | dynamic | `viewpoint` |
| 4 | Màn hình/chức năng | dynamic | `screen` |
| 5 | Loại case | dynamic | `type` |
| 6 | Chạy | dynamic | `exec_mode` |
| 7 | Phạm vi ENV | dynamic | `environment` |
| 8 | Tên case | dynamic | `title` |
| 9 | Tiền điều kiện | dynamic | `precondition` |
| 10 | Các bước thực hiện | dynamic | `steps` |
| 11 | Dữ liệu nhập | dynamic | `data_input` |
| 12 | Kết quả mong đợi | dynamic | `expected` |
| 13 | Kết quả thực thi | empty + dropdown | Đạt / Không đạt / Chưa test |
| 14 | Ghi chú | dynamic | `note` |

> ⚠️ `scripts/sync-tc.config.json` (gitignored, mỗi máy 1 bản) **không tự đổi theo** — máy nào còn bản 10 cột cũ thì copy lại mảng `columns` từ file example, hoặc giữ 10 cột nếu Sheet đích vẫn dùng layout cũ (script vẫn điền được `tc_id` / `title` / `type` / `precondition` / `steps` / `expected` từ file 04 14 cột).

## Auto-formatting

Mỗi lần sync:

- **Freeze row 1**: chỉ apply khi đây là lần sync đầu tiên (row trống đầu = 1). Lần sau append xuống → không động đến freeze.
- **Data validation dropdown**: apply trên block mới (rows trong block + buffer 200 rows). Không ảnh hưởng dropdown của block cũ.

## Troubleshooting

| Lỗi | Nguyên nhân | Fix |
|---|---|---|
| `Target URL has no 'gid'` | URL thiếu `?gid=<số>` | Mở Sheet → click vào tab cần sync → copy URL từ thanh địa chỉ (đã có gid) → update HTML comment |
| `No tab found with gid=<n>` | Tab đã bị xóa, hoặc gid không thuộc Sheet đang trỏ tới | Script in danh sách tab + gid hợp lệ. Mở Sheet, verify tab tồn tại, copy URL mới. |
| `403 Permission denied` | Sheet chưa share / share Viewer | Share folder Drive chứa Sheet với service account (Editor), hoặc share Sheet riêng lẻ |
| `No target spreadsheet resolved` | Thiếu cả CLI + HTML comment + config | Add HTML comment vào 04-tc-list.md, hoặc truyền `--spreadsheet <URL>` |
| `Config not found` | Chưa copy từ example | `Copy-Item scripts/sync-tc.config.example.json scripts/sync-tc.config.json` |
| `No TCs found in 04-tc-list.md` | File 04 không có bảng TC valid | Cột đầu của header bảng TC phải là `ID` (14 cột) / `TC No.` (16 cột) / `TC ID` (10 cột), mỗi dòng TC có ID + tên case |
| `uvx: command not found` | Chưa cài uv | `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

## So sánh /sync-tc vs MCP google-sheets

Project có 2 cách kết nối Google Sheets:

| | `/sync-tc` (script) | MCP google-sheets |
|---|---|---|
| Mục đích | Push TC list APPEND vào tab user chỉ định | Đọc Sheet bất kỳ trong session |
| Trigger | Slash command + script Python | Claude tự gọi tool MCP |
| Auth | Service account (read+write scope) | Service account (read-only scope hiện tại) |
| Khi nào dùng | Sync output review | Đọc checklist sheet / TC cũ để tham chiếu |
