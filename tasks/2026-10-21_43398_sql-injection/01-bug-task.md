# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43398 — SQL Injection` |
| Module / Màn hình | Không phải 1 module đơn — **audit bảo mật rải khắp hệ thống**, trọng tâm là **bộ lọc bạn bè nâng cao** (`Conversation::advanceFilterPost` / `advanceFilter`, ~67 nơi gọi dùng chung bởi: 友だちリスト, gửi hành động, broadcast đếm số, export CSV, cross analysis, talk list, API mobile filter, API export public, remind, booking). Ngoài ra còn ~20 điểm phụ: My page form answer, chat nhóm, mobile list friend/chat, Broadcast V2/Schedule send chat/Step message/Park template (template_ids), sort 11 màn (QR, Tag, Template, Rich menu, admin affiliate/coupon/path intro...), Action schedule, Admin affiliate payment/CSV, Salon booking theo ngày, Mobile event booking keep-slot. |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Ticket này KHÔNG phải 1 bug đơn lẻ do khách hàng báo — là kết quả security audit nội bộ, Dev tự tạo ticket để fix. Nội dung dưới đây paste nguyên văn description Redmine (đã là tiếng Việt). -->

Nguồn: security audit SQL Injection (đã bỏ SQLI-01, SQLI-08)
Ghi chú: "(Likely)" = audit đánh giá khả năng cao, cần xác nhận khi fix.

1. SQLI-02 [Immediate] — Bộ lọc nâng cao advanceFilterPost nội suy điều kiện lọc vào whereRaw/DB::raw

* Vị trí: app/Conversation.php và app/ConversationReplicate.php — advanceFilterPost()
* Vị trí :429-430 — tags_search
* Vị trí :465-469 — scenario_id = {$scenario_search}, INTERVAL {$item->number_date} DAY → DB::select(DB::raw(...))
* Vị trí :486, 490, 494, 499
* Vị trí :510, 515, 519 — conversion
* Vị trí :737, 791, 796, 804, 933-956 — {$idInfo}, {$point}
* Vị trí :779-780 — value IN ("…implode selected_op…"), thoát được chuỗi
* Vị trí nhánh OR :1166-1218, 1438, 1482, 1497-1504, 1631-1653
* Route: POST /basic/friendlist/post-advance-filter-v2 (LOGIN, web.php:2026), POST /basic/friendlist/export (2227), POST /ajax/filter/save-filter-v2 (4132), countAllFriend, CrossAnalysisController@ajaxInitCross (3074), TalkListController@ajaxGetTalkListData (3113), BroadcastController@getFilterNumber (3363), Api\ListFriendController@getDataExportCsv (api.php:418, PUBLIC), Api\Mobile\FilterMobileController · tham số item_search / item_search_or (JSON)
* Vấn đề: Nhiều trường con của điều kiện lọc nội suy thẳng vào whereRaw/DB::raw. Second-order: filter lưu ở filter_v2.data được FilterV2::initDataFilter chạy lại trong HelperService::sendAction, RemindApiController@startRemind, job export.
* Fix: intval/normalizeIdList mọi id, bind ?, validate *_condition/op_compare bằng in:; validate cấu trúc item_search ở controller. Rà toàn bộ >40 whereRaw có biến trong Conversation.php.

2. SQLI-05 [Immediate] — getDataFormAnswerMyPage nội suy user_id vào DB::raw (route PUBLIC)

* Vị trí: ChatController.php:7345-7348 getDataFormAnswerMyPage
* Route: GET /ajax/get_data_form_answer_my_page (PUBLIC, web.php:4069) · tham số user_id
* Vấn đề: DB::raw("(SELECT data … where form_old.line_id = $line_user_id …") — không nháy, không cast.
* Fix: (int) + binding; đưa route vào nhóm có auth + kiểm friend thuộc bot.

3. SQLI-03 [Urgent] — advanceFilter() không cast id / number_date

* Vị trí: app/Conversation.php:157-186 advanceFilter() (+ bản Replicate)
* Vị trí: app/Conversation.php:214-228 advanceFilter() (+ bản Replicate)
* Vị trí nguồn: FriendlistController.php:3440-3446 — id / number_date không cast
* Route: GET /basic/friendlist/advance-filter (LOGIN, web.php:2025); csvExport nhánh old (FriendlistController:618), sendActionFriend (:1045) · tham số scenario_search[][id], number_date
* Vấn đề: Id / number_date không cast, nội suy thẳng vào query.
* Fix: Như SQLI-02 — intval/normalizeIdList mọi id, bind ?.

4. SQLI-04 [Urgent] — postFilterAdvance / sendActionFriend nội suy scenario_stop_id vào whereRaw

* Vị trí: Basic\FriendlistController.php:3572-3578 postFilterAdvance
* Vị trí: Basic\FriendlistController.php:959, 1182-1184 sendActionFriend
* Vị trí lưu dữ liệu: Basic\FriendlistController.php:1250-1268 — giá trị lưu vào FilterV2.data.scenario_search
* Route: POST /basic/friendlist/post-advance-filter-v2 (2026), POST /basic/friendlist/send-action (2193) — LOGIN · tham số scenario_stop_id, scenario_unfinish_id
* Vấn đề: whereRaw("… scenario_id = {$request->scenario_stop_id} …"); giá trị còn được lưu vào FilterV2.data.scenario_search → second-order SQLI-02.
* Fix: Validate integer / bind.

5. SQLI-06 [Urgent] — getGroupChat nội suy keyword vào LIKE

* Vị trí: ChatController.php:5127 getGroupChat (gọi từ @group :5054)
* Route: GET /basic/chat/group (BASIC, ajax) · tham số key
* Vấn đề: whereRaw("… msg.content like '%{$keyword}%') > ?", [0])
* Fix: Bind like ?.

6. SQLI-07 [Urgent] — myPageFormDetails nội suy line_id lấy từ route

* Vị trí: Basic\FormAnswerController.php:5060 myPageFormDetails
* Vị trí: Basic\FormAnswerController.php:5077 myPageFormDetails
* Route: GET /basic/my-page/form-answer/{id}/{form_id?} (LOGIN, web.php:2277) · tham số route {id}
* Vấn đề: DB::raw("(select count(...) where form_answer_result.line_id = {$line_id}) as count"); route không có regex.
* Fix: ->where('id','[0-9]+') + binding; dùng abortIfFriendNotOwned().

7. SQLI-09 [Urgent] — getScenarioToChange nội suy line_user_id vào CASE WHEN

* Vị trí: app/Scenario.php:78 getScenarioToChange
* Vị trí: app/ScenarioReplicate.php:79 getScenarioToChange
* Vị trí nguồn: FriendlistController.php:3025 — line_user_id
* Route: POST /basic/friendlist/my_page/save-scenario (LOGIN, web.php:2173) · tham số line_user_id
* Vấn đề: DB::raw("CASE WHEN … line_user_id = $line_id …")
* Fix: (int) + kiểm friend thuộc bot.

8. SQLI-10 [Urgent] — Broadcast V2 lưu template_ids chưa lọc → FIELD(id, …) (2nd-order)

* Vị trí: Basic\BroadcastV2Controller.php:231, 300-303 saveBroadcastV2
* Vị trí sink 2nd-order: Basic\BroadcastV2Controller.php:653 getDetailBroadcastV2
* Vị trí sink 2nd-order: Basic\BroadcastV2Controller.php:689 getListMessage
* Vị trí nguồn ghi thêm: Basic\BroadcastV2Controller.php:1068-1071
* Vị trí nguồn ghi (Likely): BroadcastController.php:2635-2686
* Liên quan: functions.php:12823 normalizeIdList()
* Route: POST /ajax/save-broadcast-v2 (2726), /ajax/remove-item-message-broadcast-v2 (2720), /ajax/get-detail-broadcast-v2 (2728), GET /ajax/get-list-message-broadcast (2730) — LOGIN · tham số arr_template_ids[]
* Vấn đề: orderByRaw(DB::raw("FIELD(id, $strTemplateIds)")); chốt hasTemplateOfOtherBot() dùng normalizeIdList() bỏ qua phần tử không phải số nên payload lọt qua và được lưu nguyên vào broadcast.template_ids.
* Fix: Lưu implode(',', normalizeIdList(...)); cast int ở mọi sink; dọn dữ liệu template_ids không khớp ^[0-9,]*$.

9. SQLI-11 [Urgent] — Schedule send chat: FIELD(id, template_ids) (2nd-order)

* Vị trí sink: Basic\ScheduleSendChatController.php:126-134
* Vị trí nguồn: Basic\ScheduleSendChatController.php:172, 192-203
* Vị trí nguồn: Basic\ScheduleSendChatController.php:225, 243-249
* Vị trí nguồn: Basic\ScheduleSendChatController.php:342-362
* Route: POST /ajax/initDataScheduleSendChat (2742), /ajax/remove-item-message-schedule-send-chat (2743), /ajax/sort-template-schedule-send-chat (2744) — LOGIN · tham số arr_template_ids[], template_ids
* Vấn đề: FIELD(id, $scheduleSend->template_ids) (2nd-order).
* Fix: Như SQLI-10 — lưu implode(',', normalizeIdList(...)); cast int ở mọi sink; dọn dữ liệu template_ids không khớp ^[0-9,]*$.

10. SQLI-12 [Urgent] — Step message: FIELD(id, template_ids) (2nd-order)

* Vị trí sink: Basic\StepMessageController.php:3043-3047, 3292, 3345
* Vị trí nguồn: StepMessageController.php:2805-2821
* Vị trí nguồn: ScenarioController.php:2457-2471
* Route: POST /ajax/save-sort-message-step (2684), /ajax/scenario/sort-step-message-template (3347), /ajax/copy-message-and-action-step-message (2651), /ajax/copy-and-register-all-step (2649) — LOGIN · tham số templateIds / ids
* Vấn đề: FIELD(id, $step->template_ids) (2nd-order); job gửi kịch bản có thể cũng đọc cột này.
* Fix: Như SQLI-10 — lưu implode(',', normalizeIdList(...)); cast int ở mọi sink; dọn dữ liệu template_ids không khớp ^[0-9,]*$.

11. SQLI-13 [Urgent] — Mobile list friend / chat: implode tags và orderByRaw line_id

* Vị trí: Mobile\ListFriendController.php:124-128, 139-140
* Vị trí: Mobile\ChatMobileController.php:71-75, 82-83
* Route: GET /list-friend/{bot_id}, /v2/list-friend/{bot_id} (2457, 2484), GET /chat-mobile/{conversation_id} (2460, 2485) — MOBILE-WEB · tham số tags[], line_id, search_tab
* Vấn đề: implode(',', $tags) vào in ($arr); orderByRaw("… = $line_id desc"). tags còn đọc từ session mb_tag_search… (2nd-order).
* Fix: array_map('intval') + whereIn; orderByRaw('… = ? desc', [(int)$line_id]).

12. SQLI-14 [Urgent] — Admin resultDownloadCsv nội suy time vào selectRaw

* Vị trí: Admin\AffController.php:559 resultDownloadCsv
* Vị trí nguồn: Admin\AffController.php:694-697 getTime
* Route: GET /admin/download-csv-result (ADMIN, web.php:562) · tham số time
* Vấn đề: selectRaw("… >= $start AND … <= $end …"), $start = $request->time.'-01'.
* Fix: date_format:Y-m + bind.

13. SQLI-15 [High] — CategoryService::updatePosition nội suy id/pos vào CASE

* Vị trí: app/Services/V2/CategoryService.php:83-91 updatePosition
* Route: V2\RichMenuController@sortListFolderData (web.php:3084), @sortListRichMenu (3094), V2\Bill\ListPageController@saveContractPosition (3249) — LOGIN · tham số order[]
* Vấn đề: "WHEN {$id} THEN {$pos}" → UPDATE … SET col = CASE id …; order chỉ validate array.
* Fix: order.* integer / intval.

14. SQLI-16 [High] — Park template: FIELD(id, $ids) (2nd-order)

* Vị trí sink: app/Category.php:799-803 getTemplateDetailsOfCategoryInPark
* Vị trí sink: bản Replicate của Category :802
* Vị trí sink: Basic\StepMessageController.php:1558-1560
* Vị trí nguồn: Basic\MessageTemplateController.php:3808-3823 sortItem
* Vị trí nguồn: Basic\StepMessageController.php:3640-3658 saveSortTemplateChild
* Route: POST /ajax/init-park-template (LOGIN, web.php:3131), /ajax/save-sort-template-child, /ajax/get-list-step-message (LOGIN) · tham số sort_ids, template_ids[] (lưu vào template.content → 2nd-order)
* Vấn đề: orderByRaw(DB::raw("FIELD(id, $ids)"))
* Fix: intval trước khi implode; validate khi lưu.

15. SQLI-17 [High] (Likely) — TemplateRepository::handleTypeTemplate: FIELD(id, content)

* Vị trí: app/Repositories/Eloquents/TemplateRepository.php:511 handleTypeTemplate
* Route: luồng clone/transfer template · template.content (2nd-order)
* Vấn đề: FIELD(id, $item->content)
* Fix: intval từng phần tử.

16. SQLI-18 [High] (Likely) — Column-name injection qua orderBy($request…)

* Vị trí: Basic\BroadcastController.php:1306-1307, 1368-1374 — orderBy('broadcast.'.$order_by) · POST /ajax/get-list-broadcast
* Vị trí: Basic\QRCodeController.php:1369-1378, 2648, 2678-2680 · GET /ajax/v2/landing/qr-removed (2943), /ajax/v2/landing/{id}/detail-click-day (2979)
* Vị trí: Basic\TagController.php:1643-1653 · GET /ajax/v2/tag/get-tag-removed (2999)
* Vị trí: Basic\FormAnswerController.php:8020-8021 · GET /ajax/get-form-answer-removed (3713)
* Vị trí: app/Category.php:566, 724 (+ bản Replicate) · POST /ajax/init-template (3120) + Api\Mobile\TemplateMobileController
* Vị trí: V2\RichMenuController.php:72-74 · GET /ajax/rich-menu/list/{folderId} (3093)
* Vị trí: Admin\AffiliateInfoController.php:657, 781 · POST /admin/ajaxManagePaymentStatus (ADMIN, 618)
* Vị trí: Admin\SupperAdminController.php:174, 264, 339 · /ajax/supper-admin/* (LOGIN, 3721-3724)
* Tham số: order, field, sorter[][column], order[column] — LOGIN / ADMIN
* Vấn đề: Tên cột không whitelist. Các màn cùng loại đã whitelist (QRCodeController:951-960, 2187-2201, TagController:117, UserController:4680-4687, RichMenuController:935-936) — làm theo mẫu đó.
* Fix: Whitelist cột bằng in_array.

17. SQLI-24 [High] (Likely) — ActionSchedule update dùng $request->except → key body thành tên cột

* Vị trí: Basic\ActionScheduleController.php:715 — $data = $request->except([...])
* Vị trí: Basic\ActionScheduleController.php:1341 — ActionSchedule::where('id',$id)->where('bot_id',$botId)->update($data) qua query builder
* Route: POST /ajax/update-action-schedule/{id} (LOGIN), PUT /basic/action-schedules/{id} (BASIC) · tên key trong body
* Vấn đề: Key của body thành tên cột trong UPDATE … SET (key chứa -> đi qua JSON path không escape); đồng thời ghi được mọi cột.
* Fix: $request->only([...]) whitelist cột.

18. SQLI-19 [Normal] — Admin payment management: LIKE filter_month

* Vị trí: Admin\AffiliateInfoController.php:1125-1163 ajaxPaymentManagementV2
* Vị trí: Admin\AffiliateInfoController.php:1264-1317 exportCsvV2
* Route: POST /admin/ajax-payment-management-v2 (web.php:473), /admin/payment-management/export-csv (495) — supper_admin · tham số filter_month
* Vấn đề: LIKE '%{$filter_month}%' trong DB::raw/whereRaw; catch trả getMessage() về client.
* Fix: date_format:Y-m + bind; không trả getMessage().

19. SQLI-20 [Normal] — Column-name injection ở màn admin

* Vị trí: Admin\UserController.php:10041 (col_sort) · POST /admin/init-coupon-management (382)
* Vị trí: Admin\Lp\PathIntroController.php:24, 36 · GET /admin/path-intro/list (300)
* Vị trí: Admin\Lp\RestorePathIntroController.php:23, 29 · GET /admin/path-intro/restore/list (309)
* Middleware: supper_admin
* Vấn đề: Column-name injection (tên cột lấy từ request, không whitelist).
* Fix: Whitelist.

20. SQLI-21 [Normal] (Likely) — CalendarSalonTimeBookingRepository: orWhereRaw date

* Vị trí: app/Repositories/Eloquents/CalendarSalonTimeBookingRepository.php:88, 107
* Route: caller booking salon · tham số $date
* Vấn đề: orWhereRaw('DATE(date_setting) = "'.$date.'"') — đa số caller đã parse Carbon.
* Fix: Bind ?.

21. SQLI-22 [Low] — handleKeepSlot: quantity âm lọt qua

* Vị trí: Basic\MobileEventBookingController.php:653, 664 handleKeepSlot (PUBLIC change-booking)
* Tham số: infoOrder[number_order]
* Vấn đề: whereRaw("… + $quantity …") nằm trong ->increment() nên Laravel chặn giá trị không phải số → không khai thác SQLi được, nhưng số âm vẫn lọt → giảm use_people/remain_limit (sai số chỗ).
* Fix: (int) + min:1, bind.

22. SQLI-23 [Low] — Code chết còn pattern nguy hiểm

* Vị trí: Admin\BotController.php:3557 (bản sao của SQLI-01)
* Vị trí: ChatController.php:533 getFriendsES (route đã comment)
* Vấn đề: Pattern nguy hiểm còn trong code.
* Fix: Xoá.

## Steps to reproduce

<!-- Không có — ticket là audit bảo mật trên code tĩnh, không phải 1 bug tái hiện được qua thao tác UI cụ thể. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #43398 không có attachment (0). -->

## Ghi chú thêm của Leader

⚠️ Ticket này **KHÔNG phải 1 bug đơn, mà là 22 lỗ hổng SQL Injection** phát hiện qua security audit (đã bỏ SQLI-01, SQLI-08 — không nằm trong scope fix lần này). Dev đã làm **5 vòng bàn giao (v1 → v5)** qua journal, review bởi Dev Studio + automation Test Studio, với nhiều bug con phát sinh (#43513 → #43525, automation #3289 → #3341) — đa số được Dev xác nhận "không đổi code / hành vi base / lỗi kịch bản test", một số đã sửa thật (xem file 03 mục 3).

- **Nguyên tắc test cốt lõi** (Dev nhấn mạnh xuyên suốt 5 vòng): filter **hợp lệ** phải cho **đúng số bạn bè như trước fix** (bất biến); filter có **điều kiện hỏng** (enum dạng chữ, id dạng chữ, point không phải số) phải cho **0 người** (fail-closed) — ở HEAD vòng 2 cũ, điều kiện hỏng từng bị bỏ qua và trả về TOÀN BỘ bạn bè (lỗi nghiêm trọng, đã sửa ở v3/D-28).
- **Branch**: `ai_studio_implement_43398` (gốc `release_step_20260930_v2`). Conflict cần xử lý khi merge release: #42752, #42749 (BroadcastV2Controller), #41682/#42444-#42447 (FriendlistController).
- **Ngoài phạm vi ticket này** (Dev liệt kê rõ, KHÔNG được fix ở đây — xem thêm file 03): job Java (nhắc lịch/hành động theo filter_v2) CHƯA sửa SQL injection + filter hỏng vẫn khớp mọi bạn ở job → tách ticket riêng (liên quan Redmine #43514/#43521, bug #3331/#3340); dữ liệu production có `filters_v2` enum dạng chữ (do MCP cũ ghi) sẽ KHÔNG khớp ai sau khi deploy fix này → cần đếm + dọn dữ liệu trước deploy; dọn `template_ids` sai định dạng trên production; trang `/basic/chat/group` trắng do JS thiếu biến `checkFriend` (lỗi JS có từ base, không liên quan SQLi); vài khác biệt hành vi mobile vs web admin (未確認) có từ base.
- **Trạng thái trên MCP LME TEST STUDIO**: task #467 (ticket 43398, feature `friend-filter`) đang ở trạng thái **`blocked`** — lý do: *"agent viết testcase đang chờ tester trả lời / duyệt đề xuất rà bộ case cũ"*. 85 TC đã có (100% do AI viết), kết quả chạy local: 55 pass / 19 fail / 9 other (skip+error) / 2 chưa chạy. Nhiều TC fail do **kỳ vọng TC cũ sai** (hành vi base bị hiểu lầm là bug) — Dev đã note rõ từng case ở journal #145546/#145583, cần Leader/tester xác nhận lại trước khi tin theo exec status.

## Journal / note từ Redmine (nguyên văn)

**Journal #145091 — Dev Studio — 2026-10-19:**

```
Dev Studio · Nội dung thực hiện

Bản thiết kế v1 đã xong và có thể thực thi: 22 mục SQL injection được xác nhận trên code, kế hoạch gồm 22 việc (D-1 đến D-22). Hướng chung: bind mọi giá trị, ép kiểu số cho id, whitelist tên cột và hướng sắp xếp. Riêng bộ lọc nâng cao được làm sạch ngay ở đầu hàm lọc để phủ cả filter đã lưu. SQLI-15 lấy nguyên bản sửa của #42771. Rủi ro lớn nhất là lọc bạn bè sai và xung đột merge với các nhánh #42752, #42749, #42445.

Hướng sửa:
- D-1 Thêm helper đọc danh sách id lưu trong DB, giữ thứ tự và phần tử trùng
- D-2 Bộ lọc nâng cao advanceFilterPost: làm sạch điều kiện ở đầu hàm và bind từng chỗ (SQLI-02)
- D-3 advanceFilter cũ: ép kiểu, bind id/number_date và filter_name (SQLI-03)
- D-4 Xoá advanceFilter/advanceFilterPost không còn nơi gọi trong ConversationReplicate
- D-5 scenario_stop_id/scenario_unfinish_id kiểm số và bind ở FriendlistController và FilterController (SQLI-04)
- D-6 Route lấy câu trả lời form my page: bắt đăng nhập, kiểm bạn thuộc bot, bind (SQLI-05)
- D-7 Chat nhóm: tìm theo từ khoá bằng LIKE có escape và bind (SQLI-06)
- D-8 Form answer my page: route chỉ nhận số, kiểm bạn thuộc bot, bind (SQLI-07)
- D-9 getScenarioToChange bind line_user_id; saveScenario kiểm bạn thuộc bot (SQLI-09)
- D-10 Mobile web danh sách bạn bè và chat: tags ép số dùng placeholder, line_id bind (SQLI-13)
- D-11 Nơi lưu template_ids/sort_ids chỉ nhận id số, từ chối phần tử rác (SQLI-10/11/12/16)
- D-12 11 chỗ FIELD(id, …) chỉ dùng số nguyên, list rỗng thì bỏ sắp xếp (SQLI-10/11/12/16/17)
- D-13 CSV kết quả admin: tham số time kiểm định dạng Y-m và bind (SQLI-14)
- D-14 SQLI-15: cherry-pick bản sửa updatePosition của #42771 (commit 1581ac16c6)
- D-15 Whitelist cột sắp xếp ở 8 màn (SQLI-18)
- D-16 Quản lý thanh toán admin: filter_month kiểm Y-m, LIKE bind, không lộ lỗi (SQLI-19)
- D-17 Whitelist cột sắp xếp ở coupon và path-intro admin (SQLI-20)
- D-18 Cập nhật action schedule chỉ nhận 17 field cho phép (SQLI-24)
- D-19 Lịch salon: bind ngày trong orWhereRaw (SQLI-21)
- D-20 Đổi booking event: số lượng phải là số nguyên trong giới hạn của cài đặt, bind (SQLI-22)
- D-21 Xoá code chết còn pattern nguy hiểm ở Admin BotController và ChatController (SQLI-23)
- D-22 Kiểm tra: php -l, grep lại sink, Feature test nếu vendor chạy được

Ảnh hưởng / rủi ro:
Ảnh hưởng bộ lọc bạn bè (khoảng 70 chỗ gọi), broadcast, step message, chat hẹn giờ, park template, chat nhóm, form my page, kịch bản, mobile web, booking event và vài màn admin. Không đổi schema hay response khi dữ liệu hợp lệ. Rủi ro chính là lọc bạn bè sai, và xung đột merge với các nhánh #42752, #42749, #42445.
```

**Journal #145128 — Dev Studio — 2026-10-19:**

```
Dev Studio · Nội dung thực hiện

Thiết kế v2 xử lý đủ các mục review vòng 1. Thêm mục chặn SQL injection ở bộ lọc trạng thái của chat mobile (ép từng giá trị về số nguyên và dùng binding). Hai API của app chỉ lưu id mẫu tin đã tìm thấy, và số lượng đổi booking sai dùng câu lỗi có sẵn của FE. Thêm unit test, cùng bằng chứng đối chiếu cũ/mới để review soát xong nhóm bộ lọc nâng cao và nhóm admin. Về việc bỏ id tin trùng khi lưu trên UI, mặc định là chấp nhận; người phụ trách vẫn có thể yêu cầu giữ trùng.

Hướng sửa:
- D-23 Lọc trạng thái ở chat mobile: ép từng giá trị về số nguyên và dùng placeholder
- D-24 Hai API của app lưu id mẫu tin đã tìm thấy thay vì chuỗi từ request
- D-25 Đổi booking với số lượng sai định dạng hoặc < 1 báo câu lỗi có sẵn của FE
- D-26 Unit test cho helper parseStoredIdCsv và hàm statusSearch
- D-27 Lập bằng chứng đối chiếu cũ/mới cho bộ lọc nâng cao và nhóm admin/sort/action schedule

Ảnh hưởng / rủi ro:
Vòng này chỉ đổi tab lọc trạng thái của chat mobile, hai API lưu tin của app và câu lỗi số lượng ở đổi booking event; các mục vòng 1 giữ nguyên. Rủi ro thấp, nhưng phải test lại lọc trạng thái chat mobile với nhiều trạng thái. Xung đột merge với các nhánh song sinh vẫn như vòng 1.
```

**Journal #145159 — Dev Studio — 2026-10-19:**

```
Dev Studio · Nội dung thực hiện

Thiết kế v3 sửa lỗi review vòng 2: bộ lọc nâng cao đang bỏ qua điều kiện hỏng, nên trả về toàn bộ bạn bè. Từ bản này, điều kiện hỏng thuộc loại đã biết sẽ không khớp ai, ở cả nhóm AND lẫn OR, giống cách đã làm ở các bộ lọc khác. Loại điều kiện lạ vẫn bỏ qua như cũ. Dữ liệu dev có 16 filter hỏng của hai bot thử nghiệm MCP; ngay ở code gốc chúng cũng đã lọc sai nghĩa. Còn lại: thực thi, thêm test các ca hỏng ở AND/OR và chạy lại harness của review.

Hướng sửa:
- D-28 Điều kiện lọc hỏng của loại đã biết thành "không khớp ai" ở cả nhóm AND và OR
- D-29 Test các ca điều kiện hỏng ở AND/OR và chạy lại kiểm tra

Ảnh hưởng / rủi ro:
Chỉ đổi kết quả của filter có điều kiện hỏng (enum dạng chữ, id dạng chữ, point không phải số): HEAD vòng 2 trả toàn bộ bạn bè, nay trả 0 người. Filter hợp lệ không đổi. Ảnh hưởng mọi nơi dùng bộ lọc nâng cao: danh sách bạn bè, gửi hành động, remind, broadcast, export, mobile.
```

**Journal #145240 — Dev handoff — 2026-10-19 (19/10 11:45, vòng 1):**

```
Dev handoff — 19/10 11:45 · nhánh ai_studio_implement_43398

Tóm tắt:
Vá 22 mục SQL injection theo audit, cộng các lỗi cùng loại tìm thêm khi review (lọc trạng thái chat mobile, writer template_id phía app). Mọi giá trị từ request hoặc từ cột DB nay đi qua binding, ép số nguyên hoặc whitelist; code chết chứa pattern nguy hiểm đã xoá. Khi test, chú ý nhất bộ lọc bạn bè nâng cao (khoảng 67 nơi gọi): filter hợp lệ phải cho đúng số bạn bè như trước, filter có điều kiện hỏng phải ra 0 người.

Nội dung thay đổi:
- Bộ lọc bạn bè nâng cao (danh sách bạn bè, gửi hành động, broadcast đếm số, export CSV, cross analysis, talk list, mobile, remind, booking): mọi điều kiện đi qua binding; id trùng được bỏ trùng; điều kiện hỏng ra 0 người; danh sách rỗng trước đây lỗi SQL nay chạy được.
- Bộ lọc cũ và tìm theo tên: ký tự % và _ được tìm như chữ thường; tên có dấu nháy không còn lỗi.
- Danh sách bạn bè: tham số kịch bản dừng/chưa xong sai thì không khớp ai; lỗi không còn lộ message hệ thống.
- My page: lưu kịch bản kiểm bạn bè thuộc bot (400/404); chi tiết form answer kiểm id số và bạn thuộc bot (trang 404); API lấy form answer my page bắt buộc đăng nhập.
- Chat: tìm nhóm chat escape từ khoá; chat mobile lọc tag và lọc trạng thái chỉ nhận số.
- Bản tin V2, bản tin cũ, chat hẹn giờ, step message, kịch bản, park template, template V2, API app: lưu danh sách id tin chỉ nhận số, payload rác bị từ chối; dữ liệu cũ có ,, hoặc dấu phẩy cuối nay mở được; màn sửa bản tin/chat hẹn giờ bỏ id tin trùng khi lưu lại.
- Sort ở 11 màn (broadcast, QR đã xoá, chi tiết click QR, tag đã xoá, form answer đã xoá, template, rich menu, admin affiliate, supper admin, coupon, path intro) chỉ nhận cột và hướng hợp lệ.
- Admin: CSV kết quả affiliate nhận tháng dạng Y-m (sai thì tháng hiện tại) và tính đúng khoảng ngày; quản lý thanh toán affiliate kiểm filter_month Y-m; lỗi không lộ message.
- Action schedule: cập nhật chỉ nhận 17 field của màn sửa.
- Sắp xếp folder rich menu và hợp đồng (cherry-pick #42771): chặn sắp xếp chéo bot và injection.
- Đổi booking event: số lượng sai định dạng hoặc nhỏ hơn 1 báo 「予約数は、１以上入力してください」; vượt giới hạn báo câu hết chỗ.
- Lịch salon: ngày truy vấn đi qua binding.

Đánh giá ảnh hưởng — Rủi ro trung bình: Thay đổi rộng ở bộ lọc bạn bè dùng chung bởi nhiều luồng có tác dụng thật (gửi tin, hành động); đã đối chiếu SQL base và HEAD hơn 800 lượt và có test, nhưng chưa chạy với DB và runtime thật.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy:
- Không đổi JS/CSS nên không cần bump version.
- Gộp release phải xử lý conflict với #42752, #42749, #41682 và #42444-#42447.
- Nên đếm trên production các filter filters_v2 có enum dạng chữ trước khi deploy, vì sau deploy chúng không khớp ai.

Việc cần người làm thêm (ngoài phạm vi task):
- Đếm trên production các filter_v2 có enum dạng chữ hoặc info_search dạng chữ (dữ liệu MCP cũ) đang gắn với broadcast hoặc hành động còn hiệu lực; sửa dữ liệu ở ticket riêng.
- Dọn dữ liệu template_ids sai định dạng trên production.
- Job Java tự lọc theo filter_v2: cần rà SQL injection ở ticket của module job.
- Bên job linect: đưa McpModel.convertFilterData (chuyển enum chữ sang số khi MCP ghi filter) vào nhánh job đang phát hành.
- Đã có từ trước, ngoài ticket: route public rollbackChangeBookingConfirmFail giảm số chỗ đã đặt theo quantity lấy từ request; booking event mới (payment) chưa chặn số lượng âm.
- Đã có từ trước, ngoài ticket: SQLI-01 có vẻ vẫn còn ở HandleCallbackMessage; tag_filter/conversion_filter ở FilterController::ajaxGetListUserFilter còn implode thô; route /ajax/supper-admin/* không kiểm super admin.

Điểm cần test:
- Filter có điều kiện tag/QR/kịch bản dạng chữ (has, exclude_any, not_joined) hoặc trường thông tin bạn bè dạng chữ: đếm 0 người, không phải toàn bộ bạn bè.
- Nhóm OR có một điều kiện hỏng và một điều kiện hợp lệ: kết quả bằng điều kiện hợp lệ; tất cả hỏng thì 0 người.
- Hành động có điều kiện, remind và đếm số broadcast dùng filter hỏng: không chạy cho ai.
- Filter hợp lệ của mọi loại điều kiện (AND/OR, filter đã lưu) cho cùng kết quả như vòng 2.
- Bộ lọc bạn bè nâng cao: từng loại điều kiện (tag 4 kiểu, kịch bản, conversion, QR, thông tin bạn bè, point), AND/OR, filter đã lưu, đếm số broadcast, export, mobile cho cùng số bạn bè như trước.
- Filter có điều kiện hỏng (enum chữ hoặc id chữ) ở nhóm AND hoặc OR: kết quả 0 người, không phải toàn bộ bạn bè.
- Hành động có điều kiện lọc và remind: chỉ áp cho bạn thỏa điều kiện.
- Chat mobile tab trạng thái: 未確認 / 確認済み / trạng thái tự tạo cho cùng danh sách; payload trong search_status không lỗi, không thêm hội thoại.
- Bản tin V2, chat hẹn giờ, step, park template: thứ tự tin như cũ; dữ liệu cũ có ,, hoặc dấu phẩy cuối mở được; lưu payload rác bị từ chối; id tin trùng được bỏ trùng khi sửa/lưu.
- Sort 11 màn (broadcast, QR, tag, form answer đã xoá, template, rich menu, admin affiliate/supper admin/coupon/path intro) đúng với cột hợp lệ.
- Cập nhật action schedule lưu đủ field ở lặp ngày/tuần/tháng và các kiểu kết thúc.
- Đổi booking event: số lượng 0, -1, abc báo 「予約数は、１以上入力してください」; vượt giới hạn báo câu cũ; số hợp lệ đổi được.
- My page: lưu kịch bản với bạn của bot khác bị chặn (404); chi tiết form answer id không phải số hoặc bạn bot khác ra trang 404; API form answer my page khi chưa đăng nhập trả 401.
- Admin: CSV kết quả affiliate theo tháng đúng số liệu; quản lý thanh toán affiliate lọc tháng và export CSV hoạt động.

Branch: ai_studio_implement_43398 — sns-line: ai_studio_implement_43398 (nhánh gốc release_step_20260930_v2 @d137c1851896, commit 6191768988a86289cb32a0d364e285e54e4b264d)
```

**Journal #145504 — Dev Studio — 2026-10-20:**

```
Dev Studio · Nội dung thực hiện

Đã đối chiếu 12 bug automation (#3289–#3300) với code base và nhánh. Không bug nào do bản sửa SQL injection gây ra. Nhánh không đổi màn hình, JS, lệnh xuất CSV hay API app. Các bug còn lại do dữ liệu test (lịch thiếu ngày kết thúc), do kịch bản không khớp UI, hoặc là hành vi có sẵn từ base (không có thông báo khi đổi kịch bản, CSV 0 người không có file, API app cần chữ ký). Vòng này không sửa code. D-30 chỉ lập bằng chứng base = HEAD để Review trả lời từng bug. Các cải tiến UX đã ghi vào follow-up.

Hướng sửa:
- D-30 Kiểm chứng base = HEAD cho các luồng bị báo, không sửa code

Ảnh hưởng / rủi ro:
Vòng này không đổi code. Kết quả các vòng 1–3 giữ nguyên. Rủi ro duy nhất là Test Studio chạy lại với kịch bản cũ thì các bug này sẽ tiếp tục báo.
```

**Journal #145546 — Dev handoff — 2026-10-20 (20/10 09:39, vòng 4):**

```
Dev handoff — 20/10 09:39 · nhánh ai_studio_implement_43398

Tóm tắt:
Vá 22 mục SQL injection theo audit, cùng các lỗi cùng loại tìm thêm trong lúc làm (lọc trạng thái chat mobile, ghi template_id phía app). Mọi giá trị đến từ request hoặc cột DB nay đều đi qua binding, ép số nguyên hoặc whitelist; code chết chứa pattern nguy hiểm đã xoá. Vòng 4 không đổi code: 12 bug automation #3289–#3300 là hành vi base, do dữ liệu test hoặc do kịch bản. Khi test, chú ý nhất bộ lọc bạn bè nâng cao: filter hợp lệ phải cho đúng số người như trước, filter có điều kiện hỏng phải ra 0 người.

Bug automation Test Studio (12 bug — tất cả "không phải bug"):
- #3289: Màn 友だち詳細, lưu kịch bản thành công không hiện thông báo — base cũng vậy (DB + 購読中 đúng). Yêu cầu UI riêng nếu muốn có toast.
- #3290: Mở trực tiếp trang answer_form: A1 trả 200; 5 giá trị sai/bạn bot khác đều trả 404 → bảo mật ĐẠT, kịch bản test không khớp UI (mở qua drawer).
- #3291: Nút 保存 chat hẹn giờ không ghi template_ids ở base cũng vậy. Id trùng chỉ mất khi xoá/sắp xếp tin. Kỳ vọng TC sai do câu review v3 đã sửa.
- #3292: Rich menu không có cột 位置; vị trí đổi qua nút 並べ替え. Sort theo tên/ngày tạo/ngày sửa/mặc định đều đúng.
- #3293, #3300: Fixture TC43398_AS có end_date NULL từ trước — danh sách lịch (code base) không đọc được NULL → "Data missing". Lưu thành công, DB đúng. Cần sửa fixture có end_date.
- #3294: /api/mobile/save-sort-step-messages thuộc nhóm api-job-auth (chữ ký, không nhận JWT app) — routes/api.php không đổi. Cần gọi bằng request ký api-job.
- #3295–#3298: Lỗi kịch bản automation (locator nút 保存 không khớp, exception helper addQr, timeout popup, chờ nhầm nút 手動変更) — view/endpoint không đổi.
- #3299: HandleExportCsv không đổi — 0 người = 0 trang = không ghi file, ở base cũng vậy. Phần cần kiểm (filter hỏng → 0 người, job hoàn tất không lỗi) đều ĐẠT.

File đã sửa (vòng 4, php-web, 43 files changed, 1327 insertions, 3614 deletions — danh sách đầy đủ xem file 03 mục 3).

Đánh giá ảnh hưởng — Rủi ro trung bình: Thay đổi rộng ở bộ lọc bạn bè dùng chung bởi nhiều luồng có tác dụng thật (gửi tin, hành động); đã đối chiếu SQL base và HEAD hơn 800 lượt và có test, nhưng chưa chạy với DB/runtime thật.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy: không đổi JS/CSS; merge conflict với #42752, #42749 (BroadcastV2Controller), #41682/#42444-#42447 (FriendlistController) — ngày 20/10 các nhánh này chưa vào base, merge vào base hiện tại (0ca93d30b7) không conflict. Nên đếm production filters_v2 enum chữ trước deploy.

Việc cần người làm thêm (ngoài phạm vi task): Test Studio sửa kịch bản/dữ liệu test (NEW-25, NEW-28, NEW-43, NEW-48, NEW-53/57, NEW-36, NEW-12, locator helper #3295-3298); cải tiến riêng (end_date NULL, export CSV 0 người tạo file rỗng, toast đổi kịch bản); API app save-sort-step-messages chưa kiểm step_message thuộc bot (lỗi phân quyền, không phải SQLi, cần ticket riêng).

Branch: ai_studio_implement_43398 — sns-line: ai_studio_implement_43398 (nhánh gốc release_step_20260930_v2 @d137c1851896, commit 2610cfbaeaba4d847bf4097dab2a1553346c5cec)
```

**Journal #145578 — Dev Studio — 2026-10-20:**

```
Dev Studio · Nội dung thực hiện

Đã cập nhật v5 theo trả lời của HieuTM: hai bug hành động hàng loạt và nhắc lịch (#3331, #3340) do job Java, ngoài phạm vi web, không sửa trong ticket này. Kế hoạch web giữ nguyên ba chỗ sửa nhỏ kèm test: thứ tự mặc định của danh sách khôi phục path intro, sắp xếp rich menu báo thất bại khi gửi id rác, lọc trạng thái mobile bỏ giá trị rác. Tám bug còn lại có từ base hoặc kỳ vọng test sai. Sẵn sàng thực thi.

Hướng sửa:
- D-31 Danh sách khôi phục path intro: cột hoặc chiều sắp xếp lạ quay về thứ tự mặc định
- D-32 Sắp xếp folder rich menu và rich menu báo thất bại khi có id không phải số
- D-33 Màn danh sách bạn bè mobile làm sạch giá trị trạng thái lọc
- D-34 Test cho D-31..D-33 và chạy lại kiểm tra

Ảnh hưởng / rủi ro:
Thay đổi nhỏ ở 3 màn: danh sách khôi phục path intro (system admin), sắp xếp rich menu và danh sách bạn bè mobile. Cần test lại sắp xếp hợp lệ trên FE và lọc thẻ/trạng thái hợp lệ trên mobile. Job Java không đổi; bộ lọc hỏng chạy qua job vẫn khớp mọi bạn cho tới khi có ticket riêng.
```

**Journal #145583 — Dev handoff — 2026-10-20 (20/10 10:03, vòng 5 — BẢN GIAO CUỐI):**

```
Dev handoff — 20/10 10:03 · nhánh ai_studio_implement_43398

Tóm tắt:
Vá 22 mục SQL injection theo audit, cùng các lỗi cùng loại tìm thêm. Vòng 5 sửa thêm 3 điểm từ automation: thứ tự mặc định của danh sách khôi phục path intro, sắp xếp rich menu với id rác, và lọc trạng thái trên danh sách bạn bè mobile. Khi test, chú ý nhất bộ lọc bạn bè nâng cao phía web: filter hợp lệ phải đúng số người như trước, filter có điều kiện hỏng phải ra 0 người. Job Java (nhắc lịch, hành động theo bộ lọc) chưa sửa, đã tách ticket riêng.

Bug QA con (13 bug, #43513–#43525):
- #43513, #43515, #43522, #43565 (JS base): trang nhóm chat /basic/chat/group trắng vì chat_group.js thiếu biến checkFriend — lỗi có từ base, không liên quan SQLi, cần ticket riêng sửa JS hoặc Reject.
- #43514, #43521 (ngoài phạm vi web): nhắc lịch/hành động hàng loạt theo filter_v2 chạy ở job Java — HieuTM chốt 20/10 là ngoài phạm vi, tách ticket cho job.
- #43516 ĐÃ SỬA (commit sns-line@97946a2623dc, c0a61e80451f, 2610cfbaeaba): path intro restore list — cột/chiều lạ quay về deleted_at ASC (mặc định); FE ASC/DESC vẫn đúng. Có test.
- #43517 ĐÃ SỬA (commit sns-line@98eab1daa16b, 2610cfbaeaba): sort folder/rich menu — id không phải số nguyên dương → status:false, không ghi DB; danh sách hợp lệ vẫn đúng. Có test.
- #43518 không đổi code: gửi v2Child dạng mảng trả 400 — kiểm tra có từ base (#40056/#41580); CSV rác trả 403 theo thiết kế. Cần sửa kỳ vọng TC.
- #43519 ĐÃ SỬA (commit sns-line@5d1fecea41d9, 2610cfbaeaba): mobile list friend search_status chỉ giữ số nguyên, giữ 0 (未確認); giá trị rác bị bỏ (không lọc nhầm thành 1). Có test.
- #43520 không đổi code: nút lưu chat hẹn giờ/bước kịch bản không ghi template_ids ở base cũng vậy — chuẩn hoá chỉ khi thêm/xoá/sắp xếp tin. Cần sửa kỳ vọng TC.
- #43523 không đổi code: mobile hiểu 未確認 khác web admin — khác biệt có từ base.
- #43524 không đổi code: drawer câu trả lời chỉ hiện lần được chọn, như base. Cần sửa kỳ vọng TC.
- #43525 không đổi code: kéo thả bản tin V2 bị tắt (disabled: true) từ 02/2024, có từ base. Cần sửa kỳ vọng TC.

File đã sửa (vòng 5 — BẢN CUỐI, php-web, 46 files changed, 1575 insertions, 3616 deletions — danh sách đầy đủ xem file 03 mục 3).

Đánh giá ảnh hưởng — Rủi ro trung bình: Thay đổi rộng ở bộ lọc bạn bè dùng chung bởi nhiều luồng có tác dụng thật; đã đối chiếu SQL base và HEAD cùng test, nhưng chưa chạy với DB thật. Vòng 5 chỉ thêm kiểm tra đầu vào hẹp, có test.
- Filter filters_v2 có enum dạng chữ (MCP cũ ghi) sẽ không khớp ai ở phía web (fail-closed) sau deploy.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy: không đổi JS/CSS; merge conflict với #42752, #42749 (BroadcastV2Controller), #41682/#42444-#42447 (FriendlistController) — gộp vào base hiện tại (b1e34b8cfe) không conflict. Nên đếm production filters_v2 enum chữ trước deploy.

Việc cần người làm thêm (ngoài phạm vi task): ticket riêng cho job Java (bug #3331, #3340 — HieuTM chốt ngoài phạm vi web 20/10); ticket sửa JS trang nhóm chat; xác nhận chủ ý/lỗi việc kéo thả bản tin V2 bị tắt từ 02/2024; cân nhắc thống nhất 未確認 mobile vs web; Test Studio sửa kỳ vọng nhiều TC (NEW-35, NEW-42, NEW-40, NEW-24, NEW-32/33/65, NEW-14/15); rủi ro nhỏ đã CHẤP NHẬN ở D-32: id dạng "+5" qua được luật integer nhưng service bỏ qua → vẫn trả status:true mà không ghi gì (muốn chặn hẳn cần regex chỉ nhận chữ số, để ticket sau).

Branch: ai_studio_implement_43398 — sns-line: ai_studio_implement_43398 (nhánh gốc release_step_20260930_v2 @d137c1851896, commit 2610cfbaeaba4d847bf4097dab2a1553346c5cec)
```
