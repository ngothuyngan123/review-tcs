# API Spec — FA-026 「単品商品」/「商品販売」 (Bill Item / Sales Management)

> **Nguồn**: đọc trực tiếp `src/web/sns-line/routes/web.php`, `src/web/sns-line/routes/api.php` và các controller Laravel 5.
> **Mức độ tin cậy tổng thể**: **Cao** cho URL / Controller@Method / middleware (đọc trực tiếp route file); **Cao** cho tham số & response (đọc trực tiếp controller + JS gọi API); **Trung bình** cho các suy luận về ngữ nghĩa nghiệp vụ.

---

## 0. Tổng quan phân nhóm

Tính năng có **4 thế hệ code chạy song song** trên cùng một hệ thống:

| Nhóm | Controller | Trạng thái | Nhận diện dữ liệu |
|------|-----------|-----------|-------------------|
| **A. Admin V2 (hiện hành)** | `Basic\SalesManagementV2Controller` | Đang dùng | `s_items.is_product_new = 1` |
| **B. Admin V1 (legacy)** | `Basic\SalesManagementController` | Còn route, phần lớn không dùng | `s_items.is_product_new = 0` |
| **C. Public LINE User** | V2 (`/v2/order-item/*`) + V1 (`/order-item/*`) | V1 đã bị vô hiệu hoá (redirect 404) | — |
| **D. Thanh toán / Webhook / API mobile** | `SalesStripePaymentController`, `WebhookUnivapayControler`, `Api\SalesController` | Đang dùng | — |

---

## 1. Middleware áp dụng

Đọc từ định nghĩa route group trong `src/web/sns-line/routes/web.php`.

| Vị trí group | Prefix | Middleware stack |
|-------------|--------|------------------|
| `routes/web.php:81` | (root) | `NotifyChatworkRequestTimeSlow` — bọc **toàn bộ** các route dưới đây |
| `routes/web.php:822` | (root) | `LogRequestMultipart` |
| `routes/web.php:869` | `basic` | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` |
| `routes/web.php:894` | `basic/sales` | (kế thừa từ `:869`) |
| `routes/web.php:2454` | `ajax` | `check_login`, `check_remember_token` |
| `routes/web.php:2746` | `ajax/sales` | (kế thừa từ `:2454`) |
| `routes/web.php:3735` | `v2` | **Không có middleware auth** — chỉ `NotifyChatworkRequestTimeSlow` + nhóm `web` mặc định |
| `routes/api.php:30` + `:38` | `api/mobile` | `mobile-auth` |

**CSRF** (`src/web/sns-line/app/Http/Middleware/VerifyCsrfToken.php`):
- `/ajax/*` — **được miễn CSRF** (dòng 19)
- `/product-callback/*` — miễn CSRF (dòng 46)
- `/api/mobile/*` — miễn CSRF (dòng 26)
- Các route `/basic/*` và `/v2/order-item/*` **vẫn bị kiểm CSRF** (POST cần token).

> ⚠ **Cảnh báo bảo mật (tin cậy Cao)**: các endpoint AJAX của bill-item V1 nằm ngoài mọi group auth — `/ajax/get-list-data-item` (`web.php:3888`), `/ajax/init-data-action-item` (`:3954`), `/ajax/bill-item-sort-item-setting` (`:3956`), `/ajax/bill-item-save-info-setting` (`:3958`), `/ajax/bill-item-delete-item-friend-info` (`:3960`), `/ajax/get-info-friend-order-index` (`:3962`) và toàn bộ nhóm thanh toán `:3824–4034`. Chúng chỉ dựa vào `botIdCurrent` gửi từ client (nếu có) để chống nhầm bot, **không xác thực đăng nhập**.

### Ý nghĩa middleware (đọc trực tiếp `app/Http/Kernel.php` + class — **Cao**)
| Alias | Class (`app/Http/Middleware/`) | Vai trò |
|-------|-------------------------------|--------|
| `basic_access` | `BasicAccess.php` (`Kernel.php:70`) | Yêu cầu đăng nhập với `role ∈ {1,0,-1,2}`; xác định bot hiện hành; **áp whitelist route cho Staff (bot invite)** — route ngoài whitelist → redirect `adminIndex` kèm lỗi 「この権限は許可されていません。」 (`BasicAccess.php:38-51`); ghi log truy cập Staff vào `user_access_bot` 1 lượt/ngày (`:65-72`) |
| `check_login` | `CheckLogin.php` (`Kernel.php:77`) | Chỉ kiểm tra `Auth::check()`; ⚠ nếu chưa đăng nhập **không redirect** mà trả response rỗng (`CheckLogin.php:20-43`) |
| `check_remember_token` | `CheckRememberToken.php` (`Kernel.php:82`) | So khớp `remember_token_reset_pass`; lệch → logout, AJAX trả JSON 「ログイン情報が変更されましたので、再度ログインしてください。」 |
| `is_expire` | `IsExpire.php` (`Kernel.php:76`) | Chặn khi bot hết hạn / chưa thanh toán → redirect `pointSettings` hoặc `planMaxFriend` |
| `https_protocol` | `HttpsProtocol.php` (`Kernel.php:75`) | ⚠ **Hiện là no-op** — toàn bộ logic redirect HTTPS đã bị comment (`:18-20`) |
| `mobile-auth` | (`Kernel.php:79`) | Xác thực JWT token app mobile |
| `NotifyChatworkRequestTimeSlow` | (`Kernel.php:87`) | Chỉ đo/ghi cảnh báo request chậm — **không phải middleware bảo mật** |

---

## 2. Bảng danh sách endpoints

### 2.1 Nhóm A — Admin V2 · Màn hình HTML (prefix `/basic/sales`)

| ID | Method | URL | Mô tả | Controller@Method | Middleware | Xác thực |
|----|--------|-----|-------|-------------------|-----------|---------|
| EP-01 | GET | `/basic/sales/index` | Màn hình chính, điều hướng tab bằng query `tab` | `SalesManagementV2Controller@index` (`:93`) | `basic_access`, `https_protocol`, `is_expire`, `check_remember_token` | Admin/Staff |
| EP-02 | GET | `/basic/sales/get-single-item-detail/{id}` | 商品詳細 (id là hashid) | `@getItemDetail` (`:259`) | như trên | Admin/Staff |
| EP-03 | GET | `/basic/sales/add-single-item` | ⚠ **Route chết** — method `viewAddSingleItem` **không tồn tại** trong controller | `@viewAddSingleItem` (`web.php:900`) | như trên | Admin/Staff |
| EP-04 | GET | `/basic/sales/preview-invoice/{hashId}` | Xem trước hoá đơn | `@previewInvoice` (`:565`) | như trên | Admin/Staff |
| EP-05 | GET | `/basic/sales/order-history-detail/{hashId}` | 注文詳細 (単品) | `@orderHistoryDetail` (`:1095`) | như trên | Admin/Staff |
| EP-06 | GET | `/basic/sales/cycle-order-history-detail/{hashId}` | 注文詳細 (継続) + 決済履歴 | `@cycleOrderHistoryDetail` (`:1138`) | như trên | Admin/Staff |
| EP-07 | GET | `/basic/sales/set-cookie` | Lưu thư mục đang mở vào cookie `folder_sales` | `Basic\BasicController@folderSetCookie` (`web.php:3709`) | `NotifyChatworkRequestTimeSlow` | (không auth) |
| EP-08 | POST | `/basic/order-history/export-csv-v2` | CSV書出し 単品 | `SalesManagementV2Controller@exportCsvOrderHistory` (`:6918`) | `basic_access`, … | Admin/Staff |
| EP-09 | POST | `/basic/cycle-order-history/export-csv-v2` | CSV書出し 継続 | `@exportCsvCycleOrderHistory` (`:6949`) | `basic_access`, … | Admin/Staff |

### 2.2 Nhóm A — Admin V2 · AJAX

| ID | Method | URL | Mô tả | Controller@Method | Middleware |
|----|--------|-----|-------|-------------------|-----------|
| EP-10 | POST | `/ajax/sales/init-data` | Nạp dữ liệu khởi tạo form thêm/sửa sản phẩm | `@initData` (`:633`) | `check_login`, `check_remember_token` |
| EP-11 | POST | `/ajax/sales/save-settings` | Lưu 事業者・特商法設定 + 最終確認画面 | `@saveSettings` (`:776`) | như trên |
| EP-12 | POST | `/ajax/sales/save-item` | Tạo / cập nhật sản phẩm | `@saveItem` (`:849`) | như trên |
| EP-13 | GET | `/ajax/sales/get-item-detail/{id}` | Lấy chi tiết sản phẩm (JSON) | `@ajaxGetItemDetail` (`:292`) | như trên |
| EP-14 | POST | `/ajax/sales/get-list-order-history` | Danh sách 販売履歴 (phân trang 20) | `@ajaxListOrderHistory` (`:1209`) | như trên |
| EP-15 | POST | `/ajax/sales/get-init-data-tab-setting` | Nạp folder + sản phẩm cho modal 絞り込み設定 | `@ajaxGetInitDataTabSetting` (`:1381`) | như trên |
| EP-16 | POST | `/ajax/sales/cancel-cycle-order` | 解約 1 hợp đồng định kỳ | `@cancelCycleOrder` (`:1047`) | như trên |
| EP-17 | POST | `/ajax/sales/cancel-order-multiple` | 一括返金実行 (単品) | `@cancelOrderMultiple` (`:3519`) | như trên |
| EP-18 | POST | `/ajax/sales/cancel-cycle-order-multiple` | 一括解約実行 (継続) | `@cancelCycleOrderMultiple` (`:3533`) | như trên |
| EP-19 | POST | `/ajax/sales/copy-item/{id}` | Sao chép sản phẩm | `@ajaxCopyItem` (`:1408`) | như trên |
| EP-20 | POST | `/ajax/sales/ini-setting-univapay` | Lưu & kiểm tra thông tin UnivaPay | `@iniSettingUnivapay` (`:3713`) | như trên |
| EP-21 | POST | `/ajax/sales/unlink-payment-method` | Huỷ liên kết Stripe/UnivaPay (cần mật khẩu) | `@unlinkPaymentMethod` (`:6867`) | như trên |
| EP-22 | POST | `/ajax/sales/get-sales-history` | 販売履歴 theo tháng trong 商品詳細 | `@ajaxGetSalesHistory` (`:491`) | như trên |
| EP-23 | POST | `/ajax/upload-file` | Upload ảnh sản phẩm | `@uploadFile` (`:569`) | `check_login`, `check_remember_token` |
| EP-24 | POST | `/ajax/get-list-group-products` | CRUD folder + sắp xếp + di chuyển + xoá sản phẩm (đa hành động) | `@ajaxGetListGroupProducts` (`:315`) | `check_login`, `check_remember_token` |
| EP-25 | POST | `/ajax/cancel-order-v2` | Huỷ / hoàn tiền 1 đơn 単品 (dùng ở 注文詳細) | `@cancelOrderV2` (`:3192`) | ⚠ **không auth** (`web.php:3849`) |
| EP-26 | GET | `/sales/stripe/production/connect` | Redirect OAuth Stripe (本番) | Closure (`web.php:3865`) | `NotifyChatworkRequestTimeSlow` |
| EP-27 | GET | `/sales/stripe/test/connect` | Redirect OAuth Stripe (テスト) | Closure (`web.php:3873`) | `NotifyChatworkRequestTimeSlow` |

### 2.3 Nhóm B — Admin V1 legacy

| ID | Method | URL | Mô tả | Controller@Method (`SalesManagementController`) | Middleware |
|----|--------|-----|-------|------------------------------------------------|-----------|
| EP-30 | GET | `/basic/list-items` | Màn hình liên kết thanh toán + callback OAuth Stripe | `@linkPayment` (`:66`) | `basic_access`, … |
| EP-31 | GET | `/basic/list-items-old` | Danh sách sản phẩm cũ (`is_product_new = 0`) | `@listItemOld` (`:294`) | `basic_access`, … |
| EP-32 | GET | `/basic/list-item/check-step3-stripe` | Đánh dấu hoàn tất bước 3 Stripe | `@checkStep3Stripe` (`:533`) | `basic_access`, … |
| EP-33 | GET | `/basic/list-item/change-valid-item` | Bật/tắt công khai sản phẩm | `@changeValidItem` (`:557`) | `basic_access`, … |
| EP-34 | GET | `/basic/add-item` | Form thêm sản phẩm (V1) | `@addItem` (`:578`) | `basic_access`, … |
| EP-35 | POST | `/basic/store-item` | Lưu sản phẩm mới (V1) | `@storeItem` (`:604`) | `basic_access`, … |
| EP-36 | GET | `/basic/edit-item/{id}` | Form sửa sản phẩm (V1) | `@editItem` (`:784`) | `basic_access`, … |
| EP-37 | POST | `/basic/save-item/{id}` | Cập nhật sản phẩm (V1) | `@saveItem` (`:806`) | `basic_access`, … |
| EP-38 | GET | `/basic/item-monthly/{id}` | Thống kê theo tháng (`s_monthly_item`) | `@itemMonthly` (`:1110`) | `basic_access`, … |
| EP-39 | GET | `/basic/order-history` | Danh sách đơn 単品 (V1) | `@orderHistory` (`:1123`) | `basic_access`, … |
| EP-40 | GET | `/basic/cycle-order-history` | Danh sách đơn 継続 (V1) | `@cycleOrderHistory` (`:1155`) | `basic_access`, … |
| EP-41 | GET | `/basic/order-history/edit/{id}` | Sửa thông tin khách của đơn 単品 | `@editOrder` (`:1187`) | `basic_access`, … |
| EP-42 | GET | `/basic/cycle-order-history/edit/{id}` | Sửa thông tin khách của đơn 継続 | `@editCycleOrder` (`:1229`) | `basic_access`, … |
| EP-43 | GET | `/basic/order-history/export-csv` | CSV 単品 (V1, đồng bộ) | `@exportCsvOrderHistory` (`:1141`) | `basic_access`, … |
| EP-44 | GET | `/basic/cycle-order-history/export-csv` | CSV 継続 (V1, đồng bộ) | `@exportCsvCycleOrderHistory` (`:1173`) | `basic_access`, … |
| EP-45 | POST | `/ajax/sort-items` | Sắp xếp thứ tự sản phẩm (V1) | `@sortItems` (`:517`) | `check_login`, `check_remember_token` |
| EP-46 | POST | `/ajax/get-list-data-item` | Danh sách sản phẩm V1 (JSON) | `@ajaxGetDataListItems` (`:453`) | ⚠ **không auth** |
| EP-47 | POST | `/ajax/save-order` | Lưu thông tin khách của đơn 単品 | `@saveOrder` (`:1204`) | ⚠ **không auth** |
| EP-48 | POST | `/ajax/save-cycle-order` | Lưu thông tin khách của đơn 継続 | `@saveCycleOrder` (`:1252`) | ⚠ **không auth** |
| EP-49 | POST | `/ajax/cancel-order` | Huỷ + refund đơn 単品 (V1) | `@cancelOrder` (`:1381`) | ⚠ **không auth** |
| EP-50 | POST | `/ajax/cancel-cycle-order` | Huỷ hợp đồng 継続 (V1) | `@cancelCycleOrder` (`:1277`) | ⚠ **không auth** |
| EP-51 | POST | `/ajax/init-data-action-item` | Nạp cấu hình エルメアクション của item V1 | `@initDataActionItem` (`:1760`) | ⚠ **không auth** |
| EP-52 | POST | `/ajax/bill-item-sort-item-setting` | Sắp xếp mục お客様情報 | `@ajaxBillItemSortItemSetting` (`:1898`) | ⚠ **không auth** |
| EP-53 | POST | `/ajax/bill-item-save-info-setting` | Lưu 1 mục お客様情報 | `@ajaxBillItemSaveInfoSetting` (`:1926`) | ⚠ **không auth** |
| EP-54 | POST | `/ajax/bill-item-delete-item-friend-info` | Xoá 1 mục お客様情報 | `@ajaxBillItemDeleteFriendInfo` (`:1968`) | ⚠ **không auth** |
| EP-55 | POST | `/ajax/get-info-friend-order-index` | Lấy giá trị thông tin bạn bè cho trang đặt hàng | `@getConfigUserOrder` (`:2001`) | ⚠ **không auth**, `bot_id` lấy từ request |

> `SalesManagementController@addOrEditCategoryItem` (`:2047`) **không có route nào trỏ tới** → dead code.

### 2.4 Nhóm C — Public LINE User

**V2 (đang dùng)** — prefix `v2`, không middleware auth (`web.php:3735`):

| ID | Method | URL | Mô tả | Controller@Method |
|----|--------|-----|-------|-------------------|
| EP-60 | GET | `/v2/order-item/detail/{item_code}/{u_code?}` | 商品ページ (trang bán hàng) | `SalesManagementV2Controller@orderDetail` (`:1550`) |
| EP-61 | GET | `/v2/order-item/index/{item_code}/{u_code?}` | ⚠ **Route chết** — method `orderIndex` **không tồn tại** trong V2 | `@orderIndex` (`web.php:3738`) |
| EP-62 | GET | `/v2/order-item/cancel/{item_code}/{u_code?}` | 解約用ページ | `@orderCancel` (`:1727`) |
| EP-63 | GET | `/v2/order-item/change/{item_code}/{u_code?}` | カード情報変更ページ | `@orderChange` (`:1820`) |
| EP-64 | GET | `/v2/order-item/info-store/{type?}` | 特定商取引法に基づく表記 | `@detailStoreInfo` (`:545`) |
| EP-65 | GET | `/v2/order-item/enter-friend-info/{item_code}/{u_code?}` | お客様情報入力 | `@viewEnterFriendInfo` (`:1965`) |
| EP-66 | GET | `/v2/order-item/enter-payment-info/{item_code}/{u_code?}` | カード情報入力 | `@viewEnterPaymentInfo` (`:2091`) |
| EP-67 | POST | `/v2/order-item/confirm-order/{item_code}/{u_code?}` | 最終確認画面 | `@confirmOrder` (`:2246`) |

**V1 (đã vô hiệu hoá)** — `SalesManagementController`:

| ID | Method | URL | Trạng thái |
|----|--------|-----|-----------|
| EP-70 | GET | `/order-item/detail/{item_code}/{u_code}` | Còn sống; nếu `is_product_new = 1` → redirect sang `v2.orderDetail` (`:1503`) |
| EP-71 | GET | `/order-item/index/{item_code}/{u_code}` | **`redirect()->route('404')` ngay dòng đầu** (`:1572`) |
| EP-72 | GET | `/order-item/cancel/{item_code}/{u_code}` | **redirect 404** (`:1635`) |
| EP-73 | GET | `/order-item/change/{item_code}/{u_code}` | **redirect 404** (`:1690`) |

### 2.5 Nhóm D — Thanh toán (public, không auth)

| ID | Method | URL | Mô tả | Controller@Method |
|----|--------|-----|-------|-------------------|
| EP-80 | POST | `/ajax/payment-intent` | Tạo Stripe PaymentIntent/SetupIntent + tạo bản ghi order tạm | `SalesManagementV2Controller@paymentIntent` (`:2408`) |
| EP-81 | POST | `/ajax/payment-credit-card-item-v2` | Hoàn tất đơn sau khi PaymentIntent thành công (Stripe) | `SalesStripePaymentController@paymentCreditCardItemV2` (`:597`) |
| EP-82 | POST | `/ajax/payment-credit-card-item-v2-univapay` | Thanh toán qua UnivaPay (toàn bộ luồng) | `SalesManagementV2Controller@paymentCreditCardItemV2Univapay` (`:4847`) |
| EP-83 | POST | `/ajax/items/delete-order-confirm-fail` | Xoá bản ghi order tạm khi confirm thẻ thất bại | `@deletePaymentOrderConfirmFail` (`:4833`) |
| EP-84 | POST | `/ajax/update-payment-intent` | Đổi thẻ + retry bill quá hạn (Stripe) | `@updatePaymentIntent` (`:5994`) |
| EP-85 | POST | `/ajax/change-card-item/v2` | Ghi nhận thẻ mới / xử lý kết quả bill lại (Stripe) | `@changeCardItem` (`:6154`) |
| EP-86 | POST | `/ajax/change-card-univapay/v2` | Đổi thẻ + retry bill quá hạn (UnivaPay) | `@changeCardUnivapay` (`:6488`) |
| EP-87 | POST | `/ajax/mobile/cancel-cycle-order` | LINE User tự huỷ hợp đồng định kỳ | `@cancelCycleOrder` (`:1047`) |
| EP-88 | POST | `/ajax/get-ucode-by-line-user-id` | Lấy `u_code` từ `lineId` (LIFF) | `@getUcodeByLineUserId` (`:1688`) |
| EP-89 | POST | `/ajax/univapay/sales/call-create-customer-id` | Tạo `customer_id` bên UnivaPay | `@createCustomerIdUnivapay` (`:3749`) |
| EP-90 | POST | `/ajax/payment-credit-card-item` | Thanh toán Stripe **V1 legacy** | `SalesStripePaymentController@paymentCreditCardItem` (`:58`) |
| EP-91 | POST | `/ajax/change-card-item` | Đổi thẻ **V1 legacy** | `SalesStripePaymentController@changeCardItem` (`:1533`) |

### 2.6 Nhóm E — Webhook

| ID | Method | URL | Mô tả | Controller@Method |
|----|--------|-----|-------|-------------------|
| EP-94 | POST | `/mobile/univapay-callback-payment` | ★ **Webhook UnivaPay thực sự đang hoạt động**. Chỉ xử lý `event == 'charge_finished'` và `metadata.module ∈ {sales, sales_change_card, sales_job, lesson, salon, event-booking, …}` (`:18-29`) → `HandleWebhookUnivapay::dispatch($data, 'univapay')` (`:34`). **Luôn trả `{"status":"success"}`** (`:38-40`) | `WebhookUnivapayControler@webhook` (`web.php:4020`) |
| EP-95 | POST | `/product-callback/{bot_id}` | ⚠ **Thân hàm đã bị comment out hoàn toàn** (`SalesManagementV2Controller@callback` `:3806–3885`) — luôn trả `{"status": true}` mà không xử lý gì | `@callback` (`web.php:4034`) |

> Cả 2 endpoint đều được **miễn CSRF** (`VerifyCsrfToken.php:47` cho `/mobile/univapay-callback-payment`, `:46` cho `/product-callback/*`) và **không có middleware xác thực**.

### 2.7 Nhóm F — API mobile (app エルメ)

Prefix `api/mobile`, middleware `mobile-auth` (`routes/api.php:30`, `:38`).

| ID | Method | URL | Mô tả | Controller@Method |
|----|--------|-----|-------|-------------------|
| EP-96 | POST | `/api/mobile/get-history-sales` | Lịch sử mua hàng của 1 LINE User (phân trang 15) | `Api\SalesController@getHistorySales` (`:17`) |
| EP-97 | POST | `/api/mobile/get-detail-order` | Chi tiết 1 đơn | `Api\SalesController@getOrderDetail` (`:76`) |
| EP-98 | POST | `/api/mobile/get-detail-order-notify` | Chi tiết đơn từ thông báo (`s_order_history_notify`) | `Api\SalesController@getNotifyOrderDetail` (`:184`) |

---

## 3. Chi tiết endpoints quan trọng

### EP-01 · GET `/basic/sales/index`

`src/web/sns-line/app/Http/Controllers/Basic/SalesManagementV2Controller.php:93`

**Request params (query string)**

| Tên | Vị trí | Kiểu | Bắt buộc | Validation thực tế | Ghi chú |
|-----|--------|------|---------|-------------------|--------|
| `tab` | query | string | Không | Không validate; mặc định `'list-item'` (`:122-124`) | `list-item` / `sales-history` / `setting` / `add-item` / `edit-item` |
| `typePayment` | query | int | Không | Không validate | `0` = 単品商品, khác 0 = 継続商品 |
| `flag_environment` | query | int | Không | Không validate | `0` = テスト環境, `1` = 本番環境 |
| `s_category_id` | query | int | Không | mặc định `0` (`:229`) | Folder đang mở |
| `itemId` | query | string (hashid) | Không | `Hashids::decode()` (`:142`); item không tồn tại → `redirect()->route('404')` (`:145`) | Chỉ dùng khi `tab=edit-item` |
| `code`, `state` | query | string | Không | Không dùng thực tế (chỉ gán biến `:151-152`) | Tàn dư OAuth Stripe |

**Response**: HTML view `basic.sales.v2.index` (`:227`) với các biến `tab`, `typePayment`, `folderCookie`, `categories`, `itemCode`, `flagStripe`, `storeSettings`, `univapayLinked`, `emailStripe`, `emailUnivapay`, `univapayWebhook`, `maxItemBillOne`, `maxItemBillCycle`, `contractType`, `accountPayment`, `univapayAppId`, `liffAppId`, `timestamp`…

**Side effect**: ghi cookie `folder_sales` TTL 14400 phút, path `/basic/sales/index` (`:111`).

**Lỗi có thể xảy ra**

| HTTP | Trường hợp |
|------|-----------|
| 302 → `route('404')` | `itemId` hashid không giải mã được hoặc item không tồn tại (`:145`) |
| 302 | Middleware `is_expire` chặn khi hợp đồng bot hết hạn |

---

### EP-12 · POST `/ajax/sales/save-item`

`SalesManagementV2Controller.php:849` — endpoint quan trọng nhất của tính năng.

**Content-Type**: `application/json` (JS gửi `JSON.stringify(product)` — `public/js/sales/v2/add-single-item.js:473-479`).

**Request params** — controller lấy qua `$request->only([...])` (`:853-894`):

| Tên | Kiểu | Bắt buộc | Validation server | Validation client (`add-single-item.js`) |
|-----|------|---------|------------------|------------------------------------------|
| `id` | int | Không | Có → update, không → create (`:940`) | — |
| `name` | string | — | **Không validate** | required + `maxLength 20` (`:605`) — 「商品名は20文字以内で入力してください。」 |
| `product_name` | string | — | Không validate | required + `maxLength 50` (`:606`) |
| `supplement_product` | string | — | Không validate | required + `maxLength 50` (`:607`) |
| `amount` | int | — | Không validate | required + `min 100` (`:608`) — 「請求価格は100円以上を設定してください。」 |
| `s_category_id` | int | Có | Nếu `!= 0` phải tồn tại trong `s_categories` cùng `bot_id`, ngược lại trả lỗi (`:896-905`) | required |
| `item_code` | string | — | Không validate (sinh sẵn 10 ký tự) | — |
| `payment_method` | `stripe`\|`univapay` | — | Không validate | required (`:613`) |
| `flag_environment` | 0\|1 | — | Không validate | — |
| `type_payment` | 0..5 | — | Quyết định nhánh xử lý (`:907`) | — |
| `tax_item` | int (10\|8) | — | Không validate | mặc định `10` (`:98`) |
| `quantity_stock` | int | Khi `flag_use_stock=1` | Không validate | `min 0` (`:620`) |
| `max_per_person` | int | Khi `flag_use_max_per_person=1` | **Không validate và KHÔNG enforce ở server** | `min 1` (`:624`) |
| `flag_use_stock`, `flag_show_stock`, `flag_use_max_per_person`, `flag_show_max_per_person` | 0\|1 | — | — | — |
| `page_start_simple`, `final_confirm_page`, `page_end_simple`, `flag_page_end`, `url_page_outsite_end` | text | — | — | `flag_page_end=1` → `url_page_outsite_end` phải là URL (`:628`); `=0` → `page_end_simple` required |
| `image_product` | array | Không | `implode(',', ...)` (`:948`, `:963`); rỗng → `null` (`:969`) | tối đa theo UI |
| `text_button_start`, `color_button_start`, `color_text_button_start` | string | — | — | `text_button_start` maxLength 15 (`:610`) |
| `text_button_friend_info`, `color_button_friend_info`, `bg_button_friend_info` | string | — | — | maxLength 15 (`:612`) |
| `text_confirm_button`, `bg_confirm_button`, `color_confirm_button` | string | — | — | maxLength 15 (`:614`) |
| `text_payment_button`, `bg_payment_button`, `color_payment_button` | string | — | — | maxLength 15 (`:615`) |
| `action_show_page_id`, `number_action_show_page`, `action_contract_id`, `number_action_contract` | int | — | — | — |
| `listFriendInfo` | array | Không | Đồng bộ vào `b_c_info_setting`; mục thiếu trong payload sẽ bị **xoá** (`:1004-1006`) | — |

**Chỉ khi `type_payment != 0`** (`:907-930`) mới nhận thêm: `action_purchase_1st_id`, `number_action_purchase_1st`, `action_purchase_2st_id`, `number_action_purchase_2st`, `auto_action_purchase_2st`, `action_buy_error_id`, `number_action_buy_error`, `action_contract_trial_id`, `number_action_contract_trial`, `number_day_action_contract_trial`, `action_cancel_payment_id`, `number_action_cancel_payment`, `text_button_cancel`, `color_button_cancel`, `color_text_button_cancel`, `page_cancel`, `number_charge`, `auto_cancel`, `flag_trial`, `time_trial`, `amount_first`, `flag_first`.

> `action_contract_trial_id` và `time_trial` chỉ được ghi khi `flag_trial == 1`, ngược lại ghi `null` (`:915`, `:927`).

**Request mẫu**
```json
{
  "id": null,
  "name": "オンライン講座",
  "product_name": "オンライン講座（全5回）",
  "supplement_product": "初心者向け",
  "amount": 5000,
  "tax_item": 10,
  "payment_method": "univapay",
  "type_payment": 2,
  "flag_environment": 1,
  "s_category_id": 0,
  "item_code": "a1B2c3D4e5",
  "quantity_stock": 100,
  "flag_use_stock": 1,
  "flag_show_stock": 1,
  "max_per_person": 1,
  "flag_use_max_per_person": 1,
  "flag_show_max_per_person": 1,
  "flag_trial": 1,
  "time_trial": 7,
  "flag_first": 1,
  "amount_first": 100,
  "number_charge": 0,
  "auto_cancel": 1,
  "flag_page_end": 2,
  "page_start_simple": "<p>...</p>",
  "final_confirm_page": "<p>...</p>",
  "image_product": ["/media/images/1/2/bill-item/abc.png"],
  "text_button_start": "お客様情報入力にすすむ",
  "listFriendInfo": [
    {"id": null, "title": "お名前", "type": 1, "setting": "newname", "is_require": 1, "order_index": 1, "friend_info_id": -1, "is_default": 1}
  ]
}
```

**Response thành công** (`:1032-1036`)
```json
{
  "status": true,
  "product": { "id": 123, "item_code": "a1B2c3D4e5", "...": "...", "listFriendInfo": [], "hashId": "kXe9..." },
  "message": "変更されました。"
}
```

**Lỗi**

| HTTP | Body | Nguyên nhân |
|------|------|------------|
| 200 | `{"status": false, "message": "選択したフォルダーは、現在存在していません。"}` | `s_category_id` không thuộc bot (`:903`) |
| 200 | `{"status": false, "message": "現在のプランは利用できない機能です。アップグレードが必要になります。"}` | Vượt giới hạn gói khi tạo mới (`:956-959`) |
| 200 | `{"status": false, "message": "<exception message>"}` | Exception bất kỳ (`:1042`) |

---

### EP-14 · POST `/ajax/sales/get-list-order-history`

`SalesManagementV2Controller.php:1209` (`?page=N` để phân trang).

| Tên | Kiểu | Mặc định | Ý nghĩa |
|-----|------|---------|--------|
| `type_payment` | int | — | `0` → truy vấn `s_order_history`; khác 0 → `s_cycle_order_history` |
| `flag_environment` | 0\|1 | — | Lọc 本番/テスト |
| `beforeDate` | `Y-m-d` | hôm nay (`:1214`) | Đầu khoảng ngày |
| `currentDate` | `Y-m-d` | hôm nay (`:1215`) | Cuối khoảng ngày |
| `keyword` | string | null | Tìm theo `line_user.name`, `line_user.view_name`, `s_items.name`, id đơn |
| `payment_method` | string\|`-1` | — | `-1` = 全て; ngược lại lọc `s_items.payment_method` |
| `status_bill` | int\|`-1` | — | Chỉ dùng cho 単品 → lọc `s_order_history.status_order` |
| `statusBillMany` | int[] | — | Chỉ dùng cho 継続: `1` 契約中, `2` トライアル, `3` 解約, khác = 期限切れ (`:1266-1294`) |
| `productIds` | int[] | — | Lọc theo sản phẩm |
| `page` | query int | 1 | Phân trang, 20/trang (`:1362`) |

**Response** (`:1375-1378`)
```json
{
  "listOrderHistory": {
    "current_page": 1, "per_page": 20, "total": 57,
    "data": [ { "id": 1001, "hashId": "3xKw...", "name_item": "...", "amount_order": 5000,
                "status_order": 1, "payment_date": "2026-07-01 10:00:00",
                "line_user_name": "...", "lineUser": {"id":1,"view_name":"…","avatar_url":"…"} } ]
  },
  "accountPayment": "acct_xxx"
}
```

**Lưu ý**: khoảng ngày với 継続 dùng điều kiện `OR` giữa `last_bill_time` và `c_register_date` (`:1238-1247`) — **Cao**.

---

### EP-24 · POST `/ajax/get-list-group-products`

`SalesManagementV2Controller.php:315` — endpoint đa hành động điều khiển sidebar folder + thao tác sản phẩm.

| `action` | Params bổ sung | Hành vi |
|---------|----------------|--------|
| *(rỗng)* | — | Chỉ trả về danh sách |
| `addAndEditGroup` | `id`, `group_name`, `typePayment` | Có `id` tồn tại → đổi tên; không → tạo folder mới (`type_payment` = 0 hoặc 2), `position = max+1` (`:330-357`) |
| `deleteItem` | `item_id` | Xoá 1 sản phẩm (`:358-371`) |
| `deleteGroup` | `group_id` | Xoá folder **và toàn bộ sản phẩm bên trong** (`:372-383`) |
| `renameGroup` | `group_id`, `group_name` | ⚠ Update bảng `category` (không phải `s_categories`) — **nghi vấn bug** (`:390`) |
| `sortItem` | `items[]` | Ghi lại `position` theo thứ tự đảo ngược (`:394-404`) |
| `sortFolder` | `sort_ids`, `sort_position` | Sắp xếp folder (`:405-415`) |
| `moveItem` | `item_ids[]`, `folder_move_id` | Di chuyển sản phẩm sang folder khác (`:416-436`) |

Params chung: `group_id`, `typePayment`, `paymentMethod`, `flag_environment`.

**Response** (`:476-482`)
```json
{ "status": true, "groups": [{"id":1,"name":"…","position":3,"count":5}],
  "items": [{"id":10,"name":"…","totalBuy":12,"...":"…"}],
  "group_open": 1, "count_default": 4 }
```
**Lỗi**: `{"status": false, "msg": "<message>"}` HTTP **200** (`:487`).

---

### EP-16 · POST `/ajax/sales/cancel-cycle-order` (và EP-87 `/ajax/mobile/cancel-cycle-order`)

`SalesManagementV2Controller.php:1047`

| Tên | Kiểu | Ghi chú |
|-----|------|--------|
| `cycle_order_id` | int | Bắt buộc |
| `flagExecuteAction` | 0\|1 | 1 = có chạy エルメアクション「解約時」 |
| `user_cancel` | string | `'customer'` khi LINE User tự huỷ → luôn chạy action huỷ (`:1071`) |
| `type_cancel` | string | Chỉ dùng ở JS, controller không đọc |

**Response**: `{"success": true|false}` HTTP 200 (`:1083`).
**Lỗi nghiệp vụ** (`:1058-1064`): nếu `status_webhook ∈ {0 UNPROCESSED, 3 TIMEOUT, 4 TIMEOUT_WEBHOOK}` →
```json
{"success": false, "error_message": "決済処理を行っていますので、操作できません。"}
```

---

### EP-17 / EP-18 · Huỷ hàng loạt

| Endpoint | Params | Response |
|----------|--------|---------|
| `/ajax/sales/cancel-order-multiple` (`:3519`) | `orderIds[]`, `autoRefund` (0\|1) | `{"success": true}` — luôn true, kể cả khi từng đơn lỗi |
| `/ajax/sales/cancel-cycle-order-multiple` (`:3533`) | `cycleOrderIds[]`, `flagExecuteAction` (0\|1) | `{"success": true}` — exception từng đơn bị nuốt và chỉ ghi log (`:3557`) |

---

### EP-11 · POST `/ajax/sales/save-settings`

`SalesManagementV2Controller.php:776`

| Tên | Kiểu | Ghi chú |
|-----|------|--------|
| `general_settings` | HTML | Nội dung 最終確認画面 |
| `info_store` | HTML | 事業者・特商法設定 |

Controller nhận **toàn bộ** `$request->input()` rồi `update()`/`create()` trên `s_store_settings` — model `guarded = []` → **mass assignment không giới hạn** (tin cậy Cao, `:781-790`).

**Response**: `{"status": true, "message": "変更されました。"}` (`config/messages.php:3`) / `{"status": false}` (`:804`).

---

### EP-20 · POST `/ajax/sales/ini-setting-univapay`

`SalesManagementV2Controller.php:3713`

| Tên | Kiểu | Ghi chú |
|-----|------|--------|
| `univapay_app_token` | string | Bắt buộc (validate ở client) |
| `univapay_secret` | string | Bắt buộc |
| `univapay_webhook` | string | URL webhook |

Gọi `UnivapayPayment::getAccountInfo($secret, $appToken)`; thành công → lưu `univapay_app_id` từ response và upsert `s_strip_bot` (`:3725-3734`).

**Response**: `{"status": true, "email": "...", "message": "..."}` hoặc `{"status": false, "message": "<error_message>"}`.

---

### EP-21 · POST `/ajax/sales/unlink-payment-method`

`SalesManagementV2Controller.php:6867`

| Tên | Kiểu | Ghi chú |
|-----|------|--------|
| `password` | string | Mật khẩu tài khoản đăng nhập, đối chiếu `Hash::check(..., Auth::user()->password)` (`:6871`) |
| `type` | `stripe`\|khác | `stripe` → xoá 6 cột khoá Stripe; khác → xoá 4 cột UnivaPay |

**Response**: `{"status": true}` / `{"status": false, "error": "パスワードが間違っています。"}`.

---

### EP-80 · POST `/ajax/payment-intent`

`SalesManagementV2Controller.php:2408` — bước 1 của luồng thanh toán Stripe.

| Tên | Kiểu | Ghi chú |
|-----|------|--------|
| `amount` | int | **Số lượng mua** (không phải số tiền) |
| `item_id` | int | ID sản phẩm |
| `u_code` | string | Định danh `bot_line_user` |
| `listInfoSetting` | JSON string | Thông tin khách nhập |
| `email_default`, `name_default` | string | Dùng để tạo Stripe Customer |
| `aff_id`, `lp_id`, `aff_setting_id` | int | Affiliate |

Số tiền được tính ở server (`:2437-2449`): `amount = đơn giá × quantity`; với 継続 áp dụng `amount_first` khi `flag_first = 1`, và `0` khi có trial mà không có giá đầu.

**Response thành công** (`:2664-2673`)
```json
{ "status": true, "charge": {"status": true, "responseIntent": {"id": "pi_…", "client_secret": "pi_…_secret_…", "status": "requires_confirmation"}},
  "setupIntent": null, "pmId": "pm_…", "error_message": null,
  "flagPayment": true, "cycleId": 55, "orderId": 987 }
```

**Lỗi**

| Body | Nguyên nhân |
|------|------------|
| `{"result":"error","error_message":"購入数量は1以上で入力してください。"}` | `quantity <= 0` (`:2429-2433`) |
| `{"result":"error","error_message":"在庫切りです。{n}以下入力してください"}` | Vượt tồn kho (`:2566`) |
| `{"result":"error","error_message":"在庫がないので、購入できません。販売者に連絡してください。"}` | Hết hàng (`:2569`) |
| `{"status": false, ... "error_message": "<msg Nhật>"}` | Tạo Stripe Customer / attach payment method thất bại (`:2497`, `:2509`) |

Tất cả đều HTTP **200**.

---

### EP-81 · POST `/ajax/payment-credit-card-item-v2`

`SalesStripePaymentController.php:597` — bước 2 (ghi nhận kết quả PaymentIntent).

Params: `item_id`, `u_code`, `charge_id` (PaymentIntent id), `listInfoSetting`, `amount` (số lượng), `flagPayment`, `cycleId`, `orderId`, `aff_id`, `aff_setting_id`.
Session dùng: `stripeSalesV2.token_id`, `stripeCustomerV2` (`customer_id`, `last4`, `brandName`, `pm_id`).

**Response** (`:1491-1495`): `{"result": "success"|"error", "error_message": ..., "urlRedirectChat": ...}` — HTTP luôn 200.
Thông điệp lỗi: `"Item bill does not exist"` (`:650`), `"Item or Bot - not exist"` (`:673`), `"create customer error"` (`:724`), `"error"` (`:1503`).

---

### EP-82 · POST `/ajax/payment-credit-card-item-v2-univapay`

`SalesManagementV2Controller.php:4847`

Params: `item_id`, `u_code`, `amount` (số lượng), `listInfoSetting` (JSON string), `aff_id`, `lp_id`, `aff_setting_id`.
Session: `univapaySalesV2` (`token`, `customer_id`, `customer_code`, `installment_count`).

**Response** (`:5956-5960`)
```json
{ "result": "success" | "error" | "pending", "error_message": "", "urlRedirectChat": "https://line.me/R/..." }
```
- `pending`: đơn đã gửi lên UnivaPay nhưng webhook chưa xác nhận sau 5 lần thử (`:5059-5067`) → UI hiển thị màn hình chờ `wait-process.blade.php`.
- Lỗi: `{"result":"error","error_message":"購入数量は1以上で入力してください。"}` (`:4915`), lỗi tồn kho (`:4943-4945`), thông điệp UnivaPay dịch qua `getMessageErrorUnivapay()` (`:2676`).
- Exception → HTTP **400** với `{"result":"error","error_message":"<msg>--line: <n>"}` (`:5965`).

---

### EP-88 · POST `/ajax/get-ucode-by-line-user-id`

`SalesManagementV2Controller.php:1688`

| Tên | Kiểu | Ghi chú |
|-----|------|--------|
| `lineId` | string | LINE user id |
| `botId` | int | |
| `retry` | int | Mặc định 15 (`:1691`) — số lần thử kiểm tra bạn bè |

**Response**: `{"status": true, "uCode": "…"}` / `{"status": false, "url": "<url_add_friend>"}` / `{"status": false, "msgError": "商品販売ページ中に「ページ貼り付けJavaScriptタグ」…"}`.

---

### EP-08 / EP-09 · Xuất CSV V2

`SalesManagementV2Controller.php:6918`, `:6949` — nhận **cùng bộ params như EP-14** (vì gọi lại `ajaxListOrderHistory($request, true)`) cộng thêm:

| Tên | Kiểu | Ghi chú |
|-----|------|--------|
| `list_order_id_selected` | string (CSV id) | Nếu có → chỉ xuất các đơn được tick |

**Response**: file CSV tải trực tiếp (`Maatwebsite\Excel`), tên `単品商品販売履歴_{botName}_{YmdHis}.csv` / `継続商品販売履歴_{botName}_{YmdHis}.csv`. **Đồng bộ, không qua queue, không ghi bảng `csv_management`** (tin cậy Cao).

---

### EP-35 / EP-37 · V1 `store-item` / `save-item/{id}`

`SalesManagementController.php:604`, `:806` — có Form validation thực sự bằng `Validator::make` trong `validateItem()` (`:1002`):

| Field | Rule | Message |
|-------|------|--------|
| `name` | `required` | 「商品名を入力してしてください。」 |
| `amount` | `required\|numeric\|min:50` | 「課金金額は５０円以上入力してください。」 |
| `amount1st` | `required\|numeric\|min: 50` (khi `charge_type=subscr` và `amount1st_flag=1`) | 「初回課金金額は５０円以上入力してください。」 |
| `freetrial_days` | `required\|numeric\|min: 1` (khi `freetrial_days_flag=1`) | 「トライアル日数は1日以上入力してください。」 |
| `product_name`, `body_page_start`, `text_button_start` | `required` khi `flag_page_start=0` | — |
| `url_page_start` | `required\|url` khi `flag_page_start=1` | 「URLのフォーマットで入力してください。」 |
| `body_page_end` / `url_page_end` | `required` / `required\|url` theo `flag_page_end` | — |
| `body_page_cancel`, `text_button_cancel` | `required` khi `charge_type=subscr` | — |

> V1 **không có** rule 100円, không có giới hạn ký tự (`max:`), không có tồn kho / 購入上限 / thuế.

**Response**: `{"success": true}` / `{"success": false, "errors": {...}}` / `{"success": false, "msgBot": "..."}` / HTTP **500** `{"status": false, "msg": "<MESSAGE_NOTIFY_BACKUP>"}` khi đang backup (`:611-618`).

---

### EP-96 · POST `/api/mobile/get-history-sales`

`Api\SalesController.php:17`

| Tên | Kiểu |
|-----|------|
| `botId` | int |
| `lineUserId` | int |
| `typePayment` | int (0 = 単品, khác = 継続) |

Chỉ lấy dữ liệu **本番** (`flag_environment = 1` cả ở `s_items` lẫn bảng lịch sử — `:27`, `:30`) và `is_product_new = 1` (`:28`).

**Response**
```json
{ "result": "ok",
  "data": { "list_history": [{"id":1,"name_item":"…","created_at":"…","status_order":1,"status_text":"…"}],
            "pagination": {"current_page":1,"last_page":3,"per_page":15,"total":40} } }
```

---

## 4. Liên kết endpoint ↔ màn hình UI

| Màn hình UI | Endpoint sử dụng |
|-------------|------------------|
| Tab 商品一覧 (list-item) — sub-tab 単品商品/継続商品, toggle 本番/テスト, filter 表示設定, sidebar folder | EP-01 (`?tab=list-item`), EP-24 (`/ajax/get-list-group-products`), EP-07 (`/basic/sales/set-cookie`), EP-19 (copy-item) |
| Tab 販売履歴 (sales-history) — search, date range, 絞り込み設定 modal | EP-01 (`?tab=sales-history`), EP-14, EP-15 |
| 販売履歴 → CSV書出し | EP-08 (単品), EP-09 (継続) |
| 販売履歴 → 一括返金実行 | EP-17 |
| 販売履歴 → 一括解約実行 | EP-18 |
| Tab 各種設定 — 事業者・特商法設定 + 最終確認画面 | EP-01 (`?tab=setting`), EP-11 |
| Tab 各種設定 — liên kết UnivaPay | EP-20 |
| Tab 各種設定 — liên kết Stripe | EP-26, EP-27 (OAuth), EP-30 (callback), EP-32 |
| Tab 各種設定 — huỷ liên kết (nhập mật khẩu) | EP-21 |
| Form 商品追加/編集 (tab 基本設定 / 各種ページ wizard 5 trang / アクション設定) | EP-01 (`?tab=add-item`/`edit-item`), EP-10 (init-data), EP-12 (save-item), EP-13 (get-item-detail), EP-23 (upload-file) |
| 商品詳細 | EP-02, EP-22 (販売履歴 theo tháng) |
| 注文詳細 (単品) | EP-05, EP-25 (huỷ/refund) |
| 注文詳細 (継続) + 決済履歴 | EP-06, EP-25 (refund 1 kỳ), EP-16 (解約) |
| プレビュー請求書 | EP-04 |
| **LINE User** — 商品ページ | EP-60 |
| **LINE User** — お客様情報入力 | EP-65 |
| **LINE User** — カード情報入力 | EP-66, EP-89 (tạo customer UnivaPay), EP-88 (lấy u_code qua LIFF) |
| **LINE User** — 最終確認 | EP-67 |
| **LINE User** — Thực hiện thanh toán | Stripe: EP-80 → EP-81 (+ EP-83 khi confirm lỗi); UnivaPay: EP-82 |
| **LINE User** — 完了 | Nội dung `page_end_simple` (`flag_page_end=0`) / redirect `url_page_outsite_end` (`=1`) / redirect LINE chat (`=2`) |
| **LINE User** — 解約用ページ | EP-62, EP-87 |
| **LINE User** — カード情報変更ページ | EP-63, EP-84 → EP-85 (Stripe), EP-86 (UnivaPay) |
| **LINE User** — 特定商取引法に基づく表記 | EP-64 |
| Webhook UnivaPay | EP-94 (đang hoạt động); EP-95 đã vô hiệu hoá |
| App mobile — 購入履歴 | EP-96, EP-97, EP-98 |

---

## 5. Ghi chú tổng hợp về mã lỗi

| Thông điệp (JP) | Nguồn | Ngữ cảnh |
|-----------------|-------|---------|
| 「決済処理を行っていますので、操作できません。」 | `V2:1063`, `:1614`, `:1783`, `:1887` | Đơn đang chờ webhook |
| 「在庫切りです。{n}以下入力してください」 | `V2:2566`, `:4943` | Vượt tồn kho |
| 「在庫がないので、購入できません。販売者に連絡してください。」 | `V2:2569`, `:4945` | Hết hàng |
| 「購入数量は1以上で入力してください。」 | `V2:2430`, `:4915` | Số lượng ≤ 0 |
| 「商品が非公開か、存在していません」 | `V2:1555`, `:1735`, `:1833`, `:2110` | Item không tồn tại / `status_valid != 1` |
| 「商品販売ページ中に「ページ貼り付けJavaScriptタグ」が確認できないか、お客様情報を取得できませんでした」 | `V2:1713`, `:1750`, `:2048`, `:2115` | Không xác định được `bot_line_user` từ `u_code` |
| 「この商品は購入されていません。」 / 「既にキャンセルしました。」 / 「キャンセル済です」 / 「試用期間が終了しました」 | `V2:1757`, `:1769`, `:1771`, `:1763` | Trạng thái hợp đồng khi vào trang 解約 |
| 「決済できません。管理者に連絡してください。」 | `V2:2158`, `:2162`, `:2166` | Chưa cấu hình khoá Stripe/UnivaPay hoặc thiếu `payment_method` |
| 「現在のプランは利用できない機能です。アップグレードが必要になります。」 | `V2:958`, `:1419`; `V1:653` | Vượt giới hạn số sản phẩm theo gói |
| 「選択したフォルダーは、現在存在していません。」 | `V2:903` | Folder bị xoá ở tab khác |
| 「パスワードが間違っています。」 | `V2:6874` | Sai mật khẩu khi huỷ liên kết |
| 「別のアカウントに切り替えたので、要求を処理できません。」 | `V1:540`, `:622`, `:825`, `:1904`, `:1934`, `:1977` | `botIdCurrent` không khớp bot hiện tại |
| Bộ 17 thông điệp lỗi thẻ Stripe | `V2:2216-2233`; `SalesStripePaymentController:1811-1828` | Map từ Stripe error code |
| Bộ thông điệp lỗi UnivaPay | `V2:2676-3112` (`getMessageErrorUnivapay`) | Map từ UnivaPay error code |

> **Đặc điểm chung**: gần như **mọi lỗi đều trả HTTP 200**, phân biệt bằng field `status` / `success` / `result` trong body. Chỉ có 2 ngoại lệ: HTTP 500 khi đang backup (V1 `store-item`/`save-item`) và HTTP 400 khi exception ở EP-82.
