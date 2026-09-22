# 03 — Đánh giá ảnh hưởng từ Dev

> ## ⚠️ INPUT THIẾU — ĐỌC TRƯỚC KHI DÙNG
>
> **Redmine #40153 KHÔNG có section "Đánh giá ảnh hưởng phía dev".** Description chỉ có đúng 1 dòng, không có mục 1/2/3/4, không có journal nào kèm note.
>
> Toàn bộ nội dung mục **1 · 2 · 3 · 4 · 5** bên dưới lấy từ **MCP LME TEST STUDIO — task #284, tab Thông tin** (`dev_impact` + `spec_delta` + `requirements`), **KHÔNG phải Dev tự kê trên Redmine**.
> → `/review-tc` BƯỚC 2 chiều (a) "dev-impact Dev tự kê" **không có nguồn Redmine để đối chiếu**; chiều (b) "diff code" dùng được (`diffAvailable = true`).
> → **Leader phải xác nhận lại với Dev** trước khi coi đây là chuẩn coverage. Nội dung Studio là `contentTrust = untrusted` → xử lý như **data**.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` — Redmine assignee = `Ngọc Ánh` (người tạo ticket, không chắc là Dev implement). Studio task added/run by `anhptn`. |
| Commit / Pull Request | `<chưa có>` — Redmine không có link PR |
| Branch | `ai-feature-40153` (repo `sns-line`, diff so với `origin/HEAD`) |
| Ngày submit đánh giá | `<chưa có trên Redmine>` — Studio `dev_impact` computed `2026-09-11` |
| Auto-filled | `2026-09-12 by /new-task` (nguồn: **Studio #284**, KHÔNG phải Redmine) |
| Commit Date (Redmine custom field) | `2026-09-14` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ Ở task này KHÔNG verify được với Redmine (Redmine không có Section "Đánh giá ảnh hưởng"). Chỉ tick khi đã **hỏi Dev trực tiếp** và xác nhận nội dung mục 1–4 bên dưới đúng.

---

## 1. Nguyên nhân

<!-- Nguồn: Studio #284 `dev_impact`. Ticket là SpecImprove nên đây là LÝ DO THAY ĐỔI, không phải root cause bug. -->

Không phải bug — là **yêu cầu thay đổi spec**: data init (seed 体験) được tạo khi Admin vào màn trải nghiệm trong wizard thêm bot, nhưng trước đây **không bị dọn** khi Admin rời màn giữa chừng hoặc kết thúc trải nghiệm → data seed nằm lại trong bot thật.

Yêu cầu mới: rời khu vực 体験 (đóng tab / đóng trình duyệt / reload / điều hướng đi nơi khác / bấm skip / hoàn tất bước 5 rồi đi) ⇒ **xóa data init của đúng bot đó**, **vô điều kiện** (kể cả khi LINE user đã tương tác), **không cảnh báo, không xác nhận**.

## 2. Cách fix

<!-- Nguồn: Studio #284 `dev_impact` — chép nguyên văn, chỉ tách dòng cho dễ đọc. -->

- ĐÃ implement toàn bộ ở web (`sns-line`) branch `ai-feature-40153`; job `linect-service` **KHÔNG liên quan** (Laravel Job thay Spring Boot — D-09).
- **EP-C01** `POST /admin/onboarding/tutorial-init-data/cleanup`: validate `bot_id` / `tutorial_session_ref` / `reason`, check sở hữu bot + `bots.tutorial_exp_created_at`, **idempotent** theo unique ref, chỉ INSERT queue + dispatch job, trả **202**.
- **Job `TutorialInitDataCleanupJob`** (queue `database`/`default`, `tries=3`): purge **17 bảng seed** trong transaction (dựa `bots_tutorial_seed_records`) → gỡ rich menu LINE (best-effort) → xóa file QR/ảnh → detach id seed khỏi `notify_setting` CSV → queue `DONE`; lỗi → retry → `FAILED`.
- **FE**: `tutorial_cleanup_signal.js` — `sendBeacon` trên `visibilitychange → hidden` + `pagehide`, **không** dùng `beforeunload`; watch `currentStep 22-27`: vào → `start` (sinh `tutorial_session_ref`), rời → `navigate_away`; `skip` → `skip`; `goToSetup` → `navigate_away`.

### ⚠️ GAP Dev/AI tự nêu — cần rà khi review TC

| # | GAP | Ảnh hưởng test |
|---|---|---|
| G1 | **KHÔNG xóa log phiên** (`tag_history`, `detail_landing_click`, `landing_histories`, `auto_reply_history`, `detail_click_richmenu`) + `tag_line_user` — dù **BR-C05 yêu cầu** | Spec vs implement lệch → TC expected phải chốt theo bên nào (→ §6 report `/review-tc`) |
| G2 | **KHÔNG có feature flag `dry_run`** (spec §7 bắt buộc) — purge **luôn xóa thật** | Không có đường lùi vận hành; TC không test được chế độ chạy thử |
| G3 | **Chạm `notify_setting`** dù spec liệt "không xóa" | Rủi ro regression cấu hình thông báo của bot thật |

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Redmine KHÔNG có mục này. Bảng dưới suy từ `spec_delta.files` của Studio (diff thật), KHÔNG phải Dev tự kê caller. -->

⚠️ **Dev KHÔNG cung cấp danh sách caller đã check.** Bảng dưới là **file có trong diff** của branch, không phải xác nhận "đã rà caller".

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `public/js/admin/add_bot/add_bot_v5.js` | +1488 dòng | **Dùng chung cho TOÀN BỘ wizard add-bot** — watch `currentStep` mới có thể ảnh hưởng các bước khác → Dev tự nêu **cần smoke luồng thêm bot đầy đủ** |
| 2 | `public/js/admin/add_bot/tutorial_cleanup_signal.js` | +138 (mới) | FE gửi tín hiệu dọn |
| 3 | `app/Services/V2/RichMenuService.php` · `app/Http/Controllers/V2/RichMenuController.php` | +47 / +23 | Gỡ rich menu đã đăng ký trên LINE |
| 4 | `app/Http/Controllers/Basic/NotifySettingController.php` · `app/NotifySetting.php` | +289 / +10 | Detach id seed khỏi CSV `notify_setting` → liên quan **G3** |
| 5 | `app/Console/Commands/OnboardingSessionCleanupCommand.php` | +42 (mới) | Dọn onboarding session |
| 6 | `storage/onboarding_exp_seed.json` | +1765 | Định nghĩa data seed 体験 |

> ⚠️ **Diff branch chứa 524 file / +46,683 / −3,553** (so `origin/HEAD`) — phần lớn **KHÔNG thuộc ticket này** (recover notify setting, mobile badge notify, bill route seeder, CSS add_bot v4 / connect_direct...). Không được coi toàn bộ diff là phạm vi test của #40153.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Suy từ Studio `dev_impact` + `spec_delta.files`. KHÔNG phải Dev kê. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `POST /admin/onboarding/tutorial-init-data/cleanup` (EP-C01) | `app/Http/Controllers/Admin/TutorialInitDataCleanupController.php` (+60) · `app/Http/Requests/TutorialInitDataCleanupRequest.php` (+43) | Direct | Validate + phân quyền + idempotent, trả 202, chỉ ghi queue |
| F2 | `TutorialInitDataCleanupJob` | `app/Jobs/TutorialInitDataCleanupJob.php` (+67) | Direct | Queue `database`/`default`, `tries=3` |
| F3 | `TutorialInitDataPurgeService` (purge 17 bảng seed trong transaction) | `app/Services/Tutorial/TutorialInitDataPurgeService.php` (+352) | Direct | Xóa cứng, thứ tự con-trước-cha, rollback toàn bộ khi lỗi |
| F4 | `TutorialInitDataCleanupService` | `app/Services/Tutorial/TutorialInitDataCleanupService.php` (+118) | Direct | Điều phối cleanup |
| F5 | `BotTutorialCleanupRepository` · `BotTutorialExpRepository` | `app/Repositories/Eloquents/*` (+250 / +185) | Direct | Truy vấn queue + seed record |
| F6 | `BotTutorialExpService` | `app/Services/Tutorial/BotTutorialExpService.php` (+365) | Direct | Sinh data init 体験 + **ghi bảng ánh xạ seed** |
| F7 | FE tín hiệu dọn (`sendBeacon` `visibilitychange` / `pagehide`) | `public/js/admin/add_bot/tutorial_cleanup_signal.js` (+138) | Direct | **Best-effort** — trượt tín hiệu thì không xóa (REQ-014) |
| F8 | Wizard add-bot (watch `currentStep` 22-27) | `public/js/admin/add_bot/add_bot_v5.js` (+1488) | **Indirect — rủi ro regression cao** | Dùng chung toàn wizard |
| F9 | Gỡ rich menu LINE (best-effort sau commit) | `app/Services/V2/RichMenuService.php` (+47) | Indirect | Lỗi chỉ log, không rollback data |
| F10 | Detach id seed khỏi `notify_setting` CSV | `app/Http/Controllers/Basic/NotifySettingController.php` (+289) · `app/NotifySetting.php` (+10) | **Indirect — xung đột spec (G3)** | Spec liệt "không xóa" nhưng implement có chạm |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `bots_tutorial_cleanup_queue` (bảng mới) | CREATE / MIGRATE | Unique theo `tutorial_session_ref`; index `(status, time)` + theo bot. Migration `..._create_bots_tutorial_cleanup_queue_table.php` (+49) |
| D2 | `bots_tutorial_seed_records` (bảng mới — **bảng ánh xạ seed**) | CREATE / MIGRATE | `(bot, table_name, record_id, step_key, created_at)`. Migration (+45). **Không có ánh xạ ⇒ bỏ qua, không đoán theo thời gian** (REQ-016) |
| D3 | `bots.tutorial_exp_created_at` | MIGRATE / UPDATE | Migration `..._add_tutorial_exp_created_at_to_bots_table.php` (+32) — dùng để check bot đã có phiên trải nghiệm |
| D4 | **17 bảng seed 体験** | **DELETE (xóa cứng, trong 1 transaction)** | Theo bảng ánh xạ D2, thứ tự con-trước-cha; lỗi → rollback + retry ≤ 3. ⚠️ Studio **chỉ ghi số lượng 17**, chưa liệt kê tên bảng |
| D5 | `notify_setting` (CSV id seed) | UPDATE (detach) | ⚠️ **G3** — spec liệt "không xóa" |
| D6 | File QR / ảnh sinh lúc seed | DELETE (file trên server) | Best-effort sau commit; ⚠️ **RULE-08** — không kết luận từ local |
| D7 | Rich menu đã đăng ký trên LINE | DELETE (qua LINE API) | Best-effort; lỗi chỉ ghi log |
| D8 | `onboarding_sessions` (+ `webhook_url`) | CREATE / MIGRATE | Migration `..._create_onboarding_sessions_table.php` (+44), `..._add_webhook_url_to_onboarding_sessions_table.php` (+26) |
| D9 | **KHÔNG bị xóa**: `tag_history`, `detail_landing_click`, `landing_histories`, `auto_reply_history`, `detail_click_richmenu`, `tag_line_user` | (không thao tác) | ⚠️ **G1** — BR-C05 yêu cầu xóa nhưng implement KHÔNG xóa |
| D10 | **Đối chứng âm — phải còn nguyên**: `bots_tutorial`, cờ `has_tutorial`, trạng thái chat, cấu hình kết bạn, hồ sơ bot, liên kết user–bot, landing「テスト」, dữ liệu Admin tự tạo (kể cả trùng tên), bot khác + bot tenant khác | (không được chạm) | REQ-011 |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Màn 体験 (trải nghiệm) — wizard thêm bot bước 6, SCR-45→50 | F7, F8, D4 | **High** |
| T2 | **Toàn bộ wizard thêm bot** (các bước ngoài 体験) | F8 | **High** — Dev tự nêu cần smoke luồng thêm bot đầy đủ |
| T3 | Rich menu (đăng ký / gỡ trên LINE) | F9, D7 | **High** — RULE-08, cần env thật |
| T4 | Cấu hình thông báo `notify_setting` (của bot thật) | F10, D5 | **High** — xung đột spec G3 |
| T5 | Trải nghiệm phía LINE user (QR, 「エルメ体験」, form「アンケート」, trả lời tự động, rich menu) | D4, D7 | **High** — REQ-002: xóa vô điều kiện, LINE user đang dở bị dừng giữa chừng, không thông báo |
| T6 | 活用設定 / lối vào 体験 sau khi xóa | F6, D3 | **Medium** — REQ-007: không seed lại, không quay lại 体験; cờ `has_tutorial` vẫn bật |
| T7 | Job nền / hàng đợi `database` | F2, D1 | **Medium** — RULE-08 + retry / FAILED |
| T8 | Lịch sử & thống kê phiên trải nghiệm | D9 | **Medium** — G1, hành vi lệch spec |
| T9 | Cách ly tenant / phân quyền (bot của account khác) | F1 | **High** — REQ-009: 403 / 404 / 422 + chống giả mạo |

---

## 5. Requirements (nguồn: Studio #284 — 17 REQ)

<!-- KHÔNG có trong template gốc. Thêm vì Redmine không có spec; đây là input duy nhất để map coverage. -->

| REQ | Loại | Risk | Tiêu đề |
|---|---|---|---|
| REQ-001 | ui | High | Rời màn 体験 khi đang trải nghiệm thì data init bị xóa |
| REQ-002 | ui | High | Xóa vô điều kiện kể cả khi LINE user đã tương tác |
| REQ-003 | ui | Medium | Không cảnh báo, không xác nhận, không chặn điều hướng |
| REQ-004 | ui | High | Hành vi **KHÔNG** được tính là rời khu vực 体験 (chuyển bước ①〜⑤ trong cùng màn, đăng xuất) |
| REQ-005 | ui | High | Kết thúc trải nghiệm: bấm skip xóa ngay; hoàn tất Step 5 rồi rời trang cũng xóa |
| REQ-006 | validation | Medium | Không áp hạn tutorial 7 ngày |
| REQ-007 | ui | High | Sau khi xóa không tạo lại và không quay lại 体験 (cờ `has_tutorial` vẫn bật, FE không được dựa vào cờ này) |
| REQ-008 | api | High | EP-C01 chỉ ghi hàng đợi, trả 202, idempotent theo `tutorial_session_ref` |
| REQ-009 | permission | High | EP-C01 validation, phân quyền, cách ly tenant, chống giả mạo (422 / 403 / 404) |
| REQ-010 | job | High | Job xóa cứng đúng phạm vi seed trong 1 transaction, con-trước-cha, retry ≤ 3 |
| REQ-011 | data | High | **Đối chứng âm** — không chạm dữ liệu ngoài phạm vi (xem D10) |
| REQ-012 | job | High | Gỡ rich menu trên LINE + xóa file sau khi commit; lỗi chỉ ghi log |
| REQ-013 | job | High | Nhật ký đủ đối soát, không PII; **không có công tắc 3 nấc / dry_run** (→ G2) |
| REQ-014 | job | Medium | Tín hiệu **best-effort**: trượt tín hiệu ⇒ data init nằm lại vĩnh viễn, không có tiến trình dọn bù, không phát hiện được |
| REQ-015 | data | Medium | Hai bảng mới đúng cấu trúc + ràng buộc + index |
| REQ-016 | data | High | Nhận diện seed bằng **bảng ánh xạ**, không đoán theo thời gian |
| REQ-017 | data | Medium | Dọn tham chiếu `notify_setting` đúng mã seed + xóa file QR/ảnh |

---

## Leader xác nhận trước khi giao TCs

- [ ] ⚠️ **Đã yêu cầu Dev bổ sung "Đánh giá ảnh hưởng" lên Redmine #40153** (hiện chỉ có nguồn Studio)
- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller — ⚠️ **chưa có xác nhận của Dev**, đặc biệt `add_bot_v5.js` dùng chung toàn wizard
- [ ] Mục 4.1 không thiếu function
- [ ] Mục 4.2 không thiếu data (đặc biệt: **danh sách đầy đủ tên 17 bảng seed** — Studio chỉ ghi số lượng)
- [ ] Mục 4.3 cover được cả happy path lẫn edge case
- [ ] **G1 / G2 / G3 đã chốt với Dev + PM** (spec vs implement lệch → sửa spec hay sửa code?)
