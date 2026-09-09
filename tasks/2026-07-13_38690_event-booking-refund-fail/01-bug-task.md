# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38690 — [Event booking] Thao tác refund bị "refund fail"` |
| Redmine URL | https://redmine.watermelon.vn/issues/38690 |
| Auto-filled | `2026-07-13 by /new-task` |
| Ngày báo cáo | `2026-07-10` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` |
| Module / Màn hình | `Event Booking — màn hình quản lý booking event (thao tác refund)` *(suy từ subject; Redmine không có category)* |
| Priority | `Medium` *(Redmine: Normal)* |
| Môi trường phát hiện | `<chưa rõ — tester fill>` *(description không nêu env; journal Dev chỉ nhắc DB dev)* |

> Tracker: `Bug tự detect` · Status Redmine: `Fix done - Đợi test` · Assignee: Ngô Thúy Ngần · Parent: #26684

## Mô tả bug (nguyên văn từ khách hàng)

```
1. User booking event có bill tiền stripe
2. Admin thao tác refund ở màn hình quản lý booking event

BUG: GUI hiển thị lỗi "refund fail"
Expect: Refund success
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. User booking event có bill tiền stripe
2. Admin thao tác refund ở màn hình quản lý booking event

## Expected result

- Refund success

## Actual result

- GUI hiển thị lỗi "refund fail"

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/28053/6233287162426233783.jpg

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- Parent ticket: #26684. Dev (AI auto-fixbug) ghi rõ: fix được làm **độc lập trên branch `ai_small_38690`** vì run offline không verify được #26684; nếu #26684 là bug đang mở có branch `ai_small_26684` thì human nên chuyển commit sang branch đó trước khi push → **cần confirm branch nào QA test**.
- Bug chỉ xảy ra với booking thanh toán kiểu **PaymentIntent** (`strip_charge_id` dạng `pi_`); booking cũ dạng `ch_` vẫn refund được → precondition data quan trọng khi test.
