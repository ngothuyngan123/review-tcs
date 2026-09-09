# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38301 — [Tạo auto reply] Lưu thông tin アクション稼働対象絞り込み(phạm vi người dùng không đúng) khi chọn đối tượng user block` |
| Reviewer (Leader) | `<Test Leader — verify draft này>` |
| Tester được review | `AI` (Studio job `#600`) — task tạo & chạy bởi `phapbt` |
| Ngày review | `2026-08-25` |
| Version TCs | `v1` (4 TC) + `v2` (3 TC: NEW-2, NEW-7, NEW-8) — toàn bộ `status = draft` |
| Vòng review | `Round 1` |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO task #200** (nguồn sự thật) — bổ sung `task_get_report` để lấy **lịch sử chạy**, `review_list_comments` (rỗng) |
| Ticket · task_id · round · branch | `38301` · `#200` · round `1` · `ai_fixbug_38301` |
| Thời điểm fetch | `2026-08-25` |
| Tổng số TC review | **7** |
| File 04 trong repo vs Studio | ✅ **Khớp** (7 vs 7 TC, cùng tập `temp_id` NEW-1/2/4/5/6/7/8) → **không** flag STALE-INPUT |
| `02-spec-reference.md` | **Không có** → fallback [spec-features/admin/auto-reply/feature-spec.md](../../spec-features/admin/auto-reply/feature-spec.md) (chi tiết hơn LME-SYSTEM-SPEC cho feature này) |

> ⚠️ **Report này thay thế phần nhận định ở §0 của `04-tc-list.md`.** File 04 được sinh từ `testcase_list` (chỉ có `last_exec`) nên kết luận "chưa có bằng chứng fix giải quyết bug". `task_get_report` cho thấy **có 2 lần chạy**, và bức tranh **đảo ngược** — xem §0.A.

### 0.A — Phát hiện quan trọng nhất: 2 lần chạy, 2 kết quả trái ngược

| Run | Env | Thời điểm | Kết quả | Diễn giải |
|---|---|---|---|---|
| **#473** | `local` | `2026-08-25 04:47 → 05:20` | run.counts: **pass 8 · fail 1** (9 kết quả); trong 7 TC hiện còn: **7/7 PASS** | Môi trường **CÓ** code fix. NEW-2 (tái hiện bug): *"Fix xác nhận: block=0 lưu & hiển thị đúng"* |
| **#478** | `dev` | `2026-08-25 07:14 → 07:47` | **pass 2 · fail 4 · error 1** | Môi trường **CHƯA CÓ** code fix |
| **#496** | `local` | — | **`queued`** — chưa từng chạy | Run treo trong hàng đợi |

**Triage do chính runner ghi lại ở run #478** (nguyên văn, rút gọn):

- TC 12639 (EP-11): *"A tạo mới: `is_apply_active_friend` **VẮNG MẶT** (expect 1) ✗ … **fix a chưa deploy**"*
- TC 12640 (EP-12): *"payload=0→id=21085, readback=1 (expect 0) ✗ … create bỏ qua `is_apply_active_friend`, DB áp default 1 (**fix b chưa deploy**)"*
- Bug #684 (Studio) `actual`: *"**Root cause: fix #38301 chưa được deploy lên môi trường dev**"*

⇒ **4 TC `fail` KHÔNG phải bug sản phẩm — là bug môi trường.** Đây **đúng y hệt** kịch bản đã làm tester fail oan ngày `2026-08-21` (commit vòng 1 mồ côi, môi trường chạy code cũ). **Lịch sử lặp lại lần 2.**

⇒ Nhưng **cũng không được kết luận "fix OK"** từ run #473: `local` là máy chạy pipeline, **không phải môi trường dùng chung**. Toàn bộ bộ TC hiện **chưa có 1 lượt chạy hợp lệ nào trên STAGING**.

**Kết luận về giá trị bằng chứng: bộ kết quả hiện tại KHÔNG dùng để nghiệm thu được — cả chiều Đạt lẫn chiều Không đạt.**

### 0.B — 6 cảnh báo bắt buộc từ metadata Studio

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật (`pass` mới là Đạt) | Run #478 (`dev`): **2/7 pass = 28.6%** · Run #473 (`local`): 7/7 pass nhưng env không hợp lệ | **`[BLOCKER]`** — < 50% trên lần chạy gần nhất, **và** cả 2 run đều không có giá trị nghiệm thu |
| 2 | TC `fail`/`error` + ticket bug | `fail`: NEW-2, NEW-6, NEW-7, NEW-8 · `error`: NEW-4 (lỗi hạ tầng `fetch failed`, **không phải bug sản phẩm**). **Không TC nào có `bug_tickets`**; Studio có bug **#684 (open, High)** gắn `tc_id = 12634` nhưng **`redmine_id = null`** | **`[BLOCKER]`** — bug chưa đẩy về Redmine; TC fail không trace được ticket ở tầng TC |
| 3 | Môi trường đã chạy | `PRODUCTION 0` · `STAGING 0` · `DEV 7` (run #478) · `LOCAL 7` (run #473). `env_tag`: `local-only` 6/7 | **`[BLOCKER]`** (test-validity, **không phải** RULE-08 — xem ghi chú dưới) |
| 4 | Ai chạy | **100% `last_exec.source = ai`**, `by = phapbt`. `manual.results = []` — **0 lượt chạy tay của người**. `exec_mode = auto` cho 7/7 | **`[BLOCKER]`** — nhóm rủi ro cao (gửi tin sai đối tượng, app mobile) không thể kết luận bằng runner tự động |
| 5 | Tác giả TC | **7/7 do AI sinh** (`author = AI`, `provenance.source = ai`, `createdJobId = 600`); `toolWritten`: tool 7 / mcp 0 / human 0. `reviewState = leader`, `reviewed = false` | **`[MAJOR]`** — 100% AI sinh + chưa review xong |
| 6 | Mã quan điểm không có trong `checklist-lme.md` | **2 mã / 3 lượt TC**: `TOOL-KNOW-002` (NEW-2), `API-001` (NEW-7, NEW-8). Ngoài ra `test_viewpoint_selection` còn nhắc `TOOL-OLDREC-001`, `STATE-MATRIX-001` — cũng không có | **`[MAJOR]`** — 3/7 TC không map được coverage; **không tính là cover** ở §3/§7 |

> **Ghi chú về mục 3 — không dùng RULE-08 để flag.** Task này **không** chạm media / domain / job nền / loadbalance / bill tiền ⇒ trigger của `ENV-003` **không khớp**, RULE-08 **không** bắt buộc chạy PRODUCTION. Vấn đề ở đây khác: **không có lượt chạy nào trên môi trường dùng chung có code fix**. `dev` = không có fix; `local` = máy pipeline. Yêu cầu tối thiểu là **STAGING có commit `f6ee800f86`**.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: **Không có TC nào verify đối tượng nhận tin thật** (bug này bản chất là auto-reply chạy **sai đối tượng**), **0 Abnormal / 0 Boundary** trên một fix chạm đường ghi dữ liệu — thiếu đúng case Dev đã cảnh báo (MySQL 1048), **không có TC cho kịch bản đổi payload API lúc deploy**, và **không có lượt chạy hợp lệ nào** trên môi trường dùng chung có code fix.

> 📌 **Luồng mobile (F3/F4/T2) đã được Leader descope khỏi vòng test này** — xem §4.0. Verdict `REJECTED` **không** đến từ phần mobile.

---

## 2. Tóm tắt cho member

Bộ TC bám rất sát diff và làm tốt 3 điểm: có **TC tái hiện đúng bug gốc**, có **đối chứng nhánh UPDATE/COPY** để bắt regression, và mọi TC đều verify **2 tầng UI + DB** với cách định danh bản ghi an toàn (dùng id trong response / marker duy nhất thay vì "id lớn nhất") — đây là chỗ nhiều người làm sai. Phần cần fix trong phạm vi web: toàn bộ 7 TC đều là `Normal`, chưa có case bất thường/biên nào — đặc biệt thiếu chính cái case mà Dev đã cảnh báo trong báo cáo (payload thiếu key → `NULL` vào cột `NOT NULL` → MySQL 1048); và chưa TC nào đi tới **kết quả cuối cùng người dùng thấy** là ai nhận được auto-reply.

**Luồng app mobile đã được Leader chốt là KHÔNG test ở vòng này** — member không cần viết TC cho phần đó, nhưng phải nắm rằng bản fix chốt **có sửa cả mobile** (2 file 4 dòng), nên đây là **rủi ro chấp nhận có chủ đích**, không phải phần bị bỏ quên (§4.0).

Điểm quan trọng nhất cần nắm: **4 TC `fail` trên `dev` không phải lỗi của bộ TC** — môi trường `dev` chưa có code fix, runner đã tự triage đúng. Đừng sửa TC theo hướng "nới expected cho pass"; việc cần làm là **chạy lại trên môi trường có commit `f6ee800f86`**.

---

## 3. Coverage Matrix

> Cột `Exec` = `<pass>/<số TC>` theo **run #478 (`dev`)** — lần chạy gần nhất; ngoặc là kết quả run #473 (`local`). Nhắc lại: **cả 2 run đều chưa đủ tư cách nghiệm thu** (§0.A).

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Exec (#478 / #473) | Status |
|---|---|---|---|---|---|---|
| **BUG** — nhánh CREATE không gán `is_apply_active_friend`; init default thiếu key | Fix | — | NEW-2 (tái hiện), NEW-6 (copy=create), NEW-8 (EP-12) | 3 | 0/3 (3/3) | **RISK** — có TC đúng trọng tâm nhưng **0 Abnormal/Boundary** + chưa có run hợp lệ |
| **F1** — `ReplyController::saveDataDetailAutoReply` nhánh CREATE (EP-12 web) | Function | **Direct** | NEW-1, NEW-2, NEW-6, NEW-8 | 4 | 1/4 (4/4) | **RISK** — chỉ Normal; thiếu case payload thiếu key / giá trị ngoài enum |
| **F2** — `ReplyController::initDataDetailAutoReply` mảng mặc định (EP-11 web) | Function | **Direct** | NEW-7 (dataset A) | 1 | 0/1 (1/1) | **RISK** — chỉ verify ở tầng API; **không có TC nào verify hệ quả UI** (radio preselect = REQ-002) |
| **F3** — `AutoreplyMobileController::saveAutoreply` nhánh CREATE (`/save-autoreply`) | Function | **Direct** | — | **0** | — | ⚪ **GAP — DESCOPED** (Leader duyệt, §4.0) |
| **F4** — `AutoreplyMobileController::initAutoreplyForm` mảng mặc định (`/init-autoreply-form`) | Function | **Direct** | — | **0** | — | ⚪ **GAP — DESCOPED** (Leader duyệt, §4.0) |
| **F5** — nhánh UPDATE `saveDataDetailAutoReply` (~L1017) / `saveAutoreply` (~L279) | Function | Indirect | NEW-4, NEW-5 | 2 | 1/2 (2/2) | **OK** — đủ vai trò regression cho phần web (NEW-4 lỗi hạ tầng, không phải lỗi TC) |
| **F6** — `initDataDetailAutoReply` gán từ `$dataReply` (edit/copy đọc DB) | Function | Indirect | NEW-7 (dataset B, C) | 1 | 0/1 (1/1) | **OK** — regression đủ cho phần web |
| **F7** — `TemplateRepository:1919` clone auto-reply sang bot mới | Function | Indirect — **CHƯA FIX** | — | **0** | — | 🔴 **GAP** (xem `[MAJOR]` §4.2 — Dev tự khai ngoài scope) |
| **F8** — `create.js` + `create_v2.blade.php` (Vue 2.6.12) | Function | Indirect | NEW-2 (bước 2 xác nhận trạng thái radio trước lưu) | 1 | 0/1 (1/1) | **RISK** — chỉ kiểm radio *sau khi user bấm*; **không kiểm trạng thái mặc định lúc mở màn** |
| **D1** — `auto_reply.is_apply_active_friend` (CREATE) | Data | — | NEW-1, NEW-2, NEW-5, NEW-6, NEW-8 | 5 | 2/5 (5/5) | **RISK** — chỉ 2 giá trị hợp lệ 0/1; **không có** null / thiếu key / ngoài enum; **không có** kiểm `WHERE` scope trên 2 tài khoản |
| **T1** — Auto Reply (FA-003) web — màn `自動応答（作成/編集）` | Feature | **High** | NEW-1, NEW-2, NEW-4, NEW-5, NEW-6 | 5 | 2/5 (5/5) | **RISK** — regression chỉ happy-path, precondition toàn state sạch (AP-3) |
| **T2** — Auto Reply (FA-003) **API mobile app Elme** | Feature | **High** | — | **0** | — | ⚪ **GAP — DESCOPED** (Leader duyệt, §4.0) |

### ORPHAN TCs

**Không có ORPHAN.** Cả 7 TC đều nằm trong scope `BUG / F* / D* / T*` của `03-dev-impact.md`.

> Lưu ý AP-5 (over-coverage): NEW-4, NEW-5, NEW-7 (dataset B/C) test **nhánh UPDATE / đọc DB — code không bị chạm**. Đây **không** phải over-coverage vì `saveDataDetailAutoReply` là hàm dùng chung CREATE/UPDATE ⇒ regression bắt buộc theo `REG-SHARED-001` + RULE-12. **Giữ nguyên**, không đề nghị remove.

### Đối chiếu requirement Studio → TC

| Requirement (Studio) | Risk | TC | Trạng thái |
|---|---|---|---|
| `REQ-001` Tạo mới lưu đúng đối tượng theo radio | **High** | NEW-1, NEW-2 | RISK (chỉ Normal) |
| `REQ-002` Màn tạo mới preselect `有効友だち` (fix a) | Medium | — | 🔴 **GAP** |
| `REQ-003` EP-11 trả default `= 1` khi tạo mới | Medium | NEW-7 | OK (tầng API) |
| `REQ-004` EP-12 nhánh CREATE ghi từ payload | **High** | NEW-8 | RISK (chỉ Normal) |
| `REQ-005` Regression EDIT | Medium | NEW-4, NEW-5 | OK |
| `REQ-006` Regression COPY | Medium | NEW-6 | OK |

> **Không có requirement nào cho luồng mobile** — `requirements` của Studio cũng dừng ở phạm vi web. Đây là **gốc rễ** của GAP F3/F4/T2: bộ requirement + `test_viewpoint_selection` được chốt theo **vòng fix 2** (câu mở đầu ghi nguyên văn *"1 file 2 dòng"*), trong khi bản chốt là **2 file 4 dòng** có mobile.
>
> ⚪ **Leader đã quyết định descope phần mobile khỏi vòng test này** (§4.0). Ghi nhận nguyên nhân gốc ở trên **vẫn giữ nguyên** để lần sau Studio sinh requirement theo đúng diff chốt, tránh lặp lại tình trạng bộ TC stale so với code.

> **Về con số `coverage.summary` của Studio (`0/29 covered · 25 none`)**: đây là độ phủ **toàn feature auto-reply** (BR-01…BR-15, EP-01…EP-12), **không phải** độ phủ scope fix. Các BR chưa phủ (BR-02 backup chặn ghi, BR-05 keyword trùng, BR-11 đổi bot giữa chừng…) **không** nằm trong diff và **không** có trong danh sách ảnh hưởng của Dev ⇒ theo RULE-12 **không** yêu cầu bổ sung trong vòng này. **Không dùng con số 0/29 để đánh giá bộ TC.**

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** | **(a) Shared-code / lặp pattern ở nhiều nơi** (chính) + **(b) Thêm field vào INSERT & default vào response init** — KHÔNG phải generic catch-all, KHÔNG phải race-condition, KHÔNG phải migration |
| **Trigger space cần cover** | Dev đã grep `AutoReply::create` toàn `app/` → **5 call site**: ① `ReplyController` create (web) ✅ đã fix · ② `AutoreplyMobileController` create (mobile) ✅ đã fix · ③ `TemplateRepository:1919` clone bot ❌ **chưa fix, ngoài scope** · ④ `AutoReplyRepository:146` đã có sẵn field · ⑤ `BotTutorialExpRepository:74` không liên quan. Cộng thêm **2 endpoint init** (web + mobile). |
| **Số trigger TCs hiện cover** | **2 / 5** — chỉ ① và (một phần) endpoint init web. ② mobile = **0 TC**. ③ clone bot = **0 TC**. |
| **KH report dạng** | ✅ **Có root cause cụ thể** — file 01 ghi rõ `[Test steps]` + `[Actual]` = `有効友だち` vs `[Expected]` = `ブロックした友だち`. Dev xác định root cause bằng đọc code + `git merge-base`, có số dòng cụ thể. **KHÔNG phải symptom-only** ⇒ không flag AP-2. |
| **Alternative root causes cần verify** | `N/A` — root cause đã được chứng minh ở tầng code, và run #473 (`local`, có fix) đã chứng minh fix giải quyết đúng triệu chứng. |
| **Anti-patterns dính** | **AP-3** (happy-path-only regression) — xem §4.2. AP-1/AP-2/AP-4/AP-5/AP-6 **không dính**. |

**Kết luận fix-shape**: đây là shape **`sửa hàm dùng chung / lặp pattern`** → theo `REG-SHARED-001` + [review-checklist.md §A.6](../../framework/review-checklist.md), yêu cầu bắt buộc là *"có danh sách nơi ảnh hưởng do DEV cung cấp **và** TC test **từng nơi** trong danh sách"*. **Dev ĐÃ cung cấp danh sách đầy đủ (5 call site) — nhưng TC chỉ phủ 2/5.**

Sau khi Leader descope mobile (§4.0), phần thiếu còn lại được phân loại:

| Call site | Trạng thái | Xử lý |
|---|---|---|
| ② `AutoreplyMobileController` create + init (mobile) | Đã fix, **0 TC** | ⚪ **DESCOPED** — rủi ro chấp nhận (§4.0) |
| ③ `TemplateRepository:1919` clone bot | **CHƯA fix**, 0 TC | 🟡 `[MAJOR]` GAP-6 — cần TC lấy bằng chứng raise ticket riêng |

⇒ Không còn `[BLOCKER] FIX-SHAPE`; hạ xuống **`[MAJOR]`** (mục GAP-6 §4.2). **Lưu ý**: coverage fix-shape thực tế của vòng này là **2/5 call site**, con số này nên được ghi vào biên bản nghiệm thu.

**Chi tiết AP-4 (không dính)**: mục "Commit / Pull Request" của `03-dev-impact.md` có `commit f6ee800f86` + branch `ai_fixbug_38301` + số dòng cụ thể ⇒ QA checkout và đọc diff được. Không cần flag.

---

## 4. Issues phát hiện

### 4.0 Rủi ro đã được Leader chấp nhận (descoped — KHÔNG chặn merge)

> Ghi theo **RULE-03**: quan điểm ưu tiên **Cao** bị đánh × bắt buộc có lý do + Leader duyệt. Mục này tồn tại để rủi ro được **chấp nhận công khai**, không phải bị bỏ quên.

**[DESCOPED] GAP-1 (F3, F4, T2, `SYNC-APP-001`) — Luồng mobile API không test ở vòng này.**

| Trường | Nội dung |
|---|---|
| Người quyết định | **Test Leader** — chốt ngày `2026-08-25` khi review round 1 |
| Phạm vi bỏ | `AutoreplyMobileController::saveAutoreply` (`/save-autoreply`) · `initAutoreplyForm` (`/init-autoreply-form`) · app Elme trên thiết bị thật |
| TC đã gỡ khỏi §5 | `TC-SYNCAPP001-01` · `TC-SYNCAPP001-02` · `TC-SYNCAPP001-03` |
| Quan điểm bị đánh × | `SYNC-APP-001` (ưu tiên **Cao**) |

**Rủi ro tồn đọng — Leader cần nắm khi ký nghiệm thu:**

1. Bản fix chốt `f6ee800f86` **CÓ sửa mobile** (2 file 4 dòng, `AutoreplyMobileController`). Code mobile **được release nhưng không được test** — không phải "không đụng tới nên không cần test".
2. Dev tự nêu rủi ro chưa ai verify: *"App mobile phía client cần đọc key `is_apply_active_friend` từ `/init-autoreply-form` để preselect radio; **nếu client hardcode default** thì vẫn hiển thị đúng vì server trả 1"* — mệnh đề "nếu" này **chưa được kiểm chứng**.
3. Mobile là **copy 1:1 của web** ⇒ nếu web phát hiện lỗi ở các TC còn lại, **mặc định phải giả định mobile cũng dính**, không được suy ra ngược lại rằng mobile an toàn.
4. Kịch bản **app bản cũ gọi server mới** (`COMPAT-LEGACY-001`) cũng theo đó không được test — cùng nhóm rủi ro với `[BLOCKER]` GAP-4 ở phía web.

**Đề nghị đi kèm quyết định descope** (Leader chọn 1):
- Raise **ticket test mobile riêng** cho `#38301`, đính 3 TC đã gỡ (còn lưu ở lịch sử git của file này), **hoặc**
- Ghi vào biên bản release rằng phần mobile của `#38301` **lên production không có bằng chứng test**, kèm phương án giám sát sau deploy.

### 4.1 Blocker (phải fix trước khi merge)

**[BLOCKER] ENV-1 — Không có lượt chạy hợp lệ nào: `dev` chưa deploy fix, `staging` chưa từng chạy.**
Run #478 chạy trên `dev` **không có code fix** (runner tự triage: *"fix a/b chưa deploy"*); run #473 pass 7/7 nhưng ở `local` — máy pipeline, không phải môi trường dùng chung. `STAGING = 0 run`, `PRODUCTION = 0 run`.
— **Fix**: deploy `ai_fixbug_38301` (commit `f6ee800f86`) lên **STAGING**, verify commit đang chạy đúng (`git log -1` hoặc endpoint version), rồi chạy lại toàn bộ 7 TC. **Chưa có kết quả STAGING thì không kết luận Đạt/Không đạt cho ticket này.** Đây là lần thứ **2** ticket fail vì lý do môi trường (lần 1: `2026-08-21`) — đề nghị thêm 1 bước "xác nhận commit trên môi trường" vào quy trình trước mọi run.

**[BLOCKER] GAP-2 (MSG-001, MSG-USER-001) — Không TC nào verify auto-reply chạy đúng ĐỐI TƯỢNG.**
Theo [feature-spec auto-reply **BR-19**](../../spec-features/admin/auto-reply/feature-spec.md): `is_apply_active_friend` quyết định **tập rule nào được nạp lúc runtime** (`conversation.isBlockedByBot()`). Vậy hệ quả thật của bug là **auto-reply chạy sai đối tượng theo 2 chiều**: (1) friend đã block **không** nhận rule dành cho họ; (2) **nguy hiểm hơn** — rule soạn cho người đã block **lại bắn cho friend đang hoạt động**. `MSG-001` (**Cao**) ghi rõ: *"Gửi nhầm đối tượng = lỗi nghiêm trọng nhất, luôn ưu tiên cao nhất"*, và bắt buộc *"xác nhận nhận thật trên LINE app"* (RULE-06). Cả 7 TC dừng ở **giá trị DB + radio màn admin**. Chính `test_viewpoint_selection` của Studio đã tự hạ cấp: *"MSG-USER-001 — verify **gián tiếp qua DB**, tầng job out-scope"* — vi phạm RULE-06.
— **Fix**: bổ sung `TC-MSG001-01`, `TC-MSGUSER001-01` (§5).
— ⚠️ **Giới hạn phạm vi có chủ đích (tránh AP-5)**: chỉ cần **2 TC smoke E2E** chứng minh giá trị đã lưu tạo ra đúng hành vi nhận tin. **KHÔNG** yêu cầu dựng ma trận test cho `HandlePostbackTask` / Spring Boot — layer đó **không bị chạm code**.

**[BLOCKER] GAP-3 (FUNC-002, FUNC-003, RULE-01) — 0 Abnormal, 0 Boundary trên toàn bộ 7 TC.**
`REQ-001` và `REQ-004` là risk **High**; `FUNC-001`/`FUNC-002`/`FUNC-004` đều ưu tiên **Cao** ⇒ RULE-01 đòi tối thiểu Normal + Abnormal + Boundary, **không TC nào ghi lý do miễn trừ**. Nghiêm trọng nhất: **case mà chính Dev đã cảnh báo trong báo cáo lại không được test** — payload **thiếu key** `is_apply_active_friend` → `NULL` vào cột `NOT NULL` → **MySQL 1048, lưu thất bại** (Dev xác nhận `config/database.php strict=false` **không** tự chuyển 0). Đây là lý do tồn tại của fix (b), và nó **hoàn toàn không có TC**.
— **Fix**: bổ sung `TC-FUNC002-01`, `TC-FUNC003-01`, `TC-FUNC004-01` (§5).

**[BLOCKER] GAP-4 (DEPLOY-LIVE-001, Cao) — Fix đổi payload API nhưng không có TC cho client cũ gọi server mới.**
Fix (b) **thêm key vào response của endpoint init** (EP-11 web + `/init-autoreply-form` mobile). `DEPLOY-LIVE-001` trigger: *"release lên production không bật maintain, **đặc biệt khi đổi payload API / field form / cấu trúc request**"*. Kịch bản thật, xác suất cao: admin **mở sẵn màn tạo auto reply trước lúc deploy** (model Vue nạp payload **cũ**, không có key) → sau deploy **không reload**, chọn `ブロックした友だち`, bấm `登録` → payload gửi lên thiếu key → theo phân tích của chính Dev sẽ **lỗi 1048**. Không TC nào cover.
— **Fix**: bổ sung `TC-DEPLOYLIVE001-01` (§5).

**[BLOCKER] EXEC-1 — 4 TC `fail` không có `bug_tickets`; bug Studio #684 chưa đẩy về Redmine.**
Studio raise bug **#684** (`open`, severity `High`, `tc_id = 12634`) nhưng **`redmine_id = null`** ⇒ trên Redmine #38301 **không có** comment nào báo kết quả test fail; ticket vẫn treo `Fix done - Đợi test`. Ở tầng TC, cả 4 TC `fail` (NEW-2/6/7/8) đều `bug_tickets = []` ⇒ không trace được.
— **Fix**: (1) **KHÔNG** đẩy #684 sang Redmine như bug sản phẩm — nội dung `actual` của chính nó đã kết luận *"fix chưa được deploy lên môi trường dev"*; đổi thành **issue môi trường** hoặc đóng sau khi chạy lại trên STAGING. (2) Sau run STAGING, gắn `bug_tickets` cho từng TC còn fail.

**[BLOCKER] EXEC-2 — 0 lượt chạy tay; 100% kết quả do runner tự động.**
`manual.results = []`, `exec_mode = auto` cho 7/7, `last_exec.source = ai` cho 7/7. Hạng mục ở GAP-2 (nhận tin thật trên LINE app iOS/Android) **về bản chất không thể** kết luận bằng runner — cần thiết bị thật + tài khoản LINE thật (RULE-06). GAP-4 (submit qua thời điểm deploy) cũng phải chạy tay.
— **Fix**: các TC bổ sung ở §5 phải để `exec_mode = manual`, phân công QA người chạy.

### 4.2 Major (nên fix)

**[MAJOR] INPUT-1 — Checkbox "Tester verify auto-fill chính xác" ở CẢ `01-bug-task.md` và `03-dev-impact.md` chưa tick.**
Cả 2 file đều có `Auto-filled: 2026-08-25 by /new-task`. Chưa ai verify ⇒ F/D/T có thể thiếu hoặc map sai, và toàn bộ coverage matrix §3 dựa trên đó. Yêu cầu tester đọc lại Redmine #38301 (đặc biệt **3 journal Auto-fixbug** — nội dung khác nhau giữa 3 vòng) rồi tick.

**[MAJOR] AP-3 — Regression chỉ happy-path, precondition toàn state sạch.**
`T1` có 5 TC nhưng precondition đều là bản ghi mới dựng, dữ liệu sạch. Không TC nào chạy regression ở **edge state**: bản ghi tạo **trước fix** (đang lưu sai `= 1`), bản ghi có action đã bị xóa, folder `未分類`, bot vừa đổi. `T2` thì không có TC nào.
— **Fix**: `TC-COMPATLEGACY001-01` (§5) + mở rộng precondition của NEW-4/NEW-6.

**[MAJOR] GAP-5 (REQ-002, UI-FIELD-001) — Không TC nào verify radio preselect ở màn tạo mới.**
`REQ-002` (risk Medium) là **hệ quả UI trực tiếp của fix (b)** — trước fix **không radio nào được chọn sẵn**, sau fix `有効友だち` phải preselect. NEW-7 chỉ verify ở **tầng API** (`data_reply.is_apply_active_friend = 1`), **không** verify UI thật sự render đúng — mà chính `create.js:56` (`self.data_reply = a.data_reply`) là mắt xích Dev nói gây mất key.
— **Fix**: `TC-UIFIELD001-01` (§5).

**[MAJOR] GAP-6 (REG-SHARED-001) — `TemplateRepository:1919` (clone auto-reply sang bot mới) cùng pattern lỗi, chưa fix, không TC.**
Dev tự khai 2 lần trong báo cáo: *"Clone auto-reply sang bot mới (`TemplateRepository:1919`) vẫn chưa copy `is_apply_active_friend` — ngoài scope ticket, cần ticket riêng."* Chấp nhận ngoài scope fix, **nhưng không được để trống bằng chứng**: cần 1 TC ghi nhận hành vi hiện tại (dự kiến FAIL) để làm căn cứ raise ticket riêng.
— **Fix**: `TC-REGSHARED001-04` (§5) + Leader raise ticket Redmine riêng.

**[MAJOR] GAP-7 (DATA-DB-001, PERM-003) — Không TC kiểm scope trên 2 tài khoản.**
Fix ghi thêm 1 field vào `INSERT` trong hàm dùng chung cho nhiều bot. Không TC nào tạo bản ghi **trùng tên trên 2 bot** rồi xác nhận không ghi chéo.
— **Ghi chú deviation**: [.claude/commands/review-tc.md](../../.claude/commands/review-tc.md) quy định *"task có UPDATE/DELETE mà không có TC kiểm `WHERE` scope trên 2 tài khoản → `[BLOCKER]`"*. Tôi hạ xuống **`[MAJOR]`** vì diff **chỉ thêm 1 khóa vào mảng `INSERT`**, **không chạm mệnh đề `WHERE`** nào — áp BLOCKER ở đây là over-coverage (AP-5). **Leader có quyền nâng lại BLOCKER** nếu muốn giữ nguyên tắc cứng.
— **Fix**: `TC-DATADB001-01` (§5).

**[MAJOR] NEW-1 — Kết quả `pass` được ghi nhận dù runner KHÔNG chạy đúng steps của TC.**
Steps bước 3 của NEW-1 ghi *"Chọn 1 action hợp lệ ở nhóm 「アクション設定」…"*, nhưng `actual` của run #478 ghi: *"bước chọn action để trống — FE create_v2 KHÔNG bắt buộc action để lưu (đã xác minh save hợp lệ với `action_id=null`)"*. TC và lượt thực thi **lệch nhau**, nhưng vẫn tick `pass`. Vi phạm nguyên tắc bằng chứng (RULE-02): kết quả phải chứng minh **đúng cái TC mô tả**.
— **Fix**: sửa TC trên Studio (`testcase_update`) cho khớp thực tế (action là optional), **hoặc** chạy lại đúng steps. Không để lệch.

**[MAJOR] EXEC-3 — Số liệu run #473 không khớp số kết quả lưu trữ (nghi có TC bị xóa sau khi FAIL).**
`run #473.counts` = `pass 8 · fail 1` (**9 kết quả**), nhưng chỉ **7 kết quả** của run #473 còn tồn tại và **cả 7 đều `pass`**. ⇒ **2 kết quả đã biến mất, trong đó có kết quả `fail` duy nhất của run đó.** Khớp với việc dãy `temp_id` thiếu hẳn **`NEW-3`** (dãy còn lại: NEW-1, 2, 4, 5, 6, 7, 8).
— **Fix**: Leader yêu cầu Studio giải trình — TC `NEW-3` là gì, ai xóa, xóa lúc nào, **có phải TC đã FAIL ở run #473 không**. Nếu đúng thì đây là **xóa bằng chứng lỗi**, phải khôi phục. Dùng `testcase_get_history` / `task_get_history`.

**[MAJOR] DEV-IMPACT-1 — Mục 7 của `03-dev-impact.md` khẳng định SAI rằng luồng COPY không bị ảnh hưởng.**
Nguyên văn Dev: *"không đổi luồng edit/copy (2 luồng này vốn trả `is_apply_active_friend` từ DB)"*. Nhận định này chỉ đúng cho **đường ĐỌC** (EP-11). Đường **GHI** của copy đi qua **đúng nhánh CREATE** đang bị lỗi — bằng chứng: run #478 TC 12638 ghi *"copy id=21083 … readback=1. SAI … **Bug #38301 (nhánh copy=create)**"*.
— **Fix**: Leader yêu cầu Dev đính chính mục 7; COPY phải được liệt kê là **ảnh hưởng Direct**, không phải "không đổi". Ảnh hưởng tới `DATA-REF-001` (Cao — tính độc lập của bản sao).

### 4.3 Minor (có thể fix sau)

**[MINOR] TC-No. / mã quan điểm** — 3/7 TC dùng mã **không tồn tại** trong [checklist-lme.md](../../framework/checklist-lme.md): `TOOL-KNOW-002` (NEW-2), `API-001` (NEW-7, NEW-8) ⇒ `/review-tc` không map coverage được, và theo mục 0.B #6 **không tính là cover**. Đề xuất ánh xạ lại: `TOOL-KNOW-002` → **`OUT-TRUTH-001`** (UI/message khớp trạng thái thật — đúng bản chất bug lõi); `API-001` → **`FUNC-001`** + ghi `endpoint` ở `Ghi chú`. Nếu team muốn giữ mã nội bộ Studio → bổ sung bảng ánh xạ chính thức vào `framework/checklist-lme.md`.

**[MINOR] Cột `Trạng thái đánh giá spec` trống toàn bộ 7 TC** (`spec_status = null`) dù cả 7 đều `spec_change = 1`. Phải điền `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. Riêng `REQ-002` (default `有効友だち`) hiện đang **suy từ default cột DB**, không có spec — phải ghi `Spec không ghi` + nêu rõ đã hỏi ai (xem §6).

**[MINOR] Cột `Evidence thực tế` trống + `Ghi chú` không ghi LOẠI evidence bắt buộc** (RULE-02). Studio có artifact thật cho 3 TC (`tc-12634-fail.png`, `.webm`, `trace.zip`) nhưng không đồng bộ về file 04.

**[MINOR] Evidence của bug Studio #684 trỏ sai đường dẫn**: `[{"name":"TC 12638","path":"478/tc-12634/tc-12638-fail.png"}]` — file `tc-12638` nằm trong thư mục `tc-12634`. Đường dẫn đúng phải là `478/tc-12638/tc-12638-fail.png`. Ảnh hưởng khả năng truy vết bằng chứng.

**[MINOR] Run #496 (`local`) kẹt trạng thái `queued`** — chưa từng chạy. Dọn hoặc chạy lại để tránh nhiễu số liệu.

### 4.4 Nit (gợi ý)

**[NIT]** NEW-2 precondition ghi *"bot 'oppo' theo precondition report — nếu môi trường test không có bot này thì dùng bot tương đương và ghi rõ"*. Chính TC tự nhận *"chưa xuất hiện trong info-pack"*. Nên chốt hẳn 1 bot test cố định cho ticket này để 2 người chạy ra cùng kết quả.

**[NIT]** NEW-7 gộp 3 dataset (A/B/C) trong 1 TC → khi fail chỉ biết "TC fail", phải đọc `actual` mới biết dataset nào. Cân nhắc tách 3 TC atomic (B.2).

**[NIT]** Có thể bổ sung TC cho `BR-11` (đổi bot giữa chừng → từ chối lưu) và `BR-02` (bot đang backup → chặn ghi) vì cùng nằm trong `saveDataDetailAutoReply`. **Không bắt buộc vòng này** — không nằm trong diff và không có trong danh sách ảnh hưởng của Dev (RULE-12).

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` round tiếp theo. **10 TC** lấp 7 GAP ở §4.
> *(3 TC mobile `TC-SYNCAPP001-01/02/03` đã gỡ theo quyết định descope ở §4.0 — vẫn còn trong lịch sử git của file này nếu cần khôi phục.)*

> ✅ **Đã push lên LME TEST STUDIO task #200 ngày `2026-08-25`** (`testcase_create`, `provenance = mcp`, `status = draft`, `exec = untested`). Bảng trace ngược:
>
> | TC No. (report) | Studio `id` | `temp_id` | `client_ref` |
> |---|---|---|---|
> | TC-MSG001-01 | `13531` | NEW-9 | `REV38301-TC-MSG001-01` |
> | TC-MSGUSER001-01 | `13532` | NEW-10 | `REV38301-TC-MSGUSER001-01` |
> | TC-FUNC002-01 | `13533` | NEW-11 | `REV38301-TC-FUNC002-01` |
> | TC-FUNC003-01 | `13534` | NEW-12 | `REV38301-TC-FUNC003-01` |
> | TC-FUNC004-01 | `13535` | NEW-13 | `REV38301-TC-FUNC004-01` |
> | TC-DEPLOYLIVE001-01 | `13536` | NEW-14 | `REV38301-TC-DEPLOYLIVE001-01` |
> | TC-UIFIELD001-01 | `13537` | NEW-15 | `REV38301-TC-UIFIELD001-01` |
> | TC-COMPATLEGACY001-01 | `13538` | NEW-16 | `REV38301-TC-COMPATLEGACY001-01` |
> | TC-DATADB001-01 | `13539` | NEW-17 | `REV38301-TC-DATADB001-01` |
> | TC-REGSHARED001-04 | `13540` | NEW-18 | `REV38301-TC-REGSHARED001-04` |
>
> `client_ref` là khoá idempotent — push lại cùng `client_ref` sẽ **reuse**, không tạo trùng. Studio đã tự map spec: `BR-19` ← 13531/13532 · `EP-11` ← 13536/13537 · `EP-12` ← 13533/13534/13535/13536/13539 · `SCR-AR-02` ← 13533/13536/13537/13538.
> Toàn bộ `exec_mode` nên đặt **`manual`** (cần thiết bị thật / thao tác deploy / LINE app thật) — trừ `TC-FUNC003-01`, `TC-FUNC004-01` có thể auto.
> Môi trường mặc định **STAGING** (đã deploy commit `f6ee800f86`). Task **không** chạm media/domain/job/bill tiền nên RULE-08 không bắt buộc PRODUCTION.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-MSG001-01 | MSG-001 | Normal | Auto reply đối tượng ブロック chỉ chạy cho friend đã block, KHÔNG bắn cho friend đang hoạt động | - 1 bot test trên STAGING đã deploy `f6ee800f86`<br>- 2 tài khoản LINE thật: **A đã block** OA, **B đang là bạn bình thường**<br>- Đã tạo auto reply R1: đối tượng `ブロックした友だち`, từ khóa `TC38301BLOCK`, nội dung trả lời `REPLY-BLOCK`<br>- Đã tạo auto reply R2: đối tượng `有効友だち`, cùng từ khóa `TC38301BLOCK`, nội dung `REPLY-ACTIVE` | 1. Từ tài khoản LINE **B (đang hoạt động)** gửi cho OA tin nhắn `TC38301BLOCK`. Quan sát tin nhận được trên LINE app.<br>2. Từ tài khoản LINE **A (đã block)** gỡ block tạm thời? **KHÔNG** — giữ nguyên trạng thái block, gửi tin `TC38301BLOCK` cho OA. Quan sát tin nhận được.<br>3. Mở màn chat 1:1 trên admin, đối chiếu lịch sử trả lời tự động của từng người.<br>4. Chụp màn hình LINE app của **cả A và B**. | Từ khóa `TC38301BLOCK` · R1 = block/`REPLY-BLOCK` · R2 = active/`REPLY-ACTIVE` | - Tài khoản **B (hoạt động)** nhận **đúng `REPLY-ACTIVE`**, **KHÔNG** nhận `REPLY-BLOCK`.<br>- Tài khoản **A (đã block)** nhận **đúng `REPLY-BLOCK`** (hoặc đúng hành vi spec cho user block), **KHÔNG** nhận `REPLY-ACTIVE`.<br>- Không có trường hợp 1 người nhận cả 2 tin. | Chưa test |  | STAGING |  |  |  | Spec ghi rõ | **Lấp GAP-2** — đây là **output cuối chuỗi** của bug (RULE-06). Spec: `BR-19` trong [feature-spec auto-reply](../../spec-features/admin/auto-reply/feature-spec.md). Evidence: **screenshot LINE app thật của cả 2 tài khoản**. ⚠️ Chỉ smoke E2E — **không** mở rộng test routing của Spring Boot (layer không bị chạm, tránh AP-5). |
| TC-MSGUSER001-01 | MSG-USER-001 | Normal | Friend block rồi unblock nhận đúng auto reply của tập rule mới | - Như TC-MSG001-01 (R1 block, R2 active, cùng từ khóa)<br>- Tài khoản LINE A đang ở trạng thái **đã block** OA | 1. Ở trạng thái đang block, tài khoản A gửi `TC38301BLOCK` → ghi nhận tin nhận được.<br>2. Tài khoản A **gỡ block** OA (unblock), đợi hệ thống cập nhật trạng thái bạn bè.<br>3. Tài khoản A gửi lại `TC38301BLOCK` → ghi nhận tin nhận được.<br>4. Đối chiếu 2 lần nhận ở bước 1 và bước 3. | Cùng 1 tài khoản LINE, 2 trạng thái block → unblock | - Lần 1 (đang block): nhận `REPLY-BLOCK`.<br>- Lần 2 (sau unblock): nhận `REPLY-ACTIVE`, **không** còn nhận `REPLY-BLOCK`.<br>- Chuyển trạng thái có hiệu lực ngay ở lần gửi kế tiếp, không cần thao tác thêm trên admin. | Chưa test |  | STAGING |  |  |  | Spec ghi rõ | **Lấp GAP-2** — lifecycle block/unblock (`MSG-USER-001` ưu tiên **Cao**). Evidence: **screenshot LINE app 2 thời điểm**. |
| TC-FUNC002-01 | FUNC-002 | Abnormal | Lưu auto reply tạo mới khi màn hình không gửi lên lựa chọn đối tượng phải báo lỗi rõ, không lưu nửa vời | - Đăng nhập admin STAGING đã deploy `f6ee800f86`, đã chọn bot test<br>- Mở DevTools tab Network để chặn/sửa request trước khi gửi | 1. Mở màn tạo auto reply mới, điền các trường bắt buộc.<br>2. Dùng DevTools chặn request lưu và **xoá trường lựa chọn đối tượng** khỏi dữ liệu gửi lên (mô phỏng màn cũ / client cũ không gửi trường này).<br>3. Cho request đi tiếp, quan sát màn hình.<br>4. Mở lại danh sách auto reply, tìm theo tên vừa đặt.<br>5. Nếu bản ghi có được tạo, mở ra xem đối tượng đang hiển thị là gì. | Tên auto reply `TC38301-NOKEY-01`; dữ liệu gửi lên **thiếu hẳn** trường lựa chọn đối tượng | - Màn hình **báo lỗi rõ ràng bằng tiếng Nhật cho người dùng** — không phải lỗi hệ thống thô (`SQLSTATE`, `1048`, trang 500 trắng).<br>- **Không** hiển thị thông báo "lưu thành công" giả.<br>- Danh sách **không** xuất hiện bản ghi rác nửa vời; nếu có tạo thì phải mang giá trị mặc định hợp lệ và mở ra được bình thường. | Chưa test |  | STAGING |  |  |  | Spec không ghi | **Lấp GAP-3** — chính là case Dev cảnh báo: thiếu key → `NULL` vào cột `NOT NULL` → **MySQL 1048**. Liên kết `OUT-TRUTH-001`, `UI-003` (chống false success). Evidence: **screenshot màn báo lỗi + screenshot danh sách sau thao tác**. |
| TC-FUNC003-01 | FUNC-003 | Abnormal | Gọi thẳng API lưu auto reply với giá trị đối tượng ngoài quy định phải bị từ chối | - Có phiên đăng nhập admin hợp lệ trên STAGING đã deploy `f6ee800f86`<br>- Bot test không ở trạng thái đang sao chép dữ liệu | 1. Gọi thẳng endpoint lưu auto reply (nhánh tạo mới) với giá trị đối tượng = `2`.<br>2. Ghi nhận phản hồi trả về.<br>3. Lặp lại với giá trị `-1`, chuỗi rỗng `""`, và chuỗi chữ `"abc"`.<br>4. Sau mỗi lần, mở màn danh sách auto reply trên trình duyệt kiểm tra có bản ghi rác nào được tạo không.<br>5. Với bản ghi (nếu có), mở màn sửa xem radio hiển thị ra sao. | Giá trị đối tượng: `2`, `-1`, `""`, `"abc"` — mỗi lần 1 giá trị, tên bản ghi duy nhất theo giá trị | - Cả 4 giá trị đều bị **từ chối** với thông báo lỗi nghiệp vụ rõ ràng, **không** tạo bản ghi.<br>- Nếu hệ thống chấp nhận (hiện chưa validate) → ghi nhận là **phát hiện mới**, báo Leader: bản ghi mở màn sửa sẽ **không radio nào được chọn**, và tập rule chạy lúc runtime không xác định. | Chưa test |  | STAGING |  |  |  | Spec không ghi | **Lấp GAP-3** — validate **server-side**, không chỉ dựa radio ở giao diện (`FUNC-003`: *"frontend chặn được nhưng gọi thẳng API vẫn lưu được = lỗi kinh điển"*). `exec_mode` có thể `auto`. Evidence: **request/response từng giá trị + screenshot danh sách**. |
| TC-FUNC004-01 | FUNC-004 | Boundary | Chỉ đúng 2 giá trị 0 và 1 được chấp nhận cho đối tượng アクション稼働対象絞り込み | - Như TC-FUNC003-01 | 1. Gọi endpoint lưu auto reply tạo mới với giá trị đối tượng = `0` → mở lại bản ghi trên màn sửa.<br>2. Lặp lại với `1` → mở lại bản ghi.<br>3. Lặp lại với `2` (biên trên +1) và `-1` (biên dưới −1).<br>4. Với mỗi lần, đối chiếu giá trị hiển thị trên màn sửa với giá trị đã gửi. | 5 pattern biên: `0` (biên dưới hợp lệ) · `1` (biên trên hợp lệ) · `2` (biên+1) · `-1` (biên−1) · bỏ trống | - `0` → lưu và hiển thị `ブロックした友だち`.<br>- `1` → lưu và hiển thị `有効友だち`.<br>- `2`, `-1`, bỏ trống → **bị từ chối**, không tạo bản ghi.<br>- Nguồn giới hạn: cột `is_apply_active_friend` kiểu số nguyên nhỏ, `NOT NULL`, mặc định `1` (migration `2023_01_05_160920`). | Chưa test |  | STAGING |  |  |  | Spec không ghi | **Lấp GAP-3** — RULE-01 yêu cầu loại `Boundary` cho quan điểm ưu tiên **Cao**. `exec_mode` có thể `auto`. Evidence: **bảng 5 pattern + kết quả từng pattern**. |
| TC-DEPLOYLIVE001-01 | DEPLOY-LIVE-001 | Abnormal | Màn tạo auto reply mở TRƯỚC khi deploy, submit SAU deploy không lỗi hệ thống và không lưu sai | - STAGING đang chạy bản **CHƯA** có fix<br>- Có quyền deploy `ai_fixbug_38301` (`f6ee800f86`) lên STAGING trong lúc test<br>- Đăng nhập admin, đã chọn bot test | 1. Mở màn tạo auto reply mới, điền đầy đủ trường bắt buộc, chọn `ブロックした友だち`. **Dừng lại, KHÔNG bấm đăng ký, KHÔNG reload.**<br>2. Deploy bản có fix lên STAGING.<br>3. Quay lại tab đang mở (vẫn **không reload**), bấm nút `登録`.<br>4. Quan sát màn hình.<br>5. Mở lại danh sách (tab mới) kiểm tra bản ghi và giá trị đối tượng.<br>6. Lặp lại nhưng ở bước 1 **không chạm vào radio nào**. | Tên `TC38301-STALE-01` / `TC38301-STALE-02`; màn mở trước deploy, submit sau deploy | - **Không** lỗi hệ thống 500, **không** trang trắng.<br>- Hoặc lưu đúng `ブロックした友だち`, hoặc báo lỗi rõ ràng yêu cầu tải lại trang — **không được lưu sai âm thầm thành `有効友だち`**.<br>- Không tạo bản ghi nửa vời.<br>- Lần 2 (không chạm radio): cũng không lỗi hệ thống. | Chưa test |  | STAGING |  |  |  | Spec không ghi | **Lấp GAP-4** — `DEPLOY-LIVE-001` ưu tiên **Cao**, trigger khớp vì fix (b) **đổi payload của endpoint init**. Đây là bản mở rộng của `TC-FUNC002-01` sang kịch bản deploy thật. Evidence: **video từ lúc mở màn → deploy → submit + log request**. |
| TC-UIFIELD001-01 | UI-FIELD-001 | Normal | Màn tạo auto reply mới trên web có sẵn 有効友だち được chọn, không để trống cả 2 radio | - Đăng nhập admin STAGING đã deploy `f6ee800f86`, đã chọn bot test<br>- Xoá cache trình duyệt để chắc chắn tải bản mới | 1. Từ danh sách auto reply bấm 「新規作成」.<br>2. Ngay khi màn load xong, **chưa chạm vào bất kỳ radio nào**, quan sát nhóm 「アクション稼働対象絞り込み」.<br>3. Điền các trường bắt buộc khác, **không đổi radio**, bấm 「登録」.<br>4. Mở lại bản ghi bằng 「編集」, quan sát radio.<br>5. Lặp lại bước 1-2 nhưng mở màn tạo qua chức năng 「コピー」từ 1 bản ghi `ブロックした友だち` — radio phải là `ブロックした友だち` (không bị ép về mặc định). | Không nhập gì vào nhóm đối tượng ở lần 1; lần 2 mở qua chức năng sao chép từ bản ghi block | - Lần 1: radio `有効友だち` **được chọn sẵn ngay khi màn load**, không có trạng thái cả 2 radio đều trống. Lưu xong mở lại vẫn `有効友だち`.<br>- Lần 2 (mở qua sao chép): radio là `ブロックした友だち` **đúng theo bản gốc**, giá trị mặc định **không** ghi đè giá trị đọc từ bản ghi nguồn. | Chưa test |  | STAGING |  |  |  | Spec không ghi | **Lấp GAP-5** (`REQ-002`). Verify hệ quả **UI** của fix (b) — NEW-7 mới chỉ verify ở tầng API. Bước 5 chống hồi quy: mặc định mới không được đè luồng sao chép. Evidence: **screenshot màn ngay khi load, chưa thao tác**. |
| TC-COMPATLEGACY001-01 | COMPAT-LEGACY-001 | Normal | Bản ghi auto reply tạo TRƯỚC fix mở ra sửa và lưu lại được đúng đối tượng | - STAGING đã deploy `f6ee800f86`<br>- Có sẵn ≥ 2 bản ghi auto reply **tạo từ trước khi fix lên môi trường** (bản ghi cũ hiện đang lưu `有効友だち` dù người tạo đã chọn `ブロックした友だち`)<br>- Ghi lại danh sách id/tên các bản ghi cũ này trước khi test | 1. Mở 1 bản ghi cũ bằng 「編集」, quan sát radio đang hiển thị.<br>2. Đổi radio sang `ブロックした友だち`, bấm 「登録」.<br>3. Mở lại bản ghi, quan sát radio.<br>4. Mở 1 bản ghi cũ thứ hai, **không đổi gì cả**, chỉ sửa 1 trường phụ (VD tên) rồi lưu.<br>5. Mở lại bản ghi thứ hai, quan sát radio có bị đổi ngoài ý muốn không. | 2 bản ghi tạo trước fix; bản 1 đổi đối tượng, bản 2 chỉ đổi trường phụ | - Bản 1: sau lưu hiển thị `ブロックした友だち`, giá trị được sửa thành công.<br>- Bản 2: radio **giữ nguyên như trước khi sửa**, không bị mặc định mới ép về `有効友だち`.<br>- Cả 2 bản ghi mở màn sửa / danh sách không lỗi. | Chưa test |  | STAGING |  |  |  | Spec không ghi | **Lấp AP-3 + `[MAJOR]` §4.2** — RULE-09 (cũ & mới song song). Dev khẳng định *"bản ghi cũ không tự sửa được"* ⇒ phải chứng minh user **sửa tay được**. Evidence: **screenshot trước/sau của cả 2 bản ghi**. |
| TC-DATADB001-01 | DATA-DB-001 | Normal | Tạo auto reply trùng tên trên 2 bot, mỗi bot giữ đúng đối tượng của mình | - STAGING đã deploy `f6ee800f86`<br>- Tài khoản admin quản lý **≥ 2 bot** (bot X và bot Y)<br>- Cả 2 bot chưa có auto reply trùng tên với tên test | 1. Chọn **bot X**, tạo auto reply tên `TC38301-SCOPE`, đối tượng `ブロックした友だち`, lưu.<br>2. Chuyển sang **bot Y**, tạo auto reply **trùng tên** `TC38301-SCOPE`, đối tượng `有効友だち`, lưu.<br>3. Quay lại bot X, mở bản ghi `TC38301-SCOPE`, quan sát radio.<br>4. Sang bot Y, mở bản ghi cùng tên, quan sát radio.<br>5. Ở bot X sửa đối tượng sang `有効友だち` rồi lưu; quay sang bot Y kiểm tra bản ghi bot Y **có bị đổi theo không**. | Cùng tên `TC38301-SCOPE` trên 2 bot · bot X = block(0) · bot Y = active(1) | - Bot X hiển thị `ブロックした友だち`, bot Y hiển thị `有効友だち` — **độc lập, không lẫn**.<br>- Sau bước 5: bot X đổi thành `有効友だち`, **bot Y giữ nguyên** giá trị cũ, không bị ghi đè.<br>- Danh sách của mỗi bot chỉ hiện bản ghi của chính bot đó. | Chưa test |  | STAGING |  |  |  | Spec ghi rõ | **Lấp GAP-7** — `DATA-DB-001` + `PERM-003` (cách ly đa tài khoản). Evidence: **screenshot danh sách + màn sửa của cả 2 bot**. |
| TC-REGSHARED001-04 | REG-SHARED-001 | Normal | Sao chép dữ liệu sang bot mới giữ đúng đối tượng ブロック của auto reply nguồn | - STAGING đã deploy `f6ee800f86`<br>- Bot nguồn có ≥ 1 auto reply đối tượng `ブロックした友だち` và ≥ 1 auto reply `有効友だち`<br>- Có quyền dùng chức năng sao chép dữ liệu sang bot mới | 1. Ở bot nguồn, ghi lại danh sách auto reply kèm đối tượng của từng bản ghi.<br>2. Chạy chức năng sao chép dữ liệu sang bot mới (bot đích).<br>3. Đợi quá trình sao chép hoàn tất.<br>4. Chuyển sang bot đích, mở từng auto reply được sao chép, quan sát radio đối tượng.<br>5. Đối chiếu với danh sách ghi ở bước 1.<br>6. Quay lại bot nguồn kiểm tra các bản ghi gốc không bị thay đổi. | Bot nguồn có cả 2 loại đối tượng: `ブロックした友だち` và `有効友だち` | - Mọi auto reply ở bot đích mang **đúng đối tượng như bản ghi nguồn tương ứng**.<br>- Bản ghi nguồn `ブロックした友だち` **không** bị chuyển thành `有効友だち` ở bot đích.<br>- Bot nguồn giữ nguyên, không bị tác động. | Chưa test |  | STAGING |  |  |  | Spec không ghi | **Lấp GAP-6** — `TemplateRepository:1919`, Dev tự khai **cùng pattern lỗi nhưng CHƯA fix, ngoài scope**. ⚠️ **TC này dự kiến FAIL** — mục đích là lấy bằng chứng để **raise ticket riêng**, không phải để chặn ticket #38301. Evidence: **bảng đối chiếu đối tượng từng bản ghi nguồn ↔ đích**. |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — 3 điểm:

**(1) Giá trị mặc định của màn tạo mới chưa có trong spec.**
- Section: [spec-features/admin/auto-reply/feature-spec.md](../../spec-features/admin/auto-reply/feature-spec.md) — bảng mapping UI ↔ DB (dòng ~598) và bảng enum (dòng ~1011-1012).
- Nội dung cần update: ghi rõ **màn 自動応答（作成）mặc định chọn `有効友だち` (`is_apply_active_friend = 1`)**, và giá trị này **bắt buộc luôn có mặt trong payload gửi lên** (cột `NOT NULL`, không chấp nhận `null`). Hiện `REQ-002` đang **suy từ default cột DB**, không có spec chống lưng ⇒ mọi TC liên quan phải để `Trạng thái đánh giá spec = Spec không ghi`.
- Người chịu trách nhiệm: PM + Dev (xác nhận đây là hành vi chủ ý, không phải side-effect của fix).

**(2) Spec auto-reply thiếu hẳn nhóm endpoint mobile.**
- Section: cùng file, danh sách `EP-01` … `EP-12` hiện **chỉ có endpoint web**.
- Nội dung cần update: bổ sung `/init-autoreply-form` và `/save-autoreply` (`api.php:345-346`, `AutoreplyMobileController`) — đây là lý do khiến bộ requirement Studio bỏ sót hoàn toàn luồng mobile (§3). Ghi rõ **mobile là bản copy 1:1 của web** để lần sau mọi thay đổi web tự động kéo theo phạm vi mobile.
- ⚠️ **Vẫn cần update dù vòng này đã descope test mobile** (§4.0): spec thiếu endpoint là **nguyên nhân gốc** khiến bộ TC sinh ra không có mobile — không sửa spec thì vòng sau lặp lại y hệt.
- Người chịu trách nhiệm: Dev.

**(3) Ghi nhận `TemplateRepository:1919` là nợ kỹ thuật đã biết.**
- Nội dung: thêm ghi chú vào spec rằng **chức năng sao chép dữ liệu sang bot mới hiện KHÔNG copy `is_apply_active_friend`** — hành vi hiện tại là bản sao luôn về `有効友だち`. Kèm số ticket riêng sau khi raise.
- Người chịu trách nhiệm: Leader raise ticket → Dev cập nhật spec.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ✅ (có NEW-2 tái hiện đúng steps file 01) · A.2 ⚪ (F3/F4 GAP — **descoped** §4.0) · A.3 ⚠️ (D1 thiếu boundary/negative) · A.4 ⚪ (T2 GAP — **descoped**) · A.5 ✅ (không ORPHAN) · A.6 ⚠️ (fix-shape phủ 2/5 call site; phần thiếu còn lại = clone bot)
- [x] **B. Chất lượng từng TC** — B.1 ✅ (title có keyword, expected đo lường được) · B.2 ⚠️ (NEW-7 gộp 3 dataset) · B.3 ✅ (định danh bằng id/marker duy nhất — làm tốt) · B.4 ⚠️ (NEW-2 precondition "bot oppo" không chắc tồn tại)
- [x] **C. Chất lượng bộ TC tổng thể** — ❌ tỷ lệ `Normal : Abnormal : Boundary` = **7 : 0 : 0** (khuyến nghị ~40/35/25); không trùng lặp TC ✅; phân bố quan điểm dồn 3/7 vào `REG-SHARED-001` ⚠️
- [x] **D. Spec alignment** — ⚠️ TC không mâu thuẫn spec, nhưng `REQ-002` không có spec chống lưng → §6
- [x] **E. Hành chính** — ⚠️ `TC No.` đúng format repo, nhưng 3/7 gắn mã quan điểm không tồn tại; `Trạng thái đánh giá spec` trống toàn bộ
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — **A** (input): ❌ chưa bê 3 cột Normal/Abnormal/Boundary của kiểu input radio/enum · **B** (UI): ⚠️ chỉ rà radio, chưa rà trạng thái mặc định · **C** (bản đồ LME): ❌ chưa mở khối 21 đường gửi tin / xử lý friend block · **D/D2**: ⚠️ task không chạm media/domain/job/bill ⇒ RULE-08 không bắt buộc PRODUCTION, nhưng chưa có run STAGING · **E** (media): × không áp dụng
  - [x] F.3 RULE — RULE-01 ❌ · RULE-02 ❌ (Ghi chú không ghi loại evidence) · RULE-03 ⚠️ (Studio có ghi lý do × cho `STATE-MATRIX-001`, `DATA-DB-001` — chấp nhận được) · RULE-06 ❌ · RULE-07 ✅ (verify DB + UI đầy đủ — làm tốt) · RULE-08 × không áp dụng · RULE-09 ❌ · RULE-12 ⚠️ (có smoke + vùng ảnh hưởng web, thiếu mobile)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` — luồng chính đúng đặc tả | **Cao** | ◯ luôn bắt buộc | NEW-1, NEW-2 | **RISK** — chỉ `Normal`, thiếu Abnormal + Boundary (RULE-01); thiếu output cuối chuỗi (RULE-06) |
| `FUNC-002` — bỏ trống trường bắt buộc, đủ luồng create/edit/copy/API | **Cao** | ◯ form có trường bắt buộc; luồng mobile là luồng vào thứ 5 | — | 🔴 **GAP** → `[BLOCKER]` GAP-3 |
| `FUNC-003` — nhập sai định dạng, **test cả server-side** | Cao (field ảnh hưởng đối tượng gửi tin) | ◯ | — | 🔴 **GAP** → `[BLOCKER]` GAP-3 |
| `FUNC-004` — giới hạn trên/dưới, 5 pattern biên | **Cao** | ◯ enum nhị phân 0/1 vẫn có biên ±1 | — | 🔴 **GAP** → `[BLOCKER]` GAP-3 |
| `DATA-DB-001` — `WHERE` scope 2 tài khoản + khóa mồ côi | **Cao** | ◯ hàm dùng chung CREATE/UPDATE | — | 🔴 **GAP** → `[MAJOR]` (hạ từ BLOCKER — diff không chạm `WHERE`, xem §4.2) |
| `DATA-REF-001` — copy phải độc lập với bản gốc | **Cao** | ◯ có chức năng コピー, và copy đi qua nhánh CREATE | NEW-6 | **RISK** — chỉ `Normal`; chưa test copy khi dữ liệu tham chiếu đã xóa |
| `REG-SHARED-001` — shared code, test **từng nơi** trong danh sách Dev | **Cao** | ◯ pattern lặp ở 5 call site | NEW-4, NEW-5, NEW-6 | 🟡 **GAP một phần** — phủ 2/5 call site: mobile ⚪ descoped (§4.0), clone bot → `[MAJOR]` GAP-6 |
| `OUT-TRUTH-001` — UI/message khớp trạng thái THẬT | **Cao** | ◯ chính là bug lõi | NEW-1, NEW-2 (readback) | **RISK** — không có case "báo thành công giả" khi lưu thất bại |
| `MSG-001` — gửi ĐÚNG đối tượng | **Cao** | ◯ `BR-19`: field này quyết định tập rule chạy runtime | — | 🔴 **GAP** → `[BLOCKER]` GAP-2 |
| `MSG-USER-001` — LINE user lifecycle (block/unblock) | **Cao** | ◯ | — (Studio tự hạ cấp *"verify gián tiếp qua DB"*) | 🔴 **GAP** → `[BLOCKER]` GAP-2 |
| `SYNC-APP-001` — đồng bộ Web ⇔ Mobile app | **Cao** (flow critical user-facing) | ◯ trigger **có khớp** (fix chốt sửa cả web và mobile) → Leader chuyển sang **✕** | — | ⚪ **DESCOPED** — Leader duyệt không test mobile vòng này. Lý do + rủi ro tồn đọng ghi ở **§4.0** (RULE-03: × ở quan điểm **Cao** bắt buộc có lý do + Leader approve) |
| `DEPLOY-LIVE-001` — client cũ gọi server mới (đổi payload API) | **Cao** | ◯ fix (b) thêm key vào response init | — | 🔴 **GAP** → `[BLOCKER]` GAP-4 |
| `COMPAT-LEGACY-001` — dữ liệu đời cũ chạy song song | **Cao** | ◯ bản ghi tạo trước fix đang lưu sai; app client cũ | — | 🔴 **GAP** → `[MAJOR]` AP-3 |
| `PERM-003` — cách ly dữ liệu đa tài khoản LINE OA | **Cao** | ◯ hàm dùng chung nhiều bot | — | 🔴 **GAP** → `[MAJOR]` GAP-7 (gộp với `DATA-DB-001`) |
| `UI-FIELD-001` — field con theo field cha / trạng thái mặc định | Trung bình | ◯ radio mặc định là hệ quả fix (b) | — | 🔴 **GAP** → `[MAJOR]` GAP-5 |
| `UI-003` — loading / rỗng / lỗi, chống **false success** | Trung bình → Cao (có rủi ro false success) | ◯ case 1048 có thể báo thành công giả | — | 🔴 **GAP** → gộp `[BLOCKER]` GAP-3 |
| `ENV-003` — khác biệt dev/staging/production | Cao | ✕ | — | **×** — task không chạm media / domain / job nền / loadbalance / bill tiền ⇒ RULE-08 không bắt buộc PRODUCTION. *(Vấn đề môi trường được xử lý riêng ở `[BLOCKER]` ENV-1)* |
| `DEPLOY-ASSET-001` — version asset JS/CSS | Cao | ✕ | — | **×** — diff **không** sửa file JS/CSS/font/icon (`create.js` giữ nguyên). Rủi ro client cũ đã quy về `DEPLOY-LIVE-001` |
| `CONC-001` — 1 hành động chỉ xử lý 1 lần | Cao | ✕ | — | **×** — fix không chạm khóa/giao dịch/đồng thời; double-click 「登録」là hành vi có sẵn, ngoài phạm vi diff (RULE-12) |
| `DATA-AUDIT-001` — lịch sử thao tác | Cao | ✕ | — | **×** — auto-reply config không thuộc nhóm dữ liệu nhạy cảm (khách hàng / thanh toán / phân quyền / tag) |
| `DATA-MIG-001` — migration | Cao | ✕ | — | **×** — không có migration, không đổi cấu trúc bảng (`✔ Không cần recover data`) |
| `MSG-003` — xử lý blocked user khi gửi hàng loạt | Cao | ✕ | — | **×** — auto-reply là trả lời 1:1 theo sự kiện, không phải gửi hàng loạt. Khía cạnh blocked user đã quy về `MSG-001` / `MSG-USER-001` |
| `PAY-*` · `MEDIA-*` · `INTG-*` · `JOB-001` · `PERF-LARGE-001` · `BULK-001` · `SEC-*` · `STATE-*` | — | ✕ | — | **×** — fix 4 dòng, không chạm tiền / media / tích hợp ngoài / job nền / dữ liệu lớn / thao tác hàng loạt / bảo mật / máy trạng thái |

> **§4 checklist-lme (FORM-01, CHAT-01, ADM-01/03/04, TPL-01)**: đã rà, **không mục nào khớp task**. Theo RULE-11 cũng không dùng để flag BLOCKER/MAJOR.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

### Việc cần làm ngay (theo thứ tự)

1. **Deploy `f6ee800f86` lên STAGING + xác nhận commit đang chạy** → chạy lại 7 TC. Không làm bước này thì mọi kết luận Đạt/Không đạt đều vô nghĩa (`[BLOCKER]` ENV-1).
2. **Không đẩy bug Studio #684 sang Redmine như bug sản phẩm** — chính nội dung của nó kết luận là lỗi môi trường (`[BLOCKER]` EXEC-1).
3. Bổ sung **10 TC** ở §5, đặt `exec_mode = manual` cho nhóm cần LINE app thật / thao tác deploy.
4. Yêu cầu Studio giải trình **TC `NEW-3` đã biến mất** và kết quả `fail` bị thiếu ở run #473 (`[MAJOR]` EXEC-3).
5. Yêu cầu Dev **đính chính mục 7 của `03-dev-impact.md`**: luồng COPY **có** bị ảnh hưởng (`[MAJOR]` DEV-IMPACT-1).
6. Tester **tick 2 checkbox verify** ở `01-bug-task.md` và `03-dev-impact.md` (`[MAJOR]` INPUT-1).
7. Leader **raise ticket riêng** cho `TemplateRepository:1919` (`[MAJOR]` GAP-6).
8. **Chốt phương án cho phần mobile đã descope** (§4.0): raise ticket test mobile riêng, **hoặc** ghi biên bản release rằng mobile của `#38301` lên production **không có bằng chứng test**.
