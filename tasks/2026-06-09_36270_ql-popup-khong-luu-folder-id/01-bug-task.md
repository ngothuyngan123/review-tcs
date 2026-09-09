# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36270 — [QL Popup] Sau khi tạo item thì ko lưu lại folder_id đã tạo trước đó nên đang bị back về folder default` |
| Redmine URL | `https://redmine.watermelon.vn/issues/36270` |
| Auto-filled | `2026-06-09 by /new-task` |
| Ngày báo cáo | `2026-05-05` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` |
| Module / Màn hình | `Quản lý popup (/basic/popup-manager)` |
| Priority | `Medium` |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Fix triển khai khang các màn hình sau:
Quản lý popup: /basic/popup-manager

> Tái hiện + đánh giá ảnh hưởng (nguyên văn từ journal Dev Hạnh Nguyễn, #36270):
>
> Hiện tượng: Sau khi tạo popup thành công ở folder khác folder default, ra màn list thì focus hiển thị trỏ về folder default `未分類` thay vì giữ folder vừa thao tác.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Tạo 1 popup ở folder khác folder default
2. Nhấn save => tạo thành công

## Expected result

- Sau khi tạo thành công ra màn list, cần hiển thị folder trước đó đã thao tác (giữ đúng folder vừa tạo item).

## Actual result

- Sau khi tạo thành công ra màn list, focus hiển thị trỏ về folder default `未分類`.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->
