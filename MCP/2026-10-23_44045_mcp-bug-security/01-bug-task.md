# 01 — Bug Task từ khách hàng

> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL, môi trường phát hiện) tra thẳng trên Redmine khi cần, KHÔNG chép lại vào đây.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44045 — [MCP] Bug Security` |
| Module / Màn hình | `MCP server (backend-mcp-line)` — authorization check (IDOR trên id lồng trong payload), log JWT, SSRF ở `get_image_fileparams`, và kênh trả lỗi (error message) cho toàn bộ tool ghi: scenario filter/step/step_template, template (text/image/form/location), broadcast, friend info field, auto-reply, welcome message (addfriend setting message). |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Redmine `description` **trống** (`_(trong)_`). Tracker là **"Bug tự detect"** — ticket này là audit security nội bộ do Dev tự phát hiện, KHÔNG phải bug user report. Toàn bộ nội dung nguyên nhân/fix nằm trong journal Dev (chép nguyên văn ở cuối file). Tóm tắt lại đây để dễ đọc:

Server MCP chuyển các id lồng trong payload (`filter`, `action`, `template`, `option`, `url`, `lmePage`, `templateChildId`) sang linect mà **không kiểm id đó thuộc bot nào**. linect chỉ kiểm chữ ký HMAC, PHP chỉ kiểm user có quyền với `botId` ngoài cùng → MCP là **lớp kiểm quyền duy nhất**, và đang thiếu → nguy cơ **IDOR** (agent/AI gửi sai id của bot khác thì vẫn sửa được dữ liệu bot đó, vd filter/action/template/option/url/lmePage).

Ngoài lỗ hổng IDOR chính, ticket gộp 3 vấn đề bảo mật khác:
- `LmeHttpClient` ghi **JWT** (token xác thực) ra log server.
- `get_image_fileparams` gọi tới URL ảnh **tuỳ ý**, không chặn host nội bộ → nguy cơ **SSRF**.
- Thư viện MCP + `GlobalExceptionHandler` trả **nguyên message lỗi gốc** (body PHP, lỗi SQL) ra ngoài cho AI/client gọi tool.

## Steps to reproduce

<!-- Để trống — ticket không có case tái hiện cụ thể (audit code, không phải bug user report). Case cụ thể để verify từng điểm fix xem "Điểm cần test" ở cuối 03-dev-impact.md. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Không có attachment trên Redmine (0).

## Ghi chú thêm của Leader

- ⚠️ Ticket **không có bước tái hiện** — audit security nội bộ (tracker "Bug tự detect"), không phải bug khách hàng báo. TCs nên bám **D-1 → D-15** (cách fix) + "Điểm cần test" Dev gợi ý ở file 03, KHÔNG cần viết theo khung Steps to reproduce.
- Branch fix: `ai_studio_fixbug_44045` (gốc `release-product-mcp-api-202609` @`5f2f14e004fe`, commit `da61f2e2bea63985b7f1b92241038803f54564e3`).
- Rủi ro theo Dev: **Trung bình** — đổi kênh lỗi chung của mọi tool MCP + thêm kiểm quyền sở hữu vào nhiều tool ghi; payload AI gửi id "copy nhầm" sẽ bị chặn (có thể làm hỏng luồng hợp lệ nếu kiểm sai).
- **Recover data**: KHÔNG cần — token JWT đã ghi vào log trước fix: Dev (DucNV, 22/10/2026) chọn để tự hết hạn sau 30 ngày thay vì xoá log. Với lỗi IDOR: DB điều tra không thấy bản ghi liên kết chéo bot do MCP tạo ra; các bản ghi lệch còn lại có từ trước khi có MCP.
- 2 ticket liên quan cần port fix sang nhánh `release-product-202609-v2` sau (Dev chọn để sau, ngoài phạm vi task này): **#44047** (log token) và **#44048** (SSRF).
- Dev liệt kê thêm nhiều mục **ngoài phạm vi task** (chưa sửa trong #44045) — xem đầy đủ ở "Ghi chú thêm từ Dev" trong file 03: `actions[].id`/`actionId` chưa được kiểm thuộc bot ở mọi tool nhận `actions`; PHP `/api/mobile/save-action` không kiểm bot; nhiều tool khác thiếu trong `TOOL_ACCESS_MAP`; `update_*_template` sửa được template của broadcast/kịch bản cùng bot mà bỏ qua kiểm trạng thái.

## Journal / note từ Redmine (nguyên văn)

**Journal #147320 — Dev Studio — 2026-10-22:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Server MCP chuyển các id lồng trong payload (filter, action, template, option, url, lmePage, templateChildId) sang linect mà không kiểm id đó thuộc bot. linect chỉ kiểm chữ ký HMAC, PHP chỉ kiểm user có quyền với botId ngoài cùng, nên MCP là lớp kiểm duy nhất. Ngoài ra `LmeHttpClient` ghi JWT ra log; `get_image_fileparams` gọi tới URL tuỳ ý mà không chặn host nội bộ; thư viện MCP và `GlobalExceptionHandler` trả nguyên message lỗi gốc, làm lộ body PHP và lỗi SQL.

Hướng sửa:
- D-1 Bỏ ghi JWT ra log và xoá hàm isTokenBlacklisted không dùng
- D-2 Chặn SSRF khi server đọc ảnh và ảnh OGP từ URL
- D-3 Không trả body PHP hay lỗi hệ thống trong message lỗi
- D-4 Làm sạch lỗi trên kênh tool MCP chính
- D-5 Thêm truy vấn và hàm kiểm dùng chung
- D-6 save_scenario_filter: kiểm filter_manager và id trong filter
- D-7 save_scenario_step: kiểm action_id và filter khi tạo mới
- D-8 Kiểm lmePage.id cho các tool broadcast
- D-9 Kiểm urls[] của template text cho cả 6 tool
- D-10 save_scenario_step_template: chạy đủ các bước kiểm template
- D-11 edit_broadcast_template: templateChildId phải thuộc broadcast
- D-12 update_addfriend_setting_message: kiểm template_id và quyền
- D-13 save_friend_info_field: kiểm detailsAction, option id và actionId
- D-14 save_autoreply: kiểm copy_id, categoryId, actionId, keyword id
- D-15 Unit test cho các hàm kiểm mới

Ảnh hưởng / rủi ro:
Thay đổi nằm trong server MCP: mọi lời gọi sang LME, kênh lỗi của mọi tool, và 12 tool ghi (kịch bản, tin chào, thông tin bạn bè, auto-reply, template, broadcast). Rủi ro chính: nội dung lỗi trả cho AI thay đổi, các payload mang id sai hoặc copy nhầm sẽ bị chặn, và URL ảnh có redirect sẽ không còn lấy được kích thước.
```

**Journal #147390 — Dev Studio — 2026-10-23:**

```
Dev handoff — 23/10 09:17 · nhánh ai_studio_fixbug_44045

Nguyên nhân:
Server MCP chuyển các id lồng trong payload (filter, action, template, option, url, lmePage, templateChildId) sang linect mà không kiểm id đó thuộc bot. linect chỉ kiểm chữ ký HMAC, PHP chỉ kiểm user có quyền với botId ngoài cùng, nên MCP là lớp kiểm duy nhất. Ngoài ra `LmeHttpClient` ghi JWT ra log; `get_image_fileparams` gọi tới URL tuỳ ý mà không chặn host nội bộ; thư viện MCP và `GlobalExceptionHandler` trả nguyên message lỗi gốc, làm lộ body PHP và lỗi SQL.

Nội dung thay đổi:
- Log server: không còn in JWT khi MCP gọi sang LME.
- get_image_fileparams: chỉ đọc kích thước ảnh qua https, không theo redirect, bỏ qua host nội bộ (127.x, 10.x, 169.254.x, localhost…) và ảnh > 10MB; khi bị bỏ qua thì trả object không có kích thước.
- Kiểm kích thước ogp.imageUrl của template text: không theo redirect, bỏ qua host nội bộ.
- Mọi tool MCP và /call-tool: lỗi hệ thống trả 'Internal server error (rid=…)'; lỗi validate, lỗi quyền và lỗi LME đã phân loại vẫn giữ message; LME_REJECTED_RAW và LME_SERVER_ERROR không còn kèm body PHP (Public API cũng vậy).
- save_scenario_filter: filter_manager_id phải thuộc đúng kịch bản; id dòng filter phải thuộc filter đó; các id trong điều kiện filter (tag, friend info…) phải thuộc bot.
- save_scenario_step: tạo step mới chỉ được dùng filter của chính kịch bản đó và action chain của bot; khi sửa step, action_id phải là action_id hiện có của step.
- save_scenario_step_template: kiểm detail_action, LIFF, lmePage và URL của template text giống broadcast.
- update_addfriend_setting_message: template phải là template cha của bot; staff cần quyền 「友だち追加時設定」.
- save_friend_info_field: option id, actionId và detailsAction phải thuộc field/bot.
- save_autoreply: copy_id, categoryId, actionId và id keyword phải thuộc bot/rule.
- Template text (create/update_text_template, create_broadcast, add/edit_broadcast_template, save_scenario_step_template): urlId/actionId/outTimeActionId phải thuộc template đang sửa, tạo mới thì để trống; action gắn với URL phải thuộc bot.
- create_broadcast, add/edit_broadcast_template: lmePage.id của nút form và vùng chạm ảnh phải thuộc bot.
- edit_broadcast_template: templateChildId phải thuộc broadcast_id.

File đã sửa (java-mcp):
  .../wssv/backendmcpline/BackendMcpApplication.java |  32 ++++-
  .../wssv/backendmcpline/mcp/McpAutoReplyTool.java  |  47 ++++++-
  .../wssv/backendmcpline/mcp/McpBroadcastTool.java  |  88 ++++++++++--
  .../wssv/backendmcpline/mcp/McpFriendInfoTool.java |  71 ++++++++++
  .../wssv/backendmcpline/mcp/McpScenarioTool.java   |  72 +++++++++-
  .../wssv/backendmcpline/mcp/McpTemplateTool.java   |  32 +----
  .../backendmcpline/mcp/McpWelcomeMessageTool.java  |  16 +++
  .../model/exception/ClientErrorMessage.java        |  43 ++++++
  .../model/exception/GlobalExceptionHandler.java    |   3 +-
  .../repositories/ActionDetailRepository.java       |   4 +
  .../linedb/repositories/FilterRepository.java      |   6 +
  .../wssv/backendmcpline/security/jwt/JwtUtil.java  |  13 --
  .../backendmcpline/services/BroadcastService.java  |  19 +++
  .../FilterActionIdAuthorizationValidator.java      | 129 ++++++++++++++++-
  .../backendmcpline/services/LmeHttpClient.java     |  17 ++-
  .../backendmcpline/services/SecurityService.java   |   1 +
  .../wssv/backendmcpline/utils/MediaUtil.java       |  91 +++++++++++-
  .../model/exception/ClientErrorMessageTest.java    |  76 ++++++++++
  ...ctionIdAuthorizationValidatorOwnershipTest.java | 155 +++++++++++++++++++++
  .../backendmcpline/utils/MediaUtilSsrfTest.java    |  69 +++++++++
  20 files changed, 907 insertions(+), 77 deletions(-)

Đánh giá ảnh hưởng — Rủi ro trung bình: Sửa kênh lỗi chung của mọi tool MCP và thêm kiểm quyền sở hữu vào nhiều tool ghi; payload AI gửi id 'copy nhầm' sẽ bị chặn. Đã chạy unit test nhưng chưa verify runtime.
- Mọi tool MCP (Stateless và SSE): lỗi nay đi qua wrapper logToolInvocation nên message trả về đổi dạng, và mọi lỗi đều ghi [TOOL_FAIL] mức ERROR.
- GlobalExceptionHandler (lỗi 500 của /call-tool và mọi controller): message thành câu chung kèm rid.
- LmeHttpClient dùng cho mọi lời gọi MCP sang LME: message lỗi 4xx không parse được và 5xx bỏ body; Public API trả 422 với detail 'status=…' thay cho body.
- Validator dùng chung FilterActionIdAuthorizationValidator: validate (broadcast, scenario template, auto-reply, scenario filter, friend info) và validateAndEnrichTemplateDataActions (create/update text/image/form/location template) quét thêm message_text.urls[].
- Form/image template (create/update_form_template, create/update_image_template): hàm kiểm lmePage chuyển sang validator, hành vi phải giữ nguyên.
- MediaUtil.validateImageUrlSize: dùng khi build URL setting có ogp.imageUrl của template text và broadcast.
- SecurityService.TOOL_ACCESS_MAP: staff không có quyền 123 bị chặn update_addfriend_setting_message.
- Luồng copy auto-reply và luồng sửa template text có URL đã lưu (id lấy từ get_template_detail) phải vẫn chạy.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Token đã ghi vào log: anh DucNV (22/10/2026) chọn chờ token hết hạn sau 30 ngày. Với các lỗi IDOR, DB điều tra không có bản ghi liên kết chéo bot do MCP tạo ra; các bản ghi lệch còn lại có từ trước khi có MCP.

Việc cần người làm thêm (ngoài phạm vi task):
- Port bản sửa log token (#44047) và SSRF (#44048) sang nhánh release-product-202609-v2 khi đến lượt nhánh đó.
- actions[].id và actions[].actionId (DetailActionBuilder) không được kiểm thuộc bot ở mọi tool nhận actions; option id của friend_info trong action cũng chưa được kiểm. Nên tạo ticket riêng.
- Các tool update_*_template sửa được template của broadcast hoặc kịch bản cùng bot mà bỏ qua bước kiểm trạng thái được sửa; nên tạo ticket riêng.
- Nhiều tool khác thiếu trong TOOL_ACCESS_MAP nên bỏ qua phân quyền theo vai trò (mục P1-9 của audit); nên tạo ticket riêng.
- PHP /api/mobile/save-action và một số API PHP nhận id ngoại bot mà không kiểm (không xử lý trong task này theo anh DucNV).
- Chạy lại các câu kiểm dữ liệu chéo bot trên production (DB điều tra chỉ tới khoảng 06/2026).
- Lỗi IllegalStateException có message hướng dẫn giờ chỉ còn 'Internal server error (rid=…)' trên kênh MCP, vì thiết kế D-3 không giữ loại lỗi này. Ví dụ: SecurityService.assertNotBackup ('Bot is currently in backup state… retry later') ở các tool template. Cần quyết định có thêm loại lỗi này (hoặc đổi assertNotBackup sang IllegalArgumentException) ở vòng sau không.
- Lỗi ép kiểu JSON không do @JsonCreator ném ra (vd 'Cannot deserialize value of type…' của Jackson) trước đây tới AI nguyên văn, giờ thành câu chung kèm rid. Nên theo dõi log [TOOL_FAIL] sau khi deploy để xem AI có tự sửa payload kém đi không.
- Port các sửa log token và SSRF sang nhánh release-product-202609-v2 sau (DucNV đã chọn để sau).
- Chạy lại các câu kiểm dữ liệu chéo bot của docs/investigation/v1.md trên production. DB điều tra chỉ có dữ liệu tới khoảng 06/2026.
- Các phát hiện ngoài phạm vi chưa sửa: actions[].id/actionId của DetailAction ở mọi tool chưa được kiểm; PHP /api/mobile/save-action không kiểm bot; nhiều tool khác vẫn thiếu trong TOOL_ACCESS_MAP và đang được cho qua (P1-9); update_*_template sửa được template của broadcast hoặc kịch bản cùng bot.
- Cải tiến kênh lỗi MCP: trả message rõ ràng cho lỗi tham số sai kiểu (JsonMappingException) và cho các lỗi có hướng dẫn (assertNotBackup, Salon/Lesson calendar not found), đồng thời ghi lỗi validate ở mức WARN không kèm stack (R-1..R-3 của review v1).

Điểm cần test:
- Sau khi gọi tool ghi, log không còn chuỗi token; header Authorization gửi sang LME vẫn có.
- get_image_fileparams với URL https công khai trả kích thước; với http, 127.0.0.1, 169.254.169.254, 10.x, localhost hoặc URL có redirect thì không trả kích thước và server không gửi request tới host nội bộ; ảnh lớn hơn 10MB bị bỏ qua.
- Lỗi LME 4xx/5xx và lỗi SQL, qua kênh MCP lẫn /call-tool: không lộ body hay SQL; lỗi validate vẫn hiện nguyên message.
- Trên bot A, từng tool save_scenario_filter, save_scenario_step, save_scenario_step_template, update_addfriend_setting_message, save_friend_info_field, save_autoreply, create/update_text_template, create_broadcast, add_broadcast_template, edit_broadcast_template: từ chối id của bot B và chạy bình thường với id của bot A.
- edit_broadcast_template với templateChildId của broadcast khác (cùng bot) bị chặn.
- Copy auto-reply (init_autoreply_form có copy_id rồi save_autoreply) vẫn chạy bình thường.
- Tạo step mới gắn filter vừa tạo bằng save_scenario_filter vẫn chạy; gắn filter của kịch bản khác thì bị chặn.
- Staff không có quyền 「友だち追加時設定」 gọi update_addfriend_setting_message thì bị chặn (403).
- Log server sau khi gọi một tool ghi (vd save_autoreply) không còn chuỗi JWT; lời gọi sang LME vẫn thành công (header Authorization vẫn có).
- get_image_fileparams: download_url https công khai thì có img_width/img_height; với http://, https://127.0.0.1, 169.254.169.254, 10.x, localhost, URL có redirect và ảnh > 10MB thì trả object không có kích thước và server không gửi request tới host nội bộ.
- Lỗi LME 5xx, lỗi 4xx không parse được và lỗi SQL, gọi qua MCP lẫn /call-tool, không lộ body PHP hay SQL, chỉ còn 'Internal server error (rid=…)'; lỗi validate và lỗi LME_REJECTED vẫn hiện nguyên message.
- Hai bot test A/B cùng admin: save_scenario_filter, save_scenario_step, save_scenario_step_template, update_addfriend_setting_message, save_friend_info_field, save_autoreply, create/update_text_template, create_broadcast, add_broadcast_template, edit_broadcast_template từ chối id của bot B và chạy bình thường với id của bot A.
- save_scenario_filter: filter_manager_id của kịch bản khác trong cùng bot thì bị chặn; sửa filter với id dòng filter lấy từ get_scenario_detail thì chạy.
- save_scenario_step: tạo step mới với filter của kịch bản khác thì bị chặn; sửa step mà giữ action_id lấy từ get_scenario_detail thì chạy, đổi sang action_id khác thì bị chặn.
- edit_broadcast_template với templateChildId của broadcast khác thì bị chặn.
- Copy auto-reply (init_autoreply_form với copy_id, rồi save_autoreply với copy_id và actionId clone) vẫn chạy; sửa rule với id keyword hiện có thì chạy.
- update_text_template giữ nguyên urlSettings (urlId/actionId lấy từ get_template_detail) thì chạy; tạo template mới có urlId thì bị chặn kèm hướng dẫn bỏ id.
- save_friend_info_field: sửa field giữ option id cũ thì chạy; option id của field khác thì bị chặn.
- Staff không có quyền 「友だち追加時設定」 gọi update_addfriend_setting_message thì bị 403.
- Form/image template (create/update_form_template, create/update_image_template) có lmePage của bot vẫn tạo/sửa được (hàm kiểm đã chuyển chỗ).

Branch: ai_studio_fixbug_44045
- backend-mcp-line: ai_studio_fixbug_44045 (nhánh gốc release-product-mcp-api-202609 @5f2f14e004fe, commit da61f2e2bea63985b7f1b92241038803f54564e3)
```
