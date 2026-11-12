# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42422 — Tag – Copy, folder, template, sort & id phụ` |
| Module / Màn hình | Tag v2 (`/basic/tag` — danh sách, sửa/copy tag, folder, sort, CSV) + API mobile Tag (`TagMobileController`). Controller chính: `app/Http/Controllers/Basic/TagController.php`. |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Đây KHÔNG phải bug báo lỗi từ khách hàng, mà là ticket security audit (IDOR) nội bộ — description gốc đã tiếng Việt, giữ nguyên văn. -->

Controller: TagController
Nguồn: security audit IDOR (Bạn bè / Tag / Form / Rich menu)

1. IDOR-FR-14 (3/3) [High] — Tag · Copy / init info tag chéo bot

* Vị trí: TagController.php:1117, 1131-1141 initDataInfo
* Route: POST /basic/initDataInfoTag — LOGIN · id (middleware: LOGIN)
* Vấn đề / Fix: Tags::where('id'), Actions::find/clone → load theo bot_id, bản copy gán bot_id = getBotId()

2. IDOR-FR-15 (1/4) [High] — Tag · Folder/category & move chéo bot

* Vị trí: TagController.php:280, 427-435
* Route: PUT /ajax/v2/tag/category/update/{category}, POST /ajax/get-list-group-tag — LOGIN (middleware: LOGIN)
* Vấn đề / Fix: DB::table('category')->where('id')->update(...) (mọi kind), DB::table(...)->where('id')->update(group_id); implicit binding Category không kiểm → bot_id + kind; abort_if($category->bot_id != getBotId(), 404)

3. IDOR-FR-21 (1/2) [Normal] — Tag · Đọc category template chéo bot

* Vị trí: TagController.php:720 ajaxGetListCategoryTemplate
* Route: POST /ajax/get-list-group-template — LOGIN · group_id (middleware: LOGIN)
* Vấn đề / Fix: Category::find($gid) → bot_id + kind

4. IDOR-FR-25 (1/5) [Normal] — Tag · Id phụ (action/folder/template…) lưu không kiểm bot

* Vị trí: TagController.php:288, 469, 639, 1422-1424, 1486-1488, 1516
* Route: các route lưu tag — LOGIN/BASIC (middleware: LOGIN BASIC)
* Vấn đề / Fix: action/folder/tag/template/scenario/switch id → kiểm bot_id (+kind) trước khi lưu

5. IDOR-FR-26 (1/4) [Low] — Tag · Sort chéo bot

* Vị trí: TagController.php:356, 368, 600, 612
* Route: /ajax/v2/tag/sort-* — LOGIN · sort_ids (middleware: LOGIN)
* Vấn đề / Fix: where('id')->update(['position']) → thêm bot_id

6. IDOR-FR-27 (1/5) [Low] — Tag · Đọc/ghi phụ chưa lọc bot, code chết

* Vị trí: TagController.php:1317, 1627, 842-888
* Route: — (middleware: —)
* Vấn đề / Fix: id đọc/ghi phụ chưa lọc bot; dọn code chết

## Steps to reproduce

<!-- Ticket security audit — không có Steps/Expected/Actual dạng bug thường. Mỗi mục trong "Mô tả bug" ở trên đã có Vị trí (file:line) + Route + Vấn đề/Fix tương đương. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Attachments (0) — Redmine #42422 không có attachment. -->

## Ghi chú thêm của Leader

⚠️ Đây là ticket **security audit (IDOR)** — 6 nhóm lỗi audit trong `TagController`/`TagMobileController`, KHÔNG có Steps to reproduce / Expected / Actual dạng bug khách báo. Dev (AI agent "Dev Studio", quyết định cuối do Truong Minh Hieu — HieuTM) đã fix qua **8 vòng thiết kế/handoff (v1 → v8)**, chi tiết đầy đủ ở phần Journal dưới + tổng hợp ở `03-dev-impact.md`.

**4 bug con phát sinh trong lúc QA (đã xử lý)**:
- `#43826` (v3, D-12) — đã fix: app sửa tag không gửi `is_limit` thì giữ nguyên `limit` cũ (sai) → nay reset về 0.
- `#44028` / automation `#3769` (v4, D-13) — đã fix: `tag_id` dạng mảng khi sửa tag ghi đè nhầm tag đầu tiên, báo thành công sai → nay `tag_id` phải là số thuộc bot hiện tại, sai → 403.
- automation `#3935` — **not a bug**: 403 cho `tag_id` dạng mảng là đúng thiết kế D-13/D-14 (Dev xác nhận kỳ vọng cũ của Test Studio sai).
- `#3951` (v5, D-14) — đã fix: `validate-limit` khi tag đã bị xoá ở tab khác trả lỗi 404 tiếng Anh → nay trả 403 kèm message tiếng Nhật.
- automation `#3974` — **not a bug**: `validate-limit` với id không tồn tại trả 403 (không phải 404) đúng thiết kế D-14.

⚠️ **Quan trọng cho QA**: Dev đã nhiều lần (từ v4 đến v8) yêu cầu người cập nhật lại kỳ vọng của 2 test case trên Test Studio — **`NEW-66`** (`tag_id` dạng mảng → đổi kỳ vọng từ `200 「保存に失敗しました。」` sang `403 「このデータを操作する権限がありません。」`; muốn kiểm `保存に失敗しました` thì đổi trigger sang `add_tag` với `tag_name` là mảng 2 phần tử) và **`NEW-47`** (`validate-limit` với id không tồn tại → đổi kỳ vọng từ `404` sang `403`) — nhưng **CHƯA có xác nhận đã sửa** (journal cuối #147623 vẫn còn liệt kê việc này ở "Việc cần người làm thêm"). Đúng như vậy, `testcase_list` fetch về cho thấy **`NEW-66` và `NEW-47` đang ở trạng thái `error`** — khớp với cảnh báo của Dev. Xem thêm ở `04-tc-list.md` + §Warnings khi review.

⚠️ **Rủi ro conflict merge với ticket `#42421`** (nhánh anh em, cùng sửa `ajaxSaveTag`/`TagMobileController::saveTag`/`findTagInBot`/`validateLimit`) — 2 nhánh dùng 2 message 403 khác nhau (`このデータを操作する権限がありません。` của #42422 vs `このデータにアクセスする権限がありません。` của #42421). Khi merge chỉ giữ 1 bản `findTagInBot`, người merge chọn 1 message. TC review cần lưu ý message 403 có thể đổi sau merge.

⚠️ **Dữ liệu lệch cũ trên production cần dọn** (ngoài phạm vi code fix) — DB dev có: 2 tag (26005, 26024) trỏ folder của bot khác, 7 tag trỏ folder không tồn tại, cùng vài tag QA tạo ra ở lượt test #2985 (category 47639, 47640, 999999999). Nếu không dọn về `未分類` (id 0), lần lưu lại tiếp theo của các tag này sẽ bị 403/404.

⚠️ Không đổi bảng, migration, config, job, JS/CSS ở mọi vòng — không cần hard-reload khi deploy. **Riêng v8 (hiện tại) không đổi code so với v5-v7** — commit hiện hành: `sns-line@188ad8624d314b08be69b2499bd2df0384c18d8a`.

## Journal / note từ Redmine (nguyên văn)

**Journal #141493 — Dev Studio — 2026-10-08:**

```
Dev Studio · Nội dung thực hiện (v1)

Đã viết thiết kế v1 chặn IDOR cho 6 mục audit của TagController: copy/xem chi tiết tag, đổi tên và di chuyển folder, đọc folder template, id phụ khi lưu (folder, action), sắp xếp và đọc phụ, kèm dọn hàm update() chết. Khi id thuộc bot khác, hệ thống trả 403 và không ghi dữ liệu; với request hợp lệ thì hành vi giữ nguyên. Bản song sinh trên app (TagMobileController) có cùng lỗi nên được đưa vào phạm vi. Các phần thuộc ticket anh em #42421 và #42424 không làm ở đây. Thiết kế đã sẵn sàng thực thi, chỉ cần lưu ý dễ bị conflict với #42421.

Hướng sửa:
- D-1 initDataInfo: tìm tag theo bot, kiểm action trước khi xem trước hoặc nhân bản
- D-2 Folder: chặn đổi tên folder của bot khác
- D-3 Move tag: kiểm folder đích thuộc bot
- D-4 ajaxGetListCategoryTemplate: chỉ đọc folder template của bot
- D-5 Kiểm id phụ (folder, action) trước khi lưu tag
- D-6 Sort: thêm điều kiện bot_id vào câu cập nhật position
- D-7 Đọc phụ: friendList và validateLimit lọc theo bot
- D-8 Dọn code chết update()/edit() cũ
- D-9 Sửa bản song sinh trên app TagMobileController

Ảnh hưởng / rủi ro:
Ảnh hưởng màn Tag v2 (danh sách, folder, sửa/copy, CSV), các modal chọn template/tag dùng get-list-group-template và get-list-group-tag ở nhiều màn, và API tag của app. Rủi ro chính là conflict khi merge với #42421 (cùng sửa ajaxSaveTag edit_tag và TagMobileController). Cần test hồi quy các thao tác hợp lệ trên chính bot, gồm cả folder 未分類.
```

**Journal #141727 — Dev Studio — 2026-10-08 (Dev handoff v1):**

```
Dev handoff — v1 · nhánh ai_studio_implement_42422

Tóm tắt:
Chặn bot A thao tác dữ liệu tag/folder/action của bot B qua 6 nhóm endpoint của màn Tag (copy/init tag, folder & move, template folder, lưu tag với id phụ, sort, đọc phụ) và 4 API app tương ứng; dọn màn sửa tag cũ đã chết. Khi test chú ý nhất: luồng hợp lệ của bot mình (tạo/sửa/copy/CSV/folder/sort, 未分類 id 0) phải giữ nguyên; id của bot khác phải bị 403 và không ghi gì. Modal chọn template dùng chung ở booking/friendlist/detect URL cũng đi qua endpoint đã sửa nên cần test lướt.

Nội dung thay đổi:
- Màn Tag: copy/khởi tạo thông tin tag (/basic/initDataInfoTag) chỉ cho tag của bot mình; tag của bot mình trỏ action lệch bot thì không preview/không nhân bản action đó và báo Chatwork.
- Màn Tag: đổi tên folder (PUT category/update, addAndEditGroup) và di chuyển tag vào folder (move-category, moveItem) chỉ với folder tag của bot mình; sai → 403 kèm message 「このデータを操作する権限がありません。」.
- Modal chọn template (/ajax/get-list-group-template, dùng ở nhiều màn): group_id không phải folder template của bot mình → coi như 未分類.
- Lưu tag (save-tag add/copy/edit), tạo nhiều tag, import CSV: folder/action/action giới hạn của bot khác → 403, không tạo/sửa.
- Sắp xếp tag/folder (sort-tag, sort-category, sortItem, sortFolder): id của bot khác bị bỏ qua im lặng.
- Màn danh sách bạn theo tag (/basic/tag/friend-list/{id}) với tag bot khác → về /basic/tag; validate-limit tag bot khác → 403.
- URL màn sửa cũ /basic/tag/edit/{id} chuyển sang màn sửa v2; POST /basic/tag/update và view cũ basic/tag/edit đã xoá.
- App (API mobile): get-tag-detail, update-tag-folder, save-tag, create-multiple-tag chặn id của bot khác (403).

File đã sửa (php-web):
  .../Controllers/Api/Mobile/TagMobileController.php | 101 +++++++-
  app/Http/Controllers/Basic/TagController.php       | 287 +++++++++++----------
  resources/views/basic/tag/edit.blade.php           | 244 ------------------
  routes/web.php                                     |   2 -
  4 files changed, 255 insertions(+), 379 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ thêm điều kiện bot_id/kind vào câu tìm/ghi và guard trả 403 trước khi ghi; luồng hợp lệ giữ nguyên câu ghi và response. Harness kiểm cả nhánh hợp lệ (folder 0, folder/action của mình, detail bot_id NULL) và nhánh chặn; chưa verify runtime.
- Màn Tag v2 (/basic/tag): mọi thao tác tạo/sửa/copy tag, tạo nhiều, import CSV, folder (đổi tên/sắp xếp/di chuyển), sắp xếp tag — các endpoint /ajax/v2/tag/*, /ajax/save-tag*, /basic/initDataInfoTag đều có thêm điều kiện bot_id.
- Modal chọn template qua /ajax/get-list-group-template ở màn booking (setting_default, list_slot_event, setting_booking_event, booking_event_day), friendlist (script.js, get_friend_follow, result_search với tag/edit.js) và detect URL (setting_detect_url, template_v2/messages/detect_url): group_id lạ nay bị coi như 0.
- /ajax/get-list-group-tag (16 file JS/blade gọi): chỉ đổi nhánh addAndEditGroup, moveItem, sortItem, sortFolder.
- URL cũ /basic/tag/edit/{id} (còn trong js/tag/index.js của view cũ không render) nay redirect; POST /basic/tag/update trả 404.
- API app /api/mobile/save-tag, get-tag-detail, create-multiple-tag, update-tag-folder: thêm 403; bản Flutter phát hành hiện không gọi các API này.
- Tag có dữ liệu lệch cũ (folder/action của bot khác) sẽ bị 403 khi lưu lại cho tới khi chọn lại folder/action.
- Không đổi bảng, migration, config, job.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy:
- Không đổi JS/CSS nên không cần hard-reload.
- Merge chung với #42421 (cùng sửa ajaxSaveTag và TagMobileController::saveTag) cần kiểm tay để giữ cả guard của #42422 lẫn câu update có bot_id của #42421.

Việc cần người làm thêm (ngoài phạm vi task):
- Kiểm dữ liệu production: tag đang trỏ tới folder hoặc action của bot khác (DB dev có 2 tag: 26005 và 26024), rồi quyết định cách sửa dữ liệu cũ.
- Báo người làm #42421: TagMobileController::saveTag nhánh edit cũng update tag theo id mà không lọc bot_id (song sinh của IDOR-FR-12).
- DB dev có 2 tag đang trỏ vào folder của bot khác (tag 26005 và 26024, dữ liệu đến 2026-06-08). Cần người kiểm trên production và chuyển các tag này về 未分類 (id 0); nếu để nguyên, lần lưu lại tiếp theo của các tag đó sẽ bị 403.
- FE màn Tag v2 đang im lặng khi gặp 403 ở /basic/initDataInfoTag và /ajax/save-tag-csv (không có alert). Chỉ ảnh hưởng request giả mạo, nhưng có thể làm việc cải tiến riêng để hiển thị thông báo.
- Bộ PHPUnit của dự án đang có 4 file lỗi sẵn trên base (BillingServiceTest, ChatMediaSizeValidationTest, ContractExpireServiceTest fatal, Feature/ExampleTest); nên giao người sửa riêng.
- web.php còn 4 route trỏ tới method không tồn tại trong TagController (createCategoryTag, deleteCategoryTag, createTag, findTag). Đây là code chết có sẵn, ngoài phạm vi #42422.
- Khi merge cần chú ý conflict với #42421, vì ticket đó cũng sửa ajaxSaveTag (edit_tag) và TagMobileController.
- Kiểm trên DB production các tag có category_id trỏ folder của bot khác (dev có 2: tag 26005, 26024) hoặc action_id/limit_action_id có detail thuộc bot khác, rồi reset về 0/null hoặc folder đúng bot để khách không bị 403 khi sửa các tag đó.

Điểm cần test:
- Đăng nhập bot A, gọi /basic/initDataInfoTag với id tag của bot B (có và không có action=copy_tag) ⇒ 403, không phát sinh t_actions mới
- PUT /ajax/v2/tag/category/update/{folder bot B} ⇒ 403, tên folder B không đổi; dùng folder template (kind khác 0) của A cũng ⇒ 403
- get-list-group-tag action=addAndEditGroup với id folder của B ⇒ folder B không đổi
- move-category và moveItem với folder_move_id của B ⇒ 403, tag của A giữ nguyên folder
- /ajax/get-list-group-template với group_id là folder của B ⇒ không trả template của B
- save-tag (add/copy/edit), create-multiple, save-tag-csv với folder hoặc action/limit_action của B ⇒ 403, không tạo hay sửa tag
- sort-tag, sort-category, sortItem, sortFolder có lẫn id của B ⇒ position của B không đổi, id của A vẫn sắp xếp đúng
- /basic/tag/friend-list/{tag B} ⇒ chuyển về /basic/tag; validate-limit/{tag B} ⇒ 403
- /basic/tag/edit/{tag A} ⇒ chuyển sang màn sửa v2; POST /basic/tag/update ⇒ 404
- API app get-tag-detail, update-tag-folder, save-tag, create-multiple-tag với id của B ⇒ bị chặn
- Hồi quy trên bot A: tạo/sửa/copy tag có action và giới hạn, tạo nhiều tag, import CSV, tạo/đổi tên/xoá/sắp xếp folder, di chuyển và sắp xếp tag, chọn template/tag trong modal action ở các màn khác, folder 未分類 (id 0)

Branch: ai_studio_implement_42422
- sns-line: ai_studio_implement_42422 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit 177b5e379a4554f99da8a799b2e54f7dcb6fd116)
```

**Journal #142646 — Dev Studio — 2026-10-12 (v2 — bug #42723, #42722):**

```
Dev Studio · Nội dung thực hiện (v2)

Thiết kế v2 xử lý 2 bug QA vòng 1. Với #42723: bản v1 chỉ kiểm folder có thuộc bot khác không, nên vẫn cho lưu, di chuyển hoặc tạo tag vào folder template, folder đã xoá hay id không tồn tại. v2 chỉ nhận folder tag còn sống của chính bot: folder của bot khác vẫn trả 403, các trường hợp còn lại trả 404 kèm câu 「フォルダが見つかりません。」, áp ở đủ 7 lối vào trên web và app. Với #42722: save-tag dùng mặc định 0 khi thiếu is_limit, và khi gặp lỗi chỉ trả message chung, không còn lộ câu SQL. Lỗi này có sẵn từ base. Thiết kế đã sẵn sàng để thực thi.

Hướng sửa:
- D-10 Chỉ cho lưu/chuyển/tạo tag vào folder tag còn sống của chính bot
- D-11 save-tag: mặc định 0 cho trường giới hạn và không lộ SQL khi lỗi

Ảnh hưởng / rủi ro:
Ảnh hưởng các thao tác lưu, copy, tạo nhiều, di chuyển và import CSV tag trên màn Tag v2, cùng API save-tag và create-multiple-tag của app. Rủi ro: thao tác vào folder vừa bị xoá ở tab khác sẽ nhận 404 thay vì lưu "mất" tag. Cần test hồi quy với folder hợp lệ và 未分類.
```

**Journal #142662 — Dev Studio — 2026-10-12 (Dev handoff v2):**

```
Dev handoff — v2 · nhánh ai_studio_implement_42422

Tóm tắt:
Chặn bot A thao tác dữ liệu tag/folder/action của bot B ở màn Tag và API tag của app, và dọn màn sửa tag cũ. Vòng 2 sửa 2 bug QA. Folder đích nay phải là folder tag còn sống của chính bot: folder template, folder đã xoá hoặc id không tồn tại trả 404, folder bot khác vẫn trả 403. Lưu tag thiếu trường giới hạn được mặc định 0 và không còn lộ SQL. Khi test chú ý luồng hợp lệ (folder của mình, 未分類) vẫn lưu, copy, di chuyển bình thường.

Nội dung thay đổi:
- Màn Tag: copy/khởi tạo thông tin tag chỉ cho tag của bot mình. Tag trỏ action lệch bot thì không preview, không nhân bản action đó, và có báo Chatwork.
- Màn Tag: đổi tên folder và di chuyển tag chỉ với folder tag của bot mình.
- Lưu tag (add/copy/edit), tạo nhiều tag, import CSV, di chuyển tag: folder template, folder đã xoá, id không tồn tại trả 404 「フォルダが見つかりません。」. Folder hoặc action của bot khác trả 403 「このデータを操作する権限がありません。」.
- Lưu tag trên web và app: thiếu is_limit, limit, limit_action_mode thì lưu 0. Lỗi bất ngờ trả 「保存に失敗しました。」, không lộ SQL, và báo Chatwork.
- Modal chọn template dùng ở nhiều màn: group_id không phải folder template của bot mình được coi như 未分類.
- Sắp xếp tag/folder bỏ qua id của bot khác. Danh sách bạn theo tag và validate-limit chặn tag của bot khác.
- URL màn sửa cũ /basic/tag/edit/{id} chuyển sang màn sửa v2. POST /basic/tag/update và view cũ đã bị xoá.
- API app get-tag-detail, update-tag-folder, save-tag, create-multiple-tag chặn id của bot khác. save-tag và create-multiple-tag còn chặn folder không hợp lệ (404).

File đã sửa (php-web):
  .../Controllers/Api/Mobile/TagMobileController.php | 169 +++++++++-
  app/Http/Controllers/Basic/TagController.php       | 355 +++++++++++++--------
  resources/views/basic/tag/edit.blade.php           | 244 --------------
  routes/web.php                                     |   2 -
  4 files changed, 375 insertions(+), 395 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi chỉ thêm điều kiện bot_id/kind/is_deleted và guard trước câu ghi, cùng giá trị mặc định trùng default của cột. Luồng hợp lệ có test hồi quy trong harness. Chưa verify runtime.
- Màn Tag v2: lưu/copy/sửa tag, tạo nhiều tag, di chuyển tag, import CSV. Folder không hợp lệ của chính bot nay bị từ chối 404 thay vì được nhận rồi tag biến mất khỏi danh sách.
- Phản hồi lỗi của save-tag web và app đổi từ câu lỗi kỹ thuật sang 「保存に失敗しました。」. FE màn sửa v2 hiện alert message này.
- API app save-tag và create-multiple-tag có thêm mã 404. Bản Flutter phát hành hiện không gọi các API này.
- Modal chọn template qua get-list-group-template ở booking, friendlist, detect URL, và tag/edit.js trong friendlist/result_search (thay đổi từ vòng 1).
- get-list-group-tag: các nhánh addAndEditGroup, moveItem, sortItem, sortFolder (thay đổi từ vòng 1).
- Tag có dữ liệu lệch cũ (folder của bot khác hoặc folder không tồn tại) bị 403 hoặc 404 khi lưu lại qua app hoặc API cho tới khi chọn lại folder.
- Không đổi bảng, migration, config, job.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy:
- Không đổi JS/CSS nên không cần hard-reload.
- Merge chung với #42421 phải kiểm tay ajaxSaveTag và TagMobileController::saveTag. Cần giữ guard folder/action, default giới hạn, catch an toàn, và câu update có bot_id của #42421.

Việc cần người làm thêm (ngoài phạm vi task):
- Nhiều catch khác trong TagController và TagMobileController (ví dụ get-list-group-tag, initDataInfo, save-tag-csv, getTagDetail) vẫn trả nguyên exception message ra body. Nên tạo ticket riêng để dọn nếu cần.
- Sửa dữ liệu cũ: các tag trỏ tới folder không tồn tại sẽ không hiện trên màn danh sách (DB dev có 7 tag), cùng các tag QA đã tạo trong lượt test #2985 (category 47639, 47640, 999999999).
- DB dev có 7 tag trỏ tới folder không tồn tại. Cần người kiểm trên production và chuyển các tag này về 未分類 (id 0): nếu app gửi lại đúng category_id cũ khi sửa thì nay sẽ nhận 404.
- Màn Tag v2 vẫn im lặng khi import CSV gặp lỗi 403/404 (đã ghi từ v1); có thể làm cải tiến riêng để hiện thông báo.
- Khi merge cần chú ý conflict với #42421, vì ticket đó cũng sửa ajaxSaveTag (edit_tag) và TagMobileController saveTag.
- Bộ PHPUnit của dự án có sẵn 4 file lỗi trên base (BillingServiceTest, ChatMediaSizeValidationTest, ContractExpireServiceTest, Feature/ExampleTest); nên giao người sửa riêng.
- Dọn dữ liệu lệch trên production: đưa về 未分類 (0) các tag trỏ folder của bot khác hoặc folder không tồn tại. Trên DB dev có 2 tag trỏ folder bot khác và 7 tag trỏ folder không tồn tại. Mục đích là khách không bị 403 hoặc 404 khi lưu lại các tag đó.

Điểm cần test:
- Bot A: save-tag add/copy/edit với category_id là folder template của A, folder tag đã xoá của A, hoặc 999999999 ⇒ 404 「フォルダが見つかりません。」, không tạo hay sửa tag
- move-category và moveItem với folder_move_id là folder template, folder đã xoá hoặc id không tồn tại ⇒ 404, tag vẫn ở folder cũ
- create-multiple, save-tag-csv, app save-tag, app create-multiple-tag với các folder không hợp lệ trên ⇒ 404, không tạo tag
- Các lối trên với folder tag của bot B ⇒ vẫn 403
- Folder tag còn sống của A và 未分類 (0) ⇒ lưu, di chuyển, tạo nhiều, import CSV bình thường
- App save-tag add_tag không gửi is_limit ⇒ 200 status=true, tag có is_limit=0; gửi is_limit=1, limit=5 ⇒ lưu đúng
- save-tag (web và app) gặp exception, ví dụ tên quá 255 ký tự ⇒ body chỉ có 「保存に失敗しました。」, không có SQL hay tên cột
- Hồi quy toàn bộ các điểm kiểm thử của v1 (IDOR chéo bot, sort, copy, friend-list, validate-limit)

Branch: ai_studio_implement_42422
- sns-line: ai_studio_implement_42422 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit 450bd344c7f784941c4ea4879a50ef8b947dff8b)
```

**Journal #146844 — Dev Studio — 2026-10-22 (v3 — bug #43826):**

```
Dev Studio · Nội dung thực hiện

Bản v3 sửa bug QA #43826. Nguyên nhân: khi app sửa tag mà không gửi các trường giới hạn, code chỉ ghi is_limit=0 còn limit và limit_action_mode giữ giá trị cũ (DB ra 0/5/1). Thêm D-12: khi sửa tag mà không gửi is_limit (thiếu, null hoặc rỗng) thì lưu cả 3 cột về 0, áp cho cả app lẫn bản web dùng chung logic. Nếu client gửi rõ is_limit=0 thì hành vi giữ như cũ, nên màn web không đổi. Không cần sửa dữ liệu vì code v2 chưa phát hành, còn giá trị limit thừa không có tác dụng khi is_limit=0.

Hướng sửa:
- D-12 edit_tag không gửi is_limit thì lưu is_limit/limit/limit_action_mode = 0/0/0 (app saveTag và web ajaxSaveTag)

Ảnh hưởng / rủi ro:
Chỉ đổi nhánh edit_tag của API app save-tag và ajax/save-tag web, và chỉ khi request không gửi is_limit. Màn web luôn gửi đủ trường nên không đổi; cần test lại sửa tag có hoặc không giới hạn trên app và web.
```

**Journal #146869 — Dev Studio — 2026-10-22 (Dev handoff v3):**

```
Dev handoff — 22/10 14:17 · nhánh ai_studio_implement_42422

Tóm tắt:
Bản này chặn bot A thao tác dữ liệu tag, folder và action của bot B ở màn Tag và API tag của app, đồng thời dọn màn sửa tag cũ. Folder đích phải là folder tag còn sống của chính bot. Lưu tag không còn lộ SQL. Vòng 3 sửa bug #43826: sửa tag mà không gửi is_limit thì cả 3 cột giới hạn về 0. Khi test cần biết rằng gửi rõ is_limit=0 vẫn giữ số giới hạn cũ theo thiết kế, và màn web chuyển 制限する ↔ 制限しない phải lưu bình thường.

Nội dung thay đổi:
- Màn Tag: copy và khởi tạo thông tin tag chỉ cho tag của bot mình. Tag trỏ action lệch bot thì không preview, không nhân bản action đó, và có báo Chatwork.
- Màn Tag: đổi tên folder và di chuyển tag chỉ với folder tag của bot mình.
- Lưu tag (add/copy/edit), tạo nhiều tag, import CSV, di chuyển tag: folder template, folder đã xoá hoặc id không tồn tại trả 404 「フォルダが見つかりません。」. Folder hoặc action của bot khác trả 403 「このデータを操作する権限がありません。」.
- Lưu tag trên web và app: khi tạo tag thiếu trường giới hạn thì lưu 0. Lỗi bất ngờ trả 「保存に失敗しました。」, không lộ SQL, và có báo Chatwork.
- Sửa tag qua app hoặc ajax/save-tag mà không gửi is_limit (thiếu, null hoặc rỗng) thì lưu is_limit=0, limit=0, limit_action_mode=0 (bug #43826). Gửi rõ is_limit=0 thì giữ số giới hạn cũ.
- Modal chọn template: group_id không phải folder template của bot mình được coi như 未分類.
- Sắp xếp tag và folder bỏ qua id của bot khác. Danh sách bạn theo tag và validate-limit chặn tag của bot khác.
- URL màn sửa cũ /basic/tag/edit/{id} chuyển sang màn sửa v2. POST /basic/tag/update và view cũ đã bị xoá.
- API app get-tag-detail, update-tag-folder, save-tag và create-multiple-tag chặn id của bot khác. save-tag và create-multiple-tag còn chặn folder không hợp lệ.

Bug QA con:
- #43826 đã sửa (commit sns-line@b4b9b638cc98): Đã sửa nhánh edit_tag của save-tag ở cả app và web. Khi không gửi is_limit (thiếu, null hoặc rỗng), tag được lưu is_limit=0, limit=0, limit_action_mode=0 thay vì giữ limit cũ. Gửi rõ is_limit=0 vẫn giữ số giới hạn cũ theo thiết kế.

File đã sửa (php-web):
  .../Controllers/Api/Mobile/TagMobileController.php | 176 +++++++++-
  app/Http/Controllers/Basic/TagController.php       | 362 +++++++++++++--------
  resources/views/basic/tag/edit.blade.php           | 244 --------------
  routes/web.php                                     |   2 -
  4 files changed, 387 insertions(+), 397 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi chỉ thêm điều kiện và guard trước câu ghi, cùng giá trị mặc định trùng default của cột. Vòng 3 chỉ thêm một nhánh cho trường hợp thiếu is_limit, và màn web không đi vào nhánh này. Harness có test hồi quy cho luồng hợp lệ. Chưa verify runtime.
- Nhánh edit_tag của API app save-tag và ajax/save-tag: client cũ không gửi is_limit sẽ tắt giới hạn của tag. Trên base, request này lỗi SQL hẳn.
- Màn Tag v2: lưu, copy, sửa, tạo nhiều tag, di chuyển tag, import CSV, đổi tên và sắp xếp folder. Các thao tác này nay có thêm guard bot/folder/action.
- Modal chọn template qua get-list-group-template ở booking, friendlist, detect URL, và tag/edit.js trong friendlist/result_search.
- get-list-group-tag: các nhánh addAndEditGroup, moveItem, sortItem, sortFolder.
- API app tag có thêm mã 403/404. Bản Flutter phát hành hiện không gọi các API này.
- Tag có dữ liệu lệch cũ, tức trỏ folder bot khác hoặc folder không tồn tại, bị 403/404 khi lưu lại qua app hoặc API cho tới khi chọn lại folder.
- Không đổi bảng, migration, config, job hay JS/CSS.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy:
- Không đổi JS/CSS nên không cần hard-reload.
- Merge chung với #42421 phải kiểm tay ajaxSaveTag và TagMobileController::saveTag. Cần giữ guard folder/action, default giới hạn, catch an toàn và câu update có bot_id của #42421.

Việc cần người làm thêm (ngoài phạm vi task):
- Dọn dữ liệu lệch trên production: đưa về 未分類 (0) các tag trỏ folder của bot khác hoặc folder không tồn tại. DB dev có 2 tag trỏ folder bot khác và 7 tag trỏ folder không tồn tại. Việc này để khách không bị 403/404 khi lưu lại các tag đó.

Branch: ai_studio_implement_42422
- sns-line: ai_studio_implement_42422 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit b4b9b638cc986f47669eb07582c86f195f5e3d42)
```

**Journal #147479 — Dev Studio — 2026-10-23 (v4 — bug automation #3769):**

```
Dev Studio · Nội dung thực hiện

Bản v4 sửa bug automation #3769: app sửa tag với tag_id dạng mảng thì báo thành công và ghi đè tag đầu tiên. Nguyên nhân là nhánh sửa tag không kiểm tag_id. Bản web cũng chỉ trả lỗi vì tình cờ gặp exception. Thêm D-13: ở cả app và web, tag_id phải là một số và là tag của bot hiện tại, nếu không thì trả 403 và không ghi gì. Cách kiểm giống nhánh anh em #42421 để dễ merge. Mã trả về 403 khác với kỳ vọng 「保存に失敗しました。」 của Test Studio, nên test case cần cập nhật theo.

Hướng sửa:
- D-13 edit_tag kiểm tag_id là số và thuộc bot trước khi lưu (app saveTag và web ajaxSaveTag)

Ảnh hưởng / rủi ro:
Chỉ đổi nhánh edit_tag của API app save-tag và web ajax/save-tag. Màn web luôn gửi tag_id hợp lệ nên không đổi luồng. Cần test lại sửa tag thường trên cả hai. Chắc chắn conflict với nhánh #42421 ở cùng đoạn code.
```

**Journal #147488 — Dev Studio — 2026-10-23 (Dev handoff v4):**

```
Dev handoff — 23/10 10:37 · nhánh ai_studio_implement_42422

Bug QA con:
- #44028 đã sửa (commit sns-line@b4a39f94fa1a): Đã sửa guard đầu nhánh edit_tag ở cả app save-tag và web ajax/save-tag: tag_id phải là một số và là tag của bot hiện tại. Mảng [TA1,TA2] nay trả 403 {status:false,msg:「このデータを操作する権限がありません。」}, TA1 và TA2 không đổi, có logInfo. Kết quả là 403 thay cho kỳ vọng 200 「保存に失敗しました。」, vì đây là request bị chặn chủ động.

Bug automation Test Studio:
- Bug #3769 đã sửa (commit sns-line@b4a39f94fa1a): Đã sửa ở app và web: tag_id sai nay trả 403 {status:false,msg:「このデータを操作する権限がありません。」}, không ghi tag và không chạm option form. Không có tin Chatwork vì đây là request bị chặn chứ không phải lỗi server. Cần đổi kỳ vọng của NEW-66 từ 200 「保存に失敗しました。」 sang 403.

Lưu ý khi deploy:
- Merge chung với #42421 chắc chắn conflict ở nhánh edit_tag của ajaxSaveTag và TagMobileController::saveTag. Chỉ giữ một bản findTagInBot vì hai bản giống hệt. Chọn một trong hai message 403.
- Test Studio cần cập nhật kỳ vọng của test case NEW-66: request tag_id dạng mảng trả 403 「このデータを操作する権限がありません。」.

Branch: ai_studio_implement_42422
- sns-line: ai_studio_implement_42422 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit b4a39f94fa1a7483a75dea9fc31d100abee04e4f)
```

**Journal #147557 — Dev Studio — 2026-10-23 (v5 — bug #3951):**

```
Dev Studio · Nội dung thực hiện

Bản v5 thêm D-14 để sửa bug #3951: tag đã bị xoá ở tab khác mà bấm 保存 thì bước kiểm giới hạn hiện báo lỗi 404 tiếng Anh. Sau khi sửa, bước này tự tìm tag trong bot hiện tại; không thấy thì trả 403 「このデータを操作する権限がありません。」, ở lại màn và không lưu. Với hai bug #3769 và #3935 (tag_id dạng mảng), code giữ nguyên mức chặn 403 đã làm ở v4. Chính lượt chạy #4964 của Test Studio cũng ghi nhận đây là đúng thiết kế, nên test case cần đổi kỳ vọng và dùng cách khác để tạo lỗi server.

Hướng sửa:
- D-14 validate-limit tự tra tag theo bot, tag đã xoá/không thuộc bot thì trả 403 message tiếng Nhật

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng nút 保存 ở màn sửa và copy tag v2, khi tag đã bị xoá hoặc không thuộc bot. Tag hợp lệ đi luồng như cũ. Có thể conflict nhẹ với nhánh #42421 ở hàm validateLimit.
```

**Journal #147561 — Dev Studio — 2026-10-23 (Dev handoff v5):**

```
Dev handoff — 23/10 11:41 · nhánh ai_studio_implement_42422

Bug automation Test Studio:
- Bug #3769 đã sửa (commit sns-line@b4a39f94fa1a): Tag không còn bị ghi đè. App và web đều trả 403 {status:false,msg:「このデータを操作する権限がありません。」} cho tag_id dạng mảng, không ghi gì, có logInfo và không báo Chatwork vì đây không phải lỗi server. NEW-66 cần đổi trigger lỗi server, ví dụ add_tag với tag_name là mảng 2 phần tử.
- Bug #3935 không phải bug: Web /ajax/save-tag trả 403 cho tag_id dạng mảng là hành vi đã chốt trong thiết kế v4 (D-13) và v5. Lượt #4964 của Test Studio cũng ghi nhận như vậy, các test case chặn tag_id cùng lượt đều mong đợi 403. NEW-66 cần dùng trigger khác cho 「保存に失敗しました。」.
- Bug #3951 đã sửa (commit sns-line@188ad8624d31): validate-limit không dùng route model binding nữa mà tự tra tag theo id và bot hiện tại. Tag đã xoá, không tồn tại hoặc của bot khác trả 403 {message:「このデータを操作する権限がありません。」}. Màn sửa/copy alert message này, ở lại màn và không gọi save-tag.

Lưu ý khi deploy:
- Khi merge với #42421: phần edit_tag của ajaxSaveTag và TagMobileController::saveTag chắc chắn conflict. Chỉ giữ một bản findTagInBot và chọn một message 403. Với validateLimit, giữ bản của nhánh này.
- Test Studio cần cập nhật test case NEW-66: tag_id dạng mảng trả 403. Để kiểm 「保存に失敗しました。」, hãy dùng trigger khác, ví dụ tag_name là mảng.

Branch: ai_studio_implement_42422
- sns-line: ai_studio_implement_42422 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit 188ad8624d314b08be69b2499bd2df0384c18d8a)
```

**Journal #147589 — Dev Studio — 2026-10-23 (v6 — không đổi code):**

```
Dev Studio · Nội dung thực hiện

Bản v6 không có thay đổi code. Hai bug của vòng này đều do test case còn ghi kỳ vọng cũ, còn code đang chạy đúng thiết kế đã chốt. Bug #3769: lỗi ghi đè đã được sửa ở v4, nay tag_id dạng mảng bị chặn bằng 403 và không ghi gì. Bug #3974: validate-limit với id không tồn tại trả 403 như thiết kế v5, test case vẫn đợi 404. Việc còn lại là Test Studio cập nhật hai test case NEW-66 và NEW-47 theo kỳ vọng ghi trong tài liệu.

Ảnh hưởng / rủi ro:
Không đổi code nên không có ảnh hưởng mới. Nếu hai test case NEW-66 và NEW-47 không được cập nhật, Test Studio sẽ tiếp tục mở lại hai bug này ở mọi vòng.
```

**Journal #147593 — Dev Studio — 2026-10-23 (Dev handoff v6):**

```
Dev handoff — 23/10 13:31 · nhánh ai_studio_implement_42422

Bug automation Test Studio:
- Bug #3769 đã sửa (commit sns-line@b4a39f94fa1a): Tag không còn bị ghi đè. tag_id dạng mảng trả 403 「このデータを操作する権限がありません。」, có logInfo, không có Chatwork. Để kiểm 「保存に失敗しました。」, NEW-66 nên dùng add_tag với tag_name là mảng 2 phần tử.
- Bug #3974 không phải bug: validate-limit với id không tồn tại trả 403 {message:「このデータを操作する権限がありません。」} đúng thiết kế D-14 (docs/design/v5.md, v6.md mục 4; commit 188ad8624d). Test case NEW-47 (TC 25210) cần đổi kỳ vọng 404 thành 403.

Việc cần người làm thêm (ngoài phạm vi task):
- Test Studio cập nhật test case NEW-66: với tag_id dạng mảng thì kỳ vọng 403 「このデータを操作する権限がありません。」 và không có Chatwork; phần kiểm 「保存に失敗しました。」 dùng add_tag với tag_name là mảng.
- Test Studio cập nhật test case NEW-47: validate-limit với id không tồn tại thì kỳ vọng 403 「このデータを操作する権限がありません。」 thay cho 404.

Branch: ai_studio_implement_42422
- sns-line: ai_studio_implement_42422 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit 188ad8624d314b08be69b2499bd2df0384c18d8a)
```

**Journal #147607 — Dev Studio — 2026-10-23 (v7 — không đổi code):**

```
Dev Studio · Nội dung thực hiện

Bug #3769 bị gửi lại lần thứ năm nhưng không có bằng chứng mới. Lỗi ghi đè chỉ xảy ra trên code cũ, còn code hiện tại chặn đúng bằng 403. Bản v7 không sửa code và giữ phương án A mà HieuTM đã chốt. Tôi đã thử nhắn Test Studio cập nhật test case NEW-66, nhưng bị từ chối vì token của Dev Studio chưa có quyền gửi góp ý. Cần một người cập nhật NEW-66 và NEW-47 rồi đóng Redmine #44028, nếu không vòng sau bug sẽ lại bị gửi.

Ảnh hưởng / rủi ro:
Không đổi code nên không có ảnh hưởng mới. Nếu chưa ai cập nhật test case, vòng sau Test Studio sẽ lại gửi #3769, và có thể cả #3935, #3974.
```

**Journal #147609 — Dev Studio — 2026-10-23 (Dev handoff v7 — không đổi code):**

```
Dev handoff — 23/10 14:00 · nhánh ai_studio_implement_42422

Vòng 7 không đổi code so với vòng 5/6 (commit 188ad8624d). HieuTM đã chốt giữ 403 khi sửa tag với tag_id dạng mảng. Test case NEW-66 cần đổi cách gây lỗi server sang add_tag với tag_name mảng, sau đó đóng #44028.

Việc cần người làm thêm (ngoài phạm vi task):
- Test Studio cập nhật test case NEW-66: với tag_id dạng mảng thì kỳ vọng 403 「このデータを操作する権限がありません。」; phần kiểm 「保存に失敗しました。」 dùng add_tag với tag_name là mảng 2 phần tử (HieuTM chốt 23/10).
- Đóng Redmine #44028 sau khi NEW-66 được cập nhật.
- Test Studio cần cập nhật test case NEW-47: validate-limit với id không tồn tại phải mong đợi 403, không còn là 404.

Branch: ai_studio_implement_42422
- sns-line: ai_studio_implement_42422 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit 188ad8624d314b08be69b2499bd2df0384c18d8a)
```

**Journal #147620 — Dev Studio — 2026-10-23 (v8 — không đổi code, mới nhất):**

```
Dev Studio · Nội dung thực hiện

Bug #3769 bị gửi lại lần thứ năm nhưng không có bằng chứng mới. Lỗi ghi đè chỉ xảy ra trên code cũ, còn code hiện tại chặn đúng bằng 403. Bản v8 không sửa code và giữ phương án A mà HieuTM đã chốt. Tôi đã thử nhắn Test Studio cập nhật test case NEW-66, nhưng bị từ chối vì token của Dev Studio chưa có quyền gửi góp ý. Cần một người cập nhật NEW-66 và NEW-47 rồi đóng Redmine #44028, nếu không vòng sau bug sẽ lại bị gửi.

Ảnh hưởng / rủi ro:
Không đổi code nên không có ảnh hưởng mới. Nếu chưa ai cập nhật test case, vòng sau Test Studio sẽ lại gửi #3769, và có thể cả #3935, #3974.
```

**Journal #147623 — Dev Studio — 2026-10-23 (Dev handoff v8 — mới nhất, authoritative):**

```
Dev handoff — 23/10 14:22 · nhánh ai_studio_implement_42422

Tóm tắt:
Bản này chặn bot A thao tác dữ liệu tag, folder và action của bot B ở màn Tag và API tag của app, đồng thời dọn màn sửa tag cũ. Vòng 8 không đổi code so với vòng 5–7 (commit 188ad8624d). tag_id dạng mảng trả 403 theo quyết định của HieuTM. Cần cập nhật NEW-66/NEW-47 và đóng #44028, nếu không #3769 sẽ tiếp tục bị gửi lại.

Không có commit mới so với lần bàn giao trước (23/10 14:00): nhánh giữ nguyên commit đã bàn giao.

Nội dung thay đổi:
- Màn Tag (web) và API tag của app: thao tác lên tag, folder, action, template của bot khác, hoặc gửi id sai định dạng, sẽ trả 403 kèm message tiếng Nhật.
- Lưu hoặc di chuyển tag vào folder template, folder đã xoá hoặc folder không tồn tại sẽ trả 404 「フォルダが見つかりません。」.
- Lưu tag gặp lỗi server sẽ trả 「保存に失敗しました。」, không lộ SQL. Thiếu is_limit thì mặc định là 0.
- Sửa tag với tag_id không hợp lệ sẽ trả 403 và không ghi đè tag nào.
- Bước kiểm giới hạn trước khi lưu ở màn sửa/copy tag: nếu tag đã xoá, không tồn tại hoặc thuộc bot khác thì trả 403.
- Màn sửa tag cũ /basic/tag/edit chuyển sang màn v2, route update cũ bị bỏ.

Bug QA con:
- #44028 đã sửa (commit sns-line@b4a39f94fa1a): Đã sửa: tag_id dạng mảng không còn ghi đè TA1. App và web trả 403 theo phương án A HieuTM chốt ngày 23/10. NEW-66 cần đổi cách gây lỗi server sang add_tag với tag_name là mảng.

Bug automation Test Studio:
- Bug #3769 đã sửa (commit sns-line@b4a39f94fa1a): Tag không còn bị ghi đè. tag_id dạng mảng trả 403, có logInfo, không có Chatwork (phương án A do HieuTM chốt). Lượt #5095 không có bằng chứng mới. NEW-66 nên dùng add_tag với tag_name là mảng 2 phần tử để kiểm 「保存に失敗しました。」.

File đã sửa (php-web):
  .../Controllers/Api/Mobile/TagMobileController.php | 205 ++++++++++-
  app/Http/Controllers/Basic/TagController.php       | 400 +++++++++++++--------
  resources/views/basic/tag/edit.blade.php           | 244 -------------
  routes/web.php                                     |   2 -
  4 files changed, 445 insertions(+), 406 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Vòng này không đổi code. Harness chạy lại trên HEAD vẫn pass.
- Vòng 8 không đổi code nên không có ảnh hưởng mới.
- Ảnh hưởng của các vòng trước giữ nguyên: màn Tag v2 (danh sách, sửa, copy, folder, sort, CSV) và API tag của app (save-tag, create-multiple, updateTagFolder, getTagDetail).
- Khi merge với nhánh #42421 sẽ conflict ở edit_tag vì message 403 khác nhau. Cần giữ validateLimit của nhánh này.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy:
- Không đổi JS/CSS, không cần xoá cache.
- Khi merge với #42421: giữ validateLimit của nhánh này và thống nhất message 403.

Việc cần người làm thêm (ngoài phạm vi task):
- Cập nhật test case NEW-66 (TC 31958) theo quyết định của HieuTM ngày 23/10: tag_id dạng mảng kỳ vọng 403; phần kiểm 「保存に失敗しました。」 dùng add_tag với tag_name là mảng 2 phần tử. Sau đó đóng Redmine #44028.
- Cập nhật test case NEW-47 (TC 25210): validate-limit với id không tồn tại kỳ vọng 403 thay cho 404 (bug #3974); đóng bug #3935 vì đây là kỳ vọng cũ.
- Cấp scope 'feedback' cho token Test Studio của Dev Studio. Hiện công cụ góp ý bị từ chối nên agent không báo được cho Test Studio rằng test case đã lỗi thời.

Điểm cần test:
- edit_tag (app và web) với tag_id dạng mảng ⇒ 403 「このデータを操作する権限がありません。」, TA1 và TA2 không đổi
- NEW-66: add_tag với tag_name là mảng 2 phần tử ⇒ 200 「保存に失敗しました。」, có log và Chatwork, không lộ SQL
- NEW-47: validate-limit với id không tồn tại ⇒ 403 「このデータを操作する権限がありません。」
- Hồi quy: sửa và copy tag hợp lệ (kể cả cảnh báo limit) phải chạy như trước.

Branch: ai_studio_implement_42422
- sns-line: ai_studio_implement_42422 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit 188ad8624d314b08be69b2499bd2df0384c18d8a)
```
