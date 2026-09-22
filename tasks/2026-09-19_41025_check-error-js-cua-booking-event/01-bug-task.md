# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #41025 bởi `/new-task` (2026-09-19). Metadata Redmine tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41025 — Check error js của booking event` |
| Module / Màn hình | Event Booking (FA-021) — LIFF イベント予約 (màn đăng ký / đổi lịch sự kiện trên LINE), URL `https://s.lmes.jp/mobile/event-booking/index/<...>` · JS `public/js/booking_event_day/order-item.js` |

## Mô tả bug (bản dịch tiếng Việt)

Ticket là bug tự detect (Tracker "Bug tự detect") — description là danh sách cảnh báo lỗi JavaScript tự động gửi về từ màn [イベント予約 LIFF] (LIFF đặt lịch sự kiện). Log giữ nguyên văn:

* [イベント予約 LIFF] Lỗi JavaScript
  - message: `getFriendInfo request failed`
  - url: `https://s.lmes.jp/mobile/event-booking/index/Dl7r7NQ5WJje/v68hcebf22`
  - user_agent: `Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari Line/15.9.0 LIFF`
  - detail: `{"where":"getFriendInfo.fail","status":0,"textStatus":"error","errorThrown":null}`
* [イベント予約 LIFF] Lỗi JavaScript
  - message: `TypeError: null is not an object (evaluating 'this.cardNumber.clear')`
  - url: `https://s.lmes.jp/mobile/event-booking/index/E2abBPO2rwvg/VeWxxt1Pak`
  - user_agent: `Mozilla/5.0 (iPhone; CPU iPhone OS 26_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari Line/26.14.1 LIFF`
  - detail: `{"where":"window.onerror","source":"https://s.lmes.jp/js/booking_event_day/order-item.js?v=2026091630","line":188,"col":28,"stack":"resetElement@https://s.lmes.jp/js/booking_event_day/order-item.js:188:28\nsuccess@https://s.lmes.jp/js/booking_event_day/order-item.js:978:54\nc@https://code.jquery.com/jquery-3.6.3.min.js:2:28604\nfireWith@https://code.jquery.com/jquery-3.6.3.min.js:2:29345\nl@https://code.jquery.com/jquery-3.6.3.min.js:2:80339\n@https://code.jquery.com/jquery-3.6.3.min.js:2:82783"}`
* [イベント予約 LIFF] Lỗi JavaScript
  - message: `Uncaught TypeError: Cannot read properties of null (reading 'clear')`
  - url: `https://s.lmes.jp/mobile/event-booking/index/YJlq1ojOWR6B/dUD8EPTOLb#wrap-input-choose-plan-slot`
  - user_agent: `Mozilla/5.0 (Linux; Android 16; A502SO Build/72.1.A.2.184; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/151.0.7922.199 Mobile Safari/537.36 Line/26.14.0 LIFF`
  - detail: `{"where":"window.onerror","source":"https://s.lmes.jp/js/booking_event_day/order-item.js?v=2026091630","line":188,"col":29,"stack":"TypeError: Cannot read properties of null (reading 'clear')\n    at nt.resetElement (https://s.lmes.jp/js/booking_event_day/order-item.js?v=2026091630:188:29)\n    at nt.n [as resetElement] (https://s.lmes.jp/js/media/vue.min.js:6:839)\n    at Object.success (https://s.lmes.jp/js/booking_event_day/order-item.js?v=2026091630:823:42)\n    at c (https://code.jquery.com/jquery-3.6.3.min.js:2:28599)\n    at Object.fireWith [as resolveWith] (https://code.jquery.com/jquery-3.6.3.min.js:2:29344)\n    at l (https://code.jquery.com/jquery-3.6.3.min.js:2:80328)\n    at XMLHttpRequest.<anonymous> (https://code.jquery.com/jquery-3.6.3.min.js:2:82782)"}`
* [イベント予約 LIFF] Lỗi JavaScript
  - message: `Uncaught TypeError: Cannot read properties of null (reading 'clear')`
  - url: `https://s.lmes.jp/mobile/event-booking/index/E4PbaDB6q6OV/TmWJLChQxh`
  - user_agent: `Mozilla/5.0 (Linux; Android 16; SCG34 Build/BP4A.251205.006; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/153.0.8010.36 Mobile Safari/537.36 Line/26.14.0 LIFF`
  - detail: `{"where":"window.onerror","source":"https://s.lmes.jp/js/booking_event_day/order-item.js?v=2026091630","line":188,"col":29,"stack":"TypeError: Cannot read properties of null (reading 'clear')\n    at nt.resetElement (https://s.lmes.jp/js/booking_event_day/order-item.js?v=2026091630:188:29)\n    at nt.n [as resetElement] (https://s.lmes.jp/js/media/vue.min.js:6:839)\n    at Object.success (https://s.lmes.jp/js/booking_event_day/order-item.js?v=2026091630:823:42)\n    at c (https://code.jquery.com/jquery-3.6.3.min.js:2:28599)\n    at Object.fireWith [as resolveWith] (https://code.jquery.com/jquery-3.6.3.min.js:2:29344)\n    at l (https://code.jquery.com/jquery-3.6.3.min.js:2:80328)\n    at XMLHttpRequest.<anonymous> (https://code.jquery.com/jquery-3.6.3.min.js:2:82782)"}`

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug". -->

## Expected result

## Actual result

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — log lỗi JS nằm ngay trong description (không có attachment)

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Ticket **gộp 3 lỗi khác nhau** (theo journal AI auto-fixbug): (1) TypeError `this.cardNumber.clear` ở nhánh báo lỗi đăng ký/đổi lịch với sự kiện miễn phí / Univapay · (2) màn trắng sau lỗi nghiệp vụ (vd 予約がいっぱいです。) — nhánh đổi lịch là **hồi quy do chính fix (1) mở khoá** · (3) `getFriendInfo request failed` status 0 — lỗi tầng vận chuyển, **không tái hiện chủ động được**, fix bằng retry 1 lần.
- Môi trường phát hiện: **Production** (`s.lmes.jp`), LIFF trên LINE app — iOS 18.7 / iOS 26.6.1 / Android 16 (LINE 15.9.0 · 26.14.0 · 26.14.1).
- Điều kiện dựng env: cần ≥ 3 loại sự kiện — **miễn phí**, **Stripe** (`type_system_bill=1`), **Univapay** (`type_system_bill=2`); thêm ca `is_auto_bill=1` nhưng gói giá 0 / bot gói `free`. Trigger lỗi nghiệp vụ phổ biến nhất: chọn khung giờ vừa hết chỗ.
- Lỗi (3) chỉ quan sát được khi request chết ở tầng vận chuyển — test cần giả lập (chặn request / offline tạm thời); Dev ghi "Chưa chạy được trên LINE thật: container không có thiết bị/LIFF" (verify mới ở mức lint).
- JS gắn tham số phiên bản `order-item.js?v=...` → sau deploy phải xác nhận trang nạp đúng bản mới (cache).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<không có trong ticket>` |
| Ca lỗi (3) getFriendInfo status 0 | `/mobile/event-booking/index/Dl7r7NQ5WJje/v68hcebf22` — iPhone iOS 18.7, LINE 15.9.0 |
| Ca lỗi (1) cardNumber.clear | `/index/E2abBPO2rwvg/VeWxxt1Pak` (iOS 26.6.1) · `/index/YJlq1ojOWR6B/dUD8EPTOLb` (Android 16 A502SO) · `/index/E4PbaDB6q6OV/TmWJLChQxh` (Android 16 SCG34) |
| Vị trí lỗi | `order-item.js?v=2026091630` dòng 188 (`resetElement`), gọi từ `success` dòng 978 / 823 |
| Thời điểm lỗi | `<không có trong ticket>` |
| Đối chứng | Journal: 26 giây sau khách mở lại thì request getFriendInfo trả về bình thường |

## Journal / note từ Redmine (nguyên văn)

**Journal #137091 — AI LME Fix bug — 2026-09-18:**

```
<pre>
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt &amp; push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
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

■ 2. CÁCH FIX
Bổ sung lần 5 (yêu cầu human): LOG ĐẦY ĐỦ THUỘC TÍNH jqXHR khi request lấy thông tin khách hỏng. Hàm mới collectXhrInfo đọc mọi thứ jQuery thực sự cung cấp trên bản bọc jqXHR: status, statusText, readyState (0-4 — dừng ở 0/1 nghĩa là chết trước khi nhận byte nào của response), trạng thái Deferred (pending/resolved/rejected), TOÀN BỘ response headers (chuỗi rỗng = bằng chứng trực tiếp không có response nào về tới nơi), Content-Type, thân responseText (cắt 500 ký tự — chỗ duy nhất nhìn thấy trang lỗi HTML 502/504 của nginx khi status bị quy về 0), và responseJSON nếu parse được. Khối xhr này đính vào CẢ 2 báo cáo: lần hỏng tạm thời trước khi thử lại (chỉ ghi log backend) lẫn lần thất bại cuối cùng (đẩy Chatwork). Toàn bộ bọc try/catch, lỗi khi đọc ghi vào readError. Cố ý KHÔNG đọc responseURL/timeout/withCredentials/upload — jQuery không chuyển tiếp các thuộc tính đó, đọc ra undefined rồi tưởng là dữ liệu thật. Kèm theo: nới trần payload detail phía client 2000→4000 ký tự và phía server 2000→4000 (khối xhr chiếm tới ~1700 ký tự, giữ trần cũ là cắt mất đúng phần vừa thêm); Chatwork vẫn chỉ nhận bản rút gọn 1000 như đã chốt. Giữ nguyên toàn bộ các phần trước.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
resetElement (public/js/booking_event_day/order-item.js)
payment - nhánh res.success=='error'
changeBooking - nhánh res.success=='error'
getFriendInfo + nhánh .fail (public/js/booking_event_day/order-item.js)
getSlots - nhánh res.success==false -&gt; window.location.href (public/js/booking_event_day/order-item.js)
MobileEventBookingController@getSlots (app/Http/Controllers/Basic/MobileEventBookingController.php:210) - 2 nhánh trả success=false + url kết bạn
MobileEventBookingController@index - cách suy ra lineId từ u_code
BookingEventDayController@getFriendInfoEvent
reportBookingEventJsError + window.onerror + unhandledrejection (resources/views/basic/booking_event_day/order/index.blade.php)
khối liff.init 3 tầng (resources/views/basic/booking_event_day/order/index.blade.php:741)
view đăng ký sự kiện (resources/views/basic/booking_event_day/order/index.blade.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - public/js/booking_event_day/order-item.js
   - resources/views/basic/booking_event_day/order/index.blade.php
   - app/Http/Controllers/Basic/BookingEventDayController.php
   - app/Http/Controllers/Basic/MobileEventBookingController.php
 • 4.2 Data ảnh hưởng:
   - Không có — không đụng bảng nào, chỉ ghi thêm log ra file
 • 4.3 Tính năng liên quan:
   - Event Booking (FA-021) — màn đăng ký/đổi lịch sự kiện trên LINE: hết lỗi JavaScript ở nhánh báo lỗi; sự kiện miễn phí không còn màn trắng; request lấy thông tin khách chết ở tầng vận chuyển được tự thử lại thay vì doạ khách
   - Cảnh báo lỗi JS gửi Chatwork — chỉ còn nhận lỗi thật khách nhìn thấy; sự cố thoáng qua và vết thao tác chuyển hết về log backend

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: node --check public/js/booking_event_day/order-item.js: OK; php -l app/Http/Controllers/Basic/MobileEventBookingController.php: No syntax errors detected; Tách khối script báo lỗi trong blade rồi node --check: OK; Làm việc trong git worktree riêng (worktrees/chat-41025-sns-line) vì working copy source/sns-line đang bị worker khác checkout branch ai_fixbug_41108 — tránh hazard shared-checkout; commit xong đã worktree remove sạch; git log ai_fixbug_41025: commit mới 3ac589e748 nằm trên branch, diff dashboard đã cập nhật; Chưa chạy được trên LINE thật: container không có thiết bị/LIFF

■ TỰ REVIEW (AI)
Refix vòng 1 theo AI review: sửa hồi quy do chính diff vòng 1 mở khoá. Đã đọc blade resources/views/basic/booking_event_day/order/index.blade.php xác nhận: khối đăng ký dùng v-show page=='confirm-order' (dòng 315), khối đổi lịch dùng v-if page=='confirm-change-order' (dòng 398, bị huỷ khỏi DOM), còn khối nhập thẻ v-show yêu cầu eventDetail.is_auto_bill==1 (dòng 591) nên sự kiện miễn phí đổi sang page='payment' là màn trắng. Chọn điều kiện autoBill==1 (tham số hàm) thay vì eventDetail.is_auto_bill: đã truy hết 4 nơi gọi trong blade — payment(0)/changeBooking(0) là nút v-else ở màn xác nhận thường, payment(1)/changeBooking(1) nằm trong khối confirm-payment; autoBill do đó phản ánh đúng khách có đi qua bước nhập thẻ hay không, chặn được cả ca is_auto_bill==1 nhưng plan_price==0 / contractType=='free' (v-if dòng 388/493 trượt nên vẫn gọi nhánh autoBill=0).
 • Rủi ro / lưu ý khi test:
   - Sự kiện thanh toán thẻ (autoBill=1, bấm nút ở màn xác nhận thanh toán): hành vi giữ NGUYÊN như trước — vẫn quay về bước nhập thẻ, không có thay đổi nào
   - 4 điểm reset ở nhánh xác thực 3D-Secure của Stripe (dòng 780/805/944/969) KHÔNG đụng tới: đã kiểm chúng nằm trong if(type_system_bill==1 &amp;&amp; res.already_payment) nên chỉ chạy khi đã thực sự quẹt thẻ (autoBill=1), thêm điều kiện vào đó là thừa
   - Sự kiện miễn phí nay đứng lại màn xác nhận thay vì nhảy bước: đúng trạng thái trước khi có ticket này (lúc đó TypeError chặn dòng đổi bước), nút đã được mở lại ngay phía trên nên khách gửi lại được

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41025 (nhánh gốc release_step_20260827, commit 98db57da20, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 3 phút 28 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&amp;tab=events&amp;session=e6e5adec-a8b4-40a2-bf4f-3483b843e082
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=41025
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
</pre>
```

**Journal #137108 — AI LME Fix bug — 2026-09-18:**

```
<pre>
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt &amp; push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
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

■ 2. CÁCH FIX
Gồm 3 phần sửa + phần log chẩn đoán.

(1) Hết TypeError: bọc kiểm tra rỗng cho từng ô nhập thẻ trong hàm xoá trắng ô thẻ — chỉ gọi lệnh xoá khi ô đó thực sự đã được khởi tạo, nên nhánh báo lỗi của đăng ký/đổi lịch không còn ném lỗi và các dòng phía sau chạy đủ.

(2) Hết màn trắng: chỉ quay về bước nhập thẻ khi khách THỰC SỰ đi qua bước đó (tham số autoBill = 1, tức nút ở màn xác nhận thanh toán). Sự kiện miễn phí giữ nguyên màn xác nhận với nút vừa được mở lại nên sửa/gửi lại được ngay. Áp cho CẢ 2 nhánh: đăng ký mới (lỗi vốn có từ trước) và đổi lịch (hồi quy do phần sửa (1) mở khoá). Dùng tham số autoBill thay vì cờ is_auto_bill của sự kiện vì nó khớp đúng nút khách vừa bấm, chặn thêm được ca sự kiện có thu tiền nhưng khoá giá 0 đồng / gói miễn phí.

(3) Hết báo động giả 'getFriendInfo request failed': request chết ở tầng vận chuyển (không nhận được response nào) thì THỬ LẠI ĐÚNG 1 LẦN sau 800ms rồi mới báo. An toàn tuyệt đối vì endpoint thuần đọc, chỉ SELECT, và không có nhánh nào trả lỗi nghiệp vụ. Chốt 1 lần (không phải 2) vì lỗi thuộc riêng kết nối của request đó chứ không phải trạng thái kéo dài — lần gọi lại gần như luôn đi qua được, thử nhiều lần chỉ kéo dài thời gian khách ngồi chờ trước khi thấy thông báo. Kèm theo: không báo nhầm lỗi mạng khi request bị huỷ do trang chủ động chuyển đi.

(4) Log chẩn đoán. Phía máy chủ: hàm lấy thông tin khách ghi log lúc VÀO (mã sự kiện, mã khách, cờ mã khách rỗng, địa chỉ IP, trình duyệt, trang giới thiệu), lúc TRA CỨU (tìm được khách hay không, số ô thông tin, số khung giờ) và lúc RA (số ô, số ô điền sẵn được, thời lượng xử lý) — không có dòng VÀO nghĩa là request chưa từng tới máy chủ, có VÀO mà thiếu RA nghĩa là chết giữa chừng. Phía khách: mỗi lần lỗi đính kèm toàn bộ số đo tại thời điểm đó (trạng thái hiển thị của trang, thiết bị có mạng không, request sống được bao lâu, lỗi xảy ra bao lâu sau khi trang load, thông tin mạng, số lần đã thử lại, và bản ghi đo hiệu năng của chính request đó để biết nó đã ra tới mạng hay chưa), cộng toàn bộ thuộc tính đọc được của đối tượng request (mã trạng thái, chữ trạng thái, giai đoạn, toàn bộ header trả về — rỗng là bằng chứng không có response nào về tới nơi, kiểu nội dung, thân trả về, JSON trả về). Ngoài ra ghi VẾT THAO TÁC của khách tại 13 điểm trên toàn luồng, giữ 40 bước gần nhất và gửi kèm lúc báo lỗi.

(5) Chatwork CHỈ nhận lỗi chính như hiện tại; sự cố thoáng qua đã tự khắc phục và vết thao tác chỉ ghi log máy chủ. Hạn mức gửi và khoá trùng tách riêng theo đích đến nên không ăn mất suất của lỗi thật.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
resetElement (public/js/booking_event_day/order-item.js:339) - 6 caller cung file: :940 :965 :1013 (payment) / :1123 :1148 :1169 (changeBooking)
payment - nhanh res.success==error (order-item.js:1010); caller blade payment(0)@450 [btn-payment-0], payment(1)@757
changeBooking - nhanh res.success==error (order-item.js:1186); caller blade changeBooking(0)@556 [btn-change-booking-0], changeBooking(1)@758
getFriendInfo + nhanh .fail (order-item.js:1487) - caller changePageBooking:401 + tu goi lai khi retry :1580
getSlots - nhanh res.success==false -&gt; markLeavingPage() + window.location.href (order-item.js:454-458)
MobileEventBookingController@getSlots (app/Http/Controllers/Basic/MobileEventBookingController.php:210) - 2 nhanh tra success=false + url ket ban
MobileEventBookingController@index - cach suy ra lineId tu u_code
MobileEventBookingController@reportJsError (MobileEventBookingController.php:1508) - HAM BI SUA (them nhanh notify=0 thoat truoc Chatwork, noi detail 1000-&gt;4000, them steps); route POST /ajax/booking-event/report-js-error (routes/web.php:4130, throttle:10,1)
BookingEventDayController@getFriendInfoEvent (BookingEventDayController.php:6127) - chi route POST /mobile/booking-event/get-friend-info (routes/web.php:3868). LUU Y: route /ajax/booking-event/get-friend-info (:3695) tro BookingEventController@getFriendInfoEvent = CLASS KHAC, khong bi anh huong
reportBookingEventJsError (blade index.blade.php:52) - doi chu ky them options; caller window.onerror :115, unhandledrejection :126, getFriendInfo :1568 + :1586 (loi goi cu 2 tham so van giu hanh vi Chatwork)
pushBookingEventStep (blade index.blade.php:29) - HAM MOI, chen vao 14 diem tren duong di chinh cua khach trong order-item.js; co stub rong phong ho o order-item.js:174-180
isLeavingPage / markLeavingPage / clearLeavingPage (order-item.js:18-22, 297-306) - co danh dau chu dong roi trang; chi getFriendInfo.fail doc
khoi liff.init 3 tang (blade index.blade.php:796-839) - nguon bien userId ma getFriendInfo dung
view dang ky su kien (resources/views/basic/booking_event_day/order/index.blade.php)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - public/js/booking_event_day/order-item.js
   - resources/views/basic/booking_event_day/order/index.blade.php
   - app/Http/Controllers/Basic/BookingEventDayController.php
   - app/Http/Controllers/Basic/MobileEventBookingController.php
 • 4.2 Data ảnh hưởng:
   - KHONG doi du lieu DB - toan bo diff chi SELECT, khong insert/update/delete, khong migration
   - Tham so POST MOI: notify (0/1) va steps (chuoi JSON &lt;=2000) o endpoint /ajax/booking-event/report-js-error; thieu tham so thi mac dinh notify=1 nen client cu giu nguyen hanh vi
   - Noi gioi han detail cua endpoint bao loi tu 1000 -&gt; 4000 ky tu (ban 1000 van la ban gui Chatwork)
   - DU LIEU CA NHAN MOI TRONG LOG (khong phai DB): line_id + IP + User-Agent + Referer ghi moi lan mo man dang ky (BookingEventDayController:6136/6166/6244); phia client dinh them responseText/responseJSON cua request hong (co the chua ten/dien thoai/email khach) -&gt; can chot moc go log sau khi truy xong nguyen nhan
 • 4.3 Tính năng liên quan:
   - Dat lich su kien - Event Booking (FA-021), man dang ky/doi lich tren LIFF: het TypeError o nhanh bao loi; su kien mien phi/Univapay khong con man trang; request lay thong tin khach chet o tang van chuyen duoc tu thu lai 1 lan. Su kien Stripe co thu tien: hanh vi giu nguyen
   - Canh bao loi JS gui Chatwork: chi con nhan loi that khach nhin thay; su co thoang qua + vet thao tac chi ghi log backend
   - Thanh toan the trong dat lich su kien (Stripe/Univapay) - GIAN TIEP: khong doi lenh goi cong thanh toan, chi doi KHI NAO quay lai buoc nhap the sau loi; luong Univapay can QA bam thu
   - Ket ban khi chua la ban tu man dang ky su kien - GIAN TIEP: luong chuyen trang giu nguyen, chi them danh dau de khong bao nham loi mang
   - Van hanh log server - GIAN TIEP: +3 dong info moi luot mo man dang ky cua MOI bot, payload bao loi to gap ~3

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: node --check public/js/booking_event_day/order-item.js: OK; php -l app/Http/Controllers/Basic/MobileEventBookingController.php: No syntax errors detected; Tách khối script báo lỗi trong blade rồi node --check: OK; Làm việc trong git worktree riêng (worktrees/chat-41025-sns-line) vì working copy source/sns-line đang bị worker khác checkout branch ai_fixbug_41108 — tránh hazard shared-checkout; commit xong đã worktree remove sạch; git log ai_fixbug_41025: commit mới 3ac589e748 nằm trên branch, diff dashboard đã cập nhật; Chưa chạy được trên LINE thật: container không có thiết bị/LIFF

■ TỰ REVIEW (AI)
Refix vòng 1 theo AI review: sửa hồi quy do chính diff vòng 1 mở khoá. Đã đọc blade resources/views/basic/booking_event_day/order/index.blade.php xác nhận: khối đăng ký dùng v-show page=='confirm-order' (dòng 315), khối đổi lịch dùng v-if page=='confirm-change-order' (dòng 398, bị huỷ khỏi DOM), còn khối nhập thẻ v-show yêu cầu eventDetail.is_auto_bill==1 (dòng 591) nên sự kiện miễn phí đổi sang page='payment' là màn trắng. Chọn điều kiện autoBill==1 (tham số hàm) thay vì eventDetail.is_auto_bill: đã truy hết 4 nơi gọi trong blade — payment(0)/changeBooking(0) là nút v-else ở màn xác nhận thường, payment(1)/changeBooking(1) nằm trong khối confirm-payment; autoBill do đó phản ánh đúng khách có đi qua bước nhập thẻ hay không, chặn được cả ca is_auto_bill==1 nhưng plan_price==0 / contractType=='free' (v-if dòng 388/493 trượt nên vẫn gọi nhánh autoBill=0).
 • Rủi ro / lưu ý khi test:
   - Sự kiện thanh toán thẻ (autoBill=1, bấm nút ở màn xác nhận thanh toán): hành vi giữ NGUYÊN như trước — vẫn quay về bước nhập thẻ, không có thay đổi nào
   - 4 điểm reset ở nhánh xác thực 3D-Secure của Stripe (dòng 780/805/944/969) KHÔNG đụng tới: đã kiểm chúng nằm trong if(type_system_bill==1 &amp;&amp; res.already_payment) nên chỉ chạy khi đã thực sự quẹt thẻ (autoBill=1), thêm điều kiện vào đó là thừa
   - Sự kiện miễn phí nay đứng lại màn xác nhận thay vì nhảy bước: đúng trạng thái trước khi có ticket này (lúc đó TypeError chặn dòng đổi bước), nút đã được mở lại ngay phía trên nên khách gửi lại được

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41025 (nhánh gốc release_step_20260827, commit 36501465fa, 4 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 3 phút 28 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&amp;tab=events&amp;session=f9bb45aa-1c4c-43d0-bcf8-17e353d32eb9
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=41025
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
</pre>
```
