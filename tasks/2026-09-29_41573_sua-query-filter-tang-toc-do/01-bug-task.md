# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41573 — [web] sửa query filter để tăng tốc độ` |
| Module / Màn hình | Friend Filter / Segment (SC-003) — điều kiện lọc theo **thẻ (tag)** của bộ lọc bạn bè (`Conversation::advanceFilter` / `advanceFilterPost`); dùng chung bởi Friend List (FA-013), Broadcast (FA-008) + Delivery Target Selector (SC-006), 1-on-1 Chat (FA-001) |

## Mô tả bug (bản dịch tiếng Việt)

Nội dung report gốc (đã là tiếng Việt, giữ nguyên văn):

Vấn đề:
Query filter hiện tại chạy mất 12s trên MySQL 5.7, mất 30s trên MySQL 8.0 (đối với query mẫu bên dưới). Query hiện tại có 2 vấn đề:
1. Sử dụng `NOT EXISTS` chưa tối ưu làm sai chiến lược thực thi bên MySQL 8.0 khiến query rất chậm.
2. Bản thân query chạy trên MySQL 5.7 cũng chưa tối ưu.

Giải pháp: Sửa cách query giống với bên job Java.

Query gốc (rút gọn, giữ nguyên cấu trúc — danh sách `tag_id` đầy đủ xem nguyên văn Redmine #41573):
```sql
select count(*) as aggregate from bot_line_user
where bot_line_user.bot_id = 196392 and bot_line_user.is_blocked = 0
  and (
    (NOT EXISTS (select 1 from tag_line_user where tag_line_user.tag_id IN (2435824,2417867,2403111)
                 and bot_line_user.line_user_id = tag_line_user.line_user_id limit 1)
     and EXISTS (select 1 from tag_line_user where tag_line_user.tag_id IN (<~200 tag_id>)
                 and bot_line_user.line_user_id = tag_line_user.line_user_id limit 1)
     and NOT EXISTS (select 1 from tag_line_user where tag_line_user.tag_id IN (2440096,2440145,2440180,2440211,2440607,2440644,2441032,2441081,2441189)
                     and bot_line_user.line_user_id = tag_line_user.line_user_id limit 1)
     and ((select COUNT(DISTINCT(line_id)) from friend_information_value
           where friend_information_setting_id = 287868 AND friend_information_value.bot_id = bot_line_user.bot_id
             AND friend_information_value.line_id = bot_line_user.line_user_id
             AND CAST(value as SIGNED integer) <= 180) > 0)
    )
  );
```

Query improve giống với job Java:
```sql
select count(*) as aggregate from bot_line_user
where bot_line_user.bot_id = 196392 and bot_line_user.is_blocked = 0
  and bot_line_user.line_user_id NOT IN (select distinct tag_line_user.line_user_id from tag_line_user where tag_line_user.tag_id IN (2435824,2417867,2403111))
  and bot_line_user.line_user_id NOT IN (select distinct tag_line_user.line_user_id from tag_line_user where tag_line_user.tag_id IN (2440096,2440145,2440180,2440211,2440607,2440644,2441032,2441081,2441189))
  and EXISTS (select 1 from tag_line_user where tag_line_user.tag_id IN (<~200 tag_id>)
              and bot_line_user.line_user_id = tag_line_user.line_user_id limit 1)
  and ((select COUNT(DISTINCT(line_id)) from friend_information_value
        where friend_information_setting_id = 287868 AND friend_information_value.bot_id = bot_line_user.bot_id
          AND friend_information_value.line_id = bot_line_user.line_user_id
          AND CAST(value as SIGNED integer) <= 180) > 0);
```

**Diễn giải chi tiết (theo Journal #138647 — AI LME Fix bug):** Điều kiện lọc theo thẻ của bộ lọc bạn bè dùng subquery TƯƠNG QUAN (`EXISTS`/`NOT EXISTS` kèm `LIMIT 1` cho lựa chọn có/không có thẻ; subquery đếm so với số thẻ cho lựa chọn đủ/không đủ N thẻ). Vì subquery tham chiếu cột bảng ngoài (+ có `LIMIT 1`) nên MySQL không chuyển được thành semi-join/anti-join mà phải chạy lại subquery cho TỪNG dòng bạn bè — bot nhiều bạn + danh sách thẻ dài (hàng trăm `tag_id`) khiến câu đếm chậm, và MySQL 8.0 còn chọn chiến lược thực thi tệ hơn cho `NOT EXISTS` so với 5.7.

## Steps to reproduce

<!-- Redmine không có Section "Tái hiện bug" dạng step-by-step — đây là ticket cải tiến hiệu năng (tracker "Improve nội bộ"), report chỉ gồm query mẫu + số đo thời gian chạy (12s/30s). Không có luồng thao tác UI cụ thể để tái hiện. -->

## Expected result

- Query lọc bạn bè theo thẻ trả về **kết quả giống hệt cách cũ** ở cả 4 lựa chọn điều kiện thẻ (có thẻ / không có thẻ / đủ N thẻ / không đủ N thẻ), nhưng **chạy nhanh hơn** (không còn tương quan theo từng dòng bạn bè).

## Actual result

- Trước fix: query dùng subquery tương quan (`EXISTS`/`NOT EXISTS` + `LIMIT 1`) → chạy ~12s (MySQL 5.7) / ~30s (MySQL 8.0) với bot nhiều bạn + danh sách thẻ dài.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments rỗng (0) -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không có Section "Tái hiện bug" dạng step-by-step** — đây là ticket **cải tiến hiệu năng nội bộ** (tracker `Improve nội bộ`, không phải `Bug`), root cause + cách fix đã được Dev trình bày trực tiếp trong Description + Journal #138647 (đóng vai trò section "Đánh giá ảnh hưởng", xem file 03). TCs nên tập trung verify **kết quả lọc không đổi** (regression tính đúng của 4 lựa chọn điều kiện thẻ) trên diện rộng các màn dùng chung bộ lọc, không cần đo lại tốc độ (đo tốc độ là việc của Dev/DBA).
- Priority: **High** | Status: **Fix done - Đợi test**.
- ⚠️ **Chưa chạy EXPLAIN / đo tốc độ thật** — Dev tự nhận không kết nối được MySQL dev trong phiên fix (`host.docker.internal:3306`, `127.0.0.1`, `172.17.0.1` đều Connection refused). Dev chỉ verify bằng mô phỏng ngữ nghĩa PHP (24/24 case khớp), **chưa đo tăng tốc thực tế** trên môi trường có dữ liệu — QA/DBA cần đo lại nếu muốn xác nhận mục tiêu "tăng tốc độ" của ticket.
- ⚠️ **Cách viết mới phụ thuộc index trên `tag_line_user.tag_id`** — nếu production thiếu index này, Dev khuyến nghị DBA xác nhận trước khi kết luận đã tối ưu.
- ⚠️ **Hành vi giữ nguyên có chủ ý (không phải bug)**: lựa chọn "đủ N thẻ" vẫn đếm theo **số dòng** `tag_line_user` (không `DISTINCT tag_id`) — nếu bạn bè có dòng thẻ TRÙNG thì kết quả có thể khác so với job Java (Java dùng `count(distinct tag_id)`). Dev giữ nguyên hành vi cũ, cần BA/DBA chốt riêng nếu muốn đổi.
- ⚠️ **Bug có sẵn KHÔNG thuộc phạm vi ticket, giữ nguyên**: danh sách thẻ rỗng ở lựa chọn 1/2/3 của bộ lọc nâng cao vẫn sinh `IN ()` lỗi SQL như trước fix (chỉ lựa chọn 0 có guard `!empty`).
- ⚠️ **Ticket riêng (ngoài phạm vi #41573)**: cùng 2 file còn các subquery đếm tương quan khác cho điều kiện **kịch bản (scenario)** và **điều kiện chuyển đổi (conversion)** — Dev ghi nhận nhưng KHÔNG fix trong ticket này (không phải lỗi `NOT EXISTS` mà ticket nêu).
- Branch fix: `ai_small_41573` (nhánh gốc `release_step_20260827`, commit `38c6fd1d21`, 2 file) — đã push lên `sns-line`.
- ⚠️ **Đã có task Studio cho ticket này** — `task_id=337` (feature `friend-filter`, round 1, 39 TC, trạng thái `tc-ready`, `reviewState=leader`) — dùng làm nguồn TC cho `/review-tc` (xem file 04).

## Journal / note từ Redmine (nguyên văn)

**Journal #138647 — AI LME Fix bug — 2026-09-26:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Điều kiện lọc theo thẻ (tag) của bộ lọc bạn bè dùng subquery TƯƠNG QUAN: EXISTS/NOT EXISTS có kèm LIMIT 1 (lựa chọn có/không có thẻ) và subquery đếm so với số thẻ (lựa chọn đủ/không đủ N thẻ). Vì subquery tham chiếu cột của bảng ngoài (và còn có LIMIT 1) nên MySQL không chuyển được thành semi-join/anti-join mà phải chạy lại subquery cho TỪNG dòng bạn bè; bot nhiều bạn cộng danh sách hàng trăm thẻ khiến câu đếm mất khoảng 12s trên MySQL 5.7 và khoảng 30s trên MySQL 8.0, do bản 8.0 chọn chiến lược thực thi tệ hơn cho NOT EXISTS.

■ 2. CÁCH FIX
Đổi cả 4 lựa chọn của điều kiện thẻ trong bộ lọc bạn bè từ subquery tương quan sang subquery KHÔNG tương quan giống job Java: có thẻ = 'bot_line_user.line_user_id IN (select distinct line_user_id from tag_line_user where tag_id IN (...))', không có thẻ = NOT IN cùng danh sách đó, đủ N thẻ = IN của danh sách gom nhóm 'group by line_user_id having count(tag_id) = N', không đủ N thẻ = NOT IN của chính danh sách gom nhóm đó; bỏ hẳn EXISTS/NOT EXISTS và LIMIT 1. Thêm điều kiện 'tag_line_user.line_user_id is not null' vì cột này cho phép NULL, nếu không thì NOT IN gặp NULL sẽ trả về rỗng. Áp cho 3 chỗ trong bộ lọc bạn bè (bộ lọc cơ bản, nhánh AND và nhánh OR của bộ lọc nâng cao) và 3 chỗ tương ứng ở bản sao đọc replica; giữ nguyên cách đếm count(tag_id) không distinct để kết quả y hệt trước. Quét ngang: cùng 2 file còn các subquery đếm tương quan cho điều kiện kịch bản và điều kiện chuyển đổi, ghi lại làm ticket riêng vì thuộc điều kiện lọc khác và không phải lỗi NOT EXISTS mà ticket nêu.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
Conversation::advanceFilter (app/Conversation.php:92, điều kiện thẻ ~188-210)
Conversation::advanceFilterPost nhánh AND (app/Conversation.php:247, case 'tag' ~423-443)
Conversation::advanceFilterPost nhánh OR (app/Conversation.php, case 'tag' ~1120-1140)
ConversationReplicate::advanceFilter (app/ConversationReplicate.php:76, điều kiện thẻ ~172-191)
ConversationReplicate::advanceFilterPost nhánh AND + OR (app/ConversationReplicate.php ~392-414 và ~1012-1036)
FriendlistController::postFilterAdvance / getListFriend / ajaxCountFriend (app/Http/Controllers/Basic/FriendlistController.php — bên gọi)
BroadcastController (app/Http/Controllers/Basic/BroadcastController.php:411/466/2607 — bên gọi)
ChatController (app/Http/Controllers/ChatController.php:1740 — bên gọi)
BotLineUser / BotLineUserPackage / FilterV2 (app/BotLineUser.php:28,695; app/BotLineUserPackage.php:27,526; app/FilterV2.php:1473,1480 — bên gọi)
LineUserModel.buildWhere / buildWhereV2 (linect-service src/main/java/sns/line/models/LineUserModel.java:190-212, 480-525 — bản java dùng làm mẫu, KHÔNG sửa)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Conversation.php
   - app/ConversationReplicate.php
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ đổi cách viết câu SELECT, không có lệnh ghi/sửa dữ liệu, không thêm index, không migration
 • 4.3 Tính năng liên quan:
   - Friend Filter / Segment (SC-003) — điều kiện lọc theo thẻ nhanh hơn, kết quả giữ nguyên ở cả 4 lựa chọn
   - Friend List (FA-013) — màn danh sách bạn bè và ô đếm số bạn khớp bộ lọc
   - Broadcast (FA-008) và Delivery Target Selector (SC-006) — chọn đối tượng nhận tin dùng chung hàm lọc, số người nhận phải không đổi
   - 1-on-1 Chat (FA-001) — lọc hội thoại theo thẻ ở màn chat dùng chung hàm lọc

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Conversation.php: No syntax errors detected; php -l app/ConversationReplicate.php: No syntax errors detected; grep kiểm tra: không còn EXISTS/NOT EXISTS nào trong 2 file sau khi sửa; các subquery qr_code/qr_code_action dùng biến $in_string riêng không bị đụng (đã đổi tên biến của khối thẻ thành $tag_in_string/$tag_count_string/$tag_number để không trùng); Mô phỏng ngữ nghĩa bằng PHP cho cả 4 lựa chọn trên bộ dữ liệu có dòng thẻ TRÙNG và dòng line_user_id NULL: 24/24 ca cho kết quả giống hệt cách cũ; Chưa chạy EXPLAIN: MySQL dev host.docker.internal:3306 (và 127.0.0.1, 172.17.0.1) đều Connection refused trong phiên này
   Bằng chứng: tag_line_user.line_user_id là int(12) DEFAULT NULL (share/db/db-structure/tables/tag_line_user.sql) => bắt buộc lọc IS NOT NULL trong subquery NOT IN; bot_line_user.line_user_id là int(11) NOT NULL (share/db/db-structure/tables/bot_line_user.sql) => vế ngoài của NOT IN không bao giờ NULL, không đổi kết quả so với NOT EXISTS; Mẫu java: LineUserModel.java:204-206 dùng 'line_user.id NOT IN (SELECT DISTINCT tag_line_user.line_user_id ...)' và 201/208 dùng IN/NOT IN của subquery group-by-having — đúng cách ticket yêu cầu; Tiền lệ cùng kiểu trong repo: fix #39121 đã đổi điều kiện QR/landing từ subquery đếm tương quan sang IN/NOT IN kèm 'line_id is not null' (comment còn ở app/Conversation.php:528); Cách viết EXISTS/NOT EXISTS hiện tại do fix #38294 (commit cfcaded173) đưa vào để thay count()>0 — nhanh hơn trên 5.7 nhưng vẫn tương quan, và MySQL 8.0 chọn plan xấu cho NOT EXISTS

■ TỰ REVIEW (AI)
Thay 6 khối điều kiện thẻ giống nhau (3 trong bộ lọc bạn bè + 3 trong bản sao replica) bằng subquery không tương quan theo đúng mẫu job java. Đã chứng minh tương đương ngữ nghĩa cho cả 4 lựa chọn, kể cả trường hợp bạn không có thẻ nào (lựa chọn không đủ N thẻ vẫn lấy) và trường hợp bảng thẻ có dòng trùng (giữ count không distinct nên kết quả y như cũ, không tự ý sửa luôn điểm này). Đã đổi tên biến khối thẻ để không trùng biến $in_string/$number của khối QR ngay bên dưới trong cùng switch.
 • Rủi ro / lưu ý khi test:
   - Không chạy được EXPLAIN vì MySQL dev không kết nối được trong phiên này — mức tăng tốc thực tế cần người test đo lại trên môi trường có dữ liệu (ticket đã có số đo của người tạo cho cách viết java)
   - Cách viết mới phụ thuộc index trên tag_line_user.tag_id; nếu production thiếu index này thì subquery phải quét bảng thẻ một lần (vẫn tốt hơn quét lại theo từng dòng bạn, nhưng nên để DBA xác nhận index)
   - Với bạn bè có dòng thẻ TRÙNG trong tag_line_user, lựa chọn 'đủ N thẻ' vẫn đếm theo số dòng (không distinct) — đây là hành vi CŨ được giữ nguyên có chủ ý; bản java dùng count(distinct tag_id) nên kết quả có thể khác java ở ca trùng dữ liệu, cần BA/DBA chốt riêng nếu muốn đổi
   - Trường hợp danh sách thẻ rỗng ở lựa chọn 1/2/3 của bộ lọc nâng cao vẫn sinh 'IN ()' lỗi SQL như trước khi sửa (chỉ lựa chọn 0 có guard !empty) — lỗi có sẵn, không thuộc phạm vi ticket nên giữ nguyên hành vi

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_small_41573 (nhánh gốc release_step_20260827, commit 38c6fd1d21, 2 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 9 phút 7 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=2581165f-95af-4b6a-b762-0f062a014107
» Dashboard fixbug: https://dashboard.melonglobal.net/implement-task-small-lme/?id=41573
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
