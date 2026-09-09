# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38294 — [Lme][call] Check process database quá 300s` |
| Reviewer (Leader) | `<Leader điền — draft sinh bởi /review-tc>` |
| Tester được review | `<member điền>` (file 04 hiện là draft do AI `/write-tc` sinh, chưa có người ký) |
| Ngày review | `2026-07-16` |
| Version TCs | `v1 (draft AI 2026-07-16)` |
| Vòng review | `Round 1` |

> **Spec reference**: không có `02-spec-reference.md` → dùng [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) tổng, không có spec riêng cho task này. **Nguồn spec thực tế tốt nhất hiện có** là expected result ở tab TC cũ "improve filter ngày 13/11" (*"setting 25/10/2023 - 1/11/2023 → hiển thị user kết bạn ngày 25/10 <= x <= 1/11"*) — đây là **TC cũ, không phải spec chính thức**.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC bám đúng bản chất "rewrite tương đương" và bắt được nhiều rủi ro thật (biên `23:59:59`, nhánh `NOT EXISTS`, index chưa có). Nhưng **3 BLOCKER** chặn: (1) Dev **chưa cung cấp danh sách caller thật** — mục 3 chỉ lặp lại 2 function được sửa, nên phạm vi regression đang là **suy đoán từ sheet cũ**; (2) TC quan trọng nhất của patch (biên đầu/cuối ngày) có **precondition không dựng được bằng thao tác tay**; (3) hàng loạt TC phụ thuộc **baseline "môi trường chưa có patch" chưa được định nghĩa** → không chạy được.

---

## 2. Tóm tắt cho member

Bộ TC này chọn đúng trục: với một fix thuần tối ưu query, thứ cần chứng minh là **kết quả lọc không đổi** + **không còn process > 300s**, và bạn đã bám đúng vậy thay vì đi test "tính năng chạy được". Ba điểm rất tốt: bắt được biên `23:59:59` chính là chỗ giả định của Dev có thể vỡ; tách riêng nhánh `=N`/`!=N` (không bị rewrite) để chứng minh không đụng nhầm; và phát hiện **index composite không nằm trong patch** — nếu perf chỉ đạt khi có index thì ticket đang phụ thuộc một việc chưa ai làm.

Cần sửa trước vòng 2: **precondition của TC-FUNCDATE001-02 hiện không dựng được** (không ai add friend đúng giây `23:59:59` qua UI — phải xin Dev script seed), và **chốt cách dựng baseline "trước fix"** vì 6 TC đang dựa vào nó. Ngoài ra TC-REGSHARED001-01 gộp 8 màn vào 1 dòng — khi 1 màn fail thì không biết ghi `Kết quả thực thi` thế nào, nên tách ra (§5 đã viết sẵn 6 TC tách cho bạn copy).

Quan trọng nhất: **đừng tự đi test 8 màn dựa trên sheet cũ** — hãy bắt Dev trả lời chính thức ai gọi `advanceFilter`/`advanceFilterPost`. Sheet cũ là gợi ý tốt, không phải cam kết của Dev cho lần fix này.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — query lọc bạn (tag + ngày kết bạn) chạy > 300s | Fix | — | TC-PERFLARGE001-01 (tái hiện đúng khoảng ngày `2025-11-18`→`2026-06-18` + query monitor trong ticket), -02, -03 | 3 | **RISK** — thiếu số liệu quy mô thật (placeholder `<hỏi PM/DBA>`) + chưa loại trừ slow query khác (AP-2) |
| **F1** — `Conversation::advanceFilter` | Function | Direct | TC-FUNCDATE001-01/02, TC-BULK001-01/02/03, TC-REGSHARED001-01 (suy từ màn Friend list) | ~6 | **RISK** — xem [MAJOR] M5: không xác định được màn nào gọi F1 vs F2 |
| **F2** — `Conversation::advanceFilterPost` | Function | Direct | TC-FUNC001-01/02/03, TC-MSG001-01/02/03, TC-REGSHARED001-03 (suy từ màn send all/Broadcast) | ~7 | **RISK** — như trên |
| **D1** — `bot_line_user.followed_at` (READ) | Data | — | TC-FUNCDATE001-01→05, TC-MSGUSER001-01/02, TC-FUNC003-03 | 8 | **OK** — đủ Normal + Abnormal + Boundary (biên giây, xuyên năm, năm nhuận, NULL) |
| **D2** — `tag_line_user.tag_id/line_user_id` (READ) | Data | — | TC-DATACOUNT001-03, TC-MSG001-02, TC-PERM003-01/02, TC-BULK001-03, TC-FUNC001-02 | 6 | **OK** — có cả nhánh EXISTS, NOT EXISTS, `=N`/`!=N` |
| **T1** — Friend Filter / Segment (SC-003) | Feature | `<Redmine không ghi risk>` | TC-FUNC001-01/02/03, TC-FUNCDATE001-01→05, TC-REGSHARED001-01 | ~9 | **OK** |
| **T2** — Broadcast (FA-008) | Feature | `<Redmine không ghi risk>` | TC-MSG001-01/02/03, TC-ENV003-01, TC-REGSHARED001-01 | 5 | **OK** — có full happy path end-to-end tới LINE app thật |
| **T3** — Friend List (FA-013) | Feature | `<Redmine không ghi risk>` | TC-FUNCDATE001-01, TC-BULK001-01/02/03, TC-REGSHARED001-01 | 5 | **OK** |
| **T4–T9 (ngoài 4.3)** — `scenario` · `auto reply` · `action schedule` · `csv` · `cross analysic` · `modal action` | Feature | **chưa được Dev đánh giá** | TC-REGSHARED001-01 (gộp chung 1 TC) | 1 | **RISK** → xem [BLOCKER] B1. 6 màn chia nhau **1 dòng TC**, và nguồn là **sheet cũ chứ không phải Dev** |
| **Phía job** (broadcast / scenario / callback) | Feature | **chưa được Dev đánh giá** | TC-ENV003-01 (theo dõi log 3 job) | 1 | **GAP** → xem [BLOCKER] B1 + §5 TC-JOB001-01 |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | **Không phát hiện orphan.** Mọi TC đều trace được về code path Dev sửa (điều kiện ngày `followed_at` / subquery tag) hoặc về impact F/D/T. | Giữ nguyên |

> **Ghi chú AP-5 (layer-downstream over-coverage)**: TC-FUNC003-02 (gọi thẳng API với ngày sai định dạng, gồm cả `' OR 1=1 --`) **không** phải orphan — patch **nối chuỗi ngày trực tiếp** (`>= 'ngày 00:00:00'`), nên đây chính là code path bị sửa. Giữ.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **Kết hợp 2 shape**: (1) `optimize query` — *"bỏ whereDate(followed_at), đổi sang so sánh khoảng datetime sargable"*, *"đổi count>0→EXISTS và count=0→NOT EXISTS"*; (2) `sửa hàm dùng chung` — sửa builder `Conversation::advanceFilter`/`advanceFilterPost` mà **nhiều màn cùng gọi** |
| **Trigger space cần cover** | **Nhánh SQL bị rewrite**: ① ngày cố định — nhóm AND · ② ngày cố định — nhóm OR · ③ ngày theo số ngày — nhóm AND · ④ ngày theo số ngày — nhóm OR · ⑤ tag `có tag` (count>0 → EXISTS) · ⑥ tag `không tag` (count=0 → NOT EXISTS) · ⑦ tag `=N` (giữ nguyên — phải chứng minh KHÔNG đổi) · ⑧ tag `!=N` (giữ nguyên) |
| **Số trigger TCs hiện cover** | **7/8** — ①②⑤⑥⑦⑧ cover rõ (TC-FUNCDATE001-01/02, TC-REGSHARED001-03, TC-MSG001-01/02, TC-DATACOUNT001-03); ③ cover ở TC-FUNCDATE001-05; **④ (nhánh "theo số ngày" trong nhóm OR) KHÔNG có TC nào** → xem [MAJOR] M9 |
| **Quy mô test cho shape `optimize query`** | **CHƯA ĐẠT** — checklist yêu cầu *"test với quy mô khách hàng lớn nhất THỰC TẾ"*; TC-PERFLARGE001-01/03 để placeholder `<hỏi PM/DBA số liệu>` → chưa có con số → chưa chạy được. Rate limit API bên thứ 3: **N/A** (patch không gọi API ngoài) |
| **Danh sách nơi ảnh hưởng cho shape `shared code`** | **KHÔNG CÓ từ Dev** → **[BLOCKER] B1**. Mục 3 file 03 chỉ lặp lại 2 function **được sửa**, không list **caller**. Mục 4.3 nêu 3 tính năng, trong khi tiền lệ cùng builder (tab "Improve filter web", "improve filter ngày 13/11") test **8 màn** |
| **KH report dạng** | **Symptom-only** → **[MAJOR] M3**. Alert chỉ nói *"COUNT(*) process > 300s: Expect 0 - Result 1"* — tức "**có 1 process nào đó** chạy > 300s", **không chứng minh** process đó là query modal filter, cũng không chứng minh **chỉ có nó**. Việc quy về query filter đến từ 1 journal của Dev (*"cái này do query modal filter"*), không kèm snapshot `processlist` tại thời điểm alert (6/26 8:51 VNT) |
| **Alternative root causes cần verify** | ① slow query **khác** cùng gây alert tại 6/26 8:51 (chưa loại trừ) · ② bộ lọc `qr_code`/`conversion` — **cùng kiểu subquery đếm, Dev tự nhận còn tồn** (yokoten) → **vẫn có thể gây alert y hệt sau khi patch này lên** · ③ lock/contention từ job nền chứ không phải bản thân câu SELECT |
| **Anti-patterns dính** | **AP-2** (symptom-only) · **AP-4** (không có PR link để verify fix shape thực tế — chỉ có commit hash `d9807bde4e`) · **AP-6** (mục 3 không có caller thật). **Không dính** AP-1 (không phải generic catch), AP-3, AP-5 |

> ⚠️ **Điểm mấu chốt của cả review này**: alternative root cause ② nghĩa là **kể cả patch chạy đúng 100%, alert vẫn có thể tái phát** do `qr_code`/`conversion` chưa được fix. Cần Leader chốt với Dev: đóng ticket #38294 theo tiêu chí nào — "query tag+ngày không còn > 300s" hay "không còn process > 300s nào"?

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / AP-6 — GAP-1**: Mục 3 `03-dev-impact.md` ("Đã check và sửa các function **sử dụng đến** function/data vừa sửa") **không list caller nào** — chỉ lặp lại `advanceFilter` + `advanceFilterPost`, tức chính 2 function được sửa. Với fix shape `shared code`, `REG-SHARED-001` bắt buộc *"yêu cầu **dev cung cấp danh sách** nơi ảnh hưởng"*. Hệ quả: TC-REGSHARED001-01 đang phủ 8 màn dựa trên **suy luận từ sheet TC cũ**, không phải cam kết của Dev cho lần fix này — vừa có nguy cơ **thiếu** (màn mới phát sinh sau 2024 chưa ai biết), vừa có nguy cơ **thừa** (màn không còn dùng builder). — **Fix**: yêu cầu Dev trả lời bằng văn bản trên Redmine: (a) liệt kê **mọi caller** của `advanceFilter`/`advanceFilterPost` (grep toàn repo `sns-line`); (b) xác nhận rõ **phía job** (broadcast/scenario/callback) có gọi 2 hàm này không; (c) xác nhận 8 màn ở tiền lệ còn đúng không. Có danh sách rồi mới chốt phạm vi TC.
- **[BLOCKER] TC-FUNCDATE001-02 — precondition không dựng được**: TC yêu cầu F01 có `followed_at` = đúng `2026-06-01 00:00:00` và F04 = đúng `2026-06-30 23:59:59` ("set chính xác tới giây"), nhưng **`followed_at` sinh tự động khi LINE user kết bạn** — tester **không có cách nào** qua UI để tạo friend đúng giây đó. Theo [severity-levels.md](../../framework/severity-levels.md): *"TC phụ thuộc data/env không tồn tại trên môi trường test → không chạy được"* = Blocker. Nghiêm trọng vì **đây chính là TC verify giả định cốt lõi của patch** (`'23:59:59'` bao trọn ngày). — **Fix**: xin Dev/DBA **script seed** `followed_at` tới giây trên staging, ghi thẳng lệnh seed vào cột `Điều kiện tiền đề`; nếu không được cấp, ghi rõ "không verify được biên giây" và **escalate cho Leader quyết** — không được im lặng bỏ qua.
- **[BLOCKER] Baseline "môi trường chưa có patch" chưa được định nghĩa — GAP-2**: 6 TC (TC-DATACOUNT001-02, -03, TC-MSGUSER001-01, -02, TC-REGSHARED001-02, -03) có bước *"chạy trên môi trường chưa có patch → so sánh"*, nhưng **không TC nào nói môi trường đó là gì**. Sau khi branch `ai_fixbug_38294` merge lên staging thì baseline **biến mất** → 6 TC thành không chạy được. File 04 chỉ ghi *"member thống nhất với Dev"* — đó là việc chưa làm, không phải precondition. — **Fix**: chốt **trước khi deploy** 1 trong 2 phương án và ghi vào `Điều kiện tiền đề` của cả 6 TC: (a) giữ 1 env chạy nhánh gốc `release_step_20260623` để đối chiếu song song; **hoặc** (b) **chụp lại số đếm + danh sách friend của toàn bộ bộ filter trên staging TRƯỚC khi deploy** làm baseline tĩnh. Phương án (b) rẻ hơn nhưng **phải làm ngay, trước khi merge**.

### 4.2 Major (nên fix)

- **[MAJOR] M1 — File 01 auto-fill chưa được tester verify**: `01-bug-task.md` có `Auto-filled: 2026-07-16 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. Toàn bộ review này đứng trên input chưa ai kiểm chứng. — **Fix**: tester đọc lại Redmine #38294 (gồm **journal**, vì query gây lỗi nằm ở journal 2026-07-03 chứ không ở description) rồi tick.
- **[MAJOR] M2 — File 03 auto-fill chưa được tester verify**: tương tự, và **nặng hơn** vì `03-dev-impact.md` **không phải Dev viết tay** — nguồn là journal của user tự động "AI LME Fix bug". F/D/T ở mục 4.1/4.3 là do `/new-task` **map lại** từ báo cáo đó (4.1 gốc chỉ ghi "File thay đổi", F1/F2 là suy luận; 4.3 gốc **không ghi mức risk** nên đang để `<Redmine không ghi risk>`). — **Fix**: tester đối chiếu lại với Redmine, và **yêu cầu 1 Dev người thật xác nhận** báo cáo auto-fixbug trước khi dùng làm nguồn coverage.
- **[MAJOR] SYMPTOM-ONLY / AP-2 — M3**: xem §3.5. TCs hiện cover **1 root cause** (query filter tag+ngày). — **Fix**: hỏi Dev 2 câu: (a) có snapshot `SHOW FULL PROCESSLIST` / slow-query log tại **6/26 8:51 VNT** chứng minh process > 300s **chính là** query filter không? (b) ngoài query filter, còn slow query nào khác từng vượt 300s không? Bổ sung **TC-PERFLARGE001-04** (§5) để rà toàn hệ thống theo **RULE-04**.
- **[MAJOR] AP-4 — M4**: mục "Commit / Pull Request" chỉ có `commit d9807bde4e`, **không có link PR/diff**. Reviewer **không đọc được diff** → không verify được rewrite có thật sự tương đương không (VD: subquery `EXISTS` có giữ đủ scope `bot_id` không — đúng chỗ TC-PERM003-02 đang nghi). — **Fix**: yêu cầu Dev đính link PR/diff lên Redmine.
- **[MAJOR] M5 — không phân biệt được F1 vs F2**: Dev không nói màn nào gọi `advanceFilter`, màn nào gọi `advanceFilterPost` (chỉ nói *"màn gửi tin hàng loạt gọi advanceFilterPost"*). TC hiện gán F1/F2 theo **phỏng đoán tên hàm** → coverage F1/F2 ở §3 là **RISK, không phải OK**. — **Fix**: gộp vào câu hỏi của BLOCKER B1; sau khi có trả lời, chỉnh `Tiêu đề test case` cho đúng function.
- **[MAJOR] M6 — TC-REGSHARED001-01 không atomic**: 1 TC verify **8 màn** (vi phạm [review-checklist §B.2](../../framework/review-checklist.md)). Khi 1 trong 8 màn fail thì `Kết quả thực thi` ghi `Đạt` hay `Không đạt`? Evidence 8 ảnh trong 1 dòng cũng không truy vết được. — **Fix**: tách 8 TC (§5 đã viết sẵn 6 TC cho các màn ngoài 4.3; 2 màn `Màn friend list` + `send all` đã có TC riêng ở file 04).
- **[MAJOR] M7 — thiếu số liệu quy mô thật**: TC-PERFLARGE001-01/-03 ghi *"bot có quy mô friend lớn nhất thực tế (hỏi PM/DBA)"* — **chưa có con số**. `PERF-LARGE-001` yêu cầu *"hỏi/tra số liệu khách hàng lớn nhất hiện tại → tạo test data bằng hoặc lớn hơn"* và evidence phải *"ghi rõ nguồn"*. Không có số → TC không chạy được và không nghiệm thu được. — **Fix**: lấy số friend của bot lớn nhất trên production (query `COUNT` theo `bot_id`, hoặc hỏi DBA), điền vào `Dữ liệu test/input`. Ghi chú: bot trong evidence của Dev là **bot 542 trên dev DB** — quy mô đó **không đại diện** production.
- **[MAJOR] M8 — RULE-06/MSG-004 chưa đủ iOS + Android**: TC-MSG001-01 có ghi "(có iOS + Android trong nhóm này)" nhưng **TC-MSG001-02 và -03 không ghi** — trong khi TC-MSG001-02 mới là TC verify nhánh `NOT EXISTS` (nhánh rewrite). `MSG-004` yêu cầu evidence *"screenshot LINE app thật iOS VÀ Android"*. — **Fix**: bổ sung yêu cầu iOS + Android vào TC-MSG001-02/-03, hoặc thêm **TC-MSG001-04** (§5).
- **[MAJOR] M9 — thiếu trigger ④ (ngày "theo số ngày" trong nhóm OR)**: Dev ghi rõ rewrite áp cho *"cả nhóm điều kiện AND lẫn OR (ngày cố định + theo số ngày)"* = **4 tổ hợp**. TC-FUNCDATE001-05 chỉ test "theo số ngày" ở **nhóm AND**; TC-REGSHARED001-03 test AND/OR nhưng dùng **ngày cố định**. → tổ hợp **"theo số ngày × OR" không có TC**. — **Fix**: thêm 1 bước vào TC-FUNCDATE001-05 hoặc tách TC mới (§5 TC-FUNCDATE001-06).
- **[MAJOR] M10 — `Spec không ghi` nhưng chưa hỏi ai**: 12/35 TC ghi `Trạng thái đánh giá spec = Spec không ghi` kèm "Cần hỏi Leader/Dev", và file 04 tự thú nhận *"Chưa ai được hỏi thực tế"*. Theo quy tắc review: ghi `Spec không ghi` mà **không nêu đã hỏi ai** → MAJOR (nguy cơ tự suy diễn rồi cho `Đạt`). — **Fix**: member hỏi thật, rồi đổi sang `Đã hỏi leader` + ghi tên người trả lời + nội dung chốt. **Ưu tiên hỏi 3 câu**: biên `23:59:59` có đóng 2 đầu không · quy tắc friend block trong số đếm · `followed_at` của old friend (既存友だち取得) được set thế nào.
- **[MAJOR] M11 — 2 quan điểm Cao bị đánh × với lý do treo (RULE-03)**: `JOB-001` và `REG-RUN-001` đều × với lý do *"phụ thuộc câu trả lời của Dev"* — tức **lý do chưa thành lập**, đang treo chờ BLOCKER B1. RULE-03: × ở quan điểm Cao với lý do mơ hồ **phải có Leader approve**. — **Fix**: sau khi Dev trả lời B1, nếu job **có** dùng builder → nâng `JOB-001` + `REG-RUN-001` lên ◯ và bổ sung TC (§5 TC-JOB001-01). Nếu **không** → Leader ký duyệt lý do × vào §8.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC-ENV003-02**: `Kết quả mong đợi` = *"bảng đối chiếu ghi rõ chênh lệch quy mô"* — đó là **evidence**, không phải kết quả **đo lường được** ([review-checklist §B.1](../../framework/review-checklist.md)). — **Fix**: đổi thành giá trị cụ thể, VD "số đếm staging = số đếm production khi cùng bộ dữ liệu; thời gian production ≤ X giây".
- **[MINOR] TC-FUNCDATE001-03**: gộp 3 biên (xuyên năm + năm nhuận + cuối tháng 30 ngày) vào 1 TC với 3 bước độc lập → nếu bước 2 fail, `Kết quả thực thi` của cả TC mất ý nghĩa. — **Fix**: tách 3 TC, hoặc chấp nhận và ghi rõ ở `Ghi chú` cách chấm điểm từng bước.
- **[MINOR] Config sync chưa dùng được**: dòng `<!-- sync-tcs: ... | sheet=<⚠️ CHƯA XÁC ĐỊNH ...> -->` — URL trỏ tới Sheet **TC cũ**, chưa có tab đích cho TC mới. `/sync-ai-tc` và `/sync-review-tc` sẽ fail. — **Fix**: user tạo/chỉ định tab đích rồi điền `sheet=`.
- **[MINOR] §Thông tin file 04 chưa điền**: `Tester viết TCs` / `Ngày submit` còn placeholder → vi phạm [review-checklist §E](../../framework/review-checklist.md) *"Tester ký tên / version đã điền"*. — **Fix**: member ký tên khi submit.

### 4.4 Nit (gợi ý)

- **[NIT] `COMPAT-LEGACY-001` đánh × — Leader nên soi lại**: lý do ghi *"patch không chạm landing cũ/mới"* là hợp lý, nhưng tab "Bug filter OR" cho thấy filter **có** nhánh đời cũ/mới (`5. filter landing cũ` / `6. filter landing mới`) cùng nằm trong builder này. Nếu Dev xác nhận 2 nhánh landing dùng chung câu WHERE với điều kiện ngày → nên nâng ◯. Không block.
- **[NIT] TC-FUNC001-02 (xóa tag đang được filter tham chiếu)**: giá trị test tốt nhưng liên quan gián tiếp tới rewrite. Nếu cần cắt scope vòng 2, đây là TC hy sinh được — `MAP-TAG-05` đã có TC cũ cover.
- **[NIT] Đề xuất đóng vòng lặp RULE-10**: bug này **đã lọt ra production** (alert thật). Sau khi fix xong, cân nhắc thêm 1 dòng catalog ghi nhận *"builder filter dùng chung — mọi thay đổi phải rà đủ danh sách màn consumer"* để lần sau không phải đi tra sheet cũ như review này.

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` ở round tiếp theo. Tham chiếu data seed `S1` đã định nghĩa ở file 04.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERFLARGE001-04 | PERF-LARGE-001 | Abnormal | Rà TOÀN HỆ THỐNG sau deploy: không còn process > 300s nào KHÁC ngoài query filter | - **Production**, sau khi deploy `ai_fixbug_38294`<br>- Có quyền chạy query monitor trên DB production<br>- Chọn khung giờ cao điểm (đối chiếu giờ alert gốc **6/26 8:51 VNT**) | 1. Chạy query monitor của ticket **mỗi 5 phút trong 2 giờ** khung cao điểm:<br>`SELECT * FROM information_schema.processlist WHERE TIME > 300 AND db is not null AND command <> "Sleep" AND USER <> 'xtrabackup_lme' AND USER <> 'dump-analytics'`<br>2. Mỗi lần trả về > 0 dòng → **ghi lại nguyên văn câu SQL** của process đó<br>3. Phân loại: process đó là (a) query filter tag+ngày, (b) query filter `qr_code`/`conversion`, hay (c) query khác<br>4. Đối chiếu với kết quả chạy cùng cách **trước khi deploy** | Chu kỳ giám sát 2 giờ khung cao điểm | - **Không** process nào thuộc nhóm (a) query filter tag+ngày vượt 300s<br>- Nếu xuất hiện nhóm (b) hoặc (c) → **ghi ticket riêng**, KHÔNG đóng #38294 với kết luận "đã hết alert"<br>- Có bảng phân loại mọi process > 300s ghi nhận được trong 2 giờ | Chưa test | | **PRODUCTION** | | | | Spec ghi rõ | Lấp **GAP-3 / [MAJOR] M3 (AP-2 symptom-only)**. Áp **RULE-04** — *"phải có query/thống kê toàn hệ thống xác nhận phạm vi, không kết luận cảm tính"*. ⚠️ Đây là TC quyết định **tiêu chí đóng ticket**: alert gốc là "có process > 300s", không phải "query filter chậm". Evidence: bảng log processlist theo thời gian + câu SQL nguyên văn từng process |
| TC-FUNCDATE001-06 | FUNC-DATE-001 | Boundary | Nhánh ngày "theo SỐ NGÀY" trong nhóm điều kiện OR — tổ hợp thứ 4 chưa được cover | - Bot A, data seed `S1`<br>- Friend H01 `followed_at` = đúng **7 ngày trước**, H02 = **8 ngày trước** (cần script seed của Dev — xem BLOCKER B2)<br>- Baseline "trước fix" đã chốt (BLOCKER B3) | 1. Mở modal filter màn **send all**<br>2. Set nhóm **OR**: điều kiện 1 = ngày kết bạn kiểu **theo số ngày** `7 ngày gần đây`; điều kiện 2 = tag ĐK1 `Khách cũ`<br>3. Áp dụng → đọc số đếm + danh sách<br>4. Chạy đúng tổ hợp đó trên **baseline trước fix**<br>5. So sánh 2 kết quả | OR(ngày-theo-số-ngày = 7, tag ĐK1 = Khách cũ)<br>Phép tính tay: member tự lập từ `S1` + H01/H02 | - Kết quả **giống hệt** baseline trước fix<br>- H01 (đúng 7 ngày) **có** trong danh sách, H02 (8 ngày) **không**<br>- Friend chỉ thỏa tag `Khách cũ` (F03) vẫn có mặt — đúng ngữ nghĩa OR | Chưa test | | STAGING | | | | Spec không ghi | Lấp **[MAJOR] M9**. Dev ghi rewrite áp cho *"cả nhóm AND lẫn OR (ngày cố định + theo số ngày)"* = **4 tổ hợp**; file 04 mới cover 3. **Cần hỏi Dev** cách tính biên nhánh "theo số ngày". Evidence: screenshot 2 môi trường + `followed_at` của H01/H02 |
| TC-REGSHARED001-04 | REG-SHARED-001 | Normal | Màn `csv` (quản lý CSV): export theo filter tag + ngày → số dòng khớp modal | - Bot A, data seed `S1`<br>- ⚠️ Chỉ chạy **sau khi Dev xác nhận** màn này gọi `advanceFilter*` (BLOCKER B1) | 1. Vào màn **quản lý CSV**<br>2. Áp filter `Q1` (tag ĐK1 `VIP` + ngày kết bạn `2026-06-01`→`2026-06-30`)<br>3. Đọc số friend thỏa mãn hiển thị trên màn<br>4. Export file → mở file, đếm số dòng dữ liệu<br>5. Đối chiếu với số đếm ở màn Broadcast cùng filter | Filter `Q1`<br>Phép tính tay: **4** | - Số trên màn = **4**<br>- File CSV có **đúng 4 dòng** dữ liệu, đúng F01/F02/F04/F10<br>- Khớp số đếm của màn Broadcast | Chưa test | | STAGING | | | | Spec ghi rõ | Tách từ TC-REGSHARED001-01 — lấp **[MAJOR] M6**. Cover **T7 (csv)** — nằm ngoài mục 4.3 của Dev. Evidence: file CSV thật + screenshot màn. `regression` |
| TC-REGSHARED001-05 | REG-SHARED-001 | Normal | Màn `cross analysic`: filter tag + ngày → số liệu phân tích khớp modal | - Như TC-REGSHARED001-04 | 1. Vào màn **phân tích cross**<br>2. Áp filter `Q1`<br>3. Đọc số friend / số liệu trục tương ứng<br>4. Đối chiếu với số đếm màn Broadcast cùng filter | Filter `Q1`<br>Phép tính tay: **4** | - Số friend trong kết quả phân tích = **4**, khớp modal Broadcast<br>- Màn không lỗi / không loading vô hạn | Chưa test | | STAGING | | | | Spec ghi rõ | Tách từ TC-REGSHARED001-01. Cover **T8 (cross analysic)** — ngoài 4.3. Liên kết `DATA-COUNT-001` (số liệu phải khớp giữa các màn). Evidence: screenshot 2 màn. `regression` |
| TC-REGSHARED001-06 | REG-SHARED-001 | Normal | Màn `action schedule`: filter tag + ngày lưu và áp đúng | - Như TC-REGSHARED001-04 | 1. Vào màn **action schedule** → tạo/sửa 1 action có setting filter<br>2. Set filter `Q1`, lưu<br>3. Mở lại → xác nhận filter lưu đúng<br>4. Đọc số friend thỏa mãn (nếu màn có hiển thị) | Filter `Q1`<br>Phép tính tay: **4** | - Filter lưu đúng, mở lại không mất điều kiện<br>- Số friend thỏa mãn = **4** (nếu màn hiển thị)<br>- Không lỗi khi lưu | Chưa test | | STAGING | | | | Spec không ghi | Tách từ TC-REGSHARED001-01. Cover **T6 (action schedule)** — ngoài 4.3. **Cần hỏi Dev** màn này có hiển thị số đếm không. Evidence: screenshot. `regression` |
| TC-REGSHARED001-07 | REG-SHARED-001 | Normal | Màn `auto reply`: filter tag + ngày → đối tượng auto reply đúng | - Như TC-REGSHARED001-04 | 1. Vào màn **auto reply** → tạo/sửa 1 auto reply có setting filter<br>2. Set filter `Q1`, lưu<br>3. Đọc số friend thỏa mãn<br>4. Mở lại sau F5 → xác nhận filter giữ nguyên | Filter `Q1`<br>Phép tính tay: **4** | - Số friend thỏa mãn = **4**<br>- Filter giữ nguyên sau F5<br>- Khớp số của màn Broadcast | Chưa test | | STAGING | | | | Spec ghi rõ | Tách từ TC-REGSHARED001-01. Cover **T5 (auto reply)** — ngoài 4.3. Tab TC cũ "improve filter ngày 13/11" có khối `Màn auto_reply` để tham chiếu. Evidence: screenshot. `regression` |
| TC-REGSHARED001-08 | REG-SHARED-001 | Normal | Màn `scenario`: filter tag + ngày LƯU đúng vào DB (màn không hiện số đếm) | - Như TC-REGSHARED001-04 | 1. Vào màn **scenario** → tạo/sửa scenario có setting filter<br>2. Set filter `Q1`, lưu<br>3. Mở lại màn → xác nhận điều kiện filter hiển thị đúng như đã set<br>4. Kích hoạt scenario cho 1 friend thỏa mãn và 1 friend không thỏa mãn → xác nhận đúng đối tượng được add | Filter `Q1` | - Filter lưu và load lại **đúng nguyên vẹn**<br>- Chỉ friend thỏa mãn filter được add vào scenario<br>- Friend không thỏa mãn **không** bị add | Chưa test | | STAGING | | | | Spec không ghi | Tách từ TC-REGSHARED001-01. Cover **T4 (scenario)** — ngoài 4.3. ⚠️ Tab TC cũ "Improve filter web" ghi rõ: *"màn này không hiện số friend thỏa mãn filter, chỉ lưu filter vào db"* → **không verify được bằng số đếm**, phải verify qua đối tượng thực sự được add. Evidence: screenshot filter sau khi load lại + danh sách friend đã add. `regression` |
| TC-REGSHARED001-09 | REG-SHARED-001 | Normal | `modal action`: filter tag + ngày trong modal multi action → đúng đối tượng bị tác động | - Như TC-REGSHARED001-04<br>- Tag `ACT-38294` chưa gán cho ai | 1. Mở **modal action** (multi action) từ màn friend list<br>2. Set filter `Q1` trong modal<br>3. Chọn action = gắn tag `ACT-38294`<br>4. Thực thi<br>5. Lọc lại theo tag `ACT-38294`, đếm | Filter `Q1`<br>Phép tính tay: **4** | - **Đúng 4 friend** (F01/F02/F04/F10) bị tác động<br>- Số friend có tag `ACT-38294` = **4**, khớp 100% số đã lọc<br>- Không rơi về toàn bộ friend | Chưa test | | STAGING | | | | Spec ghi rõ | Tách từ TC-REGSHARED001-01. Cover **T9 (modal action)** — ngoài 4.3. Liên kết `BULK-001`, Catalog C `MAP-FI-03` (modal action là 1 trong 9 nơi hiển thị friend info). Evidence: danh sách 4 friend bị tác động. `regression` |
| TC-JOB001-01 | JOB-001 | Normal | Job broadcast THẬT chạy theo filter đã lưu → người nhận khớp số đếm lúc set | - **Production** (Catalog D `ENV-JOB`: production tách **3 job độc lập**)<br>- ⚠️ **Chỉ viết/chạy TC này nếu Dev xác nhận job gọi `advanceFilter*`** (BLOCKER B1)<br>- Nhóm tài khoản LINE test nội bộ | 1. Tạo broadcast **đặt lịch** (không gửi ngay) với filter tag + ngày kết bạn, chỉ nhắm nhóm test nội bộ<br>2. Ghi lại **số đếm tại thời điểm set lịch**<br>3. Chờ job chạy tới giờ<br>4. Đối chiếu: số đã gửi trong lịch sử vs số đếm lúc set vs người nhận thật trên LINE app<br>5. Theo dõi log job `broadcast` trong lúc chạy | Filter tag + ngày, gửi cho nhóm test nội bộ | - Số người nhận thật trên **LINE app** = số đếm lúc set lịch<br>- Log job `broadcast` không có lỗi SQL, không timeout<br>- Job không chạy quá 300s (query monitor = 0 trong lúc job chạy) | Chưa test | | **PRODUCTION** | | | | Spec không ghi | Lấp **GAP phía job** + **[MAJOR] M11**. `JOB-001` hiện bị đánh × với lý do treo. Tab TC cũ "Test bug KH" có khối `Check filter job` (broadcast/scenario/csv/cross/callback) → **bằng chứng filter CÓ chạy phía job**; nhưng tab "improve filter ngày 13/11" lại ghi *"phía job không sửa gì nên không cần check"* → **mâu thuẫn, Dev phải chốt**. RULE-08: job không kết luận từ staging. Evidence: log job + screenshot LINE app thật |
| TC-MSG001-04 | MSG-001 | Normal | Nhánh NOT EXISTS (tag ĐK3) — verify nhận tin trên CẢ iOS và Android | - Bot A, data seed `S1`<br>- F03 dùng **iPhone (iOS)**, F07 dùng **máy Android** (hoặc ngược lại — ghi rõ thiết bị thật) | 1. Tạo broadcast có emoji + xuống dòng, nội dung `Test #38294 NOT EXISTS ✅`<br>2. Set filter tag **ĐK3 (loại trừ)** = `VIP` + ngày kết bạn `2026-06-01`→`2026-06-30`<br>3. Xác nhận số đếm = 2 → gửi ngay<br>4. Mở LINE app **iOS** của F03 → chụp màn<br>5. Mở LINE app **Android** của F07 → chụp màn<br>6. So nội dung nhận được với preview ở màn admin | Phép tính tay: **2** (F03 iOS, F07 Android) | - **Cả 2 thiết bị** đều nhận đúng tin, đúng nội dung (emoji + xuống dòng không vỡ)<br>- Không thiết bị nào của F01/F02/F04/F10 nhận tin<br>- Nội dung khớp preview admin | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp **[MAJOR] M8**. `MSG-004` yêu cầu evidence **iOS VÀ Android**; TC-MSG001-02 ở file 04 chưa ghi thiết bị dù đó là TC verify nhánh rewrite `NOT EXISTS`. Evidence: screenshot LINE app iOS + Android (2 ảnh) + screenshot preview admin |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — chi tiết:
  - **Section**: ngữ nghĩa **điều kiện lọc "ngày kết bạn"** (Friend Filter / Segment — SC-003).
  - **Nội dung cần update**: spec hiện **không định nghĩa** biên của khoảng ngày. Sau patch này, hành vi thực tế là **biên đóng 2 đầu** (`ngày bắt đầu 00:00:00` ≤ x ≤ `ngày kết thúc 23:59:59`). Nguồn duy nhất đang ghi lại điều này là **TC cũ** (tab "improve filter ngày 13/11": *"setting 25/10/2023 - 1/11/2023 → hiển thị user kết bạn ngày 25/10 <= x <= 1/11"*) — tức **spec đang sống trong test case, không có trong tài liệu**. Cần đưa vào spec chính thức, kèm ghi chú ràng buộc kỹ thuật: **`followed_at` phải giữ kiểu DATETIME giây**; nếu đổi sang `datetime(6)` thì biên `23:59:59` sẽ **bỏ sót** các bản ghi trong khoảng `23:59:59.000001`–`23:59:59.999999` (chính Dev đã cảnh báo rủi ro này ở mục "Rủi ro / lưu ý khi test").
  - **Người chịu trách nhiệm update**: `<PM / Leader điền>`

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 ✓ · A.2 **RISK** (F1/F2 không phân biệt được) · A.3 ✓ · A.4 ✓ (T1-T3), **GAP** (T4-T9 + job) · A.5 ✓ (không orphan) · A.6 ✓ (xem §3.5)
- [x] B. Chất lượng từng TC — B.1 ✓ · **B.2 FAIL** (TC-REGSHARED001-01 gộp 8 màn) · B.3 ✓ · **B.4 FAIL** (seed `followed_at` tới giây + baseline không dựng được)
- [x] C. Chất lượng bộ TC tổng thể — tỷ lệ **Normal 12 / Abnormal 11 / Boundary 12** (34/31/34) — hợp lý với task nặng biên. Không trùng lặp. Phân bố quan điểm đều (11 quan điểm ◯, 3-5 TC/quan điểm). Multi-device: xem [MAJOR] M8. i18n: N/A (patch không chạm text)
- [x] D. Spec alignment — không mâu thuẫn spec; **cần update spec** → §6
- [x] E. Hành chính — **FAIL nhẹ**: tester chưa ký tên, chưa điền ngày submit ([MINOR])
- [x] F. Base quan điểm test LME (2 tầng)
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — **A** ✓ (DI-08/09/10 bê đủ 3 cột) · **B** N/A (patch không đổi UI) · **C** ✓ (MAP-SEND-01/20, MAP-TAG-01/03/05, MAP-PERM-01/03) · **D/D2** ✓ (ENV-JOB → có TC PRODUCTION) · **E** N/A (không chạm media)
  - [x] F.3 RULE — RULE-01 ✓ (REG-SHARED-001 thiếu Boundary **có ghi lý do**) · **RULE-02 ✓** · RULE-05 N/A · RULE-06 ✓ (có TC tới LINE app thật) — trừ [MAJOR] M8 · RULE-07 N/A (patch thuần SELECT, không CRUD) · **RULE-08 ✓** (6 TC ghi PRODUCTION) · RULE-09 ✓ (old friend) — xem [NIT] · **RULE-03 FAIL** → [MAJOR] M11 · **RULE-04 FAIL** → §5 TC-PERFLARGE001-04

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| FUNC-001 | Cao | ✓ luôn bắt buộc | TC-FUNC001-01/02/03 | **OK** |
| FUNC-003 | Cao (nâng — field ngày) | ✓ patch nối chuỗi ngày trực tiếp | TC-FUNC003-01/02/03 | **OK** — có test server-side (gọi thẳng API), đúng yêu cầu |
| FUNC-DATE-001 | Cao | ✓ patch đổi cách so sánh ngày | TC-FUNCDATE001-01→05 | **RISK** — thiếu tổ hợp "theo số ngày × OR" ([MAJOR] M9); TC-02 không dựng được env (BLOCKER B2) |
| DATA-COUNT-001 | Cao | ✓ màn có số đếm, patch sửa **chính** query đếm | TC-DATACOUNT001-01/02/03 | **OK** — có đối chiếu 4 nguồn + phép tính tay |
| MSG-001 | Cao | ✓ filter quyết định đối tượng gửi tin | TC-MSG001-01/02/03 | **RISK** — thiếu iOS+Android ở nhánh NOT EXISTS ([MAJOR] M8) |
| MSG-USER-001 | Cao | ✓ chạm friend LINE | TC-MSGUSER001-01/02/03 | **RISK** — phụ thuộc baseline chưa định nghĩa (BLOCKER B3) |
| BULK-001 | Cao | ✓ filter + thao tác hàng loạt | TC-BULK001-01/02/03 | **OK** |
| PERM-003 | Cao | ✓ tag/friend đa bot | TC-PERM003-01/02/03 | **OK** — TC-02 (EXISTS scope bot) là catch tốt |
| REG-SHARED-001 | Cao | ✓ **sửa builder dùng chung** | TC-REGSHARED001-01/02/03 | **RISK** → **BLOCKER B1** — không có danh sách caller từ Dev; TC-01 không atomic |
| PERF-LARGE-001 | Cao (nâng) | ✓ chính là mục tiêu fix | TC-PERFLARGE001-01/02/03 | **RISK** — thiếu số liệu quy mô ([MAJOR] M7); thiếu rà toàn hệ thống (§5) |
| ENV-003 | Cao | ✓ job nền + quy mô production | TC-ENV003-01/02/03 | **OK** — TC-03 (verify khi **chưa có** index) là catch tốt |
| **JOB-001** | Cao | **⚠️ CHƯA XÁC ĐỊNH** — phụ thuộc B1 | × với lý do treo | **RISK** → [MAJOR] M11 + §5 TC-JOB001-01 |
| **REG-RUN-001** | Cao | **⚠️ CHƯA XÁC ĐỊNH** — phụ thuộc B1 | × với lý do treo | **RISK** → [MAJOR] M11 |
| FUNC-002 / FUNC-004 / DATA-DB-001 / DATA-001 / DATA-REF-001 / MSG-003 / CONC-001 / MSG-002 / MSG-004 / MSG-005 / PAY-* / PERM-001 / PERM-002 / SEC-001 / STATE-* / DATA-MIG-001 / DATA-BACKUP-001 / DATA-AUDIT-001 / INTG-* / COMPAT-LEGACY-001 / DEPLOY-* / REG-SPEC-001 / REG-URL-001 / SEC-ISO-001 / ENV-001 / ENV-002 / MEDIA-* / FRIEND-001 / LIFF-ENTRY-001 / OUT-* / NOTI-MAIL-001 / UI-* / LIST-001 / CONC-002/003 / FUNC-SEQ-001 / FUNC-MULTI-001 / FUNC-DRAFT-001 / FUNC-UNIQ-001 / DATA-TEXT-001 / DATA-ID-001 / DATA-CACHE-001 / SYNC-APP-001 / PERM-004 | Cao→Thấp | ✗ | × có lý do cụ thể trong file 04 | **OK** — Leader đã soi lại, **lý do hợp lệ**. `DATA-DB-001` × đúng (patch thuần SELECT, mục 4.2 ghi rõ chỉ ĐỌC) → **không** phát sinh BLOCKER `WHERE` scope; rủi ro scope vẫn được cover ở `PERM-003`. Riêng `COMPAT-LEGACY-001` xem [NIT] |

> **Không dùng §4 checklist-lme** (FORM-01, CHAT-01, ADM-01/03/04, TPL-01 — RULE-11): đã kiểm, **không mục nào liên quan task này**, không flag.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

> **Việc Leader phải quyết trước vòng 2**:
> 1. Chốt **tiêu chí đóng ticket** — "query filter tag+ngày không còn > 300s" hay "không còn process > 300s nào" (liên quan `qr_code`/`conversion` chưa fix + §5 TC-PERFLARGE001-04).
> 2. Duyệt hoặc bác lý do × của `JOB-001` + `REG-RUN-001` (RULE-03), sau khi Dev trả lời BLOCKER B1.
> 3. Quyết phương án **baseline trước fix** (BLOCKER B3) — **phải quyết trước khi merge lên staging**, sau đó là quá muộn.
