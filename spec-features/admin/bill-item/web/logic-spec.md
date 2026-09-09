# Logic Spec — FA-026 「単品商品」/「商品販売」 (Bill Item / Sales Management)

> **Nguồn**: đọc trực tiếp source Laravel 5 tại `src/web/sns-line/`.
> Mọi đường dẫn ghi dạng `src/web/sns-line/...:dòng`.
> **Mức độ tin cậy** được ghi cho từng nhóm kết luận.

---

## 1. Bản đồ thành phần

```
┌─ Admin/Staff (portal) ─────────────────────────────────────────────┐
│  SalesManagementV2Controller   ← hiện hành (is_product_new = 1)     │
│  SalesManagementController     ← V1 legacy (is_product_new = 0)     │
└────────────────────────────────────────────────────────────────────┘
┌─ LINE User (public) ───────────────────────────────────────────────┐
│  SalesManagementV2Controller (orderDetail → … → confirmOrder)       │
│  SalesStripePaymentController (paymentCreditCardItemV2)             │
└────────────────────────────────────────────────────────────────────┘
┌─ Nền / bất đồng bộ ────────────────────────────────────────────────┐
│  WebhookUnivapayControler → Job HandleWebhookUnivapay → SalesService │
│  Command handle:bill_stripe        (07:00 hằng ngày)                │
│  Command handle:HandleSendActionTrialV2 (07:00 hằng ngày)           │
│  Command refresh:month_sales       (00:05 hằng ngày)                │
│  Command recover:payment_univapay_timeout (mỗi 5 phút)              │
│  Command univapay:check_status_webhook (01:00 hằng ngày)            │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. Controllers & Actions

### 2.1 `Basic\SalesManagementV2Controller`
`src/web/sns-line/app/Http/Controllers/Basic/SalesManagementV2Controller.php` — **6.979 dòng**.

**Dependency inject** (`:81-91`): `StripePayment $stripPayment`, `UnivapayPayment $univapayPayment`, `MobileNotifyService $mobileNotifyService`, `SalesService $salesService`.

#### `index(Request $request)` — `:93`
Điều phối toàn bộ màn hình chính bằng query `tab` (`list-item` / `sales-history` / `setting` / `add-item` / `edit-item`) — view `basic.sales.v2.index` include từng phần theo tab (`resources/views/basic/sales/v2/index.blade.php:97-100`).

Logic đáng chú ý:
- **Khôi phục folder từ cookie** (`:102-113`): đọc cookie `folder_sales` dạng `{botId: categoryId}`; nếu category không còn tồn tại → reset về `0` và ghi lại cookie (TTL 14400 phút, path `/basic/sales/index`).
- **Danh sách folder theo loại thanh toán** (`:130-138`): `typePayment == 0` → `s_categories.type_payment = 0`; ngược lại `= 2`. → **Folder của 単品 và 継続 tách biệt hoàn toàn** (Cao).
- **Trạng thái liên kết Stripe** (`:154-165`): `s_strip_bot.status_strip_bot` khác 0 → gọi `StripePayment::getInfoAccount()` để lấy email hiển thị.
- **Trạng thái liên kết UnivaPay** (`:171-184`): dựa vào `univapay_app_id`; URL webhook lấy từ `s_strip_bot.univapay_webhook`, mặc định `env('DOMAIN_WEBHOOK_UNIVAPAY_BILL') . 'product-callback/' . Hashids::encode(bot_id)` (`:169`).
- **Giới hạn số sản phẩm theo gói** (`:191-217`) → biến `maxItemBillOne`, `maxItemBillCycle` để ẩn nút 新規作成 (xem BR-01).
- Khi `tab = edit-item`: `itemId` là hashid; giải mã sai hoặc item không tồn tại → `redirect()->route('404')` (`:142-146`).

#### `getItemDetail($id)` — `:259` / `ajaxGetItemDetail($id)` — `:292`
- `getItemDetail` nhận **hashid**, giải mã và lọc theo `bot_id` (`:263-268`) → an toàn.
- `ajaxGetItemDetail` nhận **id thô**, vẫn lọc `bot_id` (`:294-297`) → an toàn.

#### `ajaxGetListGroupProducts(Request $request)` — `:315`
Endpoint đa hành động cho sidebar folder + thao tác hàng loạt trên sản phẩm. Xem bảng `action` ở api-spec (EP-24).

Điểm cần lưu ý:
- `deleteGroup` (`:372-383`): `SCategory::destroy()` rồi **xoá toàn bộ `s_items` trong folder** — kéo theo model event `deleting`/`deleted` của `SItems` (mục 3.1).
- `renameGroup` (`:384-393`): update `DB::table('category')` — **sai bảng**, bảng đúng là `s_categories`. Nhánh này thực tế không được UI dùng (UI dùng `addAndEditGroup`). **Nghi vấn bug — tin cậy Cao về code, Trung bình về tác động**.
- `sortItem` (`:394-404`): `position` được gán theo mảng **đảo ngược** (`array_reverse`), khớp với `orderBy('position','DESC')` khi hiển thị.
- `moveItem` (`:416-436`): mọi item được đẩy lên `max(position)+1` **cùng một giá trị** → thứ tự trong folder đích không xác định (Trung bình).
- Toàn bộ nằm trong `try/catch` nhưng `DB::beginTransaction()` **đã bị comment** (`:318`, `:474`, `:484`) → **không có transaction**.

#### `ajaxGetSalesHistory(Request $request)` — `:491`
Lịch sử bán theo tháng cho màn 商品詳細. Params `month` (`YYYY/MM`), `itemId`, `typePayment`. Lọc thêm `flag_environment` = của chính item (`:508`, `:520`). Phân trang 20. Gắn `hashId` cho từng bản ghi (`:528`).

#### `uploadFile(Request $request)` — `:569`
- Lưu vào `public_path(env('FOLDER_MEDIA') . 'media/images/{admin_id}/{bot_id}/bill-item')`, tạo thư mục `0777` nếu chưa có (`:575-578`).
- Resize ảnh về tối đa **2048px** qua `resizeImageToMaxSize()` (`:588`), bỏ qua `image/svg+xml`.
- **Không validate MIME/kích thước file trước khi `move()`** (Cao) — chỉ kiểm tra sau khi đã lưu.
- Trả về **chuỗi đường dẫn thuần** (không phải JSON).

#### `initData(Request $request)` — `:633`
Nạp dữ liệu cho form thêm/sửa:
- `friendInfoTypeText`: `friend_information_setting` với `type_data = 2`.
- `settings`: `s_store_settings` của bot.
- `detailActionItemV2`: đọc `t_actions_detail` của 7 action slot (`showPage`, `contract`, `contract_trial`, `action_purchase_1st`, `action_purchase_2st`, `action_buy_error`, `action_cancel_payment` — `:645-652`), mỗi detail chạy qua `Actions::initDataAction()`.
- `listFriendInfo`: `b_c_info_setting` theo `item_id`; **nếu rỗng → trả 2 mục mặc định** 「お名前」(`friend_info_id = -1`) và 「メールアドレス」(`friend_info_id = -3`) (`:673-695`, `:729-750`).
- Ánh xạ `friend_info_id` âm sang nhãn (`:707-723`): `0` = 利用しない, `-1` = システム表示名, `-2` = 携帯電話, `-3` = メールアドレス, `-6` = 都道府県.

#### `saveSettings(Request $request)` — `:776`
Upsert `s_store_settings` theo `bot_id`, dùng **toàn bộ `$request->input()`** (`:781`). Model `SStoreSetting` có `$guarded = []` → **mass assignment không giới hạn** (Cao). Bảng chỉ có `general_settings` + `info_store` nên rủi ro thực tế thấp.

#### `canCreateItemByPlan($typePayment)` — `:816` (private)
Xem BR-01.

#### `saveItem(Request $request)` — `:849` ★ trung tâm
1. `$request->only([...])` với whitelist 40 field (`:853-894`) — field ngoài whitelist bị bỏ.
2. **Kiểm tra folder** (`:896-905`): `s_category_id != 0` phải tồn tại và thuộc `bot_id` hiện tại.
3. **Chỉ khi `type_payment != 0`** (`:907-930`) mới nạp 22 field của 継続商品 (trial, chu kỳ, action mua lần 1/2, action lỗi, action huỷ, page 解約…).
   - `action_contract_trial_id` và `time_trial` bị **ép `null`** khi `flag_trial != 1` (`:915`, `:927`).
4. Luôn set `is_product_new = 1`, `status_valid = 1` (`:932-933`) → **sản phẩm luôn ở trạng thái công khai; không có chức năng ẩn ở V2** (Cao).
5. **Tạo mới**: kiểm tra `canCreateItemByPlan()` (`:954`) → chặn vượt gói; `position = max(position trong folder) + 1` (`:1011-1012`).
6. **Cập nhật**: nếu `name` thay đổi → **đồng bộ ngược `name_item`** sang toàn bộ `s_order_history` và `s_cycle_order_history` của item (`:977-980`).
7. **Đồng bộ `b_c_info_setting`** (`:982-1006`): mục có `id` → update, không có → create, mục có trong DB nhưng **không có trong payload → bị xoá cứng** (`:1006`).
8. `image_product` là mảng → `implode(',')`; rỗng → `null` (`:947-971`).
9. Trả về `product` kèm `hashId` (`:1030`).

**Không có transaction** (comment `:1038`) — Cao.

#### `cancelCycleOrder(Request $request)` — `:1047`
- **Chặn khi đang xử lý thanh toán** (`:1058-1064`): `status_webhook ∈ {0,3,4}` → trả lỗi 「決済処理を行っていますので、操作できません。」
- Gọi `cancelCycleOrderItem()` (`:1070`).
- Nếu `user_cancel == 'customer'` (LINE User tự huỷ) → **luôn chạy** エルメアクション「解約時」 kể cả `flagExecuteAction = 0` (`:1071-1081`) và tăng `bot_line_user_item.count_action_cancel`.

#### `orderHistoryDetail($hashId)` — `:1095` / `cycleOrderHistoryDetail($hashId)` — `:1138`
- Cả hai giải mã `detail_info_user` (JSON) rồi **sắp xếp lại theo `b_c_info_setting.order_index`** (`:1101-1110`, `:1166-1175`).
- ⚠ `orderHistoryDetail` **không lọc `bot_id`** khi `find($orderId)` (`:1099`) → chỉ chặn gián tiếp qua `SItems::find()` sau đó (`:1112`, redirect 404 nếu item không tồn tại — nhưng item vẫn có thể thuộc bot khác). **Rủi ro IDOR — tin cậy Trung bình.** `cycleOrderHistoryDetail` **có** lọc `bot_id` (`:1159`).
- `cycleOrderHistoryDetail` kèm `orderDetail` = danh sách `s_order_history` theo `cycle_order_id` (`:1180`) → đây là bảng 決済履歴 trong màn 注文詳細 (継続).

#### `ajaxListOrderHistory(Request $request, $export = false)` — `:1209`
- 2 nhánh truy vấn hoàn toàn khác nhau theo `type_payment`.
- **単品**: `s_order_history` + `cycle_order_id IS NULL` (`:1310`) → chỉ đơn mua lẻ, loại các kỳ của hợp đồng định kỳ.
- **継続**: `s_cycle_order_history` LEFT JOIN `s_order_history` qua `last_bill_id`, khoảng ngày dùng **OR** giữa `last_bill_time` và `c_register_date` (`:1238-1247`).
- Bộ lọc trạng thái 継続 `statusBillMany` được dựng bằng `whereRaw` (`:1266-1294`):

| Giá trị | Nhãn UI | Điều kiện SQL |
|--------|--------|--------------|
| 1 | 契約中 | `status_trial = 0` và (`last_bill_id` có + `status_bill = 1` + `status_order <> 3`) hoặc (`last_bill_id` null + `status_bill = 1`) |
| 2 | トライアル | `status_trial = 1 AND status_bill = 1` |
| 3 | 解約 | `status_bill = 3` |
| khác | 期限切れ | `status_trial = 0 AND last_bill_id` có `AND status_bill = 1 AND status_order = 3` |

- Khi `$export = true` → trả **Collection** thay vì paginator, dùng lại bởi 2 hàm xuất CSV.
- Luôn lọc `s_items.is_product_new = 1` (`:1237`, `:1314`) → **danh sách V2 không bao giờ hiển thị dữ liệu V1** (Cao).

#### `ajaxCopyItem($id)` — `:1408`
- Kiểm tra giới hạn gói trước khi sao chép (`:1415-1421`).
- `replicate()` + sinh `item_code` mới (`:1423-1427`).
- **Clone toàn bộ 7 action** qua `cloneAction()` (`:1429-1450`) — nhân bản cả `t_actions` lẫn `t_actions_detail` (`:1523-1548`).
- Reset toàn bộ counter thống kê về 0 (`:1452-1463`).
- Clone `b_c_info_setting` (`:1467-1476`) và **copy file ảnh vật lý** (`:1478-1498`, hàm `copy()` `:601`).
- Trả URL để redirect sang màn sửa item mới.

#### `orderDetail(Request $request, $item_code, $u_code = null)` — `:1550` (public LINE User)
Luồng trang 商品ページ:
1. Item không tồn tại → view lỗi 「商品が非公開か、存在していません」 (`:1554`).
2. **Chặn bot hết hạn** (`:1568-1571`): `plan_type == 1` và (`expired_date + 7 ngày < now` hoặc `bot_contract.status == 3`) → `route('410')`.
3. Nếu `u_code` hợp lệ (khác `'preview'`, UA không phải crawler LINE/FB):
   - `bot_line_user` không tồn tại/bị block → redirect `url_add_friend` (`:1589`).
   - **Chặn khi đang có đơn định kỳ chờ webhook** (`:1592-1618`) → view lỗi 「決済処理を行っていますので、操作できません。」
   - Tạo `bot_line_user_item` với `status_contract = unregister (0)` nếu chưa có (`:1620-1629`).
   - **Bắn エルメアクション「ページ表示時」** (`:1630-1636`) khi `action_show_page_id` có giá trị **và** `flag_page_start != 2`; thành công → `count_action_view_page + 1`.
4. **Tính tồn kho còn lại** (`:1640-1652`):
   - 単品: `quantity_stock - SUM(s_order_history.quantity_purchased WHERE status_order = 1)`
   - 継続: `quantity_stock - SUM(s_cycle_order_history.quantity_purchased WHERE status_bill <> 3)`
   - Luôn lọc thêm `flag_environment` của item.
5. Chọn public key Stripe theo `flag_environment` (`:1654-1658`).
6. **OGP cho crawler Facebook** (`:1663-1669`): trả view nhẹ `preview_url` với `og:title`/`og:description`.

#### `orderCancel` — `:1727` / `orderChange` — `:1820` (public)
Cùng khung: kiểm tra item → kiểm tra hạn bot → kiểm tra `u_code` → tra `bot_line_user_item.status_contract` để quyết định thông điệp lỗi.

| `status_contract` | Thông điệp |
|------------------|-----------|
| 0 unregister | 「この商品は購入されていません。」 |
| 1 registered | Cho phép (nếu tìm được cycle `status_bill = 1`); nếu `cycle_payment == once && status_trial == 0` → 「試用期間が終了しました」 |
| 2 complete | 「既にキャンセルしました。」 |
| 3 cancel | 「キャンセル済です」 |

Ngoài ra nếu `status_webhook ∈ {0,3,4}` → 「決済処理を行っていますので、操作できません。」 (`:1778-1785`, `:1882-1889`).

`orderChange` còn nạp `flag_brand_card_univapay` (danh sách brand thẻ được phép, chuỗi CSV trong `s_strip_bot`, `:1916-1924`) và **hard-code `flagInstallment = 0`** (`:1929`) → **tính năng trả góp đã bị tắt ở trang đổi thẻ** (Cao).

#### `viewEnterFriendInfo` — `:1965` (public)
- Nạp `b_c_info_setting` theo `order_index`, và **prefill giá trị** từ hồ sơ bạn bè:
  - `friend_info_id > 0` → `friend_information_value.value` theo `line_id` (`:2019-2022`), kèm `setting_actions` (danh sách lựa chọn) từ `friend_information_setting.setting_value`.
  - `-1` → `line_user.view_name`; `-2` → `phone_number`; `-3` → `email`; `-6` → `province` + danh sách 47 đô-đạo-phủ-huyện từ `config('sns-line.province_default')` (`:2025-2041`).
- Nút mặc định khi chưa cấu hình: 「決済情報入力にすすむ」, chữ `#ffffff`, nền `#08bf5a` (`:1985-1989`).
- ⚠ `:1998` so sánh `$u_code != 'preivew'` — **lỗi chính tả** (`preivew`), khiến chế độ preview vẫn truy vấn `bot_line_user`. Tin cậy Cao.

#### `viewEnterPaymentInfo` — `:2091` (public)
- Chặn khi `status_valid != 1` (`:2109`).
- **Chặn khi chưa cấu hình cổng thanh toán** (`:2155-2167`): thiếu bản ghi UnivaPay khi `payment_method = 'univapay'`, thiếu public key khi `= 'stripe'`, hoặc `payment_method` rỗng → 「決済できません。管理者に連絡してください。」

#### `confirmOrder(Request $request, $item_code, $u_code)` — `:2246` (public)
- **Lưu thông tin thẻ vào session** thay vì gửi kèm request thanh toán:
  - `session('univapaySalesV2')` = `{token, installment_count, customer_id, customer_code}` (`:2283-2290`)
  - `session('stripeSalesV2')` = `{card_id, token_id}` (`:2292-2297`)
  - `session('stripeCustomerV2')` = `{last4, brandName, pm_id}` (`:2354-2358`)
- Với UnivaPay: gọi `getInfoTokenSale()` để lấy thông tin thẻ hiển thị; lỗi → dịch qua `getMessageErrorUnivapay()` (`:2331-2337`).

#### `paymentIntent(Request $request)` — `:2408` (Stripe bước 1)
1. Validate số lượng `> 0` (`:2429-2433`).
2. **Tính số tiền ở server** (`:2437-2449`) — xem BR-05.
3. Tạo Stripe Customer (`:2492`) + attach PaymentMethod (`:2504`).
4. **Tạo trước bản ghi order/cycle** qua `CycleOrderHistory::createOrderPayment()` (`:2531-2545`) với `isProcessWithWebhook = false` → `status_webhook = STATUS_WEBHOOK_TIMEOUT (3)`.
5. **Kiểm tra tồn kho SAU khi đã tạo bản ghi** (`:2553-2583`) — nếu vượt thì xoá bản ghi vừa tạo rồi trả lỗi. **Race condition: 2 người mua đồng thời có thể cùng vượt tồn kho** (Trung bình).
6. Gọi `StripePayment::paymentIntents()` (`:2597`/`:2599`); thành công → lưu `o_strip_charge_id` / `c_strip_charge_id`.
7. Nếu `amount == 0` (trial không có giá đầu) → tạo **SetupIntent** thay vì PaymentIntent (`:2618-2623`).
8. Thất bại → `CycleOrderHistory::deleteOrderPaymentError()` xoá cứng bản ghi tạm (`:2635`) + ghi `s_order_history_notify` (status `-1`) + `MobileNotifyService::insertNotifyItem()` (`:2644-2661`).

#### `paymentCreditCardItemV2Univapay(Request $request)` — `:4847` (UnivaPay, toàn luồng)
- Validate số lượng (`:4914-4918`), **kiểm tra tồn kho trước khi tạo đơn** (`:4921-4950`) — khác với nhánh Stripe.
- Lấy thông tin thẻ qua `getInfoTokenSale()` (`:4955`).
- Tính `trialExpiredTime = now()->addDay(time_trial)->format('Y-m-d 23:59:59')` (`:4980`).
- **Cơ chế webhook vs polling** (`:4989`, `:5042-5098`):
  - `isProcessWithWebhook($stripBot)` (`app/Helpers/functions.php:138`) = true khi `univapay_webhook_id` có và `status_webhook == 1`.
  - Nếu **có webhook**: sau khi charge, gọi `SalesService::checkStatusProcessCallback()` (`SalesService.php:2377`) — vòng lặp tối đa **5 lần, mỗi lần `sleep(1)`** chờ webhook cập nhật `status_webhook`. Hết 5 lần vẫn chưa xong → đặt `status_webhook = STATUS_WEBHOOK_TIMEOUT_WEBHOOK (4)` và trả `result = 'pending'` → UI hiện màn hình chờ.
  - Nếu **không webhook**: polling `getChargesSale()` trực tiếp (`:5072`).
- Nếu xử lý > 2 phút → gửi tin LINE thông báo kết quả qua `SalesService::sendNotifyExecutionTimeMoreThanTwoMinute()` (`:5084-5090`, `SalesService.php:97`).
- Sau khi thành công: cập nhật hồ sơ bạn bè, ghi `sync_elasticsearch` (`:5786`), xử lý affiliate (`:5794-5900`), bắn action `contract` / `purchase_1st` / `purchase_2st` (`:5916-5951`).
- Exception → `notifyChatwork()` + HTTP 400 (`:5964-5965`).

#### `cancelOrderV2(Request $request)` — `:3192` / `cancelOrderItemV2($orderId, $autoRefund)` — `:3405`
- Chỉ xử lý khi `amount_order > 0` (`:3202`).
- **Stripe**: chọn secret key theo `flag_environment`; nếu `o_strip_charge_id` bắt đầu bằng `ch` → `refundMoney()`, ngược lại → `refundMoneyPaymentIntent()` (`:3217-3221`).
- **UnivaPay**: `refundMoney()` rồi `getRefundMoney()` để xác nhận (`:3250-3257`).
- `autoRefund = 0` → **chỉ đổi trạng thái, không gọi API hoàn tiền** (`:3237-3243`, `:3274-3280`).
- Thành công → `updateDataAfterRefund()` (`:3113`) rồi set `status_order = 2`, `cancel_date = now()`.

#### `updateDataAfterRefund($order)` — `:3113` (private)
- Trừ `bot_line_user_item.total_money` (chỉ khi đủ) (`:3114-3117`).
- Tăng `s_items.number_refund(_test)`, trừ `sum_sales(_test)` (`:3143-3171`).
- Nếu đơn **không thuộc hợp đồng định kỳ** → tăng `number_cancel(_test)` (`:3174-3190`).
- ⚠ **Toàn bộ cập nhật `s_monthly_item` đã bị comment out** (`:3120-3189`) → **thống kê tháng không còn được điều chỉnh khi hoàn tiền ở V2** (Cao). Nhánh V1 `cancelOrder()` (`:3297`) vẫn còn logic này.

#### `cancelCycleOrderItem($orderId, $flagExecuteAction, $userCancel)` — `:3567`
- Chặn khi `status_webhook ∈ {0,3,4}` → `return false` (`:3583-3591`).
- `s_cycle_order_history`: `status_bill = 3`, `c_cancel_date = now()` (`:3594-3597`).
- Điều chỉnh counter `s_items`: `number_cancel(_test) + 1`; nếu đang trial thì thêm `number_trial(_test) - 1` (`:3598-3631`).
- Bắn `sendActionOrderItem('cancel', …)` khi `flagExecuteAction == 1` (`:3632-3642`).
- `bot_line_user_item.status_contract = 3 (cancel)` (`:3643-3647`).
- Ghi `s_order_history_notify` với `status_order = -2` (`:3652-3658`) + `MobileNotifyService::insertNotifyItem(PRODUCT_SALES_CYCLE_ADMIN_CANCEL)` (`:3687`).
- ⚠ Cập nhật `s_monthly_item` cũng **đã bị comment out** (`:3578-3617`).
- **Không gọi API huỷ subscription bên cổng thanh toán** ở nhánh này (Cao).

#### `cancelOrderMultiple` — `:3519` / `cancelCycleOrderMultiple` — `:3533`
- Vòng lặp gọi hàm đơn lẻ; **luôn trả `{"success": true}`** dù từng phần tử lỗi (`:3528`, `:3562`).
- `cancelCycleOrderMultiple` chỉ xử lý bản ghi `status_bill == 1 && cycle_payment != 0` (`:3546`), và exception mỗi phần tử chỉ ghi log (`:3557`).

#### `iniSettingUnivapay` — `:3713`
Gọi `UnivapayPayment::getAccountInfo($secret, $appToken)`; nếu OK → lưu `univapay_app_id` lấy từ response (không lấy từ input) và upsert `s_strip_bot`.

#### `createCustomerIdUnivapay` — `:3749`
Sinh `customer_code` dạng `product` + 20 ký tự ngẫu nhiên, lặp cho tới khi không trùng `s_order_history.o_univapay_customer_code` (`:3757-3763`); gọi thẳng REST `https://api.univapay.com/stores/{appId}/create_customer_id` bằng Guzzle (`:3778-3786`) — **không qua helper `UnivapayPayment`** (Cao).

#### `callback(Request $request)` — `:3806` ⚠
**Toàn bộ thân hàm đã bị comment out (`:3813-3880`)**, chỉ log body và trả `{"status": true}`. Webhook thật đi qua `WebhookUnivapayControler` (mục 6).

#### `changeCardItem` — `:6154` / `changeCardUnivapay` — `:6488` / `updatePaymentIntent` — `:5994`
Luồng đổi thẻ + **retry bill kỳ đang quá hạn**:
- Điều kiện retry (`:6033-6037`, `:6521`): `count_bill_error` đã set **và** `c_expired_date < now()`.
- Nếu chỉ đổi thẻ (không cần bill lại) → chỉ update `c_strip_*` / `c_univapay_*` + `payment_new = 1` (`:6176-6182`).
- Bill lại thành công → tạo `s_order_history` mới, `createDataInvoice()` với thuế, cập nhật `last_bill_id`, `number_payment + 1`, `number_continue - 1`, **reset `count_bill_error = null`** (`:6418`, `:6803`).
- Bill lại thất bại → `count_bill_error + 1` (`:6218`, `:6664`) và kiểm tra auto-cancel (`:6232-6235`, `:6667-6670`) — xem BR-07.

#### `unlinkPaymentMethod` — `:6867`
Xác thực lại mật khẩu (`Hash::check` với `Auth::user()->password`); `type = 'stripe'` → xoá 6 cột khoá Stripe; ngược lại xoá 4 cột UnivaPay. **Không xoá key test của UnivaPay** (`univapay_app_test_id`, `univapay_app_token_test`, `univapay_secret_test` vẫn còn) — Cao.

#### `exportCsvOrderHistory` — `:6918` / `exportCsvCycleOrderHistory` — `:6949`
Gọi lại `ajaxListOrderHistory($request, true)` để lấy Collection, lọc thêm theo `list_order_id_selected` nếu có, rồi `Excel::download()` **đồng bộ**. Tên file `単品商品販売履歴_{slugify(botName)}_{YmdHis}.csv` / `継続商品販売履歴_…`.
⚠ Nếu `bots.view_name` rỗng → `$fileName` không được gán → **hàm trả `null`, trình duyệt nhận response rỗng** (`:6944`, `:6975`) — Cao.

#### Method chết (không có route hoặc route trỏ sai)
| Method / Route | Vấn đề |
|---------------|--------|
| `getInfoProductSales()` (`:6903`) | Không có route nào trỏ tới |
| `saveOrder()` (`:3709`) | Thân hàm **rỗng** |
| Route `/basic/sales/add-single-item` → `@viewAddSingleItem` | Method **không tồn tại** trong controller |
| Route `/v2/order-item/index/{item_code}/{u_code?}` → `@orderIndex` | Method **không tồn tại** trong V2 |

---

### 2.2 `Basic\SalesManagementController` (V1 legacy)
`src/web/sns-line/app/Http/Controllers/Basic/SalesManagementController.php` — 2.089 dòng. Inject `StripePayment`, `UnivapayPayment` (`:59-65`) nhưng **`univapayPayment` không được dùng ở bất kỳ đâu**.

| Method | Dòng | Ghi chú logic chính |
|--------|------|--------------------|
| `linkPayment` | `:66` | Callback OAuth Stripe Connect (`\Stripe\OAuth::token`, `:81`, `:122`). Khi `status_strip_bot == 2` → **tạo 4 TaxRate trên Stripe** (test/live × 8%/10%, `:201-219`) và lưu id vào `s_strip_bot`, rồi set `status_strip_bot = 3`. Ràng buộc: `account_test_id` phải trùng `account_live_id`, lệch → reset toàn bộ khoá + lỗi 「テストと本番は同じアカウントを利用してください。」 (`:162-179`). ⚠ **Ghi secret key ra log** (`:90`, `:91`, `:131`, `:132`). |
| `listItemOld` | `:294` | Danh sách sản phẩm `is_product_new = 0`. Cookie `filter_item{botId}` TTL 14400 phút (`:507`). |
| `ajaxGetDataListItems` | `:453` | Trả JSON kèm 6 counter (trial/cancel/done × live/test) tính từ `s_cycle_order_history`. |
| `sortItems` | `:517` | Update `position`, **không lọc `bot_id`** → IDOR (`:523`). |
| `checkStep3Stripe` | `:533` | Set `status_strip_bot = 3`. |
| `changeValidItem` | `:557` | Bật/tắt `status_valid`, **không lọc `bot_id`** (`:562`). |
| `storeItem` | `:604` | Chặn khi đang backup (`BackupHistory.status ∈ {0,1}` → HTTP 500, `:611-618`). Giới hạn gói free `plan_type = 2`: tối đa **1 単品 + 1 継続** (`:633-655`). Tạo `s_items` + **`s_monthly_item`** (`:763-768`) + gán `item_id` cho `b_c_info_setting` (`:770`). |
| `saveItem` | `:806` | Ngoài update `s_items`, còn **cascade**: `amount1st` đổi → update `s_cycle_order_history.amount_first` cho hợp đồng `status_bill = 1` (`:889-892`); `name` đổi → update `name_item` ở cả 2 bảng lịch sử (`:984-987`); `amount` đổi → update `amount_item` (`:988-991`). **Xoá action cũ** qua `FilterV2::deleteActionFilterByActions` + xoá `t_actions_detail` + `t_actions` (`:979-983`). |
| `validateItem` | `:1002` | Xem BR-02 (rule V1). |
| `itemMonthly` | `:1110` | Đọc `s_monthly_item`. ⚠ `:1115` dùng `=` thay `==` (gán thay so sánh). |
| `orderHistory` / `cycleOrderHistory` | `:1123` / `:1155` | Lọc `is_product_new = 0`. |
| `exportCsvOrderHistory` / `exportCsvCycleOrderHistory` | `:1141` / `:1173` | `Excel::download` đồng bộ với `OrderHistoryExport` / `CycleOrderHistoryExport` (bản V1). |
| `editOrder` / `saveOrder` / `editCycleOrder` / `saveCycleOrder` | `:1187`–`:1275` | Cho phép Admin sửa `name_friend`, `email_friend`, `phone_friend` của đơn. **Không validate, không lọc `bot_id`** → IDOR. |
| `cancelCycleOrder` | `:1277` | Huỷ hợp đồng V1: `status_bill = 3`, điều chỉnh counter `s_items` **và** `s_monthly_item`, `status_contract = 3`, bắn action `cancel`, `insertMobileNotify` với `money_bill = 2`. **Không gọi API huỷ subscription.** |
| `cancelOrder` | `:1381` | Refund Stripe (`refundMoney`, `:1399`) rồi điều chỉnh `s_items` + `s_monthly_item` + `bot_line_user_item.total_money`. |
| `orderDetail` | `:1490` | Nếu `is_product_new == 1` → redirect sang `v2.orderDetail` (`:1503`). Hỗ trợ `flag_page_start` 0/1/2. |
| `orderIndex` / `orderCancel` / `orderChange` | `:1569` / `:1632` / `:1688` | **`return redirect()->route('404')` ngay dòng đầu** → ~200 dòng dead code. |
| `initDataActionItem` | `:1760` | Nạp 4 action slot V1 + `b_c_info_setting`. |
| `ajaxBillItemSortItemSetting` / `SaveInfoSetting` / `DeleteFriendInfo` | `:1898` / `:1926` / `:1968` | CRUD `b_c_info_setting`. ⚠ `:1984` so sánh `order_index` với **object Model** thay vì giá trị → logic dồn thứ tự sai. |
| `getConfigUserOrder` | `:2001` | ⚠ Lấy `bot_id` **từ request** (`:2004`), không xác thực. |
| `addOrEditCategoryItem` | `:2047` | **Không có route** → dead code. ⚠ `catch` trả `status = true` (`:2083`). |

---

### 2.3 `Basic\SalesStripePaymentController`
`src/web/sns-line/app/Http/Controllers/Basic/SalesStripePaymentController.php` — 1.840 dòng. Inject `StripePayment`, `MobileNotifyService` (`:49-56`).

| Method | Dòng | Ghi chú |
|--------|------|--------|
| `paymentCreditCardItem` | `:58` | V1 legacy. Charge trực tiếp bằng `chargeMoney()` (`:293`) khi `$amount >= 50` (`:289`). **Không tính thuế** (không gọi `createDataInvoice`). |
| `createOrderNotify` | `:575` | INSERT `s_order_history_notify` với `status_order` = `-1` (mua lần đầu thất bại) / `-2` (huỷ đơn). |
| `paymentCreditCardItemV2` | `:597` | **Bước 2 của luồng Stripe** — không charge lại, chỉ ghi nhận kết quả PaymentIntent (`$chargeSuccess = true` hard-code, `:993`). Tạo/cập nhật `s_cycle_order_history` + `s_order_history` với `status_webhook = 1 (PROCESSED)`, gọi `createDataInvoice()` để phát hành hoá đơn có thuế, cập nhật hồ sơ bạn bè + `sync_elasticsearch` (`:1330`), xử lý affiliate (`:1339-1435`), bắn action `contract` / `purchase_1st` / `purchase_2st` (`:1454`, `:1470`, `:1480`). ⚠ **Kiểm tra tồn kho đã bị comment out (`:749-773`)** — hàng rào tồn kho duy nhất nằm ở `paymentIntent()` phía trước. |
| `calculateNextExpiredDateItem` | `:1508` | Tính ngày hết hạn kỳ tiếp theo — xem BR-06. |
| `changeCardItem` | `:1533` | Đổi thẻ V1 + retry bill quá hạn. **Auto-cancel khi `count_bill_error >= 3` và `auto_cancel == 1`** (`:1586-1591`). |
| `cancelCycle` | `:1721` | Huỷ hợp đồng nội bộ (gọi từ `changeCardItem`): `status_bill = 3`, điều chỉnh counter + `s_monthly_item`, bắn action `cancel`, `status_contract = 3`, `insertMobileNotify` `money_bill = 2`. |
| `getMessageError` | `:1808` | Map 17 mã lỗi Stripe → tiếng Nhật. ⚠ Fallback luôn rơi vào `processing_error` → **message gốc của Stripe bị nuốt** (`:1832-1836`). |

---

### 2.4 `Api\SalesController` (app mobile)
`src/web/sns-line/app/Http/Controllers/Api/SalesController.php` — 357 dòng.

| Method | Dòng | Ghi chú |
|--------|------|--------|
| `getHistorySales` | `:17` | JOIN `s_items` với `s_order_history` hoặc `s_cycle_order_history` theo `typePayment`. **Chỉ trả dữ liệu 本番** (`flag_environment = 1` ở cả 2 bảng, `:27`, `:30`) và `is_product_new = 1` (`:28`). Phân trang 15. Gắn `status_text` qua `getStatusOrder()` / `getStatusOrderItem()`. |
| `getOrderDetail` | `:76` | Chi tiết đơn kèm `detail_info_user`, `current_amount` (giá hiện tại của item để so sánh). |
| `getNotifyOrderDetail` | `:184` | Đọc `s_order_history_notify` theo `modelType` — dùng khi mở thông báo đẩy. |

---

## 3. Models Eloquent

Tất cả model nằm ở **`src/web/sns-line/app/*.php`** (không phải `app/Models/`).

| Class | File | Table | Đặc điểm |
|-------|------|-------|---------|
| `SItems` | `app/SItems.php` | `s_items` | `$guarded = []`, `timestamps = true`. Accessor `getHashIdAttribute()` (`:20`) → `$appends = ['hash_id']`. **Model events** `deleting` (`:32-49`) và `deleted` (`:51-66`). |
| `OrderHistory` | `app/OrderHistory.php` | `s_order_history` | `$guarded = []`. Hằng `STATUS_WEBHOOK_UNPROCESSED = 0`, `PROCESSED = 1`, `ERROR = 2`, `TIMEOUT = 3`, `TIMEOUT_WEBHOOK = 4` (`:13-17`). Quan hệ `lineUser()` `belongsTo(LineUser)`. |
| `CycleOrderHistory` | `app/CycleOrderHistory.php` | `s_cycle_order_history` | `$guarded = []`. Hằng `STATUS_WEBHOOK_*` (0/1/2). Quan hệ `lineUser()`, `item()` (`belongsTo(SItems, 'item_id')`). 2 static factory: `createOrderPayment()` (`:26`), `deleteOrderPaymentError()` (`:157`). |
| `SCategory` | `app/SCategory.php` | `s_categories` (mặc định theo quy ước) | `$fillable = ['name','bot_id','position','type_payment']`. Static query builder `getListCategoryProducts()` (`:18`), `getListItemOfCategory()` (`:55`). Quan hệ `items()` `hasMany(SItems,'s_category_id')`. |
| `SStoreSetting` | `app/SStoreSetting.php` | `s_store_settings` | `$guarded = []`. Cột: `bot_id`, `general_settings`, `info_store`. |
| `StripBot` | `app/StripBot.php` | `s_strip_bot` | `$guarded = []`, **`timestamps = false`**. Lưu toàn bộ khoá Stripe + UnivaPay + tax rate id của 1 bot. |
| `SMonthlyItem` | `app/SMonthlyItem.php` | `s_monthly_item` | `$guarded = []`. Khoá logic `bot_id + item_id + month + year`. |
| `OrderHistoryNotify` | `app/OrderHistoryNotify.php` | `s_order_history_notify` | `$guarded = ['o_strip_pm_id','payment_new']`. Quan hệ `lineUser()`. |
| `BotLineUserItem` | `app/BotLineUserItem.php` | `bot_line_user_item` | `$guarded = []`. Lưu trạng thái hợp đồng + toàn bộ counter action của cặp (bạn bè × sản phẩm). |
| `BCInfoSetting` | `app/BCInfoSetting.php` | `b_c_info_setting` | `$fillable` gồm `bot_id`, `booking_calendar_id`, `item_id`, `item_code`, `title`, `type`, `setting`, `is_require`, `order_index`, `friend_info_id`, `is_default`. **Dùng chung với tính năng đặt lịch** (có `booking_calendar_id`). |
| `SyncElasticsearch` | `app/SyncElasticsearch.php` | `sync_elasticsearch` | **Connection riêng `mysql_step_message`** (`:10`). Static `insertElasticsearch()` (`:15`) — **chỉ INSERT khi `env('API_KEY_ES')` được cấu hình**, ngược lại trả `null`. |
| `ActionLineUser` | `app/ActionLineUser.php` | **`action_lineuser`** | Hàng đợi thực thi エルメアクション. |

> ⚠ **Đính chính**: bảng `action_line_users` (số nhiều) **không tồn tại** trong codebase. Tên đúng là **`action_lineuser`** (model `App\ActionLineUser`, `app/ActionLineUser.php:10`). Tin cậy **Cao**.

### 3.1 Model events của `SItems` (`app/SItems.php:28-67`)
| Event | Hành vi |
|-------|--------|
| `deleting` | Ghi log `s_order_history` / `s_cycle_order_history` liên quan (**không xoá**, chỉ log); **xoá cứng toàn bộ `b_c_info_setting` theo `item_id`** (`:47`). |
| `deleted` | **Xoá file ảnh vật lý** trong `image_product` khỏi disk (`:53-65`), bỏ qua URL tuyệt đối. |

→ Khi xoá 1 sản phẩm hoặc xoá cả folder, **lịch sử đơn hàng vẫn còn nhưng mất liên kết cấu hình form và mất ảnh** (Cao).

### 3.2 `CycleOrderHistory::createOrderPayment(...)` — `app/CycleOrderHistory.php:26`
Factory dựng **cặp** bản ghi `s_cycle_order_history` (chỉ khi `type_payment != once`) + `s_order_history`.

Logic then chốt:
- `number_continue` = `-1` nếu `number_charge == 0` (vô hạn); nếu đã bill ngay (`statusTrial == 0`) thì `number_charge - 1` (`:41-49`).
- `number_payment` = `0` khi bắt đầu bằng trial, `1` khi bill ngay.
- `amount_first` chỉ ghi khi `flag_first == 1`, ngược lại `0` (`:68`).
- `status_webhook`: `isProcessWithWebhook = true` → `0 (UNPROCESSED)`; `false` → `3 (TIMEOUT)`; `null` → `1 (PROCESSED)` (`:52-58`).
- `is_installment` chỉ set khi `type_payment == once` và có `installment_count` (`:106-110`).
- `s_order_history.status_order = 1` ngay từ lúc tạo (`:117`) → bản ghi "lạc quan", sẽ bị xoá cứng nếu thanh toán thất bại.

### 3.3 `CycleOrderHistory::deleteOrderPaymentError($cycleId, $orderId)` — `:157`
`forceDelete()` cả 2 bản ghi. Gọi từ `paymentIntent()` (`:2635`) và `deletePaymentOrderConfirmFail()` (`:4838`).

---

## 4. Services / Repositories / Helpers

### 4.1 `App\Services\Sales\SalesService`
`src/web/sns-line/app/Services/Sales/SalesService.php` — 2.945 dòng. Inject `MobileNotifyService`, `TemplateService`, `MessageService`, `StripePayment` (`:57-67`).

| Method | Dòng | Vai trò |
|--------|------|--------|
| `checkExecutionTimeMoreThanTwoMinute($start,$end)` | `:70` | So sánh > 120 giây |
| `sendMessageAction(...)` | `:74` | Gửi 1 tin nhắn LINE (qua `MessageService::createMessageV2`) |
| `sendNotifyExecutionTimeMoreThanTwoMinute($type,$bot,$lineUser)` | `:97` | Gửi tin 「決済が完了しました。」 hoặc 「決済に失敗しました。…」 khi xử lý quá lâu; tăng `bots.free_send_count` + `updateMessageSendCount(bot, date, 3, 1)` |
| `getDataCallback($data,$paymentMethod)` | `:120` (private) | Chuẩn hoá payload webhook |
| **`handleOrderCallback($data,$paymentMethod)`** | `:174` | **Xử lý webhook `module = 'sales'`** — hoàn tất/huỷ đơn theo kết quả charge |
| **`callbackChangeCard($data,$paymentMethod)`** | `:809` | Webhook `module = 'sales_change_card'` |
| **`callbackJob($data,$paymentMethod)`** | `:1239` | Webhook `module = 'sales_job'` (kết quả bill định kỳ từ cron) |
| `calculateNextExpiredDateItemJob` / `calculateNextExpiredDateItem` | `:1697` / `:2444` | Tính ngày hết hạn kỳ kế |
| `cancelCycleJob` / `cancelCycle` | `:2134` / `:2275` | Huỷ hợp đồng từ job / từ web |
| `createOrderNotify(...)` | `:2355` (private) | Ghi `s_order_history_notify` |
| **`checkStatusProcessCallback($orderId,$type)`** | `:2377` | **Polling đồng bộ**: lặp tối đa 5 lần, `sleep(1)` mỗi lần, đợi `status_webhook ∈ {1 PROCESSED, 2 ERROR}` |
| **`getOrderTimeout()`** | `:2469` | Quét đơn treo và **dispatch `HandleWebhookUnivapay`** (`:2564`, `:2695`) |
| `checkFriendBotLine($lineId,$botId,$retry)` | `:2702` | Kiểm tra người dùng đã kết bạn (có retry) |

**Chi tiết `getOrderTimeout()`** (Cao — quan trọng cho job-analyzer):
- Quét `s_order_history` và `s_cycle_order_history` có `status_webhook ∈ {0 UNPROCESSED, 3 TIMEOUT, 4 TIMEOUT_WEBHOOK}`, có `c_univapay_charge_id` hoặc `c_strip_charge_id`, và `created_at < now() - 15 phút` (`:2569-2580`).
- Với bản ghi `TIMEOUT_WEBHOOK (4)`: dùng **update có điều kiện** làm khoá lạc quan — `where('status_webhook', 4)->update(['status_webhook' => 3])`; nếu `affected != 1` → bỏ qua (đã có tiến trình khác xử lý) (`:2547-2559`).
- Sau đó `HandleWebhookUnivapay::dispatch($dataCharge, $paymentMethod)` với `$dataCharge['from_job'] = true` (`:2561-2564`).

### 4.2 `App\Helpers\StripePayment`
`src/web/sns-line/app/Helpers/StripePayment.php`

| Method | Dòng | Vai trò |
|--------|------|--------|
| `createCustomer($token,$email,$name)` | `:25` | `\Stripe\Customer::create` |
| `updateCustomer($cusId,$token)` | `:54` | Đổi nguồn thanh toán |
| `chargeMoney($customerId,$amount,$description,$email)` | `:82` | `\Stripe\Charge::create` currency `jpy` |
| `getCardInfo($customerId,$cardId)` | `:161` | last4 / brand |
| `refundMoney($chargeId)` | `:185` | Hoàn tiền theo Charge |
| `refundMoneyPaymentIntent($chargeId)` | `:209` | Hoàn tiền theo PaymentIntent |
| `getInfoAccount($secretKey,$accountId)` | `:233` | Thông tin Connect account |
| `setApiKey($key)` | `:255` | Đặt secret key runtime |
| `attachPaymentMethodToCustomer($secretKey,$pmId,$customerId)` | `:260` | Gắn PaymentMethod |
| `setupIntent(...)` / `updateSetupIntent(...)` | `:283` / `:314` | Đăng ký thẻ (3DS) khi số tiền = 0 |
| `paymentIntents(...)` | `:337` | Thanh toán có 3DS từ web |
| **`autoPaymentIntents(...)`** | `:376` | **Thanh toán off-session dùng cho cron auto-bill** |
| `createTaxRate($secretKey,$param,$logJob)` | `:413` | Tạo 消費税 rate |
| `createInvoiceItem(...)` | `:444` | Tạo invoice item |
| `getTaxRateById(...)` | `:474` | Lấy tax rate |
| **`createDataInvoice($secretKey,$taxRateId,$customerId,$params,$taxItem,$environment,$botId,$logJob)`** | `:488` | Phát hành hoá đơn có thuế; **tự tạo TaxRate và lưu ngược vào `s_strip_bot`** nếu thiếu (`:515-529`) |
| `getPaymentMethod` / `retrievePaymentIntent` | `:558` / `:571` | Truy vấn |

### 4.3 `App\Helpers\UnivapayPayment`
`src/web/sns-line/app/Helpers/UnivapayPayment.php` — 2.600+ dòng. Các method dùng cho 商品販売 (tất cả nhận `$univapay` = bản ghi `s_strip_bot` và `$flagEnvironment`):

| Method | Dòng | Vai trò |
|--------|------|--------|
| `getInfoTokenSale(...)` | `:1076` | Lấy thông tin thẻ từ transaction token |
| `chargeMoneyUnivapaySale(...)` | `:1156` | Charge 1 lần |
| `chargeInstallment(...)` | `:1244` | Charge trả góp (分割) |
| `getChargeIntsallment(...)` | `:1330` | Trạng thái charge trả góp |
| `getWebhook(...)` / `updateWebhook(...)` | `:1383` / `:1452` | Quản lý webhook của merchant |
| `getChargesSale(...)` / `getChargeStatus(...)` | `:1525` / `:1625` | Polling trạng thái charge |
| `getTypepayment($type)` | `:1697` | Map `item_type_payment` → cycle type UnivaPay |
| `cancelCharge(...)` | `:1711` | Huỷ charge |
| **`chargeMoneySubcriptionUnivapay(...)`** | `:1730` | **Tạo subscription định kỳ (継続課金)** |
| `getAccountInfo($secret,$token)` | `:1811` | Thông tin merchant (dùng bởi `iniSettingUnivapay`) |
| `getChargeSubcriptionSale(...)` | `:1883` | Chi tiết subscription |
| `updateSubcriptionSale(...)` | `:1945` | Đổi thẻ subscription |
| **`cancelSubcriptionSale(...)`** | `:1995` | **Huỷ subscription** (dùng bởi auto-cancel) |
| `refundMoney(...)` / `getRefundMoney(...)` | `:877` / `:924` | Hoàn tiền + xác nhận |
| `getMessageErrorUnivapay(...)` | `:2014` | Map mã lỗi → tiếng Nhật |

### 4.4 Helper functions toàn cục
Toàn bộ nằm trong **`src/web/sns-line/app/Helpers/functions.php`** (~11.700 dòng). **Không có `app/helpers.php`.**

| Hàm | Dòng | Vai trò |
|-----|------|--------|
| `getBotId()` | `:378` | `Session::get('current_bot_id')` |
| `resizeImageToMaxSize($file,$dest,$maxSize=2048)` | `:995` | Resize ảnh; kiểm tra MIME phải `image/*` |
| `checkFullUrl($url)` | `:2508` | `strpos($url,'http') === 0` |
| `updateMessageSendCount($botId,$date,$typeChat,$amount=1)` | `:2961` | Tăng bộ đếm `SummaryMessageSend` |
| `addLogUserAction($action)` | `:9224` | **Chỉ ghi log file, KHÔNG ghi DB** |
| **`sendActionOrderItem(...)`** | `:6526` | Xem mục 5.1 |
| `sendAction(...)` | `:7903` | Xem mục 5.1 |
| `insertMobileNotify(...)` | `:6765` | Ghi thông báo app (legacy) |
| `checkEnableInsertNotify($botId,$action,$flag)` | `:~6709` | Kiểm tra cấu hình `notify_setting` trước khi ghi notify |
| `isProcessWithWebhook($stripBot)` | `:138` | `univapay_webhook_id` có + `status_webhook == 1` |
| `isProcessedStatusCallbackUnivapay($botContractId)` | `:149` | Polling `bot_contracts.process_status`, tối đa 80 lần × `sleep(4)` |

---

## 5. Events / Listeners / Queued Jobs / Artisan Commands

### 5.1 エルメアクション — `sendActionOrderItem` → `sendAction` → bảng `action_lineuser`

`src/web/sns-line/app/Helpers/functions.php:6526`

```php
sendActionOrderItem($type, $action_id, $number_action, $botItem, $line_user_id,
                    $logCustom = false, $productId = null, $orderId = null)
```

| `$type` | Dòng | Counter `bot_line_user_item` được +1 | `type_start_scenario` ghi vào `action_lineuser` |
|--------|------|--------------------------------------|-----------------------------------------------|
| `view_page` | `:6543` | `count_action_view_page` | `12001` (単品) / `13001` (継続) — ⚠ biến `$sItem` chưa khởi tạo ở nhánh này nên **luôn ra `13001`** (bug, `:6557`) |
| `click_button` | `:6563` | `count_action_click_button` | `billItemClickButton` |
| `contract_trial` | `:6579` | `count_action_contract_trial` | `13003` |
| `contract` | `:6595` | `count_action_contract` | `12002` (単品) / `13002` (継続) |
| `purchase_1st` | `:6616` | `count_action_purchase_1st` | `13004` |
| `purchase_2st` | `:6632` | `count_action_purchase_2st` | `13005` |
| `bill_error` | `:6648` | `count_action_buy_error` | `13006` |
| `cancel` | `:6664` | `count_action_cancel` | `13007` |

Quy tắc `number_action`: `0` = gửi **mọi lần**; `1` = **chỉ gửi lần đầu** (khi counter tương ứng đang `= 0`).
Giá trị trả về: `1` = đã gửi, `2` = bỏ qua vì đã gửi, `0` = exception.

**`sendAction()` (`:7903`) ghi vào đâu** — quan trọng cho job-analyzer:
- Nhánh async (nhánh mà sales luôn đi vào): **INSERT 1 bản ghi `action_lineuser`** (`:8625-8637`) với `bot_id`, `line_user_id`, `type`, `action_id`, `type_start_scenario`, `product_id` (= `s_items.id`), `order_id`, **`status = 0` (chưa xử lý)**, `from_id`, `table_history`. → consumer/worker khác pick up để gửi tin LINE.
- Nhánh đồng bộ (`friendList` / `chat11W`): thực thi ngay và có thể ghi **`sync_elasticsearch`** (`:8584`) khi `env('API_KEY_ES')` được set.

> **Kết luận**: sales **không** dispatch Job Laravel nào cho エルメアクション; nó chỉ đẩy hàng đợi qua bảng `action_lineuser`. Bảng `action_schedules` **không liên quan** tới sales (Cao).

### 5.2 Queued Job

**`App\Jobs\HandleWebhookUnivapay`** — `src/web/sns-line/app/Jobs/HandleWebhookUnivapay.php`

- `implements ShouldQueue` (`:15`), dùng `Dispatchable, InteractsWithQueue, Queueable, SerializesModels`.
- **Không khai báo** `$queue`, `$connection`, `$tries`, `$timeout` → chạy trên queue `default`, connection mặc định = `env('QUEUE_DRIVER', 'database')` (`config/queue.php:18`) tức bảng `jobs` (`config/queue.php:37-40`).
- **Không có try/catch** trong `handle()` → exception đẩy sang `failed_jobs`.
- `handle()` (`:37-73`) định tuyến theo `$data['metadata']['module']`:

| `module` | Xử lý |
|---------|------|
| `sales` (`:63`) | `SalesService::handleOrderCallback()` |
| `sales_change_card` (`:66`) | `SalesService::callbackChangeCard()` |
| `sales_job` (`:69`) | `SalesService::callbackJob()` |
| `lesson`, `salon`, `event-booking`, … | Các service khác (không thuộc FA-026) |

**Nơi dispatch**:
- `src/web/sns-line/app/Http/Controllers/WebhookUnivapayControler.php:34` — endpoint webhook thật; chỉ dispatch khi `event == 'charge_finished'` và `metadata.module` nằm trong whitelist (`:18-29`); luôn trả `{"status":"success"}` (`:38-40`).
- `src/web/sns-line/app/Services/Sales/SalesService.php:2564`, `:2695` — self-dispatch từ `getOrderTimeout()` (fallback khi webhook không tới).

> **Metadata `module = 'sales'`** được gắn khi tạo charge — xem `SalesManagementV2Controller.php:2586-2594` (Stripe) và `:5010-5021` (UnivaPay).

**Job KHÔNG tồn tại**: không có job nào cho CSV export, không có job nào cho auto-bill (dùng Artisan Command thay thế). Tin cậy **Cao**.

### 5.3 Artisan Commands + lịch cron

`src/web/sns-line/app/Console/Kernel.php`

| Dòng | Command | Lịch | Vai trò với FA-026 |
|------|---------|------|-------------------|
| **`:160`** | **`handle:bill_stripe`** (`app/Console/Commands/HandleBillStripe.php`) | **`dailyAt('07:00')`** | ★ **Thanh toán định kỳ 継続商品**. Quét `s_cycle_order_history` có `status_bill = 1` và `item.is_product_new = 1` (`:76-81`); tới hạn khi `trial_expired_time < now && status_trial = 1` hoặc `c_expired_date < now && status_trial = 0` (`:108`); charge Stripe, tạo `s_order_history`, ghi `s_order_history_notify` (`:735`), upsert `s_monthly_item` (`:138-140`), bắn action `bill_error`(`:370`) / `purchase_1st`(`:541`) / `purchase_2st`(`:550`) / `contract_trial`(`:638`) / `cancel`(`:810`). Bỏ qua bot hết hạn quá 7 ngày (`:102-106`). |
| **`:172`** | **`handle:HandleSendActionTrialV2`** | **`dailyAt('07:00')`** | Bản song song chuyên xử lý **trial**: bắn `contract_trial` (`:115`, `:615`), `bill_error` (`:388`), `purchase_1st/2st` (`:533`, `:542`), `cancel` (`:813`). |
| **`:161`** | **`refresh:month_sales`** (`app/Console/Commands/refreshMonthSales.php`) | **`dailyAt('00:05')`** | ★ **Chỉ chạy vào ngày 01** (`:54`). Reset `s_items.current_month_sales` và `current_month_sales_test` về 0 (`:59-62`); tạo bản ghi `s_monthly_item` cho tháng mới và **carry-over `m_trial`, `m_trial_test`** từ tháng trước (`:67-89`). |
| **`:186`** | **`recover:payment_univapay_timeout`** | **`everyFiveMinutes()`** | ★ Gọi `SalesService::getOrderTimeout()` (`RecoverPaymentUnivapayTimeout.php:65`) → dispatch `HandleWebhookUnivapay` cho đơn treo > 15 phút. |
| `:159` | `univapay:check_status_webhook` | `dailyAt('01:00')` | Kiểm tra & tự sửa cấu hình webhook UnivaPay của từng bot; cập nhật `s_strip_bot.status_webhook` (`CheckStatusWebhook.php:76-86`). |
| `:151` | `job:check_auto_payment_univapay` | `dailyAt('06:30')` | Auto-bill **hợp đồng bot**, không phải 商品販売. |
| `:149` | `job:check_auto_payment` | `dailyAt('00:01')` | **Đã comment out**. |

**Command chạy thủ công (không có trong schedule)** liên quan bill-item: `change:status_bill_fail`, `recover:order_notify`, `recover:notifyItem`, `recover:info_user_bill_item`, `job:RecoverActionBillItem`, `recover:richmenuItemBill`, `recover:last-four-card-univapay`, `recover:RecoverFlagBranchCardUnivapay`, `handle:export_csv`, `handle:export_csv2`.

---

## 6. Luồng webhook UnivaPay (tổng hợp)

```
UnivaPay ──charge_finished──► POST /mobile/univapay-callback-payment (WebhookUnivapayControler@webhook, web.php:4020)
                                    │ whitelist module ∈ {sales, sales_change_card, sales_job, …}
                                    ▼
                            HandleWebhookUnivapay::dispatch()   [queue: default, driver: database]
                                    ▼
        module=sales        → SalesService::handleOrderCallback()   (SalesService.php:174)
        module=sales_change_card → SalesService::callbackChangeCard() (:809)
        module=sales_job    → SalesService::callbackJob()             (:1239)
                                    ▼
              cập nhật s_order_history / s_cycle_order_history.status_webhook

Fallback (đơn treo > 15 phút):
  cron recover:payment_univapay_timeout (mỗi 5') → SalesService::getOrderTimeout() (:2469)
     → polling charge từ UnivaPay/Stripe → HandleWebhookUnivapay::dispatch(from_job = true)
```

Trong lúc chờ, phía web `paymentCreditCardItemV2Univapay` gọi `checkStatusProcessCallback()` (5 lần × 1s); nếu chưa xong → đặt `status_webhook = 4 (TIMEOUT_WEBHOOK)` và trả `pending` cho UI.

> ⚠ Route `POST /product-callback/{bot_id}` (`web.php:4034`) tuy vẫn tồn tại nhưng **thân hàm đã comment out hoàn toàn** (`SalesManagementV2Controller.php:3813-3880`) → không xử lý gì.

---

## 7. Form Requests / Validation

**Không có Form Request nào cho tính năng này.** Grep `app/Http/Requests/` với `sales|item|order|bill|product` → **0 kết quả** (tin cậy Cao). Toàn bộ validation nằm inline trong controller.

| Nơi | Cơ chế |
|-----|--------|
| **V2 `saveItem`** | **Không dùng `Validator`** — chỉ kiểm tra `s_category_id` thuộc bot (`:896-905`) và giới hạn gói (`:954`). **Toàn bộ ràng buộc nhập liệu chỉ tồn tại ở client** (`public/js/sales/v2/add-single-item.js:600-655`). |
| **V1 `storeItem` / `saveItem`** | Có `Validator::make` trong `validateItem()` (`SalesManagementController.php:1002-1108`) |
| **Endpoint thanh toán** | Chỉ kiểm tra thủ công: số lượng > 0, tồn kho, tồn tại item/bot |
| **API mobile** | Không validate |

---

## 8. Authorization

- **Không có Policy, không có Gate** cho tính năng này (grep `app/Policies/` → không có class liên quan sales; tin cậy Trung bình).
- Phân quyền dựa hoàn toàn vào middleware **`basic_access`** (`app/Http/Middleware/BasicAccess.php`):
  - Nếu `session('is_bot_invite')` = true (Staff được Admin mời) hoặc `bot->admin_id !== Auth::id()` → lấy whitelist route qua `getRouterBotInvite()`; route hiện tại không nằm trong whitelist → redirect `adminIndex` kèm lỗi 「この権限は許可されていません。」 (`:38-51`).
  - **Ghi log truy cập Staff**: `UserAccessBot::create()` 1 lượt/staff/bot/ngày (`:65-72`).
  - → **Quyền Staff với 商品販売 là quyền theo route (all-or-nothing)**, không có phân quyền chi tiết ở mức chức năng (xem/sửa/xoá) — tin cậy **Trung bình** (cần đọc `getRouterBotInvite()` và bảng phân quyền để xác nhận danh sách route cụ thể).
- **Cách ly dữ liệu theo bot** phụ thuộc vào việc mỗi truy vấn tự thêm `where('bot_id', getBotId())`. Các chỗ **thiếu** đã liệt kê ở mục 2 (rủi ro IDOR).

---

## 9. Business Rules

### BR-01 · Giới hạn số sản phẩm theo gói hợp đồng
`SalesManagementV2Controller.php:816-847` (`canCreateItemByPlan`) và `:191-217` (`index`).

| Điều kiện | Giới hạn mỗi loại (単品 / 継続) |
|-----------|-------------------------------|
| `bot_contracts.contract_type == 'free'` **hoặc** `bots.plan_type == 2` | **1 sản phẩm** (`:837-839`) |
| `bots.flag_contract_new == 1` **và** `contract_type == 'standard'` | **10 sản phẩm** (`:842-844`) |
| Còn lại | Không giới hạn (`:846`) |

- Đếm chỉ tính `is_product_new = 1`, phân biệt `type_payment == 0` (単品) và `<> 0` (継続).
- Áp dụng ở **cả** `saveItem` khi tạo mới (`:954`) và `ajaxCopyItem` (`:1415`).
- Vượt giới hạn → 「現在のプランは利用できない機能です。アップグレードが必要になります。」
- **V1** có quy tắc riêng: `plan_type == 2` → tối đa 1 単品 + 1 継続 (`SalesManagementController.php:633-655`).

### BR-02 · Ràng buộc nhập liệu form sản phẩm

**V2 (chỉ ở client — `public/js/sales/v2/add-single-item.js:600-655`)** — tin cậy **Cao** về vị trí code, và **Cao** về kết luận "server không kiểm tra":

| Trường | Rule | Thông điệp |
|-------|------|-----------|
| `name` (商品名) | required, **max 20 ký tự** (`:605`) | 「商品名は20文字以内で入力してください。」 |
| `product_name` (表示商品名) | required, **max 50** (`:606`) | 「表示商品名は50文字以内で入力してください。」 |
| `supplement_product` (説明) | required, **max 50** (`:607`) | 「説明は50文字以内で入力してください。」 |
| `amount` (商品価格) | required, **min 100** (`:608`) | 「請求価格は100円以上を設定してください。」 |
| `amount_first` (初回トライアル価格) | required, **min 100** khi `flag_first = 1` (`:638`) | 「請求価格は100円以上を設定してください。」 |
| `time_trial` (無料期間設定) | **min 1** khi `flag_trial = 1` (`:634`) | 「トライアル日数は1日以上入力してください。」 |
| `quantity_stock` (在庫数) | **min 0** khi `flag_use_stock = 1` (`:620`) | 「1以上入力してください」 |
| `max_per_person` (購入上限) | **min 1** khi `flag_use_max_per_person = 1` (`:624`) | 「1以上入力してください」 |
| `text_button_start` / `text_button_friend_info` / `text_confirm_button` / `text_payment_button` | **max 15** | 「ボタンテキストは15文字以内で入力してください。」 |
| `text_button_cancel` (解約ボタン) | **max 10** khi `type_payment != 0` (`:642`) | 「解約ボタンは10文字以内で入力してください。」 |
| `url_page_outsite_end` | định dạng URL khi `flag_page_end = 1` (`:628`) | 「URLのフォーマットで入力してください。」 |
| `payment_method`, `s_category_id`, `page_start_simple`, `final_confirm_page` | required | — |
| Tên item của 表示項目名 (お客様情報) | max 30 (`:880`) | 「表示項目名は30文字以内で入力してください。」 |
| Tên folder | max 15 (`list-items-v2.js:367`) / 50 (`:394`) | 「フォルダ名は15文字以内で入力してください。」 |

> ⚠ **Rủi ro**: mọi giới hạn trên có thể bỏ qua bằng cách gọi thẳng `POST /ajax/sales/save-item` (endpoint được **miễn CSRF** vì thuộc `/ajax/*`). Giá 0円, tên 10.000 ký tự đều được server chấp nhận. Tin cậy **Cao**.

**V1 (server-side)** — `SalesManagementController.php:1004-1101`: `amount` `min:50`, `amount1st` `min:50`, `freetrial_days` `min:1`, các trường page `required`/`url`. **Không có giới hạn ký tự, không có 100円** — tức 100円 là quy tắc **chỉ của V2**.

### BR-03 · 決済システム (payment_method) không đổi được sau khi lưu
- Không có kiểm tra ở server: `saveItem` vẫn nhận `payment_method` khi update (`:874`).
- Ràng buộc nằm ở client: sau khi lưu/tải chi tiết, giá trị được lưu vào `paymentMethodOld` (`add-single-item.js:488`, `:546`) và UI khoá dropdown.
- **Kết luận**: ràng buộc **chỉ ở UI**, server vẫn cho phép đổi — tin cậy **Cao**.

### BR-04 · 在庫数 (tồn kho) & 購入上限 (giới hạn mua/người)

**Tồn kho** — tin cậy **Cao**:
- Công thức (`:1641-1652`, `:2554-2561`, `:4921-4935`):
  - 単品: `quantity_stock - SUM(s_order_history.quantity_purchased WHERE status_order = 1 AND flag_environment = item.flag_environment)`
  - 継続: `quantity_stock - SUM(s_cycle_order_history.quantity_purchased WHERE status_bill <> 3 AND flag_environment = item.flag_environment)`
- Chỉ chặn khi `flag_use_stock == 1`.
- Thông điệp: 「在庫切りです。{còn lại}以下入力してください」; hết hàng → 「在庫がないので、購入できません。販売者に連絡してください。」
- **Nơi kiểm tra**:
  - UnivaPay: **trước khi tạo đơn** (`:4939`)
  - Stripe: **sau khi đã tạo bản ghi đơn**, nếu vượt thì xoá lại (`:2563-2583`) → tồn tại race condition
  - `SalesStripePaymentController::paymentCreditCardItemV2`: **đã comment out** (`:749-773`)

**購入上限 `max_per_person`** — tin cậy **Cao**:
- **Không có bất kỳ kiểm tra nào ở server.** Grep toàn `app/` chỉ ra `max_per_person` xuất hiện duy nhất trong danh sách `$request->only()` của `saveItem` (`:862-868`).
- Chỉ chặn ở client: `resources/views/basic/sales/v2/order/detail.blade.php:550-551` (alert) và thuộc tính `max` của input (`:437`).
- → **Người mua có thể vượt giới hạn bằng cách gọi API trực tiếp.**

### BR-05 · Công thức tính số tiền
`SalesManagementV2Controller.php:2437-2449` (Stripe) và `:4968-4980` (UnivaPay). Tin cậy **Cao**.

| `type_payment` | `flag_trial` | `flag_first` | Số tiền kỳ đầu |
|---------------|-------------|-------------|---------------|
| `0` (単品) | — | — | `amount` |
| `<> 0` (継続) | `!= 1` | `1` | `amount_first` |
| `<> 0` | `!= 1` | `!= 1` | `amount` |
| `<> 0` | `1` | `1` | `amount_first` |
| `<> 0` | `1` | `!= 1` | **`0`** (chỉ tạo SetupIntent để lưu thẻ) |

Tổng tiền = số tiền kỳ đầu **× số lượng mua** (`:2449`, `:5002`).

⚠️ **ĐÍNH CHÍNH (xác minh từ source, tin cậy Cao)** — các kỳ tiếp theo do cron charge = **`s_items.amount` HIỆN TẠI** × `s_cycle_order_history.quantity_purchased`, **không** dùng `amount_item`:
- `HandleBillStripe.php:173` — `$amount = $item->amount;` (nhánh `amount_first` bị comment out tại `:174-178`) → `:186` `$amount = $amount * $quantity_purchased;`
- `HandleSendActionTrialV2.php:180` — `$amount = $item->amount;` → `:189` nhân `quantity_purchased`

`s_cycle_order_history.amount_item` **chỉ là snapshot dùng để HIỂN THỊ** 「販売価格」 tại SCR-BIL-19, không tham gia tính tiền.

**Hệ quả nghiệp vụ**: nếu Admin đổi giá sản phẩm sau khi khách đã đăng ký, khách sẽ bị trừ **giá mới** ở kỳ kế tiếp mà không được thông báo. Xem thêm rủi ro cùng gốc tại `job/job-spec.md` (`ActionModel.AMOUNT_ORDER` cũng đọc giá hiện tại của `s_items` thay vì giá đã chốt trong đơn) — hai nơi khác nhau nhưng cùng một nguyên nhân.

### BR-06 · Chu kỳ thanh toán & ngày hết hạn kỳ kế
`config/sns-line.php:412-419`:

| Giá trị | Ý nghĩa | Nhãn CSV (`CycleOrderHistoryExportV2.php:27`) |
|--------|--------|----------------------------------------------|
| `0` | once (単品) | — |
| `1` | weekly | 毎週 |
| `2` | monthly | 毎月 |
| `3` | 3month | 3ヶ月毎 |
| `4` | 6month | 6ヶ月毎 |
| `5` | yearly | 毎年 |

`calculateNextExpiredDateItem()` (`SalesManagementV2Controller.php:5969`, `SalesStripePaymentController.php:1508`, `SalesService.php:2444`):
- weekly: `+7 days` rồi ép giờ **`06:58:59`** (`:5973`) — mốc này nằm trước cron `handle:bill_stripe` chạy 07:00.
- monthly / 3month / 6month / yearly: uỷ quyền cho `UserPointSettings::nextExpireMonthItem / nextExpire3MonthItem / nextExpire6MonthItem / nextExpireYearItem`.

`number_charge` (回数): `0` → `number_continue = -1` (**vô hạn**); ngược lại `number_continue = number_charge` (hoặc `- 1` nếu đã bill ngay) — `CycleOrderHistory.php:41-49`.
Hết số kỳ → `status_bill = 2` (決済終了) và `bot_line_user_item.status_contract = 2` (`SalesStripePaymentController.php:1648`, `:1656`).

### BR-07 · 請求エラー 3 lần liên tiếp → tự động huỷ
Tin cậy **Cao**.

| Vị trí | Code |
|--------|------|
| `SalesManagementV2Controller.php:4542-4554` | `if ($item->auto_cancel == 1) { $countBill = …count_bill_error; if ($countBill >= 3) { $this->univapayPayment->cancelSubcriptionSale(...); } }` |
| `SalesManagementV2Controller.php:6232-6235`, `:6667-6670` | Cùng logic trong `changeCardItem` / `changeCardUnivapay` |
| `SalesStripePaymentController.php:1586-1591` | `if ($countBill >= 3) { $autoCancel = $this->cancelCycle($cycle, $botItem, $item); }` |

- Bộ đếm: lần lỗi đầu tiên set `count_bill_error = 1` **và** tạo `s_order_history` với `status_order = 3` (`:4501-4531`); các lần sau `+1` (`:4533-4535`).
- **Reset về `null`** khi bill lại thành công (`:4707`, `:4719`, `:4748`, `:4769`, `:6418`, `:6803`).
- Chỉ tự huỷ khi `s_items.auto_cancel == 1`; nếu tắt thì hợp đồng ở trạng thái 期限切れ vô thời hạn.
- Khi bill lỗi và `s_items.flag_msg_fail == 1` → gửi tin LINE 「{商品名}の定期決済に失敗しました。…クレジットカード情報変更はこちら [CHANGE_{item_code}]」 (`:4537-4541`, template ở `:4057`).
- Đồng thời bắn エルメアクション `bill_error` (`:4556-4562`) và `insertMobileNotify` với `money_bill = 4` (`:4565-4578`).

### BR-08 · Thuế tiêu thụ (消費税) 10% / 8%
Tin cậy **Cao**.

- `s_items.tax_item` mặc định `10` (schema `db/schema/tables/s_items.sql`, và default JS `add-single-item.js:98`).
- Ánh xạ sang TaxRate của Stripe (`SalesManagementV2Controller.php:6311-6324`; `SalesStripePaymentController.php:885-897`, `:1083-1095`):

| `tax_item` | `flag_environment = 1` (本番) | `flag_environment = 0` (テスト) |
|-----------|------------------------------|-------------------------------|
| `10` | `s_strip_bot.tax_rate_id_percent_10` | `tax_rate_id_test_percent_10` |
| khác (8) | `tax_rate_id_percent_8` | `tax_rate_id_test_percent_8` |

- TaxRate được tạo lần đầu ở `SalesManagementController::linkPayment` (`:187-231`) với `['display_name' => '消費税', 'inclusive' => true, 'percentage' => 8|10, 'jurisdiction' => 'JP']` → **内税 (thuế đã bao gồm trong giá)**.
- `StripePayment::createDataInvoice()` (`:488`) tự tạo lại TaxRate và lưu ngược vào `s_strip_bot` nếu thiếu (`:515-529`).
- ⚠ **UnivaPay không có xử lý thuế** — `createDataInvoice` chỉ được gọi ở nhánh Stripe. Tin cậy **Cao**.

### BR-09 · トライアル (dùng thử)
- `flag_trial = 1` + `time_trial` (số **ngày**).
- Hạn trial = `now()->addDay(time_trial)->format('Y-m-d 23:59:59')` (`:4980`; `SalesStripePaymentController.php:161`, `:790`).
- Khi có trial: `status_trial = 1`, `number_payment = 0`, `number_continue = number_charge` (chưa trừ) — `CycleOrderHistory.php:41-49`.
- Nếu **có** `flag_first = 1` → vẫn charge `amount_first` ngay khi đăng ký; nếu **không** → charge `0` và chỉ tạo SetupIntent.
- Huỷ trong thời gian trial → `s_items.number_trial(_test) - 1` và `number_cancel(_test) + 1` (`:3604-3629`).
- Action `contract_trial` được bắn bởi cron `handle:HandleSendActionTrialV2` (`:115`, `:615`), **không** bắn từ web (các lời gọi trong controller đã comment out — `:4756`, `:6372`).

### BR-10 · 本番環境 / テスト環境 (`flag_environment`)
Tin cậy **Cao**.

- `0` = テスト, `1` = 本番 (comment schema `s_items.flag_environment`).
- Là **thuộc tính của sản phẩm**, quyết định:
  - Khoá Stripe dùng: `strip_secret_test_key`/`strip_public_test_key` vs `strip_secret_live_key`/`strip_public_live_key` (`:1654-1658`, `:2456-2460`, `:3210-3214`).
  - Khoá UnivaPay: `univapay_app_test_id`/`univapay_app_token_test`/`univapay_secret_test` vs bản live (`:3774-3776`).
  - TaxRate test vs live (BR-08).
  - Bộ counter thống kê **tách đôi**: `number_register` vs `number_register_test`, `sum_sales` vs `sum_sales_test`, `current_month_sales` vs `current_month_sales_test`, tương tự cho `number_trial`, `number_cancel`, `number_refund`.
  - Truy vấn danh sách sản phẩm và lịch sử luôn lọc theo `flag_environment` (`:1235`, `:1312`, `SCategory.php:32`, `:59`).
- Tin nhắn LINE khi bill ở môi trường test có prefix 「【ご注意】これはテスト決済なので実際には課金されません」 (`:4051`).
- **API mobile chỉ trả dữ liệu 本番** (`Api/SalesController.php:27`, `:30`).

### BR-11 · Trạng thái đơn hàng
Tin cậy **Cao** (đọc từ `CycleOrderHistoryExportV2.php:80-106` và các nhánh update).

**`s_order_history.status_order`**: `1` = 決済成功, `2` = 返金済み/キャンセル, `3` = 決済エラー/延滞.
**`s_cycle_order_history.status_bill`**: `1` = 継続中, `2` = 決済終了 (hết số kỳ), `3` = キャンセル済.
**`s_cycle_order_history.status_trial`**: `1` = đang trial.
**`bot_line_user_item.status_contract`** (`config/sns-line.php:420-425`): `0` unregister, `1` registered, `2` complete, `3` cancel.
**`status_webhook`** (`app/OrderHistory.php:13-17`): `0` UNPROCESSED, `1` PROCESSED, `2` ERROR, `3` TIMEOUT, `4` TIMEOUT_WEBHOOK.

Nhãn hiển thị 継続 (`CycleOrderHistoryExportV2.php:80-106`):

| Điều kiện | Nhãn |
|-----------|-----|
| `status_trial=0` + `last_bill_id` có + `status_bill=1` + `status_order<>3` | 継続中 |
| `status_trial=0` + `last_bill_id` có + `status_bill=1` + `status_order=3` | 延滞中 |
| `status_trial=0` + `last_bill_id` null + `status_bill=1` | 継続中 |
| `status_bill=2` | 決済終了 |
| `status_trial=1` + `status_bill=1` | トライアル中 |
| `status_bill=3` | キャンセル済 |

### BR-12 · Trang hoàn tất (`flag_page_end`)
`resources/views` + `public/js/sales/v2/confirm-order.js:70-80`:
- `0` → thay nội dung body bằng HTML `page_end_simple`
- `1` → redirect `url_page_outsite_end`
- `2` → redirect về chat LINE (`bots.url_add_friend`, trả qua `urlRedirectChat`)

### BR-13 · Sinh `item_code`
`randomItemCodeRecursion()` (`SalesManagementV2Controller.php:536`, `SalesManagementController.php:594`): `str_random(10)`, kiểm tra trùng trong `s_items.item_code`, đệ quy tới khi unique. → URL công khai `/{v2}/order-item/detail/{item_code}/{u_code}` (Cao).

### BR-14 · Chặn thao tác khi đơn đang chờ webhook
Khi `status_webhook ∈ {0 UNPROCESSED, 3 TIMEOUT, 4 TIMEOUT_WEBHOOK}` thì:
- Admin không huỷ được hợp đồng (`:1058-1064`, `:3583-3591`)
- LINE User không mở được trang mua lại (`:1592-1618`), trang 解約 (`:1778-1785`), trang đổi thẻ (`:1882-1889`)
→ Thông điệp thống nhất 「決済処理を行っていますので、操作できません。」

---

## 10. Ghi chú cho bước job-analyzer

Các điểm code ghi vào bảng hàng đợi / dispatch job / gọi cron — **đây là đầu mối cần đối chiếu với Spring Boot**:

| Bảng / cơ chế | Nơi ghi (Laravel) | Ý nghĩa |
|--------------|-------------------|--------|
| **`action_lineuser`** (App\ActionLineUser) ⚠ *không phải `action_line_users`* | `app/Helpers/functions.php:8625` (từ `sendAction`), được gọi qua `sendActionOrderItem` tại `SalesManagementV2Controller.php:1074, 1631, 3633, 4557, 4684, 5918, 5934, 5944, 6240, 6356, 6365, 6748, 6757`; `SalesStripePaymentController.php:264, 439, 1454, 1470, 1480, 1774`; `SalesManagementController.php:1338, 1525`; `HandleBillStripe.php:370, 541, 550, 638, 810`; `HandleSendActionTrialV2.php:115, 388, 533, 542, 615, 813` | Hàng đợi thực thi エルメアクション, `status = 0` chờ consumer xử lý. Cột `product_id` = `s_items.id`, `order_id` = id đơn, `type_start_scenario` = mã 12001/12002/13001…13007 |
| **`sync_elasticsearch`** (connection `mysql_step_message`) | `SalesManagementV2Controller.php:5786`; `SalesStripePaymentController.php:563, 1330`; `SalesService.php:653`; `functions.php:8584` | Hàng đợi đồng bộ hồ sơ bạn bè sang Elasticsearch. **Chỉ ghi khi `env('API_KEY_ES')` được set** (`app/SyncElasticsearch.php:15-20`) |
| **`s_order_history_notify`** | `SalesManagementV2Controller.php:4820, 6265, 6402, 6691, 6787`; `SalesStripePaymentController.php:584`; `SalesService.php:989, 1147, 1385, 1389, 1551, 2364`; `HandleBillStripe.php:735`; `HandleSendActionTrialV2.php` (5 chỗ) | Hàng đợi thông báo đơn hàng cho app mobile. `status_order`: `-1` mua lần đầu thất bại, `-2` huỷ đơn |
| **`s_monthly_item`** | `SalesService.php:415, 436, 489, 513, 2155`; `SalesManagementV2Controller.php:5250, 5271, 5581, 5605`; `refreshMonthSales.php:68, 77, 84`; `HandleBillStripe.php:138-140`; V1 `SalesManagementController.php:763, 1309-1465` | Thống kê doanh số tháng. ⚠ **V2 đã comment out phần cập nhật khi refund/huỷ** (`:3120-3189`, `:3578-3617`) |
| **`jobs`** (queue driver `database`) | `HandleWebhookUnivapay::dispatch()` tại `WebhookUnivapayControler.php:34`, `SalesService.php:2564, 2695` | Job Laravel duy nhất của tính năng. Queue `default`, không set `tries`/`timeout` |
| **`mobile_notify`** | `insertMobileNotify()` (`functions.php:6765`) + `MobileNotifyService::insertNotifyItem()` — hàng chục điểm gọi | Thông báo app. `type` = 8 (`bill_one`) / 9 (`bill_cycle`); `money_bill`: `0` đăng ký, `1` thất bại, `2` huỷ, `3` bill chu kỳ thành công, `4` bill chu kỳ thất bại |
| **`csv_management`** | ❌ **Không dùng** — export CSV của bill-item chạy **đồng bộ** qua `Excel::download()` | Bảng này chỉ phục vụ import/export danh sách bạn bè |
| **`action_schedules`** | ❌ **Không liên quan** — sales không ghi vào bảng này | Thuộc tính năng アクション予約 riêng |

**Cron cần đối chiếu với Spring Boot**:
| Command | Giờ | Vai trò |
|---------|-----|--------|
| `handle:bill_stripe` | 07:00 | Thanh toán định kỳ 継続商品 |
| `handle:HandleSendActionTrialV2` | 07:00 | Xử lý kết thúc trial + bắn action |
| `refresh:month_sales` | 00:05 (chỉ ngày 01) | Chốt sổ / khởi tạo thống kê tháng |
| `recover:payment_univapay_timeout` | mỗi 5 phút | Cứu đơn treo > 15 phút |
| `univapay:check_status_webhook` | 01:00 | Tự sửa cấu hình webhook |

---

## 11. Danh sách rủi ro / bug đáng lưu ý

| # | Vị trí | Vấn đề | Tin cậy |
|---|--------|--------|--------|
| 1 | `SalesManagementV2Controller.php:849` | `saveItem` **không có validation server** — mọi ràng buộc (100円, 20/50文字…) chỉ ở JS, endpoint lại được miễn CSRF | Cao |
| 2 | Toàn bộ V2 | `max_per_person` (購入上限) **không được enforce ở server** | Cao |
| 3 | `:2553-2583` | Kiểm tra tồn kho ở nhánh Stripe chạy **sau khi** đã tạo bản ghi đơn → race condition | Trung bình |
| 4 | `SalesStripePaymentController.php:749-773` | Kiểm tra tồn kho bị comment out | Cao |
| 5 | `:3120-3189`, `:3578-3617` | Cập nhật `s_monthly_item` khi refund/huỷ bị comment out ở V2 → **thống kê tháng sai lệch** | Cao |
| 6 | `:3806-3885` | Webhook `/product-callback/{bot_id}` rỗng hoàn toàn | Cao |
| 7 | `web.php:900`, `:3738` | 2 route trỏ tới method không tồn tại (`viewAddSingleItem`, `orderIndex` ở V2) | Cao |
| 8 | `:390` | `renameGroup` update sai bảng (`category` thay vì `s_categories`) | Cao |
| 9 | `:1099` | `orderHistoryDetail` không lọc `bot_id` | Trung bình |
| 10 | `:1998` | So sánh `'preivew'` (sai chính tả `preview`) | Cao |
| 11 | `:6944`, `:6975` | Export CSV trả `null` khi `bots.view_name` rỗng | Cao |
| 12 | `functions.php:6557` | `$sItem` chưa khởi tạo trong case `view_page` → luôn dùng mã action `13001` | Cao |
| 13 | `SalesStripePaymentController.php:70, 77, 621, 632` | `if($flagName = 0 && …)` là phép **gán** → `name_friend` luôn `null` | Cao |
| 14 | `SalesStripePaymentController.php:1832-1836` | `getMessageError` luôn fallback về `processing_error`, nuốt message gốc Stripe | Cao |
| 15 | `SalesManagementController.php:90, 91, 131, 132` | **Ghi Stripe secret key ra log** | Cao |
| 16 | `SalesManagementController.php:523, 562, 992, 1212, 1260, 1389` | Update không lọc `bot_id` → IDOR | Cao |
| 17 | `web.php:3824-3962` | Nhóm endpoint thanh toán + bill-item AJAX **không có middleware auth** | Cao |
| 18 | Nhiều nơi | `DB::beginTransaction/commit/rollback` bị comment out ở hầu hết hàm ghi nhiều bảng | Cao |
| 19 | `:6890-6895` | `unlinkPaymentMethod` không xoá khoá **test** của UnivaPay | Cao |
| 20 | `:1929` | `flagInstallment` hard-code `0` ở trang đổi thẻ → tính năng trả góp bị tắt | Cao |
