# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI) |
| Commit / Pull Request | `sns-line@02a6a660abe8` (v1–v5, LINE/job) → `sns-line@85e13c53dc20` / `sns-line@0b96e9991592` (bổ sung màn quản trị) |
| Branch | `ai_studio_fixbug_43379` (gốc `release_step_20260930_v2` @`d137c1851896`) |
| Ngày submit đánh giá | 2026-10-19 |
| Auto-filled | `2026-10-19 by /new-task` (tổng hợp từ journal #145075, #145248, #145315, #145324 của Redmine #43379 — Redmine không có section "Đánh giá ảnh hưởng" độc lập trong description) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại journal Dev Studio trên Redmine #43379 và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ Task có **2 root cause nối tiếp**: (a) lỗi gốc khớp đúng bug khách báo (LINE hiển thị sai khung trống) — Dev sửa ở v1–v5; (b) lỗi QA phát hiện trong lúc test v1–v5 — màn quản trị xem ngày **lệch ngược** so với LINE sau khi (a) được sửa — Dev sửa thêm ở vòng cuối (journal #145315/#145324). Cả 2 đã gộp vào 1 branch `ai_studio_fixbug_43379`.

---

## 1. Nguyên nhân

**(a) LINE / job phân bổ — nguyên nhân gốc, khớp bug khách báo (#145075, bổ sung biên nửa đêm ở #145248):**

Ở lịch salon nhiều nhân viên có course và giới hạn theo từng nhân viên, khi khách chọn nhân viên + course trên LINE, số chỗ được tính từ nhóm nhân viên làm được course đó. Nhưng mọi đơn 指定なし (staff_id = 0) của **mọi course** đều bị trừ vào số chỗ này. Vì vậy một đơn 指定なし của course mà nhân viên được chọn **không làm được** vẫn chiếm suất duy nhất của người đó, nên khung trống bị ẩn và khi đặt bị báo hết chỗ. Lỗi nằm ở `Mobile\CalendarSalonController` (`getListTimeBooking`, `showTimeBookingMonth`, `checkCanBooking`) cùng `CalendarSalonLineBookingService::checkLimitHasStaff`; cách lọc này có từ tháng 02/2025.

Bổ sung (biên nửa đêm, #145248): Màn tuần và màn tháng chỉ dựng dữ liệu xét đơn 指定なし đến ngày cuối của khoảng xem. Khi ca vắt qua nửa đêm (Chủ nhật → thứ Hai tuần sau, ngày cuối → ngày 1 tháng sau), lưới giờ nạp thêm ca ngày kế tiếp nhưng dữ liệu đơn 指定なし của ngày đó không có → hàm `canPoolServeNoStaffBooking` coi như không ai trong nhóm có ca và **bỏ** đơn 指定なし, trong khi suất của người trong nhóm vẫn được cộng → có thể mở khung **quá suất**.

**(b) Màn quản trị xem ngày — lệch ngược, phát sinh khi QA test (a) (#145315, #145324):**

`CalendarSalonStaffService::checkReasonBookingWithSettingSeason` đếm **mọi** đơn 指定なし của lịch vào suất, rồi chặn khi tổng suất còn lại của nhân viên đang có ca ≤ số đơn đó — không xét có ai đang làm việc làm được course của đơn đó không. Kịch bản QA chốt (TungKS): NV-a nghỉ, NV-b không làm course A → đơn 指定なし course A không ai nhận được nhưng vẫn chiếm suất duy nhất của NV-b → quản trị hiện `×` (hết chỗ) trong khi LINE (đã sửa ở a) hiện đúng là còn chỗ. Bản sửa (a) đã bỏ loại đơn này ở LINE nhưng **chưa sửa màn quản trị**, nên 2 màn lệch nhau theo chiều ngược lại.

## 2. Cách fix

**(a) LINE / job:**
- D-1 Thêm `course_id` vào danh sách đơn đã đặt dùng để tính chỗ.
- D-2 Thêm hàm lấy tập course và hàm bỏ đơn 指定なし thuộc course khác.
- D-3 `getListBookingByShift` nhận tập course và lọc đơn 指定なし theo course.
- D-4 Áp quy tắc ở màn tuần, màn tháng và lúc bấm đặt trên LINE (+ kiểm lại sau khi tạo đơn, cùng quy tắc).
- Áp dụng tương tự khi friend chọn **指定なし + course** (lọc theo cả nhóm nhân viên làm course đó).
- Job phân bổ nhân viên tự động (`CalendarSalonStaffAssignment`, `CalendarSalonStaffAssignmentAdmin`) dùng cùng quy tắc để gán nhân viên — thứ tự chọn (random/順番) không đổi, chỉ đổi kết quả nhân viên đang xét có nhận được đơn hay không.
- Phạm vi: lịch nhiều nhân viên, dùng course, kiểu `上限をその時間に受付可能なスタッフ数の合計にする` hoặc `上限を設定しない`. Kiểu `上限を設定する` (limit cố định, vd limit=1), lịch không dùng course, lịch 1 nhân viên: **không đổi**.

**(b) Màn quản trị xem ngày:**
- D-21 Màn quản trị xem ngày bỏ đơn 指定なし mà **không nhân viên nào đang có ca làm được course** đó khỏi phép đếm suất (áp cho cả hàng nhân viên và hàng 「指定なし」).
- D-22 Test PHPUnit cho màn quản trị (`CalendarSalonAdminDayNoStaffBookingTest`) + chạy lại toàn bộ Unit suite của (a).
- Đơn 指定なし vẫn **hiển thị như cũ** trên hàng 「指定なし」 — chỉ đổi biểu tượng ○/× tính chỗ của các hàng nhân viên khác.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Controllers/Mobile/CalendarSalonController.php` (`getListTimeBooking`, `showTimeBookingMonth`, `checkCanBooking`) | +38/-12 dòng | Core API tuần/tháng/lúc đặt trên LINE — nơi hiển thị khung trống và validate lúc bấm đặt |
| 2 | `Services/.../CalendarSalonLineBookingService.php` (`checkLimitHasStaff`, `checkLimitNoStaff`, `canPoolServeNoStaffBooking`, `getListBookingByShift`) | +476 dòng | Engine tính chỗ dùng chung cho cả tuần/tháng/lúc đặt + cả 指名あり và 指定なし |
| 3 | `app/Jobs/CalendarSalonStaffAssignment.php` | +12 dòng | Job gán nhân viên khi **friend** đặt đơn 指定なし — phải đồng bộ quy tắc với (1)+(2) |
| 4 | `app/Jobs/CalendarSalonStaffAssignmentAdmin.php` | +12 dòng | Job gán nhân viên khi **admin** tạo đơn 指定なし — tương tự (3) |
| 5 | `Services/CalendarSalon/CalendarSalonStaffService.php` (`checkReasonBookingWithSettingSeason`) | +25/-13 dòng | Màn quản trị xem ngày — phải khớp logic với (1)+(2) sau khi (a) đổi hành vi LINE |
| 6 | `tests/Unit/CalendarSalonNoStaffBookingCourseTest.php` | +616 dòng (mới) | Unit test case a/b/c, repro 2 staff, Risk1/Risk2 cho phần (a) |
| 7 | `tests/Unit/CalendarSalonNoStaffBookingOutsideStaffTest.php` | +604 dòng (mới) | Unit test nhân viên ngoài nhóm nhận đơn 指定なし cho phần (a) |
| 8 | `tests/.../CalendarSalonAdminDayNoStaffBookingTest.php` | +421 dòng (mới) | Unit test màn quản trị xem ngày cho phần (b) |

Dev xác nhận: **không có migration / thay đổi dữ liệu** (đã kiểm diff); không cần recover data — lỗi chỉ ở phần tính/hiển thị chỗ trống, chưa phát hành (phần LINE) hoặc không ghi sai dữ liệu (phần quản trị).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getListTimeBooking` (API màn tuần LINE) | `Mobile/CalendarSalonController.php` | Direct | Khung giờ tuần hiển thị đúng/sai |
| F2 | `showTimeBookingMonth` (API màn tháng LINE) | `Mobile/CalendarSalonController.php` | Direct | Khung giờ tháng hiển thị đúng/sai |
| F3 | `checkCanBooking` (validate lúc bấm đặt + kiểm lại sau tạo đơn) | `Mobile/CalendarSalonController.php` | Direct | Chặn/cho đặt — cả trước và sau khi tạo đơn |
| F4 | `checkLimitHasStaff` (tính chỗ khi chọn nhân viên cụ thể) | `CalendarSalonLineBookingService.php` | Direct | Engine chính của bug gốc |
| F5 | `checkLimitNoStaff` (tính chỗ khi chọn 指定なし + course) | `CalendarSalonLineBookingService.php` | Direct | Nhánh 指定なし + course |
| F6 | `canPoolServeNoStaffBooking` (xét nhóm có ai làm được course) | `CalendarSalonLineBookingService.php` | Direct | Riêng cho case biên nửa đêm |
| F7 | `CalendarSalonStaffAssignment` (job gán NV khi friend đặt) | `app/Jobs/CalendarSalonStaffAssignment.php` | Direct | Job nền — đồng bộ quy tắc mới |
| F8 | `CalendarSalonStaffAssignmentAdmin` (job gán NV khi admin tạo) | `app/Jobs/CalendarSalonStaffAssignmentAdmin.php` | Direct | Job nền — đồng bộ quy tắc mới |
| F9 | `checkReasonBookingWithSettingSeason` (icon ○/× màn quản trị xem ngày) | `CalendarSalonStaffService.php` | Direct | Sửa vòng 2 để khớp với F4–F6 |
| F10 | Filter friend / Google Calendar check của nhân viên **ngoài nhóm** | (đọc qua, không sửa file riêng) | Indirect | Giờ ảnh hưởng tới việc khung của **người khác** có mở hay không (nhân viên ngoài nhóm đủ điều kiện mới được tính là "có người nhận") |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Đơn đặt lịch salon (`reservation`/booking) — cột `course_id`, `staff_id` | READ (thêm điều kiện lọc) | Không ghi/sửa dữ liệu — chỉ đọc thêm `course_id` để lọc đơn 指定なし theo course. Dev xác nhận không có migration. |
| D2 | Ca làm việc (shift) của nhân viên trong nhóm + ngoài nhóm | READ | Dùng để xác định "có ai trong nhóm/ngoài nhóm đang có ca làm được course" |
| D3 | Lịch Google Calendar liên kết nhân viên ngoài nhóm | READ | Nhân viên ngoài nhóm bị Google Calendar chặn giờ đơn 指定なし → không được tính là "có thể nhận" |

> Không có bảng/field bị **CREATE/UPDATE/DELETE/MIGRATE** — toàn bộ thay đổi là logic tính toán (đọc thêm dữ liệu để lọc), theo xác nhận "Migration / thay đổi dữ liệu: không có" của Dev.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | LINE サロン・面談予約 — màn tuần + tháng + lúc bấm đặt | F1, F2, F3, F4, F5, F6, D1, D2, D3 | High |
| T2 | Job phân bổ nhân viên tự động (指定なし自動割り当て) — cả đơn friend đặt và đơn admin tạo | F7, F8, D1, D2 | High |
| T3 | Màn quản trị 「予約カレンダー」 xem ngày — icon ○/× số chỗ | F9, D1, D2 | Medium |
| T4 | Hiệu năng API tuần/tháng của LINE (thêm ~5 query/request) + 2 query cho màn quản trị xem ngày | F1, F2, F9 | Low/Medium (cần đo trên dữ liệu thật — Studio mới chạy ở env `local`) |

**Ngoài phạm vi (Dev xác nhận không đổi — cần TC regression xác nhận giữ nguyên hành vi cũ):**
- Lịch kiểu `上限を設定する` (giới hạn chung toàn lịch cố định, vd limit=1) — kể cả khi có đơn 指定なし course khác. ⚠️ Bug con `#43447` (QA raise) đang test đúng kịch bản này và theo snapshot Studio TC liên quan (`NEW-8`) đang **fail** — cần Leader xác nhận lại với Dev có đúng là "ngoài phạm vi, giữ hành vi release" hay là gap thật trước khi quyết reject/giữ ticket.
- Lịch 個人 (1 nhân viên), lịch không dùng course, đơn 指定なし không gắn course.
- Màn tuần/tháng của **app quản trị di động** — Dev chỉ nêu màn quản trị **web xem ngày** đổi, không đề cập app quản trị mobile.
- Nhân viên bị ẩn khỏi trang đặt (`表示しない`): màn quản trị vẫn cộng suất của họ như cũ (**chưa đồng bộ** với LINE/job — Dev ghi nhận đây là việc cần làm thêm riêng, không nằm trong phạm vi fix lần này).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ Riêng: xác nhận lại với Dev về kết quả **fail** của TC `NEW-8` (map bug con `#43447`, kiểu `上限を設定する`) trước khi reject ticket đó
