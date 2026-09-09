# 01 — Bug Task từ khách hàng

> **Nguồn**: Redmine #38962 — auto-fill bằng `/new-task` từ MCP Redmine (description + journal `133115`).
> ⚠️ Ticket dạng **「Bug tự detect」** (audit bảo mật nội bộ), KHÔNG phải bug do khách hàng báo → không có luồng tái hiện của khách.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38962 — IDOR đọc: getBroadcastLimitAlert lấy broadcast theo id không scope bot [S5]` |
| Redmine URL | https://redmine.watermelon.vn/issues/38962 |
| Auto-filled | `2026-09-03 by /new-task` |
| Ngày báo cáo | `2026-07-22` |
| Khách hàng / PM báo | `Tuấn Anh Trần` (tracker **Bug tự detect** — audit nội bộ, không phải KH) |
| Module / Màn hình | `Broadcast (FA-008)` — API `getBroadcastLimitAlert` phục vụ modal cảnh báo vượt hạn mức gửi ở màn tạo/sửa tin gửi hàng loạt. ⚠️ Redmine **không có** field category/Module — giá trị này suy từ description (`TemplateV2Controller`) + Studio `feature = broadcast`; tester xác nhận lại. |
| Priority | `Medium` (Redmine priority = `Normal`) — ⚠️ nhưng ticket tự gắn nhãn **`[S5]`** ở tiêu đề và bản chất là **lỗ hổng phân quyền cross-bot (IDOR)**; Leader cân nhắc nâng mức rủi ro khi giao TC. |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi>`. Manh mối duy nhất: *"Human Note: checkout từ branch release_staging_20260704"*; Dev fix trên base `release_step_20260805`. |
| Trạng thái Redmine | `Fix done - Đợi test` · assigned_to = `Ngô Thúy Ngần` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description Redmine #38962. KHÔNG diễn giải lại. -->

```
app/Http/Controllers/Basic/TemplateV2Controller.php:1051
BroadCast::where('id',$broadcastId)->value('filter_number' / 'template_ids') theo broadcast_id client gửi, không where('bot_id',$botId). Route ajax check_login không kiểm ownership ⇒ dò broadcast_id để lộ số người nhận + template_ids của bot khác.
Đề xuất: Thêm ->where('bot_id',$botId) cho BroadCast (và Template con); 404/403 nếu không thuộc bot hiện tại.

Human Note: checkout từ branch release_staging_20260704
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- ⚠️ Redmine KHÔNG có section "Tái hiện bug" / "再現手順". Description chỉ mô tả lỗ hổng ở tầng code. -->
<!-- Luồng khai thác dưới đây là Claude SUY RA từ description — tester phải verify lại trước khi dùng làm oracle. -->

1. Đăng nhập bằng tài khoản chỉ có quyền trên **bot A**, chọn bot A ở màn chọn bot.
2. Dùng chính phiên đó, gọi route ajax `templateV2.getBroadcastLimitAlert` (`GET /ajax/template-v2/get-broadcast-limit-alert`) với `broadcast_id` là mã của một tin gửi hàng loạt **thuộc bot B** (bot của tài khoản khác).
3. Đọc phản hồi.

## Expected result

- Yêu cầu bị từ chối (403 / 404), **không** trả về bất kỳ số liệu nào của bot B.

## Actual result

- (Trước khi fix) Trả về **số người nhận** (`filter_number`) và **danh sách mẫu tin** (`template_ids`) của tin gửi thuộc bot B ⇒ dò tuần tự `broadcast_id` là lộ dữ liệu của mọi bot khác.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine #38962 **không có attachment nào** (`attachments = []`).

## Ghi chú thêm của Leader

⚠️ **Bug không có luồng tái hiện từ khách trong Redmine** — đây là bug tự detect qua đọc code; root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix (cổng 403 theo bot)** + **regression luồng đăng ký tin gửi hợp lệ của chính bot**.

⚠️ **Lớp lỗi hệ thống, không phải lỗi đơn lẻ** — Dev ghi rõ ở mục 2: *"còn nhiều chỗ cùng kiểu đọc/ghi tin gửi theo mã thô ở BroadcastV2Controller / BroadcastController / ChatController, chưa sửa vì ngoài phạm vi ticket"*, và nhóm route ajax chỉ có `check_login` + `check_remember_token`, **không có cổng phân quyền theo bot**. Leader cân nhắc mở ticket riêng cho phần quét ngang này.

⚠️ **Ticket cha**: #38803 (tracker Feature) — Dev không gộp fix vào ticket cha, fix nằm ở branch riêng `ai_fixbug_38962`.
