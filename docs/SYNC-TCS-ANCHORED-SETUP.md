# Sync TC vào sheet TC human (anchored) — Setup

Hướng dẫn `/sync-ai-tc <folder>` và `/sync-review-tc <folder>` — push TC vào **sheet TC human/master**, ghi 5 cột bắt đầu tại cột **"Main Function"**.

**Strategy**: APPEND data-only. Script tìm cột header `anchor` ("Main Function") trên 15 dòng đầu của tab, đo row cuối có data theo cột đó, ghi 5 cột `TC ID, Title, Precondition, Steps, Expected` vào 5 cột LIÊN TIẾP từ cột anchor xuống dưới. **KHÔNG ghi header, KHÔNG tạo tab mới, KHÔNG đè data cũ.**

| | `/sync-ai-tc` | `/sync-review-tc` |
|---|---|---|
| Nguồn TC | bảng TC trong `04-tc-list.md` (TC do AI viết) | bảng §5 "TCs đề xuất bổ sung" trong `05-review-report.md` (TC reviewer bổ sung) |
| `--source` | `04` | `05` |
| Target Sheet | config `sync-tcs` trong `04-tc-list.md` | config `sync-tcs` trong `04-tc-list.md` (dùng chung) |

> So với `/sync-tc` (ghi từ cột A + 1 header block vào tab AI pre-create, dùng `<!-- sync-target: ... -->`): 2 command này ghi thẳng vào sheet TC human tại cột "Main Function", không header, dùng config riêng `<!-- sync-tcs: ... -->`.

## Tiền điều kiện

- ✅ Service account đã setup → [MCP-SETUP.md](MCP-SETUP.md). `credentials/google-service-account.json` tồn tại.
- ✅ `uv` đã cài.
- ✅ Service account có quyền **Editor** trên sheet TC human (write scope).

## Config target trong file 04

Chèn HTML comment ở **dòng 1** của `tasks/<folder>/04-tc-list.md`:

```markdown
<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit | sheet=<tên tab TC human> | anchor=Main Function -->
```

- `url` — URL Google Sheet TC human/master (cần `/d/<SHEET_ID>`; gid không bắt buộc vì tab resolve theo tên).
- `sheet` — **tên tab** chứa TC human (resolve theo tên, không theo gid).
- `anchor` — tên cột header để canh vị trí ghi. Mặc định `Main Function` nếu bỏ trống.

Template `templates/04-tc-list.template.md` đã có sẵn dòng này với placeholder — điền giá trị thật per-task.

## Chạy

```powershell
# TC do AI viết (file 04)
uv run scripts/push_tc_anchored.py tasks/<folder>/ --source 04

# TC bổ sung của reviewer (file 05 §5)
uv run scripts/push_tc_anchored.py tasks/<folder>/ --source 05
```

Override không sửa file 04:

```powershell
uv run scripts/push_tc_anchored.py tasks/<folder>/ --source 04 `
  --url "https://docs.google.com/spreadsheets/d/<id>/edit" --sheet "<tab>" --anchor "Main Function"
```

Output success:
```
OK: ghi 12 TC vào tab 'TC_KH-35968' cột C:G, row 48-59
```

## Precedence target

1. CLI `--url` / `--sheet` / `--anchor`
2. Config `<!-- sync-tcs: ... -->` trong `04-tc-list.md`

## Troubleshooting

| Lỗi | Nguyên nhân | Fix |
|---|---|---|
| `Thiếu target URL Sheet TC human` | Chưa có config sync-tcs + không truyền CLI | Add `<!-- sync-tcs: url=... \| sheet=... -->` vào file 04 |
| `Không tìm thấy tab tên '<x>'` | Sai tên tab | Script in list tab hợp lệ — copy đúng tên |
| `Không tìm thấy cột header 'Main Function'` | Sheet không có cột đó trong 15 dòng đầu | Verify header, hoặc `--anchor "<tên cột đúng>"` |
| `Không tìm thấy section '## 5...'` (source 05) | File 05 thiếu §5 | Verify file 05 bám template |
| `Không có TC nào parse được` | Bảng TC rỗng / chỉ row template | Điền TC vào bảng nguồn |
| `403 Permission denied` | Sheet chưa share Editor | Share sheet với `client_email` service account, quyền **Editor** |
