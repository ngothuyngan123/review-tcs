# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Ticket #42781 đi qua **19 bản dev-impact (v1 → v19)** trong **28 journal note** (2026-10-29 → 2026-11-17, nhánh `ai_studio_implement_42781`) — các bản sau sửa đè/bổ sung bản trước, không phải 19 thay đổi độc lập cộng dồn. File này tổng hợp theo **trạng thái cuối cùng (v19 — Journal #155445, 17/11 15:12)**, có chú thêm các cột mốc quan trọng của v1/v4/v5/v6/v8 khi cần hiểu rationale. Review/approve gần nhất ghi nhận "Không còn câu hỏi chờ trả lời" (Journal #153854, v8) và 11 bug con + nhiều bug automation đều đã Dev confirm "đã sửa" kèm commit hash — xem Redmine #42781 journal #149383 → #155445 để trace đầy đủ nếu cần.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI Dev Studio (journal author "Dev Studio") — assignee Redmine: `Thanh Phương` (thanhntp) |
| Commit / Pull Request | `sns-line@1520e454eea9d45c12d56b75038c6fe6c0f47b35` (nhánh gốc `release_step_20260930_v2@0637cd04f7c1`) |
| Branch | `ai_studio_implement_42781` |
| Ngày submit đánh giá | 2026-11-17 (v19 cuối cùng; bản đầu 2026-10-29) |
| Auto-filled | `2026-11-17 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại toàn bộ journal "Đánh giá ảnh hưởng" trên Redmine #42781 (28 journal, đặc biệt các bản Dev handoff #149793/v2, #153352/v6-v7, #154508, #154773, #154789, #155055, #155198, #155445/v19) và xác nhận file này không sót impact.

---

## 1. Nguyên nhân

**Động lực ban đầu (v1, Journal #149383):** Hệ thống chưa có webhook Stripe nào cho bill item. Đơn bill item đã trừ tiền nhưng nếu khách đóng màn giữa chừng thì phải chờ 15–20 phút cron mới chốt đơn (trải nghiệm chậm, rủi ro đơn kẹt lâu).

**Root cause của bản sửa cuối cùng (v19, Journal #155445 — #46126/#5928):** Khối bắt lỗi của trang mua Stripe gọi `failStripeItemClaim` (gửi tin Chatwork "chốt dở" riêng của ticket), nhưng sau đó vẫn gửi tiếp tin lỗi chung có sẵn từ trước ticket → bị báo **2 tin Chatwork cho cùng 1 sự cố**. Lỗi cùng kiểu lặp lại ở handler webhook bill item, Event, Lesson và trang đặt Salon, vì helper `failStripeItemClaim` không trả về đã gửi hay chưa nên nơi gọi không biết để bỏ tin thứ hai.

**Các root cause trung gian đáng chú ý (đã fix, có thể còn tồn tại nếu test nhánh cũ):**
- v5 (#45308): Stripe **không cho dùng token OAuth để tự quản lý webhook endpoint theo từng bot** → phải đổi hẳn sang 1 endpoint Connect chung trên tài khoản platform.
- v3 (lỗi thiết kế v2): trình duyệt giành quyền chốt đơn **quá sớm** (trước khi ghi) → đơn đã thu tiền có thể bị kẹt nếu trình duyệt lỗi giữa đường.
- v3/v6: 4 lỗi trong hàm chốt dùng chung (`handleOrderCallback`/`callbackChangeCard`) ảnh hưởng cả Stripe và UnivaPay: dòng thống kê tháng tạo trùng/thiếu, affiliate đơn một lần không chạy action, tiền đổi thẻ không nhân theo số lượng.
- v7 (#45905 — slot): đổi lịch Event có 3DS mà webhook chốt trước, trình duyệt gọi lại không đếm lại slot → slot bị đầy giả.

## 2. Cách fix

**Thiết kế cuối cùng (v19, cumulative):**
- **Webhook mới** `POST /stripe/item-webhook` (Stripe **Connect** trên tài khoản platform, không dùng chữ ký riêng theo bot — đổi từ thiết kế v1-v4 do Stripe chặn OAuth token quản lý webhook per-bot): nhận `payment_intent.succeeded`, chốt ngay (qua queue) cho **bill item** (mua, đổi thẻ) và **Booking Event** (đặt mới, đổi lịch), **Lesson**, **Salon**. account phải khớp bot + phải có bản ghi đang chờ; id PaymentIntent sai dạng thì bỏ qua (200).
- **Job** `HandleStripeItemWebhook`: gọi lại Stripe lấy PaymentIntent bằng khoá của bot rồi chốt ngay bằng đúng handler cron đang dùng.
- **Giành quyền chốt (claim) theo PaymentIntent** bằng 1 lệnh UPDATE có điều kiện — áp cho cả 3 đường: trình duyệt, webhook, cron. Chỉ bên thắng chạy side-effect (action, thông báo, doanh thu); bên thua chỉ hiện màn hoàn tất (trình duyệt) hoặc bỏ qua (cron/webhook). Giành quyền **ngay trước lần ghi đầu tiên** (sửa từ lỗi giành quá sớm ở v2).
- **Lệnh** `php artisan recover:stripe_item_webhook [--stripe_env=all|test|live] [--bot_id=] [--dry-run]`: tạo/giữ/sửa endpoint Connect trên platform, kiểm token OAuth từng bot đã liên kết, ghi `s_strip_bot.stripe_status_webhook_test/live` (1/0), gửi 1 tin Chatwork tổng hợp, `exit 1` khi lỗi.
- **Màn liên kết/huỷ liên kết Stripe**: từ v5 (D-24 — bỏ webhook theo từng bot) liên kết/huỷ liên kết **KHÔNG** tạo/xoá endpoint Connect dùng chung; huỷ liên kết (LinkPaymentController, SalesManagementV2Controller) chỉ đặt `stripe_status_webhook_test/live` về NULL. (Bản v1–v2 từng tự cài/xoá webhook theo bot — đã bỏ.)
- **Cron** `recover:payment_univapay_timeout`: PaymentIntent Stripe thành công đi qua **cùng job giành quyền chốt** như webhook (không gọi handler trực tiếp nữa); giao dịch 3DS bỏ dở > 15 phút → gọi Stripe **huỷ PaymentIntent** trước, chỉ dọn dữ liệu sau khi Stripe xác nhận đã huỷ (quyết định của AnhTT, v8); chỉ báo lỗi khi thẻ thật bị từ chối.
- **Sửa 2 handler dùng chung với UnivaPay** (`SalesService::handleOrderCallback`, `callbackChangeCard`): dòng thống kê tháng (`s_monthly_item`) cộng nguyên tử có khoá dòng (không trùng/thiếu khi nhiều đơn chốt song song); mua 1 lần có affiliate chạy action + ghi `aff_result_id`; đổi thẻ tính tiền theo số lượng (`quantity_purchased` NULL = 1); bỏ cộng tay `count_action_contract`/`count_action_purchase_1st/2st` (tránh cộng đôi bộ đếm action).
- **Chatwork mới** (không chứa khoá bí mật): lỗi khoá/token bot (401/403); đã thu tiền nhưng đơn/hợp đồng không còn (đã xác minh PaymentIntent); thiếu dữ liệu để chốt; chốt dở; tin lỗi chung kèm `order_id`/`cycle_id`/`charge_id` (cắt ≤100 ký tự). (v19) Khi đã giành quyền chốt mà có sự cố → **chỉ 1** tin Chatwork, không kèm tin lỗi chung cũ (bug #46126/#5928 vừa fix).
- **Đổi lịch Event có 3DS** mà webhook chốt trước: lần gọi thứ 2 của trình duyệt **đếm lại slot/plan từ dữ liệu thật** trước khi trả response (fix v7, tránh slot đầy giả).
- **Chặn thu trùng**: còn lần thu đang chờ (trong 60 phút) → chặn thao tác mới, báo `「決済処理を行っていますので、操作できません。」`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `SalesService::handleOrderCallback` / `callbackChangeCard` | Sửa thống kê tháng (khoá dòng, nguyên tử), affiliate, nhân số lượng, bỏ cộng tay bộ đếm action | Dùng chung Stripe + UnivaPay → mọi thay đổi phải hồi quy cả UnivaPay |
| 2 | `StripePayment::retrievePaymentIntent` (7 nơi gọi) | Trả thêm message/code/HTTP status, không ném exception stripe-php | Nơi gọi cũ chỉ đọc `success` — phải kiểm không có nơi gọi nào vỡ |
| 3 | `createDataInvoice` | Nay trả về trạng thái (trước đó void) | Nơi gọi cũ không dùng giá trị trả về — kiểm không phá vỡ |
| 4 | `sendActionOrderItem` | Bộ đếm `count_action_contract`/`count_action_purchase_1st/2st` không còn cộng tay sau khi gọi hàm này (hàm tự cộng đủ) | Tránh cộng đôi action — đã check 3 nơi gọi (webhook, trang mua Stripe, trang mua UnivaPay) |
| 5 | `CalendarCourseBookingService`, `CalendarSalonLineBookingService`, `EventBookingService` (handler đặt lịch Event/Lesson/Salon) | Thêm cờ `stripe_claimed`, giành quyền chốt, báo Chatwork | Dùng chung với UnivaPay — cờ chỉ có tác dụng với Stripe, UnivaPay giữ guard cũ |
| 6 | `addItemSalesStats` / `addMonthlyItemStats` (helper thống kê) | Khoá dòng `s_items`/`s_monthly_item`, cộng nguyên tử `col = col + n` | Dùng ở 4 lối chốt (webhook, trình duyệt mua Stripe, đổi thẻ trình duyệt, `callbackChangeCard`) — tránh trùng/mất khi chốt song song |
| 7 | `getOrderTimeout` / `getBookingTimeout` (cron `recover:payment_univapay_timeout`) | PaymentIntent Stripe thành công đi qua job giành quyền chốt qua queue, không gọi handler trực tiếp | Tránh chốt trùng với webhook/trình duyệt đến gần như đồng thời |
| 8 | `LinkPaymentController`, `SalesManagementV2Controller` (liên kết/huỷ liên kết Stripe) | Huỷ liên kết đặt `stripe_status_webhook_test/live` về NULL; KHÔNG gọi Stripe tạo/xoá endpoint (v5 D-24) | 2 lối vào liên kết + 2 lối vào huỷ liên kết đều phải đồng bộ |
| 10 | `sendActionOrderItem` (helper action bill item — **74 chỗ gọi**, mọi lối bill item Stripe/UnivaPay, job thu định kỳ / nhắc dùng thử) | v17: chỉ +1 bộ đếm `count_action_*` khi action thật sự chạy; bỏ cộng tay sau khi gọi ở các lối chốt Stripe + trang mua UnivaPay + `HandleBillStripe` | Dev **chưa kê danh sách 74 nơi gọi**; lối huỷ hợp đồng / thu lỗi / mở trang vẫn còn cộng tay (+2, có từ base — ngoài phạm vi) |
| 11 | `MobileNotifyService::insertNotifyItem` | v17: insert lỗi trả `false` ⇒ nơi gọi bill item/booking gửi Chatwork chốt dở; các nơi gọi khác bỏ qua giá trị trả về | Hàm thông báo app LME dùng chung (form, đặt lịch không thu tiền…) |
| 12 | `changeCardUnivapay` (trang đổi thẻ UnivaPay, bot không dùng webhook) | v18: cộng `total_money`, doanh thu item, `s_monthly_item` theo đơn giá × số lượng, tạo dòng tháng khi thiếu; v19 D-99: hợp đồng `status_trial = 1` không cộng doanh thu | Lỗi có từ trước ticket (#46088 / #5905) |
| 13 | `HandleBillStripe` (J1) · `HandleSendActionTrialV2` (J2) · `HandleWebhookUnivapay::callbackJob` · `WebhookUnivapayControler` | J1 bỏ cộng tay bộ đếm action; J2 + callbackJob thu thành công cộng `s_monthly_item` `m_payment(_test)` +1, `m_sales(_test)` + số tiền; webhook UnivaPay bỏ khoá nội bộ `stripe_claimed` / `from_job` | Job thu định kỳ 07:00 của cả 2 cổng + webhook UnivaPay |
| 9 | `failStripeItemClaim` (helper Chatwork) | Trả về đã gửi tin hay chưa | v19 — nơi gọi (trang mua, webhook bill item/Event/Lesson, trang đặt Salon) dựa vào giá trị này để không gửi thêm tin lỗi chung |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `StripeItemWebhookController` — `POST /stripe/item-webhook` | `app/Http/Controllers/StripeItemWebhookController.php` | Direct (mới) | Endpoint Connect chung, verify bằng cách gọi lại Stripe lấy PaymentIntent, không dùng chữ ký |
| F2 | `HandleStripeItemWebhook` (queue job) | `app/Jobs/HandleStripeItemWebhook.php` | Direct (mới) | Chốt đơn/booking ngay từ webhook |
| F3 | `StripeFinalizeClaim` / `StripeCronIntentResolver` (giành quyền chốt dùng chung) | `app/Services/StripeWebhook/*.php` | Direct (mới) | Lõi UPDATE có điều kiện — trình duyệt, webhook, cron đều gọi |
| F4 | `StripeBookingFinalizeService` | `app/Services/StripeWebhook/StripeBookingFinalizeService.php` | Direct (mới) | Chốt Stripe cho Event/Lesson/Salon |
| F5 | `SalesService::handleOrderCallback` / `callbackChangeCard` | `app/Services/Sales/SalesService.php` (+786/+1166 dòng qua các bản) | **Direct — dùng chung UnivaPay** | Rủi ro regression cao nhất, đã sửa 4+ lỗi qua nhiều bản |
| F6 | `StripePayment::retrievePaymentIntent` | `app/Helpers/StripePayment.php` | Direct | 7 nơi gọi phải kiểm shape response mới |
| F7 | `RecoverStripeItemWebhook` (console command) | `app/Console/Commands/RecoverStripeItemWebhook.php` | Direct (mới) | Phải chạy sau mọi lần deploy |
| F8 | `SalesStripePaymentController` (trang mua / đổi thẻ bill item) | `app/Http/Controllers/Basic/SalesStripePaymentController.php` | Direct | Thêm bước giành quyền chốt + chặn thu trùng 60 phút |
| F9 | `SalesManagementV2Controller`, `LinkPaymentController` (liên kết/huỷ liên kết) | `app/Http/Controllers/Basic/*.php` | Direct | Huỷ liên kết đặt `stripe_status_webhook_test/live` = NULL; KHÔNG quản lý endpoint Connect (v5) |
| F10 | `MobileEventBookingController`, `CalendarController`, `CalendarSalonController` (app LME di động — đặt/đổi lịch) | `app/Http/Controllers/{Basic,Mobile}/*.php` | Direct | Giành quyền chốt ở 4 endpoint đặt lịch |
| F11 | `CalendarCourseBookingService`, `CalendarSalonLineBookingService`, `EventBookingService` | `app/Services/{Calendar,EventBooking}/*.php` | Direct | Cờ `stripe_claimed`, đếm lại slot khi thua quyền chốt (Event 3DS) |
| F12 | `addItemSalesStats` / `addMonthlyItemStats` | (helper dùng chung, trong `SalesService` hoặc service thống kê) | Indirect (bị sửa logic khoá) | Dùng ở 4 lối chốt |
| F13 | `getOrderTimeout` / `getBookingTimeout` (cron `recover:payment_univapay_timeout`) | (Console command cron) | Direct | Stripe thành công đi qua job giành quyền chốt |
| F14 | `failStripeItemClaim` | `app/Services/StripeWebhook/*.php` (helper Chatwork) | Direct (v19) | Trả về đã-gửi-hay-chưa để chặn gửi trùng tin Chatwork |
| F15 | `VerifyCsrfToken` middleware | `app/Http/Middleware/VerifyCsrfToken.php` | Direct | Thêm `/stripe/item-webhook` vào danh sách miễn CSRF |
| F16 | `sendActionOrderItem` (74 chỗ gọi) | helper bill item (Dev không ghi file) | **Direct — dùng chung** | v17: bộ đếm action chỉ +1 khi action chạy |
| F17 | `MobileNotifyService::insertNotifyItem` | `app/Services/Notify/MobileNotifyService.php` | Direct — dùng chung | Insert lỗi trả `false` |
| F18 | `changeCardUnivapay` | `SalesManagementV2Controller` | Direct | v18 × số lượng; v19 bỏ cộng khi `status_trial = 1` |
| F19 | `HandleBillStripe` (J1) / `HandleSendActionTrialV2` (J2) | `app/Console/Commands/*.php` | Direct | Job thu định kỳ 07:00 — bộ đếm action, `s_monthly_item` |
| F20 | `HandleWebhookUnivapay::callbackJob` / `WebhookUnivapayControler` | `app/Jobs/`, `app/Http/Controllers/` | Direct | Thống kê tháng khi thu định kỳ UnivaPay qua webhook; bỏ khoá nội bộ `stripe_claimed` / `from_job` |

### 4.2. List data bị update

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `s_monthly_item` (dòng thống kê tháng theo item) | UPDATE (cộng nguyên tử có khoá dòng) | 4 lối: webhook, trình duyệt mua Stripe, đổi thẻ trình duyệt, `callbackChangeCard` UnivaPay. ⚠️ Dữ liệu cũ đã có **~3.101 dòng trùng** (2.339 nhóm item/tháng) từ trước fix — Dev nói rõ **không recover trong ticket này** |
| D2 | `s_items` (sum_sales, current_month_sales, number_register, doanh thu) | UPDATE | Vẫn đọc-rồi-ghi (chưa chuyển atomic) — review R-5 chưa sửa, có thể mất 1 lần cộng khi chốt song song |
| D3 | `bot_line_user_items.total_money` | UPDATE | Đổi thẻ tính theo số lượng (quantity × đơn giá) |
| D4 | `s_strip_bot.stripe_status_webhook_test` / `stripe_status_webhook_live` | UPDATE | Ghi bởi lệnh recover; NULL khi huỷ liên kết Stripe |
| D5 | `b_slot`, `b_plan_slot` (slot/plan Event booking) | UPDATE | Đếm lại khi trình duyệt thua quyền chốt (đổi lịch 3DS) |
| D6 | Queue `database` / connection `default` | CREATE (job mới) | `HandleStripeItemWebhook` — cần worker chạy và được restart sau deploy |
| D7 | `config/services.php` — `services.item_stripe_webhook` | UPDATE (config mới) | Đọc `ITEM_STRIP_SECRET_TEST_KEY`, `ITEM_STRIP_SECRET_LIVE_KEY`, `DOMAIN_WEBHOOK_UNIVAPAY_BILL` |
| D8 | ENV `ITEM_STRIP_WEBHOOK_SECRET_TEST/LIVE` | DELETE (nếu đã điền ở v1/v2) | Không còn dùng — môi trường nào đã điền cần xoá |
| D9 | `routes/web.php` | CREATE (route mới) | `POST /stripe/item-webhook` + ngoại lệ CSRF |
| D10 | Cache key `stripe_item_webhook_*`, `stripe_notify_fail_*` | CREATE/UPDATE | Dùng cho giành quyền chốt + chống lặp Chatwork |
| D11 | `o_strip_charge_id` (đơn bill item) | Đọc đối chiếu (không chốt nếu NULL + charge_id client gửi tuỳ ý) | Bảo mật — tránh client tự gửi charge_id giả |
| D12 | `count_action_*` trên item (`count_action_contract`, `count_action_purchase_1st/2st`, `count_action_contract_trial`…) | UPDATE | v5 D-32 / v8 D-49 / v17: bỏ cộng đôi, chỉ +1 khi action chạy |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Bill item — mua qua Stripe** (`/ajax/payment-credit-card-item-v2`) | F5, F8, D1, D2, D3, D6 | High |
| T2 | **Bill item — đổi thẻ qua Stripe** (`/ajax/change-card-item/v2`) | F5, F6, F8, D1, D3 | High |
| T3 | **Bill item — mua/đổi thẻ qua UnivaPay** (hồi quy, dùng chung handler) | F5, F12, D1, D2, D3 | **High** — không đổi UI nhưng logic chốt dùng chung đã sửa nhiều lần |
| T4 | **Webhook Stripe Connect** `/stripe/item-webhook` | F1, F2, F3, F15, D9 | High (mới hoàn toàn, chưa test runtime với Stripe thật) |
| T5 | **Lệnh `recover:stripe_item_webhook`** | F7, D4 | Medium — vận hành, cần test trên staging trước prod |
| T6 | **Cron `recover:payment_univapay_timeout`** (bill item + 3 luồng đặt lịch) | F13, F3 | High — đổi từ gọi handler trực tiếp sang qua job giành quyền chốt |
| T7 | **Màn liên kết / huỷ liên kết thanh toán Stripe** (SCR-PSI-03, SCR-PSI-01, tab 各種設定) | F9, D4 | Medium |
| T8 | **Booking Event** (đặt mới, đổi lịch, đặc biệt có 3DS) | F4, F10, F11, D5 | High — slot/plan đếm lại khi thua quyền chốt là điểm vừa fix (v7) |
| T9 | **Booking Lesson** | F4, F10, F11 | Medium-High |
| T10 | **Booking Salon** | F4, F10, F11 | Medium-High |
| T11 | **Thông báo Chatwork vận hành** (chốt dở, thiếu dữ liệu, lỗi khoá, sự cố sau giành quyền) | F3, F14, D10 | Medium — v19 đổi điều kiện gửi, có thể làm phòng Chatwork nhận ít tin hơn cho case đã có tin "chốt dở" |
| T12 | **Bộ đếm action hợp đồng** (`count_action_contract`, `count_action_purchase_1st/2st`) | F5, F16, D12 | Medium — đã sửa lỗi cộng đôi 2 lần (v5 D-32, v8 D-49) + v17 |
| T13 | **Job thu định kỳ 07:00** (Stripe J1 / UnivaPay J2) + webhook UnivaPay `callbackJob` | F19, F20, D1, D12 | High — chạy trong queue worker, không restart thì vẫn chạy code cũ |
| T14 | **Thông báo app LME** (thông báo 商品販売 / đặt lịch; hàm dùng chung với form, đặt lịch không thu tiền) | F17 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

## Input thiếu

- Redmine #42781 **KHÔNG có section "Link TCs"** → file `04-tc-list.md` lấy theo fallback BƯỚC 6b: **MCP LME TEST STUDIO** task #527 (213 TC, xem digest đầu file 04). Tất cả 213 TC mới chạy ở **env `local`** — 0 TC ở `dev`/`staging`/`prd` ⇒ vi phạm RULE-08, cần Leader quyết định có chặn release khi chưa test runtime với Stripe/UnivaPay thật không.
- 31/213 TC chưa có kết luận (`skip`/`blocked`) — xem danh sách trong `04-tc-list.md`.
- 13 mã quan điểm Studio dùng (`JOB-002`, `OBS-001`, `SEC-INJECT-001`, `API-001`, `TOOL-OLDREC-001`, `TOOL-NEGCTRL-001`, `RULE-TOOL-028`, `TOOL-KNOW-004`, `TOOL-ERRHYG-001`, `TOOL-KNOW-002`, `RULE-05`, `RULE-06`, `RULE-TOOL-029`) **không có trong `framework/checklist-lme.md`** → `/review-tc` sẽ không map được coverage cho 28 TC gắn các mã này.
