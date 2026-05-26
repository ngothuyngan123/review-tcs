# Review TCs — hướng dẫn dùng

> File này là tài liệu cho người. Logic vận hành nằm ở slash command [/review-tc](../.claude/commands/review-tc.md).

## Cách chạy

Trong Claude Code, gõ:

```
/review-tc tasks/YYYY-MM-DD_<bug-id>_<slug>/
```

Hoặc gõ `/review-tc` không kèm folder → Claude sẽ liệt kê các folder con trong `tasks/` để bạn chọn.

## Khi nào dùng

Sau khi member đã submit `04-tc-list.md` vào folder review, Leader chạy `/review-tc` để Claude:
1. Đọc 4 file input (`01` → `04`)
2. Lập coverage matrix (impact ↔ TC)
3. Chạy [framework/review-checklist.md](../framework/review-checklist.md) + [framework/checklist-lme.md](../framework/checklist-lme.md)
4. Phân loại issues theo severity ([BLOCKER] / [MAJOR] / [MINOR] / [NIT])
5. Đề xuất TC bổ sung cho các GAP
6. Ghi `05-review-report.md` theo [template](../templates/05-review-report.template.md)

## Tiền điều kiện

Folder review phải có:
- ✅ `01-bug-task.md` (BẮT BUỘC)
- ⚠️ `02-spec-reference.md` (tùy chọn — không có thì fallback về [LME-SYSTEM-SPEC.md](../templates/LME-SYSTEM-SPEC.md))
- ✅ `03-dev-impact.md` (BẮT BUỘC)
- ✅ `04-tc-list.md` (BẮT BUỘC — do member submit)

Thiếu file bắt buộc → Claude DỪNG và yêu cầu bổ sung. Thiếu `02` → tiếp tục với note tham chiếu spec tổng.

## Tips cho Leader

1. **Không tin 100% output**: draft của Claude có thể miss nuance — luôn verify coverage matrix và đọc lại các TC bị flag `[BLOCKER]`.
2. **Iterate**: nếu draft chưa đủ sâu, hỏi tiếp:
   - `"Hãy soi kỹ hơn impact F2, tại sao chỉ có 1 TC là đủ?"`
   - `"TC003 và TC005 có trùng mục đích không?"`
   - `"Fix mục 2 là generic catch-all hay specific code-check? TCs hiện tại verify với mấy trigger condition khác nhau?"` — câu hỏi adversarial bắt buộc khi fix là error handler / validation. Xem [framework/anti-patterns.md](../framework/anti-patterns.md) AP-1.
3. **Vòng review tiếp theo**: chỉ cần báo Claude member đã fix gì, Claude re-assess thay vì chạy `/review-tc` lại từ đầu.
4. **Spec conflict**: nếu spec cũ mâu thuẫn cách fix, Claude sẽ flag mục "Spec update needed" — Leader nên xác nhận với Dev/PM trước khi approve.

## Khi không có Claude Code

Có thể đọc trực tiếp [.claude/commands/review-tc.md](../.claude/commands/review-tc.md), copy nội dung phần dưới frontmatter, paste vào AI khác. Nhớ thay `$ARGUMENTS` bằng đường dẫn folder review thật.
