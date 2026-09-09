# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39642 — [Friend info + Salon + Lesson] Validate nếu nhập label option trả lời giống nhau thì báo lỗi` |
| Redmine URL | https://redmine.watermelon.vn/issues/39642 |
| Auto-filled | `2026-09-04 by /new-task` |
| Ngày báo cáo | `2026-08-13` |
| Khách hàng / PM báo | Kim Cúc |
| Module / Màn hình | Friend Information (FA-015) · Salon Booking (FA-020) · Lesson/Calendar Booking (FA-019) — suy từ subject + mục 4.3 của đánh giá dev. Redmine KHÔNG có field `category`. |
| Priority | `Medium` (Redmine priority = `Normal`) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>` |

**Metadata Redmine bổ sung (không có trong template gốc — để Leader nắm bối cảnh):**

| Trường | Giá trị |
|---|---|
| Tracker | `Triển khai ngang` — **không phải ticket bug tái hiện**, mà là yêu cầu nhân bản validate đã có ở Biểu mẫu sang 3 màn còn thiếu |
| Status | `Fix done - Đợi test` |
| Assignee hiện tại | Ngô Thúy Ngần (chuyển từ AI LME Fix bug ngày 2026-08-25) |
| Done ratio | 100% |
| Commit Date (custom field) | 2026-08-18 |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Friend info:
Msg lỗi: 選択肢が重複しています。異なる値を入力してください。

Apply các loại info:
Select
Point

Validate nếu nhập label option trả lời giống nhau thì báo lỗi: 選択肢の表示名が重複しています。異なる値を入力してください。
1. Apply các loại item của form:
Radio
Droplist
Checkbox
Remind
Chẩn đoán
Giới tính

2. Apply các loại item của salon và lesson:
Radio
Droplist
Checkbox
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket dạng Triển khai ngang, mô tả yêu cầu chứ không mô tả cách tái hiện. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- `Friend info- validate-value.png` — https://redmine.watermelon.vn/attachments/download/29046/Friend%20info-%20validate-value.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

**Bối cảnh thêm (từ Redmine, không phải suy diễn):**

- Ticket là **triển khai ngang (横展開)**: validate chặn trùng đã tồn tại sẵn ở màn Biểu mẫu (fix gốc `public/js/form_answer/v3/setting_form_items.js`), nay nhân bản sang 3 màn chưa có: Friend info, Salon booking, Lesson booking.
- **2 thông báo lỗi KHÁC NHAU theo màn** — dễ nhầm khi viết/review TC:
  - Friend info → `選択肢が重複しています。異なる値を入力してください。`
  - Salon + Lesson → `選択肢の表示名が重複しています。異なる値を入力してください。`
- Description liệt kê **mục 1 (các loại item của Form)** nhưng Dev kết luận phần Form **đã có fix gốc, không sửa code** — TCs cho phần Form là **regression verify**, không phải verify fix mới.
- Ticket do **AI Auto-fixbug** xử lý (journal 2026-08-18), không phải dev người.
