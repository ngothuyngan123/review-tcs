# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#35578 — [Bill max friend] Bill max friend fail -> nhấn bill lại có nhập card mới thì khi bill success chưa tạo lịch sử change card` |
| Module / Màn hình | Bill phí theo lượng bạn bè (bill max friend) — màn **Lịch sử hợp đồng** (contract history), loại lịch sử đổi thẻ chính (change main card). Liên quan Contract Plan & Payment (FA-031), Payment History (FS-009). |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine chỉ có 1 dòng, không có section "Tái hiện bug" tách riêng — giữ nguyên văn. -->

Exp: Tạo được thêm 1 lịch sử change main card (đổi thẻ chính).

⚠️ Redmine không có section "Tái hiện bug" (Steps/Expected/Actual) tách riêng. Ngữ cảnh đầy đủ lấy từ Journal note (#131899) + báo cáo đánh giá ảnh hưởng của Dev (file 03): khi bill phí theo lượng bạn bè (bill max friend) **thất bại**, user bấm **bill lại** và **nhập thẻ mới** → bill thành công, hệ thống ghi đè thẻ chính của hợp đồng bằng thẻ mới nhưng **không** tạo bản ghi lịch sử đổi thẻ chính (change main card) trong màn lịch sử hợp đồng.

## Steps to reproduce

<!-- Không có trong Redmine description gốc — suy ra từ Journal #131899 + nguyên nhân Dev mô tả ở file 03. Member/Leader verify lại trước khi dùng để viết TC. -->

1. Tạo/chọn 1 hợp đồng (bot) đang bill phí theo lượng bạn bè (max friend) bị **fail** (ví dụ do bot vượt mốc 100.000 bạn và thẻ cũ bị lỗi thanh toán) → hợp đồng ở trạng thái `max_friend_plan=3` (đang bill lỗi).
2. Vào màn chi tiết hợp đồng, bấm **bill lại** phí theo lượng bạn bè, nhập **thẻ mới** (card mới).
3. Bill thành công (callback `handleCallbackBillMaxFriendSuccess`).
4. Mở màn **lịch sử hợp đồng** (contract history).

## Expected result

- Có đủ **2 dòng lịch sử**: (1) bill phí theo lượng bạn bè thành công, (2) **đổi thẻ chính** (change main card, type=11) với 4 số cuối + hãng thẻ mới.

## Actual result

- Chỉ có dòng lịch sử bill phí theo lượng bạn bè thành công — **thiếu** dòng lịch sử đổi thẻ chính, mặc dù `bot_contracts` đã bị ghi đè thẻ chính bằng thẻ mới (mã khách, 4 số cuối, hãng thẻ).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine issue #35578 không có attachment (0). -->

## Ghi chú thêm của Leader

- Ở trạng thái bill lỗi (`max_friend_plan=3`), nút đổi thẻ chính trên màn chi tiết hợp đồng bị **ẩn** (`detail-bill-fail.blade.php` dòng 108) → bấm **bill lại kèm nhập thẻ mới** là **đường duy nhất** để đổi thẻ ở trạng thái này, nên mất lịch sử ở đây là mất hẳn vết đổi thẻ (không có cách nào khác để trace lại).
- Dev **không tái hiện được trên dev** (MySQL `host.docker.internal:3306` connection refused) + kịch bản cần **bot trên 100.000 bạn** + **tài khoản Univapay thật** → fix dựa trên đọc code, chưa có bằng chứng chạy thật trên dev/staging. Theo RULE-11, đây **không phải bằng chứng hợp lệ** để tự tin coverage đã đủ — cần test thật trên môi trường có dữ liệu tương đương (xem cảnh báo RULE-08 ở file 03).
- Rủi ro Dev tự nêu (file 03): hợp đồng đang ở hình thức **chuyển khoản** mà user chọn trả phí theo lượng bạn bè bằng **thẻ** → thẻ chính hợp đồng cũng bị ghi đè → sau fix sẽ sinh thêm dòng lịch sử đổi thẻ (thay đổi hành vi so với trước, cần TC riêng). Tương tự, nhập lại **đúng thẻ cũ** vẫn sinh dòng lịch sử đổi thẻ.
- Yokoten Dev tự nêu: còn 1 chỗ cùng kiểu ghi đè thẻ chính chưa sửa (**gia hạn hợp đồng nhập thẻ mới** — re-contract) — **ngoài phạm vi ticket này**, chỉ ghi nhận.

## Journal / note từ Redmine (nguyên văn)

**Journal #131899 — Thanh Phương — 2026-08-21:**

```
Check lại ngày 21/8 vẫn chưa tạo lịch sử change main card (chỉ có lịch sử bill max friend success)
```
