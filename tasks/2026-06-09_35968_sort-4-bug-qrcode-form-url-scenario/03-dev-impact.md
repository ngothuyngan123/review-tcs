# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude parse section "Đánh giá ảnh hưởng" trong Redmine, fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Hạnh Nguyễn` (người viết đánh giá ảnh hưởng) — assigned_to: `Kieu Son Tung` |
| Commit / Pull Request | https://bitbucket.org/snstool/sns-line/pull-requests/10350/overview |
| Branch | `ai_fixbug_35968` (gốc `release_step_20260511`, commit `2a287b6a4d`, 15 file — theo journal AI Auto-fixbug #120468) |
| Ngày submit đánh giá | `2026-06-03` (journal #119876) |
| Auto-filled | `2026-06-09 by /new-task` |

> ℹ️ Redmine #35968 có **2 đánh giá**: journal #119876 (Hạnh Nguyễn, 2026-06-03 — bản có cấu trúc đầy đủ, dùng làm gốc file này) và journal #120468 (AI Auto-fixbug, 2026-06-08 — bổ sung branch/commit). Cả 2 mô tả cùng 1 fix. Commit Date custom field: 2026-06-08.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ journal #119876 mục 1. -->

- Các màn có chức năng sort (QR item/folder, form, message template, url, cross analysis, scenario) dùng jQuery UI sortable kéo-thả trên list render bằng Vue `v-for`, nhưng 2 phía không đồng bộ.
- Khi kéo-thả xong, code chỉ ghi thứ tự mới vào ô ẩn (`#array_sort` / `#array_sort_fol` / `#array_sort_qr`) để submit, KHÔNG cập nhật lại mảng dữ liệu của Vue (`arrGroupSort`, `dataSortForm`, `items_sort`/`items_default_sort`, `arrItemsSort`, `item_all`). Trong khi đó nút sort lên/xuống dùng index của `v-for` và đặt `:disabled` theo `index == 0` / `index == length - 1`. Sau khi kéo-thả, mảng Vue vẫn theo thứ tự cũ nên index lệch với thứ tự hiển thị → click sort không phản hồi / nhảy sai vị trí (**bug 1, 2**).
- List `v-for` thiếu `:key="item.id"` (hoặc dùng `:key="index"`). Khi sortable đổi thứ tự DOM, Vue tái sử dụng node theo index nên trạng thái nút và `:disabled` bị gán nhầm sang item khác → item ở vị trí 2 mà nút sort lên bị disable, item dưới cùng vẫn hiện nút sort xuống (**bug 3, 4**).

## 2. Cách fix

<!-- Nguyên văn từ journal #119876 mục 2. -->

- Thêm `:key="item.id"` cho `v-for` ở tất cả modal sort (form, message template item/folder, QR item/folder, url item/folder, cross folder, scenario item/folder) — riêng các chỗ đang dùng `:key="index"` thì đổi thành `:key="item.id"` — để Vue track đúng từng item khi đổi thứ tự.
- Trong handler update của sortable: sau khi đọc thứ tự id mới từ DOM, lọc bỏ id rỗng, dựng lại mảng dữ liệu Vue theo đúng thứ tự DOM mới (map id → item rồi gán lại) cho `arrGroupSort` / `dataSortForm` / `items_sort` / `items_default_sort` / `arrItemsSort` / `item_all` → index và trạng thái disable của nút lên/xuống luôn khớp thứ tự hiển thị.
- Thêm biến `self` trong các hàm `openModalSortItem` / `openModalSortFolder` / `openModalSortQr` để callback sortable tham chiếu đúng instance Vue khi gán lại mảng dữ liệu.

> 📌 Mẫu chuẩn: fix theo đúng pattern đã được duyệt ở màn **Tag** (`tag/v2`, `index_v2.js` + `index.blade.php`) đang chạy production. Đây là ticket 横展開 (triển khai ngang) áp mẫu đó sang 6 màn.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn từ journal #119876 mục 3. -->

- Các biến được dựng lại (`arrGroupSort`, `dataSortForm`, `items_sort`, `items_default_sort`, `arrItemsSort`, `item_all`) đều là data nội bộ của từng Vue instance — đã rà soát, chỉ dùng trong chính modal sort tương ứng, không ảnh hưởng màn khác.
- Logic submit thứ tự (ô ẩn `#array_sort` / `#array_sort_fol` / `#array_sort_qr` → API lưu sort) giữ nguyên, không đổi → việc lưu thứ tự xuống server không thay đổi.

> ℹ️ Journal AI #120468 bổ sung: màn **Cross — sort item** (`showModalSortItems`) dùng ajax + nút (không kéo-thả), đã có `:key`, **không cần sửa**. Màn **URL** là button-based (không có jQuery sortable), chỉ thêm `:key` cho đồng bộ.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn list file/function từ journal #119876 mục 4.1. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | sortable `.sort-folder` update — dựng lại `arrGroupSort` theo thứ tự kéo-thả | `public/js/cross_analysis/index.js` | Direct | Cross analysis |
| F2 | `openModalSortItem()` dựng lại `dataSortForm`; `openModalSortFolder()` dựng lại `arrGroupSort` | `public/js/form_answer/index_v3.js` | Direct | Form answer |
| F3 | sortable `.sort-folder` (dựng lại `arrGroupSort`) + `.sort-list` (dựng lại `items_default_sort`/`items_sort` theo `group_open`) | `public/js/msg_template/index.js` | Direct | Message template |
| F4 | `openModalSortQr()` dựng lại `arrItemsSort`; `openModalSortFolder()` dựng lại `arrGroupSort` | `public/js/qr_code/v2/index.js` | Direct | QR code |
| F5 | sortable `.sort-folder` (dựng lại `arrGroupSort`) + `.sort-list` (dựng lại `item_all`) | `public/js/scenario/index_v2.js` | Direct | Scenario |
| F6 | thêm `:key="item.id"` cho `v-for` `arrGroupSort` | `resources/views/basic/cross_analysis/v2/modal/sort_folder.blade.php` | Direct | Cross folder |
| F7 | thêm `:key="item.id"` cho `v-for` `arrGroupSort` | `resources/views/basic/form_answer/index_v3.blade.php` | Direct | Form folder |
| F8 | thêm `:key="item.id"` cho `v-for` `dataSortForm` | `resources/views/basic/form_answer/modal/modal_sort_form.blade.php` | Direct | Form sort item |
| F9 | thêm `:key="item.id"` cho `v-for` `arrGroupSort` | `resources/views/basic/message_template/index.blade.php` | Direct | Template folder |
| F10 | đổi `:key="index"` → `:key="item.id"` cho `items_default_sort` và `items_sort` | `resources/views/basic/message_template/partials/modal_sort.blade.php` | Direct | Template sort item |
| F11 | thêm `:key="item.id"` cho `v-for` `arrGroupSort` | `resources/views/basic/qr_code/v2/modal/sort_folder.blade.php` | Direct | QR folder |
| F12 | thêm `:key="item.id"` cho `v-for` `arrItemsSort` | `resources/views/basic/qr_code/v2/modal/sort_qr.blade.php` | Direct | QR sort item |
| F13 | đổi `:key="index"` → `:key="item.id"` cho `arrGroupSort` và `item_all` | `resources/views/basic/scenario/scenario_index.blade.php` | Direct | Scenario item + folder |
| F14 | thêm `:key="url_sort.id"` cho `v-for` `list_url_sort`; thêm `:key="item.id"` cho `v-for` `folders_sort` | `resources/views/basic/url/index_v2.blade.php` | Direct | URL item + folder (button-based) |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn từ journal #119876 mục 4.2. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** | — | Chỉ sửa logic FE đồng bộ thứ tự hiển thị; thứ tự sort vẫn lưu qua API cũ, không đổi backend / không đổi cột DB. Journal AI #120468: không có dữ liệu hỏng cần backfill, không cần recover data. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn từ journal #119876 mục 4.3 (+ ghi chú risk từ Dev). -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn **QR code**: sort item (並べ替え) và sort folder (フォルダ並べ替え) | F4, F11, F12 | Medium |
| T2 | Màn **Form answer**: sort form và sort folder | F2, F7, F8 | Medium |
| T3 | Màn **Message template**: sort template (ngoài folder và trong folder) và sort folder | F3, F9, F10 | Medium |
| T4 | Màn **URL**: sort url và sort folder (button-based, không kéo-thả — chỉ thêm `:key`) | F14 | Low |
| T5 | Màn **Cross analysis**: sort folder (sort item dùng ajax+nút, không sửa) | F1, F6 | Low |
| T6 | Màn **Scenario**: sort item và sort folder | F5, F13 | Medium |

> ⚠️ **Lưu ý khi test (từ Dev tự review, journal AI #120468):**
> - So khớp id dùng `item.id === parseInt(data-id)`: an toàn vì id thư mục/template/form/scenario đều là số (PK auto-increment). Nếu màn nào có id chuỗi sẽ rớt item — đã rà soát không có.
> - jQuery sortable + Vue keyed re-render: cùng tập key (chỉ đổi thứ tự) nên reconcile không xoá node.
> - Container không chạy app thật nên **chưa test runtime** — mới verify `node -c` (5 file JS) + `php -l` (9 blade). → cần test thủ công kỹ trên Staging.
> - Cùng pattern còn tồn tại ở nhiều màn KHÁC ngoài 6 màn ticket (popup, image_richmenu, sales, reply, conversion, events, action_schedules, booking_event, rich_menu, infor_friend...) — gợi ý 横展開 tiếp ở ticket sau, **ngoài scope ticket này**.

---

## Leader xác nhận trước khi giao TCs

- [ x] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ x] Mục 2 (cách fix) có thể trace về code
- [ x] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ x] Mục 4.1 không thiếu function (so với mục 3)
- [ x] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ x] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ x] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
