# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI) — Assignee Redmine: Thanh Phương |
| Commit / Pull Request | `sns-line@2e4c0f786b4ff9c7695c3f39b608c80eff352933` (commit cuối trên nhánh, theo journal #143139) |
| Branch | `ai_studio_implement_42765` (nhánh gốc `release_step_20260930_v2` @`0637cd04f7c1`) |
| Ngày submit đánh giá | 2026-10-12 (journal #143139 — Dev handoff v2) |
| Auto-filled | 2026-10-24 by /new-task |

> ⚠️ **Input tổng hợp từ 3 journal** (không có 1 section "Đánh giá ảnh hưởng" theo đúng format chuẩn 4 mục) — ticket qua 2 vòng thiết kế (v1 → v2) trong 3 journal. Nội dung dưới đây được AI gộp lại từ "Nội dung thực hiện" (#143086, #143128) + "Dev handoff" (#143139). Tester **PHẢI** đọc lại `01-bug-task.md` phần Journal nguyên văn trước khi tick checkbox dưới đây.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại cả 3 journal ở Redmine #42765 và xác nhận bảng tổng hợp dưới đây không sót vòng fix nào (v1 → v2).

---

## 1. Nguyên nhân

**IDOR (Insecure Direct Object Reference) ở tính năng Auto reply (自動応答)**, phát hiện qua security audit (cùng nguồn audit với [#42764](../2026-10-24_42764_auto-reply-route-public-detail/03-dev-impact.md)):

- **IDOR-MSG-19 (3/4) [High]** — Thư mục (folder, kind=reply) theo id không ràng `bot_id`/`kind`: `ReplyController.php:471-476, 542`, route `/ajax/get-list-group` (middleware LOGIN). `category->where('id')->update(...)` không kiểm sở hữu; `moveItem` không kiểm `folder_move_id` trước khi ghi.
- **IDOR-MSG-20 (7/9) [Normal]** — Id liên kết của bot khác lưu được vào cấu hình auto reply: `ReplyController.php:127-170, 304-348` (middleware LOGIN/BASIC) — id scenario/tag/action/template/profile/folder không kiểm theo bot trước khi lưu.
- **IDOR-MSG-22 (4/10) [Low]** — Sort position chéo bot: `ReplyController.php:647, 699` — `whereIn('id')->update(['position'])` không thêm điều kiện `bot_id`.
- **Bug con phát sinh trong lúc fix (v1 → v2)**: bản sửa v1 cho IDOR-MSG-20 chặn **nhầm** cả giá trị hợp lệ của chính form cũ — lựa chọn mặc định `変更しない` (`scenario_id = -1`) và sentinel `-1000` có sẵn trong dữ liệu cũ — vì check theo bot áp luôn cho số âm (không trỏ tới kịch bản của bot nào).

## 2. Cách fix

**2 vòng (v1 → v2), 10 hướng sửa (D-1 → D-10):**

| Vòng | Mục tiêu | Hướng sửa |
|---|---|---|
| v1 (#143086) | IDOR-MSG-19/20/22 | D-1 Thêm trait `AutoReplyFolderGuardTrait` dùng chung web + API mobile · D-2 Thư mục web (`addAndEditGroup`/`renameGroup`/`deleteGroup`) ràng theo `bot_id` + `kind` · D-3 `moveItem` kiểm `folder_move_id` trước khi ghi · D-4 `sortItem`/`sortFolder` chỉ cập nhật `position` bản ghi của bot · D-5 Form cũ `store`/`save` kiểm id liên kết theo bot trước khi ghi · D-6 Lưu V2 (web + MCP) chặn id filter v2 của bot khác · D-7 API mobile: thư mục, chuyển thư mục, danh sách theo `group_id` · D-8 Kiểm tra `php -l` + test PHPUnit không chạm DB thật |
| v2 (#143128) | Bug con: chặn nhầm `変更しない` (-1) / sentinel -1000 | D-9 Form cũ: cho số nguyên **âm** của `step_to_id` đi qua trước khi kiểm theo bot (số âm không trỏ kịch bản của bot nào) · D-10 Thêm test sentinel vào `ReplyFolderGuardTest`, chạy lại toàn bộ test |

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `/ajax/get-list-group` (dùng chung `addAndEditGroup`/`renameGroup`/`deleteGroup`/`moveItem`/`sortItem`/`sortFolder`/`searchByKeyWord`/`showGroup`) — `ReplyController.php` | Bộ lọc `group_id` ở đầu hàm + guard mới chạy trước khi ghi | 8 action của màn thư mục auto reply dùng chung 1 endpoint — guard phải chặn trước khi bất kỳ nhánh nào ghi dữ liệu |
| 2 | `/ajax/save-data-detail-auto-reply` (tạo/sửa/sao chép auto reply V2) | Guard filter v2 chạy trước khi ghi | Filter mới (id rỗng) và filter của chính bot phải lưu bình thường — không được chặn nhầm (bài học v1→v2 ở mục 1) |
| 3 | `Api\Mobile\AutoreplyMobileController` (save, move, update/delete/create folder, delete, toggle) | Áp `AutoReplyFolderGuardTrait`; hàm dựng danh sách ép `group_id` không hợp lệ về `未分類` | Dùng chung hàm dựng danh sách với các action khác — API MCP (`create_autoreply`/`update_autoreply`) + app mobile đi qua controller này |
| 4 | `category` (kind=reply) / `auto_reply` (`position`, `category_id`) / `filters_v2` (`parent_type=auto_reply`) / filters v1 | Thêm điều kiện `bot_id`/`kind` vào câu ghi | Không đổi cấu trúc bảng — chỉ thêm scope theo bot vào query ghi |
| 5 | `/basic/reply/store`, `/basic/reply/save` (form cũ) | Thêm bước kiểm id liên kết theo bot trước khi ghi; v2 nới cho số âm của `step_to_id` | Form cũ lưu nhiều loại id liên kết (scenario/tag/action/template/profile/folder) — v1 chặn quá tay giá trị mặc định hợp lệ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `addAndEditGroup` / `renameGroup` / `deleteGroup` (`/ajax/get-list-group`) | `Basic\ReplyController.php` | Direct | Ràng theo `bot_id` + `kind` (IDOR-MSG-19) |
| F2 | `moveItem` | `Basic\ReplyController.php` | Direct | Kiểm `folder_move_id` thuộc bot trước khi ghi; đích đã xoá/không tồn tại → 404 |
| F3 | `sortItem` / `sortFolder` | `Basic\ReplyController.php` | Direct | Chỉ cập nhật `position` của bản ghi thuộc bot (IDOR-MSG-22); id lạ bị bỏ qua |
| F4 | `store` / `save` (form cũ, `/basic/reply/store`, `/basic/reply/save`) | `Basic\ReplyController.php` | Direct | Kiểm id liên kết (scenario/tag/action/template/profile/folder) theo bot; **ngoại lệ**: số âm của `step_to_id` (`-1` 変更しない, `-1000` sentinel cũ) đi qua trước khi kiểm (IDOR-MSG-20 + fix v2) |
| F5 | `saveDataDetailAutoReply` (lưu V2, web + API MCP) | `Basic\ReplyController.php` | Direct | Chặn id filter v2 của auto reply bot khác |
| F6 | `AutoreplyMobileController` — folder create/update/delete, move, danh sách theo `group_id` | `Api\Mobile\AutoreplyMobileController.php` | Direct | API MCP (`create_autoreply`/`update_autoreply`) + app mobile dùng chung controller; `group_id` không hợp lệ → ép về `未分類` |
| F7 | `AutoReplyFolderGuardTrait` (mới tạo) | `app/Traits/AutoReplyFolderGuardTrait.php` | Direct | Helper kiểm quyền thư mục dùng chung web + API mobile |
| F8 | `searchByKeyWord` / `showGroup` (cùng endpoint `/ajax/get-list-group`) | `Basic\ReplyController.php` | Indirect | Dùng chung bộ lọc `group_id` ở đầu hàm với 6 action còn lại — cần hồi quy không bị chặn nhầm |

> ⚠️ **Điểm cần verify riêng**: journal #146834 của #42764 ghi rõ phần IDOR thư mục API mobile (`updateAutoreplyFolder`, `buildListCategoryResponse`, `folder_move_id` của `moveAutoreply`) thuộc về ticket này và **gợi ý dùng lại trait `AutoReplyOwnershipGuardTrait`** của #42764. Nhưng F6/F7 ở trên cho thấy #42765 tạo **trait riêng** `AutoReplyFolderGuardTrait` — chưa có xác nhận 2 trait không xung đột khi merge. Nên hỏi lại Dev trước khi chốt coverage phần API mobile.

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `category` (kind=reply) | UPDATE (logic) | Thêm điều kiện `bot_id` + `kind` khi sửa/đổi tên/xoá/chuyển thư mục — không migration |
| D2 | `auto_reply.position` | UPDATE (logic) | Sort chỉ cập nhật bản ghi thuộc bot đang đăng nhập |
| D3 | `auto_reply` (id liên kết: `category_id`, `step_to_id`/scenario, template, tag, filter v1 của form cũ) | UPDATE (logic) | Kiểm sở hữu theo bot trước khi ghi; ngoại lệ số âm của `step_to_id` |
| D4 | `filters_v2` (`parent_type=auto_reply`) | UPDATE (logic) | Chặn ghi đè filter v2 thuộc auto reply của bot khác |

**Không có migration / thay đổi schema DB** ở cả 2 vòng (Dev xác nhận đã kiểm diff, journal #143139).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | 自動応答 (Auto reply) — web: thư mục (CRUD/chuyển/sắp xếp), form cũ, lưu V2 | F1-F5, D1-D4 | **High** — guard mới chạy trên mọi thao tác ghi của 1 endpoint dùng chung (`/ajax/get-list-group`), guard sai sẽ chặn nhầm user hợp lệ |
| T2 | API MCP auto reply (`create_autoreply`/`update_autoreply` — phần folder) | F6, D1 | **High** — AI agent phải nhận đúng mã lỗi 4xx/behavior `未分類` khi dùng `group_id` không hợp lệ hoặc của bot khác |
| T3 | App mobile LME (auto reply — thư mục, chuyển, danh sách) | F6, D1 | **High** — cùng controller với MCP, cùng guard mới |
| T4 | Form tạo/sửa auto reply kiểu cũ (giá trị mặc định `変更しない` / `購読停止`) | F4, D3 | **Medium → High** — bug con v1→v2 cho thấy đây là vùng dễ bị fix-lệch (over-blocking), cần TC riêng cho nhánh số âm |

**Dev tự đánh giá tổng thể: "Rủi ro trung bình"** — guard mới chạy trên mọi thao tác ghi của màn 自動応答 (web) và API MCP/mobile. Đã có **82 test** kèm kiểm chứng ngược trên code cũ, nhưng **CHƯA verify runtime trên app thật** (nguyên văn Dev, journal #143139) và **còn phải merge cùng #42764** (cùng 2 controller, conflict chưa giải tại thời điểm handoff).

**Phải phát hành cùng [#42764](../2026-10-24_42764_auto-reply-route-public-detail/03-dev-impact.md)** — sau merge, Dev yêu cầu chạy lại 3 bộ test: `ReplyFolderGuardTest` (ticket này), `ReplyOwnershipGuardTest` + `AutoreplyMobileOwnershipGuardTest` (của #42764).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] Đã hỏi Dev rõ việc 2 trait `AutoReplyFolderGuardTrait` (#42765) và `AutoReplyOwnershipGuardTrait` (#42764) có xung đột/trùng lặp logic khi merge không
