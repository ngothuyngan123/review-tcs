# Write TCs — hướng dẫn dùng

> File này là tài liệu cho người. Logic vận hành nằm ở slash command [/write-tc](../.claude/commands/write-tc.md).

## Cách chạy

Trong Claude Code, gõ:

```
/write-tc tasks/YYYY-MM-DD_<bug-id>_<slug>/
```

Hoặc gõ `/write-tc` không kèm folder → Claude sẽ liệt kê các folder con trong `tasks/` để bạn chọn.

## Khi nào dùng

QA member chạy `/write-tc` khi **chưa viết TC**, muốn AI sinh draft để verify + chỉnh thay vì viết từ đầu. Mục tiêu: bám đúng coverage rule + checklist LME ngay từ vòng 1, giảm số vòng review.

Claude sẽ:
1. Đọc bug + dev-impact (+ spec nếu có)
1b. **(TÙY CHỌN)** Hỏi user 2 thứ: (a) link Google Sheet TCs cũ để tham chiếu (read-only — Claude KHÔNG sửa TC cũ), (b) tên tab output cho TC mới (cùng Spreadsheet với TC cũ, tab mới user tự đặt)
2. Xác định scope checklist LME liên quan
3. Lập ma trận TC tối thiểu theo 5 quy tắc vàng (reuse TC cũ nếu đã cover; KHÔNG override TC cũ)
4. Sinh TC theo [template 04](../templates/04-tc-list.template.md) (10 cột — không có Map to Impact, Title phải chứa keyword để Leader suy luận impact)
5. Self-check coverage trước khi xuất
6. Ghi `04-tc-list.md` (hoặc `04-tc-list.draft.md` nếu file đã tồn tại). Nếu user có chỉ định sync target → chèn HTML comment `<!-- sync-target: spreadsheet=... tab=... -->` ở đầu file để `/sync-tc` đọc.

## Tiền điều kiện

Folder review phải có:
- ✅ `01-bug-task.md` (BẮT BUỘC — không có thì DỪNG)
- ✅ `03-dev-impact.md` (BẮT BUỘC — không có thì DỪNG)
- ⚠️ `02-spec-reference.md` (tùy chọn — không có thì fallback về [LME-SYSTEM-SPEC.md](../templates/LME-SYSTEM-SPEC.md))

## Optional input — TCs cũ của tính năng (Google Sheet) + Tab output

Khi tính năng đã có TCs ở vòng test trước, cung cấp link Sheet để Claude **đọc tham chiếu, tránh sinh TC trùng**. **TC cũ là READ-ONLY** — Claude KHÔNG sửa, KHÔNG override TC cũ dù BUG fix có đổi behavior. Nếu phát hiện TC cũ có vẻ sai sau fix, Claude chỉ ghi cảnh báo cho member tự verify thủ công.

TC mới do Claude sinh ra sẽ luôn đi vào **tab MỚI** (do bạn tự đặt tên) trong **cùng Spreadsheet** với TC cũ, không động vào tab TC cũ.

Khi Claude hỏi ở Bước 1.4, chuẩn bị:
1. **Link spreadsheet** — paste URL đầy đủ (vd `https://docs.google.com/spreadsheets/d/ABC123XYZ/edit#gid=0`) hoặc chỉ Sheet ID (`ABC123XYZ`).
2. **Tên tab TC cũ** — vd `Broadcast TCs v2`. Không nhớ → Claude sẽ liệt kê tab cho chọn.
3. **Range TC cũ** *(tùy chọn)* — A1 notation, vd `A2:J100` (skip header) hoặc `A:J` (cả cột). **Để trống → đọc toàn bộ sheet.**
4. **Tên tab output cho TC mới** — bạn tự đặt, vd `KH-36202_fix_2026-05-08`. Tab này sẽ được tạo ở cùng Spreadsheet ở step 1 khi chạy `/sync-tc`.

Sheet phải đã share **Editor** với service account email trong `credentials/google-service-account.json` (field `client_email`). Setup chi tiết: [docs/MCP-SETUP.md](../docs/MCP-SETUP.md).

Không có TCs cũ → vẫn có thể cung cấp riêng tab output (link Spreadsheet + tab name). Hoàn toàn skip → Claude dùng config master mặc định khi `/sync-tc` chạy.

Sau khi user cung cấp, Claude lưu vào HTML comment ở đầu `04-tc-list.md`:
```html
<!-- sync-target: spreadsheet=ABC123XYZ tab=KH-36202_fix_2026-05-08 -->
```
`/sync-tc` đọc comment này và push vào đúng target — không cần truyền args lại.

## Sau khi Claude sinh xong — member BẮT BUỘC verify

1. **Đọc lại từng TC** — Claude có thể bịa precondition không khả thi, hoặc steps thiếu chi tiết domain.
2. **Điền thông tin header** — tên tester, ngày submit, version, link Sheet.
3. **Chỉnh data sample** — thay placeholder bằng data nghiệp vụ thật của môi trường test.
4. **Check lại Map to Impact** — Claude có thể map sai nếu impact mô tả mơ hồ.
5. **Bổ sung TC từ kinh nghiệm cá nhân** — Claude chỉ cover từ input, không có kinh nghiệm thực tế.

## Iterate

Nếu draft chưa đủ:
- `"F2 chỉ có 2 TC, mà F2 là Direct impact và liên quan payment — bổ sung thêm Negative case cho F2"`
- `"Bỏ TC005, TC006 — đó là case spec ngoài scope, không liên quan bug này"`
- `"Convert TC003 sang Regression thay vì Positive — vì T1 là tính năng cũ"`
- `"TC cũ #42 ở sheet cũ thật ra đã cover Negative cho F1 rồi, bỏ TC003 mới đi"`
- `"Đổi tab output thành 'KH-36202_round2'"`

## So sánh với `/review-tc`

| | /review-tc | /write-tc |
|---|---|---|
| Đối tượng | Test Leader | QA member |
| Input file | 4 file (01, 02, 03, 04) | 2-3 file (01, 03, 02 tùy chọn) |
| Output file | `05-review-report.md` | `04-tc-list.md` |
| Goal | Phát hiện gap/issue | Sinh TC bám rule ngay từ đầu |

## Khi không có Claude Code

Có thể đọc trực tiếp [.claude/commands/write-tc.md](../.claude/commands/write-tc.md), copy nội dung phần dưới frontmatter, paste vào AI khác. Nhớ thay `$ARGUMENTS` bằng đường dẫn folder review thật.
