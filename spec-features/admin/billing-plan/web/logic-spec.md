# Logic Spec — FA-031: Hợp đồng và Thanh toán (Billing Plan)

## Tổng quan

| Thuộc tính | Giá trị |
|-----------|---------|
| Mã tính năng | FA-031 |
| Controllers | `V2\Bill\ListPageController`, `Basic\UserController`, `Admin\BotController`, `PointSettingController` |
| Services | `BillingService`, `CancelContractService`, `V2\CategoryService` |
| Helpers | `UnivapayPayment`, `StripePayment` |
| Models | `BotContracts`, `BotLifeCycle`, `PaymentHistories`, `Bots`, `BotSlots`, `BotLineUser`, `SubcardBotContract`, `User` |

---

## 1. Controllers và Actions

### 1.1 V2\Bill\ListPageController

**File**: `app/Http/Controllers/V2/Bill/ListPageController.php`

#### Constructor
```
UserRepositoryInterface $userRepositoryInterface
UnivapayPayment $univapayPayment
```

#### `indexView()` — SCR-BLP-01

**Logic chính**:
1. Lấy admin mặc định (id=1) để lấy `basic_fee`
2. Lấy `plan_pro_fee` từ config `sns-line`
3. Lấy bot đang active trong session (`getBotId()`)
4. Nếu có bot active: tìm hợp đồng gắn với bot qua `BotContracts → bot_slots`
5. Đếm số bot free plan của admin hiện tại (`plan_type=2, is_deleted=0`)
6. Render view `basic.bill.index`

**File:line**: `app/Http/Controllers/V2/Bill/ListPageController.php:41`

---

#### `getDataContract(Request $request)` — EP-02

**Logic phân loại hợp đồng** (quan trọng):

Hợp đồng được chia thành 6 nhóm sau khi query:

```
BotContracts
  JOIN bot_slots ON bot_slots.bot_contract_id = bot_contracts.id
  LEFT JOIN bots ON bots.id = bot_slots.bot_id AND bots.is_deleted = 0
  LEFT JOIN (subquery payment_histories lần gần nhất) AS payment_histories
    ON bot_contracts.id = payment_histories.bot_contract_id
WHERE (bots.id IN [listBot] OR bot_contracts.admin_id = current_user)
  AND bot_contracts.status != 0
GROUP BY bot_contracts.id
ORDER BY position DESC, date_cancel_contract DESC, id DESC
```

**Subquery payment_histories** (lấy payment lần gần nhất theo bot_contract):
- Điều kiện: `parent_month = 1` AND (`type_bill IN(1,2) AND type=1`) OR (`type_bill=3`)
- Lấy record có `MAX(id)` theo nhóm `bot_contract_id`

**Phân loại sau khi lấy kết quả**:

| Nhóm | Điều kiện |
|------|-----------|
| `cancelDataContract` | `status == CANCEL (3)` |
| `overdueDataContract` | Thanh toán lỗi (`status_bill_card` hoặc `status_bill_transfer`) VÀ `expired_date_contract < now` |
| `transferDataContract` | `payment_method==2` VÀ `status_payment NOT IN (1,2)` HOẶC `status_payment_max_friend==0` |
| `otherDataContract` (key `data`) | Các hợp đồng bình thường còn lại |
| `maxFriendDataContract` | Clone của item có `max_friend_plan==1` |
| `maxFriendErrorDataContract` | Clone của item có `max_friend_plan==3` |

**Điều kiện thanh toán lỗi**:
```
status_bill_card = payment_method==1 AND status_payment==2 AND status_payment_fail < 5
status_bill_transfer = payment_method==2 AND (status_payment==5 OR status_payment==2) AND status_payment_fail < 5
```

**Logic max_friend_plan**:
- `max_friend_plan == 0`: Không tính phí theo bạn bè
- `max_friend_plan == 1`: Đang đăng ký plan max friend, tính phí bình thường
- `max_friend_plan == 2`: Plan max friend free (không bị lỗi)
- `max_friend_plan == 3`: Plan max friend lỗi

**Tính toán amount cho max friend**:
- Dùng hàm helper `calculateBillMaxFriend($totalFriend)` để tính phí
- Nếu `contract_bill_type == 'year'`: nhân 12
- `totalFriend` = tổng số `BotLineUser` có `bot_id` tương ứng

**File:line**: `app/Http/Controllers/V2/Bill/ListPageController.php:181`

---

#### `cancelTransfer(int $botContractId, Request $request)` — EP-10

**Logic hủy chuyển khoản** — 2 trường hợp:

**Trường hợp 1: `type == 'max-friend'`**

1. Tìm `bot_card_bill_friend` theo `bot_contract_id`
2. Hủy charge Univapay nếu có `univa_charge_id` (gọi `cancelChargeWeb`)
3. Kiểm tra nếu `expired_date < now` AND `expired_date_max_friend <= now`:
   - `process_status = 2, status = 1` → hủy hoàn toàn
   - Set `bots.max_friend_plan = 3` (lỗi)
4. Ngược lại:
   - `process_status = 2, status = 0` → hủy nhưng vẫn còn hiệu lực
   - Set `bots.max_friend_plan = 2` (free)
5. Ghi log `BotLifeCycle::addState` với type `CANCEL_TRANSFER`

**Trường hợp 2: Hủy chuyển khoản thường**

Logic phức tạp dựa trên trạng thái hợp đồng:

| Điều kiện | Hành động |
|-----------|-----------|
| `isContractPendingAccountTransfer && !isHaveBot` | Xóa hợp đồng (`forceDelete`) — chưa có bot nào |
| Không có `chargeId` | Trả về false |
| `status_payment==0 AND is_active==0 AND expired < now+7days` → có bot slot | Set CANCEL |
| `status_payment==0 AND is_active==0 AND expired < now+7days` → không có bot | Delete |
| `status_payment==5 AND expired > now` | Set `status_payment = 1` (hoàn nguyên) |
| `expiredDate + 7days < now` | Set CANCEL |
| Lý do từ nhóm `upgradeFromFree` AND `status_payment==6` | Về lại free plan |
| Lý do từ nhóm `upgradeFromStandard` | Về lại standard plan |
| Lý do từ nhóm `extendContract` | Khôi phục ngày hết hạn trước |
| Mặc định | Set CANCEL |

**Sau đó**: Ghi log `BotLifeCycle::addState` với type `CANCEL_TRANSFER`

**File:line**: `app/Http/Controllers/V2/Bill/ListPageController.php:550`

---

### 1.2 Basic\UserController

**File**: `app/Http/Controllers/Basic/UserController.php`

#### `detailContract(int $id)` — EP-07

1. Gọi `authenticationBotContract($user, $id)` — xác thực quyền truy cập
2. Lấy `SubcardBotContract` theo `bot_contract_id`
3. Hash bot ID bằng `Hashids::encode`
4. Nếu có `user_id_cancel`: lấy tên người hủy
5. Lấy `basic_fee` và `planProFee`
6. Render view `basic.bill.detail`

**File:line**: `app/Http/Controllers/Basic/UserController.php:4620`

#### `ajaxPaymentHistories(Request $request)` — EP-04

**3 mode**:
- `type=1` (năm): Trả về tổng thanh toán theo từng tháng trong năm
- `type=2` (tháng): Trả về chi tiết theo tháng, có phân trang
- `type=3` (ngày): Trả về chi tiết theo khoảng ngày, có phân trang

**Khi `download_invoice=1`**: Không phân trang, trả về toàn bộ để tạo PDF

**Cách lấy bot contracts**: 
- `getBotContractIds($listBotId, $currentUser, $contractId)` — tách bot contracts thành free và paid
- Free contracts: lọc bởi `scopeFilterContractIds` khác nhau
- Paid contracts: chỉ lấy non-free contracts

**Scope `typeBill`**: Chỉ lấy bản ghi hợp lệ — (type=1 AND type_bill IN(1,2)) OR (status_transfer=1 AND type_bill=3)

**Lọc theo plan**: Mapping plan name → danh sách `reason` values trong payment history.

**File:line**: `app/Http/Controllers/Basic/UserController.php:4378`

#### `botLifeCycles(Request $request)` — EP-06

1. Lấy `adminId` từ request hoặc user hiện tại
2. Lấy danh sách bot IDs được phép truy cập (`getListBotIdStaffManagement`)
3. Lấy bot contract IDs từ bot IDs
4. Query `BotLifeCycle` với filter:
   - Theo adminId hoặc botContractIds
   - Nếu `disconnect_account=true`: chỉ lấy type=28 (DELETE_ACCOUNT)
5. Đếm riêng số sự kiện PAYMENT
6. Trả về data kèm `count_payment`

**File:line**: `app/Http/Controllers/Basic/UserController.php:4894`

#### `authenticationBotContract(User $user, int $botContractId)` — private

Dùng để xác thực quyền truy cập hợp đồng. Gọi `Bots::dataBotContract()` với danh sách bot mà user được phép quản lý. Nếu không tìm thấy: throw `HttpException(404)`.

**File:line**: `app/Http/Controllers/Basic/UserController.php:4886`

---

### 1.3 Admin\BotController

**File**: `app/Http/Controllers/Admin/BotController.php`

#### `PlanEstimation(Request $request)` — EP-08

1. Lấy thông tin admin hiện tại và bot active
2. Nếu có `bot_id` trong request: lấy thông tin bot và hợp đồng hiện tại
3. Lấy danh sách bot free (`plan_type=2, is_deleted=0`)
4. Lấy `basic_fee` từ admin id=1
5. Render view `admin.plan_estimate.plan_estimation`

**Note**: `PlanEstimationPost` và `ajaxPlanEstimation` chưa được implement (body rỗng)

**File:line**: `app/Http/Controllers/Admin/BotController.php:11426`

---

## 2. Models

### 2.1 BotContracts

**File**: `app/BotContracts.php`
**Table**: `bot_contracts`

#### Constants

| Constant | Giá trị | Mô tả |
|----------|---------|-------|
| `UNREGISTER` | 0 | Chưa đăng ký |
| `REGISTERED` | 1 | Đang hoạt động |
| `WAITING_CANCEL` | 2 | Đang chờ hủy |
| `CANCEL` | 3 | Đã hủy |
| `CANCEL_BY_JOBS` | 0 | Hủy bởi job tự động |
| `CANCEL_BY_USER` | 1 | Hủy bởi người dùng |

#### Relationships

| Method | Loại | Model | FK |
|--------|------|-------|-----|
| `lastPayment()` | HasOne | `PaymentDetailAff` | `bot_contract_id` |
| `lastHistoryWaitTransfer()` | HasOne | `PaymentHistories` | `bot_contract_id` |
| `lastHistoryAvailable()` | HasOne | `PaymentHistories` | `bot_contract_id` |
| `paymentDetailAffs()` | HasMany | `PaymentDetailAff` | `bot_contract_id` |
| `botSlots()` | HasMany | `BotSlots` | `bot_contract_id` |

#### Computed Attributes (Appended)

**`getIsWaitTransferAttribute()`**: Trả về `true` khi `payment_method==2 AND status_payment NOT IN(1,2) AND univa_account_number != null`
- Tức là: đang chờ xác nhận chuyển khoản đã có số tài khoản

**`getIsOverdueAttribute()`**: Trả về `true` khi `status==1 AND (card payment lỗi OR transfer payment lỗi) AND expired_date_contract < now`

#### Static Methods

| Method | Mô tả |
|--------|-------|
| `getBotNeedChargeByStripe()` | Lấy hợp đồng cần charge bằng Stripe (còn lại từ migration cũ) |
| `getBotNeedChargeByUnivapayCard()` | Lấy hợp đồng cần charge thẻ Univapay |
| `getBotNeedChargeByUnivapayTransfer()` | Lấy hợp đồng cần charge chuyển khoản Univapay (trước 30 ngày) |
| `getBotNeedCancel()` | Lấy hợp đồng cần hủy tự động |
| `getListContractCanceled()` | Lấy hợp đồng đã hủy, đã hết hạn, không có bot slot |
| `getListContractTransferPaymentWaiting()` | Lấy payment history chuyển khoản quá 7 ngày chưa thanh toán |

**File:line**: `app/BotContracts.php:1`

---

### 2.2 BotLifeCycle

**File**: `app/BotLifeCycle.php`
**Table**: `bot_life_cycles` (tên chuẩn Laravel conventions)

#### Constants STATUS

| Constant | Giá trị | Mô tả |
|----------|---------|-------|
| `STATUS['START']` | 1 | Sự kiện bắt đầu |
| `STATUS['PAYMENT']` | 2 | Sự kiện thanh toán |
| `STATUS['CHANGED']` | 3 | Sự kiện thay đổi |
| `STATUS['CANCELED']` | 4 | Sự kiện hủy |

#### Constants TYPE

**Nhóm START**:
| TYPE | Giá trị | Mô tả |
|------|---------|-------|
| `CONNECT_BOT_FREE` | 1 | Kết nối LOA free plan |
| `CONNECT_WITH_PLAN` | 2 | Kết nối LOA có plan |

**Nhóm PAYMENT**:
| TYPE | Giá trị | Mô tả |
|------|---------|-------|
| `PLAN_MONTHLY` | 3 | Bắt đầu trả phí tháng |
| `PLAN_YEARLY` | 4 | Bắt đầu trả phí năm |
| `UPGRADE_PLAN_PRO` | 5 | Nâng cấp lên Pro (tính ngày) |
| `BILL_FRIEND_USE` | 6 | Tính phí theo số bạn bè |
| `UPDATE_PLAN_MONTH` | 7 | Gia hạn tháng |
| `UPDATE_PLAN_YEAR` | 8 | Gia hạn năm |
| `RECONTRACT` | 9 | Tái ký hợp đồng |
| `EXTEND_MORE_1_YEAR` | 10 | Kéo dài thêm 1 năm |

**Nhóm CHANGED**:
| TYPE | Giá trị | Mô tả |
|------|---------|-------|
| `CHANGE_MAIN_CARD` | 11 | Đổi thẻ chính |
| `REGISTER_SUB_CARD` | 12 | Đăng ký thẻ phụ |
| `CHANGE_SUB_CARD` | 13 | Đổi thẻ phụ |
| `REGISTER_CHANGE_PAYMENT_METHOD_CARD` | 14 | Đổi phương thức → thẻ |
| `REGISTER_CHANGE_PAYMENT_METHOD_TRANSFER` | 22 | Đổi phương thức → chuyển khoản |
| `REGISTER_CHANGE_PAYMENT_TIMES_YEAR` | 15 | Đổi chu kỳ → năm |
| `REGISTER_CHANGE_PAYMENT_TIMES_MONTH` | 23 | Đổi chu kỳ → tháng |
| `REPLACE_ACCOUNT_LINE` | 16 | Thay thế LINE OA |
| `ADD_STAFF` | 24 | Thêm staff |
| `DELETE_STAFF` | 25 | Xóa staff |
| `REMOVE_SUB_CARD` | 26 | Xóa thẻ phụ |

**Nhóm CANCELED**:
| TYPE | Giá trị | Mô tả |
|------|---------|-------|
| `CANCEL_TRANSFER` | 17 | Hủy chuyển khoản |
| `WAITING_CANCEL` | 18 | Đăng ký hủy hợp đồng |
| `CANCELED` | 19 | Hủy hợp đồng hoàn thành |
| `BILL_ERROR` | 20 | Lỗi thanh toán |
| `FORCE_CANCEL` | 21 | Cưỡng chế hủy |
| `REMOVE_CANCEL` | 27 | Hủy yêu cầu hủy hợp đồng |
| `DELETE_ACCOUNT` | 28 | Ngắt kết nối LINE OA |

#### JSON_DATA structure (ghi vào cột `data`)

Mỗi bản ghi BotLifeCycle chứa JSON với các field:
`bot_id`, `bot_name`, `bot_image`, `bot_line_id`, `bot_name_new`, `bot_image_new`, `bot_line_id_new`, `plan`, `operator_id`, `operator_name`, `operator_email`, `amount`, `type_bill`, `payment_method`, `payment_id`, `friend_number`, `last4_card_main`, `last4_card_sub`, `next_date_payment`, `remain_upgrade_day`, `staff_name`, `staff_email`, `staff_id`, `extend_time_start`, `extend_time_end`

#### `addState(array $attributes, User $user, Bots $bot)` — static

- Tự động điền `operator_id/name/email` từ User object
- Tự động điền `bot_id/name/image/line_id` từ Bots object
- Nếu bot=null: điền `bot_id=-111, bot_name='LINE公式アカウント未接続'`
- Merge với `JSON_DATA` template để đảm bảo đủ fields
- Exception được catch và log (không throw lại)

**File:line**: `app/BotLifeCycle.php:171`

---

### 2.3 PaymentHistories

**File**: `app/PaymentHistories.php`
**Table**: `payment_histories`

#### Constants

| Constant | Giá trị | Mô tả |
|----------|---------|-------|
| `STATUS_REFUND_AVAILABLE` | 0 | Chưa hoàn tiền |
| `STATUS_REFUND_REFUNDED` | 1 | Đã hoàn tiền |

#### Relationships

| Method | Loại | Model |
|--------|------|-------|
| `user()` | BelongsTo | `User` |
| `botSlot()` | HasOne | `BotSlots` |

#### Scopes

**`scopeTypeBill`**: Lọc bản ghi hợp lệ:
- (type=1 AND type_bill IN(1,2)) OR (status_transfer=1 AND type_bill=3)

**`scopeFilterDate`**: Lọc theo khoảng thời gian:
- mode `month`: lọc theo `LIKE "%YYYY-MM%"`
- mode `day`: lọc theo `BETWEEN start_date AND end_date+1`
- Luôn áp dụng: `remain_day < 365 OR (remain_day >= 365 AND parent_month = 1)`

**`scopeFilterContractIds`**: Lọc theo quyền truy cập:
- `user_id = currentUser AND bot_contract_id NOT IN freeContracts` OR `bot_contract_id IN paidContracts`

#### Cấu trúc cột quan trọng (từ logic suy ra)

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `bot_contract_id` | int | FK đến `bot_contracts.id` |
| `user_id` | int | FK đến `users.id` |
| `amount` | decimal | Số tiền |
| `type` | int | Kiểu bản ghi (1=thu phí thành công) |
| `type_bill` | int | 1=card tháng, 2=card năm, 3=chuyển khoản |
| `status_transfer` | int | Trạng thái chuyển khoản (1=đã thanh toán) |
| `parent_month` | int | 1=bản ghi tháng gốc (không phải phân bổ) |
| `remain_day` | int | Số ngày còn lại (<365=tháng, >=365=năm) |
| `status_refund` | int | 0=chưa hoàn, 1=đã hoàn |
| `reason` | string | Lý do thanh toán (xem danh sách reason trong logic-spec) |
| `created_at` | datetime | Thời gian ghi nhận thanh toán |

**File:line**: `app/PaymentHistories.php:1`

---

### 2.4 Bots

**File**: `app/Bots.php`

#### `dataBotContract(int $botContractId, array $listBotAccept, int $currentUserId)` — static

Query kết hợp:
```sql
SELECT bots.view_name, bots.line_id, bots.bot_image, bots.plan_type, 
       bots.max_friend_plan, bots.expired_date_max_friend, bots.created_at as bot_created_at,
       bot_contracts.*, bots.id as bot_id, users.username
FROM bot_contracts
  JOIN bot_slots ON bot_contracts.id = bot_slots.bot_contract_id
  LEFT JOIN bots ON bots.id = bot_slots.bot_id
  LEFT JOIN users ON bot_contracts.admin_id = users.id
WHERE bot_contracts.id = $botContractId
  AND (bots.id IN $listBotAccept OR bot_contracts.admin_id = $currentUserId)
LIMIT 1
```

**Mục đích**: Xác thực quyền truy cập hợp đồng theo user (Admin hoặc Staff với quyền pointSettings)

**File:line**: `app/Bots.php:116`

---

## 3. Services

### 3.1 BillingService

**File**: `app/Services/BillingService.php`

| Method | Mô tả |
|--------|-------|
| `nextExpiredDate(...)` | Tính ngày hết hạn tiếp theo (theo tháng) |
| `nextExpiredDateByYear(...)` | Tính ngày hết hạn tiếp theo (theo năm) |

**Độ tin cậy**: Trung bình — chỉ đọc tên method, chưa đọc chi tiết logic

### 3.2 CancelContractService

**File**: `app/Services/V2/Bill/CancelContractService/CancelContractService.php`

Sử dụng pattern Specification (`CancelContractSpecInterface`, `RemindSpec`) để xác định điều kiện hủy hợp đồng.

**Độ tin cậy**: Thấp — chỉ thấy import, chưa đọc chi tiết

### 3.3 V2\CategoryService

**File**: (tìm thấy qua import `App\Services\V2\CategoryService`)

Có method `updatePosition('bot_contracts', $data['order'], 'DESC')` — cập nhật vị trí (field `position`) theo thứ tự drag & drop.

**Độ tin cậy**: Trung bình

---

## 4. Helpers / Payment Integrations

### 4.1 UnivapayPayment (Helper)

**File**: `app/Helpers/UnivapayPayment.php`

#### Method `cancelChargeWeb($chargeId)` — dùng cho web requests

- Gọi API Univapay: `POST https://api.univapay.com/stores/{STORE_ID}/charges/{chargeId}/cancels`
- Authentication: Bearer token từ env `UNIVAPAY_APP_SECRET.UNIVAPAY_APP_TOKEN`
- Return: `true` nếu thành công, `false` nếu exception

**Sử dụng tại**: `V2\Bill\ListPageController@cancelTransfer` — hủy pending payment

**File:line**: `app/Helpers/UnivapayPayment.php:815`

#### Các method Univapay khác (dùng trong job hoặc controller khác)

| Method | Mô tả |
|--------|-------|
| `cancelChargeJob($chargeId)` | Hủy charge bởi background job |
| `cancelChargeJobWeb($chargeId)` | Phiên bản khác cho job từ web context |
| `refundMoney(...)` | Hoàn tiền |
| `getRefundMoney(...)` | Lấy thông tin hoàn tiền |
| `cancelCharge(...)` | Hủy charge (phiên bản cũ) |
| `getAccountInfo(...)` | Lấy thông tin tài khoản |
| `getMessageErrorUnivapay(...)` | Dịch mã lỗi Univapay sang text |

### 4.2 StripePayment (Helper)

**File**: `app/Helpers/StripePayment.php`

Đây là integration với Stripe — hệ thống thanh toán cũ trước khi chuyển sang Univapay. Vẫn tồn tại trong code nhưng có vẻ không còn được dùng cho luồng chính.

**Độ tin cậy**: Thấp — chỉ thấy qua import

---

## 5. Business Rules

### 5.1 Quy tắc phân loại hợp đồng

**File**: `app/Http/Controllers/V2/Bill/ListPageController.php:280-429`

1. Hợp đồng `status=0` (UNREGISTER) bị loại khỏi query (`WHERE status != 0`)
2. Hợp đồng CANCEL (3) → nhóm `cancelDataContract`
3. Hợp đồng WAITING_CANCEL (2) → nhóm `otherDataContract` (hiển thị bình thường nhưng đang chờ hủy)
4. Hợp đồng có payment lỗi (card hoặc transfer) và quá hạn → `overdueDataContract`
5. Hợp đồng chuyển khoản chưa xác nhận → `transferDataContract`
6. Còn lại → `otherDataContract` (nhóm `data`)

### 5.2 Quy tắc max_friend_plan

**File**: `app/Http/Controllers/V2/Bill/ListPageController.php:292-433`

- Mỗi hợp đồng có thể sinh thêm 1 "item phụ" cho khoản thanh toán theo số bạn bè
- Item phụ này là bản clone (`clone $item`) với `contract_max_friend=1`
- Giá trị `amount_payment` của item phụ được tính bằng `calculateBillMaxFriend($totalFriend)` (nhân 12 nếu year)
- Item phụ xuất hiện đồng thời với item chính trong tất cả các nhóm

### 5.3 Quy tắc hủy chuyển khoản

**File**: `app/Http/Controllers/V2/Bill/ListPageController.php:679-745`

Khi hủy chuyển khoản pending, hệ thống cố gắng khôi phục hợp đồng về trạng thái trước đó, dựa trên `reason` field trong `PaymentHistories`:

| reason | Hành động |
|--------|-----------|
| Upgrade từ free | Về lại free, bill_type=month, payment_method=card |
| Upgrade từ standard | Về lại standard |
| Extend contract (year) | Khôi phục `expired_date_contract` về giá trị trước |
| Mặc định | Hủy hoàn toàn |

### 5.4 Quy tắc lọc payment history

**File**: `app/PaymentHistories.php:27-65`

Chỉ đếm/hiển thị bản ghi thanh toán thật sự hợp lệ:
- Card: `type=1` (thu phí thành công) VÀ `type_bill IN(1,2)` (tháng hoặc năm)
- Transfer: `status_transfer=1` (đã nhận được tiền) VÀ `type_bill=3`
- Không tính hoàn tiền: `status_refund=0`
- Đối với year contract: chỉ tính tháng gốc (`parent_month=1`), không tính các tháng phân bổ

### 5.5 Mapping reason → plan (lọc payment history)

**File**: `app/Http/Controllers/Basic/UserController.php:4516-4541`

| Plan | Danh sách reason values |
|------|------------------------|
| standard | `standard_year`, `standard_month`, `standard_year_transfer`, `standard_month_upgrade`, `standard_year_upgrade`, `card_mapping`, `pay_monthly_fee`, `card_mapping_year`, `pay_year_fee`, `pay_year_fee_extend_standard` |
| pro | `pro_year`, `pro_month`, `pro_year_transfer`, `pro_month_upgrade_standard`, `pro_month_upgrade_enterprise`, `pro_month_upgrade_free`, `pro_year_upgrade_standard`, `pro_year_upgrade_enterprise`, `pro_year_upgrade_free`, `pro_year_upgrade_enterprise_2`, `pro_year_upgrade_free_2`, `pay_year_fee_extend_pro`, `pay_pro_monthly_fee`, `pay_pro_year_fee` |
| enterprise | `enterprise_year`, `enterprise_month`, `enterprise_year_transfer`, `enterprise_pro_year_transfer`, `enterprise_month_upgrade`, `enterprise_pro_year_upgrade`, `enterprise_year_upgrade`, `enterprise_pro_year_upgrade`, `enterprise_pro_month`, `enterprise_pro_year`, `slot_plus_enterprise_year`, `slot_plus_enterprise_month`, `pay_year_fee_extend_enterprise` |

---

## 6. Authorization (Phân quyền)

### Middleware

| Middleware | Mô tả |
|-----------|-------|
| `basic_access` | Kiểm tra user đã đăng nhập (role 0/1/2/-1) và có quyền truy cập trang. Kiểm tra `checkExistsUserStaffBot()` cho Staff |
| `check_login` | Xác thực đăng nhập đơn giản |
| `check_remember_token` | Xác thực remember token |

**File**: `app/Http/Middleware/BasicAccess.php`

### Phân quyền theo role

**BasicAccess** kiểm tra:
- `role == 1` (Admin) hoặc `role == 0` hoặc `role == -1` hoặc `role == 2` → được phép
- Nếu đang dùng bot invite: chỉ được truy cập các route trong `getRouterBotInvite()`
- Nếu không có bot active trong session và route không trong `access_route_no_bot`: redirect về adminIndex

### Phân quyền theo dữ liệu

**`getListBotIdStaffManagement($userId, 'pointSettings')`**: Lấy danh sách bot ID mà user được phép truy cập trong chức năng `pointSettings`. Staff chỉ thấy hợp đồng của các bot họ được phân quyền.

---

## 7. Events / Listeners

Không phát hiện event/listener pattern trực tiếp trong feature này. Thay vào đó sử dụng `BotLifeCycle::addState()` để ghi log lịch sử.

---

## 8. Ghi chú quan trọng

### 8.1 Stripe Integration (deprecated)

Hệ thống có code Stripe còn tồn tại trong `PointSettingController` (import `StripePayment`) nhưng có dấu hiệu đang migrate sang Univapay. Các bot có `stripe_customer_id` vẫn được lấy trong `BotContracts::getBotNeedChargeByStripe()` — khả năng vẫn còn bot cũ dùng Stripe.

### 8.2 Background Jobs liên quan

Feature này có nhiều background jobs:
- Job auto-charge thẻ card (hàng tháng/năm) qua Univapay
- Job hủy hợp đồng quá hạn
- Job kiểm tra chuyển khoản pending

Chi tiết nên được phân tích trong `job-spec.md` của Spring Boot.

### 8.3 Tables liên quan (cần mapping trong db-spec)

- `bot_contracts` — bảng chính
- `bot_slots` — liên kết contract ↔ bot
- `payment_histories` — lịch sử thanh toán
- `bot_life_cycles` — lịch sử sự kiện
- `bot_card_bill_friend` — thanh toán theo số bạn bè
- `subcard_bot_contracts` — thẻ phụ
- `bots` — thông tin bot
- `users` — thông tin admin/user

### 8.4 Helper functions

Nhiều logic phụ thuộc vào global helper functions:
- `getBotId()` — lấy bot ID hiện tại từ session
- `getCurrentUser()` — lấy user ID hiện tại
- `getListBotIdStaffManagement($userId, $permission)` — lấy list bot theo quyền
- `calculateBillMaxFriend($totalFriend)` — tính phí theo số bạn bè
- `calculateSaleEnterprise($basicFee, $contractType, $billType, $numberSlot)` — tính phí enterprise
- `getBotByContractId($botContractId)` — lấy bot từ contract ID

**Độ tin cậy**: Cao — observed từ source code trực tiếp
