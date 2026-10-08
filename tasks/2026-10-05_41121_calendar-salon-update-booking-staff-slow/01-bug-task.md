# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41121 — [AI][Performance] POST /basic/calendar-salon/staff/update-booking-page-display-staff chậm max 471s (2 lần/24h)` |
| Module / Màn hình | Đặt lịch Salon (FA-020) — API tắt/bật hiển thị nhân viên trên trang đặt lịch `POST /basic/calendar-salon/staff/update-booking-page-display-staff` (công tắc 「予約ページ表示」 trong màn 「スタッフ作成・編集」, tab chi tiết lịch salon). Feature Studio: `calendar-salon`. |

## Mô tả bug (bản dịch tiếng Việt)

Ticket **tự tạo bởi hệ thống check-performance AI** (từ report request chậm bắn lên Chatwork room 417532006), **không phải khách hàng báo trực tiếp**. Không có "Steps to reproduce" thủ công — đây là cảnh báo đo hiệu năng tổng hợp từ log request thật.

**Endpoint:** `POST /basic/calendar-salon/staff/update-booking-page-display-staff`

- Mức: **high** — xếp theo độ chậm (max 471s trong kỳ; >30s cao · 15–30s trung bình · ≤15s thấp); điểm xếp thứ tự 65.
- Số lần chậm 24h: **2** (kỳ trước 0, 1h qua 2) — xu hướng **new**.
- Thời gian: **max 471s** · p95 471s · trung bình 268s · median 471s.
- Phân bố: ≥15s SUPPERSLOW **2** · 10–15s VERYSLOW **0** · 5–10s SLOWLV1 **1**.
- User bị ảnh hưởng: 1 (tổng 2).
- Server: `step.lme.jp` — BotId: `189563, 125959`.
- Lần đầu: 2026-09-15 10:57 UTC — Lần cuối: 2026-09-18 09:45 UTC.
- Lịch sử dài hạn: tổng 3 lần chậm trong 2 ngày, đỉnh 2 lần/24h, chậm nhất 471s, từ 2026-09-15 10:57 UTC.

**Vì sao ưu tiên này:**
- Độ chậm: p95 471s — treo gần như timeout (+45 điểm).
- Tần suất: 2 lần/24h (+2 điểm).
- User ảnh hưởng: 1 user bị chậm (+3 điểm).
- Độ mới: vừa xảy ra trong 1h qua (+12 điểm).
- Xu hướng: mới xuất hiện (kỳ trước 0 lần, nay 2) (+3 điểm).
- Journal #138068 (2026-09-24, ai-exception detect-bug): nâng độ ưu tiên theo quy định 2.1 → **Immediate** (có request treo ≥300s → coi như endpoint chết, cần xử lý ngay).

**URL mẫu:** `/basic/calendar-salon/staff/update-booking-page-display-staff`.

**Các lần chậm nhất đã ghi nhận** (nguyên văn Redmine):

| Giây | Thời điểm (VN) | Mức | User | URL |
|---|---|---|---|---|
| 471 | 2026-09-18 16:45 | SUPPERSLOW | 87535 | /basic/calendar-salon/staff/update-booking-page-display-staff |
| 65 | 2026-09-18 16:45 | SUPPERSLOW | 87535 | /basic/calendar-salon/staff/update-booking-page-display-staff |
| 5 | 2026-09-15 17:57 | SLOWLV1 | 113683 | /basic/calendar-salon/staff/update-booking-page-display-staff |

**Nguồn cảnh báo trong source:** Middleware `NotifyChatworkRequestTimeSlow` (web, >4s) và `MobileAuthenticate` (API mobile) gọi `notifySlowRequestCommon()` — `app/Helpers/functions.php:11093`: ≥5s SLOWLV1, ≥10s VERYSLOW, ≥15s SUPPERSLOW.

## Steps to reproduce

⚠️ Không có steps thủ công — ticket do AI check-performance phát hiện qua thống kê thời gian request thật, không phải khách hàng report theo flow UI cụ thể. Theo đánh giá của Dev (journal, xem `03-dev-impact.md`), độ chậm phụ thuộc **khối lượng dữ liệu đồng bộ Google Calendar đã tích luỹ của nhân viên** (số lượt đặt đã đồng bộ + số dòng lịch sử đồng bộ, có thể tới hàng triệu dòng), không phải 1 thao tác đơn lẻ nào tái hiện được 100% trên data rỗng.

Dev đã sửa theo hướng: đẩy TOÀN BỘ việc gỡ liên kết Google Calendar (xoá sự kiện trên Google + dọn dữ liệu đồng bộ theo lô) ra khỏi request, chạy nền qua job riêng ở connection/queue riêng (`database_salon_google` / `salonGoogleUnlink`). Xem chi tiết ở `03-dev-impact.md`.

## Expected result

- Request `POST /basic/calendar-salon/staff/update-booking-page-display-staff` hoàn tất nhanh (ngưỡng tham chiếu theo thang check-performance: **dưới 5 giây**), không phụ thuộc khối lượng dữ liệu đồng bộ Google đã tích luỹ của nhân viên.
- Việc gỡ liên kết Google Calendar luôn chạy **ngoài request**, qua hàng đợi riêng `salonGoogleUnlink`.

## Actual result

- Request tắt hiển thị nhân viên từng chậm tới **471 giây** (tối đa), p95 **471 giây**, lặp lại **2 lần/24h** và mới xuất hiện — gần như timeout, ảnh hưởng tới user có nhiều dữ liệu đồng bộ Google tích luỹ.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

Không có attachment trên Redmine #41121 (0 attachment) — log request chậm đã trích nguyên văn ở "Mô tả bug" phía trên (lấy từ description gốc, hệ thống check-performance AI tự log).

## Ghi chú thêm của Leader

- ⚠️ Ticket do **AI check-performance tự tạo** từ thống kê request chậm, không phải CS/khách hàng báo — không có bước tái hiện thủ công, không có screenshot/video.
- Môi trường phát hiện: **Production** (`step.lme.jp`).
- Ticket status hiện tại: `Fix done - Đợi test`. Dev fix **1 journal duy nhất** (#137390, 2026-09-21) nhưng tự nêu rõ đây là **"sửa lần 2"** theo quyết định vận hành của human — nền tảng lần 1 (đưa việc gỡ Google ra khỏi request) giữ nguyên, lần 2 chỉ đổi cách cách ly job (connection/queue riêng + bỏ guard kiểm cờ hiển thị + thêm `failed()`). Không có journal riêng cho lần 1 — toàn bộ lịch sử gộp trong 1 note. Xem đầy đủ ở `03-dev-impact.md`.
- ⚠️ **Hành vi có đổi (đã được human chốt 2026-09-21, KHÔNG phải spec cũ)**: sau khi tắt hiển thị (đẩy job vào hàng đợi), bật hiển thị lại **KHÔNG huỷ được** việc gỡ liên kết Google — liên kết vẫn bị gỡ khi job chạy, muốn dùng lại phải liên kết Google lại từ màn cấu hình nhân viên. TC phải verify đúng hành vi MỚI này, không áp expected "giống trước fix" (bài học #40128 → #41448 — xem RULE liên quan ở `framework/checklist-lme.md`).
- ⚠️ **BẮT BUỘC vận hành**: cần worker riêng cho queue mới — `php artisan queue:work database_salon_google --queue=salonGoogleUnlink`. Thiếu worker ⇒ job nằm im vĩnh viễn, liên kết Google không bao giờ được gỡ dù UI báo thành công.
- Branch fix: `ai_small_41121` (gốc `release_step_20260827`, commit `f02a52db01`, 5 file, 224 dòng thêm / 7 dòng xoá, 2 commit). Toàn bộ nội dung "Đánh giá ảnh hưởng" đã chuyển sang `03-dev-impact.md`.
- Studio đã có task review-ready cho ticket này (task **#349**, feature `calendar-salon`, round 1, 20 TC do AI sinh: **18 Đạt / 0 Không đạt / 2 Skip** (NEW-3 cần tài khoản Google thật + app LINE thật — manual; NEW-11 chờ PO chốt expected cho case liên kết lại Google trong lúc job cũ còn chờ) — xem `04-tc-list.md`. `reviewState` hiện là `leader` (đang chờ Leader duyệt).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `189563, 125959` |
| Friend / User bị ảnh hưởng (mẫu) | `87535` (2 lần SUPPERSLOW 471s/65s cùng thời điểm) · `113683` (1 lần SLOWLV1 5s) |
| Đối tượng cấu hình | Nhân viên salon bị tắt hiển thị trên trang đặt lịch (`booking_page_display=0`), có liên kết Google Calendar + nhiều dữ liệu đồng bộ tích luỹ |
| Thời điểm lỗi | Chậm nhất: `2026-09-18 16:45 VN` (471s, cùng user với lần 65s ngay sau) |
| Đối chứng | Không có case chạy đúng (<5s) được ghi trong ticket để so sánh trực tiếp — chỉ có 1 lần SLOWLV1 (5s) làm mốc thấp nhất đã cảnh báo |

## Journal / note từ Redmine (nguyên văn)

**Journal #137390 — AI LME Fix bug — 2026-09-21:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi tắt hiển thị nhân viên trên trang đặt lịch (booking_page_display=0), endpoint chạy TOÀN BỘ việc gỡ liên kết Google Calendar ngay trong request: xoá từng sự kiện trên Google cho mọi lượt đặt đã đồng bộ (mỗi lượt = 1 lần gọi HTTP sang Google + 3 câu truy vấn), rồi xoá theo lô toàn bộ dữ liệu đồng bộ và lịch sử đồng bộ (bảng lịch sử có thể tới hàng triệu dòng cho 1 salon/nhân viên). Khối lượng việc tỉ lệ thuận với dữ liệu tích luỹ và không có trần. Tệ hơn: bảng lịch sử đồng bộ và bảng lượt đặt salon đều KHÔNG có index theo (salon, nhân viên) nên câu tìm lượt đặt quét toàn bảng, còn vòng xoá theo lô thì MỖI lô lại quét toàn bảng + khoá khoảng — xoá hàng triệu dòng trở thành chi phí bậc hai. Nhân viên có nhiều lịch sử đồng bộ thì request treo tới 471s.

■ 2. CÁCH FIX
Sửa lần 2 theo quyết định human: (1) BỎ chốt kiểm cờ hiển thị trong job — đã đẩy vào hàng đợi là CHẮC CHẮN gỡ liên kết Google, người dùng bật hiển thị lại trong lúc chờ cũng không huỷ được, muốn dùng lại thì liên kết Google lại từ màn cấu hình nhân viên; (2) chuyển job sang connection + queue RIÊNG (database_salon_google / salonGoogleUnlink) thay vì database/default để việc nặng không chiếm worker dùng chung — connection mới cùng bảng jobs nhưng retry_after=7200 > timeout job 3600 nên job dài không bị nhả ra chạy trùng và không sinh bản ghi failed_jobs giả; (3) thêm failed() ghi logError + notifyChatworkException để dev biết khi job hỏng giữa chừng (tries=1 nên dữ liệu có thể dọn dở). Nền tảng lần 1 giữ nguyên: toàn bộ khối gỡ liên kết Google ra khỏi request (request chỉ lưu cờ hiển thị rồi trả JSON y hệt cũ) + 2 migration index (calendar_salon_id, staff_id) cho calendar_salon_sync_booking_google_calendar_histories và calendar_salon_line_booking.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
Basic\CalendarSalonController::updateBookingPageDisplayStaff (app/Http/Controllers/Basic/CalendarSalonController.php:1181)
App\Jobs\CalendarSalonDeleteGoogleSyncStaff::handle (app/Jobs/CalendarSalonDeleteGoogleSyncStaff.php)
CalendarSalonGoogleCalendarService::deleteBookingSyncFromLme (app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php:413)
CalendarSalonGoogleCalendarService::deleteEventByBookingId + executeDeleteEventByBookingSalon (cùng file, ~161/~952)
CalendarSalonBookingByGoogleService::deleteBookingByGoogleCalendar + deleteInChunks (app/Services/CalendarSalon/CalendarSalonBookingByGoogleService.php:101/124)
CalendarSalonStaffService::updateBookingPageStaff (app/Services/CalendarSalon/CalendarSalonStaffService.php:84)
updateBookingPageDisplayStaff (public/js/calendar_salon/calendar_detail.js:2057 — phía gọi, sau khi success chỉ reload danh sách nhân viên)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/CalendarSalonController.php
   - app/Jobs/CalendarSalonDeleteGoogleSyncStaff.php
   - config/queue.php
   - database/migrations/2026_09_18_110001_add_index_salon_staff_to_calendar_salon_sync_booking_google_calendar_histories_table.php
   - database/migrations/2026_09_18_110002_add_index_salon_staff_to_calendar_salon_line_booking_table.php
 • 4.2 Data ảnh hưởng:
   - calendar_salon_line_booking.google_event_id / google_calendar_id — vẫn xoá (set null) như cũ, chạy nền; thêm index (calendar_salon_id, staff_id)
   - calendar_salon_sync_booking_google_calendar_histories — vẫn xoá theo lô như cũ, chạy nền; thêm index (calendar_salon_id, staff_id)
   - calendar_salon_booking_by_google — vẫn xoá theo lô như cũ, chạy nền
   - bc_salon_google_calendars — bản ghi liên kết Google của nhân viên vẫn bị xoá, sau khi job chạy xong; bật hiển thị lại KHÔNG cứu được bản ghi này (quyết định human 2026-09-21)
   - jobs — job mới nằm ở queue riêng salonGoogleUnlink (vẫn bảng jobs); failed_jobs — chỉ ghi khi job thật sự hỏng
 • 4.3 Tính năng liên quan:
   - Salon Booking (FA-020) — tắt hiển thị nhân viên trên trang đặt lịch: phản hồi ngay; việc gỡ liên kết Google Calendar chạy nền ở hàng đợi riêng và không thể huỷ bằng cách bật hiển thị lại
   - Salon Booking (FA-020) — gỡ liên kết Google thủ công / callback OAuth / xoá nhân viên: không sửa code, nhanh hơn nhờ 2 index mới

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: runtime-data
   Lệnh: php -l 3 file sửa lần 2 (job, controller, config/queue.php): No syntax errors detected; Boot Laravel trong worktree: tries=1, timeout=3600, CONNECTION=database_salon_google, QUEUE=salonGoogleUnlink; config('queue.connections.database_salon_google') resolve OK, retry_after=7200 > timeout job 3600 (không bị re-reserve chạy trùng), queue mặc định của connection = salonGoogleUnlink, class = Illuminate\Queue\DatabaseQueue; Xác nhận đã bỏ hẳn guard booking_page_display khỏi job; method failed() tồn tại; helper notifyChatworkException tồn tại; git diff --stat release_step_20260827...ai_small_41121: 5 file, 224 thêm / 7 bớt (2 commit)
   Bằng chứng: Không EXPLAIN được trên dev: MySQL host.docker.internal:3306 'Connection refused' — kết luận thiếu index dựa trên migration 2 bảng + lesson #38446 (EXPLAIN cũ: type=ALL, key=NULL, rows=42358); Migration index của #39523 có commit nhưng KHÔNG có trong cây release_step_20260827 (rơi khi merge) ⇒ bảng histories thật sự chưa có index ngoài PRIMARY; tên index mới không trùng; Quy ước queue riêng đã có sẵn trong repo (googleEvent, googleFormAnswer, countView) nên cách đặt queue riêng là nhất quán

■ TỰ REVIEW (AI)
Lần 2 chốt theo quyết định vận hành của human: teardown là một chiều (đã queue là xoá), cách ly hẳn sang connection+queue riêng, và có đường báo lỗi khi job hỏng. Đơn giản hơn lần 1 (bỏ hẳn nhánh guard) và xử lý luôn 3 cảnh báo của AI reviewer vòng 1 (queue dùng chung, timeout > retry_after, thiếu failed()).
 • Rủi ro / lưu ý khi test:
   - ⚠ BẮT BUỘC ops: phải thêm worker cho queue mới, ví dụ `php artisan queue:work database_salon_google --queue=salonGoogleUnlink` (supervisor). Nếu không có worker lắng nghe, job nằm im vĩnh viễn ⇒ liên kết Google KHÔNG bị gỡ dù đã tắt hiển thị.
   - Hành vi có đổi (đã được human chốt): tắt rồi bật lại ngay thì liên kết Google vẫn bị gỡ — người dùng phải liên kết Google lại. Cần PM/CS biết để trả lời khách.
   - Bất đồng bộ: từ lúc trả về tới khi job xong, tab Google連携 của nhân viên còn hiện đang liên kết trong chốc lát.
   - tries=1: job hỏng giữa chừng thì dọn dở và không tự chạy lại — nay đã có failed() ghi log + báo Chatwork để dev xử lý tay.
   - Tạo index trên 2 bảng rất lớn: chạy migration vào giờ thấp điểm (đã ghi cảnh báo trong migration).

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41121 (nhánh gốc release_step_20260827, commit f02a52db01, 5 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 13 phút 6 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=7344dbc8-4395-4d88-af37-823c2ffcf045
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41121
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

**Journal #138068 — ai-exception detect-bug — 2026-09-24:**

```
check-performance: bổ sung độ ưu tiên theo quy định 2.1 → *Immediate*
* Mức endpoint "high" (chậm nhất trong kỳ 471s) → High
* ⬆️ Nâng lên Urgent: Có request treo ≥ 60s — user gần như chắc chắn bỏ cuộc / timeout
* ⬆️ Nâng lên Immediate: Có request treo ≥ 300s — coi như endpoint chết, cần xử lý ngay
```
