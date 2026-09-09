<!-- sync-tcs: url=<chưa có Sheet TC human cho ticket này> | sheet=<tên tab> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=184, ticket 33222, testcase_list (11 TC), fetch lúc 2026-09-03. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ MCP LME TEST STUDIO — TCs do **AI sinh**)

> ⚠️ **ĐỌC TRƯỚC KHI REVIEW** — đây KHÔNG phải TC do member người viết.

## Cảnh báo bắt buộc cho Leader

| # | Cảnh báo | Chi tiết |
|---|---|---|
| 1 | **TCs do AI sinh** | 10/11 TC có `author = AI`, `provenance.source = ai`, `createdJobId = 549`, tạo `2026-08-24 08:35:17`. Chỉ **1 TC** (`NEW-12`, Studio #15561) có `provenance.source = human`, `actor = quyend@mcp`, tạo `2026-09-03 09:08` — TC bổ sung của reviewer. Studio `toolWritten`: tool 10 · mcp 1 · **human 0** (rate 90.9%). |
| 2 | **Kết quả chạy: 10 pass / 0 fail / 0 error / 1 chưa chạy** | Tất cả 10 TC pass chạy cùng 1 lượt (`runId 435`, `2026-08-24 09:12:55`). TC chưa chạy: `TC-REGSHARED001-02` (Studio #15561 / NEW-12). Không TC nào fail → **không có ticket bug con**. |
| 3 | **Kết quả do AI pipeline chạy, KHÔNG phải QA người** | `last_exec.source = ai`, `last_exec.by = pipeline` cho cả 10 TC. Chưa có lượt chạy tay nào của QA. |
| 4 | ⚠️ **RULE-08 — toàn bộ chạy ở `env = local`** | `envAuto`: local 11 TC / 10 automated / 1 run · **dev = 0 run · staging = 0 run · prd = 0 run**. Kết luận "đã pass" **không có giá trị cho staging/production**. Trong khi đó `env_scope` của cả 11 TC đều khai `["all"]` → khai báo và thực thi **lệch nhau**. |
| 5 | ⚠️ **Fix chưa từng chạy trên data thật** | Journal Redmine #132590 ghi rõ AI **không kết nối được DB dev** (`host.docker.internal:3306` refused), verify chỉ ở mức `lint`. Ghi chú của chính TC `NEW-1`: *"Dữ liệu cần dựng thủ công (DB dev từng từ chối kết nối lúc AI fix)"* → cần chất vấn: 10 TC pass ở local đã dựng đủ data (staff có filter, staff phụ trách khóa, ca làm việc) hay pass "rỗng"? |
| 6 | ⚠️ **2 mã quan điểm KHÔNG có trong `framework/checklist-lme.md`** | `TOOL-NEGCTRL-001` (1 TC) và `TOOL-KNOW-002` (2 TC) → **3/11 TC không map được coverage** khi chạy `/review-tc`. Xem bảng bên dưới. |
| 7 | ⚠️ **REQ-005 không có TC nào cover** | Studio khai 5 requirement (REQ-001…REQ-005). `requirement_keys` của 11 TC chỉ phủ REQ-001 (3 TC) · REQ-002 (4 TC) · REQ-003 (1 TC) · REQ-004 (2 TC) · REQ-001+REQ-002 (1 TC). **REQ-005 "Regression: shared logic giữ nguyên ở call site khác" (2 job gán nhân viên, `getTotalListTimeBookingQ`, luồng đặt thật) = GAP hoàn toàn.** |
| 8 | **Trạng thái Studio** | task #184 · `status = done-ai` · `round = 1` · `reviewState = leader` · `reviewed = false` · `openBugs = 0` · `branch = ai_fixbug_33222` · assignee `quyend`, addedBy `ngannt`. Tất cả 11 TC `status = draft`. |

### 6.1 — Mã quan điểm Studio đối chiếu `framework/checklist-lme.md`

| Mã quan điểm Studio | Số TC | Có trong checklist-lme? | TC liên quan |
|---|---|---|---|
| `FUNC-001` | 2 | ✅ Có (Cao · nhóm 2.1) | TC-FUNC001-01, -02 |
| `TOOL-NEGCTRL-001` | 1 | ❌ **KHÔNG có** | TC-TOOLNEGCTRL001-01 |
| `UI-003` | 1 | ✅ Có (TB → Cao khi rủi ro false success · 2.8) | TC-UI003-01 |
| `TOOL-KNOW-002` | 2 | ❌ **KHÔNG có** | TC-TOOLKNOW002-01, -02 |
| `OUT-PREVIEW-001` | 1 | ✅ Có (Cao · 2.7 — BẮT BUỘC khi có chế độ preview) | TC-OUTPREVIEW001-01 |
| `FUNC-SEQ-001` | 1 | ✅ Có (TB · 2.1) | TC-FUNCSEQ001-01 |
| `REG-SHARED-001` | 2 | ✅ Có (Cao · 2.11) | TC-REGSHARED001-01, -02 |
| `FRIEND-001` | 1 | ✅ Có (Cao · 2.17) | TC-FRIEND001-01 |

### 6.2 — Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | **Normal 8** · **Abnormal 2** · **Boundary 1** |
| `priority` (Studio) | High 6 · Medium 5 |
| `tc_group` | `ui` **11/11** — **không có TC nhóm `api` / `data`** |
| `exec_mode` | `auto` 11/11 |
| `env_tag` | `read-only` 9 · `env-safe` 2 |
| `screen` | Preview — danh sách nhân viên 4 · Preview — lịch tuần 1 · Preview — lịch tháng 2 · Đối chiếu preview ⇔ friend 1 · Luồng friend thật (regression) 2 · Preview không dùng khóa 1 |
| `feature` | `calendar-salon` 11/11 |
| `temp_id` | NEW-1…NEW-5, NEW-7…NEW-12 — **NEW-6 bị thiếu** (đã xóa trên Studio, `totalMatched = 11`) |

---

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | **AI pipeline** (job #549) — 1 TC bổ sung bởi `quyend@mcp` |
| Ngày submit | `2026-08-24` (10 TC) · `2026-09-03` (TC-REGSHARED001-02) |
| Version TCs | Studio round 1 — 10 TC ở `version 2`, TC-REGSHARED001-02 ở `version 1` |
| Link TC gốc | MCP LME TEST STUDIO — `task_id = 184` (ticket 33222) |

---

## TC List

> **16 cột canonical.** Nội dung TC là **read-only** — chép nguyên văn từ Studio, KHÔNG sửa title/precondition/steps/expected. Muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | FUNC-001 | Normal | Preview: nhân viên có gắn filter bạn bè vẫn hiển thị trong danh sách | Đăng nhập admin, chọn bot; có 1 lịch salon dùng khóa (use_course=1). Có nhân viên NV-A phụ trách khóa K1 và CÓ gắn điều kiện lọc bạn bè (filter). Nhân viên đang hiển thị trên trang đặt lịch (booking_page_display). | 1. Từ màn quản lý lịch salon, bấm nút xem trước để mở màn preview đặt lịch (line_id='preview').<br>2. Chọn khóa K1.<br>3. Quan sát danh sách nhân viên phụ trách khóa hiển thị (AJAX get-list-staff-by-calendar). | Nhân viên NV-A: phụ trách khóa K1, có gắn filter bạn bè (điều kiện mà preview không có friend thật để thỏa). | NV-A PHẢI xuất hiện trong danh sách nhân viên ở preview (điều kiện lọc bạn bè bị bỏ qua, coi như thỏa). Trước fix NV-A vẫn hiện nhưng do bỏ MỌI lọc; sau fix vẫn hiện đúng vì thuộc khóa K1. | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12285 (NEW-1) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=High · REQ-001 · spec_ids: TICKET-33222, Mobile/CalendarSalonController.php:446-503 · Note gốc: "Kỹ thuật: endpoint /ajax/mobile/calendar-salon/get-list-staff-by-calendar; nhánh if (!$isPreview && $staff->filters) bị bỏ khi preview. Dữ liệu cần dựng thủ công (DB dev từng từ chối kết nối lúc AI fix)." · ⚠️ chạy ở local, chưa chạy staging/prd |
| TC-FUNC001-02 | FUNC-001 | Normal | Preview: nhân viên không gắn filter bạn bè vẫn hiển thị bình thường | Như trên; có nhân viên NV-B phụ trách khóa K1, KHÔNG gắn filter bạn bè. | 1. Mở màn preview đặt lịch salon.<br>2. Chọn khóa K1.<br>3. Quan sát danh sách nhân viên. | Nhân viên NV-B: phụ trách khóa K1, không gắn filter bạn bè. | NV-B hiển thị trong danh sách nhân viên ở preview (không bị ảnh hưởng bởi fix). | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12286 (NEW-2) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=Medium · REQ-001 · Note gốc: "Case đối chứng để phân biệt tác động của nhánh filter bạn bè." · ⚠️ chạy ở local |
| TC-TOOLNEGCTRL001-01 | TOOL-NEGCTRL-001 | Abnormal | Preview: nhân viên không phụ trách khóa đang chọn KHÔNG hiển thị | Lịch salon use_course=1; nhân viên NV-C chỉ phụ trách khóa K2 (không phụ trách K1). | 1. Mở màn preview đặt lịch salon.<br>2. Chọn khóa K1.<br>3. Quan sát danh sách nhân viên. | Nhân viên NV-C: chỉ phụ trách khóa K2; khóa đang chọn là K1. | NV-C KHÔNG xuất hiện khi chọn K1 (fix vẫn áp lọc theo khóa ở preview). Đây là regression quan trọng: bản cũ preview hiện TẤT CẢ nhân viên kể cả không phụ trách khóa. | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12287 (NEW-3) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=High · REQ-001 · spec_ids: Mobile/CalendarSalonController.php:455-465 · Note gốc: "Kiểm nhánh if ($useCourse == 1) { if (!in_array($courseId, $courseIds)) continue; } nay luôn áp cả preview." · ⚠️ **mã quan điểm TOOL-NEGCTRL-001 KHÔNG có trong framework/checklist-lme.md** · TC này cover **Bug 2** của ticket · ⚠️ chạy ở local |
| TC-UI003-01 | UI-003 | Boundary | Preview: khóa chưa gán nhân viên nào thì danh sách nhân viên trống | Có khóa K3 chưa gán nhân viên phụ trách nào. | 1. Mở màn preview đặt lịch salon.<br>2. Chọn khóa K3.<br>3. Quan sát danh sách nhân viên. | Khóa K3: không có nhân viên phụ trách. | Danh sách nhân viên trống ở preview (đúng và khớp bên friend), màn hiển thị trạng thái rỗng rõ ràng, không lỗi. | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12288 (NEW-4) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=Medium · REQ-001 · Note gốc: "Boundary danh sách rỗng theo spec state 'Khóa chưa gán nhân viên nào'." · ⚠️ chạy ở local |
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 | Normal | Preview: chọn nhân viên có filter bạn bè, lịch tuần hiển thị slot | Nhân viên NV-A phụ trách khóa K1, CÓ gắn filter bạn bè, có ca làm (time booking) cho tuần đang xem. | 1. Mở màn preview đặt lịch salon và chọn khóa K1.<br>2. Chọn nhân viên NV-A.<br>3. Xem lịch tuần (AJAX get-list-time-booking) và quan sát slot đặt lịch. | NV-A có ca làm trong tuần; line_id='preview'. | Lịch tuần hiển thị đầy đủ slot của NV-A. Trước fix: NV-A có filter bạn bè bị loại (lineUserId rỗng ⇒ isValidFilter luôn false) nên lịch trống. Sau fix: NV-A được tính, có slot. | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12289 (NEW-5) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=High · REQ-002 · spec_ids: CalendarSalonLineBookingService.php:2349-2358, Mobile/CalendarSalonController.php:639 · Note gốc: "Kỹ thuật: getListStaffCanBook(...,$isPreview=true) bỏ nhánh isValidFilter khi filter_id; route get-list-time-booking → getListTimeBookingWeek. Đây là TC tái hiện + verify bug lõi." · ⚠️ **mã quan điểm TOOL-KNOW-002 KHÔNG có trong framework/checklist-lme.md** · TC này cover **Bug 1** của ticket · ⚠️ chạy ở local |
| TC-OUTPREVIEW001-01 | OUT-PREVIEW-001 | Normal | Preview: lịch tháng hiển thị slot cho nhân viên có filter bạn bè | NV-A phụ trách K1, có filter bạn bè, có ca làm trong tháng đang xem. | 1. Mở màn preview đặt lịch salon, chọn khóa K1 và nhân viên NV-A.<br>2. Chuyển sang xem lịch tháng M và ghi nhận các ngày có slot khả dụng.<br>3. Mở cùng lịch salon bằng friend F-OK thỏa điều kiện filter của NV-A.<br>4. Chọn cùng khóa K1, nhân viên NV-A và cùng tháng M.<br>5. So sánh các ngày có slot giữa preview và bên friend. | NV-A có ca làm nhiều ngày trong tháng; line_id='preview'. | Các ngày có slot của NV-A trong tháng M ở preview phải khớp với bên friend F-OK khi cùng khóa, cùng nhân viên và cùng tháng. Preview vẫn tính NV-A dù có filter bạn bè, nhưng không được tạo thêm hoặc làm mất ngày có slot so với luồng friend thỏa điều kiện. | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12291 (NEW-7) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=High · REQ-002 · spec_ids: Mobile/CalendarSalonController.php:3941 · Note gốc: "Đối chiếu trực tiếp preview với luồng thật để cover nhánh lịch tháng. Kỹ thuật: showTimeBookingMonth truyền trạng thái preview vào getListStaffCanBook; chi tiết source chỉ dùng làm oracle." · ⚠️ chạy ở local |
| TC-FUNCSEQ001-01 | FUNC-SEQ-001 | Normal | Preview: chuyển tháng thì slot lịch tháng cập nhật đúng | NV-A có ca làm khác nhau ở tháng hiện tại và tháng kế tiếp. | 1. Ở màn preview lịch tháng của NV-A (khóa K1), ghi nhận slot tháng hiện tại.<br>2. Bấm chuyển sang tháng kế tiếp.<br>3. Quan sát slot của tháng mới. | Ca làm tháng T và T+1 khác nhau. | Khi chuyển tháng, lịch tháng gọi lại và hiển thị slot đúng theo dữ liệu ca làm của tháng được chọn, vẫn tính NV-A (có filter bạn bè) ở preview. | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12292 (NEW-8) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=Medium · REQ-002 · spec_ids: Mobile/CalendarSalonController.php:3941 · Note gốc: "Kiểm chuỗi thao tác chuyển tháng, đảm bảo isPreview vẫn được truyền mỗi lần gọi." · ⚠️ chạy ở local |
| TC-TOOLKNOW002-02 | TOOL-KNOW-002 | Normal | Đối chiếu preview và friend thỏa điều kiện: cùng danh sách nhân viên và slot | Có friend thật F-OK THỎA mọi điều kiện lọc bạn bè của nhân viên trên khóa K1; nhân viên NV-A phụ trách K1 có filter bạn bè; cùng khóa, cùng tuần. | 1. Mở màn preview đặt lịch salon, chọn khóa K1 và nhân viên NV-A có filter bạn bè.<br>2. Chọn đúng khoảng thời gian có ca làm theo dữ liệu reproduce gốc và ghi nhận danh sách nhân viên cùng các slot hiển thị.<br>3. Mở cùng lịch salon bằng friend F-OK thỏa toàn bộ điều kiện filter của NV-A.<br>4. Chọn cùng khóa K1, cùng nhân viên NV-A và cùng khoảng thời gian.<br>5. So sánh trực tiếp danh sách nhân viên và slot giữa preview với bên friend. | F-OK thỏa toàn bộ điều kiện filter của NV-A. | Với cùng khóa, cùng nhân viên và cùng khoảng thời gian, preview phải hiển thị cùng danh sách nhân viên và cùng slot như friend F-OK thỏa điều kiện. Lỗi gốc 'preview không hiển thị lịch trong khi bên friend hiển thị được' không còn tái diễn. | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12293 (NEW-9) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=High · REQ-003 · Note gốc: "TC tái hiện và verify bug gốc theo ticket. Khi có dataset chính xác từ report, dùng đúng ngày/ca làm tương ứng (ticket ghi hiện tượng từ 19/12); không thay bằng khoảng thời gian ngẫu nhiên nếu dữ liệu reproduce gốc đã xác định." · ⚠️ **mã quan điểm TOOL-KNOW-002 KHÔNG có trong framework/checklist-lme.md** · ⚠️ chạy ở local |
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Regression friend: friend thỏa filter bạn bè thì nhân viên hiển thị và có slot | Friend F-OK thỏa điều kiện filter của NV-A; NV-A phụ trách K1 có filter bạn bè. | 1. Mở màn đặt lịch salon với line_id = id friend F-OK.<br>2. Chọn khóa K1 và nhân viên NV-A.<br>3. Xem danh sách nhân viên và lịch tuần. | F-OK thỏa filter của NV-A. | NV-A hiển thị và có slot cho friend F-OK (hành vi filter bạn bè vẫn hoạt động, không bị fix làm hỏng). | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12294 (NEW-10) · tc_group=ui · exec_mode=auto · env_tag=env-safe · env_scope=["all"] · priority=Medium · REQ-004 · spec_ids: CalendarSalonLineBookingService.php:2352 · Note gốc: "Luồng friend chạy nhánh isPreview=false (mặc định) — chứng minh call site đặt lịch thật giữ nguyên." · ⚠️ chạy ở local |
| TC-FRIEND001-01 | FRIEND-001 | Abnormal | Regression friend: friend KHÔNG thỏa filter bạn bè thì nhân viên bị ẩn | Friend F-NG KHÔNG thỏa điều kiện filter của NV-A; NV-A phụ trách K1 có filter bạn bè. | 1. Mở màn đặt lịch salon với line_id = id friend F-NG.<br>2. Chọn khóa K1.<br>3. Quan sát danh sách nhân viên và slot của NV-A. | F-NG không thỏa filter của NV-A. | NV-A bị ẩn khỏi danh sách (và không có slot) đối với friend F-NG — filter bạn bè vẫn loại đúng, fix KHÔNG nới lỏng luồng friend thật. Đây là regression trọng yếu. | Đạt | | LOCAL | pipeline (AI) | 2026-08-24 | | | Studio #12295 (NEW-11) · tc_group=ui · exec_mode=auto · env_tag=env-safe · env_scope=["all"] · priority=High · REQ-004 · spec_ids: CalendarSalonLineBookingService.php:2352, Mobile/CalendarSalonController.php:490-497 · Note gốc: "Đối chứng âm cho luồng thật: fix chỉ bỏ filter khi $isPreview=true; friend thật vẫn chạy advanceFilterPost/isValidFilter." · ⚠️ chạy ở local |
| TC-REGSHARED001-02 | REG-SHARED-001 | Normal | Preview không dùng khóa: nhân viên có filter bạn bè vẫn hiển thị và có slot | Lịch salon không sử dụng bước chọn khóa (use_course=0). Có nhân viên NV-A đang hiển thị trên trang đặt lịch, có gắn filter bạn bè và có ca làm trong khoảng thời gian kiểm tra. | 1. Mở màn preview của lịch salon không sử dụng khóa.<br>2. Quan sát danh sách nhân viên và chọn NV-A.<br>3. Mở lịch tuần hoặc lịch tháng trong khoảng thời gian NV-A có ca làm.<br>4. Quan sát các slot khả dụng của NV-A. | Salon use_course=0; NV-A có filter bạn bè và có ca làm hợp lệ. | NV-A vẫn xuất hiện trong preview và các slot làm việc hiển thị đúng dù NV-A có filter bạn bè. Việc sửa logic lọc theo khóa không được làm mất nhân viên hoặc slot khi lịch salon không sử dụng khóa. | Chưa test | | Tất cả (dự kiến) | | | | | Studio #15561 (NEW-12) · **client_ref=review184-usecourse0-20260903** · **provenance.source=human, actor=quyend@mcp** (TC bổ sung của reviewer, tạo 2026-09-03 09:08) · version=1 · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=["all"] · priority=Medium · REQ-001, REQ-002 · spec_ids: CalendarSalonLineBookingService.php:2330-2358, Mobile/CalendarSalonController.php:446-503 · Note gốc: "Case regression cho nhánh use_course=0 vì fix thay đổi vị trí logic lọc staff/course. Trigger phải đi qua preview UI thật; không dùng request tự dựng thay thế." · **last_exec = null → CHƯA CHẠY** |

---

## Requirements của Studio task #184 (để đối chiếu coverage)

| REQ | Tiêu đề | Category | Risk | TC cover |
|---|---|---|---|---|
| REQ-001 | Preview: danh sách nhân viên bỏ lọc bạn bè, vẫn lọc theo khóa | ui | High | TC-FUNC001-01, TC-FUNC001-02, TC-TOOLNEGCTRL001-01, TC-UI003-01, TC-REGSHARED001-02 |
| REQ-002 | Preview: slot lịch tuần/tháng tính cả nhân viên có filter bạn bè | ui | High | TC-TOOLKNOW002-01, TC-OUTPREVIEW001-01, TC-FUNCSEQ001-01, TC-REGSHARED001-02 |
| REQ-003 | Preview khớp bên friend khi friend thỏa mọi điều kiện | ui | Medium | TC-TOOLKNOW002-02 |
| REQ-004 | Regression: luồng friend thật vẫn lọc bạn bè đúng | ui | High | TC-REGSHARED001-01, TC-FRIEND001-01 |
| REQ-005 | Regression: shared logic giữ nguyên ở call site khác — `getListStaffCanBook` mặc định `isPreview=false`; 2 job gán nhân viên, luồng đặt lịch thật, `getTotalListTimeBookingQ` không truyền `isPreview=true` | **data** | Medium | ⚠️ **KHÔNG có TC nào** — GAP |

---

## Member tự check

`<member điền sau khi review>` — TCs này do AI sinh, không có member người viết.

<!-- Source: fetched từ MCP LME TEST STUDIO task_id=184 (ticket 33222) — testcase_list(limit=100), totalMatched=11, contentTrust=untrusted, lúc 2026-09-03. Redmine #33222 KHÔNG có section "Link TCs". TCs là READ-ONLY — muốn sửa thì sửa trên Studio (testcase_update) rồi fetch lại. -->
