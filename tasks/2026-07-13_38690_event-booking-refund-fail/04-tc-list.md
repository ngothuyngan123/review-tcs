<!-- sync-target: https://docs.google.com/spreadsheets/d/1r6N_p59tudrzfEjoK5xrnWQG5oYwv9hM8daBSuM8kLY/edit?gid=29229128#gid=29229128 -->
<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1r6N_p59tudrzfEjoK5xrnWQG5oYwv9hM8daBSuM8kLY/edit?gid=29229128#gid=29229128 | sheet=Task nhỏ + fix bug KH | anchor=Main Function -->

# 04 — TC List (do member viết)

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `Thanh Phương` (người post Link testcase trên Redmine) |
| Ngày submit | `2026-07-13` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1r6N_p59tudrzfEjoK5xrnWQG5oYwv9hM8daBSuM8kLY/edit?gid=29229128#gid=29229128 — tab `Task nhỏ + fix bug KH`, row 296–300 |

---

## TC List

> Fetch **nguyên văn** từ Sheet (row 296–300). Sheet dùng format cột `Main Function / Sub1 / Sub2 / Sub3 / Expect Result / Actual result`, **không có** cột Type / Priority / Steps riêng → các cột đó để `<không có trong Sheet>`.
> Row 295 của Sheet là dòng tiêu đề nhóm: `Bug tự detect #38690: [Event booking] Thao tác refund bị "refund fail"`.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Refund stripe — refund stripe kiểu cũ | `<không có trong Sheet>` | `<không có trong Sheet>` | - charge có dạng ch_<br>Strip_customer_id: cus_S0pwpBofXvUsyz<br>Strip_card_id: card_1R6oGbEojkVpWWGaV2io7Max | `<không có trong Sheet>` | - Check refund success => update trạng thái sang đã refund (check DB có status_payment =2<br>- Check bill tiền trên stripe đã được refund<br>- Check lưu được lịch sử của booking hiển thị ở detail friend | | | OK |
| TC002 | Refund stripe — refund stripe kiểu mới | `<không có trong Sheet>` | `<không có trong Sheet>` | - charge có dạng pi_ | `<không có trong Sheet>` | - Check refund success => update trạng thái sang đã refund (check DB có status_payment =2<br>- Check bill tiền trên stripe đã được refund<br>- Check lưu được lịch sử của booking hiển thị ở detail friend | Actual result (Sheet): `chưa tạo được lịch sử` | | `<trống trong Sheet>` |
| TC003 | Refund stripe — refund chọn option chỉ refund Lme, không refund trên stripe | `<không có trong Sheet>` | `<không có trong Sheet>` | | `<không có trong Sheet>` | - Check refund success => update trạng thái sang đã refund (check DB có status_payment =2<br>- Check bill tiền trên stripe không bị refund<br>- Check lưu được lịch sử của booking hiển thị ở detail friend | | | OK |
| TC004 | Refund univapay — refund univapay | `<không có trong Sheet>` | `<không có trong Sheet>` | | `<không có trong Sheet>` | - Check refund success => update trạng thái sang đã refund (check DB có status_payment =2<br>- Check bill tiền trên univapay đã được refund<br>- Check lưu được lịch sử của booking hiển thị ở detail friend | | | OK |
| TC005 | Refund univapay — refund chọn option chỉ refund Lme, không refund trên univapay | `<không có trong Sheet>` | `<không có trong Sheet>` | | `<không có trong Sheet>` | - Check refund success => update trạng thái sang đã refund (check DB có status_payment =2<br>- Check lưu được lịch sử của booking hiển thị ở detail friend | | | OK |

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). Sheet có cột `staging` — TC nào cần env khác Staging → ghi vào cột **Output note** hoặc **Precondition**.

---

## Member tự check trước khi submit

<member điền sau khi review>

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
- [ ] Mỗi quan điểm ◯ **đã mở đúng catalog** ở tầng 2 và **duyệt hết** khối tương ứng
- [ ] Mọi quan điểm ◯ ưu tiên **Cao** có đủ 3 loại case Positive + Negative + Boundary (**RULE-01**)
- [ ] Mọi × đều có lý do; × ở quan điểm **Cao** đã báo Leader duyệt (**RULE-03**)
- [ ] TC có output ra ngoài → Expected đi tới **output cuối trên thiết bị thật** (**RULE-06**)
- [ ] TC CRUD verify đủ **3 tầng** DB + màn hình + output (**RULE-07**)
- [ ] Task chạm **media / domain / job / loadbalance / bill tiền** → có TC verify **trên Production** (**RULE-08**)
- [ ] Task chạm đối tượng đã từng version-up → test **cả nhánh cũ và mới** (**RULE-09**)
- [ ] Mỗi TC đã ghi **loại evidence bắt buộc** ở Output note (**RULE-02**)

<!-- Source: fetched từ Redmine #38690 Link TCs (journal #125785), range A296:N300 tab "Task nhỏ + fix bug KH" lúc 2026-07-13. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
