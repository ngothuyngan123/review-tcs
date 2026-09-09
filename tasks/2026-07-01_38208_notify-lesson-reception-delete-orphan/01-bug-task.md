# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine bởi `/new-task`. Tester đọc lại + tick checkbox verify bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38208 — [26-06-2026][TY-11380][Notify Setting] Thông báo (1 cái) về đặt chỗ/hủy không sao xóa được dù làm gì (通知が消えない)` |
| Redmine URL | https://redmine.watermelon.vn/issues/38208 |
| Auto-filled | `2026-07-01 by /new-task` |
| Ngày báo cáo | `2026-06-26` |
| Khách hàng / PM báo | AI LME CSS (KH: Risa Yoga — risayoga39@gmail.com, Bot: Risa Yoga) |
| Module / Màn hình | Notify Setting (Lesson Booking / Notification — App mobile) |
| Priority | Medium |
| Môi trường phát hiện | Production — App mobile (スマホアプリ). Khách báo qua Form hỏi thao tác. `<tester confirm URL>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: risayoga39@gmail.com
Bot Name: Risa Yoga

【Form hỏi về cách thao tác (操作方法に関するお問い合わせフォーム)】
Về thông báo (通知) khi có đặt chỗ hoặc hủy đặt chỗ. Có 1 thông báo dù làm gì cũng không xóa/mất đi được. Đó là thông báo của 1 trường hợp: đặt chỗ đã vào, sau đó phía chúng tôi (admin) tự thực hiện thao tác hủy.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BDARM3S90

---

原文 (JP)
【操作方法に関するお問い合わせフォーム】
予約やキャンセルが入ったときの通知に関して。通知1件が何をしても消えません。予約が来たものにこちらからキャンセル作業を行った1件です。
```

**Comment bổ sung từ khách (journal Redmine):**
- Ngọc Ánh (2026-06-26): "Trên app mobile, hiện đang có 1 thông báo về đặt lịch bài học bị giữ lại và không thể xóa được. Mong hỗ trợ kiểm tra giúp."
- エルメCS管理 (沖原) (Slack): "スマホアプリでレッスン予約の通知が1件残ったまま消すことが出来ない状態です。" (Trên app mobile, có 1 thông báo đặt chỗ lesson còn sót lại không sao xóa được.)
- WSSサポーター (2026-06-29): "Sau khi điều tra, xác nhận sự kiện đặt chỗ tương ứng đã bị xóa từ ngày 24/5. Hiện bản thân thông tin đặt chỗ không còn tồn tại. Đã thực hiện khôi phục cho user tương ứng."

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Từ Section "Tái hiện bug" — journal 124422 (Thanh Phương, 2026-07-01) -->

1. User thực hiện booking, sau đó admin nhấn **cancel booking** → hệ thống tạo notify (mobile_notify type=11) có status **chưa confirm (is_confirm=0)**.
2. Admin vào **app mobile**, nhấn **xóa slot (受付枠 / reception)** của calendar Lesson.

## Expected result

- Khi xóa slot, các notify (mobile_notify) tương ứng của booking trong slot cũng bị xóa.
- Màn danh sách notify ở menu Lesson không còn hiển thị notify chưa đọc mồ côi; badge giảm đúng.

## Actual result

- Khi xóa slot **chưa xóa các notify** → màn danh sách notify ở menu Lesson vẫn hiện có notify chưa đọc.
- Vào bên trong detail thì lại **không hiện các notify đó** nữa nên user **không thể confirm** notify.
- ⇒ Thông báo trở thành mồ côi, dù làm gì cũng không xóa/mất đi được; badge kẹt vĩnh viễn.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- download_file.png — https://redmine.watermelon.vn/attachments/download/27575/download_file.png
- download_file.png — https://redmine.watermelon.vn/attachments/download/27581/download_file.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- ⚠️ Bug xảy ra **chỉ khi thao tác xóa slot trên APP** (API/JWT không có session web → `getBotId()` rỗng). Trên **web** thao tác xóa slot vẫn đúng.
- ⚠️ Root cause đã được Dev (Auto-fixbug) confirm qua đánh giá ảnh hưởng (xem `03-dev-impact.md`). TCs nên tập trung verify cách fix (app xóa đúng notify) + regression web + data recovery orphan cũ.
