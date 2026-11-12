# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio (AI dev-impact) — tác giả ticket: Do Van Tu TuDV` |
| Commit / Pull Request | `<chưa có PR link>` — commit: `f15ff4688c` (bug gốc #38562) · `198a07ab8b28` (bản giao #1, tối ưu N→2 query) · `31b77d952862` (bản giao #2, bỏ gọi đếm trùng khi xoá bạn, fix #43430 + bug automation #3285) |
| Branch | `ai_studio_fixbug_43378` (nhánh gốc `release_step_20260930_v2` @`d137c1851896`) |
| Ngày submit đánh giá | `2026-10-19` (bản giao #2, Journal #145255, 14:06) |
| Auto-filled | `2026-10-19 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

**Vòng 1 (job chạy chậm + retry lặp):**
Job `RecountAppBadgeNotify` chạy với `userId = null` (28/31 chỗ gọi) để đếm lại badge cho tất cả user của bot (chủ bot + `access_bot` + `notify_setting`). Code cũ chạy 1 câu `COUNT` trên `mobile_notify` **cho mỗi user**, điều kiện `user_id IS NULL OR user_id = X`. Notify dùng chung (`user_id = NULL`, phần lớn dữ liệu) bị quét lại N lần. Job không đặt `$timeout`, trong khi connection database có `retry_after = 600` (`config/queue.php:41`) — job chạy > 10 phút bị queue giao lại cho worker khác dù lần đầu chưa xong → chạy lặp mà không lần nào xong. Hàm `recountAppBadgeNotify()` được gọi từ ~31 chỗ nên job cùng 1 bot còn bị đẩy vào queue liên tục.

**Vòng 2 (phát hiện thêm khi bàn giao — nguyên nhân phụ, cùng ticket):**
Khi xoá 1 bạn bè, code gọi `recountAppBadgeNotify($botId)` **2 lần** trong cùng 1 request: lần 1 ngay sau khi xoá `mobile_notify` của bạn bè đó, lần 2 sau khi xoá lịch hẹn. Giữa 2 lần không ghi thêm `mobile_notify` nào → lần 2 chỉ đếm lại y hệt, nhân đôi tải đếm của bot. Lỗi có từ commit `#38562` (thay 2 đoạn tính badge cũ bằng `recountAppBadgeNotify` nhưng giữ nguyên cả 2 vị trí gọi). Redmine con #43430 và bug automation Test Studio #3285 báo cùng lỗi này; có 3 lối vào xoá 1 bạn bè cùng mắc.

## 2. Cách fix

**Vòng 1:** Cả bot chỉ còn 2 câu query thay cho N câu:
- Đếm notify dùng chung (`user_id IS NULL`) một lần.
- Đếm notify riêng bằng `WHERE user_id IN (...) GROUP BY user_id`.
- Badge mỗi user = số dùng chung + số riêng của user đó → tương đương toán học với cách đếm cũ (2 tập `user_id IS NULL` và `user_id = X` rời nhau).
- Thêm `MobileBadgeNotifyRepository::recountUnconfirmNotifyByUsers()`; tách bộ lọc chung (`bot_id`, `is_confirm=0`, `status=1`, loại trừ `type=1` chat 1:1 và `type=5` payment) vào `unconfirmNotifyQuery()`; `recountUnconfirmNotify()` cũ (đường 1 user, dùng ở `NotifyController` khi xác nhận thông báo trên app) dùng lại hàm lọc chung này, SQL không đổi.
- Khai báo hàm mới trong `MobileBadgeNotifyRepositoryInterface.php`; `RecountAppBadgeNotify::handle()` dùng hàm mới khi đếm cho cả bot. Lệnh `recover:mobileBadgeNotify` tự dùng đường đếm mới nên nhanh hơn theo.

**Vòng 2:** Bỏ lời gọi `recountAppBadgeNotify()` thứ 2 (sau khi xoá lịch hẹn) ở 3 lối vào xoá 1 bạn bè — mỗi lần xoá giờ chỉ đẩy đúng 1 job:
- `FriendlistController::deleteUserBlock` — nút 「削除」 từng dòng ở 「ブロックされた友だち」.
- `FriendlistController::updateLineUser` — xoá bạn ở trang chi tiết bạn bè / 1:1 chat.
- `Api\FriendInformationController::deleteFriend` — API xoá bạn bè app mobile (request/response không đổi).
- Xoá hàng loạt (`deleteUserBlockAction`) không đổi, vẫn 1 lời gọi (không bị lỗi này).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `MobileBadgeNotifyRepositoryInterface.php` | +10 dòng — khai báo `recountUnconfirmNotifyByUsers()` | Interface cho hàm đếm theo lô mới |
| 2 | `app/Repositories/Eloquents/MobileBadgeNotifyRepository.php` | +47 dòng — thêm `recountUnconfirmNotifyByUsers()` + tách `unconfirmNotifyQuery()`; `recountUnconfirmNotify()` cũ dùng lại hàm lọc chung | Giảm N query → 2 query cho cả bot, không đổi SQL đường 1 user |
| 3 | `app/Jobs/RecountAppBadgeNotify.php` | +12/-? dòng — `handle()` dùng hàm đếm theo lô khi `userId = null` | Điểm vào chính của job |
| 4 | `app/Http/Controllers/Api/FriendInformationController.php` (`deleteFriend`) | -1 dòng — bỏ lời gọi `recountAppBadgeNotify()` thứ 2 | Fix #43430/#3285 — tránh đếm trùng khi xoá bạn qua API app |
| 5 | `app/Http/Controllers/Basic/FriendlistController.php` (`deleteUserBlock`, `updateLineUser`) | -2 dòng — bỏ lời gọi `recountAppBadgeNotify()` thứ 2 ở 2 hàm | Fix #43430/#3285 — tránh đếm trùng khi xoá bạn ở web |
| 6 | `tests/Feature/RecountAppBadgeNotifyBatchTest.php` | +227 dòng (file mới) | Test dev: số câu query/SQL + kiểm chứng ngược công thức. **Chưa verify runtime trên MySQL thật** |
| 7 | `recover:mobileBadgeNotify` (Artisan command) | Không sửa code — tự dùng đường đếm mới vì gọi lại `(new RecountAppBadgeNotify($botId))->handle()` cho mọi bot `is_deleted=0` | Lệnh vận hành chạy nhanh hơn theo |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `MobileBadgeNotifyRepository::recountUnconfirmNotifyByUsers()` (mới) | `MobileBadgeNotifyRepository.php` | Direct | 2 query cho cả bot: COUNT dùng chung + COUNT GROUP BY user_id riêng |
| F2 | `MobileBadgeNotifyRepository::unconfirmNotifyQuery()` (mới, bộ lọc chung) | `MobileBadgeNotifyRepository.php` | Direct | `bot_id`, `is_confirm=0`, `status=1`, loại `type=1` (chat 1:1), `type=5` (payment) |
| F3 | `MobileBadgeNotifyRepository::recountUnconfirmNotify()` (đường 1 user, giữ cũ) | `MobileBadgeNotifyRepository.php` | Direct | Refactor dùng lại F2, SQL sinh ra **không đổi** — dùng khi xác nhận thông báo qua app (`NotifyController`) |
| F4 | `RecountAppBadgeNotify::handle()` | `app/Jobs/RecountAppBadgeNotify.php` | Direct | Nhánh `userId = null` (cả bot) chuyển sang F1; nhánh `userId != null` (1 user) vẫn gọi F3 |
| F5 | Helper `recountAppBadgeNotify()` | `app/Helpers/functions.php` | Indirect | **Không sửa** — vẫn dispatch job qua connection database/queue default; comment cũ ("1 câu COUNT/user") chưa cập nhật (ngoài phạm vi) |
| F6 | `Api\FriendInformationController::deleteFriend` | `FriendInformationController.php` | Direct | Bỏ lời gọi đếm lại thứ 2 — xoá bạn qua app mobile |
| F7 | `Basic\FriendlistController::deleteUserBlock` | `FriendlistController.php` | Direct | Bỏ lời gọi đếm lại thứ 2 — nút 「削除」 ở 「ブロックされた友だち」 |
| F8 | `Basic\FriendlistController::updateLineUser` | `FriendlistController.php` | Direct | Bỏ lời gọi đếm lại thứ 2 — xoá bạn ở trang chi tiết bạn bè / 1:1 chat |
| F9 | `Basic\FriendlistController::deleteUserBlockAction` (xoá hàng loạt) | `FriendlistController.php` | Indirect | **Không đổi** — vẫn 1 lời gọi, không mắc lỗi vòng 2 |
| F10 | Artisan `recover:mobileBadgeNotify` | (command, không đổi code) | Indirect | Tự dùng F4/F1 mới → chạy nhanh hơn, idempotent |
| F11 | ~28 chỗ gọi `recountAppBadgeNotify($botId)` khác (Booking/Salon/Lesson, `通知設定`, API Notify, Admin Bot, `HandlePushMessageNotify`) | rải nhiều file | Indirect | Không sửa, chỉ hưởng lợi tốc độ từ F1/F4 — Dev yêu cầu kiểm badge sau các thao tác này |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `mobile_badge_noitfy.count_app_notify` | UPDATE (qua `setCount()`, không đổi cách ghi) | Giá trị phải **giống cách đếm cũ** cho mọi user (chủ bot/staff/notify_setting). Rủi ro Dev tự nêu: lệch do key mảng `user_id` kiểu string/int từ PDO, user có notify riêng nhưng không có notify chung… |
| D2 | `jobs` / `failed_jobs` table | — (quan sát) | Trước fix: job `RecountAppBadgeNotify` có thể kẹt/lặp (`attempts` tăng dần) cho bot lớn. Sau fix: chạy xong 1 lần, không còn dòng kẹt. Job đã nằm trong queue trước deploy vẫn chạy bằng code mới (payload chỉ có `botId`/`userId`) sau khi worker restart |
| D3 | `mobile_badge_noitfy_bk_43378` (bảng backup, **MIGRATION thủ công sau deploy**) | CREATE | `CREATE TABLE mobile_badge_noitfy_bk_43378 AS SELECT * FROM mobile_badge_noitfy;` — backup trước khi chạy recover |
| D4 | Log `[action=recount][entity=MobileBadgeNotify]` | CREATE (log, không đổi format) | Phải có đủ 1 dòng/user sau mỗi lần job chạy; xoá 1 bạn ở bot có N user → N dòng log (không phải N job) |

**Recover dữ liệu (vận hành, sau deploy — BẮT BUỘC):**
- Lý do: trước fix, nếu job không chạy xong thì `mobile_badge_noitfy.count_app_notify` giữ số cũ (sai) cho tới lần đếm lại thành công tiếp theo. `mobile_notify` gốc vẫn đúng → đếm lại được, **không mất dữ liệu**.
- Khoảng thời gian ảnh hưởng: từ khi deploy bản có commit `f15ff4688c` (#38562, có trong `release_step_20260805` trở đi) tới khi bản sửa này chạy.
- Lệnh recover: `php artisan recover:mobileBadgeNotify` (idempotent, chạy lại không đổi số, mỗi bot chỉ tốn 2 câu sau fix).
- Không ảnh hưởng khách hàng — không gửi tin, chỉ số badge admin/staff đổi về đúng.
- ⚠️ Riêng lỗi "gọi đếm trùng 2 lần khi xoá bạn" (vòng 2) **không cần recover** — badge cuối cùng vẫn đúng, chỉ thừa 1 lần đếm lãng phí tài nguyên.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Badge thông báo app mobile (số đếm hiển thị) — toàn bộ các action trigger recount (xoá bạn, booking/salon/lesson, `通知設定`, admin bot, API Notify/FriendInformation) | F1–F4, D1 | High — sai công thức đếm ảnh hưởng mọi nghiệp vụ dùng job này |
| T2 | Xoá 1 bạn bè — 3 lối vào: `ブロックされた友だち` (削除 từng dòng), trang chi tiết bạn bè/1:1 chat, API app mobile | F6, F7, F8 | Medium — phải còn đúng 1 job/log 2 dòng (bot 2 user), không về lại 2 job; lịch hẹn kèm theo (calendar/salon/lesson) vẫn phải xoá đúng |
| T3 | Xoá hàng loạt bạn bè ở `ブロックされた友だち` | F9 (không đổi) | Low — hồi quy: vẫn chỉ 1 job như trước |
| T4 | Xác nhận thông báo trên app mobile (đường 1 user) | F3, F4 (nhánh `userId != null`) | Medium — chỉ badge của user thao tác được đổi, badge user khác của bot không đổi |
| T5 | Vận hành queue/jobs (RecountAppBadgeNotify không còn kẹt/retry lặp trên production) | F4, D2 | High ở quy mô production — **chưa verify runtime trên MySQL thật**, job vẫn chưa có `$timeout`/chống dispatch trùng (theo Dev, ngoài phạm vi ticket) |
| T6 | Lệnh vận hành `recover:mobileBadgeNotify` (chạy sau deploy) | F10, D3 | Medium — phải chạy hết, idempotent, không đụng bot đã xoá (`is_deleted=0`) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

> ⚠️ Lưu ý riêng: 31 chỗ gọi `recountAppBadgeNotify()` — Dev chỉ sửa 3 (xoá 1 bạn bè). 28 chỗ còn lại (Booking/Salon/Lesson, `通知設定`, API Notify/FriendInformation, Admin Bot, `HandlePushMessageNotify`) không sửa code nhưng **đổi đường tính** (từ N query sang F1) — Leader cân nhắc phạm vi regression khi duyệt TC ở `/review-tc` BƯỚC 3a (quét theo bảng "Coverage theo màn hình/chức năng", không chỉ lọc theo diff).
> ⚠️ Chưa verify runtime trên MySQL thật (test dev dùng connection giả) — `/review-tc` nên ưu tiên RISK ở các TC chạy trên DB thật (staging/prd) cho T1/T5.
