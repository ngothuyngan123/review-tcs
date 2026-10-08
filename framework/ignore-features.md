# Danh sách tính năng IGNORE — tính năng / hàm cũ LME đã bỏ

> Dùng bởi `/review-tc` (BƯỚC 1 mục 4 + BƯỚC 4c `CONF-IGNORE`).
> Tính năng trong danh sách này **đã không còn dùng** trên LME, nên:
> - không tính vào coverage ở §1 / §2 (kể cả khi diff vẫn sửa file của nó);
> - Dev ghi nó trong đánh giá ảnh hưởng → báo ở **§4 report** (`CONF-IGNORE`);
> - TC đang có trên test tool cho nó → đề nghị **xóa**;
> - **KHÔNG** đề xuất TC bổ sung (§7) cho nó.
>
> Thêm dòng mới khi Leader xác nhận 1 tính năng đã bỏ. Cột `Nhận diện` phải đủ cụ thể để grep được (file, class, route, tên màn).

| # | Tính năng | Nhận diện (file · class · route · màn hình · từ khoá) | Ghi chú | Ngày thêm | Người chốt |
|---|---|---|---|---|---|
| IG-01 | Booking Manager cũ (lịch đặt chỗ kiểu cũ) | `app/Http/Controllers/Basic/BookingManagerController.php` · class `BookingManagerController` (mọi method, vd `ajaxFilterBookingByCondition`, `getListTimeBlockByCondition`) · route `booking_manager/*`, `filter-booking-by-condition` · màn 「カレンダー予約」 cài đặt lịch kiểu cũ · Dev hay ghi "Booking manager (outside glossary)" | Thay bằng Lesson Booking (FA-019) / Salon Booking (FA-020). Ví dụ đã gặp: #41996 (F9 / T10, Studio NEW-31) | 2026-10-06 | Leader |
