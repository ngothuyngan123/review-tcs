# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #38447 — [Chat 1:1] Tin nhắn đối tác không phản ánh đủ vào phòng chat (tái phát dù bật 『Webhookの再送』) |
| Reviewer (Leader) | `<Leader điền>` |
| Tester được review | `<member điền>` (TC nguồn: Sheet "Test callback friend" row 198~243) |
| Ngày review | 2026-07-09 |
| Version TCs | v1 |
| Vòng review | Round 1 |

> **Note spec reference**: Folder không có `02-spec-reference.md` → dùng `templates/LME-SYSTEM-SPEC.md` tổng (feature Chat 1:1 / Callback friend), không có spec riêng cho task này.
> **Note nguồn TC**: File 04 được `/new-task` fetch nguyên văn từ Redmine #38447 Link TCs (Sheet human "Test callback friend"). Đây là bộ TC đã chạy (đa số Status = `OK`, 4 case `Reject`), không phải draft mới.

---

## 1. Verdict

- [ ] **APPROVED**
- [x] **APPROVED WITH CHANGES** — Bộ TC cover tốt phần fix chính, nhưng **có 1 residual drop-path chưa test (media+message batch)** + 2 gate auto-fill chưa verify. Cần Dev trả lời 1 câu hỏi trước khi chốt.
- [ ] **REJECTED**

**Lý do ngắn gọn**: Coverage mechanical mạnh (mọi F1–F4 / T1–T4 đều có ≥ 1 TC đã chạy, có concurrency + batch test). Nhưng fix **giữ nguyên `return` cho `STATUS_MEDIA_NEW`** → batch [media, message] có thể **vẫn rớt message** (chính TC036 reject note tự xác nhận). Đây là điểm phải confirm với Dev — nếu media job KHÔNG reprocess phần còn lại của batch → **escalate BLOCKER**.

---

## 2. Tóm tắt cho member

Bộ TC "Test callback friend" rất chắc ở phần cốt lõi: bạn đã cover đúng kịch bản bug (callback gộp nhiều event, event skip đứng trước không được làm rớt event hợp lệ sau) qua TC034/035/042/044, lại có sẵn test đồng thời nhiều user/nhiều callback — đó là điểm mạnh thật sự. Hai việc cần làm: (1) tick 2 checkbox "Tester verify auto-fill" ở file 01 + 03 sau khi đọc lại Redmine; (2) chú ý 3 case đang để `Reject` (TC033/036/045) — đây đúng là kịch bản webhook thật của KH (nhiều loại event trộn nhau), đặc biệt **case media+message (TC036) tự ghi rằng message sau media không được xử lý tiếp** → cần hỏi Dev xem đây có phải root cause còn sót không.

---

## 3. Coverage Matrix

> Suy luận map từ Title / Precondition / Steps / Expected. `*` = TC có Status `Reject` (KHÔNG chạy — chỉ monitor).

| Impact | Loại | Priority | TCs map | # TC (chạy) | Status |
|---|---|---|---|---|---|
| BUG — event skip đứng trước không làm rớt event hợp lệ sau | Fix | — | TC034, TC035, TC042, TC044, TC037–TC041, TC043 · (TC033*, TC036*, TC045* reject) | 11 | **OK** (fix chính đã test) — xem §3.5 residual gap |
| F1 — `doHandleMessage` (group + ignore source) | Function | Direct | TC034 (ignore-source room), TC029 (friend+group cùng batch), TC021–TC032 (group) | 12 | OK |
| F2 — `doHandlePostbackEvent` (ignore source) | Function | Direct | TC035 (postback ignore-source + valid sau), TC008–TC014, TC025 | 8 | OK |
| F3 — `doHandleVideoPlayComplete` (2 nhánh NOT_FRIEND) | Function | Direct | TC042 (NOT_FRIEND + Friend), TC043 (nhiều VideoPlayComplete) · (TC036* reject) | 2 | OK (same-type) — cross-type deferred |
| F4 — `doHandleFollowEvent` (BLOCKED_BY_BOT) | Function | Direct | TC044 (blocked + follow valid, verify `is_block` không đổi), TC018, TC019 | 3 | OK |
| D1 — MessagesV2s + UnconfirmMessage + Conversation/ES + socket | Data | CREATE/UPDATE | TC001–TC007, TC021–TC030, TC037/TC038 | ~20 | OK (verify tạo đủ msg + status uncomfirm + count) — xem MINOR về ES/socket |
| D2 — `callback_event.status` event skip → DONE | Data | UPDATE | — (không TC; dev: terminal/không query → chỉ thống kê) | 0 | **RISK-low** (monitor-only, không quan sát được bằng manual UI) |
| T1 — Chat 1:1 + group nhận tin inbound | Feature | High | TC001–TC007, TC021–TC030, TC037/TC038 (+ concurrency TC003/004/016/017) | ~20 | OK (full path + multi + batch + concurrency) |
| T2 — Postback (button/richmenu/imagemap/video) | Feature | Medium | TC008–TC014, TC025, TC035, TC039, TC041 | ~10 | OK |
| T3 — Video play complete | Feature | Medium | TC042, TC043 · (TC036* reject) | 2 | OK |
| T4 — Follow | Feature | Medium | TC018, TC019, TC020 (unfollow), TC044 | 4 | OK |

### ORPHAN TCs

| TC ID | Title | Lý do | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề. TC001–TC032 (single-event + same-type batch) là **regression hợp lệ** cho side-effect "method giờ chạy cho mọi event trong batch" (mục 3 dev-impact) | Giữ nguyên |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Control-flow fix trong vòng lặp per-event** (`return` → `continue` ở nhánh skip). KHÔNG phải generic catch-all / validation / cache / migration. Gần nhất với nhóm "batch/event ordering". |
| Câu hỏi adversarial cốt lõi | "Khi 1 event bị skip đứng TRƯỚC trong batch, event hợp lệ SAU có còn được xử lý không?" |
| Trigger space cần cover | (a) skip-source-room trước + message hợp lệ sau [F1]; (b) group-message trước + 1:1 sau [F1]; (c) postback-ignore-source trước + postback hợp lệ sau [F2]; (d) NOT_FRIEND video trước + friend video sau [F3]; (e) BLOCKED_BY_BOT follow trước + follow hợp lệ sau [F4]; (f) **MEDIA_NEW trước + message sau** [nhánh giữ `return` cố ý]; (g) cross-event-type trộn (follow+message, media+message, mixed) |
| Số trigger TCs hiện cover (chạy) | (a) TC034 ✓ · (b) TC029 ✓ · (c) TC035 ✓ · (d) TC042 ✓ · (e) TC044 ✓ · (f) **CHƯA TEST** (TC036 reject) · (g) **CHƯA TEST** (TC033/036/045 reject → monitor) |
| KH report dạng | **Symptom-only** — KH chỉ mô tả "một số tin nhắn không phản ánh", không có error code. Dev trace được root cause code cụ thể (return giữa loop) → rủi ro alternative-root-cause **thấp hơn** bình thường, NHƯNG nhánh giữ `return` (MEDIA_NEW) là ứng viên alternative-drop-path cần loại trừ. |
| Alternative root causes cần verify | Batch chứa **MEDIA_NEW / STATUS_MEDIA_NEW** đứng trước message thường → do fix cố ý giữ `return`, message sau có thể vẫn rớt. Reject-note của TC036 xác nhận: *"chỉ sửa lý callback của video, còn callback của message sẽ không xử lý tiếp được"*. |
| Anti-patterns dính | **AP-2 (một phần)** — symptom-only + 1 root cause; giảm nhẹ vì Dev có code trace. **Không dính** AP-1 (không generic-catch), AP-3 (regression có batch+concurrency, không happy-only), AP-4 (có PR link 2 commit), AP-5 (không over-coverage layer khác), AP-6 (mục 3 đã fill). |

> **Kết luận §3.5**: 5/7 trigger đã test (a–e). Trigger (f) media+message và (g) cross-type là **gap chưa test**. (f) nguy hiểm nhất vì trùng đúng symptom KH → xem §4.2 FIX-SHAPE, có thể escalate BLOCKER.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- _(Chưa có BLOCKER cứng — mọi impact đều có ≥ 1 TC đã chạy. Nhưng §4.2 FIX-SHAPE có thể escalate lên BLOCKER tùy câu trả lời của Dev.)_

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE — GAP-1 (media+message batch, ưu tiên #1):** Fix **giữ nguyên `return` cho `STATUS_MEDIA_NEW`** (defer sang media job). Nếu 1 webhook batch có event media đứng trước message thường → `return` vẫn thoát method → **message sau vẫn rớt** = ĐÚNG symptom KH báo. TC036 (video/media + message) đang `Reject` và reject-note tự xác nhận message không được xử lý tiếp. → **Hỏi Dev**: media job có reprocess **toàn bộ phần còn lại** của batch không? (1) Nếu CÓ → thêm TC-NEW-01 để verify. (2) Nếu KHÔNG → **escalate BLOCKER**: đây là root-cause còn sót, cùng class bug, cần fix code (đổi `return`→`continue` + defer media riêng cho từng event).

- **[MAJOR] SYMPTOM-ONLY — GAP-2:** KH report symptom-only (không error code). Dev tái hiện 1 root cause (return giữa loop). Cần loại trừ drop-path khác cùng tạo symptom "tin nhắn không phản ánh" — ứng viên chính là (f) media-mixed ở trên. Đề nghị replay **payload thật của KH** (conversion 55672388, friend 森川一樹, botId 200163 — có trong file 01) trên staging để confirm sau fix message lưu đủ → **TC-NEW-02**.

- **[MAJOR] TC033 / TC036 / TC045 để `Reject` (cross-event-type batch):** Đây đúng là hình dạng webhook production thật (LINE gộp **nhiều loại event** trong 1 callback). Lý do reject là **giới hạn test infra** (postman tạo 2 callback khác user bị LINE gộp về cùng 1 user), không phải code đã an toàn. → Xác nhận với Leader/Dev: **monitor đã deploy chưa** (dev nhắc "add monitor để theo dõi" ở cả 3 note)? Nếu chưa có monitor → coverage cross-type = 0 và không có cả monitor → nâng lên rủi ro cao. Ghi rõ quyết định chấp nhận rủi ro.

- **[MAJOR] Auto-fill chưa verify — file 01:** `01-bug-task.md` có `Auto-filled: 2026-07-09 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. Yêu cầu tester đọc lại Redmine #38447 (description + journals) và tick trước khi review có giá trị pháp lý.

- **[MAJOR] Auto-fill chưa verify — file 03:** `03-dev-impact.md` cũng `Auto-filled: 2026-07-09 by /new-task`, checkbox verify **chưa tick**. F1–F4 / D1–D2 / T1–T4 map từ journal Dev chưa được tester confirm → nếu mapping sai thì cả coverage matrix lệch. Yêu cầu tick sau khi verify.

### 4.3 Minor (có thể fix sau)

- **[MINOR] D2 (`callback_event.status`) không có TC verify:** Chấp nhận được theo góc nhìn manual tester (status terminal, không quan sát bằng UI) — nhưng nên verify qua **monitor/stats dashboard** rằng event skip = `DONE`, không kẹt retry. Ghi TC-NEW-04 (Low).

- **[MINOR] D1 — ES/socket/badge realtime không assert tường minh:** Các TC verify "hiển thị ở màn chat 1:1 + count uncomfirm" nhưng không nói rõ **badge/preview cập nhật realtime qua socket** (dev-impact mục 4.2 có nhắc "push socket"). Bổ sung 1 dòng expected: "badge + last message preview cập nhật ngay không cần reload".

- **[MINOR] Title generic:** TC016 / TC017 / TC027 / TC028 dùng title "Check dummy data" — không nói rõ mục đích. Đổi thành vd "Batch nhiều callback cùng thời điểm của 1 user — không rớt/không duplicate".

### 4.4 Nit (gợi ý)

- **[NIT]** Cột Type / Priority của toàn bộ TC đang trống (nguồn Sheet không có) → điền để prioritize khi regression (đặc biệt đánh dấu TC034/035/042/044 = High vì cover trực tiếp fix).
- **[NIT]** Nhiều ô Expected trống (kế thừa merge từ hàng trên trong Sheet gốc) → khi đưa vào tool, điền đủ để mỗi TC chạy độc lập (checklist B.3).

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` round tiếp theo. (TC-NEW-01/03 chỉ cần khi Dev xác nhận hướng ở §4.2.)

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Batch [MEDIA_NEW event trước + message thường sau] — message sau media không bị rớt | Bot có friend A; dùng postman tạo 1 callback gồm 2 event của cùng user: (1) event media/`STATUS_MEDIA_NEW`, (2) message text thường | 1. Gửi callback batch qua postman theo thứ tự trên. 2. Chờ job callback + media job chạy xong. 3. Mở Chat 1:1 của friend A | Cả event media LẪN message text sau đều được lưu → hiển thị đủ 2 message trên chat 1:1; count uncomfirm đúng; KHÔNG rớt message sau media | High | Regression / Boundary | BUG, F1, D1 |
| TC-NEW-02 | Replay payload webhook thật của KH #38447 — message lưu đủ sau fix | Staging có bot mô phỏng ASH株式会社 (botId 200163); có payload/log webhook thời điểm 2026/07/03 12:41:59 (xin Dev/log) | 1. Replay đúng callback batch KH gặp lỗi (friend 森川一樹, conversion 55672388). 2. Chờ xử lý. 3. Kiểm tra phòng chat 1:1 | Tất cả message trong batch được phản ánh vào phòng chat (không còn thiếu) — reproduce chính xác bug đã fix | High | Positive (reproduce KH) | BUG |
| TC-NEW-03 | Cross-event-type batch [follow BLOCKED_BY_BOT (A) + message (B)] — B vẫn được xử lý | 2 friend A (đang bị bot block), B; test infra cho phép tạo callback cross-user (hoặc verify qua monitor) | 1. Tạo 1 callback gồm follow của A (blocked) + message của B. 2. Chờ xử lý | Follow A bị ignore (is_block không đổi); message B được tạo đủ trên chat 1:1 → mở lại TC033 khi infra sẵn sàng | Medium | Regression | BUG, F4, F1 |
| TC-NEW-04 | Monitor: callback_event.status của event skip = DONE, không kẹt retry | Có quyền xem monitor/stats callback | 1. Trigger batch có event bị skip (IGNORE_GROUP / NOT_FRIEND / BLOCKED_BY_BOT). 2. Xem monitor/DB stats | Event skip có status `DONE` (terminal), không nằm trong hàng đợi retry, không sinh log lỗi lặp | Low | Regression | D2 |

---

## 6. Spec update needed

- [x] Không cần update spec — fix là sửa hành vi rớt event (bug), không đổi business rule. Behavior sau fix = spec vốn có (mọi event trong batch phải được xử lý).
- [ ] Cần update spec

> Lưu ý: nếu §4.2 xác nhận media-mixed vẫn rớt và Dev quyết định để lại (giữ `return`) → cần **ghi rõ giới hạn đã biết** này vào spec/known-issues + monitor, để lần KH báo tiếp không bị coi là bug mới.

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 BUG ✓ (TC034/035/042/044) · A.2 F1–F4 ✓ · A.3 D1 ✓ / D2 RISK-low · A.4 T1–T4 ✓ · A.5 không orphan · **A.6 fix-shape** ✓ (xem §3.5 — gap media-mixed + cross-type)
- [x] B. Chất lượng từng TC — B.1 một số title generic (MINOR) · B.2 atomic OK · B.3 nhiều expected trống do merge (NIT) · B.4 realistic OK
- [x] C. Chất lượng bộ TC — có concurrency (2/3 user, nhiều callback cùng lúc) + batch; phân bổ tốt. Thiếu Type/Priority (NIT)
- [x] D. Spec alignment — không mâu thuẫn (dùng LME-SYSTEM-SPEC tổng)
- [x] E. Hành chính — TC nguồn read-only từ Sheet; version/tester chưa điền (member fill)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — chủ yếu backend callback, ít UI. Liên quan: **CL-Func-19** (hiển thị đủ trigger chat 1:1) ✓ ngầm; A.2 Regression ✓ (effect range Dev = 4 method)
  - [x] **F.2 Checklist job — B.1 Job callback: LIÊN QUAN TRỰC TIẾP.** Đối chiếu **TC-22** (liệt kê & test toàn bộ pattern webhook: normal/abnormal/exception/chưa nhận/trùng + giả lập webhook): bộ TC cover normal + resend (TC015) + gộp chung (MF2) nhưng **cross-type deferred** → chưa "toàn bộ pattern". Ghi nhận ở §4.2.
  - [x] F.3 Các tính năng chung — **C.2 Send message** (nguồn #9 Postback: button/richmenu/imagemap/video ✓ TC008–014; #4 Action callback autoreply ✓ TC005/006; case friend block ✓ TC019/044). Không chạm Bill/Friend info/Tag/Google/Sort/Plan.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
