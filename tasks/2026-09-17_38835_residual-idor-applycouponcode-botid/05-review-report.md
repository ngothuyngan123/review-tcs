# 05 — Review Report

## 0. Nguồn TC

- **Nguồn đã dùng**: MCP LME TEST STUDIO — task `#190` (ticket 38835, feature `coupon-management`, round 1, `reviewState=leader`, `reviewed=false`)
- **Tổng số TC review**: 10

---

## 1. Coverage — `dev-impact` + `diff code`

> **Phạm vi áp dụng**: diff chỉ **1 file, +12/−3** (`app/Http/Controllers/Admin/UserController.php:9611`), nội dung đúng 1 việc — **đổi nguồn lấy `botId`** từ `$request` sang `$botContract->bot_id`. Vùng cần TC vì vậy **chỉ gồm những chỗ nguồn dữ liệu này đổi**. Các vùng khác của luồng coupon (công thức cộng ngày, trạng thái hợp đồng, idempotency) **không nằm trong phạm vi** — xem khối cuối §1.

**Kết luận**: 9/12 vùng ảnh hưởng đủ TC · **2 GAP** · **1 RISK**

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Vấn đề | Severity |
|---|---|---|---|---|---|---|
| **G1** | diff code | `applyCouponCode` — nhánh `$botContract->bot_id` **rỗng/NULL**: hợp đồng có **slot chưa gắn bot** (`bot_slots.bot_id` nullable, `db-mapping.md` §2.1) | — | **GAP** | **Nhánh này do chính fix tạo ra**: trước fix `botId` đến từ request nên luôn có giá trị FE gửi; sau fix nó phụ thuộc `bot_slots` và **có thể NULL**. Hợp đồng mua slot nhưng chưa gắn LINE OA là trạng thái phổ biến và **vẫn mở được màn chi tiết** (kho `TC-BLP-132`, `TC-BLP-13`) → vẫn bấm được nút 「クーポンコードを入力する」. Khi `bot_id` NULL, `Bots::where(id,NULL)->update()` không chạm bot nào trong khi coupon và `bot_contracts` vẫn bị ghi → khách mất coupon, hợp đồng gia hạn nhưng bot thì không. Không TC nào chạm | `[BLOCKER]` |
| **G2** | diff code | Hợp đồng **Enterprise nhiều slot / nhiều bot** — `dataBotContract` join `bot_slots` (quan hệ **N:N**, "một hợp đồng có `number_slot` slots") | — | **GAP** | **Fix đổi ai là người chọn bot**: trước fix client chọn qua `botId`, sau fix server tự chọn `$botContract->bot_id`. Với hợp đồng Enterprise gắn nhiều bot (kho `TC-BLP-16`, `TC-BLP-63`, `TC-BLP-148`), join trả **nhiều dòng** → không xác định bot nào được gia hạn. Đây đúng là ca Dev tự gọi là "FE gửi botId khác bot của hợp đồng — trường hợp hợp lệ hiếm", nhưng Enterprise đa slot **không hiếm**. Không TC nào có hợp đồng > 1 bot | `[BLOCKER]` |
| **G3** | dev-impact `D4` | `bot_life_cycles` (type=29 APPLY_COUPON) → màn 「アクティビティログ」 (EP-06 `/ajax/bot-life-cycle`, SCR-BLP-04) | NEW-1, NEW-3, NEW-4 (chỉ tầng DB) | **RISK** | Studio `dev_impact` ghi rõ fix **đổi nguồn** `bot_life_cycles.admin_id` sang `$botContract->admin_id` và `logInfo bot_id` sang bot của hợp đồng. 3 TC chỉ query DB, **không TC nào mở màn lịch sử** → RULE-07 mới đủ 2/3 tầng. Kho `TC-BLP-228` cho thấy modal lịch sử có nhánh riêng khi hợp đồng chưa kết nối bot (liên quan G1) | `[MAJOR]` |

**Không có dòng `orphan`** — cả 10 TC đều trace được về `applyCouponCode` / `checkCouponCode` / màn hợp đồng.

### Vùng ĐÃ LOẠI khỏi phạm vi ticket (fix không chạm — `[AP-5]` over-coverage)

Các vùng dưới đây **chưa có TC nào bao giờ** và là rủi ro thật của tính năng coupon, nhưng hành vi **trước và sau fix giống hệt nhau** → không phải việc verify của ticket này. Đề nghị Leader mở **task test riêng cho tính năng coupon** (xem §6 mục 1):

| Vùng | Vì sao loại |
|---|---|
| Áp coupon khi hợp đồng 延滞中 / 解約待ち / 解約済み / 強制解約 | Fix không chạm logic trạng thái hợp đồng; nhánh này lỗi (nếu có) đã lỗi từ trước |
| Công thức cộng hạn: mốc cộng, biên ngày 29/30/31, hợp đồng đã quá hạn | Fix không chạm công thức, chỉ đổi **bot đích** nhận ngày đó. Kho FA-031 **MT-06** đã ghi nhận đây là mâu thuẫn mức CAO chưa chốt — vấn đề có sẵn |
| Đồng thời / idempotency: 2 tab, double-click cùng 1 coupon | Fix không chạm transaction hay cờ `is_used`; race tồn tại như nhau trước/sau |
| Job nền đọc `bots.expired_date` (`AutoPaymentJobUnivapay`, `HandleBillStripe`, `FlowDeleteBot`) + mốc `expired_date + 7 ngày` chặn trang LINE user (kho `TC-BLP-371`…`375`) | `spec_delta.files[]` chỉ có 1 file controller — không chạm code job. Hệ quả sai giá trị đã bắt ở G1/G2 ngay tại tầng ghi |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 15 quan điểm Trigger khớp task · 11 đã cover đủ · **4 chưa cover đủ**

| Mã | Quan điểm | Ưu tiên | Vì sao Trigger khớp **và fix có chạm** | Tình trạng TC | Severity |
|---|---|---|---|---|---|
| **Q1** | `PERM-003` | Cao | "tổ chức vận hành **nhiều LINE OA**" — fix chuyển việc chọn bot sang server, hợp đồng Enterprise gắn nhiều bot qua `bot_slots` | **GAP** — không TC nào có hợp đồng > 1 bot (→ G2) | `[BLOCKER]` |
| **Q2** | `STATE-001` | Cao | "≥2 bước ghi dữ liệu tuần tự" — fix đặt bước ghi `bots` phụ thuộc kết quả của bước tra hợp đồng, tạo ra nhánh "ghi được 3 bảng nhưng không ghi được bot" | **GAP** — không TC nào test nhánh `bot_id` NULL. Chính note của NEW-5 đã nêu nghi vấn rồi bỏ ngỏ ("pre-existing STATE-001 — không kết luận bug ở đây") (→ G1) | `[BLOCKER]` |
| **Q3** | `DATA-AUDIT-001` | Cao | "thao tác đổi trạng thái trên dữ liệu nhạy cảm (**thanh toán/hợp đồng**); dấu hiệu spec: màn 操作履歴" — fix đổi nguồn `admin_id` + `bot_id` ghi vào log | **RISK** — chỉ verify DB, không verify màn lịch sử (→ G3) | `[MAJOR]` |
| **Q4** | `PERM-001` | Cao | "chức năng có phân biệt quyền" — sau fix, `dataBotContract` là **trust boundary duy nhất** quyết định `botId`; BR-07: Staff chỉ thấy hợp đồng được phân quyền qua `getListBotIdStaffManagement($userId,'pointSettings')` | **RISK** — chỉ NEW-10 (Normal, staff **có** quyền) và **chưa chạy lần nào**; thiếu Abnormal staff **không** có quyền | `[MAJOR]` |

**Quan điểm đã cover đủ (không ghi chi tiết)**: `FUNC-001` · `SEC-001` · `DATA-DB-001` · `OUT-TRUTH-001` · `REG-SHARED-001` · `PERM-002` · `DATA-001` · `SEC-002` · `FUNC-002` · `UI-003` · `INTG-002`.

**Đã loại khỏi phạm vi** (Trigger khớp nhưng fix không chạm — chi tiết ở khối cuối §1): `PAY-STATE-001` · `FUNC-DATE-001` · `CONC-001` · `JOB-001` · `REG-RUN-001`.

---

## 3. TC trùng lặp

**Đã rà 10/10 TC theo 4 yếu tố (mã quan điểm × loại case × đối tượng+thao tác × tiền đề tương đương) — không phát hiện cặp trùng cần xóa.**

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Happy path apply coupon | NEW-1 (UI) | **NEW-3 — KHÔNG xóa, giữ cả 2** | `DUP-SUBSET` (một phần) | Trùng: đối tượng+thao tác (apply coupon hợp lệ cho hợp đồng own), tiền đề, expected 4 bảng. **Khác**: mã quan điểm (`FUNC-001` vs `OUT-TRUTH-001`) và tầng kiểm chứng (UI browser vs craft request API). NEW-3 là đối chứng dương cùng tầng với NEW-4/5/7 | `[NIT]` |

- **Gate xóa đã chạy**: giả định xóa NEW-3 → `OUT-TRUTH-001` chỉ còn NEW-9 (**chưa chạy lần nào**) → mất cover. Theo quy tắc "không xóa TC duy nhất cover một quan điểm" → đổi sang **giữ nguyên**.
- NEW-4 / NEW-7 / NEW-8 cùng `SEC-001` + Abnormal nhưng **khác tiền đề** (bot khác tenant · botId rỗng/0 · bot cùng owner khác contract) → 3 chiều rủi ro riêng, không trùng.
- Không có `DUP-INFLATE` → không dòng nào ở §1/§2 bị trùng lặp che GAP.

---

## 4. Issues khác

### Chất lượng nguồn TC

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 1 | `[MAJOR]` | Toàn bộ task #190 | **Tỷ lệ pass thật = 7/10 = 70% (< 80%)**. 3 TC **chưa chạy lần nào**: NEW-8 (`priority=High`, IDOR cùng tenant), NEW-9, NEW-10 — đều do người (`cucdtk@mcp`) thêm ngày 2026-09-16, **sau** run duy nhất 2026-08-24. Có TC ≠ đã test. **Đây là việc rẻ nhất và quan trọng nhất của đợt này** — ưu tiên hơn cả 4 TC mới ở §5 | Chạy 3 TC còn lại trước khi kết luận fix đạt |
| 2 | `[MAJOR]` | Toàn bộ task #190 | **RULE-08 / ENV-003** — chỉ **1 run duy nhất** (`#446`), `env = local`, do `pipeline` AI chạy. `dev` / `staging` / `prd` đều **0 run**; **không TC nào khai `env_scope = prd`**. Task chạm **bill tiền / hạn hợp đồng** → không được kết luận từ local | Bổ sung run ở staging, và chạy tối thiểu bộ TC giá trị tiền/hạn ở production |
| 3 | `[MAJOR]` | Toàn bộ task #190 | **RULE-02 — không có evidence dạng artifact**. `task_get_report` có trường `actual` mô tả chi tiết, nhưng `artifacts: []` ở cả 7 kết quả và cột `Evidence thực tế` rỗng 10/10 → kết quả là **text tự khai của runner**, không có ảnh/log đối chứng | Yêu cầu runner đính kèm dump DB before/after + response JSON làm artifact |
| 4 | `[MAJOR]` | Toàn bộ task #190 | Cột **`Trạng thái đánh giá spec` rỗng 10/10 TC** (`spec_status = null`) trong khi spec FA-031 **không có** business rule cho coupon (xem #5) → mọi Expected hiện là suy diễn chưa ai xác nhận | Điền `Spec không ghi` + ghi rõ đã hỏi ai, hoặc chốt spec (→ §6) |
| 5 | `[MAJOR]` | Spec nguồn | **Không có spec cho hành vi apply coupon.** `spec-features/admin/billing-plan/feature-spec.md` §9 **[M2]** ghi rõ: "UI có button 「クーポンコードを入力する」… API Spec: **không tìm thấy endpoint** xử lý coupon; DB: **không tìm thấy** cột `coupon_code` / bảng `coupons`". §6 chỉ có 12 endpoint, coupon nằm trong danh sách "chưa tìm thấy endpoint". Kho FA-031 **MT-23** xác nhận: "cả spec lẫn TCs đều bỏ trống — KHÔNG có TC nào trong kho" | Dùng ticket này bổ sung spec §6 + §2 (→ §6 report) |
| 6 | `[MINOR]` | NEW-6 | Mã quan điểm **`TOOL-ERRHYG-001` không có trong `framework/checklist-lme.md`** (mã nội bộ Studio) → NEW-6 **không tính là cover** quan điểm LME nào. Các mã chỉ xuất hiện trong `Ghi chú` (`TOOL-KNOW-002`, `TOOL-NEGCTRL-001`, `DATA-DB-001`, `STATE-001`) cũng không map được | Gán thêm mã LME thật cho NEW-6 (gần nhất: `FUNC-002` / `UI-003`) |
| 7 | `[MAJOR]` | `03-dev-impact.md` | **Auto-fill chưa được tester verify** — file có `Auto-filled: 2026-09-17 by /new-task`, checkbox "Tester verify auto-fill chính xác" **chưa tick**. Mục 4.1 của Dev chỉ liệt kê **file**, không liệt kê function; mục 4.2 khai **"Không có data ảnh hưởng"** dù luồng UPDATE 4 bảng; mục 4.3 **không ghi mức nguy cơ regression** | Tester đọc lại Journal #126738 và tick checkbox trước khi review có hiệu lực |
| 8 | `[MAJOR]` | Dev — audit code, **không phải việc của QA** | **Sibling cùng lớp bug chưa được kê.** Mục 3 file 03 chỉ kê 3 function trong cùng 1 file + 1 model; không kê nơi nào khác mutate `bots` / `bot_contracts` theo id lấy thẳng từ request. Cùng lớp bug IDOR đã lặp **2 vòng** (#38785 → #38835). Kho FA-031 **MT-15** liệt kê 8 URL thao tác hợp đồng (`change-bill-type`, `change-payment-method`, `detail/extend-contract`, `{id}/cancel`, `re-contract`, `change-card`, `sub-card-setting`, `detail-contract`) | **Dev grep source** tìm các chỗ còn đọc id định danh từ request rồi mutate (rẻ hơn nhiều so với QA craft 8 request). Chỉ khi grep còn ra điểm nghi vấn mới cần TC — xem TC-REGSHARED001-01 (điều kiện) ở §5 |

### Chất lượng từng TC

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 9 | `[MAJOR]` | NEW-5 | **Expected quá lỏng + thông báo sai nguyên nhân.** Expected chấp nhận "`status:false` **hoặc** lỗi do `$botContract` null". Evidence run cho thấy hệ thống trả 「クーポンコードは無効です」 (= *mã coupon vô hiệu*) trong khi coupon của A **hoàn toàn hợp lệ**, lỗi thật là **không có quyền trên hợp đồng** → user bị hiểu nhầm coupon hỏng, và thông báo này che dấu hiệu tấn công | Chốt message đúng cho ca sai quyền (→ §6), rồi siết Expected thành 1 giá trị cụ thể |
| 10 | `[MAJOR]` | NEW-10 | **Steps không đủ để người khác dựng lại env.** 3 bước ở mức tiêu đề: "Đăng nhập bằng Staff A" / "Gửi apply-coupon-code với contract CA" / "Kiểm tra DB sau khi apply" — không nêu cách cấp quyền `pointSettings`, không nêu bot/contract cụ thể, không nêu bảng/field cần đối chiếu. `requirement_keys` cũng rỗng | Viết lại steps kèm bước cấp quyền + danh sách field verify |
| 11 | `[MINOR]` | NEW-9 | Bước 1 "Apply coupon thành công cho contract CA" gói cả một luồng vào 1 dòng; `requirement_keys` rỗng | Tách bước hoặc dẫn chiếu `NEW-1` làm tiền đề |
| 12 | `[MINOR]` | NEW-6 | **Không atomic** — 1 TC gộp 2 ca lỗi khác nhau (mã không tồn tại · mã đã dùng) với 2 expected riêng | Tách thành 2 TC |
| 13 | `[MAJOR]` | `[AP-3]` Happy-path-only regression | `T1` (FS-015) và `T2` (FA-031) mỗi cái chỉ có TC với tiền đề "hợp đồng 正常, **đúng 1 bot đã gắn**, data sạch" — tức đúng cấu hình mà fix **không** làm đổi hành vi. Không TC nào chạy ở cấu hình mà fix **có** làm đổi: slot trống, Enterprise đa slot | Xem TC đề xuất §5 |

---

## 5. TCs đề xuất bổ sung (4)

> **Nguyên tắc cắt phạm vi**: fix chỉ đổi **nguồn lấy `botId`**. TC bổ sung vì vậy **chỉ** phủ những cấu hình dữ liệu mà nguồn mới cho kết quả **khác** nguồn cũ (slot trống → NULL; nhiều slot → không xác định; quyền staff → quyết định `botId`), cộng 1 TC xác nhận tầng hiển thị của log đã đổi nguồn. Bản review trước liệt kê 15 TC — 10 TC đã bị **loại vì fix không chạm** (`[AP-5]`, lý do ở khối cuối §1), và **TC-PERM003-01 (Enterprise nhiều slot) do Leader loại ngày 2026-09-17** — GAP G2/Q1 vẫn để ngỏ, chốt quy tắc ở §6 mục 2 trước.

**Xác nhận đối chiếu** — đã đọc `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (nhóm『Rule slot trống & bot free』`TC-BLP-56…63`, 『Detail hợp đồng — enterprise』`TC-BLP-143…152`, 『Phân quyền & staff』`TC-BLP-379…390`, 『Lịch sử thao tác hợp đồng』`TC-BLP-222…230`) và 10 TC ở BƯỚC 0 — **không TC đề xuất nào trùng**. Kho FA-031 **MT-23** xác nhận kho chưa có bất kỳ TC coupon nào, nên không dẫn chiếu lại được TC kho; các TC kho ở trên chỉ dùng làm **bằng chứng cấu hình có thật**.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-STATE001-01 | UI | STATE-001 | Chi tiết hợp đồng — áp mã coupon | Abnormal | manual | product | Áp coupon cho hợp đồng có slot CHƯA gắn bot | - Tài khoản A đã mua 1 slot standard/pro, thanh toán thành công, **chưa gắn LINE OA nào vào slot** (màn list hiện 「LINE公式アカウント未接続」)<br>- A có 1 mã coupon hợp lệ chưa dùng<br>- Ghi lại ngày ở cột 次回決済(更新)日 của hợp đồng này | 1. Mở /basic/point-settings, xác nhận dòng hợp đồng hiện 「LINE公式アカウント未接続」<br>2. Click vào dòng đó để mở màn chi tiết hợp đồng<br>3. Bấm 「クーポンコードを入力する」, nhập mã coupon hợp lệ<br>4. Bấm nút kiểm tra → ghi lại ngày gia hạn dự kiến<br>5. Bấm 「適用」, ghi lại thông báo trả về<br>6. Quay lại màn list, đọc cột 次回決済(更新)日<br>7. Thử áp **lại đúng mã coupon đó** một lần nữa<br>8. Lặp lại toàn bộ với 1 hợp đồng vừa bị **gỡ bot khỏi slot** (slot trở về trống) | coupon hợp lệ chưa dùng; hợp đồng slot trống của A | Hệ thống xử lý **nhất quán, không để trạng thái nửa vời** — 1 trong 2: (a) chặn từ đầu, thông báo nêu rõ hợp đồng chưa gắn LINE OA, ngày ở cột 次回決済(更新)日 **không đổi**, và mã coupon **vẫn dùng lại được** ở bước 7; hoặc (b) áp thành công và ngày ở cột 次回決済(更新)日 đổi đúng bằng ngày dự kiến ở bước 4. **KHÔNG được**: báo thành công nhưng ngày không đổi, hoặc coupon bị tiêu ở bước 7 trong khi không bot nào được gia hạn | | Lấp G1 · Q2 · `[AP-3]` · Nhánh `bot_id` NULL **do chính fix tạo ra** · Cấu hình có thật: kho `TC-BLP-132` (slot chưa kết nối bot vẫn mở được màn chi tiết) + `TC-BLP-13` · Bước 8 gộp ca gỡ bot vì trạng thái cuối giống nhau · RULE-08: liên quan tiền → product · Evidence: ảnh màn list trước/sau + ảnh thông báo + ảnh kết quả bước 7 |
| TC-PERM001-01 | API | PERM-001 | Áp mã coupon — phạm vi quyền Staff | Abnormal | manual | Tất cả | Staff KHÔNG được phân quyền pointSettings không áp được coupon | - Admin A có hợp đồng CA gắn bot BA<br>- Tạo Staff S thuộc A nhưng **KHÔNG** cấp quyền `pointSettings` cho bot BA<br>- Staff S đăng nhập thật, có session + CSRF<br>- Có 1 coupon hợp lệ chưa dùng<br>- Ghi lại hạn của hợp đồng CA và bot BA | 1. Staff S đăng nhập, mở /basic/point-settings → xác nhận **không thấy** hợp đồng CA trong danh sách<br>2. Staff S mở thẳng URL màn chi tiết hợp đồng CA → ghi lại kết quả<br>3. Craft request áp coupon với `botContractId` = CA bằng session của S<br>4. Đọc thông báo trả về<br>5. Đọc lại hạn của hợp đồng CA và bot BA<br>6. Kiểm tra coupon còn dùng lại được không | Staff S không có quyền; coupon hợp lệ; hợp đồng CA | Cả 3 tầng đều chặn: không thấy ở màn list, mở thẳng URL bị chặn, và **request craft cũng bị chặn** — hạn của CA và BA không đổi, coupon không bị tiêu | | Lấp Q4 (chiều Abnormal mà NEW-10 thiếu) · Sau fix `dataBotContract` là **trust boundary duy nhất** của `botId` → nhánh từ chối quyền nay quyết định luôn việc có ghi `bots` hay không · BR-07 spec: `getListBotIdStaffManagement($userId,'pointSettings')` · Kho `TC-BLP-382`/`387` có nhánh staff không quyền nhưng **chưa có** nhánh coupon · group=api vì bước 3 phải craft request |
| TC-DATAAUDIT001-01 | UI | DATA-AUDIT-001 | Lịch sử thao tác hợp đồng (アクティビティログ) | Normal | manual | Tất cả | Lịch sử 「クーポンコードの適用」 hiện đúng bot và người thực hiện của hợp đồng | - Tài khoản A có hợp đồng CA gắn bot BA, có coupon hợp lệ chưa dùng<br>- A là chủ hợp đồng CA | 1. Áp coupon thành công cho hợp đồng CA (theo NEW-1)<br>2. Mở khu 「操作履歴 / アクティビティログ」 của hợp đồng CA<br>3. Tìm dòng mới nhất 「クーポンコードの適用」<br>4. Click vào dòng đó để mở modal chi tiết<br>5. Đọc tên bot và người thực hiện hiển thị trong modal | coupon hợp lệ; hợp đồng CA | Dòng 「クーポンコードの適用」 xuất hiện đúng thời điểm. Modal chi tiết hiện **tên bot BA** (bot thật của hợp đồng) và **chủ hợp đồng A** — không hiện bot khác, không bỏ trống tên bot | | Lấp G3 · Q3 · Fix **đổi nguồn** `bot_life_cycles.admin_id` → `$botContract->admin_id` và `logInfo bot_id` (Studio `dev_impact`) → phải verify tầng hiển thị, không chỉ tầng DB (RULE-07) · Kho `TC-BLP-222`/`223`/`228` mô tả cấu trúc màn lịch sử · Evidence: ảnh modal lịch sử |
| TC-REGSHARED001-01 | API | REG-SHARED-001 | 8 màn thao tác hợp đồng — rà IDOR tầng ghi | Abnormal | manual | Tất cả | **(CÓ ĐIỀU KIỆN)** Rà sibling: thao tác hợp đồng khác có còn tin tham số định danh từ request không | ⚠️ **Chỉ chạy khi Dev đã grep source (§4 #8) và còn điểm nghi vấn** — đây là TC đắt, chỉ nên chạy cho những màn Dev không khẳng định được<br>- 2 tài khoản: A (có hợp đồng CA + bot BA) và B (có hợp đồng CV + bot BV)<br>- A đăng nhập thật, có session + CSRF<br>- Ghi lại trạng thái, hạn, kỳ thanh toán, phương thức, thẻ của hợp đồng CV trước test | 1. Với **từng màn Dev còn nghi vấn**: mở màn đó bằng hợp đồng CA của chính A, thao tác tới bước xác nhận cuối<br>2. Tại bước gửi đi, sửa tham số định danh trong request thành id của B (`botId`=BV và/hoặc `botContractId`=CV), rồi gửi<br>3. Đọc thông báo trả về<br>4. Mở màn hợp đồng của B kiểm tra trạng thái, hạn, kỳ thanh toán, phương thức, thẻ có bị đổi không<br>5. Lập bảng kết quả theo từng màn | Mỗi màn: 1 request hợp lệ của A + 1 request đã sửa id sang của B | Không thao tác nào của A làm đổi bất kỳ dữ liệu nào của B. Màn nào để lọt → bug IDOR cùng lớp với #38835, **raise ticket riêng cho màn đó** (không gộp vào ticket này) | | Lấp §4 #8 · Danh sách 8 màn lấy từ kho FA-031 **MT-15** (`「Quản lý hợp đồng」r820-r827`) · Kho `TC-BLP-386` mới cover chặn **mở màn**, TC này cover tầng **ghi** · group=api vì phải sửa tham số request · **Ngoài phạm vi verify fix #38835** — đây là chặn tái phát cùng lớp bug đã lặp 2 vòng |

<!-- synced: Studio task #190 — 2026-09-17 -->
**Đã push lên Studio task #190** (2026-09-17, `testcase_create`, actor `@mcp`) — `client_ref` = cột `ID` nên chạy lại sẽ không tạo trùng:

| ID (§5) | Studio | temp_id |
|---|---|---|
| `TC-STATE001-01` | #18487 | **NEW-11** |
| `TC-PERM001-01` | #18488 | **NEW-12** |
| `TC-DATAAUDIT001-01` | #18489 | **NEW-13** |
| `TC-REGSHARED001-01` | #18490 | **NEW-14** |

Cả 4 ở trạng thái `draft`, chưa chạy. Cột `Ghi chú` của §5 **không** được đẩy lên Studio (chỉ phục vụ report local). `surfaces` để trống = TC web — đúng với các TC này vì chúng thao tác trên màn admin / ajax nội bộ, không gọi public API `/v1` từ ngoài.

### Ánh xạ GAP/quan điểm → TC

| Mã | TC đề xuất | Ghi chú |
|---|---|---|
| G1 · Q2 | TC-STATE001-01 | **Thiếu Normal/Boundary** (RULE-01): Normal = hợp đồng gắn đúng 1 bot đã có NEW-1/NEW-3 pass; slot trống **chính là** giá trị biên của `bot_id` |
| G2 · Q1 | **— Leader quyết định KHÔNG viết TC** (2026-09-17) | GAP vẫn để ngỏ ở §1/§2: hợp đồng Enterprise nhiều bot chưa có TC nào xác định bot nào được gia hạn. Chốt quy tắc ở §6 mục 2 trước, cần TC thì mở sau |
| G3 · Q3 | TC-DATAAUDIT001-01 | **Thiếu Abnormal/Boundary** (RULE-01): màn lịch sử chỉ đọc, fix không tạo nhánh lỗi mới ở đây |
| Q4 | TC-PERM001-01 | Normal đã có NEW-10 — **nhưng NEW-10 chưa chạy lần nào**, phải chạy trước (§4 #1) |
| §4 #8 | TC-REGSHARED001-01 | Có điều kiện — chỉ chạy sau khi Dev grep source |

---

## 6. Spec update needed

| # | Nội dung cần chốt | Vì sao | Ai chốt |
|---|---|---|---|
| 1 | **Bổ sung toàn bộ spec cho chức năng coupon vào FA-031**: endpoint `apply-coupon-code` / `check-coupon-code`, bảng `coupon_management`, quy tắc gia hạn. Kèm theo: mở **task test riêng cho tính năng coupon** phủ các vùng đã loại khỏi ticket này (trạng thái hợp đồng · công thức cộng ngày · idempotency) | `spec-features/admin/billing-plan/feature-spec.md` §9 **[M2]** ghi rõ chưa tìm được endpoint và bảng; §6 liệt kê 「クーポンコードを入力する」 trong nhóm "chưa tìm thấy endpoint". Kho FA-031 **MT-23** xác nhận cả spec lẫn TC đều trống — **tính năng đang chạy production mà chưa từng có TC nào**. Ticket này là lần đầu có đủ thông tin để lấp | Dev + Leader |
| 2 | **Quy tắc chọn bot khi hợp đồng có nhiều slot / slot trống**: `dataBotContract` trả bot nào khi hợp đồng Enterprise gắn nhiều bot? Khi `bot_slots.bot_id` là NULL thì được phép áp coupon không? | **Câu hỏi trực tiếp của fix này** — fix chuyển nguồn `botId` từ client sang server (`$botContract->bot_id`) nhưng `bot_slots` là quan hệ **N:N** ("một hợp đồng có `number_slot` slots", `bot_id` nullable — `db-mapping.md` §2.1). Không có quy tắc thì không viết được Expected cho TC-PERM003-01 / TC-STATE001-01 | Dev |
| 3 | **Thông báo lỗi khi `botContractId` không thuộc quyền người dùng** | Evidence run `#446` của NEW-5: hệ thống trả 「クーポンコードは無効です」 (*mã coupon vô hiệu*) trong khi coupon hoàn toàn hợp lệ — lỗi thật là không có quyền trên hợp đồng. Message hiện tại gây hiểu nhầm cho khách thật và che dấu hiệu tấn công. Expected của NEW-5 đang chấp nhận cả 2 khả năng nên không bắt được | Dev + Leader |
| 4 | **Bảng enum `bot_life_cycles.type`** — xác nhận `type=29` = 「クーポンコードの適用」 | Spec §2 ghi 「クーポンコードの適用 \| (chưa xác định type)」; kho **MT-21** còn ghi nhận nghi vấn **trùng mã type** giữa các sự kiện khác nhau (type 16, 24). TC-DATAAUDIT001-01 cần enum đúng để đối chiếu | Dev |

> **Đã chuyển sang task riêng** (không chặn ticket #38835): công thức cộng hạn khi áp coupon (mốc cộng · ngày 29/30/31 · hợp đồng đã quá hạn — kho **MT-06** ghi nhận mâu thuẫn mức CAO) và quy tắc cho phép áp coupon theo trạng thái hợp đồng. Cả hai là vấn đề có sẵn, fix #38835 không chạm.
