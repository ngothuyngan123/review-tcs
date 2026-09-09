<!-- sync-target: https://docs.google.com/spreadsheets/d/1337DDgFt-zTLL4OfPg-4JUQ-jOreeiwQIOiV_5eDJIE/edit?gid=1974520139#gid=1974520139 -->
# 04 — TC List (do member viết)

> File này là **output của member**, **input của Leader**.
> TCs dưới đây được **fetch từ Google Sheet** (tab "Setting calendar", cột "Bug KH #36729"). KHÔNG sửa Title / Expected dù bug fix đổi behavior — TCs cũ là read-only cho tới khi confirm với Leader.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1337DDgFt-zTLL4OfPg-4JUQ-jOreeiwQIOiV_5eDJIE/edit?gid=1974520139#gid=1974520139 |

---

## TC List

> Fetch từ Sheet tab "Setting calendar", range A1224:N1236 (cột status = "Bug KH #36729"). Cột Type / Priority / Assignee không có trong Sheet gốc → để trống. Cột "Output note" map từ cột "Actual Result" trong Sheet.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Đăng ký nhận thông báo chờ hủy lần đầu thành công | | | User chưa có đăng ký WAIT_CANCEL cho slot A | 1. Mở màn hình Lesson Booking<br>2. Chọn slot A đã đầy<br>3. Đăng ký nhận thông báo chờ hủy | Tạo record WAIT_CANCEL (Tạo booking đợi nhận notify có status =3)<br>Gửi message chứa キャンセル用URL<br>Khi có slot trống => User nhận được thông báo | | | OK |
| TC002 | Chặn đăng ký trùng cùng slot khi đã có WAIT_CANCEL | | | User đã có WAIT_CANCEL cho slot A | 1. Truy cập lại màn hình booking<br>2. Chọn slot A<br>3. Đăng ký nhận thông báo lần nữa | Hiển thị message lỗi キャンセル待ち通知受け取りがすでに登録されています<br>Không gửi message mới; Không gửi URL mới; DB không thay đổi | | | OK |
| TC003 | Không phát sinh action/message khi đăng ký trùng | | | User đã có WAIT_CANCEL cho slot A | Thực hiện đăng ký lại slot A | Không nhận message mới; Không xuất hiện キャンセル用URL mới | | | OK |
| TC004 | Không update record WAIT_CANCEL khi đăng ký trùng | | | User có WAIT_CANCEL cho slot A | 1. Ghi nhận bookingId hiện tại<br>2. Đăng ký lại slot A | bookingId giữ nguyên; status vẫn WAIT_CANCEL; Không phát sinh update | | | OK |
| TC005 | Hủy bằng Cancel URL hợp lệ | | | User có WAIT_CANCEL hợp lệ | 1. Mở キャンセル用URL<br>2. Thực hiện hủy | Hiển thị hủy thành công; Record được cancel; Không còn nhận thông báo | Hiện tại mở detail của booking này không có nút cancel (Chỉ có nút mở sang màn booking mới) | | OK |
| TC006 | Cancel URL cũ vẫn hoạt động sau khi bị chặn đăng ký trùng | | | User có WAIT_CANCEL cho slot A | 1. Đăng ký lại slot A (bị chặn)<br>2. Mở Cancel URL ban đầu | URL cũ vẫn hủy được đăng ký; Trạng thái cập nhật chính xác | Click vào url cũ thì mở được detail của booking nhưng sẽ không có nút để cancel | | OK |
| TC007 | Đăng ký WAIT_CANCEL cho slot khác | | | User có WAIT_CANCEL cho slot A | 1. Chọn slot B<br>2. Đăng ký nhận thông báo | Đăng ký thành công; Tạo WAIT_CANCEL mới; Gửi URL tương ứng | | | OK |
| TC008 | User khác đăng ký cùng slot | | | User A có WAIT_CANCEL slot A | User B đăng ký WAIT_CANCEL slot A | User B đăng ký thành công; Sinh booking riêng | | | OK |
| TC009 | Kiểm tra nhánh bookingType='notify' | | | Có booking WAIT_CANCEL với bookingId hợp lệ | Thực hiện flow bookingType='notify'<br>- Khi slot A có slot trống => User Nhấn mở link booking và thực hiện book slot A<br>- Khi slot A có slot trống => User Nhấn mở キャンセル用URL => Nhấn nút mở sang màn booking mới và thực hiện book slot A | User book được slot A success<br>Check DB: không tạo booking mới mà sẽ update vào booking có status =3 ban đầu<br>Send được action booking mới | Bug đang bị hiện message giống case đăng ký notify trùng | | NG |
| TC010 | Đăng ký lại sau khi đã hủy | | | WAIT_CANCEL đã được hủy | 1. Hủy bằng Cancel URL<br>2. Đăng ký lại cùng slot | Đăng ký thành công; Tạo booking mới; Gửi URL mới | | | Test Bug |
| TC011 | Truy cập Cancel URL không hợp lệ | | | Có URL bị sửa bookingId hoặc token | Truy cập URL không hợp lệ | Hiển thị lỗi phù hợp; Không thay đổi dữ liệu DB | | | Test Bug |
| TC012 | Spam nhiều request đăng ký cùng slot | | | Chưa có WAIT_CANCEL | Gửi 2~5 request đăng ký cùng slot gần như đồng thời | Chỉ tạo 1 WAIT_CANCEL; Các request còn lại bị reject; Không phát sinh nhiều URL | | | Test Bug |

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

<!-- Source: fetched từ Redmine #36729 Link TCs, range A1224:N1236 tab "Setting calendar" (gid 1974520139) lúc 2026-06-02. Redmine ghi "Line 1222~1235" nhưng bug block thực tế gồm cả row 1236 (TC012 Spam request, cùng cột status "Bug KH #36729") → đã include đủ. Rows 1222 (bug header) + 1223 (Tái hiện Bug) không phải TC nên không đưa vào bảng. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
