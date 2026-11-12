# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (phân tích root cause ban đầu: Do Van Tu TuDV) |
| Commit / Pull Request | `<chưa rõ>` — chỉ có commit base `e3d1cc9140213f8a63d610444a86e92220f83c79` của nhánh gốc `release_step_20261106` |
| Branch | `ai_studio_fixbug_45752` (gốc `release_step_20261106 @20b5bcae03df`) |
| Ngày submit đánh giá | `2026-11-11` (Journal #153974, 16:16) |
| Auto-filled | `2026-11-12 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

⚠️ Redmine ticket này **không có section "Đánh giá ảnh hưởng" theo format chuẩn** — nội dung được Dev Studio điền rải qua các journal. Nội dung dưới đây tổng hợp nguyên văn từ Journal #153920 + #153974 (xem đầy đủ ở `01-bug-task.md`).

Một số client gửi giá trị trống dưới dạng chữ `"null"` (app LME khi thêm đặt lịch salon, màn sửa rich menu cũ qua FormData). Từ khi web lên **PHP 8.5**, chữ đó không còn bằng `0` khi so sánh với số:
- `"null" != 0` → `true` → bước check ngày nghỉ vẫn chạy.
- `"null" > 0` → `true` (so sánh ký tự `"n" > "0"`) → đi vào nhánh "đã có staff".
- `"null" == 0` → `false` → **đoạn dispatch job tự động assign (`CalendarSalonStaffAssignmentAdmin`) bị bỏ qua**.

→ Kết quả: booking lưu `staff_id = 0`, nằm mãi ở hàng 「指定なし」, không có job assign nào chạy. Cùng pattern này còn gây ra nhánh phụ **D-2** ở màn sửa rich menu cũ (`Basic/UserController`, `/rich-menu/edit/{id}`) — giá trị trạng thái trống bị coi khác `0`, khiến rich menu bị đẩy lên LINE ở chế độ tự mở sai lẽ ra phải giữ tắt.

Đợt nâng PHP 8.5 (`docs/upgrade/runtime-audit.md`) đã rà soát các so sánh lỏng nhưng **bỏ qua giá trị lấy trực tiếp từ request** → lớp lỗi này lọt qua.

## 2. Cách fix

- **D-1** — Coi `staff_id` không phải số là "không chỉ định" (`0`) khi thêm đặt lịch salon từ app (chuẩn hóa giá trị trước khi dùng trong `CalendarSalonController::createBooking`).
- **D-2** — Chuẩn hóa tương tự cho trạng thái rich menu trống ở `UserController` (màn sửa rich menu cũ qua FormData), để không bị coi khác `0`.

File đã sửa (`php-web`):
| File | Thay đổi |
|---|---|
| `app/Http/Controllers/Api/CalendarSalonController.php` | +2 dòng (D-1) |
| `app/Http/Controllers/Basic/UserController.php` | +2 dòng (D-2) |

Mỗi sửa đổi chỉ 2 dòng ở một endpoint, đưa kết quả về như thời PHP 7.4, chỉ khác hành vi khi giá trị gửi lên **không phải số**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | App thêm đặt lịch salon có chọn nhân viên cụ thể + lịch kiểu 1 nhân viên | Không đổi | Cùng hàm đã sửa, kết quả không đổi khi id gửi lên là dạng số |
| 2 | `CalendarSalonStaffAssignmentAdmin` (job queue database) | Không đổi code, nhận thêm việc dispatch từ app sau fix | Cần worker queue chạy để job thực thi |
| 3 | `createRichmenuLine` — dùng chung bởi rich menu v2, copy rich menu, API, tutorial | Không đổi (đọc status từ DB) | Dev Studio khuyến nghị "nên lướt kiểm lưu/copy rich menu v2" dù không đổi code |
| 4 | Lưu rich menu status `1`/`0` ở màn sửa cũ (giá trị radio) | Không đổi | Giá trị radio `"1"`/`"0"` giữ nguyên, không rơi vào nhánh lỗi |
| 5 | Web quản trị + LIFF đặt lịch salon 指名なし, tạo rich menu mới | Không đổi | Không đi qua code đã sửa (gửi rỗng/0 thẳng, không phải chuỗi "null") |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Api\CalendarSalonController::createBooking` — thêm đặt lịch salon từ app LME | `app/Http/Controllers/Api/CalendarSalonController.php` | Direct | Root cause D-1; dòng ~1613 (`$staffId = $request['staff_id'] ?? 0`), nhánh check ngày nghỉ ~1926, dispatch job ~1955 |
| F2 | `Basic\UserController` — lưu rich menu ở màn sửa cũ qua FormData | `app/Http/Controllers/Basic/UserController.php` | Direct | Root cause D-2, cùng pattern PHP8 string-vs-number, phát hiện khi rà PHP8.5 (không phải khách báo ở ticket này) |
| F3 | `CalendarSalonStaffAssignmentAdmin` (job tự động phân bổ nhân viên) | queue database | Indirect | Trước fix: không được dispatch cho booking từ app; sau fix: nhận thêm việc, cần worker chạy |
| F4 | `createRichmenuLine` (đồng bộ rich menu lên LINE) | dùng chung rich menu v2 / copy / API / tutorial | Indirect — rủi ro thấp | Đọc status từ DB nên không đổi, Dev Studio khuyến nghị lướt kiểm thêm |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_line_booking.staff_id` | UPDATE (code fix) + **Recover data** thủ công | Booking tạo từ app với 指名なし trên lịch bật phân bổ tự động, từ khi lên PHP 8.5 đến khi fix deploy, bị kẹt `staff_id = 0`. Đã biết ID `2600339`, `2602171` (calendar `23996`); danh sách đầy đủ lập bằng SQL trong `docs/investigation/v1.md` (nội bộ Dev). **Recover theo quyết định của Tu (11/11/2026): gán tay trên màn quản trị salon, không script.** |
| D2 | Rich menu trên LINE — trạng thái tự mở (status lưu DB vẫn `0`/`1`, nhưng hành vi đẩy lên LINE bị sai khi status trống) | Không đổi dữ liệu DB, chỉ **Recover hiển thị** | Rich menu cũ (status trống) lưu trong khoảng PHP 8.5 có thể đang tự mở sai trên LINE. **Không viết script recover** — hướng dẫn mở màn sửa cũ (`/rich-menu/edit/{id}`) và lưu lại (không cần đổi gì) sau khi deploy để đồng bộ lại đúng trên LINE. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | App LME — đặt lịch salon, để nhân viên 「選択してください」(指名なし) trên lịch bật phân bổ tự động | F1, F3, D1 | High — đúng bug chính của ticket, job assign phải chạy + tin/Sheet/remind/Google event gửi đúng 1 lần sau khi gán |
| T2 | App LME — đặt lịch salon có chọn nhân viên cụ thể / lịch kiểu 1 nhân viên | F1 | Low (regression) — hàm chung đã sửa, Dev khẳng định không đổi khi id là số, cần test lại để xác nhận ngày nghỉ + phí nhân viên vẫn đúng |
| T3 | Web quản trị / LIFF — đặt lịch salon 指名なし (không qua code đã sửa) | — | Low (regression đối chứng) — dùng để so sánh hành vi, xác nhận không bị ảnh hưởng bởi fix |
| T4 | Rich menu — màn sửa cũ (`/rich-menu/edit/{id}`), lưu menu có trạng thái trống | F2, D2 | High — bug phụ D-2, rich menu trên LINE phải không tự mở khi trạng thái trống/tắt |
| T5 | Rich menu — tạo mới (v2 wizard), copy rich menu, lưu menu đã chọn rõ bật/tắt tự mở | F4 | Low (regression) — Dev Studio khẳng định không đổi vì đọc status từ DB, nhưng khuyến nghị lướt kiểm |
| T6 | Job `CalendarSalonStaffAssignmentAdmin` chạy trên production thật | F3, D1 | Medium — RULE-08 (job nền), cần verify trên prd/staging thật, không kết luận từ local |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- ⚠️ Input thiếu: Redmine #45752 không có section "Đánh giá ảnh hưởng" theo format chuẩn (1./2./3./4.1/4.2/4.3) — nội dung trên được AI tổng hợp từ nhiều journal rải rác (#153882, #153920, #153974). Leader/Dev nên xác nhận lại trước khi dùng làm oracle coverage. -->
