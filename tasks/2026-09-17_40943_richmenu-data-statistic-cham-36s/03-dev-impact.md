# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | commit `fe4d32fa54` (2 file) — Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40943 |
| Branch | `ai_small_40943` (repo `sns-line`, nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-15 (Journal #136535) |
| Auto-filled | `2026-09-17 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Màn thống kê rich menu đếm lượt bấm bằng **MỘT câu đếm riêng cho TỪNG ngày × TỪNG vùng bấm**, cộng thêm **một câu đếm tổng cho từng vùng**. Khoảng ngày càng dài thì số câu lệnh càng nhiều — **đặc biệt khi tải CSV**, lúc này màn **không phân trang** nên lấy trọn khoảng (URL chậm nhất 36 giây có khoảng gần 11 tháng = **327 ngày**), nhân với số vùng của rich menu thành **hàng nghìn câu đếm cho một request**.

Mỗi câu lại lọc ngày bằng hàm `DATE()` bọc lên cột thời gian bấm nên **MySQL không dùng được chỉ mục**, phải mở và quét toàn bộ lịch sử bấm của vùng đó rồi mới lọc; bảng nhật ký bấm cũng **chỉ có chỉ mục một cột** (vùng bấm / rich menu), chưa có chỉ mục phù hợp cho bộ lọc **bot + vùng + thời gian**.

## 2. Cách fix

Viết lại phần đếm lượt bấm của màn thống kê rich menu:

1. **Thay hàng nghìn câu đếm lặp** (mỗi ngày × mỗi vùng, cộng mỗi vùng một câu tổng) bằng **ĐÚNG 2 câu truy vấn tổng hợp**:
   - một câu gom theo `(vùng, ngày)` cho **bảng chi tiết**
   - một câu gom theo `vùng` cho **dòng tổng**

   rồi ghép kết quả trong PHP theo **đúng thứ tự vùng và ngày như cũ**.
2. **Đổi điều kiện lọc ngày** từ `DATE(time_click)` sang so sánh **khoảng thời gian nửa mở** (`>=` đầu ngày bắt đầu, `<` đầu ngày sau ngày kết thúc) để MySQL dùng được chỉ mục.
3. **Thêm migration** tạo chỉ mục ghép `(bot_id, rich_item_id, time_click)` cho bảng nhật ký bấm rich menu (migration **idempotent**, kiểm tra `information_schema` trước khi tạo/xoá).

**Số liệu trả về không đổi** — Dev đã kiểm tương đương cả ở biên đầu/cuối ngày, bản ghi ngoài kỳ, bản ghi của bot khác và bản ghi thời gian rỗng.

**Quét ngang:** còn 1 chỗ **TRÙNG y hệt pattern** ở màn thống kê rich menu **bản cũ** (`Basic/UserController::ajaxInitDataDetail`) — **CHƯA sửa** vì ngoài phạm vi ticket, đã ghi trong mục yokoten.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `RichMenuService::calculateStatistic` — `app/Services/V2/RichMenuService.php:397` | **Đã viết lại** | Điểm chậm chính |
| 2 | `RichMenuService::startOfDay` / `startOfNextDay` — `app/Services/V2/RichMenuService.php:496,504` | **Helper mốc ngày mới thêm** | Dựng khoảng nửa mở cho điều kiện lọc ngày |
| 3 | `RichMenuController::dataStatistic` — `app/Http/Controllers/V2/RichMenuController.php:453` | Không đổi | Endpoint bị báo chậm, chỉ gọi service |
| 4 | `StatisticRickMenuExport::array` / `headings` — `app/Exports/StatisticRickMenuExport.php` | Không đổi | Bên tiêu thụ CSV — xác nhận hình dạng dữ liệu `detailClick` / `countTotal` giữ nguyên |
| 5 | `UserController::ajaxInitDataDetail` — `app/Http/Controllers/Basic/UserController.php:1410` | **KHÔNG sửa** (ngoài phạm vi) | Bản cũ cùng pattern chậm |
| 6 | `DetailClickRichmenuRepository` (linect-service) | Không đổi | Chỉ ghi, không có truy vấn đọc nào bị ảnh hưởng |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Journal Dev mục 4.1 liệt kê theo **file thay đổi** (2 file). Bảng dưới giữ nguyên danh sách file + map sang function ở mục 3.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `RichMenuService::calculateStatistic` + helper mới `startOfDay` / `startOfNextDay` | `app/Services/V2/RichMenuService.php` | Direct | 2 câu gom thay câu đếm lặp; lọc ngày nửa mở |
| F2 | Migration thêm chỉ mục ghép `detail_click_richmenu_statistic_index` | `database/migrations/2026_09_14_100000_add_statistic_index_to_detail_click_richmenu_table.php` | Direct | Idempotent — kiểm `information_schema` trước khi tạo/xoá |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `detail_click_richmenu` — chỉ mục `detail_click_richmenu_statistic_index (bot_id, rich_item_id, time_click)` | MIGRATE | **THÊM chỉ mục**, không sửa/xoá dữ liệu. Cần chạy migration khi release; bảng lớn → ALTER TABLE tốn thời gian và dung lượng đĩa (MySQL 5.6+ thêm index online, không khoá ghi) → chạy giờ thấp điểm |
| D2 | `detail_click_richmenu` — đường ghi log bấm (linect-service insert) | (gián tiếp) | Mỗi lần ghi log bấm tốn thêm chi phí cập nhật 1 chỉ mục; đổi lại đọc thống kê nhanh hơn nhiều lần |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Rich Menu (FA-004)** — màn **Thống kê rich menu**: bảng lượt bấm theo ngày × vùng, dòng tổng, và **tải CSV** | F1, F2, D1 | Dev đánh giá: số liệu giữ nguyên, chỉ đổi cách truy vấn cho nhanh |

---

## 5. Recover data

✔ Không cần recover data

## 6. Verify (Dev tự verify)

**Mức:** lint

**Lệnh đã chạy:**
- `php -l app/Services/V2/RichMenuService.php`: No syntax errors detected
- `php -l database/migrations/2026_09_14_100000_add_statistic_index_to_detail_click_richmenu_table.php`: No syntax errors detected
- Boot Laravel trong worktree (vendor copy thật + `composer dump-autoload`) rồi in `toSql()`:
  - câu 1 = `select rich_item_id, DATE(time_click) as day_click, COUNT(*) as total_click from detail_click_richmenu where bot_id = ? and rich_item_id in (?, ?, ?) and time_click >= ? and time_click < ? group by rich_item_id, DATE(time_click)`
  - câu 2 = cùng dạng, `group by rich_item_id`
  - câu CŨ in ra `date(time_click) = ?` — xác nhận đúng chỗ bọc hàm làm hỏng index
- Kiểm 2 helper mốc ngày: `startOfDay(2026-09-08)=2026-09-08 00:00:00`; `startOfNextDay(2026-09-14)=2026-09-15 00:00:00`
- Test tương đương ngữ nghĩa (PHP thuần, mô phỏng cả 2 vị từ trên cùng tập dữ liệu có bản ghi biên `00:00:00` và `23:59:59`, bản ghi trước/sau kỳ, bản ghi bot khác, bản ghi `time_click` rỗng): detail OLD==NEW PASS, total OLD==NEW PASS
- Xác nhận Laravel 5.5 `Query\Builder::groupBy` là variadic và `columnize` giữ nguyên Expression (`vendor/laravel/framework .../Builder.php:1318`)

**Bằng chứng:**
- Chỉ mục hiện có của bảng (migration `2022_08_18_175625_create_detail_click_richmenu_table.php`): chỉ `rich_id` và `rich_item_id`, mỗi cái 1 cột; KHÔNG có `bot_id`, KHÔNG có `time_click`
- URL chậm nhất có `download_csv=1` và khoảng `2025-10-23..2026-09-14` (327 ngày); code bỏ qua `array_slice` khi `download_csv=1` nên `listDay` giữ trọn 327 ngày → 327 × số vùng câu đếm, khớp mức 36 giây
- Các URL 6–7 giây còn lại là khoảng 7–13 ngày, `per_page=100` → vài chục câu đếm, khớp mức SLOWLV1
- ⚠️ **KHÔNG kiểm được trên MySQL thật**: dev DB `host.docker.internal:3306` connection refused, container chỉ có PDO driver mysql (không có pdo_sqlite) → **chưa chạy EXPLAIN, chưa đo thời gian thực tế**

## 7. Tự review + rủi ro / lưu ý khi test (Dev tự nêu)

**Tự review (AI):** Fix bám đúng root cause và tối thiểu: giữ nguyên toàn bộ hình dạng dữ liệu trả về (`detailClick` là mảng theo index ngày với khoá `day` + `data` theo đúng thứ tự vùng đã sort; `countTotal` là mảng theo đúng thứ tự vùng) nên màn hình, phân trang và lớp xuất CSV không phải sửa gì. Vẫn đếm **SỐ DÒNG** (`COUNT(*)`) chứ không đổi sang cộng cột `count`, đúng như hành vi cũ. Hai câu mới dùng khoảng datetime nửa mở, đã đối chiếu tương đương với `whereDate` ở cả 4 tình huống biên. **Có bổ sung khởi tạo `data = []` cho mỗi ngày** (trước đây khi rich menu không có vùng nào thì khoá `data` không tồn tại) — an toàn hơn cho lớp xuất CSV và không đổi kết quả.

**Rủi ro / lưu ý khi test:**
- **Migration thêm chỉ mục trên bảng nhật ký click cỡ lớn**: ALTER TABLE chạy lâu và tốn dung lượng tạm. Thêm index là thao tác online từ MySQL 5.6 (không chặn ghi) nhưng vẫn nên chạy vào giờ thấp điểm và theo dõi đĩa.
- **Thêm 1 chỉ mục làm mỗi lần ghi log bấm tốn thêm chút chi phí** (bảng này ghi liên tục từ job linect). Đánh đổi chấp nhận được vì đường đọc đang chậm tới 36 giây.
- **Chưa đo được trên MySQL thật** (dev DB đang tắt) nên **chưa có EXPLAIN** xác nhận optimizer chọn đúng chỉ mục mới. Đề nghị người review chạy EXPLAIN 2 câu trên môi trường có dữ liệu thật sau khi chạy migration.
- Câu gom theo (vùng, ngày) trả về tối đa (số ngày × số vùng) dòng — với 1 năm và 20 vùng là khoảng 7.300 dòng, nhẹ; không có rủi ro bộ nhớ.
- **Endpoint bản cũ `ajaxInitDataDetail` vẫn còn nguyên pattern chậm** (xem yokoten) — nếu khách dùng màn cũ thì vẫn có thể gặp lại triệu chứng.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
