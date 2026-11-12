# LME – Security Main Cases (chi tiết hoá) — 22/10/2026

> Nguồn: `security-audit-20261022.html` · Branch `release_step_20260930_v2`. Chi tiết hoá từng leaf case (Tiền điều kiện · Dữ liệu nhập · Các bước · Expected). Kèm bổ sung review C21–C37, X06–X08.

## Tiền điều kiện chung (áp cho mọi case)

- Staging gần cấu hình production, DB test riêng, cổng thanh toán sandbox (Stripe test / Univapay sandbox).
- 2 shop khách: **Shop A** (owner A, staff A hạn quyền) và **Shop B** (owner B). 1 **SuperAdmin**.
- Bot: **botA** (hashid hashA, channel_secret biết trước để ký webhook) · **botB** (hashid hashB, bot_id tuần tự).
- LINE user: **lineA** (bạn bè botA, có chat/tag), **lineB** (bạn bè botB).
- Dữ liệu nghiệp vụ 2 shop: chat, tag, đơn sản phẩm, booking event/lesson/salon, subscription — ở nhiều trạng thái (pending/paid/cancelled).
- File test: `ok.png` (ảnh hợp lệ), `shell.php` (`<?php echo 1;?>`), `x.html`, `y.svg` (onload), `ok.php.png`, `SHELL.PHP`.
- Quy tắc chung: HTTP 401/403 CHƯA đủ kết luận — luôn đối chiếu DB / queue-job / dịch vụ sandbox / log. Che secret khi lưu bằng chứng.


## C01. Đọc file bất kỳ trên server qua /ajax/get-file-url (lấy .env)
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.1 · Nguồn: audit SEC-01 (Confirmed)  
Vị trí/endpoint: `BasicController.php:2755 · POST /ajax/get-file-url (web.php:4248)`

**C01-01** — No-auth gọi endpoint
- **Tiền điều kiện:** Xóa toàn bộ cookie/session (ẩn danh).
- **Dữ liệu nhập:** link_url = media/shopA/ok.png (đường dẫn file media hợp lệ bất kỳ).
- **Các bước:** 1) Client không cookie POST /ajax/get-file-url 2) Ghi HTTP code + body.
- **Kết quả mong đợi:** Bị từ chối do chưa đăng nhập (302 login / 401 / 403); KHÔNG trả URL/nội dung file.

**C01-02** — Path traversal đọc .env
- **Tiền điều kiện:** Biết vị trí .env tương đối thư mục media; đăng nhập hợp lệ nếu endpoint yêu cầu.
- **Dữ liệu nhập:** link_url lần lượt: `../.env` · `../../.env` · `../../../.env` · `/var/www/html/.env` · `..%2f..%2f.env` · `%2e%2e/%2e%2e/.env` · `....//....//.env` · `php://filter/convert.base64-encode/resource=../../.env`
- **Các bước:** 1) POST từng payload 2) Đọc body 3) Nếu trả URL thì GET URL đó.
- **Kết quả mong đợi:** Mọi payload → 400/403/rỗng; KHÔNG lộ nội dung .env (APP_KEY, DB_PASSWORD); KHÔNG trả URL ngoài thư mục media.

**C01-03** — Đọc file media shop khác
- **Tiền điều kiện:** Đăng nhập owner A; biết path file của shop B: media/shopB/secret.png.
- **Dữ liệu nhập:** link_url = media/shopB/secret.png
- **Các bước:** 1) owner A POST yêu cầu file của B 2) Kiểm response.
- **Kết quả mong đợi:** Từ chối / không trả file thuộc shop B (chỉ file của shop A).

**C01-04** — File hợp lệ (positive)
- **Tiền điều kiện:** Đăng nhập owner A; file media/shopA/ok.png tồn tại.
- **Dữ liệu nhập:** link_url = media/shopA/ok.png
- **Các bước:** 1) POST 2) Nhận URL 3) GET URL.
- **Kết quả mong đợi:** Trả đúng URL/nội dung file hợp lệ của chính shop A — chức năng KHÔNG hỏng.


## C02. Trang xem log /error/logs mở công khai – xem/tải/xóa file bất kỳ
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.1 · Nguồn: audit SEC-02 (Confirmed)  
Vị trí/endpoint: `routes/web.php:81 (middleware https_protocol rỗng)`

**C02-01** — Mở trang log
- **Tiền điều kiện:** (a) ẩn danh; (b) đăng nhập user thường (không supper_admin).
- **Dữ liệu nhập:** GET /error/logs
- **Các bước:** Mở trang bằng cả 2 vai trò.
- **Kết quả mong đợi:** Cả 2 → 403/redirect; KHÔNG hiển thị nội dung laravel.log.

**C02-02** — Download/delete trực tiếp (?dl=/?del=)
- **Tiền điều kiện:** Biết tham số ?dl= / ?del= của gói log-viewer.
- **Dữ liệu nhập:** GET /error/logs?dl=/var/www/html/.env · ?dl=../../.env · ?del=storage/logs/laravel.log
- **Các bước:** Gọi từng param ẩn danh; kiểm response + file còn/mất.
- **Kết quả mong đợi:** Không tải được .env/file ngoài; không xóa được log; trả 403.

**C02-03** — File ngoài thư mục log (vai trò được phép)
- **Tiền điều kiện:** Đăng nhập supper_admin (nếu route giữ sau supper_admin); có /tmp/marker_outside.txt.
- **Dữ liệu nhập:** ?dl=/tmp/marker_outside.txt · ?dl=../../.env
- **Các bước:** supper_admin gọi tải file ngoài thư mục log.
- **Kết quả mong đợi:** Kể cả supper_admin chỉ thao tác file TRONG thư mục log; file ngoài → từ chối.

**C02-04** — File đánh dấu sau delete bị từ chối
- **Tiền điều kiện:** Tạo file storage/logs/MARKER_donotdelete.txt.
- **Dữ liệu nhập:** ?del=storage/logs/MARKER_donotdelete.txt (ẩn danh)
- **Các bước:** 1) Gọi xóa 2) Kiểm tra file còn không.
- **Kết quả mong đợi:** Request bị từ chối VÀ file MARKER còn nguyên (không xóa ngầm).


## C03. Secret Stripe/Univapay lộ trên 3 trang đặt lịch công khai
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.1 · Nguồn: audit SEC-03 (Confirmed)  
Vị trí/endpoint: `MobileEventBookingController.php:167,204 + index.blade.php:871; CalendarController.php:126,195; CalendarSalonController.php:172,255`

**C03-01** — Mở ẩn danh đủ 3 loại trang
- **Tiền điều kiện:** Ẩn danh; biết URL public trang event / lesson (mobile calendar) / salon của shopStripe & shopUniva.
- **Dữ liệu nhập:** GET trang booking event day · mobile calendar (lesson) · mobile calendar salon.
- **Các bước:** Mở từng trang ẩn danh, chuẩn bị soi ở C03-02.
- **Kết quả mong đợi:** Trang hiển thị bình thường, không lỗi (bước nền cho C03-02).

**C03-02** — Soi View Source / JS / Network tìm secret
- **Tiền điều kiện:** Đã mở các trang ở C03-01.
- **Dữ liệu nhập:** Tìm chuỗi: `strip_secret_live_key` · `univapay_secret` · `univapay_app_token` · `sk_live` · `sk_test`.
- **Các bước:** Ctrl+U; DevTools > Sources + Network; grep các khóa trong HTML/JS/XHR.
- **Kết quả mong đợi:** KHÔNG tìm thấy secret key / app token; chỉ có publishable key / cờ công khai.

**C03-03** — Stripe vs Univapay vs chưa cấu hình
- **Tiền điều kiện:** 3 shop: shopStripe, shopUniva, shopNone (chưa cấu hình thanh toán).
- **Dữ liệu nhập:** Lặp C03-02 trên cả 3 shop.
- **Các bước:** Soi secret trên từng shop.
- **Kết quả mong đợi:** Không shop nào lộ secret; shopNone không rò cấu hình nội bộ.

**C03-04** — Booking + thanh toán sandbox (positive)
- **Tiền điều kiện:** Tài khoản sandbox Stripe/Univapay.
- **Dữ liệu nhập:** Thẻ test Stripe 4242 4242 4242 4242 · Univapay sandbox token.
- **Các bước:** Đặt 1 slot + thanh toán sandbox tới hoàn tất.
- **Kết quả mong đợi:** Booking + thanh toán vẫn chạy sau khi gỡ secret (chức năng không hỏng).


## C04. Trang sản phẩm công khai in bản ghi bot ra console (LINE token, key ChatGPT)
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.1 · Nguồn: audit SEC-04 (Confirmed)  
Vị trí/endpoint: `SalesManagementV2Controller.php:1789,1931; detail.blade.php:494 · GET /v2/order-item/detail/{item_code}`

**C04-01** — Soi Console/Source/Network
- **Tiền điều kiện:** Ẩn danh; item_code hợp lệ.
- **Dữ liệu nhập:** Tìm `channel_access_token` · `channel_secret` · `key_chatgpt` · `google_sheet_access_token`.
- **Các bước:** Mở trang; xem Console, View Source, Network.
- **Kết quả mong đợi:** Không in object bot ra console; không có token/secret trong dữ liệu client.

**C04-02** — Dữ liệu còn nhúng dù đã bỏ console.log
- **Tiền điều kiện:** item_code hợp lệ.
- **Dữ liệu nhập:** grep các khóa trên trong HTML + file JS dù Console trống.
- **Các bước:** Tải HTML raw + JS, tìm khóa.
- **Kết quả mong đợi:** Object bot KHÔNG được nhúng vào trang (không chỉ ẩn console).

**C04-03** — Nhiều bot
- **Tiền điều kiện:** Shop có ≥2 bot, mỗi bot 1 product.
- **Dữ liệu nhập:** item_code của bot1 và bot2.
- **Các bước:** Soi từng trang.
- **Kết quả mong đợi:** Không bot nào lộ token.

**C04-04** — Đặt hàng hợp lệ (positive)
- **Tiền điều kiện:** Product test đặt được.
- **Dữ liệu nhập:** Đặt mua 1 item test.
- **Các bước:** Hoàn tất đơn.
- **Kết quả mong đợi:** Đặt hàng vẫn chạy bình thường.


## C05. Webhook LINE không kiểm chữ ký (luôn hợp lệ)
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.1 · Nguồn: audit SEC-05 (Confirmed) — xem task #43212  
Vị trí/endpoint: `BotController.php:2034-2040 · POST /line/callback/add/{bot_id}`

**C05-01** — Thiếu/rỗng/sai chữ ký
- **Tiền điều kiện:** Body là event message JSON hợp lệ của botA.
- **Dữ liệu nhập:** 3 request: (a) KHÔNG header X-Line-Signature; (b) X-Line-Signature rỗng; (c) X-Line-Signature=`AAAAsai==`.
- **Các bước:** 1) POST /line/callback/add/{botA} 2) Sau mỗi request kiểm chat/tag/scenario/queue.
- **Kết quả mong đợi:** Cả 3 → 401, chặn TRƯỚC xử lý; không tạo chat, không gắn tag, không chạy scenario, không đẩy job.

**C05-02** — Chữ ký đúng body gốc (positive)
- **Tiền điều kiện:** Biết channel_secret botA.
- **Dữ liệu nhập:** X-Line-Signature = base64(HMAC-SHA256(body, channel_secret_botA)) đúng.
- **Các bước:** POST với chữ ký đúng.
- **Kết quả mong đợi:** 200; webhook hợp lệ chạy bình thường (chat/auto-reply).

**C05-03** — Sửa body sau khi ký
- **Tiền điều kiện:** Có chữ ký đúng cho body gốc.
- **Dữ liệu nhập:** Ký body gốc → đổi text trong body → gửi (chữ ký cũ).
- **Các bước:** POST body đã sửa.
- **Kết quả mong đợi:** 401 — chữ ký không khớp body đã sửa.

**C05-04** — Chữ ký bot A gửi tới bot B
- **Tiền điều kiện:** Biết secret botA; botB bot_id tuần tự.
- **Dữ liệu nhập:** Chữ ký ký bằng secret_botA, gửi tới /line/callback/add/{botB}.
- **Các bước:** POST.
- **Kết quả mong đợi:** 401 — secret B khác A.

**C05-05** — Biến thể message/follow/postback
- **Tiền điều kiện:** Như C05-01.
- **Dữ liệu nhập:** Event type: message, follow, postback — đều sai chữ ký.
- **Các bước:** POST từng loại, kiểm welcome/scenario/postback.
- **Kết quả mong đợi:** Mọi loại event sai chữ ký đều bị chặn, không kích hoạt xử lý.


## C06. SQL Injection qua nội dung tin nhắn LINE (auto-reply)
`Critical` · Đối tượng: **End user / Người lạ** · Đợt: P0.3 · Nguồn: audit SEC-06 (Likely) — xem task #43398  
Vị trí/endpoint: `HandleCallbackMessage.php:436; BotController.php:3563`

**C06-01** — Xác nhận worker/command còn chạy
- **Tiền điều kiện:** Quyền kiểm process staging / hỏi dev-ops.
- **Dữ liệu nhập:** Kiểm supervisor/queue + command HandleCallbackMessage.
- **Các bước:** Xác minh command/worker có chạy ở prod/staging.
- **Kết quả mong đợi:** Nếu KHÔNG chạy → ghi Blocked/Chưa xác minh (không Pass). Nếu chạy → tiếp C06-02.

**C06-02** — Ký tự SQL/Unicode
- **Tiền điều kiện:** Worker chạy; autoreply keyword 'hello'.
- **Dữ liệu nhập:** Tin LINE: `O'Reilly` · `"` · `admin'--` · `１＝１`(fullwidth) · emoji.
- **Các bước:** Gửi qua LINE thật tới botA; theo dõi log DB/job.
- **Kết quả mong đợi:** Tin xử lý như văn bản; không lỗi SQL; auto-reply vẫn khớp đúng.

**C06-03** — Payload SQLi time-based
- **Tiền điều kiện:** Như C06-02.
- **Dữ liệu nhập:** `' or sleep(5)-- -` · `' AND (SELECT 1 FROM (SELECT SLEEP(5))x)-- -` · `test' UNION SELECT NULL-- -`.
- **Các bước:** Gửi; đo thời gian xử lý worker/phản hồi.
- **Kết quả mong đợi:** Không delay ~5s; không đổi dữ liệu; không lộ lỗi SQL.

**C06-04** — Keyword khớp/không khớp + theo dõi lỗi
- **Tiền điều kiện:** Autoreply có keyword.
- **Dữ liệu nhập:** Tin khớp keyword & tin chứa payload không khớp.
- **Các bước:** Gửi cả 2; theo dõi DB/job log.
- **Kết quả mong đợi:** Logic khớp đúng; payload không làm sai truy vấn; log sạch.


## C07. SQL Injection ở trang đặt chỗ sự kiện công khai (quantity)
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.3 (đề xuất nâng P0.1) · Nguồn: audit SEC-07 (Confirmed)  
Vị trí/endpoint: `MobileEventBookingController.php:653,664 · POST /ajax/booking-event/change-booking (không auth)`

**C07-01** — Int hợp lệ + boundary (positive)
- **Tiền điều kiện:** Event test tồn chỗ max=10, có giá/slot xác định.
- **Dữ liệu nhập:** quantity/number_order = 1 và = 10 (max tồn).
- **Các bước:** POST change-booking; kiểm booking + tổng tiền.
- **Kết quả mong đợi:** Nhận, cập nhật đúng, tổng tiền đúng.

**C07-02** — Giá trị bất thường
- **Tiền điều kiện:** Như C07-01.
- **Dữ liệu nhập:** 0 · -1 · 1.5 · `abc` · null · `[]`(mảng) · 99999999999.
- **Các bước:** POST từng giá trị.
- **Kết quả mong đợi:** Validate từ chối (integer|min:1|max tồn); không 500; không đổi booking.

**C07-03** — SQLi time-based
- **Tiền điều kiện:** Như C07-01.
- **Dữ liệu nhập:** `1)) >= 0 or sleep(5) or ((1` · `1 or sleep(5)` · `1;SELECT SLEEP(5)`.
- **Các bước:** POST, đo thời gian phản hồi.
- **Kết quả mong đợi:** Không delay ~5s; input bị validate/ép (int); không thực thi SQL.

**C07-04** — Đối chiếu sau request bị từ chối
- **Tiền điều kiện:** Đã chạy C07-02/03.
- **Dữ liệu nhập:** Truy vấn lại booking / tồn chỗ / tổng tiền.
- **Các bước:** So sánh trước-sau.
- **Kết quả mong đợi:** Không thay đổi — không ghi nhận booking từ input sai.


## C08. Callback Telecom cho phép đánh dấu 'đã thanh toán' giả
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.1 · Nguồn: audit SEC-08 (Confirmed)  
Vị trí/endpoint: `Customers.php:300-410 · /customer/telecom_callback_*.php (web.php:3799-3801)`

**C08-01** — Callback giả cho payment pending
- **Tiền điều kiện:** Payment pending P_pending của shopA.
- **Dữ liệu nhập:** POST telecom_callback với rel=yes, payment_id=P_pending.
- **Các bước:** Gửi callback giả; kiểm trạng thái payment + hoa hồng.
- **Kết quả mong đợi:** P_pending KHÔNG chuyển 'đã trả'; không ghi hoa hồng.

**C08-02** — Thiếu/sai xác thực nguồn
- **Tiền điều kiện:** P_pending.
- **Dữ liệu nhập:** Callback từ IP ngoài whitelist / thiếu tham số ký.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối (403); không tác động.

**C08-03** — Sai payment/amount/status
- **Tiền điều kiện:** P_pending.
- **Dữ liệu nhập:** payment_id không tồn tại · amount khác đơn · status lạ.
- **Các bước:** Gửi từng biến thể.
- **Kết quả mong đợi:** Từ chối; không ghi nhận thanh toán.

**C08-04** — make_form_telecom lộ hash người khác
- **Tiền điều kiện:** Payment P_other của shopB.
- **Dữ liệu nhập:** GET /make_form_telecom/{P_other}.
- **Các bước:** Truy cập route public với id của shop khác.
- **Kết quả mong đợi:** Không trả hash/thông tin payment shop khác (route nên gỡ/bắt auth).

**C08-05** — Sandbox hợp lệ + gửi lặp
- **Tiền điều kiện:** Callback sandbox đúng.
- **Dữ liệu nhập:** Callback hợp lệ gửi 2 lần.
- **Các bước:** Gửi lần 1, lần 2.
- **Kết quả mong đợi:** Lần 1 ghi nhận đúng; lần 2 không tạo tác động trùng (idempotent).


## C09. WebSocket không xác thực – nghe chat realtime mọi shop
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.1 · Nguồn: audit SEC-09 (Confirmed)  
Vị trí/endpoint: `node_serve/server.js:53-67,120-126`

**C09-01** — Token sai/thiếu/hết hạn
- **Tiền điều kiện:** Endpoint socket.io; JWT hợp lệ userA (quyền botA) để so sánh.
- **Dữ liệu nhập:** connect: (a) không token; (b) token=`abc`; (c) JWT hết hạn.
- **Các bước:** Thử connect từng biến thể.
- **Kết quả mong đợi:** Bị từ chối kết nối / không join được room nào.

**C09-02** — Không botCode → room legacy
- **Tiền điều kiện:** userA token hợp lệ.
- **Dữ liệu nhập:** connect không gửi botCode.
- **Các bước:** Connect, chờ event.
- **Kết quả mong đợi:** Không vào room 'legacy'; không nhận event tin nhắn chung.

**C09-03** — userA join room botB
- **Tiền điều kiện:** userA chỉ quyền botA.
- **Dữ liệu nhập:** emit join-room với botB.
- **Các bước:** Join rồi quan sát.
- **Kết quả mong đợi:** Bị từ chối join; không nhận event botB.

**C09-04** — typing/join-room-typing tới room B
- **Tiền điều kiện:** userA chỉ quyền botA.
- **Dữ liệu nhập:** emit `typing` / `join-room-typing` với room botB.
- **Các bước:** Emit rồi kiểm phía botB.
- **Kết quả mong đợi:** Không phát được dữ liệu vào room B.

**C09-05** — Chat đồng thời A/B — kiểm metadata
- **Tiền điều kiện:** Tạo chat thật ở botA và botB.
- **Dữ liệu nhập:** userA lắng nghe toàn bộ event.
- **Các bước:** Sinh tin nhắn 2 bot; ghi lại event userA nhận.
- **Kết quả mong đợi:** userA chỉ nhận event botA; nội dung/metadata botB không rò.

**C09-06** — Thu hồi quyền rồi reconnect
- **Tiền điều kiện:** userA đang có quyền botA.
- **Dữ liệu nhập:** Gỡ quyền botA của userA → userA reconnect/join lại.
- **Các bước:** Reconnect sau khi bị gỡ.
- **Kết quả mong đợi:** Không còn nhận event botA sau thu hồi.


## C10. Upload file tùy ý qua form trả lời công khai (nguy cơ RCE)
`Critical` · Đối tượng: **Người lạ / End user** · Đợt: P0.1 · Nguồn: audit SEC-10 (Confirmed, RCE phụ thuộc cấu hình)  
Vị trí/endpoint: `FormAnswerController.php:6111-6160; functions.php:766-787 · /ajax/render/upload-image-form-answer`

**C10-01** — Upload hợp lệ (positive)
- **Tiền điều kiện:** Form public bật upload.
- **Dữ liệu nhập:** ok.png.
- **Các bước:** Upload; truy cập URL trả về.
- **Kết quả mong đợi:** Upload thành công; URL hiển thị ảnh.

**C10-02** — .php/.html/.svg
- **Tiền điều kiện:** Như C10-01.
- **Dữ liệu nhập:** shell.php · x.html · y.svg.
- **Các bước:** Upload từng file.
- **Kết quả mong đợi:** Bị chặn theo whitelist; không lưu vào public/media.

**C10-03** — Đuôi kép/hoa/giả MIME/đổi tên
- **Tiền điều kiện:** Như C10-01.
- **Dữ liệu nhập:** ok.php.png · SHELL.PHP · evil.php (Content-Type image/png) · ảnh thật đổi tên .php.
- **Các bước:** Upload từng biến thể.
- **Kết quả mong đợi:** Chặn hết; không lưu file thực thi được.

**C10-04** — URL file bị từ chối
- **Tiền điều kiện:** Đoán được path lưu (vd /media/...).
- **Dữ liệu nhập:** GET URL của file vừa bị từ chối ở C10-02/03.
- **Các bước:** Truy cập URL đoán.
- **Kết quả mong đợi:** Không truy cập được bản nào của file bị từ chối (không lưu ngầm).

**C10-05** — Media không exec PHP (dev/ops)
- **Tiền điều kiện:** Quyền đặt file trong public/media (manual).
- **Dữ liệu nhập:** Đặt test.php trong public/media (kể cả file cũ trước vá).
- **Các bước:** GET /media/test.php.
- **Kết quả mong đợi:** Web server trả text/download, KHÔNG thực thi PHP (manual, cấu hình nginx).


## C11. API /api/unfollow-line xóa hội thoại/tin/tag bot bất kỳ
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.2 · Nguồn: audit SEC-11 (Confirmed)  
Vị trí/endpoint: `LineApiController.php:23 · routes/api.php:21`

**C11-01** — No-auth gửi cặp bot/user test
- **Tiền điều kiện:** botA có lineA (chat/msg/tag); snapshot trước.
- **Dữ liệu nhập:** POST /api/unfollow-line {bot_id=botA, line_id=lineA} không token.
- **Các bước:** Gửi; so dữ liệu trước/sau.
- **Kết quả mong đợi:** Từ chối (401/403); chat/msg/tag lineA còn nguyên.

**C11-02** — Auth sai
- **Tiền điều kiện:** Như C11-01.
- **Dữ liệu nhập:** Kèm token/secret sai.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối.

**C11-03** — Trộn botA + lineB
- **Tiền điều kiện:** lineB thuộc botB.
- **Dữ liệu nhập:** {bot_id=botA, line_id=lineB}.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối / không xóa (lineB không thuộc botA).

**C11-04** — Đối chiếu trước/sau
- **Tiền điều kiện:** Snapshot chat/msg/tag.
- **Dữ liệu nhập:** Các request trái phép ở trên.
- **Các bước:** So snapshot trước-sau.
- **Kết quả mong đợi:** Không thay đổi.

**C11-05** — Unfollow hợp lệ (nếu giữ endpoint)
- **Tiền điều kiện:** Luồng unfollow chính thống.
- **Dữ liệu nhập:** Callback LINE unfollow hợp lệ.
- **Các bước:** Chạy luồng hợp lệ.
- **Kết quả mong đợi:** Chỉ xử lý đúng phạm vi hợp lệ.


## C12. User thường gọi được API SuperAdmin (đổi bank affiliate)
`Critical` · Đối tượng: **User shop** · Đợt: P0.2 · Nguồn: audit SEC-12 (Confirmed)  
Vị trí/endpoint: `SupperAdminController.php (56,82,125,167,201,369) · web.php:3718`

**C12-01** — Từng vai trò gọi từng endpoint
- **Tiền điều kiện:** 6 endpoint /ajax/supper-admin/*.
- **Dữ liệu nhập:** Vai trò: ẩn danh · owner shop · staff.
- **Các bước:** Mỗi vai trò gọi 6 endpoint.
- **Kết quả mong đợi:** Tất cả bị chặn trừ supper_admin.

**C12-02** — Đổi bank/hoa hồng/affiliate/xem bot-staff
- **Tiền điều kiện:** Affiliate B có bank account.
- **Dữ liệu nhập:** POST đổi STK affiliate B · đổi % hoa hồng · tự đăng ký affiliate · GET bot/staff user khác.
- **Các bước:** Owner/staff thử từng chức năng; đối chiếu dữ liệu tài chính.
- **Kết quả mong đợi:** Bị chặn; không đổi dữ liệu/tài chính.

**C12-03** — SuperAdmin hợp lệ (positive)
- **Tiền điều kiện:** Đăng nhập supper_admin.
- **Dữ liệu nhập:** Nghiệp vụ hợp lệ.
- **Các bước:** Thao tác đúng quyền.
- **Kết quả mong đợi:** Chạy bình thường.


## C13. Ghi đè channel token/secret bot shop khác (chiếm bot)
`Critical` · Đối tượng: **User shop** · Đợt: P0.2 · Nguồn: audit SEC-13 (Confirmed)  
Vị trí/endpoint: `BotController.php:787-799,1150-1212 · POST /admin/bot-save`

**C13-01** — A sửa B bằng id/hash B
- **Tiền điều kiện:** owner A đăng nhập; biết hashB; snapshot botB trước.
- **Dữ liệu nhập:** bot-save {hashid=hashB, channel_access_token='A_ctrl', channel_secret='A_ctrl'}.
- **Các bước:** POST; so token/secret botB.
- **Kết quả mong đợi:** Từ chối; token/secret botB KHÔNG đổi.

**C13-02** — Staff không quyền sửa token
- **Tiền điều kiện:** staff của A.
- **Dữ liệu nhập:** bot-save sửa token.
- **Các bước:** POST.
- **Kết quả mong đợi:** Từ chối.

**C13-03** — Đối chiếu B trước/sau
- **Tiền điều kiện:** Snapshot token/secret/webhook/BotUsers botB.
- **Dữ liệu nhập:** Các request trên.
- **Các bước:** So trước-sau.
- **Kết quả mong đợi:** Không thay đổi/không reset BotUsers.

**C13-04** — Owner sửa bot mình (positive)
- **Tiền điều kiện:** owner B đăng nhập.
- **Dữ liệu nhập:** bot-save botB hợp lệ.
- **Các bước:** POST.
- **Kết quả mong đợi:** Lưu thành công.


## C14. Lấy list bot (kèm LINE token) của user bất kỳ, không đăng nhập
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.1 · Nguồn: audit SEC-14 (Confirmed)  
Vị trí/endpoint: `UserController.php:4872 · POST /ajax/employees-management/get-list-bot-access (web.php:3768)`

**C14-01** — No-auth + quét id tuần tự
- **Tiền điều kiện:** User id tuần tự 1..N.
- **Dữ liệu nhập:** Ẩn danh POST {id=1},{id=2}...{id=N}.
- **Các bước:** Quét dải id.
- **Kết quả mong đợi:** Từ chối (chưa đăng nhập); không trả bot list + token.

**C14-02** — A truyền id B
- **Tiền điều kiện:** owner A đăng nhập.
- **Dữ liệu nhập:** POST {id=userB}.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối / không trả bot của B.

**C14-03** — A lấy list của mình (positive)
- **Tiền điều kiện:** owner A.
- **Dữ liệu nhập:** POST {id=userA}.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Trả bot được phép của A (chức năng ok).

**C14-04** — Kiểm field response
- **Tiền điều kiện:** Response thành công C14-03.
- **Dữ liệu nhập:** Soi field.
- **Các bước:** Kiểm từng field.
- **Kết quả mong đợi:** Không chứa channel_access_token/secret dư thừa.


## C15. API kiểm tra bước tạo bot trả nguyên bản ghi bot người khác
`Critical` · Đối tượng: **User shop** · Đợt: P0.2 · Nguồn: audit SEC-15 (Confirmed)  
Vị trí/endpoint: `BotController.php:7114-7214; UserController.php:396-499 · web.php:191,2002-2003`

**C15-01** — A truyền bot B vào từng endpoint
- **Tiền điều kiện:** owner A; botB id tuần tự.
- **Dữ liệu nhập:** bot_id=botB tại step3-check · step5-check · bot/check-mode.
- **Các bước:** Gọi 3 endpoint.
- **Kết quả mong đợi:** Từ chối; không trả full model.

**C15-02** — Bot id không tồn tại
- **Tiền điều kiện:** —
- **Dữ liệu nhập:** bot_id=999999.
- **Các bước:** Gọi.
- **Kết quả mong đợi:** Lỗi xử lý gọn; không 500 lộ thông tin.

**C15-03** — Owner/staff hợp lệ (positive)
- **Tiền điều kiện:** owner B.
- **Dữ liệu nhập:** bot_id=botB.
- **Các bước:** Gọi luồng check.
- **Kết quả mong đợi:** Luồng check chạy.

**C15-04** — Kiểm response success/error
- **Tiền điều kiện:** Response của C15-01/03.
- **Dữ liệu nhập:** Soi response.
- **Các bước:** Kiểm trường trả về.
- **Kết quả mong đợi:** Không có token/secret/key_chatgpt trong response.


## C16. Chuyển 'bot hiện tại' trong session sang bot bất kỳ
`Critical` · Đối tượng: **User shop** · Đợt: P0.2 · Nguồn: audit SEC-16 (Confirmed gán session / Likely ajax)  
Vị trí/endpoint: `ListFriendController.php (index); BasicAccess.php nhánh basicHome`

**C16-01** — A mở list-friend hash B
- **Tiền điều kiện:** owner A; hashB.
- **Dữ liệu nhập:** GET /list-friend/{hashB}.
- **Các bước:** Mở trang.
- **Kết quả mong đợi:** Từ chối trước khi gán session; không hiển thị bạn bè B.

**C16-02** — Kiểm session + gọi ajax sau khi bị từ chối
- **Tiền điều kiện:** Sau C16-01.
- **Dữ liệu nhập:** Gọi /ajax/* (friend/chat/tag list).
- **Các bước:** Quan sát bot nào được dùng.
- **Kết quả mong đợi:** Session vẫn botA (hoặc không bot); ajax không trả dữ liệu botB.

**C16-03** — Thao tác ghi trên dữ liệu B
- **Tiền điều kiện:** Sau C16-01.
- **Dữ liệu nhập:** POST sửa tag/memo của botB qua ajax.
- **Các bước:** Gửi ghi.
- **Kết quả mong đợi:** Bị chặn.

**C16-04** — Nhiều tab
- **Tiền điều kiện:** owner A.
- **Dữ liệu nhập:** tab1 botA, tab2 mở /list-friend/{hashB}.
- **Các bước:** Thao tác xen kẽ 2 tab.
- **Kết quả mong đợi:** Không nhiễm session chéo; tab1 vẫn botA.

**C16-05** — Staff chuyển bot có quyền (positive)
- **Tiền điều kiện:** staff có quyền botA & botC.
- **Dữ liệu nhập:** Chuyển qua lại botA/botC.
- **Các bước:** Mở list-friend từng bot.
- **Kết quả mong đợi:** Chạy bình thường.


## C17. API mobile nhận botId từ client – đọc chat/gửi tin thay bot khác
`Critical` · Đối tượng: **User shop (app mobile)** · Đợt: P0.2 · Nguồn: audit SEC-17 (Confirmed)  
Vị trí/endpoint: `Api/ChatController.php:132,1911,2671,5064,5185,5387 · /api/mobile/chat/*`

**C17-01** — tokenA + botIdCurrent B
- **Tiền điều kiện:** token userA (quyền botA); convB thuộc botB.
- **Dữ liệu nhập:** Header token A; body botIdCurrent=botB; gọi get chat list.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối / không trả chat botB.

**C17-02** — botA + conversationId B
- **Tiền điều kiện:** Như C17-01.
- **Dữ liệu nhập:** botIdCurrent=botA, conversationId=convB.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối (conversation không thuộc botA).

**C17-03** — Cả bot & conversation B
- **Tiền điều kiện:** Như C17-01.
- **Dữ liệu nhập:** botIdCurrent=botB, conversationId=convB.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối (token A không quyền botB).

**C17-04** — Đọc chat/gửi tin
- **Tiền điều kiện:** Như trên.
- **Dữ liệu nhập:** get-messages + send message tới convB.
- **Các bước:** Thử đọc & gửi.
- **Kết quả mong đợi:** Không đọc/gửi được thay bot B.

**C17-05** — Owner/staff mobile hợp lệ (positive)
- **Tiền điều kiện:** userA + botA/convA.
- **Dữ liệu nhập:** Thao tác hợp lệ.
- **Các bước:** Đọc/gửi convA.
- **Kết quả mong đợi:** Chạy bình thường.


## C18. Xóa vĩnh viễn đơn/booking theo id, không đăng nhập
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.2 · Nguồn: audit SEC-18 (Confirmed)  
Vị trí/endpoint: `SalesManagementV2Controller.php:5203; CalendarController.php:1396; CalendarSalonController.php:2182; MobileEventBookingController.php:1653`

**C18-01** — Đủ 4 loại bản ghi
- **Tiền điều kiện:** Tạo bản ghi test: product order / lesson / salon / event của shopB.
- **Dữ liệu nhập:** Gọi mỗi endpoint delete-*-confirm-fail với id test.
- **Các bước:** Chạy đủ 4 loại.
- **Kết quả mong đợi:** Thiết lập nền cho C18-02..05 (mỗi loại test đủ biến thể).

**C18-02** — No-auth / token sai / A xóa B (quét id)
- **Tiền điều kiện:** id tuần tự của shopB.
- **Dữ liệu nhập:** Ẩn danh forceDelete id của shopB · token sai · ownerA xóa id B · quét id 1..N.
- **Các bước:** Gửi từng biến thể; kiểm bản ghi B.
- **Kết quả mong đợi:** Từ chối; bản ghi B còn nguyên.

**C18-03** — Các trạng thái pending/success/paid/cancelled
- **Tiền điều kiện:** Bản ghi ở 4 trạng thái.
- **Dữ liệu nhập:** Thử xóa từng trạng thái.
- **Các bước:** Gọi delete.
- **Kết quả mong đợi:** Không xóa bản ghi đã thanh toán/đã xác nhận; chỉ pending-mới-tạo-của-chính-mình (nếu hợp lệ).

**C18-04** — Cleanup hợp lệ + gửi lặp (positive)
- **Tiền điều kiện:** End user đã xác thực sở hữu bản pending.
- **Dữ liệu nhập:** Xóa đúng bản pending của mình; gửi lặp.
- **Các bước:** Gọi 2 lần.
- **Kết quả mong đợi:** Xóa 1 lần; lặp không lỗi/không tác động thêm.

**C18-05** — Tồn chỗ/tồn kho + job
- **Tiền điều kiện:** Sau các thao tác xóa.
- **Dữ liệu nhập:** Kiểm tồn chỗ/tồn kho + job liên quan.
- **Các bước:** Đối chiếu số liệu + job log.
- **Kết quả mong đợi:** Không hoàn tồn 2 lần; job không chạy sai.


## C19. Hủy subscription (đơn định kỳ) của bất kỳ ai
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.2 · Nguồn: audit SEC-19 (Confirmed)  
Vị trí/endpoint: `SalesManagementV2Controller.php:1225; SalesManagementController.php:1333 · /ajax/(mobile/)cancel-cycle-order`

**C19-01** — Cả 2 biến thể cancel-cycle-order
- **Tiền điều kiện:** subB của shopB; cycle_order_id tuần tự.
- **Dữ liệu nhập:** Gọi cả /ajax/cancel-cycle-order & /ajax/mobile/cancel-cycle-order.
- **Các bước:** Chạy đủ 2 biến thể cho các case dưới.
- **Kết quả mong đợi:** Nền cho C19-02..06.

**C19-02** — Không session
- **Tiền điều kiện:** subB.
- **Dữ liệu nhập:** Ẩn danh POST {cycle_order_id=subB}.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối; sub B không hủy.

**C19-03** — Session A hủy B (quét id)
- **Tiền điều kiện:** owner A.
- **Dữ liệu nhập:** POST {cycle_order_id=subB}; quét id tuần tự.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối.

**C19-04** — Token thiếu/sai/hết hạn
- **Tiền điều kiện:** subB.
- **Dữ liệu nhập:** Các biến thể token.
- **Các bước:** Gửi.
- **Kết quả mong đợi:** Từ chối.

**C19-05** — Chủ hủy hợp lệ + lặp (positive)
- **Tiền điều kiện:** Chủ sub.
- **Dữ liệu nhập:** Hủy đúng; gửi lặp.
- **Các bước:** Gọi 2 lần.
- **Kết quả mong đợi:** Hủy 1 lần; lặp không tác động trùng.

**C19-06** — Đối chiếu nội bộ + cổng sandbox
- **Tiền điều kiện:** Sub hủy hợp lệ.
- **Dữ liệu nhập:** So DB nội bộ vs Univapay/Stripe sandbox.
- **Các bước:** Đối chiếu 2 phía.
- **Kết quả mong đợi:** Trạng thái 2 phía nhất quán.


## C20. File credential bị commit vào git, 1 file tải được qua web
`Critical` · Đối tượng: **Người lạ / người có source** · Đợt: P0.1 · Nguồn: audit SEC-20 (Confirmed)  
Vị trí/endpoint: `public/client_secret.json, public/dev_secret.json, storage/credentials_dev.json, storage/snsline-lme-firebase-adminsdk-*.json`

**C20-01** — Truy cập URL trực tiếp
- **Tiền điều kiện:** Biết tên file credential.
- **Dữ liệu nhập:** GET https://<host>/client_secret.json.
- **Các bước:** Truy cập URL.
- **Kết quả mong đợi:** 404 — không tải được.

**C20-02** — Bản deploy còn credential/backup
- **Tiền điều kiện:** Quyền kiểm deploy.
- **Dữ liệu nhập:** Rà thư mục deploy + backup.
- **Các bước:** Liệt kê file.
- **Kết quả mong đợi:** Không còn file credential trong public/.

**C20-03** — Git history + rotate (dev/ops)
- **Tiền điều kiện:** Quyền repo (manual).
- **Dữ liệu nhập:** git log --all cho từng file; rotate key.
- **Các bước:** Xóa history + rotate.
- **Kết quả mong đợi:** Đã xóa khỏi history + rotate.

**C20-04** — Credential cũ mất hiệu lực
- **Tiền điều kiện:** Đã rotate.
- **Dữ liệu nhập:** Dùng Google OAuth secret cũ / Firebase key cũ gọi API.
- **Các bước:** Thử key cũ.
- **Kết quả mong đợi:** Bị từ chối (đã revoke).

**C20-05** — Chức năng với key mới (positive)
- **Tiền điều kiện:** Key mới cấu hình.
- **Dữ liệu nhập:** Tính năng dùng Google/Firebase.
- **Các bước:** Chạy chức năng.
- **Kết quả mong đợi:** Hoạt động bình thường.


## X01. Chuỗi: webhook LINE sai chữ ký → auto-reply/scenario/postback/booking
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.3 · Nguồn: audit (combo)  
Vị trí/endpoint: `C05 + C06`

**X01** — Chain webhook sai chữ ký
- **Tiền điều kiện:** C05 đã vá.
- **Dữ liệu nhập:** Webhook sai chữ ký kèm payload kích hoạt scenario/postback/đổi booking.
- **Các bước:** Gửi → kiểm chat/scenario/booking/queue.
- **Kết quả mong đợi:** Không xử lý nghiệp vụ, không job nền.


## X02. Chuỗi: đổi session sang bot B → đọc friend/chat và ghi dữ liệu B
`Critical` · Đối tượng: **User shop** · Đợt: P0.3 · Nguồn: audit (combo)  
Vị trí/endpoint: `C16 + /ajax/*`

**X02** — Chain session switch
- **Tiền điều kiện:** C16.
- **Dữ liệu nhập:** Mở /list-friend/{hashB} → gọi chuỗi ajax friend/chat + ghi tag/memo.
- **Các bước:** Thực hiện chuỗi.
- **Kết quả mong đợi:** Session và mọi API tiếp theo giữ đúng giới hạn quyền.


## X03. Chuỗi: trang đã bỏ secret → kiểm credential cũ sau rotate
`Critical` · Đối tượng: **Người lạ** · Đợt: P0.3 · Nguồn: audit (combo)  
Vị trí/endpoint: `C03/C04 + rotate`

**X03** — Chain secret rotate
- **Tiền điều kiện:** Đã gỡ secret + rotate.
- **Dữ liệu nhập:** Dùng secret cũ lấy từ trang trước đây.
- **Các bước:** Thử secret cũ với cổng thanh toán.
- **Kết quả mong đợi:** Secret cũ mất hiệu lực.


## X04. Chuỗi: upload → truy cập URL file
`Critical` · Đối tượng: **Người lạ / End user** · Đợt: P0.3 · Nguồn: audit (combo)  
Vị trí/endpoint: `C10`

**X04** — Chain upload→access
- **Tiền điều kiện:** C10.
- **Dữ liệu nhập:** Upload (bị chặn) → đoán URL → GET.
- **Các bước:** Thực hiện chuỗi.
- **Kết quả mong đợi:** Không thực thi mã / không phục vụ nội dung nguy hiểm; file hợp lệ vẫn dùng được.


## X05. Chuỗi: request bị từ chối → kiểm DB/queue/dịch vụ ngoài
`Critical` · Đối tượng: **—** · Đợt: P0.3 · Nguồn: audit (combo)  
Vị trí/endpoint: `mọi case ghi/xóa`

**X05** — Chain side-effect
- **Tiền điều kiện:** Bất kỳ case ghi/xóa.
- **Dữ liệu nhập:** Request trái phép bị 4xx.
- **Các bước:** Sau response lỗi, kiểm DB/queue/dịch vụ ngoài.
- **Kết quả mong đợi:** Không có tác động trước hoặc sau response lỗi.


## U01. Univapay: callback thiếu/sai xác thực
`High` · Đối tượng: **Người lạ** · Đợt: P0.1 (đi cùng C08) · Nguồn: audit High (Confirmed)  
Vị trí/endpoint: `WebhookUnivapayControler.php:11-41; BotController.php:12260+; SalesManagementV2Controller.php:4176; SalesService.php:125-160`

**U01** — Univapay: callback thiếu/sai xác thực
- **Tiền điều kiện:** Đơn O_pending của shopA; webhook Univapay charge_finished.
- **Dữ liệu nhập:** POST charge_finished thiếu/sai auth token webhook.
- **Các bước:** Gửi callback; đối chiếu đơn + cổng sandbox.
- **Kết quả mong đợi:** Bị từ chối; đơn/booking/hợp đồng không đổi.


## U02. Univapay: charge không tồn tại / không thuộc đơn
`High` · Đối tượng: **Người lạ** · Đợt: P0.1 (đi cùng C08) · Nguồn: audit High (Confirmed)  
Vị trí/endpoint: `WebhookUnivapayControler.php:11-41; BotController.php:12260+; SalesManagementV2Controller.php:4176; SalesService.php:125-160`

**U02** — Univapay: charge không tồn tại / không thuộc đơn
- **Tiền điều kiện:** Đơn O_pending của shopA; webhook Univapay charge_finished.
- **Dữ liệu nhập:** charge_id không tồn tại hoặc không thuộc đơn O_pending.
- **Các bước:** Gửi callback; đối chiếu đơn + cổng sandbox.
- **Kết quả mong đợi:** Không ghi nhận thanh toán.


## U03. Univapay: sai số tiền/tiền tệ/trạng thái
`High` · Đối tượng: **Người lạ** · Đợt: P0.1 (đi cùng C08) · Nguồn: audit High (Confirmed)  
Vị trí/endpoint: `WebhookUnivapayControler.php:11-41; BotController.php:12260+; SalesManagementV2Controller.php:4176; SalesService.php:125-160`

**U03** — Univapay: sai số tiền/tiền tệ/trạng thái
- **Tiền điều kiện:** Đơn O_pending của shopA; webhook Univapay charge_finished.
- **Dữ liệu nhập:** status=successful nhưng amount/currency khác đơn.
- **Các bước:** Gửi callback; đối chiếu đơn + cổng sandbox.
- **Kết quả mong đợi:** Không ghi nhận thanh toán thành công.


## U04. Univapay: callback sandbox hợp lệ (positive)
`High` · Đối tượng: **Người lạ** · Đợt: P0.1 (đi cùng C08) · Nguồn: audit High (Confirmed)  
Vị trí/endpoint: `WebhookUnivapayControler.php:11-41; BotController.php:12260+; SalesManagementV2Controller.php:4176; SalesService.php:125-160`

**U04** — Univapay: callback sandbox hợp lệ (positive)
- **Tiền điều kiện:** Đơn O_pending của shopA; webhook Univapay charge_finished.
- **Dữ liệu nhập:** Callback sandbox đúng với charge thật.
- **Các bước:** Gửi callback; đối chiếu đơn + cổng sandbox.
- **Kết quả mong đợi:** Đối chiếu GET /charges/{id} + cập nhật đúng đơn.


## U05. Univapay: gửi lặp callback hợp lệ
`High` · Đối tượng: **Người lạ** · Đợt: P0.1 (đi cùng C08) · Nguồn: audit High (Confirmed)  
Vị trí/endpoint: `WebhookUnivapayControler.php:11-41; BotController.php:12260+; SalesManagementV2Controller.php:4176; SalesService.php:125-160`

**U05** — Univapay: gửi lặp callback hợp lệ
- **Tiền điều kiện:** Đơn O_pending của shopA; webhook Univapay charge_finished.
- **Dữ liệu nhập:** Callback hợp lệ gửi 2 lần.
- **Các bước:** Gửi callback; đối chiếu đơn + cổng sandbox.
- **Kết quả mong đợi:** Không tạo tác động tài chính/nghiệp vụ trùng.


## C21. Master password PASS_LOGIN đăng nhập mọi tài khoản
`High` · Đối tượng: **Người biết mật khẩu chung** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (G1)  
Vị trí/endpoint: `AuthController.php:145-149; Api/AuthMobileController.php:224; Mobile/LoginMobileController.php:65; Affiliate/AffiliaterController.php:181; PointSettingController.php:670`

**C21** — Master password
- **Tiền điều kiện:** Biết giá trị PASS_LOGIN (hỏi dev staging); có owner A, staff A, affiliate X, mobile user M.
- **Dữ liệu nhập:** Đăng nhập username hợp lệ + password = <PASS_LOGIN> tại web /login, mobile login, affiliate login.
- **Các bước:** 1) Thử từng kênh 2) Kiểm log/alert 3) Thử password thật 4) Sau khi dev bỏ backdoor, thử lại PASS_LOGIN.
- **Kết quả mong đợi:** PASS_LOGIN bị từ chối mọi kênh; password thật vẫn đăng nhập; login-as chính thống có audit log.


## C22. Route /command chạy Artisan trên production
`High` · Đối tượng: **User shop** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (G2)  
Vị trí/endpoint: `RunTestCommandController.php:66-80 · web.php:4256`

**C22** — /command Artisan
- **Tiền điều kiện:** User thường đăng nhập + 1 lần ẩn danh.
- **Dữ liệu nhập:** GET/POST /command?type=auto_payment · type=delete_landing · type=delete_richmenu.
- **Các bước:** 1) Gọi từng type 2) Đối chiếu số dư/giao dịch tự động, landing, richmenu trước-sau 3) Kiểm route sau khi gỡ.
- **Kết quả mong đợi:** Không chạy Artisan qua web; không trừ tiền/xóa dữ liệu; route trả 404.


## C23. /b2/upload-url phát token Backblaze B2 cho bất kỳ ai
`High` · Đối tượng: **Người lạ** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (G3)  
Vị trí/endpoint: `closure routes/web.php:4263-4274`

**C23** — B2 upload token
- **Tiền điều kiện:** Ẩn danh.
- **Dữ liệu nhập:** GET /b2/upload-url → lấy uploadUrl + authorizationToken; dùng token upload test.html, test.js.
- **Các bước:** 1) Gọi lấy token (ẩn danh) 2) POST file lên uploadUrl.
- **Kết quả mong đợi:** Không phát token cho ẩn danh; không upload html/js lên CDN.


## C24. SQL Injection nhóm bộ lọc bạn bè (second-order)
`High` · Đối tượng: **User shop** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (G4)  
Vị trí/endpoint: `Conversation.php:427-959,1135-1660; FriendlistController.php:976,1200,3598,3602; FilterController.php:383-407; ChatController.php:5115; BroadcastV2Controller.php:231,299-303,653,689`

**C24** — SQLi filter
- **Tiền điều kiện:** owner A; có tag/scenario/conversion id; 1 broadcast lưu được.
- **Dữ liệu nhập:** tag_id/scenario_stop_id/conversion_id=`1 or sleep(5)` · number_date=`1 or sleep(5)` · point=`1)) or sleep(5)-- -` · arr_template_ids=`1),(SELECT SLEEP(5))-- -`.
- **Các bước:** 1) Gửi tới friendlist/export, post-advance-filter-v2, filter/get-list-user, chat/group, broadcast save 2) Đo time-based 3) Lưu filter rồi chạy job (send-action) test second-order 4) Thử UNION SELECT.
- **Kết quả mong đợi:** Ép int/binding; không delay ~5s; không lộ DB; filter lưu chạy an toàn trong job.


## C25. SQL Injection không auth ở MyPage (line_user_id)
`High` · Đối tượng: **Người lạ** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (G5)  
Vị trí/endpoint: `ChatController::getDataFormAnswerMyPage · /ajax/get_data_form_answer_my_page`

**C25** — SQLi no-auth MyPage
- **Tiền điều kiện:** Ẩn danh.
- **Dữ liệu nhập:** POST /ajax/get_data_form_answer_my_page line_user_id=`1 or sleep(5)` · `1 UNION SELECT NULL-- -`.
- **Các bước:** Gửi; đo time; kiểm có yêu cầu auth không.
- **Kết quả mong đợi:** Yêu cầu xác thực end user; ép int/binding; không thực thi SQL.


## C26. Path traversal tải .env / mã nguồn ở nhiều hàm download
`High` · Đối tượng: **Người lạ / User shop** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (G6)  
Vị trí/endpoint: `CsvManagementController.php:423-437; BookingEventController.php:3059; ImageRichmenuController.php:1238; ChatController.php:7649-7676 (download-img-info, no-auth); UserController.php:801; AffiliateInfoController.php:1375`

**C26** — Path traversal download
- **Tiền điều kiện:** Biết endpoint; file .env tồn tại.
- **Dữ liệu nhập:** ?fileName=../../.env tại csv export / booking event download / image richmenu download; GET /basic/download-img-info?...=/../.env (no-auth); admin user/affiliate download.
- **Các bước:** 1) Gọi từng endpoint 2) Thử tải file hợp lệ 3) Regression: grep toàn repo các hàm nhận path từ client.
- **Kết quả mong đợi:** basename/realpath chặn; auth bắt buộc; file hợp lệ vẫn tải.


## C27. Upload media dùng đuôi client ở nhiều controller (RCE/XSS)
`High` · Đối tượng: **User shop / Người lạ** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (G7)  
Vị trí/endpoint: `MessageTemplateController.php:1139-1180; Services/ChatService.php:911-1022; ChatController.php:2136-2245; Api/ChatController.php:886-993,4269 (upload_image_common no-auth, path2); MediaController.php`

**C27** — Upload đa controller
- **Tiền điều kiện:** Vai trò tương ứng (staff/owner) + /api/upload_image_common ẩn danh.
- **Dữ liệu nhập:** Upload shell.php/x.html/y.svg qua message template, chat service, chat, api chat; /api/upload_image_common với path2=`../../public`.
- **Các bước:** 1) Upload từng đường 2) Truy cập URL sau upload 3) Thử path2 traversal.
- **Kết quả mong đợi:** Chặn đuôi nguy hiểm ở MỌI đường; không exec; thư mục cố định.


## C28. Open redirect & chạy JS qua url_back (payment success)
`High` · Đối tượng: **Người lạ (gửi link)** · Đợt: P0/P1 (đề xuất) · Nguồn: Bổ sung review (G8)  
Vị trí/endpoint: `routes/web.php:4196-4211; payment_bot_success.blade.php:10-12`

**C28** — Open redirect url_back
- **Tiền điều kiện:** Nạn nhân admin đang đăng nhập.
- **Dữ liệu nhập:** ?url_back=`javascript:alert(document.cookie)` · `//evil.com` · `https://evil.com`.
- **Các bước:** Mở link payment success; quan sát redirect/JS.
- **Kết quả mong đợi:** Chỉ cho path nội bộ (/ không //); javascript:/host ngoài bị chặn.


## C29. Stored XSS câu trả lời form (v-html màn admin)
`High` · Đối tượng: **End user** · Đợt: P0/P1 (đề xuất) · Nguồn: Bổ sung review (G9)  
Vị trí/endpoint: `mypage_v2.blade.php:2276; my_page.js:1266-1330; answer_form_history.js:35-70`

**C29** — Stored XSS form
- **Tiền điều kiện:** Form public shopA; admin xem lịch sử trả lời.
- **Dữ liệu nhập:** answer=`<img src=x onerror=alert(document.cookie)>` · `<script>fetch('/ajax/bot-save',{method:'POST',...})</script>`.
- **Các bước:** 1) End user gửi form 2) Admin mở mypage_v2 / answer history.
- **Kết quả mong đợi:** Giá trị được escape; JS không chạy trong phiên admin/staff.


## C30. Miễn CSRF quá rộng cho /ajax/* và /admin/ajax/*
`High` · Đối tượng: **Trang web bên ngoài** · Đợt: P0/P1 (đề xuất) · Nguồn: Bổ sung review (G10)  
Vị trí/endpoint: `VerifyCsrfToken.php:14-54`

**C30** — CSRF too broad
- **Tiền điều kiện:** Admin đăng nhập ở tab khác.
- **Dữ liệu nhập:** Form HTML auto-POST tới /ajax/bot-save, /ajax/create-notification, /login, /change_password, /postReset — KHÔNG CSRF token.
- **Các bước:** Admin mở trang attacker; quan sát request có được chấp nhận không.
- **Kết quả mong đợi:** Thiếu CSRF token → chặn; chỉ webhook thật được miễn.


## C31. Booking Calendar cũ: xóa/sửa lịch–staff–khóa học + đọc chi tiết khách shop khác
`High` · Đối tượng: **User shop** · Đợt: P1 (đề xuất) · Nguồn: Bổ sung review (G11)  
Vị trí/endpoint: `BookingManagerController.php (525,544,582,846,1244,1802,1939,1985,2058,3781,2573,4074); BookingAjaxController.php:207`

**C31** — Booking calendar cũ IDOR
- **Tiền điều kiện:** owner A; botB có lịch/staff/khóa học + booking khách.
- **Dữ liệu nhập:** Các action BookingManager với bot_id=botB (xóa slot, sửa staff, xóa khóa học); GET chi tiết booking (2573/4074).
- **Các bước:** Gọi từng action; đối chiếu dữ liệu B + thông tin khách.
- **Kết quả mong đợi:** Lọc theo bot phiên; không chạm B; không lộ chi tiết khách B.


## C32. App mobile IDOR: friend/refund/booking/notify/tag/sales theo botId client
`High` · Đối tượng: **User shop (app mobile)** · Đợt: P1 (đề xuất) · Nguồn: Bổ sung review (G11)  
Vị trí/endpoint: `Api/FriendInformationController.php:438,895,955; Api/CalendarSalonController.php:909; Api/CalendarLessonController; Api/BookingCalendar.php:349,1244; Api/NotifyController; Api/TagController; Api/SalesController`

**C32** — App mobile IDOR
- **Tiền điều kiện:** token userA; dữ liệu botB (friend, salon/lesson order trả trước, booking, notify, tag, sales).
- **Dữ liệu nhập:** Các API với $request->botId=botB và line_id/booking_id của B.
- **Các bước:** Xóa/chặn bạn B · hoàn tiền/hủy đơn salon/lesson B · xóa booking B · đọc SĐT/email/địa chỉ · add/xóa tag.
- **Kết quả mong đợi:** Bot lấy từ token; owner/staff check; không thao tác/đọc dữ liệu B.


## C33. Popup: liệt kê/sửa/copy/xóa popup shop khác
`High` · Đối tượng: **User shop** · Đợt: P1 (đề xuất) · Nguồn: Bổ sung review (G11)  
Vị trí/endpoint: `Ajax/PopupAjaxController.php (32,455,510) · /ajax/popup/*`

**C33** — Popup IDOR
- **Tiền điều kiện:** owner A; botB có popup.
- **Dữ liệu nhập:** /ajax/popup/* list/edit/copy/delete với bot_id=botB.
- **Các bước:** Gọi từng action.
- **Kết quả mong đợi:** Lọc theo bot hiện tại (getBotIdInScope()); không chạm popup B.


## C34. Booking event LIFF: hủy/sửa booking khách khác (ghi đè SĐT/email)
`High` · Đối tượng: **End user** · Đợt: P1 (đề xuất) · Nguồn: Bổ sung review (G11)  
Vị trí/endpoint: `BookingEventController.php:2630,2710; MobileEventBookingController.php:1714`

**C34** — Booking event LIFF IDOR
- **Tiền điều kiện:** lineA đặt eventA; eventB của lineB.
- **Dữ liệu nhập:** PUT/POST sửa/hủy BBooking id của lineB; ghi đè phone/email.
- **Các bước:** lineA gọi với id booking của B.
- **Kết quả mong đợi:** Xác thực LIFF id_token so khớp line_user_id; từ chối.


## C35. Lộ SĐT/email qua API đơn hàng (no-auth) + thao tác MyPage no-auth
`High` · Đối tượng: **Người lạ** · Đợt: P1 (đề xuất) · Nguồn: Bổ sung review (G11)  
Vị trí/endpoint: `SalesManagementController.php:2074 (/ajax/get-info-friend-order-index); ChatController.php:6620,7311,7503 (/ajax/stopRemind, remove-tag-line-user-my-page, saveSettingDisplayInfo)`

**C35** — No-auth leak + MyPage ops
- **Tiền điều kiện:** Ẩn danh; order có line_user_id; remind/tag/setting tồn tại.
- **Dữ liệu nhập:** POST /ajax/get-info-friend-order-index {lineUserId=<bất kỳ>}; /ajax/stopRemind {id=<bất kỳ>}; remove-tag-line-user-my-page; saveSettingDisplayInfo.
- **Các bước:** Gọi ẩn danh từng endpoint.
- **Kết quả mong đợi:** Xác thực end user; không trả/không xóa dữ liệu người khác.


## C36. User thường sửa/xóa thông báo toàn hệ thống
`High` · Đối tượng: **User shop** · Đợt: P1 (đề xuất) · Nguồn: Bổ sung review (G11)  
Vị trí/endpoint: `Ajax/NotificationAjaxController.php · /ajax/create-notification, delete-notification, mass-delete-notification`

**C36** — Notification IDOR
- **Tiền điều kiện:** User thường đăng nhập.
- **Dữ liệu nhập:** POST /ajax/create-notification (nội dung chèn link phishing) · delete-notification · mass-delete-notification.
- **Các bước:** Gọi từng endpoint; kiểm thông báo hiển thị cho user khác.
- **Kết quả mong đợi:** Chỉ supper_admin; không chèn được link phishing toàn hệ thống.


## C37. Key hardcode trong code & route test tạo Stripe customer
`High` · Đối tượng: **Người có source / Người lạ** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (G12)  
Vị trí/endpoint: `routes/web.php:4227-4235; config/open_ai.php:3; MailApiService.php:143; ActiveAccount.php:566`

**C37** — Key hardcode + /test-customer
- **Tiền điều kiện:** Ẩn danh.
- **Dữ liệu nhập:** GET /test-customer; dùng Stripe `sk_test_51BX***`, OPEN_AI_API_KEY `sk-V***`, EMAIL_API_TOKEN `WSSV***` (giá trị cũ) gọi API tương ứng sau rotate.
- **Các bước:** 1) Truy cập route test 2) Thử key cũ với Stripe/OpenAI/Email.
- **Kết quả mong đợi:** /test-customer trả 404; key cũ revoke; chức năng dùng key mới vẫn chạy.


## X06. Chuỗi: Stored XSS form → /ajax miễn CSRF → IDOR chiếm bot
`High` · Đối tượng: **End user → admin** · Đợt: P0/P1 (đề xuất) · Nguồn: Bổ sung review (chain)  
Vị trí/endpoint: `C29 + C30 + C13/C11/C12`

**X06** — Chain XSS→CSRF→IDOR
- **Tiền điều kiện:** C29 + C30 + C13 chưa vá.
- **Dữ liệu nhập:** Payload XSS trong câu trả lời form chứa JS tự POST /ajax/bot-save (chiếm bot).
- **Các bước:** End user gửi form → admin mở trang xem → JS tự chạy gọi /ajax.
- **Kết quả mong đợi:** Không bước nào thực thi được: XSS escape / CSRF chặn / IDOR chặn.


## X07. Chuỗi: Master password → login as nạn nhân → IDOR/thanh toán
`High` · Đối tượng: **Người biết mật khẩu chung** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (chain)  
Vị trí/endpoint: `C21`

**X07** — Chain master-pass→IDOR
- **Tiền điều kiện:** C21.
- **Dữ liệu nhập:** Dùng PASS_LOGIN login as nạn nhân rồi thử IDOR/thanh toán.
- **Các bước:** Login as → thao tác.
- **Kết quả mong đợi:** Backdoor đã gỡ nên không vào được; nếu còn, mọi tác động quy về 1 lỗ gốc.


## X08. Chuỗi: Firebase adminsdk key (C20) → toàn quyền project Firebase
`High` · Đối tượng: **Người có source** · Đợt: P0 (đề xuất) · Nguồn: Bổ sung review (chain)  
Vị trí/endpoint: `C20`

**X08** — Chain Firebase key
- **Tiền điều kiện:** C20 (file firebase-adminsdk json từng lộ).
- **Dữ liệu nhập:** Dùng key Firebase adminsdk cũ gọi FCM/Firestore sau rotate.
- **Các bước:** Thử key cũ với Firebase Admin SDK.
- **Kết quả mong đợi:** Key cũ bị revoke; không thao tác được project Firebase.
