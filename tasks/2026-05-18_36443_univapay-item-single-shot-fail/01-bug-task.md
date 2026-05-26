# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #36443 bằng `/new-task`. Tester verify rồi tick checkbox bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | #36443 — [15-05-2026][10926][App + API app] [Item] Decision Univapay lỗi — màn quay lại trước khi bấm nút mua, chỉ single-shot product fail |
| Redmine URL | https://redmine.watermelon.vn/issues/36443 |
| Auto-filled | 2026-05-18 by /new-task |
| Ngày báo cáo | 2026-05-15 |
| Khách hàng / PM báo | AI CSS (báo hộ KH user `wings.nontitle@gmail.com`, bot `バリューオブスピーカー`) |
| Module / Màn hình | App + API app — Page bán item (item single-shot) liên kết Univapay |
| Priority | Medium (Redmine Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine không ghi rõ env; KH report flow Production trên LINE app) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
User: wings.nontitle@gmail.com
Bot Name: バリューオブスピーカー

Khi thanh toán item, message 「処理完了まで2～3分かかる場合があります。」 (Có thể mất 2-3 phút để xử lý hoàn tất) hiển thị rồi màn hình lập tức quay về trước khi user kịp bấm nút mua, không thanh toán được.

[Bổ sung]
■Hiện trạng
・Page bán item liên kết với Univapay không xử lý được decision
・Cả Android và iPhone đều không được
・Decision sub continue thực hiện được vào 5/12 7:14 nên có vẻ không có vấn đề
・Test decision sub item: decision mới OK
・Chỉ item single-shot là không decision được

■Đã thử
・Check update LINE app
・Restart smartphone
・Tạo item khác để test

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B3ZVD299C
```

### 原文 (JP)

```
商品決済時に「処理完了まで2～3分かかる場合があります。」が表示された後にすぐに画面が購入ボタンを押す前に戻り、決済が行えない。

[補足]
■現状
・ユニバペイと連携している商品販売ページの決済処理ができない
・Android、iphoneに限らず不可
・サブスクの継続決済は5/12 7:14に行われているので問題ないと思われる
・サブスク商品のテスト決済は新規決済ができた
・単発商品のみ決済できない状態

■試したこと
・LINEのアプリアップデート確認
・スマホの再起動
・他の商品を作成して試した
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Từ journal "Tái hiện bug" của Thanh Phương (2026-05-18). KH gốc không có steps cụ thể — Dev tái hiện theo hướng số tiền > max Univapay. -->

1. Login vào Page bán item (item single-shot) đã liên kết Univapay.
2. Tạo / chọn item có số tiền bill **> số tiền max** mà account Univapay được phép.
3. Trên LINE app (Android hoặc iPhone), user nhấn nút **Mua** trên item bill Univapay.

## Expected result

- Khi bill thất bại do số tiền vượt max Univapay → hiển thị **message lỗi rõ ràng** cho user (không silent fail, không quay về màn talklist ngay).

## Actual result

- Hiển thị message 「処理完了まで2～3分かかる場合があります。」 rồi màn hình quay về talklist trước khi user kịp bấm nút mua → không bill tiền được, không có message lỗi.
- Bug chỉ xảy ra với **item single-shot** (単発商品). Subscription continue + subscription test decision đều OK.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments từ Redmine:
- https://redmine.watermelon.vn/attachments/download/25771/Screenshot_2026-05-15-12-24-05-29_94c3c0214f41e8559bec03caf75c21c7%20(1).jpg

## Ghi chú thêm của Leader

- Bug do KH report qua Slack list `Rec0B3ZVD299C` (xem link Slack trong description).
- Dev (Thanh Phương) tái hiện được theo hướng **số tiền bill > max Univapay** — đây là root cause: lỗi từ Univapay return về nhưng frontend không hiển thị → user thấy như "màn hình tự quay lại". KH chỉ thấy hiện tượng, không biết nguyên nhân số tiền vượt max.
- Function fix: `paymentCreditCardItemV2Univapay` (app/Http/Controllers/Basic/SalesManagementV2Controller.php) — xem `03-dev-impact.md`.
- TC tham chiếu (Dev đã chuẩn bị template): Sheet master "Improve bill tiền univapay" từ row 292 — xem `04-tc-list.md`.
