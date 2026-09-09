# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #39121 — Improve performance khi thực hiện filter ở modal filter theo điều kiện QR/landing |
| Reviewer (Leader) | `<Leader ký>` (draft do `/review-tc` sinh) |
| Tester được review | Ngô Thúy Ngần |
| Ngày review | 2026-07-30 |
| Version TCs | fetch từ Sheet "Improve nhỏ " 2026-07-29 (dòng 1196–1260) |
| Vòng review | Round 1 |

> **Spec reference**: KHÔNG có `02-spec-reference.md` riêng → dùng `templates/LME-SYSTEM-SPEC.md` tổng (Friend Filter/Segment SC-003, Friend List FA-013, QR Code/Landing FA-017). Không có spec chi tiết riêng cho task này.
>
> **Nguồn file 04**: TC do QA viết sẵn trên Sheet master, fetch read-only qua `/new-task` (Link TCs Redmine). Sheet dùng **format phân cấp riêng** (Main Function → Sub1..Sub5 → Expect Result), **không phải 16 cột canonical** → nhiều cột canonical (Mã quan điểm liên kết / Loại case / Trạng thái đánh giá spec / evidence) không tồn tại trong nguồn. Review theo nội dung, không nitpick schema cột (xem §4.4).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER + nhiều MAJOR, cần bổ sung TC và review lại.

**Lý do ngắn gọn**: Bộ TC phủ **tính đúng của kết quả filter** rất tốt (2 option × 7 màn × AND/OR × 1/nhiều QR), nhưng đây là ticket **improve performance** mà **không có TC nào đo hiệu năng** (mục tiêu chính của ticket) — không thể nghiệm thu fix. Ngoài ra thiếu các chiều biên/nhánh code mà cách fix vừa động đến (NULL `line_id` cho `NOT IN`, option "すべて含む" dùng `group by having`, nhánh QR web `is_action_web`).

---

## 2. Tóm tắt cho member

Ngần cover coverage **chiều rộng** rất chắc — filter QR/landing được soi qua đủ 7 màn dùng chung (`advanceFilterPost`), cả 2 option include/exclude, cả AND/OR, cả 1 và nhiều QR — đúng tinh thần REG-SHARED-001 (fix ở code dùng chung → test từng nơi gọi). Điểm cần bổ sung là **chiều sâu theo cách fix**: (1) ticket này mục tiêu là *tốc độ* nên **phải có TC đo thời gian trên bot lớn thật + EXPLAIN** (Dev còn chưa đo được — file 03 §5); (2) fix đổi SQL sang `IN`/`NOT IN` nên cần TC **so kết quả trước/sau fix trên cùng bot** + các biên Dev vừa thêm (`line_id is not null`, option "すべて含む", nhánh QR web). Không cần test end-to-end nhận tin trên LINE cho từng màn — fix chỉ ở tầng query lọc, thêm chiều gửi tin là thừa (xem §4.4 AP-5).

---

## 3. Coverage Matrix

> Impact lấy từ `03-dev-impact.md`. TC map suy luận từ Main Function/Sub/Expect của file 04.

| Impact | Loại | Priority (Dev) | TCs cover (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — query lọc QR/landing chậm >300s (root cause: subquery đếm tham chiếu cột ngoài) | Fix (performance) | — | *không có TC đo hiệu năng* | **0** | **GAP** |
| **F1** — `Conversation::advanceFilterPost` (qr_code, AND+OR) | Function | Direct | 1197–1227 (include) · 1228–1258 (exclude) — tính đúng kết quả | ~60 | RISK (thiếu NULL/all-codes/web-action) |
| **F2** — `ConversationReplicate::advanceFilterPost` (AND+OR) | Function | Direct | gián tiếp qua màn dùng replica (friendlist count, cross analysis) — không tách bạch | ~ | RISK (không có TC verify riêng bản replica trên production) |
| **D1** — *(không có data write)* | Data | — | N/A (fix read-only) | — | N/A |
| **T1** — Friend Filter/Segment (SC-003) | Feature | High | 1197–1258 toàn bộ | ~60 | RISK (thiếu biên) |
| **T2** — Friend List (FA-013) | Feature | Medium | 1197–1200, 1228–1231 (màn friendlist) | 8 | OK |
| **T3** — QR Code/Landing (FA-017) | Feature | Medium | 1201–1203, 1232–1234 (màn QR: new/unblock/old) | 6 | OK |
| **T4** — Broadcast/Scenario/Auto reply/Action schedule/Cross analysis | Feature | Medium | 1204–1227, 1235–1258 | ~48 | OK (đúng kết quả); thiếu đo hiệu năng |

### ORPHAN TCs

Không có TC lạc chủ đề — toàn bộ 64 dòng đều thuộc scope filter QR/landing (F1/F2/T1–T4). ✅

> **Lưu ý coverage vs execution**: cột "KQ #39121" (cột I của Sheet) mới đánh `OK` ở màn friendlist→Auto reply của Block 1 (1197–1215) + 1 dòng staff (1260); **Action schedule + Cross analysis của Block 1 và TOÀN BỘ Block 2 (exclude) đang `–`** = chưa chạy. Đây là **tiến độ thực thi**, không phải thiếu TC — nhưng Leader lưu ý bộ exclude (nhánh `NOT IN`, nơi rủi ro nhất) chưa được chạy dòng nào.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** | **Performance / optimize query** (rewrite subquery đếm tham chiếu cột ngoài → subquery độc lập `IN`/`NOT IN` + `group by having` + ép kiểu số). Kèm tính chất **logic-rewrite nhạy cảm đúng/sai** (đổi cách tính tập đối tượng). |
| **Trigger space cần cover** | (a) Hiệu năng: bot lớn nhất thực tế + EXPLAIN + đo thời gian; (b) 2 điều kiện QR filter (theo **live API** `guide_filter_structure`): `scanned_any` (1つ以上含む) + `never_scanned` (1つ以上含む...除く) — **chỉ 2, không có "すべて含む"**; (c) 2 loại QR theo data: `action=2` (kết bạn) + `is_action_web` (thao tác web); (d) biên: `line_id` NULL (NOT IN), list QR rỗng `in ()`, friend old (action=1); (e) môi trường: production + DB replica + loadbalance. |
| **Số trigger TCs hiện cover** | Điều kiện QR: **2/2** ✅ (human phủ đủ `scanned_any` + `never_scanned`). Loại QR data: **1/2** (chỉ `action=2`, thiếu `is_action_web`). Hiệu năng: **0** (không đo). Biên NULL: **0**. Môi trường prod: **0** (không ghi env). |
| **KH report dạng** | **Có root cause cụ thể** — KH đưa thẳng câu SQL + ">300s", Dev xác định đúng nguyên nhân (subquery tương quan). Không phải symptom-only. |
| **Alternative root causes cần verify** | N/A (root cause rõ ràng, xác định ở tầng SQL). |
| **Anti-patterns dính** | **AP-3** (happy-path-only regression — mọi TC ở trạng thái "friend tồn tại", thiếu edge NULL/rỗng/quy mô lớn). AP-1/AP-2/AP-6 **không** dính (không phải generic error-handler; root cause rõ; mục 3 caller list đầy đủ). AP-5 (over-coverage) **có nguy cơ nếu bổ sung sai** — xem §4.4. |

> Trigger space cover < tổng ở nhiều chiều → flag [BLOCKER] (hiệu năng) + [MAJOR] (option/biên/web-action/prod) trong §4.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-1 (PERF-LARGE-001, ENV-003)**: Ticket mục tiêu **improve performance (>300s)** nhưng **không TC nào đo hiệu năng**. Không có TC reproduce câu lọc chậm gốc, không đo thời gian trước/sau, không chạy EXPLAIN, không test ở quy mô bot lớn nhất thực tế. Dev cũng **chưa đo được thời gian thật** (MySQL dev không kết nối được — file 03 §5) và cảnh báo **prod có thể tắt materialization** khiến cải thiện không như kỳ vọng → **bắt buộc đo trên PRODUCTION** (RULE-08). → *Fix*: thêm TC `TC-PERFLARGE001-01/02` (xem §5): đo thời gian + EXPLAIN trên bot lớn nhất, env = PRODUCTION. **Không nghiệm thu fix nếu chưa có bằng chứng thời gian giảm.**

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE / GAP-2 (MSG-001 + DATA-COUNT-001)**: Fix đổi SQL sang `IN`/`NOT IN` — rủi ro lớn nhất là **kết quả lọc lệch → gửi nhầm đối tượng**. TC hiện chỉ mô tả "filter ra friend đã kết bạn qua QR" nhưng **không có TC đếm tay số friend khớp + so kết quả TRƯỚC/SAU fix trên cùng bot**, cũng không đối chiếu số đếm 4 nguồn (friendlist / cross analysis / CSV / API). Dev đề nghị đúng việc này ("QA/DBA so số bạn bè trước/sau"). → *Fix*: `TC-MSG001-01` (§5).
- **[MAJOR] FIX-SHAPE / GAP-3 (FUNC-004 boundary — nhánh `NOT IN`)**: Dev thêm điều kiện `line_id is not null` để `NOT IN` không bị NULL nuốt kết quả. **Không TC nào test friend có `detail_landing_click.line_id` NULL với option exclude.** Đây là nhánh dễ sai nhất (NOT IN + NULL → có thể loại nhầm toàn bộ). Thêm nữa **toàn bộ Block 2 (exclude) đang chưa chạy dòng nào** (col I `–`). → *Fix*: `TC-FUNC004-01` (§5) + yêu cầu chạy hết Block 2.
- **[MAJOR] FIX-SHAPE / GAP-4 (MSG-001 — QR web `is_action_web`)**: Dev sửa cho **cả** QR đăng ký bạn (`action=2`) **lẫn** QR thao tác trên web (`is_action_web`). Mọi TC chỉ nhắc `detail_landing_click.action = 2` (loại kết bạn). **Landing loại thao tác web (`is_action_web`) chưa có TC.** Đây là data-variant (loại landing), không phải option filter. → *Fix*: `TC-MSG001-02` (§5). *(Cần xác nhận với Dev: filter có phân biệt được landing web-action không, hay chỉ lọc theo QR ID bất kể loại.)*
- **[MAJOR] ENV-003 / GAP-5 (F2 — bản replica trên production)**: Fix áp cho cả `ConversationReplicate` (đọc DB replica). TC không ghi môi trường và không có case verify riêng trên **production** (replica + 2 server loadbalance). Materialization + replica lag có thể cho kết quả/tốc độ khác staging. → *Fix*: `TC-ENV003-01` (§5).
- **[MAJOR] Verify auto-fill chưa tick (01 + 03)**: Cả `01-bug-task.md` và `03-dev-impact.md` đều `Auto-filled: 2026-07-29 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick**. Review chỉ có giá trị sau khi tester đọc lại Redmine (description + journal đánh giá ảnh hưởng) và xác nhận F/D/T + môi trường (đặc biệt: môi trường phát hiện đang là **suy luận "Production"**, và "Steps to reproduce" là suy luận vì Redmine không có section tái hiện). → *Fix*: Ngần đọc lại Redmine #39121, tick 2 checkbox.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Format sheet không canonical**: File 04 (nguồn Sheet human) thiếu các cột canonical `Mã quan điểm liên kết`, `Loại case`, `Trạng thái đánh giá spec`, cột evidence bắt buộc (RULE-02). Đây là **đặc thù Sheet master phân cấp**, không phải lỗi member — không yêu cầu convert. Chỉ lưu ý: TC bổ sung ở §5 dùng đúng 16 cột canonical, khi `/sync-review-tc` sẽ ghi 5 cột về Sheet.
- **[MINOR] Không có phép tính tay/số cụ thể trong Expect**: Các Expect dạng "filter ra friend đã kết bạn qua QR" chưa có **số đối tượng cụ thể/đếm tay** → 2 người chạy có thể ra 2 cách hiểu về "đúng". Nên chốt bộ seed data biết trước kết quả (đã đưa vào TC §5).

### 4.4 Nit (gợi ý)

- **[CONFIRM với Dev] Option "すべて含む" (group by having) — KHÔNG flag GAP**: File 03 §2 (báo cáo Auto-fixbug) ghi fix xử lý **"Bốn lựa chọn"**, gồm nhánh "đã quét đủ tất cả mã" dùng `group by line_id having count(distinct landing_id) = số mã`. **NHƯNG** live filter API (`guide_filter_structure` type `qr_code`) chỉ expose **2 điều kiện**: `scanned_any` + `never_scanned` — trùng khớp **đúng 2 option** human đã test. → Không đủ bằng chứng để flag GAP; 2 option human test **nhiều khả năng đã đủ**. Hỏi Dev: nhánh `group by having` có phải option user-facing (surface nào?) hay chỉ là logic nội bộ/dead code. *(Đây là chỗ round 1 tôi suýt flag nhầm GAP + bịa label `すべて含む` — đã rút.)*
- **[NIT] AP-5 — tránh over-coverage tầng gửi tin**: Fix chỉ ở `advanceFilterPost` (tầng query lọc). **Không cần** thêm TC nhận tin thật trên LINE app cho từng màn Broadcast/scenario/auto reply — logic gửi không bị chạm, thêm vào là thừa (tham chiếu memory `feedback_root_cause_layer_focus`). Trọng tâm test đúng ở **kết quả tập lọc + hiệu năng**.
- **[NIT] List QR rỗng `in ()`**: Dev giữ nguyên hành vi lỗi cú pháp cũ khi list mã rỗng (ngoài phạm vi ticket). Có thể thêm 1 case Boundary xác nhận "không regress thêm", nhưng không bắt buộc.
- **[NIT] Ép kiểu số chống SQL injection**: Dev ép integer cho list landing_id. Rủi ro thấp (id nội bộ) — có thể thêm 1 case SEC nhẹ nếu rảnh, không bắt buộc.
- **[NIT] PR link**: File 03 có commit `4c10d81570` + branch `ai_small_39121` nhưng không có URL PR. Fix shape vẫn trace được qua commit → không cần thiết, nhưng nếu cần verify code path chính xác (`if is_action_web` vs generic) thì checkout branch để xác nhận.

---

## 5. TCs đề xuất bổ sung

> Copy vào `04-tc-list.md` round sau. 16 cột canonical. TC No. không trùng file 04.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERFLARGE001-01 | PERF-LARGE-001 | Normal | `advanceFilterPost`: đo thời gian filter QR (1つ以上含む) trên bot lớn nhất thực tế + EXPLAIN | - Bot có số friend lớn nhất thực tế (hỏi PM/DBA, vd ≥ vài trăm nghìn friend)<br>- 1 landing có **nhiều lượt click** trong `detail_landing_click`<br>- Có baseline thời gian trước fix (>300s) | 1. Mở modal filter tại màn friendlist<br>2. Thêm điều kiện QR option `1つ以上含む` với landing nhiều click<br>3. Áp filter, đo thời gian phản hồi (Network tab + log query)<br>4. Chạy `EXPLAIN` câu SQL sinh ra<br>5. So với baseline trước fix | Bot lớn nhất; landing_id nhiều click; đo `t_before` vs `t_after` | - Thời gian < ngưỡng chấp nhận (chốt với Leader, vd < 10s)<br>- EXPLAIN: subquery được **materialize** (không phải DEPENDENT SUBQUERY chạy lại mỗi dòng)<br>- Kết quả tập friend không đổi so với trước | Chưa test | | PRODUCTION | | | | Spec không ghi (ngưỡng thời gian — **đã hỏi Leader**) | Lấp **GAP-1 / BUG performance** + RULE-08/ENV-003. Evidence bắt buộc: log thời gian + ảnh EXPLAIN trên prod |
| TC-PERFLARGE001-02 | PERF-LARGE-001 | Boundary | `advanceFilterPost`: filter nhiều QR + OR trên bot lớn (worst case) | - Như TC-PERFLARGE001-01<br>- Chọn **3+ landing** nhiều click | 1. Modal filter, option `1つ以上含む` filter OR, chọn 3 landing<br>2. Áp filter, đo thời gian + EXPLAIN | 3 landing nhiều click, filter OR | - Thời gian vẫn < ngưỡng chấp nhận ở tổ hợp nhiều QR<br>- Không timeout | Chưa test | | PRODUCTION | | | | Đã hỏi leader | Lấp GAP-1 (biên tải). Evidence: log thời gian |
| TC-MSG001-01 | MSG-001 | Normal | Kết quả filter QR khớp phép tính tay + so trước/sau fix (đếm 4 nguồn) | - Bot seed **biết trước**: 5 friend qua landing A (3 new + 2 unblock), 3 friend qua landing B, 1 friend old scan A (action=1) | 1. Đếm tay số friend khớp `1つ以上含む landing A` = 5<br>2. Áp filter friendlist → so số + danh sách<br>3. Đối chiếu count ở: friendlist / cross analysis / CSV export / API<br>4. So danh sách với kết quả câu query CŨ trên cùng data | landing A/B; phép tính tay: 5 friend khớp A | - Số & danh sách khớp **100%** phép tính tay (=5, không tính friend old)<br>- 4 nguồn (friendlist/cross/CSV/API) khớp nhau<br>- Tập friend **giống hệt** kết quả trước fix | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **GAP-2** (MSG-001 + DATA-COUNT-001). Evidence: bảng đối chiếu 4 nguồn + phép tính tay |
| TC-FUNC004-01 | FUNC-004 | Boundary | Exclude filter (`NOT IN`) với friend có `line_id` NULL không bị nuốt kết quả | - Seed 1 friend có bản ghi `detail_landing_click.line_id = NULL` (click ẩn danh/chưa map line_id)<br>- 1 landing A có vài friend hợp lệ | 1. Áp filter option `1つ以上含む...を除く` (exclude) landing A<br>2. Kiểm friend NULL line_id có bị xử lý đúng không<br>3. Kiểm tập trả về KHÔNG rỗng bất thường (NOT IN không nuốt hết) | friend line_id NULL; option exclude | - `NOT IN` trả đúng tập (Dev đã thêm `line_id is not null`)<br>- Không loại nhầm toàn bộ friend hợp lệ<br>- Friend NULL line_id xử lý theo spec (không kết bạn qua landing) | Chưa test | | STAGING | | | | Spec không ghi (hành vi NULL — **đã hỏi Dev**) | Lấp **GAP-3**. Verify trực tiếp điều kiện `line_id is not null` Dev thêm |
| TC-MSG001-02 | MSG-001 | Normal | Filter QR loại thao tác web (`is_action_web`) thay vì action=2 | - Landing có lượt thao tác web (`is_action_web`), không phải kết bạn | 1. Áp filter QR với landing loại thao tác web<br>2. So danh sách với data `detail_landing_click.is_action_web` | landing is_action_web | - Filter ra đúng friend theo lượt thao tác web<br>- Không lẫn với nhánh `action=2` | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **GAP-4** — nhánh `is_action_web` Dev sửa nhưng chưa có TC. Xác nhận với Dev filter có phân biệt được loại landing web-action |
| TC-ENV003-01 | ENV-003 | Normal | Kết quả filter QR trên PRODUCTION (bản replica `ConversationReplicate` + loadbalance) khớp staging | - Bot thật trên production; có ≥2 router loadbalance | 1. Áp cùng bộ filter QR trên production<br>2. So kết quả với staging (cùng logic)<br>3. Lặp qua từng router (lưu router id) | filter QR trên prod, 2 router | - Kết quả tập friend nhất quán giữa replica (prod) và master, và giữa 2 router<br>- Không lệch do replica lag/materialization | Chưa test | | PRODUCTION | | | | Đã hỏi leader | Lấp **GAP-5 / F2**. Evidence: kết quả trên prod theo từng router |

> **RULE-01**: PERF-LARGE-001 (Cao) đề xuất Normal + Boundary; **thiếu Abnormal** vì quan điểm hiệu năng không có "abnormal" tự nhiên — nếu muốn có thể thêm case "prod tắt materialization" nhưng phụ thuộc cấu hình DBA (ghi lý do ở đây theo RULE-01). MSG-001 (Cao): Normal = TC-MSG001-01/02; Boundary = TC-FUNC004-01 (NULL line_id); **Abnormal** = cụm exclude/`never_scanned` đã có sẵn ở Block 2 human (dòng 1228–1258) — nên chạy hết Block 2 để đủ chiều Abnormal.

---

## 6. Spec update needed

- [x] Không cần update spec — fix giữ nguyên ngữ nghĩa 4 option filter, không đổi behavior end-user (chỉ đổi cách dựng SQL). 
- [ ] ~~Cần update spec~~
- ⚠️ **Cần Leader chốt 1 con số**: ngưỡng thời gian chấp nhận cho filter trên bot lớn (spec không ghi) → dùng làm Kết quả mong đợi của TC-PERFLARGE001-01/02.

---

## 7. Checklist đã chạy

- [x] A. Coverage — matrix §3; BUG=GAP (perf), F1/F2/T1=RISK, T2/T3/T4=OK
- [x] B. Chất lượng từng TC — Expect chưa đo lường được số cụ thể (§4.3 MINOR)
- [x] C. Chất lượng bộ TC tổng thể — chiều rộng tốt, thiếu chiều sâu biên/hiệu năng
- [x] D. Spec alignment — không mâu thuẫn spec (giữ nguyên ngữ nghĩa filter)
- [x] E. Hành chính — format sheet phân cấp (không canonical), verify auto-fill chưa tick (§4.2)
- [x] F. Base quan điểm test LME
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — C (filter/QR/friend/21 đường gửi tin/plan) · D/D2 (production, job, replica, loadbalance)
  - [x] F.3 RULE — RULE-01 (§5) · RULE-06 (không áp — fix ở tầng query, không output cuối chuỗi mới) · RULE-07 (× — read-only, không CRUD) · RULE-08 (**vi phạm** — thiếu prod, §4.1) · RULE-09 (× — không version-up)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| **PERF-LARGE-001** | Cao | ◯ (ticket improve performance, `大量` lượt click, bot lớn) | Không có | **GAP → [BLOCKER]** |
| **MSG-001** (filter đúng đối tượng) | Cao | ◯ (filter điều kiện QR → chọn đối tượng gửi) | 1197–1258 phủ **đủ 2/2 điều kiện QR** (`scanned_any` + `never_scanned` — khớp live API) | **RISK** (thiếu đếm tay/before-after + biên NULL + loại QR web) → [MAJOR]. *Không* thiếu "すべて含む" (option không tồn tại ở live filter — xem §4.4) |
| **ENV-003** (dev/staging/prod) | Cao | ◯ (perf phụ thuộc materialization prod + replica + loadbalance) | Không (TC không ghi env prod) | **GAP → [MAJOR]** (RULE-08) |
| **DATA-COUNT-001** (số đếm) | Cao | ◯ (friendlist count + cross analysis count phản ánh tập lọc) | gián tiếp (không đối chiếu 4 nguồn + phép tính tay) | **RISK → [MAJOR]** |
| **FUNC-004** (giới hạn/biên 5 pattern) | Cao | ◯ (NULL line_id, list QR rỗng, đủ/không đủ mã) | Không (không test biên) | **GAP → [MAJOR]** |
| **BULK-001** (phạm vi thao tác sau lọc) | Cao | ◯ (filter + gửi tin/tag hàng loạt dùng chung) | gián tiếp (verify tập lọc, không đếm số bị tác động 100%) | RISK → [MAJOR] (gộp vào GAP-2) |
| **REG-SHARED-001** (shared code) | Cao | ◯ (`advanceFilterPost` dùng chung 7 màn; Dev có list caller mục 3) | 7 màn đều có TC | **OK** ✅ (điểm mạnh) |
| **PERM-003** (cách ly đa tài khoản) | Cao | ◯ nhẹ (filter phải scope theo bot/landing) | Block 3 "Check account staff" (cover 1 phần) | RISK → nêu ở NIT (read-only, landing per-bot → rủi ro thấp) |
| **DATA-DB-001** (WHERE scope UPDATE/DELETE) | Cao | ✕ | — | ✕ — fix **read-only**, không UPDATE/DELETE (RULE-03: lý do rõ) |
| **DATA-AUDIT-001 / DATA-BACKUP-001 / STATE-CLEAN-001 / PAY-*** | Cao | ✕ | — | ✕ — không chạm data write / hủy HĐ / tiền / job dọn dẹp |
| **COMPAT-LEGACY-001 / RULE-09** | Cao | ✕ | — | ✕ — không version-up cấu trúc data/link |
| **JOB-001** | Cao | ✕ | — | ✕ — fix ở tầng query đồng bộ, không thêm/sửa job nền (Broadcast job dùng kết quả nhưng logic job không đổi) |
| **MSG-004** (preview khớp LINE thật) | Cao | ✕ | — | ✕ — không đổi nội dung/gửi tin (RULE-06 không kích hoạt), tránh over-coverage AP-5 |

> **KHÔNG** dùng §4 checklist-lme (FORM-01/CHAT-01/ADM-*/TPL-01) để flag — RULE-11 (không áp dụng task này).

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<chờ Leader verify draft>` | |
| Tester | Ngô Thúy Ngần (đã đọc & hiểu feedback) | |

---

### Tóm tắt hành động cho Ngần (round 2)
1. **Tick verify auto-fill** ở `01` + `03` sau khi đọc lại Redmine #39121.
2. **Thêm TC hiệu năng** (`TC-PERFLARGE001-01/02`) đo thời gian + EXPLAIN trên bot lớn nhất, **env PRODUCTION** — đây là điều kiện nghiệm thu ticket. Chốt ngưỡng thời gian với Leader.
3. **Thêm TC so kết quả trước/sau fix + đếm tay 4 nguồn** (`TC-MSG001-01`).
4. **Thêm biên `NOT IN` + NULL line_id** (`TC-FUNC004-01`) và **chạy hết Block 2 (exclude)** — hiện `–` toàn bộ.
5. **Bổ sung TC QR web `is_action_web`** (`TC-MSG001-02`). *(Đã rút TC option "すべて含む" — live filter chỉ có 2 điều kiện QR, human đã phủ đủ; chỉ cần hỏi Dev về nhánh `group by having` — §4.4.)*
6. **Verify trên production** replica + loadbalance (`TC-ENV003-01`).
7. **Không** thêm TC nhận tin end-to-end trên LINE cho từng màn — thừa (fix ở tầng query lọc).
