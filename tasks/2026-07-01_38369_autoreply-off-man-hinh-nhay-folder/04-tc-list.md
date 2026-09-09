<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1tDhs4pzTa61-FqtDIh9e0KNkjYomAvOKks7u7sy3E3s/edit?gid=980379112#gid=980379112 | sheet=Ver1.0 | anchor=Main Function -->

# 04 — TC List (fetch từ Redmine #38369 Link TCs)

> ⚠️ TCs dưới đây **fetch nguyên văn** từ Google Sheet do Kim Cúc gắn trong Redmine — **read-only**, KHÔNG sửa expected/title dù bug fix đổi behavior, chưa confirm với Leader thì không chỉnh.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `Kim Cúc` (nguồn Sheet) |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1tDhs4pzTa61-FqtDIh9e0KNkjYomAvOKks7u7sy3E3s/edit?gid=980379112#gid=980379112 (tab `Ver1.0`, dòng 108-120) |

---

## TC List

> Nguồn Sheet gộp TC theo **Main Function** (cột B). Cột "Title" dưới đây = `[Main Function] Case`. Cột A của Sheet trống → TC ID sinh tuần tự (`TC001`…) để tham chiếu; giữ nguyên Steps/Expected.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | [Check auto reply trong folder tự tạo] OFF Auto Reply trong folder thường | | | | 1. Tạo ≥2 folder (A, B).<br>2. Mở folder A.<br>3. OFF một auto trong folder A. | - Sau khi nhấn OFF vẫn ở tại màn folder A<br>- Sau khi reload danh sách vẫn ở folder A, không nhảy sang "未分類". | | | |
| TC002 | [Check auto reply trong folder tự tạo] ON Auto Reply trong folder thường | | | | 1. Mở folder A.<br>2. ON một auto. | - Sau khi nhấn ON vẫn ở tại màn folder A<br>- Sau khi reload danh sách vẫn ở folder A, không nhảy sang "未分類". | | | |
| TC003 | [Check auto reply trong folder tự tạo] Folder có nhiều Auto Reply | | | | OFF auto reply | - Sau khi nhấn OFF vẫn ở tại màn folder A<br>- Sau khi reload danh sách vẫn ở folder A, không nhảy sang "未分類". | | | |
| TC004 | [Check auto reply trong folder tự tạo] ON/OFF nhiều liên tiếp | | | | ON/OFF nhiều liên tục trong cùng folder. | - Không lần nào bị chuyển sang folder khác. | | | |
| TC005 | [Check auto reply trong folder tự tạo] Refresh sau khi OFF | | | | OFF autoreply → F5. | Folder đang mở và trạng thái rule hiển thị đúng. | | | |
| TC006 | [Check auto reply trong folder tự tạo] Edit folder | | | | Đổi tên folder đang mở. | Sau khi lưu vẫn ở folder vừa chỉnh sửa. | | | |
| TC007 | [Check auto reply trong folder tự tạo] Cancel Sort | | | | Vào chế độ sort → Cancel. | Quay về đúng folder đang mở trước đó. | | | |
| TC008 | [Check auto reply trong folder tự tạo] Sort => On/OFF auto reply | | | | | - hiển thị folder đang mở và trạng thái rule hiển thị đúng | | | |
| TC009 | [Check auto reply trong folder default] OFF trong folder "未分類" | | | | | - Sau khi nhấn OFF vẫn ở tại màn folder default | | | |
| TC010 | [Check auto reply trong folder default] ON trong folder "未分類" | | | | | - Sau khi nhấn ON vẫn ở tại màn folder default | | | |
| TC011 | [Check auto reply trong folder default] Add folder mới | | | | Đang ở folder A → Thêm folder mới. | Sau khi thêm, folder đang mở xử lý đúng theo spec (không tự nhảy về 未分類). | | | |
| TC012 | [Check send auto reply được bình thường] | | | | | - user nhận được action bình thường | | | |
| TC013 | [Check account staff] | | | | | | | | |

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

<!-- Source: fetched từ Redmine #38369 Link TCs (journal Kim Cúc), range A108:J120 tab "Ver1.0" (gid 980379112 — resolve theo nội dung data khớp, list_sheets không trả sheetId) lúc 2026-07-01. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
