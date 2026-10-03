# 05 — Review Report

> Draft cho Leader verify. Bug ID + ngày nằm ở tên folder; file này = round 1.
> Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #337 (ticket 41573, round 1, fetch 2026-09-29) |
| Tổng số TC review | 39 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 10/11 mục có TC (`BUG` + F1–F6 + T1–T4; mục 4.2 Dev ghi "không có data") — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (2 file, +81/−78) | 14/15 điểm có TC (2 file · 3 rủi ro hồi quy · luồng replica · 9 nơi dùng chung Studio kê) — **CHƯA ĐỦ** |

**Kết luận**: 7 dòng thiếu — 2 GAP · 5 RISK. Phần lõi (4 lựa chọn điều kiện thẻ × nhánh AND/OR, NOT IN + NULL, biên N, tổ hợp AND/OR trong CÙNG loại `tag`, CSV, mobile, phân tích chéo) đã đủ và đều `pass`. Chỗ thiếu nằm ở **mục tiêu hiệu năng của ticket**, **bộ lọc cơ bản (V1)**, **các nơi dùng chung ngoài màn 友だちリスト**, và **tổ hợp filter tag với filter type KHÁC** (`対応ステータス` — status_chat).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — mục tiêu ticket là **tăng tốc** câu đếm (12s trên 5.7 / 30s trên 8.0) | dev-impact | NEW-29, NEW-30 (chưa chạy); NEW-27 chỉ kiểm dạng câu lọc | RISK — chưa TC nào đo tốc độ; mọi run chạy ở local. Theo ghi chú của NEW-29/NEW-30, local là bản MySQL cũ hơn 5.7/8.0 → không kết luận được mục tiêu của ticket | `[MAJOR]` |
| G2 | F1 — `Conversation::advanceFilter` (bộ lọc cơ bản V1, vị trí sửa 1/6), lựa chọn loại 0 「いずれか1つ以上を含む」 | dev-impact | NEW-15 (pass, chỉ loại 1/2/3); NEW-12, NEW-13, NEW-14 (skip) | RISK — loại 0 của V1 không có TC nào được chấm. Run #2276: bộ lọc CŨ không còn trên UI, URL cũ vẫn đi `post-advance-filter-v2` (V2) → 3 TC UI không chạy được | `[MAJOR]` |
| G3 | F4 / T3 — `BroadcastController` + Delivery Target (SC-006): số người nhận | dev-impact | #20591 (pass, chỉ loại 0, 1 thẻ); #20600 (chưa chạy); NEW-26 (skip) | RISK — 2 lựa chọn loại trừ (NOT IN, rủi ro số 1 của Studio) chưa được kiểm trên màn gửi tin. Studio `dev_impact`: broadcast truyền `useDBReplicate=true` → là luồng khác với 友だちリスト | `[MAJOR]` |
| G4 | F5 / T4 — `ChatController:1740`: lọc hội thoại theo thẻ (talk list チャット管理) | dev-impact | #20593 (skip) | RISK — TC duy nhất bị skip (run #2276: runner không đặt được điều kiện thẻ trong modal của talk list チャット管理) và chỉ có loại 0 | `[MAJOR]` |
| G5 | F6 — nơi gọi `BotLineUser:28,695` · `BotLineUserPackage:27,526` · `FilterV2:1473,1480` | dev-impact | không map được | GAP — Input thiếu: Dev chỉ kê số dòng, không nói **tính năng/màn nào** đi qua 3 nơi gọi này → không viết được TC | `[MAJOR]` |
| G6 | Đặt lịch (lesson / salon): lọc **1 bạn bè** khớp bộ lọc — `filter_id_send_after_booking` (ẩn course), `filter_id_show_booking` (受付停止) | diff code | không có (NEW-25 là tự động trả lời, đi Java — xem §6) | GAP — Studio `dev_impact` kê "calendar-salon booking" trong phạm vi ảnh hưởng. Spec lesson `api-spec-public.md:128,932` xác nhận gọi `Conversation::advanceFilterPost()` giới hạn `[$lineUserId]`, `count() < 1` ⇒ ẩn course. Luồng này không có trong danh sách caller của Dev (mục 3) | `[BLOCKER]` |
| G7 | Khối tag (đã đổi cấu trúc câu lệnh) nằm trong CÙNG câu WHERE động với khối `対応ステータス` (`status_chat`, 1 trong 11 loại filter của cùng modal SC-003) — hỏi trực tiếp của human reviewer | diff code | NEW-21 (chỉ đối chứng tag + scenario/conversion/friend_info/day_add_friend) | RISK — chưa TC nào kết hợp filter tag với filter `対応ステータス` trên CẢ 3 màn dùng chung: 友だちリスト, 一斉配信, talk list チャット管理. Khối tag đổi từ `EXISTS`/`NOT EXISTS` sang `IN`/`NOT IN` + `GROUP BY` — nếu chuỗi mới sai ngoặc/dấu phẩy khi ghép với khối `status_chat` thì có thể âm thầm làm hỏng cả 2 điều kiện, không chỉ điều kiện tag | `[MAJOR]` |

> **Lưu ý phạm vi — 2 cơ chế "chat" khác nhau**: `/basic/chat-v3` ("Chat 1:1" FA-001) dùng filter sidebar riêng (`ConversationService@getFriend`, `havingRaw COUNT` — `chat-11/feature-spec.md` BR-04), **KHÔNG** gọi `Conversation::advanceFilter`/`advanceFilterPost` → **ngoài phạm vi diff #41573**, không cần TC cho ticket này. `/basic/talk-list` (talk list チャット管理, FA-002) mới dùng chung SC-003 qua `ChatController:1740` → **trong phạm vi**, đã tính ở G4/G7.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 14 quan điểm Trigger khớp task · 9 đủ · **5 chưa cover đủ**.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `BULK-001` | Cao | RISK — 2 TC đều skip: NEW-14 (bộ lọc CŨ không còn trên UI) và #20594. #20594 có ghi phạm vi đúng 3 người nhưng bước cuối (gắn thẻ) do job Java làm, và job chưa có branch để chạy. Chỉ có loại 0 | `[MAJOR]` |
| Q2 | `PERF-LARGE-001` | Trung bình → **Cao** (gửi tin / export / phân tích) | GAP — chỉ NEW-29/NEW-30 mang mã lạ `PERF-LATENCY-001`, cả 2 chưa chạy. Chưa có TC đo trên bot dữ liệu lớn với điều kiện giống query mẫu của ticket (2 khối loại trừ + ~200 thẻ + friend info) | `[BLOCKER]` |
| Q3 | `COMPAT-LEGACY-001` / RULE-09 | Cao | RISK — nhánh cũ V1 (`advanceFilter`) chỉ được phủ bởi NEW-12 (`RULE-09`, skip) và NEW-15 (`API-001`) — đều là mã lạ, và thiếu loại 0 (cùng gốc G2) | `[MAJOR]` |
| Q4 | `MSG-USER-001` | Cao | GAP — phía LINE user chỉ có NEW-25 (chưa chạy, đi job Java nên không qua code sửa). Chưa TC nào kiểm màn LINE user khi hệ thống lọc đúng 1 bạn bè bằng code PHP đã sửa (cùng gốc G6) | `[BLOCKER]` |
| Q5 | `REG-SHARED-001` | Cao | RISK — human reviewer hỏi trực tiếp: filter tag + filter `対応ステータス` (status_chat) + kết hợp cả 2 trên 友だちリスト / 一斉配信 / talk list チャット管理 chưa có TC nào (39 TC hiện có + kho `fa013`/`fa008` đều không có tổ hợp này — kho FA-013 chỉ có tổ hợp tag+QR ở TC-FRL-57). Cùng gốc G7 | `[MAJOR]` |

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-1 | #20592 → **gộp** | DUP-SUBSET | màn 友だちリスト · modal 「絞り込み」 tab AND · điều kiện thẻ loại 0 · loại trừ bạn đã chặn → đúng tập người. NEW-1 (2 thẻ, 8 bạn) bao trọn #20592 (1 thẻ, dữ liệu TC40948) | `[MINOR]` |

- **Gate đã chạy**: bỏ #20592 thì T2 vẫn còn NEW-1..NEW-11, `REG-SHARED-001` vẫn còn #20593/#20595/NEW-22/NEW-28 → coverage không đổi. Riêng bước "mở lại modal thấy đúng điều kiện đã lưu" của #20592 thì nên **chuyển sang NEW-1** trước khi xóa.
- Đã rà 39 TC, không có `DUP-EXACT` / `DUP-INFLATE`. NEW-7/NEW-9/NEW-10 (tab OR) không trùng NEW-1/NEW-3/NEW-4 (tab AND) vì nhánh OR là khối code riêng (`Conversation.php:1124`).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check | Expected TC | Nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-18 | Điều kiện 「選択したタグをすべて含む人」 (A+B) khi TC41573_F08 có **2 dòng trùng thẻ A**, không có thẻ B | F08 **có** trong kết quả (count(tag_id) không distinct đếm thành 2) — TC tự ghi "chỉ là regression compatibility, không phải business correctness" | `friend-filter/web/logic-spec.md:284` — `tag_filter_option.and_filter = 1`: "Tag: tất cả tag (AND)" → F08 thiếu thẻ B thì không khớp. Job Java dùng `count(distinct tag_id)` (Journal #138647) → số hiển thị trên web có thể khác tập nhận thật | (1) Hành vi cũ sai sẵn, Dev cố ý giữ → cần chốt quy tắc và mở ticket riêng · (2) Leader chấp nhận là hành vi hệ thống → NEW-18 giữ nguyên, spec ghi thêm ngoại lệ dữ liệu trùng | `[MAJOR]` | Leader / PM |

**Đã rà**: 39 TC × `spec-features/admin/friend-filter/web/logic-spec.md` (§5 config, §6 Business rules) + `spec-features/admin/lesson-booking` (luồng filter) + kho `fa013-friendlist` (nhóm "Lọc nâng cao 絞り込み" TC-FRL-52..58) · `fa003-tudongtraloi` (TC-RPL-53..63) · `fa008-broadcast` · `fa020-datlichsalon`. Không có `CONF-TC`: đã tính lại tập kết quả của toàn bộ TC dùng bộ 8 bạn TC41573_F01..F08, các số đều khớp nhau. Không có `CONF-KHO`: ngữ nghĩa 4 lựa chọn ở kho FA-003 (TC-RPL-58..62) khớp NEW-3/NEW-4/NEW-9/NEW-10.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn — kết quả thực thi | Chỉ 30/39 TC `pass` (77% < 80%): 5 skip (NEW-12, NEW-13, NEW-14, #20594, NEW-26) + 4 chưa chạy (NEW-25, #20600, NEW-29, NEW-30). Lúc review, run staging #2305 **đang chạy** → số liệu còn thay đổi | Chờ run #2305 xong rồi fetch lại. Không dùng tỷ lệ pass hiện tại để kết luận |
| I2 | `[MAJOR]` | Nguồn — môi trường (RULE-08 / performance) | 35/35 TC đã chạy đều ở `local`, 0 TC ở staging/production. Ticket là cải tiến **hiệu năng trên MySQL 5.7 / 8.0 với dữ liệu thật** — local không kết luận được | Chạy lại bộ lõi trên staging (run #2305) + chạy TC hiệu năng trên môi trường có MySQL 5.7/8.0 và dữ liệu lớn (G1 / Q2) |
| I3 | `[MAJOR]` | NEW-12, NEW-13, NEW-14 | Tiền đề không còn đúng thực tế: build hiện tại **không còn** khu vực bộ lọc CŨ trên 友だちリスト (run #2276, có screenshot) → 3 TC không bao giờ chạy được | Hỏi Dev V1 `advanceFilter` còn đường UI nào không (§8 #4). Không còn → viết lại qua endpoint như NEW-15, hoặc xóa sau khi có TC-FUNC001-01 (§7) |
| I4 | `[MAJOR]` | #20597 | Không dựng lại được: tiền đề "một bản ghi sử dụng bộ lọc đã lưu", bước 1 "mở một màn hình sử dụng modal…" — không nêu màn nào, số người bao nhiêu. Expected "hiển thị đúng" không đo được | Ghi rõ màn (vd 一斉配信), dữ liệu (bộ 8 bạn TC41573), điều kiện và số người kỳ vọng |
| I5 | `[MAJOR]` | #20601 | Expected bước 4 "kết quả đúng theo quy tắc AND/OR của spec" không đo được. Bước 5 "toán tử AND NOT" không nói chọn lựa chọn 「条件」 nào trong 4 lựa chọn của modal | Ghi con số kỳ vọng cho bước 4 (theo dữ liệu tiền đề: AND(A) ∩ OR(B) = F02) và ghi đúng label lựa chọn ở bước 5 |
| I6 | `[MINOR]` | NEW-3, NEW-4, NEW-9, NEW-16, NEW-20 | Mã `DATA-DB-001` (Trigger: có UPDATE/DELETE) không đúng — task chỉ đổi câu SELECT (file 03 mục 4.2). Map sai làm coverage quan điểm lệch | Đổi sang `FUNC-001` (NEW-3/4/9/16) và `DATA-COUNT-001` hoặc giữ ở nhóm data (NEW-20) |

---

## 6. TCs thừa / ngoài phạm vi task

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | NEW-25 | Test layer **không bị chạm code**: tự động trả lời kiểm bộ lọc bằng job Java, không qua `Conversation.php` | `spec-features/admin/auto-reply/job/job-spec.md:235,247-249` — `checkFilterV2()` → `LineUserModel.isValidFilterV2(...)` (Java). Mâu thuẫn với Studio `REQ-009` (ghi PHP `HelperService`) → §8 #3 | Nếu Dev xác nhận đi Java: bỏ khỏi task, luồng "lọc 1 bạn bè" thay bằng TC đặt lịch ở G6. Nếu thật ra đi PHP: giữ và đổi `Chạy` = auto (bước bạn bè gửi tin trên LINE runner mô phỏng được) | `[MINOR]` |
| X2 | NEW-26 | Diagnostic Web ↔ Job: chính TC ghi "không dùng để fail #41573". Lượt 2 chỉ quan sát job Java (không bị sửa) khi có dòng thẻ NULL | Studio note của NEW-26 + `dev_impact` không kê job Java | Chuyển thành ticket điều tra riêng (§8 #5), không chạy mỗi vòng fix | `[NIT]` |

- **Gate đã chạy**: NEW-25 là TC duy nhất gắn `MSG-USER-001`, nhưng nó **không đi qua code sửa** nên thực chất không cover được gì → quan điểm đó đã được mở lại ở Q4 / G6, không bị mất. NEW-26 không phải TC duy nhất của mục nào (lượt 1 trùng ý với #20591 / NEW-9).
- #20600 (gửi thật bằng job Java) **không** flag: là regression lấy từ kho (`OUT-TRUTH-001`, so số hiển thị do PHP tính với tập người nhận thật).

---

## 7. TCs đề xuất bổ sung (11)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa013-friendlist-友だちリスト.md` (Coverage 16 nhóm + nhóm "Lọc nâng cao" / "Bulk action" / "Elasticsearch") · `fa003-tudongtraloi-自動応答.md` (TC-RPL-47..63) · `fa008-broadcast-メッセージ配信.md` (TC-BC-17/19) · `fa020-datlichsalon` · `fa019-datlichbaihoc` · `fa001-chat11-11チャット.md` (nhóm "Modal 絞り込み — tag & trạng thái", để xác nhận đây là màn `/basic/chat-v3` KHÁC màn talk list チャット管理, không dùng làm nguồn cho G7/Q5) |
| Vùng regression phát hiện từ kho | FA-008 TC-BC-19 (cột 配信数 = filter_number) → dùng làm oracle cho TC-MSG001-01 · FA-013 TC-FRL-58 (điều kiện lọc truyền sang bulk action) → cơ sở TC-BULK001-01 · FA-013 TC-FRL-57 (tổ hợp tag + QR code) là tiền lệ **duy nhất** kho có test tổ hợp filter khác loại, nhưng KHÔNG có tổ hợp tag + `対応ステータス` → G7/Q5 là GAP thật, không dùng lại được TC kho |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không — kho FA-003 TC-RPL-53..63 là ma trận đầy đủ cho tự động trả lời, nhưng luồng đó đi Java (X1) nên không dùng để lấp G6 |
| Căn cứ TC regression `R<x>` | Không có TC R riêng — mọi vùng regression đã thành dòng G/Q |
| G1 | Đã có NEW-29 (đo 2 nhánh cùng dữ liệu) → không đẻ TC trùng (5b). TC-PERFLARGE001-01 lấp Q2 (đo trên production theo đúng dạng query của ticket) và dùng chung làm bằng chứng cho G1 |
| G5 | **Không đề xuất TC** — Input thiếu: chưa biết tính năng nào đi qua 3 nơi gọi (§8 #6). Có danh sách thì bổ sung ở round 2 |
| G7 / Q5 | TC-REGSHARED001-05/06/07 lấp tổ hợp filter tag + `対応ステータス` cho cả 3 màn human hỏi trực tiếp: 友だちリスト, 一斉配信, talk list チャット管理. `/basic/chat-v3` KHÔNG lấp vì ngoài phạm vi diff (xem note dưới §1) |
| Xác nhận chống trùng | Đã đối chiếu 39 TC ở BƯỚC 0 + kho — không TC đề xuất nào trùng. TC-MSG001-01 khác #20591 (loại trừ, không phải loại 0); TC-REGSHARED001-01 khác #20593 (loại 2); TC-FUNC001-01 bổ sung loại 0 mà NEW-15 thiếu; TC-REGSHARED001-05/06/07 khác mọi TC hiện có vì là TC tổ hợp 2 loại filter đầu tiên ngoài tag+tag |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | API | FUNC-001 | 友だちリスト — bộ lọc cơ bản V1 (advanceFilter) | Normal | auto | Tất cả | Bộ lọc cơ bản V1 lựa chọn loại 0 có ít nhất 1 thẻ trả đúng tập bạn bè qua endpoint | Dùng bộ 8 bạn TC41573_F01..F08 và 3 thẻ TC41573_TAG_A/B/C như NEW-1 (F06 đã chặn). Đăng nhập admin bằng phiên thật trên bot test. Đã ghi kết quả của nhánh gốc release_step_20260827 cho 2 lượt | 1. Gọi cùng endpoint bộ lọc CŨ mà NEW-15 dùng, danh sách thẻ = TAG_A, trường loại điều kiện thẻ = 0. 2. Ghi số bạn và danh sách trả về. 3. Gọi lại với danh sách thẻ = TAG_A và TAG_B, loại = 0. 4. Ghi số bạn và danh sách. 5. So với nhánh gốc | Lượt 1: TAG_A · Lượt 2: TAG_A + TAG_B · loại điều kiện = 0 | Cả 2 lượt HTTP 200. Lượt 1: 4 bạn — F01, F02, F03, F08. Lượt 2: 5 bạn — F01, F02, F03, F04, F08 (phép hợp, không phải giao). F05, F07 không có; F06 không có vì đã chặn. Không lỗi SQL. Trùng khít nhánh gốc | | Lấp G2 · Lấp Q3 · Vị trí sửa 1/6 (Conversation.php:188) · Bổ sung loại 0 mà NEW-15 thiếu · Đánh giá spec: Spec ghi rõ (logic-spec.md:283 or_filter=0) · Evidence: response JSON 2 lượt + response nhánh gốc |
| TC-MSG001-01 | UI | MSG-001 | 一斉配信 — 絞り込み điều kiện lọc đối tượng gửi | Normal | auto | Tất cả | Tin gửi hàng loạt đếm đúng số người nhận với 2 lựa chọn loại trừ thẻ | Bộ 8 bạn TC41573 như NEW-1. Có 1 tin 一斉配信 nháp, giờ gửi cách lúc test ít nhất 30 phút. Đã ghi số đếm của màn 友だちリスト cho cùng 2 điều kiện | 1. Mở tin nháp ở màn 一斉配信, mở modal 「絞り込み」. 2. Tab 「全て満たす」 thêm 「タグ」 = TAG_A, 「条件」 = 「選択したタグを1つ以上含む人を除外」, bấm 「保存」. 3. Đọc số người nhận trên màn soạn tin. 4. Mở tab 配信予約, đọc cột 配信数 của tin này. 5. Sửa điều kiện: 「タグ」 = TAG_A + TAG_B, 「条件」 = 「選択したタグを全て含む人を除外」, bấm 「保存」. 6. Lặp lại bước 3–4 | Lượt 1: TAG_A, loại trừ ≥1 thẻ · Lượt 2: TAG_A + TAG_B, loại trừ đủ tất cả | Lượt 1: số người nhận = 3 (F04, F05, F07), cột 配信数 cũng = 3. Lượt 2: = 5 (F01, F04, F05, F07, F08), 配信数 = 5. Không lượt nào ra 0. Mỗi số bằng đúng số đếm của 友だちリスト với cùng điều kiện | | Lấp G3 · Luồng broadcast dùng useDBReplicate=true (Studio dev_impact) — khác luồng 友だちリスト · regression dẫn từ TC-BC-19 (配信数 = filter_number) · Đánh giá spec: Spec ghi rõ (logic-spec.md §5 broadcast → filter_number) · Evidence: screenshot màn soạn tin + tab 配信予約 |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | talk list チャット管理 — 絞り込み điều kiện lọc bạn bè | Normal | auto | Tất cả | Danh sách hội thoại lọc theo thẻ loại trừ trả đúng hội thoại, không rỗng | Bộ 8 bạn TC41573 như NEW-1; cả 8 bạn đều đã có ít nhất 1 tin trong hội thoại với bot | 1. Mở màn danh sách hội thoại (talk list チャット管理) của bot test. 2. Mở modal lọc, tab 「全て満たす」 thêm 「タグ」 = TAG_A, 「条件」 = 「選択したタグを1つ以上含む人を除外」. 3. Bấm 「保存」, đợi danh sách nạp lại. 4. Liệt kê tên từng hội thoại còn lại. 5. Mở lại modal, kiểm tra điều kiện | TAG_A · loại trừ ≥1 thẻ | Chỉ còn hội thoại của F04, F05, F07. Không có F01, F02, F03, F08 (mang A). Danh sách không rỗng. Mở lại modal thấy đúng 1 điều kiện thẻ vừa lưu. Không lỗi hệ thống | | Lấp G4 · Caller ChatController:1740 (file 03 mục 3) · #20593 bị skip vì runner không đặt được điều kiện thẻ trong modal — cần sửa cách thao tác trước khi chạy · Đánh giá spec: Spec ghi rõ · Evidence: screenshot danh sách + modal |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | レッスン予約 — 「コースの絞り込み表示」 (lọc course theo bạn bè) | Normal | auto | Tất cả | Course có bộ lọc loại trừ thẻ chỉ ẩn với bạn mang thẻ, vẫn hiện với bạn không mang thẻ | Bot gói Standard hoặc Pro. 1 lịch レッスン予約 có 2 course đang hiển thị: COURSE_X và COURSE_Y. 2 tài khoản LINE đã kết bạn: LU_A đang mang TAG_A, LU_0 không mang thẻ nào | 1. Mở màn chỉnh sửa COURSE_X, khối 「コースの絞り込み表示」, bấm 「絞り込み条件 登録・編集」. 2. Thêm 「タグ」 = TAG_A, 「条件」 = 「選択したタグを1つ以上含む人を除外」, bấm 「保存」. 3. Đọc 「対象人数」. 4. Lưu course. 5. Từ LU_0 mở trang đặt lịch của lịch này. 6. Từ LU_A mở cùng trang | TAG_A · loại trừ ≥1 thẻ | Bước 3: 対象人数 = số bạn chưa chặn không mang TAG_A, bằng số của 友だちリスト với cùng điều kiện, không phải 0. Bước 5: LU_0 thấy cả COURSE_X và COURSE_Y. Bước 6: LU_A chỉ thấy COURSE_Y, không thấy COURSE_X. Không trang nào lỗi | | Lấp G6 · Lấp Q4 · Spec lesson api-spec-public.md:128 (advanceFilterPost giới hạn [lineUserId], count < 1 ⇒ loại course) + :932 · Nhánh nguy hiểm: nếu NOT IN trả rỗng sai thì LU_0 mất COURSE_X · Salon có parent_type tương tự (calendar-salon-course-setting-status-send-after-booking) → hỏi Dev có cần TC riêng · Đánh giá spec: Spec ghi rõ · Evidence: screenshot admin + màn LINE của 2 tài khoản |
| TC-REGSHARED001-03 | UI | REG-SHARED-001 | レッスン予約 — 「コースの絞り込み表示」 (lọc course theo bạn bè) | Boundary | auto | Tất cả | Course lọc loại trừ người có đủ tất cả thẻ vẫn hiện với bạn chỉ có một phần thẻ | Như TC-REGSHARED001-02. Thêm tài khoản LINE LU_AB mang TAG_A + TAG_B. LU_A chỉ mang TAG_A | 1. Sửa bộ lọc của COURSE_X: 「タグ」 = TAG_A + TAG_B, 「条件」 = 「選択したタグを全て含む人を除外」, bấm 「保存」, lưu course. 2. Từ LU_AB mở trang đặt lịch. 3. Từ LU_A mở trang. 4. Từ LU_0 mở trang | TAG_A + TAG_B · loại trừ đủ tất cả | LU_AB không thấy COURSE_X. LU_A (thiếu TAG_B) và LU_0 (không thẻ) đều thấy COURSE_X — chưa đủ tập thẻ nên không bị loại | | Lấp G6 · Lấp Q4 · Biên "có một phần thẻ" / "0 thẻ" (rủi ro số 2 của Studio dev_impact) trên luồng lọc 1 bạn bè · Đánh giá spec: Spec ghi rõ (logic-spec.md:286 and_not_filter=3) · Evidence: screenshot màn LINE của 3 tài khoản |
| TC-REGSHARED001-04 | UI | REG-SHARED-001 | レッスン予約 — 「コースの絞り込み表示」 (lọc course theo bạn bè) | Abnormal | auto | Tất cả | Course lọc loại trừ thẻ khi bảng thẻ có dòng thiếu mã bạn bè vẫn hiện với bạn không mang thẻ | Như TC-REGSHARED001-02. Có sẵn 1 dòng trong bảng thẻ với mã thẻ TAG_A và mã bạn bè để trống, dựng giống NEW-16 | 1. Xác nhận dòng thẻ thiếu mã bạn bè đang tồn tại. 2. Bộ lọc COURSE_X: 「タグ」 = TAG_A, 「条件」 = 「選択したタグを1つ以上含む人を除外」, lưu. 3. Từ LU_0 mở trang đặt lịch. 4. Từ LU_A mở trang | TAG_A · loại trừ ≥1 thẻ · 1 dòng thẻ thiếu mã bạn bè | LU_0 vẫn thấy COURSE_X. LU_A không thấy COURSE_X. Nếu LU_0 cũng không thấy thì phép loại trừ đã bị rỗng sai — phải báo ngay | | Lấp G6 · Rủi ro số 1 của Studio dev_impact (NOT IN + NULL) trên luồng lọc 1 bạn bè — NEW-16 mới chỉ kiểm ở 友だちリスト · Đánh giá spec: Spec ghi rõ · Evidence: screenshot màn LINE 2 tài khoản |
| TC-BULK001-01 | Job | BULK-001 | 友だちリスト — 友だち一括アクション (bulk action) | Normal | auto | Tất cả | Bulk action gắn thẻ với bộ lọc loại trừ đủ tất cả thẻ chỉ tác động đúng người khớp | Bộ 8 bạn TC41573 như NEW-1. Thẻ đích TAG_BULK chưa gắn cho ai. Môi trường có job xử lý bulk action đang chạy (run #2276: job chưa có branch → phải có trước khi chạy) | 1. Ở 友だちリスト mở modal 「絞り込み」, tab 「全て満たす」 thêm 「タグ」 = TAG_A + TAG_B, 「条件」 = 「選択したタグを全て含む人を除外」, bấm 「保存」. 2. Đọc số người. 3. Tích 全選択, mở 友だち一括アクション, thêm hành động gắn thẻ TAG_BULK, chạy. 4. Chờ job xong. 5. Lọc 友だちリスト theo TAG_BULK | TAG_A + TAG_B · loại trừ đủ tất cả · thẻ đích TAG_BULK | Bước 2: 5 người. Bước 5: đúng F01, F04, F05, F07, F08 mang TAG_BULK. F02, F03 (đủ A và B) không bị gắn; F06 (đã chặn) không bị gắn. Không gắn cho toàn bộ bạn, không để trống | | Lấp Q1 · Phạm vi người được đưa vào hành động do PHP tính (code sửa), bước gắn thẻ do job Java (không sửa) · regression dẫn từ TC-FRL-58 · Đánh giá spec: Spec ghi rõ · Evidence: screenshot số người + danh sách lọc theo TAG_BULK |
| TC-PERFLARGE001-01 | UI | PERF-LARGE-001 | 友だちリスト — 「絞り込み」 số đếm trên bot dữ liệu lớn | Normal | manual | product | Số đếm bộ lọc theo thẻ trên bot lớn hiện ra nhanh hơn trước release và không đổi giá trị | Bot production có số bạn lớn và nhiều thẻ, Leader chọn (vd bot của query mẫu trong ticket). TRƯỚC khi deploy đã đo và ghi số đếm + thời gian cho đúng bộ điều kiện ở bước 2 | 1. Sau deploy, mở 友だちリスト của bot đó, mở modal 「絞り込み」. 2. Tab 「全て満たす」 thêm: 「タグ」 3 thẻ loại 「選択したタグを1つ以上含む人を除外」; 「タグ」 ~200 thẻ loại 「選択したタグのいずれか1つ以上を含む人」; 「タグ」 9 thẻ loại 「選択したタグを1つ以上含む人を除外」; 「友だち情報」 kiểu số ≤ 180. 3. Bấm 「保存」, đo thời gian đến khi số đếm hiện. 4. Lặp 5 lần, ghi min / trung vị / max. 5. Làm lại với 一斉配信 (số người nhận) | Bộ điều kiện dạng query mẫu Redmine #41573 | Số đếm sau deploy bằng đúng số đo trước deploy (dữ liệu không đổi trong lúc đo). Trung vị thời gian nhỏ hơn rõ so với trước deploy (mốc ticket 12s trên 5.7 / 30s trên 8.0). Không bị timeout, không màn lỗi | | Lấp Q2 · Làm bằng chứng cho G1 · Chỉ Normal — hiệu năng không có biên / abnormal có nghĩa riêng (biên phiên bản DB đã có NEW-30) · RULE-08 performance · manual vì môi trường production · Đánh giá spec: Spec không ghi — chưa có ngưỡng giây, Leader chốt · Evidence: bảng thời gian 5 lần trước/sau + screenshot số đếm |
| TC-REGSHARED001-05 | UI | REG-SHARED-001 | 友だちリスト — kết hợp filter タグ và filter 対応ステータス | Normal | auto | Tất cả | Kết hợp filter tag (loại 0) và filter 対応ステータス trả đúng phép giao của 2 nhóm | Bộ 8 bạn TC41573_F01..F08 + 3 thẻ TAG_A/B/C như NEW-1. Gán thêm 対応ステータス = TC41573_STATUS_X cho F02, F04, F07 (các bạn còn lại không có status). Đã đếm tay: tag loại 0 (A hoặc B) = F01,F02,F03,F04,F08; status = STATUS_X → giao = F02, F04 | 1. Mở 友だちリスト, mở modal 「絞り込み」. 2. Tab 「全て満たす」 thêm 「タグ」 = TAG_A + TAG_B, 「条件」 = 「選択したタグのいずれか1つ以上を含む人」. 3. Cùng tab, thêm tiếp 「対応ステータス」 = STATUS_X. 4. Bấm 「保存」. 5. Đọc số đếm và danh sách. 6. Mở lại modal, xác nhận còn đủ 2 điều kiện | TAG_A + TAG_B (loại 0) · 対応ステータス = STATUS_X | Số đếm = 2, danh sách gồm đúng F02 và F04 (2 người vừa có tag vừa đúng status). F01, F03, F08 (có tag, sai status) và F07 (đúng status, không tag) đều KHÔNG có mặt. F06 không có vì đã chặn. Mở lại modal còn đủ 2 điều kiện, không mất điều kiện nào. Không lỗi SQL | | Lấp G7 · Lấp Q5 · Khối tag đổi cấu trúc EXISTS→IN nằm cùng WHERE với khối status_chat chưa sửa — kiểm không vỡ khi ghép chung · Đánh giá spec: Spec ghi rõ (logic-spec.md §6.2 kết quả cuối = AND của các khối) · Evidence: screenshot số đếm + danh sách + modal mở lại |
| TC-REGSHARED001-06 | UI | REG-SHARED-001 | 一斉配信 — kết hợp filter タグ và filter 対応ステータス | Normal | auto | Tất cả | Kết hợp filter tag (loại trừ) và filter 対応ステータス đếm đúng số người nhận trên màn gửi tin | Như TC-REGSHARED001-05 (F02, F04, F07 mang STATUS_X). Có 1 tin 一斉配信 nháp. Đã đếm tay: loại trừ TAG_A (chỉ giữ người KHÔNG mang A, chưa chặn) = F04, F05, F07; giao với STATUS_X (F02,F04,F07) = F04, F07 | 1. Mở tin nháp ở 一斉配信, mở modal 「絞り込み」. 2. Tab 「全て満たす」 thêm 「タグ」 = TAG_A, 「条件」 = 「選択したタグを1つ以上含む人を除外」. 3. Cùng tab thêm 「対応ステータス」 = STATUS_X. 4. Bấm 「保存」. 5. Đọc số người nhận trên màn soạn tin. 6. Mở tab 配信予約, đọc cột 配信数 | TAG_A loại trừ · 対応ステータス = STATUS_X | Số người nhận = 2 (F04, F07). Cột 配信数 cũng = 2, không lệch số hiển thị trên màn soạn tin. F02 (đúng status, có tag A) và F05 (không status) không có mặt | | Lấp G7 · Lấp Q5 · Broadcast dùng useDBReplicate=true (khác luồng 友だちリスト) nên vẫn cần test riêng dù cùng logic · Đánh giá spec: Spec ghi rõ · Evidence: screenshot màn soạn tin + tab 配信予約 |
| TC-REGSHARED001-07 | UI | REG-SHARED-001 | talk list チャット管理 — kết hợp filter タグ và filter 対応ステータス | Normal | auto | Tất cả | Kết hợp filter tag (loại 0) và filter 対応ステータス trả đúng danh sách hội thoại | Như TC-REGSHARED001-05. Cả 8 bạn đều đã có ít nhất 1 tin trong hội thoại với bot | 1. Mở talk list チャット管理, mở modal lọc. 2. Thêm 「タグ」 = TAG_A + TAG_B, 「条件」 = 「選択したタグのいずれか1つ以上を含む人」. 3. Cùng khối thêm 「対応ステータス」 = STATUS_X. 4. Bấm 「保存」. 5. Liệt kê hội thoại còn lại. 6. Mở lại modal xác nhận còn đủ 2 điều kiện | TAG_A + TAG_B (loại 0) · 対応ステータス = STATUS_X | Chỉ còn hội thoại của F02 và F04. Không có F01, F03, F08 (có tag, sai status), không có F07 (đúng status, không tag). Danh sách không rỗng, không lỗi hệ thống. Mở lại modal còn đủ 2 điều kiện | | Lấp G7 · Lấp Q5 · Caller ChatController:1740 · Cần thao tác đặt điều kiện thẻ trong modal talk list チャット管理 khác cách #20593 đã thử (đang skip) — ghi rõ cách bấm nếu #20593 vẫn không mở được · Đánh giá spec: Spec ghi rõ · Evidence: screenshot danh sách + modal |

---

## 8. Spec update needed

| # | Section spec / nguồn | Nội dung cần chốt | Nguồn | Ai chốt |
|---|---|---|---|---|
| 1 | `friend-filter/web/logic-spec.md` §5 (`tag_filter_option.and_filter`) | Quy tắc 「選択したタグをすべて含む人」 khi `tag_line_user` có dòng trùng (bạn, thẻ): đếm theo dòng (web, hành vi cũ) hay theo thẻ khác nhau (job Java, `count(distinct)`). Hiện số hiển thị web có thể khác tập nhận thật | C1 `CONF-SPEC` (NEW-18) · Journal #138647 TỰ REVIEW | Leader / PM |
| 2 | `03-dev-impact.md` mục 3 / 4.1 | `ConversationReplicate::advanceFilter` / `advanceFilterPost` có nơi gọi không? NEW-28 grep: không có — đọc replica làm bên trong lớp chính bằng cách đổi model. Nếu đúng thì 3 vị trí replica là code chết | NEW-28 (Studio REQ-011) vs file 03 | Dev |
| 3 | `auto-reply/job/job-spec.md:235-249` vs Studio `REQ-009` | Tự động trả lời kiểm bộ lọc ở Java (`isValidFilterV2`) hay PHP (`HelperService:146,548`)? Quyết định NEW-25 có thuộc phạm vi không (X1) | §6 X1 | Dev |
| 4 | `friend-filter/web/logic-spec.md` §6.1 (V1 vs V2) | V1 `advanceFilter` còn đường gọi thật nào (UI / mobile / broadcast cũ `filter.js:612`)? Run #2276: URL bộ lọc cũ đi V2. Không còn → cập nhật spec + xóa NEW-12/13/14 | I3 · G2 | Dev |
| 5 | Job Java gửi tin (linect-service `LineUserModel.buildWhere`) | NEW-26 lượt 2: bảng thẻ có dòng `line_user_id = NULL` thì câu `NOT IN` phía Java có thể trả rỗng → tin gửi hàng loạt có điều kiện loại trừ **có thể không gửi cho ai**. Là lỗi có sẵn, ngoài #41573 — cần Dev xác nhận và mở ticket riêng nếu đúng | X2 (NEW-26) | Dev |
| 6 | `03-dev-impact.md` mục 3 | Kê **tính năng/màn** đi qua `BotLineUser:28,695` · `BotLineUserPackage:27,526` · `FilterV2:1473,1480`, và bổ sung caller đặt lịch (`CalendarController` lesson/salon — `filter_id_show_booking`, `filter_id_send_after_booking`) còn thiếu trong danh sách | G5 · G6 | Dev |
