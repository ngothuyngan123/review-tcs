# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#28418 — [Talk-list] Sau khi change 1 status thì ko change tiếp được` |
| Redmine URL | https://redmine.watermelon.vn/issues/28418 |
| Auto-filled | `2026-08-27 by /new-task` |
| Ngày báo cáo | `2025-02-24` |
| Khách hàng / PM báo | Ngô Thúy Ngần |
| Module / Màn hình | Talk-list — MH 「チャット管理」 (danh sách hội thoại / chat management) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — Redmine description không ghi môi trường |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Thao tác:
1. Vào MH talk-list => Click tab dánh sách 一覧
2. Chọn msg chưa confirm => Click confirm
3. Chọn lại msg ở bước 2 => Click unconfirm

BUG: Ko chuyển sang unconfirm được
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Vào MH talk-list => Click tab dánh sách 一覧
2. Chọn msg chưa confirm => Click confirm
3. Chọn lại msg ở bước 2 => Click unconfirm

## Expected result

- Chuyển được msg ở bước 2 sang trạng thái unconfirm (未確認).

## Actual result

- Ko chuyển sang unconfirm được.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine issue #28418 KHÔNG có attachment nào.

## Ghi chú thêm của Leader

**Trạng thái Redmine hiện tại:** `Fix done - Đợi test` · Assignee: Quỳnh Trang Nguyễn (đổi từ AI LME Fix bug ngày 2026-08-25) · Tracker: `Bug tự detect` · Project: Lme.

**Lịch sử quan trọng (từ journals Redmine):**

| Ngày | Người | Nội dung |
|---|---|---|
| 2025-02-24 | Ngô Thúy Ngần | Tạo ticket |
| 2026-08-19 | Ngô Thúy Ngần | `2026-08-19: Ngần check lại vẫn đang bug` — bug tồn tại **~18 tháng**, đã re-confirm còn lỗi |
| 2026-08-21 | AI LME Fix bug | Auto-fixbug hoàn tất, chuyển status → Fix done - Đợi test (chi tiết ở `03-dev-impact.md`) |
| 2026-08-25 | Ngô Thúy Ngần | Assign sang Quỳnh Trang Nguyễn để test |

⚠️ **Bug được fix bởi hệ thống Auto-fixbug LME (AI), không phải dev người.** Đánh giá ảnh hưởng ở file 03 là báo cáo tự động — Leader cần soi kỹ mục "Function caller đã check" và phần tự review của AI trước khi chốt coverage.

⚠️ **Môi trường phát hiện không được ghi trong Redmine** — cần hỏi lại người báo bug (Ngần) trước khi chốt môi trường test. Theo RULE-08, kết quả chạy trên local/staging không đủ để kết luận cho các quan điểm media / domain / job / bill tiền.
