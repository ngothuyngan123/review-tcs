# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43178 — [JOB] Forward webhook (#40475): tối ưu vòng quét callback_event / tag_history / friend_info_history` |
| Module / Màn hình | `Job nền — Forward webhook (JOB-*): vòng quét callback_event (Kênh 1) / tag_history + friend_info_history (Kênh 2)` |

## Mô tả bug (bản dịch tiếng Việt)

<!--
Đây KHÔNG phải bug khách hàng báo — là task Improve nội bộ do Dev tự phát hiện + tự đánh giá ảnh hưởng (xem 03-dev-impact.md). Không có section "Tái hiện bug" riêng trong Redmine, nội dung dưới đây = mô tả vấn đề (nguyên văn description, đã dịch sát) làm context chung.
-->

- Kênh 1: row `callback_event` webhook trùng (status `11`/`111`) bị câu quét loại ra nên `status_sync` mãi `NULL`. Row trùng tích tụ ở đầu dải `status_sync IS NULL`, mỗi vòng quét phải đi qua lại toàn bộ đống đó → câu quét chậm dần theo thời gian.
- Cả 2 kênh (Kênh 1 + Kênh 2 — tag_history / friend_info_history): mỗi batch có data đều nghỉ cố định (Kênh 1: 2s) → trần ~250 row/s, giờ cao điểm callback đổ vào nhanh hơn thì job forward trễ dần.

## Steps to reproduce

<!-- Input thiếu: Redmine KHÔNG có section "Tái hiện bug" (task Improve nội bộ, không phải bug report từ khách hàng) — để trống, không đoán. -->

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

<!-- Redmine #43178 không có attachment (0). -->

## Ghi chú thêm của Leader

- Đây là task **Improve nội bộ** (tracker = "Improve nội bộ"), không phải bug khách hàng báo — không có bước tái hiện cụ thể, root cause + cách fix do Dev tự nêu trong journal (xem `03-dev-impact.md`).
- Task liên quan trực tiếp đến **#40475** (ticket gốc tạo ra cơ chế forward webhook này) — nên đối chiếu thêm kho TC / spec của #40475 nếu có, để tránh viết trùng hoặc bỏ sót regression trên luồng chính.
- Vấn đề mang tính **hiệu năng/hành vi theo thời gian** (chậm dần theo khối lượng row tích tụ, trần throughput ~250 row/s) — khó verify bằng 1 lần chạy nhanh, cần dữ liệu test đủ lớn/đủ dồn tích để quan sát được triệu chứng trước khi so sánh với bản fix.
- Env ảnh hưởng: `callback_event`, `tag_history`, `friend_info_history` là bảng nóng — nên cân nhắc **không kết luận chỉ từ local/staging** (RULE-08) khi đánh giá throughput/giờ cao điểm.

## Dữ liệu định danh ca lỗi

<!-- Redmine không có ca lỗi cụ thể (không ghi bot_id / friend / thời điểm lỗi) — bỏ section theo hướng dẫn, chỉ giữ ghi chú định tính ở trên. -->
