# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #43562 qua `/new-task` (2026-10-23).

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43562 — [20-10-2026][32404][Booking Event] Khách đặt thanh toán trước cho đặt chỗ sự kiện: sau khi nhập mã xác thực thẻ báo 'chỉ được đặt 1 lần', không gửi tin nhắn hoàn tất dù đã bị trừ tiền và vào danh sách tham gia.` |
| Module / Màn hình | `Booking Event — LIFF đặt chỗ sự kiện (イベント予約), thanh toán trước qua Stripe (事前決済) có xác thực 3DS` |

## Mô tả bug (bản dịch tiếng Việt)

User: dezawa@moneygo.jp
Bot Name: ながの結婚相談所シアワセロード

Tôi đã cài đặt thanh toán trước khi đặt chỗ sự kiện (イベント予約の事前決済).
Hành vi lúc thanh toán bị lỗi, gây trở ngại cho việc đăng ký.
Xin hãy cải thiện gấp.

Lưu ý: thanh toán thử (テスト決済) thì hành vi không có vấn đề.

Khi khách hàng của chúng tôi bắt đầu đăng ký thì có nhiều khách hỏi, nên xin sửa gấp.
Trong tình trạng này không thể mở lại (再開出来ません).

## Steps to reproduce

1. Cài đặt Booking Event với thanh toán trước qua Stripe (duyệt tự động) và giới hạn số lần đặt là 「このイベントで1度のみ予約可能」(chỉ được đặt chỗ 1 lần duy nhất tại sự kiện này).
2. Friend (line user) **chưa từng đặt chỗ sự kiện này** vào LIFF đặt chỗ, nhập thông tin thẻ tín dụng.
3. Vì khoản thanh toán trên 1 vạn yên (10,000 yên) nên hệ thống yêu cầu nhập mã xác thực của công ty thẻ (3D Secure / 3DS).
4. Nhập mã xác thực 3DS xong, nhấn COMPLETE (hoàn tất xác thực).

## Expected result

- Đặt chỗ hoàn tất ngay sau khi xác thực 3DS thành công, chuyển sang trang/tin kết thúc theo đúng cài đặt (chat / URL / văn bản).
- Tin nhắn hoàn tất đặt chỗ (đã cài đặt gửi sau khi thanh toán xong) được gửi ngay.
- Có đúng 1 booking trong danh sách người tham gia, đã thanh toán (status_payment = đã thanh toán).

## Actual result

- Hiển thị thông báo lỗi 「このイベントの予約は1回のみです」 (chỉ được đặt chỗ 1 lần) và quay lại màn hình nhập thông tin thẻ với dữ liệu đã bị xóa — dù đây là **lần đặt chỗ đầu tiên** của friend này.
- Tin nhắn hoàn tất đặt chỗ đã cài đặt **không được gửi ngay** (theo Dev: thực tế gửi trễ 15–20 phút, do job `recover:payment_univapay_timeout` chốt đơn thay).
- Tuy nhiên thanh toán vẫn được thực hiện (tiền đã bị trừ) và friend đã có trong danh sách người tham gia.
- Khách không thể mở lại màn hình đặt chỗ ở trạng thái lỗi này để thử lại bình thường.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [x] Có video
- [ ] Có log / request-response

<!-- Redmine issue.attachments = 0 (không có file đính kèm trực tiếp). Video khách gửi qua LINE, link được Support dán lại ở Journal #146190: -->
- https://go.lmes.jp/msg_template/line-user/media-step/218/video/video_1143559_637095241791045854_1792569664136.mp4

## Ghi chú thêm của Leader

- Môi trường phát hiện: **Production** — khách hàng thật, bot `ながの結婚相談所シアワセロード`.
- Trạng thái Redmine tại thời điểm fetch: **Fix done - Đợi test** (branch `ai_studio_fixbug_43562`, nhánh gốc `release_step_20260930_v2`).
- Tái hiện theo Dev: xảy ra khi đủ **cả 3 điều kiện** — sự kiện thu tiền trước qua Stripe + duyệt tự động + giới hạn "1 lần" (`このイベントで1度のみ` / `各予約枠で1度のみ` / từng khung `1回のみ`) + thẻ cần xác thực 3DS. Thanh toán test (テスト決済, không cần 3DS) thì **không** gặp lỗi.
- Khách hàng bị ảnh hưởng theo Journal #146189: chính người báo, anh/chị Arai (`m.arai.kakehashi@gmail.com`), anh/chị Umemoto. Khóa học liên quan: `【男性早割申込み】5000円OFF！`. Sự kiện đã đặt: `【男性】12/27アマンダンスカイ`.
- Dev handoff (Journal #146733) ghi các booking liên quan trên production: `949863`, `949949` (thành công, hợp lệ), `950193` (friend `40770053`, event `42139` — đã huỷ nhưng `status_payment` vẫn = 1, **CS cần xác nhận đã hoàn tiền cho khách chưa** — nằm ngoài phạm vi code fix).
- Dev lưu ý: **không cần recover data** — các booking thành công trên production đã được job timeout chốt đúng (chỉ trễ ~15–20 phút), booking thừa do khách thử lại đã bị huỷ và hoàn tiền tay.
- Issue phụ (Dev nêu, **ngoài phạm vi task** #43562): lần gọi lại sau 3DS hiện tin tưởng cờ `alreadyPayment` do client gửi mà không retrieve lại PaymentIntent thật từ Stripe để xác nhận `succeeded` — rủi ro bảo mật thanh toán, Dev đề nghị tách ticket riêng.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — tra theo tên bot "ながの結婚相談所シアワセロード">` |
| Friend | Người báo: `dezawa@moneygo.jp`; liên quan: `m.arai.kakehashi@gmail.com` (Arai), anh/chị Umemoto; friend `40770053` (booking 950193) |
| Đối tượng cấu hình | Sự kiện `【男性】12/27アマンダンスカイ` (event_id `42139` theo booking 950193); khóa học `【男性早割申込み】5000円OFF！`; cài đặt giới hạn `このイベントで1度のみ予約可能` |
| Thời điểm lỗi | `2026/10/20 17:08:00` |
| Đối chứng | Thanh toán test (テスト決済, không cần 3DS) không gặp lỗi — dùng làm case so sánh. Booking production liên quan: `949863`, `949949` (thành công), `950193` (đã huỷ, status_payment vẫn 1) |

## Journal / note từ Redmine (nguyên văn)

**Journal #145808 — Ngô Thúy Ngần — 2026-10-20:**

```
User: m.arai.kakehashi@gmail.com
```

**Journal #146189 — AI bug detect Lme — 2026-10-21:**

```
Comment slack ngày 2026-10-21 17:00:16

お客様
Những friend bị lỗi là tôi, anh/chị Arai và anh/chị Umemoto.

Khóa học liên quan là 【男性早割申込み】5000円OFF！

Sự kiện đã đặt là 【男性】12/27アマンダンスカイ

Trong phần liên hệ tôi đã viết là không nhận được tin nhắn hoàn tất đặt chỗ (sau thanh toán), nhưng sau 15〜20 phút tin nhắn đã cài đặt đã được gửi đến.

Như một cách khắc phục tạm, tôi đã thử hiển thị bằng văn bản thay vì quay lại màn hình chat sau thanh toán, nhưng màn hình văn bản không hiển thị và quay lại màn hình nhập thông tin thẻ.

Video quay màn hình ở đây↓
```

**Journal #146733 — Dev Studio — 2026-10-22:**

```
Dev handoff — 22/10 11:32 · nhánh ai_studio_fixbug_43562

Nguyên nhân:
Với sự kiện thu tiền trước qua Stripe (duyệt tự động), khi thẻ cần 3DS thì màn LIFF gọi API thanh toán 2 lần. Lần 1 server tạo sẵn booking (予約完了, chưa thanh toán) rồi trả về để trình duyệt hiện 3DS. Lần 2, sau khi khách nhập mã, gọi lại để chốt đơn. Bước chặn "chỉ được đặt 1 lần" trong `MobileEventBookingController::payment` chạy lại ở lần 2 mà không loại trừ booking của chính lần thanh toán này, nên tìm thấy booking vừa tạo và trả 「このイベントの予約は一回のみです。」. Đơn vì vậy không được chốt ngay; job `recover:payment_univapay_timeout` chốt đơn và gửi tin hoàn tất trễ 15–20 phút.

Nội dung thay đổi:
- LIFF đặt chỗ sự kiện (thanh toán trước bằng Stripe, duyệt tự động, thẻ 3DS, cài 「このイベントで1度のみ」, 「各予約枠で1度のみ」 hoặc từng khung 「1回のみ」): sau khi nhập mã 3DS, đặt chỗ hoàn tất ngay, không còn alert 「このイベントの予約は一回のみです。」, không quay lại màn nhập thẻ.
- Tin hoàn tất đặt chỗ, nhắc lịch và thông báo được gửi ngay sau khi thanh toán 3DS, thay vì trễ 15–20 phút.
- Friend đã có booking khác (chưa huỷ) của sự kiện/khung đó vẫn bị chặn với message như cũ.

File đã sửa (php-web):
  .../Basic/MobileEventBookingController.php         |  39 ++-
  .../Feature/MobileEventBookingPaymentOnceTest.php  | 284 +++++++++++++++++++++
  2 files changed, 320 insertions(+), 3 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi chỉ nới bước chặn cho đúng 1 booking khớp đủ 5 điều kiện ở lần gọi lại Stripe, có test và kiểm chứng ngược. Chưa thử runtime với Stripe thật.
- API /ajax/booking-event/payment (lần gọi 1 và lần gọi lại sau 3DS): chỉ thêm điều kiện loại trừ ở bước kiểm số lần đặt. Univapay, sự kiện cần duyệt và lần gọi 1 không đi qua điều kiện mới.
- Bước chốt đơn của lần gọi lại (cập nhật booking, ghi friend info, nhắc lịch, gửi tin hoàn tất, thông báo app, affiliate) giờ chạy cả cho sự kiện 「1度のみ」. Đây là cùng đường code đang chạy cho sự kiện 「何度でも」.
- Bảng b_user_booking: chỉ thêm 1 câu đọc theo id, không ghi mới.
- Job recover:payment_univapay_timeout: ca 3DS thành công được chốt ngay (status_webhook=1) nên job không xử lý lại. Cần kiểm không bị gửi tin hoàn tất 2 lần.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Dữ liệu production cho thấy các booking thành công đã được job timeout chốt (đã thu tiền, đã gửi tin hoàn tất, chỉ trễ khoảng 18 phút). Các booking thừa do khách thử lại đã được huỷ và phần lớn đã hoàn tiền bằng tay. Không có booking kẹt ở trạng thái chờ.

Việc cần người làm thêm (ngoài phạm vi task):
- CS kiểm tra booking 950193 (friend 40770053, sự kiện 42139): đã huỷ nhưng status_payment vẫn là 1 (chưa ghi nhận hoàn tiền), cần xác nhận khách đã được hoàn tiền chưa.
- CS báo khách: 2 booking thành công (949863, 949949) hợp lệ; các lần thử lại đã được huỷ/hoàn tiền; lỗi sẽ được sửa ở release tới. Trong lúc chờ có thể tạm đổi cài đặt số lần đặt sang 「何度でも」 nếu khách chấp nhận.
- Bộ test PHPUnit trên base đang hỏng: tests/Feature/ContractExpireServiceTest.php báo PHP Fatal vì class giả thiếu các method mới của BotRepositoryInterface, kèm vài test lỗi sẵn như BillingServiceTest. Cần sửa ở một ticket riêng.
- Việc riêng về bảo mật thanh toán: ở lần gọi lại sau 3DS của thanh toán Stripe (đặt chỗ sự kiện), server nên tra lại PaymentIntent và chỉ chốt đơn khi trạng thái là succeeded, thay vì tin cờ alreadyPayment do client gửi.

Điểm cần test:
- Stripe test, duyệt tự động, 「このイベントで1度のみ」, thẻ 3DS 4000 0027 6000 3184, friend chưa từng đặt: hoàn tất 3DS ⇒ đặt thành công ngay, không có alert, tin hoàn tất đến ngay, trang kết thúc đúng cài đặt (chat/URL/text); DB chỉ 1 booking với status_payment=1, status_webhook=1.
- Lặp lại với 「各予約枠で1度のみ」 và với cài theo từng khung 「1回のみ可能」.
- Friend đã có booking chưa huỷ của sự kiện/khung đó, đặt lại bằng thẻ 3DS: bị chặn ở lần 1 với đúng message, không hiện 3DS, không tạo booking, không thu tiền.
- Thẻ không cần 3DS (4242…): đặt bình thường như cũ.
- Huỷ hoặc làm thất bại 3DS: booking chờ bị xoá như cũ, đặt lại được.
- Univapay, sự kiện cần duyệt, cài 「何度でも」: hành vi không đổi.
- Sau ca 3DS thành công, đợi qua 20 phút: job timeout không gửi lại tin hoàn tất lần 2.
- Gửi tay request alreadyPayment=true kèm bookingId/chargeId của booking cũ đã thanh toán (hoặc PaymentIntent khác): vẫn bị chặn.

Branch: ai_studio_fixbug_43562
- sns-line: ai_studio_fixbug_43562 (nhánh gốc release_step_20260930_v2 @d6c0a2653f63, commit 27ca043b44cf054b6b18a43fa9d8969cf6359977)
```

**Journal #147648 — Thanh Phương — 2026-10-23:**

```
Thao tác tái hiện:
1. Booking event có cài đặt thanh toán stripe và cài đặt giời hạn cho user booking là このイベントで1度のみ予約可能 (Chỉ có thể đặt chỗ một lần duy nhất tại sự kiện này)
2. Line user vào book nhập card 3DS -> Ở màn xác thực nhấn COMPLETE
3. Hiện tượng: màn hình bị hiện thông báo このイベントの予約は1回のみです
```
