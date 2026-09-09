<!-- sync-target: https://docs.google.com/spreadsheets/d/1l5_kwyl9ny_8XRUTwxFr05VUdhkYk_z4UcYvuKOxNug/edit?gid=943868485#gid=943868485 -->
# 04 — TC List (do member viết)

> Fetch từ Redmine #37606 Link TCs. Sheet gốc dạng **bảng phân cấp** (Main Function > Sub1 > Sub2 > Sub3), đã convert sang 10 cột chuẩn. Title = đường dẫn phân cấp, giữ nguyên Expected/Status từ cell gốc.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1l5_kwyl9ny_8XRUTwxFr05VUdhkYk_z4UcYvuKOxNug/edit?gid=943868485#gid=943868485 (tab "test fix bug", rows 229–243) |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Friend info select — mở trường Lựa chọn 「予約済みのプラン」 có lựa chọn gắn action_id bị xóa — case không xóa hết action_id: **xóa action đầu tiên** | | | | Mở trường Lựa chọn có nhiều action; xóa **action đầu tiên** (còn action khác); mở detail friend info | - Màn không được báo lỗi, hiển thị detail friend info<br>- Không hiển thị action_id đó tại màn detail nữa<br>- Hiển thị các action_id đang tồn tại bình thường | | | OK |
| TC002 | Friend info select — case không xóa hết action_id: **xóa action giữa** | | | | Xóa **action ở giữa** (còn action khác); mở detail friend info | (như TC001) | | | OK |
| TC003 | Friend info select — case không xóa hết action_id: **xóa action cuối** | | | | Xóa **action cuối** (còn action khác); mở detail friend info | (như TC001) | | | OK |
| TC004 | Friend info select — case không xóa hết action_id: **xóa nhiều action (không xóa hết)** | | | | Xóa **nhiều action** nhưng vẫn còn action khác; mở detail friend info | (như TC001) | | | OK |
| TC005 | Friend info select — mở trường Lựa chọn có lựa chọn gắn action_id bị xóa — case **xóa hết action_id** có trong friend info | | | | Xóa **toàn bộ** action_id gắn trong friend info; mở detail friend info | - Màn không được báo lỗi, hiển thị detail friend info | | | OK |
| TC006 | Friend info select — mở trường Lựa chọn 「予約済みのプラン」 có lựa chọn **KHÔNG có action_id bị xóa** | | | | Mở trường Lựa chọn mà các action_id đều còn tồn tại; mở detail friend info | - Màn không được báo lỗi, hiển thị detail friend info<br>- Hiển thị các action_id đang tồn tại bình thường | | | OK |
| TC007 | Friend info select — **friend info không có action nào** | | | | Mở trường friend info không gắn action; mở detail friend info | - Màn không được báo lỗi, hiển thị detail friend info | | | OK |
| TC008 | Xóa action có chứa action con của friend info — **xóa tag được gắn** | | | | Steps:<br>1. Tạo tag<br>2. Tạo action dùng tag đó<br>3. Gắn action vào friend info option<br>4. Xóa tag<br>5. Detail friend info | - Action con đó bị xóa theo<br>- Màn không được báo lỗi, hiển thị detail friend info<br>- Hiển thị các action id khác bình thường (nếu có) | | | OK |
| TC009 | Xóa action có chứa action con của friend info — **xóa tag không liên quan** | | | | Steps:<br>1. Tạo tag A<br>2. Tạo action dùng tag đó<br>3. Gắn action vào friend info option<br>4. Tạo tag B => Xóa tag B<br>5. Detail friend info | - Không ảnh hưởng tới friend info<br>- Không bị clean nhầm<br>- Màn không được báo lỗi, hiển thị detail friend info | | | OK |
| TC010 | Xóa action có chứa action con của friend info — **xóa tag đang được gắn => khôi phục lại tag đó** | | | | Xóa tag đang gắn action vào friend info option → khôi phục lại tag đó; mở detail friend info | - Không ảnh hưởng tới friend info<br>- Màn không được báo lỗi, hiển thị detail friend info<br>- Không hiển thị tag đó trong detail friend info nữa | | | OK |
| TC011 | Friend info select — **2 user thao tác cùng lúc** | | | | User A: đang mở friend info<br>User B: xóa tag | - User A reload không crash<br>- Màn không được báo lỗi, hiển thị detail friend info | | | OK |
| TC012 | Check thêm các friend info khác có thể gắn action — **friend info date** | | | | Áp dụng các case trên cho trường friend info kiểu **date** | `<member điền — sheet gốc để trống>` | | | |
| TC013 | Check thêm các friend info khác có thể gắn action — **friend info point** | | | | Áp dụng các case trên cho trường friend info kiểu **point** | `<member điền — sheet gốc để trống>` | | | |
| TC014 | **Check account staff** — mở detail friend info bằng tài khoản staff | | | | Đăng nhập account staff; thực hiện flow mở detail friend info | `<member điền — sheet gốc để trống>` | | | OK |

### Chú thích cột

- **Type**:
  - `Positive` — happy path đúng theo fix
  - `Negative` — input sai / điều kiện sai, verify xử lý lỗi
  - `Boundary` — giá trị biên (min/max, null, empty, max length, race condition, multi-tab)
  - `Regression` — verify tính năng cũ không bị ảnh hưởng
- **Priority**: `High` block release nếu fail / `Medium` quan trọng nhưng có workaround / `Low` nice-to-have
- **Output note** / **Assignee** / **Status**: Status fetch từ sheet gốc; còn lại để member fill sau khi run TC.

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). Bug gốc ở Production (bot ULUM) — Dev không tái hiện được trên Dev DB, TC tập trung verify cách fix + regression cascade xóa tag.

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mark các mục đã áp dụng:

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22
- [ ] A.2 Non-function: Regression / Security / Compatibility

**§C Các tính năng chung** (task này chạm):
- [ ] C.3 Friend info
- [ ] C.4 Tag

<!-- Source: fetched từ Redmine #37606 Link TCs, tab "test fix bug" rows 229–243 (header bug ở row 229, TCs ở rows 230–243), file spreadsheet 1l5_kwyl9ny_8XRUTwxFr05VUdhkYk_z4UcYvuKOxNug lúc 2026-06-16. Sheet gốc dạng bảng phân cấp; Title đã ghép từ Main Function > Sub1 > Sub2 > Sub3. KHÔNG sửa Expected/Status. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
