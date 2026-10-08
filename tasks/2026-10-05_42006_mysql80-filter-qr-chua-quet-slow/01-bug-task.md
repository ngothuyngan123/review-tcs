# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42006 — [WEB-P1] Nâng MySQL 5.7 → 8.0: Bộ lọc bạn bè nhánh QR "chưa quét" — NOT IN detail_landing_click chậm ~7 s (5.7) → ~50 s (8.0)` |
| Module / Màn hình | Bộ lọc bạn bè (`advanceFilterPost`) — nhánh điều kiện QR `qr_condition = 2` ("chưa quét QR / chưa kết bạn qua landing"), dùng chung bởi 友だちリスト, トークリスト, 一斉配信, phân tích chéo, xuất CSV bạn bè, rich menu theo bộ lọc... (xem danh sách caller ở `03-dev-impact.md` mục 3/4.1) |

## Mô tả bug (bản dịch tiếng Việt)

Luận điểm P1 — NOT EXISTS / NOT IN (subquery) bị đổi thành antijoin rồi materialize cả bảng con. Project: sns-line (web Laravel). Sự cố THỰC TẾ trong slow log MySQL 8.0 — thuộc item "Bộ lọc bạn bè — nhánh QR chưa quét" của #42000 (WEB-P1), tách task riêng vì đã xảy ra và đã có query đo được. Ticket gốc #39528.
Nguồn: https://dashboard.melonglobal.net/fixbug-lme/mysql80-report/#perf/P1 · Máy B: MySQL 8.0.46-0ubuntu0.22.04.4

**1. Sự cố thực tế**

- Tính năng: bộ lọc bạn bè (`advanceFilterPost`) — đếm số bạn bè khớp điều kiện "không có tag …" **và** "chưa quét QR / chưa kết bạn qua landing 524457" (`qr_condition = 2`), bot 126066.
- Cùng một câu: **MySQL 5.7 ~7 s, MySQL 8.0 ~50 s** (slow log 8.0).
- Phần gây chậm: điều kiện `line_user.line_id NOT IN (SELECT detail_landing_click.line_id …)` — subquery KHÔNG có DISTINCT trên bảng click `detail_landing_click` (~31,3 triệu dòng · 18,8 GiB trên máy B; 1 người có nhiều dòng click). Phần NOT IN trên `tag_line_user` giữ nguyên ở cả 2 câu.
- Đổi subquery này thành bảng dẫn xuất `SELECT DISTINCT …` (câu tối ưu bên dưới) ⇒ **cả 5.7 và 8.0 đều còn 0,1–0,5 s**, kết quả không đổi.
- Nguồn gốc code: nhánh này được #39121 (commit 4c10d81570, 07/2026) đổi từ subquery đếm tương quan sang IN / NOT IN để chạy nhanh trên 5.7.

**2. Mô tả luận điểm**

- Thay đổi 5.7 → 8.0: 5.7: NOT EXISTS / NOT IN luôn chạy như subquery phụ thuộc — với từng dòng ngoài, tra index bảng con rồi dừng ở dòng khớp đầu tiên, nên chi phí tỉ lệ với số dòng ngoài (vài chục → vài nghìn user). 8.0.17+: optimizer được phép biến chúng thành ANTIJOIN và chọn chiến lược materialization — dựng "danh sách đen" bằng cách đọc TOÀN BỘ dòng bảng con khớp điều kiện (với `tag_line_user` là quét ~178 triệu dòng) rồi mới loại trừ. Chi phí chuyển sang tỉ lệ với kích thước bảng con, không còn phụ thuộc số user cần xét.
- Điều kiện kích hoạt: NOT EXISTS (luôn đủ điều kiện) hoặc NOT IN (SELECT …) khi cả 2 vế NOT NULL; bảng con lớn; nằm ở mức AND của WHERE (dưới OR thì không chuyển). Plan còn KHÔNG ỔN ĐỊNH: cùng bot, cùng điều kiện, lượt trước 746 dòng, lượt sau 178 triệu dòng.
- Tác động: Chậm từ < 1 s lên hàng chục–hàng trăm giây; giữ connection, chồng tải khi client retry.
- Bằng chứng: Slow log 8.0 (03/10): lọc QR "chưa quét" của bộ lọc bạn bè web 5.7 ~7 s → 8.0 ~50 s, bọc DISTINCT bằng bảng dẫn xuất còn 0,1–0,5 s ở cả 2 bản. Slow log máy B: 7/8 nhóm "B chậm hơn A" thuộc luận điểm này — U001 712 s (178.323.108 dòng), U002 378 s, U008 167 s cho 151 user, U009 167 s cho 78 user, Q10 37,5 s (A 8,7 s), Q12 31,8 s (A 9,3 s), W0 sự cố 24/09. Đo trên máy .25: viết lại `NOT IN (SELECT DISTINCT … AND col IS NOT NULL)` còn 0,1–0,3 s / 1–4 ms.

**Query gốc (slow log):**

```sql
select count(*) as aggregate from `bot_line_user` inner join `line_user` on `line_user`.`id` = `bot_line_user`.`line_user_id` and `bot_line_user`.`bot_id` = 126066
where `bot_line_user`.`bot_id` = 126066 and `bot_line_user`.`is_blocked` = 0
  and ((bot_line_user.line_user_id NOT IN (select distinct tag_line_user.line_user_id from tag_line_user
          where tag_line_user.tag_id IN (2207112,2167388,2043744,2023981,1731547,1731544,2458442) and tag_line_user.line_user_id is not null)
  and line_user.line_id not in (select detail_landing_click.line_id from detail_landing_click
          where detail_landing_click.landing_id in (524457) and detail_landing_click.line_id is not null and action=2)));
```

**Query đã tối ưu (đã đo 0,1–0,5 s trên cả 5.7 và 8.0):**

```sql
select count(*) as aggregate from `bot_line_user` inner join `line_user` on `line_user`.`id` = `bot_line_user`.`line_user_id` and `bot_line_user`.`bot_id` = 126066
where `bot_line_user`.`bot_id` = 126066 and `bot_line_user`.`is_blocked` = 0
  and ((bot_line_user.line_user_id NOT IN (select distinct tag_line_user.line_user_id from tag_line_user
          where tag_line_user.tag_id IN (2207112,2167388,2043744,2023981,1731547,1731544,2458442) and tag_line_user.line_user_id is not null)
  and line_user.line_id not in (select x.line_id from (select distinct detail_landing_click.line_id from detail_landing_click
          where detail_landing_click.landing_id in (524457) and detail_landing_click.line_id is not null and action=2) x)));
```

## Steps to reproduce

1. Trên bot 126066 (MySQL 8.0), mở bộ lọc bạn bè (`advanceFilterPost`) với điều kiện mức AND: "không có tag" (tag_id IN 2207112, 2167388, 2043744, 2023981, 1731547, 1731544, 2458442) **và** "chưa quét QR / chưa kết bạn qua landing 524457" (`qr_condition = 2`).
2. Chạy câu đếm (count) trên MySQL 8.0 và so với thời gian chạy cùng câu trên MySQL 5.7.

## Expected result

- Thời gian chạy trên MySQL 8.0 tương đương hoặc nhanh hơn MySQL 5.7 (~7 s); với query đã tối ưu (bảng dẫn xuất `SELECT DISTINCT`) đo được 0,1–0,5 s trên cả 2 bản, kết quả số đếm không đổi.

## Actual result

- MySQL 8.0 chạy ~50 s (ghi nhận trong slow log 03/10), do subquery `NOT IN` trên `detail_landing_click` (~31,3 triệu dòng, không DISTINCT) bị optimizer MySQL 8.0.17+ chuyển thành ANTIJOIN + materialize toàn bảng con trước khi loại trừ, thay vì chạy subquery phụ thuộc như 5.7.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Không có attachment đính kèm trực tiếp trên Redmine (0). Bằng chứng là slow log + dashboard nội bộ dẫn trong mô tả:
- Dashboard: https://dashboard.melonglobal.net/fixbug-lme/mysql80-report/#perf/P1
- Dashboard fixbug (xử lý AI): https://dashboard.melonglobal.net/implement-task-small-lme/?id=42006

## Ghi chú thêm của Leader

- Status Redmine hiện tại: **Fix done - Đợi test**. Priority: **High**. Ticket thuộc loại "Improve nội bộ" — phát hiện qua phân tích slow log khi migration MySQL 5.7 → 8.0 (không phải khách hàng report trực tiếp), tách từ ticket tổng #42000 (WEB-P1), ticket gốc #39528.
- Tác giả ticket + người fix đều là hệ thống **AI LME Fix bug** (auto-fixbug), assignee: Ngô Thúy Ngần.
- Đây là bug **hiệu năng (performance)**, không đổi kết quả dữ liệu — TC cần verify **2 trục**: (a) kết quả lọc/đếm không đổi trước/sau fix, (b) thời gian chạy trên MySQL 8.0 cải thiện (chỉ đo được trên môi trường có dữ liệu quy mô lớn thật, không kết luận được từ local/staging nhỏ).
- Plan optimizer MySQL 8.0 **không ổn định**: cùng bot, cùng điều kiện, có lượt chỉ quét 746 dòng rồi lượt sau quét 178 triệu dòng — cần lưu ý khi đánh giá "random pass" lúc đo hiệu năng.
- Dev xác nhận KHÔNG viết lại sang NOT EXISTS / LEFT JOIN … IS NULL — hướng fix cố định là `NOT IN (SELECT DISTINCT col FROM … WHERE … AND col IS NOT NULL)`. Chữa cháy khác (không áp dụng ở fix này): hint `/*+ SET_VAR(optimizer_switch='materialization=off') */`.
- Dev không EXPLAIN được trên MySQL dev lúc verify (`host.docker.internal:3306 Connection refused`) — dựa vào số đo đã có trong ticket trên máy A/B. QA nên đánh giá rủi ro này khi quyết định có cần đo lại hiệu năng độc lập hay không.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `126066` |
| Friend | `<không có 1 friend cụ thể — bug là hiệu năng câu đếm, ảnh hưởng toàn bộ bạn bè của bot>` |
| Đối tượng cấu hình | Tag IDs: 2207112, 2167388, 2043744, 2023981, 1731547, 1731544, 2458442 · Landing ID: 524457 (qr_condition = 2) |
| Thời điểm lỗi | Slow log ghi nhận 2026/10/03 (báo cáo P1 dashboard) |
| Đối chứng | Câu tối ưu (bảng dẫn xuất `SELECT DISTINCT`) đo 0,1–0,5 s trên cả MySQL 5.7 và 8.0, kết quả số đếm giống câu gốc |

## Journal / note từ Redmine (nguyên văn)

**Journal #140022 — AI LME Fix bug — 2026-10-05:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Điều kiện "chưa quét QR / chưa kết bạn qua landing" (qr_condition=2, nhánh AND) của bộ lọc bạn bè dùng NOT IN trên subquery bảng click landing KHÔNG khử trùng (1 người có nhiều dòng click). Từ MySQL 8.0.17, NOT IN ở mức AND được đổi thành antijoin và optimizer chọn plan quét lặp bảng click rất lớn (~31 triệu dòng) ⇒ cùng câu đếm 7s trên 5.7 thành ~50s trên 8.0. Nhánh này do #39121 đổi từ subquery đếm tương quan sang IN/NOT IN.

■ 2. CÁCH FIX
Nhánh "chưa quét QR" (qr_condition=2, mức AND) của bộ lọc bạn bè: đổi subquery NOT IN trên bảng click landing thành bảng dẫn xuất SELECT DISTINCT line_id (alias qr_clicked) để MySQL buộc materialize danh sách người đã quét 1 lần rồi loại trừ — đúng câu tối ưu ticket đã đo; giữ nguyên điều kiện lọc (landing_id, line_id is not null, action=2). Sửa ở Conversation::advanceFilterPost và bản mirror ConversationReplicate; các nhánh IN / group-by giữ nguyên. Quét ngang: nhánh IN (qr_condition=0), qr_code_action chưa đổi (ngoài phạm vi, ghi yokoten). [Tự review v1] Bổ sung nhánh OR qr_condition=2 (Conversation + mirror): nhóm OR chỉ 1 điều kiện "chưa quét QR" được Laravel sinh SQL ở mức AND ⇒ dính cùng antijoin trên MySQL 8.0 — nay cũng NOT IN trên bảng dẫn xuất DISTINCT (mirror giữ đúng điều kiện cũ không lọc action).

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
Conversation::advanceFilterPost — case qr_code nhánh AND (app/Conversation.php)
Conversation::advanceFilterPost — case qr_code nhánh OR (app/Conversation.php, đã sửa ở tự review v1 — nhóm OR 1 điều kiện = mức AND)
ConversationReplicate::advanceFilterPost — case qr_code nhánh AND (app/ConversationReplicate.php, mirror)
Caller: BotLineUser / BotLineUserPackage / FilterV2 (+Replicate) gọi Conversation::advanceFilterPost
LineUserModel (linect-service) — điều kiện QR vẫn là subquery đếm tương quan, khác pattern
Toàn bộ caller Conversation::advanceFilterPost (~27 file): Filter/Friendlist/CrossAnalysis/Broadcast(V2)/TalkList/Chat/RichMenu controllers, Api ListFriend/Remind/Mobile Filter, Mobile Calendar(Salon), Helpers/functions (remind), HelperService, CalendarSalonLineBookingService, console HandleExportCsv(2)/HandelCrossAnalysis(Screen)/HandleUpdateLatestInformationCsv/recoverShowFilterBroadcast — chỉ đổi hiệu năng, kết quả không đổi

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Conversation.php
   - app/ConversationReplicate.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ đổi cách viết câu SELECT, không ghi dữ liệu
 • 4.3 Tính năng liên quan:
   - Friend Filter / Segment (SC-003) — điều kiện QR "chưa quét" ở mức AND trong bộ lọc bạn bè / phân đoạn (đếm & danh sách bạn bè, FilterV2, BotLineUser) chạy nhanh hơn, kết quả không đổi
   - QR Code Action / Landing (FA-017) — dữ liệu click landing (detail_landing_click action=2) chỉ được đọc, không đổi
   - Gián tiếp (chỉ hiệu năng, kết quả không đổi): gửi tin theo bộ lọc (broadcast/remind), xuất CSV bạn bè, phân tích chéo, rich menu theo bộ lọc, lọc hội thoại, bộ lọc trên app mobile, lịch đặt chỗ salon

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Conversation.php: No syntax errors; php -l app/ConversationReplicate.php: No syntax errors; Mô phỏng ngữ nghĩa trên SQLite (dữ liệu có dòng click trùng, line_id NULL, action khác 2, nhiều landing): NOT IN subquery cũ vs NOT IN bảng dẫn xuất DISTINCT cho kết quả GIỐNG HỆT ở 4 bộ landing; EXPLAIN trên MySQL dev: KHÔNG chạy được (host.docker.internal:3306 Connection refused)
   Bằng chứng: Ticket: câu gốc 5.7 ~7s / 8.0 ~50s; câu tối ưu (bảng dẫn xuất SELECT DISTINCT) 0,1–0,5s trên cả 2 bản, kết quả không đổi — SQL sau fix trùng khớp câu tối ưu này (chỉ khác tên alias)

■ TỰ REVIEW (AI)
Diff 2 file, chỉ đổi nhánh qr_condition=2 mức AND sang NOT IN bảng dẫn xuất DISTINCT; các nhánh 0/1/3 và OR dùng nguyên biến cũ. Tương đương ngữ nghĩa: NOT IN là phép tập hợp nên DISTINCT không đổi kết quả; vẫn giữ line_id is not null bên trong nên không có bẫy NULL. Alias qr_clicked nằm trong scope subquery riêng nên nhiều điều kiện QR cùng lúc không đụng nhau.
 • Rủi ro / lưu ý khi test:
   - Không EXPLAIN được trên MySQL dev (connection refused) — dựa vào số đo của ticket trên máy A/B
   - Bảng dẫn xuất vẫn phải đọc mọi click của landing (index landing_id); landing cực lớn vẫn tốn chi phí materialize 1 lần — chấp nhận được (0,1–0,5s theo ticket)

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_42006 (nhánh gốc release_step_20260930_v2, commit cecb9eddff, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 2 phút 31 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=2d55f180-9cc3-478a-8684-54ffb32af87c
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=42006
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
