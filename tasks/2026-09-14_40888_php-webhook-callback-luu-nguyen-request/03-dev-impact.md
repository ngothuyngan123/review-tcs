# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — author Redmine: Thanh Duy Nguyen · assignee: Ngô Thúy Ngần |
| Commit / Pull Request | `sns-line` commit `272e29d0c2` (7 file) · Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40888 |
| Branch | `ai_small_40888` (nhánh gốc `release_step_20260805`) — đã push lên origin. **Phụ thuộc job** `linect-service`: `m_202609_forward_webhook_40475_cb_full_request` (b47e086) + `m_202609_forward_webhook_40475_release-callback` (f6104a3) |
| Ngày submit đánh giá | `2026-09-14` (Journal #136271) |
| Auto-filled | `2026-09-14 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Khi LINE gọi webhook, phía PHP **giải mã JSON rồi mã hoá lại từng sự kiện** trước khi ghi vào bảng lưu callback. Vì vậy nội dung lưu **không còn là request gốc**:

- **Mất lớp bao ngoài** (`destination` + `events`).
- Ký tự **tiếng Nhật / emoji bị đổi sang dạng escape** (`\uXXXX`).
- **Mỗi lần LINE gọi bị tách thành nhiều bản ghi**, trong đó **chỉ 2 sự kiện đầu được lưu** — sự kiện thứ 3 trở đi bị bỏ khi LINE gộp nhiều tin dồn dập.

Tính năng **chuyển tiếp webhook sang hệ thống ngoài** (Webhook転送, #40475) lại gửi lại đúng chuỗi đã lưu với yêu cầu **giữ nguyên trạng** (`加工せずそのまま`, spec 2026-09-12), nên bắt buộc phải lưu đúng body gốc. Phía job đã được sửa để đọc được **cả định dạng đầy đủ mới lẫn định dạng cũ**.

> Dev ghi nhận: bug này **đã lặp lại nhiều lần** ở các ticket #37235 / #37631 / #37700 / #38033 nhưng chưa từng được đưa lên.

## 2. Cách fix

**Refix vòng 1 theo AI review độc lập, 2 lỗi bắt buộc.**

**(1) Đọc nhầm sự kiện.** Vì mỗi lần LINE gọi nay chỉ tạo **1 bản ghi chứa đủ mọi sự kiện**, sự kiện mở đầu có thể là loại báo đã gửi tin (`delivery`) trong khi cột `type` / `line_id` của bản ghi lại ghi theo **sự kiện đầu tiên KHÁC delivery** — 4 chỗ phía PHP vẫn đọc cứng **sự kiện thứ nhất** nên lấy nhầm:

- mất thao tác bấm nút của khách (postback), hoặc
- xử lý **kết bạn / hủy kết bạn cho SAI người**.

Đã thêm **hàm dùng chung `callbackEventsMainFirst()`** đưa đúng sự kiện ứng với cột `type` của bản ghi lên đầu, thứ tự ưu tiên:
1. trùng đúng cột `type` →
2. sự kiện đầu tiên khác `delivery` →
3. không khớp thì giữ nguyên.

Gọi ở **cả 4 chỗ đọc**, nhờ vậy toàn bộ đoạn code phía sau (kể cả hàm phản hồi tin nhắn dùng chung) tự khớp mà không phải sửa rải rác.

**(2) Rủi ro 1 bản ghi lẫn nhiều loại sự kiện.** Đã tải **THẬT** 2 nhánh job nêu trong ticket về kiểm chứng:

- Job **KHÔNG** định tuyến theo cột `type` của bản ghi mà theo loại của **TỪNG sự kiện** (gom các sự kiện liền kề cùng loại rồi gọi đúng nhánh xử lý).
- Job lấy bản ghi **theo trạng thái** chứ không lọc theo cột `type`.

→ không có chuyện chạy nhầm kịch bản kết bạn hay chặn nhầm bạn bè. Đã ghi dẫn chứng file + dòng + mã commit vào phần Bằng chứng & Verify và ghi rõ giả định này vào chú thích hàm lưu callback.

**Bổ sung 9 unit test** cho các gói `[delivery, message]`, `[delivery, postback]`, `[message, follow]` và các trường hợp biên.

**Hành vi cũ được giữ nguyên:** bỏ qua request chỉ có sự kiện loại `delivery` · đánh dấu bot đã xác thực khi LINE gửi danh sách sự kiện rỗng · xác thực chữ ký trước khi lưu.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BotController::callbackWebHook` (`app/Http/Controllers/Admin/BotController.php`) | Sửa | Điểm nhận webhook EP-24 — gọi sang hàm lưu nguyên văn mới |
| 2 | `BotController::storeCallbackEventRaw` (`app/Http/Controllers/Admin/BotController.php`) | **Hàm mới** | Lưu nguyên văn body vào `callback_event.request`, tính `type` / `line_id` theo event đầu tiên khác `delivery` |
| 3 | `parseCallbackEventRequest` (`app/Helpers/functions.php`) | **Hàm mới** | Đọc song song 2 định dạng (body đầy đủ mới / mảng event cũ) |
| 4 | `callbackEventsMainFirst` (`app/Helpers/functions.php`) | **Hàm mới** | Đưa event khớp cột `type` của bản ghi lên vị trí số 0 |
| 5 | `HandleCallback::handle` (`app/Console/Commands/HandleCallback.php`) | Sửa | Tiến trình kết bạn / hủy kết bạn — 1 trong 4 chỗ đọc event |
| 6 | `HandleCallbackMessage::handle` (`app/Console/Commands/HandleCallbackMessage.php`) | Sửa | Tiến trình tin nhắn — 1 trong 4 chỗ đọc event |
| 7 | `HandleCallbackPostback::handle` (`app/Console/Commands/HandleCallbackPostback.php`) | Sửa | Tiến trình postback — 1 trong 4 chỗ đọc event |
| 8 | `CallbackPostbackApiController::handleCallbackPostback` (`app/Http/Controllers/Api/CallbackPostbackApiController.php`) | Sửa | Endpoint xử lý postback nội bộ — 1 trong 4 chỗ đọc event |
| 9 | `UserController::storeFakeCallbackEvent` (`app/Http/Controllers/Basic/UserController.php`) | **Đã đọc, GIỮ NGUYÊN** | Callback nội bộ (postback giả lập) → vẫn sinh bản ghi **định dạng CŨ** |
| 10 | `HandlePostbackTask.parseCallbackEventData` (`linect-service`, phía job) | Sửa (branch của dev) | Đã hỗ trợ 2 định dạng |
| 11 | `HandleForwardCallbackEventTask.buildBody` (`linect-service`, phía job) | Không sửa | Gửi nguyên chuỗi `request` ra ngoài — là bên tiêu thụ chính của fix này |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev kê theo "file thay đổi"; gán mã F* để map coverage. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BotController::callbackWebHook` + `storeCallbackEventRaw` (hàm mới) | `app/Http/Controllers/Admin/BotController.php` | Direct | Điểm ghi `callback_event` — trung tâm của fix. Bao cả nhánh `bot_type=0` và `bot_type=1` |
| F2 | `parseCallbackEventRequest` + `callbackEventsMainFirst` (2 hàm mới dùng chung) | `app/Helpers/functions.php` | Direct | **Hàm dùng chung** — 4 caller ở F3–F6. Xem RULE hàm dùng chung: cần danh sách caller đầy đủ |
| F3 | `HandleCallback::handle` | `app/Console/Commands/HandleCallback.php` | Direct | Tiến trình kết bạn / hủy kết bạn |
| F4 | `HandleCallbackMessage::handle` | `app/Console/Commands/HandleCallbackMessage.php` | Direct | Tiến trình tin nhắn |
| F5 | `HandleCallbackPostback::handle` | `app/Console/Commands/HandleCallbackPostback.php` | Direct | Tiến trình postback |
| F6 | `CallbackPostbackApiController::handleCallbackPostback` | `app/Http/Controllers/Api/CallbackPostbackApiController.php` | Direct | Endpoint postback nội bộ |
| F7 | `CallbackEventRequestParseTest` | `tests/Feature/CallbackEventRequestParseTest.php` | Direct (test) | 19 tests / 59 assertions, thêm 9 test mới |
| F8 | `UserController::storeFakeCallbackEvent` | `app/Http/Controllers/Basic/UserController.php` | **Indirect — KHÔNG sửa** | Vẫn sinh bản ghi định dạng cũ → nguồn dữ liệu để verify đọc song song 2 định dạng |
| F9 | `HandlePostbackTask.parseCallbackEventData` · `handleCallbackEventByType` · `startJobGetEvent` | `linect-service` (job Java) | Indirect — repo khác | Bên tiêu thụ; phải deploy kèm 2 branch job |
| F10 | `HandleForwardCallbackEventTask.buildBody` | `linect-service` (job Java) | Indirect — repo khác | Gửi nguyên chuỗi ra hệ thống ngoài; đang gọi `unescapeUnicode` để bù cho PHP mã hoá lại |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `callback_event.request` | UPDATE (đổi nội dung ghi vào) | Từ nay chứa **body đầy đủ** LINE gửi (có `destination` + `events`) thay vì mảng sự kiện. **Bản ghi cũ giữ nguyên định dạng cũ**; cả job lẫn PHP đọc được 2 dạng → **KHÔNG cần migrate dữ liệu cũ**. ⚠️ Cột kiểu **TEXT (~65.535 byte)** — body lớn hơn bị **cắt cụt âm thầm**, đã thêm log cảnh báo |
| D2 | `callback_event.type` · `callback_event.line_id` | UPDATE (đổi cách tính) | Lấy theo **sự kiện đầu tiên khác `delivery`** của request. **1 bản ghi có thể chứa nhiều sự kiện khác loại** → cột `type` chỉ mô tả được 1 loại. Phía đọc: job định tuyến theo `type` của TỪNG sự kiện; 4 chỗ PHP đưa đúng sự kiện khớp cột `type` lên đầu trước khi xử lý. Event không có `source.userId` → `line_id` để **rỗng** thay vì lỗi máy chủ |
| D3 | `callback_event.webhook_event_id` | **KHÔNG ghi (giữ nguyên hiện trạng)** | PHP vẫn không ghi cột này → cơ chế **chống trùng khi LINE gửi lại (redelivery)** của job **chưa kích hoạt** cho bản ghi do PHP tạo. Dev ghi rõ **ngoài phạm vi ticket** → đề nghị ticket riêng |
| D4 | `bots.is_verify` | UPDATE | Giữ hành vi cũ: bot `bot_type=0`, request **không có event nào** (events rỗng / thiếu hẳn) → set `is_verify=1` và **không tạo bản ghi** `callback_event` |
| D5 | **Số lượng bản ghi** `callback_event` | CREATE (đổi số lượng) | 1 lần LINE gọi = **đúng 1 bản ghi** (trước đây tách nhiều bản ghi, mất event thứ 3 trở đi) |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Chat 1:1 (FA-002)** | F1, F2, F4, D1, D2, D5 | **High** — toàn bộ tin nhắn bạn bè gửi đến đi qua bảng callback này; nay không còn mất sự kiện thứ 3 trở đi khi LINE gộp nhiều tin dồn dập |
| T2 | **Webhook転送 / Forward webhook (#40475)** | F1, F10, D1 | **High** — nội dung chuyển tiếp ra hệ thống ngoài nay đúng nguyên trạng LINE gửi (đủ `destination`, không escape unicode). Là lý do chính của ticket |
| T3 | **Friend Information (FA-001)** | F2, F3, D2 | **High** — sự kiện kết bạn / hủy kết bạn đi cùng đường lưu callback này; lỗi chọn event = xử lý **SAI người** |
| T4 | **Auto Reply (FA-003)** | F2, F5, F6, D1, D2 | **Medium** — sự kiện postback từ nút đọc từ cùng cột `request` |
| T5 | **Rich Menu (FA-004)** | F2, F5, F6, D1, D2 | **Medium** — sự kiện postback từ rich menu đọc từ cùng cột `request` |
| T6 | **Xác thực webhook URL của LINE (bot connect)** | F1, D4 | **Medium** — bước LINE verify đường dẫn webhook phải vẫn set `is_verify=1` và không sinh bản ghi rác |

---

## 5. Recover data

✔ **Không cần recover data** (Dev ghi rõ) — bản ghi cũ giữ định dạng cũ, cả 2 phía đều đọc được.

## 6. Mức verify Dev đã làm

| Mục | Nội dung |
|---|---|
| Mức | **unit-test** (không có test tích hợp / không có dữ liệu thật) |
| Lệnh | `php -l` trên 7 file PHP: No syntax errors · `phpunit --filter CallbackEventRequestParseTest`: **OK (19 tests, 59 assertions)** · `phpunit tests/Feature`: 66 tests — 1 error + 2 failures **nền sẵn** ở `BillingServiceTest` (ngày hết hạn) và `ExampleTest` (cần HTTP/DB), **KHÔNG phát sinh lỗi mới** |
| Kiểm chéo job | Đã `git fetch` **THẬT** 2 branch dev từ origin `linect-service` rồi đọc code, không suy đoán |
| ⚠️ Hạn chế | **Không kết nối được MySQL dev** (`host.docker.internal:3306` refused) → **không dump được dữ liệu thật**; cấu trúc cột lấy từ snapshot schema `/workspace/share/db` |

**Bằng chứng Dev dẫn (rủi ro "1 row nhiều event khác loại"):**

- `HandlePostbackTask.handleCallbackEventByType()` — `src/main/java/sns/line/task/HandlePostbackTask.java` **dòng 416-470** (branch `b47e086`), gọi tại **dòng 366**: gom các event **LIỀN KỀ** cùng type rồi switch sang đúng handler (`follow`/`unfollow`/`postback`/`message`/`videoPlayComplete`/`join`/`leave`/`unsend`). Javadoc ghi rõ: *"Cột type của row chỉ lưu được 1 type nên không dùng để dispatch được: dispatch theo type của CHÍNH từng event"* → gói `[unfollow A, message B]` hay `[follow A, message B]` **KHÔNG** bị xử lý nhầm loại.
- Job lấy row **theo STATUS**: `callbackEventRepository.findAllByStatus(CallbackEvent.STATUS_NEW)` — `startJobGetEvent` **dòng 161** → không row nào bị bỏ sót.
- Job đọc được định dạng mới: `parseCallbackEventData` **dòng 4803-4820** — phân biệt full body và mảng cũ bằng ký tự mở đầu; events rỗng/thiếu → trả list rỗng.
- Phía PHP (trước fix): 4 chỗ tiêu thụ lấy row **THEO cột type** và chỉ đọc phần tử số 0, **KHÔNG hề lặp mảng event** (grep 4 file: không có `foreach ($body`, không có `$body[1]`, không có `count($body)`) → đã thêm `callbackEventsMainFirst()`.

## 7. Rủi ro / lưu ý khi test (Dev tự nêu)

| # | Rủi ro | Trạng thái |
|---|---|---|
| R1 | 1 row chứa nhiều event **khác loại** → job chạy nhầm kịch bản kết bạn / chặn nhầm bạn bè | ★ **ĐÃ KIỂM CHỨNG — không còn là rủi ro** (job dispatch theo type từng event) |
| R2 | 1 row có **nhiều event CÙNG loại** → 3 tiến trình PHP cũ (`HandleCallback`/`HandleCallbackMessage`/`HandleCallbackPostback`) chỉ xử lý **MỘT** event, các event sau **chưa được xử lý** | ⚠️ **CÒN TỒN TẠI** — chỉ ảnh hưởng nếu 3 tiến trình này còn chạy song song với job. **Cần xác nhận đã dừng hẳn** |
| R3 | Cột `request` kiểu **TEXT (~65.535 byte)** → body quá lớn bị **cắt cụt âm thầm** (kết nối không bật chế độ nghiêm ngặt) | ⚠️ **CÒN TỒN TẠI** — đã thêm log cảnh báo; thấy log thì phải đổi cột sang `MEDIUMTEXT` |
| R4 | `webhook_event_id` chưa được PHP ghi → chống trùng khi LINE **gửi lại (redelivery)** chưa kích hoạt | ⚠️ **NGOÀI PHẠM VI TICKET** — đề nghị ticket riêng (1 row nay chứa nhiều event với nhiều mã khác nhau) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ `parseCallbackEventRequest` / `callbackEventsMainFirst` là **hàm dùng chung**, Dev kê 4 caller: F3, F4, F5, F6
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
