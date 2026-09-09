<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/11s9nRImqzWZM6-i2LH4luN89FudC2VR4sRJOkr8o8qc/edit?gid=242730884 | sheet=Lesson | anchor=Main Function -->

# 04 — TC List (fetched từ Redmine Link TCs — read-only)

> ⚠️ TCs này **fetch từ Google Sheet** (member đã viết), giữ NGUYÊN giá trị. KHÔNG sửa Title/Expected dù bug fix đổi behavior. Đây là **input cho `/review-tc`**.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` (fetch từ Sheet Lesson) |
| Ngày submit | `<member điền>` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/11s9nRImqzWZM6-i2LH4luN89FudC2VR4sRJOkr8o8qc/edit?gid=242730884 (sheet Lesson, row 714~737) |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-01 | Xóa Lesson Reception trên App khi reception có booking | Fix | | Tạo Lesson, Reception có 1 booking, có mobile_notify type=11 chưa đọc | 1. Mở App<br>2. Xóa Reception | Reception bị soft delete.<br>Booking bị soft delete.<br>mobile_notify tương ứng bị xóa (Chỉ xóa các notify có is_comfirm =0)<br>Badge notification giảm đúng. | | | OK Staging |
| TC-02 | Xóa Lesson Reception trên App khi reception có nhiều booking | Fix | | Reception có nhiều booking và nhiều mobile_notify | Xóa Reception | Tất cả booking bị soft delete.<br>Xóa các mobile_notify của booking và có is_comfirm =0 | | | OK Staging |
| TC-03 | Badge notification sau khi xóa reception | Fix | | Có badge = số notification lesson | Xóa Reception trên App | Badge giảm đúng bằng số notification đã xóa. | | | OK Staging |
| TC-04 | Danh sách Notification sau khi xóa reception | Fix | | Có notification lesson chưa đọc | Xóa Reception | Notification của booking bị xóa không còn hiển thị trong danh sách. | | | OK Staging |
| TC-05 | Kiểm tra DB sau khi xóa reception | Fix | | Có booking và mobile_notify | Xóa Reception | calendar_course_bookings.deleted_at được set.<br>mobile_notify bị delete. | | | OK Staging |
| TC-06 | Kiểm tra DB sau khi xóa reception | Fix | | Check không bị xóa nhầm các notify không phải của các booking bị xóa | Xóa Reception | - Các notify của reception khác giữ nguyên<br>- các notify của tính năng khác giữ nguyên (check notify của salon không bị xóa) | | | OK Staging |
| TC-07 | Kiểm tra botId được suy ra từ CalendarManagement | Fix | | Có calendar_management.bot_id | Xóa Reception qua App | mobile_notify được xóa đúng bot_id tương ứng. | | | OK Staging |
| TC-08 | Xóa reception trên app | Fix | | reception có 1 booking ở trạng thái chưa cancel | | Khi xóa sẽ báo lỗi, không cho phép xóa<br>=> Notify giữ nguyên không xóa | | | OK Staging |
| TC-09 | Xóa Reception trên Web | Regression | | Có booking | Xóa Reception trên Web | Hành vi giống trước fix.<br>Booking và notification được xóa đúng. | | | OK Staging |
| TC-10 | deleteList() trên Web | Regression | | Có nhiều reception | Xóa nhiều reception | Hoạt động như trước, không phát sinh lỗi. | | | OK Staging |
| TC-11 | Badge sau khi xóa reception trên Web | Regression | | Có notification | Xóa Reception | Badge giảm đúng như version cũ. | | | OK Staging |
| TC-12 | Reception không có booking | Negative | | Reception chưa ai đặt | Xóa Reception | Reception bị xóa thành công.<br>Không phát sinh lỗi. | | | OK Staging |
| TC-13 | Booking đã bị soft delete trước | Negative | | Booking deleted_at != null | Xóa Reception | Không lỗi, không còn notification orphan. | | | OK Staging |
| TC-14 | Không tìm thấy CalendarManagement | Negative | | Calendar bị thiếu dữ liệu | Xóa Reception | API xử lý an toàn, không crash. | | | OK |
| TC-15 | botId không tìm thấy | Negative | | CalendarManagement.bot_id null | Xóa Reception | Không phát sinh exception, xử lý theo thiết kế. | | | OK |
| TC-16 | Chạy SQL recovery với orphan notification | Data Recovery | | DB có orphan mobile_notify | Thực hiện SQL recovery | Các orphan notification bị xóa. | recover check sau | | Not test |
| TC-17 | Kiểm tra badge sau recovery | Data Recovery | | Badge đang bị kẹt | Refresh App | Badge trở về đúng số notification thực tế. | | | Not test |
| TC-18 | Notification hợp lệ không bị xóa | Data Recovery | | Có notification còn booking | Chạy SQL recovery | Notification hợp lệ vẫn tồn tại. | | | Not test |
| TC-19 | Notification type khác 11 | Data Recovery | | Có notification type khác | Chạy recovery | Không bị ảnh hưởng (trừ khi có xử lý type=10). | | | Not test |
| TC-20 | Lesson Booking bình thường sau fix | Compatibility | | User đặt lesson mới | Đặt booking | Notification mới vẫn được tạo bình thường. | | | OK Staging |
| TC-21 | Notification mới sau khi xóa reception khác | Compatibility | | Tạo booking mới sau khi đã xóa reception cũ | Booking mới | Notification hoạt động bình thường. | | | OK Staging |
| TC-22 | Notification đọc/chưa đọc | Compatibility | | Có notification mới | Đọc notification | Trạng thái đọc hoạt động bình thường. | | | OK Staging |
| TC-23 | Xóa Reception có 100 booking | Performance | | Reception có nhiều booking | Xóa Reception | Hoàn thành trong thời gian chấp nhận được, không timeout. | | | OK |
| TC-24 | Xóa nhiều reception liên tiếp | Performance | | Có nhiều reception | Xóa liên tục | Không phát sinh notification orphan. | | | OK Staging |

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). Bug này **chỉ tái hiện khi thao tác trên APP mobile** (session web rỗng) → TC "Fix" cần test trên app; TC "Regression" test trên web.

---

## Member tự check trước khi submit

`<member điền sau khi review>`

<!-- Source: fetched từ Redmine #38208 Link TCs (journal 124422), range A714:J737 tab "Lesson" (gid=242730884) lúc 2026-07-01. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
