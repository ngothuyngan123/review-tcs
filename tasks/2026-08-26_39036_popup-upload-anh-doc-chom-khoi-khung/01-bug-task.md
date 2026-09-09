# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bởi `/new-task`. Tester verify rồi tick checkbox bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39036 — [Upload ảnh][Popup] Ảnh bị chờm ra khỏi khung sau khi upload ảnh dọc và đã được resize` |
| Redmine URL | https://redmine.watermelon.vn/issues/39036 |
| Auto-filled | `2026-08-26 by /new-task` |
| Ngày báo cáo | `2026-07-24` |
| Khách hàng / PM báo | `Đoàn Thị Bích Hảo` |
| Module / Màn hình | `Popup (FA-018) — màn tạo/sửa popup 「ポップアップ（作成）」, khối 「プレビュー」 (SCR-PU-02)` ⚠️ *Redmine `category` trống — giá trị này suy từ subject + journal Auto-fixbug + Studio task #203, tester confirm lại* |
| Priority | `Medium` (Redmine priority = `Normal`) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (description không ghi env; báo cáo dev + Studio chỉ chạy `local`) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Steps:
1. Đi đến màn popup
2. Thực hiện upload ảnh dọc (dài theo chiều dọc) - kich thước 2048x10000 px
3. check ảnh sau khi lưu

Actuals:
3. Anhr đã được resize về kích thước tương ứng với max kích thước = 2048px, nhưng ảnh vẫn bị chờm ra khỏi khung

Expected:
3. ảnh sau khi resize hiển thị đúng kích thước, và căn chỉnh để không bị chờm ra khỏi khung


=> evidence: https://prnt.sc/efd28xbC67TS
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Đi đến màn popup
2. Thực hiện upload ảnh dọc (dài theo chiều dọc) - kich thước 2048x10000 px
3. check ảnh sau khi lưu

## Expected result

- 3. ảnh sau khi resize hiển thị đúng kích thước, và căn chỉnh để không bị chờm ra khỏi khung

## Actual result

- 3. Anhr đã được resize về kích thước tương ứng với max kích thước = 2048px, nhưng ảnh vẫn bị chờm ra khỏi khung

## Ảnh / video / log đính kèm

- [x] Có screenshot — link ngoài trong description (KHÔNG phải Redmine attachment): https://prnt.sc/efd28xbC67TS
- [ ] Có video
- [ ] Có log / request-response

> `issue.attachments` từ Redmine API = **rỗng**. Evidence duy nhất là link prnt.sc dán trong description — link prnt.sc có thể hết hạn, tester nên tải về lưu kèm folder.

## Ghi chú thêm của Leader

- **Đây là lần fix THỨ 2 cho cùng 1 bug.** Báo cáo Auto-fixbug (journal 2026-08-21) tự nêu: *"Fix trước nhắm SAI hướng (tưởng tràn ngang, thêm `max-width` vốn đã có sẵn ở reset.css → no-op, bug vẫn còn)"*. Bug đã từng được chuyển "Fix done" một lần mà không hết → **TC phải tái hiện đúng bằng ảnh gốc 2048×10000 đi qua luồng upload/resize thật**, không được test bằng ảnh đã resize sẵn.
- Trạng thái Redmine hiện tại: **`Fix done - Đợi test`**, custom field `Commit Date = 2026-08-21`.
- Fix là **thuần CSS 1 dòng** (`max-height`) trong khung preview màn admin — không đụng luồng upload/resize server, không đụng popup thật render trên site khách.
- Dev có ghi **yokoten chưa sửa**: popup thật trên site khách (`public/js/embedded-popup/default_setting.js`) cũng chỉ set `width:100%`, không giới hạn chiều cao — *"cùng pattern nhưng khác phạm vi ticket nên chỉ ghi nhận, không sửa"*. Leader cân nhắc có yêu cầu TC quan sát (không phải TC fix) cho popup thật hay tách ticket riêng.
