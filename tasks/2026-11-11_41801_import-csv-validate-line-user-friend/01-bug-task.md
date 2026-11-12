# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41801 — [JOB][ImportCsv] Import CSV cần validate line_user có phải bạn bè của account (bot) đang import hay không` |
| Module / Màn hình | `SCR-CSV-01 CSV管理 — tab インポート (Import CSV) → job nền HandleImportCsvTask (readFileCSVV2 / readDataCSVV1 / csvValidate)` |

## Mô tả bug (bản dịch tiếng Việt)

■ Hiện trạng / Bug

Import CSV tìm line_user theo line_id trên toàn hệ thống, không check user có phải bạn bè (bạn bè = có conversation) của account (bot) đang import hay không.
- Nếu CSV chứa line_id của user chỉ kết bạn với account khác, job vẫn gắn tag và chạy action của tag cho user đó.
- Action có type cần conversation (compliant_status / bookmark / block) bị NullPointerException (NPE).
- Case thực tế 2026-10-23 11:17: csv_filter_upload_history id=79045, bot 219704, line_id `Ud59a152addd53bea2eb10aff7e0d4882` (line_user 59128955). User này chỉ có conversation với bot 215086, 218683 → NPE ở action 21667493 (action detail 24273317, loại compliant_status), và tag 2554449 của bot 219704 bị gắn cho user không phải bạn bè.

■ Spec sửa (yêu cầu gốc từ người báo bug)
- Khi validate từng row CSV (`csvValidate`), bỏ qua row nếu:
  1. line_id rỗng (đã có)
  2. Không tồn tại line_user với line_id này
  3. Không tồn tại conversation (bot_id = account import, tb_line_user_id = line_user.id) → không phải bạn bè của account
- Row bị bỏ qua: không cập nhật thông tin bạn bè, không gắn tag, không chạy action, không ghi memo. Chỉ log lỗi kèm số row và lý do.
- Các row hợp lệ khác vẫn import bình thường.

## Steps to reproduce

<!-- Redmine không ghi khối "Steps to reproduce" tách riêng — tái hiện qua ca lỗi thực tế ở mục "Mô tả bug" + "Dữ liệu định danh ca lỗi" bên dưới. -->

1. Chuẩn bị CSV import chứa `line_id` của 1 user **chỉ là bạn bè (có conversation) của bot khác**, không phải bạn bè của bot đang import.
2. Bật 1 tag có cấu hình action loại `compliant_status` / `bookmark` / `block` cho cột tag trong CSV, cấu hình thêm 1 cột friend info tuỳ chỉnh có action.
3. Import CSV vào bot đang thao tác (không phải bot mà user này là bạn bè).

## Expected result

- Row của user không phải bạn bè của bot import: bị bỏ qua hoàn toàn — không gắn tag, không chạy action, không ghi friend info, không ghi memo, không NPE/Chatwork exception. Log ghi rõ số row + lý do "not friend of bot".
- Row hợp lệ khác trong cùng file (kể cả bạn bè đã chặn bot) vẫn import như bình thường.

## Actual result

- User không phải bạn bè của bot import vẫn bị gắn tag + chạy action của tag.
- Action loại `compliant_status` (cần conversation) ném NullPointerException do `conversation.getIdStatus()` gọi trên `null` (không có conversation).
- Tag của bot đang import bị gắn sai cho user không phải bạn bè → sai cả `tags.count_user_tag`.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

Log exception gốc (server `step.lme.jp`):
```
Class: ActionModel
Message: #doAction-> exception -> 21394511 -> action id detail: 23756769 to userId: U98e00193ccd1ab051d0a99319b860cd2 with bot:219703
Exception: null
Line user id: 60910785,61495377,50324744,61424496
Time: 2026-09-30 17:24:12
Log: import csv
```
(Redmine `Attachments: 0` — không có file đính kèm.)

## Ghi chú thêm của Leader

- Bug không có "Steps to reproduce" tường minh trong Redmine — root cause + điểm cần test đã được Dev xác nhận rất chi tiết qua 4 journal handoff (xem file `03-dev-impact.md` + journal nguyên văn bên dưới). TCs nên bám theo các "Điểm cần test" Dev đã nêu ở mỗi vòng fix.
- Đây là **task JOB nền** (`HandleImportCsvTask`, chạy từ `HandleImportCsvManager`), kích hoạt từ màn `SCR-CSV-01 CSV管理 → tab インポート` nhưng xử lý thực tế ở job Java, không phải request đồng bộ trên web.
- Fix đã qua **3 vòng** (round 1 → round 3, nhánh `ai_studio_fixbug_41801`): vòng 1 chặn sai khi 1 `line_id` có nhiều bản ghi `line_user` (chọn nhầm bản ghi); vòng 2 sửa chọn đúng bản ghi là bạn bè + thêm try/catch theo row; vòng 3 (mới nhất, 2026-10-27) thêm cảnh báo Chatwork cấp-file khi có lỗi DB ở bước kiểm. **Bản mới nhất = commit `8555b15d846996d320749558ead7540d1023496a`** trên branch `ai_studio_fixbug_41801` (gốc `release-t09-2026@be6ef546aedb`).
- **Cần Recover data production** (xem mục Migration ở file 03): script `docs/recovery/41801-recover.sql` (+ hướng dẫn `.md`, là tài liệu task — không có trong repo code) dọn `tag_line_user` / `friend_information_value` mà import CSV đã ghi sai cho non-friend, truy vết được từ **2026-05-28** (có history trigger 19001) tới khi bản sửa chạy production. Dữ liệu sai trước 2026-05-28 không truy vết được, không xử lý trong ticket này. Action đã chạy cho non-friend (tin, kịch bản, đổi trạng thái, tag do action gắn) **không hoàn tác được**.
- Đã có task trên **MCP LME TEST STUDIO** (task_id `511`, round 1, `aiResult=fail`) với 18 TC do AI sinh — xem `04-tc-list.md`. 2 TC đang `error`/`fail` (NEW-8, NEW-11) + 2 TC `skip` (NEW-9, NEW-10 — script recover). Dev đã note ở journal #148730: TC `NEW-11` (bug #4003 Studio) nên **đổi hướng kiểm** (từ kỳ vọng "0 line_id trùng" sang "import ghi đúng bản ghi bạn bè"); journal #148915: TC `TC33330`/`NEW-8` cần cập nhật theo hành vi vòng 3 (gom 1 dòng log + 1 Chatwork cấp-file).
- Toàn bộ 18 TC trên Studio chỉ chạy ở env **`local`** — theo RULE-08, chưa có kết luận nào về production cho phần job nền / Chatwork notify thật.
- `ENABLE_NOTIFY_CHATWORK=0` ở local — TC phải kiểm qua dòng log, không gọi Chatwork thật (room exception `448190376`, template `[To:6395420]#readFileCSVV2 validate exception: ...`).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `219704` (case gây bug) — các case điều tra/test khác còn có `219703`, `215086`, `218683` |
| Friend | `line_id Ud59a152addd53bea2eb10aff7e0d4882` → `line_user 59128955` (không phải bạn bè của bot 219704 — chỉ có conversation với bot 215086, 218683) |
| Đối tượng cấu hình | `csv_filter_upload_history id=79045` · tag `2554449` (bot 219704) · action `21667493` (action detail `24273317`, loại `compliant_status`) |
| Thời điểm lỗi | `2026-10-23 11:17` (case ghi trong bug) · log exception gốc `2026-09-30 17:24:12` (server step.lme.jp) |
| Đối chứng | Bạn bè hợp lệ của bot import (kể cả đã chặn bot) vẫn phải import bình thường — dùng làm case regression đối chứng |

## Journal / note từ Redmine (nguyên văn)

**Journal #147631 — Dev Studio — 2026-10-23:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Trong `HandleImportCsvTask.readDataCSVV1`, chỉ phần thông tin cơ bản và memo nằm trong khối `if (conversationSetting != null)`; khối gắn/bỏ tag (kèm action của tag) và khối friend info tuỳ chỉnh (kèm action) nằm ngoài khối này. `csvValidate` chỉ kiểm line_id rỗng và line_user được tìm theo line_id trên toàn hệ thống, nên user chỉ kết bạn với bot khác vẫn bị gắn tag, ghi friend info và chạy action. Với action loại compliant_status/bookmark/block, `ActionModel.doAction` không có conversation nên `conversation.getIdStatus()` ném NullPointerException.

Hướng sửa:
- D-1 csvValidate bỏ qua row không có line_user hoặc không phải bạn bè của bot import
- D-2 Script SQL recover dữ liệu tag/friend info đã ghi cho non-friend

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng luồng import CSV của job (HandleImportCsvTask, csvValidate có một caller); row không phải bạn bè bị bỏ qua hoàn toàn, row hợp lệ (kể cả user đã chặn bot) xử lý như cũ. Mỗi row thêm 2 query có index; script recover xoá dữ liệu production nên phải chạy chế độ đếm và đối chiếu trước.
```

**Journal #147640 — Dev Studio — 2026-10-23 (round 1, branch `ai_studio_fixbug_41801` @ `cf9a3149438429016d80a5c6a973e6181036a9eb`):**

```
Dev handoff — 23/10 14:51 · nhánh ai_studio_fixbug_41801

Nguyên nhân:
Trong `HandleImportCsvTask.readDataCSVV1`, chỉ phần thông tin cơ bản và memo nằm trong khối `if (conversationSetting != null)`; khối gắn/bỏ tag (kèm action của tag) và khối friend info tuỳ chỉnh (kèm action) nằm ngoài khối này. `csvValidate` chỉ kiểm line_id rỗng và line_user được tìm theo line_id trên toàn hệ thống, nên user chỉ kết bạn với bot khác vẫn bị gắn tag, ghi friend info và chạy action. Với action loại compliant_status/bookmark/block, `ActionModel.doAction` không có conversation nên `conversation.getIdStatus()` ném NullPointerException.

Nội dung thay đổi:
- Job import CSV người dùng (HandleImportCsv): row có line_id không tồn tại trong hệ thống bị bỏ qua, log 'Row: N - line_user not found: line_id=...'.
- Job import CSV: row của user không có conversation với account đang import (chỉ là bạn bè của account khác) bị bỏ qua toàn bộ (thông tin cơ bản, tag và action tag, friend info và action, memo), log 'Row: N - not friend of bot: botId=... - lineUserId=... - line_id=...'.
- Row hợp lệ (kể cả user đã chặn account) import như trước; row lỗi không làm dừng các row khác.
- Script recover docs/recovery/41801-recover.sql (kèm hướng dẫn .md, là tài liệu task, không nằm trong repo): dọn tag và friend info mà import CSV đã ghi cho non-friend từ 2026-05-28.

File đã sửa (java-job):
  src/main/java/sns/line/threads/csv/HandleImportCsvTask.java | 12 ++++++++++++
  1 file changed, 12 insertions(+)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ thêm 12 dòng vào hàm validate có 1 caller và chỉ làm hẹp phạm vi ghi dữ liệu. Đã compile và chạy harness có kiểm chứng ngược; chưa verify runtime với DB thật.
- Toàn bộ luồng import CSV của job (HandleImportCsvManager → HandleImportCsvTask.readFileCSVV2): mọi row đều đi qua bước kiểm mới, nên thông tin cơ bản, memo, tag, friend info của bạn bè phải cập nhật như cũ.
- Action tag và action friend info do CSV kích hoạt: từ nay chỉ chạy cho bạn bè của account import.
- Bộ đếm tags.count_user_tag và friend_information_setting.total_user_has_value: không còn tăng do non-friend.
- Hiệu năng job import CSV: mỗi row thêm 2 query có index (line_user theo line_id, conversation theo bot và line_user), file lớn chạy lâu hơn một chút.
- Lỗi DB thoáng qua lúc kiểm một row sẽ dừng phần còn lại của file (có báo Chatwork); trước đây chỉ mất 1 row.

Migration / thay đổi dữ liệu:
- [Recover · Sau deploy] Dọn tag_line_user và friend_information_value mà import CSV đã ghi cho user không phải bạn bè của bot import (truy theo history trigger 19001 từ 2026-05-28), và giảm tags.count_user_tag, friend_information_setting.total_user_has_value tương ứng (module job): Chạy trên linedb production theo docs/recovery/41801-recover.md (script docs/recovery/41801-recover.sql trong tài liệu task, không có trong repo). Bước 1: đặt @bot_id (NULL = mọi bot), chạy PHẦN 1 (chỉ đọc) và lưu kết quả ra CSV. Bước 2: chạy PHẦN 2 trong cùng session; script mở transaction và không … — không rollback được, backup: Trước khi COMMIT: lưu kết quả PHẦN 1; mysqldump các row tag_line_user và friend_information_value theo id liệt kê ở PHẦN 1, và các row tags, friend_information_setting liên quan (để khôi phục bộ đếm).

Recover dữ liệu: Cần recover — Bug đã ghi dữ liệu sai cho user không phải bạn bè: gắn tag, ghi friend info và tăng bộ đếm. Nếu để nguyên, khi user kết bạn về sau sẽ có sẵn tag/friend info sai.
- Ảnh hưởng: tag_line_user của bot import gắn cho user không có conversation với bot (kèm tag_history trigger 19001, tags.count_user_tag bị tăng)
- Ảnh hưởng: friend_information_value của bot import ghi cho non-friend (kèm friend_info_history trigger 19001, friend_information_setting.total_user_has_value bị tăng)
- Ảnh hưởng: Action của tag/friend info đã chạy cho non-friend (một phần NPE); phần đã chạy không hoàn tác được
- Khoảng thời gian: Từ release-t3-2024 (03/2024, commit job import csv) tới khi bản sửa chạy; chỉ truy vết chắc chắn từ 2026-05-28 (commit ghi history trigger CSV 19001)
- Cách recover: Script SQL docs/recovery/41801-recover.sql (mục D-2): phần đếm chỉ SELECT; phần dọn trong transaction xoá tag_line_user và friend_information_value truy được qua history trigger 19001 mà user không có conversation với bot, giảm count_user_tag / total_user_has_value tương ứng. Idempotent nhờ điều kiện NOT EXISTS conversation và row còn tồn tại; không ghi history, không chạy action. Người vận hành chạy chế độ đếm trước rồi mới dọn.
- Ảnh hưởng tới khách: User không phải bạn bè không hiện trong danh sách bạn bè của bot nên dọn không đổi màn khách đang thấy; chỉ bộ đếm tag/friend info giảm về đúng. Action đã chạy không hoàn tác.

Việc cần người làm thêm (ngoài phạm vi task):
- Người vận hành chạy phần đếm của script docs/recovery/41801-recover.sql trên production, đối chiếu kết quả rồi quyết định chạy phần dọn.
- Dữ liệu import trước 2026-05-28 không có history trigger CSV nên không truy được; nếu cần dọn phải xử lý riêng.
- Cập nhật spec admin/csv-management/job/job-spec.md mục 0.3: job import Java hiện đang chạy theo cờ ENABLE_HANDLE_IMPORT_CSV, không còn là dead code.
- ActionModel bookmark/block/compliant_status không kiểm conversation null: đây là lỗi cùng kiểu ở luồng gọi khác, đề xuất ticket riêng nếu cần.
- Kiểm thêm (chưa kiểm chứng): friend info dạng ngày ghi qua CSV cho user không phải bạn bè có thể đã tạo lịch action (event_step_time) qua EventModel.csvSettingActionFriendInfoDate; script không dọn phần này.
- Action đã chạy cho non-friend (tin, kịch bản, đổi trạng thái, tag do action gắn) và lịch event_step_time từ friend info dạng ngày không hoàn tác được bằng script; cần người quyết có xử lý tay hay báo khách hàng bị ảnh hưởng.
- Dữ liệu sai do import CSV trước 2026-05-28 không truy vết được qua history; không xử lý trong ticket này.

Điểm cần test:
- CSV có line_id của user chỉ kết bạn bot khác, tag = 1, bật action tag loại compliant_status: không gắn tag, không chạy action, không NPE/Chatwork, log 'Row: N - not friend of bot'
- Cùng user với cột friend info tuỳ chỉnh có giá trị và bật action friend info: không ghi friend_information_value/history, không chạy action; memo, view_name, status message không đổi
- line_id không có trong line_user: log 'line_user not found', các row khác vẫn import
- line_id rỗng: log message cũ
- CSV trộn: row bạn bè hợp lệ (kể cả user đã chặn bot) vẫn cập nhật thông tin, tag + action, friend info, memo như trước
- Tag = 0 cho non-friend: không bỏ tag, không ghi history
- Script recover: chạy phần đếm trên DB test có dữ liệu mẫu; chạy dọn 2 lần, lần 2 ảnh hưởng 0 row; bạn bè hợp lệ không bị đụng
- Bộ đếm số người của tag và của friend info không tăng do non-friend.

Branch: ai_studio_fixbug_41801
- linect-service: ai_studio_fixbug_41801 (nhánh gốc release-t09-2026 @be6ef546aedb, commit cf9a3149438429016d80a5c6a973e6181036a9eb)
```

**Journal #148730 — Dev Studio — 2026-10-26 (round 2, branch `ai_studio_fixbug_41801` @ `f5ce5a0a2ca8fbc3802a58333ec14fdcf460909a`):**

```
Dev handoff — 26/10 15:26 · nhánh ai_studio_fixbug_41801

Nguyên nhân:
Nguyên nhân gốc giữ như bản 1: khối tag và friend info tuỳ chỉnh của job import CSV chạy cả cho user không phải bạn bè của bot. Bản sửa vòng 1 kiểm bạn bè bằng chỉ một bản ghi line_user (bản ghi id nhỏ nhất của line_id). Vì vậy khi bạn bè của bot là một bản ghi khác cùng line_id thì row bị bỏ qua sai. Ngoài ra readDataCSVV1 tự tra lại line_user, nên ghi nhầm bản ghi và số lần tra line_id tăng gấp đôi. Thêm nữa, các truy vấn ở bước kiểm không có try/catch theo row, nên một lỗi DB làm dừng cả các row sau.

Nội dung thay đổi:
- Job import CSV (HandleImportCsv): row có line_id không tồn tại bị bỏ qua, log 'Row: N - line_user not found: line_id=…'.
- Job import CSV: row của user không có conversation với account đang import bị bỏ qua toàn bộ (thông tin cơ bản, tag + action, friend info + action, memo), log 'Row: N - not friend of bot: botId=… - lineUserId=… - line_id=…'.
- Job import CSV: line_id có nhiều bản ghi line_user thì thông tin cơ bản, tag, friend info, memo và action ghi vào bản ghi là bạn bè của account import; các bản ghi khác không đổi.
- Job import CSV: lỗi DB khi kiểm một row chỉ bỏ row đó (log 'validate exception: …'), các row sau vẫn import.
- Script recover docs/recovery/41801-recover.sql kèm hướng dẫn: dọn tag và friend info do CSV đã ghi cho non-friend từ 2026-05-28; câu đếm PHẦN 1 nay khớp với số dòng sẽ xoá.

Bug automation Test Studio:
- Bug #4000 không phải bug: Lỗi ở bước tải CSV xuất (tab エクスポート): FOLDER_MEDIA rỗng trong môi trường test làm web CsvManagementController::csvExport lỗi 'Undefined offset: 4'. Luồng xuất CSV không nằm trong diff của ticket, nên đây là lỗi cấu hình môi trường test.
- Bug #4001 không phải bug: Helper chờ AJAX của tab タグ trong khi chưa bấm tab (ảnh đang ở 基本情報). Snapshot DB sau import đúng mọi mong đợi (tag T7 + history 19001, action, friend info B, memo, bộ đếm 3), nên đây là lỗi kịch bản test.
- Bug #4002 để sau: Đúng là line_user.line_id không có index, nhưng có từ trước ticket và schema do web/DBA quản lý. Commit f5ce5a0a2 đã đưa số lần tra line_id mỗi row về 1 như trước ticket; tra conversation theo (bot, line_user) đã dùng index tb_line_user_id. Việc thêm index chuyển cho DBA xác nhận trên production.
- Bug #4003 không phải bug: 18 line_id trùng là dữ liệu nền có sẵn (khớp DB điều tra, không do import tạo ra). Rủi ro chọn sai user mà bug nêu đã được xử lý ở f5ce5a0a2: job ghi vào bản ghi là bạn bè của account import. Nên đổi testcase sang kiểm import ghi đúng bản ghi bạn bè thay vì kỳ vọng 0 dòng trùng.

File đã sửa (java-job):
  .../linedb/repository/ConversationRepository.java  |  3 ++
  .../sns/line/threads/csv/HandleImportCsvTask.java  | 59 ++++++++++++++++++----
  2 files changed, 51 insertions(+), 11 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đổi 2 hàm private có 1 caller và thêm 1 method repository mới. Thay đổi chỉ thu hẹp phạm vi ghi và chọn đúng bản ghi bạn bè; harness pass trên HEAD và fail trên base. Chưa verify runtime với DB thật.
- Toàn bộ luồng import CSV của job (HandleImportCsvManager → readFileCSVV2 → csvValidate → readDataCSVV1): bạn bè thường, đã chặn, đang ẩn phải import như trước (view_name, email, sinh nhật, trạng thái tin nhắn, 対応マーク, memo, tag, friend info).
- Action tag và action friend info do CSV kích hoạt: chỉ chạy cho bạn bè, trên đúng bản ghi line_user (ActionModel nhận object line_user đã xác định).
- Bộ đếm tags.count_user_tag và friend_information_setting.total_user_has_value: không còn tăng do non-friend.
- ConversationRepository chỉ thêm method mới, không sửa method cũ: các nơi khác dùng repo không bị ảnh hưởng.
- Hiệu năng job import: row hợp lệ vẫn tra line_id 1 lần như trước ticket; row non-friend thêm 1 truy vấn nối conversation với line_user (phụ thuộc index line_user.line_id trên production).

Migration / thay đổi dữ liệu:
- [Recover · Sau deploy] Dọn tag_line_user / friend_information_value do import CSV ghi cho user không phải bạn bè của bot import (truy qua history trigger 19001, từ 2026-05-28), giảm count_user_tag / total_user_has_value — docs/recovery/41801-recover.sql: Trên linedb production, ngoài giờ cao điểm: đặt @bot_id (NULL = mọi bot), chạy PHẦN 1 (chỉ đọc) và lưu kết quả; trong cùng session chạy PHẦN 2 (script mở transaction, không tự COMMIT); đối chiếu 1a' = tag_line_user_to_delete, số row 1b = friend_information_value_to_delete, kết quả 2.6 bằng 0 thì gõ … — không rollback được, backup: Lưu kết quả PHẦN 1 (CSV); mysqldump các row tag_line_user và friend_information_value theo id liệt kê ở PHẦN 1, cùng các row tags và friend_information_setting liên quan, trước khi COMMIT.

Recover dữ liệu: Cần recover — Giữ như bản 1: dữ liệu import CSV đã ghi tag/friend info cho user không phải bạn bè cần dọn bằng script recover. Bản 2 chỉ sửa câu đếm 1a để số liệu đối chiếu khớp.
- Ảnh hưởng: tag_line_user và tags.count_user_tag do CSV gắn cho user không phải bạn bè (truy qua tag_history trigger 19001)
- Ảnh hưởng: friend_information_value và total_user_has_value do CSV ghi cho user không phải bạn bè (truy qua friend_info_history trigger 19001)
- Khoảng thời gian: Từ 2026-05-28 (có history trigger 19001) tới khi bản sửa chạy production; dữ liệu cũ hơn không phân biệt được
- Cách recover: docs/recovery/41801-recover.sql: chạy PHẦN 1 (đếm) → đối chiếu → PHẦN 2 dọn trong transaction, COMMIT/ROLLBACK tay; idempotent. Bản 2 sửa câu 1a gom theo tag_line_user và thêm COUNT DISTINCT để so với bảng tạm.
- Ảnh hưởng tới khách: Không gửi bù; action đã chạy (tin, kịch bản) không hoàn tác. Bạn bè thật trước đây không được cập nhật do line_id trùng thì khách import lại CSV.

Việc cần người làm thêm (ngoài phạm vi task):
- DBA xác nhận production có index trên line_user.line_id; nếu chưa có thì đề xuất thêm qua migration của web. Việc này ngoài ticket.
- Môi trường test local của Test Studio: cấu hình FOLDER_MEDIA cho job để tải được CSV xuất (#4000), và sửa helper bấm tab タグ trước khi chờ AJAX (#4001).
- Dữ liệu line_user trùng line_id (18 line_id trên DB test, có line_id lặp 217.450 lần) là dữ liệu nền: leader quyết định có dọn hay không.
- Nếu muốn, sau này có thể gom một tin Chatwork mỗi file cho các row bị lỗi DB ở bước kiểm. Theo thiết kế D-5 hiện chỉ ghi log, không gửi Chatwork.
- Test Studio sửa môi trường (FOLDER_MEDIA) cho #4000, helper chờ tab タグ cho #4001, và testcase NEW-11 (#4003) chuyển sang kiểm import ghi đúng bản ghi bạn bè thay vì kỳ vọng 0 line_id trùng.

Điểm cần test:
- line_id có 2 bản ghi line_user, chỉ bản ghi id lớn hơn là bạn bè của bot import: tag, friend info, memo, thông tin cơ bản ghi vào bản ghi id lớn; bản ghi id nhỏ không đổi; log không có 'not friend of bot'.
- line_id trùng nhưng không bản ghi nào là bạn bè của bot import: row bị bỏ qua, log 'Row: N - not friend of bot: …'.
- CSV trộn bạn bè và user chỉ là bạn bè của bot khác, tag có action compliant_status / bookmark / block: bạn bè được gắn tag và chạy action; non-friend không bị gắn tag, không có Chatwork '#doAction-> exception'.
- Bạn bè thường, đã chặn bot, đang bị ẩn: tag + action, friend info + action, thông tin cơ bản, memo import như trước; count_user_tag và total_user_has_value tăng đúng số bạn bè.
- line_id không tồn tại và line_id rỗng: row bị bỏ qua, các row khác vẫn import, file chuyển 完了済.
- Script recover: dữ liệu có 2 tag_history ADD (trigger 19001) cho cùng một tag_line_user của non-friend thì câu 1a ra 1 dòng, 1a' bằng tag_line_user_to_delete; chạy lại cả script thì 0 row.

Branch: ai_studio_fixbug_41801
- linect-service: ai_studio_fixbug_41801 (nhánh gốc release-t09-2026 @be6ef546aedb, commit f5ce5a0a2ca8fbc3802a58333ec14fdcf460909a)
```

**Journal #148915 — Dev Studio — 2026-10-27 (round 3 — MỚI NHẤT, branch `ai_studio_fixbug_41801` @ `8555b15d846996d320749558ead7540d1023496a`):**

```
Dev handoff — 27/10 10:41 · nhánh ai_studio_fixbug_41801

Nguyên nhân:
Trong job import CSV, khối gắn/bỏ tag (kèm action) và khối friend info tuỳ chỉnh của `readDataCSVV1` nằm ngoài điều kiện 'user có conversation với bot import'. Vì vậy user không phải bạn bè vẫn bị gắn tag, ghi friend info và chạy action (NPE ở `ActionModel` khi conversation null). Bản 1–2 đã chặn ở bước kiểm row. Bản 3 chỉ thêm cảnh báo khi lỗi DB ở bước kiểm làm bỏ row; #4758 xuất phát từ testcase lỗi thời, không phải lỗi mới.

Nội dung thay đổi:
- Job import CSV (HandleImportCsv): row có line_id không tồn tại bị bỏ qua, ghi log `Row: N - line_user not found: line_id=…`.
- Job import CSV: row của user không có conversation với account đang import bị bỏ qua toàn bộ (thông tin cơ bản, tag + action, friend info + action, memo), ghi log `Row: N - not friend of bot: …`.
- Job import CSV: khi line_id có nhiều bản ghi line_user, dữ liệu và action được ghi vào bản ghi là bạn bè của account import.
- Job import CSV: khi lỗi DB lúc kiểm một row, chỉ row đó bị bỏ (log `validate exception: …`); các row sau vẫn import và file vẫn 完了済.
- Mới ở vòng 3: nếu file có row bị bỏ do lỗi DB, cuối file ghi 1 dòng log ERROR và gửi 1 tin Chatwork vào room exception: `[To:6395420]#readFileCSVV2 validate exception: csvId=… - botId=… - skipped rows=N/M - sample rows=[…] - first error=…`. Row lỗi do dữ liệu người dùng không được báo.
- Script recover docs/recovery/41801-recover.sql kèm hướng dẫn: dọn tag/friend info mà CSV đã ghi cho non-friend từ 2026-05-28.

Bug automation Test Studio:
- Bug #4758 không phải bug: Bỏ row lỗi DB, file vẫn 完了済, file sau import đủ: đúng chủ đích D-5 (docs/design/v2.md) và TC34818, khớp log run #6110. TC33330 viết theo hành vi vòng 1, cần cập nhật. Ý 'một lỗi cấp file' nay đã có ở 8555b15d8: 1 dòng `#readFileCSVV2 validate exception: csvId=… skipped rows=3/3` + 1 tin Chatwork.

File đã sửa (java-job):
  .../linedb/repository/ConversationRepository.java  |  3 +
  .../sns/line/threads/csv/HandleImportCsvTask.java  | 84 +++++++++++++++++++---
  2 files changed, 76 insertions(+), 11 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi nằm trong các hàm private có 1 caller và 1 method repo mới. D-7 chỉ thêm log và notify sau vòng lặp, không đổi dữ liệu ghi. Đã chứng minh bằng harness (bản mới pass, bản trước fail); chưa verify runtime với DB thật.
- Toàn bộ luồng import CSV của job (HandleImportCsvManager → readFileCSVV2 → csvValidate → readDataCSVV1): bạn bè thường, đã chặn, đang ẩn phải import như trước (view_name, email, sinh nhật, trạng thái tin nhắn, 対応マーク, memo, tag, friend info).
- Action tag / action friend info do CSV kích hoạt: chỉ chạy cho bạn bè, trên đúng bản ghi line_user.
- Bộ đếm tags.count_user_tag và friend_information_setting.total_user_has_value: không tăng do non-friend.
- Room Chatwork exception: thêm tối đa 1 tin mỗi file khi DB lỗi lúc import. Không gửi trên host production lme.watermeru.com và khi ENABLE_NOTIFY_CHATWORK tắt.
- ConversationRepository chỉ thêm method mới, không sửa method cũ → các nơi khác dùng repo không đổi.
- Hiệu năng: row hợp lệ vẫn tra line_id 1 lần; row non-friend thêm 1 truy vấn; D-7 không thêm truy vấn, chỉ thêm 1 lời gọi HTTP Chatwork mỗi file khi có lỗi DB.
- Không đổi API, web hay module khác.

Migration / thay đổi dữ liệu:
- [Recover · Sau deploy] Dọn tag_line_user / friend_information_value mà CSV đã ghi cho non-friend từ 2026-05-28, giảm count_user_tag / total_user_has_value — docs/recovery/41801-recover.sql: Trên linedb production: chạy PHẦN 1 (đếm/liệt kê, lưu kết quả), đối chiếu, rồi chạy PHẦN 2 (xoá + giảm bộ đếm). Script không tự COMMIT: người chạy COMMIT hoặc ROLLBACK bằng tay sau khi đối chiếu. Chi tiết trong docs/recovery/41801-recover.md — không rollback được, backup: Lưu kết quả PHẦN 1; mysqldump các row tag_line_user, friend_information_value theo id ở PHẦN 1 và các row tags, friend_information_setting liên quan trước khi COMMIT

Recover dữ liệu: Cần recover — Không đổi so với bản 1–2: tag và friend info đã ghi cho user không phải bạn bè vẫn còn trong DB. Hành vi bỏ row khi lỗi DB (bản 3) không làm hỏng dữ liệu vì row bị bỏ không được ghi gì.
- Ảnh hưởng: tag_line_user (+ tag_history trigger 19001) của bot import ghi cho user không phải bạn bè
- Ảnh hưởng: friend_information_value (+ friend_info_history 19001, total_user_has_value) ghi cho non-friend
- Ảnh hưởng: Action của tag/friend info đã chạy — không hoàn tác được
- Khoảng thời gian: Từ release-t3-2024 (03/2024) tới khi bản sửa chạy; chỉ truy vết chắc chắn từ 2026-05-28 (history có trigger 19001)
- Cách recover: Script docs/recovery/41801-recover.sql (đã làm ở D-2/D-6): phần đếm + phần dọn idempotent (điều kiện NOT EXISTS conversation), không tự COMMIT; người vận hành chạy trên production.
- Ảnh hưởng tới khách: User không phải bạn bè không hiện ở danh sách bạn bè nên dọn dữ liệu không đổi màn khách đang thấy; action đã chạy không hoàn tác.

Việc cần người làm thêm (ngoài phạm vi task):
- Test Studio: cập nhật TC33330 (NEW-8) theo hành vi bỏ row: mỗi row một lỗi validate, cộng một dòng tổng kết cấp file; không còn kỳ vọng dừng phần còn lại của file.
- DBA xác nhận index line_user.line_id trên production (Test Studio #4002, vẫn để sau).
- Báo team đang theo dõi room Chatwork exception (448190376): khoảng 03:04 ngày 2026-10-27 (giờ runner), harness của reviewer nhiều khả năng đã gửi thật 1 tin test `[To:6395420]#readFileCSVV2 validate exception: csvId=79046 - botId=219704 - skipped rows=3/4 …`. Tin này dùng dữ liệu giả và có thể bỏ qua.
- Sửa riêng lỗi cũ của import CSV: row thiếu cột đi nhánh `continue` mà không tăng số row, làm lệch số row trong log (HandleImportCsvTask.readFileCSVV2).
- Cân nhắc gom báo Chatwork cho lỗi DB trong catch theo row của `readDataCSVV1` (code cũ, hiện chỉ ghi log), theo cách đã làm ở D-7.

Điểm cần test:
- TC33330 cập nhật (#4758): đổi tên bảng conversation rồi import 3 row → có 3 dòng `#csvValidate Exception`, có `Row: 2/3/4 - validate exception` và đúng 1 dòng `[To:6395420]#readFileCSVV2 validate exception: csvId=… - botId=… - skipped rows=3/3 - sample rows=[2, 3, 4] - first error=validate exception: …`; file 完了済; không ghi tag/data; khôi phục bảng rồi import file sau thì vào đủ.
- Lỗi DB thoáng qua ở 1 row giữa file → `skipped rows=1/N`; các row trước và sau vẫn import.
- File chỉ có row line_id rỗng / line_user not found / not friend of bot (không có lỗi DB) → không có dòng `validate exception: csvId`, không có Chatwork.
- File có trên 10 row lỗi DB → `sample rows` chỉ có 10 số đầu, `first error` dài tối đa 200 ký tự.
- Môi trường local giữ `ENABLE_NOTIFY_CHATWORK=0` → chỉ kiểm dòng log, không bật Chatwork thật.
- Hồi quy vòng 1–2: bạn bè thường / đã chặn / đang ẩn import như trước; non-friend bị bỏ, không gắn tag, không chạy action, không NPE; line_id trùng thì ghi vào đúng bản ghi là bạn bè.

Branch: ai_studio_fixbug_41801
- linect-service: ai_studio_fixbug_41801 (nhánh gốc release-t09-2026 @be6ef546aedb, commit 8555b15d846996d320749558ead7540d1023496a)
```
