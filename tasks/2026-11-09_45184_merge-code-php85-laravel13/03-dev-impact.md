# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT KHÔNG THEO FORMAT CHUẨN 4 MỤC** — Redmine #45184 không có section "Đánh giá ảnh hưởng" dạng 1./2./3./4. thông thường (ticket là task merge/upgrade nhánh, không phải bug fix). Nội dung dưới đây được **tổng hợp lại** (không bịa thêm) từ 3 journal "Dev Studio" trong file `01-bug-task.md` (#151325 ngày 2026-11-05, #151494 ngày 2026-11-05, #152119 — Dev handoff final ngày 2026-11-06). Journal #152119 là bản đầy đủ nhất, các mục bên dưới ưu tiên lấy từ journal này; 2 journal trước giữ vai trò lịch sử thiết kế (v1 → v2). **Tester BẮT BUỘC đọc lại nguyên văn 3 journal ở file 01 trước khi tick checkbox verify.**

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio (journal author — issue.assigned_to rỗng trên Redmine)` |
| Commit / Pull Request | `<không có link PR>` — base `3003323eaee8` (nhánh gốc `release_staging_20261104`), commit merge `51da3341673f25cad80ce953101a685c8413d1b6` |
| Branch | `ai_studio_implement_45184` (nguồn: `release_staging_20261104` @`3003323eaee8` ← merge `release_staging_20261014_v3`, thay cho `release_staging_20260930_v3` ghi trong ticket — nhánh này không tồn tại trên repo) |
| Ngày submit đánh giá | `2026-11-06` (journal #152119 — handoff final) |
| Auto-filled | `2026-11-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại nguyên văn 3 journal ở `01-bug-task.md` và xác nhận tổng hợp dưới đây không sót/sai lệch ý Dev.

---

## 1. Nguyên nhân

<!-- Task merge/upgrade — không có "nguyên nhân bug", đây là lý do phải thực hiện merge. -->

Nhánh code đã nâng cấp PHP 8.5 / Laravel 13 (`release_staging_20261104`) **chưa có** phần code nghiệp vụ của nhánh Laravel 5.5 cũ. Theo Dev (journal #151325):

> "Nhánh cũ ghi trong ticket (release_staging_20260930_v3) không có trên repo. Vì vậy thiết kế dùng release_staging_20261014_v3, nhánh Laravel 5.5 mới nhất và đã chứa mọi nhánh staging cũ. So với nhánh đã nâng cấp còn **210 nhóm task chưa merge**, trong đó **54 task đã vào một phần**."

→ Rủi ro gốc: 54 task đã merge một phần → nguy cơ **áp trùng code** (double-apply) khi merge toàn bộ nhánh cũ vào.

## 2. Cách fix

<!-- "Cách fix" = cách thực hiện merge, theo kế hoạch D-1 → D-10 của Dev (v1 + v2). -->

**V1 (journal #151325) — kế hoạch 7 bước:**
- D-1 Chuẩn bị: lấy SHA mới nhất 2 nhánh, xác nhận nhánh cũ, cài vendor
- D-2 Commit `merge --no-ff` nhánh cũ, giải **10 file xung đột**
- D-3 Đối chiếu từng dòng + kiểm áp trùng **54 ticket** có ở cả 2 nhánh
- D-4 Chuyển code mới sang PHP 8.5 / Laravel 13 theo bộ quét `tools/upgrade`
- D-5 Chỉnh khung PHPUnit 12 cho test mới của nhánh cũ
- D-6 Chạy bộ kiểm, so với kết quả trên base `3003323eae`
- D-7 Cập nhật tài liệu upgrade: progress, deploy, smoke-list

**V2 (journal #151494) — sửa 2 lỗi review:**
- D-8 Khôi phục nguyên văn production **2 bước kiểm** của màn tin nhắn đặt lịch Salon (#41366 / #41365) mà bản gộp đầu làm mất + thêm test khoá hành vi. **Không** áp kiểm này cho chế độ mới 「予約後のキャンセル不可」.
- D-9 Bổ sung **13 biến môi trường** 広告連携 vào tài liệu deploy + ca QA vào smoke-list (không dùng `config:cache` vì runbook cấm)
- D-10 Chạy lại bộ kiểm, đối chiếu chiều ngược, cập nhật progress
- Dev ghi nhận: luật kiểm production có vẻ **ngược chiều** công tắc 「利用しない」 — theo yêu cầu giữ spec, **giữ nguyên hành vi hiện tại**, đề nghị mở ticket riêng xem lại (KHÔNG sửa trong task này).

**Kết quả cuối (journal #152119 — Dev handoff):**
> "Nhánh gộp toàn bộ code nhánh staging Laravel 5.5 (release_staging_20261014_v3) vào nhánh PHP 8.5 / Laravel 13. Phần code mới đã được chuyển để chạy trên phiên bản mới mà giữ nguyên nghiệp vụ, và 2 bước kiểm dữ liệu của màn tin nhắn đặt lịch Salon được khôi phục như production."

Quy mô diff cuối: **327 files changed, 30491 insertions(+), 1853 deletions(-)**. Bộ kiểm tĩnh/tự động cho kết quả bằng nhánh gốc, nhưng **chưa test runtime trên môi trường PHP 8.5 thật**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê "Các chức năng ở 10 file giải xung đột cần test hồi quy" (journal #152119). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Ngắt kết nối bot & webhook Univapay | File trong số 10 file giải xung đột | Merge trùng điểm sửa giữa 2 nhánh → cần test hồi quy sau giải xung đột |
| 2 | Xoá tài khoản (account deletion) | nt | nt |
| 3 | Gửi tin ở トークリスト (talk list) | nt | nt |
| 4 | Chat 1:1 — gắn tag và action | nt | nt |
| 5 | Lưu filter ở CSV管理 | nt | nt |
| 6 | Auto reply và broadcast trên mobile | nt | nt |
| 7 | Menu khoá học Salon | nt | nt |
| 8 | API lưu cài đặt tin nhắn + huỷ lịch Salon (`CalendarSalonSaveSettingMessageValidationTest`) | Khôi phục validate #41366/#41365 (D-8) | Bản gộp v1 làm mất 2 bước kiểm production |
| 9 | 54 ticket đã merge một phần vào nhánh đích theo đường khác | Đối chiếu từng dòng (D-3) | Nguy cơ áp trùng (double-apply) code |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | 広告連携設定 (Google/Meta Ads, link đo lường, 送信ログ) | theo diff nhánh 5.5 (326 file nghiệp vụ) | Direct | Lần đầu chạy trên PHP 8.5/Laravel 13; phụ thuộc 13 biến `.env` (xem D2) |
| F2 | Huỷ hợp đồng và xoá tài khoản | `tests/Feature/.../AccountDeletionResendLimitMergeTest.php` + liên quan | Direct | |
| F3 | API MCP form survey | — | Direct | Theo `CLAUDE.md`: caller dùng chung filter web/app/MCP — cần kiểm cả 3 surface |
| F4 | Giới hạn nhập liệu Lesson/Salon/Form | `tests/Feature/ScreenInputLimitTest.php`, `FormAnswerResultDataLimitTest.php` | Direct | |
| F5 | Gỡ liên kết Google Calendar salon | queue `database_salon_google` | Direct | Cần worker riêng (xem D6) |
| F6 | Salon 予約設定 > メッセージ/キャンセル — validate theo cờ 利用しない (#41366), câu hướng dẫn bắt buộc khi có điều kiện lọc (#41365), chế độ 予約後のキャンセル不可 (#39009), chặn sửa config bot khác (#41426) | `CalendarSalonSaveSettingMessageValidationTest.php` | Direct | **Có điểm nghi vấn chiều luật #41366** — xem Ghi chú thêm |
| F7 | Form / Broadcast V2 / Auto reply / CSV管理 / Univapay (regression qua 10 file xung đột) | `FormAnswerIdorGuardTest.php`, `ReplyFolderGuardTest.php`, `FakeReplyFolderConnection.php` | Indirect | Cộng dồn với mục 3 |
| F8 | UI dùng chung: header/footer/sidebar (admin, admin_v2, basic, v2), modal chọn action (`modal_select_action.blade.php` +159 dòng), label action | `resources/views/layout/**`, `modal_setting/**` | Indirect | Ảnh hưởng mọi màn render qua layout chung — rủi ro UI-wide regression |
| F9 | Route mới | `routes/api.php` (+15), `routes/web.php` (+67) | Direct | |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `calendar_setting_send_messages`, `calendar_salon_setting_send_messages` | MIGRATE (thêm cột) | 1 trong 18 migration nhánh 5.5 |
| D2 | `t_actions_detail.bot_id` | MIGRATE (thêm cột) | |
| D3 | `form_answer`, `form_answer_details.position` | MIGRATE (nới độ dài cột) | |
| D4 | Bảng Ads (mới), index `mobile_notify` (`2026_09_18_100000_add_index_menu_status_to_mobile_notify_table.php`) | CREATE / MIGRATE | Tổng 18 migration — chạy trước deploy: `php artisan migrate:status` rồi `migrate --force` |
| D5 | 13 biến `.env` 広告連携 (`GOOGLE_*`, `GOOGLE_ADS_*`, `META_*`, `ADS_TRACKING_DOMAIN`) | CONFIG — copy từ env Laravel 5.5 sang env PHP 8.5 | Thiếu key → lệnh kiểm trong `deploy-notes.md` phải in đúng tên key thiếu |
| D6 | Queue `database_salon_google` (dùng chung bảng `jobs`) | CREATE (queue mới) | Cần worker: `queue:work database_salon_google --queue=salonGoogleUnlink` |
| D7 | `access_feature`, `bot_role_access` | UPDATE (`php artisan recover:ads_setting_permission` — gắn quyền 広告連携 cho 副管理人) | **Không rollback được** — phải backup (dump) 2 bảng trước khi chạy |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | 広告連携設定 (Ads) | F1, D5, D7 | High — lần đầu chạy PHP 8.5; thiếu env key hoặc permission chưa gắn sẽ lỗi toàn bộ |
| T2 | Huỷ hợp đồng / xoá tài khoản | F2 | High |
| T3 | API MCP form survey | F3 | Medium — kiểm thêm surface `mcp` theo [feedback MCP shares mobile filter] |
| T4 | Giới hạn nhập liệu Lesson/Salon/Form | F4 | Medium |
| T5 | Gỡ liên kết Google Calendar salon | F5, D6 | Medium — phụ thuộc worker chạy đúng |
| T6 | Salon 予約設定 (メッセージ/キャンセル) | F6 | High — có điểm nghi vấn chiều luật, phải test đúng theo hành vi **production hiện tại**, không theo mô tả gốc #41366 |
| T7 | Form / Broadcast V2 / Auto reply / CSV管理 / Univapay | F7 | High — rủi ro áp trùng 54 ticket + runtime PHP 8.5 (so sánh lỏng, count, catch Throwable, ngày giờ) |
| T8 | UI chung (header/footer/sidebar/modal action) toàn hệ thống | F8 | Medium — 35 file JS/CSS đổi nhưng KHÔNG bump version → QA phải Ctrl+F5 |

---

## Ghi chú thêm từ Dev (ngoài 4 mục chuẩn — quan trọng cho việc viết TC)

### Điểm cần test (nguyên văn Dev, journal #152119)

- Salon → 予約設定 → メッセージ (自動承認): tick 「利用しない」 + xoá trắng 予約完了メッセージ, bấm 保存 ⇒ 422, thông báo tiếng Nhật, nội dung cũ không bị ghi đè (đúng production)
- Cùng màn: bỏ tick 「利用しない」, nội dung trống ⇒ lưu được; nội dung 5.001 ký tự ⇒ 422 「…は5000文字以内で入力してください。」
- Chế độ 手動承認: ô リクエスト / 承認 / 否認 áp cùng luật theo cờ tương ứng
- Lịch có điều kiện lọc: xoá trắng 「予約ページの案内テキスト」 rồi lưu ⇒ 422; lịch không có điều kiện lọc ⇒ lưu được
- キャンセル設定, chế độ 予約後のキャンセル不可: lưu được dù ô 予約完了 (ẩn) trống; nội dung khối huỷ > 5.000 ký tự ⇒ 422; lưu khối huỷ không mất 「予約ページの案内テキスト」 (#41424)
- Gửi id cấu hình của bot khác ⇒ 404 「対象の設定が見つかりません。」
- Deploy: thiếu 1 trong 13 key 広告連携 → lệnh kiểm `deploy.md` in đúng tên key; đủ key → Google Ads/Meta + link đo lường chạy (chỉ dùng tài khoản test)
- Bộ kiểm trên HEAD mới = base: lint 0, phpstan 14 lỗi có sẵn (không tăng), route 2673, `tests/Upgrade` xanh, file đỏ trùng danh sách base; đối chiếu chiều ngược không còn dòng production mất ngoài danh sách chủ ý
- Chạy smoke mục #45184 trong `docs/upgrade/smoke-list.md` (nhớ Ctrl+F5): 広告連携, huỷ hợp đồng/xoá tài khoản, Salon, giới hạn nhập liệu, Form, Broadcast V2, Auto reply, Google Calendar salon, Univapay test mode.

### Rủi ro / việc mở (không thuộc phạm vi fix của task #45184 — chỉ để QA biết, KHÔNG test như bug)

- **#41366 chiều luật nghi ngược**: production bắt buộc nhập khi cờ `is_send_message` = 1 (利用しない), không bắt khi bật gửi — ngược mô tả gốc #41366. Task này **giữ nguyên** theo production. Dev đã mở ghi chú `evidence/design-v2/salon-flag-semantics.md`. → Không báo bug nếu TC thấy hành vi này; nếu Leader muốn đổi lại thì phải ticket riêng.
- **Xung đột tương lai #41389**: nhánh song song `merge_code_41389`/`ai-feature-41389` sửa cùng chỗ `@error` theo cách khác, 7 commit mới hơn → sẽ xung đột khi gộp sau. Không ảnh hưởng test task #45184 hiện tại.
- Route `basic/meta-review-test/*` (#41389) — số phận chưa chốt, đi theo nhánh cũ.
- Việc còn mở từ vòng 1: xác nhận tên nhánh cũ, chạy 18 migration + worker `salonGoogleUnlink`, chỉnh PHPUnit 12 cho 6 test đỏ sẵn có trên base (không phải lỗi mới).
- `recover:main-card-token-univapay`: chỉ chạy thử trong task này, chạy thật (`--execute`/`--check-api`) cần người phụ trách #41762 duyệt — KHÔNG viết TC verify execute thật trong task #45184.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
