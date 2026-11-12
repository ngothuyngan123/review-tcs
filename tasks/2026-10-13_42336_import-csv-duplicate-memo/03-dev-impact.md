# 03 — Đánh giá ảnh hưởng từ Dev

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-id>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`) rồi parse section "Đánh giá ảnh hưởng", fill các mục bên dưới. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — Dev paste nguyên văn đánh giá theo format 4 mục.
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

> ⚠️ Redmine #42336 không có 1 section "Đánh giá ảnh hưởng" duy nhất — Dev Studio điều tra qua **3 vòng journal** (v1 → v2 → v3), mỗi vòng tự phát hiện thêm lỗi trong bản sửa trước. Nội dung dưới đây lấy từ vòng **cuối cùng, đầy đủ nhất** (Journal #141987, "Dev handoff — v3", 2026-10-09) — đã cumulative cả v1+v2+v3. Nguyên văn đầy đủ cả 5 journal nằm ở file `01-bug-task.md`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (handoff tự động) — assignee Redmine: `Nguyen Ha Vi (vinth)` |
| Commit / Pull Request | `<chưa có PR link>` — commit cuối: `15e30c841203d4932c1b7af9715b6d6cad9168b0` (base `release-t09-2026@2e12efbf5710`) |
| Branch | `ai_studio_fixbug_42336` |
| Ngày submit đánh giá | `2026-10-09` (Journal #141987, vòng v3 — vòng cuối) |
| Auto-filled | `2026-10-13 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

**Root cause gốc (v1 — Journal #141080, 2026-10-08):**

Job import CSV (`HandleImportCsvTask#readDataCSVV1`) coi mọi cột sau phần header là memo và luôn insert memo mới 「CSV追加 (ngày)」 mà không kiểm tra memo cùng nội dung đã có. File export (`HandleExportCsvTask`) xuất toàn bộ memo hiện có của bạn bè vào các cột cuối, nên export → import lại (hoặc import cùng file 2 lần, hoặc 2 cột cùng nội dung) tạo memo trùng.

**2 lỗi bổ sung Dev tự phát hiện khi tự test v1/v2 (v3 — Journal #141983/#141987, 2026-10-09):**

Bản sửa v1/v2 kiểm trùng bằng cách đọc tập nội dung memo của bạn bè rồi mới insert, không có khoá. Job import có 5 worker dùng chung một hàng đợi nên 2 file của cùng bot có thể chạy cùng lúc: cả hai worker cùng thấy "chưa có" và cùng insert (**#42521** — race condition). Ngoài ra, tập kiểm trùng lọc theo `bot_id`, trong khi export xuất mọi memo của hội thoại, kể cả memo cũ `bot_id=0`. Vì vậy import lại file export vẫn tạo memo 「CSV追加」 trùng với memo đó (**#42522**).

(Lỗi trung gian ở v1 — đã fix ở v2, không còn trong code hiện tại: v1 dùng `SELECT DISTINCT` dưới collation `utf8mb4_unicode_ci` nên gộp nhầm các biến thể chỉ khác hoa/thường, khoảng trắng cuối, kana, độ rộng ký tự → các biến thể này vẫn bị tạo trùng.)

## 2. Cách fix

**Trạng thái code hiện tại (cumulative v1+v2+v3, theo Journal #141987):**

- Job import CSV: cột memo trùng nội dung với memo hiện có của bạn bè (so khớp **chính xác từng ký tự**, không dùng DISTINCT/collation gộp biến thể) bị bỏ qua, không tạo memo 「CSV追加」 và `memo_histories` mới; job ghi log số memo bị bỏ qua (`#readDataCSVV1 skip duplicate memo: n - conversationId ... - csvId ...`).
- Job import CSV: 2 cột memo cùng nội dung trong một dòng chỉ tạo 1 memo.
- Job import CSV: kiểm trùng memo theo **hội thoại (conversation_id)**, không lọc theo `bot_id` — để bắt được cả memo cũ `bot_id=0`.
- Job import CSV: mỗi bot chỉ xử lý **1 file import tại một thời điểm**, theo thứ tự upload (`mapBotIdRunning`, khuôn tái dùng từ salon calendar); file của bot khác vẫn chạy song song trên 5 worker.

File đã sửa (java-job, nhánh `ai_studio_fixbug_42336`):
| File | Thay đổi |
|---|---|
| `.../models/linedb/repository/MemoRepository.java` | +10 dòng — method lấy content memo hiện có theo `conversation_id` (không filter bot_id, không DISTINCT) |
| `.../threads/csv/HandleImportCsvManager.java` | +9/-? dòng — khoá theo bot khi lấy việc từ hàng đợi |
| `.../threads/csv/HandleImportCsvTask.java` | +47 dòng — gọi method kiểm trùng mới + logic khoá theo bot + log skip |

Không có migration / thay đổi schema / biến cấu hình (Dev đã confirm qua diff).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleImportCsvTask#readDataCSVV1` — phần tag, friend info (default/custom), status_message, phone, unconfirm message, count user unconfirm của cùng dòng | Không đổi code | Nằm trong cùng hàm với nhánh memo vừa sửa — Dev tự note "test lại một dòng đầy đủ cột" |
| 2 | `HandleExportCsvTask` (export CSV) | Không đổi code | Dùng chung bảng `memos`; là nguồn sinh ra kịch bản báo lỗi gốc (export → import lại) |
| 3 | Chat 1:1 — tạo/sửa memo tay (`ChatController`), memo từ form answer | Không đổi code | Dùng chung bảng `memos`/`memo_histories`; memo sửa/xoá ở đây không còn chặn import nội dung cũ (import lại tạo lại memo — theo REQ-011 của Studio) |
| 4 | `recover:recover_memos` (lệnh Laravel có sẵn) | Không đổi code | Dùng chung bảng `memos` |
| 5 | `HandleImportCsvManager` — cách lấy việc từ hàng đợi job import (5 worker) | **Có đổi** — thêm khoá theo bot | Nguồn gốc bug #42521 (race condition); ảnh hưởng toàn bộ job import, không riêng nhánh memo |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `readDataCSVV1` — nhánh memo (cột sau header) | `HandleImportCsvTask.java` | Direct | Thêm kiểm trùng exact theo memo hiện có (toàn hội thoại) + trong cùng dòng |
| F2 | Method mới lấy content memo theo `conversation_id` | `MemoRepository.java` | Direct | Thay method cũ dùng `bot_id` + `SELECT DISTINCT` (v1) |
| F3 | Lấy việc từ hàng đợi job import (khoá theo bot) | `HandleImportCsvManager.java` | Direct | File cùng bot chạy tuần tự; bot khác vẫn song song (5 worker) |
| F4 | `readDataCSVV1` — nhánh tag / friend info / status_message / phone / unconfirm message cùng dòng | `HandleImportCsvTask.java` | Indirect | Code không đổi nhưng nằm trong cùng hàm + không còn chạy chồng 2 file cùng bot |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `memos` (content theo conversation_id) | Chỉ **bớt INSERT** khi trùng chính xác — không UPDATE/DELETE | Hiển thị ở Chat 1:1 tab メモ |
| D2 | `memo_histories` | Chỉ bớt INSERT tương ứng với D1 | — |
| D3 | `csv_filter_upload_history` (trạng thái file import) | Không đổi enum (WAIT → IN_QUEUE → RUNNING → DONE) nhưng **thời gian ở IN_QUEUE lâu hơn** nếu cùng bot có nhiều file | Hệ quả của khoá theo bot (F3) |
| D4 | Memo trùng **cũ** (tạo trước khi deploy bản fix) | **KHÔNG xoá/sửa** — vẫn còn trong DB | Cần **recover data** riêng (job follow-up, ngoài phạm vi task này theo ticket): DB điều tra ghi nhận ~15 dòng thừa / 13 nhóm / 10 hội thoại từ 2025-07-18 tới lúc deploy; production cần đếm lại. Quyết định xoá ảnh hưởng tới khách (khách nhìn thấy ở tab メモ) — cần người phụ trách chốt trước khi chạy |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Job import CSV (CSV管理 tab インポート) | F1, F2, D1, D2 | High — core của fix, phải verify đúng case trùng/không trùng |
| T2 | Thứ tự & tốc độ xử lý khi 1 bot upload nhiều file liên tiếp | F3, D3 | Medium — hành vi đổi từ song song → tuần tự cho cùng bot; file lỗi giữ bot thêm ~60s |
| T3 | Chat 1:1 tab メモ (hiển thị memo) | D1, D2 | Low — chỉ số lượng memo giảm (ít trùng hơn), không đổi UI/logic hiển thị |
| T4 | Job export CSV | (không đổi code, nhưng là nguồn sinh kịch bản lỗi) | Low — cần test lại chu trình export → import làm oracle, không phải vì export đổi |
| T5 | Memo cũ `bot_id=0` | F2 (bỏ filter bot_id), D4 | Medium — rủi ro bỏ sót nếu env test không có memo cũ dạng này |
| T6 | Hiệu năng job import (file lớn, bảng `memos` không index ngoài PK trên DB điều tra) | F1, F2 | Low/Medium — thêm 1 SELECT mỗi dòng có memo; RULE-08 không kết luận từ local/staging, cần kiểm `SHOW INDEX FROM memos` trên production (ngoài phạm vi task) |

> **Rủi ro tổng thể theo Dev**: phần memo cục bộ (F1/F2) — thấp. Phần khoá theo bot (F3) đổi cách lấy việc của *cả* job import — trung bình, cần test hồi quy luồng import nhiều file (không riêng case có memo).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
