# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#28542 — [Chat 1:1] Khi friend gửi stamp cho bot thì bị hiển thị code ở leftbar` |
| Redmine URL | https://redmine.watermelon.vn/issues/28542 |
| Auto-filled | `2026-08-26 by /new-task` |
| Ngày báo cáo | `2025-02-26` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` |
| Module / Màn hình | `Chat 1:1 (FA-001) — leftbar danh sách hội thoại` (suy từ subject, Redmine không có category) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine không ghi env; Dev ghi "Không tái hiện được runtime: MySQL/web dev host.docker.internal không kết nối được") |
| Tracker | `Bug tự detect` |
| Status hiện tại | `Fix done - Đợi test` |
| Assignee hiện tại | `Ngô Thúy Ngần` (2026-08-25, trước đó `Quỳnh Trang Nguyễn`) |

## Mô tả bug (nguyên văn từ khách hàng)

> Check case đang ở chat 1:1 và friend gửi tin stamp mới

**Journal #129573 — Ngô Thúy Ngần, 2026-08-19 (nguyên văn):**

> 2026-08-19: Ngần check lại vẫn đang bug
> Phải reload lại màn hình mới hiển thị đúng last message kiểu stamp

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" tách riêng — không tự suy diễn. Tester bổ sung sau khi verify. -->

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

- https://redmine.watermelon.vn/attachments/download/17939/stamp.png
- https://redmine.watermelon.vn/attachments/download/29174/chat-11.png (đính kèm 2026-08-19 kèm note "vẫn đang bug")

## Ghi chú thêm của Leader

⚠️ Bug không có section "Tái hiện bug" chuẩn trong Redmine (description chỉ 1 dòng) — root cause đã được Dev (AI Auto-fixbug) confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

⚠️ **Bug tái phát**: ticket mở từ 2025-02-26, đến 2026-08-19 QA check lại **vẫn còn bug** → đây là lần fix sau khi bug đã tồn tại lâu. Cần TC regression chặt.

⚠️ **Fix mở rộng hơn mô tả bug gốc**: ngoài lỗi hiển thị stamp, Dev còn vá 2 lỗi phát hiện trong review — (a) cập nhật last message **nhầm hội thoại** khi có nhiều tin đến gần nhau, (b) **lỗ hổng lộ nội dung tin nhắn** ở `/ajax/get-badge` (không lọc theo bot đang đăng nhập). Đây là 2 impact bắt buộc phải có TC riêng, KHÔNG nằm trong bug gốc.

⚠️ **Verify của Dev chỉ ở mức `lint`** (php -l / node --check), **không chạy runtime** vì môi trường dev không kết nối được DB/web. Toàn bộ hành vi thực tế chưa được ai chạy thử.

⚠️ Có sửa file JS (`public/js/chats/chat-v2.js`) → cần bump version static asset; tester phải hard-reload / kiểm tra cache trình duyệt trước khi kết luận fail.
