# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (Ngô Thúy Ngần — assignee)` |
| Commit / Pull Request | `sns-line: ai_small_39008 — commit 1dfa4ac55e (4 file)` |
| Branch | `ai_small_39008` (nhánh gốc `release_step_20260930`) |
| Ngày submit đánh giá | `2026-09-30` |
| Auto-filled | `2026-09-30 by /new-task` |

<!-- Nguồn: Redmine #39008, Journal #139439 (2026-09-30) — bản fix MỚI NHẤT/ACTIVE, dựng lại trên release hiện hành sau khi bản đầu (Journal #130742, 2026-08-20, branch ai_fixbug_39008 trên release_step_20260623) bị trễ 2 release. -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Yêu cầu cải tiến giao diện lịch salon: trong hộp thoại cảnh báo khi kết nối Google Calendar bị ngắt, dòng chữ phụ chỉ đóng hộp thoại mà không làm gì, nên người dùng vẫn kẹt ở trạng thái lỗi và không có cách nào dọn dẹp kết nối hỏng ngay tại đó. Khách hàng yêu cầu đổi dòng này thành thao tác đặt lại cài đặt kết nối Google Calendar, có hộp thoại xác nhận, và khi thực hiện thì bắt buộc hủy kết nối Google Calendar của nhân viên tương ứng (nhân viên đang ở trạng thái mất kết nối trên lịch đó).

## 2. Cách fix

Dựng lại branch `ai_small_39008` trên release hiện hành `release_step_20260930` (bản cũ base `release_step_20260805`, đã trễ 2 release). Nội dung fix giữ nguyên: đổi dòng chữ trong hộp thoại cảnh báo mất kết nối Google Calendar (màn chi tiết lịch salon) thành thao tác đặt lại cài đặt kết nối; thêm hộp thoại xác nhận đúng design (biểu tượng cảnh báo + tiêu đề + cảnh báo lịch trên hệ thống sẽ bị xóa + 2 nút Đóng / Đặt lại cài đặt màu đỏ); khi xác nhận thì gọi endpoint mới hủy kết nối Google Calendar của mọi nhân viên đang lỗi kết nối trên đúng lịch đó (lọc kèm bot) rồi tải lại trang.

**Conflict khi chuyển base**: release mới đã đổi mã lỗi của luồng hủy liên kết từ 500 sang mã do service trả về (mặc định 422) — giữ hành vi mới của release ở endpoint public, còn hàm dùng chung trả thẳng kết quả cho caller tự dựng response.

**Rủi ro / lưu ý khi test (Dev tự nêu)**:
- Thao tác đặt lại **xóa lịch đã đồng bộ hai chiều** của nhân viên đang lỗi — đúng như cảnh báo hiển thị trong hộp thoại xác nhận, nhưng **không hoàn tác được**; đã đặt sau một bước xác nhận rõ ràng.
- Nếu một lịch có **nhiều nhân viên cùng mất kết nối** thì thao tác này **hủy kết nối tất cả** các nhân viên đó (đây chính là nhóm gây ra cảnh báo); nếu vận hành muốn chỉ hủy đúng một người thì cần bổ sung chọn nhân viên (**chưa có** ở bản fix này).
- Luồng hủy gọi tới Google cho từng lượt đặt đã đồng bộ, lịch nhiều dữ liệu có thể chạy lâu — đặc tính này **có sẵn từ nút hủy liên kết cũ**, không phát sinh thêm do thay đổi này.
- **Không kiểm chứng được bằng dữ liệu dev** vì MySQL dev (`host.docker.internal:3306`) từ chối kết nối lúc chạy → verify chỉ dừng ở mức lint/compile/route/reflection, **chưa chạy runtime thật**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonController::detailCalendar` (`app/Http/Controllers/Basic/CalendarSalonController.php`) | Không đổi logic, chỉ là nơi tính cờ báo lỗi kết nối để bật hộp thoại cảnh báo | Đã check để xác nhận cờ hiển thị modal không đổi |
| 2 | `CalendarSalonController::deleteGoogleSyncLink` (`app/Http/Controllers/Basic/CalendarSalonController.php`) | Refactor: nay gọi hàm dùng chung `unlinkGoogleCalendarOfStaff` thay vì code inline | Tách logic dùng chung, giữ nguyên hành vi HTTP/response cũ |
| 3 | `CalendarSalonController::unlinkGoogleCalendarOfStaff` (`app/Http/Controllers/Basic/CalendarSalonController.php`) | **Hàm mới** (private, dùng chung) — hủy kết nối Google Calendar 1 nhân viên | Tách từ logic hủy liên kết sẵn có để 2 endpoint (hủy đơn lẻ cũ + reset mới) cùng dùng |
| 4 | `CalendarSalonController::resetGoogleCalendarConnectionOnError` (`app/Http/Controllers/Basic/CalendarSalonController.php`) | **Endpoint mới** (public) — đặt lại kết nối cho mọi nhân viên lỗi trên lịch (lọc theo bot) | Endpoint chính của tính năng mới |
| 5 | `CalendarSalonService::getStaffIdsGoogleCalendarDisconnected` (`app/Services/CalendarSalon/CalendarSalonService.php`) | **Hàm mới** — truy vấn nhân viên đang mất kết nối, có lọc bot | Xác định đúng phạm vi nhân viên bị hủy kết nối |
| 6 | `CalendarSalonService::deleteGoogleSyncLink` (`app/Services/CalendarSalon/CalendarSalonService.php`) | Không đổi | Đã check — xóa bản ghi liên kết, dùng lại nguyên logic cũ |
| 7 | `CalendarSalonGoogleCalendarService::deleteBookingSyncFromLme` (`app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php`) | Không đổi | Đã check — xóa lịch đã đẩy sang Google, dùng lại nguyên logic cũ |
| 8 | `CalendarSalonBookingByGoogleService::deleteBookingByGoogleCalendar` (`app/Services/CalendarSalon/CalendarSalonBookingByGoogleService.php`) | Không đổi | Đã check — xóa lịch lấy về từ Google, dùng lại nguyên logic cũ |
| 9 | `routes/web.php` | Thêm route `POST /ajax/calendar-salon/action/google-sync/reset-on-error` | Route mới cho endpoint reset |
| 10 | `resources/views/basic/calendar_salon/detail.blade.php` | Đổi text nút phụ + thêm modal xác nhận + JS gọi endpoint reset | UI thay đổi theo yêu cầu |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `resetGoogleCalendarConnectionOnError` (endpoint mới, route `POST /ajax/calendar-salon/action/google-sync/reset-on-error`) | `CalendarSalonController.php` + `routes/web.php` | Direct | Hủy kết nối Google Calendar TẤT CẢ nhân viên đang lỗi trên lịch (lọc theo bot), không hủy chọn lọc từng người |
| F2 | `unlinkGoogleCalendarOfStaff` (hàm dùng chung mới, private) | `CalendarSalonController.php` | Direct | Dùng chung bởi cả endpoint reset mới VÀ endpoint hủy liên kết cũ |
| F3 | `deleteGoogleSyncLink` (endpoint hủy liên kết cũ ở tab cài đặt liên kết Google Calendar) | `CalendarSalonController.php` | Indirect | Refactor delegate sang F2 — Dev khẳng định "giữ nguyên hành vi và phản hồi cũ" |
| F4 | `getStaffIdsGoogleCalendarDisconnected` (query mới) | `CalendarSalonService.php` | Direct | Lọc kèm `bot_id` — Dev khẳng định "không chạm dữ liệu bot khác" |
| F5 | Mã lỗi HTTP của luồng hủy liên kết (conflict khi rebase base) | `CalendarSalonController.php` | Indirect | Đổi từ 500 → mã do service trả (mặc định 422) ở **endpoint public**; hàm dùng chung (F2) trả thẳng kết quả cho caller tự dựng response — 2 endpoint (F1 reset mới, F3 hủy cũ) có thể set mã lỗi khác nhau nếu tự dựng response khác nhau |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `b_c_salon_google_calendar` | DELETE | Xóa bản ghi liên kết Google Calendar của nhân viên đang mất kết nối trên lịch salon đó |
| D2 | `calendar_salon_booking_by_google` | DELETE | Xóa lịch chặn (booking) lấy về từ Google của nhân viên đó |
| D3 | `calendar_salon_sync_booking_google_calendar_history` | DELETE | Xóa lịch sử đồng bộ của nhân viên đó |
| D4 | `calendar_salon_line_booking.google_event_id` / `.google_calendar_id` | UPDATE | Đặt về rỗng cho các lượt đặt (booking LINE user) đã đẩy sang Google |
| D5 | `result_error_googles.status` | UPDATE | Đánh dấu `4` (đã xử lý) cho bản ghi lỗi Google của nhân viên đó |
| D6 | `b_c_salon_google_calendar_histories` | CREATE | Thêm bản ghi lịch sử ghi nhận đã hủy kết nối tài khoản Google |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — hộp thoại cảnh báo mất kết nối Google Calendar ở màn chi tiết lịch salon | F1, F2, F4, D1-D6 | High — thao tác mới, xóa data không hoàn tác, hủy TẤT CẢ nhân viên lỗi cùng lúc (không chọn lọc) |
| T2 | Salon Booking (FA-020) — nút hủy liên kết tài khoản Google trong tab cài đặt liên kết Google Calendar (đơn lẻ, luồng cũ) | F2, F3, F5 | Medium — refactor dùng chung hàm mới, Dev khẳng định giữ nguyên hành vi nhưng chưa verify runtime (không kết nối được MySQL dev) |
| T3 | Đồng bộ 2 chiều Google Calendar (booking LINE user đã đẩy sang Google) | D2, D3, D4 | Medium — booking đã sync bị xóa liên kết khi reset, ảnh hưởng cả phía LINE user booking lẫn phía admin xem lịch |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
