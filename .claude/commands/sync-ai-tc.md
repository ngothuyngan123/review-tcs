---
description: Push TOÀN BỘ TCs do AI viết (04-tc-list.md) vào sheet TC human/master, ghi 5 cột (TC ID, Title, Precondition, Steps, Expected) từ cột "Main Function", append xuống dưới data hiện có.
argument-hint: <đường dẫn folder review, vd tasks/2026-06-09_35968_sort-4-bug-qrcode-form-url-scenario/>
---

User muốn sync **toàn bộ TCs do AI viết** trong `04-tc-list.md` lên **sheet TC human/master** (sheet được fetch từ TCs human). Script ghi 5 cột `TC ID, Title, Precondition, Steps, Expected` vào 5 cột **LIÊN TIẾP** bắt đầu đúng tại cột header **"Main Function"**, APPEND xuống dưới row cuối cùng có data. **KHÔNG ghi header, KHÔNG tạo tab mới, KHÔNG đè data cũ.**

> Khác `/sync-tc` (ghi từ cột A + header block vào tab AI pre-create). `/sync-ai-tc` ghi thẳng vào sheet TC human tại cột "Main Function".

**Folder review cần sync:** `$ARGUMENTS`

Nếu `$ARGUMENTS` trống → liệt kê folder con trong `tasks/` (sắp xếp ngày mới nhất), hỏi user chọn 1 rồi tiếp tục. KHÔNG tự đoán.

### BƯỚC 1 — Pre-flight check
Verify TRƯỚC khi chạy. Fail → DỪNG và hướng dẫn fix:

- `$ARGUMENTS/04-tc-list.md` tồn tại → nếu không, gợi ý `/write-tc $ARGUMENTS` trước.
- `04-tc-list.md` có config target: `<!-- sync-tcs: url=<URL> | sheet=<tên tab> | anchor=Main Function -->`
  - **Có rồi** → dùng luôn.
  - **Chưa có** → hỏi user: (1) URL Google Sheet TC human/master, (2) tên tab chứa TC human. Sau đó chèn comment trên vào đầu file 04 (xác nhận với user trước khi ghi).
  - `anchor` mặc định `Main Function` nếu bỏ trống.
- `credentials/google-service-account.json` tồn tại → nếu không, trỏ [docs/MCP-SETUP.md](../../docs/MCP-SETUP.md). Service account phải có quyền **Editor** trên Sheet.

### BƯỚC 2 — Chạy push script

**Default** (đọc target từ config sync-tcs trong 04-tc-list.md):
```
uv run scripts/push_tc_anchored.py $ARGUMENTS --source 04
```

**Override target** (không sửa file 04):
```
uv run scripts/push_tc_anchored.py $ARGUMENTS --source 04 --url "<Google Sheet URL>" --sheet "<tên tab>"
```

**Override cột anchor** (nếu sheet không dùng tên "Main Function"):
```
uv run scripts/push_tc_anchored.py $ARGUMENTS --source 04 --anchor "<tên cột>"
```

**Precedence**: CLI `--url/--sheet/--anchor` > config `sync-tcs` trong 04-tc-list.md.

Trước khi confirm: đọc stderr dòng `Resolved tab: '<tab>' | anchor 'Main Function' tại cột <X>` và `Row trống kế tiếp: <n>` — verify đúng tab + đúng cột. Sai → cancel, sửa config.

### BƯỚC 3 — Báo kết quả + xử lý lỗi

**Success**:
```
OK: ghi N TC vào tab '<tab>' cột <start>:<end>, row <start_row>-<end_row>
```
Forward URL cho user. Nhắc: TC được APPEND xuống dưới (không đè data cũ); lần sync sau tiếp tục append.

**Lỗi thường gặp:**

| Stderr chứa | Nguyên nhân | Hướng dẫn user |
|---|---|---|
| `Thiếu target URL Sheet TC human` | Chưa có config sync-tcs + không truyền CLI | Add `<!-- sync-tcs: url=... \| sheet=... -->` vào 04, hoặc `--url --sheet` |
| `Không tìm thấy tab tên '<x>'` | Sai tên tab | Verify tên tab (script in list tab hợp lệ) |
| `Không tìm thấy cột header 'Main Function'` | Sheet không có cột tên đó trong 15 dòng đầu | Kiểm tra header, hoặc truyền `--anchor "<tên cột đúng>"` |
| `403 Permission denied` | Sheet chưa share Editor | Share Sheet → paste `client_email` từ service account, quyền **Editor** |
| `Không có TC nào parse được` | Bảng TC trong file 04 sai format | Verify bảng `\| TC ID \| Title \| ... \|` chuẩn template |

### QUY TẮC
- KHÔNG sửa `04-tc-list.md` khi sync (trừ Bước 1 add config nếu thiếu — hỏi user trước).
- KHÔNG hard-code Sheet ID / credentials trong file commit-được. Target nằm trong config sync-tcs (per-task) + `credentials/` (gitignored).
- KHÔNG tạo tab mới, KHÔNG ghi header, KHÔNG xóa/đè data cũ — chỉ APPEND data rows xuống dưới.
