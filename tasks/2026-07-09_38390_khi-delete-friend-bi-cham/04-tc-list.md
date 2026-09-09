<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1gVJjKgom9Cjrvo5K0r4ekhrawlokFT1ovh3SuDcG3PI/edit?gid=412698763#gid=412698763 | sheet=Testcase | anchor=Main Function -->

# 04 — TC List (fetch từ Redmine #38390 Link TCs)

> ⚠️ **TCs fetch read-only** từ Google Sheet (tab `Testcase`, range A143:J155). KHÔNG sửa nội dung TC gốc nếu chưa confirm với Leader.
> Sheet gốc dùng **cấu trúc phân cấp / merge cell** (Main Function → Màn → Case → nhiều check-point). Bảng dưới giữ NGUYÊN giá trị cell; ô trống = ô bị merge trên sheet.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1gVJjKgom9Cjrvo5K0r4ekhrawlokFT1ovh3SuDcG3PI/edit?gid=412698763#gid=412698763 (tab Testcase, dòng 143-155) |

---

## TC List

> Bảng giữ đúng cột nguồn của sheet human (Main Function / Màn / Case / Steps / Check point / Expected / Status). Newline trong cell render bằng `<br>`.

| TC ID | Main Function | Màn (screen) | Case / Title | Steps | Check point | Expected result | Status |
|---|---|---|---|---|---|---|---|
| TC001 | Màn friend list<br>=> Web | màn hidden | Xóa friend hàng loạt | 1. Vào màn friend list<br>2. Click button 非表示中の友だち để vào màn `/basic/friendlist/hidden`<br>3. Chọn check box all friend => nhấn xóa hàng loạt | check data sau khi đã xóa friend | - check ở các bảng: `url_shorten`, `url_shorten_detail`, `form_answer_result: update deleted_at`, `b_event_detail`<br>- data ở các bảng đã được xóa | OK |
| TC002 | | | (Xóa friend hàng loạt — tiếp) | | check sau khi kết bạn lại | - Detail các data của line friend này trước đó không hiển thị<br>- click vào url_shorten có count<br>- trả lời form được thành công => có ghi nhận form_result<br>- có booking được event | OK |
| TC003 | | | Chọn all friend => thực hiện xóa 1 friend | | | - Chỉ xóa data của line friend đã xóa<br>- check ở các bảng: `url_shorten`, `url_shorten_detail`, `form_answer`, `b_event_detail`<br>- data ở các bảng đã được xóa | OK |
| TC004 | | màn user-block | Xóa friend hàng loạt | 1. Vào màn friend list<br>2. Click button ブロックされた友だち để vào màn `/basic/friendlist/user-block`<br>3. Chọn check box all friend => nhấn xóa hàng loạt | check data sau khi đã xóa friend | - check ở các bảng: `url_shorten`, `url_shorten_detail`, `form_answer_result: update deleted_at`, `b_event_detail`<br>- data ở các bảng đã được xóa | OK |
| TC005 | | | (Xóa friend hàng loạt — tiếp) | | check sau khi kết bạn lại | - Detail các data của line friend này trước đó không hiển thị<br>- click vào url_shorten có count<br>- trả lời form được thành công => có ghi nhận form_result<br>- có booking được event | OK |
| TC006 | | | Chọn all friend => thực hiện xóa 1 friend | | | - Chỉ xóa data của line friend đã xóa<br>- check ở các bảng: `url_shorten`, `url_shorten_detail`, `form_answer`, `b_event_detail`<br>- data ở các bảng đã được xóa | OK |
| TC007 | | màn block | Xóa friend hàng loạt | 1. Vào màn friend list<br>2. Click button ブロックした友だち để vào màn `/basic/friendlist/block`<br>3. Chọn check box all friend => nhấn xóa hàng loạt | check data sau khi đã xóa friend | - check ở các bảng: `url_shorten`, `url_shorten_detail`, `form_answer_result: update deleted_at`, `b_event_detail`<br>- data ở các bảng đã được xóa | OK |
| TC008 | | | (Xóa friend hàng loạt — tiếp) | | check sau khi kết bạn lại | - Detail các data của line friend này trước đó không hiển thị<br>- click vào url_shorten có count<br>- trả lời form được thành công => có ghi nhận form_result<br>- có booking được event | OK |
| TC009 | | | Chọn all friend => thực hiện xóa 1 friend | | | - Chỉ xóa data của line friend đã xóa<br>- check ở các bảng: `url_shorten`, `url_shorten_detail`, `form_answer`, `b_event_detail`<br>- data ở các bảng đã được xóa | OK |
| TC010 | | Xóa friend ở my page | | | | - check ở các bảng: `url_shorten`, `url_shorten_detail`, `form_answer`, `b_event_detail`<br>- data ở các bảng đã được xóa | OK |
| TC011 | | check detail friend tab scenario | | | | - Xóa lịch sử scenario đã chạy<br>- check db: `scenario_lineuser_history` | OK |

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

<!-- Source: fetched từ Redmine #38390 Link TCs, range A143:J155 tab "Testcase" lúc 2026-07-09. KHÔNG sửa TCs này nếu chưa confirm với Leader. Lưu ý: file 04 này là TC do human viết (fetch read-only) — nếu dùng /sync-ai-tc sẽ push chính TC này ngược lại sheet, cân nhắc trước khi sync. -->
