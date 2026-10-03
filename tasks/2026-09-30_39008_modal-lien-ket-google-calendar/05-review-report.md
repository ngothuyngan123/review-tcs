# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #338 (ticket 39008, round 2, branch `ai_fixbug_39008`) |
| Tổng số TC review | 59 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 12/15 mục có TC đúng nội dung (BUG + F1–F5 + D1–D6 + T1–T3), nhưng **0/59 TC đã chạy** — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` | 6/10 điểm có TC đúng nội dung, nhưng **0/59 TC đã chạy** — **CHƯA ĐỦ** |

**Kết luận**: 18/25 vùng ảnh hưởng có TC đúng nội dung · 2 GAP · 3 RISK nội dung. Vì chưa TC nào chạy nên **toàn bộ 25 vùng đang ở mức RISK** (có TC ≠ đã test) — xem I1.

> Mẫu số (b) = 10 điểm: 4 file trong diff (blade · controller · routes · `CalendarSalonService.php` — file thứ 4 chỉ có ở branch mới, xem I2) + 6 điểm `dev_impact` nêu (phạm vi reset tất cả staff lỗi · xóa event phía Google · phản hồi thành công · regression hàm dùng chung · đổi mã lỗi 500→422 · lỗi kết nối do nhiều nguyên nhân).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F1 — endpoint mới `POST /ajax/calendar-salon/action/google-sync/reset-on-error` khi bị **gọi thẳng** | dev-impact + diff code | NEW-31, NEW-48 (chỉ case hợp lệ của bot đang đăng nhập) | **GAP** — 0 TC gọi thẳng endpoint mới với lịch bot khác / staff không có quyền / mã lịch không tồn tại hoặc thiếu. NEW-43 · NEW-47 chỉ test endpoint hủy liên kết CŨ. Thiếu mã lịch mà điều kiện lọc lịch bị bỏ thì reset lan sang **mọi lịch** của bot (cùng kiểu RISK-1 mà NEW-41 đã bắt ở endpoint cũ) | [BLOCKER] |
| G2 | T3 — liên kết lại Google Calendar **sau khi** reset (case 4/5 trong checklist 7 case Google Calendar của Leader, 2026-09-29) | dev-impact | không có | **GAP** — reset bỏ trống `google_event_id` của booking (D4). Liên kết lại thì booking được đẩy lên Google lần nữa (TC-SLN-359) → có thể **nhân đôi event** trên Google, hoặc event cũ của LME bị kéo về thành block time **tự chặn chính booking** vì hệ thống không còn nhận ra event đó là của LME | [BLOCKER] |
| G3 | Staff bị đưa về trạng thái lỗi bởi **4 mã lỗi khác nhau** (401/403/404/400 — Dev j#130742 mục 6) | diff code | Mọi TC chỉ dựng lỗi theo 1 cách: thu hồi quyền app hoặc sửa DB ở local | **RISK** — chỉ có 1 trigger. Reset gọi tiếp API Google (`deleteBookingSyncFromLme`) bằng token đã hỏng; j#130742 ghi "lỗi Google API thì bỏ qua, vẫn trả success". Phải chứng minh reset vẫn dọn xong với từng nguyên nhân lỗi | [MAJOR] |
| G4 | F5 — mã lỗi của endpoint hủy liên kết cũ đổi 500 → mã do service trả (mặc định 422) | diff code | NEW-44, NEW-58, NEW-38 | **RISK** — 3 TC đưa 3 oracle loại trừ nhau cho cùng điều kiện "bản ghi kết nối không còn" → mất chuẩn Đạt/Không đạt (C1 ở §4) | [MAJOR] |
| G5 | Xóa event phía Google khi reset (`deleteBookingSyncFromLme` — hai chiều) | diff code | NEW-26, NEW-27 | **RISK** — TC kỳ vọng event trên Google **còn nguyên**; code tái dùng luồng hủy liên kết cũ (kho TC-SLN-365 = xóa event LME đã đẩy lên Google). Chưa chốt bên nào đúng (C2 ở §4) | [BLOCKER] |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 22 quan điểm Trigger khớp task · 4 chưa cover đủ (ngoài phần đã ghi ở §1: PERM-002/PERM-003 trên endpoint mới → G1; INTG-CAL-001 → G2/G3/G5).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | PERF-LARGE-001 | Trung bình → **Cao** (sync) | **RISK** — NEW-32 chỉ tăng số **staff** (expected "thời gian chấp nhận được"), không có TC lịch nhiều **booking đã đồng bộ**. Dev tự nêu "luồng hủy gọi Google cho từng lượt đặt, lịch nhiều dữ liệu có thể chạy lâu"; reset còn lặp qua nhiều staff. Kho TC-SLN-373 (#38446) đã có lỗi hiệu năng ở chính luồng hủy liên kết, chạy production | [MAJOR] |
| Q2 | OUT-EXPORT-001 | Trung bình → **Cao** | **GAP** — reset xóa `calendar_salon_sync_booking_google_calendar_history` (D3), mà dữ liệu này hiện ở tab データ同期履歴 + file CSV lịch sử đồng bộ (spec §7.1.3, kho TC-SLN-372) và tab Googleカレンダー同期履歴 của booking (TC-SLN-131). 0 TC mở các màn này sau khi reset | [BLOCKER] |
| Q3 | JOB-001 | Cao | **RISK** — NEW-54/NEW-55 chỉ kiểm job **kéo** dữ liệu từ Google. Thiếu chiều **đẩy**: booking mới của staff vừa reset không được đẩy sang Google, và không sinh bản ghi lỗi Google để job retry chạy lại (kho TC-SLN-371). Tất cả TC job chỉ chạy local (RULE-08, xem I3) | [MAJOR] |
| Q4 | PERM-001 · STATE-CLEAN-001 · REG-SHARED-001 · DATA-AUDIT-001 | Cao | **RISK RULE-01** — mỗi mã chỉ có 1 loại case (Normal), không ghi lý do. Abnormal của REG-SHARED-001 thực tế đã có ở NEW-51/NEW-58 nhưng gắn mã nội bộ Studio nên không tính | [MAJOR] |

Đã loại khỏi phạm vi (kèm căn cứ):
- SYNC-APP-001 (App mobile): Studio `dev_impact` ghi "chỉ chạm web (sns-line)"; kho FA-020 nhóm App mobile (TC-SLN-474 → 478) không có chức năng Google Calendar → không có căn cứ App mobile hiện modal này.
- BR-10 ẩn staff (EP-62) cũng xóa liên kết Google, nhưng không gọi hàm dùng chung mới (`unlinkGoogleCalendarOfStaff`) → không phải sibling bị chạm.

---

## 3. TC trùng lặp nội dung

Đã rà 59 TC, không phát hiện trùng lặp. Các cặp gần nhau đã xét và giữ nguyên vì khác mục đích kiểm: NEW-26/NEW-27 (Google thật / log), NEW-15/NEW-16 (「閉じる」/ icon ×), NEW-49/NEW-50 (nội dung modal cũ / dữ liệu sau hủy), NEW-21/NEW-28/NEW-35 (DB / vào lại màn / phản hồi).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | CONF-TC | NEW-44 vs NEW-58 (+ tiền đề NEW-38) | Endpoint hủy liên kết cũ khi bản ghi kết nối **đã không còn** | NEW-44: **200**, không tác dụng (theo RISK-3 của technical design Studio) | NEW-58: trả **mã lỗi của nhánh nền** (mã do service trả, mặc định 422 theo j#139439). NEW-38 lại lấy chính điều kiện này để **tạo lỗi** cho reset | 1 trong 2 TC sai chuẩn — hoặc RISK-3 chưa được hiện thực (Dev giữ 422) | [MAJOR] | Dev / Leader |
| C2 | CONF-KHO | NEW-26, NEW-27 | Event đã đẩy lên Google của staff sau khi xóa liên kết | NEW-26/27: reset **không** xóa event trên Google (REQ-006, phương án A theo BA; câu xác nhận chỉ nói 「エルメ上の…スケジュールが削除」) | Kho TC-SLN-365: hủy liên kết = **xóa** event LME đã đẩy lên Google. Code reset tái dùng đúng luồng này (Studio `dev_impact`: "XÓA event phía Google — trái AC-7") | Code sai so với thiết kế (TC đúng, sẽ FAIL) / hoặc yêu cầu thật là "hủy kết nối" như luồng cũ → REQ-006 + NEW-26/27 cần sửa | [BLOCKER] — thao tác không hoàn tác, xóa dữ liệu trên tài khoản Google của khách | PM / BA |
| C3 | CONF-SPEC | NEW-40, NEW-45, NEW-46 | Hợp đồng endpoint hủy liên kết cũ với 2 cờ `delete_lme_google_schedule` / `delete_google_side_event` | TC test 2 cờ theo technical design v2 của Studio | Dev (j#139439) không thêm cờ nào — tạo endpoint riêng `reset-on-error`, endpoint cũ giữ nguyên. `spec-features` BR-09 không nhắc cờ | TC test hợp đồng chưa có → sẽ FAIL/không áp dụng / hoặc Dev chưa làm đủ thiết kế | [MAJOR] | Dev / PM |
| C4 | CONF-SPEC | NEW-38 | Reset nhiều staff mà 1 staff hủy thất bại | Báo câu lỗi cố định + **dừng** ở staff lỗi (BR-C2-08, default A-8 của spec Studio) | j#130742: "1 nhân viên hủy lỗi thì **vẫn tiếp tục** các nhân viên còn lại + log, trả **success**" (j#139439 không nhắc lại) | Code lệch spec / hoặc spec cần đổi theo cách Dev đã làm | [MAJOR] | PM / Dev |
| C5 | CONF-SPEC | NEW-35 | Phản hồi khi reset thành công | Toast 「Googleカレンダーの接続設定をリセットしました。」 + mở tab Googleカレンダー連携 (BR-C2-07) | j#139439: "gọi endpoint … rồi **tải lại trang**"; Studio `dev_impact` cũng nghi thiếu toast + điều hướng | Code thiếu phần phản hồi / hoặc spec chấp nhận chỉ reload | [MAJOR] | Dev |

Đã rà 59 TC × `spec-features/admin/salon-booking/feature-spec.md` (BR-09, BR-10, §7.1.3) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm Googleカレンダー連携 TC-SLN-359 → 376, TC-SLN-131, TC-SLN-372). `spec-features` chưa có rule nào cho thao tác reset → C3–C5 lấy chuẩn là spec Studio của task (BR-C2-xx).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | [BLOCKER] | Toàn bộ 59 TC | 0/59 TC đã chạy (0% Đạt) ở mọi env — chưa có kết luận test nào | Chạy sau khi xử lý I2 |
| I2 | [BLOCKER] | Studio task #338 | Task Studio gắn branch `ai_fixbug_39008` (j#130742, base `release_step_20260623`, 3 file). Bản fix cần test là `ai_small_39008` (j#139439, base `release_step_20260930`, commit `1dfa4ac55e`, 4 file — thêm `CalendarSalonService.php`). `spec_delta` / `diffStat` hiện là diff của branch CŨ. Studio đã tự cảnh báo "branch đang tranh chấp" | Chuyển task sang `ai_small_39008` rồi lấy lại diff trước khi chạy; nếu không thì kết quả chạy không có giá trị |
| I3 | [MAJOR] | NEW-52 → NEW-55, NEW-26 | RULE-08 / ENV-003 — task chạm đồng bộ Google Calendar (webhook + job nền + API Google), nhưng 0 TC chạy production; TC job/webhook đều khai `local` | Thêm ít nhất 1 lượt production cho reset + job sau reset (Q1, Q3) |
| I4 | [MAJOR] | NEW-42 (lần 2), NEW-47, NEW-31, NEW-48 | RULE-13 — NEW-42 khai mã lịch không tồn tại → 422 (quy ước: 403/404); NEW-47 chỉ ghi "bị chặn", không có mã HTTP; NEW-31/NEW-48 ghi "khớp contract", không có mã | Sửa expected theo bảng mục 1.1 của checklist-lme |
| I5 | [MAJOR] | NEW-31, NEW-48, NEW-56, NEW-58, NEW-32 | Expected không đo được: "phải khớp contract thực tế", "hiển thị bình thường, không có dòng trống", "đúng mã lỗi mà nhánh nền quy định", "thời gian chấp nhận được" | Ghi giá trị cụ thể (mã HTTP, số dòng, ngưỡng giây) |
| I6 | [MAJOR] | NEW-38, NEW-36 | Tiền đề không tạo ra được lỗi như mô tả. NEW-38 xóa trước bản ghi kết nối của NV-B → endpoint chỉ lấy staff có bản ghi `status_connect_gg_calendar = 0` nên NV-B bị **loại khỏi danh sách**, không có bước hủy nào thất bại. NEW-36 "chặn lời gọi tới Google" → theo j#130742 lỗi Google API thì vẫn trả success | Dựng lỗi ở bước ghi DB của một staff (vd khóa bản ghi), không dựng ở phía Google; chốt C1 + C4 trước |
| I7 | [MAJOR] | NEW-50 | Regression hủy liên kết cũ không kiểm event phía Google bị xóa — đây chính là hành vi của luồng cũ (kho TC-SLN-365) và là điểm khác biệt với reset. Chỉ có NEW-45 kiểm qua log, chạy local | Thêm bước mở Google Calendar sau khi hủy liên kết vào NEW-50 |
| I8 | [NIT] | NEW-60 | Kiểm mục 「対象スタッフ」 trong modal xác nhận; báo cáo Dev (icon + tiêu đề + câu cảnh báo + 2 nút) và NEW-12 đều không có mục này; bước "bấm reset của NV-A" nghe như reset theo từng staff, trái phạm vi "tất cả staff lỗi" (NEW-22) | Hỏi tác giả (trangnq) nguồn thiết kế của mục này; nếu có thật thì thêm case lịch có 2 staff lỗi |

---

## 6. TCs thừa / ngoài phạm vi task

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | NEW-34 | Không map BUG/F/D/T · diff không có migration · DATA-MIG-001 không có Trigger | 4 file trong diff đều là code (blade/controller/routes/service); Dev mục 4.2 không có MIGRATE | Bỏ khỏi phạm vi task | [MINOR] |
| X2 | NEW-9 | Test màn chi tiết lịch bài học — layer không bị chạm code (AP-5) | Diff chỉ sửa `calendar_salon/detail.blade.php`; Dev ghi "nút cùng chữ ở Lesson/Form-answer là modal Google SHEET — ngoài scope, không sửa" | Chuyển sang bộ regression chung của kho | [NIT] |
| X3 | NEW-10 | Như X2 — màn trả lời form | Như X2 | Chuyển sang bộ regression chung của kho | [NIT] |

Gate đã chạy: 3 TC trên không phải TC duy nhất cover impact nào trong file 03. NEW-8 (modal Spreadsheet trên **cùng** file blade bị sửa) giữ lại.

---

## 7. TCs đề xuất bổ sung (11)

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (bảng Coverage 54 nhóm + nhóm Googleカレンダー連携 + TC-SLN-131/372/373/375) |
| Vùng regression phát hiện từ kho | TC-SLN-359 (liên kết → đẩy booking lên Google) · TC-SLN-365 (hủy liên kết xóa 2 chiều) · TC-SLN-371 (job retry lỗi Google) · TC-SLN-372 / TC-SLN-131 (lịch sử đồng bộ + CSV) · TC-SLN-373 (hiệu năng hủy liên kết) |
| Conflict expected vs kho | NEW-26/27 vs TC-SLN-365 → C2, đã đưa §4 + §8. TC-INTGCAL001-01 ghi expected theo quy tắc nghiệp vụ (mỗi booking chỉ có 1 event), dùng được cho cả 2 cách chốt C2 |
| GAP dùng lại TC kho (không viết mới) | Không |
| G4, G5 | Không đẻ TC mới — TC đã có (NEW-44/58/38, NEW-26/27), chỉ chờ chốt C1/C2 rồi sửa expected trên Studio; viết thêm sẽ trùng (BƯỚC 5b) |
| Q4 | Không đẻ TC mới — ghi lý do thiếu loại case trên Studio, hoặc gắn lại mã REG-SHARED-001 cho NEW-51/NEW-58 |
| Căn cứ TC regression R | Không có TC R riêng — các regression đã đi theo G2 / Q2 / Q3 |
| Xác nhận chống trùng | Đã đối chiếu 59 TC ở BƯỚC 0 + kho FA-020 — không TC đề xuất nào trùng (NEW-43/NEW-47 thuộc endpoint cũ; NEW-32 tăng số staff, không tăng số booking; NEW-54/55 là job kéo về, không phải đẩy lên) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERM003-01 | API | PERM-003 | Googleカレンダー連携 — đặt lại cài đặt kết nối | Abnormal | auto | Tất cả | Gọi thẳng endpoint đặt lại kết nối Google Calendar (reset-on-error) với lịch salon của bot khác thì bị chặn | - Có 2 phiên đăng nhập riêng: phiên 1 ở bot A, phiên 2 ở bot B<br>- Bot B có lịch salon SB có staff S9 đang lỗi kết nối Google Calendar (modal cảnh báo tự mở khi vào màn chi tiết lịch SB) | 1. Ở phiên 1 (bot A), gửi request POST tới /ajax/calendar-salon/action/google-sync/reset-on-error với mã lịch SB<br>2. Đọc mã HTTP và nội dung phản hồi<br>3. Ở phiên 2 (bot B), mở màn chi tiết lịch SB<br>4. Mở tab Googleカレンダー連携 của lịch SB | Mã lịch: SB (thuộc bot B)<br>Phiên gửi request: bot A | Mã HTTP 403 hoặc 404, không phải 200. Ở phiên bot B: modal cảnh báo mất kết nối của lịch SB vẫn tự mở; tab Googleカレンダー連携 vẫn hiện S9 ở trạng thái lỗi kết nối; không có dòng lịch sử hủy kết nối mới cho S9 | | Lấp G1 · RULE-13 (cross-bot = 403/404) · dùng 2 phiên riêng vì đổi bot ở 1 tab đổi cả trình duyệt · Đánh giá spec: Spec không ghi — chuẩn theo RULE-13 · Evidence: request/response + ảnh tab liên kết bot B |
| TC-PERM003-02 | API | PERM-003 | Googleカレンダー連携 — đặt lại cài đặt kết nối | Abnormal | auto | Tất cả | Gọi endpoint đặt lại kết nối với mã lịch không tồn tại hoặc thiếu mã lịch thì bị từ chối và không lịch nào bị đặt lại | - Đăng nhập admin bot A<br>- Bot A có 2 lịch salon L1 và L3, mỗi lịch có 1 staff đang lỗi kết nối Google Calendar (NV-A ở L1, NV-D ở L3) | 1. Gửi POST tới /ajax/calendar-salon/action/google-sync/reset-on-error KHÔNG kèm mã lịch, đọc mã HTTP<br>2. Gửi lại với mã lịch là một số không tồn tại, đọc mã HTTP<br>3. Gửi lại với mã lịch là chuỗi chữ abc, đọc mã HTTP<br>4. Mở màn chi tiết lịch L1 rồi lịch L3 | Lần 1: không gửi mã lịch<br>Lần 2: mã lịch 99999999<br>Lần 3: mã lịch abc | Lần 1 và lần 3: mã HTTP 400 hoặc 422. Lần 2: mã HTTP 403 hoặc 404. Không lần nào trả 200 hoặc 500. Sau cả 3 lần: modal cảnh báo vẫn tự mở ở cả lịch L1 và L3; NV-A và NV-D vẫn ở trạng thái lỗi kết nối trên tab Googleカレンダー連携 | | Lấp G1 · nếu thiếu mã lịch mà điều kiện lọc lịch bị bỏ thì reset lan sang mọi lịch của bot (cùng kiểu RISK-1 ở NEW-41) · Đánh giá spec: Spec không ghi — chuẩn theo RULE-13 · Evidence: request/response + ảnh 2 lịch |
| TC-PERM002-01 | API | PERM-002 | Googleカレンダー連携 — đặt lại cài đặt kết nối | Abnormal | auto | Tất cả | Tài khoản staff không có quyền màn 予約管理 gọi thẳng endpoint đặt lại kết nối thì bị chặn | - Bot A có tài khoản staff ST1 KHÔNG được cấp quyền màn 予約管理<br>- Lịch salon L1 của bot A có staff NV-A đang lỗi kết nối Google Calendar | 1. Đăng nhập ST1, gửi POST tới /ajax/calendar-salon/action/google-sync/reset-on-error với mã lịch L1<br>2. Đọc mã HTTP và nội dung phản hồi<br>3. Đăng nhập admin bot A ở phiên khác, mở màn chi tiết lịch L1<br>4. Mở tab Googleカレンダー連携 của lịch L1 | Tài khoản: ST1 (không có quyền 予約管理)<br>Mã lịch: L1 | Mã HTTP 403 hoặc 404. Phiên admin: modal cảnh báo vẫn tự mở; NV-A vẫn ở trạng thái lỗi kết nối; không có dòng lịch sử hủy kết nối mới | | Lấp G1 · Leader chốt #39275: staff không có quyền tính năng thì chặn cả API · kho MT-35: phân quyền staff salon chưa từng được test · Đánh giá spec: Đã hỏi leader · Evidence: request/response + ảnh tab liên kết |
| TC-INTGCAL001-01 | API | INTG-CAL-001 | Googleカレンダー連携 | Normal | auto | Tất cả | Sau khi đặt lại cài đặt, liên kết lại CÙNG tài khoản Google thì mỗi lịch hẹn chỉ có 1 event trên Google và không tự chặn chính nó | - Tài khoản Google test G-A dựng riêng cho lần chạy<br>- Lịch salon L1, staff NV-A đã liên kết G-A; có 2 lịch hẹn 予約確定 của NV-A ở tương lai đã hiện trên Google Calendar của G-A<br>- Trên G-A có thêm 1 event tự tạo (không phải từ LME) trong giờ làm của NV-A<br>- Đưa NV-A về trạng thái lỗi kết nối, rồi thực hiện đặt lại cài đặt kết nối trên màn chi tiết lịch L1 | 1. Mở tab Googleカレンダー連携 của lịch L1, liên kết lại NV-A với tài khoản G-A<br>2. Chờ lượt đồng bộ đầu tiên chạy xong<br>3. Mở Google Calendar của G-A, đếm số event ở giờ của 2 lịch hẹn<br>4. Mở lưới ngày trên màn chi tiết lịch L1 ở ngày của 2 lịch hẹn và ngày có event tự tạo<br>5. Mở trang đặt lịch của khách, chọn NV-A, xem các khung giờ đó | 2 lịch hẹn 予約確定 của NV-A<br>1 event tự tạo trên G-A | Mỗi lịch hẹn có ĐÚNG 1 event trên Google Calendar của G-A (không bị nhân đôi). Event tự tạo được kéo về thành block time ở đúng khung giờ. Ở khung giờ của 2 lịch hẹn, lưới admin chỉ hiện lịch hẹn, KHÔNG hiện thêm block time Google trùng giờ. Modal cảnh báo không mở | | Lấp G2 · checklist 7 case Google Calendar (Leader 2026-09-29) case 4: mất liên kết phía Google → liên kết lại tài khoản cũ; kéo về phải trừ event của booking LME · Expected theo quy tắc nghiệp vụ, đúng với cả 2 cách chốt C2 · Đánh giá spec: Đã hỏi leader · Evidence: ảnh Google Calendar + ảnh lưới admin |
| TC-INTGCAL001-02 | API | INTG-CAL-001 | Googleカレンダー連携 | Normal | auto | Tất cả | Sau khi đặt lại cài đặt, liên kết tài khoản Google MỚI thì lịch hẹn được đẩy sang tài khoản mới và block time của tài khoản cũ không còn | - 2 tài khoản Google test G-A và G-B dựng riêng<br>- Lịch salon L1, NV-A đã liên kết G-A, có 2 lịch hẹn 予約確定 tương lai và 1 block time kéo về từ event tự tạo trên G-A<br>- Đưa NV-A về trạng thái lỗi, rồi đặt lại cài đặt kết nối trên màn chi tiết lịch L1 | 1. Mở tab Googleカレンダー連携 của lịch L1, liên kết NV-A với tài khoản G-B<br>2. Chờ lượt đồng bộ đầu tiên chạy xong<br>3. Mở Google Calendar của G-B, tìm 2 lịch hẹn<br>4. Mở lưới ngày của lịch L1 ở ngày có event tự tạo trên G-A<br>5. Mở trang đặt lịch của khách, chọn NV-A, xem khung giờ của event G-A | Tài khoản cũ: G-A<br>Tài khoản mới: G-B | Google Calendar của G-B có đúng 1 event cho mỗi lịch hẹn. Block time của event tự tạo trên G-A KHÔNG còn trên lưới admin; khung giờ đó mở cho khách đặt. Tab liên kết hiện NV-A đã liên kết với G-B | | Lấp G2 · checklist 7 case Google Calendar case 5: mất liên kết phía Google → liên kết tài khoản mới · Đánh giá spec: Đã hỏi leader · Evidence: ảnh Google Calendar G-B + lưới admin + trang đặt lịch |
| TC-INTGCAL001-03 | API | INTG-CAL-001 | Màn chi tiết lịch salon — đặt lại cài đặt kết nối | Normal | auto | Tất cả | Đặt lại cài đặt hoàn tất khi staff lỗi kết nối do đã thu hồi quyền ứng dụng trong tài khoản Google | - Tài khoản Google test G-A dựng riêng<br>- Lịch salon L1, NV-A liên kết G-A, có 1 lịch hẹn đã đẩy lên Google và 1 block time kéo về<br>- Vào cài đặt bảo mật của G-A, gỡ quyền truy cập của ứng dụng エルメ; chờ lượt đồng bộ chạy để NV-A chuyển sang lỗi (modal cảnh báo tự mở) | 1. Mở màn chi tiết lịch L1, bấm Googleカレンダー接続設定をリセットする rồi 設定をリセットする<br>2. Chờ xử lý xong, đọc thông báo trên màn<br>3. Mở tab Googleカレンダー連携 của lịch L1<br>4. Mở lưới ngày có block time cũ và có lịch hẹn<br>5. Rời màn rồi mở lại màn chi tiết lịch L1 | Nguyên nhân lỗi: thu hồi quyền ứng dụng (token hết hiệu lực) | Không hiện câu lỗi 「Googleカレンダーの接続設定のリセットに失敗しました。」. NV-A ở trạng thái chưa liên kết. Block time cũ không còn trên lưới; lịch hẹn vẫn còn với nguyên trạng thái. Vào lại màn thì modal cảnh báo không tự mở | | Lấp G3 · trigger 1/3 · token hỏng nên mọi lời gọi xóa phía Google sẽ lỗi — kiểm phần dọn dữ liệu phía エルメ vẫn chạy hết · Đánh giá spec: Spec không ghi · Evidence: ảnh tab liên kết + lưới admin |
| TC-INTGCAL001-04 | API | INTG-CAL-001 | Màn chi tiết lịch salon — đặt lại cài đặt kết nối | Normal | auto | Tất cả | Đặt lại cài đặt hoàn tất khi staff lỗi kết nối do lịch Google đã liên kết bị xóa | - Tài khoản Google test G-A dựng riêng, tạo 1 lịch phụ CAL-X<br>- Lịch salon L1, NV-A liên kết G-A chọn lịch CAL-X, có 1 lịch hẹn đã đẩy lên CAL-X và 1 block time kéo về<br>- Xóa lịch CAL-X trên Google; chờ lượt đồng bộ chạy để NV-A chuyển sang lỗi | 1. Mở màn chi tiết lịch L1, bấm Googleカレンダー接続設定をリセットする rồi 設定をリセットする<br>2. Chờ xử lý xong, đọc thông báo trên màn<br>3. Mở tab Googleカレンダー連携 của lịch L1<br>4. Mở lưới ngày có block time cũ và có lịch hẹn<br>5. Rời màn rồi mở lại màn chi tiết lịch L1 | Nguyên nhân lỗi: lịch Google đã liên kết bị xóa | Không hiện câu lỗi đặt lại thất bại. NV-A ở trạng thái chưa liên kết. Block time cũ không còn; lịch hẹn vẫn còn. Vào lại màn thì modal cảnh báo không tự mở | | Lấp G3 · trigger 2/3 · Đánh giá spec: Spec không ghi · Evidence: ảnh tab liên kết + lưới admin |
| TC-INTGCAL001-05 | API | INTG-CAL-001 | Màn chi tiết lịch salon — đặt lại cài đặt kết nối | Abnormal | auto | Tất cả | Đặt lại cài đặt hoàn tất khi staff lỗi kết nối do bị gỡ quyền ghi trên lịch Google được chia sẻ | - Tài khoản Google G-OWNER sở hữu lịch CAL-S, chia sẻ quyền chỉnh sửa cho tài khoản G-A<br>- Lịch salon L1, NV-A liên kết G-A chọn lịch CAL-S, có 1 lịch hẹn đã đẩy lên CAL-S<br>- Ở G-OWNER, gỡ quyền chia sẻ của G-A với CAL-S; chờ lượt đồng bộ chạy để NV-A chuyển sang lỗi | 1. Mở màn chi tiết lịch L1, bấm Googleカレンダー接続設定をリセットする rồi 設定をリセットする<br>2. Chờ xử lý xong, đọc thông báo trên màn<br>3. Mở tab Googleカレンダー連携 của lịch L1<br>4. Rời màn rồi mở lại màn chi tiết lịch L1 | Nguyên nhân lỗi: mất quyền ghi trên lịch chia sẻ | Không hiện câu lỗi đặt lại thất bại. NV-A ở trạng thái chưa liên kết. Lịch hẹn vẫn còn. Vào lại màn thì modal cảnh báo không tự mở | | Lấp G3 · trigger 3/3 · Đánh giá spec: Spec không ghi · Evidence: ảnh tab liên kết |
| TC-PERFLARGE001-01 | API | PERF-LARGE-001 | Màn chi tiết lịch salon — đặt lại cài đặt kết nối | Boundary | manual | product | Đặt lại cài đặt trên lịch có nhiều lịch hẹn đã đồng bộ không bị treo và xử lý hết | - Bot test trên production, không phải bot khách<br>- Lịch salon LP có 2 staff NV-P1, NV-P2 cùng lỗi kết nối Google Calendar; tổng cộng ít nhất 500 lịch hẹn đã đẩy lên Google và ít nhất 50 block time kéo về | 1. Mở màn chi tiết lịch LP, bấm Googleカレンダー接続設定をリセットする rồi 設定をリセットする, bấm giờ<br>2. Chờ tới khi màn phản hồi xong, ghi thời gian<br>3. Mở tab Googleカレンダー連携 của lịch LP<br>4. Mở màn danh sách lịch hẹn, đếm số lịch hẹn của 2 staff | Ít nhất 500 lịch hẹn đã đồng bộ, 2 staff lỗi | Màn phản hồi trong 60 giây, không hiện lỗi hết thời gian chờ (504) và không có màn trắng. Cả NV-P1 và NV-P2 ở trạng thái chưa liên kết. Số lịch hẹn của 2 staff giữ nguyên như trước thao tác | | Lấp Q1 · RULE-08 performance · manual vì môi trường production · dẫn từ TC-SLN-373 (#38446) · ngưỡng 60 giây cần Leader xác nhận · Đánh giá spec: Spec không ghi · Evidence: video có đồng hồ + ảnh tab liên kết |
| TC-OUTEXPORT001-01 | API | OUT-EXPORT-001 | Googleカレンダー連携 — データ同期履歴 | Normal | auto | Tất cả | Sau khi đặt lại cài đặt, tab データ同期履歴, file CSV lịch sử đồng bộ và tab Googleカレンダー同期履歴 của lịch hẹn vẫn mở được | - Lịch salon L1 có 2 staff: NV-A đang lỗi kết nối, NV-C liên kết bình thường; cả 2 đã có nhiều lượt đồng bộ 2 chiều<br>- Đã chụp tab データ同期履歴 và tải 1 file CSV lịch sử đồng bộ trước khi thao tác<br>- Có lịch hẹn R1 của NV-A đã đẩy lên Google | 1. Mở màn chi tiết lịch L1, thực hiện đặt lại cài đặt kết nối<br>2. Mở tab データ同期履歴 của lịch L1, xem danh sách<br>3. Bấm tải file CSV lịch sử đồng bộ, mở file<br>4. Mở chi tiết lịch hẹn R1, xem tab Googleカレンダー同期履歴 | Staff bị đặt lại: NV-A<br>Đối chứng: NV-C | Tab データ同期履歴 mở được, không lỗi; các dòng của NV-C còn nguyên như ảnh trước thao tác. File CSV tải được, mở được bằng Excel, các dòng của NV-C khớp với file trước. Chi tiết lịch hẹn R1 mở được, không lỗi. Số dòng của NV-A còn lại ghi vào Ghi chú để Leader chốt có được phép xóa hay không | | Lấp Q2 · D3 xóa lịch sử đồng bộ của NV-A · dẫn từ TC-SLN-372 và TC-SLN-131 · spec §7.1.3 CSV SHIFT-JIS · Đánh giá spec: Spec không ghi việc reset có xóa lịch sử hay không → đã đưa §8 · Evidence: ảnh tab + file CSV trước/sau |
| TC-JOB001-01 | Job | JOB-001 | Googleカレンダー連携 — đồng bộ lịch hẹn lên Google | Normal | manual | product | Lịch hẹn mới của staff vừa được đặt lại cài đặt không bị đẩy sang Google và không sinh lỗi đồng bộ | - Bot test trên production, không phải bot khách<br>- Lịch salon L1, NV-A vừa được đặt lại cài đặt kết nối (tab liên kết hiện chưa liên kết)<br>- NV-C cùng lịch liên kết Google bình thường để đối chứng | 1. Khách đặt 1 lịch hẹn với NV-A qua trang đặt lịch<br>2. Khách đặt 1 lịch hẹn với NV-C<br>3. Chờ 10 phút cho job đồng bộ và job retry chạy<br>4. Mở Google Calendar của NV-C và của tài khoản Google cũ của NV-A<br>5. Mở màn chi tiết lịch L1 | 1 lịch hẹn mới của NV-A, 1 lịch hẹn mới của NV-C | Lịch hẹn của NV-C hiện trên Google Calendar của NV-C. Lịch hẹn của NV-A KHÔNG xuất hiện trên tài khoản Google cũ của NV-A. Màn chi tiết lịch L1 không mở lại modal cảnh báo mất kết nối. Lịch hẹn của NV-A ở trạng thái 予約確定 bình thường | | Lấp Q3 · RULE-08 job nền · manual vì môi trường production · dẫn từ TC-SLN-371 (job retry ghi bảng lỗi Google) + D5 · Đánh giá spec: Spec không ghi · Evidence: ảnh Google Calendar 2 tài khoản + màn chi tiết lịch |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | Technical design Studio RISK-3 / mã lỗi endpoint hủy liên kết cũ | Chốt 1 mã cho "bản ghi kết nối không còn" (200 không tác dụng hay 422) rồi sửa NEW-44 / NEW-58 / tiền đề NEW-38 | C1 CONF-TC | Dev / Leader |
| 2 | REQ-006 / BR-C2-04b + `spec-features` BR-09 | Reset có xóa event LME đã đẩy lên Google hay không. Nếu giữ phương án A → Dev phải bỏ bước xóa phía Google khỏi luồng reset; nếu đổi → sửa REQ-006, NEW-26, NEW-27 và câu cảnh báo trong modal xác nhận | C2 CONF-KHO | PM / BA |
| 3 | Technical design Studio — hợp đồng EP-A100 (2 cờ) | Xác nhận thiết kế cuối là endpoint riêng `reset-on-error` (như Dev đã làm) → archive hoặc sửa NEW-40 / NEW-45 / NEW-46 | C3 CONF-SPEC | Dev / PM |
| 4 | BR-C2-08 / default A-8 | Khi 1 staff hủy thất bại: dừng + báo lỗi (spec) hay tiếp tục + trả success (Dev j#130742) | C4 CONF-SPEC | PM / Dev |
| 5 | BR-C2-07 | Phản hồi thành công: toast + mở tab Googleカレンダー連携 (spec) hay chỉ tải lại trang (Dev j#139439) | C5 CONF-SPEC | Dev |
| 6 | `spec-features/admin/salon-booking/feature-spec.md` BR-09 + §7.1.3 | Bổ sung thao tác reset từ modal cảnh báo (phạm vi: mọi staff lỗi của lịch, lọc theo bot) và việc reset có xóa lịch sử đồng bộ (D3) hiện ở tab データ同期履歴 / CSV hay không | BƯỚC 1 — spec chưa có rule reset · Q2 | PM |
