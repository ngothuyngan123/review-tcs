# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bằng `/new-task https://redmine.watermelon.vn/issues/33117`.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#33117 — [Modal multi action] Action text không click được phần emoji` |
| Redmine URL | https://redmine.watermelon.vn/issues/33117 |
| Auto-filled | `2026-08-24 by /new-task` |
| Ngày báo cáo | `2025-12-15` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` (bug nội bộ — tracker `Bug tự detect`) |
| Module / Màn hình | `<chưa rõ — Redmine không set category>`. Theo journal #131644: **Chat 1:1 (FA-001)** — modal cấu hình hành động 「アクション」 (**SC-004**), action 「テキスト」 |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — description trống, không journal nào ghi domain/env>` |
| Tracker / Status | `Bug tự detect` / `Fix done - Đợi test` |
| Assigned to | `Ngô Thúy Ngần` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

> ⚠️ **Description Redmine TRỐNG** (`description = ""`). Toàn bộ thông tin bug chỉ nằm ở **tiêu đề ticket** + **1 ảnh đính kèm** + journals.
>
> Tiêu đề: `[Modal multi action] Action text không click được phần emoji`

**Journal #129540** (Ngô Thúy Ngần, 2026-08-19):

```
2026-08-19: Ngần check vẫn đang bug
```

> → Bug tồn tại **liên tục từ 2025-12-15 đến 2026-08-19** (~8 tháng), được người báo confirm lại trước khi fix.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> ⚠️ **Redmine KHÔNG có** — description trống, không journal nào ghi steps. Các bước dưới đây **suy từ mục 1 "Nguyên nhân" của journal #131644** (báo cáo AI Auto-fixbug), **cần tester verify lại trước khi dùng làm chuẩn**.

1. Mở màn **chat 1:1**, chọn một bạn bè để hiện khung hội thoại
2. Mở **modal multi action** 「アクション」 từ thanh công cụ gửi tin
3. Thêm **action gửi text** 「テキスト」
4. Bấm **icon emoji** (mặt cười) của action đó

## Expected result

> Suy từ tiêu đề ticket + mục 1 journal #131644.

- Bảng chọn emoji hiện ra và **giữ nguyên** trên màn hình.
- Chọn emoji → emoji được chèn vào **đúng ô nội dung của action**, không rơi sang ô nhập tin chat.

## Actual result

> Nguyên văn từ mục 1 "Nguyên nhân" journal #131644.

- Bấm icon emoji của action gửi text → bảng emoji **mở xong bị xoá ngay trong cùng cú click** → người dùng thấy "bấm mà không có gì hiện ra".
- Nếu bảng có hiện thì cả 2 bộ chọn emoji cùng xử lý việc chèn → **emoji bị chèn nhầm sang cả ô nhập tin chat**.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/22074/multiaction.png

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — description trống, không có Steps/Expected/Actual. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.
- ⚠️ **Điều kiện tái hiện then chốt**: bug **CHỈ xảy ra ở màn chat 1:1** vì đó là màn duy nhất khởi tạo **2 bộ chọn emoji** cùng lúc (một cho modal action, một cho ô nhập tin chat). Mở modal multi action từ màn khác (tự động trả lời, kịch bản, tag, form, đặt lịch, bán hàng...) chỉ có 1 bộ → **không tái hiện được**.
- ⚠️ Fix nằm ở **thư viện dùng chung** `public/js/fgEmojiPicker.js` + **nâng version asset chung** → mọi màn dùng emoji picker đều bị chạm. Xem `03-dev-impact.md` mục 7.
- Dev tự khai báo **chỉ verify mức lint**, **không chạy được runtime** trong container → toàn bộ hành vi UI phải do tester bấm tay verify.
- Bug đã tồn tại ~8 tháng (2025-12-15 → 2026-08-19) và được confirm "vẫn đang bug" ngay trước khi fix.
