# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37061 — [Header/Menu] Hiển thị thời gian cập nhật limit và hiển thị theo định dạng 24h` |
| Reviewer (Leader) | `<Leader điền>` |
| Tester được review | `<member điền>` |
| Ngày review | `2026-06-09` |
| Version TCs | `v1 (fetched từ Sheet "Improve 2026/05/13" rows 280–293)` |
| Vòng review | `Round 1` |

> **Spec reference**: không có file `02-spec-reference.md` riêng → dùng `templates/LME-SYSTEM-SPEC.md` tổng. Member nên bổ sung 02 nếu có spec riêng cho hiển thị limit header.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: 2 TC (TC011, TC014) thiếu Expected → không chạy được. Core fix (12h→24h) chưa có TC boundary mốc giờ. Đánh giá ảnh hưởng của Dev sai (4.2 "Không có" data trong khi fix ghi field `bots.limit_message_loa_last_updated`; mục 3 trống; PR link trống). Cả 2 file input auto-fill chưa được tester verify.

---

## 2. Tóm tắt cho member

Bộ TC fetch từ Sheet cũ đã bao quát khá tốt các luồng hiển thị (header reload, summary message, change/add bot) và nhiều TC đã verify đúng `db: bots.limit_message_loa_last_updated` — điểm cộng. **Tuy nhiên** bộ TC đang thiếu đúng **trọng tâm của fix**: (1) không có TC nào kiểm tra **giá trị giờ biên** khi đổi 12h→24h (vd 5pm→17:00, 12am→00:00); (2) không có TC negative khẳng định **không còn hiển thị fix cứng 00:01**; (3) hai TC bị bỏ trống Expected. Ngoài ra cần đẩy ngược cho Dev: đánh giá ảnh hưởng (file 03) đang mâu thuẫn với chính cách fix về phần data. Fix các điểm này rồi review lại Round 2.

---

## 3. Coverage Matrix

> Map suy luận từ Title / Steps / Expected (file 04 không có cột Map to Impact).

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG — fix cứng 00:01 + format 12h | Fix | — | TC001 (24h), TC002 (time thật) | 2 | **RISK** — thiếu boundary giờ 24h + thiếu negative "không còn 00:01" |
| F1 — `fetchInfoBot()` (header) | Function | Direct | TC001, TC005, TC006 | 3 | **RISK** — có positive+boundary, thiếu negative (bot không có data) |
| F2 — `summaryMessageSend()` | Function | Direct | TC003, TC004, TC013, TC014 | 4 | OK (TC014 lỗi expected — xem §4.1) |
| F3 — `step2CheckFriend()` (change/add bot) | Function | Direct | TC009, TC010, TC011, TC012 | 4 | **RISK** — TC011 trống expected; thiếu negative |
| D1 — `bots.limit_message_loa_last_updated` (UPDATE) ⚠️ **KHÔNG có trong 4.2 Dev** | Data | — | TC002, TC003, TC005, TC007, TC008, TC010, TC012 | 7 | **RISK** — verify giá trị nhiều nhưng thiếu boundary null + thiếu cross-bot (CL11) |
| T1 — Fetch info bot header | Feature | Medium | TC005, TC006 | 2 | OK (smoke + click liên tiếp) |
| T2 — Màn Summary message | Feature | Medium | TC003, TC004, TC013, TC014 | 4 | OK |
| T3 — Change bot | Feature | Medium | TC011, TC012 | 2 | **RISK** — TC011 trống expected |
| T4 — Add bot | Feature | Medium | TC009, TC010 | 2 | OK (smoke) |
| T5 — Click btn reload thông tin bot | Feature | Medium | TC005, TC006 | 2 | OK |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề | Tất cả 14 TC đều thuộc scope BUG / F* / D* / T* |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Khác** — "Data persistence + display-format change": lưu timestamp get-limit vào bot, đổi hiển thị 12h→24h. (Không phải generic-catch / validation / race / cache / migration / soft-delete.) |
| Trigger space cần cover | Mốc giờ biên cho 24h convert: `00:00` (12am), `00:30`, `12:00` (12pm), `13:05` (1pm), `17:00` (5pm), `23:59`; trạng thái **null** (bot chưa từng get limit); giá trị cũ **00:01** phải biến mất |
| Số trigger TCs hiện cover | **1/8** — chỉ TC001 nói "format HH:MM 24h" chung chung, không cố định mốc giờ nào |
| KH report dạng | **Có root cause cụ thể** (Dev nêu: "chưa lưu thời gian get limit") — KHÔNG symptom-only → AP-2 không áp dụng |
| Alternative root causes cần verify | N/A |
| Anti-patterns dính | **AP-4** (PR link trống), **AP-6** (mục 3 dev-impact trống) |

> Trigger space cover 1/8 → flag **[MAJOR] FIX-SHAPE** §4.2 (không nâng BLOCKER vì có TC001 chạm format, nhưng thiếu nghiêm trọng boundary mốc giờ — trọng tâm fix).

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] TC011**: cột Expected **trống** (sheet gốc để trống) — "Check change bot free" không có tiêu chí pass/fail → không chạy được. Bổ sung Expected: "Sau khi change sang bot free, hiển thị đúng thời gian get-limit của bot free (định dạng 24h); db `bots.limit_message_loa_last_updated` của bot free đúng."
- **[BLOCKER] TC014**: cột Expected **trống** — "đứng tại summary → upgrade → reload màn summary" không có expected. Bổ sung: "Sau upgrade + reload, màn summary hiển thị thời gian get-limit MỚI (sau upgrade) đúng định dạng 24h, không giữ giá trị cũ."

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE**: thiếu TC boundary cho chuyển đổi **12h → 24h**. Toàn bộ bộ TC chỉ có TC001 nói "format HH:MM 24h" chung chung. Đây là 1 trong 2 nội dung cốt lõi của fix. Cần ≥ 1 TC seed các mốc giờ AM/PM/nửa đêm/giữa trưa và verify giá trị cụ thể (xem TC-NEW-01).
- **[MAJOR] DATA-IMPACT sai lệch (file 03 mục 4.2)**: Dev ghi data update = "Không có", nhưng cách fix là "lưu thời gian get limit vào bot" và **7 TC** verify `db: bots.limit_message_loa_last_updated`. → Thực tế có **D1 = `bots.limit_message_loa_last_updated` (UPDATE)**. Yêu cầu Dev cập nhật mục 4.2; bổ sung quan điểm regression/backup cho field này (CL liên quan update DB).
- **[MAJOR] [AP-6] Mục 3 dev-impact trống**: "Đã check và sửa các function sử dụng đến function/data vừa sửa" chỉ có heading, không nội dung. Yêu cầu Dev liệt kê **mọi nơi đọc** `limit_message_loa_last_updated` (có thể có màn/job khác đọc field này chưa được verify).
- **[MAJOR] [AP-4] PR / Commit link trống** (file 03): không verify được fix shape thực tế — 24h convert làm ở backend hay frontend? timezone xử lý ở tầng nào? Yêu cầu Dev cung cấp PR link.
- **[MAJOR] Negative bug cũ chưa cover**: không có TC nào khẳng định **không còn hiển thị fix cứng `00:01`** (1 trong 2 Actual của bug). Bổ sung TC-NEW-02.
- **[MAJOR] Boundary null (D1) chưa rõ**: TC009 "add bot mới chưa có time" nhưng Expected "Hiển thị time update sau khi tạo bot thành công" mâu thuẫn — bot mới CHƯA get limit thì lấy đâu ra time? Cần làm rõ trạng thái rỗng hiển thị gì (placeholder/"–"), và phải KHÔNG hiển thị `00:01`/giá trị rác. Xem TC-NEW-03.
- **[MAJOR] CL21 — đồng nhất format datetime**: fix đổi format hiển thị → bắt buộc verify format 24h **giống nhau** ở mọi nơi hiển thị (header web / màn summary / app nếu có). Hiện không có TC cross-surface. Xem TC-NEW-04.
- **[MAJOR] Input chưa được tester verify**:
  - `01-bug-task.md` auto-filled `2026-06-09 by /new-task`, checkbox "Tester verify auto-fill chính xác" **CHƯA tick** + Steps to reproduce để trống.
  - `03-dev-impact.md` auto-filled `2026-06-09 by /new-task`, checkbox **CHƯA tick**.
  → Review chỉ có giá trị tạm thời. Yêu cầu tester đọc lại Redmine #37061, bổ sung steps, tick 2 checkbox.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Thiếu Type / Priority / Precondition**: sheet gốc không có 3 cột này nên file 04 để trống. Member cần điền (đặc biệt Precondition: account, bot có/không limit, **timezone test**) để review chiều sâu chính xác.
- **[MINOR] Timezone không khai báo**: feature về hiển thị giờ nhưng không TC nào ghi rõ timezone (JST?). Bổ sung vào Precondition.
- **[MINOR] Bộ TC chưa chạy hết**: TC002–TC008 status `OK`, nhưng TC009–TC014 chưa có status (chưa test). Cần hoàn tất run trước khi kết luận pass.

### 4.4 Nit (gợi ý)

- **[NIT] CL5 double-click**: TC004 / TC006 ("click liên tiếp") nên nêu rõ mục đích chống duplicate (double-click ở lần get-limit cuối) để map đúng CL5.
- **[NIT]** TC013 gộp 2 expected ("hiển thị đúng bot đang chọn" + "get lại time khi bot upgrade") — có thể tách atomic.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` round tiếp theo. (TC cũ giữ nguyên, đây là TC delta.)

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Boundary format 24h — verify mốc giờ AM/PM/nửa đêm/giữa trưa | Bot có get-limit timestamp set ở các mốc: 00:00, 00:30, 12:00, 13:05, 17:00, 23:59 (timezone JST) | 1. Seed/trigger get-limit ở từng mốc giờ trên<br>2. Mở header + màn summary xem thời gian hiển thị | Hiển thị lần lượt: 00:00, 00:30, 12:00, 13:05, 17:00, 23:59 (24h). KHÔNG có AM/PM, KHÔNG hiển thị 5:00 cho 17:00 | High | Boundary | BUG, F1, D1 |
| TC-NEW-02 | Negative — không còn hiển thị fix cứng 00:01 | Bot get limit thành công ở giờ ≠ 00:01 (vd 15:30) | 1. Trigger job get-limit lúc 15:30<br>2. Mở header / màn summary | Hiển thị 15:30; **KHÔNG** hiển thị 00:01; db `bots.limit_message_loa_last_updated` = thời điểm thật | High | Negative | BUG, D1 |
| TC-NEW-03 | Boundary null — bot chưa từng get limit | Bot vừa add, **chưa** chạy job get-limit lần nào (timestamp null) | 1. Add bot mới<br>2. Mở header + màn summary trước khi job chạy | Hiển thị trạng thái rỗng theo design (vd "–" / ẩn), KHÔNG hiển thị 00:01 hay giá trị rác | High | Boundary | D1, T4 |
| TC-NEW-04 | CL21 — đồng nhất format 24h across surfaces | Bot có get-limit timestamp ở giờ PM (vd 18:45) | 1. Xem thời gian ở header web<br>2. Xem ở màn summary message<br>3. (Nếu có) xem ở app admin | Cả 3 nơi hiển thị **giống hệt**: 18:45 (24h), không lệch định dạng/timezone | Medium | Regression | T1, T2, CL21 |
| TC-NEW-05 | CL11 — đúng bot_id, không lẫn account | 2 bot (A, B) cùng admin, get-limit ở 2 thời điểm khác nhau | 1. Bot A get-limit 09:00, Bot B get-limit 21:00<br>2. Lần lượt chọn A rồi B, xem header/summary | Bot A hiển thị 09:00, Bot B hiển thị 21:00 — không lẫn; db update đúng `WHERE bot_id` | Medium | Boundary | D1, CL11 |

---

## 6. Spec update needed (nếu có)

- [x] Cần update spec / input Dev — chi tiết:
  - **File 03 mục 4.2**: thêm `D1 — bots.limit_message_loa_last_updated (UPDATE)` (hiện ghi sai "Không có").
  - **File 03 mục 3**: Dev điền danh sách caller đọc field timestamp.
  - **File 03 Thông tin**: bổ sung PR / Commit link.
  - **Design/spec hiển thị**: làm rõ trạng thái hiển thị khi bot **chưa từng get limit** (null) + timezone chuẩn.
  - Người chịu trách nhiệm: Dev `Tuấn Anh Trần` + tester verify auto-fill.

---

## 7. Checklist đã chạy

- [x] A. Coverage
- [x] B. Chất lượng từng TC
- [x] C. Chất lượng bộ TC tổng thể
- [x] D. Spec alignment (không có file 02 — dùng SPEC tổng)
- [x] E. Hành chính
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — liên quan: **CL21** (đồng nhất format datetime — GAP, xem TC-NEW-04), **CL11** (CRUD đúng bot — RISK, xem TC-NEW-05), **CL5** (double-click — partial TC004/006), **CL2** (reload — TC005/006), **CL7** (plan limit — TC007 chạm "có upgrade limit")
  - [x] F.2 Checklist job — **B.1 callback** không chạm. Job get-limit là job nội bộ (không phải Google sync) → CLJ01 không áp dụng. Lưu ý: TC002 phụ thuộc "job hàng ngày lấy limit" → cần cơ chế trigger job thủ công trên Dev.
  - [x] F.3 Các tính năng chung — **C.7 Plan limits** liên quan (limit message loa); **C.2 Send message** chạm gián tiếp qua màn summary message send. Member chưa tick mục nào trong file 04 → cần verify.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
