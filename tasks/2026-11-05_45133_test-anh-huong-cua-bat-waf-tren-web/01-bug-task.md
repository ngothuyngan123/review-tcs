# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45133 — Test ảnh hưởng của bật WAF trên web` |
| Module / Màn hình | `<chưa rõ — tester fill>` — ticket **không phải bug 1 màn hình cụ thể**, mà là re-test phạm vi **toàn hệ thống web admin** sau khi Infra bật WAF (Web Application Firewall). Studio xếp feature chính `form-answer` nhưng bộ TC (xem file 04) trải khắp ~37 màn hình khác nhau (chat, friend list, tag, template, rich menu, salon/lesson, billing, CSV import/export, webhook, system-admin...). |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Nguyên văn description, KHÔNG diễn giải lại. Ticket này là YÊU CẦU TEST (tracker = Test), không phải báo bug cụ thể. -->

Từ kho test case có sẵn dự án. Sử dụng những testcase tính năng cơ bản sử dụng bình thường.
Bổ sung những case nhạy cảm có khả năng WAF chặn, thì vẫn phải sử dụng bình thường. Ví dụ các từ khóa khi post gần giống XSS, SQLinjection, tính năng submit nội dung có html, js, css.

## Steps to reproduce

<!-- Không có — ticket không phải case bug cụ thể, không có bước tái hiện. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #45133 không có attachment (Attachments (0)). -->

## Ghi chú thêm của Leader

⚠️ **Đây KHÔNG phải bug report** — tracker Redmine là `Test`, không phải `Bug`. Ticket yêu cầu **re-test phạm vi** (regression) toàn bộ tính năng cơ bản của web admin sau khi Infra bật WAF, cộng thêm các case "nhạy cảm" có khả năng bị WAF chặn nhầm (XSS-like, SQL injection-like, submit nội dung HTML/JS/CSS, upload file, v.v.) — mục tiêu là xác nhận WAF **không chặn nhầm** nghiệp vụ hợp lệ, trong khi vẫn phải chặn đúng các request thật sự nguy hiểm.

- Không có Section "Đánh giá ảnh hưởng phía dev" trong Redmine (ticket không gắn với 1 fix code cụ thể) → xem cảnh báo INPUT THIẾU ở `03-dev-impact.md`.
- Bộ TC (274 TC) đã được AI sinh sẵn trên **MCP LME TEST STUDIO** (task #546, round 1, status `tc-ready`), dựa trên 28 requirements (`REQ-001..017`, `REQ-101..111`) do `thanhntp` biên soạn trực tiếp trên Studio — xem digest ở đầu `04-tc-list.md`. **Chưa TC nào được chạy** (`exec.untested = 274/274`).
- Requirements trên Studio cho thấy phạm vi rộng hơn mô tả Redmine gốc nhiều: không chỉ form-answer mà còn auth/session, friend/tag, template, auto-reply/scenario, chat/broadcast, salon/lesson/event booking, rich menu, LP/QR/popup/conversion, sales/billing, CSV/webhook/API integration, và system-admin.
- **RULE-08**: toàn bộ 274 TC hiện `env_scope = (chưa chạy)` — khi chạy thật, case liên quan rate-limit/WAF thật (`REQ-017`, `NEW-20`...) **phải chạy được trên staging/prd**, không thể kết luận chỉ từ local/dev vì WAF là hạ tầng chỉ có ở môi trường thật.
- **5 mã quan điểm Studio dùng KHÔNG có trong `framework/checklist-lme.md`**: `SEC-INJECT-001` (33 TC) · `SEARCH-001` (16 TC) · `AUTH-SESSION-001` (10 TC) · `API-CONTRACT-001` (9 TC) · `RULE-09` (1 TC) → `/review-tc` sẽ không map được coverage cho các mã này, cần Leader lưu ý khi review.

## Dữ liệu định danh ca lỗi

<!-- Bỏ — ticket không có ca lỗi cụ thể, là yêu cầu test phạm vi rộng. -->
