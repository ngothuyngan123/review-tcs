# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-id>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`), tạo folder mới + fill các section bên dưới (cùng với `03-dev-impact.md`).
> 2. **Paste tay** — nếu không có Redmine link, member paste nội dung task bug.
>
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL, môi trường phát hiện) tra thẳng trên Redmine khi cần, KHÔNG chép lại vào đây.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42336 — [JOB] Import csv gây duplicate memo` |
| Module / Màn hình | `CSV管理 (CSV management) — Job import CSV (HandleImportCsvTask, linect-service); liên quan Chat 1:1 tab メモ và job export CSV` |

## Mô tả bug (bản dịch tiếng Việt)

<!--
Dịch sát nội dung khách hàng báo sang tiếng Việt — KHÔNG tóm tắt, KHÔNG diễn giải lại.
Giữ nguyên thuật ngữ JP trong câu (vd 到達アクション, リッチメニュー), có thể chú thích VN trong ngoặc.
KHÔNG chép lại nguyên khối 原文 tiếng Nhật.
-->

Logic hiện tại: Mỗi lần import CSV thì job lại tạo ra các bản ghi memo mới của friend (bạn bè) => Gây duplicate memo (memo trùng).

=> Chỗ này sửa lại: Check 'content' (nội dung) memo nếu đã tồn tại thì bỏ qua, nếu chưa tồn tại thì tạo mới.

Cách làm (đề xuất của người báo): SELECT DISTINCT content memo theo bot và conversation ra add vào map. Kiểm tra nếu memo import chưa tồn tại thì mới insert.

Tồn đọng làm sau khi xong: làm job recover check clear memo trùng (Recover data memo trùng cũ, Dev ghi là follow-up ngoài phạm vi task này).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" / "Steps to reproduce" riêng — chỉ có mô tả logic sai ở trên. Dev đã tự tái hiện và confirm qua các vòng đánh giá ảnh hưởng (xem file 03). -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #42336 không có attachment (0). -->

## Ghi chú thêm của Leader

⚠️ Bug không tái hiện được bằng steps cụ thể trong Redmine (ticket chỉ mô tả logic sai + hướng sửa đề xuất) — root cause thật đã được Dev Studio tự điều tra và confirm qua 3 vòng đánh giá ảnh hưởng (v1 → v2 → v3, xem file 03). TCs nên tập trung verify cách fix cuối cùng (v3) + regression impact, không chỉ bám theo "cách làm" ban đầu của người báo (SELECT DISTINCT) — cách này đã bị Dev đổi 2 lần vì phát sinh bug mới.

Lịch sử các vòng sửa (Dev tự phát hiện thêm lỗi trong lúc làm, KHÔNG phải do khách hàng báo thêm):
- **v1** (#141080): fix gốc — thêm query lấy memo hiện có theo bot + conversation, bỏ qua memo trùng nội dung khi import.
- **v2** (#141146 / #141197): v1 dùng `SELECT DISTINCT` dưới collation `utf8mb4_unicode_ci` nên gộp nhầm các biến thể chỉ khác hoa/thường, khoảng trắng, kana, độ rộng ký tự → các biến thể này vẫn bị tạo trùng. v2 bỏ DISTINCT, so khớp chính xác từng ký tự.
- **v3** (#141983 / #141987): v1/v2 tự phát hiện thêm 2 lỗi qua tự test — **#42521** (race condition: 5 worker job import chạy song song, 2 file cùng bot cùng thấy "chưa có" nên cùng insert trùng) và **#42522** (tập kiểm trùng lọc theo `bot_id`, trong khi export xuất memo của cả hội thoại kể cả memo cũ `bot_id=0` → import lại file export vẫn tạo trùng với memo cũ đó). v3 sửa: kiểm trùng theo hội thoại (không lọc bot_id) + mỗi bot chỉ chạy 1 file import tại 1 thời điểm (file của bot khác vẫn song song).

Ticket status hiện tại: `Fix done - Đợi test`. Branch: `ai_studio_fixbug_42336` (gốc `release-t09-2026`).

## Journal / note từ Redmine (nguyên văn)

<!--
Chép nguyên văn journal/note có giá trị điều tra (log, SQL, ID, xác nhận của Dev/CS).
Bỏ qua journal chỉ đổi status / assignee.
Format: **Journal #<id> — <author> — <YYYY-MM-DD>:** rồi block ``` nội dung ```
-->

**Journal #141080 — Dev Studio — 2026-10-08:**

```
Dev Studio · Nguyên nhân & hướng sửa (v1)

Nguyên nhân:
Job import CSV (`HandleImportCsvTask#readDataCSVV1`) coi mọi cột sau phần header là memo và luôn insert memo mới 「CSV追加 (ngày)」 mà không kiểm tra memo cùng nội dung đã có. File export (`HandleExportCsvTask`) xuất toàn bộ memo hiện có của bạn bè vào các cột cuối, nên export → import lại (hoặc import cùng file 2 lần, hoặc 2 cột cùng nội dung) tạo memo trùng. Giả thuyết của người báo là đúng.

Hướng sửa:
- D-1 Thêm query lấy nội dung memo hiện có theo bot và hội thoại vào MemoRepository
- D-2 Import CSV bỏ qua memo đã tồn tại cùng nội dung

Ảnh hưởng / rủi ro:
Chỉ đổi job import CSV (CSV管理 upload) ở linect-service: memo trùng nội dung với memo đã có của cùng bạn bè, hoặc trùng ngay trong file, không còn được tạo. Export, Chat 1:1 và dữ liệu cũ không đổi; mỗi dòng có memo thêm 1 SELECT trên bảng memos (rủi ro hiệu năng nếu production không có index conversation_id).
```

**Journal #141146 — Dev Studio — 2026-10-08:**

```
Dev Studio · Nguyên nhân & hướng sửa (v2)

Nguyên nhân:
Job import CSV (`HandleImportCsvTask#readDataCSVV1`) luôn insert memo mới 「CSV追加」 cho mọi cột memo mà không kiểm tra memo cùng nội dung đã có, trong khi export xuất toàn bộ memo hiện có; vì vậy export rồi import lại (hoặc import cùng file 2 lần) sinh memo trùng. Bản sửa v1 lấy nội dung memo đã có bằng `SELECT DISTINCT` dưới collation `utf8mb4_unicode_ci`, nên các nội dung chỉ khác hoa/thường, khoảng trắng cuối, kana hay độ rộng ký tự bị gộp lại và biến thể bị gộp vẫn bị tạo trùng.

Hướng sửa:
- D-1 Bỏ DISTINCT trong query lấy nội dung memo hiện có và đổi tên method
- D-2 Import CSV gọi method mới, giữ nguyên logic bỏ qua memo trùng

Ảnh hưởng / rủi ro:
Chỉ đổi job import CSV ở linect-service: memo trùng chính xác nội dung với memo đã có của cùng bạn bè, kể cả các biến thể chỉ khác hoa/thường, kana hay khoảng trắng cuối, không còn bị tạo lại. Export, Chat 1:1 và dữ liệu cũ không đổi; không migration.
```

**Journal #141197 — Dev Studio — 2026-10-08:**

```
Dev handoff — v2 · nhánh ai_studio_fixbug_42336

Nguyên nhân:
Job import CSV (`HandleImportCsvTask#readDataCSVV1`) luôn insert memo mới 「CSV追加」 cho mọi cột memo mà không kiểm tra memo cùng nội dung đã có, trong khi export xuất toàn bộ memo hiện có; vì vậy export rồi import lại (hoặc import cùng file 2 lần) sinh memo trùng. Bản sửa v1 lấy nội dung memo đã có bằng `SELECT DISTINCT` dưới collation `utf8mb4_unicode_ci`, nên các nội dung chỉ khác hoa/thường, khoảng trắng cuối, kana hay độ rộng ký tự bị gộp lại và biến thể bị gộp vẫn bị tạo trùng.

Nội dung thay đổi:
- Job import CSV: cột memo trùng nội dung với memo hiện có của bạn bè bị bỏ qua, không tạo memo 「CSV追加」 và memo_histories mới; ghi log số memo bỏ qua theo conversation và csv.
- Job import CSV: hai cột memo cùng nội dung trong một dòng chỉ tạo một memo.

File đã sửa (java-job):
  .../sns/line/models/linedb/repository/MemoRepository.java    |  8 ++++++++
  src/main/java/sns/line/threads/csv/HandleImportCsvTask.java  | 12 ++++++++++++
  2 files changed, 20 insertions(+)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi cục bộ trong một nhánh của job import, chỉ chặn insert khi trùng chính xác; không migration, không đổi cấu hình, các luồng khác dùng bảng memos không đổi.
- Job import CSV (hàm readDataCSVV1): phần tag, friend info, status_message, phone của cùng dòng không đổi nhưng nằm trong cùng hàm; test lại một dòng đầy đủ cột.
- Bảng memos và memo_histories: chỉ bớt insert, không update/delete; màn Chat 1:1 tab メモ hiển thị dữ liệu này.
- Export CSV, tạo/sửa memo ở Chat 1:1, memo từ form answer, lệnh recover:recover_memos: không đổi code, chỉ dùng chung bảng memos.
- Hiệu năng job import: thêm 1 SELECT memos theo bot_id + conversation_id cho mỗi dòng có memo; bảng memos trên DB điều tra không có index ngoài khoá chính.

Lưu ý khi deploy:
- Không migration/SQL, không biến cấu hình; deploy module job (linect-service) như thường và restart app.
- Nên kiểm SHOW INDEX FROM memos trên production; thiếu index conversation_id thì cân nhắc thêm (ngoài ticket).

Việc cần người làm thêm (ngoài phạm vi task):
- Làm job recover dọn memo trùng cũ (theo bot + conversation + content), như ticket ghi là làm sau.
- Kiểm tra trên production bảng memos có index conversation_id hay không; DB điều tra chỉ có PRIMARY KEY, nếu thiếu thì export và import đều full scan mỗi dòng.
- Export CSV ghi Shift-JIS và thay chuỗi "null" trên cả dòng nên memo có emoji hoặc chứa chữ null bị biến dạng; cân nhắc ticket riêng.
- Cập nhật spec csv-management (job): job import Spring Boot không còn là dead code.

Branch: ai_studio_fixbug_42336
- linect-service: ai_studio_fixbug_42336 (nhánh gốc release-t09-2026 @2e12efbf5710, commit a4c4153d4bd0cc1615642c5435c6ddb783b89c50)
```

**Journal #141983 — Dev Studio — 2026-10-09:**

```
Dev Studio · Nguyên nhân & hướng sửa (v3)

Nguyên nhân:
Bản sửa hiện tại kiểm trùng bằng cách đọc tập nội dung memo của bạn bè rồi mới insert, không có khoá. Job import có 5 worker dùng chung một hàng đợi nên 2 file của cùng bot có thể chạy cùng lúc: cả hai worker cùng thấy "chưa có" và cùng insert (#42521). Ngoài ra, tập kiểm trùng lọc theo bot_id, trong khi export xuất mọi memo của hội thoại, kể cả memo cũ bot_id=0. Vì vậy import lại file export vẫn tạo memo 「CSV追加」 trùng với memo đó (#42522).

Hướng sửa:
- D-1 Kiểm trùng memo theo hội thoại, không lọc bot_id
- D-2 Mỗi bot chỉ chạy 1 file import tại một thời điểm (mapBotIdRunning)

Ảnh hưởng / rủi ro:
Chỉ đổi job import CSV: các file của cùng một bot nay chạy lần lượt (bot khác vẫn song song) và kiểm trùng memo theo hội thoại; export, Chat 1:1 và form answer không đổi, không có migration. Cần test lại: 2 file cùng bot và 2 file khác bot, file lỗi giữa chừng không làm treo bot, job khởi động lại khi còn file đang chờ, và memo cũ bot_id=0.
```

**Journal #141987 — Dev Studio — 2026-10-09:**

```
Dev handoff — v3 · nhánh ai_studio_fixbug_42336

Nguyên nhân:
Bản sửa hiện tại kiểm trùng bằng cách đọc tập nội dung memo của bạn bè rồi mới insert, không có khoá. Job import có 5 worker dùng chung một hàng đợi nên 2 file của cùng bot có thể chạy cùng lúc: cả hai worker cùng thấy "chưa có" và cùng insert (#42521). Ngoài ra, tập kiểm trùng lọc theo bot_id, trong khi export xuất mọi memo của hội thoại, kể cả memo cũ bot_id=0. Vì vậy import lại file export vẫn tạo memo 「CSV追加」 trùng với memo đó (#42522).

Nội dung thay đổi:
- Job import CSV: cột memo trùng nội dung với memo hiện có của bạn bè bị bỏ qua, không tạo memo 「CSV追加」 và memo_histories mới; job ghi log số memo bị bỏ qua.
- Job import CSV: 2 cột memo cùng nội dung trong một dòng chỉ tạo 1 memo.
- Job import CSV: mỗi bot chỉ xử lý 1 file import tại một thời điểm, theo thứ tự upload; file của bot khác vẫn chạy song song trên 5 worker.

File đã sửa (java-job):
  .../models/linedb/repository/MemoRepository.java   | 10 +++++
  .../line/threads/csv/HandleImportCsvManager.java   |  9 +++--
  .../sns/line/threads/csv/HandleImportCsvTask.java  | 47 ++++++++++++++++++++--
  3 files changed, 60 insertions(+), 6 deletions(-)

Đánh giá ảnh hưởng — Rủi ro trung bình: Phần memo cục bộ và rủi ro thấp. Phần khoá theo bot đổi cách lấy việc của cả job import (dùng khuôn đã chạy ở salon calendar) và làm file cùng bot chạy tuần tự, nên cần test hồi quy luồng import nhiều file.
- Toàn bộ job import CSV: khi một bot upload nhiều file liền, các file đó nay chạy tuần tự nên thứ tự và tốc độ xử lý thay đổi. Một file lỗi giữ bot thêm khoảng 60s.
- Phần tag, friend info, status_message, phone của cùng dòng: code không đổi, nhưng không còn 2 file cùng bot chạy chồng nhau.
- Bảng memos và memo_histories: chỉ bớt insert, không update hay delete. Màn Chat 1:1 tab メモ hiển thị dữ liệu này.
- Export CSV, tạo/sửa memo ở Chat 1:1, memo từ form answer và lệnh recover:recover_memos: không đổi code, chỉ dùng chung bảng memos.
- Bảng csv_filter_upload_history: trạng thái vẫn đi WAIT, IN_QUEUE, RUNNING rồi DONE như cũ. File của bot đang bận nằm ở IN_QUEUE lâu hơn.
- Hiệu năng job import: thêm 1 SELECT memos theo conversation_id cho mỗi dòng có memo. Trên DB điều tra, bảng memos chỉ có index khoá chính.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Cần recover — Hai lỗ hổng vòng 2 chỉ có trên nhánh task chưa phát hành, nên không làm hỏng thêm dữ liệu. Memo trùng cũ do lỗi gốc (import vô điều kiện) vẫn nằm trong DB. Theo ticket, việc dọn là job recover riêng làm sau khi xong.
- Ảnh hưởng: memos: các nhóm cùng conversation_id và cùng content chính xác (thường có title 「CSV追加 (ngày)」), kèm memo_histories của chúng
- Khoảng thời gian: Từ khi job import CSV ghi vào bảng memos (memo CSV追加 sớm nhất trên DB điều tra là 2025-07-18) tới khi bản sửa được deploy
- Ước lượng: 15
- Cách recover: Job recover riêng theo ticket (follow-up, không thuộc lần sửa này): có chế độ dry-run đếm theo nhóm, xoá memo thừa và memo_histories của chúng, chạy lại nhiều lần không sinh thêm thay đổi. 15 dòng thừa trong 13 nhóm, 10 hội thoại là số trên DB điều tra (đã tính cả trùng tạo tay); production cần đếm lại.
- Ảnh hưởng tới khách: Xoá memo khách nhìn thấy ở tab メモ: cần người phụ trách quyết định trước khi chạy trên production.

Lưu ý khi deploy:
- Deploy module job (linect-service) và restart app; job tự nạp lại file IN_QUEUE/RUNNING khi khởi động.
- Chỉ chạy 1 tiến trình import (cờ ENABLE_HANDLE_IMPORT_CSV bật ở đúng 1 instance) vì khoá theo bot chỉ có hiệu lực trong một JVM; đây cũng là điều kiện sẵn có của job.
- Nên kiểm SHOW INDEX FROM memos trên production (ngoài ticket).

Branch: ai_studio_fixbug_42336
- linect-service: ai_studio_fixbug_42336 (nhánh gốc release-t09-2026 @2e12efbf5710, commit 15e30c841203d4932c1b7af9715b6d6cad9168b0)
```
