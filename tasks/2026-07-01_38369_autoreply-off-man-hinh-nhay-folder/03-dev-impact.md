# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #38369 (journal "AI LME Fix bug" — báo cáo Auto-fixbug) bởi `/new-task`. Tester verify rồi tick checkbox.
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME` |
| Commit / Pull Request | `commit f33e727563` (repo `sns-line`) |
| Branch | `ai_fixbug_38369` (nhánh gốc `release_step_20260623`) |
| Ngày submit đánh giá | `2026-07-01` |
| Auto-filled | `2026-07-01 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ báo cáo Auto-fixbug. -->

Màn Tự động trả lời (自動応答) xác định thư mục đang mở bằng bộ chọn jQuery quá rộng `$(.active)` — lấy phần tử có class `active` **ĐẦU TIÊN** trên toàn trang. Gần đây header được thêm popup Điều khoản/Chính sách (`#popupTerm`), trong đó có tab mang class `active` nằm TRƯỚC danh sách thư mục trong DOM và **không có** thuộc tính `data-id`. Vì vậy `$(.active)` trả về tab của popup đó → `group_id` bị rỗng → server hiểu là thư mục mặc định và trả về `group_open=0`, khiến màn nhảy về thư mục Chưa phân loại (未分類) mỗi khi bật/tắt công tắc trả lời tự động.

## 2. Cách fix

<!-- Nguyên văn từ báo cáo Auto-fixbug. -->

Thay bộ chọn quá rộng `$(.active).attr(data-id)` bằng trạng thái thư mục đang mở của Vue (`group_open`) trong các hàm bật/tắt rule (`turnOnItem` / `turnOffItem` — nguyên nhân trực tiếp của ticket), tìm kiếm theo từ khoá, thêm/sửa thư mục và huỷ sắp xếp của màn Tự động trả lời. `group_open` là nguồn dữ liệu chuẩn cho thư mục hiện tại (không phụ thuộc DOM), nên không còn bị popup Điều khoản (hay phần tử `.active` khác) làm sai.

> ⚠️ Dev note: Cùng lỗi này còn ở **~26 màn danh sách khác** dùng chung pattern `$(.active)` — Dev đề xuất **tách 1 ticket triển khai ngang (yokoten)**, KHÔNG nằm trong scope fix này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `changeStatusReply` — `public/js/reply/index.js` | Kiểm tra | Handler công tắc ON/OFF của rule |
| 2 | `turnOnItem` / `turnOffItem` — `public/js/reply/index.js` | **Đã sửa** — gọi `initData` với `group_id` lấy từ `group_open` | Nguyên nhân trực tiếp của ticket |
| 3 | `searchByKeyWord` — `public/js/reply/index.js` | **Đã sửa** | Cùng dùng `$(.active)` |
| 4 | `addGroup` — `public/js/reply/index.js` | **Đã sửa** | Cùng dùng `$(.active)` (thêm/sửa thư mục) |
| 5 | `cancelSorted` — `public/js/reply/index.js` | **Đã sửa** | Cùng dùng `$(.active)` (huỷ sắp xếp) |
| 6 | `ReplyController::ajaxGetListCategory` — `app/Http/Controllers/Basic/ReplyController.php` | Không sửa (xác nhận) | `group_open` trả về = `request.group_id`, empty → 0 |
| 7 | `popupTerm` / `term-tab active` — `resources/views/layout/basic/header.blade.php` | Không sửa (xác nhận) | Nguồn phần tử `.active` gây nhiễu (luôn có trong DOM) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev report 4.1 chỉ ghi file thay đổi: public/js/reply/index.js. Các function bên dưới tổng hợp từ mục 3. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `turnOnItem` / `turnOffItem` | `public/js/reply/index.js` | Direct | Nguyên nhân trực tiếp — sửa dùng `group_open` thay `$(.active)` |
| F2 | `changeStatusReply` | `public/js/reply/index.js` | Direct | Handler công tắc ON/OFF của rule, gọi `turnOnItem`/`turnOffItem` |
| F3 | `searchByKeyWord` | `public/js/reply/index.js` | Direct | Cùng dùng `$(.active)`, đã sửa (tìm kiếm theo từ khoá) |
| F4 | `addGroup` | `public/js/reply/index.js` | Direct | Cùng dùng `$(.active)`, đã sửa (thêm/sửa thư mục) |
| F5 | `cancelSorted` | `public/js/reply/index.js` | Direct | Cùng dùng `$(.active)`, đã sửa (huỷ sắp xếp) |
| F6 | `ReplyController::ajaxGetListCategory` | `app/Http/Controllers/Basic/ReplyController.php` | Indirect | Không sửa — nhận `group_id`, empty → `group_open=0` |

### 4.2. List data bị update khi fix bug

<!-- Dev report 4.2: "Không có — chỉ sửa logic chọn thư mục phía client, không đụng DB". -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Chỉ sửa logic chọn thư mục phía client (JS), **không** đụng DB / cache / migration |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Auto Reply (自動応答 / FA-003) — bật/tắt rule trong thư mục | F1, F2 | Medium |
| T2 | Auto Reply — tìm kiếm theo từ khoá | F3 | Low |
| T3 | Auto Reply — thêm/sửa thư mục | F4 | Low |
| T4 | Auto Reply — huỷ sắp xếp (cancel sort) | F5 | Low |

> ⚠️ Dev tự review: rủi ro thấp (chỉ đổi cách xác định thư mục, dùng `group_open` đồng nhất với `deleteItem`/`moveItems` vốn đã dùng sẵn). Không đổi backend, không đổi DB. Lưu ý test: chỉ màn Tự động trả lời được sửa — **~26 màn danh sách khác cùng bug vẫn còn** (yokoten, ticket riêng).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
