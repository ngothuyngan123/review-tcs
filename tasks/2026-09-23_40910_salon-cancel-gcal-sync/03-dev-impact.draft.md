# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #40910 — **Journal #138011 (AI LME Fix bug, 2026-09-23)** — báo cáo Auto-fixbug LME bản mới nhất (thay thế Journal #137774).
>
> ⚠️ **DRAFT** — sinh bởi `/new-task` ngày 2026-09-24 vì `03-dev-impact.md` đã tồn tại. Thay đổi so với bản cũ: thêm mục **2d** (bỏ migration index `2026_09_21_100001`) + **2e** (TỰ REVIEW v2) · commit mới `d937091e12` (10 file) · mục 3 thêm #15 → #19 · F9 gạch bỏ · D4 đổi nội dung · thêm D8, D9 · T6 đổi nội dung · thêm T7. Human merge tay vào file chính.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Đỗ Quyên |
| Commit / Pull Request | commit `d937091e12` (trước đó `8f1781ae67`; `34025588db` bỏ migration index) — phiên AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=4b9056c7-93eb-49d0-aeb4-64a8d5d01d63 · dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=40910 |
| Branch | `ai_fixbug_40910` (repo `sns-line`, nhánh gốc `release_step_20260827`, **10 file**) — **đã push**. Branch mang thêm commit của ticket con **#41376** (gộp branch theo quy tắc bug con) |
| Ngày submit đánh giá | `2026-09-23` (Commit Date custom field: 2026-09-23) |
| Auto-filled | `2026-09-24 by /new-task` (refresh từ Journal #138011) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi hủy đặt lịch salon, Elme gọi xóa sự kiện trên Google Calendar nhưng hàm xóa **BỎ QUA IM LẶNG** nếu không tra được bản ghi liên kết Google của lịch/nhân viên đó hoặc token rỗng — không báo lỗi, không ghi bản ghi retry nên **không bao giờ thử lại**.

Thêm nữa cách **tra liên kết lúc xóa lỏng hơn lúc tạo** (đặt lịch không chỉ định nhân viên thì lấy nhầm liên kết đầu tiên của lịch, tức tài khoản Google khác) nên xóa hụt. Sự kiện vì vậy nằm lại trên Google Calendar.

Do 2 lịch salon (khách mới / hội viên) dùng **CHUNG một Google Calendar**, lịch còn lại vẫn giữ **bản sao chặn giờ** kéo từ Google — bản sao này chỉ bị xóa khi Google báo sự kiện đã hủy, mà điều đó không bao giờ xảy ra, nên đặt lịch đã hủy vẫn hiện ở lịch khách mới và **không sửa/xóa được từ Elme** (nó không phải đặt lịch của Elme).

## 2. Cách fix

### 2a. Refix theo AI review vòng 2 (1 lỗi bắt buộc) — index cho câu DELETE

Câu DELETE dọn bản sao chặn giờ (`deleteBlockTimeByGoogleEventId`, lọc `bot_id` + `calendar_id_google_calendar` + `event_id_google_calendar`) **KHÔNG dùng được index nào** của bảng `calendar_salon_booking_by_google` — rà cả 3 migration của bảng thì chỉ có `PRIMARY(id)` và `idx_csbbg_salon_staff_event` (dẫn đầu là `calendar_salon_id`), không index nào dẫn đầu bằng `bot_id`.

DELETE không dùng index sẽ **quét toàn bảng VÀ đặt next-key/gap lock** trên mọi dòng quét qua (kể cả khi không khớp dòng nào), đúng sự cố **#38446**; mà câu này chạy ở **MỌI lần hủy đặt lịch salon** (Basic/Mobile/Api) và trong job retry, trên bảng tích lũy rất lớn đang bị job đồng bộ Google insert liên tục ⇒ **hủy lịch chậm, nguy cơ timeout/deadlock**.

→ Đã thêm migration `2026_09_21_100001` tạo index `idx_csbbg_bot_gcal_event (bot_id, calendar_id_google_calendar, event_id_google_calendar)` — **GIỮ NGUYÊN logic** và giữ điều kiện `bot_id` (đúng rule giới hạn theo bot), **không** đổi sang xóa theo `calendar_salon_id` vì mục đích fix là dọn bản sao ở MỌI lịch salon dùng chung Google Calendar. Không cần xóa theo lô (mỗi lần chỉ khớp vài dòng của đúng 1 sự kiện).
⚠️ **Lưu ý deploy**: tạo index trên bảng lớn nên chạy **giờ thấp điểm**.

### 2b. BỔ SUNG theo chốt của human — hủy lịch khi bật phân bổ nhân viên tự động (ランダム / 設定順)

Lịch loại này chọn nhân viên **VÀ** tạo sự kiện Google ở **job nền** `CalendarSalonStaffAssignment(Admin)`, nên hủy ngay lúc job chưa xong thì **lệnh xóa chạy TRƯỚC lệnh tạo** ⇒ xóa hụt rồi job tạo sự kiện sau khi đã hủy (đặt lịch ma trên Google + bản sao chặn giờ ở lịch dùng chung).

Đã thêm:

1. Cột `calendar_salon_line_booking.staff_assignment_status` (`0` = không/đã xong, `1` = đang xử lý phân bổ) + 2 hằng số trong model; **đặt cờ NGAY TRƯỚC khi dispatch job** ở cả **4 điểm** (Mobile controller + Api controller + 2 chỗ trong `CalendarSalonLineBookingService`), **gỡ cờ trong khối `finally`** của 2 job nên lỗi job cũng không kẹt cờ.
2. Job mới `CalendarSalonCancelDeleteGoogleEvent`: còn cờ thì **hẹn lại mỗi 10 giây (tối đa 30 lần = 5 phút)**, hết cờ mới gọi `deleteEventByBookingId` — tức việc xóa xếp hàng chạy **TUẦN TỰ SAU** khi random xong; **quá 5 phút mà cờ vẫn bật** (job phân bổ chết / queue dừng) thì **vẫn xóa + ghi log lỗi**, để không bỏ sót sự kiện của đặt lịch đã hủy.
3. Method mới `CalendarSalonGoogleCalendarService::deleteEventByBookingIdAfterStaffAssignment` quyết định xóa ngay hay xếp hàng, và **5 điểm HỦY** đặt lịch gọi method này (Mobile cancel tự duyệt, Api `approveCancel` + `adminCancel`, service `approveCancel` + `adminCancel`).

**Các điểm KHÔNG đổi**: đổi nhân viên thủ công (Api 2846 / service 4761) và xóa cả lịch salon (Basic 3053) vẫn gọi thẳng như cũ vì **không phải luồng hủy**.

Trạng thái đặt lịch + lịch sử + tin nhắn vẫn chạy **đồng bộ như cũ** (khách thấy hủy ngay), chỉ phần đồng bộ Google bị hoãn.

### 2c. TỰ REVIEW v1 (2026-09-22) — sửa thêm 1 lỗi BẮT BUỘC còn sót ở đường RETRY

Đường RETRY (`RetryCalendarSalonGoogleCalendarSync::executeDeleteEventByStoredInfo`) vẫn tra liên kết Google theo **cách LỎNG cũ** (bot + lịch salon, chỉ lọc staff khi `staff_id` khác null) — **đúng như lỗi gốc của ticket**: mọi luồng hủy gọi `deleteEventByBookingId` với `usingToken=0` nên `access_token` lưu trong `google_calendar_event_info` là NULL, job retry buộc phải tra lại và **lại bốc nhầm tài khoản Google khác** ⇒ Google trả **404/403**, sự kiện + bản sao chặn giờ vẫn nằm lại (mà **retry chính là đường chạy trong kịch bản ticket** vì lần xóa đầu đã lỗi).

Đã:
1. Đổi `findGoogleCalendarConnectionForEvent` từ `private(booking)` sang `public(botId, googleCalendarId, bookingCalendarId, staffId)` — giữ nguyên logic **chấm điểm ưu tiên** đúng lịch salon + đúng nhân viên — và dùng **CHUNG** cho cả luồng xóa chính lẫn job retry (booking đã bị force-delete thì lấy `bot_id`/`calendar_id` từ `result_error_google`).
2. **Chỉ ghi token làm mới trở lại bản ghi liên kết khi token được lấy TỪ chính bản ghi đó**, tránh đè token của nhân viên / tài khoản Google khác.

Commit `[ai-selfreview #40910] 8f1781ae67`.

### 2d. CẬP NHẬT 2026-09-23 (yêu cầu human) — BỎ migration index

**ĐÃ BỎ** migration `2026_09_21_100001` tạo index `idx_csbbg_bot_gcal_event` trên `calendar_salon_booking_by_google` (commit `34025588db`) — không chạy migrate index này nữa. Logic KHÔNG đổi: `deleteBlockTimeByGoogleEventId` vẫn lọc `bot_id` + `calendar_id_google_calendar` + `event_id_google_calendar`.

⚠️ Hệ quả phải biết khi release: câu DELETE này không còn index phủ (bảng chỉ có `PRIMARY(id)` + `idx_csbbg_salon_staff_event` dẫn đầu `calendar_salon_id`) nên sẽ quét toàn bảng và đặt next-key/gap lock trên các dòng quét qua ở MỌI lần hủy đặt lịch salon — rủi ro chậm/timeout/deadlock như sự cố **#38446**. Nếu cần bù: để DBA thêm index thủ công lúc thấp điểm, hoặc đổi điều kiện DELETE sang bộ cột đã có index. Branch cũng đang mang commit của ticket con #41371 (gộp branch theo quy tắc bug con) — *đã đính chính ở 2e: là #41376*.

### 2e. TỰ REVIEW v2 (2026-09-23)

1. **SỬA lỗi BẮT BUỘC do việc bỏ migration index đẻ ra** — `deleteBlockTimeByGoogleEventId` nay **xóa theo TỪNG liên kết Google** (`calendar_salon_id` + `staff_id` + `event_id_google_calendar`, vẫn giữ `bot_id` + `calendar_id_google_calendar`) nên khớp TRỌN index sẵn có `idx_csbbg_salon_staff_event`, KHÔNG cần migration nào và hết cảnh quét toàn bảng + next-key/gap lock ở mọi lần hủy đặt lịch (rủi ro kiểu #38446 mà chính report đã cảnh báo).
   - Cơ sở: bản sao chặn giờ luôn sinh từ một liên kết `b_c_salon_google_calendar` (`createBookingFromEvent` copy nguyên `booking_calendar_id` + `staff_id`), và 3 nơi khác trong hệ thống đã xóa đúng theo bộ cột này (job linect, `JobRecoverSalonSyncBookingGoogle`, `deleteBookingByGoogleCalendar`).
   - Có **nhánh dự phòng** quay về câu lọc rộng nếu bot không còn liên kết nào trỏ vào Google Calendar đó.
2. **Xóa dòng `Log::debug(json_encode($gCalendar))`** trong `executeDeleteEventByBookingSalon` — dump cả bản ghi liên kết nghĩa là ghi `access_token`/`refresh_token` Google ra file log (`APP_LOG_LEVEL` mặc định debug).
3. Sửa report: ticket con gộp branch là **#41376** (KHÔNG phải #41371 — #41371 đã REJECTED, không có commit trên branch).

Commit `[ai-selfreview #40910] d937091e12`.

⚠️ **LƯU Ý RELEASE**: phải chạy migration `2026_09_21_100002` **TRƯỚC** khi deploy code, vì lệnh đọc cột `staff_assignment_status` nằm ngoài try/catch (thiếu cột = **500 mọi thao tác hủy đặt lịch salon**).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonGoogleCalendarService::executeDeleteEventByBookingSalon` (`app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php`) | Sửa | Điểm bỏ qua im lặng khi không tra được liên kết / token rỗng |
| 2 | `CalendarSalonGoogleCalendarService::deleteEventByBookingId` (cùng file) | Sửa | Entry point xóa sự kiện Google của mọi luồng hủy |
| 3 | `CalendarSalonGoogleCalendarService::deleteBlockTimeByGoogleEventId` (cùng file) | **MỚI THÊM** | Dọn bản sao chặn giờ ngay sau khi xóa sự kiện Google |
| 4 | `CalendarSalonGoogleCalendarService::getGoogleCalendarConfig` / `executeAddEventByBookingSalon` | Đối chiếu | So cách tra liên kết **lúc tạo** (chặt hơn) với lúc xóa |
| 5 | `CalendarSalonGoogleCalendarService::createBookingFromEvent` / `createBookingFromEventRecover` | Đối chiếu | Nguồn sinh bản ghi chặn giờ |
| 6 | `Api/CalendarSalonController::actionBooking` | Sửa | Nhánh `approveCancel` / `adminCancel` gọi xóa sự kiện → chuyển sang method có xếp hàng |
| 7 | `Basic/CalendarSalonController::deleteCalendarSalon` | Không đổi | Xóa lịch salon, gọi xóa sự kiện theo vòng lặp — không phải luồng hủy |
| 8 | `RetryCalendarSalonGoogleCalendarSync::handle` / `executeDeleteEventByStoredInfo` | Sửa (self-review v1) | Job thử lại khi xóa lỗi — vẫn tra liên kết theo cách lỏng cũ |
| 9 | `HandleErrorGoogleSpreadSheet::handle` | Đối chiếu | Cron 1 phút/lần đẩy bản ghi lỗi sang job retry |
| 10 | `HandleSalonCalendarCallbackTask::handleCallbackEvent` (linect) | Đối chiếu | **Nơi DUY NHẤT** xóa bản sao chặn giờ trước fix — chỉ chạy khi Google báo sự kiện đã hủy |
| 11 | `CalendarSalonGoogleCalendarService::deleteBookingSyncFromLme` | Đối chiếu (self-review v1) | Luồng gỡ liên kết Google gọi `deleteEventByBookingId` theo vòng lặp |
| 12 | `CalendarSalonLineBookingService::changeStaffAssignment` (~:4847) | Không đổi (self-review v1) | Đổi nhân viên thủ công, cũng gọi `deleteEventByBookingId` — không phải luồng hủy |
| 13 | `CalendarSalonGoogleCalendarService::findGoogleCalendarConnectionForEvent` | **MỚI — nay `public`** | Dùng chung cho luồng xóa chính + job retry |
| 14 | `Basic/CalendarSalonController::getDetailHistorySyncForBooking` / `getListHistorySyncBookingGoogleCalendar` | Đối chiếu | Màn **Google同期履歴** đọc bảng lịch sử đồng bộ |
| 15 | `CalendarSalonGoogleCalendarService::deleteEventByBookingIdAfterStaffAssignment` | **MỚI** (tự review v2) | 5 điểm hủy gọi, quyết định xóa ngay hay xếp hàng |
| 16 | `App\Jobs\CalendarSalonCancelDeleteGoogleEvent::handle` | **MỚI** (tự review v2) | Hẹn lại 10s × 30 lần chờ phân bổ nhân viên xong |
| 17 | `CalendarSalonStaffAssignment::handle` / `CalendarSalonStaffAssignmentAdmin::handle` | Sửa (tự review v2) | Thêm `finally` gỡ cờ `staff_assignment_status` |
| 18 | 4 điểm dispatch job phân bổ đặt cờ: `Mobile/CalendarSalonController:2660`, `Api/CalendarSalonController:1873`, `CalendarSalonLineBookingService:4123` + `:5231` | Sửa (tự review v2) | grep `"new CalendarSalonStaffAssignment"` = đúng 4 hit, không sót |
| 19 | `CalendarSalonBookingByGoogleService::deleteBookingByGoogleCalendar` + `JobRecoverSalonSyncBookingGoogle` + linect `CalendarSalonBookingByGoogleRepository` | Đối chiếu (tự review v2) | 3 tiền lệ ĐÚNG dùng để đối chứng cách xóa bản sao chặn giờ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev kê theo **file thay đổi** (mục 4.1 gốc). Bảng dưới giữ nguyên danh sách file + quy về tag `F*` để map coverage.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarSalonGoogleCalendarService` (xóa sự kiện, dọn bản sao chặn giờ, tra liên kết Google) | `app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php` | Direct | Gồm `deleteBlockTimeByGoogleEventId` (mới), `deleteEventByBookingIdAfterStaffAssignment` (mới), `findGoogleCalendarConnectionForEvent` (mới, public) |
| F2 | Job thử lại đồng bộ Google Calendar lịch salon | `app/Jobs/RetryCalendarSalonGoogleCalendarSync.php` | Direct | Sửa cách tra liên kết + không đè token của tài khoản khác |
| F3 | Job **MỚI** xếp hàng xóa sự kiện sau khi phân bổ nhân viên xong | `app/Jobs/CalendarSalonCancelDeleteGoogleEvent.php` | Direct (mới) | Hẹn lại mỗi 10s, tối đa 30 lần = 5 phút, hết hạn vẫn xóa + ghi log lỗi |
| F4 | Job phân bổ nhân viên tự động | `app/Jobs/CalendarSalonStaffAssignment.php` / `CalendarSalonStaffAssignmentAdmin.php` | Direct | Gỡ cờ trong khối `finally` |
| F5 | Model đặt lịch salon | `app/CalendarSalonLineBooking.php` | Direct | 2 hằng số trạng thái phân bổ |
| F6 | Controller ứng dụng admin (mobile) | `app/Http/Controllers/Mobile/CalendarSalonController.php` | Direct | Đặt cờ khi dispatch + điểm hủy gọi method có xếp hàng |
| F7 | Controller API | `app/Http/Controllers/Api/CalendarSalonController.php` | Direct | Đặt cờ khi dispatch + `approveCancel` / `adminCancel` |
| F8 | Service đặt lịch LINE salon | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | Direct | 2 chỗ dispatch job (đặt cờ) + `approveCancel` / `adminCancel` gọi method có xếp hàng |
| ~~F9~~ | ~~Migration thêm index~~ | ~~`database/migrations/2026_09_21_100001_add_index_bot_gcal_event_to_calendar_salon_booking_by_google_table.php`~~ | **ĐÃ BỎ** (commit `34025588db`, 2026-09-23) | Không còn trong danh sách file thay đổi của Journal #138011 |
| F10 | Migration thêm cột | `database/migrations/2026_09_21_100002_add_staff_assignment_status_to_calendar_salon_line_booking_table.php` | Direct (MỚI) | Thêm cột `staff_assignment_status` |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_booking_by_google` | DELETE | Xóa các dòng chặn giờ có cùng `bot_id` + `calendar_id_google_calendar` + `event_id_google_calendar` **ngay sau khi sự kiện bị xóa khỏi Google** (trước đây **chỉ callback Google** mới xóa) |
| D2 | `result_error_google` | CREATE | Phát sinh thêm dòng lỗi (`type 4`, `is_update=2`) khi xóa sự kiện thất bại vì thiếu liên kết / token, để job retry xử lý |
| D3 | `b_c_salon_google_calendar` | (đọc) | **Không đổi cấu trúc**; chỉ đổi cách **TRA** bản ghi (ưu tiên khớp đúng `staff_id`) |
| D4 | `calendar_salon_booking_by_google` — **KHÔNG thêm index** | (không migrate) | Migration `2026_09_21_100001` **đã bị bỏ** theo yêu cầu human 2026-09-23. Tự review v2 đổi câu DELETE dọn bản sao chặn giờ sang xóa theo **TỪNG liên kết Google** (`calendar_salon_id` + `staff_id` + `event_id_google_calendar`) nên khớp trọn index sẵn có `idx_csbbg_salon_staff_event` ⇒ **KHÔNG còn** quét toàn bảng / next-key-gap lock, không cần DBA thêm index thủ công |
| D5 | `calendar_salon_line_booking.staff_assignment_status` (tinyint, default `0`) | MIGRATE + UPDATE | `0` = không/đã xong, `1` = đang xử lý phân bổ nhân viên. Bản ghi cũ mặc định `0` nên luồng hủy **giữ nguyên hành vi cũ**. ⚠️ `ALTER TABLE` trên bảng đặt lịch **rất lớn** ⇒ chạy giờ thấp điểm cùng lúc với migration index *(nguyên văn Dev — migration index nay đã bỏ)* |
| D6 | Hàng đợi job (bảng `jobs`, connection `database`, queue `default`) | CREATE | Phát sinh thêm job `CalendarSalonCancelDeleteGoogleEvent` **mỗi lần hủy đặt lịch ĐANG chờ phân bổ nhân viên**; mỗi lần hẹn lại là 1 job mới (**tối đa 30 job / đặt lịch trong 5 phút**) |
| D7 | `calendar_salon_sync_booking_google_calendar_histories` | (KHÔNG ghi — nợ kỹ thuật) | **KHÔNG được dọn/ghi thêm** khi xóa bản sao chặn giờ: dòng lịch sử `type_model=2` trỏ tới bản ghi `calendar_salon_booking_by_google` vừa bị xóa trở thành **mồ côi**; màn **Google同期履歴** mất dấu vết lần dọn này (linect khi Google báo `cancelled` thì xóa KÈM ghi history `status 3`). Không gây lỗi màn hình (`getDetailHistorySyncForBooking` dùng `->value('staff_id')` nên chỉ trả `null`) — ghi nhận ở tự review v1 |
| D8 | Thứ tự deploy | (release) | **PHẢI chạy migration `2026_09_21_100002` TRƯỚC khi deploy code** — `deleteEventByBookingIdAfterStaffAssignment` đọc cột `staff_assignment_status` ngoài try/catch, thiếu cột ⇒ **500 ở MỌI thao tác hủy đặt lịch salon** (bổ sung ở tự review v2) |
| D9 | `calendar_salon_sync_booking_google_calendar_histories` — dòng `type_model=2` mồ côi | (chưa xử lý — chờ quyết định) | Tự review v2 xác nhận **KHÔNG dọn được an toàn** (bảng history chỉ có index `(calendar_salon_id, staff_id)`, xóa theo `booking_id` sẽ tái tạo đúng hazard quét toàn bảng). **Cần human/DBA quyết**: ghi 1 dòng history `status 2` thay vì xóa, hoặc thêm index cho history |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Salon Booking (FA-020)** — hủy / xóa đặt lịch salon | F1, F2, D1, D2 | **High** — nay xóa dứt điểm sự kiện trên Google Calendar và dọn bản sao chặn giờ ở các lịch salon dùng chung Google Calendar |
| T2 | **Lesson / Calendar Booking (FA-019)** | (không sửa) | **Low** — KHÔNG sửa; Dev **ghi nhận có cùng kiểu bỏ qua im lặng** ở luồng xóa sự kiện Google của đặt lịch bài học |
| T3 | **Salon Booking (FA-020)** — phân bổ nhân viên tự động (ランダム / 設定順), luồng **HỦY** | F3, F4, F5, F6, F7, F8, D5, D6 | **High** — hủy đặt lịch trong lúc job phân bổ đang chạy nay **đợi phân bổ xong mới xóa** sự kiện Google, không còn đặt lịch ma. **RETEST**: lịch salon đặt `staff_assignment_type = random`, đặt lịch rồi **hủy NGAY (trong ~10–30 giây)** → kiểm tra Google Calendar không còn sự kiện và lịch salon khác dùng chung Google Calendar không còn khung giờ bị chặn |
| T4 | **Salon Booking (FA-020)** — luồng **ĐẶT** lịch (khách đặt qua LIFF + admin đặt hộ) trên lịch bật phân bổ nhân viên tự động | F6, F7, F8, D5 | **Medium** — 4 điểm dispatch job phân bổ có thêm 1 `UPDATE` đặt cờ `staff_assignment_status` **ngay trước dispatch**. **RETEST**: đặt lịch bình thường trên lịch random / 設定順 (cả LIFF lẫn admin đặt hộ) phải **vẫn gán được nhân viên + tạo sự kiện Google như cũ** — bổ sung ở tự review v1 |
| T5 | **Salon Booking (FA-020)** — màn **Google同期履歴** (lịch sử đồng bộ) | D7 | **Low** — dòng lịch sử `type_model=2` trở thành mồ côi khi bản sao chặn giờ bị xóa; không gây lỗi màn hình nhưng **mất dấu vết** lần dọn |
| T6 | **Hiệu năng hủy đặt lịch salon + job đồng bộ Google** (mọi bot) | D4, D8 | **Medium** — migration index đã bỏ; câu DELETE nay xóa theo từng liên kết Google, khớp index sẵn có `idx_csbbg_salon_staff_event` (tránh quét toàn bảng kiểu #38446). Có **nhánh dự phòng lọc rộng** khi bot không còn liên kết nào trỏ vào Google Calendar đó. Thứ tự deploy: migration `100002` trước code (D8) |
| T7 | **Salon Booking (FA-020)** — 3 luồng **GIÁN TIẾP** dùng chung `deleteEventByBookingId` | F1 | **Medium** — cũng đổi hành vi (bổ sung ở tự review v2): **xóa cả lịch salon** (`Basic:3065`), **đổi nhân viên thủ công** (`Api:2872` / `Service:4871`), **gỡ liên kết Google** (`deleteBookingSyncFromLme`) — nay cũng dọn bản sao chặn giờ và sinh dòng lỗi retry khi thiếu liên kết/token thay vì im lặng. **RETEST 3 luồng này** |

---

## 5. RECOVER DATA (từ báo cáo Dev)

⚠️ **CÓ** — Các sự kiện **mồ côi đã tồn tại** trên Google Calendar của khách (ví dụ 桑田様 9/24 11:30) và bản sao chặn giờ tương ứng trong `calendar_salon_booking_by_google` **KHÔNG tự biến mất sau khi deploy** — fix **chỉ chặn ca phát sinh mới**.

Sau khi khách xóa sự kiện trực tiếp trên Google Calendar, cần kiểm tra lại bảng `calendar_salon_booking_by_google` của bot này và xóa dòng còn sót nếu callback Google không dọn được.

**Phạm vi**: Bot `エッコネイル広島京橋店` — 1 sự kiện đã biết; **nên rà thêm các bot có nhiều lịch salon cùng trỏ 1 `google_calendar_id`**.

## 6. VERIFY (mức Dev đã làm)

- **Mức**: `lint` (chỉ lint, KHÔNG chạy test / KHÔNG tái hiện được trên dev).
- **Lệnh**: `php -l app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php` → No syntax errors detected; `git diff --stat origin/release_step_20260827...ai_fixbug_40910` → 1 file, +95/-19.
- **Bằng chứng**:
  - ⚠️ **Không kiểm chứng được bằng DB dev**: MySQL `host.docker.internal:3306` Connection refused (dev stack không chạy) — **không tái hiện được trên dev**, kết luận dựa trên **đọc code 2 repo**.
  - Cron `handle:googleSpreadSheet` chạy `everyMinute` (`app/Console/Kernel.php:238`) → dispatch `RetryCalendarSalonGoogleCalendarSync` cho bản ghi `result_error_google` type `CALENDAR_SALON_CALENDAR` ⇒ lỗi ném ra thật sự được thử lại, **tối đa 5 lần** rồi báo Chatwork.
  - linect-service `HandleSalonCalendarCallbackTask.handleCallbackEvent`: bản sao chặn giờ **CHỈ** bị xóa ở nhánh event `status = cancelled` ⇒ sự kiện không bị xóa khỏi Google thì bản sao **nằm lại vĩnh viễn**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
