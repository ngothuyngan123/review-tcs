<!-- sync-target: https://docs.google.com/spreadsheets/d/15QEYkgp3OhzQyA5CLADvpQu_CAGovQIREuNjxPnBbOk/edit?gid=412698763#gid=412698763 -->
# 04 — TC List (fetched từ Sheet master)

> ⚠️ Source là **bảng TC phân cấp** (Main Function / Sub1-5 / Expect Result với merged cells), KHÔNG phải bảng 10 cột chuẩn.
> Khi convert: cột **Precondition** = ngữ cảnh cha (Main Function + nhánh cha carry-forward từ merged cell); **Steps** = điều kiện lá của từng dòng; **Expected result** = cột "Expect Result" giữ NGUYÊN văn. Title được suy ra từ đường dẫn nhánh (để Leader trace). TC ID đánh số theo dòng. Type/Priority/Output note/Assignee/Status để trống — member fill khi review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/15QEYkgp3OhzQyA5CLADvpQu_CAGovQIREuNjxPnBbOk/edit?gid=412698763#gid=412698763 (tab "Improve 1.0", line 643-660) |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Bot đã liên kết GG Sheet — tạo landing mới (google_sheet_id=NULL), landing chưa có data | | | Bot đã liên kết Google Sheet → tạo qr landing mới | setting: 1 Landing có google_sheet_id = NULL → landing chưa có count data nào | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- data trên gg sheet không có | | | |
| TC002 | Bot đã liên kết GG Sheet — tạo landing mới (google_sheet_id=NULL), quét qr có data | | | Bot đã liên kết Google Sheet → tạo qr landing mới → setting: 1 Landing có google_sheet_id = NULL | quét qr => landing có data | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- check data sync lên gg sheet bình thường => job sync data sau 1 days mới chạy (ngày hôm nay liên kết => tối job chạy mới sync data lên) | | | |
| TC003 | Nhiều landing cùng thiếu google_sheet_id — job chạy, landing chưa có data | | | Bot đã liên kết Google Sheet → tạo qr landing mới | Nhiều landing cùng bị thiếu google_sheet_id → job thực hiện chạy (job chạy ngay chỉ test được ở dev) → landing chưa có count data nào | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- data trên gg sheet không có | | | |
| TC004 | Nhiều landing cùng thiếu google_sheet_id — job chạy, quét qr có data | | | Bot đã liên kết Google Sheet → tạo qr landing mới → Nhiều landing cùng bị thiếu google_sheet_id → job thực hiện chạy | quét qr => landing có data | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- check data sync lên gg sheet bình thường => job sync data sau 1 days mới chạy (ngày hôm nay liên kết => tối job chạy mới sync data lên) | | | |
| TC005 | Landing có trước khi liên kết GG thành công — check icon gg sheet, chưa có data | | | Bot đã liên kết Google Sheet → landing đã có trước khi liên kết gg thành công | check hiển thị icon gg sheet → landing chưa có count data nào | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- check data sync lên gg sheet bình thường | | | |
| TC006 | Landing có trước khi liên kết GG thành công — check icon gg sheet, landing đã có data | | | Bot đã liên kết Google Sheet → landing đã có trước khi liên kết gg thành công → check hiển thị icon gg sheet | landing đã có data | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- check data sync lên gg sheet bình thường => job sync data sau 1 days mới chạy (ngày hôm nay liên kết => tối job chạy mới sync data lên) | | | |
| TC007 | Landing có trước khi liên kết GG — check landing OFF | | | Bot đã liên kết Google Sheet → landing đã có trước khi liên kết gg thành công | check landing OFF | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- check data sync lên gg sheet bình thường => job sync data sau 1 days mới chạy (ngày hôm nay liên kết => tối job chạy mới sync data lên) | | | |
| TC008 | Landing đã xóa => khôi phục lại — landing chưa có data | | | Bot đã liên kết Google Sheet → landing đã có trước khi liên kết gg thành công → check những landing đã xóa | khôi phục lại landing → landing chưa có count data nào | - khi job chạy để sync data lên gg sheet sẽ quét google_shet_id đã có hay chưa => chưa có thì thực hiện tạo<br>- google_sheet_id được cập nhật vào landing.<br>- data trên gg sheet không có | | | |
| TC009 | Landing đã xóa => khôi phục lại — landing đã có data | | | Bot đã liên kết Google Sheet → landing đã có trước khi liên kết gg thành công → check những landing đã xóa → khôi phục lại landing | landing đã có data | - khi job chạy để sync data lên gg sheet sẽ quét google_shet_id đã có hay chưa => chưa có thì thực hiện tạo<br>- google_sheet_id được cập nhật vào landing.<br>- check data sync lên gg sheet bình thường | | | |
| TC010 | Landing đã xóa — đang nằm trong màn remote | | | Bot đã liên kết Google Sheet → landing đã có trước khi liên kết gg thành công → check những landing đã xóa | đang nằm trong màn remote | - google_sheet_id không được cập nhật vào landing. | | | |
| TC011 | Xóa liên kết landing => liên kết lại — landing trước đó đã tạo gg sheet 1 lần | | | Bot đã liên kết Google Sheet → Xóa liên kết landing => liên kết lại | check những landing trước đó đã được tạo gg sheet 1 lần | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- check data sync lên gg sheet bình thường => job sync data sau 1 days mới chạy (ngày hôm nay liên kết => tối job chạy mới sync data lên)<br>- data sync lên gg sheet không bị trùng | | | |
| TC012 | Xóa liên kết landing => liên kết lại — landing chưa tạo google_sheet_id lần nào | | | Bot đã liên kết Google Sheet → Xóa liên kết landing => liên kết lại | check landing chưa tạo google_shet_id lần nào | - hiển thị icon gg sheet ở landing => check màn list và màn detail<br>- Sheet mới được tạo.<br>- google_sheet_id được cập nhật vào landing.<br>- check data sync lên gg sheet bình thường => job sync data sau 1 days mới chạy (ngày hôm nay liên kết => tối job chạy mới sync data lên) | | | |
| TC013 | Bot KHÔNG liên kết GG — quét landing | | | check những bot không liên kết gg | check quét landing | - quét landing thành công<br>- send action bình thường | | | |
| TC014 | Check account staff — liên kết gg sheet | | | Check account staff | (liên kết gg sheet) | - liên kết gg sheet thành công<br>- sync data lên bình thường | | | |
| TC015 | Recover data KH — landing tạo trước khi liên kết, google_sheet_id=NULL | | | Check recover data KH → liên kết gg sheet thành công | Landing đã tạo trước khi liên kết → trường google_sheet_id = NULL | - sau khi job chạy, thêm google_sheet_id cho landing<br>- hiển thị icon gg sheet lên GUI<br>- sau khi chạy job sync data<br>+ data hiển thị trên gg sheet thành công<br>+ hiển thị đúng/đủ data | | | |
| TC016 | Recover data — bot account tự tạo, landing tạo trước khi liên kết, google_sheet_id=NULL | | | Check recover data KH → check data bot account mình tự tạo | Landing đã tạo trước khi liên kết → trường google_sheet_id = NULL | - sau khi job chạy, thêm google_sheet_id cho landing<br>- hiển thị icon gg sheet lên GUI<br>- sau khi chạy job sync data<br>+ data hiển thị trên gg sheet thành công<br>+ hiển thị đúng/đủ data | | | |
| TC017 | Recover data — bot account tự tạo, landing tạo sau khi liên kết, job chạy lần 2 | | | Check recover data KH → check data bot account mình tự tạo | Landing tạo sau khi liên kết → check sau khi job chạy lần 2 | - sau khi job chạy, thêm google_sheet_id cho landing<br>- hiển thị icon gg sheet lên GUI<br>- sau khi chạy job sync data<br>+ data hiển thị trên gg sheet thành công<br>+ hiển thị đúng/đủ data | | | |
| TC018 | Recover data — bot account tự tạo, landing trong màn xóa => khôi phục, sau khi job chạy | | | Check recover data KH → check data bot account mình tự tạo | Check landing đang nằm trong màn xóa => khôi phục landing → check sau khi job chạy | - sau khi job chạy, thêm google_sheet_id cho landing<br>- hiển thị icon gg sheet lên GUI<br>- sau khi chạy job sync data<br>+ data hiển thị trên gg sheet thành công<br>+ hiển thị đúng/đủ data | | | |

### Chú thích cột

- **Type**: `Positive` / `Negative` / `Boundary` / `Regression` — để trống, member fill.
- **Priority**: `High` / `Medium` / `Low` — để trống, member fill.
- **Output note** / **Assignee** / **Status**: để trống khi sinh draft. QA fill sau khi run TC.

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). Lưu ý source ghi nhiều case "job chạy ngay chỉ test được ở dev" (`form.watermeru.com`) — TC003/TC004 và các case ép job chạy ngay nên test ở Dev.

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
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md):

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22 (chọn mục liên quan task)
- [ ] A.2 Non-function: URLs đo lường / Regression / Security / Compatibility

**§B Checklist job**:
- [ ] B.1 Job callback (nếu chạm callback)
- [ ] B.2 Job sync Java — CLJ01 (nếu chạm Google sync)

**§C Các tính năng chung**:
- [ ] C.5 Google sheet
- [ ] C.8 Sort

<!-- Source: fetched từ Redmine #37396 Link TCs, range A641:J660 tab "Improve 1.0" (gid 412698763). Dòng 641-642 là header bug + note "chưa tái hiện được" (không phải TC); dòng 643-660 = 18 TC phân cấp. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
