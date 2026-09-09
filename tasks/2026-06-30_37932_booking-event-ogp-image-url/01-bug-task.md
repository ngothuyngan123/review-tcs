# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37932 — [19-06-2026][No.11303][Booking Event] Hỏi đổi setting ảnh OGP (OGP画像) của URL đặt lịch sự kiện (イベント予約URL) ở đâu` |
| Redmine URL | https://redmine.watermelon.vn/issues/37932 |
| Auto-filled | `2026-06-30 by /new-task` |
| Ngày báo cáo | `2026-06-19` |
| Khách hàng / PM báo | `AI LME CSS` (User: meryabepi@kmail.li — Bot: 田村ハヤト公式アカウント) |
| Module / Màn hình | `Booking Event — URL đặt lịch sự kiện (イベント予約URL) / OGP preview` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `Production — URL công khai chia sẻ qua Facebook / Email / LINE (liff.line.me). Verify fix trên Staging (staging.lme.jp).` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: meryabepi@kmail.li
Bot Name: 田村ハヤト公式アカウント

Có thể đổi setting ảnh OGP (OGP画像) của URL đặt lịch sự kiện (イベント予約URL) ở đâu vậy?

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0BBUMP675F

---

h3. 原文 (JP)
イベント予約URLのOGP画像はどちらで設定変更できますでしょうか？
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments (Redmine):
- スクリーンショット 2026-06-19 180757.png — https://redmine.watermelon.vn/attachments/download/27254/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-06-19%20180757.png
- スクリーンショット 2026-06-19 180757.png — https://redmine.watermelon.vn/attachments/download/27321/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-06-19%20180757.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được qua description (description gốc chỉ là **câu hỏi của KH**, không có steps format chuẩn). Root cause + cách fix đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify cách fix + regression impact.

**Bối cảnh tái hiện thực tế (trích từ journal Redmine — phục vụ tester, KHÔNG phải Steps chuẩn):**
- KH chia sẻ URL đặt lịch sự kiện (イベント予約URL, dạng `liff.line.me/...?booking_event_id=...`) qua **Facebook hoặc Email** → preview hiển thị **sai ảnh** (ảnh American Express — chính là ảnh đính kèm trong email liên hệ ban đầu của KH), thay vì ảnh tiêu đề (ヘッダー画像) của sự kiện.
- KH hỏi nơi cài đặt ảnh OGP riêng. Kết luận: **OGP không có mục cài đặt riêng** — hệ thống tự lấy ảnh tiêu đề / title / content của sự kiện làm OGP.
- Vấn đề kỹ thuật: trang đặt lịch sự kiện **1 ngày** (route `event-booking/index` → `MobileEventBookingController@index` → blade `order/index`) **thiếu thẻ `og:image`** → Facebook tự nhặt ảnh bất kỳ trong HTML / cache → hiển thị sai ảnh.
