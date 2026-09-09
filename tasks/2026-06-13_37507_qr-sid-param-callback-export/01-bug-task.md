# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37507 — [10-06-2026][QR Code]Giá trị của tham số động sid có được truyền sang Callback URL của Parameter Export hay không` |
| Redmine URL | `https://redmine.watermelon.vn/issues/37507` |
| Auto-filled | `2026-06-13 by /new-task` |
| Ngày báo cáo | `2026-06-12` |
| Khách hàng / PM báo | `Ngọc Ánh` |
| Module / Màn hình | `QR Landing` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `Production` (KH tái hiện trên `s.lmes.jp` — landing QR) |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Khi gắn tham số động như ví dụ dưới đây vào URL Action của QR Code, thì thông tin của tham số động đó có được gửi tới Callback URL của chức năng Export Parameter hay không?
Ví dụ:
https://s.lmes.jp/landing-qr/1657915967-2oy4rqWl?uLand=dC5cSJ&sid=<giá trị base64 thay đổi theo mỗi lần click>

https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B99HES3J7

**Bổ sung từ journal (Ngọc Ánh):**
- 10/6: Mặc dù phía Callback URL đang nhận được các thông tin cơ bản như tên LINE, địa chỉ email..., nhưng nếu chỉ riêng thông tin của tham số động không được gửi tới thì ngoài nguyên nhân: Phía Callback URL chưa implement xử lý nhận tham số động — còn có nguyên nhân nào khác có thể xảy ra hay không?
- 10/6: a Thắng báo lại khả năng nó chưa được triển khai là rất thấp.
- 11/6: Cụ thể, khách hàng cho biết đã truy cập vào QR Code Action 「メディア03」 vào lúc 2026-06-08 13:55. Tuy nhiên, phía Callback URL đã nhận được các thông tin như tên LINE, email..., nhưng lại không nhận được các tham số đã được gắn trên QR Code Action URL. Vì vậy, khách hàng muốn nhờ kiểm tra giúp: Tại thời điểm truy cập, URL thực tế có được gắn kèm các tham số đó hay không?

**Truy vấn DB tham chiếu (journal Thanh Duy Nguyen 13/6):**
`SELECT * FROM detail_landing_click WHERE landing_id = 458318`

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Từ Section "Tái hiện bug KH" (journal Kim Cúc 13/6). -->

1. QR landing: `https://s.lmes.jp/landing-qr/1657915967-2oy4rqWl?uLand=dC5cSJ&sid=<giá trị>` (URL Action gắn thêm tham số tự nhập, vd `sid`).
2. Detail landing → tab `パラメーターエクスポート` (Parameter Export): setting URL của request bin, **KHÔNG** setting `ucid={line_id}`, `{friend_type}`, `{friend_name}`, `{mail}` hoặc `{forward_param}`.
3. Friend quét landing → hệ thống tự động add all param `ucid` mặc định vào request bin.

## Expected result

- Các tham số động/tự nhập KH gắn trên QR Code Action URL (vd `sid`) **phải được forward** tới Callback URL (request bin) của chức năng Parameter Export.

## Actual result

- Những param KH tự nhập **không được** add vào request bin (Callback URL chỉ nhận các thông tin cơ bản: tên LINE, email...).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #37507 không có attachment. -->

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- Spec liên quan: QR Landing / Parameter Export (Callback URL request bin) → tham chiếu [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) section QR Code / Landing.
- `forward_param` là param chứa các tham số custom KH tự nhập trên URL Action; bug nằm ở case URL **không** setting param info nào → `forward_param` chưa được set vào URL callback.
