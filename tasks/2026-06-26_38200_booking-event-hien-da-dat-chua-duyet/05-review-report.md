# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #38200 — [Booking Event] Đặt chỗ event hiển thị "đã đặt" phía user dù admin chưa duyệt (リクエスト制) |
| Reviewer (Leader) | `<Leader điền>` |
| Tester được review | `<tên — file 04 chưa điền>` |
| Ngày review | 2026-06-27 |
| Version TCs | v1 |
| Vòng review | Round 1 |

> **Spec reference**: Không có file `02-spec-reference.md` — dùng `templates/LME-SYSTEM-SPEC.md` tổng (FA-021 Event Booking) + checklist TC cũ "Improve 2026.05" (row 463-532) làm spec hành vi tham chiếu.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có MAJOR cần fix + confirm với Dev, review lại vòng 2.

**Lý do ngắn gọn**: Coverage cơ học của BUG/F1/D1/T1 đều đạt và bộ TC chất lượng tốt, NHƯNG (a) cả 2 file input auto-fill chưa được tester verify, (b) KH report symptom-only và **Lỗi ① (booking biến mất khỏi cả list đặt lẫn list hủy) không được fix bằng code** — cần confirm scope trước khi đóng, (c) thiếu cover **C.1 Bill tiền** dù booking-có-bill đi qua chính `saveAction`. Đây là rủi ro bỏ lọt đúng phần KH report → reject để chốt vòng 2.

---

## 2. Tóm tắt cho member

Bộ TC viết **đúng trọng tâm fix** và rất biết tiết chế — cover đủ 3 trigger field (SĐT/Tuổi/Tỉnh), thêm nhánh null (TC006), và cố ý KHÔNG re-test lại ma trận hiển thị status 1-7 (vùng không bị fix chạm) → tránh được over-coverage. Điểm cần fix chính không nằm ở chỗ thiếu TC cho code đã sửa, mà ở **scope**: KH báo 2 lỗi nhưng fix chỉ chạm Lỗi ② (crash) — Lỗi ① (khách ひろよ biến mất khỏi list) chưa có TC/confirm; và **transaction chưa được bọc** nên triệu chứng "đã đặt khi chưa duyệt" vẫn có thể tái phát từ lỗi khác (TC008 đang cover nhưng để Medium/Dev-only — cần nâng cấp). Sau khi đối chiếu 2 sheet feature "Event booking 1.0/2.0", phát hiện thêm: `saveAction` còn xử lý **approve request CHANGE** (status=6, vùng từng dính Bug #32366) và 3 side-effect khi approve (remind `user_event`, count slot/plan, bill) — đều có nguy cơ hỏng nếu crash → đã thêm TC-NEW-05/06/07. Bổ sung các TC này là đủ chốt.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — Undefined var `lineUserForHistory` → crash khi approve | Fix | — | TC001, TC007 | 2 | OK |
| F1 — `BookingEventController::saveAction` | Function | Direct | TC001/002/003 (Pos), TC008 (Neg), TC005/006 (Bound), TC004/009 (Reg) | 7 | OK |
| D1 — `b_user_booking.status` | Data | UPDATE | TC007 (verify), TC005/006 (Bound), TC008 (Neg), TC009/010 (Reg) | 6 | OK |
| T1 — Event Booking (FA-021) | Feature | High | TC007 (e2e), TC004/009/010/011 (Reg) | 5 | OK |

> Cơ học không có GAP cho impact đã được Dev list. Rủi ro nằm ở §3.5 (fix-shape) — coverage matrix bị "đánh lừa" vì impact F/D/T do AI tự list chỉ phản ánh **1 root cause đã sửa**, không phản ánh **symptom-class** KH report.

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề. TC010/TC011 chạm display nhưng được frame là regression sau approve (hợp lệ, không vi phạm AP-5). | Giữ nguyên |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Khác — restore biến bị rớt do bad-merge** (`$lineUserForHistory = LineUser::find(...)`). Không phải generic-catch / validation / race / cache / migration. |
| Trigger space cần cover | Biến dùng ở 3 case field: **-2 (SĐT) / -4 (Tuổi) / -6 (Tỉnh)** + nhánh `LineUser::find` trả **null** (friend đã hủy kết bạn). |
| Số trigger TCs hiện cover | **4/4** — TC001 (-2), TC002 (-4), TC003 (-6), TC006 (null). ✅ Trigger space đầy đủ. |
| KH report dạng | **Symptom-only** — KH chỉ mô tả hiện tượng ("hiển thị 予約済み dù chưa duyệt", "ひろよ biến mất khỏi list"), không có error code. Dev (AI) tái hiện 1 root cause qua stack trace. |
| Alternative root causes cần verify | (1) **Bất kỳ exception nào khác sau khi đổi status** (transaction chưa bọc) cũng tạo cùng symptom "đã đặt khi chưa duyệt" — TC008 cover một phần. (2) **Lỗi ① — ひろよ biến mất khỏi cả 2 list**: Dev xếp "data cũ, ngoài scope code" → **CHƯA có TC verify + chưa confirm có root cause riêng**. |
| Anti-patterns dính | **AP-2** (symptom-only KH report) — dính. **AP-6 (một phần)** — mục 3 mỏng, chỉ list chính `saveAction`, chưa rà các chỗ khác cùng bad-merge. AP-1/AP-4/AP-5 không dính. AP-3: T1 có regression đa trạng thái (deny/null/multi-field) → không dính. |

> Trigger space của **code đã sửa** = 4/4 đủ. Nhưng **symptom-class** KH report rộng hơn code fix → rủi ro thật nằm ở alternative root causes (xem §4.2).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- _(Không có BLOCKER thuần coverage — mọi impact Dev list đều có TC. Các rủi ro symptom-class được nâng ở MAJOR vì TC008/scope cần confirm chứ chưa phải GAP tuyệt đối.)_

### 4.2 Major (nên fix)

- `[MAJOR] SYMPTOM-ONLY (AP-2) — GAP-Lỗi①`: KH report 2 lỗi, fix chỉ chạm **Lỗi ② (crash → action không gửi)**. **Lỗi ① (khách ひろよ biến mất khỏi CẢ list đặt lẫn list hủy)** được Dev xếp "data cũ / ngoài scope code" nhưng **không có TC nào verify và chưa xác nhận có root cause riêng** (vd: status bị set sang giá trị không thuộc filter của cả 2 list). — **Đề xuất**: hỏi Dev xác nhận Lỗi ① có hoàn toàn do crash của Lỗi ② gây ra không; nếu không → tách ticket/điều tra riêng. Thêm TC-NEW-02 verify hiển thị list theo từng status.
- `[MAJOR] FIX-SHAPE — transaction yokoten chưa fix`: Cách fix chỉ khôi phục biến, **KHÔNG bọc transaction** quanh đoạn đổi status + lưu form_info + gửi notification (Dev tự ghi yokoten). Nghĩa là symptom "user thấy 予約済み dù chưa duyệt" **vẫn tái phát** nếu có exception khác sau khi status đã đổi. TC008 có cover nhưng để **Medium + Dev-only + mang tính giả định**. — **Đề xuất**: nâng TC008 lên **High**, bắt buộc chạy; ghi rõ với Leader/Dev rằng fix hiện tại là *necessary but not sufficient* cho symptom-class → cân nhắc bọc transaction.
- `[MAJOR] F.3 C.1 Bill tiền — chưa cover`: Event booking có course set tiền → luồng approve đi qua **chính `saveAction`** (sheet TC cũ row 480-500 cho thấy 支払い金額/決済方法/決済ステータス là phần lõi của booking). Approve booking **có bill + có field friend-info** là kịch bản thật chưa có TC. Member đã tự note nhưng để trống. — **Đề xuất**: thêm TC-NEW-01. *(Đối chiếu sheet "Event booking 1.0": "admin approve booking có bill tiền → tiến hành bill tiền, update amount + status_payment" → xác nhận approve-có-bill là luồng thật.)*
- `[MAJOR] Scope — bỏ sót approve REQUEST CHANGE / side-effect khi approve`: Đối chiếu 2 sheet feature đầy đủ ("Event booking 1.0" + "2.0"), `saveAction` xử lý **cả approve request CHANGE (status=6) lẫn approve request BOOKING (status=3)**. Khi user đổi friend-info rồi gửi request change, approve-change **cũng chạy `recordFriendInfoHistory`** → cùng nguy cơ crash `$lineUserForHistory`. Bộ TC hiện chỉ cover approve request **booking**. Ngoài ra approve có **3 side-effect** mà crash giữa chừng sẽ làm hỏng, chưa có TC: (a) tạo bản ghi remind `user_event` (sheet 1.0: "admin approve → thêm user_event"); (b) cập nhật count slot/plan 参加予定/承認待ち/remain (sheet 2.0); (c) **regression Bug #32366** — approve request change đã từng lỗi "ngày giờ để trống trong message" do booking gốc bị xóa (`sendActionBookingV1`). — **Đề xuất**: TC-NEW-05/06/07.
- `[MAJOR] Input auto-fill chưa verify — file 01`: `01-bug-task.md` auto-filled `2026-06-26 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" (dòng 90) **CHƯA tick**. Review chỉ có giá trị khi tester đã đọc lại detail Redmine. — **Đề xuất**: tester đọc lại description + 2 lỗi journal #123732, điền "Môi trường phát hiện", rồi tick checkbox.
- `[MAJOR] Input auto-fill chưa verify — file 03`: `03-dev-impact.md` auto-filled `by /new-task`, checkbox (dòng 17) **CHƯA tick**. Đặc biệt impact F/D/T do **AI Auto-fixbug tự đánh giá**, không phải dev người → F/D/T có thể thiếu (vd thiếu D cho `b_user_booking` các cột khác bị đổi, thiếu T cho luồng bill). — **Đề xuất**: tester verify lại 4 mục + tick checkbox trước khi review vòng 2.
- `[MAJOR] AP-6 (một phần) — mục 3 dev-impact mỏng`: Root cause là **bad-merge làm rớt dòng định nghĩa biến**. Nếu 1 dòng bị rớt, có thể có dòng/biến khác cũng bị rớt trong cùng merge mà chưa được rà. Mục 3 chỉ list lại chính `saveAction`. — **Đề xuất**: hỏi Dev rà toàn bộ diff của merge nghi vấn (commit `79c01515411` + nhánh merge cùng ngày) xem có biến mồ côi / dòng bị rớt khác trong `BookingEventController` hoặc file liên quan không.

### 4.3 Minor (có thể fix sau)

- `[MINOR] TC005 vs TC011 — chồng lấn nhẹ`: Cả hai chạm việc ghi/hiển thị friend info sau approve; TC005 focus "không ghi trùng", TC011 focus "hiển thị đúng giá trị". Chấp nhận được nhưng có thể gộp phần verify hiển thị để tránh chạy lặp.
- `[MINOR] AP-4 — không có PR/diff URL`: Mục "Commit / Pull Request" chỉ có commit hash `24d403e089` + branch `ai_fixbug_38200`, không có link diff để reviewer xem nhanh fix shape thực tế. Reviewer phải checkout branch. — Đề xuất Dev đính kèm link diff nếu có.
- `[MINOR] Tỷ lệ Type lệch Regression`: Regression 5/11 (~45%) so với gợi ý 20%. Member đã giải thích là chủ ý (bug regression do bad-merge) — hợp lý, ghi nhận, không bắt sửa.

### 4.4 Nit (gợi ý)

- `[NIT] CL-Func-5 double-click`: Cân nhắc 1 TC double-click nút 承認 ở lần thao tác cuối → verify không tạo bản ghi lịch sử trùng / không double-approve (liên quan luôn transaction yokoten). Xem TC-NEW-03.
- `[NIT] Field value rỗng`: TC hiện cover field-type trigger nhưng chưa cover **giá trị field rỗng/null** (friend bỏ trống SĐT) → recordFriendInfoHistory xử lý empty ra sao. Xem TC-NEW-04.

---

## 5. TCs đề xuất bổ sung

> Nguồn đối chiếu gap: spec/TC feature đầy đủ tại sheet **"Event booking 1.0"** + **"Event booking 2.0"** (spreadsheet `1r6N_p59...`), gồm Bug #31908 (item bắt buộc không lấy được info) và Bug #32366 (approve request change → message trống ngày giờ).

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | saveAction approve booking event **CÓ BILL** (course set tiền) + field friend-info: không crash, status + payment + action nhất quán | Event booking リクエスト制, course có setting số tiền (vd ¥100), form thu field SĐT. Friend đã request booking + đã nhập thẻ. | 1. Admin mở booking 来店リクエスト có bill.<br>2. Nhấn 承認.<br>3. Quan sát màn admin + 決済ステータス + LINE friend. | Không crash. Status → 来店予定; 決済ステータス → 決済成功 (¥100); action gửi tới friend. Không có tình trạng status đổi nhưng bill/action lỗi giữa chừng. | High | Positive | F1, D1, T1, C.1 |
| TC-NEW-02 | Verify hiển thị booking theo status ở list đặt chỗ vs list hủy (điều tra Lỗi ① ひろよ) | Tạo booking với từng status: 1/2/3/4/5/6/7 (và status bất thường nếu reproduce được). | 1. Với mỗi status, mở màn quản lý đặt chỗ event.<br>2. Kiểm tra booking xuất hiện ở list đặt / list hủy / không list nào. | Mỗi status hiển thị đúng list theo spec (sheet cũ). **Xác định status nào khiến booking biến mất khỏi CẢ 2 list** → confirm với Dev đó có phải root cause Lỗi ① không, có cần fix riêng. | High | Regression | BUG (Lỗi ①), D1 |
| TC-NEW-03 | Double-click 承認 booking event: không double-approve / không ghi lịch sử trùng | Booking event 来店リクエスト có field friend-info. | 1. Admin double-click nhanh nút 承認.<br>2. Kiểm tra status + modal 操作履歴 + lịch sử friend info. | Chỉ 1 lần approve có hiệu lực; status → 来店予定; modal 操作履歴 chỉ ghi 1 mục 予約リクエスト 承認; không ghi trùng friend info (liên quan transaction yokoten + CL-Func-5). | Medium | Boundary | F1, D1 |
| TC-NEW-04 | saveAction approve booking khi friend để **trống** field friend-info: recordFriendInfoHistory xử lý empty | Form thu SĐT nhưng không bắt buộc; friend request booking **bỏ trống** SĐT. | 1. Admin nhấn 承認.<br>2. Kiểm tra detail friend → friend info SĐT. | Không crash; friend info SĐT không bị ghi giá trị rỗng sai (hoặc ghi theo spec); status → 来店予定. | Low | Boundary | F1, C.3 |
| TC-NEW-05 | saveAction approve **REQUEST CHANGE** (status=6) của booking có field friend-info: không crash + message replace đúng ngày giờ (regression Bug #32366) | Event booking リクエスト制 (cho phép change phải đợi approve), form thu field SĐT/Tuổi/Tỉnh. User đã có booking approve, sau đó **gửi request change** (đổi slot + đổi friend-info) → tồn tại 2 bản ghi status=6. | 1. Admin mở detail **booking gốc** → nhấn 承認 (approve request change).<br>2. Lặp lại bằng cách mở **booking mới** → approve.<br>3. Quan sát màn admin + message gửi cho user. | Không crash `$lineUserForHistory`. Booking gốc bị xóa, booking mới status→1. Message gửi user **replace đầy đủ** event_name + ngày/giờ slot + số lượng + số tiền (lấy theo booking mới) — KHÔNG để trống ngày giờ (regression Bug #32366). | High | Regression | F1, D1, T1 |
| TC-NEW-06 | saveAction approve booking có field friend-info: bản ghi remind `user_event` được tạo (không mất do crash) | Event booking リクエスト制 có field friend-info, có setting remind. Friend đã request booking (status 3, **chưa** có user_event). | 1. Admin nhấn 承認.<br>2. Kiểm tra bảng remind / nhắc lịch event của friend (hoặc chờ tới giờ remind). | Sau approve thành công → **thêm 1 bản ghi user_event** cho friend (sheet 1.0: "admin approve booking → thêm user_event"). Trước fix, crash giữa chừng làm remind không được tạo. | Medium | Regression | F1, T1, C.2 |
| TC-NEW-07 | saveAction approve booking có field friend-info: count 参加予定/承認待ち/remain cập nhật đúng | Event booking リクエスト制, slot có max số người, có field friend-info. Friend gửi request booking → count đang nằm ở 承認待ち. | 1. Ghi nhận count 参加予定 / 承認待ち / remain trước approve.<br>2. Admin nhấn 承認.<br>3. Đối chiếu count sau approve. | Sau approve: số booking chuyển từ **承認待ち → 参加予定**, **remain giảm 1**. Trước fix, crash làm count đứng sai (đúng triệu chứng 参加予定 KH có thể quan sát). | Medium | Regression | F1, D1, T1 |

---

## 6. Spec update needed

- [x] Không cần update spec (fix là khôi phục hành vi đúng, không đổi spec).
- Lưu ý: spec hiển thị status 1-7 + modal 操作履歴 đã có ở sheet "Improve 2026.05" — nếu confirm Lỗi ① có status bất thường thì cần bổ sung định nghĩa hiển thị cho status đó.

---

## 7. Checklist đã chạy

- [x] A. Coverage — BUG/F1/D1/T1 đủ chiều, không GAP cơ học, không ORPHAN.
- [x] B. Chất lượng từng TC — rõ ràng, atomic, realistic (trừ TC008 mang tính giả định, đã note).
- [x] C. Chất lượng bộ TC — tỷ lệ lệch Regression (đã giải thích); priority phân bổ ổn (High 5 / Medium 6).
- [x] D. Spec alignment — không mâu thuẫn; TC cũ read-only giữ nguyên.
- [x] E. Hành chính — TC ID đúng format; file đúng folder; **tester name/version chưa điền** (member fill).
- [x] F. Base checklist LME
  - [x] F.1 Web: A.1 Function (CL-Func-5 double-click → NIT; CL-Func-2 reload — member tự verify). A.2 Non-function: Regression OK; Security/Compatibility N/A (không thêm URL/UI).
  - [x] F.2 Job: B.1 callback — fix không chạm callback job (đã revert nhầm handleOrderCallback). B.2 sync Java N/A.
  - [x] F.3 Tính năng chung: **C.1 Bill tiền → MAJOR thiếu** (TC-NEW-01). C.2 Send message (action approve) OK. C.3 Friend info OK. C.8 Sort N/A.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
