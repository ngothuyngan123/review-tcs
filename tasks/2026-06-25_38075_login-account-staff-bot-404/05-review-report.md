# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38075 — Login account thanhntp142+1 bị hiện lỗi 404` |
| Reviewer (Leader) | `<điền tên Leader>` |
| Tester được review | `<điền tên tester>` |
| Ngày review | `2026-06-25` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: Không có `02-spec-reference.md` riêng → dùng `templates/LME-SYSTEM-SPEC.md` tổng. Không có business rule chi tiết cho luồng select-bot/BasicAccess trong spec tổng → review dựa trên `03-dev-impact.md` + checklist LME (CL-Func-1, CL-NonF-2/4/5).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Bộ TC cover tốt luồng **login** với 6 trạng thái select-bot, nhưng đây là fix **access-control ở middleware `handle()`** (chạy trên MỌI request) → còn bỏ lọt 2 chiều quan trọng: (1) **truy cập trực tiếp URL** màn bot khi đang select bot không có quyền, (2) **staff bị thu hồi quyền giữa session** ("không còn là staff" đúng nguyên văn root cause). Thêm `F2 getRouterBotInvite()` chưa có TC nào, và TC003/TC004 trống Expected.

---

## 2. Tóm tắt cho member

Bộ TC bám rất sát luồng đăng nhập và đã phủ đủ 6 trạng thái của `user_selected_bot` (chưa có bot / chưa select / owner / staff / không-staff / bot đã xóa) — TC007 và TC008 đúng là 2 case lõi của bug, rất tốt. Điều cần bổ sung: bug này fix ở **middleware kiểm soát quyền** nên phải test cả việc **gõ thẳng URL màn bot** khi đang đứng ở bot không có quyền (không chỉ login), case **đang là staff rồi bị gỡ quyền giữa chừng** (đúng chữ "không còn là staff"), và **regression cho `getRouterBotInvite()`**. Ngoài ra TC003/TC004 đang trống Expected nên chưa chạy được — cần điền.

---

## 3. Coverage Matrix

> Map suy luận từ Title / Precondition / Steps / Expected (file 04 không có cột Map to Impact).

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG (select bot không có quyền → 404, fix = redirect pre-select-bot) | Fix | — | TC007 (không-staff), TC008 (bot đã xóa) | 2 | **RISK** — chỉ reproduce qua **login**; thiếu chiều "không còn là staff" (revoked) + truy cập trực tiếp URL |
| F1 — `handle()` (BasicAccess middleware) | Function | Direct | TC001, TC002, TC005, TC006, TC007, TC008 (đều ở login) | 6 | **RISK** — middleware chạy trên mọi request nhưng chỉ test entry point **login**; thiếu direct-URL + navigation mid-session |
| F2 — `getRouterBotInvite()` (functions.php) | Function | Direct | — | **0** | **GAP** |
| D1 — Không có data update | Data | — | N/A | — | N/A (Dev xác nhận không chạm data) |
| T1 — Login account staff | Feature | `<Dev chưa ghi risk>` | TC006 (staff→overview), TC007 (không-staff) | 2 | **RISK** — thiếu regression navigation sau login + app side |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề — tất cả TC001–TC008 đều thuộc scope BUG/F1/T1 | Giữ nguyên |

> Lưu ý: TC003/TC004 KHÔNG orphan (thuộc F1) nhưng **chưa hoàn chỉnh** (trống Expected) — xem §4.2.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Validation / specific code-check + redirect** — middleware thêm điều kiện: nếu bot đang select user không có quyền (không owner & không trong `user_staff_bot`) → redirect `pre-select-bot` (Dev ghi "list bot"). KHÔNG phải generic catch-all. |
| Trigger space cần cover | Tổ hợp **trạng thái `user_selected_bot` × quan hệ user-bot × entry point**: (a) chưa có bot, (b) chưa select, (c) bot owner, (d) bot người khác + đang staff, (e) bot người khác + KHÔNG staff, (f) bot đã xóa/không tồn tại, (g) **đang staff rồi bị thu hồi quyền** (revoked), (h) bot **hủy hợp đồng / inactive**. Entry point: **login** ✅ vs **direct URL / navigation mid-session** ❌. |
| Số trigger TCs hiện cover | **6/8 trạng thái** ở entry point login (a–f). Thiếu (g) revoked, (h) inactive/hủy hợp đồng. **0/1** entry point direct-URL (TC003/TC004 trống Expected, lại đặt ở precondition "chưa select" chứ không phải "select bot không quyền"). |
| KH report dạng | **Gần symptom-only** — KH/QA thấy "404", có nêu điều kiện data (bot_id của user khác + không trong `user_staff_bot`) nên đã có 1 root cause. Nhưng "404" có thể đến từ **state khác** chưa verify (bot inactive, bot hủy hợp đồng, bot khác tenant). |
| Alternative root causes cần verify | (1) Đang là staff → bị **gỡ** khỏi `user_staff_bot` sau khi đã select (đúng chữ "không còn"); (2) bot **hủy hợp đồng / inactive** (`is_deleted=0` nhưng không hoạt động); (3) bot thuộc tenant/công ty khác. |
| Anti-patterns dính | **AP-2** (symptom-only, partial), **AP-4** (PR link trống — không verify được fix shape thực tế ở mọi entry point), **AP-6** (mục 3 caller trống). AP-1 KHÔNG dính (fix không phải generic catch). AP-3 partial (regression login). |

> Trigger space cover < tổng (thiếu revoked + inactive + direct-URL) → flag [BLOCKER]/[MAJOR] FIX-SHAPE trong §4.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-1 (F1 `handle()`):** Fix nằm ở **middleware chạy trên mọi request**, nhưng toàn bộ TC chỉ test entry point **login**. Thiếu case: user đang select 1 bot **không có quyền** rồi **gõ thẳng URL màn bot** (vd `/basic/message-template`) hoặc navigate giữa session → phải redirect `pre-select-bot`, **KHÔNG 404, KHÔNG lộ data bot người khác**. Đây là lỗ hổng access-control có thể ship. — *Thêm TC-NEW-01 + TC-NEW-07 (xem §5). Đối chiếu checklist `CL-NonF-2` (access từ menu chính / favourite / trực tiếp URL / hyperlink) + `CL-NonF-4` (đổi param bot_id sang bot khác → từ chối).*
- **[BLOCKER] GAP-2 (F2 `getRouterBotInvite()`):** Function Direct impact trong mục 4.1 nhưng **0 TC** nào chạm tới luồng invite/routing. Thay đổi logic redirect có thể làm hỏng luồng **staff nhận link mời bot**. — *Thêm TC-NEW-04 (regression invite). Hỏi Dev: `getRouterBotInvite()` đã sửa gì, caller nào gọi, để xác định scope.*

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE / SYMPTOM-ONLY (BUG):** Root cause ghi "user đang select vào bot mà mình **không còn** là staff" (revoked), nhưng TC007 chỉ test "user **KHÔNG** là staff" (chưa bao giờ là staff — tĩnh). Chiều **đang staff → bị gỡ quyền sau khi đã select** chưa có TC. — *Thêm TC-NEW-02.*
- **[MAJOR] SYMPTOM-ONLY (AP-2):** "404" có thể phát sinh từ trạng thái khác chưa verify: bot **hủy hợp đồng / inactive** (`is_deleted=0` nhưng ngừng hoạt động), bot khác tenant. — *Thêm TC-NEW-05. Hỏi Dev có alternative state nào cùng cho 404 không.*
- **[MAJOR] TC003 & TC004 — Expected TRỐNG:** Sheet gốc để trống Expected + Test Result → TC **chưa chạy được**, không đo lường được (vi phạm review-checklist B.1). Đồng thời precondition đặt sai ngữ cảnh (đang để "chưa select" thay vì "select bot không quyền" — chính là case security cần test). — *Điền Expected (xem TC-NEW-06) hoặc gộp vào TC-NEW-01.*
- **[MAJOR] AP-6 — Mục 3 dev-impact TRỐNG:** Không list caller đã check. `handle()` là middleware dùng chung → cần biết áp lên những route/nhóm nào; `getRouterBotInvite()` caller chưa rõ. Có thể còn function cùng pattern chưa fix. — *Yêu cầu Dev list caller + phạm vi route áp middleware.*
- **[MAJOR] AP-4 — PR/Commit link TRỐNG:** Mục "Commit / Pull Request" = `<chưa có>` → không verify được fix là redirect ở tất cả entry point hay chỉ ở nhánh login. — *Yêu cầu Dev cung cấp link PR branch `fix/Task_Basic_Access_Staff`.*
- **[MAJOR] Bug task auto-filled chưa verify:** `01-bug-task.md` có `Auto-filled: 2026-06-25 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. Yêu cầu tester đọc lại Redmine #38075 và tick trước khi review có giá trị.
- **[MAJOR] Dev impact auto-filled chưa verify:** `03-dev-impact.md` có `Auto-filled: 2026-06-25 by /new-task` nhưng checkbox **chưa tick** — F/D/T có thể chưa đầy đủ (đặc biệt mục 3 trống). Yêu cầu tester verify + tick.
- **[MAJOR] Regression navigation (AP-3, T1 + F1):** TC005/TC006 chỉ verify màn **overview** ngay sau login. Vì `handle()` chặn mọi request, cần regression: user có quyền (owner/staff) **navigate qua nhiều màn bot** sau login → đều vào được bình thường (fix không over-block). — *Thêm TC-NEW-03.*
- **[MAJOR] Chưa xác định phạm vi Web vs App (TC-14):** `BasicAccess` middleware có áp cho luồng **app** không? Bug liền kề cùng sheet (#37743) có section App. Nếu app dùng chung middleware mà chỉ test web → bỏ lọt. — *Hỏi Dev; nếu có → bổ sung TC app cho TC007/TC008.*

### 4.3 Minor (có thể fix sau)

- **[MINOR] Module/Màn hình** trong `01` còn `<chưa rõ — tester fill>` — điền "Login / Select bot (BasicAccess middleware)".
- **[MINOR] Mâu thuẫn nhãn target redirect:** Dev ghi "redirect về màn **list bot**" (file 03) còn TC expect `/admin/pre-select-bot`. Cần thống nhất 1 tên màn để Expected đo lường chính xác (xem §6).
- **[MINOR] Priority cột trống** toàn bộ TC — gợi ý gán: TC007/TC008/TC-NEW-01 = High; TC001/TC002/TC005/TC006 = Medium.

### 4.4 Nit (gợi ý)

- **[NIT] TC001** ("chưa có bot → màn add bot") hơi ngoài root cause (không liên quan quyền staff) nhưng giữ lại làm smoke regression luồng login là hợp lý.
- **[NIT]** Cân nhắc thêm `CL-NonF-5`: gõ URL màn bot khi **chưa login** → redirect login (middleware-adjacent, smoke nhẹ).

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Direct URL màn bot khi đang select bot KHÔNG có quyền | `user_selected_bot` trỏ bot của user khác, user KHÔNG là staff (không có trong `user_staff_bot`); user đã đăng nhập | 1. Đăng nhập (đã bị đẩy về pre-select-bot)<br>2. Gõ thẳng URL 1 màn bot, vd `/basic/message-template` của bot không có quyền | Redirect về `/admin/pre-select-bot` (hoặc màn từ chối). KHÔNG hiển thị 404, KHÔNG hiển thị data của bot người khác | High | Negative/Security | BUG, F1, CL-NonF-2 |
| TC-NEW-02 | Staff bị thu hồi quyền SAU khi đã select bot ("không còn là staff") | User là staff bot B, đã select bot B (có bản ghi `user_selected_bot`); admin xóa user khỏi `user_staff_bot` của bot B | 1. (Đang ở session bot B) admin gỡ quyền staff<br>2. User reload / navigate sang màn bot B khác / login lại | Redirect về `/admin/pre-select-bot`, KHÔNG 404, không còn vào được bot B | High | Negative | BUG (root cause "không còn"), F1 |
| TC-NEW-03 | Regression: staff/owner có quyền navigate nhiều màn sau login | `user_selected_bot` trỏ bot user là owner HOẶC đang là staff hợp lệ | 1. Đăng nhập → vào overview<br>2. Lần lượt mở ≥ 3 màn bot khác nhau (message-template, friend-information, broadcast…) | Mọi màn vào bình thường, không bị middleware đẩy về pre-select-bot | Medium | Regression | F1, T1 |
| TC-NEW-04 | Regression `getRouterBotInvite()`: staff nhận link mời bot | Có link mời staff vào 1 bot (invite flow) | 1. User mở link mời bot<br>2. Đăng nhập / accept lời mời | Routing đúng tới bot được mời (theo spec invite hiện hành), không bị redirect sai sang pre-select-bot | High | Regression | F2 |
| TC-NEW-05 | Select bot hủy hợp đồng / inactive (`is_deleted=0` nhưng ngừng hoạt động) | `user_selected_bot` trỏ bot đã hủy hợp đồng hoặc inactive | 1. Đăng nhập | Hành vi đúng spec (redirect pre-select-bot hoặc thông báo), KHÔNG 404 — *xác nhận expected với Dev/PM* | Medium | Boundary | BUG (alt root cause), CL-Func-20 |
| TC-NEW-06 | (Hoàn thiện TC003/TC004) Direct URL khi CHƯA select bot | User đã có bot; `user_selected_bot` không có bản ghi | 1a. Gõ URL màn **bot** `/basic/message-template`<br>1b. Gõ URL màn **user** `/admin/my-page` | 1a → redirect `/admin/pre-select-bot` (chưa chọn bot không vào được màn bot)<br>1b → vào được màn my-page (màn user không phụ thuộc bot) — *xác nhận với Dev* | Medium | Negative | F1 |
| TC-NEW-07 | Security: đổi param bot_id trên URL sang bot không có quyền | User đã login, đang ở 1 bot hợp lệ | 1. Sửa `bot_id` (hoặc id trên URL) sang bot của user khác mà mình không là staff | Từ chối access / redirect, không lộ data — theo `CL-NonF-4` | High | Negative/Security | F1, CL-NonF-2/4 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần làm rõ (không hẳn update spec — cần Dev/PM confirm)**:
  - **Section**: Luồng select-bot / màn redirect khi bot không hợp lệ.
  - **Nội dung cần làm rõ**: Thống nhất tên màn đích redirect — Dev ghi "màn **list bot**", TC dùng `/admin/pre-select-bot`. Định nghĩa rõ hành vi cho từng state: không-staff / bot đã xóa / bot hủy hợp đồng / staff bị thu hồi → màn nào, có message gì.
  - **Người chịu trách nhiệm**: Dev `Tuấn Anh Trần` + PM/Leader.

---

## 7. Checklist đã chạy

- [x] A. Coverage — RISK ở BUG/F1/T1, GAP ở F2 (xem §3)
- [x] B. Chất lượng từng TC — TC003/TC004 fail (trống Expected)
- [x] C. Chất lượng bộ TC tổng thể — thiếu chiều Security + Regression navigation + App
- [x] D. Spec alignment — mâu thuẫn nhãn màn redirect (§6)
- [x] E. Hành chính — Tester/version chưa điền; 2 checkbox auto-fill verify chưa tick
- [x] F. Base checklist LME
  - [x] **F.1 Checklist web** — **CL-Func-1** (account staff: không quyền → không access, có quyền → thao tác như account chính) **chưa cover đủ** (chỉ login, thiếu navigation/direct-URL). **A.2 Non-function — CL-NonF-2/CL-NonF-4** (security access staff không quyền, đổi param bot_id) **GAP**. CL-NonF-5 (URL khi chưa login) chưa test.
  - [x] **F.2 Checklist job** — Không liên quan (fix ở web middleware, không chạm job).
  - [x] **F.3 Các tính năng chung** — C.7 Plan limits: không trực tiếp; lưu ý liên hệ CL-Func-20 (hủy hợp đồng) qua TC-NEW-05. TC-12 (đối tượng đã xóa) ✅ đã cover bởi TC008. TC-14 (web↔app) ❓ chưa rõ.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
