# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `<chưa có PR>` — repo `sns-line`, commit `ec1ce93f3b` (nhánh gốc `release_step_20260623`) |
| Branch | `ai_fixbug_39263` (đã push origin) |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-09-14 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ **Điểm nghi vấn cần hỏi Dev trước khi chốt coverage** (do `/new-task` phát hiện khi map, KHÔNG phải nội dung Dev viết):
> 1. **Mâu thuẫn số file sửa**: mục 4.1 + mục 6 ghi **2 file** (`FilterController.php`, `functions.php`); dòng BRANCH/COMMIT ghi `commit ec1ce93f3b, **4 file**`.
> 2. **Mâu thuẫn vị trí fix**: mục 2 nói fix nằm trong `UserController::editRichMenuForm` và "chỉ sửa trong hàm này", nhưng `UserController.php` **không** nằm trong danh sách file thay đổi ở 4.1.
> 3. **Mục 4.1 kê theo FILE, không kê theo FUNCTION** → chưa đủ granularity để map coverage; bảng 4.1 bên dưới giữ nguyên mức file Dev cung cấp, cần Dev bổ sung tên hàm cụ thể đã đổi.
> 4. **Mức verify chỉ là `lint`** — Dev không chạy được dev stack (MySQL Connection refused), không có bằng chứng runtime nào cho cả fix lẫn regression.

---

## 1. Nguyên nhân

Khi TẠO MỚI richmenu thì richmenu chưa có id, nên filter của action chuyển richmenu được lưu tạm với `parent_id` rỗng và mã vùng âm. Phía server, hàm nạp lại filter bỏ qua toàn bộ truy vấn khi `parent_id` rỗng nên mở lại modal không thấy filter nào. Cùng lý do, khi bấm lưu richmenu mới các filter tạm cũng không được gắn lại vào richmenu/vùng vừa tạo (câu lệnh gắn lại bắt buộc khớp `parent_id = id richmenu`) nên mở lại từ màn sửa cũng không thấy filter.

## 2. Cách fix

Sửa theo AI review vòng 2: khi mở form TẠO MỚI richmenu (route `/basic/rich-menu/create`, không có id), phần dọn filter tạm ở `UserController::editRichMenuForm` trước đây lọc theo `parent_id = null` nên không khớp các bản ghi tạm được lưu với `parent_id` rỗng (cột int, lưu thành `0`) — filter tạm của phiên tạo mới bỏ dở (đóng tab/tải lại trang) nằm lại vĩnh viễn, và sau khi có fix nạp lại filter thì chúng hiện lên ở phiên tạo mới sau và bị gắn thật vào richmenu vừa tạo. Nay giữ nguyên nhánh cũ khi có id richmenu (luồng sửa), còn khi không có id thì dọn đúng phạm vi mà phần nạp lại dùng: cùng bot, loại filter chuyển richmenu, mã vùng âm và `parent_id` rỗng (`null` hoặc `0`). Chỉ sửa trong hàm này, không đụng luồng sửa richmenu.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev list dạng plain, convert sang bảng. Cột "Thay đổi" để `<Dev không ghi rõ>` khi journal không nêu — KHÔNG suy đoán. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FilterController::initDataFilter` — `app/Http/Controllers/Basic/FilterController.php` | Có sửa (file nằm trong 4.1) — hàm nạp lại filter cho modal | Đây là chỗ bỏ qua truy vấn khi `parent_id` rỗng ⇒ nguyên nhân modal trống |
| 2 | `FilterController::saveFilterV2` — `app/Http/Controllers/Basic/FilterController.php` | `<Dev không ghi rõ>` | Đường lưu filter tạm (`parent_id` rỗng, mã vùng âm) |
| 3 | `FilterV2::saveFilter` — `app/FilterV2.php` | `<Dev không ghi rõ>` (file KHÔNG có trong 4.1) | Model ghi filter |
| 4 | `buildAreaRichmenu` — `app/Helpers/functions.php` | Có sửa (file nằm trong 4.1) | Chỗ gắn lại filter tạm về richmenu/vùng khi lưu richmenu mới |
| 5 | `UserController::getRichMenu` — `app/Http/Controllers/Basic/UserController.php` | `<Dev không ghi rõ>` (file KHÔNG có trong 4.1) | Trả `data = null` ở luồng create ⇒ `rich_menu_detail.id` rỗng |
| 6 | `UserController::editRichMenuForm` — `app/Http/Controllers/Basic/UserController.php` | Mục 2 nói **có sửa** nhưng file KHÔNG có trong 4.1 ⇒ ⚠️ mâu thuẫn | Phần dọn filter tạm (`rich_menu_item_id < 0`) |
| 7 | `showModalFilterV2RichMenuToggle` — `public/_assets/modules/rich_menu/js/create.js` | `<Dev không ghi rõ>` | FE mở modal filter cho richmenu đích |
| 8 | `initDataStep3` / `prepareFormData` — `public/_assets/modules/rich_menu/js/create.js` | `<Dev không ghi rõ>` | Sinh mã vùng âm `0-1-i` ở bước 3 |
| 9 | `initDataFilter` + `saveFilterV2` phía modal — `public/js/friendlist/modal_filter_v2.js` | `<Dev không ghi rõ>` | Modal filter V2 **dùng chung nhiều màn** ⇒ vùng regression |
| 10 | `HandlePostbackTask` switch richmenu — `linect-service` | Chỉ đọc, không sửa | Xác nhận runtime dùng `filter_ids` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- ⚠️ Dev kê mục 4.1 theo FILE, không theo function. Giữ nguyên mức Dev cung cấp. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FilterController` (nạp/lưu filter modal — `initDataFilter`, `saveFilterV2`) | `app/Http/Controllers/Basic/FilterController.php` | Direct | Dev kê ở mục "4.1 File thay đổi" |
| F2 | `buildAreaRichmenu` (helper gắn filter về richmenu/vùng khi lưu) | `app/Helpers/functions.php` | Direct | Dev kê ở mục "4.1 File thay đổi" |
| F3 | `UserController::editRichMenuForm` (dọn filter tạm) | `app/Http/Controllers/Basic/UserController.php` | ⚠️ Mục 2 mô tả là chỗ sửa chính, nhưng KHÔNG có trong danh sách file thay đổi | Cần Dev xác nhận |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `filters_v2.parent_id` | UPDATE | Từ nay filter tạo trong lúc tạo mới richmenu được gắn lại đúng richmenu khi lưu |
| D2 | `filters_v2.rich_menu_item_id` | UPDATE | Gắn lại đúng **vùng** bấm thật (thay cho mã vùng âm tạm) |
| D3 | `filters_v2` — bản ghi nháp mồ côi (`parent_id` rỗng/`0`, mã vùng âm) | DELETE | Dọn khi mở form tạo mới: cùng bot + loại filter chuyển richmenu + mã vùng âm + `parent_id` null/0 |
| D4 | Dữ liệu cũ đã lưu sai trước bản fix | (không đụng) | Dev ghi "vẫn còn mồ côi" nhưng mục 5 kết luận **không cần recover data** ⇒ ⚠️ rủi ro dữ liệu cũ hồi sinh sai chỗ, cần TC verify |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Rich Menu (FA-004) — filter của action chuyển richmenu trong luồng **tạo mới** richmenu | F1, F2, F3, D1, D2, D3 | High |
| T2 | Friend Filter (SC-003) — modal lọc bạn nạp lại điều kiện đã lưu khi **chưa có bản ghi cha** | F1, D1 | High — modal `modal_filter_v2.js` dùng chung nhiều ngữ cảnh (một lần gửi, cài đặt hiển thị richmenu, preview từ màn danh sách) |
| T3 | Rich Menu — luồng **sửa** richmenu đã lưu | F3 (nhánh "có id" giữ nguyên) | Medium — Dev khẳng định không đụng, cần TC chứng minh |

---

## 5. Recover data (nguyên văn Dev)

> ✔ Không cần recover data

## 6. Verify của Dev (nguyên văn)

> **Mức: lint**
> Lệnh: `php -l app/Http/Controllers/Basic/FilterController.php: OK`; `php -l app/Helpers/functions.php: OK`; `git diff --stat release_step_20260623...ai_fixbug_39263: chỉ 2 file đã sửa`
> Bằng chứng: Không tái hiện được trên dev: MySQL `host.docker.internal:3306` trả về Connection refused (dev stack không chạy); Đọc code xác nhận luồng tạo mới richmenu không có id richmenu: `/basic/rich-menu/create` không tạo bản ghi (`quickAddRichMenu` chỉ update khi đã có id), `getRichMenu` trả data null nên `rich_menu_detail.id` rỗng; `layout_actions[i].id = 0-1-i` (mã vùng âm) trong `initDataStep3`, khớp với chỗ dọn rác `rich_menu_item_id < 0` ở `editRichMenuForm`

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
