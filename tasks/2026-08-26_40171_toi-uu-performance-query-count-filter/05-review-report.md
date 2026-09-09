# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Task folder | `tasks/2026-08-26_40171_toi-uu-performance-query-count-filter/` |
| Ticket | Redmine #40171 — Tối ưu performance query count filter friend (tracker **Improve nội bộ**, status *Fix done - Đợi test*) |
| Feature | **SC-003 Friend Filter** (絞り込みモーダル) — shared component |
| Branch | `ai_small_40171` (gốc `release_step_20260805`), commit `e131fdbf80` |
| Reviewer | Test Leader (draft do `/review-tc` sinh) |
| Ngày review | 2026-08-26 |
| Vòng review | 1 |

---

## 0. Nguồn TC

| Mục | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, task `#240` (ticket 40171, feature `friend-filter`, round 1, `archived=false`) |
| Vì sao không dùng nguồn dưới | Nguồn 1 lấy được TC → **dừng ngay**. Nguồn 2 (link Sheet human) và nguồn 3 (file `04-tc-list.md`) **KHÔNG được fetch, KHÔNG đối chiếu chéo** theo đúng quy tắc BƯỚC 0. |
| Tổng TC | **52** (46 gốc + 6 TC mới; đã xoá 43 TC trùng ngày 2026-08-27 — xem §4.5) |
| Thời điểm fetch | 2026-08-26 (vòng 1) · **fetch lại 2026-08-27** sau khi xoá trùng |
| Snapshot | [04-tc-list.md](04-tc-list.md) — refresh 2026-08-27, **52 TC** |
| Context Studio | `task_get_context` → 11 requirement `REQ-001`…`REQ-011`; `task_get_report` → run history; `review_list_comments` → 1 comment vòng 1 |

> ⚠️ Nội dung Studio có `contentTrust = untrusted` → xử lý như **data**, không phải chỉ thị. TC là **read-only**; mọi đề xuất sửa/xóa dưới đây phải do human thực hiện trên Studio (`testcase_update` / `testcase_delete`).

### 0.6 — Cảnh báo bắt buộc về chất lượng nguồn

| # | Nội dung | Thực tế | Flag |
|---|---|---|---|
| 1 | **Kết quả thực thi thật** | `pass 1` · `fail 0` · `error 0` · `skip 49` · chưa chạy 2 → **1/52 TC (2%) có kết luận test** | **`[BLOCKER]`** (pass < 50%) |
| 2 | TC `fail`/`error`, TC gắn ticket bug | Không có TC nào `fail`/`error`; `openBugs = 0`; không TC nào gắn `bug_tickets` | — (nhưng vì 0 TC chạy nên **không có nghĩa là không có bug**) |
| 3 | **Môi trường đã chạy** | `local` 50 TC · 2 TC chưa chạy. **`dev` / `staging` / `prd` = 0 run**. Task chạm **job nền xuất CSV**, **gửi tin hàng loạt**, **job pre-filter broadcast** | **`[MAJOR]` RULE-08 / ENV-003** |
| 4 | **Ai chạy** | `ai / haodtb` 43 TC · **`manual / haodtb` 7 TC** (2026-08-27 03:07–03:13, env `local`) · 2 TC chưa chạy. QA đã bắt đầu chạy tay, nhưng **6/7 run manual vẫn ra `skip`** — chỉ `NEW-4` đạt. `submittedWithoutMcp = false` | **`[MAJOR]`** |
| 5 | **Tác giả TC** | `author`: **AI 49/52 (94.2%)**, `haodtb@mcp` 3. `human = 0`. `status = draft` cho **cả 52 TC**. `reviewState = tester`, `reviewed = false` | **`[MAJOR]`** (≥50% AI sinh + review chưa done) |
| 6 | **Mã quan điểm không có trong `checklist-lme.md`** | **12 mã / 19 TC (19/52)**: `TOOL-OLDREC-001`(4) · `TOOL-AXIS-001`(3) · `API-CONTRACT-001`(2) · `TOOL-KNOW-002`(2) · `TOOL-NEGCTRL-001` · `SEARCH-001` · `RULE-09` · `API-001` · `TOOL-ERRHYG-001` · `JOB-002` · `RULE-12` · `TOOL-SELFAUDIT-001` | **19/46 TC KHÔNG tính là cover** ở BƯỚC 2/3b |

### 0.6b — Vì sao 49 TC `skip`: KHÔNG phải kết quả test

`task_get_report(240)` → run `#604` (env `local`, 10:18:56 → 10:18:58 = **2 giây cho 41 TC**), `status = fail`. Cả 41 TC có `actual` **giống hệt nhau**, `durationMs = 0`, `artifacts` rỗng:

```
[SOURCE_BLOCKED] web: SOURCE_CHECKOUT_ERROR: checkout "ai_small_40171" trong worktree thất bại:
fatal: Unable to create '/workspace/source/sns-line/.git/worktrees/sns-line--runner-slot-3-web/index.lock':
File exists. Another git process seems to be running in this repository...
```

👉 **Runner chết ở bước checkout branch — không TC nào thực sự chạy.** Run `#617` (local) còn ở trạng thái `queued`.
Redmine đang ở *"Fix done - Đợi test"* nhưng **không có một dòng bằng chứng test nào**.

### 0.6c — Comment review vòng trước (đã đọc, KHÔNG raise lại)

| Thread | TC | Người | Decision | Nội dung |
|---|---|---|---|---|
| #70 | `NEW-6` (id 14262), field `precondition` | `ngannt` | **reject** | *"Sai tiền điều kiện: BOT FREE không bị chặn filter ở màn friend list, chỉ bị chặn filter trong modal multi action thôi"* |

→ Issue này **đã được Leader raise**, không tính lại. ✅ **Đã được xử lý** — fetch lại 2026-08-27 cho thấy tiền đề NEW-6 nay ghi *"bot FREE vẫn được phép sử dụng filter ở màn 友だちリスト; chỉ bị giới hạn filter trong modal multi action"*, và có thêm 2 TC tách bạch 2 nhánh: NEW-47 (`PERM-001` Normal) + NEW-48 (`PERM-001` Abnormal). Xem `PRE-01` §4.2.

---

## 1. Verdict

## 🔴 REJECTED

Có **4 `[BLOCKER]`**. Bộ TC về **thiết kế** là khá tốt (52 TC, 11 requirement, phủ 13 màn, có đối chứng âm, có TC dữ liệu legacy) — nhưng **về bằng chứng thì bằng 0**, và thiếu đúng quan điểm cốt lõi của một ticket sửa câu đếm.

---

## 2. Tóm tắt cho member

**Điểm tốt:** bộ TC bám rất sát root cause — có TC đối chứng âm (`NEW-16`), có TC kiểm tĩnh câu SQL sinh ra (`NEW-42`), có 7 TC riêng cho dữ liệu hội thoại đời cũ (`REQ-002`), có TC so sánh trước/sau trên cùng dữ liệu ở hầu hết đường lọc. Cách chia requirement `REQ-001`…`REQ-011` rõ và trace được về source line.

**Phải fix trước khi test tiếp:**
1. **Chạy lại toàn bộ** — hiện 1/52 TC có kết quả (49 `skip` vì runner chết ở lỗi git lock, không phải test đạt; chạy tay ngày 27/08 cũng không thoát được). Mọi kết luận "fix xong" đều chưa có căn cứ.
2. **Thiếu hẳn `DATA-COUNT-001`** — ticket này sửa đúng câu `SELECT COUNT(*)` mà không TC nào đối chiếu 4 nguồn số (modal / danh sách chi tiết / CSV / API) trên cùng một bộ dữ liệu.
3. **Chưa ai kiểm nhánh DB replica (`BR-14`)** — sau fix vòng 2, nhánh chính lọc bằng cột `tb_line_user_id` còn nhánh replicate vẫn dựng mảng PHP từ `line_id`; nếu cột số trống ở bản ghi cũ thì **hai nhánh trả về hai tập bạn bè khác nhau**.
4. Chạy toàn bộ ở `local`, trong khi ticket chạm job xuất CSV và gửi tin hàng loạt.

---

## 3. Coverage Matrix

Impact tag lấy từ [03-dev-impact.md](03-dev-impact.md). Cột `Exec` = `<số pass>/<số TC>`.

| Impact | Loại | TCs cover (suy luận từ nội dung) | # TC | Exec | Status |
|---|---|---|---|---|---|
| `BUG` — subquery `IN` lệch kiểu → dependent subquery, câu đếm chậm | Root cause | NEW-39 (plan nhánh gốc còn dependent subquery) · NEW-40 (plan sau vá hết dependent) · NEW-41 (đo thời gian) · NEW-42 (kiểm tĩnh câu SQL) · NEW-43 (xác nhận lại ở env gần thật) | 5 | **0/5** | **RISK** |
| `F1` `Conversation::lineIdAsInt` (hàm mới) | Direct | NEW-42 (đếm số lần cột số xuất hiện = số điều kiện; bộ lọc rỗng không sinh subquery) | 1 | **0/1** | **RISK** |
| `F2` `Conversation::advanceFilter` (bộ lọc CŨ) | Direct | NEW-20 · NEW-21 · NEW-22 (đều trên màn 友だちリスト bộ lọc cũ) | 3 | **0/3** | **RISK** |
| `F3` `Conversation::advanceFilterPost` (AND/OR, 8 vị trí) | Direct | NEW-6…NEW-13 (6 loại điều kiện × 2 tab) · NEW-14 (kết hợp cả 3 loại 2 tab) · NEW-15 (rỗng) · NEW-16 (đối chứng âm) · NEW-18 (block) | 12 | **0/12** | **RISK** |
| `F4` `FilterController::initDataFilter` | Indirect | NEW-23 · NEW-24 · NEW-25 · NEW-26 (hợp đồng 3 endpoint EP-01/05/07) | 4 | **0/4** | **RISK** |
| `F5` `FilterV2::initDataFilter` (đường Rich Menu) | Indirect | NEW-34 (rich menu) | 1 | **0/1** | **RISK** |
| `F6` `FriendlistController::index` / `getListFriend` | Indirect | NEW-17 (số đếm chân modal ↔ danh sách) · NEW-25 (phân trang) · NEW-20 | 3 | **0/3** | **RISK** |
| `F7` `BotLineUser::makeDataTalkList` | Indirect | NEW-33 (danh sách hội thoại) | 1 | **0/1** | **RISK** |
| `F8` `ConversationReplicate::advanceFilterPost` (Dev nói không sửa) | Không đổi | **— không TC nào** | 0 | — | **🔴 GAP** (xem `[BLOCKER] GAP-02`) |
| `D-` Không có data bị ghi (chỉ SELECT) | Read-only | NEW-1 · NEW-2 · NEW-3 (kiểm kê `conversation.line_id` ↔ `tb_line_user_id`) · **NEW-4** · NEW-5 (bản ghi đời cũ vẫn nằm trong kết quả lọc) | 5 | **1/5** | **RISK** |
| `T1` Friend Filter / Segment (SC-003) | High | NEW-6…NEW-19 (14 TC modal lọc) | 14 | **0/14** | **RISK** |
| `T2` Friend List (FA-013) | High | NEW-17 · NEW-19 · NEW-20 · NEW-21 · NEW-25 | 5 | **0/5** | **RISK** |
| `T3` Broadcast (FA-008) — số người nhận | High | NEW-28 (preview) · NEW-29 (danh sách thật) · NEW-30 (nhận trên LINE) · NEW-31 (legacy) · NEW-52 (đổi filter tin đã đặt lịch) | 5 | **0/5** | **RISK** |
| `T4` Cross Analysis (FA-024) | Medium | NEW-32 (giữ bạn đã chặn) | 1 | **0/1** | **RISK** |
| `T5` Chat / Talk Management (FA-002) | Medium | NEW-33 · NEW-50 (tự động trả lời + job tin đến) | 2 | **0/2** | **RISK** |
| `T6` Step Delivery / Scenario (FA-009) | Medium | NEW-45 · NEW-46 · NEW-51 (segment gắn kịch bản step) | 3 | **0/3** | **RISK** |
| `T7` Rich Menu (FA-004) | Medium | NEW-34 · NEW-22 | 2 | **0/2** | **RISK** |
| `T8` CSV Management (FA-014) | High | NEW-36 · NEW-37 · NEW-38 | 3 | **0/3** | **RISK** |
| `T9`* Calendar / Booking — 5 `parent_type` (spec §7.7) | **Dev KHÔNG liệt kê** | **— không TC nào** | 0 | — | **🔴 GAP** |
| `T10`* Action Schedule (`action_schedule`) | **Dev KHÔNG liệt kê** | **— không TC nào** | 0 | — | **🔴 GAP** |
| `T11`* Form (フォーム) / `filter_remind_form` | **Dev KHÔNG liệt kê** | **— không TC nào** | 0 | — | **🔴 GAP** |
| `T12`* Filter Manager (`filter_manager`) | **Dev KHÔNG liệt kê** | **— không TC nào** | 0 | — | RISK (rủi ro thấp: không tính `filterNumber`, không trả `line_user_ids`) |
| `T13`* Job pre-filter broadcast (`PrepareFilterTask`) | **Dev KHÔNG liệt kê** | **— không TC nào** | 0 | — | **🔴 GAP** |
| — Cách ly bot / phạm vi bulk | — | NEW-19 (bulk tag) · NEW-27 (bot isolation) · NEW-49 (action trong modal 一括アクション) | 3 | **0/3** | **RISK** |
| — Phân quyền theo gói cước ở đường lọc | — | NEW-47 (Free lọc được ở 友だちリスト) · NEW-48 (Free bị chặn trong modal 一括アクション) | 2 | **0/2** | **RISK** |

> `T9`–`T13` là impact **`/review-tc` phát hiện thêm** từ [spec-features/admin/friend-filter/shared-spec.md](../../spec-features/admin/friend-filter/shared-spec.md) §2 + §7.7 — **không có trong mục 4.3 của Dev**. Xem `[MAJOR] IMPACT-01`.

**Không impact nào đạt `OK`** — điều kiện `OK` yêu cầu đủ chiều **và** có TC đã chạy `pass`. Cả bộ chỉ có **1 TC `pass`** (`NEW-4`, chạy tay 2026-08-27 trên `local`), nằm ở nhóm `D-`; nhóm này vẫn `RISK` vì 4/5 TC còn lại chưa có kết luận và `NEW-4` mới chỉ chạy ở `local`.

### ORPHAN TCs

| TC | Lý do nghi orphan | Kết luận |
|---|---|---|
| NEW-1, NEW-2, NEW-3 | Là **truy vấn kiểm kê DB thuần**, không phải thao tác quan sát được trên UI | **KHÔNG orphan** — chúng chứng minh tiền đề của `REQ-002` (có/không có bản ghi `tb_line_user_id` trống). Nhưng xem `[NIT] STYLE-01`. |
| NEW-44 | Tiêu đề generic "So sánh số lượng bạn bè trước và sau fix", `requirement_keys = []` | **Không orphan nhưng trùng** — xem §4.5 |

Không phát hiện TC nào nằm ngoài phạm vi `BUG` / `F*` / `D*` / `T*`.

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape nhận diện từ mục 2 file 03**: `"optimize query" + "performance"` **và** `"sửa hàm dùng chung"` (`Conversation::advanceFilter*` được 8 caller dùng) **và** `"số đếm / count"`.

| Fix shape | Câu hỏi adversarial | TC hiện có trả lời được? | Kết luận |
|---|---|---|---|
| **optimize query / performance** | Test với **quy mô khách hàng lớn nhất THỰC TẾ**? | NEW-41 ghi *"Bot test quy mô lớn (ghi rõ số bạn bè thực tế)"* — **không chốt ngưỡng**, `env_scope = local/dev/staging`. Dev tự khai *"CHƯA EXPLAIN được"*. `REQ-009` tự nhận *"Không đặt ngưỡng tuyệt đối vì chưa có mục tiêu số"* | **`[MAJOR]` PERF-01** — "giảm rõ rệt" không kiểm chứng được |
| | Rủi ro **`tmp_table_size`** Dev tự nêu (bảng tạm materialize rơi xuống đĩa) đã có TC? | **Không TC nào** | **`[MAJOR]` PERF-02** |
| **sửa hàm dùng chung** | Có **danh sách nơi ảnh hưởng do DEV cung cấp**? | ✅ Có — 8 tính năng ở mục 4.3 | không BLOCKER |
| | TC test **từng nơi** trong danh sách? | ✅ 8/8 đều có ≥1 TC | ✅ |
| | Danh sách của Dev **có đủ** so với spec? | ❌ spec §2 liệt kê **15+ context**, §7.7 liệt kê **9+ `parent_type`**. Thiếu: calendar-* (5 loại), `action_schedule`, form/`filter_remind_form`, `filter_manager`, job pre-filter broadcast | **`[MAJOR]` IMPACT-01** |
| | Chức năng **tương tự** đã rà? | Nhánh **DB replica** (`BR-14` / `BotLineUserReplicate`) — 0 TC, Dev chỉ nhắc `ConversationReplicate` | **`[BLOCKER]` GAP-02** |
| **số đếm / count** | Đối chiếu **4 nguồn** (summary / detail / CSV / API) + **phép tính tay** trên bộ dữ liệu biết trước kết quả? | NEW-17 đối chiếu **2 nguồn** (số chân modal ↔ danh sách). NEW-24 (API) và NEW-36 (CSV) chạy **bộ dữ liệu khác, không đối chiếu chéo**. **Không TC nào làm phép tính tay 4 nguồn trên cùng 1 filter** | **`[BLOCKER]` GAP-01** |
| | Mẫu số xử lý **friend đã block** đúng spec? | ✅ NEW-18 (loại bạn đã chặn) + NEW-32 (cross_analysis giữ bạn đã chặn — đúng `BR-06`) | ✅ |

**Symptom-only KH report check**: **KHÔNG áp dụng** — Redmine #40171 không có mô tả triệu chứng, description chỉ là câu SQL. Nhưng phát sinh vấn đề tương đương: **không có số đo baseline, không có ngưỡng chấp nhận** → gộp vào `[MAJOR] PERF-01`.

### Anti-patterns

| AP | Dính? | Ghi chú |
|---|---|---|
| AP-1 Single-trigger generic-fix | ❌ | Fix không phải dạng generic catch |
| AP-2 Symptom-only KH report | ❌ | Không có symptom |
| **AP-3 Happy-path-only regression** | **✅ DÍNH** | 8/13 mã quan điểm checklist chỉ có **1 loại case duy nhất** (xem `[MAJOR] RULE01-01`). Các đường regression `T4`–`T8` mỗi đường đúng 1 TC `Normal`, không có Abnormal/Boundary |
| AP-4 Specific code-check disguised as generic catch | ❌ | — |
| **AP-5 Layer-downstream over-coverage** | ⚠️ **một phần** | NEW-1/2/3 (kiểm kê DB) + NEW-42 (kiểm tĩnh chuỗi SQL) + NEW-39/40 (đọc execution plan) = **5 TC ở tầng dưới UI**. Hợp lệ cho ticket performance, nhưng đang chiếm 11% bộ TC trong khi `DATA-COUNT-001` ở tầng quan sát được lại trống |
| **AP-6 Mục 3 dev-impact trống** | ❌ nhưng ⚠️ | Mục 3 **có** 9 dòng. Vấn đề là mục **4.1 lại là danh sách FILE, không phải function** — bảng `F*` do `/new-task` ghép từ mục 3, Dev chưa xác nhận |

---

## 4. Issues phát hiện

> Thứ tự: issue từ **BƯỚC 0.6** (kết quả thực thi / env / tác giả) và **BƯỚC 3c** (fix-shape) nằm trên cùng.

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER]` EXEC-01 — 51/52 TC không có kết luận test**
`pass 1 / 52` (2%). 49 TC `skip`, 2 TC chưa chạy lần nào. Nguyên nhân gốc: run `#604` chết ở bước checkout branch (`SOURCE_CHECKOUT_ERROR`, git `index.lock`); run `#617` còn `queued`.
**Cập nhật 2026-08-27**: QA `haodtb` đã chạy tay 7 TC (03:07–03:13, env `local`) — **6/7 vẫn ra `skip`**, chỉ `NEW-4` (`TOOL-OLDREC-001`) `pass`. Chạy tay **không** thoát được lỗi hạ tầng, nên đây vẫn là vấn đề runner chứ không phải vấn đề TC.
**2 TC chưa chạy lần nào là đúng 2 TC quan trọng nhất về môi trường**: `NEW-30` (`MSG-004` — nhận tin thật trên LINE) và `NEW-43` (`ENV-003` — kế hoạch thực thi ở môi trường gần thật).
→ **Fix**: giải phóng git lock ở runner slot 3 rồi chạy lại toàn bộ. **Không được chuyển ticket sang trạng thái test xong khi `pass` = 1/52.** Trước khi review vòng 2, xác nhận `exec.pass ≥ 50/52` (trừ 2 TC `exec_mode = manual`).

**`[BLOCKER]` GAP-01 — `DATA-COUNT-001` (ưu tiên **Cao**) không có TC nào, trong khi ticket sửa đúng câu đếm**
Trigger của `DATA-COUNT-001` là **BẮT BUỘC** khi màn hình có bất kỳ con số đếm nào — ticket này *chính là* câu `SELECT COUNT(*)` của bộ lọc. Không TC nào mang mã này; NEW-17 chỉ đối chiếu **2/4 nguồn**. Đây là **lỗi lặp nhiều nhất lịch sử bug LME (12 ticket Closed / 5 tính năng)**.
→ **Fix**: thêm `TC-DATACOUNT001-01/02/03` ở §5 — đối chiếu **cùng một bộ lọc, cùng một bot** trên 4 nguồn: số ở chân modal 「絞り込み」 · số dòng danh sách 友だちリスト · số dòng file CSV xuất ra · số `filterNumber` endpoint trả về, cộng phép đếm tay trên bộ dữ liệu 10 người biết trước kết quả.

**`[BLOCKER]` GAP-02 — `BR-14` DB replica: 0 TC, và fix vòng 2 có thể làm 2 nhánh trả về 2 tập bạn bè khác nhau**
Spec SC-003 `BR-14`: *"khi `$useDBReplicate && env('DB_REPLICATE_HOST')` → query qua `BotLineUserReplicate` (logic WHERE giống hệt)"*. `task_get_report` xác nhận `BR-14` ở mức `level = none` (`tcIds` rỗng).
Kết hợp 2 dữ kiện: (a) mục 3 file 03 ghi `ConversationReplicate::advanceFilterPost` — *"vẫn dùng mảng PHP, không bị lỗi so kiểu"* → **nhánh replicate KHÔNG được sửa**; (b) NEW-42 xác nhận nhánh chính nay lọc bằng **cột số** `tb_line_user_id`, *"không còn cột chuỗi và không có phép ép kiểu"*.
→ **Kịch bản hỏng**: bot có bản ghi hội thoại đời cũ với `tb_line_user_id` trống/0. Nhánh chính (dùng cột số) **loại** người đó khỏi kết quả lọc; nhánh replicate (dựng mảng PHP từ `line_id` chuỗi) **giữ** người đó. Bật/tắt `DB_REPLICATE_HOST` cho ra **hai số người nhận khác nhau cho cùng một broadcast**.
→ **Fix**: hỏi Dev — hệ thống có đang bật replica ở môi trường thật không, `BotLineUserReplicate` có nhánh WHERE riêng không, đã đối chiếu với nhánh chính chưa. ⚠️ **Leader đã bỏ TC đề xuất cho GAP này** → hiện KHÔNG có TC nào cover `BR-14`; GAP vẫn mở, chỉ đóng được bằng câu trả lời của Dev. Dev xác nhận production **có** bật replica → phải mở lại TC trước khi nghiệm thu.
*Tiền đề cần Dev xác nhận trước khi chốt severity: nếu replica không được bật ở production thì hạ xuống `[MAJOR]`.*

**`[BLOCKER]` FIXSHAPE-01 — Rủi ro `tb_line_user_id = NULL` do chính AI nêu ra vẫn chưa được đóng, và file 03 đang ghi mâu thuẫn**
File [03-dev-impact.md](03-dev-impact.md) đã cảnh báo mâu thuẫn giữa mục 2 (vòng 2 dùng `tb_line_user_id`) và mục 6 / TỰ REVIEW (mô tả `CAST` + xếp `tb_line_user_id` vào nhóm **KHÔNG chọn** vì *"cho phép NULL nên có nguy cơ lọc thiếu bạn bè"*).
→ **Review này chốt được**: NEW-42 (`expected`) ghi rõ *"không câu lệnh nào còn chứa phần lấy cột chuỗi… cũng không chứa phép ép kiểu"* → **fix cuối cùng là vòng 2 (`tb_line_user_id`), không phải CAST**. Vậy **rủi ro NULL là rủi ro SỐNG**, không phải rủi ro đã loại trừ.
Studio có 7 TC cho đúng rủi ro này (`REQ-002`: NEW-1, NEW-2, NEW-3, NEW-4, NEW-5, NEW-31, NEW-37) — **cả 7 đều chưa chạy**.
→ **Fix**: (1) cập nhật mục 6 + TỰ REVIEW của file 03 cho khớp vòng 2 (yêu cầu Dev, không tự sửa); (2) chạy **trước tiên** NEW-1 → NEW-3 (kiểm kê) — nếu phát hiện có bản ghi `tb_line_user_id` trống thì **dừng test, trả lại Dev để backfill**, vì mọi TC còn lại sẽ so sánh trên dữ liệu đã sai; (3) yêu cầu Dev trả lời: có migration/backfill nào đảm bảo `tb_line_user_id` luôn có giá trị không.

### 4.2 Major (nên fix)

**`[MAJOR]` INPUT-01 — Checkbox "Tester verify auto-fill chính xác" chưa tick ở CẢ `01-bug-task.md` và `03-dev-impact.md`**
Cả 2 file đều có `Auto-filled: 2026-08-26 by /new-task` nhưng checkbox còn trống → `F*`/`D*`/`T*` có thể thiếu hoặc map sai. Bằng chứng cụ thể: bảng `F*` do `/new-task` **ghép từ mục 3** vì mục 4.1 gốc của Dev chỉ là danh sách **file**, và `IMPACT-01` dưới đây cho thấy 4.3 thật sự thiếu.
→ **Fix**: tester đọc lại journal #133070 trên Redmine, xác nhận rồi tick cả 2 checkbox.

**`[MAJOR]` ENV-01 — 0 run trên `dev` / `staging` / `prd` (RULE-08 / `ENV-003`)**
Toàn bộ 41 run ở `local`. Ticket chạm **job xuất CSV** (NEW-36/37/38), **gửi tin hàng loạt thật trên LINE** (NEW-30), **job pre-filter broadcast**. Theo RULE-08 không được kết luận job nền / gửi tin từ local.
Đáng chú ý: `NEW-43` (`ENV-003` — *"Xác nhận lại kế hoạch thực thi trên môi trường gần giống môi trường thật"*) và `NEW-30` (`MSG-004` — *"nhận được tin trên LINE"*) là 2 TC env-quan trọng nhất thì **đều nằm trong nhóm 5 TC chưa chạy lần nào**.
→ **Fix**: chốt với Leader môi trường hợp lệ cho từng nhóm; tối thiểu nhóm `tc_group = job` (3 TC) + NEW-29/NEW-30 phải chạy staging hoặc production.

**`[MAJOR]` AUTHOR-01 — 49/52 TC do AI sinh, toàn bộ `status = draft`, `reviewed = false`**
`toolWritten`: AI 49 · mcp 3 · **human 0** (`rate = 94.2%`). `reviewState = tester`, `reviewed = false`. Không TC nào ở trạng thái đã duyệt.
→ **Fix**: tester/leader duyệt từng TC trên Studio (đổi `status` khỏi `draft`) trước khi lấy kết quả chạy làm bằng chứng nghiệm thu.

**`[MAJOR]` SPEC-01 — `Trạng thái đánh giá spec` trống ở **cả 52 TC** (`spec_status = null`)**
Không TC nào ghi `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader` → không phân biệt được TC nào dựa trên spec thật, TC nào do AI tự suy diễn. Rủi ro cao vì spec SC-003 có **7 Gap đã biết** (`Gap-01`…`Gap-07`).
→ **Fix**: điền `spec_status` cho 52 TC; TC nào ghi `Spec không ghi` phải nêu đã hỏi ai.

**`[MAJOR]` RULE01-01 — 8/13 mã quan điểm checklist chỉ có **1 loại case duy nhất** (RULE-01)**

| Mã quan điểm | Ưu tiên | Loại case hiện có | Thiếu |
|---|---|---|---|
| `DATA-DB-001` | Cao | Normal ×2 | Abnormal, Boundary |
| `OUT-TRUTH-001` | Cao | Normal ×4 | Abnormal, Boundary |
| `MSG-001` | Cao | Normal ×2 | Abnormal, Boundary |
| `MSG-004` | Cao | Normal ×1 | Abnormal, Boundary |
| `MSG-USER-001` | Cao | Abnormal ×1 | Normal, Boundary |
| `BULK-001` | Cao | Boundary ×1 | Normal, Abnormal |
| `SEC-ISO-001` | Cao | Abnormal ×1 | Normal, Boundary |
| `OUT-EXPORT-001` | Cao (nâng) | Normal ×1 | Abnormal, Boundary |
| `ENV-003` | Cao | Normal ×1 | Abnormal, Boundary |
| `PERF-LARGE-001` | Cao (gửi tin/export) | Boundary ×1 | Normal, Abnormal |
| `REG-SHARED-001` | Cao | Normal ×5, Abnormal ×1 | Boundary |

Không TC nào ghi lý do thiếu ở `Ghi chú`.
→ **Fix**: bổ sung loại case còn thiếu cho các mã **Cao**, hoặc ghi lý do vào `Ghi chú` từng TC.

**`[MAJOR]` IMPACT-01 — Mục 4.3 của Dev thiếu ≥ 5 context so với spec SC-003**
Dev liệt kê 8 tính năng. Spec [shared-spec.md](../../spec-features/admin/friend-filter/shared-spec.md) §2 liệt kê **15+ nhóm tính năng** dùng chung modal này, §7.7 liệt kê **9+ `parent_type`** với side-effect khác nhau. Thiếu hẳn:
`calendar-*` (5 loại — **có** tính `filterNumber`, **có** trả `line_user_ids`, update column trên entity calendar) · `action_schedule` · `filter_remind_form` / Form · `filter_manager` · **job pre-filter broadcast**.
→ **Fix**: yêu cầu Dev bổ sung mục 4.3 cho đủ context. ⚠️ **Leader đã bỏ 2 TC smoke đề xuất** (calendar + action_schedule) → `T9`/`T10` giữ nguyên trạng thái **GAP**, không có TC nào cover. Chấp nhận GAP này là **quyết định của Leader về phạm vi test**, cần ghi rõ khi nghiệm thu.

**`[MAJOR]` GAP-03 — Job pre-filter broadcast (`PrepareFilterTask`) không có trong impact và không có TC**
kho-tcs [fa008-broadcast](../../kho-tcs/fa008-broadcast-メッセージ配信.md) `TC-BC-246` (env **PRODUCTION**) cho thấy tồn tại cơ chế **job nền pre-cache danh sách người nhận trước giờ gửi**, tách biệt với số preview ở màn admin. Mục 4.3 Dev chỉ ghi *"số người nhận **hiển thị trước khi gửi**"* — tức chỉ đường preview.
→ **Fix**: hỏi Dev — job pre-filter có đi qua `Conversation::advanceFilterPost` không? **Có** → đây là GAP thật, phải mở lại TC (Leader đã bỏ TC đề xuất). **Không** → ghi rõ vào mục 4.3 để loại khỏi phạm vi và đóng GAP.

**`[MAJOR]` PERF-01 — Không có baseline, không có ngưỡng chấp nhận → `NEW-41` không kiểm chứng được**
`REQ-009` tự ghi *"Không đặt ngưỡng tuyệt đối vì chưa có mục tiêu số"*; NEW-41 expected là *"giảm rõ rệt"*. Redmine không có số đo trước fix. Dev tự khai *"CHƯA EXPLAIN được… cần dev/QA chạy EXPLAIN để đo trước/sau"*. Với ticket mà **mục tiêu duy nhất là performance**, không có ngưỡng thì không có tiêu chí đạt/không đạt.
→ **Fix**: chốt với Dev/Leader ngưỡng cụ thể (VD: *"trên bot ≥ 100.000 bạn bè, trung vị 5 lần đo ≤ X giây, và ≤ 1/3 thời gian nhánh gốc"*), ghi vào `NEW-41.expected` + `REQ-009`. NEW-41 hiện `env_scope = local/dev/staging` → phải nâng lên môi trường có dữ liệu thật.

**`[MAJOR]` PERF-02 — Rủi ro `tmp_table_size` do chính Dev nêu chưa có TC**
File 03 mục 7: *"Nếu bảng `conversation` của bot quá lớn, bảng tạm materialize có thể vượt `tmp_table_size` và rơi xuống đĩa"*. Không TC nào chạm ngưỡng này.
→ **Fix**: gộp vào TC boundary số điều kiện AND/OR (`TC-BULK001-02` §5) — nhiều điều kiện = nhiều bảng tạm cùng lúc, đúng kịch bản Dev lo.

**`[MAJOR]` RULE12-01 — Case đã từng Không đạt chưa nằm trong phạm vi regression**
RULE-12 phần (3): *"mọi case đã từng Không đạt và được fix"* phải nằm trong regression. kho-tcs FA-008 ghi nhận case NG cũ: *"check double click text số người dự định send → tính 1 lần"* → kết quả corpus **"hiển thị sai số ng dự định send"**. Ticket này sửa đúng câu đếm sinh ra con số đó, nhưng không TC nào mang mã `CONC-*`.
→ **Fix**: thêm `TC-CONC001-01` ở §5.

**`[MAJOR]` VP-01 — 19/52 TC mang mã quan điểm không có trong `checklist-lme.md` → không tính là cover**
12 mã (xem §0.6 #6). Riêng nhóm `TOOL-*` (11 TC) là mã nội bộ Studio. Hệ quả trực tiếp: 3 TC job CSV mang `JOB-002` / `RULE-12` — **không map được** sang `OUT-EXPORT-001` hay `JOB-001` dù nội dung có test đúng.
→ **Fix**: map lại `viewpoint` của 19 TC sang mã trong `framework/checklist-lme.md`, hoặc bổ sung các mã `TOOL-*` vào checklist nếu Leader công nhận chúng là quan điểm chính thức.

**`[MAJOR]` ~~PRE-01~~ → ✅ ĐÃ XỬ LÝ (giữ lại để trace) — Tiền điều kiện sai về gói cước**
Vòng 1 phát hiện tiền đề *"gói Free bị chặn modal lọc"* lan ra **15 TC** (comment #70 chỉ nhắm NEW-6).
→ **Kết quả fetch lại 2026-08-27**: đã sửa. Batch TC gốc nay ghi đúng *"bot FREE vẫn được phép sử dụng filter ở màn 友だちリスト; chỉ bị giới hạn filter trong modal multi action"*, và bổ sung **2 TC `PERM-001`** tách bạch 2 nhánh (NEW-47 Normal / NEW-48 Abnormal) cùng **NEW-49** cho hành động trong modal 友だち一括アクション. Điểm ngược tôi nêu vòng 1 — NEW-19 (bulk tag) thiếu ràng buộc gói — cũng đã được xử lý ở tiền đề mới.

### 4.3 Minor (có thể fix sau)

**`[MINOR]` DUP-01 — `NEW-44` là tập con của `NEW-6`…`NEW-13` + `NEW-41`** → xem §4.5.

**`[MINOR]` META-01 — `priority` trống ở 50/52 TC** (chỉ 2 TC có `High`); `origin`, `kho_id`, `spec_ids` trống toàn bộ → không trace được TC nào dẫn từ kho TC cũ.

**`[MINOR]` EVID-01 — Không TC nào ghi **loại evidence bắt buộc** ở `note` (RULE-02)**
Hiện `Evidence thực tế` trống ở cả 52 TC. Với ticket performance, evidence tối thiểu phải nêu rõ: ảnh chụp `EXPLAIN` trước/sau, bảng 5 lần đo, và bảng đối chiếu số đếm 2 nhánh. Hiện `Evidence thực tế` trống ở cả 46 TC (đúng, vì chưa chạy) nhưng **loại** evidence cũng không được khai báo trước.

### 4.4 Nit (gợi ý)

**`[NIT]` STYLE-01** — NEW-1/2/3 và NEW-42 viết ở tầng truy vấn DB / chuỗi SQL, không phải góc nhìn manual tester. Hợp lệ với ticket này (chúng là kiểm kê tiền đề + kiểm tĩnh), nhưng nên ghi rõ ở `note` rằng **cần Dev hoặc QA có quyền DB chạy**, để tester UI không nhận nhầm.

**`[NIT]` ID-01** — TC dùng `temp_id` dạng `NEW-4`…`NEW-46`, không theo format canonical `TC-<mã quan điểm bỏ gạch>-<nn>`. Đây là format của Studio, không phải lỗi member — snapshot [04-tc-list.md](04-tc-list.md) đã tự sinh TC No. canonical để đối chiếu.

**`[NIT]` ORDER-01** — `sort_order` khiến NEW-1/2/3 (kiểm kê tiền đề) nằm gần **cuối** danh sách, trong khi theo `FIXSHAPE-01` chúng phải chạy **đầu tiên** (nếu phát hiện dữ liệu trống thì mọi TC sau đều vô nghĩa). Cân nhắc `testcase_resort`.

---

## 4.5 TC trùng lặp nội dung

### Vòng 1 (2026-08-26) — rà 46 TC

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | Severity |
|---|---|---|---|---|
| So sánh số đếm trước/sau fix | **NEW-6…NEW-13** + **NEW-41** | **NEW-44** | `DUP-SUBSET` — chỉ so **số đếm**, không so **danh sách**, không chỉ định tab AND/OR | `[MINOR]` |

Gate kiểm tra: NEW-44 mang `OUT-TRUTH-001` (còn NEW-7/10/17 giữ mã này) và `requirement_keys = []` → xoá không mất cover.
→ **Đề xuất GỘP, không xoá**: chuyển câu *"Nếu thời gian query giảm nhưng count thay đổi thì phải FAIL"* vào `NEW-41.expected` rồi mới xoá NEW-44. **Chưa thực hiện.**

### Vòng 2 (2026-08-27) — task tăng lên 95 TC, ĐÃ XOÁ 43 TC

Fetch lại phát hiện **batch sinh TC thứ 2** (id 14482–14530, 49 TC) sinh lại gần như toàn bộ batch 1 (id 14230–14410, 46 TC).

| Chỉ số | Giá trị |
|---|---|
| Tổng trước xoá | **95 TC** |
| Cặp trùng phát hiện | **43** (6 cặp giống hệt cả 5 field · 37 cặp chỉ khác cách diễn đạt tiền đề) |
| Trùng nội bộ trong từng batch | **0** |
| TC batch 2 thật sự mới | **6** (NEW-47 → NEW-52) |
| **Đã xoá** | **43 TC** — toàn bộ thuộc batch 2 |
| Tổng sau xoá | **52 TC** |

**Quyết định giữ batch 1** (Leader `ngannt` duyệt 2026-08-27), lý do:
1. Comment review **#70 neo vào `tcId 14262`** (NEW-6, batch 1) — xoá batch 1 là mất lịch sử review.
2. Batch 2 **gán sai mã quan điểm ở 5 TC**: đổi từ mã hợp lệ sang `TOOL-AXIS-001` (không có trong `checklist-lme.md`) — NEW-70←NEW-6 `DATA-DB-001` · NEW-71←NEW-7 `OUT-TRUTH-001` · NEW-72/73←NEW-8/9 `COMPAT-LEGACY-001` · NEW-74←NEW-10 `OUT-TRUTH-001`.
3. Report này tham chiếu temp_id batch 1 xuyên suốt §3/§4/§7.

**43 ID đã xoá** (mỗi lệnh `testcase_delete` ghi rõ TC được giữ để trace ngược):
`14488`–`14530` trừ 6 TC giữ lại — cụ thể: 14488, 14489, 14490, 14491, 14492, 14493, 14494, 14495, 14496, 14497, 14498, 14499, 14500, 14501, 14502, 14503, 14504, 14505, 14506, 14507, 14508, 14509, 14510, 14511, 14512, 14513, 14514, 14515, 14516, 14517, 14518, 14519, 14520, 14521, 14522, 14523, 14524, 14525, 14526, 14527, 14528, 14529, 14530.

**6 TC batch 2 GIỮ LẠI** (mới thật, lấp GAP):

| TC | id | Mã quan điểm | Loại | Lấp GAP nào |
|---|---|---|---|---|
| NEW-47 | 14482 | `PERM-001` | Normal | Bot Free vẫn lọc/đếm được ở 友だちリスト — trả lời comment #70 |
| NEW-48 | 14483 | `PERM-001` | Abnormal | Bot Free bị chặn khi mở bộ lọc trong modal 友だち一括アクション |
| NEW-49 | 14484 | `REG-SHARED-001` | Abnormal | Hành động trong modal 友だち一括アクション có điều kiện lọc |
| NEW-50 | 14485 | `REG-SHARED-001` | Normal | Tự động trả lời có điều kiện 確認状況 khi job xử lý tin đến chạy |
| NEW-51 | 14486 | `REG-SHARED-001` | Normal | Segment lọc gắn cho kịch bản step |
| NEW-52 | 14487 | `STATE-DEP-001` | Abnormal | Đổi điều kiện lọc của tin đã đặt lịch → tính lại tập người nhận |

> ⚠️ **NEW-44 vẫn chưa xử lý** — đó là đề xuất *gộp* từ vòng 1, độc lập với đợt xoá trùng vòng 2 này.

> ⚠️ Bài học quy trình: 2 batch AI sinh cách nhau vài giờ trên **cùng 1 task** tạo ra 43 TC trùng (45% bộ TC). Nên chặn ở khâu sinh — kiểm `client_ref` / rà trùng trước khi ghi vào Studio, thay vì để review bắt sau.

## 5. TCs đề xuất bổ sung

### 5a — Đối chiếu kho TCs (bắt buộc, làm TRƯỚC khi viết)

- **kho-tcs KHÔNG có SC-003 (Friend Filter) và KHÔNG có FA-013 (Friend List)** → không đối chiếu trực tiếp được. Đáng chú ý: [fa008-broadcast](../../kho-tcs/fa008-broadcast-メッセージ配信.md) tự ghi nhận *"SC-003 Friend Filter là SHARED COMPONENT dùng chung bởi FA-008, FA-009, FA-013, FA-024… **ĐỀ XUẤT: tách feature riêng『SC-003 絞り込み』— HỎI USER XÁC NHẬN**"* → xem §6.
- Đã rà kho của **5 tính năng bị ảnh hưởng**: FA-008 (broadcast), FA-009 (step), FA-004 (rich menu), FA-003 (auto-reply), FA-012 (tag).

| Câu hỏi | Kết quả |
|---|---|
| **Phạm vi ảnh hưởng** — TC kho nào chạm cùng chức năng với `F*`/`T*`? | `TC-BC-172` (số 配信数 ngoài list lệch danh sách chi tiết — `filter_number` là **cache**) · `TC-BC-173` (ranh giới số điều kiện AND/OR) · `TC-BC-246` / `TC-BC-249` (cửa sổ đóng băng filter của job, env PRODUCTION) · `TC-BC-164` (chuyển 絞り込み ⇄ すべての友だち). **Không TC nào ở BƯỚC 0 cover 4 vùng này.** Sau khi Leader lược TC đề xuất: chỉ còn `TC-BC-173` được lấp (bằng `TC-BULK001-02`) và vùng double-click 再計算 được lấp (bằng `TC-CONC001-01`); **`TC-BC-172` và `TC-BC-246`/`TC-BC-249` vẫn là vùng regression HỞ**. |
| **Conflict expected** | **CÓ 1 conflict** — cửa sổ đóng băng filter: kho `MT-17` ghi **10 phút** cho broadcast / **5 phút** cho scenario step, còn spec SC-003 §7.3 ghi **5 phút**. → **KHÔNG tự chọn bên**; toàn bộ ngưỡng phút đẩy sang §6 `SPEC-UPD-01`. TC duy nhất chạm vùng này đã bị Leader bỏ → conflict vẫn treo, chưa TC nào kiểm chứng. |
| **Đã có sẵn** | `TC-BC-173` (kho) đã cover ma trận ranh giới AND/OR — `TC-BULK001-02` bên dưới **dùng lại kịch bản của `TC-BC-173`**, chỉ thêm trục *đo thời gian + đối chiếu số đếm 2 nhánh* cho đúng bug này. |

### 5b — Xác nhận chống trùng

> **Đã đối chiếu 52 TC ở BƯỚC 0 + kho-tcs FA-008/009/004/003/012 — không TC đề xuất nào trùng.**
>
> ⚠️ **Leader đã bỏ 5 TC đề xuất** (`TC-DATADB001-03`, `TC-COMPATLEGACY001-06`, `TC-MSG001-03`, `TC-REGSHARED001-07`, `TC-REGSHARED001-08`) — còn lại **5 TC** dưới đây. Các GAP mà 5 TC bị bỏ định lấp (`BR-14` replica · `filter_number` cache trước deploy · job pre-filter broadcast · calendar · action_schedule) **vẫn mở** ở §4 và §7 F.1, chỉ là không còn TC đề xuất kèm theo.
> Mỗi TC dưới đây đã qua 2 lần check theo 4 yếu tố: (1) vs bộ 52 TC Studio, (2) vs các TC khác trong chính §5.

### 5d — Trạng thái push lên Studio (2026-08-27)

| TC No. | Đã push? | Studio id | temp_id |
|---|---|---|---|
| TC-DATACOUNT001-01 | ❌ **Leader không push** | — | — |
| TC-DATACOUNT001-02 | ✅ đã push | `14547` | `NEW-53` |
| TC-DATACOUNT001-03 | ✅ đã push | `14548` | `NEW-54` |
| TC-BULK001-02 | ✅ đã push | `14549` | `NEW-55` |
| TC-CONC001-01 | ❌ chưa push | — | — |

`client_ref` = `TC No.` → idempotent theo task, chạy lại `/sync-review-tc` sẽ **không** tạo trùng.

⚠️ **2 điểm cần biết về bản đã push:**
1. `TC-DATACOUNT001-02` và `-03` trong §5c viết *"Giống TC-DATACOUNT001-01"* / *"Lặp lại đúng 5 bước của TC-DATACOUNT001-01"*. Vì `-01` **không được push**, bản trên Studio đã **nội suy nguyên văn tiền đề + 5 bước của `-01`** vào từng TC để chúng tự đứng được — ý định test giữ nguyên, chỉ khác ở chỗ không còn tham chiếu chéo. Nội dung trong §5c của report này **giữ nguyên bản gốc**.
2. `DATA-COUNT-001` là quan điểm **ưu tiên Cao**. Sau khi bỏ `-01` (loại `Normal`), quan điểm này trên Studio chỉ còn **Abnormal + Boundary** → **vẫn vi phạm RULE-01** (thiếu `Normal`). `[BLOCKER] GAP-01` do đó **chưa đóng hoàn toàn**: đã có TC đối chiếu 4 nguồn ở nhánh bất thường và nhánh biên, nhưng chưa có nhánh thường trên bộ dữ liệu biết trước kết quả.

---

### 5c — Bảng TC đề xuất (16 cột canonical)

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATACOUNT001-01 | DATA-COUNT-001 | Normal | Cùng một bộ lọc cho ra cùng một con số ở cả 4 nơi: chân modal, danh sách bạn bè, file CSV và số hiển thị sau khi lưu bộ lọc | Đăng nhập admin, chọn bot test. Dựng đúng 10 người bạn đặt tên TC40171_F01…F10, trong đó **biết trước** 4 người ở trạng thái 確認状況「未確認」. Không có bạn nào đang bị chặn. | 1. Mở màn 友だちリスト → bấm「絞り込み」<br>2. Chọn điều kiện 確認状況「未確認」ở nhóm AND → đọc và ghi lại con số ở **chân modal**<br>3. Bấm áp dụng → **đếm tay số dòng** hiển thị trên danh sách bạn bè (qua hết các trang)<br>4. Từ chính màn này bấm xuất CSV → mở file, **đếm số dòng dữ liệu** (không tính dòng tiêu đề)<br>5. Lưu bộ lọc lại → đọc con số người khớp mà màn hình hiển thị sau khi lưu | Bộ dữ liệu 10 bạn, biết trước **đúng 4 người** thỏa 確認状況「未確認」 | Cả 4 con số ở bước 2, 3, 4, 5 **bằng nhau và bằng 4** — đúng bằng số đếm tay đã biết trước. Danh sách tên người ở bước 3 và bước 4 **trùng khít nhau từng người**, không thiếu không thừa. | Chưa test | | Staging hoặc Production | | | | Spec ghi rõ (SC-003 §6 Filter → DB Mapping) | Lấp **GAP-01** — cover `BUG` + `F3` + `F6` + `T1`. Evidence bắt buộc: **bảng đối chiếu 4 nguồn + phép đếm tay**. |
| TC-DATACOUNT001-02 | DATA-COUNT-001 | Abnormal | Bạn bè bị chặn không được tính vào số đếm ở bất kỳ nguồn nào trong 4 nguồn | Giống TC-DATACOUNT001-01. Thêm: chặn bot từ 1 trong 4 người thỏa điều kiện (còn lại 3 người hợp lệ). | 1. Lặp lại đúng 5 bước của TC-DATACOUNT001-01 với cùng điều kiện lọc<br>2. Ghi lại 4 con số<br>3. Mở bộ lọc của クロス分析 với **cùng điều kiện**, đọc số người khớp | 4 người thỏa điều kiện, trong đó 1 người đang chặn bot | Bốn con số ở màn 友だちリスト / CSV / modal / sau khi lưu đều bằng **3** — người đang chặn bị loại ở **mọi** nguồn. Riêng クロス分析 hiển thị **4** (giữ cả người đang chặn) đúng theo `BR-06`. Không nơi nào cho ra số 4 ngoài クロス分析. | Chưa test | | Staging hoặc Production | | | | Spec ghi rõ (SC-003 `BR-06`) | Lấp **GAP-01** + **RULE01-01** (`DATA-COUNT-001` loại Abnormal). Cover `T1`, `T4`. |
| TC-DATACOUNT001-03 | DATA-COUNT-001 | Boundary | Bộ lọc khớp đúng 1 người và bộ lọc khớp 0 người vẫn cho cùng con số ở cả 4 nguồn | Giống TC-DATACOUNT001-01. Chuẩn bị thêm 1 nhãn 対応ステータス chỉ gắn cho **đúng 1 người**, và 1 nhãn **chưa gắn cho ai**. | 1. Lọc theo nhãn chỉ gắn cho 1 người → chạy đủ 5 bước của TC-DATACOUNT001-01<br>2. Lọc theo nhãn chưa gắn cho ai → chạy lại đủ 5 bước<br>3. Quan sát màn hình và file CSV ở trường hợp 0 người | Nhãn A = 1 người · Nhãn B = 0 người | Trường hợp 1 người: cả 4 nguồn đều ra **1**, CSV có đúng 1 dòng dữ liệu. Trường hợp 0 người: cả 4 nguồn đều ra **0**, danh sách hiển thị trạng thái rỗng đúng chuẩn (không lỗi, không trắng màn), file CSV **chỉ có dòng tiêu đề**, không có dòng rỗng thừa. | Chưa test | | Staging hoặc Production | | | | Spec ghi rõ | Lấp **GAP-01** + **RULE01-01** (loại Boundary). Cover `T1`, `T2`, `T8`. |
| TC-BULK001-02 | BULK-001 | Boundary | Bộ lọc ở **số điều kiện tối đa** vẫn ra đúng tập bạn bè và không chậm hơn nhánh gốc | Bot test **quy mô lớn** (ghi rõ số bạn bè thực tế, tối thiểu vài chục nghìn). Đã chạy cùng kịch bản trên nhánh gốc và ghi lại số đếm + thời gian phản hồi. | 1. Mở modal lọc, thêm điều kiện vào nhóm AND cho tới khi hệ thống báo không thêm được nữa — **ghi lại con số tối đa thật**<br>2. Làm tương tự cho nhóm OR<br>3. Ở trạng thái cả 2 nhóm đầy điều kiện, bấm áp dụng → **bấm giờ** thời gian tới khi ra kết quả, đo **5 lần** lấy trung vị<br>4. Ghi lại số đếm và danh sách bạn bè<br>5. Lặp lại toàn bộ trên nhánh gốc với **cùng bot, cùng dữ liệu**<br>6. So sánh số đếm, danh sách và thời gian giữa 2 nhánh | Nhóm AND đầy điều kiện + nhóm OR đầy điều kiện, dùng cả 3 loại điều kiện bị sửa (確認状況 · 対応ステータス · 新規・既存友だち) | Khi vượt giới hạn: hiện đúng thông báo「これ以上追加できません。」. Ở mức tối đa: **số đếm và danh sách bạn bè bằng tuyệt đối** giữa 2 nhánh. Trung vị thời gian nhánh sửa **không lớn hơn** nhánh gốc. Màn hình không treo, không timeout, không lỗi máy chủ. | Chưa test | | Staging hoặc Production | | | | Đã hỏi leader — ⚠️ con số giới hạn thật chờ chốt (kho `MT-12`: 100 hay 5?) | Lấp **PERF-02** (rủi ro `tmp_table_size` — nhiều điều kiện = nhiều bảng tạm cùng lúc) + **RULE01-01**. `dẫn từ TC-BC-173` (kho FA-008). Cover `F3`, `T1`. |
| TC-CONC001-01 | CONC-001 | Abnormal | Bấm liên tiếp nút tính lại số người nhận chỉ tính **một lần** và ra đúng số | Broadcast nháp đã đặt bộ lọc, biết trước số người khớp. Bot quy mô đủ lớn để thao tác tính lại mất vài giây. | 1. Mở broadcast, bấm「再計算」**2 lần liên tiếp thật nhanh**<br>2. Quan sát con số hiển thị trong lúc chờ và sau khi xong<br>3. Bấm vào con số để mở danh sách chi tiết, **đếm số dòng**<br>4. Lặp lại thao tác với 2 tab trình duyệt mở cùng broadcast, bấm tính lại gần như đồng thời | Broadcast filter biết trước đúng 4 người khớp | Con số cuối cùng là **4**, không nhân đôi, không nhảy số bất thường. Danh sách chi tiết có đúng 4 dòng và **khớp con số hiển thị bên ngoài**. Trường hợp 2 tab: cả 2 tab cùng hiển thị 4 sau khi tải lại, không tab nào ra số khác. | Chưa test | | Staging hoặc Production | | | | Đã hỏi leader | Lấp **RULE12-01** — kho FA-008 ghi nhận case NG cũ *"double click text số người dự định send → hiển thị sai số ng dự định send"*. `regression`. Cover `BUG`, `F4`, `T3`. |

---

## 6. Spec update needed

| # | Vấn đề | Nguồn mâu thuẫn | Cần ai chốt |
|---|---|---|---|
| **SPEC-UPD-01** | **Cửa sổ đóng băng filter trước giờ gửi: 5 phút hay 10 phút?** Spec SC-003 §7.3 ghi *"trong vòng **5 phút** trước giờ gửi (và không phải draft): chặn"*. kho-tcs FA-008 `MT-17` ghi cửa sổ đóng băng của **broadcast là 10 phút**, của **scenario step là 5 phút**, và chỉ ra đây là **2 cơ chế khác nhau** (chặn edit ở tầng web vs đóng băng danh sách ở tầng job) đang bị lẫn. | spec-features SC-003 §7.3 ⇄ kho-tcs FA-008 `MT-17` (`TC-BC-246`, `TC-BC-249`) | **Dev + Leader** — cần tra giá trị thật của hằng số `PREPARE_FILTER_BROADCAST_BEFORE`. Chốt xong mới viết được TC cho cửa sổ đóng băng (TC đề xuất cũ đã bị bỏ). |
| **SPEC-UPD-02** | **Giới hạn số điều kiện AND/OR: 100 hay 5?** kho `MT-12`: tiêu đề khối ghi *"filter and và or ko add quá 100 item"* nhưng TC thực tế đo ở mốc **5 item**. Spec SC-003 §5/§7.2 **không ghi giới hạn nào**. Chênh nhau 20 lần → ảnh hưởng trực tiếp `TC-BULK001-02` và tới rủi ro `tmp_table_size` của chính ticket này. | kho-tcs FA-008 `MT-12` ⇄ spec SC-003 §7.2 | **Dev** — tra giới hạn thật trong code/config, bổ sung vào spec §7.2. |
| **SPEC-UPD-03** | **`conversation.tb_line_user_id` có được đảm bảo luôn có giá trị không?** Bản vá vòng 2 lọc bằng cột này, trong khi chính báo cáo AI ghi *"tb_line_user_id cho phép NULL nên có nguy cơ lọc thiếu bạn bè"*. Spec SC-003 §6 (Filter → DB Mapping) và §5.4 **không mô tả cột này**. | file 03 mục 2 ⇄ file 03 mục 7 (TỰ REVIEW); spec SC-003 §5–§6 bỏ trống | **Dev + DBA** — xác nhận có backfill chưa; bổ sung cột vào spec §5.4 + §6. Đây là tiền đề của `[BLOCKER] FIXSHAPE-01`. |
| **SPEC-UPD-04** | **Nhánh DB replica có nằm trong phạm vi bản vá không?** `BR-14` nói *"logic WHERE giống hệt"*, nhưng file 03 mục 3 nói nhánh replicate *"vẫn dùng mảng PHP"* → hai cách nói không tương thích. | spec SC-003 `BR-14` ⇄ file 03 mục 3 | **Dev** — tiền đề của `[BLOCKER] GAP-02`. |
| **SPEC-UPD-05** | **Mục 4.3 của Dev thiếu ≥ 5 context** so với spec §2 / §7.7 (calendar-*, action_schedule, form, filter_manager, job pre-filter broadcast). | file 03 mục 4.3 ⇄ spec SC-003 §2 + §7.7 | **Dev** — bổ sung mục 4.3 (`[MAJOR] IMPACT-01`). |
| **SPEC-UPD-06** | **kho-tcs chưa có feature riêng cho SC-003.** Chính [fa008-broadcast](../../kho-tcs/fa008-broadcast-メッセージ配信.md) đề xuất *"tách feature riêng『SC-003 絞り込み』— HỎI USER XÁC NHẬN"*. Ticket #40171 là bằng chứng cho thấy component này cần kho riêng: TC của nó đang nằm rải ở FA-008/009/013/024. | kho-tcs FA-008 (dòng 25) | **Leader** — quyết định có chạy `/collect-tcs SC-003 Friend Filter` không. |

---

## 7. Checklist đã chạy

| Mục | Kết quả | Ghi chú |
|---|---|---|
| **A. Coverage** (đối chiếu `03-dev-impact.md`) | ⚠️ **FAIL một phần** | `BUG` + `F1`–`F7` + `T1`–`T8` đều có TC. `F8` = GAP; `T9`–`T13` = GAP do **mục 4.3 của Dev thiếu**. Không impact nào đạt `OK` vì `pass = 0`. |
| **B. Chất lượng từng TC** | ⚠️ **FAIL một phần** | Steps/expected viết tốt, cụ thể, có baseline nhánh gốc. Nhưng: `spec_status` trống 52/52 · `priority` trống 50/52 · loại evidence không khai báo. (Tiền đề gói cước ở 15 TC đã được sửa — xem PRE-01.) |
| **C. Chất lượng bộ TC** | ⚠️ **FAIL một phần** | 52 TC / 13 màn / 11 requirement — bố cục tốt, có đối chứng âm. Nhưng 8/13 mã quan điểm chỉ 1 loại case (AP-3) và 19/46 TC mang mã ngoài checklist. |
| **D. Spec alignment** | ⚠️ **FAIL** | Spec SC-003 tồn tại và đầy đủ, nhưng **6 điểm** cần chốt (§6). `BR-14` không TC nào cover. |
| **E. Hành chính** | ❌ **FAIL** | Checkbox verify chưa tick ở cả 2 file input · toàn bộ TC `status = draft` · `reviewed = false`. |
| **F. Base quan điểm test LME** | ⚠️ **FAIL một phần** | Xem F.1. |

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận từ nội dung) | Exec | Kết luận |
|---|---|---|---|---|---|
| `DATA-COUNT-001` | **Cao** | ✅ BẮT BUỘC — ticket sửa đúng câu `COUNT(*)` | **— không TC nào** | — | **🔴 `[BLOCKER]` GAP-01** |
| `DATA-DB-001` | **Cao** | ✅ — xác minh tầng DB, `WHERE` scope theo `bot_id` | NEW-1 · NEW-6 · (NEW-27 nội dung) | 0/3 | `RISK` + RULE-01 (chỉ Normal) |
| `REG-SHARED-001` | **Cao** | ✅ — sửa hàm dùng chung 8+ caller | NEW-22 · NEW-32 · NEW-33 · NEW-34 · NEW-35 · NEW-45 | 0/6 | `RISK` — thiếu Boundary + thiếu 5 context (IMPACT-01) |
| `COMPAT-LEGACY-001` | **Cao** | ✅ — bản ghi hội thoại đời cũ, cột `tb_line_user_id` có thể trống | NEW-2 · NEW-5 · NEW-8 · NEW-9 · NEW-46 · (NEW-4, NEW-31, NEW-37 nội dung) | 0/8 | `RISK` — **đủ 3 loại case ✅**, nhưng 0 TC chạy |
| `MSG-001` | **Cao** | ✅ — lọc người nhận tin hàng loạt | NEW-28 · NEW-29 | 0/2 | `RISK` + RULE-01 (chỉ Normal) |
| `MSG-004` | **Cao** | ✅ — preview admin ↔ nhận thật trên LINE | NEW-30 | **0/1 (chưa chạy)** | `RISK` + RULE-01 |
| `MSG-USER-001` | **Cao** | ✅ — bạn bè đã chặn | NEW-18 | 0/1 | `RISK` + RULE-01 (chỉ Abnormal) |
| `SEC-ISO-001` | **Cao** | ✅ — cách ly bạn bè giữa các bot | NEW-27 | 0/1 | `RISK` + RULE-01 |
| `BULK-001` | **Cao** | ✅ — chọn tất cả sau lọc rồi thao tác hàng loạt | NEW-19 | 0/1 | `RISK` + RULE-01 (chỉ Boundary) |
| `OUT-TRUTH-001` | **Cao** | ✅ — số hiển thị phải khớp trạng thái thật | NEW-7 · NEW-10 · NEW-17 · NEW-44 | 0/4 | `RISK` + RULE-01 (chỉ Normal) |
| `OUT-EXPORT-001` | Cao (nâng) | ✅ — xuất CSV theo bộ lọc | NEW-21 · (NEW-36, NEW-37, NEW-38 nội dung — mã `JOB-002`/`RULE-12` không tính) | 0/4 | `RISK` + VP-01 + RULE-01 |
| `ENV-003` | **Cao** | ✅ — khác biệt dev/staging/production | NEW-43 | **0/1 (chưa chạy)** | `RISK` + **`[MAJOR]` ENV-01** |
| `PERF-LARGE-001` | Cao (gửi tin/export) | ✅ — chính là mục tiêu ticket | NEW-41 | 0/1 | `RISK` + **`[MAJOR]` PERF-01/02** |
| `PERM-001` | **Cao** | ✅ — chốt gói cước ở đường lọc (phát sinh từ comment #70) | NEW-47 (Normal) · NEW-48 (Abnormal) | 0/2 | `RISK` — thiếu Boundary |
| `STATE-DEP-001` | Trung bình | ✅ — đổi điều kiện lọc của tin đã đặt lịch | NEW-52 | 0/1 | `RISK` |
| `UI-003` | TB → Cao (false success) | ✅ — kết quả rỗng không được báo lỗi | NEW-15 | 0/1 | `RISK` |
| `LIST-001` | Trung bình | ✅ — filter giữ khi sort/chuyển trang, click số mở đúng danh sách | NEW-25 (phân trang) · NEW-17 (click số) | 0/2 | `RISK` — **thiếu chiều "filter giữ khi sort / đổi tab"** |
| `JOB-001` | **Cao** | ⚠️ một phần — job xuất CSV **không** gọi API ngoài; job gửi broadcast **có** | NEW-36/37/38 (CSV) — **không TC nào cho job pre-filter broadcast** | 0/3 | **`[MAJOR]` GAP-03** |
| `CONC-001` | **Cao** | ✅ — nút「再計算」từng có case NG double-click | **— không TC nào** | — | **`[MAJOR]` RULE12-01** |
| `DATA-MIG-001` | **Cao** | ✅ — đổi sang đọc cột `tb_line_user_id` có thể chưa backfill | NEW-1 · NEW-2 · NEW-3 (kiểm kê) | 0/3 | `RISK` — cover về nội dung, nhưng gắn `[BLOCKER] FIXSHAPE-01` |
| `DATA-AUDIT-001` | Cao | ❌ không khớp — fix chỉ `SELECT`, không ghi dữ liệu | — | — | Không áp dụng |
| `DATA-BACKUP-001` | Cao | ❌ không khớp — không thêm bảng/cột | — | — | Không áp dụng |
| `DEPLOY-ASSET-001` | — | ❌ không khớp — không đụng JS/CSS/asset | — | — | Không áp dụng |
| `MEDIA-*` | — | ❌ không khớp | — | — | Không áp dụng |

**Quan điểm THIẾU (trigger khớp nhưng không TC nào cover):**
1. `DATA-COUNT-001` (Cao) → **`[BLOCKER]`**
2. `CONC-001` (Cao) → `[MAJOR]`
3. `JOB-001` nhánh job pre-filter broadcast (Cao) → `[MAJOR]`
4. `BR-14` DB replica (business rule spec, `level = none`) → **`[BLOCKER]`**
5. `LIST-001` chiều "filter được giữ khi sort / đổi tab" → `[MINOR]`

> Theo **RULE-11**, §4 của `checklist-lme.md` ("Quan điểm chưa đủ bằng chứng" — FORM-01, CHAT-01, ADM-01/03/04, TPL-01) **không** được dùng để flag BLOCKER/MAJOR. Không mục nào trong nhóm đó được dùng ở report này.

---

## 8. Ký duyệt

| Vai trò | Tên | Ngày | Kết luận |
|---|---|---|---|
| Reviewer (draft AI) | `/review-tc` | 2026-08-26 | **REJECTED** — 4 BLOCKER |
| Test Leader verify | | | |
| Member nhận feedback | | | |

### Việc phải làm theo thứ tự

1. **Dev trả lời 4 câu** (chặn mọi việc còn lại): ① `tb_line_user_id` có row NULL / đã backfill chưa? ② nhánh DB replica có được sửa cùng không, production có bật không? ③ job pre-filter broadcast có đi qua `advanceFilterPost` không? ④ ngưỡng performance chấp nhận là bao nhiêu?
2. **Cập nhật file 03** — mục 6 + TỰ REVIEW còn mô tả `CAST` trong khi fix cuối là `tb_line_user_id`; bổ sung mục 4.3 thiếu 5 context.
3. **Tester tick 2 checkbox verify** ở file 01 và 03.
4. ~~Sửa tiền điều kiện 15 TC (PRE-01)~~ ✅ **đã xong**. Còn: điền `spec_status` cho 52 TC trên Studio.
5. **Chạy NEW-1 → NEW-3 trước tiên** (kiểm kê dữ liệu). Có bản ghi `tb_line_user_id` trống → **dừng, trả Dev**.
6. **Giải phóng git lock ở runner slot 3, chạy lại toàn bộ run.**
7. Bổ sung **5 TC** ở §5 vào Studio (`/sync-review-tc` — nguồn là Studio nên push thẳng bằng `testcase_create`).
8. Chốt 6 mục §6 với Dev/Leader.

> Report này là **draft cho Leader verify**, không phải kết luận cuối.
