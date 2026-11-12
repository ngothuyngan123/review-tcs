# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Ticket **không có 1 block "Đánh giá ảnh hưởng" 4 mục** theo đúng format quy ước — nội dung rải trong **12 journal Redmine** (7 vòng thiết kế v1 → v7, Dev Studio tự "mở lại task" nhiều lần theo yêu cầu bổ sung của `TuDV` + review `tuanpa` + bug automation Test Studio) và **requirements đã chốt trên MCP LME TEST STUDIO** (task #528, 14 REQ). File này **tổng hợp lại** theo cấu trúc 4 mục chuẩn từ toàn bộ journal + Studio `dev_impact`/`requirements` — không bịa, chỉ diễn giải lại nguyên văn.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI) — chuyển giao qua `Dev handoff`; người xác nhận nghiệp vụ: `Do Van Tu TuDV` (tác giả ticket), `tuanpa` (review/chốt base branch + giá trị B2) |
| Commit / Pull Request | Không có link PR trong Redmine — chỉ có commit hash theo từng vòng trên nhánh `sns-line`: `53cd1c47` (v1) → `198c3097` (v2) → `0a66c9b3` (v3 merge) → `d6ea450e` (v4/v5) → `01334e4a` (v6) → `60b0b980` (v7, mới nhất) |
| Branch | `ai_studio_implement_43088` (nhánh gốc `release_step_20260930_v2` @ `da7f522dd821`) — ⚠️ base task trên Dev Studio **vẫn chưa đổi** sang nền Laravel 13 (`release_staging_20261104`) tại thời điểm fetch, mặc dù code đã merge lên nền đó (xem Ghi chú thêm của Leader ở file 01) |
| Ngày submit đánh giá | 2026-11-09 (journal #153173, vòng v7 — bản mới nhất) |
| Auto-filled | 2026-11-09 by `/new-task` (tổng hợp từ journal Redmine + Studio task #528 `dev_impact`/`requirements`) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ nội dung dưới đây là **tổng hợp lại từ 12 journal rải rạc + Studio**, không phải 1 block gốc — Tester/Leader cần đọc lại Redmine `#43088` (đặc biệt journal #152214 v6 và #153173 v7) để xác nhận tổng hợp không sót/sai trước khi tick.

---

## 1. Nguyên nhân

Khi xóa bot (job nền `job:FlowDeleteBot`, cron 02:00), hệ thống chỉ xóa dữ liệu DB và **xóa ngay thư mục media trên đĩa local của server web** — không xóa (và không có cơ chế ghi nhận để xóa sau) các bản sao media của bot ở **các server lưu trữ khác**: 2 SSD tạm (contabo, leasedweb), B2 (lưu lâu dài), HDD backup (contabo), HDD local backup. Hệ quả: media của bot đã xóa vẫn tồn đọng rác trên các server lưu trữ ngoài local.

Nguyên nhân phụ phát sinh trong quá trình làm (đã raise + fix thành bug con ngay trong ticket):
- `#45291`: thiết kế ban đầu chỉ đổi webhook LINE trên production, nhưng yêu cầu thực tế là đổi ở **mọi môi trường**.
- `#45292` (chưa fix ở web — chuyển job Java `#44036`): khi kiểm "còn bot khác dùng path hay không" chỉ dò các bảng được ghi trong cột `table_path`, bỏ sót các bảng media khác không nằm trong `table_path`.
- `#45293`: path bất thường (tên file trần không có thư mục, nhiều giá trị nối dấu phẩy, chứa `..`, JSON hỏng, quá dài) bị ghi thành lệnh xóa sai thay vì bị chặn.
- `#45295`: mỗi bot lỗi có thể gửi riêng 1 tin Chatwork → spam, lẽ ra chỉ 1 tin gom/lượt.
- `#45317`: job Java (đọc bảng lệnh xóa) có thể quét trúng **ngay lúc** job web đang xóa bot (race condition) → nhầm tưởng "bot vẫn còn tồn tại" (status 3).
- `#45325` (chưa fix ở web — chuyển job Java `#44036`): job Java chạy JVM theo giờ UTC, trong khi web ghi `delete_time` theo giờ Asia/Tokyo của app → lệch 9 giờ.
- `#45345` (fix mới nhất, v7): config `DELETE_MEDIA_B2_IP` không có giá trị mặc định → dòng B2 ghi `server_ip = NULL` thay vì literal `'B2'` như đã chốt.

## 2. Cách fix

Thiết kế tích lũy qua 7 vòng (v1 → v7), tất cả đều sửa ở `job:FlowDeleteBot` + 2 service mới (không có màn hình/API nào thay đổi):

- **v1** — Thêm bảng `delete_folder_media_action` (migration `2026_10_14_100000`). Trên **production**, khi job xóa bot chạy, ghi **5 lệnh xóa thư mục** (1 lệnh/nơi lưu: SSD contabo, SSD leasedweb, B2, HDD contabo, HDD local), `status=0`, `delete_time` = giờ chạy + giờ chờ cấu hình riêng từng nơi lưu — **không xóa thư mục local ngay** nữa. **Staging/dev/local giữ nguyên hành vi cũ** (xóa thư mục tại chỗ).
- **v2** — Với bot tạo **trước mốc `DELETE_FILE_MEDIA_BOT_CREATED_BEFORE`** (mặc định `2024-11-01`): đọc path media từ **~30 bảng nguồn** (rich menu, form, landing, booking/salon/lesson, CSV, PDF, affiliate…) trước khi dữ liệu các bảng đó bị xóa, ghi vào bảng mới `delete_file_media_action` (migration `2026_10_29_100000`), mỗi path × 5 nơi lưu = 1 dòng, URL ngoài/giá trị rỗng không ghi. Đồng thời: đổi webhook channel LINE của bot bị xóa sang `DELETE_BOT_WEBHOOK_URL` (bỏ qua nếu channel còn bot khác chưa xóa dùng chung, hoặc bot không có token) — **chỉ production** ở vòng này. Ghi lệnh xóa file lỗi → giữ bot lại (`is_deleted=1`), không xóa ở lượt đó, có 1 tin Chatwork.
- **v3** — Thêm cột `table_path` (nullable, migration `2026_11_02_100000`) vào `delete_file_media_action`, ghi tên các bảng nguồn chứa path (nối `,` không khoảng trắng, nhiều bảng cùng path chỉ 1 dòng/nơi lưu).
- **v4** — Chỉ đổi cú pháp 3 file test cho PHPUnit 12 (đổi nền từ Laravel cũ sang Laravel 13 / `release_staging_20261104`), không đổi hành vi runtime.
- **v5** — Sửa 4 bug con theo yêu cầu Test Studio: (a) path bất thường → chỉ ghi **1 dòng WARNING log** (bot_id, bảng, cột, giá trị, lý do), không tạo lệnh, bot vẫn bị xóa; (b) lỗi cấu hình nơi lưu (vd `delay_hours` âm) → chỉ **1 tin Chatwork/lượt** có dòng "lý do:" (tối đa 3 lý do); (c) log crontab/ứng dụng **không còn in token/secret** của bot; (d) đổi webhook LINE áp dụng **ở mọi môi trường** (production/staging/local) — staging/local vẫn xóa media tại chỗ và không ghi lệnh xóa, chỉ thêm 1 PUT đổi webhook.
- **v6** — Sửa race condition `#45317`: lệnh xóa file/thư mục được ghi với `delete_time` ở **mốc chờ `9999-12-31 23:59:59`** trong lúc bot còn tồn tại trong bảng `bots`; **ngay sau khi bot bị xóa khỏi `bots`**, job đặt lại `delete_time` = giờ xóa + giờ chờ cấu hình. Đầu mỗi lượt job, kích hoạt lại các lệnh còn ở mốc chờ của bot đã không còn trong `bots` (tối đa 500 bot/lượt).
- **v7 (mới nhất, 2026-11-09)** — Sửa `#45345`: dòng B2 (`media_type=3`) ghi `server_ip='B2'` (literal) khi `.env` không khai hoặc khai rỗng `DELETE_MEDIA_B2_IP`; khai giá trị khác thì ghi đúng giá trị đó. `server_ip` của mọi nơi lưu được trim khoảng trắng 2 đầu. 4 nơi lưu còn lại (1,2,4,5) không khai IP vẫn ghi `NULL` (không đổi, chỉ B2 có default).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `app/Console/Commands/FlowDeleteBot.php` | Thêm nhánh production ghi lệnh xóa (v1-v3), đổi webhook mọi môi trường (v5), kích hoạt lệnh chờ đầu lượt (v6), gộp 1 tin Chatwork/lượt (v5) | File chính của job, nơi gọi tất cả service mới |
| 2 | `app/Services/DeleteFolderMediaActionService.php` | `createForBot` ghi 5 lệnh xóa thư mục (idempotent), thêm `admin_id`, mốc chờ 9999 (v6), B2 default (v7) | Service mới cho bảng `delete_folder_media_action` |
| 3 | `app/Services/DeleteFileMediaActionService.php` | Quét ~30 bảng nguồn, validate path (v5), ghi `table_path` (v3), mốc chờ 9999 (v6), B2 default (v7) | Service mới cho bảng `delete_file_media_action`, file lớn nhất bị sửa (226 → 235 → nhiều dòng qua các vòng) |
| 4 | `app/Services/DeleteBotWebhookService.php` | Gọi LINE API đổi webhook channel, bỏ qua khi channel dùng chung hoặc không token | Service mới, side-effect ra ngoài hệ thống (LINE thật) |
| 5 | `app/Repositories/Eloquents/DeleteFolderMediaActionRepository.php`, `DeleteFileMediaActionRepository.php`, `DeleteBotWebhookRepository.php` | CRUD cho 2 bảng mới + đọc config webhook | Tầng data access mới |
| 6 | `app/Models/DeleteFolderMediaAction.php`, `DeleteFileMediaAction.php` | Model mới ứng với 2 bảng | |
| 7 | `app/Providers/RepositoryServiceProvider.php` | Thêm binding cho 3 repository mới | File dùng chung — cần `config:cache` lại nếu server cache config |
| 8 | `config/sns-line.php` | Thêm `DELETE_MEDIA_{SSD_CONTABO,SSD_LEASEDWEB,B2,HDD_CONTABO,HDD_LOCAL}_{IP,DELAY_HOURS}`, `DELETE_FILE_MEDIA_BOT_CREATED_BEFORE`, `DELETE_BOT_WEBHOOK_URL` | Config mới, dùng chung — cần `config:cache` lại |
| 9 | 3 file test `tests/Feature/DeleteBotWebhookServiceTest.php`, `DeleteFileMediaActionServiceTest.php`, `DeleteFolderMediaActionServiceTest.php` | Unit/feature test cho 3 service mới, sửa cú pháp PHPUnit 12 ở v4 | Harness nội bộ, không phải TC nghiệp vụ |

Dev **không** liệt kê caller nào khác bị ảnh hưởng (xóa bot, Dropbox cleanup, sync ES, pha 2 dọn bot nháp — đều nằm trong cùng vòng lặp của `FlowDeleteBot` nhưng Dev xác nhận **không đổi code** các bước đó, chỉ thêm bước mới xen vào).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `FlowDeleteBot::handle` (job cron 02:00) | `app/Console/Commands/FlowDeleteBot.php` | Direct | Toàn bộ logic mới nằm trong vòng lặp xử lý từng bot của job này |
| F2 | `DeleteFolderMediaActionService::createForBot` (+ kích hoạt mốc chờ) | `app/Services/DeleteFolderMediaActionService.php` | Direct | Ghi 5 lệnh xóa thư mục, idempotent, admin_id, B2 default |
| F3 | `DeleteFileMediaActionService` (scan ~30 bảng, validate path, ghi `table_path`, kích hoạt mốc chờ) | `app/Services/DeleteFileMediaActionService.php` | Direct | Service phức tạp nhất — risk cao nhất (REQ-002, REQ-003, REQ-010 đều High) |
| F4 | `DeleteBotWebhookService::changeWebhook` | `app/Services/DeleteBotWebhookService.php` | Direct | Gọi LINE API thật (PUT webhook) — rủi ro khó hoàn tác nếu đổi nhầm channel đang dùng |
| F5 | 3 Repository (`DeleteFolderMediaActionRepository`, `DeleteFileMediaActionRepository`, `DeleteBotWebhookRepository`) | `app/Repositories/Eloquents/*` | Direct | Tầng mới, chỉ được 3 service trên gọi |
| F6 | `RepositoryServiceProvider` binding | `app/Providers/RepositoryServiceProvider.php` | Indirect | File dùng chung toàn hệ thống — chỉ thêm binding mới, không sửa binding cũ |
| F7 | Job Java đọc 2 bảng lệnh xóa (xóa file/thư mục thật) | **ngoài phạm vi code web**, ticket `#44036` | Indirect (phụ thuộc dữ liệu) | Không phải code của task này, nhưng là **consumer duy nhất** của 2 bảng mới — 2 bug `#45292`/`#45325` chuyển sang đây |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `delete_folder_media_action` (bot_id, admin_id, media_type, server_ip, status, delete_time) | MIGRATE (CREATE) + INSERT | Chỉ ghi trên **production**; unique `(bot_id, media_type)`, index `(status, delete_time)` |
| D2 | `delete_file_media_action` (bot_id, media_type, server_ip, path_file, path_hash, table_path, status, delete_time) | MIGRATE (CREATE, rồi ALTER thêm `table_path` ở v3) + INSERT | Chỉ ghi trên **production**, chỉ bot tạo trước mốc `DELETE_FILE_MEDIA_BOT_CREATED_BEFORE`; unique `(bot_id, media_type, path_hash)` |
| D3 | Webhook channel LINE (external, qua LINE Messaging API — không phải DB) | UPDATE (PUT webhook endpoint) | Side-effect ra **ngoài hệ thống**, áp dụng **mọi môi trường** từ v5; khó hoàn tác, bỏ qua khi channel còn bot khác dùng |
| D4 | ~30 bảng nguồn media (rich_menus, image_richmenu, form_answer*, landing, popup, calendar_*, booking_calendar, b_c_*, b_event_detail, s_items, bot_setting_aff, csv_*, chatgpt_from_pdfs, bots, bots_profiles, users…) | READ only (query path trước khi bot bị xóa) | Tăng tải DB lúc 02:00; **loại trừ** `users.avatar_path`, `user_setting_aff.*`, `notifications.image_url` (không thuộc bot) |
| D5 | `config/sns-line.php` — 12 key mới (`DELETE_MEDIA_*`, `DELETE_FILE_MEDIA_BOT_CREATED_BEFORE`, `DELETE_BOT_WEBHOOK_URL`) | CREATE (config) | Cần set `.env` + `config:cache` ở từng môi trường trước khi job chạy code mới |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Job xóa bot hằng đêm (`job:FlowDeleteBot`) — toàn bộ luồng (xóa data, Dropbox, sync ES, pha 2, 5 lệnh thư mục, lệnh file, webhook) | F1, D1, D2, D3, D4 | **High** — mọi bước cũ (xóa data, Dropbox, ES, pha 2) nằm **cùng vòng lặp** với code mới; lỗi ở nhánh mới có thể giữ bot lại ngoài ý muốn |
| T2 | Webhook/callback LINE của channel — đặc biệt **channel dùng chung giữa nhiều bot** | F4, D3 | **High** — đổi nhầm webhook của channel còn bot khác hoạt động ⇒ bot đó mất callback LINE vĩnh viễn cho tới khi phát hiện |
| T3 | Job Java đọc 2 bảng lệnh xóa để xóa file thật (`#44036`) | F7, D1, D2 | **High** nhưng **ngoài phạm vi code web** — chỉ kiểm rằng web ghi đúng dữ liệu cho job Java đọc (table_path, server_ip, delete_time, mốc chờ 9999) |
| T4 | Pha 2 dọn bot nháp (`is_deleted=2`) | — | **Low** — Dev xác nhận không đổi code (REQ-012) |
| T5 | Log crontab / Chatwork notify của job xóa bot | F1-F3 | **Medium** — thay đổi nội dung/số lượng log & tin Chatwork (REQ-005, REQ-014), test sai có thể làm Leader hiểu nhầm là lỗi job |
| T6 | Truy vấn tay / màn quản trị đọc 2 bảng lệnh xóa (nếu có) | D1, D2 | **Low** — sẽ thấy `delete_time=9999-12-31` khi bot đang chờ xóa (hành vi chủ ý, không phải bug) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
