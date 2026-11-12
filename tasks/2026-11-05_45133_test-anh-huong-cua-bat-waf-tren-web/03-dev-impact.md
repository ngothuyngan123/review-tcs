# 03 — Đánh giá ảnh hưởng từ Dev

⚠️ **INPUT THIẾU: Redmine #45133 KHÔNG có section "Đánh giá ảnh hưởng phía dev"** — description chỉ có 2 câu yêu cầu test, không phải báo cáo fix bug kèm đánh giá ảnh hưởng. `/write-tc` và `/review-tc` sẽ fail hoặc cho coverage sai nếu chạy với input này ở mục 1-4 dưới đây (toàn bộ đang là placeholder). Yêu cầu Dev/Leader bổ sung trước khi tiếp tục, HOẶC xác nhận: ticket này vốn **không gắn với 1 commit/PR cụ thể** (là re-test phạm vi hạ tầng WAF, không phải bug fix) — nếu vậy, coverage ở `/review-tc` nên dựa vào 28 `requirements` (REQ-001..017, REQ-101..111) mà Studio task #546 đã có sẵn (xem `task_get_context(task_id=546, sections=["requirements"])`) thay cho mục 4.1/4.2/4.3 thông thường.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` — Redmine không ghi Dev, assignee ticket là `Thanh Phương` (vai trò Tester trên Studio: `thanhntp`) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `<chưa rõ>` |
| Auto-filled | 2026-11-05 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ KHÔNG áp dụng bình thường được vì Section "Đánh giá ảnh hưởng" không tồn tại trong Redmine. Leader cần xác nhận hướng xử lý (xem cảnh báo INPUT THIẾU ở trên) trước khi tick.

---

## 1. Nguyên nhân

`<Input thiếu — Dev chưa cung cấp>`

Ghi chú: không phải "nguyên nhân bug" — đây là thay đổi hạ tầng (Infra bật WAF trên web) có khả năng chặn nhầm nghiệp vụ hợp lệ.

## 2. Cách fix

`<Input thiếu — Dev chưa cung cấp>` — không có "fix" vì không phải bug code; nếu phát sinh case bị chặn nhầm trong lúc test, cách xử lý thực tế sẽ là Infra tinh chỉnh rule WAF (whitelist/exception), không phải code fix.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu>` | | |
| 2 | | | |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Không có 4.1 từ Dev. Thay thế: 28 requirements REQ-001..017 (phạm vi form-answer) + REQ-101..111 (phạm vi mở rộng: auth, friend/tag, template, auto-reply/scenario, chat/broadcast, booking, rich menu, LP/popup/conversion, sales/billing, CSV/webhook/API, system-admin) do Studio task #546 soạn — xem 04-tc-list.md digest mục "requirement_keys". -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `<Input thiếu>` | | Direct / Indirect | Dùng 28 `REQ-*` của Studio task #546 thay thế — không phải function code cụ thể |

### 4.2. List data bị update khi fix bug

<!-- Không áp dụng — không phải bug fix có data migration. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu — không áp dụng>` | | |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Suy từ 28 requirements Studio: mọi tính năng có request POST/PUT/DELETE nội dung tự do (HTML/JS/CSS/ký tự đặc biệt) hoặc upload file đều có rủi ro bị WAF chặn nhầm. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Form-answer (tạo/sửa form, CSS·JS設定, custom HTML, trả lời khách, upload) | REQ-001..017 | High |
| T2 | Auth/session/chuyển bot/staff | REQ-101 | High |
| T3 | Friend list/info/tag | REQ-102 | High |
| T4 | Template (text/image/carousel) | REQ-103 | High |
| T5 | Auto-reply/scenario/action | REQ-104 | High |
| T6 | Chat 1:1/gửi hàng loạt/broadcast | REQ-105 | High |
| T7 | Salon/Lesson/Event booking | REQ-106 | High |
| T8 | Rich menu | REQ-107 | High |
| T9 | LP/QR/Popup/URL/Conversion | REQ-108 | High |
| T10 | Sales/billing/point | REQ-109 | High |
| T11 | CSV import/export, Webhook, API integration, My page, notify, cross-analysis | REQ-110 | High |
| T12 | System-admin (お知らせ, 機能紹介, ポップアップ設定, báo cáo) | REQ-111 | High |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix — **KHÔNG ĐẠT, Input thiếu**
- [ ] Mục 2 (cách fix) có thể trace về code — **KHÔNG ĐẠT, không áp dụng**
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — **KHÔNG ĐẠT, Input thiếu**
- [ ] Mục 4.1 không thiếu function (so với mục 3) — thay bằng 28 `REQ-*` Studio, Leader cần xác nhận đủ phạm vi
- [ ] Mục 4.2 không thiếu data — không áp dụng
- [ ] Mục 4.3 cover được cả happy path lẫn edge case — xem 12 nhóm tính năng T1-T12 trên
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev/Infra trước khi member viết TC (vd: rule WAF cụ thể là gì, ngưỡng body size, danh sách pattern bị chặn)
