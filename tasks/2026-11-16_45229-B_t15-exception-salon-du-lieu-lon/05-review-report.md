# 05 — Review Report

> Draft cho Leader verify. **Lượt B của sprint #45229 — T15 phần Salon (#41717 · #41529 · #41718)**, review 2026-11-16.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) Studio task #560` (task cha #45229) — lọc 10/1225 TC gắn `REQ-X-41717-*` / `REQ-X-41529-*` / `REQ-X-41718-*` |
| Tổng số TC review | 10 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` mục 4 (BUG ×3 + F1–F7 trừ F4 + D1–D3 + T1–T5). ⚠️ Dev không viết đánh giá — file 03 ghép từ requirement Studio | `6/17 mục có TC` — **CHƯA ĐỦ** (11 RISK) |
| **(b) diff code** — 6 điểm: guard API khung giờ · guard `initDataBooking` · hành vi siết khoảng ngày > 31 → 422 · `user_block.js` + view · xoá ở `block.js` / `FriendlistController` · `config/queue.php` | `2/6 điểm có TC` — **CHƯA ĐỦ** (2 GAP · 2 RISK) |

**Kết luận**: `8/23 vùng ảnh hưởng đủ TC · 2 GAP · 13 RISK` — trong 13 RISK có **6 RISK chỉ vì TC đã có nhưng chưa chạy** (BUG-1 · BUG-2 · F2 · F3 · D2 · T2 → chạy lại, không cần TC mới, xem §5 I1); còn lại gom thành 4 dòng dưới.

Loại khỏi mẫu số: F4 truy vấn khung giờ tuần viết lại (T16 #41345 — review ở nhóm T16) · các thay đổi Google Calendar / Sheet / phân bổ nhân viên trong `CalendarSalon*` (T9 / T10 / T16) · `Mobile/CalendarSalonController.php` +304 (nhóm khác — chưa rõ có gọi API khung giờ, xem §5 I3).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Quy tắc mới **khoảng hiển thị ≤ 31 ngày → 422** (fix bug Studio #45409) — F1 · F3 · T1 · guard API + guard `initDataBooking` | dev-impact + diff code | NEW-764 ✓ (calendarId / ngày sai) · NEW-703, NEW-763 (skip, expected cũ) · NEW-702 (skip) | **GAP** — (1) biên 31 / 32 ngày: 0 TC; (2) hành vi bị **siết lại** nhưng chưa TC nào chứng minh trang khách ở 3 chế độ tuần / tháng / danh sách, với lịch nhận đặt dài (tới 180 ngày), không tự gửi khoảng > 31 ngày rồi nhận 422 | `[BLOCKER]` |
| G2 | 3 exception production — BUG-1 · BUG-2 · BUG-3 · F6 · T4 | dev-impact | 10/10 TC chạy `local`, dữ liệu seed | **RISK** — lỗi chỉ xảy ra trên production (dữ liệu thật bot 153361 / 52318 / 108684, cấu hình PHP + MySQL production); chưa TC nào xác nhận sau release các signature không còn ở room `SNSLineException` / dashboard check-exception. Task có job nền + thanh toán UnivaPay (RULE-08) | `[BLOCKER]` |
| G3 | Xoá bạn bè ở màn ブロックされた友だち (`/basic/friendlist/user-block`) — F5 · `user_block.js` · `user_block.blade.php` | diff code | NEW-697 ✓ · NEW-698 (skip) — cả 2 chỉ ở màn `/basic/friendlist/block` | **GAP** — JS + view màn user-block đổi trong sprint, 0 TC chạm; câu SQL của exception mẫu 1 là bước xoá đơn salon dùng chung khi xoá bạn bè | `[MAJOR]` |
| G4 | BUG-3 #41718 — nguyên nhân gốc | diff code | NEW-700 ✓ (1 giả thuyết: worker rảnh quá `wait_timeout`) · NEW-697 ✓ · NEW-699 ✓ | **RISK** (symptom-only) — ticket chỉ có triệu chứng, Dev chưa xác định nguyên nhân, không có commit; TC chỉ chứng minh "không tái hiện ở local". Exception mẫu 1 xảy ra trong request web xoá bạn bè, giả thuyết worker không giải thích được luồng này → cần Dev nêu nguyên nhân trước khi đẻ TC (§5 I3) | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `12 quan điểm Trigger khớp task · 7 chưa cover đủ`.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-004` | Cao | **GAP** Boundary của giới hạn mới 31 ngày (RULE-01). Normal có (NEW-764 B1 đối chứng 200); Abnormal chỉ có NEW-703 / NEW-763 — đang skip và mang mã Studio lạ → đổi NEW-703 sang `FUNC-004` | `[BLOCKER]` |
| Q2 | `ENV-003` | Cao | **GAP** — 0 TC production; task chạm job nền (`recover:payment_univapay_timeout`, worker) + thanh toán, exception chỉ thấy trên production | `[BLOCKER]` |
| Q3 | `DEPLOY-LIVE-001` | Cao | **GAP** — release không maintain + API khung giờ đổi hợp đồng (422 mới) + `public/js/calendar_salon/booking.js` (+31) đổi cùng đợt: khách đang mở trang bằng JS cũ lúc release — 0 TC | `[BLOCKER]` |
| Q4 | `PERF-LARGE-001` | Trung bình | **RISK** — 4 TC (NEW-701, 702, 703, 762) đều skip; quy mô seed (30 nhân viên × 90 ngày, ≈ 20.000 đơn) không lấy từ số liệu thật của bot gặp lỗi (153361, 52318); expected không có ngưỡng đo (§5 I4) | `[MAJOR]` |
| Q5 | `JOB-001` | Cao | **RISK** — NEW-699 mang mã `JOB-002` (không có trong checklist) → đổi sang `JOB-001`. Thiếu Abnormal (RULE-01): dữ liệu lệnh đang đọc bị xoá giữa 2 lượt chạy | `[MAJOR]` |
| Q6 | `DATA-REF-001` | Cao | **RISK** — xoá bạn bè có đơn salon: chỉ có Normal (NEW-697 mang mã lạ, NEW-698 skip), thiếu Abnormal (RULE-01). Boundary không đề xuất: số lượng xoá hàng loạt không đổi trong sprint | `[MAJOR]` |
| Q7 | `REG-SHARED-001` · `SYNC-APP-001` | Cao · Trung bình (→ Cao, đặt lịch là flow critical) | **RISK** — Dev chưa cung cấp danh sách nơi gọi `getListTimeLineBooking` / API khung giờ (web tuần · tháng · danh sách · `order()` · API app `Mobile/CalendarSalonController`) → chưa biết app quản trị di động có chịu guard 31 ngày không | `[MAJOR]` |

**Đã loại khỏi phạm vi (có căn cứ):**
- `LIFF-ENTRY-001`: guard 31 ngày nằm ở API khung giờ, chạy sau khi trang đã mở; không đọc `id_token` / `u_code` / trạng thái kết bạn → ma trận điểm vào không đổi.
- Ma trận option 受付上限 × シフトの合算 × 指名 × 前後の空き時間: độ đúng khung giờ trên ma trận option thuộc T16 #41345 (`REQ-X-41345`, `CalendarSalonSlotGoldenTest`); guard 31 ngày chặn trước bước tính khung, không phụ thuộc option.
- `CONC-*`: không đổi luồng ghi đồng thời.
- `FUNC-003`: NEW-764 B4 (ngày sai → 422) + TC-FUNC004-01 ở §7 đủ cho thay đổi này.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-703 | NEW-763 → **gộp** vào NEW-703 | DUP-EXACT (sau khi sửa expected theo quy tắc 31 ngày) | mã (cả 2 cùng kiểm khoảng ngày bất thường) · Abnormal · gọi API khung giờ với khoảng > 31 ngày (365 ngày / 10 năm) · cùng lịch seed → cùng kết quả 422 | `[MINOR]` |

- **Gate đã chạy**: NEW-763 là TC duy nhất gắn `REQ-X-41529-01` → **gộp, không xoá**: chép dữ liệu "10 năm" + `timeShowWeek` như FE của NEW-763 thành bước thứ 2 của NEW-703, ghi cả 2 requirement key.
- Đã rà 10 TC (+ đối chiếu NEW-337 / NEW-339 của #38931 — khác ticket, khác thao tác), ngoài DUP-1 không phát hiện trùng lặp.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-699 | Giá trị `status_webhook` của đơn salon đang chờ webhook thanh toán | Tiền đề TC dựng `status_webhook = 3 / 4` (khớp câu SQL production ở exception mẫu 2 của #41718) | `spec-features/admin/salon-booking/db/db-mapping.md` L105: `status_webhook` "0=chưa xử lý, 1=đã xử lý, 2=lỗi (webhook thanh toán)" | (A) spec thiếu giá trị 3, 4 → cần update · (B) TC dựng dữ liệu không có thật | `[MINOR]` | `Dev` |

**Đã rà**: 10 TC × `spec-features/admin/salon-booking/` (`feature-spec.md`, `db/db-mapping.md`, `job/job-spec.md`) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 29 · 43–53) + `kho-tcs/fa013-friendlist-友だちリスト.md` (nhóm 12–13, Xoá bạn bè & cascade) — 1 mâu thuẫn (C1). Spec **không mô tả** API khung giờ trang khách lẫn lệnh `recover:payment_univapay_timeout` → quy tắc 31 ngày chưa có chuẩn để đối chiếu (§8 #2, #3).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Nguồn TC | **4/10 pass (40%)**. 6 TC skip: NEW-701, NEW-702, NEW-703 (#41717 → **0/3 pass**) · NEW-762, NEW-763 (#41529 → chỉ NEW-764 kiểm tham số sai pass, **chưa TC nào chứng minh hết lỗi bộ nhớ**) · NEW-698. Bug Studio #45409 đóng theo lượt #7415 (07/11); lần chạy gần nhất (13/11) của NEW-703 / NEW-763 lại skip | Chuẩn bị seed dữ liệu lớn rồi chạy lại 6 TC; NEW-703 / NEW-763 sửa expected trước (I2) |
| I2 | `[MAJOR]` | NEW-703 · NEW-763 · NEW-762 · NEW-701 · NEW-702 | Expected còn 2 nhánh "4xx … **hoặc** 200 …" trong khi quy tắc đã chốt qua #45409 (422 「表示期間は31日以内で指定してください。」). 3 TC còn lại chưa kiểm "không bị 422" (REG-SPEC-001) | NEW-703 / NEW-763: expected = 422 + message. NEW-701 / 702 / 762: thêm 1 dòng expected "không request nào trả 422 表示期間…" |
| I3 | `[MAJOR]` | Input thiếu từ Dev | (1) 3 ticket không có đánh giá ảnh hưởng / commit — #41717 / #41529 coi là xong nhờ #41345 + guard #45409, hay còn sửa `order()` / lịch tháng? (2) endpoint thật của exception #41529 (server `step.lme.jp`, kèm user admin 177888 — có thể là màn quản trị, không phải trang khách) chưa xác định; (3) nguyên nhân #41718; (4) API app `Mobile/CalendarSalonController` (+304) có gọi API khung giờ / chịu guard 31 ngày không; (5) `CalendarSalonInitDataBookingGuardTest` (+131) chặn gì | Hỏi Dev, cập nhật `03-dev-impact.md`, review lại G2 / G4 / Q7 |
| I4 | `[MAJOR]` | NEW-701 · NEW-762 | Expected không đo được: "không hết thời gian chạy", "vài trăm KB trở xuống (chỉ tham khảo)"; quy mô seed không dựa trên dữ liệu thật | Leader chốt ngưỡng (thời gian phản hồi, bộ nhớ); Dev / DBA cung cấp số dòng `calendar_salon_time_booking` + `calendar_salon_line_booking` của bot 153361, 52318 → seed ≥ mức đó |
| I5 | `[MAJOR]` | NEW-697 | B4 kỳ vọng "dữ liệu bot khác không đổi" nhưng tiền đề không dựng dữ liệu ở bot khác cho cùng 30 bạn bè → B4 luôn Đạt, không kiểm được phạm vi xoá (DATA-DB-001) | Thêm tiền đề: 3/30 bạn bè cũng là bạn của bot test thứ 2, mỗi người 1 đơn salon ở bot đó |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 10 TC — không có TC nào ngoài phạm vi task. (NEW-764 kiểm validate calendarId — thuộc guard API trong diff, fix bug Studio #45410; NEW-700 là TC duy nhất kiểm giả thuyết worker của `REQ-X-41718-02`.)

---

## 7. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 29 予約の開始・締切 · 43–48 LINE user · 49 Đồng thời & verify API · 50 Job nền · 51 App mobile · 53 Dữ liệu cũ & hồi quy) · `kho-tcs/fa013-friendlist-友だちリスト.md` (nhóm 12 ブロックされた友だち · 13 ブロックした友だち · Xoá bạn bè & cascade) |
| Vùng regression phát hiện từ kho | TC-SLN-435 / TC-SLN-436 (chọn & điều hướng tuần / tháng) · TC-SLN-490 (hiệu năng API calendar salon) · TC-FRL-137 (xoá hàng loạt ở 2 màn chặn) · TC-FRL-142 (xoá bạn bè nhiều dữ liệu) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho | Không — TC-FRL-137 xoá ở màn user-block nhưng bạn bè không có đơn salon, không kiểm lỗi DB → dẫn chiếu trong TC-DATAREF001-01 |
| Căn cứ TC regression `R<x>` | Không có TC R riêng — vùng regression đã nằm trong G1 / G3 |
| Xác nhận chống trùng | Đã đối chiếu 10 TC ở BƯỚC 0 + NEW-337 / NEW-339 (#38931) + kho FA-020 / FA-013 — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC004-01 | API | FUNC-004 | Salon booking サロン予約 (API khung giờ get-list-time-booking): Biên khoảng hiển thị 表示期間 31 ngày | Boundary | auto | dev, local, prd, staging | api | Khoảng ngày 1 ngày và 31 ngày trả khung giờ; 32 ngày bị từ chối 422 「表示期間は31日以内で指定してください。」 | - Bot test có lịch salon 「QA45229B_Salon31」 đang bật, 2 nhân viên S1 / S2 có ca 10:00–18:00 mọi ngày trong 60 ngày tới, 1 menu M1 (60 phút).<br>- Khách QA45229B_F01 (gọi tắt F01) là bạn bè của bot, có link đặt lịch riêng (u_code).<br>- F01 mở trang đặt lịch, chọn M1 + 指名なし; tester lấy request `GET /ajax/mobile/calendar-salon/get-list-time-booking` của tuần đầu ở DevTools (Network) làm mẫu. | 1. Gửi lại request mẫu với start_date = D, end_date = D.<br>2. Gửi lại với start_date = D, end_date = D + 30 ngày.<br>3. Gửi lại với start_date = D, end_date = D + 31 ngày.<br>4. Gửi lại với start_date = D − 1 ngày, end_date = D + 30 ngày. | D = ngày mai.<br>Các tham số khác giữ nguyên như request mẫu. | - B1: HTTP 200, JSON có khung giờ của ngày D.<br>- B2: HTTP 200, JSON có khung giờ đủ 31 ngày D … D + 30.<br>- B3: HTTP 422, message 「表示期間は31日以内で指定してください。」, không có dữ liệu khung giờ.<br>- B4: HTTP 422, cùng message (32 ngày, lệch ở đầu).<br>- Không request nào trả 500. | | Lấp G1 / Q1 · Đánh giá spec: Spec không ghi — quy tắc từ fix bug Studio #45409; cách đếm "31 ngày" (tính cả ngày đầu và cuối) suy từ message, Dev xác nhận trước khi chạy · Evidence: request + response 4 lần gọi |
| TC-FUNC001-01 | UI | FUNC-001 | Salon booking サロン予約 (trang khách): 3 chế độ hiển thị tuần / tháng / danh sách với lịch nhận đặt 180 ngày | Normal | auto | dev, local, prd, staging | line-friend, web | Trang đặt lịch ở chế độ tuần, tháng và danh sách với lịch nhận đặt 180 ngày: đi tới cuối phạm vi không gặp lỗi 422 表示期間 | - Đăng nhập admin (主管理者) bot test.<br>- Lịch salon 「QA45229B_Salon180」 đang bật; tab 「予約設定」 → 「予約の開始・締切」: bắt đầu nhận đặt trước 180 ngày.<br>- 2 nhân viên S1 / S2 có ca 10:00–18:00 mọi ngày trong 180 ngày tới; menu M1 (60 phút).<br>- Khách QA45229B_F01 (gọi tắt F01) là bạn bè của bot, có link đặt lịch. | 1. Admin cài trang đặt lịch hiển thị theo tuần.<br>2. F01 mở trang đặt lịch, chọn M1 + 指名なし.<br>3. F01 bấm tuần kế tiếp liên tục tới tuần chứa ngày thứ 180, theo dõi DevTools Network.<br>4. Admin cài hiển thị theo tháng.<br>5. F01 mở lại trang, chọn M1 + 指名なし, bấm tháng kế tiếp tới tháng chứa ngày thứ 180, ở mỗi tháng bấm 1 ngày có ca.<br>6. Admin cài hiển thị dạng danh sách.<br>7. F01 mở lại trang, chọn M1 + 指名なし, cuộn tới cuối danh sách khung giờ.<br>8. Ở mỗi chế độ, F01 chọn 1 khung trong tuần / tháng cuối và đi tới màn xác nhận (không bấm 「予約確定」). | Phạm vi nhận đặt: 180 ngày.<br>Ngày cuối nhận đặt: hôm nay + 180 ngày. | - B3, B5, B7: mọi request khung giờ trả HTTP 200; **không** request nào trả 422 「表示期間は31日以内で指定してください。」; không màn trắng, không spinner treo.<br>- Tuần / tháng / danh sách cuối hiển thị khung tới đúng ngày thứ 180; ngày sau ngày thứ 180 không có khung đặt được.<br>- B8: tới được màn xác nhận ở cả 3 chế độ. | | Lấp G1 · regression — dẫn từ TC-SLN-435 / TC-SLN-436 · chế độ danh sách = request có `timeShowWeek=1` (theo NEW-703) · Đánh giá spec: Spec không ghi (API khung giờ không có trong spec-features) · Evidence: HAR Network 3 chế độ + screenshot tuần / tháng cuối |
| TC-DEPLOYLIVE001-01 | UI | DEPLOY-LIVE-001 | Salon booking サロン予約 (trang khách): khách đang mở trang đặt lịch lúc release | Normal | auto | staging, prd | line-friend | Khách mở trang đặt lịch trước release (JS bản cũ) rồi thao tác tiếp sau release: không lỗi 422, đặt được lịch | - Bot test (staging, và bot test production) có lịch salon 「QA45229B_SalonLive」 đang bật, 2 nhân viên có ca mọi ngày trong 60 ngày tới, menu M1 (60 phút).<br>- Khách QA45229B_F01 (gọi tắt F01) là bạn bè của bot, có link đặt lịch.<br>- Biết giờ deploy bản sprint #45229. | 1. Trước deploy 10 phút: F01 mở trang đặt lịch, chọn M1 + 指名なし, để ở tuần hiện tại.<br>2. Chờ deploy xong, không tải lại trang.<br>3. F01 bấm tuần kế tiếp 3 lần.<br>4. Nếu lịch cho xem theo tháng: chuyển sang tháng, bấm tháng kế tiếp 1 lần.<br>5. F01 chọn 1 khung, nhập thông tin, bấm 「予約確定」.<br>6. F01 tải lại trang, lặp bước 3–4. | Thời điểm mở trang: 10 phút trước deploy. | - B3, B4: khung giờ hiển thị; không request nào trả 422 「表示期間は31日以内で指定してください。」 hay 500; nếu bị chặn thì trang báo lỗi rõ và tải lại được, không màn trắng.<br>- B5: đặt thành công, đơn hiện ở 予約管理.<br>- B6: hiển thị như B3–B4 bằng JS bản mới. | | Lấp Q3 · chỉ staging+prd vì cần deploy thật · `public/js/calendar_salon/booking.js` (+31) đổi cùng đợt — Dev chưa xác nhận có đổi cách gửi khoảng ngày · Đánh giá spec: Spec không ghi · Evidence: HAR trước / sau deploy + mã đơn |
| TC-ENV003-01 | Data | ENV-003 | Salon booking サロン予約 (trang khách + API khung giờ): giám sát exception sau release trên production | Normal | manual | prd | web | 7 ngày sau release không còn exception hết thời gian / hết bộ nhớ ở luồng khung giờ salon | - Bản sprint #45229 đã release production.<br>- Có quyền xem room Chatwork SNSLineException và dashboard check-exception.<br>- Mốc trước release: #41717 (`Maximum execution time … Collection`, server s.lmes.jp, bot 153361) 1 lần ngày 2026-09-28; #41529 (`Allowed memory size … JsonResponse`, server step.lme.jp, bot 52318) 10 lần ngày 2026-09-25. | 1. Ghi giờ release.<br>2. Mỗi ngày trong 7 ngày sau release, lọc dashboard check-exception theo signature `Maximum execution time … Collection`.<br>3. Cùng ngày, lọc theo signature `Allowed memory size … JsonResponse`.<br>4. Với mỗi exception tìm được, ghi URL request, bot_id, thời điểm. | Thời gian theo dõi: 7 ngày.<br>2 signature của #41717, #41529. | - Không có exception nào của 2 signature ở request trang đặt lịch salon / API khung giờ / đặt lịch trong 7 ngày.<br>- Nếu có: danh sách URL + bot_id + thời điểm, mở lại #41717 / #41529 kèm dữ liệu này. | | Lấp G2 / Q2 · chỉ prd vì exception chỉ xảy ra với dữ liệu khách hàng thật · manual vì chỉ chạy trên production · Surface web vì phán quyết đọc trên dashboard trình duyệt · Đánh giá spec: không áp dụng · Evidence: ảnh dashboard 7 ngày |
| TC-ENV003-02 | Job | ENV-003 | Friend list 友だちリスト + UnivaPay 決済 (lệnh recover:payment_univapay_timeout): giám sát lỗi Packets out of order sau release trên production | Normal | manual | prd | job | 7 ngày sau release không còn lỗi Packets out of order khi đọc đơn salon (xoá bạn bè đã chặn + lệnh khôi phục thanh toán quá hạn) | - Bản sprint #45229 đã release production.<br>- Có quyền xem dashboard check-exception; Dev hỗ trợ lấy log server của lệnh `recover:payment_univapay_timeout`.<br>- Mốc trước release: #41718 — 4 lần + 1 nhóm gộp, 2026-09-28 → 29, server step.lme.jp. | 1. Ghi giờ release.<br>2. Mỗi ngày trong 7 ngày, lọc dashboard check-exception theo signature `Packets out of order … Connection`.<br>3. Với mỗi exception, ghi câu SQL, server, thời điểm.<br>4. Ngày thứ 7, nhờ Dev lấy log lệnh `recover:payment_univapay_timeout` của 1 ngày, đếm số lượt chạy và số lượt lỗi DB. | Thời gian theo dõi: 7 ngày.<br>Lệnh chạy mỗi 5 phút. | - Không có exception `Packets out of order` ở 2 câu SQL đọc `calendar_salon_line_booking` (theo line_user_id + bot_id; theo status_webhook + charge_id).<br>- B4: lệnh chạy đủ 288 lượt / ngày, 0 lượt lỗi DB.<br>- Nếu có lỗi: ghi điều kiện (giờ, câu SQL) và mở lại #41718. | | Lấp G2 / Q2 · chỉ prd vì lỗi giao thức DB chỉ thấy trên hạ tầng production · manual vì chỉ chạy trên production · Đánh giá spec: không áp dụng · Evidence: ảnh dashboard + log lệnh |
| TC-DATAREF001-01 | Data | DATA-REF-001 | Friend list 友だちリスト: Xoá ở màn bạn bè chặn bot ブロックされた友だち khi bạn bè có đơn salon | Normal | auto | dev, local, prd, staging | web | Xoá từng người và xoá hàng loạt ở màn ブロックされた友だち: bạn bè có đơn salon bị xoá đủ đơn, bot khác không bị chạm, không lỗi DB | - Đăng nhập admin (主管理者) bot test A.<br>- 6 khách QA45229B_F01 … QA45229B_F06 (gọi tắt F01 … F06) đã chặn bot A (hiện ở ブロックされた友だち); mỗi người có 2 đơn ở lịch salon 「QA45229B_SalonDel」 của bot A (1 đơn 予約確定, 1 đơn 予約リクエスト).<br>- F05, F06 cũng là bạn bè của bot test B, mỗi người có 1 đơn salon ở lịch của bot B.<br>- QA45229B_F07 (gọi tắt F07) cũng chặn bot A, có 1 đơn salon ở bot A — không bị chọn xoá. | 1. Mở `/basic/friendlist/user-block` (ブロックされた友だち).<br>2. Bấm 「削除」 ở dòng F01, xác nhận.<br>3. Chọn F02 … F06, bấm xoá hàng loạt, xác nhận.<br>4. Mở 予約管理 của lịch 「QA45229B_SalonDel」 (bot A).<br>5. Đổi sang bot B, mở 予約管理 lịch salon của bot B.<br>6. Kiểm DB `calendar_salon_line_booking` theo line_user_id của F01 … F07. | Xoá từng người: F01.<br>Xoá hàng loạt: F02 … F06. | - B2, B3: màn tải lại, không lỗi; F01 … F06 không còn trong danh sách; F07 vẫn còn.<br>- B4: không còn đơn nào của F01 … F06 ở bot A (bạn bè đã bị xoá); đơn của F07 còn nguyên (F07 không bị chọn).<br>- B5: đơn của F05, F06 ở bot B còn nguyên (xoá ở bot A không chạm bot B).<br>- B6: DB khớp B4–B5; log không có `Packets out of order` / QueryException. | | Lấp G3 / Q6 · regression — `public/js/friendlist/user_block.js` + `user_block.blade.php` đổi trong sprint · dẫn từ TC-FRL-137 (xoá hàng loạt 2 màn chặn, chưa có đơn salon) · Đánh giá spec: Spec không ghi việc xoá đơn salon khi xoá bạn bè — hỏi Leader · Evidence: screenshot danh sách + query DB trước / sau |
| TC-DATAREF001-02 | Job | DATA-REF-001 | UnivaPay 決済 + Friend list 友だちリスト (lệnh recover:payment_univapay_timeout): đơn chờ thanh toán của bạn bè vừa bị xoá | Abnormal | auto | dev, local, prd, staging | job, web | Bạn bè có đơn salon đang chờ webhook thanh toán UnivaPay bị xoá: lượt chạy kế tiếp của lệnh khôi phục không lỗi, đơn của người khác vẫn được xử lý | - Đăng nhập admin (主管理者) bot test A; lịch salon 「QA45229B_SalonPay」 bật thanh toán UnivaPay (store test, không gọi thanh toán thật).<br>- Khách QA45229B_F01 (gọi tắt F01) đã chặn bot A, có 1 đơn đang chờ webhook thanh toán (status_webhook = 3, có charge_id, tạo cách đây 20 phút).<br>- Khách QA45229B_F02 (gọi tắt F02) là bạn bè bình thường, có 1 đơn cùng trạng thái, tạo cách đây 20 phút.<br>- Lệnh `recover:payment_univapay_timeout` chưa chạy trên 2 đơn này. | 1. Admin mở `/basic/friendlist/user-block`, xoá F01.<br>2. Chạy lệnh `recover:payment_univapay_timeout` (hoặc chờ lượt chạy 5 phút kế tiếp).<br>3. Đọc log lượt chạy vừa rồi.<br>4. Mở 予約管理 lịch 「QA45229B_SalonPay」, xem đơn của F02. | Đơn chờ thanh toán: 2 (F01, F02), quá 15 phút. | - B2: lệnh kết thúc bình thường, không exception (không `Packets out of order`, không lỗi đọc đơn đã xoá).<br>- B3: log không có dòng xử lý đơn của F01 (đơn đã bị xoá cùng bạn bè); có dòng xử lý đơn của F02.<br>- B4: đơn của F02 đổi trạng thái theo kết quả lượt chạy, không bị bỏ sót. | | Lấp Q5 / Q6 · 2 câu SQL của #41718 cùng đọc `calendar_salon_line_booking` — 1 từ luồng xoá bạn bè, 1 từ lệnh 5 phút · RULE-08 (job + thanh toán): giữ đủ 4 env; prd chỉ chạy được khi có đơn chờ webhook thật — Leader quyết · Đánh giá spec: Spec không ghi (spec không mô tả lệnh này; giá trị status_webhook 3 xem §4 C1) · Evidence: log lệnh + trạng thái 2 đơn |

**Không đề xuất TC mới (có lý do):**
- **G4** (nguyên nhân #41718): chờ Dev xác định nguyên nhân (§5 I3) — không tự đoán giả thuyết thứ 2. TC-ENV003-02 là bằng chứng production tạm thời.
- **Q4** (`PERF-LARGE-001`): đã có 4 TC — sửa tiền đề + ngưỡng theo §5 I4, chạy lại.
- **Q7** (`REG-SHARED-001` · `SYNC-APP-001`): chưa đề xuất TC app quản trị di động khi Dev chưa xác nhận app có gọi API khung giờ (§5 I3).
- Đổi mã quan điểm (không cần TC mới): NEW-703 → `FUNC-004` · NEW-699 → `JOB-001` · NEW-697 → `DATA-REF-001` · NEW-701 → `FUNC-001`.

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/salon-booking/db/db-mapping.md` L105 — cột `status_webhook` | Bổ sung giá trị 3, 4 (đơn chờ webhook thanh toán — lệnh `recover:payment_univapay_timeout` đọc) | C1 `CONF-SPEC` ở §4 | `Dev` |
| 2 | `spec-features/admin/salon-booking/web/api-spec.md` — chưa có API khung giờ trang khách | Thêm `GET /ajax/mobile/calendar-salon/get-list-time-booking`: khoảng hiển thị ≤ 31 ngày (ghi rõ cách đếm) → 422 「表示期間は31日以内で指定してください。」; calendarId không tồn tại → 404 「カレンダーが見つかりません。」; thiếu / sai tham số → 422 「パラメータが不正です。」 | Quy tắc mới từ fix bug Studio #45409 / #45410 — spec chưa có | `Dev / Leader` |
| 3 | `spec-features/admin/salon-booking/job/job-spec.md` | Thêm lệnh `recover:payment_univapay_timeout`: chu kỳ 5 phút, điều kiện chọn đơn (status_webhook 3 / 4, có charge_id, tạo quá 15 phút), xử lý khi lỗi từng đơn | Spec thiếu lệnh này | `Dev` |
