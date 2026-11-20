# 03 — Đánh giá ảnh hưởng từ Dev

> **Lượt B — T15 phần Salon (#41717 · #41529 · #41718).**
> ⚠️ **INPUT THIẾU: Dev KHÔNG viết đánh giá ảnh hưởng cho 3 ticket này.** 3 ticket `New`, không assignee, không journal Dev; handoff T15 ở ticket cha #45229 chỉ nêu #45186 + #42266. Nội dung dưới đây **ghép nguyên ý** từ 3 nguồn có sẵn, không thêm suy luận:
> (1) Studio task #560 — `requirements` `REQ-X-41717` · `REQ-X-41529` · `REQ-X-41718` (+ `-01`/`-02`) do Dev Studio viết;
> (2) 2 bug Studio phát sinh khi test lượt này: #45409, #45410 (đã `Closed`, có kết quả re-test);
> (3) Studio `spec_delta.diffStat` — file salon / friendlist / queue bị sửa trong nhánh sprint (phần lớn thuộc nhóm T7 / T9 / T10 / T16).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` — 3 ticket không có assignee |
| Commit / Pull Request | **Không có commit riêng** cho #41717 / #41529 / #41718. Liên quan: T16 #41345 commit `229f1a4788` (viết lại truy vấn khung giờ tuần); fix bug Studio #45409 / #45410 có trong `web@67500733` (re-test lượt #7415) |
| Branch | `ai_studio_implement_45229` (sns-line) |
| Ngày submit đánh giá | `<chưa có>` |
| Auto-filled | 2026-11-16 by `/review-tc` lượt B (ghép từ Studio, không phải `/new-task`) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — đối chiếu với Studio `REQ-X-41717/41529/41718` + Redmine #45409 / #45410.

---

## 1. Nguyên nhân

Ticket AI chỉ **nghi ngờ**, Dev chưa xác nhận:
- #41717 / #41529: `getListTimeLineBooking` (`CalendarSalonLineBookingService.php`) nạp toàn bộ `calendar_salon_time_booking` rồi gom trong bộ nhớ → hết thời gian (500 s) / hết bộ nhớ (1 GB) khi dữ liệu lớn.
- #41718: `Packets out of order` khi đọc `calendar_salon_line_booking` — Studio ghi: *"lỗi giao thức MySQL thường do kết nối bị đóng/tái dùng trong tiến trình dài"* (giả thuyết, chưa xác nhận).

## 2. Cách fix

- **#41717 / #41529**: không có commit riêng. Thay đổi chạm cùng luồng:
  - T16 #41345 — `GET /ajax/mobile/calendar-salon/get-list-time-booking`: *"Đọc booking cả tuần một câu, tính mốc giờ ca một lần; khung trống/đã kín phải giống trước"* (`REQ-X-41345`).
  - Fix bug Studio #45409 — khoảng ngày > 31 ngày ⇒ **422 「表示期間は31日以内で指定してください。」** (re-test: khoảng 365 ngày trả 422 sau 0,0 s).
  - Fix bug Studio #45410 — calendarId không tồn tại ⇒ 404 「カレンダーが見つかりません。」; thiếu calendarId / ngày sai ⇒ 422 「パラメータが不正です。」; không ghi `calendar_salon_setting_time_free`.
- **#41718**: không có commit; Studio chỉ dựng TC kiểm giả thuyết kết nối DB bị đóng (`wait_timeout`) ở worker.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `order()` → `getListTimeLineBooking` (kiểm khung còn trống khi 「予約確定」) | Không ghi | `REQ-X-41717-01` |
| 2 | `initDataBooking` ⇒ `showTimeBookingMonth` ⇒ `getListTimeLineBooking` (lịch tháng) | Không ghi; diff có test mới `CalendarSalonInitDataBookingGuardTest` (+131) — Dev chưa mô tả | ghi chú NEW-702 |
| 3 | API khung giờ `get-list-time-booking` (tuần / danh sách `timeShowWeek=1`) | Guard khoảng ngày ≤ 31 + validate calendarId / ngày (`CalendarSalonListTimeBookingGuardTest` +158) | #45409, #45410 |
| 4 | `FriendlistController` `deleteUserBlock` / `deleteUserBlockAction` | Không ghi cho #41718; file +204 dòng do nhóm khác; `public/js/friendlist/block.js`, `user_block.js` (+11 mỗi file) và 2 view `block.blade.php`, `user_block.blade.php` cũng đổi | `REQ-X-41718-01` |
| 5 | Lệnh `recover:payment_univapay_timeout` (everyFiveMinutes, `Console/Kernel.php`) | Không đổi code lệnh | `REQ-X-41718-02` |
| 6 | Queue worker (`config/queue.php` +3) | Đổi cấu hình queue (nhóm T21 #45230) | `REQ-X-41718-02` |
| 7 | API app quản trị salon (`Mobile/CalendarSalonController.php` +304) | Do nhóm khác — **chưa rõ** có gọi `getListTimeLineBooking` / API khung giờ không | — |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | API khung giờ trang khách: guard khoảng ngày ≤ 31 (422) + validate calendarId / ngày (404 / 422) | `Api/CalendarSalonController.php`, `CalendarSalonLineBookingService.php` | Direct | #45409 · #45410 · `REQ-X-41529-01/02` · `REQ-X-41717-02` |
| F2 | Đặt lịch `order()` dùng `getListTimeLineBooking` | `CalendarSalonLineBookingService.php` | Indirect | `REQ-X-41717-01` |
| F3 | Lịch tháng `initDataBooking` ⇒ `showTimeBookingMonth` | `CalendarSalonLineBookingService.php` | Indirect | ghi chú NEW-702 |
| F4 | Truy vấn khung giờ tuần viết lại | `CalendarSalonLineBookingService.php` | Indirect | **T16 #41345** — review ở nhóm T16, loại khỏi mẫu số lượt này |
| F5 | Xoá bạn bè đã chặn (từng người / hàng loạt) | `Basic/FriendlistController.php` | Indirect | `REQ-X-41718-01` |
| F6 | Lệnh `recover:payment_univapay_timeout` | `CalendarSalonLineBookingService.php:7171-7180` | Indirect | `REQ-X-41718-02` |
| F7 | Queue worker chạy lâu nối lại DB | `config/queue.php` | Indirect | `REQ-X-41718-02` |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_line_booking` | READ / DELETE (khi xoá bạn bè) | #41718 |
| D2 | `calendar_salon_time_booking` | READ (khối lượng lớn) | #41717 · #41529 |
| D3 | `calendar_salon_setting_time_free` | CREATE (không được tạo khi calendarId sai) | #45410 |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Trang đặt lịch salon phía khách — tuần / tháng / danh sách | F1, F3, D2 | High (rule mới 31 ngày) |
| T2 | Đặt lịch 「予約確定」 | F2, D2 | Medium |
| T3 | 友だちリスト — xoá bạn bè ở ブロックした友だち / ブロックされた友だち | F5, D1 | Low |
| T4 | Thanh toán UnivaPay của đơn salon — khôi phục đơn quá hạn | F6, D1 | Low |
| T5 | Job / worker nền salon | F7 | Low |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng — **chưa: Dev chưa xác nhận nguyên nhân cả 3 ticket**
- [ ] Mục 2 (cách fix) có thể trace về code — **chưa: không có commit riêng**
- [ ] Mục 3 đã check đủ caller — **chưa rõ API app (`Mobile/CalendarSalonController`) có dùng API khung giờ không; chưa rõ guard ở `initDataBooking` chặn gì**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data
- [ ] Mục 4.3 cover được cả happy path lẫn edge case
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
