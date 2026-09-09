# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #37606 (journal AI AUTO-FIXBUG, 2026-06-15) bởi `/new-task` ngày 2026-06-16. **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs. Tester verify đủ 4 mục rồi tick checkbox.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kieu Son Tung` (assigned_to) / AI Auto-fixbug |
| Commit / Pull Request | `sns-line` commit `7c5ed6562a` (2 file) — [đã push] |
| Branch | `ai_fixbug_37606` (nhánh gốc `release_step_20260511`) |
| Ngày submit đánh giá | `2026-06-15` |
| Auto-filled | `2026-06-16 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn xem-sửa một trường thông tin bạn bè (click vào trường → `/basic/friend-information/{id}`) vừa vào đã gọi AJAX `initDataInfo` để nạp lại cấu hình trường. Trường 'plan đã đặt' (kiểu Lựa chọn, do tính năng đặt lịch dùng) có gắn hành động (Action) cho từng lựa chọn — id của các hành động này lưu trong cấu hình trường. Khi một hành động đã bị xóa nhưng id của nó vẫn còn trong cấu hình, backend tra hành động ra `null` nhưng vẫn cố đọc chi tiết của nó.

Điều kiện bảo vệ lại kiểm tra **nhầm biến phụ** (danh sách `details` — luôn khác rỗng) thay vì kiểm tra chính đối tượng `action`, nên rơi vào vòng lặp đọc thuộc tính trên `null` → sinh lỗi `Trying to get property 'details' of non-object` → màn trả lỗi và hiện alert ngay khi vào.

## 2. Cách fix

Fix 2 lớp:

1. **Chặn crash (guard đọc):** `FriendInformationController::initDataInfo` đổi guard `if($details)` (luôn đúng) thành `if(!empty($action))` để bỏ qua action mồ côi khi mở trường — chặn crash cho dữ liệu đã hỏng sẵn trên production + mọi đường cascade.
2. **Vá tận gốc nơi sinh orphan:** tại `TagController::deletedDataTag` — khi xóa tag làm Action bị xóa theo, thu thập các `action_id` vừa xóa rồi dọn tham chiếu mồ côi ở `friend_info_option_selects` (set `action_id=null`) và trong `setting_value` JSON của `friend_information_setting` (xóa `action_id` mồ côi) — để không sinh orphan mới. Helper mới `cleanOrphanFriendInfoActionRef` bọc try-catch riêng, không làm fail luồng xóa tag.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FriendInformationController::initDataInfo` — `app/Http/Controllers/Basic/FriendInformationController.php:141-144` | Đổi guard `if($details)` → `if(!empty($action))` | Bỏ qua action mồ côi khi mở trường → chặn crash |
| 2 | `TagController::deletedDataTag` — `app/Http/Controllers/Basic/TagController.php` | Thu thập `action_id` bị xóa cùng tag + gọi helper dọn reference | Vá tận gốc nơi sinh orphan |
| 3 | `TagController::cleanOrphanFriendInfoActionRef` (helper mới) | Thêm mới — dọn orphan ở `friend_info_option_selects` + `friend_information_setting` | Dọn tham chiếu action mồ côi |
| 4 | `infor_friend/create.js` — `created() → initDataInfo → alert(a.msg)` | Không sửa (chỉ là nơi hiển thị alert khi backend trả lỗi) | Truy vết hiển thị alert |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FriendInformationController::initDataInfo` | `app/Http/Controllers/Basic/FriendInformationController.php` | Direct | Guard đọc action — sửa trực tiếp để chặn crash |
| F2 | `TagController::deletedDataTag` | `app/Http/Controllers/Basic/TagController.php` | Direct | Xóa tag cascade xóa Action — thêm dọn reference orphan |
| F3 | `TagController::cleanOrphanFriendInfoActionRef` | `app/Http/Controllers/Basic/TagController.php` | Direct | Helper mới dọn orphan (try-catch riêng) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `friend_info_option_selects.action_id` | UPDATE (set null) | Set null khi action bị xóa cùng tag — chỉ ghi đè reference mồ côi, cột nullable |
| D2 | `friend_information_setting.setting_value` (JSON `setting_actions`) | UPDATE | Xóa `action_id` mồ côi trong JSON khi action bị xóa cùng tag |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Quản lý thông tin bạn bè (友だち情報管理) — mở/sửa trường Lựa chọn có gắn action | F1, D1, D2 | High |
| T2 | Quản lý tag (タグ管理) — khi xóa tag: ngoài dọn FilterV2/tag_line_user như cũ, nay dọn thêm tham chiếu action mồ côi ở trường thông tin bạn bè | F2, F3, D1, D2 | Medium |

---

## Ghi chú thêm (từ Dev)

- **5. Recover data:** ⚠ CÓ (tùy chọn) — Các bot dính orphan TRƯỚC khi deploy vẫn còn `action_id` mồ côi trong `setting_value`/`friend_info_option_selects`. Guard đọc đã khiến chúng KHÔNG còn gây lỗi (an toàn) → data recovery **KHÔNG bắt buộc**. Nếu muốn dọn sạch tồn đọng: quét 1 lần `friend_information_setting` + `friend_info_option_selects`, set `action_id` mồ côi về null/''.
- **Lưu ý khi test:**
  - `deletedDataTag` thuộc feature tag (khác feature ticket) — đã thêm cleanup tối thiểu, bọc try-catch để không ảnh hưởng luồng xóa tag nếu lỗi.
  - Orphan vẫn có thể sinh từ **đường cascade khác** (xóa scenario/richmenu/template làm Action bị xóa) — guard đọc đã chặn crash cho mọi đường; vá gốc các đường khác là ticket yokoten riêng (chưa làm trong ticket này).
  - **Verify mức lint** — Dev DB không có data bot ULUM nên không tái hiện trực tiếp; xác nhận qua error message + truy vết code + tiền lệ guard `ConversionController:353`, `QRCodeController:1546`.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
