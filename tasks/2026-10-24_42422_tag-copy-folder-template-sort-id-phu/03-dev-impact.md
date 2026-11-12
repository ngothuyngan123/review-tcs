# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Ticket này KHÔNG có section "Đánh giá ảnh hưởng" 4-mục chuẩn trong Description Redmine — đây là ticket **security audit (IDOR)**, nội dung đánh giá ảnh hưởng nằm rải trong **16 journal / 8 vòng handoff** (v1 → v8) của "Dev Studio" (AI agent), được HieuTM (Truong Minh Hieu) chốt quyết định cuối. File này **tổng hợp lại** từ journal mới nhất (v8, #147623 — authoritative, không đổi code so với v5-v7) + lịch sử các vòng trước + `task_get_context(dev_impact, requirements, spec_delta)` của MCP LME TEST STUDIO (task #391). Xem nguyên văn đầy đủ từng vòng ở `01-bug-task.md`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI agent) — quyết định cuối: Truong Minh Hieu (HieuTM) |
| Commit / Pull Request | `sns-line@188ad8624d314b08be69b2499bd2df0384c18d8a` (hiện hành, từ v5 — không đổi tới v8). Lịch sử: v1 `177b5e379a45` → v2 `450bd344c7f7` → v3 `b4b9b638cc98` → v4 `b4a39f94fa1a` → v5-v8 `188ad8624d31` |
| Branch | `ai_studio_implement_42422` (nhánh gốc `release_step_20260930_v2@657ba962f25d`) |
| Ngày submit đánh giá | 2026-10-23 (journal #147623, vòng 8) |
| Auto-filled | 2026-10-24 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — Leader đọc lại toàn bộ journal ở `01-bug-task.md` (16 journal, 8 vòng) trước khi tick, vì nội dung mục 1→4 dưới đây là **AI tổng hợp lại** từ nhiều vòng, không phải 1 section đơn nhất của Dev.

---

## 1. Nguyên nhân

`TagController.php` (web) và `TagMobileController.php` (app, bản song sinh) khi load/ghi dữ liệu tag, folder (category), action, template theo **id truyền vào từ request** (`id`, `category_id`, `action_id`, `limit_action_id`, `group_id`, `folder_move_id`, `sort_ids`, `tag_id`...) **không kiểm `bot_id` của bản ghi** trước khi dùng — cho phép bot A (đăng nhập hợp lệ) đọc/ghi dữ liệu tag/folder/action/template thuộc bot B (IDOR — Insecure Direct Object Reference). Phát hiện từ security audit nội bộ, 6 nhóm:

- **IDOR-FR-14** — `initDataInfo` (copy/init tag): `Tags::where('id')`, `Actions::find/clone` không lọc bot.
- **IDOR-FR-15** — folder/category rename + move: `DB::table('category')->where('id')->update(...)`, implicit binding `Category` không kiểm bot_id + kind.
- **IDOR-FR-21** — `ajaxGetListCategoryTemplate`: `Category::find($gid)` không lọc bot.
- **IDOR-FR-25** — lưu tag (`save-tag`, tạo nhiều, CSV): id phụ (action/folder/template/scenario/switch) không kiểm bot trước khi lưu.
- **IDOR-FR-26** — sort tag/folder: `where('id')->update(['position'])` không có điều kiện bot_id.
- **IDOR-FR-27** — đọc/ghi phụ (friend-list theo tag, validate-limit) chưa lọc bot + code chết (view/route sửa tag cũ).

**4 bug con phát sinh trong lúc QA fix** (nguyên nhân riêng, không thuộc 6 nhóm audit gốc):
- `#43826` — app sửa tag (`edit_tag`) không gửi `is_limit` → code chỉ set `is_limit=0`, còn `limit`/`limit_action_mode` giữ giá trị cũ (lỗi thiếu field reset đồng bộ).
- `#44028` / automation `#3769` — nhánh `edit_tag` của `save-tag` (app + web) **không kiểm `tag_id`** trước khi dùng: `tag_id` dạng mảng `[TA1,TA2]` → code lấy phần tử đầu, ghi đè nhầm `TA1`, báo thành công sai.
- `#3951` — `validate-limit` dùng route model binding trực tiếp theo `id`, tag đã bị xoá ở tab khác → lỗi 404 tiếng Anh (không xử lý nghiệp vụ) thay vì chặn 403 nghiệp vụ.

## 2. Cách fix

Theo thứ tự các hướng sửa (D-1 → D-14), trạng thái hiện hành (sau v8):

- **D-1** `initDataInfo`: tìm tag theo `bot_id`; nếu tag thuộc bot mình nhưng action chi tiết lệch bot thì không preview/không clone action đó (chỉ log + Chatwork).
- **D-2** Đổi tên folder (`PUT category/update`, `addAndEditGroup`): chặn nếu folder không thuộc bot mình.
- **D-3** Di chuyển tag (`move-category`, `moveItem`): kiểm folder đích thuộc bot.
- **D-4** `ajaxGetListCategoryTemplate` (`/ajax/get-list-group-template`): chỉ đọc folder template của bot mình, id lạ → coi như `未分類` (0).
- **D-5** Lưu tag kiểm id phụ (folder, action, action giới hạn) trước khi ghi.
- **D-6** Sort (`sort-tag`, `sort-category`, `sortItem`, `sortFolder`): thêm điều kiện `bot_id` vào câu `update(position)` — id bot khác bị bỏ qua im lặng, không lỗi.
- **D-7** Đọc phụ: `friend-list` theo tag + `validate-limit` lọc theo bot.
- **D-8** Dọn code chết: xoá view `basic/tag/edit.blade.php` + route `POST /basic/tag/update` (chuyển hẳn sang màn sửa v2 `/basic/tag/edit-tag/{id}`).
- **D-9** Áp cùng guard cho bản song sinh trên app (`TagMobileController`: `get-tag-detail`, `update-tag-folder`, `save-tag`, `create-multiple-tag`).
- **D-10** (v2, fix bug #42723) Folder đích của save/move/create-multiple/CSV phải là **folder tag còn sống của chính bot** — folder template, folder đã xoá, id không tồn tại → 404 `「フォルダが見つかりません。」`; folder bot khác → vẫn 403.
- **D-11** (v2, fix bug #42722) `save-tag`: thiếu `is_limit`/`limit`/`limit_action_mode` khi **tạo tag** → mặc định 0; lỗi bất ngờ → 200 `{status:false,msg:「保存に失敗しました。」}`, không lộ SQL, có log + Chatwork.
- **D-12** (v3, fix bug #43826) `edit_tag` (app + web dùng chung logic) không gửi `is_limit` (thiếu/null/rỗng) → set cả 3 cột `is_limit/limit/limit_action_mode = 0/0/0`. Gửi rõ `is_limit=0` → giữ `limit`/`limit_action_mode` cũ (không reset) — hành vi đã chốt thiết kế, không phải bug.
- **D-13** (v4, fix bug #44028/#3769) `edit_tag`: `tag_id` phải là **số** và là **tag của bot hiện tại**, sai → 403 `{status:false,msg:「このデータを操作する権限がありません。」}`, không ghi gì, có `logInfo`, không báo Chatwork (vì là request bị chặn chủ động, không phải lỗi server).
- **D-14** (v5, fix bug #3951) `validate-limit` bỏ route model binding, tự tra tag theo `id` + bot hiện tại — tag đã xoá/không tồn tại/thuộc bot khác → 403 `{message:「このデータを操作する権限がありません。」}` (không còn 404 tiếng Anh); màn sửa/copy alert message này, ở lại màn, không gọi `save-tag`.

**v6, v7, v8**: không đổi code — chỉ xác nhận lại 2 automation bug KHÔNG phải bug thật (`#3935`, `#3974`) và yêu cầu người cập nhật kỳ vọng 2 TC trên Test Studio (xem §4.3 + Ghi chú cuối file).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TagController::initDataInfo` (`app/Http/Controllers/Basic/TagController.php`) | Thêm filter `bot_id` khi load tag + action; D-1 | IDOR-FR-14 |
| 2 | `TagController` — `category/update`, `get-list-group-tag` (addAndEditGroup/moveItem/sortItem/sortFolder) | Thêm filter `bot_id` + 404 nếu folder không phải loại tag còn sống; D-2,3,6,10 | IDOR-FR-15, #42723 |
| 3 | `TagController::ajaxGetListCategoryTemplate` | Thêm filter `bot_id`; D-4 | IDOR-FR-21 |
| 4 | `TagController` — `save-tag` (add/copy/edit), `create-multiple`, `save-tag-csv` | Guard folder/action/limit_action theo bot + is_limit default + chặn SQL leak; D-5,10,11,12,13 | IDOR-FR-25, #42722, #43826, #44028 |
| 5 | `TagController::validateLimit` (`/ajax/v2/tag/validate-limit`) | Bỏ route model binding, tự tra theo bot; D-14 | IDOR-FR-27, #3951 |
| 6 | `TagController` — `friend-list` theo tag | Redirect `/basic/tag` nếu tag không thuộc bot; D-7 | IDOR-FR-27 |
| 7 | `resources/views/basic/tag/edit.blade.php` + route `POST /basic/tag/update` | Xoá view + route cũ (244 dòng); D-8 | Dọn code chết, màn sửa cũ đã thay bằng v2 |
| 8 | `TagMobileController` (`app/Http/Controllers/Api/Mobile/TagMobileController.php`) — `get-tag-detail`, `update-tag-folder`, `save-tag`, `create-multiple-tag` | Áp toàn bộ guard trên (bản song sinh app); D-9 + D-10..D-14 | Audit ghi rõ app có cùng lỗi |
| 9 | `findTagInBot` (helper dùng chung web/app, mới thêm) | Dùng ở nhiều guard trên | Trùng với helper cùng tên ở ticket anh em `#42421` → **conflict khi merge**, chỉ giữ 1 bản |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `POST /basic/initDataInfoTag` (copy/init tag) | TagController.php | Direct | D-1 |
| F2 | `PUT /ajax/v2/tag/category/update/{category}`, `POST /ajax/get-list-group-tag` (addAndEditGroup/moveItem) | TagController.php | Direct | D-2, D-3, D-10 |
| F3 | `POST /ajax/get-list-group-template` | TagController.php | Direct | D-4 |
| F4 | `save-tag` (add/copy/edit), `create-multiple`, `save-tag-csv` | TagController.php | Direct | D-5, D-10, D-11, D-12, D-13 |
| F5 | `sort-tag`, `sort-category`, `sortItem`, `sortFolder` | TagController.php | Direct | D-6 |
| F6 | `/basic/tag/friend-list/{id}`, `/ajax/v2/tag/validate-limit/{id}` | TagController.php | Direct | D-7, D-14 |
| F7 | `/basic/tag/edit/{id}` (route cũ), `POST /basic/tag/update` | routes/web.php, edit.blade.php (đã xoá) | Direct (removed) | D-8 |
| F8 | API app: `get-tag-detail`, `update-tag-folder`, `save-tag`, `create-multiple-tag` | TagMobileController.php | Direct | D-9, D-10..D-14 |
| F9 | Modal chọn template dùng chung `get-list-group-template` ở booking (`setting_default`, `list_slot_event`, `setting_booking_event`, `booking_event_day`), friendlist (`get_friend_follow`, `result_search`, `tag/edit.js`), detect URL (`setting_detect_url`, `template_v2/messages/detect_url`) | nhiều view/JS khác | Indirect | F3 dùng chung — group_id lạ nay bị coi như 0 |
| F10 | `get-list-group-tag` dùng ở 16 file JS/blade khác | nhiều view/JS | Indirect | Chỉ nhánh addAndEditGroup/moveItem/sortItem/sortFolder đổi |
| F11 | `ajaxSaveTag` (edit_tag nhánh) / `TagMobileController::saveTag` / `findTagInBot` / `validateLimit` | TagController.php, TagMobileController.php | Indirect — **risk merge** | Dùng chung với ticket anh em `#42421` (cùng sửa IDOR), 2 nhánh có message 403 khác nhau, phải chọn 1 khi merge |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `t_tags` (`category_id`, `action_id`, `limit_action_id`, `is_limit`, `limit`, `limit_action_mode`) | UPDATE (guard trước khi ghi, không đổi schema) | Guard bot/folder/action chạy trước câu ghi hiện có |
| D2 | `t_category` (tag folder) | UPDATE (rename/move guard) | D-2, D-3, D-10 |
| D3 | `t_actions` | READ (clone khi copy tag, kiểm bot_id trước clone) | D-1 |
| D4 | — | Không có migration / schema / config / job thay đổi | Dev xác nhận "không đổi bảng, migration, config, job" ở mọi vòng (đã kiểm diff) |
| D5 | Dữ liệu lệch cũ trên production (ngoài phạm vi code fix) | Cần dọn tay | DB dev: 2 tag (26005, 26024) trỏ folder bot khác; 7 tag trỏ folder không tồn tại; vài tag QA tạo ở lượt test #2985 (category 47639, 47640, 999999999). Nếu không dọn về `未分類`(0), lần lưu lại tiếp theo của các tag này sẽ bị 403/404 |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn Tag v2 (`/basic/tag`) — danh sách, sửa/copy tag, tạo nhiều, import CSV, folder (đổi tên/di chuyển/sort), sort tag | F1-F7, D1, D2 | High |
| T2 | API app Tag (`TagMobileController`) | F8 | High |
| T3 | Modal chọn template dùng chung (booking / friendlist / detect URL) | F9 | Medium |
| T4 | `get-list-group-tag` dùng ở 16 file JS/blade khác | F10 | Medium |
| T5 | Màn sửa tag cũ `/basic/tag/edit` | F7 | Low (đã xoá, chỉ cần verify redirect/404) |
| T6 | Merge với ticket `#42421` (cùng sửa `ajaxSaveTag`/`TagMobileController::saveTag`/`findTagInBot`/`validateLimit`) | F11 | **High — risk đặc biệt cần Leader lưu ý, không phải regression thông thường** |
| T7 | Test case trên Test Studio `NEW-66` (TC 31958) và `NEW-47` (TC 25210) | Bug con `#44028`/automation `#3769`,`#3935`,`#3974` | **High — 2 TC đang SAI kỳ vọng, hiện trạng thái `error` trong `testcase_list`** |

---

## Ghi chú quan trọng cho Leader (không có trong template gốc, bổ sung do ticket phức tạp)

1. **2 TC Studio cần sửa kỳ vọng trước khi review coverage** — Dev đã yêu cầu từ v4 đến v8 (5 vòng liên tiếp) nhưng **chưa có xác nhận đã sửa**:
   - `NEW-66` (TC 31958) — hiện kỳ vọng `edit_tag` với `tag_id` dạng mảng trả `200 {status:false,msg:「保存に失敗しました。」}` → phải đổi sang `403 {status:false,msg:「このデータを操作する権限がありません。」}`. Muốn giữ phần kiểm `保存に失敗しました`, đổi trigger sang `add_tag` với `tag_name` là mảng 2 phần tử.
   - `NEW-47` (TC 25210) — hiện kỳ vọng `validate-limit` với id không tồn tại trả `404` → phải đổi sang `403 {message:「このデータを操作する権限がありません。」}`.
   - Khớp với thực tế: `testcase_list` fetch về cho thấy **cả 2 TC này đang ở trạng thái `error`** (xem `04-tc-list.md`).
2. **Không tự chọn message 403 cuối cùng** — ticket `#42421` (đang chạy song song, cùng sửa chung code) dùng message khác (`このデータにアクセスする権限がありません。`) cho cùng nhánh `edit_tag`. Review TC cần coi cả 2 message là có thể đúng tuỳ thời điểm merge, tránh hardcode 1 message làm "sai" khi so sánh.
3. **16 requirement_keys REQ-001 → REQ-016** đã có sẵn trên Test Studio (`task_get_context`) — map khá sát với D-1→D-14; dùng để đối chiếu coverage ở BƯỚC 2 của `/review-tc` thay vì tự suy từ 4.1/4.2 ở trên khi cần chi tiết hơn.
4. **Case `0 TC chạy trên `prd`/`staging``** (76/76 TC đều chạy ở `local`) — RULE-08 áp dụng nếu có TC liên quan domain/job/bill tiền, nhưng ticket này chủ yếu là permission/IDOR nên rủi ro RULE-08 thấp; vẫn nên lưu ý khi review GAP.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
