# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40164 — [Job callback] Add xử lý callback tin nhắn có source.type là loại room` |
| Redmine URL | https://redmine.watermelon.vn/issues/40164 |
| Auto-filled | `2026-08-26 by /new-task` |
| Ngày báo cáo | `2026-08-25` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set Category; Studio task #220 gắn `feature = chat`) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — description không nêu môi trường |
| Tracker / Status | `Bug KH` / `Fix done - Đợi test` |
| Dev assigned | `Thanh Duy Nguyen` |
| Base branch (theo description) | `release-t07-2026` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #40164. KHÔNG diễn giải lại. -->

Base branch: release-t07-2026

Hệ thống hiện đã xử lý được webhook từ LINE với 2 loại nguồn: user (chat 1-1) và group (group chat). Cần bổ sung xử lý cho loại thứ 3: room (multi-person chat) — hiện đang bị bỏ sót/không xử lý.
Lý do cần làm: Các room cũ (tạo trước LINE v10.17.0, ~05/10/2020) vẫn hoạt động và vẫn bắn webhook với source.type = "room". Nếu không xử lý, các event từ những room này sẽ bị bỏ qua hoặc gây lỗi.

2 điểm khác biệt cốt lõi cần lưu ý khi code:
1. Endpoint quản lý member tách riêng theo path /group/ vs /room/ → không dùng chung được, phải phân nhánh theo source.type.
2. Room không có Group Summary API (không có tên nhóm, không có icon) → mọi chỗ hiển thị/lưu "tên nhóm" phải có fallback cho room.

Các action cần làm
1. Webhook parsing / routing
Nhận diện source.type === "room", extract source.roomId.
Thêm "room" vào enum/validation của source type (đừng để rơi vào nhánh default/throw).
2. Xử lý các event trong room
join — OA được thêm vào room → khởi tạo record room (nếu có lưu).
leave — OA bị kick/rời room → cleanup/deactivate record room.
memberJoined / memberLeft — cập nhật thành viên room (nếu có tracking).
message, postback trong room → route giống group.
3. Gửi tin nhắn
Reply: dùng replyToken — không cần thay đổi, nhưng verify chạy đúng trong room.
Push: to = roomId khi source là room.
4. Xử lý "tên nhóm" cho room (khác biệt quan trọng)
Ở mọi nơi hiện đang gọi Group Summary để lấy tên/icon nhóm → với room không gọi API này.
Đặt fallback hiển thị (ví dụ "Multi-person chat" hoặc để trống + hiển thị roomId rút gọn).
Bảo đảm không crash khi field name/icon bị null với room.
5. UI / Admin (nếu có màn hình quản lý hội thoại)
Hiển thị đúng loại room (icon/label riêng, phân biệt với group).
Xử lý ô "tên nhóm" trống cho room.
6. Test
Unit test parse webhook payload source.type = "room".
Test resolve target ID ưu tiên đúng thứ tự.
Test push/reply vào room.
Test các event join/leave/memberJoined/memberLeft trong room.
Test fallback khi room không có tên/icon.
Regression: đảm bảo luồng user và group không bị ảnh hưởng.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống, xem cảnh báo ở "Ghi chú thêm của Leader". -->

## Expected result

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. -->

## Actual result

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40164 KHÔNG có attachment nào. -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.

<!-- Bổ sung từ /new-task (metadata Redmine, không phải suy diễn nội dung):
- Ticket dạng "Bug KH" nhưng nội dung description là **yêu cầu bổ sung xử lý** (add source.type = room), không phải bug report có steps tái hiện.
- Đánh giá ảnh hưởng của Dev nằm ở **journal #133002 (2026-08-26T02:58:39Z)**, KHÔNG nằm trong description → xem `03-dev-impact.md`.
- Redmine KHÔNG có "Link TCs" → bộ TC ở `04-tc-list.md` lấy từ MCP LME TEST STUDIO task #220 (45 TC do AI sinh).
- Điều kiện tiên quyết / account test / feature flag: <chưa có trong Redmine — Leader fill>.
-->
