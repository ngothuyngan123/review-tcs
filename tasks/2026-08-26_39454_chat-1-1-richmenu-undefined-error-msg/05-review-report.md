# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Task folder | `tasks/2026-08-26_39454_chat-1-1-richmenu-undefined-error-msg/` |
| Bug / Ticket | Redmine #39454 — `[Chat 1: 1][Rich menu] Khi add hiển thị rich menu từ màn chat 1:1, case rich menu không tồn tại, sửa lại error message` |
| Trạng thái Redmine | `Fix done - Đợi test` · branch `ai_fixbug_39454` · commit `b5b3faa25f` |
| Reviewer | Test Leader (draft do `/review-tc` sinh) |
| Ngày review | 2026-08-26 |
| Vòng review | round 1 (Studio `reviewState = leader`, `reviewed = false`, `review_list_comments` = **0 comment** → chưa có vòng nào trước) |

---

## 0. Nguồn TC

| Mục | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, `task_id = 185`, ticket 39454, feature `chat-1on1`, branch `ai_fixbug_39454`, round 1 |
| Tổng TC lấy về | **11 TC** (`testcase_list`, `totalMatched = 11`, `nextCursor = null`) |
| Thời điểm fetch | 2026-08-26 (trong phiên này) |
| Payload | Trả về **inline, không vượt token limit** → không phát sinh file `tool-results/*.txt`, không cần `scripts/parse_studio_tcs.py` |
| Snapshot | Bộ TC này đã được ghi sẵn ra [04-tc-list.md](04-tc-list.md) bởi `/new-task` **cùng ngày, cùng payload** → không tạo thêm `04-tc-list.studio.md` trùng nội dung |
| Nguồn 2 (Sheet human) | **KHÔNG dùng** — Studio đã có TC nên dừng ở nguồn 1 (đúng quy tắc). Redmine #39454 cũng không có section "Link TCs" |
| Nguồn 3 (file 04) | **KHÔNG dùng làm nguồn** — chỉ đối chiếu là cùng payload Studio |
| Đối chiếu chéo | **KHÔNG** — đã dừng ở nguồn đầu tiên có TC |
| Bổ sung | `task_get_context(requirements, test_viewpoint_selection, review)` — 10 REQ · `task_get_report` — run history + evidence `actual` · `review_list_comments` — rỗng |

### 0.1 Cảnh báo bắt buộc về chất lượng nguồn (BƯỚC 0.6)

| # | Nội dung | Kết quả | Flag |
|---|---|---|---|
| 1 | **Kết quả thực thi thật** | `pass 6` · `fail 0` · `error 0` · `skip 0` · **`untested` 5** → tỷ lệ pass = **6/11 = 54.5%** | `[MAJOR]` (< 80%) |
| 2 | **TC fail / error · ticket bug** | 0 TC fail, 0 TC error, `bug_tickets` rỗng ở cả 11 TC, `openBugs = 0` → **không có TC fail chưa raise ticket** | — |
| 3 | **Môi trường đã chạy** | **100% `local`** (runId 436). `dev` 0 run · `staging` 0 run · `prd` 0 run. Task chạm **LINE API bên thứ 3** + liên đới **job nền** rich menu | `[MAJOR] RULE-08 / ENV-003` |
| 4 | **Ai chạy** | `last_exec.source = ai`, `by = pipeline` · `manual.results = []` (**0 kết quả manual**) · `submittedWithoutMcp = false` | `[MAJOR]` |
| 5 | **Tác giả TC** | **9/11 do AI sinh** (`provenance.source = ai`, job #550) = **81.8%**; 2 TC do người (`anhptn@mcp`, 2026-08-26). `reviewState = leader` (chưa `done`), toàn bộ 11 TC `status = draft` | `[MAJOR]` |
| 6 | **Mã quan điểm lạ** | `TOOL-KNOW-002` (1 TC) và `API-CONTRACT-001` (1 TC) **không tồn tại** trong `framework/checklist-lme.md`; `RULE-12` (2 TC) **có trong file nhưng là RULE quy trình, không phải mã quan điểm** → **4/11 TC KHÔNG được tính là cover** ở BƯỚC 2/3b | `[MAJOR]` |

### 0.2 Phát hiện thêm từ `task_get_report` (ngoài digest chuẩn)

1. 🔴 **Run `561` đang ở trạng thái `queued`** trên `local` — có một lần chạy đang chờ. Report này dựa trên run **436** (2026-08-24 08:39:45 → 09:15:42). Kết quả có thể đổi sau khi 561 chạy xong.
2. 🔴 **Evidence (`artifacts`) rỗng ở 5/6 TC pass** — chỉ `TC-APICONTRACT001-01` (#12314) có 1 artifact log. Cột `Evidence thực tế` của cả 11 TC đều trống → **RULE-02**.
3. 🔴 **`TC-APICONTRACT001-01` đánh `pass` nhưng `actual` chỉ chứng minh 1/3 dataset** — xem `[BLOCKER-2]`.
4. **Studio tự khai coverage `0/3 covered, 3 partial`** (`SCR-CHT-01`, `EP-49`, `TICKET-39454` đều mức `partial`), `redmineWriteback` ghi *"Độ phủ spec: 0/3 covered"* → chính Studio cũng không coi bộ TC này là đủ phủ.

---

## 1. Verdict

# 🔴 REJECTED

**5 `[BLOCKER]`** — không được nghiệm thu "Fix done" với bộ kết quả hiện tại. Lý do gốc: **toàn bộ kết quả `Đạt` đến từ 1 lần chạy pipeline AI ở `local` với LINE API không thật**, trong khi **đúng những TC tái hiện kịch bản khách báo và phân biệt nguyên nhân lỗi thì chưa chạy lần nào**, và **một TC được đánh `pass` nhưng bằng chứng chỉ phủ 1/3 điều kiện mà chính TC đó khai**.

---

## 2. Tóm tắt cho member

**Điểm tốt:** bộ TC bám sát code diff, tách nhánh lỗi khá sạch (id LINE rỗng / 404 / non-404 / exception khi kiểm tra lại), có **đối chứng âm** kiểm dữ liệu friend không bị ghi đè — đây là chỗ nhiều bộ TC hay bỏ. 10/10 REQ đều có TC gắn.

**Phải fix trước khi test lại:** (1) chạy lại toàn bộ nhánh lỗi trên môi trường có **LINE thật** — 6 kết quả `Đạt` hiện tại đều ở `local` và không kết luận được; (2) `TC-APICONTRACT001-01` phải tách/chạy đủ 3 dataset kèm evidence riêng, hiện đang **che một GAP**; (3) bổ sung TC cho **friend đã block / user không còn tồn tại phía LINE** — chính Dev cảnh báo 404 dễ nhập nhằng nhưng không TC nào kiểm; (4) danh sách caller của Dev **thiếu 2 đường cũng set rich menu cho friend** (multi action ở chat 1:1, job hiển thị/dừng).

---

## 3. Coverage Matrix

Impact lấy từ [03-dev-impact.md](03-dev-impact.md) §4. Cột `Exec` = `<số pass>/<số TC>` của các TC cover impact đó (nguồn Studio, run 436).

| Impact | Loại | TCs cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — catch trả `success=false` không kèm `msg` → FE `alert(response.msg)` = 「undefined」 | Root cause | `TC-TOOLKNOW002-01`, `TC-INTGLINE001-01`, `TC-DATATEXT001-01`, `TC-OUTTRUTH001-02` | 4 | 3/4 | **RISK** — TC tái hiện **đúng kịch bản khách báo** (`TC-INTGLINE001-01`, rich menu bị tool ngoài xóa → LINE 404) **chưa chạy lần nào** |
| **F1** — `ChatController::chatEditRichMenu` | Direct | `TC-TOOLKNOW002-01`, `TC-OUTTRUTH001-02`, `TC-ENV001-01`, `TC-INTGLINE001-01`, `TC-OUTTRUTH001-03`, `TC-RULE12-01/02` | 7 | 4/7 | **RISK** — nhánh 404 + cả 2 nhánh thành công chưa chạy |
| **F2** — `ChatController::isRichMenuDeletedOnLine` (hàm mới) | Direct | `TC-INTGLINE001-01` (404=true), `TC-ENV001-01` (false), `TC-ENV001-02` (exception) | 3 | 1/3 | **RISK** — 2/3 nhánh của **hàm mới** chưa chạy; không TC nào kiểm nhánh 404-do-nguyên-nhân-khác |
| **F3** — `handleSaveEditRichMenu` / `hideRichMenu` (FE `alert(response.msg)`) | Indirect, không sửa code | `TC-TOOLKNOW002-01`, `TC-DATATEXT001-01` (gián tiếp qua popup) | 2 | 2/2 | **RISK** — chỉ verify popup ở các nhánh BE **đã thêm `msg`**; không nhánh lỗi nào **không đi qua try/catch** (500 / CSRF 419 / session hết hạn) được kiểm → xem `[MAJOR-11]` |
| **F4** — `FriendlistController::saveRichMenu` (đặt rich menu hàng loạt) | Không sửa — Dev khai ngoài phạm vi, **"nuốt lỗi, vẫn trả thành công"** | *(không TC nào)* | 0 | — | 🔴 **GAP** |
| **D1** — `bot_line_user.rich_menu_id` | UPDATE (nhánh thành công) / không đổi (nhánh lỗi) | `TC-OUTTRUTH001-03` (nhánh id rỗng), `TC-ENV001-01` (nhánh non-404), `TC-RULE12-01/02` (nhánh thành công) | 4 | 2/4 | **RISK** — đối chứng âm chỉ chạy ở **1/3 nhánh lỗi**; **không TC nào kiểm `WHERE` scope trên 2 tài khoản** |
| **D2** — `rich_menu_history` (`trigger_type_start=15001`) | Không sinh bản ghi ở nhánh lỗi | `TC-OUTTRUTH001-03`, `TC-ENV001-01`, `TC-RULE12-01` | 3 | 2/3 | **RISK** — nhánh 404 không có đối chứng history |
| **D3** — `rich_menus.rich_menu_id` (đọc) | READ | `TC-TOOLKNOW002-01`, `TC-OUTTRUTH001-02`, `TC-INTGLINE001-01` | 3 | 2/3 | **RISK** |
| **T1** — Rich Menu (FA-004) | Regression | `TC-INTGLINE001-01`, `TC-OUTTRUTH001-01` (recovery edit/save) | 2 | **0/2** | 🔴 **RISK nặng** — **cả 2 TC đều chưa chạy**; không TC nào cover job hiển thị/dừng rich menu |
| **T2** — 1-on-1 Chat (FA-001) | Regression | `TC-RULE12-01`, `TC-RULE12-02` | 2 | **0/2** | 🔴 **RISK nặng** — 2 TC regression **chưa chạy**, và cả 2 đều là happy path (AP-3) |

**Tổng kết:** 0 impact đạt `OK` · 9 `RISK` · 1 `GAP`. Không impact nào đủ điều kiện `OK` vì điều kiện `OK` yêu cầu "có TC đã chạy `pass`" **và** đủ chiều — không có impact nào thoả cả hai.

### ORPHAN TCs

**Không có ORPHAN.** Cả 11 TC đều nằm trong scope `BUG / F1 / F2 / F3 / D1 / D2 / D3 / T1 / T2` hoặc một quan điểm LME hợp lệ. `TC-APICONTRACT001-01` tuy dùng mã quan điểm không tồn tại nhưng nội dung vẫn thuộc scope `F1` + `EP-49`, không phải orphan.

**Lưu ý AP-5 (over-coverage layer downstream):** `TC-DATATEXT001-01` và `TC-TOOLKNOW002-01` cùng dừng lại ở popup FE — FE **không bị sửa code**. Không đề nghị bỏ (mỗi TC vẫn có oracle riêng), chỉ ghi nhận ở §4.5.

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape nhận diện** (từ [03-dev-impact.md](03-dev-impact.md) §2): **`handle exception` / `return error` / `fallback message`** — hàng 1 bảng fix-shape (generic catch) — **kết hợp** với **`early-return theo điều kiện cụ thể`** (specific check) và một phần **`quét ngang chức năng tương tự`**.

| Câu hỏi adversarial | Trả lời từ input thật | Kết luận |
|---|---|---|
| Impl là **generic catch-all** hay **specific code check**? | **Hỗn hợp.** 2 nhánh early-return theo điều kiện cụ thể (`empty($richIdForLine)`), + 1 nhánh catch có thêm 1 lần kiểm tra `isRichMenuDeletedOnLine` (404 = đã xóa), + else trả message chung. | Ghi nhận |
| TCs verify với **≥ 3 trigger condition khác nhau**? | **Có — 5 trigger**: (a) id LINE rỗng khi đổi · (b) id LINE rỗng ở rich menu mặc định khi dừng · (c) LINE non-404 (401) · (d) LINE 404 · (e) exception ngay ở bước kiểm tra lại. → **KHÔNG dính AP-1** ở mức thiết kế TC. | ✅ Pass thiết kế |
| Nhưng **bao nhiêu trigger đã THỰC SỰ chạy**? | **Chỉ 3/5** — (a)(b)(c) pass ở `local`. **(d) và (e) chưa chạy lần nào.** (d) chính là trigger của bug khách báo. | 🔴 `[BLOCKER-3]` |
| Có TC trigger error code **CHƯA BIẾT** để test fallback generic? | **KHÔNG.** Mọi TC đều dựng một lỗi đã biết trước. Không TC nào chạy nhánh lỗi **không đi qua try/catch của controller** — HTTP 500 (PHP fatal), 419 CSRF, session hết hạn, mất mạng giữa chừng. Ở các nhánh đó FE vẫn `alert(response.msg)` → **vẫn hiện 「undefined」**. | 🔴 `[MAJOR-11]` |
| **Specific code check** — đã list TẤT CẢ condition Dev handle? | Có 4 nhánh trong controller. Nhưng **404 được dùng làm dấu hiệu duy nhất** để kết luận "rich menu bị xóa" — chính Dev ghi rủi ro: *"đường dẫn đó có cả mã người dùng nên 404 dễ nhập nhằng"*. **Không TC nào kiểm 404 sinh ra vì lý do khác** (friend đã block / user không còn tồn tại phía LINE). | 🔴 `[BLOCKER-1]` |
| **Quét ngang** — danh sách nơi ảnh hưởng do Dev cung cấp có đủ? | Dev list 5 mục (§3 file 03) và tự phát hiện `FriendlistController::saveRichMenu` cùng lớp lỗi. Nhưng đối chiếu [kho-tcs/fa004](../../kho-tcs/fa004-richmenu-リッチメニュー.md) `TC-RM-421`/`TC-RM-422` — *"Set rich menu qua **multi action** / **right bar chat 1:1** / **friend list**"* — và `spec-features/admin/rich-menu/feature-spec.md` §7 (job `SettingDisplayRichMenuHistoriesTask` gọi `POST /v2/bot/richmenu/bulk/link`): **thiếu 2 đường** cũng set `bot_line_user.rich_menu_id` qua LINE API. | 🔴 `[BLOCKER-4]` |

### Symptom-only KH report check

🔴 **DÍNH.** [01-bug-task.md](01-bug-task.md) mục "Mô tả bug" ghi nguyên văn: *"khi richmenu **được tạo từ phía tool khác**, không phải từ lme tool"*. Nhưng root cause Dev fix là *"rich menu **đã bị xóa** khỏi tài khoản LINE chính thức (thường do công cụ khác dùng song song xóa mất) **hoặc chưa từng đăng ký được**"*.

**"Được tạo bởi tool khác" ≠ "bị tool khác xóa"** — đây là **2 kịch bản khác nhau**. KH không nêu error code / log. Toàn bộ 11 TC bám kịch bản Dev chọn; **không TC nào** cover kịch bản KH mô tả theo nghĩa đen (một rich menu do tool ngoài tạo trên LINE OA, LME không có bản ghi). → `[MAJOR-9]`.

### Anti-pattern check

| AP | Dính? | Ghi chú |
|---|---|---|
| **AP-1** Single-trigger generic-fix | ⚠️ **Một phần** | Thiết kế TC có 5 trigger (đạt), nhưng **không có trigger "unknown error"** và chỉ 3/5 đã chạy → `[MAJOR-11]` |
| **AP-2** Symptom-only KH report | 🔴 **Dính** | Xem trên → `[MAJOR-9]` |
| **AP-3** Happy-path-only regression | 🔴 **Dính** | T1 + T2 mỗi cái đúng 1–2 TC, precondition đều là data sạch/hợp lệ. Không TC regression nào ở edge state (friend đã block, rich menu ngoài thời gian hiển thị, bot free plan, 2 bot) → `[MAJOR-17]` |
| **AP-4** Specific check ngụy trang generic | 🔴 **Dính** | Mục "Commit / Pull Request" **không có link PR** — chỉ có commit hash `b5b3faa25f` + link dashboard nội bộ. Không review được diff thật để xác nhận fix shape → `[MAJOR-10]` |
| **AP-5** Over-coverage layer downstream | ⚠️ Nhẹ | 2 TC dừng ở popup FE (không sửa code). Giữ nguyên, chỉ ghi nhận §4.5 |
| **AP-6** Mục 3 dev-impact trống | ✅ Không dính | Dev list 5 mục caller — nhưng **thiếu** (xem `[BLOCKER-4]`) |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER-1]` GAP-MSG003 — Không TC nào phân biệt "rich menu bị xóa" với "friend đã block / user không tồn tại phía LINE"**
Cơ chế phân biệt duy nhất của fix là **HTTP 404 từ LINE**. Chính Dev ghi rủi ro trong §7 file 03: *"Nếu LINE trả 404 vì lý do khác ngoài rich menu không tồn tại thì thông báo có thể chưa sát… đường dẫn đó có cả mã người dùng nên 404 dễ nhập nhằng"*. Quan điểm **`MSG-003` — Xử lý blocked user · Cao** trigger khớp (`INTG-LINE-001` cũng ghi rõ "user block/unblock" phải xét) nhưng **0 TC**.
**Rủi ro bỏ lọt:** friend đã block bot → admin đổi rich menu → hệ thống báo 「リッチメニューが削除されました」 + hướng dẫn "sửa và lưu lại rich menu" → **khách sửa rich menu vô ích**, nguyên nhân thật bị che.
→ **Fix:** bổ sung `TC-MSG003-01` (§5 GAP-10) trước khi chạy lại.

**`[BLOCKER-2]` `TC-APICONTRACT001-01` (Studio #12314) — đánh `pass` nhưng evidence chỉ phủ 1/3 dataset mà chính TC khai**
`Kết quả mong đợi` khai 3 dataset: **A** (LINE id rỗng), **B** (LINE trả 404), **C** (LINE non-404 / 401). `task_get_report.actual` của run 436 chỉ ghi: `HTTP=200; success=false; hasMsg=true; msg==DELETED=true; body={...削除されま` — **một response duy nhất, đúng dataset A**. Không có bằng chứng nào cho B và C.
Mâu thuẫn thêm: TC UI tương ứng cho dataset B (`TC-INTGLINE001-01`) bị đánh `manual`/`staging` với lý do *"container dev không gọi được LINE API"* — vậy dataset B **không thể** đã chạy ở `local`.
**Rủi ro:** kết quả `Đạt` sai sự thật → REQ-006 (risk **High**) trông như đã kiểm chứng, đồng thời **che GAP** của REQ-003/REQ-004 ở tầng API (xem §4.5 `DUP-INFLATE`).
→ **Fix:** tách #12314 thành 3 TC (hoặc giữ 1 TC nhưng ghi 3 lần chạy + 3 artifact riêng), **hủy kết quả `Đạt` hiện tại**, chạy lại.

**`[BLOCKER-3]` `TC-INTGLINE001-01` (Studio #12309) — TC tái hiện ĐÚNG kịch bản khách báo chưa chạy lần nào**
`last_exec = null`. Đây là TC duy nhất verify REQ-003 (risk **High**) — rich menu bị xóa khỏi LINE bởi tool ngoài → LINE 404 → hiện message đúng. Đúng nghiệp vụ mà khách báo bug. Quan điểm `INTG-LINE-001` (**Cao**, trigger BẮT BUỘC) coi như **chưa có kết luận test** (RULE: có TC ≠ đã test). Ghi chú của chính TC còn ghi *"CONFLICT chưa kiểm chứng: cơ chế phân biệt 404 vs user-không-tồn-tại"*.
→ **Fix:** chạy trên môi trường có LINE thật trước khi chuyển ticket sang Closed.

**`[BLOCKER-4]` REG-SHARED-001 — Danh sách caller của Dev thiếu 2 đường cũng set rich menu cho friend qua LINE API**
Ngoài `chatEditRichMenu` (đã fix) và `FriendlistController::saveRichMenu` (Dev khai ngoài phạm vi), còn:
- **Multi action ở chat 1:1** — gắn/gỡ rich menu cho friend (bằng chứng: [kho-tcs/fa001](../../kho-tcs/fa001-chat11-11チャット.md) `TC-CHT-237`; [kho-tcs/fa004](../../kho-tcs/fa004-richmenu-リッチメニュー.md) `TC-RM-421`, `TC-RM-422` ghi rõ 3 đường *"multi action / right bar chat 1:1 / friend list"*).
- **Job hiển thị / dừng rich menu** — `SettingDisplayRichMenuHistoriesTask` gọi `POST /v2/bot/richmenu/bulk/link` theo lô 500 user rồi cập nhật `bot_line_user.rich_menu_id` (`spec-features/admin/rich-menu/feature-spec.md` §SCR-RCM-07 + §7).

Cả 2 đường đều gặp đúng tình huống "rich menu đã bị xóa khỏi LINE" nhưng **không nằm trong danh sách §3 file 03** và **0 TC**. `REG-SHARED-001` (**Cao**, trigger BẮT BUỘC với *"fix bug có thể tồn tại ở chức năng tương tự"*).
→ **Fix:** yêu cầu Dev bổ sung danh sách đầy đủ nơi set `bot_line_user.rich_menu_id`; bổ sung `TC-REGSHARED001-01` + `TC-JOB001-01` (§5).

**`[BLOCKER-5]` DATA-DB-001 — Không TC nào kiểm `WHERE` scope trên 2 tài khoản**
Endpoint `EP-49` **UPDATE** `bot_line_user.rich_menu_id`. `DATA-DB-001` (**Cao ★**) yêu cầu: task có UPDATE/DELETE → phải có TC kiểm `WHERE` scope trên **2 tài khoản**. `TC-OUTTRUTH001-03` chỉ kiểm 1 friend, 1 bot.
Kho đã có TC đúng chiều này: [kho-tcs/fa001](../../kho-tcs/fa001-chat11-11チャット.md) **`TC-CHT-346`** — *"Thao tác ở tab 基本情報 chỉ ảnh hưởng đúng bot đang chọn"* (cùng 1 tài khoản LINE là bạn của cả bot A và bot B).
→ **Fix:** dùng lại `TC-CHT-346` (§5 GAP-5), chạy kèm nhánh lỗi mới.
> 📌 *Ghi chú cho Leader:* fix **không sửa mệnh đề `WHERE`** của UPDATE (chỉ thêm early-return **trước** UPDATE). Nếu Leader tin vùng regression này đã ổn định, có thể hạ xuống `[MAJOR]`. Mức `[BLOCKER]` ở đây là theo đúng chữ của rule `DATA-DB-001`.

### 4.2 Major (nên fix)

- **`[MAJOR-1]`** *(BƯỚC 0.6 #1)* **Tỷ lệ pass chỉ 6/11 = 54.5%** — dưới ngưỡng 80%. 5 TC chưa chạy, trong đó **4 TC là toàn bộ các TC cần LINE thật**. Bộ kết quả hiện tại không đủ để kết luận.
- **`[MAJOR-2]` RULE-08 / ENV-003** — **100% execution ở `local`**, `staging`/`prd` 0 run. Bug này về bản chất là **bug tích hợp LINE API**; kết quả `Đạt` với LINE giả lập **không kết luận được** cho production. Dev cũng tự khai §6 file 03: *"không tái hiện được trên dev… không được phép gọi API LINE từ container"*, mức verify chỉ **`lint`**. `ENV-003` (**Cao ★**) trigger khớp (API bên thứ 3 + job nền) nhưng **0 TC** → xem §5 GAP-7.
- **`[MAJOR-3]`** *(BƯỚC 0.6 #4)* **Toàn bộ kết quả do pipeline AI tự chạy** (`last_exec.source = ai`, `by = pipeline`), `manual.results = []` — **chưa có QA người nào chạy TC nào**. Nhóm rủi ro cao (nhánh lỗi tích hợp LINE) không được người xác nhận.
- **`[MAJOR-4]`** *(BƯỚC 0.6 #5)* **9/11 TC do AI sinh (81.8%)** mà `reviewState = leader`, `reviewed = false`, 11/11 TC `status = draft` → bộ TC chưa qua duyệt của người.
- **`[MAJOR-5]` RULE-02 — Evidence gần như không có.** `artifacts` rỗng ở 5/6 TC pass (chỉ #12314 có 1 log). Cột `Evidence thực tế` rỗng ở **cả 11 TC**. Không TC nào ghi **loại evidence bắt buộc** ở `Ghi chú`. Theo RULE-02, các kết quả `Đạt` này **chưa được nghiệm thu**.
- **`[MAJOR-6]`** *(BƯỚC 0.6 #6)* **4/11 TC không map được mã quan điểm**: `RULE-12` ×2 (là RULE quy trình, không phải viewpoint), `TOOL-KNOW-002` ×1, `API-CONTRACT-001` ×1 (cả 2 không tồn tại trong `framework/checklist-lme.md`). → **Fix:** đổi `viewpoint` trên Studio: `RULE-12` → `FUNC-001`; `TOOL-KNOW-002` → `OUT-TRUTH-001`; `API-CONTRACT-001` → `OUT-TRUTH-001` hoặc `INTG-LINE-001`.
- **`[MAJOR-7]` RULE-01 — Thiếu loại case ở 3 quan điểm ưu tiên Cao, không ghi lý do:**
  - `OUT-TRUTH-001` (Cao): Normal 1 + Abnormal 2, **thiếu Boundary**.
  - `ENV-001` (Cao): Abnormal 2, **thiếu Normal + Boundary**.
  - `INTG-LINE-001` (Cao): Abnormal 1, **thiếu Normal + Boundary**.
  Toàn bộ 11 TC: Normal 3 / Abnormal 7 / **Boundary 1**.
- **`[MAJOR-8]` Auto-fill chưa được tester verify** — cả [01-bug-task.md](01-bug-task.md) và [03-dev-impact.md](03-dev-impact.md) đều có `Auto-filled: 2026-08-26 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick**. F/D/T có thể thiếu hoặc map sai → coverage matrix ở §3 chỉ có giá trị sau khi tester đọc lại Redmine và tick.
- **`[MAJOR-9]` SYMPTOM-ONLY / lệch root cause** — KH viết *"richmenu **được tạo từ phía tool khác**"*, Dev fix *"richmenu **bị xóa** bởi tool khác"*. Cần hỏi Dev/PM: khi tool ngoài **tạo** rich menu trên LINE OA (LME không có bản ghi), màn chat 1:1 hiển thị gì? Đó có phải case khách gặp không? TCs hiện chỉ cover 1 root cause.
- **`[MAJOR-10]` AP-4 — Không có link PR để verify fix shape.** Mục "Commit / Pull Request" chỉ có commit hash + dashboard nội bộ. Không đọc được diff → không xác nhận được nhánh nào là early-return, nhánh nào là catch, `isRichMenuDeletedOnLine` bắt exception ra sao. → Yêu cầu Dev cung cấp link diff.
- **`[MAJOR-11]` Thiếu TC cho "unknown error" — nhánh KHÔNG đi qua try/catch của controller.** Fix chỉ đảm bảo `msg` có nội dung **ở các nhánh controller đã handle**. Với HTTP 500 (PHP fatal), 419 CSRF, session hết hạn, mất mạng giữa chừng → response không có field `msg` → FE `alert(response.msg)` **vẫn hiện 「undefined」**, tức bug gốc **chưa được đóng hoàn toàn**. FE **không được sửa** nên đây là câu hỏi phạm vi cho Dev/Leader, không phải TC test layer FE. → §5 GAP-8 + §6.
- **`[MAJOR-12]` SPEC-CONFLICT — "Rich menu mặc định" đã bị bỏ khỏi tính năng.** [kho-tcs/fa004](../../kho-tcs/fa004-richmenu-リッチメニュー.md) **MT-25 (CAO, ✅ ĐÃ CHỐT)**: *"**KHÔNG còn khái niệm Richmenu mặc định ở tính năng này**"* — đợt improve 09/2025 đã bỏ, màn setting mới chỉ còn 表示する/停止する, không có nút đặt mặc định. Nhưng **REQ-002**, `TC-OUTTRUTH001-02` và `TC-RULE12-02` đều xây quanh `$richDefault` (`status_rich=1 & status_line=1`). → Nhánh này có thể **chỉ tồn tại với dữ liệu legacy**; TC pass ở `local` nhiều khả năng do pipeline seed thẳng DB, **không phản ánh đường vào thật của người dùng**. Đưa vào §6.
- **`[MAJOR-13]` SPEC-CONFLICT — rich menu có `rich_menu_id` rỗng có chọn được từ modal chat 1:1 không?** `spec-features/admin/rich-menu/feature-spec.md` **BR-05** (tin cậy **Cao**): *"Chỉ `step_active=4` + `rich_menu_id NOT NULL` mới coi là hoàn chỉnh"* (`scopeIgnoreRichNoneSetting`). Nếu scope này áp cho danh sách chọn ở chat 1:1 thì **2 nhánh early-return mới (REQ-001/REQ-002) là đường không tới được từ UI** — tức 2 TC `pass` duy nhất đang kiểm code chết, còn đường thật (404) thì chưa chạy. Đưa vào §6.
- **`[MAJOR-14]` Regression chưa cover — message 「表示期間外」 cùng modal.** [kho-tcs/fa001](../../kho-tcs/fa001-chat11-11チャット.md) `TC-CHT-344` ghi: chọn rich menu **hết thời gian hiển thị** ở tab 基本情報 → hiện 「選択したリッチメニューは表示期間外の設定となっています。表示期間設定をご確認下さい。」. Đây là **message lỗi có sẵn trong cùng function vừa bị sửa**; fix thêm 2 early-return **trước** đoạn này. Không TC nào verify message cũ không bị nuốt/đổi thứ tự. → §5 GAP-6 (dùng lại kho).
- **`[MAJOR-15]` RULE-06 — Không TC nào đi tới output cuối trên LINE app thật.** Rich menu là thứ hiển thị **trên máy friend**. Cả 11 TC dừng ở popup + DB. Kho có `TC-CHT-345` (*"OK: rich menu biến mất trên app LINE của friend"*, môi trường PRODUCTION) làm chuẩn. Riêng nhánh lỗi cần khẳng định: báo lỗi thì rich menu trên app friend **không được đổi**. → §5 GAP-4.
- **`[MAJOR-16]` Run `561` đang `queued`** — kết quả review này chốt trên run 436. Cần xác nhận 561 là gì (chạy lại cùng bộ? thêm TC mới?) trước khi Leader ký.
- **`[MAJOR-17]` AP-3 — Regression chỉ có happy path.** T1/T2 mỗi impact 1–2 TC, precondition đều "rich menu hợp lệ / friend bình thường". Không có regression ở edge state: friend đã block, bot free plan, 2 bot, rich menu ngoài thời gian hiển thị, rich menu đang tắt.
- **`[MAJOR-18]` Toàn bộ 11 TC có `Trạng thái đánh giá spec` = rỗng** (`spec_status = null`). Nhiều TC đang tự suy hành vi đúng từ code (`empty($richIdForLine)`, `~2701-2706`) mà không ghi đã hỏi ai — nguy cơ tự suy diễn rồi cho Đạt. Với `[MAJOR-12]`/`[MAJOR-13]` chưa chốt, ít nhất `TC-OUTTRUTH001-02`, `TC-RULE12-02`, `TC-TOOLKNOW002-01` phải là `Đã hỏi leader`.
- **`[MAJOR-19]` Studio tự khai coverage `0/3 covered` (3 partial)** — `SCR-CHT-01`, `EP-49`, `TICKET-39454` đều `partial`. Chính hệ thống nguồn cũng không coi bộ TC là đủ phủ.

### 4.3 Minor (có thể fix sau)

- **`[MINOR-1]`** `TC-ENV001-01` và `TC-ENV001-02` có **`Kết quả mong đợi` giống hệt nhau** (cùng message 「リッチメニューの設定に失敗しました…」). Khác biệt duy nhất nằm ở **cách dựng điều kiện**, mà steps ghi khá chung (*"Làm cho lời gọi… cũng không kết nối được"*). Người chạy rất dễ chạy trùng 1 lần rồi tick cả 2. → Bổ sung vào steps cách dựng cụ thể (chặn host `api.line.me` ở tầng nào, dùng token nào).
- **`[MINOR-2]`** `requirement_keys` **rỗng** ở 2 TC do người bổ sung (`TC-OUTTRUTH001-01` #13617, `TC-ENV001-02` #13616) → không tự map được vào REQ, phải suy tay. `TC-ENV001-02` thực chất cover REQ-005, `TC-OUTTRUTH001-01` không có REQ tương ứng (đề nghị tạo REQ-011 cho vế "recovery bằng edit/save").
- **`[MINOR-3]`** `TC-ENV001-01` (#12308) khai `requirement_keys = [REQ-004, REQ-005]` nhưng `note` của chính nó ghi *"Chỉ kiểm REQ-004"* → nhãn REQ sai, làm REQ-005 trông như đã có 2 TC.
- **`[MINOR-4]`** `priority` = `null` ở 9/11 TC (chỉ 2 TC người bổ sung có `Medium`).

### 4.4 Nit (gợi ý)

- **`[NIT-1]`** TC No. gốc trên Studio dùng `temp_id` dạng `NEW-1…NEW-11`, không theo format repo `TC-<mã quan điểm bỏ gạch>-<nn>`. File [04-tc-list.md](04-tc-list.md) đã chuẩn hoá khi snapshot — nếu muốn thống nhất 2 chiều thì đặt `client_ref` theo format repo trên Studio.
- **`[NIT-2]`** `sort_order` hiện xếp 2 TC regression (`TC-RULE12-01/02`) lên đầu, đẩy TC tái hiện bug xuống giữa. Đọc bộ TC không thấy ngay TC nào là "TC của bug". Cân nhắc `testcase_resort`.
- **`[NIT-3]` (RULE-11)** Các mục §4 `checklist-lme.md` ("quan điểm chưa đủ bằng chứng" — CHAT-01) chỉ nêu ở mức gợi ý, **không** dùng để flag ở report này.

---

## 4.5 TC trùng lặp nội dung

**Đã rà toàn bộ 11 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `điều kiện tiền đề tương đương` → `kết quả mong đợi`). Kết quả: **1 nhóm `DUP-INFLATE`, 1 nhóm `DUP-SUBSET`, 0 `DUP-EXACT`, 0 `DUP-CONFLICT`.**

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| **N1** — nhánh lỗi ở tầng API vs tầng UI | `TC-TOOLKNOW002-01` (#12306, dataset A) · `TC-INTGLINE001-01` (#12309, dataset B) · `TC-ENV001-01` (#12308, dataset C) | `TC-APICONTRACT001-01` (#12314) — **KHÔNG xóa**, đề nghị **tách thành 3 lần chạy có evidence riêng** | **`DUP-INFLATE`** | Cùng đối tượng+thao tác (`POST /basic/chat-edit-rich-menu`, 3 nhóm lỗi), cùng tiền đề dựng lỗi, expected là **hợp của 3 TC UI**, chỉ khác tầng quan sát (JSON vs popup) | **`[MAJOR]`** — trùng đang **che GAP**: #12314 làm dataset B (404) + C (401) trông như đã có TC ở tầng API, trong khi evidence run 436 chỉ chứng minh dataset A. **Coverage mở lại**: REQ-003 và REQ-004 ở tầng API hạ xuống **RISK/GAP** |
| **N2** — cùng nhánh "id LINE rỗng khi đổi rich menu" | `TC-TOOLKNOW002-01` (#12306) — oracle: nội dung message + không gọi LINE API | `TC-DATATEXT001-01` (#12313) — **KHÔNG xóa**, chỉ **tách oracle rõ hơn** | **`DUP-SUBSET`** (một phần) | Trùng tiền đề (chính #12313 ghi *"Như TC đổi sang rich menu có id LINE rỗng"*), trùng đối tượng+thao tác, expected của #12313 chứa lại toàn bộ chuỗi message mà #12306 đã assert; khác `mã quan điểm` (TOOL-KNOW-002 vs DATA-TEXT-001) và `loại case` (Abnormal vs Boundary) | **`[MINOR]`** |

**Gate trước khi đề nghị xóa (đã chạy):**
- Xóa `TC-APICONTRACT001-01` → mất toàn bộ cover ở **tầng API** và **REQ-006** (không TC nào khác là `tc_group = api`) → **chuyển từ "xóa" sang "tách/gộp"**. ✅
- Xóa `TC-DATATEXT001-01` → mất **TC `Boundary` duy nhất** của cả bộ và mất cover `DATA-TEXT-001` → **giữ nguyên**. ✅
- **Không TC nào bị đề nghị xóa.**

---

## 5. TCs đề xuất bổ sung

> **Đã đối chiếu 11 TC ở BƯỚC 0 + [kho-tcs/fa001-chat11-11チャット.md](../../kho-tcs/fa001-chat11-11チャット.md) (FA-001, 430+ TC) + [kho-tcs/fa004-richmenu-リッチメニュー.md](../../kho-tcs/fa004-richmenu-リッチメニュー.md) (FA-004, 474+ TC) — không TC đề xuất nào trùng** (kiểm theo 4 yếu tố với cả bộ BƯỚC 0 và với các TC khác trong chính §5).

### 5.1 GAP dùng lại TC có sẵn trong kho — KHÔNG viết TC mới

| GAP | Dùng lại | Tên case | Cần chỉnh gì cho bug này |
|---|---|---|---|
| **GAP-5** (lấp `[BLOCKER-5]` DATA-DB-001) | [`TC-CHT-346`](../../kho-tcs/fa001-chat11-11チャット.md) | *Thao tác ở tab 基本情報 chỉ ảnh hưởng đúng bot đang chọn* | Thêm 1 vòng chạy với **rich menu có id LINE rỗng / đã bị xóa trên LINE** ở bot A → khẳng định `bot_line_user.rich_menu_id` của **cùng tài khoản LINE ở bot B** không bị chạm ở cả nhánh lỗi |
| **GAP-6** (lấp `[MAJOR-14]`) | [`TC-CHT-344`](../../kho-tcs/fa001-chat11-11チャット.md) | *Gán rich menu cho bạn bè từ tab 基本情報* (đã có bước 3–4: R3 đang tắt không hiện trong danh sách; R4 ngoài thời gian hiển thị → 「表示期間外」) | Chạy lại nguyên trạng trên branch fix để khẳng định 2 hành vi cũ **không regress** sau khi thêm 2 early-return. Đồng thời **bước 3 của TC này chính là câu trả lời cho `[MAJOR-13]`** — quan sát rich menu có `rich_menu_id` rỗng có xuất hiện trong danh sách chọn không |

### 5.2 TC mới (16 cột canonical)

> 🔻 **Leader đã bỏ 2 TC khỏi đề xuất (2026-08-26)**: `TC-INTGLINE001-02` (Boundary — rich menu bị xóa đúng lúc đang thao tác) và `TC-ENV003-01` (chạy lại toàn bộ nhánh trên môi trường có LINE thật).
> **Hệ quả cần biết**: `INTG-LINE-001` (Cao) **vẫn thiếu Normal + Boundary** → `[MAJOR-7]` RULE-01 chưa được đóng; `ENV-003` (Cao ★) **vẫn ở trạng thái GAP** → `[MAJOR-2]` RULE-08 phải được đóng bằng cách **ràng buộc môi trường chạy** của 6 TC dưới đây (`STAGING` / `PRODUCTION`), không có TC riêng để truy vết.
>
> ✅ **6 TC dưới đây đã được sync lên MCP LME TEST STUDIO — task #185, ngày 2026-08-26** (`testcase_create`, actor `@mcp`, `status = draft`, chèn sau `#12314`):
>
> | TC No. (report) | Studio ID | `temp_id` | `client_ref` |
> |---|---|---|---|
> | `TC-MSG003-01` | **#14020** | NEW-12 | `review39454-msg003-blocked-friend-404` |
> | `TC-OUTTRUTH001-04` | **#14021** | NEW-13 | `review39454-outtruth-friendlist-bulk` |
> | `TC-REGSHARED001-01` | **#14022** | NEW-14 | `review39454-regshared-multiaction` |
> | `TC-JOB001-01` | **#14023** | NEW-15 | `review39454-job001-schedule-display` |
> | `TC-OUTTRUTH001-05` | **#14024** | NEW-16 | `review39454-outtruth-line-app-unchanged` |
> | `TC-UI003-01` | **#14025** | NEW-17 | `review39454-ui003-unknown-error` |
>
> Task #185 giờ có **17 TC**. `client_ref` là idempotent key — chạy lại `testcase_create` với cùng key sẽ **reuse**, không tạo bản trùng.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-MSG003-01 | MSG-003 | Abnormal | Friend đã block bot — đổi rich menu KHÔNG được báo nhầm là "rich menu đã bị xóa" | Bot LINE thật (staging/production). Có rich menu R1 **đang tồn tại hợp lệ trên LINE** (đã đăng ký, chưa bị xóa). Có friend F1 đã kết bạn rồi **chủ động block bot** từ app LINE. Ghi lại rich menu hiện tại của F1 trên panel. | 1. Mở màn chat 1:1, chọn friend F1 (đang block)<br>2. Ở panel 基本情報, ô Rich menu bấm nút đổi rich menu<br>3. Chọn R1 (rich menu hợp lệ, còn trên LINE) rồi bấm lưu<br>4. Đọc **nguyên văn** nội dung popup hiện ra<br>5. Kiểm tra lại ô Rich menu trên panel sau khi đóng popup | Friend F1 ở trạng thái block · rich menu R1 có `rich_menu_id` LINE hợp lệ và **vẫn tồn tại** trên LINE Official Account | Popup **KHÔNG** được hiện 「LINE公式アカウントからリッチメニューが削除されました…該当のリッチメニューを編集・保存すると、再作成できます。」 vì rich menu R1 thực tế **vẫn còn** trên LINE. Phải hiện thông báo phản ánh đúng nguyên nhân (friend đã block / không thao tác được), hoặc tối thiểu là message chung 「リッチメニューの設定に失敗しました。時間をおいて再度お試しください。」. Không hiện 「undefined」, không HTTP 500. Ô Rich menu trên panel giữ nguyên giá trị trước thao tác. | Chưa test | | STAGING → **PRODUCTION** | | | | Spec không ghi — cần hỏi leader (S3) | **Lấp `[BLOCKER-1]` · GAP-10** — cover `MSG-003` (Cao) hiện GAP hoàn toàn. Đây là **rủi ro do chính Dev nêu** ở §7 file 03: 404 từ LINE có thể sinh ra vì user chứ không phải rich menu. Cover impact `F2` (nhánh `isRichMenuDeletedOnLine` trả 404 sai ngữ cảnh) + `BUG`. **Evidence bắt buộc**: screenshot popup nguyên văn + log request/response LINE API (mã lỗi thật) + screenshot panel trước/sau. Nếu kết quả cho ra message "đã bị xóa" → **raise ticket mới**, không được cho Đạt |
| TC-OUTTRUTH001-04 | OUT-TRUTH-001 | Abnormal | Màn danh sách bạn bè — đặt rich menu hàng loạt khi rich menu đã bị xóa trên LINE báo kết quả gì | Bot LINE thật. Rich menu R3 có `rich_menu_id` LINE nhưng **đã bị xóa khỏi LINE**. Có ≥ 3 friend hiển thị ở màn danh sách bạn bè. Ghi lại rich menu hiện tại của 3 friend đó. | 1. Mở màn danh sách bạn bè, chọn 3 friend<br>2. Chọn thao tác đặt rich menu hàng loạt, chọn R3<br>3. Xác nhận và thực thi<br>4. Đọc nguyên văn thông báo kết quả trên màn danh sách<br>5. Mở chat 1:1 của từng friend, kiểm tra ô Rich menu trên panel<br>6. Kiểm tra rich menu thực tế trên app LINE của 1 friend test | Rich menu R3 đã bị xóa khỏi LINE Official Account · 3 friend | Hệ thống **KHÔNG được báo thành công** khi thực tế không gán được. Thông báo phải khớp trạng thái thật (báo lỗi hoặc báo rõ số thành công / số thất bại). Ô Rich menu trên panel của 3 friend phản ánh đúng kết quả thật, không hiển thị R3 nếu chưa gán được. Rich menu trên app LINE của friend không đổi. | Chưa test | | STAGING → **PRODUCTION** | | | | Spec không ghi — cần hỏi leader | **Lấp GAP `F4`** (impact duy nhất status GAP ở §3) + hỗ trợ `[BLOCKER-4]`. Dev tự khai `FriendlistController::saveRichMenu` **"nuốt lỗi theo kiểu khác (vẫn trả thành công)"** — TC này để **ghi nhận hiện trạng và chốt phạm vi**, không phải verify fix. Nếu ra kết quả "báo thành công dù thất bại" → **raise ticket mới**, đây là lỗi nặng hơn 「undefined」. **Evidence bắt buộc**: screenshot thông báo + screenshot panel 3 friend + ảnh app LINE |
| TC-REGSHARED001-01 | REG-SHARED-001 | Abnormal | Multi action ở chat 1:1 — gắn rich menu đã bị xóa trên LINE báo đúng kết quả | Bot LINE thật. Rich menu R3 đã bị xóa khỏi LINE (như TC trên). Friend F3 đang gắn rich menu R_cũ. Multi action đã cấu hình sẵn action gắn rich menu R3. | 1. Mở chat 1:1 của F3<br>2. Mở modal multi action, chọn action gắn rich menu R3<br>3. Thực thi multi action<br>4. Đọc nguyên văn thông báo kết quả<br>5. Kiểm tra ô Rich menu trên panel 基本情報 của F3<br>6. Kiểm tra rich menu thực tế trên app LINE của F3 | Rich menu R3 đã bị xóa khỏi LINE · friend F3 đang gắn R_cũ | Thông báo khớp trạng thái thật — không báo thành công khi LINE không nhận. Ô Rich menu của F3 vẫn hiển thị R_cũ, không bị đổi sang R3 và không bị xoá trắng. Rich menu trên app LINE của F3 vẫn là R_cũ. Không hiện 「undefined」. | Chưa test | | STAGING → **PRODUCTION** | | | | Spec không ghi — cần hỏi leader | **Lấp `[BLOCKER-4]`** — đường **multi action** set rich menu cho friend **không có trong danh sách caller §3 file 03**. `regression` — dẫn từ [`TC-CHT-237`](../../kho-tcs/fa001-chat11-11チャット.md) (multi action gắn/gỡ rich menu) và [`TC-RM-421`](../../kho-tcs/fa004-richmenu-リッチメニュー.md) (*"Set rich menu qua multi action / right bar chat 1:1 / friend list"*). **Evidence bắt buộc**: screenshot thông báo + panel + ảnh app LINE |
| TC-JOB001-01 | JOB-001 | Abnormal | Job hiển thị rich menu theo lịch — rich menu bị xóa khỏi LINE thì job không nuốt lỗi | Bot LINE thật. Rich menu R4 đã đăng ký hợp lệ lên LINE. Đặt lịch hiển thị R4 cho ≥ 20 friend (màn `リッチメニュー表示・停止の設定`, kiểu 日時を設定する, thời điểm cách hiện tại vài phút). Trước giờ chạy, **xóa R4 khỏi LINE Official Account**. Ghi lại rich menu hiện tại của các friend. | 1. Chờ tới thời điểm job chạy<br>2. Mở màn 操作予約・履歴 đọc trạng thái bản ghi lịch<br>3. Kiểm tra ô Rich menu trên panel của vài friend trong tập đối tượng<br>4. Kiểm tra rich menu thực tế trên app LINE của 1 friend test<br>5. Đối chiếu số friend trong tập đối tượng với số friend thực sự được gán | Rich menu R4 bị xóa trên LINE **trước** khi job chạy · tập đối tượng ≥ 20 friend | Job **không dừng giữa chừng và không báo hoàn tất sai sự thật**. Trạng thái bản ghi lịch phản ánh đúng kết quả (lỗi / hoàn tất một phần), không tự nhảy sang hoàn tất khi LINE từ chối. Rich menu trên panel và trên app LINE của friend **không bị đổi sang R4**. Số friend gán thành công đối chiếu được với số friend trong tập đối tượng, không bản ghi nào biến mất im lặng. | Chưa test | | STAGING → **PRODUCTION** | | | | Spec không ghi — cần hỏi leader | **Lấp `[BLOCKER-4]` + `[MAJOR-2]`** — đường **job nền** cũng set `bot_line_user.rich_menu_id` qua `POST /v2/bot/richmenu/bulk/link` (`spec-features/admin/rich-menu/feature-spec.md` §SCR-RCM-07 + §7), **không có trong danh sách caller**. `regression` — dẫn từ [`TC-RM-421`, `TC-RM-422`](../../kho-tcs/fa004-richmenu-リッチメニュー.md). **Evidence bắt buộc**: log job (thấy lỗi LINE + retry nếu có) + bảng đối chiếu số friend vào/ra + screenshot màn lịch sử |
| TC-OUTTRUTH001-05 | OUT-TRUTH-001 | Abnormal | Khi popup báo lỗi, rich menu trên app LINE của friend KHÔNG được đổi | Bot LINE thật + **thiết bị LINE thật** của friend F4. F4 đang hiển thị rich menu R_cũ trên app LINE (mở app xác nhận trước). Rich menu R5 đã bị xóa khỏi LINE Official Account. | 1. Mở app LINE trên máy F4, chụp màn hình rich menu hiện tại (R_cũ)<br>2. Trên LME, mở chat 1:1 của F4, đổi rich menu sang R5, bấm lưu<br>3. Xác nhận popup báo lỗi hiện ra<br>4. Trên máy F4, đóng và mở lại cuộc chat với bot<br>5. Chụp lại màn hình rich menu trên app LINE | Rich menu R5 đã bị xóa trên LINE · friend F4 đang hiển thị R_cũ trên app | Rich menu trên app LINE của F4 **vẫn là R_cũ**, không biến mất, không đổi sang trống. Ô Rich menu trên panel LME cũng vẫn là R_cũ — khớp với những gì friend thật sự nhìn thấy. | Chưa test | | **PRODUCTION** | | | | Spec không ghi — cần hỏi leader | **Lấp `[MAJOR-15]` RULE-06** — không TC nào trong 11 TC đi tới **output cuối trên thiết bị thật**. `OUT-TRUTH-001` yêu cầu message phải khớp trạng thái THẬT, mà trạng thái thật của rich menu nằm trên app LINE. `regression` — dẫn từ [`TC-CHT-345`](../../kho-tcs/fa001-chat11-11チャット.md) (đã có chuẩn "rich menu biến mất trên app LINE của friend", môi trường PRODUCTION). Cover `BUG`, `D1`, `T1`, `T2`. **Evidence bắt buộc**: **2 ảnh chụp màn hình app LINE trước/sau** trên máy thật |
| TC-UI003-01 | UI-003 | Abnormal | Lỗi KHÔNG đi qua xử lý của màn chat (session hết hạn / mất mạng) không được hiện 「undefined」 | Đăng nhập admin, mở chat 1:1 của 1 friend, mở sẵn modal đổi rich menu và chọn 1 rich menu hợp lệ. Chuẩn bị 3 tình huống: (a) để phiên đăng nhập hết hạn (hoặc đăng xuất ở tab khác) trước khi bấm lưu; (b) ngắt mạng máy trạm ngay trước khi bấm lưu; (c) bấm lưu 2 lần liên tiếp thật nhanh. | 1. Với **từng** tình huống (a)(b)(c): dựng điều kiện rồi bấm lưu<br>2. Đọc nguyên văn nội dung popup / thông báo hiện ra<br>3. Ghi lại có màn trắng, loading vô hạn hay không<br>4. Sau mỗi lần, đăng nhập lại và kiểm tra ô Rich menu trên panel | (a) session hết hạn · (b) mất kết nối mạng · (c) double-click nút lưu | **Không tình huống nào** hiện 「undefined」. Mỗi tình huống có thông báo đọc hiểu được (hết phiên / lỗi kết nối / đang xử lý), **không màn trắng, không loading vô hạn**. Ô Rich menu của friend giữ nguyên giá trị trước thao tác ở cả 3 tình huống; tình huống (c) không tạo 2 lần cập nhật. | Chưa test | | STAGING | | | | Spec không ghi — cần hỏi leader | **Lấp `[MAJOR-11]`** — đây là **"unknown error fallback"** mà fix-shape generic-catch bắt buộc phải có. Fix chỉ thêm `msg` **trong** try/catch của controller; các lỗi không tới được controller vẫn khiến màn chat đọc `response.msg` thành undefined → **bug gốc chưa đóng hoàn toàn**. TC này quan sát hoàn toàn ở UI, không đòi sửa FE. Cover `BUG`, `F3`. **Evidence bắt buộc**: screenshot popup của **cả 3** tình huống |

**Chống trùng (BƯỚC 5b) — đã kiểm:**
- vs 11 TC BƯỚC 0: 6 TC đề xuất đều khác bộ TC BƯỚC 0 ở ít nhất 1 trong 4 yếu tố — `TC-MSG003-01` khác nguyên nhân sinh 404; `TC-OUTTRUTH001-04` / `TC-REGSHARED001-01` / `TC-JOB001-01` khác **đường vào** (friend list / multi action / job nền, không phải panel chat 1:1); `TC-OUTTRUTH001-05` khác **tầng quan sát** (app LINE thật); `TC-UI003-01` khác **loại lỗi** (lỗi không đi qua try/catch của controller).
- vs các TC khác trong §5: `TC-REGSHARED001-01` (multi action) và `TC-OUTTRUTH001-04` (friend list) là **2 đường vào khác nhau**, không gộp. `TC-OUTTRUTH001-05` (app LINE) tách khỏi `TC-MSG003-01` vì khác nguyên nhân lỗi và khác oracle.
- vs kho: GAP-5 và GAP-6 đã chuyển sang **dùng lại** `TC-CHT-346` / `TC-CHT-344` thay vì viết mới.

---

## 6. Spec update needed

| # | Điểm cần chốt | Bằng chứng | Ai chốt |
|---|---|---|---|
| **S1** | **"Rich menu mặc định" còn tồn tại không?** Fix xây 1 nhánh riêng quanh `$richDefault` (`status_rich=1 & status_line=1`) cho REQ-002, nhưng [kho-tcs/fa004](../../kho-tcs/fa004-richmenu-リッチメニュー.md) **MT-25 đã CHỐT: "KHÔNG còn khái niệm Richmenu mặc định ở tính năng này"** (bỏ ở đợt improve 09/2025; màn setting mới chỉ còn 表示する/停止する). Nếu đúng vậy thì `TC-OUTTRUTH001-02` và `TC-RULE12-02` đang test **code chết / chỉ chạm được bằng dữ liệu legacy**. | `spec-features/admin/rich-menu/feature-spec.md` BR-04 + §SCR-RCM-07 "Luồng: Đặt làm mặc định" (EP-32/EP-33) vs kho MT-25 (✅ ĐÃ CHỐT) | **Dev + Leader** |
| **S2** | **Rich menu có `rich_menu_id` rỗng có chọn được từ modal chat 1:1 không?** `BR-05` (tin cậy **Cao**): *"Chỉ `step_active=4` + `rich_menu_id NOT NULL` mới coi là hoàn chỉnh"* (`scopeIgnoreRichNoneSetting`). Nếu scope này áp cho danh sách chọn ở chat 1:1 → REQ-001/REQ-002 là **đường không tới được từ UI**, và 2 TC `pass` duy nhất đang kiểm nhánh không xảy ra thật. Kho `TC-CHT-344` bước 3 đã có tiền lệ: rich menu **đang tắt KHÔNG xuất hiện trong danh sách chọn**. | `spec-features/admin/rich-menu/feature-spec.md` BR-05 · [`TC-CHT-344`](../../kho-tcs/fa001-chat11-11チャット.md) | **Dev** |
| **S3** | **404 từ LINE có đủ để kết luận "rich menu bị xóa" không?** Dev tự nêu rủi ro (§7 file 03) nhưng không có phương án phân biệt với 404 do user (block / không tồn tại). Cần chốt hành vi mong đợi để làm oracle cho `TC-MSG003-01`. | §7 file 03 (nguyên văn) · `INTG-LINE-001` (Cao) · `MSG-003` (Cao) | **Dev + Leader** |
| **S4** | **Phạm vi: FE `alert(response.msg)` có được hardened không?** Nếu không, mọi nhánh lỗi tương lai không kèm `msg` (HTTP 500 / 419 / session hết hạn) sẽ **tái hiện lại đúng bug 「undefined」**. Cần chốt: đóng ticket ở mức BE thôi, hay bổ sung fallback ở FE. | §3 file 03 (Dev đã check `chat-v2.js` nhưng không sửa) · `[MAJOR-11]` | **Leader + Dev** |
| **S5** | **`FriendlistController::saveRichMenu` — cùng lớp lỗi, nặng hơn (báo thành công khi thất bại).** Dev khai ngoài phạm vi. Chốt: raise ticket riêng ngay, hay gộp vào ticket này. | §2 file 03 "Quét ngang" (nguyên văn) · `[BLOCKER-4]` | **Leader** |
| **S6** | **KH báo "richmenu được tạo từ tool khác" — Dev fix "richmenu bị tool khác xóa".** 2 kịch bản khác nhau. Cần PM/KH xác nhận đúng kịch bản trước khi đóng. | [01-bug-task.md](01-bug-task.md) "Mô tả bug" vs §1 file 03 · `[MAJOR-9]` | **PM / Leader** |
| **S7** | Message mới là **chuỗi tiếng Nhật hardcode trong controller**, chưa có file ngôn ngữ (Dev tự ghi §7). Chốt có cần đưa vào lang file không (ảnh hưởng brand Lwaka / Saruwaka / Lgram — `REG-SHARED-001`). | §7 file 03 | **Leader** |

---

## 7. Checklist đã chạy

| Mục | Kết quả | Ghi chú |
|---|---|---|
| **A.1** Bug root cause | ⚠️ **Fail một phần** | Có TC tái hiện (`TC-INTGLINE001-01`) nhưng **chưa chạy**; TC đã chạy lại là nhánh `id rỗng` — chưa chắc là đường khách gặp (S2) |
| **A.2** Function impact | ❌ **Fail** | `F4` không có TC; danh sách caller thiếu 2 đường (`[BLOCKER-4]`); `F1` Direct thiếu Boundary |
| **A.3** Data impact | ⚠️ **Fail một phần** | `D1`/`D2` có đối chứng âm nhưng chỉ ở 1/3 nhánh lỗi; **không có TC `WHERE` scope 2 tài khoản** (`[BLOCKER-5]`) |
| **A.4** Feature impact | ❌ **Fail** | `T1` 0/2 chạy, `T2` 0/2 chạy; regression đều happy path (AP-3) |
| **A.5** Gap & orphan | ✅ Pass | 0 orphan; 1 GAP (`F4`) đã ghi nhận |
| **A.6** Fix-shape adversarial | ❌ **Fail** | Xem §3.5 — thiếu unknown-error fallback, thiếu TC 404-do-nguyên-nhân-khác, không có link PR |
| **B.1** Rõ ràng | ⚠️ Một phần | Steps của `TC-ENV001-01/02` quá chung ở bước dựng lỗi (`[MINOR-1]`) |
| **B.2** Atomic | ❌ **Fail** | `TC-APICONTRACT001-01` gộp 3 dataset vào 1 TC → false-pass (`[BLOCKER-2]`) |
| **B.3** Độc lập | ⚠️ Một phần | `TC-DATATEXT001-01` và `TC-OUTTRUTH001-03` dùng tiền đề dạng *"Như TC …"* — phụ thuộc cách đọc TC khác |
| **B.4** Realistic | ⚠️ Một phần | Tiền đề "rich menu có `rich_menu_id` rỗng" chưa chắc dựng được từ UI thật (S2) |
| **C** Chất lượng bộ TC | ⚠️ Một phần | Phân bố Normal 3 / Abnormal 7 / **Boundary 1** — lệch so với gợi ý 40/35/25; không TC nào cho role/permission, multi-device, i18n |
| **D** Spec alignment | ❌ **Fail** | 2 xung đột spec chưa chốt (S1, S2); `spec_status` rỗng ở **cả 11 TC** (`[MAJOR-18]`) |
| **E** Hành chính | ⚠️ Một phần | TC No. gốc Studio không theo format repo (`[NIT-1]`); file 04 đúng folder; 11/11 TC `status = draft`, `reviewed = false` |

**Nguồn spec đã dùng** (không có `02-spec-reference.md` trong folder): (1) `spec-features/admin/rich-menu/feature-spec.md` — BR-04, BR-05, BR-08, BR-10, §SCR-RCM-07, §7 jobs, §6 LINE API calls; (2) `spec-features/admin/chat-11/feature-spec.md` — §4.3 Tab 基本情報 (rich menu ↔ `bot_line_user.rich_menu_id`), EP-49; (3) kho TCs FA-001 + FA-004. Không cần tới `lme.jp/manual` hay nguồn ngoài.

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-001` — Luồng chính đúng đặc tả | **Cao** | ◯ (đổi / dừng rich menu ở chat 1:1) | `TC-RULE12-01`, `TC-RULE12-02` *(mã Studio `RULE-12` không hợp lệ → không tính cover)* | **0/2** | 🔴 **GAP thực thi** — cả 2 TC chưa chạy **và** mã quan điểm không map được (`[MAJOR-6]`) |
| `OUT-TRUTH-001` — UI/message khớp trạng thái THẬT | **Cao** | ◯ **BẮT BUỘC** (thao tác có thông báo kết quả) | `TC-OUTTRUTH001-01/02/03` | 1/3 | ⚠️ **RISK** — **thiếu Boundary** (RULE-01, `[MAJOR-7]`); chưa verify tới app LINE (`[MAJOR-15]`) |
| `INTG-LINE-001` — Lỗi từ LINE API | **Cao** | ◯ **BẮT BUỘC** | `TC-INTGLINE001-01` | **0/1** | 🔴 **BLOCKER-3** — chưa chạy; **vẫn thiếu Normal + Boundary** (RULE-01) sau khi `TC-INTGLINE001-02` bị Leader bỏ khỏi §5 (2026-08-26) |
| `ENV-001` — Fail-safe sự cố hạ tầng | **Cao** | ◯ | `TC-ENV001-01`, `TC-ENV001-02` | 1/2 | ⚠️ **RISK** — thiếu Normal + Boundary (RULE-01) |
| `ENV-003` ★ — Khác biệt dev/staging/production | **Cao** | ◯ **BẮT BUỘC** (API bên thứ 3 + job nền) | *(không TC)* | — | 🔴 **GAP** → flag `[MAJOR-2]` theo BƯỚC 0.6 #3 (rule chuyên biệt hơn F.1); **vẫn GAP** — TC `TC-ENV003-01` đã bị Leader bỏ khỏi §5 (2026-08-26). Yêu cầu RULE-08 chuyển thành **điều kiện môi trường khi chạy 6 TC còn lại** (`STAGING` / `PRODUCTION`), không tách TC riêng |
| `MSG-003` — Xử lý blocked user | **Cao** | ◯ (404 từ LINE có thể do user block / không tồn tại) | *(không TC)* | — | 🔴 **BLOCKER-1** |
| `DATA-DB-001` ★ — WHERE scope + khóa mồ côi | **Cao** | ◯ (UPDATE `bot_line_user.rich_menu_id`) | *(không TC 2 tài khoản)* | — | 🔴 **BLOCKER-5** — dùng lại kho `TC-CHT-346` |
| `REG-SHARED-001` — Shared code / logic | **Cao** | ◯ **BẮT BUỘC** (bug tồn tại ở chức năng tương tự) | *(không TC)* | — | 🔴 **BLOCKER-4** |
| `DATA-001` — Dữ liệu phản ánh đủ ở mọi màn | **Cao** | ◯ (rich menu hiện ở panel chat, màn rich menu, app LINE) | `TC-OUTTRUTH001-03` (panel) | 1/1 | ⚠️ **RISK** — chỉ 1 màn; chưa đối chiếu màn rich menu và app LINE |
| `DATA-AUDIT-001` — Lịch sử thao tác | **Cao** | ◯ (`rich_menu_history`) | `TC-OUTTRUTH001-03`, `TC-RULE12-01` | 1/2 | ⚠️ **RISK** — nhánh 404 không có đối chứng history; chưa kiểm từ **từng nguồn** (web / multi action / job) |
| `JOB-001` ★ — Job nền gọi API ngoài | **Cao** | ◯ (regression — job hiển thị/dừng cũng link rich menu qua LINE) | *(không TC)* | — | ⚠️ `[MAJOR]` — fix **không sửa** job nên không phải BLOCKER, nhưng là vùng regression thật → §5 `TC-JOB001-01` |
| `UI-003` — Loading / rỗng / lỗi | **Trung bình → Cao** (rủi ro false success) | ◯ | *(không TC cho nhánh không có `msg`)* | — | ⚠️ `[MAJOR-11]` → §5 `TC-UI003-01` |
| `COMPAT-LEGACY-001` ★ — Dữ liệu đời cũ song song | **Cao** | ◯ (rich menu mặc định là khái niệm legacy — S1) | `TC-OUTTRUTH001-02`, `TC-RULE12-02` (chạm nhưng không phân biệt cũ/mới) | 1/2 | ⚠️ `[MAJOR-12]` — chờ chốt S1 |
| `DATA-TEXT-001` — Emoji & ký tự đặc biệt | **Trung bình** (→ Cao vì text hiển thị cho user) | ◯ | `TC-DATATEXT001-01` | 1/1 | ⚠️ **RISK** — pass ở `local`; chưa xác nhận encoding/xuống dòng trên browser thật (`UI-002`) |
| `SYNC-APP-001` — Đồng bộ Web ⇔ App | **Trung bình** | ◯ (chat 1:1 có trên app mobile) | *(không TC)* | — | ⚠️ `[MAJOR]` — hỏi Dev: app mobile có ô đổi rich menu ở màn chat không? Nếu có thì cùng lỗi và chưa được rà |
| `REG-RUN-001` — Job/dữ liệu chạy dở khi release | **Cao** | ◯ (lịch hiển thị/dừng rich menu đang chờ chạy lúc deploy) | *(không TC)* | — | ⚠️ `[MAJOR]` — gộp vào `TC-JOB001-01` |
| `UI-002` — Khác biệt trình duyệt | **Trung bình** | ◯ (popup `alert` chứa ký tự JP + `\n`) | *(không TC)* | — | ⚠️ `[MINOR]` — tối thiểu kiểm Mac Safari + Windows Chrome |
| `CONC-003` — Race ở tầng giao diện | **Trung bình** | ◯ (double-click nút lưu rich menu) | *(không TC)* | — | Đã gộp vào §5 `TC-UI003-01` tình huống (c) |
| `PERM-002` / `PERM-003` / `SEC-ISO-001` | Cao | × | — | — | Fix không đụng phân quyền; cách ly đa tài khoản đã gộp vào `DATA-DB-001` |
| `DEPLOY-ASSET-001` ★ | Cao | × | — | — | `chat-v2.js` **không được sửa** → không có asset version mới. Lý do ghi rõ (RULE-03) |
| `MEDIA-*`, `PAY-*`, `BULK-001`, `LIFF-ENTRY-001`, `NOTI-MAIL-001`, `OUT-EXPORT-001`, `PERF-LARGE-001`, `DATA-MIG-001`, `INTG-HOOK-*` | — | × | — | — | Fix chỉ đổi nội dung response lỗi của 1 endpoint; không chạm media/ảnh, thanh toán, thao tác hàng loạt sau lọc, LIFF, email, export, migration, webhook. Lý do ghi rõ (RULE-03) |
| `CHAT-01` (§4 "chưa đủ bằng chứng") | — | ◯ | — | — | **RULE-11** — chỉ nêu ở mức `[NIT]`, không dùng để flag BLOCKER/MAJOR |

---

## 8. Ký duyệt

| Vai trò | Tên | Ngày | Kết luận |
|---|---|---|---|
| Reviewer (draft) | `/review-tc` — **cần Leader verify** | 2026-08-26 | 🔴 **REJECTED** — 5 BLOCKER |
| Test Leader | | | |
| Dev xác nhận S1–S7 | | | |

### Việc cần làm ngay (theo thứ tự)

1. **Chốt S2 với Dev** — rich menu `rich_menu_id` rỗng có chọn được từ UI không. Câu trả lời quyết định 2/6 kết quả `Đạt` hiện tại có giá trị hay không.
2. **Hủy kết quả `Đạt` của `TC-APICONTRACT001-01`**, tách thành 3 dataset có evidence riêng (`[BLOCKER-2]`).
3. **Yêu cầu Dev bổ sung danh sách caller đầy đủ** (multi action + job) và link PR (`[BLOCKER-4]`, `[MAJOR-10]`).
4. **Tạo TC còn thiếu trên Studio** (`testcase_create`): **6 TC** ở §5.2 + 2 TC dùng lại kho. → ✅ **đã sync lên Studio task #185 ngày 2026-08-26**.
5. **Chạy lại toàn bộ nhánh lỗi trên staging/production với LINE thật** — điều kiện tối thiểu để nghiệm thu (RULE-08). Không còn TC riêng cho việc này; phải ràng buộc bằng cột `Môi trường test` của từng TC.
6. **Tick 2 checkbox "Tester verify auto-fill chính xác"** ở [01-bug-task.md](01-bug-task.md) và [03-dev-impact.md](03-dev-impact.md) (`[MAJOR-8]`).
7. **Kiểm tra run `561` đang `queued`** — nếu là lần chạy lại thì đọc kết quả trước khi ký (`[MAJOR-16]`).
