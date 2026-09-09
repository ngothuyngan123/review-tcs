# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

> Nguồn: journal Redmine #37640 — "★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST" (2026-06-18).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Do Van Tu TuDV` (assigned) / `AI LME Fix bug` (auto-fix) |
| Commit / Pull Request | `commit d788a7da27` (repo sns-line) |
| Branch | `ai_fixbug_37640` (nhánh gốc `release_step_20260511`) |
| Ngày submit đánh giá | `2026-06-18` |
| Auto-filled | `2026-06-25 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Câu hỏi họ tên mặc định của form đặt lịch (lesson + salon) bị **khoá cứng đích liên kết (連携先) vào tên hiển thị hệ thống (システム表示名)**: ô chọn đích liên kết bị vô hiệu khi `can_delete=0`, nên đáp án của khách **luôn ghi đè lên tên hiển thị hệ thống**. Khách (lớp luyện thi) quản lý tên học sinh ở tên hiển thị hệ thống nên không muốn bị ghi đè. Comment cuối Redmine chốt: **giữ bắt buộc liên kết nhưng cho tự chọn đích liên kết**.

## 2. Cách fix

Chỉ ở **KHỐI câu hỏi dạng văn bản (type text / 短文回答)**: mở khoá ô chọn đích liên kết (連携先) cho câu hỏi họ tên mặc định (`can_delete=0`) ở màn cài đặt form đặt lịch lesson + salon, bằng cách **đổi điều kiện khoá** từ `can_delete=0` sang `(can_delete=0 && friend_information_id == -3)` — chỉ còn khoá đúng câu email mặc định (id `-3`).

- Picker của **RADIO (単一選択) / DATETIME (日時) giữ nguyên** như cũ (vẫn khoá theo `!can_delete`).
- **Loại liên kết vẫn khoá** nên liên kết vẫn bắt buộc.
- Backend đã định tuyến lưu theo `friend_information_id` nên **không cần sửa backend** (case `-1` → `view_name`; default → `friend_information_value`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `setting_form.blade.php` (lesson) — `resources/views/basic/calendar_management/tabs/setting_calendar_tab/` | **Có** — đổi điều kiện khoá dropdown 連携先 (chỉ khối TEXT, dòng ~491) | Mở khoá đích liên kết câu họ tên text |
| 2 | `setting_form.blade.php` (salon) — `resources/views/basic/calendar_salon/tabs/setting_calendar_tab/` | **Có** — đổi điều kiện khoá dropdown 連携先 (chỉ khối TEXT, dòng ~518) | Mở khoá đích liên kết câu họ tên text |
| 3 | `CalendarController::updateFriendInfoValue` — `app/Http/Controllers/Mobile/CalendarController.php` | Không (check) | Định tuyến lưu: case `-1` vs default theo `friend_information_id` |
| 4 | `CalendarSalonController::updateFriendInfoValue` — `app/Http/Controllers/Mobile/CalendarSalonController.php` | Không (check) | Định tuyến lưu: case `-1` vs default |
| 5 | `CalendarManagementController::getDataFriendInfo` — `app/Http/Controllers/Basic/CalendarManagementController.php:2261` | Không (check) | Seed basic info `-1` / `-2` / `-3` |
| 6 | `CalendarSettingSendFormService::getSettingForm` | Không (check) | Seed `-1` / `-3` |
| 7 | `CalendarSalonSettingSendFormService` (update) | Không (check) | Không có guard `can_delete` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Mọi function Dev đã sửa HOẶC có thể bị ảnh hưởng gián tiếp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | View setting form lesson — điều kiện khoá dropdown 連携先 (khối TEXT) | `resources/views/basic/calendar_management/tabs/setting_calendar_tab/setting_form.blade.php` | Direct | Đổi `can_delete=0` → `can_delete=0 && id==-3` |
| F2 | View setting form salon — điều kiện khoá dropdown 連携先 (khối TEXT) | `resources/views/basic/calendar_salon/tabs/setting_calendar_tab/setting_form.blade.php` | Direct | Như F1 |
| F3 | `CalendarController::updateFriendInfoValue` | `app/Http/Controllers/Mobile/CalendarController.php` | Indirect | Định tuyến lưu theo `friend_information_id` (không sửa) |
| F4 | `CalendarSalonController::updateFriendInfoValue` | `app/Http/Controllers/Mobile/CalendarSalonController.php` | Indirect | Như F3 |
| F5 | `CalendarManagementController::getDataFriendInfo` | `app/Http/Controllers/Basic/CalendarManagementController.php:2261` | Indirect | Seed basic info `-1`/`-2`/`-3` |
| F6 | `CalendarSettingSendFormService::getSettingForm` / `CalendarSalonSettingSendFormService` | (service) | Indirect | Seed/update setting form, không guard `can_delete` |

### 4.2. List data bị update khi fix bug

<!-- Mọi bảng DB, field, cache, config, migration,... bị chạm tới. -->

> Dev note: **Không có thay đổi cấu trúc/dữ liệu (không migration)**. Chỉ đổi đích lưu đáp án tuỳ 連携先 user chọn.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `friend_information_value` (đáp án câu họ tên khi 連携先 = trường tự chọn) | CREATE / UPDATE | Sau fix: đáp án có thể lưu vào friend_information_value thay vì view_name |
| D2 | `line_users.view_name` (システム表示名) | UPDATE | Chỉ update khi 連携先 = システム表示名 (case `-1`); không còn bị ghi đè bắt buộc |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev suy ra từ 4.1 và 4.2: tính năng end-user nào có nguy cơ regression. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đặt lịch học (レッスン予約) — cài đặt câu hỏi form (お客様への質問項目): câu họ tên cho phép chọn đích liên kết + flow đặt lịch lưu đáp án | F1, F3, D1, D2 | High |
| T2 | Đặt lịch salon (サロン予約) — cài đặt câu hỏi form: câu họ tên cho phép chọn đích liên kết + flow đặt lịch lưu đáp án | F2, F4, D1, D2 | High |

---

## Ghi chú rủi ro / lưu ý khi test (từ Dev tự review)

- Edge hiếm: nếu user cố chọn メールアドレス cho câu họ tên thì câu đó sẽ bị khoá lại (vì trùng điều kiện `id==-3`) — không gây hại, hành vi vô nghĩa.
- Cần build asset FE (npm) khi deploy nếu blade được cache; đây là blade nên thường không cần, nhưng **kiểm tra view cache** sau deploy.
- Verify mức: `lint` (php -l blade — no syntax error). Chỉ sửa FE (2 blade), diff = 4 insertions / 4 deletions (2 dòng/file).
- 商品販売 (bán sản phẩm) + イベント予約 (đặt chỗ sự kiện) **CHƯA đối ứng đợt này** — cùng pattern khoá 連携先 nhưng ngoài scope fix #37640.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
