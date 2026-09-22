# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #230 (ticket 35932, round 1, `done-ai`, reviewState `leader`) |
| Tổng số TC review | 7 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: 9/15 vùng ảnh hưởng đủ TC · 4 GAP · 2 RISK

> `Input thiếu: không có diff` — Studio `spec_delta.diffAvailable = false` (không tìm thấy ref `release-t07-2026`). Chiều (b) suy từ `dev_impact` của Studio + mục 1/2/3 file 03 + file điều tra đính kèm Redmine.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | T4 — **unsend** tin gửi qua luồng delay | `dev-impact` | `NEW-17` (blocked) | `RISK` — NEW-17 blocked, actual: "Chat 11: ko có phần thu hồi msg" → màn chat 1:1 admin không có thao tác thu hồi tin của bot. Chưa rõ Dev nói "unsend" ở 4.3 là luồng nào | `[MAJOR]` |
| G2 | T5 — **hành vi đổi**: template group bật `is_delay_sent_message` gửi qua lịch có delay → gửi hết message con 1 lần, không giãn từng con | `dev-impact` + `diff code` (câu hỏi 4) | `NEW-11` | `RISK` — NEW-11 chỉ "ghi lại" mốc giờ message con, không chốt expected cho hành vi MỚI; pass mà không có actual/evidence | `[MAJOR]` |
| G3 | `SentMessageHelper.checkError` (:572) — mục 3 file 03: sau fix mới match được tin luồng delay → **đường ghi lỗi gửi** thay đổi | `diff code` (câu hỏi 2 — nhánh lỗi) | không có | `GAP` — 0 TC cho nhánh gửi thất bại của luồng delay (Studio REQ-013 cũng chưa có TC) | `[MAJOR]` |
| G4 | Hàm dùng chung `DelayMessageService.startJobAddMessageToQueue` — mọi bản ghi `send_random_messages` đều đi qua (nguồn `MessageBuilder:167`: template group bật delay gửi từ các đường khác) | `diff code` (câu hỏi 3) | `NEW-12` (chỉ auto reply) | `GAP` — Dev **không kê danh sách đường gửi** sinh `send_random_messages`; đường phổ biến nhất là **chat 1:1 gửi ngay template group bật delay** (kho TC-CHT-228) chưa có TC | `[MAJOR]` |
| G5 | Bản ghi tin luồng delay tạo **TRƯỚC** fix (`replace_content` rỗng, thiếu `quote_token`/`message_line_capture`) — `dev_impact` Studio + REQ-008 | `diff code` | không có | `GAP` — không TC nào phân biệt bản ghi cũ và mới sau deploy | `[MAJOR]` |
| G6 | Preview tin cuối ở **danh sách bạn bè (cột trái)** chat 1:1 — cùng đọc `replace_content` (Studio REQ-010, `TalkListController:419-470`) | `diff code` | không có | `GAP` — mọi TC chỉ xem khung hội thoại | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 9 quan điểm Trigger khớp task · 3 chưa cover đủ

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FRIEND-001` | Cao | `RISK` — chỉ có `Normal` (NEW-1); case "không có giá trị" bị gộp trong NEW-1 dataset B; thiếu `Abnormal` riêng (friend info bị xóa sau khi đặt lịch) + `Boundary` (group tối đa message con, đủ các TYPE: date / point / email / SĐT / địa chỉ) — RULE-01 | `[MAJOR]` |
| Q2 | `SYNC-APP-001` | Trung bình → **Cao** (chat là flow critical user-facing) | `GAP` — MAP-FI-10 yêu cầu kiểm **3 nơi**: LINE user / chat 1:1 web / **chat 1:1 app admin mobile**. Chưa TC nào xem app mobile (NEW-8 mang mã này nhưng test LINE quote, không phải app) | `[BLOCKER]` |
| Q3 | `MSG-002` | Cao | `RISK` — chỉ `Normal` (NEW-11); thiếu `Boundary` về **vị trí template group trong lịch** (giữa / cuối, nhiều group) và `Abnormal` | `[MAJOR]` |

- Đã xét, không flag: `MSG-004` (có đối chiếu LINE ở NEW-1/9/11/12 — thiếu evidence đưa xuống §4 I1) · `REG-SHARED-001` (gộp vào G4) · `COMPAT-LEGACY-001` (cặp group/không group đã có ở NEW-1; bản ghi cũ = G5) · `JOB-001` (fix không chạm retry/rate limit; môi trường đưa xuống §4 I2) · `OUT-TRUTH-001` (NEW-7).

---

## 3. TC trùng lặp nội dung

Đã rà 7 TC, không phát hiện trùng lặp. (NEW-7 = admin trích dẫn trên web, NEW-8 = bạn bè trích dẫn từ LINE → khác đối tượng thao tác; NEW-9 / NEW-12 cùng mã `REG-SHARED-001` nhưng khác đường gửi.)

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | 6 TC pass (NEW-1, 7, 8, 9, 11, 12) | **RULE-02**: `task_get_report` cho thấy cả 6 kết quả manual pass đều `evidence: []`, `actual: null` — kết quả tự khai, riêng NEW-1 yêu cầu đối chiếu chat/LINE/DB mà không có ảnh nào | Đính kèm screenshot chat 1:1 + LINE app (iOS và Android — MSG-004) cho từng TC, rồi submit lại kết quả |
| I2 | `[MAJOR]` | Toàn bộ 7 TC | **RULE-08 / ENV-003**: 7/7 chạy `local`, 0 run staging/production; luồng bị sửa là **job nền** (`DelayMessageService`). NEW-1 còn ghi tiền đề "đã xác nhận **staging** chạy bản job chứa fix" nhưng lại chạy trên local | Chạy lại tối thiểu NEW-1, NEW-9, NEW-11 trên staging (có sẵn dữ liệu repro bot 562 / user 131204); sau release chạy lại NEW-1 trên production |
| I3 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill từ Redmine (`2026-09-19 by /new-task`) nhưng checkbox "Tester verify auto-fill chính xác" chưa tick — F/D/T có thể thiếu hoặc map sai | Tester đọc lại Journal #132627 + tick checkbox |
| I4 | `[MAJOR]` | Dữ liệu `messages_v2s` luồng delay | **RULE-04**: bug làm **sai dữ liệu đã lưu** (`replace_content` rỗng, thiếu `quote_token` / `message_line_capture`) cho mọi tin gửi qua luồng delay bằng template group trước fix. Chưa có số liệu phạm vi toàn hệ thống, chưa có quyết định recovery | Yêu cầu Dev query thống kê số bản ghi bị ảnh hưởng (theo bot/khoảng thời gian); Leader quyết định recovery hay chấp nhận. Kết quả quyết định expected của TC-COMPATLEGACY001-01 ở §5 |
| I5 | `[MAJOR]` | `NEW-17` | TC dựa trên thao tác **không tồn tại** (blocked: "Chat 11: ko có phần thu hồi msg"). Tiêu đề/steps giả định admin thu hồi tin bot | Hỏi Dev "unsend" ở 4.3 là luồng nào (xem §6 #5). Không có luồng thật → `testcase_delete` NEW-17 trên Studio; có → sửa steps theo đúng luồng |
| I6 | `[MAJOR]` | `NEW-1` | **Không atomic**: 8 bước gồm 2 dataset khác mục đích (A = template group có giá trị; B = template đơn + friend info rỗng) + đối chiếu DB. Fail 1 phần thì không biết phần nào; dataset B thực chất là case `Abnormal` của FRIEND-001 nhưng bị gộp trong case `Normal` | Tách dataset B thành TC riêng (`case_type = Abnormal`) trên Studio, NEW-1 giữ dataset A |
| I7 | `[MAJOR]` | `NEW-11` | Expected **không đo lường được** ở phần message con: "Thời điểm gửi … phải được GHI LẠI để báo cáo leader/PO" → TC pass mà không có actual/mốc giờ nào được ghi | Chờ §6 #1 chốt hành vi, rồi sửa expected thành số đo cụ thể (VD "3 message con hiển thị cùng giây" hoặc "cách nhau 2-4 giây") |
| I8 | `[MINOR]` | NEW-1, NEW-9, NEW-12, NEW-17 | Expected dẫn bằng field DB (`replace_content`, `rp_key/rp_value`, `quote_token`, `message_line_capture`) — manual tester không tự kiểm được | Diễn đạt bằng dấu hiệu quan sát được: icon trả lời hiện trên tin, trích dẫn dựng đúng nội dung (như NEW-7/NEW-8); phần DB để Dev xác nhận |
| I9 | `[MINOR]` | NEW-1, NEW-17 | `env_tag = local-only`, `env_scope = all` nhưng tiền đề ghi "staging" → khai báo môi trường không nhất quán | Thống nhất `env_scope` với môi trường thực sự cần chạy |

---

## 5. TCs đề xuất bổ sung (8)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa001-chat11-11チャット.md` — nhóm "Đặt lịch gửi — delay & job" (TC-CHT-320…326), "Chèn friend info vào tin nhắn" (TC-CHT-176, 181), "Gửi template — nội dung & action" (TC-CHT-228), "Reply / quote message" (TC-CHT-240…255) |
| Vùng regression phát hiện từ kho | TC-CHT-228 (chat 1:1 gửi ngay template group bật delay — đi qua cùng `DelayMessageService`) → G4 · TC-CHT-181 (friend info khi gửi qua đặt lịch) → Q1 |
| Conflict expected vs kho | TC-CHT-322 ("tin ĐẦU TIÊN gửi ngay") vs `job-spec.md` §3.2 → đưa §6 #2 · MT-05 (2-4 vs 2-5 giây) → §6 #3. Không TC đề xuất nào phụ thuộc trực tiếp các con số này |
| GAP dùng lại TC kho (không viết mới) | Q3 Abnormal → dùng lại `TC-CHT-323` "Sửa thời gian gửi khi lịch ĐANG gửi dở", bổ sung: lịch chứa template group có mã friend info, kiểm các tin còn lại hiển thị giá trị đã thay |
| Xác nhận chống trùng | Đã đối chiếu 7 TC ở BƯỚC 0 + kho FA-001 — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Gửi template — nội dung & action | Normal | auto | Tất cả | Chat 1:1 gửi ngay template group bật gửi giãn cách ở màn template — mọi tin hiển thị giá trị friend info đã thay | - Môi trường đã deploy bản fix #35932<br>- Đăng nhập admin, chọn bot test, có friend test đã kết bạn<br>- Friend test đã có giá trị システム表示名 và 1 friend info tự tạo kiểu text<br>- Template group `TC35932_RS` gồm 3 message text con, **bật** tuỳ chọn gửi giãn cách trên màn template; mỗi con chứa 1 mã friend info | 1. Mở /basic/chat-v3, chọn friend test<br>2. Chọn template `TC35932_RS` và gửi ngay (không đặt lịch)<br>3. Chờ khoảng 15 giây cho job gửi các tin sau<br>4. Đọc nội dung 3 tin trên khung chat 1:1<br>5. Đối chiếu với 3 tin trên app LINE của friend<br>6. Rê chuột vào tin thứ 2 và thứ 3, xem có icon trả lời không | Con 1: 「こんにちは[システム表示名]さん」 · Con 2: 「会員区分:[friend info text]」 · Con 3: 「[システム表示名]様、ご確認ください」 | - Tin 1 gửi ngay, tin 2 và 3 tới sau vài giây<br>- Cả 3 tin trên chat 1:1 hiển thị giá trị thật, KHÔNG còn chuỗi `[FRIEND_INFO_...]`, nội dung giống hệt tin trên LINE<br>- Tin 2 và 3 có icon trả lời như tin 1<br>- Không có tin trùng hoặc tin rỗng | | Lấp G4 · regression — dẫn từ TC-CHT-228 · Đánh giá spec: Spec ghi rõ (chat-11 job-spec §3.2, MAP-SEND-07) · Evidence: screenshot chat 1:1 + LINE app |
| TC-MSG003-01 | UI | MSG-003 | Đặt lịch gửi — delay & job | Abnormal | auto | Tất cả | Friend chặn bot sau khi đã đặt lịch gửi có delay — không có tin hiển thị như gửi thành công, friend khác không bị ảnh hưởng | - Môi trường đã deploy bản fix<br>- 2 friend test A, B cùng bot, đều đã kết bạn<br>- Template group `TC35932_G1` (2 message con có mã friend info) | 1. Ở chat 1:1 của A và của B, mỗi người đặt 1 lịch gửi `TC35932_G1`, bật 「メッセージを1通ずつ数秒遅延させて送信する」, giờ gửi = hiện tại + 3 phút<br>2. Trước giờ gửi, friend A chặn bot trên LINE<br>3. Chờ qua giờ gửi<br>4. Mở chat 1:1 của A: đọc các tin của lịch<br>5. Mở màn 配信エラー (lỗi gửi tin) của bot, tìm theo friend A<br>6. Mở chat 1:1 của B, đối chiếu với LINE của B | A chặn bot · B bình thường | - Chat 1:1 của A: KHÔNG có tin nào của lịch hiển thị như đã gửi thành công<br>- Nếu hệ thống có gọi LINE và bị từ chối: tin của A xuất hiện ở màn 配信エラー đúng friend, đúng nội dung<br>- B nhận đủ 2 tin, chat 1:1 của B hiển thị giá trị friend info đã thay | | Lấp G3 · Đánh giá spec: Spec không ghi — cần Dev chốt ở §6 #4 (MAP-SEND-20 "không gửi" vs REQ-013 "ghi lỗi") · Evidence: screenshot chat A, B + màn 配信エラー |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Đặt lịch gửi — delay & job | Normal | auto | staging | Tin gửi qua lịch có delay TRƯỚC khi deploy fix và SAU khi deploy — màn chat 1:1 vẫn hiển thị ổn định, phân biệt được 2 loại | - Staging đã deploy bản fix #35932<br>- Bot 562, friend line_user_id 131204 còn tin cũ của lịch `schedule_send_chat.id = 697` (gửi 2026-08-24 11:30, trước fix)<br>- Template group 105649 (con 105650, 105651) còn tồn tại | 1. Mở chat 1:1 của friend 131204, cuộn tới các tin gửi lúc 2026-08-24 11:30<br>2. Quan sát nội dung và icon trả lời của các tin cũ<br>3. Đặt lịch mới với template group 105649, bật delay, giờ gửi = hiện tại + 3 phút, chờ gửi xong<br>4. So sánh tin mới với tin cũ trên cùng khung chat<br>5. Tải lại màn, mở preview cột trái của friend | Lịch cũ 697 · lịch mới do tester tạo | - Màn chat 1:1 tải bình thường, không lỗi, không trắng màn khi có tin cũ<br>- Tin **mới**: hiển thị 「msg 1」 + giá trị friend info đã thay, có icon trả lời<br>- Tin **cũ**: giữ nguyên như trước fix (hiện mã friend info) — **trừ khi Leader chốt recovery** (§4 I4), khi đó phải hiển thị giá trị đã thay | | Lấp G5 · RULE-04 · Đánh giá spec: Đã hỏi leader (chờ quyết định recovery) · Evidence: screenshot tin cũ + tin mới cùng khung chat |
| TC-MSG004-01 | UI | MSG-004 | Danh sách bạn bè — hiển thị | Normal | auto | Tất cả | Preview tin cuối ở danh sách bạn bè sau lịch gửi có delay — hiển thị giá trị friend info đã thay | - Môi trường đã deploy bản fix<br>- Friend test có giá trị システム表示名<br>- Template group `TC35932_G1`, **message con cuối** chứa 「[システム表示名]様」 | 1. Đặt lịch gửi `TC35932_G1` cho friend test, bật delay, giờ gửi = hiện tại + 3 phút<br>2. Chờ gửi xong, KHÔNG mở hội thoại friend<br>3. Tải lại /basic/chat-v3, đọc dòng preview tin cuối của friend ở cột trái<br>4. Mở hội thoại, đối chiếu với tin cuối trên khung chat | Con cuối: 「[システム表示名]様、ご確認ください」 | - Preview cột trái hiển thị 「<tên thật>様、ご確認ください」, KHÔNG hiện `[FRIEND_INFO_...]`<br>- Nội dung preview khớp tin cuối trên khung chat<br>- Friend được đẩy lên đầu danh sách theo thời điểm tin cuối | | Lấp G6 · MAP-SEND-21 (last_message) · Đánh giá spec: Spec ghi rõ (catalog MAP-SEND-21) · Evidence: screenshot cột trái + khung chat |
| TC-FRIEND001-01 | UI | FRIEND-001 | Chèn friend info vào tin nhắn | Abnormal | auto | Tất cả | Friend info bị xóa sau khi đã đặt lịch gửi có delay — vị trí mã để trống, không hiện mã thô | - Môi trường đã deploy bản fix<br>- Tạo friend info tự tạo kiểu text `TC35932_DEL`, friend test có giá trị 「ゴールド」<br>- Template group 2 message con: con 1 chứa `[TC35932_DEL]`, con 2 chứa システム表示名 | 1. Đặt lịch gửi template group cho friend test, bật delay, giờ gửi = hiện tại + 5 phút<br>2. Vào màn quản lý friend info, **xóa** `TC35932_DEL`<br>3. Chờ qua giờ gửi<br>4. Đọc 2 tin trên chat 1:1 và trên LINE app | Friend info `TC35932_DEL` bị xóa giữa lúc lưu lịch và lúc gửi | - Vẫn gửi đủ 2 tin<br>- Con 1: vị trí mã để trống, phần chữ còn lại giữ nguyên; KHÔNG hiện `[FRIEND_INFO_...]` ở cả chat 1:1 và LINE<br>- Con 2: hiển thị tên thật<br>- Chat 1:1 và LINE giống nhau | | Lấp Q1 · dẫn từ TC-CHT-181 ("info đã bị xoá thì để trống") · Đánh giá spec: Spec ghi rõ (kho TC-CHT-176/181) · Evidence: screenshot chat 1:1 + LINE |
| TC-FRIEND001-02 | UI | FRIEND-001 | Chèn friend info vào tin nhắn | Boundary | auto | Tất cả | Template group 5 con và 6 con (biên 5 tin/lần gọi LINE API) chứa friend info khác TYPE — gửi qua lịch có delay, tất cả thay đúng | - Môi trường đã deploy bản fix<br>- Friend test có đủ giá trị: システム表示名, 生年月日, email, SĐT, 都道府県, friend info tự tạo kiểu date (`TC35932_DATE`) và kiểu point (`TC35932_PT`)<br>- Template group `TC35932_G5` = **5** message text con<br>- Template group `TC35932_G6` = **6** message text con (5 con như G5 + 1 con thêm) | 1. Đặt lịch gửi `TC35932_G5` cho friend test, bật delay, giờ gửi = hiện tại + 3 phút, chờ gửi xong<br>2. Đếm số tin và đọc từng tin trên chat 1:1, đối chiếu LINE app<br>3. Đặt lịch gửi `TC35932_G6` tương tự, chờ gửi xong<br>4. Đếm số tin và đọc từng tin, đặc biệt **tin thứ 6**, đối chiếu LINE app<br>5. Rê chuột vào tin thứ 5 và tin thứ 6, xem có icon trả lời không | Con 1: 「[システム表示名]様」 · Con 2: 「誕生日:[生年月日]」 · Con 3: 「連絡先:[email] / [SĐT]」 · Con 4: 「地域:[都道府県]」 · Con 5: 「予約日:[TC35932_DATE]」 · Con 6 (chỉ G6): 「ポイント:[TC35932_PT]」 | - G5: chat 1:1 hiển thị đúng **5** tin, G6: đúng **6** tin; đúng thứ tự, không trùng/rỗng<br>- Mọi mã được thay đúng giá trị theo format của TYPE (ngày, số point); không còn `[FRIEND_INFO_...]` ở tin nào, **kể cả tin thứ 6** (tin nằm ở lần gọi API thứ 2)<br>- Chat 1:1 và LINE khớp nhau<br>- Tin thứ 5 và thứ 6 đều có icon trả lời<br>- Nếu màn template **không cho** thêm con thứ 6 → ghi nhận giới hạn thực tế ở Kết quả thực thi, chỉ chạy G5 | | Lấp Q1 · RULE-01 Boundary · Biên lấy từ job-spec :311/:462/:502 (`callSentPushMessage` chia tối đa 5 tin/lần gọi API) — sau fix luồng delay gửi toàn bộ message con trong 1 request nên 6 con buộc tách 2 lần gọi · Đánh giá spec: Spec không ghi giới hạn số con trên màn template · Evidence: screenshot từng tin G5 + G6 |
| TC-MSG002-01 | UI | MSG-002 | Đặt lịch gửi — delay & job | Boundary | auto | Tất cả | Lịch có delay chứa template group ở giữa và ở cuối danh sách — mọi message con hiển thị đúng, đúng thứ tự | - Môi trường đã deploy bản fix<br>- Friend test có giá trị システム表示名<br>- Template đơn `TC35932_S1`; template group `TC35932_G1` (2 con) và `TC35932_G2` (2 con), mỗi con chứa mã システム表示名 | 1. Đặt lịch gửi cho friend test, thêm theo thứ tự: `TC35932_S1` → `TC35932_G1` → `TC35932_G2`<br>2. Bật delay, giờ gửi = hiện tại + 3 phút, lưu<br>3. Chờ gửi xong, đếm tin và đọc nội dung trên chat 1:1<br>4. Đối chiếu với LINE app, ghi giờ:phút:giây từng tin | 1 template đơn + 2 template group (group ở giữa + group ở cuối) | - Chat 1:1 hiển thị đúng 5 tin theo thứ tự S1 → G1 (2) → G2 (2)<br>- Tất cả tin hiển thị tên thật, không còn `[FRIEND_INFO_...]`, có icon trả lời<br>- Không trùng/rỗng; chat 1:1 khớp LINE<br>- Khoảng cách giữa các template theo spec job (§6 #3) | | Lấp Q3 · Đánh giá spec: Spec ghi rõ phần thứ tự (job-spec §3.2); khoảng giãn chờ §6 #3 · Evidence: screenshot + bảng giờ gửi |
| TC-SYNCAPP001-01 | UI | SYNC-APP-001 | Chat 1:1 — app admin mobile | Normal | manual | Tất cả | Tin gửi qua lịch có delay hiển thị giá trị friend info đã thay trên chat 1:1 của app admin mobile | - Môi trường đã deploy bản fix<br>- App admin mobile LME (iOS và Android) đăng nhập account có quyền bot test<br>- Đã chạy xong NEW-1 dataset A (tin template group qua lịch có delay đã gửi) | 1. Mở app admin mobile, vào chat 1:1 của friend test<br>2. Đọc các tin của lịch có delay<br>3. So với chat 1:1 web và LINE app<br>4. Xem dòng preview tin cuối ở danh sách hội thoại trên app | Tin của NEW-1 dataset A | - App hiển thị giá trị friend info đã thay, KHÔNG hiện `[FRIEND_INFO_...]`<br>- Nội dung khớp chat 1:1 web và LINE<br>- Preview tin cuối trên app cũng đã thay giá trị | | Lấp Q2 · MAP-FI-10 · manual vì thiết bị thật (app admin mobile) · Đánh giá spec: Spec ghi rõ (catalog MAP-FI-10) · Evidence: screenshot app iOS + Android |

- **G1** (unsend) — không đề xuất TC: màn chat 1:1 admin không có thao tác thu hồi (NEW-17 blocked). Chờ Dev trả lời §6 #5 rồi mới viết.
- **G2** (hành vi đổi T5) — không viết TC mới: sửa expected của NEW-11 sau khi Leader/PO chốt §6 #1 (xem §4 I7).
- **Q3 Abnormal** — dùng lại kho `TC-CHT-323` (xem bảng đối chiếu), không viết mới.

---

## 6. Spec update needed

| # | Nội dung | Nguồn mâu thuẫn | Cần ai chốt |
|---|---|---|---|
| 1 | **Hành vi đổi sau fix (T5)**: lịch có delay + template group bật `is_delay_sent_message` → message con gửi **cùng lúc** (Dev) hay **giãn từng con**? Spec chỉ mô tả giãn 2-4 giây theo **từng template** trong lịch, không nói mức message con; còn kho TC-CHT-228 (gửi ngay) ghi các con giãn cách | Journal #132627 mục 4.3 vs `spec-features/admin/chat-11/job/job-spec.md` §3.2 (dòng 269-284) vs kho TC-CHT-228 | Leader/PO → cập nhật job-spec §3.2 + expected NEW-11 |
| 2 | Lịch bật delay: **tin đầu tiên gửi ngay** (kho TC-CHT-322) hay **mọi template đều vào `send_random_messages`** (job-spec §3.2)? Log ticket (`SendRandomMessage id=868, templateId=105649`, group duy nhất trong lịch) ủng hộ job-spec. Điểm này quyết định group ở vị trí 1 có đi luồng delay (luồng bị lỗi) hay không | kho TC-CHT-322 vs job-spec §3.2 + log file điều tra | Dev xác nhận → sửa kho hoặc spec |
| 3 | Khoảng giãn cách delay: 2-4 giây (spec) vs 2-5 giây (corpus) — kho MT-05 đang chờ quyết định; ảnh hưởng cách đo của NEW-11 và TC-MSG002-01 | kho MT-05 | Dev (đọc `getRandomTimeSent`) |
| 4 | Friend đã chặn bot khi tới giờ gửi luồng delay: **không gửi** (catalog MAP-SEND-20) hay **gửi, bị LINE từ chối rồi ghi lỗi** (Studio REQ-013, `checkError`)? | catalog MAP-SEND-20 vs Studio REQ-013 | Dev → chốt expected TC-MSG003-01 |
| 5 | Dev ghi "Reply/quote **và unsend**" bị ảnh hưởng (4.3) nhưng màn chat 1:1 admin không có thao tác thu hồi tin bot → "unsend" là luồng nào (bạn bè thu hồi? app mobile?) | Journal #132627 mục 4.3 vs kết quả NEW-17 | Dev |
