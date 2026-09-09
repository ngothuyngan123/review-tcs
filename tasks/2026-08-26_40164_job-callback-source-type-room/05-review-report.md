# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Task | `tasks/2026-08-26_40164_job-callback-source-type-room/` |
| Ticket | Redmine #40164 — [Job callback] Add xử lý callback tin nhắn có source.type là loại room |
| Reviewer | Test Leader (draft sinh bởi `/review-tc`) |
| Ngày review | 2026-08-26 |
| Round | 1 |
| Verdict | **REJECTED** |

---

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, task `#220`, ticket `40164` |
| Vì sao không dùng nguồn dưới | Nguồn 1 có TC → **dừng tại đây theo BƯỚC 0**. Không fetch Sheet human, không đối chiếu chéo với file `04-tc-list.md`. |
| Thời điểm fetch | 2026-08-26 (`testcase_list` + `task_get_context` + `task_get_report`) |
| Tổng TC | **27** |
| Snapshot | `04-tc-list.md` trong folder **chính là** snapshot Studio (sinh bởi `/new-task` BƯỚC 6b, đã refresh sau dedup cùng ngày) → không sinh thêm `04-tc-list.studio.md` để tránh 2 file trùng nội dung. |
| Branch Studio | `m_202608_callback_room_40164` (khớp mục 5.2 của `03-dev-impact.md`) |
| `reviewState` / `reviewed` | `tester` / `false` — **chưa qua vòng review nào** |

### 0.6 — Cảnh báo bắt buộc về chất lượng nguồn

| # | Nội dung | Kết quả | Flag |
|---|---|---|---|
| 1 | **Kết quả thực thi thật** | `pass` **1/27 = 3.7%**. 26 TC còn lại chưa chạy lần nào. | **[BLOCKER]** (< 50%) |
| 2 | **TC fail / error / gắn ticket bug** | 0 TC `fail`, 0 bug ticket. **NHƯNG** `task_get_report` cho thấy **cả 2 lần chạy pipeline đều không thành công ở mức run**: run `#562` status = `fail`, run `#542` status = `error` (counts rỗng). | **[MAJOR]** |
| 3 | **Môi trường đã chạy** | 100% `local`. Production **0 TC**, staging **0 TC**. `env_tag` = `local-only` (25 TC) / `read-only` (2 TC). Task là **job nền callback** → thuộc nhóm bắt buộc production. | **[BLOCKER]** RULE-08 / ENV-003 |
| 4 | **Ai chạy** | `last_exec.source = ai`, `by = pipeline-resume`. **Không có TC nào do QA người chạy.** `submittedWithoutMcp = false`. | **[MAJOR]** |
| 5 | **Tác giả TC** | `toolWritten`: tool **27/27 (100%)**, human 0, mcp 0. `author = AI`, `provenance.source = ai`, `created_job_id` 682/743. `reviewed = false`. | **[MAJOR]** |
| 6 | **Mã quan điểm không có trong `checklist-lme.md`** | **5 mã / 8 TC (30%)**: `TOOL-KNOW-002` (2) · `TOOL-ERRHYG-001` (2) · `JOB-002` (2) · `STATE-MATRIX-001` (1) · `API-001` (1). | 8 TC này **KHÔNG tính là cover** ở §3 và §7 F.1 |

**Độ phủ spec theo Studio** (`task_get_report.coverage`): **0/67 covered**, 18 partial, **49 none**. Lưu ý diễn giải: 49 mục `none` là EP/BR của **toàn feature `chat`**, task fix-bug này không có nghĩa vụ phủ hết — nhưng con số `covered = 0` (không mục nào phủ **đầy đủ**) vẫn là tín hiệu bộ TC chỉ chạm bề mặt.

---

## 1. Verdict

**REJECTED** — có 6 `[BLOCKER]`.

Không phải vì TC viết kém: nội dung 27 TC khá chắc, oracle bám code (`DELIMITER_MEMBER_NAME_ROOM = ', '`, `MAX_MEMBER_NAME_ROOM = 5`, `TextUtils.isEmpty`, `status` 2/9/10), và bộ TC đã tự bắt được 2 ranh giới scope mà `03-dev-impact.md` bỏ sót. Vấn đề nằm ở **3 chỗ khác**: (a) 26/27 TC chưa từng chạy nên coverage mới chỉ là trên giấy; (b) toàn bộ chạy ở `local` trong khi đây là job nền — vi phạm RULE-08; (c) **thiếu hẳn nhóm quan điểm bắt buộc của một task webhook** (INTG-HOOK-001) và **thiếu đường vào chính của bug** (room đời cũ, và gửi tin từ admin vào room).

---

## 2. Tóm tắt cho member

Bộ TC bám sát diff commit `2cd86fc6`, oracle cụ thể và đo được, phần xử lý lỗi khi lấy tên room được phủ rất dày (6 nhánh lỗi khác nhau) — đây là điểm mạnh thật sự. Hai TC `NEW-19` và `NEW-22` còn chủ động ghi nhận `postback` và `memberJoined/memberLeft` **chưa được implement** dù Redmine yêu cầu, đúng tinh thần không tự suy diễn.

Phải fix trước khi approve: **chạy thật** (mới 1/27 TC có kết luận), **bổ sung nhóm webhook trùng/trễ/sai thứ tự** (bắt buộc với mọi task nhận webhook, hiện 0 TC), **bổ sung TC gửi tin từ màn chat admin vào room** (`to = roomId` — Redmine mục 3 yêu cầu, hiện 0 TC), và **bổ sung TC room đời cũ chưa có record trong DB nhận tin** — đây chính là lý do ticket tồn tại (room tạo trước LINE v10.17.0, bot đã ở sẵn nên sẽ **không bao giờ** có event `join` nữa).

---

## 3. Coverage Matrix

Nguồn impact: `03-dev-impact.md` (F1–F18 / D1–D2 / T1–T5) + BUG. Cột `Exec` = số TC `pass` / tổng TC cover impact đó.

| Impact | Loại | TCs cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|
| **BUG** — `LineCallbackSource` thiếu `roomId` → Jackson drop id | Root cause | NEW-40, NEW-30 | 2 | 0/2 | **RISK** |
| F1 `LineCallbackSource.isRoom` | Direct (mới) | NEW-40 | 1 | 0/1 | RISK |
| F2 `LineCallbackSource.getGroupOrRoomId` | Direct (mới) | NEW-33, NEW-40 | 2 | 0/2 | RISK |
| F3 `LineCallback.isSourceRoom` | Direct (mới) | NEW-40 | 1 | 0/1 | RISK |
| F4 `LineCallback.isSourceGroupOrRoom` | Direct (mới) | NEW-30, NEW-40, NEW-43 | 3 | 0/3 | RISK |
| F5 `LineCallback.getRoomId` | Direct (mới) | NEW-33 | 1 | 0/1 | RISK |
| F6 `LineCallback.getGroupOrRoomId` | Direct (mới) | NEW-33, NEW-36 | 2 | 0/2 | RISK |
| F7 `LineCallback.getGroupId` (null-safe) | Direct (sửa) | NEW-33, NEW-42 | 2 | 0/2 | RISK |
| F8 `ILineService.getRoomMemberProfile` | Direct (mới) | NEW-39, NEW-26 | 2 | 0/2 | RISK |
| F9 `ILineService.getRoomMemberIds` | Direct (mới) | NEW-39, NEW-29, NEW-25 | 3 | 0/3 | RISK |
| F10 `HandlePostbackTask.updateRoomLineProfile` | Direct (mới) | NEW-29, NEW-24, NEW-25, NEW-26, NEW-27, NEW-28, NEW-31, NEW-32 | 8 | 0/8 | RISK |
| F11 `HandlePostbackTask.getRoomMemberName` | Direct (mới) | NEW-26, NEW-27 | 2 | 0/2 | RISK |
| F12 `doHandleJoinGroup` | Direct (sửa) | NEW-35, NEW-37, NEW-21 | 3 | 0/3 | RISK |
| F13 `doHandleLeaveGroup` | Direct (sửa) | NEW-36, NEW-21 | 2 | 0/2 | RISK |
| F14 `doHandleMessage` | Direct (sửa) | NEW-30, NEW-34 | 2 | 0/2 | RISK |
| F15 `handleMessageGroup` | Direct (sửa) | NEW-30, NEW-20 | 2 | 0/2 | RISK |
| F16 `checkAddGroupFriend` | Direct (sửa) | NEW-23 | 1 | 0/1 | RISK |
| F17 `updateGroupMember` (+ `isRoom`) | Direct (sửa) | NEW-39, NEW-23, NEW-41 | 3 | 0/3 | RISK |
| F18 `checkAddGroup` (+ `isRoom`) | Direct (sửa) | NEW-35, NEW-37, NEW-42 | 3 | 0/3 | RISK |
| D1 — không đổi schema / migration / config | — | (không cần TC) | — | — | N/A |
| D2 — `line_user.type=1`, `conversation.conversation_kind=1`, phân biệt bằng prefix `R.../C...` | Runtime data | NEW-23, NEW-7 | 2 | **1/2** | **RISK** — thiếu kiểm `WHERE` scope 2 tài khoản (DATA-DB-001) |
| T1 — Chat trong room (text / sticker / ảnh) | High | NEW-30 (text), NEW-34 (ảnh) | 2 | 0/2 | **RISK** — thiếu **sticker** (Dev nêu rõ 3 loại), thiếu **room chưa có record** |
| T2 — Join / Leave room | High | NEW-35, NEW-36, NEW-37, NEW-21 | 4 | 0/4 | RISK |
| T3 — Tên hội thoại room | High | NEW-29, NEW-24, NEW-25, NEW-26, NEW-27, NEW-28, NEW-31, NEW-32 | 8 | 0/8 | RISK |
| T4 — Regression group chat | High | NEW-41, NEW-42 | 2 | 0/2 | **RISK** — chỉ happy path, không có edge state (AP-3) |
| T5 — Regression chat 1-1 **và push/reply** | High | NEW-43 (chỉ nhánh `source.type=user`) | 1 | 0/1 | **GAP một phần** — **không TC nào test push `to = roomId`** |
| — | Redmine mục 3 "Gửi tin nhắn: Push `to = roomId` khi source là room" | *(không có)* | 0 | — | **GAP** |
| — | Redmine mục 5 "UI/Admin quản lý hội thoại" | NEW-44, NEW-45 | 2 | 0/2 | RISK |

### ORPHAN TCs

**Không có.** Cả 27 TC đều trace được về BUG / F* / D* / T* hoặc ranh giới scope do Redmine description yêu cầu (`NEW-19`, `NEW-22` → REQ-013).

Riêng `NEW-40` và `NEW-33` test ở tầng model (unit) — **đúng layer của root cause**, không phải over-coverage AP-5.

---

## 3.5 Fix-shape analysis (adversarial)

Đọc mục 2 `03-dev-impact.md`. Task này khớp **5 fix shape** cùng lúc:

| # | Fix shape | Keyword trong mục 2 | Câu hỏi adversarial | Trả lời từ bộ TC | Kết luận |
|---|---|---|---|---|---|
| 1 | **webhook / callback** | toàn bộ task là "job callback", "webhook từ room" | Test webhook **trùng / trễ / sai thứ tự / KHÔNG tới**? Có log chứng minh lần thứ 2 bị bỏ qua? | **0 TC.** Không TC nào nạp cùng 1 `callback_event` 2 lần, không TC nào đảo thứ tự `join`/`leave`. | **[BLOCKER]** INTG-HOOK-001 |
| 2 | **sửa hàm dùng chung** | "checkAddGroup, updateGroupMember đổi signature (thêm param isRoom) — grep toàn repo chỉ có 3 callsite" | Có danh sách nơi ảnh hưởng do Dev cung cấp? TC test **từng nơi**? | Dev **có** cung cấp (mục 3, 3 callsite) ✔. NEW-41/42 (nhánh group), NEW-35/37 (nhánh room), NEW-23 (member) → phủ đủ 2 nhánh. Chưa rà **brand khác** (Lwaka / Saruwaka / Lgram) dùng chung job callback. | **[MAJOR]** REG-SHARED-001 |
| 3 | **thêm guard / validate** | "mọi chỗ lấy id nhóm đều đổi sang getGroupOrRoomId() **kèm guard rỗng**" | Bao nhiêu input variant? Đủ biên (thiếu field / rỗng / sai format)? | NEW-20 (message thiếu roomId), NEW-21 (join+leave thiếu roomId), NEW-33 (groupId chuỗi rỗng, không có cả hai, `source=null`) → **3 biên** ✔. Thiếu: `roomId` **sai format** (không bắt đầu bằng `R`), `roomId` quá dài. | **[MAJOR]** FUNC-003 |
| 4 | **generic catch-all** | "lấy không được thì **để rỗng và không throw**" | ≥ 3 trigger khác nhau? Có trigger **CHƯA BIẾT** để test fallback generic? | **6 trigger**: 403 (NEW-31), 429/timeout (NEW-32), token invalid (NEW-24), list rỗng (NEW-25), profile member lỗi (NEW-26), room cũ + lỗi (NEW-28) ✔ vượt ngưỡng 3. **Nhưng không có TC nào mock error code chưa handle riêng** để verify fallback generic. | **[MAJOR]** AP-1 (không lên BLOCKER vì đã ≥ 3 trigger) |
| 5 | **job nền gọi API bên thứ 3 theo lô** | "lấy tên 5 member đầu (qua `/members/ids`)" → 1 + N lời gọi API mỗi room | Test với **quy mô thực tế**? Có **retry + backoff**? `số vào = số thành công + số vào hàng đợi lỗi`? | NEW-32 test 429 nhưng **chỉ 1 event đơn lẻ**, và chính TC đó ghi nhận: *"hệ thống KHÔNG thử lại và không có backoff cho 429"*. Không TC nào chạy lô lớn / nhiều room join đồng thời. | **[MAJOR]** JOB-001 + cần Leader quyết chấp nhận thiếu backoff |

### Symptom-only KH report check

**Không dính AP-2** — nhưng theo hướng ngược lại, cũng đáng lưu ý: ticket là tracker **"Bug KH"** nhưng description **không có mục tái hiện bug, không có KH nào report triệu chứng cụ thể**. Root cause được Dev suy ra từ code (`Jackson drop roomId`), không từ ca lỗi thật. Hệ quả: **không ai biết KH thực sự gặp gì ở room** — có thể còn triệu chứng khác (tin nhắn mất, hội thoại trùng, tên hiển thị sai) mà bộ TC không nhắm tới. → `[MAJOR]`, xem ISS-09.

### Anti-patterns

| AP | Dính? | Ghi chú |
|---|---|---|
| AP-1 Single-trigger generic-fix | **Một phần** | 6 trigger ✔ nhưng thiếu unknown-error fallback → ISS-11 |
| AP-2 Symptom-only KH report | Biến thể | Không có report KH nào cả → ISS-09 |
| AP-3 Happy-path-only regression | **Dính** | T4 (group) chỉ có 2 TC precondition "data sạch": không có group đang `is_blocked=1`, group tên rỗng, group vừa leave → ISS-08 |
| AP-4 Specific code-check disguised | Không | Mục 5.1 có commit `2cd86fc6`; note các TC cho thấy đã đọc code thật (hằng số, `TextUtils.isEmpty`). Thiếu **PR link** để review diff → `[NIT]` |
| AP-5 Layer-downstream over-coverage | Không | NEW-40/NEW-33 test đúng tầng model = tầng root cause |
| AP-6 Mục 3 dev-impact trống | Không | Dev điền đầy đủ, có nêu số callsite đã grep ✔ |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**[BLOCKER] ISS-01 — Bộ TC chưa được chạy: 1/27 (3.7%)**
26/27 TC không có kết luận test nào. TC duy nhất `pass` là `NEW-7` (`#13549`), chỉ verify `line_user.type=1` bằng một câu SELECT. Toàn bộ coverage ở §3 hiện là **coverage trên giấy**.
→ *Fix*: chạy đủ 27 TC, đính evidence theo RULE-02 trước khi xin review vòng 2.

**[BLOCKER] ISS-02 — Toàn bộ chạy ở `local`, production 0 TC (RULE-08 / ENV-003)**
`envAuto`: local có run, dev/staging/prd đều 0 run. Task này là **job nền callback** — theo Catalog D, production **tách 3 job độc lập** (callback / broadcast / scenario) trong khi dev/staging chạy **1 job all**. Kết quả `pass` ở local **không chứng minh** job callback production xử lý đúng.
→ *Fix*: thêm ≥ 1 TC `Môi trường test = PRODUCTION` cho luồng room end-to-end (xem TC-ENV003-01 ở §5).

**[BLOCKER] FIX-SHAPE ISS-03 — 0 TC cho webhook trùng / trễ / sai thứ tự (INTG-HOOK-001, Cao, BẮT BUỘC)**
INTG-HOOK-001 là **bắt buộc khi nhận webhook từ bên ngoài**. Bộ TC không có TC nào: nạp cùng `callback_event` 2 lần → chỉ xử lý 1 lần; `leave` đến trước `join`; webhook đến trễ. Rủi ro cụ thể ở task này: LINE **retry webhook** khi không nhận được 200 → `join` xử lý 2 lần có tạo `line_user` trùng không? `NEW-37` test *join lại room* nhưng đó là **2 event join hợp lệ khác thời điểm**, không phải **cùng 1 event bị gửi lặp**.
→ *Fix*: thêm TC-INTGHOOK001-01/02/03 (§5).

**[BLOCKER] GAP-01 — Không TC nào test gửi tin từ màn chat admin vào room (`to = roomId`)**
Redmine description mục 3 yêu cầu rõ: *"Push: `to = roomId` khi source là room"*. `03-dev-impact.md` T5 cũng ghi *"push/reply … chạy như cũ"*. Nhưng `NEW-43` **chỉ** test `source.type = user`. Không TC nào gửi tin vào room và xác nhận **thành viên room nhận được trên LINE app thật** (RULE-06).
Đây là chiều **LME → LINE**, ngược với 27 TC hiện tại đều là chiều **LINE → LME**.
→ *Fix*: TC-MSG001-01/02/03 (§5). Kho `FA-001` đã có `TC-CHT-385` cho group — dẫn chiếu và chỉnh cho room.

**[BLOCKER] GAP-02 — Không TC nào cho room đời cũ CHƯA có record trong DB nhận tin (COMPAT-LEGACY-001, Cao)**
Đây là **lý do tồn tại của ticket**: room tạo trước LINE v10.17.0 (~05/10/2020), **bot đã ở sẵn trong room** → sẽ **không bao giờ** phát sinh event `join` nữa. Đường vào duy nhất của những room này là event `message`.
`NEW-30` (message text room) có precondition *"Bot tồn tại trong DB"* nhưng **không nói room đã có `line_user`/`conversation` hay chưa**, và expected giả định conversation đã tồn tại. Nếu `handleMessageGroup` không tự gọi `checkAddGroup` khi record chưa có → **bug gốc vẫn còn nguyên với đúng nhóm room mà ticket nhắm tới**, mà bộ TC hiện tại không phát hiện được.
Kho `FA-001` có TC tương ứng cho group: `TC-CHT-378` *"Nhóm LINE cũ (bot đã ở sẵn) gửi tin — hội thoại nhóm được tạo"*.
→ *Fix*: TC-COMPATLEGACY001-01/02 (§5) **và** hỏi Dev: `handleMessageGroup` có tạo record khi room chưa tồn tại không?

**[BLOCKER] GAP-05 — Không TC nào kiểm `WHERE` scope trên 2 tài khoản (DATA-DB-001, Cao, BẮT BUỘC với UPDATE/DELETE)**
`leave room` thực hiện **UPDATE** `conversation.is_blocked = 1`. DATA-DB-001 bắt buộc: tạo bản ghi trùng ở 2 tài khoản → update ở A → query xác nhận **B không đổi** (`WHERE` đủ `bot_id`). Kịch bản rất thực tế ở room: **2 bot của 2 khách hàng khác nhau cùng được mời vào 1 room** → cùng `roomId`, khác `bot_id`. `NEW-7`/`NEW-23` chỉ SELECT trên 1 bot.
→ *Fix*: TC-DATADB001-01/02 (§5).

### 4.2 Major (nên fix)

**[MAJOR] ISS-04 — `01-bug-task.md` và `03-dev-impact.md` chưa được tester verify**
Cả 2 file có `Auto-filled: 2026-08-26 by /new-task` nhưng checkbox *"Tester verify auto-fill chính xác"* **chưa tick**. F/D/T ở §3 đang dựa trên bản auto-fill chưa ai đối chiếu lại với Redmine.
→ *Fix*: tester đọc lại Redmine #40164 (chú ý journal `#133002`) rồi tick 2 checkbox.

**[MAJOR] ISS-05 — 27/27 TC do AI sinh, `reviewed = false`, chưa QA người nào chạy**
`toolWritten`: tool 27, human 0. `last_exec.by = pipeline-resume` (AI). `reviewState = tester`.
→ *Fix*: QA người chạy lại tối thiểu nhóm ưu tiên Cao (T1/T2/T3 + regression) và ký tên ở cột `Người thực hiện`.

**[MAJOR] ISS-06 — Cả 2 lần chạy pipeline đều không thành công ở mức run**
`task_get_report.auto.runs`: run `#562` status = `fail` (dù 16 pass / 0 fail / 2 skip tại thời điểm đó), run `#542` status = `error` (counts rỗng). Nghĩa là **harness tự nó lỗi**, không phải TC fail.
→ *Fix*: xác định nguyên nhân run lỗi trước khi tin bất kỳ con số `pass` nào; nếu do môi trường local thiếu dependency thì càng củng cố ISS-02.

**[MAJOR] ISS-07 — 8/27 TC (30%) mang mã quan điểm không có trong `checklist-lme.md`**
`TOOL-KNOW-002` (NEW-30, NEW-40) · `TOOL-ERRHYG-001` (NEW-20, NEW-21) · `JOB-002` (NEW-34, NEW-24) · `STATE-MATRIX-001` (NEW-19) · `API-001` (NEW-39). Đây là mã nội bộ Studio, **không map được coverage** sang bộ 80 quan điểm của team.
Hệ quả trực tiếp: `NEW-30` — TC verify bug root cause quan trọng nhất — mang mã `TOOL-KNOW-002`, nên ở §7 F.1 quan điểm `FUNC-001` (Cao) **không được tính là có TC** từ TC này.
→ *Fix*: gán lại mã quan điểm chuẩn trên Studio (`testcase_update`). Gợi ý: `TOOL-KNOW-002` → `FUNC-001`; `TOOL-ERRHYG-001` → `FUNC-002`; `JOB-002` → `JOB-001`; `STATE-MATRIX-001` → `STATE-001`; `API-001` → `INTG-LINE-001`.

**[MAJOR] AP-3 ISS-08 — Regression group (T4) chỉ có happy path**
`NEW-41`/`NEW-42` đều precondition "data sạch". Không có regression group ở **edge state**: group đang `is_blocked = 1`, group có tên rỗng, group vừa `leave` xong. Vì `checkAddGroup`/`updateGroupMember` **đổi signature**, chính các edge state cũ mới là chỗ nhánh `else` dễ lệch.
→ *Fix*: bổ sung ≥ 1 TC regression group ở trạng thái `is_blocked = 1`.

**[MAJOR] ISS-09 — Ticket "Bug KH" nhưng không có ca lỗi thật nào từ KH**
Description không có mục tái hiện bug; root cause do Dev đọc code suy ra. Không biết KH gặp triệu chứng gì ở room → không loại trừ được triệu chứng khác cùng nguồn gốc.
→ *Fix*: hỏi PM/KH xem có ca lỗi room thật không (tin nhắn mất / hội thoại trùng / tên sai). Nếu không có → ghi rõ vào file 01 là ticket **chủ động bổ sung tính năng**, không phải bug report, để vòng review sau không đi tìm steps tái hiện không tồn tại.

**[MAJOR] ISS-10 — Redmine yêu cầu `memberJoined`/`memberLeft` và `postback` nhưng chưa implement, `03-dev-impact.md` không nêu**
`NEW-19` và `NEW-22` đã ghi nhận đúng hành vi hiện tại (postback bị bỏ qua; `memberJoined/memberLeft` → `status = 9`). Nhưng mục 4.1/4.3 của Dev **không nhắc 2 nhánh này**, tức đánh giá ảnh hưởng **không khớp** phạm vi Redmine yêu cầu.
→ *Fix*: Leader chốt — đóng scope (sửa Redmine description) hay mở ticket bổ sung. Xem §6.

**[MAJOR] AP-1 ISS-11 — Thiếu TC trigger error code CHƯA BIẾT**
6 nhánh lỗi đã phủ, nhưng đều là lỗi **biết trước**. Mục 2 Dev mô tả fallback dạng generic ("lấy không được thì để rỗng và không throw") → cần 1 TC mock LINE API trả **mã lỗi chưa handle riêng** (VD `500`, `503`, body không phải JSON) để verify fallback thật sự generic chứ không phải chuỗi `if` các mã đã biết.

**[MAJOR] ISS-12 — JOB-001: không TC nào chạy lô lớn / rate limit thực tế**
Mỗi room join tốn `1 + N` lời gọi LINE API (`members/ids` + profile từng member). Nhiều room join đồng loạt → dễ chạm rate limit. `NEW-32` chỉ mock 429 cho **1 event**, và tự ghi nhận hệ thống **không retry, không backoff**.
→ *Fix*: TC-JOB001-01 (§5) + Leader xác nhận có chấp nhận thiếu backoff không (§6).

**[MAJOR] ISS-13 — FUNC-004 / DATA-TEXT-001: tên room ghép chưa test biên độ dài và ký tự đặc biệt**
`NEW-27` test 8 member với tên `Member1..Member8` — tên ASCII ngắn. Chưa test: tên member chứa **emoji / ký tự đặc biệt**, và **5 tên dài tối đa** nối bằng `', '` có vượt giới hạn cột `line_user.name` (`varchar(128)` theo `spec-features/admin/chat-11/db/db-mapping.md`) hay không, có bị cắt giữa ký tự multi-byte không.
→ *Fix*: TC-FUNC004-01, TC-DATATEXT001-01 (§5).

**[MAJOR] ISS-14 — Bảng `group_members` không được nhắc trong mục 4.2 nhưng liên quan trực tiếp**
`spec-features/admin/chat-11/db/db-mapping.md` mục 18: `group_members` — *"Thành viên nhóm — dùng cho `conversation_kind = 1`"*, màn chat 1:1 **Đọc** bảng này. Room dùng chung `conversation_kind = 1`. Mục 4.2 của Dev khẳng định *"Không có data bị update"* và không nhắc `group_members`.
→ *Fix*: hỏi Dev — job callback có ghi `group_members` cho room không? Nếu không, màn chat admin hiển thị thành viên room thế nào? Xem §6 + TC-DATAREF001-01.

**[MAJOR] GAP-06 — Event `unsend` KHÔNG có TC nào, cho cả room / group / 1-1**
Rà ma trận **event type × source type** trên 45 TC: `unsend` trống hoàn toàn ở cả 3 nguồn. Đây là event **có `source`** (user/group/room) giống hệt `message`/`join`/`leave` — tức là một callback `source.type = room`, **nằm đúng phạm vi mục tiêu của ticket** (*"xử lý callback tin nhắn có source.type là loại room"*), nhưng cả Redmine description lẫn mục 4.1 của Dev đều không nhắc tới.
Bằng chứng hệ thống có xử lý `unsend`: kho `FA-001` `TC-CHT-55/56/57/274` — tin bị thu hồi đổi thành 「友だちがメッセージを送信取り消しました」, thời gian giữ nguyên. Cả 4 TC kho đều là **chat 1-1**.
Rủi ro cụ thể: nếu handler `unsend` lấy id hội thoại bằng `getGroupId()` (đúng cách `doHandleLeaveGroup` làm **trước** fix) → `unsend` trong room không tìm được hội thoại → tin thu hồi vẫn hiển thị ở màn admin. Đây là **cùng một lớp bug** với ticket, chỉ khác event.
→ *Fix*: TC-MSGUSER001-01 (room) · TC-REGSHARED001-02 (group) · TC-REGSHARED001-03 (1-1) ở §5, **và** hỏi Dev theo §6 SPEC-09 trước khi chạy.

**[MINOR] GAP-07 — `memberJoined`/`memberLeft` chỉ test cho room, không có đối chứng group**
`NEW-22` xác nhận 2 event này rơi vào `status = 9` (chưa implement) với `source.type = room`, nhưng không có TC nào chạy cùng 2 event đó với `source.type = group`. Thiếu đối chứng parity nên chưa chứng minh được "chưa implement" là **nhất quán giữa 2 nguồn** chứ không phải regression do lần fix này — đúng kiểu đối chứng mà `NEW-19` đã làm cho `postback`.
→ *Fix*: TC-MSGUSER001-02 ở §5.

**[MAJOR] GAP-08 — 4/7 loại `message.type` không có TC nào; không TC nào verify `last_message` / `last_time`**
Rà ma trận `message.type` × source trên 49 TC: `text` đủ cả 3 nguồn; `image` chỉ room (`NEW-34`); `sticker` chỉ room (`NEW-60`); **`video`, `audio`, `file`, `location` trống hoàn toàn ở cả room, group lẫn 1-1**.
Quan trọng hơn số lượng: **không TC nào hiện verify `conversation.last_message` và `last_time_message`** — tức phần hiển thị trên màn 「1:1チャット」 mà người dùng thực sự nhìn thấy. `ui-spec.md:58` định nghĩa rõ quy tắc nhãn preview theo loại tin, và kho `TC-CHT-291` đã chốt bảng nhãn (【画像】/【動画】/【音声】/【スタンプ】/【位置】).
Vì `handleMessageGroup` bị sửa và room dùng chung code path với group, mọi loại tin đều đi qua vùng code đã đổi. `NEW-34` mới chỉ chứng minh nhánh media hoạt động với **ảnh**.
→ *Fix*: TC-DATA001-01 (room, nhóm xử lý ngay) · TC-DATA001-02 (room, nhóm media) · TC-REGSHARED001-04 (group, đủ 7 loại) · TC-REGSHARED001-05 (1-1, đủ 7 loại) ở §5. Nhãn của `file` cần chốt theo §6 SPEC-10.

**[MAJOR] ISS-15 — RULE-05 chưa thực hiện: chưa đối chiếu tài liệu LINE mới nhất**
Note của `NEW-39` tự ghi *"behavior 403 phía LINE vẫn nên đối chiếu tài liệu chính thức (RULE-05)"* — nghĩa là **chưa làm**. Cả giả định "bot thường bị 403 khi gọi `/room/{roomId}/members/ids`" lẫn "room không có Summary API" đều đang dựa vào suy luận, chưa có link tài liệu LINE.
→ *Fix*: đính link Messaging API doc (mục Group/Room member) vào `02-spec-reference.md`.

**[MAJOR] ISS-16 — T1 thiếu sticker**
Mục 4.3 của Dev ghi rõ *"nhắn text / sticker / ảnh trong room"*. Bộ TC có text (`NEW-30`) và ảnh (`NEW-34`), **thiếu sticker** — mà sticker đi nhánh xử lý ngay (không qua job media), khác cả 2 nhánh đã test.

### 4.3 Minor

**[MINOR] ISS-17** — `TC No.` của toàn bộ TC là `temp_id` dạng `NEW-nn`, không theo format repo `TC-<mã quan điểm bỏ gạch>-<nn>`. Chấp nhận được vì nguồn là Studio, nhưng khi sync sang sheet human cần đánh lại.

**[MINOR] ISS-18 RULE-02** — Không TC nào ghi **loại evidence bắt buộc** ở `note`. TC job nền cần nói rõ: log job / kết quả query DB / screenshot LINE app.

**[MINOR] ISS-19** — `spec_status` = `null` ở cả 27 TC (không TC nào ghi `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader`), dù nhiều TC đang dựa trên hành vi tự suy từ code.

### 4.4 Nit

**[NIT] ISS-20** — Mục 5.1 `03-dev-impact.md` chỉ có commit hash, **không có PR link** → reviewer không xem được diff để verify fix shape (AP-4).

**[NIT] ISS-21** — Mục 4.3 của Dev không ghi mức `High/Medium/Low` cho từng tính năng T1–T5; §3 đang tự suy "High" cho cả 5 dựa vào việc chúng đều là luồng chính.

**[NIT] ISS-22 (RULE-11)** — Các quan điểm ở §4 `checklist-lme.md` (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) không được dùng để flag ở report này; nếu sau này có ticket Closed liên quan room thì bổ sung.

---

## 4.5 TC trùng lặp nội dung

Đã rà **toàn bộ 27 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected` tương đương).

**Kết quả vòng này: không phát hiện trùng lặp còn tồn tại.**

Lý do: đợt rà trùng đã chạy **trước** review này (2026-08-26) trên bộ 45 TC gốc và **18 TC trùng đã được xóa trên Studio theo phê duyệt của Leader**, đưa bộ TC về 27. Ghi lại để giữ vết:

| Nhóm trùng | TC giữ lại | TC đã xóa | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Tên room ghép từ member | `NEW-29` (#14245) | `NEW-38` (#14254) | `DUP-EXACT` | FUNC-001 × Normal × join room + mock 3 member × bot verified → cùng expected `田中, 佐藤, 鈴木` | `[MINOR]` |
| Postback trong room | `NEW-19` (#14235) | `NEW-3` (#13545) | `DUP-CONFLICT` | STATE-MATRIX-001 × postback room × cùng payload → **expected mâu thuẫn**: "được xử lý" vs "vẫn bị bỏ qua" | `[MAJOR]` |
| 16 cặp lô draft cũ ⇄ lô viết lại | `NEW-30,34,35,36,37,29,31,32,39,40,33,41,42,43,44,45` | `NEW-1,2,4,5,6,8,9,10,11,12,13,14,15,16,17,18` (#13543–13567) | `DUP-REWRITE` | Cùng mã quan điểm × cùng loại case × cùng đối tượng+thao tác × cùng tiền đề; bản mới siết oracle (`status=2` thay vì "DONE") và **sửa `requirement_keys` gán sai** ở 6/16 cặp | `[MINOR]` |

**Cảnh báo về hệ quả của việc xóa** (gate BƯỚC 4b đã chạy lại §3 + §7 trên tập 27 TC còn lại):
- Không impact/quan điểm nào **mất cover** do xóa ✔ — mọi TC bị xóa đều có bản thay thế 1:1.
- **Ngoại lệ `DUP-CONFLICT`**: `NEW-3` từng được tính `pass`, nhưng oracle của nó (`status = DONE`) sai — `status` bị ghi đè ở cuối vòng lặp. Việc xóa `NEW-3` làm lộ ra rằng **`postback` trong room chưa từng được verify đúng cách**; `NEW-19` (oracle đúng) chưa chạy.
- Backup nguyên bản 18 TC đã xóa: `04-tc-list.deleted-dups.json` trong folder này.

---

## 5. TCs đề xuất bổ sung

> **Đã đối chiếu 27 TC ở BƯỚC 0 + `kho-tcs/fa001-chat11-11チャット.md` (nhóm "Group chat", 15 TC `TC-CHT-377` → `TC-CHT-391`) — không TC đề xuất nào trùng với bộ TC hiện có, cũng không trùng lẫn nhau trong §5.**

**Kết quả đối chiếu kho `FA-001`** (room dùng chung `conversation_kind = 1` với group → toàn bộ nhóm "Group chat" của kho là **vùng regression** của task này):

| TC kho | Đã có TC ở BƯỚC 0? | Xử lý |
|---|---|---|
| `TC-CHT-377` Bot được thêm vào nhóm mới — tự tạo hội thoại | ✔ `NEW-35` | Đủ |
| `TC-CHT-378` **Nhóm cũ (bot đã ở sẵn) gửi tin — hội thoại được tạo** | ✘ | → **TC-COMPATLEGACY001-01** (GAP-02) |
| `TC-CHT-379` Rời nhóm rồi thêm lại — trạng thái chặn đổi tương ứng | ✔ `NEW-36`, `NEW-37` | Đủ |
| `TC-CHT-385` **Gửi tin vào nhóm — thành viên nhận được** | ✘ | → **TC-MSG001-01/02/03** (GAP-01) |
| `TC-CHT-380/381/382/383` Panel phải, ẩn mục, bookmark/status/ghi chú, ẩn+xoá nhóm | ✘ | → **TC-REGSHARED001-01** (gộp, smoke) |
| `TC-CHT-384` Nhận tin từ nhóm — đủ loại tin | Một phần (`NEW-30` text, `NEW-34` ảnh) | → **TC-FUNC001-01** (sticker, ISS-16) |
| `TC-CHT-386/387/388/389/390/391` URL không rút gọn, link form/item/booking, mã form cũ, nút/video/ảnh có action, tính năng không áp dụng cho nhóm, profile người gửi | ✘ | **Ngoài scope commit `2cd86fc6`** — không đề xuất TC mới (tránh AP-5). Ghi nhận là vùng regression cần chạy **nếu** Leader mở rộng scope. |

⚠️ **Conflict expected phát hiện khi đối chiếu kho — KHÔNG tự chọn bên**: kho `FA-001` mục "Điểm mâu thuẫn với spec" có **`MT-01` (mức CAO, đang CHỜ QUYẾT ĐỊNH)**: *"Gửi tin từ LME có cập nhật last message của bạn bè hay không — spec nói CÓ, TC mới nhất (SpecImprove #35389, 4/2026) nói KHÔNG"*. TC đề xuất `TC-MSG001-01` (gửi tin vào room) **chạm đúng vùng mâu thuẫn này** → cột `Kết quả mong đợi` của nó **cố ý không khẳng định** hành vi `last_message`, và điểm này được đẩy lên §6.

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa001-chat11-11チャット.md` — nhóm "Group chat" (15 TC `TC-CHT-377` → `TC-CHT-391`) |
| Vùng regression phát hiện từ kho | `TC-CHT-378` (nhóm cũ bot đã ở sẵn gửi tin) · `TC-CHT-385` (gửi tin vào nhóm) · `TC-CHT-380/381/382/383` (panel phải, bookmark/status/ghi chú, ẩn nhóm) · `TC-CHT-384` (đủ loại tin) · **`TC-CHT-55/56/57/274` (thu hồi tin `unsend`)** — bằng chứng duy nhất cho thấy hệ thống CÓ xử lý `unsend`, nhưng cả 4 TC kho đều là chat 1-1 |
| Conflict expected vs kho | `TC-MSG001-01` vs kho `MT-01` (mức CAO, CHỜ QUYẾT ĐỊNH) — *"gửi tin từ LME có cập nhật `last_message` không"* → **KHÔNG tự chọn bên**, đã đưa §6 SPEC-06; cột `Kết quả mong đợi` cố ý không assert `last_message` |
| GAP dùng lại TC kho (không viết mới) | Không — kho chỉ cover **group**, room là đối tượng mới chưa từng test. `TC-CHT-386/387/388/389/390/391` nằm **ngoài scope** commit `2cd86fc6` → không đề xuất TC mới (tránh AP-5), chỉ ghi nhận là vùng regression nếu Leader mở rộng scope |
| Xác nhận chống trùng | Đã đối chiếu **27 TC ở BƯỚC 0** + kho `FA-001` — **không TC đề xuất nào trùng**. Rà lại sau khi push (990/990 cặp trên 45 TC): cặp chéo cũ↔mới score cao nhất **0.459 < ngưỡng 0.5** |

### Bảng TC đề xuất (14 cột — 12 cột kho + `Chạy` + `Phạm vi ENV`)

> `Chạy` → Studio `exec_mode` · `Phạm vi ENV` → Studio `env_scope` (`Tất cả` → `["all"]`, `product` → `["prd"]`, `staging` → `["staging"]`).
> Cột `Ghi chú` **không** được `/sync-review-tc` đẩy lên test tool — mọi thứ cần có mặt trên Studio đã nằm ở cột riêng.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-MSG001-01 | API | MSG-001 | Chat admin - gửi tin vào room | Normal | manual | staging | Gửi text từ màn chat admin vào room — thành viên room nhận được trên LINE app thật | - Bot A đã ở trong room R1 (hội thoại room đã hiện ở màn Chat)<br>- Room R1 có 2 thành viên thật: 1 máy iOS và 1 máy Android<br>- Đăng nhập admin, chọn bot A, màn `/basic/chat-v3` | 1. Mở màn Chat, chọn filter 「グループ」<br>2. Mở hội thoại room R1<br>3. Nhập nội dung và bấm gửi<br>4. Mở LINE app trên **cả iOS và Android** của 2 thành viên, xem trong room R1<br>5. Bật log/spy request tới LINE API, đối chiếu tham số `to` | Nội dung: `Xin chào room 40164` | - Tin xuất hiện trong room R1 trên **cả iOS và Android**, đúng nguyên văn, đúng bot gửi<br>- Request push có `to = <roomId của R1>` (bắt đầu `R`), KHÔNG phải `groupId`, KHÔNG phải `userId`<br>- Tin hiển thị lại đúng ở khung hội thoại màn admin sau khi gửi | | Lấp `GAP-01` `[BLOCKER]` · Đánh giá spec: Đã hỏi leader · Evidence: ảnh LINE app iOS + Android + log request có tham số `to` (RULE-06) · dẫn từ kho `TC-CHT-385` · ⚠️ KHÔNG assert `conversation.last_message` — vướng `MT-01`, chờ §6 SPEC-06 · manual vì RULE-06; phần assert `to = roomId` trong log **tách ra auto được** |
| TC-MSG001-02 | API | MSG-001 | Chat admin - gửi tin vào room | Abnormal | auto | Tất cả | Gửi tin vào room mà bot đã bị kick — báo lỗi rõ ràng, không báo gửi thành công giả | - Bot A từng ở room R2, đã bị kick (`conversation.is_blocked = 1`)<br>- Hội thoại R2 vẫn còn trong danh sách chat | 1. Mở hội thoại room R2 ở màn Chat<br>2. Nhập nội dung, bấm gửi<br>3. Quan sát thông báo trên màn hình<br>4. Kiểm tra DB bảng message và log lời gọi LINE API | Nội dung: `test sau khi bị kick` | - Hiển thị lỗi/nội dung chặn rõ ràng cho admin, **KHÔNG hiện "đã gửi thành công"**<br>- Không tạo bản ghi message trạng thái thành công trong DB<br>- Không ném exception 500, không trắng màn | | Lấp `GAP-01` `[BLOCKER]` · Đánh giá spec: Spec không ghi · Evidence: screenshot thông báo + log API response · INTG-LINE-001: "vẫn hiện đã gửi thành công dù chưa gửi được" là lỗi kinh điển · ⚠️ auto được nhưng **đang bị chặn**: cần project `web` có branch run |
| TC-MSG001-03 | API | MSG-001 | Chat admin - gửi tin vào room | Boundary | manual | product | Gửi 5 media cùng lúc vào room — chunk 5 theo giới hạn LINE API | - Bot A ở trong room R1, có thành viên thật để nhận<br>- Có sẵn 5 file ảnh hợp lệ | 1. Mở hội thoại room R1<br>2. Chọn 5 ảnh, xác nhận gửi<br>3. Quan sát room trên LINE app thật<br>4. Đếm số lời gọi Push API trong log | 5 ảnh JPG < 10MB mỗi file | - Đủ 5 ảnh xuất hiện trong room trên LINE app, đúng thứ tự<br>- Số lời gọi Push API đúng theo quy tắc chunk 5 của hệ thống, mỗi lời gọi `to = roomId`<br>- Không ảnh nào bị mất hoặc gửi trùng | | Lấp `GAP-01` · Đánh giá spec: Spec không ghi · Evidence: ảnh LINE app + log số lời gọi API · RULE-08: media → bắt buộc product |
| TC-COMPATLEGACY001-01 | Data | COMPAT-LEGACY-001 | Job callback - Xử lý tin nhắn room | Normal | auto | Tất cả | Room đời cũ (bot đã ở sẵn, chưa có record DB) gửi tin — hội thoại room được tạo | - Room R3 tạo trước LINE v10.17.0, bot A **đã ở sẵn** trong room từ trước<br>- DB **chưa có** `line_user` nào có `line_id` = roomId của R3, chưa có conversation tương ứng<br>- Không nạp event `join` — mô phỏng đúng room đời cũ | 1. Ghi lại số bản ghi `line_user` / `conversation` của bot A trước khi chạy<br>2. Cho 1 thành viên trong room R3 gửi 1 tin text tới room<br>3. Chạy job xử lý callback<br>4. Truy vấn DB: `line_user` theo `line_id` của R3, `conversation` tương ứng, bản ghi message<br>5. Mở màn Chat admin, filter 「グループ」 | Webhook `message` / `text`, `source.type = room`, room chưa có record | - Tạo mới `line_user` với `line_id` bắt đầu `R`, `type = 1`<br>- Tạo mới `conversation` `conversation_kind = 1`, `is_blocked = 0`<br>- Tin nhắn lưu đúng dưới conversation vừa tạo, `callback_event.status = 2`<br>- Hội thoại room R3 xuất hiện ở màn Chat filter 「グループ」 | | Lấp `GAP-02` `[BLOCKER]` — **kịch bản chính mà ticket nhắm tới** · Đánh giá spec: Đã hỏi leader · Evidence: query DB trước/sau + screenshot màn Chat · dẫn từ kho `TC-CHT-378` · ⚠️ Chốt §6 SPEC-04 (`handleMessageGroup` có gọi `checkAddGroup` khi record chưa tồn tại không) **trước khi** chạy |
| TC-COMPATLEGACY001-02 | Data | COMPAT-LEGACY-001 | Job callback - Xử lý tin nhắn room | Abnormal | auto | Tất cả | Room đời cũ chưa có record + API member trả 403 — vẫn tạo hội thoại, tên rỗng | - Như TC-COMPATLEGACY001-01, dùng room R4<br>- Bot A là bot **thường** (không verified/premium) → LINE trả 403 khi gọi danh sách member room | 1. Xác nhận DB chưa có record của room R4<br>2. Cho thành viên trong room R4 gửi 1 tin text<br>3. Chạy job xử lý callback<br>4. Truy vấn DB record room + kiểm log<br>5. Mở màn Chat admin xem dòng hội thoại | Bot thường, room chưa có record, API member 403 | - `line_user` + `conversation` của room **vẫn được tạo**<br>- Tên room là chuỗi rỗng (không phải null), có log lỗi kèm roomId<br>- `callback_event.status = 2`, không phải 3<br>- Màn Chat vẫn render dòng room tên rỗng, không trắng màn | | Lấp `GAP-02` · Đánh giá spec: Spec không ghi · Evidence: query DB + log + screenshot · Tổ hợp 2 nhánh chưa từng test chung: room chưa có record × bot thường 403 (`NEW-31` có event join, TC này không) |
| TC-INTGHOOK001-01 | API | INTG-HOOK-001 | Job callback - Join/Leave room | Normal | auto | Tất cả | Cùng một webhook room được gửi 2 lần — chỉ được xử lý 1 lần | - Bot A, room R5 chưa có record trong DB<br>- Chuẩn bị 1 payload webhook `join` room R5 **giống hệt nhau về mọi trường** (kể cả `webhookEventId` nếu có) | 1. Nạp payload lần 1 vào `callback_event`, chạy job<br>2. Ghi lại số bản ghi `line_user` / `conversation` của R5<br>3. Nạp **đúng payload đó** lần 2, chạy job<br>4. Đếm lại số bản ghi và **đếm số lần xử lý thực tế trong log** | 1 payload `join` room, nạp 2 lần | - Sau lần 2: `line_user` của R5 vẫn **đúng 1 bản ghi**, `conversation` vẫn **đúng 1 bản ghi**<br>- Log chứng minh lần thứ 2 **bị bỏ qua** (hoặc xử lý idempotent, không tạo thêm)<br>- Không phát sinh lời gọi LINE API thừa cho lần 2 | | Lấp `GAP-03` `[BLOCKER]` · Đánh giá spec: Spec không ghi · Evidence: payload gốc + **số lần xử lý đếm từ log/DB** — INTG-HOOK-001 ghi rõ KHÔNG chấp nhận "đã thử, thấy bình thường" |
| TC-INTGHOOK001-02 | API | INTG-HOOK-001 | Job callback - Join/Leave room | Abnormal | auto | Tất cả | Webhook room đến sai thứ tự — `leave` xử lý trước `join` | - Bot A, room R6 chưa có record trong DB<br>- Chuẩn bị 2 payload: `join` R6 (timestamp sớm) và `leave` R6 (timestamp muộn) | 1. Nạp và xử lý payload **`leave` trước**<br>2. Truy vấn DB xem có tạo bản ghi rác không, kiểm log<br>3. Nạp và xử lý payload **`join` sau**<br>4. Truy vấn lại trạng thái cuối của `line_user` / `conversation` R6 | `leave` đến trước `join` | - Bước 2: `leave` cho room chưa tồn tại **không tạo bản ghi rác**, không ném exception, có log rõ ràng<br>- Bước 4: trạng thái cuối phản ánh đúng thực tế (room đang có bot → `is_blocked = 0`), đúng 1 bản ghi mỗi bảng | | Lấp `GAP-03` `[BLOCKER]` · Đánh giá spec: Spec không ghi · Evidence: query DB sau mỗi bước + log · Rủi ro thật: LINE không đảm bảo thứ tự webhook |
| TC-INTGHOOK001-03 | API | INTG-HOOK-001 | Job callback - Join/Leave room | Boundary | auto | Tất cả | `join` → `leave` → `join` room liên tiếp trong dưới 1 giây | - Bot A, room R7 chưa có record<br>- 3 payload liên tiếp cho R7, timestamp cách nhau < 1s | 1. Nạp cả 3 payload vào `callback_event`<br>2. Chạy job xử lý callback<br>3. Truy vấn DB đếm bản ghi và trạng thái `is_blocked` cuối cùng<br>4. Kiểm log thứ tự xử lý | `join` → `leave` → `join`, < 1s | - Đúng 1 `line_user` và 1 `conversation` cho R7 (không nhân bản)<br>- `is_blocked` cuối = 0 (khớp event cuối cùng là `join`)<br>- Không deadlock, không bỏ sót event nào trong log | | Lấp `GAP-03` · Đánh giá spec: Spec không ghi · Evidence: query DB + log đủ 3 event · Liên kết CONC-001 |
| TC-ENV003-01 | API | ENV-003 | Job callback - Xử lý tin nhắn room | Normal | manual | product | Smoke luồng room trên PRODUCTION — job callback chạy tách riêng | - Đã deploy branch `m_202608_callback_room_40164` lên production<br>- Có room thật trên production với bot thật, 2 thành viên thật<br>- **Không tạo/xóa dữ liệu khách hàng thật** | 1. Mời bot vào room thật trên production<br>2. Thành viên gửi 1 tin text vào room<br>3. Kiểm tra hội thoại room xuất hiện ở màn Chat production<br>4. Gửi 1 tin từ màn Chat vào room, xem trên LINE app thật<br>5. Đối chiếu log **job callback riêng** (production tách 3 job độc lập) | Room thật trên production | - Hội thoại room được tạo, hiển thị đúng ở filter 「グループ」<br>- Tin 2 chiều đều tới đích trên LINE app thật<br>- Log cho thấy event room được **job callback riêng** xử lý (không phải job all như dev/staging), không rơi vào job broadcast/scenario | | Lấp `ISS-02` `[BLOCKER]` · Đánh giá spec: Đã hỏi leader · Evidence: log job callback production + ảnh LINE app · RULE-08 + Catalog D: production tách 3 job độc lập |
| TC-DATADB001-01 | Data | DATA-DB-001 | Job callback - Join/Leave room | Normal | auto | Tất cả | Hai bot khác nhau cùng ở một room — mỗi bot có bản ghi riêng, không lẫn | - Bot A và bot B thuộc **2 tài khoản khác nhau**<br>- Cùng mời cả 2 bot vào **cùng 1 room R8** (cùng roomId) | 1. Nạp event `join` room R8 cho bot A, chạy job<br>2. Nạp event `join` room R8 cho bot B, chạy job<br>3. Truy vấn `line_user` theo `line_id` của R8 — đếm số bản ghi và các `bot_id`<br>4. Truy vấn `conversation` tương ứng<br>5. Mở màn Chat của bot A rồi bot B | Cùng roomId, 2 `bot_id` khác nhau | - Có **đúng 2 bản ghi** `line_user` cùng `line_id` nhưng khác `bot_id` — không đè lên nhau<br>- Mỗi bot có `conversation` riêng<br>- Màn Chat của bot A chỉ thấy hội thoại của bot A, bot B chỉ thấy của bot B | | Lấp `GAP-05` `[BLOCKER]` · Đánh giá spec: Spec không ghi · Evidence: ảnh chụp kết quả query kèm câu query, trên **cả 2 tài khoản** · DATA-DB-001 BẮT BUỘC với UPDATE/DELETE |
| TC-DATADB001-02 | Data | DATA-DB-001 | Job callback - Join/Leave room | Abnormal | auto | Tất cả | Kick bot A khỏi room chung — hội thoại của bot B không bị ảnh hưởng | - Tiếp nối TC-DATADB001-01: bot A và bot B cùng ở room R8, cả 2 `is_blocked = 0` | 1. Ghi lại `is_blocked` và `updated_at` của conversation cả 2 bot<br>2. Nạp event `leave` room R8 **chỉ cho bot A**, chạy job<br>3. Truy vấn lại `conversation` của **cả 2 bot**<br>4. Mở màn Chat của bot B | `leave` chỉ cho bot A | - Conversation của **bot A**: `is_blocked = 1`, bản ghi **không bị xóa**<br>- Conversation của **bot B**: `is_blocked` vẫn = 0, `updated_at` **không đổi**<br>- Màn Chat bot B vẫn dùng hội thoại room bình thường | | Lấp `GAP-05` `[BLOCKER]` · Đánh giá spec: Spec không ghi · Evidence: query trước/sau trên 2 tài khoản · Verify `WHERE` có đủ `bot_id` khi UPDATE |
| TC-FUNC004-01 | UI | FUNC-004 | Job callback - Tổng hợp tên room | Boundary | auto | Tất cả | Tên room ghép từ 5 member tên dài nhất — không vượt giới hạn cột, không cắt giữa ký tự | - Bot verified/premium<br>- Room R9 có 5 thành viên, mỗi thành viên đặt tên LINE **dài nhất mà LINE cho phép**, dùng ký tự tiếng Nhật (multi-byte) | 1. Nạp event `join` room R9, chạy job<br>2. Truy vấn `line_user.name` và tên conversation của R9<br>3. Đếm độ dài chuỗi kết quả, đối chiếu giới hạn cột `line_user.name`<br>4. Mở màn Chat xem tên hiển thị | 5 member tên dài tối đa, ký tự tiếng Nhật | - Tên room lưu được, **không bị lỗi tràn cột / không bị DB từ chối**<br>- Nếu bị cắt: cắt ở ranh giới ký tự, **không tạo ký tự lỗi (mojibake)**<br>- Màn Chat hiển thị tên không vỡ layout, không tràn ngang | | Lấp `ISS-13` `[MAJOR]` · Đánh giá spec: Spec không ghi · Evidence: query DB + screenshot màn Chat · `db-mapping.md`: `line_user.name varchar(128)`; 5 tên dài + 4 dấu `', '` có thể chạm biên |
| TC-DATATEXT001-01 | Data | DATA-TEXT-001 | Job callback - Tổng hợp tên room | Normal | auto | Tất cả | Tên member chứa emoji và ký tự đặc biệt — tên room hiển thị đúng ở mọi tầng | - Bot verified/premium<br>- Room R10 có 3 thành viên: 1 tên chứa emoji, 1 tên chứa ký tự đặc biệt (`&`, `<`, `"`), 1 tên tiếng Nhật thường | 1. Nạp event `join` room R10, chạy job<br>2. Truy vấn `line_user.name` trong DB<br>3. Mở màn Chat admin xem tên hội thoại<br>4. Xem tên hội thoại đó trên mobile app (nếu có) | 3 member: emoji / ký tự đặc biệt / tiếng Nhật | - DB lưu đúng nguyên văn cả emoji lẫn ký tự đặc biệt, không mojibake<br>- Màn Chat hiển thị đúng, **không bị escape sai / không vỡ HTML**<br>- Tên nối đúng bằng `', '` | | Lấp `ISS-13` `[MAJOR]` · Đánh giá spec: Spec không ghi · Evidence: query DB + screenshot màn Chat · Tên room lấy từ tên LINE user → không kiểm soát được nội dung |
| TC-JOB001-01 | API | JOB-001 | Job callback - Tổng hợp tên room | Boundary | manual | product | Nhiều room join đồng loạt, mỗi room nhiều member — job không mất bản ghi khi chạm rate limit | - Chuẩn bị **20 room**, mỗi room ≥ 5 thành viên (tổng ≥ 120 lời gọi LINE API)<br>- Nạp 20 event `join` vào `callback_event` cùng lúc | 1. Ghi lại tổng số event đưa vào<br>2. Chạy job xử lý callback<br>3. Đếm số room được tạo record thành công, số room lỗi<br>4. Đọc log: có retry không, có backoff không, có event nào biến mất không<br>5. Đối chiếu: số event vào = số xử lý thành công + số vào hàng đợi lỗi | 20 room × ≥ 5 member | - **Không event nào biến mất**: số vào = số thành công + số lỗi có log<br>- Job **không dừng giữa chừng**, các event sau vẫn được xử lý dù event trước lỗi<br>- Log ghi rõ từng lần chạm rate limit kèm roomId<br>- Ghi nhận thực tế hệ thống có retry/backoff hay không để báo Leader | | Lấp `ISS-12` `[MAJOR]` · Đánh giá spec: Đã hỏi leader · Evidence: log job + bảng đối chiếu số bản ghi vào/ra · RULE-08: job nền → product · Tách được: bản mock rate limit ở local **auto được** (như `NEW-32`); bản này manual vì cần rate limit THẬT |
| TC-FUNC001-01 | UI | FUNC-001 | Job callback - Xử lý tin nhắn room | Normal | auto | Tất cả | Sticker gửi trong room — xử lý ngay, không đi nhánh job media | - Bot A ở trong room R1, hội thoại đã tồn tại<br>- Thành viên room có LINE app thật | 1. Thành viên gửi 1 **sticker** vào room R1<br>2. Chạy job xử lý callback<br>3. Truy vấn `callback_event.status` và bản ghi message<br>4. Mở màn Chat admin xem hiển thị sticker | Webhook `message`, `message.type = sticker`, `source.type = room` | - `callback_event.status = 2`, KHÔNG rơi vào 10<br>- Sticker lưu đúng dưới conversation của room, xử lý **ngay** (không chờ lượt job media như ảnh)<br>- Màn Chat admin hiển thị sticker đúng, không lỗi | | Lấp `ISS-16` `[MAJOR]` · Đánh giá spec: Spec không ghi · Evidence: query DB + screenshot màn Chat · dẫn từ kho `TC-CHT-384` · Mục 4.3 Dev ghi "text / sticker / ảnh" nhưng bộ TC thiếu sticker |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Chat admin - danh sách hội thoại | Normal | auto | Tất cả | Smoke các thao tác hội thoại nhóm áp dụng cho room — bookmark, trạng thái, ghi chú, ẩn | - Bot A có ≥ 1 room và ≥ 1 group LINE trong danh sách chat<br>- Đăng nhập admin, màn `/basic/chat-v3` | 1. Với hội thoại room: bật bookmark, đổi 対応ステータス, thêm ghi chú<br>2. Kiểm tra panel thông tin bên phải của room<br>3. Ẩn hội thoại room, mở màn danh sách đã ẩn<br>4. Lặp lại toàn bộ với hội thoại **group** để đối chiếu | 1 room + 1 group | - Room hỗ trợ bookmark / trạng thái / ghi chú **giống group**, lưu đúng và giữ sau reload<br>- Panel phải của room ẩn đúng các mục không áp dụng, **không lỗi khi tên room rỗng**<br>- Ẩn/hiện room hoạt động như group<br>- Không thao tác nào ở room làm ảnh hưởng hội thoại group | | Lấp `ISS-08` `[MAJOR]` · Đánh giá spec: Spec không ghi · Evidence: screenshot từng thao tác cho **cả room và group** · regression · Gộp vùng kho `TC-CHT-380/381/382/383` · ⚠️ auto được nhưng **đang bị chặn**: cần project `web` có branch run |
| TC-DATAREF001-01 | Data | DATA-REF-001 | Chat admin - danh sách hội thoại | Normal | auto | Tất cả | Danh sách thành viên room ở màn Chat — đối chiếu bảng `group_members` | - Bot A ở trong room R1 có 3 thành viên đã gửi tin<br>- Bot A cũng ở trong 1 group LINE có 3 thành viên (để đối chứng) | 1. Mở màn Chat, mở hội thoại room R1, xem phần thành viên ở panel thông tin<br>2. Truy vấn bảng `group_members` theo conversation của room R1<br>3. Lặp lại với hội thoại group để đối chiếu<br>4. Truy vấn `line_user` các member (`type = 2`) của room | Room 3 member + group 3 member | - Xác định rõ: màn Chat có hiển thị thành viên room hay không, và **lấy từ đâu**<br>- Nếu group có bản ghi `group_members` mà room **không có** → ghi nhận là chênh lệch, báo lại Dev (không tự kết luận là bug)<br>- Không màn nào lỗi/trắng do thiếu dữ liệu thành viên room | | Lấp `ISS-14` `[MAJOR]` · Đánh giá spec: Spec không ghi · Evidence: query `group_members` cho cả room và group + screenshot panel · Xem §6 SPEC-05 · ⚠️ auto được nhưng **đang bị chặn**: cần project `web` có branch run |
| TC-INTGLINE001-01 | API | INTG-LINE-001 | Job callback - Tổng hợp tên room | Abnormal | auto | Tất cả | LINE API trả mã lỗi CHƯA HANDLE riêng — fallback generic hoạt động | - Bot verified<br>- Mock LINE API `/room/{roomId}/members/ids` trả **HTTP 500 với body không phải JSON** (mã lỗi chưa được handle riêng trong code)<br>- Room R11 chưa có record | 1. Cấu hình mock trả 500 + body rác cho room R11<br>2. Nạp event `join` room R11, chạy job<br>3. Truy vấn DB record room + tên room<br>4. Kiểm log<br>5. Lặp lại với biến thể: HTTP 503, body rỗng | HTTP 500 body không phải JSON; HTTP 503; body rỗng | - Với **mọi biến thể**: `line_user` / `conversation` vẫn được tạo, tên room rỗng<br>- Có log lỗi kèm roomId, **không ném exception ra ngoài job**<br>- `callback_event.status = 2`, các event khác trong cùng lượt vẫn chạy<br>- Không có mã lỗi nào làm job dừng | | Lấp `ISS-11` `[MAJOR]` / AP-1 · Đánh giá spec: Spec không ghi · Evidence: log cho **từng biến thể** + query DB · Verify fallback thật sự generic chứ không phải chuỗi `if` các mã đã biết |
| TC-MSGUSER001-01 | API | MSG-USER-001 | Job callback - Xử lý tin nhắn room | Normal | auto | Tất cả | Thu hồi tin (`unsend`) trong room — tin đổi thành thông báo thu hồi | - Bot A đã ở trong room R12, hội thoại có ≥ 3 tin nhắn do thành viên gửi<br>- Ghi lại `messageId` của tin thứ 2 | 1. Ghi lại nội dung + thời gian của cả 3 tin trong hội thoại room R12<br>2. Nạp `callback_event` payload: `{"type":"unsend","unsend":{"messageId":"<id tin thứ 2>"},"source":{"type":"room","roomId":"R12","userId":"Uxxxxxxxx"}}`<br>3. Chạy job xử lý callback<br>4. Truy vấn DB bản ghi message theo `messageId` + `conversation.last_message` của room<br>5. Mở màn Chat admin, xem hội thoại room R12 | Webhook `unsend`, `source.type = room`, `messageId` của tin thứ 2 | - Tin bị thu hồi đổi nội dung thành thông báo thu hồi 「友だちがメッセージを送信取り消しました」, **thời gian của tin KHÔNG đổi**<br>- 2 tin còn lại không bị ảnh hưởng<br>- `callback_event.status = 2` (DONE)<br>- ⚠️ Nếu hệ thống **chưa xử lý** `unsend` cho room (status = 9 unknown event type, hoặc tin không đổi) → **ghi nhận là ranh giới scope, báo Leader, KHÔNG tự kết luận là bug** | | Lấp `GAP-06` `[MAJOR]` · Đánh giá spec: Spec không ghi — spec `chat-11` không mô tả `unsend` ở tầng job/DB; hành vi lấy từ kho `TC-CHT-274` (chat 1-1) · Evidence: query DB trước/sau + screenshot màn Chat · **`unsend` là callback có `source.type = room`** → nằm đúng phạm vi mục tiêu ticket, nhưng Redmine description và mục 4.1 của Dev đều KHÔNG liệt kê · Xem §6 SPEC-09 |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | Job callback - Regression group/1-1 | Normal | auto | Tất cả | Regression: thu hồi tin (`unsend`) trong group vẫn hoạt động như trước | - Bot A ở trong group Cgrp03, hội thoại có ≥ 3 tin do thành viên group gửi<br>- Branch fix đã checkout | 1. Ghi lại nội dung + thời gian 3 tin trong hội thoại group Cgrp03<br>2. Nạp `callback_event` payload `unsend` với `source.type = group`, `groupId = Cgrp03`, `messageId` của tin thứ 2<br>3. Chạy job xử lý callback<br>4. Truy vấn DB bản ghi message + `conversation.last_message` của group<br>5. Đối chiếu kết quả với TC-MSGUSER001-01 (cùng event, khác `source.type`) | Webhook `unsend`, `source.type = group` | - Tin bị thu hồi trong group đổi thành thông báo thu hồi, thời gian không đổi<br>- Hành vi **không đổi so với trước fix** (nhánh group không bị ảnh hưởng bởi việc thêm nhánh room)<br>- `callback_event.status = 2` | | Lấp `GAP-06` `[MAJOR]` · regression · Đánh giá spec: Spec không ghi · Evidence: query DB trước/sau · Đối chứng parity với TC-MSGUSER001-01 — nếu group xử lý được mà room không thì đó là bằng chứng `unsend` bị bỏ sót đúng như bug gốc |
| TC-REGSHARED001-03 | UI | REG-SHARED-001 | Job callback - Regression group/1-1 | Normal | auto | Tất cả | Regression: thu hồi tin (`unsend`) trong chat 1-1 vẫn hoạt động như trước | - Bot A có friend Uuser02 (bạn cũ), hội thoại 1-1 có ≥ 3 tin do friend gửi<br>- Branch fix đã checkout | 1. Ghi lại nội dung + thời gian 3 tin trong hội thoại 1-1 của Uuser02<br>2. Nạp `callback_event` payload `unsend` với `source.type = user`, `userId = Uuser02`<br>3. Chạy job xử lý callback<br>4. Truy vấn DB bản ghi message + `conversation.last_message`<br>5. Mở màn Chat admin xem hội thoại và dòng danh sách bạn bè | Webhook `unsend`, `source.type = user` | - Tin bị thu hồi đổi thành 「友だちがメッセージを送信取り消しました」, thời gian không đổi<br>- Dòng danh sách bạn bè hiển thị đúng theo hành vi cũ<br>- KHÔNG bị route vào luồng nhóm<br>- `callback_event.status = 2` | | Lấp `GAP-06` · regression · Đánh giá spec: Spec không ghi · Evidence: query DB + screenshot màn Chat · dẫn từ kho `TC-CHT-274`, `TC-CHT-55/56/57` · Verify điểm rẽ theo `source.type` của `unsend` không bị lệch sau khi mở rộng điều kiện route |
| TC-MSGUSER001-02 | API | MSG-USER-001 | Job callback - Regression group/1-1 | Abnormal | auto | Tất cả | Ranh giới scope: `memberJoined`/`memberLeft` trong group cũng chưa được xử lý (parity với room) | - Bot A ở trong group Cgrp03<br>- Branch fix đã checkout<br>- Đã có kết quả của `NEW-22` (cùng 2 event nhưng `source.type = room`) để đối chiếu | 1. Nạp `callback_event` payload `{"type":"memberJoined","source":{"type":"group","groupId":"Cgrp03"}}`<br>2. Chạy job xử lý callback<br>3. Truy vấn `callback_event.status` và đếm số `line_user`<br>4. Lặp lại với `type = memberLeft`<br>5. Đối chiếu với kết quả `NEW-22` (source.type = room) | Webhook `memberJoined` / `memberLeft`, `source.type = group` | - Cả 2 event: `callback_event.status = 9` (loại sự kiện chưa hỗ trợ), log 「unknown event type」<br>- Không có bản ghi member nào được thêm/xóa<br>- Hành vi **GIỐNG HỆT** room (`NEW-22`) → xác nhận việc chưa implement là nhất quán giữa 2 nguồn, **không phải regression do lần fix này** | | Lấp `GAP-07` `[MINOR]` · Đánh giá spec: Spec không ghi · Evidence: query DB + log cho cả 2 event · Parity check với `NEW-22`; giá trị chính là chứng minh chưa-implement là có chủ đích, phục vụ §6 SPEC-02 |
| TC-DATA001-01 | Data | DATA-001 | Job callback - Xử lý tin nhắn room | Normal | auto | Tất cả | Room nhận text / sticker / location — xử lý ngay, màn 1:1チャット hiện đúng nhãn và last_time | - Bot A đã ở trong room R13, hội thoại đã tồn tại<br>- Đăng nhập admin, chọn bot A, mở màn 「1:1チャット」 (`/basic/chat-v3`) | 1. Ghi lại `last_message` + `last_time_message` hiện tại của hội thoại room R13<br>2. Cho thành viên gửi vào room R13 **lần lượt**: (a) text, (b) sticker, (c) location<br>3. Sau **mỗi** tin: chạy job xử lý callback<br>4. Sau **mỗi** tin: truy vấn `callback_event.status`, `conversation.last_message`, `conversation.last_time_message`<br>5. Sau **mỗi** tin: mở màn 「1:1チャット」, đọc dòng room R13 ở danh sách + khung hội thoại | text `xin chào room 40164` · 1 sticker · 1 location | - Cả 3 loại: `callback_event.status = 2` (DONE) **ngay lượt job đầu** — KHÔNG rơi vào nhánh job media<br>- `last_message` ở danh sách: text → nội dung tin (cắt gọn nếu dài) · sticker → 「【スタンプ】」 · location → 「【位置】」<br>- `last_time_message` = thời điểm tin vừa nhận, cập nhật sau **mỗi** tin<br>- Khung hội thoại render đúng từng loại, không lỗi | | Lấp `GAP-08` `[MAJOR]` · Đánh giá spec: Spec ghi rõ (`ui-spec.md:58,86` — quy tắc nhãn last message preview) · Evidence: query DB `conversation` trước/sau mỗi tin + screenshot màn 1:1チャット · Nhãn đối chiếu kho `TC-CHT-291` · Tách khỏi nhóm media vì đây là code path xử lý ngay (note `NEW-34`) |
| TC-DATA001-02 | Data | DATA-001 | Job callback - Xử lý tin nhắn room | Normal | auto | Tất cả | Room nhận image / video / audio / file — qua job media 2 lượt, màn 1:1チャット hiện đúng nhãn | - Bot A đã ở trong room R13, hội thoại đã tồn tại<br>- LINE content API mock trả file hợp lệ cho cả 4 loại<br>- Đăng nhập admin, mở màn 「1:1チャット」 | 1. Ghi lại `last_message` + `last_time_message` hiện tại của room R13<br>2. Cho thành viên gửi vào room R13 **lần lượt**: image, video, audio, file (PDF)<br>3. Sau **mỗi** tin: chạy job callback **lượt 1**, kiểm `callback_event.status`<br>4. Chạy tiếp job media **lượt 2**, kiểm lại `callback_event.status`<br>5. Truy vấn `conversation.last_message` + `last_time_message`<br>6. Mở màn 「1:1チャット」, đọc dòng room R13 và mở hội thoại xem từng media | 1 ảnh JPG · 1 video MP4 · 1 audio M4A · 1 file PDF | - Mỗi loại: lượt 1 `status = 30` (MEDIA_NEW), lượt 2 `status = 2` (DONE) — khớp hành vi đã xác nhận ở `NEW-34`<br>- `last_message`: image → 「【画像】」 · video → 「【動画】」 · audio → 「【音声】」 · file → **ghi nhận giá trị THẬT** (`ui-spec.md:58` ghi 「【PDF】」, không phải 「【ファイル】」 — xem §6 SPEC-10)<br>- `last_time_message` cập nhật đúng sau mỗi tin<br>- Mở hội thoại: ảnh có thumbnail, video/audio phát được, PDF tải được | | Lấp `GAP-08` `[MAJOR]` · Đánh giá spec: Spec ghi rõ một phần — nhãn `file` chưa chốt · Evidence: query DB + screenshot màn 1:1チャット + mở thử từng media · RULE-08: media nên smoke thêm ở product (đã có `TC-MSG001-03`) |
| TC-REGSHARED001-04 | UI | REG-SHARED-001 | Job callback - Regression group/1-1 | Normal | auto | Tất cả | Regression: group nhận đủ 7 loại message — nhãn và last_time không đổi sau fix | - Bot A ở trong group Cgrp04, hội thoại đã tồn tại<br>- Branch fix đã checkout<br>- Đăng nhập admin, mở màn 「1:1チャット」 | 1. Ghi lại `last_message` + `last_time_message` của group Cgrp04<br>2. Cho thành viên group gửi **lần lượt đủ 7 loại**: text · image · video · audio · file · location · sticker<br>3. Sau mỗi tin: chạy job (media chạy đủ 2 lượt)<br>4. Truy vấn `callback_event.status` + `conversation.last_message` + `last_time_message`<br>5. Đối chiếu từng loại với kết quả của TC-DATA001-01 / TC-DATA001-02 (cùng loại tin, khác `source.type`) | 7 tin, mỗi loại 1 tin, `source.type = group` | - Cả 7 loại xử lý đúng: text/sticker/location `status = 2` ngay; image/video/audio/file qua 2 lượt rồi `status = 2`<br>- Nhãn `last_message` **giống hệt** kết quả của room ở TC-DATA001-01/02 (parity)<br>- Group vẫn gọi Group Summary + endpoint `/group/`, KHÔNG gọi `/room/`<br>- Hành vi **không đổi so với trước fix** | | Lấp `GAP-08` `[MAJOR]` · regression · Đánh giá spec: Spec ghi rõ · Evidence: query DB + screenshot cho từng loại · Parity với TC-DATA001-01/02 — lệch giữa group và room là dấu hiệu nhánh room xử lý thiếu loại tin |
| TC-REGSHARED001-05 | UI | REG-SHARED-001 | Job callback - Regression group/1-1 | Normal | auto | Tất cả | Regression: chat 1-1 nhận đủ 7 loại message — nhãn và last_time không đổi sau fix | - Bot A có friend Uuser03 (bạn cũ), hội thoại 1-1 đã tồn tại<br>- Branch fix đã checkout<br>- Đăng nhập admin, mở màn 「1:1チャット」 | 1. Ghi lại `last_message` + `last_time_message` của hội thoại Uuser03<br>2. Cho friend gửi **lần lượt đủ 7 loại**: text · image · video · audio · file · location · sticker<br>3. Sau mỗi tin: chạy job (media chạy đủ 2 lượt)<br>4. Truy vấn `callback_event.status` + `conversation.last_message` + `last_time_message`<br>5. Mở màn 「1:1チャット」, đọc dòng của Uuser03 ở danh sách sau mỗi tin | 7 tin, mỗi loại 1 tin, `source.type = user` | - Cả 7 loại xử lý đúng, `status` kết thúc = 2<br>- Nhãn `last_message` đúng theo loại: nội dung / 【画像】/【動画】/【音声】/ nhãn file /【位置】/【スタンプ】<br>- `last_time_message` cập nhật sau mỗi tin<br>- KHÔNG bị route vào luồng nhóm — hành vi 1-1 không đổi sau khi mở rộng điều kiện route | | Lấp `GAP-08` · regression · Đánh giá spec: Spec ghi rõ (`ui-spec.md:86` cho ảnh nhận từ bạn bè) · Evidence: query DB + screenshot danh sách sau mỗi tin · dẫn từ kho `TC-CHT-291` |

**Tổng: 26 TC đề xuất** — 8 lấp `[BLOCKER]`, 17 lấp `[MAJOR]`, 1 lấp `[MINOR]`.

Phân bố: **Loại case** Normal 16 · Abnormal 6 · Boundary 4 — **Nhóm** API 11 · Data 8 · UI 7 — **Chạy** auto 22 · manual 4 — **Phạm vi ENV** Tất cả 22 · product 3 · staging 1.

**Cơ sở đánh giá cột `Chạy`** (không phải mặc định — suy từ những gì runner Studio **đã thực sự làm được** ở run #619):

| Runner đã chứng minh làm được | Bằng chứng từ run #619 |
|---|---|
| Nạp `callback_event` payload tùy ý, chạy job, đếm bản ghi trước/sau | `NEW-20`: *"line_user 375769->375769, conversation 226614->226614"* |
| Mock LINE API theo mã lỗi | 403 (`NEW-31`) · 429 + lỗi mạng (`NEW-32`) · token invalid + refresh (`NEW-24`) · list rỗng (`NEW-25`) |
| Đếm số lời gọi API + ghi lại URL đã gọi | `NEW-39`: *"URL đã gọi=[/v2/bot/room/Rapi01/members/ids, …]"* · `NEW-24`: *"số lần gọi members/ids=2"* |
| Mock nhiều member với tên cụ thể | `NEW-27`: 8 member → *"Member1, …, Member5"* |
| Chạy job nhiều lượt | `NEW-34`: *"pass1 status=30 → pass2 status=2"* |
| Tạo đối tượng đối chứng để so parity | `NEW-19` (room vs group) · `NEW-23` (tạo group `Ctypecmp01`) |
| **Không** làm được: bất cứ gì cần project `web` | `NEW-44`/`NEW-45`: `[SOURCE_BLOCKED] SOURCE_BRANCH_MISSING` |

→ **11 TC auto chạy được ngay**; **3 TC** (`TC-MSG001-02`, `TC-REGSHARED001-01`, `TC-DATAREF001-01`) đánh `auto` nhưng **bị chặn** đến khi project `web` có branch run; **4 TC** buộc `manual` vì RULE-06 (LINE app thật) hoặc RULE-08 (production). Trong 4 TC manual, `TC-MSG001-01` và `TC-JOB001-01` còn **tách được** phần auto — đã ghi ở `Ghi chú`, chờ Leader quyết có tách thành TC riêng không.

**RULE-01 — quan điểm Cao thiếu loại case, đã ghi lý do:**
- `COMPAT-LEGACY-001` (Cao): có Normal + Abnormal, **thiếu Boundary** — biên "cũ/mới" đã được `NEW-28` (join lại room đã có tên + API lỗi) phủ ở bộ TC hiện có, không đẻ thêm.
- `ENV-003`, `DATA-TEXT-001`, `REG-SHARED-001`, `DATA-REF-001`, `FUNC-001`: chỉ đề xuất Normal vì đây là **TC lấp GAP bổ sung**; các chiều Abnormal/Boundary của cùng quan điểm đã có trong bộ 27 TC hiện tại (`NEW-31`, `NEW-32`, `NEW-45`, `NEW-41`, `NEW-42`).
- `FUNC-004`, `JOB-001`: chỉ đề xuất Boundary vì Normal/Abnormal đã có (`NEW-27`, `NEW-25`, `NEW-32`).
- `INTG-LINE-001`: chỉ đề xuất Abnormal — Normal đã có (`NEW-39`); quan điểm "lỗi từ LINE API" không có khái niệm biên rõ ràng.


---

## 6. Spec update needed

| # | Vấn đề | Nguồn mâu thuẫn | Cần ai chốt |
|---|---|---|---|
| **SPEC-01** | **`postback` trong room: xử lý hay bỏ qua?** Redmine description mục 2 yêu cầu *"message, postback trong room → route giống group"*. Nhưng commit `2cd86fc6` **không chạm** `doHandlePostbackEvent` — hàm này vẫn bỏ qua mọi source ≠ user. `03-dev-impact.md` mục 4.1/4.3 **không nhắc** nhánh postback. | Redmine description ⇄ commit thực tế ⇄ `NEW-19` (REQ-013) | **Dev + Leader** — đóng scope (sửa description) hay mở ticket bổ sung |
| **SPEC-02** | **`memberJoined` / `memberLeft` chưa implement.** Redmine mục 2 yêu cầu *"cập nhật thành viên room (nếu có tracking)"*; thực tế 2 event này rơi vào `status = 9` (unknown event type). Mục 4.1/4.3 của Dev không nhắc. | Redmine description ⇄ `NEW-22` (REQ-013) | **Dev + Leader** |
| **SPEC-03** | **UI/Admin quản lý hội thoại.** Redmine mục 5 yêu cầu *"hiển thị đúng loại room (icon/label riêng, phân biệt với group)"*. `NEW-44` lại expect room **nằm chung** filter 「グループ」, không có icon/label riêng. Mục 4.3 của Dev không liệt kê màn Chat admin. | Redmine mục 5 ⇄ `NEW-44` ⇄ `03-dev-impact.md` 4.3 | **Leader** — chốt room có cần phân biệt hiển thị với group không |
| **SPEC-04** | **`handleMessageGroup` có tạo record khi room chưa tồn tại không?** Quyết định trực tiếp việc room đời cũ (bot đã ở sẵn, không còn event `join`) có hoạt động hay không — tức là ticket có giải quyết được vấn đề gốc hay không. Mục 2 của Dev chỉ nói `checkAddGroup` được gọi từ `doHandleJoinGroup` và `checkAddGroupFriend`. | `03-dev-impact.md` mục 2/3 ⇄ GAP-02 | **Dev** — trả lời trước khi chạy TC-COMPATLEGACY001-01 |
| **SPEC-05** | **Bảng `group_members` có được ghi cho room không?** `spec-features/admin/chat-11/db/db-mapping.md` mục 18 định nghĩa `group_members` dùng cho `conversation_kind = 1` và màn chat **Đọc** bảng này; room dùng chung `conversation_kind = 1`. Mục 4.2 của Dev khẳng định "không có data bị update" và không nhắc bảng này. | `spec-features` db-mapping ⇄ `03-dev-impact.md` 4.2 | **Dev** |
| **SPEC-06** | **`MT-01` của kho `FA-001` (mức CAO, đang CHỜ QUYẾT ĐỊNH)**: *"Gửi tin từ LME có cập nhật `last_message` của bạn bè hay không — spec nói CÓ, TC mới nhất (SpecImprove #35389, 4/2026) nói KHÔNG"*. TC-MSG001-01 (gửi tin vào room) chạm đúng vùng này nên **cố ý không assert** `last_message`. | `kho-tcs/fa001` MT-01 ⇄ `spec-features/admin/chat-11/feature-spec.md:57` | **Leader** — chốt trước khi chạy TC-MSG001-01 |
| **SPEC-07** | **Thiếu retry/backoff cho 429 khi gọi API member room** — `NEW-32` ghi nhận: *"hệ thống KHÔNG thử lại và không có backoff cho 429 (chỉ lỗi token mới được thử lại)"*. JOB-001 yêu cầu job có **retry + backoff**. | `NEW-32` note ⇄ JOB-001 | **Leader** — chấp nhận hành vi hiện tại hay yêu cầu Dev bổ sung |
| **SPEC-08** | **RULE-05 chưa thực hiện** — chưa đối chiếu tài liệu LINE Messaging API mới nhất cho: (a) bot thường có thực sự bị 403 ở `/v2/bot/room/{roomId}/members/ids` không; (b) room có Summary API không. Cả bộ TC đang dựa trên suy luận. | `NEW-39` note ⇄ RULE-05 | **Member** — đính link tài liệu vào `02-spec-reference.md` |
| **SPEC-09** | **Event `unsend` có được xử lý cho `source.type = room` / `group` không?** Kho `FA-001` (`TC-CHT-55/56/57/274`) chứng minh hệ thống **có** xử lý `unsend` cho chat 1-1 (tin đổi thành 「友だちがメッセージを送信取り消しました」). Nhưng: (a) `spec-features/admin/chat-11` **không mô tả** `unsend` ở tầng job/DB; (b) Redmine description liệt kê `join`/`leave`/`memberJoined`/`memberLeft`/`message`/`postback` — **không có `unsend`**; (c) mục 4.1 của Dev không có function nào cho `unsend`. Nếu handler `unsend` lấy id hội thoại bằng `getGroupId()` (như `leave` trước khi fix) thì **room vẫn bị bỏ sót** — đúng lớp bug mà ticket này định giải quyết. | kho `FA-001` `TC-CHT-274` ⇄ Redmine description ⇄ `03-dev-impact.md` 4.1 | **Dev** — trả lời trước khi chạy TC-MSGUSER001-01 |
| **SPEC-10** | **Nhãn `last_message` của `message.type = file` là 「【ファイル】」 hay 「【PDF】」?** `spec-features/admin/chat-11/ui/ui-spec.md:58` ghi quy tắc preview là 「【画像】」「**【PDF】**」「【button 1】」; `EP-11` giới hạn loại file LME hỗ trợ là **PDF**. Kho `TC-CHT-291` liệt kê nhãn cho button/ảnh/video/audio/sticker/vị trí nhưng **không có** mục `file`. Nhãn sai làm TC fail oan hoặc bỏ lọt lỗi hiển thị. | `ui-spec.md:58` ⇄ kho `TC-CHT-291` (thiếu mục file) | **Leader/Dev** — chốt trước khi chạy TC-DATA001-02 |

---

## 7. Checklist đã chạy

| Mục | Kết quả | Ghi chú |
|---|---|---|
| **A.1** Bug root cause | ⚠️ Một phần | Có `NEW-40` (tầng model) + `NEW-30` (end-to-end), nhưng **thiếu đường vào chính**: room đời cũ chưa có record (GAP-02) |
| **A.2** Function impact (4.1) | ⚠️ RISK | 18/18 function đều có ≥ 1 TC ✔ nhưng **0/18 đã chạy pass** |
| **A.3** Data impact (4.2) | ❌ Fail | Thiếu kiểm `WHERE` scope 2 tài khoản (GAP-05); `group_members` chưa được xét (SPEC-05) |
| **A.4** Feature impact (4.3) | ❌ Fail | T5 thiếu push `to = roomId` (GAP-01); T1 thiếu sticker; T4 chỉ happy path (AP-3) |
| **A.5** Gap & orphan | ✔ Pass | Không có ORPHAN; mọi TC trace được về scope |
| **A.6** Fix-shape adversarial | ❌ Fail | 5 fix shape → 1 BLOCKER (webhook) + 4 MAJOR — xem §3.5 |
| **B.1** Rõ ràng | ✔ Pass | Precondition/steps/expected cụ thể, oracle đo được (`status = 2`, `', '`, `type = 1`) |
| **B.2** Atomic | ✔ Pass | Mỗi TC 1 mục đích chính |
| **B.3** Độc lập | ⚠️ Một phần | `NEW-7`, `NEW-23` phụ thuộc TC join/message chạy trước (có ghi rõ ở precondition) |
| **B.4** Realistic | ✔ Pass | Dùng mock LINE API, roomId đặt tên có nghĩa (`Rvip01`, `Rplain01`…) |
| **C** Chất lượng bộ TC | ⚠️ Một phần | Tỷ lệ Normal 11 : Abnormal 12 : Boundary 4 — hợp lý với task thiên xử lý lỗi. Không còn trùng lặp (§4.5). **Nhưng 8/27 TC mang mã quan điểm ngoài bộ chuẩn** |
| **D** Spec alignment | ❌ Fail | 8 điểm cần chốt ở §6, trong đó 3 điểm là **mâu thuẫn giữa Redmine description và code thực tế** |
| **E** Hành chính | ⚠️ Một phần | `TC No.` dùng `temp_id` Studio; `spec_status` null toàn bộ; chưa ghi loại evidence bắt buộc |

### F.1 — Bảng quan điểm đối chiếu

Quan điểm **đáng lẽ phải ◯** cho task (suy từ root cause + cách fix + F/D/T + bản chất "job callback nhận webhook LINE"):

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `INTG-LINE-001` | Cao | ◯ BẮT BUỘC — gọi LINE API + nhận webhook LINE | NEW-26, NEW-31 | 0/2 | ⚠️ RISK — có TC nhưng chưa chạy; thiếu unknown error (ISS-11) |
| `INTG-HOOK-001` | Cao | ◯ **BẮT BUỘC** — nhận webhook từ bên ngoài | **không có** | — | ❌ **[BLOCKER]** GAP-03 |
| `INTG-HOOK-002` | Trung bình | ◯ — luồng chỉ hoàn tất khi webhook tới | **không có** | — | ❌ [MAJOR] — không TC nào chặn webhook để verify không treo |
| `COMPAT-LEGACY-001` | Cao | ◯ **BẮT BUỘC** — room đời cũ (pre-v10.17.0) chạy song song group | NEW-28 | 0/1 | ❌ **[BLOCKER]** GAP-02 — `NEW-28` chỉ là nhánh giữ tên cũ, không phải room chưa có record |
| `REG-SHARED-001` | Cao | ◯ **BẮT BUỘC** — `checkAddGroup` / `updateGroupMember` đổi signature | NEW-41, NEW-42, NEW-43 | 0/3 | ⚠️ RISK — chỉ happy path (AP-3), chưa rà brand khác |
| `DATA-DB-001` | Cao | ◯ **BẮT BUỘC** — có UPDATE (`is_blocked`) | NEW-23, NEW-7 | 1/2 | ❌ **[BLOCKER]** — thiếu `WHERE` scope 2 tài khoản (GAP-05) |
| `ENV-003` | Cao | ◯ **BẮT BUỘC** — job nền, không được × vì "staging đã pass" | **không có** | — | ❌ **[BLOCKER]** ISS-02 |
| `JOB-001` | Cao | ◯ **BẮT BUỘC** — job nền gọi API bên thứ 3 theo lô | NEW-32 | 0/1 | ❌ [MAJOR] ISS-12 — chỉ 1 event, không lô lớn, không backoff |
| `MSG-001` | Cao | ◯ — gửi tin phải tới đúng đối tượng (`to = roomId`) | **không có** | — | ❌ **[BLOCKER]** GAP-01 |
| `FUNC-001` | Cao | ◯ — luồng chính room hoàn tất đúng đặc tả | NEW-44, NEW-35, NEW-36, NEW-29 | 0/4 | ⚠️ RISK — thiếu sticker (ISS-16); `NEW-30` bị gán mã lạ nên không tính vào đây (ISS-07) |
| `FUNC-004` | Cao | ◯ — giới hạn 5 member, độ dài tên ghép | NEW-27, NEW-25, NEW-33 | 0/3 | ⚠️ RISK — thiếu biên độ dài tên (ISS-13) |
| `CONC-001` | Cao | ◯ — 1 event chỉ xử lý 1 lần | NEW-37 | 0/1 | ⚠️ RISK — `NEW-37` là 2 event hợp lệ, không phải cùng 1 event lặp → chồng lấn GAP-03 |
| `MSG-USER-001` | Cao | ◯ BẮT BUỘC — tương tác với friend LINE | NEW-22 | 0/1 | ⚠️ RISK — chỉ cover `memberJoined` / `memberLeft`; thiếu member block/unblock, member đã xóa tài khoản |
| `DATA-001` | Cao | ◯ — dữ liệu room phản ánh đủ ở màn Chat | NEW-44, NEW-45 | 0/2 | ⚠️ RISK |
| `DATA-TEXT-001` | Trung bình → **Cao** (text gửi LINE) | ◯ — tên room lấy từ tên LINE user | **không có** | — | ❌ [MAJOR] ISS-13 |
| `DATA-REF-001` | Cao | ◯ — `group_members` / khóa tham chiếu của room | **không có** | — | ❌ [MAJOR] ISS-14 |
| `UI-003` | Trung bình → **Cao** (rủi ro false success) | ◯ — room tên rỗng phải render an toàn | NEW-45 | 0/1 | ⚠️ RISK |
| `PERF-LARGE-001` | Trung bình | ◯ — nhiều room × nhiều member | **không có** | — | ❌ [MAJOR] — gộp vào ISS-12 |
| `SEC-ISO-001` / `PERM-003` | Cao | ◯ — cách ly dữ liệu đa tài khoản OA (2 bot cùng room) | **không có** | — | ❌ [MAJOR] — gộp vào GAP-05 |
| `SYNC-APP-001` | Trung bình | ◯ — hội thoại room hiển thị trên mobile app | **không có** | — | ❌ [MAJOR] — chưa xác nhận app có hiển thị room không |
| `STATE-001` | Cao | ◯ — vòng đời join → message → leave → join lại | NEW-37, NEW-36 | 0/2 | ⚠️ RISK |
| `DEPLOY-LIVE-001` | Cao | ◯ — release không lock maintain | **không có** | — | ❌ [MAJOR] — gộp REG-RUN-001 |
| `REG-RUN-001` | Cao | ◯ — `callback_event` tồn đọng từ trước release | **không có** | — | ❌ [MAJOR] — event room cũ nằm sẵn trong hàng đợi khi deploy có được xử lý đúng không |
| `DATA-AUDIT-001` | Cao | × | — | — | Không có thao tác trên dữ liệu nhạy cảm do người dùng thực hiện (RULE-03: lý do đã ghi) |
| `PAY-*` | Cao | × | — | — | Task không chạm thanh toán (RULE-03) |
| `LIFF-ENTRY-001` | Cao | × | — | — | Không phát sinh URL cho LINE user trong scope commit này (RULE-03) |
| `MEDIA-*` | — | × | — | — | Không đổi xử lý media; `NEW-34` chỉ đi qua nhánh job media có sẵn (RULE-03) |

**Tổng kết F.1**: 23 quan điểm ◯ · **8 quan điểm hoàn toàn không có TC**, trong đó 4 ở mức Cao và BẮT BUỘC (`INTG-HOOK-001`, `ENV-003`, `MSG-001`, `SEC-ISO-001`/`PERM-003`) · **không quan điểm nào có TC đã chạy pass**, ngoài `DATA-DB-001` (1/2).

---

## 8. Ký duyệt

| Vai trò | Tên | Ngày | Trạng thái |
|---|---|---|---|
| Reviewer (draft AI) | `/review-tc` | 2026-08-26 | Draft — **cần Leader verify** |
| Test Leader | | | ☐ Chờ duyệt |
| Member nhận feedback | | | ☐ Chờ fix |

**Điều kiện để chuyển sang round 2**: fix xong 6 `[BLOCKER]`, chốt xong SPEC-04 và SPEC-06 với Dev/Leader (2 điểm này chặn việc viết đúng expected cho TC bổ sung), và chạy thật bộ TC với evidence theo RULE-02.
