# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39008 — Modal liên kết Google calendar` |
| Module / Màn hình | `Salon Booking (FA-020) — modal cảnh báo mất kết nối Google Calendar ở màn chi tiết lịch salon (calendar_salon/detail.blade.php)` |

## Mô tả bug (bản dịch tiếng Việt)

Đổi text thành:
再連携せずにこの画面を閉じる => Googleカレンダー接続設定をリセットする (Đặt lại cài đặt kết nối Google Calendar)

Đồng thời, khi thực hiện thao tác này, bắt buộc hủy kết nối Google Calendar của staff tương ứng.
Khi click button reset, hiển thị modal confirm: https://docs.missiona.co/product_lme/gcal-disconnect-reset.html
Tài khoản login html: missiona58174/Vk3mPwRn7xQe
Github: https://github.com/missiona-inc/prototype-lme/blob/main/gcal-disconnect-reset.html

Link task: https://missiona-tools.vercel.app/lme-dev/tickets/af56313e-1b3c-4cf9-8b6e-48a0c52fb23b

## Steps to reproduce

<!-- Ticket tracker = SpecImprove (yêu cầu cải tiến UI/UX), không phải bug reproduction — Redmine không có section "Tái hiện bug". -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/28530/e9b02ab2-e52a-413f-8ba4-a4501e01ec89.png

## Ghi chú thêm của Leader

⚠️ Ticket không tái hiện được vì đây là **SpecImprove** (yêu cầu cải tiến giao diện), không phải bug — không có Steps to reproduce/Expected/Actual từ khách hàng. Nội dung yêu cầu + cách fix đã có sẵn trong journal Dev dạng cấu trúc đầy đủ (xem `03-dev-impact.md`).

Trang thiết kế modal confirm tham khảo: https://docs.missiona.co/product_lme/gcal-disconnect-reset.html (login: `missiona58174` / `Vk3mPwRn7xQe`) — bám đúng bố cục: biểu tượng cảnh báo + tiêu đề + cảnh báo "lịch trên hệ thống sẽ bị xóa" + 2 nút Đóng / Đặt lại cài đặt (màu đỏ).

Có **2 lần fix** cho cùng ticket:
- Journal #130742 (2026-08-20) — branch `ai_fixbug_39008` trên base `release_step_20260623` — bản fix ban đầu, chỉ đổi text + gọi endpoint reset (không có modal xác nhận riêng).
- Journal #139439 (2026-09-30, **mới nhất, đang active**) — branch `ai_small_39008`, dựng lại trên base `release_step_20260930` (base cũ đã trễ 2 release) — bổ sung modal xác nhận đúng design, tách hàm dùng chung `unlinkGoogleCalendarOfStaff`, xử lý conflict mã lỗi 500→422 giữa 2 release.
- **File `03-dev-impact.md` dùng nội dung của Journal #139439 (bản mới nhất/active)** vì Commit Date custom field = 2026-09-30 khớp với journal này, status hiện tại = `Fix done - Đợi test`.

Dev **không verify được trên dev** vì MySQL dev (`host.docker.internal:3306`) từ chối kết nối lúc chạy — mức verify chỉ dừng ở lint/compile/route/reflection, **chưa test runtime thật**.

## Journal / note từ Redmine (nguyên văn)

<!-- Journal #130742 và #139439 là báo cáo AI auto-fixbug dạng "Đánh giá ảnh hưởng" (4 mục cấu trúc) — đã chuyển nguyên văn sang 03-dev-impact.md thay vì lặp lại ở đây. Journal #137398 (2026-09-21) chỉ đổi trạng thái Dashboard (PM duyệt → Đã đóng), không có giá trị điều tra — bỏ qua. -->
