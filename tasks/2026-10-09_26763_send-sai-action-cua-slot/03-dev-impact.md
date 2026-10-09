# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine qua `/new-task 26763`, parse Journal #131865 ("AI LME Fix bug") + đối chiếu `dev_impact` / `requirements` của MCP LME TEST STUDIO task #178.
> **Tester verify rồi tick checkbox dưới đây.**

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (Auto-fixbug) — assignee Redmine: Đỗ Quyên |
| Commit / Pull Request | `a98d58ed54` (không có PR URL — workflow AI Auto-fixbug, không qua PR review thường) |
| Branch | `ai_fixbug_26763` (base `release_step_20260805`) |
| Ngày submit đánh giá | 2026-08-21 |
| Auto-filled | 2026-10-09 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #131865 và xác nhận đầy đủ 4 mục dưới đây.

---

## 1. Nguyên nhân

Sự kiện để chế độ cần duyệt (リクエスト制) + khung giờ chọn ưu tiên action theo course nhưng **không có course nào**: hàm gửi action đặt lịch đọc mã khung giờ từ bản ghi **đã ghép bảng course** (JOIN). Bảng course cũng có cột cùng tên `slot_id` nên giá trị bị ghi đè thành rỗng, hệ thống không tra được chế độ duyệt và mặc định hiểu là duyệt ngay (`全承認`).

Hậu quả: khách đăng ký chờ duyệt nhưng nhận action của khung giờ ở mục 「予約受付時」 (lúc nhận đặt lịch / duyệt ngay) thay vì mục 「予約リクエスト申請時」 (lúc gửi yêu cầu đặt lịch), đồng thời lịch sử action (`action_lineuser.type_start_scenario`) bị ghi sai loại (8001 thay vì 8002). Cùng lỗi này xảy ra ở nhánh hủy đặt lịch — gửi nhầm action mục 「予約キャンセル時」 (trigger 8009) thay vì 「キャンセルリクエスト申請時」 (trigger 8010).

**Bằng chứng kỹ thuật**: schema `b_plan_slot.sql:17` có cột `slot_id` → khi `SELECT *` JOIN với `b_user_booking`, `slot_id` của booking bị ghi đè, rỗng khi đơn không có course; `b_slot.sql` KHÔNG có cột trùng tên `slot_id`/`plan_slot_id` nên nhánh ưu tiên action theo **khung giờ** (không qua JOIN course) không dính lỗi này.

## 2. Cách fix

Trong hàm gửi action đặt lịch sự kiện phía khách (`sendActionAppBookingV1` — `app/Helpers/functions.php:6427`), lấy mã khung giờ/course từ **chính bản ghi đặt lịch** (`BBooking::find($bookingId)`) thay vì từ bản ghi đã ghép bảng course (bị cột trùng tên ghi đè). Nhờ đó tra đúng chế độ duyệt và gửi đúng action mục 「予約リクエスト申請時」 (kèm đúng loại lịch sử action).

Sửa đồng thời **2 nhánh** dùng chung đoạn lỗi trong cùng hàm: nhánh đặt lịch trực tiếp (case `'3'`/`'5'`, `isChange=false`) và nhánh hủy trực tiếp (case `'4'`). Không đổi cấu trúc hàm, không đổi thứ tự ưu tiên action (course trước, thiếu thì lùi về khung giờ) — fix tối giản, chỉ đổi nguồn đọc.

Diff thật (theo Studio `spec_delta`): `app/Helpers/functions.php | 18 ++++++++++++------` — 1 file, 12 insertions, 6 deletions.

⚠️ **Phạm vi fix KHÔNG bao gồm** (phát hiện qua đối chiếu Studio `requirements` REQ-008, xem mục 4.3 T4): nhánh **đổi lịch** (`isChange=true`, `functions.php:6449-6451`) và nhánh **sửa lại đơn đang chờ duyệt** (`functions.php:6572-6576`) — đọc mã nguồn cho thấy **cùng lớp lỗi** (đọc chế độ duyệt từ bản ghi JOIN course) vẫn còn tồn tại ở 2 nhánh này, Dev không sửa vì không nằm trong mô tả gốc của ticket.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `sendActionAppBookingV1` (`app/Helpers/functions.php:6427`) | **Có** — case `'3'`/`'5'` (đặt lịch trực tiếp) + case `'4'` (hủy trực tiếp): đổi nguồn đọc `slot_id`/`plan_slot_id` từ bản ghi JOIN course sang `BBooking::find()` | Root cause fix |
| 2 | `sendActionBookingV1` (`app/Helpers/functions.php:6011`) | Không | Dev đã check, không dính lỗi (không đọc qua bản ghi JOIN course bị ghi đè) |
| 3 | `sendActionBooking` (`app/Helpers/functions.php:6247`) | Không | Dev đã check, không dính lỗi |
| 4 | `MobileEventBookingController::saveUserBooking` (`app/Http/Controllers/Basic/MobileEventBookingController.php:1368`) | Không | Caller của hàm vừa sửa — Dev xác nhận không cần đổi, chỉ gọi hàm với tham số không đổi |
| 5 | `EventBookingService::handleOrderCallback` (`app/Services/EventBooking/EventBookingService.php:416`) | Không | Caller cho nhánh sự kiện có thu phí (callback thanh toán) — Dev xác nhận không cần đổi |
| 6 | `BookingEventDayController::saveAdminBooking` (`app/Http/Controllers/Basic/BookingEventDayController.php:2890`) | Không | Caller từ màn quản trị (đặt lịch hộ) — Dev xác nhận không cần đổi |
| 7 | `BookingEventDayController::saveActionBooking` (`app/Http/Controllers/Basic/BookingEventDayController.php:3774`) | Không | Caller từ màn quản trị (đổi trạng thái booking) — Dev ghi chú: **luồng đổi trạng thái từ màn quản trị vẫn chưa xét chế độ duyệt**, nhưng UI hiện không cho đặt trạng thái chờ duyệt nên chưa lộ lỗi |
| 8 | `HelperService` (`app/Services/HelperService.php:1094`) | Không | Dev đã check, không dính lỗi |

⚠️ Dev **không liệt kê** 2 nhánh đổi lịch (`isChange=true`) và sửa đơn đang chờ duyệt trong mục 3 này, nhưng Studio xác nhận (REQ-008) đây vẫn là code path đi qua cùng hàm `sendActionAppBookingV1` và còn cùng lớp lỗi — leader cần hỏi Dev có cố ý loại trừ hay bị sót.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `sendActionAppBookingV1` — case đặt lịch trực tiếp (`'3'`/`'5'`) | `app/Helpers/functions.php:6427` | Direct | Root cause fix — ảnh hưởng action LINE gửi khi Event ở chế độ リクエスト制 |
| F2 | `sendActionAppBookingV1` — case hủy trực tiếp (`'4'`) | `app/Helpers/functions.php:6427` | Direct | Cùng hàm, cùng cơ chế fix, nhánh hủy |
| F3 | `sendActionAppBookingV1` — case đổi lịch (`isChange=true`) | `app/Helpers/functions.php:6449-6451` | Indirect (NGOÀI phạm vi fix) | Cùng lớp lỗi, Dev chưa sửa — Studio đã test riêng (REQ-008), raise bug #41310 |
| F4 | `sendActionAppBookingV1` — case sửa lại đơn đang chờ duyệt | `app/Helpers/functions.php:6572-6576` | Indirect (NGOÀI phạm vi fix) | Cùng lớp lỗi, Dev chưa sửa — Studio đã test riêng (REQ-008), raise bug #41310 |
| F5 | `BookingEventDayController::saveActionBooking` — đổi trạng thái từ màn quản trị | `app/Http/Controllers/Basic/BookingEventDayController.php:3774` | Indirect | Dev tự nhận chưa xét chế độ duyệt; chưa lộ lỗi vì UI hiện không cho đặt trạng thái chờ duyệt — rủi ro tiềm ẩn nếu UI đổi sau này |
| F6 | `EventBookingService::handleOrderCallback` (đường có thu phí) | `app/Services/EventBooking/EventBookingService.php:416` | Indirect | Caller không đổi code, nhưng kết quả cuối (action gửi) vẫn phụ thuộc F1 — cần regression smoke cho sự kiện bật thu phí |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `action_lineuser.type_start_scenario` (cột lịch sử loại action) | UPDATE (hành vi ghi) | Giá trị ghi đổi theo cấu hình: đặt lịch 8001 (duyệt ngay) ↔ 8002 (gửi yêu cầu); hủy 8009 (hủy ngay) ↔ 8010 (gửi yêu cầu hủy). ⚠️ Journal Dev ghi "Không có data ảnh hưởng" nhưng đây **là** 1 thay đổi ghi dữ liệu (không phải chỉ hành vi gửi LINE) — Studio đã tạo 2 TC riêng (`NEW-17`/`NEW-18`) để verify giá trị DB này |
| D2 | `action_lineuser` (bản ghi action LINE được xếp hàng gửi) | CREATE | Đổi `action_id` được chọn để tạo bản ghi gửi — không phải sửa bản ghi cũ, mà đổi action nào được chọn khi tạo bản ghi mới |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Event Booking (FA-021) — đặt lịch mới khi sự kiện リクエスト制 + ưu tiên action theo course + đơn không có course | F1, D1, D2 | **High** — đây là bug chính |
| T2 | Event Booking (FA-021) — hủy lịch khi chế độ hủy リクエスト制 + ưu tiên action theo course + đơn không có course | F2, D1, D2 | **High** — bug chính, nhánh hủy |
| T3 | Event Booking (FA-021) — đặt/hủy lịch khi đơn CÓ course, hoặc ưu tiên action theo khung giờ | F1, F2 (đường không dính lỗi) | Medium — PHẢI test đối chứng để chứng minh fix không làm hỏng 2 đường vốn đã đúng |
| T4 | Event Booking (FA-021) — **đổi lịch** (`予約内容変更`) và **sửa đơn đang chờ duyệt**, cùng tổ hợp リクエスト制 + コース別アクション + không course | F3, F4 | **High, NGOÀI phạm vi fix #26763** — Studio đã phát hiện cùng lớp lỗi khi test, raise bug riêng **#41310**; Leader cần quyết định có đưa vào phạm vi task này hay tách ticket riêng |
| T5 | Event Booking (FA-021) — chế độ hủy 「不可」 khi friend đang ở màn xác nhận cancel, admin đổi setting giữa chừng | Ngoài mô tả gốc, phát hiện qua test boundary | **TC đã FAIL trên Studio** (`NEW-11`, bug **#41892**) — cần xác nhận đây là bug cũ hay do fix #26763 gây ra (regression), xem `04-tc-list.md` |
| T6 | Reminder Delivery (FA-022) | Theo đánh giá của Dev trong journal, chưa có bằng chứng code cụ thể | Low/Medium — action gửi kèm có thể chứa lệnh bật/tắt nhắc lịch; cần Leader xác nhận với Dev hoặc test smoke |
| T7 | Event Booking có thu phí (sự kiện bật thu phí, callback thanh toán) | F6 | Medium — Studio có 1 requirement (REQ-009) nhưng KHÔNG thấy TC tương ứng trong 17 TC fetch về (xem §1 report) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **đặc biệt hỏi Dev về nhánh đổi lịch (F3) và sửa đơn chờ duyệt (F4)** chưa được liệt kê ở mục 3 nhưng Studio phát hiện cùng lớp lỗi
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Quyết định rõ bug #41310 (đổi lịch/sửa đơn chờ duyệt) và #41892 (chặn hủy 「不可」) có thuộc phạm vi release/test của #26763 hay tách riêng** — ảnh hưởng tới §1/§6 của report review
