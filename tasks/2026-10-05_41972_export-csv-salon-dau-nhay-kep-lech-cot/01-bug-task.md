# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41972 — [JOB] Export csv salon  fix bug tên user có dấu nháy kép không bị lệch cột.` |
| Module / Màn hình | Job xuất CSV lịch sử đồng bộ salon ↔ Google Calendar (`HandleExportSalonCalendarTask`) — Dev xác nhận cùng lỗi tồn tại ở `HandleExportCsvTask` (job xuất CSV danh sách bạn bè) |

## Mô tả bug (bản dịch tiếng Việt)

Xuất CSV lịch sử sync salon (`HandleExportSalonCalendarTask`): Tiêu đề sự kiện Google và tên LINE user được đưa thẳng vào dòng CSV mà không escape → khi tên/tiêu đề chứa dấu nháy kép (`"`), mở file CSV sẽ bị **lệch cột**.

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

<!-- Redmine #41972 không có attachment (0). -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được theo format Steps/Expected/Actual trong Redmine — ticket chỉ có mô tả ngắn + root cause đã được Dev tự confirm qua đánh giá ảnh hưởng (xem file 03, nguồn: Journal #139898). TCs nên tập trung verify cách fix (escape `"`, xử lý giá trị `null`) + regression impact trên cả 2 job (`HandleExportSalonCalendarTask`, `HandleExportCsvTask`).

## Journal / note từ Redmine (nguyên văn)

<!-- Journal #139898 chính là nội dung "Đánh giá ảnh hưởng phía dev" — đã chuyển nguyên văn vào file 03-dev-impact.md, không lặp lại ở đây. -->
