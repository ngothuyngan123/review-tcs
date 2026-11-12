# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio (AI implement)` — quyết định nghiệp vụ bởi `Đỗ Văn Tú (TuDV)` (ngày 04/11/2026: #44707 sửa trong task, #45093 hoãn sang đội job) |
| Commit / Pull Request | `<chưa có PR link>` — commit `sns-line@d6dead11a1e8` (v1, 03/11) → `sns-line@217e39e85e8d` (v2 final, 04/11, sửa bug con #44707) |
| Branch | `ai_studio_implement_44774` (nhánh gốc `release_step_20260930_v2` @`79380b16eeec`) |
| Ngày submit đánh giá | `2026-11-04` (handoff v2 final, Journal #151011) |
| Auto-filled | `2026-11-06 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Callback giả mà web PHP tạo khi bạn bè bấm nút carousel, image map hoặc rich menu có action đang được gửi đi mà **không có chữ ký `X-Line-Signature`**, và event **không có `webhookEventId`**. Vì vậy:
- Bên callback Java (#43212) ghi log sai chữ ký (`#verifyLineSignature MISSING_SIGNATURE`) cho mỗi lần bấm, và **bỏ luôn event** khi bật `ENFORCE` (`LINE_WEBHOOK_SIGNATURE_MODE`).
- Receiver PHP dự phòng (`/line/callback/add/{botId}`, `BotController::callbackWebHook`) trả **401** khi `DOMAIN_ENDPOINT_WEBHOOK` rỗng (rơi về receiver này).

Bug con phát sinh trong lúc implement (v2): khi web **tự ghi thẳng** `callback_event` (không gọi webhook, `ENABLE_CALL_API_WEBHOOK=false`), cột `request` chỉ lưu **mảng event** thay vì đúng khuôn LINE `{"destination","events"}` như nhánh webhook → job chuyển tiếp webhook ra hệ thống ngoài (#40475) gửi **sai định dạng** cho bên thứ 3 → đây là bug `#44707`, đã được sửa trong chính task #44774 (không mở ticket riêng).

> ⚠️ Bug `#45093` (cộng điểm song song bị mất khi bấm nút liên tiếp/đồng thời) **không thuộc nguyên nhân của #44774** — nằm ở job Java `HandlePostbackTask` (đọc-rồi-ghi `value+1` không khoá theo bạn bè), tồn tại từ trước, không do thay đổi của task này. Tu quyết ngày 04/11/2026: để đội job (linect-service) sửa riêng, **không sửa trong #44774**.

## 2. Cách fix

Sửa tập trung ở một hàm private `storeFakeCallbackEvent` (`app/Http/Controllers/Basic/UserController.php`):

- **D-1** Thêm helper sinh `webhookEventId` dạng ULID (26 ký tự) và helper tính chữ ký webhook LINE (`Base64(HMAC-SHA256(body, channel_secret))`) — file `app/Helpers/functions.php`.
- **D-2** `storeFakeCallbackEvent` gán `webhookEventId` cho mỗi event, ký body và gửi header `X-Line-Signature` khi gọi webhook.
- **D-3** Unit test cho 2 helper mới (`tests/Unit/LineFakeCallbackHelperTest.php`, chạy trên PHP 7.4).
- **D-4** (v2, fix `#44707`) `storeFakeCallbackEvent` dựng **1 lần** body `{"destination": "<line_id bạn bè>", "events": [...]}` dùng chung cho **cả 2 nhánh** — nhánh gọi webhook (`ENABLE_CALL_API_WEBHOOK=true`) và nhánh ghi thẳng (`ENABLE_CALL_API_WEBHOOK=false`, trước đó chỉ lưu mảng event).
- **D-5** Kiểm lại nhánh ghi thẳng + luồng chuyển tiếp webhook (#40475) bằng harness độc lập + unit test.
- **D-6** (v3, không đổi code) Trả lời 2 bug automation Studio: `#45093` hoãn sang đội job; `#5022` xác nhận không phải lỗi sản phẩm (format `{destination,events}` là đúng ý đồ fix `#44707`).

Bot **không có `channel_secret`**: giữ behavior cũ — vẫn gửi **không ký**, ghi log lỗi (`missing channel_secret`, không log secret/chữ ký) và gửi 1 tin Chatwork mỗi lần bấm.

`destination` trong body hiện là `line_id` của bạn bè (KHÔNG phải `userId` của bot như webhook LINE thật) — Dev xác nhận đây là đúng thiết kế hiện tại của task này, lệch chuẩn này chưa có ticket riêng để sửa.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `storeFakeCallbackEvent` (private, `UserController.php`) | Có — điểm sửa chính (D-1→D-4) | Nguồn phát sinh callback giả cho cả carousel/image map/rich menu |
| 2 | `executeActionOpenMobileNormal` (`/ajax/open-action-mobile-normal/execute`) — carousel + image map, trang trình duyệt | Không — chỉ là caller | Dev xác nhận action gắn nút phải chạy như cũ |
| 3 | `executeActionOpenMobile` (`/ajax/open-action-mobile/execute`) — 3 nhánh rich menu (action/DELETE_RICH/switch), LIFF | Không — chỉ là caller | Dev xác nhận action gắn nút phải chạy như cũ |
| 4 | `BotController::callbackWebHook` (`/line/callback/add/{botId}`) | Không — nhận request có chữ ký hợp lệ nên tự lưu thay vì 401 | Nhánh webhook, không đổi code receiver |
| 5 | Callback Java `verifyLineSignature` (#43212, `LINE_WEBHOOK_SIGNATURE_MODE`) | Không — code Java không đổi | Event giả giờ pass verify chữ ký ở cả `LOG_ONLY` và `ENFORCE` |
| 6 | `parseCallbackEventRequest` (7 chỗ PHP: `HandleCallback`, `HandleCallbackPostback`, `HandleCallbackMessage`, `CallbackPostbackApiController`,...) | Không — đã hỗ trợ đọc cả 2 dạng (mảng cũ + object mới) từ trước (#40475) | Row cũ dạng mảng tạo trước deploy vẫn phải xử lý được |
| 7 | Job Java `HandlePostbackTask` | Không — đọc row status 50 dạng mới: string bắt đầu bằng `{` thì lấy `events` | Dedup theo `webhook_event_id`; row phải về status 2 sau xử lý |
| 8 | Job chuyển tiếp webhook ra hệ thống ngoài (#40475) | Không — code job không đổi, chỉ nhận input khác | Body gửi bên thứ 3 cho event giả đổi từ mảng → object `{destination, events}` |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `storeFakeCallbackEvent` | `app/Http/Controllers/Basic/UserController.php` | Direct | Sinh `webhookEventId`, ký `X-Line-Signature`, dựng body `{destination,events}` |
| F2 | Helper sinh ULID + tính chữ ký HMAC-SHA256 | `app/Helpers/functions.php` | Direct | 2 hàm mới, không đổi hàm cũ |
| F3 | `executeActionOpenMobileNormal` (`/ajax/open-action-mobile-normal/execute`) | `UserController.php` | Indirect | Caller — carousel + image map, trang trình duyệt |
| F4 | `executeActionOpenMobile` (`/ajax/open-action-mobile/execute`) | `UserController.php` | Indirect | Caller — 3 nhánh rich menu (LIFF) |
| F5 | `BotController::callbackWebHook` (`/line/callback/add/{botId}`) | — | Indirect | Nhận request đã ký hợp lệ → lưu thay vì trả 401 |
| F6 | Callback Java `verifyLineSignature` (#43212) | sns-line-java | Indirect | Event giả pass verify ở cả `LOG_ONLY` và `ENFORCE` |
| F7 | `parseCallbackEventRequest` (7 chỗ: `HandleCallback`, `HandleCallbackPostback`, `HandleCallbackMessage`, `CallbackPostbackApiController`,...) | nhiều file | Indirect | Phải đọc đúng cả dạng mảng cũ lẫn object mới |
| F8 | Job Java `HandlePostbackTask` | sns-line-java | Indirect | Đọc row status 50 dạng mới, dedup theo `webhook_event_id` |
| F9 | Job chuyển tiếp webhook ra hệ thống ngoài (#40475) | — | Indirect | Gửi body `{destination, events}` cho bên thứ 3 (thay vì mảng) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `callback_event.webhook_event_id` (DB callback, connection `mysql_callback`) | UPDATE (ghi giá trị khi insert/webhook) | Cột đã tồn tại từ trước (#38380/#40888), **không phải migration mới** — Dev lưu ý **phải xác nhận cột tồn tại trên môi trường test trước khi test**, thiếu cột thì nhánh ghi thẳng lỗi |
| D2 | `callback_event.request` (cùng bảng) | UPDATE | Đổi format: mảng event → object `{"destination","events"}` ở nhánh ghi thẳng (status 50, `ENABLE_CALL_API_WEBHOOK=false`) — fix `#44707` |
| D3 | Không có migration / schema change mới | — | Dev đã kiểm diff xác nhận |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Nút carousel (trang trình duyệt) — action gắn nút (gửi tin/gắn tag/cộng điểm/kịch bản) | F1, F2, F3, D2 | Medium (Dev tự đánh giá "rủi ro thấp" nhưng chưa verify runtime với receiver thật) |
| T2 | Nút image map (trang trình duyệt) | F1, F2, F3, D2 | Medium |
| T3 | Rich menu có action (LIFF, 3 nhánh: action / DELETE_RICH / switch) | F1, F2, F4, D2 | Medium |
| T4 | Callback Java verify signature (#43212, cả `LOG_ONLY` và `ENFORCE`) | F6 | Medium — behavior đổi: event giả trước bị bỏ ở `ENFORCE`, giờ pass |
| T5 | Receiver PHP dự phòng khi `DOMAIN_ENDPOINT_WEBHOOK` rỗng | F5 | Medium — trước trả 401 không tạo row, giờ trả 200 + tạo row |
| T6 | Job xử lý postback (`HandlePostbackTask`) — action chạy, row về status 2 | F7, F8, D2 | High — nếu đọc sai format mới thì action không chạy hoặc lỗi; phải test cả row cũ (mảng) lẫn row mới (object) tồn song song sau deploy |
| T7 | Job chuyển tiếp webhook ra hệ thống ngoài (#40475) | F9, D2 | High — bên thứ 3 (tích hợp khách hàng) nhận sai format nếu fix lỗi |
| T8 | Bot thiếu `channel_secret` — fallback gửi không ký | F1 | Low — giữ behavior cũ, chỉ cần test không lộ secret/chữ ký trong log |
| T9 | Cộng điểm (point) khi bấm nút liên tiếp/đồng thời | — (ngoài phạm vi, bug `#45093`) | **Không test trong task #44774** — bug tồn tại từ trước, để đội job sửa riêng; TC không nên dùng kịch bản "bấm song song" để đánh giá fix của task này |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
