# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#35932 — [Chat 1:1] Đặt lịch send có delay message: message hiển thị ở màn chat 1:1 bị hiện code của friend info` |
| Module / Màn hình | Chat 1:1 (1:1チャット) — màn đặt lịch gửi 「送信予約」 + 「送信オプション」 bật delay message; hiển thị tin ở khung chat 1:1. Phía job: `snsline_job` (linect-service) — `DelayMessageService` |

## Mô tả bug (bản dịch tiếng Việt)

Server staging
Bot id 562
Line user id 131204
schedule_send_chat.id 697
Thời gian gửi 2026-08-24 11:30:00

-------------------------------
Nội dung điều tra bug, cần đọc trong file đính kèm `bug_35932_chat11_delay_friendinfo.md`.

Base branch: `release-t07-2026`

> Tóm tắt từ file đính kèm (để tiện đọc — xem nguyên văn trong attachment): khi **đặt lịch gửi** một **template group** nhiều template và bật **delay message**, tin **gửi tới LINE thì đúng** (friend info đã thay giá trị), nhưng bản ghi hiển thị ở **màn chat 1:1** lại hiện raw code `[FRIEND_INFO_xxx]`. Nguyên nhân: luồng delay truyền id template CHA (group) vào `req.templateIds` trong khi `listMessageToSave` mang id template CON → không match → `replace_content` lưu rỗng. Luồng gửi ngay (`sendNow`) không bị.

## Steps to reproduce

(Theo Journal #129829 — Thanh Phương)
1. Vào màn đặt lịch send ở màn chat 1:1, đặt lịch gửi 1 template (template có chứa code của friend info).
2. Setting On tính năng random message (delay message — 「送信オプション」 → 「メッセージを1通ずつ数秒遅延させて送信する」).
3. Gửi message cho user.

## Expected result

- Màn chat 1:1 hiển thị giá trị friend info đã thay (giống nội dung LINE user nhận được).

## Actual result

- Màn chat 1:1 hiển thị nguyên code friend info `[FRIEND_INFO_xxx]`; tin gửi sang LINE vẫn đúng.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [x] Có log / request-response (file phân tích điều tra `.md` có trích log)

- https://redmine.watermelon.vn/attachments/download/25262/2026_04_16_16_25_47_1_1%E3%83%81%E3%83%A3%E3%83%83%E3%83%88.png
- https://redmine.watermelon.vn/attachments/download/29191/2026_08_19_17_38_03_Window.png
- https://redmine.watermelon.vn/attachments/download/29321/bug_35932_chat11_delay_friendinfo.md

## Ghi chú thêm của Leader

- Môi trường phát hiện: **Staging**.
- Điều kiện lỗi: phải là **template group** (≥ 2 template con) + bật delay message ở lịch gửi. Template đơn (id cha = id con) vốn không lỗi.
- Tin LINE user nhận được đúng từ trước fix — lỗi chỉ ở dữ liệu lưu để hiển thị chat 1:1 (`messages_v2s.replace_content`); kèm theo Dev phát hiện `quote_token` / `line_message_id` / `message_line_capture` của luồng delay cũng bị bỏ sót → ảnh hưởng quote/unsend.
- Dev lưu ý hành vi đổi: template group bật cờ `is_delay_sent_message` → luồng delay nay gửi hết message con 1 lần (giống sendNow) thay vì giãn thời gian từng message con.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `562` (staging) |
| Friend | line_user_id `131204` |
| Đối tượng cấu hình | Template group `105649` = [`105650`, `105651`]; `schedule_send_chat.id = 697`; `SendRandomMessage.id = 868`; friend info setting_id `3112` (`[FRIEND_INFO_6J7bvo81WjGa]`, giá trị `dfgf`) · `3111` (`[FRIEND_INFO_JaeqVoQybGR2]`, rỗng) |
| Thời điểm lỗi | `2026/08/24 11:30:00` |
| Đối chứng | Cùng template group, đặt lịch **không** bật delay (luồng `sendNow`) → hiển thị đúng |

## Journal / note từ Redmine (nguyên văn)

**Journal #129829 — Thanh Phương — 2026-08-19:**

```
** Tái hiện bug:
- Vào màn đặt lịch send ở màn chat 1:1 đặt lịch gửi 1 template (template có chứa code của friend info)
- setting On tính năng random message
=> Gửi message cho user
```
