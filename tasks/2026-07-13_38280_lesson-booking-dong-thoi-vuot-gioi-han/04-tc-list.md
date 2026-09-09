<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1337DDgFt-zTLL4OfPg-4JUQ-jOreeiwQIOiV_5eDJIE/edit?gid=2021990578 | sheet=Booking phía line user | anchor=Main Function -->
<!-- Sheet Salon (target thứ 2, /sync-* chỉ push được 1 target — đổi tay khi cần): https://docs.google.com/spreadsheets/d/1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s/edit?gid=2021990578 | sheet=Booking phía line user -->

# 04 — TC List (do member viết)

> **TCs fetch từ Sheet — READ-ONLY.** Không sửa Title / Expected dù fix đổi behavior. Đây là input cho `/review-tc`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `Thanh Phương` (theo journal Redmine #125009, 2026-07-07) |
| Ngày submit | `2026-07-07` |
| Version TCs | `v1` |
| Link TC gốc — Lesson | https://docs.google.com/spreadsheets/d/1337DDgFt-zTLL4OfPg-4JUQ-jOreeiwQIOiV_5eDJIE/edit?gid=2021990578 — tab `Booking phía line user`, row 551–563 |
| Link TC gốc — Salon | https://docs.google.com/spreadsheets/d/1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s/edit?gid=2021990578 — tab `Booking phía line user`, row 1397–1409 |

> ⚠️ Redmine ghi range Lesson `551~562` và Salon `1397~1408` (12 dòng), nhưng Sheet thực tế có **13 dòng TC** mỗi bên (551–563 / 1397–1409) — dòng cuối (`Slot remain=1, User A booking trước sau đó User B`, nhóm *có setting bill tiền*) nằm ngoài range Redmine. Đã fetch **đủ 13 dòng** mỗi bên. Tester confirm lại với Thanh Phương.
>
> ⚠️ Sheet gốc **không có cột Type / Priority / Output note / Assignee** → các cột đó để trống (`-`). Cột `Status` giữ **nguyên văn** giá trị cell của Sheet (`OK staging`).

---

## TC List

### A. Lesson — Sheet `1337DDg…`, tab `Booking phía line user`, row 551–563

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Check calendar không setting bill tiền — Slot không giới hạn | - | - | Calendar **không** setting bill tiền; Slot **không giới hạn** | 2 user nhấn booking cùng lúc | Cả hai booking thành công | - | - | OK staging |
| TC002 | Check calendar không setting bill tiền — Slot có số remain = 2 | - | - | Calendar **không** setting bill tiền; Slot có số remain = 2 | 2 user nhấn booking cùng lúc | Cả hai booking thành công | - | - | OK staging |
| TC003 | Check calendar không setting bill tiền — Slot remain = 1, 1 user booking | - | - | Calendar **không** setting bill tiền; Slot có số remain = 1 | User A booking | User A booking thành công | - | - | OK staging |
| TC004 | Check calendar không setting bill tiền — Slot remain = 1, 2 user booking cùng lúc | - | - | Calendar **không** setting bill tiền; Slot có số remain = 1 | User A và User B nhấn booking cùng lúc | Chỉ 1 booking được tạo, user còn lại nhận thông báo hết chỗ | - | - | OK staging |
| TC005 | Check calendar không setting bill tiền — Slot remain = 1, 3 user booking cùng lúc | - | - | Calendar **không** setting bill tiền; Slot có số remain = 1 | 3 user nhấn booking cùng lúc | Chỉ 1 booking được tạo, user còn lại nhận thông báo hết chỗ | - | - | OK staging |
| TC006 | Check calendar không setting bill tiền — Slot remain = 1, booking tuần tự | - | - | Calendar **không** setting bill tiền; Slot có số remain = 1 | User A nhấn booking trước sau đó user B nhấn booking | User A book thành công<br>User B báo hết chỗ | - | - | OK staging |
| TC007 | Check case calendar setting request booking — Slot remain = 1, 2 user cùng lúc | - | - | Calendar setting **request booking**; Slot có số remain = 1 | Slot có số remain = 1<br>2 user nhấn booking cùng lúc | Cả 2 booking đều book success, trạng thái là request booking | - | - | OK staging |
| TC008 | Check calendar có setting bill tiền — Slot không giới hạn | - | - | Calendar **có** setting bill tiền; Slot **không giới hạn** | 2 user nhấn booking cùng lúc | Cả hai booking thành công | - | - | OK staging |
| TC009 | Check calendar có setting bill tiền — Slot có số remain = 2 | - | - | Calendar **có** setting bill tiền; Slot có số remain = 2 | 2 user nhấn booking cùng lúc | Cả hai booking thành công | - | - | OK staging |
| TC010 | Check calendar có setting bill tiền — Slot remain = 1, 1 user booking | - | - | Calendar **có** setting bill tiền; Slot có số remain = 1 | User A booking | User A booking thành công | - | - | OK staging |
| TC011 | Check calendar có setting bill tiền — Slot remain = 1, 2 user booking cùng lúc | - | - | Calendar **có** setting bill tiền; Slot có số remain = 1 | User A và User B nhấn booking cùng lúc | Chỉ 1 booking được tạo, user còn lại nhận thông báo hết chỗ | - | - | OK staging |
| TC012 | Check calendar có setting bill tiền — Slot remain = 1, 3 user booking cùng lúc | - | - | Calendar **có** setting bill tiền; Slot có số remain = 1 | 3 user nhấn booking cùng lúc | Chỉ 1 booking được tạo, user còn lại nhận thông báo hết chỗ | - | - | OK staging |
| TC013 | Check calendar có setting bill tiền — Slot remain = 1, booking tuần tự | - | - | Calendar **có** setting bill tiền; Slot có số remain = 1 | User A nhấn booking trước sau đó user B nhấn booking | User A book thành công<br>User B báo hết chỗ | - | - | OK staging |

### B. Salon — Sheet `1SojySaG…`, tab `Booking phía line user`, row 1397–1409

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC014 | [Salon] Check calendar không setting bill tiền — Slot không giới hạn | - | - | Calendar **không** setting bill tiền; Slot **không giới hạn** | 2 user nhấn booking cùng lúc | Cả hai booking thành công | - | - | OK staging |
| TC015 | [Salon] Check calendar không setting bill tiền — Slot có số remain = 2 | - | - | Calendar **không** setting bill tiền; Slot có số remain = 2 | 2 user nhấn booking cùng lúc | Cả hai booking thành công | - | - | OK staging |
| TC016 | [Salon] Check calendar không setting bill tiền — Slot remain = 1, 1 user booking | - | - | Calendar **không** setting bill tiền; Slot có số remain = 1 | User A booking | User A booking thành công | - | - | OK staging |
| TC017 | [Salon] Check calendar không setting bill tiền — Slot remain = 1, 2 user booking cùng lúc | - | - | Calendar **không** setting bill tiền; Slot có số remain = 1 | User A và User B nhấn booking cùng lúc | Chỉ 1 booking được tạo, user còn lại nhận thông báo hết chỗ | - | - | OK staging |
| TC018 | [Salon] Check calendar không setting bill tiền — Slot remain = 1, 3 user booking cùng lúc | - | - | Calendar **không** setting bill tiền; Slot có số remain = 1 | 3 user nhấn booking cùng lúc | Chỉ 1 booking được tạo, user còn lại nhận thông báo hết chỗ | - | - | OK staging |
| TC019 | [Salon] Check calendar không setting bill tiền — Slot remain = 1, booking tuần tự | - | - | Calendar **không** setting bill tiền; Slot có số remain = 1 | User A nhấn booking trước sau đó user B nhấn booking | User A book thành công<br>User B báo hết chỗ | - | - | OK staging |
| TC020 | [Salon] Check case calendar setting request booking — Slot remain = 1, 2 user cùng lúc | - | - | Calendar setting **request booking**; Slot có số remain = 1 | Slot có số remain = 1<br>2 user nhấn booking cùng lúc | Cả 2 booking đều book success, trạng thái là request booking | - | - | OK staging |
| TC021 | [Salon] Check calendar có setting bill tiền — Slot không giới hạn | - | - | Calendar **có** setting bill tiền; Slot **không giới hạn** | 2 user nhấn booking cùng lúc | Cả hai booking thành công | - | - | OK staging |
| TC022 | [Salon] Check calendar có setting bill tiền — Slot có số remain = 2 | - | - | Calendar **có** setting bill tiền; Slot có số remain = 2 | 2 user nhấn booking cùng lúc | Cả hai booking thành công | - | - | OK staging |
| TC023 | [Salon] Check calendar có setting bill tiền — Slot remain = 1, 1 user booking | - | - | Calendar **có** setting bill tiền; Slot có số remain = 1 | User A booking | User A booking thành công | - | - | OK staging |
| TC024 | [Salon] Check calendar có setting bill tiền — Slot remain = 1, 2 user booking cùng lúc | - | - | Calendar **có** setting bill tiền; Slot có số remain = 1 | User A và User B nhấn booking cùng lúc | Chỉ 1 booking được tạo, user còn lại nhận thông báo hết chỗ | - | - | OK staging |
| TC025 | [Salon] Check calendar có setting bill tiền — Slot remain = 1, 3 user booking cùng lúc | - | - | Calendar **có** setting bill tiền; Slot có số remain = 1 | 3 user nhấn booking cùng lúc | Chỉ 1 booking được tạo, user còn lại nhận thông báo hết chỗ | - | - | OK staging |
| TC026 | [Salon] Check calendar có setting bill tiền — Slot remain = 1, booking tuần tự | - | - | Calendar **có** setting bill tiền; Slot có số remain = 1 | User A nhấn booking trước sau đó user B nhấn booking | User A book thành công<br>User B báo hết chỗ | - | - | OK staging |

### Environment (note)

Sheet ghi kết quả `OK staging` ⇒ TCs đã chạy trên **Staging** (`staging.lme.jp`).

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

### Base quan điểm test LME (2 tầng)

**Tầng 1 — quan điểm**: [framework/checklist-lme.md](../../framework/checklist-lme.md) (80 quan điểm + 12 RULE).
**Tầng 2 — catalog**: [framework/catalog-lme.md](../../framework/catalog-lme.md).

| Mã quan điểm | Ưu tiên | ◯/× | Catalog đã mở | TC cover | Lý do nếu × |
|---|---|---|---|---|---|
| `<member điền sau khi review>` | | | | | |

- [ ] Đã duyệt **toàn bộ** tầng 1 từ trên xuống, không bỏ nhóm nào
- [ ] Mỗi quan điểm ◯ **đã mở đúng catalog** ở tầng 2
- [ ] Mọi quan điểm ◯ ưu tiên **Cao** có đủ 3 loại case Positive + Negative + Boundary (**RULE-01**)
- [ ] Mọi × đều có lý do; × ở quan điểm **Cao** đã báo Leader duyệt (**RULE-03**)
- [ ] TC có output ra ngoài (LINE app / mail / gateway) → Expected đi tới **output cuối trên thiết bị thật** (**RULE-06**)
- [ ] TC CRUD verify đủ **3 tầng** DB + màn hình + output (**RULE-07**)
- [ ] Task chạm **media / domain / job / loadbalance / bill tiền** → có TC verify **trên Production** (**RULE-08**)
- [ ] Task chạm đối tượng đã từng version-up → test **cả nhánh cũ và mới** (**RULE-09**)
- [ ] Mỗi TC đã ghi **loại evidence bắt buộc** ở Output note (**RULE-02**)

<!-- Source: fetched từ Redmine #38280 journal #125009 (Link testcase). Lesson = Sheet 1337DDgFt-zTLL4OfPg-4JUQ-jOreeiwQIOiV_5eDJIE, tab "Booking phía line user", range A551:M563. Salon = Sheet 1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s, tab "Booking phía line user", range A1397:M1409. Fetch lúc 2026-07-13. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
