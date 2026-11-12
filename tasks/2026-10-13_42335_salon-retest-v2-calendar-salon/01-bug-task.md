# 01 — Bug Task từ khách hàng

> ⚠️ **Ticket #42335 KHÔNG phải ticket bug đơn lẻ** — đây là ticket **re-test phạm vi** (lần 2, nối tiếp `#42274` "[Re-test v1]" ở `tasks/2026-10-07_42274_re-test-salon-tcs/`). QA chủ động yêu cầu re-test lại **toàn bộ** tính năng Calendar Salon sau khi nhiều fix đã lên branch `release_step_20260930_v2`. Không có Steps/Expected/Actual của 1 ca lỗi cụ thể như ticket bug thông thường. Auto-fill từ Redmine `#42335` qua `/new-task`.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42335 — [Salon] [Re-test v2] Re-test lại toàn bộ tính năng calendar salon` |
| Module / Màn hình | Calendar Salon (cả loại **スタッフ** và **個人**) — admin web + app mobile. Controller liên quan theo diff: `Mobile\CalendarSalonController`, `Basic\CalendarSalonController`, `Basic\CalendarManagementController`, `Api\CalendarSalonController`, service `Services\CalendarSalon\*` (`CalendarSalonLineBookingService`, `CalendarSalonGoogleCalendarService`, `CalendarSalonStaffService`, `CalendarSalonCourseService`), job `Jobs\CalendarSalonStaffAssignment(Admin)`. Xem chi tiết diff ở Phụ lục `03-dev-impact.md`. |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Nội dung Redmine gốc đã là tiếng Việt — giữ nguyên văn, không diễn giải lại. -->

Phạm vi re-test:
* Test lại toàn bộ logic cài đặt của salon calendar và các case booking phía line friend tương ứng. Thứ tự ưu tiên test:
1. Setting limit calendar và limit staff: Gồm các option limit 1.1, 1.2, 2 và 3
2. Setting random staff khi chọn vào staff không chỉ định: Không random, random ngẫu nhiên, random theo thứ tự ưu tiên
3. Setting mùa vụ
4. Setting time nghỉ trước sau
5. Setting thời gian có thể bắt đầu nhận booking, nhận cancel booking
6. Setting action lúc booking, action lúc cancel
7. Setting giới hạn nhận booking 予約の受付制限 và setting ẩn hiển thị calendar đối với friend 予約ページの非表示
8. Setting send remind sau khi booking success: remind loại send trước time bắt đầu 予約開始前, remind loại send sau time kết thúc 予約終了後
9. Setting form info: test đủ các loại item form: 2 item mặc định, short text, long text, radio, checkbox, date, date time
10. Setting bill tiền: Stripe, Univpay, Bill tại chỗ
11. Setting liên kết google spread
12. Setting liên kết google calendar
13. Check việc booking và hủy booking theo những setting mà admin đã cài đặt: User thao tác, admin thao tác trên web, admin thao tác trên app mobile

* Đảm bảo test đầy đủ các loại setting tôi đã liệt kê ở trên, mỗi loại setting có những cài đặt gì thì test cho đủ, sau đó test mix các loại setting với nhau
* Đảm bảo test trên cả calendar loại staff và calendar loại private. Về các cài đặt của admin cần test cả trên web và app mobile

Hãy đọc spec-features cũ và TCs cũ trước khi viết TCs.

## Steps to reproduce

<!-- Không áp dụng — ticket là re-test phạm vi, không mô tả 1 ca lỗi cụ thể để tái hiện. -->

## Expected result

<!-- Không áp dụng ở cấp ticket — expected cụ thể của từng TC xem `04-tc-list.md`. -->

## Actual result

<!-- Không áp dụng — 334 TC trong task Studio #376 đang ở trạng thái "Chưa chạy" (xem §Kết quả thực thi trong `04-tc-list.md`). -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #42335: Attachments (0) — không có đính kèm. -->

## Ghi chú thêm của Leader

- Branch đang test: `release_step_20260930_v2`.
- **Spec cũ** (human đưa link trực tiếp — không phải `spec-features/`): https://spec-studio.melonglobal.net/p/lme/specs/admin/calendar-salon — đọc trước khi viết/review TC theo quy tắc nguồn spec (`spec-features/calendar-salon/feature-spec.md` nếu có, cộng link này).
- **TCs cũ** (human đưa link trực tiếp, KHÔNG có `Row: <start>-<end>` nên không tự fetch theo BƯỚC 6 được): https://docs.google.com/spreadsheets/d/18aOAtq6BzHbSII5TDX1b_yGztlI4U9DPIezapkwU34k/edit?gid=2038853093 — Sheet "FA-020 Đặt lịch salon (サロン・面談予約)". `04-tc-list.md` hiện tại lấy từ **MCP LME TEST STUDIO** (fallback BƯỚC 6b) vì Redmine không có format `Link TCs` + `Row:` chuẩn — xem cảnh báo trong `04-tc-list.md`.
- Ticket #42335 nối tiếp `#42274` ([Re-test v1]) — xem `tasks/2026-10-07_42274_re-test-salon-tcs/` để biết các FIX-01–FIX-14 / VERIFY-01–05 đã audit trước đó, phần nào đã lên `release_step_20260930_v2`.
- Yêu cầu bắt buộc: test đủ **cả 2 loại calendar** (スタッフ / 個人) và **cả 2 kênh admin** (web + app mobile) cho mọi mục setting, sau đó test **mix nhiều setting cùng lúc**.

## Journal / note từ Redmine (nguyên văn)

<!-- Redmine #42335: Journals có notes (0) — không có journal nào để trích. -->
