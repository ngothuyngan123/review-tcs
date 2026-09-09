# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`), tạo folder mới + fill các section bên dưới (cùng với `03-dev-impact.md`).
> 2. **Paste tay** — nếu không có Redmine link, member paste nội dung task bug.
>
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL, môi trường phát hiện) tra thẳng trên Redmine khi cần, KHÔNG chép lại vào đây.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `<#40515 — [tiêu đề ticket]>` |
| Module / Màn hình | `<e.g. Info friend — 到達アクション của friend info>` |

## Mô tả bug (bản dịch tiếng Việt)

<!--
Dịch sát nội dung khách hàng báo sang tiếng Việt — KHÔNG tóm tắt, KHÔNG diễn giải lại.
Giữ nguyên thuật ngữ JP trong câu (vd 到達アクション, リッチメニュー), có thể chú thích VN trong ngoặc.
KHÔNG chép lại nguyên khối 原文 tiếng Nhật.
-->

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

<!-- List link attachment Redmine phía dưới nếu có. -->

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone, tần suất lỗi (100% hay xác suất),... nếu có -->

## Dữ liệu định danh ca lỗi

<!-- Dùng để dựng env test. Bỏ section này nếu ticket không có ca lỗi cụ thể. -->

| Mục | Giá trị |
|---|---|
| bot_id | `<...>` |
| Friend | `<tên — friend ID / line_user_id>` |
| Đối tượng cấu hình | `<tên + ID: friend info / action / template / richmenu...>` |
| Thời điểm lỗi | `<YYYY/MM/DD HH:MM:SS>` |
| Đối chứng | `<case chạy đúng để so sánh, nếu có>` |

## Journal / note từ Redmine (nguyên văn)

<!--
Chép nguyên văn journal/note có giá trị điều tra (log, SQL, ID, xác nhận của Dev/CS).
Bỏ qua journal chỉ đổi status / assignee.
Format: **Journal #<id> — <author> — <YYYY-MM-DD>:** rồi block ``` nội dung ```
-->
