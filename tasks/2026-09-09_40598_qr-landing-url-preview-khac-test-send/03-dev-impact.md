# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (hệ thống Auto-fixbug LME) — có DEV XÁC NHẬN / DEV CHỈ ĐẠO ngày 2026-09-09 |
| Commit / Pull Request | `sns-line` commit `8c7e5285eb` (2 commit, 3 file, +70/-21) — Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=40598 |
| Branch | `ai_fixbug_40598` (nhánh gốc `origin/release_step_20260827`) — đã push |
| Ngày submit đánh giá | 2026-09-09 (journal #135377, bản cuối) |
| Auto-filled | `2026-09-09 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ **Ticket có 3 journal auto-fixbug** (#135335 · #135375 · #135377). File này lấy theo **bản cuối #135377** (nội dung trùng #135375, 3 file). Bản đầu #135335 chỉ sửa **2 file** (không đụng `app/Helpers/ChatMessages.php` vì "dev xác nhận file này không còn được sử dụng"), sau đó **DEV CHỈ ĐẠO 2026-09-09 sửa luôn** `ChatMessages.php` → phạm vi mở rộng thêm Step Delivery / Scenario (FA-009) và Broadcast (FA-008). **Không dùng bản #135335 để viết TC.**

---

## 1. Nguyên nhân

Hai cách gửi đi qua hai thành phần khác nhau: gửi thử chạy ở web (PHP), còn hành động khi chạm rich menu chạy ở tiến trình nền (Java) — mỗi bên tự chuyển mã `[LANDING_INTRO_xxx]` theo cách riêng. Khác biệt gồm:

- **(a)** mã định danh người nhận nhúng trong link khác nhau vì người nhận khác nhau (**đúng thiết kế**);
- **(b)** web thay mã **TRƯỚC** bước rút gọn URL nên link giới thiệu bị rút gọn, còn job rút gọn **TRƯỚC** rồi mới thay mã nên link giữ dạng đầy đủ; thêm nữa job dùng **tên miền rút gọn riêng của tài khoản** còn web dùng **tên miền hệ thống**;
- **(c)** job **không ghi** cặp thay thế của mã giới thiệu vào bảng thay thế của tin nhắn nên màn hình xem lại vẫn hiện nguyên chuỗi mã, trong khi web có ghi (nhưng ghi bản đầy đủ, khác link rút gọn đã gửi).

Link thực nhận vẫn đúng ở cả hai đường.

## 2. Cách fix

Hai commit, 3 file.

1. **Sửa biểu thức chặn rút gọn URL nội bộ viết sai ở 8 chỗ**: `stripos($v[0], '/landing-qr/' == false)` → `stripos($v[0], '/landing-qr/') === false` — `TemplateService.php` (2), `ChatMessages.php` (2), `Basic/UserController.php` (4). Vế phải cũ luôn thành chuỗi rỗng nên nhánh bỏ qua **không bao giờ chạy**.
2. **Đổi thứ tự dựng nội dung tin cho giống phía job ở CẢ HAI bản sao hàm rút gọn** (`TemplateService::sendShortUrl` và `ChatHelper::sendShortUrl`): thay thông tin bạn bè và tên **trước**, rút gọn URL, rồi mới **dựng link từ mã ở cuối**; tách 4 lời gọi dựng link thành hàm `makeLinkInMessage` ở mỗi lớp.
   - Bên `TemplateService` còn **bỏ dựng link khỏi `replaceMessageText`** (chỉ dựng ở đó khi bot **TẮT** rút gọn, vì lúc đó tin không đi qua `sendShortUrl`); riêng `getTemplate` xét cờ của **mẫu tin** nên nhánh không rút gọn của nó gọi `makeLinkInMessage` trực tiếp.
   - Kèm bổ sung `return $message;` còn thiếu trong nhánh **bắt lỗi** của `makeLinkLandingPageIntro` ở **cả hai file**, vì sau khi đổi thứ tự đây là lời gọi cuối trước khi trả kết quả.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TemplateService::makeLinkLandingPageIntro` — app/Services/TemplateService.php:1377 | Có — thêm `return $message;` ở nhánh bắt lỗi | Là lời gọi cuối trước khi trả kết quả sau khi đổi thứ tự |
| 2 | `TemplateService::sendShortUrl` — app/Services/TemplateService.php:1016 | Có — đổi thứ tự: replace friend info/name → rút gọn → dựng link | Trước gọi `makeLinkLandingPageIntro` rồi mới rút gọn → link bị rút gọn |
| 3 | `TemplateService::getTemplate` — app/Services/TemplateService.php:83 | Có — nhánh không rút gọn gọi `makeLinkInMessage` trực tiếp | Nhánh text của luồng gửi thử; xét cờ của **mẫu tin** chứ không phải cờ bot |
| 4 | `TemplateService::replaceMessageText` | Có — bỏ dựng link, chỉ dựng khi bot TẮT rút gọn | Tránh dựng link 2 lần; 15/16 nơi gọi đóng mở bằng đúng điều kiện `$bot->is_shorten_url` |
| 5 | `TemplateService::sendTestTemplate` — app/Services/TemplateService.php:2606 | Đã check | Luồng gửi thử của màn template |
| 6 | `TemplateService::generateContentPreview` / `generateCode` — :2072 / :2184 | Đã check | Dựng `replace_content` cho preview; khối LANDING_INTRO ở dòng 2309 |
| 7 | `ChatHelper::sendShortUrl` — app/Helpers/ChatMessages.php | Có — cùng thay đổi như (2) + tách `makeLinkInMessage` + `return $message;` ở nhánh bắt lỗi | DEV CHỈ ĐẠO 2026-09-09: sửa luôn bản sao thứ hai để hai đường gửi ra cùng kết quả |
| 8 | `Basic/UserController` — `executeActionOpenMobile` / `executeActionOpenMobileNormal` | Có — sửa biểu thức chặn ở 4 chỗ (:3145, :3289, :3292, :3616, :3619) | Cùng lỗi biểu thức; nơi này còn gọi thẳng `new ChatMessages()` |
| 9 | `ChatController` — dựng preview tin nhắn — app/Http/Controllers/ChatController.php:6042-6110 | Đã check | Ghép `capture_template.content` với `replace_content` |
| 10 | route `pageIntro` — routes/web.php:831 → `Basic\QRCodeController@pageIntro` | Đã check | Đích của link giới thiệu |
| 11 | `UrlModel.replaceLandingQRLink` / `detectLandingQR` — linect-service UrlModel.java:183-201 | **KHÔNG sửa** (phía Java) | Bản đối chiếu phía job |
| 12 | `MessageBuilder.buildTextMessageFromHelper` — linect-service MessageBuilder.java:382-396 | **KHÔNG sửa** | `urlShorting` chạy TRƯỚC `replaceLandingQRLink` — thứ tự mà web được sửa cho giống |
| 13 | `MessageBuilder.buildTextMessage` — linect-service MessageBuilder.java:521-531 | **KHÔNG sửa** | Cùng thứ tự |
| 14 | `MessageBuilder.replaceFriendInfo` — linect-service MessageBuilder.java:4081 | **KHÔNG sửa** | Nơi **DUY NHẤT** ghi `mapReplaceContent`, **không có LANDING_INTRO** → gốc của vấn đề preview (c) |
| 15 | `SentMessageHelper.setReplaceContent` — linect-service SentMessageHelper.java:205/418/588 | **KHÔNG sửa** | Ghi bảng thay thế phía job |
| 16 | `HandlePostbackTask` — linect-service HandlePostbackTask.java:3466-3495 | **KHÔNG sửa** | Chạm rich menu → doAction → gửi template |

**Đã loại khỏi phạm vi test (DEV XÁC NHẬN 2026-09-09):**
- Gửi lại tin ở màn danh sách lỗi phát hành — đã chuyển sang job.
- Hai daemon `HandleCallbackMessage::checkAutoReply` và `HandleCallbackPostback::responseMessage` — không còn dùng.

**Lối vào `ChatHelper::sendShortUrl` còn lại nhưng CHƯA được xác nhận còn dùng (Dev để ưu tiên thấp khi test):**
- `Api/ChatController@sendMessage` (chat văn bản trên app)
- `ChatController@sendMessage` (route cũ `/basic/send_message`, còn được blade mobile `chat_11` và `mypage_v2` nhúng)
- `Api/CallbackPostbackApiController@responseMessage`
- `Admin/BotController` `responseMessage` / `checkAutoReply`

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `TemplateService::sendShortUrl` + `makeLinkInMessage` + `makeLinkLandingPageIntro` | app/Services/TemplateService.php | Direct | Đổi thứ tự dựng nội dung + thêm `return $message;` nhánh catch |
| F2 | `TemplateService::replaceMessageText` | app/Services/TemplateService.php | Direct | Bỏ dựng link; nay **phụ thuộc ngầm** vào cờ `$bot->is_shorten_url` |
| F3 | `TemplateService::getTemplate` (nhánh text) | app/Services/TemplateService.php:83 | Direct | Xét cờ của **mẫu tin**; nhánh không rút gọn gọi `makeLinkInMessage` trực tiếp |
| F4 | `ChatHelper::sendShortUrl` + `makeLinkInMessage` (bản sao thứ 2) | app/Helpers/ChatMessages.php | Direct | Áp cùng thay đổi theo DEV CHỈ ĐẠO |
| F5 | Biểu thức chặn rút gọn URL nội bộ `/landing-qr/` — 8 chỗ | TemplateService.php (2) · ChatMessages.php (2) · Basic/UserController.php (4) | Direct | Nhánh bỏ qua trước đây **không bao giờ chạy**, nay có hiệu lực |
| F6 | `Basic/UserController::executeActionOpenMobile` / `executeActionOpenMobileNormal` | app/Http/Controllers/Basic/UserController.php:3145,3289,3292,3616,3619 | Direct | Vừa sửa biểu thức, vừa gọi thẳng `new ChatMessages()` |
| F7 | `TemplateService::detectContent` / `QuickReplyService::detectContent` (quick reply) | 2 bản riêng | Indirect | Nội dung nút trả lời nhanh dựng qua đường vừa đổi thứ tự |
| F8 | `TemplateService::makeImageMapVer2` / `ChatHelper::makeImageMap` | — | Indirect | URL trong vùng bấm của ảnh và nút |
| F9 | `TemplateService::sendMessageAction` · `HelperService::sendAction` · `LiffController::sendMessageAction` | — | Indirect | Các đường gửi tin theo hành động |
| F10 | `TemplateService::generateContentPreview` / `generateCode` + `ChatController` dựng preview | :2072 / :2184 / ChatController.php:6042-6110 | Indirect | Preview/history — **web có ghi replace_content, job KHÔNG ghi** |
| F11 | 15 nơi gọi `replaceMessageText` (FormAnswerService · CalendarCourseBookingService · CalendarSalonLineBookingService · EventBookingService · SalesService …) | — | Indirect | Không sửa code nhưng phụ thuộc ngầm vào cờ `is_shorten_url`; **nơi gọi MỚI không theo nếp này sẽ gửi đi nguyên mã** |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `url` / `url_shorten` | CREATE (giảm) | **Không còn sinh bản ghi rút gọn** cho link dựng từ mã trong tin (gồm `/landing/page-intro/`). Bản ghi cũ **giữ nguyên**, link rút gọn đã gửi vẫn chuyển hướng bình thường |
| D2 | `url` / `url_shorten` — mọi URL trỏ về miền hệ thống | CREATE (giảm) | Vì môi trường thật **CÓ khai báo BASE_URL** nên nhánh chặn nay có hiệu lực → **mọi** URL cùng miền hệ thống (trừ `/landing-qr/`) thôi được rút gọn → **mất số liệu lượt bấm** của những link đó. 🔴 **Cần PM xác nhận** |
| D3 | Bảng thay thế của tin nhắn (`replace_content` / `mapReplaceContent`) | — (không sửa) | Web **có ghi**, job Java **KHÔNG ghi** cặp thay thế của mã giới thiệu → preview/history phía job vẫn hiện nguyên chuỗi mã. **Fix không chạm phần này** |

**RECOVER DATA:** ✔ Không cần recover data.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **QR Code Action / Landing (FA-017)** — trọng tâm ticket: mã `[LANDING_INTRO_xxx]` phải ra link đầy đủ `.../landing/page-intro/<mã QR>/<mã người nhận>` | F1, F5, D1 | **High** |
| T2 | **Message Template (FA-010)** — gửi thử mẫu tin ở màn mẫu tin (`/ajax/template-v2/send-test-template-v3`, qua TemplateService) | F1, F2, F3 | **High** |
| T3 | **Step Delivery / Scenario (FA-009)** — nút gửi thử ở màn kịch bản (`/ajax/template-v2/send-test-template`, qua ChatHelper) | F4 | **High** |
| T4 | **Broadcast (FA-008)** — nút gửi thử ở màn gửi tin hàng loạt (cùng route trên, qua ChatHelper) | F4 | **High** |
| T5 | **1-on-1 Chat (FA-001)** — chat 1:1 trên web: gửi mẫu tin (gồm nhánh sửa nội dung ngay trước khi gửi) và gửi tin văn bản | F1, F4 | **High** |
| T6 | **1-on-1 Chat trên app điện thoại (FA-001)** — gửi mẫu tin từ app (`Api ChatController::sendTemplate`) | F1 | Medium |
| T7 | **Action Settings (SC-004) / Action Schedule (FA-016)** — tin gửi khi chạy hành động: `TemplateService::sendMessageAction`, `HelperService::sendAction`, và mở hành động từ điện thoại (`executeActionOpenMobile` / `executeActionOpenMobileNormal`) | F6, F9 | **High** |
| T8 | **Form Builder (FA-011) + Point** — tin trả lời sau khi khách gửi biểu mẫu và tin tặng điểm (`FormAnswerService` `sendMessageReply` / `sendActionPoint`) | F11 | Medium |
| T9 | **Lesson / Calendar Booking (FA-019)** — tin gửi khi đặt lịch bài học (`CalendarCourseBookingService`) | F11 | Medium |
| T10 | **Salon Booking (FA-020)** — tin gửi khi đặt lịch salon (`CalendarSalonLineBookingService`) | F11 | Medium |
| T11 | **Event Booking (FA-021)** — tin gửi khi đặt lịch sự kiện (`EventBookingService`) | F11 | Medium |
| T12 | **Single Product / Sales (FA-026)** — tin gửi trong luồng bán sản phẩm (`SalesService`) | F11 | Medium |
| T13 | **Quick reply** — nội dung nút trả lời nhanh, dựng ở hai bản riêng (`TemplateService::detectContent` và `QuickReplyService::detectContent` qua ChatHelper) | F7 | Medium |
| T14 | **Rich message / image map** — URL gắn trong vùng bấm của ảnh và nút (`TemplateService::makeImageMapVer2` và `ChatHelper::makeImageMap`) | F8 | Medium |
| T15 | **LIFF (mở link trong LINE)** — tin gửi theo hành động khi khách mở link (`LiffController::sendMessageAction`) | F9 | Medium |
| T16 | **URL Analytics (FA-023)** — kiểm ngược: URL của khách trỏ ra ngoài **VẪN phải** được rút gọn và vẫn đếm lượt bấm; URL trỏ về miền hệ thống thì **CÓ CHỦ Ý** thôi rút gọn (trừ link quét mã `/landing-qr/`) | D1, D2, F5 | **High** |

---

## Ma trận test Dev yêu cầu (áp cho MỖI tính năng ở 4.3)

| # | Điểm kiểm |
|---|---|
| (a) | Tin chứa mã `[LANDING_INTRO_x]` ra **link đầy đủ**, bấm vào mở đúng trang giới thiệu và **ghi đúng người giới thiệu** |
| (b) | Tin chứa `[FORM_x]` / `[CONVERSION_x]` / `[ITEM_x]` / `[CANCEL_x]` / `[CHANGE_x]` vẫn ra link đúng |
| (c) | URL của khách trỏ **ra ngoài** VẪN được rút gọn và đếm lượt bấm; URL trỏ về **miền hệ thống** thì thôi rút gọn (chủ ý) |
| (d) | `{name}` và `[FRIEND_INFO_x]` thay đúng giá trị, **kể cả khi nằm trong URL** |
| (e) | Chạy lại với cờ rút gọn của **bot** BẬT và TẮT, **nhân với** cờ rút gọn của **mẫu tin** BẬT và TẮT |

## Rủi ro / lưu ý khi test (Dev tự nêu)

1. 🔴 Khi **BASE_URL có giá trị** (môi trường thật có), **MỌI URL trỏ về miền hệ thống thôi được rút gọn** nên **mất số liệu lượt bấm** của những link đó — **cần PM xác nhận** vì hệ thống đã chạy nhiều năm với chốt chặn không hoạt động.
2. `replaceMessageText` nay **phụ thuộc ngầm** vào cờ `$bot->is_shorten_url` để biết ai dựng link; đúng với toàn bộ 15 nơi gọi hiện tại, **nơi gọi MỚI không theo nếp này sẽ gửi đi nguyên mã** — đã ghi chú tại chỗ trong code.
3. Phần **thay tên và thông tin bạn bè nay chạy sớm hơn**: URL có nhúng `{name}` hoặc `[FRIEND_INFO_x]` sẽ được rút gọn với **giá trị thật** thay vì còn nguyên mã — sửa đúng nhưng là **thay đổi quan sát được**.
4. Nhánh **trả lời nhanh qua ChatHelper** trước thay tên bằng `$line_user_info['name']` **sau** khi rút gọn, nay bằng `$lineUser->name` **trước** đó; **cần xác nhận hai giá trị luôn như nhau**.
5. **Hai bản sao hàm rút gọn vẫn tồn tại song song**; lần sau sửa quy tắc phải nhớ cả hai.

## Mức verify của Dev

- **Mức: lint** — `php -l` cả 3 file: No syntax errors detected.
- Rà 16 nơi gọi `replaceMessageText`: 15 nơi đóng mở bằng đúng điều kiện `$bot->is_shorten_url`; nơi còn lại là `getTemplate` xét cờ mẫu tin và đã sửa riêng.
- `php -r` kiểm biểu thức tìm URL: `[LANDING_INTRO_9NTTkr]` KHÔNG bị nhận là URL nên không thể lọt vào bước rút gọn.
- `php -r` đối chiếu hai vế biểu thức chặn: bản mới trả `true` với URL nội bộ, `false` với URL chứa `/landing-qr/`.
- Đối chiếu đủ 4 tổ hợp cờ rút gọn của bot và của mẫu tin: mọi tổ hợp dựng link đúng một lần.
- `git diff --stat`: 3 file, +70/-21.
- ⚠️ **KHÔNG chạy được unit test** — các hàm này đụng DB; dev DB cũng không kết nối được (`host.docker.internal:3306 Connection refused`).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] 🔴 **Đã chốt với PM** về việc mất số liệu lượt bấm của URL cùng miền hệ thống (D2)
- [ ] 🔴 **Đã chốt với Dev/PM** phần **(b) preview text** của khách — fix chỉ chạm web/PHP, phía job Java (`MessageBuilder.replaceFriendInfo` không ghi LANDING_INTRO vào `mapReplaceContent`) **chưa được sửa**
