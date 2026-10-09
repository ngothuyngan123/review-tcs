# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine qua `/new-task 26763` (`scripts/redmine_fetch.py`).
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL) tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#26763 — [26-09-2024] [Event] Send sai action của slot` |
| Module / Màn hình | Event Booking (FA-021) — trang đặt chỗ LIFF 「イベント予約」, màn cài đặt khung giờ (box 「予約時」/「予約キャンセル」) khi sự kiện ở chế độ cần duyệt 「リクエスト制」 + ưu tiên action theo course (「コース別アクション」) |

## Mô tả bug (bản dịch tiếng Việt)

> Nội dung khách báo đã là tiếng Việt — giữ nguyên văn, không diễn giải lại.

Case Event setting request + không có course nhưng set ưu tiên action course.
Logic đang send action của slot nhưng lại send nhầm action approve ngay

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

*(Redmine #26763 không có attachment.)*

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** (description không có section "Tái hiện bug" riêng, không có Steps/Expected/Actual) — root cause đã được Dev confirm qua journal (xem mục dưới) và `03-dev-impact.md`. TCs nên tập trung verify cách fix + regression impact.
- Giải nghĩa thuật ngữ: 「リクエスト制」 = chế độ **cần duyệt** (request) của Event booking, đối lập với 「全承認」 = **duyệt ngay**. 「コース別アクション」 = ưu tiên action theo **course**; 「予約枠（下記）のアクション」 = ưu tiên action theo **khung giờ (slot)**.
- Status Redmine hiện tại: **Fix done - Đợi test**. Nhánh fix: `ai_fixbug_26763` (base `release_step_20260805`, commit `a98d58ed54`, 1 file: `app/Helpers/functions.php`).
- Journal ghi rõ cùng lỗi xảy ra ở **2 nhánh**: đặt lịch (gửi nhầm action mục 「予約受付時」/duyệt ngay) và hủy đặt lịch (gửi nhầm action mục 「予約キャンセル時」/hủy ngay) — thay vì đúng ra phải gửi action mục 「予約リクエスト申請時」 / 「キャンセルリクエスト申請時」.
- Dev tự ghi chú thêm 2 điểm **chưa chắc đã lộ lỗi** nhưng cùng pattern: (a) luồng đổi trạng thái từ màn quản trị hiện chưa xét chế độ duyệt nhưng UI không cho đặt trạng thái chờ duyệt nên chưa lộ; (b) không kiểm chứng được trên DB dev (kết nối `host.docker.internal:3306` bị từ chối) — chỉ verify ở mức `php -l` + `git diff --stat`, **chưa chạy test thật lúc Dev nộp báo cáo**.
- Dev cảnh báo rủi ro hành vi đổi (không phải bug mới): sau fix, nếu bot **chưa cấu hình action cho mục 「予約リクエスト申請時」** thì sẽ **không gửi tin nào** (trước đây gửi nhầm action mục khác nên luôn có tin) — đây là hành vi ĐÚNG theo cài đặt, không phải regression.
- **MCP LME TEST STUDIO đã có task #178** cho ticket này (17 TC, AI viết 15 + `quyend@mcp` viết 2, round 1, status `done-ai`, reviewState `leader`, exec 16 pass / 1 fail) — xem `04-tc-list.md` (fetch từ Studio, KHÔNG phải từ Google Sheet). **1 TC fail** (`NEW-11`/id 11901 — chặn hủy khi admin đổi chế độ hủy sang 「不可」 giữa lúc friend đang ở màn xác nhận cancel) đã raise bug ticket **#41892** (ticket riêng, KHÔNG phải #26763 này). 3 TC khác (`NEW-14`, `NEW-15`, `NEW-16`) đánh dấu "out of scope discovery" + gắn bug ticket **#41310** dù last_exec = pass — xem chi tiết ở `04-tc-list.md`.

## Journal / note từ Redmine (nguyên văn)

**Journal #131865 — AI LME Fix bug — 2026-08-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Sự kiện để chế độ cần duyệt (リクエスト制) + khung giờ chọn ưu tiên action theo course nhưng không có course nào: hàm gửi action đặt lịch đọc mã khung giờ từ bản ghi đã ghép bảng course. Bảng course cũng có cột cùng tên slot_id nên giá trị bị ghi đè thành rỗng, hệ thống không tra được chế độ duyệt và mặc định hiểu là duyệt ngay. Hậu quả: khách đăng ký chờ duyệt nhưng nhận action của khung giờ ở mục 'lúc nhận đặt lịch' (duyệt ngay) thay vì mục 'lúc gửi yêu cầu đặt lịch', đồng thời lịch sử action bị ghi sai loại. Cùng lỗi này xảy ra ở nhánh hủy đặt lịch (gửi action hủy ngay thay vì action gửi yêu cầu hủy).

■ 2. CÁCH FIX
Trong hàm gửi action đặt lịch sự kiện phía khách (sendActionAppBookingV1 - app/Helpers/functions.php), lấy mã khung giờ/course từ chính bản ghi đặt lịch (BBooking::find) thay vì lấy từ bản ghi đã ghép bảng course (bị cột trùng tên ghi đè). Nhờ đó tra đúng chế độ duyệt và gửi đúng action 'lúc gửi yêu cầu đặt lịch' (kèm đúng loại lịch sử action). Sửa cùng lúc ở 2 nhánh dùng chung đoạn lỗi: đặt lịch và hủy đặt lịch. Quét tương tự: các chỗ ghép bảng course khác chỉ đọc cột action nên không dính lỗi; riêng luồng đổi trạng thái từ màn quản trị vẫn chưa xét chế độ duyệt nhưng giao diện hiện không cho đặt trạng thái chờ duyệt nên chưa lộ lỗi.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
sendActionAppBookingV1 (app/Helpers/functions.php:6427)
sendActionBookingV1 (app/Helpers/functions.php:6011)
sendActionBooking (app/Helpers/functions.php:6247)
MobileEventBookingController::saveUserBooking (app/Http/Controllers/Basic/MobileEventBookingController.php:1368)
EventBookingService::handleOrderCallback (app/Services/EventBooking/EventBookingService.php:416)
BookingEventDayController::saveAdminBooking (app/Http/Controllers/Basic/BookingEventDayController.php:2890)
BookingEventDayController::saveActionBooking (app/Http/Controllers/Basic/BookingEventDayController.php:3774)
HelperService (app/Services/HelperService.php:1094)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Helpers/functions.php
 • 4.2 Data ảnh hưởng:
   - Không có (không đổi dữ liệu; chỉ đổi action LINE được gửi và cột trigger_type ghi vào lịch sử action)
 • 4.3 Tính năng liên quan:
   - Event Booking (FA-021) — gửi đúng action lúc gửi yêu cầu đặt lịch / yêu cầu hủy khi sự kiện ở chế độ cần duyệt
   - Reminder Delivery (FA-022) — action gửi kèm có thể chứa lệnh bật/tắt gửi nhắc lịch nên bị ảnh hưởng gián tiếp

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Helpers/functions.php: No syntax errors detected; git diff --stat origin/release_step_20260805...ai_fixbug_26763: 1 file, 12 insertions, 6 deletions
   Bằng chứng: Schema /workspace/share/db/db-structure/tables/b_plan_slot.sql:17 có cột slot_id → khi ghép bảng với b_user_booking (select *) thì slot_id của booking bị ghi đè, rỗng khi đơn không có course; b_slot.sql không có cột slot_id/plan_slot_id nên nhánh ghép b_slot không dính lỗi (giải thích vì sao chỉ lỗi khi ưu tiên action theo course); MobileEventBookingController.php:912 statusBooing = 3 khi chế độ cần duyệt → đi đúng nhánh case 3 vừa sửa; Không kiểm chứng được trên DB dev (kết nối host.docker.internal:3306 bị từ chối)

■ TỰ REVIEW (AI)
Sửa tối giản đúng gốc: đọc mã khung giờ/course từ bản ghi đặt lịch thay vì bản ghi bị cột trùng tên ghi đè. Không đổi cấu trúc hàm, không đổi thứ tự ưu tiên action (course trước, thiếu thì lùi về khung giờ). Phần chọn action và fallback giữ nguyên.
 • Rủi ro / lưu ý khi test:
   - Sau fix, sự kiện cần duyệt sẽ gửi action ở mục 'lúc gửi yêu cầu đặt lịch'; khách hàng nào đang vô tình dựa vào hành vi cũ (nhận action mục 'lúc nhận đặt lịch') sẽ thấy khác đi - đây là hành vi đúng theo cài đặt
   - Nếu khách chưa cài action cho mục 'lúc gửi yêu cầu đặt lịch' thì sẽ không có tin nào được gửi (trước đây gửi nhầm action mục khác)
   - Thêm 1 truy vấn nhẹ theo khóa chính mỗi lần gửi action (không đáng kể)

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_26763 (nhánh gốc release_step_20260805, commit a98d58ed54, 1 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 11 phút 10 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=e460ce95-d3fd-4a20-8bca-cab95d5740ee
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=26763
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
