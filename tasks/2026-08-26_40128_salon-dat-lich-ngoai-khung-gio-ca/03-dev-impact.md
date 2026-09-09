# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #40128 journal **#132918** (user `AI LME Fix bug`, 2026-08-25T08:59:44Z) — báo cáo **★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST**. Toàn bộ nội dung dưới đây là **nguyên văn** từ báo cáo đó, chỉ sắp lại theo khung template.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` — hệ thống Auto-fixbug LME (báo cáo tạo tự động). QA nhận: `Ngô Thúy Ngần` |
| Commit / Pull Request | `sns-line` commit `3d50f0a332` (4 file). ⚠️ Không có link GitHub/GitLab trong Redmine. Phiên AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=90009d73-774f-4f21-a5fa-a6414a97c350 · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=40128 |
| Branch | `ai_fixbug_40128` (nhánh gốc `release_step_20260805`) — đã push lên origin |
| Ngày submit đánh giá | `2026-08-25` |
| Auto-filled | `2026-08-26 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục ■ 1. NGUYÊN NHÂN -->

Khi xét "nhân viên nào phụ trách được trọn khung đặt" (chế độ trần = tổng nhân viên tiếp nhận được + một đơn do một nhân viên phụ trách, khách không chỉ định nhân viên), hệ thống lấy mốc kết thúc của khoảng đặt rồi TRỪ ĐI nguyên số phút nghỉ sau đã cấu hình. Nhưng khi thời gian nghỉ sau không đủ chỗ trong ca, hàm dựng khoảng đặt đã kéo mốc kết thúc về cuối ca (tức phần nghỉ thực tế không được cộng vào), nên phép trừ đó nới lỏng mốc cuối ca thêm đúng bằng thời gian nghỉ. Hệ quả: nhân viên hết ca giữa chừng vẫn bị coi là phụ trách được cả khung.

Ca ngày 9/4: A 12:00-20:30, B 14:30-21:00, khoá 120 phút, nghỉ sau 60 phút, B đã có đơn 17:30-21:00 → khung 19:00 (19:00-21:00) chỉ còn A đảm nhận được, mà A hết ca 20:30; do mốc yêu cầu bị nới từ 21:00 xuống 20:00 nên A vẫn được tính là rảnh → trần chỗ = 2 > 1 đơn đã có → khung 19:00 vẫn BẬT thay vì TẮT.

## 2. Cách fix

<!-- Nguyên văn mục ■ 2. CÁCH FIX -->

Thêm THAM SỐ RIÊNG bắt buộc `breakTimeAfterApplied` (số phút nghỉ sau THỰC SỰ nằm trong khoảng bị chiếm) đi xuyên chuỗi kiểm tra trần chỗ, thay vì đổi ý nghĩa tham số nghỉ-sau cũ. `getStartAndEndBooking` tính và trả về giá trị này (0 khi phần nghỉ bị cắt vì đụng cuối ca, đúng cấu hình khi cộng đủ, đúng phần lọt khi cộng dở); `isReachMaxBooking` / `checkSlotBookingIsValid` / `checkSlotBookingIsValidType0` / `checkLimitShiftsNotCombined` nhận và truyền tiếp; `getListStaffValidInRange` đổi hẳn tên tham số thành `breakTimeAfterApplied` và dùng trực tiếp (không fallback).

Nhánh chế độ trần N cố định (`getListStaffValidInRangeOpt3`) và chế độ gộp ca vẫn dùng số phút nghỉ ĐÃ CẤU HÌNH nên bất biến. Nhờ đó mốc nhân viên phải còn ca tới lúc kết thúc phục vụ không bị nới lỏng, còn phần nghỉ sau vẫn được phép tràn qua cuối ca. **Áp cho cả 5 điểm gọi**: danh sách khung theo tuần/tháng trên LIFF, kiểm tra lại lúc bấm đặt, 2 job tự gán nhân viên.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonLineBookingService::getStartAndEndBooking` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Tính & trả về `breakTimeAfterApplied` | Nguồn sự thật của "số phút nghỉ sau THỰC SỰ nằm trong khoảng bị chiếm" |
| 2 | `CalendarSalonLineBookingService::getListStaffValidInRange` | Đổi tên tham số thành `breakTimeAfterApplied`, dùng trực tiếp (không fallback) | **Nơi phát sinh lỗi**: trừ nghỉ sau khỏi mốc cuối ca |
| 3 | `CalendarSalonLineBookingService::checkLimitShiftsNotCombined` / `checkSlotBookingIsValid` / `checkSlotBookingIsValidType0` / `getSumSlot` / `checkStaffFalse` | Nhận & truyền tiếp tham số mới | Chuỗi kiểm tra trần chỗ |
| 4 | `CalendarSalonLineBookingService::isReachMaxBooking` | Nhận & truyền tiếp | Đường truyền tham số nghỉ sau |
| 5 | `Mobile\CalendarSalonController::getListTimeBooking` + `handleShowListBooking` + `checkCanBooking` — `app/Http/Controllers/Mobile/CalendarSalonController.php` | Truyền tham số mới | Caller: danh sách khung LIFF + kiểm tra lại lúc bấm đặt |
| 6 | `Jobs\CalendarSalonStaffAssignment` + `Jobs\CalendarSalonStaffAssignmentAdmin` | Mỗi nơi +1 dòng truyền `breakTimeAfterApplied` | Caller: 2 job tự gán nhân viên |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Redmine mục **4.1 ghi là "File thay đổi"** (4 file), không phải list function. Bảng dưới lấy 4 file đó + function-level từ mục 3 ở trên. Không suy diễn thêm.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getStartAndEndBooking`, `getListStaffValidInRange`, `checkLimitShiftsNotCombined`, `checkSlotBookingIsValid`, `checkSlotBookingIsValidType0`, `getSumSlot`, `checkStaffFalse`, `isReachMaxBooking` | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Direct | Core logic tính khung trống; `getListStaffValidInRange` là nơi phát sinh lỗi |
| F2 | `getListTimeBooking`, `handleShowListBooking`, `checkCanBooking` | `app/Http/Controllers/Mobile/CalendarSalonController.php` | Direct | Danh sách khung LIFF (tuần/tháng) + validate lúc bấm đặt |
| F3 | `CalendarSalonStaffAssignment` (job tự gán nhân viên) | `app/Jobs/CalendarSalonStaffAssignment.php` | Direct | +1 dòng truyền tham số mới |
| F4 | `CalendarSalonStaffAssignmentAdmin` (job tự gán nhân viên — admin) | `app/Jobs/CalendarSalonStaffAssignmentAdmin.php` | Direct | +1 dòng truyền tham số mới |
| F5 | `getListStaffValidInRangeOpt3` (chế độ trần N cố định) | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | **Không đổi (Dev khẳng định bất biến)** | Vẫn nhận nghỉ-sau ĐÃ CẤU HÌNH |
| F6 | `checkLimitShiftsCombined` (chế độ gộp ca) | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | **Không đổi (Dev khẳng định bất biến)** | Vốn không nhận tham số này |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục ■ 4.2 -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** | — | Nguyên văn Dev: `Không có — chỉ đổi cách tính khung giờ trống, không đọc/ghi thêm cột nào`. Mục ■ 5. RECOVER DATA: `✔ Không cần recover data` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục ■ 4.3 -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Salon Booking (FA-020)** — khung giờ trống trên LIFF, kiểm tra lúc bấm đặt và tự gán nhân viên: nhân viên hết ca giữa chừng không còn bị tính là phụ trách được cả khung; khung nào không ai đủ ca sẽ tắt | F1, F2, F3, F4 | `<Dev không ghi mức risk>` — đây là tính năng bị fix trực tiếp |
| T2 | **Booking Management (FA-020 / 予約管理)** — số khung nhận đặt cuối ca giảm đúng theo ca thật khi lịch có cài thời gian nghỉ sau | F1, F2 | `<Dev không ghi mức risk>` |

---

## 5. Recover data (mục ■ 5 của báo cáo)

`✔ Không cần recover data`

## 6. Verify của Dev (mục ■ 6 của báo cáo)

- **Mức**: unit-test
- **Lệnh / cách verify**:
  - `php -l` 4 file đã sửa: No syntax errors detected
  - Mô phỏng bằng chính hàm thật của service (không cần DB), truyền đúng hình dạng mới (tham số 5 = nghỉ cấu hình, tham số 7 = nghỉ thực tế)
  - Case ticket (A 12:00-20:30, B 14:30-21:00, khoá 120 phút, nghỉ 60 phút, B có đơn 17:30-21:00, không chỉ định nhân viên) → khung 19:00 **OFF** (trước fix ON)
  - Regression: 19:00 khi B RẢNH → ON (kết thúc 21:00 trùng cuối ca B, nghỉ không cần lọt trong ca); 18:30 kết thúc đúng 20:30 = hết ca A → ON; 18:30 dưới ca B (nghỉ áp dụng 30 phút) → ON; 15:00 khoá 60 phút nghỉ cộng đủ 60 phút → ON; 19:30 khoá 60 phút dưới ca A → ON
  - Bảng đối chiếu cũ/mới trên `getListStaffValidInRange`: chỉ khác khi nghỉ thực tế < nghỉ cấu hình (khung sát cuối ca) và chỉ theo hướng LOẠI nhân viên không đủ ca; lịch không cài nghỉ sau hoặc nghỉ cộng đủ → giống hệt
  - `getListStaffValidInRangeOpt3` (chế độ trần N): vẫn nhận nghỉ ĐÃ CẤU HÌNH → bất biến về mặt code, ngoài ra đã đo cho kết quả giống hệt ở mọi kịch bản thử
  - Rà bằng grep: 5/5 điểm gọi `isReachMaxBooking` đều truyền tham số mới và đều có `$timeSlotBooking` trong cùng hàm; `getStartAndEndBooking` không có nơi gọi nào khác
- **Bằng chứng**:
  - Cấu hình do human xác nhận: một đơn một nhân viên (không gộp ca), mỗi nhân viên trần 1 lượt, nghỉ sau 1h
  - **Quy tắc human chốt**: kết thúc course trùng giờ hết ca thì KHÔNG cộng thời gian nghỉ sau → `breakTimeAfterApplied = 0` đúng theo quy tắc này
  - Script mô phỏng `/tmp/sim40128.php`, `/tmp/sim2.php`, `/tmp/sim3.php`, `/tmp/sim4.php` (bảng đối chiếu cũ/mới)

## 7. Tự review của AI + rủi ro khi test (nguyên văn)

Bản 2 theo góp ý human: dùng THAM SỐ MỚI thay vì đổi ý nghĩa tham số cũ, nên các chế độ trần khác không bị chạm. Tham số mặc định `null` → mọi nơi gọi cũ (nếu có) giữ nguyên hành vi. Chỉ **chế độ trần 0 (không giới hạn)** và **trần 2 (tổng nhân viên)** đi qua `getListStaffValidInRange` mới nhận giá trị mới; chế độ trần N cố định và chế độ GỘP CA (`checkLimitShiftsCombined` vốn không nhận tham số này) bất biến.

**Rủi ro / lưu ý khi test (Dev tự nêu):**
- Lịch **CÓ cài nghỉ sau**, ở chế độ **trần 0 / trần 2**: vài khung sát cuối ca sẽ **tắt đi** — đúng ý đồ nhưng là thay đổi hiển thị, nên báo trước cho vận hành
- Khoảng chặn của **đơn đã tồn tại** vẫn dùng nghỉ sau đã cấu hình (không đổi)
- ⚠️ **Chưa chạy trên môi trường thật** (DB dev không kết nối được từ container) — mới verify bằng mô phỏng gọi trực tiếp hàm thật

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

**Điểm cần Leader chú ý khi review TC:**
1. Dev tự khai **chưa chạy trên môi trường thật** → toàn bộ kết luận "bất biến" của chế độ trần N / gộp ca mới chỉ dựa trên đọc code + mô phỏng.
2. Fix chạm **5 điểm gọi** (LIFF list tuần/tháng, validate lúc bấm đặt, 2 job auto-assign) → coverage TC phải phủ đủ 5, không chỉ màn LIFF.
3. Đường **gán nhân viên thủ công** (`saveStaffAssignment`) KHÔNG nằm trong 4 file sửa → phải giữ nguyên hành vi cũ (cho phép vượt ca). Đây là đối chứng âm bắt buộc, vì chính giả thuyết ban đầu của support xoay quanh đường này.
