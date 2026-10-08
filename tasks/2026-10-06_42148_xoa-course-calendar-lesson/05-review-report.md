# 05 — Review Report

> Draft cho Leader verify. Round 1 — review bộ TC Studio task #370 (ticket #42148).

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #370 (round 1, `tc-ready`, branch `ai_fixbug_42148`) |
| Tổng số TC review | 16 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 6/9 mục có TC (`BUG` · F1 · F2 · D1 · T1 · T2) — **CHƯA ĐỦ** (F3 GAP · F4 GAP/Input thiếu · D2 RISK) |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` | 6/8 điểm có TC — **CHƯA ĐỦ** (rủi ro hồi quy `mobile_notify` RISK · thay đổi round 2 ở `deleteCalendar` GAP) |

**Kết luận**: 12/17 điểm kiểm chứng đủ TC · 3 GAP (G1, G2, G4) · 1 RISK (G3, chung cho 2 chiều)

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F3 — `CalendarSalonCourseService::deleteCalendarCourse` (xoá khoá học **salon**, chiều ngược của bug) | `dev-impact` | không có | GAP — Dev khẳng định "đã lọc type=5" (nhánh bất biến), nhưng không TC nào kiểm chiều ngược: xoá khoá học salon có xoá nhầm lịch nhắc **bài học** trùng mã đơn không. Kho `TC-SLN-246` chỉ kiểm `deleted_at` + 削除済み予約, không kiểm lịch nhắc | `[MAJOR]` |
| G2 | F4 — `ActionBookingCalendar::removeActionRemind` (lọc `events.type=2`) | `dev-impact` | không có | GAP — **Input thiếu**: chưa rõ luồng UI nào gọi hàm này. Nếu `type=2` là 予約管理 thế hệ cũ đã gỡ khỏi tool (Feature #30540, theo `kho-tcs/fa019` mục "Nguồn đã loại") thì đây là GAP giả. Cần Dev xác nhận trước khi viết TC | `[MINOR]` |
| G3 | D2 `mobile_notify` · rủi ro hồi quy Studio: *"thông báo app của đơn lesson có `is_confirm=1` hoặc `status≠1` sẽ còn lại sau khi xoá khoá học (lùi #41265/#41267); badge recount"* | `dev-impact` · `diff code` | `NEW-1` (pass), `#23854` (pass) | RISK — `NEW-1` dựng đúng 2 dòng thông báo (2)(3) nhưng expected ghi *"chờ PO/leader xác nhận — KHÔNG kết luận Fail"* ⇒ Đạt mà không kiểm gì cho đúng điểm hồi quy này. Ngoài ra chỉ kiểm DB + số badge, chưa kiểm trên app (RULE-06) | `[MAJOR]` |
| G4 | Round 2 của fix (Journal #140503, commit `7a00b8cd03`): `CalendarManagementController::deleteCalendar` **bỏ hẳn** câu xoá `event_step_time` theo `user_booking_id` (round 1 / Studio diff là *thêm subquery type=4*) | `diff code` | `#23863`, `NEW-8`, `NEW-12` (pass) | GAP — Dev tự nêu rủi ro "dòng nhắc bài học mồ côi (`event_step` đã xoá cứng) không còn được dọn". Với xoá cả lịch, đơn bị `forceDelete` ⇒ dòng nhắc mồ côi trỏ tới đơn **không còn tồn tại**. `NEW-5` chỉ kiểm luồng xoá khoá học và chỉ ở tầng DB; chưa TC nào kiểm job có gửi nhắc cho đơn đã mất không | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 9 quan điểm Trigger khớp task · 6 chưa cover đủ (đã xét: `DATA-DB-001` · `DATA-REF-001` · `STATE-DEP-001` · `MSG-002` · `SYNC-APP-001` · `REG-SHARED-001` · `DATA-COUNT-001` · `INTG-SHEET-001` · `ENV-003`; `ENV-003` đưa xuống §5 I1).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `DATA-DB-001` | Cao | RISK — 3 TC gắn mã (`#23854`, `#23863`, `NEW-11`) đều là `Normal`. Nội dung Abnormal (WHERE scope sang bot B: `NEW-3`, `NEW-8`) và Boundary (`NEW-7`) **đã có** nhưng gắn mã lạ `TOOL-*` / `FUNC-004` ⇒ chưa tính là cover (RULE-01). **Không cần TC mới** — đổi mã quan điểm trên Studio: `NEW-3`, `NEW-8` → `DATA-DB-001`; `NEW-7` → `DATA-DB-001` | `[MAJOR]` |
| Q2 | `MSG-002` | Cao | RISK — chỉ có 2 TC `Normal` (`NEW-9`, `NEW-12`). Thiếu Abnormal: dòng nhắc của đơn đã xoá không được gửi trong trường hợp mồ côi (rủi ro Dev đã nêu); thiếu Boundary theo thời điểm gửi | `[MAJOR]` |
| Q3 | `SYNC-APP-001` (→ Cao: flow thông báo admin) | Cao | RISK — `NEW-1` chỉ kiểm DB + cột đếm badge, **không mở app quản trị** (RULE-06 output cuối). Fix #42148 đổi chính tập thông báo app bị dọn khi xoá khoá học | `[MAJOR]` |
| Q4 | `DATA-REF-001` | Cao | RISK — Normal có ở `#23854` (đơn ở 削除済み予約 giữ tên khoá học snapshot). Thiếu Abnormal: **nơi tham chiếu còn lại** sau fix là thông báo app đã xác nhận của đơn thuộc khoá học bị xoá → mở ra có sập màn không. Nếu #41265/#41267 sinh ra để xử lý đúng lỗi này thì #42148 đang lùi fix đó | `[MAJOR]` |
| Q5 | `STATE-DEP-001` | Cao | RISK — nội dung "hành động đã lên lịch khi gốc bị xoá" có ở `NEW-2` / `NEW-4` nhưng gắn `TOOL-*`; thiếu Boundary theo thời điểm (xoá sát giờ gửi). Đổi mã `NEW-2` (Abnormal), `NEW-4` (Normal) → `STATE-DEP-001` + thêm 1 TC Boundary | `[MAJOR]` |
| Q6 | `REG-SHARED-001` | Cao | RISK — Dev có danh sách nơi dùng chung (mục 3); `NEW-3` đã kiểm chiều lesson → loại nhắc khác. Thiếu chiều ngược Salon → Lesson (cặp Salon/Lesson là điểm lặp lại nêu trong quan điểm) — lấp chung với G1 | `[MAJOR]` |

---

## 3. TC trùng lặp nội dung

Đã rà 16 TC, không phát hiện trùng lặp. Các cặp gần nhau đã soi và giữ nguyên: `NEW-9` (xoá khoá học, EP-20) vs `NEW-12` (xoá cả lịch, EP-14) — khác luồng; `NEW-2` (salon cùng bot) vs `NEW-3` (loại nhắc khác + bot B) — khác đối tượng; `#23863` (dọn toàn bộ dữ liệu con) vs `NEW-8` (bảo toàn nhắc trùng mã) — khác mục đích; `#23854` (nhắc chưa gửi bị huỷ) vs `NEW-7` (nhắc đã gửi được giữ) — 2 phía của cùng biên.

---

## 4. Mâu thuẫn trong TCs

**Đã rà**: 16 TC × `spec-features/admin/lesson-booking/feature-spec.md` (§4.5, §4.7, BR-31) + `spec-features/admin/lesson-booking/web/logic-spec.md` (§9.5, §9.6) + `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (`TC-LSN-72/73/398/457/616`) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (`TC-SLN-246`) — **không phát hiện mâu thuẫn** giữa expected của TC với spec / kho.

Ghi chú: spec **tự mâu thuẫn** về `mobile_notify` khi xoá cả lịch (feature-spec §4.7 bước 4 "`mobile_notify delete()`" vs logic-spec §9.6 bước 4 "`is_confirm=0, status=1`") — không phải lỗi TC (`#23863` chỉ chấm phần "chưa đọc phải bị xoá"), đưa sang §8 #2.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Toàn bộ 16 TC · `NEW-9`, `NEW-12` | **RULE-08 / ENV-003** — 16/16 TC chạy ở `staging`, 0 TC production. Task chạm **job nền** gửi nhắc (`NewEventRemindTask` đọc `event_step_time`) — hậu quả end-user của bug nằm ở job | Sau release, chạy lại `NEW-9` / `NEW-12` (hoặc tối thiểu `TC-STATEDEP001-01` ở §7 — không cần dựng DB) trên prd |
| I2 | `[MAJOR]` | Nguồn diff Studio · `#23863`, `NEW-8` + 10 TC tiền đề "local" | (a) Studio `spec_delta` tính lúc 06:30Z với `journalCount=1` = **round 1** (commit `da18d20000`, diffStat `CalendarManagementController +5 −1`); Redmine round 2 (Journal #140503, 06:50Z, commit `7a00b8cd03`) **đổi cách fix `deleteCalendar`** (bỏ câu xoá thay vì thêm subquery). Note của `#23863` / `NEW-8` vẫn mô tả round 1. (b) 10 TC có tiền đề "Môi trường local, nhánh ai_fixbug_42148" + `env_scope=local` nhưng `last_exec.env = staging` | Xác nhận staging đang chạy commit nào (`7a00b8cd03`?) trước khi chấp nhận 15 pass; refresh diff trên Studio cho round 2. Expected của `NEW-8` / `#23863` vẫn đúng với round 2 (nhắc salon trùng mã còn nguyên), chỉ cần sửa note |
| I3 | `[MAJOR]` | `NEW-10` | **RULE-04** — TC rà phạm vi dữ liệu bị xoá nhầm trước bản fix bị `skip`. Dev ghi "Không cần Recover data" nhưng ■6 tự nhận *chưa kết nối được DB, chưa kiểm dữ liệu runtime* ⇒ kết luận "không cần Recover data" chưa có số liệu | Leader cung cấp mốc T (#41265/#41267 lên prd), chạy `NEW-10` (query chỉ đọc) trước khi đóng ticket; > 0 đơn salon thiếu nhắc thì quyết phương án Recover data |
| I4 | `[MAJOR]` | `NEW-1` | Expected cho thông báo (2) đã xác nhận + (3) lệch trạng thái = *"chỉ ghi nhận, KHÔNG kết luận Fail"* ⇒ không đo lường được, TC Đạt nhưng không kiểm điểm hồi quy chính (G3). Logic-spec §9.5 bước 4 ghi rõ chỉ xoá `is_confirm=0, status=1` | Chốt quy tắc ở §8 #1 rồi sửa expected `NEW-1` trên Studio (`testcase_update`), chạy lại |
| I5 | `[MAJOR]` | Quét ngang của Dev (`FriendlistController:2883/4121/4552`, `BookingManagerController:1268`, `BookingAjaxController:239`, `Api/FriendInformationController:1249`) | `REG-SHARED-001` — 5 câu xoá `event_step_time` theo id booking cũ **chưa lọc type/bot_id** (cùng dạng lỗi #42148), Dev đề xuất "ticket riêng" nhưng ticket #42148 chưa liên kết ticket nào | Leader tạo / liên kết ticket riêng cho 5 điểm này để không mất dấu; không đưa vào phạm vi test #42148 |
| I6 | `[MINOR]` | `NEW-6`, `NEW-7` | Gắn `FUNC-004` (giới hạn số lượng / ký tự / dung lượng) — nội dung là biên 0 đơn và biên trạng thái nhắc, không phải giới hạn nhập | `NEW-7` → `DATA-DB-001` (Q1); `NEW-6` → `FUNC-001` |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 16 TC — không có TC nào ngoài phạm vi task. `NEW-11` (Google Sheet) và `#23859` (chặn xoá khi còn đơn tương lai) không map thẳng F*/D*/T* nhưng dẫn được từ dòng "Không đổi: chặn xoá khi còn đơn tương lai (422) … enqueue xoá Google Sheet" của Studio `dev_impact` ⇒ là TC regression, giữ lại. `#23865` thuộc `DATA-DB-001` (WHERE scope lịch khác) ⇒ giữ.

---

## 7. TCs đề xuất bổ sung (6)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (nhóm コース — tạo/sửa/xóa, リマインド — job gửi & recover, 予約システムの削除, App mobile, Googleスプレッドシート連携) · `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (コース — tạo/sửa/xóa) |
| Vùng regression phát hiện từ kho | `TC-SLN-246` (xoá khoá học salon — không kiểm lịch nhắc) → G1 · `TC-LSN-398` (xoá nhắc theo thao tác huỷ — không có nhánh xoá khoá học) · `TC-LSN-616` (mở thông báo app → detail booking) → Q4 |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không |
| GAP / Q không đẻ TC mới | **G2** — Input thiếu, chờ Dev xác nhận luồng gọi `removeActionRemind` · **G3** (phần DB) — trùng 4 yếu tố với `NEW-1` ⇒ sửa expected `NEW-1` (I4), phần app lấp bằng `TC-SYNCAPP001-01` · **Q1** — đổi mã quan điểm `NEW-3` / `NEW-8` / `NEW-7` · **Q5** Normal/Abnormal — đổi mã `NEW-4` / `NEW-2` |
| Căn cứ TC regression `R<x>` | R1 = 03-dev-impact "■ TỰ REVIEW — dòng nhắc bài học mồ côi không còn được dọn" + câu hỏi mở Q3 trong note `NEW-5` + feature-spec §4.4 d3 **B-5** (khách nhận nhắc cho đơn đã xoá = lỗi) |
| Xác nhận chống trùng | Đã đối chiếu 16 TC ở BƯỚC 0 + 2 file kho — không TC đề xuất nào trùng (`TC-MSG002-01` khác `NEW-5` ở chỗ kiểm job gửi tin; `TC-STATEDEP001-01` khác `NEW-9` ở biên thời gian và dữ liệu dựng bằng UI) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-01 | Data | REG-SHARED-001 | コース — tạo/sửa/xóa (Salon) | Abnormal | auto | dev, local, staging | Xoá khoá học salon không xoá lịch nhắc bài học (lesson) có mã đơn trùng | - Có bản fix #42148 (commit `7a00b8cd03`)<br>- Bot A có Lịch salon 「QA42148-SLN」 đã cài bước nhắc trước giờ hẹn; khoá học 「QA42148-SLN-C1」 chỉ còn 1 đơn đã huỷ, mã N, kèm 1 lịch nhắc salon chưa gửi<br>- Bot A có Lịch bài học 「レッスンA」 với 1 đơn bài học mã N (dựng bằng DB cho trùng mã) ở trạng thái 「予約確定」, khung giờ tương lai, kèm 1 lịch nhắc bài học chưa gửi<br>- Ghi lại mã bản ghi, trạng thái, giờ gửi của 2 lịch nhắc | 1. Đăng nhập admin bot A, mở Lịch salon 「QA42148-SLN」 → tab 「コース・スタッフ」.<br>2. Bấm xoá khoá học 「QA42148-SLN-C1」.<br>3. Bấm 「このコースを削除する」 trong popup xác nhận.<br>4. Tra DB lịch nhắc bài học của đơn bài học mã N.<br>5. Tra DB lịch nhắc salon của đơn salon mã N.<br>6. Mở Lịch bài học 「レッスンA」 → Lịch đặt chỗ 「予約カレンダー」, mở đơn mã N. | Mã đơn trùng: N (đơn salon đã huỷ + đơn bài học 「予約確定」, cùng bot A)<br>Lịch nhắc bài học: chưa gửi, giờ gửi tương lai<br>Lịch nhắc salon: chưa gửi | - Bước 3: xoá thành công, khoá học biến mất khỏi danh sách<br>- Bước 4: lịch nhắc bài học của đơn N còn nguyên — cùng mã bản ghi, trạng thái chưa gửi, giờ gửi không đổi<br>- Bước 5: lịch nhắc salon chưa gửi của đơn salon N đã bị huỷ<br>- Bước 6: đơn bài học vẫn hiển thị 「予約確定」 |  | Lấp G1 + Q6 · regression · căn cứ: 03-dev-impact mục 3 #3 "CalendarSalonCourseService::deleteCalendarCourse — đối chứng: đã lọc type=5" (Dev khẳng định bất biến, chưa có TC — câu 5 BƯỚC 2); kho `TC-SLN-246` không kiểm lịch nhắc · Đánh giá spec: Spec không ghi (salon feature-spec "Luồng xóa khóa học" không nêu lịch nhắc) · không chạy prd vì phải dựng dữ liệu trùng mã đơn bằng DB · Boundary: không có khái niệm biên cho chiều này (RULE-01) · Evidence: query DB trước/sau + ảnh màn hình |
| TC-MSG002-01 | Job | MSG-002 | リマインド — job gửi & recover | Abnormal | auto | dev, local, prd, staging | Sau khi xoá khoá học, lịch nhắc bài học mồ côi của đơn đã xoá không được job gửi tới khách | - Có bản fix #42148; job gửi nhắc (linect-service) đang chạy, trỏ cùng DB<br>- Bot A có Lịch bài học 「レッスンA」, khoá học 「QA42148-ORPHAN-JOB」 có 1 đơn đã huỷ, mã N, của bạn bè LINE test U1<br>- Dựng bằng DB 1 lịch nhắc bài học chưa gửi của đơn N trỏ tới bước nhắc **đã bị xoá** khỏi DB (mồ côi), giờ gửi = hiện tại + 10 phút<br>- Đối chứng: U1 có 1 lịch nhắc salon hợp lệ, chưa gửi, cùng giờ gửi<br>- Ghi lại lịch sử chat của U1 làm mốc | 1. Mở màn sửa khoá học 「QA42148-ORPHAN-JOB」, bấm 「このコースを削除する」, xác nhận trong modal 「コースの削除」.<br>2. Tra DB: dòng nhắc mồ côi của đơn N còn lại hay không.<br>3. Chờ qua giờ gửi + 1 chu kỳ quét của job.<br>4. Mở Chat 1:1 「1:1チャット」 của U1 trên admin và LINE app của U1.<br>5. Tra lại trạng thái dòng nhắc mồ côi + dòng nhắc salon đối chứng; xem log job. | Đơn N: đã huỷ, thuộc khoá học bị xoá<br>Lịch nhắc mồ côi: bước nhắc đã xoá, chưa gửi, giờ gửi +10 phút<br>Lịch nhắc salon đối chứng: hợp lệ, cùng giờ gửi | - Bước 1: xoá thành công, không có alert lỗi<br>- Bước 4: U1 KHÔNG nhận tin nhắc bài học nào cho đơn N đã xoá<br>- Bước 4: U1 nhận đúng 1 tin nhắc salon đối chứng<br>- Bước 5: job không dừng / không lặp lỗi vì dòng mồ côi; ghi trạng thái cuối của dòng mồ côi vào kết quả |  | Lấp Q2 (Abnormal) + R1 · regression · căn cứ: 03-dev-impact "TỰ REVIEW — dòng nhắc bài học mồ côi không còn được dọn" + câu hỏi mở Q3 trong `NEW-5` + feature-spec §4.4 d3 B-5 (khách nhận nhắc cho đơn đã xoá là lỗi) · Đánh giá spec: Spec ghi rõ (B-5) · ⚠️ RULE-08 job nền ⇒ giữ 4 env; dữ liệu mồ côi phải dựng bằng DB — trên prd chỉ chạy khi có sẵn dòng mồ côi, Leader quyết · Evidence: ảnh chat 1:1 + LINE app, log job, query DB |
| TC-MSG002-02 | Job | MSG-002 | 予約システムの削除 | Abnormal | auto | dev, local, prd, staging | Sau khi xoá cả Lịch bài học, lịch nhắc bài học mồ côi của đơn đã bị xoá cứng không được job gửi | - Có bản fix #42148 round 2 (`deleteCalendar` đã bỏ câu xoá lịch nhắc theo mã đơn); job gửi nhắc đang chạy, trỏ cùng DB<br>- Bot A có Lịch bài học 「QA42148-CAL-ORPHAN」 có 1 khoá học với 1 đơn mã M của bạn bè LINE test U1<br>- Dựng bằng DB 1 lịch nhắc bài học chưa gửi của đơn M trỏ tới bước nhắc **đã bị xoá** (mồ côi), giờ gửi = hiện tại + 15 phút<br>- Đối chứng: U1 có 1 lịch nhắc salon hợp lệ, chưa gửi, cùng giờ gửi<br>- Ghi lại lịch sử chat của U1 làm mốc | 1. Mở chi tiết lịch 「QA42148-CAL-ORPHAN」 → tab 「全体設定」 → mục 「予約システムの削除」.<br>2. Bấm 「削除用認証コードをメールで受け取る」, nhập mã vào ô 「認証コード」.<br>3. Bấm 「削除の最終確認にすすむ」, rồi 「予約システムを削除する」.<br>4. Tra DB: đơn M đã bị xoá; dòng nhắc mồ côi của đơn M còn lại hay không.<br>5. Chờ qua giờ gửi + 1 chu kỳ quét của job.<br>6. Mở Chat 1:1 「1:1チャット」 của U1 trên admin và LINE app của U1; xem log job. | Đơn M: thuộc lịch bị xoá<br>Lịch nhắc mồ côi: bước nhắc đã xoá, chưa gửi, giờ gửi +15 phút<br>Lịch nhắc salon đối chứng: hợp lệ, cùng giờ gửi | - Bước 3: lịch biến mất khỏi danh sách lịch<br>- Bước 6: U1 KHÔNG nhận tin nhắc bài học nào cho đơn M<br>- Bước 6: U1 nhận đúng 1 tin nhắc salon đối chứng<br>- Bước 6: job không dừng / không lặp lỗi vì dòng mồ côi; ghi trạng thái cuối của dòng mồ côi vào kết quả |  | Lấp G4 · regression · căn cứ: Journal #140503 round 2 "deleteCalendar — chỉ bỏ câu EventStepTime" + "TỰ REVIEW — dòng nhắc mồ côi không còn được dọn"; khác `TC-MSG002-01` ở luồng EP-14 (đơn bị xoá cứng, không truy ngược được) · Đánh giá spec: Spec ghi rõ (feature-spec §4.4 d3 B-5) · ⚠️ RULE-08 job nền ⇒ giữ 4 env; dữ liệu mồ côi dựng bằng DB, Leader quyết phần prd · Evidence: ảnh chat 1:1 + LINE app, log job, query DB |
| TC-STATEDEP001-01 | Job | STATE-DEP-001 | リマインド — job gửi & recover | Boundary | auto | dev, local, prd, staging | Xoá khoá học ngay trước giờ gửi nhắc sau buổi học: nhắc của đơn thuộc khoá học bị xoá không gửi, nhắc của khoá học khác cùng giờ vẫn gửi | - Có bản fix #42148<br>- Lịch bài học 「レッスンA」 đã cài bước nhắc sau buổi học ở 「予約前後に送るリマインドメッセージ」<br>- Khoá học 「QA42148-DEL」 có 1 đơn 「予約確定」 của bạn bè U1 (tạo qua 「予約追加」) ở khung giờ đã kết thúc, sao cho giờ gửi nhắc T = hiện tại + 5 phút; không còn đơn tương lai<br>- Khoá học 「QA42148-KEEP」 có 1 đơn 「予約確定」 của bạn bè U2 kết thúc cùng giờ (cùng T)<br>- Ghi lại lịch sử chat U1, U2 làm mốc | 1. Ghi lại giờ gửi T của 2 đơn.<br>2. Khoảng 2 phút trước T: mở màn sửa khoá học 「QA42148-DEL」, bấm 「このコースを削除する」, xác nhận trong modal 「コースの削除」.<br>3. Chờ qua T + 1 chu kỳ quét của job.<br>4. Mở Chat 1:1 「1:1チャット」 và LINE app của U1.<br>5. Mở Chat 1:1 「1:1チャット」 và LINE app của U2.<br>6. Mở 「削除済み予約」 tìm đơn của U1. | Giờ gửi nhắc T: hiện tại + 5 phút<br>Thời điểm xoá: T − 2 phút<br>U1: đơn thuộc khoá học bị xoá<br>U2: đơn thuộc khoá học đối chứng | - Bước 2: xoá thành công<br>- Bước 4: U1 KHÔNG nhận tin nhắc sau buổi học<br>- Bước 5: U2 nhận đúng 1 tin nhắc sau buổi học<br>- Bước 6: đơn của U1 hiển thị trong 「削除済み予約」 |  | Lấp Q5 (Boundary) · đồng thời là biên thời gian cho Q2 (`MSG-002`) · căn cứ: Studio `dev_impact` "nhắc lesson còn chờ gửi (status=0) của đơn bị xoá phải vẫn bị huỷ, nếu không job vẫn gửi nhắc cho đơn đã mất" · dữ liệu dựng hoàn toàn bằng màn hình ⇒ chạy được trên prd (RULE-08, I1) · Đánh giá spec: Spec ghi rõ (logic-spec §9.5 bước 5) · Evidence: ảnh chat 1:1 + LINE app U1/U2, giờ thao tác |
| TC-SYNCAPP001-01 | UI | SYNC-APP-001 | App mobile | Normal | manual | dev, local, prd, staging | Sau khi xoá khoá học, badge và danh sách thông báo trên app quản trị khớp số thông báo chưa xác nhận còn lại | - App quản trị LME đã đăng nhập bot A, bật thông báo<br>- Khoá học 「QA42148-NOTI」 có 2 đơn đã huỷ, mỗi đơn sinh 1 thông báo app: 1 thông báo đã mở trên app, 1 chưa mở<br>- Khoá học 「QA42148-OTHER」 có 1 thông báo app chưa mở<br>- Ghi lại số badge và danh sách thông báo trên app | 1. Trên app, ghi số badge và danh sách thông báo hiện tại.<br>2. Trên web, mở màn sửa khoá học 「QA42148-NOTI」, bấm 「このコースを削除する」, xác nhận trong modal 「コースの削除」.<br>3. Trên app, kéo làm mới danh sách thông báo.<br>4. Quan sát số badge và danh sách thông báo. | 3 thông báo app: 2 của 「QA42148-NOTI」 (1 đã mở, 1 chưa mở), 1 của 「QA42148-OTHER」 (chưa mở) | - Thông báo chưa mở của 「QA42148-NOTI」 biến mất khỏi danh sách<br>- Thông báo của 「QA42148-OTHER」 còn nguyên<br>- Số badge = số thông báo chưa xác nhận còn lại<br>- Thông báo đã mở của 「QA42148-NOTI」: hiển thị theo quy tắc chốt ở §8 #1 |  | Lấp Q3 + G3 (phần app) · RULE-06 output cuối trên app · căn cứ: Studio `dev_impact` "thông báo app (mobile_notify) của đơn lesson có is_confirm=1 hoặc status≠1 sẽ còn lại sau khi xoá khoá học (lùi #41265/#41267); badge recount" · Đánh giá spec: Spec ghi rõ (logic-spec §9.5 bước 4 + 7), dòng cuối chờ §8 #1 · manual vì app quản trị di động thật · Evidence: ảnh chụp app trước/sau |
| TC-DATAREF001-01 | UI | DATA-REF-001 | App mobile | Abnormal | manual | dev, local, prd, staging | Mở thông báo app còn lại của đơn thuộc khoá học đã xoá: không lỗi, hiển thị rõ đơn đã xoá | - App quản trị LME đã đăng nhập bot A<br>- Khoá học 「QA42148-REF」 có 1 đơn đã huỷ của bạn bè U1, thông báo app của đơn này **đã mở** (đã xác nhận) trên app<br>- Không còn đơn tương lai (xoá được khoá học) | 1. Trên web, mở màn sửa khoá học 「QA42148-REF」, bấm 「このコースを削除する」, xác nhận trong modal 「コースの削除」.<br>2. Trên app, mở danh sách thông báo.<br>3. Chạm thông báo của đơn U1 (nếu còn hiển thị).<br>4. Quan sát màn chi tiết mở ra. | Thông báo app: đã xác nhận, thuộc đơn của khoá học bị xoá | - Bước 3–4: app không crash, không màn trắng, không lỗi hệ thống<br>- Bước 4: đơn hiển thị ở trạng thái đã xoá 削除済み (hoặc thông báo rõ đối tượng không còn tồn tại)<br>- Bước 4: tên khoá học hiển thị là tên đã chụp lại khi xoá |  | Lấp Q4 · regression · căn cứ: Studio `dev_impact` "lùi #41265/#41267" — thông báo đã xác nhận của đơn thuộc khoá học bị xoá không còn bị dọn; kho `TC-LSN-616` (bấm thông báo mở detail booking); DATA-REF-001 Kiểm tra (1) · Đánh giá spec: Spec không ghi hành vi app khi mở đơn đã xoá — cần Leader xác nhận · manual vì app quản trị di động thật · Evidence: video thao tác app |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `lesson-booking/web/logic-spec.md` §9.5 bước 4 | Chốt quy tắc dọn thông báo app khi **xoá khoá học**: chỉ `is_confirm=0, status=1` (spec hiện tại + #42148) hay mọi thông báo của đơn (#41265/#41267)? Ghi rõ lý do #41265/#41267 từng mở rộng, và hệ quả với app (Q4) | G3 · I4 | Leader / PM |
| 2 | `lesson-booking/feature-spec.md` §4.7 bước 4 vs `web/logic-spec.md` §9.6 bước 4 | Spec tự mâu thuẫn khi **xoá cả lịch**: "`mobile_notify delete()`" vs "`is_confirm=0, status=1`"; Studio `dev_impact` nói code xoá toàn bộ. Sau khi chốt #1, thống nhất 2 luồng xoá khoá học / xoá lịch | §4 ghi chú | Dev |
| 3 | `lesson-booking/web/logic-spec.md` §9.5 bước 5 + §9.6 bước 8 · `feature-spec.md` §4.5 bảng "Dọn hàng đợi" | Ghi hành vi sau #42148: xoá khoá học chỉ dọn lịch nhắc `event_step.type=4` cùng bot theo từng đơn; xoá cả lịch chỉ dọn qua sự kiện nhắc của lịch (round 2 bỏ câu xoá theo mã đơn). Nêu rủi ro dòng nhắc mồ côi không được dọn | G4 · I2 | Dev |
| 4 | `kho-tcs/fa019-…` `TC-LSN-457` (sửa ở `kho-tcs/data/`) | Bổ sung ngoại lệ [#42148]: lịch nhắc salon / loại nhắc khác / bot khác có mã đơn trùng phải **còn nguyên** sau khi xoá lịch — theo `#23863` / `NEW-8` | Kho cũ hơn bản fix | Leader |
