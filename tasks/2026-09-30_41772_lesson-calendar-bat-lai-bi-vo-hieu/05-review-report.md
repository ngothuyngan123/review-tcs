# 05 — Review Report

> Draft cho Leader verify. Round 1 · review bởi `/review-tc` ngày 2026-09-30.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #343 (ticket 41772, round 1, status `tc-ready`, reviewState `leader`) |
| Tổng số TC review | 25 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 10/13 mục có TC đủ chiều — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` | 4/9 điểm có TC đủ chiều — **CHƯA ĐỦ** |

**Kết luận**: 10/13 vùng ảnh hưởng (a) + 4/9 điểm (b) có TC về mặt thiết kế · 3 GAP · 4 RISK. ⚠️ Toàn bộ 25 TC **chưa chạy** (xem §5 I1) → kể cả các vùng "đủ" cũng chưa có kết luận Đạt.

> Mẫu số (a) = BUG + F1–F3 + D1–D3 + T1–T6. D4–D6 là khẳng định "không ảnh hưởng" (không migration / job Java không map cờ / 15 câu ghi khác dùng whitelist) → không tính mẫu số.
> Mẫu số (b) = 2 file thuộc ticket (`CalendarManagementController.php`, `index.js`) + 3 rủi ro hồi quy (modal 管理名 · lịch trống 店舗名 · luồng tạo lịch) + 3 hành vi đổi (nới validate · error branch · bật lại hiện ở các surface đọc cờ) + 1 caller dùng chung hàm ghi (`CalendarManagementService::sort`, Dev mục 3). 14/16 file còn lại trong `spec_delta` thuộc ticket khác — xem §5 I2.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Nới `calendar_name` sang `sometimes` → mọi payload **không có** `calendar_name` giờ lọt validate, gồm cả giá trị cờ lạ (`enable_use_calendar=2` / `"abc"`) và body rỗng. Spec §7 dòng 2: `!= 1` ⇒ LIFF chặn → giá trị lạ lưu vào DB sẽ làm lịch "có vẻ bật" nhưng khách không đặt được | diff code | NEW-20 (chỉ payload đúng 0/1) | RISK — chỉ test hành vi MỚI mong muốn, chưa test phía bị nới ra (câu 4) | [MAJOR] |
| G2 | Nới validate + `editCalendar` = `update($request->all() trừ id)` (spec §11.1 A-02, Dev xác nhận `except([id])`) → payload chỉ có trường ngoài (`is_use_payment`, `bot_id`, `google_sheet_access_token`, `code_delete`) trên lịch **cùng bot** nay không cần kèm `calendar_name` | diff code | NEW-23 (chỉ cross-bot / không tồn tại) | GAP — không TC nào kiểm server chỉ ghi đúng cờ khi body chứa trường khác | [MAJOR] |
| G3 | F2 — `enableUseCalendar` nhánh error gọi `showLessonAjaxError(xhr)` cho **mọi** lỗi = generic-fix | dev-impact + diff code | NEW-8 (1 trigger: lịch bị chuyển bot → 「カレンダーが見つかりません。」) | RISK — generic-fix chỉ test 1 trigger; thiếu ≥ 2 trigger khác + 1 trigger không có phản hồi server (fallback) | [BLOCKER] |
| G4 | T3 — trang LIFF đặt lịch của khách (chỗ sinh triệu chứng) | dev-impact | NEW-17 | RISK — mở bằng 「予約カレンダーを見る」 = trang **preview admin** (expected có 「この画面はプレビューとなります。」), không phải LINE user mở URL booking / URL lịch sử (RULE-06) | [MAJOR] |
| G5 | T5 — init-data thiết lập action (`UserController:797` / `:3060`); Studio REQ-009 nêu cụ thể "gán hành động cho richmenu" | dev-impact + diff code | không có (NEW-18 = tin nhắn mẫu, NEW-19 = Step) | GAP — 0 TC cho picker lịch ở luồng action / richmenu. Input thiếu: Dev chưa nêu tên màn gọi 2 dòng init-data | [MAJOR] |
| G6 | Endpoint PARTIAL UPDATE dùng chung 2 caller — Studio REQ-006: "đổi 管理名 không đổi trạng thái 有効/無効, **kể cả khi trang đã mở từ trước và trạng thái vừa bị đổi ở nơi khác**" | diff code | NEW-12 (cùng 1 tab, không có trạng thái cũ) | RISK — chưa test modal 管理名 trên trang cũ có ghi đè cờ vừa đổi ở tab khác không | [MAJOR] |
| G7 | Sắp xếp lịch (popup sắp xếp ở màn danh sách) — Dev mục 3: `CalendarManagementRepository::editCalendar` (hàm ghi cờ 有効/無効) **cũng được `CalendarManagementService::sort` dùng** | diff code | không có (NEW-7 chỉ kiểm cột thứ tự không bị đổi khi bật/tắt) | GAP — hàm dùng chung có caller không TC nào đi qua (câu 3); chưa kiểm sắp xếp giữ nguyên trạng thái 有効/無効 + 管理名, và sắp xếp trên trang cũ có ghi đè cờ không | [MAJOR] |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 21 quan điểm Trigger khớp task · 4 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `CONC-001` | Cao | GAP — nút 有効/無効 là thao tác ghi trạng thái; chưa có TC double-click / 2 tab cùng sửa 1 lịch (kịch bản 3 gộp với G6) | [BLOCKER] |
| Q2 | `PERM-001` | Cao | RISK — NEW-6 chỉ Normal (staff CÓ quyền); thiếu Abnormal staff KHÔNG có quyền レッスン予約 gọi toggle (RULE-01) | [MAJOR] |
| Q3 | `LIFF-ENTRY-001` | Cao | GAP — không TC nào mang mã này; sau bật lại chưa kiểm LINE user mở URL booking + URL lịch sử (gộp chung TC với G4) | [BLOCKER] |
| Q4 | `FUNC-SEQ-001` | Trung bình (BẮT BUỘC với màn có Sort) | RISK — NEW-3 chỉ nối tiếp bật/tắt; chưa có TC nối tiếp bật/tắt ↔ sắp xếp trên cùng danh sách (gộp chung TC với G7) | [MAJOR] |

> Đã loại khỏi phạm vi (có căn cứ): `JOB-001` (Dev 4.2: entity Java không map `enable_use_calendar`, không job đọc/ghi cờ) · `INTG-SHEET-001` (`CalendarGoogleSheetService` ghi bằng whitelist không có cờ) · `PAY-LIMIT-001` (spec BR-06: hạn mức đếm số lịch tạo, toggle không qua `PlanLimitGuard`) · `OUT-EXPORT-001` (CSV 受付枠 không đọc cờ) · `ENV-003` / RULE-08 (không chạm media / domain / job / bill).

---

## 3. TC trùng lặp nội dung

Đã rà 25 TC, không phát hiện trùng lặp. Các cặp gần nhau đã soi và giữ nguyên vì khác tầng / khác ý định: NEW-1 (UI) vs NEW-20 (API) · NEW-13 (chặn phía màn) vs NEW-21 (API) · NEW-15 (UI biên) vs NEW-22 (API biên) · NEW-10 (đổi tên lưu được) vs NEW-12 (đổi tên không đổi cờ) · NEW-2 vs NEW-3 (NEW-3 không reload giữa các lượt).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check | Expected của TC | Nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | CONF-SPEC | NEW-15, NEW-22 | 管理名 11 ký tự gửi lên server | Server chặn, trả 「管理名は10文字以下にしてください。」 | `feature-spec.md` §7 Field Traceability dòng 1: "UI ép 10 ký tự; DB `varchar(100)`, **server không ép**" | TC sai / spec cũ hơn #40050 (Dev: `max:10` đã có ở server) → cần update spec | [MAJOR] | Dev |
| C2 | CONF-SPEC | NEW-23 | Bot A gọi `POST /{id}/edit` với id lịch của bot B | Bị từ chối 403, cờ lịch bot B không đổi | `feature-spec.md` §11.1 A-02: "Route nằm ngoài `checkLessonCalendarInBot` … không lọc `bot_id`, không validate trường nào" | TC sai / spec cũ hơn bản hiện tại (Dev: `checkCalendarBelongBot` ở `CalendarManagementService::editCalendar`) → cần update spec | [MAJOR] | Dev |

**Đã rà**: 25 TC × `spec-features/admin/lesson-booking/feature-spec.md` (§7, §8.5 BR-P01, §11.1) + `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (nhóm Màn list calendar, Wizard tạo, Đồng thời & verify API, MT-01/02/16). Không phát hiện `CONF-TC` / `CONF-KHO`: NEW-17 khớp TC-LSN-12 + BR-P01 (「この予約は現在利用できません。」); NEW-15 khớp TC-LSN-15 (báo lỗi, không tự cắt).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | [BLOCKER] | Toàn bộ 25 TC | 0/25 TC có kết quả (0% pass). `envAuto.local.runs = 1` nhưng không TC nào có `last_exec`. Dev tự verify mới ở mức lint, ghi rõ "CHƯA bấm tay end-to-end" | Chạy toàn bộ trên nhánh fix trước khi đóng ticket; chưa được kết luận Fix done |
| I2 | [MAJOR] | Studio task #343 — `spec_delta` | Diff tính trên branch `release_staging_20260910`: 16 file, chỉ 2 file thuộc #41772; 14 file còn lại (`CalendarSalonLineBookingService`, `Mobile/CalendarSalonController`, 2 job salon, `SalesManagement*`, 3 header blade, `config/sns-line.php`, 4 test) thuộc ticket khác. Nhánh fix Dev ghi là `ai_fixbug_41772` (gốc `release_step_20260930`) | Leader xác nhận branch của task Studio. Hỏi Dev: `config/sns-line.php` + 3 header blade có phải bump version asset không — nếu có thì tiền đề NEW-9 ("fix không bump version, JS còn cache") không còn đúng |
| I3 | [MAJOR] | NEW-22 | RULE-13: expected ghi "Ghi lại HTTP status thực tế … chỉ coi status code là contract nếu source/spec xác nhận" — không có mã HTTP cụ thể | Sửa trên Studio: 10 ký tự → 200; 11 ký tự → 422 (giá trị vi phạm validation nghiệp vụ). Code đang trả 400 thì ghi ở Ghi chú + báo Dev, không sửa expected theo code |
| I4 | [MAJOR] | NEW-2/3 (FUNC-001), NEW-4/5 (COMPAT-LEGACY-001), NEW-7 (DATA-DB-001), NEW-17/18/19/26 (DATA-001), NEW-9 (DEPLOY-ASSET-001), NEW-23 (PERM-002) | RULE-01: quan điểm Cao thiếu 1–2 loại case, không ghi lý do (vd FUNC-001 không có Boundary vì toggle 0/1 — hợp lý nhưng chưa ghi) | Ghi lý do thiếu loại case vào `note` trên Studio; phần thiếu thật (PERM-001, OUT-TRUTH-001) đã lấp ở §7 |
| I5 | [MAJOR] | NEW-18, NEW-19 | Steps không đủ dựng lại: "thêm một thành phần có gắn hành động (ví dụ nút hoặc ảnh có liên kết)", "Mở màn tạo hoặc sửa Step có thể gán hành động" — không nêu loại tin nhắn mẫu, đường vào, tên action | Ghi cụ thể loại tin nhắn mẫu + tên lựa chọn action + đường vào màn Step |
| I6 | [MINOR] | NEW-8 | Tiền đề phải sửa `bot_id` trực tiếp trong DB → chỉ chạy được local, thực chất là ca cross-bot đã có ở NEW-23 | Giữ làm trigger #1, bổ sung trigger tái hiện được bằng thao tác màn hình (§7 TC-OUTTRUTH001-01..03) |
| I7 | [NIT] | NEW-26 | Gọi tên "App Flutter" | Đổi thành "App mobile" cho thống nhất tên gọi |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 25 TC — không có TC nào ngoài phạm vi task. Các TC dễ bị nghi thừa đều dẫn được từ Studio `dev_impact` / requirements: NEW-24 (Salon — đối chứng REQ-010, endpoint sinh đôi Dev nêu ở mục 3) · NEW-25 (tạo lịch — rủi ro hồi quy "không được vỡ luồng tạo lịch") · NEW-6 (quyền — loại giả thuyết 操作権限 của khách) · NEW-9 (cache JS — REQ-011).

---

## 7. TCs đề xuất bổ sung (14)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (nhóm 1, 2, 3, 30, 33, 36, 40, 47, 48, 49 + MT-01/02/05/16) |
| Vùng regression phát hiện từ kho | TC-LSN-12 (OFF → chặn cả URL booking và URL lịch sử) → chiều ngược lại dùng cho G4 · TC-LSN-612 (mass assignment `POST /{id}/edit`) → G2 · TC-LSN-05/06/07 (popup sắp xếp) → G7 |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | G7 (phần thứ tự): dùng lại TC-LSN-05 "Popup sắp xếp: đổi vị trí bằng nút rồi Lưu", TC-LSN-06 "đổi vị trí bằng drag&drop rồi Lưu", TC-LSN-07 "đổi vị trí nhưng KHÔNG lưu → thứ tự giữ nguyên" — chạy nguyên văn, không cần chỉnh. 4 TC mới dưới đây chỉ phủ phần kho chưa có: sắp xếp không được đổi trạng thái 有効/無効 + 管理名. G2: TC-LSN-612 chỉ test lịch bot khác, không test payload thiếu `calendar_name` trên lịch cùng bot → vẫn viết mới |
| Căn cứ TC regression `R<x>` | Không có TC R — rủi ro hồi quy Studio (modal 管理名, 店舗名 trống, luồng tạo lịch) đều đã có TC |
| Xác nhận chống trùng | Đã đối chiếu 25 TC ở BƯỚC 0 + kho — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC003-01 | API | FUNC-003 | Đồng thời & verify API | Abnormal | auto | Tất cả | Gọi cập nhật lịch lesson với giá trị cờ trạng thái lạ hoặc body rỗng thì bị từ chối và trạng thái không đổi | Phiên đăng nhập admin hợp lệ (cookie + CSRF) đang chọn bot A. Lịch lesson 「TC41772値」 của bot A đang 無効, biết id | 1. Gửi POST /basic/calendar-management/{id}/edit, body chỉ có enable_use_calendar=abc. Ghi mã HTTP<br>2. Gửi lại với enable_use_calendar=2. Ghi mã HTTP<br>3. Gửi lại với body không có trường nào (chỉ CSRF). Ghi mã HTTP<br>4. Mở màn レッスン予約（一覧）, tải lại, xem trạng thái lịch<br>5. LINE user là bạn của bot A mở URL đặt lịch của lịch này | enable_use_calendar=abc · enable_use_calendar=2 · body rỗng | Lượt 1: 400. Lượt 2: 422. Lượt 3: 400 hoặc 422, không trả 200. Sau cả 3 lượt: lịch vẫn hiển thị 無効 trên màn danh sách và LINE user vẫn thấy 「この予約は現在利用できません。」 — không có trạng thái lửng (màn admin hiện 有効 nhưng khách không đặt được) |  | Lấp G1 · RULE-13 (enum lạ / thiếu tham số không được điền mặc định) · Đánh giá spec: Spec không ghi — spec §7 chỉ nêu enum 0/1 · Evidence: response HTTP + screenshot màn danh sách + màn LIFF |
| TC-SEC002-01 | API | SEC-002 | Đồng thời & verify API | Abnormal | auto | Tất cả | Gọi cập nhật lịch lesson cùng bot, body chỉ có cờ trạng thái kèm trường nhạy cảm, không có tên quản lý thì server không ghi các trường ngoài cờ | Phiên admin bot A. Lịch 「TC41772項目」 của bot A đang 無効, chưa bật 決済連携, chưa liên kết Google スプレッドシート. Có bot B cùng tài khoản để quan sát | 1. Ghi lại trạng thái hiện tại của lịch: 管理名, trạng thái 決済連携, liên kết スプレッドシート, lịch đang nằm ở bot A<br>2. Gửi POST /basic/calendar-management/{id}/edit với body gồm enable_use_calendar=1, is_use_payment=1, bot_id=id bot B, code_delete=x, google_sheet_access_token=x (không có calendar_name)<br>3. Ghi mã HTTP<br>4. Mở màn レッスン予約（一覧） của bot A, tải lại<br>5. Mở tab 決済連携 và phần liên kết スプレッドシート của lịch<br>6. Chuyển sang bot B, mở màn レッスン予約（一覧） | Body: enable_use_calendar=1 + 4 trường ngoài | Phản hồi 200 chỉ khi server bỏ qua trường ngoài, hoặc 400/422 từ chối cả request. Trong mọi trường hợp: lịch vẫn nằm ở bot A và KHÔNG xuất hiện ở bot B; 決済連携 vẫn tắt; không phát sinh liên kết スプレッドシート; 管理名 không đổi. Nếu phản hồi 200 thì lịch chuyển 有効, nếu bị từ chối thì vẫn 無効 |  | Lấp G2 · Dẫn từ kho TC-LSN-612 (bản kho chỉ test lịch bot khác) + spec §11.1 A-02 · ⚠️ Dự kiến FAIL nếu code vẫn update toàn bộ request — lỗi có sẵn, nhưng fix #41772 bỏ yêu cầu kèm calendar_name nên cần Dev xác nhận có whitelist không · Đánh giá spec: Spec ghi rõ (A-02) · Evidence: response + screenshot 2 bot + tab 決済連携 |
| TC-OUTTRUTH001-01 | UI | OUT-TRUTH-001 | Màn list calendar | Abnormal | auto | Tất cả | Bấm bật/tắt lịch sau khi phiên đăng nhập đã hết thì không lật trạng thái trong im lặng | Tab A mở màn レッスン予約（一覧） bot A, lịch 「TC41772失効」 đang 無効, đã hard-reload. Tab B cùng trình duyệt | 1. Ở tab B, đăng xuất khỏi LME<br>2. Quay lại tab A (không tải lại), bấm nút bật/tắt của lịch 「TC41772失効」<br>3. Quan sát thông báo / màn hình sau khi loading tắt<br>4. Đăng nhập lại, mở màn danh sách, xem trạng thái lịch | Lịch 「TC41772失効」 · phiên đã đăng xuất | Hiện thông báo lỗi hoặc chuyển sang màn đăng nhập — không được đứng yên với nút đã lật về 無効 mà không nói gì. Thông báo không rỗng, không hiện chữ undefined. Sau khi đăng nhập lại: lịch vẫn 無効 |  | Lấp G3 (trigger 2/4 — phiên hết hạn) · generic-fix · Đánh giá spec: Spec không ghi · Evidence: screenshot thông báo + trạng thái sau đăng nhập lại |
| TC-OUTTRUTH001-02 | UI | OUT-TRUTH-001 | Màn list calendar | Abnormal | auto | Tất cả | Bấm bật/tắt lịch khi mất kết nối mạng thì có thông báo và nút về đúng trạng thái đang lưu | Màn レッスン予約（一覧） bot A đã mở, lịch 「TC41772通信」 đang 無効, đã hard-reload | 1. Bật chế độ Offline của trình duyệt (DevTools > Network > Offline)<br>2. Bấm nút bật/tắt của lịch 「TC41772通信」<br>3. Quan sát thông báo và nút sau khi loading tắt<br>4. Tắt Offline, tải lại màn danh sách | Lịch 「TC41772通信」 · mạng Offline | Có thông báo lỗi (nội dung chung chung vẫn chấp nhận, nhưng không rỗng / không undefined), loading không treo vô hạn, nút về 無効. Sau khi có mạng và tải lại: lịch vẫn 無効 |  | Lấp G3 (trigger 3/4 — không có phản hồi server, kiểm fallback của showLessonAjaxError) · generic-fix · Đánh giá spec: Spec không ghi · Evidence: screenshot thông báo + nút |
| TC-OUTTRUTH001-03 | UI | OUT-TRUTH-001 | Màn list calendar | Abnormal | auto | Tất cả | Bấm bật/tắt lịch đã bị xóa ở tab khác thì hiện thông báo không tìm thấy lịch | Bot A có lịch 「TC41772削除」 (không có booking) đang 無効. Tab A mở sẵn màn レッスン予約（一覧）, đã hard-reload | 1. Ở tab B, xóa lịch 「TC41772削除」 bằng chức năng 予約システムの削除<br>2. Quay lại tab A (không tải lại), bấm nút bật/tắt của lịch đó<br>3. Quan sát thông báo và nút<br>4. Tải lại tab A | Lịch 「TC41772削除」 đã xóa ở tab khác | Hiện 「カレンダーが見つかりません。」 (hoặc thông báo lỗi tương đương từ server), nút về 無効. Sau khi tải lại, lịch không còn trong danh sách |  | Lấp G3 (trigger 4/4 — dữ liệu không tồn tại, tái hiện được không cần sửa DB như NEW-8) · generic-fix · Đánh giá spec: Spec không ghi · Evidence: screenshot thông báo |
| TC-LIFFENTRY001-01 | UI | LIFF-ENTRY-001 | LINE user — mở link & entry | Normal | auto | Tất cả | Sau khi bật lại lịch, LINE user mở URL đặt lịch và URL lịch sử đặt lịch vào được bình thường | Bot A có lịch 「TC41772LIFF」 đang 無効, có 1 コース đang ON và 受付枠 trong tuần. LINE user U1 là bạn của bot A, đã từng đặt 1 lần ở lịch này. Lấy URL 予約ページ và URL lịch sử từ màn danh sách | 1. U1 mở URL 予約ページ trong app LINE — ghi nhận màn hiển thị<br>2. Admin bật lịch 「TC41772LIFF」 sang 有効 ở màn レッスン予約（一覧）, tải lại xác nhận 有効<br>3. U1 mở lại URL 予約ページ trong app LINE<br>4. U1 chọn コース và mở được danh sách 受付枠<br>5. U1 mở URL lịch sử đặt lịch | Lịch 「TC41772LIFF」 · U1 đã có 1 booking | Bước 1: 「この予約は現在利用できません。」. Bước 3–4: vào màn chọn コース, chọn được コース và thấy 受付枠 — không có dòng 「この画面はプレビューとなります。」. Bước 5: xem được lịch sử, có booking cũ của U1 |  | Lấp G4 · Q3 · regression — chiều ngược của kho TC-LSN-12 · RULE-06 output cuối ở phía LINE user, không dùng preview admin · Đánh giá spec: Spec ghi rõ (BR-P01) · Evidence: screenshot trên LINE app bước 1 / 3 / 5 |
| TC-DATA001-01 | UI | DATA-001 | Add link booking vào tin nhắn | Normal | auto | Tất cả | Sau khi bật lại lịch, lịch xuất hiện lại trong danh sách chọn lịch khi thiết lập hành động cho richmenu | Bot A có lịch 「TC41772RM」 đang 無効 | 1. Mở màn tạo richmenu, chọn 1 vùng bấm, chọn loại hành động mở trang đặt lịch レッスン予約, mở danh sách chọn lịch — tìm 「TC41772RM」<br>2. Thoát không lưu<br>3. Bật 「TC41772RM」 sang 有効 ở màn レッスン予約（一覧）<br>4. Lặp lại bước 1 và chọn 「TC41772RM」, lưu richmenu | Lịch 「TC41772RM」 | Bước 1: 「TC41772RM」 không có trong danh sách. Bước 4: 「TC41772RM」 có trong danh sách, chọn và lưu được |  | Lấp G5 · Input thiếu: Dev chưa nêu màn nào dùng init-data UserController:797 / :3060 — TC viết theo richmenu vì Studio REQ-009 nêu; Dev xác nhận nếu còn màn action khác thì bổ sung · Đánh giá spec: Spec không ghi · Evidence: screenshot danh sách chọn lịch 2 lượt |
| TC-CONC001-01 | UI | CONC-001 | Màn list calendar | Abnormal | auto | Tất cả | Đổi tên quản lý trên trang mở từ trước không ghi đè trạng thái 有効 vừa bật ở tab khác | Lịch 「TC41772並行」 đang 無効. Tab A và tab B cùng mở màn レッスン予約（一覧） bot A, đã hard-reload | 1. Ở tab B, bật 「TC41772並行」 sang 有効, tải lại tab B xác nhận 有効<br>2. Ở tab A (không tải lại, nút vẫn hiện 無効), mở modal カレンダー管理名 変更 của lịch đó, đổi tên, bấm 保存<br>3. Tải lại cả 2 tab | Tên mới: 「TC41772並行2」 | Bước 2 lưu tên thành công. Sau khi tải lại: tên là 「TC41772並行2」 và lịch vẫn 有効 — lượt lưu tên không đưa lịch về 無効 |  | Lấp G6 · Q1 (kịch bản 3: 2 người sửa 2 field khác nhau của 1 bản ghi) · Studio REQ-006 · Đánh giá spec: Spec không ghi · Evidence: screenshot 2 tab trước/sau |
| TC-CONC001-02 | UI | CONC-001 | Màn list calendar | Abnormal | auto | Tất cả | Bấm nút bật/tắt 2 lần liên tiếp thật nhanh thì trạng thái hiển thị khớp trạng thái đã lưu | Lịch 「TC41772連打」 đang 無効, đã hard-reload màn レッスン予約（一覧） | 1. Bấm nút bật/tắt của 「TC41772連打」 2 lần liên tiếp nhanh nhất có thể (không chờ loading)<br>2. Chờ loading tắt, ghi lại trạng thái trên màn<br>3. Tải lại màn danh sách | Lịch 「TC41772連打」 · double-click | Trạng thái ở bước 2 và sau khi tải lại phải giống nhau (có 無効 hoặc 有効 đều được, miễn khớp). Không có thông báo lỗi giả |  | Lấp Q1 (kịch bản 1: double-click) · Đánh giá spec: Spec không ghi · Evidence: screenshot trước/sau tải lại |
| TC-PERM001-01 | API | PERM-001 | Phân quyền & môi trường | Abnormal | auto | Tất cả | Nhân viên không có quyền レッスン予約 gọi bật/tắt lịch thì bị từ chối và trạng thái không đổi | Tài khoản staff S1 của bot A KHÔNG được cấp quyền レッスン予約. Lịch 「TC41772権限外」 của bot A đang 無効, biết id | 1. Đăng nhập S1, xác nhận không vào được màn レッスン予約（一覧）<br>2. Trong phiên S1, gửi POST /basic/calendar-management/{id}/edit, body chỉ có enable_use_calendar=1. Ghi mã HTTP<br>3. Đăng nhập admin, mở màn danh sách xem trạng thái lịch | Body: enable_use_calendar=1 | Bước 1: không vào được màn. Bước 2: 403. Bước 3: lịch vẫn 無効 |  | Lấp Q2 · RULE-01 cho PERM-001 · Đánh giá spec: Spec không ghi · Evidence: response + screenshot trạng thái |
| TC-FUNCSEQ001-01 | UI | FUNC-SEQ-001 | Màn list calendar | Normal | auto | Tất cả | Sắp xếp lại lịch thì chỉ đổi thứ tự, trạng thái 有効/無効 và 管理名 của từng lịch giữ nguyên | Bot A có 3 lịch lesson theo thứ tự: 「TC41772並A」 đang 有効, 「TC41772並B」 đang 無効, 「TC41772並C」 đang 有効. Đã hard-reload màn レッスン予約（一覧） | 1. Ghi lại thứ tự, trạng thái 有効/無効 và 管理名 của 3 lịch<br>2. Bấm nút sắp xếp để mở popup sắp xếp<br>3. Dùng nút mũi tên đưa 「TC41772並C」 lên đầu, bấm Lưu<br>4. Tải lại màn danh sách | Thứ tự mới: 「TC41772並C」 lên đầu | Sau khi tải lại: thứ tự là 「TC41772並C」, 「TC41772並A」, 「TC41772並B」. 「TC41772並A」 vẫn 有効, 「TC41772並B」 vẫn 無効, 「TC41772並C」 vẫn 有効. 管理名 của cả 3 lịch KHÔNG đổi |  | Lấp G7 · Q4 · regression — Dev mục 3: sort dùng chung CalendarManagementRepository::editCalendar với nút 有効/無効 · phần thứ tự đã có ở kho TC-LSN-05, TC này chỉ thêm kiểm trạng thái + tên · Đánh giá spec: Spec không ghi · Evidence: screenshot màn danh sách trước/sau |
| TC-FUNCSEQ001-02 | UI | FUNC-SEQ-001 | Màn list calendar | Normal | auto | Tất cả | Bật lịch rồi sắp xếp ngay trên cùng màn (không tải lại) thì lịch vừa bật giữ 有効 ở vị trí mới | Bot A có 3 lịch: 「TC41772並A」 有効, 「TC41772並B」 無効, 「TC41772並C」 有効, theo đúng thứ tự đó. Đã hard-reload màn レッスン予約（一覧） | 1. Bấm nút bật/tắt của 「TC41772並B」 để chuyển sang 有効, chờ loading tắt<br>2. KHÔNG tải lại, bấm nút sắp xếp để mở popup<br>3. Đưa 「TC41772並B」 lên đầu, bấm Lưu<br>4. Tải lại màn danh sách | Chuỗi thao tác: bật 「TC41772並B」 → sắp xếp đưa 「TC41772並B」 lên đầu | Sau khi tải lại: 「TC41772並B」 đứng đầu và đang 有効 — lượt lưu sắp xếp không đưa lịch về 無効. 2 lịch còn lại giữ nguyên trạng thái 有効 |  | Lấp G7 · Q4 (2 thao tác nối tiếp trên cùng danh sách có Sort) · Đánh giá spec: Spec không ghi · Evidence: screenshot sau từng bước + sau tải lại |
| TC-FUNCSEQ001-03 | UI | FUNC-SEQ-001 | Màn list calendar | Normal | auto | Tất cả | Sắp xếp lịch rồi bật lịch ngay trên cùng màn (không tải lại) thì thứ tự vừa lưu không bị đổi lại | Bot A có 3 lịch: 「TC41772並A」 有効, 「TC41772並B」 無効, 「TC41772並C」 有効, theo đúng thứ tự đó. Đã hard-reload màn レッスン予約（一覧） | 1. Mở popup sắp xếp, đưa 「TC41772並B」 lên đầu, bấm Lưu<br>2. KHÔNG tải lại, bấm nút bật/tắt của 「TC41772並B」 để chuyển sang 有効, chờ loading tắt<br>3. Tải lại màn danh sách | Chuỗi thao tác: sắp xếp đưa 「TC41772並B」 lên đầu → bật 「TC41772並B」 | Sau khi tải lại: thứ tự là 「TC41772並B」, 「TC41772並A」, 「TC41772並C」 và 「TC41772並B」 đang 有効 — lượt bật/tắt không làm thứ tự quay về như cũ |  | Lấp G7 · Q4 (chiều ngược của TC-FUNCSEQ001-02) · Đánh giá spec: Spec không ghi · Evidence: screenshot sau tải lại |
| TC-CONC001-03 | UI | CONC-001 | Màn list calendar | Abnormal | auto | Tất cả | Sắp xếp trên trang mở từ trước không ghi đè trạng thái 有効 vừa bật ở tab khác | Bot A có 3 lịch: 「TC41772並A」 有効, 「TC41772並B」 無効, 「TC41772並C」 有効. Tab A và tab B cùng mở màn レッスン予約（一覧） bot A, đã hard-reload | 1. Ở tab B, bật 「TC41772並B」 sang 有効, tải lại tab B xác nhận 有効<br>2. Ở tab A (KHÔNG tải lại, 「TC41772並B」 vẫn hiện 無効), mở popup sắp xếp, đưa 「TC41772並C」 lên đầu, bấm Lưu<br>3. Tải lại cả 2 tab | Lịch bật ở tab khác: 「TC41772並B」 · Thứ tự mới: 「TC41772並C」 lên đầu | Bước 2 lưu thành công. Sau khi tải lại cả 2 tab: thứ tự là 「TC41772並C」, 「TC41772並A」, 「TC41772並B」 và 「TC41772並B」 vẫn 有効 — lượt sắp xếp trên trang cũ không đưa lịch về 無効 |  | Lấp G7 · Q1 (kịch bản 3: 2 người sửa 2 field khác nhau của 1 bản ghi) · cùng dạng rủi ro với TC-CONC001-01 nhưng đi qua caller sort · Đánh giá spec: Spec không ghi · Evidence: screenshot 2 tab trước/sau |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/lesson-booking/feature-spec.md` §7 Field Traceability dòng 1 (「エルメ上での管理名」) | "server không ép" → server `sometimes\|required\|max:10` + chặn trùng 管理名 trong bot (#40050, #41104, #41772) | C1 CONF-SPEC | Dev |
| 2 | `feature-spec.md` §11.1 TOP 12 — A-02 | Cập nhật: đã có `checkCalendarBelongBot` (chặn cross-bot) và validate `calendar_name`; còn mở hay đã đóng phần mass assignment (chờ kết quả TC-SEC002-01) | C2 CONF-SPEC | Dev |
| 3 | `kho-tcs/fa019-…` MT-16 + TC-LSN-612 | Cập nhật ghi chú "DỰ KIẾN FAIL" theo trạng thái code hiện tại sau khi chạy NEW-23 + TC-SEC002-01 | §7 G2 (không phải mâu thuẫn expected) | Leader |
