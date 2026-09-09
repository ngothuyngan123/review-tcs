# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39507 — [08-08-2026] [TY-11824] [Booking Event] Lỗi khi test thanh toán event đặt chỗ 11/5-6SASALABO合宿` |
| Redmine URL | https://redmine.watermelon.vn/issues/39507 |
| Auto-filled | `2026-08-18 by /new-task` |
| Ngày báo cáo | `2026-08-08` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn gốc: OEM tạo task trên Slack — ユーザー問い合わせ, 管理番号 TY-11824, 担当 沖原) |
| Module / Màn hình | `Booking Event` (category Redmine) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<Redmine description KHÔNG ghi rõ>` — theo mục "Bằng chứng" của đánh giá ảnh hưởng (file 03): log **production** của khách 2026-08-06 17:04:20, tham số môi trường cổng thanh toán = 0 (môi trường THỬ của UnivaPay) |
| Trạng thái Redmine | `Fix done - Đợi test` · assigned_to `Ngô Thúy Ngần` · Commit Date `2026-08-12` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine. KHÔNG diễn giải lại. -->

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-11824
担当: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1786182896799669?thread_ts=1786182896.799669&cid=C0BALS7S73L

Quản lý No　：TY-11824
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BPS05B1L0
Địa chỉ ：ma-gta2@l-marketing.jp
Tên LOA　　：【FC問い合わせ】 EMILUCA
Phụ trách　　 ：沖原
Công cụ　 ：リンク
Nội dung yêu cầu
Khi thử test thanh toán ở event đặt chỗ thì hiển thị lỗi.

Event đặt chỗ：「11/5-6SASALABO合宿」
Course：「一般の方」

---
h3. 原文 (JP)
<pre>管理No　：TY-11824
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BPS05B1L0
アドレス ：ma-gta2@l-marketing.jp
LOA名　　：【FC問い合わせ】 EMILUCA
担当　　 ：沖原
ツール　 ：リンク
問い合わせ内容
イベント予約でテスト決済をしようとするとエラーが表示される。

イベント予約：「11/5-6SASALABO合宿」
コース：「一般の方」</pre>

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống theo quy tắc /new-task. Xem "Ghi chú thêm của Leader" để biết dữ kiện rời rạc trích từ journal. -->

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

- https://redmine.watermelon.vn/attachments/download/28938/4bb0c0e4-9f05-4b7c-9733-dab31a14c1fc.png
- https://redmine.watermelon.vn/attachments/download/28939/ddb97acf-c71b-4fde-bb71-550cfd0c9c56.jpg

## Ghi chú thêm của Leader

⚠️ **Bug không có section "Tái hiện bug" trong Redmine** — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

### Dữ kiện rời rạc trích từ journal Redmine (không phải steps chính thức)

| Journal | Nội dung |
|---|---|
| J#128666 (2026-08-10) | WSSサポーター: "Chúng tôi đã kiểm tra nhưng hiện tại **chưa tái hiện được** hiện tượng này. Ngoài ra, khi kiểm tra log ngày 8/7・8/8, cũng **không tìm thấy log xử lý đặt lịch** tương ứng." |
| J#128691 (2026-08-11) | Khách cung cấp: friend lỗi — LINE 濱﨑由香 (tên hệ thống ハマサキテスト), LINE れーさん♡ (tên hệ thống テスト). Thời điểm: "kể từ ngay sau khi thêm gói 66000 yên cuối tháng 7 & chọn gói 66000 yên để test thanh toán". |
| J#128717 (2026-08-11) | WSSサポーター: "nguyên nhân của lỗi lần này là do **số tiền đặt chỗ vượt quá giới hạn**. Mong quý khách cài đặt số tiền của khóa **dưới 50,000円** rồi thử thanh toán test lại." |
| J#129041 (2026-08-14) | エルメサポート: "do **đã đạt giới hạn sử dụng của tài khoản UnivaPay** đang sử dụng nên khoản thanh toán 66000 yên không thể thực hiện." |
| J#129061 (2026-08-15) | エルメサポート: thanh toán test cũng bị chặn nếu account vượt hạn mức; **エルメ account khác liên kết cùng tài khoản UnivaPay cũng gặp vấn đề tương tự**. |

> ⚠️ **2 vấn đề tách rời** (theo file 03): (1) thanh toán 66.000 yên thất bại — **giới hạn cổng UnivaPay môi trường thử ~50.000 yên/giao dịch, KHÔNG fix bằng code**; (2) hộp thoại lỗi **hiện trống không có chữ** — đây mới là phần được fix. TC không được kỳ vọng 66.000 yên thanh toán thành công ở môi trường thử.
