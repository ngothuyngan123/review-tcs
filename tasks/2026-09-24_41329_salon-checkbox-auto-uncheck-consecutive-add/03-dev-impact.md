# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41329 (Journal #137865 — báo cáo AI AUTO-FIXBUG) bởi `/new-task`. Tester verify rồi tick checkbox bên dưới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) · Assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `f1c773221f` (repo `sns-line`, 1 file) — chưa có link PR |
| Branch | `ai_fixbug_41329` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-23 |
| Auto-filled | 2026-09-24 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Ở màn Lịch Salon, sau khi thêm đặt lịch thủ công thành công, đoạn code khởi tạo lại form đặt ô 'Tự tính giờ kết thúc theo thời lượng khóa' về trạng thái KHÔNG chọn, trong khi mặc định lúc mở màn là CÓ chọn. Modal dùng lại đúng đối tượng form đó và trang không tải lại, nên từ lần thêm thứ 2 trở đi ô này luôn bị bỏ chọn. Kèm theo đó, khi ô bị bỏ chọn thì việc bấm chọn khung giờ trống chỉ cập nhật giờ bắt đầu mà không cập nhật giờ kết thúc, nên giờ kết thúc còn sót giá trị của lần đặt trước.

## 2. Cách fix

Sửa màn Lịch salon: đoạn khởi tạo lại form sau khi thêm đặt lịch thành công nay đặt ô 'tự tính giờ kết thúc theo thời lượng khóa' về ĐÚNG mặc định là được chọn (trước đó đặt thành bỏ chọn, lệch với giá trị khởi tạo ban đầu của màn). Quét ngang thấy màn Đặt lịch bài học có cùng kiểu lệch ở lựa chọn 'thực hiện action' nhưng khác tính năng nên chỉ ghi nhận, không sửa.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `callAjaxCreateBooking` (public/js/calendar_salon/add-new-booking.js:340) | **Sửa** — reset ô về được chọn | Chỗ reset form sau khi tạo booking thành công |
| 2 | `mixinAddNewBooking.data` (public/js/calendar_salon/add-new-booking.js:9) | Không | Giá trị mặc định của form khi mở màn |
| 3 | `changeFlagUseDurationCourse` (public/js/calendar_salon/add-new-booking.js:115) | Không | Xử lý khi tick/bỏ tick ô |
| 4 | `updateTimeBooking` (public/js/calendar_salon/add-new-booking.js:380) | Không | Tự tính giờ kết thúc theo khóa |
| 5 | `showAddNewBooking` / `showAddNewBookingDay` / `showAddNewBookingWeek` (public/js/calendar_salon/calendar-management.js:1128/1191/1206) | Không | Mở modal, không reset lại ô này |
| 6 | `add_new_booking.blade.php:112-125` | Không | Markup checkbox + khóa ô giờ kết thúc |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev chỉ ghi "File thay đổi"; function map từ mục 3. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `callAjaxCreateBooking` — reset form sau khi tạo booking thành công | public/js/calendar_salon/add-new-booking.js | Direct | Dòng duy nhất bị sửa (diff 1+/1−) |
| F2 | `showAddNewBooking` / `showAddNewBookingDay` / `showAddNewBookingWeek` + `updateTimeBooking` — tính giờ kết thúc khi ô được chọn | public/js/calendar_salon/calendar-management.js · add-new-booking.js | Indirect | Không sửa code; hành vi đổi vì ô nay luôn được chọn ở lần mở thứ 2+ |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có | — | Chỉ đổi trạng thái mặc định của form phía giao diện, không đụng DB. Recover data: ✔ Không cần recover data |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — màn thêm đặt lịch thủ công của lịch salon: ô tự tính giờ kết thúc theo thời lượng khóa giữ đúng mặc định khi thêm nhiều lượt liên tiếp | F1, F2 | <chưa rõ — Dev không ghi mức> |

> Ghi chú Dev (mục 2): màn Đặt lịch bài học (Lesson) có cùng kiểu lệch ở lựa chọn 'thực hiện action' — **chỉ ghi nhận, không sửa**.
> Rủi ro Dev tự nêu: user cố ý bỏ chọn ô để nhập tay giờ kết thúc → lần thêm kế tiếp ô trở lại được chọn (hành vi mặc định, giống màn 予約管理 — không phải hồi quy).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
