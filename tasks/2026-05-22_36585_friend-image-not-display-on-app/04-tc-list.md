<!-- sync-target: https://docs.google.com/spreadsheets/d/1Pble8KLJMtMzxNyi5gLnAXr7f2hvSzDo8IACv84QKi4/edit?gid=641612048#gid=641612048 -->
# 04 — TC List (do member viết)

> File này là **output của member**, **input của Leader**.
> Member copy file này (hoặc paste từ Excel/Google Sheet) vào folder review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | v1 |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1Pble8KLJMtMzxNyi5gLnAXr7f2hvSzDo8IACv84QKi4/edit?gid=641612048#gid=641612048 (tab "Content message", row 252–272) |

---

## TC List

> Bảng TC dùng **10 cột chuẩn team**. Khi `/sync-tc` push lên Google Sheet master, cột Status sẽ có dropdown 4 giá trị: `OK` / `NG` / `Not test` / `NG -> Đã fix`.
>
> ⚠️ Source sheet ("Content message") dùng layout phân cấp **13 cột** (Assignee / Main Function / Sub1 / Sub2 / Sub3 / Sub 4 / Expect Result / Actual Result / Test result / Note / Staging / Note (staging) / Step) — không trùng 10 cột chuẩn. Mapping bên dưới: Title = Main Function › Sub1 › Sub2 (kế thừa từ row trên khi cell trống do merged cells trong Sheet gốc). Expect Result cũng kế thừa. Các cột Steps / Precondition / Type / Priority / Assignee / Status để member tự fill khi viết draft chính thức.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Check user gửi message ảnh › Hiển thị ảnh khi gửi ảnh là image (không gửi dạng file) | | | | | Hiển thị được ảnh do user gửi ở chat 1:1 | | | |
| TC002 | Check user gửi message ảnh › Hiển thị ảnh khi gửi dạng image file | | | | | Hiển thị được ảnh do user gửi ở chat 1:1 | | | |
| TC003 | Check user gửi message ảnh › Hiển thị nhiều ảnh liên tiếp | | | | | Hiển thị được ảnh do user gửi ở chat 1:1 | | | |
| TC004 | Check user gửi message ảnh › Hiển thị ảnh từ message cũ › Check các ảnh cũ khi gửi là dạng image | | | | | Hiển thị được ảnh do user gửi ở chat 1:1 | | | |
| TC005 | Check user gửi message ảnh › Hiển thị ảnh từ message cũ › Check các ảnh cũ khi gửi là dạng image file | | | | | Hiển thị được ảnh do user gửi ở chat 1:1 | | | |
| TC006 | Check user gửi message video › Hiển thị video khi gửi video thường (không gửi dạng file) | | | | | Hiển thị được video do user gửi ở chat 1:1. Click vào video thì play được bình thường | | | |
| TC007 | Check user gửi message video › Hiển thị video khi gửi dạng video file | | | | | Hiển thị được video do user gửi ở chat 1:1. Click vào video thì play được bình thường | | | |
| TC008 | Check user gửi message video › Hiển thị nhiều video liên tiếp | | | | | Hiển thị được video do user gửi ở chat 1:1. Click vào video thì play được bình thường | | | |
| TC009 | Check user gửi message video › Hiển thị video từ message cũ › Check các video cũ khi gửi là dạng video thường | | | | | Hiển thị được video do user gửi ở chat 1:1. Click vào video thì play được bình thường | | | |
| TC010 | Check user gửi message video › Hiển thị video từ message cũ › Check các video cũ khi gửi là dạng file | | | | | Hiển thị được video do user gửi ở chat 1:1. Click vào video thì play được bình thường | | | |
| TC011 | Check user gửi message audio › Hiển thị audio khi gửi audio thường (không gửi dạng file) | | | | | Hiển thị được audio do user gửi ở chat 1:1. Click vào audio thì play được bình thường | | | |
| TC012 | Check user gửi message audio › Hiển thị audio khi gửi dạng file | | | | | Hiển thị được audio do user gửi ở chat 1:1. Click vào audio thì play được bình thường | | | |
| TC013 | Check user gửi message audio › Hiển thị nhiều audio liên tiếp | | | | | Hiển thị được audio do user gửi ở chat 1:1. Click vào audio thì play được bình thường | | | |
| TC014 | Check user gửi message audio › Hiển thị audio từ message cũ › Check các audio cũ khi gửi là dạng audio thường | | | | | Hiển thị được audio do user gửi ở chat 1:1. Click vào audio thì play được bình thường | | | |
| TC015 | Check user gửi message audio › Hiển thị audio từ message cũ › Check các audio cũ khi gửi là dạng file | | | | | Hiển thị được audio do user gửi ở chat 1:1. Click vào audio thì play được bình thường | | | |
| TC016 | Check send các loại file khác không bị ảnh hưởng (pdf, docx) › check user gửi file mới đến bot | | | | | | | | |
| TC017 | Check send các loại file khác không bị ảnh hưởng (pdf, docx) › check các message file cũ | | | | | | | | |
| TC018 | Check các message type khác vẫn hiển thị bình thường › message type text, sticker, location, button, media do bot send cho user | | | | | Hiển thị được toàn bộ message của user và bot được bình thường | | | |
| TC019 | Check trên cả 2 loại máy android và ios | | | | | | | | |

### Chú thích cột

- **Type**:
  - `Positive` — happy path đúng theo fix
  - `Negative` — input sai / điều kiện sai, verify xử lý lỗi
  - `Boundary` — giá trị biên (min/max, null, empty, max length, race condition, multi-tab)
  - `Regression` — verify tính năng cũ không bị ảnh hưởng
- **Priority**:
  - `High` — block release nếu fail
  - `Medium` — quan trọng nhưng có workaround
  - `Low` — nice-to-have
- **Output note** / **Assignee** / **Status**: để trống khi sinh draft. QA fill sau khi run TC.

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). Trường hợp đặc biệt:
- `Dev` (`form.watermeru.com`) — dùng khi test sớm / verify source code / reproduce timing race condition
- `Production` (`step.lme.jp`) — chỉ smoke test sau deploy, **tránh** test tạo/xoá data thật

Nếu TC nào cần env khác Staging → ghi vào cột **Output note** hoặc **Precondition**.

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify (Title / Steps đủ rõ để Leader nhận ra TC nào cover impact nào)
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover (tên function / table / màn hình)

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mark các mục đã áp dụng (chỉ những mục **liên quan** đến task này):

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22 (chọn mục liên quan task)
- [ ] A.2 Non-function: URLs đo lường / Regression / Security / Compatibility

**§B Checklist job**:
- [ ] B.1 Job callback (nếu chạm callback)
- [ ] B.2 Job sync Java — CLJ01 (nếu chạm Google sync)

**§C Các tính năng chung** (chọn feature mà task chạm đến):
- [ ] C.1 Bill tiền
- [ ] C.2 Send message (12 job + 7 web + 4 app)
- [ ] C.3 Friend info
- [ ] C.4 Tag
- [ ] C.5 Google sheet
- [ ] C.6 Google calendar
- [ ] C.7 Plan limits
- [ ] C.8 Sort

<!-- Source: fetched từ Redmine #36585 Link TCs, range A252:M272 tab "Content message" (sheet_id 641612048) lúc 2026-05-22. Section C trong Redmine ghi "line 252" (không có range end) — /new-task suy luận range = row 252 (bug header) → row 272 (TC cuối "Check trên cả 2 loại máy android và ios "). Source dùng layout phân cấp 13 cột, mapping sang 10 cột chuẩn team kế thừa Main Function + Expect Result từ row trên khi cell trống (do merged cells). KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
