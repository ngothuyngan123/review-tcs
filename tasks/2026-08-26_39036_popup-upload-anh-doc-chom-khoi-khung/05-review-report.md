# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39036 — [Upload ảnh][Popup] Ảnh bị chờm ra khỏi khung sau khi upload ảnh dọc và đã được resize` |
| Reviewer (Leader) | `<điền tên>` (draft sinh bởi `/review-tc`) |
| Tester được review | `AI` (6/7 TC, job Studio #613) + `haodtb@mcp` (1/7 TC) — **không có TC nào do member người viết** |
| Ngày review | `2026-08-26` |
| Version TCs | Studio round `1`, TC version `v1`/`v2`, toàn bộ `status = draft` |
| Vòng review | `Round 1` (Studio `reviewState = leader`, `reviewed = false`, 0 comment vòng trước) |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | **(1) MCP LME TEST STUDIO — task #203** |
| Vì sao không dùng nguồn ưu tiên cao hơn | N.A. — đã dùng nguồn 1 (ưu tiên cao nhất) |
| Ticket · task_id · round · branch | `39036` · `#203` · round `1` · `ai_fixbug_39036` |
| Thời điểm fetch | `2026-08-26` (`task_list` + `testcase_list` + `task_get_context` + `task_get_report`) |
| Tổng số TC review | **7** |
| Snapshot đã ghi | `04-tc-list.md` — đã có sẵn header `<!-- source: MCP LME TEST STUDIO — task_id=203 ... -->` do `/new-task` sinh **cùng ngày, cùng nguồn**; nội dung 7 TC khớp bản fetch lại → **không ghi đè** (không có delta) |
| Đối chiếu chéo nguồn | **KHÔNG** — đã dừng ở nguồn 1 |

**Cảnh báo bắt buộc về chất lượng nguồn** — *Nguồn 1 (Studio)*:

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | Manual **7/7 pass (100%)** · Auto run `#485` 6 pass · Auto run `#508` **7 skip** (lỗi hạ tầng `SOURCE_CHECKOUT_ERROR`, **không** phải lỗi sản phẩm) · Auto run `#644` (staging) đang **`queued`, chưa chạy** | `OK` về tỉ lệ pass — nhưng xem mục 3 |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **0 fail · 0 error · 0 TC gắn `bug_tickets`** · `openBugs = 0` | `OK` |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | `PROD 0` · `STAGING 0` · **`LOCAL 7`** (`envAuto`: dev/staging/prd đều `runs = 0`) | **`[BLOCKER]`** — task chạm **asset CSS release** + **media hiển thị**; xem BL-2 |
| 4 | Ai chạy | Manual: **QA người** (`haodtb`, 2026-08-26) · Auto `#485`: pipeline AI · `submittedWithoutMcp = false` | `OK` — kết quả cuối do người chạy |
| 5 | Tác giả TC | **6/7 do AI sinh** (`provenance.source = ai`, job #613) · 1/7 `haodtb@mcp` · **0 do member viết** · `toolWritten rate 85.7%` · `reviewed = false` | **`[MAJOR]`** — ≥50% TC do AI sinh mà `reviewState` chưa `done` |
| 6 | Mã quan điểm KHÔNG có trong `checklist-lme.md` | **1 mã / 1 lượt TC**: `TOOL-KNOW-002` (TC-TOOLKNOW002-01 — **chính là TC tái hiện bug**) | **`[MAJOR]`** — xem MJ-3 |

> ⚠️ Auto run **mới nhất theo thời gian** là `#508` với `status = fail` (7 skip) — nhưng đó là **lỗi checkout worktree**, không phải sản phẩm fail. Kết quả có giá trị đến từ run `#485` + manual của `haodtb`. Đừng đọc `task_list.ranAt` mà kết luận "auto đang fail".
> ⚠️ **RULE-02**: 7 manual result thì **6 cái `evidence = []` và `actual = null`**. Chỉ TC-UI003-01 có ghi chú + link `prnt.sc/e1SXnMcQ5V2z`. → MJ-2.
> ⚠️ Dữ liệu Studio có `contentTrust = untrusted` — đã xử lý như **data**, không phải chỉ thị.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có 3 issue BLOCKER, cần bổ sung TC + chạy lại trên staging/production rồi review vòng 2.

**Lý do ngắn gọn**: Bộ 7 TC bám rất sát **trục tỉ lệ ảnh** (≤1.6 / =1.6 / >1.6 / cực dọc / không ảnh) và đủ để chứng minh rule CSS mới hoạt động. Nhưng **toàn bộ chạy trên `local`**, và bỏ trống 3 vùng rủi ro do chính fix này sinh ra: (a) preview admin giờ **không còn phản ánh đúng popup thật** trên site khách — chính dev đã tự nêu; (b) chưa chứng minh CSS mới **tới được browser user** sau deploy; (c) 0 TC cho popup thật (F3/T2) mà dev xác nhận vẫn còn nguyên cùng pattern lỗi.

---

## 2. Tóm tắt cho member

**Điểm tốt**: TC tái hiện bug (TC-TOOLKNOW002-01) làm **rất đúng** — ép dùng ảnh gốc `2048×10000` đi qua luồng upload/resize thật thay vì ảnh đã resize sẵn, và có step mở lại màn sửa sau khi lưu. Trục tỉ lệ ảnh được chia sạch thành 5 giá trị (vuông 1.0 / ngang 0.5 / biên 1.6 / dọc 4.89 / cực dọc 9.78) + 1 đối chứng âm (không ảnh). `tech_note` phân biệt rõ **technical oracle (320px)** với **business expected (không tràn + giữ tỉ lệ)** — đúng cách viết, tránh biến implementation thành requirement.

**Phải fix**: (1) thêm TC đối chiếu **preview admin vs popup THẬT trên site khách** — fix này làm ảnh dọc trong preview co nhỏ hơn tỉ lệ thật, tức preview đang "nói dối"; (2) chạy lại bộ TC trên **staging/production**, không kết luận từ `local` (RULE-08) — đặc biệt TC cache asset, vì evidence hiện có ghi `detail.css?v=202607111205` (mốc 2026-07-11) trong khi commit fix là 2026-08-21; (3) bổ sung **evidence** cho 6/7 TC đang trống (RULE-02); (4) thêm TC cho **1366×768** và **Safari/Mac** — đây là fix thuần CSS, 2 trục này là nơi CSS hay lệch nhất.

---

## 3. Coverage Matrix

| Impact | Loại | TCs cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — preview ảnh dọc tràn khung điện thoại mẫu | Fix | TC-TOOLKNOW002-01 | 1 | 1/1 pass (local, **không evidence**) | **RISK** |
| **F1** — rule CSS `.preview__body img` (`detail.css:322`) | Function **Direct** | Cả 7 TC | 7 | 7/7 pass (local) | **RISK** — thiếu Abnormal, thiếu trục môi trường/browser/độ phân giải |
| **F2** — luồng upload/validate/resize (dev **không sửa**) | Function không chạm code | TC-TOOLKNOW002-01 (đi qua luồng thật) | 1 | 1/1 pass | **OK** — không đòi thêm TC (layer không bị chạm, xem AP-5) |
| **F3** — popup thật site khách `embedded-popup/default_setting.js` (dev **không sửa**, xác nhận **cùng pattern lỗi**) | Function không sửa | — | **0** | — | **GAP** |
| **D** — không có (mục 4.2 = "Không có") | Data | — | — | — | **N/A** |
| **T1** — Popup FA-018, khối 「プレビュー」 (SCR-PU-02) | Feature **Medium** | Cả 7 TC | 7 | 7/7 pass (local) | **RISK** |
| **T2** — popup thật hiển thị trên site khách | Feature **Low** | — | **0** | — | **GAP** |

### ORPHAN TCs

**Không có.** Cả 7 TC đều nằm trong scope `BUG / F1 / T1`, `screen` đồng nhất `SCR-PU-02`. Không TC nào test tầng server/DB không bị chạm → **AP-5 không dính**.

> ⚠️ Studio tự tính "coverage spec: 0/37 covered, 30 none" — 30 mục `EP-*` / `BR-*` chưa phủ là của **toàn bộ feature popup** (plan free, xóa folder, copy popup, tracking…), **không** thuộc phạm vi ticket này. **Không** tính là GAP của review này.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** | **`JS / CSS / font / icon / asset / build`** — mục 2: *"Sửa rule `.preview__body img` trong `public/css/popup/detail.css`… giới hạn CHIỀU CAO tối đa 320px kèm max-width 100%"*. Shape phụ: **media / ảnh** (hiển thị, **không** chạm upload). **Không phải** generic catch-all / validation / race / migration / soft-delete. |
| **Trigger space cần cover** | Trục chính = **tỉ lệ h/w của ảnh**: `≤1.6 không kích hoạt` (vuông 1.0, ngang 0.5) · `=1.6 đúng biên` · `>1.6 kích hoạt` (4.89) · `cực lớn` (9.78) · `không có ảnh`. Trục phụ (do fix shape asset + media sinh ra): **môi trường** (local/staging/production) · **trình duyệt** (Chrome-Win / Safari-Mac) · **độ phân giải** (1366×768 / 1920) · **nguồn ảnh** (mới upload / popup cũ đã lưu / ảnh 404) · **surface** (preview admin / popup thật site khách). |
| **Số trigger TCs hiện cover** | Trục chính **5/5 ✅** · Trục phụ **0/5 ❌** (môi trường 1/3 = chỉ local; browser 0/2; độ phân giải 0/2; nguồn ảnh 1/3; surface **1/2 — thiếu popup thật**) |
| **KH report dạng** | **Có root cause cụ thể** — tester đưa kích thước chính xác `2048×10000`, evidence DevTools `naturalWidth=419 / naturalHeight=2048`, dev đo được `.popup__preview` cao 500px. |
| **Alternative root causes cần verify** | **N/A** — không phải symptom-only. Root cause đã được chứng minh bằng số đo DOM, không phải suy đoán. |
| **Anti-patterns dính** | **AP-3** (happy-path-only regression) — T2 có 0 TC, và **mọi** TC hiện có đều dùng precondition "ảnh vừa upload, data sạch"; không có edge state (ảnh cũ đã lưu từ trước fix, ảnh 404). · **AP-4 gần dính** → chỉ mức `[NIT]`: không có link PR/diff, chỉ có commit hash `73014385e8` — nhưng fix shape **đã được verify gián tiếp** bằng computed style trong auto run #485 (`max-height=320px, max-width=100%`). · **AP-1 / AP-2 / AP-5 / AP-6 KHÔNG dính** (không phải generic-fix; KH có root cause; không over-test layer dưới; mục 3 có 7 dòng caller). |

### Câu hỏi adversarial bắt buộc cho fix shape `asset` — và câu trả lời

| Câu hỏi (BƯỚC 3c) | Trạng thái |
|---|---|
| Test **F5 thường** (không Ctrl+F5) trên browser còn cache bản cũ? | TC-DEPLOYASSET001-01 **có steps đúng** ("không dùng Ctrl+Shift+R, không xóa cache thủ công") → nhưng chạy trên `local` nơi không có CDN/cache thật → **chưa trả lời được**. |
| Network tab có asset 404 / query version mới? | Evidence auto run #485: `http://127.0.0.1:18403/css/popup/detail.css?v=202607111205`. **Version stamp `2026-07-11 12:05` CŨ HƠN commit fix `2026-08-21`** → nếu chuỗi version này không đổi khi deploy, browser giữ cache sẽ tiếp tục dùng CSS cũ và **fix không tới user**. → BL-2. |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER] BL-1 — GAP-1 / OUT-PREVIEW-001 (Cao): fix làm preview admin KHÔNG còn phản ánh đúng popup thật, 0 TC nào bắt được điều đó.`**
`OUT-PREVIEW-001` là **BẮT BUỘC** với mọi chức năng có chế độ preview, và yêu cầu rõ: *"preview/test-send pass **chưa đủ** → bắt buộc chạy thêm 1 lần **luồng thật**… So từng điểm"*. Đây là ticket **về chính khối preview** mà 7/7 TC dừng lại ở màn admin.
Rủi ro cụ thể, do **chính dev tự nêu** ở mục TỰ REVIEW: *"Ảnh có tỉ lệ cao/rộng > 1.6 giờ hiển thị hẹp hơn 200px trong khung xem trước (vd 1000x2000 → 160x320) — đúng ý đồ để vừa khung, **nhưng preview sẽ nhỏ hơn tỉ lệ thật của popup trên site khách**"*. Cộng với F3 (popup thật vẫn `width:100%` không giới hạn chiều cao) → **admin nhìn preview thấy gọn gàng, khách vào site lại thấy ảnh dài phủ kín trang**. Trước fix, preview sai theo hướng "cảnh báo thừa"; sau fix, preview sai theo hướng **"trấn an giả"** — nguy hiểm hơn.
→ **Fix**: thêm `TC-OUTPREVIEW001-01/02/03` (§5). Đồng thời đưa câu hỏi *"preview có bắt buộc phản ánh đúng tỉ lệ popup thật không"* lên Leader/PM (§6-2).

**`[BLOCKER] BL-2 — GAP-2 / ENV-003 (Cao) + DEPLOY-ASSET-001 (Cao): 7/7 TC chạy trên "local"; chưa chứng minh CSS mới tới được browser user sau deploy.`**
`ENV-003` **BẮT BUỘC** khi tính năng chạm **media/file** hoặc **asset release**, và ghi thẳng: *"**Không được đánh × với lý do 'staging đã pass'"* (RULE-08). Ở đây còn nhẹ hơn staging — **`local`**. `envAuto` xác nhận `dev / staging / prd` đều `runs = 0`; run staging `#644` mới ở trạng thái `queued`.
Bằng chứng cụ thể làm việc này thành BLOCKER chứ không phải MAJOR: evidence của TC-DEPLOYASSET001-01 ghi `detail.css?v=202607111205` — **mốc version cũ hơn commit fix (2026-08-21) đúng 6 tuần**. Trên `local`, runner mở browser context mới nên không có cache → TC pass **một cách vô nghĩa**. Trên production, nếu chuỗi `?v=` không đổi theo release, URL byte-identical → browser trả bản cache cũ → **user không nhận fix mà không ai biết**. Thêm nữa `ENV-003` ghi rõ production phục vụ media qua **`p.lmes.jp` → B2**, khác hẳn đường dẫn local.
→ **Fix**: chạy lại toàn bộ 7 TC trên **STAGING**, và tối thiểu TC-TOOLKNOW002-01 + TC-DEPLOYASSET001-01/-02 + TC-ENV003-01 trên **PRODUCTION**; đính kèm screenshot DevTools > Network (query version + status 200).

**`[BLOCKER] BL-3 — GAP-3 / REG-SHARED-001 (Cao): dev tự khai bug cùng pattern còn ở popup thật (F3) nhưng không có danh sách nơi ảnh hưởng đầy đủ và 0 TC.`**
`REG-SHARED-001` trigger: *"BẮT BUỘC với mọi release sửa code dùng chung **hoặc fix bug có thể tồn tại ở chức năng tương tự**"*, và yêu cầu *"**dev cung cấp danh sách nơi ảnh hưởng** → test lại **từng mục**"*. Dev đã tự tìm ra **1** nơi (`embedded-popup/default_setting.js` — *"cũng chỉ set width 100% không giới hạn chiều cao — cùng pattern nhưng khác phạm vi ticket nên chỉ ghi nhận, không sửa"*) nhưng **dừng ở đó**: không rà hết các khối preview khác, không có TC nào chạm F3/T2.
⚠️ **Phạm vi yêu cầu có giới hạn** — không đòi test lại tầng upload/resize server (F2 không bị chạm code). Chỉ đòi: (a) dev liệt kê **đủ** các khối hiển thị ảnh dùng pattern `img` **không** giới hạn chiều cao (dev đã tự dẫn 2 nơi **đúng chuẩn** để đối chiếu: `.c_h_file-preview img`, `scenario/list-message.css`); (b) 1 TC regression cho popup thật; (c) quyết định tách ticket cho F3.
→ **Fix**: `TC-OUTPREVIEW001-01` (§5) + yêu cầu danh sách từ dev + §6-3.

### 4.2 Major (nên fix)

**`[MAJOR] MJ-1 — 01-bug-task.md + 03-dev-impact.md: checkbox "Tester verify auto-fill chính xác" CHƯA tick.`**
Cả 2 file đều có `Auto-filled: 2026-08-26 by /new-task` mà chưa ai xác nhận. Toàn bộ F1/F2/F3/T1/T2 trong review này suy ra từ bản auto-fill đó — nếu map sai thì coverage matrix ở §3 sai theo. → Tester đọc lại Redmine #39036 (description + journal #131913) rồi tick 2 checkbox trước khi report này có giá trị nghiệm thu.

**`[MAJOR] MJ-2 — RULE-02: 6/7 TC pass nhưng evidence trống.`**
Manual result: 6 TC có `evidence = []` **và** `actual = null`; chỉ TC-UI003-01 ghi *"vẫn hiển thị đúng logic trước kia"* + link `prnt.sc/e1SXnMcQ5V2z`. RULE-02: *"Chỉ tick Đạt khi đã đính kèm **đúng loại** bằng chứng… Không chấp nhận 'đã xem, OK'"*. Với TC đo kích thước hiển thị thì evidence bắt buộc là **screenshot khung preview + số đo px** (MEDIA-IMG-001 ghi rõ: *"ảnh gốc + ảnh sau upload **kèm số đo px**"*). → Chạy lại và đính evidence cho cả 7 TC; link `prnt.sc` dễ hết hạn, nên tải về lưu kèm folder.

**`[MAJOR] MJ-3 — TC-TOOLKNOW002-01 gắn mã quan điểm "TOOL-KNOW-002" không tồn tại trong framework/checklist-lme.md.`**
Đây là **TC quan trọng nhất** của bộ (tái hiện bug gốc) nhưng mã quan điểm của nó là mã nội bộ Studio → `/review-tc` **không map được coverage**, và theo BƯỚC 0.6 #6 thì quan điểm chỉ được cover bởi mã lạ **không được tính là cover**. Nội dung TC thì đúng và có giá trị — vấn đề chỉ ở nhãn. → Gắn lại `Mã quan điểm liên kết = MEDIA-IMG-001` (hoặc `OUT-PREVIEW-001` sau khi bổ sung TC ở §5), giữ `TOOL-KNOW-002` ở `Ghi chú` để trace ngược Studio. Sửa bằng `testcase_update` trên Studio rồi fetch lại — **không sửa tay** file 04.

**`[MAJOR] MJ-4 — TC-FUNC004-01 gắn sai mã quan điểm: FUNC-004 là "Giới hạn trên/dưới về số ký tự, số lượng", TC lại test biên tỉ lệ hiển thị ảnh.`**
`FUNC-004` (Cao) yêu cầu **5 pattern** (đúng biên / biên+1 / biên−1 / 0 / chuỗi rỗng) và *"ghi rõ **nguồn của giới hạn**"* — không áp được cho tỉ lệ 1.6 vốn là **hệ quả hình học của `max-height:320px` ÷ `width 200px`**, không phải giới hạn nghiệp vụ. Hệ quả kép: (a) `FUNC-004` trông như đã cover trong khi task này **không hề chạm** giới hạn ký tự/số lượng nào; (b) `FUNC-004` là quan điểm **Cao** → kích hoạt RULE-01 đòi đủ 3 loại case một cách vô nghĩa (TC hiện chỉ có Boundary). → Gắn lại thành `MEDIA-IMG-001`, giữ `Boundary`.

**`[MAJOR] MJ-5 — RULE-01: DEPLOY-ASSET-001 là quan điểm ưu tiên CAO nhưng chỉ có 1 TC Normal, không ghi lý do thiếu Abnormal/Boundary.`**
→ Bổ sung `TC-DEPLOYASSET001-02` (Abnormal — cache CSS cũ + F5 thường, §5). Loại `Boundary`: **ghi lý do** *"version asset không có khái niệm biên"* vào `Ghi chú` (RULE-01 cho phép, nhưng bắt buộc ghi).

**`[MAJOR] MJ-6 — GAP-4 / UI-001 (Trung bình): 0 TC ghi độ phân giải, trong khi fix chốt cứng 320px vào khung 500px.`**
`UI-001` + `UIC-13`: *"**Bắt buộc kiểm ở 1366×768** (độ phân giải thấp nhất được hỗ trợ)"*. Dev tự nêu Rủi ro 2: *"320px là con số **cố định** hợp với khung 500px hiện tại"* — nếu ở 1366×768 khối `.popup__preview` co lại dưới 500px thì 320px + ~70px nội dung có thể vượt khung trở lại. Kho TCs có tiền lệ đúng dạng này: **TC-RM-288** (FA-004) *"màn edit hiển thị đúng ở 14 inch và 17 inch… **Kiểm tra preview ảnh ở mỗi độ rộng**"*. → `TC-UI001-01` (§5).

**`[MAJOR] MJ-7 — GAP-5 / UI-002 (Trung bình): fix thuần CSS nhưng 0 TC chạy Safari/Mac.`**
`UI-002`: *"danh sách tối thiểu — **Mac Safari + Chrome** (user chính là chủ salon/cửa hàng nhỏ, dùng Safari nhiều)"*. `max-height` áp lên `<img>` bên trong container flex là điểm Safari và Chromium hay tính khác nhau. Auto run #485 chạy bằng runner headless (Chromium), manual cũng không ghi browser. Tiền lệ trong kho rất sát: **TC-RM-111** (FA-004, Support #32989) — *"ảnh preview để chiều cao TỰ ĐỘNG theo chiều rộng: ảnh half size không bị co, **đúng trên Chrome/Win và Safari/Mac**"*, tức team đã từng **nhận ticket khách** về đúng loại lỗi "preview co ảnh sai" và chốt chuẩn phải verify 2 browser. → `TC-UI002-01` (§5).

**`[MAJOR] MJ-8 — GAP-6 / UI-003 (Trung bình): chỉ cover trạng thái RỖNG, thiếu trạng thái LỖI.`**
`UI-003` đòi **cả 3** trạng thái loading / rỗng / lỗi. TC-UI003-01 chỉ cover "chưa upload ảnh" (rỗng). Trạng thái lỗi rất thực tế ở đây: trên production ảnh phục vụ qua `p.lmes.jp`/B2 (ENV-003) — nếu URL 404, thẻ `<img>` gãy vẫn bị áp `max-height:320px`, cần xác nhận không vỡ layout khung điện thoại mẫu. → `TC-UI003-02` (§5).

**`[MAJOR] MJ-9 — AP-3: toàn bộ 7 TC dùng precondition "ảnh vừa upload trong phiên hiện tại"; không có TC nào mở popup ĐÃ TẠO TRƯỚC bản fix.`**
Người dùng thật gặp bug này trên các popup **đã tồn tại**, không phải popup vừa tạo. TC-TOOLKNOW002-01 step 5 có "lưu rồi mở lại màn sửa" nhưng vẫn trong cùng phiên, cùng ảnh vừa upload. → `TC-MEDIAIMG001-04` (§5, `regression`).

**`[MAJOR] MJ-10 — Cả bộ 7 TC có 0 case Abnormal (Normal 5 / Boundary 2 / Abnormal 0).`**
Checklist §C.1: tỷ lệ Normal : Abnormal : Boundary phải hợp lý. Đây là hệ quả gộp của MJ-5 + MJ-8 — hai TC Abnormal đề xuất ở §5 (`TC-DEPLOYASSET001-02`, `TC-UI003-02`, `TC-OUTPREVIEW001-02`) đưa tỉ lệ về `6 : 3 : 3`.

### 4.3 Minor (có thể fix sau)

**`[MINOR] MN-1 — TC-MEDIAIMG001-01 (Studio #12828): steps chỉ ghi ảnh vuông 1000×1000 nhưng auto run #485 thực tế chạy CẢ ảnh ngang 2048×1024 bên trong TC này.`**
Evidence run #485 của #12828: *"Vuông 1000×1000 → 200×200px; **Ngang 2048×1024 → 200×100px**"* — trùng đúng nội dung của TC-MEDIAIMG001-02 (#12925, tạo sau). TC đang test rộng hơn steps của chính nó → khó truy vết khi 1 trong 2 shape fail. → Đồng bộ lại: `#12828` chỉ giữ ảnh vuông, ảnh ngang để nguyên ở `#12925`.

**`[MINOR] MN-2 — TC-MEDIAIMG001-02 (Studio #12925) có requirement_keys RỖNG.`**
6 TC còn lại đều gắn `REQ-001`…`REQ-004`. TC này tách tay từ #12828 nên mất liên kết → coverage theo requirement bị hụt 1 dòng. → Gắn `REQ-003` (cùng requirement với #12828).

**`[MINOR] MN-3 — TC-UI003-01 (Studio #12829) không có priority (field Studio = null).`** 6 TC khác đều có `High`/`Medium`. → Điền `Medium`.

**`[MINOR] MN-4 — Cả 7 TC có spec_status = null.`**
Cột `Trạng thái đánh giá spec` trống toàn bộ. Với task này câu trả lời đúng phải là **`Spec không ghi`** (xem §6-1: `spec-features/` chưa có FA-018, `lme.jp/manual` không mô tả preview) — và khi chọn `Spec không ghi` thì **bắt buộc ghi đã hỏi ai**. → Điền `Spec không ghi` + tên người đã hỏi cho cả 7 TC.

### 4.4 Nit (gợi ý)

**`[NIT] NT-1 — AP-4: không có link PR/diff, chỉ có commit hash 73014385e8 + branch.`** Không nâng lên MAJOR vì fix shape đã được verify gián tiếp bằng computed style trong auto run #485 (`max-height=320px, max-width=100%`) và diff được mô tả là đúng 1 rule CSS. Vẫn nên đính link diff để reviewer tự đọc.

**`[NIT] NT-2 — Ảnh tái hiện bug là 2048×10000, đúng ngay ngưỡng chặn upload của hệ thống.`** Catalog E `MED-L10`: *"Cạnh **> 10.000px: chặn upload**"* — ảnh của tester nằm đúng tại biên (10.000px, chưa vượt). Luồng validate **không bị chạm code** nên **không** đề xuất TC (tránh AP-5 over-coverage), chỉ ghi nhận: nếu sau này ngưỡng chặn đổi thành `>= 10.000` thì TC tái hiện bug sẽ không dựng được data nữa.

**`[NIT] NT-3 — Drift tài liệu nội bộ`**: `.claude/commands/review-tc.md` BƯỚC 5c ghi §5 report dùng **16 cột canonical**, trong khi `CLAUDE.md` §"Ràng buộc khi sinh report" và `templates/05-review-report.template.md` (dòng 161) đều dùng **12 cột kho**. Report này theo `CLAUDE.md` + template (12 cột). → Leader sửa 1 trong 2 file cho khớp.

**`[NIT] NT-4 — RULE-11`**: đã rà §4 "Quan điểm chưa đủ bằng chứng" của `checklist-lme.md` (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) — **không mục nào liên quan** task này. Không dùng để flag.

---

## 4.5 TC trùng lặp nội dung

**Đã rà toàn bộ 7 TC theo 4 yếu tố** (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `điều kiện tiền đề tương đương` → `kết quả mong đợi`).

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Ảnh tỉ lệ ≤ 1.6 không kích hoạt `max-height` | TC-MEDIAIMG001-01 (vuông) | TC-MEDIAIMG001-02 (ngang) — **KHÔNG đề nghị xóa/gộp** | *(đã xem xét, kết luận **không trùng**)* | Trùng 3/4: cùng `MEDIA-IMG-001` · cùng `Normal` · cùng thao tác "upload → quan sát preview" · tiền đề tương đương. **Khác** ở giá trị trên trục shape mà `MEDIA-IMG-001` mục (3) yêu cầu test riêng: *"ảnh vuông/dọc/ngang → rule fix chiều rộng, giãn chiều cao"* | — |

**Kết luận: đã rà 7 TC, KHÔNG phát hiện TC trùng lặp cần xóa hoặc gộp.**

Diễn giải cặp trên: `1000×1000` (h/w = 1.0) và `2048×1024` (h/w = 0.5) là **2 giá trị khác nhau trên trục shape** mà framework gọi tên riêng, nên giữ 2 TC là đúng — dù chúng đi qua **cùng một code path** (`max-height` không kích hoạt). Chạy **gate bắt buộc**: giả định xóa `TC-MEDIAIMG001-02` → `MEDIA-IMG-001` vẫn còn `-01` + `-03`, `F1`/`T1` vẫn còn 6 TC → **không mất cover**; nhưng vì framework yêu cầu tách shape nên **vẫn giữ**. Vấn đề thực sự của cặp này là steps của `#12828` chưa khớp phạm vi nó thực chạy → đã ghi ở **MN-1**, không phải vấn đề trùng lặp.

Không có `DUP-EXACT` / `DUP-SUBSET` / `DUP-INFLATE` / `DUP-CONFLICT` nào khác. Riêng `TC-FUNC004-01` (h/w = 1.6) vs `TC-MEDIAIMG001-03` (h/w = 9.78): cùng `Boundary` nhưng là **đúng biên** vs **vượt xa biên** — không trùng.

> Nhắc lại: TC ở nguồn Studio là **read-only**. Report này **không sửa, không xóa** TC nào. Mọi thay đổi (MJ-3, MJ-4, MN-1…MN-4) thực hiện trên Studio bằng `testcase_update`, rồi fetch lại.

---

## 5. TCs đề xuất bổ sung

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | **`kho-tcs` CHƯA có FA-018 Popup** — không đối chiếu trực tiếp được. Đã đọc bù các file kho có khối **preview ảnh** cùng bản chất: `kho-tcs/fa004-richmenu-リッチメニュー.md` (TC-RM-111, TC-RM-288, TC-RM-96…99), `kho-tcs/fa001-chat11-11チャット.md` (TC-CHT-215, TC-CHT-01, TC-CHT-195) |
| Vùng regression phát hiện từ kho | **TC-RM-111** (FA-004, Support #32989) — preview ảnh richmenu phải giữ chiều cao tự động theo chiều rộng, verify **Chrome/Win + Safari/Mac** → dẫn cho `TC-UI002-01`. **TC-RM-288** (FA-004) — kiểm preview ảnh ở nhiều độ rộng màn hình → dẫn cho `TC-UI001-01`. **TC-CHT-215** (FA-001, `OUT-PREVIEW-001`) — preview template phải hiện đúng ảnh theo tỉ lệ với **cả 3 shape dọc/vuông/ngang** → xác nhận cách chia trục shape của bộ TC hiện tại là đúng chuẩn team |
| Conflict expected vs kho | **Không có mâu thuẫn cứng.** Nhưng có **căng thẳng về chuẩn** cần Leader chốt: TC-RM-111 coi việc "ảnh preview bị co" là **lỗi khách báo** (Support #32989), trong khi fix #39036 **cố ý** co ảnh dọc h/w > 1.6 xuống hẹp hơn 200px. Hai bên khác feature (richmenu vs popup) và khác trục (co méo tỉ lệ vs thu nhỏ giữ tỉ lệ) → **không tự chọn bên**, đã đưa vào **§6-2** |
| GAP dùng lại TC kho (không viết mới) | **Không** — kho chưa có FA-018, các TC kho dẫn chiếu ở trên thuộc feature khác nên chỉ dùng làm **chuẩn tham chiếu**, không dùng lại nguyên TC |
| Xác nhận chống trùng | **Đã đối chiếu 9 TC đề xuất với 7 TC ở BƯỚC 0 + các TC kho dẫn chiếu — không TC đề xuất nào trùng.** Không TC đề xuất nào lặp lại trục tỉ lệ ảnh (đã cover 5/5); toàn bộ nằm trên các trục **surface / môi trường / browser / độ phân giải / nguồn ảnh** hiện đang trống |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-OUTPREVIEW001-01 | UI | OUT-PREVIEW-001 | Popup — Preview vs popup thật | Normal | Đối chiếu preview admin với popup THẬT trên site khách, cùng 1 ảnh dọc | - Đăng nhập admin, chọn bot A, môi trường **PRODUCTION** (hoặc staging có site test nhúng được)<br>- Có 1 trang web test đã nhúng đoạn JS popup của bot A (lấy ở màn quản lý popup)<br>- Chuẩn bị ảnh dọc gốc 2048×10000 px | 1. Vào 「ポップアップ（作成）」, tab 「表示設定」, upload ảnh dọc 2048×10000<br>2. Chụp màn khối 「プレビュー」, đo chiều rộng × chiều cao ảnh hiển thị<br>3. Lưu popup và bật hiển thị<br>4. Mở trang web test đã nhúng popup bằng browser khác (chưa có cache)<br>5. Chờ popup hiện, chụp màn, đo chiều rộng × chiều cao ảnh trong popup thật<br>6. So 2 số đo và so tỉ lệ hiển thị của 2 nơi | Ảnh dọc 2048×10000 (sau resize ≈ 419×2048, h/w ≈ 4.89) | - Ghi nhận được **cặp số đo** preview vs popup thật<br>- Popup thật hiển thị **y như trước bản fix** (fix chỉ chạm CSS màn admin, không chạm `embedded-popup/default_setting.js`) → không có regression trên site khách<br>- **Nếu tỉ lệ hiển thị ở 2 nơi lệch nhau** → ghi nhận là phát hiện, đính cặp ảnh và báo Leader (§6-2), **không tự kết luận Đạt** |  | Lấp `GAP-1` + `GAP-3` · cover `F3`, `T2` · **regression** · Môi trường: **PRODUCTION** (RULE-08) · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: **cặp screenshot preview vs popup thật, mỗi ảnh kèm số đo px** · dẫn chuẩn từ `TC-CHT-215` (kho FA-001) |
| TC-OUTPREVIEW001-02 | UI | OUT-PREVIEW-001 | Popup — Preview vs popup thật | Abnormal | Ảnh cực dọc: preview gọn trong khung nhưng popup thật phủ kín trang khách | - Như TC-OUTPREVIEW001-01<br>- Chuẩn bị ảnh cực dọc 419×4096 px | 1. Upload ảnh cực dọc 419×4096 vào popup, quan sát khối 「プレビュー」<br>2. Lưu và bật hiển thị popup<br>3. Mở trang web test trên browser sạch, chờ popup hiện<br>4. Quan sát popup thật có che hết nội dung trang / có nút đóng bấm được không<br>5. Lặp lại bước 3-4 trên màn hình 1366×768 | Ảnh cực dọc 419×4096 (h/w ≈ 9.78) | - Preview admin: ảnh nằm gọn trong khung điện thoại mẫu (đã được TC-MEDIAIMG001-03 xác nhận)<br>- Popup thật: ghi nhận rõ ảnh có tràn/che kín trang khách không, **nút đóng popup có bấm được không**<br>- Nếu popup thật tràn → **raise ticket riêng** cho `embedded-popup/default_setting.js`, không gộp vào #39036 |  | Lấp `GAP-1` · cover `F3`, `T2` · Môi trường: **PRODUCTION** · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: **screenshot popup thật ở 1920 và 1366, thấy rõ mép trên/dưới ảnh và nút đóng** · 🔴 dự kiến phát hiện lỗi → chuẩn bị raise ticket (yokoten dev đã ghi nhận) |
| TC-OUTPREVIEW001-03 | UI | OUT-PREVIEW-001 | Popup — Preview vs popup thật | Boundary | Ảnh tỉ lệ đúng 1.6 — preview và popup thật phải khớp nhau | - Như TC-OUTPREVIEW001-01<br>- Chuẩn bị ảnh 500×800 px (h/w = 1.6) | 1. Upload ảnh 500×800, chụp và đo ảnh trong khối 「プレビュー」<br>2. Lưu, bật hiển thị popup<br>3. Mở trang web test trên browser sạch, chụp và đo ảnh trong popup thật<br>4. So tỉ lệ hiển thị 2 nơi | Ảnh 500×800 (h/w = 1.6 — đúng biên `max-height` kích hoạt) | - Tại đúng biên 1.6, `max-height` chưa co ảnh nhỏ hơn chiều rộng khung → **preview và popup thật hiển thị cùng tỉ lệ**<br>- Đây là mốc phân định: từ 1.6 trở xuống preview phản ánh đúng popup thật; trên 1.6 thì bắt đầu lệch (xem TC-OUTPREVIEW001-01/-02) |  | Lấp `GAP-1` · cover `F1`, `F3` · Môi trường: **PRODUCTION** · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: cặp screenshot kèm số đo px · Bộ 3 TC OUT-PREVIEW-001 thỏa **RULE-01** (quan điểm Cao đủ Normal + Abnormal + Boundary) |
| TC-ENV003-01 | API | ENV-003 | Popup — Preview trên môi trường thật | Normal | Ảnh dọc trong preview không tràn khung trên STAGING và PRODUCTION (ảnh phục vụ qua `p.lmes.jp`) | - Bản fix đã deploy lên STAGING và PRODUCTION<br>- Đăng nhập admin trên từng môi trường, chọn bot A<br>- Chuẩn bị ảnh dọc gốc 2048×10000 px | 1. Trên **STAGING**: upload ảnh dọc 2048×10000, quan sát khối 「プレビュー」, chụp màn<br>2. Lưu popup, reload màn sửa, quan sát lại preview của ảnh đã lưu<br>3. Mở DevTools > Network, ghi lại **URL thật của ảnh** đang được preview nạp<br>4. Lặp lại bước 1-3 trên **PRODUCTION**<br>5. Đối chiếu: URL ảnh trên production có trỏ về `p.lmes.jp` không, và ảnh có hiển thị đúng như trên local không | Ảnh dọc 2048×10000 · 2 môi trường: STAGING + PRODUCTION | - Cả 2 môi trường: ảnh nằm trọn trong khung 「プレビュー」, giữ đúng tỉ lệ, không chờm trên/dưới<br>- Ảnh sau khi lưu và reload vẫn hiển thị đúng (không phụ thuộc ảnh còn trong bộ nhớ phiên upload)<br>- Trên production, ảnh nạp từ đường dẫn media của production (`p.lmes.jp`) vẫn bị áp đúng giới hạn chiều cao |  | Lấp `GAP-2` · cover `BUG`, `F1`, `T1` · Môi trường: **PRODUCTION** (RULE-08 — `ENV-003` cấm kết luận từ staging/local) · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: **screenshot preview trên từng môi trường + URL ảnh trong tab Network** · Thay thế việc chỉ chạy `local` của cả 7 TC hiện có |
| TC-DEPLOYASSET001-02 | API | DEPLOY-ASSET-001 | Popup — Asset CSS sau release | Abnormal | Browser còn cache CSS bản cũ + chỉ F5 thường → phải nhận rule mới, chuỗi version của `detail.css` phải đổi | - Trước khi deploy bản fix: mở màn 「ポップアップ（作成）」 trên browser thật (Chrome), để browser cache `detail.css` bản cũ; **không** đóng browser, **không** xóa cache<br>- Ghi lại chuỗi `?v=...` của `detail.css` **trước** deploy<br>- Sau đó deploy bản fix lên môi trường đó | 1. Sau khi deploy xong, quay lại tab cũ, **chỉ bấm F5** (KHÔNG Ctrl+Shift+R, KHÔNG xóa cache)<br>2. Mở DevTools > Network, lọc `detail.css`, đọc **chuỗi `?v=...` sau deploy** và status code<br>3. So chuỗi version trước/sau deploy<br>4. Chọn thẻ ảnh trong khối 「プレビュー」, đọc computed style `max-height`<br>5. Upload ảnh dọc 2048×10000, quan sát ảnh có tràn khung không | Ảnh dọc 2048×10000 · 1 browser giữ nguyên cache từ trước deploy | - **Chuỗi `?v=...` của `detail.css` SAU deploy phải KHÁC trước deploy** — nếu giống hệt thì browser dùng lại bản cache cũ và fix không tới user → **Không đạt, raise ticket cache-busting**<br>- `detail.css` trả **200** (không 404, không `304` phục vụ nội dung cũ)<br>- Computed style của ảnh preview có `max-height` của bản fix<br>- Ảnh dọc không tràn khung mà **không cần** hard-reload |  | Lấp `GAP-2` + `GAP-7` · cover `F1` · **Abnormal còn thiếu của `DEPLOY-ASSET-001` (RULE-01)** · Môi trường: **PRODUCTION** · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: **2 screenshot DevTools Network (trước/sau deploy) thấy rõ chuỗi `?v=` và status code** · ⚠️ Bằng chứng khả nghi từ auto run #485: `detail.css?v=202607111205` — mốc cũ hơn commit fix 2026-08-21 · `Boundary` cho quan điểm này **không áp dụng** — version asset không có khái niệm biên (lý do theo RULE-01) |
| TC-UI001-01 | UI | UI-001 | Popup — Preview theo độ phân giải | Normal | Preview ảnh dọc không tràn khung ở 1366×768 (độ phân giải thấp nhất được hỗ trợ) | - Đăng nhập admin, chọn bot A, màn 「ポップアップ（作成）」<br>- Có màn hình / cửa sổ browser đặt được ở 1366×768 và 1920×1080<br>- Chuẩn bị ảnh dọc 419×2048 và ảnh cực dọc 419×4096 | 1. Đặt cửa sổ browser ở **1366×768**, mở màn tạo popup<br>2. Upload ảnh dọc 419×2048, quan sát khung 「プレビュー」: đo chiều cao khung điện thoại mẫu và chiều cao ảnh<br>3. Lặp lại với ảnh cực dọc 419×4096<br>4. Đổi cửa sổ sang **1920×1080**, lặp lại bước 2-3<br>5. So kết quả 2 độ phân giải | 2 ảnh × 2 độ phân giải | - Ở **cả 1366×768 và 1920×1080**: ảnh nằm trọn trong khung điện thoại mẫu, không chờm lên trên/xuống dưới, không đè lên phần text/nút của khung<br>- Khung 「プレビュー」 không vỡ layout, không tràn ngang ở 1366<br>- Nếu ở 1366 khung preview co nhỏ lại làm ảnh tràn trở lại → **Không đạt** (giới hạn chiều cao đang chốt cứng, không co theo khung) |  | Lấp `GAP-4` · cover `F1`, `T1` · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: **screenshot full màn ở 1366 và 1920** · dẫn từ `TC-RM-288` (kho FA-004) · Kiểm chứng trực tiếp Rủi ro 2 dev tự nêu ("320px cố định hợp với khung 500px hiện tại") |
| TC-UI002-01 | UI | UI-002 | Popup — Preview theo trình duyệt | Normal | Preview ảnh dọc hiển thị giống nhau trên Chrome/Windows và Safari/Mac | - Đăng nhập admin, chọn bot A, màn 「ポップアップ（作成）」<br>- Có máy Windows (Chrome) và máy Mac (Safari)<br>- Chuẩn bị 3 ảnh: vuông 1000×1000, dọc 419×2048, cực dọc 419×4096 | 1. Trên **Chrome/Windows**: upload lần lượt 3 ảnh, mỗi ảnh chụp khung 「プレビュー」 và đo chiều rộng × chiều cao ảnh hiển thị<br>2. Lặp lại **toàn bộ** trên **Safari/Mac**<br>3. So từng cặp số đo giữa 2 trình duyệt<br>4. Ở mỗi trình duyệt, kiểm ảnh có bị méo / bị crop / tràn khung không | 3 ảnh × 2 trình duyệt = 6 điểm đo | - 3 cặp số đo giữa Chrome/Win và Safari/Mac **khớp nhau** (chênh lệch chỉ do làm tròn hiển thị)<br>- Không trình duyệt nào để ảnh tràn khung, méo tỉ lệ hoặc bị crop<br>- Đặc biệt ảnh cực dọc: cả 2 trình duyệt cùng co ảnh theo tỉ lệ, không kéo giãn |  | Lấp `GAP-5` · cover `F1`, `T1` · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: **screenshot 2 trình duyệt kèm số đo px** · dẫn từ `TC-RM-111` (kho FA-004, Support #32989 — khách đã từng báo lỗi đúng dạng "preview co ảnh sai") · Fix thuần CSS `max-height` trên `<img>` là điểm Safari/Chromium hay tính khác nhau |
| TC-UI003-02 | UI | UI-003 | Popup — Preview trạng thái lỗi | Abnormal | Ảnh preview không tải được (URL 404) → khung preview không vỡ layout, không tràn | - Đăng nhập admin, chọn bot A, môi trường **PRODUCTION**<br>- Có 1 popup đã lưu kèm ảnh dọc, ảnh đang phục vụ qua đường dẫn media của production<br>- Có cách làm ảnh không tải được: dùng popup có ảnh đã bị xóa/đổi, hoặc chặn domain media trong DevTools > Network request blocking | 1. Mở màn sửa popup đó, chặn request tới domain media (hoặc dùng popup có ảnh đã bị xóa)<br>2. Reload màn, quan sát khối 「プレビュー」<br>3. Kiểm khung điện thoại mẫu còn nguyên vẹn không, phần text/nút bên dưới có bị đẩy lệch không<br>4. Bỏ chặn, reload lại, xác nhận preview trở về bình thường | Popup có ảnh dọc, URL ảnh trả 404 | - Khung 「プレビュー」 vẫn hiển thị đúng khung điện thoại mẫu, **không trắng vùng, không vỡ layout, không tràn**<br>- Thẻ ảnh gãy (nếu hiện) vẫn bị giới hạn trong khung, không đẩy phần nội dung phía dưới ra ngoài<br>- Không có thông báo "thành công" giả; sau khi bỏ chặn thì preview hiển thị lại đúng |  | Lấp `GAP-6` · cover `F1`, `T1` · Môi trường: **PRODUCTION** (ảnh phục vụ qua `p.lmes.jp`/B2 — `ENV-003`) · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: **screenshot khung preview lúc ảnh 404 + tab Network thấy request lỗi** · Bổ sung trạng thái **lỗi** còn thiếu của `UI-003` (TC-UI003-01 mới cover trạng thái rỗng) |
| TC-MEDIAIMG001-04 | UI | MEDIA-IMG-001 | Popup — Preview popup đã tồn tại | Normal | Popup TẠO TRƯỚC bản fix, mở lại màn sửa → ảnh dọc đã lưu cũng hết tràn khung | - Có ≥1 popup **đã tạo từ trước khi deploy bản fix**, đang gắn ảnh dọc tỉ lệ > 1.6 (ưu tiên lấy đúng popup mà tester đã dùng khi báo bug #39036)<br>- Bản fix đã deploy lên môi trường đang test<br>- **Không** upload lại ảnh mới cho popup đó | 1. Vào danh sách popup, mở màn sửa của popup cũ nói trên<br>2. Quan sát khối 「プレビュー」 ngay khi màn vừa load, không thao tác gì thêm<br>3. Đo chiều cao ảnh và đối chiếu với khung điện thoại mẫu<br>4. Bấm lưu lại popup (không đổi ảnh), reload màn, quan sát preview lần nữa | Popup cũ + ảnh dọc đã lưu từ trước fix (không upload lại) | - Ảnh dọc của popup cũ hiển thị trọn trong khung 「プレビュー」, giữ đúng tỉ lệ, không chờm ra ngoài — **giống hệt popup mới tạo**<br>- Sau khi lưu lại và reload, preview vẫn đúng<br>- Xác nhận fix áp cho **dữ liệu cũ**, không chỉ ảnh vừa upload trong phiên |  | Lấp `GAP-8` · cover `BUG`, `F1`, `T1` · **regression** · Môi trường: **PRODUCTION** · Đánh giá spec: Spec không ghi — đã hỏi Leader · Evidence: **screenshot preview của popup cũ kèm ngày tạo popup** · Lấp `AP-3` (MJ-9): mọi TC hiện có đều dùng ảnh vừa upload trong phiên, chưa TC nào chạm popup đã tồn tại |

> **Ánh xạ sang 16 cột của `04-tc-list.md`** (khi member copy vào file 04): `ID`→`TC No.` · `Tên case`→`Tiêu đề test case` · `Mã quan điểm`→`Mã quan điểm liên kết` · `Tiền điều kiện`→`Điều kiện tiền đề` · `Dữ liệu nhập`→`Dữ liệu test/input`; tách `Ghi chú` trả lại `Môi trường test` + `Trạng thái đánh giá spec`; `Kết quả thực thi` = `Chưa test`.
>
> **Sau khi Leader duyệt** → push về **đúng nguồn gốc là Studio task #203** bằng `/sync-review-tc <folder> studio` (`testcase_create` idempotent theo `client_ref = ID`). **Không** push sang Sheet.

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — 4 mục:

**§6-1. `[MAJOR]` Không có spec nào định nghĩa hành vi ĐÚNG của khối 「プレビュー」 màn popup.**
- Đã tra đủ 3 nguồn theo thứ tự: (1) `spec-features/admin/` — **không có thư mục popup**; `spec-features/admin/index.md:28` ghi FA-018 Popup ở trạng thái **`CHƯA`** trên mọi cột; (2) `https://lme.jp/manual/` → `category/promotion/pop_up/` — chỉ là trang danh mục, **không mô tả** màn tạo/sửa, mục 画像 hay khối プレビュー; (3) không có link Confluence/Docs nào được cung cấp.
- Hệ quả: `Kết quả mong đợi` của cả 7 TC hiện tại đều dựa vào **suy luận từ implementation** (320px) chứ không có chuẩn đối chiếu. Đây chính là lý do cả 7 TC có `spec_status = null` (MN-4) — đáng lẽ phải là `Spec không ghi` + ghi rõ đã hỏi ai.
- **Nội dung cần update**: bổ sung `spec-features/admin/popup/feature-spec.md` cho FA-018, tối thiểu ghi rõ business rule của khối preview: preview dùng để làm gì, có bắt buộc phản ánh đúng tỉ lệ popup thật không, kích thước ảnh khuyến nghị là bao nhiêu.
- **Người chịu trách nhiệm**: `<Leader phân công>`

**§6-2. `[MAJOR]` SPEC-CONFLICT (mềm) — chuẩn "preview không được co ảnh" vs ý đồ fix này.**
- Fix #39036 **cố ý** để ảnh h/w > 1.6 hiển thị hẹp hơn chiều rộng khung preview (dev tự nêu: `1000x2000 → 160x320`).
- Trong kho TCs có tiền lệ ngược chiều: **TC-RM-111** (FA-004, Support **#32989**, 04-12-2025) — *"ảnh preview để chiều cao TỰ ĐỘNG theo chiều rộng: **ảnh half size không bị co**"*, tức khách đã từng **báo ticket** về việc preview co ảnh sai.
- 2 bên khác feature (richmenu vs popup) và khác bản chất (méo tỉ lệ vs thu nhỏ giữ nguyên tỉ lệ) → **không đủ căn cứ để tự chọn bên**.
- **Cần Leader/PM chốt**: preview popup ưu tiên *"nằm gọn trong khung điện thoại mẫu"* hay *"phản ánh đúng tỉ lệ popup thật trên site khách"*? Câu trả lời quyết định `Kết quả mong đợi` của `TC-OUTPREVIEW001-01/-02/-03`.

**§6-3. `[MAJOR]` Yokoten chưa xử lý — popup thật trên site khách còn nguyên cùng pattern lỗi.**
- Dev ghi rõ: *"popup thật hiển thị trên site khách (`embedded-popup/default_setting.js`) cũng chỉ set width 100% không giới hạn chiều cao — cùng pattern nhưng khác phạm vi ticket nên chỉ ghi nhận, không sửa"*.
- Đây là phần **người dùng cuối thực sự nhìn thấy**. Nếu đóng #39036 với kết luận "ảnh dọc không còn tràn khung" thì dễ hiểu nhầm là đã xử lý xong cả phía khách.
- **Cần quyết định**: tách ticket mới cho `embedded-popup/default_setting.js`, hay mở rộng phạm vi #39036. Kèm theo (BL-3): yêu cầu dev cung cấp **danh sách đầy đủ** các khối hiển thị ảnh dùng pattern `img` không giới hạn chiều cao.

**§6-4. `[NIT]` Ngưỡng 320px là hằng số phụ thuộc khung 500px.**
- Dev tự nêu Rủi ro 2: *"320px là con số cố định hợp với khung 500px hiện tại; nếu sau này đổi kích thước `.popup__preview` thì phải chỉnh lại"*.
- **Đề nghị**: ghi ràng buộc này vào spec FA-018 (§6-1) để lần sau ai đổi `.popup__preview` biết phải chỉnh kèm.

**Ngoài spec — đề nghị bổ sung kho TCs**: `kho-tcs` chưa có **FA-018 Popup**. Sau khi ticket này đóng, chạy `/collect-tcs Popup` để bộ TC này (7 TC gốc + 9 TC bổ sung) trở thành nền regression cho các lần sau.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ✅ (TC-TOOLKNOW002-01 mô phỏng đúng steps file 01) · A.2 ⚠️ F1 thiếu Abnormal, **F3 GAP** · A.3 N/A (không có data impact) · A.4 ⚠️ **T2 GAP**, T1 chỉ có regression happy-path · A.5 ✅ không có ORPHAN · **A.6 ❌** (xem §3.5 — trục phụ 0/5)
- [x] **B. Chất lượng từng TC** — B.1 ✅ (title có keyword, precondition dựng được, expected đo lường được, `tech_note` tách oracle/business rất tốt) · B.2 ⚠️ MN-1 (`#12828` test rộng hơn steps) · B.3 ✅ · B.4 ✅ (data là kích thước px thật, không dùng `"test"`/`"abc"`)
- [x] **C. Chất lượng bộ TC** — ❌ **Normal 5 / Abnormal 0 / Boundary 2** (MJ-10) · ✅ không trùng lặp (§4.5) · ⚠️ phân bố quan điểm lệch (3/7 TC dồn vào `MEDIA-IMG-001`, 2 TC gắn sai mã) · N/A phân quyền · ❌ **không có TC multi-device/responsive dù là task UI** (MJ-6, MJ-7) · N/A i18n
- [x] **D. Spec alignment** — ❌ **không có spec để đối chiếu** (§6-1); tiền lệ kho có căng thẳng chuẩn (§6-2)
- [x] **E. Hành chính** — ⚠️ `TC No.` sinh đúng format repo nhưng 2 mã quan điểm sai (MJ-3, MJ-4) · ✅ file đúng folder · ⚠️ toàn bộ TC còn `status = draft`, `reviewed = false`
- [x] **F. Base quan điểm test LME**
  - [x] **F.1** Quan điểm (tầng 1) — bảng dưới
  - [x] **F.2** Catalog (tầng 2) — **A**: `DI-16 Upload ảnh` ✅ đã đối chiếu (trục shape vuông/dọc/ngang khớp; phần *"upload A rồi thay bằng B"*, *"double click nút upload"*, *"file đổi đuôi giả"* thuộc **luồng upload không bị chạm code** → **không** đòi TC, tránh AP-5) · **B**: `UIC-13` ❌ chưa kiểm 1366×768 + Chrome/Safari (MJ-6, MJ-7); `UIC-11` ⚠️ thiếu trạng thái lỗi (MJ-8); `UIC-15` ⚠️ asset sau merge — gộp BL-2 · **C**: N/A (không chạm gửi tin / friend info / tag / plan / bill) · **D/D2**: ❌ **0 TC production dù task chạm media + asset release** (BL-2); không có job nền liên quan · **E**: `MED-L10` ✅ ngưỡng resize 2048 / chặn 10.000px đã đúng trong data test; `MED-12` ✅ *"preview mở được cả trước và sau khi save"* — TC-TOOLKNOW002-01 step 5 có cover
  - [x] **F.3** RULE — **RULE-01** ❌ (MJ-5) · **RULE-02** ❌ (MJ-2) · **RULE-03** ✅ (mọi × đều có lý do, xem F.1) · **RULE-06** ✅ N/A (không có output LINE/mail/file; "output cuối" của popup là **site khách** → đã ép vào BL-1) · **RULE-07** ✅ N/A (không có CRUD data mới; mục 4.2 = "Không có") · **RULE-08** ❌ (BL-2) · **RULE-09** ✅ × có lý do (popup chưa từng version-up) · **RULE-11** ✅ đã tuân thủ (NT-4) · **RULE-12** ⚠️ vùng ảnh hưởng dev cung cấp chưa đủ (BL-3)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `OUT-PREVIEW-001` | **Cao** | ◯ **BẮT BUỘC** — chức năng có chế độ preview; đây là ticket **về chính khối preview** | — (7/7 TC dừng ở màn admin) | **GAP → `[BLOCKER]` BL-1** |
| `ENV-003` | **Cao** | ◯ **BẮT BUỘC** — chạm media hiển thị + asset release | — (0 TC staging/production) | **GAP → `[BLOCKER]` BL-2** |
| `DEPLOY-ASSET-001` | **Cao** | ◯ **BẮT BUỘC** — release sửa file CSS | TC-DEPLOYASSET001-01 (chỉ `Normal`, chỉ `local`, version stamp khả nghi) | **RISK → `[BLOCKER]` BL-2 + `[MAJOR]` MJ-5 (RULE-01)** |
| `REG-SHARED-001` | **Cao** | ◯ — *"fix bug **có thể tồn tại ở chức năng tương tự**"*; dev tự khai yokoten ở `embedded-popup` | — | **GAP → `[BLOCKER]` BL-3** |
| `MEDIA-IMG-001` | Trung bình *(không nâng Cao: ảnh không gửi ra LINE user, không dùng cho richmenu/imagemap)* | ◯ — resize / tỉ lệ / shape ảnh | TC-MEDIAIMG001-01/-02/-03 (+ TC-TOOLKNOW002-01 về nội dung) | **RISK** — trục shape đủ 5/5 ✅ nhưng chỉ chạy `local`, thiếu popup cũ (MJ-9) |
| `UI-003` | Trung bình | ◯ — mọi màn có xử lý bất đồng bộ | TC-UI003-01 (chỉ trạng thái **rỗng**) | **RISK → `[MAJOR]` MJ-8** (thiếu trạng thái **lỗi**) |
| `UI-001` | Trung bình | ◯ — thay đổi layout, hằng số 320px gắn với khung 500px | — | **GAP → `[MAJOR]` MJ-6** |
| `UI-002` | Trung bình | ◯ — fix thuần CSS; Safari/Mac là surface chính của user | — | **GAP → `[MAJOR]` MJ-7** |
| `DATA-CACHE-001` | Trung bình → **Cao** (output user-facing) | ◯ — *"release có đổi JS/asset"* | TC-DEPLOYASSET001-01 | **RISK** — chỉ `local`, gộp BL-2 |
| `MEDIA-001` | Trung bình | ◯ — chức năng có upload ảnh, **nhưng luồng upload không bị chạm code** | TC-TOOLKNOW002-01 (đi qua luồng upload thật) | **OK** — không đòi thêm TC (AP-5 / root-cause layer focus) |
| `FUNC-004` | **Cao** | **×** — task không chạm giới hạn ký tự / số lượng / dung lượng nào | TC-FUNC004-01 **gắn nhầm mã** | **`[MAJOR]` MJ-4** — gắn lại `MEDIA-IMG-001` |
| `TOOL-KNOW-002` | *(không có trong framework)* | — | TC-TOOLKNOW002-01 | **`[MAJOR]` MJ-3** — không tính là cover quan điểm nào; gắn lại mã framework |
| `MEDIA-CLEAN-001` | Trung bình → Cao khi cho phép xóa/thay file | **×** — fix không chạm luồng xóa/thay file; `PopupService::uploadImagePopup` không bị sửa | — | × **có lý do** (RULE-03) |
| `COMPAT-LEGACY-001` | **Cao** | **×** — popup **chưa từng version-up**; không có cặp cũ/mới (template group, form `s.lmes.jp` vs `step3.lmes.jp`, remind, header spread) | — | × **có lý do** — nhưng khía cạnh "bản ghi tạo trước fix" vẫn được cover bằng `TC-MEDIAIMG001-04` (MJ-9) |
| `DEPLOY-LIVE-001` | **Cao** | **×** — không đổi payload API / field form / cấu trúc request; chỉ 1 file CSS tĩnh | — | × **có lý do** |
| `REG-RUN-001` | **Cao** | **×** — không có job / dữ liệu chạy dở nào liên quan tới CSS tĩnh | — | × **có lý do** |
| `SYNC-APP-001` | Trung bình | **×** — màn tạo/sửa popup là màn admin web | — | × — ⚠️ **cần Leader xác nhận** màn popup có xuất hiện trên mobile app LME không; nếu có thì trigger khớp và phải mở lại |
| `DATA-*` (DATA-001, DATA-DB-001, DATA-COUNT-001, DATA-REF-001, DATA-MIG-001, DATA-AUDIT-001, DATA-BACKUP-001) | Cao | **×** — mục 4.2 dev impact = **"Không có"**; fix là CSS tĩnh, không CREATE/UPDATE/DELETE/MIGRATE dữ liệu nào | — | × **có lý do** |
| `PERM-*` · `SEC-*` · `PAY-*` · `MSG-*` · `CONC-*` · `INTG-*` · `JOB-001` · `BULK-001` · `LIST-001` · `PERF-LARGE-001` · `FRIEND-001` · `STATE-*` · `UI-INPUT-001` · `UI-FIELD-001` · `OUT-TRUTH-001` · `OUT-EXPORT-001` · `NOTI-MAIL-001` · `LIFF-ENTRY-001` | — | **×** — fix 1 rule CSS trong khung preview màn admin: không chạm quyền, tiền, gửi tin, đồng thời, tích hợp ngoài, job nền, thao tác hàng loạt, danh sách, hiệu năng, friend info, lifecycle, ô nhập liệu, thông báo kết quả, export, mail, LIFF | — | × **có lý do** (RULE-03) |
| §4 checklist-lme (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) | — | — | — | **KHÔNG dùng để flag** (RULE-11) — không mục nào liên quan (NT-4) |

---

## 8. Ký duyệt

| Vai trò | Tên | Ngày | Kết luận |
|---|---|---|---|
| Reviewer (Leader) | `<điền>` | `2026-08-26` | **REJECTED** — 3 BLOCKER, 10 MAJOR, 4 MINOR, 4 NIT |
| Tester tiếp nhận | `haodtb` | | |

### Việc cần làm trước vòng review 2

1. **BL-2 trước tiên** — deploy lên STAGING, chạy lại **cả 7 TC hiện có** + `TC-ENV003-01` + `TC-DEPLOYASSET001-02`; kiểm ngay chuỗi `?v=` của `detail.css` có đổi sau deploy không. *(Run staging `#644` đang `queued` — chờ nó chạy xong rồi đọc kết quả, đừng kết luận từ run `local`.)*
2. **BL-1 + BL-3** — dựng 1 trang web test có nhúng popup, chạy `TC-OUTPREVIEW001-01/-02/-03`; yêu cầu dev gửi **danh sách đầy đủ** các khối preview dùng pattern `img` không giới hạn chiều cao.
3. **MJ-3, MJ-4, MN-1…MN-4** — sửa trên **Studio** (`testcase_update`), rồi `/review-tc` fetch lại. Không sửa tay `04-tc-list.md`.
4. **MJ-1** — tester tick 2 checkbox verify auto-fill ở `01-bug-task.md` và `03-dev-impact.md`.
5. **MJ-2** — chạy lại và đính evidence cho cả 7 TC (screenshot khung preview **kèm số đo px**).
6. **§6** — Leader/PM chốt §6-2 (chuẩn preview) và §6-3 (tách ticket cho popup thật) trước khi chốt `Kết quả mong đợi` của nhóm `TC-OUTPREVIEW001-*`.
