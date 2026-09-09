# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38003 — Sửa màn hình lịch sử access bot theo sort theo time_access` |
| Redmine URL | `https://redmine.watermelon.vn/issues/38003` |
| Auto-filled | `2026-06-22 by /new-task` |
| Ngày báo cáo | `2026-06-22` |
| Khách hàng / PM báo | `Do Van Tu TuDV` |
| Module / Màn hình | `Admin — Màn hình lịch sử access bot (アクセス履歴) + export CSV / detail bot (Supper Admin)` (suy từ subject + đánh giá ảnh hưởng) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

> ⚠️ Redmine #38003 có **description rỗng**. Nội dung bug chỉ có ở subject + journal "Đánh giá ảnh hưởng dev" (xem `03-dev-impact.md`).

Subject: **Sửa màn hình lịch sử access bot theo sort theo time_access**

Theo đánh giá ảnh hưởng của Dev (root cause):
- Danh sách lịch sử access đang order theo `id` (mong đợi: order theo `time_access`).
- Dropdown chọn bot trên màn không hoạt động.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

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

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Bug không tái hiện được trong Redmine (description rỗng, không có Section "Tái hiện bug" → Steps/Expected/Actual để trống) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (order theo `time_access` + dropdown chọn bot) + regression impact.
