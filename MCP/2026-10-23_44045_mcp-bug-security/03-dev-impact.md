# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #44045 (không có section "Đánh giá ảnh hưởng" theo khung chuẩn trong `description` — nội dung lấy nguyên văn từ 2 journal Dev, xem bản gốc ở `01-bug-task.md`).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (tác giả 2 journal trên Redmine) — assignee Redmine: `Văn Đức Nguyễn` |
| Commit / Pull Request | `<chưa có link PR>` — commit gốc nhánh: `da61f2e2bea63985b7f1b92241038803f54564e3` |
| Branch | `ai_studio_fixbug_44045` (gốc `release-product-mcp-api-202609` @`5f2f14e004fe`) |
| Ngày submit đánh giá | `2026-10-23` (Journal #147390, handoff cuối) |
| Auto-filled | `2026-10-23 by /new-task-mcp` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại 2 journal Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Server MCP (`backend-mcp-line`) chuyển các id lồng trong payload (`filter`, `action`, `template`, `option`, `url`, `lmePage`, `templateChildId`) sang **linect** mà **không kiểm id đó thuộc bot nào**. linect chỉ kiểm chữ ký HMAC, PHP chỉ kiểm user có quyền với `botId` ngoài cùng → **MCP là lớp kiểm quyền duy nhất**, và lớp đó đang thiếu. Hậu quả: payload mang id của **bot khác** (IDOR) có thể đi lọt qua và sửa dữ liệu không thuộc bot đang gọi.

3 vấn đề bảo mật phụ gộp chung ticket:
- `LmeHttpClient` ghi **JWT** (token xác thực của user) ra log server khi MCP gọi sang LME.
- `get_image_fileparams` gọi tới **URL ảnh tuỳ ý**, không chặn host nội bộ (127.x, 10.x, 169.254.x, localhost…) → nguy cơ **SSRF**.
- Thư viện MCP + `GlobalExceptionHandler` trả **nguyên message lỗi gốc** (body response PHP, lỗi SQL) ra cho AI/client gọi tool khi LME trả lỗi 4xx/5xx hoặc có exception hệ thống.

## 2. Cách fix

15 điểm fix (D-1 → D-15, Journal #147320), triển khai cụ thể theo Journal #147390:

| # | Điểm fix | Nội dung |
|---|---|---|
| D-1 | Bỏ ghi JWT ra log | `LmeHttpClient` không còn in token; xoá hàm `isTokenBlacklisted` không dùng (`JwtUtil`) |
| D-2 | Chặn SSRF đọc ảnh | `get_image_fileparams` + check `ogp.imageUrl` của template text: chỉ https, không theo redirect, bỏ qua host nội bộ, bỏ qua ảnh > 10MB; bị bỏ qua → trả object không có kích thước, **server không gửi request** tới host nội bộ (`MediaUtil`) |
| D-3 | Không trả body PHP / lỗi hệ thống | Lỗi hệ thống trả `'Internal server error (rid=…)'`; lỗi validate / quyền / LME đã phân loại vẫn giữ message gốc; `LME_REJECTED_RAW` + `LME_SERVER_ERROR` không kèm body PHP (cả MCP và Public API) |
| D-4 | Làm sạch lỗi kênh tool MCP chính | Mọi tool MCP (Stateless + SSE) đi qua wrapper `logToolInvocation`, mọi lỗi ghi `[TOOL_FAIL]` mức ERROR |
| D-5 | Hàm kiểm dùng chung | `FilterActionIdAuthorizationValidator.validate(...)` + `validateAndEnrichTemplateDataActions(...)` — dùng cho broadcast / scenario template / auto-reply / scenario filter / friend info, quét thêm `message_text.urls[]` |
| D-6 | `save_scenario_filter` | `filter_manager_id` phải thuộc đúng kịch bản; id dòng filter phải thuộc filter đó; id trong điều kiện filter (tag, friend info…) phải thuộc bot |
| D-7 | `save_scenario_step` | Tạo step mới chỉ dùng filter của chính kịch bản + action chain của bot; sửa step thì `action_id` phải là `action_id` hiện có của step |
| D-8 | Kiểm `lmePage.id` cho tool broadcast | `create_broadcast`, `add/edit_broadcast_template`: `lmePage.id` của nút form + vùng chạm ảnh phải thuộc bot |
| D-9 | Kiểm `urls[]` template text (6 tool) | `urlId`/`actionId`/`outTimeActionId` phải thuộc template đang sửa, tạo mới để trống; action gắn URL phải thuộc bot |
| D-10 | `save_scenario_step_template` | Kiểm `detail_action`, LIFF, `lmePage`, URL của template text — giống logic broadcast |
| D-11 | `edit_broadcast_template` | `templateChildId` phải thuộc `broadcast_id` |
| D-12 | `update_addfriend_setting_message` | Template phải là template cha của bot; staff cần quyền 「友だち追加時設定」(quyền 123) |
| D-13 | `save_friend_info_field` | `option id`, `actionId`, `detailsAction` phải thuộc field/bot |
| D-14 | `save_autoreply` | `copy_id`, `categoryId`, `actionId`, id keyword phải thuộc bot/rule |
| D-15 | Unit test | Test cho các hàm kiểm mới (`ClientErrorMessageTest`, `FilterActionIdAuthorizationValidatorOwnershipTest`, `MediaUtilSsrfTest`) |

**Migration / thay đổi dữ liệu: KHÔNG có** (Dev đã kiểm diff).
**Recover data: KHÔNG cần** — token đã ghi log trước fix: Dev chọn để tự hết hạn sau 30 ngày (không xoá/rotate log); với lỗi IDOR, DB điều tra không phát hiện bản ghi liên kết chéo bot do MCP tạo ra (bản ghi lệch còn lại có từ trước khi có MCP).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BackendMcpApplication.java` | +32/−? | Wiring wrapper lỗi / log |
| 2 | `mcp/McpAutoReplyTool.java` | +47 | D-14 kiểm `copy_id`/`categoryId`/`actionId`/keyword |
| 3 | `mcp/McpBroadcastTool.java` | +88 | D-8, D-9, D-11 kiểm `lmePage`, `urls[]`, `templateChildId` |
| 4 | `mcp/McpFriendInfoTool.java` | +71 | D-13 kiểm option id/`actionId`/`detailsAction` |
| 5 | `mcp/McpScenarioTool.java` | +72 | D-6, D-7, D-10 kiểm filter/step/step_template |
| 6 | `mcp/McpTemplateTool.java` | +32/−(hàm kiểm lmePage chuyển ra validator) | D-9, D-10 |
| 7 | `mcp/McpWelcomeMessageTool.java` | +16 | D-12 kiểm template cha + quyền 123 |
| 8 | `model/exception/ClientErrorMessage.java` | +43 (mới) | D-3 chuẩn hoá message lỗi |
| 9 | `model/exception/GlobalExceptionHandler.java` | +3/−? | D-3, D-4 |
| 10 | `linedb/repositories/ActionDetailRepository.java` | +4 | Query kiểm action thuộc bot (D-5) |
| 11 | `linedb/repositories/FilterRepository.java` | +6 | Query kiểm filter thuộc bot/kịch bản (D-5) |
| 12 | `security/jwt/JwtUtil.java` | −13 | D-1 xoá `isTokenBlacklisted` |
| 13 | `services/BroadcastService.java` | +19 | Hỗ trợ D-8, D-11 |
| 14 | `services/FilterActionIdAuthorizationValidator.java` | +129 | D-5 validator dùng chung (file lớn nhất bị sửa) |
| 15 | `services/LmeHttpClient.java` | +17/−? | D-1 bỏ log JWT, D-3 bỏ body lỗi |
| 16 | `services/SecurityService.java` | +1 | D-12 `TOOL_ACCESS_MAP` quyền 123 |
| 17 | `utils/MediaUtil.java` | +91 | D-2 chặn SSRF + check kích thước ảnh |
| 18-20 | 3 file unit test mới | +300 | D-15 |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Mọi tool MCP (Stateless + SSE) qua wrapper `logToolInvocation` | `BackendMcpApplication.java` | Direct | Message lỗi trả về đổi dạng cho **mọi** tool, không riêng 12 tool ghi |
| F2 | `GlobalExceptionHandler` (lỗi 500 của `/call-tool` + mọi controller) | `GlobalExceptionHandler.java` | Direct | Message thành câu chung kèm `rid` |
| F3 | `LmeHttpClient` (mọi lời gọi MCP → LME) | `LmeHttpClient.java` | Direct | 4xx không parse được + 5xx bỏ body; Public API 422 trả `detail='status=…'` thay body |
| F4 | `FilterActionIdAuthorizationValidator` (validate + validateAndEnrichTemplateDataActions) | `FilterActionIdAuthorizationValidator.java` | Direct | Dùng chung cho broadcast / scenario template / auto-reply / scenario filter / friend info; quét thêm `message_text.urls[]` |
| F5 | `save_scenario_filter` | `McpScenarioTool.java` | Direct | D-6 |
| F6 | `save_scenario_step` | `McpScenarioTool.java` | Direct | D-7 |
| F7 | `save_scenario_step_template` | `McpScenarioTool.java` / `McpTemplateTool.java` | Direct | D-10 |
| F8 | `update_addfriend_setting_message` | `McpWelcomeMessageTool.java` | Direct | D-12 |
| F9 | `save_friend_info_field` | `McpFriendInfoTool.java` | Direct | D-13 |
| F10 | `save_autoreply` (+ `init_autoreply_form` copy flow) | `McpAutoReplyTool.java` | Direct | D-14 |
| F11 | `create/update_text_template`, `create_broadcast`, `add/edit_broadcast_template` | `McpTemplateTool.java` / `McpBroadcastTool.java` | Direct | D-8, D-9 — `urlId`/`actionId`/`outTimeActionId` + `lmePage.id` |
| F12 | `edit_broadcast_template` | `McpBroadcastTool.java` | Direct | D-11 — `templateChildId` phải thuộc `broadcast_id` |
| F13 | `get_image_fileparams` | `utils/MediaUtil.java` | Direct | D-2 SSRF |
| F14 | `create/update_form_template`, `create/update_image_template` | (hàm kiểm `lmePage` chuyển sang validator) | Indirect | Hành vi phải **giữ nguyên** — chỉ đổi chỗ code, Dev tự note "cần verify không đổi hành vi" |
| F15 | `SecurityService.TOOL_ACCESS_MAP` | `SecurityService.java` | Direct | D-12 — staff thiếu quyền 123 bị chặn `update_addfriend_setting_message` |
| F16 | Log JWT khi gọi LME | `LmeHttpClient.java`, `JwtUtil.java` | Direct | D-1 |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Log server (file log ứng dụng) | UPDATE (format log) | Không còn in JWT; thêm `[TOOL_FAIL]` mức ERROR cho mọi lỗi tool |
| D2 | DB nghiệp vụ (filter / action / template / option / url / lmePage / broadcast / friend_info_field / autoreply) | **KHÔNG** CREATE/UPDATE/DELETE/MIGRATE | Dev confirm không có thay đổi dữ liệu — chỉ thêm validate (chặn trước khi ghi) |
| D3 | Token JWT đã ghi vào log (trước fix) | Recover data: **KHÔNG cần** | Chờ tự hết hạn 30 ngày — không phải tác vụ cleanup DB |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Kênh lỗi chung của **mọi** tool MCP (Stateless + SSE + `/call-tool`) | F1, F2, F3 | **High** — ảnh hưởng mọi tool kể cả tool đọc; AI nhận message khác (ít chi tiết hơn) có thể tự sửa payload kém đi |
| T2 | Kịch bản (scenario) — filter & step | F4, F5, F6 | Medium — payload id "copy nhầm" bị chặn đúng, nhưng luồng sửa hợp lệ (lấy id từ `get_scenario_detail`) phải không bị chặn nhầm |
| T3 | Tin chào mừng / addfriend setting message | F8, F15 | Medium — thêm gate quyền 123, risk staff hợp lệ bị chặn nhầm |
| T4 | Thông tin bạn bè (friend info field) | F9 | Medium |
| T5 | Auto-reply (kể cả luồng copy rule) | F10 | Medium — luồng copy (`init_autoreply_form` + `copy_id`) phải vẫn chạy |
| T6 | Template (text/image/form/location) + Broadcast | F7, F11, F12, F14 | Medium — form/image template hành vi phải giữ nguyên dù code dời chỗ |
| T7 | `get_image_fileparams` / kiểm OGP image của template text | F13 | Low-Medium — fix SSRF, ảnh hưởng case redirect / host nội bộ / ảnh lớn |
| T8 | Log server (an ninh, không phải tính năng end-user) | F16 | Low |

---

## Ghi chú thêm từ Dev (ngoài 4 mục chuẩn)

**Việc cần làm thêm / ngoài phạm vi task #44045** (Dev đã nêu — Leader cân nhắc tạo ticket riêng, KHÔNG đưa vào scope coverage của review này, chỉ note để tránh hiểu nhầm là đã fix):
- Port fix log token (#44047) và SSRF (#44048) sang nhánh `release-product-202609-v2` khi tới lượt.
- `actions[].id` / `actions[].actionId` (`DetailActionBuilder`) **chưa được kiểm** thuộc bot ở mọi tool nhận `actions[]`; option id của `friend_info` trong action cũng chưa kiểm.
- Tool `update_*_template` sửa được template của broadcast/kịch bản **cùng bot** mà bỏ qua bước kiểm trạng thái được sửa.
- Nhiều tool khác vẫn thiếu trong `TOOL_ACCESS_MAP` → bỏ qua phân quyền theo vai trò (mục P1-9 của audit).
- PHP `/api/mobile/save-action` và một số API PHP khác nhận id ngoại bot không kiểm — không xử lý trong task này (theo quyết định DucNV).
- Case lỗi `IllegalStateException` có message hướng dẫn (vd `SecurityService.assertNotBackup`) giờ bị D-3 nuốt thành `'Internal server error (rid=…)'` trên kênh MCP — **có thể là regression hành vi** cần Leader quyết định ở vòng sau (giữ loại lỗi riêng hay đổi `assertNotBackup` sang `IllegalArgumentException`).
- Lỗi ép kiểu JSON của Jackson (không qua `@JsonCreator`, vd "Cannot deserialize value of type…") trước đây lộ nguyên văn cho AI, giờ thành câu chung kèm `rid` — cần theo dõi log `[TOOL_FAIL]` sau deploy xem AI có tự sửa payload kém đi không.
- Cần chạy lại câu kiểm dữ liệu chéo bot trên production (`docs/investigation/v1.md`) — DB điều tra chỉ có dữ liệu tới khoảng 06/2026.

**"Điểm cần test" Dev tự gợi ý** (từ 2 journal — tham khảo, KHÔNG thay cho review độc lập của Leader; đã gộp các điểm trùng giữa 2 journal):
1. Sau khi gọi tool ghi, log không còn chuỗi JWT; header `Authorization` gửi sang LME vẫn có.
2. `get_image_fileparams`: URL https công khai → trả `img_width`/`img_height`; URL http / `127.0.0.1` / `169.254.169.254` / `10.x` / `localhost` / có redirect / ảnh > 10MB → KHÔNG trả kích thước, server KHÔNG gửi request tới host nội bộ.
3. Lỗi LME 4xx/5xx (parse được / không parse được) + lỗi SQL, qua cả kênh MCP và `/call-tool`: không lộ body PHP / SQL, chỉ còn `'Internal server error (rid=…)'`; lỗi validate + `LME_REJECTED` vẫn hiện nguyên message.
4. 2 bot test A/B cùng admin: mỗi tool `save_scenario_filter`, `save_scenario_step`, `save_scenario_step_template`, `update_addfriend_setting_message`, `save_friend_info_field`, `save_autoreply`, `create/update_text_template`, `create_broadcast`, `add_broadcast_template`, `edit_broadcast_template` — từ chối id của bot B, chạy bình thường với id của bot A.
5. `edit_broadcast_template` với `templateChildId` của broadcast **khác** (cùng bot) → bị chặn.
6. Copy auto-reply (`init_autoreply_form` có `copy_id` → `save_autoreply` với `copy_id` + `actionId` clone) vẫn chạy bình thường; sửa rule giữ id keyword hiện có vẫn chạy.
7. Tạo step mới gắn filter vừa tạo bằng `save_scenario_filter` → chạy; gắn filter của kịch bản khác → bị chặn. Sửa step giữ `action_id` lấy từ `get_scenario_detail` → chạy; đổi sang `action_id` khác → bị chặn.
8. Staff không có quyền 「友だち追加時設定」(123) gọi `update_addfriend_setting_message` → bị chặn **403**.
9. `update_text_template` giữ nguyên `urlSettings` (urlId/actionId lấy từ `get_template_detail`) → chạy; tạo template mới có `urlId` → bị chặn kèm hướng dẫn bỏ id.
10. `save_friend_info_field`: sửa field giữ option id cũ → chạy; option id của field khác → bị chặn.
11. Form/image template (`create/update_form_template`, `create/update_image_template`) có `lmePage` của bot vẫn tạo/sửa được (hàm kiểm chỉ đổi chỗ, hành vi phải giữ nguyên).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
