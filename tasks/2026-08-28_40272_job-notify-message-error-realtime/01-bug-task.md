# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40272 — [LME-JOB][notify]  imporve lại case notifty message error notify realtime` |
| Redmine URL | https://redmine.watermelon.vn/issues/40272 |
| Auto-filled | `2026-08-28 by /new-task` |
| Ngày báo cáo | `2026-08-27` |
| Khách hàng / PM báo | `Văn Dũng Đinh` (author = assignee = Dev) |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine `category` trống, không có custom field. Tham chiếu: Studio task #260 `feature = notify-setting`) |
| Priority | `Medium` (Redmine priority = `Normal`) |
| Môi trường phát hiện | `<chưa rõ>` — description KHÔNG nêu môi trường; chỉ ghi `base branch: release-t08-2026` |

> ⚠️ **Đây KHÔNG phải bug từ khách hàng.** Redmine tracker = **`Improve nội bộ`** (đã đổi từ tracker id 5 → 19 bởi Thanh Duy Nguyen lúc 2026-08-28 11:22). Ticket do Dev tự tạo, parent issue = **#39543**.

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #40272. KHÔNG diễn giải lại. -->

```
base branch: release-t08-2026
1. Xác định các bot có message error mới bởi query sau ví dụ như sau:
ví dụ: SELECT DISTINCT(bot_id) FROM message_error WHERE id > 58341051 ORDER BY message_error.id DESC

Bảng job_config_daily lưu thêm trường để lưu last_id bảng message_error.id dùng cho query trên. Chạy xong lưu lại id mới
- last_id_message_error_notify_app: Dùng cho task HandlePushMessageNotifyService
- last_id_message_error_notify_pc : Dùng cho task HandlePushNotifyPc
- last_id_message_error_notify_chat_work : Dùng cho task HandlePushNotifyChatwork

2. Phần cần sửa: case schedule realtime, kiểm tra điều kiện setting và tạo notify luôn cho các notify_setting của mấy bot thuộc list trên, ko cần query lại countMsgError để check khác nhau nữa, vì chắc chắn các bot trong list này mới có message_error mới.
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine #40272 KHÔNG có section "Tái hiện bug" — ticket improve, không có flow tái hiện. -->

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

> Redmine #40272: `attachments = []` (không có file đính kèm nào).

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

Bổ sung ngữ cảnh lấy từ Redmine (không diễn giải):

- Tracker = `Improve nội bộ`, status = `New`, parent issue = **#39543**.
- Nội dung "Đánh giá ảnh hưởng phía dev" **không nằm trong description** mà ở **journal #133203** (Văn Dũng Đinh, 2026-08-27T06:51:56Z) — đã map sang [03-dev-impact.md](03-dev-impact.md).
- Description hiện tại được Dev bổ sung sau (journal #133396, 2026-08-28T06:53). Bản đầu chỉ có đúng dòng `base branch: release-t08-2026`.
- Đây là task **job nền** (3 job: `HandlePushMessageNotifyService`, `HandlePushNotifyPc`, `HandlePushNotifyChatwork`) + có **ALTER TABLE** `job_config_daily` → xem **RULE-08** (job / migration không kết luận từ local-staging).
