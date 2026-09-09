# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bởi `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38075 — Login account thanhntp142+1 bị hiện lỗi 404` |
| Redmine URL | https://redmine.watermelon.vn/issues/38075 |
| Auto-filled | `2026-06-25 by /new-task` |
| Ngày báo cáo | `2026-06-24` |
| Khách hàng / PM báo | `Thanh Phương` |
| Module / Màn hình | `<chưa rõ — tester fill>` (gợi ý: Login / Select bot — Basic Access middleware) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `Staging (staging.lme.jp)` (TCs đánh dấu "OK staging") |

## Mô tả bug (nguyên văn từ khách hàng)

Check bảng user_selected_bot thì bot_id đang select là của 1 user khác và user thanhntp142+1 không được phân quyền (không có trong bảng user_staff_bot)

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Chuẩn bị data: bảng `user_selected_bot` có `bot_id` đang select là của 1 user khác, và user `thanhntp142+1` **không được phân quyền** (không có bản ghi trong bảng `user_staff_bot`).
2. User `thanhntp142+1` thực hiện login.

## Expected result

- <Section "Tái hiện bug" trong Redmine không ghi rõ Expected — theo cách fix (file 03): redirect user về màn list bot / `/admin/pre-select-bot` thay vì lỗi 404.>

## Actual result

- Bị hiện lỗi 404.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

(Redmine issue #38075 không có attachment.)

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->
- Bug liên quan trực tiếp middleware `BasicAccess` — kiểm soát quyền truy cập khi user đã select 1 bot mà không/không-còn là staff.
- Lưu ý đối chiếu: Dev ghi "redirect về màn **list bot**" (file 03), nhưng TCs human trong Sheet expect màn `/admin/pre-select-bot`. Leader xác nhận target redirect đúng khi review.
