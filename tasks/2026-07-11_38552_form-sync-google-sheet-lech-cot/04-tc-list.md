<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4/edit?gid=806554565#gid=806554565 | sheet=Sync google | anchor=Main Function -->
<!-- sync-target: https://docs.google.com/spreadsheets/d/1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4/edit?gid=806554565#gid=806554565 -->

# 04 — TC List (do member viết)

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` (fetch từ Sheet, chưa qua vòng review nào) |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4/edit?gid=806554565#gid=806554565 — tab `Sync google`, rows 439–465 |

---

## TC List

> Fetch nguyên văn từ Google Sheet. Cột **Type** / **Priority** / **Assignee** không tồn tại trên sheet gốc → để trống (KHÔNG suy đoán). Cột **Status** lấy từ cột `Bug KH #38552 07/2026`.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC01 | Verify sync lần đầu lên Google Sheet | | | Form mới, chưa có dữ liệu trên Google Sheet | 1. Tạo form.<br>2. Link Google Sheet.<br>3. Submit form lần đầu. | Header được tạo đúng, dữ liệu ghi từ cột A. | | | OK |
| TC02 | Verify append trên sheet đã có dữ liệu | | | Google Sheet đã có ít nhất 1 dòng dữ liệu | Submit thêm một câu trả lời mới. | Dòng mới được append từ cột A, không bị lệch cột. | | | OK |
| TC03 | Verify nhiều lần submit liên tiếp | | | Google Sheet đã có dữ liệu | Submit liên tiếp nhiều lần. | Mỗi submit tạo đúng 1 dòng mới, không lệch cột. | | | OK |
| TC04 | Verify dữ liệu cũ không bị thay đổi | | | Google Sheet đã có nhiều dòng | Submit thêm dữ liệu. | Chỉ thêm dòng mới, dữ liệu cũ giữ nguyên. | | | OK |
| TC05 | Verify form có nhiều loại câu hỏi | | | Form gồm Text, Radio, Checkbox, Select, Textarea... | Submit đầy đủ dữ liệu. | Dữ liệu hiển thị đúng theo từng cột. | | | OK |
| TC06 | Verify fix bug khi thêm câu hỏi mới và có câu trả lời để trống | | | Form đã sync Google Sheet | 1. Tạo form.<br>2. Submit lần 1.<br>3. Edit form thêm câu hỏi.<br>4. Submit lần 2, để trống 1 câu hỏi mới.<br>5. Submit lần 3. | Lần submit thứ 3 không bị lệch cột, các ô trống vẫn đúng vị trí. | | | OK |
| TC07 | Verify nhiều câu hỏi mới đều để trống | | | Form đã thêm nhiều câu hỏi | Thực hiện như TC06 nhưng để trống nhiều câu hỏi liên tiếp. | Các ô trống được giữ đúng vị trí, không làm lệch dữ liệu các cột phía sau. | | | OK |
| TC08 | Verify tất cả câu hỏi mới đều có dữ liệu | | | Form đã thêm câu hỏi | Submit đầy đủ dữ liệu nhiều lần. | Không phát sinh lệch cột. | | | OK |
| TC09 | Verify chèn câu hỏi vào giữa form | | | Form đã có dữ liệu | Chèn câu hỏi vào giữa danh sách câu hỏi rồi submit. | Dữ liệu map đúng với header. | Data sync mới sẽ fill lần lượt các cột theo thứ tự trong form result chứ không map theo header => Khi nào sync lại toàn bộ sheet thì mới map lại theo header | | OK |
| TC10 | Verify Form 1 Page + Header cũ | | | Form loại 1 Page, Header cũ (không có LINE ユーザーID, システム表示名) | 1. Tạo form.<br>2. Submit lần 1.<br>3. Edit form thêm câu hỏi.<br>4. Submit lần 2, để trống 1 câu hỏi mới.<br>5. Submit lần 3. | Không lệch cột. | | | OK |
| TC11 | Verify Form 1 Page + Header mới | | | Form loại 1 Page, Header mới | 1. Tạo form.<br>2. Submit lần 1.<br>3. Edit form thêm câu hỏi.<br>4. Submit lần 2, để trống 1 câu hỏi mới.<br>5. Submit lần 3. | Hai cột LINE ユーザーID và システム表示名 đúng vị trí, dữ liệu không lệch. | | | OK |
| TC12 | Verify Form Multi Page + Header cũ | | | Form nhiều page, Header cũ | 1. Tạo form.<br>2. Submit lần 1.<br>3. Edit form thêm câu hỏi.<br>4. Submit lần 2, để trống 1 câu hỏi mới.<br>5. Submit lần 3. | Dữ liệu đúng vị trí. | | | OK |
| TC13 | Verify Form Multi Page + Header mới | | | Form nhiều page, Header mới | 1. Tạo form.<br>2. Submit lần 1.<br>3. Edit form thêm câu hỏi.<br>4. Submit lần 2, để trống 1 câu hỏi mới.<br>5. Submit lần 3. | Dữ liệu đúng vị trí, không lệch cột. | | | OK |
| TC14 | Header bị xóa (hàng đầu tiên rỗng) | | | Xóa toàn bộ hàng header của Google Sheet | Submit form. | Hệ thống nhận diện sheet không hợp lệ và ghi lại như sheet mới (tạo lại header rồi ghi dữ liệu). | | | OK |
| TC15 | Result ID không nằm ở A1 hoặc B1 | | | Di chuyển cột Result ID sang C1/D1 | Submit form. | Hệ thống coi như sheet mới và tạo lại header chuẩn trước khi ghi dữ liệu. | | | OK |
| TC16 | Result ID nằm ở A1 | | | Header chuẩn cũ | Submit form. | Append bình thường, không tạo lại sheet. | | | OK |
| TC17 | Result ID nằm ở B1 | | | Header chuẩn mới (A1 là LINE ユーザーID) | Submit form. | Append bình thường, không tạo lại sheet. | | | OK |
| TC18 | Retry khi lần sync đầu thất bại | | | Giả lập Google API lỗi ở lần sync đầu | 1. Submit form.<br>2. Lần sync đầu thất bại.<br>3. Job retry chạy. | Retry sync thành công, dữ liệu giống hệt trường hợp sync mới, không tạo dòng sai hoặc lệch cột. | | | OK |
| TC19 | Retry với sheet đã có dữ liệu | | | Google Sheet đã có dữ liệu, lần sync đầu lỗi | Submit form → retry. | Retry append đúng từ cột A, không bị lệch cột. | | | OK |
| TC20 | Retry khi sheet được coi là sheet mới | | | Header bị xóa hoặc Result ID không ở A1/B1 | Submit form → retry. | Retry tạo lại header và ghi dữ liệu như trường hợp sync mới. | | | OK |
| TC21 | Retry không tạo duplicate | | | Lần đầu ghi thành công nhưng timeout khi trả response khiến job retry chạy | Thực hiện retry. | Không tạo thêm bản ghi trùng trên Google Sheet. | | | OK |
| TC22 | Verify nhiều user submit đồng thời | | | Có nhiều LINE User | Nhiều user submit cùng lúc. | Mỗi user có đúng một dòng dữ liệu, không lệch cột. | | | Not test |
| TC23 | Verify Google Sheet có nhiều dữ liệu | | | Sheet có hàng nghìn dòng | Submit thêm dữ liệu. | Append đúng cuối sheet, không lệch cột. | | | OK |
| TC24 | Verify dữ liệu Unicode | | | Form có tiếng Nhật, Emoji | Submit dữ liệu. | Hiển thị đúng, không lỗi encoding, không lệch cột. | | | OK |
| TC25 | Verify sau nhiều lần edit form | | | Form được thêm câu hỏi nhiều lần | Edit → Submit → Edit → Submit nhiều lần. | Dữ liệu luôn đúng theo cấu trúc hiện tại của form. | | | OK |
| TC26 | Check sync xóa form-result không bị ảnh hưởng | | | | | Job sync xóa được đúng form-result trên google | | | OK |
| TC27 | Check sync form cũ (using_old_version = 1) | | | `<trống trên Sheet>` | `<trống trên Sheet>` | `<trống trên Sheet>` | | | |

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

<!-- Source: fetched từ Redmine #38552 Link TCs, tab "Sync google" (gid=806554565), spreadsheet 1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4, lúc 2026-07-11.
     Redmine ghi "row 439 ~ 463" nhưng block TC thực tế chạy từ row 439 (TC01) đến row 465 (TC27) — đã fetch đủ 27 TC. Verify lại với người viết TC.
     Layout sheet: B=TC ID, C=Mục tiêu(Title), D=Điều kiện(Precondition), E=Các bước, H=Kết quả mong đợi, I=note, J=Status (cột "Bug KH #38552 07/2026").
     KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
