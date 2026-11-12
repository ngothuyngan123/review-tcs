# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thanh Duy Nguyen (assignee Redmine)` — journal ký `Dev Studio` |
| Commit / Pull Request | `8555b15d846996d320749558ead7540d1023496a` (round 3 — mới nhất) — xem thêm `cf9a3149438429016d80a5c6a973e6181036a9eb` (round 1), `f5ce5a0a2ca8fbc3802a58333ec14fdcf460909a` (round 2) |
| Branch | `ai_studio_fixbug_41801` (nhánh gốc `release-t09-2026@be6ef546aedb`), repo `linect-service` |
| Ngày submit đánh giá | `2026-10-27` (Journal #148915, round 3 — mới nhất) |
| Auto-filled | `2026-11-11 by /new-task` |

> ⚠️ Fix đã qua **3 vòng** — nội dung mục 1–4 dưới đây tổng hợp theo bản **mới nhất (round 3, Journal #148915)**, có chú thêm phần cộng dồn từ round 1–2 khi cần. Toàn văn cả 4 journal gốc xem ở `01-bug-task.md`.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Trong job import CSV, khối gắn/bỏ tag (kèm action) và khối friend info tuỳ chỉnh của `HandleImportCsvTask.readDataCSVV1` nằm **ngoài** điều kiện "user có conversation với bot import". Vì vậy user không phải bạn bè (không có conversation với bot đang import) vẫn bị gắn tag, ghi friend info và chạy action — action loại `compliant_status` / `bookmark` / `block` ném `NullPointerException` ở `ActionModel.doAction` vì không có `conversation` để lấy `getIdStatus()`.

`csvValidate` (bước validate mỗi row) trước fix chỉ kiểm `line_id` rỗng, và tìm `line_user` theo `line_id` **trên toàn hệ thống** (không giới hạn theo bot) — đây là lỗ hổng gốc cho phép non-friend lọt qua.

Bổ sung qua 3 vòng fix (đã khắc phục, không còn là vấn đề mở):
- Round 1: chặn sai khi 1 `line_id` có **nhiều bản ghi `line_user`** — chỉ kiểm bản ghi id nhỏ nhất, nên khi bạn bè thật là 1 bản ghi khác cùng `line_id` → bị bỏ qua sai (false positive "not friend").
- Round 2: sửa chọn đúng bản ghi `line_user` là bạn bè của bot import; thêm try/catch theo row (1 lỗi DB khi kiểm 1 row trước đây làm dừng toàn bộ các row sau).
- Round 3: thêm cảnh báo Chatwork **cấp file** khi có row bị bỏ do lỗi DB ở bước kiểm (gộp 1 tin/file, không gửi 1 tin/row).

## 2. Cách fix

- `csvValidate`: với mỗi row, sau khi tìm được (các) bản ghi `line_user` theo `line_id`, kiểm thêm tồn tại `conversation` (`bot_id` = account đang import, `tb_line_user_id` = line_user.id) qua method mới của `ConversationRepository`. Row **không có `line_user`** → bỏ qua, log `Row: N - line_user not found: line_id=...`. Row **có `line_user` nhưng không phải bạn bè của bot import** → bỏ qua toàn bộ (không cập nhật thông tin cơ bản, không gắn/bỏ tag + action, không ghi friend info + action, không ghi memo), log `Row: N - not friend of bot: botId=... - lineUserId=... - line_id=...`.
- Khi `line_id` trùng nhiều bản ghi `line_user`: chọn đúng bản ghi là bạn bè của bot import để ghi dữ liệu + chạy action; các bản ghi `line_user` khác (không phải bạn bè) giữ nguyên, không đụng.
- Lỗi DB khi kiểm 1 row: bắt riêng theo row (`validate exception: ...`), chỉ bỏ row đó, các row sau vẫn import tiếp, file vẫn chuyển trạng thái `完了済` (hoàn tất).
- (Round 3 — mới) Nếu file có ≥1 row bị bỏ do lỗi DB: cuối file ghi 1 dòng log ERROR tổng kết + gửi **đúng 1** tin Chatwork vào room exception (`448190376`): `[To:6395420]#readFileCSVV2 validate exception: csvId=... - botId=... - skipped rows=N/M - sample rows=[...] - first error=...` (tối đa 10 số row mẫu, `first error` tối đa 200 ký tự). Không gửi khi host là production `lme.watermeru.com` hoặc khi `ENABLE_NOTIFY_CHATWORK` tắt. Row bị bỏ vì lý do dữ liệu người dùng (line_id rỗng / not found / not friend) **không** tính vào cảnh báo này.
- Row hợp lệ (bạn bè thường, đã chặn bot, đang bị ẩn) — import như cũ: thông tin cơ bản (view_name, email, sinh nhật, trạng thái tin nhắn, 対応マーク), memo, tag + action, friend info + action.
- Script recover `docs/recovery/41801-recover.sql` (+ hướng dẫn `.md`, là **tài liệu task, không nằm trong repo code**): dọn `tag_line_user` / `friend_information_value` mà import CSV đã ghi sai cho non-friend, truy vết từ **2026-05-28** (có `tag_history`/`friend_info_history` trigger `19001`) tới khi bản sửa chạy production, giảm tương ứng `tags.count_user_tag` / `friend_information_setting.total_user_has_value`. Idempotent (điều kiện `NOT EXISTS conversation`), không tự `COMMIT` — người vận hành đối chiếu rồi `COMMIT`/`ROLLBACK` tay.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleImportCsvTask.csvValidate` (java-job) | Có — thêm kiểm `line_user` tồn tại + là bạn bè (conversation) của bot import, xử lý line_id trùng nhiều `line_user`, try/catch theo row | Root cause — bước validate gốc để lọt non-friend |
| 2 | `HandleImportCsvTask.readDataCSVV1` (java-job) | Có — chỉ ghi thông tin cơ bản/memo/tag+action/friend info+action vào đúng bản ghi `line_user` đã xác định là bạn bè | Khối tag + friend info trước đây nằm ngoài điều kiện check bạn bè |
| 3 | `HandleImportCsvTask.readFileCSVV2` (java-job) | Có (round 3) — tổng hợp số row bị bỏ do lỗi DB cuối file, ghi log ERROR + gọi Chatwork 1 lần/file | D-7: cảnh báo cấp file thay vì im lặng từng row |
| 4 | `ConversationRepository` (linedb) | Có — **thêm method mới** tra `conversation` theo `(bot_id, tb_line_user_id)`, dùng index `tb_line_user_id` sẵn có | Dev xác nhận: chỉ thêm method mới, **không sửa method cũ** → các nơi khác dùng repo không bị ảnh hưởng |
| 5 | `ActionModel.doAction` (loại `compliant_status` / `bookmark` / `block`) | **Không sửa trong ticket này** | Dev note: đây là lỗi cùng kiểu (không kiểm `conversation` null) ở luồng gọi khác — đề xuất ticket riêng. Với fix này, `ActionModel` không còn nhận được `conversation` null từ luồng import CSV (vì non-friend đã bị chặn ở `csvValidate`), nhưng bản thân hàm không có fix defensive |
| 6 | Export CSV (`CsvManagementController::csvExport`) | Không — Bug Studio #4000 không liên quan diff, do cấu hình môi trường test (`FOLDER_MEDIA` rỗng) | Dev confirm không phải bug của ticket |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandleImportCsvTask.csvValidate` | `src/main/java/sns/line/threads/csv/HandleImportCsvTask.java` | Direct | Root cause fix — kiểm non-friend + line_id trùng + try/catch theo row |
| F2 | `HandleImportCsvTask.readDataCSVV1` | cùng file trên | Direct | Ghi tag/friend info/action/memo vào đúng bản ghi `line_user` là bạn bè |
| F3 | `HandleImportCsvTask.readFileCSVV2` | cùng file trên | Direct | Mới (round 3): tổng hợp + gửi Chatwork cấp file khi có row lỗi DB |
| F4 | `ConversationRepository` (method mới tra theo bot + line_user) | `.../linedb/repository/ConversationRepository.java` | Direct (method mới) | Không sửa method cũ — các caller khác của repo không đổi hành vi |
| F5 | `ActionModel.doAction` (compliant_status / bookmark / block) | (không trong diff) | Indirect | Hết nhận `conversation = null` từ luồng CSV sau fix, nhưng hàm chưa có defensive check — rủi ro tồn dư ở luồng gọi khác (ngoài phạm vi ticket) |
| F6 | `HandleImportCsvManager` (entry point job) | (không trong diff) | Indirect | Gọi `readFileCSVV2` → nhận toàn bộ hành vi mới qua chuỗi gọi, không đổi chữ ký |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `tag_line_user` + `tag_history` (trigger `19001`) | UPDATE (hành vi ghi — thu hẹp, chỉ ghi khi là bạn bè) | Trước fix: bị ghi sai cho non-friend |
| D2 | `friend_information_value` + `friend_info_history` (trigger `19001`) | UPDATE (hành vi ghi — thu hẹp) | Trước fix: bị ghi sai cho non-friend |
| D3 | `tags.count_user_tag` | UPDATE (counter) | Không còn tăng do non-friend |
| D4 | `friend_information_setting.total_user_has_value` | UPDATE (counter) | Không còn tăng do non-friend |
| D5 | `tag_line_user` / `friend_information_value` dữ liệu **production** đã ghi sai (từ `release-t3-2024` 03/2024, truy vết được từ 2026-05-28) | DELETE (ngoài code fix — chạy tay qua `docs/recovery/41801-recover.sql`, **không có trong repo**) | **Cần Recover data** — xem "Migration" + "Ghi chú thêm của Leader" ở file 01. Không tự COMMIT, idempotent, chỉ xoá qua điều kiện `NOT EXISTS conversation` |
| D6 | Message Chatwork room exception (`448190376`) | CREATE (external call, không phải DB) | Mới ở round 3 — tối đa 1 tin/file; tắt khi host production `lme.watermeru.com` hoặc `ENABLE_NOTIFY_CHATWORK=0` |
| D7 | `event_step_time` (từ friend info dạng ngày, qua `EventModel.csvSettingActionFriendInfoDate`) | Chưa xác định — **chưa kiểm chứng** | Dev nêu rõ: script recover **không** dọn phần lịch event này nếu đã tạo sai cho non-friend trước fix |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Import CSV (`SCR-CSV-01 CSV管理` tab `インポート`) — toàn luồng `HandleImportCsvManager → readFileCSVV2 → csvValidate → readDataCSVV1` | F1, F2, F3, F6 | High |
| T2 | Tag management — gắn/bỏ tag qua import CSV + action tag + bộ đếm `count_user_tag` | F1, F2, D1, D3 | High |
| T3 | Friend info management — ghi friend info tuỳ chỉnh qua import CSV + action friend info + bộ đếm `total_user_has_value` | F1, F2, D2, D4 | High |
| T4 | Action loại `compliant_status` / `bookmark` / `block` kích hoạt từ CSV (tag/friend info) | F1, F2, F5 | High (root cause NPE) — regression quan trọng nhất cần verify |
| T5 | Chatwork notify room exception khi job import lỗi DB | F3, D6 | Medium — mới, cần kiểm cả case KHÔNG gửi (host production, `ENABLE_NOTIFY_CHATWORK=0`) |
| T6 | Recover data production (tag/friend info ghi sai cho non-friend) | D5 | High — rủi ro vận hành (script xoá dữ liệu thật, không rollback được) nhưng **nằm ngoài code fix**, do người vận hành chạy tay |
| T7 | Lịch action theo friend info dạng ngày (`event_step_time`) đã tạo sai cho non-friend trước fix | D7 | Medium — Dev xác nhận **chưa kiểm chứng**, không nằm trong script recover |
| T8 | Hiệu năng job import CSV (file lớn) | F1 (thêm 1-2 query/row có index) | Low |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
