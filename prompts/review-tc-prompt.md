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
1. Đọc input còn lại (`01` + `03`). Spec đọc thẳng từ `spec-features/<feature>` (hoặc spec ngoài **nếu bạn dán link/nội dung trực tiếp**; **không** WebFetch `lme.jp/manual`) — **không tạo file `02`**, nguồn spec in ra chat; chỉ khi **không tìm được spec** mới ghi 1 dòng `[MAJOR]` ở §5 report
2. Lập bảng coverage **2 chiều** — **(a)** ảnh hưởng Dev tự kê ở `03-dev-impact.md` mục 4 · **(b)** ảnh hưởng suy từ **diff thật**, lấy ở tab Thông tin của Studio (`task_get_context` → `dev_impact` + `spec_delta.files`/`diffStat`). Bảng là nháp nội bộ; **§1** mở đầu bằng **2 dòng trả lời ĐỦ / CHƯA ĐỦ** cho từng chiều, rồi bảng các dòng `GAP` / `RISK`
3. Đối chiếu bộ quan điểm 2 tầng qua **index tự sinh** — [checklist-lme.index.md](../framework/checklist-lme.index.md) (80 quan điểm) + [catalog-lme.index.md](../framework/catalog-lme.index.md) — rồi chỉ `sed` chi tiết của các mã thực sự trigger. Quan điểm ưu tiên **Cao** có Trigger khớp task mà thiếu TC → `[BLOCKER]`. Kết quả ra **§2** report — **chỉ liệt kê quan điểm còn thiếu**, quan điểm đã đủ không ghi
4. Rà **trùng lặp** → **§3** · rà **mâu thuẫn** (`CONF-TC` 2 TC expected loại trừ nhau · `CONF-SPEC` trái `spec-features/` · `CONF-KHO` trái `kho-tcs/`) → **§4** + **§8** · issue chất lượng nguồn + chất lượng TC → **§5** · **TC thừa / ngoài phạm vi task** → **§6**. Claude **không tự xóa** TC nào, chỉ đề nghị
5. Đề xuất TC bổ sung từ **3 nguồn**: `G<x>` (GAP/RISK §1 — bắt buộc có TC) · `Q<x>` (§2) · **`R<x>` regression theo đánh giá của AI** (căn cứ: rủi ro hồi quy Studio / `<ID kho>` / caller hàm dùng chung). Tiêu đề §7 ghi kèm **số TC đề xuất** (`## 7. TCs đề xuất bổ sung (20)`) — **trước đó đọc TC cũ trong [kho-tcs/](../kho-tcs/)** để bắt vùng regression và không đẻ TC trùng
6. Ghi `05-review-report.md` theo [template](../templates/05-review-report.template.md)

## Tiền điều kiện

Folder review phải có:
- ✅ `01-bug-task.md` (BẮT BUỘC)
- ✅ `03-dev-impact.md` (BẮT BUỘC)
- 🔄 `04-tc-list.md` — **KHÔNG còn bắt buộc**, và là nguồn TC **cuối cùng** (sau Studio và link Sheet bạn đưa).

Thiếu `01` / `03` → Claude DỪNG và yêu cầu bổ sung (`/new-task <redmine-id>` hoặc paste tay). Thiếu `02` → tiếp tục, Claude đọc spec trong `spec-features/` (hoặc link bạn đưa trực tiếp) và ghi rõ đã dùng nguồn nào; không có spec → flag `[MAJOR]` chứ không tự bịa business rule.

## Đọc kỹ §0 của report

§0 "Nguồn TC" chỉ có **2 dòng**: nguồn đã dùng (Studio task #`<id>` / Sheet / `04-tc-list.md`) + tổng số TC review — đọc để biết report đang nói về bộ TC nào. Cảnh báo chất lượng nguồn (bao nhiêu TC **thực sự pass** — TC `skip` không phải đã test, chạy ở env nào theo RULE-08, TC `fail` chưa raise ticket) nằm ở **§5**.

## Tips cho Leader

1. **Không tin 100% output**: draft của Claude có thể miss nuance — luôn verify §1 (coverage — 2 dòng ĐỦ/CHƯA ĐỦ) + §2 (quan điểm) + §4 (mâu thuẫn) và đọc lại các TC bị flag `[BLOCKER]`. Report **chỉ ghi phần thiếu** — muốn xem ma trận đầy đủ thì hỏi thẳng Claude trong chat.
2. **Iterate**: nếu draft chưa đủ sâu, hỏi tiếp:
   - `"Hãy soi kỹ hơn impact F2, tại sao chỉ có 1 TC là đủ?"`
   - `"TC003 và TC005 có trùng mục đích không?"` — §3 đã rà tự động, nhưng bạn có thể bắt Claude soi lại 1 cặp cụ thể
   - `"Fix mục 2 là generic catch-all hay specific code-check? TCs hiện tại verify với mấy trigger condition khác nhau?"` — câu hỏi adversarial bắt buộc khi fix là error handler / validation. Xem [framework/anti-patterns.md](../framework/anti-patterns.md) AP-1.
3. **Vòng review tiếp theo**: chỉ cần báo Claude member đã fix gì, Claude re-assess thay vì chạy `/review-tc` lại từ đầu.
4. **Spec conflict**: nếu spec cũ mâu thuẫn cách fix, Claude sẽ flag mục "Spec update needed" — Leader nên xác nhận với Dev/PM trước khi approve.

## Khi không có Claude Code

Có thể đọc trực tiếp [.claude/commands/review-tc.md](../.claude/commands/review-tc.md), copy nội dung phần dưới frontmatter, paste vào AI khác. Nhớ thay `$ARGUMENTS` bằng đường dẫn folder review thật.
