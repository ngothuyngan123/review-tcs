# LME – Main case kiểm thử lỗi bảo mật nghiêm trọng

**Ngày lập:** 22/10/2026  
**Nguồn:** security-audit-20261022.html  
**Branch được audit:** release_step_20260930_v2  
**Phạm vi:** 20 phát hiện Critical; bổ sung Univapay (High) vào nhóm ưu tiên thanh toán.

> Đây là kế hoạch kiểm thử, chưa phải kết quả chạy test. Confirmed trong báo cáo là xác nhận qua code. SQLi tin nhắn chưa xác nhận luồng chạy production; RCE qua upload phụ thuộc cấu hình server. Mã C01–C20 do kế hoạch này đặt, theo thứ tự báo cáo.

## 1. Chuẩn bị và cách chạy

- Staging gần cấu hình production, dữ liệu test riêng; thanh toán sandbox.
- Shop A/B, bot A/B; owner A/B, staff giới hạn quyền và SuperAdmin.
- LINE user A/B, phiên không đăng nhập và LIFF hết hạn.
- Chat, tag, đơn sản phẩm, booking event/lesson/salon và subscription ở cả hai shop.
- File media hợp lệ và file đánh dấu ngoài thư mục cho phép, không chứa secret thật.
- Với thao tác ghi/xóa/gửi tin/thanh toán: đối chiếu DB, queue/job, log và dịch vụ sandbox. HTTP 401/403 chưa đủ chứng minh không có tác động.
- Mỗi case bị chặn phải có case hợp lệ tương ứng; che secret khi lưu bằng chứng.

## 2. Thứ tự ưu tiên

| Đợt | Mục tiêu | Nhóm case |
|---|---|---|
| P0.1 | Chặn lộ secret, truy cập server và giả mạo từ bên ngoài | C01–C05, C08–C10, C14, C20 |
| P0.2 | Chặn phá dữ liệu và vượt quyền | C11–C13, C15–C19 |
| P0.3 | Xác minh SQLi và chuỗi kết hợp | C06–C07, X01–X05 |

Thứ tự này là thứ tự chạy test, không phải trì hoãn vá các lỗi Critical còn lại.

## 3. Main case Critical

### C01. Đọc file bất kỳ trên server qua /ajax/get-file-url (lấy được .env)

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** app/Http/Controllers/Basic/BasicController.php:2755 · route POST /ajax/get-file-url (routes/web.php:4248)
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C01-01 | Không đăng nhập gọi endpoint |
| C01-02 | Yêu cầu file ngoài media bằng đường dẫn tương đối, tuyệt đối và dạng mã hóa |
| C01-03 | User A yêu cầu file media của shop B |
| C01-04 | User hợp lệ đọc file được phép |

**Kết quả mong đợi chung:** Không trả nội dung/URL file trái phép; file hợp lệ vẫn đọc được.

### C02. Trang xem log /error/logs mở công khai – xem, tải, xóa file bất kỳ

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** routes/web.php:81 (middleware https_protocol rỗng)
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C02-01 | Người lạ và user thường mở trang log |
| C02-02 | Gọi trực tiếp chức năng download/delete |
| C02-03 | Vai trò được phép yêu cầu file ngoài thư mục log |
| C02-04 | Kiểm tra file đánh dấu sau request xóa bị từ chối |

**Kết quả mong đợi chung:** Không lộ log, không tải/xóa file ngoài quyền; file đánh dấu không bị thay đổi.

### C03. Secret key Stripe/Univapay của shop lộ trên 3 trang đặt lịch công khai

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** Basic/MobileEventBookingController.php:167,204 + views/basic/booking_event_day/order/index.blade.php:871; Mobile/CalendarController.php:126,195; Mobile/CalendarSalonController.php:172,255
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C03-01 | Mở ẩn danh đủ trang event, lesson và salon |
| C03-02 | Kiểm tra View Source, HTML, JS khởi tạo và response Network |
| C03-03 | Kiểm tra shop dùng Stripe, Univapay và shop chưa cấu hình thanh toán |
| C03-04 | Thực hiện booking và thanh toán sandbox hợp lệ |

**Kết quả mong đợi chung:** Không lộ secret key/token; chỉ trả dữ liệu công khai cần thiết; booking/thanh toán vẫn hoạt động.

### C04. Trang sản phẩm công khai in toàn bộ bản ghi bot ra console (LINE token, key ChatGPT)

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** Basic/SalesManagementV2Controller.php:1789,1931; views/basic/sales/v2/order/detail.blade.php:494 · route GET /v2/order-item/detail/{item_code}
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C04-01 | Kiểm tra Console, View Source và Network của trang sản phẩm |
| C04-02 | Kiểm tra dữ liệu bot còn nhúng trong trang dù đã xóa console.log hay không |
| C04-03 | Kiểm tra sản phẩm của nhiều bot |
| C04-04 | Đặt hàng hợp lệ |

**Kết quả mong đợi chung:** Không có LINE token/secret, OpenAI key, Google access token trong dữ liệu client; đặt hàng vẫn hoạt động.

### C05. Webhook LINE không kiểm tra chữ ký (luôn hợp lệ)

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** app/Http/Controllers/Admin/BotController.php:2034-2040 · route POST /line/callback/add/{bot_id}
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C05-01 | Gửi webhook thiếu, rỗng và sai chữ ký |
| C05-02 | Gửi chữ ký đúng với body gốc |
| C05-03 | Sửa body sau khi ký |
| C05-04 | Dùng chữ ký của bot A gửi tới bot B |
| C05-05 | Chạy các biến thể trên message, follow và postback |

**Kết quả mong đợi chung:** Request sai bị chặn trước mọi xử lý; không tạo chat, gắn tag, chạy scenario, đổi booking hoặc đưa job vào queue; webhook hợp lệ vẫn chạy.

### C06. SQL Injection qua nội dung tin nhắn LINE (auto-reply)

- **Đối tượng trong báo cáo:** End user / Người lạ
- **Vị trí/endpoint:** app/Console/Commands/HandleCallbackMessage.php:436; Admin/BotController.php:3563
- **Mức xác nhận trong báo cáo:** Likely (chưa xác minh command còn chạy ở prod)

| Mã case | Thao tác chính |
|---|---|
| C06-01 | Xác nhận command/worker trong báo cáo có chạy trên môi trường test |
| C06-02 | Gửi tin LINE thật chứa dấu nháy, ký tự SQL và Unicode |
| C06-03 | Gửi chuỗi kiểm thử SQLi không phá dữ liệu trên staging |
| C06-04 | Kiểm tra keyword khớp/không khớp và theo dõi lỗi DB/job |

**Kết quả mong đợi chung:** Nội dung là văn bản, không thay đổi logic truy vấn, không lộ lỗi SQL; auto-reply và worker hoạt động. Chưa xác nhận luồng chạy phải ghi Blocked/Chưa xác minh, không đánh Pass.

### C07. SQL Injection ở trang đặt chỗ sự kiện công khai (tham số quantity)

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** Basic/MobileEventBookingController.php:653,664 · route POST /ajax/booking-event/change-booking (không auth)
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C07-01 | Truyền số nguyên hợp lệ và giá trị tại giới hạn số lượng |
| C07-02 | Truyền 0, số âm, thập phân, chuỗi, null, mảng và số quá lớn |
| C07-03 | Truyền chuỗi kiểm thử SQLi không phá dữ liệu |
| C07-04 | Đối chiếu booking, tồn chỗ và tổng tiền sau request bị từ chối |

**Kết quả mong đợi chung:** Input sai bị validate; không thực thi thành SQL; không thay đổi booking, tồn chỗ hoặc tổng tiền.

### C08. Callback Telecom cho phép đánh dấu “đã thanh toán” giả

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** app/Http/Controllers/Customers.php:300-410 · /customer/telecom_callback_*.php (routes/web.php:3799-3801)
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C08-01 | Gửi callback giả cho payment pending |
| C08-02 | Thiếu/sai thông tin xác thực nguồn gửi |
| C08-03 | Sai payment, số tiền hoặc trạng thái |
| C08-04 | Truy cập payment/hash của người khác qua make_form_telecom |
| C08-05 | Callback sandbox hợp lệ và gửi lặp |

**Kết quả mong đợi chung:** Không tạo trạng thái đã thanh toán hoặc hoa hồng giả; callback hợp lệ chỉ tạo tác động một lần.

### C09. Server WebSocket không xác thực – nghe được chat realtime của mọi shop

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** node_serve/server.js:53-67,120-126
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C09-01 | Kết nối không token, token sai và hết hạn |
| C09-02 | Không truyền botCode để kiểm tra room legacy |
| C09-03 | User A join room bot B |
| C09-04 | Gửi typing/join-room-typing tới room B |
| C09-05 | Tạo chat đồng thời ở A/B, kiểm tra nội dung và metadata nhận được |
| C09-06 | Thu hồi quyền rồi reconnect/join lại |

**Kết quả mong đợi chung:** Chỉ nhận/phát event ở bot có quyền; không nhận dữ liệu qua room legacy hoặc room khác; quyền bị thu hồi không tiếp tục được cấp khi reconnect.

### C10. Upload file tùy ý qua form trả lời công khai (nguy cơ chạy mã trên server)

- **Đối tượng trong báo cáo:** Người lạ / End user
- **Vị trí/endpoint:** Basic/FormAnswerController.php:6111-6160; app/Helpers/functions.php:766-787 · route /ajax/render/upload-image-form-answer
- **Mức xác nhận trong báo cáo:** Confirmed (RCE phụ thuộc cấu hình server)

| Mã case | Thao tác chính |
|---|---|
| C10-01 | Upload file hợp lệ |
| C10-02 | Upload .php, .html, .svg theo chính sách bản vá |
| C10-03 | Thử đuôi kép, chữ hoa/thường, giả MIME và đổi tên file có nội dung không hợp lệ |
| C10-04 | Kiểm tra URL file sau upload và file bị từ chối có còn truy cập được không |
| C10-05 | Dev/ops xác minh media không thực thi PHP, kể cả file đã tồn tại trước vá |

**Kết quả mong đợi chung:** File nguy hiểm bị chặn; không còn bản truy cập được của file bị từ chối; file hợp lệ hoạt động; media không thực thi mã.

### C11. API /api/unfollow-line xóa hội thoại, tin nhắn, tag của bot bất kỳ

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** app/Http/Controllers/Api/LineApiController.php:23 · routes/api.php:21
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C11-01 | Không auth gửi cặp bot/user của dữ liệu test |
| C11-02 | Gửi auth sai |
| C11-03 | Trộn bot A với LINE user B |
| C11-04 | Đối chiếu chat, tin nhắn và tag trước/sau |
| C11-05 | Kiểm tra luồng unfollow hợp lệ nếu endpoint được giữ lại |

**Kết quả mong đợi chung:** Request trái phép không xóa dữ liệu; luồng hợp lệ chỉ xử lý đúng phạm vi.

### C12. User thường gọi được API SuperAdmin (đổi tài khoản ngân hàng affiliate)

- **Đối tượng trong báo cáo:** User shop
- **Vị trí/endpoint:** Admin/SupperAdminController.php (56, 82, 125, 167, 201, 369) · routes/web.php:3718
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C12-01 | Người lạ, owner shop và staff gọi trực tiếp từng API trong group |
| C12-02 | Thử chức năng đổi ngân hàng/hoa hồng, đăng ký affiliate và xem bot/staff |
| C12-03 | SuperAdmin thực hiện nghiệp vụ hợp lệ |

**Kết quả mong đợi chung:** Chỉ vai trò được cấp quyền thao tác được; request trái phép không làm thay đổi dữ liệu/tài chính.

### C13. Ghi đè channel token/secret của bot shop khác (chiếm/phá bot)

- **Đối tượng trong báo cáo:** User shop
- **Vị trí/endpoint:** Admin/BotController.php:787-799, 1150-1212 · POST /admin/bot-save
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C13-01 | User A sửa bot B bằng ID/hash của B |
| C13-02 | Staff không có quyền sửa token gọi API |
| C13-03 | Đối chiếu channel token/secret, webhook và BotUsers của B trước/sau |
| C13-04 | Owner cập nhật bot của mình hợp lệ |

**Kết quả mong đợi chung:** Không ghi đè/reset bot B; cập nhật hợp lệ vẫn hoạt động.

### C14. Lấy danh sách bot (kèm LINE token) của user bất kỳ, không cần đăng nhập

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** Admin/UserController.php:4872 · POST /ajax/employees-management/get-list-bot-access (web.php:3768)
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C14-01 | Không đăng nhập truyền user ID hợp lệ |
| C14-02 | User A truyền ID của B |
| C14-03 | User A lấy danh sách bot được phép của mình |
| C14-04 | Kiểm tra từng field trong response thành công |

**Kết quả mong đợi chung:** Không lấy được bot ngoài quyền; response hợp lệ không chứa secret dư thừa.

### C15. API kiểm tra bước tạo bot trả nguyên bản ghi bot của người khác

- **Đối tượng trong báo cáo:** User shop
- **Vị trí/endpoint:** Admin/BotController.php:7114-7214; Admin/UserController.php:396-499 · web.php:191, 2002-2003
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C15-01 | User A truyền bot B vào từng endpoint step3-check, step5-check và bot/check-mode |
| C15-02 | Truyền bot ID không tồn tại |
| C15-03 | Owner/staff được phép thực hiện luồng hợp lệ |
| C15-04 | Kiểm tra response thành công và lỗi |

**Kết quả mong đợi chung:** Chặn bot ngoài quyền; không trả full model chứa secret.

### C16. Chuyển “bot hiện tại” trong session sang bot bất kỳ

- **Đối tượng trong báo cáo:** User shop
- **Vị trí/endpoint:** Mobile/ListFriendController.php (index); app/Http/Middleware/BasicAccess.php nhánh basicHome
- **Mức xác nhận trong báo cáo:** Confirmed (gán session) / Likely (khai thác từng ajax)

| Mã case | Thao tác chính |
|---|---|
| C16-01 | A mở list-friend bằng hash bot B |
| C16-02 | Sau request bị từ chối, kiểm tra bot trong session và gọi API friend/chat/tag |
| C16-03 | Thử thao tác ghi trên dữ liệu test của B |
| C16-04 | Lặp lại với nhiều tab |
| C16-05 | Staff chuyển giữa các bot có quyền |

**Kết quả mong đợi chung:** Session không chuyển trái phép sang B; API sau đó vẫn giới hạn đúng quyền; chuyển bot hợp lệ hoạt động.

### C17. API mobile nhận botId từ client – đọc chat và gửi tin thay bot khác

- **Đối tượng trong báo cáo:** User shop (app mobile)
- **Vị trí/endpoint:** Api/ChatController.php:132, 1911, 2671, 5064, 5185, 5387 · /api/mobile/chat/*
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C17-01 | Token A kết hợp botIdCurrent B |
| C17-02 | Bot A kết hợp conversationId B |
| C17-03 | Truyền cả bot và conversation của B |
| C17-04 | Thử đọc chat, gửi tin và các thao tác liên quan |
| C17-05 | Owner/staff mobile thao tác hợp lệ |

**Kết quả mong đợi chung:** Không đọc chat/gửi tin thay B; kiểm tra cả quyền bot và quan hệ conversation–bot; tác vụ hợp lệ hoạt động.

### C18. Xóa vĩnh viễn đơn hàng/booking theo id, không cần đăng nhập

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** SalesManagementV2Controller.php:5203; Mobile/CalendarController.php:1396; Mobile/CalendarSalonController.php:2182; MobileEventBookingController.php:1653
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C18-01 | Test đủ bốn loại: đơn sản phẩm, lesson, salon và event |
| C18-02 | Không auth, token sai/hết hạn, user A xóa bản ghi B |
| C18-03 | Thử bản ghi pending, success/đã xác nhận, paid và cancelled |
| C18-04 | Cleanup đúng bản ghi được phép và gửi lặp |
| C18-05 | Kiểm tra tồn chỗ/tồn kho và job liên quan |

**Kết quả mong đợi chung:** Chỉ cleanup bản ghi đúng điều kiện; không xóa bản ghi ngoài quyền hoặc đã thanh toán/đã xác nhận; không hoàn tồn chỗ/tồn kho hai lần.

### C19. Hủy subscription (đơn định kỳ) của bất kỳ ai

- **Đối tượng trong báo cáo:** Người lạ
- **Vị trí/endpoint:** SalesManagementV2Controller.php:1225; SalesManagementController.php:1333 · /ajax/(mobile/)cancel-cycle-order
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C19-01 | Test cả hai biến thể cancel-cycle-order |
| C19-02 | Không session gửi yêu cầu hủy |
| C19-03 | Session A yêu cầu hủy subscription B |
| C19-04 | Token thiếu/sai/hết hạn |
| C19-05 | Chủ sở hữu hủy hợp lệ và gửi lặp |
| C19-06 | Đối chiếu trạng thái nội bộ và cổng thanh toán sandbox |

**Kết quả mong đợi chung:** Không hủy subscription ngoài quyền; hủy hợp lệ chỉ có tác động một lần; trạng thái hai phía nhất quán.

### C20. File credential bị commit vào git, 1 file tải được qua web

- **Đối tượng trong báo cáo:** Người lạ / người có source
- **Vị trí/endpoint:** các file trên (có trong git ls-files)
- **Mức xác nhận trong báo cáo:** Confirmed

| Mã case | Thao tác chính |
|---|---|
| C20-01 | Truy cập trực tiếp URL credential được nêu trong báo cáo |
| C20-02 | Kiểm tra bản deploy còn credential hoặc bản sao dự phòng không |
| C20-03 | Dev/ops xác minh xử lý Git history và rotate credential |
| C20-04 | Xác minh credential cũ mất hiệu lực |
| C20-05 | Chức năng dùng credential mới vẫn hoạt động |

**Kết quả mong đợi chung:** Không tải được file credential; credential cũ bị vô hiệu hóa. Chỉ xóa file trên web chưa đủ để đóng lỗi.

## 4. Case kết hợp bắt buộc

| Mã | Chuỗi kiểm thử | Kết quả mong đợi |
|---|---|---|
| X01 | Webhook LINE sai chữ ký → auto-reply/scenario/postback/booking | Không có xử lý nghiệp vụ hoặc job nền. |
| X02 | Thử đổi session sang bot B → đọc friend/chat và ghi dữ liệu B | Session và các API tiếp theo đều giữ đúng giới hạn quyền. |
| X03 | Trang đã bỏ secret → kiểm tra credential cũ sau rotate | Credential cũ mất hiệu lực. |
| X04 | Upload → truy cập URL file | Không thực thi mã hoặc phục vụ nội dung nguy hiểm; file hợp lệ vẫn dùng được. |
| X05 | Request bị từ chối → kiểm tra DB/queue/dịch vụ ngoài | Không có tác động xảy ra trước hoặc sau response lỗi. |

Sau khi vá chữ ký LINE, vẫn chạy C06 bằng tin nhắn LINE hợp lệ để kiểm tra riêng SQLi.

## 5. Bổ sung ưu tiên: webhook Univapay (High trong báo cáo)

Đề xuất chạy cùng Telecom vì báo cáo mô tả khả năng đánh dấu thanh toán thành công khi chưa trả tiền. Đây là đề xuất ưu tiên test, không đổi severity gốc.

| Mã | Main case | Kết quả mong đợi |
|---|---|---|
| U01 | Callback thiếu/sai xác thực | Bị từ chối, không đổi đơn/booking/hợp đồng. |
| U02 | Charge không tồn tại hoặc không thuộc tài khoản/đơn tương ứng | Không ghi nhận thanh toán. |
| U03 | Sai số tiền, tiền tệ hoặc trạng thái | Không ghi nhận thanh toán thành công. |
| U04 | Callback sandbox hợp lệ | Đối chiếu giao dịch và cập nhật đúng đơn. |
| U05 | Gửi lặp callback hợp lệ | Không tạo tác động tài chính/nghiệp vụ trùng. |

## 6. Điều kiện đóng lỗi

- Case khai thác chính và biến thể liên quan bị chặn.
- Không có dữ liệu hoặc tác động phụ từ request trái phép, kể cả job nền.
- Owner/staff/end-user hợp lệ vẫn thực hiện được nghiệp vụ.
- Test đủ endpoint và biến thể được nêu trong báo cáo.
- Có bằng chứng request/response và trạng thái trước/sau, che secret.
- Lỗi lộ credential: rotate hoàn tất và key cũ mất hiệu lực.
- Lỗi phụ thuộc cấu hình/luồng chạy: có xác minh tương ứng từ dev/ops; chưa đủ điều kiện thì ghi Blocked/Chưa xác minh.

## 7. Mẫu ghi kết quả

| Mã case | Môi trường/build | Vai trò/dữ liệu test | Actual result | Pass/Fail/Blocked | Bằng chứng/Bug |
|---|---|---|---|---|---|
| C01-01 | | | | | |
