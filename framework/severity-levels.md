# Severity Levels — khi review TCs

Phân loại mức độ issue phát hiện khi review. Dùng trong `05-review-report.md`.

---

## Blocker

**Định nghĩa**: TCs nếu giữ nguyên sẽ **bỏ lọt bug** ra production.

Ví dụ:
- **GAP** coverage cho bug root cause (không có TC verify fix).
- **GAP** coverage cho function `Direct` impact trong mục 4.1.
- **GAP** coverage cho tính năng `High` risk trong mục 4.3.
- TC verify **sai** expected result (không khớp spec / cách fix).
- TC phụ thuộc data/env **không tồn tại** trên môi trường test → không chạy được.

**Hành động**: member **PHẢI** fix, Leader review lại vòng 2 trước khi approve.

---

## Major

**Định nghĩa**: TCs thiếu chiều sâu, có nguy cơ bỏ lọt edge case nhưng không bỏ lọt happy path.

Ví dụ:
- Có TC cover function/data nhưng **thiếu negative hoặc boundary**.
- Không có regression test cho tính năng `Medium` risk.
- TC steps không rõ ràng, 2 người chạy có thể ra 2 kết quả khác.
- TC không atomic (1 TC verify 3 thứ khác nhau).
- Có **case thừa** / lạc chủ đề (ORPHAN trong coverage matrix).

**Hành động**: member **NÊN** fix, có thể approve nếu priority gấp + Leader approve exception.

---

## Minor

**Định nghĩa**: Vấn đề hình thức, không ảnh hưởng coverage.

Ví dụ:
- Title TC chung chung.
- Sai format TC ID.
- Data sample không realistic (`"test"`, `"abc"`).
- Thiếu precondition chi tiết nhưng có thể infer.
- Priority gán chưa hợp lý.

**Hành động**: ghi vào report, member tự fix trong version tiếp theo. Không block approval.

---

## Nit (Nitpick)

**Định nghĩa**: Gợi ý cải thiện, không bắt buộc.

Ví dụ:
- Đề xuất cách chia TC khác gọn hơn.
- Đề xuất thêm TC cho scenario hiếm.
- Đề xuất rename cho rõ nghĩa hơn.

**Hành động**: optional — member tham khảo.

---

## Cách ghi trong report

Format: `[SEVERITY] <TC ID hoặc "GAP-X">: <mô tả ngắn> — <đề xuất fix>`

Ví dụ:

```
[BLOCKER] GAP-1: Không có TC nào verify function `sendBroadcast` (F2 trong dev impact) — cần thêm ≥ 2 TC (positive + negative).
[MAJOR] TC005: Thiếu boundary test cho max recipients (D1) — thêm TC với 10,000 recipients.
[MINOR] TC012: Title "test function" quá chung — đổi thành "Verify broadcast stops when scheduled time is in the past".
[NIT] TC003: Có thể tách thành 2 TC riêng cho case success và case partial success.
```
