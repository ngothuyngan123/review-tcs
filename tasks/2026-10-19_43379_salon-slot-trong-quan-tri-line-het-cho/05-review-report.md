# 05 — Review Report

> Draft cho Leader verify. Review trên bộ TC v7 (47 TC, fetch 2026-10-21).
> Lịch sử: vòng đầu review trên 28 TC (v6); bộ v7 đã lấp phần lớn GAP vòng đầu (màn quản trị, thanh toán, option 3, app mobile, gộp ca 1.2, đồng thời). File này là bản gộp cuối cùng.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #470 (ticket 43379, round 1, branch `ai_studio_fixbug_43379` @`09f97bee`, run cuối 2026-10-20) |
| Tổng số TC review | 47 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` mục 4 | 16/18 mục có TC — **CHƯA ĐỦ** (thiếu `前後の空き時間`; T4 hiệu năng chỉ có TC `skip`) |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` v7 (9 file, REQ-001…013) | 11/13 REQ có TC chạy thật — **CHƯA ĐỦ** (REQ-002 thiếu nhánh `前後の空き時間`; REQ-010 hiệu năng `skip`; REQ-001/005/011 có TC nhưng đang **fail** → RISK) |

**Kết luận**: 9/13 vùng đủ TC đạt · 1 GAP · 4 RISK (so với round 1: 5 GAP → đa số đã lấp bằng NEW-28…NEW-47)

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Gán thử đơn 指定なし cho NV ngoài nhóm × `前後の空き時間` (nghỉ trước/sau) — Studio `dev_impact` liệt kê "nghỉ trước/sau" trong nhóm "rủi ro cao nhất" | diff code · dev-impact | không có — 47/47 TC đều `前後の空き時間` không cài | GAP — 4/5 điều kiện ứng viên ngoài nhóm đã có TC (suất NEW-16, ca NEW-25, Google NEW-26, filter NEW-10); thiếu nghỉ trước/sau | [MAJOR] |
| R1 | REQ-001/004/007 — gộp ca 1.2 giờ thường | diff code | NEW-28 (**fail**, #43561) | RISK — TC đang fail: khung 17:30 qua biên ca 18:00 bị ẩn (bug thật, xem §5 I2) | [BLOCKER] |
| R2 | REQ-011/013 — quản trị xem ngày kiểu 上限を設定する | diff code | NEW-33 (**fail**, chưa ticket) | RISK — TC fail chưa triage: hàng 指定なし 17:30 báo hết chỗ dù course B còn suất (§5 I1) | [BLOCKER] |
| R3 | REQ-001/003/011 — đặt lịch có thanh toán | diff code · dev-impact | NEW-29 (**fail**, #43571) | RISK — fail, run note "thiếu merchant TEST" → chưa rõ lỗi sản phẩm hay thiếu tài nguyên test (§5 I3) | [MAJOR] |
| R4 | REQ-010 / T4 — hiệu năng API tuần/tháng LINE + màn quản trị ngày | diff code · dev-impact | NEW-1, NEW-43 (đều `skip`) | RISK — chưa chạy (thiếu baseline release + ngưỡng chưa chốt) | [MAJOR] |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 17 quan điểm Trigger khớp task · 6 chưa cover đủ

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `JOB-001` | Cao | RISK — 7 TC job (NEW-2/3/4/5/35/42/46) gắn mã lạ `JOB-002` / `TOOL-NEGCTRL-001` → không tính cover. Nội dung đã đủ (friend+admin, random+ưu tiên, limit 1, Risk2) → chỉ cần đổi mã trên Studio, không đẻ TC | [MAJOR] |
| Q2 | `INTG-CAL-001` | Cao | RISK — chỉ NEW-26 (Abnormal); thiếu Normal + Boundary (chồng 1 phần giờ đơn) | [MAJOR] |
| Q3 | `REG-SHARED-001` | Cao | RISK — TC hồi quy NEW-6/7/44/47 gắn mã lạ (`RULE-TOOL-029`); NEW-44 (quản trị tuần/tháng không đổi) đã có nhưng không tính cover vì mã lạ → đổi mã | [MAJOR] |
| Q4 | `FRIEND-001` | Cao | RISK — NEW-10 (filter NV ngoài nhóm) gắn mã lạ `SEARCH-001`; nội dung đủ → đổi mã, không đẻ TC | [MAJOR] |
| Q5 | `PERF-LARGE-001` | Trung bình | RISK — NEW-1, NEW-43 `skip` (= R4), gắn mã lạ `PERF-LATENCY-001` | [MAJOR] |
| Q6 | `FUNC-DATE-001` | Cao | RISK — NEW-14/15/18/27 chỉ phủ biên **nửa đêm**; thiếu **mùa vụ 期間限定** (grep=0), **khung đầu/cuối ca**, và **kết hợp nghỉ trước-sau + mùa vụ** → 3 TC ở §7 (TC-FUNCDATE001-02/03/04) | [MAJOR] |

Đã xét và loại: `PAY-STATE-001` (nay có NEW-29) · `SYNC-APP-001` (NEW-45, `skip` unsupported — app mobile cần thiết bị thật) · `DATA-DB-001` (NEW-34 kiểm staff_id=-1 không ghi DB) · `CONC-001` (NEW-12/13/41) · `COMPAT-LEGACY-001` (xem G-COMPAT ở §7) · `OUT-TRUTH-001` (NEW-11/23/30/32/39).

---

## 3. TC trùng lặp nội dung

Đã rà 47 TC, không phát hiện trùng lặp.

- Các cặp gần giống nhưng khác mục đích/kiểu giới hạn, không trùng: NEW-19 (合計) vs NEW-20 (上限を設定しない) vs NEW-38 (上限を設定する) — cùng kịch bản repro nhưng 3 kiểu giới hạn khác nhau (cố ý phủ ma trận option). NEW-30/32/33 (quản trị ngày 合計 / biến thể / 上限を設定する) tương tự.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-15 | Đơn 指定なし course A vắt nửa đêm (23:30〜翌00:30), NV-a làm course A có ca liên tục qua nửa đêm | NEW-15: "khung của NV-b KHÔNG chọn được (đơn vắt nửa đêm không gán thử cho NV-a nên vẫn chiếm suất NV-b)" | Quyết định Leader 2026-10-14 (memory salon-limit-option2-relay): "1 staff làm trọn thì đặt được khung vắt qua 00:00 … cùng 1 staff vẫn tính liên tục". Chính NEW-15 ghi "thiết kế bảo thủ của Dev … cần PO xác nhận" | (A) chấp nhận chặn bảo thủ (gán thử bỏ qua đơn qua đêm) · (B) NV-a thực tế nhận được → NEW-15 sai, chặn oan đúng loại lỗi khách báo | [MAJOR] | Leader / PO |

**Đã rà**: 47 TC × `spec-features/admin/salon-booking/feature-spec.md` (§2.2, §2.4.4 — nay đã có 4 option sau khi lưu 2026-10-20, BR-09/10) + `kho-tcs/fa020` (nhóm 12/18/24/25/26/45/49/50/51/53) — chỉ phát hiện C1. Không có `CONF-IGNORE`.

- C1 giống round 1. NEW-28 (bug #43561 gộp ca) **không** phải mâu thuẫn — là bug thật, ghi §5.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | [BLOCKER] | NEW-33 | **TC fail chưa raise ticket** (RULE 0.6). Quản trị xem ngày kiểu 上限を設定する: hàng 「指定なし」 17:30 báo hết chỗ dù course B còn suất (上限数 2). Cùng triệu chứng #43560 (NEW-30, đã Reject) nhưng ở nhánh option 3 — chưa triage | Triage: lỗi sản phẩm màn quản trị ngày nhánh 上限を設定する hay lỗi automation? Nếu sản phẩm → raise ticket; nếu automation → sửa kịch bản. Chặn release tới khi rõ |
| I2 | [BLOCKER] | NEW-28 → #43561 (logged, High) | Bug thật: gộp ca 1.2 giờ thường, NV2 2 ca liền 16–18 + 18–20, course B 17:30–18:30 (qua biên ca 18:00) **bị ẩn** — đáng lẽ đặt được (1 staff làm trọn qua 2 ca liền). Bản fix chưa xử lý ghép ca của **chính 1 staff** qua biên ca ở giờ thường | Dev xử lý #43561; đây là biến thể giờ-thường của logic gộp ca mà NEW-18 chỉ phủ ở biên nửa đêm |
| I3 | [MAJOR] | NEW-29 → #43571 (logged, Medium) | Fail luồng thanh toán Stripe/UnivaPay. Run note (agent) ghi "30293 thiếu merchant TEST; tài nguyên thanh toán hiện vẫn thiếu" → nghi **thiếu tài nguyên test**, chưa chắc lỗi sản phẩm | Cấp merchant TEST Stripe/UnivaPay cho bot test rồi chạy lại; nếu vẫn fail mới kết luận sản phẩm. Làm rõ #43571 là lỗi gì |
| I4 | [MAJOR] | Cả bộ (47 TC) | RULE-08 / ENV-003: 47/47 chỉ chạy `local`, 0 staging/prd — task chạm job nền (2 job) + thanh toán + lệch quản trị↔LINE. Bug #43561, #43571 đều chỉ thấy ở local | Chạy lại bộ core (repro + option 3 + job + thanh toán) trên staging và prd (bot test) trước khi đóng |
| I5 | [MAJOR] | `03-dev-impact.md` | File 03 (viết cho v6) ghi option 3 「上限を設定する」 **ngoài phạm vi** — nay v7 đã đưa vào phạm vi (REQ-011, #43459/#43447, staff_id=-1). File 03 lỗi thời so với branch hiện tại | Cập nhật 03 mục 2/4: thêm nhánh option 3 (D-xx v7), file `CalendarSalonNoStaffBookingCalendarLimitTest.php`, hành vi "đơn 指定なし loại khỏi suất nhóm nhưng vẫn đếm 上限数" |
| I6 | [MAJOR] | Spec + 47 TC | 47/47 TC để trống đánh giá spec; NEW-9/10/15 tự ghi "cần PO xác nhận" nhưng vẫn ra Đạt → expected dựa thiết kế Dev. (feature-spec §2.4.4 đã bổ sung 4 option 2026-10-20 nhưng chưa có BR đếm đơn 指定なし theo course) | Leader chốt §8, cập nhật đánh giá spec trên Studio |
| I7 | [MINOR] | NEW-45 | Hồi quy app mobile `skip` [Unsupported] — runner Playwright không điều khiển app native | Giao QA chạy tay app mobile 1 lượt (đặt + random staff + quản trị ngày), đánh dấu manual |
| I8 | [NIT] | Deploy | REG-RUN-001: Dev yêu cầu restart worker queue database khi deploy (job phân bổ nạp code mới) | Thêm vào checklist deploy |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 47 TC — không có TC nào ngoài phạm vi task.

- NEW-6/7/9/31/47/#29698 (lịch 上限を設定しない không giới hạn / không course / đơn không course / lịch 個人) là hồi quy "cấu hình ngoài phạm vi giữ nguyên" (REQ-008) dẫn từ Studio `dev_impact` → không phải TC thừa.

---

## 7. TCs đề xuất bổ sung (5)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 25 受付上限, 26 前後の空き時間, 53 hồi quy) |
| Vùng regression phát hiện từ kho | TC-SLN-296 (前後の空き時間 ma trận) · TC-SLN-280 (option mặc định lịch cũ) · TC-SLN-437 (mùa vụ 期間限定) · TC-SLN-295 (slot đầu/cuối ca) · TC-SLN-211 (ca qua ngày × mùa vụ) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC có sẵn (không viết mới) | Q1/Q3/Q4 → đổi mã quan điểm NEW-2…5/6/7/10/44 trên Studio (nội dung đủ) · R4/Q5 → chạy NEW-1/NEW-43 sau khi chốt ngưỡng · G-admin/payment/option3/app → đã có NEW-28…47 |
| Căn cứ TC regression | TC-FUNCDATE001-01…04 dẫn từ Studio `dev_impact` ("rủi ro cao nhất … nghỉ trước/sau") + ma trận biên thời gian của FUNC-DATE-001 mà bộ v7 chỉ phủ nhánh nửa đêm |
| Xác nhận chống trùng | Đã đối chiếu 47 TC ở BƯỚC 0 + kho FA-020 — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNCDATE001-01 | UI | FUNC-DATE-001 | Salon booking サロン・面談予約 (LIFF): NV ngoài nhóm nhận thay đơn 指定なし × khoảng trống trước/sau 「前後の空き時間」 | Boundary | auto | dev, local, prd, staging | line-friend, web | Khoảng trống sau 30 phút của đơn NV-a chồng giờ đơn 指定なし course A → NV-a không nhận thay được (NV-b bị ẩn); khoảng trống kết thúc vừa khít → NV-a nhận được (NV-b mở) | - Đăng nhập admin bot test gói trả phí (cần 3 NV). Tạo MỚI 1 lịch salon loại 「スタッフ」 có dùng course, tên có hậu tố riêng.<br>- 「予約設定」: 「予約受付単位」 = 30 phút; 「前後の空き時間」: trước 0 phút, **sau 30 phút**; 「全承認制にする」.<br>- 「コース・スタッフ」: 「指定なし」 = 「利用する」; 「スタッフ自動割り当てを利用しない」; mọi NV 「表示する」, không filter.<br>- 「店舗とスタッフの受付上限」 = 「上限をその時間に受付可能なスタッフ数の合計にする」 + 「シフトの合算をしない」; mọi NV 「上限を設定する」 = 1.<br>- Course A, B đều 60 phút. NV-a làm A; NV-b làm A và B; NV-c làm B.<br>- Ngày X: NV-a, NV-b, NV-c đều ca 16:00–20:00.<br>- Admin thêm qua 「予約追加」, đều đã xác nhận: đơn chỉ định NV-a course A 16:30–17:30; đơn 指定なし course A 17:30–18:30; đơn 指定なし course B 17:30–18:30.<br>- F01 = bạn bè test đã kết bạn bot. | 1. F01 mở trang đặt lịch, chọn course B + NV-b, tới ngày X, quan sát khung 17:30.<br>2. Admin đổi giờ đơn chỉ định của NV-a thành 16:00–17:00, lưu.<br>3. F01 tải lại trang, chọn course B + NV-b, tới ngày X, quan sát khung 17:30.<br>4. F01 bấm khung 17:30, điền thông tin, gửi đặt lịch.<br>5. Admin mở 「予約管理」 ngày X. | - 「前後の空き時間」 sau 30 phút<br>- Đơn NV-a: lượt 1 16:30–17:30 (khoảng trống sau đến 18:00), lượt 2 16:00–17:00 (khoảng trống sau đến 17:30)<br>- 2 đơn 指定なし A, B 17:30–18:30<br>- F01: NV-b + course B | - Bước 1: khung 17:30 KHÔNG chọn được — khoảng trống sau của đơn NV-a (17:30–18:00) chồng giờ đơn 指定なし A ⇒ NV-a không nhận được, đơn A phải do NV-b làm, đơn B do NV-c.<br>- Bước 3: khung 17:30 chọn được — khoảng trống sau của đơn NV-a kết thúc đúng 17:30 ⇒ NV-a nhận đơn A.<br>- Bước 4: đặt thành công.<br>- Bước 5: có đơn mới NV-b course B 17:30–18:30; các đơn khác giữ nguyên. | | Lấp G1 · Studio dev_impact "rủi ro cao nhất: gán thử … sai (… nghỉ trước/sau)" — 1 trong 5 điều kiện ứng viên ngoài nhóm chưa TC nào phủ · dẫn từ kho TC-SLN-296 · Đánh giá spec: Spec không ghi · Evidence: screenshot LINE 2 lượt + 予約管理 |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Salon booking サロン・面談予約 (LIFF): Lịch cũ chưa từng lưu 「店舗とスタッフの受付上限」 | Normal | auto | dev, local, prd, staging | line-friend, web | Lịch cũ chưa lưu setting 受付上限 hành xử giống hệt lịch mới cấu hình bằng đúng giá trị nó đang hiển thị (mặc định 1.2) → khung NV2 + course B mở | - Đăng nhập admin bot test.<br>- Lịch cũ: lịch salon loại 「スタッフ」 có dùng course, tạo TRƯỚC khi có tính năng 「店舗とスタッフの受付上限」 (issue #29114) và chưa từng bấm lưu mục này. Local/dev không có lịch cũ → nhờ Dev xoá bản ghi `calendar_salon_setting_limit_booking` của 1 lịch mới để mô phỏng.<br>- Lịch đối chứng: tạo MỚI 1 lịch salon cùng loại, tên có hậu tố riêng.<br>- Cả 2 lịch: 「予約受付単位」 = 30 phút; 「前後の空き時間」 không cài; 「全承認制にする」; 「指定なし」 = 「利用する」; 「スタッフ自動割り当てを利用しない」; mọi NV 「表示する」, không filter.<br>- Cả 2 lịch: course A 60 phút chỉ NV1 làm; course B 60 phút chỉ NV2 làm; ngày X NV1 nghỉ, NV2 ca 16:00–20:00; 1 đơn 指定なし course A ngày X 17:30–18:30, đã xác nhận.<br>- F01 = bạn bè test đã kết bạn bot. | 1. Admin mở 「予約設定」 → 「店舗とスタッフの受付上限」 của lịch cũ, ghi lại option + giới hạn từng NV đang hiển thị (không bấm lưu).<br>2. Ở lịch đối chứng, chọn đúng các giá trị ghi ở bước 1, lưu.<br>3. F01 mở trang đặt lịch của lịch cũ, chọn course B + NV2, tới ngày X, quan sát khung 17:00, 17:30.<br>4. F01 mở trang đặt lịch của lịch đối chứng, làm lại thao tác bước 3. | - Lịch cũ chưa có setting 受付上限<br>- Đơn 指定なし course A 17:30–18:30 ở cả 2 lịch<br>- F01: NV2 + course B | - Bước 1: hiển thị 「上限をその時間に受付可能なスタッフ数の合計にする」 + 「シフトの合算をする」 (option 1.2 — mặc định lịch cũ, kho MT-22).<br>- Bước 3: khung 17:00, 17:30 chọn được — option 1.2 thuộc phạm vi fix, NV2 không làm course A.<br>- Bước 4: kết quả khung 17:00, 17:30 giống hệt bước 3. | | Lấp G-COMPAT · Q (COMPAT-LEGACY-001) · Studio `dev_impact` "chưa cài giới hạn giữ logic cũ" (REQ-008) — chưa TC nào phủ lịch cũ chưa lưu setting · kho TC-SLN-280 / MT-22 "lịch cũ mặc định 1.2" · nếu bước 3 khác bước 4 → báo Dev (§8 #3) · Đánh giá spec: Spec không ghi · Evidence: screenshot setting + LINE ở 2 lịch |
| TC-FUNCDATE001-02 | UI | FUNC-DATE-001 | Salon booking サロン・面談予約 (LIFF): Mùa vụ 「期間限定」 × đơn 指定なし course khác | Boundary | auto | dev, local, prd, staging | line-friend, web | Trong khoảng mùa vụ: đơn 指定なし course A không chiếm suất NV2 (logic #43379 vẫn đúng); ngày ngoài mùa vụ vẫn bị chặn độc lập logic 指定なし | - Đăng nhập admin bot test. Tạo MỚI 1 lịch salon loại 「スタッフ」 có dùng course, tên có hậu tố riêng.<br>- 「予約設定」: 「予約受付単位」 = 30 phút; 「前後の空き時間」 không cài; 「全承認制にする」; bật **「期間限定」** với khoảng đặt lịch = [ngày đầu … ngày Z], ngày X nằm TRONG khoảng, ngày Z+1 NGOÀI khoảng.<br>- 「コース・スタッフ」: 「指定なし」 = 「利用する」; 「スタッフ自動割り当てを利用しない」; mọi NV 「表示する」, không filter.<br>- 「店舗とスタッフの受付上限」 = 「上限をその時間に受付可能なスタッフ数の合計にする」 + 「シフトの合算をしない」; NV1, NV2 「上限を設定する」 = 1.<br>- Course A 60 phút chỉ NV1 làm; course B 60 phút chỉ NV2 làm.<br>- Ngày X (trong mùa vụ): NV1 nghỉ; NV2 ca 16:00–20:00. Admin thêm 1 đơn 指定なし course A ngày X 17:30–18:30, đã xác nhận.<br>- F01 = bạn bè test đã kết bạn bot. | 1. F01 mở trang đặt lịch, chọn course B + NV2, tới ngày X, quan sát khung 17:30.<br>2. F01 bấm khung 17:30, điền thông tin, gửi đặt lịch.<br>3. F01 điều hướng tới ngày Z+1 (ngoài mùa vụ), quan sát ngày đó có hiển thị / chọn được khung nào không.<br>4. Admin mở 「予約管理」 ngày X. | - 「期間限定」 khoảng [đầu … Z]; ngày X trong khoảng, Z+1 ngoài khoảng<br>- Đơn 指定なし course A 17:30–18:30 ngày X<br>- F01: NV2 + course B | - Bước 1: khung 17:30 ngày X chọn được — đơn 指定なし course A không chiếm suất NV2 (NV2 không làm A), logic #43379 chạy bình thường trong mùa vụ.<br>- Bước 2: đặt thành công.<br>- Bước 3: ngày Z+1 ngoài mùa vụ — không hiển thị khung / không đặt được, độc lập với logic đơn 指定なし.<br>- Bước 4: có đúng 1 đơn mới NV2 course B 17:30–18:30 ngày X. | | Lấp G-MÙAVỤ · Q6 · 47/47 TC không xét 「期間限定」 (grep = 0) · quy tắc mùa vụ: ngoài khoảng dù 1 phần không đặt được (memory salon-limit-option2-relay) · dẫn từ kho TC-SLN-437 · Đánh giá spec: Spec không ghi (Leader chốt) · Evidence: screenshot LINE trong/ngoài mùa vụ + 予約管理 |
| TC-FUNCDATE001-03 | UI | FUNC-DATE-001 | Salon booking サロン・面談予約 (LIFF): Khung đầu ca / cuối ca × đơn 指定なし course khác | Boundary | auto | dev, local, prd, staging | line-friend, web | Đơn 指定なし course A ở ngay đầu ca (16:00–17:00) và cuối ca (19:00–20:00) không chiếm suất NV2 → khung đầu ca 16:00 và cuối ca 19:00 của NV2 + course B vẫn mở | - Đăng nhập admin bot test. Tạo MỚI 1 lịch salon loại 「スタッフ」 có dùng course, tên có hậu tố riêng.<br>- 「予約設定」: 「予約受付単位」 = 30 phút; 「前後の空き時間」 không cài; 「全承認制にする」.<br>- 「コース・スタッフ」: 「指定なし」 = 「利用する」; 「スタッフ自動割り当てを利用しない」; mọi NV 「表示する」, không filter.<br>- 「店舗とスタッフの受付上限」 = 「上限をその時間に受付可能なスタッフ数の合計にする」 + 「シフトの合算をしない」; NV1, NV2 「上限を設定する」 = 1.<br>- Course A 60 phút chỉ NV1 làm; course B 60 phút chỉ NV2 làm.<br>- Ngày X: NV1 nghỉ; NV2 ca **đúng 16:00–20:00** (16:00 là đầu ca, 20:00 là hết ca → 19:00–20:00 là khung 60' cuối).<br>- Admin thêm qua 「予約追加」, đều đã xác nhận: đơn 指定なし course A 16:00–17:00 (đầu ca) và đơn 指定なし course A 19:00–20:00 (cuối ca).<br>- F01 = bạn bè test đã kết bạn bot. | 1. F01 mở trang đặt lịch, chọn course B + NV2, tới ngày X, quan sát khung **16:00** (đầu ca) và **19:00** (khung cuối 19:00–20:00).<br>2. F01 bấm khung 16:00, điền thông tin, gửi đặt lịch.<br>3. F01 tải lại, chọn course B + NV2, bấm khung 19:00, gửi đặt lịch.<br>4. Admin mở 「予約管理」 ngày X. | - NV2 ca 16:00–20:00, giới hạn 1<br>- 2 đơn 指定なし course A: 16:00–17:00 và 19:00–20:00<br>- F01: NV2 + course B, khung 16:00 rồi 19:00 | - Bước 1: khung 16:00 và 19:00 của NV2 đều chọn được — đơn 指定なし course A ở đầu/cuối ca không chiếm suất NV2 (NV2 không làm A, NV1 nghỉ); logic loại đơn 指定なし chạy đúng ở biên ca, không chỉ giữa ca.<br>- Bước 2–3: đặt 16:00 và 19:00 đều thành công.<br>- Bước 4: có 2 đơn mới NV2 course B (16:00–17:00 và 19:00–20:00); 2 đơn 指定なし course A giữ nguyên. | | Lấp G-BIÊNCA · Q6 · 47/47 TC chỉ test khung giữa ca (17:30) · biên đầu/cuối ca theo kho TC-SLN-295 · Đánh giá spec: Spec không ghi · Evidence: screenshot LINE + 予約管理 |
| TC-FUNCDATE001-04 | UI | FUNC-DATE-001 | Salon booking サロン・面談予約 (LIFF): Kết hợp 「前後の空き時間」 + 「期間限定」 × đơn 指定なし | Boundary | auto | dev, local, prd, staging | line-friend, web | Bật đồng thời nghỉ trước/sau và mùa vụ: trong mùa vụ, khoảng trống sau của NV-a quyết định NV-a có nhận thay đơn A không (→ NV-b ẩn/mở); ngày ngoài mùa vụ vẫn bị chặn | - Đăng nhập admin bot test gói trả phí (cần 3 NV). Tạo MỚI 1 lịch salon loại 「スタッフ」 có dùng course, tên có hậu tố riêng.<br>- 「予約設定」: 「予約受付単位」 = 30 phút; 「前後の空き時間」: trước 0 phút, **sau 30 phút**; 「全承認制にする」; bật **「期間限定」** với khoảng [đầu … Z], ngày X TRONG khoảng, ngày Z+1 NGOÀI khoảng.<br>- 「コース・スタッフ」: 「指定なし」 = 「利用する」; 「スタッフ自動割り当てを利用しない」; mọi NV 「表示する」, không filter.<br>- 「店舗とスタッフの受付上限」 = 「上限をその時間に受付可能なスタッフ数の合計にする」 + 「シフトの合算をしない」; mọi NV 「上限を設定する」 = 1.<br>- Course A, B đều 60 phút. NV-a làm A; NV-b làm A và B; NV-c làm B.<br>- Ngày X (trong mùa vụ): NV-a, NV-b, NV-c đều ca 16:00–20:00.<br>- Admin thêm qua 「予約追加」, đều đã xác nhận: đơn chỉ định NV-a course A 16:30–17:30; đơn 指定なし course A 17:30–18:30; đơn 指定なし course B 17:30–18:30.<br>- F01 = bạn bè test đã kết bạn bot. | 1. F01 mở trang đặt lịch, chọn course B + NV-b, tới ngày X, quan sát khung 17:30.<br>2. Admin đổi giờ đơn chỉ định NV-a thành 16:00–17:00, lưu.<br>3. F01 tải lại, chọn course B + NV-b, tới ngày X, quan sát khung 17:30; bấm đặt.<br>4. F01 điều hướng tới ngày Z+1 (ngoài mùa vụ), chọn course B + NV-b, quan sát.<br>5. Admin mở 「予約管理」 ngày X. | - 「前後の空き時間」 sau 30 phút + 「期間限定」 [đầu … Z]<br>- Đơn NV-a: lượt 1 16:30–17:30 (trống sau đến 18:00), lượt 2 16:00–17:00 (trống sau đến 17:30)<br>- 2 đơn 指定なし A, B 17:30–18:30 ngày X<br>- F01: NV-b + course B | - Bước 1: khung 17:30 ngày X KHÔNG chọn được — trống sau của đơn NV-a (17:30–18:00) chồng giờ đơn 指定なし A ⇒ NV-a không nhận, đơn A phải do NV-b.<br>- Bước 3: khung 17:30 chọn được và đặt thành công — trống sau của NV-a kết thúc đúng 17:30 ⇒ NV-a nhận đơn A. Nghỉ trước/sau và mùa vụ không can thiệp logic loại đơn 指定なし.<br>- Bước 4: ngày Z+1 ngoài mùa vụ — không đặt được dù logic 指定なし cho phép.<br>- Bước 5: có 1 đơn mới NV-b course B 17:30–18:30 ngày X. | | Lấp G1 + G-MÙAVỤ (kết hợp) · Q6 · chưa TC nào bật đồng thời 2 setting · mùa vụ ngoài khoảng không đặt được (memory salon-limit-option2-relay); nghỉ sau theo kho TC-SLN-296 + TC-SLN-211 · Đánh giá spec: Spec không ghi · Evidence: screenshot LINE 3 lượt + 予約管理 |

Ghi chú: phần lớn TC đề xuất round 1 (màn quản trị, thanh toán, option 3, app mobile, gộp ca 1.2, race) đã được bộ v7 (NEW-28…NEW-47) phủ. 5 TC còn lại nhắm vào GAP chưa ai phủ: nghỉ trước/sau (`前後の空き時間`), mùa vụ (`期間限定`), khung đầu/cuối ca, kết hợp nghỉ trước/sau + mùa vụ, và lịch cũ chưa lưu 受付上限.

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | feature-spec §2.4.4 (chưa có BR) | Đơn 指定なし vắt qua 00:00: NV ngoài nhóm có ca liên tục làm được course có được tính là người nhận thay không. Có → NEW-15 sai, code chặn oan | C1 `CONF-SPEC` (NEW-15) | Leader / PO |
| 2 | feature-spec §2.4.4 (mới) | Thêm BR đếm đơn 指定なし theo course + NV ngoài nhóm (suất, ca phủ trọn, Google, filter friend, NV ẩn, **nghỉ trước/sau**, đơn qua đêm, đơn không course), phạm vi cả 3 kiểu giới hạn, áp cho LINE · job · quản trị xem ngày. (4 option đã bổ sung 2026-10-20) | §5 I6 · G1 | PM / Dev |
| 3 | feature-spec §2.4.4 — lịch chưa lưu setting | Lịch cũ chưa có bản ghi 受付上限 tính theo option nào: màn hiển thị 1.2 (kho MT-22), cần xác nhận code đi nhánh 1.2 | TC-COMPATLEGACY001-01 | Dev |
| 4 | — (handoff Dev) | Màn quản trị xem ngày vẫn cộng suất NV 「表示しない」 (ẩn) → có thể lệch quản trị↔LINE. Dev ghi "nên mở việc riêng". Sửa trong task hay ticket riêng | Dev `dev_impact` v7 dòng "Lệch quản trị ↔ LINE còn tồn tại" | Dev / Leader |
| 5 | — (NEW-33) | Quản trị xem ngày kiểu 上限を設定する hàng 指定なし báo hết chỗ sai (đang fail) — xác nhận là lỗi sản phẩm hay automation | §5 I1 | Dev / Leader |
| 6 | feature-spec §2.4.4 — mùa vụ 期間限定 | Quy tắc mùa vụ (ngoài khoảng dù 1 phần không đặt được; ngày cuối tới 24:00) chỉ có ở memory Leader + kho, chưa ghi vào feature-spec; cần xác nhận mùa vụ không can thiệp logic đếm đơn 指定なし | TC-FUNCDATE001-02/04 | Leader / PM |
