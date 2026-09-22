# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40598 — [07-09-2026] [TY-12081] [QR Landing] Hỏi vì sao URL/preview khác nhau giữa test send và tap richmenu (QR referral)` |
| Module / Màn hình | QRコードアクション (QR Code Action) — 紹介時アクション (action khi giới thiệu) · メッセージテンプレート (Message Template) — テスト送信 (gửi thử) · リッチメニュー (rich menu) — action gửi template |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ — khách hàng hỏi) — 管理番号 (số quản lý) TY-12081.

| Mục | Giá trị |
|---|---|
| 管理No (Số quản lý) | TY-12081 |
| アドレス (Địa chỉ) | haru@clinique-haru-osaka.com |
| LOA名 (Tên LOA) | クリニーク ハル 京都 |
| 担当 (Phụ trách) | 沖原 |
| ツール (Công cụ) | リンク (Link) |

**問い合わせ内容 (Nội dung yêu cầu):**

Tôi đang lưu mã giới thiệu (紹介コード) của 「紹介時アクション」 trong QRコードアクション (action mã QR) vào template. Trong trường hợp này, khi gửi template bằng テスト送信 (test send) và khi gửi bằng action lúc tap リッチメニュー (rich menu), URL được chuyển đổi và text プレビュー (preview) lại khác nhau, không biết vì sao ạ.

**Link tham chiếu:**
- Slack thread: https://l-message.slack.com/archives/C0BALS7S73L/p1788738334107349?thread_ts=1788738334.107349&cid=C0BALS7S73L
- Slack list record: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C0T26U74G
- Dashboard CSS analytics: https://dashboard.melonglobal.net/css-analytics/?id=T12081

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — khách chỉ mô tả hiện tượng, không đưa bước tái hiện chuẩn. -->

## Expected result

<!-- Không có trong Redmine. -->

## Actual result

<!-- Không có trong Redmine. -->

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.jpg — https://redmine.watermelon.vn/attachments/download/30024/screenshot1.jpg
- 3fd200b61c34084fe718379fadc21998.png — https://redmine.watermelon.vn/attachments/download/30025/3fd200b61c34084fe718379fadc21998.png
- SnapCrab_NoName_2026-9-7_8-42-33_No-00.png — https://redmine.watermelon.vn/attachments/download/30026/SnapCrab_NoName_2026-9-7_8-42-33_No-00.png

(3 ảnh do khách gửi kèm trong thread Slack — journal #134671 / #134672 ghi "Khách gửi ảnh — xem đính kèm".)

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — ticket là 問い合わせ (câu hỏi của khách), không có Steps/Expected/Actual. Root cause đã được Dev (AI auto-fixbug) confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.
- **Tracker = Support**, không phải Bug. Status Redmine hiện tại: `New`. Assignee: Ngô Thúy Ngần.
- **Điều kiện tiên quyết để dựng env test:**
  - Bot phải có 1 QRコードアクション đang hoạt động, có cấu hình 紹介時アクション → lấy được mã giới thiệu `[LANDING_INTRO_<mã QR>]`.
  - Template text chứa mã `[LANDING_INTRO_xxx]` đó.
  - 1 rich menu gắn action gửi đúng template trên.
  - Tài khoản LINE tester **là bạn của bot** và **đã có mã định danh (u_code)**.
  - ⚠️ **Cùng 1 người nhận** cho cả 2 đường (test send + tap rich menu) — u_code khác nhau theo từng người nhận, khác người nhận thì URL khác nhau là **đúng thiết kế**.
- **Feature flag / cấu hình ảnh hưởng trực tiếp kết quả đọc:**
  - Cờ rút gọn URL cấp **bot** (`is_shorten_url`) BẬT/TẮT.
  - Cờ rút gọn URL cấp **template** BẬT/TẮT.
  - Bot có/không cấu hình **miền rút gọn riêng** (custom short domain).
  - Biến môi trường **BASE_URL** — Dev xác nhận 2026-09-09 môi trường thật CÓ khai báo. Nếu env test thiếu BASE_URL thì nhánh chặn rút gọn theo miền hệ thống không có hiệu lực → kết quả đọc sẽ sai vì lý do cấu hình, không phải lỗi sản phẩm.
- **Môi trường cần có tiến trình job** (linect-service Java) để chạy được đường tap rich menu. Thiếu job → không kiểm được vế đối chiếu, KHÔNG suy đoán kết quả phía job.
- **Tần suất lỗi:** không ghi trong ticket — theo mô tả của Dev thì là khác biệt hành vi **luôn xảy ra** giữa 2 đường gửi (web PHP vs job Java), không phải lỗi xác suất.
- 🔴 **Điểm cần chốt trước khi close:** khách hỏi về **CẢ HAI** thứ — (a) URL chuyển đổi khác nhau, (b) **text preview khác nhau**. Theo root cause mục (c) của Dev, phía job **không ghi** cặp thay thế của mã giới thiệu vào bảng thay thế của tin nhắn nên màn xem lại vẫn hiện nguyên chuỗi mã. Bản fix hiện tại **chỉ chạm web/PHP** (3 file), **KHÔNG chạm linect-service Java** → phần (b) preview có khả năng **chưa được fix**.
- 🔴 **Cần PM xác nhận:** sau fix, khi BASE_URL có giá trị (môi trường thật có) thì **MỌI URL trỏ về miền hệ thống thôi được rút gọn** → mất số liệu lượt bấm của những link đó. Hệ thống đã chạy nhiều năm với chốt chặn này không hoạt động → đây là thay đổi hành vi quan sát được trên production.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa có trong ticket — cần hỏi CS/Dev>` |
| LOA / khách hàng | クリニーク ハル 京都 — haru@clinique-haru-osaka.com |
| Friend | `<chưa có trong ticket>` |
| Đối tượng cấu hình | QRコードアクション có 紹介時アクション + template lưu mã giới thiệu + rich menu gắn action gửi template — `<chưa có ID cụ thể trong ticket>` |
| Thời điểm lỗi | 2026-09-07 (ngày khách hỏi trên Slack) |
| Đối chứng | Đường tap rich menu (job Java) = kết quả khách coi là ĐÚNG; đường test send (web PHP) = kết quả khác |
| 管理No (số quản lý CS) | TY-12081 |
