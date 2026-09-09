# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39736 — Ngày thanh toán tiền theo trên modal coupon đang lệch 1 ngày so với ngày` |
| Reviewer (Leader) | `<Leader ký>` — draft sinh bởi `/review-tc` |
| Tester được review | **AI** (LME TEST STUDIO job #458 / task #169) — **0 TC do member người viết** |
| Ngày review | `2026-08-19` |
| Version TCs | `v1` (Studio round 1, toàn bộ TC `version = 1`, `status = draft`) |
| Vòng review | `Round 1` |

> **Input đã dùng**: `01-bug-task.md` · `03-dev-impact.md` · `04-tc-list.md` (17 TC).
> **Input thiếu**: `02-spec-reference.md` **không có** → Spec reference: dùng [LME-SYSTEM-SPEC](../../templates/LME-SYSTEM-SPEC.md) tổng (§3.12 FA-031) + sub-repo [spec-features/admin/billing-plan/](../../spec-features/admin/billing-plan/). Không có spec riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC bám rất sát root cause và biên ngày tháng (4 nhánh của công thức gia hạn đều có TC), nhưng **3 BLOCKER** chặn approve: (1) **5/17 TC ở trạng thái `blocked` chưa chạy** mà task Studio vẫn báo `aiResult = pass` — toàn bộ tầng API chưa verify, không ai raise ticket; (2) **0/17 TC chạy trên PRODUCTION** trong khi task chạm **bill tiền + version asset JS** — vi phạm RULE-08 / `ENV-003`; (3) **GAP `DEPLOY-LIVE-001`** — fix **đổi payload API response** nhưng không TC nào test kịch bản client cũ (chưa reload) gọi server mới.

---

## 2. Tóm tắt cho member

Bộ TC này mạnh ở phần **biên thời gian** — 4 nhánh của công thức `nextExpiredDate` (cuối tháng / qua năm / tháng thiếu ngày + năm nhuận / hợp đồng quá hạn > 7 ngày) đều có TC riêng, và TC NEW-2 verify đủ **3 tầng DB + màn hình + thông báo** (RULE-07) thay vì chỉ nhìn UI — đúng chỗ dễ vỡ nhất của một bản fix cộng ngày. Phần cảnh báo trong `note` cũng rất tốt: NEW-3 và NEW-16 chủ động nói trước cho người chạy biết chỗ nào **lệch 1 ngày nhưng KHÔNG phải bug**, tránh raise ticket nhầm.

Điểm phải fix trước vòng 2: **5 TC nhóm API đang `blocked` mà không có lý do và không ai raise ticket** — con số `12 Đạt / 0 Không đạt` đang che mất việc gần 1/3 bộ TC chưa chạy; và **toàn bộ chạy trên staging** trong khi ticket chạm tiền + chạm file JS phải có bằng chứng trên production (RULE-08). Ngoài ra oracle "+1 ngày" hiện đang **tự tham chiếu chính công thức UI cũ** — cần 1 TC đối chiếu với **ngày trừ tiền thật** để chốt con số, vì spec `billing-plan` đang ghi ngược lại (xem §6).

---

## 3. Coverage Matrix

> Map **quan điểm** đọc thẳng ở cột `Mã quan điểm liên kết`; map **impact BUG/F/D/T** suy luận từ Tiêu đề / Điều kiện tiền đề / Các bước / Kết quả mong đợi.
> Ký hiệu: TC ghi theo `temp_id` Studio (NEW-n) cho gọn; đối chiếu `TC No.` ở file 04. `⛔` = TC đó đang `blocked`, chưa chạy.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — modal coupon hiển thị hạn hợp đồng thay vì mốc thanh toán kế | Fix | — | NEW-1 (reproduce đúng steps KH), NEW-2, NEW-3 | 3 | **OK** |
| **F1** — API `checkCouponCode` (thêm field ngày thanh toán kế) | Function | Direct | NEW-1 (gián tiếp qua UI), ⛔NEW-10, ⛔NEW-12, ⛔NEW-13, ⛔NEW-14 | 5 (**1 chạy được**) | **RISK** — 4/5 TC blocked, chỉ còn verify gián tiếp qua UI |
| **F2** — API `applyCouponCode` (thêm field ngày thanh toán kế) | Function | Direct | NEW-2 (gián tiếp qua UI + DB), ⛔NEW-11, ⛔NEW-12, ⛔NEW-13 | 4 (**1 chạy được**) | **RISK** — hợp đồng response ở tầng API chưa verify |
| **F3** — JS `checkCouponCode` / `confirmCouponCode` / `openModalInputCoupon` | Function | Direct | NEW-1, NEW-2, NEW-3, NEW-4, NEW-15, NEW-17 | 6 | **OK** |
| **F4** — Modal coupon bước xác nhận + thành công (`detail.blade.php`) | Function | Direct | NEW-1, NEW-2, NEW-4, NEW-5 | 4 | **OK** |
| **F5** — `BillingService::nextExpiredDate` (**không sửa code**) | Function | Indirect | NEW-6, NEW-7, NEW-8, NEW-9, ⛔NEW-14 | 5 | **OK** — 4/4 nhánh công thức có TC (nhánh NULL `date_add_contract` blocked) |
| **F6** — JS `expiredDateContract` — dòng 次回決済日 trên màn (**không sửa code**) | Function | Indirect | NEW-3, NEW-7, NEW-15 | 3 | **OK** — dùng làm mốc đối chứng 2 đường tính độc lập |
| **D1** — `bot_contracts.expired_date_contract` | Data | UPDATE (không đổi so trước fix) | NEW-2, NEW-16, ⛔NEW-11 | 3 (**2 chạy được**) | **RISK** — thiếu TC kiểm `WHERE` scope trên 2 tài khoản (`DATA-DB-001`) |
| **D2** — `bots.expired_date` | Data | UPDATE (không đổi so trước fix) | NEW-2, ⛔NEW-11 | 2 (**1 chạy được**) | **RISK** — chỉ 1 TC chạy được, không có boundary/negative riêng |
| **T1** — Contract Plan & Payment (FA-031) — màn chi tiết hợp đồng | Feature | `<Dev không chấm>` | NEW-15 (regression), NEW-16 (操作履歴), NEW-3, NEW-17 | 4 | **RISK** — chỉ regression trên hợp đồng "sạch"; không có TC ở trạng thái hợp đồng edge (延滞中 / chờ chuyển khoản / free plan) — xem AP-3 |
| **T2** — Coupon Code Issue (FS-015) — luồng áp dụng mã coupon | Feature | `<Dev không chấm>` | NEW-1, NEW-2, NEW-3, NEW-4, NEW-5, NEW-6, NEW-7, NEW-8, NEW-9 | 9 | **OK** |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | **Không phát hiện ORPHAN** — cả 17 TC đều map được về BUG / F* / D* / T*. | Giữ nguyên |

> Đã cân nhắc **AP-5** (over-coverage layer downstream) với NEW-6/7/8/9 — 4 TC exercise sâu `BillingService::nextExpiredDate` là hàm **không bị sửa**. **Kết luận: KHÔNG phải AP-5** — bản fix cộng `+1 ngày` lên chính output của hàm đó, nên hành vi biên của `output + 1` là **hành vi mới**, phải test. Giữ cả 4 TC.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Khác — "Display-only field addition"**: thêm field `new_next_payment_date` vào response 2 API + đổi biến hiển thị `couponNewExpiredDate` → `couponNextPaymentDate` ở 2 modal. **Không** đổi logic tính ngày, **không** đổi dữ liệu ghi DB. Khớp thêm **4 shape phụ** trong bảng Bước 3c: `sửa hàm dùng chung` (detail.js là JS của TOÀN màn chi tiết) · `JS/asset/build` · `đổi trạng thái hợp đồng` (audit log) · `đổi payload API` (→ DEPLOY-LIVE-001). |
| **Trigger space cần cover** | 3 nhánh của công thức `BillingService::nextExpiredDate`: (a) ngày neo là ngày thường · (b) ngày neo là ngày cuối tháng / tháng đích thiếu ngày · (c) hợp đồng quá hạn > 7 ngày (mốc đặt lại theo hiện tại) — **×** 2 bước modal (xác nhận / thành công) **×** 2 endpoint (check / apply). Cộng biên lịch: cuối tháng → đầu tháng · 31/12 → 01/01 · 29/2 năm nhuận · `date_add_contract` NULL · **timezone JST vs local**. |
| **Số trigger TCs hiện cover** | **4/5 nhánh dữ liệu** — (a) NEW-1/2 · (b) NEW-6/7/8 · (c) NEW-9 · NULL `date_add_contract` = ⛔NEW-14 (**blocked**). **Timezone: 0/1 — GAP** (xem §4.2). 2 bước modal: đủ (NEW-1 + NEW-2). 2 endpoint ở tầng API: **0/2 chạy được** (⛔NEW-10, ⛔NEW-11). |
| **KH report dạng** | **Có root cause cụ thể** — KH nêu chính xác 2 con số (hiện `2026/09/26`, kỳ vọng `2026/09/27`), nêu rõ mốc đối chiếu (`次回決済日 = 2026/08/27`) và **tự kết luận yêu cầu**: 「export ngày trên modal coupon phải = ngày thanh toán tiền theo」. → **AP-2 KHÔNG dính**, không cần cover alternative root cause. |
| **Alternative root causes cần verify** | `N/A` — KH đã chỉ đúng chỗ, Dev tái hiện được bằng Carbon và ra đúng con số KH báo (mục 6 VERIFY của file 03). |
| **Anti-patterns dính** | **AP-3** (happy-path-only regression) · **AP-4 một phần** (không có link PR/diff để verify fix shape thực tế, chỉ có commit hash). **AP-1 không dính** (fix không phải generic catch) · **AP-2 không dính** · **AP-5 không dính** (xem §3) · **AP-6 không dính** (mục 3 dev-impact có 6 dòng caller). |

### Câu hỏi adversarial theo từng shape phụ — đã trả lời

| Shape phụ | Câu hỏi bắt buộc | Trả lời từ input hiện có | Kết luận |
|---|---|---|---|
| `sửa hàm dùng chung` (REG-SHARED-001) | Có danh sách nơi ảnh hưởng do **DEV cung cấp** không? TC test từng nơi? Chức năng tương tự đã rà chưa? | **Có** — mục 3 file 03 liệt kê 6 mục (2 API + 3 JS func + 1 view + 2 hàm chỉ đọc). NEW-15 test lại toàn màn chi tiết + console JS. **Nhưng** chưa rà chiều **brand** (Lme / Lwaka / Saruwaka / Lgram) mà `REG-SHARED-001` yêu cầu. | **RISK** → [MINOR] §4.3 |
| `JS / asset / build` (DEPLOY-ASSET-001) | Có test **F5 thường** trên browser còn cache bản cũ? Network tab có 404? | **Có** — NEW-17 làm đúng: F5 thường, đọc query version, kiểm nội dung file JS. **Nhưng chỉ chạy STAGING**; Dev tự khai commit「version up」**nằm ngoài ticket này**. | **GAP env** → [BLOCKER] §4.1 |
| `đổi payload API` (DEPLOY-LIVE-001) | Có test **client cũ (KHÔNG reload) gọi server mới** sau release? | **KHÔNG có TC nào.** NEW-17 có reload (F5) → không phủ được kịch bản này. Dev giữ lại field cũ `new_expired_date` **chính vì** kịch bản này, nhưng không ai test. | **GAP** → [BLOCKER] §4.1 |
| `đổi trạng thái hợp đồng` (DATA-AUDIT-001) | Có TC verify 操作履歴 ghi đủ 4 thông tin, **từ TỪNG nguồn**? | NEW-16 verify bản ghi 操作履歴 mới + dòng 「クーポン適用後の次回決済日」. Nguồn: chỉ **web** — hợp lý vì coupon **chỉ** áp dụng được từ web (không có app / action job / multi action). | **OK** (× các nguồn khác có lý do) |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] GAP-1 — RULE-08 / `ENV-003`: 0/17 TC chạy trên PRODUCTION.** Toàn bộ 17 TC có `Môi trường test = STAGING` (`last_exec.env = staging`), `envAuto` cho thấy 2 lượt tự động ở `local` + 1 lượt manual ở `staging`, **`prd` = 0 lượt**. Task chạm **bill tiền** (`bot_contracts.expired_date_contract`, `bots.expired_date` — hợp đồng thật) **và version asset JS** — cả hai đều nằm trong danh sách RULE-08 **không được kết luận từ staging**. `env_scope` do AI đặt cho 14/17 TC còn **chủ động loại trừ `prd`**. — **Fix**: bổ sung `TC-ENV003-01` (§5) chạy smoke trên PRODUCTION **ngay sau deploy**, tối thiểu phủ NEW-1 + NEW-17; ghi `Môi trường test = PRODUCTION`. Nếu không thể chạy trên hợp đồng thật → phải có **phiếu xác nhận không thể verify + phương án giám sát** (theo Evidence của `ENV-003`), không được bỏ trống.

- **[BLOCKER] GAP-2 — 5/17 TC ở trạng thái `blocked`, chưa chạy, chưa raise ticket, không có lý do.** ⛔NEW-10, ⛔NEW-11, ⛔NEW-12, ⛔NEW-13, ⛔NEW-14 (toàn bộ nhóm `tc_group = api`) có `last_exec.status = blocked`, `bug_tickets` **rỗng**, `blockedReason = null`. Studio quy `blocked` vào `other` nên task vẫn hiện **`aiResult = pass` / `openBugs = 0`** — Leader đọc lướt sẽ tưởng đã test xong, trong khi **29% bộ TC chưa chạy**. Hậu quả coverage: **REQ-004** (risk High) và **REQ-006** *hoàn toàn* chưa verify; **REQ-005** (risk High) chỉ còn verify gián tiếp qua NEW-2; **REQ-007** chỉ verify ở tầng UI (NEW-5) — mất case "hợp đồng không tồn tại" mà chỉ NEW-13 có. Khớp đúng định nghĩa BLOCKER trong [severity-levels.md](../../framework/severity-levels.md): *"TC phụ thuộc data/env không tồn tại trên môi trường test → không chạy được"*. — **Fix**: bắt buộc ghi **lý do blocked** vào Studio (`blockedReason`), rồi chạy lại đủ 5 TC. Nếu blocked vì không lấy được CSRF token / không gọi được endpoint từ staging → hạ về chạy ở `dev`/`local` và ghi rõ env, **không được để `Chưa test` rồi đóng ticket**.

- **[BLOCKER] GAP-3 — `DEPLOY-LIVE-001` (Cao) trigger khớp nhưng KHÔNG có TC nào cover.** Trigger của `DEPLOY-LIVE-001` là *"release lên production không bật maintain, **đặc biệt khi đổi payload API / field form / cấu trúc request**"* — bản fix này **chính là** đổi payload response của 2 API. Kịch bản chưa ai test: user đang mở sẵn màn chi tiết hợp đồng **trước** khi release → release xong → **không reload**, bấm 「クーポンコードを入力する」→「次へ」. JS cũ trong trang đọc `new_expired_date`; Dev **cố ý giữ lại field này** để không phá bên gọi cũ — nhưng **không có bằng chứng nào** chứng minh nhánh đó còn chạy đúng. NEW-17 **không phủ** được vì bước 1 của nó đã F5. — **Fix**: bổ sung `TC-DEPLOYLIVE001-01` (§5). *(Ghi chú cho Leader: theo quy tắc F.1, quan điểm ưu tiên **Cao** + trigger khớp + 0 TC → BLOCKER. Nếu Leader đánh giá hậu quả chỉ là hiển thị sai tạm thời tới lần reload kế tiếp thì có thể hạ xuống MAJOR — cần Leader quyết, `/review-tc` không tự hạ.)*

### 4.2 Major (nên fix)

- **[MAJOR] INPUT — `01-bug-task.md` auto-filled từ Redmine nhưng chưa được tester verify.** Field `Auto-filled = 2026-08-19 by /new-task`, checkbox **"Tester verify auto-fill chính xác" CHƯA tick**. Yêu cầu tester đọc lại detail Redmine #39736 (gồm cả 2 journal) và tick checkbox — trước khi tick, kết luận review này chỉ có giá trị tham khảo.

- **[MAJOR] INPUT — `03-dev-impact.md` auto-filled từ Redmine nhưng chưa được tester verify.** Checkbox **CHƯA tick**. Rủi ro cụ thể ở task này: (a) mục **4.1 của báo cáo AI chỉ liệt kê 3 FILE**, không liệt kê function theo format F1/F2 → bảng F1–F6 là do `/new-task` **suy luận** từ mục 3, có thể sót; (b) Dev **không chấm mức nguy cơ regression** ở 4.3 → coverage matrix không có Priority để xếp hạng; (c) báo cáo do **AI sinh**, danh sách caller ở mục 3 chưa có người xác nhận. Yêu cầu tester đọc lại Redmine + tick checkbox.

- **[MAJOR] ORACLE — quan điểm `PAY-STATE-001`: oracle "+1 ngày" đang TỰ THAM CHIẾU, không TC nào đối chiếu với ngày trừ tiền THẬT.** Cả 17 TC dùng chung một oracle: *"ngày trên modal = hạn hợp đồng sau khi áp dụng + 1 ngày"*. Nguồn của oracle này là **chính công thức UI cũ** `detail.js expiredDateContract() = moment(expired_date_contract).add(1,'day')` (mục 6 VERIFY file 03). Nghĩa là: **17/17 TC sẽ Đạt bất kể +1 có đúng hay không**, miễn là code làm đúng +1. Không TC nào đi tới **output cuối chuỗi** (RULE-06) = **ngày hệ thống thực sự trừ tiền**. `PAY-STATE-001` yêu cầu đối chiếu **3 nơi**: admin nội bộ / màn user / dashboard cổng thanh toán — hiện chỉ có nơi thứ nhất. Rủi ro thật: [spec-features/admin/billing-plan/feature-spec.md](../../spec-features/admin/billing-plan/feature-spec.md) đang ghi 次回決済日 = `bot_contracts.expired_date_contract` **thô** (dòng 101 cho SCR-BLP-01 và dòng 183 cho SCR-BLP-02) — **ngược với** oracle +1 ngày (xem §6). — **Fix**: bổ sung `TC-PAYSTATE001-01` (§5) — TC **read-only**, đối chiếu bản ghi 決済 đã có trong 操作履歴/lịch sử thanh toán với `expired_date_contract` ngay trước lần thanh toán đó, không cần chạy job. *(Cố ý KHÔNG đề xuất TC chạy `AutoPaymentJobUnivapay` — job không bị chạm code, chạy nó sẽ là over-coverage.)*

- **[MAJOR] GAP-4 — `FUNC-DATE-001` (Cao): thiếu TC timezone, trong khi bug này có ĐÚNG 2 đường tính ngày ở 2 múi giờ khác nhau.** Checklist `FUNC-DATE-001` yêu cầu test **timezone (JST/local)** và **23:00–23:59 / 00:00–00:59**. Dữ liệu ở đây nằm đúng vùng nguy hiểm: `expired_date_contract` luôn là **`...23:59:59`**. Hai đường tính chạy ở 2 nơi khác nhau: modal do **server** tính (PHP/Carbon, TZ ứng dụng) còn dòng 次回決済日 trên màn do **trình duyệt** tính (`moment(...).add(1,'day')`, TZ máy người dùng). QA team ở **ICT (UTC+7)**, khách hàng ở **JST (UTC+9)** — nếu giá trị truyền xuống JS có kèm offset/`Z`, `moment()` sẽ đổi sang giờ máy và `23:59:59` có thể **rơi về ngày hôm trước**, làm NEW-3 / NEW-7 ra kết quả khác nhau tùy máy ai chạy. NEW-3 và NEW-7 *có* so 2 đường tính nhưng chỉ ở **một** timezone. — **Fix**: `TC-FUNCDATE001-06` (§5).

- **[MAJOR] GAP-5 — `FUNC-DATE-001` (Cao) vi phạm RULE-01: chỉ có `Boundary`, thiếu `Normal` + `Abnormal`, không ghi lý do.** 5 TC gắn mã `FUNC-DATE-001` (NEW-6/7/8/9/14) **đều là `Boundary`**. Không TC nào loại `Normal` hay `Abnormal` gắn mã này, và cột `Ghi chú` **không ghi lý do thiếu**. — **Fix**: (a) `Normal` — đổi `Mã quan điểm liên kết` của **NEW-1** từ `TOOL-KNOW-002` (mã không tồn tại trong checklist, xem [MAJOR] tiếp theo) sang `FUNC-DATE-001`, **không cần viết TC mới**; (b) `Abnormal` — bổ sung `TC-FUNCDATE001-06` + `TC-FUNCDATE001-07` (§5).

- **[MAJOR] RULE-03 / F.1 — bộ TC KHÔNG có bảng duyệt quan điểm tầng 1, và 5/11 mã quan điểm không map được về `checklist-lme.md`.** Studio trả `test_viewpoint_selection = null` → **chưa ai duyệt tầng 1 từ trên xuống**, nên không có dòng nào ghi ◯/× kèm lý do (vi phạm RULE-03). Thêm vào đó, `Mã quan điểm liên kết` của 6/17 TC dùng mã **không tồn tại** trong [checklist-lme.md](../../framework/checklist-lme.md): `TOOL-KNOW-002` (NEW-1), `TOOL-VAL2-001` (NEW-5), `API-CONTRACT-001` (NEW-10, NEW-12), `TOOL-ERRHYG-001` (NEW-13); riêng NEW-11 điền `RULE-07` — đó là **mã RULE, không phải mã quan điểm**. Hệ quả: `/review-tc` không map được coverage cho 6 TC này, và ưu tiên (Cao/TB/Thấp) không suy ra được. — **Fix**: remap 6 TC theo bảng ở §4.3, và điền bảng quan điểm tầng 1 trong `04-tc-list.md` (mục "Base quan điểm test LME") **trước** vòng review 2.

- **[MAJOR] RULE-02 — 12 TC tick `Đạt` nhưng cột `Evidence thực tế` trống, và 0/17 TC ghi LOẠI evidence bắt buộc ở `Ghi chú`.** RULE-02: *"Chỉ tick Đạt khi đã đính kèm **đúng loại** bằng chứng"*. ⚠️ Lưu ý input: `testcase_list` của Studio **không trả về** trường evidence → **không thể kết luận từ file 04 rằng evidence thực sự không tồn tại**. — **Fix**: Leader mở trực tiếp Studio task #169 đối chiếu evidence của 12 TC `pass`; đồng thời bổ sung vào `Ghi chú` từng TC loại evidence bắt buộc (ví dụ: NEW-2 → *"screenshot modal + kết quả query `bot_contracts` / `bots` / `coupon_management` trước-sau"*; NEW-17 → *"screenshot DevTools Network kèm query version + 200"*).

- **[MAJOR] Cột `Trạng thái đánh giá spec` trống 17/17** (`spec_status = null` toàn bộ). Quy tắc: TC thiếu trường này → MAJOR, vì nguy cơ *tự suy diễn rồi cho Đạt*. Ở task này đặc biệt nghiêm trọng vì oracle "+1 ngày" **đang mâu thuẫn spec** (§6): các TC lẽ ra phải để `Spec không ghi` + ghi rõ **đã hỏi ai**, chứ không phải để trống rồi tick Đạt. — **Fix**: điền `Spec ghi rõ` cho các TC dựa BR-09/EP-05/EP-06; điền `Đã hỏi leader` + tên người cho các TC dựa oracle +1 ngày.

- **[MAJOR] GAP-6 — `DATA-DB-001` (Cao): không TC nào kiểm `WHERE` scope trên 2 tài khoản.** Luồng áp dụng coupon có **UPDATE** trên `bot_contracts` + `bots` (D1, D2) → trigger của `DATA-DB-001` là *"BẮT BUỘC với mọi chức năng có UPDATE hoặc DELETE"*. NEW-2 và ⛔NEW-11 có verify DB nhưng **chỉ trên 1 tài khoản** — không chứng minh được `WHERE` đủ `bot_id` / `bot_contract_id`. — **Fix**: `TC-DATADB001-01` (§5), chi phí rất thấp (1 lần apply + 2 query). *(Ghi chú cho Leader: luồng ghi DB **không bị chạm code** trong lần fix này, nên nếu Leader áp nguyên tắc "chỉ test layer bị chạm" thì có thể hạ mục này xuống [NIT]. `/review-tc` giữ ở MAJOR vì `DATA-DB-001` là quan điểm **Cao** và trigger ghi rõ "BẮT BUỘC".)*

- **[MAJOR] AP-3 — Happy-path-only regression cho T1.** Cả NEW-15 và NEW-16 đều có precondition là hợp đồng **bình thường, đang trả phí, thao tác được**; NEW-1 còn ghi rõ điều kiện *"nút không bị mờ — không đang chờ đăng ký thẻ, không đang chờ chuyển khoản"*. Nghĩa là **toàn bộ các trạng thái hợp đồng edge đều nằm ngoài bộ TC**: `延滞中` (quá hạn thanh toán), đang chờ chuyển khoản (`payment_method = 2`, `status_payment = 5`), free plan, hợp đồng đã đăng ký hủy. Đây đúng là nơi nhãn ngày dễ sai nhất vì `ステータス` được compute từ `expired_date_contract`. — **Fix**: `TC-PAYSTATE001-02` (§5).

- **[MAJOR] GAP-7 — `UI-002` (Trung bình) trigger khớp nhưng 0 TC chỉ định trình duyệt.** Không TC nào ghi browser/OS. `UI-002` yêu cầu tối thiểu **Mac Safari + Chrome** (checklist ghi rõ: *"user chính là chủ salon/cửa hàng nhỏ, dùng Safari nhiều"*, *"đặc biệt input ngày giờ"*). Rủi ro cụ thể: `moment()` / `new Date()` parse chuỗi `"2026-09-26 23:59:59"` (dấu cách, không có `T`) **khác nhau giữa Safari và Chrome** — Safari hay trả `Invalid Date`. Đúng loại lỗi mà NEW-15 đang canh (*"không hiện 'Invalid date'"*) nhưng lại không chạy trên Safari. — **Fix**: `TC-UI002-01` (§5).

- **[MAJOR] GAP-8 — `SEC-001` (Cao): chưa test truy cập chéo tài khoản ở 2 API vừa đổi payload.** ⛔NEW-13 có test `botContractId = 999999999` (**không tồn tại**) nhưng **không** test `botContractId` **của tổ chức khác đang tồn tại**. Response 2 API nay mang thêm 1 field ngày → cần khẳng định không rò thông tin hợp đồng của tenant khác. — **Fix**: `TC-SEC001-01` (§5) — chi phí thấp, gộp luôn vào lượt rerun ⛔NEW-13.

- **[MAJOR] `COMPAT-LEGACY-001` (Cao) / REQ-006 — tương thích ngược field cũ `new_expired_date` CHƯA verify.** TC duy nhất phủ điểm này là ⛔NEW-12 → **blocked**. Đây là điều kiện tiên quyết cho quyết định thiết kế của Dev ("giữ field cũ để không phá bên gọi khác") và cũng là điều kiện tiên quyết của GAP-3 (`DEPLOY-LIVE-001`). NEW-15 chỉ kiểm phía JS (*"không còn chuỗi `couponNewExpiredDate`"*), **không** kiểm field trong response API. — **Fix**: **không cần TC mới** — chạy lại ⛔NEW-12 sau khi gỡ blocked (xem GAP-2).

### 4.3 Minor (có thể fix sau)

- **[MINOR] Remap 6 mã quan điểm không tồn tại trong `checklist-lme.md`** (chi tiết đã nêu ở §4.2). Đề xuất remap:

  | TC | Mã Studio hiện tại | Đề xuất remap | Lý do |
  |---|---|---|---|
  | NEW-1 | `TOOL-KNOW-002` | `FUNC-DATE-001` | Đồng thời lấp `Normal` còn thiếu của RULE-01 |
  | NEW-5 | `TOOL-VAL2-001` | `FUNC-002` | Bỏ trống / mã không tồn tại / mã đã dùng = nhánh validate input |
  | NEW-10 | `API-CONTRACT-001` | `OUT-TRUTH-001` | Response phải khớp trạng thái thật + không ghi dữ liệu |
  | NEW-11 | `RULE-07` (là RULE, không phải quan điểm) | `DATA-DB-001` | Verify 3 tầng + dữ liệu ghi xuống không đổi |
  | NEW-12 | `API-CONTRACT-001` | `COMPAT-LEGACY-001` | Tương thích ngược field cũ ⇄ mới |
  | NEW-13 | `TOOL-ERRHYG-001` | `FUNC-002` hoặc `OUT-TRUTH-001` | Nhánh lỗi trả thông báo đúng, không rò field |

  Sau khi remap, `TC No.` phải đánh lại theo `TC-<mã quan điểm bỏ gạch>-<nn>`.

- **[MINOR] AP-4 — không có link PR / diff để verify fix shape thực tế.** File 03 chỉ có commit hash `8ef593df85` + branch `ai_small_39736`, không có URL Github/Gitlab. Reviewer phải tự checkout branch mới đọc được diff. — **Fix**: yêu cầu Dev bổ sung link so sánh nhánh vào Redmine.

- **[MINOR] `REG-SHARED-001` — chưa rà chiều BRAND.** Checklist yêu cầu rà **Lme / Lwaka / Saruwaka / Lgram**. File 03 không nói `public/_assets/modules/bill/js/detail.js` có được brand khác dùng chung hay không. — **Fix**: hỏi Dev 1 câu; nếu dùng chung → bổ sung TC smoke màn chi tiết hợp đồng cho brand đó.

- **[MINOR] `DEPLOY-ASSET-001` (Cao) vi phạm RULE-01 nhẹ** — chỉ có 1 TC loại `Abnormal` (NEW-17), thiếu `Normal` + `Boundary`, không ghi lý do ở `Ghi chú`. — **Fix**: ghi lý do (*"quan điểm không có khái niệm biên"*) là đủ, không cần thêm TC.

- **[MINOR] 5 TC `blocked` vẫn có `Người thực hiện` = `hanhntb` và `Ngày thực hiện` = `2026-08-19`.** TC chưa chạy mà có người + ngày thực thi → đọc lướt dễ tưởng đã chạy. — **Fix**: để trống 2 cột này cho tới khi TC thật sự chạy xong.

- **[MINOR] Tỉ lệ loại case lệch — `Normal` 11 / `Abnormal` 2 / `Boundary` 4 (65% / 12% / 23%)** so với gợi ý 40/35/25 của §C review-checklist. Thiếu rõ rệt `Abnormal`. Các TC §5 bổ sung 4 `Abnormal` sẽ kéo về ~55/25/20.

### 4.4 Nit (gợi ý)

- **[NIT] `CONC-001` — double-click nút 「クーポンコードの利用を確定する」.** Trigger *"nút thực thi hành động quan trọng"* khớp (áp coupon = gia hạn hợp đồng), nhưng luồng ghi **không bị chạm code** lần này → `/review-tc` đánh × với lý do đó. Nếu Leader muốn chắc, đây là TC rẻ nhất còn thiếu: double-click → verify chỉ 1 bản ghi 操作履歴 và hạn hợp đồng chỉ +1 tháng.

- **[NIT] Gộp 2 điểm "nhãn còn lệch 1 ngày" đã biết vào 1 ticket riêng.** Dev nêu màn **Cài đặt điểm (ポイント設定 / SCR-BLP-01)**; NEW-16 phát hiện thêm dòng **「クーポン適用後の次回決済日」 trong modal 操作履歴** cũng hiển thị hạn hợp đồng thô (`2026/09/26`). **Cả hai đều KHÔNG phải bug của ticket này** — nhưng cùng một họ lỗi, nên mở **1 ticket chung** thay vì 2, kèm rà toàn bộ nơi hiển thị nhãn 次回決済日 (spec `billing-plan` liệt kê ít nhất 2 màn: dòng 101 và dòng 183).

- **[NIT] Task Studio #169 đang `reviewed = false`, toàn bộ 17 TC ở `status = draft`.** Sau khi fix xong nên chuyển TC sang trạng thái chính thức trên Studio để lần fetch sau không lẫn với bản nháp.

- **[NIT] RULE-11 — không dùng §4 checklist-lme để flag.** Đã kiểm: task này không chạm FORM-01 / CHAT-01 / ADM-01/03/04 / TPL-01. Không có mục nào ở §4 được dùng để flag trong report này.

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` ở round tiếp theo. Bảng dùng **đúng 16 cột canonical**.
> **Lưu ý**: 5 TC ⛔ blocked (NEW-10/11/12/13/14) **không** cần viết lại — chỉ cần gỡ blocked và chạy (xem GAP-2). Bảng dưới chỉ gồm TC **chưa tồn tại**.

> ### 🆕 Trạng thái đẩy lên Studio (cập nhật 2026-08-19)
>
> | TC No. | Đã tạo trên Studio? | Studio id / temp_id | client_ref |
> |---|---|---|---|
> | `TC-ENV003-01` | ✅ **Đã tạo** | #11148 / NEW-18 | `review-39736-r1-env003-01` |
> | `TC-DATADB001-01` | ✅ **Đã tạo** | #11149 / NEW-19 | `review-39736-r1-datadb001-01` |
> | `TC-FUNCDATE001-06` | ✅ **Đã tạo** | #11150 / NEW-20 | `review-39736-r1-funcdate001-06` |
> | `TC-DEPLOYLIVE001-01` | ❌ chưa | — | — |
> | `TC-FUNCDATE001-07` | ❌ chưa | — | — |
> | `TC-PAYSTATE001-01` | ❌ chưa | — | — |
> | `TC-PAYSTATE001-02` | ❌ chưa | — | — |
> | `TC-UI002-01` | ❌ chưa | — | — |
> | `TC-SEC001-01` | ❌ chưa | — | — |
>
> ⚠️ **`TC-DEPLOYLIVE001-01` (lấp BLOCKER GAP-3) chưa được đẩy lên Studio** — vẫn còn là gap chưa có TC trên tool.
>
> ⚠️ Sau khi thêm 3 TC, `aiResult` của task #169 chuyển từ `pass` → **`null`**. Ngoài ra Studio ghi nhận lượt chạy mới (`runBy = ngannt`, `ranAt = 2026-08-19 10:45:19`) làm exec của **17 TC gốc** đổi từ `12 pass / 5 other` → **`11 pass / 6 other`** — **1 TC gốc đã rớt khỏi trạng thái Đạt sau khi report này được viết**. Cần fetch lại Studio để xác định TC nào trước khi chốt verdict.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENV003-01 | ENV-003 | Normal | Smoke modal coupon + version asset JS trên PRODUCTION ngay sau deploy (bill tiền — không kết luận từ staging) | - Bản fix đã deploy lên production (`step.lme.jp`).<br>- Có 1 hợp đồng bot **thật** đang active, đã thanh toán, nút 「クーポンコードを入力する」 không bị mờ.<br>- Có 1 mã coupon chưa sử dụng do Admin phát hành **riêng cho lần smoke này**.<br>- Đã ghi lại `expired_date_contract` hiện tại của hợp đồng trước khi thao tác. | 1. Mở màn 「ポイント設定」 trên production → vào chi tiết hợp đồng đã chuẩn bị; ghi lại ngày ở dòng 「次回決済日」.<br>2. Mở DevTools > Network, F5 **thường** (KHÔNG Ctrl+F5); tìm `public/_assets/modules/bill/js/detail.js`, ghi lại query version + HTTP status.<br>3. Mở nội dung file JS trình duyệt vừa tải; tìm chuỗi `couponNextPaymentDate` và chuỗi `couponNewExpiredDate`.<br>4. Bấm 「クーポンコードを入力する」, nhập mã coupon, bấm 「次へ」; ghi lại ngày trên modal bước xác nhận.<br>5. Bấm 「クーポンコードの利用を確定する」; ghi lại ngày trên modal bước thành công.<br>6. F5 lại màn chi tiết; so ngày ở dòng 「次回決済日」 với ngày modal vừa báo.<br>7. Query lại `bot_contracts.expired_date_contract` và `bots.expired_date` của hợp đồng này. | Hợp đồng bot thật trên production (ghi lại `date_add_contract` + `expired_date_contract` trước khi chạy). Mã coupon: `PRD-39736-A` (chưa sử dụng). Phép tính tay: ngày kỳ vọng trên modal = `expired_date_contract` sau khi áp dụng + 1 ngày. | Bước 2: file `detail.js` trả **HTTP 200** với **query version MỚI** (khác version trước deploy), không 404. Bước 3: file chứa `couponNextPaymentDate`, **không còn** `couponNewExpiredDate`. Bước 4 + 5: cả 2 modal hiển thị **cùng một ngày** = `expired_date_contract` sau khi áp dụng **+ 1 ngày**, không bị trống, không hiện `Invalid date`. Bước 6: dòng 「次回決済日」 sau F5 trỏ **đúng cùng ngày lịch** với modal. Bước 7: dữ liệu ghi xuống **KHÔNG cộng thêm 1 ngày** (giữ đúng `...23:59:59` của ngày liền trước). | Chưa test | | **PRODUCTION** | | | | Đã hỏi leader | Lấp **GAP-1** — cover `ENV-003` + `DEPLOY-ASSET-001` trên production (RULE-08: bill tiền / asset **không** kết luận từ staging). Cover impact F1, F2, F3, F4, D1, D2, T1, T2. **Evidence bắt buộc**: screenshot DevTools Network (query version + 200) + screenshot 2 modal + kết quả query DB trước/sau. ⚠️ Dùng hợp đồng **thật** → chọn bot nội bộ, KHÔNG dùng hợp đồng khách hàng; báo Leader trước khi chạy. |
| TC-DEPLOYLIVE001-01 | DEPLOY-LIVE-001 | Abnormal | Client cũ chưa reload gọi server mới: modal coupon không vỡ, không hiện ngày trống | - Có 2 mốc thời gian rõ ràng: **trước** và **sau** khi deploy bản fix lên môi trường test.<br>- Trước deploy: mở sẵn màn chi tiết hợp đồng bot và **giữ nguyên tab, KHÔNG reload** trong suốt TC.<br>- Có 1 mã coupon chưa sử dụng riêng cho lần chạy này.<br>- Không bật maintain khi deploy. | 1. **Trước deploy**: mở màn chi tiết hợp đồng bot; để nguyên tab, không đóng, không F5.<br>2. Deploy bản fix (2 API + JS + view) lên môi trường test, **không bật maintain**.<br>3. Quay lại **đúng tab cũ** (JS cũ vẫn đang chạy trong trang), bấm 「クーポンコードを入力する」.<br>4. Nhập mã coupon rồi bấm 「次へ」; đọc câu thông báo ở bước xác nhận và ghi lại ngày (hoặc ghi "trống" nếu không có ngày).<br>5. Mở DevTools > Console, kiểm có lỗi JavaScript nào không.<br>6. Bấm 「クーポンコードの利用を確定する」; đọc câu thông báo bước thành công.<br>7. Query `bot_contracts.expired_date_contract`, `bots.expired_date`, trạng thái mã coupon và bản ghi 操作履歴 mới.<br>8. F5 trang, lặp lại bước 3–4 với mã coupon thứ hai để đối chứng. | Hợp đồng bot: ngày bắt đầu thanh toán `2026-06-27 00:00:00`, hạn hợp đồng `2026-08-26 23:59:59`. Mã coupon lần 1 (client cũ): `TC39736-LIVE-1`; mã coupon lần 2 (client mới, đối chứng): `TC39736-LIVE-2`. | Bước 4: câu thông báo **vẫn hiển thị một ngày**, KHÔNG để trống, KHÔNG hiện `undefined` / `Invalid date` — vì server mới **vẫn giữ** field cũ `new_expired_date`. Chấp nhận ngày hiển thị là ngày **cũ** (`2026/09/26`, tức chưa có fix) — đây là hành vi mong đợi của client cũ. Bước 5: **không có lỗi JavaScript** nào trong console. Bước 6 + 7: giao dịch vẫn hoàn tất đúng — `expired_date_contract` và `bots.expired_date` = `2026-09-26 23:59:59`, mã coupon chuyển sang đã dùng, phát sinh **đúng 1** bản ghi 操作履歴; **không** exception 500, **không** lưu nửa vời. Bước 8 (đối chứng sau F5): modal hiển thị `2026/10/27` — tức client mới đọc field mới đúng. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-3** — cover `DEPLOY-LIVE-001` (Cao). Cover impact F1, F2, F3, F4. Kịch bản này **NEW-17 không phủ được** (NEW-17 có F5 ở bước 1). Đây cũng là TC duy nhất chứng minh quyết định "giữ lại field cũ `new_expired_date`" của Dev thật sự có tác dụng. **Evidence bắt buộc**: screenshot modal ở tab cũ + screenshot Console (không lỗi) + kết quả query DB + screenshot đối chứng sau F5. |
| TC-DATADB001-01 | DATA-DB-001 | Normal | Áp coupon ở bot A không được đụng hợp đồng bot B (kiểm `WHERE` scope trên 2 tài khoản) | - Có **2 hợp đồng bot riêng biệt** A và B, **cùng ngày neo thanh toán** và **cùng hạn hợp đồng** để dễ phát hiện ghi nhầm.<br>- Cả 2 đều đang active, đã thanh toán, thao tác được.<br>- Có 1 mã coupon chưa sử dụng.<br>- Đã query và ghi lại `bot_contracts.expired_date_contract` + `bots.expired_date` của **cả A và B** trước khi thao tác. | 1. Query và ghi lại `expired_date_contract` + `bots.expired_date` của **cả 2** hợp đồng A và B (kèm câu query).<br>2. Vào màn chi tiết hợp đồng **A**, áp dụng mã coupon tới bước thành công.<br>3. Query lại `expired_date_contract` + `bots.expired_date` của **cả 2** hợp đồng A và B.<br>4. Query bảng 操作履歴 (`bot_life_cycles`) lọc theo hợp đồng A và theo hợp đồng B.<br>5. Mở màn chi tiết hợp đồng **B**, đọc dòng 「次回決済日」 và danh sách 「操作履歴」. | Hợp đồng A: ngày bắt đầu thanh toán `2026-06-27 00:00:00`, hạn hợp đồng `2026-08-26 23:59:59`. Hợp đồng B: **cùng** ngày bắt đầu thanh toán và **cùng** hạn hợp đồng như A (cố ý trùng để lộ lỗi thiếu `WHERE`). Mã coupon: `TC39736-SCOPE-A`. | Hợp đồng **A**: `expired_date_contract` và `bots.expired_date` → `2026-09-26 23:59:59`; phát sinh **đúng 1** bản ghi 操作履歴 loại áp dụng coupon; modal báo `2026/09/27`. Hợp đồng **B**: `expired_date_contract` và `bots.expired_date` **giữ nguyên `2026-08-26 23:59:59`, không đổi 1 giây nào**; **KHÔNG** phát sinh bản ghi 操作履歴 nào; dòng 「次回決済日」 trên màn B không đổi. Không có bản ghi mồ côi. | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **GAP-6** — cover `DATA-DB-001` (RULE-07: tạo bản ghi trùng ở 2 tài khoản để kiểm chứng `WHERE`). Cover impact D1, D2, F2. **Evidence bắt buộc**: ảnh chụp kết quả query **trước và sau**, **kèm câu query**, cho **cả 2** tài khoản. |
| TC-FUNCDATE001-06 | FUNC-DATE-001 | Abnormal | Timezone trình duyệt khác JST: ngày trên modal (server tính) và dòng 次回決済日 (trình duyệt tính) không được lệch nhau | - Có 1 hợp đồng bot thao tác được và 1 mã coupon chưa sử dụng.<br>- Chuẩn bị **cùng 1 máy**, đổi được timezone hệ điều hành giữa **JST (UTC+9)** và **ICT (UTC+7)**.<br>- Biết trước `expired_date_contract` hiện tại (luôn kết thúc bằng `23:59:59` — đây là giá trị sát ranh giới ngày). | 1. Đặt timezone máy = **JST (UTC+9)**, mở lại trình duyệt, vào màn chi tiết hợp đồng; ghi lại ngày ở dòng 「次回決済日」.<br>2. Áp dụng mã coupon tới bước thành công; ghi lại ngày ở **cả** bước xác nhận và bước thành công.<br>3. F5 màn chi tiết; ghi lại ngày ở dòng 「次回決済日」 sau khi áp dụng.<br>4. Đổi timezone máy sang **ICT (UTC+7)**, mở lại trình duyệt (không xoá dữ liệu), vào **cùng** màn chi tiết đó; ghi lại ngày ở dòng 「次回決済日」.<br>5. Mở DevTools > Network, xem response của API kiểm tra coupon và ghi lại **nguyên văn chuỗi ngày** server trả về (có kèm `Z` / offset hay không).<br>6. Lặp lại bước 2 với mã coupon thứ hai khi đang ở timezone ICT; ghi lại ngày trên 2 modal. | Hợp đồng bot: ngày bắt đầu thanh toán `2026-06-27 00:00:00`, hạn hợp đồng `2026-08-26 23:59:59`. Mã coupon lần JST: `TC39736-TZ-JST`; mã coupon lần ICT: `TC39736-TZ-ICT`. Timezone test: `Asia/Tokyo` (UTC+9) và `Asia/Ho_Chi_Minh` (UTC+7). | Ở **cả 2 timezone**, ngày trên modal và ngày ở dòng 「次回決済日」 phải **trỏ cùng một ngày lịch**, và ngày đó **không đổi** khi chuyển timezone: bước 1–3 (JST) ra `2026/09/27` thì bước 4 (ICT) trên **cùng** hợp đồng cũng phải là `2026年09月27日`, không được lùi về `2026年09月26日`. Không xuất hiện `Invalid date`. Bước 5: ghi nhận nguyên văn chuỗi ngày trong response — nếu chuỗi có `Z` hoặc offset thì đây chính là nguồn rủi ro, phải báo Leader kể cả khi kết quả hiển thị đang đúng. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-4** + **GAP-5 (nhánh Abnormal của RULE-01)** — cover `FUNC-DATE-001` (checklist yêu cầu test **timezone JST/local** và mốc **23:00–23:59**). Cover impact F1, F3, F6. Rủi ro thật: modal do **server** tính (PHP/Carbon) còn dòng trên màn do **trình duyệt** tính (`moment().add(1,'day')`) — QA ở ICT, khách ở JST. `Trạng thái đánh giá spec = Spec không ghi` → **phải hỏi Leader/Dev** timezone chuẩn là gì trước khi kết luận Đạt. **Evidence bắt buộc**: screenshot cặp (modal + dòng 次回決済日) ở **từng** timezone + screenshot response API trong Network tab. |
| TC-FUNCDATE001-07 | FUNC-DATE-001 | Abnormal | Hạn hợp đồng rỗng / không hợp lệ: modal không hiện `Invalid date`, không hiện ngày trống | - Có 1 hợp đồng bot được dựng với `bot_contracts.expired_date_contract` ở trạng thái bất thường theo phần Dữ liệu nhập.<br>- Nút 「クーポンコードを入力する」 vẫn bấm được.<br>- Có 2 mã coupon chưa sử dụng (mỗi bộ dữ liệu 1 mã).<br>- Mở sẵn DevTools > Console để bắt lỗi JavaScript. | 1. Dựng hợp đồng theo **bộ dữ liệu 1** (hạn hợp đồng NULL); mở màn chi tiết, ghi lại dòng 「次回決済日」 đang hiển thị gì.<br>2. Bấm 「クーポンコードを入力する」, nhập mã coupon, bấm 「次へ」; đọc câu thông báo ở bước xác nhận.<br>3. Đọc Console xem có lỗi JavaScript không; đọc Network xem response API trả gì ở field ngày.<br>4. Nếu modal cho phép, bấm 「クーポンコードの利用を確定する」 và ghi lại kết quả + trạng thái dữ liệu sau đó.<br>5. Lặp lại bước 1–4 với **bộ dữ liệu 2** (hạn hợp đồng là chuỗi ngày không hợp lệ). | Bộ 1: `bot_contracts.expired_date_contract = NULL`, ngày bắt đầu thanh toán `2026-06-27 00:00:00`, mã coupon `TC39736-NULL-1`. Bộ 2: `expired_date_contract = '0000-00-00 00:00:00'`, ngày bắt đầu thanh toán `2026-06-27 00:00:00`, mã coupon `TC39736-NULL-2`. | Cả 2 bộ: màn hình và modal **KHÔNG** hiển thị chuỗi `Invalid date`, `NaN`, `undefined` hay ô ngày trống. Hệ thống hoặc (a) hiển thị một ngày hợp lệ tính theo nhánh dự phòng, hoặc (b) chặn thao tác với **thông báo lỗi rõ ràng bằng tiếng Nhật** — cả hai đều chấp nhận được, nhưng **không được** hiện thông báo nửa vời có chỗ trống. **Không** có lỗi JavaScript trong Console; **không** trả HTTP 5xx. Nếu bấm xác định sử dụng: hoặc bị chặn và mã coupon **giữ nguyên chưa dùng**, hoặc hoàn tất và dữ liệu ghi xuống đúng định dạng datetime hợp lệ — **không** được ghi `NULL` / `0000-00-00` xuống `expired_date_contract`. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-5 (nhánh Abnormal của RULE-01 cho `FUNC-DATE-001` — quan điểm Cao)**. Cover impact F1, F3, F5, D1. Bản fix cộng `+1 ngày` lên giá trị server trả về → đầu vào bất thường là nơi dễ sinh `Invalid date` nhất; NEW-15 có canh chuỗi này nhưng chỉ trên hợp đồng bình thường. `Spec không ghi` → **hỏi Dev/Leader** hành vi mong đợi (chặn hay fallback) trước khi kết luận Đạt. **Evidence bắt buộc**: screenshot modal + screenshot Console + screenshot response API cho **từng** bộ dữ liệu. |
| TC-PAYSTATE001-01 | PAY-STATE-001 | Normal | Đối chứng oracle: ngày trừ tiền THẬT trong lịch sử có đúng bằng hạn hợp đồng + 1 ngày không | - Có 1 hợp đồng bot **đã phát sinh ít nhất 2 lần thanh toán thành công** trong quá khứ (đọc được ở 「操作履歴」 / lịch sử thanh toán).<br>- Có quyền query `bot_life_cycles` và `payment_histories` của hợp đồng đó.<br>- **TC read-only** — KHÔNG chạy job, KHÔNG áp coupon, KHÔNG sửa dữ liệu. | 1. Mở màn chi tiết hợp đồng bot; lọc 「操作履歴」 theo nhóm 決済 và ghi lại **ngày** của 2 lần thanh toán thành công gần nhất (gọi là P1, P2).<br>2. Query `payment_histories` của hợp đồng, ghi lại thời điểm ghi nhận thanh toán của P1 và P2.<br>3. Query `bot_contracts.expired_date_contract` **tại thời điểm ngay trước** mỗi lần thanh toán (suy từ giá trị hiện tại trừ ngược theo chu kỳ, hoặc lấy từ bản ghi lịch sử nếu có lưu).<br>4. Tính hiệu: `ngày thanh toán thật (P) − hạn hợp đồng ngay trước đó`.<br>5. Đối chiếu kết quả bước 4 với con số **+1 ngày** mà bản fix đang hiển thị trên modal coupon.<br>6. Ghi lại kết luận và báo Leader. | Hợp đồng bot có lịch sử thanh toán thật (ưu tiên bot nội bộ, chu kỳ 毎月払い). Phép tính tay: nếu `expired_date_contract` trước lần thanh toán là `YYYY-MM-DD 23:59:59` và job charge vào `YYYY-MM-(DD+1)` thì hiệu = **+1 ngày** ⇒ oracle của bản fix đúng. | Hiệu tính ở bước 4 = **đúng +1 ngày** cho **cả 2** lần thanh toán ⇒ oracle "ngày thanh toán tiếp theo = hạn hợp đồng + 1 ngày" được xác nhận bằng dữ liệu thật, bản fix hiển thị đúng. Nếu hiệu = **0 ngày** (job charge đúng vào ngày `expired_date_contract`) ⇒ **bản fix đang hiển thị muộn hơn ngày trừ tiền thật 1 ngày** → phải **raise ticket** và dừng approve. Nếu 2 lần cho ra 2 kết quả khác nhau ⇒ ghi nhận và escalate Leader. | Chưa test | | **PRODUCTION** | | | | Đã hỏi leader | Lấp **GAP ORACLE** ([MAJOR] §4.2) — cover `PAY-STATE-001` + **RULE-06** (đi tới output cuối chuỗi = giao dịch tiền thật). Cover impact BUG, F5. **TC read-only, không sửa dữ liệu** → an toàn chạy production; RULE-08 yêu cầu bill tiền phải verify ở production. ⚠️ **Cố ý KHÔNG đề xuất TC chạy `AutoPaymentJobUnivapay`** — job không bị chạm code lần này, chạy job là over-coverage (AP-5). **Evidence bắt buộc**: screenshot 「操作履歴」 lọc nhóm 決済 + kết quả query kèm câu query + bảng tính tay hiệu số ngày. |
| TC-PAYSTATE001-02 | PAY-STATE-001 | Abnormal | Modal coupon ở các trạng thái hợp đồng edge (延滞中 / chờ chuyển khoản / free plan) | - Chuẩn bị **3 hợp đồng bot** ở 3 trạng thái khác nhau theo phần Dữ liệu nhập.<br>- Có 3 mã coupon chưa sử dụng (mỗi hợp đồng 1 mã).<br>- Ghi lại `status`, `status_payment`, `payment_method`, `expired_date_contract` của từng hợp đồng trước khi thao tác. | 1. Mở màn chi tiết hợp đồng **bộ 1** (延滞中 — quá hạn thanh toán); ghi lại 「ステータス」 và dòng 「次回決済日」; kiểm nút 「クーポンコードを入力する」 có bấm được không.<br>2. Nếu bấm được: nhập mã coupon → 「次へ」 → ghi lại ngày trên modal; nếu bị chặn: ghi lại thông báo/trạng thái nút.<br>3. Lặp lại bước 1–2 với **bộ 2** (đang chờ chuyển khoản, `payment_method = 2`).<br>4. Lặp lại bước 1–2 với **bộ 3** (free plan).<br>5. Với mọi bộ bấm được tới bước thành công: query lại `expired_date_contract` + `bots.expired_date` và đối chiếu với ngày modal đã báo.<br>6. Đọc Console mỗi lần để bắt lỗi JavaScript. | Bộ 1 (延滞中): `expired_date_contract` = ngày chạy test **trừ 10 ngày**, có lỗi thanh toán; mã `TC39736-EDGE-1`. Bộ 2 (chờ chuyển khoản): `payment_method = 2`, `status_payment = 5`, có `expired_date_bank_transfer`; mã `TC39736-EDGE-2`. Bộ 3 (free plan): hợp đồng gói free còn hạn; mã `TC39736-EDGE-3`. | Mỗi bộ chỉ được rơi vào **đúng 1 trong 2** kết quả, và phải **nhất quán với spec/nút**: (a) nút bị mờ / thao tác bị chặn kèm **thông báo rõ ràng** — chấp nhận, ghi nhận; hoặc (b) thao tác được thì ngày trên **cả 2 modal** = `expired_date_contract` sau khi áp dụng **+ 1 ngày**, đúng cùng công thức như hợp đồng bình thường. **Tuyệt đối không** được: hiện ngày trong quá khứ, hiện `Invalid date` / ô trống, sập màn, hoặc ghi dữ liệu nửa vời (modal báo thành công nhưng DB không đổi). Không có lỗi JavaScript ở mọi bộ. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **AP-3** ([MAJOR] §4.2) — cover `PAY-STATE-001` + `UI-003`. Cover impact T1, F1, F2, F3, F4. Lý do: toàn bộ 17 TC hiện có đều dùng hợp đồng "sạch, đang trả phí, thao tác được" (NEW-1 ghi rõ điều kiện này) → chưa TC nào chạm trạng thái edge, trong khi 「ステータス」 được compute từ chính `expired_date_contract`. `Spec không ghi` → **hỏi Leader** hành vi mong đợi của nút coupon ở từng trạng thái. **Evidence bắt buộc**: screenshot 「ステータス」 + modal (hoặc nút bị chặn) + kết quả query DB cho **từng** bộ. |
| TC-UI002-01 | UI-002 | Normal | Modal coupon hiển thị ngày đúng trên Mac Safari và Chrome (parse chuỗi datetime khác nhau) | - Có máy **Mac** cài sẵn **Safari** và **Chrome**.<br>- Có 1 hợp đồng bot thao tác được và 2 mã coupon chưa sử dụng (mỗi trình duyệt 1 mã).<br>- Mở sẵn DevTools/Web Inspector Console trên cả 2 trình duyệt.<br>- Độ phân giải màn hình đặt về **1366×768** (mức thấp nhất hỗ trợ). | 1. Trên **Mac Safari**: vào màn chi tiết hợp đồng; ghi lại dòng 「次回決済日」.<br>2. Bấm 「クーポンコードを入力する」, nhập mã coupon 1, bấm 「次へ」; ghi lại ngày ở bước xác nhận.<br>3. Bấm 「クーポンコードの利用を確定する」; ghi lại ngày bước thành công; đọc Web Inspector Console.<br>4. F5 và ghi lại dòng 「次回決済日」 sau khi áp dụng.<br>5. Trên **Mac Chrome**: lặp lại bước 1–4 với mã coupon 2 (trên hợp đồng khác hoặc sau khi reset dữ liệu).<br>6. Ở cả 2 trình duyệt, kiểm modal không vỡ layout tại 1366×768 và 2 nút 「次へ」 / 「クーポンコードの利用を確定する」 đều bấm được. | Hợp đồng bot: ngày bắt đầu thanh toán `2026-06-27 00:00:00`, hạn hợp đồng `2026-08-26 23:59:59`. Mã coupon Safari: `TC39736-SAFARI`; mã coupon Chrome: `TC39736-CHROME`. Chuỗi datetime cần soi: `expired_date_contract` dạng `"2026-09-26 23:59:59"` (dấu cách, **không** có ký tự `T`). | Trên **cả Safari và Chrome**: modal bước xác nhận và bước thành công hiển thị **cùng một ngày** `2026/09/27`; dòng 「次回決済日」 sau F5 hiển thị `2026年09月27日`. **Không** trình duyệt nào hiện `Invalid Date` / `NaN` / ô ngày trống. **Không** có lỗi JavaScript trong Console. Ở 1366×768: modal không vỡ layout, cả 2 nút bấm được. | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **GAP-7** — cover `UI-002` + `UI-001` (checklist yêu cầu tối thiểu **Mac Safari + Chrome**, "đặc biệt input ngày giờ", và mốc **1366×768**). Cover impact F3, F4, T1. Rủi ro thật: Safari parse chuỗi `"YYYY-MM-DD HH:mm:ss"` (dấu cách, không `T`) **khác** Chrome và hay trả `Invalid Date` — đúng chuỗi mà NEW-15 đang canh nhưng NEW-15 không chạy trên Safari. **Evidence bắt buộc**: screenshot modal + dòng 次回決済日 trên **từng** trình duyệt + screenshot Console. |
| TC-SEC001-01 | SEC-001 | Abnormal | Gọi 2 API coupon với `botContractId` của tổ chức KHÁC: bị chặn, không rò ngày hợp đồng | - Có **2 tài khoản admin thuộc 2 tổ chức khác nhau**: tài khoản X (dùng để gọi) và tài khoản Y (nạn nhân).<br>- Biết `botId` / `botContractId` **có thật, đang tồn tại** của tổ chức Y.<br>- Có phiên đăng nhập hợp lệ của tài khoản **X** kèm mã chống giả mạo biểu mẫu lấy từ trang chi tiết hợp đồng của **chính X**.<br>- Có 1 mã coupon chưa sử dụng.<br>- Đã ghi lại `expired_date_contract` của hợp đồng Y trước khi thử. | 1. Đăng nhập bằng tài khoản **X**, mở màn chi tiết hợp đồng của X để lấy phiên + mã chống giả mạo biểu mẫu.<br>2. Gọi endpoint **kiểm tra** mã coupon với mã coupon hợp lệ nhưng `botId` / `botContractId` **của tổ chức Y**; ghi lại mã trạng thái HTTP và **toàn bộ** nội dung phản hồi.<br>3. Gọi endpoint **áp dụng** mã coupon với cùng tham số của Y; ghi lại phản hồi.<br>4. Query `bot_contracts.expired_date_contract` + `bots.expired_date` của hợp đồng **Y** và trạng thái mã coupon.<br>5. Đăng nhập tài khoản Y, mở màn chi tiết hợp đồng Y và danh sách 「操作履歴」 để xác nhận không có thay đổi. | Tài khoản gọi: X. Tài khoản nạn nhân: Y (`botContractId` thật của Y). Mã coupon: `TC39736-SEC` (chưa sử dụng). Đối chứng: `expired_date_contract` của Y ghi lại trước khi thử. | Cả 2 lời gọi đều **bị chặn**: trả về trạng thái thất bại (hoặc 403/404), **KHÔNG** trả HTTP 5xx. Phản hồi **KHÔNG chứa** bất kỳ field ngày nào của hợp đồng Y — cụ thể **không có** `new_expired_date` và **không có** `new_next_payment_date`, cũng không có thông tin nhận dạng nào khác của Y. Dữ liệu của **Y không đổi**: `expired_date_contract` và `bots.expired_date` giữ nguyên, **không** phát sinh bản ghi 操作履歴 nào ở Y. Mã coupon **vẫn ở trạng thái chưa dùng** (không bị đánh dấu đã dùng oan). | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-8** — cover `SEC-001` (Cao). Cover impact F1, F2, D1, D2. Bổ sung cho ⛔NEW-13: NEW-13 chỉ thử `botContractId = 999999999` (**không tồn tại**), chưa thử ID **có thật của tenant khác** — chỉ trường hợp sau mới chứng minh được `WHERE` có scope theo tổ chức. Nên **gộp chạy cùng lượt rerun ⛔NEW-13** (xem GAP-2) để tiết kiệm công dựng env. ⚠️ Liên quan **BR-08** đã biết: với endpoint áp dụng, `botContractId` sai có thể vẫn đánh dấu mã coupon đã dùng — nếu quan sát thấy, ghi nhận là **lỗi có sẵn**, tách ticket riêng, không kết luận bản fix hỏng. **Evidence bắt buộc**: nguyên văn response 2 lời gọi + kết quả query DB của Y trước/sau + screenshot màn Y. |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:

**(1) Mâu thuẫn trực tiếp — `spec-features/admin/billing-plan/feature-spec.md`**

- **Section**: bảng field SCR-BLP-02 (**dòng 183**) và bảng field SCR-BLP-01 (**dòng 101**), cùng bảng "Field → DB source" (dòng 511, 521).
- **Hiện trạng**: spec ghi 次回決済(更新)日 = `bot_contracts.expired_date_contract` — tức **giá trị thô, KHÔNG cộng 1 ngày**.
- **Sau fix #39736**: modal coupon hiển thị `expired_date_contract` **+ 1 ngày**, và Dev xác nhận dòng 次回決済日 trên màn chi tiết cũng dùng `+ 1 ngày` (`detail.js expiredDateContract()`).
- **⚠️ Đây là mâu thuẫn thật, không phải nhầm lẫn diễn đạt** — và là lý do `/review-tc` flag [MAJOR] ORACLE ở §4.2: bộ TC hiện tại **không có nguồn độc lập nào** để chốt con số +1 ngày. Phải làm rõ **trước** khi đóng ticket: nhãn 次回決済日 đúng là `expired_date_contract` hay `expired_date_contract + 1`?
- **Nội dung cần update**: ghi rõ công thức hiển thị của **từng** màn (SCR-BLP-01 vs SCR-BLP-02 vs modal coupon vs modal 操作履歴) — vì theo ghi nhận của Dev + NEW-16, **4 nơi này hiện KHÔNG đồng nhất**.
- **Người chịu trách nhiệm**: `<PM / Dev owner FA-031 — Leader chỉ định>`

**(2) Bổ sung phần coupon đang bỏ trống trong spec**

- **Section**: mục 9 "Gaps" của cùng file — **[M2] Coupon code — chưa xác định hoàn toàn** (dòng ~789–794) và câu hỏi mở số 1 (dòng ~846): *"Coupon code: Bảng DB lưu ở đâu? Endpoint xử lý là gì?"*. Ngoài ra dòng 187 và 525 đang ghi クーポンコード = `Chưa xác định`, dòng 221 ghi 「クーポンコードの適用」 = `(chưa xác định type)`.
- **Nội dung cần update** — ticket này đã trả lời được phần lớn: 2 endpoint `POST /ajax/check-coupon-code` và `POST /ajax/apply-coupon-code` (tham số `coupon`, `botId`, `botContractId`); field response `new_expired_date` (cũ, **vẫn giữ**) + `new_next_payment_date` (**mới**); bảng lưu mã là `coupon_management`; bản ghi lịch sử 「クーポンコードの適用」 = **type 29**.
- **Người chịu trách nhiệm**: `<Dev owner FA-031>`

**(3) `api-spec.md` mô tả response cũ** — Studio đã ghi nhận ở note của ⛔NEW-12: tài liệu api-spec vẫn mô tả response chưa có `new_next_payment_date`, và **tiền tố đường dẫn ghi `/admin` lệch so với mã nguồn**. Cần cập nhật cả 2 điểm.

**(4) Ticket riêng cho các nhãn còn lệch 1 ngày (ngoài phạm vi #39736)** — gộp 2 điểm vào 1 ticket (xem [NIT] §4.4): màn **ポイント設定 / SCR-BLP-01** (Dev tự phát hiện khi quét ngang) và dòng **「クーポン適用後の次回決済日」 trong modal 操作履歴** (NEW-16 phát hiện). Cả hai đang hiển thị `expired_date_contract` thô.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ✅ pass (BUG có 3 TC, NEW-1 mô phỏng đúng steps journal #129304) · A.2 ⚠️ RISK (F1/F2 chỉ verify gián tiếp, TC API blocked) · A.3 ⚠️ RISK (thiếu `WHERE` scope) · A.4 ⚠️ RISK (T1 happy-path-only) · A.5 ✅ pass (không ORPHAN, không TC generic) · A.6 ⚠️ xem §3.5
- [x] **B. Chất lượng từng TC** — B.1 ✅ pass (title có keyword rõ, precondition dựng được, expected có **giá trị ngày cụ thể** chứ không "hiển thị đúng") · B.2 ⚠️ NEW-5 và NEW-8 gộp 2–3 bộ dữ liệu trong 1 TC — **chấp nhận được**, Studio đã ghi lý do ở `note` (cùng root cause / cùng nhánh công thức) · B.3 ✅ pass · B.4 ✅ pass (dữ liệu ngày cụ thể, không dùng `test`/`abc`)
- [ ] **C. Chất lượng bộ TC tổng thể** — ❌ **fail**: tỉ lệ loại case 65/12/23 lệch (thiếu `Abnormal`); không có TC role/permission; không có TC multi-device/browser (GAP-7); không trùng lặp TC ✅
- [ ] **D. Spec alignment** — ❌ **fail**: thiếu `02-spec-reference.md`; phát hiện **mâu thuẫn spec** (§6); cột `Trạng thái đánh giá spec` trống 17/17
- [ ] **E. Hành chính** — ❌ **fail**: `TC No.` có 6 mã quan điểm không tồn tại trong checklist; 2 checkbox "Tester verify auto-fill" chưa tick; TC còn ở `status = draft`, task Studio `reviewed = false`; 5 TC blocked có sẵn `Người thực hiện` + `Ngày thực hiện`
- [ ] **F. Base quan điểm test LME**
  - [ ] **F.1 Quan điểm (tầng 1)** — ❌ **fail**: Studio `test_viewpoint_selection = null` → **chưa duyệt tầng 1**, không có dòng ◯/× nào (vi phạm **RULE-03**). Bảng đối chiếu do `/review-tc` tự lập ở dưới.
  - [ ] **F.2 Catalog (tầng 2)** — **A** input: × có lý do (fix không chạm validation) · **B** UI: ❌ chưa rà `UIC-*` cho modal (GAP-7) · **C** bản đồ LME: khối `MAP-PLAN` × có lý do (không đụng giới hạn gói), khối `MAP-CANCEL` × có lý do (không đụng hủy hợp đồng) · **D/D2** môi trường: ❌ **fail** — không TC nào trên production dù chạm bill tiền + asset (GAP-1) · **E** media: × không áp dụng
  - [ ] **F.3 RULE quy trình** — RULE-01 ❌ (`FUNC-DATE-001` thiếu Normal + Abnormal) · RULE-02 ❌ (Evidence trống, không ghi loại evidence) · RULE-03 ❌ (không có bảng duyệt quan điểm) · RULE-06 ❌ (không đi tới ngày trừ tiền thật) · RULE-07 ✅ **pass** (NEW-2 + NEW-16 verify đủ DB + màn hình + thông báo) — nhưng thiếu vế `WHERE` 2 tài khoản · RULE-08 ❌ (0 TC production) · RULE-09 ⚠️ (`COMPAT-LEGACY-001` có TC nhưng blocked) · RULE-12 ✅ pass (regression bám danh sách Dev cung cấp ở mục 3)

### F.1 — Bảng quan điểm đối chiếu

> `⛔` = TC đó đang blocked. Ưu tiên lấy từ [checklist-lme.md](../../framework/checklist-lme.md).

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ — mọi chức năng, luôn bắt buộc | NEW-1, NEW-2 (Normal) · NEW-5 (Abnormal) · NEW-6/7/8/9 (Boundary) | **OK** |
| `FUNC-DATE-001` | **Cao** | ◯ — fix là bài toán tính/so sánh ngày | NEW-6, NEW-7, NEW-8, NEW-9, ⛔NEW-14 — **toàn bộ là `Boundary`** | **RISK** → [MAJOR] **RULE-01** (thiếu Normal + Abnormal, không ghi lý do) + [MAJOR] **GAP timezone** |
| `FUNC-SEQ-001` | Trung bình | ◯ — áp coupon 2 lần liên tiếp, có reload | NEW-4 (Normal) | **OK** |
| `FUNC-002` / `FUNC-003` / `FUNC-004` | Cao / TB / Cao | **×** — logic validate mã coupon **không bị chạm code**; NEW-5 chỉ cần khẳng định field mới không rò ra nhánh lỗi | NEW-5, ⛔NEW-13 | **×** có lý do (tránh AP-5 over-coverage) |
| `CONC-001` | Cao | **×** — luồng ghi (apply) không bị chạm code | — | **×** có lý do → [NIT] §4.4 |
| `DATA-001` | Cao | ◯ — ngày hiển thị ở nhiều nơi | NEW-3, NEW-15, NEW-16 | **OK** |
| `DATA-DB-001` | **Cao** | ◯ — luồng có **UPDATE** `bot_contracts` + `bots` | NEW-2, ⛔NEW-11 (chỉ 1 tài khoản) | **GAP** (vế `WHERE` 2 tài khoản) → [MAJOR] |
| `DATA-AUDIT-001` | Cao | ◯ — đổi trạng thái **hợp đồng** | NEW-16 | **OK** (× các nguồn app/job có lý do: coupon chỉ áp từ web) |
| `DATA-CACHE-001` | TB → Cao | ◯ — release đổi JS/asset | NEW-17 | **OK** (nhưng chỉ staging → gộp vào GAP-1) |
| `DATA-COUNT-001` | Cao | **×** — không có số đếm / tỷ lệ / tổng hợp nào | — | **×** có lý do |
| `OUT-TRUTH-001` | **Cao** | ◯ — thao tác lưu **có thông báo kết quả** | NEW-2, NEW-3 (Normal) · NEW-5 (Abnormal, đang gắn mã khác) | **RISK** → [MINOR] remap NEW-5 |
| `OUT-PREVIEW-001` | Cao | **×** — modal xác nhận **không** phải preview/test-send | — | **×** có lý do |
| `UI-001` | TB | ◯ — có UI modal | NEW-15 (một phần) | **RISK** — chưa test 1366×768 → gộp `TC-UI002-01` |
| `UI-002` | **TB** | ◯ — UI user-facing, **có input ngày giờ** | — | **GAP** → [MAJOR] |
| `UI-003` | TB → Cao | ◯ — rủi ro **false success** (báo thành công nhưng ngày sai) | NEW-15 (canh `Invalid date` + lỗi JS) | **RISK** → bổ sung `TC-FUNCDATE001-07` |
| `PAY-STATE-001` | **Cao** | ◯ — đổi trạng thái **hợp đồng** | NEW-2, NEW-16 (chỉ nơi thứ 1/3) | **RISK** → [MAJOR] ORACLE + [MAJOR] AP-3 |
| `PAY-AMOUNT-001` | Cao | **×** — coupon chỉ gia hạn ngày, Dev xác nhận **không** đổi số tiền | — | **×** có lý do |
| `PAY-BATCH-001` / `PAY-PLAN-001` / `PAY-LIMIT-001` | Cao | **×** — không chạm batch / đổi gói / giới hạn gói | — | **×** có lý do |
| `STATE-001` | Cao | ◯ — modal 2 bước (check → apply), chỉ bước 2 ghi dữ liệu | NEW-1 (xác nhận bước 1 **chưa** ghi dữ liệu) | **OK** |
| `STATE-CLEAN-001` | Cao | **×** — không chạm hủy hợp đồng / ngắt kết nối | — | **×** có lý do |
| `REG-SHARED-001` | **Cao** | ◯ — `detail.js` là JS **dùng chung toàn màn** chi tiết hợp đồng | NEW-15 | **OK** — nhưng thiếu chiều **brand** → [MINOR] |
| `REG-RUN-001` | Cao | **×** — fix display-only, không đổi job / dữ liệu đang chạy dở | — | **×** có lý do |
| `ENV-003` | **Cao** | ◯ — chạm **bill tiền** + **asset/domain** | — (17/17 TC ở staging) | **GAP** → **[BLOCKER]** |
| `JOB-001` | Cao | **×** — không thêm/sửa job nền, không gọi API bên thứ 3 theo lô | — | **×** có lý do |
| `DEPLOY-ASSET-001` | **Cao** | ◯ — release sửa file **JS**, file nằm trong **luồng thanh toán** (Cao tuyệt đối) | NEW-17 (chỉ `Abnormal`) | **RISK** → gộp GAP-1 + [MINOR] RULE-01 |
| `DEPLOY-LIVE-001` | **Cao** | ◯ — **đổi payload API response** | — | **GAP** → **[BLOCKER]** |
| `COMPAT-LEGACY-001` | **Cao** | ◯ — response tồn tại **song song** field cũ + field mới | ⛔NEW-12 (**blocked**) | **RISK** → [MAJOR] (chạy lại sau khi gỡ blocked) |
| `SEC-001` | **Cao** | ◯ — API chạm dữ liệu hợp đồng của tổ chức | ⛔NEW-13 (chỉ ID **không tồn tại**) | **GAP** (cross-tenant) → [MAJOR] |
| `SEC-002` | Cao | ◯ — quét rò thông tin ở màn lỗi | ⛔NEW-13 (một phần: "không phản hồi nào chứa field ngày") | **RISK** — chấp nhận, gộp vào rerun ⛔NEW-13 |
| `LIST-001` / `BULK-001` / `MSG-*` / `MEDIA-*` / `FRIEND-*` / `INTG-*` / `PERM-*` / `PERF-*` | — | **×** — task không chạm danh sách / gửi tin / media / friend info / tích hợp ngoài / phân quyền / hiệu năng | — | **×** có lý do |
| §4 checklist-lme (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) | — | **Không áp dụng** | — | **RULE-11** — không dùng để flag, đã kiểm task không chạm |

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

> ⚠️ **Draft do `/review-tc` sinh — Leader verify trước khi gửi member.** Đặc biệt cần Leader quyết 3 điểm: (1) hạ hay giữ BLOCKER cho `DEPLOY-LIVE-001` (§4.1 GAP-3); (2) giữ hay hạ MAJOR cho `DATA-DB-001` (§4.2 GAP-6) — luồng ghi không bị chạm code; (3) `TC-ENV003-01` + `TC-PAYSTATE001-01` chạy trên **hợp đồng thật ở production** — cần Leader chỉ định bot nội bộ và duyệt trước.
