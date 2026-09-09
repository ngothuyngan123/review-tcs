# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #36768 bởi `/new-task`. Tester đọc lại + tick checkbox verify trước khi chạy skill tiếp theo.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36768 — Get premium ID của bot` |
| Redmine URL | https://redmine.watermelon.vn/issues/36768 |
| Auto-filled | `2026-07-02 by /new-task` |
| Ngày báo cáo | `2026-05-26` |
| Khách hàng / PM báo | `Ngọc Ánh` |
| Module / Màn hình | `Hiển thị LINE ID của bot — header / bill (請求) / admin (アカウント検索, supper admin) / backup` |
| Priority | `Medium` |
| Môi trường phát hiện | `Staging` |

> ⚠️ Đây là **Feature (仕様変更), không phải bug tái hiện được**. Redmine không có Section "Tái hiện bug" — phần dưới là **Spec**. TCs nên tập trung verify **đúng spec + regression** ở các màn hiển thị LINE ID (xem file 03).

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Tên gốc: 【仕様変更】プレミアムIDの自動更新
Môi trường Staging
【マーケ】エルメ（@281qduvu）
Premium ID: @lmessage

Spec:
1. Khi add bot/change bot thì kiểm tra nếu có premiumId => Tất cả những cột LINE ID trên GUI sẽ ưu tiên hiển thị premiumId (Nếu không có premiumId thì mới hiển thị basicId thường) => Chỗ này cần kiểm tra all code và báo lại tester những màn cần check
2. Click button 情報更新 ở header cũng get lại premiumId (nếu có)
3. Có job chạy hàng ngày để update lại premiumId (Nếu có)

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Feature spec — Redmine không có Section "Tái hiện bug". Để trống. -->

1.
2.
3.

## Expected result

<!-- Xem Spec 1/2/3 phần "Mô tả bug" ở trên + Đánh giá ảnh hưởng file 03. -->

-

## Actual result

<!-- Không áp dụng (feature mới, không có actual bug behavior). -->

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments (Redmine):
- スクリーンショット 2026-05-28 7.15.20.png — https://redmine.watermelon.vn/attachments/download/26124/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-05-28%207.15.20.png
- スクリーンショット 2026-05-28 7.14.44.png — https://redmine.watermelon.vn/attachments/download/26125/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-05-28%207.14.44.png

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine (đây là feature/spec change). Root cause + phạm vi thay đổi đã được Dev confirm qua đánh giá ảnh hưởng (file 03, journal #124403). TCs nên tập trung verify **cách hiển thị premium-first + regression impact** ở toàn bộ màn Dev liệt kê. Bot test: 【マーケ】エルメ（@281qduvu）, Premium ID @lmessage (Staging).
