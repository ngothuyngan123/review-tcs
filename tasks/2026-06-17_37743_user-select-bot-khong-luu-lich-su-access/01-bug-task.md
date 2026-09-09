# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37743 — User đã login và select bot ngày hôm sau user vào đang không lưu lịch sử access` |
| Redmine URL | `https://redmine.watermelon.vn/issues/37743` |
| Auto-filled | `2026-06-17 by /new-task` |
| Ngày báo cáo | `2026-06-16` |
| Khách hàng / PM báo | `Do Van Tu TuDV` |
| Module / Màn hình | `<chưa rõ — tester fill>` (liên quan middleware access bot — `BasicAccess.php`) |
| Priority | `High` |
| Môi trường phát hiện | `<chưa rõ>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

_(Redmine description rỗng — bug chỉ có tiêu đề: "User đã login và select bot ngày hôm sau user vào đang không lưu lịch sử access". Đánh giá ảnh hưởng phía Dev nằm trong journal, xem `03-dev-impact.md`.)_

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

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
