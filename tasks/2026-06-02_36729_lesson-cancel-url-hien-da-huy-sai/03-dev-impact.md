# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kieu Son Tung` (assigned_to) |
| Commit / Pull Request | `<chưa có>` |
| Branch | `<chưa rõ>` |
| Ngày submit đánh giá | `2026-06-02` (journal Thanh Phương) |
| Auto-filled | `2026-06-02 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Dev mô tả root cause. Càng cụ thể càng tốt: file nào, function nào, logic sai ở đâu. -->

- Khi user đã có 1 đăng ký nhận thông báo chờ cancel (キャンセル待ち通知受け取り, status WAIT_CANCEL) cho khung giờ, mà thao tác đăng ký lại cùng khung giờ đó, API `order()` của Lesson tìm thấy đăng ký cũ và set cờ `$checkExistsRegisterNotifySlot = true`.
- Với code cũ (không có return): vì `$checkExistsRegisterNotifySlot = true` và `$register_notify_slot = true`, hệ thống KHÔNG tạo/không update bản ghi nào (bỏ qua cả nhánh create lẫn nhánh update), nhưng VẪN tiếp tục gửi lại action + message 「キャンセル用URL」.
- 「キャンセル用URL」 gửi lại này gắn với bookingId rỗng/không hợp lệ (request đăng ký lại không kèm bookingId của đăng ký cũ) → khi user click vào, màn hình hiển thị 「予約が解除されました」 nhưng đăng ký thật (bản ghi WAIT_CANCEL ban đầu) không bị hủy → user vẫn tiếp tục nhận thông báo.

## 2. Cách fix

<!-- Dev mô tả cách fix. Nếu có snippet code thì càng tốt. -->

- Khi phát hiện đã tồn tại đăng ký chờ cancel cho khung giờ này, return ngay với `status = false` kèm message 「すでにキャンセル待ち通知受け取りの予約があるため、この受付枠は予約できません」.
- Chặn không cho gửi lại action/「キャンセル用URL」 thừa, tránh phát sinh URL hủy trỏ sai → loại bỏ trường hợp hiển thị "đã hủy" nhưng thực tế chưa hủy.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarController@order` (Mobile) | Thêm điều kiện return chặn thao tác đăng ký trùng | Nơi sửa trực tiếp — API đăng ký nhận thông báo / đặt chỗ Lesson |
| 2 | Nhánh create (block `!$checkExistsRegisterNotifySlot`) + nhánh update (block `!$register_notify_slot`) | Không sửa | Đã rà soát: trường hợp đăng ký trùng không đụng tới DB, chỉ phát sinh ở bước gửi action/message → fix chặn ngay từ đầu là đủ |
| 3 | Nhánh `bookingType == 'notify'` (đặt lại chỗ từ một đăng ký đã biết bookingId) | Giữ nguyên | Không bị ảnh hưởng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarController@order` (Mobile) | `app/Http/Controllers/Mobile/CalendarController.php` | Direct | API đăng ký nhận thông báo / đặt chỗ Lesson — nơi thêm điều kiện return |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Dev xác nhận: chỉ thêm điều kiện return chặn thao tác trùng, KHÔNG thay đổi/ghi đè dữ liệu hiện có |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đăng ký nhận thông báo chờ cancel (キャンセル待ち通知受け取り) của Lesson trên màn hình booking | F1 | Medium |
| T2 | Luồng nhận / hủy qua 「キャンセル用URL」 của Lesson | F1 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
