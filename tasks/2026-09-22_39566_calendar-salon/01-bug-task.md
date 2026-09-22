# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39566 — Calendar salon` (Tracker: **Bug API** · Status: **Fix done - Đợi test**) |
| Module / Màn hình | Salon Booking (**FA-020**) — toàn bộ màn quản trị lịch đặt chỗ salon 「サロン予約」: danh sách lịch (SCR-01), modal tạo lịch 「サロン・面談予約新規作成」(SCR-02b), tab 「コース・スタッフ」/「予約カレンダー」/「シフト」(SCR-03), cài đặt đặt chỗ, liên kết Google Calendar. Lớp xử lý: `Basic\CalendarSalonController` (KHÔNG phải `Api\CalendarSalonController`). |

## Mô tả bug (bản dịch tiếng Việt)

Ticket là **yêu cầu chuẩn hoá phía Dev**, không phải bug do khách hàng báo với ca lỗi cụ thể. Nội dung nguyên văn (3 yêu cầu):

1. Sửa lại http code cho đúng ý nghĩa với các api, ajax
2. validate required đầu vào
3. Mọi query đều **PHẢI** ràng buộc theo bot đang đăng nhập

Diễn giải theo điều tra của Dev (chi tiết ở `03-dev-impact.md`):

- **(1) HTTP code sai ý nghĩa** — các endpoint ajax của lịch đặt chỗ salon trả lỗi nghiệp vụ (không tìm thấy khoá học/nhân viên, vượt hạn mức gói) bằng mã **500** (nghĩa là server sập) hoặc **200** (nghĩa là thành công) → giám sát báo động nhầm, phía màn hình không phân biệt được loại lỗi.
- **(2) Thiếu validate required** — hầu hết endpoint nhận dữ liệu thẳng từ request mà không kiểm tra bắt buộc; thiếu tham số sẽ đi tới tận tầng service rồi báo lỗi chung chung hoặc lỗi hệ thống thật.
- **(3) Query không ràng buộc bot** — id nhận từ request được dùng luôn mà không lọc theo bot của phiên đăng nhập → đọc/sửa/xoá chéo bot (IDOR). Dev quét thấy **78/106 query** trong controller chưa ràng buộc bot, trong đó **32 câu nằm trong 25 hàm không có bất kỳ guard nào** — là lỗ hổng thật.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket là yêu cầu chuẩn hoá, không có ca lỗi tái hiện. -->

## Expected result

<!-- Không có trong Redmine. -->

## Actual result

<!-- Không có trong Redmine. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #39566 có 0 attachment. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — ticket không có section "Tái hiện bug", không có ca lỗi/ID cụ thể. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix** (mã HTTP theo loại lỗi · validate required · cách ly dữ liệu theo bot) + **regression impact**.

- **Branch QA checkout**: `ai_fixbug_39566` (repo `sns-line`, nhánh gốc `release_step_20260805`, commit `1b32a31c0a`, 32 file) — đã push.
- ⚠️ **Cảnh báo trạng thái push từ journal #136532** (nguyên văn): *"Bản QA đang test KHÔNG có phần vá bảo mật chéo bot. Cần DEV/PM review lại commit này rồi bấm Push để đẩy tiếp."* — commit `8def715890` (ràng buộc mọi query theo bot) tại thời điểm viết journal **chỉ có ở local, CHƯA push**. Journal sau đó lại ghi branch ở commit `1b32a31c0a` đã push. **Leader phải xác nhận với Dev commit nào đang có trên môi trường QA trước khi test nhóm TC phân quyền chéo bot** — nếu bản test chưa có vá, các TC chéo bot sẽ fail không phải do bug mới.
- **Điều kiện tiên quyết để test**: cần **2 bot khác nhau** (bot A / bot B) cùng có lịch salon để test IDOR chéo bot; cần dữ liệu cũ có `bot_id = NULL` ở 4 bảng nullable (`calendar_salon_course`, `calendar_salon_course_menu`, `sync_booking_google_calendar_histories`, `download_csv_sync_google_calendar`) để verify không bị "giấu mất" dữ liệu hợp lệ.
- **Dev CHƯA verify được bằng dữ liệu thật** (nguyên văn journal): *"⚠ CHƯA chạy được test trên dữ liệu thật: MySQL dev không kết nối được từ container (Connection refused)... Cần human chạy regression trên môi trường có DB, tập trung vào: danh sách khoá học/nhân viên, xoá lịch (cascade 16 câu), đồng bộ Google Calendar và hoàn tiền."* → 4 vùng này là **trọng tâm test bắt buộc**.
- **Mức verify của Dev chỉ là `lint`** (`php -l` + `node --check` + grep đếm) — không có unit/integration test.
- **Phạm vi CỐ Ý không sửa** (Dev khai): 14 service trong `app/Services/CalendarSalon` (149 query cũng thiếu ràng buộc bot) · `Api\CalendarSalonController` (app mobile + LIFF khách vẫn giữ 200 + `error_message`) · 2 endpoint `changeStatusBooking` + `createBooking` vẫn trả 200 với cờ thành công động. → **Tester ghi nhận hiện trạng, KHÔNG báo bug nhầm** cho 2 endpoint này.
- **Ngôn ngữ message**: message validate 422 phải là **tiếng Nhật hoàn chỉnh** với nhãn đúng chữ trên màn hình (店舗名 · カレンダー管理名 · メニュー名 · スタッフ名 · コース名 · シフト · 並び順 · カレンダー · 予約枠 · アクション · 予約ページでの表示 · 連携するスタッフ · Googleカレンダー) — **không được lẫn tên field tiếng Anh** kiểu `course menu id`.
- **Bộ TC hiện có do AI sinh trên LME TEST STUDIO** (task #149, 81 TC) — xem `04-tc-list.md`, chạy toàn bộ ở env `local`.

## Journal / note từ Redmine (nguyên văn)

**Journal #136482 — Kieu Son Tung — 2026-09-15:**

```
Kieu Son Tung wrote:
> Sửa lại http code cho đúng ý nghĩa với các api, ajax
> validate required đầu vào
```

> 2 journal còn lại (**#134891** — AI LME Fix bug — 2026-09-07 và **#136532** — AI LME Fix bug — 2026-09-15) là **báo cáo AUTO-FIXBUG** = chính nội dung "Đánh giá ảnh hưởng phía dev" → chép nguyên văn ở [`03-dev-impact.md`](03-dev-impact.md) (dùng bản mới nhất #136532), không nhân bản ở đây.
