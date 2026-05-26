# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `<e.g. LME-1234>` |
| Redmine URL | `<link nếu có, vd https://redmine.lme.jp/issues/36317>` |
| Auto-filled | `<chưa>` hoặc `YYYY-MM-DD by /new-task` |
| Ngày báo cáo | `YYYY-MM-DD` |
| Khách hàng / PM báo | `<tên>` |
| Module / Màn hình | `<e.g. Broadcast / Friend detail>` |
| Priority | `High / Medium / Low` |
| Môi trường phát hiện | `Production (step.lme.jp) / Staging (staging.lme.jp) / Dev (form.watermeru.com)` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

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
