# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42765 — Auto reply – Folder, id liên kết & sort` |
| Module / Màn hình | 自動応答 (Auto reply) — `Basic\ReplyController` (web — thư mục, sắp xếp, form cũ, lưu V2) + `Api\Mobile\AutoreplyMobileController` (API mobile/MCP — thư mục) |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Ticket này có nguồn gốc là **security audit IDOR** (Template / Broadcast / Scenario), không phải bug khách hàng báo qua reproduce steps thông thường — cùng nguồn audit với ticket liên quan [#42764](../2026-10-24_42764_auto-reply-route-public-detail/01-bug-task.md). Mô tả dưới đây là nguyên văn nội dung audit (dịch sát), không phải "Steps to reproduce / Expected / Actual" kiểu cổ điển.

Controller: `Basic\ReplyController`
Nguồn: security audit IDOR (Template / Broadcast / Scenario)

**1. IDOR-MSG-19 (3/4) [High] — Auto reply · Folder theo id không bot_id/kind**
- Vị trí: `ReplyController.php:471-476, 542`
- Route: `/ajax/get-list-group` — LOGIN (middleware: LOGIN)
- Vấn đề / Fix: `category->where('id')->update(...)` → thêm điều kiện `bot_id` + `kind`, `isCategoryOfOtherBot(folder_move_id)`

**2. IDOR-MSG-20 (7/9) [Normal] — Auto reply · Id liên kết bot khác lưu vào cấu hình**
- Vị trí: `ReplyController.php:127-170, 304-348`
- Route: các route lưu — LOGIN/BASIC (middleware: LOGIN BASIC)
- Vấn đề / Fix: id scenario/tag/action/template/profile/folder → kiểm theo bot trước khi lưu

**3. IDOR-MSG-22 (4/10) [Low] — Auto reply · Sort position chéo bot**
- Vị trí: `ReplyController.php:647, 699`
- Route: — (middleware: —)
- Vấn đề / Fix: `whereIn('id')->update(['position'])` → thêm `bot_id`

## Steps to reproduce

<!-- Không có — ticket gốc là audit tìm lỗ hổng qua đọc code, không phải case tái hiện cụ thể do khách hàng báo. -->

## Expected result

- Mọi thao tác bình thường với dữ liệu của **chính bot đang đăng nhập** (thư mục: thêm/sửa/đổi tên/xoá/chuyển, sắp xếp item/folder, form cũ, lưu V2) vẫn chạy **như cũ**.
- Form cũ: chọn mặc định `変更しない` (scenario_id = -1) và `購読停止・予約キャンセル` (0) vẫn lưu được; sửa bản ghi cũ giữ nguyên giá trị cũ vẫn lưu được.
- Id (folder/scenario/tag/action/template/profile/filter v2/item sort) **thuộc bot khác** → bị chặn, trả `403 — 「この権限は許可されていません。」`, không ghi gì.
- Id **không tồn tại hoặc sai định dạng** → trả `404 — 「データが見つかりません。」`.
- Chuyển auto reply vào `未分類` hoặc folder của chính mình → OK (cả web và API MCP/mobile).
- API MCP/mobile: gửi `group_id` của bot khác → danh sách trả về như `未分類`, không lộ auto reply của bot khác; xoá folder → danh sách mở về `未分類`.

## Actual result

- **Thư mục** (`/ajax/get-list-group`): sửa/đổi tên/xoá/chuyển bằng id của bot khác vẫn thực hiện được — `category->where('id')->update()` không kiểm `bot_id`/`kind` (IDOR-MSG-19).
- **Id liên kết** (scenario/tag/action/template/profile/folder) của bot khác vẫn lưu được vào cấu hình auto reply — không kiểm theo bot trước khi lưu (IDOR-MSG-20).
- **Sắp xếp (sort position)** chéo bot — `whereIn('id')->update(['position'])` cập nhật cả bản ghi của bot khác (IDOR-MSG-22).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #42765 không có attachment (Attachments (0)). -->

## Ghi chú thêm của Leader

- Ticket cùng nguồn **security audit IDOR** với [#42764](../2026-10-24_42764_auto-reply-route-public-detail/01-bug-task.md) (đọc/ghi detail auto reply) — #42764 fix phần route PUBLIC + lưu/xoá/move/toggle theo id; #42765 (ticket này) fix phần **thư mục, id liên kết form cũ, và sort**.
- **PHẢI phát hành cùng #42764** — 2 ticket sửa chung **2 controller** (`ReplyController.php`, `AutoreplyMobileController.php`), journal #146834 của #42764 xác nhận còn conflict merge chưa giải. Sau khi merge, Dev yêu cầu chạy lại **3 bộ test**: `ReplyFolderGuardTest` (của ticket này), `ReplyOwnershipGuardTest` + `AutoreplyMobileOwnershipGuardTest` (của #42764).
- ⚠️ **Điểm cần Leader lưu ý khi đối chiếu 2 ticket**: journal #146834 của #42764 ghi "Cho người làm #42765: API mobile còn IDOR thư mục ở `updateAutoreplyFolder`, `buildListCategoryResponse` (group_id), `folder_move_id` của `moveAutoreply`; **nên dùng lại trait `AutoReplyOwnershipGuardTrait`**" (trait Dev #42764 đã tạo). Nhưng ticket này (#42765) lại tạo **trait riêng** `AutoReplyFolderGuardTrait` (file mới, 174 dòng) — KHÔNG thấy xác nhận có tái dùng `AutoReplyOwnershipGuardTrait` của #42764 hay không. Nên hỏi lại Dev để chắc 2 trait không có logic xung đột/trùng lặp khi merge.
- Đi qua **2 vòng thiết kế**: v1 (journal #143086) fix IDOR-MSG-19/20/22; v2 (journal #143128) sửa lại vì v1 chặn nhầm giá trị mặc định `変更しない` (-1) và giá trị cũ `-1000` có trong dữ liệu cũ của trường scenario (`step_to_id`) ở form cũ — số âm được cho đi qua trước khi kiểm theo bot vì số âm không trỏ tới kịch bản của bot nào.
- Dev tự đánh giá: **"Rủi ro trung bình"**. Có **82 test** kèm kiểm chứng ngược trên code cũ, nhưng **CHƯA chạy thử trên app thật** (nguyên văn Dev, journal #143139) và còn phải merge cùng #42764.
- Không đổi schema DB / FE / job nền ở cả 2 vòng (Dev xác nhận đã kiểm diff).
- Branch: `ai_studio_implement_42765` (nhánh gốc `release_step_20260930_v2` @`0637cd04f7c1`, commit `2e4c0f786b4ff9c7695c3f39b608c80eff352933`). Journal không ghi rõ đã lên staging/release nào — tra lại trên Redmine/CI nếu cần biết trạng thái deploy cụ thể trước khi test.

## Journal / note từ Redmine (nguyên văn)

**Journal #143086 — Dev Studio — 2026-10-12:**
```
Dev Studio · Nội dung thực hiện (v1)

Thiết kế v1 đã xong, có thể thực thi. Màn 自動応答 sẽ chặn thao tác bằng id của bot khác ở: thư mục (thêm/sửa, đổi tên, xoá, chuyển vào), sắp xếp, và id liên kết của form lưu cũ. Theo bàn giao của #42764, thiết kế gồm cả phần thư mục của API dùng cho MCP/mobile, và chặn việc chiếm filter của bot khác khi lưu. Không đổi schema, FE hay job. Rủi ro chính là xung đột merge với #42764 (cùng hai controller, chưa merge); thiết kế đã đặt thay đổi tránh các đoạn #42764 sửa.

Hướng sửa:
- D-1 Thêm trait AutoReplyFolderGuardTrait dùng chung cho web và API mobile
- D-2 Thư mục trên web: addAndEditGroup, renameGroup, deleteGroup ràng theo bot + kind
- D-3 moveItem kiểm folder_move_id trước khi ghi
- D-4 sortItem/sortFolder chỉ cập nhật position bản ghi của bot
- D-5 Form cũ store/save kiểm id liên kết theo bot trước khi ghi
- D-6 Lưu V2 (web và MCP) chặn id filter v2 của bot khác
- D-7 API mobile: thư mục, chuyển thư mục, danh sách theo group_id
- D-8 Kiểm tra: php -l và test PHPUnit không chạm DB thật

Ảnh hưởng / rủi ro:
Ảnh hưởng màn 自動応答 trên web (thư mục, chuyển, sắp xếp, lưu V2, form cũ) và công cụ auto reply của MCP qua API mobile; không đổi schema, FE hay job. Cần test hồi quy các luồng bình thường với id của chính bot, và chạy lại test của cả #42764 sau khi merge vì hai ticket sửa chung hai controller.
```

**Journal #143128 — Dev Studio — 2026-10-12:**
```
Dev Studio · Nội dung thực hiện (v2)

Thiết kế v2 sửa đúng mục review yêu cầu: form tạo/sửa auto reply kiểu cũ đang chặn nhầm lựa chọn mặc định 「変更しない」 (-1) và giá trị -1000 có trong dữ liệu cũ, nên không lưu được. Bản sửa cho số âm của ô kịch bản đi qua trước khi kiểm theo bot, vì số âm không trỏ tới kịch bản của bot nào. Id kịch bản của bot khác vẫn bị chặn. Đã kiểm DB: chỉ ô kịch bản có giá trị âm, các trường khác không có. Còn lại là thêm test cho các ca này rồi chạy lại toàn bộ test.

Hướng sửa:
- D-9 Form cũ: cho số nguyên âm của step_to_id đi qua trước khi kiểm theo bot
- D-10 Thêm test sentinel vào ReplyFolderGuardTest và chạy lại

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng hai route lưu của form cũ (/basic/reply/store và /basic/reply/save). Thay đổi chỉ nới một trường cho giá trị âm, nên id kịch bản của bot khác vẫn bị chặn. Không đổi luồng V2, API mobile, schema hay FE.
```

**Journal #143139 — Dev Studio — 2026-10-12:**
```
Dev handoff — v2 · nhánh ai_studio_implement_42765

Tóm tắt:
Ticket này chặn truy cập dữ liệu của bot khác (IDOR) ở màn 自動応答 và API auto reply của MCP. Các thao tác được chặn: sửa/đổi tên/xoá/chuyển thư mục, sắp xếp, các id liên kết của form cũ và id filter v2 khi lưu V2. Khi id thuộc bot khác thì trả 403 「この権限は許可されていません。」; khi không tồn tại hoặc sai định dạng thì trả 「データが見つかりません。」. Điều cần chú ý nhất khi test: các thao tác bình thường với dữ liệu của chính bot (folder, chuyển, sắp xếp, lưu V2, form cũ với 変更しない) vẫn phải chạy như cũ. Phải phát hành cùng #42764.

Nội dung thay đổi:
- Màn 自動応答 – thư mục: sửa/đổi tên/xoá chỉ áp dụng cho folder auto reply của bot đang đăng nhập. Folder của bot khác ⇒ 403; id sai định dạng ⇒ 400
- Màn 自動応答 – chuyển thư mục: folder đích của bot khác ⇒ 403; folder đã xoá hoặc không tồn tại ⇒ 404; chuyển vào 未分類 và folder của mình giữ như cũ
- Màn 自動応答 – sắp xếp item và folder: chỉ cập nhật thứ tự của bản ghi thuộc bot; id lạ bị bỏ qua
- Form tạo/sửa cũ: folder, kịch bản, mẫu tin, tag thêm/gỡ, filter tag/kịch bản/conversion phải thuộc bot. 変更しない (-1) và 購読停止 (0) vẫn lưu được; sửa bản ghi cũ mà giữ nguyên giá trị vẫn lưu được
- Lưu auto reply V2 trên web và qua API MCP: gửi id filter v2 của auto reply bot khác ⇒ 403, không ghi đè filter của bot khác
- API MCP auto reply: cập nhật/xoá folder và chuyển auto reply chặn folder của bot khác như trên web. Danh sách trả về với group_id không phải folder của bot ⇒ mở 未分類

File đã sửa (php-web):
  .../Api/Mobile/AutoreplyMobileController.php       |  44 ++
  app/Http/Controllers/Basic/ReplyController.php     | 113 ++++-
  app/Traits/AutoReplyFolderGuardTrait.php           | 174 +++++++
  tests/Feature/FakeReplyFolderConnection.php        | 254 ++++++++++
  tests/Feature/ReplyFolderGuardTest.php             | 536 +++++++++++++++++++++
  5 files changed, 1118 insertions(+), 3 deletions(-)

Đánh giá ảnh hưởng — Rủi ro trung bình: Guard mới chạy trên mọi thao tác ghi của màn 自動応答 và API auto reply của MCP; nếu guard sai sẽ chặn nhầm người dùng hợp lệ. Đã có 82 test kèm kiểm chứng ngược trên code cũ, nhưng chưa chạy thử trên app thật và còn phải merge cùng #42764 trên cùng 2 controller.
- Endpoint /ajax/get-list-group của màn 自動応答: mọi action dùng chung endpoint này (addAndEditGroup, renameGroup, deleteGroup, moveItem, sortItem, sortFolder, searchByKeyWord, showGroup). Bộ lọc group_id ở đầu hàm và guard mới chạy trước khi ghi
- Endpoint /ajax/save-data-detail-auto-reply (tạo/sửa/sao chép auto reply V2): guard filter v2 chạy trước khi ghi. Filter mới (id rỗng) và filter của chính bot phải lưu bình thường
- API MCP auto reply: save, move, update/delete/create folder, delete, toggle. Các endpoint này dùng chung hàm dựng danh sách nên giờ ép group_id không hợp lệ về 未分類
- Bảng category (kind=reply), auto_reply (position, category_id), filters_v2 (parent_type=auto_reply), filters v1: chỉ thêm điều kiện bot/kind vào câu ghi, không đổi cấu trúc
- Form cũ /basic/reply/store và /basic/reply/save: thêm bước kiểm id liên kết trước khi ghi
- Nhánh #42764 sửa cùng 2 controller: merge sẽ có conflict, giải bằng cách giữ code của cả hai bên

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy:
- Phát hành cùng #42764: hai ticket sửa cùng ReplyController và AutoreplyMobileController, phải có cả hai thì mới chặn đủ IDOR của màn này. Khi merge, giải conflict bằng cách giữ code của cả hai bên, rồi chạy lại 3 bộ test ReplyFolderGuardTest, ReplyOwnershipGuardTest, AutoreplyMobileOwnershipGuardTest
- Có file mới app/Traits/AutoReplyFolderGuardTrait.php (autoload PSR-4); deploy đủ file
- Không đổi JS/CSS/Blade nên không cần hard-reload

Việc cần người làm thêm (ngoài phạm vi task):
- Khi phát hành cùng #42764 vẫn cần giải conflict theo kiểu giữ code cả hai bên như đã ghi ở vòng 1 (dòng use trait/hằng, khối guard đầu save(), vị trí helper private). Sau khi merge, chạy lại cả ba bộ test: ReplyFolderGuardTest, ReplyOwnershipGuardTest và AutoreplyMobileOwnershipGuardTest.
- Các test lỗi sẵn có trên base, không liên quan ticket này: ContractExpireServiceTest, BillingServiceTest, ChatMediaSizeValidationTest, ExampleTest.
- Phát hành #42765 cùng #42764. Khi merge, giữ code của cả hai bên và chạy lại 3 bộ test của hai ticket

Điểm cần test:
- Form tạo auto reply kiểu cũ: để mặc định 「変更しない」 rồi lưu thì thành công, scenario_id = -1
- Form sửa kiểu cũ: đổi 「ステップ変更・停止」 sang 「変更しない」 hoặc 「購読停止・予約キャンセル」 thì lưu được; chọn kịch bản của chính bot thì lưu được
- Gửi tay id kịch bản của bot khác vào form cũ: quay lại kèm 「この権限は許可されていません。」 và không ghi gì
- Hồi quy các trường khác của form cũ (folder, mẫu tin, tag, filter) theo tiêu chí của v1
- Form cũ /basic/reply/edit/{id}: chọn ステップ変更・停止 = 変更しない, 購読停止・予約キャンセル hoặc một kịch bản của bot ⇒ lưu được. Sửa request gửi id kịch bản của bot khác ⇒ quay lại kèm 「この権限は許可されていません。」 và không ghi gì
- Màn 自動応答: sửa/đổi tên/xoá folder bằng id folder của bot khác ⇒ alert 「この権限は許可されていません。」, folder bot khác không đổi. Folder của mình tạo/sửa/xoá bình thường
- Chuyển auto reply vào folder của bot khác ⇒ 403. Vào folder đã xoá hoặc không tồn tại ⇒ 「データが見つかりません。」. Vào 未分類 hoặc folder của mình ⇒ OK (cả web và API MCP)
- Sắp xếp item/folder có lẫn id của bot khác ⇒ position của bot khác không đổi; sắp xếp bình thường vẫn giữ đúng thứ tự
- Lưu V2 (web, MCP) kèm id filter v2 của auto reply bot khác ⇒ 403, filter bot khác không đổi. Tạo mới, sửa filter của mình hoặc sao chép auto reply ⇒ OK
- API MCP: gửi group_id của bot khác ⇒ danh sách như 未分類, không lộ auto reply của bot khác. Xoá folder ⇒ danh sách mở 未分類

Branch: ai_studio_implement_42765 (nhánh gốc release_step_20260930_v2 @0637cd04f7c1, commit 2e4c0f786b4ff9c7695c3f39b608c80eff352933)
```
