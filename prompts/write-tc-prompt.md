# Write TCs — hướng dẫn dùng

> File này là tài liệu cho người. Logic vận hành nằm ở slash command [/write-tc](../.claude/commands/write-tc.md).

## Cách chạy

Trong Claude Code, gõ:

```
/write-tc tasks/YYYY-MM-DD_<bug-id>_<slug>/
```

Hoặc gõ `/write-tc` không kèm folder → Claude sẽ liệt kê các folder con trong `tasks/` để bạn chọn.

## Khi nào dùng

QA member chạy `/write-tc` khi **chưa viết TC**, muốn AI sinh draft để verify + chỉnh thay vì viết từ đầu. Mục tiêu: bám đúng coverage rule + bộ quan điểm test LME (2 tầng) ngay từ vòng 1, giảm số vòng review.

Claude sẽ:
1. Đọc bug + dev-impact. Spec đọc **chỉ** ở `spec-features/<feature>` (hoặc spec ngoài nếu bạn dán link/nội dung trực tiếp) — **không** WebFetch `lme.jp/manual`
1a. Hỏi bạn **URL Google Sheet đích** (bắt buộc, phải có `?gid=`) — nơi `/sync-tc` sẽ append TC mới
1b. Lấy **TC cũ tham chiếu** theo **3 nguồn ưu tiên**, dừng ở nguồn đầu tiên có TC: **(1)** MCP LME TEST STUDIO → **(2)** link Google Sheet bạn cung cấp → **(3)** `04-tc-list.md` sẵn có trong folder. **TC cũ read-only** — Claude không sửa, không override
2. Duyệt [tầng 1 — 80 quan điểm](../framework/checklist-lme.md), đánh ◯/× theo Trigger (× phải có lý do); với mỗi ◯ mở đúng [tầng 2 — catalog](../framework/catalog-lme.md)
3. Lập ma trận TC tối thiểu: 5 quy tắc vàng + **RULE-01** (quan điểm Cao ⇒ đủ 3 loại `Normal`/`Abnormal`/`Boundary`) + RULE-06 (output cuối chuỗi) + RULE-07 (verify 3 tầng). Reuse TC cũ nếu đã cover; KHÔNG override TC cũ
3b. **Đối chiếu [kho-tcs/](../kho-tcs/)** của tính năng trước khi viết → bắt vùng regression, phát hiện conflict expected (không tự chọn bên, cảnh báo để Leader/Dev chốt), và không viết TC trùng TC đã có trong kho
4. Sinh TC theo [template 04](../templates/04-tc-list.template.md) — **16 cột canonical** (bám sheet "7. Ví dụ test case"): `TC No.` = `TC-<mã quan điểm bỏ gạch>-<nn>`; bắt buộc có `Mã quan điểm liên kết`; `Loại case` chỉ 3 giá trị; không có Priority/Regression; `Tiêu đề test case` phải chứa keyword để Leader suy luận impact
5. Self-check coverage + **rà trùng 3 chiều** (TC mới vs nhau · vs TC cũ · vs TC kho) theo 4 yếu tố: `mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected` tương đương
6. Ghi `04-tc-list.md` (hoặc `04-tc-list.draft.md` nếu file đã tồn tại). Nếu user có chỉ định sync target → chèn HTML comment `<!-- sync-target: spreadsheet=... tab=... -->` ở đầu file để `/sync-tc` đọc.

## Tiền điều kiện

Folder review phải có:
- ✅ `01-bug-task.md` (BẮT BUỘC — không có thì DỪNG)
- ✅ `03-dev-impact.md` (BẮT BUỘC — không có thì DỪNG)
- ⚠️ Spec: Claude chỉ đọc `spec-features/<feature>` (+ spec ngoài bạn đưa link trực tiếp); không có thì TC ghi `Spec không ghi` + cảnh báo, không bịa business rule

## Input — Sheet đích + TCs cũ tham chiếu

**Sheet đích (bắt buộc)**: URL đầy đủ có `?gid=<số>` trỏ tới **tab bạn đã tạo sẵn**. `/sync-tc` append TC mới xuống dưới data hiện có của tab đó — **không tạo tab mới**.

**TCs cũ tham chiếu (để tránh sinh TC trùng)**: Claude tự lấy theo **3 nguồn ưu tiên, dừng ở nguồn đầu tiên có TC**:

| # | Nguồn | Ghi chú |
|---|---|---|
| 1 | **MCP LME TEST STUDIO** | Tự dò theo ticket trong tên folder / file 01. Task đã có TC trên Studio → Claude cảnh báo "cân nhắc `/review-tc` thay vì viết mới" |
| 2 | **Link Google Sheet bạn cung cấp** | Tab TC cũ (có thể khác Sheet đích). Sheet dạng cây `Main Function / Sub1..Sub5` có ô gộp → Claude dùng `scripts/fetch_grid.py` |
| 3 | **`04-tc-list.md` sẵn có trong folder** | TC round trước / member viết tay |

Ngoài ra Claude **luôn đối chiếu [kho-tcs/](../kho-tcs/)** của tính năng (không phải nguồn TC cũ — là kho chuẩn để bắt regression + conflict expected).

**TC cũ và TC kho đều READ-ONLY** — Claude KHÔNG sửa, KHÔNG override dù BUG fix có đổi behavior. Phát hiện TC cũ có vẻ sai sau fix → chỉ ghi cảnh báo cho member tự verify thủ công.

Khi Claude hỏi ở Bước 1.4a, chuẩn bị:
1. **Link spreadsheet** — paste URL đầy đủ (vd `https://docs.google.com/spreadsheets/d/ABC123XYZ/edit#gid=0`) hoặc chỉ Sheet ID (`ABC123XYZ`).
2. **Tên tab TC cũ** — vd `Broadcast TCs v2`. Không nhớ → Claude sẽ liệt kê tab cho chọn.
3. **Range TC cũ** *(tùy chọn)* — A1 notation, vd `A2:J100` (skip header) hoặc `A:J` (cả cột). **Để trống → đọc toàn bộ sheet.**
4. **URL Sheet đích** phải có `?gid=` trỏ đúng tab đã pre-create — thiếu `gid` thì Claude DỪNG (không chạy được `/sync-tc` sau này).

Sheet phải đã share **Editor** với service account email trong `credentials/google-service-account.json` (field `client_email`). Setup chi tiết: [docs/MCP-SETUP.md](../docs/MCP-SETUP.md).

Không có TCs cũ ở Sheet → Claude vẫn thử Studio (nguồn 1) và file 04 sẵn có (nguồn 3).

Sau khi bạn cung cấp, Claude lưu vào HTML comment ở **dòng đầu** `04-tc-list.md`:
```html
<!-- sync-target: https://docs.google.com/spreadsheets/d/ABC123XYZ/edit?gid=2004892297 -->
```
`/sync-tc` đọc comment này, parse `spreadsheet_id` + `gid` và append vào đúng tab — không cần truyền args lại.

## Sau khi Claude sinh xong — member BẮT BUỘC verify

1. **Đọc lại từng TC** — Claude có thể bịa precondition không khả thi, hoặc steps thiếu chi tiết domain.
2. **Điền thông tin header** — tên tester, ngày submit, version, link Sheet.
3. **Chỉnh data sample** — thay placeholder bằng data nghiệp vụ thật của môi trường test.
4. **Check lại `Mã quan điểm liên kết` + mapping impact** — Claude có thể map sai nếu impact mô tả mơ hồ.
5. **Check `Trạng thái đánh giá spec`** — case `Spec không ghi` phải thật sự đã hỏi leader/PM, không để Claude tự suy diễn.
6. **Bổ sung TC từ kinh nghiệm cá nhân** — Claude chỉ cover từ input, không có kinh nghiệm thực tế.

## Iterate

Nếu draft chưa đủ:
- `"F2 chỉ có 2 TC, mà F2 là Direct impact và liên quan payment — bổ sung thêm Abnormal case cho F2"`
- `"Bỏ TC-PERM002-02, TC-PERM002-03 — đó là case spec ngoài scope, không liên quan bug này"`
- `"TC-FUNC001-03 nên là Boundary thay vì Normal — vì đang test giá trị biên"`
- `"TC cũ #42 ở sheet cũ thật ra đã cover Abnormal cho F1 rồi, bỏ TC mới đi"`
- `"TC-MSG002-02 và TC-MSG002-04 trùng ý định — gộp làm 1"`
- `"Kho FA-012 đã có TC-TAG-118 cover case này rồi, dẫn chiếu thay vì viết mới"`

## So sánh với `/review-tc`

| | /review-tc | /write-tc |
|---|---|---|
| Đối tượng | Test Leader | QA member |
| Input file | 01 + 03 (+02 tùy chọn) + **bộ TC cần review** (Studio → Sheet → file 04) | 01 + 03 (+02 tùy chọn) + **TC cũ tham chiếu** (Studio → Sheet → file 04) |
| Đối chiếu `kho-tcs/` | Trước khi đề xuất TC bổ sung (BƯỚC 5a) | Trước khi sinh TC (BƯỚC 3f) |
| Rà TC trùng | TC trong nguồn → §3 report, đề nghị xóa/gộp | TC mới vs nhau / vs TC cũ / vs kho → không sinh TC trùng |
| Output file | `05-review-report.md` | `04-tc-list.md` |
| Goal | Phát hiện gap/issue | Sinh TC bám rule ngay từ đầu |

## Khi không có Claude Code

Có thể đọc trực tiếp [.claude/commands/write-tc.md](../.claude/commands/write-tc.md), copy nội dung phần dưới frontmatter, paste vào AI khác. Nhớ thay `$ARGUMENTS` bằng đường dẫn folder review thật.
