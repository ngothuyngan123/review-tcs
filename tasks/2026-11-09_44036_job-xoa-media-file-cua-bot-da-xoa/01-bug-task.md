# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44036 — [JOB] Job xóa media file của bot đã xóa` |
| Module / Màn hình | Job nền (java-job / linect-service), không gắn màn hình admin cụ thể — tác động lên dữ liệu media (file hệ thống) của web (module Lme). Category Redmine không set. |

## Mô tả bug (bản dịch tiếng Việt)

⚠️ Đây **không phải ticket bug** — tracker Redmine là "Improve nội bộ". Nội dung Description là **yêu cầu/spec nghiệp vụ** cho 1 job nền mới, không phải báo lỗi + bản dịch sát như sau:

1. Bảng `delete_folder_media_action`
- Các cột:
  + `bot_id`
  + `media_type`
  + `server_ip`
  + `status` (0: chưa chạy, 1: đang trong process, 2: done, 3: error)
  + `delete_time` (thời điểm muốn xóa)

2. Config file
- `DELETE_FOLDER_MODE_DRY_RUN` (default 1) — chỉ log ra, hay có thực hiện xóa thật.
- `DELETE_FOLDER_SERVER_IP` — Job hiện tại server IP là gì, để map với `delete_folder_media_action.server_ip`, dùng để nhận diện xem job có được giao việc không.
- `DELETE_FOLDER_ROOT_PATH` — thư mục tổng.

3. List các thư mục cần xóa
- Xác định thư mục dựa vào bot id, user id: mỗi bot id gắn với 1 user id admin role 0.
- Logic cũ: vẫn còn user id của staff.
- Logic mới đã sửa: user id của admin.
- ⇒ cần check cả user id admin và staff.

**Step 1.** Tìm bot id, admin id, staff id — từ bot id suy ra list admin, staff id:
- Xóa bot rồi có lấy ra được admin id, staff id không? ⇒ xóa cứng không tìm được trong DB, tìm lại trong log.
- `bot_id`: 131305
- `admin_id`: 13320 — user id của admin, tìm trong bảng `user_staff_bots` theo `bot_id` và `role != 0`.
- `staff_id`: list user id của staff, tìm trong bảng `user_staff_bots` theo `bot_id` và `role != 0`.

**Step 2.** List ra các thư mục cần xóa — xóa các thư mục web upload, prefix: `ext-media-step`; `ext-media-bak`:
- `/[prefix]/media/images/{userId}/{botId}/`
- `/[prefix]/media/image-thumbnail/{userId}/{botId}/`
- `/[prefix]/media/video-thumbnail/{userId}/{botId}/`
- `/[prefix]/media/videos/{userId}/{botId}/`
- `/[prefix]/media/voices/{userId}/{botId}/`
- `/[prefix]/media/pdf/{userId}/{botId}/`
- `/[prefix]/media/pdf_chatgpt/{userId}/{botId}/`
- `/[prefix]/media/csv/{userId}/{botId}/`
- `/[prefix]/images/{userId}/{botId}/landing/`
- `/[prefix]/csv/{botId}/`
- `/[prefix]/qr_image/qr_add_friend_bot_{botId}.png`

Thư mục friend media gửi qua chat:
- `/cb-media/line-user/media-step/{botId}`

========================================================

**Phase 2: JOB RECOVER dùng 1 lần, tách làm class riêng**
1. Lấy danh sách các bot đã bị xóa từ bảng `bots` (tìm theo kiểu: id nào không tìm thấy trong bảng bot thì coi như bot bị xóa).
2. Lấy danh sách staff trong bảng `user_access_bot` để lấy ra list `user_id` access vào bot rồi tìm ra các thư mục.
3. Insert bản ghi vào bảng yêu cầu xóa.

> Ghi chú: ticket sau đó mở thêm **Phase 3** (job xóa từng file riêng lẻ, bảng `delete_file_media_action`) qua journal #149690 (note bổ sung của Do Van Tu TuDV ngày 2026-10-29) — xem chi tiết đầy đủ ở file `03-dev-impact.md` vì không nằm trong Description gốc.

## Steps to reproduce

<!-- Không có — ticket không phải bug reproduction, là spec yêu cầu xây job mới. -->

1.
2.
3.

## Expected result

- (không áp dụng — xem yêu cầu nghiệp vụ ở "Mô tả bug" + đánh giá ảnh hưởng ở `03-dev-impact.md`)

## Actual result

- (không áp dụng)

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Redmine ghi `Attachments (0)` — không có file đính kèm.

## Ghi chú thêm của Leader

⚠️ **Đây là ticket "Improve nội bộ" (tạo job nền mới), không phải bug reproduction** — file `01-bug-task.md` không có Section "Tái hiện bug" trong Redmine nên Steps/Expected/Actual để trống. TCs nên tập trung verify đúng spec nghiệp vụ (bảng `delete_folder_media_action` / `delete_file_media_action`, config `DELETE_FOLDER_*`, logic xóa/dry-run/recover/shared-check) theo diễn giải ở `03-dev-impact.md` (tổng hợp từ 12 vòng thiết kế Dev + log journal), **không phải** so sánh behavior cũ/mới.

Ticket đã qua **~12 vòng thiết kế (v1 → v13)** và nhiều bug con phát sinh trong quá trình AI code + AI test (QA con #44783, #44910, #44911, #44912, #45292; bug automation Test Studio #4938, #4989–#4992, #5043, #5139, #5140) — tất cả đã được Dev xác nhận sửa hoặc trả lời "không phải bug" (xem journal nguyên văn bên dưới). Task Studio tương ứng: `task_id=510` (xem `04-tc-list.md`), `round=1`, `handoffs=9`, 59 TC, tất cả đã PASS ở env `local` (chưa test `dev`/`staging`/`prd`).

**Phụ thuộc ngoài phạm vi job (module web, ticket #43088)** — BẮT BUỘC đọc trước khi review coverage:
- Web phải viết migration Laravel tạo bảng `delete_folder_media_action` + `delete_file_media_action` (kèm cột `table_path`) **trước khi** job này được deploy/bật config — thiếu bảng thì job lỗi SQL mỗi vòng quét kèm Chatwork exception.
- Web phải chèn dòng vào `delete_folder_media_action` / `delete_file_media_action` khi flow xóa bot thật chạy (`FlowDeleteBot`) — job #44036 chỉ tiêu thụ bảng do web ghi, không tự biết bot nào bị xóa (trừ job Recover Phase 2, cũng chỉ chèn vào chính bảng này).
- Web phải ghi đúng format `table_path` (danh sách tên bảng cách nhau dấu phẩy, khớp `PATH_SOURCES` phía job) để cơ chế shared-check (không xóa file bot khác còn dùng) hoạt động đúng.
- Đến ngày journal cuối (09/11/2026, #153152/#153172) — migration web **vẫn CHƯA lên** release nào → phần DB/runtime thật **CHƯA được verify** trên bất kỳ env nào ngoài mock/unit test của Dev.

**Yêu cầu vận hành khi deploy** (ảnh hưởng tới môi trường test):
- Server chạy job phải cấu hình locale UTF-8 (`LANG`/`LC_ALL=*.UTF-8` hoặc `-Dsun.jnu.encoding=UTF-8 -Dfile.encoding=UTF-8`) — thiếu thì path tiếng Nhật bị từ chối sai (status 3, file không bị xóa dù đúng phải xóa).
- `DELETE_FOLDER_MODE_DRY_RUN` mặc định = 1 (chỉ log, không xóa thật) — PHẢI giữ dry-run và xem log trước khi set = 0 (xóa thật, không hoàn tác được).
- 3 key cấu hình `DELETE_FOLDER_*` dạng số chỉ nhận chữ số ASCII — viết sai (kể cả số toàn-góc 全角) làm app không khởi động được.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id (ví dụ minh họa trong ticket) | `131305` (đã bị xóa cứng, không còn trong DB) |
| admin_id | `13320` — user id admin, tra trong `user_staff_bots` theo `bot_id` + `role != 0` |
| staff_id | list user id staff, tra trong `user_staff_bots` theo `bot_id` + `role != 0` |
| Bug con tiêu biểu (dữ liệu test) | `#44910` — path `rich_menus.url_image` / `image_richmenu.detail_tab` dạng JSON escape (`\/msg_template\/...`) · `#44913` — bot `8045001`, file tiếng Nhật `音声 ファイル 1.m4a` · `#45292` — bot F đã xóa, bot H còn sống dùng chung `/msg_template/cross.png` ở bảng `landing` |
| Đối chứng | Test Studio task `#510` — 59 TC, tất cả PASS ở env `local` (handoffs=9, round=1) |

## Journal / note từ Redmine (nguyên văn)

> Ticket có **23 journal có notes**, gần hết là Dev Studio tự log thiết kế v1 → v13 + 6 lần "Dev handoff" (bàn giao code cho QA). Chép nguyên văn **các journal có giá trị điều tra/bàn giao** (bỏ qua journal chỉ đổi status/assignee). Đây là nguồn DUY NHẤT thay cho "Đánh giá ảnh hưởng" có cấu trúc 4 mục chuẩn — xem diễn giải/tổng hợp ở `03-dev-impact.md`.

**Journal #147299 — Dev Studio — 2026-10-22:**

```
Dev Studio · Nội dung thực hiện

Đã ghi câu trả lời của Duy NT vào thiết kế v1: team web tự viết migration tạo bảng delete_folder_media_action, nên task này chỉ làm phần job. DDL đề xuất trong tài liệu là danh sách cột mà web cần tạo và entity job sẽ theo. Không còn câu hỏi nào chặn, có thể thực thi luôn. Còn hai điểm đang theo mặc định đã nêu: ý nghĩa giá trị media_type và ai chèn dòng việc.

Hướng sửa:
- D-1 Thêm 3 key config DELETE_FOLDER_* vào ConfigFile
- D-2 Entity và Repository cho delete_folder_media_action
- D-3 DeleteFolderMediaJob: dựng đường dẫn, quét userId, xóa hoặc đếm an toàn
- D-4 DeleteFolderMediaTask: reset khi khởi động, poll/claim, kiểm an toàn, cập nhật status, Chatwork
- D-5 Khởi động task trong AppMain khi đủ SERVER_IP và ROOT_PATH
- D-6 Unit test JUnit 4 cho DeleteFolderMediaJob trên thư mục tạm

Ảnh hưởng / rủi ro:
Chỉ thêm một task nền mới và 3 key config; code cũ chỉ đổi ở AppMain, ConfigFile và ShareDbRepository. Bảng do migration web tạo nên job cần khớp cột với migration đó. Rủi ro chính là xóa nhầm file, được giảm bằng dry-run mặc định, chặn đường dẫn ra ngoài ROOT, kiểm bot còn tồn tại và unit test trên thư mục tạm.
```

**Journal #147569 — Dev Studio — 2026-10-23 (Dev handoff vòng 1):**

```
Dev handoff — 23/10 11:47 · nhánh ai_studio_implement_44036

Tóm tắt:
Giao job mới trong linect-service: dọn thư mục media của bot đã xóa theo bảng delete_folder_media_action. Job chỉ chạy trên server có cấu hình DELETE_FOLDER_SERVER_IP và DELETE_FOLDER_ROOT_PATH, mặc định ở chế độ dry-run (chỉ log). Khi test cần chú ý nhất: dry-run không được mất file và phải log đủ mọi dòng (kể cả khi hơn 50 dòng); chạy thật chỉ xóa đúng thư mục của bot, không đụng bot khác, không đi xuyên symlink. Bảng do web tạo bằng migration; phần DB chưa verify runtime.

Điểm cần test:
- Dry-run với hơn 50 dòng đến hạn (vd 120): trong một vòng có log DRY_RUN đủ 120 id; vòng sau không log lại.
- Dòng có id nhỏ nhưng delete_time ở tương lai được xử lý ở vòng đầu tiên sau khi đến hạn.
- Chạy thật với hơn 50 dòng: xử lý hết trong một vòng, không dòng nào bị xử lý hai lần.
- Thư mục {botId} của images là symlink sang bot khác: landing của bot kia còn nguyên, dòng chuyển status 3.
- Thư mục {userId} là symlink: không xóa ở đích link, dòng chuyển status 3.
- Chèn 50 dòng của bot còn tồn tại: mỗi vòng quét chỉ có một tin Chatwork, kèm số lượng và tối đa 5 mẫu.

Branch: ai_studio_implement_44036
- linect-service: ai_studio_implement_44036 (nhánh gốc release-t09-2026 @be6ef546aedb, commit d947b7cb79fbc899fae7ccdb3014baef01161062)
```

**Journal #149690 — Do Van Tu TuDV — 2026-10-29 (bổ sung yêu cầu Phase 3):**

```
4. tạo bảng delete_file_media_action có các column => bảng lưu các file cụ thể cần xóa
- bot_id
- path_file
- server_ip
- status (0: chưa chạy, 1: trong proccess, 2: done, 3: error)
- delete_time (thời gian muốn xóa)

5. thêm job check bảng delete_file_media_action đến time xóa thì xóa file
```

**Journal #150052 — Dev Studio — 2026-11-02 (bug automation #4938):**

```
Dev Studio · Nội dung thực hiện

Thiết kế v6 sửa bug automation #4938: ở dry-run, một số dòng bị từ chối bị đổi sang status 3, còn dòng symlink hoặc thư mục thì giữ 0 mà không báo Chatwork. Bản sửa chọn hướng theo ticket ("dry-run chỉ log") và đúng mong đợi của testcase: ở dry-run không dòng nào đổi status, còn mọi lý do từ chối đều được log và vào một tin Chatwork, mỗi dòng một lần. Job xóa thư mục cũng lệch giống vậy nên sửa cùng lúc. Chạy thật vẫn giữ nguyên. Có thể thực thi ngay; hướng này đổi so với bàn giao trước nên cần PO xác nhận, và QA cần chạy lại kịch bản dry-run của cả hai job.
```

**Journal #150196 — Dev Studio — 2026-11-03 (Dev handoff vòng 7 — khớp web #43088 + table_path):**

```
Dev handoff — 03/11 09:53 · nhánh ai_studio_implement_44036

Tóm tắt:
Giao toàn bộ #44036 cho java-job: job xóa thư mục media của bot đã xóa, recover chạy một lần và job xóa từng file. Job đã khớp dữ liệu web #43088 ghi (media_type là nơi lưu, path tính từ public) và không xóa file bot khác còn dùng (cột mới table_path). Dry-run là mặc định và không đổi status (bug #44783). Khi test cần chú ý nhất hai điểm: file dùng chung với bot còn sống phải còn nguyên; mọi dòng bị từ chối khi chạy thật ra status 3 mà không xóa gì. Phần DB chưa verify runtime.

Bug QA con:
- #44783 đã sửa (commit linect-service@6a4f8e059fee): Dry-run của cả job xóa file và job xóa thư mục không còn ghi status: mọi dòng bị từ chối (lỗi kiểm hợp lệ, bot còn, symlink, thư mục) giữ 0 và cùng vào một tin Chatwork ghi 'DRY_RUN, status unchanged'; chạy thật vẫn status 3. Vòng 7 giữ nguyên quy tắc này với luật path mới.

Bug automation Test Studio:
- Bug #4938 đã sửa (commit linect-service@6a4f8e059fee): Dry-run xử lý mọi dòng bị từ chối giống nhau: giữ status 0, có trong tin Chatwork gom ('DRY_RUN, status unchanged'); chạy thật status 3.

Migration / thay đổi dữ liệu:
- [Schema · Trước deploy] Tạo bảng delete_folder_media_action, delete_file_media_action và cột table_path (migration web #43088) (module web): php artisan migrate --force (migration của nhánh web #43088, đã thêm cột table_path varchar)
- [Config · Khi deploy] Cấu hình job xóa media: DELETE_FOLDER_SERVER_IP, DELETE_FOLDER_ROOT_PATH (= public của web trên server), DELETE_FOLDER_MODE_DRY_RUN=1 (module job)
- [Config · Sau deploy] Key mới DELETE_FOLDER_RECOVER_MEDIA_TYPE (1,2,4,5) đi cùng DELETE_FOLDER_RECOVER_MODE khi chạy recover (module job)

Việc cần người làm thêm (ngoài phạm vi task):
- Web #43088: thêm migration cột table_path vào delete_file_media_action và ghi danh sách bảng chứa path (cách nhau dấu phẩy, đúng tên trong PATH_SOURCES) khi gom path; báo job khi thêm/bớt bảng trong PATH_SOURCES.
- Web #43088: đổi index delete_folder/file_media_action từ (status, delete_time) sang (server_ip, status, delete_time) để câu poll mỗi phút không đọc dòng B2 kẹt status 0.
- Vận hành: deploy migration web trước job; giữ DELETE_FOLDER_MODE_DRY_RUN=1 tới khi xem log dry-run (DRY_RUN, DRY_RUN:SHARED, NOT_FOUND) trên từng server.
- Xóa file trên B2 (server_ip NULL) không thuộc ticket job này.

Điểm cần test:
- Dòng file /img_rich_menu/richmenu_415_233_a.jpg bot 415, table_path=rich_menus, bot 425 còn trong bots có cùng url_image ⇒ chạy thật: file còn, status 2, log SHARED usedByBotId=425
- Path chỉ còn trong image_richmenu.detail_tab (JSON) của bot khác, table_path=image_richmenu ⇒ không xóa
- Bot khác dùng path nhưng đã xóa cứng khỏi bots ⇒ file được xóa
- Bot khác dùng path đang is_deleted=1 ⇒ không xóa
- table_path trống ⇒ kiểm cả 30 bảng; table_path=abc ⇒ chạy thật status 3 + Chatwork, dry-run giữ 0
- Lỗi query khi kiểm dùng chung ⇒ file giữ nguyên, status 3, có Chatwork
- Dry-run: dòng dùng chung log DRY_RUN:SHARED, status giữ 0, không Chatwork
- Năm dòng thư mục web ghi cho một bot: server IP khớp xóa đủ thư mục; dòng B2 không ai nhận; media_type 4/5 không còn status 3

Branch: ai_studio_implement_44036
- linect-service: ai_studio_implement_44036 (nhánh gốc release-t09-2026 @be6ef546aedb, commit 382e2feeafd4a2a4dd4f56925cdbfb968649a831)
```

**Journal #151191 — Dev Studio — 2026-11-04 (Dev handoff vòng 9 — sửa 4 bug QA #44910–#44913):**

```
Dev handoff — 04/11 16:20 · nhánh ai_studio_implement_44036

Tóm tắt:
Giao toàn bộ #44036 cho java-job (HEAD aa3f46377, vòng 9 không đổi code). Bản này sửa cả 4 bug QA #44910–#44913, vì QA đã test trên bản cũ 382e2fee: job xóa file chỉ xóa trong thư mục upload của web; nhận ra file dùng chung dù path ghi dạng nào, kể cả JSON \/; tên file tiếng Nhật không còn lỗi collation. Khi test, chú ý nhất là file của bot còn sống và file giao diện web phải còn nguyên; job phải chạy locale UTF-8.

Bug QA con:
- #44783 đã sửa (commit linect-service@6a4f8e059fee): Dry-run của cả hai job không còn ghi status: mọi dòng bị từ chối giữ 0 và cùng vào một tin Chatwork 'DRY_RUN, status unchanged'; chạy thật vẫn status 3.
- #44910 đã sửa (commit linect-service@aa3f463776e4): Kiểm dùng chung thêm dạng JSON của path ('\/' và \uXXXX như json_encode của web). detail_tab chứa '\/msg_template\/…' của bot sống được nhận là SHARED, file còn. QA đã test trên 382e2fee, trước bản sửa.
- #44911 đã sửa (commit linect-service@aa3f463776e4): Kiểm dùng chung so theo path tương đối đã chuẩn hóa (bỏ '/' đầu và ROOT). Mọi tổ hợp path_file × dạng lưu nguồn đều SHARED, file còn; path_file là URL thì bị từ chối (status 3, file còn).
- #44912 đã sửa (commit linect-service@aa3f463776e4): Job xóa file chỉ nhận thư mục upload của web; js/css/fonts/plugins/tinymce/images giao diện bị từ chối 'top folder not allowed', file còn, chạy thật status 3.
- #44913 đã sửa (commit linect-service@aa3f463776e4): Mỗi cột được so bằng CONVERT(... USING utf8mb4), nên cột latin1 của form_answer không còn lỗi collation; file tên tiếng Nhật được xóa, status 2. Job cần chạy locale UTF-8 (đã có deploy note).

Bug automation Test Studio:
- Bug #4989 đã sửa: Chỉ nhận thư mục upload của web; js/css/fonts/plugins/tinymce/images giao diện, img_rich_menu/type_* bị từ chối (chạy thật status 3, dry-run giữ 0), file còn.
- Bug #4990 đã sửa: SQL kiểm dùng chung dùng CONVERT(cột USING utf8mb4), nên không lỗi collation với cột latin1; path tiếng Nhật được xóa, status 2 (JVM phải chạy locale UTF-8).
- Bug #4991 đã sửa: Thêm dạng JSON '\/' và \uXXXX vào điều kiện kiểm dùng chung, nên detail_tab của bot sống được nhận là SHARED, file còn.
- Bug #4992 đã sửa: So theo path tương đối chuẩn hóa (không '/' đầu, bỏ ROOT), nên mọi tổ hợp path_file × dạng lưu nguồn đều SHARED, file còn.

Việc cần người làm thêm (ngoài phạm vi task):
- Cấu hình server chạy job với locale UTF-8 (LANG/LC_ALL=*.UTF-8); repo java-job không có script khởi động nên không sửa được trong code.
- Web #43088 deploy migration hai bảng và cột table_path trước job; giữ DELETE_FOLDER_MODE_DRY_RUN=1 tới khi đã xem log dry-run.
- QA cần test lại #44910–#44913 trên bản aa3f46377. Cả 4 issue hiện ghi kết quả test trên bản cũ 382e2feea.

Điểm cần test:
- #44912: các path /js/…, /css/…, /fonts/…, /plugins/…, /tinymce/… và /images/t44036_*.png (không theo mẫu thư mục bot) của bot đã xóa ⇒ file còn; chạy thật: status 3 và có trong tin gom 'top folder not allowed'.
- #44911: rich_menus.url_image = msg_template/x.png của bot còn sống; path_file /msg_template/x.png và <ROOT>/msg_template/x.png ⇒ log SHARED, file còn, status 2 (đủ 12 tổ hợp).
- #44910: detail_tab của bot còn sống chứa \/msg_template\/t44036_j2.png ⇒ log SHARED table=image_richmenu, file còn, status 2.
- #44913: file 音声 ファイル 1.m4a của bot đã xóa 8045001, table_path NULL, DRY_RUN=0 ⇒ file bị xóa, status 2, không có tin Chatwork (process job chạy locale UTF-8).
- Hồi quy: dry-run với các dòng bị từ chối thì status giữ 0 (#44783); path upload của đúng bot vẫn xóa được.

Branch: ai_studio_implement_44036
- linect-service: ai_studio_implement_44036 (nhánh gốc release-t09-2026 @be6ef546aedb, commit aa3f463776e4f3e613d97c15935e73e10e6b6697)
```

**Journal #151279 — Dev Studio — 2026-11-05 (bug automation #5043 — không phải lỗi):**

```
Dev Studio · Nội dung thực hiện

Bug automation #5043 không phải lỗi sản phẩm. Testcase dùng file /img_rich_menu/t44036_*.png, nhưng web chỉ ghi ảnh rich menu tên richmenu_{bot}_{rich menu}_*.jpg; 103 path thật trong DB đều theo dạng này. Vì vậy job từ chối dòng đó là đúng thiết kế v8. Bản v10 không sửa code: chỉ chạy lại test có sẵn và ghi trả lời "không phải bug", kèm dữ liệu testcase đúng. Phần còn lại là người phụ trách Test Studio cập nhật dữ liệu cho 3 testcase liên quan.
```

**Journal #152262 / #152283 — Dev Studio — 2026-11-06 (bug #45292 — shared-check thiếu bảng):**

```
Dev Studio · Nội dung thực hiện

Bug #45292 đúng là lỗi của code nhánh này. Job xóa từng file chỉ kiểm các bảng ghi trong table_path, mà web ghi vào đó các bảng của bot bị xóa. Vì vậy khi bot khác còn dùng cùng file ở bảng khác (ví dụ landing), file vẫn bị xóa. Em đã mở lại task và viết thiết kế v12: luôn kiểm đủ 30 bảng, bảng trong table_path được kiểm trước, kèm test tái hiện bug. Đổi lại, mỗi file chưa dùng chung tốn 30 lần quét bảng thay vì 1–3, cần xem thời gian chạy khi dry-run trước khi bật chạy thật.

---

Dev handoff — 06/11 17:30 · nhánh ai_studio_implement_44036 (HEAD db7a3373e)

Nội dung thay đổi:
- Job xóa từng file: luôn kiểm file dùng chung ở đủ 30 bảng nguồn, các bảng ghi trong table_path được kiểm trước. Có bot khác dùng ở bảng bất kỳ ⇒ SHARED, file còn (chạy thật status 2, dry-run giữ 0). Tên bảng lạ vẫn làm dòng không hợp lệ.

Đánh giá ảnh hưởng — Rủi ro trung bình: Xóa file không hoàn tác được, phần DB chưa chạy runtime, và chi phí 30 lần quét bảng trên production chưa đo. Thay đổi của vòng này chỉ làm job giữ file nhiều hơn; dry-run là mặc định và lỗi query không dẫn tới xóa.
- DB chính: mỗi file có trên đĩa mà chưa ai dùng chung ⇒ 30 câu SELECT quét bảng trên mỗi server (trước đây 1–3 câu khi table_path có giá trị). Các bảng form_answer* trên production có thể lớn.

Việc cần người làm thêm (ngoài phạm vi task):
- Khi deploy, xem log elapsedMs của DeleteFileMediaTask ở chế độ dry-run trên production trước khi đặt DELETE_FOLDER_MODE_DRY_RUN=0.
- QA test lại bug #45292 (issue con của web #43088) trên bản mới; các issue con #44783, #44910, #44911, #44912 vẫn chờ QA đóng.

Điểm cần test:
- #45292: bot F đã xóa, bot H còn sống dùng /msg_template/cross.png ở bảng landing; dòng xóa có table_path=rich_menus, chạy thật ⇒ log SHARED table=landing usedByBotId=H, file còn, status 2, không có tin Chatwork.
- Cùng dữ liệu ở dry-run ⇒ log DRY_RUN:SHARED, status giữ 0.
- Không bot nào dùng path ở 30 bảng ⇒ file bị xóa, status 2.
- table_path có tên bảng lạ ⇒ dòng không hợp lệ như cũ (chạy thật status 3 + tin gom, dry-run giữ 0).
```

**Journal #153152 / #153172 — Dev Studio — 2026-11-09 (bàn giao cuối cùng, HEAD `db7a3373e` — bug automation #5139/#5140 là lỗi kịch bản, không phải code):**

```
Dev Studio · Nội dung thực hiện

Hai bug automation #5139 và #5140 đều không phải lỗi sản phẩm. Với #5139, kịch bản chèn nhiều dòng trùng cặp bot và loại lưu trữ, nên vi phạm khóa duy nhất mà migration web tạo; lỗi xảy ra ngay ở bước chuẩn bị, trước khi job chạy. Với #5140, job đã chuyển dòng sang status 2 và cập nhật updated_at, nhưng kịch bản so chuỗi với 'null' nên đánh sai. Bản v13 không sửa code: chỉ chạy lại test và ghi trả lời kèm dữ liệu kịch bản đúng.

---

Dev handoff — 09/11 10:16 · nhánh ai_studio_implement_44036

Tóm tắt:
Giao toàn bộ #44036 cho java-job, HEAD db7a3373e; code không đổi so với vòng 12. Vòng này trả lời bug automation #5139 và #5140: cả hai là lỗi kịch bản test, không phải lỗi job. Khi chấm lại: mỗi dòng chèn vào delete_folder_media_action phải có cặp (bot_id, media_type) riêng và delete_time ở quá khứ; chấm bằng updated_at IS NOT NULL thay vì so chuỗi.

Nội dung thay đổi:
- Không có thay đổi code mới ở vòng này (HEAD db7a3373e như vòng 12).
- Giữ nguyên: job xóa thư mục media của bot đã xóa (web upload + cb-media); job recover chèn lệnh cho bot đã xóa còn thư mục.
- Giữ nguyên: job xóa từng file chỉ xóa trong thư mục upload của web và kiểm dùng chung ở đủ 30 bảng (bảng trong table_path kiểm trước).
- Giữ nguyên: dry-run không đổi status; ba key số DELETE_FOLDER_* chỉ nhận chữ số ASCII.

Đánh giá ảnh hưởng — Rủi ro trung bình: Code không đổi so với vòng 12. Nhưng xóa file không hoàn tác được, phần DB chưa chạy runtime và chi phí 30 lần quét bảng trên production chưa đo; dry-run là mặc định.
- DB chính: như vòng 12, tối đa 30 câu SELECT quét bảng cho mỗi file có trên đĩa mà chưa ai dùng chung; log có thêm dòng SHARED_CHECK.
- Phối hợp web #43088 (#45317): lệnh của bot còn trong bots có delete_time 9999 và job không xử lý tới khi web kích hoạt sau khi xóa bot. Cần test luồng xóa bot đầy đủ trên web.

Migration / thay đổi dữ liệu:
- [Schema · Trước deploy] Tạo bảng delete_folder_media_action, delete_file_media_action và cột table_path (migration web #43088) (module web) — database/migrations/2026_10_14_100000_create_delete_folder_media_action_table.php: php artisan migrate --force
- [Config · Khi deploy] Thêm DELETE_FOLDER_SERVER_IP, DELETE_FOLDER_ROOT_PATH, DELETE_FOLDER_MODE_DRY_RUN=1 vào config java-job
- [Hạ tầng · Khi deploy] Process java-job chạy với locale UTF-8
- [Config · Sau deploy] Bật recover một lần: DELETE_FOLDER_RECOVER_MODE và DELETE_FOLDER_RECOVER_MEDIA_TYPE

Lưu ý khi deploy:
- Migration web #43088 (hai bảng + cột table_path) phải lên trước job.
- Giữ DELETE_FOLDER_MODE_DRY_RUN=1 tới khi đã xem log dry-run, gồm elapsedMs.
- Process java-job phải chạy với locale UTF-8 (path tiếng Nhật).
- Ba key số DELETE_FOLDER_* viết bằng chữ số ASCII.

Việc cần người làm thêm (ngoài phạm vi task):
- Người phụ trách Test Studio sửa 4 kịch bản NEW-3, NEW-16, NEW-17, NEW-22: mỗi dòng delete_folder_media_action phải có cặp (bot_id, media_type) khác nhau, và xóa dòng cũ cùng cặp trước khi chèn. Sau đó Reject bug #5139.
- Người phụ trách Test Studio sửa kịch bản NEW-12: kiểm status = 2 và updated_at IS NOT NULL thay cho so chuỗi với 'null'. Sau đó Reject bug #5140.

Điểm cần test:
- #5139: chèn dữ liệu không trùng (bot_id, media_type), ví dụ bot_id=0 và -1 mỗi giá trị một dòng, 50 dòng lỗi dùng 50 bot khác nhau. Chạy thật: bot không hợp lệ, ROOT không có hoặc bot còn trong bots ⇒ status 3, không xóa gì.
- #5139: dry-run khác 0 ⇒ chỉ log; 50 dòng lỗi trong một vòng quét ⇒ đúng 1 tin Chatwork (số lượng và tối đa 5 mẫu).
- #5140: chạy thật media_type 1 ⇒ thư mục của bot 8041201 trên 2 prefix và cb-media bị xóa, file khác còn; dòng status 2 và updated_at IS NOT NULL (không so chuỗi với 'null').
- Dòng có delete_time 9999-12-31 (lệnh web đang chờ) không được job xử lý.
- Hồi quy: #45292 kiểm đủ 30 bảng; #44783 dry-run không đổi status; #44910/#44911/#44912; khi dry-run xem elapsedMs.

Branch: ai_studio_implement_44036
- linect-service: ai_studio_implement_44036 (nhánh gốc release-t09-2026 @be6ef546aedb, commit db7a3373e6a226c68da3c9f95821161d80653a15)
```

> 11 journal còn lại (không chép lại ở đây để tránh trùng lặp — tất cả cùng dạng Dev Studio tự log thiết kế v2–v9/v11 trung gian hoặc Dev handoff lặp lại nội dung đã chốt ở bản mới nhất phía trên) có cùng nội dung lõi, chỉ khác số vòng/commit. Xem đầy đủ raw trong `scripts/redmine_fetch.py 44036` nếu cần tra lại chi tiết 1 vòng cụ thể.
