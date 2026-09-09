# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #38208 — [Notify Setting] Thông báo đặt chỗ/hủy không xóa được (通知が消えない) |
| Reviewer (Leader) | `<Leader verify>` (draft by /review-tc) |
| Tester được review | (fetch từ Sheet Lesson row 714~737) |
| Ngày review | 2026-07-01 |
| Version TCs | v1 |
| Vòng review | Round 1 |

> **Spec reference**: dùng LME-SYSTEM-SPEC tổng (FA-019 Lesson Booking, FA-006 Notification Settings), không có `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Coverage bề rộng **rất tốt** (24 TC, cover đủ BUG/F/D/T + cross-platform web↔app), nhưng còn **6 MAJOR** cần xử lý trước merge: (1)(2) auto-fill 01/03 chưa được tester verify; (3) **phạm vi root cause** — `getBotId()` rỗng ảnh hưởng MỌI app flow xóa notify, fix chỉ patch 1 flow; (4) 4 TC Data Recovery đang "Not test" nhưng là lệnh DELETE prod; (5) TC-08 expected nghi vấn + steps trống; (6) thiếu boundary `is_confirm=1`.

---

## 2. Tóm tắt cho member

Bộ TC viết **rất chắc tay** — bạn đã bám đúng cơ chế fix (suy `botId` qua `calendar_management`), cover cả isolation (TC-06 không xóa nhầm notify reception/salon khác), regression web (TC-09/10/11) và đối chiếu web↔app đúng tinh thần cross-platform. Điểm cần siết: (a) **hỏi lại Dev** xem còn app flow nào khác cũng xóa `mobile_notify` qua `getBotId()` không (hủy/xóa 1 booking lẻ, salon) — vì đó mới là gốc lỗi, fix hiện chỉ vá luồng xóa slot; (b) 4 TC Data Recovery (TC-16→19) đang `Not test` mà lại là lệnh `DELETE` chạy prod — bắt buộc test an toàn trên dev/staging trước; (c) làm rõ expected + điền steps cho TC-08.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — `getBotId()` session rỗng → orphan notify khi xóa slot trên app | Fix | — | TC-01, TC-04, TC-07 | 3 | OK |
| F1 — `deleteFromApp()` (suy botId qua calendar_management) | Function | Direct | TC-01, TC-02, TC-06, TC-07, TC-14, TC-15 | 6 | OK |
| F2 — `Api\CalendarLessonController::deleteReception` (đổi route sang deleteFromApp) | Function | Direct | TC-01, TC-02, TC-08 | 3 | OK (implicit) |
| F3 — `delete()`/`deleteList()` web (giữ nguyên) | Function | Indirect | TC-09, TC-10, TC-11 | 3 | OK (regression) |
| D1 — `mobile_notify` DELETE (chỉ is_confirm=0) | Data | — | TC-01, TC-02, TC-05, TC-06 | 4 | **RISK** — thiếu boundary `is_confirm=1` |
| D2 — `calendar_course_bookings.deleted_at` (soft-delete) | Data | — | TC-01, TC-02, TC-05 | 3 | OK |
| D3 — orphan `mobile_notify` recovery (SQL 1 lần trên prod) | Data | — | TC-16, TC-17, TC-18, TC-19 | 4 | **RISK** — tất cả `Not test` |
| T1 — Lesson Booking (FA-019) | Feature | Medium | TC-01, TC-20, TC-21 | 3 | OK |
| T2 — Notification Settings (FA-006) — badge/list notify | Feature | Medium | TC-03, TC-04, TC-11, TC-22 | 4 | OK |
| T3 — Xóa slot Lesson trên Web (regression) | Feature | Low | TC-09, TC-10, TC-11 | 3 | OK |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC-23 | Xóa Reception có 100 booking (Performance) | Fix không chạm code path performance; over-coverage nhẹ (AP-5) | Giữ là nice-to-have, Priority Low |
| TC-24 | Xóa nhiều reception liên tiếp | Ranh giới: liên quan regression fix ("không phát sinh orphan") | Giữ — re-label Regression thay vì Performance |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Soft-delete + ghost-reference cleanup** kèm **specific code-check** (suy `botId` qua `reception.course_id → calendar_course.calendar_id → calendar_management.bot_id`). **KHÔNG** phải generic catch-all. |
| Trigger space cần cover | (1) booking đã cancel + notify `is_confirm=0` [main]; (2) botId resolve thành công / thất bại (calendar_management thiếu / bot_id null); (3) notify `is_confirm=1` của booking bị xóa; (4) **các app flow KHÁC cũng xóa notify qua getBotId** (hủy/xóa 1 booking lẻ, salon type=10) |
| Số trigger TCs hiện cover | 3/4 nhóm — (1)✔ TC-01/02, (2)✔ TC-07/14/15, (3)✘ thiếu, (4)✘ thiếu |
| KH report dạng | **Symptom-only** ("dù làm gì cũng không xóa được") — nhưng Dev + QA (Thanh Phương) đã reproduce root cause rõ ràng → rủi ro AP-2 **giảm** nhưng chưa loại trừ hết đường sinh orphan khác |
| Alternative root causes cần verify | App flow khác xóa booking/notify qua `getBotId()` rỗng: hủy/xóa **1 booking lẻ** trên app; xóa slot **Salon** (type=10). Fix chỉ patch `deleteReception` của Lesson. |
| Anti-patterns dính | **AP-2** (một phần — symptom-only, mitigated bởi root-cause confirm); **AP-5** (nhẹ — TC-23 over-coverage) |

> ⚠️ Fix shape soft-delete: câu hỏi bắt buộc "TC có test **ghost reference** ở nơi khác chưa?" → **ĐÃ CÓ** (TC-06 isolation, TC-13 booking đã soft-delete). Điểm hở duy nhất là **trigger nhóm (4)**: root cause `getBotId()` rỗng mang tính **hệ thống** (mọi app flow lọc notify theo bot_id), fix lại **cục bộ** 1 flow → xem §4.2 MAJOR SYMPTOM-ONLY.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- Không có GAP coverage tuyệt đối (mọi impact đều có ≥ 1 TC). Các rủi ro cao nhất được nâng lên MAJOR bên dưới.

### 4.2 Major (nên fix)

- **[MAJOR] SYMPTOM-ONLY / ROOT-CAUSE SCOPE — GAP-1**: Root cause `getBotId() = Session('current_bot_id')` rỗng trên app là lỗi **hệ thống** — ảnh hưởng **mọi** câu xóa `mobile_notify` lọc theo `bot_id` trong ngữ cảnh app, không riêng luồng xóa slot. Fix chỉ thêm `deleteFromApp()` cho `deleteReception`. **Đề xuất**: hỏi Dev list toàn bộ app endpoint có xóa/cập nhật `mobile_notify` qua `getBotId()` (hủy/xóa 1 booking lẻ trên app, xóa slot Salon type=10). Nếu có → cùng bug, cần TC (xem TC-NEW-01).
- **[MAJOR] AUTO-FILL chưa verify — 01-bug-task.md**: file auto-filled `2026-07-01 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** → yêu cầu tester đọc lại detail Redmine (description + steps + journal 124422) và tick trước khi review có giá trị.
- **[MAJOR] AUTO-FILL chưa verify — 03-dev-impact.md**: tương tự, checkbox verify **chưa tick** → F/D/T có thể chưa đầy đủ / mapping sai. Đặc biệt xác nhận đã dùng **đúng bản đánh giá mới** (journal 124139: suy botId qua `calendar_management`), không nhầm bản cũ 124019 (`$request['botId']`).
- **[MAJOR] TC-16→TC-19 (D3) "Not test" — GAP-2**: 4 TC Data Recovery đang status `Not test`, nhưng nội dung là lệnh **`DELETE mn FROM mobile_notify ...` chạy trên DB prod**. Chạy lệnh DELETE chưa verify an toàn = rủi ro xóa nhầm data thật. **Đề xuất**: bắt buộc execute TC-18 (notify hợp lệ không bị xóa) + TC-19 (type≠11 không ảnh hưởng) trên **dev/staging** với data seed (đếm trước/sau), trước khi human duyệt chạy prod (xem TC-NEW-03).
- **[MAJOR] TC-08 expected nghi vấn + steps trống — GAP-3**: TC-08 "reception có 1 booking chưa cancel → xóa sẽ báo lỗi, không cho phép xóa". Rule "không cho xóa reception khi có booking chưa cancel" **KHÔNG có** trong `03-dev-impact.md` mục 1/2, cũng không trong steps reproduce (repro là booking **đã** cancel). Đồng thời **cột Steps trống**. **Đề xuất**: confirm expected với Dev/spec; điền Steps rõ ràng; nếu rule không tồn tại → sửa expected.
- **[MAJOR] D1 thiếu boundary `is_confirm=1` — GAP-4**: expected TC-01/02 ghi "chỉ xóa notify `is_confirm=0`". Chưa có TC verify hành vi với notify **`is_confirm=1`** (đã đọc) của booking bị xóa — giữ nguyên hay xóa? Đây là boundary trực tiếp của điều kiện fix. **Đề xuất**: thêm TC-NEW-02.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Priority trống toàn bộ TC**: file 04 fetch từ Sheet không có cột Priority → 24/24 TC thiếu Priority. Member điền để phân bổ High/Medium/Low (đặc biệt TC recovery = High).
- **[MINOR] PR link trống (AP-4)**: mục "Commit / Pull Request" chỉ có commit `638308272a`, không có PR URL. Fix shape vẫn xác định được từ mục 2, nhưng nên bổ sung PR link để verify diff `deleteFromApp()` thực tế.
- **[MINOR] Trùng title TC-05 & TC-06**: cả 2 đều "Kiểm tra DB sau khi xóa reception". Đổi TC-06 → "Không xóa nhầm notify của reception/salon khác (isolation theo bot_id)".
- **[MINOR] Salon cùng pattern?**: Dev ghi "cân nhắc type=10 cho salon". Fix KHÔNG chạm code salon nên **không bắt buộc TC** (theo nguyên tắc root-cause-layer-focus), nhưng nên **hỏi Dev** salon delete trên app có cùng bug `getBotId()` không — nếu có là ticket riêng.

### 4.4 Nit (gợi ý)

- **[NIT] TC-23**: test perf xóa 100 booking không nằm trên code path đổi bởi fix — giữ như smoke nice-to-have, Priority Low.
- **[NIT] TC-14/TC-15**: nên ghi rõ expected đo lường được ("API trả HTTP 200, không 500, log warning `botId not found`") thay vì "xử lý an toàn / theo thiết kế".

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Xóa/hủy 1 booking lẻ trên App (không xóa cả slot) — verify notify không thành orphan | Reception có ≥ 2 booking; 1 booking có `mobile_notify` type=11 `is_confirm=0`; thao tác trên **App** | 1. Mở App<br>2. Hủy/xóa **1 booking** trong reception (không xóa reception)<br>3. Check DB `mobile_notify` + màn danh sách notify + badge | notify của **đúng booking** bị hủy được xóa (đúng bot_id suy từ calendar); notify booking khác giữ nguyên; badge giảm đúng; **không** phát sinh orphan | High | Negative/Regression | BUG (root-cause scope), F1 |
| TC-NEW-02 | Xóa reception khi booking có notify `is_confirm=1` (đã đọc) | Reception có 1 booking; booking có 1 notify `is_confirm=1` + 1 notify `is_confirm=0` | 1. App → xóa Reception<br>2. Check DB `mobile_notify` của booking | Đúng theo spec fix: chỉ notify `is_confirm=0` bị xóa; notify `is_confirm=1` **giữ nguyên** (hoặc theo behavior Dev confirm); không lỗi | Medium | Boundary | D1 |
| TC-NEW-03 | [Dev/Staging] Verify an toàn SQL recovery orphan trước khi chạy prod | DB dev seed: N notify type=11 orphan (booking đã soft-delete) + M notify type=11 **hợp lệ** (booking còn sống) + K notify type=10 salon | 1. `COUNT` trước theo type/is_confirm<br>2. Chạy đúng câu SQL recovery của Dev<br>3. `COUNT` sau + so khớp | Chỉ N orphan type=11 bị xóa; M notify hợp lệ **còn nguyên**; K notify type=10 **không bị đụng**; số liệu trước/sau khớp kỳ vọng | High | Data Recovery | D3 |
| TC-NEW-04 | (Nếu Dev confirm) Xóa slot Salon trên App — cùng pattern getBotId | Salon reception có booking + notify type=10 `is_confirm=0`; thao tác App | 1. App → xóa slot Salon<br>2. Check `mobile_notify` type=10 + badge | notify salon của booking bị xóa được dọn đúng bot_id; badge giảm đúng | Medium | Regression | BUG (scope mở rộng) |

---

## 6. Spec update needed

- [x] Không cần update spec (fix bám cơ chế nội bộ; behavior end-user không đổi ngoài việc dọn đúng orphan)
- Lưu ý PM/Dev: nếu quyết định **mở rộng fix** sang các app flow khác (TC-NEW-01/04) thì cần cập nhật phạm vi ticket.

---

## 7. Checklist đã chạy

- [x] A. Coverage — đủ bề rộng; RISK ở D1 (is_confirm=1), D3 (Not test)
- [x] B. Chất lượng từng TC — TC-08 steps trống; TC-14/15 expected chưa đo lường được
- [x] C. Chất lượng bộ TC — spread Type hợp lý; Priority trống toàn bộ; trùng title TC-05/06
- [x] D. Spec alignment — không mâu thuẫn LME-SYSTEM-SPEC (FA-019/FA-006)
- [x] E. Hành chính — tester/version chưa điền (file 04 fetch từ Sheet)
- [x] F. Base checklist LME:
  - [x] F.1 Web — **CL-Func-11** (CRUD đúng bot_id) ✔ TC-06/07; **CL-Func-10** (update/delete ảnh hưởng data) ✔ TC-04/06; **CL-Func-16** (xóa không để rác) ✔ D1; **TC-14 cross-platform Web↔App** ✔ TC-01..08 (app) + TC-09..11 (web); **TC-13** (trạng thái hợp lệ 否認/cancel) — liên quan TC-08 (đang nghi vấn)
  - [x] F.2 Job — không chạm job callback / Google sync → N/A
  - [x] F.3 Tính năng chung — **C.2 Send message**: fix chỉ **xóa** notify, không gửi tin (Dev ghi rõ "KHÔNG gửi tin") → không cần cover 12 job send; **C.8 Sort** N/A
  - **Cảnh báo**: file 04 (fetch từ Sheet) **chưa có** mục "Member tự check / Base checklist LME" điền → không xác nhận được member đã tự base checklist. Yêu cầu tester bổ sung.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<verify draft này>` | |
| Tester | (đã đọc & hiểu feedback) | |
