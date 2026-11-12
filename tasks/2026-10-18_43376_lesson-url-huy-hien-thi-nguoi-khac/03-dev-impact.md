# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #43376 bằng `/new-task`. Nguồn: **Journal #144995 — Dev Studio — 2026-10-18** ("Nguyên nhân & hướng sửa").
> ⚠️ Journal **không theo format 4 mục** (thiếu mục 3 caller, thiếu commit/branch). Mục 4.x dưới đây map từ "Hướng sửa D-1…D-5" + "Ảnh hưởng / rủi ro" của Dev — tester verify lại.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-10-18` |
| Auto-filled | `2026-10-18 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn journal #144995:

API xem chi tiết lịch (getDetailBookingCalendar) và API huỷ lịch của Lesson chỉ tìm booking theo booking_id, không lọc theo LINE user đang mở trang. Vì vậy ai có URL huỷ của người khác cũng xem được họ tên, kana, email và huỷ được lịch. Trong vụ này, RIKO nhận URL huỷ của 登川 qua một tin shop gửi lẻ (copy từ tin xác nhận của 登川); hệ thống gửi tin tự động không sai. Salon có cùng lỗ hổng.

## 2. Cách fix

> Nguyên văn journal #144995:

- D-1 API chi tiết lịch Lesson chỉ trả lịch thuộc đúng LINE user đang mở
- D-2 JS trang Lesson gửi LINE user khi lấy chi tiết lịch
- D-3 API huỷ lịch Lesson kiểm tra chủ lịch trước khi huỷ
- D-4 API chi tiết lịch Salon kiểm tra chủ lịch như Lesson
- D-5 API huỷ lịch Salon kiểm tra chủ lịch như Lesson

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Dev xác nhận thêm (2026-10-18):
> - **LIFF xác định chủ lịch qua phiên LIFF** (line_user_id lấy từ LIFF app của người đang mở), không còn chỉ tra theo `booking_id`.
> - **Người không phải chủ booking** nhận thông báo `予約が存在しません。` (không lộ dữ liệu, không huỷ được).
> - Phạm vi apply: **Lesson + Salon**. **Chưa** đụng Event booking (FA-021).
>
> ⚠️ Vẫn còn thiếu: danh sách caller đầy đủ (màn lịch sử, nút 同じ内容で予約, xin huỷ / rút yêu cầu huỷ, huỷ đăng ký chờ キャンセル待ち, app mobile có dùng chung 2 API không) — member xác nhận khi test.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `getDetailBookingCalendar` (Lesson) | Lọc theo LINE user đang mở | D-1 |
| 2 | API huỷ lịch Lesson | Kiểm chủ lịch trước khi huỷ | D-3 |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | API chi tiết lịch Lesson (`getDetailBookingCalendar`) — chỉ trả booking của LINE user đang mở | `<chưa rõ>` | Direct | D-1 |
| F2 | JS trang LIFF Lesson — gửi LINE user khi lấy chi tiết lịch | `<chưa rõ>` | Direct | D-2 · rủi ro cache JS cũ |
| F3 | API huỷ lịch Lesson — kiểm chủ lịch trước khi huỷ | `<chưa rõ>` | Direct | D-3 |
| F4 | API chi tiết lịch Salon — kiểm chủ lịch | `<chưa rõ>` | Direct | D-4 |
| F5 | API huỷ lịch Salon — kiểm chủ lịch (+ JS trang Salon; Dev nói "2 file JS") | `<chưa rõ>` | Direct | D-5 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | Dev: "Không đổi DB, route, text giao diện hay mã HTTP" |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lesson (FA-019) — LIFF khách: xem chi tiết / huỷ booking từ キャンセル用URL và màn lịch sử | F1, F2, F3 | High |
| T2 | Salon (FA-020) — LIFF khách: xem chi tiết / huỷ booking | F4, F5 | High |
| T3 | Release — WebView giữ JS cũ → chính chủ bị báo không tìm thấy (cần bump version JS) | F2, F5 | Medium |

---

## Rủi ro / lưu ý khi test (Dev tự nêu — nguyên văn)

Chỉ đổi 4 API công khai xem/huỷ lịch của Lesson và Salon cùng 2 file JS. Không đổi DB, route, text giao diện hay mã HTTP. URL huỷ bị chuyển cho người khác sẽ không còn lộ thông tin hay huỷ được. Rủi ro: nếu WebView còn giữ JS cũ thì chính chủ lịch cũng bị báo không tìm thấy, nên bản release phải bump version JS.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
