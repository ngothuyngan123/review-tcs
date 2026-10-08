# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42258 — [JOB] Nâng MySQL 5.7 → 8.0: gộp R1 (GROUP BY không tự sắp xếp) + P1 (NOT IN antijoin) + bộ lọc tag IN (subquery) — #41997 #42002 #42014` |
| Module / Màn hình | Job nền (linect-service, Java) — bộ lọc bạn bè dùng chung cho: Broadcast, Action schedule, Rich menu theo bộ lọc, Export CSV (quản lý + chat 1:1), Phân tích chéo, Chuẩn bị template broadcast, Auto reply bộ lọc cũ, `isValidFilter`/`isValidFilterV2` (kiểm 1 bạn bè) |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Đây **không phải** bug tái hiện từ 1 ca lỗi cụ thể của khách hàng — là ticket kỹ thuật nội bộ, gộp 3 task con (A/B/C) từ báo cáo đối chiếu hành vi MySQL 5.7 → 8.0 (ticket gốc #39528). Mỗi phần có luận điểm rủi ro riêng, dịch nguyên văn theo thứ tự ticket.

**Phần A — #41997 [JOB-R1] GROUP BY không còn tự sắp xếp kết quả**

Thay đổi 5.7 → 8.0: ở 5.7, `GROUP BY x` ngầm định `ORDER BY x` (trừ khi ghi `ORDER BY NULL`). Ở 8.0, hành vi này bị bỏ hẳn — câu không có `ORDER BY` thì thứ tự trả về là thứ tự của execution plan (temp table, hash, index…), có thể khác nhau giữa các lần chạy.

Điều kiện kích hoạt: câu có `GROUP BY` mà không có `ORDER BY`, và code/UI đang dùng thứ tự dòng trả về (hiển thị danh sách, phân trang, so vị trí phần tử, `LinkedHashMap`…).

Tác động: sai kết quả hiển thị (danh sách, biểu đồ theo ngày lộn xộn), phân trang lặp/sót, và nặng nhất — logic nghiệp vụ dựa vào **vị trí phần tử trong danh sách**.

3 vị trí rủi ro (đối chiếu code commit `a84acd44`):
1. **[Ưu tiên Cao]** ★ **Resume broadcast bị gián đoạn** — `BroadcastNewJob.java:83`. Dò người nhận cuối trong `lineUsers` rồi gửi tiếp những người PHÍA SAU trong danh sách (`getListLineUserFromFilterV2(..., orderByBotLineUser=false)` → `GROUP BY line_user.id` KHÔNG `ORDER BY`). 5.7: luôn tăng theo `line_user.id` nên resume đúng. 8.0: thứ tự có thể khác lần gửi đầu ⇒ người chưa nhận nằm "trước" người cuối bị **BỎ SÓT**, người đã nhận nằm "sau" bị **GỬI LẶP** tin cho khách.
2. **[Ưu tiên Cao]** Câu lấy người nhận V1/V2 — `LineUserModel.java:399`. `GROUP BY line_user.id`; chỉ `ORDER BY bot_line_user.id ASC` khi cờ `orderByBotLineUser = true`. Broadcast truyền `false` nên bị ảnh hưởng; export CSV (`HandleExportCsvTask.java:90`) truyền `true` nên không bị; action schedule / rich menu / chuẩn bị template xử lý cả danh sách (không phụ thuộc thứ tự); `isValidFilterV2` chỉ kiểm có/không.
3. **[Ưu tiên Trung bình]** Phân tích chéo — tiêu đề hàng theo thông tin cơ bản — `HandleCrossAnalysis.java:235`. `listRowTitle` thêm theo thứ tự dòng trả về ⇒ thứ tự hàng trong bảng phân tích chéo có thể đổi (sai hiển thị/xuất file, không gửi tin cho khách).

Hướng xử lý: thêm `ORDER BY` tường minh (theo đúng cột 5.7 đang ngầm sắp xếp) cho từng câu.

**Phần B — #42002 [JOB-P1] NOT EXISTS / NOT IN (subquery) bị đổi thành antijoin rồi materialize cả bảng con**

Thay đổi 5.7 → 8.0: 5.7 chạy `NOT EXISTS`/`NOT IN` như subquery phụ thuộc (dependent) — tra index bảng con cho từng dòng ngoài, chi phí tỉ lệ số dòng ngoài. 8.0.17+: optimizer được phép biến chúng thành **ANTIJOIN** + **materialization** — đọc TOÀN BỘ dòng bảng con khớp điều kiện (với `tag_line_user` là ~178 triệu dòng) trước khi loại trừ. Chi phí chuyển sang tỉ lệ kích thước bảng con.

Điều kiện kích hoạt: `NOT EXISTS` (luôn đủ điều kiện) hoặc `NOT IN (SELECT …)` khi cả 2 vế NOT NULL; bảng con lớn; ở mức AND của WHERE. Plan còn **không ổn định** (cùng bot/điều kiện, lượt trước 746 dòng, lượt sau 178 triệu dòng).

Tác động: chậm từ < 1s lên hàng chục–hàng trăm giây; giữ connection, chồng tải khi client retry. Bằng chứng slow log B: U001 712s (178.323.108 dòng), U002 378s, U008 167s/151 user, U009 167s/78 user, Q10 37,5s (A: 8,7s), Q12 31,8s (A: 9,3s), sự cố 24/09.

2 vị trí rủi ro:
1. **[Ưu tiên Cao]** Lọc "thông tin bạn bè chưa đăng ký" — `LineUserModel.java:997` (+ cùng mẫu ở 1032, 1034, 1063, 1821, 1856, 1858, 1887). `NOT IN (select distinct line_id from friend_information_value where bot_id = ... AND friend_information_setting_id = ...)` — `line_id` NOT NULL ⇒ đủ điều kiện antijoin. Bảng `friend_information_value` ≥ 50 triệu dòng.
2. **[Ưu tiên Trung bình]** Lọc "không theo kịch bản" — `LineUserModel.java:623` (+ cùng mẫu ở 241, 265, 656, 1421, 1456, 2247, 2272). `NOT IN` trên `scenario_lineuser` — 2 vế NOT NULL ⇒ đủ điều kiện antijoin. Bảng `scenario_lineuser` 5–50 triệu dòng.

**Diễn biến quyết định xử lý (quan trọng — đã đổi 2 lần, chốt lần cuối):**
- Ban đầu (#42002): dùng `NOT IN (SELECT DISTINCT col ... AND col IS NOT NULL)`.
- Review bổ sung (journal 05/10): phát hiện nhánh "không có tag" ở `LineUserModel.java:206, 541, 1329, 2220` **thiếu** `line_user_id IS NOT NULL` (commit `45fce05` chỉ thêm cho `scenario_lineuser`/`friend_information_value`, chưa sửa `tag_line_user`).
- Quyết định lần 1 (05/10, journal #140257): thống nhất 3 repo (web/job/MCP) dùng CHUNG 1 dạng cho lọc kịch bản: `x NOT IN (SELECT DISTINCT line_user_id FROM scenario_lineuser WHERE scenario_id = ? AND is_following = <1|2> AND is_deleted = 0)` — **KHÔNG** thêm `IS NOT NULL` (cột `scenario_lineuser.line_user_id` là NOT NULL).
- **Đính chính (05/10, journal #140263) — quyết định CUỐI**: **GIỮ** `line_user_id IS NOT NULL` → dạng chuẩn cuối cùng: `x NOT IN (SELECT DISTINCT line_user_id FROM scenario_lineuser WHERE scenario_id = ? AND is_following = <1|2> AND is_deleted = 0 AND line_user_id IS NOT NULL)`. Job (commit `45fce05`) đã đúng dạng này từ đầu — giữ nguyên.
- `tag_line_user`: xử lý riêng ở Phần C (#42014) — **BẮT BUỘC** có `IS NOT NULL` vì cột này cho phép NULL (production có 22 dòng NULL).
- `friend_information_value`: giữ `IS NOT NULL`, chưa chốt lại riêng.

Hướng xử lý cuối: `x NOT IN (SELECT DISTINCT col FROM … WHERE … AND col IS NOT NULL)`. **KHÔNG** viết lại sang `NOT EXISTS` / `LEFT JOIN ... IS NULL`. Chữa cháy dự phòng: hint `/*+ SET_VAR(optimizer_switch='materialization=off') */`.

**Phần C — #42014 [JOB] Bộ lọc bạn bè: đổi điều kiện "có tag" từ `(SELECT COUNT…) > 0` sang `IN (subquery)` — ~48% thời gian query chậm DB B**

Vấn đề: filter builder của job sinh điều kiện "bạn bè có ít nhất một tag trong danh sách" bằng phép đếm tương quan:
```sql
(SELECT COUNT(tag_line_user.tag_id) FROM tag_line_user
 WHERE tag_line_user.tag_id IN (<danh sách tag>)
   AND tag_line_user.line_user_id = line_user.id) > 0
```
MySQL phải duyệt từng bạn bè của bot và đếm tag cho từng người, bất kể danh sách tag hiếm/phổ biến. Lỗi hiệu năng có trên cả 5.7 và 8.0. Ví dụ bot 97640 (~306 nghìn bạn bè): mỗi lượt đọc ~20 triệu dòng `tag_line_user`, mất 16–125s. Slow log B (00:37 JST 03/10 → 17:31 JST 04/10, ngưỡng ≥10s): 126 lượt, tổng 4.348s, 13 nhóm query cùng mẫu.

Vị trí code (commit `a84acd44`, `LineUserModel.java`): dòng 517 `buildWhereFilter` (nhóm AND, nhánh `TagFilterOption.OR_FILTER`, `lineId == null`) và dòng 1301 `buildWhereORFilter` (nhóm OR, cùng nhánh). **Không sửa** nhánh `lineId != null` (dòng 519, 1303 — dùng cho `isValidFilterV2` kiểm 1 người, điều kiện đã cố định).

Đổi mẫu SQL "có tag": `(SELECT COUNT...) > 0` → `line_user.id IN (SELECT tag_line_user.line_user_id FROM tag_line_user WHERE tag_line_user.tag_id IN (<tags>))`. Nhiều điều kiện tag nối AND → đổi từng điều kiện thành 1 `IN(...)` riêng. Giữ nguyên `GROUP BY line_user.id`, danh sách tag, điều kiện khác, thứ tự.

Không đổi (ngoài phạm vi task): "Không có tag" (`NOT IN` — thuộc #42002), Landing count, Thông tin bạn bè count (đã thử `IN`, EXPLAIN không có lợi).

Vì sao kết quả không đổi: `COUNT(tag_id)... > 0` ⇔ tồn tại dòng `tag_line_user` khớp tag + `line_user_id = line_user.id` ⇔ chính là điều kiện `line_user.id IN (...)` đúng. `GROUP BY line_user.id` giữ nguyên nên không nhân dòng. Lưu ý NULL: `tag_line_user.line_user_id` cho phép NULL — nếu điều kiện bị đặt trong `NOT(...)` thì kết quả IN/NOT IN có thể khác do 3 giá trị logic của SQL; builder hiện KHÔNG sinh `NOT(...)` quanh điều kiện "có tag" (đã rà code) nên không ảnh hưởng ở điều kiện có tag — nhưng chính vì cột cho phép NULL mà nhánh "không có tag" phải có `IS NOT NULL` (xem Phần B).

Đã đo hiệu năng (DB B, MySQL 8.0.46, production, 04/10 19:22–19:43 JST):
| Query | Trước (server) | Sau (server) | Nhanh hơn | Dòng đọc (trước→sau) |
|---|---|---|---|---|
| Q017: 2 điều kiện tag, trả 6.449 dòng | 129,2s | **0,17s** | **760×** | 20,8tr → 120k |
| Q005: 2 tag + `followed_at`, trả ~160k dòng | 60,7s | **1,63s** | **37×** | 21,8tr → 1,6tr |
| Q002: 2.733 tag, trả ~281k dòng | 73,2s | **27,0s** | **2,7×** | 22,7tr → 6,9tr |

Tiêu chí nghiệm thu (ghi nguyên văn, dùng để đối chiếu khi viết TC):
1. Kết quả giống hệt bản cũ (so tập `line_user.id`, trên dữ liệu không đổi — DB test/snapshot, không so trên production đang ghi): bot lớn + bot nhỏ; 1 tag hiếm; nhiều tag phổ biến; danh sách ~2.700 tag; 2 điều kiện tag nối AND; điều kiện tag trong nhóm OR; kết hợp "không có tag", `followed_at`, `is_blocked`, landing.
2. Plan: `EXPLAIN FORMAT=TREE` trên DB B của query mới bắt đầu từ `tag_line_user` (range/lookup theo index `idx_tag_line_delete`). Không còn `Select #... (subquery in condition; dependent)` cho điều kiện tag.
3. Hiệu năng: thời gian server không vượt Q017 1s, Q005 5s, Q002 40s. Không query nào chậm hơn bản cũ.
4. Sau deploy: theo dõi slow log B 1–2 ngày, số lượt ≥10s mẫu `SELECT COUNT(tag_line_user.tag_id)` về 0.

**Quyết định chốt bộ lọc tag 3 repo (journal 05/10, #140247) — thống nhất theo dạng của WEB:**
- "Có tag": `x IN (SUB)` · "Không có tag": `x NOT IN (SUB)` — 2 nhánh dùng CHUNG 1 subquery `SUB`.
- `SUB` chuẩn: `SELECT DISTINCT tag_line_user.line_user_id FROM tag_line_user WHERE tag_line_user.tag_id IN (<tags>) AND tag_line_user.line_user_id IS NOT NULL`.
- Lý do: (1) ở mức AND, MySQL 8.0 xử lý EXISTS và IN như nhau; (2) trong nhóm OR, IN không tương quan chỉ dựng 1 lần còn EXISTS/đếm tương quan chạy lại từng bạn bè; (3) trên 5.7, IN được semijoin còn EXISTS thì không; (4) 2 nhánh dùng chung 1 subquery tránh sửa lệch (vụ thiếu IS NOT NULL ở nhánh "không có tag").
- **Vì sao gấp**: `tag_line_user.line_user_id` cho phép NULL (production có 22 dòng NULL). Thiếu `IS NOT NULL` thì tag có dòng NULL sẽ làm "không có tag" trả **0 người** — broadcast/action schedule gửi thiếu, trong khi web đếm ra N người đúng.
- Kiểm thử yêu cầu: so số người nhận job với số đếm trên màn lọc web (có tag / không có tag, nhóm AND/OR); thêm 1 ca tag có dòng `line_user_id NULL`.

## Steps to reproduce

<!-- Không có — ticket là audit kỹ thuật từ báo cáo đối chiếu MySQL 5.7 vs 8.0, không phải 1 ca lỗi khách hàng báo. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #42258 không có attachment (0). Báo cáo gốc "dev_task_02_job_tag_filter_in_subquery.md" được dẫn nhưng KHÔNG đính kèm trong issue này. Dashboard tham khảo (không fetch được qua API, chỉ ghi lại link):
- https://dashboard.melonglobal.net/fixbug-lme/mysql80-report/#result/R1 (Phần A)
- https://dashboard.melonglobal.net/fixbug-lme/mysql80-report/#perf/P1 (Phần B)
- https://dashboard.melonglobal.net/fixbug-lme/mysql80-review/#findings (Phần B, journal 05/10)
- https://dashboard.melonglobal.net/fixbug-lme/mysql80-review/#features/F3 (Phần B, quyết định lọc kịch bản)
- https://dashboard.melonglobal.net/fixbug-lme/mysql80-review/#features/F2 (Phần C, quyết định lọc tag 3 repo)
-->

## Ghi chú thêm của Leader

⚠️ Ticket này **KHÔNG tái hiện từ 1 ca lỗi khách hàng** — là audit kỹ thuật nội bộ gộp 3 task (A=#41997, B=#42002, C=#42014), ticket gốc #39528, dựa trên báo cáo đối chiếu hành vi MySQL 5.7 vs 8.0 (dashboard nội bộ). TCs nên tập trung verify: (1) kết quả filter/query **không đổi** so với bản cũ trên dữ liệu cố định, (2) hiệu năng đạt ngưỡng đã nêu, (3) EXPLAIN plan không còn antijoin/materialize/missing ORDER BY, (4) không có TC nào dựa trên "tái hiện" — đây là kiểm chứng theo tiêu chí nghiệm thu đã nêu trong mô tả.

Dự án/repo liên quan: `linect-service` (job Java), branch chung `m_202610_mysql_update_80_39528`. Môi trường: DB B = MySQL 8.0.46-0ubuntu0.22.04.4 (production); đối chiếu với DB A = MySQL 5.7. Việc đo hiệu năng (Phần C) đã thực hiện trực tiếp trên production (04/10/2026) — nhạy cảm, không nên re-run đo hiệu năng trên production khi viết TC mà nên dùng DB test/staging cùng cấu hình dữ liệu nếu có, trừ khi Leader xác nhận được phép đo trên prd.

⚠️ Có **sự thay đổi quyết định 2 lần trong cùng 1 ngày** (05/10) cho nhánh lọc "không theo kịch bản"/"chưa hoàn thành kịch bản" — bản đầu bỏ `IS NOT NULL`, bản đính chính giữ lại. Dev impact (03-dev-impact.md, phần B) và commit `45fce05` đã áp theo **quyết định cuối (giữ IS NOT NULL)** — khi viết/review TC, đối chiếu đúng bản cuối, không dùng bản đã bị đính chính.

⚠️ **Studio đã có task sẵn cho ticket này** (task #372, round 1, trạng thái `tc-ready`, 38 TC, chưa chạy (0 pass/0 fail/38 untested), tất cả trên env `local` — chưa chạy trên `dev/prd/staging`) — xem `04-tc-list.md`.

## Dữ liệu định danh ca lỗi

<!-- Không phải 1 ca lỗi cụ thể của 1 khách hàng — đây là ví dụ/dữ liệu dùng để đo & minh họa trong báo cáo kỹ thuật. -->

| Mục | Giá trị |
|---|---|
| bot_id ví dụ (Phần C, bot lớn) | `97640` (~306.000 bạn bè — dùng để đo Q017/Q005/Q002) |
| Bảng dữ liệu liên quan | `line_user` (62.044.908 dòng, 19,0 GiB) · `bot_line_user` (49.987.580 dòng, 17,8 GiB) · `tag_line_user` (~178 triệu dòng — scan khi antijoin) · `friend_information_value` (50.989.021 dòng, 6,8 GiB) · `scenario_lineuser` (26.385.876 dòng, 5,0 GiB) |
| Code đối chiếu | Commit `a84acd44` (28/09/2026, trước fix) |
| Commit sau fix | `208983f` (Phần A) · `45fce05` (Phần B) · `1515afc` + `1db73cf` (Phần C) |
| Branch chung | `m_202610_mysql_update_80_39528` |
| DB B (môi trường đối chiếu) | MySQL 8.0.46-0ubuntu0.22.04.4 (production) |
| Thời điểm đo hiệu năng (Phần C) | 04/10/2026 19:22–19:43 JST, trên production |
| Đối chứng data đặc biệt | Tag có dòng `tag_line_user.line_user_id = NULL`: production có **22 dòng** như vậy — case bắt buộc khi test "không có tag" |

## Journal / note từ Redmine (nguyên văn)

<!-- Redmine API trả 0 journal có notes riêng (issue không có journal thật) — toàn bộ nội dung journal gốc của 3 task con (#41997/#42002/#42014) đã được tác giả chép thủ công vào trong Description khi gộp ticket (xem "Đánh giá ảnh hưởng của DEV" từng phần ở 03-dev-impact.md, và các mục "Ghi chú (nguyên văn)" đã lồng vào Mô tả bug ở trên). Không có journal bổ sung nào khác ngoài nội dung đã paste trong description. -->
