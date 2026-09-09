# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37396 — [10-06-2026][11200][QR Landing] QR code action (QRコードアクション)「保留：アルコールset*1m」 không hiển thị nút Spreadsheet` |
| Redmine URL | https://redmine.watermelon.vn/issues/37396 |
| Auto-filled | `2026-06-13 by /new-task` |
| Ngày báo cáo | `2026-06-11` |
| Khách hàng / PM báo | `AI LME CSS` (User: mooriniwt@gmail.com) |
| Module / Màn hình | `QR Landing` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — Bug KH, nhiều khả năng Production (step.lme.jp)>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: mooriniwt@gmail.com
Bot Name: メディトク　byみかげ調剤薬局

Trong QR code action (QRコードアクション)「保留：アルコールset*1m」, nút Spreadsheet (スプレッドシートボタン) không được hiển thị.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B9GM49PHT

---

原文 (JP)
QRコードアクション「保留：アルコールset*1m」にスプレッドシートボタンが表示されていない。
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- ⚠️ Bug KH chưa tái hiện được — không có steps. Xem Ghi chú Leader. -->

1.
2.
3.

## Expected result

- Nút/icon Spreadsheet (スプレッドシートボタン) hiển thị trong QR code action.

## Actual result

- Nút/icon Spreadsheet (スプレッドシートボタン) KHÔNG hiển thị.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachment:
- SnapCrab_NoName_2026-6-10_20-39-45_No-00.png — https://redmine.watermelon.vn/attachments/download/26645/SnapCrab_NoName_2026-6-10_20-39-45_No-00.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine (journal Kim Cúc 2026-06-12: "Tái hiện case KH: chưa tái hiện được => chưa tìm ra được nguyên nhân") — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03): khi tạo landing bị missing `google_sheet_id`. TCs nên tập trung verify cách fix (job tự tạo sheet + insert data cho landing thiếu `google_sheet_id`) + regression impact, KHÔNG cố reproduce flow KH.
