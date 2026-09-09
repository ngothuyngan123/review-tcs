# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38957 — Khi mua hợp đồng thành công cần redirect sang router bill success trước sau đó mới quay về màn bill thành công` |
| Reviewer (Leader) | `<Leader điền>` |
| Tester được review | `<không xác định — 04-tc-list.md là slice fetch trực tiếp từ sheet master "Màn hình bill tiền", không có cột Người thực hiện>` |
| Ngày review | 2026-07-29 |
| Version TCs | Fetch từ Google Sheet `TCsLine_Bill tiền_Improve2025` › tab "Màn hình bill tiền" (gid `412698763`), rows 257–315, lúc 2026-07-29 |
| Vòng review | Round 1 |

---

## 1. Verdict

- [ ] APPROVED
- [ ] APPROVED WITH CHANGES
- [x] **REJECTED** — Có issue BLOCKER, cần Dev xác nhận phạm vi ảnh hưởng + bổ sung TC trước khi review vòng 2.

**Lý do ngắn gọn**: Bộ TC hiện có (59 case, đã có sẵn từ sheet master) cover Normal khá tốt, vượt cả phạm vi Dev nêu trong `03-dev-impact.md`, nhưng (1) Dev chưa xác nhận bằng văn bản các luồng "bill lại hợp đồng" ngoài 2 luồng đã nêu có dùng chung code path đã fix hay không, và (2) không có bất kỳ TC nào test kịch bản gián đoạn giữa 2 bước của chính cách fix (redirect → back step) — đúng loại rủi ro cách fix 2-bước-tuần-tự dễ mắc nhất.

---

## 2. Tóm tắt cho member

Bộ 59 TC fetch từ sheet master "Màn hình bill tiền" cover rất đầy đủ các luồng nghiệp vụ redirect (mua mới / upgrade / bill lại overdue card / overdue transfer / đã hủy / extend / campaign × standard/pro × tháng/năm) + có case negative "không bill tiền → không redirect" — đây là điểm mạnh thật sự, vượt xa phạm vi 2 luồng Dev nêu trong `03-dev-impact.md` mục 4.3. Tuy nhiên bộ TC này thiên hoàn toàn về Normal (đúng URL, đúng luồng); chưa có case nào test việc **gián đoạn** giữa lúc bill thành công và lúc redirect hoàn tất (đóng tab/mất mạng/back/F5) — đây chính là rủi ro cách fix mới thêm vào (2 bước tuần tự: redirect rồi mới back step). Cần bổ sung 7 TC (xem §5) + Dev confirm phạm vi ảnh hưởng đầy đủ trước khi duyệt.

---

## 3. Coverage Matrix

> Coverage matrix dựa trên impact liệt kê ở `03-dev-impact.md` (mục 4.1/4.3; mục 4.2 = "Không có" nên không có dòng Data).

| Impact | Loại | Priority Dev đánh giá | TCs cover (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause: thiếu bước redirect trước khi vào step success) | Fix | — | Rows 257–261 ("Check redirect khi mua mới hợp đồng") tái hiện trực tiếp root cause | 5 | OK |
| F1 — `created()` (bill_tool/index.js) | Function Direct | — | Toàn bộ 48 TC nhóm 1–7 (mọi redirect đều qua hàm này khi bill thành công) | 48 | OK (Normal) — không có Abnormal/Boundary riêng cho hàm này |
| F2 — `univapayTokenHandler()` (bill_tool/index.js) | Function Direct | — | Các TC ghi rõ "Bill card" (nhóm 1–3, thanh toán qua card/Univapay) | ~29 | OK (Normal) — không có Abnormal/Boundary riêng |
| F3 — view `payment_bot_success.blade.php` | Function Direct | — | Toàn bộ 48 TC (view này render khi redirect tới `*_success`) | 48 | OK |
| D1 — (không có data impact, Dev ghi "Recover data: Không cần") | Data | — | N/A | — | N/A — chấp nhận theo xác nhận Dev |
| T1 — Mua slot mới **standard** (tháng/năm) | Feature Medium | rows 258–259, 293–294 (đã hủy), 297–298 (extend), 301–302 (campaign) | 8 | OK |
| T2 — Mua slot mới **pro** (tháng/năm) | Feature Medium | rows 260–261, 295–296, 299–300, 303–304 | 8 | OK |
| T3 — **Upgrade lên pro** | Feature Medium | rows 262–272 | 11 | OK |
| T4 — Luồng thanh toán **Univapay** (token handler) | Feature Medium | các TC "Bill card" trải khắp nhóm 1–3 | ~29 | OK |
| *(ngoài scope đã nêu)* — Bill lại hợp đồng **overdue card / overdue transfer / đã hủy / extend / campaign** | Feature — **KHÔNG có trong mục 4.3 gốc của Dev** | rows 273–304 | 32 | Có TC nhưng **Dev chưa xác nhận scope** — xem §4.1 issue #1 |

### ORPHAN TCs

Không phát hiện TC lạc chủ đề — toàn bộ 59 TC (rows 257–315) đều trực tiếp liên quan redirect logic của bug #38957 (cột "Bug tự detect #38957" = OK cho cả 59 dòng).

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **"Sửa hàm dùng chung"** — `created()` / `univapayTokenHandler()` là 2 hàm chung cho nhiều luồng bill (mua mới, upgrade, bill lại, extend, campaign — theo cấu trúc 8-nhóm của chính sheet TC master). Dev mô tả cách fix ("redirect đến màn success trước, sau đó back lại step success") là generic cho **mọi** giao dịch bill thành công, không phải specific-check theo loại giao dịch. |
| Trigger space cần cover (REG-SHARED-001) | 7 luồng kích hoạt bill thành công: mua mới / upgrade / bill lại overdue card / bill lại overdue transfer / bill lại hợp đồng đã hủy / extend / thanh toán campaign — theo đúng cấu trúc 8 nhóm (nhóm 8 là case KHÔNG bill nên không tính) của sheet "Màn hình bill tiền". |
| Số trigger Dev đã xác nhận trong 03-dev-impact mục 4.3 | **2/7** (chỉ "mua slot mới" + "upgrade pro") |
| Số trigger có TC cover trong file 04 | **7/7** (TC đã có sẵn từ trước, rows 257–304) |
| KH report dạng | N/A — tracker "Bug tự detect" (Dev tự phát hiện, không phải KH report), không áp dụng AP-2 theo đúng nghĩa "symptom-only KH". Rủi ro tương đương vẫn tồn tại ở dạng khác: xem Alternative root causes. |
| Alternative root causes cần verify | Không áp dụng trực tiếp (root cause đã rõ, không phải symptom-only) — nhưng cần verify: 5 luồng bill ngoài phạm vi Dev nêu có **thực sự đi qua cùng `created()`/`univapayTokenHandler()`** đã fix hay đi qua code path khác chưa được fix. |
| Anti-patterns dính | **AP-6-adjacent** (mục 3 dev-impact có nội dung nhưng cột "Thay đổi"/"Lý do" đều để trống — không đủ chi tiết để xác nhận caller đã check hết) + **AP-4** (Commit/PR trống → không thể trace code để xác nhận fix shape thực tế) |

> Trigger space 7 nhưng Dev chỉ xác nhận 2 → **[BLOCKER] FIX-SHAPE** trong §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / REG-SHARED-001**: `03-dev-impact.md` mục 3 và mục 4.3 chỉ liệt kê **2/7 luồng** bill (mua mới, upgrade) dùng chung `created()`/`univapayTokenHandler()`, trong khi bộ TC sẵn có (rows 273–304, 32 case) test tới cả 7 luồng (thêm overdue card, overdue transfer, đã hủy, extend, campaign). Dev **chưa xác nhận bằng văn bản** các luồng còn lại có đi qua đúng code path đã fix hay không. Rủi ro kép: (a) nếu KHÔNG chung code path, 32 TC "OK" hiện tại đang che khuất 1 gap thật; (b) file 04 không có cột "Ngày thực hiện" nên không thể xác nhận 59 kết quả "OK" này được chạy **SAU** khi merge branch `fix/Task_Redirect_Bill_Success_38957`, có thể là baseline cũ tái sử dụng. — **Đề xuất**: (1) yêu cầu Dev bổ sung mục 4.3 xác nhận rõ cả 7 luồng dùng chung code path; (2) yêu cầu tester xác nhận/re-run 59 TC này trên môi trường đã deploy fix, ghi rõ ngày chạy.
- **[BLOCKER] GAP — STATE-001**: Cách fix (`03-dev-impact.md` mục 2) tự thêm 1 quy trình **2 bước tuần tự** ("redirect đến màn success trước, sau đó back lại step success") — khớp trigger `STATE-001` (Cao, Catalog C). **0/59 TC** test việc gián đoạn giữa 2 bước này (đóng tab / mất mạng / back / F5 trong đúng cửa sổ "Sau 3s redirect về step 完了" mà mọi TC hiện có đều ghi). Nếu gián đoạn, hợp đồng có thể kẹt ở trạng thái "đã bill nhưng chưa hoàn tất step" vĩnh viễn. — **Đề xuất**: bổ sung `TC-STATE001-01/02/03` (xem §5).

### 4.2 Major (nên fix)

- **[MAJOR] Checkbox verify chưa tick**: `01-bug-task.md` và `03-dev-impact.md` đều auto-fill `2026-07-29 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** ở cả 2 file — review này chưa có giá trị chính thức cho tới khi tester xác nhận đã đọc lại Redmine (đặc biệt journal #126891). — Đề xuất: tester đọc lại rồi tick cả 2 checkbox.
- **[MAJOR] AP-4 — Commit/PR trống**: mục "Commit / Pull Request" ở `03-dev-impact.md` để `<chưa có>` — không thể đối chiếu TCs với code thật để xác nhận fix shape (generic hay specific-check). — Đề xuất: yêu cầu Dev bổ sung link PR/commit trước khi Leader duyệt vòng cuối.
- **[MAJOR] RULE-01 / REG-URL-001**: 4 URL `*_success` trong bug này khớp **chính xác** danh sách "URL đo lường conversion KHÔNG được đổi" (`REG-URL-001`, ưu tiên nâng Cao vì chạm thanh toán — [checklist-lme.md §2.11](../../framework/checklist-lme.md)). 59 TC hiện tại chỉ test **Normal** (redirect đúng khi luồng nghiệp vụ hợp lệ) — thiếu **Abnormal** (gõ thẳng URL khi chưa có giao dịch, kỳ vọng không treo spinner) và **Boundary** (biến thể có/không dấu `/` cuối, param thừa). Vi phạm RULE-01 (quan điểm Cao thiếu 2/3 loại case, không ghi lý do). — Đề xuất: bổ sung `TC-REGURL001-01/02` (xem §5).
- **[MAJOR] RULE-08 / ENV-003**: File 04 (fetch trực tiếp từ sheet master, format "native") **không có cột Môi trường test** — không thể xác nhận 59 TC đã chạy trên Production hay chỉ Staging. Bill tiền là hạng mục RULE-08 minh thị cấm kết luận chỉ từ Staging. — Đề xuất: bổ sung xác nhận môi trường, kèm 1 TC chạy lại trên Production (`TC-ENV003-01`, xem §5).
- **[MAJOR] CONC-001 (phạm vi giới hạn của slice đang review)**: Quan điểm "double-click nút thanh toán" (Cao, tương tự `MAP-PLAN-05`) không xuất hiện trong 59 TC (rows 257–315). Có thể đã được test ở phần khác của sheet "Màn hình bill tiền" (ngoài phạm vi rows đã fetch) — cần xác nhận với Leader trước khi kết luận đây là GAP thật hay chỉ nằm ngoài phạm vi được lấy về. — Đề xuất: nếu xác nhận chưa có ở đâu trong sheet, bổ sung `TC-CONC001-01` (xem §5).
- **[MAJOR] Mục 3 (`03-dev-impact.md`) thiếu chi tiết**: cột "Thay đổi (nếu có)" và "Lý do" của cả 3 function/file đều để `<Dev không ghi chi tiết>` — gần với AP-6 dù mục 3 không hoàn toàn trống. Leader khó xác nhận mục 3 đã đủ caller nếu thiếu chi tiết cụ thể. — Đề xuất: yêu cầu Dev điền rõ nội dung thay đổi từng function.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Format file 04 không phải 16-cột canonical**: thiếu `TC No.` / `Mã quan điểm liên kết` / `Loại case` / `Kết quả thực thi` riêng / `Trạng thái đánh giá spec` / `Ghi chú` — vì đây là data fetch trực tiếp từ sheet master "Màn hình bill tiền" (không qua `/write-tc`). Chấp nhận được cho mục đích regression, nhưng khiến việc map quan điểm ở review này phải suy luận 100% thủ công (không có cột tường minh). — Gợi ý: nếu muốn đưa hẳn vào quy trình canonical, member bổ sung cột "Mã quan điểm liên kết" cho 59 dòng.
- **[MINOR] Row 280** (nhóm "Bill lại hợp đồng overdue card" › "Nhấn change maincard" › "Bot pro year"): Expected result ghi URL `https://step.lme.jp/yearly//pro_success` (2 dấu `/` liên tiếp). Nghi lỗi đánh máy khi soạn TC, nhưng theo `ENV-PATH` (Catalog D) đây đúng là điểm khác biệt dev/staging vs production (path thừa `//` "vẫn chạy ở dev nhưng hỏng ở production" qua B2) — nên xác minh lại URL thật trước khi dùng để đối chiếu kết quả test.

### 4.4 Nit (gợi ý)

- **[NIT]** Dev ghi D1 "Không có" data impact — hợp lý với fix thuần navigation, nhưng tên hàm `created()` gợi ý khả năng liên quan tạo bản ghi — gợi ý hỏi Dev xác nhận thêm 1 câu cho chắc (không bắt buộc, RULE-03 đã có lý do hợp lệ).
- **[NIT]** `PAY-STATE-001` (nhất quán trạng thái 3 nơi sau giao dịch) không thấy trong slice rows 257–315 — nhiều khả năng được test ở phần khác của sheet ("Quản lý hợp đồng", "Bill max friend" — không được fetch trong task này). Chỉ nêu để Leader biết, không tính là gap riêng của bug #38957.

---

## 5. TCs đề xuất bổ sung

> Copy thẳng vào `04-tc-list.md` (hoặc phụ lục riêng nếu muốn giữ format native của file 04 hiện tại).

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-STATE001-01 | STATE-001 | Abnormal | Đóng tab/mất mạng ngay sau bill thành công, trước khi redirect sang router success chạy | Bot free, đủ điều kiện upgrade standard/month; thẻ test Univapay sandbox hợp lệ | 1. Vào màn bill tiền, chọn plan standard/tháng, nhập thẻ test hợp lệ.<br>2. Bấm nút thanh toán.<br>3. Ngay khi Network tab thấy response 200 từ API bill nhưng TRƯỚC khi trang bắt đầu redirect — đóng tab (hoặc tắt mạng qua DevTools).<br>4. Mở lại app, vào lại màn quản lý hợp đồng/danh sách bot. | Thẻ test Univapay sandbox (thành công), bot free, plan standard/month | Giao dịch đã ghi nhận thành công, không mất tiền vô ích; trạng thái hợp đồng hiển thị đúng standard/active dù không hoàn tất redirect; KHÔNG kẹt ở trạng thái "đã bill nhưng vẫn hiện free" hoặc lỗi khi vào lại | Chưa test | | STAGING | | | #38957 | Spec không ghi | Lấp GAP STATE-001 (0/59 TC hiện có test gián đoạn giữa bước bill và bước redirect). Cần hỏi leader/dev hành vi mong đợi trước khi chấm Đạt/Không đạt. |
| TC-STATE001-02 | STATE-001 | Abnormal | Bấm Back trình duyệt trong lúc đang ở router bill success (trong cửa sổ 3s trước khi tự động redirect) | Đã tới bước redirect thành công, đang ở URL `.../monthly/standard_success` | 1. Thực hiện luồng mua/upgrade tới khi redirect sang URL success.<br>2. Trong vòng 3 giây (trước khi tự động chuyển tiếp), bấm nút Back trình duyệt.<br>3. Quan sát URL và trạng thái hiển thị.<br>4. Đợi thêm vài giây, F5 lại màn danh sách bot/hợp đồng để kiểm step hoàn tất có set đúng không | Giống TC-STATE001-01 | Không bị redirect loop (quay lại/tiến tới lặp giữa 2 URL); step hoàn tất (完了) vẫn được set đúng dù bấm Back; không tạo giao dịch trùng | Chưa test | | STAGING | | | #38957 | Spec không ghi | Lấp GAP STATE-001 + OUT-TRUTH-001. Hỏi leader nếu phân vân Đạt/Không đạt. |
| TC-STATE001-03 | STATE-001 | Boundary | F5 refresh đúng lúc router success vừa load (trong cửa sổ 3s trước khi tự động redirect) | Đã tới URL `.../yearly/pro_success` | 1. Thực hiện luồng bill tới khi vào URL `.../yearly/pro_success`.<br>2. Ngay khi trang vừa load (trong 3s đầu), bấm F5.<br>3. Quan sát Network tab xem có gọi lại API tính tiền/tạo giao dịch lần 2 không; quan sát countdown/redirect có chạy lại từ đầu hay tiếp tục đúng | Giống trên, quan sát thêm Network tab | F5 không kích hoạt xử lý bill lần 2 (không tạo giao dịch trùng); cuối cùng vẫn redirect đúng về step 完了 | Chưa test | | STAGING | | | #38957 | Spec không ghi | Lấp GAP STATE-001 (Boundary — cửa sổ thời gian 3s). Hỏi leader nếu phân vân Đạt/Không đạt. |
| TC-REGURL001-01 | REG-URL-001 | Abnormal | Truy cập trực tiếp URL redirect khi KHÔNG qua luồng bill (gõ thẳng URL) | User đã đăng nhập admin, KHÔNG vừa thực hiện giao dịch bill nào | 1. Đăng nhập admin.<br>2. Gõ thẳng URL `https://step.lme.jp/monthly/standard_success` trên thanh địa chỉ (không qua flow bill).<br>3. Lặp lại với 3 URL còn lại: `/yearly/standard_success`, `/monthly/pro_success`, `/yearly/pro_success` | 4 URL nêu trong `01-bug-task.md` | Trang trả về hành vi hợp lý (redirect về trang phù hợp hoặc thông báo lỗi rõ ràng) — KHÔNG treo spinner vô hạn, KHÔNG lỗi 500, KHÔNG hiển thị nhầm "thanh toán thành công" khi chưa có giao dịch | Chưa test | | STAGING | | | #38957 | Spec không ghi | Lấp GAP REG-URL-001 (Abnormal) — RULE-01 quan điểm Cao thiếu case này. Normal đã có sẵn ở file 04 (48 TC business flow). |
| TC-REGURL001-02 | REG-URL-001 | Boundary | Biến thể dấu `/` cuối và param thừa trên 4 URL success | Giống TC-REGURL001-01, hoặc thực hiện ngay sau 1 giao dịch billing thật | 1. Với mỗi 1 trong 4 URL, test thêm dấu `/` ở cuối (vd `.../monthly/standard_success/`).<br>2. Test thêm 1 query param thừa (vd `?foo=bar`) trên cả 4 URL.<br>3. Quan sát response từng biến thể (8 case) | 4 URL × 2 biến thể = 8 case | Cả 8 biến thể đều trả về đúng màn hình mong đợi (200, không lỗi, không treo spinner vô hạn) theo REG-URL-001 | Chưa test | | STAGING | | | #38957 | Spec không ghi | Lấp GAP REG-URL-001 (Boundary). Normal đã có sẵn ở file 04. |
| TC-ENV003-01 | ENV-003 | Normal | Verify redirect flow trên Production với giao dịch thật | Account Production thật hoặc account nội bộ được duyệt test trên Production | 1. Trên Production (`step.lme.jp`), thực hiện 1 luồng mua/upgrade thật (chọn luồng rẻ nhất hoặc dùng account test nội bộ được duyệt).<br>2. Verify redirect sang đúng router success.<br>3. Verify sau 3s về step 完了.<br>4. Đối soát với dashboard Univapay Production (PAY-STATE-001) khớp trạng thái/số tiền | Account Production thật (theo RULE-08 / ENV-PAY) | Hành vi giống hệt Staging — redirect đúng URL, về step 完了 đúng, dashboard Univapay khớp trạng thái/số tiền | Chưa test | | PRODUCTION | | | #38957 | Spec ghi rõ | Lấp GAP RULE-08/ENV-003 — bill tiền không được kết luận chỉ từ Staging (file 04 hiện không có cột môi trường). |
| TC-CONC001-01 | CONC-001 | Boundary | Double-click nút thanh toán | Bot đủ điều kiện mua/upgrade, thẻ test hợp lệ | 1. Điền đầy đủ thông tin thanh toán.<br>2. Double-click thật nhanh (hoặc script click 2 lần liên tiếp < 300ms) vào nút xác nhận thanh toán.<br>3. Kiểm tra Network tab số lượng request bill được gửi đi.<br>4. Kiểm tra số giao dịch được tạo trong hệ thống + dashboard Univapay | Thẻ test sandbox | Chỉ 1 giao dịch được xử lý (không bị charge 2 lần, không tạo 2 bản ghi hợp đồng); redirect chỉ chạy đúng 1 lần | Chưa test | | STAGING | | | #38957 | Spec không ghi | Lấp CONC-001 — xác nhận trước với Leader nếu quan điểm này đã có TC ở phần khác của sheet (ngoài rows 257–315) để tránh trùng lặp. |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - Section: FA-031 (Hợp đồng và thanh toán) — luồng redirect `*_success` của bill_tool hiện KHÔNG có mô tả riêng trong `templates/LME-SYSTEM-SPEC.md` lẫn `spec-features/admin/detail-contract/feature-spec.md` (đã kiểm tra, không tìm thấy).
  - Nội dung cần update: mô tả rõ hành vi mong đợi khi **gián đoạn** giữa bước "redirect sang router success" và bước "back lại step hoàn tất" (đóng tab/mất mạng/back/F5 trong cửa sổ 3 giây) — hiện tại mọi quyết định Đạt/Không đạt cho các TC bổ sung ở §5 đều phải dựa vào suy đoán "hành vi user bình thường mong đợi" (theo §0.5 checklist-lme.md), rủi ro mỗi người đánh giá khác nhau.
  - Người chịu trách nhiệm update: `<PM/Dev — Leader chỉ định>`

---

## 7. Checklist đã chạy

- [x] A. Coverage
- [x] B. Chất lượng từng TC
- [x] C. Chất lượng bộ TC tổng thể
- [x] D. Spec alignment
- [x] E. Hành chính
- [x] F. Base quan điểm test LME
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới đây
  - [x] F.2 Catalog (tầng 2) — A input (N/A, không có form nhập mới) / B UI (N/A) / C bản đồ LME (MAP-PAY-01/02, MAP-SEND N/A) / D-D2 môi trường (ENV-PAY, ENV-DOMAIN) + job (N/A) / E media (N/A)
  - [x] F.3 RULE quy trình — RULE-01 (vi phạm ở REG-URL-001) · RULE-02 (chưa đủ dữ liệu đánh giá vì Kết quả thực thi hiện là OK nhưng thiếu ngày chạy) · RULE-03 (D1 × có lý do) · RULE-06 (N/A, output là redirect nội bộ) · RULE-07 (N/A, fix thuần navigation) · RULE-08 (vi phạm — không có cột môi trường) · RULE-09 (N/A, không phải version-up)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| FUNC-001 | Cao | ✓ (mọi chức năng) | 48 TC nhóm 1–7 | OK |
| STATE-001 | Cao | ✓ (2 bước tuần tự: redirect → back step) | 0 | **GAP → BLOCKER** |
| REG-SHARED-001 | Cao | ✓ (created()/univapayTokenHandler() dùng chung nhiều luồng bill) | 32 TC có sẵn (rows 273–304) nhưng Dev chưa xác nhận danh sách đầy đủ | **RISK → BLOCKER** (dev-impact thiếu, không phải thiếu TC) |
| REG-URL-001 | Cao (nâng từ Trung bình vì chạm thanh toán) | ✓ (đúng 4 URL liệt kê trong catalog) | Normal: 48 TC. Abnormal/Boundary: 0 | **RISK → MAJOR (RULE-01)** |
| PAY-STATE-001 | Cao | ✓ (giao dịch tiền) | Ngoài phạm vi rows 257–315 (không thấy trong slice này) | RISK → [NIT] (note phạm vi, không tính gap riêng bug này) |
| ENV-003 / RULE-08 | Cao | ✓ (chạm bill tiền) | 0 (không có cột môi trường trong file 04) | **GAP → MAJOR** |
| CONC-001 | Cao | ✓ (nút thanh toán quan trọng) | 0 trong slice này | **RISK → MAJOR** (note phạm vi, cần Leader xác nhận) |
| DATA-DB-001 | Cao | × | N/A | × — lý do: Dev xác nhận D1 "không có" data impact (navigation-only fix) |
| COMPAT-LEGACY-001 | Cao | × | N/A | × — lý do: không phải version-up, không có nhánh cũ/mới song song |
| UI-003 / OUT-TRUTH-001 | Trung bình→Cao (false success) / Cao | ✓ (cửa sổ 3s trước redirect) | 0 rõ ràng | Gộp vào GAP STATE-001 ở trên |

> Quan điểm Trigger khớp task mà **GAP** → `[BLOCKER]` nếu ưu tiên **Cao**, `[MAJOR]` nếu Trung bình.
> **KHÔNG** dùng §4 "Quan điểm chưa đủ bằng chứng" của checklist-lme (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) để flag BLOCKER/MAJOR — RULE-11. (Không mục nào trong §4 đó liên quan task này.)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
