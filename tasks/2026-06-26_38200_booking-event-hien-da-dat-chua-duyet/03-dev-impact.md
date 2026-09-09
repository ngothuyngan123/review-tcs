# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: journal #123822 (AI AUTO-FIXBUG) trên Redmine #38200. Paste nguyên văn, parse thành 4 mục.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (Auto-fixbug LME) |
| Commit / Pull Request | commit `24d403e089` (1 file) — không có PR URL |
| Branch | `ai_fixbug_38200` (gốc `release_step_20260623`) — repo `sns-line`, đã push |
| Ngày submit đánh giá | 2026-06-26 |
| Auto-filled | 2026-06-26 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Hàm xử lý thao tác admin với booking sự kiện (`Api/BookingEventController::saveAction`) tham chiếu biến `$lineUserForHistory` ở các nhánh field SĐT(-2)/Tuổi(-4)/Tỉnh(-6) NHƯNG biến này KHÔNG được định nghĩa → `ErrorException 'Undefined variable: lineUserForHistory'` (dòng ~409).

Nguyên nhân gốc: commit 'fix friend info' (`79c01515411`, tudv 2026-05-27) thêm dòng định nghĩa `$lineUserForHistory = LineUser::find($lineUserId);` NGAY TRƯỚC switch + các lời gọi `recordFriendInfoHistory`; nhưng khi merge với một nhánh khác cùng ngày (thêm khối `if(isset($lineUser))`), dòng ĐỊNH NGHĨA bị rớt còn các lời gọi vẫn còn → biến mồ côi.

Vì `saveAction` đổi status booking TRƯỚC vòng lặp lưu form_info và KHÔNG bọc transaction, booking nào có field SĐT/Tuổi/Tỉnh sẽ crash giữa chừng: status đã bị đổi sang đã đặt nhưng thao tác admin báo lỗi (phần gửi thông báo phía sau không chạy) → user thấy 予約済み dù admin chưa duyệt xong.

## 2. Cách fix

Khôi phục đúng dòng bị rớt: thêm lại `$lineUserForHistory = LineUser::find($lineUserId);` ngay trước switch trong `saveAction` (`Api/BookingEventController.php`). GIỮ NGUYÊN toàn bộ logic ghi lịch sử `recordFriendInfoHistory` mà tudv thêm (đây là logic cần thiết) — chỉ bổ sung định nghĩa biến (4 dòng thêm, không xóa gì). Hết crash.

(Đã revert hướng sửa sai trước đó: lần 1 sửa nhầm `handleOrderCallback`, lần 2 xóa nhầm chính các lời gọi `recordFriendInfoHistory` — đều đã hủy.)

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Api/BookingEventController::saveAction` (`app/Http/Controllers/Api/BookingEventController.php`) | Định nghĩa lại `$lineUserForHistory` trước switch | Dùng ở case -2/-4/-6 (SĐT/Tuổi/Tỉnh); thiếu định nghĩa gây crash |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BookingEventController::saveAction` | `app/Http/Controllers/Api/BookingEventController.php` | Direct | Thao tác admin duyệt/đổi booking sự kiện; case field -2/-4/-6 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `b_user_booking.status` | UPDATE | Không sửa dữ liệu cũ; chỉ ngăn crash cho thao tác admin về sau. Booking đã bị đổi status sai trước đây do crash là dữ liệu lịch sử, admin cần rà lại thủ công |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Event Booking (FA-021) — admin duyệt/đổi booking sự kiện có field SĐT/Tuổi/Tỉnh; thao tác duyệt chạy trọn vẹn (đổi trạng thái + ghi lịch sử thông tin bạn + gửi thông báo) | F1, D1 | High |

---

## Ghi chú thêm từ AI Auto-fixbug (ngoài 4 mục chuẩn)

**■ 5. RECOVER DATA:** ✔ Không cần recover data (lưu ý: booking cũ đã bị đổi status sai do crash vẫn còn — ngoài scope code, admin rà thủ công).

**■ 6. VERIFY:** Mức `lint`. `php -l Api/BookingEventController.php` → No syntax errors; `git blame` xác nhận dòng định nghĩa từng tồn tại ở commit `79c01515411` rồi bị rớt khi merge. Bằng chứng: stack trace KH `ErrorException Undefined variable: lineUserForHistory ...BookingEventController.php:409`.

**■ Rủi ro / lưu ý khi test (AI tự review):**
- Booking cũ đã đổi status sai do crash vẫn còn — ngoài scope code.
- Ghi lịch sử TRÙNG ở case -2/-4/-6 do bad-merge (ghi yokoten, để reviewer chọn dedupe).
- Transaction bị comment trong `saveAction` (yokoten).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
