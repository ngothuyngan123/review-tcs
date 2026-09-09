# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#33762 — [Lesson] [Remind send sau khi kết thúc booking] Remind type ngày có day =0 khi add remind đang bị tính theo time start booking` |
| Module / Màn hình | Lesson / Calendar Booking (FA-019) — màn cấu hình remind 「予約前後に送るリマインドメッセージ」, khối 「コース終了後のメッセージ・アクション」 (remind gửi SAU khi kết thúc booking) |

## Mô tả bug (bản dịch tiếng Việt)

Remind loại send sau có setting send vào ngày 0 lúc 15:00.
Time của booking là ngày 17/1 12:00 - 17:00.

<!-- Nguyên văn Redmine (đã là tiếng Việt, giữ nguyên không dịch lại). -->

## Steps to reproduce

1. Vào lịch đặt bài học (lesson), tạo/lấy một booking có time là **ngày 17/1, 12:00 - 17:00**.
2. Thêm remind loại **send sau (khi kết thúc booking)** với setting **send vào ngày 0, lúc 15:00**.
3. Kiểm tra bảng `event_step_time` xem remind có được add hay không.

<!-- Redmine không tách heading "Steps"; 3 bước trên suy trực tiếp từ 2 dòng setting + dòng Bug/Exp trong description. -->

## Expected result

- Remind day 0 lúc 15:00 **KHÔNG** được add vào `event_step_time`, do có time < time end của booking (15:00 < 17:00).

## Actual result

- Remind day 0 lúc 15:00 **vẫn được add** vào bảng `event_step_time`.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #33762 không có attachment nào. -->

## Ghi chú thêm của Leader

- Ticket tracker = **`Bug tự detect`** (không phải khách hàng báo) — người tạo: Thanh Phương, ngày 2026-01-16.
- Status hiện tại: **`Fix done - Đợi test`**. Fix do hệ thống **AI Auto-fixbug LME** thực hiện (journal 2026-08-26), branch `ai_fixbug_33762`, commit `b25cd9f78b`, 2 file / 2 dòng đổi.
- Ticket con của **#26684**.
- Redmine **KHÔNG ghi môi trường phát hiện**. Dev **chưa kiểm chứng bằng DB dev** (kết nối `host.docker.internal:3306` bị từ chối) và **chưa chạy unit test** — mức verify chỉ đạt `lint` + `git diff --stat`. ⚠️ Đây là điểm cần TC thực chứng bù lại.
- ⚠️ **Có dữ liệu sai còn tồn** (mục 5 RECOVER DATA của file 03): bản ghi `event_step_time` sai tạo TRƯỚC bản vá vẫn còn và **vẫn sẽ được job gửi sớm**. Bản vá chỉ chặn ghi mới, không dọn dữ liệu cũ.
- ⚠️ **Ngoài phạm vi ticket** (Dev tự khai): luồng **CẬP NHẬT** remind (cả lesson lẫn salon) vốn **thiếu hẳn** kiểm tra này, và màn đặt hẹn bản cũ. Luồng đặt lịch **salon** đã đúng sẵn từ trước.
- Bug tái hiện **100%** theo mô tả (lỗi logic so sánh, không phải xác suất).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Booking mẫu | Ngày **17/1**, khung **12:00 - 17:00** |
| Cấu hình remind | Loại **gửi sau khi kết thúc**, kiểu **ngày**, `day = 0`, giờ **15:00** |
| Bảng dữ liệu quan sát | `event_step_time` (nối `event_step` → `events.type=4` → `calendar_course_bookings` → `calendar_course_receptions`) |
| Đối chứng | Luồng đặt lịch **salon** — đã so đúng với giờ KẾT THÚC từ trước, dùng làm chuẩn so sánh |
| bot_id / friend / line_user_id | `<Redmine không cung cấp — tester tự dựng>` |

## Journal / note từ Redmine (nguyên văn)

- **Journal #120857 — Ngô Thúy Ngần — 2026-06-10:** chỉ đổi `tracker_id` 9 → 14, không có notes → bỏ qua.
- **Journal #133036 — AI LME Fix bug — 2026-08-26:** nội dung = báo cáo AI Auto-fixbug (đánh giá ảnh hưởng 6 mục + tự review + branch). Đã chép **nguyên văn** sang [03-dev-impact.md](03-dev-impact.md) để tránh trùng lặp 2 file.
