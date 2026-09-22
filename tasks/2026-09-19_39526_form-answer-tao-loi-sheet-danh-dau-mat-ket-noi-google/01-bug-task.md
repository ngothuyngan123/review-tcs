# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39526 — Form answer sau khi kết nối google, nếu tạo lỗi sheet thì đánh dấu là mất kết nối google` |
| Module / Màn hình | Form Builder (FA-011) — màn danh sách biểu mẫu 回答フォーム (Form Answer) · liên kết Google スプレッドシート · job nền `form-answer:create-google-sheet` |

## Mô tả bug (bản dịch tiếng Việt)

Form answer (biểu mẫu) sau khi kết nối Google, nếu tạo sheet bị lỗi thì đánh dấu là mất kết nối Google.

## Steps to reproduce

<!-- Nguồn: Journal #137199 — Kim Cúc — 2026-09-19 (Section "Tái hiện bug") -->

1. Liên kết Google Sheet ở form.
2. Job đang chạy để liên kết Google Sheet (job nền tạo sheet cho từng form chưa chạy xong).
3. Vào Google để xóa quyền kết nối: https://myaccount.google.com/connections?

## Expected result

- <Ticket không ghi rõ — suy từ tiêu đề ticket> Khi job tạo sheet lỗi, bot bị đánh dấu **mất kết nối Google** → màn biểu mẫu hiện cảnh báo mời liên kết lại.

## Actual result

- Một số form chưa liên kết thành công thì bị mất kết nối (form không có sheet, nhưng màn biểu mẫu vẫn báo đang liên kết bình thường — theo mô tả nguyên nhân của Dev ở file 03).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine không có attachment. -->

## Ghi chú thêm của Leader

- Tracker: **Bug tự detect** (không phải khách báo). Status hiện tại: `Fix done - Đợi test`.
- Điều kiện tiên quyết: bot phải **liên kết Google Sheet thật** (OAuth Google thật). Dev ghi: **không tái hiện được trên dev** (dev không có tài khoản Google liên kết) → nhánh thành công / luồng revoke quyền thật cần staging.
- Cách tái hiện thực tế: thu hồi quyền ứng dụng tại https://myaccount.google.com/connections trong khoảng giữa lúc liên kết xong và lúc job nền (chạy **mỗi phút**) tạo xong sheet cho các form.
- Fix có **2 lần commit**: `8748629bbd` (2026-08-19 — lỗi ⇒ cờ = 0) và `88307c747a` (2026-09-19 — thành công mà cờ đang 0 ⇒ bật lại 1). Xem file 03.

## Journal / note từ Redmine (nguyên văn)

<!-- Journal #129266 và #137196 (báo cáo AI auto-fixbug) đã tách vào 03-dev-impact.md. -->

**Journal #137199 — Kim Cúc — 2026-09-19:**
```
Tái hiện bug:
1. Liên kết gg sheet ở form
2. Job đang chạy để liên kết gg sheet
3. Thực hiện vào gg để xóa quyền kết nối: https://myaccount.google.com/connections?

Hiện tượng: 1 số form chưa liên kết thành công thì bị mất kết nối
```
