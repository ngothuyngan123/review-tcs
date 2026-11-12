# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44774 — Callback fake tạo từ phía web PHP tạo chưa có signature và webhook_event_id` |
| Module / Màn hình | `Callback giả (fake callback) khi bạn bè bấm nút carousel / image map (trang trình duyệt) / rich menu có action (LIFF) — hàm storeFakeCallbackEvent, app/Http/Controllers/Basic/UserController.php` |

## Mô tả bug (bản dịch tiếng Việt)

Callback từ phía web PHP tạo chưa có signature và webhook_event_id
=> Đề xuất bên PHP tự tạo signature (có thể tạo giống bên line) và webhook_event_id

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" riêng — xem Journal #150048 bên dưới để biết root cause cụ thể hơn description gốc. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #44774 không có attachment (Attachments (0)). -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được qua Steps to reproduce trong Redmine — root cause + cách fix đã được Dev confirm qua các Journal (chép nguyên văn ở dưới) và qua `03-dev-impact.md`. TCs nên tập trung verify cách fix + regression impact.

Ticket tracker = `SpecImprove`, status = `Đang fix`. Dev đã handoff 2 lần (v1 ngày 03/11, v2 ngày 04/11 sửa bug con #44707), kèm 1 bản v3 (04/11) không đổi code — chỉ trả lời 2 bug automation (#45093, #5022).

⚠️ Bug con phát sinh trong quá trình implement:
- `#44707` — ĐÃ sửa trong chính task này (commit `217e39e85e8d`): khi web tự ghi callback_event thẳng (không gọi webhook), cột `request` phải lưu đúng khuôn `{"destination","events"}` giống nhánh webhook (trước đó chỉ lưu mảng event, khiến job chuyển tiếp #40475 gửi sai định dạng cho bên thứ 3).
- `#45093` — KHÔNG sửa trong task này (Tu quyết ngày 04/11/2026). Lỗi mất điểm khi cộng điểm song song (race condition ở job Java `HandlePostbackTask`, đọc-rồi-ghi không khoá theo bạn bè) — để đội job (linect-service) sửa riêng. **Không dùng kịch bản cộng điểm song song để đánh giá lượt sửa #44774 này.**
- `#5022` — Dev kết luận KHÔNG phải lỗi sản phẩm: cột `request` lưu dạng `{destination, events}` là đúng ý đồ của bản sửa `#44707`. TC Studio `NEW-3`/`NEW-4`/`NEW-11` cần cập nhật mong đợi theo dạng mới này; `NEW-14` cần tách ý kiểm khỏi phần tổng điểm.

⚠️ `destination` trong body request hiện là `line_id` của bạn bè, KHÔNG phải `userId` của bot như webhook LINE thật — Dev xác nhận đây là đúng thiết kế hiện tại (lệch chuẩn đã biết, chưa có ticket riêng để sửa).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `46963` (bot dùng để test kênh chuyển tiếp — nêu trong Journal #151011) · bot bất kỳ thiếu `channel_secret` (test nhánh không ký) |
| Friend | `<chưa rõ — tester tự dựng bạn bè test>` |
| Đối tượng cấu hình | Nút carousel / image map (trang trình duyệt, `executeActionOpenMobileNormal`), rich menu có action (LIFF, `executeActionOpenMobile`, 3 nhánh) |
| Thời điểm lỗi | `<không áp dụng — ticket SpecImprove, không phải lỗi production cụ thể>` |
| Đối chứng | `<chưa rõ>` |

## Journal / note từ Redmine (nguyên văn)

**Journal #150048 — Dev Studio — 2026-11-02:**

```
Dev Studio · Nội dung thực hiện

Callback giả mà web PHP tạo khi bạn bè bấm nút carousel, image map hoặc rich menu có action đang được gửi đi mà không có chữ ký X-Line-Signature, và event không có webhookEventId. Vì vậy bên Java (#43212) ghi log sai chữ ký cho mỗi lần bấm, bỏ luôn event khi bật ENFORCE, còn receiver PHP dự phòng thì trả 401. Thiết kế sửa ở một chỗ là hàm storeFakeCallbackEvent: tự sinh webhookEventId dạng ULID cho từng event, rồi ký body bằng channel secret của bot giống cách LINE ký. Không có câu hỏi chặn, có thể thực thi ngay.

Hướng sửa:
- D-1 Thêm helper sinh webhookEventId (ULID) và tính chữ ký webhook LINE
- D-2 storeFakeCallbackEvent gán webhookEventId, ký và gửi X-Line-Signature
- D-3 Unit test cho hai helper mới

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng luồng bạn bè bấm nút carousel, image map (trang trình duyệt) và rich menu có action (LIFF), qua hàm storeFakeCallbackEvent. Receiver PHP và callback Java không đổi. Cần test cả hai nhánh: gọi webhook và insert thẳng. Rủi ro chính là body gửi đi phải đúng là chuỗi đã ký.
```

**Journal #150465 — Dev Studio — 2026-11-03:**

```
Dev handoff — 03/11 15:42 · nhánh ai_studio_implement_44774

Tóm tắt:
Khi bạn bè bấm nút carousel, image map (trang mở trình duyệt) hoặc rich menu (LIFF) có gắn action, callback giả do web gửi tới webhook giờ có header X-Line-Signature hợp lệ, và mỗi event có webhookEventId (ULID 26 ký tự). Ở chế độ insert thẳng, row cũng có cột webhook_event_id. Điều cần chú ý nhất khi test: với Java callback ở ENFORCE và với receiver PHP, hành động của nút phải chạy lại (trước đây event bị bỏ); webhook_event_id của row phải trùng webhookEventId trong request.

Nội dung thay đổi:
- Bấm nút carousel / image map (trang trình duyệt) và rich menu (LIFF) có action, khi ENABLE_CALL_API_WEBHOOK=true: request webhook giả được ký X-Line-Signature bằng channel secret của bot, body có thêm webhookEventId.
- Cùng thao tác khi ENABLE_CALL_API_WEBHOOK=false: row callback_event status 50 có cột webhook_event_id, cột request có thêm webhookEventId.
- Bot không có channel secret: vẫn gửi không ký như cũ, ghi log lỗi và gửi 1 tin Chatwork mỗi lần bấm.

File đã sửa (php-web):
  app/Helpers/functions.php                     |  55 ++++++++++++++
  app/Http/Controllers/Basic/UserController.php |  55 ++++++++++++--
  tests/Unit/LineFakeCallbackHelperTest.php     | 103 ++++++++++++++++++++++++++
  3 files changed, 208 insertions(+), 5 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ sửa một hàm private dùng cho một tính năng (5 caller). Byte gửi đi được encode giống hệt Guzzle trước đây, và chữ ký đã được kiểm độc lập bằng openssl và LINE SDK. Chưa verify runtime với receiver thật.
- 5 điểm gọi callback giả: button carousel và image map ở trang trình duyệt (executeActionOpenMobileNormal); 3 nhánh rich menu ở trang LIFF (executeActionOpenMobile). Hành động gắn nút phải chạy như cũ.
- Callback Java (#43212, LINE_WEBHOOK_SIGNATURE_MODE): event giả giờ qua được bước verify chữ ký ở cả LOG_ONLY lẫn ENFORCE.
- Receiver PHP /line/callback/add/{botId} (BotController::callbackWebHook): event giả được lưu thay vì trả 401.
- Job HandlePostbackTask dedup theo webhook_event_id: row giả giờ có id riêng mỗi lần bấm, không được đánh nhầm là webhook trùng.
- Chuyển tiếp webhook ra hệ thống ngoài (#40475): body của row giả có thêm khoá webhookEventId.
- app/Helpers/functions.php (nạp toàn app): chỉ thêm 2 hàm mới tên riêng, không đổi hàm cũ.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy:
- Trước khi deploy, xác nhận bảng callback_event trên DB callback (connection mysql_callback) đã có cột webhook_event_id (cột từ #38380/#40888). Thiếu cột thì nhánh insert thẳng sẽ lỗi khi bấm nút.
- Không có cache hay asset cần xử lý, không có thứ tự deploy với module khác (Java không đổi).

Việc cần người làm thêm (ngoài phạm vi task):
- Mục 1 và mục 3 trong ghi chú 28/10/2026 của #43212 (chặn forward callback về chính webhook LME; liệt kê các bot có callback INVALID) cần ticket riêng, không thuộc #44774.
- Sau khi deploy bản này, các log #verifyLineSignature MISSING_SIGNATURE do callback giả của PHP gây ra sẽ hết. Người theo dõi #43212 nên lọc lại danh sách callback INVALID trước khi bật ENFORCE.
- Tester bật ENABLE_CALL_API_WEBHOOK trên môi trường test, bấm nút carousel, image map và rich menu có action: kiểm log Java không còn #verifyLineSignature MISSING_SIGNATURE, receiver PHP trả 200 và row callback_event có webhook_event_id (A1-A3).
- Kiểm trên môi trường test một bot thiếu channel_secret: vẫn gửi được và có đúng 1 tin Chatwork, log không chứa secret/chữ ký (A5).

Điểm cần test:
- Bấm nút carousel và image map (trang trình duyệt), rồi rich menu có action (LIFF), với ENABLE_CALL_API_WEBHOOK=true: request tới /line/callback/add/{botId} có X-Line-Signature hợp lệ. Java ở LOG_ONLY không còn log #verifyLineSignature; ở ENFORCE event được lưu và action chạy.
- DOMAIN_ENDPOINT_WEBHOOK rỗng (rơi về receiver PHP): trả 200 và tạo row callback_event (trước khi sửa trả 401).
- Row callback_event có webhook_event_id 26 ký tự, trùng với webhookEventId trong request; bấm hai lần ra hai id khác nhau, job không đánh dấu trùng.
- ENABLE_CALL_API_WEBHOOK=false: row status 50 có webhook_event_id, postback vẫn xử lý như cũ.
- Bot thiếu channel_secret: vẫn gửi, có log và một tin Chatwork; log không chứa secret hay chữ ký.
- Tin postback có data dài hoặc ký tự đặc biệt: chữ ký vẫn khớp, vì body gửi đi đúng là chuỗi đã ký.
- Unit test D-3 pass trên PHP 7.4.
- ENABLE_CALL_API_WEBHOOK=true, Java callback ở LOG_ONLY: bấm nút carousel (trang trình duyệt) có action ⇒ action chạy, log Java không còn #verifyLineSignature cho request này.
- Java callback ở ENFORCE: bấm carousel, image map, rich menu (LIFF) ⇒ row callback_event được tạo và action chạy (trước sửa: event bị bỏ).
- DOMAIN_ENDPOINT_WEBHOOK rỗng (receiver PHP): bấm nút ⇒ HTTP 200 và có row callback_event (trước sửa: 401, không có row).
- Row sinh ra có webhook_event_id dài 26 ký tự, trùng webhookEventId trong cột request; bấm 2 lần ⇒ 2 id khác nhau, không row nào bị đánh trạng thái webhook trùng.
- ENABLE_CALL_API_WEBHOOK=false: bấm nút ⇒ row status 50 có webhook_event_id, action xử lý như cũ.
- Bot test không có channel secret: bấm nút ⇒ vẫn gửi, có log lỗi missing channel_secret và 1 tin Chatwork; log không chứa secret hay chữ ký.

Branch: ai_studio_implement_44774
- sns-line: ai_studio_implement_44774 (nhánh gốc release_step_20260930_v2 @79380b16eeec, commit d6dead11a1e8e1656c65604ae8cefe487c479795)
```

**Journal #150498 — Dev Studio — 2026-11-03:**

```
Automation Test Studio: pass ở lượt #6422. Lần bàn giao 03/11 15:42 @d6dead11a1e8 chuyển sang chờ test.
```

**Journal #151007 — Dev Studio — 2026-11-04:**

```
Dev Studio · Nội dung thực hiện

Theo trả lời của Tu, bug #45093 (cộng điểm song song bị mất) không sửa trong task này, đội job sẽ sửa sau, nên không thêm module job. Bản thiết kế v2 giờ chỉ còn sửa bug #44707: khi web tự ghi callback, cột request phải lưu body đầy đủ {"destination","events"}, giống nhánh gọi webhook (D-4). Sau đó chạy harness và test để kiểm lại (D-5). Không còn câu hỏi chặn nên bản thiết kế sẵn sàng thực thi.

Hướng sửa:
- D-4 storeFakeCallbackEvent dựng body {destination, events} một lần, dùng cho cả nhánh webhook và nhánh ghi thẳng
- D-5 Kiểm lại nhánh ghi thẳng và luồng chuyển tiếp bằng harness và unit test

Ảnh hưởng / rủi ro:
Chỉ đổi nhánh web tự ghi callback_event (ENABLE_CALL_API_WEBHOOK tắt) cho các nút carousel, image map và rich menu: request đổi từ mảng event sang body đầy đủ. Job xử lý postback và job chuyển tiếp đã đọc được cả hai dạng; cần test lại việc chuyển tiếp sang bên thứ 3 và việc xử lý các row dạng cũ còn tồn.
```

**Journal #151011 — Dev Studio — 2026-11-04:**

```
Dev handoff — 04/11 09:33 · nhánh ai_studio_implement_44774

Tóm tắt:
Khi bạn bè bấm nút carousel, image map (trang mở trình duyệt) hoặc rich menu (LIFF) có action, callback giả do web tạo gửi webhook có X-Line-Signature hợp lệ và webhookEventId (v1). Bản v2 sửa bug #44707: khi web tự ghi callback_event (ENABLE_CALL_API_WEBHOOK=false), cột request lưu đúng khuôn LINE {"destination","events"} nên job chuyển tiếp gửi sang bên thứ 3 đúng định dạng. Cần chú ý nhất khi test: bot bật kênh chuyển tiếp, bên thứ 3 nhận body có destination và events, và action của nút vẫn chạy (row về status 2). destination là line_id của bạn bè, không phải userId của bot; đây là đúng thiết kế.

Nội dung thay đổi:
- Bấm nút carousel / image map / rich menu có action khi ENABLE_CALL_API_WEBHOOK=true: request webhook giả có X-Line-Signature ký bằng channel secret của bot, mỗi event có webhookEventId.
- Cùng thao tác khi ENABLE_CALL_API_WEBHOOK=false: row callback_event status 50 có webhook_event_id, cột request có dạng {"destination":"<line_id bạn bè>","events":[...]} thay vì chỉ là mảng event, nên bên thứ 3 của kênh chuyển tiếp nhận đúng định dạng (#44707).
- Bot không có channel secret: vẫn gửi không ký như cũ, ghi log lỗi và gửi 1 tin Chatwork mỗi lần bấm.

Bug QA con:
- #44707 đã sửa (commit sns-line@217e39e85e8d): Khi web tự ghi callback_event (không gọi webhook), cột request giờ lưu dạng {"destination","events"} giống nhánh webhook, nên job chuyển tiếp gửi sang bên thứ 3 đúng định dạng LINE. destination là line_id của bạn bè, không phải userId của bot.
- #45093 không đổi code: Lỗi mất điểm khi cộng điểm song song nằm ở job Java HandlePostbackTask (đọc rồi ghi cũ+1 mà không khoá theo bạn bè), không do thay đổi ở web. Tu quyết ngày 04/11/2026 để đội job sửa ở việc riêng. Người phụ trách cần chuyển bug này sang ticket hoặc đội job.

File đã sửa (php-web):
  app/Helpers/functions.php                     |  55 ++++++++++++++
  app/Http/Controllers/Basic/UserController.php |  63 ++++++++++++++--
  tests/Unit/LineFakeCallbackHelperTest.php     | 103 ++++++++++++++++++++++++++
  3 files changed, 215 insertions(+), 6 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ sửa một hàm private, 5 nơi gọi cùng một tính năng; mọi nơi đọc request đã hỗ trợ dạng đầy đủ từ #40475; harness độc lập đã kiểm cả 2 nhánh. Chưa kiểm tra trên môi trường thật với job và chuyển tiếp thật.
- 5 nơi gọi storeFakeCallbackEvent (carousel và image map ở trang trình duyệt, 3 nhánh rich menu LIFF): action gắn nút (gửi tin, gắn tag, cộng điểm, kịch bản) phải chạy như cũ.
- Job Java HandlePostbackTask đọc row status 50 ở dạng mới: chuỗi bắt đầu bằng { thì lấy events; row phải về status 2.
- Job chuyển tiếp webhook (#40475): body gửi bên thứ 3 cho event giả đổi từ mảng sang object {destination, events}.
- Các job/API PHP đọc callback_event.request qua parseCallbackEventRequest (HandleCallback, HandleCallbackPostback, HandleCallbackMessage, CallbackPostbackApiController) đều nhận được cả 2 dạng.
- Row cũ dạng mảng còn chờ xử lý lúc deploy vẫn được xử lý bình thường.
- Callback Java (#43212) và receiver PHP: event giả có chữ ký hợp lệ nên không bị bỏ ở chế độ ENFORCE và không còn bị trả 401.
- Job chống trùng theo webhook_event_id: mỗi lần bấm có một id riêng nên không bị đánh trùng nhầm.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Lưu ý khi deploy:
- Xác nhận cột webhook_event_id đã có trên bảng callback_event của DB callback (connection mysql_callback, cột có từ #38380/#40888); nếu thiếu cột thì nhánh web ghi thẳng sẽ lỗi khi insert.
- Không có cache hay asset; không cần thứ tự deploy với module khác vì job Java không đổi.

Việc cần người làm thêm (ngoài phạm vi task):
- Đội job (linect-service) sửa #45093: HandlePostbackTask cộng điểm bằng cách đọc rồi ghi lại, không khoá theo bạn bè. Gợi ý dùng UPDATE nguyên tử (value = value + 1) hoặc khoá theo bạn bè; chi tiết ở evidence/code/45093-job-lost-update.md. Theo quyết định của Tu ngày 04/11/2026, bug này để sửa sau, không làm trong #44774.
- Trên môi trường test, kiểm cột webhook_event_id đã có trên bảng callback_event của DB callback, vì repo không có migration cho cột này.
- destination trong request đang là line_id của bạn bè, chưa phải userId của bot như LINE thật; muốn đúng phải lưu thêm userId bot hoặc gọi API bot/info, nên tách thành một cải tiến riêng nếu bên thứ 3 cần.
- Nếu khách hoặc bên thứ 3 cần destination đúng userId của bot như webhook LINE thật: mở việc riêng để lưu userId bot (gọi LINE bot/info hoặc thêm cột).

Điểm cần test:
- Nhánh ghi thẳng: bấm image map, carousel và rich menu ⇒ row status 50 có webhook_event_id, request dạng {"destination":"<line_id bạn bè>","events":[{…,"webhookEventId":…}]}; job xử lý action như cũ và row về status 2.
- Bot bật kênh chuyển tiếp: bên thứ 3 nhận body có destination và events ở cả nhánh webhook lẫn nhánh ghi thẳng.
- Row cũ dạng mảng còn chờ xử lý vẫn được job xử lý bình thường.
- Nhánh webhook: chữ ký X-Line-Signature vẫn hợp lệ, receiver lưu request đúng body đã ký.
- Không dùng kịch bản cộng điểm song song (#45093) để đánh giá lượt sửa này.
- Bot 46963 bật kênh chuyển tiếp, ENABLE_CALL_API_WEBHOOK=false: bấm image map có action ⇒ row callback_event status 50 có request bắt đầu {"destination":"<line_id bạn bè>","events":[ và webhook_event_id trùng webhookEventId; action chạy, row về status 2; bên thứ 3 nhận body có destination và events.
- Như trên với nút carousel (trang trình duyệt) và rich menu (LIFF).
- ENABLE_CALL_API_WEBHOOK=true (callback Java hoặc receiver PHP): bấm các nút ⇒ request cùng khuôn {destination, events}, chữ ký hợp lệ (Java ENFORCE không bỏ event, receiver PHP không trả 401), bên thứ 3 nhận đúng định dạng.
- Row cũ dạng mảng tạo trước deploy và đang chờ xử lý vẫn được job xử lý và chuyển tiếp bình thường.
- Bấm 2 lần ⇒ 2 row có 2 webhook_event_id khác nhau, không row nào bị đánh là webhook trùng.
- Bot test không có channel secret (ENABLE_CALL_API_WEBHOOK=true): vẫn gửi, có log lỗi missing channel_secret, 1 tin Chatwork; log không chứa secret hay chữ ký.

Branch: ai_studio_implement_44774
- sns-line: ai_studio_implement_44774 (nhánh gốc release_step_20260930_v2 @79380b16eeec, commit 217e39e85e8deb17ed1d3a7be66545ffdba342f9)
```

**Journal #151085 — Dev Studio — 2026-11-04:**

```
Dev Studio · Nội dung thực hiện

Bản v3 không đổi code, chỉ trả lời 2 bug automation. Bug #45093 (cộng điểm song song bị mất) nằm ở job Java và có sẵn từ trước; theo quyết định của Tu ngày 04/11 thì hoãn, để đội job sửa sau. Bug #5022 không phải lỗi sản phẩm: cột request lưu dạng {destination, events} là đúng ý đồ của bản sửa #44707. Các testcase NEW-3/4/11 cần cập nhật theo dạng này. Còn lại: người cần chuyển ticket #45093 sang đội job.

Hướng sửa:
- D-6 Ghi trả lời 2 bug automation, không đổi code

Ảnh hưởng / rủi ro:
Không đổi code nên không có rủi ro mới. Lỗi #45093 vẫn tái hiện được cho tới khi đội job sửa. Tester cần cập nhật mong đợi của NEW-3/4/11 và tách ý kiểm của NEW-14 khỏi phần tổng điểm.
```
