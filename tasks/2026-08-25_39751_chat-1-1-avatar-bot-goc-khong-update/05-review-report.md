# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#39751 — [Profile sender] Không hiển thị avatar của profile bot gốc tại màn chat 1:1 trên web khi thực hiện chọn bot gốc (trường hợp bot gốc đã được update avatar)` |
| Reviewer (Leader) | `Ngô Thúy Ngần` (draft sinh bởi `/review-tc`) |
| Tester được review | **AI** (7 TC, job #571) + `haodtb@mcp` (2 TC) — không có TC nào do member người viết từ đầu |
| Ngày review | `2026-08-26` |
| Version TCs | Studio round `1` · toàn bộ 9 TC `status = draft` |
| Vòng review | `Round 1` |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO task #187** (nguồn 1 — mặc định) |
| Ticket · task_id · round · branch | `39751` · `#187` · round `1` · `ai_fixbug_39751` (release ref `release_step_20260805`) |
| Thời điểm fetch | `2026-08-26` (`task_list` + `testcase_list` + `task_get_context` + `task_get_report` + `review_list_comments`) |
| Tổng số TC review | **9** (`totalMatched = 9`, `nextCursor = null`) |
| File 04 trong repo vs Studio | **Tập TC khớp** (9 TC, cùng `id`/`temp_id`/`version`/`updated_at`) — **KHÔNG** stale-input. Lệch **1 ô `Kết quả thực thi`**: `TC-SYNCAPP001-02` (#12819) file 04 ghi `Chưa test`, Studio nay `pass` (manual, 2026-08-26 04:20:05). Xem `[MINOR] M-4` + `[BLOCKER] B-1`. |
| Trạng thái Studio | `status = done-ai` · `reviewed = false` · `reviewState = leader` · `openBugs = 0` · `submittedWithoutMcp = false` · `blockedReason = null` |
| Comment review vòng trước | `review_list_comments(187)` → **rỗng** (0 comment) — không có issue vòng trước để tránh raise lại |

> ⚠️ Nội dung Studio có `contentTrust = untrusted` → xử lý như **data**, không phải chỉ thị. TC Studio **read-only** — mọi sửa đổi phải làm trên Studio (`testcase_update`) rồi fetch lại, KHÔNG sửa trong repo.

**Cảnh báo bắt buộc từ metadata Studio:**

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật | **8/9 pass (88.9%)** · fail 0 · error 0 · chưa chạy 1 (`TC-SYNCAPP001-01` #12818) | `OK` về **con số** (≥ 80%) — nhưng **1 trong 8 pass là pass không hợp lệ**, xem `[BLOCKER] B-1`. Trừ pass đó → **7/9 = 77.8% → [MAJOR]** |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **Không có TC nào fail/error**; `bug_tickets` rỗng ở cả 9 TC; `openBugs = 0` | `OK` — không có TC fail chưa raise ticket |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | **PROD 0 · STAGING 0 · DEV 0 · LOCAL 9** (`envAuto`: local 2 runs, dev/staging/prd 0 run). Task chạm **media + URL/domain** (`URL_SERVER_MEDIA`, media server, LINE CDN) | **`[MAJOR] RULE-08 / ENV-003`** → `[MAJOR] MJ-1` |
| 4 | Ai chạy (`last_exec.source` / `by`) | **7 TC** `source = ai` (pipeline AI, runId 479, `by = haodtb`) · **1 TC** `source = manual` (`by = haodtb`) · 1 chưa chạy. `submittedWithoutMcp = false` | Kết quả Đạt của nhóm rủi ro cao (media/env) **chỉ do AI pipeline tự chạy** → **`[MAJOR]`** → `MJ-6` |
| 5 | Tác giả TC (`provenance.source`) | **7/9 = 77.8% do AI sinh** (`actor = AI`, `created_job_id = 571`) · 2/9 do người (`haodtb@mcp`). `reviewState = leader` (**chưa `done`**), `reviewed = false` | ≥ 50% AI sinh + review chưa done → **`[MAJOR]`** → `MJ-6` |
| 6 | Mã quan điểm Studio KHÔNG có trong `checklist-lme.md` | **3 nhóm / 5 lượt TC**: `TOOL-KNOW-002` (2 TC), `API-CONTRACT-001` (1 TC), `viewpoint = null` (2 TC) → **4/9 TC không map được coverage** | **`[MAJOR]`** → `MJ-3`. Các TC này **KHÔNG được tính là cover** ở §7 F.1 |

> ⚠️ **Lưu ý đọc field `toolWritten`**: `{tool: 7, mcp: 2, human: 0}` là **kênh ghi**, KHÔNG phải tác giả. Tác giả thật đọc ở `provenance.source` → 7 `ai` + 2 `human`. Đừng kết luận "0 TC do người viết".

### Bổ sung từ `task_get_report` (không có trong `testcase_list`)

| Chiều | Nội dung |
|---|---|
| Số lần chạy auto | **2 run**, cả 2 ở `env = local`: run **443** (2026-08-24, `counts.pass = 8`) · run **479** (2026-08-25, `counts.pass = 7`) |
| Chênh lệch run 443 | `counts.pass = 8` nhưng chỉ **7 result** được trả về (12409, 12410, 12411, 12412, 12413, 12414, 12415). Dãy `temp_id` hiện có là NEW-1…NEW-7, **NEW-9, NEW-10** — **thiếu NEW-8** → có **1 TC đã bị xóa** sau run 443. Xem `[NIT] N-1` |
| Manual result | **1 result** — `id 4420`, tcId **12819**, env **`local`**, tester `haodtb`, status `pass`, **`actual = null`**, **`evidence = []`**, at `2026-08-26 04:20:05` → **`[BLOCKER] B-1`** |
| Coverage spec (Studio tự tính) | `total 12 · covered **0** · partial 11 · **none 1`** — **không ref nào đạt `covered`** |
| Ref `level = none` | **`BR-10`** — *"sharding lịch sử tin theo năm — `refreshMessage` đọc nhiều bảng, fix áp dụng cho tất cả"*, `tcIds = []` → **`[BLOCKER] B-2`** |
| Redmine writeback đề xuất | *"Auto pass 14 · Manual pass 1 · Độ phủ spec: 0/12 covered (1 chưa phủ) · Bug: tổng 0"* — **KHÔNG được post lên Redmine ở trạng thái hiện tại** (xem §1) |

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: 3 BLOCKER — (1) TC end-to-end LINE app được tick `pass` ở `env = local` với `actual = null` và **0 evidence**, vi phạm RULE-02 + RULE-06 + MSG-004; (2) `BR-10` sharding lịch sử tin **theo năm** có **0 TC** trong khi bug đúng là về **tin cũ** — chính Studio đánh `level = none`; (3) `getMessageSocket` (F2, Direct impact) chỉ có 1 TC cover **1/4 nhánh điều kiện** mà fix đã thêm, trong khi `refreshMessage` được cover đủ 4/4 — lỗi ở nhánh còn lại sẽ lọt. Ngoài ra 0/9 TC chạy production dù fix nửa sau là **dựng URL media theo env**, và Dev **không chạy runtime lần nào** (verify chỉ mức `php -l`).

---

## 2. Tóm tắt cho member

Bộ TC bám khá sát diff: 4 nhánh điều kiện của fix (`bot_image` relative / full URL / null / profile nhân viên) đều có TC, và TC API `refreshMessage` tách riêng là ý hay — evidence run 479 đọc rất rõ ràng, chỉ ra đúng chuỗi URL trước/sau. 2 TC bổ sung sau review (App → Web, LINE app) cũng đúng hướng RULE-06.

Ba chỗ phải sửa trước vòng 2: **(a)** `TC-SYNCAPP001-02` không thể tick Đạt ở `env = local` với evidence rỗng — TC này chỉ có nghĩa khi mở LINE app trên máy thật; hãy hủy kết quả và chạy lại trên staging + thiết bị thật (iOS **và** Android). **(b)** Bug này là về **tin cũ**, mà lịch sử tin nhắn LME **chia bảng theo năm** — tất cả TC hiện tại đều dựng tin "cũ" ngay trong cùng phiên chạy, tức là cùng bảng năm nay; cần TC lấy tin từ **năm trước**. **(c)** Fix được nhân bản ở **2 chỗ** (`refreshMessage` + `getMessageSocket`) nhưng chỉ chỗ thứ nhất được test đủ nhánh — chỗ thứ hai (tin realtime qua socket) mới có 1 case; hãy nhân đủ 4 nhánh sang đường socket.

Ngoài ra: cả bộ **không có TC `Abnormal` nào** (7 Normal + 2 Boundary), và 4/9 TC đang gắn mã quan điểm không tồn tại trong `checklist-lme.md` nên không map được coverage — sửa mã trên Studio giúp vòng 2 chạy được ma trận quan điểm.

---

## 3. Coverage Matrix

> Impact lấy từ `03-dev-impact.md`. Cột `Exec` = `<số pass hợp lệ>/<số TC>` — pass ở `env = local` vẫn tính là pass nhưng **không kết luận được cho production** (RULE-08).

| Impact | Loại | Priority | TCs map | # TC | Exec | Status |
|---|---|---|---|---|---|---|
| **BUG (a)** — hồ sơ mặc định dùng **ảnh snapshot cũ** thay vì ảnh bot hiện tại | Fix | — | TC-TOOLKNOW002-01 (#12409, tin cũ), TC-TOOLKNOW002-02 (#12410, tin mới) | 2 | 2/2 @local | **RISK** — chỉ local; "tin cũ" dựng trong cùng phiên → **không chạm shard năm cũ** (`BR-10`), xem `B-2` |
| **BUG (b)** — ảnh bot upload từ LME lưu **đường dẫn tương đối** → 404 → rơi placeholder | Fix | — | TC-ENV003-01 (#12411) | 1 | 1/1 @local | **RISK** — evidence chỉ chứng minh **ghép chuỗi URL**, không chứng minh ảnh tải được (`MJ-2`); `URL_SERVER_MEDIA = http://127.0.0.1:18403` ≠ production |
| **F1** — `ChatController::refreshMessage` | Function | **Direct** | #12409, #12411, #12412, #12413, #12414, #12415 | 6 | 6/6 @local | **OK** (đủ 4/4 nhánh) — nhưng chỉ local |
| **F2** — `ChatController::getMessageSocket` | Function | **Direct** | TC-TOOLKNOW002-02 (#12410) | 1 | 1/1 @local | **RISK → BLOCKER** — chỉ **1/4 nhánh** (thiếu `bot_image` null, full-URL LINE, profile nhân viên trên đường socket). Xem `B-3` |
| **F3** — `checkFullUrl` + env `URL_SERVER_MEDIA` | Function | Indirect | #12411, #12412, #12415 | 3 | 3/3 @local | **RISK** — biến env là **thứ khác nhau giữa các môi trường**, 0 TC production (`MJ-1`) |
| **F4** — render avatar ở `content_chat.blade.php` / `chat-v2.js` | Function | Indirect | #12409, #12413, #12414 (evidence có "DOM avatar khớp X/Z = true") | 3 | 3/3 @local | **RISK** — không có TC verify ảnh thật **load 200** (chỉ so giá trị thuộc tính) |
| **F5** — *(Dev khai CHƯA sửa)* 2 chỗ hiển thị cho **app điện thoại** | Function | Chưa sửa | TC-SYNCAPP001-01 (#12818) — App **gửi** → Web **hiển thị** | 1 | **0/1 chưa chạy** | **RISK** — và **GAP** cho chiều *app **hiển thị*** (không TC nào mở app xem avatar) |
| **F6** — *(Dev khai CHƯA sửa)* nội dung **trích dẫn (quoted)** lưu lúc gửi | Function | Chưa sửa | — | **0** | — | **GAP** (`MJ-5`) |
| **D1** — thao tác ghi DB | Data | — | *(không có — fix chỉ đọc)* | — | — | **N/A** — `DATA-DB-001` đánh × hợp lệ, xem §7 F.1 |
| **R1** — đọc `bots.bot_image` | Data (đọc) | — | #12409, #12410, #12411, #12412, #12413 | 5 | 5/5 @local | **OK** — đủ 3 dạng: relative / full URL / null |
| **R2** — đọc `bots_profiles.avt_path` (nhánh profile nhân viên) | Data (đọc) | — | TC-NOVIEWPOINT-01 (#12414) | 1 | 1/1 @local | **RISK** — 1 TC happy-path, không có edge state (`avt_path` null, profile đã xóa) → `MJ-8` (AP-3) |
| **R3** — đọc `nick_name` / `view_name` | Data (đọc) | — | #12414 (UI), #12415 (API) | 2 | 2/2 @local | **RISK** — chưa test **tên bot đổi** song song với avatar đổi (spec REQ-001 nói "và tên hiện tại") |
| **R4** — env `URL_SERVER_MEDIA` | Config | — | #12411 | 1 | 1/1 @local | **RISK** — chỉ giá trị localhost; không có case cấu hình **sai/thiếu** (rủi ro #2 Dev tự nêu) |
| **T1** — **1-on-1 Chat (FA-001)** | Feature | *(Dev không ghi mức)* → Leader chốt **Medium** | #12409, #12410, #12411, #12412, #12413, #12414, #12415, #12818 | 8 | 7/8 @local | **RISK** — chỉ hover trong khung tin; **không** test màn danh sách hội thoại / modal chọn profile sender / loadmore tin cũ (`MJ-9`, `MJ-10`) |
| **T2** — **Chat Settings** — quy ước "hồ sơ mặc định = danh tính bot hiện tại" | Feature | *(Dev không ghi mức)* → Leader chốt **Medium** | #12414 | 1 | 1/1 @local | **RISK** — 1 TC regression happy-path duy nhất (AP-3) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| `TC-SYNCAPP001-02` (#12819) | LINE app hiển thị đúng avatar của profile sender mà user đã chọn khi gửi tin | Avatar hiển thị **trên LINE app** do payload gửi tin quyết định (sender icon lúc gửi), **không** do `refreshMessage` / `getMessageSocket` — 2 chỗ duy nhất fix chạm. TC này **không trace về code path đã sửa** → **AP-5 layer-downstream over-coverage** | **GIỮ** làm regression RULE-06 (khẳng định fix không làm lệch profile gửi ra ngoài), nhưng: (1) **KHÔNG** được coi là bằng chứng cho fix web-hover; (2) kết quả `pass` hiện tại **phải hủy** — xem `B-1` |

> Không có TC nào lạc chủ đề hoàn toàn. 8/9 TC còn lại đều trace về `refreshMessage` hoặc `getMessageSocket`.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 `03-dev-impact.md`) | **Specific code check** (nhánh điều kiện `if hồ sơ mặc định → bots.bot_image / else → avt_path`, cộng nhánh `checkFullUrl` → ghép hay không ghép `URL_SERVER_MEDIA`) — **nhân bản ở 2 call site**. Đồng thời khớp 2 shape phụ trong bảng BƯỚC 3c: **"upload / media / ảnh / đổi path"** (chuẩn hoá URL media) và **"sửa hàm dùng chung"** (Dev quét ngang, tự khai 3 chỗ cùng kiểu chưa sửa) |
| **Trigger space cần cover** | **8 tổ hợp** = 4 nhánh × 2 call site:<br>① mặc định + `bot_image` **relative** → ghép `URL_SERVER_MEDIA`<br>② mặc định + `bot_image` **full URL (LINE)** → giữ nguyên<br>③ mặc định + `bot_image` **null/rỗng** → placeholder<br>④ **profile nhân viên** → `avt_path` snapshot<br>× call site **A `refreshMessage`** / **B `getMessageSocket`** |
| **Số trigger TCs hiện cover** | **5/8** — call site A: ①#12411 ②#12412 ③#12413 ④#12414 (**4/4 ✔**) · call site B: chỉ ① qua #12410 (**1/4 ✘**) → **thiếu ②③④ ở đường socket** |
| **KH report dạng** | **Symptom-only** — file 01 Actual chỉ ghi *"Hiển thị avatar mặc định của bot gốc và không hiển thị avatar mới sau khi user update"*. Không có error code / log / response. **Không có attachment** trong Redmine |
| **Alternative root causes cần verify** | Dev đã tự tìm **2** root cause (snapshot cũ · relative URL 404). Còn **2 nguyên nhân khả dĩ khác cùng tạo ra đúng triệu chứng đó mà 0 TC nào cover**:<br>**(RC-3)** Nút **đồng bộ avatar** (`Admin\BotController::reGetAvatarBot`) không thực sự cập nhật `bots.bot_image` → **mọi TC đều đặt precondition "đồng bộ thành công"**, tức là **giả định luôn phần KH thao tác**.<br>**(RC-4)** **Cache ảnh của trình duyệt** — `Admin\SettingBotController::update` ghi đường dẫn tương đối; nếu thay ảnh mà **giữ nguyên path**, server trả đúng URL nhưng browser vẫn render ảnh cũ từ cache → KH thấy "avatar cũ". Không TC nào ép bỏ cache (`?v=x` / DevTools disable cache) |
| **Anti-patterns dính** | **AP-2** (symptom-only, xem RC-3/RC-4) · **AP-3** (regression T2 chỉ 1 TC happy-path) · **AP-5** (`TC-SYNCAPP001-02` test layer không bị chạm code).<br>**AP-1** không dính (fix không phải generic catch-all) · **AP-4** không dính (mục "Commit / PR" **có** commit `fda3c1e983` + branch `ai_fixbug_39751` để checkout, dù không có link PR) · **AP-6** không dính (mục 3 có **11 dòng** caller) |

> **Trigger space cover 5/8 → flag `[BLOCKER] B-3` ở §4.1.**

**Ghi chú riêng về shape "sửa hàm dùng chung"**: theo bảng BƯỚC 3c, shape này là BLOCKER **nếu không có danh sách nơi ảnh hưởng do Dev cung cấp**. Ở đây Dev **CÓ** cung cấp (mục 3 — 11 mục; mục 2 — 3 chỗ cùng kiểu chưa sửa) → **không** BLOCKER, nhưng yêu cầu tiếp theo của `REG-SHARED-001` là *"test lại **từng mục** trong danh sách"* thì **chưa đạt**: 0 TC cho quoted message, 0 TC cho app **hiển thị** → `[MAJOR] MJ-5`.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] B-1 · `TC-SYNCAPP001-02` (#12819)** — TC được tick **`pass`** với `env = **local**`, `actual = **null**`, `evidence = **[]**` (manual result `id 4420`, `by = haodtb`, `2026-08-26 04:20:05`). TC này yêu cầu *"Trên thiết bị người nhận mở LINE app và quan sát avatar sender"*, `env_scope = ["dev","staging"]`, note của chính TC ghi *"Cần thiết bị/tài khoản LINE thật nên để manual"*. Một kết quả Đạt ở `local` không có bằng chứng nào là **không thể có thật** — vi phạm đồng thời **RULE-02** (evidence bắt buộc khi Đạt, không chấp nhận "đã xem, OK"), **RULE-06** (output cuối chuỗi trên thiết bị thật) và **`MSG-004`** (bắt buộc screenshot LINE app **iOS VÀ Android**).
  → **Fix**: hủy result `4420` trên Studio, chạy lại trên **staging** với **2 thiết bị thật (iOS + Android)**, đính kèm screenshot LINE app từng thiết bị + screenshot màn chọn profile sender phía admin. Cho tới khi có evidence, coi TC này là **Chưa test** → tỷ lệ pass thật là **7/9 = 77.8%**, dưới ngưỡng 80% của mục 0.6 #1.

- **[BLOCKER] B-2 · GAP-1 — `BR-10` sharding lịch sử tin theo năm: 0 TC** — `task_get_report.coverage` của **chính Studio** đánh `BR-10` = `level: "none"`, `tcIds: []`, kèm note *"sharding lịch sử tin theo năm — `refreshMessage` đọc nhiều bảng, fix áp dụng cho tất cả"*. Bug #39751 **đúng là về tin cũ** (`TC-TOOLKNOW002-01`), nhưng evidence run 479 cho thấy TC đó dựng "2 tin bot (cũ + mới)" **ngay trong cùng một phiên chạy** → cùng bảng shard của năm hiện tại. Nếu nhánh đọc shard **năm trước** dựng thông tin người gửi theo cách khác (hoặc không đi qua đoạn code đã sửa), KH mở hội thoại có tin từ năm ngoái **vẫn thấy avatar cũ** → bug lọt nguyên vẹn với đúng kịch bản KH báo.
  → **Fix**: thêm 3 TC `COMPAT-LEGACY-001` (§5 `TC-COMPATLEGACY001-01/02/03`) — hội thoại có tin thuộc **shard năm trước**, hội thoại **trộn** tin năm trước + năm nay, và tin ở **ranh giới chuyển năm**.

- **[BLOCKER] B-3 · GAP-2 — `getMessageSocket` (F2, Direct impact) chỉ cover 1/4 nhánh** — Fix nhân bản **cùng một khối logic ở 2 chỗ**, nhưng ma trận điều kiện chỉ được test đủ ở `refreshMessage` (4/4 qua #12411/#12412/#12413/#12414). Đường socket chỉ có **#12410**, và evidence run 479 xác nhận nó chỉ chạm nhánh ①: *"getMessageSocket trả `bot_send.bot_image = http://127.0.0.1:18403/images/favicon.png`"*. **Thiếu**: ② `bot_image` đã là full URL LINE (rủi ro **ghép prefix 2 lần** → URL kép → ảnh vỡ), ③ `bot_image` null (rủi ro hiện lại **snapshot cũ** — chính là triệu chứng KH báo), ④ profile nhân viên (rủi ro fix **đụng nhầm** nhánh không mặc định trên đường realtime). Theo `review-checklist.md` §A.6: *"Specific code check → list TẤT CẢ condition Dev đã handle, TCs cover từng cái một"* — mục này **fail**.
  → **Fix**: thêm 3 TC (§5 `TC-FUNC001-01/02/03`) nhân nhánh ②③④ sang đường tin realtime. Evidence #12410 ghi *"Transport socket mô phỏng; code server + render THẬT"* — chấp nhận được cho auto, nhưng **≥ 1 TC phải chạy socket thật** (2 cửa sổ trình duyệt, gửi từ cửa sổ A xem cửa sổ B).

### 4.2 Major (nên fix)

- **[MAJOR] MJ-1 · RULE-08 / `ENV-003` — 0/9 TC chạy production, 0 TC chạy staging** — `envAuto`: `local` 2 run · `dev` 0 · `staging` 0 · `prd` 0. Fix có **nửa sau là dựng URL ảnh theo biến môi trường**; theo Catalog D, production dùng **server media riêng qua `p.lmes.jp`**, ảnh lưu tạm ~1 ngày rồi **sync lên B2**, và access media qua link `step`/`shorten` phải **redirect sang `p.lmes.jp`** — không môi trường nào trong số đó tồn tại ở `local`. Dev **tự nêu đây là rủi ro #2** (*"Phụ thuộc biến môi trường `URL_SERVER_MEDIA`; nếu cấu hình sai thì ảnh bot upload từ LME vẫn không tải được"*) và **chưa chạy runtime lần nào** (mục 6 VERIFY: MySQL Connection refused, verify chỉ mức `php -l`).
  → **Fix**: 3 TC `ENV-003` (§5 `TC-ENV003-03/04/05`) chạy **PRODUCTION**, kèm bảng đối chiếu môi trường theo Catalog D.

- **[MAJOR] MJ-2 · `TC-ENV003-01` (#12411) — evidence yếu hơn Expected** — Expected ghi *"Avatar bot gốc hiển thị đúng trên Web, **không bị vỡ ảnh** hoặc rơi về avatar mặc định do lỗi đường dẫn media"*, nhưng `actual` của run 479 chỉ chứng minh **chuỗi URL được ghép đúng**: *"relative … đã được ghép prefix `URL_SERVER_MEDIA='http://127.0.0.1:18403'` thành full URL"*. Không có bằng chứng ảnh **thật sự tải được** (HTTP 200) hay render ra pixel. Đây đúng là loại "pass ở tầng chuỗi, fail ở tầng ảnh" mà bug gốc gây ra.
  → **Fix**: bổ sung vào Expected/evidence yêu cầu **DevTools > Network: request ảnh avatar trả 200** (không 404) + screenshot avatar hiển thị trong tooltip hover.

- **[MAJOR] MJ-3 · MAPPING — 4/9 TC không map được vào `checklist-lme.md`** — `TOOL-KNOW-002` (#12409, #12410) và `API-CONTRACT-001` (#12415) **không tồn tại** trong tầng 1; #12414 và #12413 có `viewpoint = null`. Theo BƯỚC 0.6 #6 + BƯỚC 3b, các TC này **không được tính là cover** → 3 quan điểm **Cao** (`OUT-TRUTH-001`, `DATA-001`, `FUNC-001`) hiện **không chứng minh được coverage** dù nội dung TC thực tế có chạm. Nghiêm trọng nhất: 2 TC **tái hiện trực tiếp bug** lại là 2 TC không map được.
  → **Fix** (sửa trên Studio bằng `testcase_update`, không sửa trong repo): #12409/#12410 → `OUT-TRUTH-001` (mục *"Đổi cấu hình hiển thị (tên người gửi, **avatar**) → kiểm cả 2 phía độc lập"* khớp chính xác) · #12415 → `OUT-TRUTH-001` hoặc `FUNC-001` · #12414 → `REG-SHARED-001` · #12413 → `UI-003`.

- **[MAJOR] MJ-4 · AP-2 SYMPTOM-ONLY — 2 root cause khả dĩ chưa có TC** — KH chỉ mô tả triệu chứng, Dev tái hiện 2 root cause. Còn **RC-3** (nút đồng bộ không thực sự cập nhật `bots.bot_image`) và **RC-4** (cache ảnh trình duyệt khi thay ảnh giữ nguyên path). **9/9 TC đều đặt precondition "đồng bộ thành công"** → toàn bộ bộ TC **giả định luôn phần KH thao tác**. Nếu bug thật của KH nằm ở RC-3/RC-4 thì fix này ship xong KH **vẫn báo lại**.
  → **Fix**: (a) hỏi Dev có alternative root cause không; (b) thêm `TC-DATACACHE001-01/02` (§5); (c) thêm 1 TC quan sát **kết quả của chính nút đồng bộ** trước khi vào chat.

- **[MAJOR] MJ-5 · `REG-SHARED-001` / REQ-007 — 3 chỗ Dev khai chưa sửa có 0 TC ghi nhận hiện trạng** — Mục 2 file 03: *"Quét ngang còn **3 chỗ cùng kiểu chưa sửa**: 2 chỗ hiển thị cho app điện thoại và nội dung trích dẫn lưu lúc gửi"*. REQ-007 của Studio ghi nhận là ngoài phạm vi, `tcIds` rỗng. Rủi ro thực tế: **Pre-Conditions của chính bug report có nhắc "Trên app, chọn bot gốc → gửi tin"** → KH sẽ kiểm trên app; QA đóng ticket "đã fix" trong khi KH mở app / xem tin trích dẫn **vẫn thấy avatar cũ** → ticket bật lại.
  → **Fix**: thêm 2 TC `REG-SHARED-001` (§5 `TC-REGSHARED001-01/02`) **ghi nhận hiện trạng đã biết** (avatar cũ ở quoted + app là **known-issue ngoài scope #39751**), và Leader chốt với PM có tách ticket riêng không.

- **[MAJOR] MJ-6 · Kết quả Đạt của nhóm rủi ro cao chỉ do AI pipeline chạy, trên bộ TC 77.8% do AI sinh, review chưa done** — (0.6 #4 + #5) 7/8 kết quả pass đến từ `source = ai`; TC thì `provenance.source = ai` 7/9 (`created_job_id = 571`); `reviewState = leader`, `reviewed = false`. Không có QA người nào **tự tay** chạy lại nhóm `ENV-003` / media.
  → **Fix**: QA người chạy tay tối thiểu #12411, #12412, #12413 trên **staging**, đính kèm evidence riêng.

- **[MAJOR] MJ-7 · Không có TC `Abnormal` nào (0/9)** — Phân bố `case_type`: Normal 7 · Boundary 2 · **Abnormal 0**. `ENV-003` là quan điểm **Cao** → **RULE-01** đòi tối thiểu 3 TC Normal + Abnormal + Boundary; hiện có Normal (#12411) + Boundary (#12412) nhưng **thiếu Abnormal** và **không TC nào ghi lý do thiếu**. Abnormal đáng lẽ phải có: `URL_SERVER_MEDIA` cấu hình sai/thiếu, file ảnh tồn tại trong DB nhưng đã bị xóa trên media server (404), đồng bộ avatar thất bại.
  → **Fix**: `TC-ENV003-04` (§5) + ghi lý do vào `Ghi chú` nếu vẫn quyết định bỏ.

- **[MAJOR] MJ-8 · AP-3 — regression T2 chỉ 1 TC happy-path** — `T2 (Chat Settings — quy ước hồ sơ mặc định)` chỉ có #12414, precondition sạch (*"profile 「NV A」 có avatar Z và tên hiển thị riêng"*). Không có edge state: profile nhân viên có `avt_path` **null**, profile nhân viên **đã bị xóa** nhưng tin cũ vẫn tham chiếu, bot **đổi cả tên lẫn avatar** cùng lúc (REQ-001 nói *"và tên hiện tại (`view_name`)"* nhưng **không TC nào verify tên đổi**).
  → **Fix**: `TC-OUTTRUTH001-01/02` (§5).

- **[MAJOR] MJ-9 · `DATA-001` (Cao) — chỉ verify 1 trong nhiều nơi hiển thị** — `DATA-001` yêu cầu đối chiếu **từng nơi** dữ liệu được tham chiếu. Avatar bot gốc xuất hiện ở nhiều chỗ ngoài tooltip hover: **danh sách hội thoại**, **modal chọn profile sender** (`ajaxGetProfileOfBots` — Dev đã đọc nhưng không test), màn `表示設定`, app. Bộ TC chỉ soi tooltip hover trong khung tin.
  → **Fix**: `TC-DATA001-01/02` (§5) — bảng đối chiếu từng nơi hiển thị sau khi đổi avatar.

- **[MAJOR] MJ-10 · `CONC-003` / `LIST-001` — chưa xác nhận đường loadmore tin cũ** — Fix chỉ chạm `refreshMessage` (mở hội thoại) + `getMessageSocket` (tin realtime). **Chưa ai xác nhận** màn chat 1:1 cuộn lên tải thêm tin cũ có dùng **endpoint thứ 3** hay không. Nếu có, đó là **call site thứ 3 chưa được fix** và đúng vào kịch bản "tin cũ" của bug.
  → **Fix**: hỏi Dev endpoint loadmore là gì; nếu khác `refreshMessage` → **nâng lên BLOCKER** và yêu cầu fix bổ sung. TC quan sát: cuộn lên tải thêm rồi hover tin vừa tải.

- **[MAJOR] MJ-11 · Auto-fill từ Redmine chưa được tester verify** — `01-bug-task.md` và `03-dev-impact.md` đều có `Auto-filled: 2026-08-25 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick** ở cả 2 file. Riêng file 03, bảng **4.1 (F1–F6)** và **R1–R4** là do `/new-task` **tự tách ra** từ text Dev (Dev chỉ ghi đúng 1 dòng file ở mục 4.1 và "không có" ở mục 4.2) → toàn bộ coverage matrix §3 đang dựa trên bảng **chưa ai xác nhận**.
  → **Fix**: tester đọc lại Redmine #39751 journal #131960, tick 2 checkbox trước khi review vòng 2 có giá trị.

- **[MAJOR] MJ-12 · `Trạng thái đánh giá spec` trống ở 9/9 TC** — `spec_status = null` toàn bộ. Không TC nào ghi `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`. Trong khi đó **có ít nhất 2 điểm spec không ghi**: (a) bot chưa đặt avatar thì hiện placeholder — Dev tự nhận *"là thay đổi nhìn thấy được"*, chưa ai duyệt đây là hành vi mong muốn; (b) tin trích dẫn hiển thị avatar nào. Nguy cơ **tự suy diễn rồi cho Đạt**.
  → **Fix**: điền `spec_status` cho 9 TC; #12413 phải là `Đã hỏi leader` kèm tên người duyệt.

### 4.3 Minor (có thể fix sau)

- **[MINOR] M-1 · `TC No.` không theo format repo** — Studio dùng `temp_id` dạng `NEW-1`…`NEW-10`; format canonical là `TC-<mã quan điểm bỏ gạch>-<nn>`. `04-tc-list.md` đã sinh TC No. chuẩn khi map, nhưng trên Studio thì chưa. Với 4 TC ở `MJ-3`, TC No. hiện **vô nghĩa** (`TC-NOVIEWPOINT-01/02`) — sửa `viewpoint` xong thì TC No. tự đúng.
- **[MINOR] M-2 · Không TC nào ghi loại evidence bắt buộc (RULE-02)** — Studio không có trường riêng cho việc này; `artifacts` chỉ có screenshot tự động của runner. Với `MSG-004` / `ENV-003`, loại evidence bắt buộc (screenshot LINE app iOS+Android; screenshot/log lấy **trên production**) phải ghi rõ ở `note` để người chạy tay biết cần nộp gì.
- **[MINOR] M-3 · 2 TC người bổ sung có `requirement_keys` rỗng** — #12818, #12819 không gắn REQ nào → không xuất hiện trong bảng truy vết requirement. Gắn #12818 → REQ-001/REQ-002; #12819 → REQ-005.
- **[MINOR] M-4 · `04-tc-list.md` trong repo lệch Studio 1 ô** — cột `Kết quả thực thi` của `TC-SYNCAPP001-02`: repo `Chưa test`, Studio `Đạt`. Tập TC vẫn khớp nên **không** phải `STALE-INPUT`. Vì kết quả Studio đang bị `B-1` bác bỏ, **giữ nguyên `Chưa test` trong repo là đúng hơn** — cập nhật sau khi chạy lại có evidence.

### 4.4 Nit (gợi ý)

- **[NIT] N-1 · TC `NEW-8` đã bị xóa, không có lý do lưu lại** — run 443 báo `counts.pass = 8` nhưng chỉ trả 7 result; dãy `temp_id` nhảy từ NEW-7 sang NEW-9. Nên ghi lý do xóa vào `note` của task hoặc comment review để vòng sau không hỏi lại.
- **[NIT] N-2 · Xung đột merge với #39612 không có TC** — file 03 mục 7: ticket **#39612** (branch `ai_fixbug_33137`, **chưa lên release**) từng chạm **đúng 2 dòng này** với cách sửa tương tự. Không phải việc của bộ TC, nhưng Leader nên chốt với Dev **trước** khi merge, tránh 2 nhánh cùng sửa 1 chỗ rồi hỏng cả hai.
- **[NIT] N-3 · `CHAT-01`** (§4 `checklist-lme.md` — "quan điểm chưa đủ bằng chứng") có liên quan chủ đề chat 1:1, nhưng theo **RULE-11** chỉ nêu ở mức gợi ý, **không** dùng để flag BLOCKER/MAJOR.
- **[NIT] N-4 · Không post `redmineWriteback` ở trạng thái hiện tại** — `task_get_report` đề xuất writeback *"Auto pass 14 · Manual pass 1 · Độ phủ spec 0/12 covered"*. Post nội dung này lên Redmine lúc này sẽ đọc như "đã test xong" trong khi verdict là REJECTED.

---

## 5. TCs đề xuất bổ sung

> Member copy thẳng vào `04-tc-list.md` (hoặc tạo trên Studio bằng `testcase_create`) ở round tiếp theo. **16 cột canonical.** Viết từ góc nhìn manual tester — thao tác UI + quan sát.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-COMPATLEGACY001-01 | COMPAT-LEGACY-001 | Normal | refreshMessage: hội thoại chỉ có tin từ NĂM TRƯỚC (shard cũ) hiển thị avatar bot hiện tại khi hover | - Bot test đã có hội thoại 1:1 với ít nhất 3 tin gửi bằng **hồ sơ mặc định (bot gốc)** từ **năm trước** (nhờ Dev/DBA seed vào shard năm trước, hoặc chọn bot production đã dùng từ năm ngoái)<br>- Lúc gửi các tin đó, avatar bot là ảnh Y<br>- Sau đó đổi avatar bot sang ảnh X (khác rõ ràng, VD Y = hình tròn đỏ, X = hình vuông xanh) và bấm nút đồng bộ trên web, xác nhận đồng bộ báo thành công<br>- Dùng nhánh `ai_fixbug_39751` | 1. Mở màn chat 1:1, chọn hội thoại đã chuẩn bị<br>2. Chờ danh sách tin tải xong<br>3. Hover lần lượt vào **từng** tin của năm trước<br>4. Quan sát ảnh trong tooltip người gửi<br>5. Mở DevTools > Network, lọc theo tên file ảnh avatar, kiểm mã trạng thái của request ảnh | - Avatar cũ Y = `avatar_Y.png` (hình tròn đỏ)<br>- Avatar mới X = `avatar_X.png` (hình vuông xanh)<br>- Số tin năm trước cần kiểm: 3 | **Toàn bộ** tin của năm trước hiển thị avatar **X (hình vuông xanh)** khi hover — không tin nào còn hiện Y. Request tải ảnh avatar trả **HTTP 200**, không 404, không rơi về `avatar_bot_v2.png`. | Chưa test | | STAGING | | | | | **Lấp GAP-1 / `[BLOCKER] B-2`** — `BR-14`+`BR-10`, cover impact **BUG(a)** + **F1** ở nhánh shard năm cũ (Studio đánh `BR-10` level = none). Evidence bắt buộc: screenshot tooltip hover **từng** tin + screenshot Network tab thấy 200. |
| TC-COMPATLEGACY001-02 | COMPAT-LEGACY-001 | Normal | refreshMessage: hội thoại TRỘN tin năm trước + năm nay đều hiển thị cùng avatar hiện tại | - Như TC-COMPATLEGACY001-01<br>- Bổ sung: sau khi đồng bộ avatar X, gửi thêm 2 tin mới bằng hồ sơ mặc định trong **cùng** hội thoại đó | 1. Mở màn chat 1:1, chọn hội thoại trộn<br>2. Hover vào tin **năm trước**, ghi nhận ảnh<br>3. Hover vào tin **năm nay (mới gửi)**, ghi nhận ảnh<br>4. So sánh 2 ảnh<br>5. F5 tải lại trang, lặp lại bước 2–4 | - 3 tin năm trước (gửi khi avatar = Y)<br>- 2 tin năm nay (gửi sau khi avatar = X) | Tin năm trước **và** tin năm nay hiển thị **cùng một** avatar X. Không có hiện tượng tin cũ ra Y còn tin mới ra X. Sau F5 kết quả không đổi. | Chưa test | | STAGING | | | | | **Lấp GAP-1 / B-2** — cover **F1** khi `refreshMessage` phải đọc **nhiều bảng shard** trong 1 lần tải. Evidence: 2 screenshot hover cạnh nhau (tin cũ / tin mới) + 1 cặp sau F5. |
| TC-COMPATLEGACY001-03 | COMPAT-LEGACY-001 | Boundary | refreshMessage: tin ở RANH GIỚI chuyển năm (31/12 và 01/01) hiển thị đúng avatar hiện tại | - Hội thoại có đúng 1 tin gửi bằng hồ sơ mặc định vào **31/12 năm trước** và 1 tin vào **01/01 năm nay** (nhờ Dev/DBA seed)<br>- Avatar bot đã đổi Y → X và đã đồng bộ | 1. Mở hội thoại, cuộn tới vùng giao 2 năm<br>2. Hover tin ngày 31/12<br>3. Hover tin ngày 01/01<br>4. Quan sát avatar của cả 2 | - Tin A: 31/12 năm trước, 23:59<br>- Tin B: 01/01 năm nay, 00:01 | Cả tin 31/12 và tin 01/01 đều hiển thị avatar **X**. Không tin nào bị lỗi hiển thị hay mất avatar tại điểm giao 2 shard. | Chưa test | | STAGING | | | | Spec không ghi → hỏi Dev cách `refreshMessage` gộp shard | **Lấp GAP-1 / B-2** — biên của `BR-10`. Evidence: screenshot hover 2 tin liền kề qua mốc năm. |
| TC-FUNC001-01 | FUNC-001 | Boundary | getMessageSocket: bot CHƯA đặt avatar → tin realtime hiển thị placeholder, không hiện snapshot cũ | - Bot test **chưa đặt avatar** (màn 表示設定 để trống ảnh đại diện)<br>- Trước đó hồ sơ mặc định của bot này **đã từng** có ảnh (snapshot cũ tồn tại)<br>- Mở màn chat 1:1 của **cùng** hội thoại trên **2 cửa sổ trình duyệt** A và B, cả 2 đang ở trạng thái mở sẵn | 1. Ở cửa sổ A, chọn hồ sơ người gửi là **bot gốc**<br>2. Gửi 1 tin nhắn từ cửa sổ A<br>3. **Không** F5 cửa sổ B — chờ tin xuất hiện realtime ở cửa sổ B<br>4. Ở cửa sổ B, hover vào tin vừa nhận<br>5. Quan sát avatar trong tooltip | - `表示設定` của bot: ô ảnh đại diện để **trống**<br>- Nội dung tin: `TC39751_SOCKET_NULL` | Ở cửa sổ B, tin realtime hiển thị **ảnh placeholder mặc định** khi hover. **Không** hiện lại ảnh snapshot cũ của hồ sơ mặc định, **không** vỡ ảnh. | Chưa test | | STAGING | | | | Đã hỏi leader (hành vi placeholder là thay đổi nhìn thấy được — Dev nêu ở mục 7 file 03) | **Lấp GAP-2 / `[BLOCKER] B-3`** — nhánh ③ ở call site **F2 `getMessageSocket`**. Bắt buộc dùng **socket thật 2 cửa sổ**, không mô phỏng. Evidence: screenshot cửa sổ B khi hover. |
| TC-FUNC001-02 | FUNC-001 | Boundary | getMessageSocket: avatar bot là URL đầy đủ từ LINE → tin realtime không bị ghép prefix 2 lần | - Bot test có avatar **lấy từ LINE** (đã bấm đồng bộ avatar từ account LINE, không upload ảnh từ LME)<br>- Mở cùng hội thoại trên 2 cửa sổ trình duyệt A và B | 1. Ở cửa sổ A chọn hồ sơ người gửi là bot gốc, gửi 1 tin<br>2. Chờ tin xuất hiện realtime ở cửa sổ B (không F5)<br>3. Ở cửa sổ B hover vào tin vừa nhận<br>4. Mở DevTools > Network ở cửa sổ B, tìm request tải ảnh avatar, đọc **đường dẫn đầy đủ** và mã trạng thái | - Avatar bot lấy từ LINE (URL bắt đầu bằng `https://profile.line-scdn.net/...`)<br>- Nội dung tin: `TC39751_SOCKET_FULLURL` | Avatar hiển thị bình thường ở cửa sổ B. Đường dẫn ảnh trong Network **chỉ có một** phần `https://` — **không** bị chèn thêm địa chỉ máy chủ media phía trước (không URL kép). Request trả **HTTP 200**. | Chưa test | | STAGING | | | | | **Lấp GAP-2 / B-3** — nhánh ② ở call site F2. Đối chứng với #12412 (đã cover nhánh này ở F1). Evidence: screenshot Network thấy URL đầy đủ + 200. |
| TC-FUNC001-03 | FUNC-001 | Normal | getMessageSocket: tin realtime gửi bằng hồ sơ NHÂN VIÊN vẫn giữ avatar và tên của hồ sơ đó | - Bot có hồ sơ người gửi 「NV A」 với avatar Z và tên hiển thị riêng, khác avatar bot gốc X<br>- Mở cùng hội thoại trên 2 cửa sổ trình duyệt A và B | 1. Ở cửa sổ A mở phần chọn hồ sơ người gửi, chọn 「NV A」<br>2. Gửi 1 tin từ cửa sổ A<br>3. Chờ tin xuất hiện realtime ở cửa sổ B (không F5)<br>4. Ở cửa sổ B hover vào tin vừa nhận<br>5. Quan sát **cả avatar lẫn tên** người gửi trong tooltip | - Hồ sơ 「NV A」: avatar Z, tên hiển thị `NV A`<br>- Avatar bot gốc hiện tại: X<br>- Nội dung tin: `TC39751_SOCKET_STAFF` | Tooltip ở cửa sổ B hiển thị avatar **Z** và tên **`NV A`**. **Không** bị thay bằng avatar X hay tên bot gốc. | Chưa test | | STAGING | | | | | **Lấp GAP-2 / B-3** — nhánh ④ ở call site F2, cover impact **R2** + **T2**. **regression**. Đối chứng với #12414 (đã cover nhánh này ở F1). Evidence: screenshot tooltip cửa sổ B. |
| TC-ENV003-03 | ENV-003 | Normal | PRODUCTION: avatar bot upload từ LME hiển thị được trong chat 1:1 qua máy chủ media thật | - Chạy trên **production** (`step.lmes.jp`), bot thật đã được duyệt cho smoke test<br>- Avatar bot được **upload từ trong LME** ở màn 表示設定 (không phải đồng bộ từ LINE)<br>- Đã bấm đồng bộ và xác nhận thành công<br>- Hội thoại có ít nhất 1 tin gửi bằng hồ sơ mặc định<br>- ⚠️ Không tạo/xóa dữ liệu thật ngoài phạm vi TC | 1. Mở màn chat 1:1 trên production, chọn hội thoại đã chuẩn bị<br>2. Hover vào tin gửi bằng bot gốc<br>3. Mở DevTools > Network, tìm request tải ảnh avatar<br>4. Ghi nhận **tên miền** của request ảnh và mã trạng thái<br>5. Copy đường dẫn ảnh, mở ở tab mới kèm `?v=1` để bỏ qua cache | Avatar upload từ LME, tên file có ký tự thường: `tc39751_prod_avatar.png` | Avatar hiển thị đúng khi hover. Request ảnh trả **HTTP 200**, tên miền là **máy chủ media của production** (`p.lmes.jp`) chứ không phải đường dẫn tương đối hay localhost. Mở lại link kèm `?v=1` vẫn ra đúng ảnh. | Chưa test | | **PRODUCTION** | | | | | **Lấp `[MAJOR] MJ-1` (RULE-08)** — cover **BUG(b)** + **F3** + **R4**. Catalog D: production dùng máy chủ media riêng qua `p.lmes.jp`, ảnh sync lên B2 sau ~1 ngày. Evidence bắt buộc: screenshot Network **trên production** thấy domain + 200. |
| TC-ENV003-04 | ENV-003 | Abnormal | Ảnh avatar không còn trên máy chủ media → hover hiện placeholder, không vỡ ảnh và không hiện snapshot cũ | - Bot có avatar upload từ LME<br>- Nhờ Dev/hạ tầng **xóa file ảnh đó khỏi máy chủ media** (hoặc đổi tên file) trong khi **giữ nguyên** thông tin ảnh của bot trong hệ thống<br>- Hội thoại có tin gửi bằng hồ sơ mặc định | 1. Mở màn chat 1:1, chọn hội thoại<br>2. Hover vào tin gửi bằng bot gốc<br>3. Quan sát avatar hiển thị<br>4. Mở DevTools > Network, đọc mã trạng thái của request ảnh<br>5. Kiểm tra console có lỗi JavaScript nào không | File ảnh avatar bị xóa khỏi máy chủ media; thông tin ảnh của bot vẫn còn | Hover hiện **ảnh placeholder mặc định**, khung tooltip **không vỡ layout**, **không** hiện lại ảnh snapshot cũ, **không** có lỗi JavaScript trên console. Request ảnh trả 404 nhưng giao diện xử lý êm. | Chưa test | | STAGING | | | | Spec không ghi → hỏi leader hành vi mong muốn khi file media biến mất | **Lấp `[MAJOR] MJ-7` (RULE-01 — `ENV-003` là quan điểm Cao đang thiếu Abnormal)**. Cover **F3** + **F4**. Evidence: screenshot tooltip + screenshot Network thấy 404 + console sạch. |
| TC-ENV003-05 | ENV-003 | Abnormal | Cấu hình máy chủ media sai/thiếu → avatar không tải được nhưng không làm hỏng màn chat | - Môi trường test (DEV) được Dev cố tình cấu hình **sai địa chỉ máy chủ media**<br>- Bot có avatar upload từ LME (đường dẫn tương đối)<br>- Hội thoại có tin gửi bằng hồ sơ mặc định | 1. Mở màn chat 1:1, chọn hội thoại<br>2. Chờ danh sách tin tải xong<br>3. Quan sát màn hình có tải đủ tin không<br>4. Hover vào tin gửi bằng bot gốc<br>5. Quan sát avatar + kiểm console | Địa chỉ máy chủ media cấu hình sai (trỏ tới host không tồn tại) | Danh sách tin **vẫn tải đủ và đọc được** — không trắng màn, không loading vô hạn. Avatar rơi về placeholder. Không có exception 500 khi mở hội thoại. | Chưa test | | DEV | | | | Đã hỏi leader | **Lấp `MJ-7`** — đây chính là **rủi ro #2 Dev tự nêu** ở mục 7 file 03 (*"nếu cấu hình sai thì ảnh bot upload từ LME vẫn không tải được"*). Cover **R4**. Evidence: screenshot màn chat còn dùng được + console. |
| TC-DATACACHE001-01 | DATA-CACHE-001 | Abnormal | Thay ảnh avatar mà GIỮ NGUYÊN tên file → hover phải ra ảnh mới, không ra ảnh cũ từ cache trình duyệt | - Bot có avatar upload từ LME, tên file `bot_avatar.png`<br>- Đã mở màn chat 1:1 và hover ít nhất 1 lần để trình duyệt cache ảnh cũ<br>- Chuẩn bị sẵn 1 ảnh mới **khác rõ ràng** nhưng **đặt trùng tên** `bot_avatar.png` | 1. Vào màn 表示設定, upload ảnh mới (trùng tên file), lưu và bấm đồng bộ<br>2. Quay lại màn chat 1:1, **chỉ bấm F5 thường** (KHÔNG Ctrl+F5, KHÔNG xóa cache)<br>3. Hover vào tin gửi bằng bot gốc<br>4. Quan sát ảnh hiển thị<br>5. Mở DevTools > Network, xem request ảnh là `200` hay `from disk cache` | - Ảnh cũ: `bot_avatar.png` = hình tròn đỏ<br>- Ảnh mới: `bot_avatar.png` = hình vuông xanh (trùng tên) | Sau F5 thường, hover hiển thị **ảnh mới (hình vuông xanh)**. Nếu vẫn ra ảnh cũ → **là bug**: cần tham số version trên đường dẫn ảnh. | Chưa test | | STAGING | | | | Spec không ghi → hỏi Dev có gắn tham số version cho ảnh avatar không | **Lấp `[MAJOR] MJ-4` (AP-2, root cause RC-4)** — đây là nguyên nhân khả dĩ thứ 4 tạo đúng triệu chứng KH báo mà **fix hiện tại không xử lý**. Evidence bắt buộc: screenshot Network phân biệt `200` vs `from disk cache`. |
| TC-DATACACHE001-02 | DATA-CACHE-001 | Normal | Nút đồng bộ avatar thực sự cập nhật ảnh bot trước khi kiểm màn chat | - Avatar bot trên account LINE vừa được đổi từ Y sang X<br>- Trên LME, ảnh đại diện bot **vẫn đang là Y** (chưa đồng bộ) | 1. Vào màn quản lý bot / 表示設定, quan sát ảnh đại diện đang hiển thị (phải là Y)<br>2. Bấm nút **đồng bộ avatar**<br>3. Chờ thông báo kết quả, ghi nhận nội dung thông báo<br>4. **F5** lại màn 表示設定, quan sát ảnh đại diện<br>5. Sang màn chat 1:1, hover vào tin gửi bằng bot gốc | Avatar LINE trước: Y (hình tròn đỏ) · sau: X (hình vuông xanh) | Sau khi bấm đồng bộ: thông báo báo **thành công**, và sau F5 màn 表示設定 hiển thị ảnh **X**. Chỉ khi bước này đúng thì hover trong chat mới ra X. Nếu thông báo báo thành công nhưng ảnh vẫn Y → **là bug**, và mọi TC khác của ticket này **không kết luận được**. | Chưa test | | STAGING | | | | | **Lấp `MJ-4` (AP-2, root cause RC-3)** — 9/9 TC hiện tại đều đặt precondition "đồng bộ thành công" mà **không TC nào kiểm chính bước đó**. `OUT-TRUTH-001`: báo thành công thì dữ liệu phải THẬT SỰ được cập nhật. Evidence: screenshot 表示設定 trước/sau + screenshot thông báo. |
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Ghi nhận hiện trạng: tin TRÍCH DẪN (quoted) trên web vẫn hiển thị avatar cũ — known-issue ngoài scope #39751 | - Bot đã đổi avatar Y → X và đã đồng bộ<br>- Trong hội thoại có 1 tin gửi bằng hồ sơ mặc định **từ trước khi đổi avatar**<br>- Dùng nhánh `ai_fixbug_39751` | 1. Mở màn chat 1:1, chọn hội thoại<br>2. Thực hiện thao tác **trích dẫn (reply)** tin cũ đó và gửi 1 tin mới<br>3. Quan sát avatar hiển thị **trong khối trích dẫn**<br>4. Hover vào **tin mới** (không phải khối trích dẫn), quan sát avatar<br>5. Chụp lại cả 2 | Avatar cũ Y (hình tròn đỏ) · avatar mới X (hình vuông xanh) | **Tin mới** hover ra avatar **X** (fix có tác dụng). **Khối trích dẫn** vẫn hiển thị avatar **Y** — đây là **hiện trạng đã biết**, Dev khai ngoài phạm vi (mục 2 file 03, REQ-007), **KHÔNG phải fail của #39751**. | Chưa test | | STAGING | | | | Spec không ghi → REQ-007 ghi nhận là ngoài phạm vi | **Lấp `[MAJOR] MJ-5`** — cover **F6**. Mục đích là **chốt ranh giới** để QA không đóng ticket nhầm và để PM quyết có tách ticket riêng. **regression**. Evidence: 1 screenshot chụp cả khối trích dẫn lẫn tin mới. |
| TC-REGSHARED001-02 | REG-SHARED-001 | Normal | Ghi nhận hiện trạng: xem tin trên APP điện thoại vẫn hiển thị avatar cũ — known-issue ngoài scope #39751 | - Đã đăng nhập cùng bot trên web và app<br>- Bot đã đổi avatar Y → X và đã đồng bộ trên web<br>- Hội thoại có tin gửi bằng hồ sơ mặc định từ trước khi đổi avatar | 1. Trên **web**, mở hội thoại, hover tin cũ → ghi nhận avatar<br>2. Trên **app**, mở đúng hội thoại đó (pull-to-refresh, không restart)<br>3. Quan sát avatar người gửi của cùng tin đó trên app<br>4. So sánh web vs app | Avatar cũ Y · avatar mới X | Web hiển thị **X**; app hiển thị **Y** — lệch nhau. Đây là **hiện trạng đã biết** (Dev khai 2 chỗ hiển thị cho app chưa sửa), **KHÔNG phải fail của #39751**, nhưng phải ghi nhận vì **Pre-Conditions của bug report có nhắc thao tác trên app**. | Chưa test | | STAGING | | | | Spec không ghi → REQ-007 | **Lấp `MJ-5`** — cover **F5** ở chiều *app hiển thị* (khác #12818 vốn là app **gửi** → web **xem**). `SYNC-APP-001`: bug kinh điển là sửa web nhưng quên triển khai sang app. Evidence: screenshot **cả** web và app cạnh nhau. |
| TC-DATA001-01 | DATA-001 | Normal | Sau khi đổi avatar bot, đối chiếu avatar hiển thị ở TẤT CẢ nơi liên quan trên web | - Bot đã đổi avatar Y → X và đã đồng bộ<br>- Hội thoại có tin gửi bằng hồ sơ mặc định (cả tin cũ lẫn tin mới) | 1. Mở màn chat 1:1<br>2. Ghi nhận avatar ở **danh sách hội thoại** bên trái<br>3. Hover tin gửi bằng bot gốc → ghi nhận avatar trong tooltip<br>4. Mở **modal chọn hồ sơ người gửi** → ghi nhận avatar của mục 「hồ sơ mặc định」<br>5. Mở màn **表示設定** → ghi nhận ảnh đại diện<br>6. Lập bảng đối chiếu 4 nơi | Avatar mới X (hình vuông xanh) | **Cả 4 nơi** đều hiển thị avatar **X**. Không nơi nào còn Y hoặc placeholder. | Chưa test | | STAGING | | | | | **Lấp `[MAJOR] MJ-9`** — `DATA-001` (Cao) yêu cầu **bảng đối chiếu từng nơi hiển thị**. Cover **T1**. Bộ TC hiện tại chỉ soi 1/4 nơi (tooltip hover). Evidence: bảng đối chiếu 4 nơi + 4 screenshot. |
| TC-DATA001-02 | DATA-001 | Normal | Đổi ĐỒNG THỜI cả tên lẫn avatar bot → hover tin cũ hiện đủ tên mới và avatar mới | - Bot có tên hiển thị `BOT_OLD` và avatar Y<br>- Hội thoại có tin gửi bằng hồ sơ mặc định lúc còn tên `BOT_OLD` + avatar Y | 1. Vào 表示設定, đổi tên bot thành `BOT_NEW` **và** đổi avatar sang X, lưu<br>2. Bấm đồng bộ, xác nhận thành công<br>3. Mở màn chat 1:1, chọn hội thoại đã chuẩn bị<br>4. Hover vào tin cũ<br>5. Quan sát **cả tên lẫn avatar** trong tooltip | Tên: `BOT_OLD` → `BOT_NEW` · Avatar: Y → X | Tooltip hiển thị tên **`BOT_NEW`** và avatar **X**. Không hiện tên cũ `BOT_OLD` hay avatar Y. | Chưa test | | STAGING | | | | | **Lấp `[MAJOR] MJ-8`** — REQ-001 nói rõ *"và tên hiện tại (`view_name`)"* nhưng **không TC nào verify tên**. Cover **R3**. Evidence: screenshot tooltip thấy đủ tên + ảnh. |
| TC-OUTTRUTH001-01 | OUT-TRUTH-001 | Boundary | Hồ sơ nhân viên CHƯA có ảnh → tin cũ gửi bằng hồ sơ đó không bị thay bằng avatar bot gốc | - Bot có hồ sơ người gửi 「NV B」 **chưa đặt ảnh đại diện**<br>- Hội thoại có tin đã gửi bằng 「NV B」 từ trước<br>- Avatar bot gốc hiện tại là X | 1. Mở màn chat 1:1, chọn hội thoại<br>2. Hover vào tin đã gửi bằng 「NV B」<br>3. Quan sát avatar và tên trong tooltip<br>4. So với avatar bot gốc X | Hồ sơ 「NV B」: ảnh đại diện để trống, tên `NV B` · avatar bot gốc: X | Tooltip hiển thị tên **`NV B`** kèm ảnh placeholder của hồ sơ nhân viên. **KHÔNG** bị thay bằng avatar bot gốc X. | Chưa test | | STAGING | | | | Spec không ghi → hỏi leader | **Lấp `MJ-8` (AP-3)** — edge state của **R2**/**T2** mà #12414 (happy-path) không chạm. Rủi ro: điều kiện phân nhánh hiểu nhầm "không có ảnh" thành "hồ sơ mặc định". **regression**. Evidence: screenshot tooltip. |
| TC-OUTTRUTH001-02 | OUT-TRUTH-001 | Abnormal | Hồ sơ nhân viên ĐÃ BỊ XÓA → tin cũ gửi bằng hồ sơ đó vẫn mở được, không lỗi màn | - Hội thoại có tin đã gửi bằng hồ sơ 「NV C」<br>- Sau đó hồ sơ 「NV C」 **đã bị xóa** ở màn quản lý hồ sơ người gửi | 1. Mở màn chat 1:1, chọn hội thoại<br>2. Chờ danh sách tin tải xong, quan sát có tải đủ tin không<br>3. Hover vào tin đã gửi bằng 「NV C」<br>4. Quan sát tooltip<br>5. Kiểm console có lỗi JavaScript không | Hồ sơ 「NV C」 đã bị xóa khỏi danh sách hồ sơ người gửi | Danh sách tin **vẫn tải đủ**, không trắng màn, không lỗi 500. Hover ra tooltip hợp lệ (tên/ảnh lưu lúc gửi hoặc placeholder), console không lỗi. | Chưa test | | STAGING | | | | Spec không ghi → hỏi leader | **Lấp `MJ-8`** — cover **R2** ở trạng thái tham chiếu mồ côi. Fix đổi cách dựng thông tin người gửi nên nhánh này có rủi ro. Evidence: screenshot màn chat + console. |
| TC-PERM003-01 | PERM-003 | Normal | Đổi avatar bot A không làm đổi avatar hiển thị của bot B trong chat 1:1 | - Tài khoản quản trị có **2 bot**: bot A (avatar X1) và bot B (avatar X2), 2 ảnh khác nhau rõ ràng<br>- Mỗi bot có ít nhất 1 hội thoại với tin gửi bằng hồ sơ mặc định | 1. Chọn bot A, đổi avatar sang X1_new, đồng bộ<br>2. Mở chat 1:1 của bot A, hover tin → ghi nhận avatar<br>3. **Chuyển sang bot B** (change bot)<br>4. Mở chat 1:1 của bot B, hover tin → ghi nhận avatar<br>5. So sánh 2 kết quả | Bot A: X1 → X1_new · Bot B: X2 (không đổi) | Chat của bot A hiện **X1_new**; chat của bot B vẫn hiện **X2**, không bị lây avatar của bot A. | Chưa test | | STAGING | | | | | **Bổ sung theo `PERM-003` (Cao)** — fix đổi nguồn ảnh sang bảng bot; nếu điều kiện lọc theo bot không đủ chặt sẽ lấy nhầm ảnh bot khác. Không TC nào hiện cover đa bot. **regression**. Evidence: 2 screenshot hover sau change bot. |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — 3 điểm:

**(1) Hành vi khi bot chưa đặt avatar** (liên quan `TC-NOVIEWPOINT-02` #12413, `TC-FUNC001-01`)
- Section: spec chat 1:1 — hiển thị thông tin người gửi (`SCR-CHT-01`); `spec-features/admin/chat-1on1/`
- Nội dung cần update: ghi rõ hồ sơ mặc định khi bot **chưa có ảnh đại diện** thì hiển thị **ảnh placeholder hệ thống**, **không** dùng lại ảnh snapshot cũ. Dev tự nhận đây là *"thay đổi nhìn thấy được"* (mục 7 file 03) nhưng **chưa có ai duyệt** đây là hành vi mong muốn — hiện `spec_status` của 9/9 TC đều trống.
- Người chịu trách nhiệm: PM + Test Leader duyệt trước vòng 2.

**(2) Ranh giới phạm vi: tin trích dẫn (quoted) + hiển thị trên app điện thoại**
- Section: spec chat 1:1 — người gửi của tin trích dẫn; spec app mobile
- Nội dung cần update: ghi rõ 3 chỗ Dev khai chưa sửa **vẫn dùng ảnh snapshot lúc gửi**, và đây là hành vi **được chấp nhận tạm thời** (REQ-007) hay là **nợ kỹ thuật cần tách ticket**. Nếu không chốt, KH sẽ báo lại đúng bug này ở đường app.
- Người chịu trách nhiệm: PM chốt scope; Dev tách ticket nếu cần.

**(3) Quy ước đồng bộ `bots.bot_image` ⇄ `bots_profiles.avt_path`**
- Section: spec 表示設定 / quản lý hồ sơ người gửi
- Nội dung cần update: `Admin\SettingBotController::update` chỉ ghi `bots.bot_image`, **không** đồng bộ `bots_profiles.avt_path` (`:246`) → **dữ liệu lệch vẫn tồn tại trong DB**; fix này chỉ **né** nó khi render chứ không dọn. Spec cần ghi rõ `bots_profiles.avt_path` của **hồ sơ mặc định** là trường **không dùng nữa** (deprecated), tránh chức năng mới sau này lại đọc nhầm.
- Người chịu trách nhiệm: Dev + PM.

---

## 7. Checklist đã chạy

- [x] **A. Coverage** — A.1 ✔ (2 TC reproduce) · A.2 ✘ (**F2 thiếu 3/4 nhánh** → `B-3`) · A.3 N/A (không ghi DB) · A.4 ✘ (T2 chỉ 1 TC happy-path → `MJ-8`) · A.5 ✔ (1 ORPHAN nghi ngờ, đã ghi §3) · **A.6 ✘** (trigger space 5/8 → `B-3`; symptom-only 2 root cause thiếu → `MJ-4`)
- [x] **B. Chất lượng từng TC** — B.1 ✔ (title/precondition/steps rõ, expected đo lường được) · B.2 ✔ (atomic) · B.3 ✔ · B.4 ✔ (data cụ thể, không dùng `"test"`/`"abc"`)
- [x] **C. Chất lượng bộ TC** — ✘ **tỷ lệ loại case lệch nặng**: Normal 7 / Abnormal **0** / Boundary 2 (gợi ý 40/35/25) → `MJ-7` · không trùng lặp ✔ · phân bố quan điểm ✘ (dồn vào 2 mã không tồn tại) · multi-device ✘ (chỉ #12819, đang bị `B-1`) · i18n N/A
- [x] **D. Spec alignment** — ✘ `spec_status` trống 9/9 (`MJ-12`); 3 điểm cần update spec ở §6
- [x] **E. Hành chính** — TC ID ✘ (`MJ-3`/`M-1`) · file đúng folder ✔ · version/tester ✔ (Studio round 1, `provenance` đầy đủ)
- [x] **F. Base quan điểm test LME**
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới
  - [x] F.2 Catalog (tầng 2) — **A** N/A (không có ô nhập trong scope fix) · **B** ✔ một phần (tooltip hover — `UIC` chưa rà hết) · **C** ✘ (chưa duyệt hết khối *nơi hiển thị friend/bot info*, chỉ lấy 1 nơi → `MJ-9`) · **D/D2** ✘ (**0 TC production** dù task chạm media + domain → `MJ-1`) · **E** ✘ (không TC nào chạm giới hạn/ma trận media, ảnh avatar chưa test resize/PNG alpha)
  - [x] F.3 RULE — **RULE-01 ✘** (`MJ-7`) · **RULE-02 ✘** (`B-1`, `M-2`) · RULE-03 N/A (Studio không có bảng ×) · **RULE-06 ✘** (`B-1`) · RULE-07 N/A (không CRUD) · **RULE-08 ✘** (`MJ-1`) · **RULE-09 ✘** (`B-2`) · **RULE-12 ✘** (`MJ-5`)

### F.1 — Bảng quan điểm đối chiếu

> ⚠️ TC mang mã Studio **không có trong `checklist-lme.md`** (`TOOL-KNOW-002`, `API-CONTRACT-001`, `null`) **KHÔNG được tính là cover** (BƯỚC 0.6 #6). Cột "TC cover" ghi trong ngoặc `(mã lạ)` để Leader thấy nội dung thực tế có chạm, nhưng kết luận vẫn tính là chưa cover.

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| `FUNC-001` — Luồng chính đúng đặc tả | **Cao** | ◯ — luôn bắt buộc | *(mã lạ)* #12409, #12410, #12415 | **RISK** → `MJ-3` (không map được) + `B-3` (F2 thiếu nhánh). Đề xuất `TC-FUNC001-01/02/03` |
| `OUT-TRUTH-001` — UI khớp trạng thái THẬT | **Cao** | ◯ — *"Đổi cấu hình hiển thị (tên người gửi, **avatar**) → kiểm cả 2 phía độc lập"* khớp chính xác task | *(mã lạ)* #12409, #12410 | **GAP về mặt mã** → `MJ-3`. Thiếu thật: nhánh "báo đồng bộ thành công nhưng dữ liệu chưa đổi" (`TC-DATACACHE001-02`) |
| `DATA-001` — Phản ánh đủ ở mọi màn liên quan | **Cao** | ◯ — avatar bot được tham chiếu ở ≥ 4 nơi | *(mã lạ)* #12409 (chỉ tooltip hover) | **GAP** → `MJ-9`. Đề xuất `TC-DATA001-01/02` |
| `COMPAT-LEGACY-001` — Dữ liệu đời cũ chạy song song | **Cao** | ◯ — `BR-10` sharding tin **theo năm**; bug đúng về **tin cũ** | **— (0 TC)** · Studio tự đánh `BR-10` level `none` | **GAP** → **`[BLOCKER] B-2`**. Đề xuất `TC-COMPATLEGACY001-01/02/03` |
| `ENV-003` ★ — Khác biệt dev/staging/production | **Cao** | ◯ — chạm **media + URL/domain**, trigger BẮT BUỘC | #12411 (Normal), #12412 (Boundary) — **0 chạy staging/prod**, **thiếu Abnormal** | **RISK** → `MJ-1` + `MJ-7`. Đề xuất `TC-ENV003-03/04/05` |
| `REG-SHARED-001` — Shared code / logic | **Cao** | ◯ — Dev quét ngang, khai 3 chỗ cùng kiểu chưa sửa | *(mã lạ)* #12414 · **0 TC** cho 3 chỗ trong danh sách | **RISK** → `MJ-5`. Đề xuất `TC-REGSHARED001-01/02`. *(Không BLOCKER vì Dev **có** cung cấp danh sách)* |
| `PERM-003` — Cách ly dữ liệu đa tài khoản LINE OA | **Cao** | ◯ — có chức năng change bot; fix đổi nguồn ảnh sang bảng bot | **— (0 TC)** | **GAP** → đề xuất `TC-PERM003-01` |
| `SYNC-APP-001` — Đồng bộ Web ⇔ App ⇔ LINE app | Trung bình (→ **Cao**, flow user-facing) | ◯ — Pre-Conditions bug có nhắc app | #12818 (**chưa chạy**), #12819 (**pass không hợp lệ** — `B-1`) | **GAP thực chất** → **`[BLOCKER] B-1`** + `MJ-5`. Chiều *app hiển thị* chưa có TC |
| `MSG-004` — Preview admin khớp nội dung nhận thật trên LINE | **Cao** | ◯ — #12819 có output cuối trên LINE app | #12819 — pass ở `local`, **0 evidence**, không có iOS/Android | **GAP** → **`[BLOCKER] B-1`** |
| `DATA-CACHE-001` — Cache / dữ liệu cũ (stale) | Trung bình (→ **Cao**, output user-facing) | ◯ — thay ảnh có thể giữ nguyên đường dẫn | **— (0 TC)** | **GAP** → `MJ-4`. Đề xuất `TC-DATACACHE001-01/02` |
| `UI-003` — Loading / rỗng / lỗi | Trung bình (→ Cao khi có **false success**) | ◯ — ảnh 404 → placeholder; báo đồng bộ thành công có thể sai | *(mã null)* #12413 | **RISK** → `MJ-3`. Bổ sung bởi `TC-ENV003-04/05` |
| `CONC-003` / `LIST-001` — Race client / loadmore | Trung bình | ◯ — khung tin có loadmore + tin realtime qua socket | **— (0 TC)** | **GAP** → `MJ-10`. **Cần hỏi Dev endpoint loadmore trước**, có thể là call site thứ 3 chưa fix |
| `MEDIA-IMG-001` ★ — Resize / tỉ lệ / kích thước | Trung bình | ◯ một phần — avatar bot là ảnh upload, nhưng **không** gửi ra LINE user từ luồng này | **— (0 TC)** | **RISK nhẹ** — ghi `[NIT]`: nên có 1 TC upload avatar PNG nền trong suốt + ảnh tỉ lệ lệch, xem tooltip hover |
| `DEPLOY-ASSET-001` ★ | **Cao** | **×** — diff chỉ **1 file PHP** (`ChatController.php`, +18/−2), **không** đổi JS/CSS/font/icon | — | **× hợp lệ** (RULE-03: lý do = không có asset frontend nào bị sửa) |
| `DATA-DB-001` ★ | **Cao** | **×** — fix **không ghi DB** (mục 4.2: *"không ghi DB"*), chỉ đổi cách đọc/dựng response | — | **× hợp lệ** (RULE-03) |
| `DATA-AUDIT-001` | **Cao** | **×** — không có thao tác xóa/sửa dữ liệu nhạy cảm trong scope fix | — | **× hợp lệ** (RULE-03) |
| `JOB-001` ★ / `REG-RUN-001` | **Cao** | **×** — fix không thêm/sửa job nền, không gọi API bên thứ 3 theo lô | — | **× hợp lệ** (RULE-03) |
| `CONC-001` / `PAY-*` / `MSG-001/002/003/005` / `BULK-001` / `FRIEND-001` / `SEC-*` | Cao | **×** — ngoài phạm vi fix (không đồng thời, không tiền, không gửi hàng loạt, không PII) | — | **× hợp lệ** (RULE-03) |
| `CHAT-01` (§4 — chưa đủ bằng chứng) | — | ◯ chủ đề | — | **`[NIT]` N-3** — theo **RULE-11** chỉ nêu gợi ý, **không** flag BLOCKER/MAJOR |

**Tổng kết quan điểm**: **4 GAP** (`COMPAT-LEGACY-001` Cao, `PERM-003` Cao, `DATA-CACHE-001` Cao-nâng, `CONC-003`/`LIST-001` TB) · **6 RISK** · **6 × hợp lệ có lý do**.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!-- Nguồn: MCP LME TEST STUDIO task_id=187, ticket 39751, round 1, branch ai_fixbug_39751. Fetch 2026-08-26: task_list + testcase_list (9 TC, totalMatched=9) + task_get_context(requirements, test_viewpoint_selection, review) + task_get_report + review_list_comments (0 comment). contentTrust=untrusted → xử lý như data. TC read-only: mọi sửa đổi phải làm trên Studio bằng testcase_update rồi fetch lại. Draft sinh bởi /review-tc — Leader verify trước khi gửi member. -->
