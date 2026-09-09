# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee ticket hiện tại: Ngô Thúy Ngần (QA) |
| Commit / Pull Request | commit `b25cd9f78b` (repo `sns-line`) — **không có link PR**. Dashboard: `https://dashboard.melonglobal.net/fixbug-lme/?id=33762` |
| Branch | `ai_fixbug_33762` (nhánh gốc `release_step_20260805`, 2 file, **đã push** lên origin) |
| Ngày submit đánh giá | 2026-08-26 |
| Auto-filled | `2026-09-09 by /new-task` (nguồn: Redmine #33762 journal #133036) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ Đánh giá này do **AI Auto-fixbug sinh tự động**, không phải Dev người viết. Mức verify của Dev chỉ đạt `lint` — **chưa chạy unit test, chưa kiểm chứng bằng DB dev**.

---

## 1. Nguyên nhân

Với remind loại "gửi sau khi kết thúc đặt lịch" của lịch đặt bài học, khi kiểm tra mốc gửi có hợp lệ hay không, code so sánh mốc gửi với giờ BẮT ĐẦU của lượt đặt thay vì giờ KẾT THÚC. Vì vậy remind kiểu ngày với day=0 lúc 15:00 của lượt đặt 17/1 12:00-17:00 vẫn được thêm vào bảng lịch gửi, dù 15:00 vẫn nằm trước lúc lượt đặt kết thúc. Màn đặt lịch salon đã so đúng với giờ kết thúc, chỉ luồng đặt lịch bài học bị lệch.

## 2. Cách fix

Sửa điều kiện hợp lệ của nhắc lịch loại gửi-sau kiểu ngày: so sánh mốc gửi với giờ KẾT THÚC lượt đặt thay vì giờ bắt đầu, tại 2 chỗ thêm lịch gửi của đặt lịch bài học — khi quản trị thêm nhắc lịch cho các lượt đặt đã có (CalendarManagementController) và khi khách/quản trị tạo lượt đặt mới (CalendarCourseBookingService). Mốc gửi rơi trước giờ kết thúc sẽ không còn được ghi vào bảng lịch gửi. Quét ngang: đặt lịch salon đã đúng sẵn; còn tồn luồng CẬP NHẬT nhắc lịch (cả bài học lẫn salon) vốn thiếu hẳn kiểm tra này và màn đặt hẹn bản cũ — để ngoài phạm vi ticket.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarManagementController::addActionRemindNew` — `app/Http/Controllers/Basic/CalendarManagementController.php:919` | **CÓ SỬA** — đổi mốc so sánh sang giờ kết thúc | Luồng admin thêm nhắc lịch cho các lượt đặt đã có |
| 2 | `CalendarManagementController::saveCreateSettingRemind` — `.../CalendarManagementController.php:831` | Đã check | Nơi lưu cấu hình remind mới |
| 3 | `CalendarManagementController::saveSettingSendMessageEventStep` — `.../CalendarManagementController.php:1227` | Đã check | Luồng CẬP NHẬT remind — **thiếu hẳn kiểm tra này, để ngoài phạm vi ticket** |
| 4 | `CalendarCourseBookingService::addActionRemind` — `app/Services/CalendarManagement/CalendarCourseBookingService.php:529` | **CÓ SỬA** — đổi mốc so sánh sang giờ kết thúc | Luồng khách/quản trị tạo lượt đặt mới |
| 5 | `CalendarSalonLineBookingService::addActionRemind` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php:861` | Không sửa | Salon **đã đúng sẵn** (so với giờ kết thúc) — dùng làm đối chứng |
| 6 | `CalendarSalonController::addActionRemindNew` — `app/Http/Controllers/Basic/CalendarSalonController.php:2074` | Không sửa | Salon đã đúng sẵn |
| 7 | `FormAnswerService::addActionRemind` — `app/Services/FormAnswer/FormAnswerService.php:2264` | Không sửa | Caller cùng tên hàm, khác luồng |
| 8 | `ActionBookingCalendar::addActionRemind` — `app/Http/Controllers/ActionBookingCalendar.php:234` | Không sửa | Màn đặt hẹn bản cũ — **để ngoài phạm vi ticket** |
| 9 | `CalendarCourseReception::getEndTimeAttribute` — `app/CalendarCourseReception.php:22` | Không sửa | Accessor trả `end_time` dạng `H:i` — nguồn của mốc so sánh mới |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev **chỉ kê "File thay đổi"**, không kê function-level. Dòng F1/F2 dưới đây suy từ mục 2 + mục 3 (2 chỗ Dev nói rõ đã sửa).

**Nguyên văn Dev — 4.1 File thay đổi:**
- `app/Http/Controllers/Basic/CalendarManagementController.php`
- `app/Services/CalendarManagement/CalendarCourseBookingService.php`

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarManagementController::addActionRemindNew` | `app/Http/Controllers/Basic/CalendarManagementController.php` | Direct | Admin thêm nhắc lịch cho các lượt đặt đã có (màn cấu hình remind) |
| F2 | `CalendarCourseBookingService::addActionRemind` | `app/Services/CalendarManagement/CalendarCourseBookingService.php` | Direct | Khách/quản trị tạo lượt đặt mới — dùng chung cho **thêm booking thủ công · duyệt yêu cầu đặt lịch · khách LINE tự đặt** |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `event_step_time` | CREATE (bị chặn bớt) | Từ nay không còn thêm bản ghi nhắc lịch gửi-sau có mốc gửi trước giờ kết thúc lượt đặt. **Các bản ghi sai đã tạo trước đây vẫn còn** (xem mục 5 Recover data) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lesson / Calendar Booking (**FA-019**) | F1, F2, D1 | *Dev không ghi mức* — nhắc lịch gửi sau khi kết thúc lượt đặt bài học chỉ được lên lịch khi mốc gửi nằm sau giờ kết thúc |
| T2 | Reminder Delivery (**FA-022**) | D1 | *Dev không ghi mức* — bảng lịch gửi nhắc không còn sinh bản ghi sai mốc cho loại gửi-sau |

---

## 5. Recover data (nguyên văn Dev)

⚠ **CÓ** — Các bản ghi lịch gửi sai đã tạo trước fix vẫn nằm trong bảng `event_step_time` và **sẽ vẫn được gửi sớm**. Rà bằng câu SELECT các bản ghi chưa gửi (`status = 0`) của nhắc lịch bài học loại gửi-sau kiểu ngày mà mốc gửi < giờ kết thúc lượt đặt (nối `event_step_time` > `calendar_course_bookings` > `calendar_course_receptions`), rồi xoá nếu xác nhận sai.

Phạm vi: `event_step_time` của các nhắc lịch (`event_step`) có `is_after_day=1`, `type_remind=1` thuộc sự kiện đặt lịch bài học (`events.type=4`), `status=0`.

## 6. Verify của Dev (nguyên văn)

- **Mức: `lint`** (không phải unit test / integration).
- `php -l app/Services/CalendarManagement/CalendarCourseBookingService.php`: No syntax errors detected
- `php -l app/Http/Controllers/Basic/CalendarManagementController.php`: No syntax errors detected
- `git diff --stat release_step_20260805...ai_fixbug_33762`: đúng 2 file, 2 dòng đổi
- ⚠️ **Chưa chạy unit test** — chỗ sửa nằm trong hàm truy vấn/ghi DB trực tiếp, không phải logic thuần.
- ⚠️ **Chưa kiểm chứng bằng DB dev** — kết nối `host.docker.internal:3306` bị từ chối.

**Bằng chứng Dev đưa ra:**
- Biến `$time_end_booking` đã có sẵn trong cả 2 hàm (dùng cho nhánh đếm ngược), chỉ nhánh kiểu ngày dùng nhầm `$time_start_booking`.
- Luồng đặt lịch salon (`CalendarSalonLineBookingService:897`, `CalendarSalonController:2107`) gán mốc so sánh = giờ kết thúc khi `is_after_day=1` — xác nhận quy tắc đúng là so với giờ kết thúc.
- `calendar_course_receptions.start_time/end_time` là kiểu `TIME`, model trả về dạng `H:i` qua accessor nên chuỗi ngày-giờ ghép ra đúng định dạng.

## 7. Tự review của AI — rủi ro khi test (nguyên văn)

Sửa 1 dòng ở mỗi luồng thêm lịch gửi của đặt lịch bài học, đổi mốc so sánh từ giờ bắt đầu sang giờ kết thúc lượt đặt cho nhắc lịch gửi-sau kiểu ngày. Biến giờ kết thúc đã tồn tại sẵn trong cả 2 hàm nên không phát sinh truy vấn hay thay đổi cấu trúc. Nhánh gửi-trước và nhánh đếm ngược giữ nguyên. Đối chiếu với luồng đặt lịch salon (đã đúng) để xác nhận quy tắc.

**Rủi ro / lưu ý khi test:**
- Nhắc lịch gửi-sau đặt vào khung giờ nằm giữa lượt đặt sẽ không còn được lên lịch — đây chính là hành vi mong đợi, nhưng nếu khách đang cố tình dùng kiểu này thì **số nhắc lịch sinh ra sẽ giảm**.
- Trường hợp **lượt đặt kết thúc qua nửa đêm** (giờ kết thúc nhỏ hơn giờ bắt đầu) vẫn ghép giờ kết thúc với ngày đặt như code cũ ở nhánh đếm ngược — không đổi so với hiện trạng.
- **Bản ghi sai tạo trước fix vẫn còn**, cần rà tay theo mục 5.

## 8. Ngoài phạm vi ticket (Dev tự khai)

| Luồng | Trạng thái |
|---|---|
| Đặt lịch **salon** | Đã đúng sẵn từ trước — dùng làm đối chứng |
| Luồng **CẬP NHẬT** nhắc lịch (cả bài học lẫn salon) | **Thiếu hẳn kiểm tra này** — để ngoài phạm vi ticket |
| Màn **đặt hẹn bản cũ** (`ActionBookingCalendar`) | Để ngoài phạm vi ticket |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
