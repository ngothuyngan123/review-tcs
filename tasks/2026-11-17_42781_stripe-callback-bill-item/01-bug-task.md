# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42781 — Xử lý callback stripe cho tính năng bill item` |
| Module / Màn hình | Bill item — thanh toán Stripe (mua / đổi thẻ) + webhook callback. Phạm vi mở rộng qua các bản dev-impact: Booking Event / Lesson / Salon (thanh toán Stripe), màn liên kết/huỷ liên kết Stripe (SCR-PSI), lệnh `recover:stripe_item_webhook`, cron `recover:payment_univapay_timeout`. |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Đây **KHÔNG phải bug khách báo** — ticket thuộc tracker "Triển khai ngang" (feature implementation), không có hiện tượng lỗi cụ thể để tái hiện. Nội dung dưới là yêu cầu triển khai nguyên văn từ Redmine (đã là tiếng Việt):

- Tìm hiểu callback của Stripe khi thực hiện bill tiền.
- Khi xử lý bill item bằng phương thức Stripe, thực hiện xử lý callback (webhook).
- Cách recover cho các account Stripe cũ để có thể nhận được callback khi có xử lý bill tiền.

## Steps to reproduce

<!-- Không áp dụng — ticket là yêu cầu triển khai feature, không phải bug tái hiện được. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có file đính kèm. -->

## Ghi chú thêm của Leader

⚠️ **Ticket không tái hiện được vì không phải bug** — đây là task triển khai tính năng mới (Stripe webhook cho bill item + mở rộng sang Event/Lesson/Salon booking), đi qua **19 bản dev-impact (v1 → v19)** trong **28 journal note** từ 2026-10-29 đến 2026-11-17 (nhánh `ai_studio_implement_42781`). Toàn bộ nội dung "Đánh giá ảnh hưởng" đã được tổng hợp sang `03-dev-impact.md` theo **trạng thái cuối cùng (v19, Journal #155445 — 17/11 15:12)** vì các bản sau luôn sửa đè/bổ sung bản trước (không phải 19 thay đổi độc lập). Lịch sử đầy đủ từng version — xem trực tiếp Redmine #42781 (journal #149383 → #155445) khi cần trace.

- Task gắn với **11 bug con Redmine** (#45308, #45309, #45310, #45311, #45312, #45313, #45315, #45316, #45630, #45631, #45632) + nhiều bug automation Test Studio (#5114, #5115, #5117–#5121, #5449–#5451, #46126/#5928) — tất cả đã Dev confirm "đã sửa" trong các journal, kèm commit hash cụ thể.
- Độ phức tạp **cao**: diff cuối cùng chạm **50 file** (`+12762 / -668` dòng), vừa sửa luồng Stripe **vừa chạm 2 handler dùng chung với UnivaPay** (`SalesService::handleOrderCallback`, `callbackChangeCard`) → bắt buộc hồi quy UnivaPay song song với Stripe.
- Rủi ro runtime: **420 test đơn vị pass nhưng v4–v19 CHƯA có lượt test runtime với Stripe/UnivaPay thật** (chỉ test local, 0 TC chạy ở staging/prd theo snapshot Studio ở `04-tc-list.md`) → vi phạm RULE-08 (không kết luận bill tiền từ local/staging).
- Môi trường / config cần chuẩn bị trước khi test: endpoint webhook Connect `<domain>/stripe/item-webhook` phải được tạo trên dashboard Stripe platform qua lệnh `php artisan recover:stripe_item_webhook` (dry-run → staging `--stripe_env=test` → production `--stripe_env=all`); cần có queue worker chạy + `CACHE_DRIVER` dùng chung giữa web và worker (redis/database/memcached); domain phải truy cập được từ Internet.
- **Việc Dev nêu rõ KHÔNG thuộc phạm vi task này** (không đẻ TC cho các mục sau, chỉ note rủi ro regression nếu chạm): dữ liệu `s_monthly_item` trùng cũ (~3.101 dòng) từ trước khi fix, lỗi cũ tên/email/SĐT người mua không được ghi (do `$flagName = 0` phép gán) — ticket riêng, bảo mật code cũ (route `/test-customer` hard-code key test, `access_token` Stripe bị log khi liên kết), bộ đếm `s_items` đọc-rồi-ghi chưa chuyển sang atomic (review R-5), hoàn tác đổi lịch khi 3DS báo lỗi giả (review R-8, code gốc cũng vậy).
- Dev phụ trách thực chất là **AI Dev Studio** (journal author "Dev Studio", branch `ai_studio_implement_42781`) — assignee Redmine là `Thanh Phương` (thanhntp), cũng là người chạy review/test trên Studio (task #527).

## Journal / note từ Redmine (nguyên văn)

> Chỉ chép 2 journal có giá trị nhất để trace nhanh (bản đầu xác định hướng thiết kế + bản cuối là trạng thái final). 26 journal còn lại (v2 → v18, 11 bug fix con) — xem Redmine #42781 hoặc `03-dev-impact.md` (đã tổng hợp).

**Journal #149383 — Dev Studio — 2026-10-29 (bản thiết kế v1 — khởi đầu):**

```
Dev Studio · Nội dung thực hiện

Hiện chưa có webhook Stripe nào. Đơn bill item đã trừ tiền nhưng khách đóng màn thì 15–20 phút sau cron mới chốt. Thiết kế thêm một endpoint webhook Connect ở tài khoản Stripe platform để nhận event mọi tài khoản đã liên kết, nên tài khoản cũ chỉ cần cấu hình một lần, không cần migration. Event thanh toán thành công được xử lý trễ 5 phút như lưới an toàn: chốt các đơn mua lần đầu và đổi thẻ còn chờ bằng đúng handler cron đang dùng. Sau khi bàn giao, cần đăng ký endpoint trên dashboard Stripe và điền 2 khoá ký vào env.

Hướng sửa:
- D-1 Thêm endpoint nhận webhook Stripe cho bill item, verify chữ ký và xếp hàng có độ trễ
- D-2 Thêm queue job HandleStripeItemWebhook gọi SalesService
- D-3 Thêm SalesService::handleStripeItemWebhook chốt đơn còn chờ bằng handler sẵn có
- D-4 Viết hướng dẫn vận hành để tài khoản Stripe cũ nhận được callback

Ảnh hưởng / rủi ro:
Chỉ thêm code mới: endpoint công khai, job queue, một hàm mới trong SalesService. Ngoài ra sửa routes/web.php và danh sách miễn CSRF; không migration, không đổi luồng trình duyệt, thu định kỳ Stripe, cron recover hay UnivaPay. Cần test kỹ phần chốt đơn trùng (đơn đã được trình duyệt chốt thì không chạy lại action), việc đối chiếu tài khoản/livemode, và trường hợp env rỗng thì cron vẫn chốt như cũ.
```

**Journal #155445 — Dev Studio — 2026-11-17 15:12 (Dev handoff cuối — v19, trạng thái hiện tại):**

```
Dev handoff — 17/11 15:12 · nhánh ai_studio_implement_42781

Nguyên nhân:
Khối bắt lỗi của trang mua Stripe gọi `failStripeItemClaim` (gửi tin chốt dở của ticket), rồi vẫn gửi tin lỗi chung có từ trước ticket. Cùng kiểu ở handler webhook bill item, Event, Lesson và trang đặt Salon. Helper không trả về đã gửi hay chưa, nên nơi gọi không biết để bỏ tin thứ hai.

Nội dung thay đổi:
- Endpoint POST /stripe/item-webhook (Connect) và lệnh php artisan recover:stripe_item_webhook: chốt ngay đơn mua / đổi thẻ bill item và lịch Event (đặt mới, đổi lịch), Lesson, Salon.
- Trang mua bill item, trang đổi thẻ, đặt / đổi lịch Event, Lesson, Salon: còn lần thu đang chờ (trong 60 phút) ⇒ chặn, báo 「決済処理を行っていますので、操作できません。」.
- Cron recover:payment_univapay_timeout (Stripe): 3DS bỏ dở quá 15 phút ⇒ huỷ PaymentIntent, dọn dữ liệu, không gửi tin; chỉ lỗi thẻ thật mới gửi 「決済に失敗しました」.
- Job thu định kỳ UnivaPay / callbackJob: thu thành công cộng s_monthly_item (tháng lúc chạy) m_payment(_test) +1, m_sales(_test) + số tiền.
- (v17) Chatwork chốt dở khi tạo thông báo mobile bill item lỗi; bộ đếm action "chỉ 1 lần" chỉ tăng khi action thật sự chạy.
- (v18) Trang đổi thẻ UnivaPay cộng total_money, doanh thu item, thống kê tháng theo đơn giá × số lượng.
- (v19, #46126 / #5928) Một sự cố sau khi đã giành quyền chốt Stripe ⇒ đúng 1 Chatwork, không kèm tin lỗi chung cũ. Áp cho trang mua bill item, webhook mua / đổi thẻ, webhook Event / Lesson / Salon, trang đặt Salon. UnivaPay hoặc lỗi trước khi giành quyền vẫn gửi tin lỗi chung.

(... đầy đủ "Bug QA con", "File đã sửa", "Đánh giá ảnh hưởng", "Migration", "Điểm cần test" — xem 03-dev-impact.md, đã chép đủ)
```
