# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | LME-2054 |
| Ngày báo cáo | 2026-04-18 |
| Khách hàng / PM báo | PM Tanaka (khách hàng: Salon ABC) |
| Module / Màn hình | Broadcast / Scheduled broadcast |
| Priority | High |
| Môi trường phát hiện | Production |

## Mô tả bug (nguyên văn từ khách hàng)

> Khi tôi tạo 1 broadcast schedule gửi lúc 2026-04-20 09:00 JST cho tag "VIP" (150 friends), đến giờ chạy thì chỉ có 98 friends nhận được. Nhưng lúc tôi preview ở bước tạo broadcast thì hệ thống báo 150 recipients. Khách hàng đang phàn nàn vì missed campaign sale.

## Steps to reproduce

1. Login bot có ≥ 150 friends với tag "VIP".
2. Vào Broadcast → Create new broadcast.
3. Chọn filter: tag = "VIP".
4. Preview recipients: hệ thống hiển thị "150 recipients".
5. Set scheduled time = 2 ngày sau, 09:00 JST.
6. Trong 2 ngày chờ, có ~50 friend mới được gắn thêm tag "VIP" (tăng từ 150 → 200).
7. Đến 09:00 JST → broadcast chạy.

## Expected result

- Broadcast gửi đến **200 friends** (tag "VIP" tại thời điểm chạy).
- Hoặc: gửi đến đúng **150 friends** đã snapshot tại lúc tạo (nếu spec là snapshot).

## Actual result

- Chỉ 98 friends nhận được.
- Log cho thấy 52 friend bị skip với lý do "tag_mismatch" mặc dù tag VIP vẫn active.

## Ảnh / video / log đính kèm

- [x] Có screenshot (preview recipients = 150)
- [ ] Có video
- [x] Có log (attached: broadcast_run_log_2026-04-20.json)

## Ghi chú thêm của Leader

- Spec hiện tại chưa clarify rõ "snapshot tại lúc tạo" hay "resolve tại lúc chạy".
- Timezone: bot đang config JST, cần test thêm case bot ở timezone khác.
- Account test: `test-salon-abc@dev.lme`
