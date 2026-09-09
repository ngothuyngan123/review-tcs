# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Do Van Tu TuDV` (assigned_to) |
| Commit / Pull Request | https://bitbucket.org/snstool/sns-line/pull-requests/10467/diff |
| Branch | `bugs/fix_bug_friend_info_20260629` |
| Ngày submit đánh giá | `2026-06-29` |
| Auto-filled | `2026-07-02 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Redmine journal. -->

Chưa xử lý lưu được preview action friend info.

## 2. Cách fix

<!-- Nguyên văn từ Redmine journal. -->

- Lưu preview action lịch sử friend info.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev chỉ ghi "Đã check function/data" trong Redmine, KHÔNG liệt kê chi tiết caller. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu — Dev chỉ ghi "Đã check function/data", không liệt kê>` | | |

⚠️ Mục 3 Dev chưa liệt kê cụ thể caller/data dependency. Leader nên hỏi lại Dev nếu nghi ngờ sót caller (đặc biệt các nơi khác cũng tạo lịch sử friend info).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `handleOrderCallback` | `app/Services/EventBooking/EventBookingService.php` | Direct | Callback booking event (univapay) |
| F2 | `saveAdminBooking` | `app/Http/Controllers/Basic/BookingEventDayController.php` | Direct | Admin booking |

### 4.2. List data bị update khi fix bug

<!-- Dev ghi: "k có". -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Dev ghi: không có data bị update khi fix bug>` | — | |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Admin booking | F2 | `<chưa rõ — Dev không ghi mức>` |
| T2 | Booking event có callback univapay | F1 | `<chưa rõ — Dev không ghi mức>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
