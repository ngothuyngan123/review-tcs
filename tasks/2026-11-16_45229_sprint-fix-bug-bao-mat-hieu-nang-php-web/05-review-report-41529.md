# 05 — Review Report

> Draft cho Leader verify. **Sprint #45229 · T15 · sub-task #41529** — `Allowed memory size of 1073741824 bytes exhausted` (JsonResponse.php, cấp thêm 561 MB) trên `step.lme.jp`, 10 lần ngày 2026-09-25 03:14 → 03:20 UTC (user admin 177888, bot 52318), review 2026-11-19. Bản này thay phần #41529 của report lượt B (`45229-B_t15-exception-salon-du-lieu-lon/05-review-report.md`). Cùng luồng với #41717 → dùng lại TC đã đề xuất ở [05-review-report-41717.md](05-review-report-41717.md). Main case nằm ở §9.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) Studio task #560` (task cha #45229, fetch 2026-11-19, 1287 TC) — lọc TC gắn `REQ-X-41529-*` |
| Tổng số TC review | 3 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev **không** viết đánh giá cho #41529 (không commit riêng). Dùng 4 mục từ requirement Studio `REQ-X-41529` (risk **High**) / `-01` / `-02`: BUG hết bộ nhớ khi trả JSON lớn · khoảng ngày 10 năm không làm hết bộ nhớ · request tuần như FE trên dữ liệu lớn trả JSON đúng, kích thước hợp lý · calendarId sai ⇒ 4xx sạch, không ghi rác (#45410) | `4/4 mục có TC` — **CHƯA ĐỦ** (3 RISK) |
| **(b) diff code** — 4 điểm: guard khoảng ngày ≤ 31 → 422 (`CalendarSalonListTimeBookingGuardTest` +158) · validate calendarId / ngày → 404 / 422, không tạo `calendar_salon_setting_time_free` (#45410) · hành vi siết lại (> 31 ngày trước trả dữ liệu, nay 422) · endpoint thật của exception (symptom-only) | `3/4 điểm có TC` — **CHƯA ĐỦ** (1 GAP · 2 RISK) |

**Kết luận**: `2/8 vùng ảnh hưởng đủ TC · 1 GAP · 5 RISK`.

Loại khỏi mẫu số: truy vấn khung giờ tuần viết lại (T16 #41345) · `public/js/calendar_salon/booking.js` (+31) và rủi ro deploy (đã xét ở report #41717 — G3) · Google Calendar / Sheet / phân bổ nhân viên (T9 / T10 / T16).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | BUG #41529 hết bộ nhớ + request tuần như FE trên dữ liệu lớn + khoảng 10 năm | dev-impact | NEW-762 · NEW-763 — **cả 2 skip** (`needs-prep`, run #7782 ngày 13/11) | **RISK** — 0 TC Đạt trên dữ liệu lớn → chưa có bằng chứng nào hết tràn bộ nhớ, dù requirement risk **High**; seed (30 nhân viên × 90 ngày, ≈ 20.000 đơn) không lấy từ bot 52318; chưa TC nào xác nhận sau release signature không còn | `[BLOCKER]` |
| G2 | Quy tắc mới **khoảng hiển thị ≤ 31 ngày → 422 「表示期間は31日以内で指定してください。」** (#45409) | diff code | NEW-763 (skip, expected cũ "4xx **hoặc** 200") | **GAP** — biên 31 / 32 ngày: 0 TC; chưa TC nào chứng minh khách dùng bình thường (tuần / tháng tới 180 ngày, tự nhảy tuần có ca) không bị 422 | `[BLOCKER]` |
| G3 | **Endpoint thật của exception** — symptom-only | diff code | NEW-762 · NEW-763 · NEW-764 (đều thử 1 giả thuyết: API khung giờ **trang khách** public) | **RISK** — exception có gắn **user admin 177888** → request gây lỗi có thể đến từ **màn quản trị đã đăng nhập** (lịch ngày / tuần / tháng, danh sách booking, app quản trị), không phải trang khách. AI chỉ "nghi" `getListTimeLineBooking`, Dev chưa xác nhận. Diff có thay đổi hiệu năng màn quản trị (`Basic/CalendarSalonController` +112, `CalendarSalonDayViewPerformanceTest` +199 — nhóm T16) nhưng không gắn với #41529. Cần Dev tra URL request trong log trước khi đẻ TC — **không tự đoán** (§5 I5) | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `6 quan điểm Trigger khớp task · 6 chưa cover đủ`.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-004` | Cao | **GAP** — giới hạn 31 ngày: 0 TC mang mã; Abnormal chỉ có NEW-763 (mã `TOOL-KNOW-002`, skip); Normal + Boundary 0 TC (RULE-01) → TC-FUNC004-01 (report #41717) | `[BLOCKER]` |
| Q2 | `FUNC-003` | Trung bình → **Cao** (field ngày giờ) | **RISK** — validate định dạng ngày: Normal (NEW-764 B1 đối chứng) + Abnormal (NEW-764 B4 `start_date = abc`) có nhưng mang mã `TOOL-ERRHYG-001`; **thiếu Boundary** (ngày không tồn tại 30/02, tháng 13 — RULE-01) → TC-FUNC003-01 | `[MAJOR]` |
| Q3 | `REG-SPEC-001` | Cao | **RISK** — quy tắc 31 ngày chốt sau khi NEW-762 / 763 đã viết; NEW-763 expected còn 2 nhánh, NEW-762 chưa kiểm "không bị 422" (§5 I2) | `[MAJOR]` |
| Q4 | `PERF-LARGE-001` | Trung bình | **RISK** — NEW-762 skip; expected kích thước "vài trăm KB trở xuống (chỉ tham khảo)" không đo được; seed không dựa trên dữ liệu thật (§5 I4) | `[MAJOR]` |
| Q5 | `REG-SHARED-001` · `SYNC-APP-001` | Cao · Trung bình (→ Cao, đặt lịch là flow critical) | **RISK** — chưa có danh sách nơi gọi API khung giờ / `getListTimeLineBooking` (web tuần · tháng · `order()` · app quản trị `Mobile/CalendarSalonController` +321) — gắn với G3 | `[MAJOR]` |

**Đã loại khỏi phạm vi (có căn cứ):**
- `LIFF-ENTRY-001`: guard 31 ngày + validate calendarId nằm ở API, chạy sau khi trang đã mở; điểm vào không đổi.
- Ma trận option 受付上限 / シフトの合算 / 指名: độ đúng khung thuộc T16 #41345; guard chặn trước bước tính khung.
- `DATA-DB-001`: luồng chỉ đọc; việc **không** tạo `calendar_salon_setting_time_free` khi calendarId sai đã kiểm ở NEW-764.
- `DEPLOY-LIVE-001`: xét chung ở report #41717 (TC-DEPLOYLIVE001-01), cùng endpoint + cùng `booking.js`.
- `ENV-003` / RULE-08: không chạm media / domain / job nền / thanh toán; xác nhận production đi theo G1 (TC-ENV003-01).

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-703 (#41717) | NEW-763 → **gộp** vào NEW-703 | DUP-EXACT (sau khi sửa expected theo quy tắc 31 ngày) | mã (cùng kiểm khoảng ngày bất thường) · Abnormal · gọi API khung giờ với khoảng > 31 ngày (365 ngày / 10 năm) · cùng lịch seed → cùng kết quả 422 | `[MINOR]` |

- **Gate đã chạy**: NEW-763 là TC duy nhất gắn `REQ-X-41529-01` → **gộp, không xoá**: chép dữ liệu "10 năm" thành bước thứ 2 của NEW-703, gắn thêm `REQ-X-41529-01` vào NEW-703. (Giống kết luận report lượt B + report #41717.)
- Đã rà 3 TC + NEW-337 (#38931) + NEW-701 / 702 / 703 (#41717): ngoài DUP-1 không phát hiện trùng. NEW-762 (khung tuần dữ liệu lớn qua API) khác NEW-337 (khung tuần trên màn) ở cách kiểm chứng.

---

## 4. Mâu thuẫn trong TCs

Đã rà 3 TC × `spec-features/admin/salon-booking/` (`feature-spec.md`, `web/api-spec.md` — **không mô tả** API khung giờ trang khách) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 35 · 45 · 49 · 51 · 53) — không phát hiện mâu thuẫn. Quy tắc 31 ngày + mã lỗi calendarId / ngày sai chưa có trong spec để đối chiếu (§8 #1). (Mâu thuẫn "`timeShowWeek=1` = dạng danh sách" chỉ nằm ở NEW-703 — đã ghi ở report #41717 C1; 3 TC của #41529 không dính.)

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Nguồn TC | **1/3 Đạt (33%)**. NEW-762, NEW-763 `skip` trạng thái `needs-prep` (chưa dựng dữ liệu lớn) từ 13/11. NEW-764 Đạt nhưng chỉ ở `local`, scope `all` chưa chạy dev / staging / prd. TC duy nhất Đạt kiểm tham số sai, **không** kiểm bộ nhớ | Chuẩn bị seed rồi chạy lại NEW-762 / 763 (sau khi sửa I2); chạy NEW-764 thêm dev + staging |
| I2 | `[MAJOR]` | NEW-763 · NEW-762 | NEW-763 expected "4xx **hoặc** 200 trong giới hạn" trong khi quy tắc đã chốt 422 「表示期間は31日以内で指定してください。」. NEW-762 chưa có dòng "không bị 422" | NEW-763: gộp vào NEW-703 (DUP-1) với expected 422 + message. NEW-762: thêm expected "HTTP 200, không phải 422 表示期間…" |
| I3 | `[MAJOR]` | NEW-764 | RULE-13: expected ghi chung "HTTP 4xx (404/422)". Ghi chú còn câu lỗi thời "Dự kiến CHƯA ĐẠT ở B2/B3 … lỗi 500" (đã sửa ở #45410, TC đang Đạt) | Expected theo #45410: B2 `calendarId = 999999999` ⇒ **404** 「カレンダーが見つかりません。」 · B3 thiếu calendarId ⇒ **422** 「パラメータが不正です。」 · B4 `start_date = abc` ⇒ **422** 「パラメータが不正です。」. Bỏ câu "Dự kiến CHƯA ĐẠT…". Đổi mã sang `FUNC-003` |
| I4 | `[MAJOR]` | NEW-762 | Expected không đo được: "kích thước ở mức vài trăm KB trở xuống … chỉ tham khảo". Seed không dựa trên dữ liệu thật của bot gặp lỗi | Leader chốt ngưỡng kích thước body + thời gian; Dev / DBA cung cấp số dòng `calendar_salon_time_booking` + `calendar_salon_line_booking` của bot 52318 → seed ≥ mức đó |
| I5 | `[MAJOR]` | Input thiếu từ Dev | (1) **URL request** của 10 exception #41529 (2026-09-25 03:14 → 03:20 UTC, `step.lme.jp`, user admin 177888, bot 52318) — màn quản trị hay trang khách? (G3) (2) #41529 coi là xong nhờ T16 #41345 + guard #45409, hay còn phải sửa? (3) danh sách nơi gọi API khung giờ / `getListTimeLineBooking`, gồm app quản trị (Q5) | Hỏi Dev; Dev chỉ ra endpoint khác trang khách thì thêm TC cho endpoint đó (slot B2b ở §9.2) |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 3 TC — không có TC nào ngoài phạm vi task. (NEW-764 kiểm validate calendarId — thuộc guard API trong diff, fix bug Studio #45410 phát sinh khi test #41529.)

---

## 7. TCs đề xuất bổ sung (1)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 29 · 35 · 45 · 49 · 51 · 53) |
| Vùng regression phát hiện từ kho | TC-SLN-308 / 347 / 434 / 435 / 436 — đã dùng ở TC-FUNC001-02 (report #41717) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC đã đề xuất (không viết mới) | **G1** → TC-ENV003-01 (giám sát cả 2 signature #41717 + #41529 trên prd) · **G2** → TC-FUNC004-01 (biên 1 / 31 / 32 ngày) + TC-FUNC001-02 (tuần / tháng tới 180 ngày không bị 422) — cả 3 ở §7 [05-review-report-41717.md](05-review-report-41717.md), **push từ report đó** |
| Căn cứ TC regression `R<x>` | Không có TC R |
| Xác nhận chống trùng | Đã đối chiếu 3 TC ở BƯỚC 0 + NEW-701 / 702 / 703 + 4 TC §7 report #41717 + kho FA-020 — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC003-01 | API | FUNC-003 | Salon booking サロン予約 (API khung giờ get-list-time-booking): Biên định dạng ngày start_date / end_date | Boundary | auto | dev, local, prd, staging | api | Ngày hợp lệ cuối tháng 2 trả khung giờ; ngày không tồn tại (30/02, tháng 13) bị từ chối 422 「パラメータが不正です。」, không bị tự quy sang ngày khác | - Bot test có lịch salon 「QA45229_41529_SalonDate」 đang bật, nhận đặt trước 180 ngày.<br>- 2 nhân viên S1 / S2 có ca 10:00–18:00 mọi ngày từ hôm nay tới 31/03/2027; menu M1 (60 phút).<br>- Khách QA45229_F01 (gọi tắt F01) là bạn bè của bot, có link đặt lịch.<br>- F01 mở trang đặt lịch, chọn M1 + 指名なし; tester lấy request `GET /ajax/mobile/calendar-salon/get-list-time-booking` của tuần đầu ở DevTools (Network) làm mẫu. | 1. Gửi lại request mẫu với start_date = 2027-02-22, end_date = 2027-02-28.<br>2. Gửi lại với start_date = 2027-02-24, end_date = 2027-02-30.<br>3. Gửi lại với start_date = 2027-02-30, end_date = 2027-03-06.<br>4. Gửi lại với start_date = 2027-13-01, end_date = 2027-13-07. | Các tham số khác (calendarId, courseId, line_id, timeShowWeek …) giữ nguyên như request mẫu | - B1: HTTP 200, JSON có khung giờ đủ 7 ngày 22/02 … 28/02/2027.<br>- B2, B3, B4: HTTP 422, message 「パラメータが不正です。」; không trả khung giờ của ngày khác (không tự quy 30/02 thành 02/03).<br>- Không request nào trả 500. | | Lấp Q2 · Đánh giá spec: Spec không ghi — quy tắc "ngày sai ⇒ 422 「パラメータが不正です。」" từ fix bug Studio #45410; ngày không tồn tại có tính là "ngày sai" không thì Dev xác nhận trước khi chạy · Evidence: request + response 4 lần gọi |

**Không đề xuất TC mới (có lý do):**
- **G3** (endpoint thật — symptom-only): chờ Dev chỉ ra URL request trong log (§5 I5) — không tự đoán giả thuyết thứ 2. TC-ENV003-01 là bằng chứng production tạm thời.
- **Q3** (`REG-SPEC-001`) · **Q4** (`PERF-LARGE-001`): sửa NEW-762 / 763 theo §5 I2 / I4.
- **Q5** (`REG-SHARED-001` · `SYNC-APP-001`): chờ Dev xác nhận nơi gọi (§5 I5) — đặt sẵn slot B4 ở §9.2.
- Đổi mã quan điểm (không cần TC mới): NEW-763 → `FUNC-004` (gộp vào NEW-703) · NEW-764 → `FUNC-003`.

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/salon-booking/web/api-spec.md` — chưa có API khung giờ trang khách | Như [report #41717 §8 #1](05-review-report-41717.md) (khoảng ≤ 31 ngày → 422; calendarId không tồn tại → 404 「カレンダーが見つかりません。」; thiếu / sai tham số → 422 「パラメータが不正です。」), **thêm**: ngày không tồn tại (30/02, tháng 13) xử lý thế nào | Quy tắc mới từ fix bug Studio #45409 / #45410 — spec chưa có · TC-FUNC003-01 | `Dev / Leader` |

---

## 9. Main cases (`/pick-maincase`)

<!-- generated: /pick-maincase 2026-11-19 · pool: Studio task #560 (3 TC lọc REQ-X-41529-*) + §7 report này (1 TC) + §7 report #41717 (3 TC cover #41529 — chưa trên tool) -->

### 9.0 Tóm tắt

| Mục | Giá trị |
|---|---|
| Loại task | Fix bug — exception production do AI phát hiện (hết bộ nhớ khi trả JSON lớn). Không có commit riêng; thay đổi chạm luồng đến từ T16 #41345 + guard #45409 / #45410 → main case = chứng minh API khung giờ không tràn bộ nhớ trên dữ liệu lớn + quy tắc 31 ngày không chặn nhầm khách thật |
| Bộ TC | 7 TC (Studio: 3 · §7 report này: 1 · §7 report #41717: 3) |
| Main case | 4 TC (57% bộ TC) · Bắt buộc sau release: 2 |
| Slot chưa có main case | 2 (B2b, B4 — có điều kiện) |
| Input thiếu | Dev không viết đánh giá ảnh hưởng cho #41529 · URL request của exception chưa xác định (§5 I5) |

3 / 4 main case dùng chung với #41717 (TC-FUNC004-01 · TC-FUNC001-02 · TC-ENV003-01) — ở mức sprint chỉ chạy 1 lần.

### 9.1 Main cases (4)

| # | TC ID | Slot | Tên case | Surface | Môi trường chạy | Sau release | Tiêu chí đạt | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| 1 | NEW-762 | B1 | API khung giờ tuần (đúng request FE) trên lịch dữ liệu lớn: JSON trả đủ, khớp khung hiển thị, kích thước hợp lý | api, line-friend | local · đề xuất: dev, local, staging (seed dữ liệu lớn) | Không — seed dữ liệu lớn | C1 BUG #41529 · REQ-X-41529-02 · C4 so JSON với khung trên trang · C3 đúng request FE gửi | ⚠️ skip `needs-prep` — sửa theo §9.4 |
| 2 | TC-FUNC004-01 (chưa trên tool — §7 report #41717) | B2 | API khung giờ: khoảng 1 và 31 ngày trả khung; 32 ngày bị 422 「表示期間は31日以内で指定してください。」 | api | dev, local, prd, staging | Không — gửi request tay; luồng khách thật trên prd do #3 kiểm | C1 trigger thứ 2 của cùng root cause (khoảng ngày cực dài — REQ-X-41529-01) nay chặn bằng quy tắc 31 ngày · C2 `FUNC-004` Cao · được phép + bị chặn + sát ngưỡng | Thay NEW-763 (10 năm ⇒ 422 cùng quy tắc) · dùng chung #41717 |
| 3 | TC-FUNC001-02 (chưa trên tool — §7 report #41717) | B3 | Lịch nhận đặt 180 ngày, 14 ngày đầu không có ca: tuần + tháng đi hết phạm vi, tự nhảy tới tuần có ca — không request nào bị 422 | line-friend, web | dev, local, prd, staging | Bắt buộc — guard 31 ngày chặn nhầm thì khách không đặt được lịch | C1 hành vi siết lại (G2) · C2 `FUNC-001` Cao · C3 2 chế độ hiển thị thật | dùng chung #41717 |
| 4 | TC-ENV003-01 (chưa trên tool — §7 report #41717) | B6 | 7 ngày sau release không còn exception hết thời gian / hết bộ nhớ ở luồng khung giờ salon | web | prd | Bắt buộc — exception chỉ thấy trên prd | C1 BUG #41529 (signature `Allowed memory size … JsonResponse`, `step.lme.jp`, bot 52318) · C5 đúng hạ tầng + dữ liệu thật | `manual` vì chỉ chạy trên production · dùng chung #41717 |

**TC trong pool không chọn (3):**
- NEW-763: khoảng 10 năm ⇒ nay 422 theo cùng quy tắc với TC-FUNC004-01; gộp vào NEW-703 (DUP-1).
- NEW-764: validate calendarId / ngày sai (#45410) — validate từng tham số thuộc danh sách loại trừ; đã Đạt local, chạy ở vòng regression.
- TC-FUNC003-01: biên định dạng ngày — biên phụ, chạy ở vòng regression.

### 9.2 Slot chưa có main case (2)

| # | Slot | Case cần có | Surface | Expected cốt lõi | Môi trường |
|---|---|---|---|---|---|
| 1 | B2b (có điều kiện — endpoint thật) | Chỉ áp khi Dev chỉ ra URL request của exception #41529 **khác** API khung giờ trang khách (§5 I5). Đăng nhập admin (主管理者) bot test, dựng lịch salon 「QA45229_41529_SalonBig」 với số nhân viên × ngày ca × số đơn ≥ số dòng thật của bot 52318 (Dev / DBA cung cấp), mở đúng màn / gọi đúng endpoint Dev chỉ ra với tham số giống request lúc lỗi; ghi bộ nhớ tiến trình PHP, kích thước response, thời gian | web | HTTP 200, màn hiển thị xong; log không có `Allowed memory size of … bytes exhausted`; bộ nhớ tiến trình dưới `memory_limit` production | dev, local, staging (seed dữ liệu lớn) |
| 2 | B4 (có điều kiện — app) | Chỉ áp khi Dev xác nhận app quản trị `Mobile/CalendarSalonController` gọi API khung giờ / `getListTimeLineBooking` (§5 I5). Đăng nhập app LME bằng admin (主管理者) bot test, mở lịch salon 「QA45229_41717_Salon180」 (nhận đặt trước 180 ngày, 2 nhân viên S1 / S2 ca 10:00–18:00 mọi ngày, menu M1 60 phút), tạo booking thủ công cho khách QA45229_F01 (gọi tắt F01) ở ngày thứ 60, M1 + S1, khung 10:00 | mobile-app, web | Booking lưu thành công, hiện ở 予約管理 trên web đúng ngày thứ 60 / 10:00 / S1; app không báo lỗi 422 「表示期間は31日以内で指定してください。」 hay lỗi hệ thống | dev, local, prd, staging |

### 9.3 Slot không áp dụng

| Slot | Lý do |
|---|---|
| B3 (calendarId) | Nhánh "calendarId đúng vẫn trả khung" đã nằm trong B1 của NEW-762 / TC-FUNC004-01 |
| B5 | Hết bộ nhớ chỉ xảy ra ở bước đọc + trả JSON; không có dữ liệu đã lưu bị sai cần kiểm hay khôi phục |

### 9.4 TC cần sửa trước khi chạy

| TC ID | Vấn đề | Cần sửa |
|---|---|---|
| NEW-762 | Skip `needs-prep`; expected kích thước chỉ "tham khảo"; chưa kiểm "không 422" | Seed theo số dòng thật của bot 52318 (§5 I4); thêm ngưỡng kích thước / thời gian Leader chốt; thêm "HTTP 200, không phải 422 表示期間…" |
| NEW-763 (không chọn) | Expected 2 nhánh | Gộp vào NEW-703 với expected 422 + message (DUP-1) |
| NEW-764 (không chọn) | Expected mã HTTP chung (RULE-13); ghi chú lỗi thời | Sửa theo §5 I3 |
| TC-FUNC004-01 · TC-FUNC001-02 · TC-ENV003-01 | Chưa có trên tool | Push từ [05-review-report-41717.md](05-review-report-41717.md) (`/sync-review-tc`) — không push lại từ report này |
| TC-FUNC003-01 | Chưa có trên tool | `/sync-review-tc` sau khi Leader duyệt; Dev xác nhận ngày không tồn tại thuộc "ngày sai" |
