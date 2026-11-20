# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45812 — [MCP][Public API] /v1/do_action: lỗi capture action_multi_capture do timestamp tính bằng mili-giây` |
| Module / Màn hình | Public API `POST /v1/do_action` (module callback, linect-service `McpModel.requestDoAction`) — bản chụp action (`action_multi_capture`) và các bảng lịch sử thao tác friend tham chiếu tới nó (`友だち追加履歴`, `タグ履歴`, `友だち情報追加履歴`...) |

> ⚠️ Ticket thuộc tracker **"Bug tự detect"** — tác giả = assignee = Dev (`Văn Đức Nguyễn`), tự phát hiện + tự viết root cause/fix trong description, **không có section "Tái hiện bug" theo format khách hàng báo** (Steps/Expected/Actual riêng). Nội dung "Hiện tượng" dưới đây đã gộp cả vai trò mô tả bug + cách trigger.

## Mô tả bug (bản dịch tiếng Việt)

**Hiện tượng:**
Gọi `POST /v1/do_action` → linect log ERROR:
```
HistoryHelper:52 #captureMultiAction error ... DataException: could not execute statement
```

**Ảnh hưởng:**
- Chỉ ảnh hưởng `Public API /v1/do_action`, **mọi request** (không phải case hiếm).
- Action vẫn áp lên friend bình thường (friend vẫn được gắn tag / đổi friend info / chặn.../ gửi tin đúng), nhưng **không ghi được `action_multi_capture`**
  → `action_multi_capture_id = null` trong các bảng lịch sử (`tag_history`, `friend_info_history`, `line_user_add_friend_history`...) — tức là **mất liên kết "xem lại action đã chạy"** trên màn lịch sử thao tác, chứ không mất dữ liệu nghiệp vụ.

## Steps to reproduce

1. Gọi `POST /v1/do_action` cho 1 friend với bất kỳ action nào (vd gắn tag), dùng API key hợp lệ của bot.
2. Quan sát response trả về.
3. Mở log linect ngay sau request, tìm dòng `#captureMultiAction`.
4. Mở trang chi tiết friend trên web, tab lịch sử thao tác tương ứng (vd `タグ履歴`), xem cột action/preview của dòng vừa phát sinh.

## Expected result

- Response vẫn `success = true` (hợp đồng API không đổi).
- Log có `#captureMultiAction new ... timestamp <10 chữ số>`, KHÔNG có `#captureMultiAction error`.
- `action_multi_capture` có dòng mới tương ứng; cột lịch sử (`action_multi_capture_id`) khác NULL; màn lịch sử thao tác hiện được chi tiết action (nút `プレビュー` → tab `アクション`).

## Actual result

- Response vẫn `success = true` (action áp dụng đúng cho friend).
- Log ghi `#captureMultiAction error ... DataException: could not execute statement` (môi trường lỗi: cột `action_multi_capture.timestamp` là `INT(11)`, giá trị mili-giây ~1.7×10¹² vượt giới hạn INT → INSERT lỗi, exception bị nuốt).
- `action_multi_capture_id` trong các bảng lịch sử thành `NULL` → màn lịch sử thao tác không hiện được chi tiết action đã chạy qua `do_action`.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — excerpt log lỗi `#captureMultiAction error ... DataException` đã nằm nguyên văn trong Description Redmine (không có file attachment riêng, `issue.attachments` rỗng).

## Ghi chú thêm của Leader

- Ticket **không có ca lỗi cụ thể của 1 khách hàng** (bug tự detect từ code, xảy ra với **mọi request** `/v1/do_action` ở môi trường có cột `action_multi_capture.timestamp` kiểu `INT`) → không có bảng "Dữ liệu định danh ca lỗi" (bỏ theo quy ước khi ticket không có ca lỗi cụ thể).
- Root cause + fix đã được Dev xác nhận trong 2 journal (xem bên dưới) — **rủi ro Dev tự đánh giá là THẤP**: đổi đúng 1 dòng code (đơn vị mili-giây → giây), không đổi request/response/schema, không cần migrate/recover dữ liệu (`DucNV` xác nhận 2026-11-12 không cần recover).
- Nhánh fix: `ai_studio_fixbug_45812` (linect-service, gốc `release-backend-mcp-api-v2-202610@a4d03ccd5f88`, commit `bd7e7cae4b1f1374e4f6384ba881f440a2a2571c`).
- Dev ghi rõ **còn lỗi cùng loại ở nơi khác, NGOÀI phạm vi ticket này** (không nên viết TC coverage cho các điểm sau trong task này, nhưng nên cân nhắc mở ticket riêng):
  - `ActionModel.java:136` và `HandlePostbackTask.java:4247`/`4248` vẫn fallback `System.currentTimeMillis()` (mili-giây) khi không tìm thấy `t_actions` — cùng loại lỗi, lối vào khác.
  - Web (`HelperService`, `MessageService`) ghi `action_multi_capture.timestamp = action_id nối update_timestamp` (vd `4907471779868544`) — giá trị này **vượt INT** luôn, không liên quan request `do_action`; migration hiện vẫn khai cột là `INT`.
  - Nhánh `release-backend-mcp-api-202609` (nhánh release khác) cũng còn dòng `McpModel.java:384` tính bằng mili-giây — nếu nhánh này còn deploy thì cần mang fix sang.
  - Vấn đề build/dependency (`build.gradle` thiếu `converter-jackson`) — thuộc hạ tầng CI/release, không liên quan logic bug, KHÔNG cần TC.
- MCP là 1 trong các caller gọi `Public API /v1/do_action` (chứ không phải bug nằm trong 1 MCP tool cụ thể) — cân nhắc dùng `/new-task-mcp` nếu Leader muốn đi luồng review MCP riêng, nhưng bản chất bug ở tầng Public API/linect-service dùng chung cho mọi caller nên `/new-task` + `/review-tc` thường vẫn phù hợp hơn.

## Journal / note từ Redmine (nguyên văn)

**Journal #154175 — Dev Studio — 2026-11-12:**
```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
`McpModel.requestDoAction` tạo action chain tạm với `update_timestamp = System.currentTimeMillis()` (mili-giây), trái quy ước giây của `t_actions.update_timestamp`. `ActionModel.doAction` đọc lại giá trị đó rồi truyền vào `HistoryHelper.captureMultiAction` để INSERT `action_multi_capture.timestamp`. Ở môi trường lỗi, cột này khi đó là INT nên giá trị khoảng 1,7×10^12 bị tràn và gây DataException. Lỗi bị nuốt nên `action_multi_capture_id` trong lịch sử thành NULL.

Hướng sửa:
- D-1 Đổi mốc thời gian của action tạm trong do_action sang giây

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng luồng Public API POST /v1/do_action: không đổi request/response, không đổi schema, không có dữ liệu cần recover. Sau khi sửa, action_multi_capture và version id của action detail được ghi bằng giây, thống nhất với các luồng khác.
```

**Journal #154183 — Dev Studio — 2026-11-12:**
```
Dev handoff — 12/11 11:29 · nhánh ai_studio_fixbug_45812

Nguyên nhân:
`McpModel.requestDoAction` tạo action chain tạm với `update_timestamp = System.currentTimeMillis()` (mili-giây), trái quy ước giây của `t_actions.update_timestamp`. `ActionModel.doAction` đọc lại giá trị đó rồi truyền vào `HistoryHelper.captureMultiAction` để INSERT `action_multi_capture.timestamp`. Ở môi trường lỗi, cột này khi đó là INT nên giá trị khoảng 1,7×10^12 bị tràn và gây DataException. Lỗi bị nuốt nên `action_multi_capture_id` trong lịch sử thành NULL.

Nội dung thay đổi:
- Public API /v1/do_action (module callback): action áp lên friend giờ có bản chụp action, và lịch sử thao tác (gắn tag, đổi thông tin friend…) liên kết tới bản chụp đó; hết lỗi '#captureMultiAction error ... DataException'.

File đã sửa (java-job):
  src/main/java/sns/line/models/McpModel.java | 2 +-
  1 file changed, 1 insertion(+), 1 deletion(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đổi đơn vị của 1 giá trị trong 1 hàm của 1 API, đưa về đúng quy ước giây mà mọi đường ghi t_actions khác đang dùng; compile qua khi thêm tạm dependency còn thiếu của base.
- ActionModel.doAction và HistoryHelper.captureMultiAction khi chạy từ do_action: timestamp của bản chụp giờ là giây.
- MessageModel.getVersionId cho action gửi tin text/template trong do_action: version id giờ tính từ giây như mọi action khác (đồng thời bỏ được nguy cơ tràn Long khi nối id với mili-giây).
- Bảng t_actions, t_actions_detail (action tạm, bị xoá sau request), action_multi_capture và các bảng lịch sử có cột action_multi_capture_id.
- Các luồng action khác (broadcast, kịch bản, postback, web) không đi qua requestDoAction nên không bị ảnh hưởng.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — DucNV quyết định ngày 12/11/2026 là không cần recover. Lỗi chỉ làm mất liên kết capture trong lịch sử do_action, còn action vẫn áp đúng cho friend.

Lưu ý khi deploy:
- Build nhánh cần dependency converter-jackson giống base hiện tại; lỗi này có sẵn, không do ticket này.

Việc cần người làm thêm (ngoài phạm vi task):
- ActionModel.doAction (dòng 136) và HandlePostbackTask (dòng 4247) vẫn fallback System.currentTimeMillis() (mili-giây) khi không tìm thấy t_actions. Cùng loại lỗi nhưng ở lối vào khác, nên cân nhắc mở ticket riêng.
- Web (HelperService, MessageService) ghi action_multi_capture.timestamp = action_id nối update_timestamp (vd 4907471779868544), giá trị này vượt INT. Cần bảo đảm cột này là BIGINT ở mọi môi trường; migration hiện vẫn khai báo INT.
- build.gradle của java-job thiếu dependency com.squareup.retrofit2:converter-jackson trong khi RequestHelper.java đang import nó, nên compileJava bằng Gradle bị lỗi; đội release cần kiểm tra lại cách build.
- Nhánh release-backend-mcp-api-202609 cũng còn dòng McpModel.java:384 tính bằng mili-giây: nếu nhánh này còn deploy thì cần mang bản sửa sang.
- Base release-backend-mcp-api-v2-202610 thiếu dependency converter-jackson nên RequestHelper.java không compile: cần bổ sung vào build.gradle của release.

Điểm cần test:
- Gọi /v1/do_action để gắn tag cho 1 friend test: tag được gắn, log không còn '#captureMultiAction error', có log '#captureMultiAction new' với timestamp 10 chữ số.
- Có dòng action_multi_capture mới với timestamp dạng giây (10 chữ số) và data_action đúng action đã gửi.
- tag_history của friend có action_multi_capture_id khác NULL; màn lịch sử thao tác hiện chi tiết action.
- Chạy với nhiều friend và nhiều action (tag, friend_info): friend nào cũng có lịch sử liên kết capture, response vẫn success như cũ.
- Sau request không còn sót dòng t_actions / t_actions_detail tạm.
- Build/compile Java của repo thành công.

Branch: ai_studio_fixbug_45812
- linect-service: ai_studio_fixbug_45812 (nhánh gốc release-backend-mcp-api-v2-202610 @a4d03ccd5f88, commit bd7e7cae4b1f1374e4f6384ba881f440a2a2571c)
```
