# 05 — Review Report

> Ticket: **Redmine #39642** — `[Friend info + Salon + Lesson] Validate nếu nhập label option trả lời giống nhau thì báo lỗi`
> Review round 1 · Draft cho Leader verify.

---

## 0. Nguồn TC

| Mục | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, task `#111` (`ticket 39642`, feature `friend-info`, type `fix-bug`, round `1`, chưa archived — chỉ có **1 task duy nhất** cho ticket này) |
| Tổng TC lấy về | **60 TC** |
| Thời điểm fetch | `2026-09-04` (`testcase_list(task_id=111, limit=100)`) |
| Snapshot đã ghi | `04-tc-list.md` — refresh từ Studio, header `<!-- source: MCP LME TEST STUDIO ... -->` |
| Nguồn 2 (Sheet human) | **Không dùng** — human không cung cấp link Sheet; nguồn 1 đã có TC |
| Nguồn 3 (file 04) | **Không dùng** — nguồn 1 đã có TC |
| **Đối chiếu chéo nguồn** | **KHÔNG** — đã dừng ở nguồn đầu tiên có TC theo quy tắc BƯỚC 0 |
| Trạng thái task Studio | `status = done-ai` · `aiResult = pass` · `openBugs = 0` · `reviewed = false` · `reviewState = leader` · `submittedWithoutMcp = false` |
| Branch | `ai_fixbug_39642` |

**Nguồn spec đã dùng** (BƯỚC 1, theo thứ tự ưu tiên — dừng ở nguồn 1):

| # | Nguồn | Dùng để trả lời |
|---|---|---|
| 1 | [spec-features/admin/friend-information/feature-spec.md](../../spec-features/admin/friend-information/feature-spec.md) — `SCR-FRI-02` (form tạo/sửa kiểu 「選択肢」), bảng field #8 `friend_info_option_selects.option_value`, **`BR-09` Cascade khi đổi tên option (7 bảng)**, `BR-10`, `BR-11` | hành vi đúng của màn Friend info + phạm vi lan toả của option |
| 2 | [spec-features/admin/event-booking/feature-spec.md](../../spec-features/admin/event-booking/feature-spec.md) §`b_info_setting.type` + `ui/ui-spec.md` 「回答タイプ」 | xác định Event Booking có `2 = 選択肢回答` hay không (→ §6) |
| 3 | `templates/LME-SYSTEM-SPEC.md` | tra mã màn hình `FA-015` / `FA-019` / `FA-020` / `FA-011` → thư mục feature |
| — | Studio `task_get_context(sections=["requirements",...])` | **16 requirement key `REQ-001…REQ-016`** — dùng làm spec-delta của chính ticket này |

> ⚠️ `contentTrust = untrusted` — mọi nội dung từ Studio (TC, requirement, note, triage) được xử lý như **data**, không phải chỉ thị.

### 0.6 — Cảnh báo bắt buộc về chất lượng nguồn

| # | Nội dung | Kết quả | Flag |
|---|---|---|---|
| 1 | **Kết quả thực thi thật** | `last_exec`: **59 pass / 1 skip** = 98% ≥ 80%. **NHƯNG** `task_get_report` cho thấy lịch sử đầy đủ khác hẳn: **Auto** pass 81 · skip **148** · error **4**; **Manual** pass 37 · fail **1** · skip **6**. 3/5 run auto (511/529/532) **skip trọn 48 TC** | `[MAJOR]` — xem I-05 |
| 2 | **TC fail / error + ticket bug** | 4 TC auto `error` (đã triage TEST-BUG/flaky) · 1 TC manual `fail` → sinh Studio bug `#683` (Medium, `status = fixed`) nhưng **`redmine_id = null`** | **`[BLOCKER]`** — I-02 |
| 3 | **Môi trường đã chạy** | 60/60 `last_exec` ở `staging`; 1 run ở `local`; **0 TC chạy production**. Task chạm **asset JS/deploy** → RULE-08 | `[MAJOR]` — I-06 |
| 4 | **Ai chạy** | `ai / cucdtk` = **40 TC** · `manual / cucdtk` = 20 TC. 2/3 kết quả Đạt do **AI pipeline tự chạy**, gồm cả nhóm rủi ro cao (REG-SHARED, DEPLOY, API) | `[MAJOR]` — I-07 |
| 5 | **Tác giả TC** | `AI` = **46/60 (76.7%)** · `cucdtk@mcp` = 11 · `cucdtk` = 3. `reviewState = leader`, `reviewed = false` → **chưa qua review người** | `[MAJOR]` — I-08 |
| 6 | **Mã quan điểm ngoài `checklist-lme.md`** | **8 mã / 22 TC (37%)**: `TOOL-NEGCTRL-001`(9) · `TOOL-OLDREC-001`(4) · `TOOL-KNOW-002`(3) · `API-001`(3) · *(trống)*(3) · `TOOL-PAIRWISE-001`(2) · `TOOL-SCOPE-001`(1) · `I18N-001`(1) | **`[BLOCKER]`** — I-03 |

---

## 1. Verdict

### ❌ REJECTED

Còn **4 `[BLOCKER]`**. Bộ TC có chất lượng nội dung **tốt trên mức trung bình** (steps cụ thể, dữ liệu test thật, có negative control, có TC chốt ranh giới server theo yêu cầu leader), nhưng **không đủ điều kiện đóng ticket** vì 3 lý do độc lập:

1. Bằng chứng cho thấy **fix có thể không tới được người dùng** (asset version không bump) mà TC duy nhất kiểm điều đó **bị skip**.
2. Một **bug đã tìm ra và đã fix nhưng không có ticket Redmine** — không truy vết được.
3. **37% TC dùng mã quan điểm không tồn tại trong khung của dự án** → không map được coverage.

---

## 2. Tóm tắt cho member

**Điểm tốt:** bộ TC bám rất sát 16 requirement key, chia đều 3 màn (Friend info 16 · Salon 16 · Lesson 12), có **negative control** đầy đủ (không chặn nhầm thao tác hợp lệ) — đây là chiều hay bị bỏ sót nhất với fix kiểu "thêm guard"; có TC `NEW-42/45/46` chốt ranh giới server đúng theo yêu cầu leader và ghi rõ "KHÔNG báo bug" để tránh raise nhầm; TC `NEW-7` xử lý dữ liệu cũ rất chuẩn (dựng tiền đề qua endpoint, kiểm chứng trên UI).

**Điểm phải fix:** (1) TC `NEW-44` — thứ duy nhất chứng minh người dùng thật nhận được JS mới — đang **skip**, trong khi chính note của TC ghi commit sau force-push **không bump asset version**; đây là rủi ro "fix xanh trên staging nhưng chết trên production"; (2) 22 TC đang mang mã quan điểm nội bộ Studio (`TOOL-*`, `API-001`, `I18N-001`) không có trong `framework/checklist-lme.md` → phải remap; (3) thiếu hẳn chiều **giới hạn ký tự / số lượng lựa chọn** (`FUNC-004`) và chiều **Boundary cho kiểu 「ポイント」**; (4) 3 TC cuối (`NEW-59/60/61`) thiếu mã quan điểm, thiếu tiền đề, sai màn trong steps và có expected mâu thuẫn nội bộ.

---

## 3. Coverage Matrix

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — 3 màn thiếu validate chặn trùng lựa chọn | Root cause | `NEW-4` (FI), `NEW-6` (FI point), `NEW-19` `NEW-20` `NEW-21` `NEW-22` (Salon), `NEW-31` `NEW-32` `NEW-33` (Lesson) | 9 | 9/9 | `OK` |
| **F1** `saveInforFriend` + `hasDuplicateSettingActionValue` (`infor_friend/create.js`) | Direct | `NEW-1,2,4,5,6,7,8,9,10,11,12,13,14,53,54,59` | 16 | 16/16 | `OK` |
| **F2** `updateFormQuestion` + `hasDuplicateOptionTitle` (`calendar_salon/calendar_detail.js`) | Direct | `NEW-15…28`, `NEW-55,56,60` | 17 | 17/17 | `OK` |
| **F3** cùng bộ hàm cho Lesson (`calendar_management/calendar_detail.js`) | Direct | `NEW-29…38`, `NEW-57,58,61` | 13 | 13/13 | `OK` |
| **F4** `config/sns-line.php` — version asset | Direct | `NEW-44` (**skip**), `NEW-43` | 2 | **1/2** | **`RISK`** |
| **F5** `hasDuplicateLabels` + `validateItemForm` — fix gốc Biểu mẫu (KHÔNG sửa code) | Indirect / regression | `NEW-40` | 1 | 1/1 | **`RISK`** — 1 TC gộp 6 loại item, không có Abnormal riêng từng loại |
| **D1** *(Dev khai: không có data impact)* | — | Không TC nào verify **ở tầng DB** rằng "bị chặn ⇒ không có bản ghi/không có row `friend_info_option_selects` mới". Toàn bộ kiểm chứng qua UI + reload | 0 | — | **`RISK`** — RULE-07 |
| **T1** Friend Information (FA-015) | High | `NEW-1…14`, `53,54,59`, `NEW-52` (phía LINE user) | 17 | 17/17 | `OK` |
| **T2** Salon Booking (FA-020) | High | `NEW-15…28`, `55,56,60`, `NEW-48,49` | 19 | 19/19 | `OK` |
| **T3** Lesson / Calendar Booking (FA-019) | High | `NEW-29…38`, `57,58,61`, `NEW-50,51` | 15 | 15/15 | `OK` |
| **T4** Form Builder (FA-011) — regression thuần | Medium | `NEW-40` | 1 | 1/1 | **`RISK`** |
| **T5** Mọi màn dùng asset JS (browser cache sau release) | Medium | `NEW-44` (**skip**), `NEW-43` | 2 | **1/2** | **`GAP`** — chiều "F5 thường trên browser còn cache bản cũ" **không có kết luận** |

### ORPHAN TCs

| TC | Nhận xét |
|---|---|
| `NEW-42` `NEW-45` `NEW-46` `NEW-47` (API-001 ×3 + negative control) | **Không phải orphan thừa.** Không cover `BUG`/`F*`/`T*` vì fix **không chạm tầng server**, nhưng được tạo có chủ đích theo yêu cầu leader (`REQ-015`) để chốt mốc so sánh. Note của TC ghi rõ "KHÔNG báo bug cho #39642" → đúng cách. **Giữ nguyên.** |
| `NEW-59` `NEW-60` `NEW-61` | **Lạc chuẩn**: không có `Mã quan điểm liên kết`, không `Loại case`, không `Điều kiện tiền đề`, `exec_mode = auto` nhưng thực tế chạy manual. Nội dung chồng vùng với `NEW-53/55/57` — xem §4.5. |

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape nhận diện từ `03-dev-impact.md` mục 2**: khớp **2 shape** —

| Shape | Keyword khớp trong mục 2 | Câu hỏi adversarial | Trả lời từ bộ TC | Kết luận |
|---|---|---|---|---|
| **"validate input" / "thêm kiểm tra" / "chặn ngay trước khi lưu"** | *"thêm kiểm tra trùng giá trị… ngay trước khi lưu"*, *"so sánh sau khi trim"*, *"bỏ qua ô đang trống"* | Cover bao nhiêu **input variant**? Có test **server-side**? Đủ **5 pattern biên** (biên / biên±1 / 0 / rỗng)? Đủ **luồng vào** create / edit / **copy** / import / API? | Variant: ✅ tốt (số, chuỗi trim, hoa-thường, độ rộng ký tự, Unicode VN/JP, ký tự đặc biệt, label `0`, trùng không liền kề). Server-side: ✅ có (`NEW-42/45/46/47`). **5 pattern biên: ❌ KHÔNG có biên độ dài label, không có biên số lượng lựa chọn** (0 / 1 / max / max+1). Luồng vào: create ✅ · edit ✅ · copy ✅ (`NEW-8` — **và copy chỉ tồn tại ở Friend info**; Salon/Lesson không có chức năng sao chép calendar, question item thuộc calendar chứ không theo コース) · import CSV — N/A (3 màn này không có) · API ✅ (`NEW-42/45/46`) | **`[MAJOR]` FIX-SHAPE** → I-04 (chỉ còn thiếu **biên**, luồng vào đã đủ) |
| **"sửa hàm dùng chung" / triển khai ngang từ fix gốc** | *"Triển khai ngang validate… sang 3 màn còn thiếu"*, *"đã có sẵn fix gốc… chỉ đọc để đối chiếu"* | Có **danh sách nơi ảnh hưởng do DEV cung cấp**? TC test **từng nơi**? Chức năng **tương tự (Salon ⇄ Lesson ⇄ Booking Event)** đã rà? | Danh sách Dev: ✅ có (mục 3 file 03, 9 dòng). Test từng nơi: ✅ (FI 16 · Salon 16 · Lesson 12 · Form 1). **Booking Event: ❌ Dev không nêu đã rà; `checklist-lme.md` REG-SHARED-001 ghi rõ "cặp Salon / Lesson / Booking Event là điểm lặp lại"** | **`[MAJOR]` FIX-SHAPE** → I-12 |

**Bổ sung — shape "JS / asset / build"** (mục 2 có *"Bump version asset để trình duyệt nạp JS mới"*, mục 4.1 liệt kê `config/sns-line.php`):

> Câu hỏi: test **F5 thường** (không Ctrl+F5) trên browser còn cache bản cũ? Network tab có asset 404?
> Trả lời: TC `NEW-44` được thiết kế **đúng** cho việc này, nhưng **bị `skip`**, tester ghi *"Không test được"* / *"lúc release lên có clear cache"* — tức điều kiện thí nghiệm đã bị phá (cache được xoá thủ công), đúng cái mà TC muốn loại trừ. Note của chính `NEW-44` còn ghi commit `6356ec93a4` (sau force-push) **KHÔNG còn đổi `config/sns-line.php`**.
> → **`[BLOCKER]` FIX-SHAPE** → I-01.

**Symptom-only KH report check**: ❌ **Không áp dụng**. Ticket tracker là `Triển khai ngang`, không phải bug KH báo triệu chứng; `01-bug-task.md` không có Steps/Expected/Actual vì Redmine không có section "Tái hiện bug". Root cause đã xác định chính xác ở tầng code (thiếu guard ở 3 file JS), không có "nhiều root cause khả dĩ" cần loại trừ.

**Anti-pattern** — rà đủ AP-1 → AP-6 theo [framework/anti-patterns.md](../../framework/anti-patterns.md):

| AP | Dính? | Căn cứ |
|---|---|---|
| **AP-1** Single-trigger generic-fix | **Không** | Mục 2 file 03 **không có** keyword `set error message` / `handle exception` / `try-catch` / `fallback message`. Fix là guard `if` so sánh danh sách, không phải catch-all. Không áp dụng. |
| **AP-2** Symptom-only KH report | **Không** | File 01 không mô tả triệu chứng — ticket tracker `Triển khai ngang`, description nêu **nguyên văn 2 message lỗi cần có** và liệt kê chính xác các loại item phải áp dụng. Root cause xác định ở tầng code (thiếu guard ở 3 file JS), không có "root cause thay thế" cần loại trừ. |
| **AP-3** Happy-path-only regression | **DÍNH** | Mục 4.3 có `T1…T5`. `T1/T2/T3` cover dày (17/19/15 TC). Nhưng **`T4` (Form Builder) chỉ 1 TC** (`NEW-40`, `Normal`, tiền đề data sạch) và **`T5` (asset/cache) 2 TC trong đó 1 skip** → `[MAJOR] [AP-3]` I-25 |
| **AP-4** Specific code-check disguised as generic catch | **DÍNH** | Mục "Commit / Pull Request" của file 03 = `<không có link PR>`. Không verify được fix shape thực tế — đặc biệt nghiêm trọng ở ticket này vì đã có **force-push** và **2 mã commit mâu thuẫn** (`2faaa0caaf` vs `6356ec93a4`) → `[MAJOR] [AP-4]` I-26 |
| **AP-5** Layer-downstream over-coverage | **DÍNH (nhẹ)** | `NEW-42/45/46/47` test **tầng server**, mà fix **không sửa 1 dòng code server nào**. Theo AP-5 phải re-label. Nhưng đây là **yêu cầu của leader** (`REQ-015`) để chốt mốc so sánh → **giữ lại, chỉ re-label**, không remove → `[NIT] [AP-5]` I-19 |
| **AP-6** Mục 3 dev-impact trống | **Không** | Mục 3 file 03 có **9 dòng** function/file kèm loại thay đổi và lý do, cộng danh sách màn đã kiểm-và-loại-trừ (`setting_add_friend`, `chat`, `qr_code`, `calendar_*`). Đầy đủ. |

---

## 3.6 Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | **Cao** | ◯ mọi chức năng | `NEW-1,15,29,48,49,50,51,52` | 8/8 | **`[MAJOR]` RULE-01** — **8/8 đều `Normal`**, không có Abnormal, không có Boundary |
| `FUNC-002` | **Cao** | ◯ màn có form nhập liệu | Nội dung có ở `NEW-11` (`FUNC-003`), `NEW-12/27/37` (`FUNC-SEQ-001`), `NEW-8` (copy — Friend info, **luồng copy chỉ tồn tại ở màn này**), `NEW-42/45/46` (API) — **không TC nào mang mã `FUNC-002`** | — | **`[MAJOR]`** — chưa cover **theo mã** (I-03). **Nội dung thực chất đã đủ luồng vào**: create / edit / copy / API; import CSV N/A |
| `FUNC-003` | Trung bình | ◯ field có định dạng (bắt buộc nhập) | `NEW-11` | 1/1 | `OK` |
| `FUNC-004` | **Cao** | ◯ **có giới hạn số ký tự label + số lượng lựa chọn** (kho xác nhận: `TC-FRI-74` 50 option, `TC-LSN-355` 50/51 ký tự) | **KHÔNG CÓ TC NÀO** | 0 | **`[BLOCKER]`** — I-04 |
| `FUNC-MULTI-001` | Trung bình | ◯ thêm ≥2 phần tử cùng loại trong 1 đối tượng | `NEW-17,30` (thêm/xoá dòng lựa chọn) | 2/2 | `RISK` — không có chiều **di chuyển / sắp xếp lại** |
| `FUNC-UNIQ-001` | Trung bình | ◯ **đây chính là bản chất fix** (unique check trong 1 danh sách) | Nội dung có ở `TOOL-KNOW-002` ×3, `DATA-TEXT-001` ×7 — **không TC nào mang mã `FUNC-UNIQ-001`** | — | **`[MAJOR]`** — chưa cover theo mã (kho dùng đúng mã này: `TC-FRI-61/62/64/65/95/96/98`) |
| `FUNC-SEQ-001` ★ | Trung bình (**BẮT BUỘC** — màn có Sort + nhiều tab setting) | ◯ | `NEW-12,27,37` (chỉ chuỗi "trống + trùng") | 3/3 | **`[MAJOR]`** — thiếu chuỗi **Add→Sort · Edit→Sort · Sort→Sort + F5**, dù Dev khẳng định guard phủ "kéo sắp xếp lại lựa chọn" |
| `CONC-001` | **Cao** | ◯ nhiều tab cùng sửa 1 bản ghi | `NEW-53,55,57` (2 tab), `NEW-54,56,58` (double-click), `NEW-59,60,61` | 9/9 | `RISK` — có 2/4 kịch bản; **thiếu kịch bản (3) 2 user khác nhau**; Evidence **không có "số lần xử lý thực tế" từ log/DB** |
| `CONC-003` ★ | Trung bình | ◯ nhiều tab cùng gọi API | `NEW-53,55,57` | 3/3 | `RISK` — không có throttling / delay response |
| `DATA-TEXT-001` | Trung bình **→ Cao** (label hiển thị cho **LINE user** ở form booking) | ◯ | `NEW-5,10,13,14,26,28,36` | 7/7 | **`[MAJOR]` RULE-01** — 1 Abnormal + 6 Boundary, **không có Normal**; và **RULE-06**: chưa đối chiếu hiển thị trên **LINE app thật** (chỉ `NEW-48…52` chạm phía user, nhưng không dùng ký tự đặc biệt) |
| `DATA-REF-001` | **Cao** | ◯ option được tham chiếu — **`BR-09` cascade 7 bảng** khi đổi tên option | `NEW-25` (liên kết tới trường cũ có option trùng) | 1/1 | **`[MAJOR]`** — kho có `TC-FRI-120` (đổi TEXT option → cascade); guard nằm **cùng hàm lưu** với cascade nhưng không TC nào verify cascade còn nguyên → I-13 |
| `DATA-DB-001` ★ | **Cao** | ◯ chức năng có UPDATE | Không TC nào query DB | 0 | **`[MAJOR]`** — vế **`WHERE` scope 2 tài khoản** đánh **×** có lý do (RULE-03): fix **không chạm 1 dòng code server/query nào**. Vế còn lại (chặn ⇒ không ghi DB) **vẫn thiếu** → RULE-07, I-09 |
| `OUT-TRUTH-001` | **Cao** | ◯ mọi thao tác lưu có thông báo | `NEW-9,24,35` | 3/3 | **`[MAJOR]` RULE-01** — **3/3 đều `Abnormal`**, không có Normal ("báo thành công ⇒ đã lưu thật"), không có Boundary |
| `UI-FIELD-001` | Trung bình | ◯ field phụ thuộc lựa chọn cha (情報タイプ / 表示方法) | `NEW-16` | 1/1 | `OK` |
| `UI-INPUT-001` ★ | Trung bình (**BẮT BUỘC** — mọi màn có ô nhập text) | ◯ | **KHÔNG CÓ TC NÀO** | 0 | **`[MAJOR]`** — thiếu **paste bằng chuột phải** (JS chỉ nghe keyboard event → guard có thể không chạy), thiếu maxlength, thiếu verify trim ở **DB** → I-10 |
| `LIFF-ENTRY-001` ★ | **Cao** | ◯ Salon/Lesson booking sinh URL cho LINE user | `NEW-48,49,50,51,52` | 5/5 | **`[MAJOR]` RULE-01** — 5/5 `Normal`; thiếu **case chưa kết bạn**, thiếu **link cũ `step3.lmes.jp` ⇄ mới `s.lmes.jp`**, và **thiếu case dữ liệu cũ còn option trùng thì LINE user thấy gì** → I-14 |
| `FRIEND-001` | **Cao** | ◯ đọc/ghi friend info | `NEW-2` (Normal), `NEW-6` (Abnormal) | 2/2 | **`[MAJOR]` RULE-01** — **thiếu `Boundary`**; đúng chỗ Dev đã cảnh báo (`'5'` vs `'05'`) → I-15 |
| `REG-SHARED-001` | **Cao** | ◯ triển khai ngang từ fix gốc | `NEW-21,22,32,33,40,55,57` | 7/7 | **`[MAJOR]`** — thiếu `Boundary`; **thiếu rà Booking Event** (FA-021) → I-12 |
| `COMPAT-LEGACY-001` ★ | **Cao** | ◯ dữ liệu cũ tạo trước fix còn option trùng | Nội dung có ở `TOOL-OLDREC-001` ×4 (`NEW-7,23,25,34`) — **không TC nào mang mã `COMPAT-LEGACY-001`** | — | **`[BLOCKER]`** theo BƯỚC 3 (quan điểm Cao chỉ được cover bởi mã Studio lạ = chưa cover) → gộp vào I-03 |
| `DEPLOY-ASSET-001` ★ | **Cao** | ◯ release sửa 3 file JS | `NEW-44` | **0/1 (skip)** | **`[BLOCKER]`** — I-01 |
| `DEPLOY-LIVE-001` ★ | **Cao** | ◯ release production không maintain | `NEW-43` | 1/1 | **`[MAJOR]` RULE-01** — 1 TC `Abnormal`, thiếu Normal + Boundary |
| `ENV-003` ★ | **Cao** | ◯ chạm asset/domain phục vụ file tĩnh | `NEW-43,44` | 1/2 | **`[MAJOR]` RULE-08** — 0 TC production, mà `DEPLOY-ASSET-001` **bắt buộc bằng chứng lấy trên production** → I-06 |
| `SEC-ISO-001` | **Cao** | ◯ nhiều tab cùng hiển thị 1 đối tượng | `NEW-53,55,57,59,60,61` | 6/6 | `OK` |
| `DATA-001` | **Cao** | ◯ option được tham chiếu nơi khác | `NEW-25` | 1/1 | `RISK` — xem `DATA-REF-001` |
| `PERM-001/002/003/004` | Cao | **×** | — | — | Đánh **×** — fix không chạm phân quyền, không chạm query có `bot_id`/`staff_id` (RULE-03: lý do rõ) |
| `MSG-*`, `PAY-*`, `JOB-*`, `INTG-*`, `MEDIA-*`, `BULK-*`, `PERF-LARGE-001`, `STATE-*`, `REG-RUN-001` | Cao | **×** | — | — | Đánh **×** — fix thuần validate phía giao diện, không gửi tin, không tiền, không job nền, không media, không batch |

**Quan điểm ◯ nhưng KHÔNG có TC nào (GAP thật)**: `FUNC-004` · `UI-INPUT-001`.
**Quan điểm ◯ chỉ được cover bởi mã Studio lạ (tính là chưa cover)**: `COMPAT-LEGACY-001` · `FUNC-002` · `FUNC-UNIQ-001`.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER]` I-01 — `NEW-44` (DEPLOY-ASSET-001): TC duy nhất chứng minh fix tới được người dùng đang bị `skip`, trong khi bằng chứng nói asset version KHÔNG được bump.**
Ba dữ kiện chồng nhau:
- `03-dev-impact.md` mục 2 ghi *"Bump version asset để trình duyệt nạp JS mới"* và mục 4.1 liệt kê `config/sns-line.php` là file thay đổi.
- Studio `REQ-014` + note của chính `NEW-44` ghi ngược lại: *"commit hiện tại của nhánh fix (`6356ec93a4`, **sau force-push**) KHÔNG còn đổi `config/sns-line.php`, tức KHÔNG bump phiên bản asset"* (nhánh fix `202608062210`, base `202608191616`).
- `NEW-44` `skip` 3 lượt, tester ghi *"Không test được"* và *"lúc release lên có clear cache"* — cache đã bị xoá thủ công, đúng điều kiện mà TC muốn loại trừ.

→ Kịch bản hỏng: release lên production **không** clear cache thủ công → browser người dùng giữ JS cũ → **guard không tồn tại → toàn bộ fix vô hiệu, nhưng mọi TC trên staging vẫn xanh**.
**Đề xuất fix:** (a) Dev xác nhận nhánh nào đang chuẩn bị release và asset version có bump không; (b) nếu không bump → yêu cầu bump trước khi release; (c) chạy lại `NEW-44` **trên production, F5 thường, browser còn cache bản cũ**, ghi lại giá trị tham số version ở cả 3 màn.
> ⚠️ Leader đã quyết **không đưa TC bổ sung cho mục này vào §5** — xử lý bằng cách **chạy lại `NEW-44` đang `skip`** trên Studio (env `prd`), không tạo TC mới.

**`[BLOCKER]` I-02 — Studio bug `#683` đã fix nhưng KHÔNG có ticket Redmine (`redmine_id = null`).**
TC `NEW-53` (`tc_id 11572`) `fail` ngày `2026-08-25`, sinh bug `#683` *"[Manual] Friend info - Mở cùng màn tạo/sửa ở 2 tab và thao tác độc lập không ghi đè sai dữ liệu thất bại"* (Medium), nay `status = fixed`, `openBugs = 0`, và `NEW-53` re-run `pass`.
Vấn đề: **không có ticket Redmine nào ghi nhận bug này** → không truy vết được đã fix ở commit nào, không vào được bộ regression theo RULE-12 (3) *"mọi case đã từng Không đạt và được fix"*, và Leader duyệt ticket #39642 sẽ không thấy nó tồn tại.
**Đề xuất fix:** raise ticket Redmine cho bug `#683` (hoặc ghi journal vào chính #39642 nêu rõ bug + commit fix), rồi cập nhật `redmine_id` trên Studio.

**`[BLOCKER]` I-03 — 22/60 TC (37%) dùng mã quan điểm KHÔNG tồn tại trong `framework/checklist-lme.md` → coverage không map được; 3 quan điểm ưu tiên Cao/Trung bình bị tính là CHƯA COVER.**

| Mã Studio | # TC | Mã chuẩn đề nghị remap |
|---|---|---|
| `TOOL-NEGCTRL-001` | 9 | `FUNC-001` (Normal, negative control) hoặc `CONC-001` (nhóm 2-tab / double-click) |
| `TOOL-OLDREC-001` | 4 | **`COMPAT-LEGACY-001`** (Cao) |
| `TOOL-KNOW-002` | 3 | **`FUNC-UNIQ-001`** (hoặc `FUNC-002`) |
| `API-001` | 3 | **`FUNC-002`** (luồng vào "gọi API trực tiếp") |
| *(trống)* | 3 | `CONC-001` — xem I-16 |
| `TOOL-PAIRWISE-001` | 2 | `DATA-TEXT-001` |
| `TOOL-SCOPE-001` | 1 | `DATA-REF-001` (copy) |
| `I18N-001` | 1 | `UI-002` |

Hệ quả trực tiếp: `COMPAT-LEGACY-001` (**Cao**), `FUNC-002` (**Cao**), `FUNC-UNIQ-001` (Trung bình) đều **không có TC nào mang mã chuẩn** dù nội dung đã được test.
**Đề xuất fix:** remap `viewpoint` trên Studio bằng `testcase_update` — **KHÔNG cần viết TC mới**, chỉ đổi mã. Nếu team muốn giữ mã `TOOL-*` làm mã nội bộ thì phải bổ sung chúng vào `framework/checklist-lme.md` (kèm chạy lại `python scripts/build_indexes.py`).

**`[BLOCKER]` I-04 — `FUNC-004` (Cao) không có TC nào: thiếu hoàn toàn chiều giới hạn ký tự và số lượng lựa chọn.**
Fix so sánh chuỗi label sau `trim`. Chưa ai kiểm: 2 label **dài đúng maxlength** và chỉ khác nhau ở ký tự **vượt quá** maxlength (bị cắt ⇒ thành trùng thật, hoặc ngược lại), danh sách lựa chọn **số lượng lớn** (kho `TC-FRI-74` xác nhận 50 option là kích thước thực tế), và trường 「選択肢」 **không có option nào** (kho `TC-FRI-73`). Spec `SCR-FRI-02` ghi 「管理名」 max 20 ký tự nhưng **không ghi giới hạn cho `option_value`** → phải hỏi Dev nguồn limit (RULE-05 nội bộ).
**Đề xuất fix:** Leader đã quyết **không đưa TC `FUNC-004` vào §5 lần này** (chưa có limit chính thức của `option_value` — xem §6 mục 9). Quan điểm này **vẫn để trạng thái chưa cover**; mở lại sau khi Dev cung cấp giới hạn thật.

### 4.2 Major (nên fix)

**`[MAJOR]` I-05 — `last_exec` che mất lịch sử run thật.** Bảng TC hiển thị "59 Đạt / 1 skip" (98%), nhưng `task_get_report` cho thấy: Auto **skip 148 · error 4**, Manual **fail 1 · skip 6**; **3/5 run auto (511/529/532) skip trọn 48 TC**. — *Đề xuất:* Leader xác nhận 3 run skip-toàn-bộ là lỗi hạ tầng hay **môi trường chưa deploy nhánh fix** (nếu là vế sau thì run 535 mới là run hợp lệ duy nhất trên staging).

**`[MAJOR]` I-06 — RULE-08 / `ENV-003`: 0/60 TC chạy production.** `DEPLOY-ASSET-001` yêu cầu bằng chứng **lấy trên production** (browser cache + Network tab version), `DEPLOY-LIVE-001` yêu cầu release production không maintain. Kết luận "đã test xong" từ staging là **không hợp lệ** cho 2 quan điểm này. — *Đề xuất:* `NEW-43`, `NEW-44` chạy lại với `env_scope = prd`.

**`[MAJOR]` I-07 — 40/60 kết quả Đạt do AI pipeline tự chạy (`source = ai`), gồm cả nhóm rủi ro cao.** `NEW-40` (regression Biểu mẫu — vùng T4), `NEW-16`, `NEW-41`, `NEW-42` (chốt ranh giới server) đều `source = ai`. — *Đề xuất:* QA người chạy lại tối thiểu `NEW-40`, `NEW-42/45/46` và toàn bộ nhóm `REG-SHARED-001`.

**`[MAJOR]` I-08 — 46/60 TC (76.7%) do `AI` sinh, `reviewed = false`, `reviewState = leader`.** Bộ TC chưa từng qua review người trước khi chạy. — *Đề xuất:* chính report này là vòng review đó; sau khi xử lý các mục dưới, set `reviewed` trên Studio.

**`[MAJOR]` I-09 — RULE-07: không TC nào verify ở tầng DB.** Mọi TC "bị chặn ⇒ không lưu" chỉ kiểm bằng reload màn list. Với Friend info, option nằm ở bảng riêng `friend_info_option_selects` (spec FA-015 §field #8) → có thể xảy ra ghi nửa vời (setting đã tạo, option chưa) mà UI list không lộ. — *Đề xuất:* bổ sung bước query DB vào `NEW-4`/`NEW-6`, hoặc thêm `TC-DATADB001-01` (§5).

**`[MAJOR]` I-10 — `UI-INPUT-001` không có TC nào.** Guard Salon/Lesson chạy theo sự kiện rời ô (`@blur`), guard Friend info chạy lúc bấm 「保存」. Chưa ai kiểm **paste bằng chuột phải** (JS thường chỉ nghe keyboard event) và **verify trim ở DB**. — *Đề xuất:* `TC-UIINPUT001-01` (§5).

**~~`[MAJOR]` I-11 — thiếu luồng vào "copy" ở Salon và Lesson.~~ — ĐÃ RÚT (finding sai).**
Kiểm chứng lại: màn danh sách lịch Salon (`SCR-SLN-01`) chỉ có 「新規作成」 · dropdown 「カレンダータイプ」 · 「並び替え」 · toggle 有効/無効 · 「予約管理ページを開く」 · **copy URL vào clipboard** · preview — **không có chức năng sao chép calendar**; kho `fa020` 14 TC của section "Màn list calendar" cũng không có TC copy calendar (`TC-SLN-09` chỉ là copy 2 URL). Salon có copy ở cấp **コース** (ticket #28450) nhưng 「予約時のお客様への質問項目」 thuộc **calendar** (tab 「予約設定」), không đi theo course.
→ Luồng "copy" của `FUNC-002` **chỉ tồn tại ở Friend info** (spec FA-015: `Clone: setting + actions + action_details + filter_v2 + option_selects`) và **đã được `NEW-8` cover**. Không có GAP. TC đề xuất `TC-FUNC002-01` đã được gỡ khỏi §5.

**`[MAJOR]` I-12 — FIX-SHAPE / `REG-SHARED-001`: chưa rà Booking Event (FA-021).** `checklist-lme.md` ghi rõ *"cặp Salon / Lesson / Booking Event là điểm lặp lại"*. Spec xác nhận Event Booking có `b_info_setting.type = 2 「選択肢回答」`. Dev mục 3 chỉ loại trừ `setting_add_friend`, `chat`, `qr_code`, `calendar_*` — **không nhắc Event Booking**. — *Đề xuất:* hỏi Dev (§6 mục 7) + `TC-REGSHARED001-08` (§5).

**`[MAJOR]` I-13 — `DATA-REF-001` / `BR-09`: cascade 7 bảng không được verify.** Spec FA-015 `BR-09` (tin cậy **Cao**, `FriendInformationController.php:969-1406`): đổi tên option → cập nhật **7 bảng**, trong đó có `calendar_setting_send_forms` (Lesson) và `calendar_salon_setting_send_forms` (Salon). Guard mới đặt trong `saveInforFriend` **trước** `validateAll`, tức **trên cùng đường đi với cascade**. Hai rủi ro chưa ai kiểm: (a) khi guard chặn, cascade có chạy nửa vời không; (b) cascade từ Friend info có thể **ghi đè tên hiển thị đã tuỳ biến ở Salon/Lesson và tạo ra trùng mà guard phía Salon/Lesson không bao giờ nhìn thấy** (vì không đi qua UI). Kho có `TC-FRI-120` cho cascade nhưng chưa có chiều duplicate. — *Đề xuất:* `TC-DATAREF001-01/02` (§5).

**`[MAJOR]` I-14 — `LIFF-ENTRY-001`: 5/5 TC phía LINE user đều `Normal`, thiếu case dữ liệu cũ còn trùng.** `REQ-013` chấp nhận bản ghi cũ vẫn còn option trùng. Chưa ai kiểm **LINE user nhìn thấy gì** khi item hiển thị 2 lựa chọn **giống hệt nhau**, và khi chọn cái thứ 2 thì `friend_information_value` ghi giá trị nào. Đây là đúng triệu chứng gốc mà ticket muốn diệt (*"gây nhầm lẫn cho khách khi trả lời và ghi sai dữ liệu"* — file 03 mục 1). Cũng thiếu case **chưa kết bạn** và **link cũ `step3.lmes.jp` ⇄ mới `s.lmes.jp`**. — *Đề xuất:* `TC-LIFFENTRY001-01` (§5).

**`[MAJOR]` I-15 — `FRIEND-001` (Cao) thiếu `Boundary`, đúng chỗ Dev đã cảnh báo.** File 03 mục 7.4: *"Loại Điểm so sánh dạng chuỗi sau trim, nên `'5'` và `'05'` vẫn coi là khác nhau"* — Dev tự nhận đây là điểm chưa xử lý. Không TC nào kiểm. Kho có `TC-FRI-96` (2 ngưỡng khác dấu cách) nhưng không có case số 0 đứng đầu. — *Đề xuất:* `TC-FRIEND001-03` (§5).

**`[MAJOR]` I-16 — `NEW-59` / `NEW-60` / `NEW-61` không đạt chuẩn TC (4a #1, #2, #4).** Cả 3: **thiếu `Mã quan điểm liên kết`**, **thiếu `Loại case`**, **`Điều kiện tiền đề` rỗng**, `exec_mode = auto` nhưng thực tế `last_exec.source = manual`. Ngoài ra `Tiêu đề` giống hệt nhau ở cả 3 TC (*"Mở 2 tab thực hiện tạo label ở 2 tab giống nhau"*) → không suy được TC nào cho màn nào nếu không mở cột `screen`. — *Đề xuất:* điền `viewpoint = CONC-001`, `case_type = Abnormal`, thêm tiền đề, sửa `exec_mode = manual`, và thêm tiền tố màn vào tiêu đề (`Friend info - …` / `Salon - …` / `Lesson - …`) cho đồng bộ với `NEW-53/55/57`.

**`[MAJOR]` I-17 — `NEW-61` sai màn trong `Các bước thực hiện`.** TC gắn `screen = Lesson` nhưng bước 1 ghi *"Vào màn setting item **salon**"* (copy nguyên từ `NEW-60`). Người test làm đúng theo steps sẽ test nhầm màn Salon lần 2 và **màn Lesson không được kiểm** — đúng vùng `F3`. — *Đề xuất:* sửa steps thành *"Vào màn setting item **lesson**"*.

**`[MAJOR]` I-18 — RULE-01: 6 quan điểm ưu tiên Cao thiếu loại case, không TC nào ghi lý do.**

| Quan điểm | Normal | Abnormal | Boundary | Thiếu |
|---|---|---|---|---|
| `FUNC-001` | 8 | 0 | 0 | Abnormal + Boundary |
| `OUT-TRUTH-001` | 0 | 3 | 0 | Normal + Boundary |
| `FRIEND-001` | 1 | 1 | 0 | Boundary |
| `LIFF-ENTRY-001` | 5 | 0 | 0 | Abnormal + Boundary |
| `REG-SHARED-001` | 1 | 6 | 0 | Boundary |
| `DEPLOY-LIVE-001` | 0 | 1 | 0 | Normal + Boundary |

— *Đề xuất:* bổ sung TC theo §5, hoặc ghi lý do vào `Ghi chú` của TC đại diện (VD `DEPLOY-LIVE-001` không có khái niệm biên).

**`[MAJOR]` `[AP-3]` I-25 — Regression chỉ có happy path ở `T4` và `T5`.** `T4` (Form Builder — vùng fix gốc, không sửa code) chỉ có `NEW-40` với tiền đề data sạch, không có TC nào chạy Biểu mẫu ở **trạng thái biên**: item đã có sẵn label trùng từ trước, item có số lượng option lớn, item 「診断」 (bind `.value` chứ không phải `.label` — chính điểm Dev phải giải trình riêng ở mục 6 file 03). `T5` chỉ 2 TC và 1 đang skip. AP-3 nêu đúng rủi ro: *"regression không phải chỉ verify happy path còn chạy mà phải verify edge state cũ không bị break thêm"*. — *Đề xuất:* thêm 1 TC `Abnormal` cho Biểu mẫu với item 「診断」 đã có label trùng từ trước fix (dựng qua endpoint), verify hành vi **không đổi** so với trước.

**`[MAJOR]` `[AP-4]` I-26 — Không có link Pull Request → không verify được fix shape thực tế.** File 03 mục "Commit / Pull Request" = `<không có link PR>`. Với ticket này AP-4 nguy hiểm hơn bình thường vì: nhánh đã **force-push**, tồn tại **2 mã commit mâu thuẫn** (`2faaa0caaf` theo Redmine vs `6356ec93a4` theo Studio), và điểm khác nhau giữa 2 bản chính là **có/không đổi `config/sns-line.php`** — tức là đúng thứ quyết định `[BLOCKER]` I-01. Không đọc được diff thì không thể tự kết luận. — *Đề xuất:* yêu cầu Dev cung cấp link PR/diff của **bản đang nằm trên môi trường test**, hoặc dán output `git diff --stat release_step_20260805...ai_fixbug_39642` mới nhất vào ticket.

### 4.3 Minor (có thể fix sau)

**`[MINOR]` I-20 — `NEW-40` gộp 6 loại item Biểu mẫu vào 1 TC (4a #5).** Note của tác giả giải thích đây là chủ ý (dataset chung 1 oracle) nên **không tính là vi phạm atomic**, nhưng hệ quả vẫn thật: nếu TC fail, không biết loại item nào hỏng, mà đây là **vùng regression T4 duy nhất**. — *Đề xuất:* giữ 1 TC nhưng ghi `Kết quả thực thi` **theo từng loại item** ở `Evidence`, hoặc tách khi có loại nào từng lỗi.

**`[MINOR]` I-21 — 6 cặp TC trùng tiêu đề nguyên văn giữa các màn** (xem §4.5) — phải mở cột `screen` mới phân biệt được. — *Đề xuất:* thêm tiền tố `Friend info - / Salon - / Lesson -` như `NEW-14`, `NEW-20`, `NEW-31` đã làm.

**`[MINOR]` I-22 — RULE-02: cột `Evidence thực tế` rỗng ở toàn bộ 60 TC** (`testcase_list` không trả về trường này). Không kiểm chứng được kết quả `Đạt` có bằng chứng đúng loại hay không. — *Đề xuất:* Leader mở Studio đối chiếu evidence của nhóm rủi ro cao (`NEW-40`, `NEW-42/45/46`, `NEW-44`).

**`[MINOR]` I-23 — `Trạng thái đánh giá spec` (`spec_status`) rỗng ở toàn bộ 60 TC.** Không phân biệt được TC nào dựa trên spec ghi rõ, TC nào tự suy diễn. Riêng `NEW-41` có note *"nếu tester thấy chênh lệch thì BÁO LEADER/PO xác nhận"* → thực chất là `Spec không ghi`. — *Đề xuất:* điền `spec_status` cho tối thiểu nhóm `REQ-010` (2 câu thông báo khác nhau) và `REQ-015`.

### 4.4 Nit (gợi ý)

**`[NIT]` `[AP-5]` I-19 — 4 TC tầng server test layer không bị chạm code.** `NEW-42/45/46/47` verify endpoint lưu, trong khi fix **không sửa 1 dòng code server nào** (4 file thay đổi đều là `.js` + `config/sns-line.php`). Theo AP-5 đây là over-coverage tầng downstream. **Nhưng KHÔNG đề nghị bỏ** — đây là yêu cầu trực tiếp của leader (`REQ-015`) nhằm chốt mốc so sánh cho tương lai, và note của `NEW-42` đã ghi rõ *"KHÔNG báo bug cho ticket #39642"* → đúng cách xử lý. — *Đề xuất:* re-label 4 TC này sang `tc_group` riêng hoặc ghi `Ghi chú` = `mốc so sánh — không thuộc phạm vi fix #39642` để lần review sau không bị tính nhầm vào coverage của `F1/F2/F3`.

**`[NIT]` I-24 — `03-dev-impact.md` và `01-bug-task.md` chưa tick "Tester verify auto-fill chính xác".** Cả 2 file có `Auto-filled: 2026-09-04 by /new-task` nhưng checkbox chưa tick → F/D/T có thể thiếu hoặc map sai. Đã được chứng thực: mục 4.1 `F4` liệt kê `config/sns-line.php` là file thay đổi, **nhưng Studio nói commit sau force-push không còn đổi file này** (I-01). — *Đề xuất:* tester đọc lại Redmine + đối chiếu `git diff` nhánh `ai_fixbug_39642` rồi tick.

**`[NIT]` RULE-11 — §4 `checklist-lme.md`**: các mục "chưa đủ bằng chứng" (`FORM-01`, `TPL-01`, `ADM-01/03/04`) có liên quan tới màn Biểu mẫu / Friend info nhưng **không được dùng để flag** — chỉ nêu ở đây làm gợi ý cho vòng regression sau.

---

## 4.5 TC trùng lặp nội dung

Đã rà **60/60 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `kết quả mong đợi`).

**Kết quả: KHÔNG có `DUP-EXACT`.** 6 cặp TC trùng **tiêu đề nguyên văn** đều là **cùng kịch bản áp lên 3 màn khác nhau** (`screen` khác nhau) → **không phải trùng lặp**, chỉ là vấn đề đặt tên (→ I-21):

| Tiêu đề lặp | TC | Màn | Kết luận |
|---|---|---|---|
| "Hai lựa chọn chỉ khác nhau ở khoảng trắng đầu cuối vẫn bị coi là trùng" | `NEW-10` / `NEW-26` / `NEW-36` | FI / Salon / Lesson | **Không trùng** — 3 màn, 3 file JS khác nhau |
| "Lựa chọn khác nhau về chữ hoa thường hoặc độ rộng ký tự…" | `NEW-13` / `NEW-28` / `NEW-38` | FI / Salon / Lesson | **Không trùng** — nhưng `NEW-38` mang mã `TOOL-PAIRWISE-001` còn 2 cái kia `DATA-TEXT-001` → **mã không nhất quán**, gộp vào I-03 |
| "Vừa có ô lựa chọn trống vừa có lựa chọn trùng…" | `NEW-12` / `NEW-27` / `NEW-37` | FI / Salon / Lesson | **Không trùng** — ⚠️ expected **cố ý khác nhau**: FI báo **trùng trước**, Salon/Lesson báo **trống trước** (`REQ-012`) |
| "Nhập các lựa chọn khác nhau cho item Lựa chọn đơn thì tự lưu thành công" | `NEW-15` / `NEW-29` | Salon / Lesson | **Không trùng** |
| "Các thao tác sửa khác trên item không bị chặn nhầm…" | `NEW-17` / `NEW-30` | Salon / Lesson | **Không trùng** |
| "Thông báo trùng không lặp lại khi rời khỏi ô nhiều lần liên tiếp" | `NEW-24` / `NEW-35` | Salon / Lesson | **Không trùng** |

**1 nhóm cần xử lý:**

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| 2 tab cùng sửa 1 bản ghi — Friend info / Salon / Lesson | `NEW-53` · `NEW-55` · `NEW-57` (đủ tiền đề, expected rõ, có mã quan điểm) | **GỘP** `NEW-59` · `NEW-60` · `NEW-61` vào 3 TC trên — **KHÔNG xóa** | `DUP-SUBSET` **+** `DUP-CONFLICT` | Cùng `đối tượng + thao tác` (mở 1 bản ghi ở 2 tab, sửa label, lưu ở cả 2) và cùng `tiền đề tương đương`. Khác ở `dữ liệu`: `NEW-53/55/57` dùng label **khác nhau** giữa 2 tab (đối chứng âm — không được cảnh báo nhầm); `NEW-59/60/61` dùng label **trùng nhau** (đối chứng dương). `NEW-59/60/61` thiếu `mã quan điểm` và `loại case` nên không so được 2 yếu tố còn lại | `[MAJOR]` |

**Vì sao GỘP chứ không xóa (gate BƯỚC 4b):** `NEW-59/60/61` là **TC duy nhất** mang biến thể dữ liệu "label trùng nhau khi thao tác 2 tab". Xóa đi thì `CONC-001` mất chiều đối chứng dương → phải chuyển từ "xóa" sang "gộp": đưa bước 「nhập label trùng nhau ở cả 2 tab」 làm **bước bổ sung** của `NEW-53/55/57`, rồi xóa `NEW-59/60/61`.

⚠️ **`DUP-CONFLICT` — `NEW-59/60/61` có `Kết quả mong đợi` MÂU THUẪN NỘI BỘ**, không tự giải quyết được:
> *"Tab 2 khi save sẽ ghi đè giá trị của tab 1"* **và** *"Không cho tạo các item có giá trị trùng nhau"*

Hai vế loại trừ nhau: nếu guard chặn lưu thì **không có** chuyện tab 2 ghi đè; nếu tab 2 ghi đè được thì guard **đã không chặn**. → **KHÔNG tự chọn bên**, đẩy lên §6 mục 5.

**KHÔNG tự xóa/sửa TC nào** — TC Studio là read-only; mọi thay đổi thực hiện qua `testcase_update` / `testcase_delete` trên Studio sau khi Leader duyệt.

---

## 5. TCs đề xuất bổ sung

> **Đã đối chiếu 60 TC ở BƯỚC 0 + 3 file kho** ([kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md](../../kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md) 339 TC · [kho-tcs/fa020-datlichsalon-サロン・面談予約.md](../../kho-tcs/fa020-datlichsalon-サロン・面談予約.md) 498 TC · [kho-tcs/fa019-datlichbaihoc-レッスン予約.md](../../kho-tcs/fa019-datlichbaihoc-レッスン予約.md) 632 TC) — **không TC đề xuất nào trùng.**
>
> **TC kho đã cover sẵn — KHÔNG viết mới, dùng lại:**
> - `TC-FRI-61` (2 option trùng tên → báo lỗi) ≈ `NEW-4` · `TC-FRI-62` (khác dấu cách → vẫn trùng) ≈ `NEW-10` · `TC-FRI-65` (copy rồi tạo trùng) ≈ `NEW-8` · `TC-FRI-95` (2 ngưỡng điểm trùng) ≈ `NEW-6` → **đã có, bỏ qua**.
> - `TC-FRI-63` / `TC-FRI-97` (sau khi báo lỗi trùng → sửa hợp lệ → lưu được): `NEW-7` đã cover cho luồng bản ghi cũ. **Không viết mới.**
> - `TC-FRI-64` / `TC-FRI-98` (2 trường khác nhau được phép trùng option): `NEW-18` cover cho Salon; **Friend info chưa có** nhưng rủi ro thấp → chỉ ghi `[NIT]`, không đưa vào bảng.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FRIEND001-03 | UI | FRIEND-001 | Info kiểu Điểm | Boundary | manual | staging | Hai mốc điểm cùng giá trị số nhưng khác cách viết (số 0 đứng đầu, khoảng trắng) — xác định hành vi so trùng | - Đăng nhập admin, chọn bot<br>- Đang ở màn 「友だち情報管理（作成）」 | 1. Nhập tên quản lý<br>2. 「情報タイプ選択」 chọn 「ポイント」<br>3. Bấm 「追加」 3 lần<br>4. Nhập 3 mốc điểm theo dữ liệu bên dưới<br>5. Bấm 「保存」<br>6. Ghi lại có/không có cảnh báo và giá trị thật sự được lưu<br>7. Lặp lại bước 1–6 với bộ dữ liệu thứ 2 | Bộ 1: 「5」 / 「05」 / 「10」<br>Bộ 2: 「5」 / 「 5 」 (có khoảng trắng 2 đầu) / 「10」 | Bộ 2 (khoảng trắng): **bị chặn** với 「選択肢が重複しています。異なる値を入力してください。」 (so sánh sau trim).<br>Bộ 1 (`05` vs `5`): ghi nhận **hành vi thực tế** — Dev khai 2 giá trị này coi là **KHÁC nhau** nên **lưu được**; nếu ô nhập `type=number` đã tự chuẩn hoá `05`→`5` thì phải **bị chặn**. Hai kết quả loại trừ nhau ⇒ ghi lại kết quả quan sát được và **báo Leader chốt**, không tự kết luận Đạt/Không đạt. |  | Lấp GAP-2 / cover impact F1 · Bù `Boundary` còn thiếu của `FRIEND-001` (RULE-01, I-15) · Đánh giá spec: **Spec không ghi (đã hỏi Dev qua file 03 mục 7.4)** · Evidence: ảnh màn hình 2 bộ dữ liệu + ảnh bản ghi sau khi mở lại · dẫn từ `TC-FRI-96` |
| TC-FUNCSEQ001-04 | UI | FUNC-SEQ-001 | 予約時のお客様への質問項目 | Abnormal | manual | staging | Kéo sắp xếp lại thứ tự lựa chọn rồi sửa thành trùng — guard vẫn chặn và thứ tự sau F5 không đổi | - Lịch Salon có item 「単一選択」 với 4 lựa chọn khác nhau đã lưu | 1. Kéo lựa chọn thứ 4 lên vị trí 1 (Sort)<br>2. **Không reload**, sửa lựa chọn đang ở vị trí 3 thành giá trị giống lựa chọn ở vị trí 1, rời ô<br>3. Ghi lại cảnh báo<br>4. Sửa về giá trị riêng, rời ô<br>5. Bấm **F5**<br>6. Đối chiếu thứ tự và nội dung 4 lựa chọn<br>7. Lặp bước 1–6 cho màn Bài học tab 「全体設定」 | 4 lựa chọn 「松」「竹」「梅」「桜」; bước 2 sửa 「梅」→「桜」 | Bước 3: hiện 「選択肢の表示名が重複しています。異なる値を入力してください。」, không lưu.<br>Bước 6: thứ tự sau F5 **giống hệt** trạng thái ngay sau bước 4 (「桜」「松」「竹」「梅」), không có lựa chọn nào mất hoặc nhân đôi.<br>Màn Bài học cho kết quả tương đương. |  | Lấp GAP-4 / cover impact F2, F3 · Dev khai guard phủ luồng "kéo sắp xếp lại lựa chọn" (file 03 mục 7) nhưng **không TC nào kiểm** · Đánh giá spec: Spec ghi rõ (file 03 mục 7) · Evidence: 2 ảnh cạnh nhau — sau thao tác và sau F5 · dẫn từ `TC-FRI-70`, `TC-LSN-364` |
| TC-DATAREF001-01 | Data | DATA-REF-001 | Sửa info — cascade đổi tên option | Abnormal | manual | staging | Khi guard chặn lưu trường Friend info, cascade 7 bảng KHÔNG được chạy nửa chừng | - Trường Friend info kiểu 「選択肢」 tên 「地域」 có 3 option 「東京」「大阪」「福岡」<br>- 1 lịch Salon có item liên kết tới 「地域」<br>- ≥2 bạn bè đang giữ giá trị 「大阪」 | 1. Ghi lại: option hiện tại ở màn Salon, giá trị của 2 bạn bè ở màn 友だち詳細, số 回答人数 của trường<br>2. Vào màn sửa 「地域」, đổi 「大阪」 thành 「東京」 (tạo trùng)<br>3. Bấm 「保存」 → xác nhận bị chặn<br>4. **Không reload**, bấm 「保存」 thêm 2 lần nữa<br>5. Mở lại trường 「地域」, màn Salon và màn 友だち詳細 của 2 bạn bè<br>6. Đối chiếu với dữ liệu ghi ở bước 1 | Đổi 「大阪」 → 「東京」 (trùng option đã có) | Bước 3: hiện cảnh báo trùng, không lưu.<br>Bước 6: **mọi thứ giống hệt bước 1** — trường vẫn 3 option 「東京」「大阪」「福岡」, item Salon vẫn hiển thị đủ 3 lựa chọn cũ, 2 bạn bè vẫn giữ giá trị 「大阪」, 回答人数 không đổi. **Không có bảng nào bị cập nhật một phần.** |  | Lấp GAP-5 / cover impact F1, D1, T1, T2 · Verify `BR-09` (cascade 7 bảng, spec FA-015) không chạy nửa vời khi guard chặn — guard nằm **cùng hàm lưu** với cascade · Đánh giá spec: Spec ghi rõ (`BR-09`) · Evidence: ảnh 3 màn trước/sau + số 回答人数 · dẫn từ `TC-FRI-120` |
| TC-DATAREF001-02 | Data | DATA-REF-001 | Sửa info — cascade đổi tên option | Abnormal | manual | staging | Cascade từ Friend info có thể tạo ra lựa chọn trùng ở Salon/Lesson mà guard phía Salon/Lesson không nhìn thấy | - Trường Friend info 「地域」 có 2 option 「東京」「大阪」<br>- Lịch Salon có item liên kết 「地域」, đã **sửa tên hiển thị** ở 「表示される選択肢」 thành 「TOKYO」「OSAKA」<br>- Lịch Bài học cấu hình tương tự | 1. Ghi lại 「表示される選択肢」 của Salon và Bài học<br>2. Ở màn Friend info, đổi option 「大阪」 thành 「東京都」 (KHÔNG trùng ở phía Friend info) → lưu thành công<br>3. Mở lại item của Salon và Bài học, đọc 「表示される選択肢」<br>4. Nếu 2 dòng đã trở thành trùng nhau: rời ô ở 1 dòng bất kỳ mà **không sửa gì**<br>5. Thử sửa 1 giá trị khác trên cùng item rồi rời ô | Friend info: 「大阪」 → 「東京都」<br>Salon/Lesson trước đó: 「TOKYO」/「OSAKA」 | Bước 3: ghi nhận 「表示される選択肢」 của Salon/Bài học **có bị cascade ghi đè hay không**.<br>Nếu **có** ghi đè và tạo ra 2 dòng trùng nhau ⇒ đây là **lỗ hổng thật**: dữ liệu trùng vào được hệ thống mà không đi qua guard, và bước 4/5 sẽ chặn người dùng sửa bất kỳ thứ gì khác trên item đó cho tới khi họ tự sửa hết trùng.<br>Nếu **không** ghi đè (tên hiển thị tuỳ biến được giữ) ⇒ Đạt. |  | Lấp GAP-5 / cover impact F1, F2, F3, T2, T3 · Kết hợp `BR-09` (cascade 7 bảng gồm `calendar_salon_setting_send_forms`, `calendar_setting_send_forms`) với `REQ-006`/`REQ-008` · Đánh giá spec: **Spec không ghi — cần hỏi Dev (§6 mục 6)** · Evidence: ảnh 「表示される選択肢」 của cả 2 màn trước/sau |
| TC-LIFFENTRY001-01 | UI | LIFF-ENTRY-001 | LINE User — Đặt lịch Salon / Bài học | Abnormal | manual | staging | LINE user gặp item có 2 lựa chọn hiển thị giống hệt nhau (dữ liệu cũ trước fix) — chọn được và ghi đúng giá trị | - Dựng qua endpoint (giao diện sau fix không tạo được): 1 item 「単一選択」 của lịch Salon có 2 lựa chọn cùng tên 「東京」, và 1 item 「複数選択」 tương tự<br>- Item liên kết tới trường Friend info 「地域」<br>- Tài khoản LINE test **đã là bạn** của OA | 1. Mở URL đặt lịch Salon trong **app LINE thật** (in-app browser)<br>2. Quan sát item — đếm số lựa chọn hiển thị<br>3. Chọn lựa chọn **thứ 2** trong 2 cái trùng tên, hoàn tất booking<br>4. Ở màn admin, mở 予約詳細 của booking vừa tạo<br>5. Mở màn 友だち詳細 của tài khoản LINE đó, xem giá trị trường 「地域」<br>6. Lặp lại bước 1–5 với item 「複数選択」, tick **cả 2** lựa chọn trùng tên<br>7. Lặp lại bước 1–3 với 1 tài khoản LINE **chưa kết bạn** với OA | 2 lựa chọn cùng tên 「東京」 | Bước 2: hiển thị đúng 2 dòng (không tự gộp, không mất dòng).<br>Bước 4–5: giá trị lưu ở 予約詳細 và ở 友だち詳細 **khớp đúng lựa chọn đã chọn**, không rơi vào giá trị của dòng thứ nhất.<br>Bước 6: cả 2 giá trị được ghi nhận, không bị khử trùng.<br>Bước 7: user chưa kết bạn được **redirect sang màn kết bạn** trước khi vào form.<br>Toàn bộ luồng không văng lỗi, không màn trắng. |  | Lấp GAP-11 / cover impact T2, T3 · **RULE-06** — đi tới output cuối trên LINE app thật, không dừng ở màn admin · Bù `Abnormal` còn thiếu của `LIFF-ENTRY-001` (I-14) · Đây đúng triệu chứng gốc ticket muốn diệt (file 03 mục 1: *"gây nhầm lẫn cho khách… ghi sai dữ liệu"*) · Đánh giá spec: Spec ghi rõ (`REQ-013`) · Evidence: ảnh chụp trong app LINE + ảnh 予約詳細 + ảnh 友だち詳細 |
| TC-UIINPUT001-01 | UI | UI-INPUT-001 | Ô nhập lựa chọn (3 màn) | Abnormal | manual | Tất cả | Dán giá trị trùng bằng chuột phải > Paste vẫn kích hoạt được validate chặn trùng | - Máy **Windows** và máy **Mac**<br>- Đang ở màn 「友だち情報管理（作成）」 kiểu 「選択肢」 | 1. Nhập dòng 1 = 「東京」, copy chuỗi này ra clipboard<br>2. Ở dòng 2, dán bằng **chuột phải > Paste** (KHÔNG dùng Ctrl+V)<br>3. Click ra ngoài rồi bấm 「保存」<br>4. Ghi lại có cảnh báo trùng hay không<br>5. Lặp bước 1–4 nhưng dán bằng **Ctrl+V** để đối chiếu<br>6. Lặp toàn bộ trên **Mac** (Cmd+V và chuột phải)<br>7. Lặp toàn bộ ở màn Salon 「予約設定」 và Bài học 「全体設定」 (guard chạy khi rời ô)<br>8. Với 1 cặp lựa chọn hợp lệ có khoảng trắng 2 đầu: lưu thành công rồi **query DB** đối chiếu giá trị đã trim | Chuỗi copy: 「東京」<br>Bước 8: 「 大阪 」 / 「福岡」 | Bước 4 và 5 cho **kết quả giống hệt nhau**: đều hiện cảnh báo trùng và chặn lưu. Nếu dán bằng chuột phải mà **không** kích hoạt validate ⇒ **FAIL** (lỗi kinh điển của JS chỉ nghe keyboard event).<br>Bước 6, 7: kết quả tương đương trên Mac và ở cả 3 màn.<br>Bước 8: giá trị trong DB đã được trim, không còn khoảng trắng đầu/cuối. |  | Lấp GAP-7 / cover impact F1, F2, F3 · `UI-INPUT-001` hiện **0 TC** (I-10) · Bổ sung vế **verify trim ở tầng DB** (RULE-07, I-09) · Đánh giá spec: Spec không ghi · Evidence: ảnh trạng thái sau khi dán bằng chuột phải trên **cả Win và Mac** + kết quả query DB |
| TC-OUTTRUTH001-04 | API | OUT-TRUTH-001 | Lưu trường / item — đối chiếu 3 tầng | Normal | manual | staging | Báo lưu thành công thì dữ liệu thật sự vào DB đủ cả bản ghi cha và các dòng lựa chọn | - Đăng nhập admin, chọn bot<br>- Có quyền truy vấn DB môi trường test | 1. Tạo trường Friend info kiểu 「選択肢」 với 3 lựa chọn khác nhau, bấm 「保存」<br>2. Ghi lại thông báo/điều hướng sau khi lưu<br>3. Query `friend_information_setting` và `friend_info_option_selects` theo bot đang dùng<br>4. Lặp bước 1–3 nhưng lần này nhập 2 lựa chọn **trùng nhau** để bị chặn<br>5. Query lại 2 bảng trên<br>6. Lặp bước 4–5 cho item 「単一選択」 của Salon (bảng `calendar_salon_setting_send_forms`) | Lần 1: 「東京」「大阪」「福岡」<br>Lần 2: 「東京」「東京」「福岡」 | Bước 2–3: quay về danh sách **và** DB có đúng 1 dòng `friend_information_setting` mới + đúng 3 dòng `friend_info_option_selects`.<br>Bước 4–5: hiện cảnh báo trùng, **và DB KHÔNG phát sinh dòng nào** ở cả 2 bảng — không có bản ghi cha mồ côi không có option.<br>Bước 6: Salon cho kết quả tương đương. |  | Lấp GAP-8 / cover impact D1 · Bù `Normal` còn thiếu của `OUT-TRUTH-001` (RULE-01, I-18) · **RULE-07 verify 3 tầng** — hiện 60 TC đều chỉ kiểm qua UI (I-09) · Đánh giá spec: Spec ghi rõ (`REQ-009`) · Evidence: ảnh kết quả query kèm câu query, trước và sau |
| TC-REGSHARED001-08 | UI | REG-SHARED-001 | Booking Event — 質問項目 kiểu 選択肢回答 | Normal | manual | staging | Màn Đặt lịch sự kiện dùng lựa chọn từ Friend info có option trùng vẫn hiển thị và hoạt động đúng | - Cần Dev xác nhận trước (§6 mục 7): Event Booking có ô nhập danh sách lựa chọn tự nhập hay chỉ lấy option từ Friend info liên kết<br>- Dựng qua endpoint: trường Friend info 「地域」 có 2 option trùng 「東京」<br>- 1 sự kiện có item 「選択肢回答」 (`b_info_setting.type = 2`) liên kết tới 「地域」 | 1. Mở màn thiết lập item của sự kiện, chọn item 「選択肢回答」 liên kết 「地域」<br>2. Quan sát danh sách lựa chọn hiển thị và **có cảnh báo trùng nào không**<br>3. Nếu màn có ô nhập lựa chọn tự nhập: nhập 2 giá trị trùng rồi lưu, ghi lại kết quả<br>4. Lưu item, tải lại trang đối chiếu<br>5. Mở URL đặt sự kiện phía LINE user, chọn lựa chọn thứ 2 rồi hoàn tất<br>6. Đối chiếu giá trị ghi nhận ở màn admin | Friend info 「地域」: 「東京」「東京」 | Bước 2: hiển thị đủ 2 lựa chọn, màn **không văng lỗi**.<br>Bước 3: ghi nhận hành vi thật — nếu Event Booking **cho lưu** 2 lựa chọn tự nhập trùng nhau trong khi Salon/Lesson/Friend info/Biểu mẫu đều chặn ⇒ **không nhất quán**, báo Leader mở ticket triển khai ngang bổ sung.<br>Bước 6: giá trị ghi nhận khớp lựa chọn đã chọn. |  | Lấp GAP-10 / cover impact T2, T3 (chức năng tương tự) · `REG-SHARED-001` ghi rõ *"cặp Salon / Lesson / Booking Event là điểm lặp lại"*; Dev **không nêu đã rà** màn này (I-12) · regression · Đánh giá spec: **Spec không ghi — chờ Dev trả lời §6 mục 7 rồi mới chạy** · Evidence: ảnh màn thiết lập item + ảnh phía LINE user |

---

## 6. Spec update needed

| # | Vấn đề | Bằng chứng mâu thuẫn | Cần ai chốt |
|---|---|---|---|
| 1 | **Asset version có được bump hay không** | `03-dev-impact.md` mục 2: *"Bump version asset để trình duyệt nạp JS mới"* + mục 4.1 liệt kê `config/sns-line.php` **⟷** Studio `REQ-014` + note `NEW-44`: *"commit `6356ec93a4` sau force-push KHÔNG còn đổi `config/sns-line.php`"* | **Dev** — quyết định trực tiếp việc fix có tới được người dùng (I-01) |
| 2 | **Commit nào đang nằm trên môi trường test** | Redmine journal: `2faaa0caaf`, 4 file **⟷** Studio: `6356ec93a4`, **sau force-push**, không đổi `config/sns-line.php` | **Dev** — nếu là bản force-push thì `03-dev-impact.md` mục 4.1 đang **sai** và phải sửa lại |
| 3 | **2 thông báo lỗi khác nhau giữa các màn** | Friend info: 「選択肢が重複しています。異なる値を入力してください。」 **⟷** Salon/Lesson/Biểu mẫu: 「選択肢の表示名が重複しています。異なる値を入力してください。」 (thiếu/thừa 表示名). Ticket #39642 mô tả **cả 2 câu** nên hiện trạng đúng ticket, nhưng `NEW-41` đã tự nêu *"BÁO LEADER/PO xác nhận có cần thống nhất một câu hay không"* | **PO / Leader** — chốt giữ 2 câu hay thống nhất 1 câu |
| 4 | **Server không kiểm trùng ở cả 3 endpoint (`REQ-015`)** | `NEW-42/45/46` xác nhận gọi thẳng API vẫn lưu được dữ liệu trùng; file 03 mục 7.2 ghi đây là **giới hạn chủ đích**. Hệ quả: mọi luồng không qua UI (API, copy bot / backup FA-033, action job, cascade `BR-09`) vẫn có thể bơm dữ liệu trùng vào hệ thống | **Leader / PM** — mở ticket riêng cho **cả 4 màn** (kể cả Biểu mẫu) như Dev đề xuất, hay chấp nhận giữ nguyên |
| 5 | **`NEW-59/60/61` có expected mâu thuẫn nội bộ** | *"Tab 2 khi save sẽ ghi đè giá trị của tab 1"* **⟷** *"Không cho tạo các item có giá trị trùng nhau"* — hai vế loại trừ nhau (xem §4.5) | **Dev + Leader** — chốt hành vi đúng khi 2 tab cùng lưu, rồi viết lại expected. **Không tự chọn bên.** |
| 6 | **Nhóm 「表示される選択肢」 nay bị chặn trùng — có đúng ý PM không** | File 03 mục 7.3: nhóm `options_information_friend` *"trước đây không có validate nào; nay bị chặn trùng"*, AI tự quyết định BAO và ghi *"nếu PM muốn thu hẹp thì bỏ đúng 1 block `if`"* | **PM** — xác nhận mở rộng phạm vi này là mong muốn |
| 7 | **Booking Event (FA-021) có nằm trong phạm vi triển khai ngang không** | Spec xác nhận `b_info_setting.type = 2 「選択肢回答」`; `REG-SHARED-001` ghi *"cặp Salon / Lesson / Booking Event là điểm lặp lại"*; Dev mục 3 **không nhắc** màn này | **Dev** — trả lời: màn thiết lập item của Event Booking có ô nhập danh sách lựa chọn **tự nhập** hay chỉ lấy option từ Friend info liên kết? Nếu tự nhập ⇒ còn 1 màn chưa được triển khai ngang (I-12, `TC-REGSHARED001-08`) |
| 8 | **Kiểu 「ポイント」: `'5'` và `'05'` là trùng hay khác** | File 03 mục 7.4: so sánh dạng chuỗi sau trim ⇒ **khác nhau**; nhưng ô nhập là `type=number` nên browser có thể tự chuẩn hoá ⇒ **trùng**. Dev ghi *"không xử lý thêm để tránh phình fix"* | **Leader** — chốt hành vi mong đợi trước khi chạy `TC-FRIEND001-03` |
| 9 | **Giới hạn ký tự của `option_value`** | Spec FA-015 ghi max cho 「管理名」 (20) và 「フォルダ名」 (15) nhưng **bỏ trống** cho 「選択肢」 (bảng field #8: cột giới hạn = `—`) | **Dev** — cung cấp limit thật thì mới viết được TC cho `FUNC-004` (RULE-05 nội bộ: TC phải ghi rõ nguồn của giới hạn). Đây là lý do TC `FUNC-004` **chưa được đưa vào §5** |

---

> **Ghi chú cuối:** report này là **draft cho Leader verify**. Không TC nào bị sửa hay xoá trong quá trình review — toàn bộ 60 TC ở `04-tc-list.md` là snapshot read-only từ Studio task `#111`. Mọi thay đổi TC (remap mã quan điểm ở I-03, gộp TC ở §4.5, thêm TC ở §5) phải thực hiện trên Studio qua `testcase_update` / `testcase_create` / `testcase_delete` sau khi Leader duyệt.
