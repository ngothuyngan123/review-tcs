# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (Redmine assignee: Ngô Thúy Ngần) |
| Commit / Pull Request | `1581ac16c6f42833ee0b0f7647d8d8e63d3176a9` |
| Branch | `ai_studio_implement_42771` (gốc `release_step_20260930_v2@0637cd04f7c1`) |
| Ngày submit đánh giá | `2026-10-12` |
| Auto-filled | `2026-10-24 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

IDOR-MSG-22 (security audit, severity gốc Low 2/10) tại `V2\CategoryService.php:89-91`: hàm sắp xếp vị trí dùng chung (`updatePosition`) chạy `whereIn('id')->update(['position'])` **không lọc theo `bot_id`/phạm vi user** và **không validate `id` là số** (id bị nối thẳng vào SQL). Vì `updatePosition` được 5 chức năng sắp xếp dùng chung (thư mục rich menu, rich menu, danh sách hợp đồng, LP super admin, thư mục LP super admin), lỗ hổng cho phép:
- Ghi đè `position` của bản ghi (thư mục/rich menu) thuộc **bot khác**.
- Ghi đè `position` của **hợp đồng user khác** qua API `save-contract-position`.
- Gửi `id` không phải số (kể cả payload dạng ký tự SQL, vd `'1 THEN 0 END--'`) vào hàm dùng chung.

## 2. Cách fix

3 hướng sửa (ghi trong journal Dev Studio #143085):
- **D-1**: `updatePosition` chỉ nhận `id` dạng số (regex `^\d+$`, ném `InvalidArgumentException` nếu sai) + nhận thêm tham số `botId` → thêm điều kiện `WHERE bot_id` khi được truyền bot.
- **D-2**: Sắp xếp thư mục rich menu + rich menu v2 truyền `bot` hiện tại (`(int)getBotId()`) vào `updatePosition` → id của bot khác bị bỏ qua, response vẫn `status:true` như cũ.
- **D-3**: Sắp xếp hợp đồng (`saveContractPosition`) **không** lọc theo bot hiện tại (vì 1 danh sách gồm nhiều bot, gần nửa hợp đồng không có `bot_id`) — thay vào đó lọc theo đúng **scope hợp đồng user đang thấy** (giống điều kiện của `getDataContract`: chủ hợp đồng hoặc staff có quyền `pointSettings`). Id ngoài phạm vi bị bỏ qua + ghi log (`'saveContractPosition skip contract ids out of scope'`); nếu sau lọc rỗng thì trả `status:true` nhưng **không ghi** gì.
- Super admin (LP + thư mục LP): **chỉ thêm validate `id` phải là số** — hành vi không đổi (vì FE luôn gửi id số).
- Không đổi schema / route / FE / response khi thành công; không có migration.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CategoryService::updatePosition` (`app/Services/V2/CategoryService.php`) | Thêm validate `id` số + param `botId` lọc `WHERE bot_id` | Hàm dùng chung gốc của lỗ hổng IDOR |
| 2 | `RichMenuService` (`app/Services/V2/RichMenuService.php`) | Truyền bot hiện tại khi gọi `updatePosition` cho sort rich menu | Caller của `updatePosition` — cần giới hạn theo bot |
| 3 | `ListPageController` (`app/Http/Controllers/V2/Bill/ListPageController.php`) | `saveContractPosition`: lọc id theo scope hợp đồng user đang thấy (giống `getDataContract`), validate `order.*` là số, log id bị bỏ qua | Caller của `updatePosition` cho sort hợp đồng — không lọc theo bot (đa bot + `bot_id` NULL) nên cần logic lọc riêng |
| 4 | Super admin: `PathIntroController::sort`, `CategorySuperAdminController::sort` (không đổi tên file trong diff — chỉ gọi `updatePosition` đã validate) | Không đổi hành vi, chỉ thêm validate id số (gián tiếp qua `updatePosition`) | Caller khác của hàm dùng chung — FE luôn gửi id số nên không có regression kỳ vọng |

⚠️ Dev ghi rõ: `PathIntroController::sort` (super admin) truyền `'desc'` chữ thường nên `updatePosition` không đảo thứ tự (so sánh `== 'DESC'`) — **lỗi này NẰM NGOÀI phạm vi ticket #42771**, không fix trong task này, không đưa vào coverage GAP của task này (chỉ raise ticket riêng nếu cần).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `CategoryService::updatePosition` | `app/Services/V2/CategoryService.php` | Direct | Hàm dùng chung của cả 5 chức năng sort — sửa trực tiếp |
| F2 | Sort thư mục rich menu — `POST /ajax/folder/rich-menu/sort` | `RichMenuService` | Direct | Truyền bot hiện tại; id bot khác bị bỏ qua |
| F3 | Sort rich menu — `POST /ajax/rich-menu/list/sort` | `RichMenuService` | Direct | Truyền bot hiện tại; id bot khác bị bỏ qua |
| F4 | `saveContractPosition` — `POST /ajax/point-settings/save-contract-position` | `ListPageController` (V2\Bill) | Direct | Lọc theo scope hợp đồng user thấy, validate `order.*`, log id bị bỏ |
| F5 | Sort LP / thư mục LP (super admin) — `/admin/path-intro/sort`, `/admin/category-super-admin/sort` | (gọi `updatePosition`) | Indirect | Chỉ hưởng validate id số gián tiếp từ F1, không đổi hành vi khác |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `category.position` (thư mục rich menu) | UPDATE | Chỉ update bản ghi của bot đang chọn |
| D2 | `rich_menus.position` | UPDATE | Chỉ update bản ghi của bot đang chọn |
| D3 | `bot_contracts.position` | UPDATE | Chỉ update hợp đồng trong scope user đang thấy (không lọc theo bot) |
| D4 | `path_intro_data.position` | UPDATE | Không đổi logic, chỉ validate id |
| D5 | `category_super_admin.position` | UPDATE | Không đổi logic, chỉ validate id |
| — | `updated_at` của 5 bảng trên | KHÔNG đổi | Dev xác nhận: sort không cập nhật `updated_at` — không phải bug mới |

Không có migration / thay đổi schema (Dev đã kiểm diff xác nhận).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | リッチメニュー一覧 v2 — modal 並べ替え (sắp xếp thư mục rich menu) | F1, F2, D1 | High |
| T2 | リッチメニュー一覧 v2 — modal 並べ替え (sắp xếp rich menu trong thư mục) | F1, F3, D2 | High |
| T3 | 契約情報・領収書 (danh sách hợp đồng point-settings) — modal 並べ替え 保存 | F1, F4, D3 | High (rủi ro chính: lọc nhầm hợp đồng hợp lệ — đa bot, `bot_id` NULL/bot đã xoá, staff `pointSettings`) |
| T4 | 登録経路管理 (LP) super admin — modal 並べ替え (LP + thư mục LP) | F1, F5, D4, D5 | Medium (chỉ thêm validate, FE luôn gửi id số) |
| T5 | Chặn sort khi bot đang backup (rich menu) | F2, F3 (giữ nguyên guard cũ) | Medium — regression guard cũ, không phải fix mới nhưng nằm trong luồng bị sửa |

**Nguồn Studio (task_get_context, `dev_impact` + `requirements`)** — đối chiếu bổ sung, khớp với journal:
- Rich menu: id không phải số → exception bị `RichMenuService` nuốt → `status:true` nhưng **cả batch không lưu** (chỉ khi gọi tay / sửa payload — khác hành vi "chặn từng id lẻ" dễ hiểu nhầm).
- 11 requirement (REQ-001 → REQ-011) Studio sinh, risk High chiếm 8/11 (REQ-001/002/003/004/006/007/008/010).
- **REQ-011 (risk Medium, "cần PO chốt")**: khi lượt lưu không ghi được gì (đổi bot ở tab khác, id bị chặn hết), response/màn vẫn báo thành công giả — đây là observation Studio nêu, **chưa có quyết định Leader/PO** — không phải bug đã confirm, chỉ nêu ở `[NIT]`/gợi ý khi review, không đẩy GAP bắt buộc.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
