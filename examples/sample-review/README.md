# Sample Review — LME-2054 (Scheduled broadcast không gửi đủ recipients)

Đây là ví dụ mẫu đầy đủ của 1 lần review TC, bao gồm:

- [01-bug-task.md](01-bug-task.md) — bug của khách hàng (PM Tanaka, salon ABC)
- ~~[02-spec-reference.md](02-spec-reference.md)~~ — ⚠️ **LEGACY**: file `02` đã bỏ khỏi bộ chuẩn (2026-08-28). Giữ lại làm ví dụ lịch sử; folder review mới chỉ có `01` · `03` · `04` · `05`, spec đọc thẳng từ `spec-features/`
- [03-dev-impact.md](03-dev-impact.md) — Dev Nguyễn Văn A đánh giá impact với 5 function, 4 data, 5 feature
- [04-tc-list.md](04-tc-list.md) — Tester Trần Thị B viết 8 TCs (v1)
- [05-review-report.md](05-review-report.md) — report **rút gọn**: 3 GAP + 2 RISK coverage, 2 quan điểm thiếu, 1 nhóm TC trùng, 5 TC đề xuất bổ sung

## Điểm để học từ ví dụ

1. **§1 + §2 chỉ liệt kê phần thiếu** — 3 GAP + 2 RISK coverage và 2 quan điểm chưa cover đủ, thứ nhìn qua 8 TC không thấy rõ. Ma trận đầy đủ vẫn được lập ở BƯỚC 2/3 nhưng không ghi vào file, nên Leader đọc hết report trong 1 phút.
2. **Self-check của member** (cuối file 04) đã note thiếu 3 mục — Leader dùng luôn điểm này để coach.
3. **TC đề xuất bổ sung** trong report đủ chi tiết để member copy vào v2 mà không cần hỏi lại.
4. **Spec OK** — không phải mọi bug đều cần update spec, chỉ flag khi cần.

## Dùng làm template cho review mới

```bash
# Từ thư mục gốc project
cp -r examples/sample-review tasks/2026-04-23_LME-xxxx_<tên-bug>
# Sau đó mở folder mới và replace nội dung
```
