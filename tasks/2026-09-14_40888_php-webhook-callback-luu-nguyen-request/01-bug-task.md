# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40888 — [PHP] Webhook callback phía PHP lưu nguyên request nhận được từ phía LINE` |
| Module / Màn hình | `<chưa rõ — tester fill>` — Redmine không set category. Suy từ mô tả: **endpoint webhook LINE EP-24** (`BotController::callbackWebHook`, `app/Http/Controllers/Admin/BotController.php`) → bảng `callback_event`. Tính năng tiêu thụ: Webhook転送 / Forward webhook (#40475) · Chat 1:1 (FA-002) · Friend Information (FA-001) · Auto Reply (FA-003) · Rich Menu (FA-004) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine vốn đã là tiếng Việt — giữ nguyên văn, không diễn giải lại. -->

- Staging đang nhận callback từ php nên cần sửa cách lưu body callback
- Đọc thêm tài liệu của LINE https://developers.line.biz/en/docs/messaging-api/receiving-messages/
- `callback_event.request` giờ sẽ đầy đủ body nên cần support thêm cả case dạng đầy đủ này. Dưới đây là ví dụ:

```json
{
    "destination": "U97d458aefc8bc8faa05ae667dd0f84a8",
    "events": [
        {
            "type": "message",
            "message": {
                "type": "text",
                "id": "591547874899656962",
                "quoteToken": "lHQ6nqqCZypYGIos6cNQwvSoug2ibWvH-TpC7zWHslgSQb0G31GBStavoEcexLvrOYtqTuDsW3wJPzzpEYynLEWbunTSivqLI748sxI_WzWTxSi1py3re2sEbeiomfY8q-dWg6QbCs7bh7oZayGKuw",
                "markAsReadToken": "oAgyS-j1crLV2dpRrBk9EJzcvsdD4YAd9RS14ZG_bdgnEBOaCUrGqWrfMH-BjsOkZ-yvMCWKVRAVIVoHJIOgD0e-LIkXZK9rIbXM52enPkakz4tOogtgYMJVURHm60cVSmGl51h-q-VytxvO_IBm4XUpxaPnMVB5_2iveZmQsFxiyVy6pLYVI3x2J8I0Ww8P_q_VK34TeqmuSHUr_qEQHw",
                "text": "Chao 0618 セージをご確認ください"
            },
            "webhookEventId": "01KC5MYVNCNKH0R4EW1W8AVEZ2",
            "deliveryContext": {
                "isRedelivery": false
            },
            "timestamp": 1765421313652,
            "source": {
                "type": "user",
                "userId": "Ud9dd81da2ef9931781fbcd71d565b57a"
            },
            "replyToken": "5f3f612b60f74e21b78b5078f4be2772",
            "mode": "active"
        }
    ]
}
```

Phía job đã sửa ở 2 branch nhận và xử lý callback:

- `m_202609_forward_webhook_40475_release-callback`
- `m_202609_forward_webhook_40475_cb_full_request`

## Steps to reproduce

<!-- Ticket KHÔNG có Section "Tái hiện bug" — tracker "Improve nội bộ", là yêu cầu đổi cách lưu chứ không phải bug report từ khách hàng. -->

## Expected result

<!-- Ticket không ghi theo format Expected. Yêu cầu gốc: cột `callback_event.request` lưu NGUYÊN VĂN body LINE gửi (còn `destination` + `events`, không escape unicode); 1 lần LINE gọi = 1 bản ghi giữ đủ mọi event. -->

## Actual result

<!-- Ticket không ghi theo format Actual. Hiện trạng (theo mục 1 của Journal #136271): PHP giải mã JSON rồi mã hoá lại từng event → mất lớp bao ngoài, chữ Nhật/emoji bị đổi thành escape `\uXXXX`, mỗi lần LINE gọi bị tách nhiều bản ghi và chỉ 2 event đầu được lưu. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40888 KHÔNG có attachment nào. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được bằng thao tác người dùng thường** — ticket tracker **Improve nội bộ**, không có Section "Tái hiện bug" (Steps / Expected / Actual trống). Root cause + cách fix do AI Auto-fixbug xác định (xem file 03). TCs nên tập trung **verify cách fix + regression impact**, không phải verify hiện tượng bug.

**Môi trường phát hiện / test:** description ghi rõ **Staging đang nhận callback từ PHP**.

⚠️ **Task này CHỈ apply cho staging — production KHÔNG có** (Leader xác nhận 2026-09-15): chỉ staging mới có loại callback do PHP insert.
→ `env_scope` đúng là **`local` · `dev` · `staging`**, **không** gồm `prd`. Không áp RULE-08 theo hướng "phải test production" cho task này.
→ Bộ TC Studio tại thời điểm review chạy **100% ở `local`** — xem file 04; từ 2026-09-15 đã có run trên `staging`.

⚠️ **Domain callback bắt buộc khi test**: trên **LINE console** của bot thử nghiệm phải đặt webhook URL dạng

```
https://go.lmes.jp/line/callback/add/<id bot>
```

Không đặt đúng domain này thì callback không về được hệ thống → mọi TC của ticket đều không chạy được.

**Điều kiện tiên quyết để test:**

- Branch fix PHP: `ai_small_40888` (repo `sns-line`, nhánh gốc `release_step_20260805`, commit `272e29d0c2`, **7 file**) — đã push lên origin.
- **Phụ thuộc job**: 2 branch phía `linect-service` phải deploy kèm mới đọc được định dạng mới —
  `m_202609_forward_webhook_40475_cb_full_request` (b47e086) và `m_202609_forward_webhook_40475_release-callback` (f6104a3).
  Test PHP mà **job chưa deploy** → TC luồng tiêu thụ (chat, kết bạn, postback, forward) sẽ fail giả.
- Cần **gửi được webhook có chữ ký hợp lệ** tới EP-24 với body gộp **≥ 3 event** (mô phỏng LINE gộp nhiều tin dồn dập), gồm cả các gói lẫn loại: `[delivery, message]`, `[delivery, postback]`, `[message, follow]`.
- Cần **dữ liệu chữ Nhật + emoji** trong `message.text` để kiểm chuỗi lưu không bị escape `\uXXXX`.
- Cần **bản ghi `callback_event` định dạng CŨ (mảng event)** còn tồn để verify đọc song song 2 định dạng — kể cả bản ghi vẫn đang được sinh mới bởi postback giả lập (`UserController::storeFakeCallbackEvent`).

**Rủi ro / lưu ý Dev đã nêu (Leader lưu ý khi duyệt kết quả test):**

- **3 tiến trình PHP cũ** (`HandleCallback` / `HandleCallbackMessage` / `HandleCallbackPostback`) chỉ xử lý **MỘT** event của bản ghi. Nay đã lấy đúng event khớp cột `type`, nhưng nếu 1 bản ghi có **nhiều event CÙNG loại** thì các event sau **vẫn chưa được xử lý** → chỉ ảnh hưởng nếu 3 tiến trình này còn chạy song song với job. **Cần xác nhận đã dừng hẳn.**
- Cột `callback_event.request` kiểu **TEXT (~65.535 byte)** — body quá lớn bị **cắt cụt âm thầm** (kết nối không bật chế độ nghiêm ngặt). Dev đã thêm log cảnh báo; vận hành thấy log này thì phải đổi cột sang `MEDIUMTEXT`.
- Cột chống trùng khi LINE gửi lại (`webhook_event_id`) **vẫn chưa được PHP ghi** → cơ chế chống redelivery của job **chưa kích hoạt** cho bản ghi do PHP tạo. Dev ghi rõ **ngoài phạm vi ticket** (đề nghị ticket riêng) — là ghi nhận, không phải GAP của ticket này.
- Dev **không kết nối được MySQL dev** (`host.docker.internal:3306` connection refused) → **không dump được dữ liệu thật**, cấu trúc cột lấy từ snapshot schema. Mức verify Dev tự làm chỉ là **unit-test**.

## Journal / note từ Redmine (nguyên văn)

**Journal #136271 — AI LME Fix bug — 2026-09-14:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi LINE gọi webhook, phía PHP giải mã JSON rồi mã hoá lại từng sự kiện trước khi ghi vào bảng lưu callback. Vì vậy nội dung lưu không còn là request gốc: mất lớp bao ngoài (mã đích + danh sách sự kiện), ký tự tiếng Nhật/emoji bị đổi sang dạng escape, và mỗi lần LINE gọi bị tách thành nhiều bản ghi trong đó chỉ 2 sự kiện đầu được lưu (sự kiện thứ 3 trở đi bị bỏ khi LINE gộp nhiều tin dồn dập). Tính năng chuyển tiếp webhook sang hệ thống ngoài lại gửi lại đúng chuỗi đã lưu với yêu cầu giữ nguyên trạng, nên bắt buộc phải lưu đúng body gốc; phía job đã được sửa để đọc được cả định dạng đầy đủ mới lẫn định dạng cũ.

■ 2. CÁCH FIX
Refix vòng 1 theo AI review độc lập, 2 lỗi bắt buộc. (1) Đọc nhầm sự kiện: vì mỗi lần LINE gọi nay chỉ tạo 1 bản ghi chứa đủ mọi sự kiện, sự kiện mở đầu có thể là loại báo đã gửi tin (delivery) trong khi cột loại / định danh bạn bè của bản ghi lại ghi theo sự kiện đầu tiên KHÁC delivery — 4 chỗ phía PHP vẫn đọc cứng sự kiện thứ nhất nên lấy nhầm: mất thao tác bấm nút của khách, hoặc xử lý kết bạn / hủy kết bạn cho SAI người. Đã thêm hàm dùng chung đưa đúng sự kiện ứng với cột loại của bản ghi lên đầu (ưu tiên: trùng đúng cột loại → sự kiện đầu tiên khác delivery → không khớp thì giữ nguyên) và gọi ở cả 4 chỗ đọc, nhờ vậy toàn bộ đoạn code phía sau (kể cả hàm phản hồi tin nhắn dùng chung) tự khớp mà không phải sửa rải rác. (2) Rủi ro 1 bản ghi lẫn nhiều loại sự kiện: đã tải THẬT 2 nhánh job nêu trong ticket về kiểm chứng — job KHÔNG định tuyến theo cột loại của bản ghi mà theo loại của TỪNG sự kiện (gom các sự kiện liền kề cùng loại rồi gọi đúng nhánh xử lý), và job lấy bản ghi theo trạng thái chứ không lọc theo cột loại, nên không có chuyện chạy nhầm kịch bản kết bạn hay chặn nhầm bạn bè; đã ghi dẫn chứng file + dòng + mã commit vào phần Bằng chứng & Verify và ghi rõ giả định này vào chú thích hàm lưu callback. Bổ sung 9 unit test cho các gói [delivery, message], [delivery, postback], [message, follow] và các trường hợp biên.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
BotController::callbackWebHook (app/Http/Controllers/Admin/BotController.php)
BotController::storeCallbackEventRaw - hàm mới (app/Http/Controllers/Admin/BotController.php)
parseCallbackEventRequest - hàm mới (app/Helpers/functions.php)
HandleCallback::handle (app/Console/Commands/HandleCallback.php)
HandleCallbackMessage::handle (app/Console/Commands/HandleCallbackMessage.php)
HandleCallbackPostback::handle (app/Console/Commands/HandleCallbackPostback.php)
CallbackPostbackApiController::handleCallbackPostback (app/Http/Controllers/Api/CallbackPostbackApiController.php)
UserController::storeFakeCallbackEvent - đã đọc, giữ nguyên vì là callback nội bộ (app/Http/Controllers/Basic/UserController.php)
HandlePostbackTask.parseCallbackEventData - phía job, đã hỗ trợ 2 định dạng (linect-service, branch của dev)
HandleForwardCallbackEventTask.buildBody - phía job, gửi nguyên chuỗi request ra ngoài (linect-service)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Admin/BotController.php
   - app/Helpers/functions.php
   - app/Console/Commands/HandleCallback.php
   - app/Console/Commands/HandleCallbackMessage.php
   - app/Console/Commands/HandleCallbackPostback.php
   - app/Http/Controllers/Api/CallbackPostbackApiController.php
   - tests/Feature/CallbackEventRequestParseTest.php
 • 4.2 Data ảnh hưởng:
   - callback_event.request — từ nay chứa body đầy đủ LINE gửi (có destination + events) thay vì mảng sự kiện; bản ghi cũ giữ nguyên định dạng cũ, cả job lẫn PHP đều đọc được 2 dạng nên KHÔNG cần chuyển đổi dữ liệu cũ
   - callback_event.line_id / callback_event.type — lấy theo sự kiện đầu tiên khác delivery của request; 1 bản ghi có thể chứa nhiều sự kiện khác loại. Phía đọc: job định tuyến theo type của TỪNG sự kiện, còn 4 chỗ PHP nay đưa đúng sự kiện khớp cột type lên đầu trước khi xử lý
   - callback_event.webhook_event_id — vẫn không được ghi từ phía PHP (giữ nguyên như hiện tại), nên cơ chế chống trùng khi LINE gửi lại của job chưa kích hoạt cho bản ghi do PHP tạo
 • 4.3 Tính năng liên quan:
   - Chat 1:1 (FA-002) — toàn bộ tin nhắn bạn bè gửi đến đi qua bảng callback này; nay không còn mất sự kiện thứ 3 trở đi khi LINE gộp nhiều tin dồn dập
   - Webhook転送 / Forward webhook (outside glossary, #40475) — nội dung chuyển tiếp ra hệ thống ngoài nay đúng nguyên trạng LINE gửi (đủ destination, không escape unicode)
   - Friend Information (FA-001) — sự kiện kết bạn/hủy kết bạn đi cùng đường lưu callback này
   - Auto Reply (FA-003) / Rich Menu (FA-004) — sự kiện postback từ nút, rich menu đọc từ cùng cột request

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: unit-test
   Lệnh: php -l trên 7 file PHP đã sửa: No syntax errors detected; vendor/bin/phpunit --filter CallbackEventRequestParseTest: OK (19 tests, 59 assertions) — thêm 9 test cho việc chọn event đại diện: [delivery, message], [delivery, postback], [message, follow] theo cả 2 giá trị cột type, 1 event đúng loại, không có event trùng type (fallback), events rỗng, JSON hỏng, bản ghi cũ dạng mảng; vendor/bin/phpunit tests/Feature (toàn bộ): 66 tests — vẫn đúng 1 error + 2 failures nền sẵn ở BillingServiceTest (ngày hết hạn) và ExampleTest (cần HTTP/DB), KHÔNG phát sinh lỗi mới; Kiểm chéo phía job: đã git fetch THẬT 2 branch dev nêu trong ticket từ origin linect-service (m_202609_forward_webhook_40475_cb_full_request = b47e086, m_202609_forward_webhook_40475_release-callback = f6104a3) rồi đọc code, không suy đoán
   Bằng chứng: ★ Dẫn chứng cho rủi ro "1 row nhiều event khác loại" (reviewer vòng 1 yêu cầu): job KHÔNG dispatch theo cột type của row mà dispatch theo type của TỪNG event — HandlePostbackTask.handleCallbackEventByType(), file src/main/java/sns/line/task/HandlePostbackTask.java dòng 416-470 trên branch m_202609_forward_webhook_40475_cb_full_request (b47e086) và dòng 416+ trên m_202609_forward_webhook_40475_release-callback (f6104a3): gom các event LIỀN KỀ cùng type rồi switch sang đúng handler (follow/unfollow/postback/message/videoPlayComplete/join/leave/unsend), gọi tại dòng 366. Javadoc ngay trên hàm ghi rõ: "Cột type của row chỉ lưu được 1 type nên không dùng để dispatch được: dispatch theo type của CHÍNH từng event" => gói [unfollow A, message B] hay [follow A, message B] KHÔNG bị xử lý nhầm loại.; Job lấy row theo STATUS chứ không lọc theo cột type: callbackEventRepository.findAllByStatus(CallbackEvent.STATUS_NEW) — HandlePostbackTask.startJobGetEvent dòng 161 (branch b47e086) => không row nào bị bỏ sót dù cột type chỉ mô tả được 1 loại; Job đọc được định dạng mới: HandlePostbackTask.parseCallbackEventData dòng 4803-4820 (b47e086) phân biệt full body và mảng cũ bằng ký tự mở đầu, events rỗng/thiếu trả list rỗng — khớp đúng chuỗi PHP lưu nay; Phía PHP thì ngược lại: 4 chỗ tiêu thụ lấy row THEO cột type (findFirstEvent([follow,unfollow,join,leave]) / findFirstEvent([message]) / postback) và chỉ đọc phần tử số 0, KHÔNG hề lặp mảng event (đã grep toàn bộ 4 file: không có foreach ($body, không có $body[1], không có count($body)) => đã thêm callbackEventsMainFirst() để phần tử số 0 luôn là event khớp cột type; Không kết nối được MySQL dev (host.docker.internal:3306 connection refused) nên không dump được dữ liệu thật; cấu trúc cột lấy từ snapshot schema /workspace/share/db (request kiểu TEXT ~65535 byte); HandleForwardCallbackEventTask.buildBody (job) ghi rõ spec 2026-09-12 là 加工せずそのまま và đang phải gọi unescapeUnicode để bù cho việc PHP mã hoá lại — xác nhận đúng nguyên nhân ticket

■ TỰ REVIEW (AI)
Fix đúng phạm vi ticket: cột request lưu nguyên chuỗi body thô nên tính năng chuyển tiếp webhook gửi ra ngoài đúng nguyên trạng; đồng thời gộp 1 bản ghi cho mỗi lần LINE gọi nên hết cảnh mất sự kiện thứ 3 trở đi (bug đã lặp lại nhiều lần ở các ticket #37235/#37631/#37700/#38033 nhưng chưa từng được đưa lên). Đã giữ nguyên các hành vi cũ: bỏ qua request chỉ có sự kiện loại delivery, đánh dấu bot đã xác thực khi LINE gửi danh sách sự kiện rỗng, xác thực chữ ký trước khi lưu.
 • Rủi ro / lưu ý khi test:
   - ★ (ĐÃ KIỂM CHỨNG, không còn là rủi ro) 1 row chứa nhiều event khác loại: job dispatch theo type của từng event qua handleCallbackEventByType() nên không chạy nhầm kịch bản kết bạn / không chặn nhầm bạn bè — dẫn chứng file+dòng ở phần Bằng chứng & Verify
   - 3 tiến trình PHP cũ (HandleCallback/HandleCallbackMessage/HandleCallbackPostback) chỉ xử lý MỘT event của row: nay đã luôn lấy đúng event khớp cột type (hết cảnh đọc nhầm event delivery), nhưng nếu 1 row có NHIỀU event CÙNG loại thì các event sau vẫn chưa được các tiến trình này xử lý — chỉ ảnh hưởng nếu chúng còn chạy song song với job, cần xác nhận đã dừng hẳn
   - Cột request kiểu TEXT (~65535 byte): body quá lớn sẽ bị cắt cụt âm thầm do kết nối không bật chế độ nghiêm ngặt; đã thêm log cảnh báo để lần ra, nếu vận hành thấy log này thì cần đổi kiểu cột sang MEDIUMTEXT
   - Cột chống trùng khi LINE gửi lại (webhook_event_id) vẫn chưa được PHP ghi — nằm ngoài phạm vi ticket, nên xử lý ở ticket riêng vì 1 row nay chứa nhiều event với nhiều mã khác nhau

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_40888 (nhánh gốc release_step_20260805, commit 272e29d0c2, 7 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 6 phút 29 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=2f4f268e-a479-4ba3-9c95-14ce8795a46b
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=40888
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
