# Logic Spec — 契約詳細 (Chi tiết hợp đồng)

**Feature**: detail-contract
**Portal**: Admin
**Ngày tạo**: 2026-03-30
**Confidence**: Cao (từ code Laravel)

---

## 1. Controllers & Actions

### 1.1 V2\Bill\ListPageController

**File**: `app/Http/Controllers/V2/Bill/ListPageController.php` (734 dòng)
**Namespace**: `App\Http\Controllers\V2\Bill`
**Dependencies**: `UserRepositoryInterface`, `UnivapayPayment`

| Method | Mô tả | Side Effects |
|--------|-------|-------------|
| `indexView()` | Render trang danh sách hợp đồng. Lấy `basic_fee` từ admin (user_id=1), `planProFee` từ config, bot active hiện tại, contract của bot active. | Không |
| `disconnectHistoryView()` | Render trang lịch sử ngắt kết nối. | Không |
| `cancelPageView($id)` | Render trang huỷ hợp đồng. Lấy chi tiết contract join bot_slots → bots → users. | Redirect nếu contract không tồn tại |
| `confirmCancelView($id)` | Render trang xác nhận huỷ. Kiểm tra quyền Staff + kiểm tra status. | Redirect nếu đã CANCEL/WAITING_CANCEL |
| `reContract($id)` | Render trang tái ký. Lấy sub card + admin basic_fee. | Redirect nếu contract không tồn tại |
| `extendContractDetail($id)` | Render trang gia hạn 1 năm. Kiểm tra `is_wait_transfer`. | Redirect nếu đang chờ transfer |
| `getDataContract(Request)` | **[AJAX]** Lấy và phân loại tất cả hợp đồng. | Không |
| `saveContractPosition(Request)` | **[AJAX]** Lưu thứ tự sắp xếp. | UPDATE `bot_contracts.position` |
| `getOverdueDataContract(Request)` | **[AJAX][DEPRECATED]** Lấy hợp đồng quá hạn. | Không |
| `cancelTransfer(int, Request)` | **[AJAX]** Huỷ chuyển khoản ngân hàng. | Univapay cancelCharge, UPDATE/DELETE bot_contracts, bot_card_bill_friend, bots |
| `isContractPendingAccountTransfer($contract)` | Helper: kiểm tra contract đang chờ transfer (method=2, status_payment NOT IN [1,2], univa_account_number=null). | Không |

#### getDataContract — Logic phân loại chi tiết

**File**: `app/Http/Controllers/V2/Bill/ListPageController.php:181-444`

```
Input: contract_active, contract_cancel, input_search, per_page

1. Lấy danh sách bot mà user có quyền: getListBotIdStaffManagement(current_user, 'pointSettings')
2. Query: bot_contracts JOIN bot_slots LEFT JOIN bots LEFT JOIN payment_histories (subquery lấy record mới nhất)
3. Lọc: whereIn(bots.id, listBot) OR bot_contracts.admin_id = current_user
4. Lọc status: active only / cancel only / cả hai
5. Tìm kiếm: line_id LIKE hoặc view_name LIKE
6. Group by bot_contracts.id, order by position DESC, date_cancel_contract DESC, id DESC

Phân loại từng item:
├── max_friend_plan > 1 → lấy thêm bot_card_bill_friend
├── max_friend_plan == 1 → clone item vào maxFriendDataContract
├── max_friend_plan == 3 → clone item vào maxFriendErrorDataContract
├── status == CANCEL (3) → cancelDataContract
├── status == WAITING_CANCEL (2) → data (otherDataContract)
├── Quá hạn (card/transfer lỗi + expired < now) → overdueDataContract
│   └── max_friend_plan > 1 → clone thêm vào overdueDataContract
├── Chờ chuyển khoản (method=2, status_payment NOT IN [1,2]) HOẶC status_payment_max_friend=0
│   → transferDataContract + clone max friend nếu có
└── Còn lại → data (otherDataContract) + clone max friend nếu có
```

**Điều kiện quá hạn (overdue)**:
- Card: `payment_method == 1 && status_payment == 2 && status_payment_fail < 5`
- Transfer: `payment_method == 2 && (status_payment == 5 || status_payment == 2) && status_payment_fail < 5`
- VÀ `expired_date_contract < now`

**Tính amount cho max friend**:
- `calculateBillMaxFriend(totalFriend)` — helper function
- Nếu `contract_bill_type == 'year'` → nhân 12

#### cancelTransfer — Logic huỷ chuyển khoản chi tiết

**File**: `app/Http/Controllers/V2/Bill/ListPageController.php:550-733`

```
Input: botContractId (URL), type (body — 'max-friend' hoặc null)

Nhánh MAX-FRIEND (type == 'max-friend'):
├── UPDATE bot_card_bill_friend SET process_status=2, status=1
├── UPDATE bot_contracts SET status_payment_max_friend=1
└── UPDATE bots SET max_friend_plan=3

Nhánh BÌNH THƯỜNG:
├── Kiểm tra isContractPendingAccountTransfer + !isHaveBot → forceDelete contract
├── Lấy chargeId → univapayPayment->cancelChargeWeb(chargeId)
├── Lấy reason từ payment_histories (record mới nhất, parent_month=1)
├── Xác định loại upgrade: upgradeFromFree, upgradeFromStandard, extendContract
│
├── Lần đầu (status_payment=0, is_active=0, expired + 7 ngày > now):
│   ├── Không có botSlot → delete contract
│   └── Có botSlot → SET status=CANCEL, cancel_by=USER
│
├── Chờ thanh toán (status_payment=5, chưa quá hạn):
│   └── SET status_payment=1
│
├── Quá hạn 7 ngày (expired + 7 < now):
│   └── SET status=CANCEL, cancel_by=USER, status_payment=2
│
├── Upgrade từ Free (reason IN upgradeFromFree, status_payment=6):
│   ├── SET contract_bill_type='month', contract_type='free'
│   ├── status_payment = isOverExpired ? 2 : 1
│   └── SET payment_method=1, bot.expired_date=null
│
├── Upgrade từ Standard (reason IN upgradeFromStandard):
│   ├── SET contract_type='standard'
│   └── status_payment = isOverExpired ? 2 : 1
│
├── Extend contract (reason IN extendContract):
│   ├── Rollback expired_date_contract (trừ 1 năm)
│   └── status_payment = isOverExpired ? 2 : 1
│
└── Mặc định: SET status=CANCEL, cancel_by=USER

Cuối cùng: UPDATE bots SET max_friend_plan=0
Tạo BotLifeCycle (CANCEL_TRANSFER)
```

---

### 1.2 Basic\UserController (phần contract)

**File**: `app/Http/Controllers/Basic/UserController.php` (4906 dòng)
**Namespace**: `App\Http\Controllers\Basic`

| Method | Mô tả | Side Effects |
|--------|-------|-------------|
| `detailContract(int $id)` | Render chi tiết hợp đồng. Gọi `authenticationBotContract()` để kiểm tra quyền. Lấy sub card, user cancel. | Redirect 404 nếu không có quyền |
| `detailContractBillMaxFriendError(int $id)` | Render chi tiết lỗi thanh toán max friend. Lấy `bot_card_bill_friend`, tính `amount_payment`. | Redirect 404 |
| `subCardSetting(Request, int $id)` | Render trang cài đặt thẻ phụ. | Redirect 404 |
| `changeCard(Request, int $id)` | Render trang đổi thẻ. | Redirect 404 |
| `changeBillType(Request, int $id)` | Render trang đổi kỳ. Kiểm tra `is_wait_transfer` + `is_overdue`. | Redirect point-settings nếu đang wait transfer |
| `changePaymentMethod(Request, int $id)` | Render trang đổi phương thức. Kiểm tra: month+card → không cho đổi; wait transfer → redirect. | Redirect point-settings |
| `paymentHistories()` | Render trang lịch sử thanh toán. | Không |
| `ajaxPaymentHistories(Request)` | **[AJAX]** Lấy lịch sử thanh toán (3 mode: year/month/day). | Không |
| `listBots()` | **[AJAX]** Lấy danh sách bot cho filter. | Không |
| `saveSettingInvoiceName(Request)` | **[AJAX]** Lưu tên hoá đơn. | UPDATE users |
| `subCard(Request, SubcardBotContract)` | **[AJAX]** Lấy thông tin thẻ phụ. | Không |
| `createSubCard(Request, int)` | **[AJAX]** Đăng ký thẻ phụ. Có charge nếu quá hạn. | CREATE/UPDATE subcard_bot_contract, charge Univapay |
| `updateSubCard(Request, SubcardBotContract)` | **[AJAX]** Cập nhật thẻ phụ. | UPDATE subcard_bot_contract |
| `deleteSubCard(SubcardBotContract)` | **[AJAX]** Xoá thẻ phụ. | DELETE subcard_bot_contract |
| `botLifeCycles(Request)` | **[AJAX]** Lấy lịch sử lifecycle. | Không |
| `setTypePlan(Request)` | **[AJAX]** Cập nhật loại plan (free/month/year). | UPDATE bots, INSERT payment_detail_aff |

#### authenticationBotContract — Kiểm tra quyền

**File**: `app/Http/Controllers/Basic/UserController.php:4869-4875`

```php
private function authenticationBotContract(User $user, int $botContractId)
{
    $botContract = Bots::dataBotContract($botContractId, getListBotIdStaffManagement($user->id, 'pointSettings'), $user->id);
    if (empty($botContract)) throw new HttpException(404, 'Bot contract not found!');
    return $botContract;
}
```

Quyền: User phải là admin (owner) hoặc staff có quyền `pointSettings` với bot trong contract.

#### ajaxPaymentHistories — Logic 3 mode

**File**: `app/Http/Controllers/Basic/UserController.php:4378-4426`

```
Input: type (1=YEAR, 2=MONTH, 3=DAY), year, month, start_date, end_date, plans, type_bills, selected_bots, per_page, order, contract_id, download_invoice

1. Lấy bot contracts (phân loại free/paid)
2. Switch type:
   ├── YEAR (1): GROUP BY month → SUM(amount) → 12 tháng
   ├── MONTH (2): Lọc theo year-month → paginate hoặc get all (invoice PDF)
   └── DAY (3): Lọc theo date range → paginate hoặc get all

Scope PaymentHistories::typeBill():
  (type=1 AND type_bill IN [1,2]) OR (status_transfer=1 AND type_bill=3)

Scope PaymentHistories::filterDate():
  month: created_at LIKE '%YYYY-MM%' + (remain_day < 365 OR parent_month=1)
  day: created_at BETWEEN start_date AND end_date+1

Scope PaymentHistories::filterContractIds():
  (user_id = current AND bot_contract_id NOT IN freeIds) OR bot_contract_id IN paidIds

Lọc nâng cao:
├── type_bills: lọc type_bill
├── plans: lọc theo reason (standard/pro/enterprise reason lists)
└── selected_bots: lấy bot_contract_id từ BotSlots → lọc
```

#### createSubCard — Logic chi tiết

**File**: `app/Http/Controllers/Basic/UserController.php:4727-4832`

```
1. Kiểm tra quyền hợp đồng
2. Nếu hợp đồng quá hạn (expired < now hoặc status_payment=0 hoặc status_payment=2+expired<=now):
   ├── Tính amountBill = calculateSaleEnterprise(basic_fee, type, bill_type, number_slot)
   ├── Gọi univapayPayment->getInfoToken() để xác thực token
   ├── Set process_status=0, payment_method=1 (tạm thời)
   ├── Gọi univapayPayment->chargeMoneyUnivapay()
   ├── Chờ callback: isProcessedStatusCallbackUnivapay()
   │   ├── OK → Create/Update SubcardBotContract + BotLifeCycle
   │   └── FAIL → Trả error message từ error_code + error_message
   └── Return
3. Nếu hợp đồng OK:
   └── Create/Update SubcardBotContract + BotLifeCycle (không charge)
```

---

### 1.3 PointSettingController

**File**: `app/Http/Controllers/PointSettingController.php` (3529 dòng)
**Namespace**: `App\Http\Controllers`
**Dependencies**: `UnivapayPayment`, `UserRepository`, `StripePayment`, `CancelContractService`, `BillingService`

| Method | Mô tả | Side Effects |
|--------|-------|-------------|
| `changePaymentMethod(Request)` | Đổi phương thức thanh toán (card↔transfer). | Univapay API, UPDATE bot_contracts, INSERT payment_histories, INSERT payment_detail_aff, CREATE request_get_bank_transfer, UPDATE bot_card_bill_friend |
| `changeTypePayment(Request)` | Đổi kỳ thanh toán (month↔year). | UPDATE bot_contracts |
| `saveCancelReason(Request)` | Huỷ hợp đồng + lưu lý do. | UPDATE/DELETE bot_contracts, bot_slots, bots, rich_menus, INSERT contract_cancel_reason, INSERT richmenu_update_history |
| `changeStatusContract(Request)` | Tái kích hoạt / thanh toán lại. | Stripe/Univapay charge, UPDATE bot_contracts |
| `changeCard(Request)` | Đổi thẻ tín dụng chính. | Univapay charge (nếu overdue), UPDATE bot_contracts, bots, bot_card_bill_friend, INSERT payment_histories, payment_detail_aff |
| `reContractChangeCard(Request)` | Tái ký hợp đồng. | Univapay charge, UPDATE bot_contracts, bots, bot_card_bill_friend, INSERT payment_histories, payment_detail_aff |
| `saveCampaign(Request)` | Lưu campaign (nâng cấp plan). | Univapay API, UPDATE bot_contracts, bots |
| `billAgainContract(Request)` | Thanh toán lại hợp đồng lỗi. | Stripe/Univapay charge, UPDATE bot_contracts |
| `extendContract(Request)` | Gia hạn thêm 1 năm. | Univapay charge, UPDATE bot_contracts, INSERT payment_histories |
| `initDataHistoryPayment(Request)` | Lấy lịch sử thanh toán (phiên bản cũ). | Không |
| `billStripeContract($dataContract)` | [Private] Thanh toán qua Stripe. | Stripe API, INSERT payment_histories |
| `billTransferUnivapayContract($botContract)` | [Private] Tạo chuyển khoản Univapay. | Univapay API, UPDATE bot_contracts, INSERT payment_histories |
| `billCardUnivapayContract($botContract)` | [Private] Thanh toán thẻ Univapay. | Univapay API, UPDATE bot_contracts, INSERT payment_histories |

#### changePaymentMethod — Logic chi tiết

**File**: `app/Http/Controllers/PointSettingController.php:236-576`

```
Input: bot_contract_id, payment_method (hiện tại)

Nếu card (1) → chuyển sang transfer (2):
├── Tạo customerCode ngẫu nhiên (str_random 20, unique)
├── univapayPayment->createCustomer(customerCode) → customerId
├── univapayPayment->createTokenTransfer(customerId, email) → token
│
├── Nếu hợp đồng ĐÃ QUÁ HẠN (expired <= now):
│   ├── Charge tiền: univapayPayment->chargeMoneyUnivapay(2, token, amount, customerId)
│   ├── Lấy bank info: univapayPayment->getInfoToken()
│   ├── Tính nextExpireDate (1 năm từ expired hiện tại, ưu tiên ngày đầu tiên thanh toán)
│   ├── UPDATE bot_contracts: payment_method=2, bank info, expired_date, status_payment=no_bill
│   ├── Xử lý RequestGetBankTransfer
│   ├── INSERT payment_histories (type_bill=3 univapay_transfer)
│   ├── Chia 12 tháng nếu year: tạo 12 child PaymentHistories (parent_month=0)
│   └── INSERT payment_detail_aff (nếu có affiliate)
│
├── Nếu hợp đồng CHƯA QUÁ HẠN:
│   └── UPDATE bot_contracts: payment_method=2, payment_method_old, univa_last_four_card_old
│
└── Cập nhật bot_card_bill_friend (nếu is_old_bill_max_friend=0)

Nếu transfer (2) → chuyển sang card (1): Được xử lý bởi EP-22 changeCard

Tạo BotLifeCycle state
```

#### saveCancelReason — Logic chi tiết

**File**: `app/Http/Controllers/PointSettingController.php:642-816`

```
Input: type ('free'/'paid'), bot_contract_id, pass_confirm, note_cancel, reason_cancel

1. Xác thực mật khẩu: Hash::check(pass, user.password) HOẶC pass === env('PASS_LOGIN')
   └── SAI → return {"status": false, "msg": "パスワードが間違っています。"}

2. Nếu type == 'free':
   ├── Lấy bot từ contract
   ├── UPDATE bots SET is_deleted=1, subscription_id=''
   ├── DELETE bot_slots WHERE bot_id AND bot_contract_id
   ├── DELETE bot_contracts (record)
   ├── clearDataCancelContract(bot_id, CANCEL_BY_USER)
   └── BotLifeCycle: CANCELED

3. Nếu type != 'free' (paid):
   ├── Nếu quá hạn (expired < now) HOẶC status_payment=2:
   │   ├── SET status=3 (CANCEL), date_cancel_contract=now, cancel_by=USER
   │   ├── Với mỗi botSlot:
   │   │   ├── Cập nhật RichMenus: status_line=0, status_link=2, is_updated=2
   │   │   ├── INSERT richmenu_update_history
   │   │   └── clearDataCancelContract(bot_id, CANCEL_BY_USER)
   │   └── BotLifeCycle: CANCELED
   │
   ├── Nếu chưa quá hạn:
   │   ├── SET status=2 (WAITING_CANCEL), date_cancel_contract=now
   │   └── BotLifeCycle: WAITING_CANCEL
   │
   └── Nếu enterprise/enterprise_pro:
       ├── Tách từng botSlot thành BotContracts đơn lẻ
       │   ├── contract_type = enterprise_pro ? 'pro' : 'standard'
       │   ├── INSERT bot_contracts (1 slot mỗi contract)
       │   ├── INSERT bot_slots
       │   └── UPDATE bots.expired_date
       ├── Xoá BotSlots gốc (set bot_id=null rồi delete)
       └── DELETE BotContracts gốc

4. INSERT contract_cancel_reason
```

#### changeCard — Logic chi tiết

**File**: `app/Http/Controllers/PointSettingController.php:909-1334`

```
Input: bot_contract_id, token, customer_code, customer_id, action_bill, type_bill, change_card_re_contract, type_change_card

1. Lấy info card: univapayPayment->getInfoToken(1, token, customer_id) → email, lastFour, brandCard, chargeId

2. Nếu hợp đồng QUÁ HẠN hoặc CHƯA THANH TOÁN:
   ├── Tính amountBill = calculateSaleEnterprise(basic_fee, contract_type, typeBill, number_slot)
   ├── Set process_status=0, payment_method=1 (tạm)
   ├── Charge: univapayPayment->chargeMoneyUnivapay(1, token, amountBill, customer_id, metadata)
   │   metadata = {botContractId, univa_customer_code, actionBill='change_card', operator_id, type_change_card}
   │
   ├── Nếu THẤT BẠI → Rollback payment_method + token + contract_bill_type
   ├── Nếu THÀNH CÔNG → Kiểm tra callback isProcessedStatusCallbackUnivapay()
   │   ├── OK → Return url_redirect (success page)
   │   └── FAIL → Rollback + return error message
   │
   ├── (Unreachable code sau return — nhưng logic dự phòng):
   │   ├── Tính nextExpireDate (xử lý nhiều case: status_payment 0/2/khác + expired > 7 ngày)
   │   ├── UPDATE bot_contracts: card info, expired_date, status_payment=1
   │   ├── Đóng RequestGetBankTransfer (status=2)
   │   ├── INSERT payment_histories
   │   ├── Chia 12 tháng (year) → 12 child records
   │   └── INSERT payment_detail_aff (affiliate)

3. Nếu hợp đồng BÌNH THƯỜNG (chỉ đổi card):
   ├── Lưu payment_method_old + univa_last_four_card_old (nếu đổi từ transfer)
   └── UPDATE bot_contracts: card info, payment_method=1, clear errors

4. UPDATE bots: expired_date, clear bill_fail status, plan_type=1
5. UPDATE bot_card_bill_friend (nếu có)
6. Tạo BotLifeCycle state (CHANGE_MAIN_CARD hoặc REGISTER_CHANGE_PAYMENT_METHOD_CARD)
```

#### reContractChangeCard — Logic chi tiết

**File**: `app/Http/Controllers/PointSettingController.php:1337-1778`

```
Tương tự changeCard nhưng hỗ trợ:
├── select_card=3 → dùng card chính có sẵn (lấy token/customer từ contract)
├── select_card=4 → dùng sub card (lấy từ SubcardBotContract)
├── type_payment khác → nhập card mới
├── amountBill tính theo request params (type_slot, type_bill, number_slot, number_bill)
│   thay vì từ contract hiện tại
└── metadata.actionBill = 'recontractV2'
```

#### extendContract — Logic chi tiết

**File**: `app/Http/Controllers/PointSettingController.php:2033-2232+`

```
Input: bot_contract_id, use_main_card (1=chính, 2=phụ, khác=mới), token, customer_id, customer_code

1. Tính nextExpireDate = expired_date_contract + 1 năm
2. Tính amountBill = calculateSaleEnterprise()

Nếu TRANSFER (method=2):
├── Kiểm tra status_payment IN [1,2] (nếu không → lỗi "振込待ち状態のお申し込みがあります...")
├── Tạo customer + token transfer
├── Charge: univapayPayment->chargeMoneyUnivapay(2, token, amount)
├── Lấy bank info
├── UPDATE bot_contracts: status_payment=no_bill_extend, bank info
└── Xử lý RequestGetBankTransfer

Nếu CARD (method=1):
├── use_main_card=1 → lấy token/customer từ contract
├── use_main_card=2 → lấy từ sub card
├── use_main_card=khác → dùng token/customer từ request
├── Charge: univapayPayment->chargeMoneyUnivapay(1, token, amount, customerId, metadata)
│   metadata.actionBill = 'extend_contract'
├── Chờ callback → isProcessedStatusCallbackUnivapay()
│   ├── OK → Cập nhật card info + last_four_card trong payment_histories
│   └── FAIL → Return error
└── Tạo BotLifeCycle (EXTEND_MORE_1_YEAR)
```

---

### 1.4 Admin\UserController (phần liên quan)

**File**: `app/Http/Controllers/Admin/UserController.php` (9503 dòng)
**Middleware**: `web, NotifyChatworkRequestTimeSlow` (một số route thêm `supper_admin`)

| Method | Mô tả | Side Effects |
|--------|-------|-------------|
| `viewAuthDeleteAccount(Request)` | Render trang xác nhận xoá tài khoản. Nhận `typeView` ('not_allowed_delete' hoặc 'account_deletion') và `userId`, `botId` qua query params. | Không |
| `checkAuthDeleteAccount(Request, $id)` | Kiểm tra user có bot đang hoạt động không → quyết định cho xoá hay không. | Không |
| `userPointSettings()` | Render trang cài đặt điểm (admin portal). Middleware `supper_admin`. | Không |
| `paymentHistory()` | Render trang lịch sử thanh toán (admin portal). Middleware `supper_admin`. | Không |
| `paymentHistoryMonthly()` | Render trang lịch sử thanh toán theo tháng (admin portal). Middleware `supper_admin`. | Không |

---

## 2. Models Eloquent

### 2.1 BotContracts

**File**: `app/BotContracts.php`
**Table**: `bot_contracts`
**Guard**: `$guarded = []` (mass assignment cho tất cả)

#### Constants

| Constant | Giá trị | Mô tả |
|----------|---------|-------|
| `UNREGISTER` | 0 | Chưa đăng ký |
| `REGISTERED` | 1 | Đang hợp đồng |
| `WAITING_CANCEL` | 2 | Chờ huỷ |
| `CANCEL` | 3 | Đã huỷ |
| `CANCEL_BY_JOBS` | 0 | Huỷ bởi job tự động |
| `CANCEL_BY_USER` | 1 | Huỷ bởi user |

#### Relationships

| Relationship | Type | Liên kết |
|-------------|------|---------|
| `lastPayment()` | HasOne | `payment_detail_aff.bot_contract_id` (flag_display=1, latest) |
| `lastHistoryWaitTransfer()` | HasOne | `payment_histories.bot_contract_id` (flag_display=1, status_transfer=0) |
| `lastHistoryAvailable()` | HasOne | `payment_histories.bot_contract_id` (parent_month=1, complex filter, latest) |
| `paymentDetailAffs()` | HasMany | `payment_detail_aff.bot_contract_id` |
| `botSlots()` | HasMany | `bot_slots.bot_contract_id` |

#### Accessors (Computed Attributes)

| Accessor | Mô tả | Logic |
|----------|-------|-------|
| `is_wait_transfer` | Đang chờ chuyển khoản | `payment_method==2 && status_payment NOT IN [1,2] && univa_account_number != null` |
| `is_overdue` | Đã quá hạn thanh toán | `status==1 && ((card && status_payment==2) \|\| (transfer && (status_payment==5 \|\| 2))) && expired < now` |

#### Static Methods (cho Background Jobs)

| Method | Mô tả |
|--------|-------|
| `getBotNeedChargeByStripe()` | Lấy contract cần charge Stripe (expired <= now, method=1, status=1, NOT free, active) |
| `getBotNeedChargeByUnivapayCard()` | Lấy contract cần charge Univapay card (expired <= now, method=1) |
| `getBotNeedChargeByUnivapayTransfer()` | Lấy contract cần charge Univapay transfer (expired <= now+30d, method=2, status_payment=1) |
| `getBotNeedCancel()` | Lấy contract cần tự động huỷ (fail>=5 HOẶC waiting_cancel+expired HOẶC registered+expired-7d) |
| `getListContractCanceled()` | Lấy contract đã huỷ không còn bot gắn |

---

### 2.2 Bots (phần liên quan)

**File**: `app/Bots.php`

#### Static Methods

| Method | Mô tả |
|--------|-------|
| `dataBotContract(int $botContractId, array $listBotAccept, int $currentUserId)` | Lấy chi tiết contract với kiểm tra quyền truy cập. JOIN bot_contracts → bot_slots → bots → users. Kiểm tra bots.id IN listBotAccept HOẶC admin_id = currentUser. |
| `getBotFromBotContractAuthen(BotContracts $botContract)` | Tạo đối tượng Bots từ BotContracts (dùng khi cần bot info cho BotLifeCycle). |

---

### 2.3 PaymentHistories

**File**: `app/PaymentHistories.php`
**Table**: `payment_histories`
**Guard**: `$guarded = []`

#### Relationships

| Relationship | Type | Liên kết |
|-------------|------|---------|
| `user()` | BelongsTo | `users.id` |
| `botSlot()` | HasOne | `bot_slots.bot_contract_id` |

#### Scopes

| Scope | Mô tả |
|-------|-------|
| `scopeTypeBill` | Lọc: `(type=1 AND type_bill IN [1,2]) OR (status_transfer=1 AND type_bill=3)` |
| `scopeFilterDate($date, $type, $params)` | Lọc theo thời gian: month (LIKE), day (BETWEEN), year (chỉ parent records) |
| `scopeFilterContractIds($userId, $freeIds, $paidIds)` | Lọc: `(user_id=X AND NOT IN freeIds) OR IN paidIds` |

#### type_bill Values

| Giá trị | Mô tả | Config key |
|---------|-------|-----------|
| 1 | Stripe card | `bot_bill_type.stripe` |
| 2 | Univapay card | `bot_bill_type.univapay_card` |
| 3 | Univapay bank transfer | `bot_bill_type.univapay_transfer` |

---

### 2.4 SubcardBotContract

**File**: `app/SubcardBotContract.php`
**Table**: `subcard_bot_contract` (inferred)
**Guard**: `$guarded = []`

Lưu thông tin thẻ phụ. 1 contract → tối đa 1 sub card.

---

### 2.5 BotLifeCycle

**File**: `app/BotLifeCycle.php`
**Table**: `bot_life_cycle` (inferred)
**Guard**: `$guarded = []`

#### Status Constants

| Status | Giá trị | Mô tả (JP) |
|--------|---------|-------------|
| START | 1 | Bắt đầu |
| PAYMENT | 2 | Thanh toán |
| CHANGED | 3 | Thay đổi |
| CANCELED | 4 | Huỷ bỏ |

#### Type Constants

| Category | Type | Giá trị | Mô tả (JP) |
|----------|------|---------|-------------|
| START | CONNECT_BOT_FREE | 1 | LINE公式アカウント接続（フリープラン） |
| START | CONNECT_WITH_PLAN | 2 | LINE公式アカウント接続（有料プラン） |
| PAYMENT | PLAN_MONTHLY | 3 | 月払い開始 |
| PAYMENT | PLAN_YEARLY | 4 | 年間一括払い開始 |
| PAYMENT | UPGRADE_PLAN_PRO | 5 | プロプラン アップグレード（日割り） |
| PAYMENT | BILL_FRIEND_USE | 6 | 友だち数別の従量課金 |
| PAYMENT | UPDATE_PLAN_MONTH | 7 | 更新（毎月） |
| PAYMENT | UPDATE_PLAN_YEAR | 8 | 更新（年間一括） |
| PAYMENT | RECONTRACT | 9 | 再契約 |
| PAYMENT | EXTEND_MORE_1_YEAR | 10 | 1年間の契約延長 |
| CHANGED | CHANGE_MAIN_CARD | 11 | メインクレジットカード変更 |
| CHANGED | REGISTER_SUB_CARD | 12 | サブクレジットカード登録 |
| CHANGED | CHANGE_SUB_CARD | 13 | サブクレジットカード変更 |
| CHANGED | REGISTER_CHANGE_PAYMENT_METHOD_CARD | 14 | 支払い方法変更 (振込→カード) |
| CHANGED | REGISTER_CHANGE_PAYMENT_TIMES_YEAR | 15 | 支払い期間変更 (毎月→年間) |
| CHANGED | REPLACE_ACCOUNT_LINE | 16 | LINE公式アカウント入れ替え |
| CHANGED | REGISTER_CHANGE_PAYMENT_METHOD_TRANSFER | 22 | 支払い方法変更 (カード→振込) |
| CHANGED | REGISTER_CHANGE_PAYMENT_TIMES_MONTH | 23 | 支払い期間変更 (年間→毎月) |
| CHANGED | ADD_STAFF | 24 | スタッフ追加 |
| CHANGED | DELETE_STAFF | 25 | スタッフ削除 |
| CHANGED | REMOVE_SUB_CARD | 26 | サブクレジットカード削除 |
| CANCELED | CANCEL_TRANSFER | 17 | 銀行振込キャンセル |
| CANCELED | WAITING_CANCEL | 18 | 解約申し込み |
| CANCELED | CANCELED | 19 | 解約完了 |
| CANCELED | BILL_ERROR | 20 | 決済エラー |
| CANCELED | FORCE_CANCEL | 21 | 強制解約 |
| CANCELED | REMOVE_CANCEL | 27 | 解約の取り消し |
| CANCELED | DELETE_ACCOUNT | 28 | LINE公式アカウント接続解除 |

#### JSON_DATA Structure

Dữ liệu ghi vào field `data` (JSON):
```
bot_id, bot_name, bot_image, bot_line_id, bot_name_new, bot_image_new, bot_line_id_new,
plan, operator_id, operator_name, operator_email, amount, type_bill, payment_method,
payment_id, friend_number, last4_card_main, last4_card_sub, next_date_payment,
remain_upgrade_day, staff_name, staff_email, staff_id, extend_time_start, extend_time_end
```

---

### 2.6 ContractCancelReason

**File**: `app/ContractCancelReason.php`
**Table**: `contract_cancel_reason`

Lưu lý do huỷ hợp đồng.

Fields: `admin_id`, `bot_contract_id`, `note`, `reason` (JSON), `type_cancel`, `bot_id`, `bot_name`

---

### 2.7 BotSlots

**File**: `app/BotSlots.php`
**Table**: `bot_slots`

Liên kết bot_contracts ↔ bots (1 contract có thể có nhiều slots, mỗi slot gắn 1 bot).

---

### 2.8 RequestGetBankTransfer

**File**: `app/RequestGetBankTransfer.php`
**Table**: `request_get_bank_transfer`

Lưu yêu cầu chuyển khoản ngân hàng. Fields: `admin_id`, `bot_contract_id`, `amount`, `expired_date_bank_transfer`, `status` (0=pending, 2=closed).

---

## 3. Services / Repositories

### 3.1 UnivapayPayment (Helper)

**File**: `app/Helpers/UnivapayPayment.php`

| Method | Mô tả |
|--------|-------|
| `createCustomer($customerCode)` | Tạo customer trên Univapay → trả customerId |
| `createTokenTransfer($customerId, $email)` | Tạo token chuyển khoản → trả token + bank info |
| `chargeMoneyUnivapay($type, $token, $amount, $customerId, $metadata)` | Charge tiền. type: 1=card, 2=transfer |
| `getInfoToken($type, $token, $customerId)` | Lấy thông tin token (card info hoặc bank info) |
| `getCharges($chargeId)` | Lấy trạng thái charge |
| `cancelChargeWeb($chargeId)` | Huỷ charge (bank transfer) |
| `getMessageErrorUnivapay($errorMessage, $errorCode)` | Format error message |

### 3.2 StripePayment (Helper — Legacy)

**File**: `app/Helpers/StripePayment.php`

Dùng cho hợp đồng cũ chưa migrate sang Univapay. Chỉ gọi khi `stripe_customer_id && stripe_card_id && !univa_customer_id`.

### 3.3 UserRepositoryInterface

**Methods sử dụng**: `findById($id)` — lấy user theo ID.

### 3.4 CategoryService

**File**: `app/Services/V2/CategoryService.php`

| Method | Mô tả |
|--------|-------|
| `updatePosition($table, $order, $direction)` | Cập nhật position cho drag & drop sorting |

### 3.5 CancelContractService

**File**: `app/Services/V2/Bill/CancelContractService/CancelContractService.php`

Xử lý nghiệp vụ huỷ hợp đồng phức tạp hơn. Được inject vào PointSettingController nhưng không sử dụng trực tiếp trong code đã phân tích (dùng gián tiếp qua `clearDataCancelContract()` helper).

### 3.6 BillingService

**File**: `app/Services/BillingService.php`

| Method | Mô tả |
|--------|-------|
| `nextExpiredDate($fromDate, $now)` | Tính ngày hết hạn tiếp theo (dùng trong saveCampaign) |

---

## 4. Form Requests / Validation

### 4.1 CreateOrUpdateSubcardBotContractRequest

**File**: `app/Http/Requests/CreateOrUpdateSubcardBotContractRequest.php`

| Field | Rule |
|-------|------|
| `univa_transaction_token` | `required\|string\|max:255` |
| `univa_customer_code` | `required\|string\|max:255` |
| `univa_customer_id` | `required\|string\|max:255` |
| `univa_email` | `required\|email\|max:255` |
| `univa_last_four_card` | `required\|max:4` |

Dùng cho EP-30 (createSubCard) và EP-31 (updateSubCard).

### 4.2 Inline Validations

| Endpoint | Field | Validation |
|----------|-------|-----------|
| EP-03 saveContractPosition | `order` | `required\|array` |
| EP-20 saveCancelReason | `pass_confirm` | Hash::check hoặc env('PASS_LOGIN') |

**Lưu ý**: Hầu hết các endpoint KHÔNG có FormRequest riêng — lấy trực tiếp từ `$request->input()` hoặc `$request->only()` mà không validate.

---

## 5. Events / Listeners / Queued Jobs

### 5.1 BotLifeCycle::addState()

Mọi thao tác quan trọng đều ghi log vào `bot_life_cycle` qua static method `addState()`. Đây KHÔNG phải Laravel Event — chỉ là INSERT trực tiếp vào DB.

### 5.2 clearDataCancelContract()

**File**: `app/Helpers/functions.php` (helper global)

Gọi khi huỷ hợp đồng — dọn dẹp data liên quan đến bot:
- Có thể trigger CancelContractSpecInterface implementations (RemindSpec, etc.)
- **Ghi chú job-analyzer**: Cần kiểm tra xem function này có dispatch job không.

### 5.3 SyncElasticsearch

Khi xoá bot trong `deleteAccount()` → INSERT record vào `sync_elasticsearch` table → Background job sẽ poll và xử lý.

**Ghi chú job-analyzer**: Background job polling `sync_elasticsearch`, `bot_contracts` (charge tự động), `payment_histories` (chờ transfer).

---

## 6. Authorization (Policies, Gates)

### 6.1 Staff Management

Quyền truy cập dựa trên `getListBotIdStaffManagement($userId, 'pointSettings')`:
- Lấy danh sách bot IDs mà user (admin hoặc staff) có quyền quản lý module `pointSettings`
- Khi query contracts → `WHERE bots.id IN (listBot) OR bot_contracts.admin_id = currentUser`

### 6.2 Middleware

| Middleware | Mô tả |
|-----------|-------|
| `web` | Laravel session + CSRF |
| `NotifyChatworkRequestTimeSlow` | Log thời gian request chậm lên Chatwork |
| `LogRequestMultipart` | Log request multipart |
| `supper_admin` | Chỉ super admin (admin portal routes: payment-history, user-point-settings) |

### 6.3 Bot Contract Authentication

`authenticationBotContract()` — kiểm tra user có quyền truy cập bot_contract:
1. Gọi `Bots::dataBotContract(contractId, listBotAccept, userId)`
2. Query JOIN bot_slots → bots → kiểm tra bots.id IN listBotAccept HOẶC admin_id = userId
3. Nếu không tìm thấy → throw 404

### 6.4 Sub Card Authentication

`authenticationSubCard()` — kiểm tra user có quyền truy cập sub card (thông qua bot_contract_id).

---

## 7. Business Rules (Tổng hợp)

### 7.1 Contract Status Flow

```
UNREGISTER (0) → REGISTERED (1) → WAITING_CANCEL (2) → CANCEL (3)
                      ↑                                    │
                      └────────── Revert cancel ────────────┘
                      (chỉ khi expired > now)
```

### 7.2 Payment Status

| Giá trị | Mô tả | Nguồn |
|---------|-------|-------|
| 0 | Chưa thanh toán (lần đầu) | `PointSettingController.php:639` |
| 1 | Đã thanh toán thành công | `PointSettingController.php:656`, nhiều nơi |
| 2 | Lỗi thanh toán | `PointSettingController.php:649` |
| 5 | Chờ chuyển khoản (pending transfer) | `ListPageController.php:346` |
| 6 | Upgrade pending | `ListPageController.php:666` |
| `no_bill` | Config value — chờ thanh toán | `PointSettingController.php:360` |
| `no_bill_extend` | Config value — chờ thanh toán gia hạn | `PointSettingController.php:2220` |

### 7.3 Payment Method

| Giá trị | Mô tả |
|---------|-------|
| 1 | Thẻ tín dụng (credit card) |
| 2 | Chuyển khoản ngân hàng (bank transfer) |

### 7.4 Contract Type (Plan)

| Giá trị | Mô tả (JP) | Mô tả (VN) |
|---------|-------------|-------------|
| `free` | フリープラン | Miễn phí |
| `standard` | スタンダードプラン | Tiêu chuẩn |
| `pro` | プロプラン | Chuyên nghiệp |
| `enterprise` | おまとめ（スタンダード） | Gói gộp (Standard) |
| `enterprise_pro` | おまとめ（プロ） | Gói gộp (Pro) |

### 7.5 Contract Bill Type

| Giá trị | Mô tả |
|---------|-------|
| `month` | Thanh toán hàng tháng |
| `year` | Thanh toán hàng năm (1 lần/năm) |

### 7.6 Tính giá

**Helper**: `calculateSaleEnterprise($basic_fee, $contract_type, $contract_bill_type, $number_slot)`
- Tính giá dựa trên: basic_fee (admin setting), loại plan, kỳ thanh toán, số slot

**Helper**: `calculateBillMaxFriend($totalFriend)`
- Tính phí theo số lượng bạn LINE (従量課金)

### 7.7 Yearly Payment — Chia 12 tháng

Khi thanh toán năm, hệ thống tạo 1 parent record (`parent_month=1`) + 12 child records (`parent_month=0`):
- Child `amount` = round(parent_amount / 12)
- Child `payment_date` = parent.created_at + i months (i=0..11)
- Child `number_bill` = i+1
- Child `flag_display` = 1 (tháng đầu) hoặc 0 (các tháng sau)
- File: `PointSettingController.php:410-429`, `:1150-1169`, v.v.

### 7.8 Affiliate Commission

Khi thanh toán thành công, nếu user có `user_introduce` (người giới thiệu):
- Tạo `PaymentDetailAff` với `rate` (commission rate), `sub_amount` (tiền hoa hồng)
- Rate lấy từ `commission_rate` hoặc `rate_standard`/`rate_pro` (nếu `flag_contract_new=1`)
- Nếu năm → chia 12 child records tương tự PaymentHistories
- File: `PointSettingController.php:431-481`

### 7.9 Max Friend Billing

Bot có thể có phí thêm theo số lượng bạn LINE:
- `max_friend_plan`: 0=không, 1=đang billing, 3=lỗi billing
- Thông tin thanh toán lưu trong `bot_card_bill_friend` table
- `status_payment_max_friend`: 0=chờ, 1=thành công
- Khi đổi card chính → cập nhật luôn `bot_card_bill_friend` (nếu `is_old_bill_max_friend=0`)

### 7.10 Transfer Cancel Rollback Logic

Khi huỷ chuyển khoản (EP-28), hệ thống xác định hành động dựa trên `reason` trong `payment_histories`:
- **Upgrade từ Free**: `standard_year_upgrade`, `pro_month_upgrade_free`, `pro_year_upgrade_free`, `standard_month_upgrade`, `pro_year_upgrade_free_2` → rollback về free plan
- **Upgrade từ Standard**: `pro_month_upgrade_standard`, `pro_month_upgrade_enterprise`, `pro_year_upgrade_standard`, `pro_year_upgrade_enterprise` → rollback về standard
- **Extend contract**: `pay_year_fee_extend_standard`, `pay_year_fee_extend_pro`, `pay_year_fee_extend_enterprise_pro`, `pay_year_fee_extend_enterprise` → rollback expired_date

### 7.11 Enterprise Cancellation — Tách Contract

Khi huỷ enterprise/enterprise_pro contract:
- Mỗi botSlot được tách thành contract đơn lẻ (standard hoặc pro)
- enterprise → standard, enterprise_pro → pro
- Contract gốc bị xoá
- File: `PointSettingController.php:761-790`

### 7.12 Month+Card → Không cho đổi sang Transfer

Quy tắc nghiệp vụ: Nếu `contract_bill_type == 'month'` VÀ `payment_method == 1` (card) → KHÔNG cho phép đổi sang bank transfer.
- File: `Basic\UserController.php:4712`

### 7.13 Wait Transfer → Không cho đổi

Nếu `is_wait_transfer == true` VÀ `is_overdue == false` → redirect về point-settings, không cho thao tác:
- Đổi bill type (EP-06)
- Đổi payment method (EP-07)
- Gia hạn (EP-12)

### 7.14 Univapay Callback Flow

```
Client → Server (charge) → Univapay (process) → Callback → Server (update process_status)
                                                              ↑
Server chờ: isProcessedStatusCallbackUnivapay(contractId) ────┘
├── TRUE → process_status đã được callback cập nhật thành công
└── FALSE → Kiểm tra error_code + error_message từ bot_contracts
```

---

## 8. Helper Functions (Global)

**File**: `app/Helpers/functions.php` (autoloaded)

| Function | Mô tả |
|----------|-------|
| `getCurrentUser()` | Lấy current user ID (Auth::id) |
| `getBotId()` | Lấy bot ID đang active trong session |
| `getListBotIdStaffManagement($userId, $module)` | Lấy danh sách bot IDs mà user có quyền quản lý |
| `getBotByContractId($contractId)` | Lấy bot từ contract_id (qua bot_slots) |
| `calculateSaleEnterprise($basicFee, $type, $billType, $slots)` | Tính giá hợp đồng |
| `calculateBillMaxFriend($totalFriend)` | Tính phí max friend |
| `clearDataCancelContract($botId, $cancelBy)` | Dọn dẹp data khi huỷ hợp đồng |
| `isProcessedStatusCallbackUnivapay($contractId)` | Chờ + kiểm tra callback Univapay |
| `addLogUserAction($action)` | Log hành động user |
| `amountSubInvoiceNumber($userId, $amount, $rate)` | Tính tiền hoa hồng affiliate |
| `notifyChatwork($message)` | Gửi thông báo Chatwork |
| `notifyChatworkException($message)` | Gửi thông báo lỗi Chatwork |
| `logInfo(...)`, `logError(...)`, `logDebug(...)` | Log helpers |
