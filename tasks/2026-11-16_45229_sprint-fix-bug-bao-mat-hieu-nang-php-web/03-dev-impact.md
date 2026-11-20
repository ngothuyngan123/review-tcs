# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Ticket cha sprint #45229 — 21 nhóm (T1→T21), ~95 sub-issue.** Auto-fill từ Redmine REST API (`scripts/redmine_fetch.py`) + MCP LME TEST STUDIO (`task_get_context(task_id=560, sections=["dev_impact","spec_delta","requirements"])`). Nội dung dưới đây là **tổng hợp ở mức sprint** (vòng 31 — bản đầy đủ nhất tính tới lúc fetch 2026-11-16) + bảng risk theo nhóm từ Studio. **Khi review từng nhóm T<n>, bắt buộc đối chiếu lại dev_impact/spec_delta riêng của sub-issue đó** (Redmine con hoặc Studio `requirements` filter theo `req_key = REQ-X-<ticket>`), vì mức tổng hợp này không đủ chi tiết function-level cho từng ticket.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI implement) |
| Commit / Pull Request | Không có PR link riêng — commit theo chuỗi merge từng vòng trên branch `ai_studio_implement_45229` (sns-line) + `ai_studio_implement_45229` (linect-service). Commit mới nhất tại thời điểm fetch: `85a061ec25` (sns-line), `19b122ab88` (linect-service). |
| Branch | `ai_studio_implement_45229` (2 repo: `sns-line` gốc `release_staging_20261104`@`8877b06f2c11`; `linect-service` gốc `release-t09-2026`@`f929d79140ad`) |
| Ngày submit đánh giá | 2026-11-08 (vòng 31, bản tổng hợp đầy đủ) · cập nhật thêm 2026-11-09 (vòng 32 — mở lại T9) |
| Auto-filled | 2026-11-16 by `/new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ với ticket cha này, "verify" nghĩa là: đọc lại bảng 21 nhóm ở file 01 + bảng risk theo nhóm ở mục 4.3 dưới, xác nhận khớp Redmine #45229 + Studio task #560. Chi tiết 4.1/4.2 **không đầy đủ ở mức sprint** (xem cảnh báo đầu mục 4).

---

## 1. Nguyên nhân

Sprint gom chung nguyên nhân từ **5 nguồn khác nhau**, không phải 1 root cause:
1. **Bug tự detect** — bug do QA/CI tự phát hiện trên các màn hình hiện có.
2. **Improve nội bộ** — cải tiến theo yêu cầu nội bộ (không phải bug).
3. **Triển khai ngang** (horizontal rollout) — áp 1 pattern fix đã có cho nhiều màn/API dùng chung (vd: 1 helper upload/download chung ở T5, 1 luồng 2FA chung ở T1).
4. **AI detect exception** (T15) — exception thật bắt được trên production qua `SNSLineException` (undefined index, deadlock, packet out of order, hết thời gian/bộ nhớ) → sửa root cause, không chỉ bọc try/catch.
5. **AI detect performance** (T16-T20) — chậm phát hiện qua phân tích query (EXPLAIN, N+1, thiếu index).

Riêng **T21** (Lỗi production sau khi lên Laravel 13/PHP 8.5): nguyên nhân là nâng version base (`release_staging_20261104` = PHP 8.5 + Laravel 13) → B1-B11 là lỗi mới lộ ra sau nâng version, đọc từ log production (B3 nằm ở #43554, thuộc nhóm T14).

## 2. Cách fix

Mỗi nhóm T<n> có cách fix riêng theo sub-issue (xem bảng 21 nhóm ở file 01). Ở mức sprint, cách fix chung:
- **T1-T4, T6, T9** (bảo mật): gom nhiều đường xử lý trùng lặp về 1 luồng dùng chung (vd luồng 2FA T1, helper upload T5, check quyền theo `bot_id` T4), thêm validate/kiểm tra quyền còn thiếu.
- **T16-T20** (hiệu năng): sửa theo phân tích query thực tế (EXPLAIN, N+1, index) — có thêm **12 migration index mới trên bảng lớn**, cần chạy đúng thời điểm + có kế hoạch rollback (xem mục Migration).
- **T15** (AI detect exception): sửa nguyên nhân gốc của exception đã bắt được trên production, không che bằng try/catch.
- Đã qua **32 vòng review** tính tới Journal #153467 (09/11/2026); mỗi vòng merge thêm 1-2 sub-issue vào nhánh sprint (log merge chi tiết ở 42 journal không trích trong file 01).

**10 commit gần nhất** (từ Studio `dev_impact`, vòng #497→#508, feature `chat/upload PDF` — minh họa cách Dev fix + check caller ở mức commit):
- `#508` (`33dd262636→85a061ec25`, 3 file code): `refreshMessage` chỉ chuẩn hoá PDF chuỗi không phải JSON (rỗng/NULL/JSON hỏng giữ null); `content_chat.blade.php` (chat-v3) khối PDF/trích dẫn thiếu `filePath` ⇒ 「[PDF]」 (#45597/5424); `mobile/chat.js` link PDF URL tuyệt đối giữ nguyên (#45598/5425); #45599/5426 gửi tin chat web mobile **chưa sửa** (deferred, chờ PM).
- `#507` (`08f2eebd9a→33dd262636`, 5 file code): `ChatController::refreshMessage` trả `{filePath,fileName}` cho tin PDF lưu chuỗi URL (chat-v3 + グループチャット, không ghi DB); `chat_group.js` try/catch từng tin + nhãn `[PDF]` khi rỗng/thiếu `filePath` (#45593/5422); link PDF bỏ `data-toggle='modal'` ở `common.js`, `chats/chat.js`, `mobile/chat.js`, `chat_group.js` (#45594).
- `#506` (`21bdbfe701→08f2eebd9a`, 1 file code): `chat_group.js` tin PDF trong lịch sử グループチャット hiện tên gốc như chat-v3 (#45592/5420), escape.
- `#504` (`b12ade4f4d→21bdbfe701`, 4 file code): `ChatService::rejectMissingConversation` (conversation phải số nguyên >0, else 422 `send_message_fail`) + bỏ nhánh bỏ qua ≤0 trong `isConversationOfRecipient`; `Basic\ChatController` validator `conversation min:1`; `Api\ChatController::denyIfConversationNotOfRecipient` cho `chat/v2/send-message`, `chat/send-template`, `chat/v2/send-media` (token app); `routes/api.php` xoá 3 route trùng trong mobile-auth.
- `#503` (`10ef28ed4f→b12ade4f4d`, 2 file code): `ChatService::isConversationOfRecipient` (conversation.id+bot_id+tb_line_user_id) chặn ở `chatMessage`/`sendMedia`/`sendTemplate` ⇒ 403 (dùng chung `Basic\ChatController` v2 và `Api\ChatController` mobile).
- `#502`, `#501`, `#500`, `#499`, `#498`, `#497`: xem đầy đủ qua `task_get_context(task_id=560, sections=["dev_impact"])` — không trích hết vì chỉ minh hoạ pattern fix, không phải toàn bộ sprint (sprint có 743 file code thay đổi theo `spec_delta.diffStat`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

⚠️ **Không liệt kê đủ ở mức sprint** — 743 file code đổi (theo `spec_delta.diffStat` của Studio task #560), vượt xa khả năng tabulate 1 bảng. Dưới đây là **các điểm dùng chung (shared function/caller) đã được Dev tự nêu** ở journal vòng 31 — áp dụng RULE "hàm dùng chung phải có danh sách caller" khi review các nhóm liên quan:

| # | Function / File dùng chung | Caller / Nơi dùng chung | Nhóm liên quan |
|---|---|---|---|
| 1 | `ChatService::chatMessage` / `sendMedia` / `sendTemplate` | chat-v3, màn nhóm (グループチャット), API job | T13, T17 |
| 2 | `Api\ChatController` (app Flutter) | kiểm hội thoại khớp `to_user`; 3 route `/api/mobile/chat/send-*` chỉ còn bản khoá job | T2, T13 |
| 3 | API `save-hide-friend`, `unhidden-friend`, `block`, `save-bookmark`, `unblock-friend` | dùng chung chat 1:1, chat-v3 và 友だちリスト | T7, T13 |
| 4 | `AuthAttemptLimiter` | mọi cửa đăng nhập + mail đặt lại mật khẩu | T1 |
| 5 | `MobileAccess` | đăng xuất phiên web khi token sai | T1, T2 |
| 6 | `LegacyCharset` (S-7) | hơn 30 file ghi `line_user`/`bot_line_user` và bộ lọc friend — đọc theo charset thật của cột (cache 600s) | T7, T9, T18 |
| 7 | `SecureFileService` / `MediaFileService` | upload/tải ở form khách, chat, media, lịch đặt chỗ, template | T5, T6, T10 |
| 8 | Phân quyền theo bot (staff, owner, `Media::ofBotMembers`) | media, template, friend list, employees-management | T4, T18 |
| 9 | `TemplateV2Service` / `ApiTemplateService` `saveMedia`/`saveButton` | thứ tự ghi đổi, kiểm panel/nút của bot khác theo lô | T13, T17, T18 |
| 10 | Luồng thanh toán UnivaPay/chuyển khoản (`status_payment=4`) + webhook | API nội bộ job gọi web (`KEY_CERTIFICATION_API`, `PUSH_NOTIFY_ALLOWED_IPS`) | T8, T16 |
| 11 | `java-job` relay `tag_history` | job mới bỏ qua `action=3`; web ghi dòng limit với `status_sync=4` | T7 (#37991) |

**Yêu cầu khi review từng nhóm:** kiểm thêm caller cụ thể của nhóm đó qua Studio `task_get_context(task_id=560, sections=["dev_impact"])` lọc theo khoảng commit của sub-issue, vì bảng trên chỉ là các điểm dùng chung Dev tự nêu ở vòng 31, không phủ hết 743 file.

---

## 4. Đánh giá ảnh hưởng

> ⚠️ Ở mức ticket cha, 4.1/4.2 dưới đây là **mức tổng hợp (sprint-wide)**, không đủ để map coverage từng TC — khi review 1 nhóm T<n> cụ thể, phải lấy lại dev_impact riêng của **từng sub-issue** (Studio `requirements` có sẵn `req_key = REQ-X-<ticket_id>`, mỗi sub-issue có mô tả + risk + category riêng — 262 requirement entries cho ~95 sub-issue, cộng 132 requirement entries cấp nhóm `REQ-T<n>-*` cho 17/21 nhóm T1-T13,T15,T16,T20,T21; nhóm T14/T17/T18/T19 chỉ có requirement ở cấp sub-issue).

### 4.1. List function bị ảnh hưởng (mức sprint — xem thêm bảng mục 3)

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChatController::refreshMessage` (`/basic/refresh_message`) | `app/Http/Controllers/ChatController.php` | Direct | Dùng chung chat-v3 và グループチャット; tin PDF chuỗi URL ⇒ `{filePath,fileName}`; endpoint mobile không đổi (T13) |
| F2 | `ChatService::isConversationOfRecipient` / `rejectMissingConversation` | `app/Services/ChatService.php` | Direct | Chặn chat không đúng conversation ⇒ 403/422, dùng chung web v2 và API mobile Flutter (T2, T13) |
| F3 | `AuthAttemptLimiter` | (nhiều file, mọi cửa đăng nhập) | Direct | Giới hạn đăng nhập sai + mail reset password (T1) |
| F4 | `TemplateV2Service` / `ApiTemplateService::saveMedia/saveButton` | (service template) | Direct | Thứ tự ghi đổi, kiểm panel/nút bot khác (T13, T17, T18) |
| F5 | Helper upload/download chung (allow-list, tên file server sinh) | `SecureFileService` / `MediaFileService` | Direct | Áp dụng ngang (horizontal) cho form/chat/media/booking/template (T5, T6, T10) |
| F6 | 12 index mới trên bảng lớn (query EXPLAIN/N+1) | database/migrations (T16-T20) | Direct | Chi tiết migration ở mục dưới — cần đúng thời điểm chạy + rollback plan |
| F7 | `LegacyCharset` | >30 file ghi `line_user`/`bot_line_user` + bộ lọc friend | Indirect | Đọc theo charset thật cột, cache 600s — ảnh hưởng mọi nơi filter/hiển thị friend info (T7, T9, T18) |

### 4.2. List data bị update khi fix bug (mức sprint)

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `users.password_changed_at` | CREATE (migration thêm cột) | Migration phải chạy TRƯỚC code (T1) |
| D2 | `line_user.email` / `phone_number` / `province`, `bot_line_user.phone_number` | MIGRATE (pt-online-schema-change → utf8mb4) | Bảng lớn, dùng pt-osc; bảng > 100.000 dòng bắt buộc pt-osc, không ALTER thẳng (T7, T9) |
| D3 | `users`, `form_answer`/`form_answer_details`, `media`, `bots` — cột text | MIGRATE (utf8mb4, 3 migration: `2026_11_07_100000/100100/100200` + reconvert `2026_11_08_120000`) | Backup trước khi đổi charset (mysqldump) — không rollback được |
| D4 | 12 index mới trên bảng lớn (T16-T20) | CREATE (migration index) | `database/migrations/2026_11_06_100000_add_index_bot_id_msg_kind_id_to_message_tables.php` + 11 file khác (docs/handoff-notes.md mục b) |
| D5 | `tag_history` (relay qua java-job) | UPDATE | Job mới bỏ qua `action=3`; web ghi dòng limit với `status_sync=4` (T7, #37991) |
| D6 | `.env` — biến mới: `LINE_LOGIN_CLIENT_ID/SECRET`, `EMAIL_API_TOKEN`, `KEY_CERTIFICATION_API`, `PUSH_NOTIFY_ALLOWED_IPS`, `DB_UTF8MB4_CONVERT_LARGE`, `UPLOAD_IMAGE_REQUIRE_KEY` | CONFIG | Thiếu `PUSH_NOTIFY_ALLOWED_IPS` trước deploy ⇒ thông báo PC dừng (T16-T20) |

### 4.3. List tính năng bị ảnh hưởng — theo 21 nhóm T1→T21 (risk từ Studio `requirements`, nhóm nào Studio chưa có risk riêng ghi `Chưa rõ — xem từng sub-issue`)

| # | Tính năng / Nhóm | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Đăng nhập, 2FA, tài khoản, phiên | F3, D1 | **High** |
| T2 | MCP OAuth và đăng nhập/API mobile phía server | F2 | **High** |
| T3 | Route public, debug, API nội bộ, log và secret | (rotate secret, xoá route debug) | **High** |
| T4 | Phân quyền theo bot_id, admin và nhân viên | F8 (mục 3) | **High** |
| T5 | Upload và tải file | F5 | Medium |
| T6 | Form trả lời | F5 | Medium |
| T7 | Danh sách friend, bộ lọc, export, thông tin friend | F7, D2, D5 | Medium (riêng #37991 spec đã chốt → High nếu sai lịch sử limit) |
| T8 | Thanh toán và hợp đồng | (F10 mục 3, D6) | **High** (#41127 spec đã chốt) |
| T9 | Booking: bảo mật, Google Calendar/Sheet | (Security T05 + Google sync) | **High** (vòng 32 mở lại cho 2 bug mới + 4 fix cũ CHƯA merge — xem file 01) |
| T10 | Salon/Lesson/Event: khung giờ, màn hình, LIFF | F5 | Medium |
| T11 | Affiliate/ASP | (Security T16 riêng) | Medium |
| T12 | Báo cáo và escape (hardening) | (escape XSS) | Medium |
| T13 | Chat 1:1, trigger, action, template | F1, F2, F4 | Medium |
| T14 | Lỗi 500 và UI chung | (null check, UI nhỏ) | Low-Medium |
| T15 | Exception PHP do AI phát hiện | (SNSLineException gốc) | Medium |
| T16 | Hiệu năng: đặt lịch Salon/Lesson, thông báo | F6, D4, F10 | Medium (đổi index + endpoint booking) |
| T17 | Hiệu năng: chat, template, gửi tin | F4 | Medium |
| T18 | Hiệu năng: friend, tag, bộ lọc, rich menu, form | F7, F8 | Medium |
| T19 | Hiệu năng: phân tích, thống kê admin | (query only, không đổi hành vi) | Low-Medium |
| T20 | Hiệu năng: webhook, LIFF, đăng ký, khác | F6 | Medium |
| T21 | Lỗi production sau khi lên Laravel 13 / PHP 8.5 | (nền toàn sprint) | **High** — áp thêm `framework/php-upgrade-checklist.md` làm trục quét bổ sung (RULE-08) |

---

## Migration / thay đổi dữ liệu (nguyên văn vòng 31 — đầy đủ, dùng cho mọi nhóm chạm deploy)

- **[Backup · Trước deploy]** Backup bảng `users, bots, form_answer, form_answer_details, media, line_user, bot_line_user` trước khi đổi charset: `mysqldump --single-transaction <db> users bots form_answer form_answer_details media line_user bot_line_user > backup_45229.sql` (hoặc snapshot cả DB) — không rollback được.
- **[Config · Trước deploy]** Thêm `LINE_LOGIN_CLIENT_ID`, `LINE_LOGIN_CLIENT_SECRET` (giá trị đang viết cứng trước đây) → `php artisan config:clear`.
- **[Config · Trước deploy]** `EMAIL_API_TOKEN` bắt buộc (giá trị đang chạy trên production) → `php artisan config:clear`.
- **[Config · Trước deploy]** `KEY_CERTIFICATION_API` trùng key của job Java → `php artisan config:clear`.
- **[Thao tác tay · Trước deploy]** `ANALYZE` + đo cỡ bảng nhỏ; bảng > 100.000 dòng đổi utf8mb4 bằng pt-osc trước.
- **[Schema · Trước deploy]** pt-osc 4 cột `line_user.email/phone_number/province` và `bot_line_user.phone_number` sang utf8mb4 (SQL ở `docs/handoff-notes.md` i.2 bước 3).
- **[Schema · Trước deploy]** 12 migration thêm index (T16-T20) — `database/migrations/2026_11_06_100000_add_index_bot_id_msg_kind_id_to_message_tables.php` + 11 file khác.
- **[Schema · Trước deploy]** Thêm cột `users.password_changed_at`.
- **[Schema · Trước deploy]** 3 migration utf8mb4 (`users`, `form/media/bots`, `line_user` contact) — nếu dừng với lỗi "Bảng vượt 100000 dòng" thì chạy pt-osc với mệnh đề MODIFY in ra rồi chạy lại.
- **[Schema · Trước deploy]** Migration `2026_11_08_120000` chạy lại `up()` của `100200` cho DB đã chạy `100200`.
- **[Config · Trước deploy]** `DB_UTF8MB4_CONVERT_LARGE` chỉ đặt cho DB test/staging, **KHÔNG** đặt production.
- **[Config · Trước deploy]** `PUSH_NOTIFY_ALLOWED_IPS` = IP/CIDR mọi server job gọi `/api/notify/push-notify`.
- **[Config · Trước deploy]** Kiểm giới hạn upload mọi server web: PHP `upload_max_filesize`/`post_max_size`; Nginx `client_max_body_size` hoặc Apache `LimitRequestBody` ≥ 50MB (PDF) / 200MB (tài liệu/âm thanh/ảnh).
- **[Hạ tầng · Khi deploy]** Rule chặn file rác ở `public` (Apache `AllowOverride` / Nginx location 403).
- **[Config · Sau deploy]** Bật `UPLOAD_IMAGE_REQUIRE_KEY` sau khi server ảnh lên bản mới.
- **[Recover · Sau deploy]** Khôi phục duration audio của template (#41192): `php artisan template:recover-audio-duration` (đếm thử) → backup → `--apply [--bot_id=] [--chunk=200]`.
- **[Thao tác tay · Sau deploy]** Dọn file rác `public` trên mọi server web (`images_rich.zip`, `public/root`, `public/Users`, `public/https:`, file `.svg/.html/.php` lạ dưới `public/media`).
- **[Hạ tầng · Sau deploy]** Xoá crontab 00:10 `compress:log` (Kernel đã lịch 00:01).

### Lưu ý khi deploy

- Thứ tự đầy đủ ở `docs/handoff-notes.md` mục (g). Trước deploy: backup → env mới (gồm `PUSH_NOTIFY_ALLOWED_IPS`) → kiểm giới hạn upload → DBA ANALYZE/đo bảng nhỏ, pt-osc `line_user`/`bot_line_user` → `php artisan migrate --force`.
- Deploy web: `composer install --no-dev --optimize-autoloader` (PHP ≥ 8.4.1, ext-dom; verify `php artisan about`).
- Sau deploy: `php artisan optimize:clear`, `php artisan queue:restart`, reload PHP-FPM; web và worker cùng `APP_KEY`. **KHÔNG** chạy `route:cache`/`optimize`; **KHÔNG** bật `config:cache` mới; `APP_DEBUG=false` production.
- Trước `php artisan migrate` trên production: kiểm `php artisan env = production` (APP_ENV local/testing làm migration ALTER thẳng bảng lớn có khoá ghi).
- `java-job` (#45437): không ràng buộc thứ tự với web, khuyến nghị deploy sau web.
- Môi trường HTTP không TLS: `SESSION_SECURE_COOKIE=false`. QA hard-reload (Ctrl+F5) hoặc xoá cache CDN.
- **KHÔNG** chạy `php artisan migrate:rollback` mà không kèm `--path`.

## Việc cần người làm thêm (ngoài phạm vi code sprint — không đẻ TC cho các mục này, chỉ note)

- `public/js/chats/ajax-error.js`: `NETWORK_MESSAGE` mất câu nhắc kiểm lịch sử (có sẵn ở base).
- chat-v3: hộp 送信プレビュー không đóng sau lỗi 424/5xx (có sẵn ở base).
- PM chọn hướng #5426/#45599 (chat web mobile không gửi được tin): (a) làm lại theo route v2, (b) khoá ô gửi, hoặc (c) `not_a_bug`.
- QA #45551 đang Reject trên Redmine nhưng đã sửa theo PM 08/11 — cần mở lại/chuyển Fix done + chạy lại NEW-1004.
- Ticket riêng sửa 24 test đỏ có sẵn từ base; rotate secret viết cứng; 2FA cho `/api/mobile/login` (chờ app có màn nhập mã #45152); token webhook Univapay theo store (#45395).
- **T9 (vòng 32):** 4 fix cũ (#42413, #42414, #42437, #42439/#42791) liên quan booking/Google đang ở nhánh riêng **CHƯA merge** vào sprint — PM/Dev cần quyết trước khi chốt coverage T9 (xem file 01).

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) — đã hiểu đây là sprint gộp 5 loại nguyên nhân, không phải 1 root cause.
- [ ] Mục 2/3 — chấp nhận mức tổng hợp sprint-wide; **mỗi nhóm T<n> khi review phải tự lấy thêm dev_impact/requirements riêng của sub-issue đó** (không dùng mục 3 ở đây làm đủ coverage).
- [ ] Mục 4.1/4.2 không thiếu function/data **ở mức đã biết tới thời điểm fetch** (vòng 31) — vòng 32 (T9) đã note riêng, cần cập nhật khi có vòng mới.
- [ ] Mục 4.3 — đã thấy đủ 21 nhóm + risk.
- [ ] Đã đọc phần Migration/deploy — nhóm nào chạm T5/T6/T7/T8/T9/T16-T20 bắt buộc review kèm rủi ro deploy.
- [ ] Đã note: T9 có 4 ticket cũ chưa merge, T21 cần thêm `framework/php-upgrade-checklist.md`.
