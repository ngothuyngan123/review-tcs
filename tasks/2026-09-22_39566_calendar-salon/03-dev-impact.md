# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #39566 — **journal #136532 (AI LME Fix bug, 2026-09-15)** = bản mới nhất, đã bao gồm toàn bộ nội dung của journal #134891 (2026-09-07) + 3 phần BỔ SUNG. Chép **nguyên văn**, không diễn giải lại.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — QA assignee: Ngô Thúy Ngần |
| Commit / Pull Request | `<không có link Github/Gitlab>` — Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39566 · Phiên AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=65772f57-295c-4a45-8912-1413c228ac7f |
| Branch | `ai_fixbug_39566` (repo `sns-line`, nhánh gốc `release_step_20260805`, commit `1b32a31c0a`, 32 file) — đã push |
| Ngày submit đánh giá | `2026-09-15` (journal #136532; bản đầu #134891 ngày 2026-09-07) |
| Auto-filled | `2026-09-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Các endpoint của lịch đặt chỗ salon trả HTTP code sai ý nghĩa: lỗi nghiệp vụ (không tìm thấy khoá học/nhân viên, vượt hạn mức gói) trả 500 (nghĩa là server sập) hoặc trả 200 (nghĩa là thành công), khiến giám sát báo động nhầm và phía màn hình không phân biệt được. Ngoài ra hầu hết endpoint nhận dữ liệu thẳng từ request mà không kiểm tra bắt buộc, thiếu tham số sẽ đi tới tận tầng service rồi báo lỗi chung chung hoặc lỗi hệ thống thật.

## 2. Cách fix

Refix theo AI review vòng 2 (1 lỗi bắt buộc). Reviewer nêu 12 nhánh lỗi còn trả HTTP 200; ĐỐI CHIẾU LẠI trên HEAD nhánh ai_fixbug_39566 thì chỉ còn ĐÚNG 4 nhánh — 8 nhánh còn lại (vượt hạn mức gói/vượt giới hạn số lượng ở createCourse, createCourseSalon, createStaffSalon, createNewSettingForm) ĐÃ được đổi sang 400 ở commit b5de531 cuối vòng 2; reviewer quét trúng commit trước đó (aaefe4ad) nên số dòng lệch 3 (499/526/1343/1350/1393/1400/1429/1765 là số dòng của aaefe4ad, nay là 503/531/1349/1357/1401/1409/1439/1776 và đều đã là 400 kèm ghi chú).

ĐÃ SỬA 4 nhánh thật sự còn trả 200 (đều nằm trong luồng hoàn tiền và thêm ca làm — đúng loại lỗi ticket nêu là giám sát bị mù):
(1) orderRefund — khối catch(Exception) trả 'Error' không kèm mã, mặc định 200 → nay 500 (lỗi hệ thống trong luồng hoàn tiền phải hiện ra cho giám sát).
(2) orderRefund — Stripe từ chối hoàn tiền, khai tường minh 200 → 400 (lỗi nghiệp vụ, giữ nguyên message của cổng thanh toán cho người dùng).
(3) orderRefund — Univapay từ chối hoàn tiền, khai tường minh 200 → 400 (giữ nguyên message đã dịch qua getMessageErrorUnivapay).
(4) addWorkScheduleForStaff — thêm ca làm thất bại không kèm mã, mặc định 200 → 400.

Phía màn hình: 2 endpoint này trả message ở khoá 'error_message' chứ không phải 'message', mà showSalonAjaxError chỉ đọc 'errors' và 'message' nên chuyển sang 4xx/5xx sẽ làm người dùng MẤT HẲN thông báo lỗi. Đã bổ sung đọc 'error_message' trong public/js/calendar_salon/ajax-error.js (ưu tiên 'message', fallback 'error_message'). Đã kiểm caller thật: cả 2 endpoint chỉ được gọi từ public/js/calendar_salon/calendar-management.js (orderRefund dòng 2492, addWorkScheduleForStaff dòng 1830), cả hai đều đã có nhánh error gọi window.showSalonAjaxError + hide overlay, và nhánh else cũ của chúng chỉ alert(error_message) nên chuyển sang nhánh error là tương đương (nhánh else cũ cũng không đóng modal ca làm). Blade duy nhất nạp calendar-management.js là basic/calendar_salon/detail.blade.php và blade này đã nạp sẵn ajax-error.js. Route api.php trỏ tới Api\CalendarSalonController (controller khác) nên không bị ảnh hưởng.

KIỂM CHỨNG (script đếm tự động, không khẳng định suông): quét toàn bộ 4629 dòng CalendarSalonController, bắt cả nhánh khai tường minh 200 lẫn nhánh không khai mã (mặc định 200) → số nhánh lỗi (success=false / status=false) còn trả 200 nay là 0 (trước refix là 4). php -l và node --check đều sạch.

CÒN LẠI CÓ CHỦ Ý — KHÔNG khẳng định 'đã hết sạch': còn 2 chỗ trả 200 với cờ thành công ĐỘNG, không nằm trong danh sách blocking của reviewer nên giữ nguyên để tránh mở rộng phạm vi: changeStatusBooking (dòng 3803, 'success' => $status, thành false khi xung đột trạng thái thanh toán) và createBooking (dòng 3813, trả thẳng mảng $response của service nên chưa rõ hình dạng). Muốn siết 2 chỗ này cần rà caller + hình dạng response của service, đề nghị human/PM quyết định gộp vào ticket này hay tách.

**[BỔ SUNG theo yêu cầu human 2026-08-20] Message validate 422 nay hiển thị TIẾNG NHẬT hoàn chỉnh.**
Trước đó locale đã là ja nên câu khung vốn là tiếng Nhật, nhưng :attribute bị ghép tên field thô tiếng Anh (vd "course menu idは必ず指定してください。") vì resources/lang/ja/validation.php không khai attributes cho các field mới — đúng cảnh báo W5 của reviewer vòng 3.
Cách làm: KHÔNG sửa resources/lang/ja/validation.php (file dùng chung toàn hệ thống, thêm key generic như id/order/calendar_id sẽ đổi câu thông báo của mọi màn khác). Thay vào đó khai 2 hằng số private ngay trong CalendarSalonController và truyền vào Validator::make($data, $rules, $messages, $attributes) — pattern có sẵn trong repo (CsvManagementController, FriendlistController, AffiliaterController...): (a) VALIDATION_MESSAGES_JA = câu thông báo theo house style của repo (required/required_if -> ":attributeを入力してください。", max -> ":attributeは:max文字以内で入力してください。", integer -> ":attributeは数値で入力してください。", in/array -> ":attributeの形式が正しくありません。", min -> ":attributeを選択してください。", riêng dataCreateStaff.min -> "スタッフ名を入力してください。" cho tự nhiên); (b) VALIDATION_ATTRIBUTES_JA = 22 nhãn field lấy ĐÚNG chữ trên màn hình chứ không tự đặt (calendar_name -> 店舗名 theo label setting_calendar_top.blade.php; manager_name -> カレンダー管理名 theo tiêu đề modal_edit_calendar_salon_manager_name; course_menu_name -> メニュー名 theo modal_create_course_menu; google_calendar_id -> Googleカレンダー theo calendar_setting_reservation; staff_name/staffName -> スタッフ名; courseName -> コース名; timeLine/timeLineList -> シフト; listId/order -> 並び順; id/calendar_id/calendarId -> カレンダー; timeBookingId -> 予約枠; action_id -> アクション; booking_page_display -> 予約ページでの表示; staff_id_default -> 連携するスタッフ).
Bám house style đã có trong chính domain lịch (app/Http/Requests/CreateCalendarCourse.php dùng "コース名を入力してください"); 41 file trong app/ đang dùng mẫu を入力してください.
Lưu ý kỹ thuật: Laravel resolve inline message qua getInlineMessage theo key "<field>.<rule>" hoặc "<rule>", KHÔNG nhận key dạng "max.string"/"min.array" -> phải khai phẳng "max"/"min"; đã rà lại: trong file này mọi rule max: đều áp cho chuỗi và mọi rule min: đều áp cho mảng nên khai phẳng là đúng. Key wildcard "dataCreateStaff.*.staff_name" hoạt động nhờ getPrimaryAttribute của Laravel 5.5.
KIỂM CHỨNG: chạy THẬT Illuminate Validation Factory với translator locale ja trên đúng 19 rule-set của cả 22 lời gọi validateInput -> 25/25 câu thông báo sinh ra đều là tiếng Nhật, không còn tên field tiếng Anh (chuỗi "Google" trong "Googleカレンダーを入力してください。" là danh từ riêng, đúng như UI đang viết). php -l sạch.

**[BỔ SUNG theo yêu cầu human 2026-09-15] Ràng buộc MỌI query theo bot đang đăng nhập trong CalendarSalonController (chống đọc/sửa/xoá chéo bot - IDOR).**
Quét tự động toàn controller (script cân bằng ngoặc, bắt cả câu nhiều dòng có closure): 106 query Eloquent, trong đó 78 câu CHƯA ràng buộc bot. Phân loại trước khi sửa: 32 câu nằm trong 25 hàm KHÔNG có bất kỳ ràng buộc bot nào - đây là lỗ hổng THẬT, id đến thẳng từ request rồi dùng luôn (getCalendarById, checkDeleteCourseMenu, getListCourseByCalendar, getListStaffByCalendar, getDetailEventStep, deleteCalendarStaff, checkAuthorGoogleSync, sendMailCodeAuthGoogleSync, changeTitleGoogleCalendarToNotDisplayed, getDataSettingNotifyFullSlot, getDataSettingPolicy, saveSettingMessage, saveSystemWordChange, checkBookingCancel, checkBookingCancelStaff, checkLinkedGoogleCalendar, getListHistorySyncBookingGoogleCalendar, getDetailHistorySyncForBooking...). 46 câu còn lại nằm trong hàm đã có guard chỗ khác (defense-in-depth). ĐÃ SỬA CẢ 78.

Cách ràng buộc chọn theo SCHEMA từng bảng, KHÔNG áp một công thức cho tất cả (theo rule human ở #40056):
(a) 11 bảng có bot_id NOT NULL (calendar_salon, calendar_salon_staff, calendar_salon_time_booking, calendar_salon_line_booking, setting_time_free, setting_limit_booking, setting_send_forms, setting_send_messages, setting_notify_full_history, booking_by_google, b_c_salon_google_calendar) -> lọc thẳng ->where(bot_id, getBotId()). NOT NULL chính là bằng chứng cột luôn được ghi lúc tạo nên lọc không giấu mất dữ liệu cũ.
(b) 4 bảng có bot_id nhưng DEFAULT NULL (calendar_salon_course, calendar_salon_course_menu, sync_booking_google_calendar_histories, download_csv_sync_google_calendar) -> CỐ Ý KHÔNG lọc thẳng bot_id vì dữ liệu cũ có thể đang để trống, lọc sẽ giấu mất bản ghi hợp lệ; thay bằng subquery qua LỊCH CHA nơi bot_id là NOT NULL.
(c) 3 bảng KHÔNG có cột bot_id (line_booking_history_actions chỉ có booking_id; history_change_setting_payment và b_c_salon_google_calendar_histories chỉ có calendar_id) -> ràng buộc gián tiếp qua bảng cha bằng subquery.

Thêm 2 helper private botCalendarIds() / botBookingIds() trả Closure subquery cho nhóm (b)+(c). Dùng getBotId() chứ không phải getBotIdInScope() vì controller này KHÔNG có endpoint nào nhận bot id từ client (đã grep cả controller lẫn public/js/calendar_salon). SQL sinh ra đã kiểm và có parameter binding đầy đủ: "... where calendar_salon_id = ? and calendar_salon_id in (select id from calendar_salon where bot_id = ?)". Đã grep xác nhận không có chỗ nào subquery trỏ vào chính bảng đang UPDATE/DELETE (bẫy MySQL "You cannot specify target table ... in FROM clause").

Đổi 15 chỗ Model::find($id) sang where(id)->where(bot_id)->first(): find() và first() đều trả null khi không thấy nên không đổi hành vi, chỉ thêm điều kiện bot. Đã rà MỌI chỗ deref sau đó bằng script: chỉ 2 chỗ (getListStepRemind, saveCreateSettingRemind) deref ngay mà không guard, nhưng cả 2 đã có checkCalendarBelongBot + trả 404 phía trên nên $calendar không thể null. Riêng orderRefund chưa có guard nào -> bổ sung trả 404 khi booking không tồn tại / không thuộc bot (trước đó null-deref rơi vào catch, báo lỗi hệ thống chung chung).

CÒN LẠI 1 điểm CÓ CHỦ Ý: CalendarSalonLineBookingHistoryAction::create() trong orderRefund là INSERT nên không có gì để lọc, và bảng này không có cột bot_id; an toàn theo bot vì booking_id lấy từ $booking đã được ràng buộc bot ngay phía trên. Đã ghi chú lý do trong code.

⚠ PHẠM VI CÓ CHỦ Ý - KHÔNG đụng 14 service trong app/Services/CalendarSalon (quét thấy 149 query cũng thiếu ràng buộc bot). Lý do kỹ thuật: getBotId() = Session::get(current_bot_id), mà các service này DÙNG CHUNG với 8 Console Command, 7 Job, Mobile\CalendarSalonController (màn đặt chỗ của KHÁCH) và Api\CalendarSalonController - những nơi KHÔNG có session. Nhét where(bot_id, getBotId()) vào service sẽ thành where(bot_id, null) => khớp 0 bản ghi => làm CHẾT toàn bộ cron đồng bộ Google Calendar, webhook thanh toán và màn đặt chỗ của khách. Đây đúng là trường hợp (3) trong rule human: hàm dùng chung thì chặn ở NƠI GỌI, không thêm điều kiện vào hàm chung. Muốn siết tầng service thì phải truyền $botId tường minh qua tham số (chuẩn .claude/docs/BE-coding-rules.md muc 4.1) - refactor riêng, nên tách ticket.

KIỂM CHỨNG: php -l sạch; script quét lại xác nhận 105/106 query đã có ràng buộc bot (1 còn lại là INSERT nêu trên); đã đọc lại toàn bộ dòng bị xoá trong diff để chắc không mất logic nào. ⚠ CHƯA chạy được test trên dữ liệu thật: MySQL dev không kết nối được từ container (Connection refused) và container không có pdo_sqlite, nên KHÔNG xác minh được bằng dữ liệu là 4 bảng nhóm (b) hiện có bao nhiêu row bot_id NULL - chính vì không kiểm chứng được nên mới chọn subquery qua lịch cha thay vì lọc thẳng. Cần human chạy regression trên môi trường có DB, tập trung vào: danh sách khoá học/nhân viên, xoá lịch (cascade 16 câu), đồng bộ Google Calendar và hoàn tiền.

**=== ⚠ TRẠNG THÁI PUSH (đọc trước khi duyệt) ===**
Trong lúc phiên chat này đang sửa, ticket đã được human duyệt và PUSH (WAITING_REVIEW -> WAITING_PM_REVIEW -> PM_APPROVED -> push) và đã ghi ngược Redmine "Fix done - Đợi test" (assign Ngô Thúy Ngần).
origin/ai_fixbug_39566 hiện ở commit b48ae2a2f5 = ĐÃ bao gồm phần chuẩn hoá HTTP code + validate + message tiếng Nhật.
Commit 8def715890 (ràng buộc mọi query theo bot đang đăng nhập) là commit MỚI, CHỈ có ở local, CHƯA push lên origin.
=> Bản QA đang test KHÔNG có phần vá bảo mật chéo bot. Cần DEV/PM review lại commit này rồi bấm Push để đẩy tiếp (chỉ ADD commit, KHÔNG rebase/amend vì branch đã push).
Đã đưa state từ PUSHED về WAITING_REVIEW để ticket quay lại cổng review 2 tầng, tránh dashboard hiển thị là đã xong.

**[SỬA theo yêu cầu human 2026-09-15] Bỏ thay đổi ở config/sns-line.php.**
Commit đầu của ticket (81f609ae42) có bump version 202608062210 -> 202608111200 trong config/sns-line.php. Đây là vi phạm rule NO_CONFIG_BUMP (cache-bust tài nguyên tĩnh là việc của đội release, không phải của từng ticket fix).
Commit 81f609ae42 ĐÃ push lên origin nên KHÔNG rewrite history (lesson no-history-rewrite) - đã revert bằng commit MỚI 1b32a31c0a.
Giá trị đưa về là giá trị của MERGE-BASE (202608062210), KHÔNG phải giá trị hiện tại của release (release đã tự bump lên 202608181516 sau khi branch tách ra). Đưa về merge-base nghĩa là branch này KHÔNG đụng file đó, khi merge vào release thì giá trị của release thắng; nếu đưa về giá trị release hiện tại thì lại thành một thay đổi thật đứng tên branch này.
Đã xác nhận: git diff release_step_20260805...ai_fixbug_39566 -- config/sns-line.php nay TRỐNG; số file thay đổi giảm từ 33 xuống 32.
GIỮ NGUYÊN 28 chỗ nhúng ?v={{config('sns-line.version')}} trong blade cho các file JS mới thêm - đúng rule (file mới URL mới nên không dính cache), chỉ bỏ đúng việc bump số version.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN" của journal #136532 — Dev list dạng plain, convert sang bảng, giữ nguyên nội dung.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonController::createNewCalendarSalon` (`app/Http/Controllers/Basic/CalendarSalonController.php`) | Chuẩn hoá HTTP code + validate required | Endpoint tạo lịch salon |
| 2 | `CalendarSalonController::createStaffCalendarSalon` (cùng file) | Chuẩn hoá HTTP code + validate required | Endpoint tạo nhân viên |
| 3 | `CalendarSalonController::saveSort` (cùng file) | Chuẩn hoá HTTP code + validate required | Endpoint sắp xếp |
| 4 | `CalendarSalonController::deleteItemEvent` (cùng file) | Chuẩn hoá HTTP code + validate required | Endpoint xoá item event |
| 5 | `CalendarSalonController::updateCalendarSettingEvent` (cùng file) | Chuẩn hoá HTTP code + validate required | Endpoint cập nhật setting event |
| 6 | `CalendarSalonController::deleteCourseMenu` / `deleteImageCourseMenu` (cùng file) | Chuẩn hoá HTTP code + validate required | Endpoint xoá menu khoá học / ảnh menu |
| 7 | `CalendarSalonController::updateBookingPageDisplay` / `updateBookingPageDisplayStaff` (cùng file) | Chuẩn hoá HTTP code + validate required | Endpoint đổi hiển thị trên trang đặt chỗ |
| 8 | `CalendarSalonController::updateCalendarCourseOrder` / `updateCalendarStaffOrder` (cùng file) | Chuẩn hoá HTTP code + validate required | Endpoint đổi thứ tự khoá học / nhân viên |
| 9 | `CalendarSalonController::deleteItemAction` / `deleteItemActionStaff` (cùng file) | Chuẩn hoá HTTP code + validate required | Endpoint xoá action |
| 10 | `CalendarSalonController::validateInput` (cùng file) | **Helper MỚI** | Hàm dùng chung cho 22 lời gọi validate — ⚠️ hàm dùng chung, cần rà đủ caller |
| 11 | `CalendarSalonService` (`app/Services/CalendarSalon/CalendarSalonService.php`) | 14 nhánh trả lỗi | Chuẩn hoá nhánh lỗi tầng service |
| 12 | `CalendarSalonCourseService` (`app/Services/CalendarSalon/CalendarSalonCourseService.php`) | 13 nhánh trả lỗi | Chuẩn hoá nhánh lỗi tầng service |
| 13 | `CalendarSalonStaffService` (`app/Services/CalendarSalon/CalendarSalonStaffService.php`) | 12 nhánh trả lỗi | Chuẩn hoá nhánh lỗi tầng service |
| 14 | `showSalonAjaxError` (`public/js/calendar_salon/ajax-error.js`) | Bổ sung đọc khoá `error_message` (ưu tiên `message`, fallback `error_message`) | ⚠️ **Hàm dùng chung toàn bộ màn lịch salon** — nếu không sửa thì user MẤT HẲN thông báo lỗi sau khi đổi sang 4xx/5xx |
| 15 | `Api\CalendarSalonController` (`app/Http/Controllers/Api/CalendarSalonController.php`) | **Đã khảo sát, KHÔNG sửa** | App điện thoại (`lme-fluter-app`) chỉ đọc `error_message` ở nhánh `statusCode==200`; đổi mã ở lớp api phải đi kèm bản phát hành app |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev khai mục 4.1 là **danh sách FILE thay đổi**, không phải function. Giữ nguyên nội dung, gắn tag `F*` để map coverage.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Basic\CalendarSalonController` — 22 lời gọi `validateInput`, chuẩn hoá mã HTTP 422/400/404/500, ràng buộc bot cho 78 query, 2 helper `botCalendarIds()` / `botBookingIds()` | `app/Http/Controllers/Basic/CalendarSalonController.php` | Direct | File trung tâm của fix (4629 dòng) |
| F2 | `CalendarSalonService` — 14 nhánh trả lỗi | `app/Services/CalendarSalon/CalendarSalonService.php` | Direct | Dùng chung với Console Command / Job / Mobile / Api |
| F3 | `CalendarSalonCourseService` — 13 nhánh trả lỗi | `app/Services/CalendarSalon/CalendarSalonCourseService.php` | Direct | Dùng chung |
| F4 | `CalendarSalonStaffService` — 12 nhánh trả lỗi | `app/Services/CalendarSalon/CalendarSalonStaffService.php` | Direct | Dùng chung |
| F5 | `showSalonAjaxError` | `public/js/calendar_salon/ajax-error.js` | Direct | **Hàm dùng chung toàn màn lịch salon** |
| F6 | JS danh sách lịch | `public/js/calendar_salon/index.js` | Direct | |
| F7 | JS chi tiết lịch | `public/js/calendar_salon/calendar_detail.js` | Direct | |
| F8 | JS đặt chỗ | `public/js/calendar_salon/booking.js` | Direct | |
| F9 | JS quản lý lịch (caller của `orderRefund` dòng 2492 + `addWorkScheduleForStaff` dòng 1830) | `public/js/calendar_salon/calendar-management.js` | Direct | |
| F10 | JS bước khởi tạo lịch | `public/js/calendar_salon/step_create.js` | Direct | |
| F11 | JS sửa khoá học | `public/js/calendar_salon/edit_course.js` | Direct | |
| F12 | JS sửa nhân viên | `public/js/calendar_salon/edit_staff.js` | Direct | |
| F13 | JS thêm đơn đặt mới | `public/js/calendar_salon/add-new-booking.js` | Direct | |
| F14 | JS cài đặt tin nhắn | `public/js/calendar_salon/setting_reservation/setting-message.js` | Direct | |
| F15 | JS cài đặt thanh toán | `public/js/calendar_salon/setting_reservation/setting-payment.js` | Direct | |
| F16 | JS cài đặt nhắc lịch | `public/js/calendar_salon/setting_reservation/setting-remind.js` | Direct | |
| F17 | Blade danh sách lịch | `resources/views/basic/calendar_salon/index.blade.php` | Direct | |
| F18 | Blade chi tiết lịch (blade duy nhất nạp `calendar-management.js`, đã nạp sẵn `ajax-error.js`) | `resources/views/basic/calendar_salon/detail.blade.php` | Direct | |
| F19 | Blade layout đơn đặt | `resources/views/basic/calendar_salon/bookings/layouts/main.blade.php` | Direct | |
| F20 | Blade tạo lịch mới | `resources/views/basic/calendar_salon/calendar_salon_create_new.blade.php` | Direct | |
| F21 | Blade tạo nhân viên | `resources/views/basic/calendar_salon/calendar_salon_create_staff.blade.php` | Direct | |
| F22 | Blade tạo khoá học | `resources/views/basic/calendar_salon/calendar_salon_course_create.blade.php` | Direct | |
| F23 | Blade hiển thị event | `resources/views/basic/calendar_salon/calendar_salon_display_event.blade.php` | Direct | |
| F24 | Blade hiển thị event nhiều nhân viên | `resources/views/basic/calendar_salon/calendar_salon_display_event_many_staff.blade.php` | Direct | |
| F25 | Blade setting event | `resources/views/basic/calendar_salon/calendar_salon_setting_event.blade.php` | Direct | |
| F26 | Blade loại nhân viên | `resources/views/basic/calendar_salon/calendar_staff_type.blade.php` | Direct | |
| F27 | Blade tab sửa khoá học | `resources/views/basic/calendar_salon/tabs/course/edit_course.blade.php` | Direct | |
| F28 | Blade tab sửa nhân viên | `resources/views/basic/calendar_salon/tabs/staff/edit_staff.blade.php` | Direct | |
| F29 | ~~`config/sns-line.php`~~ | `config/sns-line.php` | **ĐÃ REVERT** | Mục 4.1 của journal vẫn liệt kê file này, nhưng phần "[SỬA theo yêu cầu human 2026-09-15]" của cùng journal xác nhận đã revert bằng commit `1b32a31c0a`; `git diff` với file này nay TRỐNG, số file giảm 33 → 32. **Không test cache-bust version.** |

### 4.2. List data bị update khi fix bug

> Nguyên văn mục 4.2: *"Không có - chỉ đổi mã HTTP trả về và thêm kiểm tra đầu vào, không đổi cấu trúc bảng, không sửa dữ liệu đã có"*.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** — không đổi cấu trúc bảng, không sửa dữ liệu đã có | — | Nguyên văn Dev khai ở mục 4.2 |

⚠️ **Leader lưu ý — mục 4.2 khai "Không có" nhưng phần BỔ SUNG 2026-09-15 của cùng journal có nêu 18 bảng bị đổi CÁCH ĐỌC/GHI (điều kiện `WHERE` mới), không phải đổi schema.** Đây là vùng regression dữ liệu thật, ghi lại để viết TC (không phải Dev khai ở 4.2):

| # | Nhóm bảng | Cách ràng buộc bot | Rủi ro |
|---|---|---|---|
| D2 | 11 bảng có `bot_id` **NOT NULL**: `calendar_salon`, `calendar_salon_staff`, `calendar_salon_time_booking`, `calendar_salon_line_booking`, `setting_time_free`, `setting_limit_booking`, `setting_send_forms`, `setting_send_messages`, `setting_notify_full_history`, `booking_by_google`, `b_c_salon_google_calendar` | Lọc thẳng `->where(bot_id, getBotId())` | Lọc sai → mất dữ liệu hợp lệ của chính bot |
| D3 | 4 bảng có `bot_id` **DEFAULT NULL**: `calendar_salon_course`, `calendar_salon_course_menu`, `sync_booking_google_calendar_histories`, `download_csv_sync_google_calendar` | **KHÔNG** lọc thẳng — subquery qua lịch cha | ⚠️ Dev **CHƯA verify được bằng dữ liệu thật** có bao nhiêu row `bot_id = NULL` → rủi ro cao nhất: danh sách khoá học / menu / lịch sử sync / CSV bị **giấu mất** bản ghi cũ |
| D4 | 3 bảng **KHÔNG có** cột `bot_id`: `line_booking_history_actions` (chỉ `booking_id`), `history_change_setting_payment` + `b_c_salon_google_calendar_histories` (chỉ `calendar_id`) | Subquery qua bảng cha | |
| D5 | 15 chỗ `Model::find($id)` → `where(id)->where(bot_id)->first()` | — | `find()`/`first()` đều trả `null` khi không thấy nên Dev khai không đổi hành vi; riêng `orderRefund` bổ sung **404** khi booking không tồn tại / không thuộc bot |
| D6 | `CalendarSalonLineBookingHistoryAction::create()` trong `orderRefund` | INSERT — CÓ CHỦ Ý không lọc (bảng không có `bot_id`) | An toàn nhờ `booking_id` lấy từ `$booking` đã ràng buộc bot |
| D7 | Xoá lịch salon — **16 câu xoá cascade** | Qua ràng buộc bot mới | ⚠️ Dev yêu cầu human test riêng vùng này |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Salon Booking (FA-020)** — toàn bộ màn quản trị lịch đặt chỗ salon: tạo lịch, khoá học, nhân viên, khung giờ, cài đặt đặt chỗ; nay trả đúng mã 422/400/404/500 và chặn thiếu dữ liệu bắt buộc ngay tại server | F1–F28, D2–D7 | **High** |
| T2 | **Lesson Booking (FA-019)** — **KHÔNG sửa**, chỉ ghi nhận trong quét ngang là có cùng kiểu trả 500 cho lỗi nghiệp vụ | (quét ngang) | Low — không bị chạm code |
| T3 | **Event Booking (FA-021)** — **KHÔNG sửa**, chỉ ghi nhận trong quét ngang là có cùng kiểu trả 500 cho lỗi nghiệp vụ | (quét ngang) | Low — không bị chạm code |
| T4 | **App mobile admin + LIFF đặt chỗ của khách** (`Api\CalendarSalonController`, `Mobile\CalendarSalonController`) — hợp đồng KHÔNG đổi, vẫn trả 200 + `error_message` | F2–F4 (service dùng chung), mục 6 VERIFY | **High** — service dùng chung với 8 Console Command, 7 Job, Mobile, Api (không có session) |
| T5 | **Cron / Job đồng bộ Google Calendar + webhook thanh toán** — dùng chung 14 service trong `app/Services/CalendarSalon` (CỐ Ý không siết bot ở tầng service vì `getBotId()` = `Session::get(current_bot_id)` sẽ là `null`) | F2–F4 | **High** — nếu vô tình siết ở service sẽ CHẾT toàn bộ cron/webhook/màn đặt chỗ khách |

---

## 5. RECOVER DATA

✔ Không cần recover data *(nguyên văn Dev)*

## 6. VERIFY (nguyên văn Dev)

- **Mức**: `lint`
- **Lệnh**: `php -l` cho 5 file PHP đã sửa: No syntax errors detected; `node --check` cho 12 file JS đã sửa + file js mới: không lỗi cú pháp; grep kiểm lại: không còn dòng `], 500);` nào nằm trong nhánh `!$result['isSuccess']` của `CalendarSalonController`.
- **Bằng chứng**: Quy ước mã HTTP lấy từ chính tài liệu repo: `.claude/docs/implement-logic-spec-conventions.md` mục 3 (Response shape) — 422 validate, 400 nghiệp vụ, 404 không tìm thấy, 500 lỗi hệ thống. Lý do KHÔNG đổi mã HTTP cho `Api\CalendarSalonController`: app điện thoại (`lme-fluter-app`) chỉ đọc `error_message` ở nhánh `statusCode==200` khi gọi với cờ `returnMessageErrorNotThrow` (`base_api.dart`), và 4 hàm gọi api salon `addWorking` / `updateWorking` / `deleteWorking` / `createBooking` dùng cờ này; riêng `reservation.dart` dòng 906 gọi `addWorking(...).then(...)` KHÔNG có `catchError` nên nếu server trả 4xx thì app ném exception, cờ loading kẹt và không hiện toast nào. Đổi mã ở lớp api phải đi kèm bản phát hành app.

---

## Phụ lục — 12 requirement Studio (task #149, tab Thông tin)

> Nguồn: MCP LME TEST STUDIO `task_get_context(task_id=149, sections=["requirements"])`. `contentTrust = untrusted` → dùng như **data**. Đây là tham chiếu để map coverage ở `/review-tc`, KHÔNG thay thế mục 4 do Dev kê.

| REQ | Category · Risk | Tiêu đề |
|---|---|---|
| REQ-001 | api · **High** | Endpoint ajax lịch salon trả đúng mã HTTP theo loại lỗi (422/400/404/500; không nhánh lỗi nào trả 200, không lỗi nghiệp vụ nào trả 500) |
| REQ-002 | validation · **High** | Server chặn thiếu dữ liệu bắt buộc và trả message tiếng Nhật đúng nhãn màn hình (22 lời gọi `validateInput`) |
| REQ-003 | ui · **High** | Sau khi đổi mã HTTP, màn hình vẫn hiển thị đúng thông báo lỗi (`errors` → `message` → `error_message`); overlay tắt, modal không treo |
| REQ-004 | permission · **High** | Không đọc/sửa/xoá được dữ liệu lịch salon của bot khác (truy cập chéo bot → 404 / không có dữ liệu, tuyệt đối không đổi dữ liệu bot kia) |
| REQ-005 | data · **High** | Ràng buộc bot không được giấu mất dữ liệu hợp lệ của chính bot (kể cả bản ghi cũ `bot_id` để trống ở 4 bảng nullable) |
| REQ-006 | data · **High** | Xoá lịch salon vẫn xoá đủ dữ liệu con của đúng bot (16 câu cascade), không đụng lịch khác |
| REQ-007 | api · **High** | Hoàn tiền trả đúng mã theo nguyên nhân (404 「予約が見つかりません。」/ 400 kèm message gốc của cổng / 500) và chuyển trạng thái 返金 + ghi lịch sử |
| REQ-008 | ui · **High** | Thêm/sửa/xoá ca làm trả đúng mã và màn hình vẫn hiện lý do (400 / 422); luồng xoá sạch ca rồi lưu vẫn phải lưu được |
| REQ-009 | validation · Medium | Vượt hạn mức gói / trần số lượng trả 400, giữ nguyên nội dung thông báo (trần 200 khoá, 200 nhân viên, 100 câu hỏi) |
| REQ-010 | api · **High** | Hợp đồng lớp API khách/mobile không đổi (vẫn 200 + `error_message`); job/cron dùng chung service vẫn chạy |
| REQ-011 | api · Medium | Ghi nhận hiện trạng 2 endpoint CỐ Ý giữ 200 (`changeStatusBooking`, `createBooking`) — không báo bug nhầm |
| REQ-012 | ui · **High** | Liên kết + đồng bộ Google Calendar vẫn đúng sau khi siết bot (xác thực mã qua email → 400 khi sai; tab データ同期履歴 + CSV vẫn đủ dữ liệu) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ `validateInput` (F1) + `showSalonAjaxError` (F5) là **hàm dùng chung**, cần danh sách caller đầy đủ
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ Dev kê **file**, không kê function
- [ ] Mục 4.2 không thiếu data — ⚠️ Dev khai "Không có" nhưng thực tế có **18 bảng đổi điều kiện đọc/ghi** (xem D2–D7)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC — ⚠️ **hỏi ngay: commit nào đang có trên môi trường QA** (`b48ae2a2f5` không có vá chéo bot vs `1b32a31c0a`)
