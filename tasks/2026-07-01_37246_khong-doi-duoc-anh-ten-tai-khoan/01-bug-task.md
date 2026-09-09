# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37246 — [08-06-2026][No.11161][Add bot/Setting bot] Không đổi được ảnh & tên tài khoản từ 「LINE公式アカウント表示設定」, hiện message lỗi (ảnh đính kèm)` |
| Redmine URL | https://redmine.watermelon.vn/issues/37246 |
| Auto-filled | `2026-07-01 by /new-task` |
| Ngày báo cáo | `2026-06-08` |
| Khách hàng / PM báo | `AI LME CSS` (author) — end user: creet.ex.office@gmail.com |
| Module / Màn hình | `Add bot/Setting bot` — màn 「LINE公式アカウント表示設定」 |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: creet.ex.office@gmail.com
Bot Name: 【個別返信専用】佐々木誠

Khi thử thay đổi ảnh tài khoản và tên tài khoản từ 「LINE公式アカウント表示設定」, message như trong ảnh đính kèm hiện ra và không thể thay đổi được. KH nhờ cho biết nguyên nhân và cách xử lý.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B8VB1HTNH

---

h3. 原文 (JP)
「LINE公式アカウント表示設定」からアカウント画像とアカウント名を変更しようとすると添付画像のメッセージが表示されて変更できないとのことですので、原因と対処法についてご教示ください。
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
- https://redmine.watermelon.vn/attachments/download/26507/スクリーンショット%202026-06-08%20132915.png
- https://redmine.watermelon.vn/attachments/download/27263/スクリーンショット%202026-06-08%20132915.png (bản duplicate)

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Bug không tái hiện được trong Redmine (không có section "Tái hiện bug" chuẩn với Steps/Expected/Actual) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

**Context từ journal Redmine (tham khảo, KHÔNG phải steps chính thức):**
- Message lỗi hiển thị (journal Ngọc Ánh 2026-06-08): `入力した情報が間違っています。WEBブラウザの自動翻訳機能が原因の可能性がございますので、自動翻訳を無効にした状態でお試しください。` (thông tin nhập sai — nghi do auto-translate của trình duyệt).
- Điều tra sâu (journal 2026-06-11 → 2026-06-22): tài khoản liên kết đã bị **BAN / đóng băng (freeze)** phía LINE. Root cause thực sự: khi đổi ảnh/tên, backend luôn re-validate Channel Secret của Messaging API — nếu secret đang lưu trống/không hợp lệ thì bị chặn. Xem file 03.
