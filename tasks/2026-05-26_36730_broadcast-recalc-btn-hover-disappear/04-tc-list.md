<!-- sync-target: https://docs.google.com/spreadsheets/d/19DOC70E0bj9UCYkndtZCJcaHuJnHmyCaqRnIXaMvAY4/edit?gid=0#gid=0 -->
# 04 — TC List (do member viết)

> ⚠️ Fetched từ Redmine #36730 Link TCs — TCs gốc do Dev (Kim Cúc / Kieu Son Tung) draft sẵn. **KHÔNG sửa nội dung** nếu chưa confirm với Leader.
>
> ⚠️ **Format gốc khác chuẩn 10-col của team** — source dùng layout phân cấp (Tab > Scenario > Filter variant > Precondition > Note). Mapping tạm:
> - **Title** ← col A source (Tab context, vd "Check ở tab: 配信予約")
> - **Type** ← col B source (Scenario group, vd "Tạo send all send ngay")
> - **Priority** ← col C source (Filter variant, vd "Không filter" / "Có filter")
> - **Precondition** ← col D source (Precondition / steps tóm tắt)
> - **Steps** ← col E source (Note phụ — thường là "check khi send broadcast cho user")
> - Expected / Output / Assignee / Status: trống — member fill khi viết lại theo chuẩn team.
>
> ⚠️ URL `sync-target` ở dòng đầu giữ nguyên `gid=0` từ Redmine — nhưng data thực fetch từ tab **"Improver send all(task broadcast)"** (gid ≠ 0). Member cần resolve gid đúng trước khi `/sync-tc` push, kẻo append nhầm sheet.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` (gốc: Kim Cúc / Dev draft) |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | v1 (draft fetch từ Sheet) |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/19DOC70E0bj9UCYkndtZCJcaHuJnHmyCaqRnIXaMvAY4/edit?gid=0#gid=0 (range A927:J950, tab "Improver send all(task broadcast)") |

---

## Context fetch từ source (rows 927-928, KHÔNG phải TC — Dev paste làm header)

**Row 927 (Bug header)**:
> Bug KH #36730: [25-05-2026][28274][Broadcast] Tab Đặt lịch phân phối (配信予約): nút 「配信数を再計算するボタン」 biến mất khi di cursor
> 1. Nguyên nhân — style top của popover bị sai
> 2. Cách fix — sửa lại style sop
> 4.1 List function liên quan — `public/css/send_all.css`
> 4.2 List data update — k có
> 4.3 Tính năng có thể bị ảnh hưởng — màn hình list send all (đợi send, draft)

**Row 928 (Tái hiện case KH)**:
> 1. Tạo send all hiển thị ở tab 配信予約
> 2. Ở màn list, hover vào số friend sẽ nhận được Broadcast đã tạo
> Hiện tượng: không thể click vào button 現時点での配信予定数を再計算

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Check ở tab: 配信予約 | Tạo send all send ngay | Không filter | 1. tạo thành công<br>2. check ở màn list | | | | | |
| TC002 | | | | | check khi send broadcast cho user | | | | |
| TC003 | | | Có filter | 1. tạo thành công<br>2. check ở màn list | | | | | |
| TC004 | | | | | check khi send broadcast cho user | | | | |
| TC005 | | Tạo send all đặt lịch | Không filter | 1. tạo thành công<br>2. check ở màn list | | | | | |
| TC006 | | | | | check khi send broadcast cho user | | | | |
| TC007 | | | Có filter | 1. tạo thành công<br>2. check ở màn list | | | | | |
| TC008 | | | | | check khi send broadcast cho user | | | | |
| TC009 | | Check khi click vào friend | | | | | | | |
| TC010 | | Check copy broadcast | | | | | | | |
| TC011 | Check ở tab: 下書き | Tạo send all send ngay | Không filter | 1. tạo thành công<br>2. check ở màn list | | | | | |
| TC012 | | | | | check khi send broadcast cho user | | | | |
| TC013 | | | Có filter | 1. tạo thành công<br>2. check ở màn list | | | | | |
| TC014 | | | | | check khi send broadcast cho user | | | | |
| TC015 | | Tạo send all đặt lịch | Không filter | 1. tạo thành công<br>2. check ở màn list | | | | | |
| TC016 | | | | | check khi send broadcast cho user | | | | |
| TC017 | | | Có filter | 1. tạo thành công<br>2. check ở màn list | | | | | |
| TC018 | | | | | check khi send broadcast cho user | | | | |
| TC019 | | Check khi click vào friend | | | | | | | |
| TC020 | | Check copy broadcast | | | | | | | |
| TC021 | check account staff | Account staff có quyền broadcast: click/hover vào hiển thị được thông tin thao tác send all | 1. Bot có 1 staff được phân quyền broadcast | Staff login → mở broadcast→ hover ở số friend→ thao tác được button | | | | | |
| TC022 | | Account staff không quyền broadcast | Bot có 1 staff KHÔNG được phân quyền broadcast. | Staff login → cố access URL form detail → kiểm tra hiển thị / redirect. | | | | | |

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

<!-- Source: fetched từ Redmine #36730 Link TCs, range A927:J950 tab "Improver send all(task broadcast)" lúc 2026-05-26. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
