# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-id>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`), tạo folder mới + fill các section bên dưới (cùng với `03-dev-impact.md`).
> 2. **Paste tay** — nếu không có Redmine link, member paste nội dung task bug.
>
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL, môi trường phát hiện) tra thẳng trên Redmine khi cần, KHÔNG chép lại vào đây.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41964 — [02-10-2026][T12307][Lesson] Đặt lịch lesson do admin đăng ký trên màn quản trị thêm dòng vào Google Spreadsheet nhưng cột L–P bị trống (đặt qua link form thì bình thường), phát sinh khoảng 2 tuần nay.` |
| Module / Màn hình | Lesson — Đặt lịch bài học (レッスン予約), liên kết Google Spreadsheet (calendar / lesson booking sync sheet) |

## Mô tả bug (bản dịch tiếng Việt)

Khách hàng (aichikankyocenter@gmail.com, Bot: 株式会社A.CE) hiện đang sử dụng tính năng 「レッスン予約」(đặt lịch bài học) của L Message, có liên kết với Google Spreadsheet.

Vấn đề hiện tại là: khi đăng ký đặt lịch lesson của L Message **từ màn hình quản trị** (Google Chrome), dòng được thêm vào spreadsheet nhưng 「các cột L〜P không được phản ánh (để trống)」.

Còn khi thêm từ **form đặt lịch** (qua link đặt lịch) thì được phản ánh đầy đủ vào spreadsheet.

Vấn đề này trước đây không có, nhưng đột ngột phát sinh từ khoảng 2 tuần trước. Khách hàng không hề chỉnh sửa cài đặt hệ thống.

Spreadsheet liên quan: https://docs.google.com/spreadsheets/d/15PTm4_8oNg1iUvd99W61WPXn6qoRXHyp9Dcxat6tuoQ/edit?usp=sharing

Chức năng: Đặt lịch lesson (レッスン予約)

## Steps to reproduce

<!-- Redmine issue không có heading "Tái hiện bug" / "再現手順" / "Steps to reproduce" riêng — description chỉ mô tả hiện tượng (xem "Mô tả bug" trên). Xem BƯỚC 1.4 (Studio NEW-10) để có kịch bản tái hiện cụ thể do AI dựng lại từ dev-impact. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, Redmine không có file đính kèm. Spreadsheet khách gửi (link ở trên) không phải attachment Redmine. -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được bằng steps rõ ràng trong Redmine (chỉ có mô tả hiện tượng từ khách, không có "Tái hiện bug" section) — root cause đã được Dev confirm qua đánh giá ảnh hưởng (xem `03-dev-impact.md`). TCs nên tập trung verify cách fix + regression impact; kịch bản tái hiện cụ thể dựng lại ở TC Studio `NEW-10` (xem `04-tc-list.md`).

- Tần suất lỗi: theo khách báo là **100%** với mọi booking đặt từ màn quản trị có form câu hỏi ẩn/tắt ở giữa (không phải lỗi xác suất) — phát sinh liên tục ~2 tuần trước khi report (từ khoảng giữa tháng 9/2026).
- Nguồn báo: Tayori task #12307 (操作方法に関するお問い合わせフォーム) → WSSJ đã tạo ticket Slack xác nhận bug KH (xem Journal #139820).
- Dashboard CS: https://dashboard.melonglobal.net/css-analytics/?id=T12307

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `186535` |
| Friend | `<không có — lỗi không gắn 1 friend cụ thể, lỗi ở tầng đồng bộ sheet của booking bất kỳ đặt từ admin>` |
| Đối tượng cấu hình | `calendar_id: 8442` (lịch 「レッスン予約」đang liên kết Spreadsheet `15PTm4_8oNg1iUvd99W61WPXn6qoRXHyp9Dcxat6tuoQ`) |
| Thời điểm lỗi | Phát sinh liên tục từ khoảng giữa tháng 9/2026 (khách báo "~2 tuần trước" tính đến 2026-10-02) |
| Đối chứng | Booking đặt qua **link form đặt lịch** (không qua màn quản trị) → sheet ghi đầy đủ cột L–P, không lỗi |

## Journal / note từ Redmine (nguyên văn)

**Journal #139819 — Ngọc Ánh — 2026-10-02:**

```
bot_id: 186535
calendar_id: 8442
```

**Journal #139820 — AI bug detect Lme — 2026-10-02:**

```
Đã Add DB CS + thread OEM đã lên Slack → xác nhận Bug.
Đổi tracker "Bug KH cần xử lý nội bộ" → "Bug KH".
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C670DTZJA
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1790940127546099
```

<!-- Journal #139997 (Thanh Duy Nguyen, 2026-10-05) là "Đánh giá ảnh hưởng phía dev" đầy đủ — đã chuyển nguyên văn vào 03-dev-impact.md, không lặp lại ở đây. -->
