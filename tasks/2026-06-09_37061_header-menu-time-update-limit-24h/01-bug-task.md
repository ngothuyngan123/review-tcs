# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37061 — [Header/Menu] Hiển thị thời gian cập nhật limit và hiển thị theo định dạng 24h` |
| Redmine URL | `https://redmine.watermelon.vn/issues/37061` |
| Auto-filled | `2026-06-09 by /new-task` |
| Ngày báo cáo | `2026-06-04` |
| Khách hàng / PM báo | `Hạnh Nguyễn` |
| Module / Màn hình | `Header / Menu (hiển thị thời gian cập nhật limit)` |
| Priority | `Medium` |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Actual:
- Hiện tại đang fix cứng việc để time update là 00:01
- Hiện tại đang hiển thị theo định dạng 12h (vd 5h chiều vẫn là 5h)

Expect:
- Cần hiển thị đúng time đã update khi change bot, add bot, click btn load lại thông tin bot và vào màn summary message send,...
- Đổi thành định dạng 24h

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine không cung cấp steps cụ thể. Tester bổ sung dựa trên Actual/Expect. -->

1.
2.
3.

## Expected result

- Hiển thị đúng thời gian đã update (không fix cứng 00:01) khi: change bot, add bot, click btn load lại thông tin bot, vào màn summary message send,...
- Hiển thị theo định dạng 24h (vd 5h chiều → 17h).

## Actual result

- Time update đang bị fix cứng là 00:01.
- Đang hiển thị theo định dạng 12h (vd 5h chiều vẫn hiển thị là 5h).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Redmine không có "Steps to reproduce" rõ ràng — chỉ có Actual/Expect. Bug liên quan hiển thị thời gian → tester cần chú ý **timezone** khi verify định dạng 24h.
