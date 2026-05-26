# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | #36437 — Khi bật xác thực 2 lớp, logout -> login lại, đang chưa select bot đã chọn trước đó |
| Redmine URL | https://redmine.watermelon.vn/issues/36437 |
| Auto-filled | 2026-05-15 by /new-task |
| Ngày báo cáo | 2026-05-15 |
| Khách hàng / PM báo | Ngọc Ánh |
| Module / Màn hình | `<chưa rõ — tester fill>` (Login flow với 2FA) |
| Priority | Medium |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

Expect: Hiển thị bot đã select trước đó

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Select bot A
2. Bật xác thực 2 lớp
3. Logout -> Login lại

## Expected result

- Hiển thị bot đã select trước đó

## Actual result

- NG: chưa select bot đã chọn trước đó (redirect về màn list bot)

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments:
- [Screenshot 2026-05-15 144200.png](https://redmine.watermelon.vn/attachments/download/25765/Screenshot%202026-05-15%20144200.png)

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->
