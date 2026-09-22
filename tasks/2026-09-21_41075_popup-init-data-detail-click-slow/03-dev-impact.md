# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `ccffbeed6c` (3 file) — Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41075 |
| Branch | `ai_small_41075` (nhánh gốc `release_step_20260827`) — repo sns-line, đã push |
| Ngày submit đánh giá | `2026-09-21` (Journal #137307) |
| Auto-filled | `2026-09-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Endpoint phục vụ màn Chi tiết dữ liệu click của Popup. Tab thống kê theo ngày chạy vòng lặp TỪNG NGÀY trong khoảng lọc, mỗi ngày bắn 2 query riêng (N+1): đếm hiển thị/click và đếm bạn bè thêm mới; query đếm hiển thị/click còn tải TOÀN BỘ bản ghi ra PHP rồi đếm bằng vòng lặp thay vì đếm bằng SQL.

Nặng nhất là 2 bảng nhật ký này chỉ có khoá chính, **KHÔNG có index theo mã popup + thời gian**, nên mỗi query là một lần quét toàn bảng nhật ký khổng lồ (bảng ghi 1 dòng cho mỗi lần popup hiển thị của mọi bot). Chọn khoảng 30-90 ngày tương đương **60-180 lần quét toàn bảng nối tiếp nhau**, gây treo tới 135s.

## 2. Cách fix

Gom N+1 query trong `PopupService::getDataActionPopup`: thay vì gọi 2 query cho MỖI ngày, nay gọi **2 query tổng hợp GROUP BY ngày cho cả khoảng lọc** rồi ghép kết quả theo từng ngày trong PHP (số query cố định = 2, không phụ thuộc số ngày).

Thêm 2 hàm range mới trong `PopupRepository` (`countDataActionPopupByTypeInRange`, `countDataAddFriendByPopupInRange`) và sửa hàm đếm theo ngày cũ để **đếm bằng COUNT/SUM trong SQL** thay vì tải toàn bộ bản ghi ra PHP đếm bằng vòng lặp.

Thêm **migration tạo index `(popup_id, created_at)`** cho 2 bảng nhật ký `detail_action_popup` và `detail_landing_click` (trước đó chỉ có khoá chính nên mọi truy vấn theo popup đều quét toàn bảng).

Đã bỏ 1 dòng ghi log debug vô nghĩa trong vòng lặp ngày.

**Dữ liệu trả về giữ nguyên tuyệt đối** — đã kiểm chứng bằng harness so sánh output bản cũ vs bản mới trên cùng dữ liệu, chỉ khác số lần gọi repository (10 lần còn 2 lần với khoảng 5 ngày).

**Quét ngang**: mẫu vòng lặp truy vấn theo ngày còn ở Cross Analysis / Calendar / Admin User nhưng khác tính năng và khác bảng nên **để ngoài scope**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `PopupAjaxController::initDataDetailClick` — `app/Http/Controllers/Ajax/PopupAjaxController.php:563` | Không sửa | Entry point của endpoint bị chậm |
| 2 | `PopupService::getDataActionPopup` — `app/Services/PopupService.php:471` | **ĐÃ SỬA** | Nơi chứa vòng lặp N+1 theo ngày |
| 3 | `PopupRepository::countDataActionPopupByType` — `app/Repositories/Eloquents/PopupRepository.php:87` | **ĐÃ SỬA** | Đổi từ tải bản ghi ra PHP đếm → COUNT/SUM trong SQL |
| 4 | `PopupRepository::countDataActionPopupByTypeInRange` — `PopupRepository.php:116` | **MỚI** | Query gộp GROUP BY ngày cho cả khoảng |
| 5 | `PopupRepository::countDataAddFriendByPopup` — `PopupRepository.php:133` | Không sửa | Hàm đếm bạn mới theo ngày (bản cũ) |
| 6 | `PopupRepository::countDataAddFriendByPopupInRange` — `PopupRepository.php:157` | **MỚI** | Query gộp đếm bạn mới cho cả khoảng |
| 7 | `getBetweenDates` — `app/Helpers/functions.php:10018` | Chỉ đọc, giữ nguyên | Sinh danh sách ngày trong khoảng. Grep toàn repo: chỉ DUY NHẤT `PopupService::getDataActionPopup` gọi |
| 8 | `PopupController::detailDataClick` — `app/Http/Controllers/Basic/PopupController.php:86` | Không sửa | Nguồn khoảng ngày mặc định của màn |
| 9 | `BotController` — `app/Http/Controllers/Admin/BotController.php:8008` | Không sửa | Xoá theo `popup_id` — hưởng lợi từ index mới |
| 10 | `FlowDeleteBot` — `app/Console/Commands/FlowDeleteBot.php:481` | Không sửa | Xoá theo `popup_id` — hưởng lợi từ index mới |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Dev kê ở mục "4.1 File thay đổi" dạng danh sách file. Quy về tag `F*` để map coverage:

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `PopupService::getDataActionPopup` | `app/Services/PopupService.php` | Direct | Gom N+1 → 2 query GROUP BY ngày cho cả khoảng; ghép kết quả theo ngày trong PHP; bỏ 1 dòng log debug trong vòng lặp |
| F2 | `PopupRepository::countDataActionPopupByType` (sửa) + `countDataActionPopupByTypeInRange` (mới) | `app/Repositories/Eloquents/PopupRepository.php` | Direct | Đếm hiển thị/click — chuyển sang COUNT/SUM trong SQL |
| F3 | `PopupRepository::countDataAddFriendByPopupInRange` (mới) | `app/Repositories/Eloquents/PopupRepository.php` | Direct | Đếm bạn thêm mới gộp cả khoảng; vẫn giữ ràng buộc soft-delete `deleted_at is null` |
| F4 | Migration thêm index 2 bảng log | `database/migrations/2026_09_18_000001_add_index_popup_id_created_at_for_detail_log_tables.php` | Direct | Idempotent (kiểm tra index tồn tại trước khi thêm) |
| F5 | `PopupAjaxController::initDataDetailClick` | `app/Http/Controllers/Ajax/PopupAjaxController.php:563` | Indirect | Không sửa, nhưng là entry point — hợp đồng response phải giữ nguyên |
| F6 | `BotController` (`:8008`) · `FlowDeleteBot` (`:481`) | như cột trước | Indirect | Xoá theo `popup_id`, không sửa code, hưởng lợi gián tiếp từ index mới |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `detail_action_popup` — index `idx_dap_popup_id_created_at (popup_id, created_at)` | MIGRATE (thêm index) | CHỈ ĐỌC trong luồng sửa. Không đổi cột/dữ liệu. **Ảnh hưởng ghi**: mỗi lần chèn bản ghi hiển thị/click popup phải cập nhật thêm 1 index (chi phí ghi tăng nhẹ) |
| D2 | `detail_landing_click` — index `idx_dlc_popup_id_created_at (popup_id, created_at)` | MIGRATE (thêm index) | CHỈ ĐỌC trong luồng sửa. Không đổi cột/dữ liệu. **Ảnh hưởng ghi**: mỗi lần chèn bản ghi click/thêm bạn từ landing tốn thêm 1 index |
| D3 | Log ứng dụng | DELETE (bỏ 1 dòng ghi log debug trong vòng lặp ngày) | Số dòng log sinh ra giảm — dùng được làm dấu hiệu quan sát việc đã bỏ vòng lặp theo ngày |

**⚠️ LƯU Ý VẬN HÀNH (nguyên văn Dev)**: 2 bảng này là nhật ký lớn, chạy migration thêm index nên làm vào **giờ thấp điểm**. MySQL 5.6+ thêm index kiểu INPLACE (online DDL) nên vẫn cho phép ghi trong lúc chạy, nhưng vẫn cần theo dõi thời gian và dung lượng đĩa cho index mới.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Popup (FA-018)** — màn Chi tiết dữ liệu click của popup: bảng thống kê theo ngày (số hiển thị, số click, tỉ lệ click, số bạn thêm mới, tỉ lệ thêm bạn) | F1, F2, F3, D1, D2 | **High** — nhanh hơn nhiều, số liệu phải giữ nguyên |
| T2 | **QR Code Action / Landing (FA-017)** — dùng chung bảng nhật ký click landing | D2 | **Medium** — chỉ nhận thêm 1 index, không đổi logic, truy vấn theo popup nhanh hơn |
| T3 | **Popup Ads Setting (FS-006)** — cùng nhóm cấu hình popup | D1, D2 | **Low** — không đụng logic, chỉ hưởng lợi gián tiếp từ index |

---

## 5. Recover data

✔ Không cần recover data.

## 6. Verify của Dev (nguyên văn, mức: unit-test)

- `php -l` 3 file: No syntax errors detected.
- Kiểm SQL sinh ra bằng Eloquent (`toSql` + bindings): 2 query range đúng cú pháp, tham số hoá đầy đủ, giữ nguyên điều kiện `where` của bản cũ và vẫn có ràng buộc soft-delete (`deleted_at is null`) của bảng click landing.
- Harness so sánh output bản **CŨ** vs bản **MỚI** của `getDataActionPopup` trên cùng tập dữ liệu giả lập (3 ca: khoảng 5 ngày có ngày trống · khoảng 1 ngày · khoảng `start > end`): **JSON kết quả GIỐNG HỆT**, chỉ khác số lần gọi repository 10 → 2.
- ⚠️ **Chưa chạy được EXPLAIN** trên MySQL dev (`host.docker.internal:3306` Connection refused) — kết luận thiếu index dựa trên migration tạo bảng (chỉ có `increments('id')`) và không có migration nào thêm index cho `popup_id`/`created_at`.
- Không viết PHPUnit: thay đổi thuộc nhóm truy vấn DB (repository), không phải logic thuần theo quy tắc B4c.

**Bằng chứng**: `2022_07_12_133040_create_tbl_detail_action_popup.php` chỉ tạo `increments('id')` + `popup_id` + `browser` + `action` + timestamps, KHÔNG có index nào cho `popup_id`/`created_at`; `2020_06_15_182615_detail_landing_click.php` chỉ index `landing_id`; migration `2025_06_13_164227` định thêm index `post_code` nhưng dòng đó bị comment; schema-annotated của `detail_action_popup` ghi rõ `[SIZE] Unbounded — needs archival`; grep toàn repo: `getBetweenDates` chỉ có DUY NHẤT 1 nơi gọi.

## 7. Rủi ro / lưu ý khi test (Dev tự nêu)

1. Migration thêm index trên 2 bảng nhật ký lớn — nên chạy **giờ thấp điểm**, theo dõi thời gian chạy và dung lượng đĩa; migration đã viết **idempotent** nên chạy lại an toàn.
2. **Chi phí ghi tăng nhẹ** ở 2 bảng nhật ký do phải cập nhật thêm index mỗi lần chèn.
3. ⚠️ **Rủi ro cao nhất**: phép gộp theo ngày dùng `DATE(created_at)` của MySQL trong khi bản cũ so sánh khoảng thời gian trong PHP — Dev khẳng định cả hai chạy trên cùng múi giờ phiên MySQL nên kết quả trùng khớp; điều kiện lọc khoảng vẫn để nguyên dạng so sánh khoảng nên index vẫn được dùng (không bọc hàm quanh cột trong `WHERE`). → **Cần TC bắt biên nửa đêm 00:00:00 / 23:59:59.**
4. ⚠️ **Chưa đo được thời gian thực tế trên môi trường có dữ liệu lớn** vì MySQL dev trong container không kết nối được — cần theo dõi lại số liệu giám sát sau khi release.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
