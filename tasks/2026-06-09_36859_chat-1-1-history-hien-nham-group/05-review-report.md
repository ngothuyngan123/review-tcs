# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#36859 — [Chat 1:1] Lịch sử chat 1:1 hiển thị nhầm thành nhóm LINE, tên user sai` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<member điền>` |
| Ngày review | `2026-06-09` |
| Version TCs | `v1` (fetched từ Sheet qua /new-task) |
| Vòng review | `Round 1` |

> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng (§Chat 1:1 / 1:1チャット), không có `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Coverage scenario rất rộng (không impact nào GAP), nhưng (1) input auto-fill chưa được tester verify nên chưa đủ tin cậy để review có giá trị; (2) các TC race-condition cốt lõi viết không executable cho manual tester ("Mock network delay" không có cách thực thi); (3) precondition trống 100% — không tái hiện được điều kiện bug (cần ≥2 hội thoại trong đó có 1 nhóm LINE `bot_line_user_id = null`).

---

## 2. Tóm tắt cho member

Bộ TC rất tốt về **độ phủ kịch bản** — bạn đã tách đúng 2 nhánh root cause (race condition của `refresh()` và lỗi điều kiện pagination của `loadFriend()`), có cả case nhóm LINE `bot_line_user_id = null` (TC019) là case "đắt" nhất. Điểm cần fix trước khi approve: **viết precondition cụ thể** (tài khoản nào, cần bao nhiêu hội thoại, hội thoại nào là nhóm LINE), **biến các TC race thành thực thi được** (chỉ rõ throttle network bằng DevTools), và **expected phải đo lường được** (ghi rõ "hiển thị tên 鈴音, KHÔNG hiển thị nhóm" thay vì "hiển thị đúng"). Cuối cùng nhờ tester đọc lại Redmine và tick 2 checkbox verify ở file 01 + 03.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause — hiển thị nhầm lịch sử/tên user) | Fix | — | TC003, TC005, TC006, TC013, TC019, TC040 | 6 | OK (xem §3.5 về executability) |
| F1 — `refresh()` (guard race condition theo conversation_id) | Function | Direct | TC003, TC004, TC005, TC006, TC007, TC008, TC009, TC010, TC011, TC012, TC040 | 11 | RISK — concurrency có test nhưng không executable (mock delay) |
| F2 — `loadFriend()` (điều kiện conversation_id thay cho id) | Function | Direct | TC017, TC018, TC019, TC020, TC021, TC022, TC029, TC030, TC033 | 9 | OK |
| (không có data impact — mục 4.2) | Data | — | N/A | — | N/A |
| T1 — Màn Chat 1:1 hiển thị đúng lịch sử + tên user | Feature | High | TC001, TC002, TC013, TC014, TC015, TC016, TC036, TC037, TC039, TC040 | 10 | RISK — expected generic "hiển thị đúng" |
| T2 — Chuyển nhanh hội thoại / nhóm LINE khi đang tải | Feature | High | TC003, TC004, TC005, TC006, TC007, TC008, TC012 | 7 | RISK — thiếu multi-tab, mock delay không thực thi |
| T3 — Scroll pagination friend list khi đang xem nhóm LINE | Feature | High | TC017, TC018, TC019, TC020, TC021, TC022 | 6 | OK |

### ORPHAN TCs (nếu có)

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| TC023, TC025, TC026, TC028 | Search friend / Clear search / Filter friend list / Clear filter (không gắn context "đang mở group") | Mục 3 dev-impact ghi nhánh search/lọc **không đổi** sau fix (vẫn tự chọn hội thoại đầu như cũ) → đây là regression-nhẹ, không trực tiếp cover F1/F2 | Giữ làm regression nhưng hạ Priority = Low; hoặc gộp vào TC024/TC027 (case có context group mới là điểm rủi ro thật) |

> TC024, TC027 (search/filter **khi đang mở group**) → giữ, map T3 (regression nhánh loadFriend khi current_friend là group).

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Race-condition** (fix (a): guard `requestedConversationId` trong `refresh()`) **+ Condition-fix** (fix (b): đổi `!current_friend.id` → `!current_friend.conversation_id` trong `loadFriend()`) |
| Trigger space cần cover | Race: (1) response cũ về **sau** khi đã đổi hội thoại; (2) response về **đảo thứ tự** (B trước A); (3) chuyển ≥3 hội thoại liên tục; (4) đa luồng gọi refresh() — getHistory / sau send / polling / loadFriend; (5) **multi-tab cùng bot**. Condition: hội thoại có `id` (friend, BotLineUser) vs `id = null` (nhóm LINE) khi scroll load more |
| Số trigger TCs hiện cover | Race **4/5** (thiếu multi-tab) — nhưng (1)(2) viết bằng "Mock network delay" **không executable** cho manual tester → coi như chưa verify chắc chắn. Condition **2/2** (TC019 nhóm null + TC021 friend) — OK |
| KH report dạng | **Symptom-only** — KH mô tả hiện tượng (lịch sử nhóm sai + tên user sai 「國本 康秀」), KHÔNG có error code/log; Dev tự tái hiện root cause |
| Alternative root causes cần verify | Dev đã chủ động tách **2** root cause (race + pagination) → tốt. **Còn nghi ngờ 1 nguồn nữa**: journal Redmine ghi bug **tái diễn sau khi tắt extension** và video cho thấy click nhóm này hiện nội dung nhóm khác → cần hỏi Dev có khả năng nguồn **socket message routing** (TC039/040 note "ở dev k có socket") hoặc cache phía server không. Hiện chỉ fix client-side JS. |
| Anti-patterns dính | **AP-2** (symptom-only, đã giảm nhẹ nhờ Dev tách 2 root cause); **AP-5** (over-coverage nhánh search/filter — TC023/025/026/028); AP-1/AP-3/AP-4/AP-6 không dính (fix không phải generic-catch; mục 3 đã list caller đầy đủ; có PR link Bitbucket #10351) |

> Race-condition fix shape **bắt buộc** có concurrency test executable. TCs có ý tưởng đúng (TC005/006) nhưng step "Mock network delay" không nói cách làm → §4.2 [MAJOR].

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- _Không có BLOCKER._ Mọi impact (BUG/F1/F2/T1/T2/T3) đều có ≥1 TC cover; nhánh concurrency có TC (chỉ thiếu executability — xếp MAJOR).

### 4.2 Major (nên fix)

- **[MAJOR] AUTO-FILL chưa verify (file 01)**: `01-bug-task.md` auto-filled `2026-06-09 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick — yêu cầu tester đọc lại detail Redmine #36859 (description + journals + attachment) và tick trước khi review có giá trị.
- **[MAJOR] AUTO-FILL chưa verify (file 03)**: `03-dev-impact.md` auto-filled `2026-06-09 by /new-task`, checkbox CHƯA tick — F1/F2/T1/T2/T3 có thể chưa đủ hoặc mapping sai; yêu cầu tester đọc lại Section "Đánh giá ảnh hưởng" trong Redmine và tick.
- **[MAJOR] FIX-SHAPE (race condition): TC003/TC005/TC006/TC040 không executable** — step "Mock network delay" / "Mở A → ngay lập tức mở B" không chỉ cách tái hiện race cho **manual tester**. Đây là các TC quan trọng nhất (verify guard `refresh()`). Fix: viết rõ step dùng **Chrome DevTools → Network → throttle "Slow 3G"** (hoặc Network conditions → custom delay) khi mở hội thoại A, rồi đổi sang B trước khi A load xong; expected = response A bị bỏ qua, panel giữ nguyên B.
- **[MAJOR] Precondition trống 100%** — cả 40 TC không có precondition. Bug chỉ tái hiện với điều kiện cụ thể: account có **≥2 hội thoại**, trong đó **≥1 nhóm LINE** (`bot_line_user_id = null`) và **≥1 friend 1:1**, danh sách friend đủ dài để **scroll sang page 2**. Fix: thêm precondition này cho nhóm TC race (TC003–012, 040) và pagination (TC017–022).
- **[MAJOR] Expected không đo lường được (T1)** — TC001/002/013/015/036/037 dùng "Hiển thị đúng lịch sử chat / tên đúng". Bug là **hiển thị NHẦM** nên expected phải đối chiếu rõ: vd TC013 → "Tên hiển thị là 鈴音 (tên friend đang chọn), KHÔNG phải 國本 康秀; lịch sử là của 鈴音, KHÔNG phải nhóm". Fix: ghi giá trị kỳ vọng cụ thể + giá trị KHÔNG được xuất hiện.
- **[MAJOR] SYMPTOM-ONLY + nghi nguồn thứ 3**: KH report symptom-only và journal ghi bug **tái diễn sau khi tắt extension**, video cho thấy click nhóm này ra nội dung nhóm khác. Hỏi Dev: ngoài 2 root cause client-side, có khả năng **socket message routing / cache server** gây cùng hiện tượng không? Nếu có → cần TC cho nguồn đó (xem TC-NEW-04).
- **[MAJOR] TC036–TC040 thiếu Steps** — chỉ có scenario + expected, cột Steps trống → 2 tester chạy ra 2 kết quả khác. Fix: bổ sung steps tuần tự.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Cột Type / Priority trống toàn bộ 40 TC** — không phân loại Positive/Negative/Boundary/Regression và High/Medium/Low. Khó đánh giá tỷ lệ chiều test. Fill theo template (TC race = Boundary, TC031–035 = Regression, TC001/002/029/030 = Positive).
- **[MINOR] Status cột Sheet là "Test Bug"/"OK"** — không khớp dropdown chuẩn team (OK/NG/Not test/NG→Đã fix). Khi sync về master nên map "Test Bug" → "Not test".
- **[MINOR] TC005/TC006 trùng mục đích với TC003** sau khi viết lại executable — cân nhắc gộp để tránh 3 TC verify cùng 1 guard.

### 4.4 Nit (gợi ý)

- **[NIT][AP-5] TC023/025/026/028 (search/filter thuần)** — nhánh này Dev xác nhận không đổi sau fix; giữ làm regression Low hoặc gộp, tránh over-coverage.
- **[NIT] TC014/TC016 (avatar)** — bug không nhắc avatar; giữ làm regression nhẹ là hợp lý, không cần High.

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | [Multi-tab] Mở Chat 1:1 cùng bot trên 2 tab, thao tác chéo | Cùng account, cùng bot mở 2 tab trình duyệt; có ≥2 hội thoại A (friend), B (nhóm LINE) | 1. Tab1 mở hội thoại A. 2. Tab2 mở hội thoại B. 3. Quay lại Tab1 scroll/refresh. 4. Quay Tab2 scroll/refresh | Mỗi tab giữ đúng hội thoại của mình; không tab nào bị nhảy/hiển thị nhầm lịch sử hay tên user của hội thoại tab kia | Medium | Boundary | F1, T2 |
| TC-NEW-02 | [Race executable] Response hội thoại A về muộn sau khi đã chuyển sang B (throttle thật) | Account có friend A + friend B, mỗi người có lịch sử chat khác nhau | 1. DevTools → Network → "Slow 3G". 2. Click mở A. 3. Khi A đang loading (spinner), click ngay sang B. 4. Đợi cả 2 response về | Panel hiển thị **chỉ** lịch sử + tên của B; response cũ của A bị guard bỏ qua, KHÔNG ghi đè panel B | High | Boundary | BUG, F1, T2 |
| TC-NEW-03 | [Reproduce KH] Nhóm LINE `bot_line_user_id=null` → scroll load more không nhảy hội thoại | Account có ≥1 nhóm LINE (id=null) đang đứng đầu vùng nhìn + danh sách friend > 1 page | 1. Mở 1 nhóm LINE. 2. Scroll danh sách friend xuống cuối để load page 2. 3. Quan sát panel | Panel vẫn giữ nhóm LINE đang chọn; KHÔNG bị reset về friend đầu list; tên + lịch sử không đổi sang hội thoại khác (đúng bug KH 鈴音/國本 康秀) | High | Boundary | BUG, F2, T3 |
| TC-NEW-04 | [Alt root cause] Friend A và nhóm B cùng nhận message mới qua socket khi đang xem A | (Cần env có socket — Staging/Prod) Đang mở hội thoại friend A | 1. Mở A. 2. Cho A và nhóm B cùng gửi message tới bot gần như đồng thời. 3. Quan sát panel A | Panel A chỉ nhận message của A; message của B không chèn vào panel A; last_message của B cập nhật ở list, không lẫn vào A | High | Negative | BUG (alt — chờ Dev confirm) |

> TC-NEW-04 chỉ thêm nếu Dev confirm có nguồn socket/server (xem [MAJOR] SYMPTOM-ONLY §4.2). Nếu Dev khẳng định thuần client-side → giữ ở dạng regression, không bắt buộc.

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec — đây là bug fix logic client-side, không đổi business rule. Hành vi đúng (hiển thị đúng hội thoại đang chọn) đã là spec gốc.

---

## 7. Checklist đã chạy

- [x] A. Coverage — không impact nào GAP; F1/T1/T2 ở RISK do executability + expected
- [x] B. Chất lượng từng TC — fail: precondition trống, expected generic, TC036–040 thiếu steps
- [x] C. Chất lượng bộ TC tổng thể — Type/Priority trống; có over-coverage search/filter
- [x] D. Spec alignment — không mâu thuẫn
- [x] E. Hành chính — Tester/Version chưa điền ở file 04 (placeholder)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **CL3** (chuyển tab) & multi-tab: chưa cover (→ TC-NEW-01); **CL2** (reload sau thao tác): TC nên thêm bước reload verify; **CL15** (phân trang scroll lên đầu): liên quan F2 nhưng TC chỉ verify "không đổi hội thoại", chưa verify hành vi scroll — cân nhắc thêm. CL1 (staff account): TC037 đã cover ✓.
  - [x] F.2 Checklist job — N/A (fix thuần client-side JS, không chạm job)
  - [x] F.3 Các tính năng chung — C.2 Send message: TC011/012/039/040 chạm send + last_message ✓ (đúng mục C.2 "update last_message"); các mục C khác N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<Leader verify + ký>` | 2026-06-09 |
| Tester | (đã đọc & hiểu feedback) | |
