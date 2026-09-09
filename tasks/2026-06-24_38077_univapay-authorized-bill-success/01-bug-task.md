# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38077 — Status authorized trả về khi bill univapay sẽ coi là trường hợp bill success` |
| Redmine URL | `https://redmine.watermelon.vn/issues/38077` |
| Auto-filled | `2026-06-24 by /new-task` |
| Ngày báo cáo | `2026-06-24` |
| Khách hàng / PM báo | `Do Van Tu TuDV` |
| Module / Màn hình | `<chưa rõ — tester fill>` (liên quan Bill/Univapay payment, Lesson booking, Bill item) |
| Priority | `Medium` |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Redmine description để trống. Subject: "Status authorized trả về khi bill univapay sẽ coi là trường hợp bill success".

(Bug không có phần mô tả/tái hiện trong Redmine. Root cause + cách fix do Dev confirm qua "Đánh giá ảnh hưởng" — xem `03-dev-impact.md`.)

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

⚠️ Bug không tái hiện được trong Redmine (description trống, không có Section "Tái hiện bug") — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (univapay status `authorized` được coi là bill thành công) + regression impact lên job cover webhook timeout (booking lesson + bill item chu kỳ / 1 lần).
