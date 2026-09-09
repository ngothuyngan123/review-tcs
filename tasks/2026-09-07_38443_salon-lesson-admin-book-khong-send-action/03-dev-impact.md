# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #38443 — Journal #131657 (báo cáo **Auto-fixbug LME (AI)**, 2026-08-21).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | **AI LME Fix bug** (hệ thống Auto-fixbug LME) — assignee hiện tại trên Redmine: Hạnh Nguyễn |
| Commit / Pull Request | commit `4e6b59e1e4` (repo `sns-line`, 2 file, 41 dòng thêm) — không có link PR trong ticket. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=38443 |
| Branch | `ai_fixbug_38443` (nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | 2026-08-21 |
| Auto-filled | `2026-09-07 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ **Mức verify của Dev(AI) chỉ là `lint`** — `php -l` 2 file + `git diff --stat`. Dev(AI) ghi rõ *"Không kiểm chứng được trên DB dev: MySQL host.docker.internal:3306 từ chối kết nối"* và *"mới dừng ở mức đọc code và lint"*. **Chưa có bất kỳ kiểm chứng hành vi thật nào.**

---

## 1. Nguyên nhân

Khi admin tự đặt lịch hộ khách (salon và bài học), hệ thống chỉ lưu giá trị thông tin bạn bè và ghi dòng lịch sử, nhưng **bỏ hẳn bước kích hoạt action** đã gắn với lựa chọn của thông tin bạn bè đó.

- Vì action không chạy → khách **không nhận được nội dung**.
- Dòng lịch sử **không được gắn liên kết tới action** → cột xem trước ở màn chi tiết bạn bè hiển thị 「設定なし」 (Chưa thiết lập).
- **Luồng khách tự đặt lịch vẫn chạy đúng** vì có sẵn đoạn kích hoạt action này.

## 2. Cách fix

Bổ sung vào **2 luồng admin đặt lịch hộ** (salon và bài học) đoạn kích hoạt action gắn với lựa chọn của thông tin bạn bè, **giống hệt luồng khách tự đặt lịch**:

1. Đọc cấu hình action của mục thông tin.
2. So khớp giá trị vừa lưu.
3. Tôn trọng chế độ chỉ chạy lần đầu (「一度のみ」).
4. Truyền id dòng lịch sử vừa ghi vào lệnh chạy action → màn chi tiết bạn bè hiện được liên kết xem trước 「プレビュー」 thay vì 「設定なし」.

> ⚠️ **Ngoài phạm vi ticket (chỉ ghi nhận, KHÔNG fix)**: quét ngang thấy **4 chỗ khác cùng thiếu đoạn này** — sửa thông tin biểu mẫu của lượt đặt đã có, và **2 luồng đặt lịch từ app**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonLineBookingService::createBooking` — `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | **CÓ sửa** — thêm đoạn kích hoạt action friend info | Luồng admin đặt lịch hộ salon — điểm thiếu chính |
| 2 | `CalendarSalonLineBookingService::updateFriendInfoValue` — cùng file (quanh dòng 5525-5545) | Không sửa | Luồng **khách tự đặt** — dùng làm **mẫu đối chiếu** (đã có sẵn đoạn kích hoạt action mã 6004 kèm id lịch sử) |
| 3 | `CalendarCourseBookingService::create` — `app/Services/CalendarManagement/CalendarCourseBookingService.php` | **CÓ sửa** — thêm đoạn kích hoạt action friend info | Luồng admin đặt lịch hộ lesson — điểm thiếu chính |
| 4 | `recordFriendInfoHistory` — `app/Helpers/functions.php` | Không sửa | Hàm ghi dòng lịch sử, trả về id lịch sử để truyền vào lệnh chạy action |
| 5 | `sendAction` — `app/Helpers/functions.php` | Không sửa | Hàm chạy action được gọi thêm từ 2 luồng trên |
| 6 | `getTableHistory` — `app/Helpers/functions.php` | Không sửa | Map mã **6004** sang bảng lịch sử thông tin bạn bè — chính là đường ghi liên kết xem trước |
| 7 | `FriendDetailFriendInfoService::triggerFriendInfoAction` — `app/Services/FriendDetailFriendInfoService.php` | Không sửa | Bản trung tâm ở màn chi tiết bạn bè — tham chiếu hành vi chuẩn |
| 8 | `cell-actions_preview` — `resources/views/basic/friend_detail/tabs/friend_info.blade.php` (dòng 202-206) | Không sửa | Chỗ render 「プレビュー」 / 「設定なし」 — khớp đúng triệu chứng ticket |

---

## 4. Đánh giá ảnh hưởng

> ⚠️ Redmine mục 4.1 Dev(AI) ghi ở mức **file thay đổi**, không phải function. Bảng dưới giữ nguyên 2 file Dev kê + gắn function tương ứng suy từ mục 2 + mục 3 (đã đánh dấu rõ nguồn).

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CalendarSalonLineBookingService::createBooking` (admin đặt lịch hộ salon) | `app/Services/CalendarSalon/CalendarSalonLineBookingService.php` | **Direct** | File Dev kê ở 4.1; function suy từ mục 2 + mục 3 |
| F2 | `CalendarCourseBookingService::create` (admin đặt lịch hộ lesson) | `app/Services/CalendarManagement/CalendarCourseBookingService.php` | **Direct** | File Dev kê ở 4.1; function suy từ mục 2 + mục 3 |
| F3 | `sendAction` (được F1/F2 gọi thêm) | `app/Helpers/functions.php` | Indirect | Không sửa code, nhưng nay có thêm 2 caller mới |
| F4 | `recordFriendInfoHistory` → id lịch sử truyền sang `sendAction` | `app/Helpers/functions.php` | Indirect | Không sửa code; đường ghi `table_history` |
| F5 | Job nền xử lý bản ghi chạy action → ghi liên kết vào dòng lịch sử | (Dev KHÔNG kê ở 4.1) | Indirect | ⚠️ **Không nằm trong 4.1 của Dev** nhưng là mắt xích bắt buộc để 「設定なし」 → 「プレビュー」. Studio đã tách thành REQ-006. |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `action_lineuser` | **CREATE** | Thêm bản ghi action chờ chạy khi admin đặt lịch hộ có gán thông tin bạn bè — **trước đây KHÔNG sinh**. Loại kích hoạt = **6004**. |
| D2 | `friend_information_history.action_multi_capture_id` | **UPDATE** | Từ nay được gắn cho dòng lịch sử sinh từ admin đặt lịch hộ; **dữ liệu cũ vẫn để trống** (không backfill). |
| — | Recover data | — | ✔ **Không cần** khôi phục dữ liệu cũ (Dev xác nhận) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Salon Booking (FA-020)** — admin đặt lịch hộ nay chạy action của thông tin bạn bè | F1, D1, D2 | High *(mức do /new-task suy từ risk REQ-001 = High; Dev không ghi mức)* |
| T2 | **Lesson / Calendar Booking (FA-019)** — admin đặt lịch hộ nay chạy action của thông tin bạn bè | F2, D1, D2 | High *(suy từ risk REQ-002 = High; Dev không ghi mức)* |
| T3 | **Friend Information (FA-015)** — lịch sử thông tin bạn bè hiện được liên kết xem trước action thay vì 「設定なし」 | D2, F4, F5 | High *(suy từ risk REQ-005 = High; Dev không ghi mức)* |

### Rủi ro / lưu ý khi test (Dev(AI) tự nêu — nguyên văn ý)

- **BUG-R1 — CONFLICT chờ PO**: tuỳ chọn 「予約時アクションの実行」 (Thực hiện / Không thực hiện) trên form đặt lịch hộ chỉ chi phối **action của lượt đặt**; fix **cố ý KHÔNG** gắn action thông tin bạn bè vào tuỳ chọn này — giống mọi luồng khác đang ghi thông tin bạn bè. Nếu nghiệp vụ muốn tuỳ chọn đó chặn cả action thông tin bạn bè thì **cần chốt lại và bọc thêm điều kiện**.
- **BUG-R2 — thay đổi hành vi thấy được**: với chế độ 「何度でも稼働」 (chạy mọi lần), **mỗi lần admin đặt lịch hộ và đổi giá trị sẽ gửi action cho khách** — đúng thiết kế tính năng nhưng khác hiện trạng.
- **BUG-R3 — chưa kiểm chứng thật**: chưa chạy được trên môi trường thật (DB dev không kết nối được), mới dừng ở mức đọc code và lint.
- **BUG-R4 — phạm vi bị thu hẹp có chủ đích**: 4 chỗ khác cùng thiếu đoạn kích hoạt action (sửa thông tin biểu mẫu của lượt đặt đã có + **2 luồng đặt lịch từ app**) **không được fix** trong ticket này.
- **BUG-R5 — tự đánh giá phạm vi**: Dev(AI) khẳng định "không tạo hàm dùng chung mới nên không ảnh hưởng luồng nào khác"; chỉ thêm code vào **nhánh field kiểu 「選択」**, các nhánh tên / điện thoại / email / ngày sinh / tỉnh thành / địa chỉ không đổi.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ Dev kê ở mức **file**, và **không kê job nền (F5)**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC — ⚠️ **BUG-R1 bắt buộc hỏi PO trước khi chấm Đạt/Không đạt**
