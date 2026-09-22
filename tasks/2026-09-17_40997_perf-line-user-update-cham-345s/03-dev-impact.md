# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `d958c99506` (5 file) — Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40997 |
| Branch | `ai_small_40997` (repo `sns-line`, nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-17 (Journal #136862) |
| Auto-filled | `2026-09-17 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Thao tác Xóa bạn bè (`POST /basic/line_user/update` với `type=deleteLineUser`) chạy cascade dọn khoảng 40 bảng; nút cổ chai nằm ở **khối dọn số liệu trang đích**. Ba bảng log trang đích dùng chung cho TOÀN hệ thống đều thiếu chỉ mục đúng với điều kiện đang lọc:

- bảng **lượt bấm trang đích** (`detail_landing_click`) và bảng **lượt hành động trang đích** (`time_action_landing`) chỉ có chỉ mục theo **mã trang đích** trong khi câu lệnh lọc theo **mã bot + mã bạn bè**;
- bảng **lượt mở trang đích** (`collect_open_landings`) **không có chỉ mục nào** ngoài khóa chính.

Vì vậy mỗi lần xóa 1 bạn, máy chủ phải **quét cạn** các bảng log này nhiều lượt (2 câu tổng hợp + 1 câu xóa), cộng thêm **5 câu lặp lại cho MỖI trang đích** mà bạn đó từng bấm (1 câu lấy mã thiết bị + 4 câu đếm).

Chi phí gần như **không phụ thuộc bot lớn hay nhỏ** nên mọi bot đều chậm ở mức hàng chục giây (59s, 65s) và **tăng vọt lên 329–345s khi hai thao tác xóa chạy song song** cùng lúc, đúng như dữ liệu trong ticket (2 request cùng một phút của cùng một người dùng).

## 2. Cách fix

Sửa trên nhánh `ai_small_40997` (`sns-line`, 5 file).

1. **Thêm migration tạo 3 chỉ mục** đúng với điều kiện lọc của khối dọn số liệu trang đích:
   - bảng lượt bấm trang đích theo `(mã bot, mã bạn bè, mã trang đích)`
   - bảng lượt hành động trang đích theo `(mã bot, mã bạn bè)`
   - bảng lượt mở trang đích theo `(mã bot, mã trang đích)`

   Dùng **prefix 64 ký tự** cho cột mã bạn bè để không chạm giới hạn độ dài khóa; **có kiểm tra chỉ mục đã tồn tại trước khi tạo** nên chạy lại vẫn an toàn.

2. **Gom 5 câu lệnh lặp cho mỗi trang đích** (1 câu lấy mã thiết bị + 4 câu đếm) thành **đúng 2 câu tổng hợp chạy một lần trước vòng lặp**, qua **3 hàm dùng chung mới** trong `app/Helpers/functions.php`; **giữ nguyên phạm vi lọc, phạm vi xóa mềm và cách tính từng con số**. Áp cho **cả 4 luồng xóa bạn bè** (xóa trên web, chặn-xóa, chặn-xóa hàng loạt, xóa trên app) theo đúng bài học #38390/#40708.

3. **Thêm unit test** cho hàm tra số liệu theo trang đích.

**Quét ngang:** các chỗ khác dùng cùng bảng đều lọc theo mã trang đích (đã có chỉ mục) nên không thuộc phạm vi lỗi này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FriendlistController::updateLineUser` case `deleteLineUser` — `app/Http/Controllers/Basic/FriendlistController.php` | Dùng 2 câu gom mới thay 5 câu lặp | Endpoint chính bị báo chậm (`POST /basic/line_user/update`) |
| 2 | `FriendlistController::deleteUserBlock` — `app/Http/Controllers/Basic/FriendlistController.php` | Dùng 2 câu gom mới | Luồng chặn-xóa 1 bạn, dùng chung khối dọn số liệu trang đích |
| 3 | `FriendlistController::deleteUserBlockAction` — `app/Http/Controllers/Basic/FriendlistController.php` | Dùng 2 câu gom mới | Luồng chặn-xóa **hàng loạt** |
| 4 | `Api\FriendInformationController::deleteFriend` — `app/Http/Controllers/Api/FriendInformationController.php` | Dùng 2 câu gom mới | Luồng xóa bạn từ **app mobile** |
| 5 | `collectLandingClickStatsOfLineUsers` — `app/Helpers/functions.php` | **Hàm dùng chung MỚI** — câu tổng hợp đếm số liệu lượt bấm theo trang đích | Thay 4 câu đếm lặp/trang đích |
| 6 | `collectLandingDeviceIdsOfLineUsers` — `app/Helpers/functions.php` | **Hàm dùng chung MỚI** — câu tổng hợp lấy mã thiết bị | Thay 1 câu lấy mã thiết bị lặp/trang đích |
| 7 | `getLandingClickStat` — `app/Helpers/functions.php` | **Hàm dùng chung MỚI** — tra số liệu từ map đã gom | Có unit test `LandingClickStatHelperTest` |
| 8 | `removeHistoryLineUser` — `app/Helpers/functions.php` | Sửa — khối dọn số liệu trang đích chuyển sang dùng 3 hàm mới | Là nơi chứa khối cổ chai |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Journal Dev mục 4.1 liệt kê theo **file thay đổi** (5 file). Bảng dưới giữ nguyên danh sách file + map sang function ở mục 3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | 3 hàm dùng chung mới (`collectLandingClickStatsOfLineUsers`, `collectLandingDeviceIdsOfLineUsers`, `getLandingClickStat`) + `removeHistoryLineUser` | `app/Helpers/functions.php` | Direct | Khối dọn số liệu trang đích — nơi cổ chai |
| F2 | `updateLineUser` (case `deleteLineUser`), `deleteUserBlock`, `deleteUserBlockAction` | `app/Http/Controllers/Basic/FriendlistController.php` | Direct | 3 lối vào xóa bạn trên web |
| F3 | `deleteFriend` | `app/Http/Controllers/Api/FriendInformationController.php` | Direct | Lối vào xóa bạn từ app mobile |
| F4 | Migration thêm 3 chỉ mục | `database/migrations/2026_09_15_103000_add_index_for_delete_friend_landing_cleanup.php` | Direct | `ALTER TABLE ... ADD INDEX` ×3 |
| F5 | Unit test hàm tra số liệu theo trang đích | `tests/Feature/LandingClickStatHelperTest.php` | Direct | 5 tests / 5 assertions — OK |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `detail_landing_click` | MIGRATE | Thêm chỉ mục `(bot_id, line_id(64), landing_id)`; **KHÔNG đổi dữ liệu** |
| D2 | `time_action_landing` | MIGRATE | Thêm chỉ mục `(bot_id, line_id(64))`; **KHÔNG đổi dữ liệu** |
| D3 | `collect_open_landings` | MIGRATE | Thêm chỉ mục `(bot_id, landing_id)`; **KHÔNG đổi dữ liệu** |
| D4 | `landing` / `landing_histories` | UPDATE | Số liệu trừ đi khi xóa bạn **giữ nguyên công thức cũ**, không thay đổi giá trị |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend List / Friend Delete (outside glossary) — luồng xóa bạn bè trên **web và app** | F1, F2, F3 | Dev đánh giá: chạy nhanh hơn, **logic dọn dữ liệu giữ nguyên** |
| T2 | **Landing Page (FA-011)** — số liệu thống kê trang đích (lượt quét, lượt bấm, lượt kết bạn) | F1, D1, D2, D3, D4 | Dev đánh giá: vẫn bị trừ đúng như trước khi sửa |
| T3 | QR Code / Landing statistics (outside glossary) | D1, D2, D3 | Dev đánh giá: chỉ hưởng lợi từ chỉ mục mới, **không sửa code** |

---

## 5. Recover data

✔ Không cần recover data

## 6. Verify (Dev tự verify)

**Mức:** unit-test

**Lệnh đã chạy:**
- `php -l` 5 file đã sửa: No syntax errors detected
- Boot Laravel (`bootstrap/app.php` + Console Kernel) rồi in `toSql()` của 2 câu tổng hợp mới: giữ nguyên điều kiện `bot_id` + `line_id` + phạm vi xóa mềm (`deleted_at is null`) như các câu COUNT cũ
- In SQL của migration: `ALTER TABLE ... ADD INDEX` đúng 3 bảng, cột và prefix như thiết kế; class migration khớp tên file
- `vendor/bin/phpunit --filter LandingClickStatHelperTest`: OK (5 tests, 5 assertions)
- `git diff --stat release_step_20260827...ai_small_40997`: đúng 5 file

**Bằng chứng:**
- `database/migrations/2020_06_15_182615_detail_landing_click.php`: chỉ có index `landing_id`, không index `line_id`
- `database/migrations/2022_06_13_173633_create_time_action_landing_table.php`: chỉ có index `landing_id`
- `database/migrations/2025_06_19_114922_create_collect_open_landings_table.php` (+2 migration bổ sung cột): không tạo chỉ mục nào
- ⚠️ **MySQL dev (`host.docker.internal:3306`) không kết nối được** trong lần chạy này nên **không EXPLAIN được trên dữ liệu thật** — kết luận dựa trên định nghĩa chỉ mục trong migration của chính repo
- lesson #38390/#40708: cùng endpoint từng chậm vì quét bảng lớn; các nút cổ chai đã fix trước đó (`url_shorten`) đã có mặt trên `release_step_20260827`

## 7. Rủi ro / lưu ý khi test (Dev tự nêu)

- **3 câu ALTER chạy trên bảng log lớn**: MySQL 5.7 thêm secondary index theo `ALGORITHM=INPLACE` nên không chặn đọc/ghi, nhưng vẫn nên **chạy ngoài giờ cao điểm** hoặc bằng `pt-online-schema-change` (đã ghi chú trong migration).
- **Không EXPLAIN được trên dữ liệu thật** vì dev DB không kết nối được; **mức cải thiện thực tế cần đo lại** sau khi lên môi trường có dữ liệu.
- Nếu môi trường thật **đã có sẵn chỉ mục tương đương nhưng khác tên** thì migration vẫn tạo thêm chỉ mục mới (**chỉ kiểm theo tên**) — dư thừa chứ không sai; **DBA nên rà trước khi chạy**.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
