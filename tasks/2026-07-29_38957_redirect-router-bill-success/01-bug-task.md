# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bởi `/new-task` — tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38957 — Khi mua hợp đồng thành công cần redirect sang router bill success trước sau đó mới quay về màn bill thành công` |
| Redmine URL | https://redmine.watermelon.vn/issues/38957 |
| Auto-filled | 2026-07-29 by /new-task |
| Ngày báo cáo | 2026-07-22 |
| Khách hàng / PM báo | Do Van Tu TuDV (tracker: "Bug tự detect" — bug nội bộ tự phát hiện) |
| Module / Màn hình | `<chưa rõ — Redmine không set category; suy từ subject: màn Bill success / thanh toán hợp đồng bot (bill_tool)>` |
| Priority | Medium _(Redmine priority = Normal)_ |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Các router bill success cần được redirect trước khi quay về màn bill thành công:

```
- /monthly/standard_success
- /yearly/standard_success
- /monthly/pro_success
- /yearly/pro_success
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. Xem cảnh báo ở "Ghi chú thêm của Leader". -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #38957 KHÔNG có attachment. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — description chỉ liệt kê 4 router `*_success`, không có step tái hiện / expected / actual. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`, journal #126891). TCs nên tập trung verify **cách fix (redirect flow) + regression impact** trên các luồng mua/upgrade.

- Tracker Redmine = **"Bug tự detect"** (bug tự phát hiện nội bộ, không phải khách hàng báo).
- `done_ratio = 100%` — Dev đã fix xong; assignee hiện tại: **Tuấn Anh Trần**.
- Root behavior (từ subject): sau khi mua hợp đồng thành công, hệ thống đang next thẳng sang step "success" mà **không redirect qua router bill success** trước → cần redirect sang router success rồi mới back về màn bill thành công.
