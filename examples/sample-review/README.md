# Sample Review — LME-2054 (Scheduled broadcast không gửi đủ recipients)

Đây là ví dụ mẫu đầy đủ của 1 lần review TC, bao gồm:

- [01-bug-task.md](01-bug-task.md) — bug của khách hàng (PM Tanaka, salon ABC)
- [02-spec-reference.md](02-spec-reference.md) — trích Broadcast Spec v2.3 section 3.2 & 3.5
- [03-dev-impact.md](03-dev-impact.md) — Dev Nguyễn Văn A đánh giá impact với 5 function, 4 data, 5 feature
- [04-tc-list.md](04-tc-list.md) — Tester Trần Thị B viết 8 TCs (v1)
- [05-review-report.md](05-review-report.md) — Leader Lê Thị C review: **REJECTED**, cần bổ sung 5 TCs

## Điểm để học từ ví dụ

1. **Coverage matrix** trong report phát hiện 3 GAP + 3 RISK mà nhìn qua 8 TCs không thấy rõ.
2. **Self-check của member** (cuối file 04) đã note thiếu 3 mục — Leader dùng luôn điểm này để coach.
3. **TC đề xuất bổ sung** trong report đủ chi tiết để member copy vào v2 mà không cần hỏi lại.
4. **Spec OK** — không phải mọi bug đều cần update spec, chỉ flag khi cần.

## Dùng làm template cho review mới

```bash
# Từ thư mục gốc project
cp -r examples/sample-review tasks/2026-04-23_LME-xxxx_<tên-bug>
# Sau đó mở folder mới và replace nội dung
```
