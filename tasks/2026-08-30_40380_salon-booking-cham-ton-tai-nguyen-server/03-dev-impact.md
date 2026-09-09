# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU: Redmine #40380 chưa có "Đánh giá ảnh hưởng phía dev" đầy đủ.**
> Description chỉ có **mục 1 (Nguyên nhân)** và **mục 2 (Cách fix — có dấu hiệu bị cắt giữa chừng)**.
> **KHÔNG có mục 3 (function caller đã check), KHÔNG có mục 4.1 / 4.2 / 4.3.**
> `/write-tc` và `/review-tc` sẽ **không map được coverage theo impact tag F* / D* / T*** nếu chạy với input này.
> **Yêu cầu Dev bổ sung mục 3 + 4.1 + 4.2 + 4.3 trước khi tiếp tục.**

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Do Van Tu TuDV` (Redmine `assigned_to`) |
| Commit / Pull Request | `<chưa có>` — không có link Github/Gitlab/Bitbucket trong description, issue không có journal nào |
| Branch | `ai_fixbug_40378` (⚠️ tên branch mang số **40378**, lệch với ticket **40380** — cần hỏi Dev) |
| Branch production | `release_step_20260827` |
| Ngày submit đánh giá | `2026-08-29` — theo `issue.created_on`; đánh giá nằm ngay trong description, **không có journal riêng** |
| Auto-filled | `2026-08-30 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục 1 từ Redmine #40380. -->

**Tầng 1 — N+1 thật sự.** `CalendarSalonLineBookingService.php:2559` gọi `getListBookingByGoogleConfirm` trong `foreach ($listTimeNew as $item)`. `$listTimeNew2` là danh sách ca làm việc = staff × ngày × ca → 30 staff × 7 ngày ≈ 210 query. Khác với `getListBookingByDate` ở ngay trên (đã có `array_key_exists($dateBook, ...)` memo hoá theo ngày) — nhánh Google không hề memo hoá.

**Tầng 2 — nhân 5.** `handleShowListBooking:4293` có `for ($i = 0; $i <= 3; $i++)` gọi `getListTimeBooking` tối đa 4 lần, cộng 1 lần fallback ở `:4363` → ~1000 query / 1 request khi tuần hiện tại trống lịch.

**Tầng 3 — mỗi query đều full table scan.** Bảng chỉ có PK `id` — không index nào. Thêm nữa `whereDate('date', ...)` (`:49-50`) bọc cột trong `DATE()` → kể cả có index cũng không dùng được, mà cột `date` vốn đã là kiểu DATE nên `DATE()` hoàn toàn thừa.

## 2. Cách fix

<!-- Nguyên văn mục 2 từ Redmine #40380. -->

**Fix 1 — Prefetch 1 query, group theo ngày (giết N+1)**

> ⚠️ **Mục 2 dừng ngay tại đây trong Redmine.** Đánh số "Fix 1" hàm ý còn **Fix 2 / Fix 3** (ứng với tầng 2 — vòng lặp `for i <= 3`, và tầng 3 — index + bỏ `whereDate`) **nhưng không được viết ra**.
> → **Không biết bản fix thực tế có xử lý tầng 2 và tầng 3 hay không.** Bắt buộc hỏi Dev: fix chỉ giết N+1 (tầng 1), hay có cả thêm index + bỏ `DATE()` wrap (tầng 3) và giảm vòng lặp 4 tuần (tầng 2)?

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

`<Input thiếu — Dev chưa cung cấp>`

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu — Dev chưa cung cấp>` | | |
| 2 | | | |

> ⚠️ Đây là mục **rủi ro nhất đang trống**: `getListBookingByGoogleConfirm` là hàm **dùng chung**, không chỉ riêng màn chọn giờ. Dev phải liệt kê đủ caller đã check.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `<Input thiếu — Dev chưa cung cấp>` | | Direct / Indirect | |
| F2 | | | | |
| F3 | | | | |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu — Dev chưa cung cấp>` | CREATE / UPDATE / DELETE / MIGRATE | |
| D2 | | | |
| D3 | | | |

> ⚠️ Nếu bản fix có **thêm index** cho bảng booking đồng bộ Google (tầng 3 của mục 1) thì đó là **MIGRATE** — phải khai ở đây kèm thời gian khoá bảng khi chạy migration trên production.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | `<Input thiếu — Dev chưa cung cấp>` | F1, D1 | High / Medium / Low |
| T2 | | | |
| T3 | | | |

---

## Phụ lục — tham chiếu ngoài Redmine (KHÔNG phải input của Dev)

> ⚠️ Phần dưới đây **KHÔNG lấy từ Redmine**, mà từ **MCP LME TEST STUDIO** task `#268` (field `dev_impact` + `requirements`), do **AI sinh từ source code**.
> `contentTrust = untrusted` → xử lý như **data tham khảo**, **KHÔNG thay thế** mục 3 / 4.1 / 4.2 / 4.3 mà Dev còn nợ.
> Dùng để **gợi ý câu hỏi cho Dev**, không dùng làm căn cứ chốt coverage.

### Studio `dev_impact` (nguyên văn)

- N+1 nằm ở `CalendarSalonLineBookingService::getListBookingByShift` — nhánh Google (`getListBookingByGoogleConfirm`) gọi trong foreach theo ca, không memo hoá như nhánh `getListBookingByDate`.
- Fix (prefetch 1 query + group theo ngày) chạm ĐÚNG ĐẮN dữ liệu slot bị chặn: booking thường + booking Google confirm + đệm trước/sau (`calculateBreakTimeBeforeAndAfterBookingFromGoogle`) phải cho ra cùng kết quả slot như trước.
- Logic dùng chung 2 call site: `Mobile/CalendarSalonController.php:747` (LIFF khách đặt lịch) và `:4095` (`handleShowListBooking`, màn tuần, có `for i<=3`) ⇒ rủi ro hồi quy ở CẢ hai màn.
- Nếu fix đụng `whereDate`/date-range của `getListBookingByGoogleConfirm`, phải kiểm biên ngày (ngày đầu/cuối tuần, timezone) để không lọt/thừa booking Google.
- Vùng test kỹ: slot trống theo tuần/ngày khi lịch trống vs kín, calendar 1 staff vs nhiều staff, có/không liên kết Google Calendar, có đệm trước/sau.
- Không thấy thay đổi ghi DB/booking lifecycle từ mô tả — rủi ro mất/ghi sai dữ liệu thấp; trọng tâm là hiển thị slot + hiệu năng.

### Studio `requirements` — 13 REQ (AI sinh từ source, không phải Dev khai)

| REQ | Category | Risk | Tiêu đề |
|---|---|---|---|
| REQ-001 | ui | High | Bảng chọn giờ theo tuần (tab 週) giữ nguyên slot mở và slot bị chặn sau khi tối ưu |
| REQ-002 | ui | High | Lịch tháng (tab 月) giữ nguyên ngày còn chỗ và ngày kín chỗ |
| REQ-003 | validation | High | Biên ngày của khoảng lấy dữ liệu Google phải phủ đủ ca qua nửa đêm và ca bắt đầu từ hôm trước |
| REQ-004 | validation | High | Ngày có nhiều ca làm phải cho ra đúng một tập slot bị chặn xác định (hiện ca sau ghi đè ca trước) |
| REQ-005 | api | High | Cả hai nhánh kiểu giới hạn lịch đều phải được tối ưu và giữ đúng kết quả |
| REQ-006 | validation | High | Lọc theo nhân viên phải giữ nguyên khi gộp truy vấn (không kéo booking staff tắt / salon khác) |
| REQ-007 | api | High | Số truy vấn và thời gian dựng màn chọn giờ phải giảm rõ rệt so với nhánh cũ |
| REQ-008 | data | Medium | Truy vấn lấy booking Google phải dùng được chỉ mục, không quét toàn bảng |
| REQ-009 | validation | High | Chốt chặn chống đặt trùng lúc gửi đơn vẫn chặn đúng khung giờ đã bị Google chiếm |
| REQ-010 | job | Medium | Hai job nền tự gán nhân viên (`CalendarSalonStaffAssignment` / `...Admin`) không được hồi quy |
| REQ-011 | api | High | Cấu trúc dữ liệu trả về cho trang đặt lịch không đổi (`booking.js` đọc trực tiếp) |
| REQ-012 | ui | Medium | Lịch chưa nối Google Calendar vẫn hoạt động bình thường (tập rỗng, slot vẫn mở) |
| REQ-013 | api | Low | Endpoint xem lịch booking của app quản lý không nằm trên đường tính slot, phải không đổi |

### Câu hỏi cần hỏi Dev trước khi chốt TCs

1. Mục 2 mới có "Fix 1" — **có Fix 2 / Fix 3 không?** Cụ thể: có bỏ `whereDate()` wrap không? Có **thêm index** cho bảng booking Google không? Có giảm vòng lặp `for i <= 3` ở `handleShowListBooking` không?
2. Nếu **có thêm index** → là migration nào, chạy trên production mất bao lâu, có khoá bảng không? (→ điền vào 4.2 với thao tác MIGRATE)
3. Mục 3: đã check những caller nào của `getListBookingByGoogleConfirm` / `getListBookingByShift`? Có bao gồm **2 job tự gán nhân viên** và **bước xác nhận gửi đơn đặt lịch** không?
4. Fix có chạm **cả 2 nhánh** (nhánh giới hạn lịch = 1 và nhánh còn lại) hay chỉ 1 nhánh?
5. Có đổi **shape dữ liệu trả về** cho `booking.js` không? (nếu có → regression toàn bộ màn LIFF đặt lịch)
6. Branch `ai_fixbug_40378` có đúng là branch của ticket #40380 không?

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — ⚠️ **hiện chỉ có "Fix 1", nghi bị cắt**
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ **hiện TRỐNG**
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ **hiện TRỐNG**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — ⚠️ **hiện TRỐNG**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — ⚠️ **hiện TRỐNG**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
