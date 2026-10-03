# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #41573 (journal "AI LME Fix bug" #138647, 2026-09-26) bởi `/new-task` ngày 2026-09-29. **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Kim Cúc` (assigned_to) / AI LME Fix bug (auto-fixbug) |
| Commit / Pull Request | `sns-line` commit `38c6fd1d21` (2 file) |
| Branch | `ai_small_41573` (nhánh gốc `release_step_20260827`) — đã push |
| Ngày submit đánh giá | `2026-09-26` (Journal #138647) |
| Auto-filled | `2026-09-29 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Điều kiện lọc theo **thẻ (tag)** của bộ lọc bạn bè dùng subquery **TƯƠNG QUAN**: `EXISTS`/`NOT EXISTS` kèm `LIMIT 1` (lựa chọn có/không có thẻ) và subquery đếm so với số thẻ (lựa chọn đủ/không đủ N thẻ). Vì subquery tham chiếu cột của bảng ngoài (và còn có `LIMIT 1`) nên MySQL không chuyển được thành semi-join/anti-join mà phải chạy lại subquery cho TỪNG dòng bạn bè; bot nhiều bạn cộng danh sách hàng trăm thẻ khiến câu đếm mất khoảng 12s trên MySQL 5.7 và khoảng 30s trên MySQL 8.0, do bản 8.0 chọn chiến lược thực thi tệ hơn cho `NOT EXISTS`.

## 2. Cách fix

Đổi cả **4 lựa chọn** của điều kiện thẻ trong bộ lọc bạn bè từ subquery tương quan sang subquery **KHÔNG tương quan** giống job Java:

- **Có thẻ** = `bot_line_user.line_user_id IN (select distinct line_user_id from tag_line_user where tag_id IN (...))`
- **Không có thẻ** = `NOT IN` cùng danh sách đó
- **Đủ N thẻ** = `IN` của danh sách gom nhóm `group by line_user_id having count(tag_id) = N`
- **Không đủ N thẻ** = `NOT IN` của chính danh sách gom nhóm đó

Bỏ hẳn `EXISTS`/`NOT EXISTS` và `LIMIT 1`. Thêm điều kiện `tag_line_user.line_user_id is not null` vì cột này cho phép NULL, nếu không thì `NOT IN` gặp NULL sẽ trả về rỗng. Áp cho **3 chỗ** trong bộ lọc bạn bè (bộ lọc cơ bản, nhánh AND và nhánh OR của bộ lọc nâng cao) và **3 chỗ tương ứng** ở bản sao đọc replica (`ConversationReplicate`); giữ nguyên cách đếm `count(tag_id)` **không distinct** để kết quả y hệt trước (hành vi cũ giữ nguyên có chủ ý, xem cảnh báo ở "Ghi chú thêm").

Quét ngang: cùng 2 file còn các subquery đếm tương quan cho điều kiện **kịch bản (scenario)** và **điều kiện chuyển đổi (conversion)** — Dev ghi nhận nhưng KHÔNG fix, để làm ticket riêng vì thuộc điều kiện lọc khác và không phải lỗi `NOT EXISTS` mà ticket #41573 nêu.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê nguyên văn 10 function/nhóm ở Journal #138647 mục ■3. Cột "Thay đổi" dưới đây suy từ mục 4.1 (chỉ 2 file Conversation.php + ConversationReplicate.php được khai là "file thay đổi"); các hàm còn lại là CALLER — chỉ được check, không sửa trực tiếp. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Conversation::advanceFilter` (`app/Conversation.php:92`, điều kiện thẻ ~188-210) | Đổi điều kiện thẻ sang subquery không tương quan | Bộ lọc bạn bè **cơ bản** |
| 2 | `Conversation::advanceFilterPost` nhánh AND (`app/Conversation.php:247`, case 'tag' ~423-443) | Đổi điều kiện thẻ sang subquery không tương quan | Bộ lọc bạn bè **nâng cao — nhánh AND** |
| 3 | `Conversation::advanceFilterPost` nhánh OR (`app/Conversation.php`, case 'tag' ~1120-1140) | Đổi điều kiện thẻ sang subquery không tương quan | Bộ lọc bạn bè **nâng cao — nhánh OR** |
| 4 | `ConversationReplicate::advanceFilter` (`app/ConversationReplicate.php:76`, điều kiện thẻ ~172-191) | Đổi điều kiện thẻ sang subquery không tương quan | Bản sao đọc (replica) của #1 |
| 5 | `ConversationReplicate::advanceFilterPost` nhánh AND + OR (`app/ConversationReplicate.php` ~392-414 và ~1012-1036) | Đổi điều kiện thẻ sang subquery không tương quan | Bản sao đọc (replica) của #2 + #3 |
| 6 | `FriendlistController::postFilterAdvance` / `getListFriend` / `ajaxCountFriend` (`app/Http/Controllers/Basic/FriendlistController.php`) | Không sửa — CALLER | Màn Friend List (FA-013) gọi hàm lọc |
| 7 | `BroadcastController` (`app/Http/Controllers/Basic/BroadcastController.php:411/466/2607`) | Không sửa — CALLER | Chọn đối tượng nhận tin Broadcast (FA-008) |
| 8 | `ChatController` (`app/Http/Controllers/ChatController.php:1740`) | Không sửa — CALLER | Lọc hội thoại theo thẻ ở màn Chat (FA-001) |
| 9 | `BotLineUser` / `BotLineUserPackage` / `FilterV2` (`app/BotLineUser.php:28,695`; `app/BotLineUserPackage.php:27,526`; `app/FilterV2.php:1473,1480`) | Không sửa — CALLER | Các entry point khác gọi hàm lọc |
| 10 | `LineUserModel.buildWhere` / `buildWhereV2` (`linect-service src/main/java/sns/line/models/LineUserModel.java:190-212, 480-525`) | Không sửa — **bản Java dùng làm MẪU** | Job Java đã dùng cách viết không tương quan này từ trước; PHP sửa theo cho khớp |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Conversation::advanceFilter` + `advanceFilterPost` (nhánh AND, nhánh OR) — điều kiện thẻ | `app/Conversation.php` | Direct | Bộ lọc bạn bè cơ bản + nâng cao (2 nhánh) — 3 khối điều kiện thẻ |
| F2 | `ConversationReplicate::advanceFilter` + `advanceFilterPost` (nhánh AND, nhánh OR) — điều kiện thẻ | `app/ConversationReplicate.php` | Direct | Bản sao đọc (replica) — 3 khối điều kiện thẻ tương ứng F1 |
| F3 | `FriendlistController::postFilterAdvance` / `getListFriend` / `ajaxCountFriend` | `app/Http/Controllers/Basic/FriendlistController.php` | Indirect (caller) | Màn Friend List — số đếm/list bạn bè khớp bộ lọc phải không đổi |
| F4 | `BroadcastController` (3 điểm gọi) | `app/Http/Controllers/Basic/BroadcastController.php` | Indirect (caller) | Chọn đối tượng nhận tin Broadcast — số người nhận phải không đổi |
| F5 | `ChatController` | `app/Http/Controllers/ChatController.php` | Indirect (caller) | Lọc hội thoại theo thẻ ở màn Chat |
| F6 | `BotLineUser` / `BotLineUserPackage` / `FilterV2` | `app/BotLineUser.php`, `app/BotLineUserPackage.php`, `app/FilterV2.php` | Indirect (caller) | Các entry point khác dùng chung hàm lọc |

### 4.2. List data bị update khi fix bug

> **Không có** — Dev xác nhận chỉ đổi cách viết câu SELECT, không có lệnh ghi/sửa dữ liệu, không thêm index, không migration.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(không có)* | — | Chỉ đổi query đọc (SELECT), không CREATE/UPDATE/DELETE/MIGRATE data nào |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend Filter / Segment (SC-003) — điều kiện lọc theo thẻ, kết quả phải giữ nguyên ở cả 4 lựa chọn (có/không có/đủ N/không đủ N thẻ) | F1, F2 | High |
| T2 | Friend List (FA-013) — màn danh sách bạn bè + ô đếm số bạn khớp bộ lọc | F1, F2, F3 | High |
| T3 | Broadcast (FA-008) + Delivery Target Selector (SC-006) — chọn đối tượng nhận tin dùng chung hàm lọc, số người nhận phải không đổi | F1, F2, F4 | High |
| T4 | 1-on-1 Chat (FA-001) — lọc hội thoại theo thẻ ở màn chat dùng chung hàm lọc | F1, F2, F5 | Medium |

---

## Ghi chú thêm (từ Dev)

- **5. Recover data:** ✔ Không cần — không có ghi/sửa dữ liệu.
- **6. Verify (mức Dev đã làm):** Mức **lint only** — `php -l` 2 file sửa: không lỗi syntax; grep xác nhận không còn `EXISTS`/`NOT EXISTS` trong 2 file sau khi sửa; các subquery `qr_code`/`qr_code_action` dùng biến `$in_string` riêng không bị đụng (đã đổi tên biến khối thẻ thành `$tag_in_string`/`$tag_count_string`/`$tag_number` để không trùng); **mô phỏng ngữ nghĩa bằng PHP** cho cả 4 lựa chọn trên bộ dữ liệu có dòng thẻ TRÙNG và dòng `line_user_id` NULL: **24/24 ca** cho kết quả giống hệt cách cũ. **Chưa chạy EXPLAIN** — MySQL dev (`host.docker.internal:3306`, `127.0.0.1`, `172.17.0.1`) đều Connection refused trong phiên fix.
- Bằng chứng Dev nêu: `tag_line_user.line_user_id` là `int(12) DEFAULT NULL` → bắt buộc lọc `IS NOT NULL` trong subquery `NOT IN`; `bot_line_user.line_user_id` là `int(11) NOT NULL` → vế ngoài của `NOT IN` không bao giờ NULL, không đổi kết quả so với `NOT EXISTS`; mẫu Java `LineUserModel.java:204-206` dùng đúng pattern `NOT IN`/`IN` group-by-having mà ticket yêu cầu; tiền lệ cùng kiểu trong repo — fix #39121 đã đổi điều kiện QR/landing từ subquery đếm tương quan sang `IN`/`NOT IN` kèm `line_id is not null`; cách viết `EXISTS`/`NOT EXISTS` hiện tại do fix #38294 (commit `cfcaded173`) đưa vào để thay `count()>0` — nhanh hơn trên 5.7 nhưng vẫn tương quan, MySQL 8.0 chọn plan xấu cho `NOT EXISTS`.
- ⚠️ **Chưa đo tốc độ thật sau fix** — mục tiêu ticket là "tăng tốc độ" nhưng Dev chỉ verify **tương đương kết quả** (24/24 ca PHP simulation), không đo lại thời gian chạy thật (không kết nối được MySQL dev). QA/DBA cần đo lại nếu muốn xác nhận mục tiêu hiệu năng.
- ⚠️ **Cách viết mới phụ thuộc index trên `tag_line_user.tag_id`** — nếu production thiếu index, DBA cần xác nhận trước khi kết luận đã tối ưu.
- ⚠️ **Hành vi giữ nguyên có chủ ý**: lựa chọn "đủ N thẻ" vẫn đếm theo **số dòng** (không `DISTINCT tag_id`) — nếu bạn bè có thẻ trùng, kết quả có thể khác job Java (Java dùng `count(distinct tag_id)`). Không phải bug của ticket này, cần BA/DBA chốt riêng nếu muốn đổi.
- ⚠️ **Bug có sẵn, giữ nguyên (ngoài phạm vi)**: danh sách thẻ rỗng ở lựa chọn 1/2/3 của bộ lọc nâng cao vẫn sinh `IN ()` lỗi SQL như trước fix (chỉ lựa chọn 0 có guard `!empty`).
- **Ticket riêng (ngoài phạm vi #41573)**: cùng 2 file còn subquery đếm tương quan cho điều kiện **kịch bản (scenario)** và **điều kiện chuyển đổi (conversion)** — không thuộc phạm vi fix này.
- Đã có **task Studio** cho ticket này: `task_id=337` (feature `friend-filter`, round 1, 39 TC, `tc-ready`, `reviewState=leader`) — dùng làm nguồn TC review (file 04).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
