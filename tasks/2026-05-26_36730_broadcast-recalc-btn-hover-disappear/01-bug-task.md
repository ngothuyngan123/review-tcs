# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #36730 bởi `/new-task` ngày 2026-05-26. Tester verify lại description + steps + attachment rồi tick checkbox dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | #36730 — [25-05-2026][28274][Broadcast] Tab Đặt lịch phân phối (配信予約): nút 「配信数を再計算するボタン」 biến mất khi di cursor |
| Redmine URL | https://redmine.watermelon.vn/issues/36730 |
| Auto-filled | 2026-05-26 by /new-task |
| Ngày báo cáo | 2026-05-25 |
| Khách hàng / PM báo | AI CSS (User: kato.yk415@gmail.com) |
| Module / Màn hình | Broadcast — Tab Đặt lịch phân phối (配信予約) / màn list send all |
| Priority | Medium |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

User: kato.yk415@gmail.com
Bot Name:

Ở tab Đặt lịch phân phối (配信予約) trong tính năng Phân phối tin nhắn (メッセージ配信), nút 「配信数を再計算するボタン」 (hiển thị ở đó) bị biến mất khi di chuyển cursor → không bấm được.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B5YN1MD25

---

### 原文 (JP)

```
メッセージ配信の配信予約タブのところに出る「配信数を再計算するボタン」がカーソルを動かすと消えてしまって押せない
```

<!-- TaskRef: user_report:Rec0B5YN1MD25 -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Trích từ journal #119437 của Kim Cúc (Section "Tái hiện case KH").

1. Tạo send all hiển thị ở tab 配信予約
2. Ở màn list, hover vào số friend sẽ nhận được Broadcast đã tạo

## Expected result

- Click được button 「現時点での配信予定数を再計算」 (配信数を再計算するボタン) khi hover vào số friend.

## Actual result

- Hiện tượng: không thể click vào button 現時点での配信予定数を再計算 (nút biến mất khi di chuyển cursor).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments từ Redmine:
- `1779623192bjJiPN.jpeg` — https://redmine.watermelon.vn/attachments/download/26041/1779623192bjJiPN.jpeg

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->
- Bug liên quan đến tooltip/popover hiển thị khi hover vào số friend ở màn list broadcast (cả tab 配信予約 lẫn 下書き).
- Verify trên cả 2 tab: `配信予約` (đã đặt lịch) và `下書き` (draft).
