# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #162 (ticket 39526, round 1) |
| Tổng số TC review | 19 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: `1/13 vùng ảnh hưởng đủ TC (T2 — popup/API đọc cờ) · 3 GAP · 9 RISK` (các RISK cùng gốc được gộp thành G2 · G3 · G6 · G7).

> ⚠️ **Input thiếu (chiều diff code)**: `spec_delta` trên Studio tính ngày **2026-08-25** — chỉ có commit `8748629bbd` (+5 dòng, nhánh lỗi). Commit **`88307c747a`** (2026-09-19, nhánh thành công bật lại cờ) **chưa có trong diff Studio** → điểm sửa này chỉ suy được từ mô tả ở `03-dev-impact.md` mục 2. Cần sync lại diff trên Studio.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Nhánh mới của commit `88307c747a`: **tạo sheet thành công khi cờ đang = 0 ⇒ bật lại 1** (D1) | `diff code` | NEW-9 (expected **ngược**: "cờ vẫn = 0"), NEW-3 / NEW-18 (chỉ ca cờ đang = 1) | GAP — không TC nào verify đúng hành vi mới; nhánh điều kiện `cờ = 0` hoàn toàn chưa có TC | `[BLOCKER]` |
| G2 | Fix dạng **generic catch** (`\Exception` tổng quát) — mọi lỗi tạo sheet đều đánh dấu mất liên kết | `diff code` | NEW-1 (token rác), NEW-17 (revoke thật), NEW-8 (lỗi non-auth) | RISK — mới có 3 trigger trên thiết kế và **chưa chạy cái nào** (NEW-1/8 `skip`, NEW-17 chưa chạy). Chưa có trigger lỗi tạm thời (429 / timeout / 5xx), và chưa có trigger "chưa biết" để test fallback. Expected của NEW-8 chưa chốt (§6) | `[MAJOR]` |
| G3 | `BUG` + F1 + D1 + T1 + D2 — job `form-answer:create-google-sheet` lỗi ⇒ cờ = 0, record chuyển ERROR, retry giữ nguyên | `dev-impact` | NEW-1, 2, 4, 5, 6, 7, 10 (`skip`), NEW-17 (chưa chạy) | RISK — **0 TC pass** cho luồng chính của fix. Có TC ≠ đã test | `[BLOCKER]` |
| G4 | Cùng 1 bot, cùng 1 lượt job: form A **lỗi** + form B **thành công** ⇒ cờ cuối cùng phụ thuộc thứ tự xử lý (A trước → B bật lại 1 → cảnh báo biến mất dù A vẫn thiếu sheet) | `diff code` | không có (NEW-6 chỉ có ca 2 form cùng lỗi) | GAP — hệ quả trực tiếp của việc ghép commit mới vào vòng lặp; hành vi đúng chưa chốt (§6) | `[MAJOR]` |
| G5 | T3 — **màn biểu mẫu bản cũ** (`FormAnswerController::index` / index_v2): banner mời liên kết lại | `dev-impact` | không rõ — NEW-11/12/13 ghi màn "index_v2" nhưng các bước là popup ajax `/ajax/google-sheet-active` của màn mới | GAP — không TC nào mô tả banner của màn cũ | `[BLOCKER]` |
| G6 | T4 — job đồng bộ câu trả lời `AddResultFormAnswerToGoogleSpreadSheet` dùng chung cờ (Dev: cờ = 0 **không** chặn đồng bộ) | `dev-impact` | NEW-19 (manual, chưa chạy, chỉ ca cờ = 1) | RISK — chưa có TC cho khẳng định chính của Dev: **cờ = 0 mà token còn hợp lệ ⇒ câu trả lời vẫn đồng bộ** | `[MAJOR]` |
| G7 | D3 — sau khi liên kết lại, form còn thiếu `google_sheet_id` phải được tạo sheet | `dev-impact` | NEW-16 (chưa chạy; chỉ kiểm cờ + popup) | RISK — expected dừng ở màn admin, chưa verify file trên Google Drive (RULE-06) | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `11 quan điểm Trigger khớp task · 8 chưa cover đủ`.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `JOB-001` | Cao | GAP — TC job chỉ gắn mã lạ `JOB-002` / `TOOL-*` (NEW-1, 3, 4, 5, 18) nên không tính là cover. Chưa có TC đối chiếu "số form vào = số tạo thành công + số vào hàng lỗi" | `[BLOCKER]` |
| Q2 | `REG-RUN-001` | Cao | GAP — nội dung có ở NEW-7 nhưng mã `TOOL-OLDREC-001` là mã lạ. Chưa xét record **đã hết lượt thử lại trước khi deploy** (xem §4 I9, §6) | `[BLOCKER]` |
| Q3 | `COMPAT-LEGACY-001` | Cao | GAP — cặp màn cũ (banner index) ⇄ màn mới (popup) chỉ có TC nhánh mới — xem G5 | `[BLOCKER]` |
| Q4 | `CONC-001` | Cao | GAP — job chạy mỗi phút và user bấm 「再連携する」 cùng ghi `bots.google_sheet_status`. Chưa có TC cho ca job đang chạy dở với token cũ thì user liên kết lại | `[BLOCKER]` |
| Q5 | `OUT-TRUTH-001` | Cao | RISK — đủ Normal/Abnormal/Boundary (NEW-12/11/13, đã pass) nhưng cả 3 đều **seed cờ bằng DB**. TC end-to-end duy nhất (job lỗi thật ⇒ popup) là NEW-17, chưa chạy | `[MAJOR]` |
| Q6 | `STATE-CLEAN-001` | Cao | RISK — NEW-16 (Normal, chưa chạy) + NEW-9 (expected sai theo G1). Thiếu Boundary; chưa verify output cuối sau khi liên kết lại (G7) | `[MAJOR]` |
| Q7 | `DATA-DB-001` | Cao | RISK — có NEW-2 (WHERE scope nhánh lỗi, `skip`). Chưa có TC WHERE scope cho **nhánh bật lại cờ** (G1); thiếu Normal/Boundary (RULE-01) | `[MAJOR]` |
| Q8 | `INTG-SHEET-001` | Cao | RISK — Kiểm tra bắt buộc có "quyền truy cập bị đổi" và "rate limit API": revoke (NEW-17) chưa chạy, rate limit chưa có TC (gắn với G2 + chưa chốt ở §6) | `[MAJOR]` |

> `REG-SHARED-001` và `ENV-003` cũng Trigger khớp: thiếu của REG-SHARED nằm ở G5/G6; thiếu của ENV-003 (0 TC chạy production) nằm ở §4 I4.
> Đã loại khỏi phạm vi: `OUT-EXPORT-001` (fix không đổi nội dung/format file Google) · `SEC-002` (fix không đổi cách lưu/đọc token) · `DATA-CACHE-001` (Studio gắn cho NEW-6 là cache in-memory của job, không khớp Trigger JS/asset/short link — ý của NEW-6 thuộc JOB-001).

---

## 3. TC trùng lặp nội dung

Đã rà 19 TC.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-18 | NEW-3 → **gộp** vào NEW-18 | `DUP-SUBSET` | `JOB-002` × Normal × job tạo sheet thành công × bot đang liên kết, token hợp lệ → sheet được tạo, cờ giữ = 1 (NEW-18 là bản nhiều form của NEW-3) | `[MINOR]` |

- **Gate đã chạy**: bỏ NEW-3 thì coverage §1/§2 vẫn còn, vì NEW-18 cover cùng nhánh. Khi gộp, chuyển phần expected chi tiết của NEW-3 (record `DONE(2)`, message `Success !!!`) sang NEW-18.
- `DUP-INFLATE`: không có.
- `DUP-CONFLICT` giữa 2 TC: không có. NEW-9 mâu thuẫn với **code hiện tại**, không phải với TC khác → xem §4 I2 + §6.
- Xóa/gộp thật do human thực hiện trên Studio (`testcase_update` / `testcase_delete`).

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ task #162 | Chỉ **5/19 TC pass (26%)**: 8 `skip` + 6 chưa chạy. Cả 5 TC pass đều là TC đọc cờ ở tầng UI/API; luồng job, là nơi thật sự bị sửa, chưa có kết quả nào | Chạy lại toàn bộ sau khi xác nhận commit `88307c747a` đã lên branch. Ghi rõ lý do `skip` cho 8 TC job (theo Dev: local/dev không có tài khoản Google) |
| I2 | `[MAJOR]` | NEW-9 | Expected "cờ VẪN = 0 sau khi retry thành công" viết theo bản fix 2026-08-19; commit `88307c747a` đã đổi hành vi thành **bật lại = 1**. Chạy theo TC này sẽ ra kết luận sai | Sửa NEW-9 trên Studio: expected = cờ về 1 và popup biến mất; bỏ tiền tố `[Conflict]`. Hoặc thay bằng TC-JOB001-01 ở §5 |
| I3 | `[MAJOR]` | Toàn bộ kết quả + diff Studio | Run cuối 2026-09-03 và `spec_delta` 2026-08-25 đều **cũ hơn** commit `88307c747a` (2026-09-19). Journal #137196 vừa ghi "CHƯA PUSH" vừa ghi "[đã push]" | Hỏi Dev xác nhận branch `ai_fixbug_39526` đã có `88307c747a`. Sync lại `spec_delta`/`dev_impact` trên Studio, rồi chạy lại |
| I4 | `[MAJOR]` | Toàn bộ — RULE-08 / ENV-003 | Task sửa **job nền** mà 0 TC chạy production; 13/19 TC gắn `env_tag = local-only`. Theo `ENV-003`, production tách job khác dev/staging | Chạy NEW-17 ở **production** (khớp TC kho `TC-FORM-369` — Môi trường: PRODUCTION). Không kết luận luồng job từ local |
| I5 | `[MAJOR]` | NEW-1, 3, 4, 5, 7, 8, 10, 15, 18 | 6 mã quan điểm không có trong `checklist-lme.md` (`JOB-002`, `API-001`, `TOOL-KNOW-002`, `TOOL-OLDREC-001`, `OBS-001`, `TOOL-NEGCTRL-001`) ⇒ 9 TC không được tính là cover (gây Q1, Q2) | Gắn lại mã trên Studio: `JOB-002` → `JOB-001` · NEW-7 → `REG-RUN-001` · NEW-8 → `INTG-SHEET-001` · NEW-10 → `DATA-DB-001` · NEW-1 → `JOB-001` · NEW-15 → `OUT-TRUTH-001` |
| I6 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill by `/new-task`, checkbox "Tester verify auto-fill chính xác" chưa tick | Tester đọc lại journal #137196 rồi tick |
| I7 | `[MAJOR]` | 19/19 TC | `Trạng thái đánh giá spec` để trống toàn bộ. `feature-spec.md` BR-08 **không mô tả** cờ `google_sheet_status` / cảnh báo mất liên kết ⇒ expected đang tự suy từ code | Ghi `Spec không ghi` + nguồn chốt (Leader chốt MT-15 ở kho FA-011 / journal Dev) cho từng TC |
| I8 | `[MAJOR]` | NEW-11, 12, 13 | Cột màn ghi "Form Answer **index_v2**", nhưng Dev nói index_v2 là **màn bản cũ dùng banner**, còn các bước của 3 TC là popup ajax của màn mới → không biết đang test màn nào | Ghi đúng URL màn đã test; banner màn cũ tách sang TC riêng (§5 TC-COMPATLEGACY001-01/02) |
| I9 | `[MAJOR]` | Dev mục 4 "Không cần recover data" — RULE-04 | Form có record đã **lỗi đủ 3 lần trước khi deploy** sẽ không được job xử lý lại (NEW-5) ⇒ bot vẫn báo "đang liên kết", form vẫn không có sheet, tức là đúng lỗi của ticket vẫn còn trên dữ liệu cũ | Yêu cầu Dev query toàn hệ thống số bot/form đang ở trạng thái này và quyết định có recover không (§6) |
| I10 | `[MAJOR]` | NEW-8 | Expected "⚠ CẦN HUMAN XÁC NHẬN… Không kết luận pass/fail" → không đo được | Chốt chính sách ở §6 rồi viết lại expected cụ thể |
| I11 | `[MAJOR]` | NEW-17 | Bước 2 "Đợi record… nhưng job chưa hoàn thành" không dựng lại được: job chạy **mỗi phút**, cửa sổ revoke rất ngắn | Tiền đề ghi rõ cách giữ record ở trạng thái chờ (vd liên kết + tạo nhiều form rồi revoke ngay, hoặc tạm dừng scheduler trên staging), và số form tối thiểu |
| I12 | `[MAJOR]` | NEW-19 | Expected "ghi vào Google Sheet đúng format" không đo được | Ghi cụ thể: dòng mới ở cuối sheet, đủ cột 回答ID / các câu hỏi, giá trị khớp câu trả lời (xem kho `TC-FORM-382`) |
| I13 | `[NIT]` | NEW-10 | Bot không còn token thì record treo `PROCESSING` vĩnh viễn — lỗi có sẵn, Dev đã ghi là ngoài phạm vi | Raise ticket riêng; đừng để TC này thành "pass" che mất lỗi |

---

## 5. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa011-taobieumau-フォーム作成.md` — nhóm "Liên kết Google Sheet" (TC-FORM-360…373) + "Sync Google Sheet & job" (TC-FORM-374…405) + MT-15, MT-22 |
| Vùng regression phát hiện từ kho | `TC-FORM-365` (hủy liên kết bị chặn khi tạo sheet lỗi — nay record ERROR + cờ 0 cùng lúc) · `TC-FORM-369` (ngắt quyền từ phía Google ⇒ modal cảnh báo) · `TC-FORM-370/371` (liên kết lại cùng / khác email) · `TC-FORM-399` (job sync gặp 429 ⇒ backoff, **không** đánh mất liên kết) |
| Conflict expected vs kho | Không có TC đề xuất nào mâu thuẫn kho. Có mâu thuẫn **chính sách** giữa 2 job: `TC-FORM-399` (job sync gặp 429 thì retry) vs code mới của job tạo sheet (gặp 429 thì đánh mất liên kết) → §6 mục 2 |
| GAP dùng lại TC kho (không viết mới) | G3/Q5 → chạy lại **`TC-FORM-369`** "Ngắt quyền truy cập Google từ phía Google → hệ thống hiển thị cảnh báo mất liên kết" ở production (MT-15 ghi "dự kiến FAIL → raise bug", chính là ticket này) · G7 (khác email) → **`TC-FORM-371`** chạy từ trạng thái mất liên kết do job · Q6 → **`TC-FORM-365`** bước 4: xác nhận hủy liên kết vẫn bị chặn khi record lỗi, nhưng nút 「再連携する」 vẫn dùng được |
| Xác nhận chống trùng | Đã đối chiếu 19 TC ở BƯỚC 0 + kho FA-011 — không TC đề xuất nào trùng |

**GAP / quan điểm không đề xuất TC mới:**
- **G2 / Q8 (lỗi tạm thời 429 / timeout)**: chưa viết TC vì expected phụ thuộc chính sách chưa chốt (§6 mục 2). Chốt xong cần bổ sung ≥ 1 TC cho lỗi tạm thời và 1 TC cho lỗi không xác định.
- **G4 (form A lỗi + form B thành công cùng lượt)**: chưa viết TC vì hành vi đúng chưa chốt (§6 mục 3). Mọi expected viết lúc này đều là tự chọn một bên.
- **G3 / Q1 / Q2**: đã có TC về nội dung → việc cần làm là **chạy** các TC đó và **gắn lại mã** (I1, I5), không cần đẻ TC mới. Riêng dữ liệu cũ đã hết lượt thử lại → §6 mục 5.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-JOB001-01 | UI | JOB-001 | Sync Google Sheet & job | Normal | auto | Tất cả | Job tạo sheet chạy thành công khi bot đang bị đánh dấu mất liên kết → cảnh báo mất liên kết tự biến mất | - Đăng nhập admin bot A<br>- Bot A đã liên kết Google bằng account G1, **quyền vẫn còn hiệu lực**<br>- Bot A đang ở trạng thái mất liên kết: mở màn /basic/form-answer thấy popup 「Googleスプレッドシートの連携が解除されました」 (dựng bằng cách chuyển trạng thái liên kết của bot về mất liên kết) | 1. Mở màn /basic/form-answer, xác nhận popup cảnh báo đang hiện<br>2. Tạo form mới F1 và bấm 保存<br>3. Chờ job tạo sheet chạy (≤ 2 phút)<br>4. Tải lại màn /basic/form-answer<br>5. Mở Google Drive của G1 | Form F1 basic, 1 câu hỏi text | - Bước 4: popup mất liên kết **không** hiện nữa; F1 có icon spread<br>- Bước 5: có file Google Spreadsheet mới của F1 | | Lấp G1 · Q1 · Đánh giá spec: Spec không ghi — hành vi theo commit `88307c747a` (Dev) · Evidence: screenshot trước/sau + file trên Drive · thay cho expected cũ của NEW-9 |
| TC-DATADB001-01 | UI | DATA-DB-001 | Sync Google Sheet & job | Abnormal | auto | Tất cả | Bật lại trạng thái liên kết chỉ áp cho bot có form tạo sheet thành công, bot khác đang mất liên kết giữ nguyên cảnh báo | - Bot A và bot B cùng liên kết Google (quyền còn hiệu lực), **cả 2** đang ở trạng thái mất liên kết (popup hiện ở cả 2 bot)<br>- Bot A **không** có form nào chờ tạo sheet | 1. Chọn bot B → tạo form F1 → 保存<br>2. Chờ job tạo sheet chạy (≤ 2 phút)<br>3. Ở bot B: tải lại màn /basic/form-answer<br>4. Chuyển sang bot A (phiên đăng nhập riêng): tải lại màn /basic/form-answer | Form F1 basic ở bot B | - Bot B: popup mất liên kết biến mất, F1 có icon spread<br>- Bot A: popup mất liên kết **vẫn hiện** | | Lấp G1 · Q7 · Đánh giá spec: Spec không ghi · Evidence: screenshot 2 bot · dùng 2 phiên đăng nhập riêng vì bot context tính theo session |
| TC-STATECLEAN001-01 | UI | STATE-CLEAN-001 | Liên kết Google Sheet | Normal | auto | Tất cả | Liên kết lại cùng email sau khi mất liên kết do job lỗi → form còn thiếu sheet được tạo file Google, form đã có sheet giữ file cũ | - Bot A liên kết Google account G1; form F1 đã có file Google<br>- Đã tạo form F2, F3 rồi **ngắt quyền LME** tại https://myaccount.google.com/connections trước khi job tạo sheet xong → F2, F3 không có icon spread, popup mất liên kết đang hiện | 1. Trên popup bấm 「再連携する」<br>2. Đăng nhập lại **G1**, cấp đủ quyền<br>3. Chờ job tạo sheet chạy (≤ 2 phút), tải lại /basic/form-answer<br>4. Mở Google Drive của G1<br>5. Cho LINE user trả lời F2 | F1 (đã có sheet), F2, F3 (chưa có sheet) | - Bước 3: popup biến mất; F1, F2, F3 đều có icon spread<br>- Bước 4: F1 vẫn là file cũ; có file mới cho F2 và F3<br>- Bước 5: câu trả lời xuất hiện ở file Google của F2 | | Lấp G7 · Q6 · regression — dẫn từ TC-FORM-370 · Đánh giá spec: Spec không ghi (BR-08 thiếu) · Evidence: screenshot màn form + Drive + sheet F2 |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Liên kết Google Sheet | Abnormal | auto | Tất cả | Màn biểu mẫu bản cũ hiển thị banner mời liên kết lại khi job tạo sheet đánh dấu mất liên kết | - Bot A đã liên kết Google<br>- Bot A bị job đánh dấu mất liên kết (như tiền đề của TC-STATECLEAN001-01)<br>- ⚠️ Hỏi Dev URL màn bản cũ (`FormAnswerController::index` / index_v2) còn truy cập được hay không | 1. Mở màn danh sách biểu mẫu **bản cũ**<br>2. Quan sát banner mời liên kết lại<br>3. Bấm link liên kết lại trên banner | — | - Banner mời liên kết lại hiển thị<br>- Link ở bước 3 mở màn OAuth Google (giống nút 「再連携する」 của popup màn mới) | | Lấp G5 · Q3 · RULE-09 · Đánh giá spec: Spec không ghi · Evidence: screenshot banner + URL đích |
| TC-COMPATLEGACY001-02 | UI | COMPAT-LEGACY-001 | Liên kết Google Sheet | Normal | auto | Tất cả | Màn biểu mẫu bản cũ KHÔNG hiện banner khi bot đang liên kết bình thường | - Bot A đã liên kết Google, không có lỗi tạo sheet (màn mới không hiện popup) | 1. Mở màn danh sách biểu mẫu **bản cũ**<br>2. Quan sát vùng banner | — | Không có banner mời liên kết lại; danh sách form hiển thị bình thường | | Lấp G5 · Q3 · RULE-09 · Đánh giá spec: Spec không ghi · Evidence: screenshot |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Sync Google Sheet & job | Abnormal | auto | Tất cả | Bot đang bị đánh dấu mất liên kết nhưng quyền Google vẫn còn → câu trả lời form cũ vẫn đồng bộ lên Google Sheet | - Bot A liên kết Google G1, quyền **còn hiệu lực**; form F1 đã có file Google<br>- Bot A đang ở trạng thái mất liên kết (popup hiện) — dựng như tiền đề TC-JOB001-01 | 1. LINE user U1 mở form F1 và gửi câu trả lời<br>2. Chờ job đồng bộ câu trả lời chạy<br>3. Mở file Google của F1<br>4. Tải lại /basic/form-answer | Câu trả lời U1: text "山田太郎" | - Bước 3: có dòng mới ở cuối sheet, chứa "山田太郎"<br>- Bước 4: popup mất liên kết **vẫn hiện** (job đồng bộ câu trả lời không bật lại trạng thái liên kết) | | Lấp G6 · regression · Đánh giá spec: Spec không ghi — theo Dev mục 4.3 T4 · Evidence: screenshot sheet + popup |
| TC-CONC001-01 | UI | CONC-001 | Liên kết Google Sheet | Abnormal | auto | Tất cả | Liên kết lại trong lúc job tạo sheet đang xử lý form lỗi bằng quyền cũ → trạng thái cuối là ĐANG liên kết, không bị job ghi đè về mất liên kết | - Bot A liên kết G1, đã tạo nhiều form (≥ 5) rồi ngắt quyền tại myaccount → job bắt đầu báo lỗi, popup mất liên kết hiện<br>- Vẫn còn form chờ thử lại (chưa lỗi đủ 3 lần) | 1. Ngay khi popup hiện, bấm 「再連携する」 và hoàn tất OAuth bằng G1<br>2. Chờ thêm 2 lượt job (≤ 3 phút)<br>3. Tải lại /basic/form-answer<br>4. Mở Google Drive G1 | ≥ 5 form chưa có sheet | - Bước 3: popup mất liên kết **không** hiện; mọi form có icon spread<br>- Bước 4: đủ file Google cho các form, không file trùng | | Lấp Q4 · race job ↔ user · Đánh giá spec: Spec không ghi · hỏi Dev job có khóa chạy chồng (withoutOverlapping) và có đọc lại token mới mỗi lượt không · Evidence: screenshot + Drive |

---

## 6. Spec update needed

| # | Nội dung | Ai chốt | Liên quan |
|---|---|---|---|
| 1 | `spec-features/admin/form-answer/feature-spec.md` **BR-08** không mô tả cờ `bots.google_sheet_status` và cảnh báo mất liên kết. Cần bổ sung: (a) job tạo sheet lỗi ⇒ đánh dấu mất liên kết; (b) tạo sheet thành công khi đang mất ⇒ bật lại; (c) popup màn mới + banner màn cũ; (d) nút 「再連携する」. Trùng đề xuất MT-15 của kho FA-011 | Leader | G1, G5, I7 |
| 2 | **Chính sách loại lỗi** (REQ-007 / NEW-8): job tạo sheet đánh dấu mất liên kết với **mọi** exception, gồm cả 429 / timeout / lỗi dữ liệu của 1 form. Trong khi đó job đồng bộ câu trả lời chỉ đánh dấu với 401 / UNAUTHENTICATED / 400, và gặp 429 thì backoff (kho `TC-FORM-399`). Chốt: 2 job có dùng chung 1 cách phân loại lỗi không? | Dev + Leader | G2, Q8, I10 |
| 3 | **Thứ tự trong cùng 1 lượt**: bot có form A lỗi và form B thành công ⇒ cảnh báo có còn hiện không? Code hiện tại: phụ thuộc thứ tự xử lý | Dev + Leader | G4 |
| 4 | NEW-9 / REQ-008 (Studio): cập nhật theo commit `88307c747a` — tạo sheet thành công thì bật lại liên kết. Dòng rủi ro thứ 2 trong phần tự review của Dev (journal #137196) đã lỗi thời, nên xóa để khỏi gây hiểu nhầm | Dev (journal) · QA (Studio) | G1, I2 |
| 5 | **Dữ liệu trước deploy** (RULE-04): bot có form đã lỗi đủ 3 lần trước khi deploy vẫn báo "đang liên kết" và không có sheet. Có recover không (reset `retry_error` hoặc đánh dấu mất liên kết hàng loạt)? | Dev + Leader | Q2, I9 |
| 6 | BR-08 và §9 ghi job `AddResultFormAnswerToGoogleSpreadSheet` "đang bị comment out", nhưng Dev (journal #137196) xác nhận job này đang chạy và ghi cờ ở dòng 437-471 → viết lại theo MT-22 của kho FA-011 | Leader | G6 |
