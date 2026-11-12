# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43715 — [LME] BUG NỘI BỘ TỰ DETECT — Báo cáo bảo mật sns-line 22/10/2026: SEC-10 → SEC-16` |
| Module / Màn hình | Quyền truy cập bot (account-select) — nhiều màn: trang chủ admin (`/basic/home`, `/basic/tutorial`), đổi bot (`select-bot`, `link-point-setting`), kiểm tra kết nối bot (`check-mode`), sửa bot (`bot-save`), thêm bot v5 (step3/step5-check), 社員管理 (`get-list-bot-access`), SysAdmin (`/ajax/supper-admin/*`), mobile `list-friend` (v1/v2), upload file form khách |

## Mô tả bug (bản dịch tiếng Việt)

> Đây là **ticket tổng (epic)** gom 7 lỗi bảo mật từ báo cáo rà soát mã nguồn tĩnh (static code review) trên branch `release_step_20260930_v2`, KHÔNG phải 1 bug đơn lẻ có steps to reproduce thông thường. Mỗi lỗi SEC-10 → SEC-16 đã được tách thành 1 sub-task riêng (#43716 → #43722).

**Nguồn:** Báo cáo kiểm tra bảo mật hệ thống LME (sns-line) ngày 22/10/2026 — rà soát mã nguồn tĩnh trên branch `release_step_20260930_v2`. Ticket này gom các lỗi SEC-10 → SEC-16; mỗi lỗi là 1 sub-task.

**Đã đối chiếu lại với code thật** (AI fixbug, 22/10/2026, đọc bằng `git show origin/release_step_20260930_v2` — không chạy tấn công trên môi trường thật):
- Cả 7 lỗi đều CÓ THẬT.
- SEC-12 **nặng hơn** báo cáo: chuỗi API SuperAdmin cho phép đăng nhập thẳng vào tài khoản staff của bot bất kỳ.
- SEC-13 **nhẹ hơn** báo cáo: đứng riêng không khai thác được (phải biết `channel_secret` của bot nạn nhân), chỉ nguy hiểm khi nối với SEC-14/SEC-15.
- Branch `origin/security-idor-merged` (14/10) CHƯA vá điểm nào trong 7 lỗi này.

**Các lỗi nối chuỗi với nhau (chain attack):**
- SEC-12 (`bots-for-user`) trả hash bot của user bất kỳ ⇒ đầu vào cho SEC-16 và SEC-12 (`staffs`).
- SEC-14 / SEC-15 làm lộ `channel_secret` ⇒ điều kiện để khai thác SEC-13.

**Thứ tự xử lý đề xuất:** SEC-12 → SEC-14 → SEC-10 → SEC-11 → SEC-16 → SEC-15 → SEC-13 (khoá SEC-12 + SEC-14 trước là cắt được phần lớn chuỗi tấn công).

**Lưu ý phạm vi (quan trọng cho Leader):**
- SEC-11 nằm trong `app/Http/Controllers/Api/*` và lối vào 1 của SEC-16 nằm trong `app/Http/Controllers/Mobile/*` — rule hiện tại của auto-fix là **không sửa 2 nhóm này** ⇒ cần human xác nhận ngoại lệ trước khi fix. (Cần verify thêm: bản fix thực tế ở branch `ai_studio_fixbug_43715` có sửa `ListFriendController.php` (Mobile) hay không — xem file đã sửa ở `03-dev-impact.md`.)
- Sau khi vá: nên rotate token/secret LINE của các bot (đã có thể bị lộ qua SEC-14/SEC-15).

Tài liệu nội bộ — mô tả lỗ hổng CHƯA được vá (tại thời điểm báo cáo), không chia sẻ ra ngoài.

## Steps to reproduce

<!-- Không có — đây là báo cáo bảo mật từ rà soát mã nguồn tĩnh, không phải bug runtime có steps tái hiện. Chi tiết từng lỗ hổng (vector khai thác cụ thể) nằm ở 7 sub-task #43716 → #43722, KHÔNG có trong ticket tổng này. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có attachment nào trên ticket #43715. -->

## Ghi chú thêm của Leader

- Ticket #43715 là **ticket tổng**, không chứa chi tiết kỹ thuật từng lỗ hổng — chi tiết vector khai thác của từng mã SEC-10..SEC-16 nằm ở sub-task riêng (#43716 → #43722), **chưa fetch trong lần `/new-task` này**.
- Dev impact (file `03-dev-impact.md`) được tổng hợp từ journal "Dev handoff" **vòng 3** (Journal #146933, 22/10 15:15) — là bản tổng hợp mới nhất, đã gộp sửa lỗi QA con phát sinh ở vòng 2. Vòng 1 (#146621) và vòng 2 (#146682) giữ nguyên văn ở section Journal bên dưới để tham khảo lịch sử.
- 3 bug con phát sinh trong quá trình QA tự động (#43839, #43840, #43841) đã được Dev kết luận **KHÔNG phải do code sửa trong ticket này** (lỗi kịch bản test / hành vi có sẵn trên base) — Dev đề nghị Reject hoặc mở ticket riêng. Leader cần xác nhận trước khi review coverage (không tính các mã này là GAP của #43715).
- Việc **ngoài phạm vi fix** nhưng Dev nêu, cần Leader/human quyết riêng (không đẻ TC cho các điểm này trong task #43715):
  - IDOR tại `BotController::changeNewBotStep1` (`/ajax/admin/step1-change-new-bot`) — ghi đè token/secret bot theo id client gửi, không kiểm chủ bot. Cần mở ticket bảo mật riêng (ưu tiên cao).
  - Hạ tầng: chặn thực thi PHP + gửi header `nosniff` cho thư mục `public/media`.
  - Middleware `MobileAccess` thiếu route `ListBotMobile.v2` trong danh sách ngoại lệ (liên quan bug con #43840/#43840 automation #3723) — hành vi có sẵn trên base, không do ticket này.
  - Quyết định có rotate token/secret LINE của các bot hay không (AnhTT xác nhận production chưa có dấu vết khai thác tại 22/10/2026).
  - Có bắt buộc bot phải có hợp đồng active mới được thao tác hay không (hiện tại KHÔNG bắt buộc — 36/231 bot đang dùng không có hợp đồng active trên DB điều tra) — cần AnhTT chốt riêng.
- **Hướng dẫn test bằng Postman** (Journal #147099, AI LME Fix bug) — áp dụng chung cho tất cả 7 sub-task:
  - Test trên **STAGING** đã deploy branch `ai_studio_fixbug_43715`. **TUYỆT ĐỐI KHÔNG test trên production** (các ca có thao tác ghi/xoá).
  - Đăng nhập lấy cookie session qua route web (KHÔNG dùng API token) — copy cookie `<APP_NAME>_session` vào Postman hoặc dùng Interceptor; giữ cùng cookie cho cả loạt request (SEC-16 phụ thuộc session).
  - Thêm header `X-Requested-With: XMLHttpRequest` để endpoint trả JSON thay vì redirect HTML.
  - 3 tài khoản test cần chuẩn bị: **A** = user thường (role 0) có bot riêng; **B** = user khác có bot riêng (lấy bot_id số + hashid của B để test vượt quyền); **S** = SysAdmin (role -1) để test regression nhóm supper-admin.
  - Quy ước kết quả mong đợi sau fix: vượt quyền bot ⇒ 403 (hoặc redirect kèm `「この権限は許可されていません。」`); route đã gỡ (`unfollow-line`) ⇒ 404; upload sai định dạng ⇒ 422; thao tác hợp lệ của chính chủ bot/staff đã chấp nhận/SysAdmin ⇒ vẫn 200 như cũ (**regression bắt buộc kiểm** để chắc fix không chặn nhầm người dùng thật).

## Dữ liệu định danh ca lỗi

<!-- Ticket tổng không có ca lỗi cụ thể (bug suite, không phải 1 lỗi runtime đơn). Dữ liệu định danh (bot_id, user A/B/S) nằm ở hướng dẫn Postman phía trên — bỏ bảng ID cụ thể. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #146556 — AI LME Fix bug — 2026-10-22:**

```
Đã tạo 7 sub-task (mỗi lỗi 1 ticket):
* SEC-10 → #43716
* SEC-11 → #43717
* SEC-12 → #43718
* SEC-13 → #43719
* SEC-14 → #43720
* SEC-15 → #43721
* SEC-16 → #43722
```

**Journal #146621 — Dev Studio — 2026-10-22 (vòng 1 — tham khảo lịch sử, bản mới nhất ở vòng 3):**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Các endpoint bị lỗi hoặc nằm ngoài nhóm route có kiểm đăng nhập/quyền (upload form công khai, unfollow-line, get-list-bot-access, nhóm supper-admin chỉ có check_login), hoặc lấy bot theo bot_id/hashid do client gửi mà không kiểm người đang đăng nhập có phải chủ/staff của bot đó không (bot-save, step3/step5, check-mode, gán bot hiện tại vào session). Model Bots không ẩn cột nào nên những chỗ trả nguyên bản ghi làm lộ token/secret LINE. Upload ở form phía khách giữ đuôi file client gửi và lưu thẳng dưới public.

Hướng sửa:
- D-1 Thêm middleware supper_admin cho nhóm route /ajax/supper-admin/*
- D-2 get-list-bot-access bắt đăng nhập, chỉ cho chủ xem nhân viên của mình, trả ít cột
- D-3 Thêm helper isBotAccessibleByUser (chủ bot hoặc staff đã chấp nhận)
- D-4 step3-check/step5-check chỉ nhận bot của chính người dùng, trả ít field
- D-5 check-mode kiểm quyền bot và chỉ trả id/is_connected/webhook_url
- D-6 bot-save kiểm quyền bot trước khi xử lý
- D-7 BasicAccess không gán bot lạ vào session ở basicHome/bot.tutorial
- D-8 select-bot và link-point-setting kiểm quyền trước khi gán session
- D-9 Mobile list-friend kiểm quyền bot trước khi gán session
- D-10 Gỡ route /api/unfollow-line
- D-11 Upload form phía khách chỉ nhận 19 đuôi đã chốt
- D-12 PHPUnit cho helper và các guard chính

Ảnh hưởng / rủi ro:
Chỉ chặn request vượt quyền; chủ bot, staff đã chấp nhận và SysAdmin dùng như cũ, một số response bớt field (đã đối chiếu mọi nơi gọi FE). Form khách sẽ từ chối file ngoài 19 đuôi đã chốt. Cần test kỹ chuyển bot, thêm bot, kiểm tra kết nối, màn SysAdmin, web mobile và upload file ở form khách; có rủi ro conflict khi merge với nhánh #43398 và #42444.
```

**Journal #146682 — Dev Studio — 2026-10-22 (vòng 2 — tham khảo lịch sử, bản mới nhất ở vòng 3):**

```
Dev handoff — 22/10 10:59 · nhánh ai_studio_fixbug_43715

Nguyên nhân:
Không có lỗi mới; 7 lỗi SEC-10 → SEC-16 giữ nguyên nguyên nhân như bản 1. Helper kiểm quyền bot ở bản 1 chỉ kiểm bots.admin_id hoặc staff đã chấp nhận, không lọc trạng thái bot như câu truy vấn danh sách bot getListBotNew mà AnhTT chỉ ra, nên bot đã xoá hoặc đang thêm dở vẫn được nhận.

Nội dung thay đổi:
- SysAdmin: 8 API /ajax/supper-admin/* chỉ SysAdmin gọi được; người thường nhận 403.
- 社員管理 (modal sửa nhân viên): API danh sách bot cần đăng nhập, chỉ trả bot của nhân viên thuộc chủ đang đăng nhập; không còn token/secret.
- Kiểm tra kết nối bot (check-mode), step3/step5 thêm bot: bot không thuộc user thì trả 403; response chỉ còn vài field cần dùng.
- Lưu chỉnh sửa bot (bot-save): bot không thuộc user thì trả 403.
- Đổi bot hiện tại qua /basic/home/{hash}, /basic/tutorial/{hash}, select-bot, link-point-setting, mobile /list-friend/{hash} (và /v2): chỉ nhận bot có trong danh sách bot của user. Với bot lạ hoặc bot đã xoá, bot hiện tại không đổi; web về trang chủ admin kèm 「この権限は許可されていません。」, mobile về danh sách bot.
- Gỡ API POST /api/unfollow-line (không còn nơi gọi), gọi vào sẽ nhận 404.
- Form phía khách: upload chỉ nhận 19 đuôi (jpg, jpeg, png, gif, pdf, mp4, mov, mp3, m4a, txt, csv, doc, docx, xls, xlsx, ppt, pptx, zip, heic); sai đuôi hoặc ảnh/PDF giả thì báo 「ファイルの形式が正しくありません。…」.

File đã sửa (php-web):
  app/Helpers/functions.php                          |  34 ++
  app/Http/Controllers/Admin/BotController.php       |  32 +-
  app/Http/Controllers/Admin/UserController.php      |  45 +-
  .../Controllers/Basic/FormAnswerController.php     |  17 +-
  .../Controllers/Mobile/ListFriendController.php    |  10 +-
  app/Http/Middleware/BasicAccess.php                |  14 +-
  routes/api.php                                     |   1 -
  routes/web.php                                     |   4 +-
  tests/Feature/BotAccessGuardTest.php               | 657 +++++++++++++++++++++
  9 files changed, 792 insertions(+), 22 deletions(-)

Đánh giá ảnh hưởng — Rủi ro trung bình: Sửa middleware dùng cho mọi trang /basic/* và nhiều endpoint. Điều kiện quyền nay trùng danh sách bot của user nên người dùng hợp lệ không bị chặn, nhưng chưa verify runtime.
- Middleware BasicAccess chạy cho mọi trang /basic/*: chuyển bot giữa bot của mình và bot được mời, vào trang chủ hoặc tutorial sau khi thêm bot.
- Helper kiểm quyền dùng getListBotId (hàm dùng chung, không sửa): staff is_admin=1 không phải chủ không còn vào được bot (3 dòng trên DB điều tra, đều không đang được chọn).
- Màn SysAdmin user detail / bot detail / affiliater nay đi qua middleware supper_admin.
- Màn 社員管理: modal chọn bot cho nhân viên.
- Luồng thêm bot v5 (select-bot, sang trang chủ bot sau khi kết nối), danh sách bot và màn cài đặt bot (nút 接続チェック gọi check-mode).
- Màn sửa bot (bot-save) cho chủ và staff đã chấp nhận.
- App mobile (WebView) /list-friend, /v2/list-friend, gồm cả tìm kiếm ajax.
- Form phía khách v1/v3 có câu hỏi file (画像, PDF, 動画, 音声, 指定無し).
- Module job/callback không gọi /api/unfollow-line, nên không bị ảnh hưởng.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Chỉ đổi điều kiện kiểm quyền; AnhTT đã xác nhận production không có dấu vết khai thác (22/10/2026).

Lưu ý khi deploy:
- Nếu server dùng php artisan route:cache thì chạy lại sau deploy (đổi routes/web.php, routes/api.php). Không đổi JS/CSS.

Việc cần người làm thêm (ngoài phạm vi task):
- Ticket riêng: changeNewBotStep1 (/ajax/admin/step1-change-new-bot) ghi đè token/secret bot khác không kiểm chủ (review R-1).
- Hạ tầng: chặn thực thi PHP và gửi nosniff cho thư mục media (review R-4).
- Người phụ trách quyết có rotate token LINE để phòng ngừa hay không.
- Nếu muốn bắt buộc bot phải có hợp đồng active mới được thao tác (hiện LEFT JOIN như getListBotNew nên không bắt buộc), AnhTT cần chốt riêng: trên DB điều tra có 36/231 bot đang dùng không có hợp đồng active.
- Bộ PHPUnit của repo vẫn có 5 file lỗi sẵn trên base (ContractExpireServiceTest bị fatal làm dừng cả suite): cần người phụ trách sửa riêng.
- Mở ticket riêng (ưu tiên cao): /ajax/admin/step1-change-new-bot (BotController::changeNewBotStep1) ghi đè token/secret bot theo id client gửi mà không kiểm chủ bot.
- Hạ tầng: cấu hình web server không thực thi PHP trong public/media; rotate token/secret LINE của các bot như ticket khuyến nghị.

Điểm cần test:
- Chủ bot và staff đã chấp nhận: chuyển bot từ trang chủ admin, kiểm tra kết nối, sửa bot, link point-settings, list-friend mobile chạy như trước.
- Bot không có hợp đồng active nhưng vẫn hiện trong danh sách bot vẫn vào được.
- Bot đã xoá của chính mình: /basic/home/{hash} về trang chủ admin kèm 「この権限は許可されていません。」; kiểm tra kết nối nhận 403.
- Thêm bot mới bằng màn v5 tới khi kết nối xong rồi vào trang chủ bot bình thường.
- Bot của người khác: mọi lối vào vẫn bị chặn như bản 1.
- Test tự động BotAccessGuardTest đạt; chạy trên base thì các ca guard mới fail.
- Chủ bot và staff đã chấp nhận: chuyển bot từ trang chủ admin, 接続チェック, sửa bot, link point-settings, list-friend mobile vẫn chạy bình thường.
- Bot không có hợp đồng active (free/hết hạn nhưng vẫn hiện trong danh sách) vẫn vào được trang chủ bot.
- Bot đã xoá của chính mình: /basic/home/{hash} chuyển về trang chủ admin kèm 「この権限は許可されていません。」; check-mode trả 403.
- Thêm bot mới bằng màn v5 (QR và Quick Connect) tới 接続完了 rồi bấm sang trang chủ bot: bình thường, bot hiện tại đổi sang bot mới.
- Tài khoản A dùng hash/id bot của tài khoản B ở /basic/home, select-bot, link-point-setting, check-mode, bot-save, /list-friend: đều bị từ chối, bot hiện tại không đổi.
- Form phía khách: upload .php/.html/.svg hoặc ảnh giả bị báo lỗi định dạng; png/mp4/heic/docx thì upload được.

Branch: ai_studio_fixbug_43715
- sns-line: ai_studio_fixbug_43715 (nhánh gốc release_step_20260930_v2 @4ae243379f82, commit d6594d7f3295dbb625fef422fe828f23896d776a)
```

**Journal #146883 — Dev Studio — 2026-10-22 (bug con phát sinh vòng QA, không đổi code):**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Không có lỗi mới do ticket gây ra. #43839: kịch bản bấm selector .cell-account__name, selector của màn danh sách tài khoản; trên màn chi tiết user, B1 là link tới /admin/bot/{hash} và link này đã hiện. #43841: khi tắt hết marker, markerUser lưu chuỗi rỗng thay cho NULL của fixture; model User coi hai giá trị này đều là không có marker, nhưng kịch bản so chuỗi tuyệt đối nên báo lệch. #43840: middleware MobileAccess chuyển /v2/list-bot về /list-bot (v1) khi session chưa có bot hiện tại vì route ListBotMobile.v2 không nằm trong danh sách ngoại lệ; hành vi này đã có trên base.

Ảnh hưởng / rủi ro:
Không đổi code nên không có rủi ro mới. Nếu sửa #43840 thì phải động tới middleware dùng chung của mọi màn mobile, cần người duyệt mở rộng phạm vi.
```

**Journal #146933 — Dev Studio — 2026-10-22 (vòng 3 — BẢN MỚI NHẤT, dùng làm input chính cho `03-dev-impact.md`):**

```
Dev handoff — 22/10 15:15 · nhánh ai_studio_fixbug_43715

Nguyên nhân:
Không có lỗi mới do ticket gây ra. #43839: kịch bản bấm selector .cell-account__name, selector của màn danh sách tài khoản; trên màn chi tiết user, B1 là link tới /admin/bot/{hash} và link này đã hiện. #43841: khi tắt hết marker, markerUser lưu chuỗi rỗng thay cho NULL của fixture; model User coi hai giá trị này đều là không có marker, nhưng kịch bản so chuỗi tuyệt đối nên báo lệch. #43840: middleware MobileAccess chuyển /v2/list-bot về /list-bot (v1) khi session chưa có bot hiện tại vì route ListBotMobile.v2 không nằm trong danh sách ngoại lệ; hành vi này đã có trên base.

Nội dung thay đổi:
- SysAdmin: 8 API /ajax/supper-admin/* chỉ SysAdmin gọi được; người thường nhận 403.
- 社員管理 (modal sửa nhân viên): API danh sách bot cần đăng nhập và chỉ trả bot của nhân viên thuộc chủ đang đăng nhập. Mỗi bot chỉ có id, view_name, plan_type, checked, accessNumber, freePlan. id sai dạng (mảng, rỗng, chữ, thiếu) ⇒ 403.
- Kiểm tra kết nối bot (check-mode): bot không thuộc user ⇒ 403; object bot trong response chỉ còn id, is_connected, webhook_url. step3/step5 thêm bot: bot không thuộc user ⇒ 403.
- Lưu chỉnh sửa bot (bot-save): bot không thuộc user ⇒ 403.
- Đổi bot hiện tại qua /basic/home/{hash}, /basic/tutorial/{hash}, select-bot, link-point-setting, mobile /list-friend/{hash} và /v2/...: chỉ nhận bot có trong danh sách bot của user. Bot lạ hoặc đã xoá ⇒ không đổi bot; web về trang chủ admin kèm 「この権限は許可されていません。」, mobile về danh sách bot.
- Gỡ API POST /api/unfollow-line ⇒ 404.
- Form phía khách: upload chỉ nhận 19 đuôi (jpg, jpeg, png, gif, pdf, mp4, mov, mp3, m4a, txt, csv, doc, docx, xls, xlsx, ppt, pptx, zip, heic). Sai đuôi hoặc ảnh/PDF giả ⇒ 「ファイルの形式が正しくありません。…」.

Bug QA con:
- #43839 không đổi code: Lỗi kịch bản (giống automation #3727): driver tìm .cell-account__name, nhưng ở ユーザー詳細 thì B1 là thẻ a tới /admin/bot/{hash} và đã hiển thị. Màn không bị chặn. Đề nghị người phụ trách Reject và sửa kịch bản.
- #43840 không đổi code: Friend của bot mình hiện đúng; URL v1 là do middleware MobileAccess có sẵn trên base (thiếu ListBotMobile.v2 trong danh sách ngoại lệ), không do ticket gây ra. Người phụ trách quyết Reject, hoặc mở ticket riêng để sửa middleware dùng chung mọi màn mobile.
- #43841 không đổi code: Lỗi kịch bản (giống automation #3724): bật/tắt marker lưu và giữ đúng sau reload, không có 403. Tắt hết marker thì ghi chuỗi rỗng thay cho NULL, và hai giá trị này cùng nghĩa (User::getMarkerAttribute đều trả []). Đề nghị Reject.

Bug automation Test Studio:
- Bug #3723 để sau: Middleware MobileAccess (không đổi trong ticket) đưa /v2/list-bot về /list-bot (v1) khi session chưa có bot, vì ListBotMobile.v2 thiếu trong danh sách ngoại lệ. Hành vi có sẵn trên base, guard mới vẫn cho chủ bot xem đúng friend. Để ticket riêng.
- Bug #3724 không phải bug: Lỗi kịch bản: tắt hết marker thì ghi chuỗi rỗng thay cho NULL, cùng nghĩa 'không có marker' (User::getMarkerAttribute trả [] cho cả hai). Bật/tắt và reload đúng, không có 403.
- Bug #3725 đã sửa (commit sns-line@5ff19ea3cfce): check-mode đọc lại bot bằng toBase(), nên object bot chỉ còn id, is_connected, webhook_url ở cả 7 nhánh. get-list-bot-access bỏ hash_botId bằng makeHidden.
- Bug #3726 đã sửa (commit sns-line@5ff19ea3cfce): Dòng log không nối chuỗi id dạng mảng nữa, nên request đi tới guard và trả 403 {success:false} cho id mảng, rỗng, chữ hoặc thiếu.
- Bug #3727 không phải bug: Lỗi kịch bản: driver tìm selector .cell-account__name, nhưng ở ユーザー詳細 thì B1 là thẻ a tới /admin/bot/{hash} và đã hiển thị (xem trace).
- Bug #3728 đã sửa (commit sns-line@5ff19ea3cfce): Mọi nhánh của check-mode trả bot đúng 3 khoá id, is_connected, webhook_url (không còn hash_botId); có test kiểm đúng tập khoá.
- Bug #3729 đã sửa (commit sns-line@5ff19ea3cfce): Mỗi phần tử allBotNew chỉ còn id, view_name, plan_type, checked, accessNumber, freePlan. Phần tử chỉ có checked có thể xuất hiện nếu nhân viên còn quyền với bot đã xoá (code cũ).

File đã sửa (php-web):
  app/Helpers/functions.php                          |  34 +
  app/Http/Controllers/Admin/BotController.php       |  32 +-
  app/Http/Controllers/Admin/UserController.php      |  56 +-
  .../Controllers/Basic/FormAnswerController.php     |  17 +-
  .../Controllers/Mobile/ListFriendController.php    |  10 +-
  app/Http/Middleware/BasicAccess.php                |  14 +-
  routes/api.php                                     |   1 -
  routes/web.php                                     |   4 +-
  tests/Feature/BotAccessGuardTest.php               | 701 +++++++++++++++++++++
  9 files changed, 846 insertions(+), 23 deletions(-)

Đánh giá ảnh hưởng — Rủi ro trung bình: Sửa middleware cho mọi trang /basic/* và nhiều endpoint kiểm quyền bot. Vòng 4 không thêm code. Chưa verify trên môi trường chạy thật.
- Middleware BasicAccess chạy cho mọi trang /basic/*: chuyển bot giữa bot của mình và bot được mời, vào trang chủ/tutorial sau khi thêm bot.
- Helper isBotAccessibleByUser dùng getListBotId (dùng chung, không sửa): staff is_admin = 1 không phải chủ không còn vào được bot.
- Màn SysAdmin user detail / bot detail / affiliater (thêm middleware supper_admin); marker và link bot hoạt động như cũ.
- Màn 社員管理: modal chọn bot cho nhân viên (dạng response get-list-bot-access đổi).
- Nút 接続チェック ở màn cài đặt bot, danh sách bot, màn thêm bot, xác nhận hợp đồng standard (dạng object bot trong response check-mode đổi).
- Luồng thêm bot v5 và màn sửa bot (bot-save) cho chủ và staff đã chấp nhận.
- App mobile (WebView) /list-friend, /v2/list-friend, gồm tìm kiếm ajax. URL v1 khi mở /v2/list-bot lần đầu là hành vi có sẵn, không do ticket.
- Form phía khách v1/v3 có câu hỏi file.
- Model Bots không đổi ($appends giữ nguyên) nên các nơi khác vẫn có hash_botId như cũ.
- Module job/callback không gọi /api/unfollow-line nên không ảnh hưởng.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Không có thay đổi code và không có dữ liệu bị ghi sai hay bỏ sót; marker chuỗi rỗng và NULL được ứng dụng coi như nhau.

Lưu ý khi deploy:
- Nếu server dùng php artisan route:cache thì chạy lại sau deploy (đổi routes/web.php, routes/api.php). Không đổi JS/CSS, không đổi submodule lme-ui.

Việc cần người làm thêm (ngoài phạm vi task):
- Reject #43839 và #43841 trên Redmine vì đây là lỗi kịch bản, và báo Test Studio sửa NEW-40 (selector link a[href*='/admin/bot/']) và NEW-39 (coi marker NULL và rỗng là như nhau).
- Reject #43840 trong ticket này; nếu cần giữ giao diện v2 thì mở ticket riêng để thêm ListBotMobile.v2 vào danh sách route ngoại lệ của middleware MobileAccess.
- Reject issue con #43839: kịch bản NEW-40 dùng sai selector, nên bấm a[href*="/admin/bot/"] trên màn ユーザー詳細.
- Reject issue con #43841: kịch bản NEW-39 coi marker NULL và chuỗi rỗng là khác nhau, nên so sánh theo danh sách marker.
- Reject hoặc mở ticket riêng cho #43840: MobileAccess thiếu route ListBotMobile.v2 trong danh sách ngoại lệ, hành vi có sẵn trên base. Nếu muốn sửa ngay trong ticket này thì người phụ trách cần duyệt mở rộng phạm vi.
- IDOR ở BotController::changeNewBotStep1 (/ajax/admin/step1-change-new-bot) vẫn cần ticket riêng.
- Mobile: thêm ListBotMobile.v2 vào danh sách route ngoại lệ của middleware MobileAccess để /v2/list-bot không bị đưa về /list-bot (v1) khi session chưa có bot (#43840 / automation #3723). Lỗi có sẵn trên base, cần ticket riêng.
- BotController::changeNewBotStep1 (/ajax/admin/step1-change-new-bot) bị IDOR: ghi đè token/secret của bot theo id do client gửi mà không kiểm chủ bot. Cần ticket bảo mật riêng.
- Sau khi deploy nên rotate token/secret LINE của các bot (có thể đã lộ qua SEC-14/SEC-15), theo khuyến nghị trong ticket.

Điểm cần test:
- Không có điểm kiểm thử mới. Gợi ý sửa kịch bản: NEW-40 bấm a[href*='/admin/bot/'] trên 「ユーザー詳細」; NEW-39 so sánh marker theo danh sách, coi NULL và rỗng là như nhau; NEW-47 chọn bot trước khi mở /v2/list-bot, hoặc chỉ kiểm tra friend hiển thị đúng.
- Re-test lại theo bàn giao vòng 3: check-mode chỉ trả id, is_connected, webhook_url; get-list-bot-access không có hash_botId và id sai dạng trả 403.
- Kịch bản NEW-40 (#43839): bấm a[href*="/admin/bot/"] trên 「ユーザー詳細」 thay cho .cell-account__name.
- Kịch bản NEW-39 (#43841): so sánh marker theo danh sách (NULL và chuỗi rỗng là như nhau) hoặc theo trạng thái trên màn.
- Kịch bản NEW-47 (#43840): chọn bot trước khi mở /v2/list-bot, hoặc chỉ kiểm danh sách friend hiển thị và không bị đẩy về danh sách bot.

Branch: ai_studio_fixbug_43715
- sns-line: ai_studio_fixbug_43715 (nhánh gốc release_step_20260930_v2 @4ae243379f82, commit 5ff19ea3cfcedb471456835848d070fc63ffdf7c)
```

**Journal #147099 — AI LME Fix bug — 2026-10-22 (hướng dẫn test Postman):**

```
Cach test cac sub-task bang Postman — phan chuan bi chung (QA xac minh fix)

Ban fix: branch ai_studio_fixbug_43715 (commit 5ff19ea3cf). Test tren STAGING da deploy branch nay. TUYET DOI KHONG test tren production (cac ca co thao tac ghi/xoa).

1) Bien moi truong Postman:
   - {{base_url}} = domain web quan tri staging (vd http://host.docker.internal:8000).
2) Dang nhap lay cookie session (route web, KHONG phai API token):
   - Cach de nhat: dang nhap bang trinh duyet roi copy cookie <APP_NAME>_session (ten theo config/session.php, mac dinh dang *_session) vao Postman (tab Cookies cua domain), hoac bat Postman Interceptor.
   - Giu cung cookie cho ca loat request de session on dinh (SEC-16 phu thuoc session).
3) De endpoint tra JSON thay vi redirect HTML, them header: X-Requested-With: XMLHttpRequest.
4) Tai khoan test nen chuan bi:
   - A = user thuong (role 0), co it nhat 1 bot cua rieng minh.
   - B = user khac, co bot rieng (lay bot_id so + hashid cua bot B de thu "vuot quyen").
   - S = SysAdmin (role -1) de kiem cac ca regression cua nhom supper-admin.
5) Quy uoc ket qua mong doi sau fix:
   - Vuot quyen bot => 403 (hoac redirect ve trang chu admin / danh sach bot voi loi 'この権限は許可されていません。').
   - Route da go (unfollow-line) => 404.
   - Upload sai dinh dang => 422.
   - Thao tac hop le cua chinh chu bot / staff da chap nhan / SysAdmin => van 200 nhu cu (ca regression BAT BUOC kiem de chac fix khong chan nham nguoi dung that).

Moi sub-task co note rieng (TC1.. + PASS): #43716 SEC-10, #43717 SEC-11, #43718 SEC-12, #43719 SEC-13, #43720 SEC-14, #43721 SEC-15, #43722 SEC-16.

Luu y: cac diem "viec can lam them" Dev Studio ghi (IDOR o changeNewBotStep1 /ajax/admin/step1-change-new-bot; chan thuc thi PHP trong public/media; rotate token LINE) nam NGOAI pham vi fix nay — can ticket rieng, khong thuoc loat test tren.
```
