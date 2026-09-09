# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39592 — [T11874][Bill tiền tool] Hóa đơn tháng 6 phát hành nhầm sang tháng 7` |
| Reviewer (Leader) | `<Leader verify draft này>` — draft sinh bởi `/review-tc` |
| Tester được review | TCs do **AI** sinh trên MCP LME TEST STUDIO (task #69, job #330); QA chạy: `anhptn` |
| Ngày review | `2026-08-13` |
| Version TCs | Studio round 1 (13 TC, `status = draft`) |
| Vòng review | Round 1 |

> **Input thiếu**: `02-spec-reference.md` không có → **Spec reference: dùng `templates/LME-SYSTEM-SPEC.md` tổng, không có spec riêng cho task này.** Hệ quả: không có nguồn spec để đối chiếu quy tắc chia trang biên lai (10 giao dịch trang đầu / 20 trang sau), quy tắc `発行日`, quy tắc làm tròn thuế 10% — xem §6.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC bắt đúng trục chính của bug (tải liên tiếp không reload) và chất lượng từng TC khá cao, nhưng **13/13 TC đã tick `Đạt` mà không có evidence nào và không có TC nào chạy PRODUCTION** — với task bill tiền thì theo RULE-02 + RULE-08 kết quả này **không nghiệm thu được**. Ngoài ra còn 5 GAP coverage thực chất: không có TC mô phỏng **đúng** steps KH, thiếu double-click, thiếu nhánh lỗi, màn Chi tiết hợp đồng không test trục "đổi hợp đồng", và tuyên bố "bịt luôn trường hợp lần tải trước hỏng giữa chừng" ở mục 2 dev-impact không có TC nào verify.

---

## 2. Tóm tắt cho member

Bộ TC này viết **tốt hơn mặt bằng chung**: steps đủ chi tiết để dựng env, expected đo lường được (số dòng / tổng tiền / số trang cụ thể), và đặc biệt phần `Ghi chú` ghi rõ lý do kỹ thuật của từng case — TC-TOOLKNOW002-01 còn tự cảnh báo "nếu reload thì kết quả pass là vô nghĩa", đúng tinh thần review.

Vấn đề lớn không nằm ở cách viết TC mà ở **cách nghiệm thu**: toàn bộ 13 TC được tick `Đạt` nhưng cột Evidence rỗng và tất cả chạy trên `staging` — với hóa đơn tiền gửi cho khách thật thì RULE-02 và RULE-08 không cho phép kết luận. Cần bổ sung bằng chứng (file PDF thật) và chạy lại trục chính trên production.

Về coverage, hãy tập trung 5 chỗ: (1) tái hiện **đúng** thao tác KH báo (tab `個別発行` + tick checkbox rồi mới đổi tháng — hiện đang bị tách rời ở 3 TC khác nhau); (2) double-click nút tải; (3) nhánh lỗi/mạng đứt; (4) màn Chi tiết hợp đồng phải đổi **hợp đồng** chứ không phải đổi `宛名`; (5) tháng có 0 và đúng 10 giao dịch.

---

## 3. Coverage Matrix

> Map **quan điểm** đọc ở cột `Mã quan điểm liên kết`; map **impact BUG/F/D/T** suy luận từ Tiêu đề / Tiền đề / Các bước / Kết quả mong đợi.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — biên lai lần tải thứ 2 lấy nội dung lần tải trước | Fix | — | TC-TOOLKNOW002-01, TC-FUNCSEQ001-02, TC-RULE06-01, TC-OUTTRUTH001-01 | 4 | **RISK** — không TC nào đi **đúng** đường KH/QA báo (`個別発行` + tick checkbox + đổi tháng) |
| **F1** — `handleResponsePdf` (invoices.js) | Function | Direct | TC-TOOLKNOW002-01, TC-FUNCSEQ001-01/-02, TC-OUTTRUTH001-01/-02, TC-SELECTSCOPE001-01, TC-CONC003-01, TC-REGSHARED001-01 | 8 | **RISK** — đủ Normal, thiếu nhánh **lỗi/timeout/double-click** (Abnormal) |
| **F2** — template `invoice_pdf` `v-show`→`v-if` | Function | Direct | TC-UI003-01, TC-FUNCSEQ001-02, TC-FUNC004-01, TC-PERFLATENCY001-01 | 4 | **RISK** — thiếu biên 0 bản ghi và đúng biên 10 (Dev có lý luận về 0 bản ghi nhưng không có TC) |
| **F3** — `generateCanvas` / `waitForElement` / `downloadPdf` (không sửa, đổi hành vi runtime) | Function | Indirect | TC-PERFLATENCY001-01, TC-FUNC004-01 | 2 | **RISK** — ngưỡng chờ 5s chỉ test ở 1 mốc "khoảng 100 giao dịch", không ghi nguồn quy mô |
| **F4** — `downloadInvoices` / `remoteLoadData` / `remoteHandleResponse` (payment_history/index.js) | Function | Indirect | 12 TC màn `SCR-DC-09` | 12 | **OK** |
| **F5** — `downloadInvoices` (bill/js/detail.js) | Function | Indirect | TC-REGSHARED001-01 | 1 | **RISK** — 1 TC, Normal, và **không đổi hợp đồng giữa 2 lần tải** |
| **D1** | Data | — | — | — | **N/A** — Dev khai không chạm data. Đúng: fix thuần tầng hiển thị client, `DATA-DB-001` / `DATA-AUDIT-001` **không** trigger (× có lý do) |
| **T1** — Payment History (FS-009) `/basic/payment-history` | Feature | High | 12/13 TC | 12 | **RISK** — coverage rộng nhưng **0 TC production** (RULE-08) và **0 evidence** (RULE-02) |
| **T2** — Contract Plan & Payment (FA-031) `/basic/detail-contract/{id}` | Feature | High | TC-REGSHARED001-01 | 1 | **RISK cận GAP** — 1 TC happy-path duy nhất cho 1 feature High risk (AP-3) |

### ORPHAN TCs

**Không có TC orphan.** Cả 13 TC đều trace được về BUG / F1–F5 / T1 / T2.

> Đáng ghi nhận: bộ TC **không** dính AP-5 (over-coverage tầng downstream). `ajaxPaymentHistories` / `handleTotalPagePdf` ở tầng server **không bị sửa** (mục 3 dev-impact ghi rõ "Đã check, không sửa") và bộ TC **không** đề xuất TC test tầng API — đúng nguyên tắc bám layer bị chạm. Vì vậy `REQ-008` (category `api`) có 0 TC **KHÔNG bị tính là GAP** trong review này.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Kết hợp 3 shape**: (a) **Shared code / component chung** — sửa `mixins/invoices.js` + blade template dùng chung 2 màn; (b) **Race-condition tầng client** — thêm `$nextTick` để ép đúng thứ tự render trước khi chụp; (c) **JS / asset** — file JS + blade thay đổi, đi kèm tham số version cache |
| **Trigger space cần cover** | (a) **2 nơi dùng chung** Dev liệt kê: `payment_history/index.js` · `bill/js/detail.js` → mỗi nơi phải test **trục thay đổi riêng** (màn 1: đổi **tháng**; màn 2: đổi **hợp đồng**). (b) **5 kịch bản race client** của `CONC-003` + **double-click** của `CONC-001`. (c) **F5 thường sau release thật** + Network kiểm query version. |
| **Số trigger TCs hiện cover** | (a) **1.5 / 2** — màn 2 có TC nhưng đổi `宛名` thay vì đổi **hợp đồng**, tức không tái lập trục gây bug. (b) **2 / 6** — có mạng chậm + chèn thao tác giữa chừng; **thiếu double-click, thiếu delay response rồi bỏ qua response cũ, thiếu bấm filter/đổi tab liên tiếp**. (c) **1 / 1 nhưng chạy sai môi trường** — TC tồn tại, chạy trên staging, mà chính TC tự ghi commit **không bump `config sns-line.version`**. |
| **KH report dạng** | **Có root cause cụ thể** — KH nêu rõ hiện tượng ("6月支払いの領収書を発行した際、7月分にて発行されます"), OEM 沖原裕樹 còn nêu đúng cơ chế ("khi tải liên tiếp các hóa đơn, ngày của hóa đơn tải lần đầu bị áp dụng luôn cho cả các lần tải sau đó"), QA Hạnh Nguyễn tái hiện được. **Không** dính AP-2. |
| **Alternative root causes cần verify** | 1 điểm còn treo: KH ghi *"tôi cũng từng hỏi cùng vấn đề này trước đây"* → cần tra ticket cũ để xác định đây là **tái phát của một fix trước** hay là **report cũ chưa từng được fix**. Nếu là tái phát → RULE-12 buộc case cũ phải nằm trong bộ regression lần này. |
| **Anti-patterns dính** | **AP-3** (happy-path-only regression ở T2 — 1 TC, precondition sạch, không edge state). **AP-4 mức nhẹ** (không có link PR/diff để verify fix shape thực tế; chỉ có branch `ai_small_39592` + commit `233c4ae7b2` — vẫn checkout được nên hạ xuống MINOR). **Không** dính AP-1, AP-2, AP-5, AP-6. |

### Câu hỏi adversarial chưa có TC trả lời

1. Mục 2 tuyên bố *"Đồng thời bịt luôn trường hợp lần tải trước **hỏng giữa chừng** làm khối biên lai còn sót lại trong trang"* — **không TC nào tạo ra tình huống "hỏng giữa chừng"**. Đây là claim của fix, phải có TC chứng minh.
2. `waitForElement` chờ tối đa 5 giây rồi **chỉ log cảnh báo và dừng** (TC-PERFLATENCY001-01 ghi rõ). Khi quá ngưỡng: popup không đóng, lớp phủ không tắt, **không có file** — nhưng user thấy gì? Có bị hiểu nhầm là đang tải? Không TC nào verify hành vi **sau khi timeout xảy ra**, chỉ verify "không timeout".
3. Đổi `v-show`→`v-if` khiến node bị **huỷ và dựng lại**. Nếu user **double-click** nút tải, lần chụp thứ 2 có thể chạy trên DOM đang bị huỷ dở → không TC nào chạm.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] RULE-08 / `ENV-003` — Toàn bộ 13/13 TC chạy `staging`, 0 TC `PRODUCTION`**: task là **bill tiền / hóa đơn gửi khách thật**, thuộc đúng hạng mục Catalog D cấm kết luận từ staging. Riêng `TC-DEPLOYASSET001-01` tự khai `env_scope = [dev, staging, prd]` mà vẫn chỉ chạy staging. — **Fix**: chạy lại tối thiểu trục chính (tháng A→tháng B) + kịch bản release trên `step.lme.jp` với account thật; xem TC đề xuất `TC-ENV003-01`, `TC-DEPLOYASSET001-02`.

- **[BLOCKER] RULE-02 — Evidence rỗng 13/13 nhưng tất cả tick `Đạt`**: không có file PDF, ảnh chụp hay log nào đính kèm. Nghiêm trọng nhất ở `TC-TOOLKNOW002-01` vì chính TC ghi *"tuyệt đối không tải lại trang giữa hai lần tải — nếu reload thì lỗi không tái hiện được và kết quả pass là vô nghĩa"* — không có bằng chứng thì không thể biết QA có tuân thủ hay không. — **Fix**: `anhptn` bổ sung **2 file PDF của 2 lần tải liên tiếp** cho mỗi TC trục chính, + ảnh console cho `TC-PERFLATENCY001-01`, + ảnh Network cho `TC-DEPLOYASSET001-01`.

- **[BLOCKER] FIX-SHAPE: GAP-1 — Không TC nào mô phỏng ĐÚNG steps KH/QA báo**. `01-bug-task.md` ghi: tab `個別発行` → **tick checkbox** hóa đơn → Download → **đổi sang tháng 6** → tick checkbox → Download. Bộ TC tách trục này ra 3 TC khác nhau và không TC nào ghép lại: `TC-TOOLKNOW002-01` đổi tháng nhưng dùng `一括ダウンロード` **không** qua tab `個別発行`; `TC-SELECTSCOPE001-01` có `個別発行`+tick nhưng **cùng một tháng**; `TC-OUTTRUTH001-01` có `個別発行` nhưng dùng nút tải **từng dòng** và cùng tháng. Vi phạm review-checklist §A.1 ("TC đó mô phỏng **chính xác** steps reproduce"). — **Fix**: thêm `TC-FUNC001-01`.

- **[BLOCKER] FIX-SHAPE: GAP-2 — `CONC-001` (Cao) không có TC nào**: nút `領収書ダウンロード` là nút thực thi hành động quan trọng → kịch bản (1) **double-click** của `CONC-001` là bắt buộc. `REQ-009` của chính Studio cũng liệt kê *"bấm liên tiếp nút tải"* nhưng **không TC nào cover**. Rủi ro cụ thể: sau fix, node biên lai bị **huỷ rồi dựng lại**, double-click có thể khiến lần chụp thứ 2 chạy trên DOM đang huỷ dở → file trắng / thiếu trang / trùng trang. — **Fix**: thêm `TC-CONC001-01`.

- **[BLOCKER] FIX-SHAPE: GAP-3 — `REG-SHARED-001` / T2: màn Chi tiết hợp đồng không test trục gây bug**. `TC-REGSHARED001-01` tải 2 lần trên **cùng một hợp đồng** và chỉ đổi `宛名`. Chính `Ghi chú` của TC thừa nhận: *"trục thay đổi giữa hai lần tải ở đây là tên người nhận"*. Nhưng trục tương đương với "đổi tháng" ở màn kia là **đổi sang hợp đồng khác (id khác) mà không reload** — đúng chỗ dữ liệu nguồn đổi hoàn toàn, đúng chỗ bug gốc phát sinh. Feature T2 là **High risk** mà chỉ có 1 TC happy-path (AP-3). — **Fix**: thêm `TC-REGSHARED001-02` + `TC-REGSHARED001-03`.

- **[BLOCKER] FIX-SHAPE: GAP-4 — Claim "bịt luôn trường hợp lần tải trước hỏng giữa chừng" không có TC verify**. Mục 2 dev-impact nêu đây là lợi ích thứ 2 của fix. `REQ-009` cũng ghi *"khi request lấy dữ liệu thất bại ... không được hiển thị dấu hiệu thành công khi thực tế chưa có file"*. Không TC nào chặn request / tạo lỗi giữa chừng. Liên quan `OUT-TRUTH-001` (Cao) + `UI-003` (nâng Cao khi có rủi ro **false success**). — **Fix**: thêm `TC-OUTTRUTH001-03`.

- **[BLOCKER] `DEPLOY-ASSET-001` — "Cao tuyệt đối" nhưng verify ở sai môi trường và điều kiện then chốt chưa được xử lý**. Framework quy định `DEPLOY-ASSET-001` là **Cao tuyệt đối khi file bị sửa nằm trong luồng thanh toán** — đúng trường hợp này. `TC-DEPLOYASSET001-01` tick `Đạt` trên staging, trong khi `Ghi chú` của chính TC cảnh báo: *commit fix **KHÔNG** thay đổi `config/sns-line.php` version → trình duyệt khách F5 thường có thể vẫn chạy JS cũ*. Blade do server dựng nên tới ngay, JS thì không → **khách vẫn dính bug sau release**. — **Fix**: (1) yêu cầu Dev/DevOps xác nhận quy trình release có tự tăng version asset không, nếu không thì bump trước khi lên production; (2) chạy `TC-DEPLOYASSET001-02` trên production sau release.

### 4.2 Major (nên fix)

- **[MAJOR] `01-bug-task.md` + `03-dev-impact.md` auto-filled từ Redmine nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick** (cả 2 file). Review chỉ có giá trị sau khi tester đọc lại Redmine #39592 và xác nhận. Riêng file 03: bảng **4.1 (F1–F5) là do `/new-task` map lại** — báo cáo AI gốc ở mục 4.1 chỉ ghi *"File thay đổi"* chứ không ghi function, nên F1–F5 **chưa được người xác nhận**.

- **[MAJOR] Dev verify chỉ ở mức `lint`, chưa chạy trình duyệt lần nào** (`03-dev-impact.md` §6: container không có browser, không kết nối được MySQL dev). Toàn bộ rủi ro runtime của một fix **thuần runtime DOM** dồn sang QA — càng làm 2 BLOCKER về evidence/production nặng thêm.

- **[MAJOR] RULE-01 — Quan điểm ưu tiên Cao thiếu loại case, không ghi lý do**: `OUT-TRUTH-001` (2 TC, cả 2 Normal) · `REG-SHARED-001` (1 TC Normal) · `DEPLOY-ASSET-001` (1 TC Normal) · `FUNC-004` (1 TC Boundary, thiếu Normal + Abnormal). Cả bộ chỉ có **1 TC Abnormal / 13** (`TC-CONC003-01`) — tỷ lệ 9 : 1 : 3 lệch xa mức gợi ý của review-checklist §C.

- **[MAJOR] `FUNC-004` (Cao) — chỉ test 1/5 pattern biên**. `TC-FUNC004-01` test 11 giao dịch (biên+1). Thiếu: **đúng biên 10** (ranh giới sinh trang 2), **biên−1 = 9**, và **0 giao dịch**. Case 0 đặc biệt quan trọng vì Dev đã dựa vào nó để lập luận an toàn (*"handleTotalPagePdf trả về 1 ngay cả khi 0 bản ghi nên `#invoice_page_1` luôn xuất hiện, không có nguy cơ chờ hết 5 giây"*) — lập luận này **chưa từng được chạy thử**. — **Fix**: `TC-FUNC004-02`, `TC-FUNC004-03`.

- **[MAJOR] `BULK-001` (Cao) — thiếu Abnormal "chưa tick dòng nào"**. `個別発行` + `一括ダウンロード` đúng là tổ hợp bộ lọc + thao tác hàng loạt. `TC-SELECTSCOPE001-01` cover Normal tốt (đổi tập tick giữa 2 lần tải), nhưng `REQ-009` liệt kê *"khi chưa chọn dòng nào"* và không TC nào cover. — **Fix**: `TC-BULK001-01`.

- **[MAJOR] `CONC-003` — cover 2/5 kịch bản**. Có mạng chậm + chèn thao tác (kịch bản 3 phần nào). Thiếu: **chủ động delay 1 response rồi để nó về sau → UI phải bỏ qua response cũ** (kịch bản 4 — đúng bản chất bug này), và chuyển tab/filter liên tiếp (kịch bản 1, 5). — **Fix**: `TC-CONC003-02`.

- **[MAJOR] `DATA-COUNT-001` (Cao — lỗi lặp nhiều nhất lịch sử bug) chưa có TC đúng chuẩn**. Biên lai chứa `合計金額`, phần chịu thuế 10%, tiền thuế (`REQ-004` ghi rõ). 3 TC có chạm tổng tiền nhưng **không TC nào làm phép tính tay** cho thuế, và **không TC nào đối chiếu tổng của tháng trên bảng tổng hợp theo năm** với tổng trên PDF. — **Fix**: `TC-DATACOUNT001-01`.

- **[MAJOR] `OUT-EXPORT-001` (nâng Cao — "sinh file cho khách tải") chưa được duyệt**. Đặc biệt **`発行日`**: OEM mô tả bug là *"**ngày** của hóa đơn tải lần đầu bị áp dụng luôn cho cả các lần tải sau"* — tức KH nhìn thấy triệu chứng ở **trường ngày**. Chỉ `TC-FUNCSEQ001-01` và `TC-OUTTRUTH001-02` chạm nhẹ ("ngày phát hành là ngày thao tác"), không TC nào lấy `発行日` làm đối tượng verify chính khi tải 2 file liên tiếp. Chưa duyệt thêm: tên file khi tải 2 file liên tiếp trong 1 phiên (trùng tên `領収書.pdf`?). — **Fix**: `TC-OUTEXPORT001-01`.

- **[MAJOR] `UI-001` / `UI-002` — không TC nào ghi trình duyệt hoặc độ phân giải**. Biên lai được tạo bằng cách **chụp DOM đang render** (html2canvas **0.4.1**, bản rất cũ) → kết quả phụ thuộc trực tiếp vào engine render và viewport. `UIC-13` bắt buộc kiểm **1366×768** và **Mac Safari** (user chính là chủ salon/cửa hàng nhỏ). Không TC nào nêu. — **Fix**: `TC-UI002-01`.

- **[MAJOR] `PERF-LARGE-001` — quy mô test không có nguồn**. `TC-PERFLATENCY001-01` dùng "khoảng 100 giao dịch" nhưng không ghi nguồn; framework yêu cầu **tra số liệu khách hàng lớn nhất hiện tại**. Ngưỡng chờ chỉ 5 giây/trang và fix làm DOM phải dựng lại mỗi lần tải → đây là chỗ dễ gãy nhất ở khách lớn. — **Fix**: `TC-PERFLARGE001-01`.

- **[MAJOR] `UI-003` — thiếu 2/3 trạng thái**. Có trạng thái "sạch sau khi tải" (`TC-UI003-01`) và mạng chậm (`TC-CONC003-01`). Thiếu **danh sách rỗng** (tháng 0 giao dịch) và **ngắt kết nối**. Gộp fix chung với `TC-FUNC004-03` + `TC-OUTTRUTH001-03`.

- **[MAJOR] KH ghi "đã từng hỏi cùng vấn đề này trước đây" — chưa được truy vết**. Cần tra Redmine xem có ticket cũ cùng hiện tượng không. Nếu đây là **tái phát**, RULE-12 buộc mọi case đã từng `Không đạt` và được fix phải nằm trong bộ regression lần này; nếu là **report cũ chưa từng fix**, cần xác nhận root cause khi đó có trùng không. — **Fix**: Leader/QA tra ticket, ghi kết quả vào `01-bug-task.md`.

- **[MAJOR] `COMPAT-LEGACY-001` — cần hỏi Dev trước khi kết luận ×**. Hóa đơn của các tháng cũ có thể được sinh từ cấu trúc gói cước / thuế suất / định dạng bản ghi đời trước. Nếu có → RULE-09 buộc test **cả nhánh cũ và mới** (tải biên lai của tháng cũ nhất còn dữ liệu). Hiện mọi TC chỉ dùng 2026年06月 / 07月. — **Fix**: hỏi Dev; nếu có nhánh cũ thì bổ sung TC.

- **[MAJOR] 4 mã quan điểm không tồn tại trong `framework/checklist-lme.md`** → `/review-tc` không map được coverage tự động, và Leader không suy ra được **ưu tiên** (vốn suy từ mã quan điểm): `TOOL-KNOW-002` · `SELECT-SCOPE-001` · `PERF-LATENCY-001` · `RULE-06` (đây là **RULE**, không phải mã quan điểm). — **Fix**: map lại `TOOL-KNOW-002`→`FUNC-001`, `SELECT-SCOPE-001`→`BULK-001`, `PERF-LATENCY-001`→`PERF-LARGE-001`, `RULE-06`→`OUT-EXPORT-001`. Nếu Studio cần giữ mã riêng thì bổ sung dòng mapping vào framework (RULE-10).

### 4.3 Minor (có thể fix sau)

- **[MINOR] `Trạng thái đánh giá spec` trống 13/13** (`spec_status = null`). Với task này nhiều hành vi **spec không ghi** (quy tắc chia trang 10/20, `発行日`, làm tròn thuế) → phải ghi `Spec không ghi` + **nêu đã hỏi ai**, không được để trống rồi cho `Đạt`.
- **[MINOR] Không có link PR / diff** — chỉ có branch `ai_small_39592` + commit `233c4ae7b2`. Vẫn checkout được nên không chặn, nhưng nếu có diff link thì Leader verify được fix shape thật (AP-4).
- **[MINOR] File 04 không có bảng "Base quan điểm test LME" đã duyệt** — Studio trả `test_viewpoint_selection = null`, nên không có bằng chứng tầng 1 đã được duyệt từ trên xuống (RULE-03: mọi × phải có lý do). Bảng §7 F.1 dưới đây là do reviewer tự lập bù.
- **[MINOR] 9 `temp_id` bị xoá không để lại vết** (thiếu NEW-6, 7, 10, 12, 13, 14, 16, 21, 22 trong dải NEW-2…NEW-23). Không biết TC nào bị loại và vì sao — nếu có trục quan trọng bị cắt thì mất dấu. Đề nghị lấy `testcase_get_history` / changelog Studio.
- **[MINOR] `TC-OUTTRUTH001-02` có ký tự xuống dòng thừa ở cuối tiêu đề**; TC này cũng đã ở `version 5` — nên ghi lý do sửa nhiều lần vào `Ghi chú`.

### 4.4 Nit (gợi ý)

- **[NIT] `FUNC-SEQ-001` chuẩn yêu cầu F5 sau mỗi chuỗi thao tác** ("dữ liệu + thứ tự phải giống hệt trạng thái ngay sau thao tác"). Bộ TC cố tình **không** reload (đúng, vì reload làm bug biến mất) — nên bổ sung 1 TC riêng: sau chuỗi tải liên tiếp thì F5 rồi tải lại, xác nhận vẫn đúng.
- **[NIT] ADM-04** (§4 checklist-lme — "Bộ lọc theo tháng/năm ở màn thống kê phải đúng qua ranh giới đầu/cuối tháng", ticket #26876): liên quan gián tiếp vì màn này lọc theo tháng. Theo **RULE-11** mục này **chưa đủ bằng chứng**, chỉ nêu ở mức gợi ý — cân nhắc test biên tháng 12/2025→01/2026 (khác năm) khi có thời gian.
- **[NIT]** Cân nhắc gộp `TC-FUNCSEQ001-01` (tải cùng tháng 2 lần) vào `TC-FUNC004-02`, vì cùng verify "dựng lại không trùng/không thiếu dòng".

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` ở round tiếp theo. 16 cột canonical. `TC No.` không trùng file 04.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | FUNC-001 | Normal | Tái hiện ĐÚNG thao tác KH: tab 個別発行 + tick checkbox, tải tháng 7 rồi tháng 6 | - Account có giao dịch ở CẢ 2026年07月 và 2026年06月, tập giao dịch 2 tháng khác nhau rõ (khác số dòng + khác tổng tiền)<br>- Ghi sẵn ra giấy: số dòng + tổng tiền của từng tháng | 1. Mở `/basic/payment-history`<br>2. Bấm 「詳細を確認 >」 dòng 「2026年07月分」<br>3. Bật công tắc 「個別発行」<br>4. Tick checkbox của **tất cả** hóa đơn tháng 7<br>5. Bấm 「一括ダウンロード」 → nhập 宛名 「株式会社トライズ」 + 「御中」 → 「領収書ダウンロード」, chờ tải xong<br>6. **KHÔNG F5, không mở tab mới**: quay lại bảng theo năm, bấm 「詳細を確認 >」 dòng 「2026年06月分」<br>7. Bật 「個別発行」, tick checkbox tất cả hóa đơn tháng 6<br>8. Bấm 「一括ダウンロード」 → 「領収書ダウンロード」, chờ tải xong<br>9. Mở cả 2 file PDF, đối chiếu với số đã ghi ở tiền đề | Lần 1: 2026年07月, tick toàn bộ<br>Lần 2: 2026年06月, tick toàn bộ<br>宛名 = 「株式会社トライズ」, 敬称 = 「御中」 | File thứ 2 chứa đúng các giao dịch 2026年06月: số dòng = số dòng tháng 6 đã ghi, 合計金額 = tổng tháng 6 đã ghi, không dòng nào của tháng 7. File thứ 1 vẫn đúng tháng 7. 発行日 trên cả 2 file = ngày thao tác. | Chưa test | | **PRODUCTION** | | | | Spec ghi rõ | Lấp **GAP-1 / BLOCKER** — cover BUG (root cause). Đây là đường đi **đúng** steps KH+QA báo (`01-bug-task.md`), khác `TC-TOOLKNOW002-01` ở chỗ đi qua tab 個別発行 + tick checkbox. **Evidence bắt buộc: 2 file PDF thật + ảnh bảng chi tiết 2 tháng trên màn.** TUYỆT ĐỐI không reload giữa bước 5 và 6. |
| TC-CONC001-01 | CONC-001 | Abnormal | Double-click nút 領収書ダウンロード không sinh file lỗi hoặc trùng trang | - Account có ≥ 3 giao dịch trong 2026年06月<br>- Ghi sẵn số dòng + tổng tiền tháng 6 | 1. Mở `/basic/payment-history`, vào chi tiết 「2026年06月分」<br>2. Bấm 「一括ダウンロード」<br>3. Ở popup, **double-click nhanh** nút 「領収書ダウンロード」 (2 lần trong < 300ms)<br>4. Chờ mọi tiến trình kết thúc, kiểm **toàn bộ** file đã tải về trong thư mục Downloads<br>5. Mở DevTools > Console kiểm cảnh báo<br>6. Lặp lại với **triple-click** | Double-click nút 「領収書ダウンロード」, tháng 2026年06月 | Hoặc chỉ sinh **1 file**, hoặc sinh nhiều file **giống hệt nhau** — mọi file đều đủ số dòng và đúng 合計金額 của tháng 6. Tuyệt đối không có file: trắng, thiếu trang, trùng trang, hoặc lẫn dữ liệu. Popup đóng và lớp phủ tắt sau khi xong. Không có lỗi JS trên console. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Dev/Leader** | Lấp **GAP-2 / BLOCKER** — `CONC-001` kịch bản (1), cover F1+F2. Rủi ro cụ thể sau fix: node bị `v-if` huỷ rồi dựng lại, click thứ 2 có thể chụp DOM đang huỷ dở. `REQ-009` của Studio có nêu "bấm liên tiếp nút tải" nhưng chưa có TC. **Evidence: toàn bộ file trong Downloads + ảnh console.** |
| TC-BULK001-01 | BULK-001 | Abnormal | Bấm 一括ダウンロード khi chưa tick dòng nào phải chặn, không sinh file rỗng | - Account có ≥ 3 giao dịch trong 2026年06月 | 1. Vào chi tiết 「2026年06月分」, bật 「個別発行」<br>2. **Không tick dòng nào**<br>3. Bấm 「一括ダウンロード」<br>4. Nếu popup mở được thì bấm 「領収書ダウンロード」<br>5. Kiểm thư mục Downloads và trạng thái màn hình<br>6. Sau đó tick 2 dòng và tải lại bình thường | Tick 0 dòng, sau đó tick 2 dòng | Hệ thống chặn ở bước 3 hoặc 4 với **thông báo rõ ràng** (VD "chưa chọn hóa đơn"), **không sinh file**, không sinh file 0 dòng, không báo thành công giả. Lớp phủ không treo. Lần tải sau khi tick 2 dòng vẫn ra đúng 2 dòng đó — trạng thái lỗi trước không để lại rác trong trang. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Dev/Leader** | Lấp GAP `BULK-001` (Cao) Abnormal + `REQ-009` mục "chưa chọn dòng nào". Cover F1. **Evidence: ảnh thông báo + ảnh thư mục Downloads chứng minh không có file mới.** |
| TC-REGSHARED001-02 | REG-SHARED-001 | Normal | Chi tiết hợp đồng: tải biên lai hợp đồng A rồi hợp đồng B không reload ra đúng từng hợp đồng | - Account có **≥ 2 hợp đồng khác nhau**, mỗi hợp đồng có lịch sử thanh toán khác nhau rõ rệt (khác số kỳ + khác tổng tiền)<br>- Ghi sẵn số kỳ + tổng tiền của từng hợp đồng | 1. Mở danh sách hợp đồng, vào chi tiết **hợp đồng A** (`/basic/detail-contract/{idA}`)<br>2. Bấm 「過去決済分の領収書ダウンロード」 → nhập 宛名 「株式会社テストＡ」 → 「領収書ダウンロード」, chờ tải xong<br>3. **KHÔNG F5**: điều hướng sang chi tiết **hợp đồng B** (`/basic/detail-contract/{idB}`) bằng menu/link trong màn<br>4. Bấm 「過去決済分の領収書ダウンロード」 → nhập 宛名 「株式会社テストＢ」 → 「領収書ダウンロード」, chờ tải xong<br>5. Mở cả 2 file, đối chiếu với số đã ghi<br>6. Lặp lại theo chiều ngược lại (B trước, A sau) | Hợp đồng A rồi hợp đồng B, không reload; 宛名 khác nhau mỗi lần | File thứ 2 chứa **đúng và đủ** lịch sử thanh toán của **hợp đồng B**: số kỳ = số kỳ B, tổng tiền = tổng B, không kỳ nào của hợp đồng A. Tên hiển thị 「株式会社テストＢ 御中」. Chiều ngược lại cho kết quả đối xứng. | Chưa test | | **PRODUCTION** | | | | Spec ghi rõ | Lấp **GAP-3 / BLOCKER** — cover T2 (FA-031, High risk) + F5. `TC-REGSHARED001-01` chỉ đổi 宛名 trên **cùng 1 hợp đồng**, không tái lập trục "dữ liệu nguồn đổi giữa 2 lần tải" vốn là bản chất bug. **Nếu điều hướng giữa 2 hợp đồng bắt buộc reload trang** thì ghi rõ vào Ghi chú và TC này chuyển thành xác nhận "không tái hiện được do có reload". **Evidence: 2 file PDF + ảnh màn chi tiết từng hợp đồng.** |
| TC-REGSHARED001-03 | REG-SHARED-001 | Abnormal | Chi tiết hợp đồng ở trạng thái biên: 0 kỳ thanh toán và hợp đồng đã hủy | - Có 1 hợp đồng **chưa phát sinh kỳ thanh toán nào**<br>- Có 1 hợp đồng **đã hủy** nhưng còn lịch sử thanh toán cũ | 1. Vào chi tiết hợp đồng **chưa có kỳ thanh toán nào**<br>2. Bấm 「過去決済分の領収書ダウンロード」 → 「領収書ダウンロード」<br>3. Ghi lại hành vi (chặn / file rỗng / lỗi)<br>4. **Không reload**, điều hướng sang hợp đồng **đã hủy** còn lịch sử<br>5. Bấm 「過去決済分の領収書ダウンロード」 → 「領収書ダウンロード」<br>6. Kiểm nội dung file và trạng thái màn hình | Hợp đồng 0 kỳ; hợp đồng đã hủy có lịch sử | Hợp đồng 0 kỳ: chặn có thông báo rõ **hoặc** ra file 1 trang không có dòng nào và 合計 = 0 — theo spec, **không** treo lớp phủ, **không** báo thành công giả. Hợp đồng đã hủy: file chứa đúng lịch sử thanh toán của chính nó, **không** dính dữ liệu của hợp đồng ở bước 2. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Dev/Leader** | Lấp AP-3 (T2 chỉ có happy-path). Cover T2 + F5 + `UI-003` trạng thái rỗng. regression. **Evidence: file PDF (nếu có) + ảnh thông báo + ảnh màn sau thao tác.** |
| TC-OUTTRUTH001-03 | OUT-TRUTH-001 | Abnormal | Lần tải hỏng giữa chừng không để lại khối biên lai cũ và lần tải kế tiếp vẫn đúng | - Account có giao dịch ở CẢ 2026年07月 và 2026年06月<br>- DevTools mở sẵn thẻ Network để chặn request | 1. Vào chi tiết 「2026年07月分」<br>2. Trong DevTools > Network bật **Block request** cho endpoint lấy lịch sử thanh toán (hoặc bật Offline)<br>3. Bấm 「一括ダウンロード」 → 「領収書ダウンロード」<br>4. Quan sát: có báo lỗi không, lớp phủ có tắt không, có file nào được tải không<br>5. **Bỏ chặn request. KHÔNG F5.**<br>6. Chuyển sang 「2026年06月分」, bấm 「一括ダウンロード」 → 「領収書ダウンロード」<br>7. Mở file tải ở bước 6 và đối chiếu bảng chi tiết tháng 6 trên màn | Lần 1: chặn request (thất bại). Lần 2: bình thường, tháng 2026年06月 | Bước 3-4: hệ thống báo **lỗi đúng nguyên nhân**, **không** hiện thông báo thành công, **không** sinh file, lớp phủ tắt trong thời gian hợp lý (không loading vô hạn). Bước 6-7: file tải được chứa **đúng** dữ liệu tháng 6 — lần hỏng trước **không** để lại khối biên lai cũ trong trang. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Dev/Leader** | Lấp **GAP-4 / BLOCKER** — verify trực tiếp claim ở mục 2 dev-impact ("bịt luôn trường hợp lần tải trước hỏng giữa chừng") + `REQ-009` mục "request lấy dữ liệu thất bại". Cover F1+F2, `UI-003` nhánh lỗi. **Evidence: ảnh thông báo lỗi + ảnh Network + file PDF bước 6.** |
| TC-FUNC004-02 | FUNC-004 | Boundary | Tháng có ĐÚNG 10 giao dịch ra đúng 1 trang, không sinh trang 2 rỗng | - Dựng dữ liệu để 1 tháng có **đúng 10** giao dịch, số tiền khác nhau để phân biệt dòng | 1. Vào chi tiết tháng đã dựng 10 giao dịch<br>2. Xác nhận bảng trên màn hiển thị đúng 10 dòng<br>3. Bấm 「一括ダウンロード」 → 「領収書ダウンロード」, chờ tải xong<br>4. Kiểm số trang và số dòng của file<br>5. **Không reload**, tải lại lần 2 cùng tháng và kiểm lại | Tháng có đúng 10 giao dịch | File có **đúng 1 trang** chứa đủ 10 dòng, **không** sinh trang 2 rỗng, **không** hiện dòng 「次ページに続く」, 合計 = tổng 10 giao dịch. Lần tải thứ 2 ra file giống hệt lần 1. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Dev** (quy tắc 10/20 chưa có trong spec) | Lấp GAP `FUNC-004` pattern **đúng biên**. Cover F2+F3. Bổ trợ `TC-FUNC004-01` (biên+1 = 11). Nếu dựng được thêm 9 giao dịch thì chạy luôn pattern biên−1. **Evidence: file PDF + ảnh bảng 10 dòng trên màn.** |
| TC-FUNC004-03 | FUNC-004 | Boundary | Tháng có 0 giao dịch không treo lớp phủ và không để lại biên lai của tháng trước | - Có 1 tháng **không phát sinh giao dịch nào**<br>- Có 1 tháng khác có ≥ 3 giao dịch | 1. Vào chi tiết tháng **có giao dịch**, tải biên lai bình thường, chờ xong<br>2. **KHÔNG reload**, chuyển sang tháng **0 giao dịch**<br>3. Bấm 「一括ダウンロード」 → 「領収書ダウンロード」<br>4. Bấm giờ, quan sát lớp phủ và popup tối đa 30 giây<br>5. Kiểm file tải về (nếu có) và console | Tháng 0 giao dịch, tải ngay sau 1 tháng có giao dịch | Hệ thống chặn có thông báo rõ **hoặc** ra file 1 trang không dòng nào với 合計 = 0 — theo spec. Tuyệt đối **không** ra file chứa dòng của tháng trước. Popup đóng, lớp phủ tắt trong ngưỡng 5 giây, **không** có cảnh báo 「Timeout: Element ...」 trên console. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Dev** | Lấp GAP `FUNC-004` pattern **0** + `UI-003` trạng thái rỗng. Verify trực tiếp lập luận của Dev ("handleTotalPagePdf trả về 1 ngay cả khi 0 bản ghi") mà Dev **chưa từng chạy thử**. **Evidence: file PDF (nếu có) + ảnh console + ảnh màn sau 30s.** |
| TC-DEPLOYASSET001-02 | DEPLOY-ASSET-001 | Normal | Sau release PRODUCTION, F5 thường vẫn nạp JS mới và tải hóa đơn đúng tháng | - Bản fix đã lên lịch release lên `step.lme.jp`<br>- Có account thật có giao dịch ở 2 tháng liên tiếp<br>- **Trước release** đã mở sẵn 1 tab và tải 1 lần để browser cache JS bản cũ | 1. Trước release: mở `/basic/payment-history` trên production, tải 1 lần biên lai để cache asset<br>2. Giữ nguyên tab, **không** đóng browser, **không** xóa cache<br>3. Release bản fix lên production<br>4. Trên chính tab cũ bấm **F5 thường** (KHÔNG Ctrl+F5)<br>5. DevTools > Network: tìm `mixins/invoices.js`, ghi lại **query version** và status code<br>6. Xác nhận nội dung file JS đã là bản mới (có `$nextTick`)<br>7. Chạy kịch bản tải tháng A rồi tháng B không reload, kiểm file thứ 2 | Tab giữ cache bản cũ; sau release chỉ F5 thường | `mixins/invoices.js` trả **200** với **query version ĐÃ ĐỔI** so với trước release, nội dung là bản mới. Không asset nào 404. Không lỗi JS trên console. Kịch bản tải 2 tháng liên tiếp cho file thứ 2 đúng tháng B. | Chưa test | | **PRODUCTION** | | | | Spec ghi rõ | Lấp **BLOCKER `DEPLOY-ASSET-001`** — `TC-DEPLOYASSET001-01` chạy staging nên không kết luận được. ⚠️ **Chốt với Dev/DevOps TRƯỚC release**: commit `233c4ae7b2` không sửa `config/sns-line.php` version → nếu quy trình release không tự tăng, phải bump tay, nếu không **khách F5 thường vẫn dính bug**. **Evidence: ảnh DevTools Network trước và sau release (thấy query version đổi) + file PDF bước 7.** |
| TC-ENV003-01 | ENV-003 | Normal | Chạy lại trục chính trên PRODUCTION với account thật (RULE-08 bill tiền) | - Account **thật** trên `step.lme.jp` có giao dịch ở 2 tháng liên tiếp<br>- Đã được duyệt thao tác trên production, **chỉ đọc và tải file**, không tạo/xóa dữ liệu | 1. Đăng nhập `step.lme.jp`, mở `/basic/payment-history`<br>2. Ghi lại số dòng + tổng tiền của 2 tháng liên tiếp từ bảng chi tiết<br>3. Tải biên lai tháng gần nhất, chờ xong<br>4. **KHÔNG reload**, chuyển sang tháng liền trước, tải tiếp<br>5. Mở cả 2 file, đối chiếu với số đã ghi ở bước 2<br>6. Lặp lại kịch bản trên màn Chi tiết hợp đồng với 2 hợp đồng khác nhau | 2 tháng liên tiếp có dữ liệu thật; không tạo/sửa/xóa dữ liệu | Cả 2 file khớp **100%** bảng chi tiết của đúng tháng tương ứng trên production (số dòng, từng dòng, 合計金額, số trang). Kết quả trên production giống staging. | Chưa test | | **PRODUCTION** | | | | Spec ghi rõ | Lấp **BLOCKER RULE-08** — bill tiền không được kết luận từ staging (Catalog D: production dùng account thật, tách domain, loadbalance 2 server). Cover BUG + T1 + T2. **Evidence: 2 file PDF production + ảnh bảng chi tiết.** ⚠️ Chỉ thao tác đọc/tải — tuyệt đối không tạo hay xóa dữ liệu thật. |
| TC-DATACOUNT001-01 | DATA-COUNT-001 | Normal | Đối chiếu phép tính tay 合計・10%対象・消費税 giữa bảng năm, bảng tháng và file PDF | - 1 tháng có 3-5 giao dịch với số tiền **khác nhau và biết trước**<br>- Chuẩn bị sẵn máy tính để tính tay | 1. Mở `/basic/payment-history`, ghi lại tổng tiền của tháng T hiển thị trên **bảng tổng hợp theo năm**<br>2. Vào chi tiết tháng T, ghi lại **từng dòng** và tổng trên **bảng chi tiết**<br>3. Tính tay: tổng các dòng, phần chịu thuế 10%, tiền thuế<br>4. Tải biên lai tháng T<br>5. Mở file, ghi lại 合計金額, phần chịu thuế 10%, 消費税 trong bảng 内訳<br>6. Lập bảng đối chiếu 3 nguồn: bảng năm / bảng tháng / file PDF / phép tính tay | VD 3 giao dịch: 11.000 + 5.500 + 3.300 = 19.800円<br>Phép tính tay: 10%対象 = 18.000, 消費税 = 1.800, 合計 = 19.800 | **Cả 3 nguồn khớp nhau và khớp phép tính tay** đến từng đồng: tổng tháng T trên bảng năm = tổng trên bảng chi tiết = 合計金額 trên PDF. 消費税 và phần chịu thuế 10% trên PDF khớp phép tính tay, không sai số làm tròn. | Chưa test | | **PRODUCTION** | | | | Spec không ghi — **hỏi Dev** (quy tắc làm tròn thuế) | Lấp GAP `DATA-COUNT-001` (Cao — 12 ticket Closed trong lịch sử bug). Cover `REQ-004`. **Evidence: bảng đối chiếu 3 nguồn + phép tính tay + file PDF + ảnh bảng năm và bảng tháng.** |
| TC-OUTEXPORT001-01 | OUT-EXPORT-001 | Normal | 発行日 và tên file của 2 lần tải liên tiếp không bị dính giá trị lần trước | - Account có giao dịch ở 2 tháng khác nhau<br>- Thư mục Downloads đã dọn sạch file 領収書 cũ | 1. Vào chi tiết tháng A, tải biên lai, chờ xong<br>2. Ghi lại **tên file** và **発行日** in trên file<br>3. **KHÔNG reload**, chuyển sang tháng B, tải biên lai<br>4. Ghi lại tên file và 発行日 của file thứ 2<br>5. So sánh 2 file: 発行日, tên người nhận, dữ liệu giao dịch<br>6. Kiểm thư mục Downloads xem 2 file có phân biệt được không | Tháng A rồi tháng B trong cùng phiên | **発行日 trên cả 2 file = ngày thao tác thật**, file thứ 2 **không** giữ 発行日 của file thứ 1. Hai file phân biệt được trong Downloads (tên khác nhau hoặc có hậu tố), không file nào ghi đè file kia. Dữ liệu giao dịch mỗi file đúng tháng của nó. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Dev** (quy tắc đặt tên file + 発行日) | Lấp GAP `OUT-EXPORT-001` (nâng Cao — "sinh file cho khách tải"). **Trục 発行日 chính là thứ OEM 沖原裕樹 mô tả**: *"ngày của hóa đơn tải lần đầu bị áp dụng luôn cho cả các lần tải sau đó"* — hiện chưa TC nào lấy 発行日 làm đối tượng verify chính. **Evidence: 2 file PDF + ảnh thư mục Downloads.** |
| TC-CONC003-02 | CONC-003 | Abnormal | Response của tháng cũ về sau khi đã đổi tháng phải bị bỏ qua | - 2 tháng đều có giao dịch, dữ liệu khác nhau rõ<br>- DevTools mở sẵn, biết cách throttle/delay từng request | 1. Trong DevTools bật throttling **Slow 3G** cho endpoint lấy lịch sử thanh toán<br>2. Vào chi tiết tháng A, bấm 「一括ダウンロード」 → 「領収書ダウンロード」<br>3. **Ngay khi request tháng A còn pending**, chuyển sang tháng B và bấm 「一括ダウンロード」 → 「領収書ダウンロード」<br>4. Trong Network, xác nhận response tháng A về **SAU** response tháng B<br>5. Chờ mọi tiến trình kết thúc, kiểm **toàn bộ** file trong Downloads<br>6. Kiểm nội dung màn hình sau khi xong | Tháng A (delay), tháng B chèn vào giữa; response A về sau B | **Không file nào trộn dữ liệu 2 tháng.** Mỗi file tải được chứa trọn vẹn dữ liệu của **đúng** tháng được yêu cầu. Response cũ về muộn **không** ghi đè nội dung đang hiển thị của tháng B. Popup/lớp phủ kết thúc, màn hình thao tác tiếp được. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Dev/Leader** | Lấp GAP `CONC-003` kịch bản (4) — đúng bản chất bug (dùng lại state cũ). Bổ trợ `TC-CONC003-01` (mới cover kịch bản 3). Cover F1. **Evidence: video thao tác + ảnh Network thể hiện thứ tự response + toàn bộ file Downloads.** |
| TC-UI002-01 | UI-002 | Normal | Trục chính chạy đúng trên Mac Safari, Windows Chrome và ở 1366×768 | - Có máy Mac (Safari + Chrome) và máy Windows (Chrome)<br>- Account có giao dịch ở 2 tháng liên tiếp | 1. Trên **Windows Chrome** ở độ phân giải **1366×768**: chạy kịch bản tải tháng A rồi tháng B không reload, mở file kiểm<br>2. Trên **Mac Safari**: chạy lại đúng kịch bản đó<br>3. Trên **Mac Chrome**: chạy lại đúng kịch bản đó<br>4. Với mỗi trình duyệt: mở file PDF và kiểm bố cục bảng 内訳, chữ tiếng Nhật, số trang<br>5. Lập bảng so sánh 3 trình duyệt | Cùng 1 kịch bản, 3 tổ hợp trình duyệt/OS; viewport 1366×768 | Cả 3 tổ hợp: file thứ 2 chứa đúng dữ liệu tháng B. Bố cục bảng 内訳 trong PDF **không** bị cắt cột hay lệch giữa các trình duyệt. Chữ tiếng Nhật rõ, không lỗi font. Ở 1366×768 khối biên lai được chụp **không** bị co/cắt so với 1920. | Chưa test | | STAGING | | | | Spec không ghi — **hỏi Leader** | Lấp GAP `UI-001` + `UI-002` + `UIC-13`. Lý do bắt buộc: biên lai được tạo bằng cách **chụp DOM đang render** (html2canvas **0.4.1**, bản rất cũ) → kết quả phụ thuộc engine render và viewport. User chính là chủ salon/cửa hàng nhỏ, dùng **Safari** nhiều. **Evidence: 3 file PDF từ 3 trình duyệt + ảnh màn ở 1366×768.** |
| TC-PERFLARGE001-01 | PERF-LARGE-001 | Boundary | Tải biên lai ở quy mô khách hàng lớn nhất THỰC TẾ không vượt ngưỡng chờ | - **Đã tra và ghi rõ nguồn**: số giao dịch/tháng lớn nhất của khách hàng thực tế hiện nay = `<N>` (hỏi Dev/PM, ghi vào Ghi chú)<br>- Dựng tháng có ≥ `N` giao dịch | 1. Mở chi tiết tháng đã dựng ≥ `N` giao dịch<br>2. Mở DevTools > Console<br>3. Bấm 「一括ダウンロード」 → 「領収書ダウンロード」, **bấm giờ**<br>4. Theo dõi tới khi có file hoặc quá 60 giây<br>5. Kiểm số trang, số dòng của file và cảnh báo trên console<br>6. **Không reload**, tải lần 2 cùng tháng, đo lại thời gian | Số giao dịch = quy mô khách lớn nhất thực tế `<N>` (ghi rõ nguồn số liệu) | File được tạo **đủ số trang và đủ số dòng** = `N`. Popup đóng, lớp phủ tắt. **Không** có cảnh báo 「Timeout: Element ...」 trên console. Ghi lại thời gian cả 2 lần tải; lần 2 **không** chậm hơn đáng kể lần 1 (fix làm DOM dựng lại mỗi lần). | Chưa test | | **PRODUCTION** | | | | Spec không ghi — **hỏi Dev/PM** (nguồn quy mô) | Nâng cấp `TC-PERFLATENCY001-01` (dùng "khoảng 100 giao dịch" **không ghi nguồn**). Framework `PERF-LARGE-001` buộc tra quy mô khách lớn nhất. Điểm gãy: `waitForElement` chỉ chờ **5 giây/trang**, quá ngưỡng thì chỉ log rồi dừng → không có file, popup treo. **Evidence: số liệu nguồn quy mô + ảnh console + thời gian đo + file PDF.** |

> **Ưu tiên chạy trước**: `TC-FUNC001-01` → `TC-ENV003-01` → `TC-REGSHARED001-02` → `TC-CONC001-01` → `TC-OUTTRUTH001-03` → `TC-DEPLOYASSET001-02` (6 TC lấp BLOCKER). Các TC còn lại lấp MAJOR.

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - **Section**: `templates/LME-SYSTEM-SPEC.md` — FS-009 Payment History / FA-031 Contract Plan & Payment (hiện **không có** `02-spec-reference.md` cho task này).
  - **Nội dung cần update** — 4 hành vi đang **không có nguồn spec**, khiến 13/13 TC để trống `Trạng thái đánh giá spec` và QA có nguy cơ tự suy diễn rồi cho `Đạt`:
    1. **Quy tắc chia trang biên lai** — trang đầu tối đa 10 giao dịch, trang sau tối đa 20 (hiện chỉ suy từ code `handleTotalPagePdf`, không có spec).
    2. **Hành vi khi tháng có 0 giao dịch** — chặn có thông báo, hay ra file 1 trang với 合計 = 0?
    3. **Hành vi khi chưa tick dòng nào** ở chế độ `個別発行` rồi bấm `一括ダウンロード`.
    4. **`発行日` và quy tắc đặt tên file** khi tải nhiều biên lai liên tiếp trong cùng phiên + **quy tắc làm tròn** phần chịu thuế 10% / 消費税.
  - **Người chịu trách nhiệm update**: `<PM / Leader phân công>`

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — chạy đủ A.1→A.6. **A.1 FAIL** (không TC nào mô phỏng chính xác steps KH), A.2/A.3/A.4 RISK, **A.5 PASS** (không orphan), **A.6 FAIL** (fix-shape còn 4 trigger chưa cover).
- [x] **B. Chất lượng từng TC** — **PASS**. Title có keyword, precondition dựng được env, steps tuần tự, expected đo lường được (số dòng / tổng tiền / số trang cụ thể). Không TC nào dùng data giả `"test"`/`"abc"`.
- [x] **C. Chất lượng bộ TC** — **FAIL**. Tỷ lệ Normal:Abnormal:Boundary = **9 : 1 : 3**, lệch xa mức gợi ý; **0 TC** cho role/permission; **0 TC** ghi trình duyệt/độ phân giải; không TC trùng lặp.
- [x] **D. Spec alignment** — **Không đánh giá được** (thiếu `02-spec-reference.md`) → xem §6.
- [x] **E. Hành chính** — **RISK**. File đúng folder, `TC No.` đúng format `TC-<mã>-<nn>`; nhưng **4 mã quan điểm không tồn tại trong framework**, `Trạng thái đánh giá spec` trống 13/13, và TC ở trạng thái `draft` chưa duyệt trên Studio.
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới. **Không** dùng §4 checklist-lme (FORM-01/CHAT-01/ADM-*/TPL-01) để flag BLOCKER/MAJOR (RULE-11) — ADM-04 chỉ nêu ở `[NIT]`.
  - [x] F.2 Catalog (tầng 2) — **B** (UIC-02 nút disable, UIC-05 modal, UIC-11 loading/rỗng/lỗi, **UIC-13 độ phân giải 1366×768 + Safari**, UIC-15 asset/font) · **C.7 bill tiền** (MAP-PAY-01) · **D** (bill tiền → production, loadbalance 2 server) · A/E không trigger (không có ô nhập nghiệp vụ mới, không upload media).
  - [x] F.3 RULE quy trình — **RULE-01 FAIL** · **RULE-02 FAIL** · RULE-03 không đánh giá được (không có bảng duyệt quan điểm) · RULE-06 PASS (`TC-RULE06-01` đi tới file PDF thật) · RULE-07 N/A (không CRUD) · **RULE-08 FAIL** · RULE-09 chưa xác định (cần hỏi Dev) · RULE-12 chưa xác định (cần tra ticket cũ KH nhắc tới).

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ luôn bắt buộc | TC-TOOLKNOW002-01, TC-FUNCSEQ001-01, TC-RULE06-01 | **RISK** — luồng chính có TC nhưng **không đi đúng đường KH báo** → xem GAP-1 |
| `FUNC-004` | Cao | ◯ giới hạn số giao dịch/trang | TC-FUNC004-01 | **RISK** — 1/5 pattern biên (chỉ biên+1) |
| `FUNC-SEQ-001` | Trung bình | ◯ ≥2 thao tác liên tiếp trên cùng danh sách | TC-FUNCSEQ001-01, TC-FUNCSEQ001-02 | **OK** — thiếu bước F5 sau chuỗi (`[NIT]`) |
| `CONC-001` | **Cao** | ◯ nút thực thi hành động quan trọng | — | **GAP → [BLOCKER]** |
| `CONC-003` | Cao (màn nhiều request + đổi tab) | ◯ | TC-CONC003-01 | **RISK** — 2/5 kịch bản |
| `DATA-COUNT-001` | **Cao** | ◯ biên lai có 合計・消費税・tỷ lệ 10% | TC-SELECTSCOPE001-01, TC-FUNC004-01, TC-RULE06-01 | **RISK** — chạm tổng tiền nhưng **không phép tính tay thuế**, không đối chiếu bảng năm |
| `DATA-CACHE-001` | Cao (output user-facing) | ◯ release đổi JS | TC-DEPLOYASSET001-01 | **RISK** — chỉ staging |
| `OUT-TRUTH-001` | **Cao** | ◯ mọi thao tác có thông báo kết quả | TC-OUTTRUTH001-01, TC-OUTTRUTH001-02 | **RISK** — 2 TC đều Normal, **thiếu nhánh false-success** → GAP-4 |
| `OUT-EXPORT-001` | Cao (sinh file cho khách tải) | ◯ | TC-RULE06-01 (một phần) | **RISK** — thiếu 発行日, tên file, giá trị 0 |
| `UI-003` | Cao (rủi ro false success) | ◯ | TC-UI003-01 | **RISK** — 1/3 trạng thái (thiếu rỗng + ngắt kết nối) |
| `UI-001` | Trung bình | ◯ mọi chức năng có UI | — | **GAP → [MAJOR]** (thiếu 1366×768) |
| `UI-002` | Trung bình | ◯ UI user-facing, canvas phụ thuộc engine | — | **GAP → [MAJOR]** (thiếu Mac Safari) |
| `REG-SHARED-001` | **Cao** | ◯ mixin + blade dùng chung 2 màn | TC-REGSHARED001-01 | **RISK cận GAP → [BLOCKER]** — không test trục "đổi hợp đồng" |
| `DEPLOY-ASSET-001` | **Cao tuyệt đối** (file trong luồng thanh toán) | ◯ | TC-DEPLOYASSET001-01 | **RISK → [BLOCKER]** — chạy staging, version asset chưa bump |
| `ENV-003` | **Cao** | ◯ bill tiền | — | **GAP → [BLOCKER]** (RULE-08) |
| `PERF-LARGE-001` | Cao (export/file) | ◯ | TC-PERFLATENCY001-01 | **RISK** — quy mô không ghi nguồn |
| `BULK-001` | **Cao** | ◯ `個別発行` tick + `一括ダウンロード` | TC-SELECTSCOPE001-01 | **RISK** — thiếu Abnormal "chưa tick dòng nào" |
| `COMPAT-LEGACY-001` | Cao | **?** — cần hỏi Dev (hóa đơn tháng cũ có cấu trúc giá/thuế đời trước không) | — | **Chưa xác định → [MAJOR] hỏi Dev** |
| `REG-RUN-001` | Cao | × — fix thuần client, không có job/dữ liệu chạy dở bị ảnh hưởng | — | × có lý do |
| `DEPLOY-LIVE-001` | Cao | × — không đổi payload API / cấu trúc request; server không bị sửa | — | × có lý do |
| `DATA-DB-001` / `DATA-AUDIT-001` / `DATA-REF-001` / `DATA-BACKUP-001` / `DATA-MIG-001` | Cao | × — **không có UPDATE/DELETE, không chạm bảng DB** (mục 4.2 = không có data) | — | × có lý do |
| `PAY-STATE-001` / `PAY-AMOUNT-001` / `PAY-PLAN-001` / `PAY-BATCH-001` / `PAY-ABANDON-001` / `PAY-LIMIT-001` | Cao | × — không phát sinh giao dịch, không đổi trạng thái hợp đồng; chỉ **hiển thị lại** dữ liệu thanh toán đã có. Độ chính xác số tiền trên biên lai xét ở `DATA-COUNT-001` | — | × có lý do |
| `PERM-001` / `PERM-002` | Cao | **?** — spec chưa nói màn hóa đơn có phân quyền theo role không | — | **Chưa xác định — hỏi Dev/PM**, nếu có role hạn chế thì phải bổ sung TC |
| `MSG-*` / `LIFF-ENTRY-001` / `FRIEND-001` / `INTG-*` / `JOB-001` / `MEDIA-*` / `STATE-*` / `SEC-*` / `NOTI-MAIL-001` / `SYNC-APP-001` / `LIST-001` | — | × — task không gửi tin, không phát sinh URL cho LINE user, không upload media, không job nền, không đổi trạng thái nhiều bước, không chạm credential/PII cross-account, không có app | — | × có lý do |

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
