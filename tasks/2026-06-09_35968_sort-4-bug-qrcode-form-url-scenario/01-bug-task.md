# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#35968 — [Sort folder, sort tên] Check 4 bug sort ở các màn qrcode, form, template, url, cross , scenario` |
| Redmine URL | https://redmine.watermelon.vn/issues/35968 |
| Auto-filled | `2026-06-09 by /new-task` |
| Ngày báo cáo | `2026-04-18` |
| Khách hàng / PM báo | `Kim Cúc` |
| Module / Màn hình | `Sort item/folder — các màn: QR code, Form answer, Message template, URL, Cross analysis, Scenario` (suy từ subject; Redmine không set category) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine description không ghi env; fix verify trên Staging — xem file 03) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

bug 1: Khi tag A đứng ở vị trí thứ 2 click sort => không phản hồi
bug 2: Khi nhấn sort ở tag A vị trí số 2 thì lại bị di chuyển lên trên
bug 3: Tag ở vị trí số 2 nhưng nút sort lên bị disable
bug 4: Tag ở dưới cùng vẫn hiển thị nút sort xuống dưới

## Tester verify (chỉ khi auto-fill từ Redmine)

- [x ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" có cấu trúc Steps/Expected/Actual. 4 bug ở trên là mô tả triệu chứng. -->

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

<!-- Redmine #35968 không có attachment. -->

## Ghi chú thêm của Leader

⚠️ Bug không có steps tái hiện cấu trúc trong Redmine — mô tả gốc chỉ liệt kê 4 triệu chứng (lấy từ màn Tag, là màn mẫu đã fix trước). Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03): desync giữa jQuery UI sortable (kéo-thả) và Vue `v-for` (thiếu `:key="item.id"` + không cập nhật lại mảng dữ liệu Vue sau kéo-thả). Ticket này là **横展開 (triển khai ngang)** áp mẫu fix màn Tag sang 6 màn: QR code, Form, Message template, URL, Cross analysis, Scenario. TCs nên tập trung verify cách fix (4 triệu chứng bug 1-4) trên cả 6 màn + regression sort.
