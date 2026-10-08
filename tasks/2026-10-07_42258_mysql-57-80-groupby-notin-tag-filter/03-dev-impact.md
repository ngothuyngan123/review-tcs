# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Ticket #42258 gộp **3 task con**, mỗi task có khối "Đánh giá ảnh hưởng của DEV" riêng (nguyên văn, cùng Dev, cùng ngày 2026-10-06, cùng branch). File này giữ cấu trúc 4 mục chuẩn nhưng **đánh dấu `[A]`/`[B]`/`[C]`** ở đầu mỗi dòng để biết thuộc task con nào — dùng khi trace ngược:
> - `[A]` = #41997 [JOB-R1] GROUP BY không tự sắp xếp
> - `[B]` = #42002 [JOB-P1] NOT EXISTS/NOT IN antijoin
> - `[C]` = #42014 [JOB] Bộ lọc tag "có tag" → IN (subquery)

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | `[A]` 208983f · `[B]` 45fce05 · `[C]` 1515afc + 1db73cf |
| Branch | `m_202610_mysql_update_80_39528` (chung cho cả 3) |
| Ngày submit đánh giá | 2026-10-06 (journal #140575 `[A]`, #140576 `[B]`, #140577 `[C]`) |
| Auto-filled | 2026-10-07 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact) cho **cả 3 phần A/B/C**.

---

## 1. Nguyên nhân

**[A]** MySQL 8 bỏ sort ngầm theo cột `GROUP BY`. Danh sách người nhận lấy với `orderByBotLineUser = false` không còn thứ tự cố định → resume broadcast (`BroadcastNewJob` dò vị trí người nhận cuối rồi gửi tiếp phía sau) có thể gửi lặp/bỏ sót; thứ tự hàng phân tích chéo bị đổi.

**[B]** MySQL 8.0.17+ biến `NOT IN (subquery)` trên `scenario_lineuser.line_user_id` / `friend_information_value.line_id` (cột NOT NULL) thành antijoin + materialize bảng con → query lọc "không theo kịch bản", "chưa xong kịch bản", "thông tin bạn bè chưa đăng ký" có thể chậm từ < 1s lên hàng chục–trăm giây.
Note bổ sung 05/10: nhánh "không có tag" thiếu `line_user_id IS NOT NULL` → tag có dòng NULL (production có 22 dòng) làm filter trả 0 người, lệch với số đếm trên web.

**[C]** Điều kiện "có tag" dạng `(SELECT COUNT … tương quan) > 0` duyệt từng bạn bè (bot 97640 ~20 triệu dòng `tag_line_user`, 16–125s), chiếm ~48% thời gian query chậm DB B.

## 2. Cách fix

**[A]** Khi `orderByBotLineUser = false`, thêm `ORDER BY line_user.id ASC` (đúng thứ tự 5.7 ngầm trả về) ở `getListLineUserFromFilter` và `getListLineUserFromFilterV2`; nhánh `true` giữ `ORDER BY bot_line_user.id`.

**[B]** Viết lại 18 subquery `NOT IN` thành `NOT IN (SELECT DISTINCT col … AND col IS NOT NULL)` theo hướng đã đo. Kết quả không đổi vì 2 cột đều NOT NULL, không thêm tham số bind.
Áp cho nhánh lọc kịch bản ("không đang theo" `is_following=1`, "chưa hoàn thành" `is_following=2`): dạng chuẩn CUỐI (sau đính chính 05/10) = `x NOT IN (SELECT DISTINCT line_user_id FROM scenario_lineuser WHERE scenario_id = ? AND is_following = <1|2> AND is_deleted = 0 AND line_user_id IS NOT NULL)` — commit `45fce05` đã đúng dạng này, giữ nguyên, KHÔNG bỏ `IS NOT NULL`.

**[C]** "Có tag" (V2 nhóm AND + OR, nhánh `lineId == null`) đổi sang `line_user.id IN (SUB)`; "không có tag" (V1, V2 nhóm AND/OR, `isValidFilter`) dùng `NOT IN (SUB)` với cùng `SUB = SELECT DISTINCT line_user_id … tag_id IN (…) AND line_user_id IS NOT NULL`. Nhánh "không có tất cả tag" (`NOT IN … GROUP BY HAVING`) cũng thêm `line_user_id IS NOT NULL`.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 `[A]` | `LineUserModel.getListLineUserFromFilter` (PrepareTemplateTask, AppMain.testFilter) | Không đổi signature | Không phải sửa caller — chỉ nhận thêm thứ tự cố định |
| 2 `[A]` | `LineUserModel.getListLineUserFromFilterV2` (11 callsite: BroadcastNewJob×4, FilterService, ActionScheduleBotTask, HandleCrossAnalysis×2, HandleExportCsvTask, HandleExportCsvChat11Task, SettingDisplayRichMenuHistoriesThread) | Không đổi signature | `HandleExportCsvTask` truyền `orderByBotLineUser=true` nên không đổi; caller còn lại xử lý cả danh sách, chỉ nhận thêm thứ tự |
| 3 `[B]` | `LineUserModel.getListLineUserFromFilter` / `getListLineUserFromFilterV2` (broadcast, action schedule, rich menu, CSV, phân tích chéo, prepare template) | Không đổi signature | Đổi câu SELECT trên `scenario_lineuser`/`friend_information_value` |
| 4 `[B]` | `LineUserModel.isValidFilterV2` (gọi `buildWhereFilter`/`buildWhereORFilter` cho từng bạn bè) | Chỉ nhánh `lineId` bị đổi | Áp dụng cho "chưa xong kịch bản" và "thông tin bạn bè chưa đăng ký" |
| 5 `[B]` | `LineUserModel.isValidFilter` (HandlePostbackTask, auto reply bộ lọc cũ) | Không đổi signature | — |
| 6 `[C]` | `LineUserModel.getListLineUserFromFilter` / `getListLineUserFromFilterV2` (broadcast, action schedule, rich menu, CSV, phân tích chéo, prepare template) | Không đổi signature | Đổi câu SELECT trên `tag_line_user` |
| 7 `[C]` | `LineUserModel.isValidFilter` (HandlePostbackTask, auto reply bộ lọc cũ) | Không đổi signature | `isValidFilterV2` KHÔNG bị ảnh hưởng — mọi thay đổi nằm ở nhánh `lineId == null`; builder không sinh `NOT(…)` nên dòng `line_user_id NULL` không đổi kết quả "có tag" |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 `[A]` | `LineUserModel.getListLineUserFromFilter` | LineUserModel.java | Direct | Thêm ORDER BY khi `orderByBotLineUser=false` |
| F2 `[A]` | `LineUserModel.getListLineUserFromFilterV2` | LineUserModel.java | Direct | 11 callsite — dùng cho broadcast, action schedule, rich menu, CSV, phân tích chéo |
| F3 `[B]` | `LineUserModel.getListLineUserFromFilter` (bộ lọc cũ) | LineUserModel.java | Direct | NOT IN trên `scenario_lineuser`/`friend_information_value` |
| F4 `[B]` | `LineUserModel.buildWhereFilter`, `LineUserModel.buildWhereORFilter` | LineUserModel.java | Direct | Dùng chung cho `getListLineUserFromFilterV2` và `isValidFilterV2` |
| F5 `[B]` | `LineUserModel.isValidFilter` | LineUserModel.java | Direct | HandlePostbackTask, auto reply bộ lọc cũ |
| F6 `[C]` | `LineUserModel.getListLineUserFromFilter` (bộ lọc cũ — không có tag, không có tất cả tag) | LineUserModel.java | Direct | Dòng 517, 1301 (buildWhereFilter/OR) — "có tag" → IN |
| F7 `[C]` | `LineUserModel.buildWhereFilter`, `LineUserModel.buildWhereORFilter` (có tag, không có tag, không có tất cả tag) | LineUserModel.java | Direct | Cùng hàm với F4 — 2 task con cùng sửa 1 hàm |
| F8 `[C]` | `LineUserModel.isValidFilter` (không có tag, không có tất cả tag) | LineUserModel.java | Direct | — |
| F9 `[A][B][C]` | `LineUserModel.isValidFilterV2` | LineUserModel.java | Indirect (không đổi code, chỉ đổi dữ liệu nhánh con gọi) | Kiểm 1 bạn bè — nhánh `lineId != null` giữ nguyên COUNT, không bị 3 task con sửa trực tiếp |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(không có record nào bị tạo/sửa/xoá)* | — | Cả 3 phần A/B/C **chỉ đổi câu SQL SELECT sinh ra** (thêm ORDER BY / đổi NOT IN / đổi COUNT→IN), **không** CREATE/UPDATE/DELETE/MIGRATE dữ liệu nào trong `line_user`, `bot_line_user`, `tag_line_user`, `scenario_lineuser`, `friend_information_value` |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 `[A]` | Broadcast (`broadcast`, `filters_v2` parent_type=`broadcast`) — dừng job giữa chừng rồi khởi động lại | F1, F2 | High — bug gửi lặp/bỏ sót tin cho khách nếu fix sai |
| T2 `[A]` | Phân tích chéo (`cross_analysis`, parent_type=`cross_analysis`) — thứ tự hàng theo thông tin cơ bản | F2 | Medium — sai hiển thị, không gửi tin khách |
| T3 `[A]` | Action schedule (`action_schedules`), rich menu theo bộ lọc (`setting_display_rich_menu_histories`), CSV chat 1:1 (`history_export_csv_chat11`), chuẩn bị template broadcast (`broadcast`, bảng `filters`) | F2 | Low — Dev nói "số người nhận không đổi so với trước" (⚠️ cần TC verify theo quy tắc nghiệp vụ, không chỉ tin "bất biến") |
| T4 `[A]` | Hiệu năng job lọc người nhận | F1, F2 | Low — Dev nói "không chậm hơn bản cũ" |
| T5 `[B]` | Lọc người nhận: broadcast, action schedule, rich menu theo bộ lọc, export CSV, phân tích chéo, chuẩn bị template — điều kiện "không theo kịch bản"/"chưa xong kịch bản"/"thông tin bạn bè chưa đăng ký" | F3, F4 | High — so số người nhận job với số đếm trên màn lọc web |
| T6 `[B]` | Kiểm filter từng bạn bè "chưa xong kịch bản"/"chưa đăng ký": step kịch bản (`step_message`, `filter_manager`), action (`t_actions` parent_type=`modal_action`), auto reply (`auto_reply`, `filters_v2`+`filters`), chuyển rich menu (`richmenu_switch_item`), nhắc sự kiện (`event_step`) | F4 | Medium |
| T7 `[B]` | Hiệu năng DB B — EXPLAIN FORMAT=TREE không còn Materialize cho NOT IN | F3, F4 | Low |
| T8 `[C]` | Lọc danh sách người nhận theo tag (có tag/không có tag/không có tất cả tag, nhóm AND/OR, 2 điều kiện AND, ~2.700 tag, ca tag NULL): broadcast, action schedule, rich menu theo bộ lọc, export CSV, phân tích chéo, chuẩn bị template broadcast | F6, F7, F8 | High — so số người nhận job với số đếm trên màn lọc web |
| T9 `[C]` | Auto reply dùng bộ lọc cũ (`auto_reply`, bảng `filters`) — "không có tag"/"không có tất cả tag" | F8 | Medium |
| T10 `[C]` | Hiệu năng DB B — Q017 ≤1s, Q005 ≤5s, Q002 ≤40s; EXPLAIN không còn subquery dependent cho tag | F6, F7 | Low |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ Đặc biệt soát lại các dòng "Dev nói bất biến" (T3, T4, T7, T10) — theo RULE-05 (5 câu hỏi adversarial của `/review-tc` BƯỚC 2), nhánh "bất biến" phải có TC expected theo **quy tắc nghiệp vụ** (vd so số người nhận job với số đếm trên web), không chỉ tin lời Dev
