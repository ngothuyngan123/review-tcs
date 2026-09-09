# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | commit `bcc9733e24` (repo `sns-line`) — không có link PR trong Redmine |
| Branch | `ai_fixbug_33222` (nhánh gốc `release_step_20260805`, 2 file, đã push) |
| Ngày submit đánh giá | `2026-08-24` (journal #132590) |
| Auto-filled | `2026-09-03 by /new-task` |
| Phiên xử lý AI | https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=6475f8c7-1105-4b54-b2a2-fc454a84aa46 |
| Dashboard fixbug | https://dashboard.melonglobal.net/fixbug-lme/?id=33222 |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ **Fix do AI Auto-fixbug sinh, KHÔNG phải Dev người.** Mục 4.2 (data) Dev ghi "Không có" và mục 4.1 chỉ liệt kê **file** thay đổi chứ không phải function — đã map lại theo mục 3 bên dưới, cần Leader verify.

---

## 1. Nguyên nhân

<!-- Nguyên văn journal #132590 -->

Màn preview đặt lịch salon mở từ admin không có bạn bè LINE thật nên hệ thống truyền mã người dùng rỗng. Bước lấy lịch làm việc vẫn đem mã rỗng đi chấm điều kiện lọc bạn bè, kết quả luôn trượt nên MỌI nhân viên có gắn điều kiện lọc bị loại và ca làm việc của họ biến mất khỏi lịch preview, trong khi bên bạn bè (thỏa điều kiện) vẫn thấy đủ. Ngoài ra bước chọn nhân viên ở preview bỏ qua toàn bộ việc lọc nên còn hiện cả nhân viên không phụ trách khóa đang chọn; chọn nhân viên đó thì màn ngày giờ cũng trống.

**Bằng chứng kỹ thuật (nguyên văn mục 6 VERIFY):**

> `Conversation::advanceFilterPost` dùng `when(!empty($lineUserId))` với mảng `[null]` → `!empty([null])` là true → `whereIn('line_user_id',[null])` không khớp bản ghi nào → `isValidFilter` luôn false ở preview; Bước hiển thị khóa (`getListCourseByCalendar`) và bước hiển thị nhân viên (`getListStaffByCalendar`) đã có sẵn nhánh bỏ qua lọc khi `lineId = 'preview'` → xác nhận ý đồ: preview xem như bạn bè thỏa điều kiện; Chưa chạy được trên DB dev: kết nối `host.docker.internal:3306` bị từ chối nên không dump được data thật để tái hiện.

## 2. Cách fix

<!-- Nguyên văn journal #132590 -->

Thêm cờ preview cho hàm lấy danh sách nhân viên có thể nhận đặt lịch: ở chế độ preview thì bỏ qua bước chấm điều kiện lọc bạn bè (coi như thỏa) nhưng vẫn lọc theo khóa nhân viên phụ trách, và truyền cờ này từ 2 chỗ dựng lịch tuần + lịch tháng của trang đặt lịch salon. Đồng thời sửa bước lấy danh sách nhân viên ở preview: trước đây bỏ qua toàn bộ việc lọc, nay vẫn lọc theo khóa phụ trách như bên bạn bè, chỉ bỏ điều kiện lọc bạn bè. Quét ngang: các chỗ chấm điều kiện lọc còn lại nằm ở luồng đặt lịch thật và job gán nhân viên (người dùng thật) nên giữ nguyên.

**Tự review của AI (nguyên văn):**

> Fix giới hạn trong chế độ preview: thêm tham số `isPreview` mặc định `false` nên 4 nơi gọi khác (đặt lịch thật, 2 job gán nhân viên, hàm nội bộ `getTotalListTimeBookingQ`) giữ nguyên hành vi lọc. Preview vẫn không đặt lịch được nên không nới lỏng ràng buộc nào của luồng đặt thật.
>
> **Rủi ro / lưu ý khi test:**
> - Danh sách nhân viên ở preview nay lọc theo khóa phụ trách: nếu khóa chưa gán nhân viên nào thì preview sẽ trống nhân viên — đúng như bên bạn bè đang thấy
> - Chưa verify được bằng data thật vì DB dev không kết nối được

**Mức verify của AI:** `lint` — `php -l` 2 file: no syntax errors; `git diff --stat origin/release_step_20260805...ai_fixbug_33222`: đúng 2 file đã sửa. **Không có unit test / không chạy thực tế.**

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục 3 journal #132590 — Dev chỉ liệt kê phẳng, không nêu rõ sửa hay chỉ check -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonLineBookingService::getListStaffCanBook` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | **SỬA** — thêm tham số `$isPreview` (mặc định `false`); preview thì bỏ nhánh `isValidFilter` | Hàm lõi lấy danh sách nhân viên nhận đặt lịch — nguồn của bug |
| 2 | `CalendarSalonLineBookingService::isValidFilter` — cùng file | **CHECK** — bị bypass khi `$isPreview=true` | Hàm chấm điều kiện lọc bạn bè, luôn trả false ở preview |
| 3 | `Mobile\CalendarSalonController::getListStaffByCalendar` — `app/Http/Controllers/Mobile/CalendarSalonController.php` | **SỬA** — trước bỏ MỌI lọc ở preview, nay vẫn lọc theo khóa phụ trách, chỉ bỏ lọc bạn bè | Fix Bug 2 (staff không phụ trách khóa vẫn hiện) |
| 4 | `Mobile\CalendarSalonController::getListTimeBooking` — cùng file | **SỬA** — truyền cờ preview vào `getListStaffCanBook` (lịch tuần) | Fix Bug 1 nhánh lịch tuần |
| 5 | `Mobile\CalendarSalonController::showTimeBookingMonth` — cùng file | **SỬA** — truyền cờ preview vào `getListStaffCanBook` (lịch tháng) | Fix Bug 1 nhánh lịch tháng |
| 6 | `Mobile\CalendarSalonController::index` — cùng file | **CHECK** | Entry point trang đặt lịch salon |
| 7 | `Mobile\CalendarSalonController::checkCanBooking` — cùng file | **CHECK** | Luồng đặt lịch thật — giữ nguyên hành vi lọc |
| 8 | `Conversation::advanceFilterPost` — `app/Conversation.php` | **CHECK — KHÔNG sửa** | Nguồn gốc lỗi `!empty([null])`; AI chọn không sửa mà bypass ở tầng trên |

> ⚠️ **Điểm Leader cần chất vấn Dev**: mục 3 không phân biệt "đã sửa" và "chỉ check" — bảng trên là **suy ra từ mục 2**, chưa được Dev confirm. Đặc biệt `Conversation::advanceFilterPost` là root cause thật (`!empty([null]) === true`) nhưng **không được sửa** → mọi caller khác của `advanceFilterPost` truyền mảng `[null]` sẽ vẫn dính lỗi tương tự.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev chỉ ghi 2 FILE ở mục 4.1; function map lại từ mục 3 -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getListStaffCanBook($isPreview)` | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Direct | Đổi signature — thêm param mặc định `false` |
| F2 | `getListStaffByCalendar` (AJAX `/ajax/mobile/calendar-salon/get-list-staff-by-calendar`) | `app/Http/Controllers/Mobile/CalendarSalonController.php` | Direct | Preview nay áp lọc theo khóa |
| F3 | `getListTimeBooking` → lịch tuần | `app/Http/Controllers/Mobile/CalendarSalonController.php` | Direct | Truyền `isPreview=true` |
| F4 | `showTimeBookingMonth` → lịch tháng | `app/Http/Controllers/Mobile/CalendarSalonController.php` | Direct | Truyền `isPreview=true` |
| F5 | `isValidFilter` | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Indirect | Bị bypass ở preview |
| F6 | 4 call site khác của `getListStaffCanBook`: luồng đặt lịch thật, **2 job gán nhân viên**, `getTotalListTimeBookingQ` | (Dev chưa liệt kê tên file/job cụ thể) | Indirect | AI khẳng định "giữ nguyên hành vi" vì default `isPreview=false` — **cần verify bằng regression** |
| F7 | `Conversation::advanceFilterPost` | `app/Conversation.php` | Indirect — **KHÔNG sửa** | Root cause `!empty([null])` vẫn còn; caller khác có thể dính lỗi tương tự |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục 4.2: "Không có" -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** | — | Dev khẳng định không đụng DB/cache/migration. Mục 5 RECOVER DATA: ✔ Không cần recover data |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục 4.3 chỉ có 1 dòng; T2/T3 là suy ra từ 4.1, Leader verify -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Salon Booking (FA-020)** — màn preview trang đặt lịch salon hiện lại ca làm việc và danh sách nhân viên giống bên bạn bè *(nguyên văn Dev)* | F1, F2, F3, F4 | High |
| T2 | Luồng đặt lịch salon **thật của friend** (LIFF) — danh sách nhân viên + slot tuần/tháng | F1, F5 | High — *(suy ra, Dev không liệt kê)* |
| T3 | **2 job gán nhân viên** dùng chung `getListStaffCanBook` | F1, F6 | Medium — *(suy ra, Dev không nêu tên job)* |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm nghi vấn cần hỏi lại Dev (auto-detect bởi `/new-task`)

1. **Mục 4.1 Dev ghi FILE, không ghi FUNCTION** — bảng F1–F7 ở trên do `/new-task` map lại từ mục 3, chưa Dev confirm.
2. **`Conversation::advanceFilterPost` không được sửa** dù là root cause (`!empty([null])` luôn true). Các caller khác của hàm này có dính cùng lỗi không?
3. **"4 call site khác" + "2 job gán nhân viên" không có tên cụ thể** → không viết được TC regression chính xác cho T3.
4. **Fix chỉ verify mức `lint`, chưa chạy trên data thật** (DB dev từ chối kết nối) → toàn bộ nhánh code mới **chưa từng được execute** trước khi giao QA.
5. **Bug 2 (staff không phụ trách course vẫn hiện)** chỉ được xử lý ở `getListStaffByCalendar`. Màn ngày/giờ và bước `getListCourseByCalendar` có bị lệch tương tự không?
