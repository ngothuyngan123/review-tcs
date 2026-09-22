# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **CẢNH BÁO NGUỒN — ticket có 2 báo cáo AI auto-fixbug, bản sau ROLLBACK bản trước.**
>
> | Journal | Commit | Nội dung | Trạng thái |
> |---|---|---|---|
> | #135579 (2026-09-10) | `182f45844f` | Tối ưu số truy vấn + dedupe `listDates` + báo lỗi khi nạp thất bại — sửa **3 file** (2 PHP + 1 JS) | ❌ **ĐÃ ROLLBACK hoàn toàn khỏi branch** |
> | #135581 (2026-09-10) | `c9889e70a1` | Bỏ toàn bộ 4 lời gọi ajax đồng bộ (`async: false`) — sửa **1 file JS duy nhất** | ✅ **HIỆU LỰC — file này bám theo bản này** |
>
> File này chép theo **Journal #135581**. Không viết TC theo bản #135579 (các thay đổi PHP: tối ưu truy vấn, dedupe `listDates`, thông báo lỗi bằng `alert()` — **không còn tồn tại trên branch**).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: `Đỗ Quyên` |
| Commit / Pull Request | `c9889e70a1` (repo `sns-line`) — Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=40378 |
| Branch | `ai_fixbug_40378` (nhánh gốc `release_step_20260827`) — đã push lên origin |
| Ngày submit đánh giá | `2026-09-10` (custom field Redmine: Commit Date = 2026-09-10) |
| Auto-filled | `2026-09-10 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn đặt lịch salon nạp bảng giờ trống bằng **synchronous XHR** (`booking.js`, hàm `getListTimeBooking`: `async: false`). Request này vốn chạy lâu vì server dò **tối đa 4 tuần trong một lần gọi**, mà **Safari/WKWebView (trình duyệt trong ứng dụng LINE trên iOS) chủ động huỷ sync XHR** khi chạy quá lâu hoặc khi tab bị đưa xuống nền, và theo chuẩn thì sync XHR cũng **không đặt được timeout**.

Request bị huỷ ⇒ nhánh `error` chỉ tắt vòng quay chờ, **lịch giữ nguyên rỗng** nên hội viên hiểu là hết khung đặt.

Vì phụ thuộc thời điểm / tải nên hiện tượng **chỉ xảy ra trên iOS** và mang tính **ngẫu nhiên** — khớp đúng mô tả 「lúc được lúc không」, tải lại trang thì khi có khi không.

## 2. Cách fix

Bỏ **toàn bộ 4 lời gọi ajax đồng bộ** (`async: false`) trong màn đặt lịch salon phía hội viên (`public/js/calendar_salon/booking.js`):

1. Nạp **bảng giờ trống** (xem tuần) — `getListTimeBooking`
2. Nạp **ngày trống** (xem tháng) — `initDataBooking`
3. Nạp **danh sách nhân viên** — `getListStaffByCalendar`
4. Nạp **danh sách khoá học** — `getListCourseByCalendar`

→ để trình duyệt không huỷ request giữa chừng nữa.

Riêng luồng **「Đặt lại」 (`copyBooking`)** trước đây đọc kết quả khoá học **ngay dòng sau** lời gọi, nên phần sau được **tách thành hàm `copyBookingStepTime`** và gọi trong callback khi request xong (dùng `.always()` để giữ đúng hành vi cũ khi request lỗi).

**KHÔNG** đổi tham số gửi lên, **KHÔNG** đổi xử lý kết quả, **KHÔNG** đụng bất kỳ điều kiện tính khung trống / giới hạn đặt nào phía server — **lần này không sửa file PHP nào**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `getListTimeBooking` — `public/js/calendar_salon/booking.js` | Bỏ `async: false` | Nạp bảng giờ trống, xem tuần — **đã rà 8 nơi gọi**, không nơi nào đọc kết quả ngay sau lời gọi |
| 2 | `initDataBooking` — `public/js/calendar_salon/booking.js` | Bỏ `async: false` | Nạp ngày trống, xem tháng — **đã rà 8 nơi gọi** |
| 3 | `getListStaffByCalendar` — `public/js/calendar_salon/booking.js` | Bỏ `async: false` | Danh sách nhân viên — **đã rà 3 nơi gọi** |
| 4 | `getListCourseByCalendar` — `public/js/calendar_salon/booking.js` | Bỏ `async: false` + trả về `jqXHR` | Danh sách khoá học — **1 nơi gọi (`copyBooking`), là nơi DUY NHẤT đọc kết quả ngay sau lời gọi** |
| 5 | `copyBooking` / `copyBookingStepTime` — `public/js/calendar_salon/booking.js` | **Tách hàm**: phần sau lời gọi chuyển sang `copyBookingStepTime`, gọi trong `.always()` | Luồng 「Đặt lại」 từ lịch sử đặt — chỗ **duy nhất đổi cấu trúc code** |
| 6 | `getListDay` — `public/js/calendar_salon/booking.js` | Không đổi | Đối chiếu với `listDay` do server trả về — server trả đủ 7 ngày của tuần, đúng bằng danh sách `getListDay` tự dựng |
| 7 | `Mobile\CalendarSalonController::handleShowListBooking` — `app/Http/Controllers/Mobile/CalendarSalonController.php` | Không đổi | Xác nhận `listDay` = đủ các ngày từ `startDate` đến `endDate` |
| 8 | `$.ajaxSetup statusCode` trong `getDataFriendInfo` — `public/js/calendar_salon/booking.js` | Không đổi | Handler global 400/401/403/404/500/502 redirect `/lme/timeout`, áp cho các request nay chạy bất đồng bộ **y như trước** |
| 9 | `public/plugins/loadingoverlay/loadingoverlay.min.js` (v1.5.3) | Không đổi | Cơ chế **đếm** show/hide qua data `LoadingOverlayCount` → vòng quay chờ không bị tắt sớm |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `getListTimeBooking` — nạp bảng giờ trống (xem tuần) | `public/js/calendar_salon/booking.js` | **Direct** | Bỏ `async: false`. Là hàm gây ra bug gốc. 8 nơi gọi |
| F2 | `initDataBooking` — nạp ngày trống (xem tháng) | `public/js/calendar_salon/booking.js` | **Direct** | Bỏ `async: false`. 8 nơi gọi. Server có thể tính tới **3 tháng** trong 1 request |
| F3 | `getListStaffByCalendar` — nạp danh sách nhân viên | `public/js/calendar_salon/booking.js` | **Direct** | Bỏ `async: false`. 3 nơi gọi (bước chọn nhân viên) |
| F4 | `getListCourseByCalendar` — nạp danh sách khoá học | `public/js/calendar_salon/booking.js` | **Direct** | Bỏ `async: false` + trả về `jqXHR` để nơi gọi chờ bằng `.always()` |
| F5 | `copyBooking` + hàm mới `copyBookingStepTime` — luồng 「Đặt lại」 từ lịch sử đặt | `public/js/calendar_salon/booking.js` | **Direct — đổi cấu trúc code** | ★ Chỗ **duy nhất** thân hàm bị tách. Rủi ro regression cao nhất |
| F6 | `$.ajaxSetup statusCode` (handler global 400/401/403/404/500/502 → redirect `/lme/timeout`) | `public/js/calendar_salon/booking.js` | Indirect | Không sửa, nhưng nay áp cho request **bất đồng bộ**. ⚠️ Request bị **huỷ** có `status = 0` → **KHÔNG** rơi vào handler này, vẫn im lặng |
| F7 | `LoadingOverlay` (vòng quay chờ) — bộ đếm `LoadingOverlayCount` | `public/plugins/loadingoverlay/loadingoverlay.min.js` | Indirect | Không sửa. Thứ tự show/hide đổi do chạy bất đồng bộ → cần verify overlay không tắt sớm / không kẹt |
| F8 | `getListDay` — dựng danh sách ngày phía FE | `public/js/calendar_salon/booking.js` | Indirect | Không sửa. Chỗ duy nhất gọi `getListTimeBooking()` **trước** `getListDay()` — Dev khẳng định kết quả `list_day` y hệt |
| F9 | Toàn bộ endpoint / logic tính khung trống phía server | `app/Http/Controllers/Mobile/CalendarSalonController.php`, `app/Services/CalendarSalon/*` | **KHÔNG đổi** | Lần fix này **không sửa file PHP nào**. Tham số gửi lên và xử lý kết quả giữ nguyên |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** | — | Chỉ sửa JS phía trình duyệt: **không đổi schema, không ghi/sửa dữ liệu, không đổi API**. Không cần recover data. |

> ⚠️ Tuy không có data impact, **có impact ở tầng phân phối file tĩnh**: Dev **chưa bump `config/sns-line.php`** theo quy ước → client đang cache `booking.js` **bản cũ** có thể chưa nhận file mới. Cần đội release xử lý **cache-bust** khi lên bản, nếu không kết quả test sẽ sai.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Đặt lịch salon / phỏng vấn (FA-020) — bảng giờ trống, xem tuần** (LIFF phía hội viên) | F1, F8 | **High** — là ca bug gốc; đổi từ sync sang async |
| T2 | **Đặt lịch salon (FA-020) — lịch ngày trống, xem tháng** | F2 | **High** — server có thể tính tới 3 tháng/request, dễ lộ race khi chuyển tháng nhanh |
| T3 | **Đặt lịch salon (FA-020) — bước chọn nhân viên** | F3 | Medium |
| T4 | **Đặt lịch salon (FA-020) — bước chọn khoá học** | F4 | Medium |
| T5 | **Đặt lịch salon (FA-020) — luồng 「Đặt lại」 (`copyBooking`) từ lịch sử đặt** | F4, F5 | **High** — chỗ duy nhất đổi cấu trúc code; phải test cả case khoá học **đã bị xoá** (vẫn phải hiện 「コースが存在していません」) |
| T6 | **Vòng quay chờ (loading overlay)** trên toàn màn đặt lịch | F7 | Medium — thứ tự show/hide đổi; kiểm tra không tắt sớm, không kẹt vĩnh viễn |
| T7 | **Xử lý lỗi / timeout phiên** trên màn đặt lịch (redirect `/lme/timeout`) | F6 | Medium — handler global nay áp cho request async; request bị huỷ (`status = 0`) vẫn im lặng |

---

## Rủi ro / lưu ý khi test (Dev tự nêu — Journal #135581)

- **Chưa test được trên thiết bị thật** trong container → **QA phải mở LIFF trên iPhone** (đây là ca bug gốc): vào màn đặt lịch salon **nhiều nhân viên**, tải lại nhiều lần, chuyển tuần/tháng qua lại, chọn nhân viên, chọn khoá học.
- **PHẢI test kỹ luồng 「Đặt lại」 (`copyBooking`)** vì đây là chỗ duy nhất đổi cấu trúc code: đặt lại một booking bình thường, **và** đặt lại booking có **khoá học đã bị xoá** (phải vẫn hiện thông báo 「コースが存在していません」).
- **Bấm nhanh liên tiếp prev/next tuần hoặc tháng** nay có thể để **2 request chồng nhau**, response về sau đè lên response trước (trước đây sync XHR nên tuần tự). Dev cho rằng vòng quay chờ che toàn màn nên khó bấm được; **nếu QA tái hiện được thì cần bổ sung huỷ request cũ trước khi gửi request mới**.
- **Request bị trình duyệt huỷ vẫn IM LẶNG**: `status = 0` nên không rơi vào handler `$.ajaxSetup` (redirect `/lme/timeout`), nhánh `error` chỉ tắt vòng quay chờ và để lịch rỗng. Fix này làm request không bị huỷ nữa, **nhưng chưa có** timeout + retry + banner báo lỗi (chưa làm, chờ quyết định).
- **Phần tính toán phía server không đổi**: màn hình **vẫn nặng như cũ** (server dò tối đa 4 tuần cho xem tuần, tới 3 tháng cho xem tháng). Nếu sau bản này khách vẫn báo 「màn hình đặt lịch hoạt động nặng」 thì cần **ticket tối ưu riêng**.
- **Không bump `config/sns-line.php`** theo quy ước → client đang cache bản `booking.js` cũ có thể chưa nhận file mới — nhờ đội release xử lý **cache-bust** khi lên bản.

## Bằng chứng Dev đưa ra (Journal #135581, mục 6 VERIFY)

- Mức verify: **lint** (không có test tự động, không chạy được trên trình duyệt thật).
- `node --check public/js/calendar_salon/booking.js`: OK
- `grep -n 'async: false' public/js/calendar_salon/booking.js`: **0 kết quả** (trước fix có **4**)
- `grep -nE 'ajaxSetup|XMLHttpRequest|\$\.(get|post|getJSON)\('` — không còn dạng gọi đồng bộ nào khác trong file; các JS khác của màn (`common.js`, `booking_news/validate.js`, `validate/message_error_univapay.js`) cũng không có sync XHR.
- `git diff --stat release_step_20260827...ai_fixbug_40378`: **1 file, 28 thêm / 10 xoá** (chỉ `public/js/calendar_salon/booking.js`).
- Không sửa file PHP nào → không cần `php -l`.
- **Không kiểm chứng được trên trình duyệt thật** trong container (không có Android SDK / iOS toolchain; dev DB `host.docker.internal:3306` Connection refused) → **cần QA test tay trên iPhone**.
- Rà từng nơi gọi 4 hàm: chỉ có **đúng 1 chỗ** phụ thuộc kết quả đồng bộ — `copyBooking` đọc `this.index_course_selected` ngay dòng sau `getListCourseByCalendar`.
- Dùng `.always()` (không phải `.done()`) để giữ đúng hành vi cũ: khi request lỗi, sync XHR trước đây vẫn để `index_course_selected` giữ giá trị cũ và luồng chạy tiếp.
- jQuery 3.2.1: `success`/`error`/`complete` vẫn là option hợp lệ của `$.ajax` và được đăng ký **TRƯỚC** `.always()` của nơi gọi → trong callback thì `self.courses` / `self.index_course_selected` đã được gán.
- `self.staffs` / `self.courses` / `self.events` chỉ được đọc để render qua Vue, không nơi nào đọc ngay sau lời gọi (đã grep từng biến).
- `fullcalendar` luôn tồn tại khi response về: `initializeFullCalendar()` chạy đồng bộ ngay trước `initDataBooking()` trong cùng `$nextTick`.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
