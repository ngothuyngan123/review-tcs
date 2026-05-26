# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #36442 — [15-05-2026][Admin] Master admin — sai lệch 1円 trang đại lý vs CSV (32 user, dư 32 yên) |
| Reviewer (Leader) | `<điền tên Leader>` |
| Tester được review | CucDTK (assignee phần dưới của bộ TC — Sheet "Improve admin v2.0" row 531+) + (chưa rõ assignee row 521-530) |
| Ngày review | 2026-05-22 |
| Version TCs | v1 (raw từ Sheet "Improve admin v2.0", range A521:J538) |
| Vòng review | Round 1 (draft AI — Leader verify) |
| Spec reference | Không có `02-spec-reference.md` → fallback dùng `templates/LME-SYSTEM-SPEC.md` tổng. **LME-SYSTEM-SPEC không có section riêng cho 代理店報酬 / 振込用CSV** — cần Dev hoặc PM cung cấp spec riêng nếu có. |

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC hiện cover được flow KH per-user (¥X.5/¥X.6/¥X.8 → round up khớp GUI vs CSV), nhưng **bỏ lọt 2 vector trọng yếu**: (1) halfway-DOWN boundary `.4/.5-on-even` chưa verify rule round chính xác (PHP `round()` mode mặc định `PHP_ROUND_HALF_UP` ≠ JS `Math.round()` round-to-even ở `.5` → có thể vẫn lệch ở số khác); (2) **aggregate sum** N-user (KH báo `32 user × 1円 = 32円` ở tổng) — TCs chỉ verify per-user, chưa có TC verify tổng CSV = tổng GUI = tổng đã chuyển. Cộng thêm dev-impact mục 3 trống (AP-6) + scope 商品決済 vs 代理店報酬 chưa rõ (BLOCKER tiềm ẩn) → block đến khi fix.

---

## 2. Tóm tắt cho member

Bộ TC làm tốt phần verify **per-user halfway-UP** (4 TC với amount .5/.6/.8 → cả GUI và CSV đều round lên) + cover CL5 double-download + cover format CSV với 7 field info đại lý — đủ độ rộng cho regression export CSV. Tuy nhiên **3 chỗ cần bổ sung quan trọng**: (1) test halfway-DOWN (.4) và halfway-even (.5 với phần nguyên chẵn) để pin down rule round chính xác — nếu không, bug 1円 dễ tái phát ở số khác; (2) test **aggregate sum** với ≥ 32 user có phần lẻ — đây là chính xác case KH gặp (tổng 32円 dư) — không có TC này thì regression sẽ không catch nếu fix chỉ chữa per-user mà không chữa tổng; (3) clarify với Dev xem `商品決済` ở mục 4.3 dev-impact có phải gõ nhầm `代理店報酬` không — nếu là 2 màn khác hẳn thì 0 TC nào cover 商品決済. Sau khi bổ sung 5-7 TC mới (xem §5), re-submit để review round 2.

---

## 3. Coverage Matrix

> Index TC: dùng row số trong Sheet "Improve admin v2.0" (521-538) làm ID. Row 521-522 là **heading impact + reference SQL** (không phải TC) → excluded. 16 TC thực tế: row 523-538.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| **BUG** (root cause: lệch 1円 GUI vs CSV) | Fix | — | row 523, 524, 525, 526, 537 | 5 | **RISK** — chỉ verify per-user, thiếu aggregate sum test (case KH thực tế = tổng 32 user) |
| **F1** — FE render amount (`affiliater.js`) | Function | Direct | row 523-526, 527, 528, 537 (đều có "check ở màn hình admin số amount đã được làm tròn") | 7 | **RISK** — thiếu halfway-DOWN boundary (.4) + thiếu test rule round-half-even vs half-up |
| **F2** — `exportCsvV2` (CSV BE) | Function | Direct | row 523-526, 528, 530, 531, 532-538 (đều "check down load csv ...") | 13 | OK breadth — nhưng cùng gap halfway-DOWN/even |
| **D** (data) | Data | — | (Dev confirm "k có" data update) | — | N/A — KHÔNG có data impact theo dev (raw `payment_detail_aff.amount` giữ nguyên decimal) |
| **T1** — 商品決済 (Dev viết — verify scope) | Feature | Medium | **0** (không TC nào title đề cập "商品決済") | 0 | **GAP (BLOCKER tiềm ẩn)** — nếu Dev viết nhầm = 代理店報酬 → housekeeping; nếu khác hẳn → 0 TC cover |
| **T2** — Export CSV 振込用CSV | Feature | High | row 527, 530, 531, 532-538 | 11 | OK |
| **T3** — 代理店報酬 màn admin (AI suy luận) | Feature | High | row 523-526, 527, 529 | 6 | RISK — happy path only, không test edge state (kỳ rỗng, kỳ chỉ 1 user, kỳ có refund) |
| **T4** — Tổng 振込金額 cuối trang (AI suy luận, = case KH 32 user) | Feature | High | row 527 (tổng số tiền) + 537 (cell 振込金額) | 2 | **GAP** — không có TC verify aggregate khi có N user (≥ 2, lý tưởng ≥ 32) có phần lẻ |

### ORPHAN TCs

Không có ORPHAN rõ rệt. Các TC ban đầu nghi orphan đều map được:
- row 532-536 (代理店登録名, 銀行名, 支店名, 口座番号, 口座名義) → regression T2 (CSV format intact sau fix)
- row 538 (インボイス登録) → regression T2
- row 529 (register affiliate) → regression T3 (màn list display)
- row 528 (edit amount) → F1 re-render + F2 reflect new amount

| TC ID | Title | Cover impact nào? | Hành động đề xuất |
|---|---|---|---|
| (không có) | | | |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (mục 2 dev-impact) | **Specific logic change** (đổi quy tắc làm tròn): `floor` ở FE → `round-to-nearest` ở cả FE và BE. KHÔNG phải generic catch / validation / race-condition / cache / migration / soft-delete. |
| **Trigger space cần cover** | Halfway boundary phải cover **đủ 4 hướng**: (a) `X.4` → round DOWN; (b) `X.6/X.7/X.8/X.9` → round UP (✓ đã có TC cho .6 và .8); (c) `X.5 với phần nguyên chẵn` (vd 15556.5) — tùy mode → up hay even; (d) `X.5 với phần nguyên lẻ` (vd 15557.5) ✓ đã có 1 TC. Ngoài ra: amount = 0, amount âm (sub_amount > amount), amount cực lớn (¥10,000,000+). Tổng: **≥ 6 trigger boundary** + **2 trigger edge** (0, âm). |
| **Số trigger TCs hiện cover** | **3/8** — chỉ cover `.5 (X lẻ)`, `.6`, `.8` ở 1 vài amount cố định. Thiếu `.4 DOWN`, `.5 X chẵn`, `0`, `âm`, `cực lớn`. |
| **KH report dạng** | **Có root cause cụ thể** — KH chỉ rõ "lệch 1円 ở 32 user kỳ 2025/04, dư 32 yên" + có file Excel danh sách 32 user. Không phải symptom-only. |
| **Alternative root causes cần verify** | N/A (KH đã rõ root cause). Tuy nhiên cần verify thêm: có **alternative function** (job batch tổng hợp doanh số, page export khác) cũng dùng cùng logic `floor` không → dev mục 3 trống → AP-6 dính. |
| **Anti-patterns dính** | **AP-4** (Commit/PR trống → không verify fix-shape thực tế ở code), **AP-6** (Mục 3 trống), **AP-3** (T3 regression chỉ happy path). KHÔNG dính AP-1 (specific, không generic catch), KHÔNG dính AP-2 (KH có root cause), KHÔNG dính AP-5 (không over-coverage layer downstream). |

> **Adversarial questions** (Leader hỏi Dev trước khi approve):
> 1. PHP `round()` ở `exportCsvV2` đang dùng mode nào? Default `PHP_ROUND_HALF_UP` hay `PHP_ROUND_HALF_EVEN`?
> 2. JS rounding ở `affiliater.js` đang dùng `Math.round()` (half-away-from-zero, `-0.5 → -1`) hay `toFixed()` (banker's rounding ở 1 số browser) hay custom?
> 3. Nếu 2 mode khác nhau → **bug 1円 vẫn xảy ra** ở số `X.5 với X chẵn` (vd ¥15,556.5).
> 4. Có job batch nào (vd job sinh bảng thống kê doanh số tháng, job notification amount cho đại lý) cũng dùng logic làm tròn không?
> 5. 商品決済 ở 4.3 có phải = 代理店報酬 không?

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE — GAP-1** (Halfway-DOWN + half-even boundary chưa verify): TCs chỉ cover 3 trigger (`.5 lẻ`, `.6`, `.8`) → cùng kết quả UP. Nếu PHP `round()` mode # JS `Math.round()` mode ở case `.5 với X chẵn` (vd ¥15,556.5) hoặc `.4` (¥15,556.4 → 15,556 hay 15,557?) → bug 1円 vẫn còn ở số khác. **Đề xuất fix**: thêm ≥ 4 TC (xem §5: TC-NEW-01, TC-NEW-02) verify cả half-DOWN và half-even with X chẵn/lẻ. Dev cũng phải confirm round mode (PHP function nào, JS function nào) bằng PR link.

- **[BLOCKER] GAP-2 — Aggregate sum N user**: Bug thực tế KH gặp là **tổng 32 user lệch 32円**, không phải per-user lệch. TCs hiện không có TC nào verify khi có ≥ 2 user có phần lẻ → tổng admin GUI = tổng CSV download = tổng thực tế chuyển khoản (= sum sau làm tròn). Không có TC này = không catch được nếu fix chỉ chữa display per-user nhưng tổng vẫn tính sai. **Đề xuất fix**: thêm TC-NEW-03 (xem §5) dataset 32 user có phần lẻ.

- **[BLOCKER] GAP-3 — Scope T1 (商品決済) chưa rõ**: Dev mục 4.3 viết "màn hình admin 商品決済" và "export csv 振込用CSV tại màn 商品決済" — nhưng bug context 100% là `代理店報酬`. Nếu 商品決済 là **màn khác hẳn** với 代理店報酬 (vd: màn thanh toán item/event/salon riêng) thì 0 TC nào cover 商品決済. **Đề xuất fix**: hỏi Dev trực tiếp: (a) Có phải gõ nhầm 商品決済 = 代理店報酬? → đổi xuống MAJOR housekeeping. (b) Là 2 màn khác, cùng có CSV cùng logic làm tròn? → thêm bộ TC cover 商品決済 (~ tương đương 11 TC như cover 代理店報酬).

### 4.2 Major (nên fix)

- **[MAJOR] Auto-fill verify chưa tick**: Cả `01-bug-task.md` và `03-dev-impact.md` có field "Auto-filled: 2026-05-22 by /new-task" **nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick** ở cả 2 file. Review hiện đang dựa input chưa được tester kiểm tra → có thể tester còn sót journal / attachment / custom field nào quan trọng. **Đề xuất fix**: tester đọc lại Redmine #36442 (journal #118957 và attachment `振込金額_差異リスト.xlsx`), verify nội dung 01 + 03 khớp, tick 2 checkbox, rồi mới merge review report này.

- **[MAJOR] AP-6 — Mục 3 dev-impact trống**: Dev không list function caller đã check. Có thể có job batch (vd job sinh bảng thống kê doanh số tháng, job notification amount cho đại lý qua mail/LINE) cũng dùng cùng logic `floor` cũ → nếu không fix nốt thì user đại lý nhận notification amount # CSV chuyển khoản. **Đề xuất fix**: yêu cầu Dev list rõ ràng các function caller / job batch dùng cùng amount logic. Sau khi có list → review lại có cần thêm TC regression không.

- **[MAJOR] AP-4 — Commit/PR trống**: `03-dev-impact.md` field "Commit / Pull Request" để trống. Không có cách verify fix-shape thực tế ở code: rounding mode (PHP `round()` mode? `floor() + 0.5`? `intval()`?), có dùng config chung hay hardcode 2 nơi. **Đề xuất fix**: yêu cầu Dev cung cấp PR link + chỉ rõ 2 function (`affiliater.js` line bao nhiêu, `exportCsvV2` line bao nhiêu) đã đổi như thế nào.

- **[MAJOR] FIX-SHAPE — Consistency check thiếu**: TCs verify "GUI và CSV cùng round up" cho 1 vài input, nhưng chưa có TC verify với **dataset realistic** (kỳ có refund — `status_refund = 0` filter trong SQL Dev paste row 522, kỳ có user vừa hết hợp đồng `flag_display`, kỳ có `parent_month` mix). Source query Dev paste ở row 522 phức tạp (4 OR điều kiện) → có thể tồn tại case mà rounding ăn vào filter (vd: round xuống = 0 → vô hình trong GUI vs CSV vẫn hiện). **Đề xuất fix**: thêm TC với dataset gồm user `status_refund=1` (đã refund), user `parent_month=1`, user `remain_day < 365 vs ≥ 365` để đảm bảo fix không ảnh hưởng filter.

- **[MAJOR] AP-3 — Happy-path-only regression T3**: T3 (代理店報酬 màn admin) chỉ có 6 TC (4 verify rounding + 1 register affiliate + 1 tổng số tiền). Không có TC test edge state: (a) kỳ không có user nào (empty list), (b) kỳ chỉ 1 user, (c) kỳ có user mà tất cả amount = 0 (free contract), (d) kỳ có user với `sub_amount > amount` (negative reward). **Đề xuất fix**: thêm TC-NEW-04 + TC-NEW-05 (xem §5).

- **[MAJOR] CL12 — Max data**: Bug có dataset thực tế 32 user. Không có TC test với dataset lớn (≥ 100 user, ≥ 1000 user). Có khả năng performance hoặc memory issue ở CSV export với N rất lớn → nên có 1 TC smoke với N = 1000. **Đề xuất fix**: thêm TC-NEW-06.

- **[MAJOR] F.3 §C.1 Bill tiền (LME checklist)**: Đây là feature về tiền hoa hồng đại lý — liên quan loose tới C.1. Tuy nhiên bug không ở payment gateway → không bắt buộc cover 10 error scenarios payment gateway (card_declined, insufficient_funds, ...). **Đề xuất**: Leader confirm scope C.1 áp dụng đến đâu cho task này. Nếu chỉ "Bill tiền/display" → đã cover; nếu cần "Bill tiền/error scenarios" → out of scope task này, ghi rõ trong report.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Title TC generic**: row 531 "check format", row 532 "check data khi down load xuống" — không có keyword đủ rõ để map impact. Đề nghị member rename: "Verify CSV format header rows khớp template Sheet [link]" / "Verify CSV row data cho field 代理店登録名 khớp DB affiliate_info.name".

- **[MINOR] Merged-cell context (row 524-526, 533-538)**: Các TC này không atomic, chỉ điền cột con Sub2/Sub3 và inherit Sub1 từ row 523/531/532. Khi tester chạy độc lập (vd Cucumber assign chỉ row 535 cho 1 tester khác) → có thể không hiểu phải làm gì. **Đề xuất fix**: inline full title vào mỗi row, hoặc thêm Precondition rõ "Tiếp theo TC row 523: ...".

- **[MINOR] Row 532-536 thiếu Status (col I)**: Source data không có "Not test" ở 5 row này, trong khi các row khác có. Có thể là chưa fill (vô tình) hoặc merge với row 537. Verify với Cúc trước khi run.

- **[MINOR] CL2 — Reload sau save không có TC**: Sau khi `check khi edit số amount` (row 528) thì có TC reload page verify amount mới persist không? Hiện không có. Đề xuất tách row 528 thành 2 TC: edit + reload.

- **[MINOR] CL1 — Staff account access**: Trang `代理店報酬` là admin page → staff có quyền view không? Có quyền export CSV không? Hiện không có TC. Đề xuất thêm TC-NEW-08.

- **[MINOR] CL15 — Phân trang scroll**: Nếu màn 代理店報酬 có pagination (kỳ có nhiều user) → next page có scroll-to-top không? Verify có pagination không trước.

- **[MINOR] C.8 Sort**: Nếu màn 代理店報酬 có sort theo cột (vd sort theo 振込金額 giảm dần) → sau khi sort thì rounding có còn đúng không? Hiện không có TC sort.

- **[MINOR] Field 01 placeholder**: `Module / Màn hình` và `Môi trường phát hiện` ở file 01 đang chứa `<chưa rõ — tester fill>` — tester fill vào trước khi finalize.

- **[MINOR] Non-function — Compatibility**: Bug có 2 đầu (JS FE + PHP BE). JS rounding có thể khác giữa Chrome / Safari / Firefox / Edge (đặc biệt với amount cực lớn vượt safe integer). Hiện không có TC test cross-browser. Đề xuất thêm TC-NEW-07.

### 4.4 Nit (gợi ý)

- **[NIT]** Row 530 (double download) có thể tách 2 case: (a) double-click rapid liên tục cùng button (CL5); (b) mở 2 tab cùng kỳ, click download cùng lúc — case này dễ catch race condition hơn.

- **[NIT]** Row 531 reference Sheet ngoài (`docs.google.com/.../edit?gid=0#gid=0` của `1j0yIzyveUMvf...`) như là format template — Sheet đó có thể bị thay đổi → đề xuất snapshot format vào trong file 04 (hoặc reference commit hash của Sheet template).

- **[NIT]** Có thể thêm TC verify CSV với **encoding** đúng (UTF-8 BOM hay Shift-JIS — JP CSV thường yêu cầu Shift-JIS để mở bằng Excel mặc định Nhật) — Bug fix không chạm encoding nhưng dễ bị ảnh hưởng khi chạm CSV controller.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. Đặt TC ID từ `TC-NEW-01` đến `TC-NEW-09`.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Verify halfway-DOWN boundary: amount = ¥X.4 thì làm tròn xuống ở cả GUI và CSV | Account admin, có ≥ 1 affiliate user kỳ test với raw amount = `15556.4` (rate/sub_amount thỏa) | 1. Vào màn 代理店報酬, chọn kỳ test.<br>2. Note amount user đó ở GUI.<br>3. Download `振込用CSV`.<br>4. Mở CSV, so sánh amount với GUI. | GUI hiển thị `¥15,556` (round DOWN, KHÔNG là ¥15,557).<br>CSV cũng hiển thị `¥15,556`.<br>2 đầu bằng nhau. | High | Boundary | BUG, F1, F2 |
| TC-NEW-02 | Verify halfway-EVEN: amount = ¥X.5 với X chẵn vs X lẻ (pin down rule round mode) | Account admin, có 2 affiliate user kỳ test: user A raw amount = `15556.5` (X = 15556 chẵn), user B raw amount = `15557.5` (X = 15557 lẻ) | 1. Vào màn 代理店報酬.<br>2. Note amount user A và user B ở GUI.<br>3. Download CSV.<br>4. Đối chiếu amount user A và user B giữa GUI vs CSV. | **Rule cần xác định trước với Dev**:<br>- Nếu `PHP_ROUND_HALF_UP`: A=¥15,557, B=¥15,558 (cả 2 round UP).<br>- Nếu `PHP_ROUND_HALF_EVEN` (banker's): A=¥15,556 (về chẵn), B=¥15,558 (về chẵn).<br>**Bắt buộc**: GUI và CSV của cùng 1 user **luôn bằng nhau**, không phụ thuộc rule. | High | Boundary | BUG, F1, F2 |
| TC-NEW-03 | Verify aggregate sum: 32 user cùng có phần lẻ → tổng GUI = tổng CSV = tổng chuyển khoản thực tế (reproduce KH case kỳ 2025/04) | Account admin, kỳ test có **đúng 32 user** với raw amount có phần lẻ (mix các phần lẻ .5/.6/.7/.8/.9) | 1. Vào màn 代理店報酬, chọn kỳ test.<br>2. Note tổng số tiền 振込金額 hiển thị cuối trang GUI.<br>3. Note từng amount của 32 user.<br>4. Download `振込用CSV`.<br>5. Tính tổng cột amount trong CSV.<br>6. So sánh: tổng GUI vs tổng CSV vs sum của 32 amount per-user. | Tổng GUI = tổng CSV = sum(32 amount per-user sau làm tròn).<br>**KHÔNG có chênh lệch nào** (vd dư 32円 như bug gốc).<br>Tổng = `sum(round(raw_amount_i))` với `i = 1..32`, không phải `round(sum(raw_amount))`. | **Critical** | Positive (reproduce KH) | BUG, T4, F1, F2 |
| TC-NEW-04 | Verify edge state: kỳ có user với amount = 0 (free contract / chưa phát sinh) | Account admin, kỳ test có ≥ 1 user `payment_detail_aff` với raw amount = 0 | 1. Vào màn 代理店報酬, chọn kỳ test.<br>2. Note hiển thị user đó ở GUI.<br>3. Download CSV.<br>4. Verify user đó có xuất hiện trong CSV không + amount value. | GUI hiển thị `¥0` (không phải `¥-0`, không phải blank, không phải NaN).<br>CSV cũng hiển thị `0` ở cột amount user đó.<br>Tổng cuối trang không bị ảnh hưởng. | Medium | Boundary / Edge | T3, F1, F2 |
| TC-NEW-05 | Verify edge state: kỳ có user với `sub_amount > amount` (negative reward / refund offset) | Account admin, kỳ test có ≥ 1 user với `payment_detail_aff` có `sub_amount > amount` (vd amount=1000, sub_amount=1500, rate=10 → raw_reward = 1000*10/100 - 1500 = -1400) | 1. Vào màn 代理店報酬, chọn kỳ test.<br>2. Note amount user negative ở GUI.<br>3. Download CSV.<br>4. So sánh amount user đó giữa GUI vs CSV. | GUI và CSV hiển thị **cùng giá trị âm** (vd `-¥1,400` ở cả 2).<br>Rounding ở số âm consistent (vd `-1400.5 → -1400` hay `-1401` tùy mode, nhưng 2 đầu phải bằng nhau).<br>Tổng cuối trang trừ đúng. | Medium | Boundary / Edge | T3, F1, F2 |
| TC-NEW-06 | Verify performance + correctness: kỳ có ≥ 1000 user (smoke max data per CL12) | Account admin, kỳ test có ≥ 1000 user `payment_detail_aff` (có thể seed bằng SQL hoặc dùng kỳ thực tế đông user nhất) | 1. Vào màn 代理店報酬, chọn kỳ.<br>2. Đợi GUI load xong (note thời gian).<br>3. Note tổng số tiền cuối trang.<br>4. Download CSV.<br>5. Note thời gian download xong + size file.<br>6. So sánh tổng GUI vs tổng CSV vs row count CSV. | GUI load < 10s, không crash.<br>CSV download < 30s, file mở được trong Excel/LibreOffice.<br>Row count CSV = số user ở GUI.<br>Tổng GUI = tổng CSV (không lệch). | Medium | Boundary (max) / Performance smoke | F1, F2, T3, T4 |
| TC-NEW-07 | Verify cross-browser rounding consistency (FE Math.round không khác giữa browser) | Account admin, kỳ test có 1 user raw amount = 15557.5, mở app trên Chrome / Safari / Firefox / Edge | 1. Trên Chrome: vào 代理店報酬 → note amount.<br>2. Trên Safari: làm lại bước 1.<br>3. Trên Firefox: làm lại bước 1.<br>4. Trên Edge: làm lại bước 1. | Cả 4 browser hiển thị **cùng 1 giá trị** ở GUI (`¥15,558` nếu rule = half-up, hoặc `¥15,558` nếu rule = half-even with 15557 lẻ).<br>Không có sự khác biệt giữa browser. | Medium | Compatibility | F1 |
| TC-NEW-08 | Verify staff account access — staff có quyền view 代理店報酬 + download CSV không? | Account staff (chưa được phân quyền) + account staff (đã phân quyền cụ thể cho màn 代理店報酬 nếu có config) | 1. Login bằng staff chưa phân quyền → vào URL `/admin/<path>/代理店報酬`.<br>2. Verify redirect / từ chối.<br>3. Login bằng staff đã phân quyền → vào màn, thử download CSV.<br>4. So sánh với account admin chính. | Staff chưa phân quyền: redirect về trang phân quyền hoặc 403.<br>Staff đã phân quyền: thao tác giống admin chính, CSV download cùng nội dung. | Medium | Negative / Security | F.1 §A.1 CL1, F.1 §A.2 Security |
| TC-NEW-09 | (Verification task — KHÔNG phải TC test) Clarify với Dev: 商品決済 ở 4.3 dev-impact = 代理店報酬 hay là màn khác | — | 1. Hỏi Dev trực tiếp.<br>2. Update file 03 mục 4.3 nếu là gõ nhầm.<br>3. Nếu là màn khác → spawn task review TC riêng cho 商品決済. | Có 1 trong 2 kết luận rõ ràng:<br>(a) "Dev gõ nhầm, 商品決済 ≡ 代理店報酬" → update 03, không cần TC mới.<br>(b) "Dev nói thật, 商品決済 là /admin/<path khác>" → tạo folder review riêng + bộ TC tương đương 16 TC hiện có. | — | — | — |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] Cần update spec — chi tiết:
  - **Section**: Spec rounding cho 報酬額 (tiền hoa hồng đại lý) — hiện không có spec riêng cho rule round (half-up vs half-even). LME-SYSTEM-SPEC.md tổng không cover màn 代理店報酬.
  - **Nội dung cần update**: Ghi rõ rule round dùng ở display 報酬額 và export 振込用CSV — kèm rule cho edge case (`.5` X chẵn vs lẻ, amount âm, amount = 0).
  - **Người chịu trách nhiệm update**: Dev fix + PM xác nhận với KH (do KH đã chuyển dư 32円 nên decision business — có cần refund đại lý hay không).

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — chạy, kết quả ở §3 + §3.5
  - A.1 Bug root cause: ✓ (TCs reproduce per-user, **RISK** aggregate)
  - A.2 Function impact: ✓ F1/F2 có TC, **RISK** boundary
  - A.3 Data impact: N/A (Dev confirm "k có")
  - A.4 Feature impact: **GAP** T1, **GAP** T4
  - A.5 Gap & orphan: không orphan, có gap
  - A.6 Fix-shape adversarial: **BLOCKER** halfway-DOWN/even
- [x] **B. Chất lượng từng TC**
  - B.1 Rõ ràng: MINOR (title generic ở row 531-532, merged context)
  - B.2 Atomic: MINOR (merged cell rows không atomic)
  - B.3 Độc lập: MINOR (TC con phụ thuộc parent title)
  - B.4 Realistic: ✓ (data sample dùng amount thực)
- [x] **C. Chất lượng bộ TC tổng thể**
  - Tỷ lệ Positive : Negative : Boundary : Regression — hiện ~ 70% Positive + 10% Boundary + 20% Regression, thiếu Negative → MAJOR
  - Trùng lặp: không
  - Priority phân bổ: không có cột Priority trong source → MINOR (mặc định không gán)
  - Role/permission: KHÔNG có TC staff → MINOR
  - Multi-device/responsive: KHÔNG có → MINOR (đề xuất TC-NEW-07)
  - i18n: amount format JP `¥X,XXX` (✓ có), nhưng không test EN/VN format → N/A (LME tool chính là JP)
- [x] **D. Spec alignment** — không có spec riêng, fallback LME-SYSTEM-SPEC tổng. §6 đề xuất update spec.
- [x] **E. Hành chính** — TC IDs dùng row số source Sheet (không có format chuẩn LME), file 04 lưu đúng folder, Tester chưa ký tên trong file 04.
- [x] **F. Base checklist LME** — kết quả:
  - **F.1 Checklist web**:
    - A.1 Function checklist:
      - CL5 (double click): ✓ row 530
      - CL10 (update impact): ✓ row 528 (edit)
      - CL11 (CRUD đúng account): MINOR — không test multi-account, multi-affiliate
      - CL12 (max data): **MAJOR** không có TC ≥ 100 user → TC-NEW-06
      - CL1 (staff account): **MINOR** không có TC → TC-NEW-08
      - CL2 (reload sau save): **MINOR** không có
      - CL15 (phân trang scroll): MINOR (verify màn có pagination không)
      - CL9 (search JP): N/A nếu màn không có search
    - A.2 Non-function:
      - URLs đo lường: N/A
      - Regression: ✓ TC row 532-538 cover regression CSV format
      - Security: **MINOR** thiếu test direct URL access bằng user/bot khác (TC-NEW-08 cover phần này)
      - Compatibility: **MINOR** không có TC Win/Mac, Android/iOS → TC-NEW-07 cover Browser
  - **F.2 Checklist job**:
    - B.1 Job callback: N/A (không chạm)
    - B.2 Job sync Java: N/A (không chạm)
  - **F.3 Các tính năng chung**:
    - C.1 Bill tiền: liên quan loose (đây là display tiền hoa hồng, không phải payment gateway). **MAJOR housekeeping** — Leader confirm scope C.1 áp dụng đến đâu.
    - C.2-C.7: N/A
    - C.8 Sort: **MINOR** (verify màn có sort không, nếu có thì cần TC sort + verify rounding sau sort)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!-- AI-DRAFT — Leader cần verify trước khi gửi member. AI generate dựa trên 3 input file: 01-bug-task.md, 03-dev-impact.md, 04-tc-list.md (range A521:J538 Sheet "Improve admin v2.0") tại thời điểm 2026-05-22. -->
