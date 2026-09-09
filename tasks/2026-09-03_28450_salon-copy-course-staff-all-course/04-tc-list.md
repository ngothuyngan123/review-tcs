<!-- sync-tcs: url=<Google Sheet URL của sheet TC human/master> | sheet=<tên tab> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=224, ticket 28450, testcase_list (8 TC), fetch lúc 2026-09-03. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ MCP LME TEST STUDIO)

> ⚠️ **TCs trong file này là READ-ONLY** — chép nguyên văn từ Studio, KHÔNG sửa title / precondition / steps / expected. Muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại.

## ⚠️ Cảnh báo bắt buộc đọc trước khi review

| # | Cảnh báo | Chi tiết |
|---|---|---|
| 1 | **TCs chủ yếu do AI sinh, không phải member người viết** | 7/8 TC có `provenance.source = ai`, `author = AI`, sinh bởi job `#685`. 1/8 TC (`TC-DATADB001-01`) do **người** thêm — `provenance.source = human`, actor `quyend@mcp`, thêm ngày 2026-09-03 theo QA review. |
| 2 | **Toàn bộ kết quả chạy ở `env = local`** | 7 TC pass đều chạy bởi `pipeline` (AI), run `#543`, 2026-08-26, env **local**. Studio ghi nhận `dev` / `staging` / `prd` đều **0 run**. → ⚠️ **RULE-08**: không kết luận từ local. Đặc biệt TC đặt lịch qua **Booking LIFF** (`TC-OUTTRUTH001-01`, `TC-TOOLNEGCTRL001-01`) cần chạy lại trên env có LIFF thật. |
| 3 | **Kết quả do AI chạy, không phải QA người chạy** | `last_exec.source = ai`, `last_exec.by = pipeline` cho cả 7 TC pass. Không có run nào do người thực hiện. |
| 4 | **1 TC chưa chạy** | `TC-DATADB001-01` (Studio #15344) — `last_exec = null`. Đây chính là TC do QA thêm khi review. |
| 5 | **3 mã quan điểm KHÔNG có trong `framework/checklist-lme.md`** | `TOOL-KNOW-002` · `TOOL-OLDREC-001` · `TOOL-NEGCTRL-001` → `/review-tc` sẽ **không map được coverage** cho 4 TC dùng các mã này. Xem bảng đối chiếu bên dưới. |
| 6 | **3/8 requirement KHÔNG có TC nào cover** | `REQ-004` (không ghi trùng id) · `REQ-007` (hợp đồng endpoint server-side) · `REQ-008` (boundary gói Free đủ giới hạn khóa). Xem bảng coverage requirement bên dưới. |
| 7 | **Không có TC loại `Boundary`** | Phân bố: 6 Normal + 2 Abnormal + **0 Boundary**. `REQ-008` (boundary) và rủi ro R1 (tràn `varchar(255)`) đều không có TC. |
| 8 | **Trạng thái Studio** | `status = done-ai`, `reviewState = leader`, `reviewed = false`, `round = 1`, `openBugs = 0`, `branch = ai_fixbug_28450`. Tất cả 8 TC còn ở `status = draft`. |

### Đối chiếu mã quan điểm Studio vs `framework/checklist-lme.md`

| Mã quan điểm (Studio) | Số TC | Có trong `checklist-lme.md`? |
|---|---|---|
| `TOOL-KNOW-002` | 1 | ❌ KHÔNG |
| `REG-SHARED-001` | 1 | ✅ Có |
| `DATA-DB-001` | 1 | ✅ Có |
| `DATA-001` | 1 | ✅ Có |
| `TOOL-OLDREC-001` | 1 | ❌ KHÔNG |
| `OUT-TRUTH-001` | 1 | ✅ Có |
| `TOOL-NEGCTRL-001` | 2 | ❌ KHÔNG |

### Coverage requirement (Studio `task_get_context`)

| REQ | Tiêu đề | Risk | TC cover |
|---|---|---|---|
| REQ-001 | Copy khóa đồng bộ `course_ids` cho staff đã chọn tất cả khóa | High | `TC-TOOLKNOW002-01`, `TC-DATADB001-01`, `TC-DATA001-01` |
| REQ-002 | Tạo mới khóa vẫn đồng bộ đúng sau refactor (regression) | Medium | `TC-REGSHARED001-01` |
| REQ-003 | Staff không chọn tất cả khóa không bị tự thêm khóa copy | Medium | `TC-TOOLNEGCTRL001-01`, `TC-TOOLNEGCTRL001-02` |
| REQ-004 | Không ghi trùng id trong `course_ids` | Low | ❌ **GAP — không TC nào** |
| REQ-005 | Màn đặt lịch hiển thị đúng staff cho khóa vừa copy | High | `TC-OUTTRUTH001-01`, `TC-TOOLNEGCTRL001-01` |
| REQ-006 | Recovery dữ liệu cũ bằng re-save staff | Medium | `TC-TOOLOLDREC001-01` |
| REQ-007 | Hợp đồng endpoint copy khóa đồng bộ ở server | Medium | ❌ **GAP — không TC nào** |
| REQ-008 | Copy khi gói Free đã đủ giới hạn khóa bị chặn (boundary) | Low | ❌ **GAP — không TC nào** |

### Phân bố khác

| Chiều | Phân bố |
|---|---|
| `case_type` | Normal 6 · Abnormal 2 · **Boundary 0** |
| `tc_group` | `ui` 8/8 (không có TC `api` / `data` thuần) |
| `exec_mode` | `auto` 8/8 |
| `env_tag` | `local-only` 6 · `env-safe` 2 |
| `env_scope` | `all` 8/8 |
| `priority` (Studio) | High 4 · Medium 4 |
| `screen` | Màn danh sách khóa 3 · Màn quản lý nhân viên 3 · Trang đặt lịch (Booking LIFF) 2 |

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | AI (job `#685`) — 7 TC · `quyend@mcp` (human) — 1 TC |
| Ngày submit | 2026-08-26 (AI) · 2026-09-03 (TC bổ sung của QA) |
| Version TCs | Studio round 1 — `reviewState = leader`, `reviewed = false` |
| Link TC gốc (nếu có) | MCP LME TEST STUDIO `task_id = 224` |

---

## TC List

> **16 cột canonical.** `TC No.` sinh theo quy ước repo (`TC-<mã quan điểm bỏ gạch>-<nn>`); `id` + `temp_id` Studio giữ ở cột `Ghi chú` để trace ngược.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 | Normal | Copy khóa: staff đã chọn tất cả khóa được thêm id khóa mới (tái hiện + verify fix) | Đăng nhập admin, chọn bot có Lịch salon. Lịch salon có sẵn ≥1 khóa (vd Khóa A). Trên màn quản lý nhân viên đã có ít nhất 1 staff bật 'chọn tất cả khóa' (is_all_course=1) từ TRƯỚC — course_ids của staff này hiện chỉ chứa các khóa cũ, chưa có khóa sắp copy. | 1. Mở màn danh sách khóa (List course) của Lịch salon<br>2. Bấm nút Sao chép khóa (Sao chép khóa) trên Khóa A<br>3. Xác nhận/nhập tên và bấm nút lưu để hoàn tất tạo bản sao (Khóa A - bản sao)<br>4. Ghi lại id của khóa vừa được tạo (khóa copy)<br>5. Mở màn quản lý nhân viên, mở lại staff đã bật 'chọn tất cả khóa' và kiểm tra danh sách khóa được gán | Copy Khóa A của lịch salon; staff X có is_all_course=1 với course_ids chỉ gồm các khóa cũ trước khi copy | Bản sao khóa được tạo thành công. Trong course_ids của staff X (is_all_course=1) đã có thêm id của khóa vừa copy; trên màn quản lý nhân viên staff X hiển thị/được gán cả khóa copy. Đối chiếu DB: SELECT course_ids FROM calendar_salon_staff WHERE calendar_salon_id=&lt;lịch&gt; AND is_all_course=1 → chuỗi chứa id khóa copy. (Trước fix: course_ids KHÔNG chứa id khóa copy → đây là bug được sửa.) | Đạt | | LOCAL | pipeline | 2026-08-26 | | | Studio #13556 (NEW-1) · tc_group=ui · exec_mode=auto · env_tag=local-only · priority=High · REQ-001 · spec_ids: TICKET-28450, source CalendarSalonCourseService.php:200-246 · author=AI (job 685) · status=draft · note: Trigger phải phát sinh từ thao tác Sao chép khóa trên browser (JS FE gửi item_copy tới POST salon-course/create). API/DB chỉ để đối chiếu hậu quả. Hàm liên quan: storeCourse → addCourseToStaffsSelectedAllCourse. |
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Tạo mới khóa: staff đã chọn tất cả khóa vẫn được thêm id (regression sau refactor) | Đăng nhập admin, chọn bot có Lịch salon còn hạn mức tạo khóa. Có ≥1 staff bật 'chọn tất cả khóa' (is_all_course=1) từ trước. | 1. Mở màn danh sách khóa (List course) của Lịch salon<br>2. Bấm nút Tạo mới khóa<br>3. Nhập tên khóa mới hợp lệ và bấm nút lưu<br>4. Mở màn quản lý nhân viên, mở lại staff 'chọn tất cả khóa' và kiểm tra danh sách khóa được gán | Tạo mới khóa 'Khóa mới regression'; staff X có is_all_course=1 | Khóa mới được tạo. course_ids của staff X (is_all_course=1) đã có thêm id khóa mới; đối chiếu DB course_ids chứa id khóa mới. Hành vi tạo mới giữ nguyên như trước fix (logic tách ra hàm dùng chung nhưng kết quả không đổi). | Đạt | | LOCAL | pipeline | 2026-08-26 | | | Studio #13557 (NEW-2) · tc_group=ui · exec_mode=auto · env_tag=local-only · priority=Medium · REQ-002 · spec_ids: TICKET-28450, source CalendarSalonCourseService.php:198-201 · author=AI (job 685) · status=draft · note: Regression nhánh else (tạo mới) vì logic đồng bộ đã được refactor thành hàm dùng chung addCourseToStaffsSelectedAllCourse gọi sau cả 2 nhánh. |
| TC-DATADB001-01 | DATA-DB-001 | Normal | Copy khóa ở Lịch salon A không cập nhật staff của Lịch salon B | Đăng nhập admin. Có 2 Lịch salon A và B độc lập. Mỗi lịch có ít nhất 1 khóa và 1 staff bật 'chọn tất cả khóa' (is_all_course=1). Ghi lại course_ids của staff A và staff B trước khi thao tác. | 1. Mở màn danh sách khóa của Lịch salon A<br>2. Sao chép một khóa của Lịch salon A và lưu bản sao thành công<br>3. Ghi lại id của khóa vừa copy<br>4. Kiểm tra staff is_all_course=1 của Lịch salon A trên màn quản lý nhân viên và đối chiếu DB course_ids<br>5. Kiểm tra staff is_all_course=1 của Lịch salon B trên màn quản lý nhân viên và đối chiếu DB course_ids | Lịch salon A có staff A is_all_course=1; Lịch salon B có staff B is_all_course=1; chỉ thực hiện copy khóa tại Lịch salon A | Khóa copy chỉ được tạo trong Lịch salon A. course_ids của staff A được thêm đúng id khóa copy. course_ids của staff B thuộc Lịch salon B giữ nguyên hoàn toàn và không chứa id khóa vừa copy. Xác nhận thao tác đồng bộ chỉ tác động đúng calendar_salon_id mục tiêu, không cập nhật chéo dữ liệu lịch khác. | Chưa test | | (dự kiến) all | | | | | Studio #15344 (NEW-10) · client_ref=review224-cross-calendar-20260903 · tc_group=ui · exec_mode=auto · env_tag=local-only · priority=High · REQ-001 · **TC do NGƯỜI thêm** (provenance.source=human, actor quyend@mcp, 2026-09-03) theo QA review · last_exec=null (CHƯA CHẠY) · status=draft · note: Case bổ sung theo QA review để verify DB scope/cách ly dữ liệu giữa hai calendar_salon. Trigger copy phải thực hiện từ UI thật; DB chỉ dùng để đối chiếu hậu quả. |
| TC-DATA001-01 | DATA-001 | Normal | Copy khóa: mọi staff đang chọn tất cả khóa đều được cập nhật id khóa mới | Đăng nhập admin, lịch salon có ≥1 khóa. Có ÍT NHẤT 2 staff bật 'chọn tất cả khóa' (is_all_course=1) từ trước, course_ids của cả hai chưa có khóa sắp copy. | 1. Mở màn danh sách khóa, copy Khóa A → tạo bản sao<br>2. Mở màn quản lý nhân viên<br>3. Mở lần lượt từng staff is_all_course=1 và kiểm tra danh sách khóa được gán<br>4. Đối chiếu DB course_ids của từng staff is_all_course=1 | Copy Khóa A; staff X và staff Y đều is_all_course=1 | TẤT CẢ staff is_all_course=1 (X và Y) đều có thêm id khóa copy trong course_ids; không staff nào bị bỏ sót. Đối chiếu DB: mọi hàng calendar_salon_staff is_all_course=1 của lịch đều chứa id khóa copy. | Đạt | | LOCAL | pipeline | 2026-08-26 | | | Studio #13563 (NEW-5) · tc_group=ui · exec_mode=auto · env_tag=local-only · priority=High · REQ-001 · spec_ids: TICKET-28450, source CalendarSalonCourseService.php:236-246 · author=AI (job 685) · status=draft · note: Verify phạm vi 'chọn tất cả' áp cho toàn bộ staff is_all_course=1 (vòng lặp trong addCourseToStaffsSelectedAllCourse). Trigger copy từ browser. |
| TC-TOOLOLDREC001-01 | TOOL-OLDREC-001 | Normal | Recovery dữ liệu cũ: re-save staff bổ sung id khóa copy trước fix | Dựng trạng thái dữ liệu CŨ (mô phỏng copy trước khi deploy fix): lịch salon có khóa 'Khóa copy cũ' đã tồn tại, và staff V is_all_course=1 nhưng course_ids CHƯA chứa id 'Khóa copy cũ' (thiếu id — shape lỗi). Xác nhận DB trước khi test đúng trạng thái thiếu này. | 1. Kiểm tra DB: course_ids của staff V (is_all_course=1) THIẾU id 'Khóa copy cũ' (bằng chứng dữ liệu cũ lỗi)<br>2. Mở màn quản lý nhân viên, mở staff V<br>3. Giữ nguyên trạng thái 'chọn tất cả khóa' và bấm nút lưu (re-save)<br>4. Đối chiếu lại DB course_ids của staff V | Staff V is_all_course=1, course_ids thiếu id 'Khóa copy cũ' trước khi re-save | Sau khi re-save, course_ids của staff V được ghi lại đầy đủ TOÀN BỘ id khóa hiện có của lịch, bao gồm id 'Khóa copy cũ' đã thiếu trước đó. Dữ liệu cũ được khôi phục thủ công thành công. | Đạt | | LOCAL | pipeline | 2026-08-26 | | | Studio #13565 (NEW-7) · tc_group=ui · exec_mode=auto · env_tag=local-only · priority=Medium · REQ-006 · spec_ids: TICKET-28450, redmine RECOVER DATA, source CalendarSalonController.php:1572-1574 · author=AI (job 685) · status=draft · note: Fix chỉ áp cho copy MỚI; bản ghi cũ cần re-save (saveStaff, allSelected=true, course_ids = implode toàn bộ id khóa). TC phân biệt rõ record cũ (thiếu) vs sau recovery (đủ). Tiền điều kiện dựng bằng DB/seed, hành động re-save phải từ browser. |
| TC-OUTTRUTH001-01 | OUT-TRUTH-001 | Normal | Đặt lịch: khách chọn khóa vừa copy thấy staff đã chọn tất cả khóa | Lịch salon bật chọn khóa khi đặt (useCourse=1). Có staff X is_all_course=1 và booking_page_display=hiển thị. Đã copy 'Khóa copy' bằng luồng UI sau fix (course_ids của staff X đã chứa id 'Khóa copy'). Không có filter chặn staff X. | 1. Mở trang đặt lịch (Booking LIFF) của Lịch salon với tư cách khách LINE<br>2. Chọn 'Khóa copy' trong bước chọn khóa<br>3. Xem danh sách nhân viên có thể phục vụ khóa này | Khách chọn 'Khóa copy'; staff X is_all_course=1 | Staff X (is_all_course=1) XUẤT HIỆN trong danh sách nhân viên chọn được cho 'Khóa copy'; khách có thể chọn staff X để đặt lịch. (Trước fix: staff X bị loại vì course_ids thiếu id khóa copy → khách không đặt được.) | Đạt | | LOCAL | pipeline | 2026-08-26 | | | Studio #13568 (NEW-8) · tc_group=ui · exec_mode=auto · env_tag=env-safe · priority=High · REQ-005 · spec_ids: TICKET-28450, source CalendarSalonLineBookingService.php:2330-2360 · author=AI (job 685) · status=draft · ⚠️ TC qua Booking LIFF nhưng mới chỉ chạy ở local · note: Hậu quả end-user của bug. getListStaffCanBook lọc theo course_ids. Đường đặt lịch phải mở qua trang booking thật; DB dùng để đối chiếu tiền điều kiện. |
| TC-TOOLNEGCTRL001-01 | TOOL-NEGCTRL-001 | Abnormal | Đặt lịch: khách chọn khóa copy KHÔNG thấy staff chọn thủ công thiếu khóa (đối chứng âm) | Lịch salon useCourse=1. Có staff W is_all_course=0 với course_ids KHÔNG chứa 'Khóa copy'. Đã copy 'Khóa copy' sau fix. | 1. Mở trang đặt lịch (Booking LIFF) của Lịch salon với tư cách khách LINE<br>2. Chọn 'Khóa copy' trong bước chọn khóa<br>3. Xem danh sách nhân viên có thể phục vụ khóa này | Khách chọn 'Khóa copy'; staff W is_all_course=0 không có khóa copy | Staff W (is_all_course=0, course_ids không chứa 'Khóa copy') KHÔNG xuất hiện trong danh sách nhân viên cho 'Khóa copy'. Xác nhận đồng bộ không làm lộ nhầm staff không phục vụ khóa đó. | Đạt | | LOCAL | pipeline | 2026-08-26 | | | Studio #13569 (NEW-9) · tc_group=ui · exec_mode=auto · env_tag=env-safe · priority=Medium · REQ-005, REQ-003 · spec_ids: TICKET-28450, source CalendarSalonLineBookingService.php:2330-2360 · author=AI (job 685) · status=draft · ⚠️ TC qua Booking LIFF nhưng mới chỉ chạy ở local · note: Đối chứng âm ở màn booking: chỉ staff có id khóa trong course_ids mới hiện. Bổ trợ TC negative control ở màn staff. |
| TC-TOOLNEGCTRL001-02 | TOOL-NEGCTRL-001 | Abnormal | Copy khóa: staff KHÔNG chọn tất cả khóa không bị tự thêm khóa copy (đối chứng âm) | Lịch salon có ≥1 khóa. Có 1 staff Z bật 'chọn tất cả khóa' (is_all_course=1) và 1 staff W tắt (is_all_course=0, chỉ chọn thủ công một số khóa, KHÔNG gồm khóa sắp copy). | 1. Ghi lại course_ids hiện tại của staff W (is_all_course=0)<br>2. Mở màn danh sách khóa, copy Khóa A → tạo bản sao<br>3. Mở màn quản lý nhân viên, kiểm tra course_ids của staff W và staff Z<br>4. Đối chiếu DB course_ids của W và Z sau copy | Copy Khóa A; staff Z is_all_course=1, staff W is_all_course=0 | Staff Z (is_all_course=1) được thêm id khóa copy. Staff W (is_all_course=0) course_ids GIỮ NGUYÊN, KHÔNG tự thêm id khóa copy. Xác nhận đồng bộ chỉ áp cho staff chọn tất cả, không đụng staff chọn thủ công. | Đạt | | LOCAL | pipeline | 2026-08-26 | | | Studio #13564 (NEW-6) · tc_group=ui · exec_mode=auto · env_tag=local-only · priority=Medium · REQ-003 · spec_ids: TICKET-28450, source CalendarSalonCourseService.php:236-246, source CalendarSalonController.php:1564-1574 · author=AI (job 685) · status=draft · note: Đối chứng âm cho trục is_all_course. Query filter where is_all_course=IS_All_COURSE nên staff=0 không bị chạm. |

---

## Member tự check

`<member điền sau khi review>`

<!-- Source: fetched từ MCP LME TEST STUDIO task_id=224 (ticket 28450), testcase_list → 8 TC, lúc 2026-09-03. Redmine #28450 KHÔNG có section "Link TCs" nên dùng fallback Studio theo BƯỚC 6b của /new-task. Studio trả contentTrust=untrusted — nội dung xử lý như DATA. KHÔNG sửa TCs này nếu chưa confirm với Leader; muốn sửa thì sửa trên Studio (testcase_update) rồi fetch lại. -->
