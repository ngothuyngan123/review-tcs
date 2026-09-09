# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39751 — [Profile sender] Không hiển thị avatar của profile bot gốc tại màn chat 1:1 trên web khi thực hiện chọn bot gốc (trường hợp bot gốc đã được update avatar)` |
| Redmine URL | https://redmine.watermelon.vn/issues/39751 |
| Auto-filled | `2026-08-25 by /new-task` |
| Ngày báo cáo | `2026-08-19` |
| Khách hàng / PM báo | `Đoàn Thị Bích Hảo` (tracker: **Bug tự detect** — QA tự phát hiện, không phải khách báo) |
| Module / Màn hình | `<chưa rõ — tester fill>` — Redmine **không set category**, không có custom field. Suy từ subject + Studio: Chat 1:1 trên web → hover tin đã gửi → avatar profile sender (bot gốc). Studio gắn `feature = chat-1on1`, `screen = Màn chat 1:1 web (SCR-CHT-01)`. |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` — description **không ghi môi trường**. Tester xác nhận bug phát hiện trên Dev / Staging / Production nào. |

> Thông tin bổ sung từ Redmine: status hiện tại = **Fix done - Đợi test** (chuyển bởi `AI LME Fix bug`, 2026-08-21 04:19 UTC) · assigned_to = **Đoàn Thị Bích Hảo** (đổi bởi Ngô Thúy Ngần ngày 2026-08-25) · project = Lme · tracker = Bug tự detect · start_date = 2026-08-19 · **không có attachment**, **không có relations**, parent issue = **#26684 `[LME] BUG NỘI BỘ TỰ DETECT`** (ticket gom nhóm, status Closed — không mang thông tin chức năng) · 2 journals.

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Pre-Conditions:
- User update avatar cho bot gốc => đã click button đồng bộ trên web
- Trên web chọn bot gốc => thực hiện gửi tin nhắn
- Trên app , chọn bot gốc => thực hiện gửi tin nhắn

Steps:
1. Quan sát khi hover vào tin nhắn trên web

Actuals:
1. Hiển thị avatar mặc định của bot gốc và không hiển thị avatar mới sau khi user update

Expected:
1. Sau khi click đồng bộ, các tin nhắn gửi bằng profile bot gốc thì đều phải update avatar khi hover vào
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

**Pre-Conditions (nguyên văn):**
- User update avatar cho bot gốc => đã click button đồng bộ trên web
- Trên web chọn bot gốc => thực hiện gửi tin nhắn
- Trên app , chọn bot gốc => thực hiện gửi tin nhắn

**Steps (nguyên văn):**
1. Quan sát khi hover vào tin nhắn trên web

## Expected result

- Sau khi click đồng bộ, các tin nhắn gửi bằng profile bot gốc thì đều phải update avatar khi hover vào

## Actual result

- Hiển thị avatar mặc định của bot gốc và không hiển thị avatar mới sau khi user update

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine `attachments` **rỗng** — không có ảnh / video / log đính kèm trong ticket.

## Ghi chú thêm của Leader

- **2 đường gửi tin trong Pre-Conditions**: description nêu **cả web lẫn app** đều chọn bot gốc gửi tin, nhưng Steps chỉ quan sát trên web. Dev fix chỉ chạm 2 chỗ dựng dữ liệu của **chat 1:1 web** — xem `03-dev-impact.md` mục 2 (Dev tự khai còn **3 chỗ cùng kiểu chưa sửa**: 2 chỗ hiển thị cho app điện thoại + nội dung trích dẫn). Leader cần chốt: tin gửi **từ app** hiển thị trên web có nằm trong scope test không.
- **Điểm mập mờ trong bug report**: "avatar mặc định của bot gốc" — cần tester xác nhận đây là *ảnh placeholder hệ thống* (`/images/avatar_bot_v2.png`) hay *ảnh snapshot cũ* của profile mặc định. Dev đánh giá đây là **2 nguyên nhân khác nhau** (snapshot cũ vs URL tương đối 404 → rơi về placeholder), quyết định phạm vi TC verify fix.
- **Không có attachment** → không có evidence hình ảnh của trạng thái lỗi. TC verify fix phải tự dựng data (bot đã đổi avatar + tin gửi trước khi đổi).
- Dev **CHƯA kiểm chứng thực nghiệm** (dev DB tắt, kết luận chỉ dựa trên đọc code) — xem mục 6 VERIFY ở `03-dev-impact.md`. Rủi ro sót case cao hơn bình thường.
