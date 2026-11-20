# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Văn Đức Nguyễn (`assigned_to` Redmine) — phân tích chi tiết do "Dev Studio" ghi trong journal |
| Commit / Pull Request | Chưa có link PR; base `origin/release-backend-mcp-api-v2-202610@a4d03ccd5f88`, commit nhánh fix `bd7e7cae4b1f1374e4f6384ba881f440a2a2571c` (linect-service), file đổi: `src/main/java/sns/line/models/McpModel.java` (1 dòng) |
| Branch | `ai_studio_fixbug_45812` |
| Ngày submit đánh giá | 2026-11-12 (Journal #154183, "Dev handoff — 12/11 11:29") |
| Auto-filled | 2026-11-12 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

`McpModel.requestDoAction` tạo action chain tạm với `update_timestamp = System.currentTimeMillis()` (**mili-giây**), trái quy ước **giây** của `t_actions.update_timestamp`. `ActionModel.doAction` đọc lại giá trị đó rồi truyền vào `HistoryHelper.captureMultiAction` để INSERT `action_multi_capture.timestamp`. Ở môi trường lỗi, cột này khi đó là `INT` nên giá trị khoảng 1,7×10¹² bị tràn và gây `DataException`. Lỗi bị nuốt (catch/log, không throw lên) nên `action_multi_capture_id` trong lịch sử thành `NULL`.

## 2. Cách fix

- **D-1**: Đổi mốc thời gian của action tạm trong `do_action` sang giây.
- Code: `McpModel.java:384` → `long now = System.currentTimeMillis() / 1000;`
- Nội dung thay đổi: Public API `/v1/do_action` (module callback) — action áp lên friend giờ có bản chụp action, và lịch sử thao tác (gắn tag, đổi thông tin friend…) liên kết tới bản chụp đó; hết lỗi `#captureMultiAction error ... DataException`.
- Diff: 1 file changed, 1 insertion(+), 1 deletion(-) (`McpModel.java`).
- Migration / thay đổi dữ liệu: **không có** (Dev đã kiểm diff).
- Recover dữ liệu: **Không cần recover** — DucNV quyết định ngày 2026-11-12. Lỗi chỉ làm mất liên kết capture trong lịch sử do_action, action vẫn áp đúng cho friend (data nghiệp vụ không sai).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

Dev không ghi bảng caller riêng, nhưng xác nhận rõ scope bị/không bị chạm:

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ActionModel.doAction` (đọc `t_actions.update_timestamp` từ chuỗi tạm `do_action`) + `HistoryHelper.captureMultiAction` (INSERT `action_multi_capture`) | Không đổi code, nhưng input (timestamp) giờ là giây | Đi qua `requestDoAction` nên nhận trực tiếp giá trị đã fix |
| 2 | `MessageModel.getVersionId` (version id khi `do_action` gửi tin text/template) | Không đổi code, nhưng input giờ là giây → version id ngắn lại, tránh tràn `Long` khi nối `id + timestamp` | Cùng đường dữ liệu `update_timestamp` của chuỗi tạm |
| 3 | `ActionModel.doAction` (dòng 136) + `HandlePostbackTask` (dòng 4247/4248) | **KHÔNG sửa** — vẫn fallback `currentTimeMillis()` khi không tìm thấy `t_actions` | Dev xác nhận cùng loại lỗi nhưng **lối vào khác, ngoài phạm vi ticket này** — không nên tính vào coverage của task |
| 4 | Broadcast / kịch bản / postback / web (`HelperService.sendAction` → worker Java → `ActionModel.doAction`) | **Không đi qua `requestDoAction`** | Dev khẳng định các luồng action khác không bị ảnh hưởng bởi fix này — nên đưa vào TC regression đối chứng, không phải TC verify fix |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `McpModel.requestDoAction` | `McpModel.java:384` | Direct | Đổi đơn vị mốc thời gian tạo action tạm cho `do_action`: ms → giây |
| F2 | `ActionModel.doAction` + `HistoryHelper.captureMultiAction` | `ActionModel.java:700-787`, `HistoryHelper.java:35-55` | Indirect | Đọc lại `t_actions.update_timestamp` (giờ là giây) để INSERT `action_multi_capture.timestamp`; capture id truyền xuống `tag_history`/`friend_info_history`/`line_user_add_friend_history` (trước fix NULL do lỗi bị nuốt) |
| F3 | `MessageModel.getVersionId` | — | Indirect | Dùng cho action gửi tin text/template trong `do_action`; version id tính theo giây — tránh `NumberFormatException`/tràn `Long` khi nối `id + timestamp` 13 chữ số cũ |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `t_actions`, `t_actions_detail` (chuỗi action tạm của `do_action`, bị xoá sau request — xem `McpModel.java:440-447`) | UPDATE (đơn vị timestamp) | Action tạm, tồn tại rất ngắn trong 1 request, không migrate dữ liệu cũ |
| D2 | `action_multi_capture.timestamp` + cột `action_multi_capture_id` ở các bảng lịch sử (`tag_history`, `friend_info_history`, `line_user_add_friend_history`...) | CREATE (bản chụp mới) | Trước fix: `NULL` do lỗi bị nuốt. Sau fix: có giá trị hợp lệ (10 chữ số, đơn vị giây) |
| D3 (⚠️ ngoài diff, chỉ để tham khảo risk schema) | `action_multi_capture.timestamp` — migration web khai kiểu `INT` | — không đổi trong ticket này | Dev cảnh báo: giây vẫn vừa `INT` (tới năm 2038); web ghi `action_id nối update_timestamp` đã **vượt INT từ trước** (ngoài phạm vi fix) — field này cần là `BIGINT` ở mọi môi trường nhưng migration hiện vẫn khai `INT` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Public API `POST /v1/do_action` (module callback) | F1, F2, F3, D1 | Low (Dev tự đánh giá) — chỉ đổi đơn vị 1 giá trị, không đổi request/response/schema/validation/HMAC |
| T2 | Màn lịch sử thao tác friend trên web (`友だち追加履歴`, `タグ履歴`, `友だち情報追加履歴` — nút `プレビュー` / tab `アクション`) cho các dòng sinh từ `do_action` | F2, D2 | Medium — hiển thị bị ảnh hưởng gián tiếp qua `action_multi_capture_id`; cần verify cả dòng lịch sử **cũ** (capture NULL, ghi trước fix) vẫn hiển thị bình thường (không recover) |
| T3 | Các luồng action KHÔNG qua `do_action` (broadcast / kịch bản / postback / `友だち一括アクション` trên web) | Caller #4 ở mục 3 | Low — Dev khẳng định không chạm, nên chỉ cần 1 TC regression đối chứng (không phải verify fix) |

---

## Ghi chú khác (ngoài 4 mục chuẩn — scope loại trừ của Dev)

Các điểm này **Dev xác nhận KHÔNG thuộc phạm vi ticket #45812** — không cần viết TC coverage cho các mục này trong task này:
- `ActionModel.java:136` và `HandlePostbackTask.java:4247`/`4248` còn fallback mili-giây khi không tìm thấy `t_actions` (cùng loại lỗi, lối vào khác) — Dev đề xuất mở ticket riêng.
- `action_multi_capture.timestamp` do **web** ghi (`action_id nối update_timestamp`) đã vượt `INT` sẵn, không liên quan request `do_action` — vấn đề schema (`INT` nên là `BIGINT`), chưa có migration.
- Nhánh release khác `release-backend-mcp-api-202609` còn dòng lỗi tương tự — vấn đề vận hành/release, không phải TC.
- `build.gradle` thiếu dependency `converter-jackson` — vấn đề build/CI, không liên quan logic bug.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
