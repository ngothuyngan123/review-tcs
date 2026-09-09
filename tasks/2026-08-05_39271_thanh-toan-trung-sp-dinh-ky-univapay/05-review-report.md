# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39271 — [29712] [OEM] Thanh toán trùng sản phẩm định kỳ「マナフレンズ」` |
| Reviewer (Leader) | NganNT |
| Tester được review | thanhntp (một số case ghi `AI (thanhntp)`) |
| Ngày review | 2026-08-05 |
| Version TCs | v1 — nguồn `39271.xlsx` sheet `Test case`, 34 case |
| Vòng review | Round 1 |

> **Input đã đọc**: `01-bug-task.md` ✓ · `02-spec-reference.md` ✗ (không có) · `03-dev-impact.md` ✓ · `04-tc-list.md` ✓ (34 TC).
>
> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng (FA-026 Single Product/Sales, FA-034 Payment System Integration), không có spec riêng cho task này.
>
> **Input thiếu / lưu ý nguồn**:
> - `04-tc-list.md` **KHÔNG dùng 16 cột canonical** — là bản export từ test-studio (`39271.xlsx`). Thiếu hẳn 2 cột bắt buộc: `Evidence thực tế` và `Trạng thái đánh giá spec`. Chi tiết ở §4.3.
> - Bộ TC này **đã chạy xong** (31 pass / 3 skip) trước khi review — nên review này vừa soi coverage, vừa soi **tính hợp lệ của kết quả đã chấm**.

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC có chất lượng kỹ thuật cao ở phần verify *logic của guard* (đối chứng âm và biên trạng thái phủ rất kín), nhưng **3 case bị skip lại đúng là 3 case rủi ro cao nhất** (đối soát cổng thật, gói kẹt vĩnh viễn, gói đã hủy), **chưa có TC nào loại trừ root cause thay thế** mà chính Dev đã gỡ khỏi branch, và **chưa có TC nào chạy guard trên dữ liệu gói định kỳ đời cũ / đang treo lúc release** — rủi ro chặn nhầm khách hợp lệ.

---

## 2. Tóm tắt cho member

Bộ TC này viết **rất chắc ở phần chứng minh guard không chặn nhầm**: 5 case đối chứng âm (khách khác / sản phẩm khác / gói đã hủy / gói đã kết thúc / sản phẩm mua 1 lần) và phủ kín toàn bộ value-space của trạng thái chờ (0/3/4 chặn — 1 và 2 không chặn). Cặp NEW-16 và NEW-20 kiểm **thứ tự** guard trong chuỗi validate là chi tiết rất tinh, nhiều bộ TC không nghĩ ra. NEW-30 chủ động ghi nhận Stripe chưa có guard mà **không** tính là fail cũng là cách xử lý out-of-scope đúng chuẩn.

Vấn đề lớn nhất không nằm ở case đã viết, mà ở **3 case bị skip**: NEW-17 (đối soát cổng UnivaPay thật), NEW-22 (gói kẹt vĩnh viễn), NEW-4 (gói đã hủy). Cả ba đều là case chứng minh *rủi ro do bản fix tạo ra*, nên skip là chỗ nguy hiểm nhất chứ không phải chỗ an toàn nhất. Ngoài ra bộ TC bám sát kịch bản "back rồi bấm mua lại" mà QA tự dựng — trong khi khách chỉ báo đúng 1 dòng "重複決済が発生している", chưa có gì loại trừ khả năng khách bị trừ trùng theo cơ chế khác (job thu tiền trừ lại vào hôm sau).

Cần bổ sung **15 TC** ở §5 và làm rõ 5 câu hỏi cho Dev/Leader ở §6 trước khi chạy lại vòng 2.

---

## 3. Coverage Matrix

> Impact lấy từ `03-dev-impact.md` §4.1/4.2/4.3. TC map bằng suy luận từ Tên case / Tiền điều kiện / Các bước / Kết quả mong đợi.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — màn confirm-order không chặn mua chồng khi giao dịch trước đang chờ | Fix | — | NEW-13, NEW-14, NEW-8, NEW-9, NEW-10, NEW-32, NEW-33, NEW-34 | 8 | **RISK** — cover kịch bản Dev/QA dựng; **chưa loại trừ root cause thay thế** (xem §3.5) |
| **F1** — `SalesManagementV2Controller::paymentCreditCardItemV2Univapay` | Function | **Direct** (file duy nhất sửa) | NEW-1→NEW-6, NEW-8→NEW-16, NEW-18, NEW-19, NEW-20, NEW-27, NEW-28, NEW-29 | 20 | **RISK** — đủ chiều logic, nhưng thiếu concurrency có bằng chứng + thiếu dữ liệu đời cũ |
| **F2** — `confirm-order.js` `nextStep` (alert + bật lại nút mua) | Function | Indirect | NEW-13 | 1 | **RISK** — 1 TC manual, không evidence; chưa verify khách **bấm lại thành công** sau khi guard nhả |
| **F3** — `CycleOrderHistory::createOrderPayment` | Function | Indirect | NEW-11, NEW-26 | 2 | OK |
| **F4** — `HandleSendActionTrialV2::billItemUnivapay` (job thu tiền định kỳ) | Function | Indirect | NEW-24, NEW-25 | 2 | **RISK** — thiếu kịch bản hủy hợp đồng **giữa lúc** job chạy (PAY-BATCH-001) |
| **F5** — `SalesService::getOrderTimeout` / cron `recover:payment_univapay_timeout` | Function | Indirect | NEW-21, NEW-22 *(skip)*, NEW-23 | 3 | **RISK** — case quan trọng nhất (NEW-22) bị skip |
| **D1** — `s_cycle_order_history.status_webhook` (READ only) | Data | — | NEW-8 (0), NEW-9 (3), NEW-10 (4), NEW-18 (1), NEW-19 (2), NEW-27 (static) | 6 | **OK** — phủ kín value-space, điểm mạnh nhất của bộ TC |
| **D2** — `s_cycle_order_history.status_bill` (READ only) | Data | — | NEW-4 *(skip, =3 hủy)*, NEW-5 (=2 kết thúc), NEW-27 (static) | 3 | **RISK** — nhánh "gói đã hủy" bị skip |
| **T1** — FA-026 Single Product / Sales (mua sản phẩm định kỳ qua UnivaPay) | Feature | (Dev không ghi mức) | NEW-1, NEW-5, NEW-6, NEW-7, NEW-11, NEW-13→NEW-16, NEW-20 | 10 | **RISK** — chưa có TC nào trên **production** (RULE-08) |
| **T2** — FA-034 Payment System Integration (cổng UnivaPay ở màn xác nhận đơn) | Feature | (Dev không ghi mức) | NEW-17 *(skip)*, NEW-21→NEW-23, NEW-26, NEW-31 | 6 | **GAP ở phần đối soát cổng thật** — TC prd duy nhất bị skip |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| NEW-33, NEW-34 | Chặn mua lại sau khi redirect URL / màn hình Text | Tiền điều kiện ghi **"Thanh toán thành công"** → `status_webhook = 1`, **nằm ngoài tập chặn {0,3,4}** ⇒ 2 case này KHÔNG verify guard mới mà verify một cơ chế khác (business rule 1 order/sản phẩm). Expected chỉ ghi "không cho phép thanh toán lại", không nêu màn/message nào. | **Giữ nhưng phải sửa**: tách rõ 2 tiền điều kiện (webhook đã về = 1 → cơ chế cũ · webhook chưa về = 0 → guard mới) và ghi rõ message mong đợi cho từng nhánh. Xem `[MAJOR] NEW-33/34` ở §4.2 |
| NEW-24 | Job thu tiền định kỳ vẫn thu tiền bình thường cho gói đã chốt trạng thái | Job **không bị chạm code** ở bản fix hiện tại (1 file controller) | **Giữ** — hợp lệ là regression cho vùng dùng chung `status_webhook`. Không cần remove |

*Không có TC nào lạc chủ đề hoàn toàn.*

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Specific code check / Guard validation** — thêm `if` đọc `s_cycle_order_history` (4 vế: `status_bill=1` + `item_id` + `line_user_id` + `status_webhook ∈ {0,3,4}`) đặt **trước** bước tính tồn kho và trước lời gọi cổng; khớp → return business error. **KHÔNG phải generic catch-all.** |
| **Trigger space cần cover** | (a) 3 giá trị trạng thái chờ `0 / 3 / 4`; (b) 2 giá trị **không** được chặn `1 / 2`; (c) 3 giá trị `status_bill` `1 / 2 / 3`; (d) trục khách hàng; (e) trục sản phẩm; (f) trục loại thanh toán (định kỳ / 1 lần); (g) **dữ liệu đời cũ (trước V1→V2) / đang treo lúc release**; (h) **2 request đồng thời** |
| **Số trigger TCs hiện cover** | **6/8** — (a)✓ NEW-8/9/10 · (b)✓ NEW-18/19 · (c)✓ NEW-4*(skip)*/NEW-5 · (d)✓ NEW-2 · (e)✓ NEW-3 · (f)✓ NEW-6 · **(g)✗ không TC nào** · **(h)△ NEW-15 chạy 1 lần, không evidence** |
| **KH report dạng** | **Symptom-only** — nguyên văn khách: *"継続商品「マナフレンズ」で重複決済が発生している"* (1 dòng). Không mã đơn, không ngày, không ảnh, không số lần trừ. Dev tự ghi ở §7: *"Chưa xác nhận được bằng dữ liệu production rằng khách 「マナフレンズ」 dính đúng trạng thái nào"* |
| **Alternative root causes cần verify** | **RC-1** (nghiêm trọng nhất): trạng thái `authorized` bị coi là THẤT BẠI → hạn gói không dời → **hôm sau job thu tiền trừ lại đúng kỳ đó, lặp tới 3 lần**. Đây là hướng fix Dev **đã GỠ** khỏi branch với lý do "không phải nguyên nhân" nhưng **không kèm bằng chứng phủ định**. · **RC-2**: webhook trùng/gửi lại → tạo 2 lần ghi nhận thu tiền · **RC-3**: cron/job chạy 2 lần do 2 server loadbalance production (`ENV-LB`) · **RC-4**: khách mua từ 2 thiết bị / 2 link khác nhau |
| **Anti-patterns dính** | **AP-2 DÍNH (nặng)** — symptom-only KH report, TCs chỉ cover 1 root cause do QA tự dựng. · AP-1 **không dính** (fix là specific check, không phải generic catch). · AP-3 **dính nhẹ** (T2 regression chỉ happy path, thiếu trạng thái lỗi thật từ cổng). · AP-4 **không dính** — NEW-27/28 đã static-check đúng dòng code (`SalesManagementV2Controller.php:4920-4937`), fix shape đã được xác minh dù thiếu link PR. · AP-5 **không dính** đáng kể. · AP-6 **không dính** — mục 3 có 6 caller |

### Vì sao RC-1 là rủi ro số 1

Hai kịch bản trừ trùng có **hình dạng hoàn toàn khác nhau**:

| | Kịch bản QA dựng (bộ TC đang cover) | RC-1 (không TC nào cover) |
|---|---|---|
| Khoảng cách 2 lần trừ | Vài giây — vài phút | **~1 ngày**, lặp tới 3 lần |
| Hành vi khách | Chủ động bấm Back rồi mua lại | **Không làm gì cả** |
| Nơi phát sinh | Màn confirm-order (đã fix) | Job thu tiền định kỳ + webhook (**đã bị gỡ khỏi branch**) |
| Khớp mô tả khách? | Cần khách thao tác bất thường | Khớp tự nhiên hơn với "重複決済が発生している" |

→ Nếu root cause thật là RC-1 thì **bản fix hiện tại không chữa được bug của khách**, mà chỉ chặn một kịch bản khác. Ticket [#38077](../2026-06-24_38077_univapay-authorized-bill-success/) (24/06) đã công nhận `authorized = thành công` **ở job đối soát bù**, nhưng theo chính note cũ #127877, **2 điểm quyết định của luồng chính vẫn chưa** — và phần sửa đó vừa bị gỡ.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] AP-2 / SYMPTOM-ONLY — GAP-1**: Không có TC nào chứng minh hoặc loại trừ **RC-1** (trạng thái `authorized` bị coi là lỗi → job trừ lại vào hôm sau). Khách chỉ báo 1 dòng, Dev tự thừa nhận chưa xác nhận được bằng dữ liệu production, và hướng fix cho RC-1 đã bị gỡ khỏi branch **không kèm bằng chứng phủ định**. — **Fix**: (1) Hỏi Dev lấy `s_cycle_order_history` + `s_order_history` của khách LOA 「[Hiroko公式]マナカード講師」 sản phẩm 「マナフレンズ」 → xác định **2 lần trừ cách nhau bao lâu** và `status_order` của chúng; (2) bổ sung `TC-PAYSTATE001-01/02` (§5) tái hiện RC-1 end-to-end qua job.

- **[BLOCKER] ENV-003 / RULE-08 + PAY-STATE-001 — GAP-2**: **NEW-17 là TC production duy nhất và bị SKIP**. Task này là **bill tiền** — theo `Catalog D` khối `ENV-PAY` và RULE-08, hạng mục bill tiền **không được kết luận từ staging**. Ngoài ra PAY-STATE-001 yêu cầu sau **mỗi** kịch bản phải đối chiếu **3 nơi** (admin nội bộ / màn user / dashboard cổng) — hiện **không TC nào** làm đủ 3 nơi, và các kịch bản `hủy` / `refund` chưa có TC nào. — **Fix**: bổ sung `TC-ENV003-01`, `TC-PAYSTATE001-03` (§5); NEW-17 phải chuyển từ skip sang chạy thật, hoặc có **phiếu xác nhận không thể verify + phương án giám sát** do Leader ký (đúng phần Evidence của ENV-003).

- **[BLOCKER] CONC-001 — GAP-3**: NEW-15 là TC concurrency duy nhất, chạy **manual 1 lần**, **không có evidence đếm số lần xử lý thực tế** (CONC-001 bắt buộc: *"bằng chứng số lần xử lý thực tế (log/DB/số tin nhận được)"*), và **chính Ghi chú của TC thừa nhận**: *"đoạn chặn đọc dữ liệu trước rồi mới ghi bản ghi gói ở bước sau, giữa hai bước không có khóa, nên hai yêu cầu đến gần như cùng lúc về lý thuyết vẫn có thể cùng lọt"* — đây là TOCTOU. Race condition **không thể kết luận Đạt từ 1 lần chạy**. Thiếu luôn kịch bản (4) của CONC-001: **batch đa luồng chạm giới hạn dùng chung** (job thu tiền định kỳ chạy đúng lúc khách bấm mua). — **Fix**: `TC-CONC001-01/02/03` (§5) — chạy lặp ≥ 20 lần, evidence là `COUNT(*)` từ DB + số giao dịch trên dashboard cổng.

- **[BLOCKER] COMPAT-LEGACY-001 + REG-RUN-001 — GAP-4**: Không TC nào chạy guard trên **gói định kỳ tạo từ trước**. Hai nhánh rủi ro: (a) **dữ liệu đời cũ** — controller/JS/route đều mang hậu tố `V2` (`SalesManagementV2Controller`, `sales/v2/confirm-order.js`, `payment-credit-card-item-v2-univapay`) ⇒ tồn tại gói tạo bởi luồng V1; nếu bản ghi cũ có `status_webhook` = `0` (giá trị mặc định của cột) **và** `status_bill = 1` thì guard sẽ **chặn vĩnh viễn** khách hợp lệ; (b) **REG-RUN-001** — gói đang ở trạng thái chờ **tại đúng thời điểm deploy** sẽ rơi vào tập chặn ngay khi code mới lên. Cả hai đều là quan điểm ưu tiên **Cao**, RULE-09 ghi rõ *"không được đánh × chỉ vì dữ liệu mới chạy ổn"*. — **Fix**: hỏi Dev *"phân bố `status_webhook` của các bản ghi `s_cycle_order_history` tạo trước tháng nào?"* + bổ sung `TC-COMPATLEGACY001-01/02`, `TC-REGRUN001-01` (§5). **Đây là rủi ro nặng hơn bug gốc**: khách không mua được = mất doanh thu + phát sinh khiếu nại mới.

- **[BLOCKER] NEW-22 (skip) — GAP-5**: Case "gói chờ **không có mã giao dịch** thì cron không chốt được trạng thái" bị **skip**, trong khi chính Ghi chú của TC ghi: *"gói giữ nguyên trạng thái chờ mãi và đoạn chặn mới sẽ khóa khách không cho mua lại. **Đây là hệ quả mới do bản sửa tạo ra**"*. Skip đúng case mô tả rủi ro do fix sinh ra là không chấp nhận được — đây cũng là kịch bản khiến "chỉ chặn 15 phút" trở thành "chặn vĩnh viễn". — **Fix**: bắt buộc chạy; `TC-INTGHOOK002-01` (§5) viết lại rõ tiêu chí Đạt/Không đạt thay cho Expected hiện tại đang bỏ ngỏ ("CẦN LEADER XÁC NHẬN").

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE / PAY-STATE-001**: Guard được chèn vào **đúng controller thanh toán**, đứng trước toàn bộ luồng gọi cổng. Không có TC nào chạy **một giao dịch thất bại THẬT từ cổng** (card declined / insufficient funds / 3DS fail / network timeout) sau khi có fix — NEW-19 chỉ **seed** `status = lỗi` vào DB, không đi qua cổng. Theo `checklist-lme.md §3 Phụ lục`, fix chạm payment gateway phải cover ≥ 4 error type + 1 unknown fallback. — **Fix**: chạy ≥ 3 error type bằng test card sandbox UnivaPay, xác nhận message lỗi cũ vẫn đúng và **không bị guard nuốt**.

- **[MAJOR] RULE-02 / §0.2 — kết quả đã chấm không có bằng chứng**: File 04 **không có cột `Evidence thực tế`**, và **31/34 TC đã đánh `pass`** mà không đính kèm bằng chứng nào. RULE-02: *"Chỉ tick Đạt khi đã đính kèm đúng loại bằng chứng… Không chấp nhận 'đã xem, OK'"*; §0.2: *"Vi phạm RULE → kết quả test **không được nghiệm thu**, dù quan điểm đã tick đủ"*. — **Fix**: bổ sung cột Evidence, đính kèm tối thiểu cho các TC ưu tiên Cao: NEW-7, NEW-11, NEW-13, NEW-15, NEW-21, NEW-25, NEW-26.

- **[MAJOR] Chấm `pass` khi Expected chưa xác định**: NEW-15 và NEW-29 có Kết quả mong đợi ghi *"CẦN DEV/LEADER KẾT LUẬN"* / *"CẦN LEADER XÁC NHẬN"* nhưng vẫn được đánh **pass**. Không thể kết luận Đạt khi tiêu chí Đạt chưa tồn tại. — **Fix**: đổi về `Chưa test` (hoặc `Pending`), đưa 2 câu hỏi vào §6, chấm lại sau khi Leader chốt.

- **[MAJOR] Business rule không có nguồn**: NEW-18 và NEW-21 khẳng định *"Khách hàng chỉ được sở hữu 01 order của cùng sản phẩm tại một thời điểm theo business rule"* và *"sẽ hiện màn thông báo lỗi"* — quy tắc này **không có trong `03-dev-impact.md`, không có trong `01-bug-task.md`, không có spec reference**. Đây đúng là chỗ mà cột `Trạng thái đánh giá spec` (đang thiếu) tồn tại để chặn. — **Fix**: hỏi Dev/BA nguồn của rule + cơ chế nào thực thi nó (không phải guard đang review), ghi `Đã hỏi leader` vào cột `Trạng thái đánh giá spec`.

- **[MAJOR] Thiếu cột `Trạng thái đánh giá spec` trên toàn bộ 34 TC**: Không TC nào ghi `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. Cột `Spec ID` hiện có là **tham chiếu nguồn**, không thay thế được — nhiều TC ghi `Spec ID: source: <file>.php:<dòng>` tức là **suy từ mã nguồn**, đúng loại tình huống RULE quy về `Spec không ghi`. Nguy cơ tự suy diễn rồi cho Đạt. — **Fix**: thêm cột, đánh dấu ≥ 8 TC đang suy từ code (NEW-4, NEW-5, NEW-15, NEW-18, NEW-21, NEW-22, NEW-23, NEW-29) là `Spec không ghi` + ghi đã hỏi ai.

- **[MAJOR] 3 mã quan điểm KHÔNG tồn tại trong framework**: `TOOL-NEGCTRL-001` (NEW-2/3/4/5/6), `TOOL-ERRHYG-001` (NEW-12/16), `TOOL-SPECFIRST-001` (NEW-27/28) — grep toàn bộ `framework/` không có. 9/34 TC không map được về bộ 80 quan điểm ⇒ coverage matrix theo quan điểm bị thủng. — **Fix**: remap — `TOOL-NEGCTRL-001` → `FUNC-004` (biên tập giá trị) hoặc `DATA-DB-001` (WHERE scope); `TOOL-ERRHYG-001` → `OUT-TRUTH-001` + `SEC-002`; `TOOL-SPECFIRST-001` → `FUNC-001`. Nếu team muốn giữ 3 mã này thì phải bổ sung vào `checklist-lme.md` theo **RULE-10** (có ID + ngày thêm + nguồn).

- **[MAJOR] RULE-01 — quan điểm ưu tiên Cao thiếu loại case, không ghi lý do**:
  | Quan điểm (Cao) | Normal | Abnormal | Boundary | Thiếu |
  |---|---|---|---|---|
  | `CONC-001` | ✗ | NEW-15/32/33/34 | ✗ | **Normal + Boundary** |
  | `PAY-STATE-001` | ✗ | NEW-8/9/10 | ✗ | **Normal + Boundary** |
  | `PAY-BATCH-001` | NEW-24 | NEW-25 | ✗ | **Boundary** |
  | `INTG-HOOK-001` | ✗ | NEW-26 | ✗ | **Normal + Boundary** |
  — **Fix**: bổ sung theo §5, hoặc ghi lý do "quan điểm không có khái niệm biên" vào `Ghi chú`.

- **[MAJOR] NEW-33 / NEW-34 — TC mơ hồ, không verify đúng cơ chế**: Tiền điều kiện là **"Thanh toán thành công"** ⇒ `status_webhook = 1`, **ngoài tập chặn {0,3,4}** ⇒ guard mới **không** kích hoạt. Expected chỉ ghi "Không cho phép thanh toán lại" mà không nêu message/màn nào, nên chạy xong không biết đã verify cơ chế nào. — **Fix**: tách mỗi case thành 2 nhánh tiền điều kiện — (a) webhook **đã** về (`=1`) → cơ chế business rule, ghi rõ màn lỗi; (b) webhook **chưa** về (`=0`) → guard mới, message 「決済処理を行っていますので、操作できません。」.

- **[MAJOR] INTG-HOOK-001 thiếu chiều**: NEW-26 chỉ test **webhook trùng**. Quan điểm yêu cầu đủ: trùng / **đến trễ** / **sai thứ tự** / **mất hẳn** / retry từ phía gửi / gửi lại thủ công. Evidence bắt buộc là **số lần xử lý thực tế đếm từ log/DB** — không được ghi. — **Fix**: `TC-INTGHOOK001-01` (§5).

- **[MAJOR] PAY-BATCH-001 thiếu kịch bản đặc trưng**: Quan điểm yêu cầu *"cho user **hủy hợp đồng ngay trong lúc batch đang chạy** (giữa lúc lấy danh sách và lúc thực thi) → không được trừ tiền"*. NEW-24/25 chỉ chạy job trên trạng thái tĩnh. — **Fix**: `TC-PAYBATCH001-01` (§5).

- **[MAJOR] REG-SHARED-001 rà chưa hết chức năng tương tự**: NEW-30 chỉ rà **Stripe**. Theo `Catalog C` khối `MAP-PAY-01`, luồng tiền của LME gồm **6 kênh**: bill bot · item mua 1 lần · **item chu kỳ** · salon · lesson · event booking. Bug "cho phép gửi yêu cầu mua khi giao dịch trước còn treo" là **pattern có thể tồn tại ở 5 kênh còn lại**. REG-SHARED-001 (Cao) ghi rõ: *"Fix bug ở chức năng A → rà chức năng B có logic tương tự"*. — **Fix**: `TC-REGSHARED001-01` (§5) — rà tĩnh, không cần test đầy đủ; kết quả chuyển Leader quyết định mở ticket riêng (giống cách NEW-30 xử lý Stripe).

- **[MAJOR] DATA-DB-001 — WHERE scope chưa kiểm 2 tài khoản**: NEW-27 xác nhận guard có 4 vế (`status_bill` + `item_id` + `line_user_id` + `status_webhook`) — **không có `bot_id`**. NEW-29 đã phát hiện guard **không lọc theo chế độ môi trường** (test/live) trong khi truy vấn tồn kho ngay bên dưới **có lọc** — đây là bất đối xứng thật, nhưng TC lại được chấm `pass` với Expected bỏ ngỏ. — **Fix**: `TC-DATADB001-01` (§5) — tạo gói chờ trùng `line_user_id` + `item_id` ở 2 bot, xác nhận không chặn chéo.

- **[MAJOR] RULE-05 — chưa tra spec UnivaPay chính thức**: Không TC nào ghi đã tra tài liệu UnivaPay mới nhất về ý nghĩa `authorized` / `pending` / `awaiting_capture`. Đây đúng là chỗ quyết định RC-1 đúng hay sai. — **Fix**: đính kèm link + trích đoạn tài liệu UnivaPay vào `Ghi chú` của TC liên quan.

- **[MAJOR] Không có TC verify UX recovery sau khi guard nhả**: NEW-13 quan sát nút 「購入する」 được bật lại, nhưng **không có bước bấm lại và mua thành công**. §3 Phụ lục yêu cầu mỗi trường hợp lỗi phải có **UX recovery** hoạt động thật. — **Fix**: nối thêm bước vào NEW-13 hoặc tách TC mới: sau khi bị chặn → chờ cron 15 phút → bấm mua lại → **thành công**.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Format file 04 không phải 16 cột canonical**: task folder tạo **2026-08-05** (sau mốc 2026-07-16) nên áp dụng format canonical. Hiện thiếu `Evidence thực tế` + `Trạng thái đánh giá spec` (đã nêu ở §4.2), và có thêm các cột riêng của test-studio (`Nhóm`, `Chạy`, `Spec ID`, `Phạm vi env`). — Giữ cột thừa cũng được, nhưng **phải bổ sung đủ 16 cột canonical** để `/sync-ai-tc` và coverage matrix chạy đúng.
- **[MINOR] `TC No.` sai format**: `NEW-1` … `NEW-34` thay vì `TC-<mã quan điểm bỏ gạch>-<nn>` (vd `NEW-8` → `TC-PAYSTATE001-01`). Đánh lại từ `01` cho mỗi quan điểm.
- **[MINOR] Dùng mã RULE làm mã quan điểm**: NEW-17 ghi `RULE-06`, NEW-11 ghi `RULE-07`. Theo `checklist-lme.md §0.2`, RULE và Quan điểm là 2 khái niệm **không được lẫn**. — Đổi: NEW-17 → `ENV-003` (ghi RULE-06/RULE-08 vào `Ghi chú`); NEW-11 → `PAY-STATE-001`.
- **[MINOR] NEW-23 gán sai quan điểm**: mốc 15 phút là biên của **cơ chế đối soát bù** → nên gán `PAY-ABANDON-001` (Boundary) thay vì `FUNC-004`; đổi xong thì `PAY-ABANDON-001` đủ cả 3 loại case.
- **[MINOR] NEW-32/33/34 thiếu thông tin so với 31 case còn lại**: `Spec ID = -`, `Phạm vi env = -`, không có `Ghi chú`; đồng thời gắn nhóm `ui` nhưng `Chạy = auto` trong khi Các bước là thao tác thủ công ("Back trình duyệt", "Nhấn Mua"). — Điền đủ + thống nhất lại `Chạy`.
- **[MINOR] `Người thực hiện` không nhất quán**: 5 case ghi `AI (thanhntp)` (NEW-25, 27, 28, 29, 30), còn lại ghi `thanhntp`. Cần phân biệt rõ vì 4/5 case đó là **kiểm tra tĩnh do AI đọc code** — bằng chứng yếu hơn chạy thật, Leader cần biết để cân nhắc khi nghiệm thu.
- **[MINOR] SEC-002 chỉ quét 1 chiều**: NEW-12 xác nhận **response** không chứa thông tin nhạy cảm, nhưng chưa quét **console DevTools + server log + log callback** như quan điểm yêu cầu.
- **[MINOR] Tỷ lệ Boundary thấp**: Normal 12 / Abnormal 18 / Boundary 4 = **35 / 53 / 12%** (gợi ý 40/35/25). Abnormal cao là hợp lý với task guard, nhưng Boundary 12% thấp so với task có nhiều biên trạng thái + biên thời gian.

### 4.4 Nit (gợi ý)

- **[NIT] PERF-LARGE-001**: guard thêm 1 truy vấn `s_cycle_order_history` vào **đúng luồng thanh toán**. Với khách có hàng nghìn bản ghi lịch sử gói, nên đo thời gian phản hồi endpoint trước/sau fix — chưa TC nào đo.
- **[NIT] NEW-16 rất tốt, nên nhân bản**: kiểm "thông báo nào được trả ra trước" là cách quan sát thứ tự guard mà không cần đọc code. Có thể áp dụng thêm cho cặp *guard vs kiểm tra sản phẩm ngừng bán / hết hạn*.
- **[NIT] NEW-30 là mẫu tốt cho case out-of-scope**: ghi nhận thực trạng + nói rõ **không tính là không đạt** + chuyển Leader quyết. Nên dùng đúng khuôn này cho `TC-REGSHARED001-01`.
- **[NIT] RULE-11 — không dùng để flag**: các mục ở §4 `checklist-lme.md` (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) không liên quan task này; ghi lại để rõ đã cân nhắc.

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` ở round tiếp theo. Bảng dùng **đúng 16 cột canonical**.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PAYSTATE001-01 | PAY-STATE-001 | Abnormal | Giao dịch UnivaPay dừng ở trạng thái `authorized` thì hạn thu tiền kỳ đó phải được dời, hôm sau job KHÔNG trừ lại | Bot cấu hình UnivaPay; 1 gói định kỳ hàng tháng của khách A đang hoạt động, đã đến hạn thu tiền; có cách ép cổng trả `authorized` (test card giữ ở trạng thái đã ủy quyền, chưa capture) | 1. Ghi lại `c_expired_date`, `count_bill_error` của gói trước khi chạy<br>2. Chạy job thu tiền định kỳ UnivaPay<br>3. Ép cổng trả trạng thái `authorized`<br>4. Kiểm `s_order_history.status_order` + `bill_success_date` của giao dịch vừa tạo<br>5. Kiểm `c_expired_date` + `count_bill_error` của gói<br>6. Đẩy ngày hệ thống sang **hôm sau**, chạy lại job thu tiền<br>7. Đếm số giao dịch trên dashboard UnivaPay của khách A | Gói định kỳ hàng tháng; thẻ test UnivaPay dừng ở `authorized`; chạy job 2 ngày liên tiếp | Giao dịch `authorized` được ghi nhận **thành công** (`status_order = 1`), `c_expired_date` **dời sang kỳ sau**, `count_bill_error` **không tăng**. Ngày hôm sau job **không** phát sinh giao dịch thứ 2. Dashboard UnivaPay chỉ có **1** giao dịch | Chưa test | | PRODUCTION (bắt buộc — RULE-08) | | | | Spec không ghi — cần hỏi Dev | Lấp **GAP-1** (RC-1). **Nếu case này KHÔNG ĐẠT ⇒ bản fix hiện tại không chữa bug của khách.** Evidence bắt buộc: query DB trước/sau (2 ngày) + screenshot dashboard UnivaPay |
| TC-PAYSTATE001-02 | PAY-STATE-001 | Boundary | Gói bị lỗi thu tiền lặp đúng 3 lần thì mới dời hạn — xác nhận cơ chế `count_bill_error` sau fix | Gói định kỳ của khách A đến hạn; ép cổng trả trạng thái lỗi ở mỗi lần chạy job | 1. Chạy job thu tiền, ghi `count_bill_error` sau lần 1<br>2. Lặp lại lần 2, lần 3, lần 4<br>3. Sau mỗi lần: ghi `c_expired_date`, `count_bill_error`, số giao dịch trên cổng | Chạy job 4 ngày liên tiếp trên cùng 1 gói | Số lần trừ tiền thực tế trên cổng khớp **đúng** số lần job chạy, không dư. Mốc dời hạn khớp giá trị `count_bill_error` mà Dev xác nhận | Chưa test | | STAGING + PRODUCTION | | | | Spec không ghi — cần hỏi Dev | Lấp **GAP-1**. Boundary của RULE-01 cho `PAY-STATE-001`. Ghi rõ vào `Ghi chú` con số ngưỡng Dev xác nhận |
| TC-PAYSTATE001-03 | PAY-STATE-001 | Normal | Đối chiếu 3 nơi (admin / màn khách / dashboard cổng) sau từng kịch bản thanh toán gói định kỳ | Bot UnivaPay hoạt động; thẻ test đủ 4 kịch bản: thành công / thất bại / hủy giữa chừng / thu tiền kỳ tiếp theo | 1. Chạy kịch bản **thành công** → mở màn quản lý đơn (admin), màn lịch sử phía khách, dashboard UnivaPay → ghi `tên gói + trạng thái + số tiền` ở cả 3 nơi<br>2. Lặp lại với kịch bản **thất bại**<br>3. Lặp lại với kịch bản **hủy giữa chừng**<br>4. Lặp lại với **thu tiền kỳ tiếp theo (recurring)** | 4 kịch bản × 3 nơi = 12 điểm đối chiếu | Cả 3 nơi khớp nhau về **tên gói + trạng thái + số tiền** ở **từng** kịch bản. Kịch bản thất bại: **không trừ tiền** trên cổng | Chưa test | | PRODUCTION | | | | Spec ghi rõ | Lấp **GAP-2**. RULE-01 Normal cho `PAY-STATE-001`. Evidence: 12 screenshot theo bảng 4×3 |
| TC-ENV003-01 | ENV-003 | Normal | Đối soát cổng UnivaPay trên production sau thao tác mua bị chặn (thay NEW-17 đang skip) | Đã chạy kịch bản khách bị chặn trên **production**; có quyền đọc dashboard UnivaPay của tài khoản bán hàng thật | 1. Ghi lại thời điểm + `line_user_id` của khách đã thao tác mua bị chặn<br>2. Mở dashboard UnivaPay, lọc giao dịch theo khách + khoảng thời gian đó<br>3. Đối chiếu với danh sách đơn hàng phía quản trị<br>4. Ghi lại **router id** của server đã xử lý request (production có 2 server — `ENV-LB`)<br>5. Lặp bước 1-3 trên **router còn lại** | Khoảng thời gian thao tác; mã khách ở cổng thanh toán; 2 router id | Số giao dịch trên cổng **khớp đúng** số đơn phía quản trị; **không** giao dịch nào phát sinh tại thời điểm thao tác bị chặn. Kết quả **giống nhau trên cả 2 router** | Chưa test | | PRODUCTION (chỉ đọc, không thao tác trên cổng) | | | | Spec ghi rõ | Lấp **GAP-2**. Thay NEW-17. Thêm trục `ENV-LB` (2 server) mà NEW-17 chưa có. Evidence: export giao dịch từ cổng + screenshot màn đơn hàng, cho **từng** router |
| TC-CONC001-01 | CONC-001 | Abnormal | Double-click nút mua lặp 20 lần — đếm số gói và số giao dịch thực tế phát sinh | Khách A chưa có gói của sản phẩm X; có script/tool bấm 2 request cách nhau < 200ms; có quyền query DB và đọc dashboard cổng | 1. `COUNT(*)` bản ghi gói của khách A cho sản phẩm X trước khi chạy<br>2. Gửi 2 request mua song song cách nhau < 200ms<br>3. `COUNT(*)` lại + đếm giao dịch trên cổng<br>4. Xoá dữ liệu, **lặp lại bước 1-3 đủ 20 lần**<br>5. Lập bảng: lần chạy × số gói × số giao dịch | 20 vòng lặp; 2 request song song mỗi vòng; cùng khách + cùng sản phẩm | **Cả 20/20 vòng** đều chỉ tạo 1 gói và 1 giao dịch. Nếu có **bất kỳ** vòng nào ra 2 → ghi Không đạt và báo Dev bổ sung khoá/unique index | Chưa test | | STAGING + PRODUCTION | | | | Spec không ghi — Dev đã nêu rủi ro TOCTOU ở §7 file 03 | Lấp **GAP-3**, thay NEW-15 (chạy 1 lần không kết luận được race). Evidence bắt buộc theo `CONC-001`: **bảng 20 dòng** `COUNT(*)` từ DB + số giao dịch cổng |
| TC-CONC001-02 | CONC-001 | Abnormal | Job thu tiền định kỳ chạy đồng thời với thao tác mua của chính khách đó | Khách A có gói định kỳ sản phẩm X **đã đến hạn thu tiền**; có thể hẹn giờ chạy job trùng thời điểm khách bấm mua | 1. Hẹn job thu tiền định kỳ chạy tại thời điểm T<br>2. Tại T, khách A bấm mua sản phẩm X trên màn xác nhận đơn<br>3. Đếm số giao dịch trên cổng + số bản ghi `s_order_history` phát sinh<br>4. Kiểm `c_expired_date` của gói<br>5. Lặp 5 lần với độ lệch thời gian khác nhau (−1s / 0 / +1s / +3s / +10s) | 5 vòng, mỗi vòng 1 độ lệch thời gian | Không có vòng nào phát sinh **2 lần trừ tiền** cho cùng 1 kỳ. Hạn gói được dời **đúng 1 lần** | Chưa test | | STAGING | | | | Spec không ghi — cần hỏi Dev | Lấp **GAP-3** — kịch bản (4) của `CONC-001` (batch đa luồng chạm giới hạn dùng chung), hiện hoàn toàn trống. Evidence: log job + query DB + dashboard cổng |
| TC-CONC001-03 | CONC-001 | Normal | Sau khi bị chặn và cron đã nhả, khách bấm mua lại thành công (UX recovery) | Khách A vừa bị chặn bởi guard; cron `recover:payment_univapay_timeout` chạy mỗi 5 phút, ngưỡng 15 phút | 1. Tạo trạng thái bị chặn, xác nhận thấy 「決済処理を行っていますので、操作できません。」<br>2. Xác nhận nút 「購入する」 được **bật lại**<br>3. Chờ cron chốt trạng thái gói (> 15 phút)<br>4. Bấm 「購入する」 lại trên **chính màn đang mở**, không reload<br>5. Kiểm gói + giao dịch phát sinh + tin nhắn kết quả trên LINE | Cùng khách, cùng sản phẩm; không reload trang giữa chừng | Lần bấm sau khi cron nhả **thành công**: tạo đúng 1 gói, đúng 1 giao dịch trên cổng, khách **nhận được tin kết quả trên LINE app thật** | Chưa test | | STAGING + PRODUCTION | | | | Spec ghi rõ | RULE-01 Normal cho `CONC-001`. Bổ sung phần UX recovery mà NEW-13 dừng giữa chừng. Evidence: video thao tác + screenshot LINE app (RULE-06) |
| TC-COMPATLEGACY001-01 | COMPAT-LEGACY-001 | Abnormal | Gói định kỳ tạo bởi luồng đời cũ (trước V2) không bị guard chặn nhầm | Lấy **mẫu thật** ≥ 5 bản ghi `s_cycle_order_history` được tạo trước khi có luồng V2, có `status_bill = 1` (đang hoạt động) | 1. Hỏi Dev/DBA lấy danh sách gói cũ đang hoạt động, ghi lại giá trị `status_webhook` của từng bản ghi<br>2. Với mỗi khách trong danh sách, mở màn xác nhận mua **chính sản phẩm đó**<br>3. Bấm 「購入する」<br>4. Ghi lại có bị chặn hay không, và message nhận được | 5 gói cũ từ **nhiều thời điểm tạo khác nhau**, mỗi gói 1 lần thử mua | Không khách nào bị chặn bởi 「決済処理を行っていますので、操作できません。」 chỉ vì bản ghi đời cũ. Nếu **có** bị chặn ⇒ Không đạt, báo Dev bổ sung điều kiện lọc theo thời điểm tạo | Chưa test | | PRODUCTION (dữ liệu thật) | | | | Spec không ghi — cần hỏi Dev | Lấp **GAP-4** nhánh (a). RULE-09: không được kết luận từ dữ liệu mới. **Câu hỏi chốt cho Dev**: bản ghi tạo trước luồng V2 có `status_webhook` bằng mấy? |
| TC-COMPATLEGACY001-02 | COMPAT-LEGACY-001 | Normal | Gói tạo trước và gói tạo sau bản fix chạy song song, cùng đi hết vòng đời thu tiền | 1 gói tạo **trước** khi deploy bản fix + 1 gói tạo **sau**, cùng sản phẩm, cùng chu kỳ | 1. Cho cả 2 gói cùng đến hạn thu tiền<br>2. Chạy job thu tiền định kỳ<br>3. So sánh kết quả 2 gói: giao dịch phát sinh, `c_expired_date` mới, trạng thái<br>4. Với mỗi gói: khách thử mua lại chính sản phẩm đó → ghi hành vi | 2 gói song song; 1 chu kỳ thu tiền đầy đủ | Hai gói cho **kết quả giống hệt nhau** ở cả 4 điểm so sánh. Không có khác biệt do thời điểm tạo | Chưa test | | STAGING + PRODUCTION | | | | Spec ghi rõ | Lấp **GAP-4**. `regression`. Evidence: bảng đối chiếu 2 gói × 4 điểm |
| TC-REGRUN001-01 | REG-RUN-001 | Abnormal | Gói đang ở trạng thái chờ tại đúng thời điểm deploy vẫn xử lý đúng sau release | Trước khi deploy: tạo sẵn 2 gói của 2 khách đang ở `status_webhook` chờ (1 gói có mã giao dịch, 1 gói không) | 1. **Trước** deploy: tạo 2 gói ở trạng thái chờ, ghi lại thời điểm tạo<br>2. Deploy bản fix<br>3. **Không** can thiệp dữ liệu, chạy cron đối soát<br>4. Kiểm trạng thái 2 gói sau cron<br>5. Với mỗi khách: thử mua lại chính sản phẩm đó<br>6. Chờ đủ 30 phút, lặp bước 4-5 | 2 gói chờ tạo trước deploy; theo dõi 30 phút sau release | Gói **có** mã giao dịch: cron chốt trạng thái, khách mua lại được. Gói **không** có mã giao dịch: **không được kẹt vĩnh viễn** — phải có cơ chế gỡ hoặc thông báo rõ | Chưa test | | STAGING (diễn tập) + PRODUCTION (ngày release) | | | | Spec không ghi — cần hỏi Dev | Lấp **GAP-4** nhánh (b). Chạy **đúng ngày release**, không lùi lại được. `regression` |
| TC-INTGHOOK002-01 | INTG-HOOK-002 | Abnormal | Gói chờ không có mã giao dịch — xác nhận khách không bị khoá vĩnh viễn (thay NEW-22 đang skip) | Khách A có gói định kỳ đang hoạt động của sản phẩm X, `status_webhook` = chờ, **mã giao dịch để trống**, thời điểm tạo lùi 30 phút | 1. Chạy cron đối soát → kiểm trạng thái gói<br>2. Khách A thử mua lại sản phẩm X → ghi message<br>3. Chạy cron thêm 3 lần nữa (cách nhau 5 phút) → kiểm lại trạng thái<br>4. Khách A thử mua lại lần nữa<br>5. Đẩy thời điểm tạo lùi **24 giờ**, lặp bước 1-4 | Gói chờ, mã giao dịch rỗng; mốc thời gian 30 phút và 24 giờ | Khách **KHÔNG** được kẹt ở trạng thái không mua được quá 1 giờ. Nếu sau 24 giờ vẫn bị chặn ⇒ **Không đạt** — báo Dev bổ sung điều kiện thời gian tối đa cho guard | Chưa test | | STAGING | | | | Đã hỏi leader — cần chốt ngưỡng thời gian tối đa chấp nhận được | Lấp **GAP-5**, thay NEW-22. Expected của NEW-22 bỏ ngỏ ("CẦN LEADER XÁC NHẬN") nên không chấm được — bản này đặt tiêu chí Đạt/Không đạt cụ thể |
| TC-INTGHOOK001-01 | INTG-HOOK-001 | Abnormal | Webhook kết quả thanh toán đến trễ / sai thứ tự / mất hẳn | Khách A có gói chờ đã ghi nhận mã giao dịch; có công cụ gửi lại webhook thủ công | 1. **Trễ**: chặn webhook 20 phút rồi mới thả → kiểm trạng thái gói + số bản ghi thu tiền<br>2. **Sai thứ tự**: gửi webhook `thành công` **trước** webhook `đang xử lý` → kiểm trạng thái cuối<br>3. **Mất hẳn**: chặn webhook vĩnh viễn, chỉ để cron đối soát chốt → kiểm trạng thái<br>4. **Gửi lại thủ công**: gửi lại webhook đã xử lý → đếm số lần xử lý trong log<br>5. Sau mỗi kịch bản: khách thử mua lại | 4 kịch bản webhook; mỗi kịch bản đếm số lần xử lý từ log/DB | Mỗi kịch bản: trạng thái cuối **đúng**, số lần ghi nhận thu tiền **đúng 1**, khách không bị chặn sai. Kịch bản 4: log phải chứng minh lần thứ 2 **bị bỏ qua** | Chưa test | | STAGING | | | | Spec ghi rõ | Bổ sung chiều thiếu của `INTG-HOOK-001` (NEW-26 chỉ có "trùng"). Evidence bắt buộc: **payload webhook gốc + idempotency key + SỐ LẦN XỬ LÝ đếm từ log** — không chấp nhận "đã thử, thấy bình thường" |
| TC-PAYBATCH001-01 | PAY-BATCH-001 | Abnormal | Hủy gói định kỳ ngay giữa lúc job thu tiền đang chạy thì không được trừ tiền | Khách A có gói định kỳ đã đến hạn thu tiền; có thể chèn thao tác hủy vào giữa lúc job lấy danh sách và lúc job thực thi | 1. Cho job thu tiền bắt đầu chạy (đã lấy danh sách gói đến hạn)<br>2. **Trong lúc job đang chạy**, hủy gói của khách A từ màn quản trị<br>3. Chờ job chạy xong<br>4. Đếm giao dịch trên cổng UnivaPay của khách A<br>5. Kiểm `status_bill` của gói + `s_order_history` phát sinh | Hủy gói tại thời điểm giữa 2 pha của job; lặp 3 lần với 3 điểm chèn khác nhau | Khách A **không bị trừ tiền** ở cả 3 lần. Job phải lấy trạng thái **mới nhất ngay trước khi thực thi**, không dùng trạng thái lấy từ đầu batch | Chưa test | | STAGING | | | | Spec ghi rõ | Kịch bản đặc trưng của `PAY-BATCH-001` hiện trống (NEW-24/25 chỉ chạy trên trạng thái tĩnh). Evidence: log job + dashboard cổng |
| TC-REGSHARED001-01 | REG-SHARED-001 | Abnormal | Rà 5 kênh thanh toán còn lại có cùng lỗ hổng "cho mua khi giao dịch trước còn treo" hay không | Đã checkout nhánh `ai_fixbug_39271`; có danh sách endpoint thanh toán do Dev cung cấp | 1. Yêu cầu Dev cung cấp danh sách endpoint thanh toán của **6 kênh** (`Catalog C` khối `MAP-PAY-01`): bill bot · item mua 1 lần · item chu kỳ · salon · lesson · event booking<br>2. Với **từng** endpoint, tìm xem có đoạn chặn tương tự guard mới không<br>3. Với kênh **không có** guard: dựng 1 kịch bản mua chồng thủ công, ghi lại có tạo 2 đơn không<br>4. Lập bảng 6 kênh × (có guard? / mua chồng được?) chuyển Leader | Nhánh `ai_fixbug_39271`; 6 kênh thanh toán | Ghi nhận **đúng thực trạng** từng kênh. Kênh nằm ngoài phạm vi ticket **KHÔNG** tính là không đạt cho ticket này — kết quả chuyển Leader quyết định mở ticket riêng | Chưa test | | Tất cả (kiểm tra tĩnh) + STAGING (kịch bản mua chồng) | | | | Spec không ghi — ngoài phạm vi ticket, ghi nhận để Leader quyết | `REG-SHARED-001` (Cao): fix bug ở chức năng A → rà chức năng B có logic tương tự. NEW-30 mới rà Stripe. Dùng đúng khuôn xử lý out-of-scope của NEW-30 |
| TC-DATADB001-01 | DATA-DB-001 | Abnormal | Điều kiện chặn không được chặn chéo giữa 2 bot / 2 chế độ môi trường | Có 2 bot cùng tổ chức; tạo được gói chờ trùng `line_user_id` và trùng `item_id` ở cả 2 bot; sản phẩm có cả chế độ thử nghiệm và chính thức | 1. Tạo gói định kỳ ở trạng thái chờ cho khách A, sản phẩm X, **bot 1**<br>2. Cùng khách A, cùng sản phẩm X, thử mua ở **bot 2** → ghi kết quả<br>3. Tạo gói chờ ở **chế độ thử nghiệm**, thử mua cùng sản phẩm ở **chế độ chính thức** → ghi kết quả<br>4. Query DB xác nhận điều kiện chặn có lọc `bot_id` và chế độ môi trường hay không | 2 bot × 1 khách × 1 sản phẩm; 2 chế độ môi trường | Thao tác ở bot 2 / chế độ chính thức **không** bị chặn bởi bản ghi của bot 1 / chế độ thử nghiệm. Nếu bị chặn ⇒ báo Dev bổ sung điều kiện lọc | Chưa test | | STAGING | | | | Đã hỏi leader — NEW-29 đã phát hiện bất đối xứng, chờ Dev xác nhận cố ý hay thiếu | `DATA-DB-001` (Cao) — kiểm `WHERE` scope trên 2 tài khoản (RULE-07). Nối tiếp phát hiện của NEW-29 (guard không lọc chế độ môi trường trong khi truy vấn tồn kho ngay bên dưới **có** lọc). Evidence: query trước/sau kèm câu query, trên **cả 2** tài khoản |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần làm rõ spec / hỏi Dev — 5 điểm chặn trước vòng 2**

| # | Câu hỏi | Gửi ai | Vì sao chặn |
|---|---|---|---|
| 1 | Dữ liệu production của khách 「マナフレンズ」: **2 lần trừ tiền cách nhau bao lâu**, `status_order` của từng lần là gì? | Dev / vận hành | Quyết định RC-1 đúng hay sai ⇒ quyết định bản fix có chữa đúng bug không (**GAP-1**) |
| 2 | Bản ghi `s_cycle_order_history` tạo **trước luồng V2** có `status_webhook` bằng mấy? Có bản ghi nào `status_bill = 1` + `status_webhook ∈ {0,3,4}` tồn tại từ lâu không? | Dev / DBA | Quyết định guard có chặn nhầm khách hợp lệ không (**GAP-4**) |
| 3 | Business rule *"khách chỉ được sở hữu 01 order của cùng sản phẩm tại một thời điểm"* — nguồn ở đâu, **cơ chế nào** thực thi (không phải guard đang review)? | BA / Dev | NEW-18 và NEW-21 đang chấm `pass` dựa trên rule chưa có nguồn |
| 4 | Guard **cố ý** không lọc theo chế độ môi trường (test/live) hay là thiếu? Có lọc `bot_id` không? | Dev | NEW-29 đã phát hiện bất đối xứng nhưng Expected bỏ ngỏ |
| 5 | Ngưỡng thời gian tối đa chấp nhận được cho việc khách bị guard chặn là bao lâu? (hiện phụ thuộc cron 15 phút, nhưng gói thiếu mã giao dịch có thể chờ vô hạn) | Leader / BA | Không có ngưỡng thì NEW-22 / `TC-INTGHOOK002-01` không chấm được Đạt/Không đạt |

**Ngoài phạm vi ticket — Leader quyết định mở ticket riêng**:
- Luồng thẻ **Stripe** cùng màn xác nhận đơn chưa có guard tương tự (Dev xác nhận ngoài phạm vi; NEW-30 đã ghi nhận).
- **Recover data**: khách đã bị trừ trùng trước fix cần đối soát + hoàn tiền thủ công. Theo **RULE-04**, trước khi đóng ticket phải có **query/thống kê toàn hệ thống** xác nhận phạm vi ảnh hưởng — không recovery 1 tài khoản rồi kết luận "hiếm gặp". Hiện chưa có TC/hạng mục nào track việc này.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ⚠️ (BUG cover kịch bản QA dựng, chưa loại trừ RC-1) · A.2 ⚠️ (F2 chỉ 1 TC) · A.3 ✓ (D1 xuất sắc) · A.4 ⚠️ (T2 GAP ở đối soát cổng) · A.5 ✓ · A.6 ⚠️ (xem §3.5)
- [x] **B. Chất lượng từng TC** — B.1 ⚠️ (NEW-15/22/29 Expected bỏ ngỏ; NEW-33/34 Expected mơ hồ) · B.2 ✓ · B.3 ✓ · B.4 ✓ (data sample nghiệp vụ thật, không dùng `"test"`/`"abc"`)
- [x] **C. Chất lượng bộ TC** — tỷ lệ 35/53/12 ⚠️ (Boundary thấp) · không trùng lặp ✓ · phân bố quan điểm ⚠️ (9 TC gán mã không tồn tại)
- [x] **D. Spec alignment** — ⚠️ không có `02-spec-reference.md`; 1 business rule chưa có nguồn (§6 #3)
- [x] **E. Hành chính** — ⚠️ TC ID sai format · thiếu 2 cột canonical · `Người thực hiện` không nhất quán
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — **A** ✓ (biên số lượng NEW-20) · **B** ⚠️ (chỉ NEW-13 chạm UI thật) · **C** ⚠️ (khối `MAP-PAY-01` mới rà 2/6 kênh) · **D/D2** ✗ (**không TC production nào chạy** — vi phạm RULE-08, `ENV-PAY`) · **E** — không áp dụng (task không chạm media)
  - [x] F.3 RULE quy trình — RULE-01 ✗ · RULE-02 ✗ · RULE-03 n/a · RULE-04 ⚠️ (recovery chưa có thống kê toàn hệ thống) · RULE-05 ✗ · RULE-06 ✓ (NEW-7 verify tới LINE app) · RULE-07 ⚠️ · RULE-08 ✗ · RULE-09 ✗ · RULE-12 ⚠️

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ mọi chức năng | NEW-1 (Normal), NEW-7 (Normal, có LINE app) | **RISK** — chỉ có Normal gán mã này; các chiều khác nằm ở mã khác |
| `FUNC-004` | Cao | ◯ có giới hạn số lượng | NEW-20 (Boundary 0 / −1) | **RISK** — thiếu biên trên (số lượng max, tồn kho biên). NEW-18/19/23 gán FUNC-004 nhưng thực chất là biên **trạng thái**, nên remap |
| `CONC-001` | **Cao** | ◯ **BẮT BUỘC** — nút thực thi hành động quan trọng, xử lý trùng | NEW-15, NEW-32, NEW-33, NEW-34 (đều Abnormal) | **GAP → [BLOCKER]** — không evidence đếm, TOCTOU tự thừa nhận, thiếu kịch bản (4), thiếu Normal + Boundary |
| `PAY-STATE-001` | **Cao** | ◯ **BẮT BUỘC** — giao dịch tiền | NEW-8, NEW-9, NEW-10 (đều Abnormal) | **GAP → [BLOCKER]** — không TC nào đối chiếu 3 nơi; thiếu kịch bản hủy/refund; thiếu Normal + Boundary |
| `PAY-ABANDON-001` | Cao | ◯ **BẮT BUỘC** — luồng thanh toán/subscription | NEW-13, NEW-14 (Abnormal), NEW-21 (Normal), NEW-23 (Boundary — hiện gán nhầm FUNC-004) | **OK** ✅ — điểm mạnh nhất của bộ TC (sau khi remap NEW-23) |
| `PAY-BATCH-001` | Cao | ◯ **BẮT BUỘC** — batch tác động tiền | NEW-24 (Normal), NEW-25 (Abnormal) | **RISK → [MAJOR]** — thiếu kịch bản hủy giữa lúc batch chạy + thiếu Boundary |
| `INTG-HOOK-001` | Cao | ◯ **BẮT BUỘC** — nhận webhook từ cổng | NEW-26 (Abnormal) | **RISK → [MAJOR]** — chỉ có "trùng"; thiếu trễ/sai thứ tự/mất/gửi lại; không evidence đếm |
| `INTG-HOOK-002` | Trung bình | ◯ luồng chỉ hoàn tất khi nhận callback | NEW-22 (**skip**), NEW-32 (pass) | **RISK → [BLOCKER]** — case skip chính là hệ quả rủi ro do fix tạo ra |
| `COMPAT-LEGACY-001` | **Cao** | ◯ **BẮT BUỘC** — đối tượng đã version-up (V1 → V2) | — | **GAP → [BLOCKER]** |
| `REG-RUN-001` | **Cao** | ◯ **BẮT BUỘC** — có dữ liệu đang chạy dở khi release | — | **GAP → [BLOCKER]** |
| `ENV-003` | **Cao** | ◯ **BẮT BUỘC** — chạm thanh toán (`ENV-PAY`) | NEW-17 (**skip** — TC prd duy nhất) | **GAP → [BLOCKER]** — RULE-08: bill tiền không được kết luận từ staging |
| `REG-SHARED-001` | Cao | ◯ **BẮT BUỘC** — bug có thể tồn tại ở chức năng tương tự | NEW-30 (Abnormal, static), NEW-31 (Normal) | **RISK → [MAJOR]** — mới rà 2/6 kênh của `MAP-PAY-01` |
| `DATA-DB-001` | Cao | ◯ — `WHERE` scope của truy vấn guard | NEW-27 (static, 4 vế), NEW-29 (phát hiện thiếu lọc chế độ môi trường) | **RISK → [MAJOR]** — chưa kiểm trên 2 tài khoản; NEW-29 Expected bỏ ngỏ mà vẫn `pass` |
| `OUT-TRUTH-001` | Cao | ◯ — thao tác có thông báo kết quả | NEW-12, NEW-16 | **OK** ✅ |
| `SEC-002` | Cao | ◯ — xử lý payment | NEW-12 | **RISK → [MINOR]** — mới quét response, chưa quét console/server log/log callback |
| `STATE-001` | Cao | ◯ — ≥2 bước ghi dữ liệu tuần tự | NEW-14 | **RISK** — 1 TC, chưa ngắt giữa **từng cặp** bước |
| `UI-003` | Trung bình → Cao (rủi ro false success) | ◯ — màn xử lý bất đồng bộ | NEW-13 | **RISK** — 1 TC manual, không evidence |
| `PERF-LARGE-001` | Trung bình | ◯ — thêm truy vấn vào luồng thanh toán | — | **GAP → [NIT]** — rủi ro thấp, ghi nhận |
| `DEPLOY-ASSET-001` | Cao | ✗ | — | **× có lý do** — bản fix cuối chỉ sửa **1 file PHP**, không sửa JS/CSS; `confirm-order.js` chỉ được đọc |
| `DATA-AUDIT-001` | Cao | ✗ | (NEW-11 có kiểm nhật ký chặn) | **× có lý do** — guard chỉ READ, không đổi trạng thái dữ liệu |
| `LIFF-ENTRY-001` | Cao | ✗ | — | **× có lý do** — fix không phát sinh URL mới cho LINE user, không đổi điểm vào |
| `JOB-001` | Cao | ✗ | (NEW-21/22/23 cover cron ở mức đủ) | **× có lý do** — fix không thêm/sửa job nền |
| `DATA-COUNT-001` · `MSG-*` · `MEDIA-*` · `FRIEND-*` · `PERM-*` | — | ✗ | — | **× có lý do** — ngoài phạm vi fix |

**Tổng kết F.1**: 6 quan điểm ưu tiên **Cao** ở trạng thái **GAP** → 5 BLOCKER (gộp `COMPAT-LEGACY-001` + `REG-RUN-001` thành GAP-4). 7 quan điểm ở trạng thái **RISK** → MAJOR.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | NganNT | 2026-08-05 |
| Tester | thanhntp — (đã đọc & hiểu feedback) | |
