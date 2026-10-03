# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Nguồn**: description Redmine #39009 **KHÔNG có** section "Đánh giá ảnh hưởng phía dev". Nội dung bên dưới lấy từ **journal #137775** (Do Van Tu TuDV — 2026-09-23) — *"AI ĐÁNH GIÁ ẢNH HƯỞNG ĐỘC LẬP"* (reviewer AI độc lập soi diff thật, **không phải Dev implement tự kê**). Cấu trúc journal ■1…■10 được map vào 4 mục template; text giữ nguyên văn, chỉ gắn tag F/D/T.
>
> ⚠️ **Lệch requirement Studio**: Studio task #325 REQ-005/REQ-009 mô tả 2 cột mới (`message_send_admin_cancel`, `setting_action_admin_cancel`, có migration). Journal này ghi diff thật **không migration, dùng chung cột** `message_send_end` / `setting_action_id` với mode 1. Leader chốt spec trước khi review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Tuấn Anh Trần (assignee Redmine) · đánh giá ảnh hưởng: Do Van Tu TuDV (phiên AI độc lập) |
| Commit / Pull Request | `<chưa có link PR>` — commit `db932849bf` (base `7bfe68fcd8`), repo `sns-line` |
| Branch | `ai-feature-39009` |
| Ngày submit đánh giá | 2026-09-23 (đánh giá lần đầu 2026-09-12, soạn lại 2026-09-23 — HEAD không đổi) |
| Auto-filled | 2026-09-24 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Ticket SpecImprove — không có root cause bug. Nguyên văn ■1 "YÊU CẦU CỦA TICKET":

Option 予約後のキャンセル不可 (approve_type = 3) của màn 予約キャンセル時の各種設定 trước đây không cho cấu hình gì: admin hủy thủ công thì hệ thống im lặng. Yêu cầu: cho phép cấu hình nội dung tin + エルメアクション (text và multi-action) cho chế độ này, áp dụng cho cả Lesson và Salon (CR-01…CR-05, BR-C1…C4).

## 2. Cách fix

> Nguyên văn ■2 "ĐÃ LÀM GÌ (đọc từ diff THẬT)":

- FE: mở khối 「メッセージ・アクション」 cho approve_type = 3 ở cả 2 hệ, heading riêng 手動キャンセル時に送信するメッセージ・アクション, ẩn 例文を挿入する / 利用しない / 必ず1通目に送信する, textarea + counter /5,000 + panel エルメアクション dùng chung cột message_send_end và setting_action_id với chế độ 全承認制.
- BE: thêm nhánh approve_type == 3 vào case 'adminCancel' của 2 service gửi tin → nạp setting_action_id + message_send_end.
- Thêm validate độ dài 5.000 ký tự phía server (trả 422) cho moment = 'cancel', kèm key config mới max_length_setting_message; bump config('sns-line.version') để cache-bust asset.
- C-05 giữ nguyên theo quyết định D-04.

Diff thật = 1 commit db932849bf trên branch ai-feature-39009, base 7bfe68fcd8 → 12 file, +159/-27. Không migration, không đổi schema, không thêm/sửa route, không có file lạ ngoài phạm vi.

> ⚠️ Lưu ý khác Studio: journal ghi FE **ẩn** 例文を挿入する / 利用しない ở mode 3, trong khi Studio REQ-003 yêu cầu mode 3 **có** toggle 利用しない + link 例文を挿入する (NEW-3, NEW-5, NEW-14 fail).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn ■3:

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `sendMessage()` / `sendActionBooking()` | Không | Mọi caller đều đi qua đúng 2 hàm này — web Basic, app mobile (Api/CalendarLessonController.php:433,465 · Api/CalendarSalonController.php:323) → web và app hành xử giống nhau, không có code path song song bị bỏ sót. |
| 2 | Endpoint `save-setting-message` | Có (validate mới) | Chỉ có 2 màn Lesson/Salon gọi; grep toàn repo không có consumer khác. |
| 3 | Hằng `SETTING_MESSAGE_APPROVE_TYPE_NO_CANCEL` | Mới | Định nghĩa ở calendar_detail.js:43 của cả 2 hệ, mixin setting-message.js nạp trước nhưng chỉ tham chiếu lúc chạy → không TDZ. |
| 4 | Blade sửa | Có | Truy được đủ chuỗi include; calendar_salon/tabs/setting-calendar.blade.php là bản chết (0 nơi include) → không có màn thứ 3 bị đổi giao diện ngoài ý muốn. |
| 5 | Job Java linect-service / backend-mcp-line | Không | Grep bảng/cột liên quan = 0 kết quả. backend-mcp-line chỉ đọc approve_type dạng String, giá trị 3 đã tồn tại từ trước → không vỡ contract, không cần bàn giao team Java. |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `saveSettingMessage` + validate mới — POST /basic/calendar-management/{id}/save-setting-message (chỉ màn Lesson) | app/Http/Controllers/Basic/CalendarManagementController.php:1387,1419 | Direct | W4 (có sẵn): :1402 ghi `CalendarSalon::where('id', calendar_id)` bằng id lịch Lesson |
| F2 | `saveSettingMessage` + validate — bản sao y hệt cho Salon | app/Http/Controllers/Basic/CalendarSalonController.php:3178,3207 | Direct | W3/W7 (có sẵn): :3190 ghi NULL `message_outside_filter`, thiếu `->where('bot_id', getBotId())` |
| F3 | case `'adminCancel'` — nhánh approve_type == 3 | app/Services/CalendarManagement/CalendarCourseBookingService.php:1045 | Direct | caller: web hủy thủ công + Api/CalendarLessonController (app mobile). W1 |
| F4 | case `'adminCancel'` — tương ứng Salon | app/Services/CalendarSalon/CalendarSalonLineBookingService.php:4223 | Direct | caller: web + Api/CalendarSalonController:323. W1 |
| F5 | `config('sns-line.version')` (cache-bust TOÀN CỤC mọi CSS/JS) + key `max_length_setting_message` | config/sns-line.php:62,1217 | Indirect | W9: phải config:clear/cache khi deploy |
| F6 | JS màn cài đặt (Lesson) | public/js/calendar_management/calendar_detail.js:4548,4582,5481,5528 | Direct | W2 (:5481 ép is_send_message=0), W5 (:5528 nhánh error 422) |
| F7 | JS màn cài đặt (Salon) | public/js/calendar_salon/calendar_detail.js:3370,3402 · public/js/calendar_salon/setting_reservation/setting-message.js:278,327 | Direct | W2 (setting-message.js:278), W5 (:327), W6 (alert xhr.responseJSON.message) |
| F8 | 4 blade setting_message / setting_message_cancel | calendar_management + calendar_salon | Direct | Heading riêng mode 3, ẩn/hiện control |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_setting_send_messages` / `calendar_salon_setting_send_messages` (moment='cancel') — `message_send_end` + `setting_action_id` | READ (mới ở mode 3) / UPDATE | Nay được ĐỌC ở chế độ approve_type=3 (trước chỉ đọc ở mode 1). **W1**: data tồn đọng từ mode 1 sẽ bắt đầu gửi tin + chạy action |
| D2 | cùng bảng — `is_send_message` | UPDATE | FE ép = 0 khi lưu ở mode 3; cột dùng chung với mode 1 → xoá âm thầm cờ 「利用しない」 của 全承認制 (**W2**) |
| D3 | `f_send_cancel_end` (chỉ Salon) | — | Checkbox bị ẩn ở mode 3 — cột chỉ được ghi, 0 nơi đọc trong PHP/JS/Java → ẩn không ảnh hưởng thứ tự gửi |
| D4 | `calendar_salon.message_outside_filter` | UPDATE (ghi NULL) | Bị hàm đã sửa ghi đè (W3/W4 — lỗi có sẵn, task làm tăng tần suất chạm) |
| D5 | config `sns-line.max_length_setting_message` / `sns-line.version` | CONFIG | Không migration, không ALTER, không ghi bảng dùng chung với job khác → không race |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | FA-019 calendar (Đặt lịch bài học / Lesson) — màn 予約キャンセル時の各種設定 + luồng admin hủy thủ công (web + app mobile) | F1, F3, F6, F8, D1, D2 | High (TRỰC TIẾP) |
| T2 | FA-020 calendar-salon (Đặt lịch salon) — màn 予約キャンセル時の各種設定 + luồng admin hủy thủ công (web + app mobile) | F2, F4, F7, F8, D1, D2, D3, D4 | High (TRỰC TIẾP) |
| T3 | エルメアクション (setting_action_id) nay chạy được ở mode 3: FA-012 tag (gắn thẻ), FA-009 scenario (kích bước kịch bản), FA-016 action-schedule, tin nhắn LINE gửi tới khách | F3, F4, D1 | High (GIÁN TIẾP — W1) |
| T4 | Chế độ 全承認制 / リクエスト制 (mode 1/2) — cờ 「利用しない」, nội dung tin hủy | D2, F6, F7 | Medium (W2) |
| T5 | Toàn bộ asset CSS/JS hệ thống (cache-bust qua `config('sns-line.version')`) | F5 | Low (conflict khi merge) |
| T6 | Tab 予約時 (moment='booking') cùng endpoint — không có validate 5.000 ký tự server | F1, F2 | Low (W8 — lệch chuẩn) |

> **Quét ngang 横展開 (■5 journal, ngoài phạm vi ticket)**: L1 HIGH — mode 3 chỉ chặn khách hủy ở FE (booking_history_detail.blade.php), endpoint `/ajax/calendar-cancel-booking` + `/calendar-cancel-booking` không guard approve_type==3 · L2 HIGH — W4/W7 · L3 MEDIUM — 24 blade có bộ đếm /5,000 nhưng chỉ 3 chỗ validate server · L4 LOW — `disabledButtonAddCode('cancel')` không có nhánh mode 3 (không phải lỗi).
>
> **Đã xác nhận an toàn (journal)**: mode 1/2 không bị chạm; hủy với 「không gửi tin」 ở mode 3 không gửi gì; app mobile cùng service; job Java không vỡ; bộ đếm FE ≥ mb_strlen server.
>
> **Verify của reviewer**: chỉ compile/lint (php -l, node --check) — **không chạy runtime test**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
