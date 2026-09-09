# Review TCs — hướng dẫn dùng

> File này là tài liệu cho người. Logic vận hành nằm ở slash command [/review-tc](../.claude/commands/review-tc.md).

## Cách chạy

Trong Claude Code, gõ:

```
/review-tc tasks/YYYY-MM-DD_<bug-id>_<slug>/
/review-tc tasks/YYYY-MM-DD_<bug-id>_<slug>/ 39667      # ép ticket Redmine
/review-tc tasks/YYYY-MM-DD_<bug-id>_<slug>/ task:94    # ép task_id trên Studio
/review-tc tasks/YYYY-MM-DD_<bug-id>_<slug>/ https://docs.google.com/spreadsheets/d/.../edit#gid=0   # ép nguồn Sheet
```

Hoặc gõ `/review-tc` không kèm folder → Claude sẽ liệt kê các folder con trong `tasks/` để bạn chọn.

## Khi nào dùng

Khi cần Leader review bộ TCs của 1 task. Claude:
0. **Tự lấy bộ TC** theo 3 nguồn ưu tiên — **dừng ở nguồn đầu tiên có TC**, không gộp, không đối chiếu chéo:
   1. **MCP LME TEST STUDIO** (`task_list` theo ticket → `testcase_list`)
   2. **Link Google Sheet do bạn cung cấp** (arg2 là URL, hoặc bạn paste link/file/bảng TC trong chat)
   3. File **`04-tc-list.md`** trong folder

   Cả 3 đều không có → Claude DỪNG và hỏi bạn gửi list TCs, KHÔNG tự viết TC.
1. Đọc input còn lại (`01` + `03`). Spec đọc thẳng từ `spec-features/<feature>` (hoặc spec ngoài **nếu bạn dán link/nội dung trực tiếp**; **không** WebFetch `lme.jp/manual`) — **không tạo file `02`**, nguồn spec in ra chat; chỉ khi **không tìm được spec** mới ghi 1 dòng `[MAJOR]` ở §4 report
2. Lập bảng coverage **2 chiều** — **(a)** ảnh hưởng Dev tự kê ở `03-dev-impact.md` mục 4 · **(b)** ảnh hưởng suy từ **diff thật**, lấy ở tab Thông tin của Studio (`task_get_context` → `dev_impact` + `spec_delta.files`/`diffStat`). Bảng là nháp nội bộ, report chỉ ghi dòng `GAP` / `RISK` vào **§1**
3. Đối chiếu bộ quan điểm 2 tầng qua **index tự sinh** — [checklist-lme.index.md](../framework/checklist-lme.index.md) (80 quan điểm) + [catalog-lme.index.md](../framework/catalog-lme.index.md) — rồi chỉ `sed` chi tiết của các mã thực sự trigger. Quan điểm ưu tiên **Cao** có Trigger khớp task mà thiếu TC → `[BLOCKER]`. Kết quả ra **§2** report — **chỉ liệt kê quan điểm còn thiếu**, quan điểm đã đủ không ghi
4. Phân loại issues theo severity ([BLOCKER] / [MAJOR] / [MINOR] / [NIT]) **+ rà TC trùng lặp nội dung** → TC trùng ra **§3** report (đề nghị xóa/gộp, Claude không tự xóa); issue chất lượng nguồn + chất lượng TC ra **§4**
5. Đề xuất TC bổ sung cho các GAP — tiêu đề §5 ghi kèm **số TC đề xuất** (`## 5. TCs đề xuất bổ sung (20)`) — **trước đó đọc TC cũ trong [kho-tcs/](../kho-tcs/)** để bắt vùng regression, phát hiện conflict expected, và không đẻ TC trùng
6. Ghi `05-review-report.md` theo [template](../templates/05-review-report.template.md)

## Tiền điều kiện

Folder review phải có:
- ✅ `01-bug-task.md` (BẮT BUỘC)
- ✅ `03-dev-impact.md` (BẮT BUỘC)
- 🔄 `04-tc-list.md` — **KHÔNG còn bắt buộc**, và là nguồn TC **cuối cùng** (sau Studio và link Sheet bạn đưa).

Thiếu `01` / `03` → Claude DỪNG và yêu cầu bổ sung (`/new-task <redmine-url>` hoặc paste tay). Thiếu `02` → tiếp tục, Claude đọc spec trong `spec-features/` (hoặc link bạn đưa trực tiếp) và ghi rõ đã dùng nguồn nào; không có spec → flag `[MAJOR]` chứ không tự bịa business rule.

## Đọc kỹ §0 của report

Khi TC lấy từ Studio, §0 "Nguồn TC" của `05-review-report.md` cho biết những thứ bảng TC không nói: bao nhiêu TC **thực sự pass** (TC `skip` không phải đã test), chạy ở env nào (RULE-08), do **AI hay QA người** viết/chạy, và mã quan điểm nào của Studio không nằm trong bộ 80 quan điểm LME (không map được coverage). Đọc mục này trước khi đọc verdict.

## Tips cho Leader

1. **Không tin 100% output**: draft của Claude có thể miss nuance — luôn verify §1 (coverage) + §2 (quan điểm) và đọc lại các TC bị flag `[BLOCKER]`. Report **chỉ ghi phần thiếu** — muốn xem ma trận đầy đủ thì hỏi thẳng Claude trong chat.
2. **Iterate**: nếu draft chưa đủ sâu, hỏi tiếp:
   - `"Hãy soi kỹ hơn impact F2, tại sao chỉ có 1 TC là đủ?"`
   - `"TC003 và TC005 có trùng mục đích không?"` — §3 đã rà tự động, nhưng bạn có thể bắt Claude soi lại 1 cặp cụ thể
   - `"Fix mục 2 là generic catch-all hay specific code-check? TCs hiện tại verify với mấy trigger condition khác nhau?"` — câu hỏi adversarial bắt buộc khi fix là error handler / validation. Xem [framework/anti-patterns.md](../framework/anti-patterns.md) AP-1.
3. **Vòng review tiếp theo**: chỉ cần báo Claude member đã fix gì, Claude re-assess thay vì chạy `/review-tc` lại từ đầu.
4. **Spec conflict**: nếu spec cũ mâu thuẫn cách fix, Claude sẽ flag mục "Spec update needed" — Leader nên xác nhận với Dev/PM trước khi approve.

## Khi không có Claude Code

Có thể đọc trực tiếp [.claude/commands/review-tc.md](../.claude/commands/review-tc.md), copy nội dung phần dưới frontmatter, paste vào AI khác. Nhớ thay `$ARGUMENTS` bằng đường dẫn folder review thật.
