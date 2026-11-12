# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43235 — [JOB] Job forward webhook test ở database callback backup ở Contabo` |
| Module / Màn hình | `Callback LINE qua cb-2 — DB backup Contabo và forward (webhook-relay)` |

## Mô tả bug (bản dịch tiếng Việt)

- Test với domain callback LINE phụ: https://cb-2.lmes.jp
- Khi thao tác phía LINE (kết bạn, send message, ...) nhận và xử lý callback bình thường (hiển thị trên chat 1:1, auto reply)
- Forward sang bên thứ 3 bình thường
- Có ghi nhận callback_event vào database callback backup ở Contabo

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #43235 không có attachment. -->

## Ghi chú thêm của Leader

- ⚠️ **Đây KHÔNG phải ticket bug** — tracker Redmine = "Improve nội bộ", status "New", không có Steps to reproduce / Expected / Actual result. Đây là task verify tính năng mới: domain callback LINE phụ `cb-2.lmes.jp` ghi callback_event vào DB backup ở Contabo + forward sang bên thứ 3, song song với xử lý callback bình thường (chat 1:1, auto reply...).
- Trên MCP LME TEST STUDIO, task tương ứng (`task_id=455`, feature `webhook-relay`) đã có sẵn **23 TC do AI sinh** (xem `04-tc-list.md`), chưa chạy (`untested=23`).
