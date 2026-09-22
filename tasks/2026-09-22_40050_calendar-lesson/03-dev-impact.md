# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #40050 bằng `/new-task`. Nguồn: **Journal #136541 — AI LME Fix bug — 2026-09-15** (vòng refix cuối, bản hiện hành). Vòng 1 (#134734) và vòng 2 (#136534) đã bị bản này thay thế — xem bảng mốc ở [01-bug-task.md](01-bug-task.md).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (hệ thống Auto-fixbug LME)` — assignee Redmine: `Ngô Thúy Ngần` |
| Commit / Pull Request | `sns-line @ f1c9a55319` (17 file) — vòng trước: `adad1a4191`, `f2f10e65cf` |
| Branch | `ai_fixbug_40050` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-09-15` |
| Auto-filled | `2026-09-22 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn journal #136541:

Các endpoint ajax của màn quản lý lịch đặt chỗ Lesson trả HTTP code sai ý nghĩa: lỗi nghiệp vụ (không tìm thấy lịch/khoá học/đơn đặt chỗ, sai mã xác thực xoá lịch, vượt hạn mức gói, cổng thanh toán từ chối hoàn tiền) đang trả 200 (nghĩa là thành công) hoặc 500 (nghĩa là server sập), khiến giám sát báo động nhầm và phía màn hình không phân biệt được. Ngoài ra hầu hết endpoint nhận dữ liệu thẳng từ request mà không kiểm tra bắt buộc, thiếu tham số sẽ chạy truy vấn theo null rồi vẫn báo thành công, hoặc đi tới tận tầng service mới gây lỗi hệ thống thật.

## 2. Cách fix

> Nguyên văn journal #136541 — gồm 4 phần, làm theo yêu cầu bổ sung của human trong quá trình review.

**(1) Chuẩn hoá HTTP code + kiểm tra dữ liệu bắt buộc** cho toàn bộ endpoint ajax của lịch Lesson trên màn quản trị, theo đúng cách đã áp dụng cho lịch Salon ở #39566. Thêm hàm dùng chung trả 422 kèm danh sách lỗi và gắn kiểm tra bắt buộc cho 24 endpoint. Lỗi nghiệp vụ đổi từ 200 sang 400, không tìm thấy bản ghi sang 404, chỉ giữ 500 cho lỗi hệ thống thật. Bổ sung 5 chỗ trước đây bỏ qua kết quả thất bại của service mà vẫn báo thành công. Phía màn hình thêm tệp xử lý lỗi dùng chung và gắn vào 78 nhánh lỗi để người dùng vẫn thấy lý do khi mã đổi từ 200 sang 4xx. Sau sửa, số nhánh lỗi còn trả 200 là 0.

**(2) Toàn bộ thông báo lỗi hiển thị cho người dùng chuyển sang tiếng Nhật**: khai bảng nhãn tiếng Nhật cho 27 tên trường nên thông báo 422 đọc trọn tiếng Nhật thay vì nửa Nhật nửa tên trường thô; các thông báo không tìm thấy bản ghi dịch theo lối viết sẵn có trong mã nguồn; các nhánh lỗi hệ thống trước đây ném thẳng nội dung ngoại lệ ra màn hình nay trả một câu tiếng Nhật chung và ghi chi tiết vào log (bổ sung ghi log ở 8 chỗ vốn không có); một nhánh trả thông báo rỗng khiến màn hình bật hộp thoại trắng nay có nội dung.

**(3) Ràng buộc MỌI truy vấn theo bot đang đăng nhập** cho màn quản trị: rà 96 điểm truy vấn trong controller và các service chỉ phục vụ màn quản trị. Bảng có sẵn cột định danh bot thì ràng buộc thẳng; bảng không có (khoá học, khung giờ tiếp nhận, đơn đặt chỗ, lịch sử thao tác đơn, bạn bè) thì chặn qua truy vấn con lần lên lịch của bot hoặc qua bảng trung gian. Vá các lỗ cho phép thao tác chéo tài khoản chỉ bằng cách đổi id gửi lên: xem chi tiết lịch, xoá bước nhắc lịch, tạo khoá học vào lịch người khác, và HOÀN TIỀN đơn đặt chỗ của tài khoản khác. CỐ Ý không đụng service/repository dùng chung với màn LIFF của khách, API và job nền, vì hàm lấy bot đọc từ phiên đăng nhập, ở các luồng đó sẽ rỗng và làm hỏng luồng đặt lịch thật của khách.

**(4) Sửa 2 lỗi do chính phần (3) gây ra**, được review độc lập phát hiện: thao tác xoá lịch và xoá khoá học đang xoá bản ghi cha TRƯỚC, trong khi các câu xoá dữ liệu con lại ràng buộc qua truy vấn con lần lên chính bản ghi cha đó. Hai bảng này xoá cứng nên sau khi cha biến mất thì truy vấn con rỗng và cả chuỗi xoá dây chuyền không làm gì, để lại dữ liệu con mồ côi. Đã chuyển việc xoá bản ghi cha xuống CUỐI chuỗi ở cả hai chỗ, kèm chú thích cảnh báo. Ràng buộc nốt cụm endpoint khoá học: 8 chỗ tra khoá học theo id thô nay đi qua hàm tra có ràng buộc bot.

### Ghi chú thêm của Dev ở mục VERIFY (nguyên văn)

- Mức verify: **lint**. `php -l` trên 5 file PHP đã sửa: không có lỗi cú pháp; `node --check` trên 6 file JS (5 file sửa + 1 file mới): không có lỗi cú pháp; Script quét lại toàn bộ 113 nhánh `response()->json` của controller: số nhánh lỗi (`success=false` / `status=false`) còn trả HTTP 200 = **0** (trước sửa là 24); **Không chạy được PHPUnit** cho thay đổi này (fix nằm ở tầng controller và cần request/session).
- Đối chiếu từng endpoint với payload thực tế phía màn hình (`public/js/calendar_management/*.js` và `course_list.blade.php`) trước khi khai required, để không chặn nhầm luồng đang chạy.
- `type_remind` **CỐ Ý không** khai required ở `saveSettingSendMessageEventStep` vì bước nhắc lịch cũ trong DB có thể để trống cột này (`getListStepRemind` đọc bằng `?? 1`).
- Đã kiểm `CalendarCourseReceptionService::update` trả `false` khi không thấy khung giờ và trả `null` khi thành công, nên guard dùng so sánh `=== false`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn mục 3 của journal #136541.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarManagementController::validateInput` — `app/Http/Controllers/Basic/CalendarManagementController.php` | **Hàm mới**, trả 422 kèm danh sách lỗi + bảng nhãn tiếng Nhật cho 27 tên trường | Kiểm tra dữ liệu bắt buộc dùng chung cho 24 endpoint |
| 2 | `storeCalendar` / `editCalendar` / `saveSort` / `savePolicyCalendar` / `saveCalendarInfo` (cùng file) | Chuẩn hoá HTTP code + validate required + ràng buộc bot | Nhóm tạo / sửa / sắp xếp / chính sách / thông tin lịch |
| 3 | `sendMailCodeAuthDeleteCalendar` / `checkAuthorDeleteCalendar` / `deleteCalendar` (cùng file) | Như trên; `deleteCalendar` còn **đổi thứ tự chuỗi xoá** (bản ghi cha xoá sau cùng) | Luồng xoá lịch bằng mã xác thực qua mail |
| 4 | `saveSettingNotifyFull` / `getHistorySettingNotifyFullSlot` / `saveCreateSettingRemind` (cùng file) | Chuẩn hoá HTTP code + validate required + ràng buộc bot | Thông báo đầy chỗ + lịch sử + tạo cài đặt nhắc lịch |
| 5 | `getListStepRemind` / `deleteEventStep` / `getListCourseByCalendar` / `getDetailEventStep` (cùng file) | Như trên; `deleteEventStep` là 1 trong 4 lỗ thao tác chéo tài khoản đã vá | Bước nhắc lịch + list khoá học theo lịch |
| 6 | `deleteItemActionEventStep` / `deleteItemActionCalendar` / `saveSettingSendMessageEventStep` (cùng file) | `action_detail_id` / `action_id` đổi sang **nullable / integer** (màn hình cố ý gọi với id rỗng); `type_remind` cố ý không required | Xoá item action trong modal khi chưa lưu DB |
| 7 | `addNewReception` / `updateReception` / `deleteReception` / `deleteListReception` (cùng file) | Chuẩn hoá HTTP code + validate required + ràng buộc bot qua truy vấn con lần lên lịch | Khung giờ tiếp nhận 受付枠 |
| 8 | `addNewBooking` / `changeStatusBooking` / `deleteBooking` / `saveInfoFormBooking` (cùng file) | Như trên; `saveInfoFormBooking` chạm friend info | Đơn đặt chỗ 予約 |
| 9 | `createNewSettingForm` / `updateSettingForm` / `deleteSettingForm` / `sortSettingForm` / `saveSettingMessage` (cùng file) | Như trên | Câu hỏi biểu mẫu khi đặt chỗ + tin nhắn cài đặt |
| 10 | `createCourse` / `updateCourse` / `deleteCalendarCourse` / `deleteImageCalendarCourse` / `updateCalendarCourseOrder` (cùng file) | Như trên; `deleteCalendarCourse` **đổi thứ tự chuỗi xoá**; 8 chỗ tra khoá học theo id thô đi qua hàm tra có ràng buộc bot | Khoá học コース |
| 11 | `updateBookingPageDisplay` / `initDataActionCalendarCourseSetting` / `deleteItemAction` / `settingBookingDisplay` (cùng file) | Như trên | Hiển thị trang đặt chỗ + action của khoá học |
| 12 | `orderRefund` / `importCsv` (cùng file) | Như trên; `orderRefund` là lỗ thao tác chéo tài khoản **nghiêm trọng** đã vá | Hoàn tiền + import CSV |
| 13 | `CalendarCourseService` — `app/Services/CalendarManagement/CalendarCourseService.php` | **12 nhánh trả về** khai thêm `httpCode` | Để controller trả đúng mã 400/404 |
| 14 | `CalendarManagementService::updateBookingSettingDisplay` — `app/Services/CalendarManagement/CalendarManagementService.php` | Chuẩn hoá kết quả trả về | Cài đặt hiển thị trang đặt chỗ |
| 15 | `CreateCalendarCourse::rules` — `app/Http/Requests/CreateCalendarCourse.php` | Cập nhật rule validate | Form request tạo khoá học |
| 16 | `window.showLessonAjaxError` — `public/js/calendar_management/ajax-error.js` | **Hàm mới**, gắn vào 78 nhánh lỗi phía màn hình | Hiển thị lý do lỗi khi mã đổi từ 200 sang 4xx |

> ⚠️ **Dev CỐ Ý không đụng** service / repository dùng chung với **màn LIFF của khách · API · job nền** — hàm lấy bot đọc từ phiên đăng nhập nên ở các luồng đó sẽ rỗng và làm hỏng luồng đặt lịch thật của khách.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev kê theo **file thay đổi** (17 file). Gom nhóm thành `F1..F8` để map coverage.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `validateInput` + 24 endpoint ajax khai required | `app/Http/Controllers/Basic/CalendarManagementController.php` | Direct | Thiếu tham số → 422 kèm nhãn tiếng Nhật; trước đây chạy query theo null vẫn báo thành công |
| F2 | 113 nhánh `response()->json` của controller — lỗi nghiệp vụ 400 · không tìm thấy 404 · sai input 422 · chỉ còn 500 cho lỗi hệ thống thật | cùng file F1 | Direct | Trước sửa 24 nhánh lỗi trả HTTP 200, sau sửa còn 0 |
| F3 | 96 điểm truy vấn ràng buộc theo bot đang đăng nhập + 4 hàm dựng truy vấn con dùng chung | cùng file F1 + `CalendarCourseService.php` · `CalendarManagementService.php` | Direct | Vá 4 lỗ thao tác chéo tài khoản: xem chi tiết lịch · xoá bước nhắc lịch · tạo khoá học vào lịch người khác · **hoàn tiền đơn của tài khoản khác** |
| F4 | Thứ tự chuỗi xoá dây chuyền của `deleteCalendar` + `deleteCalendarCourse` (bản ghi cha xoá SAU CÙNG) | cùng file F1 | Direct | Sửa lỗi do chính F3 gây ra ở commit `adad1a4191` |
| F5 | `CalendarCourseService` — 12 nhánh trả về khai thêm `httpCode`; `CalendarManagementService::updateBookingSettingDisplay`; `CreateCalendarCourse::rules` | `app/Services/CalendarManagement/CalendarCourseService.php` · `CalendarManagementService.php` · `app/Http/Requests/CreateCalendarCourse.php` | Direct | Tầng service / form request |
| F6 | `window.showLessonAjaxError` (hàm mới) gắn vào 78 nhánh lỗi phía JS | `public/js/calendar_management/ajax-error.js` + `calendar_detail.js` · `create_course.js` · `edit_course.js` · `index.js` · `setting-payment.js` | Direct | Guard đọc `error.responseJSON.errors` ở nhánh tạo / sửa khoá học (thân 400 không có khoá `errors` → TypeError) |
| F7 | Nhúng file xử lý lỗi dùng chung vào 8 blade | `resources/views/basic/calendar_management/*.blade.php` (course_create · create · detail · index · tabs/course/course_list · tabs/course/edit_course) + `resources/views/basic/setting.blade.php` | Direct | Giữ nguyên cách gọi số hiệu phiên bản sẵn có |
| F8 | Thông báo lỗi hiển thị chuyển sang tiếng Nhật — bảng nhãn 27 tên trường, thông báo không tìm thấy bản ghi, câu lỗi hệ thống chung + ghi log ở 8 chỗ vốn không có | cùng file F1 | Direct | Tham số cho phép đè nhãn khi cùng tên trường mang nghĩa khác (`id` là lịch / câu hỏi / đơn đặt chỗ) |

> ⚠️ Vòng cuối (`f1c9a55319`) **không còn** sửa `config/sns-line.php` — bỏ bump static asset version theo yêu cầu human. (Mục 4.3 của vòng 1 / vòng 2 có kê mục "Static asset version"; bản hiện hành đã gỡ.)

### 4.2. List data bị update khi fix bug

> Nguyên văn mục 4.2 journal #136541.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — (không bảng / cột nào bị thêm-sửa-xoá) | — | Không thêm/sửa/xoá cấu trúc bảng, **không chạy migration** |
| D2 | **Phạm vi dữ liệu** mà mọi câu truy vấn của màn quản trị đụng tới | READ / UPDATE / DELETE (đổi scope) | Mọi câu nay chỉ còn thấy dữ liệu của **bot đang đăng nhập**. Thao tác gửi id của bot khác trước đây chạy được thì nay trả về **không tìm thấy** — đây là chủ đích |
| D3 | Chuỗi xoá dây chuyền khi **xoá lịch** / **xoá khoá học** (khoá học · 受付枠 · đơn đặt chỗ · lịch sử thao tác đơn · cài đặt của lịch) | DELETE | Bản ghi cha xoá **sau cùng** để dữ liệu con vẫn được dọn đúng như trước |
| D4 | ⚠️ **Cảnh báo cho QA** — dữ liệu con mồ côi từ bản dựng `adad1a4191` (push 2026-09-15) | (cần rà tay) | Nếu đã thử xoá lịch / xoá khoá học trên bản đó thì khoá học / 受付枠 / đơn đặt chỗ / cài đặt của lịch đã xoá **có thể còn nằm lại trong DB** |
| D5 | Log lỗi hệ thống — bổ sung ghi log ở **8 chỗ** vốn không có | CREATE (log) | Thay cho việc ném thẳng nội dung ngoại lệ ra màn hình |

**Mục 5 — RECOVER DATA (nguyên văn):** ⚠ **CÓ** — Không cần recover cho phần chuẩn hoá HTTP code / thông báo tiếng Nhật / ràng buộc theo bot. CHỈ cần rà nếu đã thao tác **XOÁ lịch hoặc XOÁ khoá học** trên bản dựng từ commit `adad1a4191`; phạm vi: các lịch / khoá học bị xoá trong khoảng bản dựng `adad1a4191` (push 2026-09-15) → khi bản sửa `f1c9a55319` lên môi trường test.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn mục 4.3 journal #136541.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Lesson / Calendar Booking (FA-019)** — toàn bộ màn quản trị lịch bài học: tạo/sửa/xoá lịch, khoá học, khung giờ tiếp nhận (受付枠), đơn đặt chỗ, nhắc lịch, câu hỏi biểu mẫu, hoàn tiền, nhập/xuất CSV | F1, F2, F3, F4, F5, F6, F7, F8, D2, D3 | **High** |
| T2 | **Friend Information (FA-008)** — lưu thông tin bạn bè khi lưu biểu mẫu của đơn đặt chỗ (các câu đọc/ghi nay ràng buộc theo bot đang đăng nhập) | F3, D2 | **High** |
| T3 | **Remind / Step Message (FA-019)** — bước nhắc lịch của lịch bài học: tạo, sửa, xoá, sinh lịch gửi | F1, F2, F3, D3 | **High** |
| T4 | **Luồng khách LINE đặt lịch (LIFF) · API · job nền** — Dev **cố ý không** đụng service / repository dùng chung | F3 (loại trừ) | **Medium** — phải verify không hỏng: hàm lấy bot đọc từ session, ở các luồng này sẽ rỗng |

---

## Rủi ro / lưu ý khi test (Dev tự nêu — nguyên văn)

- Đổi mã trả về từ 200 sang 4xx là **thay đổi hợp đồng với màn hình**: mọi lời gọi trước đây rơi vào nhánh thành công nay rơi vào nhánh lỗi. Đã rà và gắn xử lý lỗi cho các nhánh trong thư mục màn Lesson, và đã kiểm tra không có nơi nào ngoài thư mục này gọi các endpoint đó; tuy vậy **QA nên bấm lại toàn màn** để chắc chắn không còn thao tác nào im lặng.
- Thân phản hồi 4xx của lỗi nghiệp vụ **không kèm danh sách lỗi chi tiết** (chỉ phản hồi 422 mới có). Đã rà toàn bộ mã màn Lesson: hai chỗ đọc trực tiếp đều đã được bọc kiểm tra. Nếu sau này thêm nhánh lỗi mới thì phải giữ đúng khuôn này.
- Việc thêm kiểm tra bắt buộc đầu vào **có thể chặn nhầm luồng thật** nếu khai sai so với dữ liệu màn hình thực sự gửi lên — đã xảy ra ở ba endpoint xoá item action và đã sửa ở vòng này. Các endpoint còn lại đã được đối chiếu với mã màn hình, nhưng đây là điểm QA nên tập trung: **thử các thao tác trên bản ghi cũ và trên item vừa thêm chưa lưu**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
