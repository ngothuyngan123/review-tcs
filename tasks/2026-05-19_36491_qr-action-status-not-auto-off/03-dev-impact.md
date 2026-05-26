# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #36491 (journal #118642 — Hạnh Nguyễn 2026-05-19) bằng `/new-task`. Tester verify rồi tick checkbox bên dưới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Hạnh Nguyễn (tác giả journal #118642). Issue assigned_to: Kieu Son Tung — cần Leader confirm ai là dev fix chính. |
| Commit / Pull Request | `<chưa có>` |
| Branch | `36491` (Dev ghi ở mục 5 Section "Đánh giá ảnh hưởng") |
| Ngày submit đánh giá | 2026-05-19 |
| Auto-filled | 2026-05-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Paste nguyên văn từ Redmine journal #118642. -->

Trong function `ajaxUpdateBasicQrs` (`QRCodeController.php:999-1024`), khi user toggle status của QR có bật `use_limit_time` và `limit_start_time` đã qua, code cũ luôn set `time_qr_off_status = 0` mà không phân biệt `limit_end_time` đã hết hay chưa.

Do đó với QR có set 終了時期 (`limit_end_time`) còn hiệu lực, sau khi toggle status thì flag `time_qr_off_status` bị reset về 0 → hệ thống không nhận biết QR đang ở trong giai đoạn time-limited active → status không tự OFF khi hết hạn.

## 2. Cách fix

<!-- Paste nguyên văn từ Redmine. -->

- Sửa logic tại `QRCodeController.php:1015-1023`: khi `use_limit_time = true` và `limit_start_time <= now`, kiểm tra thêm `limit_end_time`:
  - Nếu `limit_end_time <= now` (đã hết hạn) → `time_qr_off_status = 0`.
  - Ngược lại (đang trong khoảng active time-limited) → `time_qr_off_status = 1`.
- Nhờ vậy flag `time_qr_off_status` phản ánh đúng trạng thái thời hạn, job/logic auto-OFF sẽ hoạt động đúng khi đến `limit_end_time`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev đã rà soát toàn codebase điểm đọc/ghi time_qr_off_status. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ajaxUpdateBasicQrs` — `QRCodeController.php:999-1024` (line 1015-1023) | **Đã sửa** — bổ sung check `limit_end_time` trước khi set `time_qr_off_status` | Function fix chính: set flag đúng khi user toggle status QR ở list page |
| 2 | `saveSettingQrOff` — `QRCodeController.php:3500-3558` | **Không đổi** | Logic cũ set `time_qr_off_status = 1` khi user thay đổi setting thời gian — Dev xác nhận không cần đổi |

> Dev confirm: chỉ có 2 nơi đọc/ghi `time_qr_off_status` trong codebase (`ajaxUpdateBasicQrs` + `saveSettingQrOff`).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `QRCodeController@ajaxUpdateBasicQrs` | `app/Http/Controllers/.../QRCodeController.php` (line 999-1024, sửa block 1015-1023) | Direct | Route `PUT /update-basic/{qr}` — toggle status QR ở list page. Function trực tiếp được sửa. |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | _(k có)_ | — | Dev ghi nguyên văn "k có" — không có data nào bị update bởi bản fix (chỉ thay đổi giá trị flag `time_qr_off_status` set vào DB qua flow toggle, nhưng schema/table giữ nguyên) |

> ⚠️ Leader cần verify: field `time_qr_off_status` (cột landing/landing_qrs) **VẪN bị ghi giá trị khác sau fix** (0 vs 1 tùy `limit_end_time`). Dev coi đây là "không có data mới" theo nghĩa schema, nhưng giá trị **runtime** của field này thay đổi behavior — TCs phải verify giá trị field đúng theo các case start/end time.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Toggle ON/OFF QR Landing ở list page khi QR có cấu hình giới hạn thời gian (`use_limit_time`) | F1 | High — flow chính bị sửa logic, cần verify cả case `limit_end_time` chưa qua + đã qua + chưa tới `limit_start_time` |
| T2 | Auto-OFF QR theo `limit_end_time` (job/logic auto-OFF) | F1, D1 | High — đây là behavior bị bug (status không tự OFF khi hết hạn) — sau fix phải hoạt động đúng |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — Dev list 2 nơi đọc/ghi `time_qr_off_status`, có thể hỏi thêm: job auto-OFF nào đọc field này? (T2 cần verify)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — **⚠️ chỉ list F1 (`ajaxUpdateBasicQrs`) nhưng mục 3 nói `saveSettingQrOff` cũng đọc/ghi field này; cần hỏi Dev: function nào auto-OFF QR theo `limit_end_time` (cron/job)? Job này có cần vào 4.1 không?**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — **⚠️ Dev ghi "k có" nhưng thực tế `time_qr_off_status` của bảng landing bị set giá trị khác sau fix; cần xác nhận có data nào khác (cache QR status, log auto-OFF) không**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — verify: case `limit_end_time` < `now`, `limit_end_time` > `now`, không set `limit_end_time` (option `終了日時を設定しない`), edge `limit_end_time = now`
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
