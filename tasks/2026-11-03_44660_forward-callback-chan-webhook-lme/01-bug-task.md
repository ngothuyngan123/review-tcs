# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #44660 qua `/new-task` (REST API, `scripts/redmine_fetch.py`).
> ⚠️ Issue Redmine **không có mục "Description"** (trống) — tracker `SpecImprove`, không phải report khách hàng cụ thể. Toàn bộ nội dung điều tra nằm trong 4 journal "Dev Studio" (quy trình bàn giao AI dev, 2026-10-28 → 2026-11-02), chép nguyên văn ở cuối file này.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44660 — Tính năng forward callback chặn việc set chính webhook của LME vào url forward callback bên mình` |
| Module / Màn hình | Webhook転送 (Webhook Relay) — cả 2 tab: 「LINE公式アカウントデータ転送」 (SCR-01) và 「L Messageデータ転送」 (SCR-02); API lưu cấu hình: `POST /admin/webhook-relay/save` (EP-02) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- issue.description rỗng. Nội dung dưới đây lấy nguyên văn (đã là tiếng Việt) từ journal #149214/#149730 — Dev Studio tự mô tả nguyên nhân khi phân tích ticket, không phải mô tả của khách hàng/author. -->

Ô 「転送先URL」 của cả hai kênh (tab LINE và tab LME) chỉ được kiểm ở server bởi `WebhookUrlValidator::validate()`, gồm 4 luật: bắt buộc khi bật, `https://`, ≤1024 ký tự, chống SSRF (host ra IP public, cổng 443). **Không luật nào nhận diện URL webhook của chính LME** (dạng `{DOMAIN_ENDPOINT_WEBHOOK}line/callback/add/{bot_id}`). Vì host của LME là IP public, cổng 443 nên URL này vẫn pass được 4 luật cũ và **lưu được bình thường** → tạo vòng lặp webhook (LME gửi event tới chính mình). Spec `webhook-relay` §6.5 cũng thiếu luật này.

Trong lúc fix phát sinh thêm 1 bug con (#44843, cùng ticket gốc): ở bản sửa đầu tiên (commit `3ddf9d4c`), hàm `isLmeWebhookUrl()` **chưa rút gọn đoạn `.` / `..`** trong path trước khi so khớp, nên URL dạng `/line/./callback/add/1` (hoặc dùng `%2e`, `\`, `%5C`) **không bị chặn** — tức là có cách lách qua luật mới. Đã vá ở bản 2 (`4d8510dcf8`) và giữ ở bản 3 / HEAD hiện tại (`676e01b687cc`).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" riêng — suy ra từ root cause ở trên (hành vi lưu được khi lẽ ra phải bị chặn). -->

1. Mở màn Webhook転送 (tab 「LINE公式アカウントデータ転送」 hoặc tab 「L Messageデータ転送」) của 1 bot.
2. Bật switch 「転送する」, nhập vào ô 「転送先URL」 một URL chính là webhook của LME, dạng `https://<domain webhook LME>/line/callback/add/<bot_id>` (có thể dùng bot_id của bot khác, hoặc biến thể encode như `//`, `%2F`, `/./`, `/../`, `%2e`, `\`, `%5C`, kèm query string).
3. Bấm 「保存する」.

## Expected result

- Hệ thống phải từ chối lưu (vì URL này sẽ khiến LME forward event ngược về chính webhook của mình → vòng lặp), trả lỗi rõ ràng dưới ô URL.

## Actual result

- (Trước fix) Hệ thống **chấp nhận và lưu** URL webhook LME bình thường — vì validator không có luật nhận diện riêng cho URL dạng này, và URL vẫn thoả 4 luật validate cũ (https, ≤1024 ký tự, không phải localhost/IP nội bộ, cổng 443).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có file đính kèm trên Redmine. -->

## Ghi chú thêm của Leader

- ⚠️ Ticket tracker = `SpecImprove` (không phải `Bug`), status Redmine hiện tại = "Fix done - Đợi test" (digest) / "Đang fix" (snapshot context Studio lúc tạo task — có thể lệch do Redmine update sau). Không có khách hàng / PM báo bug cụ thể — phát hiện từ review nội bộ / spec gap.
- ⚠️ Đã có **3 bản bàn giao** (`3ddf9d4c` → `4d8510dcf8` → `676e01b687cc` = HEAD). Bản 1 có lỗ hổng path traversal (`.`/`..` chưa rút gọn) → phát sinh bug con **#44843**, đã vá ở bản 2 và giữ ở bản 3. **Tester PHẢI test trên HEAD `676e01b687cc`, KHÔNG test lại trên `3ddf9d4c`.**
- Branch: `ai_studio_fixbug_44660` (gốc `release_step_20260930_v2` @`303a131b9c03`).
- Automation Test Studio (task #526) đã chạy **18/18 TC pass** ở env `staging` (lượt #6353, journal #150071) — xem chi tiết + cảnh báo RULE-08 (chưa chạy `prd`) ở `04-tc-list.md`.
- Follow-up ngoài phạm vi task (Dev note, cần người làm thêm — Leader cân nhắc raise ticket riêng):
  - Kiểm production: `SELECT bot_id, is_enabled, notify_is_enabled FROM webhook_relay_setting WHERE endpoint_url LIKE '%/line/callback/add/%' OR notify_endpoint_url LIKE '%/line/callback/add/%'` — nếu có dòng thì cấu hình cũ trỏ webhook LME vẫn tồn tại và job vẫn forward tới đó, phải báo khách đổi/xoá URL.
  - Job Java (`HandleForwardCallbackEventTask` / `HandleForwardLmeEventTask`, module job) **không đổi** trong fix này — Dev đề xuất ticket riêng để chặn thêm ở job, phòng cấu hình cũ hoặc URL lách qua được validator web.
  - Cập nhật `spec-features/admin/webhook-relay/` §6.5: bổ sung luật chặn URL webhook LME (spec gốc thiếu luật này).
  - Release `release_step_20260930` / `release_staging_20261014` (và `_v2`) đã có Webhook転送 nhưng **chưa có #43730** sẽ nhận request forward như webhook thật — Dev đề xuất đưa #43730 lên cùng/trước bản sửa này.

## Journal / note từ Redmine (nguyên văn)

**Journal #149214 — Dev Studio — 2026-10-28:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Ô 「転送先URL」 của cả hai kênh chỉ được kiểm ở server bởi `WebhookUrlValidator::validate()`, gồm 4 luật: bắt buộc khi bật, `https://`, ≤1024 ký tự, chống SSRF (host ra IP public, cổng 443). Không luật nào nhận diện URL webhook của LME (`{DOMAIN_ENDPOINT_WEBHOOK}line/callback/add/{bot_id}`). Host của LME là IP public, cổng 443 nên URL này lưu được. Spec webhook-relay §6.5 cũng thiếu luật này.

Hướng sửa:
- D-1 Thêm luật chặn URL webhook LME vào WebhookUrlValidator
- D-2 Unit test cho luật mới

Ảnh hưởng / rủi ro:
Chỉ đổi validate của POST /admin/webhook-relay/save, áp cho cả tab LINE và tab LME. Cấu hình cũ trỏ về webhook LME sẽ không lưu lại được cho tới khi khách đổi URL; các luật validate khác giữ nguyên.
```

**Journal #149730 — Dev Studio — 2026-10-30:**

```
Dev handoff — 30/10 09:19 · nhánh ai_studio_fixbug_44660

Nguyên nhân:
Ô 「転送先URL」 của cả hai kênh chỉ được kiểm ở server bởi `WebhookUrlValidator::validate()`, gồm 4 luật: bắt buộc khi bật, `https://`, ≤1024 ký tự, chống SSRF (host ra IP public, cổng 443). Không luật nào nhận diện URL webhook của LME (`{DOMAIN_ENDPOINT_WEBHOOK}line/callback/add/{bot_id}`). Host của LME là IP public, cổng 443 nên URL này lưu được. Spec webhook-relay §6.5 cũng thiếu luật này.

Nội dung thay đổi:
- Màn 「Webhook転送」 (cả 2 tab), nút 「保存する」: URL có path /line/callback/add (mọi domain, mọi bot_id, chữ hoa/thường, //, %2F, có query) bị từ chối với HTTP 422 và lỗi 「このURLは転送先に指定できません。」 dưới ô URL, không lưu.

File đã sửa (php-web):
  app/Services/WebhookRelay/WebhookUrlValidator.php | 28 ++++++++++-
  tests/Unit/WebhookUrlValidatorLmeWebhookTest.php  | 58 +++++++++++++++++++++++
  2 files changed, 85 insertions(+), 1 deletion(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ thêm một luật validate thuần (không cần DNS) vào validator của một màn; không đổi DB, FE hay job, có unit test bao phủ.
- Validator ô 転送先URL dùng chung cho 2 kênh qua API lưu cấu hình Webhook転送: cần kiểm lại các lỗi cũ (rỗng khi bật, http://, >1024 ký tự, khoảng trắng, ký tự lạ, localhost/IP nội bộ, cổng khác 443, host không phân giải).
- Cấu hình đã lưu URL LME trước bản sửa: vẫn còn và job vẫn chuyển tiếp; lần 「保存する」 kế tiếp của tab đó bị chặn (kể cả chỉ tắt switch) cho tới khi xoá/đổi URL.
- Job java chuyển tiếp webhook không đổi; MCP và app mobile không ghi cấu hình này.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Lỗi nằm ở bước kiểm tra khi lưu cấu hình, không ghi sai dữ liệu nghiệp vụ nào. Cấu hình đã lưu trỏ về webhook LME (nếu có) là thiết lập của khách, chỉ khiến lần chuyển tiếp bị 401 và hiện trong card 「転送エラー」; việc kiểm chúng trên production được ghi ở follow-up.

Việc cần người làm thêm (ngoài phạm vi task):
- Kiểm trên production xem có webhook_relay_setting nào đã lưu URL webhook LME chưa: SELECT bot_id, is_enabled, notify_is_enabled FROM webhook_relay_setting WHERE endpoint_url LIKE '%/line/callback/add/%' OR notify_endpoint_url LIKE '%/line/callback/add/%'; có thì báo khách đổi URL hoặc tắt kênh.
- Các release đã có Webhook転送 nhưng chưa có #43730 (release_step_20260930, release_staging_20261014/_v2) sẽ nhận request chuyển tiếp như webhook thật; nên đưa #43730 lên cùng hoặc trước bản sửa này.
- Cân nhắc ticket riêng cho job java-job (HandleForwardCallbackEventTask/HandleForwardLmeEventTask): bỏ qua URL webhook LME lúc gửi, để chặn cả cấu hình cũ.
- Cập nhật spec-features admin/webhook-relay §6.5: thêm luật chặn URL webhook LME.
- Kiểm production xem đã có cấu hình Webhook転送 nào lưu sẵn URL webhook LME chưa. Bản sửa không tự đổi các cấu hình cũ, khách phải tự xoá hoặc đổi URL ở lần lưu tiếp theo.
- Cân nhắc chặn thêm ở job Java (WebhookRelayTask, module job) lúc gửi, để cấu hình cũ không còn chuyển tiếp event ngược về LME. Việc này nằm ngoài module web của task.
- Chạy trên production: SELECT bot_id, is_enabled, notify_is_enabled FROM webhook_relay_setting WHERE endpoint_url LIKE '%/line/callback/add/%' OR notify_endpoint_url LIKE '%/line/callback/add/%'; nếu có dòng thì báo khách xoá/đổi URL (bản sửa chỉ chặn lúc lưu, không sửa cấu hình cũ).
- Cân nhắc ticket riêng cho job java (module job) để chặn URL webhook LME lúc gửi, phòng cấu hình cũ và URL lách bằng dot-segment.

Điểm cần test:
- Tab LINE: bật và nhập https://<domain webhook LME>/line/callback/add/<bot_id>, bấm 「保存する」 → lỗi 「このURLは転送先に指定できません。」 dưới ô URL, HTTP 422, DB không đổi
- Biến thể bị chặn: bot_id của bot khác, domain webhook khác, chữ hoa, dấu // , %2F, có query string
- Tab LME: cùng các ca trên đều bị chặn
- Switch tắt nhưng URL là webhook LME → vẫn bị chặn
- Hồi quy: URL https ngoài hợp lệ lưu được; http://, >1024 ký tự, có khoảng trắng, localhost/IP nội bộ, host không phân giải vẫn báo lỗi như cũ; URL rỗng + tắt lưu được
- Chạy unit test WebhookUrlValidatorLmeWebhookTest
- Tab 「LINE公式アカウントデータ転送」: bật switch, nhập đúng Webhook URL hiển thị ở 「LOA接続設定」 của bot (…/line/callback/add/<bot_id>), bấm 「保存する」 → lỗi 「このURLは転送先に指定できません。」 dưới ô URL, không lưu (tải lại trang vẫn giá trị cũ).
- Tab 「L Messageデータ転送」: cùng thao tác → bị chặn tương tự.
- Switch tắt + URL webhook LME → vẫn bị chặn.
- Biến thể: bot_id của bot khác, domain webhook khác (cb.lme.jp / domain môi trường), chữ hoa /LINE/Callback/Add/1, //line//callback/add/1, /line%2Fcallback%2Fadd/1, có ?a=1 → đều bị chặn.
- Hồi quy: URL https ngoài hợp lệ → lưu được; http://, >1024 ký tự, có khoảng trắng, localhost/IP nội bộ, cổng khác 443, host không phân giải → báo lỗi như cũ; URL rỗng + tắt → lưu được.
- Bot đã lưu URL LME trước bản sửa: trang vẫn hiển thị URL đó; bấm 「保存する」 (kể cả chỉ tắt switch) → bị chặn cho tới khi xoá/đổi URL.

Branch: ai_studio_fixbug_44660
- sns-line: ai_studio_fixbug_44660 (nhánh gốc release_step_20260930_v2 @303a131b9c03, commit 3ddf9d4c11c1eadb26fe33dab72a7a8d9ca1c459)
```

**Journal #150058 — Dev Studio — 2026-11-02:**

```
Dev handoff — 02/11 09:41 · nhánh ai_studio_fixbug_44660

Nguyên nhân:
QA test trên commit bản 1 (3ddf9d4c). Ở bản đó hàm isLmeWebhookUrl() của WebhookUrlValidator chưa rút gọn đoạn '.'/'..', nên URL /line/./callback/add/1 không khớp mẫu chặn. Bản 2 (4d8510dcf8) đã thêm bước rút gọn này và ca test cho đúng URL đó; HEAD hiện tại (676e01b687) vẫn giữ bước này. Bản 3 chưa được bàn giao nên QA chưa test được code đã sửa.

Nội dung thay đổi:
- Màn 「Webhook転送」 (tab 「LINE公式アカウントデータ転送」 và 「L Messageデータ転送」), nút 「保存する」: nếu sau khi chuẩn hoá, path của URL chứa /line/callback/add thì bị từ chối với HTTP 422, lỗi 「このURLは転送先に指定できません。」 hiện dưới ô URL và không lưu. Luật áp dụng cho mọi domain và bot_id, không phân biệt hoa thường; chuẩn hoá xử lý //, %2F, /./, /../, %2e, \, %5C và URL có query.

Bug QA con:
- #44843 đã sửa (commit sns-line@4d8510dcf864, sns-line@676e01b687cc): Đã sửa ở 4d8510dcf8: thêm bước rút gọn đoạn ./.. (kể cả %2e) trước khi so path; 676e01b687 giữ bước này và xử lý thêm dấu \. QA đã test trên 3ddf9d4c (trước bản sửa), nên cần re-test trên bản giao mới.

File đã sửa (php-web):
  app/Services/WebhookRelay/WebhookUrlValidator.php | 48 ++++++++++++++-
  tests/Unit/WebhookUrlValidatorLmeWebhookTest.php  | 71 +++++++++++++++++++++++
  2 files changed, 118 insertions(+), 1 deletion(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi chỉ thêm một luật validate thuần (không gọi DNS) trong validator của một màn; không đổi DB, FE hay job; có 29 ca unit test.
- WebhookUrlValidator dùng chung cho cả 2 kênh qua API lưu cấu hình Webhook転送: kiểm lại các lỗi cũ (rỗng khi bật, http://, dài hơn 1024 ký tự, khoảng trắng, ký tự lạ, localhost/IP nội bộ, cổng khác 443, host không phân giải được).
- Cấu hình đã lưu URL LME trước bản sửa vẫn còn và job vẫn chuyển tiếp tới đó. Lần bấm 「保存する」 kế tiếp ở tab đó sẽ bị chặn (kể cả khi chỉ tắt công tắc) cho tới khi người dùng xoá hoặc đổi URL.
- Job java chuyển tiếp không đổi. MCP và app mobile không ghi cấu hình này.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Lỗi chỉ nằm ở bước kiểm tra lúc lưu cấu hình. URL sai trên môi trường test đã được Test Studio đổi lại ngay trong lượt test. Việc kiểm tra cấu hình production đã nằm trong follow-up của bản 1.

Việc cần người làm thêm (ngoài phạm vi task):
- QA test lại #44843 / Test Studio #4929 trên bản giao mới (HEAD 676e01b687): cả tab LINE và tab LME, công tắc bật và tắt, URL https://8.8.8.8/line/./callback/add/1 phải báo lỗi 「このURLは転送先に指定できません。」, trả HTTP 422 và sau F5 vẫn giữ URL cũ.

Điểm cần test:
- Tab LINE và tab LME, công tắc bật và tắt: nhập https://8.8.8.8/line/./callback/add/1 → hiện lỗi 「このURLは転送先に指定できません。」, HTTP 422, sau F5 vẫn là URL cũ
- Trong cùng lượt: /x/../line/callback/add/1 và /x/%2e%2e/line/callback/add/1 vẫn bị chặn; https://8.8.8.8/webhook-before lưu được
- Hồi quy các ca của bản 1–3 (domain LME, chữ hoa, //, %2F, dấu \) vẫn bị chặn
- QA phải test trên bản giao mới (HEAD 676e01b687), không test trên 3ddf9d4c
- Tab LINE và tab LME, công tắc bật và tắt: nhập https://8.8.8.8/line/./callback/add/1 rồi bấm 保存する → lỗi 「このURLは転送先に指定できません。」, HTTP 422; sau F5 ô URL vẫn là URL cũ (https://8.8.8.8/webhook-before)
- Cùng lượt test: /x/../line/callback/add/1, /x/%2e%2e/line/callback/add/1 và /line/%2e/callback/add/1 đều bị chặn
- https://8.8.8.8/webhook-before vẫn lưu được
- Hồi quy các lỗi cũ: rỗng khi bật, http://, dài hơn 1024 ký tự, localhost/IP nội bộ, cổng khác 443

Branch: ai_studio_fixbug_44660
- sns-line: ai_studio_fixbug_44660 (nhánh gốc release_step_20260930_v2 @303a131b9c03, commit 676e01b687cc2d70c455c210fe0eed4f77116ec1)
```

**Journal #150071 — Dev Studio — 2026-11-02:**

```
Automation Test Studio: pass ở lượt #6353. Lần bàn giao 02/11 09:41 @676e01b687cc chuyển sang chờ test.
```
