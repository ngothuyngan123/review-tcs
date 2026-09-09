<!-- sync-tcs: url=<chưa có Sheet TC human/master cho ticket này> | sheet=<tên tab> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=198, ticket 34051, testcase_list (12 TC), fetch lúc 2026-09-04. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ MCP LME TEST STUDIO)

> ⚠️ **ĐỌC TRƯỚC KHI REVIEW** — bộ TC này **KHÔNG do member người viết**.

## Nguồn & cảnh báo cho Leader

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO** — `task_list(ticket_id=34051)` → `testcase_list(task_id=198)` |
| Studio task | `#198` — "[Detail form-answer] Sau khi nhấn stop remind thì màn hình bị hiển thị đóng detail form-result" |
| Type / Feature | `fix-bug` / `shop-card` |
| Status / pipelineStage | `done-ai` · `aiResult = pass` |
| Round | `1` |
| Branch | `ai_fixbug_33350` |
| reviewState | `leader` — **đang chờ Leader review** (`reviewed = false`) |
| Tạo bởi / Assignee | `ngannt` (2026-08-24 09:51) / `quyend` |
| Run gần nhất | `2026-09-04 03:25:58` by `quyend` (runId 846) |
| Tổng TC | **12** (`totalMatched = 12`) |
| Link TCs trong Redmine | **KHÔNG có** → fallback Studio (BƯỚC 6b) |

### 1. Tác giả TC — AI sinh 9/12, người viết 3/12

| `provenance.source` | Số TC | temp_id | Ý nghĩa |
|---|---|---|---|
| `ai` (actor `AI`, `created_job_id=582`) | **9** | NEW-1, NEW-2, NEW-4, NEW-5, NEW-6, NEW-7, NEW-8, NEW-9, NEW-10 | **AI sinh tự động** |
| `human` (actor `haodtb@mcp`) | **3** | NEW-11, NEW-12, NEW-13 | **Người viết** (`haodtb`), ghi vào Studio **qua kênh MCP** — không phải AI sinh |

> `task_list` báo `toolWritten: {tool: 9, mcp: 3, human: 0, rate: 75}` — con số `mcp: 3` chỉ là **kênh ghi**, tác giả thật là người (`haodtb`). Đừng đọc nhầm thành "0 TC do người viết".

### 2. Kết quả thực thi — 11 pass / 0 fail / 1 skip

| Trạng thái | Số TC | Chi tiết |
|---|---|---|
| `pass` | **11** | 9 TC run `2026-08-25 08:16:49` by `haodtb` (runId 488) · 2 TC (NEW-12, NEW-13) run `2026-09-04 03:25:58` by `quyend` (runId 846) |
| `fail` | **0** | — |
| `error` | **0** | — |
| `skip` | **1** | **NEW-10 / TC-DEPLOYASSET001-01** — `skip` (`source=manual`) by `quyend` lúc `2026-09-04 07:17:58` |
| Chưa chạy | 0 | — |

- **Không TC nào fail** → không có ticket bug phát sinh (`bug_tickets` rỗng ở cả 12 TC).
- Kết quả `pass` đều có `last_exec.source = "ai"` → **do pipeline AI chạy**, không phải QA người bấm tay.

### 3. ⚠️ Môi trường — TOÀN BỘ chỉ chạy ở `local` (RULE-08)

`envAuto` của task #198:

| env | envClass | total | automated | rate | runs |
|---|---|---|---|---|---|
| `local` | local | 12 | 11 | 91.7% | **3** |
| `dev` | safe | 12 | 0 | 0% | **0** |
| `staging` | safe | 12 | 0 | 0% | **0** |
| `prd` | prod | 12 | 0 | 0% | **0** |

⚠️ **RULE-08** — chưa có bất kỳ run nào ở `staging` / `prd`. Đặc biệt:

- **TC-DEPLOYASSET001-01 (NEW-10)** khai `env_scope = ["staging","prd"]`, `exec_mode = manual` — nhưng lại bị **`skip` khi run ở `local`**. Đây chính là TC cover rủi ro **cache-busting asset JS** (Dev không bump `sns-line.version`, xem `03-dev-impact.md` mục D2 / T5) → **rủi ro này hiện CHƯA được verify**.
- 11 TC còn lại khai `env_scope = ["all"]` nhưng `env_tag = "local-only"` → kết luận chỉ có giá trị ở `local`.

### 4. ⚠️ Mã quan điểm KHÔNG có trong `framework/checklist-lme.md`

| Mã quan điểm Studio | Có trong framework? | TC dùng |
|---|---|---|
| `TOOL-KNOW-002` | ❌ **KHÔNG** | NEW-1 (TC chính tái hiện bug) |
| `TOOL-ERRHYG-001` | ❌ **KHÔNG** | NEW-9 |
| `DATA-ID-001` | ✅ có | NEW-2 |
| `OUT-TRUTH-001` | ✅ có | NEW-4 |
| `DATA-001` | ✅ có | NEW-5, NEW-13 |
| `REG-SHARED-001` | ✅ có | NEW-6, NEW-12, NEW-7, NEW-8 |
| `CONC-003` | ✅ có | NEW-11 |
| `DEPLOY-ASSET-001` | ✅ có | NEW-10 |

→ **2 mã** (`TOOL-KNOW-002`, `TOOL-ERRHYG-001`) `/review-tc` **không map được coverage**. Đáng chú ý: TC quan trọng nhất (tái hiện + verify bug chính, NEW-1) lại gắn mã ngoài framework.

### 5. Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | **Normal 9** · **Abnormal 3** (NEW-9, NEW-10, NEW-11) · **Boundary 0** ⚠️ |
| `tc_group` | `ui` 12/12 — **không có TC nào ở tầng `api` / `data`** |
| `exec_mode` | `auto` 11 · `manual` 1 (NEW-10) |
| `env_tag` | `local-only` 11 · `env-safe` 1 (NEW-10) |
| `screen` | 12/12 = "Màn danh sách câu trả lời biểu mẫu V3 - popup chi tiết (tab nhắc lịch)" |
| `status` | `draft` 12/12 |
| `requirement_keys` | REQ-001…REQ-008 đều có ≥1 TC map. **3 TC không map REQ nào**: NEW-11, NEW-12, NEW-13 |
| `spec_status` | `null` 12/12 → cột "Trạng thái đánh giá spec" để trống |
| `priority` | `null` 9/12 · `High` (NEW-12) · `Medium` (NEW-11, NEW-13) |

> ℹ️ `temp_id` **NEW-3 khuyết** (id Studio 12508 không còn trong danh sách) — nhiều khả năng TC đã bị xóa. Nếu cần truy vết, dùng `testcase_get_history`.

### 6. Requirements của task Studio #198 (đối chiếu với `03-dev-impact.md`)

| REQ | Tiêu đề | Category | Risk | TC cover |
|---|---|---|---|---|
| REQ-001 | Popup chi tiết giữ nguyên mở sau khi dừng nhắc lịch | ui | **High** | NEW-1 |
| REQ-002 | Popup trỏ đúng bản ghi theo resultId sau reload | ui | Medium | NEW-2 |
| REQ-003 | Trạng thái 'đã dừng' hiển thị đúng và khớp DB | ui | Medium | NEW-4 |
| REQ-004 | Danh sách câu trả lời reload sau stop remind | ui | Low | NEW-5 |
| REQ-005 | initData tương thích ngược với các caller cũ | ui | Medium | NEW-6 |
| REQ-006 | 3 luồng đóng popup hợp lệ không đổi | ui | Medium | NEW-7, NEW-8 |
| REQ-007 | Xử lý lỗi khi dừng nhắc lịch thất bại | ui | Low | NEW-9 |
| REQ-008 | Cache-busting asset JS sau deploy | **data** | Medium | NEW-10 (**skip**) |

---

## TC List

> **16 cột canonical.** TCs dưới đây **chép nguyên văn từ Studio, read-only** — muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại, KHÔNG sửa trực tiếp file này.
>
> `TC No.` được **sinh lại theo quy ước repo** (`TC-<mã quan điểm bỏ gạch>-<nn>`); `temp_id` + `id` Studio giữ ở cột `Ghi chú` để trace ngược.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 | Normal | Dừng nhắc lịch trong popup — popup giữ nguyên mở (tái hiện & verify bug chính) | Đăng nhập Admin/Staff qua /login-v2, đã chọn bot. Có form biểu mẫu bản V3 và ≥1 câu trả lời có nhắc lịch đang hoạt động (chưa dừng). Mở màn danh sách câu trả lời V3 (/basic/form-answer/v3/result/{id}). | 1. Bấm vào một câu trả lời có nhắc lịch để mở popup chi tiết bên phải<br>2. Trong popup, chuyển sang tab 「リマインド」<br>3. Bấm nút 「配信停止」 của một nhắc lịch đang hoạt động<br>4. Ở hộp thoại xác nhận 「リマインドの停止 / リマインド配信を停止しますがよろしいですか？」 bấm 「配信停止」 | Câu trả lời có nhắc lịch đang hoạt động, chưa thực hiện dừng gửi. | Popup chi tiết vẫn mở và tiếp tục hiển thị đúng câu trả lời đang xem. Tab 「リマインド」 chuyển sang trạng thái đã dừng, hiển thị đúng tên người thao tác và 「操作日時」; không bị đóng popup sau khi xác nhận dừng. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12506 (NEW-1) · ui / auto / local-only · REQ-001 · spec_ids: TICKET-34051, EP-09, EP-55, git:6daa778302 · ⚠️ mã quan điểm KHÔNG có trong framework · last_exec: pass (source=ai, runId 488) · note: Thực hiện đúng luồng người dùng trên browser thật. Testcase này là case bắt buộc để xác nhận bug gốc không còn tái diễn sau fix. |
| TC-DATAID001-01 | DATA-ID-001 | Normal | Sau dừng nhắc lịch, popup vẫn hiển thị đúng câu trả lời đang xem (không nhảy bản ghi) | Có ≥2 câu trả lời có nhắc lịch active trong danh sách. Đăng nhập Admin/Staff, mở màn danh sách câu trả lời V3. | 1. Mở popup chi tiết của câu trả lời KHÔNG nằm đầu danh sách (vd bản ghi thứ 2 hoặc thứ 3), ghi nhớ tên người và ngày tạo hiển thị<br>2. Chuyển tab 「リマインド」, bấm 「配信停止」 và xác nhận | Bản ghi B (không phải phần tử đầu danh sách) | Sau khi danh sách được tải lại, popup vẫn hiển thị đúng bản ghi B đã mở trước đó: tên người, ngày tạo và nội dung tại tab 「回答内容」 đều thuộc bản ghi B; không tự chuyển sang câu trả lời khác. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12507 (NEW-2) · ui / auto / local-only · REQ-002 · spec_ids: TICKET-34051, EP-09 · last_exec: pass (source=ai, runId 488) · note: Dùng ít nhất 2 câu trả lời khác nhau rõ ràng để dễ phát hiện trường hợp popup trỏ nhầm bản ghi. |
| TC-OUTTRUTH001-01 | OUT-TRUTH-001 | Normal | Trạng thái đã dừng trên popup khớp dữ liệu thực tế (người thao tác + thời điểm) | Đăng nhập bằng tài khoản Admin/Staff xác định (ghi nhớ username). Có câu trả lời với nhắc lịch active. | 1. Mở popup chi tiết của câu trả lời có nhắc lịch đang hoạt động<br>2. Chuyển sang tab 「リマインド」, bấm 「配信停止」 và xác nhận dừng<br>3. Quan sát tên người thao tác và giá trị 「操作日時」 hiển thị sau khi dừng | Tài khoản đăng nhập = người thao tác | Popup vẫn mở và hiển thị trạng thái đã dừng. Tên người thao tác đúng với tài khoản đang đăng nhập và 「操作日時」 đúng với thời điểm dừng; dữ liệu lưu thực tế phải khớp với thông tin đang hiển thị. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12509 (NEW-4) · ui / auto / local-only · REQ-003 · spec_ids: TICKET-34051, EP-09 · last_exec: pass (source=ai, runId 488) · note: Ưu tiên đối chiếu UI với dữ liệu thực tế sau thao tác để tránh false success. |
| TC-DATA001-01 | DATA-001 | Normal | Danh sách câu trả lời được nạp lại sau khi dừng nhắc lịch | Danh sách có ít nhất 2 trang và đang áp dụng bộ lọc khoảng ngày cụ thể. Mở popup chi tiết từ một câu trả lời nằm ở trang N trong phạm vi đang lọc. | 1. Ghi nhận trang hiện tại N và khoảng ngày đang lọc<br>2. Mở popup chi tiết của một câu trả lời trên trang N<br>3. Chuyển sang tab 「リマインド」, bấm 「配信停止」 và xác nhận | Trang hiện tại N > 1 và một khoảng ngày lọc có dữ liệu phù hợp. | Sau khi dừng nhắc lịch, danh sách phía sau popup được tải lại nhưng vẫn giữ đúng trang N và khoảng ngày đang lọc; không tự quay về trang 1 hoặc mất điều kiện lọc. Popup vẫn hiển thị đúng câu trả lời đang xem. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12510 (NEW-5) · ui / auto / local-only · REQ-004 · spec_ids: TICKET-34051, EP-09 · last_exec: pass (source=ai, runId 488) · note: Case này kiểm đồng thời pagination + filter vì expected yêu cầu giữ cả hai trạng thái. |
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Smoke các thao tác tiêu biểu dùng chung luồng tải danh sách vẫn hoạt động sau fix | Danh sách câu trả lời có đủ dữ liệu để phân trang, lọc và sort. | 1. Chuyển sang trang khác bằng phân trang và xác nhận dữ liệu của trang được chọn hiển thị đúng<br>2. Đổi số dòng hiển thị mỗi trang và xác nhận số bản ghi hiển thị cập nhật đúng<br>3. Đổi thứ tự sắp xếp asc/desc và xác nhận danh sách đổi đúng thứ tự<br>4. Áp dụng bộ lọc khoảng ngày, sau đó reset bộ lọc và xác nhận dữ liệu tương ứng<br>5. Đổi tab danh sách và xác nhận dữ liệu của tab được chọn được tải đúng | 5 thao tác người dùng tiêu biểu có dùng chung luồng tải lại danh sách. | Cả 5 thao tác đều hoạt động đúng như trước fix: danh sách hiển thị đúng theo thao tác cuối cùng của người dùng, không xuất hiện lỗi JavaScript và không làm sai trạng thái popup/danh sách. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12511 (NEW-6) · ui / auto / local-only · REQ-005 · spec_ids: TICKET-34051, EP-09 · last_exec: pass (source=ai, runId 488) · note: Không coi case này là full coverage toàn bộ caller nội bộ; mục tiêu là regression smoke các đường người dùng có rủi ro cao và dễ quan sát. |
| TC-REGSHARED001-02 | REG-SHARED-001 | Normal | [Regression] Các luồng còn lại dùng chung tải danh sách vẫn hoạt động đúng sau fix | Đăng nhập Admin/Staff, mở màn danh sách câu trả lời V3. Chuẩn bị dữ liệu đủ để thực hiện các thao tác reload danh sách còn lại chưa được NEW-6 cover sau khi đối chiếu đủ 8 caller cũ của luồng tải danh sách. | 1. Xác định các thao tác UI tương ứng với các caller cũ của luồng tải danh sách chưa được NEW-6 cover<br>2. Thực hiện lần lượt từng thao tác đó trên màn danh sách câu trả lời V3<br>3. Sau mỗi thao tác, kiểm tra danh sách được tải lại đúng theo trạng thái/điều kiện người dùng vừa chọn<br>4. Mở popup chi tiết một câu trả lời sau các thao tác và xác nhận dữ liệu/popup vẫn hoạt động bình thường | Các đường thao tác user-facing còn thiếu trong tổng số 8 caller cũ của luồng tải danh sách. | Tất cả các thao tác còn lại dùng chung luồng tải danh sách đều hoạt động đúng như trước fix: dữ liệu reload đúng theo thao tác cuối cùng, không lỗi JavaScript, không làm sai trạng thái danh sách và không làm đóng/đổi sai popup ngoài hành vi thiết kế. | Đạt | | LOCAL | quyend | 2026-09-04 | | | Studio #15345 (NEW-12) · **người viết `haodtb@mcp`** · priority High · ui / auto / local-only · client_ref `task198-initdata-missing-callers` · KHÔNG map REQ nào · spec_ids: TICKET-34051, EP-09, REG-SHARED-001 · last_exec: pass (source=ai, runId 846) · note: Bắt buộc đối chiếu đủ danh sách 8 caller trước khi execute để case này không trở thành smoke mơ hồ. Mục tiêu là hoàn tất coverage REG-SHARED-001 còn thiếu của NEW-6. |
| TC-DATA001-02 | DATA-001 | Normal | Dừng một nhắc lịch khi cùng câu trả lời có nhiều nhắc lịch đang hoạt động | Có một câu trả lời biểu mẫu V3 chứa ít nhất 2 nhắc lịch đang hoạt động, ví dụ remind A và remind B. Đăng nhập Admin/Staff và mở popup chi tiết của câu trả lời đó. | 1. Trong popup, chuyển sang tab 「リマインド」 và xác nhận remind A, remind B đều đang hoạt động<br>2. Bấm 「配信停止」 tại remind A và xác nhận dừng<br>3. Sau khi dữ liệu reload, kiểm tra trạng thái của remind A<br>4. Kiểm tra trạng thái của remind B và khả năng tiếp tục thao tác với remind B | Một form-result có ít nhất 2 remind active: remind A và remind B. | Popup chi tiết vẫn mở đúng câu trả lời đang xem. Chỉ remind A chuyển sang trạng thái đã dừng và hiển thị đúng người thao tác cùng 「操作日時」. Remind B vẫn giữ trạng thái active, không bị dừng/xóa/đổi dữ liệu ngoài ý muốn và vẫn có thể thao tác bình thường. | Đạt | | LOCAL | quyend | 2026-09-04 | | | Studio #15346 (NEW-13) · **người viết `haodtb@mcp`** · priority Medium · ui / auto / local-only · client_ref `task198-multi-remind-stop-one` · KHÔNG map REQ nào · spec_ids: TICKET-34051, EP-09, EP-55 · last_exec: pass (source=ai, runId 846) · note: Case bổ sung để phát hiện lỗi cập nhật nhầm toàn bộ dataRemind hoặc trỏ sai item sau reload khi một result có nhiều remind. |
| TC-REGSHARED001-03 | REG-SHARED-001 | Normal | Xóa câu trả lời vẫn đóng popup và xóa item khỏi danh sách (luồng hợp lệ không đổi) | Có câu trả lời có thể xóa; mở popup chi tiết của câu trả lời đó. | 1. Trong popup, thực hiện thao tác xóa câu trả lời<br>2. Xác nhận hộp thoại 「削除しますが、宜しいですか？」 | Một câu trả lời bất kỳ | Sau khi xác nhận xóa, popup chi tiết đóng lại và câu trả lời bị xóa khỏi danh sách sau khi tải lại. Luồng xóa vẫn hoạt động đúng như trước fix, không bị ảnh hưởng bởi thay đổi ở thao tác dừng nhắc lịch. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12512 (NEW-7) · ui / auto / local-only · REQ-006 · spec_ids: TICKET-34051, EP-09 · last_exec: pass (source=ai, runId 488) · note: Kiểm tra đúng hành vi người dùng: xóa câu trả lời phải đóng popup; khác với stop remind là popup phải giữ mở. |
| TC-REGSHARED001-04 | REG-SHARED-001 | Normal | Nút đóng popup và đổi tab danh sách vẫn đóng popup như cũ (luồng hợp lệ) | Mở popup chi tiết một câu trả lời. | 1. Bấm nút đóng popup và xác nhận popup đóng<br>2. Mở lại popup chi tiết một câu trả lời<br>3. Đổi sang tab danh sách khác và kiểm tra trạng thái popup | 2 luồng đóng: nút đóng, đổi tab danh sách | Bấm nút đóng làm popup chi tiết đóng. Khi đang mở popup rồi đổi sang tab danh sách khác, popup cũng đóng như trước. Cả hai thao tác không phát sinh lỗi JavaScript và không bị ảnh hưởng bởi fix stop remind. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12513 (NEW-8) · ui / auto / local-only · REQ-006 · spec_ids: TICKET-34051, EP-09 · last_exec: pass (source=ai, runId 488) · note: Không dùng tên hàm/biến nội bộ trong expected; chỉ xác nhận hành vi quan sát được trên màn hình. |
| TC-TOOLERRHYG001-01 | TOOL-ERRHYG-001 | Abnormal | Dừng nhắc lịch thất bại — hiển thị thông báo lỗi, không đổi trạng thái sai | Dàn cảnh để POST /ajax/stop-item-remind trả lỗi: ví dụ đang có BackupHistory status 0/1 (backup guard chặn), hoặc mô phỏng lỗi server 5xx. | 1. Mở popup chi tiết, tab 「リマインド」, bấm 「配信停止」 và xác nhận<br>2. Quan sát phản hồi khi request lỗi | Điều kiện gây lỗi endpoint (backup guard / 5xx) | Hiển thị alert 「削除できません」; LoadingOverlay được ẩn; popup KHÔNG hiển thị trạng thái 'đã dừng' giả; nhắc lịch vẫn ở trạng thái active. Không báo thành công giả. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12514 (NEW-9) · ui / auto / local-only · REQ-007 · spec_ids: TICKET-34051, EP-55 · ⚠️ mã quan điểm KHÔNG có trong framework · last_exec: pass (source=ai, runId 488) · note: Nhánh error của stopItemRemind không đổi trong fix; kiểm để chắc fix không phá error path. EP-55 có backup guard chặn khi BackupHistory status 0/1. |
| TC-CONC003-01 | CONC-003 | Abnormal | Response reload cũ không được ghi đè câu trả lời user đang xem mới nhất | Có ít nhất 2 câu trả lời A và B với nội dung dễ phân biệt. Có thể làm chậm request tải lại danh sách bằng Network throttling hoặc công cụ test tương đương. Câu trả lời A có nhắc lịch đang hoạt động. | 1. Mở popup chi tiết câu trả lời A và chuyển sang tab 「リマインド」<br>2. Bật mạng chậm, bấm 「配信停止」 và xác nhận để request tải lại danh sách của A chưa trả về ngay<br>3. Trong khi request trước vẫn đang chờ, nếu UI cho phép thì mở câu trả lời B hoặc thực hiện thao tác chuyển selection sang B<br>4. Chờ toàn bộ response trả về và quan sát popup cuối cùng | Câu trả lời A có remind active; câu trả lời B có tên/ngày/nội dung khác rõ ràng với A. | Trạng thái cuối cùng của popup phải khớp thao tác mới nhất của user. Response tải lại phát sinh từ thao tác với A không được làm popup đang xem B tự nhảy ngược về A hoặc hiển thị lẫn dữ liệu A/B. Không xuất hiện lỗi JavaScript hay trắng màn. | Đạt | | LOCAL | haodtb | 2026-08-25 | | | Studio #12853 (NEW-11) · **người viết `haodtb@mcp`** · priority Medium · ui / auto / local-only · client_ref `task198-race-reload-1` · KHÔNG map REQ nào · spec_ids: TICKET-34051, EP-09, CONC-003 · last_exec: pass (source=ai, runId 488) · tech_note: nếu UI khóa hoàn toàn không cho đổi selection trong lúc request đang chờ, runner ghi nhận branch này là N/A · note: Ưu tiên chạy với Network throttling để ép response về chậm. Đây là case thay thế cho boundary giả tạo 'record biến mất khỏi trang sau reload'. |
| TC-DEPLOYASSET001-01 | DEPLOY-ASSET-001 | Abnormal | Sau deploy, trình duyệt nhận đúng JS mới khi chỉ refresh thường | Đã deploy branch fix lên môi trường. Trình duyệt của user từng load bản trước fix (đã cache form_result_v3.js cũ). | 1. Trên trình duyệt đã từng mở màn trước khi deploy, mở lại màn danh sách câu trả lời V3 và chỉ refresh thường, không hard-reload<br>2. Mở DevTools > Network và xác nhận file JavaScript của màn form-result được tải thành công với asset version hiện hành<br>3. Mở popup chi tiết một câu trả lời, vào tab 「リマインド」, bấm 「配信停止」 và xác nhận | Cache trình duyệt cũ + asset version hiện tại | Sau refresh thường, trình duyệt sử dụng đúng JavaScript mới của release; file asset tải thành công và luồng dừng nhắc lịch hoạt động theo bản fix: popup vẫn mở, trạng thái đã dừng hiển thị đúng. Nếu vẫn dùng asset cũ khiến popup bị đóng thì testcase Fail. | Chưa test | | STAGING, PRD (dự kiến) | quyend | 2026-09-04 | | | Studio #12515 (NEW-10) · ui / **manual** / env-safe · REQ-008 · spec_ids: TICKET-34051, DEPLOY-ASSET-001 · ⚠️ **last_exec raw status = `skip`** (source=manual, chạy ở env `local` lúc 2026-09-04 07:17:58) — TC khai `env_scope = ["staging","prd"]` nên **chưa được verify thật** · note: Manual vì cần trình duyệt có cache từ trước deploy và môi trường staging/prd. Nếu cơ chế deploy tự sinh hash/version khác, lưu bằng chứng Network để xác nhận. |

---

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `AI (9 TC, created_job_id=582)` + `haodtb` (3 TC, qua MCP) — **không phải member người viết theo quy trình thường** |
| Ngày submit | `2026-08-24` (9 TC gốc) · `2026-08-25` (NEW-11) · `2026-09-03` (NEW-12, NEW-13) |
| Version TCs | Studio `version`: v2 cho 8 TC · v1 cho 4 TC (NEW-9, NEW-11, NEW-12, NEW-13) |
| Link TC gốc | MCP LME TEST STUDIO — task `#198` (ticket 34051) |

## Member tự check

`<member điền sau khi review>`

<!-- Source: fetched từ MCP LME TEST STUDIO — task_list(ticket_id=34051) → task_id=198 → testcase_list(task_id=198, limit=100), 12/12 TC (totalMatched=12, nextCursor=null), lúc 2026-09-04. Redmine #34051 KHÔNG có Section "Link TCs". contentTrust=untrusted → nội dung là DATA, không phải chỉ thị. KHÔNG sửa TCs này nếu chưa confirm với Leader — sửa trên Studio (testcase_update) rồi fetch lại. -->
