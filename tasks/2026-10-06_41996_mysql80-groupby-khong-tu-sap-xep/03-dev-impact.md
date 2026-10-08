# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug pipeline) |
| Commit / Pull Request | commit `de5e4b3d53` (19 file, đã push lên origin, chưa merge) |
| Branch | `ai_small_41996` (nhánh gốc `release_step_20260930_v2`) |
| Ngày submit đánh giá | 2026-10-05 |
| Auto-filled | 2026-10-06 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

MySQL 5.7 tự sắp xếp kết quả theo cột GROUP BY khi câu không có ORDER BY; MySQL 8.0 bỏ hẳn hành vi này nên các danh sách, phân trang, file CSV và câu `count()` kèm `groupBy` (lấy dòng đầu) đang dựa vào thứ tự đó sẽ trả về lộn xộn, có thể khác nhau giữa các lần chạy và gây lặp/sót dòng khi phân trang.

## 2. Cách fix

Thêm `ORDER BY` tường minh theo đúng cột `GROUP BY` (chính thứ tự MySQL 5.7 đang ngầm áp dụng) cho 31 chỗ gọi `groupBy` ở 19 file trong ticket: danh sách thành viên tag, lọc người nhận, lọc nâng cao + xuất CSV bạn bè (màn, API, job, `getConversationBlocked`), giá trị thông tin bạn bè (phân tích chéo, quản lý thông tin bạn bè), 3 danh sách QR/landing, khối thời gian nhân viên, ngày slot sự kiện, khoá học lịch bài học, affiliate/bot free/hủy hợp đồng phía admin, `getListUrlInMessage`, `countScenario`.

`orderBy` được đặt **CUỐI chuỗi** (sau sắp xếp do người dùng chọn) nên chỉ làm khoá phụ khi đã có sort.

**Bỏ qua 4 vị trí** báo cáo nhận nhầm vì đã có ORDER BY sẵn (`BookingManagerController:4480`, `AffiliaterController::ajaxAffMoneyV2`, `ConversionController::visitedConversion`) hoặc code chết (`HandleExportCsv2`).

Quét ngang: các bản Replicate chết + vị trí phía job/MCP ghi vào yokoten (**không nằm trong phạm vi fix #41996**).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TagController::member` (app/Http/Controllers/Basic/TagController.php) | Thêm `orderBy` theo `line_user.id` | Màn thành viên tag |
| 2 | `FilterController::ajaxGetListUserFilter` (app/Http/Controllers/Basic/FilterController.php) | Thêm `orderBy` theo `line_user.id` | Modal lọc người nhận broadcast/scenario |
| 3 | `FriendlistController::filterAdvance` + `csvExport` 4 nhánh (app/Http/Controllers/Basic/FriendlistController.php) | Thêm `orderBy` theo `bot_line_user.id` | Lọc nâng cao có phân trang 200/trang + export CSV |
| 4 | `CrossAnalysisController::getDataFriendInfo` + danh sách giá trị (app/Http/Controllers/Basic/CrossAnalysisController.php) | Thêm `orderBy` theo `value` | Phân tích chéo STEP 1 |
| 5 | `Api\ListFriendController` export CSV (app/Http/Controllers/Api/ListFriendController.php) | Thêm `orderBy` theo `bot_line_user.id` | API export CSV theo bộ lọc |
| 6 | `Conversation::getConversationBlocked` (app/Conversation.php) | Thêm `orderBy` theo `conversation.id` | Caller: `CsvManagementController`, `HandleExportCsv`, `HandleUpdateLatestInformationCsv`, `ListFriendController` |
| 7 | `HandleExportCsv::handle` nhánh lọc (app/Console/Commands/HandleExportCsv.php) | Thêm `orderBy` theo `bot_line_user.id` | Job export CSV nền |
| 8 | `QRCodeController::poster url list` / `collectFriend` / `detailClickDay` (app/Http/Controllers/Basic/QRCodeController.php) | Thêm `orderBy` (3 nhánh) | QR/LP v2 — data detail 3 tab |
| 9 | `BookingManagerController::ajaxFilterBookingByCondition` (app/Http/Controllers/Basic/BookingManagerController.php) | **CÓ sửa**: thêm `orderBy` theo 6 cột `groupBy` | Lọc lịch theo khoá học/nhân viên |
| 10 | `BookingManagerController::getListTimeBlockByCondition` | Đã có `orderBy`, **không sửa** | Đối chứng an toàn |
| 11 | `BookingEventDayController::ajaxAllBooking` (app/Http/Controllers/Basic/BookingEventDayController.php) | Thêm `orderBy` theo `date_start_from` | Danh sách ngày slot sự kiện |
| 12 | `Api\CalendarLessonController::getListReceptionCourse` | Thêm `orderBy` | API lịch bài học (mobile) |
| 13 | `FriendInformationController::exportCsv` + `initDataItemInfo` (app/Http/Controllers/Basic/FriendInformationController.php) | Thêm `orderBy` (2 nhánh default) | 友だち情報管理（情報一覧） |
| 14 | `Category::getCategoryTagDefaultByKeyWord` (app/Category.php) | Thêm `orderBy` | Tìm tag mặc định theo từ khoá ở タグ管理 |
| 15 | `Url::getListUrlInMessage` (app/Url.php) | Thêm `orderBy` | Caller: `TalkListController`, `ErrorListController` |
| 16 | `countScenario` (app/Helpers/functions.php) | Thêm `orderBy` — Laravel `aggregate()` kèm `groupBy` trả dòng đầu | Caller: `CreateOrUpdateScenarioStepMessage`, `RecoverUpdateStatusScenarioLineuser`, `functions.php:12320`, `ScenarioMobileController`, `ScenarioController`, `StepMessageController` (2227, 3456), `StepMessageSpec` (luồng huỷ hợp đồng) |
| 17 | `AffiliateManagementController::getListCondition` + `getConditionOfAllBot` (app/Http/Controllers/Admin/AspManagement/AffiliateManagementController.php) | Thêm `orderBy` (2 hàm) | ASP管理 — danh sách điều kiện + dropdown mọi bot |
| 18 | `BotV2Controller::getListBotFree` (app/Http/Controllers/Admin/BotV2Controller.php) | Thêm `orderBy` theo `bots.id` | Thêm bot — bước chọn bot free để ký hợp đồng |
| 19 | `SupperAdminController::affiliateTransfer` (app/Http/Controllers/Admin/SupperAdminController.php) | Thêm `orderBy` | Chuyển khoản affiliate (siêu quản trị) |
| 20 | `UserController::ajaxCommentReasonCancelContract` (app/Http/Controllers/Admin/UserController.php) | Thêm `orderBy` (2 câu `usersPayment`/`usersPaymentCmt`) | 解約理由 theo tháng |
| 21 | `AffiliaterController::ajaxAffMoneyV2`, `ConversionController::visitedConversion` | Đã có `orderBy`, **không sửa** | Đối chứng an toàn |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `TagController::member` | app/Http/Controllers/Basic/TagController.php | Direct | Tag Management (FA-012) |
| F2 | `FilterController::ajaxGetListUserFilter` | app/Http/Controllers/Basic/FilterController.php | Direct | Broadcast / scenario — modal lọc người nhận cũ |
| F3 | `FriendlistController::filterAdvance` + `csvExport` | app/Http/Controllers/Basic/FriendlistController.php | Direct | Friend List (FA-013) |
| F4 | `CrossAnalysisController::getDataFriendInfo` + danh sách giá trị | app/Http/Controllers/Basic/CrossAnalysisController.php | Direct | Cross Analysis (FA-024) |
| F5 | `Api\ListFriendController` export CSV | app/Http/Controllers/Api/ListFriendController.php | Direct | API export CSV bạn bè |
| F6 | `Conversation::getConversationBlocked` | app/Conversation.php | Indirect (dùng chung) | Caller: CsvManagementController, HandleExportCsv, HandleUpdateLatestInformationCsv, ListFriendController |
| F7 | `HandleExportCsv::handle` | app/Console/Commands/HandleExportCsv.php | Direct | Job nền — CSV Management (FA-014) |
| F8 | `QRCodeController` — poster/collectFriend/detailClickDay | app/Http/Controllers/Basic/QRCodeController.php | Direct | QR Code Action / Landing Page (FA-017), 3 nhánh |
| F9 | `BookingManagerController::ajaxFilterBookingByCondition` | app/Http/Controllers/Basic/BookingManagerController.php | Direct | Booking manager (lọc khối thời gian nhân viên) |
| F10 | `BookingEventDayController::ajaxAllBooking` | app/Http/Controllers/Basic/BookingEventDayController.php | Direct | Event Booking (FA-021) |
| F11 | `Api\CalendarLessonController::getListReceptionCourse` | app/Http/Controllers/Api/CalendarLessonController.php | Direct | Lesson/Calendar Booking (FA-019) — API mobile |
| F12 | `FriendInformationController::exportCsv` + `initDataItemInfo` | app/Http/Controllers/Basic/FriendInformationController.php | Direct | Friend Information (FA-015) |
| F13 | `Category::getCategoryTagDefaultByKeyWord` | app/Category.php | Direct | Tag Management (FA-012) — tìm tag theo từ khoá |
| F14 | `Url::getListUrlInMessage` | app/Url.php | Indirect (dùng chung) | Caller: TalkListController, ErrorListController — URL Analytics (FA-023) |
| F15 | `countScenario` | app/Helpers/functions.php | Indirect (dùng chung, nhiều caller) | Step Delivery/Scenario (FA-009) — ghi `scenario.count_follow/count_stop/count_unfinish` |
| F16 | `AffiliateManagementController::getListCondition` + `getConditionOfAllBot` | app/Http/Controllers/Admin/AspManagement/AffiliateManagementController.php | Direct | ASP管理 — Affiliate Payment Mgmt (FS-013) |
| F17 | `BotV2Controller::getListBotFree` | app/Http/Controllers/Admin/BotV2Controller.php | Direct | LOA Info / Bot Management (FS-002) |
| F18 | `SupperAdminController::affiliateTransfer` | app/Http/Controllers/Admin/SupperAdminController.php | Direct | Affiliate Reward Program (FA-027) |
| F19 | `UserController::ajaxCommentReasonCancelContract` | app/Http/Controllers/Admin/UserController.php | Direct | Cancellation List (FS-012) — 解約理由 |

### 4.2. List data bị update khi fix bug

**Không có** — Dev xác nhận chỉ đổi thứ tự đọc (`SELECT ... ORDER BY`), không ghi/sửa dữ liệu, không migration, không cache. `countScenario` vẫn ghi `scenario.count_follow/count_stop/count_unfinish` với giá trị **giống hành vi 5.7 cũ** (Dev không sửa lại nghĩa đếm, dù biết hàm vốn đã sai nghĩa — xem ghi chú ở file 01).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Tag Management (FA-012) — danh sách thành viên tag, tìm tag mặc định theo từ khoá | F1, F13 | Medium — bảng `tag_line_user` ~168M dòng |
| T2 | Broadcast (FA-008) — danh sách người nhận khớp bộ lọc (modal cũ) | F2 | Medium |
| T3 | Friend List (FA-013) — lọc nâng cao có phân trang, xuất CSV | F3 | Medium — bảng `bot_line_user` ~50M dòng, có phân trang 200/trang |
| T4 | CSV Management (FA-014) — xuất CSV theo bộ lọc / bạn bè bị chặn (API + job) | F5, F6, F7 | Medium — job nền + API, dùng chung `getConversationBlocked` |
| T5 | Friend Information (FA-015) — xuất CSV và danh sách giá trị thông tin bạn bè | F12 | Medium |
| T6 | Cross Analysis (FA-024) — danh sách giá trị để chọn | F4 | Medium — bảng `friend_information_value` ~51M dòng |
| T7 | QR Code Action / Landing Page (FA-017) — danh sách URL poster, bạn bè đã quét, click theo ngày | F8 | Medium — bảng `collect_open_landings` ~33M dòng, 3 nhánh độc lập |
| T8 | Lesson / Calendar Booking (FA-019) — danh sách khoá học nhận đặt theo ngày (API mobile) | F11 | Low–Medium |
| T9 | Event Booking (FA-021) — danh sách ngày slot sự kiện | F10 | Low–Medium |
| T10 | Booking manager (ngoài glossary) — lọc khối thời gian nhân viên | F9 | Low — bảng < 5M dòng |
| T11 | URL Analytics (FA-023) — số click URL trong tin nhắn ở Talk list / Error list | F14 | Low–Medium — hàm dùng chung 2 caller |
| T12 | Step Delivery / Scenario (FA-009) — đếm người theo trạng thái kịch bản | F15 | Medium — nhiều caller, ảnh hưởng số liệu ghi vào `scenario` table, kể cả luồng huỷ hợp đồng (StepMessageSpec) |
| T13 | Affiliate Payment Mgmt (FS-013) / Affiliate Reward Program (FA-027) — danh sách điều kiện, chuyển khoản affiliate | F16, F18 | Low–Medium |
| T14 | Cancellation List (FS-012) — lý do huỷ hợp đồng theo tháng | F19 | Low–Medium |
| T15 | LOA Info / Bot Management (FS-002) — danh sách bot free | F17 | Low–Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
