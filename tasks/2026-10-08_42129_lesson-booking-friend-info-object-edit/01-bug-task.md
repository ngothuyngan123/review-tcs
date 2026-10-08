# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine qua `/new-task 42129` (`scripts/redmine_fetch.py`).
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL) tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42129 — [Lesson] Booking lưu friend infor dạng object, khi edit không get được thông tin cũ` |
| Module / Màn hình | Lesson booking (FA-019 — 「レッスン予約」), module **Admin web**: màn chi tiết lịch Lesson (`/basic/calendar-management`) — modal 「予約追加」 (thêm booking) + 「お客様情報を編集」 (sửa thông tin khách) ở cả 3 lối vào (modal chi tiết slot, chi tiết booking chế độ 「一覧」, tab 「本日／新着の予約」) |

## Mô tả bug (bản dịch tiếng Việt)

> Nội dung khách báo đã là tiếng Việt — giữ nguyên văn, không diễn giải lại.

1. Friend infor: name + email + 1 friend infor khác
2. ẩn email đi
3. admin booking => tbl calendar_salon_line_booking.friend_infor của booking đó bị lưu dạng object {
4. admin vào detail booking đó => edit friend infor

Hiện tại: thông tin get ra bị trống
Expect: get được thông tin cũ

## Steps to reproduce

1. Cấu hình form câu hỏi booking Lesson gồm: tên (friend info), email, và 1 friend info khác — theo thứ tự đó.
2. Ẩn (非表示) câu email.
3. Admin vào màn chi tiết lịch, thêm booking (予約追加) cho một bạn LINE — booking được lưu nhưng cột `friend_info` của booking đó bị lưu dạng **object** `{...}` (key nhảy cóc) thay vì mảng JSON.
4. Admin vào chi tiết booking đó, bấm 「お客様情報を編集」 để sửa thông tin khách.

## Expected result

- Form sửa thông tin khách (「お客様情報を編集」) điền sẵn đúng giá trị cũ của booking.

## Actual result

- Thông tin get ra bị trống (form sửa không điền được giá trị cũ).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

*(Redmine #42129 không có attachment.)*

## Ghi chú thêm của Leader

- ⚠️ Mô tả gốc ghi bảng `calendar_salon_line_booking` — theo Dev xác nhận ở journal + Studio (note TC "Tái hiện bug", human-correction #136), **bảng đúng là `calendar_course_bookings`** (Lesson, không phải Salon). Bug thuộc Lesson booking, Salon chỉ bị regression smoke (xem file 03 mục 4.3 — T4).
- Root cause (theo Dev): JS tạo `formQuestion` bằng `map`, trả `{}` cho câu ẩn → jQuery bỏ phần tử rỗng → PHP nhận mảng key nhảy cóc (0,1,4,...) → `CalendarCourseBookingService::create` `json_encode` thẳng thành JSON **object** thay vì **array**. Lúc mở form sửa, `showEditFormBooking` gọi `friendInfo.find(...)` trên object → `TypeError`, không điền được giá trị cũ.
- Status Redmine hiện tại: **Fix done - Đợi test**. Nhánh fix: `ai_studio_fixbug_42129_v1` (base `release_step_20260930_v2`).
- Deploy note (Dev): file JS nạp với `?v=` cố định, **không bump version** → tester/admin phải **hard-reload (Ctrl+F5)** trang chi tiết lịch sau deploy trước khi test, nếu không JS cũ vẫn chạy từ cache.
- Bug không ghi tần suất xác suất — theo mô tả root cause thì xảy ra **mọi lần** admin tạo booking khi form có câu hỏi ẩn (không phải lỗi ngẫu nhiên).
- MCP LME TEST STUDIO đã có task #374 cho ticket này (17 TC do AI + 2 TC do `quyend@mcp` viết, round 1, trạng thái `done-ai`, reviewState `leader`) — xem `04-tc-list.md` (fetch từ Studio, KHÔNG phải từ Google Sheet).

## Journal / note từ Redmine (nguyên văn)

**Journal #140763 — Dev Studio — 2026-10-07:**

```
Dev Studio · Nguyên nhân & hướng sửa (v1)

Nguyên nhân:
Khi admin tạo booking Lesson trên web, JS tạo `formQuestion` bằng `map` và trả `{}` cho các câu ẩn. jQuery bỏ các phần tử rỗng này nên PHP nhận mảng có key nhảy cóc (0,1,4). `CalendarCourseBookingService::create` gọi `json_encode` thẳng nên lưu thành JSON object. Lúc mở form sửa, `showEditFormBooking` gọi `friendInfo.find(...)` trên object nên báo lỗi TypeError và không điền được giá trị cũ.

Hướng sửa:
- D-1 Lưu friend_info của booking admin Lesson dạng danh sách
- D-2 Form sửa thông tin khách đọc được dữ liệu cũ dạng object

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng luồng admin tạo booking Lesson trên web và form sửa thông tin khách ở màn chi tiết lịch Lesson. Mọi nơi đọc vẫn hiểu được dạng danh sách. Salon và app không đổi hành vi.
```

**Journal #140806 — Dev Studio — 2026-10-07:**

```
Dev handoff — v1 · nhánh test ai_studio_fixbug_42129_v1

Nguyên nhân:
Khi admin tạo booking Lesson trên web, JS tạo `formQuestion` bằng `map` và trả `{}` cho các câu ẩn. jQuery bỏ các phần tử rỗng này nên PHP nhận mảng có key nhảy cóc (0,1,4). `CalendarCourseBookingService::create` gọi `json_encode` thẳng nên lưu thành JSON object. Lúc mở form sửa, `showEditFormBooking` gọi `friendInfo.find(...)` trên object nên báo lỗi TypeError và không điền được giá trị cũ.

Nội dung thay đổi:
- Web admin, chi tiết lịch Lesson, tạo booking cho bạn bè: friend_info lưu dạng list kể cả khi form có câu hỏi ẩn (module web).
- Web admin, chi tiết booking Lesson, 「お客様情報を編集」 ở cả 3 lối vào (modal slot, chi tiết booking, booking hôm nay): điền được giá trị cũ với booking lưu dạng object trước đây và không lỗi với booking không có câu trả lời (module web).

File đã sửa (php-web):
  app/Services/CalendarManagement/CalendarCourseBookingService.php | 2 +-
  public/js/calendar_management/calendar_detail.js                 | 4 +++-
  2 files changed, 4 insertions(+), 2 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Hai thay đổi nhỏ và cục bộ (một array_values khi lưu, một biến cục bộ trong hàm mở form sửa); dạng dữ liệu mới trùng dạng mặc định mọi booking khác đang dùng.
- Các nơi đọc friend_info của booking Lesson: 4 modal xem chi tiết booking (v-for), export CSV booking, cập nhật friend info bạn bè sau khi duyệt booking, Google Calendar sync — đều đã nhận list từ các booking khác nên không đổi.
- Luồng admin tạo booking Lesson khi bạn bè đang có booking chờ huỷ (update thay vì insert) dùng cùng dữ liệu ghi.
- Không chạm app mobile, LIFF, Salon, job Java; API không đổi contract.

Lưu ý khi deploy:
- Không migration, không SQL, không đổi config; không sửa Blade nên không cần view:clear.
- JS nạp với ?v= cố định, không bump: tester/admin hard-reload (Ctrl+F5) trang chi tiết lịch sau deploy.

Việc cần người làm thêm (ngoài phạm vi task):
- Salon (CalendarSalonLineBookingService create) cũng lưu friend_info dạng object theo cùng cách, nhưng UI không lỗi vì đã chuẩn hoá khi đọc; có thể làm ticket riêng nếu muốn dữ liệu đồng nhất.
- Salon (CalendarSalonLineBookingService) và API app Lesson (Api CalendarLessonController) cũng ghi friend_info theo cùng kiểu, có thể ra object. Hiện chưa gây lỗi giao diện nên ticket này không sửa; nếu muốn dữ liệu đồng nhất thì tạo ticket riêng.
- Đồng bộ cùng khuôn array_values cho các điểm ghi friend_info còn lại (Salon web CalendarSalonLineBookingService, API app CalendarLessonController và CalendarSalonController) trong một ticket cải tiến riêng; hiện không gây lỗi UI.

Điểm cần test:
- Form Lesson gồm tên + email + 1 câu friend info, ẩn câu email; admin tạo booking: DB friend_info bắt đầu bằng '[' và 「お客様情報を編集」 hiện đủ giá trị cũ
- Booking cũ đã lưu dạng object: mở form sửa thấy giá trị cũ; lưu lại thì friend info của bạn bè cập nhật đúng
- Kiểm đủ 3 lối vào nút sửa: modal chi tiết slot, chi tiết booking, booking hôm nay
- Form không ẩn câu nào: tạo và sửa vẫn bình thường; booking không có câu hỏi (friend_info null) mở form sửa không báo lỗi console
- Màn xem chi tiết booking Lesson vẫn hiện đủ câu trả lời; Salon không đổi
- Lịch Lesson có form: tên + メールアドレス + 1 câu gắn friend info khác, ẩn câu email. Admin tạo booking cho bạn bè ở màn chi tiết lịch → DB calendar_course_bookings.friend_info bắt đầu bằng '[' ; mở 「お客様情報を編集」 thấy đủ giá trị cũ, console không lỗi.
- Booking Lesson cũ đã lưu object (tạo trước bản sửa) → mở sửa hiện đủ giá trị cũ; lưu → friend_info thành list, friend info bạn bè cập nhật đúng; mở sửa lại vẫn đúng.
- Kiểm cả 3 lối vào nút sửa: modal chi tiết slot, chi tiết booking (tuần/tháng), booking hôm nay.
- Không ẩn câu nào: tạo + sửa bình thường. Booking không có câu trả lời (friend_info null) trên lịch có câu hỏi: mở sửa không lỗi console.
- Màn xem chi tiết booking vẫn hiển thị đủ câu trả lời; export CSV booking và Google Calendar sync của lịch Lesson vẫn chạy.
- Admin tạo booking Lesson qua app, user đặt qua LIFF, Salon tạo/sửa booking: không đổi hành vi.
- Trước khi test, Ctrl+F5 trang chi tiết lịch vì JS ?v= không bump.

Nhánh:
- php-web: ai_studio_fixbug_42129_v1 @0601744e4c0c41222315f1fe7bc34718ff38fb1e (base release_step_20260930_v2 @bdeac6b86989)
```
