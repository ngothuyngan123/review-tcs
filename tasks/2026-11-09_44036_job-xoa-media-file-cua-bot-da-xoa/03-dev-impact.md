# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Redmine #44036 **không có section "Đánh giá ảnh hưởng" theo format chuẩn 4 mục** (ticket là "Improve nội bộ" — xây job mới, không phải bug fix). Nội dung dưới đây được **tổng hợp (không bịa)** từ 23 journal của ticket — chủ yếu từ các "Dev handoff" (bàn giao code cho QA, có mục Nội dung thay đổi / File đã sửa / Đánh giá ảnh hưởng / Migration / Điểm cần test) qua **~12 vòng thiết kế (v1 → v13)**. Dùng journal **cuối cùng #153172 (2026-11-09, HEAD `db7a3373e`)** làm trạng thái code hiện tại (code không đổi so với vòng 12 #152283); các vòng trước giữ lại để thấy rõ TẤT CẢ 3 phase + lịch sử bug con đã sửa (cần cho regression ở §4b/§7 report).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI code) — không có tên người cụ thể, assignee Redmine = Thanh Duy Nguyen |
| Commit / Pull Request | `linect-service@db7a3373e6a226c68da3c9f95821161d80653a15` (nhánh gốc `release-t09-2026@be6ef546aedb`) — không có link PR, chỉ có commit hash qua journal |
| Branch | `ai_studio_implement_44036` |
| Ngày submit đánh giá | 2026-11-09 (journal #153172, bàn giao cuối cùng) |
| Auto-filled | 2026-11-09 by `/new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ KHÔNG áp dụng nguyên văn vì input không theo format 4 mục chuẩn (xem cảnh báo đầu file). Leader/Tester cần đọc lại toàn bộ 23 journal (nguyên văn ở `01-bug-task.md` + đầy đủ hơn qua `python scripts/redmine_fetch.py 44036`) trước khi tick.

---

## 1. Nguyên nhân

**Không phải bug** — đây là nhu cầu nghiệp vụ: khi 1 bot bị xóa (xóa cứng khỏi bảng `bots`), các file media của bot đó (ảnh, video, voice, PDF, CSV, QR, landing image, file chat 1:1...) **vẫn còn sót trên disk server** vì trước đây không có cơ chế dọn tự động. Ticket yêu cầu xây **job nền (java-job / linect-service)** để:
1. Dọn các thư mục media gắn với bot đã xóa (Phase 1).
2. Dọn các bot đã bị xóa **từ trước khi có job này** mà chưa ai dọn (Phase 2 — Recover, chạy 1 lần).
3. Dọn **từng file cụ thể** theo yêu cầu riêng (Phase 3, bổ sung sau bởi note #149690 của TuDV ngày 2026-10-29), có kiểm tra **không xóa file mà bot khác còn sống đang dùng chung** (shared-check).

Trong quá trình code (v1 → v13), phát sinh và đã sửa các lỗi thiết kế/code: dry-run vô tình đổi status (#44783 / bug automation #4938), shared-check không nhận dạng path dạng JSON escape (#44910 / #4991), shared-check không chuẩn hóa path tương đối (#44911 / #4992), job xóa nhầm file giao diện web ngoài thư mục upload (#44912 / #4989), lỗi collation cột latin1 với tên file tiếng Nhật (#44913 / #4990), và quan trọng nhất — **shared-check ban đầu chỉ kiểm bảng ghi trong `table_path` nên bỏ sót trường hợp bot khác dùng file ở bảng khác (#45292)**, đã sửa bằng cách luôn kiểm đủ 30 bảng nguồn.

## 2. Cách fix

Code cuối cùng (HEAD `db7a3373e`, module **java-job**) gồm 3 job nền độc lập, cùng dùng 3 config gốc `DELETE_FOLDER_SERVER_IP` / `DELETE_FOLDER_ROOT_PATH` / `DELETE_FOLDER_MODE_DRY_RUN` (mặc định dry-run = 1, chỉ log không xóa):

- **Phase 1 — `DeleteFolderMediaTask` + `DeleteFolderMediaJob`**: mỗi 60s đọc hết (phân trang) các dòng `delete_folder_media_action` của server mình (status 0, đã đến `delete_time`) → xóa đủ thư mục web upload (`ext-media-step`/`ext-media-bak`: 8 loại media/{userId}/{botId}, `images/{userId}/{botId}/landing`, `csv/{botId}`, QR) + `cb-media/line-user/media-step/{botId}`. Guard: bot còn trong `bots` (kể cả soft-delete) ⇒ status 3 không xóa; chặn symlink, chặn ra ngoài ROOT. Dry-run **không đổi status** (mọi dòng bị từ chối gom vào 1 tin Chatwork "DRY_RUN, status unchanged" — bug #44783 đã sửa).
- **Phase 2 — `DeleteFolderMediaRecoverTask` + `DeleteFolderMediaRecoverJob`**: chạy **1 lượt lúc khởi động** khi `DELETE_FOLDER_RECOVER_MODE` > 0 (1 = chỉ log `WOULD_INSERT`, 2 = chèn dòng thật). Quét `bots` (phân trang theo khóa chính) tìm bot đã xóa cứng, suy `userId` từ `user_access_bot` + `user_staff_bots`, kiểm thư mục còn tồn tại trên disk → chèn 1 dòng/bot vào `delete_folder_media_action` với `media_type` lấy từ key `DELETE_FOLDER_RECOVER_MEDIA_TYPE` (1/2/4/5). Idempotent: đã có dòng cùng (bot, media_type) ⇒ bỏ qua. Việc xóa thật vẫn do Phase 1 làm.
- **Phase 3 — `DeleteFileMediaTask` + `DeleteFileMediaJob` + `MediaPathSources`**: mỗi 60s xóa **từng file cụ thể** trong bảng `delete_file_media_action` (`path_file` do web ghi, tính từ `DELETE_FOLDER_ROOT_PATH`). Chỉ nhận file nằm trong **danh sách thư mục cấp 1 upload của web** (allowlist — không đụng js/css/fonts/plugins/tinymce/giao diện). **Trước khi xóa, luôn kiểm file có bị bot khác (còn sống) dùng chung không** — quét đủ **30 bảng nguồn** (bảng ghi trong cột `table_path` của web được kiểm trước để tối ưu, nhưng không dừng ở đó — sửa theo bug #45292), so khớp theo path đã chuẩn hóa (có/không `/` đầu, tuyệt đối, URL) và cả dạng JSON escape (`\/`, `\uXXXX`), dùng `CONVERT(... USING utf8mb4)` để không lỗi collation với cột `latin1`. Có dùng chung ⇒ không xóa (status 2 "SHARED" khi chạy thật, giữ 0 khi dry-run, không Chatwork).
- Yêu cầu hạ tầng: process job phải chạy **locale UTF-8** (path tiếng Nhật); 6 key config `DELETE_FOLDER_*` dạng số chỉ nhận chữ số ASCII (viết sai → app không khởi động).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `AppMain.java` | +11 dòng — thêm khởi động 3 task mới (Phase 1/2/3) khi đủ config | Chỉ chạy trên server đã cấu hình; server khác giữ nguyên hành vi cũ |
| 2 | `ConfigFile.java` | +35 dòng — đọc 6 key `DELETE_FOLDER_*`, parse chặt (chỉ số ASCII) | Key sai format → app không khởi động (regression tất cả job khác nếu lỗi) |
| 3 | `ShareDbRepository.java` | +21 dòng — thêm bean repository mới | Không đổi bean cũ |
| 4 | `BotRepository.java` | +5 dòng — thêm method tra bot theo khóa chính (phục vụ Phase 2/3) | Method cũ không đổi |
| 5 | `UserAccessBotRepository.java` / `UserStaffBotRepository.java` | Repository mới (phục vụ Phase 2 suy userId từ bot đã xóa) | Mới hoàn toàn, không chạm code cũ |
| 6 | `CustomDeleteFileMediaActionRepoImpl.java` | Repository fragment mới — SQL động kiểm shared-check theo whitelist 30 bảng | Cần kiểm Spring khởi động bình thường (bean mới) |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Job xóa thư mục media bot đã xóa | `DeleteFolderMediaTask.java`, `deletefoldermedia/DeleteFolderMediaJob.java` | Direct | Chạy mỗi 60s trên server đã cấu hình; dry-run mặc định |
| F2 | Job recover (chạy 1 lần lúc khởi động) | `DeleteFolderMediaRecoverTask.java`, `deletefoldermedia/DeleteFolderMediaRecoverJob.java` | Direct | Idempotent — rerun không chèn trùng; bật qua `DELETE_FOLDER_RECOVER_MODE` |
| F3 | Job xóa từng file + kiểm shared-check 30 bảng | `DeleteFileMediaTask.java`, `deletefoldermedia/DeleteFileMediaJob.java`, `deletefoldermedia/MediaPathSources.java`, `CustomDeleteFileMediaActionRepo(Impl).java` | Direct | Rủi ro cao nhất — xóa file thật không hoàn tác; shared-check sai từng gây bug #45292 |
| F4 | Đọc config `DELETE_FOLDER_*` (6 key) | `ConfigFile.java` | Direct | App không khởi động nếu key sai format (ảnh hưởng toàn bộ job khác trên server đó) |
| F5 | Khởi động task theo config | `AppMain.java` | Indirect | Chỉ ảnh hưởng server đã cấu hình `DELETE_FOLDER_SERVER_IP` + `ROOT_PATH` |
| F6 | Alert Chatwork (room LOW) khi có dòng bị từ chối/lỗi | Trong 3 Task trên | Indirect | Gom 1 tin/vòng quét, tối đa 5 mẫu; không gửi khi shared-check (status 2) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `delete_folder_media_action` (bot_id, media_type, server_ip, status, delete_time) | CREATE (bảng, **do module web #43088 migrate**) · UPDATE status/updated_at (job) · INSERT (job Phase 2 recover) | ⚠️ Đến 2026-11-09 **web chưa deploy migration này ở release nào** — job sẽ lỗi SQL mỗi vòng nếu bảng chưa tồn tại |
| D2 | `delete_file_media_action` (bot_id, path_file, server_ip, status, delete_time, **table_path**) | CREATE (bảng + cột `table_path`, do web #43088) · SELECT + UPDATE status/updated_at (job) | Cùng rủi ro thiếu migration như D1; cột `table_path` quyết định bảng nào được kiểm trước ở shared-check |
| D3 | 30 bảng nguồn dùng cho shared-check (`rich_menus`, `image_richmenu`, `calendar_*`, `form_*`, `landing`, `popup`, `csv_*`, `form_answer`...) | SELECT only (LIKE, quét toàn bảng) | Chỉ đọc, không sửa; nhưng **thêm tải lên DB chính** mỗi khi có file trên đĩa chưa dùng chung — "các bảng `form_answer*` trên production có thể lớn" (nguyên văn Dev) |
| D4 | File hệ thống trên server media (`ext-media-step`, `ext-media-bak`, `cb-media`) | DELETE (khi `DRY_RUN=0`) | **Không hoàn tác được** — rủi ro cao nhất của cả ticket |
| D5 | `config.properties` của từng server media | CREATE/UPDATE 6 key mới `DELETE_FOLDER_SERVER_IP` / `ROOT_PATH` / `MODE_DRY_RUN` / `RECOVER_MODE` / `RECOVER_MEDIA_TYPE` | Thao tác vận hành (Ops), không phải code |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Mọi tính năng dùng file media của bot **còn sống** (rich menu, message template, landing page, form, calendar, CSV import/export, chat 1:1 gửi media...) — risk nếu shared-check sai sẽ **xóa nhầm file bot sống đang dùng** | F3, D3, D4 | **High** — không hoàn tác được; đã từng xảy ra ở #45292 |
| T2 | Flow xóa bot thật (phía web, `FlowDeleteBot`) — job #44036 chỉ tiêu thụ bảng do web ghi, phụ thuộc đúng thời điểm web chèn dòng | F1, F2, D1 | Medium — cần test luồng xóa bot end-to-end phối hợp web #43088 (chưa verify runtime theo journal #153172) |
| T3 | Vận hành/monitoring job nền trên server media (Chatwork alert, khởi động job, locale UTF-8) | F4, F5, F6 | Medium — key config sai làm **app không khởi động**, ảnh hưởng toàn bộ job khác trên server đó (không chỉ job #44036) |
| T4 | Dữ liệu cũ / legacy (bot xóa trước khi có job, file tên tiếng Nhật, path dạng JSON của web) | F2, F3 | Low–Medium — đã có TC riêng cho recover + locale + JSON escape, nhưng phụ thuộc migration web chưa lên |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

⚠️ **Lưu ý riêng cho ticket này**: do input không theo format 4 mục chuẩn và phụ thuộc migration module web (#43088) **chưa deploy** tính đến ngày tổng hợp (2026-11-09), Leader nên xác nhận với PM/Dev trạng thái migration web trước khi chốt phạm vi review — nhiều "Điểm cần test" trong journal (DB thật, shared-check 30 bảng trên production) **chưa được verify runtime**, chỉ mới unit test.
