# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI) — Assignee Redmine: Đoàn Thị Bích Hảo |
| Commit / Pull Request | sns-line@ced6de1f9cd5b0dd751fd01e6eb9e9dfab5387cb (commit cuối, v7). Các commit trung gian: 0917f7cfcebd, 5640e9f98b0b, 2abe1c5ab5f6, e71958133700 |
| Branch | `ai_studio_implement_42764` (nhánh gốc `release_step_20260930_v2` @46765b418f67) |
| Ngày submit đánh giá | 2026-10-22 (journal #146834, handoff cuối v1–v7) |
| Auto-filled | 2026-10-24 by /new-task |

> ⚠️ **Input tổng hợp từ NHIỀU journal** (không có 1 section "Đánh giá ảnh hưởng" duy nhất theo format chuẩn) — ticket trải qua 7 vòng fix (v1→v7) trong 11 journal. Nội dung dưới đây được AI gộp lại từ các journal "Nội dung thực hiện" + "Dev handoff" (đặc biệt #142942, #144089, #146667, #146834). Tester **PHẢI** đọc lại 01-bug-task.md phần Journal nguyên văn trước khi tick checkbox dưới đây.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại toàn bộ 11 journal ở Redmine #42764 và xác nhận bảng tổng hợp dưới đây không sót vòng fix nào (v1→v7) hoặc bug con nào.

---

## 1. Nguyên nhân

**IDOR (Insecure Direct Object Reference) ở tính năng Auto reply (自動応答)**, phát hiện qua security audit:

- **IDOR-MSG-10 [Immediate]**: Route **PUBLIC** (không cần đăng nhập) đọc/ghi chi tiết auto reply — `Basic\ReplyController::initDataDetailAutoReply` (L910-946) và `saveDataDetailAutoReply` (L1061-1125), qua route `/ajax/init-data-detail-auto-reply` + `/ajax/save-data-detail-auto-reply`. Code dùng `AutoReply::where('id')` / `Keyword::where('id')->update` trực tiếp theo id client gửi lên (`id`, `copyId`, `list_keyword[].id`, `action_id`, `category_id`) mà **không kiểm id đó có thuộc bot đang đăng nhập**.
- **IDOR-MSG-11 [High]**: Lưu/xoá/move auto reply theo id — `save` (L298-413), `deleteItem(s)`/`moveItem` (L606-677), route có middleware LOGIN nhưng **không scope theo bot_id** — dùng `AutoReply::findOrFail`, xoá Keyword theo `auto_reply_id` mà không xác nhận sở hữu.
- Cùng lỗ hở còn ở **API MCP/mobile** (`AutoreplyMobileController`) — phát hiện khi Dev review lại ở v2: init/save/delete/toggle/move auto reply theo id không kiểm bot (ảnh hưởng cả công cụ AI MCP `create_autoreply`/`update_autoreply`).
- **Các bug con phát sinh trong lúc fix** (v3→v7, do QA + automation Test Studio phát hiện): id sai định dạng trả 403 thay vì 400 đúng chuẩn lỗi dữ liệu; action không tồn tại vẫn cho lưu; payload thiếu `category_id` gây lỗi PHP "Undefined property"; API mobile save thành công không trả `success:true`; màn tạo mới lấy `group_id` từ URL không kiểm thư mục có thuộc bot; bật/tắt (toggle) auto reply của bot khác trả "thành công" giả dù DB không đổi; loading UI bị kẹt vì alert lỗi hiện chặn hiệu ứng tắt loading.
- **2 bug automation (#2793, #2794) KẾT LUẬN KHÔNG PHẢI LỖI CODE** — do bộ test tự động đo lệch (không bắt kịp request / đếm nhầm request mở thư mục), nghiệp vụ server vốn đã đúng. Dev chỉ thêm test hồi quy, không đổi code sản phẩm (v5).

## 2. Cách fix

**7 vòng (v1 → v7), 24 hướng sửa (D-1 → D-24):**

| Vòng | Bug/mục tiêu | Hướng sửa |
|---|---|---|
| v1 | IDOR-MSG-10/11 (web) | D-1 chuyển route init/save detail vào nhóm cần login · D-2 init chỉ đọc/sao chép auto reply của bot hiện tại · D-3 save kiểm id/action_id/category_id/keyword id trước khi ghi · D-4 save (form cũ) tìm theo id+bot · D-5 deleteItem/deleteItems/moveItem chặn id bot khác · D-6 searchByKeyWord lọc theo bot khi từ khoá rỗng · D-7 test guard |
| v2 | IDOR ở API MCP/mobile | D-8 tách helper kiểm quyền thành `AutoReplyOwnershipGuardTrait` dùng chung web+API · D-9 áp cùng rule cho API MCP/mobile (init/save/delete/toggle/move) · D-10 test 2 nhánh sao chép + IDOR API mobile · D-11 sửa log (`logDebug` có placeholder) |
| v3 | 5 bug QA khi lưu chi tiết | D-12 id sai định dạng → 400 (không phải 403) · D-13 action không tồn tại → 404, không lưu · D-14 thiếu category_id → giữ thư mục đang lưu (sửa) / về 0 (tạo mới) · D-15 API mobile save thành công trả thêm `success:true` · D-16 test bổ sung |
| v4 | Bug #2755 (thư mục mặc định) | D-17 màn tạo mới chỉ nhận `group_id` là thư mục còn sống của bot đang chọn, không hợp lệ → về 未分類 · D-18 áp cùng rule cho init tạo mới · D-19 test |
| v5 | Bug automation #2793, #2794 | D-20 — KHÔNG đổi code sản phẩm, chỉ thêm test hồi quy (bộ test automation đo lệch) |
| v6 | Bug #43617 (phần bật/tắt) | D-21 bật/tắt auto reply bot khác trên web trả lỗi 403 thay vì "thành công" giả · D-22 test bổ sung |
| v7 | Bug automation #3714 (loading UI) | D-23 màn tạo/sửa tắt hẳn loading trước khi hiện alert lỗi lưu (JS-only, `create.js`, không tăng version asset) · D-24 test + kiểm cú pháp JS |

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AutoReply::searchByKeyWord` | Thêm lọc `bot_id` khi từ khoá rỗng | Search auto reply trên màn 自動応答 vốn trả về auto reply của mọi bot khi ô tìm kiếm rỗng |
| 2 | `AutoreplyMobileController` (init/save/delete/toggle/move) | Áp `AutoReplyOwnershipGuardTrait` | API MCP (`create_autoreply`/`update_autoreply` gọi `save-autoreply`) + app mobile dùng chung controller này |
| 3 | `create_download_file.js` (màn quản lý CSV) | Không đổi code, chỉ route init giờ cần login | Route `init-data-detail-auto-reply` được màn CSV gọi lại — màn CSV vốn đã yêu cầu login nên không đổi hành vi |
| 4 | `Basic\ReplyController::ajaxGetListCategory` | Dùng chung với thay đổi thư mục/sắp xếp của #42765 | Đã thử gộp 2 nhánh, Dev xác nhận không conflict |
| 5 | `create.js` (màn tạo/sửa auto reply) | D-23: tắt hẳn loading trước khi hiện alert lỗi lưu | Loading bị kẹt khi alert chặn hiệu ứng mờ dần (bug automation #3714) |

## Leader đọc thêm trước khi giao TCs

> ⚠️ **2 ticket PHẢI phát hành cùng #42764** mới đóng hết các thao tác IDOR nêu trong bug con #43617: **#42765** (thư mục auto reply — API mobile `updateAutoreplyFolder`/`folder_move_id`/`buildListCategoryResponse` theo `group_id` **CHƯA fix**, vẫn còn lỗ IDOR thư mục, ngoài phạm vi #42764) và **#42759** (modal action). TC của #42764 **KHÔNG** cần cover phần thư mục API mobile và modal action — thuộc 2 ticket đó.
> Bản fix (tới v7) **chưa có trên nhánh release/staging nào** tại 2026-10-22 — QA/Test Studio phải retest trên build từ branch `ai_studio_implement_42764`. Vòng 7 (JS `create.js`) không tăng `sns-line.version` → **phải hard reload (Ctrl+F5)** trước khi test.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `initDataDetailAutoReply` / `saveDataDetailAutoReply` | `Basic\ReplyController.php` | Direct | Route PUBLIC → LOGIN + scope bot_id (IDOR-MSG-10) |
| F2 | `save` (form cũ) | `Basic\ReplyController.php` | Direct | Tìm theo id + bot trước khi ghi |
| F3 | `deleteItem` / `deleteItems` / `moveItem` | `Basic\ReplyController.php` | Direct | Chặn id của bot khác (IDOR-MSG-11) |
| F4 | `searchByKeyWord` | `app/AutoReply.php` | Direct | Nhánh từ khoá rỗng thêm lọc bot_id |
| F5 | Toggle bật/tắt (danh sách 自動応答) | `Basic\ReplyController.php` | Direct | v6: id bot khác → 403 thay vì "thành công" giả |
| F6 | init/save/delete/toggle/move auto reply | `Api\Mobile\AutoreplyMobileController.php` | Direct | API MCP/mobile — áp cùng quy tắc chặn như web |
| F7 | `AutoReplyOwnershipGuardTrait` (mới tạo) | `app/Traits/AutoReplyOwnershipGuardTrait.php` | Direct | Helper kiểm quyền dùng chung web + API mobile |
| F8 | Xử lý loading/alert khi lưu lỗi | `public/js/reply/create.js` | Direct | v7, JS-only, không đổi server |
| F9 | Gọi route init chi tiết auto reply | `create_download_file.js` (màn quản lý CSV) | Indirect | Route đổi sang LOGIN, màn CSV vốn đã login → hành vi không đổi |
| F10 | Cảnh báo Chatwork nội bộ khi sao chép auto reply lệch bot | (mới thêm, trong luồng sao chép) | Indirect | Chỉ phát sinh khi dữ liệu cũ lệch bot (snapshot DB không thấy ca thật) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `AutoReply` / `t_actions_detail.bot_id` | UPDATE (logic) | Thêm điều kiện `where bot_id` khi đọc/ghi auto reply — không migration schema |
| D2 | `Keyword` (theo `auto_reply_id`) | UPDATE (logic) | Thêm kiểm sở hữu trước update/delete keyword |
| D3 | `t_actions` (action liên kết auto reply) | UPDATE (logic) | Kiểm tồn tại + thuộc bot trước khi lưu; action không tồn tại → 404, không lưu |
| D4 | Folder (`category_id`, kind=reply) | UPDATE (logic) | Kiểm thư mục còn sống + thuộc bot; không hợp lệ → 未分類 (tạo mới) / giữ thư mục cũ (sửa) |
| D5 | Response API mobile (key `success`) | UPDATE (contract) | Thêm `success:true` khi lưu thành công, giữ `status`/`data.id`/`msg` cũ |

**Không có migration / thay đổi schema DB** ở bất kỳ vòng nào (Dev xác nhận đã kiểm diff ở mọi journal handoff).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | 自動応答 (Auto reply) — web: tạo/sửa/sao chép/lưu/xoá/chuyển thư mục/bật-tắt | F1-F5, D1-D4 | **High** — security fix chạm toàn bộ CRUD của tính năng chính, logic kiểm quyền chuyển sang trait dùng chung |
| T2 | API MCP (`create_autoreply`/`update_autoreply`...) | F6, D1-D4 | **High** — AI agent phải nhận đúng lỗi 4xx khi dùng id bot khác, ảnh hưởng trực tiếp hành vi AI |
| T3 | App mobile LME (auto reply qua API mobile) | F6, D5 | **High** — cùng controller với MCP, thêm key `success` trong response |
| T4 | Màn quản lý CSV (`create_download_file.js`) | F9 | **Low** — chỉ cần đã login, hành vi không đổi |
| T5 | Cảnh báo Chatwork nội bộ (sao chép auto reply lệch bot) | F10 | **Low** — cảnh báo nội bộ, không phải tính năng end-user |

**Dev tự đánh giá tổng thể: "Rủi ro trung bình"** — thay đổi chạm cả web lẫn API MCP, dựa vào `t_actions`/`t_actions_detail.bot_id` + folder kind reply. Đã có **112 test PHP** + kiểm chứng ngược + harness trình duyệt cho JS, nhưng **CHƯA verify runtime trên app thật** (theo đúng nguyên văn Dev ở mọi vòng handoff).

**Bug con đã confirm fixed** (cần TC regression verify lại, không phải GAP mới): #43033, #43034, #43035, #43036, #43037, #43617 (phần get/save/delete/move/toggle), #3714 (automation, loading UI).
**Bug con KHÔNG đổi code** (không cần TC fix mới, chỉ cần TC hồi quy đúng cách đo): #43080 (automation, chỉ đếm request sau khi bấm 削除), #43081 (automation, kiểm theo URL cuối + dữ liệu, ca `copy_id=abc`).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
