# 03 — Đánh giá ảnh hưởng từ Dev

> **Nguồn**: journal `#133021` của Redmine [#28450](https://redmine.watermelon.vn/issues/28450), ngày 2026-08-26, tác giả **AI LME Fix bug** (hệ thống Auto-fixbug LME).
> Báo cáo gốc dùng format 6 mục của Auto-fixbug (1 Nguyên nhân · 2 Cách fix · 3 Đã check · 4 Đánh giá ảnh hưởng · 5 Recover data · 6 Verify) — đã map sang 4 mục của template; mục 5/6 + tự review giữ nguyên ở phần "Phụ lục" cuối file.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assigned_to trên Redmine: `Ngô Thúy Ngần` |
| Commit / Pull Request | commit `f96d79b095` (repo `sns-line`, 1 file changed, 18 insertions(+), 8 deletions(-)) — không có link PR trong Redmine |
| Branch | `ai_fixbug_28450` (nhánh gốc `release_step_20260805`) — đã push lên origin |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-09-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "1. NGUYÊN NHÂN" của báo cáo Auto-fixbug. -->

Ở màn danh sách khóa (course) của Lịch salon, luồng TẠO MỚI khóa có bước đồng bộ: quét các nhân viên đang bật "chọn tất cả khóa" rồi thêm id khóa mới vào danh sách khóa của họ. Nhưng luồng COPY khóa đi nhánh code riêng, chỉ nhân bản bản ghi khóa (kèm ảnh, điều kiện lọc, action) mà BỎ QUA hoàn toàn bước đồng bộ này. Hậu quả: khóa vừa copy không nằm trong danh sách khóa của bất kỳ nhân viên nào bật "chọn tất cả khóa", nên khóa đó không có nhân viên đối ứng và khách không đặt lịch được.

## 2. Cách fix

<!-- Nguyên văn mục "2. CÁCH FIX" của báo cáo Auto-fixbug. -->

Tách đoạn đồng bộ "thêm id khóa mới vào danh sách khóa của các nhân viên đang bật chọn-tất-cả-khóa" (vốn chỉ nằm trong nhánh tạo mới) thành hàm dùng chung `addCourseToStaffsSelectedAllCourse`, rồi gọi hàm này SAU khi lưu khóa cho CẢ hai nhánh tạo mới và copy trong `CalendarSalonCourseService::storeCourse`. Thêm chốt bỏ qua nếu id khóa đã có sẵn trong danh sách để không ghi trùng. Quét ngang: còn 1 luồng tạo khóa khác (wizard tạo lịch salon) thiếu cùng bước đồng bộ này nhưng ngoài phạm vi ticket — đã ghi chú để xử lý riêng.

> ⚠️ **Yokoten còn hở**: luồng wizard tạo lịch salon (`createCourse`) VẪN thiếu bước đồng bộ này — Dev khai báo ngoài phạm vi ticket, chưa fix.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục "3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN". Cột "Thay đổi" suy từ mục 4.1 (chỉ 1 file thay đổi) — tester verify lại bằng diff. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonCourseService::storeCourse` — `app/Services/CalendarSalon/CalendarSalonCourseService.php` | **Có** — chuyển lời gọi đồng bộ ra sau khối if/else để áp cho cả 2 nhánh | Nhánh copy (`item_copy`) vs nhánh tạo mới — đúng chỗ phát sinh bug |
| 2 | `CalendarSalonCourseService::addCourseToStaffsSelectedAllCourse` — cùng file | **Có** — hàm MỚI, tách từ logic cũ của nhánh tạo mới + thêm chốt chống ghi trùng id | Hàm dùng chung cho 2 nhánh |
| 3 | `CalendarSalonCourseService::createCourse` — cùng file | Không đổi | Luồng tạo khóa của wizard — **ghi nhận yokoten**, thiếu cùng bước đồng bộ, ngoài phạm vi ticket |
| 4 | `CalendarSalonController::createCourseSalon` — `app/Http/Controllers/Basic/CalendarSalonController.php` | Không đổi | Endpoint nhận cả tạo mới lẫn copy |
| 5 | `CalendarSalonController::saveStaff` — cùng file | Không đổi | Nơi định nghĩa ngữ nghĩa chọn-tất-cả-khóa = danh sách toàn bộ khóa (cũng là đường recover data) |
| 6 | `copyItemCourse` — `public/js/calendar_salon/calendar_detail.js` | Không đổi | Nút "Sao chép khóa" phía giao diện (trigger FE) |
| 7 | `CalendarSalonLineBookingService::getListStaffCanBook` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Không đổi | Nơi đọc danh sách khóa của nhân viên để lọc người đối ứng (consumer của `course_ids`) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Báo cáo Auto-fixbug mục 4.1 chỉ liệt kê FILE thay đổi (1 file). Bảng dưới ghép mục 4.1 + mục 3; cột Direct/Indirect do /new-task suy ra (Dev không phân loại) — tester verify. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarSalonCourseService::storeCourse` | `app/Services/CalendarSalon/CalendarSalonCourseService.php` | Direct | File DUY NHẤT bị sửa. Lời gọi đồng bộ chuyển ra sau if/else → áp cho cả nhánh tạo mới lẫn copy |
| F2 | `CalendarSalonCourseService::addCourseToStaffsSelectedAllCourse` | cùng file F1 | Direct | Hàm mới. Chứa vòng lặp quét staff `is_all_course=1` + chốt chống ghi trùng id |
| F3 | `CalendarSalonCourseService::createCourse` (wizard tạo lịch salon) | cùng file F1 | Indirect | **Chưa fix** — vẫn thiếu bước đồng bộ (yokoten ngoài phạm vi ticket) |
| F4 | `CalendarSalonController::createCourseSalon` (endpoint POST tạo/copy khóa) | `app/Http/Controllers/Basic/CalendarSalonController.php` | Indirect | Không sửa code nhưng là đường vào của cả 2 nhánh → mọi TC copy/tạo mới đi qua đây |
| F5 | `CalendarSalonController::saveStaff` | cùng file F4 | Indirect | Định nghĩa ngữ nghĩa "chọn tất cả khóa"; là đường re-save để recover data cũ |
| F6 | `copyItemCourse` (FE) | `public/js/calendar_salon/calendar_detail.js` | Indirect | Nút "Sao chép khóa" gửi `item_copy` — trigger phải phát sinh từ UI thật |
| F7 | `CalendarSalonLineBookingService::getListStaffCanBook` | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Indirect | Đọc `course_ids` để lọc nhân viên đối ứng → nơi bug lộ ra với end-user |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục "4.2 Data ảnh hưởng". -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_staff.course_ids` | UPDATE | Từ sau khi fix, khóa copy được ghi thêm vào danh sách. Các khóa **ĐÃ copy trước đây vẫn thiếu id**, cần bổ sung thủ công (xem Phụ lục A — Recover data) |

**Ràng buộc schema** (từ mục Verify của báo cáo): `calendar_salon_staff.is_all_course` = `tinyint` (0: subset theo `course_ids`, 1: all) · `calendar_salon_staff.course_ids` = `varchar(255)` chứa CSV id khóa.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục "4.3 Tính năng liên quan". Cột "Nguy cơ regression" do /new-task suy ra (Dev không ghi mức) — tester verify. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Salon Booking (FA-021)** — khóa salon vừa copy được gán đúng cho nhân viên phụ trách nên khách đặt lịch được | F1, F2, F7, D1 | High |
| T2 | **Salon Staff Management** (outside glossary) — danh sách khóa của nhân viên bật chọn-tất-cả-khóa luôn khớp với danh sách khóa thực tế của lịch | F2, F5, D1 | Medium |
| T3 | **Tạo mới khóa** (nhánh else, đã refactor sang hàm dùng chung) | F1, F2, D1 | Medium — hành vi phải giữ nguyên như trước fix |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

---

# Phụ lục — nội dung ngoài 4 mục template (nguyên văn báo cáo Auto-fixbug)

## A. RECOVER DATA

⚠ **CÓ** — Các khóa đã được copy TRƯỚC khi có fix vẫn thiếu id trong `calendar_salon_staff.course_ids` của những nhân viên bật `is_all_course=1`. Fix chỉ áp cho lần copy mới, không tự vá dữ liệu cũ.

**Cách bổ sung**: với mỗi lịch salon, ghi lại `course_ids` của nhân viên có `is_all_course=1` thành danh sách đầy đủ id khóa hiện có của lịch đó (đúng ngữ nghĩa mà màn lưu nhân viên vẫn dùng). Có thể làm nhanh nhất bằng cách **mở màn nhân viên, lưu lại (re-save)** là hệ thống tự ghi đủ danh sách.

**Phạm vi**: bảng `calendar_salon_staff`, các bản ghi `is_all_course = 1` thuộc lịch salon từng có thao tác copy khóa.

## B. VERIFY (mức độ kiểm chứng của Dev)

| Trường | Nội dung |
|---|---|
| Mức | **lint** |
| Lệnh | `php -l app/Services/CalendarSalon/CalendarSalonCourseService.php` → No syntax errors detected · `git diff --stat origin/release_step_20260805...ai_fixbug_28450` → 1 file changed, 18 insertions(+), 8 deletions(-) — chỉ đúng file fix · Đối chiếu code trên `origin/release_step_20260805`: xác nhận nhánh copy (`item_copy`) trên release hiện hành VẪN thiếu bước đồng bộ → bug còn tồn tại, fix áp đúng chỗ |
| Bằng chứng | Ngữ nghĩa chọn-tất-cả-khóa được chốt tại `CalendarSalonController::saveStaff`: khi bật thì `course_ids` = toàn bộ id khóa của lịch → khóa mới/copy bắt buộc phải được thêm vào · Schema `calendar_salon_staff.sql`: `is_all_course` tinyint (0: subset theo course_ids, 1: all), `course_ids` varchar(255) CSV id khóa · **Không tái hiện được trên dev** (MySQL `host.docker.internal:3306` Connection refused) — bug thuần cấu trúc code nên xác định bằng đối chiếu 2 nhánh tạo mới vs copy |

> ⚠️ Mức verify chỉ đạt **lint + đọc code**, KHÔNG có run thực tế trên môi trường có DB. Toàn bộ hành vi runtime chưa được Dev chứng minh.

## C. Tự review của AI + rủi ro khi test (nguyên văn)

Fix bám đúng yêu cầu ticket: cho luồng copy khóa dùng CHUNG bước đồng bộ với luồng tạo mới, thay vì viết lại logic riêng. Đặt lời gọi sau khối if/else nên mọi đường tạo khóa qua `storeCourse` (tạo mới lẫn copy) đều được xử lý, tránh tái diễn kiểu bỏ sót nhánh. Hành vi luồng tạo mới không đổi (cùng truy vấn, cùng cách ghi), chỉ thêm chốt chống ghi trùng id. Phạm vi ảnh hưởng gọn: 1 file service, không đụng controller/giao diện, không đổi cấu trúc dữ liệu.

**Rủi ro / lưu ý khi test** (Dev tự nêu — là nguồn quan điểm test tốt):

| # | Rủi ro | Chi tiết |
|---|---|---|
| R1 | **Tràn `varchar(255)`** | `course_ids` là chuỗi CSV giới hạn 255 ký tự: lịch có rất nhiều khóa (trần 200 khóa/lịch) thì chuỗi có thể bị **cắt** khi ghi. Đây là hạn chế sẵn có của thiết kế cột, luồng tạo mới cũng dính, fix này không làm xấu thêm |
| R2 | **Race condition (đọc-rồi-ghi)** | Không phải cập nhật nguyên tử: nếu hai người cùng lúc tạo/copy khóa trên cùng lịch thì một id có thể bị **mất**. Rủi ro thấp vì đây là thao tác quản trị thủ công, và hành vi này giống hệt luồng tạo mới vốn có |
| R3 | **Dữ liệu cũ** | Khóa đã copy trước fix vẫn thiếu id — cần bổ sung riêng, xem Phụ lục A |

## D. Branch / commit để QA checkout

| Repo | Branch | Nhánh gốc | Commit | Trạng thái |
|---|---|---|---|---|
| `sns-line` | `ai_fixbug_28450` | `release_step_20260805` | `f96d79b095` (1 file) | đã push |

- Thời gian AI xử lý: 4 phút 38 giây
- Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=3ebc50b2-bfdf-4eea-9f11-90922303ef43
- Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=28450
