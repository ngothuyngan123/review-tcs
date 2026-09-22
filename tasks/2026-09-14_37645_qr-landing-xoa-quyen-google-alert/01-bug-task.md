# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37645 — [QR landing] Khi đã liên kết google thành công, vào myaccount google để xóa quyền liên kết, vào màn landing chưa hiển thị alert để liên kết lại` |
| Module / Màn hình | QR code action / Landing (FA-017) — màn liên kết Google Spreadsheet của QR code action (`/basic/landing-qr/link-google`, 「スプレッドシート連携」) |

## Mô tả bug (bản dịch tiếng Việt)

Truy cập vào: https://myaccount.google.com/connections?hl=vi&utm_source=OGB&utm_medium=act&gar=WzUwXQ
để xóa liên kết

Bug detect từ bug gốc: Bug KH #37396 [10-06-2026][11200][QR Landing] QR code action (QRコードアクション)「保留：アルコールset*1m」 không hiển thị nút Spreadsheet

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" riêng. Các bước dưới đây bám sát tiêu đề ticket + link thao tác trong description, KHÔNG phải nguyên văn từ khách. -->

1. Liên kết Google Spreadsheet thành công cho QR code action (màn 「スプレッドシート連携」).
2. Vào https://myaccount.google.com/connections → xóa quyền liên kết của ứng dụng.
3. Quay lại màn landing (màn liên kết Google Spreadsheet của QR code action).

## Expected result

- Màn hiển thị alert báo liên kết đã bị gỡ, cho phép liên kết lại.

## Actual result

- Màn chưa hiển thị alert để liên kết lại (vẫn hiện trạng thái đang kết nối như bình thường).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #37645 không có attachment nào. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không có steps/expected/actual dạng chuẩn trong Redmine** — description chỉ có 2 dòng (link trang gỡ quyền Google + nguồn bug gốc). Steps ở trên là suy từ tiêu đề ticket. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03) → TCs nên tập trung verify cách fix + regression impact.
- Tracker Redmine = **Bug tự detect** (không phải bug KH báo trực tiếp). Bug gốc từ khách: **#37396** — `[10-06-2026][11200][QR Landing] QR code action 「保留：アルコールset*1m」 không hiển thị nút Spreadsheet`.
- **Điều kiện tiên quyết để test**: cần tài khoản Google test riêng của QA (không dùng tài khoản khách hàng) + bot test riêng, vì phải thao tác gỡ quyền thật trên trang tài khoản Google.
- Ticket **không ghi môi trường phát hiện** và **không ghi tần suất lỗi**.
- Fix của Dev là **AI auto-fixbug** (branch `ai_fixbug_37645`, đã qua refix vòng 1 theo AI review) — chưa chạy được verify runtime (dev DB/web không kết nối được), mức verify mới chỉ là `lint`.

## Journal / note từ Redmine (nguyên văn)

Redmine #37645 chỉ có **1 journal có notes**: `**Journal #131642 — AI LME Fix bug — 2026-08-21**` — báo cáo AI auto-fixbug (nguyên nhân / cách fix / function đã check / đánh giá ảnh hưởng / verify / branch).

Nội dung journal này **chính là Section "Đánh giá ảnh hưởng"** và đã được chép đầy đủ sang [03-dev-impact.md](03-dev-impact.md) → không lặp lại ở đây.
