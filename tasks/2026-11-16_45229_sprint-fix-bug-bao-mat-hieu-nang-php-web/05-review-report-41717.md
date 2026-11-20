# 05 — Review Report

> Draft cho Leader verify. **Sprint #45229 · T15 · sub-task #41717** — `Maximum execution time of 500 seconds exceeded` (Collection.php) ở luồng khung giờ / đặt lịch salon phía khách với dữ liệu lớn, review 2026-11-19. Bản này thay phần #41717 của report lượt B (`45229-B_t15-exception-salon-du-lieu-lon/05-review-report.md`). Main case nằm ở §9.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) Studio task #560` (task cha #45229, fetch 2026-11-19, 1287 TC) — lọc TC gắn `REQ-X-41717-*` |
| Tổng số TC review | 3 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev **không** viết đánh giá cho #41717 (không commit riêng). Dùng 6 mục ghép từ requirement Studio `REQ-X-41717` / `-01` / `-02` + `45229-B/03-dev-impact.md`: BUG timeout · 「予約確定」 trên dữ liệu lớn (`order()`) · API khung giờ khoảng ngày dài → 422 (#45409) · lịch tháng (`initDataBooking`) · đọc `calendar_salon_time_booking` khối lượng lớn · lịch tuần trang khách | `6/6 mục có TC` — **CHƯA ĐỦ** (6 RISK — cả 3 TC chưa chạy) |
| **(b) diff code** — 5 điểm chạm luồng của #41717: guard khoảng ngày ≤ 31 ở `Api/CalendarSalonController` (`CalendarSalonListTimeBookingGuardTest` +158) · guard `initDataBooking` (`CalendarSalonInitDataBookingGuardTest` +131) · hành vi siết lại (> 31 ngày trước trả dữ liệu, nay 422) · `public/js/calendar_salon/booking.js` (+31) · nơi gọi `getListTimeLineBooking` / API khung giờ | `3/5 điểm có TC` — **CHƯA ĐỦ** (2 GAP · 3 RISK) |

**Kết luận**: `0/11 vùng ảnh hưởng đủ TC · 2 GAP · 9 RISK`.

Loại khỏi mẫu số: truy vấn khung giờ tuần viết lại (T16 #41345, commit `229f1a4788` — review ở nhóm T16) · Google Calendar / Sheet / phân bổ nhân viên trong `CalendarSalon*` (T9 / T10 / T16).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Quy tắc mới **khoảng hiển thị ≤ 31 ngày → 422 「表示期間は31日以内で指定してください。」** (fix bug Studio #45409, sinh ra từ chính NEW-703) | diff code | NEW-703 (skip, expected cũ "4xx **hoặc** 200") | **GAP** — (1) biên 31 / 32 ngày: 0 TC; (2) hành vi bị **siết lại** nhưng chưa TC nào chứng minh khách dùng bình thường không bị 422: lịch tuần + lịch tháng đi hết phạm vi nhận đặt (tối đa 180 ngày — kho TC-SLN-308), trang tự nhảy tới tuần có ca khi các tuần đầu trống (kho TC-SLN-434 / 435) | `[BLOCKER]` |
| G2 | BUG #41717 — timeout 500 giây trên production (`s.lmes.jp`, bot 153361) + 4 mục dev-impact còn lại (「予約確定」 · lịch tháng · đọc khối lượng lớn · lịch tuần) | dev-impact | NEW-701 · NEW-702 · NEW-703 — **cả 3 skip** (`needs-prep`, chưa dựng được dữ liệu lớn, run #7775 / #7782 ngày 13/11) | **RISK** — 0 TC Đạt, chưa có bằng chứng nào #41717 hết timeout; quy mô seed (30 nhân viên × 90 ngày, ≈ 20.000 đơn) không lấy từ dữ liệu thật của bot 153361; chưa TC nào xác nhận sau release signature không còn | `[BLOCKER]` |
| G3 | `public/js/calendar_salon/booking.js` (+31) đổi cùng đợt với API khung giờ đổi hợp đồng (thêm 422) | diff code | không có | **GAP** — release không maintain: khách đang mở trang bằng JS cũ lúc release; Dev chưa nói booking.js đổi gì | `[MAJOR]` |
| G4 | Guard `initDataBooking` (lịch tháng) + nơi gọi `getListTimeLineBooking` / API khung giờ | diff code | NEW-702 (skip) | **RISK** — Dev chưa mô tả guard `initDataBooking` chặn gì; chưa có danh sách nơi gọi (`order()` · lịch tuần · lịch tháng · app quản trị `Mobile/CalendarSalonController` +321) → chưa biết lịch tháng / app có bị chặn nhầm không (§5 I4) | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `7 quan điểm Trigger khớp task · 7 chưa cover đủ` (cả 3 TC chưa chạy).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-004` | Cao | **GAP** — giới hạn mới 31 ngày: 0 TC mang mã; Abnormal chỉ có NEW-703 (mã `TOOL-ERRHYG-001`, skip); **Normal + Boundary 0 TC** (RULE-01) → TC-FUNC004-01 | `[BLOCKER]` |
| Q2 | `DEPLOY-LIVE-001` | Cao | **GAP** — release không maintain + API đổi hợp đồng (422 mới) + `booking.js` đổi cùng đợt → 0 TC → TC-DEPLOYLIVE001-01 | `[BLOCKER]` |
| Q3 | `REG-SPEC-001` | Cao | **RISK** — quy tắc 31 ngày chốt **sau** khi NEW-701 / 702 / 703 đã viết (#45409 Closed 07/11) nhưng 3 TC chưa cập nhật: NEW-703 expected còn 2 nhánh, NEW-701 / 702 chưa kiểm "không bị 422" (§5 I2) | `[MAJOR]` |
| Q4 | `FUNC-001` | Cao | **RISK** — 「予約確定」 trên dữ liệu lớn chỉ có NEW-701 (mã `TOOL-KNOW-002` — đổi sang `FUNC-001`), đang skip | `[MAJOR]` |
| Q5 | `PERF-LARGE-001` | Trung bình | **RISK** — NEW-702 (Boundary) skip; expected không có ngưỡng đo; quy mô seed không dựa trên dữ liệu thật (§5 I3) | `[MAJOR]` |
| Q6 | `REG-SHARED-001` · `SYNC-APP-001` | Cao · Trung bình (→ Cao, đặt lịch là flow critical) | **RISK** — chưa có danh sách nơi gọi `getListTimeLineBooking` / API khung giờ → chưa biết app quản trị di động có chịu guard 31 ngày không (§5 I4) | `[MAJOR]` |

**Đã loại khỏi phạm vi (có căn cứ):**
- `LIFF-ENTRY-001`: guard 31 ngày nằm ở API khung giờ, chạy sau khi trang đã mở; không đọc `id_token` / `u_code` / trạng thái kết bạn → ma trận điểm vào không đổi.
- Ma trận option 受付上限 × シフトの合算 × 指名 × 前後の空き時間: độ đúng khung trên ma trận option thuộc T16 #41345 (`CalendarSalonSlotGoldenTest`); guard 31 ngày chặn trước bước tính khung, không phụ thuộc option.
- `CONC-001`: không đổi luồng ghi đồng thời (kho TC-SLN-459 giữ nguyên).
- `ENV-003` / RULE-08: #41717 không chạm media / domain / job nền / thanh toán; xác nhận production đi theo G2 (TC-ENV003-01).
- `DATA-DB-001`: luồng chỉ đọc + tạo đơn, không UPDATE / DELETE mới.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-703 | NEW-763 (#41529, cùng task #560) → **gộp** vào NEW-703 | DUP-EXACT (sau khi sửa expected theo quy tắc 31 ngày) | mã (cùng kiểm khoảng ngày bất thường) · Abnormal · gọi API khung giờ với khoảng > 31 ngày (365 ngày / 10 năm) · cùng lịch seed → cùng kết quả 422 | `[MINOR]` |

- **Gate đã chạy**: NEW-763 là TC duy nhất gắn `REQ-X-41529-01` → **gộp, không xoá**: chép dữ liệu "10 năm" của NEW-763 thành bước thứ 2 của NEW-703, ghi cả 2 requirement key. (Giữ nguyên kết luận của report lượt B.)
- Đã rà 3 TC + NEW-337 (#38931 lịch tuần dữ liệu ca lớn) + NEW-762 / 763 / 764 (#41529 / #45410): ngoài DUP-1 không phát hiện trùng.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` | NEW-703 | Chế độ hiển thị của trang đặt lịch salon phía khách ứng với tham số `timeShowWeek=1` | Tiêu đề + bước NEW-703: "API khung giờ **dạng danh sách** (`timeShowWeek=1`)" | Kho `TC-SLN-347`: màn chọn slot chỉ có 2 cách hiển thị **theo tuần / theo tháng**. Spec lesson (cùng cơ chế) `lesson-booking/web/api-spec-public.md` L167: `timeShowWeek == 1` ⇒ **tự nhảy tới tuần có chỗ** (server thử tối đa 4 tuần kế tiếp) | (A) TC hiểu sai tham số → sửa tiêu đề / bước NEW-703, và TC nào đề xuất theo "chế độ danh sách" (TC-FUNC001-01 ở §7 lượt B) phải bỏ · (B) salon có chế độ danh sách mà kho chưa ghi → update kho FA-020 | `[MAJOR]` | `Dev` |

**Đã rà**: 3 TC × `spec-features/admin/salon-booking/` (`feature-spec.md`, `web/api-spec.md` — **không mô tả** API khung giờ trang khách) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 29 予約の開始・締切 · 35 予約ページ表示設定 · 45 LINE user — chọn slot · 49 Đồng thời & verify API · 51 App mobile) — 1 mâu thuẫn (C1). Quy tắc 31 ngày chưa có trong spec để đối chiếu (§8 #1).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Nguồn TC | **0/3 Đạt**. NEW-701, NEW-702, NEW-703 đều `skip` trạng thái `needs-prep` (chưa dựng được lịch 30 nhân viên × 90 ngày + ≈ 20.000 đơn) từ 13/11, chưa chạy lại; chỉ có scope `local` | Chuẩn bị seed dữ liệu lớn rồi chạy lại 3 TC (sau khi sửa expected ở I2) |
| I2 | `[MAJOR]` | NEW-703 · NEW-701 · NEW-702 | NEW-703 expected còn 2 nhánh "4xx **hoặc** 200 trong giới hạn" trong khi quy tắc đã chốt: 422 「表示期間は31日以内で指定してください。」. NEW-701 / 702 chưa có dòng "không request nào trả 422" | NEW-703: expected = HTTP 422 + message, gộp dữ liệu 10 năm của NEW-763 (DUP-1), sửa tiêu đề theo C1. NEW-701 / 702: thêm expected "không request khung giờ nào trả 422 表示期間…" |
| I3 | `[MAJOR]` | NEW-701 · NEW-702 | Expected không đo được: "không hết thời gian chạy", "thời gian đo ghi tham khảo". Quy mô seed tự đặt, không dựa trên dữ liệu thật của bot gặp lỗi | Leader chốt ngưỡng thời gian phản hồi; Dev / DBA cung cấp số dòng `calendar_salon_time_booking` + `calendar_salon_line_booking` của bot 153361 → seed ≥ mức đó |
| I4 | `[MAJOR]` | Input thiếu từ Dev | (1) #41717 không có commit riêng — coi là xong nhờ T16 #41345 + guard #45409, hay còn phải sửa `order()` / lịch tháng? (2) `CalendarSalonInitDataBookingGuardTest` (+131): guard lịch tháng chặn gì? (3) danh sách nơi gọi `getListTimeLineBooking` / API khung giờ, gồm app quản trị `Mobile/CalendarSalonController` (+321)? (4) `booking.js` (+31) đổi gì — có đổi cách gửi khoảng ngày không? (5) salon có dùng cơ chế `timeShowWeek=1` tự nhảy tuần như lesson không (C1) | Hỏi Dev, cập nhật G2 / G3 / G4 / Q6 và slot B4 ở §9 |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 3 TC — không có TC nào ngoài phạm vi task.

---

## 7. TCs đề xuất bổ sung (4)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 29 · 35 · 43–49 · 51 · 53) |
| Vùng regression phát hiện từ kho | TC-SLN-308 (nhận đặt trước 1–180 ngày) · TC-SLN-347 (hiển thị theo tuần / tháng) · TC-SLN-434 / 435 (tự chọn tuần / tháng có ca khi các tuần đầu trống) · TC-SLN-436 (điều hướng tuần / tháng) |
| Conflict expected vs kho | Không (C1 ở §4 là mâu thuẫn của TC hiện có, không phải TC đề xuất) |
| GAP dùng lại TC kho | Không — kho chưa có TC nào kiểm biên 31 ngày hay đi hết 180 ngày sau khi có guard |
| Căn cứ TC regression `R<x>` | Không có TC R riêng — vùng regression đã nằm trong G1 (TC-FUNC001-02) |
| Xác nhận chống trùng | Đã đối chiếu 3 TC ở BƯỚC 0 + NEW-337 / 762 / 763 / 764 + kho FA-020 — **không TC đề xuất nào trùng**. TC-FUNC004-01, TC-DEPLOYLIVE001-01, TC-ENV003-01 **giữ nguyên ID + nội dung** như §7 lượt B (push lại idempotent theo `client_ref`); TC-FUNC001-02 **thay** TC-FUNC001-01 của lượt B (bỏ "chế độ danh sách" theo C1) — **không push TC-FUNC001-01** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC004-01 | API | FUNC-004 | Salon booking サロン予約 (API khung giờ get-list-time-booking): Biên khoảng hiển thị 表示期間 31 ngày | Boundary | auto | dev, local, prd, staging | api | Khoảng ngày 1 ngày và 31 ngày trả khung giờ; 32 ngày bị từ chối 422 「表示期間は31日以内で指定してください。」 | - Bot test có lịch salon 「QA45229B_Salon31」 đang bật, 2 nhân viên S1 / S2 có ca 10:00–18:00 mọi ngày trong 60 ngày tới, 1 menu M1 (60 phút).<br>- Khách QA45229B_F01 (gọi tắt F01) là bạn bè của bot, có link đặt lịch riêng (u_code).<br>- F01 mở trang đặt lịch, chọn M1 + 指名なし; tester lấy request `GET /ajax/mobile/calendar-salon/get-list-time-booking` của tuần đầu ở DevTools (Network) làm mẫu. | 1. Gửi lại request mẫu với start_date = D, end_date = D.<br>2. Gửi lại với start_date = D, end_date = D + 30 ngày.<br>3. Gửi lại với start_date = D, end_date = D + 31 ngày.<br>4. Gửi lại với start_date = D − 1 ngày, end_date = D + 30 ngày. | D = ngày mai.<br>Các tham số khác giữ nguyên như request mẫu. | - B1: HTTP 200, JSON có khung giờ của ngày D.<br>- B2: HTTP 200, JSON có khung giờ đủ 31 ngày D … D + 30.<br>- B3: HTTP 422, message 「表示期間は31日以内で指定してください。」, không có dữ liệu khung giờ.<br>- B4: HTTP 422, cùng message (32 ngày, lệch ở đầu).<br>- Không request nào trả 500. | | Lấp G1 / Q1 · Đánh giá spec: Spec không ghi — quy tắc từ fix bug Studio #45409; cách đếm "31 ngày" (tính cả ngày đầu và cuối) suy từ message, Dev xác nhận trước khi chạy · Evidence: request + response 4 lần gọi |
| TC-FUNC001-02 | UI | FUNC-001 | Salon booking サロン予約 (trang khách): lịch tuần / tháng với phạm vi nhận đặt 180 ngày sau khi có giới hạn 表示期間 31 ngày | Normal | auto | dev, local, prd, staging | line-friend, web | Lịch nhận đặt 180 ngày, 14 ngày đầu không có ca: trang tự nhảy tới tuần có ca, đi hết phạm vi ở chế độ tuần và tháng mà không request nào bị 422 表示期間 | - Đăng nhập admin (主管理者) bot test.<br>- Lịch salon 「QA45229_41717_Salon180」 đang bật; tab 「予約設定」 → 「予約の開始・締切」: bắt đầu nhận đặt trước 180 ngày.<br>- 2 nhân viên S1 / S2 có ca 10:00–18:00 mọi ngày **từ ngày thứ 15 tới ngày thứ 180** kể từ hôm nay (14 ngày đầu không có ca); menu M1 (60 phút), S1 / S2 làm được M1.<br>- Khách QA45229_F01 (gọi tắt F01) là bạn bè của bot, có link đặt lịch. | 1. Admin cài màn chọn khung của trang đặt lịch hiển thị **theo tuần**.<br>2. F01 mở trang đặt lịch, chọn M1 + 指名なし; mở DevTools (Network) theo dõi request khung giờ.<br>3. F01 bấm tuần kế tiếp liên tục tới tuần chứa ngày thứ 180.<br>4. F01 chọn 1 khung trong tuần cuối, đi tới màn xác nhận (không bấm 「予約確定」).<br>5. Admin cài hiển thị **theo tháng**.<br>6. F01 mở lại trang, chọn M1 + 指名なし; bấm tháng kế tiếp tới tháng chứa ngày thứ 180, ở mỗi tháng bấm 1 ngày có ca.<br>7. F01 chọn 1 khung ở tháng cuối, đi tới màn xác nhận (không bấm 「予約確定」). | Phạm vi nhận đặt: 180 ngày<br>Ngày đầu có ca: hôm nay + 14 ngày<br>Ngày cuối nhận đặt: hôm nay + 180 ngày | - B2: trang mở thẳng tuần chứa ngày thứ 15 (tuần có ca gần nhất), không dừng ở tuần hiện tại trống.<br>- B3, B6: mọi request khung giờ / dữ liệu lịch trả HTTP 200; **không** request nào trả 422 「表示期間は31日以内で指定してください。」; không màn trắng, không spinner treo.<br>- Tuần / tháng cuối hiển thị khung tới đúng ngày thứ 180; ngày sau ngày thứ 180 không có khung đặt được.<br>- B4, B7: tới được màn xác nhận ở cả 2 chế độ. |  | Lấp G1 / G4 · regression — dẫn từ TC-SLN-308 / 347 / 434 / 435 / 436 · thay TC-FUNC001-01 ở §7 lượt B (bỏ "chế độ danh sách" — §4 C1), không push bản cũ · B6 đi qua lịch tháng (`initDataBooking`, có guard mới) · Không bấm 「予約確定」 nên chạy được trên bot test prd · Đánh giá spec: Spec không ghi (API khung giờ trang khách không có trong spec-features) · Evidence: HAR Network 2 chế độ + screenshot tuần / tháng cuối |
| TC-DEPLOYLIVE001-01 | UI | DEPLOY-LIVE-001 | Salon booking サロン予約 (trang khách): khách đang mở trang đặt lịch lúc release | Normal | auto | staging, prd | line-friend | Khách mở trang đặt lịch trước release (JS bản cũ) rồi thao tác tiếp sau release: không lỗi 422, đặt được lịch | - Bot test (staging, và bot test production) có lịch salon 「QA45229B_SalonLive」 đang bật, 2 nhân viên có ca mọi ngày trong 60 ngày tới, menu M1 (60 phút).<br>- Khách QA45229B_F01 (gọi tắt F01) là bạn bè của bot, có link đặt lịch.<br>- Biết giờ deploy bản sprint #45229. | 1. Trước deploy 10 phút: F01 mở trang đặt lịch, chọn M1 + 指名なし, để ở tuần hiện tại.<br>2. Chờ deploy xong, không tải lại trang.<br>3. F01 bấm tuần kế tiếp 3 lần.<br>4. Nếu lịch cho xem theo tháng: chuyển sang tháng, bấm tháng kế tiếp 1 lần.<br>5. F01 chọn 1 khung, nhập thông tin, bấm 「予約確定」.<br>6. F01 tải lại trang, lặp bước 3–4. | Thời điểm mở trang: 10 phút trước deploy. | - B3, B4: khung giờ hiển thị; không request nào trả 422 「表示期間は31日以内で指定してください。」 hay 500; nếu bị chặn thì trang báo lỗi rõ và tải lại được, không màn trắng.<br>- B5: đặt thành công, đơn hiện ở 予約管理.<br>- B6: hiển thị như B3–B4 bằng JS bản mới. | | Lấp G3 / Q2 · chỉ staging+prd vì cần deploy thật · `public/js/calendar_salon/booking.js` (+31) đổi cùng đợt — Dev chưa xác nhận có đổi cách gửi khoảng ngày · Đánh giá spec: Spec không ghi · Evidence: HAR trước / sau deploy + mã đơn |
| TC-ENV003-01 | Data | ENV-003 | Salon booking サロン予約 (trang khách + API khung giờ): giám sát exception sau release trên production | Normal | manual | prd | web | 7 ngày sau release không còn exception hết thời gian / hết bộ nhớ ở luồng khung giờ salon | - Bản sprint #45229 đã release production.<br>- Có quyền xem room Chatwork SNSLineException và dashboard check-exception.<br>- Mốc trước release: #41717 (`Maximum execution time … Collection`, server s.lmes.jp, bot 153361) 1 lần ngày 2026-09-28; #41529 (`Allowed memory size … JsonResponse`, server step.lme.jp, bot 52318) 10 lần ngày 2026-09-25. | 1. Ghi giờ release.<br>2. Mỗi ngày trong 7 ngày sau release, lọc dashboard check-exception theo signature `Maximum execution time … Collection`.<br>3. Cùng ngày, lọc theo signature `Allowed memory size … JsonResponse`.<br>4. Với mỗi exception tìm được, ghi URL request, bot_id, thời điểm. | Thời gian theo dõi: 7 ngày.<br>2 signature của #41717, #41529. | - Không có exception nào của 2 signature ở request trang đặt lịch salon / API khung giờ / đặt lịch trong 7 ngày.<br>- Nếu có: danh sách URL + bot_id + thời điểm, mở lại #41717 / #41529 kèm dữ liệu này. | | Lấp G2 · chỉ prd vì exception chỉ xảy ra với dữ liệu khách hàng thật · manual vì chỉ chạy trên production · Surface web vì phán quyết đọc trên dashboard trình duyệt · Đánh giá spec: không áp dụng · Evidence: ảnh dashboard 7 ngày |

**Không đề xuất TC mới (có lý do):**
- **G2**: 3 TC đã có — chuẩn bị seed, sửa expected (§5 I2, I3) rồi chạy lại; xác nhận production bằng TC-ENV003-01.
- **Q3** (`REG-SPEC-001`) · **Q4** (`FUNC-001`) · **Q5** (`PERF-LARGE-001`): sửa 3 TC hiện có theo §5 I2 / I3, không cần TC mới.
- **Q6** (`REG-SHARED-001` · `SYNC-APP-001`): chưa đề xuất TC app quản trị khi Dev chưa xác nhận app có gọi API khung giờ (§5 I4) — đặt sẵn slot B4 ở §9.2.
- Đổi mã quan điểm (không cần TC mới): NEW-701 → `FUNC-001` · NEW-703 → `FUNC-004`.

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/salon-booking/web/api-spec.md` — chưa có API khung giờ trang khách | Thêm `GET /ajax/mobile/calendar-salon/get-list-time-booking`: khoảng hiển thị ≤ 31 ngày (ghi rõ cách đếm) → 422 「表示期間は31日以内で指定してください。」; calendarId không tồn tại → 404 「カレンダーが見つかりません。」; thiếu / sai tham số → 422 「パラメータが不正です。」; ý nghĩa `timeShowWeek` | Quy tắc mới từ fix bug Studio #45409 / #45410 — spec chưa có · C1 | `Dev / Leader` |
| 2 | `kho-tcs/fa020-…` nhóm 35 / 45 (hoặc spec `salon-booking/ui/ui-spec.md` trang khách) | Ghi rõ các chế độ hiển thị của màn chọn slot (tuần / tháng — có "danh sách" không) và cơ chế tự nhảy tuần / tháng có chỗ | C1 `CONF-KHO` ở §4 | `Dev` |

---

## 9. Main cases (`/pick-maincase`)

<!-- generated: /pick-maincase 2026-11-19 · pool: Studio task #560 (3 TC lọc REQ-X-41717-*) + §7 report này (4 TC chưa trên tool) -->

### 9.0 Tóm tắt

| Mục | Giá trị |
|---|---|
| Loại task | Fix bug — exception production do AI phát hiện (timeout 500 giây ở luồng khung giờ salon). Không có commit riêng; thay đổi chạm luồng đến từ T16 #41345 + guard #45409 / #45410 → main case = chứng minh hết timeout trên dữ liệu lớn + quy tắc 31 ngày không chặn nhầm khách thật |
| Bộ TC | 7 TC (Studio: 3 · §7 chưa trên tool: 4) |
| Main case | 5 TC (71% bộ TC) · Bắt buộc sau release: 2 |
| Slot chưa có main case | 1 (B4 — có điều kiện) |
| Input thiếu | Dev không viết đánh giá ảnh hưởng cho #41717 · nơi gọi API khung giờ chưa có (§5 I4) |

Tỉ lệ 71% vượt mức gợi ý ~20% vì pool của 1 ticket chỉ có 7 TC; đã rà lại, mỗi case giữ slot riêng.

### 9.1 Main cases (5)

| # | TC ID | Slot | Tên case | Surface | Môi trường chạy | Sau release | Tiêu chí đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| 1 | NEW-701 | B1 | Lịch salon dữ liệu lớn: khách chọn khung tuần, bấm 「予約確定」 — đơn được lưu, không hết thời gian chạy | line-friend, web | local · đề xuất: dev, local, staging (seed dữ liệu lớn) | Không — seed dữ liệu lớn | C1 BUG #41717 · REQ-X-41717-01 · `order()` gọi `getListTimeLineBooking` · C2 `FUNC-001` Cao · C3 luồng đặt lịch thật · C4 đơn ở 予約管理 + DB | ⚠️ skip `needs-prep` — sửa theo §9.4 trước khi chạy |
| 2 | NEW-702 | B2a | Lịch salon dữ liệu lớn dạng tháng: chuyển 3 tháng liên tiếp đều tải xong, khung đúng | line-friend | local · đề xuất: dev, local, staging (seed dữ liệu lớn) | Không — seed dữ liệu lớn | C1 trigger thứ 2 của cùng root cause (`initDataBooking` ⇒ `showTimeBookingMonth` ⇒ `getListTimeLineBooking`) · guard `initDataBooking` trong diff · C3 cài hiển thị theo tháng (TC-SLN-347) | ⚠️ skip `needs-prep` |
| 3 | TC-FUNC004-01 (chưa trên tool) | B2b | API khung giờ: khoảng 1 và 31 ngày trả khung; 32 ngày bị 422 「表示期間は31日以内で指定してください。」 | api | dev, local, prd, staging | Không — gửi request tay; luồng khách thật trên prd do #4 kiểm | C1 trigger thứ 3 (khoảng ngày dài — NEW-703 / #45409) nay chặn bằng quy tắc 31 ngày · C2 `FUNC-004` Cao · được phép + bị chặn + sát ngưỡng | Thay NEW-703 trong tập main case (365 ngày ⇒ 422 nằm trong B3 / B4 của TC này) |
| 4 | TC-FUNC001-02 (chưa trên tool) | B3, B4 (lịch tháng) | Lịch nhận đặt 180 ngày, 14 ngày đầu không có ca: tuần + tháng đi hết phạm vi, tự nhảy tới tuần có ca — không request nào bị 422 | line-friend, web | dev, local, prd, staging | Bắt buộc — guard 31 ngày chặn nhầm thì khách không đặt được lịch | C1 hành vi siết lại (G1) · nhánh "khung trống / kín phải giống trước" · C2 `FUNC-001` Cao · C3 2 chế độ hiển thị thật · C4 tới màn xác nhận | Không bấm 「予約確定」 → chạy được trên bot test prd |
| 5 | TC-ENV003-01 (chưa trên tool) | B6 | 7 ngày sau release không còn exception hết thời gian / hết bộ nhớ ở luồng khung giờ salon | web | prd | Bắt buộc — exception chỉ thấy trên prd | C1 BUG #41717 (+ #41529) · C5 đúng hạ tầng + dữ liệu thật bot 153361 | `manual` vì chỉ chạy trên production |

**TC trong pool không chọn (2):**
- NEW-703: khoảng 365 ngày ⇒ nay 422 theo cùng quy tắc với TC-FUNC004-01 B3 / B4; expected đang sai (§5 I2).
- TC-DEPLOYLIVE001-01: rủi ro chỉ có thật nếu `booking.js` cũ gửi khoảng > 31 ngày — chờ Dev trả lời §5 I4 (4); Dev xác nhận có đổi cách gửi khoảng ngày thì đưa vào main case, `Sau release = Bắt buộc`.

### 9.2 Slot chưa có main case (1)

| # | Slot | Case cần có | Surface | Expected cốt lõi | Môi trường |
|---|---|---|---|---|---|
| 1 | B4 (có điều kiện — app) | Chỉ áp khi Dev xác nhận app quản trị `Mobile/CalendarSalonController` gọi `getListTimeLineBooking` / API khung giờ (§5 I4). Đăng nhập app LME bằng admin (主管理者) bot test, mở lịch salon 「QA45229_41717_Salon180」 (nhận đặt trước 180 ngày, 2 nhân viên S1 / S2 ca 10:00–18:00 mọi ngày, menu M1 60 phút). Tạo booking thủ công cho khách QA45229_F01 (gọi tắt F01) ở ngày thứ 60, M1 + S1, khung 10:00 | mobile-app, web | Booking lưu thành công, hiện ở 予約管理 trên web đúng ngày thứ 60 / 10:00 / S1; app không báo lỗi 422 「表示期間は31日以内で指定してください。」 hay lỗi hệ thống | dev, local, prd, staging |

### 9.3 Slot không áp dụng

| Slot | Lý do |
|---|---|
| B5 | Timeout chỉ xảy ra ở bước đọc; không có dữ liệu đã lưu bị sai cần kiểm hay khôi phục |

### 9.4 TC cần sửa trước khi chạy

| TC ID | Vấn đề | Cần sửa |
|---|---|---|
| NEW-701 | Skip `needs-prep`; expected không có ngưỡng; chưa kiểm "không 422"; mã `TOOL-KNOW-002` | Seed theo số dòng thật của bot 153361 (§5 I3); thêm ngưỡng thời gian Leader chốt; thêm "không request khung giờ nào trả 422"; đổi mã sang `FUNC-001` |
| NEW-702 | Skip `needs-prep`; expected không có ngưỡng; chưa kiểm "không 422" | Như NEW-701 |
| NEW-703 (không chọn) | Expected 2 nhánh; tiêu đề gọi `timeShowWeek=1` là "dạng danh sách" (C1) | Expected = 422 + message; gộp NEW-763; sửa tiêu đề; đổi mã sang `FUNC-004` |
| TC-FUNC004-01 · TC-FUNC001-02 · TC-ENV003-01 | Chưa có trên tool | `/sync-review-tc` sau khi Leader duyệt. **Không push TC-FUNC001-01 của §7 lượt B** (đã thay bằng TC-FUNC001-02) |
