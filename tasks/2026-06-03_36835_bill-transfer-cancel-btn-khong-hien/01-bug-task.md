# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #36835 bởi `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36835 — [28-05-2026][28312][Bill tiền tool] Status chuyển khoản NH đang là "Chờ nhập tiền" 「入金待ち」 nhưng nút Hủy chuyển khoản (振込キャンセル) không hiển thị` |
| Redmine URL | https://redmine.watermelon.vn/issues/36835 |
| Auto-filled | `2026-06-03 by /new-task` |
| Ngày báo cáo | `2026-05-28` |
| Khách hàng / PM báo | `AI CSS` (KH cuối: info@yohaku-ai.co.jp — Bot YOHAKU清掃管理) |
| Module / Màn hình | `Bill tiền tool / Màn detail hợp đồng (Quản lý hợp đồng)` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: info@yohaku-ai.co.jp
Bot Name: YOHAKU清掃管理

Hiện đơn đang ở trạng thái "Chờ nhập tiền" 「入金待ち」 của hình thức chuyển khoản ngân hàng (銀行振り込み), nhưng nút Hủy chuyển khoản (振込キャンセルボタン) không được hiển thị.

Khách mong team kiểm tra: ở trạng thái 入金待ち thì nút hủy chuyển khoản có nên hiển thị để khách thao tác không.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B6J57KFGD

---

### 原文 (JP)
```
現在銀行振り込みの「入金待ち」のステータスになっているが、振込キャンセルボタンが表示されていない。
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Từ journal "Tái hiện case KH" của Kim Cúc (2026-06-03), nguyên văn. -->

1. Khi hợp đồng đang là năm.
2. Đang thanh toán là card => thực hiện chuyển sang tranfer (chuyển khoản).

## Expected result

- (Theo mong muốn KH) Ở trạng thái 入金待ち (Chờ nhập tiền / chờ chuyển khoản), nút Hủy chuyển khoản (振込キャンセル) hiển thị để khách thao tác được.
- (Theo cách fix Dev — xem `03-dev-impact.md`) Các button không bị disable: `次回決済から月払いに変更する` (đổi năm→tháng) và `クレジットカードに変更する` (đổi phương thức) phải enable; khi đổi phương thức thì thực hiện logic hủy chuyển khoản trước.

## Actual result

<!-- "Hiện tượng" nguyên văn từ journal tái hiện. -->

- Status hợp đồng đang là chờ chuyển khoản HOẶC đang chờ phát hành số tài khoản thì có 2 button bị disable: `[次回決済から月払いに変更する]` và button ở trường 決済方法 (`クレジットカードに変更する`).
- Nút Hủy chuyển khoản (振込キャンセル) không hiển thị (theo report KH).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- SnapCrab_NoName_2026-5-28_9-25-54_No-00.png — https://redmine.watermelon.vn/attachments/download/26126/SnapCrab_NoName_2026-5-28_9-25-54_No-00.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- ⚠️ **Có sai lệch mô tả cần verify**: KH report là "nút Hủy chuyển khoản (振込キャンセル) không hiển thị", nhưng phần Tái hiện + Đánh giá ảnh hưởng của Dev/Kim Cúc nói về **2 button bị disable** (`次回決済から月払いに変更する` đổi năm→tháng, `クレジットカードに変更する` đổi phương thức). Tester cần xác nhận: bug thực tế là nút hủy chuyển khoản KHÔNG hiện, hay là các button thay đổi bị disable — hai triệu chứng này khác nhau, ảnh hưởng tới scope TC.
- Bug **tái hiện được** (có steps từ journal). Root cause đã được Dev confirm qua đánh giá ảnh hưởng (`03-dev-impact.md`).
- Redmine có **Link TCs** (Sheet "Quản lý hợp đồng", Line 255-297) → đã fetch vào `04-tc-list.md`.
