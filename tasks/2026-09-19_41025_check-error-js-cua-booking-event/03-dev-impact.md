# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41025 bởi `/new-task`. Nguồn: 2 journal **AI AUTO-FIXBUG** (không phải Dev người viết). Nội dung chính lấy từ **Journal #137108** (bản mới nhất, 4 file, commit `36501465fa`); **Journal #137091** chỉ ghi "Bổ sung lần 5" (log `collectXhrInfo`) → chép ở cuối mục 2.
>
> ⚠️ 2 journal lệch nhau về trần payload `detail` phía server: #137091 ghi **2000→4000**, #137108 ghi **1000→4000** (bản 1000 vẫn là bản gửi Chatwork). Leader xác nhận lại trên diff.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | sns-line commit `36501465fa` (4 file, journal #137108) · trước đó `98db57da20` (1 file, journal #137091) · `3ac589e748` (mục VERIFY) · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=41025 |
| Branch | `ai_fixbug_41025` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-18 |
| Auto-filled | 2026-09-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Ticket gộp 3 lỗi khác nhau của màn đăng ký sự kiện trên LINE.

(1) TypeError 'this.cardNumber.clear' — hàm xoá trắng ô nhập thẻ được gọi ở MỌI nhánh báo lỗi của đăng ký/đổi lịch, nhưng 3 ô nhập thẻ chỉ được khởi tạo khi sự kiện dùng thanh toán thẻ Stripe. Sự kiện miễn phí hoặc Univapay thì 3 biến còn rỗng nên trình duyệt ném lỗi và nuốt luôn các dòng lệnh phía sau.

(2) MÀN TRẮNG ở nhánh báo lỗi, khách kẹt phải mở lại LINE — cả 2 nhánh lỗi đều có lệnh chuyển về bước nhập thẻ, nhưng bước đó CHỈ được vẽ ra khi sự kiện có thanh toán thẻ (điều kiện hiển thị của khối thanh toán ràng buộc is_auto_bill = 1). Với sự kiện miễn phí, chuyển sang bước đó là ẩn mất màn xác nhận mà không hiện gì thay thế: bấm OK trên thông báo lỗi xong khách chỉ còn thấy ảnh sự kiện, không còn nút nào để sửa hay gửi lại. Hai nhánh có nguồn gốc KHÁC NHAU:
   · Nhánh ĐĂNG KÝ: lệnh chuyển bước nằm TRƯỚC lệnh xoá ô thẻ nên vẫn luôn chạy kể cả khi lỗi (1) còn ném ra ⇒ lỗi này ĐÃ TỒN TẠI TỪ TRƯỚC, không phải do lần sửa này.
   · Nhánh ĐỔI LỊCH: lệnh chuyển bước nằm SAU lệnh xoá ô thẻ, nên trước đây lỗi (1) chặn nó lại, khách vẫn đứng ở màn xác nhận và gửi lại được. Vá xong lỗi (1) là gỡ mất cái 'phanh' đó, lệnh chuyển bước bắt đầu chạy cho mọi loại sự kiện ⇒ đây là HỒI QUY do chính việc sửa lỗi (1) mở khoá. Nặng hơn nhánh đăng ký vì màn xác nhận đổi lịch bị huỷ hẳn khỏi giao diện (không phải chỉ ẩn đi) nên khách buộc phải đóng/mở lại LINE.
   Tình huống kích hoạt phổ biến nhất: khách chọn đúng khung giờ vừa hết chỗ, máy chủ trả về thông báo 予約がいっぱいです。

(3) 'getFriendInfo request failed' (status 0) — KHÔNG phải máy chủ trả lỗi, KHÔNG phải mạng của khách hỏng. status 0 không phải mã lỗi HTTP (HTTP không có mã 0) mà là giá trị trình duyệt dùng khi KHÔNG nhận được dòng trạng thái HTTP nào; đối chiếu mã nguồn jQuery thì giá trị này chỉ sinh ra ở nhánh sự kiện 'error' của request, còn response về đích thì không bao giờ ra 0.
   ĐÃ CHỨNG MINH được: (a) ở lần khách mở LINE bị lỗi, request lấy thông tin khách KHÔNG HỀ TỚI MÁY CHỦ — không có dòng nào trong access log, chỉ có đúng 1 dòng của request báo lỗi JS; 26 giây sau khách mở lại thì chính request đó trả về bình thường cùng với request lấy khung giờ; (b) trang vẫn SỐNG và vẫn gọi mạng ra được ngay lúc đó, vì nhánh báo lỗi có chạy và request báo lỗi JS đã tới máy chủ thành công.
   ⇒ Loại trừ được: lỗi máy chủ, trang bị đóng/rời đi, và mạng của khách hỏng (cùng thiết bị, cùng địa chỉ, cách nhau vài giây mà một request chết một request thành công). Lỗi mang tính RIÊNG của kết nối cho request đó.
   CHƯA chứng minh được vì sao kết nối đó hỏng — ứng viên sát nhất là kết nối HTTP/2 bị đóng đúng lúc, nhưng chưa có bằng chứng nên không kết luận. Vì thế xử lý bằng cách thử lại thay vì truy tiếp: endpoint này thuần đọc và không có nhánh nào trả lỗi nghiệp vụ (không tìm thấy sự kiện vẫn trả thành công) nên mọi lần thất bại chắc chắn là lỗi tầng vận chuyển, thử lại an toàn tuyệt đối và thực tế lần khách bấm lại luôn thành công.
   Nhánh xử lý lỗi này mới được lấp ở ticket TRƯỚC (trước đó để rỗng) nên từ lúc release mới lộ ra thành thông báo doạ khách + cảnh báo Chatwork, dù sự cố vốn đã âm thầm xảy ra từ trước.

## 2. Cách fix

Gồm 3 phần sửa + phần log chẩn đoán.

(1) Hết TypeError: bọc kiểm tra rỗng cho từng ô nhập thẻ trong hàm xoá trắng ô thẻ — chỉ gọi lệnh xoá khi ô đó thực sự đã được khởi tạo, nên nhánh báo lỗi của đăng ký/đổi lịch không còn ném lỗi và các dòng phía sau chạy đủ.

(2) Hết màn trắng: chỉ quay về bước nhập thẻ khi khách THỰC SỰ đi qua bước đó (tham số autoBill = 1, tức nút ở màn xác nhận thanh toán). Sự kiện miễn phí giữ nguyên màn xác nhận với nút vừa được mở lại nên sửa/gửi lại được ngay. Áp cho CẢ 2 nhánh: đăng ký mới (lỗi vốn có từ trước) và đổi lịch (hồi quy do phần sửa (1) mở khoá). Dùng tham số autoBill thay vì cờ is_auto_bill của sự kiện vì nó khớp đúng nút khách vừa bấm, chặn thêm được ca sự kiện có thu tiền nhưng khoá giá 0 đồng / gói miễn phí.

(3) Hết báo động giả 'getFriendInfo request failed': request chết ở tầng vận chuyển (không nhận được response nào) thì THỬ LẠI ĐÚNG 1 LẦN sau 800ms rồi mới báo. An toàn tuyệt đối vì endpoint thuần đọc, chỉ SELECT, và không có nhánh nào trả lỗi nghiệp vụ. Chốt 1 lần (không phải 2) vì lỗi thuộc riêng kết nối của request đó chứ không phải trạng thái kéo dài — lần gọi lại gần như luôn đi qua được, thử nhiều lần chỉ kéo dài thời gian khách ngồi chờ trước khi thấy thông báo. Kèm theo: không báo nhầm lỗi mạng khi request bị huỷ do trang chủ động chuyển đi.

(4) Log chẩn đoán. Phía máy chủ: hàm lấy thông tin khách ghi log lúc VÀO (mã sự kiện, mã khách, cờ mã khách rỗng, địa chỉ IP, trình duyệt, trang giới thiệu), lúc TRA CỨU (tìm được khách hay không, số ô thông tin, số khung giờ) và lúc RA (số ô, số ô điền sẵn được, thời lượng xử lý) — không có dòng VÀO nghĩa là request chưa từng tới máy chủ, có VÀO mà thiếu RA nghĩa là chết giữa chừng. Phía khách: mỗi lần lỗi đính kèm toàn bộ số đo tại thời điểm đó (trạng thái hiển thị của trang, thiết bị có mạng không, request sống được bao lâu, lỗi xảy ra bao lâu sau khi trang load, thông tin mạng, số lần đã thử lại, và bản ghi đo hiệu năng của chính request đó để biết nó đã ra tới mạng hay chưa), cộng toàn bộ thuộc tính đọc được của đối tượng request (mã trạng thái, chữ trạng thái, giai đoạn, toàn bộ header trả về — rỗng là bằng chứng không có response nào về tới nơi, kiểu nội dung, thân trả về, JSON trả về). Ngoài ra ghi VẾT THAO TÁC của khách tại 13 điểm trên toàn luồng, giữ 40 bước gần nhất và gửi kèm lúc báo lỗi.

(5) Chatwork CHỈ nhận lỗi chính như hiện tại; sự cố thoáng qua đã tự khắc phục và vết thao tác chỉ ghi log máy chủ. Hạn mức gửi và khoá trùng tách riêng theo đích đến nên không ăn mất suất của lỗi thật.

**Bổ sung (Journal #137091, nguyên văn):**
> Bổ sung lần 5 (yêu cầu human): LOG ĐẦY ĐỦ THUỘC TÍNH jqXHR khi request lấy thông tin khách hỏng. Hàm mới collectXhrInfo đọc mọi thứ jQuery thực sự cung cấp trên bản bọc jqXHR: status, statusText, readyState (0-4 — dừng ở 0/1 nghĩa là chết trước khi nhận byte nào của response), trạng thái Deferred (pending/resolved/rejected), TOÀN BỘ response headers (chuỗi rỗng = bằng chứng trực tiếp không có response nào về tới nơi), Content-Type, thân responseText (cắt 500 ký tự — chỗ duy nhất nhìn thấy trang lỗi HTML 502/504 của nginx khi status bị quy về 0), và responseJSON nếu parse được. Khối xhr này đính vào CẢ 2 báo cáo: lần hỏng tạm thời trước khi thử lại (chỉ ghi log backend) lẫn lần thất bại cuối cùng (đẩy Chatwork). Toàn bộ bọc try/catch, lỗi khi đọc ghi vào readError. Cố ý KHÔNG đọc responseURL/timeout/withCredentials/upload — jQuery không chuyển tiếp các thuộc tính đó, đọc ra undefined rồi tưởng là dữ liệu thật. Kèm theo: nới trần payload detail phía client 2000→4000 ký tự và phía server 2000→4000 (khối xhr chiếm tới ~1700 ký tự, giữ trần cũ là cắt mất đúng phần vừa thêm); Chatwork vẫn chỉ nhận bản rút gọn 1000 như đã chốt. Giữ nguyên toàn bộ các phần trước.

**Rủi ro / lưu ý khi test (mục "TỰ REVIEW (AI)", nguyên văn):**
- Sự kiện thanh toán thẻ (autoBill=1, bấm nút ở màn xác nhận thanh toán): hành vi giữ NGUYÊN như trước — vẫn quay về bước nhập thẻ, không có thay đổi nào
- 4 điểm reset ở nhánh xác thực 3D-Secure của Stripe (dòng 780/805/944/969) KHÔNG đụng tới: đã kiểm chúng nằm trong if(type_system_bill==1 && res.already_payment) nên chỉ chạy khi đã thực sự quẹt thẻ (autoBill=1), thêm điều kiện vào đó là thừa
- Sự kiện miễn phí nay đứng lại màn xác nhận thay vì nhảy bước: đúng trạng thái trước khi có ticket này (lúc đó TypeError chặn dòng đổi bước), nút đã được mở lại ngay phía trên nên khách gửi lại được

**Verify phía Dev:** mức **lint** (`node --check`, `php -l`) — "Chưa chạy được trên LINE thật: container không có thiết bị/LIFF".

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `resetElement` (`public/js/booking_event_day/order-item.js:339`) | Bọc null-check từng ô thẻ | 6 caller cùng file: :940 :965 :1013 (payment) / :1123 :1148 :1169 (changeBooking) |
| 2 | `payment` — nhánh `res.success=='error'` (order-item.js:1010) | Chỉ về bước thẻ khi `autoBill==1` | Caller blade `payment(0)`@450 [btn-payment-0], `payment(1)`@757 |
| 3 | `changeBooking` — nhánh `res.success=='error'` (order-item.js:1186) | Chỉ về bước thẻ khi `autoBill==1` | Caller blade `changeBooking(0)`@556 [btn-change-booking-0], `changeBooking(1)`@758 |
| 4 | `getFriendInfo` + nhánh `.fail` (order-item.js:1487) | Retry 1 lần / 800ms, log xhr | Caller `changePageBooking`:401 + tự gọi lại khi retry :1580 |
| 5 | `getSlots` — nhánh `res.success==false` (order-item.js:454-458) | Thêm `markLeavingPage()` trước `window.location.href` | Chuyển sang trang kết bạn |
| 6 | `MobileEventBookingController@getSlots` (`app/Http/Controllers/Basic/MobileEventBookingController.php:210`) | — | 2 nhánh trả `success=false` + url kết bạn |
| 7 | `MobileEventBookingController@index` | — | Cách suy ra lineId từ `u_code` |
| 8 | `MobileEventBookingController@reportJsError` (MobileEventBookingController.php:1508) | **HÀM BỊ SỬA**: thêm nhánh `notify=0` thoát trước Chatwork, nới detail 1000→4000, thêm `steps` | Route POST `/ajax/booking-event/report-js-error` (routes/web.php:4130, `throttle:10,1`) |
| 9 | `BookingEventDayController@getFriendInfoEvent` (BookingEventDayController.php:6127) | Thêm log VÀO / TRA CỨU / RA | Chỉ route POST `/mobile/booking-event/get-friend-info` (routes/web.php:3868). LƯU Ý: route `/ajax/booking-event/get-friend-info` (:3695) trỏ `BookingEventController@getFriendInfoEvent` = CLASS KHÁC, không bị ảnh hưởng |
| 10 | `reportBookingEventJsError` (blade `index.blade.php:52`) | Đổi chữ ký thêm `options` | Caller `window.onerror`:115, `unhandledrejection`:126, `getFriendInfo`:1568 + :1586 (lời gọi cũ 2 tham số vẫn giữ hành vi Chatwork) |
| 11 | `pushBookingEventStep` (blade `index.blade.php:29`) | **HÀM MỚI**, chèn vào 14 điểm trên đường đi chính của khách trong order-item.js | Có stub rỗng phòng hộ ở order-item.js:174-180 |
| 12 | `isLeavingPage` / `markLeavingPage` / `clearLeavingPage` (order-item.js:18-22, 297-306) | Mới | Cờ đánh dấu chủ động rời trang; chỉ `getFriendInfo.fail` đọc |
| 13 | Khối `liff.init` 3 tầng (blade `index.blade.php:796-839`) | — | Nguồn biến `userId` mà getFriendInfo dùng |
| 14 | View đăng ký sự kiện (`resources/views/basic/booking_event_day/order/index.blade.php`) | — | — |

> ⚠️ Số điểm ghi vết lệch nhau giữa các đoạn: mục 2(4) ghi **13 điểm**, mục 3 ghi **14 điểm** (requirement REQ-012 trên Studio ghi 10 điểm).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `resetElement` (xoá trắng 3 ô thẻ Stripe) | `public/js/booking_event_day/order-item.js` | Direct | Null-check; 6 caller trong payment/changeBooking |
| F2 | `payment` — nhánh lỗi đăng ký | `order-item.js` | Direct | Về bước thẻ chỉ khi `autoBill==1` |
| F3 | `changeBooking` — nhánh lỗi đổi lịch | `order-item.js` | Direct | Về bước thẻ chỉ khi `autoBill==1` (fix hồi quy) |
| F4 | `getFriendInfo` + `.fail` (+ `collectXhrInfo`) | `order-item.js` | Direct | Retry 1 lần sau 800ms khi status 0; log xhr |
| F5 | `getSlots` nhánh `success==false` + `markLeavingPage/clearLeavingPage/isLeavingPage` | `order-item.js` | Direct | Không báo nhầm lỗi mạng khi chủ động chuyển trang kết bạn |
| F6 | `reportBookingEventJsError` + `window.onerror` + `unhandledrejection` | `resources/views/basic/booking_event_day/order/index.blade.php` | Direct | Chữ ký thêm `options` (notify/steps) |
| F7 | `pushBookingEventStep` (mới) | `index.blade.php` + stub `order-item.js` | Direct | Vết thao tác, giữ 40 bước gần nhất |
| F8 | `MobileEventBookingController@reportJsError` — POST `/ajax/booking-event/report-js-error` | `app/Http/Controllers/Basic/MobileEventBookingController.php` | Direct | `notify=0` chỉ log; detail 4000; `steps`; throttle 10/phút |
| F9 | `BookingEventDayController@getFriendInfoEvent` — POST `/mobile/booking-event/get-friend-info` | `app/Http/Controllers/Basic/BookingEventDayController.php` | Direct | Chỉ thêm log, không đổi response |
| F10 | Nhánh 3D-Secure Stripe (4 điểm reset dòng 780/805/944/969) | `order-item.js` | Indirect | Không đụng code — Dev khẳng định chỉ chạy khi `autoBill=1` |
| F11 | `MobileEventBookingController@getSlots` / `@index` · khối `liff.init` | Controller + blade | Indirect | Chỉ check, không sửa |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | DB | — | KHÔNG đổi dữ liệu DB — toàn bộ diff chỉ SELECT, không insert/update/delete, không migration |
| D2 | Tham số POST mới `notify` (0/1) và `steps` (chuỗi JSON ≤ 2000) ở `/ajax/booking-event/report-js-error` | Thêm tham số | Thiếu tham số thì mặc định `notify=1` nên client cũ giữ nguyên hành vi |
| D3 | Giới hạn `detail` của endpoint báo lỗi | UPDATE (config code) | 1000 → 4000 ký tự (bản 1000 vẫn là bản gửi Chatwork) — ⚠️ #137091 ghi 2000→4000 |
| D4 | Log server (không phải DB) | CREATE (log) | Dữ liệu cá nhân mới trong log: `line_id` + IP + User-Agent + Referer ghi mỗi lần mở màn đăng ký (BookingEventDayController:6136/6166/6244); phía client đính thêm `responseText`/`responseJSON` của request hỏng (có thể chứa tên/điện thoại/email khách) → cần chốt mốc gỡ log sau khi truy xong nguyên nhân |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Dev (AI) chỉ ghi Trực tiếp / GIÁN TIẾP, **không ghi mức High/Medium/Low** — cột nguy cơ giữ nguyên chữ Dev ghi.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đặt lịch sự kiện — Event Booking (FA-021), màn đăng ký/đổi lịch trên LIFF: hết TypeError ở nhánh báo lỗi; sự kiện miễn phí/Univapay không còn màn trắng; request lấy thông tin khách chết ở tầng vận chuyển được tự thử lại 1 lần. Sự kiện Stripe có thu tiền: hành vi giữ nguyên | F1–F5 | Trực tiếp |
| T2 | Cảnh báo lỗi JS gửi Chatwork: chỉ còn nhận lỗi thật khách nhìn thấy; sự cố thoáng qua + vết thao tác chỉ ghi log backend | F6–F8, D2, D3 | Trực tiếp |
| T3 | Thanh toán thẻ trong đặt lịch sự kiện (Stripe/Univapay): không đổi lệnh gọi cổng thanh toán, chỉ đổi KHI NÀO quay lại bước nhập thẻ sau lỗi; **luồng Univapay cần QA bấm thử** | F1–F3, F10 | GIÁN TIẾP |
| T4 | Kết bạn khi chưa là bạn từ màn đăng ký sự kiện: luồng chuyển trang giữ nguyên, chỉ thêm đánh dấu để không báo nhầm lỗi mạng | F5 | GIÁN TIẾP |
| T5 | Vận hành log server: +3 dòng info mỗi lượt mở màn đăng ký của MỌI bot, payload báo lỗi to gấp ~3 | F9, D4 | GIÁN TIẾP |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
