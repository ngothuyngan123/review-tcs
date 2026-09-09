# API Spec — FA-021 「イベント予約」 (Đặt lịch sự kiện)

- **Portal**: Admin (LINE OA) + trang public cho LINE User
- **Controllers chính**:
  - `src/web/sns-line/app/Http/Controllers/Basic/BookingEventDayController.php` (6.533 dòng)
  - `src/web/sns-line/app/Http/Controllers/Basic/BookingEventDayManagementController.php` (1.925 dòng)
  - `src/web/sns-line/app/Http/Controllers/Basic/MobileEventBookingController.php` (public — LINE User)
  - `src/web/sns-line/app/Http/Controllers/WebhookUnivapayControler.php` (webhook thanh toán)
- **Routes**: `src/web/sns-line/routes/web.php`
- **Ghi chú**: Tính năng này là phiên bản **v2 / "event day"** (`b_event_detail.type_event_new = 1`). Tồn tại song song bộ `booking_event` (v1, `BookingEventController` / `BookingEventManagementController`) — **KHÔNG thuộc phạm vi spec này**.

---

## 1. Nhóm middleware & prefix

| Nhóm route | Prefix | Middleware | File:line | Đối tượng |
|---|---|---|---|---|
| Giao diện Admin (HTML) | `/basic` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | `routes/web.php:869` | Admin / Staff |
| AJAX Admin (JSON) | `/ajax` | `check_login`, `check_remember_token` | `routes/web.php:2454` | Admin / Staff |
| Trang public LINE User | `/mobile` | *(không có middleware auth)* | `routes/web.php:3753` | LINE User |
| AJAX public LINE User | `/ajax` (khai báo full path, ngoài group) | *(không có middleware auth)* | `routes/web.php:4002–4016` | LINE User |
| Webhook thanh toán | — | *(không auth — xác thực bằng metadata)* | `routes/web.php:4020` | UnivaPay |

Tất cả nằm trong group ngoài cùng `Route::middleware(['NotifyChatworkRequestTimeSlow'])` (`routes/web.php:81`).

**Middleware `basic_access`** (`app/Http/Middleware/BasicAccess.php:28-60`): kiểm tra `Auth::check()` + `role ∈ {-1, 0, 1, 2}`; nếu bot hiện tại không thuộc `Auth::id()` → coi là **Staff (bot invite)**, lấy danh sách route được phép qua `getRouterBotInvite()` và chặn nếu route hiện tại không nằm trong danh sách → redirect kèm lỗi 「この権限は許可されていません。」. **Độ tin cậy: Cao**.

> Nhóm AJAX Admin chỉ có `check_login` (không có `basic_access`) → **các endpoint AJAX KHÔNG kiểm tra permission Staff**, chỉ kiểm tra đăng nhập. Phân quyền chỉ chặn ở tầng trang HTML. **Độ tin cậy: Cao** (đọc trực tiếp từ `routes/web.php:2454`).

---

## 2. Bảng tổng hợp endpoints

### 2.1 Giao diện Admin (HTML — prefix `/basic`)

| ID | Method | URL | Mô tả | Controller@method | Màn hình |
|----|--------|-----|-------|-------------------|----------|
| EP-01 | GET | `/basic/booking-event-day/list-event` | Danh sách sự kiện 「イベント一覧」 | `BookingEventDayManagementController@listBookingEvent` (`:63`) | SCR-EBD-01 |
| EP-02 | GET | `/basic/booking-event-day/add` | Trang tạo sự kiện (wizard `add_v2`) | `BookingEventDayController@create` (`:1089`) | SCR-EBD-02 |
| EP-03 | GET | `/basic/booking-event-day/{id}/edit` | Trang sửa sự kiện (wizard `add_v2`) | `BookingEventDayController@edit` (`:1130`) | SCR-EBD-02 |
| EP-04 | GET | `/basic/booking-event-day/event/{id}/slots` | Danh sách khung giờ (slot) của sự kiện 「予約枠 一覧」 | `BookingEventDayManagementController@listSlotOfEvent` (`:88`) | SCR-EBD-09 |
| EP-05 | GET | `/basic/booking-event-day/detail-slot/{date_id}` | Cấu hình khung giờ 「予約枠設定」 (thêm mới) | `BookingEventDayController@detailSlot` (`:5413`) | SCR-EBD-07 |
| EP-06 | GET | `/basic/booking-event-day/add-slot-date/{date_id}` | Quản lý ngày tổ chức 「開催日」 (slot + plan của 1 ngày) | `BookingEventDayController@addSlotDate` (`:5487`) | SCR-EBD-06 |
| EP-07 | GET | `/basic/booking-event-day/edit-slot/{date_id}/{slot_id}` | Cấu hình khung giờ 「予約枠設定」 (sửa) | `BookingEventDayController@editSlot` (`:5500`) | SCR-EBD-07 |
| EP-08 | GET | `/basic/booking_event_day/list-plan/{slot_id}` | Danh sách plan (プラン) của slot | `BookingEventDayController@listPlan` (`:5129`) | — (trả view **legacy** `list_plan_slot.blade.php` — không có mã màn hình trong `ui-spec.md`) |
| EP-09 | GET | `/basic/booking-event-day/add-plan/{slot_id}` | Cấu hình gói 「コース編集」 (thêm) | `BookingEventDayController@addPlanSlot` (`:5147`) | SCR-EBD-08 |
| EP-10 | GET | `/basic/booking-event-day/edit-plan/{plan_id}` | Cấu hình gói 「コース編集」 (sửa) | `BookingEventDayController@editPlanSlot` (`:5168`) | SCR-EBD-08 |
| EP-11 | GET | `/basic/booking-event-day/booking-all-slot/{id}` | Danh sách người tham gia 「参加者リスト」 (toàn sự kiện) | `BookingEventDayController@allBooking` (`:1803`) | SCR-EBD-10 |
| EP-12 | GET | `/basic/booking-event-day/booking-slot/{slot_id}` | Người tham gia theo 1 khung giờ | `BookingEventDayController@bookingSlotDay` (`:2175`) | SCR-EBD-11 |
| EP-13 | GET | `/basic/booking-event-day/detail-booking/{id}` | Chi tiết đặt chỗ 「予約詳細」 | `BookingEventDayController@detailBooking` (`:2532`) | SCR-EBD-12 |
| EP-14 | GET | `/basic/booking-event-day/add-booking/{id}` | Đăng ký booking thủ công 「予約手動登録」 | `BookingEventDayController@addBookingIndex` (`:6238`) | SCR-EBD-13 |
| EP-15 | GET | `/basic/booking-event-day/preview-term-bill/{id}` | Preview 「特定商取引法に基づく表記」 (`id` = Hashids) | `BookingEventDayController@previewTermBill` (`:6262`) | SCR-EBD-15 |
| EP-16 | GET | `/basic/booking-event-day/preview-event-info/{id}` | Preview 「開催情報」 | `BookingEventDayController@previewEventInfo` (`:6279`) | SCR-EBD-14 |
| EP-17 | GET | `/basic/booking_event_day/download-csv` | Tải file CSV đã export | `BookingEventDayController@downloadCsv` (`:4747`) | SCR-EBD-10 |
| EP-18 | GET | `/basic/event-booking-day/set-cookie` | Ghi nhớ folder đang mở ở panel 「フォルダ」 — **không đổi DB** | `Basic\BasicController@folderSetCookie` (`:1921`, `case 'event_booking_day'` `:2093-2108`) | SCR-EBD-01 |

> **EP-18 — `GET /basic/event-booking-day/set-cookie`** (`routes/web.php:3720`, route name `eventBookingDaySetCookie`)
> - **Query params**: `type` = `event_booking_day` (bắt buộc — chọn nhánh `switch` trong controller), `folder_id` = ID folder vừa chọn (`category.id`; `0` = 「未分類」).
> - **Xử lý** (`BasicController.php:2093-2108`): đọc cookie `folder_event_booking_day` (JSON `{ bot_id: folder_id }`), nếu `folder_id` khác giá trị cũ → ghi lại cookie với TTL **14.400 phút (10 ngày)**, `path = /basic/booking-event-day/list-event`, `domain = request()->getHost()`. Nếu không đổi → trả response rỗng, không set cookie.
> - **Response**: body rỗng (HTTP 200), kèm `Set-Cookie` khi có thay đổi. **Không đọc/ghi DB.**
> - ⚠ Route này nằm **ngoài mọi group auth** (chỉ có `NotifyChatworkRequestTimeSlow` từ `routes/web.php:81`) — không có `basic_access` cũng không có `check_login`. `bot_id` lấy từ session qua `getBotId()`. **Độ tin cậy: Cao**.

### 2.2 AJAX Admin (JSON — prefix `/ajax`)

| ID | Method | URL | Mô tả | Controller@method |
|----|--------|-----|-------|-------------------|
| EP-20 | POST | `/ajax/get-list-event-day` | Lấy danh sách sự kiện + thao tác folder/xoá/sắp xếp/di chuyển | `BookingEventDayManagementController@ajaxGetListEvent` (`:113`) |
| EP-21 | POST | `/ajax/get-list-slot-event-day` | Lấy danh sách slot của sự kiện + xoá slot | `BookingEventDayManagementController@ajaxGetListSlotOfEvent` (`:602`) |
| EP-22 | POST | `/ajax/get-all-slot-event-day` | Lấy tất cả slot (còn hiệu lực) + danh sách bạn bè | `BookingEventDayManagementController@ajaxGetAllSlotEvent` (`:1651`) |
| EP-23 | POST | `/ajax/ajaxGetSettingEditDataDay` | Nạp dữ liệu wizard tạo/sửa sự kiện | `BookingEventDayController@ajaxGetSettingEditData` (`:205`) |
| EP-24 | POST | `/ajax/initDataSettingBasicEvent` | Nạp lại tab cài đặt cơ bản (action/approval) | `BookingEventDayController@initDataSettingBasicEvent` (`:1433`) |
| EP-25 | POST | `/ajax/booking_event_day/save-setting-basic` | Lưu step「基本設定」(thông tin chung + action) | `BookingEventDayController@saveSettingBasicEvent` (`:1191`) |
| EP-26 | POST | `/ajax/booking_event_day/save` | Lưu step 1「イベント情報」(tiêu đề, ảnh, nội dung) | `BookingEventDayController@saveSettingEvent` (`:1321`) |
| EP-27 | POST | `/ajax/booking-event-day/saveSettingStep2` | Lưu step 2「予約フォーム」(setting info + điều khoản) | `BookingEventDayController@saveSettingStep2` (`:511`) |
| EP-28 | POST | `/ajax/booking-event-day/saveSettingStep3` | Lưu step 3「確認・完了画面」 | `BookingEventDayController@saveSettingStep3` (`:615`) |
| EP-29 | POST | `/ajax/booking-event-day/saveSettingBill4` | Lưu step 4「決済設定」(Stripe/UnivaPay) | `BookingEventDayController@saveSettingBill4` (`:681`) |
| EP-30 | POST | `/ajax/booking-event-day/saveAndPreviewTermBill` | Lưu + trả hashid để preview điều khoản thanh toán | `BookingEventDayController@saveAndPreviewTermBill` (`:743`) |
| EP-31 | POST | `/ajax/booking-event-day/addDateSlot` | Thêm các ngày tổ chức (date picker) | `BookingEventDayController@addDateSlot` (`:6289`) |
| EP-32 | POST | `/ajax/booking-event-day/initDateSlot` | Nạp danh sách ngày + slot của sự kiện | `BookingEventDayController@initDateSlot` (`:6360`) |
| EP-33 | POST | `/ajax/booking-event-day/initSlotOfDate` | Nạp slot + plan của 1 ngày | `BookingEventDayController@initSlotOfDate` (`:6382`) |
| EP-34 | POST | `/ajax/booking-event-day/initSlotData` | Nạp dữ liệu 1 slot (kèm chi tiết action) | `BookingEventDayController@initSlotData` (`:5444`) |
| EP-35 | POST | `/ajax/booking-event-day/initPlanData` | Nạp dữ liệu 1 plan | `BookingEventDayController@initPlanData` (`:5192`) |
| EP-36 | POST | `/ajax/booking-event-day/slot_booking_event/save` | Lưu slot (tạo/cập nhật `b_slot`) | `BookingEventDayController@saveSettingSlotEvent` (`:1503`) |
| EP-37 | POST | `/ajax/booking-event-day/save-setting-slot` | Lưu cấu hình bổ sung của slot (remind, giới hạn người) | `BookingEventDayController@saveSettingSlot` (`:5535`) |
| EP-38 | POST | `/ajax/booking-event-day/save-setting-plan` | Lưu plan (tạo/cập nhật `b_plan_slot`) | `BookingEventDayController@saveSettingPlan` (`:5310`) |
| EP-39 | POST | `/ajax/booking-event-day/saveAllSlotPlanDay` | Lưu hàng loạt slot + plan của 1 ngày | `BookingEventDayController@saveAllSlotPlanDay` (`:6404`) |
| EP-40 | POST | `/ajax/ajaxSaveDurationSettingDate` | Lưu thời điểm mở bán slot (`duration`, `time_show_slot`) | `BookingEventDayController@ajaxSaveDurationSettingDate` (`:6494`) |
| EP-41 | POST | `/ajax/booking-event-day/deleteSettingInfo` | Xoá 1 field form thông tin | `BookingEventDayController@deleteSettingInfo` (`:800`) |
| EP-42 | POST | `/ajax/booking-event-day/changeMappingInfo` | Bật/tắt mapping / hiển thị field form | `BookingEventDayController@changeMappingInfo` (`:482`) |
| EP-43 | POST | `/ajax/booking-event-day/copy-booking-event` | Copy sự kiện | `BookingEventDayController@copyBookingEvent` (`:5608`) |
| EP-44 | POST | `/ajax/booking-event-day/copyDateEvent` | Copy 1 ngày (kèm slot/plan) | `BookingEventDayController@copyDateEvent` (`:5752`) |
| EP-45 | POST | `/ajax/booking-event-day/copy-slot` | Copy slot | `BookingEventDayController@copySlot` (`:5857`) |
| EP-46 | POST | `/ajax/booking-event-day/copy-plan` | Copy plan | `BookingEventDayController@copyPlan` (`:6087`) |
| EP-47 | POST | `/ajax/booking-event-day/delete-plan` | Xoá plan | `BookingEventDayController@deletePlan` (`:6187`) |
| EP-48 | POST | `/ajax/booking-event-day/remove-slot` | Xoá slot | `BookingEventDayController@deleteSlot` (`:5001`) |
| EP-49 | POST | `/ajax/booking-event-day/deleteDateSlot` | Xoá 1 ngày (kèm toàn bộ slot/plan/booking) | `BookingEventDayController@deleteDateSlot` (`:5047`) |
| EP-50 | POST | `/ajax/booking-event-day/refund` | **Hoàn tiền** 1 đặt chỗ | `BookingEventDayManagementController@refundMoneyBookingEvent` (`:1794`) |
| EP-51 | POST | `/ajax/booking_event_day/export-csv_tab` | Export CSV danh sách đặt chỗ | `BookingEventDayController@exportCSV` (`:4620`) |
| EP-52 | POST | `/ajax/booking_event_day/export-csv-slot-or-plan` | Export CSV theo slot/plan | `BookingEventDayController@exportCSVSlotOrPlan` (`:4754`) |
| EP-53 | POST | `/ajax/booking-event/get-friend-info-type-select` | Lấy field thông tin bạn bè dạng select | `BookingEventController@getFriendInfoTypeSelect` *(dùng chung với v1)* |

### 2.3 AJAX Admin — quản lý đặt chỗ (prefix `/basic`, KHÔNG phải `/ajax`)

> Các route này khai báo **bên trong group `/basic`** (`routes/web.php:1161–1178`) → URL đầy đủ có prefix `/basic`, và **có** middleware `basic_access` + `is_expire`.

| ID | Method | URL | Mô tả | Controller@method |
|----|--------|-----|-------|-------------------|
| EP-60 | POST | `/basic/ajaxAllBooking` | Danh sách đặt chỗ toàn sự kiện (filter/paginate) | `BookingEventDayController@ajaxAllBooking` (`:1885`) |
| EP-61 | POST | `/basic/ajaxAllBookingOfDay` | Danh sách đặt chỗ theo ngày | `BookingEventDayController@ajaxAllBookingOfDay` (`:2371`) |
| EP-62 | POST | `/basic/ajaxBookingSlotDay` | Danh sách đặt chỗ theo slot | `BookingEventDayController@ajaxBookingSlotDay` (`:2194`) |
| EP-63 | POST | `/basic/ajaxBookingDetail` | Chi tiết đặt chỗ | `BookingEventDayController@ajaxBookingDetail` (`:2542`) |
| EP-64 | POST | `/basic/booking_event_day/booking-all-slot/save` | Admin tạo đặt chỗ thủ công | `BookingEventDayController@saveAdminBooking` (`:2633`) |
| EP-65 | POST | `/basic/booking_event_day/booking-all-slot/save-action` | **Duyệt / từ chối / huỷ / đổi** đặt chỗ | `BookingEventDayController@saveActionBooking` (`:3123`) |
| EP-66 | POST | `/basic/booking_event_day/booking-detail/save-action` | Như EP-65 (gọi từ màn chi tiết) | `BookingEventDayController@saveActionBooking` (`:3123`) |
| ⚠ | POST | `/basic/ajaxAddBooking` | **Route chết** — method `ajaxAddBooking` KHÔNG tồn tại trong `BookingEventDayController` (grep toàn `app/` không thấy). Gọi vào sẽ lỗi 500 (`BadMethodCallException`). **Độ tin cậy: Cao** | — |

### 2.4 Public — LINE User (không auth)

| ID | Method | URL | Mô tả | Controller@method |
|----|--------|-----|-------|-------------------|
| EP-70 | GET | `/mobile/event-booking/index/{hash_event_id}/{u_code?}` | Trang đặt chỗ LIFF cho LINE User | `MobileEventBookingController@index` (`:98`) |
| EP-71 | POST | `/ajax/booking-event/get-slots` | Lấy danh sách slot/plan còn chỗ | `MobileEventBookingController@getSlots` (`:207`) |
| EP-72 | POST | `/ajax/booking-event/payment` | **Đặt chỗ + thanh toán** | `MobileEventBookingController@payment` (`:706`) |
| EP-73 | POST | `/ajax/booking-event/change-booking` | Yêu cầu đổi đặt chỗ | `MobileEventBookingController@changeBooking` (`:1712`) |
| EP-74 | POST | `/ajax/booking-event/cancel-v2` | Yêu cầu huỷ đặt chỗ | `MobileEventBookingController@cancelUserBooking` (`:1572`) |
| EP-75 | POST | `/ajax/booking-event/delete-booking-confirm-fail` | Xoá booking khi thanh toán fail | `MobileEventBookingController@deleteBookingConfirmFail` (`:1511`) |
| EP-76 | POST | `/ajax/booking-event/rollback-change-booking-confirm-fail` | Rollback đổi booking khi thanh toán fail | `MobileEventBookingController@rollbackChangeBookingConfirmFail` (`:1527`) |
| EP-77 | POST | `/ajax/univapay/event-booking/call-create-customer-id` | Tạo customer id UnivaPay | `MobileEventBookingController@createCustomerIdUnivapay` (`:456`) |
| EP-78 | POST | `/ajax/get-info-card-event-booking` | Lấy thông tin thẻ đã lưu | `MobileEventBookingController@getInfoCardPayment` (`:517`) |
| EP-79 | POST | `/mobile/get-history-booking-app` | Lịch sử đặt chỗ của LINE User | `MobileEventBookingController@ajaxGetHistoryBookingApp` (`:2509`) |
| EP-80 | POST | `/mobile/booking-event/get-friend-info` | Lấy thông tin bạn bè để prefill form | `BookingEventDayController@getFriendInfoEvent` (`:6006`) |
| EP-81 | GET | `/mobile/booking-event-day/preview-term-bill/{id}` | Preview điều khoản (bản mobile) | `BookingEventDayController@previewTermBillMobile` (`:6271`) |
| EP-82 | POST | `/mobile/univapay-callback-payment` | **Webhook UnivaPay** `charge_finished` | `WebhookUnivapayControler@webhook` (`:11`) |

> **EP-79 — lưu ý trùng tên method**: route `POST /mobile/get-history-booking-app` (`routes/web.php:3755`) trỏ tới **`MobileEventBookingController@ajaxGetHistoryBookingApp` (`:2509`)** — đây là endpoint **thật**.
> Tồn tại một method **trùng tên** ở `BookingEventDayManagementController@ajaxGetHistoryBookingApp` (`:1690-1792`) nhưng **KHÔNG có route nào trỏ tới** → **dead code** (đã grep toàn bộ `routes/web.php`). **Độ tin cậy: Cao**.

---

## 3. Chi tiết endpoint quan trọng

### EP-20 — POST `/ajax/get-list-event-day`
Xác nhận qua network capture trên browser thật (màn hình danh sách).

**Request params** (form-data):

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `action` | body | string | Không | `addAndEditGroup` \| `deleteGroup` \| `removeEvents` \| `removeEvent` \| `sortItem` \| `sortFolder` \| `moveItem` \| (rỗng = chỉ load) |
| `group_id` | body | int | Không | ID folder (`category.id`); `0` = folder mặc định |
| `keyword` | body | string | Không | Từ khoá tìm kiếm |
| `id` | body | int | Khi `addAndEditGroup` | ID folder cần sửa (rỗng = tạo mới) |
| `group_name` | body | string | Khi `addAndEditGroup` | Tên folder |
| `item_id` | body | int | Khi `removeEvent` | ID sự kiện |
| `item_ids` | body | int[] | Khi `removeEvents` / `moveItem` | Danh sách ID sự kiện |
| `folder_move_id` | body | int | Khi `moveItem` | Folder đích |
| `sort_ids` | body | string (CSV) | Khi `sortItem` / `sortFolder` | Danh sách ID theo thứ tự mới |
| `sort_position` | body | string (CSV) | Khi `sortFolder` | Vị trí tương ứng |

**Response 200 (thành công)** — `BookingEventDayManagementController.php:457-469`:
```json
{
  "status": true,
  "isAdd": true,
  "msg_plan": null,
  "groups": [{ "id": 12, "name": "セミナー", "position": 1 }],
  "items_default": [{ "id": 101, "title": "...", "hashIdEvent": "xYz1", "max": 30, "number_approve_done": 5, "number_approve_doing": 12 }],
  "items": { "data": [], "current_page": 1, "last_page": 3 },
  "group_open": 0,
  "count_default": 4,
  "total_page": 3,
  "next_page": 2,
  "current_page": 1
}
```

**Lỗi**:
| HTTP | Body | Nguyên nhân |
|---|---|---|
| 500 | `{ "status": false, "msg": MESSAGE_NOTIFY_BACKUP }` | Bot đang backup/restore (`BackupHistory.status ∈ {0,1}`) — chặn mọi action ghi (`:139-145`, `:178-184`, `:246-252`, `:305-311`, `:380-385`) |
| 200 | `{ "status": false, "msg": "<exception message>" }` | Exception (bắt và trả 200 — **không phải 500**) (`:470-475`) |

Trường `isAdd` / `msg_plan`: giới hạn số sự kiện theo gói — xem Business Rules ở `logic-spec.md`.

---

### EP-23 — POST `/ajax/ajaxGetSettingEditDataDay`
Xác nhận qua network capture (màn hình tạo/sửa event).

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `id` | body | int | Không | `event_detail_id`. Rỗng → trả dữ liệu mặc định cho form tạo mới |

**Response 200**: object chứa `event` (`b_event_detail` kèm slots), `bSettingCommon` (`b_setting_basic_event` + danh sách action đã resolve chi tiết), `settingInfos` (`b_info_setting`), danh sách slot. Nguồn: `BookingEventDayController.php:205-313`.

---

### EP-25 — POST `/ajax/booking_event_day/save-setting-basic`

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `eventId` | body | int | Không | Rỗng = tạo mới |
| `type` | body | string | Có | `info` → lưu `$paramInfoCommon`; giá trị khác → lưu `$paramActionCommon` |
| `event` | body | JSON string | Có | `{ title, group_id, line_title, line_explain }` |
| `setting_info_common` | body | JSON string | Có | Xem bảng dưới |

`setting_info_common` khi `type = info` (`:1221-1238`): `max_number`, `is_limit_people`, `limit_people`, `min_people`, `is_set_each_booking`, `type_times_booking`, `unit_booking`, `is_hide_remain`, `is_show_slot_expire`, `is_show_slot_over`, `info_event`, `is_show_map`, `address`, `lat`, `lng`.

`setting_info_common` khi `type ≠ info` (`:1239-1268`) — 3 nhóm action (booking / change_request / cancel), mỗi nhóm gồm: `approval_system_*`, `date_end_*`, `time_end_*`, `using_action_slot_*` và 4 action id (`*_booking_approve`, `*_admin_approve`, `*_approve_request`, `*_cancel_request`).

**Response 200**:
```json
{ "success": true, "error": "", "message": "保存しました。", "event_id": 123, "redirect": "/basic/booking-event-day/123/edit", "bsettingCommonNewId": 45 }
```
`redirect` chỉ khác `null` khi tạo mới.

**Lỗi**:
| HTTP | Body | Nguyên nhân |
|---|---|---|
| 400 | `{ "success": false, "msg": "現在のプランは利用できない機能です。…" }` | Vượt giới hạn gói khi tạo mới (`:1269-1275`) |
| 500 | `{ "status": false, "msg": MESSAGE_NOTIFY_BACKUP }` | Bot đang backup (`:1203-1209`) |
| 500 | `{ "success": false, "error": "...", "message": "登録できませんでした" }` | Exception (`:1313-1318`) |

> **KHÔNG có validation server-side** cho `title` / `line_title` / `line_explain` ở endpoint này — hàm `validateFormSettingEvent()` (`:1667`) tồn tại nhưng **không được gọi** trong luồng save của controller day. **Độ tin cậy: Cao** (grep `validateFormSettingEvent` chỉ thấy định nghĩa).

---

### EP-26 → EP-31 — Các step lưu wizard
Cùng khuôn mẫu với EP-25. Điểm chung (**quan trọng**): **mọi step đều có thể tạo mới `b_event_detail`** nếu `eventId` rỗng → **mọi step đều re-check giới hạn gói** qua `getCreateEventDayLimitError()` (comment `#37292` tại `:548-554`, `:649-655`, `:712-718`, `:769-775`, `:6315-6321`).

| EP | Trường riêng ghi vào `b_event_detail` | File:line |
|---|---|---|
| EP-26 `save` | `title_event`, `content_top`, `content_bottom`, `name_button_info_event`, `bg_button_info_event`, `color_button_info_event`, `image` (upload) | `:1342-1398` |
| EP-27 `saveSettingStep2` | `is_use_terms`, `content_terms`, `is_use_checkbox`, `name/bg/color_button_info_friend` + tạo/sắp xếp `b_info_setting` | `:531-593` |
| EP-28 `saveSettingStep3` | `name/bg/color_button_confirm_detail`, `flag_page_end`, `page_end_simple` (khi `flag_page_end=2`), `url_page_outsite_end` (khi `flag_page_end=1`) | `:631-646` |
| EP-29 `saveSettingBill4` | `is_auto_bill`, `flag_environment` (0=test,1=live), `type_system_bill` (1=Stripe, 2=UnivaPay), `content_term_bill` | `:697-709` |
| EP-30 `saveAndPreviewTermBill` | `content_term_bill`; trả về `event_id` đã **Hashids::encode** | `:758-792` |
| EP-31 `addDateSlot` | Tạo `b_setting_date_event` cho từng ngày trong `dates_picker` (bỏ qua ngày đã tồn tại) | `:6331-6343` |

**Lỗi giới hạn gói ở các step** trả **HTTP 200** (không phải 400): `{ "success": false, "message": "<msg>", "msg": "<msg>" }` — **khác** EP-25 (trả 400). **Độ tin cậy: Cao**.

---

### EP-36 — POST `/ajax/booking-event-day/slot_booking_event/save`

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `slot_id` | body | int | Không | Rỗng/không tồn tại = tạo mới |
| `itemSlot` | body | JSON string | Có | Toàn bộ cấu hình slot |
| `dateSetting` | body | JSON string | Có | `{ id, bot_id, event_detail_id, date_start }` |

`itemSlot` (`:1534-1589`): `time_start`, `time_end`, `is_hide_time_end`, `duration_deadline`, `time_deadline`, `number_people` (定員), `approval_system`, `times_booking`, `event_id` (remind), `date_end_remind`, `time_end_remind`, + 3 nhóm action (booking / change_request / cancel) như EP-25 nhưng hậu tố `_v1`.

**Suy diễn ngày từ duration** (`:1545`, `:1567`, `:1578`): `date_deadline = date_start - duration_deadline` ngày; tương tự `date_end_change_request`, `date_end_cancel`.

**Khi tạo mới** (`:1594-1601`): `position = count(slot của event) + 1`, `limit_people = 10`, `min_people = 1` (hardcode).

**Response 200**: `{ "success": true, "typeSlot": "create"|"update", "slotId": 999, "error": "", "message": "保存しました。" }`

**Lỗi**: 500 `{ success: false, errors: "Booking does not exist" }` khi event không tồn tại (`:1524-1529`); 500 backup; 500 exception (`message: '登録できませんでした。'`).

---

### EP-37 — POST `/ajax/booking-event-day/save-setting-slot`
**Endpoint duy nhất trong nhóm slot có validation** — gọi `validateFormSaveSlotOfEvent($request)` (`:5540`, định nghĩa `:1718-1779`).

**Validation rules** (`:1720-1776`):

| Field | Rule | Message |
|---|---|---|
| `date_start_from` | `required` | 「開催日は必ず指定してくださ。」 |
| `address` | `max:255` | — |
| `date_start_to` | `required` khi `type_event == 1` và có `date_start_from` | 「開催日は必ず指定してくださ。」 |
| `time_start` | `required` khi `type_event != 1` và rỗng | 「開催時間は必ず指定してください。」 |
| `time_end` | `required` khi `is_hide_time_end == 0` và rỗng | 「開催時間は必ず指定してください。」 |
| `date_deadline` | `required` | 「予約期限は必ず指定してください。」 |
| `time_deadline` | `required` (khi `date_deadline` đã có) | 「予約期限は必ず指定してください。」 |
| `address_url` | regex URL http/https | 「案内URLを正しい書式にしてください。」 |

**Rule bổ sung (`after`)**:
- `time_start > time_end` (khi `type_event == 0`) → 「終了時間は開始時間より後に設定してください。」
- `date_start_from > date_start_to` (khi `type_event == 1`) → 「開催日「終了日」は「開始日」以降の日付にしてください」
- `quantity == 0` → 「定員には１以上入力してください」

**Lỗi 422**: `{ "success": false, "errors": { "field": ["message"] } }`

---

### EP-50 — POST `/ajax/booking-event-day/refund` (Hoàn tiền)

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|---|
| `bot_id` | body | int | Có | ID bot |
| `booking_id` | body | int | Có | `b_user_booking.id` |
| `reason_refund` | body | int | Có | `1` = hoàn qua cổng thanh toán (「決済システムから」); giá trị khác = hoàn thủ công ngoài hệ thống (「エルメから」) |

**Luồng** (`BookingEventDayManagementController.php:1794-1902`):
1. Tìm `BBooking` theo `bot_id` + `id`; không có → `{ success: false, message: 'user booking does not exist' }`.
2. Lấy `BEventDetail` → `type_system_bill` (1 = Stripe, 2 = UnivaPay), `flag_environment` (0 = test, 1 = live).
3. **Stripe** (`type_system_bill = 1`, `:1818-1847`): nếu `reason_refund == 1` → lấy secret key từ `s_strip_bot` (`strip_secret_test_key` / `strip_secret_live_key`) → `StripePayment::refundMoney($booking->strip_charge_id)`. Nếu thành công → update `status_payment = 2`, `refund_date = now()`, `reason_refund`.
4. **UnivaPay** (`type_system_bill = 2`, `:1848-1879`): `UnivapayPayment::refundMoney(...)` → `getRefundMoney(...)` xác nhận. Thành công → update `status_payment = 2`, `univapay_charge_id = null`, `refund_date`, `reason_refund`.
5. **Luôn** ghi `b_user_booking_history` với `reason = '¥{amount}の返金（決済システムから|エルメから）'`, `operator_id = Auth::id()`, `operator_name = Auth::user()->username` (`:1880-1889`).

**Response**: `{ "success": true, "message": "refund success" }` (HTTP 200)
**Lỗi** (đều HTTP 200): `{ success: false, message: 'refund fail' | 'user booking does not exist' | 'booking does not exist' | '<exception>' }`

> ⚠ **Không có kiểm tra idempotency / `status_payment` hiện tại** → gọi 2 lần có thể refund 2 lần ở phía cổng thanh toán. **Độ tin cậy: Trung bình** (suy từ code, chưa test).

---

### EP-64 — POST `/basic/booking_event_day/booking-all-slot/save` (Admin đặt hộ)

| Tên | Kiểu | Mô tả |
|---|---|---|
| `event_id` | int | `b_event_detail.id` |
| `slot` | int | `b_slot.id` |
| `plan` | int\|null | `b_plan_slot.id` |
| `line_user` | int | `line_user.id` |
| `name`, `quantity`, `remarks`, `email`, `phone` | mixed | Thông tin đặt chỗ |
| `type_booking` | int | Loại đặt chỗ |
| `action_before_booking` | int | `0` = **có** gửi action; khác 0 = không gửi (`:2806`) |
| `form_info` | JSON string | Mảng giá trị các field `b_info_setting` |

**Side effects** (`:2667-2862`): tạo `b_user_booking` (`status = 5` = booking, `booking_from = 1`), ghi `b_user_booking_history`, đồng bộ `line_user` / `friend_information_value` + `sync_elasticsearch`, `addActionRemind()`, tăng `b_slot.use_people` và `b_plan_slot.remain_limit`, gửi action LINE, `MobileNotifyService::insertNotifyEventBooking(..., 'autoApprove')`.

**Response**: `{ "success": true }` / `{ "success": false, "message": "<exception>" }` (đều HTTP 200).

> **Không có validation** — mọi field lấy thẳng từ `$request`. **Độ tin cậy: Cao**.

---

### EP-65 — POST `/basic/booking_event_day/booking-all-slot/save-action` (Duyệt/từ chối/huỷ/đổi)

| Tên | Kiểu | Mô tả |
|---|---|---|
| `bookingId` | int | `b_user_booking.id` |
| `status` | int | Trạng thái mới: `1` approve, `2` deny, `3` pending, `4` cancel, `5` booking, `6` request_change, `7` request_cancel (`config/sns-line.php:398-407`) |
| `type_action`, `action`, `type_request` | string | Loại thao tác (vd `deny_change`) |
| `slot_id`, `plan_slot_id`, `quantity` | int | Giá trị mới khi đổi slot/plan/số lượng |
| `approveAny` | bool | `true` = bỏ qua cảnh báo vượt định員 |
| `created_at`, `created_at_time` | string | Thời điểm tạo (ghi đè) |
| `form_info` | JSON string | Cập nhật thông tin form |

**Chặn khi đang xử lý thanh toán** (`:3149-3158`): nếu `status_webhook ∈ {0,3,4,5,6,7}` → `{ success: false, payment_failed: true, message: "決済処理を行っていますので、操作できません。" }`.

**Cảnh báo vượt định員** (`:3237-3255`): nếu còn chỗ (`limit`) < `quantity` mới và `approveAny` chưa bật → `{ success: false, admin_confirm: 1, message: "予約枠を超えています。承認しますか？" }` (HTTP 200) — FE hiển thị confirm rồi gọi lại với `approveAny = true`.

**Side effects**: xem `logic-spec.md` mục 6.

---

### EP-72 — POST `/ajax/booking-event/payment` (LINE User đặt chỗ + thanh toán)

| Tên | Kiểu | Mô tả |
|---|---|---|
| `eventId` | int | `b_event_detail.id` |
| `lineId` | string | `line_user.line_id` |
| `infoOrder` | object | `{ slot_id, plan_slot_id, number_order }` |
| `listInfoSetting` | array | Giá trị các field form (`friend_info_id`, `value`, `is_default`) |
| `infoCard` | object | Thông tin thẻ / token |
| `autoBill` | bool | Tự động thanh toán |
| `is_use_checkbox` | int | Xác nhận điều khoản |
| `alreadyPayment`, `chargeId` | mixed | Dùng khi retry sau webhook |

**Response**: `{ "success": "ok"|"error", "errorMessage": "...", ... }` (HTTP 200; `success` là **string** chứ không phải boolean — `:759-762`, `:766`).

**Luồng thanh toán**: tạo `b_user_booking` với `status_webhook = UNPROCESSED(0)` → gọi Stripe `autoPaymentIntents` hoặc UnivaPay `chargeMoneyUnivapaySale` (metadata `module = 'event-booking'`) → chờ webhook. Nếu quá thời gian chờ → `status_webhook = TIMEOUT(3)` / `TIMEOUT_WEBHOOK(4)`.

---

### EP-82 — POST `/mobile/univapay-callback-payment` (Webhook UnivaPay)
`WebhookUnivapayControler.php:11-41`.

**Request** (JSON từ UnivaPay):
```json
{ "event": "charge_finished", "data": { "metadata": { "module": "event-booking" }, "...": "..." } }
```
Chỉ xử lý khi `event == 'charge_finished'` **và** `data.metadata.module ∈ ['lesson','lesson_change_status','salon','salon_change_status','event-booking','event_booking_change','sales','sales_change_card','sales_job']`.

**Xử lý**: `HandleWebhookUnivapay::dispatch($data, 'univapay')` → **Laravel queue job** → `EventBookingService::handleOrderCallback()` (module `event-booking`) hoặc `callbackChangeBooking()` (module `event_booking_change`). Xem `app/Jobs/HandleWebhookUnivapay.php:38-62`.

**Response**: `{ "status": "success" }` — **luôn 200**, kể cả khi module không khớp.

> ⚠ Webhook **không xác thực chữ ký** — chỉ dựa vào `metadata.module`. **Độ tin cậy: Cao**.

---

## 4. Liên kết endpoint ↔ màn hình UI

> **Chuẩn mã màn hình = `ui/ui-spec.md`** (đồng bộ với `db/db-mapping.md`). Mọi mã `SCR-EBD-XX` dưới đây đều tồn tại trong `ui-spec.md` mục 2.

### 4.1 Phía Admin

| Màn hình (theo `ui-spec.md`) | Load HTML | AJAX sử dụng |
|---|---|---|
| SCR-EBD-01 Danh sách sự kiện 「イベント予約」 | EP-01 | EP-20, EP-18 (set-cookie folder) |
| SCR-EBD-02 Tạo / sửa sự kiện 「イベント編集」 (khung + 4 tab) | EP-02 / EP-03 | EP-23, EP-24, EP-53 |
| SCR-EBD-02a Tab 「開催日程」 | (tab trong SCR-EBD-02) | EP-31, EP-32, EP-40 |
| SCR-EBD-02b Tab 「各種ページ」 (3 sub-tab) | (tab trong SCR-EBD-02) | EP-26, EP-27, EP-28, EP-41, EP-42 |
| SCR-EBD-02c Tab 「詳細設定」 | (tab trong SCR-EBD-02) | EP-25 |
| SCR-EBD-02d Tab 「決済設定」 | (tab trong SCR-EBD-02) | EP-29, EP-30 |
| SCR-EBD-03 Modal 「開催日追加」 | (modal trong SCR-EBD-02a) | EP-31 |
| SCR-EBD-04 Modal 「表示予約設定」 | (modal trong SCR-EBD-02a) | EP-40 |
| SCR-EBD-05 Modal 「予約時入力項目」 | (modal trong SCR-EBD-02b) | EP-27, EP-41, EP-42, EP-53 |
| SCR-EBD-06 Quản lý ngày tổ chức 「開催日」 (slot + plan của 1 ngày) | EP-06 | EP-33, EP-39, EP-44, EP-45, EP-46, EP-47, EP-48, EP-49 |
| SCR-EBD-07 Cấu hình khung giờ 「予約枠設定」 | EP-05 / EP-07 | EP-34, EP-36, EP-37 |
| SCR-EBD-08 Cấu hình gói 「コース編集」 | EP-09 / EP-10 | EP-35, EP-38 |
| SCR-EBD-09 Danh sách khung giờ 「予約枠 一覧」 | EP-04 | EP-21 |
| SCR-EBD-10 Danh sách người tham gia 「参加者リスト」 | EP-11 | EP-60, EP-61, EP-65, EP-51, EP-17 |
| SCR-EBD-11 Người tham gia theo 1 khung giờ | EP-12 | EP-62, EP-52, EP-17 |
| SCR-EBD-12 Chi tiết booking 「予約詳細」 (+ modal 返金) | EP-13 | EP-63, EP-66, EP-50 |
| SCR-EBD-13 Đăng ký booking thủ công 「予約手動登録」 | EP-14 | EP-22, EP-64 |
| SCR-EBD-14 Preview 「開催情報」 | EP-16 | EP-25 (lưu trước khi preview) |
| SCR-EBD-15 Preview 「特定商取引法に基づく表記」 | EP-15 (+ EP-81 bản mobile) | EP-30 |

### 4.2 Phía LINE User (LIFF / public)

| Màn hình (theo `ui-spec.md`) | Load HTML | AJAX sử dụng |
|---|---|---|
| SCR-EBD-20 Trang đặt chỗ LIFF (SPA — 7 page state, gồm 20a–20f) | EP-70 | EP-71, EP-72, EP-73, EP-74, EP-75, EP-76, EP-77, EP-78, EP-79, EP-80 |
| SCR-EBD-21 Màn hình chờ xử lý thanh toán | (state trong SCR-EBD-20) | EP-82 (webhook UnivaPay — cập nhật `status_webhook` phía server) |
| SCR-EBD-22 Trang hoàn tất 「予約サイト」 | (view `success_page.blade.php`) | — |

> **EP-08** (`list-plan/{slot_id}`) không gắn với màn hình nào: controller trả view **legacy** `list_plan_slot.blade.php` — đã bị thay bởi `add_plan_slot.blade.php` (SCR-EBD-08).
