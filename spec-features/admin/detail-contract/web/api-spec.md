# API Spec — 契約詳細 (Chi tiết hợp đồng)

**Feature**: detail-contract
**Portal**: Admin
**Ngày tạo**: 2026-03-30
**Confidence**: Cao (từ code Laravel)

---

## 1. Tổng quan Endpoints

| EP | Method | URL | Controller@Action | Mô tả | Middleware |
|----|--------|-----|-------------------|-------|-----------|
| EP-01 | GET | `/basic/point-settings` | `V2\Bill\ListPageController@indexView` | Trang danh sách hợp đồng | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-02 | POST | `/ajax/point-settings/get-data-contract` | `V2\Bill\ListPageController@getDataContract` | Lấy danh sách hợp đồng (AJAX) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-03 | POST | `/ajax/point-settings/save-contract-position` | `V2\Bill\ListPageController@saveContractPosition` | Lưu thứ tự sắp xếp hợp đồng | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-04 | GET | `/basic/detail-contract/{id}` | `Basic\UserController@detailContract` | Trang chi tiết hợp đồng | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-05 | GET | `/basic/detail-contract/{id}/cancel` | `V2\Bill\ListPageController@confirmCancelView` | Trang xác nhận huỷ hợp đồng | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-06 | GET | `/basic/change-bill-type/{id}` | `Basic\UserController@changeBillType` | Trang đổi loại thanh toán (月→年 / 年→月) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-07 | GET | `/basic/change-payment-method/{id}` | `Basic\UserController@changePaymentMethod` | Trang đổi phương thức thanh toán (card↔transfer) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-08 | GET | `/basic/change-card/{id}/{type?}` | `Basic\UserController@changeCard` | Trang đổi thẻ tín dụng | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-09 | GET | `/basic/sub-card-setting/{id}/{type?}` | `Basic\UserController@subCardSetting` | Trang cài đặt thẻ phụ | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-10 | GET | `/basic/point-settings/cancel/{id}` | `V2\Bill\ListPageController@cancelPageView` | Trang huỷ hợp đồng (hiển thị thông tin trước khi huỷ) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-11 | GET | `/basic/re-contract/{id}` | `V2\Bill\ListPageController@reContract` | Trang tái ký hợp đồng | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-12 | GET | `/basic/detail/extend-contract/{id}` | `V2\Bill\ListPageController@extendContractDetail` | Trang gia hạn hợp đồng (thêm 1 năm) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-13 | GET | `/basic/disconnect-history` | `V2\Bill\ListPageController@disconnectHistoryView` | Trang lịch sử ngắt kết nối LOA | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-14 | GET | `/basic/payment-history` | `Basic\UserController@paymentHistories` | Trang lịch sử thanh toán | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-15 | GET | `/ajax/payment-history` | `Basic\UserController@ajaxPaymentHistories` | Lấy dữ liệu lịch sử thanh toán (AJAX) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-16 | GET | `/ajax/payment-history/filter-bots` | `Basic\UserController@listBots` | Lấy danh sách bot để lọc lịch sử thanh toán | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-17 | POST | `/ajax/payment-history/setting-invoice-name` | `Basic\UserController@saveSettingInvoiceName` | Lưu tên hoá đơn (invoice name) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-18 | POST | `/ajax/point-settings/change-payment-method` | `PointSettingController@changePaymentMethod` | Đổi phương thức thanh toán (card↔transfer) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-19 | POST | `/ajax/point-settings/change-type-payment` | `PointSettingController@changeTypePayment` | Đổi kỳ thanh toán (月↔年) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-20 | POST | `/ajax/point-settings/save-cancel-reason` | `PointSettingController@saveCancelReason` | Lưu lý do huỷ hợp đồng + thực hiện huỷ | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-21 | POST | `/ajax/point-settings/change-status-contract` | `PointSettingController@changeStatusContract` | Thay đổi trạng thái hợp đồng (tái kích hoạt / thanh toán lại) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-22 | POST | `/ajax/point-settings/change-card` | `PointSettingController@changeCard` | Đổi thẻ tín dụng chính + thanh toán nếu quá hạn | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-23 | POST | `/ajax/point-settings/recontract-change-card` | `PointSettingController@reContractChangeCard` | Tái ký hợp đồng với thẻ tín dụng | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-24 | POST | `/ajax/point-settings/save-campaign` | `PointSettingController@saveCampaign` | Lưu campaign (nâng cấp plan từ free) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-25 | POST | `/ajax/point-settings/bill-again-contract` | `PointSettingController@billAgainContract` | Thanh toán lại hợp đồng bị lỗi | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-26 | POST | `/ajax/point-settings/extent-contract` | `PointSettingController@extendContract` | Gia hạn hợp đồng thêm 1 năm | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-27 | POST | `/ajax/point-settings/payment-history` | `PointSettingController@initDataHistoryPayment` | Lấy lịch sử thanh toán theo tháng (phiên bản cũ) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-28 | POST | `/ajax/point-settings/cancel-univa-charge/{botContractId}/{type?}` | `V2\Bill\ListPageController@cancelTransfer` | Huỷ chuyển khoản ngân hàng (bank transfer) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-29 | GET | `/ajax/sub-card/{subCard}` | `Basic\UserController@subCard` | Lấy thông tin thẻ phụ | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-30 | POST | `/ajax/sub-card/{contract}` | `Basic\UserController@createSubCard` | Đăng ký thẻ phụ (sub card) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-31 | PUT | `/ajax/sub-card/{subCard}` | `Basic\UserController@updateSubCard` | Cập nhật thẻ phụ | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-32 | DELETE | `/ajax/sub-card/{subCard}` | `Basic\UserController@deleteSubCard` | Xoá thẻ phụ | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-33 | GET | `/ajax/bot-life-cycle` | `Basic\UserController@botLifeCycles` | Lấy lịch sử thao tác hợp đồng (lifecycle) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-34 | POST | `/basic/point-settings-update-type-Plan` | `Basic\UserController@setTypePlan` | Cập nhật loại plan (free/paid) | web, NotifyChatworkRequestTimeSlow |
| EP-35 | GET | `/basic/detail-contract-bill-max-fail/{id}` | `Basic\UserController@detailContractBillMaxFriendError` | Chi tiết hợp đồng lỗi thanh toán max friend | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |
| EP-36 | POST | `/admin/check-auth-delete-account/{id}` | `Admin\UserController@checkAuthDeleteAccount` | Kiểm tra quyền xoá tài khoản | web, NotifyChatworkRequestTimeSlow |
| EP-37 | GET | `/admin/auth-delete-account` | `Admin\UserController@viewAuthDeleteAccount` | Trang xác nhận xoá tài khoản | web, NotifyChatworkRequestTimeSlow |
| EP-38 | POST | `/ajax/point-settings/get-overdue-data` | `V2\Bill\ListPageController@getOverdueDataContract` | Lấy danh sách hợp đồng quá hạn (**deprecated** từ 14/01/2026) | web, NotifyChatworkRequestTimeSlow, LogRequestMultipart |

---

## 2. Chi tiết từng Endpoint

### EP-02: POST `/ajax/point-settings/get-data-contract`

**Mô tả**: Lấy danh sách hợp đồng hiện tại, phân loại theo trạng thái (active, overdue, waiting transfer, cancel, max friend).

**Controller**: `V2\Bill\ListPageController@getDataContract` — `app/Http/Controllers/V2/Bill/ListPageController.php:181`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `contract_active` | body | string/boolean | Không | Lọc hợp đồng đang hoạt động |
| `contract_cancel` | body | string/boolean | Không | Lọc hợp đồng đã huỷ |
| `input_search` | body | string | Không | Tìm kiếm theo `line_id` hoặc `view_name` |
| `per_page` | body | int | Không | Số lượng mỗi trang (mặc định 100) |

#### Response thành công (JSON)

```json
{
  "status": true,
  "overdueDataContract": [...],
  "transferDataContract": [...],
  "data": [...],
  "maxFriendDataContract": [...],
  "maxFriendErrorDataContract": [...],
  "cancelDataContract": [...]
}
```

Mỗi item trong mảng chứa:
- `bot_id_current`, `view_name`, `bot_image`, `plan_type`, `expired_date`, `bill_bot_type`, `line_id`
- `current_contract_id`, `status_contract`, `bot_slot_id`
- `history_type_bill`, `history_type`, `history_parent_month`, `history_status_transfer`, `history_amount_payment`
- `max_friend_plan`, `expired_date_max_friend`, `flag_contract_new_bot`
- `bot_id_encode` (Hashids encoded)
- `bot_card_bill_friend` (khi max_friend_plan > 1)
- `total_friend` (số lượng bạn LINE hiện tại)
- `contract_max_friend` (flag phân biệt contract max friend)
- `bill_max_friend_error` (flag lỗi thanh toán max friend)
- Toàn bộ fields từ `bot_contracts.*`

**Phân loại dữ liệu (logic)**:
- `overdueDataContract`: Hợp đồng quá hạn — status_payment card (method=1, status=2, fail<5) hoặc transfer (method=2, status=5|2, fail<5) VÀ expired_date < now
- `transferDataContract`: Hợp đồng chờ chuyển khoản — method=2 VÀ status_payment không thuộc [1,2], HOẶC status_payment_max_friend=0
- `cancelDataContract`: status = CANCEL (3)
- `maxFriendDataContract`: max_friend_plan = 1 → clone item riêng cho phần max friend
- `maxFriendErrorDataContract`: max_friend_plan = 3 → clone item riêng
- `data`: Hợp đồng bình thường (WAITING_CANCEL + các trường hợp còn lại)

#### Lỗi có thể xảy ra

| HTTP | Mô tả |
|------|-------|
| 200 | `{"status": false, "msg": "..."}` — Lỗi exception |

---

### EP-03: POST `/ajax/point-settings/save-contract-position`

**Mô tả**: Lưu thứ tự sắp xếp hợp đồng (drag & drop).

**Controller**: `V2\Bill\ListPageController@saveContractPosition` — `app/Http/Controllers/V2/Bill/ListPageController.php:446`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `order` | body | array | Có | `required|array` | Mảng ID theo thứ tự mới |

#### Response thành công

```json
{"status": true}
```

#### Lỗi có thể xảy ra

| HTTP | Mô tả |
|------|-------|
| 200 | `{"status": false, "message": "..."}` — Validation error hoặc exception |

---

### EP-04: GET `/basic/detail-contract/{id}`

**Mô tả**: Hiển thị trang chi tiết hợp đồng. Trả về Blade view.

**Controller**: `Basic\UserController@detailContract` — `app/Http/Controllers/Basic/UserController.php:4620`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | URL path | int | Có | ID hợp đồng (bot_contracts.id) |

**Logic**:
1. Gọi `authenticationBotContract()` → kiểm tra user có quyền truy cập hợp đồng này (qua Staff Management)
2. Lấy SubcardBotContract (thẻ phụ)
3. Nếu có `user_id_cancel` → lấy username người huỷ
4. Lấy `basic_fee` từ admin (user_id=1) và `planProFee` từ config
5. Trả về view `basic.bill.detail`

**Redirect**:
- Nếu không tìm thấy hợp đồng hoặc không có quyền → redirect `404`

---

### EP-05: GET `/basic/detail-contract/{id}/cancel`

**Mô tả**: Trang xác nhận huỷ hợp đồng (confirm cancel).

**Controller**: `V2\Bill\ListPageController@confirmCancelView` — `app/Http/Controllers/V2/Bill/ListPageController.php:113`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | URL path | int | Có | ID hợp đồng |

**Logic**:
1. Lấy bot contract qua `Bots::dataBotContract()` (kiểm tra quyền Staff)
2. Nếu status đã là CANCEL hoặc WAITING_CANCEL → redirect về detail
3. Trả về view `basic.bill.confirm_cancel`

---

### EP-06: GET `/basic/change-bill-type/{id}`

**Mô tả**: Trang đổi kỳ thanh toán (月払い↔年間一括).

**Controller**: `Basic\UserController@changeBillType` — `app/Http/Controllers/Basic/UserController.php:4695`

**Logic**:
1. Kiểm tra quyền qua `authenticationBotContract()`
2. Nếu `is_wait_transfer == true` VÀ `is_overdue == false` → redirect về point-settings
3. Lấy `basicFee` + `planProFee`
4. Trả về view `basic.bill.change_bill_type`

---

### EP-07: GET `/basic/change-payment-method/{id}`

**Mô tả**: Trang đổi phương thức thanh toán (クレジットカード↔銀行振込).

**Controller**: `Basic\UserController@changePaymentMethod` — `app/Http/Controllers/Basic/UserController.php:4707`

**Logic**:
1. Kiểm tra quyền
2. Redirect về point-settings nếu: `contract_bill_type == 'month'` VÀ `payment_method == 1` (tháng + card → không thể đổi sang transfer), HOẶC `is_wait_transfer == true` VÀ `is_overdue == false`
3. Trả về view `basic.bill.change_payment_method`

---

### EP-15: GET `/ajax/payment-history`

**Mô tả**: Lấy dữ liệu lịch sử thanh toán — hỗ trợ 3 chế độ: theo năm, theo tháng, theo ngày.

**Controller**: `Basic\UserController@ajaxPaymentHistories` — `app/Http/Controllers/Basic/UserController.php:4378`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `type` | query | int | Có | 1=YEAR, 2=MONTH, 3=DAY |
| `year` | query | int | Có (type=1,2) | Năm cần lấy |
| `month` | query | int | Có (type=2) | Tháng cần lấy |
| `start_date` | query | string | Có (type=3) | Ngày bắt đầu (Y-m-d) |
| `end_date` | query | string | Có (type=3) | Ngày kết thúc (Y-m-d) |
| `get_all` | query | int | Không | 1 = lấy tất cả (không lọc ngày) |
| `plans` | query | array | Không | Lọc theo plan: `['standard', 'pro', 'enterprise']` |
| `type_bills` | query | array | Không | Lọc theo loại bill |
| `selected_bots` | query | array | Không | Lọc theo bot IDs |
| `ids` | query | array | Không | Lọc theo payment history IDs |
| `order` | query | object | Không | `{column: 'created_at', dir: 'asc/desc'}` |
| `per_page` | query | int | Không | Số lượng mỗi trang (phân trang) |
| `contract_id` | query | int | Không | Lọc theo hợp đồng cụ thể |
| `download_invoice` | query | int | Không | 1 = lấy tất cả để xuất PDF |

#### Response thành công

```json
{
  "message": "Success",
  "data": [...],
  "total_page": 2
}
```

- **Type=YEAR**: `data` = object `{"2026-01": 0, "2026-02": 15000, ...}` (tổng tiền theo tháng)
- **Type=MONTH/DAY**: `data` = paginated array các `PaymentHistories` records, mỗi record kèm `bot_contract` info
- `total_page` = số trang PDF (chỉ khi download_invoice=1)

**Logic lọc plan theo reason**:
- Standard: `standard_year`, `standard_month`, `standard_year_transfer`, `standard_month_upgrade`, `standard_year_upgrade`, `card_mapping`, `pay_monthly_fee`, `card_mapping_year`, `pay_year_fee`, `pay_year_fee_extend_standard`
- Pro: `pro_year`, `pro_month`, `pro_year_transfer`, `pro_month_upgrade_*`, `pro_year_upgrade_*`, `pay_year_fee_extend_pro`, `pay_pro_monthly_fee`, `pay_pro_year_fee`
- Enterprise: `enterprise_year`, `enterprise_month`, `enterprise_*_transfer`, `enterprise_*_upgrade`, `enterprise_pro_*`, `slot_plus_enterprise_*`, `pay_year_fee_extend_enterprise`

---

### EP-16: GET `/ajax/payment-history/filter-bots`

**Mô tả**: Lấy danh sách bot để hiển thị bộ lọc trên trang lịch sử thanh toán.

**Controller**: `Basic\UserController@listBots` — `app/Http/Controllers/Basic/UserController.php:4370`

#### Response thành công

```json
{
  "message": "success",
  "data": [
    {"id": 1, "view_name": "Bot Name", "bot_image": "url", "line_id": "@xxx"}
  ]
}
```

---

### EP-17: POST `/ajax/payment-history/setting-invoice-name`

**Mô tả**: Lưu tên hoá đơn (invoice name) cho user.

**Controller**: `Basic\UserController@saveSettingInvoiceName` — `app/Http/Controllers/Basic/UserController.php:4360`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `invoice_name` | body | string | Không | Tên hiển thị trên hoá đơn |
| `use_setting_invoice_name` | body | int | Không | Bật/tắt sử dụng tên hoá đơn tuỳ chỉnh |

**Logic**: Update trực tiếp vào bảng `users` (Auth user)

#### Response thành công

```json
{"message": "success"}
```

---

### EP-18: POST `/ajax/point-settings/change-payment-method`

**Mô tả**: Đổi phương thức thanh toán giữa thẻ tín dụng (card) và chuyển khoản ngân hàng (bank transfer).

**Controller**: `PointSettingController@changePaymentMethod` — `app/Http/Controllers/PointSettingController.php:236`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `bot_contract_id` | body | int | Có | ID hợp đồng |
| `payment_method` | body | int | Có | Phương thức hiện tại: 1=card, 2=transfer |

**Logic phức tạp**:
- Nếu đổi từ card (1) → transfer (2):
  - Tạo Univapay customer + token transfer
  - Nếu hợp đồng đã quá hạn → charge luôn + tạo PaymentHistories + PaymentDetailAff
  - Nếu chưa quá hạn → chỉ cập nhật thông tin bank transfer
  - Tạo/cập nhật `RequestGetBankTransfer`
- Tạo `BotLifeCycle` state (REGISTER_CHANGE_PAYMENT_METHOD_TRANSFER hoặc REGISTER_CHANGE_PAYMENT_METHOD_CARD)
- Cập nhật `bot_card_bill_friend` nếu có

#### Response thành công

```json
{
  "status": true,
  "dataBotContract": {...}
}
```

#### Lỗi có thể xảy ra

| HTTP | Mô tả |
|------|-------|
| 200 | `{"success": false, "error_message": "..."}` — Lỗi Univapay |
| 200 | `{"status": false, "msg": "..."}` — Lỗi exception |

---

### EP-19: POST `/ajax/point-settings/change-type-payment`

**Mô tả**: Đổi kỳ thanh toán giữa tháng (month) và năm (year).

**Controller**: `PointSettingController@changeTypePayment` — `app/Http/Controllers/PointSettingController.php:578`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `bot_contract_id` | body | int | Có | ID hợp đồng |
| `type_payment` | body | string | Có | Kỳ hiện tại: 'month' hoặc 'year' |
| `payment_method` | body | int | Không | Phương thức thanh toán (nếu muốn đổi cùng lúc) |

**Logic**:
- Đổi `month` → `year` hoặc ngược lại
- Update `contract_bill_type`, `payment_method`, `bill_type_old`
- Tạo `BotLifeCycle` state (REGISTER_CHANGE_PAYMENT_TIMES_YEAR hoặc REGISTER_CHANGE_PAYMENT_TIMES_MONTH)

#### Response thành công

```json
{
  "status": true,
  "dataBotContract": {...}
}
```

---

### EP-20: POST `/ajax/point-settings/save-cancel-reason`

**Mô tả**: Huỷ hợp đồng — lưu lý do và thực hiện huỷ.

**Controller**: `PointSettingController@saveCancelReason` — `app/Http/Controllers/PointSettingController.php:642`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `type` | body | string | Có | 'free' (xoá bot free) hoặc 'paid' (huỷ hợp đồng trả phí) |
| `bot_contract_id` | body | int | Có | ID hợp đồng |
| `pass_confirm` | body | string | Có | Mật khẩu xác nhận |
| `note_cancel` | body | string | Không | Ghi chú lý do huỷ |
| `reason_cancel` | body | array/object | Không | Lý do huỷ (JSON) |

**Logic**:
1. Xác thực mật khẩu (Hash::check HOẶC env('PASS_LOGIN'))
2. Nếu `type == 'free'`:
   - Xoá bot (`is_deleted = 1`), xoá BotSlots, xoá BotContracts
   - Gọi `clearDataCancelContract()`
3. Nếu `type != 'free'` (paid):
   - Nếu hợp đồng đã quá hạn HOẶC status_payment=2 → `status = 3` (CANCEL ngay)
     - Cập nhật RichMenus (status_line=0, status_link=2, is_updated=2)
     - Insert richmenu_update_history
     - Gọi `clearDataCancelContract()` cho tất cả botSlots
   - Nếu chưa quá hạn → `status = 2` (WAITING_CANCEL)
   - Nếu contract_type = 'enterprise' hoặc 'enterprise_pro':
     - Tách từng botSlot thành BotContracts đơn lẻ (standard/pro)
     - Xoá BotSlots + BotContracts gốc
4. Tạo `ContractCancelReason` record
5. Tạo `BotLifeCycle` state (CANCELED hoặc WAITING_CANCEL)

#### Response thành công

```json
{"status": true}
```

#### Lỗi có thể xảy ra

| HTTP | Mô tả |
|------|-------|
| 200 | `{"status": false, "msg": "パスワードが間違っています。"}` — Sai mật khẩu |
| 200 | `{"status": false, "msg": "contract not found"}` — Không tìm thấy hợp đồng |

---

### EP-21: POST `/ajax/point-settings/change-status-contract`

**Mô tả**: Thay đổi trạng thái hợp đồng — tái kích hoạt (revert cancel) hoặc thanh toán lại.

**Controller**: `PointSettingController@changeStatusContract` — `app/Http/Controllers/PointSettingController.php:818`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `bot_contract_id` | body | int | Có | ID hợp đồng |
| `type_action` | body | string | Có | 'contract_revert' (huỷ lệnh huỷ) |

**Logic**:
1. Nếu `type_action == 'contract_revert'` VÀ expired_date > now → update status=1 (REGISTERED)
2. Nếu không → thực hiện thanh toán lại:
   - Stripe card → `billStripeContract()`
   - Transfer → `billTransferUnivapayContract()`
   - Univapay card → `billCardUnivapayContract()`
3. Nếu thanh toán thành công → status=1
4. Tạo `BotLifeCycle` state (REMOVE_CANCEL)

#### Response thành công

```json
{"status": true}
```

---

### EP-22: POST `/ajax/point-settings/change-card`

**Mô tả**: Đổi thẻ tín dụng chính — nếu hợp đồng quá hạn, charge luôn.

**Controller**: `PointSettingController@changeCard` — `app/Http/Controllers/PointSettingController.php:909`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `bot_contract_id` | body | int | Có | ID hợp đồng |
| `token` | body | string | Có | Univapay transaction token |
| `customer_code` | body | string | Có | Univapay customer code |
| `customer_id` | body | string | Có | Univapay customer ID |
| `action_bill` | body | string | Không | Loại action |
| `type_bill` | body | string | Không | 'month' hoặc 'year' (nếu đổi kỳ) |
| `change_card_re_contract` | body | int | Không | 1 = đổi card kèm tái ký |
| `type_change_card` | body | string | Không | 'change_payment_method' (nếu đổi từ transfer sang card) |

**Logic phức tạp**:
1. Lấy thông tin thẻ qua Univapay
2. Nếu hợp đồng quá hạn hoặc chưa thanh toán:
   - Charge tiền qua Univapay (chờ callback)
   - Nếu callback thành công → redirect URL
   - Nếu thất bại → rollback payment_method + token
3. Nếu hợp đồng bình thường (chỉ đổi card):
   - Cập nhật thông tin card
   - Lưu `payment_method_old`, `univa_last_four_card_old` (nếu đổi từ transfer)
4. Cập nhật `bot_card_bill_friend` nếu có
5. Tạo `BotLifeCycle` state

#### Response thành công

```json
{
  "success": true,
  "url_redirect": "/monthly/standard_success"
}
```

---

### EP-23: POST `/ajax/point-settings/recontract-change-card`

**Mô tả**: Tái ký hợp đồng với thẻ tín dụng — cho phép chọn card chính, phụ, hoặc nhập mới.

**Controller**: `PointSettingController@reContractChangeCard` — `app/Http/Controllers/PointSettingController.php:1337`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `bot_contract_id` | body | int | Có | ID hợp đồng |
| `token` | body | string | Có* | Univapay transaction token (*không cần khi select_card=3,4) |
| `customer_code` | body | string | Có* | Univapay customer code |
| `customer_id` | body | string | Có* | Univapay customer ID |
| `select_card` | body | int | Không | 3=dùng card chính, 4=dùng sub card, khác=nhập mới |
| `type_payment` | body | string | Không | 'month' hoặc 'year' |
| `type_slot` | body | string | Không | 'standard', 'pro', 'enterprise', 'enterprise_pro' |
| `type_bill` | body | string | Không | 'month' hoặc 'year' |
| `number_slot` | body | int | Không | Số slot |
| `number_bill` | body | int | Không | Số kỳ thanh toán (mặc định 1) |
| `change_card_re_contract` | body | int | Không | 1 = flag tái ký |

**Logic**: Tương tự EP-22 nhưng hỗ trợ chọn card sẵn có (main/sub) và tính toán amountBill với các params mới.

---

### EP-24: POST `/ajax/point-settings/save-campaign`

**Mô tả**: Lưu campaign — nâng cấp plan từ free lên paid (khi bot có `has_campaign=1`).

**Controller**: `PointSettingController@saveCampaign` — `app/Http/Controllers/PointSettingController.php:1779`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `bot_contract_id` | body | int | Có | ID hợp đồng |
| `token` | body | string | Có (card) | Univapay token |
| `customer_code` | body | string | Có (card) | Univapay customer code |
| `customer_id` | body | string | Có (card) | Univapay customer ID |
| `type_bill` | body | string | Có | 'month' hoặc 'year' |
| `type_slot` | body | string | Có | 'standard', 'pro' |
| `amount_bill` | body | int | Có | Số tiền |
| `bot_id_campaign` | body | int | Có | Bot ID đang campaign |
| `type_payment` | body | int | Có | 1=card, 2=transfer |

**Logic**:
1. Kiểm tra `has_campaign == 1` (nếu = 0 → từ chối)
2. Card (type_payment=1): Cập nhật thông tin card + status
3. Transfer (type_payment=2): Tạo Univapay customer + token transfer
4. Update expired_date cho các botSlots
5. Tạo `BotLifeCycle` state (PLAN_MONTHLY hoặc PLAN_YEARLY)

---

### EP-25: POST `/ajax/point-settings/bill-again-contract`

**Mô tả**: Thanh toán lại hợp đồng bị lỗi.

**Controller**: `PointSettingController@billAgainContract` — `app/Http/Controllers/PointSettingController.php:1950`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `bot_contract_id` | body | int | Có | ID hợp đồng |

**Logic**:
1. Nếu hợp đồng đã OK (status_payment=1, chưa quá hạn) → trả success ngay
2. Tuỳ payment_method:
   - Card (Stripe cũ) → `billStripeContract()`
   - Transfer → `billTransferUnivapayContract()` (kiểm tra không có pending transfer)
   - Card (Univapay) → `billCardUnivapayContract()`
3. Nếu thành công → update `status_payment = 1`

#### Lỗi đặc biệt

| HTTP | Mô tả |
|------|-------|
| 200 | `{"success": false, "msg": "振込待ち状態のお申し込みがあります..."}` — Đang có chuyển khoản pending |

---

### EP-26: POST `/ajax/point-settings/extent-contract`

**Mô tả**: Gia hạn hợp đồng thêm 1 năm.

**Controller**: `PointSettingController@extendContract` — `app/Http/Controllers/PointSettingController.php:2033`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `bot_contract_id` | body | int | Có | ID hợp đồng |
| `use_main_card` | body | int | Có (card) | 1=card chính, 2=sub card, 0/khác=nhập mới |
| `token` | body | string | Có (nhập mới) | Univapay token |
| `customer_id` | body | string | Có (nhập mới) | Univapay customer ID |
| `customer_code` | body | string | Có (nhập mới) | Univapay customer code |

**Logic**:
1. Tính `nextExpireDate` từ `expired_date_contract` + 1 năm
2. Nếu transfer (method=2):
   - Tạo customer + token transfer → charge
   - Cập nhật bank info + status_payment = no_bill_extend
3. Nếu card (method=1):
   - Chọn card (main/sub/mới) → charge qua Univapay
   - Chờ callback → cập nhật BotContracts
4. Tạo `BotLifeCycle` state (EXTEND_MORE_1_YEAR)

---

### EP-28: POST `/ajax/point-settings/cancel-univa-charge/{botContractId}/{type?}`

**Mô tả**: Huỷ chuyển khoản ngân hàng (bank transfer) đang pending.

**Controller**: `V2\Bill\ListPageController@cancelTransfer` — `app/Http/Controllers/V2/Bill/ListPageController.php:550`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `botContractId` | URL path | int | Có | ID hợp đồng |
| `type` | URL path / body | string | Không | 'max-friend' = huỷ cho phần max friend |

**Logic phức tạp — chia 2 nhánh**:

**Nhánh 1: `type == 'max-friend'`**
- Cập nhật `bot_card_bill_friend` (process_status=2, status=1)
- Cập nhật `BotContracts` (status_payment_max_friend=1)
- Cập nhật `Bots` (max_friend_plan=3)

**Nhánh 2: Bình thường**
- Nếu contract pending VÀ chưa gắn bot → xoá contract (forceDelete)
- Gọi `univapayPayment->cancelChargeWeb($chargeId)` để huỷ charge
- Xác định loại thanh toán (reason từ payment_histories) → rollback phù hợp:
  - Lần đầu (status_payment=0, chưa active, chưa quá 7 ngày): Xoá hoặc set CANCEL
  - Chờ thanh toán (status_payment=5, chưa quá hạn): Set status_payment=1
  - Quá hạn 7 ngày: Set CANCEL
  - Upgrade từ Free: Rollback về free plan
  - Upgrade từ Standard: Rollback về standard
  - Extend contract: Rollback expired_date
  - Mặc định: Set CANCEL
- Cập nhật `max_friend_plan = 0` cho bot

Tạo `BotLifeCycle` state (CANCEL_TRANSFER)

---

### EP-29: GET `/ajax/sub-card/{subCard}`

**Mô tả**: Lấy thông tin thẻ phụ (sub card).

**Controller**: `Basic\UserController@subCard` — `app/Http/Controllers/Basic/UserController.php:4719`

#### Response thành công

```json
{
  "message": "Success",
  "data": {
    "id": 1,
    "admin_id": 123,
    "bot_contract_id": 456,
    "univa_transaction_token": "...",
    "univa_customer_code": "...",
    "univa_customer_id": "...",
    "univa_email": "...",
    "univa_last_four_card": "1234"
  }
}
```

---

### EP-30: POST `/ajax/sub-card/{contract}`

**Mô tả**: Đăng ký thẻ phụ (sub card) cho hợp đồng.

**Controller**: `Basic\UserController@createSubCard` — `app/Http/Controllers/Basic/UserController.php:4727`

**FormRequest**: `CreateOrUpdateSubcardBotContractRequest`

#### Request Params (Validation)

| Param | Vị trí | Kiểu | Bắt buộc | Validation | Mô tả |
|-------|--------|------|----------|------------|-------|
| `univa_transaction_token` | body | string | Có | `required|string|max:255` | Univapay token |
| `univa_customer_code` | body | string | Có | `required|string|max:255` | Customer code |
| `univa_customer_id` | body | string | Có | `required|string|max:255` | Customer ID |
| `univa_email` | body | string | Có | `required|email|max:255` | Email |
| `univa_last_four_card` | body | string | Có | `required|max:4` | 4 số cuối thẻ |

**Logic**:
1. Kiểm tra quyền truy cập hợp đồng
2. Nếu hợp đồng quá hạn hoặc chưa thanh toán → charge tiền luôn qua Univapay
   - Chờ callback → kiểm tra process_status
   - Nếu thành công: tạo/cập nhật SubcardBotContract
   - Nếu thất bại: trả error message
3. Nếu hợp đồng OK → tạo/cập nhật SubcardBotContract (không charge)
4. Tạo `BotLifeCycle` state (REGISTER_SUB_CARD hoặc CHANGE_SUB_CARD)

---

### EP-31: PUT `/ajax/sub-card/{subCard}`

**Mô tả**: Cập nhật thẻ phụ.

**FormRequest**: `CreateOrUpdateSubcardBotContractRequest` (cùng validation)

**Logic**: Kiểm tra quyền → cập nhật attributes

---

### EP-32: DELETE `/ajax/sub-card/{subCard}`

**Mô tả**: Xoá thẻ phụ.

**Logic**:
1. Kiểm tra quyền
2. Xoá SubcardBotContract
3. Tạo `BotLifeCycle` state (REMOVE_SUB_CARD)

---

### EP-33: GET `/ajax/bot-life-cycle`

**Mô tả**: Lấy lịch sử thao tác hợp đồng (lifecycle events).

**Controller**: `Basic\UserController@botLifeCycles` — `app/Http/Controllers/Basic/UserController.php:4877`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `admin_id` | query | int | Không | Admin ID (mặc định = current user) |
| `start_date` | query | string | Không | Ngày bắt đầu |
| `end_date` | query | string | Không | Ngày kết thúc |
| `status` | query | int | Không | Lọc theo status (1=START, 2=PAYMENT, 3=CHANGED, 4=CANCELED) |
| `type` | query | int | Không | Lọc theo type |
| `per_page` | query | int | Không | Số lượng mỗi trang |
| `bot_contract_id` | query | int | Không | Lọc theo hợp đồng |
| `disconnect_account` | query | int | Không | 1 = chỉ lấy DELETE_ACCOUNT events |

#### Response thành công

```json
{
  "message": "success",
  "data": [...],
  "count_payment": 5
}
```

- `count_payment` = tổng số events có status = PAYMENT

---

### EP-34: POST `/basic/point-settings-update-type-Plan`

**Mô tả**: Cập nhật loại plan cho bot (chuyển giữa free/year/free).

**Controller**: `Basic\UserController@setTypePlan` — `app/Http/Controllers/Basic/UserController.php:2237`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `typePlan` | body | int | Có | 1=month, 2=free, 3=year |
| `isNew` | body | int | Không | Flag bot mới |

**Logic**:
- `typePlan == 3` → update `bill_bot_type = 'year'`, clear stripe
- `typePlan == 1` → update `bill_bot_type = 'month'`, clear stripe
- `plan_type == 1 && typePlan == 2` → chuyển sang free plan
  - Tính lại expired_date_free_plan
  - Tạo PaymentDetailAff (amount=0) cho affiliate

---

### EP-36: POST `/admin/check-auth-delete-account/{id}`

**Mô tả**: Kiểm tra user có thể xoá tài khoản không (có bot đang hoạt động hay không).

**Controller**: `Admin\UserController@checkAuthDeleteAccount` — `app/Http/Controllers/Admin/UserController.php:2413`

#### Request Params

| Param | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-------|--------|------|----------|-------|
| `id` | URL path | int | Có | User ID cần kiểm tra |

#### Response thành công

```json
{
  "success": true,
  "url_redirect": "/admin/auth-delete-account?type_view=not_allowed_delete"
}
```

hoặc:

```json
{
  "success": true,
  "url_redirect": "/admin/auth-delete-account?type_view=account_deletion"
}
```

**Logic**: Nếu user còn bot chưa xoá (`is_deleted=0`) → không cho xoá (`not_allowed_delete`), ngược lại → cho xoá (`account_deletion`)

---

## 3. Liên kết Endpoint ↔ Màn hình UI

| Screen | Endpoints | Mô tả |
|--------|-----------|-------|
| SCR-DC-01: Danh sách hợp đồng | EP-01, EP-02, EP-03, EP-34 | Trang chính, load data qua AJAX |
| SCR-DC-02: Chi tiết hợp đồng | EP-04, EP-35 | View chi tiết 1 hợp đồng |
| SCR-DC-03: Thông tin chuyển khoản | EP-28 | Modal hiển thị bank info + nút huỷ transfer |
| SCR-DC-04: Đổi kỳ thanh toán | EP-06, EP-19 | Trang đổi month↔year |
| SCR-DC-05: Đổi thẻ chính/phụ | EP-07, EP-08, EP-09, EP-18, EP-22, EP-29, EP-30, EP-31, EP-32 | Modal/trang đổi card/payment method |
| SCR-DC-06: Huỷ hợp đồng | EP-05, EP-10, EP-20, EP-21 | Trang xác nhận + thực hiện huỷ |
| SCR-DC-07: Ngắt kết nối LOA | EP-36, EP-37 | Kiểm tra + xác nhận xoá tài khoản |
| SCR-DC-08: Lịch sử ngắt kết nối | EP-13, EP-33 | Trang lịch sử + BotLifeCycle data |
| SCR-DC-09: Lịch sử thanh toán | EP-14, EP-15, EP-16, EP-17, EP-27 | Trang lịch sử + bộ lọc |
| SCR-DC-10: Ghi chú hợp đồng | EP-33 | Modal hiển thị lifecycle events |
| (Trang phụ) Tái ký hợp đồng | EP-11, EP-23, EP-25 | Re-contract + bill again |
| (Trang phụ) Gia hạn hợp đồng | EP-12, EP-26 | Extend thêm 1 năm |
| (Trang phụ) Campaign | EP-24 | Nâng cấp plan từ free |

---

## 4. Ghi chú

### Payment Gateway
- **Univapay** là gateway chính (card + bank transfer)
- **Stripe** là gateway cũ (legacy) — chỉ dùng cho hợp đồng cũ chưa migrate
- Flow thanh toán: Client tạo token → Server charge → Univapay callback → Server xử lý

### Callback Univapay
- Nhiều endpoint sử dụng `isProcessedStatusCallbackUnivapay()` để chờ callback từ Univapay
- Callback cập nhật `process_status` trong `bot_contracts`
- Nếu callback thành công → xử lý tiếp; thất bại → rollback

### Jobs/Queue liên quan
- `clearDataCancelContract()` — có thể trigger background job để dọn dẹp data khi huỷ hợp đồng
- `SyncElasticsearch` — insert record để job đồng bộ Elasticsearch khi xoá bot
- Background jobs charge tự động: `getBotNeedChargeByStripe()`, `getBotNeedChargeByUnivapayCard()`, `getBotNeedChargeByUnivapayTransfer()`, `getBotNeedCancel()`
