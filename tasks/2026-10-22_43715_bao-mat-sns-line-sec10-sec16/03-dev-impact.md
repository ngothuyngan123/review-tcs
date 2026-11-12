# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Nguồn: Journal #146933 (Dev Studio, "Dev handoff — 22/10 15:15", **vòng 3 — bản mới nhất**). Ticket #43715 KHÔNG có section "Đánh giá ảnh hưởng" chuẩn trong Description (đây là ticket tổng gom 7 lỗi bảo mật SEC-10 → SEC-16, chi tiết từng lỗi nằm ở sub-task #43716 → #43722 — chưa fetch). Nội dung dưới đây là bản tổng hợp chung cho TOÀN BỘ 7 lỗi trong cùng 1 branch fix.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI) |
| Commit / Pull Request | `sns-line@5ff19ea3cfcedb471456835848d070fc63ffdf7c` (branch gốc `release_step_20260930_v2@4ae243379f82`) |
| Branch | `ai_studio_fixbug_43715` |
| Ngày submit đánh giá | 2026-10-22 (vòng 3, 15:15) |
| Auto-filled | 2026-10-22 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại journal #146933 trên Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Không có lỗi mới ở vòng 3; giữ nguyên nguyên nhân gốc của 7 lỗi SEC-10 → SEC-16 (vòng 1):

Các endpoint bị lỗi hoặc nằm ngoài nhóm route có kiểm đăng nhập/quyền (upload form công khai, `unfollow-line`, `get-list-bot-access`, nhóm `supper-admin` chỉ có `check_login`), hoặc lấy bot theo `bot_id`/`hashid` do client gửi mà **không kiểm người đang đăng nhập có phải chủ/staff của bot đó không** (`bot-save`, step3/step5, `check-mode`, gán bot hiện tại vào session). Model `Bots` không ẩn cột nào nên những chỗ trả nguyên bản ghi làm lộ token/secret LINE. Upload ở form phía khách giữ đuôi file client gửi và lưu thẳng dưới `public`.

Vòng 2 bổ sung: helper kiểm quyền bot ở bản 1 chỉ kiểm `bots.admin_id` hoặc staff đã chấp nhận, **không lọc trạng thái bot** như câu truy vấn `getListBotNew`, nên bot đã xoá hoặc đang thêm dở vẫn được nhận (đã fix ở vòng 2).

3 bug con QA phát sinh (#43839, #43840, #43841) — Dev kết luận **không do code sửa trong ticket này**:
- **#43839**: lỗi kịch bản test — selector `.cell-account__name` sai, ở màn `ユーザー詳細` link đúng là `a[href*="/admin/bot/"]` và đã hiển thị. Màn không bị chặn.
- **#43840**: middleware `MobileAccess` (không đổi trong ticket) chuyển `/v2/list-bot` về `/list-bot` (v1) khi session chưa có bot hiện tại, vì route `ListBotMobile.v2` không có trong danh sách ngoại lệ — hành vi **có sẵn trên base**.
- **#43841**: lỗi kịch bản — khi tắt hết marker, `markerUser` lưu chuỗi rỗng thay cho `NULL` của fixture; `User::getMarkerAttribute` coi 2 giá trị này đều là "không có marker" (trả `[]`), kịch bản so chuỗi tuyệt đối nên báo lệch.

## 2. Cách fix

- SysAdmin: 8 API `/ajax/supper-admin/*` chỉ SysAdmin gọi được; người thường nhận **403**.
- 社員管理 (modal sửa nhân viên): API danh sách bot (`get-list-bot-access`) cần đăng nhập, chỉ trả bot của nhân viên thuộc chủ đang đăng nhập. Mỗi bot chỉ còn field `id, view_name, plan_type, checked, accessNumber, freePlan`. `id` sai dạng (mảng, rỗng, chữ, thiếu) ⇒ **403**.
- Kiểm tra kết nối bot (`check-mode`): bot không thuộc user ⇒ **403**; object bot trong response chỉ còn `id, is_connected, webhook_url`. step3/step5 thêm bot: bot không thuộc user ⇒ **403**.
- Lưu chỉnh sửa bot (`bot-save`): bot không thuộc user ⇒ **403**.
- Đổi bot hiện tại qua `/basic/home/{hash}`, `/basic/tutorial/{hash}`, `select-bot`, `link-point-setting`, mobile `/list-friend/{hash}` và `/v2/...`: chỉ nhận bot có trong danh sách bot của user. Bot lạ hoặc đã xoá ⇒ **không đổi bot hiện tại**; web về trang chủ admin kèm `「この権限は許可されていません。」`, mobile về danh sách bot.
- Gỡ API `POST /api/unfollow-line` ⇒ **404**.
- Form phía khách: upload chỉ nhận **19 đuôi** đã chốt (jpg, jpeg, png, gif, pdf, mp4, mov, mp3, m4a, txt, csv, doc, docx, xls, xlsx, ppt, pptx, zip, heic). Sai đuôi hoặc ảnh/PDF giả (magic byte không khớp) ⇒ `「ファイルの形式が正しくありません。…」`.

3 bug con QA (#43839/#43840/#43841): **không sửa code** — Dev đề nghị Reject trên Redmine + báo Test Studio sửa kịch bản tự động (NEW-40 đổi selector, NEW-39 coi marker NULL/rỗng như nhau, NEW-47 chọn bot trước khi mở `/v2/list-bot`). #43840 có thể mở ticket riêng để thêm `ListBotMobile.v2` vào danh sách ngoại lệ của middleware `MobileAccess` nếu Leader muốn fix trong phạm vi rộng hơn.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `app/Helpers/functions.php` | +34 dòng — thêm helper `isBotAccessibleByUser` (chủ bot hoặc staff đã chấp nhận), dùng `getListBotId` (hàm **dùng chung, không sửa**) | Chuẩn hoá điều kiện kiểm quyền bot cho mọi guard mới |
| 2 | `app/Http/Controllers/Admin/BotController.php` | ~32 dòng — `check-mode`, step3/step5-check, `bot-save` thêm guard quyền, giảm field response | Chặn IDOR lấy/sửa bot của người khác |
| 3 | `app/Http/Controllers/Admin/UserController.php` | ~56 dòng — `get-list-bot-access` bắt đăng nhập + lọc theo chủ, 8 API `/ajax/supper-admin/*` thêm middleware `supper_admin` | Chặn lộ token/secret qua danh sách bot nhân viên; chặn SysAdmin API cho người thường |
| 4 | `app/Http/Controllers/Basic/FormAnswerController.php` | ~17 dòng — validate 19 đuôi file đã chốt + check magic byte | Chặn upload file giả dạng / thực thi được |
| 5 | `app/Http/Controllers/Mobile/ListFriendController.php` | ~10 dòng — guard quyền bot trước khi gán session | Chặn tài khoản A dùng hash bot của B trên mobile |
| 6 | `app/Http/Middleware/BasicAccess.php` | ~14 dòng — không gán bot lạ vào session ở `basicHome`/`bot.tutorial`, kiểm quyền trước khi đổi bot hiện tại (`select-bot`, `link-point-setting`) | Chặn đổi bot hiện tại sang bot không thuộc user qua mọi trang `/basic/*` |
| 7 | `routes/api.php` | -1 dòng — gỡ route `POST /api/unfollow-line` | Route không còn nơi gọi, có rủi ro bị khai thác |
| 8 | `routes/web.php` | ~4 dòng — điều chỉnh route liên quan guard | Khớp với controller/middleware đã sửa |
| 9 | `tests/Feature/BotAccessGuardTest.php` | **+701 dòng** (file test mới) | PHPUnit cho helper `isBotAccessibleByUser` + các guard chính — chạy trên base thì các ca guard mới FAIL |
| — | `getListBotId` (helper dùng chung) | **KHÔNG sửa** | Đã dùng lại nguyên trạng trong `isBotAccessibleByUser`; staff `is_admin=1` không phải chủ sẽ **không còn vào được bot** đó nữa (regression cần test riêng — 3 dòng trên DB điều tra, không đang được chọn tại thời điểm kiểm) |
| — | Model `Bots` | **KHÔNG sửa** (`$appends` giữ nguyên `hash_botId`) | Các nơi khác ngoài 2 endpoint đã sửa (`check-mode`, `get-list-bot-access`) vẫn trả `hash_botId` như cũ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `supper_admin` middleware mới cho 8 API `/ajax/supper-admin/*` | `UserController.php` + route | Direct | Người không phải SysAdmin nhận 403 |
| F2 | `get-list-bot-access` (danh sách bot cho modal 社員管理) | `UserController.php` | Direct | Bắt đăng nhập, lọc theo chủ, bớt field (không còn token/secret) |
| F3 | `check-mode` (kiểm tra kết nối bot) | `BotController.php` | Direct | Guard quyền + object response chỉ còn `id, is_connected, webhook_url` |
| F4 | step3-check / step5-check (thêm bot) | `BotController.php` | Direct | Guard quyền bot của chính user |
| F5 | `bot-save` (lưu sửa bot) | `BotController.php` | Direct | Guard quyền trước khi xử lý |
| F6 | Middleware `BasicAccess` (mọi trang `/basic/*`) | `BasicAccess.php` | Direct | `select-bot`, `link-point-setting`, `basicHome`, `bot.tutorial` không gán bot lạ vào session |
| F7 | Mobile `list-friend` / `v2/list-friend` (kèm tìm kiếm ajax) | `ListFriendController.php` | Direct | Guard quyền bot trước khi gán session |
| F8 | Upload file form khách (v1/v3, câu hỏi 画像/PDF/動画/音声/指定無し) | `FormAnswerController.php` | Direct | Chỉ nhận 19 đuôi đã chốt + check magic byte |
| F9 | `POST /api/unfollow-line` | `routes/api.php` | Direct | Route bị gỡ, gọi vào nhận 404 |
| F10 | Helper `isBotAccessibleByUser` (mới) | `functions.php` | Direct | Dùng chung bởi F2-F7; nội bộ gọi `getListBotId` |
| F11 | `getListBotId` (hàm dùng chung, KHÔNG sửa code) | — | Indirect | Staff `is_admin=1` không phải chủ không còn qua được guard mới (regression cần test riêng) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | Không có | Dev xác nhận **không có migration / thay đổi dữ liệu** (đã kiểm diff) cả 2 vòng gần nhất |
| D2 | `users.marker` (liên quan bug con #43841, KHÔNG thuộc phạm vi fix) | Không đổi | Chuỗi rỗng và `NULL` được `User::getMarkerAttribute` coi là cùng nghĩa "không có marker" — hành vi có sẵn, không phải data bị update bởi ticket này |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Trang chủ admin / tutorial sau khi đổi bot, thêm bot (`/basic/home`, `/basic/tutorial`) | F6 | Medium — chủ bot/staff đã chấp nhận phải vào được như cũ |
| T2 | Luồng thêm bot v5 (QR / クイック接続) tới trang chủ bot mới | F4, F6 | Medium |
| T3 | Màn cài đặt bot — nút 接続チェック (check-mode) | F3 | Medium — response đổi field, FE phải đọc đúng field mới |
| T4 | Màn sửa bot (bot-save) cho chủ và staff đã chấp nhận | F5 | Medium |
| T5 | 社員管理 — modal chọn bot cho nhân viên | F2 | Medium — response đổi field (bớt token/secret), FE phải đối chiếu |
| T6 | SysAdmin — user detail / bot detail / affiliater | F1 | Low — thêm middleware, luồng dùng đúng vai trò không đổi |
| T7 | App mobile (WebView) `/list-friend`, `/v2/list-friend`, tìm kiếm ajax | F7 | Medium — guard quyền mới, cần test cả bot hợp lệ và bot lạ/đã xoá |
| T8 | Form phía khách v1/v3 — upload file (画像/PDF/動画/音声/指定無し) | F8 | Medium — chặn đúng 19 đuôi, không chặn nhầm file hợp lệ |
| T9 | Module job/callback | F9 | Low — Dev xác nhận không gọi `/api/unfollow-line`, không ảnh hưởng |
| T10 | Nhân viên (`is_admin=1`, không phải chủ) truy cập bot được giao | F11 | **High** — regression tiềm ẩn do dùng lại `getListBotId`, Dev ghi "chưa verify runtime"; cần test riêng theo role staff thường |
| T11 | Bot không có hợp đồng active nhưng vẫn hiển thị trong danh sách (36/231 bot trên DB điều tra) | F2-F7 (điều kiện quyền không bắt hợp đồng active) | Medium — cần xác nhận các bot này vẫn thao tác được bình thường sau fix (chưa đổi behavior này, nhưng chưa verify runtime) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

**Lưu ý riêng cho Leader (ticket đa lỗi + đã có kết quả Studio):**
- Ticket #43715 gom **7 lỗi** (SEC-10 → SEC-16) trong **1 branch fix duy nhất** — chi tiết vector khai thác riêng từng lỗi nằm ở 7 sub-task #43716 → #43722 (chưa fetch trong lần `/new-task` này). Nếu cần review sâu từng lỗi, nên fetch thêm từng sub-task.
- File `04-tc-list.md` đã có **63 TC từ MCP LME TEST STUDIO** (task #500, `aiResult=fail`, 52 pass / 1 fail / 10 other). TC fail (`NEW-47`, ticket #43840) và các TC skip/need-prep **đã được Dev kết luận không do code sửa trong ticket này** (xem mục 1) — Leader cần xác nhận lại trước khi tính vào GAP.
- T10 (staff `is_admin=1` dùng `getListBotId` không sửa) là điểm Dev tự nhận **"chưa verify runtime"** — nên có TC riêng ưu tiên cao.
