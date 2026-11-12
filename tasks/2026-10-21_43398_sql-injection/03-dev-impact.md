# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Truong Minh Hieu` (assigned_to Redmine; journal ký "Dev Studio" / "HieuTM") |
| Commit / Pull Request | `<chưa có PR — xem commit lẻ ở mục 3>` |
| Branch | `ai_studio_implement_43398` (gốc `release_step_20260930_v2` @`d137c1851896`; bản giao cuối tại commit `2610cfbaeaba4d847bf4097dab2a1553346c5cec`) |
| Ngày submit đánh giá | `2026-10-20` (journal #145583 — bản giao vòng 5, bản cuối) |
| Auto-filled | `2026-10-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ Ticket này không có section "Đánh giá ảnh hưởng phía dev" theo format chuẩn (1./2./3./4.1/4.2/4.3) trong Description — nội dung dưới đây được tổng hợp từ **Description gốc (22 mục SQLI)** + **8 journal "Dev Studio"/"Dev handoff" qua 5 vòng (v1→v5)** + **MCP LME TEST STUDIO task #467** (`dev_impact`, `spec_delta.diffStat`). Paste/tổng hợp nguyên văn, không diễn giải lại nội dung kỹ thuật.

---

## 1. Nguyên nhân

Audit bảo mật phát hiện **22 lỗ hổng SQL Injection** (đã bỏ SQLI-01, SQLI-08) trên code hiện hành. Hai nhóm nguyên nhân chính:

**Nhóm A — Nội suy giá trị trực tiếp vào SQL thô** (`whereRaw` / `DB::raw` / `orderByRaw` / `selectRaw`), không bind, không ép kiểu:
- SQLI-02: `Conversation::advanceFilterPost()` (+ bản Replicate) — **>40 chỗ** nội suy điều kiện lọc (tags_search, scenario_id, number_date, conversion, idInfo, point, value IN(...), nhánh OR) vào `whereRaw`/`DB::raw`. **Second-order**: filter lưu ở `filter_v2.data`, được `FilterV2::initDataFilter` chạy lại trong `HelperService::sendAction`, `RemindApiController@startRemind`, job export.
- SQLI-03: `advanceFilter()` cũ không cast `id`/`number_date`.
- SQLI-04: `postFilterAdvance`/`sendActionFriend` nội suy `scenario_stop_id` vào `whereRaw`; giá trị còn lưu lại vào `FilterV2.data.scenario_search` → second-order lặp lại SQLI-02.
- SQLI-05: `getDataFormAnswerMyPage` nội suy `user_id` vào `DB::raw` — **route PUBLIC không auth**.
- SQLI-06: `getGroupChat` nội suy `keyword` vào LIKE.
- SQLI-07: `myPageFormDetails` nội suy `line_id` lấy từ route (không regex).
- SQLI-09: `getScenarioToChange` nội suy `line_user_id` vào `CASE WHEN`.
- SQLI-13: Mobile list friend/chat — `implode($tags)` vào `IN(...)`, `orderByRaw` với `line_id`.
- SQLI-14: Admin `resultDownloadCsv` nội suy `time` vào `selectRaw`.
- SQLI-15: `CategoryService::updatePosition` nội suy `id`/`pos` vào `CASE`.
- SQLI-21: `CalendarSalonTimeBookingRepository` nội suy `date` vào `orWhereRaw`.

**Nhóm B — `FIELD(id, …)` / `orderBy` dùng giá trị lưu sẵn trong DB chưa được lọc (2nd-order)**:
- SQLI-10/11/12/16/17: `template_ids` (Broadcast V2, Schedule send chat, Step message, Park template) và `template.content` được lưu nguyên từ request (hàm `normalizeIdList()` cũ bỏ qua phần tử không phải số nên payload rác lọt qua và được LƯU), rồi dùng trong `FIELD(id, $ids)` khi hiển thị/sort — tổng **11 sink**.

**Nhóm C — Column-name injection / mass-assignment**:
- SQLI-18, SQLI-20: `orderBy($request->order_by)` ở nhiều màn (Broadcast, QRCode, Tag, FormAnswer removed, Category/template, RichMenu, Admin Affiliate/SupperAdmin/Coupon/PathIntro) — tên cột không whitelist.
- SQLI-24: `ActionScheduleController` dùng `$request->except([...])` rồi `update($data)` — key của body JSON trở thành tên cột trong `UPDATE … SET`, ghi được mọi cột.

**Nhóm D — Thiếu validate input nghiệp vụ (không phải SQLi thuần nhưng cùng audit)**:
- SQLI-19: Admin payment `filter_month` LIKE không validate `Y-m`; lỗi còn trả `getMessage()` lộ ra client.
- SQLI-22: `handleKeepSlot` — `quantity` âm lọt qua (Laravel `->increment()` chặn SQLi nhưng không chặn số âm) → sai số `use_people`/`remain_limit`.
- SQLI-23: code chết còn chứa pattern nguy hiểm (`Admin\BotController.php:3557`, `ChatController.php:533 getFriendsES` route đã comment).

**Phát sinh thêm trong lúc fix** (ngoài 22 mục audit gốc, Dev tự tìm thấy cùng loại): lọc trạng thái (`search_status`) ở chat mobile/mobile list friend không ép kiểu; 2 API app lưu `template_id` thô từ request thay vì id mẫu tin đã tìm thấy; sort ở path-intro restore list và rich menu folder/rich menu nhận cột/chiều/id rác.

**Bug nghiêm trọng tự phát hiện trong quá trình fix (vòng 2→3, đã sửa ở v3/D-28)**: bản sửa ban đầu của advanceFilterPost **bỏ qua** điều kiện lọc hỏng (enum dạng chữ, id dạng chữ, point không phải số) → query chạy nhưng **trả về TOÀN BỘ bạn bè** thay vì lọc đúng. Từ v3, điều kiện hỏng (loại đã biết) → **không khớp ai** (fail-closed), ở cả nhóm AND và OR.

## 2. Cách fix

Hướng chung xuyên suốt: **bind mọi giá trị** (`?` placeholder), **ép kiểu số** (`intval`) cho mọi id, **whitelist** tên cột/hướng sort bằng `in_array`, validate cấu trúc input (`in:`, `date_format:Y-m`), và với điều kiện lọc hỏng → **fail-closed** (không khớp ai) chứ không bỏ qua điều kiện.

**Vòng 1 (D-1 → D-22, journal #145091/#145240)**:
- D-1: Helper mới đọc danh sách id lưu trong DB, giữ thứ tự + phần tử trùng.
- D-2: `advanceFilterPost` — làm sạch điều kiện ngay đầu hàm, bind từng chỗ (SQLI-02).
- D-3: `advanceFilter` cũ — ép kiểu, bind `id`/`number_date`/`filter_name` (SQLI-03).
- D-4: Xoá `advanceFilter`/`advanceFilterPost` không còn nơi gọi trong `ConversationReplicate`.
- D-5: `scenario_stop_id`/`scenario_unfinish_id` kiểm số + bind (SQLI-04).
- D-6: Route form answer my page — bắt đăng nhập, kiểm bạn thuộc bot, bind (SQLI-05).
- D-7: Chat nhóm — LIKE có escape + bind (SQLI-06).
- D-8: Form answer my page — route chỉ nhận số, kiểm bạn thuộc bot, bind (SQLI-07).
- D-9: `getScenarioToChange` bind `line_user_id`; `saveScenario` kiểm bạn thuộc bot (SQLI-09).
- D-10: Mobile web — tags ép số dùng placeholder, `line_id` bind (SQLI-13).
- D-11/D-12: Nơi lưu `template_ids`/`sort_ids` chỉ nhận id số, từ chối phần tử rác; 11 chỗ `FIELD(id, …)` chỉ dùng số nguyên, list rỗng → bỏ sắp xếp (SQLI-10/11/12/16/17).
- D-13: CSV kết quả admin — `time` kiểm `Y-m` + bind (SQLI-14).
- D-14: SQLI-15 cherry-pick bản sửa `updatePosition` của #42771 (commit `1581ac16c6`).
- D-15/D-17: Whitelist cột sort ở 8 màn + coupon/path-intro admin (SQLI-18, SQLI-20).
- D-16: Payment admin — `filter_month` kiểm `Y-m`, bind, không lộ message lỗi (SQLI-19).
- D-18: Action schedule update — chỉ nhận 17 field cho phép (SQLI-24).
- D-19: Lịch salon — bind ngày (SQLI-21).
- D-20: Đổi booking event — số lượng phải nguyên trong giới hạn, bind (SQLI-22).
- D-21: Xoá code chết còn pattern nguy hiểm (SQLI-23).
- D-22: Kiểm `php -l`, grep lại sink, Feature test.

**Vòng 2 (D-23 → D-27, journal #145128)**: lọc trạng thái chat mobile ép số + placeholder; 2 API app lưu id mẫu tin đã tìm thấy (không phải chuỗi từ request); đổi booking số lượng sai → câu lỗi có sẵn FE; unit test `parseStoredIdCsv` + `statusSearch`; bằng chứng đối chiếu cũ/mới.

**Vòng 3 (D-28 → D-29, journal #145159) — SỬA LỖI NGHIÊM TRỌNG CỦA VÒNG 2**: điều kiện lọc hỏng (loại đã biết) → không khớp ai ở cả AND/OR (trước đó HEAD vòng 2 trả về toàn bộ bạn bè — xem mục 1). Loại điều kiện lạ vẫn bỏ qua như cũ (không đổi).

**Vòng 4 (journal #145504/#145546) — KHÔNG đổi code**: đối chiếu 12 bug automation #3289-#3300 → xác nhận tất cả là hành vi base/lỗi dữ liệu test/lỗi kịch bản, không do fix SQLi gây ra (D-30: lập bằng chứng base = HEAD).

**Vòng 5 — BẢN GIAO CUỐI (D-31 → D-34, journal #145578/#145583)**:
- D-31: Path-intro restore list — cột/chiều sort lạ → quay về mặc định (`deleted_at` ASC).
- D-32: Sort folder rich menu / rich menu — id không phải số nguyên dương → `status:false`, không ghi DB, không chéo bot. (Rủi ro nhỏ đã CHẤP NHẬN: id dạng `"+5"` qua được luật `integer` nhưng service bỏ qua → vẫn trả `status:true` mà không ghi gì; muốn chặn hẳn cần regex chữ số thuần, để ticket sau.)
- D-33: Mobile list friend — làm sạch giá trị `search_status` (request + session), giữ `0` = 未確認, giá trị rác bị bỏ (không lọc nhầm).
- D-34: Test cho D-31..D-33 + chạy lại kiểm tra.

Helper/hàm mới: `parseStoredIdCsv` (functions.php) đọc danh sách id lưu trong DB giữ thứ tự + trùng; `normalizeIdList` (có sẵn) được dùng thêm ở các sink.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

Diffstat cuối cùng (vòng 5, từ MCP LME TEST STUDIO `spec_delta.diffStat`, task #467) — **46 files changed, 1575 insertions(+), 3616 deletions(-)**:

| # | File | Thay đổi | Lý do |
|---|---|---|---|
| 1 | `app/Category.php` | +18/-? | Sink `FIELD(id, …)` park template (SQLI-16) |
| 2 | `app/CategoryReplicate.php` | +18/-? | Bản Replicate của Category |
| 3 | `app/Conversation.php` | 618 dòng đổi | Lõi `advanceFilterPost`/`advanceFilter` (SQLI-02/03) |
| 4 | `app/ConversationReplicate.php` | -1519 dòng (xoá đa số) | Xoá code không còn nơi gọi (D-4) |
| 5 | `app/Helpers/functions.php` | +49 | Helper `parseStoredIdCsv` mới (D-1) |
| 6 | `app/Http/Controllers/Admin/AffController.php` | +12/-? | CSV kết quả — `time` → `Y-m` + bind (SQLI-14) |
| 7 | `app/Http/Controllers/Admin/AffiliateInfoController.php` | +74/-? | Payment management — `filter_month` (SQLI-19) |
| 8 | `app/Http/Controllers/Admin/BotController.php` | -1304 (xoá) | Xoá 15 hàm private chết (SQLI-23) |
| 9 | `app/Http/Controllers/Admin/Lp/PathIntroController.php` | +5 | Whitelist sort (SQLI-20) |
| 10 | `app/Http/Controllers/Admin/Lp/RestorePathIntroController.php` | +6 | Whitelist sort + default fallback (D-31) |
| 11 | `app/Http/Controllers/Admin/SupperAdminController.php` | +21/-? | Whitelist sort (SQLI-18) |
| 12 | `app/Http/Controllers/Admin/UserController.php` | +10/-? | Whitelist sort coupon (SQLI-20) |
| 13 | `app/Http/Controllers/Api/ChatController.php` | +4/-? | API app — lưu id tin đã tìm thấy (D-24) |
| 14 | `app/Http/Controllers/Api/Mobile/ScenarioMobileController.php` | +10/-? | API app liên quan kịch bản |
| 15 | `app/Http/Controllers/Basic/ActionScheduleController.php` | +10/-? | `only()` 17 field whitelist (SQLI-24) |
| 16 | `app/Http/Controllers/Basic/BroadcastController.php` | +12/-? | Whitelist sort (SQLI-18) |
| 17 | `app/Http/Controllers/Basic/BroadcastV2Controller.php` | +47/-? | `template_ids` sink (SQLI-10) |
| 18 | `app/Http/Controllers/Basic/FilterController.php` | +26/-? | `scenario_stop_id`/`unfinish_id` (SQLI-04) |
| 19 | `app/Http/Controllers/Basic/FormAnswerController.php` | +24/-? | `myPageFormDetails` (SQLI-07), whitelist sort (SQLI-18) |
| 20 | `app/Http/Controllers/Basic/FriendlistController.php` | +72/-? | Nguồn id/number_date/scenario_stop_id (SQLI-03/04/09) |
| 21 | `app/Http/Controllers/Basic/MessageTemplateController.php` | +16/-? | `sortItem` nguồn park template (SQLI-16) |
| 22 | `app/Http/Controllers/Basic/MobileEventBookingController.php` | +37/-? | `handleKeepSlot` quantity (SQLI-22) |
| 23 | `app/Http/Controllers/Basic/QRCodeController.php` | +10/-? | Whitelist sort (SQLI-18) |
| 24 | `app/Http/Controllers/Basic/ScenarioController.php` | +11/-? | Nguồn `template_ids` step (SQLI-12) |
| 25 | `app/Http/Controllers/Basic/ScheduleSendChatController.php` | +34/-? | `template_ids` sink (SQLI-11) |
| 26 | `app/Http/Controllers/Basic/StepMessageController.php` | +45/-? | `template_ids` sink step message (SQLI-12), park template (SQLI-16) |
| 27 | `app/Http/Controllers/Basic/TagController.php` | +13/-? | Whitelist sort (SQLI-18) |
| 28 | `app/Http/Controllers/Basic/TemplateV2Controller.php` | +14/-? | Template V2 id tin |
| 29 | `app/Http/Controllers/ChatController.php` | -497 (đa số xoá) | `getGroupChat` (SQLI-06), `getDataFormAnswerMyPage` (SQLI-05), xoá `getFriends`/`getFriendsES`/`index` dead code |
| 30 | `app/Http/Controllers/Mobile/ChatMobileController.php` | +10/-? | tags/line_id (SQLI-13), search_status |
| 31 | `app/Http/Controllers/Mobile/ListFriendController.php` | +26/-? | tags/line_id (SQLI-13), search_status (D-33) |
| 32 | `app/Http/Controllers/V2/Bill/ListPageController.php` | +42/-? | `saveContractPosition` (SQLI-15) |
| 33 | `app/Http/Controllers/V2/RichMenuController.php` | +27/-? | Sort folder/rich menu whitelist + validate id (SQLI-15, D-32) |
| 34 | `app/Repositories/Eloquents/CalendarSalonTimeBookingRepository.php` | +4/-? | Bind ngày (SQLI-21) |
| 35 | `app/Repositories/Eloquents/TemplateRepository.php` | +5/-? | `handleTypeTemplate` FIELD(id, content) (SQLI-17) |
| 36 | `app/Scenario.php` | +3/-? | `getScenarioToChange` (SQLI-09) |
| 37 | `app/ScenarioReplicate.php` | +3/-? | Bản Replicate |
| 38 | `app/Services/V2/CategoryService.php` | +15/-? | `updatePosition` CASE WHEN (SQLI-15, cherry-pick #42771) |
| 39 | `app/Services/V2/RichMenuService.php` | +4/-? | Hỗ trợ validate id sort rich menu |
| 40 | `routes/web.php` | +6/-? | Thêm `check_login` cho form answer my page route, regex id |
| 41 | `tests/Feature/ConversationFilterRejectedItemTest.php` | +124 (mới) | Test điều kiện lọc hỏng → 0 người (D-29) |
| 42 | `tests/Feature/ConversationStatusSearchTest.php` | +82 (mới) | Test `search_status` chat mobile |
| 43 | `tests/Feature/MobileListFriendSearchStatusTest.php` | +45 (mới) | Test search_status mobile list friend (D-34) |
| 44 | `tests/Feature/RestorePathIntroSortTest.php` | +96 (mới) | Test sort path-intro restore (D-34) |
| 45 | `tests/Feature/RichMenuSortValidationTest.php` | +84 (mới) | Test validate id sort rich menu (D-34) |
| 46 | `tests/Unit/ParseStoredIdCsvTest.php` | +79 (mới) | Test helper `parseStoredIdCsv` |

**Commit lẻ đã merge/cherry-pick** (từ bug QA con #43516-#43519, journal #145583): `sns-line@97946a2623dc`, `sns-line@c0a61e80451f`, `sns-line@98eab1daa16b`, `sns-line@5d1fecea41d9`, `sns-line@2610cfbaeaba` (base cuối).

**Function caller đã Dev tự xác nhận KHÔNG bị ảnh hưởng** (code chết, xoá an toàn): `Admin\BotController` 15 hàm private chết; `ChatController::getFriends`/`getFriendsES`/`index` (route đã comment); `ConversationReplicate::advanceFilter*` (không còn nơi gọi).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Conversation::advanceFilterPost()` (+ Replicate) | `app/Conversation.php` | Direct | **~67 nơi gọi** — friend list, gửi hành động, export CSV (web+command), cross analysis, talk list, broadcast đếm số, filter V2, API mobile filter, API export public (`Api\ListFriendController@getDataExportCsv`, PUBLIC), hành động điều kiện (`HelperService::sendAction`), remind, booking, rich menu. Vùng rủi ro lớn nhất. |
| F2 | `Conversation::advanceFilter()` (bộ lọc cũ) | `app/Conversation.php` | Direct | Auto-reply (`HandleCallbackMessage`), `BotController::checkFilter`, `GET /basic/friendlist/advance-filter`, csvExport nhánh cũ, `sendActionFriend` |
| F3 | `ChatController::getDataFormAnswerMyPage` | `app/Http/Controllers/ChatController.php` | Direct | Route **PUBLIC** → thêm `check_login` (SQLI-05) |
| F4 | `ChatController::getGroupChat` | `app/Http/Controllers/ChatController.php` | Direct | Chat nhóm — tìm theo keyword |
| F5 | `FormAnswerController::myPageFormDetails` | `Basic\FormAnswerController.php` | Direct | Route regex id + `abortIfFriendNotOwned()` (SQLI-07) |
| F6 | `Scenario::getScenarioToChange` (+ Replicate) | `app/Scenario.php`, `app/ScenarioReplicate.php` | Direct | `saveScenario` kiểm bạn thuộc bot (400/404) |
| F7 | `BroadcastV2Controller::saveBroadcastV2/getDetailBroadcastV2/getListMessage` | `Basic\BroadcastV2Controller.php` | Direct + Indirect | `template_ids` ghi + sink FIELD(id,…); job Java đọc cột này (SQLI-10) |
| F8 | `ScheduleSendChatController` (4 action) | `Basic\ScheduleSendChatController.php` | Direct | `template_ids` sink (SQLI-11) |
| F9 | `StepMessageController` (sort/copy step) | `Basic\StepMessageController.php` | Direct | `template_ids` + park template sink (SQLI-12, SQLI-16) |
| F10 | `Mobile\ListFriendController`, `Mobile\ChatMobileController` | `app/Http/Controllers/Mobile/` | Direct | tags, line_id, search_status (SQLI-13, D-33) |
| F11 | `Admin\AffController::resultDownloadCsv`, `Admin\AffiliateInfoController` (payment/CSV) | `Admin\AffController.php`, `Admin\AffiliateInfoController.php` | Direct | `time`/`filter_month` → Y-m (SQLI-14, SQLI-19) |
| F12 | `CategoryService::updatePosition` | `app/Services/V2/CategoryService.php` | Direct | Dùng chung bởi RichMenu sort folder/rich menu + Bill contract position (SQLI-15) |
| F13 | `Category::getTemplateDetailsOfCategoryInPark` (+ Replicate), `TemplateRepository::handleTypeTemplate` | `app/Category.php`, `app/Repositories/Eloquents/TemplateRepository.php` | Indirect (2nd-order) | Đọc `template.content` đã lưu (SQLI-16, SQLI-17) |
| F14 | `orderBy($request->order_by)` ở 11 màn (Broadcast, QRCode×2, Tag, FormAnswer removed, Category/template×2, RichMenu, Admin Affiliate, SupperAdmin, UserController coupon, PathIntro, RestorePathIntro) | nhiều file (xem mục 3) | Direct | Whitelist cột/hướng (SQLI-18, SQLI-20, D-31) |
| F15 | `ActionScheduleController::updateActionSchedule` | `Basic\ActionScheduleController.php` | Direct | `only()` 17 field thay `except()` (SQLI-24) |
| F16 | `CalendarSalonTimeBookingRepository` (query theo date) | `app/Repositories/Eloquents/CalendarSalonTimeBookingRepository.php` | Direct | Lịch salon (SQLI-21) |
| F17 | `MobileEventBookingController::handleKeepSlot` | `Basic\MobileEventBookingController.php` | Direct | Quantity validate (SQLI-22) |
| F18 | `V2\RichMenuController` (sort folder, sort rich menu) | `app/Http/Controllers/V2/RichMenuController.php` | Direct | Validate id integer ≥1, chặn chéo bot (SQLI-15 cherry-pick #42771, D-32) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `filter_v2.data` (JSON: tags_search, scenario_search, item_search/item_search_or, point, idInfo...) | READ (query logic đổi) | **Second-order** — filter đã lưu bị chạy lại ở `FilterV2::initDataFilter`, `HelperService::sendAction`, `RemindApiController@startRemind`, job export. Filter hợp lệ: kết quả giữ nguyên. Filter có điều kiện hỏng (enum/id dạng chữ): từ "trả toàn bộ bạn bè" (bug vòng 2, đã sửa) → **"không khớp ai"**. |
| D2 | `broadcast.template_ids`, `schedule_send_chat.template_ids`, `step_message`/`scenario`.template_ids tương đương | UPDATE (format lưu đổi) | Chỉ nhận id số, payload rác bị từ chối; dữ liệu cũ có `,,` hoặc dấu phẩy cuối **nay mở được** (cải thiện so với trước, không phải regression); id trùng bị bỏ khi **thêm/xoá/sắp xếp** tin (không phải khi bấm nút 保存 không đổi list — giữ như base). Job Java vẫn đọc cột này, giữ format `'1,2,3'`. |
| D3 | `template.content` (park template, clone/transfer) | READ (2nd-order) | `FIELD(id, content)` chỉ dùng số nguyên — cần kiểm dữ liệu cũ sai định dạng vẫn mở được. |
| D4 | `action_schedule.*` (các cột được update) | UPDATE (whitelist 17 field) | Chỉ field của màn sửa được ghi; `next_running_day` lấy từ DB thay vì nhận từ request (thay đổi hành vi nhỏ). |
| D5 | **Production**: `filters_v2` có `*_condition`/`op_compare` dạng enum chữ hoặc `info_search` dạng chữ (ghi bởi **MCP cũ**) | KHÔNG đổi schema, nhưng **đổi ý nghĩa kết quả** | ⚠️ **NGOÀI PHẠM VI TICKET** — sau deploy, các filter này sẽ **không khớp ai** (fail-closed) ở phía web, dù trước đây có thể khớp sai (toàn bộ bạn bè) hoặc đúng 1 phần. Dev yêu cầu **đếm trên production trước khi deploy** và sửa dữ liệu/báo chủ bot ở ticket riêng. |
| D6 | Code chết bị xoá vật lý: `Admin\BotController` (15 hàm private), `ChatController::getFriends/getFriendsES/index`, `ConversationReplicate::advanceFilter*` | DELETE (code, không phải DB) | Dev xác nhận không còn nơi gọi — không ảnh hưởng runtime. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **友だちリスト — bộ lọc bạn bè nâng cao** (danh sách, export CSV, lưu filter, modal 絞り込み) | F1, D1 | **High** — vùng sửa rộng nhất (~67 call site), đã có bug nghiêm trọng tự phát hiện ở vòng 2 (trả toàn bộ bạn bè). Nguyên tắc test: filter hợp lệ bất biến, filter hỏng → 0 người. |
| T2 | **Cross Analysis / Talk List / Broadcast đếm số người / Remind / Export CSV (web + command) / API mobile filter / API export public** | F1, D1 | **High** — dùng chung `advanceFilterPost`, không test riêng từng màn sẽ bỏ lọt. |
| T3 | **アクション実行 có điều kiện lọc** (`HelperService::sendAction`) | F1, D1 | High — gửi hành động sai người nếu filter parse sai. |
| T4 | **友だちリスト — bộ lọc CŨ (絞り込み cũ) + auto-reply theo filter** | F2 | Medium |
| T5 | **My page — đổi kịch bản, xem chi tiết form answer, API form answer my page** | F3, F5, F6 | Medium — route PUBLIC chuyển sang có auth là thay đổi hành vi thật (không bất biến), cần test 400/404/401. |
| T6 | **チャット — グループ (tìm nhóm chat)** | F4 | Low-Medium — kèm lỗi JS có từ base (trang trắng), không phải SQLi nhưng ảnh hưởng khả năng test UI (cần test qua ajax trực tiếp). |
| T7 | **一斉配信 V2, チャット予約 (chat hẹn giờ), ステップ配信, Park template, Template V2, API app lưu sort tin** | F7, F8, F9, F13, D2, D3 | Medium-High — nhiều sink `template_ids`/`content`; job Java đọc lại các cột này (ngoài phạm vi ticket nhưng phải test dữ liệu web ghi ra không làm job vỡ). |
| T8 | **Mobile web — danh sách bạn bè / chat (tags, line_id, search_status)** | F10 | Medium |
| T9 | **System admin — Affiliate CSV/Payment, Coupon, Path intro (+ restore list), SupperAdmin** | F11, F14 | Medium — nhiều màn whitelist sort riêng lẻ, dễ sót 1 màn khi test. |
| T10 | **Rich menu (sort folder/rich menu) + Bill 契約 position** | F12, F18 | Medium — dùng chung `CategoryService::updatePosition`; đã có bug QA con fix thật (#43517). |
| T11 | **Salon booking theo ngày** | F16 | Low |
| T12 | **Mobile event booking — đổi số lượng đặt chỗ (handleKeepSlot)** | F17 | Low-Medium — business rule (không phải SQLi) nhưng ảnh hưởng số liệu `use_people`/`remain_limit`. |
| T13 | **Job Java** (nhắc lịch, hành động hàng loạt theo filter_v2) | D1, D5 | ⚠️ **High nhưng NGOÀI PHẠM VI TICKET** — job KHÔNG được sửa SQLi/fail-closed trong lần này (Dev + HieuTM chốt 20/10, tách ticket riêng, liên quan Redmine #43514/#43521, bug #3331/#3340). Filter hỏng ở job **vẫn khớp mọi bạn** cho tới khi có ticket riêng → rủi ro bảo mật + sai người nhận còn tồn tại ở job sau khi deploy web. |

---

## Ghi chú quan trọng ngoài phạm vi ticket (Leader cần biết trước khi giao TC)

1. **Job Java chưa được fix** — rủi ro SQLi + filter hỏng khớp sai người **vẫn còn** ở nhánh job sau khi fix web này deploy. Không đề xuất TC "job phải fail-closed" cho ticket này; nếu muốn cover thì phải gắn `[Input thiếu]`/ghi rõ đây là theo dõi riêng.
2. **Dữ liệu production cần dọn trước deploy**: `filters_v2` có enum dạng chữ (ghi bởi MCP cũ) sẽ **không khớp ai** sau deploy — Dev yêu cầu đếm số lượng trước khi release. Không phải lỗi code, nhưng là rủi ro vận hành cần Leader note.
3. **13 bug QA con (#43513-#43525) + 12 bug automation (#3289-#3300, #3327-#3341)** đã được Dev triage qua 5 vòng — đa số "không đổi code / hành vi base / lỗi kịch bản test", 4 bug thực sự fixed (#43516, #43517, #43519, tương ứng automation #3333/#3335/#3337). **Review TC cần đối chiếu lại các kết luận này**, không nên tin theo exec status Studio một cách máy móc vì nhiều fail là do kỳ vọng TC cũ sai (không phải code sai) — xem chi tiết trong file 01 (Journal nguyên văn) và file 04 (exec status từng TC).
4. **Task Studio #467 đang `blocked`** chờ tester trả lời/duyệt đề xuất rà bộ case cũ — review lần này nên tính đến việc **đối chiếu & chốt lại bộ 85 TC hiện có** (nhiều TC fail nghi do kỳ vọng sai) hơn là chỉ viết TC mới từ đầu.
5. Vài vấn đề Dev nêu "đã có từ trước, ngoài ticket" (không SQLi, không fix ở đây): `/basic/chat/group` trắng do JS thiếu `checkFriend`; kéo thả bản tin V2 bị tắt từ 02/2024; mobile 未確認 khác web admin; `route /ajax/supper-admin/*` không kiểm super admin; `tag_filter`/`conversion_filter` ở `FilterController::ajaxGetListUserFilter` còn implode thô; SQLI-01 có vẻ còn ở `HandleCallbackMessage`; booking event mới (payment) chưa chặn số lượng âm.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] Đã đọc "Ghi chú quan trọng ngoài phạm vi ticket" ở trên — xác nhận KHÔNG đề xuất TC cho job Java trong task này
