# API Spec — FA-031: Hợp đồng và Thanh toán (Billing Plan)

## Tổng quan

| Thuộc tính | Giá trị |
|-----------|---------|
| Mã tính năng | FA-031 |
| Tên tính năng | Hợp đồng và Thanh toán (Billing Plan) |
| Controllers liên quan | `V2\Bill\ListPageController`, `Basic\UserController`, `Admin\BotController`, `PointSettingController` |

---

## EP-01: Trang danh sách hợp đồng

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `GET` |
| URL | `/basic/point-settings` |
| Controller@Method | `V2\Bill\ListPageController@indexView` |
| Middleware | `basic_access`, `https_protocol`, `check_remember_token` |
| Auth required | Có (Admin/Staff đã đăng nhập) |
| Màn hình liên quan | SCR-BLP-01 |

### Request params
Không có request params.

### Response
Trả về HTML view `basic.bill.index` với các biến:

| Biến | Kiểu | Mô tả |
|------|------|-------|
| `basic_fee` | int | Phí cơ bản từ user admin_id=1 |
| `planProFee` | int/float | Phí plan Pro từ config `sns-line.plan_pro_fee` |
| `botActive` | Bots\|null | Bot đang active trong session hiện tại |
| `contractBotActive` | BotContracts\|null | Hợp đồng của bot đang active |
| `botFreeNumber` | int | Số lượng bot free plan của admin hiện tại |

**Độ tin cậy**: Cao — đọc trực tiếp từ `V2\Bill\ListPageController@indexView` dòng 41-66

---

## EP-02: AJAX lấy danh sách hợp đồng

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `POST` |
| URL | `/ajax/point-settings/get-data-contract` |
| Controller@Method | `V2\Bill\ListPageController@getDataContract` |
| Route name | `ajax.pointSetting.get_data_contract` |
| Middleware | `check_login`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-01 |

### Request params (body / form-data)

| Tên | Kiểu | Bắt buộc | Mô tả |
|-----|------|----------|-------|
| `contract_active` | boolean/string | Không | Lọc hợp đồng đang hoạt động (`true`/`false`) |
| `contract_cancel` | boolean/string | Không | Lọc hợp đồng đã hủy (`true`/`false`) |
| `input_search` | string | Không | Tìm kiếm theo LINE ID hoặc tên bot |
| `per_page` | int | Không | Số item mỗi trang (mặc định: 100) |

### Request mẫu
```json
{
  "contract_active": "true",
  "contract_cancel": "true",
  "input_search": "",
  "per_page": 100
}
```

### Response thành công
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

#### Cấu trúc từng item trong mảng

| Field | Kiểu | Mô tả |
|-------|------|-------|
| `id` | int | ID hợp đồng (`bot_contracts.id`) |
| `bot_id_current` | int | ID bot gắn với hợp đồng |
| `bot_id_encode` | string | Bot ID mã hóa Hashids |
| `view_name` | string | Tên bot |
| `bot_image` | string | Ảnh đại diện bot |
| `plan_type` | int | Loại plan bot (2=free) |
| `expired_date` | datetime | Ngày hết hạn bot |
| `bill_bot_type` | int | Loại bill bot |
| `line_id` | string | LINE Official Account ID |
| `max_friend_plan` | int | Plan giới hạn bạn bè (0=không, 1=có, 3=lỗi) |
| `expired_date_max_friend` | datetime | Ngày hết hạn plan max friend |
| `status` | int | Trạng thái hợp đồng (1=active, 2=chờ hủy, 3=đã hủy) |
| `status_contract` | int | Alias của `status` |
| `payment_method` | int | Phương thức thanh toán (1=card, 2=chuyển khoản) |
| `status_payment` | int | Trạng thái thanh toán |
| `status_payment_fail` | int | Số lần thanh toán thất bại |
| `contract_type` | string | Loại hợp đồng (`free`, `standard`, `pro`, `enterprise`) |
| `contract_bill_type` | string | Chu kỳ thanh toán (`month`, `year`) |
| `amount_payment` | float | Số tiền thanh toán |
| `expired_date_contract` | datetime | Ngày hết hạn hợp đồng |
| `contract_max_friend` | int | 1 nếu là item max friend |
| `bill_max_friend_error` | int | 1 nếu max friend có lỗi |
| `total_friend` | int | Tổng số bạn bè (chỉ khi max_friend_plan > 0) |
| `history_type_bill` | int | Loại bill từ payment history gần nhất |
| `history_type` | int | Type từ payment history gần nhất |
| `history_parent_month` | int | parent_month từ payment history |
| `history_status_transfer` | int | Trạng thái chuyển khoản gần nhất |
| `history_amount_payment` | float | Số tiền từ payment history gần nhất |
| `univa_bank_name` | string | Tên ngân hàng (nếu thanh toán chuyển khoản) |
| `univa_branch_name` | string | Tên chi nhánh ngân hàng |
| `univa_account_number` | string | Số tài khoản ngân hàng |
| `univa_bank_account_holder_name` | string | Tên chủ tài khoản |
| `expired_date_bank_transfer` | datetime | Hạn chuyển khoản |

#### Phân loại trong response

| Key | Điều kiện |
|-----|-----------|
| `overdueDataContract` | Hợp đồng quá hạn thanh toán (payment lỗi và expired < now) |
| `transferDataContract` | Hợp đồng đang chờ xác nhận chuyển khoản |
| `data` | Hợp đồng bình thường đang hoạt động |
| `maxFriendDataContract` | Item plan tính phí theo số bạn bè (`max_friend_plan==1`) |
| `maxFriendErrorDataContract` | Item plan max friend có lỗi (`max_friend_plan==3`) |
| `cancelDataContract` | Hợp đồng đã hủy |

### Lỗi có thể xảy ra

| HTTP Code | Điều kiện | Response |
|-----------|-----------|----------|
| 200 | Thành công | `{ "status": true, ... }` |
| 200 | Exception | `{ "status": false, "msg": "..." }` |

**Độ tin cậy**: Cao — đọc trực tiếp từ `V2\Bill\ListPageController@getDataContract` dòng 181-444

---

## EP-03: Trang lịch sử thanh toán

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `GET` |
| URL | `/basic/payment-history` |
| Controller@Method | `Basic\UserController@paymentHistories` |
| Route name | `paymentHistories` |
| Middleware | `basic_access`, `https_protocol`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-03 |

### Response
Trả về HTML view `basic.payment_history.index` với biến `user` (đối tượng User hiện tại).

**Độ tin cậy**: Cao — đọc trực tiếp từ `Basic\UserController@paymentHistories` dòng 4353-4358

---

## EP-04: AJAX lấy dữ liệu lịch sử thanh toán

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `GET` |
| URL | `/ajax/payment-history` |
| Controller@Method | `Basic\UserController@ajaxPaymentHistories` |
| Route name | `ajaxPaymentHistories` |
| Middleware | `check_login`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-03 |

### Request params (query string)

| Tên | Kiểu | Bắt buộc | Mô tả |
|-----|------|----------|-------|
| `type` | int | Có | Kiểu xem: 1=năm, 2=tháng, 3=ngày |
| `year` | int | Có (khi type=1,2) | Năm cần xem (vd: 2024) |
| `month` | int | Có (khi type=2) | Tháng cần xem (vd: 6) |
| `start_date` | string | Có (khi type=3) | Ngày bắt đầu (YYYY-MM-DD) |
| `end_date` | string | Có (khi type=3) | Ngày kết thúc (YYYY-MM-DD) |
| `get_all` | int | Không | 1 = lấy tất cả (dùng cho download PDF) |
| `plans` | array | Không | Lọc theo plan: `standard`, `pro`, `enterprise` |
| `type_bills` | array | Không | Lọc theo loại bill |
| `selected_bots` | array | Không | Lọc theo bot ID cụ thể |
| `ids` | array | Không | Lọc theo payment history ID cụ thể |
| `order` | object | Không | Sắp xếp: `{column: "created_at", dir: "asc/desc"}` |
| `per_page` | int | Không | Số item mỗi trang |
| `contract_id` | int | Không | Lọc theo hợp đồng cụ thể |
| `download_invoice` | int | Không | 1 = chế độ tải hóa đơn (trả về toàn bộ) |

### Response thành công — type=1 (theo năm)
```json
{
  "message": "Success",
  "data": {
    "2024-01": 50000,
    "2024-02": 75000,
    ...
  },
  "total_page": 0
}
```

### Response thành công — type=2 hoặc type=3 (theo tháng/ngày)
```json
{
  "message": "Success",
  "data": {
    "data": [...payment_history_items...],
    "current_page": 1,
    "last_page": 3,
    "total": 50
  },
  "total_page": 3
}
```

#### Cấu trúc payment history item

| Field | Kiểu | Mô tả |
|-------|------|-------|
| `id` | int | ID |
| `bot_contract_id` | int | ID hợp đồng |
| `amount` | float | Số tiền |
| `type_bill` | int | Loại bill (1=card tháng, 2=card năm, 3=chuyển khoản) |
| `type` | int | 1=thu phí thành công |
| `status_transfer` | int | Trạng thái chuyển khoản |
| `created_at` | datetime | Thời gian tạo |
| `reason` | string | Lý do thanh toán |
| `bot_contract` | object | Thông tin hợp đồng kèm theo |

**Lọc payment history áp dụng trong query**:
- `typeBill` scope: chỉ lấy (type=1 AND type_bill IN(1,2)) OR (status_transfer=1 AND type_bill=3)
- `status_refund = 0`: chỉ lấy thanh toán chưa được hoàn tiền

**Độ tin cậy**: Cao — đọc trực tiếp từ `Basic\UserController@ajaxPaymentHistories` dòng 4378-4426

---

## EP-05: Trang lịch sử ngắt kết nối LOA

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `GET` |
| URL | `/basic/disconnect-history` |
| Controller@Method | `V2\Bill\ListPageController@disconnectHistoryView` |
| Route name | `disconnectHistory` |
| Middleware | `basic_access`, `https_protocol`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-04 |

### Response
Trả về HTML view `basic.bill.disconnect_history` (không truyền biến đặc biệt).

**Độ tin cậy**: Cao — đọc trực tiếp từ `V2\Bill\ListPageController@disconnectHistoryView` dòng 68-71

---

## EP-06: AJAX lấy dữ liệu lịch sử kết nối/ngắt kết nối (bot life cycle)

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `GET` |
| URL | `/ajax/bot-life-cycle` |
| Controller@Method | `Basic\UserController@botLifeCycles` |
| Route name | `botLifeCycles` |
| Middleware | `check_login`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-04 |

### Request params (query string)

| Tên | Kiểu | Bắt buộc | Mô tả |
|-----|------|----------|-------|
| `admin_id` | int | Không | Admin ID (mặc định: user hiện tại) |
| `start_date` | string | Không | Ngày bắt đầu lọc (YYYY-MM-DD) |
| `end_date` | string | Không | Ngày kết thúc lọc (YYYY-MM-DD) |
| `status` | int\|array | Không | Lọc theo status (1=START, 2=PAYMENT, 3=CHANGED, 4=CANCELED) |
| `type` | int\|array | Không | Lọc theo type event (xem bảng TYPE constants) |
| `per_page` | int | Không | Phân trang |
| `bot_contract_id` | int | Không | Lọc theo hợp đồng cụ thể |
| `disconnect_account` | bool | Không | Nếu true: chỉ lấy sự kiện DELETE_ACCOUNT (type=28) |

### Response thành công
```json
{
  "message": "success",
  "data": [...bot_life_cycle_items...],
  "count_payment": 5
}
```

#### Cấu trúc bot_life_cycle item

| Field | Kiểu | Mô tả |
|-------|------|-------|
| `id` | int | ID |
| `bot_contract_id` | int | ID hợp đồng |
| `admin_id` | int | Admin ID |
| `type` | int | Loại sự kiện (xem TYPE constants trong BotLifeCycle) |
| `status` | int | Nhóm sự kiện (1=START, 2=PAYMENT, 3=CHANGED, 4=CANCELED) |
| `time_action` | datetime | Thời điểm thực hiện |
| `data` | json | Dữ liệu chi tiết sự kiện |
| `title` | string | Tên sự kiện (appended attribute, tiếng Nhật) |

**Độ tin cậy**: Cao — đọc trực tiếp từ `Basic\UserController@botLifeCycles` dòng 4894-4921

---

## EP-07: Chi tiết hợp đồng

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `GET` |
| URL | `/basic/detail-contract/{id}` |
| Controller@Method | `Basic\UserController@detailContract` |
| Route name | `detailContract` |
| Middleware | `basic_access`, `https_protocol`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-02 |

### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `id` | URL path | int | Có | ID hợp đồng (`bot_contracts.id`) |

### Response
- **Thành công**: HTML view `basic.bill.detail` với các biến:
  - `basic_fee` — phí cơ bản
  - `planProFee` — phí plan Pro
  - `bot` — dữ liệu hợp đồng + bot kết hợp (kèm `sub_card`, `hash_botId`, `user_cancel`)
  - `user` — đối tượng user hiện tại

- **Lỗi**: Redirect đến `404` nếu hợp đồng không tìm thấy hoặc không có quyền

**Phân quyền**: Middleware `authenticationBotContract` kiểm tra user có quyền truy cập bot contract không (qua `getListBotIdStaffManagement`).

**Độ tin cậy**: Cao — đọc trực tiếp từ `Basic\UserController@detailContract` dòng 4620-4644

---

## EP-08: Trang phát hành báo giá

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `GET` |
| URL | `/admin/plan-estimation` |
| Controller@Method | `Admin\BotController@PlanEstimation` |
| Route name | `PlanEstimation` |
| Middleware | `admin_access`, `https_protocol`, `check_remember_token` (nhóm `/admin/`) |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-05 |

### Request params (query string)

| Tên | Kiểu | Bắt buộc | Mô tả |
|-----|------|----------|-------|
| `contract_type` | string | Không | Loại hợp đồng muốn báo giá (`standard`, `pro`, `enterprise`) |
| `bill_type` | string | Không | Chu kỳ thanh toán (`month`, `year`) |
| `bot_id` | int | Không | Bot ID cụ thể để báo giá |
| `invoice_name` | string | Không | Tên trên hóa đơn |
| `type_customer` | string | Không | Loại khách hàng |

### Response
- **Thành công**: HTML view `admin.plan_estimate.plan_estimation` với:
  - `listBotFree` — danh sách bot free plan
  - `contractType` — loại hợp đồng đã chọn
  - `billType` — chu kỳ thanh toán đã chọn
  - `basicFee` — phí cơ bản
  - `botId` — bot ID đã chọn
  - `botName` — tên bot (nếu có)
  - `bot` — dữ liệu bot (nếu có)
  - `contract` — hợp đồng hiện tại của bot (nếu có)

- **Lỗi**: Redirect `404` khi exception

**Độ tin cậy**: Cao — đọc trực tiếp từ `Admin\BotController@PlanEstimation` dòng 11426-11467

---

## EP-09: AJAX lưu vị trí hợp đồng (drag & drop)

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `POST` |
| URL | `/ajax/point-settings/save-contract-position` |
| Controller@Method | `V2\Bill\ListPageController@saveContractPosition` |
| Route name | `ajax.pointSetting.save_contract_position` |
| Middleware | `check_login`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-01 |

### Request params (body)

| Tên | Kiểu | Bắt buộc | Validation | Mô tả |
|-----|------|----------|-----------|-------|
| `order` | array | Có | `required\|array` | Mảng thứ tự bot contract IDs theo vị trí mới |

### Response
```json
{ "status": true }
```

Lỗi:
```json
{ "status": false, "message": "..." }
```

**Độ tin cậy**: Cao — đọc trực tiếp từ `V2\Bill\ListPageController@saveContractPosition` dòng 446-473

---

## EP-10: AJAX hủy chuyển khoản pending

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `POST` |
| URL | `/ajax/point-settings/cancel-univa-charge/{botContractId}/{type?}` |
| Controller@Method | `V2\Bill\ListPageController@cancelTransfer` |
| Route name | `ajax.pointSetting.cancel_transfer_bot_contract` |
| Middleware | `check_login`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-01, SCR-BLP-02 |

### Request params

| Tên | Vị trí | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| `botContractId` | URL path | int | Có | ID hợp đồng |
| `type` | URL path | string | Không | `max-friend` = hủy chuyển khoản max friend |

### Response
```json
{ "status": true }
```
hoặc
```json
{ "status": false }
```

**Độ tin cậy**: Cao — đọc trực tiếp từ `V2\Bill\ListPageController@cancelTransfer` dòng 550-770

---

## EP-11: AJAX lịch sử thanh toán (API cũ — Staff admin)

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `POST` |
| URL | `/ajax/point-settings/payment-history` |
| Controller@Method | `PointSettingController@initDataHistoryPayment` |
| Route name | `point.settings.payment.history` |
| Middleware | `check_login`, `check_remember_token` + nhóm phân quyền cao hơn |
| Auth required | Có |
| Màn hình liên quan | SCR-BLP-03 |

### Request params (body)

| Tên | Kiểu | Bắt buộc | Mô tả |
|-----|------|----------|-------|
| `month` | string | Không | Tháng lọc theo định dạng tiếng Nhật, vd: `2024年06月` |

### Response
```json
{
  "status": true,
  "listPaymentHistory": { ...paginated_data... },
  "totalPagesPdf": 2,
  "listPaymentHistoryAll": [...]
}
```

**Ghi chú**: Endpoint này có vẻ là API cũ, song song với EP-04 dùng cho giao diện mới hơn.

**Độ tin cậy**: Cao — đọc trực tiếp từ `PointSettingController@initDataHistoryPayment` dòng 131-234

---

## EP-12: Trang xác nhận hủy hợp đồng

| Thuộc tính | Giá trị |
|-----------|---------|
| Method | `GET` |
| URL | `/basic/detail-contract/{id}/cancel` |
| Controller@Method | `V2\Bill\ListPageController@confirmCancelView` |
| Route name | `confirmCancel` |
| Middleware | `basic_access`, `https_protocol`, `check_remember_token` |
| Auth required | Có |
| Màn hình liên quan | Màn hình phụ từ SCR-BLP-02 |

### Logic
- Kiểm tra hợp đồng thuộc quyền user hiện tại
- Nếu hợp đồng đã ở trạng thái CANCEL (3) hoặc WAITING_CANCEL (2): redirect về chi tiết hợp đồng
- Nếu hợp đồng không tồn tại: redirect về chi tiết hợp đồng

### Response
- HTML view `basic.bill.confirm_cancel`

**Độ tin cậy**: Cao — đọc trực tiếp từ `V2\Bill\ListPageController@confirmCancelView` dòng 113-132
