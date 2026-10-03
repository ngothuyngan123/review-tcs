# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug (LME Fix bug pipeline)` |
| Commit / Pull Request | `commit 925888559b (bản sửa job); PR #11148 đã merge vào origin/release_step_20260827 (3 commit lệnh recover)` |
| Branch | `ai_fixbug_41691` (nhánh gốc `release_step_20260827`) |
| Ngày submit đánh giá | `2026-09-29` |
| Auto-filled | `2026-09-29 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine (Journal #139163) và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Cron hằng ngày `job:syncEventYearlyGoogleCalendarSalon` (Kernel 02:15, lên release 2026-09-18) kéo dải sự kiện 1 năm kế tiếp từ Google Calendar về lịch salon. Trước khi tạo khung giờ chặn, job chỉ kiểm tra sự kiện đã có bản ghi chặn kéo về trước đó hay chưa (`existsSyncedGoogleEvent` tra bảng `calendar_salon_booking_by_google`), KHÔNG kiểm tra sự kiện đó có phải do chính công cụ đẩy lên từ một đơn đặt lịch hay không. Hàm tạo khung giờ chặn (`createBookingFromEvent`) cũng không có bước kiểm tra này. Kết quả: mọi sự kiện của đơn đặt lịch mà công cụ vừa đẩy lên Google Calendar đều bị kéo ngược về thành khung giờ chặn, trùng đúng giờ của đơn đã có nên hiển thị trùng và không đặt được. Với các liên kết có mốc hẹn nằm ở quá khứ, cửa sổ quét bắt đầu từ hiện tại nên toàn bộ đơn đặt lịch trong 1 năm tới bị phản ánh ngược trong một lượt cron. Ba luồng cùng loại còn lại (kéo lại khi khôi phục, kéo lịch của Đặt lịch bài học, xử lý thông báo thay đổi từ Google bên job Java) đều đã có bước kiểm tra này.

## 2. Cách fix

Sửa ĐÚNG tại job kéo lịch hằng năm theo yêu cầu human (bản sửa lần 1 đặt guard trong `createBookingFromEvent` đã revert): trong `CalendarSalonGoogleCalendarService::syncEventYearlyFromGoogle` — vòng lặp mà cron `job:syncEventYearlyGoogleCalendarSalon` chạy — thêm bước kiểm tra thứ hai ngay cạnh guard sẵn có: nếu mã sự kiện Google đang gắn với một đơn đặt lịch của chính lịch salon đó thì tính là đã đồng bộ, bỏ qua (`skipped++` và ghi log debug) chứ không tạo khung giờ chặn. Guard cũ `existsSyncedGoogleEvent` chỉ tra bảng khung giờ chặn nên không đỡ được ca này. Thêm `existsBookingSyncedToGoogleEvent` vào `CalendarSalonLineBookingRepository` + interface (khớp `calendar_salon_id` + `google_calendar_id` + `google_event_id`, không lọc `staff_id` vì đơn có thể để trống trong khi bản ghi liên kết lưu 0) và inject repo đó vào service dạng optional + tự resolve để không phá 2 call site `new CalendarSalonGoogleCalendarService()`. Kèm lệnh recover chạy tay `RecoverSalonBookingByGoogleReverseSync` (theo từng bot, mặc định `created_at >= 2026-09-18`) để dọn dữ liệu đã sinh sai.

[2026-09-29] `origin/release_step_20260827` đã merge PR #11148 (3 commit lệnh recover) — phần còn lại chưa vào release là commit `925888559b` (bản sửa job), branch đã push đầy đủ.

**Recover data (⚠ CÓ):** Chạy tay `php artisan job:RecoverSalonBookingByGoogleReverseSync --bot=<botId> --dry-run` rồi bỏ `--dry-run` để xoá thật. Lưu ý chạy recover trước khi có bản vá thì cron 02:15 hôm sau có thể sinh lại. Phạm vi: `calendar_salon_booking_by_google` + `calendar_salon_sync_booking_google_calendar_histories` (`type_model=2`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SyncEventYearlyGoogleCalendarSalon` (app/Console/Commands/SyncEventYearlyGoogleCalendarSalon.php) | Không đổi | Cron 02:15, trigger chính |
| 2 | `CalendarSalonGoogleCalendarService::syncEventYearlyFromGoogle` + `syncDueCalendarsYearly` | **Sửa — nơi thêm guard mới** | Vòng lặp mà cron chạy |
| 3 | `CalendarSalonLineBookingGoogleRepository::existsSyncedGoogleEvent` | Không đổi | Guard cũ — chỉ tra bảng khung giờ chặn, giữ nguyên nhiệm vụ chống trùng lượt cron lặp |
| 4 | `CalendarSalonGoogleCalendarService::createBookingFromEvent` | Không đổi (bản sửa lần 1 revert) | Hàm DÙNG CHUNG nhiều luồng — cố ý KHÔNG thêm guard ở đây |
| 5 | `CalendarSalonGoogleCalendarService::isEventAlreadySyncedToSalon` | **Mới — hàm guard** | Check event đã gắn đơn đặt lịch salon hay chưa |
| 6 | `CalendarSalonGoogleCalendarService::syncEventFromGoogle` | Không đổi | Lối vào thứ 2 (khi đổi liên kết Google) — KHÔNG có guard mới, giữ hành vi cũ |
| 7 | `CalendarSalonGoogleCalendarService::createBookingFromEventRecover` | Không đổi | Đối chứng — đã có sẵn bước kiểm tra tương tự |
| 8 | `CalendarSalonGoogleCalendarService::executeAddEventByBookingSalon` + `insertGoogleCalendarEvent` | Không đổi | Nơi lưu mã sự kiện Google lên đơn đặt lịch |
| 9 | `gCalendarController::syncEventToBlockTime` | Không đổi | Đối chứng lịch Bài học — đã có bước kiểm tra |
| 10 | `HandleSalonCalendarCallbackTask::handleCallbackEvent` | Không đổi (chỉ đọc) | Đối chứng job Java — đã có bước kiểm tra |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarSalonGoogleCalendarService::syncEventYearlyFromGoogle` | app/Services/CalendarSalon/CalendarSalonGoogleCalendarService.php | Direct | Thêm guard `existsBookingSyncedToGoogleEvent` ngay trước `createBookingFromEvent` trong vòng lặp event |
| F2 | `CalendarSalonGoogleCalendarService::isEventAlreadySyncedToSalon` | (cùng file) | Direct | Hàm mới |
| F3 | `CalendarSalonLineBookingRepository::existsBookingSyncedToGoogleEvent` | app/Repositories/Eloquents/CalendarSalonLineBookingRepository.php | Direct | Method mới, query 3 cột `calendar_salon_id` + `google_calendar_id` + `google_event_id`, KHÔNG lọc `staff_id` |
| F4 | `CalendarSalonLineBookingRepositoryInterface` | app/Contracts/Repositories/CalendarSalonLineBookingRepositoryInterface.php | Direct | Khai báo method mới |
| F5 | `CalendarSalonGoogleCalendarService::createBookingFromEvent` | (cùng file) | Indirect (KHÔNG sửa) | Hàm dùng chung — các luồng khác gọi hàm này (vd `syncEventFromGoogle`, callback Google) vẫn giữ nguyên hành vi cũ, KHÔNG có guard mới |
| F6 | `RecoverSalonBookingByGoogleReverseSync` | app/Console/Commands/RecoverSalonBookingByGoogleReverseSync.php | Direct | Lệnh recover chạy tay để dọn dữ liệu sinh sai |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_salon_booking_by_google` | UPDATE (chặn phát sinh mới) + DELETE (qua lệnh recover) | Fix chặn phát sinh khung giờ chặn sai mới; lệnh recover XOÁ các dòng đã sinh sai (khớp đơn đặt lịch theo `calendar_salon_id` + `calendar_id_google_calendar` + `event_id_google_calendar`) |
| D2 | `calendar_salon_sync_booking_google_calendar_histories` (`type_model=2`) | DELETE (qua lệnh recover) | Lệnh recover xoá dòng trỏ tới các khung giờ chặn bị xoá; giữ lại được bằng `--keep-history` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Salon Booking (FA-020) — cron kéo lịch 1 năm từ Google Calendar về lịch salon | F1, F2, F3, D1, D2 | High — không còn phản ánh ngược đơn đặt lịch do chính công cụ tạo, không nhân bản khung giờ chặn |
| T2 | Các luồng khác dùng chung `createBookingFromEvent` (kéo lịch khi đổi liên kết Google `syncEventFromGoogle`, callback Google) | F5 (KHÔNG sửa) | Medium — vẫn giữ hành vi cũ, cần verify KHÔNG regression theo hướng ngược (event tạo trực tiếp trên Google vẫn phải kéo về đúng) |
| T3 | Ca 2 nhân viên cùng liên kết 1 Google Calendar | F3 (không lọc `staff_id`) | High — rủi ro/regression trọng yếu: cần verify không bỏ chặn nhầm event người dùng tạo tay và không skip sai |

---

## TỰ REVIEW (AI) — nguyên văn từ Dev/AI-fixbug

Sửa đúng 1 điểm thiếu bước kiểm tra, tự chứa trên branch release, không đổi chữ ký hàm public nào. Hàm chỉ được gọi từ `syncEventFromGoogle` (job kéo lịch khi đổi liên kết Google) nên phạm vi ảnh hưởng gói trong luồng kéo lịch Salon từ Google.

**Rủi ro / lưu ý khi test (do AI tự nêu):**
- Trigger chính là cron `job:syncEventYearlyGoogleCalendarSalon` (lên release 2026-09-18, khách báo 2026-09-28 — khớp thời điểm). Guard sẵn có của job (`existsSyncedGoogleEvent`) chỉ chặn trùng bản ghi đã kéo về nên không đỡ được ca này; fix đặt ở `createBookingFromEvent`... (nguyên văn AI ghi "nên bao cả 2 lối vào" — ⚠️ lưu ý: theo mục 2/3 ở trên, fix thực tế đặt ở `syncEventYearlyFromGoogle`, KHÔNG phải `createBookingFromEvent` — bản sửa ở `createBookingFromEvent` đã bị revert. Câu này trong báo cáo AI có thể là sót lại từ bản nháp trước revert — cần Leader/Dev xác nhận lại). Nếu muốn tiết kiệm truy vấn có thể bổ sung cùng điều kiện ở tầng job, nhưng không bắt buộc.
- Sự kiện đã kéo về mà sau đó đổi giờ trên Google: lần kéo lại sẽ bỏ qua nên khung giờ chặn giữ giờ cũ. Thực tế cập nhật giờ đi qua luồng thông báo thay đổi của Google (job Java xoá rồi tạo lại) nên tự chuẩn lại; trước đây lần kéo lại sinh thêm bản ghi trùng chứ cũng không sửa giờ cũ.
- Lỗ hổng còn lại (KHÔNG sửa trong ticket này): khi người dùng kết nối lại tài khoản Google cho một nhân viên, `oauthCalendarSalon` gọi `deleteBookingSyncFromLme` xoá trắng mã sự kiện Google trên các đơn đặt lịch, nên nếu họ chọn lại đúng lịch Google cũ thì các sự kiện cũ không còn dấu vết để nhận ra và vẫn bị kéo về thành khung giờ chặn. Muốn bịt hẳn cần đánh dấu sự kiện do công cụ tạo (extendedProperties) hoặc không xoá liên kết khi kết nối lại cùng tài khoản — nên tách ticket riêng vì đường ghi sự kiện đang được chuyển sang job Java ở #41324.
- Chưa kiểm chứng được bằng dữ liệu thật (MySQL dev không kết nối được).
- Lệnh recover xoá dữ liệu thật: bắt buộc chạy `--dry-run` đối chiếu trước; đã giới hạn phạm vi bằng `--bot`/`--calendar` và `--max`, xoá theo lô `--chunk` để không giữ lock lâu. Chưa chạy thử được trên DB (dev không kết nối được) — nên chạy dry-run trên staging trước khi dùng cho khách.

**Verify của Dev (mức: lint — CHƯA chạy runtime):**
- Lệnh: `php -l` cả 4 file: No syntax errors detected.
- Kiểm binding interface→repository đã có sẵn ở RepositoryServiceProvider (dòng 385).
- Kiểm chỉ có 1 class implements `CalendarSalonLineBookingRepositoryInterface` nên thêm method vào interface không phá implementer khác.
- Kiểm 2 call site `new CalendarSalonGoogleCalendarService()` không truyền tham số → tham số repo mới là optional, không vỡ.
- **CHƯA chạy được runtime**: MySQL dev Connection refused, và bản checkout chính của source/sns-line đang tụt 492 commit nên không boot app để test container resolve được.
- Bằng chứng: Guard sẵn có `existsSyncedGoogleEvent` (CalendarSalonLineBookingGoogleRepository:83) chỉ tra `calendar_salon_booking_by_google` — đọc trực tiếp trên `release_step_20260827`; Cron `job:syncEventYearlyGoogleCalendarSalon`: Kernel.php:215 `dailyAt 02:15`, lên release 2026-09-18 (commit 250a522b08).

<!-- Nguồn: Journal #139163 (Redmine #41691, AI LME Fix bug, 2026-09-29) + đối chiếu với dev_impact/requirements của MCP LME TEST STUDIO task_get_context(task_id=340) — 10 REQ-xxx đã Studio suy sẵn, xem thêm ở 04-tc-list.md / dùng làm nháp nội bộ khi review. -->

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
