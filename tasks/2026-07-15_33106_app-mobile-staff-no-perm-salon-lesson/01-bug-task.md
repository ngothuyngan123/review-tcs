# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#33106 — [App mobile] User staff không được phân quyền vẫn vào được màn salon và lesson` |
| Redmine URL | https://redmine.watermelon.vn/issues/33106 |
| Auto-filled | 2026-07-15 by /new-task |
| Ngày báo cáo | 2025-12-12 |
| Khách hàng / PM báo | Thanh Phương |
| Module / Màn hình | App mobile — màn Salon Booking (FA-020) / Lesson Booking (FA-019). *(Category Redmine trống — suy từ subject; tester verify.)* |
| Priority | Medium *(Redmine: Normal)* |
| Môi trường phát hiện | `<chưa rõ — tester fill>` *(description trống, không nêu môi trường; nhánh fix gốc `release_step_20260623`)* |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Description Redmine TRỐNG. Nội dung dưới đây tổng hợp từ subject + comment QA (journal #125868), KHÔNG bịa. -->

Description trên Redmine #33106 để trống.

Theo subject: **User staff KHÔNG được phân quyền vẫn vào được màn Salon và Lesson trên App mobile.**

Comment QA (Ngô Thúy Ngần — 2026-07-14, journal #125868):
> **Expect:** Nếu staff không được phân quyền, khi access màn hình thì Hiển thị msg báo lỗi `この機能の操作権限が付与されていません。` giống bên event booking.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — steps để trống, tester bổ sung khi test. -->

1.
2.
3.

## Expected result

- Staff **không được phân quyền** salon/lesson → khi access màn Salon / Lesson trên App mobile phải hiển thị message báo lỗi `この機能の操作権限が付与されていません。` (không có quyền thao tác chức năng này), giống hành vi màn Event booking. *(nguồn: journal #125868)*

## Actual result

- Staff không được phân quyền **vẫn vào được** màn Salon và Lesson (xem được danh sách), không hiển thị message báo lỗi. *(suy từ subject)*

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #33106 không có attachment. -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine (description trống, không có section "Tái hiện bug"/Steps). Root cause đã được Dev (AI Auto-fixbug) confirm qua đánh giá ảnh hưởng — xem `03-dev-impact.md`. TCs nên tập trung verify cách fix (check phân quyền staff ở 2 API list salon/lesson) + regression impact.

- Bản chất là **bug phân quyền (PERM)** ở API mobile: 2 endpoint list (`getListCalendarSalon`, `getListCalendarLesson`) thiếu `checkHasPermission`, khác với màn Event booking đã có.
- Message chuẩn kỳ vọng: `この機能の操作権限が付与されていません。`
- Lưu ý: phần **hiển thị message** nằm ở repo Flutter (app mobile) — ngoài scope repo backend `sns-line`; nhưng backend fix đã **chặn data** (trả rỗng) khi staff thiếu quyền.
