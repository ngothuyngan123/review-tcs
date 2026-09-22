<!-- sync-tcs: url=<chưa có — Redmine #38783 KHÔNG có Link TCs> | sheet=<chưa có> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=192, ticket 38783, testcase_list (8 TC), fetch lúc 2026-09-17. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List (fetch từ MCP LME TEST STUDIO — task #192)

> ⚠️ **ĐỌC TRƯỚC KHI REVIEW — bộ TC này KHÔNG do member người viết.**

## 0. Nguồn TC + cảnh báo bắt buộc

| Mục | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO** — `task_id=192`, ticket `38783`, `testcase_list` (8 TC), fetch `2026-09-17` |
| Lý do fallback | Redmine #38783 **KHÔNG có Section "Link TCs"** → không có Sheet TC human |
| Task Studio | `#192` · type `fix-bug` · typeLabel `Test bug` · feature `coupon-management` · status `done-ai` · round `1` · branch `ai_small_38783` · `archived=false` |
| Review state | `reviewState = tester` · `reviewed = false` · `openBugs = 0` · `aiResult = null` |
| Tạo / chạy | `addedBy=ngannt` (2026-08-24 09:50) · `assignee=cucdtk` · `runBy=pipeline-resume` (2026-08-25 13:18, 2.2 phút) |

### 0.1. Tác giả TC — 7/8 TC do **AI sinh**, không phải member người viết

| Tác giả | Số TC | Chi tiết |
|---|---|---|
| **AI** (`provenance.source = ai`, `createdJobId = 574`) | **7** | NEW-1 → NEW-7, tạo `2026-08-24 10:28` |
| **Human qua kênh MCP** (`provenance.source = human`, actor `cucdtk@mcp`) | **1** | NEW-8 (Studio #18378) — chuyển tab sau khi lọc, tạo `2026-09-16 09:06` |

> `toolWritten` của Studio: `total=8 · tool=7 · mcp=1 · human=0 · rate=87.5%`. Field `toolWritten.mcp` chỉ là **kênh ghi**; tác giả thật đọc ở `provenance.source` (bảng trên).
> Toàn bộ 8 TC còn ở `status = draft`. NEW-7 đã lên `version 2` (update `2026-09-16 09:05` theo review).

### 0.2. Kết quả thực thi

| Trạng thái | Số TC | TC No. |
|---|---|---|
| `pass` (Đạt) | **7** | NEW-1, NEW-2, NEW-3, NEW-4, NEW-5, NEW-6, NEW-7 |
| `fail` (Không đạt) | **0** | — |
| `error` | **0** | — |
| Chưa chạy | **1** | **NEW-8** (`last_exec = null`) — TC human bổ sung `2026-09-16`, **sau** lần chạy duy nhất (2026-08-25) |

- **Không có TC fail → không có ticket bug phát sinh** (`openBugs = 0`, `bug_tickets = []` ở cả 8 TC).
- **Toàn bộ 7 kết quả `pass` đều do AI chạy tự động**, không phải QA người chạy: `last_exec.source = ai`, `by = pipeline-resume`, cùng `runId = 525`, cùng mốc `2026-08-25 13:18:50`.
- ⚠️ **`envAuto` ghi `runs = 2` ở env `local`** nhưng cả 8 TC chỉ có 1 `last_exec` (run 525) → có run trước đó không còn là kết quả cuối. Muốn xem đủ lịch sử run phải gọi `task_get_report(task_id=192)`.
- ⚠️ **NEW-8 chưa từng chạy** — đây là TC duy nhất cover quan điểm giữ/reset trạng thái filter khi đổi tab, hiện **chưa có bằng chứng**.

### 0.3. ⚠️ Môi trường đã chạy — toàn bộ ở `local`

| Env | total | automated | rate | **runs** |
|---|---|---|---|---|
| `local` | 8 | 7 | 87.5% | **2** |
| `dev` | 8 | 0 | 0% | **0** |
| `staging` | 8 | 0 | 0% | **0** |
| `prd` | 8 | 0 | 0% | **0** |

> Cả 8 TC khai `env_scope = ["all"]` nhưng `env_tag = local-only`; **thực tế chỉ có run ở `local`**, chưa có run nào ở `dev` / `staging` / `prd`.
> **RULE-08** (media · domain · job · loadbalance · bill tiền) — task này chỉ đổi điều kiện đọc của 1 query lọc danh sách, **không** chạm media/job/tiền, nên RULE-08 **không bắt buộc** phải test production. Tuy nhiên dữ liệu coupon thật trên production có phân bố ngày và timezone khác fixture local → Leader cân nhắc 1 lượt xác nhận trên staging.
> Lưu ý: `env_scope` khai báo ở từng TC là **phạm vi dự kiến**, KHÔNG phải env đã chạy — env đã chạy đọc ở `envAuto[].runs`.

### 0.4. ⚠️ Mã quan điểm Studio KHÔNG có trong `framework/checklist-lme.md`

| Mã quan điểm Studio | Có trong framework? | TC dùng |
|---|---|---|
| `TOOL-KNOW-002` | ❌ **KHÔNG** | NEW-1 |
| `DATA-HIST-001` | ❌ **KHÔNG** | NEW-2 |
| `API-001` | ❌ **KHÔNG** | NEW-6 |
| `TOOL-VAL2-001` | ❌ **KHÔNG** | NEW-7 |
| `RULE-12` | ⚠️ có nhưng là **RULE**, không phải mã quan điểm | NEW-8, NEW-5 |
| `OUT-TRUTH-001` | ✅ có | NEW-3 |
| `FUNC-DATE-001` | ✅ có | NEW-4 |

> **4/8 TC dùng mã KHÔNG có trong framework** → `/review-tc` không map được coverage cho các TC này. Thêm 2 TC gán `RULE-12` (RULE dùng thay vị trí mã quan điểm).

### 0.5. Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | Normal **5** (NEW-1, NEW-2, NEW-8, NEW-5, NEW-6) · Abnormal **2** (NEW-3, NEW-7) · Boundary **1** (NEW-4) |
| `tc_group` | ui **6** · api **2** (NEW-6, NEW-7) |
| `exec_mode` | auto **8** · manual **0** |
| `screen` | Tab 使用済み **5** · Tab 未使用者 **1** (NEW-5) · EP-02 API **2** |
| `requirement_keys` | REQ-001 → REQ-006 mỗi req có ≥1 TC; **NEW-8 có `requirement_keys` TRỐNG** |
| `spec_ids` | `SCR-CPN-01` · `EP-02` · `TICKET-38783` |

### 0.6. Requirements khai trên Studio (`task_get_context`)

| Req | Tiêu đề | Category | Risk | TC cover |
|---|---|---|---|---|
| REQ-001 | Lọc lịch sử theo 発行日 (`type_filter=0`) trả đúng records trong khoảng ngày | ui | Medium | NEW-1 |
| REQ-002 | Lọc lịch sử theo 使用日 (`type_filter=1`) trả đúng records trong khoảng ngày | ui | Medium | NEW-2 |
| REQ-003 | Biên khoảng ngày inclusive (`whereDate BETWEEN`) | ui | Medium | NEW-4 |
| REQ-004 | Clear filter (✕) → không lọc, trả toàn bộ tab đã dùng | ui | Low | NEW-3 |
| REQ-005 | Tab 未使用者 không bị ảnh hưởng bởi filter ngày (regression smoke) | ui | Low | NEW-5 |
| REQ-006 | Hợp đồng EP-02 sau fix: đủ 2 ngày → lọc; thiếu 1 đầu (rỗng) → không lọc; **nhánh `catch` vẫn trả HTTP 200 kèm field `msg`** (xoá comment chết không phá `catch`) | api | Medium | NEW-6, NEW-7 |

> ⚠️ **REQ-006 chỉ được cover một phần**: vế *"nhánh `catch` vẫn trả HTTP 200 kèm field `msg`"* — chính là phần mục 2 của Dev (xoá `// DB::rollback();` trong `catch`) — **không có TC nào verify**. NEW-6/NEW-7 chỉ cover 2 vế đầu.
> `test_viewpoint_selection = null` — Studio **không** lưu bước chọn quan điểm test cho task này.

---

## TC List — 16 cột canonical (read-only, chép nguyên văn từ Studio)

> **TC No. = ID hiển thị trên Studio** (`temp_id` dạng `NEW-x`) theo quy ước repo cho TC fetch từ tool; mã quan điểm giữ ở cột `Mã quan điểm liên kết` đúng như Studio khai.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NEW-1 | TOOL-KNOW-002 | Normal | Lọc tab 使用済み theo 発行日 trả đúng mã trong khoảng ngày | Đăng nhập System Admin (role -1) qua /login-v2. Dưới admin_id đang đăng nhập, tạo 3 mã ĐÃ DÙNG (is_used=1): A(created_at=2026-03-10), B(2026-03-20) trong khoảng, C(2026-04-25) ngoài khoảng; reason nhận diện 'TC38783-A/B/C'. | 1. Mở /admin/coupon-management<br>2. Bấm tab 「使用済み」<br>3. Chọn radio 「発行日」<br>4. Chọn khoảng 2026-03-01 → 2026-03-31 trên range picker<br>5. Chờ bảng reload | Radio 発行日; 2026-03-01 → 2026-03-31; A/B trong, C ngoài | Bảng chỉ hiển thị A,B; không có C. Đối chiếu DB whereDate('created_at' BETWEEN) scope admin_id trả {A,B}. | Đạt | | LOCAL | pipeline-resume (AI) | 2026-08-25 | | | Studio #12432 (NEW-1) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-001 · spec_ids: SCR-CPN-01, EP-02, TICKET-38783 · ⚠️ `TOOL-KNOW-002` KHÔNG có trong framework/checklist-lme.md · note Studio: "Thao tác thật trên flatpickr; API/DB chỉ để đối chiếu. verify-fixed nhánh type_filter=0 (dòng 9490)." |
| NEW-2 | DATA-HIST-001 | Normal | Lọc tab 使用済み theo 使用日 trả đúng mã trong khoảng ngày | Đăng nhập System Admin. Tạo 3 mã ĐÃ DÙNG có datetime_use: D(2026-05-05), E(2026-05-15) trong khoảng, F(2026-06-02) ngoài; created_at của D/E/F đặt ngoài khoảng lọc để cô lập cột. | 1. Mở /admin/coupon-management, tab 「使用済み」<br>2. Chọn radio 「使用日」<br>3. Chọn khoảng 2026-05-01 → 2026-05-31<br>4. Chờ bảng reload | Radio 使用日; 2026-05-01 → 2026-05-31; D/E trong, F ngoài | Bảng chỉ hiển thị D,E; không có F. Vì created_at ngoài khoảng vẫn hiển thị → lọc đúng cột datetime_use (dòng 9492). | Đạt | | LOCAL | pipeline-resume (AI) | 2026-08-25 | | | Studio #12433 (NEW-2) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-002 · spec_ids: SCR-CPN-01, EP-02 · ⚠️ `DATA-HIST-001` KHÔNG có trong framework/checklist-lme.md · note Studio: "Màn lịch sử cần data datetime_use rõ ràng. Kiểm UI + DB." |
| NEW-8 | RULE-12 | Normal | Chuyển tab sau khi lọc khoảng ngày không làm sai trạng thái filter | Đăng nhập System Admin. Chuẩn bị dữ liệu mã đã dùng có created_at và datetime_use khác nhau để phân biệt điều kiện lọc theo từng loại ngày. | 1. Mở màn quản lý mã coupon<br>2. Chọn tab 「使用済み」<br>3. Chọn radio 「発行日」 và chọn một khoảng ngày có dữ liệu<br>4. Kiểm tra kết quả hiển thị<br>5. Chuyển sang tab 「未使用者」<br>6. Quay lại tab 「使用済み」 | Coupon đã dùng: dữ liệu nằm trong và ngoài khoảng lọc theo created_at; dữ liệu có datetime_use khác created_at để nhận biết loại filter | Khi quay lại tab 「使用済み」, danh sách được load đúng theo thiết kế. Không áp dụng nhầm điều kiện created_at/datetime_use, không hiển thị sai dữ liệu do trạng thái filter cũ. Chức năng filter khoảng ngày vẫn hoạt động bình thường. | Chưa test | | ALL (dự kiến) | | | | | Studio #18378 (NEW-8) · client_ref=NEW-9-filter-tab-switch · **author=cucdtk@mcp (human bổ sung 2026-09-16)** · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · requirement_keys **trống** · spec_ids: SCR-CPN-01, EP-02, TICKET-38783 · ⚠️ `RULE-12` là RULE, không phải mã quan điểm · ⚠️ **chưa chạy lần nào** (tạo sau run 525) · note Studio: "Bổ sung theo dev impact: ajaxCouponManagement xử lý chung màn quản lý coupon; kiểm tra regression khi chuyển trạng thái màn hình sau khi sử dụng filter." |
| NEW-3 | OUT-TRUTH-001 | Abnormal | Bấm clear (✕) khoảng ngày → hiển thị lại toàn bộ mã đã dùng | Đăng nhập System Admin, có mã đã dùng ngoài khoảng đang bị lọc ẩn; đang ở trạng thái đã lọc khoảng ngày hẹp. | 1. Tại tab 「使用済み」 đang lọc theo khoảng ngày<br>2. Bấm nút clear (✕) cạnh range picker<br>3. Chờ bảng reload | Clear filter (start_date=null, end_date=null) | Range picker rỗng; bảng hiển thị lại TOÀN BỘ mã đã dùng của admin (per_page=100, 発行日 desc), gồm cả mã trước bị loại. Không áp whereDate. | Đạt | | LOCAL | pipeline-resume (AI) | 2026-08-25 | | | Studio #12434 (NEW-3) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-004 · spec_ids: SCR-CPN-01, EP-02 · note Studio: "Nhánh 'không lọc' (start/end null) — hành vi đúng, không đổi bởi fix." |
| NEW-4 | FUNC-DATE-001 | Boundary | Biên khoảng ngày inclusive: mã đúng ngày start/end được tính, ngoài 1 ngày bị loại | Đăng nhập System Admin. Tạo 4 mã ĐÃ DÙNG created_at: G(2026-07-01 00:00)=start, H(2026-07-31 23:30)=end, I(2026-06-30) trước start 1 ngày, J(2026-08-01) sau end 1 ngày. | 1. Mở /admin/coupon-management, tab 「使用済み」<br>2. Chọn radio 「発行日」<br>3. Chọn khoảng 2026-07-01 → 2026-07-31<br>4. Chờ bảng reload | 2026-07-01 → 2026-07-31; G/H biên, I/J ngoài | Bảng hiển thị G,H (biên inclusive, record 23:30 ngày end vẫn tính); không có I,J. | Đạt | | LOCAL | pipeline-resume (AI) | 2026-08-25 | | | Studio #12435 (NEW-4) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-003 · spec_ids: SCR-CPN-01, EP-02 · note Studio: "whereDate so trên phần DATE. Biến thể ngày gộp 1 dataset." |
| NEW-5 | RULE-12 | Normal | Smoke tab 未使用者: không có filter ngày, danh sách mã chưa dùng hiển thị đầy đủ | Đăng nhập System Admin. Có ≥2 mã CHƯA DÙNG (is_used=0) created_at khác nhau. | 1. Mở /admin/coupon-management (mặc định tab 「未使用者」)<br>2. Quan sát vùng thanh lọc<br>3. Quan sát danh sách | Không nhập; mở tab mặc định | Tab 未使用者 KHÔNG có thanh lọc ngày/radio; danh sách hiển thị đầy đủ mã chưa dùng, không bị ràng buộc khoảng ngày. | Đạt | | LOCAL | pipeline-resume (AI) | 2026-08-25 | | | Studio #12436 (NEW-5) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-005 · spec_ids: SCR-CPN-01 · ⚠️ `RULE-12` là RULE, không phải mã quan điểm · note Studio: "Smoke regression RULE-12: nhánh type_display=0 không bị diff chạm." |
| NEW-6 | API-001 | Normal | EP-02 với đủ 2 ngày (type_filter=0): response chỉ chứa mã trong khoảng | Phiên System Admin hợp lệ (cookie + X-CSRF-TOKEN). Có mã đã dùng A,B trong khoảng và C ngoài. | 1. Gửi POST /admin/init-coupon-management: type_display=1, type_filter=0, start_date=2026-03-01, end_date=2026-03-31, col_sort=created_at, sort_type=desc, perPage=100, page=1<br>2. Đọc JSON response | type_display=1, type_filter=0, start_date=2026-03-01, end_date=2026-03-31, col_sort=created_at, sort_type=desc, perPage=100, page=1 | HTTP 200, {status:true,data:{...}} với data.data chỉ gồm A,B (không C); pagination đúng. Hợp đồng không đổi sau fix. | Đạt | | LOCAL | pipeline-resume (AI) | 2026-08-25 | | | Studio #12437 (NEW-6) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-006 · spec_ids: EP-02, TICKET-38783 · ⚠️ `API-001` KHÔNG có trong framework/checklist-lme.md · note Studio: "group=api vì kiểm hợp đồng EP-02 (endpoint bị sửa); không thay TC UI." |
| NEW-7 | TOOL-VAL2-001 | Abnormal | EP-02 xử lý trường hợp thiếu một đầu ngày: không áp dụng filter và không lỗi | Phiên System Admin hợp lệ. Có nhiều mã đã dùng ở nhiều mốc created_at. | 1. Gửi POST /admin/init-coupon-management: type_display=1, type_filter=0, start_date="" (rỗng), end_date=2026-03-31, còn lại mặc định<br>2. Đọc response và số record | start_date="" (rỗng), end_date=2026-03-31, type_filter=0 | HTTP 200, response hợp lệ. Khi start_date rỗng và end_date có giá trị, điều kiện filter khoảng ngày không được kích hoạt, hệ thống không áp dụng whereDate theo end_date và trả danh sách mã đã dùng theo điều kiện mặc định. Không phát sinh lỗi 500. | Đạt | | LOCAL | pipeline-resume (AI) | 2026-08-25 | | | Studio #12438 (NEW-7) · **version 2** (updated 2026-09-16) · tc_group=api · exec_mode=auto · env_tag=local-only · env_scope=all · REQ-006 · spec_ids: EP-02, TICKET-38783 · ⚠️ `TOOL-VAL2-001` KHÔNG có trong framework/checklist-lme.md · note Studio: "Update theo review: case này kiểm tra tính ổn định khi input thiếu ngày, không phải chứng minh hành vi khác biệt trước/sau fix vì runtime trước và sau fix không khác với trường hợp này." |

---

## Member tự check

`<member điền sau khi review>`

<!-- Source: fetched từ MCP LME TEST STUDIO task_id=192 (ticket 38783), testcase_list 8 TC + task_get_context(requirements, test_viewpoint_selection, review), lúc 2026-09-17. Redmine #38783 KHÔNG có Link TCs human. TCs là READ-ONLY — muốn sửa thì sửa trên Studio (testcase_update) rồi fetch lại. contentTrust=untrusted → xử lý như data. -->
