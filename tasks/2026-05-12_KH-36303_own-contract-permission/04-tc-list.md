# 04 — TC List (do member viết)

> File này được **chuyển đổi** từ Google Sheet `Quản lý hợp đồng` rows 1430-1448 (gid 223705530). Format gốc trên sheet là **checklist nested** (Main Function / Sub1 / Sub2 / ... / Step / Note), KHÔNG phải bảng 10 cột chuẩn. Tôi đã suy luận map sang format chuẩn để Leader review — TC IDs mới được gán (TC-01 → TC-18).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | _<chưa rõ — sheet không có cột Assignee fill>_ |
| Ngày submit | 2026-05-12 (suy luận từ commit dev) |
| Version TCs | v1 |
| Link TC gốc | [Sheet — Quản lý hợp đồng rows 1430-1448](https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=223705530#gid=223705530&range=1430:1448) |

---

## TC List

> ⚠️ Sheet gốc thiếu nhiều thông tin: **Precondition / Steps chi tiết / Expected đo lường được** đều rỗng hoặc rất sơ sài (chỉ có 1 dòng action như "change card -> tranfer"). Tôi đã giữ nguyên nội dung gốc, đánh dấu `_<empty>_` ở các ô tester chưa viết. Đây là một vấn đề lớn cần Leader flag.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-01 | [Staff có quyền] Check access detail contract | Positive | High | Staff có quyền access hợp đồng | _<empty>_ | Access được hợp đồng thành công | | | OK |
| TC-02 | [Staff có quyền] Thao tác change card → transfer | Positive | High | Staff có quyền + đã vào detail contract | _<empty>_ | change card -> tranfer (thành công) | | | OK |
| TC-03 | [Staff có quyền] Thao tác change transfer → card | Positive | High | _<empty>_ | _<empty>_ | change tranfer -> card (thành công) | | | OK |
| TC-04 | [Staff có quyền] Đăng ký sub card | Positive | High | _<empty>_ | _<empty>_ | đăng ký sub card (thành công) | | | OK |
| TC-05 | [Staff có quyền] Change sub card | Positive | High | _<empty>_ | _<empty>_ | change sub card (thành công) | | | OK |
| TC-06 | [Staff có quyền] Xóa sub card | Positive | High | _<empty>_ | _<empty>_ | xóa sub card (thành công) | | | OK |
| TC-07 | [Staff có quyền] Change type bill | Positive | High | _<empty>_ | _<empty>_ | change type bill (thành công) | | | OK |
| TC-08 | [Staff có quyền] Hủy hợp đồng | Positive | High | _<empty>_ | _<empty>_ | hủy hợp đồng (thành công) | | | OK |
| TC-09 | [Staff KHÔNG có quyền] Check other bot contract detail của user | Positive | High | Staff không có quyền access hợp đồng | _<empty>_ | Access được hợp đồng thành công | | | OK |
| TC-10 | [Staff KHÔNG có quyền] Thao tác change card → transfer | Positive | High | _<empty>_ | _<empty>_ | change card -> tranfer (thành công) | | | OK |
| TC-11 | [Staff KHÔNG có quyền] Thao tác change transfer → card | Positive | High | _<empty>_ | _<empty>_ | change tranfer -> card (thành công) | | | OK |
| TC-12 | [Staff KHÔNG có quyền] Đăng ký sub card | Positive | High | _<empty>_ | _<empty>_ | đăng ký sub card (thành công) | | | OK |
| TC-13 | [Staff KHÔNG có quyền] Change sub card | Positive | High | _<empty>_ | _<empty>_ | change sub card (thành công) | | | OK |
| TC-14 | [Staff KHÔNG có quyền] Xóa sub card | Positive | High | _<empty>_ | _<empty>_ | xóa sub card (thành công) | | | OK |
| TC-15 | [Staff KHÔNG có quyền] Change type bill | Positive | High | _<empty>_ | _<empty>_ | change type bill (thành công) | | | OK |
| TC-16 | [Staff KHÔNG có quyền] Hủy hợp đồng | Positive | High | _<empty>_ | _<empty>_ | hủy hợp đồng (thành công) | | | OK |
| TC-17 | [Staff KHÔNG có quyền] Check **own** contract detail của staff | Negative | High | _<empty>_ | _<empty>_ | Access denied — Permission error displayed — Cannot view contract details | ⚠️ **MÂU THUẪN với fix? Cần verify** | | OK |
| TC-18 | Change từ **có quyền → không có quyền** (mid-session) | Negative | High | _<empty>_ | _<empty>_ | Access denied — Permission error displayed — Cannot view contract details | ⚠️ Ambiguous scenario | | OK |
| TC-19 | [Section "Check account staff"] _<incomplete row>_ | _<empty>_ | _<empty>_ | _<empty>_ | _<empty>_ | _<empty>_ | Row 1448 chỉ có "OK", không có nội dung khác | | OK |

### Chú thích sheet → 10 cột

Mapping từ sheet:
- Cột B "Main Function" + C "Sub1" + D "Sub2" → tôi gộp vào **Title** (có prefix `[Staff có/không quyền]`)
- Cột I/J (action như "change card -> tranfer") → coi như **Expected** (vì sheet không tách Steps riêng)
- **Precondition / Steps**: sheet **không có** → để `_<empty>_`. Đây là vấn đề lớn — Leader phải yêu cầu member bổ sung.

### Environment (note)

- Sheet không note môi trường — mặc định Staging (`staging.lme.jp`).
- Bug từ Production → cần verify ít nhất 1 TC reproduce trên môi trường có data thật hoặc data clone từ KH.

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md` — _<chưa verify Redmine — flag MAJOR>_
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có) — N/A
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục — _<partial — không có TC cho F4 (max friend), F10 (authenticationBotContract)>_
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify — _<chưa đủ — xem coverage matrix>_
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH) — _<chưa rõ — TC-17 có thể intended là reproduce nhưng expected có vẻ sai>_
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3 — _<partial>_
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2 — N/A (không có data update)
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được — _<FAIL — sheet không có Steps cụ thể>_
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover — _<partial — chỉ có thao tác, không có tên function>_

### Base checklist LME

> Member **không tick** bất kỳ ô nào — sheet chỉ có TC list raw. Cần Leader verify lại với member.

**§A Checklist web**:
- [ ] A.1 Function checklist — chưa rà
- [ ] A.2 Non-function — chưa rà

**§B Checklist job**:
- [ ] B.1 Job callback — N/A (không chạm)
- [ ] B.2 Job sync Java — N/A (không chạm)

**§C Các tính năng chung**:
- [ ] C.1 **Bill tiền** — task chạm change card / change bill type / sub card → CẦN tick — _<chưa rõ member có cover không, sheet không list>_
- [ ] C.2 Send message — N/A
- [ ] C.3 Friend info — N/A
- [ ] C.4 Tag — N/A
- [ ] C.5 Google sheet — N/A
- [ ] C.6 Google calendar — N/A
- [ ] C.7 Plan limits — N/A (không tạo mới contract)
- [ ] C.8 Sort — N/A
