# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (auto-fixbug) — Assignee Redmine: Ngô Thúy Ngần |
| Commit / Pull Request | `1fa403244d` (lần đầu) → `0680a6df61` (bổ sung `is_deleted`, Replicate) → `3068c5d224` (nhánh Dev Studio, thêm JS #42170/#42171). v3 (#42327, #42328) **đang sửa** — chưa có commit lúc review lượt 2 |
| Branch | `ai_studio_implement_42000` (base `ai_small_42000` / `release_step_20260930_v2`) — Studio task #366 đang test nhánh này |
| Ngày submit đánh giá | 2026-10-06 (Journal #140372) · cập nhật 2026-10-06 (#140529, #140556) · Dev Studio handoff 2026-10-07 (#140946) · v3 2026-10-08 (#141352) |
| Auto-filled | 2026-10-06 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Từ MySQL 8.0.17, điều kiện NOT IN (subquery) / NOT EXISTS nằm ở mức AND được đổi thành antijoin và optimizer có thể chọn đọc toàn bộ dòng khớp của bảng con rất lớn (kịch bản, thông tin bạn bè, chuyển đổi, click trang đích) rồi mới loại trừ, plan lại không ổn định giữa các lượt ⇒ câu lọc có thể từ dưới 1 giây thành hàng chục–hàng trăm giây. 5 chỗ web còn dính mẫu này (sau khi item "QR chưa quét" đã tách xử lý ở #42006): bộ lọc bạn bè (không theo kịch bản, thông tin bạn bè chưa đăng ký), màn lọc người nhận (không theo kịch bản / kịch bản chưa dừng, chưa đạt chuyển đổi) và số người đã chặn ở thống kê QR/trang đích.

## 2. Cách fix

Giữ nguyên điều kiện lọc, chỉ đổi dạng SQL:
- **4 điều kiện NOT IN (subquery)** đưa danh sách vào bảng dẫn xuất `SELECT DISTINCT` (cùng cách #42006 đã đo 0,1–0,5s):
  - Bộ lọc bạn bè nhánh **"không theo kịch bản"** (`scenario_condition=1`) và **"thông tin bạn bè chưa đăng ký"** (`op_compare=3`) — cả nhánh AND lẫn OR, qua helper mới `Conversation::distinctDerivedSubquery`.
  - Màn lọc người nhận **"không theo kịch bản"** / **"kịch bản chưa dừng"** / **"chưa đạt chuyển đổi"**.
- **Câu NOT EXISTS tương quan** đếm người đã chặn ở thống kê QR (`QRCodeController.php:2112`) — thêm hint `NO_SEMIJOIN` để MySQL 8.0 giữ cách chạy như 5.7 (seek chỉ mục `bot_id`+`line_id` từng dòng), vì dạng bảng dẫn xuất ở chỗ này đã bị loại trước đó (lý do loại không ghi chi tiết trong journal — ⚠️ cần hỏi lại Dev nếu cần).
- Item 1 (QR chưa quét) đã làm ở #42006 nên **không đụng**; bản mirror `ConversationReplicate` dùng mảng PHP (pluck) nên **không thuộc mẫu này, không sửa**.

**Quyết định chốt riêng cho nhánh scenario** (đính chính ở Journal #140262, thay cho Journal #140256): dạng SQL chung cho 3 repo (web/job/MCP) —
```
x NOT IN (SELECT DISTINCT line_user_id FROM scenario_lineuser WHERE scenario_id = ? AND is_following = <1|2> AND is_deleted = 0 AND line_user_id IS NOT NULL)
```
Quyết định yêu cầu: thêm `DISTINCT` + `is_deleted = 0`, **giữ** `whereNotNull(line_user_id)` (khác với bản nháp #140256 định bỏ `whereNotNull` — đã bị đính chính).

⚠️ **Chưa xác nhận quyết định này đã được áp vào code**: báo cáo fix (Journal #140372) ghi *"Giữ nguyên điều kiện lọc, chỉ đổi dạng SQL"* và *"điều kiện lọc giữ nguyên từng chữ"*; Studio `dev_impact` cũng không nhắc `is_deleted`. Code gốc của `Conversation.php` (nhánh scenario) **không** lọc `is_deleted` ⇒ nhiều khả năng sau fix vẫn không lọc. `FilterController` thì đã có `is_deleted = 0` từ trước.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Conversation::advanceFilterPost` — case scenario (`scenario_condition=1`) nhánh AND + OR (`app/Conversation.php`) | Sửa — NOT IN → bảng dẫn xuất DISTINCT (Dev báo giữ nguyên điều kiện; `is_deleted = 0` theo quyết định 05/10 chưa xác nhận đã áp) | Theo quyết định chốt nhánh scenario (Journal #140262) |
| 2 | `Conversation::advanceFilterPost` — thông tin bạn bè (`op_compare=3`) nhánh AND + OR (`app/Conversation.php`) | Sửa — NOT IN → bảng dẫn xuất DISTINCT | friend_information_value ≥ 50 triệu dòng |
| 3 | `Conversation::distinctDerivedSubquery` — helper mới (`app/Conversation.php`) | Thêm mới | Dùng chung cho cả 2 nhánh trên, bọc subquery gốc thành derived table SELECT DISTINCT |
| 4 | `FilterController::ajaxGetListUserFilter` — scenario not_apply/not_done, conversion or_not (`app/Http/Controllers/Basic/FilterController.php`) | Sửa | Cùng mẫu NOT IN antijoin |
| 5 | `QRCodeController::ajaxInitDataDetailV2` — đếm `total_block` (`app/Http/Controllers/Basic/QRCodeController.php`) | Sửa — thêm hint NO_SEMIJOIN | NOT EXISTS tương quan, không dùng được dạng derived table |
| 6 | `ConversationReplicate::advanceFilterPost` — mirror (`app/ConversationReplicate.php`) | KHÔNG đổi | Dùng pluck mảng PHP, không thuộc mẫu NOT IN/NOT EXISTS bị antijoin |

## Tự review (AI, nguyên văn từ Journal #140372)

> Đã rà diff: 5 item web của P1 (trừ item 1 đã ở #42006) đều được xử lý theo khuyến nghị báo cáo; điều kiện lọc giữ nguyên từng chữ, chỉ bọc bảng dẫn xuất DISTINCT hoặc thêm hint. Ngữ nghĩa NOT IN không đổi vì là phép tập hợp, các cột con đều NOT NULL (scenario_lineuser.line_user_id, friend_information_value.line_id, conversion_result.line_user_id) và nhánh Conversation vẫn giữ whereNotNull.

**Rủi ro / lưu ý khi test (Dev tự ghi):**
- Chưa EXPLAIN được trên MySQL 8.0 (dev DB không kết nối — `host.docker.internal:3306 Connection refused`) — **cần DBA/QA chạy EXPLAIN ANALYZE** các câu trên máy B/.25 với bot nhiều dữ liệu để xác nhận plan không còn antijoin/materialize toàn bảng.
- Hint `NO_SEMIJOIN` trong subquery: MySQL 5.7 hỗ trợ (5.7.7+) và không đổi plan; MariaDB coi như comment (nghĩa là test trên MariaDB container KHÔNG kiểm chứng được tác dụng thật của hint này).
- Item 1 nằm ở #42006 — khi merge 2 branch cùng sửa `Conversation.php` nhưng khác vùng dòng, Dev ghi nhận không conflict.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Conversation::advanceFilterPost` — case scenario (`scenario_condition=1` 「現在購読していない」) nhánh AND | `app/Conversation.php:457-459` | Direct | `NOT IN (SELECT DISTINCT … is_deleted = 0 AND line_user_id IS NOT NULL)` — **đã áp quyết định 05/10** (commit `0680a6df61`). **Đổi hành vi**: bạn chỉ có dòng kịch bản đã xoá mềm nay tính là không theo (#42175) |
| F2 | `Conversation::advanceFilterPost` — case scenario nhánh OR | `app/Conversation.php:1156-1158` (orWhereNotIn) | Direct | Như F1 |
| F3 | `Conversation::advanceFilterPost` — thông tin bạn bè `op_compare=3` nhánh AND + OR | `app/Conversation.php:914` (+ OR tương ứng) | Direct | friend_information_value ≥ 50 triệu dòng |
| F4 | `Conversation::distinctDerivedSubquery` (helper mới) | `app/Conversation.php` | Direct (code mới) | Dùng chung cho F1-F3; builder gốc (`$lineUserIdsFriendInfo`) không bị dính DISTINCT sau khi bọc — Dev clone trước khi bọc |
| F5 | `FilterController::ajaxGetListUserFilter` — scenario not_apply (`is_following=1`) + not_done (`is_following=2`) | `app/Http/Controllers/Basic/FilterController.php:396, 416` | Direct | scenario_lineuser 26,4 triệu dòng |
| F6 | `FilterController::ajaxGetListUserFilter` — conversion or_not_filter | `app/Http/Controllers/Basic/FilterController.php:439` | Direct | conversion_result < 5 triệu dòng; nhánh `and_not_filter` (dòng 443, có GROUP BY) KHÔNG đổi |
| F7 | `QRCodeController::ajaxInitDataDetailV2` — đếm `total_block` | `app/Http/Controllers/Basic/QRCodeController.php:2112` | Direct | Thêm hint NO_SEMIJOIN, KHÔNG đổi sang derived table |
| F8 | `ConversationReplicate::advanceFilterPost` — case scenario nhánh AND + OR | `app/ConversationReplicate.php` | Direct (đã sửa ở `0680a6df61`) | Đổi `pluck` mảng PHP sang subquery DISTINCT giống F1; chạy trên kết nối replica. Studio `dev_impact`: không có caller ngoài ⇒ rủi ro thấp |
| F9 | ~27 caller của `Conversation::advanceFilterPost` (giống #42006): Filter/Friendlist/CrossAnalysis/Broadcast(V2)/TalkList/Chat/RichMenu controllers, Api ListFriend/Remind/Mobile Filter, Mobile Calendar(Salon), Helpers/functions (remind), HelperService, CalendarSalonLineBookingService, console export/cross-analysis/recoverShowFilterBroadcast | nhiều file | Indirect | Chỉ đổi hiệu năng/cú pháp SQL, Dev khẳng định kết quả không đổi — layer chứa bug gốc nên vẫn cần TC verify lại |
| F10 | Route `/ajax/filter/get-list-user` dùng chung bởi Tự động trả lời (FA-003, `public/js/reply/filter.js`) | `FilterController` | Indirect | Cùng builder F5/F6, chỉ khác entry point UI |
| F11 | `public/js/friendlist/modal_filter_v2.js` — áp điều kiện ステップ / コンバージョン từ URL (`scenario_search`, `conversion_search`) vào bộ lọc v2 **1 lần** lúc mở 友だちリスト từ 「人が対象」 của màn lọc người nhận cũ (bug con #42170 / #42171) | `public/js/friendlist/modal_filter_v2.js` (+69 dòng) | Direct | File nạp ở ~60 màn, nhưng chỉ friendlist và event_step truyền params thật. **Không bump version asset** ⇒ trình duyệt có thể giữ JS cũ (Dev: hướng dẫn QA Ctrl+F5) |
| F12 | v3 — #42327: chỉ nhận mã kịch bản / tag / chuyển đổi trên URL nếu thuộc LINE OA hiện tại (không lộ tên dữ liệu của OA khác) | `modal_filter_v2.js` / phía server (chưa có diff) | Direct — **đang sửa** | Journal #141352 (D-10) |
| F13 | v3 — #42328: 「購読中」 của bộ lọc v2 thêm `is_deleted = 0` để bù đúng với 「現在購読していない」 (khớp job #42002 / MCP #42005) | `app/Conversation.php` (chưa có diff) | Direct — **đang sửa** | Journal #141352 (D-11). Lỗi do chính nhánh này gây ra: bạn có dòng `is_deleted` NULL/1 đang vừa thuộc 購読中 vừa thuộc 現在購読していない |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `scenario_lineuser`, `friend_information_value`, `bot_line_user`, `conversion_result`, `detail_landing_click` | READ-ONLY | Dev khẳng định "Không có — chỉ đổi dạng câu SELECT, không ghi DB, không migration" |
| D2 | `scenario_lineuser.is_deleted` (cột `tinyint(1) NULL DEFAULT 0`) | READ-ONLY (đổi cách đọc) | Dòng `is_deleted IS NULL` đang theo kịch bản: sau fix bị coi là **không theo**. Dev đề nghị đếm trên prod rồi quyết định backfill `is_deleted = 0` (Journal #140946) |
| D3 | Index `detail_landing_click_bot_line_landing_index` (bot_id, line_id, landing_id) — migration `2026_09_15_103000` (#40997) | Điều kiện deploy | Hint `NO_SEMIJOIN` chỉ có lợi khi có index này; thiếu index thì câu đếm chặn QR **chậm hơn** ⇒ phải `SHOW INDEX` trên prod trước deploy |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend Filter / Segment (SC-003) — điều kiện "không theo kịch bản" và "thông tin bạn bè chưa đăng ký" của bộ lọc bạn bè (dùng ở danh sách bạn bè, broadcast, phân tích chéo, export CSV) | F1, F2, F3, F4 | Medium — quyết định 05/10 yêu cầu thêm `is_deleted=0` (đổi nghiệp vụ nhỏ) nhưng Dev báo giữ nguyên điều kiện ⇒ cần xác nhận + TC kiểm riêng; chưa EXPLAIN được trên MySQL 8.0 thật |
| T2 | Step Delivery / Scenario (FA-009) — lọc người nhận theo kịch bản (không theo / chưa dừng) ở màn lọc người nhận | F5 | Medium — FilterController đã có `is_deleted = 0` từ trước; fix chỉ thêm DISTINCT |
| T3 | Friend Information (FA-015) — lọc bạn bè chưa đăng ký mục thông tin bạn bè | F3, F4 | Medium — bảng friend_information_value lớn nhất trong nhóm (≥50 triệu dòng) |
| T4 | Conversion (FA-025) — lọc người nhận chưa đạt chuyển đổi | F6 | Low — bảng nhỏ (<5 triệu dòng), chỉ đổi SQL thuần không kèm đổi nghiệp vụ |
| T5 | QR Code Action / Landing Page (FA-017) — số người đã chặn ở màn chi tiết thống kê QR/trang đích | F7 | Medium — hint NO_SEMIJOIN không test được trên MariaDB, cần xác nhận hiệu lực thật trên MySQL 8.0 |
| T6 | Tự động trả lời (FA-003) — màn lọc người nhận dùng chung route get-list-user | F10 | Low — chỉ là entry point khác của F5/F6 |
| T7 | Gián tiếp qua `Conversation::advanceFilterPost` (giống #42006): hành động/nhắc lịch theo user (FA-016/FA-022), Rich Menu V2 (FA-004), talk list/chat (FA-002/FA-001), phân tích chéo (FA-024), API lọc app mobile, lịch bài học/salon mobile (FA-019/FA-020) | F9 | Low/Medium — nhiều caller dùng chung builder; nên có ít nhất 1 TC smoke cho mỗi nhóm caller chính sử dụng điều kiện scenario/thông tin bạn bè, không cần lặp toàn bộ ma trận ở từng caller |
| T8 | 友だちリスト mở từ 「人が対象」 của màn lọc người nhận cũ (broadcast cũ, 自動応答 cũ) + các màn nạp `modal_filter_v2.js` (event_step truyền params thật) | F11, F12 | Medium — JS không bump version; lộ dữ liệu OA khác (#42327) |
| T9 | Đồng bộ số đếm 「現在購読していない」 / 「購読中」 giữa web, job #42002, MCP #42005 cho cùng bot / kịch bản | F1, F2, F13 | Medium — Dev khuyến nghị deploy gần nhau |

---

## 4b. Điều kiện deploy + đo hiệu năng (Dev handoff #140946)

- Trước deploy: `SHOW INDEX FROM detail_landing_click` trên prod phải có `detail_landing_click_bot_line_landing_index`; thiếu thì chạy migration `2026_09_15_103000_add_index_for_delete_friend_landing_cleanup` trước.
- Đo trên MySQL 8 dữ liệu thật (.152 / .25): chạy `docs/measure/explain-42000.sql` mỗi câu 2 lần — **câu lọc < 1 s, câu đếm chặn QR < 4 s**, plan câu QR có hint không còn `Hash antijoin` + `Table scan` trên bảng click. Người chạy: TuanPA.
- Đếm prod `scenario_lineuser` có `is_following = 1 AND is_deleted IS NULL` → quyết định backfill.
- Bug con #42173, #42293 → #42297: cho kết quả giống hệt nhánh gốc (lỗi có sẵn) — cần quyết định xử lý ở ticket riêng.

## 5. Recover data

✔ Không cần recover data (Dev xác nhận — chỉ đổi dạng câu SELECT, không ghi DB).

## 6. Verify (Dev tự làm — chưa phải EXPLAIN thật trên MySQL 8.0)

- **Mức:** lint.
- **Lệnh:** `php -l` 3 file — No syntax errors.
- **MariaDB 10.11 dựng tạm trong container + dữ liệu giả** (trùng dòng, value rỗng/NULL, line_id NULL, nhiều bot/kịch bản/mục): Laravel 5.5 builder sinh SQL đúng dạng `not in (select alias.col from (select distinct ...) as alias)` + bindings đúng thứ tự; kết quả cũ vs mới **GIỐNG HỆT** ở 6 tổ hợp kịch bản (AND + nhóm OR), 4 tổ hợp thông tin bạn bè, 6 tổ hợp màn lọc kịch bản, 3 tổ hợp chuyển đổi, 4 tổ hợp đếm chặn QR có hint.
- Builder gốc `$lineUserIdsFriendInfo` không bị dính DISTINCT sau khi bọc (helper clone trước).
- **EXPLAIN MySQL 8.0: KHÔNG chạy được** (MySQL dev `host.docker.internal:3306` Connection refused; container chỉ có MariaDB, không có antijoin) ⚠️.
- **Bằng chứng gián tiếp:** cùng dạng bảng dẫn xuất SELECT DISTINCT đã đo ở item 1 (#42006): 5.7 ~7s / 8.0 ~50s → 0,1–0,5s cả 2 bản. Tài liệu MySQL 8.0 (semijoins.html): cờ semijoin "Starting with MySQL 8.0.17, this also applies to antijoins" — hint NO_SEMIJOIN là bản theo-subquery của cờ này.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ **Đặc biệt:** đã quyết định có cần EXPLAIN thật trên MySQL 8.0 (máy B/.25) trước khi release hay chấp nhận verify chỉ bằng MariaDB — Dev tự nhận chưa làm được bước này
