# 05 — Review Report

## 0. Nguồn TC

- **Nguồn đã dùng**: MCP LME TEST STUDIO — task #191 (ticket 38785, branch `ai_small_38785`, round 1, `reviewState=leader`)
- **Tổng số TC review**: 12

---

## 1. Coverage — `dev-impact` + `diff code`

**Kết luận**: 11/16 vùng ảnh hưởng đủ TC · **3 GAP** · **2 RISK**

> **Phạm vi review đã chốt theo diff**, không theo toàn bộ tính năng coupon. Diff = **1 file** `app/Http/Controllers/Admin/UserController.php` (+12/−3), 2 hàm. Studio `dev_impact` liệt kê đúng 8 điểm thay đổi; chỉ những điểm này mới sinh GAP. Vùng đã loại khỏi phạm vi ghi ở cuối §1.

| # | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Vấn đề | Severity |
|---|---|---|---|---|---|---|
| **G1** | `diff code` | `dataBotContract` **inner join `bot_slots`** → hợp đồng **không có bản ghi `bot_slots`** trả `null` ⇒ chủ hợp đồng hợp lệ bị chặn | NEW-9 | **RISK** | Đây là **điều kiện mới do chính fix đưa vào** — trước fix `BotContracts::where('id',...)` không join `bot_slots`. NEW-9 né vấn đề: expected là *"kiểm tra dữ liệu test... đánh dấu thiếu dữ liệu môi trường"*, không phải hành vi nghiệp vụ ⇒ kết quả `pass` của nó không kết luận được gì. Kho FA-031 xác nhận hợp đồng **chưa kết nối bot** là trạng thái có thật (`TC-BLP-228` hợp đồng mua mới chưa kết nối bot · `TC-BLP-380` staff mở detail hợp đồng chưa add bot · `TC-BLP-383` Bug KH #36303 slot Standard chưa kết nối bot). | `[BLOCKER]` |
| **G2** | `diff code` | Bỏ đọc `botId` từ request, lấy từ `$botContract->bot_id` — trường hợp **2 bot của cùng một owner** | NEW-8, NEW-12 | **GAP** | NEW-8 test `botId` của **người khác**, NEW-12 test **không gửi** `botId`. Thiếu case dễ xảy ra nhất trong vận hành thật: owner có ≥2 bot, đang ở ngữ cảnh bot B nhưng mở hợp đồng của bot A — gia hạn phải rơi vào hợp đồng đang mở, không theo bot đang chọn. Ngữ cảnh bot đi theo **session trình duyệt**, không theo tab ⇒ rất dễ ghi nhầm hợp đồng. | `[MAJOR]` |
| **G3** | `diff code` | Đổi thứ tự xử lý (kiểm quyền **trước** `is_used=1`) — nhánh **coupon đã dùng rồi** | — | **GAP** | Case này **từng có** trong NEW-7 v1 nhưng bị gỡ ở v2 (note: *"đã loại bỏ bước userA apply lại C1 để tránh trùng coverage"*) và **không TC nào thay thế**. "Coupon chưa dùng" là 1 trong 2 điều kiện validate gốc của endpoint và nằm ngay trên đoạn code bị đổi thứ tự ⇒ hiện không còn TC nào đi qua nhánh này. | `[MAJOR]` |
| **G4** | `diff code` | `logInfo` trong `applyCouponCode` ghi `bot_id` từ `$botContract->bot_id` sau fix | — | **GAP** | Studio `dev_impact` nêu **đích danh**: *"logInfo ghi bot_id từ `$botContract->bot_id` sau fix — cần xác nhận log vẫn đủ context"*. 0/12 TC chạm tới. Log là bằng chứng truy vết khi khách khiếu nại bị gia hạn sai. | `[MINOR]` |
| **G5** | `dev-impact` | D1 — `coupon_management.bot_name` (+ `user_id` / `bot_contract_id` / `datetime_use`) | NEW-1 | **RISK** | `bot_name` ghi vào bản ghi coupon suy ra từ bot — mà fix **đổi nguồn lấy bot**. Chỉ NEW-1 (TC UI) assert đủ 5 cột; các TC tầng API sau v2 chỉ còn *"được đánh dấu đã dùng"*. Thêm nữa chưa TC nào kiểm chứng phạm vi ghi bằng dữ liệu **trùng tên** (RULE-07). | `[MAJOR]` |

**Đã cover đủ (không ghi chi tiết)**: EP-05 thêm kiểm quyền (NEW-3/6/11) · EP-06 thêm kiểm quyền (NEW-7) · `botId` giả mạo và `botId` vắng mặt (NEW-8/12) · nhánh staff `pointSettings` (NEW-2/5/11) · đổi thứ tự với hợp đồng không tồn tại (NEW-10) · chặn IDOR không đốt coupon (NEW-7) · happy path owner (NEW-1/4) · bỏ 1 query lặp (không cần TC).

### Đã loại khỏi phạm vi — có cân nhắc rồi bỏ

> Theo **AP-5** (`framework/anti-patterns.md`) và nguyên tắc *fix ở layer A, layer downstream không bị chạm code → không đề xuất TC*. Các vùng dưới đây **đều liên quan tới coupon** nhưng **không có dòng nào trong diff**, nên không sinh TC cho ticket này. Ghi lại để lần review sau không phải suy luận lại.

| Vùng | Vì sao loại | Nguồn kiểm chứng |
|---|---|---|
| Công thức tính `次回決済(更新)日` (cộng từ hạn cũ / từ hôm nay; ngày 29/30/31) | Fix không đụng phép tính ngày — `new_expired_date` tính y như trước | Studio `dev_impact` 8 điểm, không điểm nào chạm phép tính · `spec_delta.diffStat` = 1 file |
| Áp coupon lên hợp đồng `延滞中` / `入金待ち` / `解約待ち` / `解約済み` / `強制解約` | Logic trạng thái hợp đồng nằm ngoài 2 hàm được sửa | Kho `TC-BLP-19` (6 trạng thái) — thuộc nhóm khác của FA-031 |
| Job `AutoPaymentJobUnivapay` · `HandleBillStripe` · `FlowDeleteBot` đọc `expired_date` mới | Job không nằm trong diff; `expired_date` vẫn được ghi bằng cùng cơ chế | `templates/LME-SYSTEM-SPEC.md` §Job — không job nào thuộc `UserController` |
| Mốc `expired_date + 7 ngày` mở/chặn 5 trang phía LINE user | Không nằm trong diff | Kho `TC-BLP-371`~`375` (MT-10) — đã có sẵn TC ở kho, thuộc nhóm 38 |
| Màn `操作履歴` hiển thị dòng 「クーポンコードの適用」 | Ghi lịch sử không nằm trong diff. Phần **mâu thuẫn expected** giữa NEW-1 và NEW-4 vẫn giữ ở §3 + §6 | Kho `TC-BLP-222`~`227` |
| Tầng xác thực (`check_login`, CSRF) | Fix **không** đụng tầng auth — chỉ thêm kiểm owner bên trong hàm | Bug gốc nêu *"Route chỉ dưới `check_login`"*; diff không chạm route/middleware |
| Bỏ dở giữa preview và apply (đóng modal / back / hết phiên) | `checkCouponCode` không ghi DB — NEW-3 đã chứng minh; bỏ dở = không gọi `applyCouponCode` | NEW-3 expected: *"KHÔNG ghi DB... (preview only)"* |
| Rollback khi chuỗi ghi 4 bảng đứt giữa chừng | Rủi ro có **từ trước fix**, không phải do fix tạo ra; cần Dev dựng lỗi nhân tạo | Diff chỉ thêm 1 điều kiện chặn, không đổi cơ chế transaction |
| Caller cũ của `Bots::dataBotContract` / `getListBotIdStaffManagement` (`PointSettingController`, `ListPageController`, `BotEnterPriseController`) | ⚠️ **Fix chỉ *gọi thêm* hàm, KHÔNG *sửa* hàm** (`app/Bots.php` không nằm trong `spec_delta.files[]`) ⇒ hành vi caller cũ không thể đổi. Rule "hàm dùng chung phải có danh sách caller" chỉ áp dụng khi hàm bị sửa. | `spec_delta.files[] = ["app/Http/Controllers/Admin/UserController.php"]` — **1 file duy nhất** |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 9 quan điểm Trigger khớp phạm vi fix · 4 đã cover đủ · **5 chưa cover đủ**

> ⚠️ 4 TC mang mã quan điểm **không tồn tại** trong `framework/checklist-lme.md` (`API-001` → NEW-3 · `TOOL-KNOW-002` → NEW-7 · `API-CONTRACT-001` → NEW-8, NEW-12). Theo BƯỚC 0.6 #5 các TC này không được tính là cover quan điểm nào — nội dung vẫn dùng được, nhưng phải gán lại mã chuẩn thì coverage mới đo được.

| # | Mã quan điểm | Ưu tiên | Trigger khớp vì | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|---|
| **Q1** | `PERM-002` | Cao | Thao tác nhạy cảm (thanh toán) — quan điểm trung tâm của fix | NEW-2, NEW-5, NEW-11, NEW-6 | **RULE-01**: 3 `Normal` + 1 `Abnormal` + **0 `Boundary`**, không ghi lý do. Boundary còn thiếu là **ranh giới quyền theo thời gian**: quyền được kiểm ở *thời điểm submit* hay *thời điểm mở màn*? Fix thêm bước kiểm quyền nên đây là chiều trực tiếp của fix. Kho `TC-BLP-385` đã có đúng pattern cho màn detail hợp đồng. Thêm nữa NEW-2/NEW-5 trùng nhau (§3) làm quan điểm này **trông dày hơn thực tế**. | `[MAJOR]` |
| **Q2** | `PERM-003` | Cao | Tổ chức vận hành **nhiều LINE OA** — fix đổi cách xác định bot | **0** | → G2 | `[MAJOR]` |
| **Q3** | `CONC-001` | Cao | Nút thực thi hành động quan trọng + **tài nguyên giới hạn dùng chung** (coupon dùng 1 lần) | **0** | Fix chèn thêm 1 bước kiểm quyền **giữa** lúc đọc coupon và lúc đánh dấu `is_used=1` ⇒ khoảng cách giữa "thấy coupon còn dùng được" và "khoá coupon lại" **rộng ra**. Cần tối thiểu 1 TC double-click nút xác nhận. Không cần bộ 3 loại case: race với 2 tài khoản khác nhau đã bị `dataBotContract` chặn từ tầng quyền. | `[MAJOR]` |
| **Q4** | `FUNC-004` | Cao | Chức năng có giới hạn số lượng — coupon dùng 1 lần | **0** | → G3 | `[MAJOR]` |
| **Q5** | `ENV-003` ★ | Cao | Tính năng chạm **thanh toán** — *"không được đánh × với lý do staging đã pass"* (RULE-08) | NEW-9 (mang mã `ENV-003` nhưng nội dung là check dữ liệu test) | **0 TC chạy `staging`, 0 TC chạy `prd`** — toàn bộ 10 run ở `local`. Kho `TC-BLP-392`: *"giá plan trên PRODUCTION khác dev/staging → mọi TC tiền phải chạy PRODUCTION"*. **Không cần TC mới** — đây là yêu cầu chạy lại, đã set `Phạm vi ENV = product` cho TC ở §5 và ghi issue §4 #1 cho 12 TC hiện có. | `[MAJOR]` |

**Đã cover đủ (không ghi chi tiết)**: `FUNC-001` · `PERM-001` · `DATA-DB-001` (WHERE scope 2 tài khoản qua NEW-6/NEW-7 — phần trùng tên bổ sung ở §5) · `SEC-001`.

**Quan điểm có Trigger nhưng đã loại khỏi phạm vi** (lý do ở bảng cuối §1): `REG-RUN-001` · `PAY-AMOUNT-001` · `PAY-STATE-001` · `PAY-ABANDON-001` · `SEC-002` · `STATE-001` · `DATA-001`.

---

## 3. TC trùng lặp

Đã rà **12/12** TC theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`). Phát hiện **1 nhóm trùng + 1 nhóm mâu thuẫn**:

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Staff `pointSettings` áp coupon thành công | **NEW-2** (đi qua UI thật → thoả RULE-06 + RULE-07 đầy đủ hơn) | **NEW-5** → **GỘP**, không xóa rời | `DUP-SUBSET` | `PERM-002` × `Normal` × *staff có quyền `pointSettings` apply coupon lên hợp đồng của chủ khác* × *staff + hợp đồng có `bot_slots` + coupon chưa dùng*. Steps NEW-5 chính là request nằm dưới nút của NEW-2; expected tương đương (`status:true` + gia hạn + `is_used=1`). | `[MINOR]` |
| `bot_life_cycles` sinh ra khi apply coupon | **Chưa chốt được** — cần Dev xác nhận enum | **KHÔNG xóa TC nào** | `DUP-CONFLICT` | NEW-1 expected: *"thêm 1 bản ghi `bot_life_cycles` **type APPLY_COUPON**"* ⟷ NEW-4 (v2) expected: *"`bot_life_cycles` được tạo đúng theo flow apply coupon. **Không giả định thêm loại** ngoài evidence"*. Spec FA-031 ghi 「クーポンコードの適用 \| (chưa xác định type)」; kho MT-21 ghi nhận `bot_life_cycles` đang **dùng trùng mã type** giữa các sự kiện khác nhau. | `[MAJOR]` → §6 |

**Gate xoá đã chạy**: giả định bỏ NEW-5 → `F2`/`F4`/`T4` vẫn được NEW-2 + NEW-11 cover ⇒ không mất coverage. Vẫn đề xuất **gộp** (bổ sung assertion DB tầng API của NEW-5 vào NEW-2) thay vì xoá rời, vì NEW-2 hiện chưa assert `is_used=1` ở tầng DB.

**Không phải trùng** (đã cân nhắc, giữ cả 2): NEW-1 ⟷ NEW-4 (khác tầng vào: browser thật vs request API trực tiếp — 2 lối đi khác nhau tới cùng code path) · NEW-8 ⟷ NEW-12 (cùng `Abnormal` nhưng khác input: `botId` **giả mạo** vs `botId` **không gửi**) · NEW-3 ⟷ NEW-11 (khác role: owner vs staff).

⚠️ **DUP-INFLATE**: cặp NEW-2/NEW-5 làm `PERM-002` trông như có 3 TC `Normal` → che việc quan điểm này **thiếu hẳn loại `Boundary`** (đã mở lại ở §2 Q1).

---

## 4. Issues khác

### Chất lượng nguồn TC

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 1 | `[MAJOR]` | Toàn bộ 12 TC | **RULE-08 / ENV-003** — 10 run đều ở `env=local`; `dev`/`staging`/`prd` đều **0 run**. Task là **bill tiền** (gia hạn hợp đồng trả phí). | Chạy lại toàn bộ TC chạm tiền trên `product`. `env_scope` hiện khai `all` nhưng **khai ≠ đã chạy** — đọc `envAuto[].runs` để biết thực tế. |
| 2 | `[MAJOR]` | Toàn bộ 12 TC | **RULE-02** — 10 TC ghi `Đạt` nhưng cột `Evidence thực tế` **rỗng 12/12**. Kết quả do `pipeline` AI tự khai, không có QA người xác nhận. | Bổ sung evidence theo cột Evidence của từng quan điểm (screenshot màn 契約情報 + dump DB + log). |
| 3 | `[MAJOR]` | NEW-3, NEW-7, NEW-8, NEW-12 | **Mã quan điểm không tồn tại** trong `framework/checklist-lme.md`: `API-001`, `TOOL-KNOW-002`, `API-CONTRACT-001` → 4 TC này không map được coverage. | Gán lại mã chuẩn: NEW-3 → `FUNC-001`/`PERM-001`; NEW-7 → `PERM-002`; NEW-8, NEW-12 → `PERM-003`. Sửa trên Studio (`testcase_update`). |
| 4 | `[MAJOR]` | Toàn bộ 12 TC | Cột `Trạng thái đánh giá spec` (`spec_status`) **trống 12/12** — trong khi spec coupon là gap đã biết. TC không ghi đã hỏi ai ⇒ Expected là tự suy diễn. | Điền `Spec không ghi` + tên người đã hỏi, hoặc `Đã hỏi leader`. |
| 5 | `[MAJOR]` | Spec | **Không có spec cho chức năng coupon.** `spec-features/admin/billing-plan/feature-spec.md` §9 **[M2]**: *"API Spec: không tìm thấy endpoint xử lý coupon; DB: không tìm thấy cột `coupon_code` trong `bot_contracts` (52 cột), không tìm thấy bảng `coupons`"*. Kho FA-031 **MT-23** xác nhận lại: *"cả spec lẫn TCs đều bỏ trống"*. ⇒ Không có chuẩn đối chiếu Expected. | Xem §6. |
| 6 | `[MAJOR]` | `03-dev-impact.md` | `Auto-filled: 2026-09-17 by /new-task` **VÀ** checkbox *"Tester verify auto-fill chính xác"* chưa tick → F/D/T có thể thiếu hoặc map sai. | Tester đọc lại Redmine #38785, tick checkbox trước khi review này có giá trị. |
| 7 | `[NIT]` | `03-dev-impact.md` mục 3 | Không có bảng caller của `Bots::dataBotContract` / `getListBotIdStaffManagement`. **Không phải blocker** ở ticket này vì fix chỉ *gọi thêm*, không *sửa* 2 hàm đó (`app/Bots.php` không nằm trong diff) — caller cũ không thể đổi hành vi. | Nhắc Dev điền cho đủ form, không chặn test. |

### Chất lượng từng TC

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 8 | `[MAJOR]` | **NEW-9** | `Kết quả mong đợi` **không đo lường được** — không phải kết quả nghiệp vụ mà là mô tả quy trình: *"Kiểm tra dữ liệu test: hợp đồng dùng để test phải có `bot_slots`... đánh dấu thiếu dữ liệu môi trường hoặc cần xác nhận requirement"*. Chạy TC này không thể kết luận Đạt/Không đạt; note của chính TC thừa nhận đã *"điều chỉnh từ testcase business sang kiểm tra rủi ro môi trường"*. Kết quả `pass` hiện tại **không có nghĩa** — trong khi đây là điều kiện **mới do fix đưa vào** (G1). | Viết lại thành TC nghiệp vụ sau khi Dev chốt hành vi mong muốn (§6 mục 2) → đã đề xuất `TC-FUNC001-01/02` ở §5. |
| 9 | `[MAJOR]` | **NEW-2**, **NEW-5** | Expected chứa **nhánh tự cho phép bỏ qua**: *"nếu môi trường không dựng được staff có quyền `pointSettings` thì trả skip"*. Pipeline vẫn ghi `pass` — không phân biệt "đã chạy và đúng" với "không dựng được data". Nhánh staff (`listBotAccept`) là **1 trong 2 nhánh quyền của fix**. | Tách điều kiện dựng data thành `Tiền điều kiện` bắt buộc; bỏ nhánh skip khỏi Expected. Xác nhận lại run 2026-08-24 có thật sự chạy nhánh staff không. |
| 10 | `[MAJOR]` | **NEW-4** | Expected sau v2 bị **làm mờ**: *"được đánh dấu đã dùng"*, *"cập nhật đúng ngày gia hạn mới"*, *"`bot_life_cycles` được tạo đúng theo flow"* — không còn giá trị/trạng thái cụ thể nào để đối chiếu. TC gốc (v1) cụ thể hơn. | Ghi giá trị kỳ vọng cụ thể (ngày trước/sau, 5 cột của bản ghi coupon) thay vì tính từ "đúng". |
| 11 | `[MAJOR]` | Toàn bộ | **CONFLICT nguồn**: `03-dev-impact.md` mục 2 (chép từ Redmine) ghi *"`botId` vẫn lấy từ request như cũ"*, nhưng Studio `dev_impact` (suy từ diff `48877bb5b3`) ghi *"**bỏ đọc `botId` từ request** — `botId` nay lấy từ `$botContract->bot_id`"*, và NEW-8/NEW-12 test theo hướng sau. Báo cáo Dev trên Redmine **sai so với code**. | Chốt bằng diff. Nếu Studio đúng → sửa note Redmine (QA đời sau đọc note sẽ viết TC sai chiều). → §6. |
| 12 | `[MINOR]` | **NEW-1** | `Ghi chú` yêu cầu *"Trigger phải từ browser thật"* nhưng `exec_mode=auto` và run do `pipeline` thực hiện. | Xác nhận pipeline chạy browser thật; nếu không → đổi `exec_mode=manual`. |
| 13 | `[MINOR]` | Toàn bộ 12 TC | `exec_mode=auto` **12/12**, 0 TC `manual` — trong khi NEW-1/NEW-2 mô tả thao tác người dùng thật (bấm 「クーポンコードを入力する」, cuộn modal, quan sát màn xác nhận). | Đặt `manual` cho TC UI cần mắt người quan sát. |

---

## 5. TCs đề xuất bổ sung (9)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (549 dòng, 40 nhóm chức năng) |
| Vùng regression phát hiện từ kho | `TC-BLP-385` (đổi quyền giữa phiên) · `TC-BLP-386` (middleware bot A↔B, 8 màn thao tác hợp đồng) · `TC-BLP-228`/`380`/`383` (hợp đồng chưa kết nối bot) · `TC-BLP-398` (hợp đồng lứa cũ) · `TC-BLP-392` (mọi TC tiền phải chạy PRODUCTION) |
| Conflict expected vs kho | NEW-1 (`bot_life_cycles type APPLY_COUPON`) vs spec FA-031 「(chưa xác định type)」 + kho MT-21 (trùng mã type) → `[MAJOR] SPEC-CONFLICT`, đã đưa §6 |
| GAP dùng lại TC kho (không viết mới) | **Không** — kho FA-031 **MT-23** xác nhận *"KHÔNG có bất kỳ TC nào"* về coupon. TC dưới đây dẫn chiếu TC kho làm **mẫu regression**, không dùng lại nguyên bản. |
| Xác nhận chống trùng | Đã đối chiếu **12** TC ở BƯỚC 0 + kho FA-031 — **không TC đề xuất nào trùng** |

> **Nguyên tắc chọn TC**: mỗi TC phải buộc được về **một điểm cụ thể trong diff** (Studio `dev_impact`, 8 điểm). Các vùng liên quan tới coupon nhưng không có dòng nào trong diff đã bị loại — danh sách + lý do ở cuối §1.
> **`Q5` (`ENV-003`) không có TC riêng** — đây là yêu cầu **chạy lại** trên môi trường thật, đã thể hiện bằng cột `Phạm vi ENV = product` và issue §4 #1.
> **`TC-REGSHARED001-01` là scope riêng**, không thuộc phần verify fix — xem ghi chú của dòng đó.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | Áp mã coupon — hợp đồng chưa kết nối bot | Abnormal | manual | product | Chủ hợp đồng mua mới **chưa kết nối LINE OA** áp mã coupon | - Tài khoản owner vừa mua 1 hợp đồng Standard, **chưa kết nối bot** (màn list hiện dòng hợp đồng không có tên bot)<br>- Có 1 mã coupon chưa dùng | 1. Mở 契約情報・領収書 (`/basic/point-settings`)<br>2. Mở chi tiết hợp đồng chưa kết nối bot<br>3. Bấm 「クーポンコードを入力する」, nhập mã, bấm nút xem trước<br>4. Ghi lại nội dung hiển thị<br>5. Nếu qua được bước xem trước → bấm 「クーポンコードの利用を確定する」 | Mã coupon hợp lệ chưa dùng | Ghi nhận hành vi thực tế rồi đối chiếu kết luận của Dev (§6 mục 2): hoặc (a) áp được bình thường, hoặc (b) hiện 「クーポンコードは無効です」. **Nếu ra (b) thì đây là regression do fix** — chủ hợp đồng hợp lệ mất khả năng áp coupon → raise ticket. Mã coupon **không bị đốt** trong mọi trường hợp bị chặn. | | Lấp `G1` · Điều kiện `bot_slots` là **mới do fix** · regression · Đánh giá spec: Spec không ghi — chờ §6 mục 2 · Evidence: screenshot màn chi tiết hợp đồng + dump `bot_slots`/`coupon_management` · Mẫu kho: `TC-BLP-228`, `TC-BLP-380` |
| TC-FUNC001-02 | UI | FUNC-001 | Áp mã coupon — hợp đồng chưa kết nối bot | Boundary | manual | product | Hợp đồng lứa cũ thiếu bản ghi `bot_slots` nhưng đang chạy bình thường vẫn áp được coupon | - 1 hợp đồng trả phí **đang dùng bình thường**, bot vẫn gửi tin được, nhưng thuộc lứa dữ liệu cũ không có bản ghi `bot_slots`<br>- Có 1 mã coupon chưa dùng | 1. Xác nhận hợp đồng ở trạng thái 正常 và bot vẫn gửi tin được<br>2. Mở chi tiết hợp đồng → 「クーポンコードを入力する」<br>3. Nhập mã, bấm xem trước rồi xác nhận<br>4. Quan sát 次回決済(更新)日 trên màn list | Hợp đồng lứa cũ + coupon hợp lệ | Hợp đồng đang hoạt động bình thường **không được** bị chặn áp coupon. Nếu bị 「クーポンコードは無効です」 → khách đang trả tiền mà không dùng được coupon ⇒ raise ticket. | | Lấp `G1` · regression · Đánh giá spec: Spec không ghi · Evidence: screenshot + dump `bot_slots` · Mẫu kho: `TC-BLP-398` |
| TC-PERM003-01 | UI | PERM-003 | Áp coupon khi vận hành nhiều bot | Abnormal | manual | product | Owner sở hữu 2 bot — coupon áp đúng hợp đồng đang mở, không theo bot đang chọn | - 1 owner sở hữu **2 bot** BA và BB, mỗi bot 1 hợp đồng trả phí HA và HB<br>- Ghi lại 次回決済(更新)日 của **cả hai**<br>- 1 coupon chưa dùng | 1. Chọn ngữ cảnh bot **BB** ở thanh chọn bot<br>2. Mở 契約情報・領収書 → mở chi tiết hợp đồng **HA** (của bot BA)<br>3. Áp coupon tại đây<br>4. Kiểm tra 次回決済(更新)日 của **cả HA và HB** | Owner 2 bot, ngữ cảnh BB nhưng thao tác trên HA | **HA** được gia hạn (hợp đồng đang mở), **HB giữ nguyên**. Bot BA được gia hạn, bot BB không đổi. Ngữ cảnh bot đang chọn không được quyết định hợp đồng nào bị ghi. | | Lấp `G2` / `Q2` · Buộc về điểm diff *"bỏ đọc `botId` từ request"* · Ngữ cảnh bot theo **session trình duyệt** (đổi ở 1 tab đổi cả trình duyệt) · Đánh giá spec: Spec không ghi · Evidence: screenshot màn list trước/sau (cả 2 dòng hợp đồng) |
| TC-FUNC004-01 | UI | FUNC-004 | Áp mã coupon — coupon đã dùng | Abnormal | manual | product | Áp lại mã coupon **đã dùng rồi** → bị từ chối, hợp đồng không gia hạn thêm | - Đã áp thành công mã C1 cho hợp đồng H1 (ghi lại 次回決済(更新)日 sau lần 1)<br>- Đăng nhập bằng chính chủ H1 | 1. Mở chi tiết H1 → 「クーポンコードを入力する」<br>2. Nhập lại **chính mã C1**<br>3. Bấm nút xem trước<br>4. Quan sát thông báo và 次回決済(更新)日 | coupon = C1 (đã dùng ở lần trước) | Hiện 「クーポンコードは無効です」 ngay ở bước xem trước. 次回決済(更新)日 **giữ nguyên** giá trị sau lần áp thứ nhất, không cộng thêm lần nữa. | | Lấp `G3` / `Q4` · Case này **từng có** trong NEW-7 v1, bị gỡ ở v2 không có TC thay thế · Nhánh validate coupon nằm ngay trên đoạn **đổi thứ tự** · Đánh giá spec: Spec không ghi · Evidence: screenshot + dump `coupon_management` + `bot_contracts` |
| TC-CONC001-01 | UI | CONC-001 | Áp mã coupon — đồng thời | Abnormal | manual | product | Double-click nút 「クーポンコードの利用を確定する」 → chỉ gia hạn **1 lần** | - Hợp đồng H1 正常, ghi lại 次回決済(更新)日<br>- 1 mã coupon C1 chưa dùng<br>- Mở DevTools tab Network để đếm request | 1. Mở modal coupon, nhập C1, qua bước xem trước<br>2. Bấm 「クーポンコードの利用を確定する」 **2 lần liên tiếp thật nhanh**<br>3. Đếm số request trong tab Network<br>4. Quan sát 次回決済(更新)日 và khu 操作履歴 | C1, double-click | Dù gửi 2 request, 次回決済(更新)日 **chỉ cộng 1 lần** mệnh giá coupon. Khu 操作履歴 chỉ có **1** dòng cho lần áp này. Request thứ 2 bị từ chối (nút disable hoặc trả 「クーポンコードは無効です」). | | Lấp `Q3` · Fix chèn thêm bước kiểm quyền **giữa** lúc đọc coupon và lúc khoá coupon ⇒ cửa sổ race rộng ra · Đánh giá spec: Spec không ghi · Evidence: HAR tab Network + screenshot 操作履歴 |
| TC-PERM002-01 | UI | PERM-002 | Phân quyền & staff — áp coupon | Boundary | manual | Tất cả | Staff bị **gỡ quyền `pointSettings` giữa 2 bước** preview và xác nhận | - Staff S có quyền `pointSettings` trên bot của hợp đồng H1<br>- 1 tài khoản owner mở sẵn màn quản lý thành viên<br>- 1 coupon chưa dùng | 1. Staff S mở chi tiết H1 → nhập coupon → bấm xem trước, **dừng ở màn xác nhận** (chưa bấm 確定)<br>2. Owner gỡ quyền `pointSettings` của S trên bot đó<br>3. Staff S bấm 「クーポンコードの利用を確定する」<br>4. Quan sát kết quả và trạng thái hợp đồng | Staff bị gỡ quyền giữa 2 bước | Request bị chặn — hiện 「クーポンコードは無効です」. 次回決済(更新)日 của H1 **không đổi**, coupon **không bị đốt**. Quyền phải được kiểm ở **thời điểm submit**, không phải thời điểm mở màn. | | Lấp `Q1` · **RULE-01** — bổ sung loại `Boundary` còn thiếu của `PERM-002` · Buộc về bước kiểm quyền **mới thêm** · Đánh giá spec: Spec không ghi · Evidence: screenshot màn staff sau khi bấm + dump `coupon_management` · Mẫu kho: `TC-BLP-385` |
| TC-DATADB001-01 | Data | DATA-DB-001 | Áp mã coupon — ghi dữ liệu | Normal | manual | product | Bản ghi coupon gắn đúng tài khoản/hợp đồng/tên bot khi 2 bot **trùng tên** | - userA chủ H1 (bot BA), userB chủ H2 (bot BB)<br>- **Đặt tên bot BA và BB giống hệt nhau**<br>- 2 coupon C1, C2 chưa dùng | 1. userA áp C1 lên H1<br>2. userB áp C2 lên H2<br>3. Đối chiếu bản ghi C1: đã dùng, gắn userA, gắn H1, có thời điểm dùng, tên bot = BA<br>4. Đối chiếu C2 tương tự với userB/H2<br>5. Xác nhận C1 không gắn nhầm sang H2 và ngược lại | 2 bot **trùng tên** + 2 coupon | Mỗi coupon gắn **đúng** tài khoản + đúng hợp đồng + đúng tên bot của mình, dù 2 bot trùng tên. Thời điểm dùng khớp lúc thao tác. Không bản ghi nào bị ghi đè chéo. | | Lấp `G5` · **RULE-07** — kiểm chứng phạm vi ghi bằng dữ liệu trùng tên · `bot_name` suy từ bot mà fix **đổi nguồn lấy bot** · Đánh giá spec: Spec không ghi · Evidence: dump `coupon_management` 2 dòng + screenshot 2 màn |
| TC-DATAAUDIT001-01 | Data | DATA-AUDIT-001 | Log ứng dụng khi áp coupon | Normal | manual | product | Log của `applyCouponCode` ghi đủ context sau khi đổi nguồn `bot_id` | - Quyền đọc log ứng dụng trên môi trường test<br>- Hợp đồng H1 + 1 coupon chưa dùng | 1. Ghi lại thời điểm bắt đầu<br>2. Áp coupon thành công cho H1<br>3. Mở log ứng dụng, tìm bản ghi của lần áp này<br>4. Đối chiếu bot ghi trong log với bot thật của H1 | H1 + coupon hợp lệ | Log có bản ghi cho lần áp coupon, ghi **đúng bot của hợp đồng H1** (không phải bot khác, không rỗng). Đủ để truy vết ai áp coupon nào lên hợp đồng nào khi khách khiếu nại. | | Lấp `G4` · Studio `dev_impact` nêu đích danh *"logInfo ghi bot_id từ `$botContract->bot_id` sau fix — cần xác nhận log vẫn đủ context"* · Đánh giá spec: Spec không ghi · Evidence: trích đoạn log |
| TC-REGSHARED001-01 | API | REG-SHARED-001 | Regression phân quyền chéo bot — endpoint billing | Abnormal | manual | product | Rà IDOR trên toàn bộ endpoint thao tác hợp đồng, không chỉ 2 endpoint coupon | - userA chủ hợp đồng HA (bot BA); userB không có quyền gì trên BA<br>- Lấy session + CSRF của userB | 1. Với từng URL trong danh sách 8 màn thao tác hợp đồng (`/basic/detail-contract/`, `/basic/change-bill-type/`, `/basic/change-payment-method/`, `/basic/detail/extend-contract/`, `/basic/detail-contract/{id}/cancel`, `/basic/re-contract/`, `/basic/change-card/`, `/basic/sub-card-setting/`) **cộng** 2 endpoint coupon: gửi request bằng session userB với id của HA<br>2. Ghi lại response từng endpoint<br>3. Sau mỗi request, kiểm tra hợp đồng HA và bot BA không đổi | id hợp đồng HA + session userB | **Toàn bộ 10 endpoint** đều từ chối và **không thay đổi** dữ liệu của HA/BA. Bất kỳ endpoint nào trả thành công hoặc ghi dữ liệu = IDOR còn sót ⇒ raise ticket **riêng**, không gộp vào #38785. | | ⚠️ **Không thuộc phạm vi verify fix #38785** — 8 endpoint kia không nằm trong diff. Đây là **audit tìm bug cùng loại**: bug IDOR ở tầng API thì phải rà cả lưới phân quyền, không chỉ endpoint được fix. Leader quyết định chạy trong ticket này hay tách ticket audit riêng. · Mở rộng ma trận kho `TC-BLP-386` (8 màn) thêm 2 endpoint coupon — coupon là màn thứ 9/10 không nằm trong ma trận cũ (spec gap MT-15) · Đánh giá spec: Spec không ghi · Evidence: bảng request/response 10 endpoint |

---

## 6. Spec update needed

| # | Nội dung cần chốt | Nguồn phát hiện | Ai chốt |
|---|---|---|---|
| 1 | **Endpoint + bảng dữ liệu của chức năng coupon chưa có trong spec FA-031.** `spec-features/admin/billing-plan/feature-spec.md` §9 **[M2]**: *"API Spec: không tìm thấy endpoint xử lý coupon; DB: không tìm thấy cột `coupon_code` trong `bot_contracts` (52 cột), không tìm thấy bảng `coupons`"*; §6 chỉ liệt kê 12 endpoint, thiếu coupon (kho MT-15). Chức năng đã **live trên production** (có nút 「クーポンコードを入力する」 + log sự kiện 「クーポンコードの適用」) nhưng không có spec ⇒ 12/12 TC hiện tại không có chuẩn đối chiếu Expected. | BƯỚC 1 + kho MT-23 | Dev + Leader |
| 2 | **Hợp đồng đúng chủ nhưng KHÔNG có bản ghi `bot_slots`** (chưa kết nối bot, hoặc dữ liệu lứa cũ) — bị chặn áp coupon là **đúng nghiệp vụ** hay là **regression do fix**? `Bots::dataBotContract` inner join `bot_slots` là chi tiết cài đặt, chưa có bằng chứng là business rule. Studio REQ-006 tự ghi *"cần xác nhận hành vi mong muốn"*; NEW-9 né bằng cách đổi Expected thành "kiểm tra dữ liệu test". **Đây là câu hỏi chặn `TC-FUNC001-01/02`.** | G1 + §4 #8 | Dev + Leader |
| 3 | **Loại sự kiện `bot_life_cycles` cho 「クーポンコードの適用」.** Spec FA-031 §2 ghi 「(chưa xác định type)」; NEW-1 khẳng định `type APPLY_COUPON`; NEW-4 (v2) gỡ giả định này. Kho MT-21 còn ghi nhận `bot_life_cycles` đang **dùng trùng mã type** giữa các sự kiện khác nhau. | §3 `DUP-CONFLICT` | Dev cung cấp bảng enum type đầy đủ |
| 4 | **CONFLICT báo cáo Dev ⟷ code thật về `botId`**: `03-dev-impact.md` mục 2 (chép nguyên văn Redmine #38785 Journal #125990) ghi *"`botId` vẫn lấy từ request như cũ"*, nhưng Studio `dev_impact` (suy từ diff `48877bb5b3`) ghi *"**bỏ đọc `botId` từ request** — `botId` nay lấy từ `$botContract->bot_id` qua `bot_slots`"*, và NEW-8/NEW-12 test theo hướng sau. Một trong hai sai. Note trên Redmine là thứ QA đời sau đọc để viết TC. | §4 #11 | Dev xác nhận trên diff, sửa lại note Redmine |
