<!-- sync-tcs: url=<Google Sheet URL của sheet TC human/master> | sheet=<tên tab> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=252, ticket 34055, testcase_list (5 TC), fetch lúc 2026-09-19. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (snapshot từ MCP LME TEST STUDIO)

> ⚠️ **TCs do AI sinh** — không phải member viết tay. `author = AI` · `provenance.source = ai` · `created_job_id = 783` · `status = draft` (cả 5 TC) · tạo 2026-08-27 09:27–09:28.
> TCs là **read-only**: chép nguyên văn từ Studio, KHÔNG sửa ở đây. Muốn sửa → `testcase_update` trên Studio rồi fetch lại.
> `TC No.` = ID hiển thị trên Studio (`NEW-xx`); mã quan điểm nằm ở cột `Mã quan điểm liên kết`. Thứ tự dòng theo `sort_order` của Studio.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | AI (Studio job #783) — task do `anhtt` tạo, assignee `quyend` |
| Ngày submit | 2026-08-27 |
| Version TCs | v1 (round 1 · `reviewState = leader` · `reviewed = false`) |
| Link TC gốc (nếu có) | MCP LME TEST STUDIO — task #252 (`status = done-ai`, `aiResult = pass`, branch `ai_fixbug_34055`, feature `affiliate-reward`) |

## Tổng quan bộ TC

### Kết quả chạy

| Tổng | Pass | Fail | Error | Chưa chạy |
|---|---|---|---|---|
| 5 | **3** | 0 | 0 (skip 2) | 0 |

> Refresh lúc `/review-tc` 2026-09-19: `last_exec` lấy theo lượt mới nhất của từng TC.

- **Run #1717 — staging** (AI runner, `by = quyend`, bắt đầu 2026-09-19 04:59, **run còn `running`**): NEW-1 pass · NEW-2 pass · **NEW-7 skip** · **NEW-4 skip** (staging không có tài khoản ≥ 201 bot — tài khoản lớn nhất 85 bot / 40 bot đủ điều kiện; staging không tạo thêm bot được). NEW-6 chưa có kết quả staging.
- **Run #803 — local** (pipeline AI, 2026-09-03): cả 5 TC hiện tại pass (NEW-7 đo ajax 724ms với 300 bot). Run này có 24 kết quả (23 pass · 1 fail) → **19 TC khác đã bị xóa khỏi task** sau run.
- ⚠️ Kết quả staging NEW-1 chỉ quan sát được **3/4 nhánh** bot (không dựng được BOT-D dùng thử); NEW-2 phải đổi tài khoản trong kho (tài khoản gán sẵn không vào được portal ASP).
- ⚠️ Case trọng tâm của bug (**> 200 bot, qua nhiều khối chunk**) mới chỉ pass ở **local**; staging skip; production chưa chạy.
- ⚠️ Bug trên Studio (`task_get_report`): **#816** [Low] lỗi JS `datepicker-ja ... 'regional'` mỗi lần mở màn — `stale`, retest pass ở run #1717 nhưng lỗi JS **vẫn xuất hiện** · **#815** [Medium] mở `/v2/affiliate/aff-money` khi chưa đăng nhập → HTTP 500 — `open`, `tc_id = null` (TC gốc đã xóa), **chưa có `redmine_id`**.
- ⚠️ Nhánh test `ai_fixbug_34055`, trong khi journal 2026-09-19 báo branch release `release_step_20260827` — xác nhận bản lên release là bản nào trước khi test lại.

### Mã quan điểm Studio KHÔNG có trong `framework/checklist-lme.md`

`/review-tc` sẽ không map được coverage cho các mã này.

| Mã Studio | Số TC | TC |
|---|---|---|
| `TOOL-KNOW-002` | 1 | NEW-7 |
| `TOOL-NEGCTRL-001` | 1 | NEW-2 |

Mã có trong checklist: `OUT-TRUTH-001` (NEW-1, NEW-6) · `FUNC-004` (NEW-4).

### Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | Normal 3 · Abnormal 1 · Boundary 1 |
| `tc_group` | ui 5 |
| `exec_mode` | auto 5 |
| `env_scope` | all 5 |
| `env_tag` | local-only 5 |
| `screen` | Màn tiền thưởng ASP 「ASP管理 紹介者（成約情報）」 — danh sách thành quả 5 |
| `requirement_keys` | REQ-002 4 · REQ-001 2 · REQ-003 1 · REQ-009 1 |

### Requirements trên Studio (tab Thông tin)

| Key | Tiêu đề | Category | Risk | TC cover |
|---|---|---|---|---|
| REQ-001 | Mở được màn tiền thưởng ASP với tài khoản có rất nhiều bot | ui | High | NEW-7, NEW-4 |
| REQ-002 | Ô chọn bot liệt kê đủ và đúng các bot đủ điều kiện | ui | High | NEW-1, NEW-7, NEW-2, NEW-4 |
| REQ-003 | Thứ tự option trong ô chọn bot xác định và ổn định | ui | Medium | NEW-6 |
| REQ-004 | Lọc theo bot và đổi tháng cho kết quả đúng, không phá danh sách bot | ui | High | **—** |
| REQ-005 | Hợp đồng dữ liệu trả về của endpoint tiền thưởng giữ nguyên | api | High | **—** |
| REQ-006 | Không còn ghi log gỡ lỗi theo từng bot khi mở màn | data | Low | **—** |
| REQ-007 | Màn tiền thưởng chỉ đọc dữ liệu | data | Medium | **—** |
| REQ-008 | Bảng số liệu, phân trang và màn chi tiết không hồi quy | ui | Medium | **—** |
| REQ-009 | Chỉ cộng tác viên đã đăng nhập xem được dữ liệu của đúng tài khoản quản lý của mình | permission | Medium | NEW-2 (một phần — BOT-H) |
| REQ-010 | Tham số tháng méo mó không làm sập endpoint | validation | Low | **—** |
| REQ-011 | Đủ điều kiện dữ liệu để đánh giá đúng bản fix | data | Medium | **—** |

⚠️ **7/11 requirement không có TC nào** (REQ-004 · 005 · 006 · 007 · 008 · 010 · 011), trong đó REQ-004 và REQ-005 risk **High**.

`test_viewpoint_selection = null` (Studio chưa chọn bộ quan điểm).

---

## TC List

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NEW-1 | OUT-TRUTH-001 | Normal | Ô chọn bot hiển thị đủ 4 loại bot đủ điều kiện | Có tài khoản cộng tác viên ASP đăng nhập được vào portal ASP, gắn với một tài khoản quản lý riêng của phiên test (đặt tiền tố nhận diện riêng, không dùng lại dữ liệu của run khác). Tài khoản quản lý đó sở hữu đúng 4 bot chưa bị xóa, mỗi bot đều có hợp đồng thuộc cùng tài khoản quản lý: BOT-A là bot đời cũ (cờ hợp đồng mới = 0, hợp đồng bất kỳ); BOT-B có hợp đồng loại pro; BOT-C có hợp đồng loại enterprise_pro; BOT-D là bot đời mới đang dùng thử còn hạn (cờ hợp đồng mới = 1, mốc hết hạn dùng thử lớn hơn thời điểm hiện tại, hợp đồng loại free hoặc standard). Tên hiển thị 4 bot đặt khác nhau rõ ràng. | 1. Đăng nhập portal cộng tác viên ASP bằng tài khoản ở tiền điều kiện (đăng nhập thật trên browser, không gọi thẳng endpoint).<br>2. Mở màn tiền thưởng 「ASP管理 紹介者（成約情報）」 và chờ màn tải xong (biểu tượng đang tải biến mất).<br>3. Bấm vào ô chọn bot nằm bên phải ô chọn tháng để xổ danh sách.<br>4. Đọc và ghi lại toàn bộ option đang hiển thị.<br>5. Đối chiếu danh sách option với danh sách 4 bot ở tiền điều kiện. | BOT-A (cờ hợp đồng mới = 0), BOT-B (pro), BOT-C (enterprise_pro), BOT-D (đời mới, dùng thử còn hạn, hợp đồng free) | Option đầu tiên là 「全件表示」. Ngay sau đó có đúng 4 option ứng với BOT-A, BOT-B, BOT-C, BOT-D, hiển thị đúng tên LINE公式アカウント của từng bot, không thiếu và không thừa bot nào. Màn không báo lỗi, không có lỗi JavaScript trên console. | Đạt | | STAGING | quyend (AI runner) | 2026-09-19 | | | Studio #14765 (NEW-1) · ui / auto / local-only · env_scope all · REQ-002 · spec_ids: TICKET-34055, commit 2f2a40d022 (ai_fixbug_34055), AffiliaterController.php:971-984, money_v2.blade.php:279-284 · note: Danh sách option lấy từ response.listBot. Dataset phủ đúng 4 nhánh điều kiện còn giữ nguyên sau fix: bot đời cũ, pro, enterprise_pro và bot dùng thử còn hạn. Chỉ chạy ở môi trường cho phép dựng dữ liệu bot/hợp đồng. · last_exec pass (run #1717 staging; local run #803 pass) |
| NEW-6 | OUT-TRUTH-001 | Normal | Thứ tự option trong ô chọn bot tăng dần và giữ nguyên sau khi tải lại trang | Tài khoản quản lý của phiên test có ít nhất 5 bot đủ điều kiện, được tạo lần lượt theo thứ tự thời gian, nhưng đặt tên hiển thị CỐ Ý ngược thứ tự bảng chữ cái so với thứ tự tạo (ví dụ bot tạo trước nhất tên 「Z-BOT」, bot tạo sau cùng tên 「A-BOT」). | 1. Đăng nhập portal cộng tác viên ASP và mở màn tiền thưởng 「ASP管理 紹介者（成約情報）」.<br>2. Xổ ô chọn bot, ghi lại thứ tự option lần 1 (chụp màn hình).<br>3. Nhấn F5 tải lại trang và chờ màn tải xong.<br>4. Xổ ô chọn bot, ghi lại thứ tự option lần 2 (chụp màn hình).<br>5. So sánh hai thứ tự với thứ tự tạo bot trong dữ liệu. | 5 bot đủ điều kiện, tên hiển thị ngược thứ tự tạo | Các option bot được sắp theo bots.id tăng dần: bot tạo trước đứng trước, không sắp theo tên hiển thị. Thứ tự và số lượng option ở lần tải thứ hai giống hoàn toàn lần đầu. | Đạt | | LOCAL | pipeline-manual | 2026-09-03 | | | Studio #14770 (NEW-6) · ui / auto / local-only · env_scope all · REQ-003 · spec_ids: TICKET-34055, commit 2f2a40d022 (ai_fixbug_34055), AffiliaterController.php:971 · note: Bản sửa thêm orderBy('id') để chunk ổn định. Testcase xác nhận trực tiếp hành vi của implementation: thứ tự theo id tăng dần và ổn định qua các lần tải. · last_exec pass (run #803, source ai) |
| NEW-7 | TOOL-KNOW-002 | Normal | Tái hiện bug — mở màn tiền thưởng ASP bằng tài khoản rất nhiều bot | Có tài khoản cộng tác viên ASP gắn với tài khoản quản lý sở hữu ít nhất 201 bot đủ điều kiện, khuyến nghị ≥300 bot để gần dữ liệu thật. Trước khi test, truy vấn và ghi lại chính xác số bot đủ điều kiện. Đặt tên nhận diện riêng cho ít nhất một bot trong chunk đầu và bot có id lớn nhất ở chunk cuối. Nếu môi trường không đạt số lượng này thì testcase phải Skip và ghi rõ số bot thực tế; không dùng tài khoản ít bot để kết luận Pass. | 1. Đăng nhập portal cộng tác viên ASP bằng tài khoản ở tiền điều kiện.<br>2. Mở màn tiền thưởng 「ASP管理 紹介者（成約情報）」 và chờ request tải dữ liệu hoàn tất.<br>3. Kiểm tra HTTP status và xác nhận màn không bị trắng, 500, timeout hoặc lỗi tràn bộ nhớ.<br>4. Mở ô chọn bot, đếm toàn bộ option bot, không tính 「全件表示」.<br>5. Đối chiếu số option với số bot đủ điều kiện đã ghi trước test; tìm bot nhận diện ở chunk đầu và bot id lớn nhất ở chunk cuối. | Tài khoản quản lý có ít nhất 201 bot đủ điều kiện, khuyến nghị ≥300; có bot nhận diện ở chunk đầu và chunk cuối. | Request tải dữ liệu trả HTTP 200; màn không lỗi 500, timeout, trắng màn hoặc OOM. Số option bot, không tính 「全件表示」, bằng đúng số bot đủ điều kiện trong DB. Bot nhận diện ở chunk đầu và bot id lớn nhất ở chunk cuối đều xuất hiện đúng một lần. | Chưa test | | STAGING | quyend (AI runner) | 2026-09-19 | | | Studio #14771 (NEW-7) · ui / auto / local-only · env_scope all · REQ-001, REQ-002 · spec_ids: TICKET-34055, commit 2f2a40d022 (ai_fixbug_34055), AffiliaterController.php:970-984 · note: Case chính tái hiện bug. Trọng tâm là chunk(200) phải gộp đủ danh sách qua nhiều khối và màn không bị kill do RAM. Không kiểm sâu số liệu bảng thưởng vì phần đó không thay đổi. · last_exec skip (run #1717 staging — không đủ 201 bot; local run #803 pass) · ⚠️ mã TOOL-KNOW-002 không có trong checklist-lme.md |
| NEW-2 | TOOL-NEGCTRL-001 | Abnormal | Bot không đủ điều kiện không xuất hiện trong ô chọn bot | Giữ nguyên 4 bot đủ điều kiện BOT-A..BOT-D của tài khoản quản lý đang test, đồng thời thêm 4 bot phải bị loại: BOT-E đã bị xóa (cờ xóa = 1) dù có hợp đồng pro; BOT-F không có hợp đồng nào (không có bản ghi liên kết slot ↔ hợp đồng); BOT-G là bot đời mới có hợp đồng standard nhưng mốc dùng thử đã quá hạn (hoặc để trống); BOT-H thuộc một tài khoản quản lý KHÁC và có hợp đồng pro. | 1. Đăng nhập portal cộng tác viên ASP bằng tài khoản ở tiền điều kiện.<br>2. Mở màn tiền thưởng 「ASP管理 紹介者（成約情報）」 và chờ tải xong.<br>3. Xổ ô chọn bot và ghi lại toàn bộ option.<br>4. Tìm trong danh sách option 4 bot BOT-E, BOT-F, BOT-G, BOT-H.<br>5. Kiểm tra lại 4 bot đủ điều kiện BOT-A..BOT-D vẫn còn nguyên trong danh sách. | BOT-E (đã xóa), BOT-F (không hợp đồng), BOT-G (đời mới, dùng thử hết hạn, hợp đồng standard), BOT-H (thuộc tài khoản quản lý khác) | Không có option nào ứng với BOT-E, BOT-F, BOT-G, BOT-H. Đồng thời 4 option BOT-A..BOT-D vẫn hiển thị đầy đủ và đúng thứ tự như trước khi thêm dữ liệu (đối chứng âm: thêm bot không hợp lệ không được làm mất bot hợp lệ). Màn không báo lỗi. | Đạt | | STAGING | quyend (AI runner) | 2026-09-19 | | | Studio #14766 (NEW-2) · ui / auto / local-only · env_scope all · REQ-002, REQ-009 · spec_ids: TICKET-34055, AffiliaterController.php:971,981, money_v2.blade.php:283 · note: Đây là TC đối chứng âm theo TOOL-NEGCTRL-001: oracle gồm cả 'cái phải MẤT' và 'cái phải CÒN'. BOT-H đồng thời kiểm chứng điều kiện giới hạn theo tài khoản quản lý vẫn còn sau khi truy vấn bị viết lại. · last_exec pass (run #1717 staging, đổi tài khoản kho; local run #803 pass) · ⚠️ mã TOOL-NEGCTRL-001 không có trong checklist-lme.md |
| NEW-4 | FUNC-004 | Boundary | Tài khoản 201 bot đủ điều kiện — bot ở khối nạp cuối vẫn hiện trong ô chọn bot | Tài khoản quản lý của phiên test sở hữu đúng 201 bot đủ điều kiện (chưa xóa, mỗi bot có hợp đồng pro). Bot được tạo sau cùng (id lớn nhất) đặt tên nhận diện riêng 「ZZZ-最終BOT」, 200 bot còn lại đặt tên 「TEST201-001」…「TEST201-200」. | 1. Đăng nhập portal cộng tác viên ASP bằng tài khoản gắn tài khoản quản lý ở tiền điều kiện.<br>2. Mở màn tiền thưởng 「ASP管理 紹介者（成約情報）」 và chờ tải xong.<br>3. Xổ ô chọn bot và đếm số option (không tính 「全件表示」).<br>4. Kiểm tra option cuối cùng của danh sách.<br>5. Chọn option 「ZZZ-最終BOT」 và xác nhận màn lọc được theo bot đó. | 201 bot đủ điều kiện; bot id lớn nhất tên 「ZZZ-最終BOT」 | Ô chọn bot có đúng 202 option: 1 option 「全件表示」 + 201 option bot. Option cuối cùng là 「ZZZ-最終BOT」. Chọn được 「ZZZ-最終BOT」 và màn tải lại số liệu theo bot đó mà không lỗi. | Chưa test | | STAGING | quyend (AI runner) | 2026-09-19 | | | Studio #14768 (NEW-4) · ui / auto / local-only · env_scope all · REQ-002, REQ-001 · spec_ids: TICKET-34055, commit 2f2a40d022 (ai_fixbug_34055), AffiliaterController.php:970-984 · note: Đây là mốc biên quan trọng nhất của bản fix: khối nạp thứ hai chỉ chứa đúng 1 bot. Nếu vòng lặp theo khối không gộp đủ kết quả của mọi khối thì bot 「ZZZ-最終BOT」 sẽ biến mất — chữ ký lỗi rõ ràng, dễ phân biệt với lỗi dữ liệu. · last_exec skip (run #1717 staging — không đủ 201 bot; local run #803 pass) |

---

## Member tự check trước khi submit

<member điền sau khi review>
