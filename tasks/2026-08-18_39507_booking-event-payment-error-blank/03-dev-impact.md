# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #39507 journal J#128829 (2026-08-12 04:26:36) — báo cáo tự động của hệ thống **Auto-fixbug LME**.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | commit `6944f7ccb1` (repo `sns-line`, 1 file) — không có link GitHub/GitLab trong Redmine. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=39507 |
| Branch | `ai_fixbug_39507` (nhánh gốc `release_step_20260805`) — **đã push lên origin** |
| Ngày submit đánh giá | `2026-08-12` (custom field Commit Date = 2026-08-12) |
| Auto-filled | `2026-08-18 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Có 2 chuyện tách rời nhau. (1) Vì sao thanh toán thử thất bại: cổng thanh toán UnivaPay giới hạn mỗi giao dịch ở môi trường THỬ tối đa 50.000 yên, trong khi khoá học của khách thu 66.000 yên, nên UnivaPay từ chối ngay với mã lỗi vượt hạn mức. Đây là giới hạn của cổng thanh toán, không sửa được bằng code. (2) Vì sao khách chỉ thấy hộp thoại TRỐNG không có chữ nào: khi tài khoản có bật cơ chế chờ phản hồi từ cổng thanh toán, nhánh xử lý lỗi trong hàm thanh toán của trang đặt lịch sự kiện chỉ đánh dấu là lỗi rồi xoá lượt đặt, mà QUÊN gán nội dung thông báo lỗi. Kết quả trả về cho trình duyệt có phần thông báo rỗng nên hiện hộp thoại trắng. Nhánh không chờ phản hồi (ngay bên dưới) thì gán đúng, và 3 tính năng anh em (mua sản phẩm, đặt lịch khoá học, đặt lịch salon) cũng đều gán đúng — chỉ riêng đặt lịch sự kiện bị sót.

## 2. Cách fix

Bổ sung việc gán nội dung thông báo lỗi ở nhánh chờ phản hồi cổng thanh toán trong hàm thanh toán của trang đặt lịch sự kiện (MobileEventBookingController::payment): khi tạo giao dịch UnivaPay thất bại thì lấy thông báo lỗi đã dịch sẵn theo mã lỗi rồi trả về cho màn hình, thay vì trả chuỗi rỗng làm hiện hộp thoại trắng. Thêm một dòng ghi log lỗi cho khớp với nhánh còn lại. Đúng 2 dòng, dùng lại đúng cách viết đã có sẵn ở nhánh không chờ phản hồi ngay bên dưới và ở tính năng mua sản phẩm. Riêng nguyên nhân gốc khiến thanh toán thất bại (hạn mức 50.000 yên cho mỗi giao dịch ở môi trường thử của UnivaPay) là giới hạn của cổng thanh toán, không sửa bằng code — cần trả lời khách: muốn thử thì hạ giá khoá học xuống dưới 50.000 yên rồi trả lại giá thật, hoặc thử thẳng ở môi trường thật rồi hoàn tiền.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn Dev ở mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN", chuyển sang bảng — **không thêm/bớt mục nào**.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `MobileEventBookingController::payment` — `app/Http/Controllers/Basic/MobileEventBookingController.php:706` | **Đã sửa** — nhánh chờ phản hồi cổng thanh toán ở dòng 1102-1109 | Hàm chứa bug: quên gán nội dung thông báo lỗi |
| 2 | `MobileEventBookingController::changeBooking` — `app/Http/Controllers/Basic/MobileEventBookingController.php:1712` | **Chưa sửa** | Luồng đổi lượt đặt, cùng họ nhưng lỗi khác (ghi ở mục yokoten) |
| 3 | `UnivapayPayment::chargeMoneyUnivapaySale` — `app/Helpers/UnivapayPayment.php:1158` | Không đổi | Nơi bắt lỗi từ cổng thanh toán, trả về mã lỗi vượt hạn mức |
| 4 | `UnivapayPayment::getMessageErrorUnivapay` — `app/Helpers/UnivapayPayment.php:2016` | Không đổi | Bảng dịch mã lỗi sang tiếng Nhật, đã có sẵn câu cho lỗi vượt hạn mức ở dòng 2313 |
| 5 | `isProcessWithWebhook` — `app/Helpers/functions.php:138` | Không đổi | Quyết định đi nhánh chờ phản hồi hay không |
| 6 | `order-item.js: payment` — `public/js/booking_event_day/order-item.js:671` | Không đổi | Chỗ hiện hộp thoại lỗi ở dòng 788-800 |
| 7 | `SalesManagementV2Controller` — `app/Http/Controllers/Basic/SalesManagementV2Controller.php:5125` | Không đổi | Tính năng mua sản phẩm, bản viết ĐÚNG dùng làm mẫu đối chiếu |
| 8 | `CalendarController` — `app/Http/Controllers/Mobile/CalendarController.php:1133` | Không đổi | Đặt lịch khoá học, cũng xử lý đúng |
| 9 | `CalendarSalonController` — `app/Http/Controllers/Mobile/CalendarSalonController.php:1788` | Không đổi | Đặt lịch salon, cũng xử lý đúng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev chỉ liệt kê **file thay đổi** ở mục 4.1 (nguyên văn: "app/Http/Controllers/Basic/MobileEventBookingController.php"). Bảng dưới derive từ mục 2 + mục 3 của chính Dev, KHÔNG suy diễn thêm.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `MobileEventBookingController::payment` — nhánh `isProcessWithWebhook = true`, dòng 1102-1109 | `app/Http/Controllers/Basic/MobileEventBookingController.php` | Direct | 2 dòng: gán nội dung thông báo lỗi theo mã lỗi + thêm 1 dòng ghi log lỗi |
| F2 | Endpoint thanh toán đặt chỗ event (response JSON trả về màn LIFF) | cùng file, response cuối hàm `payment()` (dòng 1479-1484 theo TC Studio) | Direct | Giá trị message lỗi đổi từ rỗng → có nội dung; cấu trúc key **không đổi** |
| F3 | `order-item.js: payment` — chỗ render hộp thoại lỗi (dòng 788-800) | `public/js/booking_event_day/order-item.js` | Indirect | Không sửa code, nhưng là nơi biểu hiện bug (hộp thoại trắng) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** | — | Nguyên văn Dev: "Không có — chỉ đổi nội dung thông báo trả về, không ghi thêm hay sửa dữ liệu nào. Lượt đặt hỏng vẫn bị xoá và trả lại chỗ như trước." |
| D2 | (gián tiếp, KHÔNG do fix) Bản ghi đặt chỗ tạm + số chỗ đã dùng của khung giờ | DELETE / recalc | Hành vi **có sẵn từ trước**, fix không chạm — vẫn cần regression verify |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Event Booking (FA-021)** — hiện đúng lý do khi thanh toán thất bại trên trang đặt chỗ sự kiện, thay vì hộp thoại trống | F1, F2 | Nguyên văn Dev: đây là mục 4.3 **duy nhất** Dev liệt kê |
| T2 | (Dev **không** liệt kê ở 4.3, chỉ nêu ở mục 3 làm đối chiếu) Mua sản phẩm · Đặt lịch khoá học · Đặt lịch salon | F1 (dùng chung bảng dịch mã lỗi + cơ chế chờ webhook) | Low — Dev khẳng định 3 nơi này vốn đã gán message đúng |
| T3 | (Dev **không** liệt kê ở 4.3) `MobileEventBookingController::changeBooking` — luồng đổi lượt đặt | Mục 3 dòng 2: "cùng họ nhưng lỗi khác, **chưa sửa** (ghi ở mục yokoten)" | ⚠️ Dev tự nhận có lỗi khác chưa sửa ở đây — Leader cần quyết có test hay không |

---

## 5. Recover data (nguyên văn Dev)

✔ Không cần recover data

## 6. Verify của Dev (nguyên văn)

**Mức:** lint

**Lệnh:** `php -l app/Http/Controllers/Basic/MobileEventBookingController.php`: No syntax errors detected; `git diff --stat release_step_20260805...ai_fixbug_39507`: 1 file changed, 2 insertions — không kéo theo thay đổi lạ; Không viết unit test: file sửa là controller có gọi cổng thanh toán ngoài, không thuộc nhóm logic thuần được phép test theo quy ước dự án

**Bằng chứng:**
- Log production của khách 2026-08-06 17:04:20 xác nhận đường đi: `MobileEventBookingController.php:1092` gọi `chargeMoneyUnivapaySale` với số tiền 66000 và tham số môi trường 0 (thử) → UnivaPay trả `400 CHARGE_AMOUNT_TOO_HIGH` kèm lý do `Charge amount must not exceed 50000.`
- Mã lỗi `CHARGE_AMOUNT_TOO_HIGH` ĐÃ có sẵn câu tiếng Nhật trong bảng dịch (`UnivapayPayment.php:2313`) — nghĩa là chỉ thiếu bước gán, không phải thiếu bản dịch.
- Đối chiếu 4 tính năng cùng dùng cơ chế chờ phản hồi cổng thanh toán: mua sản phẩm (`SalesManagementV2Controller.php:5125-5129`) gán thông báo lỗi ở ĐÚNG vị trí này; đặt lịch khoá học (`CalendarController.php:1133-1139`) và đặt lịch salon đều chặn lỗi tạo giao dịch TRƯỚC khi vào nhánh chờ. Chỉ đặt lịch sự kiện bị sót ⇒ đây là lỗi sót thật, không phải cố ý.
- ⚠️ **Không kiểm chứng được trên môi trường dev**: MySQL `host.docker.internal:3306` và web dev cổng 8000 đều Connection refused.

## 7. Tự review của AI + rủi ro khi test (nguyên văn)

Sửa 2 dòng, đúng phạm vi lỗi được log xác nhận. Không đổi luồng nghiệp vụ, không đổi điều kiện thành công hay thất bại, không đụng dữ liệu — chỉ điền nội dung thông báo vốn bị bỏ trống. Cách viết sao chép nguyên mẫu đã chạy ổn định ở nhánh ngay bên dưới và ở 3 tính năng anh em. Nguyên nhân gốc làm thanh toán thất bại là hạn mức của cổng thanh toán nên phải trả lời khách bằng hướng dẫn vận hành, không phải bằng code.

**Rủi ro / lưu ý khi test:**
- Rất thấp: thay đổi chỉ ảnh hưởng nội dung chữ trong tình huống ĐÃ thất bại; đường đi thành công không chạm tới.
- Nếu cổng thanh toán trả về mã lỗi chưa có trong bảng dịch thì khách sẽ thấy nguyên văn thông báo tiếng Anh của thư viện gọi API — vẫn tốt hơn hộp thoại trống, và giống hệt hành vi của nhánh không chờ phản hồi đang chạy lâu nay.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm Leader cần quyết trước khi review TCs

1. **`changeBooking` chưa sửa** — Dev tự nhận "cùng họ nhưng lỗi khác, chưa sửa (yokoten)". TC Studio NEW-13/14/15 (do QA `thanhntp` tự thêm) đang test màn change booking → cần Leader xác nhận scope.
2. **Hạn mức UnivaPay là giới hạn cổng, không fix bằng code** — TC KHÔNG được kỳ vọng 66.000 yên thanh toán thành công ở môi trường thử.
3. **Mã lỗi ngoài bảng dịch → hiện chuỗi tiếng Anh thô** — Dev coi là chấp nhận được; TC Studio NEW-8 ghi "CẦN LEADER XÁC NHẬN".
4. **Dev không verify được trên dev env** (MySQL + web dev đều Connection refused) → toàn bộ gánh nặng verify dồn sang QA.
