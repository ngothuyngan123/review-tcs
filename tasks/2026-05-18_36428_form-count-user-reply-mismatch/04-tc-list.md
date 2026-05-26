<!-- sync-target: https://docs.google.com/spreadsheets/d/1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4/edit?gid=1515885666#gid=1515885666 -->
# 04 — TC List (fetched từ Sheet master)

> File này được auto-fetch từ Google Sheet master tại tab "Improve form 01/2025", range A313:J339 (27 rows).
> **KHÔNG sửa TCs này nếu chưa confirm với Leader.** Đây là TC team đã viết — giữ nguyên để `/review-tc` tham chiếu.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | v1 |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1pT_Z-NZOVYZrTreUdn6mQJI0c_vOPAiwjRf8v-4jg-4/edit?gid=1515885666#gid=1515885666 |

---

## TC List

> **Lưu ý**: Sheet master tab "Improve form 01/2025" dùng schema dạng outline lồng nhau (function → item → sub-item → steps no-setting / steps with-setting → expected). KHÔNG khớp 100% với schema chuẩn 10-cột (TC ID / Title / Type / Priority / Precondition / Steps / Expected / Output note / Assignee / Status). Dưới đây paste **NGUYÊN VĂN** dữ liệu cell từ sheet — preserve cấu trúc gốc để Leader review đúng những gì member đã ghi.

### Rows 313-314 — Dev evaluation + Reproduction note (header, không phải TC)

**Row 313 (col C):**
```
Bug KH #36428: [15-05-2026][回答ID：28184][Form] Form "初回アンケート" hiển thị "0 người trả lời" nhưng vào "表示" thì có data thực
1. Nguyên nhân
   - Trong màn hình setting 各種設定 của form, logic khi save sẽ lưu tất cả các trường của bảng form_answer (trừ các trường của 4 tab đầu). Khi user trả lời form sẽ tăng count_user_reply, nhưng cùng lúc đó admin lại vào edit màn 各種設定 thì count_user_reply bị update về data cũ
2. Cách fix
   - khi save setting 各種設定 thì chỉ save những trường được setting
3. Đã check và sửa các function sử dụng đến function/data vừa sửa
4. Đánh giá ảnh hưởng
        4.1 List function
            - public/js/form_answer/component/other-settings.js
        4.2 List những data bị update khi fix bug
            - k có
        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
            - save setting 各種設定 (check lại từng trường 1 xem có update đc k)
```

**Row 314 (col C):**
```
Tái hiện case KH:
1. User trả lời form
2. Admin thực hiện nhấn save ở màn setting tab số 5 (chỉ nhấn save k cần setting gì cả)
hiện tượng: ở màn list không count số lượng user trả lời form
```

### Rows 315-339 — TC outline

> Schema sheet (đoán từ vị trí cell): C = Function / Item, D = Detail, E = Sub-detail / Precondition, F = Step (no setting), G = Step (with setting), H = Expected result.

| Row | C — Function/Item | D — Detail | E — Precondition | F — Step (no setting) | G — Step (with setting) | H — Expected |
|---|---|---|---|---|---|---|
| 315 | Form basic | 1 user trả lời form | user đã submit form | - Admin thực hiện nhấn save ở tab 5, màn 1 |  | - save thành công<br>- màn list hiên thị đúng số lượng user trả lời<br>- check db: form_answer.count_user_reply<br>- enable btn down load csv, gg sheet<br>- hiển thị reselt câu trả lời của user |
| 316 |  |  |  |  | Có thực hiện setting thêm => save |  |
| 317 |  |  |  | - Admin thực hiện nhấn save ở tab 5, màn 2 |  |  |
| 318 |  |  |  |  | Có thực hiện setting thêm => save |  |
| 319 |  |  |  | - Admin thực hiện nhấn save ở tab 5, màn 3 |  |  |
| 320 |  |  |  |  | Có thực hiện setting thêm => save |  |
| 321 |  |  |  | - Admin thực hiện nhấn save ở tab 5, màn 4 |  |  |
| 322 |  |  |  | Admin thực hiện nhấn save ở tab 1 |  | - save thành công<br>- màn list hiên thị đúng số lượng user trả lời<br>- check db: form_answer.count_user_reply<br>- enable btn down load csv, gg sheet<br>- hiển thị reselt câu trả lời của user |
| 323 |  |  |  |  | Có thực hiện setting thêm => save |  |
| 324 |  |  |  | Admin thực hiện nhấn save ở tab 2, màn 1 |  |  |
| 325 |  |  |  |  | Có thực hiện setting thêm => save |  |
| 326 |  |  |  | Admin thực hiện nhấn save ở tab 2, màn 2 |  |  |
| 327 |  |  |  |  | Có thực hiện setting thêm => save |  |
| 328 |  |  |  | Admin thực hiện nhấn save ở tab 2, màn 3 |  |  |
| 329 |  |  |  |  | Có thực hiện setting thêm => save |  |
| 330 |  |  |  | Admin thực hiện nhấn save ở tab 4, màn 1 |  |  |
| 331 |  |  |  |  | Có thực hiện setting thêm => save |  |
| 332 |  |  |  | Admin thực hiện nhấn save ở tab 4, màn 2 |  |  |
| 333 |  | check khi user trả lời | mở opent app line | open ở device ios/android |  | - có count số user |
| 334 |  |  | opent ngoài app line |  |  |  |
| 335 |  |  | open qua click button |  |  |  |
| 336 |  | Check form rẽ nhánh | Check khi đổi vị trí page |  |  | - khi user trả lời có count số user |
| 337 |  |  | check khi add/xóa page |  |  |  |
| 338 |  | Check form copy |  |  |  |  |
| 339 |  | check account staff |  |  |  |  |

### Chú thích cột (schema chuẩn 10-cột — KHÔNG khớp với sheet này)

- **Type**: `Positive` / `Negative` / `Boundary` / `Regression`
- **Priority**: `High` / `Medium` / `Low`
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

<!-- Source: fetched từ Redmine #36428 Link TCs, range A313:J339 tab "Improve form 01/2025" lúc 2026-05-18. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
