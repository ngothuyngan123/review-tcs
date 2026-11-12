# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43378 — RecountAppBadgeNotify bị chậm retry nhiều lần không được` |
| Module / Màn hình | Job nền `RecountAppBadgeNotify` (đếm lại badge thông báo app) — gọi từ ~31 chỗ: xoá bạn bè (`ブロックされた友だち`, trang chi tiết bạn bè, API app mobile), đặt/huỷ lịch hẹn Booking/Salon/Lesson, lưu `通知設定` (cài đặt thông báo), API Notify/FriendInformation, Admin Bot, `HandlePushMessageNotify`, lệnh `recover:mobileBadgeNotify`. |

## Mô tả bug (bản dịch tiếng Việt)

1. Nguyên nhân — Vì sao chậm và bị chạy lại nhiều lần

- Job này chạy với `userId = null`, tức là đếm lại badge cho tất cả user của bot. Danh sách user gồm chủ bot, các user trong `access_bot` và các user trong `notify_setting`.
- Code cũ ở `RecountAppBadgeNotify.php` chạy một câu COUNT trên `mobile_notify` cho mỗi user. Mỗi câu có điều kiện `user_id IS NULL OR user_id = X`. Vì vậy các notify dùng chung (`user_id = NULL`), thường là phần lớn số notify, bị quét lại N lần. Bot nào có nhiều notify chưa xác nhận và nhiều user thì job chạy rất lâu.
- Connection database có `retry_after = 600` (`config/queue.php:41`). Job chạy quá 10 phút thì queue coi là đã chết và giao lại cho worker khác, trong khi lần chạy đầu vẫn chưa xong. Đó là lý do job bị chạy lại nhiều lần mà không lần nào xong. Ngoài ra hàm `recountAppBadgeNotify()` được gọi từ khoảng 30 chỗ (xoá bạn bè, huỷ lịch hẹn…), nên job cho cùng một bot còn bị đẩy vào queue liên tục.

2. Cách fix

- Giờ cả bot chỉ cần 2 câu query thay cho N câu:
  - Đếm notify dùng chung (`user_id IS NULL`) một lần.
  - Đếm notify riêng bằng `WHERE user_id IN (...) GROUP BY user_id`.
  - Badge của mỗi user bằng số dùng chung cộng với số riêng của user đó, nên kết quả giống cách đếm cũ.
- `MobileBadgeNotifyRepository.php`: thêm hàm `recountUnconfirmNotifyByUsers()`. Các điều kiện lọc chung được tách ra hàm `unconfirmNotifyQuery()`, và `recountUnconfirmNotify()` cũ dùng lại hàm này.
- `MobileBadgeNotifyRepositoryInterface.php`: khai báo hàm mới.
- `RecountAppBadgeNotify.php`: dùng hàm mới. Lệnh `recover:mobileBadgeNotify` gọi lại job này nên cũng nhanh hơn theo.

> Bản giao thứ 2 (19/10, nhánh `ai_studio_fixbug_43378`): phát hiện thêm nguyên nhân phụ — khi xoá 1 bạn bè, code gọi `recountAppBadgeNotify($botId)` **2 lần** trong cùng 1 request (lần đầu sau khi xoá `mobile_notify` của bạn bè, lần sau khi xoá lịch hẹn) dù giữa 2 lần không ghi thêm `mobile_notify` nào → nhân đôi tải đếm. Lỗi có từ commit `#38562`. Đã bỏ lời gọi thứ 2 ở 3 lối vào xoá 1 bạn bè (`FriendlistController::deleteUserBlock`, `FriendlistController::updateLineUser`, `Api\FriendInformationController::deleteFriend`). Xem chi tiết đầy đủ ở Journal #145255 bên dưới + `03-dev-impact.md`.

## Steps to reproduce

1. _(không có trong Redmine — bug được Dev tự phát hiện qua review hiệu năng job, không phải báo lỗi tái hiện theo thao tác cụ thể)_

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

(Redmine #43378 không có attachment.)

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được theo kiểu "Steps to reproduce" thông thường — đây là bug performance/job nền do Dev tự phát hiện (AI detect performance) và tự submit đánh giá ảnh hưởng + cách fix. TCs nên tập trung verify: (a) kết quả đếm badge sau fix giống cách đếm cũ (tương đương toán học), (b) job không còn chạy lặp/kẹt với bot lớn, (c) không còn gọi đếm lại trùng 2 lần khi xoá 1 bạn bè, (d) lệnh `recover:mobileBadgeNotify` chạy đúng + idempotent.

- Branch: `ai_studio_fixbug_43378` (gốc `release_step_20260930_v2` @`d137c1851896`).
- Bug con liên quan cùng gốc: Redmine #43430 (đã sửa cùng branch, commit `31b77d952862`) và bug automation Test Studio #3285 (đã sửa).
- Môi trường cần recover sau deploy: bản 1 (tối ưu N→2 query) **cần recover dữ liệu**; bản 2 (bỏ lời gọi trùng khi xoá bạn) **không cần recover** (badge cuối vẫn đúng, chỉ thừa 1 lần đếm).
- Status Redmine hiện tại: "Fix done - Đợi test" (digest `/new-task` fetch lúc 2026-10-19; trên Studio context trả `"Đang fix"` — có thể do cache, Tester verify lại trạng thái mới nhất trên Redmine khi cần).
- MCP LME TEST STUDIO đã có task #469 (feature `notify-setting`) với 37 TC do AI + `haodtb@mcp` viết, `aiResult=pass`, đã chạy ở env `staging` (chưa chạy `prd`) — xem `04-tc-list.md`.

## Dữ liệu định danh ca lỗi

_(Không có ca lỗi cụ thể — bug phát hiện qua review hiệu năng job, không gắn với 1 bot/friend/thời điểm cụ thể nào. Bỏ section.)_

## Journal / note từ Redmine (nguyên văn)

**Journal #145008 — Dev Studio — 2026-10-18:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Khi gọi theo cả bot (userId = null, 28/31 chỗ gọi), job RecountAppBadgeNotify chạy một câu COUNT trên mobile_notify cho mỗi user của bot. Điều kiện là user_id IS NULL OR user_id = X, nên toàn bộ notify dùng chung (user_id NULL, phần lớn dữ liệu) bị quét lại N lần. Job không đặt $timeout, còn connection database có retry_after = 600. Lần chạy dài hơn 10 phút bị giao lại cho worker khác khi lần đầu chưa xong, nên job chạy lặp lại mà không lần nào xong.

Hướng sửa:
- D-1 Thêm hàm đếm badge theo lô cho nhiều user và tách bộ lọc chung trong MobileBadgeNotifyRepository
- D-2 Khai báo hàm mới trong MobileBadgeNotifyRepositoryInterface
- D-3 RecountAppBadgeNotify::handle dùng hàm đếm theo lô khi đếm cho cả bot
- D-4 Recover: lệnh recover:mobileBadgeNotify tự dùng đường đếm mới, không sửa code

Ảnh hưởng / rủi ro:
Chỉ thay đổi cách job RecountAppBadgeNotify đếm badge; 31 chỗ gọi recountAppBadgeNotify() và công thức badge giữ nguyên. Rủi ro chính là số badge lệch so với cách cũ, nên cần so sánh số đếm từng user giữa cách cũ và cách mới.
```

**Journal #145185 — Do Van Tu TuDV — 2026-10-19:**

```
branch code: ai_studio_fixbug_43378
```

**Journal #145239 — Dev Studio — 2026-10-19:**

```
Dev handoff — 19/10 12:00 · nhánh ai_studio_fixbug_43378

Nguyên nhân:
Khi gọi theo cả bot (userId = null, 28/31 chỗ gọi), job RecountAppBadgeNotify chạy một câu COUNT trên mobile_notify cho mỗi user của bot. Điều kiện là user_id IS NULL OR user_id = X, nên toàn bộ notify dùng chung (user_id NULL, phần lớn dữ liệu) bị quét lại N lần. Job không đặt $timeout, còn connection database có retry_after = 600. Lần chạy dài hơn 10 phút bị giao lại cho worker khác khi lần đầu chưa xong, nên job chạy lặp lại mà không lần nào xong.

Nội dung thay đổi:
- Job nền đếm lại badge thông báo app (chạy sau xoá bạn bè, đặt/huỷ lịch, lưu cài đặt thông báo, thao tác admin bot...): đếm cả bot bằng 2 câu query, badge ra như cũ (module web).
- Đếm theo 1 user (xác nhận thông báo trên app) giữ nguyên cách cũ.
- Lệnh recover:mobileBadgeNotify tự dùng cách đếm mới nên chạy nhanh hơn.

File đã sửa (php-web):
  .../MobileBadgeNotifyRepositoryInterface.php       |  10 +
  app/Jobs/RecountAppBadgeNotify.php                 |  12 +-
  .../Eloquents/MobileBadgeNotifyRepository.php      |  47 ++++-
  tests/Feature/RecountAppBadgeNotifyBatchTest.php   | 227 +++++++++++++++++++++
  4 files changed, 287 insertions(+), 9 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đổi cách đếm trong một job nền, công thức giữ nguyên, có test số câu/SQL và kiểm chứng ngược; chưa verify runtime trên MySQL thật.
- 31 chỗ gọi helper recountAppBadgeNotify() (xoá bạn bè, đặt/huỷ lịch Booking/Salon/Lesson, cài đặt thông báo, API Notify/FriendInformation, Admin Bot, HandlePushMessageNotify, recoverCountNotifyApp) cùng đẩy job này: cần kiểm badge app sau các thao tác đó.
- Bảng mobile_badge_noitfy (count_app_notify), nơi app mobile đọc badge: giá trị ghi vào phải giống cách đếm cũ.
- Lệnh recover:mobileBadgeNotify gọi lại job này.
- recountUnconfirmNotify() (đường 1 user) được viết lại qua hàm lọc chung; SQL sinh ra không đổi.

Migration / thay đổi dữ liệu:
- [Backup · Sau deploy] Sao lưu bảng mobile_badge_noitfy trước khi chạy recover: CREATE TABLE mobile_badge_noitfy_bk_43378 AS SELECT * FROM mobile_badge_noitfy;
- [Recover · Sau deploy] Đếm lại count_app_notify trong mobile_badge_noitfy cho mọi bot (badge sai do job cũ không chạy xong): php artisan recover:mobileBadgeNotify

Recover dữ liệu: Cần recover — Khi job không chạy xong, mobile_badge_noitfy.count_app_notify của các user thuộc bot đó giữ số cũ cho tới lần đếm lại thành công tiếp theo, nên badge trên app hiển thị sai. Dữ liệu gốc mobile_notify vẫn đúng nên đếm lại được.
- Ảnh hưởng: mobile_badge_noitfy.count_app_notify của các user thuộc bot lớn bị lệch so với số notify chưa xác nhận thật
- Ảnh hưởng: Job RecountAppBadgeNotify bị kẹt hoặc chạy lặp trong bảng jobs
- Khoảng thời gian: Từ khi deploy bản có commit f15ff4688c (#38562, có trong release_step_20260805 trở đi) tới khi bản sửa chạy
- Cách recover: Sau khi deploy bản sửa, người vận hành chạy lệnh có sẵn php artisan recover:mobileBadgeNotify. Lệnh đếm lại từ mobile_notify rồi ghi đè, idempotent, và sau bản sửa mỗi bot chỉ tốn 2 câu. Trước và sau khi chạy, dùng câu identify để đếm số dòng lệch (thay cho chế độ chỉ đếm). Các job đang kẹt trong bảng jobs sẽ chạy lại bằng code mới, vì payload chỉ chứa botId/userId.
- Ảnh hưởng tới khách: Không gửi tin cho khách; chỉ số badge thông báo trên app của admin/staff đổi về đúng.

Lưu ý khi deploy:
- Restart queue worker sau deploy để worker nạp code mới; các job đang chờ trong bảng jobs sẽ chạy bằng code mới (payload chỉ có botId/userId).

Việc cần người làm thêm (ngoài phạm vi task):
- Sau khi deploy: người vận hành chạy php artisan recover:mobileBadgeNotify và dùng câu SQL so sánh để đếm số badge lệch trước và sau khi chạy.
- Kiểm bảng jobs/failed_jobs trên production xem còn bao nhiêu job RecountAppBadgeNotify kẹt hoặc trùng cho cùng một bot.
- Ticket cải tiến riêng (nếu cần): chống đẩy trùng job cho cùng một bot từ 31 chỗ gọi, và đặt $timeout nhỏ hơn retry_after cho job này.
- Docblock của interface ghi là loại cả system_notification nhưng code không loại; cần người xác nhận đúng nghiệp vụ (ngoài phạm vi ticket này).
- Suite PHPUnit có lỗi sẵn trên base: ContractExpireServiceTest bị PHP Fatal làm dừng cả suite, cùng lỗi ở BillingServiceTest, ChatMediaSizeValidationTest, ContractChangeMailServiceTest và ExampleTest — cần ticket riêng để sửa test.
- Sau deploy, theo dõi thời gian chạy thực tế của RecountAppBadgeNotify với bot lớn trên production. Nếu vẫn gần 600 giây, xét thêm $timeout, chống dispatch trùng cho cùng bot, hoặc index có cột type.
- Sửa comment của helper recountAppBadgeNotify() trong app/Helpers/functions.php: comment vẫn mô tả 'một câu COUNT cho mỗi user', không còn đúng.

Điểm cần test:
- Bot có notify dùng chung và notify riêng của 2 user, cộng 1 user không có notify riêng: badge từng user bằng kết quả cách đếm cũ.
- Notify type chat 1:1, payment, đã xác nhận (is_confirm=1) hoặc status=0 không được tính.
- Bot không có user nào: job không lỗi và không chạy câu đếm.
- Xác nhận thông báo trên app (đếm theo 1 user): chỉ badge của user đó thay đổi, số đúng.
- Xoá bạn bè, huỷ lịch hẹn, lưu cài đặt thông báo: badge cập nhật, log [action=recount] có đủ từng user.
- Chạy php artisan recover:mobileBadgeNotify trên DB test: chạy hết, số khớp; chạy lần 2 không đổi.
- Trên DB test với bot nhiều notify: số câu query của job giảm từ N xuống 2.
- Bot không có user nào: job chạy xong, không lỗi.
- Chạy php artisan recover:mobileBadgeNotify trên staging: chạy hết, số khớp SQL kiểm; chạy lần 2 số không đổi.
- Bot có nhiều notify: job theo bot xong nhanh, bảng jobs không còn dòng của job này với attempts tăng dần.

Branch: ai_studio_fixbug_43378
- sns-line: ai_studio_fixbug_43378 (nhánh gốc release_step_20260930_v2 @d137c1851896, commit 198a07ab8b28e6bc0f534e0bfbddfab14b1907e4)
```

**Journal #145255 — Dev Studio — 2026-10-19:**

```
Dev handoff — 19/10 14:06 · nhánh ai_studio_fixbug_43378

Nguyên nhân:
Khi xoá 1 bạn bè, code gọi recountAppBadgeNotify($botId) 2 lần trong cùng một request: lần đầu ngay sau khi xoá thông báo (mobile_notify) của bạn bè đó, lần sau khi xoá lịch hẹn. Giữa hai lần không có chỗ nào ghi mobile_notify, nên lần thứ hai chỉ đếm lại y hệt và nhân đôi tải đếm của bot. Lỗi có từ commit #38562: commit đó thay 2 đoạn tính badge cũ bằng recountAppBadgeNotify nhưng giữ nguyên cả hai vị trí. Issue con #43430 và bug automation #3285 báo cùng một lỗi này; có 3 lối vào xoá 1 bạn bè cùng mắc.

Nội dung thay đổi:
- Job nền đếm lại badge thông báo app: đếm cả bot bằng 2 câu query, badge ra như cũ.
- Nút 「削除」 từng dòng ở 「ブロックされた友だち」: mỗi lần xoá đẩy 1 job đếm lại (trước là 2).
- Xoá bạn bè ở trang chi tiết bạn bè / 1:1 chat: đẩy 1 job đếm lại (trước là 2).
- API xoá bạn bè của app mobile: đẩy 1 job đếm lại (trước là 2); request/response không đổi.
- Lệnh recover:mobileBadgeNotify tự dùng cách đếm mới nên chạy nhanh hơn.

Bug QA con:
- #43430 đã sửa (commit sns-line@31b77d952862): Đã bỏ lời gọi đếm lại badge thứ hai (sau khi xoá lịch hẹn) trong luồng xoá 1 bạn bè ở 「ブロックされた友だち」. Mỗi lần xoá giờ chỉ đẩy 1 job, nên bot có 2 user sẽ có 2 dòng log. Hai luồng xoá ở trang chi tiết bạn bè và API app mobile cũng được sửa giống vậy.

Bug automation Test Studio:
- Bug #3285 đã sửa (commit sns-line@31b77d952862): Cùng lỗi với Redmine #43430. Luồng xoá 1 bạn bè ở 「ブロックされた友だち」 chỉ còn 1 lời gọi đếm lại, ngay sau khi xoá thông báo của bạn bè, nên chỉ đẩy 1 job và có 2 dòng log cho bot có 2 user. Badge vẫn đúng.

File đã sửa (php-web):
  .../MobileBadgeNotifyRepositoryInterface.php       |  10 +
  .../Api/FriendInformationController.php            |   1 -
  .../Controllers/Basic/FriendlistController.php     |   2 -
  app/Jobs/RecountAppBadgeNotify.php                 |  12 +-
  .../Eloquents/MobileBadgeNotifyRepository.php      |  47 ++++-
  tests/Feature/RecountAppBadgeNotifyBatchTest.php   | 227 +++++++++++++++++++++
  6 files changed, 287 insertions(+), 12 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Vòng 2 chỉ xoá 3 lời gọi trùng, giữa hai lần gọi không có ghi mobile_notify. Vòng 1 giữ nguyên công thức, có test và kiểm chứng ngược. Chưa verify runtime.
- 31 chỗ gọi helper recountAppBadgeNotify() (xoá bạn bè, đặt/huỷ lịch Booking/Salon/Lesson, cài đặt thông báo, API Notify/FriendInformation, Admin Bot, HandlePushMessageNotify, recoverCountNotifyApp) cùng dùng job này: cần kiểm badge app sau các thao tác đó.
- Bảng mobile_badge_noitfy (count_app_notify), nơi app mobile đọc badge: giá trị ghi vào phải giống cách đếm cũ.
- 3 luồng xoá 1 bạn bè (web 「ブロックされた友だち」, chi tiết bạn bè, API app): phần xoá dữ liệu khác (lịch hẹn, form, tag...) không đổi, chỉ bớt 1 lời gọi đếm lại.
- Xoá hàng loạt ở 「ブロックされた友だち」 không đổi, vẫn 1 lời gọi.
- Lệnh recover:mobileBadgeNotify gọi lại job này.

Migration / thay đổi dữ liệu:
- [Backup · Sau deploy] Sao lưu bảng mobile_badge_noitfy trước khi chạy recover: CREATE TABLE mobile_badge_noitfy_bk_43378 AS SELECT * FROM mobile_badge_noitfy;
- [Recover · Sau deploy] Đếm lại count_app_notify trong mobile_badge_noitfy cho mọi bot (badge sai do job cũ không chạy xong): php artisan recover:mobileBadgeNotify

Recover dữ liệu: Không cần recover — Số badge cuối cùng vẫn đúng (G1=4, G2=3 theo #43430); lỗi chỉ làm thừa một lần đếm. Phần recover của bản 1 (chạy lệnh recover:mobileBadgeNotify sau khi deploy) giữ nguyên.

Lưu ý khi deploy:
- Restart queue worker sau deploy để worker nạp code mới của job; các job đang chờ trong bảng jobs sẽ chạy bằng code mới.

Việc cần người làm thêm (ngoài phạm vi task):
- Sau khi deploy, người vận hành chạy php artisan recover:mobileBadgeNotify (giữ nguyên từ bản 1).
- Ngoài ticket: job RecountAppBadgeNotify vẫn có thể bị đẩy trùng từ nhiều nơi gọi khác nhau và chưa có $timeout — nên xem xét trong một ticket riêng.
- Bộ PHPUnit có sẵn lỗi trên code gốc (ContractExpireServiceTest bị PHP Fatal, BillingServiceTest, ChatMediaSizeValidationTest, ContractChangeMailServiceTest, ExampleTest) — cần một ticket riêng để sửa test.
- Sau deploy, theo dõi thời gian chạy thực tế của RecountAppBadgeNotify với bot lớn. Nếu vẫn gần 600 giây, xét thêm $timeout, chống dispatch trùng cho cùng bot, hoặc index có cột type.
- Sửa comment của helper recountAppBadgeNotify() trong app/Helpers/functions.php: comment vẫn mô tả 'một câu COUNT cho mỗi user', không còn đúng.

Điểm cần test:
- Ở 「ブロックされた友だち」, bấm 「削除」 1 bạn bè của bot có 2 user: chỉ 1 job và 2 dòng log đếm lại; badge mỗi user giảm đúng số thông báo chưa xác nhận của bạn bè đó; badge của bot khác không đổi.
- Xoá bạn bè từ trang chi tiết bạn bè: chỉ 1 job, badge đúng.
- Xoá bạn bè trên app mobile: chỉ 1 job, badge đúng, response API như cũ.
- Bạn bè có lịch hẹn (calendar, salon, lesson): xoá vẫn thành công, lịch hẹn bị xoá, badge đúng.
- Xoá hàng loạt ở 「ブロックされた友だち」: vẫn chỉ 1 job (không hồi quy).
- Badge từng user = số notify dùng chung + số notify riêng của user đó. Notify chat 1:1, payment, đã xác nhận hoặc status=0 không được tính.
- Chạy php artisan recover:mobileBadgeNotify trên staging: chạy hết, số khớp SQL kiểm; chạy lần 2 số không đổi.

Branch: ai_studio_fixbug_43378
- sns-line: ai_studio_fixbug_43378 (nhánh gốc release_step_20260930_v2 @d137c1851896, commit 31b77d952862ef39a06f0e92335260b806ff8080)
```

**Journal #145282 — Dev Studio — 2026-10-19:**

```
Automation Test Studio: pass ở lượt #3715, đã sửa 1 bug automation. Lần bàn giao 19/10 14:06 @31b77d952862 chuyển sang chờ test.
```
