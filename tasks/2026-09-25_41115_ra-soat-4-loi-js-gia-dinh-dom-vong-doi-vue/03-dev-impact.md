# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41115 — nguồn: **Journal #137393** (báo cáo AI auto-fixbug, bản mới nhất sau tự review v1). Description Redmine không có Section "Đánh giá ảnh hưởng" riêng.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `0150dedda4` (repo sns-line, commit tự review) · trước đó `3d44770f8a` (Journal #137378). Không có link PR. |
| Branch | `ai_fixbug_41115` (nhánh gốc `release_step_20260827`) |
| Ngày submit đánh giá | 2026-09-21 |
| Auto-filled | 2026-09-25 by /new-task |

⚠️ Journal #137393 tự mâu thuẫn: mục 2 ghi "Commit thêm 0150dedda4 — CHƯA push lên origin, cần push lại", nhưng dòng BRANCH ghi "[đã push]". Mục 4.3 ghi rõ phần bill-tool "CHỈ đúng sau commit 0150dedda4". → Xác nhận với Dev commit này đã lên origin / đã deploy env test chưa.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn quản lý lịch salon gắn bộ lắng nghe cuộn và khởi tạo lại bộ chọn giờ trong hook cập nhật của Vue, nhưng vùng cuộn chỉ được vẽ ở chế độ hiển thị theo ngày. Chuyển sang tuần/tháng/tuỳ chọn thì vùng cuộn bị gỡ khỏi trang, hook vẫn truy cập trực tiếp nên báo lỗi mỗi lần trang vẽ lại; vì hook này thuộc thành phần bao cả trang chi tiết salon nên gần như mọi thao tác đều kích hoạt. Hook cập nhật còn gắn lại sự kiện đổi giờ cho các ô nhập giờ ở mọi lần vẽ mà không gỡ bản cũ, nên số trình xử lý trên cùng một ô dồn lên nhau không giới hạn.

> ℹ️ Mục 1 Dev chỉ mô tả nguyên nhân của **mục 3** ticket (salon). Nguyên nhân mục 1 / 2 / 4 nằm ở description Redmine (file 01) và trong mục 2 bên dưới.

## 2. Cách fix

Refix vòng 2 theo AI review — bổ sung 3 mục của ticket gộp còn thiếu ở lượt trước (lượt 1 mới chỉ làm mục 3):

(1) Màn Đăng ký-nâng cấp gói (`public/js/admin/bill_tool/index.js`): hook cập nhật lấy khối điều khoản rồi gắn thẳng bộ lắng nghe cuộn — nay kiểm tra khối có tồn tại mới dùng (tổ hợp hợp đồng cũ + có chiến dịch thì khối này không được vẽ nên trước đây lỗi mỗi lần vẽ lại), đồng thời tách trình xử lý cuộn thành một phương thức có tên rồi gỡ bản cũ trước khi gắn lại, nên mỗi lần vẽ lại không còn nhân thêm trình xử lý (trước đây cuộn một lần chạy N lần, mỗi lần đều đánh dấu đã đọc điều khoản). Trình xử lý đọc phần tử qua sự kiện, giữ nguyên ngưỡng cuộn và hành vi đánh dấu đã đọc.

(2) Bộ xử lý đổi kích thước cửa sổ ở CẢ hai màn quản lý lịch (`public/js/calendar_management/calendar_detail.js` và `public/js/calendar_salon/calendar_detail.js`): thêm kiểm tra bảng danh sách khoá học theo ngày có tồn tại rồi mới tính lại bề rộng — bảng này chỉ vẽ ở chế độ hiển thị theo ngày, trước đây đang xem tuần/tháng mà kéo đổi kích thước cửa sổ là lỗi liên tục (sự kiện đổi kích thước bắn liên tục khi kéo). Giữ nguyên hằng số trừ bề rộng của từng màn (230 cho Lesson, 200 cho Salon).

(3) Màn đặt lịch bài học (`public/js/booking_news/booking.js`): nút Quay lại ở bước 3 kiểm tra đối tượng lịch bằng cách sai (danh sách khoá của đối tượng rỗng vẫn được coi là hợp lệ) nên ở tab Tuần — vốn là tab mặc định và là lúc đối tượng lịch chưa được tạo — bấm Quay lại sẽ lỗi vì gọi hàm vẽ không tồn tại; nay kiểm tra thật sự có đối tượng lịch và có nội dung, theo đúng mẫu đã chốt ở #41090. Rà soát thêm theo yêu cầu review: chỗ dùng ở hàm tải dữ liệu đã có sẵn kiểm tra đúng, còn hai chỗ ở nút lùi/tiến tháng nằm trong nhánh chỉ chạy ở chế độ Tháng nên an toàn — không sửa. Tổng cộng branch hiện có 4 commit, mỗi mục của ticket một commit.

[Tự review v1 — 2026-09-21] Phát hiện mục 1 của ticket mới vá được một nửa: ngoài hook cập nhật, chính file màn Đăng ký-nâng cấp gói (`public/js/admin/bill_tool/index.js`) còn một chỗ thứ hai ở khối jQuery ready lấy khối điều khoản rồi gắn bộ lắng nghe cuộn mà không kiểm tra tồn tại — mở trang cho bot có chiến dịch (hợp đồng cũ + có chiến dịch) là lỗi ngay lúc tải trang, đúng triệu chứng mục 1 mô tả; ở luồng bình thường thì khối này gắn thêm một trình xử lý ẩn danh thứ hai nên cuộn một lần vẫn chạy hai lần. Đã sửa: kiểm tra khối có tồn tại mới dùng, và dùng chung đúng một trình xử lý có tên với hook cập nhật (gỡ rồi gắn lại) nên toàn trang chỉ còn một trình xử lý cuộn. Giữ nguyên ngưỡng cuộn và hành vi đánh dấu đã đọc. KHÔNG bỏ hẳn khối jQuery ready vì hook cập nhật chỉ chạy khi trang vẽ LẠI, bỏ đi thì lần tải trang đầu sẽ không đánh dấu được đã đọc điều khoản. Commit thêm 0150dedda4 — CHƯA push lên origin, cần push lại.

**Verify (mục 6 báo cáo Dev):** mức `lint` — `node -c` 4 file JS OK; `git diff --stat origin/release_step_20260827...ai_fixbug_41115`: 5 files changed, 44 insertions(+), 11 deletions(-). **Không tái hiện bằng trình duyệt** (container không có môi trường chạy giao diện) — kết luận dựa trên đọc mã + đối chiếu blade.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `mixinCalendarManagement.beforeDestroy` (`public/js/calendar_salon/calendar-management.js:270`) | | |
| 2 | `mixinCalendarManagement.mounted` (`calendar-management.js:277`) | | |
| 3 | `mixinCalendarManagement.updated` (`calendar-management.js:339`) | | |
| 4 | `mixinCalendarManagement.methods.initializeTimePickers` (`calendar-management.js:592`) | | |
| 5 | `mixinCalendarManagement.methods.handleScroll` (`calendar-management.js:2564`) | | |
| 6 | `appCalendarSalon` (Vue instance dùng mixin — `public/js/calendar_salon/calendar_detail.js:84`) | | |
| 7 | blade `ref=scrollDiv` (`resources/views/basic/calendar_salon/tabs/calendar_management/calendar_display_day2.blade.php:64`) | | |
| 8 | blade `v-if selectModeDisplay day` (`resources/views/basic/calendar_salon/tabs/calendar_management/index.blade.php:228`) | | |
| 9 | blade ô nhập giờ ca làm (`resources/views/basic/calendar_salon/modal/detail_staff_modal.blade.php:35-49`) | | |
| 10 | plugin timepicker (`public/js/plugins/timepicker/bootstrap-timepicker.js:983` phát sự kiện change, `:1127` chống khởi tạo trùng) | | |

> ℹ️ Danh sách caller Dev ghi **chỉ cho mục 3 (salon)**. Mục 1 (bill-tool) / 2 (resize) / 4 (booking.js) chỉ có phần rà soát nằm trong mục 2 + mục Verify: `booking.js:695` đã có kiểm tra đúng; `:560` / `:589` nằm trong nhánh chế độ month → không sửa; `main-step.blade.php:195/411/664` 3 khối `confirm_term` loại trừ nhau.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `mixinCalendarManagement` — `updated` / `initializeTimePickers` / `handleScroll` (quản lý lịch Salon) | `public/js/calendar_salon/calendar-management.js` | Direct | Mục 3 ticket |
| F2 | bill-tool — hook `updated` + khối jQuery ready gắn listener cuộn `#confirm_term` | `public/js/admin/bill_tool/index.js` | Direct | Mục 1 ticket; tự review thêm chỗ jQuery ready (commit `0150dedda4`) |
| F3 | handler resize cửa sổ — quản lý lịch Lesson | `public/js/calendar_management/calendar_detail.js` | Direct | Mục 2 ticket |
| F4 | handler resize cửa sổ — quản lý lịch Salon | `public/js/calendar_salon/calendar_detail.js` | Direct | Mục 2 ticket |
| F5 | `backBookingStep` — trang đặt lịch bài học phía user | `public/js/booking_news/booking.js` | Direct | Mục 4 ticket |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có — chỉ sửa mã phía trình duyệt, không đổi truy vấn hay dữ liệu lưu trữ | — | Không cần recover data |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — màn quản lý lịch salon: hết lỗi JS khi xem theo tuần/tháng/tuỳ chọn, giữ nguyên cuộn ngang ở chế độ ngày | F1 | `<Dev không ghi>` |
| T2 | Salon Booking (FA-020) — hộp thoại sửa ca làm nhân viên: mỗi ô chọn giờ chỉ còn một trình xử lý sự kiện đổi giờ, ô giờ của dòng ca mới thêm vẫn được khởi tạo | F1 | `<Dev không ghi>` |
| T3 | Salon Booking (FA-020) — đổi kích thước cửa sổ khi đang xem lịch salon theo tuần/tháng: không còn lỗi, bề rộng cột ở chế độ ngày vẫn tính lại như cũ | F4 | `<Dev không ghi>` |
| T4 | Lesson Booking (FA-019) — màn quản lý lịch bài học: đổi kích thước cửa sổ ở chế độ tuần/tháng không còn lỗi | F3 | `<Dev không ghi>` |
| T5 | Lesson Booking (FA-019) — màn đặt lịch bài học phía người dùng: bấm Quay lại từ bước chọn giờ khi đang ở tab Tuần không còn lỗi, chế độ Tháng vẫn vẽ lại lịch như cũ | F5 | `<Dev không ghi>` |
| T6 | Hợp đồng và thanh toán (FA-031) — màn Đăng ký / nâng cấp gói của quản trị: hết lỗi lúc tải trang với bot có chiến dịch (tổ hợp hợp đồng cũ + có chiến dịch không vẽ khối điều khoản), và việc đánh dấu đã đọc điều khoản chỉ chạy đúng một lần mỗi lượt cuộn (trước đây 2 lần ở luồng bình thường). Lưu ý: phần này CHỈ đúng sau commit tự review 0150dedda4 — cần push lại | F2 | `<Dev không ghi>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
