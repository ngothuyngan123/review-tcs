# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #36730 — [Broadcast] Tab 配信予約: nút 配信数を再計算するボタン biến mất khi di cursor |
| Reviewer (Leader) | `<điền>` (draft do `/review-tc` sinh ngày 2026-05-26) |
| Tester được review | `<chưa rõ — TC fetch từ Sheet Dev draft, Kim Cúc / Kieu Son Tung>` |
| Ngày review | 2026-05-26 |
| Version TCs | v1 (draft fetch từ Sheet) |
| Vòng review | Round 1 |

> ⚠️ **Spec reference**: Không có `02-spec-reference.md`. Fallback tham chiếu `templates/LME-SYSTEM-SPEC.md` — section Broadcast (T1 trong 38 features). Không có spec riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có 4 BLOCKER + 7 MAJOR, cần fix và review lại.

**Lý do ngắn gọn**: 22 TC nhưng **Expected result trống toàn bộ** → không thể run; không có TC nào explicit verify root cause (hover-cursor-trace flow); không test cross-browser cho CSS fix; format hierarchical sparse khiến TC002/4/6/8/... rỗng Title, không atomic.

---

## 2. Tóm tắt cho member

Bộ TC fetch từ Sheet đã cover ý tưởng đúng (2 tab 配信予約 + 下書き, role staff), nhưng còn ở dạng **outline thô** — chưa fill Expected result, mỗi sub-step lại để thành 1 row rỗng (TC002/4/6...) khiến tester sau không hiểu phải verify gì. Critical nhất: **chưa có 1 TC nào mô tả rõ thao tác "hover → di cursor xuống button → click"** đúng theo bug KH; cần ít nhất 1 TC explicit reproduce + ≥ 2 TC cross-browser (Win Chrome / Mac Safari) vì fix là CSS position — vùng cực dễ break theo browser/viewport. Sau khi reformat về chuẩn 10-col + fill Expected + bổ sung TCs ở §5 thì OK.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause: button click được sau khi hover di cursor) | Fix | — | (không TC nào explicit verify thao tác di cursor xuống button); TC001-TC010 mới chỉ "Tạo + check ở màn list" | 0 explicit | **GAP** |
| F1 — CSS popover hover (`public/css/send_all.css`) | Function | Direct | TC001-TC020 (gián tiếp qua hover ở 2 tab list) | 20 gián tiếp | **RISK** — không TC verify trực tiếp style `top` / popover position |
| D — (không có data impact) | Data | — | N/A | — | OK |
| T1 — Tab `配信予約` (đợi send / đã đặt lịch) | Feature | Medium | TC001-TC010 | 10 | **RISK** — Expected trống → không pass/fail được |
| T2 — Tab `下書き` (draft) | Feature | Medium | TC011-TC020 | 10 | **RISK** — Expected trống |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC022 | "Account staff không quyền broadcast: Staff login → cố access URL form detail → kiểm tra hiển thị / redirect." | Bug là CSS fix, không liên quan permission redirect. Expected "redirect" không cover bug này. Title đề cập "form detail" — không phải broadcast list. | Remove HOẶC rewrite: "Staff không quyền broadcast → verify URL màn list send all bị từ chối hợp lý" |
| TC021 (partial orphan) | "Account staff có quyền broadcast: click/hover hiển thị được thông tin thao tác send all" | Title đúng scope CL1, nhưng Expected trống → không actionable | Refactor: cụ thể hóa expected "staff thấy popover + button như admin chính, click button recalc OK" |

### Coverage LME §F (base checklist)

| Item | Liên quan? | Member cover? | Note |
|---|---|---|---|
| CL1 — Account staff | Có (CL1 áp dụng mọi feature) | Partial (TC021-022 — nhưng TC022 lạc topic) | Cần rewrite TC021, remove/rewrite TC022 |
| CL2 — Reload sau save | Có (đảm bảo CSS render ổn định sau reload) | Không | Cần thêm 1 TC reload màn list sau khi tạo broadcast |
| CL3 — Chuyển tab setting | Có (chuyển 配信予約 ↔ 下書き) | Không có TC explicit | Cần TC switch tab → verify popover style không bị "kế thừa" state |
| CL4 — Thao tác liên tục | Có (hover liên tục nhiều friend) | Không | Cần TC hover qua nhiều friend liên tiếp |
| CL5 — Double click | Có (button recalculate) | Không | Cần TC double click button → verify chỉ trigger 1 lần API |
| CL15 — Phân trang | Có (list send all có phân trang) | Không | Cần TC scroll cuối page + chuyển page → verify popover position |
| A.2 Compatibility Win+Mac (Chrome+Safari) | **CỰC KỲ CÓ** (CSS fix) | **Không** | **BLOCKER** — bắt buộc cross-browser |
| A.2 Security (URL mới) | Không (không có URL mới) | N/A | — |
| A.2 Regression — data cũ chạy bình thường | Có | Partial | TC001-TC020 có ý mô tả nhưng Expected trống |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **CSS position fix** (style `top` của popover) — không match thẳng bảng instruction (không phải generic catch / validation / race / cache / migration / soft-delete). Closest analog: **UI/CSS layout fix** — trigger space = viewport sizes × browsers × scroll positions × list lengths. |
| Trigger space cần cover | (a) Chrome Win, (b) Chrome Mac, (c) Safari Mac, (d) viewport nhỏ vs lớn, (e) list ngắn (1 page) vs dài (scroll), (f) popover position khi số friend ở đầu/giữa/cuối viewport, (g) zoom level browser ≠ 100% |
| Số trigger TCs hiện cover | **0/7** — không TC nào đề cập browser / viewport / scroll position / zoom |
| KH report dạng | **Symptom-only** — KH chỉ tả "button biến mất khi di cursor". KHÔNG có error code / console log / browser info / steps detail. |
| Alternative root causes cần verify | Dev đoán "style top sai". Plausible alternatives cùng tạo symptom: (1) **z-index** popover < container → bị overlap; (2) **pointer-events: none** trên popover/button → bắt sự kiện sai; (3) **mouseleave** event trigger sai (popover ẩn khi cursor vào button); (4) **focus / hover state** logic JS detach popover quá sớm; (5) **CSS transition** làm popover dịch ra khỏi vùng hover; (6) **overflow: hidden** parent cắt popover. Dev đã loại trừ những cái nào? |
| Anti-patterns dính | **AP-2** (symptom-only KH report) + **AP-6** (mục 3 caller trống) + **AP-3 partial** (regression Tx chỉ có 1 chiều, Expected trống nên happy-path-only) |

> Trigger space cover 0/7 + AP-2 dính → flag [BLOCKER] FIX-SHAPE trong §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE: GAP cross-browser test cho CSS position fix** — Fix là `top` style trong `send_all.css`. Popover position là vùng cực dễ break theo browser engine. CL A.2 Compatibility yêu cầu test Win + Mac (Chrome + Safari) bắt buộc. TCs hiện tại **0/4 browser combo** được cover. → Bổ sung TC-NEW-02, TC-NEW-03 ở §5.

- **[BLOCKER] TC001-TC022: Expected result trống TOÀN BỘ** — Không TC nào có giá trị "Expected result". Tester không có tiêu chí pass/fail → không thể run TC. → Member fill Expected cho mọi TC trước round 2.

- **[BLOCKER] GAP-1 BUG coverage: Không TC nào explicit reproduce flow KH "hover → di cursor xuống button → click"** — TC001-TC010 chỉ ghi "Tạo send all + check ở màn list" — chưa cover đúng thao tác di cursor làm button biến mất (root cause flow). Coverage matrix BUG = 0. → Bổ sung TC-NEW-01 ở §5.

- **[BLOCKER] TC format không chuẩn 10-col team** — Source dùng hierarchical (Tab > Scenario > Filter variant). TC002/004/006/008/012/014/016/018 chỉ có 1 col "check khi send broadcast cho user" — Title/Type/Priority/Precondition trống → không atomic, không chạy được độc lập. → Member reformat về 10-col chuẩn, mỗi row = 1 TC hoàn chỉnh.

### 4.2 Major (nên fix)

- **[MAJOR] AUTO-FILL VERIFY: `01-bug-task.md` checkbox "Tester verify auto-fill chính xác" CHƯA tick** — File auto-filled từ Redmine #36730 ngày 2026-05-26 nhưng tester chưa verify lại description/steps/attachment. Yêu cầu tester đọc lại Redmine + tick checkbox trước khi review có giá trị.

- **[MAJOR] AUTO-FILL VERIFY: `03-dev-impact.md` checkbox CHƯA tick** — F/D/T mapping có thể chưa chính xác / sót impact. Tester verify rồi tick trước round 2.

- **[MAJOR] SYMPTOM-ONLY (AP-2): KH chỉ mô tả triệu chứng "button biến mất khi di cursor"** — Dev đoán root cause = "style top sai". Có ≥ 6 alternative root cause plausible (xem §3.5). Member cần (a) hỏi Dev đã loại trừ các alt root cause này chưa, (b) bổ sung TC verify từ góc DOM inspection — xem TC-NEW-06.

- **[MAJOR] AP-6: Mục 3 dev-impact "Đã check và sửa các function caller" TRỐNG chi tiết** — Dev ghi tựa đề nhưng không list caller cụ thể. File `send_all.css` có thể được include từ nhiều màn (preview broadcast, modal action send all, page chi tiết broadcast). Yêu cầu Dev list explicit các view/template `<link rel="stylesheet">` đến `send_all.css` hoặc dùng class popover liên quan. Có thể có màn khác cùng bug.

- **[MAJOR] GAP-2: Không test với list dài / phân trang / scroll cuối page** — Popover position dễ vỡ khi số friend ở vị trí cuối viewport (popover bị flip lên trên hoặc bị clip). CL15 yêu cầu test phân trang. → Bổ sung TC-NEW-04.

- **[MAJOR] GAP-3: Tab 配信済み (sent / đã gửi) không được test** — Dev list 4.3 chỉ 2 tab (配信予約 + 下書き) nhưng màn list send all thường có ≥ 3 tab. Nếu tab 配信済み cũng dùng cùng `send_all.css` → cần regression. Hỏi Dev confirm + bổ sung TC-NEW-05 (hoặc đánh dấu skip nếu Dev confirm tab không dùng class này).

- **[MAJOR] TC001-TC020 Title quá generic, không nêu thao tác chính** — Title chỉ "Check ở tab: 配信予約" / "Tạo send all send ngay" — không đề cập "hover số friend" / "button 配信数を再計算" / "di cursor". Leader/QA sau đọc không suy luận được TC cover impact gì. Member rewrite Title chứa keyword `popover` hoặc `配信数を再計算` để map F1.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC021 Expected trống** — Title rõ scope CL1 (staff có quyền) nhưng Expected để member fill. Refactor: "Staff thấy popover + button recalc giống admin chính, click button OK".

- **[MINOR] TC022 lạc topic** — Title "Account staff không quyền broadcast → access URL form detail → redirect" — đề cập "form detail" trong khi bug ở "broadcast send all". Hoặc rewrite về scope (staff thiếu quyền → access URL màn list send all bị block hợp lý) hoặc remove.

- **[MINOR] Type column dùng "Tạo send all send ngay" / "Tạo send all đặt lịch"** — không phải Positive/Negative/Boundary/Regression. Cần phân loại lại đúng template.

- **[MINOR] Priority column dùng "Không filter" / "Có filter"** — không phải High/Medium/Low. Cần phân loại lại.

- **[MINOR] sync-target URL ở `04-tc-list.md` còn `gid=0`** — gid=0 = tab "Info" (data thật ở tab "Improver send all(task broadcast)"). Nếu `/sync-tc` chạy với URL hiện tại sẽ append nhầm sheet. Member resolve gid đúng trước khi sync.

### 4.4 Nit (gợi ý)

- **[NIT] Dev viết "sửa lại style sop"** trong mục 2 dev-impact — typo "sop" → "top". File 03 đã note nhưng nên xin Dev confirm bằng 1 dòng commit message hoặc PR diff.

- **[NIT] 03-dev-impact.md trống** field "Commit / Pull Request" và "Branch" — yêu cầu Dev cung cấp PR link để Leader verify fix shape thực tế (AP-4 phòng ngừa).

- **[NIT] Có thể tách TC-NEW-01** thành 2 TC riêng: (a) verify popover NOT disappear khi di cursor, (b) verify button click recalculate API + UI update.

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | **Reproduce bug KH** — Hover số friend ở tab 配信予約 → di cursor xuống button 配信数を再計算 → button KHÔNG biến mất, click được | Login admin staging.lme.jp; bot có ≥ 1 broadcast trạng thái 配信予約 (đặt lịch tương lai); friend count > 0 | 1. Vào メッセージ配信 → tab `配信予約`<br>2. Hover cursor vào **số friend** của broadcast đầu tiên ở list<br>3. Popover xuất hiện hiển thị số friend + button 「現時点での配信予定数を再計算」<br>4. Di chuyển cursor **chậm** từ số friend xuống button (đi qua khoảng trống nếu có) — **KHÔNG** rời khỏi vùng popover<br>5. Click vào button | B3: Popover visible với button rõ ràng<br>B4: Popover + button **KHÔNG biến mất** trong suốt quá trình di cursor; cursor đến button thì hover state active<br>B5: Button click được → request API recalc fire → số friend cập nhật mới ở popover | High | Positive | BUG, F1, T1 |
| TC-NEW-02 | **Cross-browser Chrome Windows** — Reproduce bug KH trên Win Chrome | Win10/11 + Chrome latest; setup giống TC-NEW-01 | Chạy đúng steps TC-NEW-01 | Giống TC-NEW-01 — popover/button hoạt động đúng | High | Regression | F1, CL Compatibility (A.2) |
| TC-NEW-03 | **Cross-browser Safari Mac** — Reproduce bug KH trên Mac Safari | macOS + Safari latest; setup giống TC-NEW-01 | Chạy đúng steps TC-NEW-01 | Giống TC-NEW-01 | High | Regression | F1, CL Compatibility (A.2) |
| TC-NEW-04 | **Boundary — popover ở vị trí cuối viewport / scroll** | Tạo ≥ 20 broadcast 配信予約; viewport browser nhỏ (~768px); scroll xuống broadcast cuối list | 1. Vào tab 配信予約, scroll xuống broadcast cuối (gần edge bottom viewport)<br>2. Hover số friend của broadcast cuối<br>3. Di cursor sang button 配信数を再計算 | B2: Popover hiển thị (có thể flip lên trên số friend để tránh clip) — visible đầy đủ<br>B3: Button KHÔNG biến mất, click được | Medium | Boundary | F1, CL15 |
| TC-NEW-05 | **Regression tab 配信済み (đã gửi)** — verify tab này không bị side-effect | Bot có broadcast đã gửi (trạng thái 配信済み); confirm Dev tab này có dùng `send_all.css` | 1. Vào tab `配信済み`<br>2. Hover số friend của broadcast đã gửi<br>3. Nếu popover có button recalc (logic phụ thuộc spec) → di cursor sang button | Popover hiển thị bình thường; KHÔNG có button recalc (tab đã gửi không recalc nữa) HOẶC nếu có thì click được; UI không lệch khung | Medium | Regression | T3 (extension of 4.3) |
| TC-NEW-06 | **Alternative root cause check** — Inspect DOM popover khi hover | DevTools open; setup giống TC-NEW-01 | 1. Hover số friend → mở DevTools → Elements tab<br>2. Verify popover element có: `z-index` ≥ z-index của parent container; `pointer-events: auto`; không parent nào có `overflow: hidden` cắt popover<br>3. Tab Computed → check `top` value của popover | Popover style: `top` đúng (sau fix), `z-index` đủ cao, `pointer-events: auto`. Không alternative root cause nào còn active. | Medium | Negative | BUG (AP-2 alt root check), F1 |
| TC-NEW-07 | **Tab switching state consistency** — Chuyển 配信予約 ↔ 下書き, popover không kế thừa state | Bot có broadcast ở cả 2 tab | 1. Tab `配信予約` → hover số friend → popover hiện → đóng popover (cursor ra ngoài)<br>2. Click sang tab `下書き`<br>3. Hover số friend ở tab 下書き<br>4. Click sang lại tab `配信予約`<br>5. Hover số friend | Mỗi lần hover ở mỗi tab → popover style render lại đúng, button click được, không bị "stuck" position từ tab trước | Medium | Regression | F1, T1, T2, CL3 |
| TC-NEW-08 | **Double click button recalculate** | Setup giống TC-NEW-01 | 1. Hover popover → di cursor xuống button<br>2. Click button **2 lần liên tiếp rất nhanh** (< 300ms) | API recalc được gọi **chỉ 1 lần** (verify Network tab DevTools), số friend cập nhật đúng, không duplicate request | Medium | Negative | F1, CL5 |
| TC-NEW-09 | **Staff có quyền broadcast** — refactor TC021 cho rõ scope CSS | Bot có 1 staff được phân quyền `broadcast`; login bằng staff | 1. Vào màn list send all tab 配信予約<br>2. Hover số friend → di cursor xuống button → click | Staff thấy popover + button **giống hệt admin chính**; button click được; số friend recalc đúng | Medium | Regression | F1, CL1 |
| TC-NEW-10 | **Reload màn list sau tạo broadcast** | Vừa tạo broadcast 配信予約 thành công | 1. Sau khi tạo broadcast xong → reload page (F5)<br>2. Vào tab 配信予約 → hover số friend → di cursor xuống button | Reload không gây lỗi CSS; popover/button hoạt động đúng | Low | Regression | F1, CL2 |

> Note: TC-NEW-01 cover BUG root cause flow → **bắt buộc có**. TC-NEW-02, 03 cover CL Compatibility → **bắt buộc**. TC-NEW-04, 05, 06, 07, 08, 09, 10 lấp các GAP/MAJOR còn lại.

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec — đây là pure CSS fix, không thay đổi behavior/spec.

(Không phát hiện mâu thuẫn giữa fix và LME-SYSTEM-SPEC section Broadcast.)

---

## 7. Checklist đã chạy

- [x] A. Coverage — **FAIL** (BUG 0 explicit, F1 RISK, T1/T2 RISK do Expected trống)
- [x] B. Chất lượng từng TC — **FAIL** (Expected trống, Title generic, Steps sparse)
- [x] C. Chất lượng bộ TC tổng thể — **FAIL** (Positive:Negative:Boundary:Regression ≈ 100:0:0:0; không có boundary; ORPHAN TC022)
- [x] D. Spec alignment — OK (không mâu thuẫn spec)
- [x] E. Hành chính — **PARTIAL** (TC ID OK, version "v1" OK, tester name chưa fill)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — CL1 partial, CL2/3/4/5/15 GAP, A.2 Compatibility **BLOCKER**, A.2 Regression partial
  - [x] F.2 Checklist job — N/A (CSS fix, không chạm job)
  - [x] F.3 Các tính năng chung — C.2 Send message N/A (không gửi msg thật, chỉ recalc count); C.7 Plan limits N/A; C.8 Sort N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<điền>` | `<điền>` |
| Tester | (đã đọc & hiểu feedback) | `<điền>` |
