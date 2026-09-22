# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40904 — [JOB][Lesson]Chuyển job sync google sheet của lesson sang java` |
| Module / Màn hình | `Lesson (レッスン予約) — sync dữ liệu booking lesson lên Google Sheet` · job nền Java + hàng đợi `calendar_sync_googles` · màn 「予約カレンダー」 / 「全体設定」>「Googleスプレッドシート連携」 · app quản lý mobile |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Đây **không phải bug từ khách hàng** — tracker Redmine là **Triển khai ngang** (refactor/port tính năng). Nội dung dưới đây là mô tả yêu cầu nguyên văn của Dev.

Phạm vi:
+ Sync google sheet của lesson
+ Retry google sheet của lesson

**0. Base branch:** `release-t08-2026`

**1. Mục tiêu**
- Chuyển tính năng sync dữ liệu lên Google Sheet của booking lesson, đã có sẵn bên PHP giờ chuyển sang JAVA.
- Lý do: Khi PHP sync luôn lên Google Sheet dẫn tới bị chậm request, cần lưu lại việc sync vào database rồi job lấy ra xử lý.

**2. Tài liệu tham khảo**
- *** Tham khảo code PHP để convert sang Java
  - folder source PHP: `/Users/apple/Desktop/Project/Z_PHP/sns-line`
  - function `insertDataToGoogleSheet` — class `app/Services/CalendarManagement/CalendarGoogleSheetService.php`
- *** Tham khảo code sync Google Sheet sẵn có của tính năng form phía Java
  - `HandleFormAnswerSyncGoogleSheetTask.java`
- *** Design bảng mới `calendar_sync_googles` + cách làm
  - `ai_docs/task_40194_40904/calendar-sync-googles-plan.md`

**3. Cách thức hoạt động**
- Phía PHP sẽ lưu lại các bản ghi cần sync ở bảng `calendar_sync_googles`.
- Phía job quét các bản ghi cần sync ở bảng này sau đó xử lý dữ liệu và sync lên Google Sheet giống logic của PHP `insertDataToGoogleSheet`.

## Steps to reproduce

<!-- Redmine KHÔNG có Section "Tái hiện bug" — đây là task triển khai ngang, không có ca lỗi tái hiện. -->

## Expected result

<!-- Không có trong Redmine. Behavior đích = giữ nguyên kết quả sync trên sheet giống bản PHP cũ (xem 03-dev-impact.md mục 2 + 4.3). -->

## Actual result

<!-- Không có trong Redmine. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40904 không có attachment nào. -->

## Ghi chú thêm của Leader

- ⚠️ **Không phải bug** — tracker `Triển khai ngang`, không có ca lỗi tái hiện. TCs phải tập trung vào: (a) **tương đương hành vi** giữa job Java mới và code PHP cũ (`insertDataToGoogleSheet`), (b) **regression** các luồng dùng chung, (c) hành vi của job nền (hàng đợi, retry, backoff, cờ bật/tắt).
- **Feature flag**: `ENABLE_HANDLE_CALENDAR_SYNC_GOOGLE_SHEET` (bật/tắt job Java) + `MAX_CALENDAR_SYNC_GOOGLE_SHEET_THREAD` trong `config.properties` → TC phải phủ cả trạng thái **tắt** và **bật**.
- ⚠️ **Điều kiện tiên quyết khi bật flag**: job PHP `HandleErrorGoogleSpreadSheet` **phải gỡ nhánh `type_result = 3` TRƯỚC**, nếu không 2 worker cùng ghi 1 dòng sheet (Dev nêu ở mục 4.3).
- **Migration bắt buộc trước khi chạy**: tạo bảng mới `calendar_sync_googles` + `ALTER result_error_googles` thêm cột `calendar_sync_googles_id`. 2 entity dùng chung (`ResultErrorGoogle`, `CalendarManagement`) chỉ chạy đúng **sau khi ALTER bảng**.
- **Ticket liên quan**: Redmine #40194 (cùng thư mục tài liệu `ai_docs/task_40194_40904/`) và **#40892** (branch `ai_fixbug_40892` — phía web/PHP ghi hàng đợi; TC trên Studio dẫn chiếu nhiều tới source của ticket này).
- **Branch / commit**: `m_202609_sync_google_sheet_lesson_40194_40904` · commit `b03c949` (base `release-t08-2026`).
- **Phạm vi test do Dev/QA chốt (quan điểm test trên Studio)**: mọi thao tác phải test **cả trên web lẫn app mobile quản lý** — admin book / cancel / approve booking / deny booking / approve cancel / deny request cancel / refund / change thông tin booking / xóa booking; user book ngay / request book / cancel ngay / request cancel; đăng ký nhận thông báo slot trống (**không** insert Google Sheet); hệ thống update trạng thái bill (chưa bill → đã bill). Cộng 1 luồng E2E: action sau khi booking · action lúc cancel · remind sau booking · sync Google Calendar · ghi lịch sử màn detail LINE user · notify app/PC/Chatwork.
- **Case sheet rỗng**: phải dựng lại **toàn bộ** booking (nhánh riêng trong job).

## Dữ liệu định danh ca lỗi

<!-- Redmine không có ca lỗi cụ thể (task triển khai ngang) — bỏ trống. -->

## Journal / note từ Redmine (nguyên văn)

Journal duy nhất có notes (**#136671 — Thanh Duy Nguyen — 2026-09-16**) chính là bản "Đánh giá ảnh hưởng" → đã chép nguyên văn vào [03-dev-impact.md](03-dev-impact.md), không lặp lại ở đây.
