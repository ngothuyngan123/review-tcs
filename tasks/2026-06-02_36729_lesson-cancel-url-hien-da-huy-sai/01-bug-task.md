# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36729 — [25-05-2026][11020][Lesson] Lesson: 「キャンセル用URL」 hiện 'đã hủy' nhưng thực tế thông báo chờ chưa cancel` |
| Redmine URL | https://redmine.watermelon.vn/issues/36729 |
| Auto-filled | `2026-06-02 by /new-task` |
| Ngày báo cáo | `2026-05-25` |
| Khách hàng / PM báo | `AI CSS` |
| Module / Màn hình | `Lesson` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine không ghi rõ; URL lỗi dạng liff.line.me) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: kato-y@entrance.jpn.com
Bot Name: wakumake

Nhận nhiều inquiry từ KH: khi đặt chỗ Lesson (レッスン予約), lúc nhận thông báo chờ cancel (キャンセル待ち通知), click vào 「キャンセル用URL」 được auto gửi đến, thì màn hình hiển thị 「予約が解除されました」, nhưng thực tế việc nhận thông báo (通知受け取り) chưa bị hủy.
Bên tôi không tái hiện được vấn đề tương tự, có phải đang phát sinh lỗi (不具合) gì không?

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B5QHK6UV9

---

### 原文 (JP)
```
レッスン予約のャンセル待ち通知受け取り時に自動送信される「キャンセル用URL」にアクセスした際に「予約が解除されました」と表示されるが、実際には通知受け取りがキャンセルされていない、という問い合わせが複数来ております。
私の方では同じ問題は確認できませんでしたが、何か不具合が発生していますか？
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguồn: journal "** Tái hiện Bug" của Thanh Phương (Redmine #36729). KH gốc không tái hiện được, nhưng QA/Dev đã tái hiện. -->

1. User đăng ký nhận thông báo chờ cancel (キャンセル待ち通知受け取り) của slot A — **lần 1** → thành công.
2. Tiếp tục nhấn đăng ký nhận thông báo của **cùng slot A** — **lần 2**.
3. Khi đăng ký lần 2, bot vẫn send 1 message "Đăng ký nhận notify success", trong đó 「キャンセル用URL」 **không có id của booking**.
4. User nhấn vào URL này (dạng `https://liff.line.me/1657756647-Hkw1Talb?calendar_id=10202&tab=detail&booking_id=` — phần `booking_id` rỗng).

## Expected result

- 「キャンセル用URL」 phải gắn đúng booking_id của đăng ký; nếu đăng ký chưa bị hủy thì KHÔNG được hiển thị 「予約が解除されました」.
- (Sau fix) Đăng ký trùng cùng slot phải bị chặn ngay, không gửi lại action/URL hủy thừa.

## Actual result

- Màn hình hiển thị 「予約が解除されました」 (đã hủy) nhưng thực tế bản ghi nhận thông báo (status WAIT_CANCEL) **chưa bị hủy** → user vẫn tiếp tục nhận thông báo.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Đính kèm từ Redmine:
- https://redmine.watermelon.vn/attachments/download/26104/287d1273-eef7-4998-af16-e2f08698bc36.png
- https://redmine.watermelon.vn/attachments/download/26105/97f5d576-4d2a-4a2e-b3cb-9f2b2cbe08be.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- **Account/case tái hiện thực tế (journal Ngọc Ánh):** Tên friend 加藤ゆうま — Booking lesson まかいの牧場 — Ngày nhận message thông báo chờ cancel: 05/26 08:54.
- **Clarify từ phía LME (journal 2026-06-02):** Hiện CHƯA có chức năng xóa "thông báo chờ hủy (キャンセル待ち通知)". Nếu đăng ký trùng, click 「URL hủy」 trong message tự động sẽ hiện sai 「予約が削除されました」. Tương lai LME dự kiến chặn đăng ký trùng. Hiện tại muốn xem lịch sử đặt chỗ nên dùng "URL trang lịch sử đặt chỗ" thay vì "URL hủy".
