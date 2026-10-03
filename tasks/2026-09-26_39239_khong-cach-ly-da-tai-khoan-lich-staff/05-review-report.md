# 05 — Review Report

> Draft cho Leader verify. Ticket #39239 · Studio task #264 (round 1) · review 2026-09-28.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #264 (ticket 39239, branch `ai_fixbug_39239`) |
| Tổng số TC review | 21 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 10/10 mục có TC (BUG · F1–F5 · D1–D2 · T1–T2) — **ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (5 file, +40/−5) | 17/18 điểm có TC — **CHƯA ĐỦ** |

**Kết luận**: 27/28 vùng ảnh hưởng đủ TC · 1 GAP · 0 RISK.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Rủi ro hồi quy Studio nêu đích danh: "luồng same-tenant hợp lệ (chủ bot / **staff được mời có quyền**) phải sửa/xoá được như cũ". Nhánh **sửa lịch**: cổng mới `checkCalendarBelongBot` so với `getBotId()` của phiên → staff được mời đang chọn bot B phải vẫn sửa được lịch của bot B | `diff code` | NEW-1, NEW-2 (chỉ chủ bot) · NEW-11 (staff nhưng là nhánh **xoá staff**) | GAP — 0 TC cho staff được mời sửa lịch lesson. Kho TC-LSN-623 (staff thao tác màn レッスン予約) không có bước sửa 管理名 | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 14 quan điểm Trigger khớp task · 3 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `DATA-DB-001` | Cao | Không TC nào mang mã này. Nội dung "kiểm WHERE scope trên 2 tài khoản + query DB bot B" **đã có đủ** ở NEW-3 / NEW-13, nhưng 2 TC này gắn mã Studio `TOOL-KNOW-002` → theo quy tắc tính là chưa cover. **BLOCKER hình thức** — chỉ cần đổi mã quan điểm của NEW-3, NEW-13 sang `DATA-DB-001` trên Studio, không cần TC mới | `[BLOCKER]` |
| Q2 | `REG-SHARED-001` | Cao | RISK — Dev ghi "quét ngang còn **6** chỗ cùng kiểu chưa kiểm sở hữu" (mục 2) nhưng phần rủi ro lại ghi "còn **4** điểm", **không có danh sách**. Quan điểm yêu cầu Dev cung cấp danh sách rồi test từng nơi. Hiện chỉ NEW-8 ghi nhận 1 sibling (sort lịch). 2 sibling Dev nêu tên và spec có endpoint (sắp xếp nhân viên EP-14 · cài đặt hiển thị đặt lịch EP-19) chưa có TC; sibling "xoá nhân viên chưa đồng ý" không tra được endpoint trong spec | `[MAJOR]` |
| Q3 | `FUNC-001` · `CONC-001` · `PERM-001` · `PERM-002` · `PERM-003` · `SEC-001` | Cao | RULE-01 — mỗi mã chỉ có 1 loại case và không TC nào ghi lý do thiếu: FUNC-001 chỉ Normal (NEW-1, NEW-10) · CONC-001 chỉ Abnormal (NEW-5, NEW-17) · PERM-001 chỉ Normal (NEW-11) · PERM-002 chỉ Abnormal (NEW-15, NEW-20) · PERM-003 chỉ Abnormal (NEW-4, NEW-14, NEW-19) · SEC-001 chỉ Abnormal (NEW-6). Về nội dung, Abnormal/Boundary của luồng sửa/xoá đã có ở NEW-3/7/9/13/16/18 nhưng dưới mã khác → đề xuất ghi lý do vào `note` Studio hoặc đổi mã; phần Normal thật sự thiếu của PERM-001 (sửa lịch) lấp bằng G1 | `[MAJOR]` |

**Đã loại khỏi phạm vi** (Trigger khớp theo tính năng nhưng không có bằng chứng bị chạm):
- `SYNC-APP-001` — app admin di động FA-019 có 15 endpoint `EP-M01…M15`, **không có** endpoint sửa lịch (spec lesson-booking §9.5); FA-035 không có endpoint app.
- `JOB-001` · `ENV-003` · `REG-RUN-001` — `spec_delta.files` chỉ có 5 file PHP, job nền chạy bên Java không bị chạm.
- `DEPLOY-ASSET-001` · `DEPLOY-LIVE-001` — không đổi JS/CSS, không đổi payload request.
- `INTG-CAL-001` — `calendar_management.google_calendar_id` là **cột chết**, 174/174 NULL; FA-019 không tích hợp Google Calendar (spec lesson-booking `db/db-mapping.md:30`). `INTG-SHEET-001` — token Google Sheet không bị chạm.
- `LIFF-ENTRY-001` / `OUT-*` — tắt 利用 lịch → LIFF bị chặn là nhánh đọc, không đổi code (kho TC-LSN-12 đã cover).
- `PERM-004` — "session đang mở của staff bị xoá còn thao tác được không" là hành vi có sẵn, fix không chạm nhánh đó; nhánh tự xoá chính mình đã có NEW-12.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-3 | NEW-19 → **gộp** | DUP-SUBSET | Cross-bot (A sửa lịch bot B) × Abnormal × `POST /{id}/edit` với id lịch bot B × tiền đề 2 tài khoản độc lập → bị từ chối, DB bot B không đổi. Chỉ khác **trường gửi lên** (`google_calendar_id` thay cho tên). Cổng kiểm đặt **trước** câu UPDATE nên mọi trường đi cùng 1 nhánh; thêm nữa `google_calendar_id` là cột chết của FA-019 | `[MINOR]` |
| DUP-2 | NEW-10 | NEW-21 → **gộp** | DUP-SUBSET | Chủ bot × Normal × xoá nhân viên hợp lệ của bot mình × cùng tiền đề → thành công, danh sách nạp lại không còn dòng đó. NEW-21 chỉ thêm 1 assertion `status=true` | `[MINOR]` |

- **Gate đã chạy**: xoá NEW-19 → D1 + PERM-003 vẫn có NEW-3, NEW-4, NEW-14; xoá NEW-21 → REQ-009 phía xoá staff còn NEW-10. Không mất cover nhưng mỗi TC bị gộp có 1 phần riêng → đề xuất **GỘP**, không xoá trắng:
  - NEW-3: mở rộng payload giống kho TC-LSN-612 (`bot_id`, `is_use_payment`, `environment`, `google_sheet_access_token`, `code_delete`, `google_calendar_id`), expected "bản ghi lịch bot B không đổi **bất kỳ** trường nào".
  - NEW-10: thêm vào expected "response `{"status": true}`".
- Không có `DUP-INFLATE`.
- Xoá/gộp thật do human thực hiện trên Studio (`testcase_update` + `testcase_delete`).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-11 (kéo theo NEW-12, NEW-20 dựa trên cùng giả định) | Staff được mời có quyền quản lý nhân viên xoá nhân viên của bot được mời | NEW-11: "Yêu cầu xoá được chấp nhận, số nhân viên của bot B giảm đúng 1" | `staff-management/feature-spec.md` **BR-004**: "Chỉ Admin mới truy cập được tính năng quản lý staff … Staff (role > 0) không có quyền truy cập các trang quản lý staff" | (1) TC + bản fix sai — chỉ admin chủ bot được xoá, `getListBotIdStaffManagement` mở rộng quá phạm vi · (2) spec BR-004 cũ/đọc sai code — thực tế quyền xét theo `checkBotHasPermission('staff-management.inviteStaff')` nên staff có quyền vẫn vào được → cần update BR-004. Chính `note` NEW-11 cũng tự nêu cần hỏi | `[MAJOR]` | Leader / PM |
| C2 | `CONF-SPEC` (chuẩn = RULE-13 · bảng mã HTTP mục 1.1 `checklist-lme.md`) | NEW-3, NEW-5, NEW-19 (cross-bot sửa lịch) · NEW-7 (lịch không tồn tại) · NEW-9, NEW-18 (id 0 / -1 / rỗng / "abc") | Mã HTTP khi bị từ chối | Lịch: **HTTP 200** + `success=false` cho cả cross-bot lẫn không tồn tại · NEW-9 chấp nhận "200 hoặc 404" · NEW-18: 403 cho cả id rỗng / "abc" | RULE-13: cross-bot / không tồn tại → **403 hoặc 404** · sai format/datatype (tham số rỗng, "abc") → **400**. Phía staff (NEW-13, NEW-15, NEW-16, NEW-17, NEW-20 trả 403) **đã khớp** | (1) TC ghi theo hành vi code Dev (TC viết 2026-08-28, trước quy ước) → sửa expected nhánh lịch về 403/404, code trả 200 thành bug Dev · (2) Leader quyết không áp hồi tố cho ticket đã đóng → giữ expected, ghi ngoại lệ. Lưu ý: màn lịch chỉ đọc `response.success`, đổi sang 403/404 thì FE phải sửa theo | `[MAJOR]` — áp hồi tố thì NEW-3 (case tái hiện bug gốc) thành `[BLOCKER]` | Leader / Dev |
| C3 | `CONF-SPEC` + `CONF-KHO` | NEW-1 (kéo theo NEW-5) | Độ dài ô 「エルメ上での管理名」 khi sửa lịch | NEW-1 nhập 「TC39239-A-LICH1-DAOI」 (20 ký tự) → "danh sách hiển thị ngay tên mới 「TC39239-A-LICH1-DAOI」" | `lesson-booking/feature-spec.md` §7 dòng 1: "「エルメ上での管理名」 — **UI ép 10 ký tự**; DB varchar(100), server không ép" · kho **TC-LSN-15**: 11 ký tự → báo lỗi / chặn gõ | (1) Dữ liệu TC sai — qua UI không gõ được quá 10 ký tự, NEW-1 pass trên local nghĩa là runner có thể đã bỏ qua UI · (2) Giới hạn 10 ký tự đã bị bỏ → cần update spec + kho. **Hệ quả ở NEW-5**: 「TC39239-STALE-TAB」 (17 ký tự) bị cắt còn 「TC39239-ST」, bước query DB tìm chuỗi 17 ký tự sẽ **không bao giờ thấy** kể cả khi tên thật đã bị lưu → nguy cơ **pass giả** cho case đổi hành vi | `[MAJOR]` | Leader |

**Đã rà**: 21 TC × `spec-features/admin/lesson-booking/` (§7, §8.10, §9.1–9.6, §11 A-02/A-08/A-23, `web/api-spec.md` EP-29/EP-30, `db/db-mapping.md`) + `spec-features/admin/staff-management/feature-spec.md` (luồng xoá staff EP-15, BR-004/007/010/011, EP-14) + `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (TC-LSN-12/13/15/612/623, MT-16/MT-63). **kho-tcs chưa có FA-035** (Quản lý nhân viên) — phía staff chỉ đối chiếu được với spec. Kho TC-LSN-612 (IDOR `POST /{id}/edit`) **không** mâu thuẫn với NEW-3 ở phần cross-bot — chỉ cần cập nhật trạng thái (§8).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn — phần xoá staff (NEW-10 → NEW-18, NEW-20, NEW-21) | Dev ghi phần xoá nhân viên **trùng nội dung với fix #38960** (branch `ai_fixbug_38960`), "khi gộp cần chọn một bản". 12 TC staff chỉ chạy trên branch `ai_fixbug_39239` → nếu release lấy bản #38960 thì kết quả pass này **không áp dụng** | Dev xác nhận bản nào lên release; chạy lại 12 TC staff trên đúng branch/release đã gộp |
| I2 | `[MAJOR]` | Nguồn — trạng thái ticket | Redmine #39239 **Closed** 2026-09-22 (đổi hàng loạt từ Dashboard, "Gom task → #41143") trong khi Studio `reviewState=leader`, `reviewed=false`; cả 21 TC chỉ chạy ở `local` bằng pipeline AI (run #2173), dev/staging/prd **0 run** | Leader xác nhận ticket gom #41143 là nơi theo dõi tiếp; TC fail ở vòng sau gắn vào #41143 |
| I3 | `[MAJOR]` | NEW-6 | Expected có 2 nhánh ("…Nếu kết quả thực tế ngược lại … báo leader") → không đo được Đạt/Không đạt. TC đang **pass** nhưng gắn **bug #40502** → 2 trạng thái trái nhau | Chốt 1 expected theo kho TC-LSN-612 ("bot_id không được đổi"). Nếu #40502 chính là bug bot_id bị ghi đè thì kết quả phải là Không đạt |
| I4 | `[MAJOR]` | NEW-8 | Expected lấy **lỗ hổng còn tồn tại** làm Đạt ("thứ tự lịch bot B BỊ ĐẢO"). Bảng Studio xanh 21/21 nhưng thực chất có 1 lỗ hổng IDOR ghi (spec EP-30) đang được đánh Đạt | Đổi expected về hành vi đúng (bị chặn, thứ tự giữ nguyên) và chấp nhận Không đạt + ticket riêng cho EP-30; hoặc gỡ khỏi bộ TC fix, chuyển thành ticket |
| I5 | `[MAJOR]` | NEW-19 | Expected "bị từ chối theo cơ chế permission hiện tại" không có mã HTTP/thông báo → không đo được. Tiền đề "lịch bot B đã liên kết google_calendar_id" **không dựng được qua UI** (cột chết) | Gộp vào NEW-3 theo DUP-1 |
| I6 | `[MINOR]` | NEW-17 | Expected lẫn đoạn "Ghi nhận thêm về trải nghiệm: tab 2 chỉ tắt vòng quay chờ…" không phải điều kiện Đạt → TC không atomic | Chuyển đoạn UX sang `note`; nếu Leader muốn sửa UX thì mở ticket riêng |
| I7 | `[MINOR]` | NEW-9 | Tiêu đề ghi "mã bằng 0, **bỏ trống** hoặc không phải số" nhưng steps/data là 0 · **-1** · "abc" (không có case bỏ trống). Expected chấp nhận 2 kết quả (200 fail hoặc 404) | Sửa tiêu đề khớp data; chốt 1 expected theo C2 |
| I8 | `[MINOR]` | Luồng xoá staff — BR-011 | `deleteStaffBot` đổi từ `destroy(id)` sang `$userStaff->delete()` trên bản ghi tìm theo phạm vi mới. Spec BR-011: xoá staff còn **huỷ Firebase topic** cho thiết bị của staff (app admin di động). `dev_impact` không nhắc, không TC nào kiểm | Dev xác nhận nhánh unsubscribe Firebase vẫn chạy với `$userStaff` mới. Không đẻ TC (cần thiết bị thật, nhánh không đổi logic) |
| I9 | `[NIT]` | NEW-2 | Tiêu đề "Bật rồi tắt" nhưng steps là tắt rồi bật | Sửa tiêu đề |
| I10 | `[NIT]` | NEW-9, NEW-18 | Dùng `DATA-ID-001` (Trigger: đối tượng **trùng tên**) cho biên mã định danh — lệch nghĩa mã | Cân nhắc `FUNC-003` (field có định dạng quy định) |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 21 TC — không có TC nào ngoài phạm vi task.

- NEW-8 (sort lịch cross-bot) dẫn từ `dev_impact` ("repo `editCalendar` cũ giữ cho luồng `/sort`") → không phải TC thừa; vấn đề expected ghi ở I4.
- NEW-6 (thăm dò ghi đè `bot_id`) đi qua đúng endpoint đã sửa (F1) + spec A-02 mass assignment → trong phạm vi; vấn đề expected ghi ở I3.

---

## 7. TCs đề xuất bổ sung (3)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (nhóm Màn list calendar · Đồng thời & verify API · Phân quyền & môi trường · App mobile) · kho-tcs chưa có FA-035 — phía staff không đối chiếu được |
| Vùng regression phát hiện từ kho | TC-LSN-13 (đổi 管理名 ≈ NEW-1) · TC-LSN-612 (IDOR `/{id}/edit` ≈ NEW-3, dùng payload cho DUP-1) · TC-LSN-05/06 (sort lịch cùng bot — luồng `/sort` dùng repo cũ không đổi code, không cần chạy lại) · TC-LSN-623 (staff thao tác màn レッスン予約 — không có bước sửa lịch nên G1 viết mới) |
| Conflict expected vs kho | Không phát sinh từ TC đề xuất. C3 (TC-LSN-15 vs NEW-1) đã đưa §4 + §8 |
| GAP dùng lại TC kho (không viết mới) | Không |
| Căn cứ TC regression `R<x>` | Không có TC R |
| Xác nhận chống trùng | Đã đối chiếu 21 TC ở BƯỚC 0 + kho FA-019 — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERM001-01 | UI | PERM-001 | Màn list calendar | Normal | auto | Tất cả | Staff được mời có quyền レッスン予約 đổi 管理名 lịch của bot được mời vẫn lưu thành công sau khi thêm cổng kiểm lịch thuộc bot | - Tài khoản B sở hữu bot B, bot B có lịch lesson 管理名 「B39239」<br>- Tài khoản C được B mời vào bot B với vai trò có quyền route レッスン予約, đã chấp nhận lời mời<br>- C không sở hữu bot nào khác có lịch lesson<br>- Dùng 2 phiên đăng nhập riêng (1 cửa sổ thường + 1 cửa sổ ẩn danh) cho C và B | 1. Phiên C: đăng nhập tài khoản C, chọn bot B ở thanh chọn bot, mở 予約管理 > レッスン予約<br>2. Bấm tên lịch 「B39239」 mở hộp thoại sửa<br>3. Xoá tên cũ, nhập 管理名 mới, bấm 保存<br>4. Quan sát hộp thoại và dòng lịch trên danh sách<br>5. Tải lại trang, quan sát lại dòng lịch<br>6. Phiên B: đăng nhập tài khoản B, chọn bot B, mở màn danh sách lịch lesson | 管理名 mới: 「C編集39239」 (9 ký tự, dưới giới hạn 10 ký tự của ô) | - Bước 4: hộp thoại đóng, không hiện 「この権限は許可されていません。」, dòng lịch hiện ngay 「C編集39239」<br>- Bước 5: sau khi tải lại vẫn là 「C編集39239」<br>- Bước 6: tài khoản B thấy lịch của bot B mang tên 「C編集39239」<br>- Các lịch khác của bot B giữ nguyên tên | | Lấp G1 · Lấp một phần Q3 (Normal của PERM-001 cho nhánh sửa lịch) · Căn cứ: Studio dev_impact "Rủi ro hồi quy: luồng same-tenant hợp lệ (chủ bot / staff được mời có quyền) phải sửa/xoá được như cũ" · Thiếu Abnormal/Boundary vì: nhánh từ chối của cổng đã có NEW-3, NEW-5; quyền route レッスン予約 (basic_access) không bị chạm code · Đánh giá spec: Spec không ghi (FA-019 BR-56 chỉ nói quyền staff xét theo tên route; kho MT-43 chưa chốt danh sách route) · Evidence: ảnh danh sách lịch ở 2 phiên C và B + DB calendar_management.calendar_name của lịch |
| TC-REGSHARED001-01 | API | REG-SHARED-001 | Quản lý nhân viên — sắp xếp thứ tự (並べ替え) | Abnormal | auto | Tất cả | Tài khoản A gửi yêu cầu lưu sắp xếp nhân viên bằng id dòng nhân viên của bot tài khoản B bị từ chối 403/404, thứ tự nhân viên bot B không đổi | - 2 tài khoản admin độc lập: A sở hữu bot A, B sở hữu bot B, không mời nhau<br>- Bot B có ≥ 3 nhân viên đã chấp nhận lời mời, đã ghi lại thứ tự hiển thị trong modal 並べ替え của bot B<br>- Dùng 2 phiên đăng nhập riêng cho A và B | 1. Phiên A: đăng nhập tài khoản A, mở màn quản lý nhân viên<br>2. Giữ phiên A, gửi yêu cầu lưu sắp xếp nhân viên (POST /admin/ajax/save-sort-staff) với ids = danh sách id dòng nhân viên của bot B theo thứ tự đảo ngược, bot_id = id bot B<br>3. Ghi lại mã HTTP và nội dung phản hồi<br>4. Phiên B: đăng nhập tài khoản B, mở màn quản lý nhân viên, chọn bot B, mở modal 並べ替え<br>5. Đối chiếu thứ tự nhân viên với thứ tự đã ghi ở tiền đề | ids: id thật các dòng nhân viên bot B, thứ tự ngược · bot_id: id bot B · phiên: tài khoản A | - Bước 3: HTTP 403 hoặc 404, không có trạng thái thành công<br>- Bước 5: thứ tự nhân viên bot B giống hệt trước khi A gửi yêu cầu | | Lấp Q2 · regression sibling cùng lớp lỗi · Căn cứ: Dev mục 2 liệt kê "sắp xếp nhân viên" trong các điểm chưa kiểm sở hữu; spec FA-035 EP-14 body { ids, bot_id } không kiểm bot thuộc người đăng nhập · NGOÀI PHẠM VI FIX #39239 — với code hiện tại kỳ vọng Không đạt; kết quả dùng để mở ticket riêng, KHÔNG chặn đóng #39239 · Mã 403/404 theo RULE-13 (quy ước mã HTTP) · Đánh giá spec: Spec không ghi · Evidence: request/response + ảnh modal 並べ替え bot B trước/sau |
| TC-REGSHARED001-02 | API | REG-SHARED-001 | 予約ページの表示設定 | Abnormal | auto | Tất cả | Tài khoản A gửi yêu cầu lưu cài đặt hiển thị trang đặt bằng id lịch lesson của bot tài khoản B bị từ chối 403/404, cài đặt của bot B không đổi | - 2 tài khoản admin độc lập: A sở hữu bot A có lịch lesson, B sở hữu bot B có lịch lesson 「B39239」<br>- Đã chụp màn 予約ページの表示設定 của lịch 「B39239」 (phiên B)<br>- Dùng 2 phiên đăng nhập riêng cho A và B | 1. Phiên A: đăng nhập tài khoản A, mở 予約ページの表示設定 của lịch bot A, đổi 1 tuỳ chọn hiển thị rồi bấm lưu để lấy mẫu yêu cầu<br>2. Gửi lại đúng yêu cầu đó nhưng thay id lịch trên đường dẫn (POST /basic/calendar-management/{calendarId}/setting-booking-display) bằng id lịch 「B39239」<br>3. Ghi lại mã HTTP và nội dung phản hồi<br>4. Phiên B: mở 予約ページの表示設定 của lịch 「B39239」, đối chiếu với ảnh chụp ở tiền đề<br>5. Phiên A: kiểm cài đặt hiển thị của lịch bot A vẫn là giá trị A vừa lưu ở bước 1 | calendarId: id thật lịch 「B39239」 · body: giống yêu cầu lưu hợp lệ của bot A | - Bước 3: HTTP 403 hoặc 404<br>- Bước 4: mọi tuỳ chọn hiển thị của lịch 「B39239」 giữ nguyên như ảnh chụp<br>- Bước 5: lịch bot A không bị ảnh hưởng | | Lấp Q2 · regression sibling cùng lớp lỗi · Căn cứ: Dev mục 2 liệt kê "cài đặt hiển thị đặt lịch" trong các điểm chưa kiểm sở hữu; spec FA-019 §11.2 A-08 "IDOR đọc/ghi cấu hình hiển thị trang đặt — route {calendarId} ngoài CLC" · NGOÀI PHẠM VI FIX #39239 — với code hiện tại kỳ vọng Không đạt; mở ticket riêng, KHÔNG chặn đóng #39239 · Mã 403/404 theo RULE-13 (quy ước mã HTTP) · Đánh giá spec: Spec ghi rõ (A-08 là lỗ hổng đã biết) · Evidence: request/response + ảnh màn 予約ページの表示設定 bot B trước/sau |

> Q1 (DATA-DB-001) và phần còn lại của Q3 (RULE-01) **không đề xuất TC mới** — nội dung đã có ở NEW-3/7/9/13/16/18, chỉ cần đổi mã / ghi lý do trên Studio.
> Sibling "xoá nhân viên chưa đồng ý" (Dev mục 2, JS `deleteUserStaffNotAgreed`) **chưa viết TC** — spec FA-035 không có endpoint tương ứng, không bịa tên endpoint → hỏi Dev (§8 dòng 4).

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `staff-management/feature-spec.md` BR-004 + luồng "Xóa Staff" (EP-15) | Chốt ai được xoá staff: chỉ admin chủ bot, hay cả staff được mời có quyền `employeesManagement` (như bản fix). Bổ sung nhánh mới của EP-15: tìm bản ghi theo `getListBotIdStaffManagement`, ngoài phạm vi / không tồn tại → 403 | C1 CONF-SPEC | Leader / PM |
| 2 | RULE-13 (quy ước mã HTTP) × `lesson-booking/web/api-spec.md` EP-29 | Chốt RULE-13 có áp hồi tố cho #39239 không. Nếu có: EP-29 cross-bot / không tồn tại → 403 hoặc 404 (hiện 200 + `success=false`); tham số sai format ("abc") → 400 (NEW-9, NEW-18); sửa expected NEW-3/5/7/9/18/19. EP-15 phía staff (403) đã khớp | C2 CONF-SPEC | Leader / Dev |
| 3 | `lesson-booking/feature-spec.md` §7 dòng 1 + kho TC-LSN-15 | Xác nhận giới hạn 10 ký tự của 「エルメ上での管理名」 còn hiệu lực không; nếu còn → sửa dữ liệu test của NEW-1, NEW-5 (và tên lịch mẫu ở tiền đề NEW-1/3/4) về ≤ 10 ký tự | C3 CONF-SPEC + CONF-KHO | Leader |
| 4 | Danh sách sibling cùng lớp lỗi (REG-SHARED-001) | Dev liệt kê đủ "6 chỗ" (hay 4?) chưa kiểm sở hữu kèm endpoint — đặc biệt endpoint của "xoá nhân viên chưa đồng ý" — và mở ticket riêng cho từng chỗ; kèm rà cặp Salon / Event booking có cùng kiểu `POST /{id}/edit` không | Q2 | Dev |
| 5 | `lesson-booking/web/api-spec.md` EP-29 · `feature-spec.md` §11.1 #3 (A-02), §11 A-23 | Cập nhật sau fix: route vẫn ngoài `checkLessonCalendarInBot` nhưng controller đã gắn `checkCalendarBelongBot` + UPDATE kèm `bot_id`; response không còn "luôn thành công". **Mass assignment trong cùng bot vẫn còn** (vẫn `$request->all()`) — giữ mục A-02 ở trạng thái "đã vá một phần" | Spec cũ hơn bản fix | Dev |
| 6 | Kho `fa019` TC-LSN-612 + MT-16 + MT-63 | Bỏ nhãn "DỰ KIẾN FAIL" cho phần cross-bot của `/{id}/edit`; giữ phần "server chỉ nhận trường 管理名" (whitelist chưa làm). Liên kết NEW-3 / ticket #39239 | Kho cũ hơn bản fix | Leader |
