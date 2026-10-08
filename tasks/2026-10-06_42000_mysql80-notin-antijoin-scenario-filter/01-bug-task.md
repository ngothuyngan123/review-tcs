# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42000 — [WEB-P1] Nâng MySQL 5.7 → 8.0: NOT EXISTS / NOT IN (subquery) bị đổi thành antijoin rồi materialize cả bảng con` |
| Module / Màn hình | 5 vị trí trên web (sns-line): (1) Bộ lọc bạn bè (`advanceFilterPost`) nhánh "không theo kịch bản" (`scenario_condition=1`) + nhánh "thông tin bạn bè chưa đăng ký" (`op_compare=3`); (2) Màn lọc người nhận (`ajax/filter/get-list-user`) nhánh "không theo kịch bản" / "kịch bản chưa dừng" + nhánh "chưa đạt conversion"; (3) Thống kê QR/landing — đếm người đã chặn (`ajaxInitDataDetailV2`). Xem danh sách function/caller đầy đủ ở `03-dev-impact.md` mục 3/4.1. (Nhánh QR "chưa quét" — item 1 của luận điểm P1 — đã tách xử lý riêng ở ticket `#42006`, KHÔNG thuộc phạm vi ticket này.) |

## Mô tả bug (bản dịch tiếng Việt)

Luận điểm P1 — NOT EXISTS / NOT IN (subquery) bị đổi thành antijoin rồi materialize cả bảng con. Project: sns-line (web Laravel).
Nguồn: báo cáo đối chiếu MySQL 8 — https://dashboard.melonglobal.net/fixbug-lme/mysql80-report/#perf/P1 · ticket gốc #39528
Code đối chiếu: release_step_20260930_v2 @441407307e · Máy B: MySQL 8.0.46-0ubuntu0.22.04.4

**1. Mô tả luận điểm**

*Thay đổi 5.7 → 8.0:* 5.7: NOT EXISTS / NOT IN luôn chạy như subquery phụ thuộc — với từng dòng ngoài, tra index bảng con rồi dừng ở dòng khớp đầu tiên, nên chi phí tỉ lệ với số dòng ngoài (vài chục → vài nghìn user). 8.0.17+: optimizer được phép biến chúng thành ANTIJOIN và chọn chiến lược materialization — dựng "danh sách đen" bằng cách đọc TOÀN BỘ dòng bảng con khớp điều kiện (với tag_line_user là quét ~178 triệu dòng) rồi mới loại trừ. Chi phí chuyển sang tỉ lệ với kích thước bảng con, không còn phụ thuộc số user cần xét.

*Điều kiện kích hoạt:* NOT EXISTS (luôn đủ điều kiện) hoặc NOT IN (SELECT …) khi cả 2 vế NOT NULL; bảng con lớn; nằm ở mức AND của WHERE (dưới OR thì không chuyển). Plan còn KHÔNG ỔN ĐỊNH: cùng bot, cùng điều kiện, lượt trước 746 dòng, lượt sau 178 triệu dòng (item 03 — thuộc #42006).

*Tác động:* Chậm từ < 1 s lên hàng chục–hàng trăm giây; giữ connection, chồng tải khi client retry.

**2. Các item thuộc phạm vi ticket này (5/6 — item 1 "QR chưa quét" đã tách sang #42006)**

| # | Ưu tiên | Logic / tính năng | Vị trí | Bảng dữ liệu (B) |
|---|---|---|---|---|
| 2 | Cao | Bộ lọc bạn bè — nhánh thông tin bạn bè "chưa đăng ký" (op_compare = 3) | app/Conversation.php:914 | friend_information_value 50.989.021 dòng (6,8 GiB); bot_line_user 49.987.580 dòng (17,8 GiB) |
| 3 | Trung bình | Màn lọc người nhận — "không theo kịch bản" / "kịch bản đã dừng" | app/Http/Controllers/Basic/FilterController.php:396 | scenario_lineuser 26.385.876 dòng (5,0 GiB); line_user 62.044.908 dòng (19,0 GiB) |
| 4 | Trung bình | Bộ lọc bạn bè — nhánh "không theo kịch bản" (scenario_condition = 1) | app/Conversation.php:458 | scenario_lineuser 26.385.876 dòng (5,0 GiB); bot_line_user 49.987.580 dòng (17,8 GiB) |
| 5 | Trung bình | Thống kê QR/landing — đếm người đã chặn | app/Http/Controllers/Basic/QRCodeController.php:2112 | detail_landing_click 31.320.190 dòng (18,8 GiB) |
| 6 | Thấp | Màn lọc người nhận — "chưa đạt conversion" | app/Http/Controllers/Basic/FilterController.php:439 | conversion_result 140.764 dòng (18,1 MiB) |

*Kết luận riêng từng item (lúc báo cáo — trước fix):*

- **Item 2** — `app/Conversation.php:914` — Rủi ro (code khớp điều kiện) · Ưu tiên Cao — Bảng bị quét friend_information_value ≥ 50 triệu dòng. `whereNotIn(…, <subquery friend_information_value>)` — `line_id` NOT NULL ⇒ đủ điều kiện antijoin trên bảng friend_information_value (lớn).
- **Item 3** — `app/Http/Controllers/Basic/FilterController.php:396` — Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Bảng bị quét scenario_lineuser 5–50 triệu dòng. `line_user.id NOT IN (SELECT line_user_id FROM scenario_lineuser …)` — cả 2 vế NOT NULL ⇒ đủ điều kiện antijoin.
- **Item 4** — `app/Conversation.php:458` — Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Bảng bị quét scenario_lineuser 5–50 triệu dòng. `whereNotIn(bot_line_user.line_user_id, <subquery scenario_lineuser>)` — cả 2 cột NOT NULL ⇒ đủ điều kiện antijoin; scenario lớn có hàng trăm nghìn dòng. Chưa có EXPLAIN lúc báo cáo.
- **Item 5** — `app/Http/Controllers/Basic/QRCodeController.php:2112` — Rủi ro (code khớp điều kiện) · Ưu tiên Trung bình — Bảng bị quét detail_landing_click 5–50 triệu dòng. `whereNotExists` tương quan trên detail_landing_click (tự join chính nó) — NOT EXISTS luôn đủ điều kiện antijoin.
- **Item 6** — `app/Http/Controllers/Basic/FilterController.php:439` — Rủi ro (code khớp điều kiện) · Ưu tiên Thấp — Bảng bị quét conversion_result < 5 triệu dòng. `NOT IN (SELECT DISTINCT line_user_id FROM conversion_result …)` — NOT NULL ⇒ đủ điều kiện antijoin. Dòng 443 (nhánh and_not_filter) có GROUP BY nên KHÔNG chuyển, không thuộc phạm vi fix.

⚠️ Khác với item 1 (#42006, có slow log THỰC TẾ đo được 7s→50s), **5 item trong ticket này ở trạng thái "Rủi ro" lúc báo cáo** (code khớp điều kiện kích hoạt antijoin nhưng chưa có đo thực tế/EXPLAIN trên MySQL 8.0) — xem thêm cảnh báo verify ở `03-dev-impact.md` mục 6 (Dev KHÔNG EXPLAIN được trên MySQL 8.0, chỉ test bằng MariaDB + so sánh builder SQL sinh ra).

**3. Hướng xử lý (theo báo cáo ban đầu + quyết định chốt ở journal)**

Dùng `x NOT IN (SELECT DISTINCT col FROM … WHERE … AND col IS NOT NULL)` (đã đo nhanh nhất ở item 1). KHÔNG viết lại sang NOT EXISTS / LEFT JOIN … IS NULL. Chữa cháy: hint `/*+ SET_VAR(optimizer_switch='materialization=off') */` cho đúng câu.

Quyết định chốt riêng cho nhánh **scenario** (items 3, 4 — xem Journal #140262 dưới): thống nhất dạng SQL dùng chung cho `Conversation.php` (nhánh AND + OR) + `ConversationReplicate.php` + `FilterController.php`:
```
x NOT IN (SELECT DISTINCT line_user_id FROM scenario_lineuser WHERE scenario_id = ? AND is_following = <1|2> AND is_deleted = 0 AND line_user_id IS NOT NULL)
```

## Steps to reproduce

<!-- Ticket không có section "Tái hiện bug" — đây là ticket phân tích/perf audit từ việc đối chiếu MySQL 5.7 vs 8.0 khi migration, không phải bug khách hàng report trực tiếp. 5 item trong phạm vi ticket này ở trạng thái "Rủi ro" (code khớp điều kiện kích hoạt antijoin), KHÔNG có slow log thực tế đo được tại thời điểm báo cáo (khác với item 1 ở #42006). -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Không có attachment đính kèm trên Redmine (0). Bằng chứng/nguồn tham chiếu trong mô tả:
- Dashboard báo cáo: https://dashboard.melonglobal.net/fixbug-lme/mysql80-report/#perf/P1
- Dashboard review quyết định scenario: https://dashboard.melonglobal.net/fixbug-lme/mysql80-review/#features/F3
- Dashboard fixbug (xử lý AI): https://dashboard.melonglobal.net/implement-task-small-lme/?id=42000

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine theo nghĩa thông thường** — đây là ticket performance audit (5 item ở mức "Rủi ro", không phải "Đã xảy ra" như item 1 #42006). Root cause + cách fix đã được Dev xác nhận qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **2 trục**: (a) kết quả lọc/đếm KHÔNG đổi trước/sau fix (chỉ đổi dạng SQL, không đổi ngữ nghĩa điều kiện), (b) thời gian chạy trên MySQL 8.0 cải thiện với bảng lớn (chỉ đo được trên môi trường có data quy mô lớn thật — RULE-08, không kết luận từ local/staging nhỏ).
- Status Redmine hiện tại: **Fix done - Đợi test**. Priority: **High**. Tracker "Improve nội bộ". Tác giả + người fix đều là hệ thống **AI LME Fix bug** (auto-fixbug), assignee: Ngô Thúy Ngần.
- **Dev tự nhận chưa EXPLAIN được trên MySQL 8.0** (DB dev không kết nối được lúc fix — `host.docker.internal:3306 Connection refused`; verify chỉ làm trên MariaDB 10.11 container, không có antijoin) — khuyến nghị QA/DBA chạy EXPLAIN ANALYZE thật trên máy B/.25 với bot nhiều dữ liệu trước khi release. Xem mục 6 (VERIFY) + "Rủi ro/lưu ý khi test" ở `03-dev-impact.md`.
- **Quyết định 05/10 (Journal #140262) yêu cầu đổi nghiệp vụ nhỏ**: nhánh scenario của bộ lọc bạn bè (`Conversation.php`) thêm `is_deleted = 0` cho khớp dạng chung 3 repo. ⚠️ Nhưng báo cáo fix (Journal #140372) ghi "giữ nguyên điều kiện lọc từng chữ" ⇒ **chưa xác nhận quyết định đã được áp vào code** — cần Dev xác nhận; TC kiểm riêng điểm này.
- Route `get-list-user` (màn lọc người nhận) dùng chung bởi nhiều màn hình (Tự động trả lời FA-003, lọc người nhận broadcast, …) — xem đủ danh sách caller/tính năng liên quan ở `03-dev-impact.md` mục 4.3.

## Journal / note từ Redmine (nguyên văn)

**Journal #139939 — AI LME Fix bug — 2026-10-03:**

```
Item "Bộ lọc bạn bè — nhánh QR chưa quét" (app/Conversation.php:537) đã xảy ra thật trong slow log MySQL 8.0: 5.7 ~7 s → 8.0 ~50 s; bọc subquery detail_landing_click thành bảng dẫn xuất SELECT DISTINCT thì cả 2 bản còn 0,1-0,5 s. Tách task riêng: #42006.
```

**Journal #140256 — AI LME Fix bug — 2026-10-05:**

```
h3. Quyết định đã chốt (05/10/2026) — lọc bạn bè theo kịch bản: thống nhất 3 repo về MỘT dạng

<pre>
x NOT IN (SELECT DISTINCT line_user_id FROM scenario_lineuser WHERE scenario_id = ? AND is_following = <1|2> AND is_deleted = 0)
</pre>

* Áp cho 2 nhánh: *"KHÔNG đang theo kịch bản"* (@is_following = 1@) và *"CHƯA hoàn thành kịch bản"* (@is_following = 2@).
* Có @DISTINCT@, có @is_deleted = 0@, *KHÔNG* thêm @line_user_id IS NOT NULL@ (@scenario_lineuser.line_user_id@ là NOT NULL nên không cần).
* Lý do thống nhất: hiện 3 repo đang có 4 cách viết khác nhau cho cùng một nghiệp vụ (job từ 2018 dùng NOT IN, MCP 04/2026 dùng NOT EXISTS, web có 2 bản — FilterController chép nguyên văn câu của job, Conversation viết riêng và không lọc is_deleted).
* Khuyến nghị giữ: chạy EXPLAIN FORMAT=TREE trên máy .152 với kịch bản có nhiều người nhất trước khi release (với cột NOT NULL, MySQL 8.0 vẫn có thể đổi NOT IN thành antijoin).
* Chi tiết so sánh: https://dashboard.melonglobal.net/fixbug-lme/mysql80-review/#features/F3

h3. Yêu cầu cho web (sns-line) — 2 bản cần đổi theo dạng chung

|_. Tính năng |_. Vị trí (release_step_20260930_v2) |_. Hiện tại |_. Yêu cầu |
| Bộ lọc bạn bè (advanceFilterPost) — nhóm AND | app/Conversation.php:457-458 | @whereNotIn(bot_line_user.line_user_id, scenario_lineuser where scenario_id, bot_id, is_following = 1, whereNotNull(line_user_id))@ — không DISTINCT, không lọc is_deleted | Đổi theo dạng chung: thêm DISTINCT + @is_deleted = 0@, bỏ @whereNotNull@ |
| Bộ lọc bạn bè — nhóm OR | app/Conversation.php:1154-1155 | như trên (@orWhereNotIn@) | như trên |
| Bản sao | app/ConversationReplicate.php (cùng 2 nhánh) | như trên | Giữ đồng bộ với Conversation.php |
| Màn lọc người nhận (POST /ajax/filter/get-list-user) | app/Http/Controllers/Basic/FilterController.php:396, 416 | @line_user.id NOT IN (SELECT line_user_id FROM scenario_lineuser WHERE scenario_id = ? AND is_following = 1/2 AND is_deleted = 0)@ | Thêm @DISTINCT@ |

* Lưu ý: comment #39667 ở Conversation.php ghi "whereNotNull BẮT BUỘC" — không còn đúng với bảng này vì cột line_user_id NOT NULL; bỏ được theo quyết định trên.
* Thêm @is_deleted = 0@ là đổi nghiệp vụ nhỏ cho khớp job / MCP / FilterController: chưa thấy code web/job ghi @is_deleted = 1@, chỉ ảnh hưởng dữ liệu cũ nếu có (@SELECT is_deleted, COUNT(*) FROM scenario_lineuser GROUP BY is_deleted@).
```

**Journal #140262 — AI LME Fix bug — 2026-10-05:**

```
h3. ĐÍNH CHÍNH quyết định lọc kịch bản (05/10/2026) — thay cho ghi chú ngay trước

Quyết định cuối: *GIỮ* @line_user_id IS NOT NULL@. Dạng chung cho 3 repo:

<pre>
x NOT IN (SELECT DISTINCT line_user_id FROM scenario_lineuser WHERE scenario_id = ? AND is_following = <1|2> AND is_deleted = 0 AND line_user_id IS NOT NULL)
</pre>

* Áp cho 2 nhánh "KHÔNG đang theo kịch bản" (@is_following = 1@) và "CHƯA hoàn thành kịch bản" (@is_following = 2@): có DISTINCT, có @is_deleted = 0@, có @IS NOT NULL@ — cùng khuôn với bộ lọc tag.
* Phần "bỏ IS NOT NULL" ở ghi chú trước *không còn hiệu lực*.
* Chi tiết: https://dashboard.melonglobal.net/fixbug-lme/mysql80-review/#features/F3

h3. Yêu cầu cho web (thay bảng ở ghi chú trước)

|_. Tính năng |_. Vị trí |_. Yêu cầu |
| Bộ lọc bạn bè — nhóm AND | app/Conversation.php:457-458 | Thêm DISTINCT + @is_deleted = 0@, *giữ* @whereNotNull(line_user_id)@ |
| Bộ lọc bạn bè — nhóm OR | app/Conversation.php:1154-1155 | như trên |
| Bản sao | app/ConversationReplicate.php (cùng 2 nhánh) | Giữ đồng bộ với Conversation.php |
| Màn lọc người nhận | app/Http/Controllers/Basic/FilterController.php:396, 416 | Thêm @DISTINCT@ và @AND line_user_id IS NOT NULL@ |
```

**Journal #140372 — AI LME Fix bug — 2026-10-06:** (nội dung đầy đủ, đã parse vào `03-dev-impact.md`)

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin.
════════════════════════════════════════════════
Xem chi tiết 6 mục (Nguyên nhân / Cách fix / Caller đã check / Đánh giá ảnh hưởng / Recover data / Verify) tại 03-dev-impact.md.
BRANCH: sns-line — ai_small_42000 (base release_step_20260930_v2, commit 1fa403244d, 3 file) [đã push]
Thời gian AI xử lý: 6 phút 22 giây
Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=42000
```
