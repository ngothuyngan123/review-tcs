# 03 — Đánh giá ảnh hưởng từ Dev

> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.
>
> Nguồn: Redmine #40492 journal **#134074** — `AI LME Fix bug`, 2026-09-04 06:29 (báo cáo Auto-fixbug LME, **vòng 2**).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — human yêu cầu quét vòng 2 ngày 04-09 |
| Commit / Pull Request | commit `f50ab9bd1b` (repo `sns-line`) — *không có link PR trong Redmine* |
| Branch | `ai_fixbug_40492` (nhánh gốc `release_step_20260827`) — đã push origin |
| Ngày submit đánh giá | `2026-09-04` |
| Auto-filled | `2026-09-05 by /new-task` |

> Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=d6f1b899-fd90-4d96-8ac6-f82690af4626
> Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=40492

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Trường thông tin bạn bè kiểu lựa chọn có cài đặt vận hành 2 chế độ: chạy một lần hoặc chạy nhiều lần. Cột cờ trên bản ghi giá trị của bạn bè chỉ là dấu 'đã chạy một lần' của chế độ chạy một lần. Nhánh lưu giá trị của màn chat 1:1 lại chặn theo cờ này ở CẢ hai chế độ, nên bạn bè nào đã từng chạy hành động trước đó (ở ca này là do hành động của mã QR và của biểu mẫu tự đặt giá trị) thì mọi lần nhân viên sửa tay ở chat về sau đều không kích hoạt hành động gắn theo lựa chọn, tức không đổi trạng thái đối ứng và không bắt đầu phát theo bước. Cùng chỗ đó, câu lệnh ghi cờ 'đã chạy' lại so cột định danh bạn bè với định danh bot nên điều kiện không bao giờ khớp, cờ không được ghi. Các nơi làm đúng (luồng hành động dùng chung và màn chi tiết bạn bè bản mới) đều xét theo chế độ vận hành trước rồi mới xét cờ, nên vẫn chạy bình thường.

## 2. Cách fix

Vòng 2 (yêu cầu human 04-09): quét ngang TOÀN BỘ điểm chạy hành động của trường thông tin bạn bè rồi sửa triệt để, tổng 11 điểm trên 7 tệp (1 điểm ở lần trước + 10 điểm mới). Cùng một khuôn sửa ở mọi nơi: (1) điều kiện chạy hành động xét chế độ vận hành TRƯỚC — chạy nhiều lần thì luôn chạy, chỉ chế độ chạy một lần mới chặn theo cờ đã-chạy, đúng bản chuẩn ở hàm gửi hành động dùng chung và dịch vụ màn chi tiết bạn bè; (2) câu lệnh ghi cờ đã-chạy đang so cột định danh bạn bè với định danh bot được sửa thành đúng định danh bạn bè (6 điểm mắc lỗi này) để chế độ chạy một lần thực sự được ghi nhận, không chạy lặp. Các điểm mới sửa: luồng lưu thông tin bạn bè từ ỨNG DỤNG (2 API bản 1 và bản 2 — human chỉ định), màn quản trị lưu thông tin bạn bè, 5 luồng đặt lịch sự kiện (2 bản web theo sự kiện, 2 bản web theo ngày, 1 bản ứng dụng), hàm đặt giá trị thông tin bạn bè dùng chung (luồng trang mini nhận tham số) và nhánh lưu cũ của màn chat. Sửa thêm ở nhánh lưu cũ của màn chat: chỗ đọc bản ghi giá trị đang lấy theo mã bản ghi có thể còn sót của vòng lặp trước (nhánh cập nhật không gán lại mã) → đổi sang lấy theo cặp định danh bạn bè + trường, tránh đọc/ghi cờ nhầm bản ghi khi bản sửa này làm câu lệnh ghi cờ thực sự khớp. Nhóm điểm còn lại (biểu mẫu, bán hàng, đặt lịch salon/khoá học, sự kiện bản dịch vụ) dùng khuôn khác đã xét chế độ vận hành sẵn (chạy nhiều lần vẫn chạy) nên KHÔNG đụng.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn Dev (mục ■ 3):

```
ChatController::saveSettingDisplayInfoItem (app/Http/Controllers/ChatController.php) — chat 1:1 sửa từng trường, ĐÃ SỬA vòng 1
ChatController::saveSettingDisplayInfo (app/Http/Controllers/ChatController.php) — nhánh lưu cũ của chat (đường dẫn còn đăng ký, giao diện cũ không còn gọi), ĐÃ SỬA vòng 2 + lấy đúng bản ghi giá trị theo định danh bạn bè + trường
ChatController::saveSettingDisplayInfoV2 (app/Http/Controllers/ChatController.php) — chỉ lưu cấu hình hiển thị/thứ tự, KHÔNG chạy hành động → không liên quan (ghi nhận vòng 1 là nhầm hàm)
Api\FriendInformationController::saveCustomInfo + saveCustomInfo2 (app/Http/Controllers/Api/FriendInformationController.php) — API ỨNG DỤNG lưu thông tin bạn bè, ĐÃ SỬA vòng 2
Admin\BotController::saveCustomInfo (app/Http/Controllers/Admin/BotController.php) — màn quản trị lưu thông tin bạn bè, ĐÃ SỬA vòng 2
Basic\BookingEventController (2 nhánh) + Basic\BookingEventDayController (2 nhánh) + Api\BookingEventController (1 nhánh) — đặt lịch sự kiện ghi thông tin bạn bè rồi chạy hành động, ĐÃ SỬA vòng 2
setValueFriendInfo (app/Helpers/functions.php) — hàm đặt giá trị dùng chung, gọi từ LiffController (trang mini nhận tham số), ĐÃ SỬA vòng 2
sendAction nhánh thông tin bạn bè (app/Helpers/functions.php) + HelperService (app/Services/HelperService.php) + FriendDetailFriendInfoService::triggerFriendInfoAction — BẢN CHUẨN, đã đúng, dùng làm mẫu
Nhóm khuôn khác (KHÔNG sửa, đã xét chế độ vận hành): FormAnswerService (4 nhánh), Basic\FormAnswerController, EventBookingService (2), SalesService, SalesManagementV2Controller, SalesStripePaymentController, BookingManagerController, MobileEventBookingController (2), AppBookingCalendar, Api\BookingCalendar, Mobile\CalendarController, Mobile\CalendarSalonController, CalendarSalonLineBookingService, CalendarCourseBookingService
```

Chuyển sang bảng template:

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ChatController::saveSettingDisplayInfoItem` — `app/Http/Controllers/ChatController.php` | **ĐÃ SỬA (vòng 1)** | Chat 1:1 sửa từng trường — điểm tái hiện bug của ticket |
| 2 | `ChatController::saveSettingDisplayInfo` — `app/Http/Controllers/ChatController.php` | **ĐÃ SỬA (vòng 2)** + lấy bản ghi giá trị theo cặp `friend + field` thay vì theo mã bản ghi còn sót của vòng lặp | Nhánh lưu cũ của chat (route còn đăng ký, UI cũ không còn gọi) |
| 3 | `ChatController::saveSettingDisplayInfoV2` — `app/Http/Controllers/ChatController.php` | **KHÔNG sửa** | Chỉ lưu cấu hình hiển thị/thứ tự, không chạy action → không liên quan (*ghi nhận vòng 1 là nhầm hàm*) |
| 4 | `Api\FriendInformationController::saveCustomInfo` + `saveCustomInfo2` — `app/Http/Controllers/Api/FriendInformationController.php` | **ĐÃ SỬA (vòng 2)** | API ỨNG DỤNG lưu thông tin bạn bè (human chỉ định) |
| 5 | `Admin\BotController::saveCustomInfo` — `app/Http/Controllers/Admin/BotController.php` | **ĐÃ SỬA (vòng 2)** | Màn quản trị lưu thông tin bạn bè |
| 6 | `Basic\BookingEventController` (2 nhánh) · `Basic\BookingEventDayController` (2 nhánh) · `Api\BookingEventController` (1 nhánh) | **ĐÃ SỬA (vòng 2)** | Đặt lịch sự kiện ghi thông tin bạn bè rồi chạy action |
| 7 | `setValueFriendInfo` — `app/Helpers/functions.php` | **ĐÃ SỬA (vòng 2)** | Hàm đặt giá trị dùng chung, gọi từ `LiffController` (trang mini nhận tham số) |
| 8 | `sendAction` nhánh friend info — `app/Helpers/functions.php` · `HelperService` · `FriendDetailFriendInfoService::triggerFriendInfoAction` | **KHÔNG sửa — BẢN CHUẨN** | Đã đúng (xét chế độ vận hành trước rồi mới xét cờ), dùng làm mẫu để sửa các nơi khác |
| 9 | Nhóm khuôn khác: `FormAnswerService` (4 nhánh) · `Basic\FormAnswerController` · `EventBookingService` (2) · `SalesService` · `SalesManagementV2Controller` · `SalesStripePaymentController` · `BookingManagerController` · `MobileEventBookingController` (2) · `AppBookingCalendar` · `Api\BookingCalendar` · `Mobile\CalendarController` · `Mobile\CalendarSalonController` · `CalendarSalonLineBookingService` · `CalendarCourseBookingService` | **KHÔNG sửa** | Dùng khuôn khác đã xét chế độ vận hành sẵn (chạy nhiều lần vẫn chạy) → không dính lỗi của ticket |

---

## 4. Đánh giá ảnh hưởng

> Nguyên văn Dev (mục ■ 4):

```
■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/ChatController.php (2 điểm: sửa từng trường ở chat 1:1 + nhánh lưu cũ)
   - app/Http/Controllers/Api/FriendInformationController.php (2 điểm: API ứng dụng bản 1 và bản 2)
   - app/Http/Controllers/Admin/BotController.php (1 điểm: màn quản trị)
   - app/Http/Controllers/Basic/BookingEventController.php (2 điểm: đặt lịch sự kiện)
   - app/Http/Controllers/Basic/BookingEventDayController.php (2 điểm: đặt lịch sự kiện theo ngày)
   - app/Http/Controllers/Api/BookingEventController.php (1 điểm: đặt lịch sự kiện phía ứng dụng)
   - app/Helpers/functions.php (1 điểm: hàm đặt giá trị thông tin bạn bè dùng chung)
 • 4.2 Data ảnh hưởng:
   - Không đổi cấu trúc bảng, không sửa dữ liệu cũ. Từ bản fix này, cột cờ đã-chạy trên bảng giá trị thông tin bạn bè mới thực sự được ghi ở 6 luồng trước đây so nhầm cột định danh bạn bè với định danh bot (chat nhánh cũ, 5 luồng đặt lịch sự kiện, hàm dùng chung) — nghĩa là trường ở chế độ chạy một lần sẽ CHỈ chạy đúng một lần thay vì chạy lại mỗi lần ghi giá trị như trước.
 • 4.3 Tính năng liên quan:
   - 1-on-1 Chat (FA-001) — panel thông tin bạn bè: đổi tay giá trị kiểu lựa chọn kích hoạt đúng hành động theo chế độ vận hành
   - Friend Information (FA-015) — cài đặt vận hành chạy một lần / chạy nhiều lần được tôn trọng ở MỌI lối ghi giá trị: chat, màn quản trị, API ứng dụng, đặt lịch sự kiện, trang mini nhận tham số
   - Action Settings (SC-004) — hành động gắn theo lựa chọn (đổi trạng thái đối ứng) được gọi lại khi giá trị đổi ở mọi luồng trên
   - Step Delivery / Scenario (FA-009) — kịch bản phát theo bước gắn trong hành động của lựa chọn bắt đầu được từ mọi luồng trên
   - Event Booking (FA-021) — đặt lịch sự kiện (web theo sự kiện / web theo ngày / ứng dụng) ghi thông tin bạn bè: hành động chạy đúng chế độ vận hành, chế độ chạy một lần không còn chạy lặp mỗi lần đặt lịch
   - LIFF / trang mini (FA-011) — tham số trang đích ghi thông tin bạn bè qua hàm dùng chung: hành động chạy đúng chế độ vận hành
```

### 4.1. List function bị ảnh hưởng

> ⚠️ Dev ghi mục 4.1 là **"File thay đổi"** (7 tệp / 11 điểm sửa), không phải list function. Bảng dưới ghép mục 3 + 4.1 để ra list function.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `saveSettingDisplayInfoItem` (chat 1:1 sửa từng trường) | `app/Http/Controllers/ChatController.php` | Direct | Điểm tái hiện bug — sửa vòng 1 |
| F2 | `saveSettingDisplayInfo` (nhánh lưu cả cụm, đời cũ) | `app/Http/Controllers/ChatController.php` | Direct | Sửa vòng 2 + đổi cách lấy bản ghi giá trị (`friend + field`) |
| F3 | `saveCustomInfo` (API ứng dụng bản 1) | `app/Http/Controllers/Api/FriendInformationController.php` | Direct | Hợp đồng API mobile |
| F4 | `saveCustomInfo2` (API ứng dụng bản 2) | `app/Http/Controllers/Api/FriendInformationController.php` | Direct | Hợp đồng API mobile |
| F5 | `saveCustomInfo` (màn quản trị) | `app/Http/Controllers/Admin/BotController.php` | Direct | Màn chi tiết bạn bè 「マイページ」 |
| F6 | Đặt lịch sự kiện — web theo sự kiện (2 nhánh) | `app/Http/Controllers/Basic/BookingEventController.php` | Direct | |
| F7 | Đặt lịch sự kiện — web theo ngày (2 nhánh) | `app/Http/Controllers/Basic/BookingEventDayController.php` | Direct | |
| F8 | Đặt lịch sự kiện — bản ứng dụng (1 nhánh) | `app/Http/Controllers/Api/BookingEventController.php` | Direct | |
| F9 | `setValueFriendInfo` (hàm đặt giá trị dùng chung) | `app/Helpers/functions.php` | Direct | Đường gọi duy nhất: `LiffController` — QR landing / trang mini có tham số |
| F10 | `sendAction` (nhánh friend info) · `HelperService` · `FriendDetailFriendInfoService::triggerFriendInfoAction` | `app/Helpers/functions.php`, `app/Services/…` | Indirect | **Không sửa** — bản chuẩn dùng làm mẫu; regression phải xác nhận vẫn đúng |
| F11 | `saveSettingDisplayInfoV2` | `app/Http/Controllers/ChatController.php` | Indirect | Không chạy action → Dev kết luận không liên quan (**cần Leader xác nhận**, vì vòng 1 đã từng nhầm hàm này) |
| F12 | Nhóm khuôn khác (form / bán hàng / đặt lịch salon–khoá học / sự kiện bản dịch vụ) | nhiều file | Indirect | **Không sửa** — smoke regression 1 điểm đại diện |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Bảng giá trị thông tin bạn bè — **cột cờ "đã chạy"** | UPDATE (runtime, từ sau khi deploy) | Trước fix câu lệnh ghi cờ so **cột định danh bạn bè với định danh bot** → không dòng nào khớp, cờ **không bao giờ được ghi** ở 6 luồng (chat nhánh cũ, 5 luồng đặt lịch sự kiện, hàm dùng chung). Sau fix cờ ghi đúng → trường ở chế độ **chạy một lần** chỉ chạy **đúng 1 lần** thay vì lặp mỗi lần ghi giá trị |
| D2 | Cấu trúc bảng / dữ liệu cũ | **KHÔNG đổi** | Không migration, không sửa data cũ, không recover data |
| D3 | Bản ghi giá trị đọc ở nhánh lưu cũ của chat | READ (đổi điều kiện) | Đổi từ "lấy theo mã bản ghi (có thể sót từ vòng lặp trước)" → "lấy theo cặp **định danh bạn bè + trường**" → tránh đọc/ghi cờ **nhầm bản ghi** khi lưu nhiều trường cùng lúc |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **1-on-1 Chat (FA-001)** — panel thông tin bạn bè: đổi tay giá trị kiểu lựa chọn kích hoạt đúng action theo chế độ vận hành | F1, F2, D1, D3 | **High** |
| T2 | **Friend Information (FA-015)** — cài đặt vận hành chạy một lần / chạy nhiều lần được tôn trọng ở MỌI lối ghi giá trị: chat, màn quản trị, API ứng dụng, đặt lịch sự kiện, trang mini nhận tham số | F1–F9, D1 | **High** |
| T3 | **Action Settings (SC-004)** — action gắn theo lựa chọn (đổi trạng thái đối ứng) được gọi lại khi giá trị đổi ở mọi luồng trên | F1–F9 | **High** |
| T4 | **Step Delivery / Scenario (FA-009)** — kịch bản phát theo bước gắn trong action của lựa chọn bắt đầu được từ mọi luồng trên | F1–F9 | **High** |
| T5 | **Event Booking (FA-021)** — đặt lịch sự kiện (web theo sự kiện / web theo ngày / ứng dụng) ghi thông tin bạn bè: action chạy đúng chế độ, chế độ chạy một lần không còn chạy lặp mỗi lần đặt lịch | F6, F7, F8, D1 | **Medium** |
| T6 | **LIFF / trang mini (FA-011)** — tham số trang đích ghi thông tin bạn bè qua hàm dùng chung: action chạy đúng chế độ | F9 | **Medium** |

---

## 5. Recover data (Dev ghi thêm)

```
■ 5. RECOVER DATA
   ✔ Không cần recover data
```

## 6. Verify của Dev

```
■ 6. VERIFY
   Mức: lint
   Lệnh: php -l cho cả 7 tệp đã sửa: No syntax errors detected; vendor/bin/phpunit tests/Unit: OK (11 tests, 22 assertions) — không có test bao phủ luồng thông tin bạn bè; git diff --stat origin/release_step_20260827...ai_fixbug_40492: 7 tệp, 100 thêm / 31 bớt — đúng phạm vi quét ngang; grep lại toàn repo: không còn điểm nào dùng khuôn 'chặn theo cờ đã-chạy ở cả 2 chế độ' và không còn câu lệnh ghi cờ nào so định danh bạn bè với định danh bot
   Bằng chứng: Bản chuẩn đối chiếu: app/Helpers/functions.php (sendAction, nhánh thông tin bạn bè) + app/Services/HelperService.php + app/Services/FriendDetailFriendInfoService.php::triggerFriendInfoAction — đều xét chế độ vận hành trước rồi mới xét cờ.; Basic\FriendInformationController (lưu cài đặt trường) xoá cờ đã-chạy của mọi bạn bè khi chuyển trường sang chế độ chạy nhiều lần — xác nhận cờ chỉ dùng cho chế độ chạy một lần.; Nhóm KHÔNG sửa dùng khuôn khác: chế độ chạy một lần thì chỉ chạy khi chưa từng có bản ghi giá trị, chế độ chạy nhiều lần luôn chạy — không dính lỗi của ticket (chạy nhiều lần vẫn chạy). Tiêu chí 'chưa từng có giá trị' khác với cờ đã-chạy, ghi nhận để BA xem lại sau, không đụng trong ticket này.; MySQL dev (host.docker.internal:3306) không kết nối được nên chưa chạy end-to-end.
```

## Tự review của AI (nguyên văn — ⚠️ chứa rủi ro test)

```
■ TỰ REVIEW (AI)
Sửa gọn trong đúng một khối điều kiện của nhánh lưu giá trị ở chat 1:1. Điều kiện mới bám sát 2 bản chuẩn đã có trong mã nguồn (hàm chạy hành động dùng chung + dịch vụ màn chi tiết bạn bè) và bám sát spec về ý nghĩa cài đặt vận hành. Không đổi cấu trúc dữ liệu, không đụng luồng khác, không sửa số phiên bản tệp cấu hình.
 • Rủi ro / lưu ý khi test:
   - Trường ở chế độ chạy nhiều lần: từ nay mỗi lần đổi tay ở chat đều chạy hành động — đúng cấu hình, nhưng nếu hành động có gửi tin thì lượng tin gửi ra tăng theo số lần nhân viên sửa. Đây chính là hành vi khách yêu cầu và đã đúng ở các màn khác.
   - Trường ở chế độ chạy một lần: trước đây câu lệnh ghi cờ sai điều kiện nên hành động bị chạy LẶP mỗi lần sửa ở chat; sau fix chỉ chạy đúng một lần theo cài đặt. Đây là siết lại cho đúng spec nhưng là thay đổi hành vi thấy được, cần nêu khi bàn giao test.
   - Nếu trường của khách đang để chế độ chạy một lần thì việc không kích hoạt lại là đúng cài đặt; khi đó cần hướng dẫn khách chuyển sang chế độ chạy nhiều lần — và bản fix này bảo đảm chuyển xong thì chat thực sự chạy lại được.
   - Không kết nối được cơ sở dữ liệu dev nên chưa chạy thử end-to-end; mới dừng ở lint + đối chiếu 2 bản chuẩn và spec.
```

## Branch / Commit (để QA checkout)

```
■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_40492 (nhánh gốc release_step_20260827, commit f50ab9bd1b, 7 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 11 phút 4 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=d6f1b899-fd90-4d96-8ac6-f82690af4626
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=40492
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### ⚠️ Điểm Leader cần soi kỹ (auto-flag bởi `/new-task`, chưa verify)

| # | Điểm nghi vấn | Nguồn |
|---|---|---|
| 1 | **Dev CHƯA chạy end-to-end** — "MySQL dev (host.docker.internal:3306) không kết nối được nên chưa chạy end-to-end". Mới dừng ở `php -l` + đối chiếu bản chuẩn. `vendor/bin/phpunit tests/Unit` OK nhưng **không có test bao phủ luồng friend info** | mục ■ 6 VERIFY |
| 2 | **Behavior change thấy được ở chế độ chạy MỘT LẦN** — trước fix action chạy **lặp** mỗi lần sửa ở chat, sau fix chỉ chạy **đúng 1 lần**. Không phải bug gốc của ticket nhưng là thay đổi hành vi → **bắt buộc có TC regression** | mục TỰ REVIEW |
| 3 | **Chế độ chạy nhiều lần + action có gửi tin** → lượng tin gửi ra **tăng theo số lần nhân viên sửa**. Đúng cấu hình nhưng cần TC xác nhận không spam ngoài ý muốn | mục TỰ REVIEW |
| 4 | **Fix generic quét ngang 11 điểm / 7 tệp** — 10 điểm mới sửa vòng 2 **không nằm trong luồng tái hiện bug**. Cần TC verify từng nhóm điểm, không chỉ chat 1:1 | mục ■ 2 |
| 5 | **Nhóm KHÔNG sửa dùng tiêu chí khác** — "chưa từng có bản ghi giá trị" ≠ "cờ đã-chạy". Dev tự ghi nhận *"để BA xem lại sau, không đụng trong ticket này"* → **spec ambiguity còn treo** | mục ■ 6 VERIFY |
| 6 | `saveSettingDisplayInfoV2` bị loại khỏi phạm vi với lý do "không chạy action" — trong khi **vòng 1 đã từng nhầm hàm** ở đúng chỗ này → nên xác nhận lại | mục ■ 3 |
