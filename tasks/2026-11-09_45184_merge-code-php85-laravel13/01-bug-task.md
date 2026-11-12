# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45184 — Merge code php và laravel version cũ vào branch code đã nâng version php 8.5 và laravel 13` |
| Module / Màn hình | `Merge nhánh toàn hệ thống (không giới hạn 1 màn). Các module bị chạm theo Dev handoff: 広告連携設定 (Google/Meta Ads) · Huỷ hợp đồng & xoá tài khoản · API MCP form survey · Giới hạn nhập liệu Lesson/Salon/Form · Gỡ liên kết Google Calendar salon · Form · Broadcast V2 · Auto reply · CSV管理 · Univapay · Salon 予約設定 (メッセージ/キャンセル)` |

> ⚠️ Ticket này **KHÔNG phải bug** — là task kỹ thuật: merge code nhánh Laravel 5.5 cũ (release_staging_20261014_v3, thay cho nhánh release_staging_20260930_v3 ghi trong ticket nhưng không còn tồn tại trên repo) vào nhánh đã nâng cấp PHP 8.5 / Laravel 13 (release_staging_20261104). Không có Section "Tái hiện bug" trong Redmine — Steps/Expected/Actual dưới đây để trống.

## Mô tả bug (bản dịch tiếng Việt)

<!-- Nguyên văn description Redmine (đã là tiếng Việt, giữ nguyên không diễn giải). -->

1. branch code đã nâng version release_staging_20261104
2. code branch cũ release_staging_20260930_v3

Bước 1: Tách branch mới từ release_staging_20261104
Bước 2: Scan lại code cũ branch release_staging_20260930_v3 và branch mới tạo kiểm tra xem các task chưa được merge
Bước 3: Thực hiện merge code
Bước 4: Merge code xong cần test lại

## Steps to reproduce

<!-- N/A — không phải bug, không có steps to reproduce. -->

## Expected result

<!-- N/A -->

## Actual result

<!-- N/A -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine: Attachments (0) — không có đính kèm. -->

## Ghi chú thêm của Leader

- ⚠️ **Task nâng version PHP/Laravel/thư viện nền** — theo `CLAUDE.md`, khi review/viết TC cho task này phải đọc thêm [framework/php-upgrade-checklist.md](../../framework/php-upgrade-checklist.md) làm trục quét bổ sung (điểm nóng PHP8 A1–A6, lib nâng version, auth/mã hoá, 3 surface web/app/LINE user).
- Dev ghi rõ: **"Chưa kiểm được trên ứng dụng chạy thật"** (chỉ mới chạy bộ kiểm tĩnh/tự động, chưa QA runtime trên môi trường PHP 8.5 thật) — toàn bộ TC phải coi là **chưa có evidence thực thi**, RULE-11 áp dụng.
- Đội release **không bump** `config('sns-line.version')` trong lần merge này (dù đổi 35 file JS/CSS) — QA phải **Ctrl+F5** khi test, tránh báo nhầm bug do cache JS/CSS cũ.
- Deploy: **KHÔNG chạy `php artisan config:cache`** (runbook cấm) — chỉ reload PHP-FPM + `queue:restart` sau khi sửa `.env`.
- **Điểm nghi vấn chưa xử lý trong task này** (Dev chủ động mở ticket riêng, QA cần biết để không báo sai bug): luật validate của màn tin nhắn đặt lịch Salon (#41366) trên production đang bắt buộc nhập nội dung khi admin tick 「利用しない」 (cờ = 1) và KHÔNG bắt khi bật gửi — Dev cho rằng điều này **ngược chiều** với mô tả fix gốc của #41366, nhưng bản merge này **giữ nguyên hành vi production theo yêu cầu giữ spec** (không sửa trong task #45184). TC phải test theo hành vi production hiện tại (xem "Điểm cần test" ở file 03), không theo mô tả gốc #41366.
- Rủi ro xung đột tương lai: nhánh song song `merge_code_41389` / `ai-feature-41389` sửa cùng chỗ `@error` theo cách khác, có 7 commit mới hơn → có thể xung đột khi gộp sau task #45184 (ngoài phạm vi test task này, nhưng cần lưu ý nếu review code).
- Trước khi QA cần: chạy đủ 18 migration, set đủ biến môi trường (13 biến `.env` 広告連携: `GOOGLE_*`, `GOOGLE_ADS_*`, `META_*`, `ADS_TRACKING_DOMAIN`), và chạy worker `php artisan queue:work database_salon_google --queue=salonGoogleUnlink`.
- Lệnh `recover:ads_setting_permission` (gắn quyền 広告連携 cho 副管理人) **không rollback được** — phải backup `access_feature` + `bot_role_access` trước khi chạy trên môi trường thật.
- Lệnh `recover:main-card-token-univapay` chỉ chạy thử trong phạm vi task này; chạy thật với `--execute`/`--check-api` phải được người phụ trách #41762 duyệt riêng — KHÔNG test case verify execute trong task #45184.
- Route `basic/meta-review-test/*` (#41389, trang test Meta App Review) đi theo nhánh cũ — người phụ trách #41389 quyết có giữ trên production không, chưa chốt trong task này.
- Smoke-list riêng cho task này: `docs/upgrade/smoke-list.md` mục `#45184` — gồm 広告連携, huỷ hợp đồng và xoá tài khoản, Salon, giới hạn nhập liệu, Form, Broadcast V2, Auto reply, Google Calendar salon, Univapay test mode.

## Journal / note từ Redmine (nguyên văn)

**Journal #151325 — Dev Studio — 2026-11-05:**

```
Dev Studio · Nội dung thực hiện

Nhánh cũ ghi trong ticket (release_staging_20260930_v3) không có trên repo. Vì vậy thiết kế dùng release_staging_20261014_v3, nhánh Laravel 5.5 mới nhất và đã chứa mọi nhánh staging cũ. So với nhánh đã nâng cấp còn 210 nhóm task chưa merge, trong đó 54 task đã vào một phần. Gộp thử ra 10 file xung đột và một số chỗ code mới phải chuyển sang PHP 8.5 / Laravel 13. Kế hoạch gồm 7 bước: merge, giải xung đột, đối chiếu áp trùng, chuyển đổi code, sửa test, chạy bộ kiểm và cập nhật tài liệu deploy. Cần người xác nhận tên nhánh cũ nhưng việc đó không chặn thực thi.

Hướng sửa:
- D-1 Chuẩn bị: lấy SHA mới nhất hai nhánh, xác nhận nhánh cũ, cài vendor
- D-2 Commit merge --no-ff nhánh cũ và giải 10 file xung đột
- D-3 Đối chiếu từng dòng và kiểm áp trùng 54 ticket có ở cả hai nhánh
- D-4 Chuyển code mới sang PHP 8.5 / Laravel 13 theo bộ quét tools/upgrade
- D-5 Chỉnh khung PHPUnit 12 cho test mới của nhánh cũ
- D-6 Chạy bộ kiểm và so với kết quả trên base 3003323eae
- D-7 Cập nhật tài liệu upgrade: progress, deploy, smoke-list

Ảnh hưởng / rủi ro:
Phạm vi gồm mọi màn mà nhánh cũ chạm tới: 318 file, 18 migration, queue mới, API MCP form survey, tính năng Ads, huỷ hợp đồng, Salon, Form, Broadcast và Auto reply. Rủi ro chính là code mới đổi hành vi khi chạy trên PHP 8 / Laravel 13 (so sánh lỏng, count, catch, ngày giờ), và code có thể bị áp trùng ở 54 ticket đã vào nhánh mới theo đường khác. Cần chạy bộ kiểm tự động, sau đó QA trên môi trường PHP 8.5.
```

**Journal #151494 — Dev Studio — 2026-11-05:**

```
Dev Studio · Nội dung thực hiện

Thiết kế v2 sửa 2 lỗi review yêu cầu. Thứ nhất, khôi phục đúng nguyên văn production 2 bước kiểm của màn tin nhắn đặt lịch Salon mà bản gộp làm mất. Thay đổi của nhánh cũ vẫn giữ, và không áp kiểm này cho chế độ mới 「予約後のキャンセル不可」. Thứ hai, thêm 13 biến môi trường của 広告連携 vào tài liệu deploy, không dùng config:cache vì runbook cấm. Khi đọc code thấy luật kiểm trên production có vẻ ngược chiều công tắc 「利用しない」; theo yêu cầu giữ spec, bản này giữ nguyên và đề nghị mở ticket riêng. Còn lại là chạy lại bộ kiểm, gồm đối chiếu dòng production bị mất.

Hướng sửa:
- D-8 Khôi phục validate #41366 / #41365 của API lưu tin nhắn Salon và thêm test khoá hành vi
- D-9 Bổ sung 13 biến môi trường 広告連携 vào tài liệu deploy và ca QA vào smoke-list
- D-10 Chạy lại bộ kiểm, đối chiếu chiều ngược và cập nhật progress

Ảnh hưởng / rủi ro:
Code chỉ đổi một endpoint: API lưu cài đặt tin nhắn và huỷ lịch của Salon, kèm một file test mới. Phần tài liệu đổi gồm deploy.md, deploy-notes.md, smoke-list.md và progress.md. Rủi ro: luật kiểm khôi phục nguyên văn production nên giữ cả điểm nghi ngược chiều; cần test cả hai tab 予約 và キャンセル, gồm chế độ không cho huỷ mới của #39009.
```

**Journal #152119 — Dev Studio — 2026-11-06:**

```
Dev handoff — 06/11 14:16 · nhánh ai_studio_implement_45184

Tóm tắt:
Nhánh gộp toàn bộ code nhánh staging Laravel 5.5 (release_staging_20261014_v3) vào nhánh PHP 8.5 / Laravel 13. Phần code mới đã được chuyển để chạy trên phiên bản mới mà giữ nguyên nghiệp vụ, và 2 bước kiểm dữ liệu của màn tin nhắn đặt lịch Salon được khôi phục như production. Trước khi QA theo smoke-list mục #45184 cần chạy migration, đặt đủ biến môi trường và worker. Chưa kiểm được trên ứng dụng chạy thật.

Nội dung thay đổi:
- Các tính năng của nhánh 5.5 nay chạy trên bản Laravel 13: 広告連携設定 (Google/Meta Ads, link đo lường, 送信ログ), huỷ hợp đồng và xoá tài khoản, API MCP form survey, giới hạn nhập liệu Lesson/Salon/Form, gỡ liên kết Google Calendar salon; kèm các fix Form, Broadcast V2, Auto reply, CSV管理, Univapay.
- Màn Salon 予約設定 > メッセージ và キャンセル: có lại kiểm nội dung bắt buộc theo công tắc và giới hạn 5.000 ký tự (#41366), có lại kiểm câu hướng dẫn bắt buộc khi lịch có điều kiện lọc (#41365). Vẫn giữ kiểm riêng của màn キャンセル (#39009) và chặn sửa cấu hình của bot khác (#41426).
- Tài liệu deploy (deploy.md, deploy-notes.md, smoke-list.md) bổ sung migration, worker, lệnh, biến môi trường và ca QA của lần gộp.

File đã sửa (php-web):
  .../components/preview-action-video.blade.php      |   13 +
  .../text/preview-action-herme-outside.blade.php    |   20 +
  .../components/text/preview-action-herme.blade.php |   20 +
  .../cancellation/confirm_disconnect.blade.php      |   93 +
  .../components/csv_create_notice_modal.blade.php   |   59 +
  .../csv_management/create_download_file.blade.php  |    5 +-
  .../views/csv_management/csv_management.blade.php  |   11 +-
  resources/views/layout/admin/footer.blade.php      |    2 +
  resources/views/layout/admin/header.blade.php      |    7 +-
  resources/views/layout/admin_v2/header.blade.php   |    7 +-
  resources/views/layout/basic/header.blade.php      |    8 +-
  .../layout/modal_setting/label_action.blade.php    |   11 +
  .../modal_setting/modal_select_action.blade.php    |  159 ++
  .../no_bracket_label_action.blade.php              |   11 +
  resources/views/layout/v2/admin/header.blade.php   |    1 -
  resources/views/layout/v2/basic/header.blade.php   |    1 -
  resources/views/layout/v2/basic/sidebar.blade.php  |   23 +-
  resources/views/qr_code_open_pc.blade.php          |    4 +-
  routes/api.php                                     |   15 +
  routes/web.php                                     |   67 +-
  ...lendarSalonSaveSettingMessageValidationTest.php |  208 +++
  tests/Feature/FakeReplyFolderConnection.php        |  256 +++
  tests/Feature/FormAnswerIdorGuardTest.php          | 1885 ++++++++++++++++++++
  tests/Feature/RecountAppBadgeNotifyBatchTest.php   |    5 +-
  tests/Feature/ReplyFolderGuardTest.php             |  511 ++++++
  tests/Feature/ScreenInputLimitTest.php             |  106 ++
  tests/Unit/FormAnswerResultDataLimitTest.php       |   45 +
  .../AccountDeletionResendLimitMergeTest.php        |   75 +
  tests/Upgrade/RuntimeT23Test.php                   |    3 +-
  327 files changed, 30491 insertions(+), 1853 deletions(-)

Đánh giá ảnh hưởng — Rủi ro cao: Lần gộp đưa 326 file nghiệp vụ của nhánh 5.5 vào bản nâng cấp. Bộ kiểm tĩnh và test tự động cho kết quả bằng nhánh gốc, nhưng chưa test runtime trên môi trường PHP 8.5 thật.
- Mọi màn và API nhánh 5.5 chạm tới (326 file): đây là lần đầu code viết cho Laravel 5.5 chạy trên PHP 8.5, rủi ro ở khác biệt runtime như so sánh lỏng hay catch Throwable.
- Các chức năng ở 10 file giải xung đột cần test hồi quy: ngắt kết nối bot và webhook Univapay, xoá tài khoản, gửi tin ở トークリスト, chat 1:1 gắn tag và action, lưu filter ở CSV管理, auto reply và broadcast trên mobile, menu khoá học Salon.
- Bảng dùng chung có thay đổi: thêm cột ở calendar_setting_send_messages và calendar_salon_setting_send_messages, thêm t_actions_detail.bot_id, nới cột form_answer và form_answer_details.position.
- Queue mới database_salon_google dùng chung bảng jobs với các queue khác.

Migration / thay đổi dữ liệu:
- [Schema · Trước deploy] 18 migration của nhánh 5.5: bảng Ads, cột gửi tin huỷ cho admin, t_actions_detail.bot_id, nới cột form answer, thêm index — database/migrations/2026_09_18_100000_add_index_menu_status_to_mobile_notify_table.php: php artisan migrate:status; php artisan migrate --force
- [Config · Trước deploy] 13 biến .env của 広告連携 (GOOGLE_*, GOOGLE_ADS_*, META_*, ADS_TRACKING_DOMAIN) — docs/upgrade/deploy-notes.md: Chép giá trị từ .env của môi trường 5.5 sang .env của môi trường 8.5 theo danh sách trong deploy-notes.md. Chạy lệnh kiểm trong đó (chỉ in tên key thiếu), rồi reload PHP-FPM.
- [Hạ tầng · Khi deploy] Worker thường trực cho queue database_salon_google (gỡ liên kết Google Calendar salon): Thêm vào supervisor lệnh: php artisan queue:work database_salon_google --queue=salonGoogleUnlink
- [Dữ liệu · Sau deploy] Gắn quyền 広告連携 cho 副管理人 (access_feature và bot_role_access): php artisan recover:ads_setting_permission — không rollback được, backup: Dump hai bảng access_feature và bot_role_access trước khi chạy.

Lưu ý khi deploy:
- Nhánh gốc release_staging_20261104 đã có commit mới (8877b06f2c). Gộp thử không xung đột; khi đưa lên cần gộp vào bản mới nhất.
- Task không bump version trong config/sns-line.php; đội release bump khi phát hành, QA dùng Ctrl+F5.
- Không chạy php artisan config:cache (quy ước runbook nâng cấp). Sau khi sửa .env chỉ cần reload PHP-FPM và chạy queue:restart.
- Lệnh recover:main-card-token-univapay chỉ chạy thử. Chạy với --execute hoặc --check-api phải được người phụ trách #41762 duyệt.
- Route basic/meta-review-test/* (#41389, trang test Meta App Review) đi theo nhánh cũ; người phụ trách quyết có giữ trên production không.

Việc cần người làm thêm (ngoài phạm vi task):
- Mở ticket riêng xác minh luật #41366 trên production (màn tin nhắn Salon): code bắt buộc nhập nội dung khi admin tick 「利用しない」 (cờ = 1) và không bắt khi bật gửi, ngược với mô tả fix của #41366. Bằng chứng: evidence/design-v2/salon-flag-semantics.md của task #45184.
- Báo người phụ trách #41389: nhánh song song merge_code_41389 / ai-feature-41389 sửa cùng chỗ @error theo cách khác và có 7 commit mới hơn, nên sẽ xung đột với bản gộp này.
- Đội release bump config('sns-line.version') khi phát hành: bản gộp đổi 35 file JS/CSS nhưng giữ version của base; QA cần Ctrl+F5.
- Người phụ trách hạ tầng chép 13 biến môi trường 広告連携 từ .env môi trường Laravel 5.5 sang môi trường PHP 8.5 trước khi QA.
- Mở ticket riêng xem lại chiều của luật #41366. Trên production, tin nhắn đang bị bắt buộc nhập khi admin tick 「利用しない」 (cờ = 1), ngược với ghi chú của ticket. Vòng này giữ nguyên hành vi production theo yêu cầu giữ spec.
- Khi deploy môi trường PHP 8.5: chép 13 key 広告連携 từ .env môi trường 5.5 và chạy lệnh kiểm trong deploy-notes; không chạy config:cache.
- QA chạy các ca mới trong smoke-list mục #45184: tin nhắn đặt lịch Salon ở 2 tab 予約 / キャンセル, và 広告連携 khi thiếu key.
- Các việc của vòng 1 vẫn còn mở: xác nhận tên nhánh cũ, chạy 18 migration và worker salonGoogleUnlink, quyết định số phận route meta-review-test, chỉnh PHPUnit 12 cho 6 test đỏ sẵn trên base.
- Người phụ trách #41389: nhánh merge_code_41389 / ai-feature-41389 có commit #41389 mới hơn và sửa @error theo cách khác, nên sẽ xung đột khi gộp sau task này.
- Mở ticket riêng để xem lại chiều của luật bắt buộc nhập theo cờ is_send_message ở màn tin nhắn Salon (cờ 1 là 利用しない).
- Đội release bump version trong config/sns-line.php khi phát hành.

Điểm cần test:
- Salon → 予約設定 → メッセージ (自動承認): tick 「利用しない」 và xoá trắng 予約完了メッセージ, bấm 保存 ⇒ 422, hiện thông báo tiếng Nhật, nội dung cũ không bị ghi đè (đúng như production)
- Cùng màn: bỏ tick 「利用しない」, nội dung trống ⇒ lưu được (giống production); nội dung 5.001 ký tự ⇒ 422 「…は5000文字以内で入力してください。」
- Chế độ 手動承認: các ô リクエスト / 承認 / 否認 áp cùng luật theo cờ tương ứng
- Lịch có điều kiện lọc: xoá trắng 「予約ページの案内テキスト」 rồi lưu ⇒ 422; lịch không có điều kiện lọc ⇒ lưu được
- キャンセル設定: chế độ 予約後のキャンセル不可 lưu được dù ô 予約完了 (ẩn) trống; nội dung khối huỷ > 5.000 ký tự ⇒ 422; lưu khối huỷ không làm mất 「予約ページの案内テキスト」 (#41424)
- Gửi id cấu hình của bot khác ⇒ 404 「対象の設定が見つかりません。」
- Deploy: thiếu một trong 13 key 広告連携 thì lệnh kiểm trong deploy.md in đúng tên key; đủ key thì kết nối Google Ads / Meta và link đo lường chạy (chỉ dùng tài khoản test)
- Bộ kiểm trên HEAD mới bằng base: lint 0, phpstan 14 lỗi có sẵn, route 2673, tests/Upgrade xanh, file đỏ trùng danh sách base; đối chiếu chiều ngược không còn dòng production mất ngoài danh sách chủ ý
- Salon, tab 予約 của màn メッセージ: tick 利用しない rồi để trống nội dung thì bị chặn (giống production). Bỏ tick và để trống thì lưu được. Nội dung quá 5.000 ký tự thì bị chặn.
- Salon có cấu hình điều kiện lọc: để trống câu hướng dẫn 予約ページの非表示 thì bị chặn. Lịch không có điều kiện lọc thì để trống được.
- Salon, tab キャンセル, chế độ 予約後のキャンセル不可: không bị chặn vì ô đó ẩn. Nội dung quá 5.000 ký tự thì hiện lỗi. Lưu tab キャンセル không xoá câu hướng dẫn của tab 予約.
- Lưu cấu hình tin nhắn của bot khác (sửa id trong request) thì trả 404.
- Chạy smoke mục #45184 trong docs/upgrade/smoke-list.md (nhớ Ctrl+F5): 広告連携, huỷ hợp đồng và xoá tài khoản, Salon, giới hạn nhập liệu, Form, Broadcast V2, Auto reply, Google Calendar salon, Univapay test mode.

Branch: ai_studio_implement_45184
- sns-line: ai_studio_implement_45184 (nhánh gốc release_staging_20261104 @3003323eaee8, commit 51da3341673f25cad80ce953101a685c8413d1b6)
```
