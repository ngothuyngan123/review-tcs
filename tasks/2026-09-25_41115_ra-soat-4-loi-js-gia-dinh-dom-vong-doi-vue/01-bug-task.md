# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41115 — [LME][Rà soát] 4 lỗi JS giả định DOM / vòng đời Vue phát hiện khi quét ngang #41090 (admin bill-tool, quản lý lịch lesson+salon, đặt lịch bài học)` |
| Module / Màn hình | 4 màn (ticket gộp): (1) Quản trị — Đăng ký / nâng cấp gói (bill-tool, FA-031) · (2) Quản lý lịch Lesson (FA-019) + Salon (FA-020) — resize cửa sổ ở chế độ 週/月 · (3) Salon — Quản lý lịch (予約カレンダー, hộp thoại シフト編集) · (4) Trang đặt lịch bài học phía người dùng LINE (nút 戻る ở tab 週) |

## Mô tả bug (bản dịch tiếng Việt)

> Ticket do AI viết bằng tiếng Việt — giữ nguyên văn, không cần dịch.

Gộp từ #41113 + #41114 + #41116 vào ticket này (fix chung trên branch ai_fixbug_41115).
Tất cả cùng một lớp lỗi với #41090: JS chạy trong vòng đời Vue (updated / resize / callback) nhưng giả định phần tử DOM của một chế độ hiển thị khác vẫn còn, hoặc kiểm tra "đã khởi tạo" sai.

**1) [Admin][Đăng ký-nâng cấp gói] updated() không guard #confirm_term + listener cuộn gắn chồng**
- Vị trí: `public/js/admin/bill_tool/index.js:252-260` · `resources/views/admin/bots/v2/main-step.blade.php:195 / 411 / 664`
- Hiện trạng:
  - a) `updated()` chỉ kiểm tra `step == 1` rồi lấy thẳng `document.getElementById('confirm_term')` và gọi `box.addEventListener(...)`. `#confirm_term` chỉ render khi `step == 1` VÀ một trong 3 nhánh:
    - `(type_contract_new == 1 || upgrade_flag == 1 || typeUpgrade == 'max_friend') && type_campaign != 1`
    - `type_contract_new == 0 && type_campaign != 1`
    - `type_contract_new == 1 && type_campaign == 1`

    Tổ hợp `type_contract_new == 0 && type_campaign == 1` không khớp nhánh nào ⇒ `box = null` ⇒ TypeError ném lại MỖI LẦN re-render.
  - b) Listener gắn bằng hàm ẩn danh nên `addEventListener` không khử trùng lặp: mỗi lần `updated()` chạy là thêm một handler scroll mới, cuộn 1 lần chạy N lần.
- Mong đợi: guard null rồi mới dùng; gắn listener một lần (mounted + watch, hoặc gỡ handler cũ trước).

**2) [Quản lý lịch][Lesson + Salon] Resize ở chế độ Tuần/Tháng gây lỗi JS**
- Vị trí: `public/js/calendar_management/calendar_detail.js:71-77` · `public/js/calendar_salon/calendar_detail.js:76-82` · blade: `calendar_management/tabs/calendar.blade.php:142` ; `calendar_salon/tabs/calendar_management/index.blade.php:228`
- Hiện trạng: handler resize lấy `#list-course-day` rồi dùng ngay `table.clientWidth`, nhưng phần tử này chỉ render khi `v-if="selectModeDisplay == 'day'"`. Đang xem 週/月 mà resize cửa sổ ⇒ null ⇒ TypeError, các `.dynamicDiv` không được đặt lại width. Chính 2 file này ở chỗ khác đã guard đúng (`calendar_detail.js:1327-1330, 2720-2724`; `calendar-management.js:699-712`).
- Mong đợi: thêm guard đầu handler, áp cho cả 2 file.

**3) [Salon][Quản lý lịch] updated() dùng $refs.scrollDiv + init lại time picker mỗi lần render**
- Vị trí: `public/js/calendar_salon/calendar-management.js:326-331` · blade: `calendar_salon/tabs/calendar_management/calendar_display_day2.blade.php:64` (`ref="scrollDiv"`)
- Hiện trạng: `ref="scrollDiv"` chỉ render ở chế độ 'day'; chuyển sang Tuần/Tháng thì `$refs.scrollDiv = undefined` ⇒ TypeError mỗi lần re-render. Kèm theo `initializeTimePickers()` chạy lại ở mọi lần render mà không huỷ daterangepicker cũ.
- Mong đợi: guard `$refs`; chỉ init lại time picker khi dữ liệu liên quan đổi (hoặc huỷ bản cũ trước). (Phần này ĐÃ có commit đầu tiên trên branch ai_fixbug_41115.)

**4) [Đặt lịch bài học] Bấm Quay lại ở tab Tuần gây lỗi do kiểm tra fullcalendar sai**
- Vị trí: `public/js/booking_news/booking.js:1287` (`backBookingStep`); liên quan `:695`, `:560`, `:589` · màn: `basic/calendar_management/bookings/layouts/main.blade.php` (`Mobile\CalendarController@index`)
- Hiện trạng: `if (Object.keys(this.fullcalendar))` — `Object.keys({})` trả `[]` (truthy) nên điều kiện LUÔN đúng. `fullcalendar` khởi tạo là `{}` và chỉ được gán khi vào chế độ Tháng, nên ở tab 週 gọi `render()` sẽ ném `"this.fullcalendar.render is not a function"`. Đây đúng là dòng anh em của chỗ đã sửa ở #41090 (`calendar_salon/booking.js` đổi thành `self.fullcalendar && Object.keys(...).length > 0`).
- Mong đợi: kiểm tra tồn tại + có hàm render; rà thêm `:695` và `:560/:589`.

**Ghi chú:** Fix cả 4 mục trên CÙNG branch ai_fixbug_41115, mỗi mục một commit riêng cho dễ review. Báo cáo quét ngang đầy đủ: `projects/fixbug-lme/verify/41090-yokoten/SUMMARY.md`

## Steps to reproduce

<!-- Redmine không có Section "Tái hiện bug" riêng — điều kiện tái hiện từng mục nằm trong "Hiện trạng" ở trên. -->

## Expected result

## Actual result

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

(Redmine không có attachment.)

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được trong Redmine — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- Ticket **tự detect** (tracker "Bug tự detect") do AI quét ngang từ #41090, không phải khách hàng báo. Gộp 3 ticket #41113 / #41114 / #41116 (đã Reject, trỏ về đây).
- Lỗi là lỗi JS phía trình duyệt → evidence chính là **console trình duyệt không có TypeError** + UI còn hoạt động.
- Điều kiện tái hiện mục 1: bot có tổ hợp **hợp đồng cũ (`type_contract_new == 0`) + có chiến dịch (`type_campaign == 1`)** ở bước `step == 1` → khối `#confirm_term` không render.
- Điều kiện tái hiện mục 2/3: màn quản lý lịch đang ở chế độ **週 / 月** (không phải 日). Mục 4: trang đặt lịch bài học phía user ở **tab 週 (mặc định)**, bấm 戻る từ bước nhập thông tin.
- Dev chỉ verify mức **lint** (`node -c`), **không tái hiện bằng trình duyệt**.
- ⚠️ Journal #137393 mâu thuẫn trạng thái push commit `0150dedda4` (thân: "CHƯA push lên origin, cần push lại"; dòng branch: "[đã push]") → xác nhận với Dev trước khi test mục 1.

## Journal / note từ Redmine (nguyên văn)

**Journal #137077 — AI LME Fix bug — 2026-09-18:**
```
Gộp #41113 + #41114 + #41116 vào ticket này theo yêu cầu: 4 lỗi cùng một lớp (JS giả định DOM / vòng đời Vue), fix chung trên branch ai_fixbug_41115. Subject + mô tả đã cập nhật thành bản gộp. 3 ticket kia đã được Reject với ghi chú trỏ về đây.
```

**Journal #137378 — AI LME Fix bug — 2026-09-21:** báo cáo auto-fixbug vòng 2 (commit `3d44770f8a`) — nội dung đã chép vào `03-dev-impact.md`; bản mới hơn là Journal #137393.

**Journal #137393 — AI LME Fix bug — 2026-09-21:** báo cáo auto-fixbug sau tự review v1 (commit `0150dedda4`) — nguồn chính của `03-dev-impact.md`, chép nguyên văn mục 1–4, 6 ở đó.
