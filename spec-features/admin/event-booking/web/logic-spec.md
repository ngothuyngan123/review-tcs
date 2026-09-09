# Logic Spec — FA-021 「イベント予約」 (Đặt lịch sự kiện)

- **Portal**: Admin (LINE OA) + Staff + trang public LINE User
- **Codebase**: Laravel 5 / PHP 7.2 — `src/web/sns-line/`
- **Phạm vi**: bộ **event day (v2)** — `b_event_detail.type_event_new = 1`. Bộ `booking_event` (v1) là tính năng khác, dùng chung nhiều model nhưng khác controller.

---

## 1. Controllers & Actions

### 1.1 `BookingEventDayManagementController`
`app/Http/Controllers/Basic/BookingEventDayManagementController.php` — 1.925 dòng.

**Dependency injection** (`:55-61`): `StripePayment $stripPayment`, `UnivapayPayment $univapayPayment`.

| Method | Line | Logic chính | Side effects |
|---|---|---|---|
| `listBookingEvent` | 63-86 | Render `basic.booking_event_day.list_event`. Lấy `liff_app_id_booking` (fallback `liff_app_id`), `domain_url_shorten` từ `bots`. Đọc cookie `folder_event_booking_day` (JSON, key = bot_id) để nhớ folder đang mở; validate folder tồn tại (`category.kind = 21`, `is_deleted = 0`), nếu không hợp lệ → reset về `0` | **Ghi cookie** `folder_event_booking_day` (TTL 14400 phút, path `/basic/booking-event-day/list-event`) (`:83`) |
| `listSlotOfEvent` | 88-106 | Render `list_slot_event`; nếu event không tồn tại → redirect list. Exception → redirect route `404` | — |
| `ajaxGetListEvent` | 113-476 | **Hub đa chức năng** theo `$request->action`: `addAndEditGroup`, `deleteGroup`, `removeEvents`, `removeEvent`, `sortItem`, `sortFolder`, `moveItem`. Sau đó luôn trả danh sách folder + sự kiện (paginate 20) + cờ giới hạn gói | CRUD `category`, **xoá cascade thủ công** `b_event_detail` → `b_setting_date_event` → `b_slot` → `b_plan_slot` → `b_user_booking` → `b_setting_basic_event`; xoá `event_step_time`, `event_times`, `user_event` khi slot có `remind_id` và là slot cuối dùng remind đó (`:208-215`) |
| `convertDataSlot` (static) | 477-570 | Tính `max` (tổng định員) và `number_approve_done` / `number_approve_doing` cho từng event. Gắn `hashIdEvent = Hashids::encode(id)` | — (chỉ tính toán) |
| `deletePlanIds` / `deleteActionParent` / `deleteActionItem` / `deleteActionId` | 572-600, 1903-1924 | Xoá plan + các bản ghi action liên quan (`b_detail_action_slot`, `actions`, `action_detail`) | Xoá `actions`, `action_detail`, `b_detail_action_slot` |
| `ajaxGetListSlotOfEvent` | 602-798 | Xoá slot (`removeSlot`/`removeSlots`) rồi trả danh sách slot + plan + số liệu booking theo tab (1 = quá khứ, 2 = sắp tới) và `filter_month` | Xoá `b_slot`, `b_plan_slot`, action |
| `ajaxBookingSave` | 800-961 | Lưu booking (có validate qua `validateFormBooking()` `:909`) | Ghi `b_user_booking` |
| `ajaxGetAllSlotEvent` | 1651-1688 | Trả slot còn hiệu lực (`date_start_from >= today`) + **100 bạn bè đầu tiên** chưa block (`limit 100` hardcode `:1664`) | — |
| `ajaxGetHistoryBookingApp` | 1690-1792 | ⚠ **DEAD CODE — không có route nào trỏ tới** (đã grep toàn `routes/web.php`). Endpoint thật đang chạy là `MobileEventBookingController@ajaxGetHistoryBookingApp:2509` (`routes/web.php:3755` → EP-79). Nội dung: lịch sử đặt chỗ của 1 LINE user; tính cờ `cancel` theo `date/time_deadline_change_cancel` | — (không được gọi) |
| `refundMoneyBookingEvent` | 1794-1902 | **Hoàn tiền** — xem mục 7 | Gọi Stripe/UnivaPay API; update `b_user_booking.status_payment/refund_date/reason_refund`; ghi `b_user_booking_history` |

### 1.2 `BookingEventDayController`
`app/Http/Controllers/Basic/BookingEventDayController.php` — 6.533 dòng.

**Dependency injection** (`:74-85`): `TemplateService`, `MessageService`, `BotRepositoryInterface`, `HelperService`.

| Method | Line | Logic chính | Side effects |
|---|---|---|---|
| `create` / `edit` | 1089-1165 | Render wizard `basic.booking_event_day.add_v2`. Nạp `Category` (kind = template), `Scenario`, `Tag`, `Events::getListEventSAfterToDay()`, `RichMenus` (status_rich = 1), `StripBot`, `bots.plan_type` | — |
| `getCreateEventDayLimitError` (private) | 1173-1189 | **Kiểm tra giới hạn gói khi tạo event** — xem Business Rule BR-01 | — |
| `saveSettingBasicEvent` | 1191-1320 | Lưu `b_event_detail` + `b_setting_basic_event`. `type = 'info'` → lưu nhóm thông tin; ngược lại → lưu nhóm action | Insert/update `b_event_detail`, `b_setting_basic_event`; gọi `saveInfoDefault()` |
| `saveInfoDefault` | 146-203 | Nếu event chưa có `b_info_setting` → tạo 2 field mặc định 「お名前」(`friend_info_id = -1`) và 「メールアドレス」(`friend_info_id = -3`), đều `is_require = 1`. Nếu chưa có `b_setting_basic_event` → tạo với default (`max_number=0`, `limit_people=1`, `min_people=1`, `unit_booking='人'`, `is_hide_remain=1`…) | Insert `b_info_setting`, `b_setting_basic_event` |
| `saveSettingEvent` | 1321-1431 | Lưu step 1. **Upload ảnh**: lưu vào `public/{FOLDER_MEDIA}media/images/{userId}/{botId}/booking/`, dùng `Intervention\ImageManager` driver **imagick**, `orientate()`, sau đó `resizeImageToMaxSize(..., 2048)` | Ghi file ảnh lên disk; update `b_event_detail.image` |
| `saveSettingStep2` | 511-614 | Lưu điều khoản + danh sách field form. Field có `id` → chỉ update `order_index`; field mới → `BInfoSetting::create()` với `is_mapping_info = 1` (hardcode `:576`) | Insert/update `b_info_setting` |
| `saveSettingStep3` | 615-679 | Lưu cấu hình màn hình xác nhận / hoàn tất | Update `b_event_detail` |
| `saveSettingBill4` | 681-742 | Lưu cấu hình thanh toán (`type_system_bill`, `flag_environment`, `is_auto_bill`, `content_term_bill`) | Update `b_event_detail` |
| `saveAndPreviewTermBill` | 743-799 | Lưu + trả `event_id` đã Hashids-encode để mở trang preview | Update `b_event_detail` |
| `changeMappingInfo` | 482-509 | Toggle `is_mapping_info` (`type_save = 'mapping'`) hoặc `is_show` (`type_save = 'show'`) của `b_info_setting` | Update `b_info_setting` |
| `deleteSettingInfo` | 800-822 | Xoá field form theo `id` + `event_detail_id` + `bot_id` | Xoá `b_info_setting` |
| `addDateSlot` | 6289-6359 | Thêm các ngày tổ chức từ `dates_picker` (JSON array). Bỏ qua ngày đã tồn tại | Insert `b_setting_date_event` |
| `initDateSlot` / `initSlotOfDate` / `initSlotData` / `initPlanData` | 6360-6402, 5444-5486, 5192-5231 | Nạp dữ liệu ngày/slot/plan + resolve chi tiết action qua `getDetailListAction()` (`:314-334`) | — |
| `saveSettingSlotEvent` | 1503-1645 | **Lưu slot** — tạo/update `b_slot`. Suy diễn `date_deadline`, `date_end_change_request`, `date_end_cancel` từ `date_start - duration_*` | Insert/update `b_slot`; **tạo `event_times`** + gọi `createEventStepTime()` khi có `event_id` (remind) |
| `saveSettingSlot` | 5535-5606 | Lưu cấu hình bổ sung slot (remind, `is_limit_people`, action). **Có validation** | Update `b_slot`; tạo `event_times`, `event_step_time` |
| `saveSettingPlan` | 5310-5389 | Lưu plan. `price` bỏ dấu `.` trước khi lưu (`:5334`). `order = max(order) + 1` khi tạo | Insert/update `b_plan_slot` |
| `saveAllSlotPlanDay` | 6404-6493 | Lưu hàng loạt. Khi `date_start` đổi → **recompute toàn bộ** `date_start_from` của slot và các `date_end_*` của slot/plan; tạo `event_times` mới + `createEventStepTime()` cho slot có remind | Update `b_slot`, `b_plan_slot`, `b_setting_date_event`; insert `event_times`, `event_step_time` |
| `ajaxSaveDurationSettingDate` | 6494-6530 | Lưu thời điểm mở bán slot: `date_show_slot = date_start - duration`, `time_show_slot`. Nếu thiếu duration hoặc time → set cả 3 field về `null` | Update `b_setting_date_event` |
| `copyBookingEvent` / `copyDateEvent` / `copySlot` / `copyPlan` / `cloneAction` | 5608-6186 | Copy sâu event/ngày/slot/plan kèm clone action | Insert nhiều bảng |
| `deleteSlot` / `deleteDateSlot` / `deletePlan` / `deleteMultipleSlot` | 5001-5114, 6187-6237, 5391-5411 | Xoá slot/ngày/plan | Xoá `b_slot`, `b_plan_slot`, `b_user_booking`, action |
| `allBooking` / `ajaxAllBooking` / `ajaxAllBookingOfDay` / `bookingSlotDay` / `ajaxBookingSlotDay` / `detailBooking` / `ajaxBookingDetail` | 1803-2632 | Danh sách / chi tiết đặt chỗ, filter theo tab, keyword, tháng, trạng thái | — |
| `saveAdminBooking` | 2633-2871 | **Admin đặt hộ** — xem mục 6.1 | Nhiều (xem mục 6.1) |
| `saveUserBooking` | 2873-3089 | Booking từ phía LINE user (luồng cũ) | Nhiều |
| `saveActionBooking` | 3123-3891 | **Duyệt / từ chối / huỷ / đổi đặt chỗ** — xem mục 6.2 | Nhiều (bao gồm charge tiền) |
| `addActionRemind` | 4169-4293 | Đăng ký user vào remind event — xem mục 8 | Insert `user_event`, `event_step_time`, `messages_v2s` |
| `cancelUserBooking` / `updateUserBooking` | 4294-4604 | Huỷ / cập nhật đặt chỗ | Update `b_user_booking`, action |
| `exportCSV` / `exportCSVSlotOrPlan` / `downloadCsv` | 4620-4871 | Export CSV bằng `Maatwebsite\Excel` (`ExportAllSlotBooking`, `ListBookedExport`) | Ghi file CSV |
| `getFriendInfoEvent` / `getInfoFriendLineUser` | 6006-6086, 4872-5000 | Lấy thông tin bạn bè để prefill form đặt chỗ | — |
| `previewTermBill` / `previewTermBillMobile` / `previewEventInfo` | 6262-6288 | Preview. `previewTermBill*` decode `id` bằng `Hashids::decode()` | — |
| ⚠ `ajaxAddBooking` | **KHÔNG TỒN TẠI** | Route `POST /basic/ajaxAddBooking` (`routes/web.php:1178`) trỏ tới method không có trong controller (grep toàn `app/` không tìm thấy). **Route chết** | — |

### 1.3 `MobileEventBookingController` (public — LINE User)
`app/Http/Controllers/Basic/MobileEventBookingController.php`.

| Method | Line | Vai trò |
|---|---|---|
| `index` | 98-206 | Render trang LIFF đặt chỗ (`hash_event_id` = Hashids) |
| `getSlots` | 207-455 | Trả slot/plan còn chỗ theo cấu hình hiển thị (`is_show_slot_expire`, `is_show_slot_over`, `is_hide_remain`) |
| `createCustomerIdUnivapay` | 456-516 | Tạo customer id UnivaPay |
| `getInfoCardPayment` | 517-597 | Lấy thẻ đã lưu |
| `payment` | 706-1493 | **Đặt chỗ + thanh toán** — xem mục 7 |
| `deleteBookingConfirmFail` / `rollbackChangeBookingConfirmFail` | 1511-1559 | Dọn dẹp khi thanh toán fail |
| `cancelUserBooking` | 1572-1711 | LINE User huỷ đặt chỗ |
| `changeBooking` | 1712-2508 | LINE User đổi đặt chỗ (tạo booking mới liên kết `update_to`) |
| `ajaxGetHistoryBookingApp` | 2509-… | Lịch sử đặt chỗ của LINE User — **endpoint THẬT** (EP-79, `POST /mobile/get-history-booking-app`, `routes/web.php:3755`). Bản trùng tên ở `BookingEventDayManagementController:1690` là **dead code** |
| `updateSlotPurchased` / `countUserPeopleSlot` / `countRemainlLimitPlan` | 1560-1571, 2744-2762 | Đếm lại số chỗ đã dùng (recompute thay vì increment) |
| `addActionRemind` | 2628-2743 | Bản sao logic remind (duplicate với `BookingEventDayController::addActionRemind`) |

### 1.4 `WebhookUnivapayControler`
`app/Http/Controllers/WebhookUnivapayControler.php:11-41` — nhận webhook `charge_finished`, lọc theo `metadata.module`, dispatch `HandleWebhookUnivapay` job. **Không xác thực chữ ký**.

---

## 2. Models Eloquent

| Model | File | Table | Ghi chú |
|---|---|---|---|
| `BEventDetail` | `app/BEventDetail.php` | `b_event_detail` | `$guarded = []`, timestamps. `slots()` = hasMany `BSlot` (`event_detail_id`). Static: `getEventById($id)` (scope theo `getBotId()`, eager `slots`), `getNameById($id,$botId)` |
| `BSettingBasicEvent` | `app/BSettingBasicEvent.php` | `b_setting_basic_event` | Cấu hình chung + 3 nhóm action của event |
| `BSettingDateEvent` | `app/BSettingDateEvent.php` | `b_setting_date_event` | 1 ngày tổ chức. `slots()` = hasMany `BSlot` |
| `BSlot` | `app/BSlot.php` | `b_slot` | `$guarded = ['is_event_many_date']`, `$appends = ['is_event_many_date']`. **Accessor** `getIsEventManyDateAttribute()` (`:17-26`): trả `'many'` nếu `date_start_to > date_start_from`, ngược lại `'one'`. Relations: `event_detail()` belongsTo, `plans()` hasMany `PlanSlot`, `bookings()` hasMany `BBooking`. Static `getSlotById($id)` |
| `PlanSlot` | `app/PlanSlot.php` | `b_plan_slot` | Relations tới các action (`action_booking_success`, `action_at_time_cancel`, `action_booking_change`, `action_booking_approve`, `action_booking_denial`), `booking()`. Static `getPlanByIds()` |
| `BBooking` | `app/BBooking.php` | `b_user_booking` | Relations: `lineUser()`, `plan()`, `slot()`. **Constants `status_webhook`**: `STATUS_WEBHOOK_UNPROCESSED=0`, `PROCESSED=1`, `ERROR=2`, `TIMEOUT=3`, `TIMEOUT_WEBHOOK=4`, `UNPROCESSED_CHANGE=5`, `TIMEOUT_CHANGE=6`, `TIMEOUT_WEBHOOK_CHANGE=7` (`:15-22`) |
| `BInfoSetting` | `app/BInfoSetting.php` | `b_info_setting` | Field form thu thập thông tin |
| `BUserBookingHistory` | `app/Models/BUserBookingHistory.php` | `b_user_booking_history` | `$fillable = [bot_id, b_user_booking_id, status, reason, operator_id, operator_name]`. **Constants status**: `ADMIN_APPROVE=1`, `DENY=2`, `REQUEST_BOOKING=3`, `CANCEL=4`, `BOOKING_NEW=5`, `REQUEST_CHANGE=6`, `REQUEST_CANCEL=7`, `CHANGE_BOOKING=8` |
| `DetailActionSlot` | `app/DetailActionSlot.php` | `b_detail_action_slot` | Chi tiết action gắn với slot/plan |
| `EventTimes` | `app/EventTimes.php` | `event_times` | Mốc thời gian remind |
| `EventStepTime` | `app/EventStepTime.php` | `event_step_time` | **Bảng hàng đợi remind cho Spring Boot** |
| `UserEvent` | `app/UserEvent.php` | `user_event` | Đăng ký user vào remind |
| `StripBot` | `app/StripBot.php` | `s_strip_bot` | Key Stripe/UnivaPay theo bot (`strip_secret_test_key`, `strip_secret_live_key`). `$timestamps = false` |
| `SyncElasticsearch` | `app/SyncElasticsearch.php` | `sync_elasticsearch` | **Bảng hàng đợi đồng bộ ES**. `insertElasticsearch($data)` chỉ chạy khi `env('API_KEY_ES')` |
| `ActionLineUser` | `app/ActionLineUser.php` | `action_lineuser` | Log action đã gửi tới LINE user |
| `SendRandomMessage` | `app/SendRandomMessage.php` | `send_random_messages` | Hàng đợi gửi tin nhắn ngẫu nhiên |

Model dùng chung: `Category` (kind = 21 cho event booking v1), `Scenario`, `Tag`, `RichMenus`, `Events`, `EventStep`, `LineUser`, `BotLineUser`, `Conversation`, `FriendInformationSetting`, `FriendInformationValue`, `Bots`, `BotContracts`, `BackupHistory`, `MessagesV2`, `MessageError`, `Affiliaters`, `AffResult`, `BotSettingAff`.

---

## 3. Services / Repositories / Helpers

| Thành phần | File | Vai trò |
|---|---|---|
| `TemplateService` | `app/Services/TemplateService.php` | `mergeListTemplate($templateIds, $lineUser, $bot)` — build nội dung tin nhắn remind |
| `MessageService` | `app/Services/MessageService.php` | `createMessageTypeV2(...)` — tạo bản ghi `messages_v2s` và đẩy gửi LINE |
| `BotRepositoryInterface` | `app/Contracts/Repositories/BotRepositoryInterface.php` | `updateBot($id, ['free_send_count' => ...])` |
| `HelperService` | `app/Services/HelperService.php` | Tiện ích chung |
| `MobileNotifyService` | `app/Services/Notify/MobileNotifyService.php` | `insertNotifyEventBooking($booking, $action, $bookingIdOld?)`, `insertNotifyAffFee(...)` — push notify app mobile |
| `EventBookingService` | `app/Services/EventBooking/EventBookingService.php` | **Xử lý callback thanh toán**: `handleOrderCallback()` (`:169`), `callbackChangeBooking()` (`:526`), `callbackChangeStatus()` (`:920`), `addActionRemind()` (`:1054`), `checkStatusProcessCallback($bookingId, $retryNumber = 25)` (`:1171`), `getBookingTimeout()` (`:1237`), `updateSlotPurchased()`, `countUserPeopleSlot()`, `countRemainlLimitPlan()` |
| `StripePayment` | `app/Helpers/StripePayment.php` | `setApiKey()`, `refundMoney()`, `autoPaymentIntents()`, `chargeMoney()` |
| `UnivapayPayment` | `app/Helpers/UnivapayPayment.php` | `chargeMoneyUnivapaySale()`, `getChargesSale()`, `getInfoTokenSale()`, `cancelCharge()`, `refundMoney()`, `getRefundMoney()`, `getMessageErrorUnivapay()` |

### Helper functions (`app/Helpers/functions.php`)

| Hàm | Line | Vai trò |
|---|---|---|
| `getBotId()` | — | Lấy bot_id hiện tại từ session |
| `addLogUserAction($name)` | — | Ghi log thao tác người dùng — gọi ở **hầu hết** action của 2 controller |
| `checkValueDuration($value)` | 9945 | Kiểm tra duration hợp lệ (dùng để quyết định set `date_end_*` hay `null`) |
| `createEventStepTime($eventId, $eventTimeId, $botId?)` | 9463-9506 | **INSERT/UPDATE bảng `event_step_time`** — xem mục 8 |
| `makeMessageStartRemind($conversationId, $botId, $type, $remindName, $eventTime, $isStop, $source)` | 9525 | Tạo bản ghi message bắt đầu remind |
| `sendAction($action_id, $lineUserId, $botId, $bookingId, $typeStartScenario, ...)` | 7903-8643 | **Thực thi action**: gắn/gỡ tag (`tag_line_user`), chạy scenario (xoá `scenario_step_time` status=0), đăng ký remind (`user_event`), gửi tin nhắn, `SendRandomMessage::create()` (`send_random_messages`), `ActionLineUser::create()` (`action_lineuser`) |
| `sendActionBookingV1($status, $bookingId, $statusOld, $type_request, $isSendAction)` | 5861-… | **Bộ máy chuyển trạng thái booking v2** — xem mục 6.3 |
| `recordFriendInfoHistory(...)` | 11676 | Ghi lịch sử thay đổi thông tin bạn bè |
| `resizeImageToMaxSize($src, $dst, $max)` | — | Resize ảnh upload |
| `updateMessageSendCount($botId, $date, $n)` | — | Cộng dồn số tin đã gửi |
| `getRouterBotInvite()` | — | Danh sách route Staff được phép truy cập |

---

## 4. Validation

**Không dùng FormRequest** — toàn bộ validate inline bằng `Validator::make()` trong controller. Nhiều endpoint **hoàn toàn không validate**.

| Hàm | File:line | Được gọi bởi | Rules |
|---|---|---|---|
| `validateFormSaveSlotOfEvent($request)` | `BookingEventDayController.php:1718-1779` | `saveSettingSlot` (`:5540`) | `date_start_from: required`; `address: max:255`; `date_start_to: required` (khi `type_event=1`); `time_start: required` / `time_end: required` (khi `type_event≠1`, `is_hide_time_end=0`); `date_deadline: required`; `time_deadline: required`; `address_url: regex URL`. **after()**: `time_start > time_end` → lỗi; `date_start_from > date_start_to` → lỗi; `quantity == 0` → 「定員には１以上入力してください」 |
| `validateFormBooking($request)` | `BookingEventDayManagementController.php:909` | `ajaxBookingSave` (`:806`) | Validate form đặt chỗ |
| `validateFormSaveSlotOfEvent($slot)` | `BookingEventDayManagementController.php:1198` | `updateSlot` | Validate slot khi update |
| `validateFormSettingEvent($request)` | `BookingEventDayController.php:1667-1716` | **KHÔNG được gọi** (dead code) | `title: required\|max:20`, `line_title: required\|max:50`, `line_explain: required\|max:50`, `content: max:20000`, `address: max:255`, `url_address: regex` |
| `validateFormSettingDefault($request)` | `BookingEventDayController.php:1647-1665` | `saveSettingDefault` | `name.*: required` → 「プラン名は必須です。」 |

> **Rủi ro**: `saveSettingBasicEvent`, `saveSettingEvent`, `saveSettingStep2/3`, `saveSettingBill4`, `saveSettingSlotEvent`, `saveSettingPlan`, `saveAdminBooking`, `saveActionBooking` **không validate** input. Ràng buộc độ dài/bắt buộc chỉ ở client-side. **Độ tin cậy: Cao**.

---

## 5. Events / Listeners / Queued Jobs

### 5.1 Laravel Queue Jobs

| Job | File | Dispatch từ | Nhiệm vụ |
|---|---|---|---|
| `HandleWebhookUnivapay` | `app/Jobs/HandleWebhookUnivapay.php` | `WebhookUnivapayControler@webhook:34` | Route theo `metadata.module`: `event-booking` → `EventBookingService::handleOrderCallback()`; `event_booking_change` → `EventBookingService::callbackChangeBooking()` |

Không có Laravel Event/Listener nào riêng cho tính năng này.

### 5.2 ⚠ Bảng hàng đợi cho Spring Boot (đầu vào cho bước `job-analyzer`)

| Bảng | Ghi bởi (file:line) | Nội dung / ý nghĩa |
|---|---|---|
| **`event_step_time`** | `functions.php:9497` (INSERT) / `:9499` (UPDATE) qua `createEventStepTime()`.<br>Gọi từ: `BookingEventDayController@saveSettingSlotEvent:1628`, `@saveSettingSlot:5598`, `@saveAllSlotPlanDay:6477` | **Hàng đợi remind**. Mỗi bản ghi = 1 tin nhắn remind cần gửi: `{event_id, event_time_id, event_step_id, bot_id, sent_date_time, status: 0}`. Chỉ insert khi `sent_date_time > now()`. Spring Boot quét `status = 0` và `sent_date_time <= now()` để gửi. **Độ tin cậy: Cao** |
| **`event_times`** | `BookingEventDayController@saveSettingSlotEvent:1623`, `@saveSettingSlot:5596`, `@saveAllSlotPlanDay:6474` | Mốc thời gian sự kiện: `{event_id, bot_id, event_date, event_start_time}`. `b_slot.remind_id` trỏ tới bảng này |
| **`user_event`** | INSERT: `BookingEventDayController@addActionRemind:4211`, `functions.php:8260` (trong `sendAction`), `MobileEventBookingController@addActionRemind`, `EventBookingService@addActionRemind:1054`.<br>DELETE: `@addActionRemind:4195`, `sendActionBookingV1` (`functions.php:5951`, `:5988`) | **Đăng ký LINE user vào remind**: `{event_id, bot_id, event_time_id, user_id, register_date_time}`. Xoá khi user không còn booking active (`status ∈ {1,5}`) trên `event_time_id` đó |
| **`sync_elasticsearch`** | `BookingEventDayController@saveAdminBooking:2708` (`SyncElasticsearch::insertElasticsearch`), và tương ứng trong `MobileEventBookingController@payment` | **Hàng đợi đồng bộ ES**: `{type: config('sns-line.type_sync.update'), line_user_id, bot_id, data_sync: json}` — khi `view_name` của bạn bè bị thay đổi qua form đặt chỗ. Chỉ ghi khi `env('API_KEY_ES')` được set |
| **`messages_v2s`** | Qua `MessageService::createMessageTypeV2()` — gọi từ `@addActionRemind:4280` | Lịch sử/hàng đợi tin nhắn LINE (remind step đầu tiên `before_day = -1`). ⚠ Tên bảng thật có **`s`** cuối — `messages_v2s` (khớp `job-spec.md` §2.7 `@Table(name = "messages_v2s")`) |
| **`send_random_messages`** | `functions.php` trong `sendAction` (`SendRandomMessage::create`) | Hàng đợi gửi tin nhắn ngẫu nhiên (khi action cấu hình random message) |
| **`action_lineuser`** | `functions.php` trong `sendAction` (`ActionLineUser::create`) | Log action đã áp dụng cho LINE user |
| **`scenario_step_time`** | `functions.php` trong `sendAction` — **DELETE** `where status = 0` | Huỷ các step scenario đang chờ khi action yêu cầu dừng scenario |
| **`tag_line_user`** | `functions.php` trong `sendAction` — INSERT/DELETE | Gắn/gỡ tag bạn bè theo action |

> **KHÔNG** tìm thấy ghi vào `action_schedules`, `csv_management`, `broadcast`, `callback_event`, `action_line_users` (số nhiều) trong luồng tính năng này. Export CSV dùng `Maatwebsite\Excel` ghi file trực tiếp (đồng bộ), **không** qua bảng `csv_management`. **Độ tin cậy: Cao** (grep 2 controller).

---

## 6. Luồng nghiệp vụ đặt chỗ

### 6.1 Admin đặt hộ — `saveAdminBooking` (`:2633-2871`)
1. Tạo `b_user_booking` với `status = 5` (booking), `booking_from = 1`, `event_time_id = slot.remind_id` (`:2667-2684`).
2. Ghi `b_user_booking_history` với `reason = '予約リクエスト'` (khi status = 3) hoặc `'手動予約追加'` (`:2686-2687`).
3. Với mỗi field `form_info` → đồng bộ ngược vào hồ sơ bạn bè theo `friend_info_id` (`:2688-2795`):
   - `-1` → `line_user.view_name` + **insert `sync_elasticsearch`**
   - `-2` → `line_user.phone_number`; `-3` → `email`; `-4` → `age`; `-6` → `province`
   - Khác → `friend_information_value` (insert/update) + tăng `friend_information_setting.total_user_has_value`
   - Luôn gọi `recordFriendInfoHistory(..., '8001')`
   - Nếu `type_data == 1` và option có `action_id` và `friend_info.action == null` → `sendAction(..., '6004')`
4. `addActionRemind($slotId, $bookingId, null, 'admin_booking')` (`:2797`).
5. **Tăng số chỗ đã dùng** (`:2798-2804`): `b_slot.use_people += quantity`; nếu có plan → `b_plan_slot.remain_limit += quantity` (⚠ tên cột `remain_limit` nhưng semantics là **đã dùng**, không phải "còn lại").
6. Nếu `action_before_booking == 0` → gửi action LINE (`:2806-2838`): chọn `action_id_booking_approve_v1` từ **plan** nếu `using_action_slot_booking_v1 == 1`, ngược lại từ **slot**. `sendAction(..., trigger '8001')`.
7. `MobileNotifyService::insertNotifyEventBooking($booking, 'autoApprove')` (`:2860-2861`).

### 6.2 Duyệt / từ chối / huỷ / đổi — `saveActionBooking` (`:3123-3891`)
1. **Chặn khi đang thanh toán** (`:3149-3158`): `status_webhook ∈ {UNPROCESSED, TIMEOUT, TIMEOUT_WEBHOOK, UNPROCESSED_CHANGE, TIMEOUT_CHANGE, TIMEOUT_WEBHOOK_CHANGE}` → trả `payment_failed: true`.
2. **Xử lý cặp booking khi đổi chỗ** (`status == 6`, `:3161-3193`): hệ thống tạo **2 bản ghi** `b_user_booking` liên kết bằng cột `update_to` (bản mới trỏ về bản cũ). Code phân biệt "đang thao tác trên bản cũ" (`update_to` null) hay "bản mới".
3. **Tính chỗ còn lại** (`:3216-3236`): nếu plan có `using_max_slot = 1` → dùng `slot.number_people - slot.use_people`; ngược lại nếu slot có `number_people` → dùng slot, không thì `plan.limit - plan.remain_limit`.
4. **Cảnh báo vượt định員** (`:3237-3255`): trả `admin_confirm: 1` + message 「予約枠を超えています。承認しますか？」 nếu chưa có `approveAny`.
5. Update `b_user_booking.status` + ghi `b_user_booking_history` (`STATUS_DENY` hoặc `STATUS_CHANGE_BOOKING`) (`:3312-3328`).
6. **Thu tiền khi duyệt** (`:3391-3510`, tức `if ($status == 1 && $bPlan->price > 0 && $checkHasPayment)`): Stripe `autoPaymentIntents()` hoặc UnivaPay `chargeMoneyUnivapaySale()` → xác nhận qua `getChargesSale()` → nếu fail thì `cancelCharge()`.
7. `sendActionBookingV1($status, $bookingId, $statusOld, $type_request)` (`:3553`) hoặc `sendAction(..., '8005')` (`:3584`).
8. **Recompute số chỗ** (`:3606-3637`): `b_slot.use_people` và `b_plan_slot.remain_limit` được **tính lại** (`update`, không phải increment) cho cả slot/plan cũ và mới.
9. Xử lý **hoa hồng affiliate** (`:3670-3712`): tạo `AffResult` + `MobileNotifyService::insertNotifyAffFee()`.
10. `MobileNotifyService::insertNotifyEventBooking($bookingNotify, $actionNotify, $bookingIdOldNotify)` (`:3736`).

### 6.3 `sendActionBookingV1` (`functions.php:5861+`) — bộ máy trạng thái
- Chọn `action_id` theo `using_action_slot_change_request`: `1` → ưu tiên action của **plan**, fallback slot; `0` → chỉ action của **slot**.
- **Khi `statusOld == 6` (request change)**:
  - `type_request` có giá trị (từ chối đổi): giữ booking cũ (`status = last_status`, `update_to = null`), **xoá booking mới**, chuyển `b_user_booking_history` sang booking cũ, action = `action_id_change_request_cancel_request_v1`, trigger `8008`.
  - `type_request` null (duyệt đổi): **xoá booking cũ**, booking mới `status = 1`, `update_to = null`, chuyển history sang booking mới, action = `action_id_change_request_approve_request_v1`, trigger `8007`. Đồng thời **xoá `user_event`** của `event_time_id` cũ nếu user không còn booking active (`status ∈ {1,5}`) trên mốc đó.
- Trigger types dùng trong tính năng: `8001` (đặt chỗ thành công), `8002` (yêu cầu đặt chỗ), `8003` (duyệt đặt chỗ), `8005`, `8006` (yêu cầu đổi), `8007` (duyệt đổi), `8008` (từ chối đổi), `6004` (action từ friend info).

---

## 7. Thanh toán & hoàn tiền

### 7.1 Cấu hình (trên `b_event_detail`)
- `type_system_bill`: `1` = **Stripe**, `2` = **UnivaPay** (`BookingEventDayManagementController:1816-1848`).
- `flag_environment`: `0` = test, `1` = live → chọn `s_strip_bot.strip_secret_test_key` / `strip_secret_live_key` (`:1822-1826`).
- `is_auto_bill`: tự động thu tiền.
- `content_term_bill`: nội dung điều khoản thanh toán.

### 7.2 Luồng thanh toán LINE User (`MobileEventBookingController@payment`)
1. Tạo `b_user_booking` với `status_webhook = STATUS_WEBHOOK_UNPROCESSED (0)`.
2. Gọi cổng thanh toán với **metadata `module = 'event-booking'`** (hoặc `'event_booking_change'` khi đổi booking).
3. Poll `EventBookingService::checkStatusProcessCallback($bookingId, 25)` chờ webhook cập nhật.
4. Quá hạn → set `status_webhook = TIMEOUT (3)` hoặc `TIMEOUT_WEBHOOK (4)`.
5. Webhook `charge_finished` → `HandleWebhookUnivapay` job → `EventBookingService::handleOrderCallback()` → cập nhật `status_webhook = PROCESSED (1)`, `status` booking, `use_people`, gửi action, remind.
6. Nếu FE báo fail → `deleteBookingConfirmFail` / `rollbackChangeBookingConfirmFail`.

### 7.3 Hoàn tiền (`refundMoneyBookingEvent`)
- `reason_refund = 1` → gọi API hoàn tiền của cổng (Stripe `refundMoney($strip_charge_id)` / UnivaPay `refundMoney($univapay_charge_id, $amount)`).
- `reason_refund ≠ 1` → **chỉ đánh dấu trong DB**, không gọi cổng (hoàn tiền ngoài hệ thống).
- Kết quả: `b_user_booking.status_payment = 2`, `refund_date = now()`, `reason_refund`; UnivaPay còn set `univapay_charge_id = null`.
- Luôn ghi `b_user_booking_history` với `reason = '¥{amount}の返金（決済システムから|エルメから）'` + `operator_id/operator_name` từ `Auth`.

---

## 8. Remind (nhắc lịch) — cầu nối sang Spring Boot

`BookingEventDayController@addActionRemind($slotId, $bookingId, $bookingOld, $type_request)` (`:4169-4293`):
1. Lấy `slot.remind_id` → `event_times` → `events`.
2. Nếu có `$bookingOld`: đếm booking active (`status ∈ {1,5}`) của user trên `event_time_id` cũ; nếu `== 0` → **DELETE `user_event`** (`:4189-4197`).
3. Lấy `conversation` (chưa block). Nếu `user_event` chưa tồn tại → **INSERT `user_event`** `{event_id, bot_id, event_time_id, user_id, register_date_time}` (`:4202-4212`).
4. Xác định `actionFrom.trigger_type` theo `$type_request` (`:4217-4249`):
   | `type_request` | trigger_type |
   |---|---|
   | `user_booking_auto_approve`, `admin_booking` | `8001` |
   | `user_request_booking` | `8002` |
   | `approve_booking` | `8003` |
   | `request_change_booking` | `8006` |
   | `approve_change_booking` | `8007` |
   | (mặc định) | `15001` |
5. `makeMessageStartRemind($conversationId, $botId, '8001', $event->event_name, $eventTimes, false, $source)` (`:4256`).
6. Gửi **step đầu tiên** của remind (`event_step.before_day = -1`) ngay lập tức qua `TemplateService::mergeListTemplate()` + `MessageService::createMessageTypeV2()` (chunk 5 template) (`:4257-4288`). Thành công → `bots.free_send_count += 1` và `updateMessageSendCount()`.
7. Các step còn lại (`before_day > -1`) được đưa vào `event_step_time` bởi `createEventStepTime()` **khi slot được lưu** (không phải khi booking) — chỉ insert nếu `sent_date_time > now()` (`functions.php:9486`).

---

## 9. Authorization

- **Không có Policy / Gate** cho tính năng này (grep `app/Policies` không có class liên quan). **Độ tin cậy: Cao**.
- Phân quyền dựa hoàn toàn vào **middleware `basic_access`** (`app/Http/Middleware/BasicAccess.php`):
  - Yêu cầu `Auth::check()` và `role ∈ {-1, 0, 1, 2}` (`:31`).
  - Nếu bot hiện tại **không thuộc** `Auth::id()` → session `is_bot_invite = true` → lấy whitelist route qua `getRouterBotInvite()`; route không nằm trong whitelist → redirect + lỗi 「この権限は許可されていません。」 (`:41-50`). Đây là cơ chế phân quyền **Staff**.
  - `checkExistsUserStaffBot()` + kiểm tra `UserStaffBot` theo `bot_id` + `user_invite_id`.
- **Tất cả endpoint AJAX (`/ajax/...`) chỉ có `check_login` + `check_remember_token`** → **không kiểm tra permission Staff, không kiểm tra `is_expire`**. Staff bị chặn ở trang HTML vẫn có thể gọi trực tiếp API AJAX. **Rủi ro bảo mật — Độ tin cậy: Cao** (`routes/web.php:2454`).
- **Cách ly dữ liệu theo bot**: hầu hết query đều `where('bot_id', getBotId())`. Ngoại lệ đáng chú ý:
  - `refundMoneyBookingEvent` nhận `bot_id` **từ request** thay vì `getBotId()` (`BookingEventDayManagementController:1797`) — có kiểm tra `BBooking::where('bot_id', $botId)` nhưng `$botId` do client cung cấp → **có thể refund booking của bot khác**. Tuy nhiên dòng `:1850` lại dùng `getBotId()` để lấy key UnivaPay → không nhất quán. **Độ tin cậy: Cao** (đọc trực tiếp code).
  - `saveActionBooking`, `deleteMultipleSlot`, `saveSettingPlan` không luôn scope `bot_id` khi update.
  - `deleteMultipleSlot` (`:5391-5411`) dùng biến `$slotId` **chưa được khai báo** ở dòng `:5402` → **lỗi runtime** (`BBooking::where('slot_id', $slotId)`). **Độ tin cậy: Cao**.

---

## 10. Business Rules tổng hợp

| ID | Quy tắc | Nguồn (file:line) | Tin cậy |
|---|---|---|---|
| **BR-01** | **Giới hạn số sự kiện theo gói**: khi `bots.flag_contract_new = 1` — gói `free` hoặc `bots.plan_type = 2` → tối đa **2** sự kiện (`type_event_new = 1`), message 「現在のプランは利用できない機能です。アップグレードが必要になります。」; gói `standard` → tối đa **10**, message 「スタンダードプランの上限に達しています。制限を解除する場合は、プロプランへの変更が必要になります。」. Gói `pro` không giới hạn. `contract_type` lấy từ `bot_contracts` join `bot_slots` | `BookingEventDayController.php:1173-1189`; mirror ở `BookingEventDayManagementController.php:443-453` (trả `isAdd`/`msg_plan` cho FE) | Cao |
| **BR-02** | Giới hạn BR-01 được **re-check ở MỌI step tạo** của wizard (basic / step2 / step3 / bill4 / previewTermBill / addDateSlot) để chặn bypass mở link trực tiếp hoặc mở nhiều tab (ticket `#37292`) | `:1269-1275`, `:548-554`, `:649-655`, `:712-718`, `:769-775`, `:6315-6321` | Cao |
| **BR-03** | **Chặn thao tác khi bot đang backup/restore**: nếu tồn tại `BackupHistory` với `code = bot.transfer_code` và `status ∈ {0,1}` → trả HTTP 500 + `MESSAGE_NOTIFY_BACKUP`. Áp dụng cho mọi action ghi | `:517-523`, `:621-627`, `:686-692`, `:748-754`, `:1203-1209`, `:1328-1334`, `:1510-1516`, `:5317-5323`, `:6295-6301`; Management: `:139-145`, `:178-184`, `:246-252`, `:305-311`, `:380-385`, `:618-625`, `:644-651` | Cao |
| **BR-04** | **Trạng thái đặt chỗ** (`b_user_booking.status`): `1` = 承認 (approve), `2` = 否認 (deny), `3` = 承認待ち (pending), `4` = キャンセル (cancel), `5` = 予約済み (booking — khi slot không cần duyệt), `6` = 変更リクエスト (request change), `7` = キャンセルリクエスト (request cancel) | `config/sns-line.php:398-407` | Cao |
| **BR-05** | **Booking "active"** (được tính vào định員) = `status ∈ {1, 5}` hoặc `status = 6 AND update_to IS NULL` hoặc `status = 7` | `BookingEventDayManagementController.php:527-532`, `:708-714` | Cao |
| **BR-06** | **Booking "chờ xử lý"** (`countRequestSlot` / `countRequestPlan`) = `status ∈ {3, 6, 7}` | `BookingEventDayManagementController.php:727-733`, `:772-778` | Cao |
| **BR-07** | **Định員 (capacity)**: `b_slot.number_people` = định員 của slot; `b_plan_slot.limit` = định員 của plan. Nếu plan có `using_max_slot = 1` → plan dùng chung định員 của slot. Nếu `number_people` = NULL → **không giới hạn** (hiển thị `-`) | `BookingEventDayManagementController.php:490-517`; `BookingEventDayController.php:3216-3236` | Cao |
| **BR-08** | **Số chỗ đã dùng**: `b_slot.use_people` và `b_plan_slot.remain_limit` (⚠ tên gây hiểu nhầm — thực chất là **số đã dùng**, không phải còn lại). `saveAdminBooking` dùng `increment`; `saveActionBooking` **recompute** lại từ tổng `quantity` các booking active | `:2798-2804` (increment); `:3606-3637` (recompute) | Cao |
| **BR-09** | **Vượt định員 khi duyệt** → không chặn cứng, trả `admin_confirm: 1` + 「予約枠を超えています。承認しますか？」 để admin xác nhận, gọi lại với `approveAny = true` sẽ bỏ qua | `:3237-3255` | Cao |
| **BR-10** | **Không thao tác được khi đang xử lý thanh toán**: `status_webhook ∈ {0,3,4,5,6,7}` → 「決済処理を行っていますので、操作できません。」 | `:3149-3158` | Cao |
| **BR-11** | **Số lần đặt chỗ**: `b_setting_basic_event.type_times_booking = 2` (hoặc `b_slot.times_booking = 2` khi `is_set_each_booking = 1`) → **chỉ cho đặt 1 lần** trên slot/event đó; hệ thống trả `arraySlotIdUserBook` để FE ẩn slot đã đặt | `BookingEventDayManagementController.php:1728-1744` | Trung bình |
| **BR-12** | **Cấu hình từng slot hay dùng chung**: `b_setting_basic_event.is_set_each_booking` — `0` = dùng cấu hình chung của event; `1` = mỗi slot cấu hình riêng | `BookingEventDayManagementController.php:1728-1744` | Cao |
| **BR-13** | **Hạn chót (deadline)** được suy diễn từ số ngày trước sự kiện: `date_deadline = date_start - duration_deadline`; `date_end_change_request = date_start - duration_change_request`; `date_end_cancel = date_start - duration_cancel`. Đổi `date_start` → **recompute toàn bộ** | `:1545`, `:1567`, `:1578` (slot); `:5338`, `:5348`, `:5359` (plan); `:6445-6458` (recompute) | Cao |
| **BR-14** | **Cho phép huỷ/đổi**: LINE user chỉ huỷ được khi `now() <= date_deadline_change_cancel + time_deadline_change_cancel` (hoặc `setting_deadline = 0` → luôn cho phép) | `BookingEventDayManagementController.php:1764-1769` | Cao |
| **BR-15** | **Thời điểm mở bán slot**: `b_setting_date_event.date_show_slot = date_start - duration`, kèm `time_show_slot`. Nếu thiếu duration/time → cả 3 field = NULL (mở bán ngay) | `:6504-6516` | Cao |
| **BR-16** | **Đổi đặt chỗ (change booking)** tạo **2 bản ghi** `b_user_booking` liên kết qua cột `update_to`: bản mới `update_to = id_cũ`. Khi duyệt → xoá bản cũ; khi từ chối → xoá bản mới và khôi phục `status = last_status`. `b_user_booking_history` được **chuyển sang** bản ghi còn lại | `functions.php:5885-5920` (từ chối), `:5921-5975` (duyệt) | Cao |
| **BR-17** | **Action ưu tiên plan hay slot**: khi `using_action_slot_booking_v1` (hoặc `using_action_slot_change_request` / `using_action_slot_cancel`) `= 1` → ưu tiên `action_id_*` của **plan**, fallback về slot; `= 0` → chỉ dùng action của **slot** | `:2825-2829`; `functions.php:5877-5884` | Cao |
| **BR-18** | **Chế độ duyệt** (`approval_system` trên slot / `approval_system_booking` trên plan/event): `0` = tự động duyệt (booking → status 5), `1` = cần admin duyệt (booking → status 3 承認待ち) | `BookingEventDayManagementController.php:705`, `:737` | Cao |
| **BR-19** | **Form thông tin mặc định**: mỗi event mới luôn có 2 field bắt buộc 「お名前」(`friend_info_id = -1`) và 「メールアドレス」(`friend_info_id = -3`), `is_default = 1`, `is_require = 1`, `is_mapping_info = 1` | `:146-179` | Cao |
| **BR-20** | **Mapping thông tin form → hồ sơ bạn bè**: `friend_info_id` âm map tới cột của `line_user` (`-1` view_name, `-2` phone_number, `-3` email, `-4` age, `-6` province); dương → `friend_information_value`. Mọi thay đổi ghi `friend_info_history` (trigger `8001`) | `:2696-2760` | Cao |
| **BR-21** | **Hoàn tiền**: `reason_refund = 1` → gọi API cổng thanh toán; giá trị khác → chỉ đánh dấu DB (hoàn ngoài hệ thống). Luôn set `status_payment = 2` + `refund_date` + ghi history | `BookingEventDayManagementController.php:1818-1889` | Cao |
| **BR-22** | **Remind**: chỉ đăng ký `user_event` khi conversation **chưa bị block** (`conversation.is_blocked = 0`). Step `before_day = -1` gửi ngay khi đặt chỗ; các step khác được đẩy vào `event_step_time` khi lưu slot | `:4199-4288`; `functions.php:9463-9506` | Cao |
| **BR-23** | **Hiển thị slot** — 3 cờ ở `b_setting_basic_event` (mục 「予約枠表示設定」), tất cả đều theo chiều **`1` = 表示 / `0` = 非表示**:<br>• `is_show_slot_expire` — hiện slot đã hết hạn nhận đặt<br>• `is_show_slot_over` — hiện slot đã đầy (満席)<br>• `is_hide_remain` — **hiện số chỗ còn lại 「残数」**. ⚠ **Tên cột ngược nghĩa**: `is_hide_remain = 1` **KHÔNG phải** "ẩn" mà là **「表示」 (HIỆN)**; `0` = 「非表示」. Xác nhận: `add_v2.blade.php:1971-1981` (radio `value="1"` → label 「表示」, `value="0"` → 「非表示」) và `order/choose_slot_plan.blade.php:31` (`v-show="is_hide_remain == true"` bọc khối 「残数」). Khớp `db/db-mapping.md` §3.2 | `:1230-1232`, `:5566-5568`; `add_v2.blade.php:1971-1981`; `order/choose_slot_plan.blade.php:31` | Cao |
| **BR-24** | **Folder sự kiện** dùng bảng `category` với `kind = 21` (`config('sns-line.category_kind.event_booking_v1')`); xoá folder = soft delete (`is_deleted = 1`) nhưng **xoá cứng** toàn bộ event bên trong | `config/sns-line.php:308`; `BookingEventDayManagementController.php:175-240` | Cao |
| **BR-25** | Trang preview điều khoản dùng **Hashids** để mã hoá `event_id` trên URL (`previewTermBill`, `saveAndPreviewTermBill`, trang LIFF `hash_event_id`) | `:6262-6277`, `:785` | Cao |

---

## 11. Điểm cần lưu ý (khuyết tật phát hiện trong code)

| # | Vấn đề | Vị trí | Mức độ |
|---|---|---|---|
| 1 | Route `POST /basic/ajaxAddBooking` trỏ tới method **không tồn tại** `BookingEventDayController@ajaxAddBooking` | `routes/web.php:1178` | Cao — route chết |
| 2 | `deleteMultipleSlot` dùng biến `$slotId` **chưa khai báo** | `BookingEventDayController.php:5402` | Cao — lỗi runtime |
| 3 | `refundMoneyBookingEvent` lấy `bot_id` từ **request** (không phải `getBotId()`), nhưng lại dùng `getBotId()` khi lấy key UnivaPay | `BookingEventDayManagementController.php:1797`, `:1850` | Cao — IDOR / không nhất quán |
| 4 | Endpoint AJAX chỉ có `check_login`, **không có `basic_access`** → bỏ qua phân quyền Staff và `is_expire` | `routes/web.php:2454` | Cao |
| 5 | Refund **không idempotent** — không kiểm tra `status_payment` hiện tại | `BookingEventDayManagementController.php:1794-1902` | Trung bình |
| 6 | **Không có DB transaction** — tất cả `DB::beginTransaction()` / `commit()` / `rollback()` đều bị **comment out** trong 2 controller → thao tác xoá cascade / lưu nhiều bảng có thể để lại dữ liệu rác nếu lỗi giữa chừng | `:530`, `:602`, `:1220`, `:1305`, `:1341`, `:1517`, `:2636`, `:3803`… và Management `:116`, `:456`, `:605`, `:787` | **Cao — rủi ro toàn vẹn dữ liệu** |
| 7 | Webhook UnivaPay **không xác thực chữ ký** | `WebhookUnivapayControler.php:11-41` | Cao |
| 8 | Hầu hết endpoint save **không validate server-side**; `validateFormSettingEvent()` là dead code | `BookingEventDayController.php:1667` | Trung bình |
| 9 | Exception ở nhiều AJAX trả **HTTP 200** với `status: false` → FE khó phân biệt lỗi | `BookingEventDayManagementController.php:470-475`, `:792-797` | Thấp |
| 10 | `ajaxGetAllSlotEvent` hardcode `limit(100)` cho danh sách bạn bè → bot nhiều bạn bè sẽ thiếu dữ liệu ở màn thêm đặt chỗ thủ công | `BookingEventDayManagementController.php:1664` | Trung bình |
| 11 | Logic `addActionRemind` bị **duplicate 3 nơi** (`BookingEventDayController:4169`, `MobileEventBookingController:2628`, `EventBookingService:1054`) | — | Trung bình |
