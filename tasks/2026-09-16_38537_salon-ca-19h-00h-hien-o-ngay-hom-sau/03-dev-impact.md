# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: **Journal #125237 (AI LME Fix bug — 2026-07-08)** của Redmine #38537. Redmine `description` để trống, không có section "Đánh giá ảnh hưởng" viết tay — báo cáo auto-fixbug là nguồn duy nhất.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | **AI Auto-fixbug LME** (journal #125237). Assignee Redmine = Kim Cúc (QA), không phải Dev người. |
| Commit / Pull Request | `sns-line` — commit `af293dc3e9` (1 file, đã push) · App — commit `2c6c861d` (journal #127213) · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=38537 |
| Branch | `ai_fixbug_38537` (nhánh gốc `release_step_20260623`) · App: `master_branch_release_store` |
| Ngày submit đánh giá | `2026-07-08` |
| Auto-filled | `2026-09-16 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #125237 trên Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Ca làm việc salon kết thúc đúng nửa đêm (vd 19:00–00:00) bị coi là ca qua đêm nên hàm `getAddShiftWhenNextDay` tự sinh thêm một ca cho **NGÀY HÔM SAU** với khung `00:00–00:00`. Khung rỗng này khiến màn đặt lịch trên app hiểu là còn chỗ cả ngày hôm sau (hiển thị **O**). Ca kết thúc đúng nửa đêm thực chất nằm trọn trong ngày hiện tại nên không được tách sang hôm sau.

## 2. Cách fix

Sửa `getAddShiftWhenNextDay` (`CalendarSalonLineBookingService`): chỉ tách phần ca sang ngày hôm sau khi giờ kết thúc **thực sự qua nửa đêm**; nếu giờ kết thúc là `00:00`/`24:00` (đúng nửa đêm) thì bỏ qua việc tạo ca ảo cho hôm sau (phần ngày hiện tại đã được cap tới `23:59` và logic `is_case_next_day` phía controller vẫn phủ đúng tới nửa đêm).

Fix độc lập trên branch `ai_fixbug_38537` vì parent **#26684** là ticket rất cũ, không kiểm chứng được khi offline nên **coi như đã đóng/release**.

**Yokoten**: các hàm SQL sibling (`getListShiftLastSunday` / `getListShiftFirstMonday`) đã guard `00:00`/`24:00` → `23:59`, không có chỗ tạo ca-hôm-sau nào khác cần sửa.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `getAddShiftWhenNextDay` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | **CÓ sửa** — guard `end = 00:00/24:00` thì không tạo ca ảo hôm sau; điều chỉnh `$index++` khi không tạo clone | Root cause |
| 2 | `getDataTimeBooking` / `getListTimeBookingSalon` (caller) — `app/Http/Controllers/Mobile/CalendarSalonController.php:714, 3944, 4546` | Không sửa — chỉ check | Caller trực tiếp của hàm vừa sửa |
| 3 | `is_case_next_day` render — `app/Http/Controllers/Mobile/CalendarSalonController.php:791, 4034` | Không sửa — chỉ check | Logic phía controller vẫn phủ đúng tới nửa đêm |
| 4 | `getListShiftLastSunday` / `getListShiftFirstMonday` (SQL sibling) | Không sửa — đã guard sẵn `00:00/24:00 → 23:59` | Yokoten: rà chỗ tạo ca-hôm-sau khác |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev chỉ kê **file thay đổi** ở mục 4.1 (`app/Services/CalendarSalon/CalendarSalonLineBookingService.php`). Bảng dưới tách theo function, gộp thêm các function Dev đã liệt kê ở **mục 3**.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getAddShiftWhenNextDay` | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | **Direct** | File DUY NHẤT Dev kê ở 4.1 |
| F2 | `getDataTimeBooking` / `getListTimeBookingSalon` | `app/Http/Controllers/Mobile/CalendarSalonController.php:714, 3944, 4546` | Indirect | Dev kê ở mục 3, không sửa — **3 call site** |
| F3 | `is_case_next_day` (render) | `app/Http/Controllers/Mobile/CalendarSalonController.php:791, 4034` | Indirect | Dev kê ở mục 3, không sửa — **2 call site** |
| F4 | `getListShiftLastSunday` / `getListShiftFirstMonday` | SQL sibling (file Dev không ghi rõ) | Indirect | Yokoten — Dev khẳng định đã guard sẵn, **không sửa** |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_time_booking` | **Không có (READ-only)** | Dev ghi nguyên văn: *"Không có (chỉ đổi logic tính khung giờ trống lúc đọc; dữ liệu `calendar_salon_time_booking` đã lưu không thay đổi)"* |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Salon Booking (FA-020)** — hiển thị khung giờ còn trống cho ca kết thúc đúng nửa đêm; không còn báo còn chỗ cả ngày hôm sau | F1, D1 | Dev **không ghi mức risk** (nguyên văn chỉ mô tả, không có High/Medium/Low) |

---

## Bổ sung từ báo cáo AI auto-fixbug (mục 5 · 6 · tự review) — nguyên văn

**■ 5. RECOVER DATA**
```
✔ Không cần recover data
```

**■ 6. VERIFY**
```
Mức: lint
Lệnh: php -l app/Services/CalendarSalon/CalendarSalonLineBookingService.php: No syntax errors;
Truy vết luồng: day1 (is_case_next_day=true, end_time_old=00:00) tại controller line 791-793
  → timeEndShift = ngày+1 00:00 → phủ đúng 19:00 hôm nay tới nửa đêm;
  không còn ca ảo 00:00-00:00 cho hôm sau
Bằng chứng: DB dev: ca qua nửa đêm lưu end_time='00:00'
  (vd calendar_salon_time_booking id14580 20:00-00:00, id14576 19:30-00:00)
  → xác nhận điều kiện start>end kích hoạt nhánh này
```

**■ TỰ REVIEW (AI)**
```
Guard tối thiểu, chỉ chặn tạo ca-hôm-sau khi end=00:00/24:00; giữ nguyên hành vi ca qua đêm thật
(vd 20:00-02:00 vẫn tạo ca hôm sau 00:00-02:00 cho cột ngày hôm sau).
Đánh số index trong vòng lặp được điều chỉnh đúng (bỏ $index++ nội bộ khi không tạo clone).
 • Rủi ro / lưu ý khi test:
   - Nếu tồn tại ca lưu end='24:00' thì điều kiện start>end vốn đã FALSE nên không vào nhánh này;
     guard 24:00 chỉ để phòng ngừa, không đổi hành vi hiện tại
```

**■ BRANCH / COMMIT (để QA checkout)**
```
- sns-line: ai_fixbug_38537 (nhánh gốc release_step_20260623, commit af293dc3e9, 1 file)  [đã push]
```

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm cần Leader làm rõ với Dev (phát hiện lúc auto-fill)

1. **Mục 4.1 chỉ kê 1 file, không kê function/caller** — 5 call site ở `CalendarSalonController` (mục 3) không được đưa vào đánh giá ảnh hưởng.
2. **Mục 4.3 không ghi mức risk** (thiếu High/Medium/Low) và chỉ liệt kê đúng 1 tính năng.
3. **Verify mức `lint`** — chưa có test chạy thật, chỉ đọc code + truy vết luồng.
4. **Parent #26684 bị coi như đã release mà không kiểm chứng** — nếu parent chưa release thì fix có thể chồng/lệch.
5. **2 điểm chạm code khác nhau**: `sns-line@af293dc3e9` (branch `ai_fixbug_38537`) và App `2c6c861d` (`master_branch_release_store`) — Journal #127213 không nói rõ commit app có chứa fix này không.
