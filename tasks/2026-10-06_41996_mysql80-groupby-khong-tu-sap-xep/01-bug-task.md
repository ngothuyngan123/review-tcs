# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41996 — [WEB-R1] Nâng MySQL 5.7 → 8.0: GROUP BY không còn tự sắp xếp kết quả` |
| Module / Màn hình | Đa màn hình (31 vị trí `groupBy` không `orderBy` ở 19 file): Tag Management (FA-012) · Broadcast (FA-008) · Friend List (FA-013) · CSV Management (FA-014) · Friend Information (FA-015) · Cross Analysis (FA-024) · QR Code Action / Landing Page (FA-017) · Lesson/Calendar Booking (FA-019) · Event Booking (FA-021) · Booking manager (ngoài glossary) · URL Analytics (FA-023) · Step Delivery/Scenario (FA-009) · Affiliate Payment Mgmt (FS-013) / Affiliate Reward Program (FA-027) · Cancellation List (FS-012) · LOA Info/Bot Management (FS-002) |

## Mô tả bug (bản dịch tiếng Việt)

> Đây là **luận điểm phát hiện qua đối chiếu kỹ thuật** (review migration MySQL 5.7 → 8.0), không phải bug do khách hàng report qua thao tác thực tế — xem ghi chú ở mục "Steps to reproduce" bên dưới.

*Luận điểm R1 — GROUP BY không còn tự sắp xếp kết quả* · Project: sns-line (web Laravel)
Nguồn: báo cáo đối chiếu MySQL 8 — https://dashboard.melonglobal.net/fixbug-lme/mysql80-report/#result/R1 · ticket gốc #39528
Code đối chiếu: release_step_20260930_v2 @441407307e · Máy B: MySQL 8.0.46-0ubuntu0.22.04.4

### 1. Mô tả luận điểm

*Thay đổi 5.7 → 8.0:* 5.7: GROUP BY x ngầm định ORDER BY x (trừ khi ghi ORDER BY NULL). 8.0: bỏ hẳn — không có ORDER BY thì thứ tự là thứ tự plan trả về (temp table, hash, index…) và có thể khác giữa các lần chạy.

*Điều kiện kích hoạt:* Câu có GROUP BY mà không có ORDER BY, và code/UI dùng thứ tự dòng (hiển thị danh sách, phân trang, so vị trí phần tử, LinkedHashMap…).

*Tác động:* Sai kết quả hiển thị (danh sách, biểu đồ theo ngày lộn xộn), phân trang lặp/sót, và nặng nhất: logic nghiệp vụ dựa vào vị trí phần tử.

*Bằng chứng:* Thay đổi tài liệu hoá của 8.0, không cần runtime để kích hoạt — mọi câu khớp điều kiện đều bị ảnh hưởng ngay khi đọc từ B.

### 2. Các item ảnh hưởng (7 + 22 vị trí bổ sung)

| # | Ưu tiên | Logic / tính năng | Vị trí | Bảng dữ liệu (B) |
|---|---|---|---|---|
| 1 | Trung bình | Thành viên của tag (tagmember) | app/Http/Controllers/Basic/TagController.php:939 | tag_line_user 168.068.675 dòng (27,4 GiB); line_user 62.044.908 dòng (19,0 GiB) |
| 2 | Trung bình | Màn lọc người nhận broadcast — danh sách người khớp | app/Http/Controllers/Basic/FilterController.php:463 | line_user 62.044.908 dòng (19,0 GiB); bot_line_user 49.987.580 dòng (17,8 GiB) |
| 3 | Trung bình | Danh sách bạn bè — lọc nâng cao (GET /basic/friendlist/advance-filter) | app/Http/Controllers/Basic/FriendlistController.php:3470 | bot_line_user 49.987.580 dòng (17,8 GiB); line_user 62.044.908 dòng (19,0 GiB) |
| 4 | Trung bình | Phân tích chéo — danh sách giá trị thông tin bạn bè để chọn | app/Http/Controllers/Basic/CrossAnalysisController.php:2479 | friend_information_value 50.989.021 dòng (6,8 GiB) |
| 5 | Trung bình | Export CSV bạn bè theo bộ lọc | app/Http/Controllers/Api/ListFriendController.php:272 | bot_line_user 49.987.580 dòng (17,8 GiB) |
| 6 | Trung bình | QR / landing — tab danh sách URL poster, bạn bè đã quét, click theo ngày | app/Http/Controllers/Basic/QRCodeController.php:2304 | collect_open_landings 33.302.231 dòng (10,1 GiB) |
| 7 | Thấp | Lịch đặt chỗ (booking manager) — khối thời gian nhân viên | app/Http/Controllers/Basic/BookingManagerController.php:4480 | b_c_setting_time_block_staff 4.089.973 dòng (1,9 GiB) |

*1. Thành viên của tag (tagmember)*
- Vị trí: app/Http/Controllers/Basic/TagController.php:939
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Sai hiển thị / thứ tự / xuất file — không gửi tin cho khách
- Rủi ro: `groupBy(line_user.id)->get()` không `orderBy`.

```
app/Http/Controllers/Basic/TagController.php @ 441407307e  (dòng 935-940, * = dòng rủi ro)
  935                          ->where('tags.category_id', $id_category->category_id)
  936                          ->where('tags.bot_id', getBotId())
  937                          ->orderBy('id', 'desc');
  938                  }])
  939*                 ->groupBy('line_user.id')
  940                  ->get();
```

*2. Màn lọc người nhận broadcast — danh sách người khớp*
- Vị trí: app/Http/Controllers/Basic/FilterController.php:463
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Sai hiển thị / thứ tự / xuất file — không gửi tin cho khách
- Rủi ro: `SELECT line_user.* … GROUP BY line_user.id`, không `ORDER BY`, trả thẳng cho UI.

```
app/Http/Controllers/Basic/FilterController.php @ 441407307e  (dòng 461-464, * = dòng rủi ro)
  461          }
  462  
  463*         $queryBuilder->select('line_user.*')
  464              ->groupBy('line_user.id');
```

*3. Danh sách bạn bè — lọc nâng cao (GET /basic/friendlist/advance-filter)*
- Vị trí: app/Http/Controllers/Basic/FriendlistController.php:3470
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Sai hiển thị / thứ tự / xuất file — không gửi tin cho khách
- Rủi ro: `groupBy` không `orderBy` trên kết quả bộ lọc.

```
app/Http/Controllers/Basic/FriendlistController.php @ 441407307e  (dòng 3466-3472, * = dòng rủi ro)
 3466                  'bot_line_user.is_blocked',
 3467                  // DB::raw('(select followed_at from bot_line_user where bot_line_user.bot_id = conversation.bot_id and bot_line_user.line_user_id = conversation.line_id order by updated_at desc limit 1) as followed_at'),
 3468                  DB::raw("(concat('/basic/friendlist/my_page/',line_user.id)) as link_my_page")
 3469              )
 3470*                 ->groupBy('bot_line_user.id')
 3471                  ->paginate(200);
 3472              foreach ($data as $item) {
```

*4. Phân tích chéo — danh sách giá trị thông tin bạn bè để chọn*
- Vị trí: app/Http/Controllers/Basic/CrossAnalysisController.php:2479
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Sai hiển thị / thứ tự / xuất file — không gửi tin cho khách
- Rủi ro: `GROUP BY value` không `ORDER BY`, trả thẳng cho người dùng chọn/sắp xếp.

```
app/Http/Controllers/Basic/CrossAnalysisController.php @ 441407307e  (dòng 2476-2481, * = dòng rủi ro)
 2476                          ->where('friend_information_setting_id', $id);
 2477              }
 2478  
 2479*             $r = $r->groupBy(['value'])->get();
 2480  
 2481              return response()->json([
```

*5. Export CSV bạn bè theo bộ lọc*
- Vị trí: app/Http/Controllers/Api/ListFriendController.php:272
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Sai hiển thị / thứ tự / xuất file — không gửi tin cho khách
- Rủi ro: `advanceFilterPost()->groupBy(bot_line_user.id)->get()` không `orderBy` ⇒ thứ tự dòng CSV khác.

```
app/Http/Controllers/Api/ListFriendController.php @ 441407307e  (dòng 270-273, * = dòng rủi ro)
  270                  $sqlFiller = Conversation::advanceFilterPost($bot_id, $itemSearch, $itemSearchOr);
  271                  $list = $sqlFiller->select($select)
  272*                     ->groupBy('bot_line_user.id')
  273                      ->get();
```

*6. QR / landing — tab danh sách URL poster, bạn bè đã quét, click theo ngày*
- Vị trí: app/Http/Controllers/Basic/QRCodeController.php:2304
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Sai hiển thị / thứ tự / xuất file — không gửi tin cho khách
- Rủi ro: `groupBy(...)->paginate()` và `orderBy` CHỈ khi request có tham số order ⇒ không có thì phân trang không xác định: trang sau lặp/sót dòng.

```
app/Http/Controllers/Basic/QRCodeController.php @ 441407307e  (dòng 2300-2306, * = dòng rủi ro)
 2300                              return $q->where('landing_page_connect_qrcode.landing_name', 'like', '%' . $keyword . '%')
 2301                                  ->orWhere('poster_connect_qrcode.poster_name', 'like', '%' . $keyword . '%');
 2302                          });
 2303                  })
 2304*                 ->groupBy('date_scan', 'collect_open_landings.post_code');
 2305  
 2306              $totals = clone $posterUrls;
```

*7. Lịch đặt chỗ (booking manager) — khối thời gian nhân viên*
- Vị trí: app/Http/Controllers/Basic/BookingManagerController.php:4480
- Kết luận: Rủi ro (code khớp điều kiện) · Ưu tiên Thấp — Bảng < 5 triệu dòng, ít dữ liệu bị ảnh hưởng
- Rủi ro: `groupBy` 3 cột không `orderBy`, render lên lịch theo thứ tự trả về.

```
app/Http/Controllers/Basic/BookingManagerController.php @ 441407307e  (dòng 4476-4481, * = dòng rủi ro)
 4476  
 4477          return BCSettingTimeBlockStaff::where($condition)
 4478          ->where('date', '>=', $start_date)
 4479          ->where('date', '<=', $end_date)
 4480*         ->groupBy('event_id_google_calendar')
 4481          ->groupBy('staff_id')
```

*Vị trí bổ sung (báo cáo audit web gốc, mục 3.1.1 mức Normal — chưa rà từng chỗ):*

| # | Vị trí (release) | Mô tả trong báo cáo |
|---|---|---|
| 1 | app/Category.php:1036 | `Category::getCategoryTagDefaultByKeyWord` chạy `SELECT count(tag_line_user.id) as count, tags.id, tags.* FROM tags LEFT JOIN tag_line_user ON tags.id=tag_line_user.tag_id AND tag_line_user.is_deleted=0 WHERE category_id=0 AND bot_id=? AND tags.name LIKE ? GROUP ...` |
| 2 | app/Console/Commands/HandleExportCsv.php:229 | Job export CSV lấy danh sách bạn bè bằng `$sqlFiller->select($select)->groupBy('bot_line_user.id')->get()` KHÔNG có ORDER BY (`advanceFilterPost` không có orderBy, xem `Conversation.php:247-1725`) |
| 3 | app/Console/Commands/HandleExportCsv2.php:207 | Export CSV: `Conversation::advanceFilterPost(...)->select($select)->whereIn('line_user.id',$lineUserChild)->groupBy('conversation.id')->get()` không có orderBy trong đoạn này; kết quả được dùng theo thứ tự để ghi từng dòng CSV (convertData/writecsv) |
| 4 | app/Helpers/functions.php:11488 | `countScenario()` chạy 3 câu `@ScenarioLineuser::where('scenario_id',..)->where('is_following',N)->groupBy('line_user_id')->count('id')@` (dòng 11406-11408) |
| 5 | app/Http/Controllers/Admin/AspManagement/AffiliateManagementController.php:2182 | `getListCondition()` chạy `Bots LEFT JOIN bot_setting_aff LEFT JOIN aff_result ..` |
| 6 | app/Http/Controllers/Admin/AspManagement/AffiliateManagementController.php:2258 | `getConditionOfAllBot()` (dropdown điều kiện của mọi bot) dùng `GROUP BY bots.id, bot_setting_aff.id` không ORDER BY, kết quả trả JSON theo thứ tự trả về |
| 7 | app/Http/Controllers/Admin/BotV2Controller.php:150 | `getListBotFree()` dựng query `Bots leftJoin bot_slots/bot_contracts/user_staff_bots` rồi `->groupBy('bots.id')->get([...])` mà KHÔNG có orderBy |
| 8 | app/Http/Controllers/Admin/SupperAdminController.php:240 | `affiliateTransfer()` join `AffiliateInfo` với derived table `(SELECT user_id, SUM(...) amount, COUNT(*) count_pm FROM payment_detail_aff ..` |
| 9 | app/Http/Controllers/Admin/UserController.php:9491 | `ajaxCommentReasonCancelContract` (route POST /admin/ajax-comment-reason-cancel-contract, màn 解約理由) chạy `BotContracts::select(bot_contracts.*, users..., contract_cancel_reason...) ..` |
| 10 | app/Http/Controllers/Affiliate/AffiliaterController.php:935 | `ajaxAffMoneyV2`: select `bot_setting_aff.*, bots.view_name, aff_result.created_at, aff_result.is_approved, aff_result.aff_id, aff_result.line_user_id FROM aff_result JOIN bot_setting_aff JOIN bots ..` |
| 11 | app/Http/Controllers/Api/CalendarLessonController.php:1460 | `getListReceptionCourse()` chạy SELECT .. |
| 12 | app/Http/Controllers/Api/ListFriendController.php:291 | Nhánh `enableBotBlockFriend/enableFriendBlockBot` của export CSV gọi `Conversation::getConversationBlocked(...)` có `->groupBy('conversation.id')->get()` không ORDER BY (`app/Conversation.php:1828-1858`) |
| 13 | app/Http/Controllers/Basic/BookingEventDayController.php:2129 | `ajaxAllBooking` dựng `BSlot::select('id','date_start_from')->where(event_detail_id,bot_id)->groupBy('date_start_from')->get()` (dòng 2009-2027) |
| 14 | app/Http/Controllers/Basic/BookingManagerController.php:636 | `ajaxFilterBookingByCondition`: `BCSettingTimeBlockStaff::where(A)->orWhere(B)->groupBy(6 cột)->get()` không có ORDER BY, kết quả array_merge với danh sách booking rồi trả cho FE lọc lịch |
| 15 | app/Http/Controllers/Basic/ConversionController.php:1069 | `visitedConversion()` chạy `SELECT DISTINCT(cr.line_user_id), cr.visited_at, c.name, l.* ..` |
| 16 | app/Http/Controllers/Basic/CrossAnalysisController.php:1026 | `getDataFriendInfo()` chạy `SELECT line_user.<cột> as value ..` |
| 17 | app/Http/Controllers/Basic/FriendInformationController.php:313 | `exportCsv` (nhánh default, dòng 307-312) dùng cùng mẫu: `FriendInformationValue leftJoin line_user`, select id/value/name/.. |
| 18 | app/Http/Controllers/Basic/FriendInformationController.php:408 | `initDataItemInfo` (nhánh default, dòng 403-408) chạy `FriendInformationValue leftJoin line_user` với select `friend_information_value.id, value, line_user.name, email` nhưng chỉ `GROUP BY friend_information_value.line_id`, không có ORDER BY, rồi `->get()` trả thẳng ra |
| 19 | app/Http/Controllers/Basic/FriendlistController.php:666 | `csvExport()` nhánh chọn tay (line_user) ở dòng 641-667 và 695-721 chạy SELECT .. |
| 20 | app/Http/Controllers/Basic/QRCodeController.php:2545 | `collectFriend` với `type_count=1` dùng `->groupBy('line_id')->select(MAX(id) as id, line_id, MAX(time_click))` rồi `->paginate($params['per_page'] ?? 10)` |
| 21 | app/Http/Controllers/Basic/QRCodeController.php:2665 | `detailClickDay` với `type_count=1` dùng `->groupBy('collect_open_landings.device')` + select MAX(...) rồi `->paginate($params['per_page'] ?? 10)`; orderBy chỉ khi có params order + dir (dòng 2606-2608) |
| 22 | app/Url.php:27 | `Url::getListUrlInMessage` chạy `SELECT url.*, sum(click_number) FROM url LEFT JOIN url_shorten_detail ud ..` |

### 3. Hướng xử lý

Thêm ORDER BY tường minh (theo đúng cột 5.7 đang ngầm sắp xếp) cho từng câu.

## Steps to reproduce

<!-- Không có — xem ghi chú dưới. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Không có attachment trên Redmine #41996. -->

## Ghi chú thêm của Leader

⚠️ **Đây KHÔNG phải bug Redmine không tái hiện được** — ticket thuộc loại **proactive audit** (soát luận điểm khi nâng MySQL 5.7 → 8.0), không có "Tái hiện bug" vì Dev tự phát hiện qua đối chiếu kỹ thuật (dashboard `fixbug-lme/mysql80-report`), không cần runtime để kích hoạt. Dev đã tự confirm + tự fix (xem file 03). TCs nên tập trung verify: (a) cách fix (thêm `ORDER BY` tường minh đúng cột 5.7 ngầm sắp xếp) có áp dụng đúng ở từng vị trí, (b) regression — kết quả danh sách/phân trang/CSV/count không lặp/sót/sai thứ tự so với trước, (c) `orderBy` đặt cuối chuỗi (sau sort người dùng chọn) không đè sort đã chọn.

Môi trường phát hiện: đối chiếu trên máy B MySQL 8.0.46 (dev); bug chỉ lộ trên MySQL 8, KHÔNG tái hiện được trên MySQL 5.7/5.6. Dev **không chạy được runtime** (dev DB `host.docker.internal:3306` connection refused) — chỉ verify ở mức lint (`php -l`) + tra thủ công cấu trúc bảng (cột `value` không tồn tại trên `line_user`/`bot_line_user` → `ORDER BY value` phân giải đúng alias như `GROUP BY value`), **chưa chạy thử thực tế**.

Phạm vi fix: 31 vị trí `groupBy` ở 19 file (7 vị trí báo cáo gốc + 22 vị trí bổ sung từ audit mức Normal). Dev **bỏ qua 4 vị trí** báo cáo nhận nhầm vì đã có ORDER BY sẵn (`BookingManagerController:4480`, `AffiliaterController::ajaxAffMoneyV2`, `ConversionController::visitedConversion`) hoặc code chết (`HandleExportCsv2`) — xem chi tiết mục 2 Journal ở file 03.

⚠️ `countScenario()` (app/Helpers/functions.php) vốn đã sai nghĩa từ trước (dùng `count()` kèm `groupBy` chỉ trả số dòng của **nhóm đầu tiên**, không phải tổng số người) — Dev **giữ nguyên hành vi 5.7** khi fix (không sửa ngoài scope ticket), chỉ thêm `orderBy` để nhóm đầu tiên vẫn đúng như 5.7 từng ngầm chọn. Cần TC verify đúng "giống hành vi cũ" (không phải "đúng nghĩa đếm người"), vì nhánh này dùng để ghi `scenario.count_follow/count_stop/count_unfinish`.

Ticket gốc tham chiếu: #39528 (báo cáo đối chiếu MySQL 8 R1). Ticket song song cùng đợt audit: #41998 (R2 — ORDER BY cột không duy nhất).

## Journal / note từ Redmine (nguyên văn)

**Journal #140123 — AI LME Fix bug — 2026-10-05:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
MySQL 5.7 tự sắp xếp kết quả theo cột GROUP BY khi câu không có ORDER BY; MySQL 8.0 bỏ hẳn hành vi này nên các danh sách, phân trang, file CSV và câu count() kèm groupBy (lấy dòng đầu) đang dựa vào thứ tự đó sẽ trả về lộn xộn, có thể khác nhau giữa các lần chạy và gây lặp/sót dòng khi phân trang.

■ 2. CÁCH FIX
Thêm ORDER BY tường minh theo đúng cột GROUP BY (chính thứ tự MySQL 5.7 đang ngầm áp dụng) cho 31 chỗ gọi groupBy ở 19 file trong ticket: danh sách thành viên tag, lọc người nhận, lọc nâng cao + xuất CSV bạn bè (màn, API, job, getConversationBlocked), giá trị thông tin bạn bè (phân tích chéo, quản lý thông tin bạn bè), 3 danh sách QR/landing, khối thời gian nhân viên, ngày slot sự kiện, khoá học lịch bài học, affiliate/bot free/hủy hợp đồng phía admin, getListUrlInMessage, countScenario. orderBy được đặt CUỐI chuỗi (sau sắp xếp do người dùng chọn) nên chỉ làm khoá phụ khi đã có sort. Bỏ qua 4 vị trí báo cáo nhận nhầm vì đã có ORDER BY (BookingManager:4480, Affiliater:935, Conversion:1069) hoặc code chết (HandleExportCsv2). Quét ngang: các bản Replicate chết + vị trí phía job/MCP ghi vào yokoten.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
TagController::member (app/Http/Controllers/Basic/TagController.php)
FilterController::ajaxGetListUserFilter (app/Http/Controllers/Basic/FilterController.php)
FriendlistController::filterAdvance + csvExport 4 nhánh (app/Http/Controllers/Basic/FriendlistController.php)
CrossAnalysisController::getDataFriendInfo + danh sách giá trị (app/Http/Controllers/Basic/CrossAnalysisController.php)
Api\ListFriendController export CSV (app/Http/Controllers/Api/ListFriendController.php)
Conversation::getConversationBlocked (app/Conversation.php) — caller: CsvManagementController, HandleExportCsv, HandleUpdateLatestInformationCsv, ListFriendController
HandleExportCsv::handle nhánh lọc (app/Console/Commands/HandleExportCsv.php)
QRCodeController::poster url list / collectFriend / detailClickDay (app/Http/Controllers/Basic/QRCodeController.php)
BookingManagerController::ajaxFilterBookingByCondition (CÓ sửa: thêm orderBy theo 6 cột groupBy) (app/Http/Controllers/Basic/BookingManagerController.php)
BookingManagerController::getListTimeBlockByCondition (đã có orderBy, không sửa)
BookingEventDayController::ajaxAllBooking (app/Http/Controllers/Basic/BookingEventDayController.php)
Api\CalendarLessonController::getListReceptionCourse
FriendInformationController::exportCsv + initDataItemInfo
Category::getCategoryTagDefaultByKeyWord (app/Category.php)
Url::getListUrlInMessage (app/Url.php) — caller TalkListController, ErrorListController
countScenario (app/Helpers/functions.php) — Laravel aggregate() kèm groupBy trả dòng đầu — caller: CreateOrUpdateScenarioStepMessage, RecoverUpdateStatusScenarioLineuser, functions.php:12320, ScenarioMobileController, ScenarioController, StepMessageController (2227, 3456), StepMessageSpec (luồng huỷ hợp đồng)
AffiliateManagementController::getListCondition + getConditionOfAllBot
BotV2Controller::getListBotFree
SupperAdminController::affiliateTransfer
UserController::ajaxCommentReasonCancelContract (2 câu usersPayment/usersPaymentCmt)
AffiliaterController::ajaxAffMoneyV2, ConversionController::visitedConversion (đã có orderBy, không sửa)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Category.php
   - app/Console/Commands/HandleExportCsv.php
   - app/Conversation.php
   - app/Helpers/functions.php
   - app/Http/Controllers/Admin/AspManagement/AffiliateManagementController.php
   - app/Http/Controllers/Admin/BotV2Controller.php
   - app/Http/Controllers/Admin/SupperAdminController.php
   - app/Http/Controllers/Admin/UserController.php
   - app/Http/Controllers/Api/CalendarLessonController.php
   - app/Http/Controllers/Api/ListFriendController.php
   - app/Http/Controllers/Basic/BookingEventDayController.php
   - app/Http/Controllers/Basic/BookingManagerController.php
   - app/Http/Controllers/Basic/CrossAnalysisController.php
   - app/Http/Controllers/Basic/FilterController.php
   - app/Http/Controllers/Basic/FriendInformationController.php
   - app/Http/Controllers/Basic/FriendlistController.php
   - app/Http/Controllers/Basic/QRCodeController.php
   - app/Http/Controllers/Basic/TagController.php
   - app/Url.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ đổi thứ tự đọc (SELECT), không ghi/sửa dữ liệu. countScenario vẫn ghi scenario.count_follow/count_stop/count_unfinish với giá trị giống 5.7
 • 4.3 Tính năng liên quan:
   - Tag Management (FA-012) — danh sách thành viên tag, tìm tag mặc định theo từ khoá
   - Broadcast (FA-008) — danh sách người nhận khớp bộ lọc
   - Friend List (FA-013) — lọc nâng cao có phân trang, xuất CSV
   - CSV Management (FA-014) — xuất CSV theo bộ lọc / bạn bè bị chặn (API + job)
   - Friend Information (FA-015) — xuất CSV và danh sách giá trị thông tin bạn bè
   - Cross Analysis (FA-024) — danh sách giá trị để chọn
   - QR Code Action / Landing Page (FA-017) — danh sách URL poster, bạn bè đã quét, click theo ngày
   - Lesson / Calendar Booking (FA-019) — danh sách khoá học nhận đặt theo ngày
   - Event Booking (FA-021) — danh sách ngày slot sự kiện
   - Booking manager (outside glossary) — lọc khối thời gian nhân viên (controller cũ)
   - URL Analytics (FA-023) — số click URL trong tin nhắn ở Talk list / Error list
   - Step Delivery / Scenario (FA-009) — đếm người theo trạng thái kịch bản
   - Affiliate Payment Mgmt (FS-013) / Affiliate Reward Program (FA-027) — danh sách điều kiện, chuyển khoản affiliate
   - Cancellation List (FS-012) — lý do huỷ hợp đồng
   - LOA Info / Bot Management (FS-002) — danh sách bot free

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l 19 file đã sửa: No syntax errors; git diff --stat release_step_20260930_v2(4cd40c1cee)...ai_small_41996: 19 files, +82/-10; Tra share/db: line_user/bot_line_user không có cột `value` → ORDER BY value phân giải đúng alias như GROUP BY value; các orderBy không qualify (line_id, date_start_from, line_user_id, event_id_google_calendar…) chỉ nằm trong câu 1 bảng; MySQL dev host.docker.internal:3306 Connection refused → chưa chạy thử runtime
   Bằng chứng: Laravel 5.5 Builder::aggregate() giữ nguyên orders và trả results[0] ⇒ count() kèm groupBy lấy nhóm đầu; thêm orderBy giữ đúng nhóm đầu như 5.7; Danh sách 22 vị trí bổ sung lấy từ fixbug-lme/perf-report/redmine_tasks.py (mô tả Redmine bị cắt 4000 ký tự)

■ TỰ REVIEW (AI)
Diff chỉ thêm orderBy theo đúng cột groupBy ở các vị trí ticket liệt kê (7 + 22), đặt cuối chuỗi sau mọi sort có điều kiện nên không đè sort người dùng chọn. 4 vị trí bỏ qua có lý do (đã có ORDER BY / code chết).
 • Rủi ro / lưu ý khi test:
   - ORDER BY trên MySQL 8.0 có thể thêm filesort cho câu GROUP BY dùng hash/temp table — chi phí tương đương 5.7 vốn đã sort ngầm
   - countScenario vốn đã sai nghĩa (count() + groupBy trả số dòng của nhóm đầu, không phải số người) — giữ nguyên hành vi 5.7, không sửa ngoài scope

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41996 (nhánh gốc release_step_20260930_v2, commit de5e4b3d53, 19 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 6 phút 30 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=1cceced0-d59a-4466-ae80-a2ec2952e1c8
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41996
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
