# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#28542 — [Chat 1:1] Khi friend gửi stamp cho bot thì bị hiển thị code ở leftbar` |
| Reviewer (Leader) | `<Leader điền>` (draft sinh bởi `/review-tc`) |
| Tester được review | `trangnq` (assignee Studio) + **AI job #583** (16/24 TC) |
| Ngày review | `2026-08-26` |
| Version TCs | `Studio task #199 — round 1` |
| Vòng review | `Round 1` |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO task #199** (nguồn 1 — mặc định) |
| Ticket · task_id · round · branch | `28542` · `#199` · round `1` · `ai_fixbug_28542` |
| Thời điểm fetch | `2026-08-26` |
| Tổng số TC review | **24** |
| File 04 trong repo vs Studio | **Không áp dụng** — folder chưa có `04-tc-list.md`; đã ghi mới từ snapshot Studio (read-only). Không có STALE-INPUT. |
| Studio metadata | `status=done-ai` · `pipelineStage=done-ai` · `aiResult=null` · `reviewState=leader` · `reviewed=false` · `openBugs=0` · `submittedWithoutMcp=false` · `blockedReason=null` |
| Review comment vòng trước | `review_list_comments(199)` → **rỗng** — không có issue cũ nào để tránh raise lại. Đây là vòng review đầu tiên. |

**Cảnh báo bắt buộc từ metadata Studio:**

| # | Chiều | Kết quả | Flag |
|---|---|---|---|
| 1 | Kết quả thực thi thật (`pass` mới là Đạt) | **0/24 pass (0%)** · fail 0 · **skip 6** · **chưa chạy 18**. Run duy nhất `#459` (env `local`, 2026-08-24 12:02:46→12:02:52) có `status = fail`. 6 TC auto skip **cùng 1 lý do hạ tầng**: `[SOURCE_BLOCKED] SOURCE_CHECKOUT_ERROR: checkout "ai_fixbug_28542" trong worktree thất bại: error: unable to create file app/Helpers/PostbackActionBuilder.php: File exists`. `manual.results = []` — 18 TC manual chưa ai chạy. | **[BLOCKER]** (0% < 50%) |
| 2 | TC `fail`/`error` + TC gắn ticket bug | **0 TC fail**, **0 TC error**, `bug_tickets = []` ở cả 24 TC, `openBugs=0`. → Không có "TC fail chưa raise ticket". ⚠️ Nhưng **0 fail ở đây KHÔNG phải tín hiệu tốt** — không TC nào chạy tới nơi để có thể fail. | OK (về hình thức) / thực chất vô nghĩa |
| 3 | Môi trường đã chạy — RULE-08 / ENV-003 | `PROD 0` · `STAGING 0` · `DEV 0` · **`LOCAL 1 run` (và run đó fail)**. `envAuto`: local `runs=1`, dev/staging/prd `runs=0`. Task chạm **asset tĩnh JS phục vụ production** (bump `sns-line.version`) + phụ thuộc **job nền linect** ghi `conversation.last_message` — production tách 3 job độc lập và có **2 server loadbalance**. | **[MAJOR]** RULE-08 / ENV-003 |
| 4 | Ai chạy (`last_exec.source` / `by`) | **100% `pipeline` (AI)** — `source=ai`, `by=pipeline`, `runId=459`. **0 TC do QA người chạy.** `submittedWithoutMcp=false`. | **[MAJOR]** |
| 5 | Tác giả TC (`provenance.source`) | **AI 16/24 (66.7%)** — `provenance.source=ai`, `actor=AI`, `created_job_id=583`. **QA `trangnq@mcp` 8/24 (33.3%)** — `provenance.source=human`. Human trực tiếp trên Studio: **0**. `reviewState=leader` (**chưa `done`**). | **[MAJOR]** (≥50% AI + review chưa done) |
| 6 | Mã quan điểm Studio KHÔNG có trong `checklist-lme.md` | **3 mã / 4 lượt TC**: `TOOL-KNOW-002` (#12535) · `API-CONTRACT-001` (#12544) · `TOOL-ERRHYG-001` (#12545, #13490). **Không tính là cover** ở §3 / §7 F.1. Nghiêm trọng nhất: **#12535 là TC tái hiện bug gốc** nhưng mang mã nội bộ Studio. | **[MAJOR]** |

> Đã grep đối chiếu `framework/checklist-lme.md`: 7 mã hợp lệ (`OUT-TRUTH-001`, `FUNC-004`, `UI-003`, `CONC-003`, `DEPLOY-ASSET-001`, `DATA-CACHE-001`, `SEC-001`) / 3 mã không hợp lệ.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC có **chất lượng nội dung khá tốt** (tách đúng từng message type, có TC race client-side, có TC cross-bot security, có baseline page-load) nhưng **0/24 TC được thực thi thành công** — nên chưa có bất kỳ kết luận test nào. Ngoài ra thiếu 4 mảng coverage bắt buộc: **REG-SHARED-001** (không có danh sách caller của `/ajax/get-badge`), **PERM-003** (luồng change bot — chính là nguồn của `getBotId()` vừa được thêm vào query), **màn FA-002 Talk Management** (Dev đánh giá High risk nhưng chỉ có TC tầng API), và **COMPAT-LEGACY-001** (nhánh dữ liệu/định dạng type cũ).

---

## 2. Tóm tắt cho member

Bộ TC này viết **chắc tay hơn mặt bằng chung**: tách riêng oracle cho từng loại tin (stamp/ảnh/video/audio/vị trí/file) thay vì gộp 1 TC, có TC race ở tầng client với hai output khác nhau để phát hiện swap, và giữ được TC baseline cho đường page-load — đúng tinh thần "verify cả đường cũ vẫn đúng". 8 TC bạn (`trangnq`) bổ sung qua MCP cũng đúng hướng tách case.

Ba việc phải fix trước vòng sau: (1) **chạy TC thật** — hiện 0/24 pass, 6 TC auto bị chặn ở bước checkout branch (lỗi hạ tầng, không phải kết quả test) và 18 TC manual chưa ai chạy, nên toàn bộ report này mới chỉ đánh giá được *TC viết đủ hay chưa*, chưa nói được gì về *fix có đúng không*; (2) **bổ sung 4 mảng coverage bắt buộc** ở §5 — đặc biệt là luồng **đổi bot** (filter `bot_id = getBotId()` lấy từ session, mà chưa TC nào chạm) và **màn Talk Management FA-002** mà chính Dev liệt kê là ảnh hưởng High; (3) **archive 2 TC trùng** (`#13491` trùng `#12541`, `#13492` trùng `#13489`) và đổi mã quan điểm cho 4 TC đang mang mã nội bộ Studio.

---

## 3. Coverage Matrix

> Cột `Exec` = `<số pass>/<số TC>`. Vì **0 TC nào pass**, mọi impact có TC đều rơi về `RISK` — "có TC ≠ đã test".

| Impact | Loại | TCs cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — switch so khớp `e.type` bằng **chuỗi** trong khi `messages_v2s.type` là **số** → rơi nhánh default → in raw JSON | Root cause | TC-TOOLKNOW002-01 (#12535) · TC-OUTTRUTH001-08 (#12546, static) · TC-OUTTRUTH001-10 (#12549, baseline page-load) | 3 | 0/3 | **RISK** |
| **F1** — socket handler `message.to.<bot>` (`chat-v2.js`) | Function Direct | TC-TOOLKNOW002-01 · TC-OUTTRUTH001-01…06 · TC-FUNC004-01 | 8 | 0/8 | **RISK** |
| **F2** — nhánh hội thoại **đang mở** | Function Direct | TC-TOOLKNOW002-01 · TC-OUTTRUTH001-01…06 · TC-FUNC004-01 | 8 | 0/8 | **RISK** |
| **F3** — nhánh hội thoại **KHÔNG mở** (callback `/ajax/get-badge`) | Function Direct | TC-OUTTRUTH001-07 · TC-UI003-01/02/03 · TC-CONC003-01/02/03 · TC-OUTTRUTH001-09 (static) | 8 | 0/8 | **RISK** |
| **F4** — `ChatController::getBadge` trả thêm `last_message` | Function Direct | TC-APICONTRACT001-01 (#12544) | 1 | 0/1 | **RISK** ⚠️ mã ngoài checklist → không tính cover ở F.1 |
| **F5** — `getBadge` thêm filter `bot_id = getBotId()` | Function Direct | TC-SEC001-01 (#12543) | 1 | 0/1 | **RISK** — chỉ 1 Abnormal, thiếu Normal + Boundary (RULE-01) |
| **F6** — bảng mã type dùng chung `config/sns-line.php` | Function Direct | TC-OUTTRUTH001-08 (static) · TC-OUTTRUTH001-06 (loại lạ) | 2 | 0/2 | **RISK** |
| **F7** — `ChatController::getMessageSocket` | Function Indirect | (không TC riêng — hợp lý, không sửa code) | 0 | — | OK (Indirect) |
| **F8** — `ConversationService::getFriend` (page-load) | Function Indirect | TC-OUTTRUTH001-10 (#12549) | 1 | 0/1 | **RISK** |
| **F9** — bump version static asset | Function Direct | TC-DEPLOYASSET001-01 (static) · TC-DATACACHE001-01 | 2 | 0/2 | **RISK** |
| **D1** — *(Dev ghi: không có data ghi/đổi)* | Data | — | — | — | OK (× có lý do) |
| **D2** — `conversations.last_message` (READ) | Data | TC-OUTTRUTH001-07/10 · TC-APICONTRACT001-01 | 3 | 0/3 | **RISK** |
| **D3** — `messages_v2s.type` `int(11)` (READ) | Data | TC-OUTTRUTH001-08 (static) | 1 | 0/1 | **RISK** — không TC runtime nào chứng minh type số đi đúng nhánh trên dữ liệu thật |
| **D4** — **contract `/ajax/get-badge` đổi** (thêm `last_message`) | Data/API | TC-APICONTRACT001-01 | 1 | 0/1 | **RISK** — không TC nào rà **caller khác** của endpoint (xem GAP-1) |
| **T1** — 1-on-1 Chat (FA-001) realtime label | Feature High | 16 TC (toàn bộ nhóm leftbar) | 16 | 0/16 | **RISK** |
| **T2** — **Chat / Talk Management (FA-002)** | Feature High | Chỉ TC-APICONTRACT001-01 ở **tầng API**. **0 TC ở tầng UI của màn FA-002.** | 1 | 0/1 | **GAP** (tầng UI) |
| **T3** — phân quyền cross-bot trên `/ajax/get-badge` | Feature High | TC-SEC001-01 | 1 | 0/1 | **RISK** |
| **T4** — badge **số tin chưa đọc** ở leftbar/menu | Feature Medium | TC-CONC003-02 (chỉ kiểm *không nhầm hội thoại*) | 1 | 0/1 | **GAP** — không TC nào verify **giá trị `confirm_count` vẫn đúng** sau khi thêm `where bot_id` |
| **T5** — cache static asset JS phía browser | Feature Medium | TC-DEPLOYASSET001-01 · TC-DATACACHE001-01 | 2 | 0/2 | **RISK** |

### GAP tổng hợp (đưa vào §5)

| GAP | Nội dung | Quan điểm | Ưu tiên |
|---|---|---|---|
| **GAP-1** | Không có TC rà **caller khác** của `/ajax/get-badge` và `chat-v2.js` (code dùng chung, đa brand Lme/Lwaka/Saruwaka/Lgram) — Dev không cung cấp danh sách nơi ảnh hưởng | `REG-SHARED-001` | **Cao** |
| **GAP-2** | Không có TC luồng **đổi bot / đa LINE OA** — trong khi filter mới lấy `bot_id` từ **session** (`getBotId()`) | `PERM-003` | **Cao** |
| **GAP-3** | Không có TC **tầng UI** cho màn **FA-002 Talk Management** (Dev đánh giá High risk) | `DATA-001` / `OUT-TRUTH-001` | **Cao** |
| **GAP-4** | Không có TC **dữ liệu / payload định dạng cũ** — socket payload `type` dạng chuỗi (producer cũ), conversation cũ chưa có `last_message` | `COMPAT-LEGACY-001` | **Cao** |
| **GAP-5** | Không có TC chạy **production** (2 router loadbalance, job nền tách 3, asset qua domain thật) | `ENV-003` | **Cao** |
| **GAP-6** | `SEC-001` chỉ có Abnormal; thiếu Normal + Boundary; thiếu chiều **URL trực tiếp** và **export** | `SEC-001` | **Cao** |
| **GAP-7** | `CONC-003` chỉ có Abnormal; thiếu Normal (nhiều tin **đúng thứ tự**) + Boundary (số hội thoại cập nhật đồng thời ở ngưỡng lớn) | `CONC-003` | **Cao** |
| **GAP-8** | Không có TC **2 tab cùng user** / **2 tài khoản trên cùng browser** — leftbar tải nhiều hội thoại đồng thời | `SEC-ISO-001` | **Cao** |
| **GAP-9** | Không có TC verify **giá trị badge/confirm_count** đúng sau khi thêm `where bot_id` (regression đếm số) | `DATA-001` | **Cao** |
| **GAP-10** | `DEPLOY-ASSET-001` thiếu Boundary — không TC nào soi **404 asset / font fallback** sau khi bump version | `DEPLOY-ASSET-001` | **Cao** |

### ORPHAN TCs

| TC No. | Studio | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC-OUTTRUTH001-08 | #12546 | "Kiểm tra tĩnh" — **đọc source code**, không phải quan sát UI của manual tester. Không thể fail theo cách phản ánh hành vi người dùng. | **Giữ** nhưng đánh dấu `static-check`, **KHÔNG tính vào coverage**. Không thay thế TC runtime. |
| TC-OUTTRUTH001-09 | #12547 | như trên | như trên |
| TC-DEPLOYASSET001-01 | #12548 | như trên | như trên |
| TC-CONC003-03 | #13491 | **Trùng nội dung** TC-CONC003-01 (#12541) — cùng kịch bản Y stamp / Z ảnh / callback đảo thứ tự. Tạo lúc 04:12 trong khi #12541 đã được cập nhật lên v2 lúc 03:54 cùng ngày. | **Archive #13491** trên Studio (`testcase_delete` / archive), giữ #12541. |
| TC-UI003-03 | #13492 | **Trùng nội dung** TC-UI003-02 (#13489) — cùng kịch bản get-badge timeout/5xx giữ content cũ. Tạo lúc 04:12, #13489 tạo lúc 03:58 cùng ngày. | **Archive #13492**, giữ #13489 (có mapping REQ-005 ở note). |

> Không TC nào lạc chủ đề hoàn toàn — 3 TC static là bổ trợ hợp lệ, chỉ không được **thay** TC runtime (AP-5).

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| **Fix shape** (đọc mục 2 dev-impact) | **3 shape cùng lúc**: (a) **Sửa hàm/config dùng chung** — đổi so khớp type sang bảng mã số `config/sns-line.php`; (b) **Race condition (client-side)** — bỏ 3 dòng tính lại index trong callback bất đồng bộ, dùng biến cục bộ; (c) **JS/asset** — bump `sns-line.version` để cache-bust. Kèm 1 **vá phân quyền** (`where bot_id = getBotId()`). |
| **Trigger space cần cover** | **(a)** 6 loại tin có nhánh riêng (sticker=5, image=2, video=3, audio=4, file=12, location=13) + text (default) + **≥1 loại KHÔNG có trong map** (image_map/pdf/loại LINE mới) + **payload type dạng chuỗi từ producer cũ** = **9 trigger**. **(b)** 4 kịch bản race client (CONC-003): chuyển tab nhanh · response về sai thứ tự · throttling Slow 3G · filter/search liên tiếp. **(c)** F5 thường trên browser còn cache + Network 200 với query mới + không 404 + font không fallback. |
| **Số trigger TCs hiện cover** | **(a) 8/9** — thiếu **payload type dạng chuỗi (định dạng cũ)**. **(b) 2/4** — có "response sai thứ tự" (#12541) và "chuyển hội thoại trước khi callback về" (#12542); **thiếu** throttling Slow 3G toàn luồng và filter/search liên tiếp trên leftbar. **(c) 2/4** — thiếu kiểm 404 asset và font fallback. |
| **KH report dạng** | **Symptom-only có kèm bằng chứng** — KH (`Ngô Thúy Ngần`) ghi "hiển thị code ở leftbar" + "phải reload lại màn hình mới hiển thị đúng last message kiểu stamp" + 2 screenshot. **Không có** error code / log / request-response. |
| **Alternative root causes cần verify** | (1) `conversation.last_message` **chưa kịp được job linect ghi** khi socket bắn tới → nhánh nào cũng lấy phải giá trị chưa chuẩn hoá; (2) LINE thêm **loại tin mới** chưa có trong `type_message_v2` → rơi nhánh default in raw (TC-OUTTRUTH001-06 chạm nhẹ, **oracle chưa chốt**); (3) producer socket bản cũ vẫn gửi `type` **dạng chuỗi** → code mới (so khớp số) không match → tái xuất bug ở nhánh ngược lại. |
| **Anti-patterns dính** | **AP-2** (symptom-only) · **AP-3** (happy-path-only regression cho T4/T5) · **AP-5** (3 TC static không thay được TC runtime — cảnh báo, chưa nghiêm trọng). **Không dính** AP-1 (fix không phải generic catch), **không dính** AP-4 (có commit `c045b0894f` + branch để trace), **không dính** AP-6 (mục 3 dev-impact có 6 dòng caller). |

> ⚠️ **Điểm adversarial quan trọng nhất**: Studio `REQ-004` ghi nguyên văn *"phần confirm_count/block_status **còn rủi ro dùng biến toàn cục cần xác nhận**"*. Nghĩa là chính hệ thống sinh TC đã đánh dấu **fix có thể chưa đóng hết race** — Dev chỉ sửa đường gán `content`, còn `confirm_count`/`block_status` trong cùng callback thì chưa. TC duy nhất chạm điểm này (**TC-CONC003-02 / #12542**) **chưa chạy lần nào**. Đây là TC phải chạy đầu tiên ở vòng sau.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] EXEC-01 (toàn bộ 24 TC)**: **0/24 pass (0%)**. Run duy nhất `#459` có `status=fail`; 6 TC auto đều `skip` với cùng lỗi hạ tầng `[SOURCE_BLOCKED] SOURCE_CHECKOUT_ERROR: checkout "ai_fixbug_28542" ... unable to create file app/Helpers/PostbackActionBuilder.php: File exists`; 18 TC manual **chưa ai chạy** (`manual.results = []`). — **Đề xuất fix**: dọn worktree runner (xoá file rác `app/Helpers/PostbackActionBuilder.php` hoặc `git worktree prune` trước checkout) rồi chạy lại run auto; song song QA chạy tay tối thiểu 5 TC ưu tiên: `#12535` (tái hiện bug) · `#12542` (race confirm_count) · `#12539` (hội thoại không mở) · `#12543` (cross-bot) · `#12550` (cache asset). **Không được kết luận "fix OK" từ trạng thái hiện tại.**

- **[BLOCKER] GAP-1 · FIX-SHAPE (REG-SHARED-001, Cao)**: fix sửa **code dùng chung** — `ChatController::getBadge` (endpoint `/ajax/get-badge`) đổi **contract response** (+`last_message`) **và** siết query bằng `where bot_id = getBotId()`; `public/js/chats/chat-v2.js` là JS dùng chung của màn chat. Dev **không cung cấp danh sách nơi ảnh hưởng** — mục 3 chỉ liệt kê 6 function trong chính luồng này. **0 TC** nào rà caller khác của `/ajax/get-badge` (màn Talk Management, badge ở header/menu, mobile app, và các brand dùng chung codebase **Lme / Lwaka / Saruwaka / Lgram**). — **Đề xuất fix**: yêu cầu Dev grep toàn repo `get-badge` + `getBadge` và trả về danh sách caller; mỗi caller → 1 TC regression (§5 `TC-REGSHARED001-01/02/03`). Rủi ro cụ thể: caller nào đang **cố tình** truy vấn conversation khác bot sẽ **im lặng nhận `confirm_count=0`** sau fix.

- **[BLOCKER] GAP-2 (PERM-003, Cao)**: filter mới lấy bot từ **session** (`getBotId()`), nhưng **0 TC** chạm luồng **đổi bot / đa LINE OA** — trigger bắt buộc của `PERM-003`. Kịch bản hỏng cụ thể: user mở màn Chat 1:1 của bot A ở tab 1, **đổi sang bot B ở tab 2** → session đổi → mọi request `get-badge` từ tab 1 (vẫn là conversation của bot A) sẽ trả `last_message=null`, `confirm_count=0` → **leftbar tab 1 âm thầm ngừng cập nhật**, đúng vào nhánh "giữ nguyên nội dung cũ" mà TC-UI003-01 coi là ĐẠT. — **Đề xuất fix**: thêm 3 TC `TC-PERM003-01/02/03` (§5).

- **[BLOCKER] GAP-3 (T2 — FA-002 Talk Management)**: Dev liệt kê ở mục 4.3 nguyên văn *"Chat / Talk Management (FA-002) — phản hồi `/ajax/get-badge` bổ sung trường `last_message` dùng cho danh sách hội thoại"* với **nguy cơ High**, nhưng toàn bộ 24 TC đều có `screen` thuộc **màn Chat 1:1**; màn FA-002 chỉ được chạm ở **tầng API** (`#12544`). — **Đề xuất fix**: thêm `TC-OUTTRUTH001-11/12` (§5) chạy đúng trên màn Talk Management, hoặc yêu cầu Dev xác nhận bằng văn bản rằng FA-002 **không** render `last_message` từ `get-badge` (nếu vậy sửa lại mục 4.3).

### 4.2 Major (nên fix)

- **[MAJOR] ENV-03 (RULE-08 / ENV-003, Cao)**: 0 TC chạy production; run duy nhất ở `local` và fail. Task chạm **asset tĩnh phục vụ production** (bump version JS) và phụ thuộc **job nền linect** ghi `conversation.last_message`. Theo Catalog D, production **tách 3 job độc lập** (khác dev/staging chạy 1 job all) và có **2 server loadbalance** → hành vi cache-bust và thời điểm `last_message` sẵn sàng **không suy ra được từ local/staging**. — **Đề xuất fix**: `TC-ENV003-01/02` (§5); tối thiểu chạy TC cache-asset và TC hội-thoại-không-mở trên production theo **từng router**.

- **[MAJOR] GAP-4 (COMPAT-LEGACY-001 / RULE-09, Cao)**: fix **đảo chiều** so khớp từ chuỗi → số. Dev ghi *"bảng tin nhắn **bản mới** lưu loại tin bằng SỐ"* — hàm ý tồn tại định dạng cũ. Nếu còn producer socket (linect bản cũ, hoặc luồng khác) gửi `type` **dạng chuỗi**, code mới sẽ **không match** và bug tái xuất ở nhánh ngược lại. Cũng chưa có TC cho **conversation cũ có `last_message = null`** (tạo trước khi job chuẩn hoá tồn tại). — **Đề xuất fix**: `TC-COMPATLEGACY001-01/02/03` (§5).

- **[MAJOR] RULE-01 · SEC-001 (Cao)**: chỉ **1 TC Abnormal** (`#12543`). Thiếu **Normal** (bot đúng → trả đúng `last_message`; hiện chỉ có `#12544` nhưng mang mã `API-CONTRACT-001` **ngoài checklist** nên không tính) và thiếu **Boundary**. Ngoài ra `SEC-001` yêu cầu thử cross-account qua **URL trực tiếp, API, VÀ file export** — hiện chỉ có API. — **Đề xuất fix**: đổi mã `#12544` thành `SEC-001` (hoặc `PERM-002`) + thêm `TC-SEC001-02/03` (§5).

- **[MAJOR] RULE-01 · CONC-003 (Cao — vì leftbar có loadmore + filter và nhiều hội thoại cùng gọi API)**: 3 TC nhưng **2 trùng nhau**, thực chất còn **2 kịch bản** và **cả 2 đều Abnormal**. Thiếu **Normal** (nhiều tin đến đúng thứ tự → tất cả row đúng) và **Boundary** (nhiều hội thoại cập nhật đồng thời ở ngưỡng lớn). Cũng thiếu 2/4 chiều của `CONC-003`: throttling Slow 3G chạy lại luồng chính, và bấm filter/search liên tiếp. — **Đề xuất fix**: `TC-CONC003-04/05` (§5).

- **[MAJOR] GAP-8 (SEC-ISO-001, Cao)**: trigger nguyên văn *"BẮT BUỘC khi UI tải/hiển thị nhiều đối tượng dữ liệu đồng thời (**nhiều cuộc trò chuyện**, nhiều tab)"* — mô tả đúng leftbar này. Mã `SEC-ISO-001` **chỉ xuất hiện ở trường `note`** của `#12541`/`#13491`, **không ở cột `viewpoint`** → `/review-tc` không map được. Nội dung TC có chạm isolation giữa 2 conversation nhưng **thiếu hẳn** 2 tầng mà quan điểm yêu cầu: **2 tab cùng user** và **2 tài khoản trên cùng browser**. — **Đề xuất fix**: gắn `SEC-ISO-001` làm viewpoint phụ trên Studio + thêm `TC-SECISO001-01/02` (§5).

- **[MAJOR] GAP-9 (DATA-001, Cao)**: `getBadge` vừa bị siết `where bot_id`, nhưng **không TC nào verify giá trị `confirm_count` / badge số chưa đọc vẫn ĐÚNG** cho bot hiện tại. `#12544` chỉ kiểm **có mặt** field, `#12542` chỉ kiểm **không nhầm hội thoại**. Nếu `getBotId()` trả sai trong một ngữ cảnh nào đó (staff phụ, bot vừa switch) → badge về 0 hàng loạt mà không TC nào bắt được. — **Đề xuất fix**: `TC-DATA001-01` (§5).

- **[MAJOR] GAP-10 (RULE-01 · DEPLOY-ASSET-001, Cao)**: có Normal (`#12548`, static) + Abnormal (`#12550`), **thiếu Boundary**. Cũng thiếu 2 chiều bắt buộc của quan điểm: **Network tab không có asset 404** và **font không fallback** sau khi đổi query version. — **Đề xuất fix**: `TC-DEPLOYASSET001-02` (§5).

- **[MAJOR] VP-01 — mã quan điểm ngoài checklist (0.6 #6)**: 4 TC mang mã nội bộ Studio, **không tính là cover**: `#12535 → TOOL-KNOW-002`, `#12544 → API-CONTRACT-001`, `#12545`/`#13490 → TOOL-ERRHYG-001`. Nghiêm trọng nhất là **`#12535` — TC tái hiện bug gốc** — khiến quan điểm chính của ticket không map được. — **Đề xuất fix** (sửa trên Studio bằng `testcase_update`, KHÔNG sửa file 04): `#12535 → OUT-TRUTH-001` · `#12544 → SEC-001` (hoặc `PERM-002`) · `#12545`, `#13490 → UI-003` (hoặc `FUNC-002` nếu coi là thiếu tham số bắt buộc).

- **[MAJOR] SPEC-01**: **toàn bộ 24 TC có `spec_status = null`** (cột `Trạng thái đánh giá spec` trống). Trong khi đó chính TC `#12545`/`#13490` ghi *"endpoint `/ajax/get-badge` hiện chưa có contract/EP chính thức trong spec"*, và `#12543` ghi *"Endpoint không có mã EP spec — expected suy từ diff code"*. Nguy cơ: tester tự suy diễn oracle rồi cho Đạt. — **Đề xuất fix**: điền `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader` cho từng TC; 3 TC nêu trên phải là `Đã hỏi leader` kèm tên người trả lời. Xem thêm §6.

- **[MAJOR] AUTHOR-01 (0.6 #4 + #5)**: **16/24 (66.7%) TC do AI sinh** (job #583) trong khi `reviewState` mới ở `leader`, **chưa `done`**; và **0 TC do QA người chạy** — 100% execution là `pipeline`. Kết hợp với việc run đó fail toàn bộ, hiện **chưa có mắt người nào** xác nhận cả TC lẫn kết quả. — **Đề xuất fix**: Leader duyệt xong đặt `reviewState=done`; QA chạy tay tối thiểu nhóm TC ưu tiên ở EXEC-01.

- **[MAJOR] [AP-2] SYMPTOM-ONLY**: KH chỉ mô tả triệu chứng ("hiển thị code ở leftbar", "phải reload mới đúng"), không có error code/log. Dev tái hiện **1 root cause** (int vs string). TCs bám sát root cause đó. — **Đề xuất fix**: hỏi Dev 2 câu — (1) *thời điểm* socket bắn so với lúc job linect ghi `last_message`, có khoảng nào socket tới trước không? (2) LINE có loại tin nào **mới** chưa nằm trong `type_message_v2` không? Rồi bổ sung TC cho ≥2 root cause (TC-COMPATLEGACY001-02 ở §5 đã lấp 1 phần).

- **[MAJOR] [AP-3] Happy-path-only regression cho T4 / T5**: mỗi feature chỉ 1–2 TC với precondition "dữ liệu sạch". Không TC nào chạy regression ở **trạng thái biên**: bot có 0 hội thoại, hội thoại đã bị ẩn (`is_hide=1`), friend đã block, hội thoại ở trang 2+ của loadmore. — **Đề xuất fix**: bổ sung precondition biên vào `TC-DATA001-01` và `TC-CONC003-05` (§5).

### 4.3 Minor (có thể fix sau)

- **[MINOR] DUP-01**: 2 cặp TC trùng nội dung — `#13491 (NEW-23)` trùng `#12541 (NEW-7)`; `#13492 (NEW-24)` trùng `#13489 (NEW-21)`. Cả 2 TC trùng đều tạo lúc `2026-08-26 04:12:59`, sau bản gốc 14–18 phút → nhiều khả năng đã áp dụng cùng 1 gợi ý review 2 lần. — **Đề xuất fix**: archive `#13491` và `#13492` trên Studio; giữ `#12541`, `#13489`.

- **[MINOR] REQ-01**: **8/8 TC do QA `trangnq` thêm đều có `requirement_keys` rỗng** (`#13485`–`#13492`), dù nội dung rõ ràng thuộc REQ-001/004/005. Hệ quả: báo cáo coverage của Studio không quy được các TC này về REQ nào. — **Đề xuất fix**: gán `requirement_keys` khi `testcase_update`.

- **[MINOR] ORACLE-01**: 3 TC có oracle chưa chốt — `#12538` (*"cần dev/LINE integration xác nhận"*), `#12545` và `#13490` (*"HTTP status/body cụ thể cần đối chiếu contract endpoint khi được xác nhận"*). TC không có oracle dứt khoát thì **không thể tick Đạt/Không đạt**. — **Đề xuất fix**: chốt câu trả lời trước khi chạy, cập nhật `expected`, ghi người trả lời vào `Ghi chú`.

- **[MINOR] AP-5 / STATIC-01**: 3 TC "Kiểm tra tĩnh" (`#12546`, `#12547`, `#12548`) là **đọc source code**, không phải TC từ góc nhìn manual tester. Chúng chiếm 3/6 slot auto và đã tiêu tốn lần chạy duy nhất. — **Đề xuất fix**: giữ nhưng đánh dấu `static-check`, **không tính vào coverage** và không dùng để thay TC runtime tương ứng.

- **[MINOR] NUM-01**: `TC No.` trên Studio dùng `temp_id` dạng `NEW-1`…`NEW-24`, không theo quy ước repo `TC-<mã quan điểm bỏ gạch>-<nn>`. File 04 trong repo đã đánh lại đúng quy ước và giữ `Studio #<id> (<temp_id>)` ở `Ghi chú` để trace ngược.

### 4.4 Nit (gợi ý)

- **[NIT] PR-01**: mục "Commit / Pull Request" của `03-dev-impact.md` có commit `c045b0894f` + branch `ai_fixbug_28542` (đủ để trace) nhưng **không có link PR**. Có link PR thì reviewer đọc diff nhanh hơn, đỡ phải checkout.

- **[NIT] COV-01**: Studio báo `coverage 0/93` — toàn bộ `EP-01…EP-49` và `BR-01…BR-17` của feature `chat-1on1` đều `none`, chỉ `SCR-CHT-01` ở mức `partial`. Với task fix-bug thì không cần phủ hết feature, nhưng đáng lưu ý: **`/ajax/get-badge` chưa có mã EP nào** trong spec chat-1on1 → xem §6.

- **[NIT] VERIFY-01**: 2 checkbox "Tester verify auto-fill chính xác" ở `01-bug-task.md` và `03-dev-impact.md` **chưa tick**. Nội dung 2 file được auto-fill từ Redmine bởi `/new-task` — theo quy trình phải có tester đọc lại Redmine và xác nhận trước khi review có hiệu lực. (Không nâng lên MAJOR vì reviewer đã đối chiếu trực tiếp với journal Redmine `#132530` trong vòng review này.)

---

## 5. TCs đề xuất bổ sung

> 21 TC lấp GAP-1 → GAP-10. Copy thẳng vào `04-tc-list.md` round sau, hoặc tạo trên Studio bằng `testcase_create`. `TC No.` đã tránh trùng với 24 TC hiện có.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Rà từng màn/nút gọi `/ajax/get-badge` theo danh sách Dev cung cấp → tất cả vẫn hiển thị đúng badge và tin cuối | Có **danh sách nơi gọi `/ajax/get-badge` do Dev cung cấp** (bắt buộc, chưa có thì không chạy được TC này). Đăng nhập bot A có ≥3 hội thoại, ≥1 hội thoại chưa đọc. | 1. Yêu cầu Dev gửi danh sách màn/JS gọi `/ajax/get-badge`<br>2. Với TỪNG mục trong danh sách, mở màn đó trên browser<br>3. Cho friend gửi 1 stamp để kích hoạt cập nhật<br>4. Quan sát badge số chưa đọc + dòng tin cuối tại màn đó<br>5. Mở DevTools > Network, xác nhận request `/ajax/get-badge` trả 200 và có field `last_message` | Danh sách caller do Dev cung cấp; friend gửi 1 stamp | Mọi màn trong danh sách hiển thị badge số chưa đọc đúng và (nếu màn đó có cột tin cuối) hiển thị 「【スタンプ】」. Không màn nào mất badge, về 0 sai, hoặc hiển thị JSON thô. | Chưa test | | STAGING + PRD | | | | Đã hỏi leader | Lấp **GAP-1** · cover **D4, F4, F5, T2** · Evidence bắt buộc (RULE-02): danh sách caller Dev cung cấp + screenshot từng màn + ảnh Network tab |
| TC-REGSHARED001-02 | REG-SHARED-001 | Abnormal | Caller cũ gọi `/ajax/get-badge` với hội thoại KHÔNG thuộc bot đang đăng nhập → xác nhận hành vi mới có làm hỏng màn nào không | Danh sách caller từ Dev. Có 2 bot A và B cùng thuộc 1 tài khoản quản lý nhiều LINE OA. Đăng nhập chọn bot A. | 1. Với từng caller trong danh sách, dựng tình huống màn đó tham chiếu tới hội thoại thuộc **bot B**<br>2. Thực hiện thao tác khiến màn gọi `/ajax/get-badge`<br>3. Quan sát màn hình và Network response | conversation_id thuộc bot B, session đang ở bot A | Không màn nào hiển thị sai lệch **âm thầm**: hoặc màn đó không bao giờ tham chiếu chéo bot (Dev xác nhận), hoặc phải báo trạng thái rõ ràng. Tuyệt đối không được hiện badge = 0 / tin cuối trống như thể "đã đọc hết" trong khi thực tế có tin chưa đọc. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-1** · cover **F5, T3** · rủi ro chính: filter `bot_id` mới làm caller cũ nhận `confirm_count=0` mà không có tín hiệu lỗi |
| TC-REGSHARED001-03 | REG-SHARED-001 | Boundary | Chức năng tương tự trên các brand dùng chung codebase (Lwaka / Saruwaka / Lgram) → leftbar hiển thị đúng nhãn tin cuối | Có tài khoản test trên các brand dùng chung `chat-v2.js` / `ChatController` mà Dev xác nhận là bị ảnh hưởng. | 1. Hỏi Dev brand nào dùng chung file đã sửa<br>2. Với từng brand được xác nhận, đăng nhập và mở màn chat<br>3. Cho friend gửi stamp và ảnh<br>4. Quan sát leftbar realtime, không reload | Mỗi brand: 1 stamp + 1 ảnh | Mọi brand dùng chung code đều hiển thị 「【スタンプ】」/「【画像】」 đúng. Không brand nào còn hiện JSON thô, cũng không brand nào ngừng cập nhật realtime. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-1** · `REG-SHARED-001` yêu cầu rà brand Lme/Lwaka/Saruwaka/Lgram · nếu Dev xác nhận brand khác KHÔNG dùng chung → ghi × kèm tên người xác nhận (RULE-03) |
| TC-PERM003-01 | PERM-003 | Normal | Đổi bot rồi mở lại Chat 1:1 → leftbar cập nhật realtime đúng cho bot mới | Tài khoản quản lý ≥2 LINE OA (bot A và bot B), mỗi bot có ≥1 hội thoại 1:1 với friend riêng. | 1. Đăng nhập, chọn bot A, mở màn Chat 1:1<br>2. Dùng chức năng đổi bot sang bot B<br>3. Mở màn Chat 1:1 của bot B<br>4. Cho friend của bot B gửi 1 stamp<br>5. Quan sát leftbar, không reload | Friend của bot B gửi 1 stamp | Leftbar của bot B cập nhật realtime thành 「【スタンプ】」. Danh sách hội thoại chỉ chứa friend của bot B, không lẫn hội thoại của bot A. | Chưa test | | STAGING + PRD | | | | Spec không ghi | Lấp **GAP-2** · cover **F5, T3** · `PERM-003` trigger: có chức năng change bot |
| TC-PERM003-02 | PERM-003 | Abnormal | Đổi bot ở tab 2 trong khi tab 1 đang mở Chat 1:1 của bot cũ → tab 1 không được âm thầm ngừng cập nhật | Tài khoản quản lý bot A và bot B. Mở 2 tab trên cùng browser (chung session). | 1. Tab 1: chọn bot A, mở màn Chat 1:1, ghi nhớ nội dung dòng tin cuối của 1 hội thoại<br>2. Tab 2: đổi bot sang bot B<br>3. Quay lại tab 1 (KHÔNG reload)<br>4. Cho friend của bot A gửi 1 stamp<br>5. Quan sát dòng leftbar ở tab 1 và Network response của `/ajax/get-badge` | Friend của bot A gửi 1 stamp trong lúc session đã chuyển sang bot B | Tab 1 **không được** giữ nội dung cũ như thể bình thường. Phải có tín hiệu rõ ràng cho người dùng (thông báo phiên đã đổi bot / yêu cầu tải lại / tự đồng bộ đúng bot). Nếu `get-badge` trả `last_message=null, confirm_count=0` mà UI im lặng → **Không đạt**, raise ticket. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-2** · cover **F5, T3, T4** · ⚠️ đây là kịch bản hỏng có xác suất cao nhất do `getBotId()` lấy từ session; hiện `TC-UI003-01` sẽ coi trạng thái này là ĐẠT |
| TC-PERM003-03 | PERM-003 | Boundary | Tài khoản quản lý số bot ở ngưỡng lớn nhất thực tế → đổi bot liên tiếp, leftbar luôn khớp bot đang chọn | Tài khoản test có số LINE OA bằng hoặc lớn hơn khách hàng lớn nhất hiện tại (hỏi CS/Dev con số này). Mỗi bot có ≥1 hội thoại có tin chưa đọc. | 1. Xác nhận số bot tối đa 1 tài khoản đang quản lý trên production<br>2. Dựng tài khoản test đạt ngưỡng đó<br>3. Đổi bot liên tiếp qua ≥5 bot, mỗi lần mở màn Chat 1:1<br>4. Ở mỗi bot, cho 1 friend gửi stamp và quan sát leftbar<br>5. Ghi lại badge số chưa đọc ở mỗi bot | Số bot = ngưỡng thực tế lớn nhất; mỗi bot 1 stamp | Mỗi lần đổi bot, leftbar hiển thị đúng hội thoại và badge của **bot đang chọn**, cập nhật realtime đúng nhãn. Không có hiện tượng dữ liệu bot trước còn sót lại sau khi đổi. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-2** · hoàn thiện RULE-01 cho `PERM-003` (Cao → đủ 3 loại case) · ghi rõ nguồn ngưỡng số bot ở `Evidence` |
| TC-OUTTRUTH001-11 | OUT-TRUTH-001 | Normal | Màn Talk Management (FA-002): friend gửi stamp → danh sách hội thoại hiển thị đúng 【スタンプ】 | Đăng nhập bot A, mở màn **Talk Management (FA-002)**, không mở màn Chat 1:1. | 1. Mở màn Talk Management<br>2. Từ LINE của friend, gửi 1 stamp cho bot<br>3. Quan sát dòng hội thoại của friend trong danh sách, KHÔNG reload<br>4. Mở DevTools > Network xem response `/ajax/get-badge` có field `last_message` | Friend gửi 1 stamp | Dòng hội thoại ở màn Talk Management hiển thị 「【スタンプ】」, không hiện JSON/code thô, cập nhật không cần reload. | Chưa test | | STAGING + PRD | | | | Đã hỏi leader | Lấp **GAP-3** · cover **T2 (Dev đánh giá High)** · nếu màn FA-002 KHÔNG render `last_message` → ghi × và yêu cầu Dev sửa lại mục 4.3 dev-impact |
| TC-OUTTRUTH001-12 | OUT-TRUTH-001 | Abnormal | Màn Talk Management và màn Chat 1:1 mở cùng lúc trên 2 tab → cả 2 hiển thị cùng một nội dung tin cuối | Đăng nhập bot A. Tab 1 mở Talk Management, tab 2 mở Chat 1:1 và đang xem đúng hội thoại của friend. | 1. Mở 2 tab như tiền đề<br>2. Cho friend gửi 1 ảnh<br>3. Quan sát dòng của friend ở CẢ 2 tab, không reload tab nào<br>4. Chụp ảnh 2 tab cạnh nhau | Friend gửi 1 ảnh | Cả 2 màn cùng hiển thị 「【画像】」. Không màn nào hiện nội dung thô, không màn nào đứng yên với nội dung cũ. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-3** + một phần **GAP-8** · cover **T1, T2, D4** · Evidence: 2 screenshot cạnh nhau (RULE-02) |
| TC-COMPATLEGACY001-01 | COMPAT-LEGACY-001 | Normal | Hội thoại tạo TRƯỚC khi job linect chuẩn hoá `last_message` → leftbar vẫn hiển thị đúng sau khi có tin mới | Tìm được 1 hội thoại cũ (tạo trước thời điểm job linect bắt đầu ghi `last_message`) đang có dòng tin cuối trống hoặc chưa chuẩn hoá. | 1. Mở màn Chat 1:1, tìm hội thoại cũ nói trên, KHÔNG mở nó<br>2. Cho friend của hội thoại đó gửi 1 stamp<br>3. Quan sát dòng leftbar của hội thoại đó<br>4. Reload trang và quan sát lại | Hội thoại cũ + friend gửi 1 stamp | Sau khi có tin mới, dòng leftbar hiển thị 「【スタンプ】」 ở cả đường realtime lẫn sau reload. Không hiển thị JSON thô, không đứng yên ở trạng thái trống. | Chưa test | | STAGING + PRD | | | | Spec không ghi | Lấp **GAP-4** · RULE-09 nhánh cũ · cover **D2, F3, F8** |
| TC-COMPATLEGACY001-02 | COMPAT-LEGACY-001 | Abnormal | Payload socket có `type` dạng CHUỖI (producer bản cũ) → leftbar không được hiển thị nội dung thô | Nhờ Dev xác nhận có luồng nào còn bắn socket với `type` dạng chuỗi không; nếu có, dựng được payload đó ở môi trường test. | 1. Hỏi Dev: sau fix, còn producer nào gửi `e.type` dạng chuỗi ('sticker', 'image'…) không<br>2. Nếu có: kích hoạt luồng đó cho 1 hội thoại đang mở<br>3. Quan sát dòng leftbar<br>4. Nếu Dev khẳng định không còn: ghi × kèm tên người xác nhận và ngày | Payload socket `type = 'sticker'` (chuỗi) | Nếu còn producer gửi chuỗi: leftbar vẫn phải ra nhãn đúng hoặc ít nhất không in JSON thô. Nếu leftbar in nội dung thô → **bug tái xuất ở nhánh ngược lại**, raise ticket. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-4** + alternative root cause (3) của **AP-2** · cover **BUG, D3, F6** · RULE-03: đánh × phải ghi lý do + người xác nhận |
| TC-COMPATLEGACY001-03 | COMPAT-LEGACY-001 | Boundary | Hội thoại đã ẩn (`is_hide=1`) hoặc friend đã block → có tin mới thì leftbar xử lý đúng, không văng lỗi | Bot A có 1 hội thoại đã ẩn và 1 friend đã block bot. | 1. Mở màn Chat 1:1 của bot A<br>2. Cho friend của hội thoại đã ẩn gửi 1 stamp<br>3. Quan sát leftbar và console DevTools<br>4. Lặp lại với friend đã block bot | Hội thoại `is_hide=1`; friend đã block | Leftbar xử lý đúng theo spec (hiện lại hay vẫn ẩn — theo BR của FA-001), **không văng lỗi JS ở console**, không hiển thị JSON thô, không làm hỏng các dòng khác. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-4** + **AP-3** (trạng thái biên) · cover **F1, F3, T1** · Evidence: screenshot leftbar + console log |
| TC-ENV003-01 | ENV-003 | Normal | Chạy lại luồng chính trên PRODUCTION theo TỪNG router loadbalance | Đã deploy bản fix lên production. Biết cách xác định router id đang phục vụ (Catalog D). Có bot test trên production. | 1. Truy cập production, ghi lại router id đang phục vụ<br>2. Mở màn Chat 1:1, cho friend gửi stamp và ảnh, quan sát leftbar realtime<br>3. Ép chuyển sang router còn lại, lặp lại bước 2<br>4. Ghi kết quả cho từng router | 1 stamp + 1 ảnh, chạy trên cả 2 router | Cả 2 router đều hiển thị 「【スタンプ】」/「【画像】」 đúng, realtime, không cần reload. | Chưa test | | **PRD** | | | | Đã hỏi leader | Lấp **GAP-5** · RULE-08 / ENV-003: production có 2 server, không kết luận từ staging · Evidence: screenshot kèm router id |
| TC-ENV003-02 | ENV-003 | Abnormal | Trên PRODUCTION: socket tới TRƯỚC khi job nền ghi xong `last_message` → leftbar không hiển thị nội dung thô | Production (job nền tách 3 job độc lập, khác dev/staging chạy 1 job all). Đang mở hội thoại X, hội thoại Y không mở. | 1. Trên production, mở màn Chat 1:1 và xem hội thoại X<br>2. Cho friend Y gửi liên tiếp nhanh 3 stamp để tăng khả năng socket tới trước khi job ghi xong `last_message`<br>3. Quan sát dòng leftbar của Y trong suốt quá trình (quay video)<br>4. Đối chiếu với response `/ajax/get-badge` ở Network tab | 3 stamp gửi liên tiếp trong ~2 giây | Dòng Y không được **nhấp nháy hiển thị JSON/code thô** ở bất kỳ khoảnh khắc nào. Nếu `last_message` chưa sẵn sàng thì giữ nội dung cũ, sau đó cập nhật đúng nhãn. | Chưa test | | **PRD** | | | | Đã hỏi leader | Lấp **GAP-5** + alternative root cause (1) của **AP-2** · cover **F3, D2, T5** · Evidence bắt buộc: **video** (hiện tượng flash chỉ thấy được qua video) |
| TC-SEC001-02 | SEC-001 | Normal | `get-badge` với hội thoại đúng bot đang đăng nhập → trả đủ `last_message` và `confirm_count` chính xác | Đăng nhập bot A. Có 1 hội thoại của bot A với `last_message` đã biết và số tin chưa đọc đã biết (đếm tay từ màn hình). | 1. Đếm tay số tin chưa đọc của hội thoại đó trên màn Chat 1:1<br>2. Gửi POST `/ajax/get-badge` kèm CSRF, `conversation_id` = hội thoại của bot A<br>3. Đọc JSON response<br>4. Đối chiếu `last_message` và `confirm_count` với những gì quan sát trên màn hình | conversation_id của bot A | `last_message` khớp đúng nội dung dòng tin cuối đang hiển thị; `confirm_count` khớp đúng số tin chưa đọc đếm tay. Không thiếu field so với trước fix. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-6** (RULE-01 Normal cho SEC-001) · thay thế vai trò của `#12544` đang mang mã ngoài checklist · cover **F4, F5, T4** |
| TC-SEC001-03 | SEC-001 | Boundary | Thử truy cập chéo bot qua URL trực tiếp và qua file export (không chỉ API) | Có bot A và bot B. Đăng nhập bot A. Biết `conversation_id` và URL màn chi tiết hội thoại của bot B. | 1. Dán thẳng URL màn chi tiết hội thoại của bot B vào trình duyệt đang đăng nhập bot A<br>2. Ghi lại HTTP status và nội dung màn<br>3. Thực hiện export/tải danh sách hội thoại (nếu màn có chức năng này) và soi file xem có lẫn hội thoại bot B không<br>4. Thử lại với `conversation_id` bot B qua API `/ajax/get-badge` | URL + conversation_id thuộc bot B | Cả 3 đường (URL trực tiếp / API / file export) đều **không lộ** nội dung tin cuối hay thông tin hội thoại của bot B. URL trực tiếp phải bị chặn rõ ràng (403 hoặc điều hướng), không trả nội dung. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-6** · `SEC-001` yêu cầu thử **URL trực tiếp, API, VÀ export** — hiện chỉ có API · cover **F5, T3** |
| TC-CONC003-04 | CONC-003 | Normal | Nhiều tin tới nhiều hội thoại theo ĐÚNG thứ tự → mọi dòng leftbar hiển thị đúng nội dung của chính nó | Bot A có ≥4 hội thoại, đang mở hội thoại X. Mạng bình thường (không throttling). | 1. Mở màn Chat 1:1, đang xem hội thoại X<br>2. Lần lượt cho friend Y gửi stamp, friend Z gửi ảnh, friend W gửi video — mỗi lần cách nhau ~2 giây<br>3. Sau mỗi tin, quan sát dòng leftbar tương ứng<br>4. Chụp màn hình sau khi cả 3 tin đã tới | Y: stamp · Z: ảnh · W: video, gửi tuần tự cách 2 giây | Dòng Y = 「【スタンプ】」, dòng Z = 「【画像】」, dòng W = 「【動画】」. Không dòng nào lẫn nội dung của dòng khác. Dòng X không đổi. | Chưa test | | STAGING | | | | Spec không ghi | Lấp **GAP-7** (RULE-01 Normal cho CONC-003) · cover **F3, REQ-004** |
| TC-CONC003-05 | CONC-003 | Boundary | Nhiều hội thoại cập nhật đồng thời ở ngưỡng lớn + bấm filter/search liên tiếp → kết quả khớp điều kiện CUỐI CÙNG | Bot A có số hội thoại bằng hoặc lớn hơn khách hàng lớn nhất thực tế (hỏi CS/Dev con số này). Leftbar có loadmore/phân trang và có filter theo tag / trạng thái đối ứng. | 1. Bật DevTools > Network throttling Slow 3G<br>2. Cho ≥5 friend gửi tin gần đồng thời (stamp/ảnh/video xen kẽ)<br>3. Trong lúc các request `get-badge` đang chờ, bấm filter/search liên tiếp 3 lần với điều kiện khác nhau<br>4. Sau khi mọi request hoàn tất, đối chiếu danh sách hiển thị với điều kiện lọc CUỐI cùng<br>5. Cuộn loadmore xuống trang 2 rồi quan sát lại | ≥5 tin gần đồng thời, 3 lần đổi filter, Slow 3G, quy mô hội thoại ở ngưỡng thực tế | Danh sách cuối cùng khớp đúng điều kiện lọc **cuối cùng**; không dòng nào trùng lặp; không dòng nào hiển thị nội dung của hội thoại khác; không có dòng hiện JSON thô; không nhảy vị trí sau loadmore. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-7** + **AP-3** · phủ 2 chiều còn thiếu của `CONC-003` (throttling + filter liên tiếp) · Evidence: video + screenshot Network tab thể hiện thứ tự response |
| TC-SECISO001-01 | SEC-ISO-001 | Normal | Mở 2 tab cùng user, mỗi tab xem 1 hội thoại khác nhau → dữ liệu 2 tab không dính chéo | Bot A có ≥2 hội thoại. Mở 2 tab trên cùng browser, cùng session. Tab 1 xem hội thoại X, tab 2 xem hội thoại Y. | 1. Mở 2 tab như tiền đề<br>2. Cho friend X gửi stamp, gần như đồng thời cho friend Y gửi ảnh<br>3. Quan sát leftbar và khung chat ở CẢ 2 tab<br>4. Chụp ảnh 2 tab cạnh nhau | X: stamp · Y: ảnh, gửi gần đồng thời | Tab 1 và tab 2 đều hiển thị dòng X = 「【スタンプ】」 và dòng Y = 「【画像】」. Khung chat mỗi tab chỉ chứa tin của hội thoại tab đó đang mở. Không tin nào xuất hiện nhầm tab. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-8** · `SEC-ISO-001` trigger: UI hiển thị nhiều cuộc trò chuyện đồng thời · cover **F3, T1** |
| TC-SECISO001-02 | SEC-ISO-001 | Abnormal | 2 tài khoản khác nhau đăng nhập trên cùng browser (2 cửa sổ thường + ẩn danh) → không dính dữ liệu chéo | Có tài khoản U1 (bot A) và U2 (bot B). Cửa sổ thường đăng nhập U1, cửa sổ ẩn danh đăng nhập U2. | 1. Mở 2 cửa sổ như tiền đề, mỗi bên mở màn Chat 1:1<br>2. Cho friend của bot A gửi stamp và friend của bot B gửi ảnh, gần như đồng thời<br>3. Quan sát leftbar ở cả 2 cửa sổ<br>4. Kiểm tra Network response `/ajax/get-badge` ở mỗi cửa sổ xem `last_message` thuộc đúng bot nào | Bot A: stamp · Bot B: ảnh, gửi gần đồng thời | Cửa sổ U1 chỉ hiện hội thoại và nội dung của bot A; cửa sổ U2 chỉ hiện của bot B. Không có bất kỳ `last_message` nào của bot kia xuất hiện ở response hoặc trên màn. | Chưa test | | STAGING | | | | Đã hỏi leader | Lấp **GAP-8** · cover **F5, T3** · liên kết trực tiếp với vá bảo mật `where bot_id = getBotId()` |
| TC-DATA001-01 | DATA-001 | Normal | Badge số tin chưa đọc vẫn khớp giữa leftbar / màn Talk Management / API sau khi thêm filter `bot_id` | Bot A có 1 hội thoại với số tin chưa đọc đã biết chính xác (đếm tay). Đăng nhập bot A. | 1. Đếm tay số tin chưa đọc của hội thoại đó trên leftbar màn Chat 1:1<br>2. Mở màn Talk Management, đọc lại con số tương ứng<br>3. Gọi `/ajax/get-badge` cho hội thoại đó, đọc `confirm_count`<br>4. Cho friend gửi thêm 2 tin, lặp lại 3 bước trên<br>5. Lập bảng đối chiếu 3 nguồn trước và sau | Số tin chưa đọc ban đầu đã biết + 2 tin mới | Cả 3 nguồn (leftbar / Talk Management / API `confirm_count`) cho **cùng một con số** ở cả 2 thời điểm, và tăng đúng 2 sau khi gửi thêm. Không nguồn nào về 0 sai. | Chưa test | | STAGING + PRD | | | | Đã hỏi leader | Lấp **GAP-9** · cover **F4, F5, T4, T2** · Evidence: bảng đối chiếu 3 nguồn + phép đếm tay (DATA-COUNT-001 style) |
| TC-DEPLOYASSET001-02 | DEPLOY-ASSET-001 | Boundary | Sau deploy: Network tab không có asset 404, font không fallback, icon không lúc có lúc mất | Browser đã cache toàn bộ asset của bản cũ (`?v=202608181516`). Đã deploy bản mới (`?v=202608191100`). | 1. Mở màn Chat 1:1 bằng browser còn cache bản cũ<br>2. Chỉ **F5 thường** (KHÔNG Ctrl+F5)<br>3. Mở DevTools > Network, lọc theo JS/CSS/font/icon: kiểm từng dòng status code và query version<br>4. Reload lại 3 lần liên tiếp, mỗi lần quan sát icon và font trên màn<br>5. Soi chữ kanji/kana và dấu tiếng Việt trên leftbar | N/A | Không có asset nào trả **404**. `chat-v2.js` trả 200 với `?v=202608191100`. Font không bị fallback (không có ô tofu ロ), glyph kanji/kana và dấu tiếng Việt hiển thị đủ. Icon-font hiển thị ổn định qua cả 3 lần reload, không lúc có lúc mất. | Chưa test | | STAGING + PRD | | | | Spec ghi rõ | Lấp **GAP-10** (RULE-01 Boundary cho DEPLOY-ASSET-001) · cover **F9, T5** · Evidence bắt buộc: screenshot DevTools Network (query version + status) + screenshot màn sau F5 thường |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần update spec** — 3 điểm:

**6.1 — `/ajax/get-badge` chưa có mã EP trong spec `chat-1on1`**
- **Section**: `spec-features/admin/chat-1on1/feature-spec.md` — danh sách endpoint `EP-01`…`EP-49`.
- **Nội dung cần update**: bổ sung EP cho `POST /ajax/get-badge`, ghi rõ **contract response mới** (`badge`, `confirm_count`, `msg_kind`, **`last_message`**), điều kiện lọc `bot_id = getBotId()`, và hành vi khi `conversation_id` thiếu / không tồn tại / thuộc bot khác. Hiện 3 TC (`#12543`, `#12545`, `#13490`) phải ghi *"expected suy từ diff code"* vì không có contract để đối chiếu.
- **Người chịu trách nhiệm**: Dev (`AI LME Fix bug` / người maintain `ChatController`) + Leader duyệt.

**6.2 — Chốt danh sách loại tin bạn bè có thể gửi**
- **Section**: spec `chat-1on1` mục hiển thị dòng tin cuối ở leftbar.
- **Nội dung cần update**: liệt kê **đầy đủ** loại tin friend gửi được và nhãn 【…】 tương ứng; ghi rõ **`image_map` / `pdf` có nằm trong tập đó không** (code mới đã **bỏ** case `image_map`). Đây là câu hỏi mở đang chặn oracle của TC `#12538`.
- **Người chịu trách nhiệm**: team LINE integration xác nhận → Leader ghi vào spec.

**6.3 — Ghi rõ hành vi mong đợi khi `get-badge` lỗi / `last_message` rỗng**
- **Section**: spec `chat-1on1`, mục cập nhật realtime.
- **Nội dung cần update**: "giữ nguyên nội dung cũ" hiện là **hành vi suy từ code**, chưa có spec. Cần chốt: giữ im lặng hay phải có tín hiệu cho người dùng? Câu trả lời quyết định TC `#12540`, `#13489` là Đạt hay Không đạt — và cũng quyết định `TC-PERM003-02` (§5).
- **Người chịu trách nhiệm**: PM/Leader.

---

## 7. Checklist đã chạy

- [x] A. Coverage
- [x] B. Chất lượng từng TC
- [x] C. Chất lượng bộ TC tổng thể
- [x] D. Spec alignment
- [x] E. Hành chính
- [x] F. Base quan điểm test LME — [checklist-lme.md](../../framework/checklist-lme.md) (tầng 1) + [catalog-lme.md](../../framework/catalog-lme.md) (tầng 2)
  - [x] F.1 Quan điểm (tầng 1) — bảng dưới đây
  - [x] F.2 Catalog (tầng 2) — B (UI: loading/rỗng/lỗi, race client) · C (bản đồ LME: chat 1:1, đa bot, phân quyền) · D (môi trường: job tách 3 trên prod, 2 router loadbalance, cache asset)
  - [x] F.3 RULE — RULE-01 ✗ (SEC-001, CONC-003, DEPLOY-ASSET-001 thiếu loại case) · RULE-02 ✗ (không TC nào ghi loại evidence bắt buộc) · RULE-03 n/a · RULE-06 n/a (output là màn admin, không có output ra ngoài) · RULE-07 n/a (fix chỉ READ, không CRUD) · RULE-08 ✗ (0 TC production) · RULE-09 ✗ (không có nhánh cũ)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` | Cao | ◯ — luôn bắt buộc | TC-TOOLKNOW002-01 · TC-OUTTRUTH001-01…07 · TC-FUNC004-01 (cover bằng **nội dung**, không TC nào mang mã này) | 0/9 | **RISK** — nội dung đủ, nhãn thiếu; chưa chạy |
| `FUNC-004` | Cao | ◯ — có giới hạn 50 ký tự ở nhánh default | TC-FUNC004-01 | 0/1 | **RISK** — có Boundary (49/50) nhưng thiếu 0/rỗng; chưa chạy |
| `CONC-001` | Cao | ✕ — không có nút thực thi hành động, không batch, không giới hạn dùng chung | — | — | ✕ có lý do |
| `CONC-003` | **Cao** (leftbar có loadmore + filter, nhiều hội thoại cùng gọi API) | ◯ | TC-CONC003-01/02/03 (03 trùng 01) | 0/3 | **RISK** — chỉ Abnormal, thiếu Normal + Boundary → **[MAJOR] RULE-01**; thiếu 2/4 chiều |
| `DATA-001` | Cao | ◯ — `last_message` hiển thị ở nhiều màn | Chỉ TC-APICONTRACT001-01 (tầng API) | 0/1 | **GAP** → **[MAJOR]** (GAP-9) |
| `DATA-COUNT-001` | Cao | ◯ — leftbar có badge số tin chưa đọc | TC-CONC003-02 (chỉ kiểm không nhầm hội thoại) | 0/1 | **GAP** → **[MAJOR]** (gộp vào GAP-9) |
| `DATA-CACHE-001` | Trung bình → **Cao** (output user-facing) | ◯ — release đổi JS | TC-DATACACHE001-01 | 0/1 | **RISK** — 1 Abnormal, chưa chạy |
| `DATA-DB-001` | Cao | ✕ — fix chỉ READ `conversation.last_message`, không UPDATE/DELETE | — | — | ✕ có lý do |
| `DATA-MIG-001` | Cao | ✕ — không đổi cấu trúc dữ liệu, không migration | — | — | ✕ có lý do |
| `DATA-AUDIT-001` | Cao | ✕ — không có thao tác xóa/sửa dữ liệu nhạy cảm | — | — | ✕ có lý do |
| `INTG-LINE-001` | Cao | ◯ — luồng nhận webhook/socket từ LINE | Không TC nào giả lập lỗi LINE / webhook mất | 0 | **GAP** → nêu ở §4.2 gián tiếp qua GAP-4/GAP-5 · ⚠️ Leader cân nhắc nâng thành TC riêng nếu vòng sau còn thời gian |
| `PERM-002` | Cao | ◯ — gọi thẳng API endpoint | TC-SEC001-01 (cùng nội dung) | 0/1 | **RISK** — gộp cover với SEC-001 |
| `PERM-003` | Cao | ◯ — **có chức năng change bot**, filter mới lấy bot từ session | **Không TC nào** | 0 | **GAP** → **[BLOCKER]** (GAP-2) |
| `OUT-TRUTH-001` | Cao | ◯ | 10 TC | 0/10 | **RISK** — nội dung tốt, 0 chạy |
| `OUT-PREVIEW-001` | Cao | ✕ — không có preview / test-send | — | — | ✕ có lý do |
| `UI-003` | Trung bình → **Cao** (rủi ro false success: giữ content cũ mà không báo) | ◯ | TC-UI003-01/02/03 (03 trùng 02) | 0/3 | **RISK** — chỉ Abnormal, thiếu trạng thái loading + rỗng (bot 0 hội thoại) |
| `UI-002` | Trung bình | ◯ — UI user-facing, JS đổi | Không TC nào ghi browser/thiết bị | 0 | **GAP** → `[MINOR]`, gợi ý ghi rõ Mac Safari + Windows Chrome vào `Môi trường test` |
| `REG-SHARED-001` | Cao | ◯ — sửa endpoint + JS dùng chung, đa brand | **Không TC nào** | 0 | **GAP** → **[BLOCKER]** (GAP-1) |
| `REG-RUN-001` | Cao | ✕ — không có job/dữ liệu chạy dở bị ảnh hưởng bởi release này | — | — | ✕ có lý do |
| `SEC-001` | Cao | ◯ — chạm nội dung hội thoại khách hàng (PII) | TC-SEC001-01 | 0/1 | **RISK** — chỉ Abnormal → **[MAJOR] RULE-01**; thiếu chiều URL/export |
| `SEC-ISO-001` | Cao | ◯ — leftbar tải nhiều hội thoại đồng thời | Chỉ ghi ở `note` của #12541/#13491, **không ở cột viewpoint** | 0 | **GAP** (theo nhãn) / RISK (theo nội dung) → **[MAJOR]** (GAP-8) |
| `ENV-003` | Cao | ◯ — asset/domain + job nền + 2 router production | **Không TC nào chạy production** | 0 | **GAP** → **[MAJOR]** (GAP-5) |
| `JOB-001` | Cao | ✕ — không thêm/sửa job nền (linect chỉ đọc để đối chiếu) | — | — | ✕ có lý do — nhưng precondition của #12539 **phụ thuộc** job linect → ghi rõ ở tiền đề |
| `LIST-001` | Trung bình | ◯ — leftbar là màn danh sách có search/filter/loadmore | Không TC nào | 0 | **GAP** → gộp vào `TC-CONC003-05` (§5) |
| `DEPLOY-ASSET-001` | Cao | ◯ — sửa file JS | TC-DEPLOYASSET001-01 · TC-DATACACHE001-01 | 0/2 | **RISK** — thiếu Boundary → **[MAJOR] RULE-01** (GAP-10) |
| `DEPLOY-LIVE-001` | Cao | ◯ — release production **không lock maintain**, và **payload API `/ajax/get-badge` đổi cấu trúc** | Không TC nào | 0 | **GAP** → **[MAJOR]**; kịch bản: tab mở sẵn với JS cũ gọi server mới. Một phần đã nằm trong `TC-DATACACHE001-01`, nhưng chiều "client cũ gọi server mới" thì chưa. Leader cân nhắc thêm 1 TC. |
| `COMPAT-LEGACY-001` | Cao | ◯ — `messages_v2s` là bảng "bản mới"; đảo so khớp chuỗi→số | Không TC nào | 0 | **GAP** → **[MAJOR]** (GAP-4) |
| `PERF-LARGE-001` | Trung bình | ◯ — leftbar ở quy mô nhiều hội thoại | Không TC nào | 0 | **GAP** → gộp vào `TC-CONC003-05` / `TC-PERM003-03` (§5) |
| `MEDIA-*` | — | ✕ — fix không chạm upload/xử lý media, chỉ hiển thị **nhãn** loại tin | — | — | ✕ có lý do |
| `MSG-*`, `BULK-*`, `PAY-*`, `NOTI-MAIL-*`, `FRIEND-001`, `INTG-CAL-001`, `INTG-SHEET-001`, `SYNC-APP-001` | — | ✕ — ngoài phạm vi fix (không gửi tin, không lọc đối tượng, không thanh toán, không friend info, không đồng bộ ngoài) | — | — | ✕ có lý do · ⚠️ `SYNC-APP-001` chuyển thành ◯ **nếu** Dev xác nhận mobile app cũng gọi `/ajax/get-badge` → khi đó thuộc GAP-1 |

**Tổng kết F.1**: 8 quan điểm `GAP` (2 → BLOCKER, 6 → MAJOR) · 10 `RISK` (đều do **chưa chạy**, không phải do thiếu TC) · 0 `OK` — vì **không quan điểm nào có TC đã `pass`**.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

> **Draft sinh bởi `/review-tc` ngày 2026-08-26** từ MCP LME TEST STUDIO task #199 (24 TC) + `01-bug-task.md` + `03-dev-impact.md`. Không có `02-spec-reference.md` → fallback [templates/LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) và spec-features `chat-1on1` qua báo cáo coverage của Studio.
> **Input thiếu**: (1) danh sách caller `/ajax/get-badge` do Dev cung cấp — chặn `REG-SHARED-001`; (2) xác nhận friend có gửi được `image_map`/`pdf` — chặn oracle `#12538`; (3) contract chính thức của `/ajax/get-badge` — chặn oracle `#12545`/`#13490`; (4) ngưỡng số bot / số hội thoại của khách hàng lớn nhất — chặn TC Boundary ở §5.
> Leader verify lại trước khi gửi member. TC trên Studio là **read-only** — mọi chỉnh sửa TC phải làm bằng `testcase_update` trên Studio rồi fetch lại, KHÔNG sửa tay `04-tc-list.md`.
