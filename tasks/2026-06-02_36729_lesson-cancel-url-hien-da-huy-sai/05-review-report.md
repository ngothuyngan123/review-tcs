# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#36729 — [Lesson] 「キャンセル用URL」 hiện 'đã hủy' nhưng thực tế thông báo chờ chưa cancel` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<chưa điền — TC fetch từ Sheet "Setting calendar", có khả năng Thanh Phương>` |
| Ngày review | `2026-06-02` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: Không có `02-spec-reference.md` riêng → dùng [LME-SYSTEM-SPEC tổng](../../templates/LME-SYSTEM-SPEC.md), không có spec riêng cho task này. Feature liên quan: Lesson (レッスン予約) — đăng ký nhận thông báo chờ cancel (キャンセル待ち通知受け取り).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: Coverage 12 TCs khá đủ chiều, NHƯNG (1) **TC009 đã NG** và mâu thuẫn trực tiếp với khẳng định của Dev ("nhánh notify không bị ảnh hưởng") → phải reconcile trước khi tin bộ TC; (2) cả `01` và `03` auto-fill từ Redmine chưa được tester verify; (3) KH không tái hiện được (symptom-only) nhưng TCs chỉ bám 1 root cause Dev tái hiện.

---

## 2. Tóm tắt cho member

Bộ 12 TCs viết tốt — có đủ positive (đăng ký lần đầu), negative (chặn đăng ký trùng), boundary/race (spam request đồng thời), và regression (slot khác / user khác / nhánh notify / đăng ký lại sau hủy). Điểm mạnh nhất là **TC006** (verify URL hủy cũ vẫn hoạt động) đánh trúng bản chất bug. Cần fix 3 điểm trước round 2: (1) làm rõ **TC009 đang NG** — đây là regression thật hay sai expected? Nó đối chọi với dev-impact; (2) tick verify cho `01`/`03` sau khi đọc lại Redmine; (3) bổ sung TC cho **root cause thay thế** (URL có bookingId hợp lệ nhưng cancel fail silent) vì KH không tái hiện được nên case thực tế của KH có thể khác.

---

## 3. Coverage Matrix

> Suy luận map từ Title / Precondition / Steps / Expected (file 04 không có cột Map to Impact). 1 TC có thể cover nhiều impact.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG — đăng ký trùng → 「キャンセル用URL」 bookingId rỗng → hiện 「予約が解除されました」 sai | Fix | — | TC002, TC003, TC004, TC006 | 4 | OK |
| F1 — `CalendarController@order` (Mobile) | Function | Direct | TC001–TC012 (toàn bộ qua API order) | 12 | OK |
| (D) — Không có data update (Dev xác nhận) | Data | — | TC004 (verify không update record) | 1 | OK |
| T1 — Đăng ký nhận thông báo chờ cancel (キャンセル待ち通知受け取り) trên màn booking | Feature | Medium | TC001, TC007, TC008, TC009, TC010 | 5 | OK |
| T2 — Luồng nhận / hủy qua 「キャンセル用URL」 | Feature | Medium | TC005, TC006, TC009, TC011 | 4 | **RISK** |

**Ghi chú status:**
- **T2 = RISK**: TC005 (hủy bằng URL hợp lệ — happy path) có note thực thi "*Hiện tại mở detail của booking này KHÔNG có nút cancel*", và TC006 note "*click url cũ mở được detail nhưng không có nút để cancel*". → Luồng hủy chính qua URL **chưa verify được** vì UI hiện không có nút cancel (khớp journal 2026-06-02: "hiện chưa có chức năng xóa 通知"). Cần Leader xác nhận expected của T2 trong điều kiện này.
- **BUG/F1/T1 = OK** về số lượng + chiều, nhưng xem §3.5 + §4 cho rủi ro ẩn.

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không phát hiện TC lạc chủ đề | Tất cả 12 TCs đều thuộc scope BUG / F1 / T1 / T2 |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Add check / guard** ("khi phát hiện đã tồn tại đăng ký chờ cancel → return ngay với status=false + message lỗi") — dạng `validate / thêm if / kiểm tra điều kiện` |
| Trigger space cần cover | Các biến thể thao tác đăng ký: (a) cùng slot trùng, (b) slot khác, (c) user khác cùng slot, (d) nhánh `bookingType='notify'`, (e) concurrent/spam cùng slot, (f) đăng ký lại sau khi đã hủy |
| Số trigger TCs hiện cover | **6/6** — (a)=TC002/003/004, (b)=TC007, (c)=TC008, (d)=TC009, (e)=TC012, (f)=TC010 → **đủ ≥ 4 boundary**, đạt yêu cầu fix-shape "add check" |
| KH report dạng | **Symptom-only** — KH chỉ thấy "URL hiện 予約が解除されました nhưng thực tế chưa hủy" + **"không tái hiện được"**. Root cause (đăng ký trùng → bookingId rỗng) là do QA/Dev tái hiện, không phải KH cung cấp |
| Alternative root causes cần verify | 「キャンセル用URL」 có **bookingId hợp lệ** nhưng action cancel **fail silent** (DB không update) → cũng hiện "đã hủy" mà thực tế chưa hủy. Hoặc URL trỏ tới record đã bị hủy/khác. **Cần hỏi Dev có path khác tạo cùng symptom không** |
| Anti-patterns dính | **AP-2** (symptom-only), **AP-4** (PR link trống). AP-1 không dính (fix là guard cụ thể, không phải generic catch). AP-6 không dính (mục 3 có nội dung) |

> Fix-shape "add check" về số biến thể đã **đủ** (6/6). Rủi ro chính KHÔNG nằm ở thiếu trigger mà ở: **(1) TC009 NG mâu thuẫn dev-impact** và **(2) symptom-only chưa cover alternative root cause** — xem §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE/REGRESSION — TC009 đang NG, mâu thuẫn dev-impact mục 3**: TC009 ("Kiểm tra nhánh `bookingType='notify'`") có **Status = NG**, note: *"Bug đang bị hiện message giống case đăng ký notify trùng"*. Nhưng `03-dev-impact.md` mục 3 khẳng định *"Nhánh `bookingType == 'notify'` giữ nguyên, không bị ảnh hưởng"* và mục 4.1 chỉ list 1 function. → **Có 2 khả năng, cả 2 đều phải xử lý trước khi approve**: (a) fix đã **gây regression** lên luồng đặt-lại-chỗ từ đăng ký notify (điều kiện return chặn nhầm cả nhánh notify hợp lệ) → đây là bug mới; hoặc (b) expected của TC009 sai. **Đề xuất**: trả TC009 về Dev xác nhận — nếu (a) thì fix lại điều kiện guard để loại trừ nhánh `bookingType='notify'` + cập nhật mục 4.1/4.3; nếu (b) thì sửa expected TC009. KHÔNG approve bộ TC khi còn TC NG chưa kết luận.

### 4.2 Major (nên fix)

- **[MAJOR] 01-bug-task auto-fill chưa verify**: `01` có `Auto-filled: 2026-06-02 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. → Yêu cầu tester đọc lại detail Redmine #36729 (description + journals + 2 ảnh đính kèm) và tick checkbox trước khi review có giá trị (steps reproduce lấy từ journal, cần tester confirm đúng).
- **[MAJOR] 03-dev-impact auto-fill chưa verify**: `03` có `Auto-filled: 2026-06-02 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** → F/D/T có thể chưa đầy đủ/mapping sai. Đặc biệt nghiêm trọng vì TC009 NG gợi ý mục 3/4.1 có thể **thiếu nhánh notify** trong scope ảnh hưởng. Yêu cầu tester + Dev verify lại.
- **[MAJOR] SYMPTOM-ONLY (AP-2): KH không tái hiện được → cần ≥ 2 plausible root causes**: `01` mục Mô tả bug ghi KH "*không tái hiện được vấn đề tương tự*". Root cause "đăng ký trùng → bookingId rỗng" là do QA tái hiện, **chưa chắc là case KH thực tế gặp**. → Bổ sung TC cho root cause thay thế: 「キャンセル用URL」 có bookingId **hợp lệ** nhưng cancel **fail silent** (xem TC-NEW-01). Hỏi Dev: ngoài đăng-ký-trùng, còn path nào khiến URL hiện "đã hủy" mà không hủy thật không?
- **[MAJOR] AP-4: PR/Commit link trống → không verify được fix shape thực tế**: `03` mục "Commit / Pull Request" = `<chưa có>`. Không đọc được diff để xác nhận điều kiện `return` có loại trừ đúng nhánh `bookingType='notify'` hay không (liên quan trực tiếp BLOCKER ở §4.1). → Yêu cầu Dev cung cấp PR link.
- **[MAJOR] CL21 — chưa verify hiển thị message lỗi mới phía LINE user**: Fix thêm message 「すでにキャンセル待ち通知受け取りの予約があるため、この受付枠は予約できません」. Không có TC nào verify message này **hiển thị đúng format** (dấu cách/ngoặc kiểu Nhật) trên màn LINE user. TC002 chỉ check "hiển thị message lỗi" chung. → Bổ sung verify nội dung + format message (xem TC-NEW-02).

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC viết dẫn bằng DB thay vì quan sát UI** (TC004, TC009): TC004 expected "status vẫn WAIT_CANCEL", TC009 "Check DB: không tạo booking mới mà update vào booking status=3". Theo quan điểm manual tester nên dẫn bằng **hiện tượng quan sát được** (message hiển thị, không nhận thêm thông báo) trước, DB chỉ là verify phụ. → Reword expected lấy UI/observation làm chính, DB làm bằng chứng bổ trợ.
- **[MINOR] Type / Priority để trống toàn bộ 12 TCs**: File 04 fetch từ Sheet không có 2 cột này. → Member điền Type (Positive/Negative/Boundary/Regression) + Priority để Leader đánh giá phân bổ chiều (gợi ý: TC002/006 = High; TC012 = Boundary).
- **[MINOR] Status "Test Bug" không thuộc dropdown chuẩn**: TC010/011/012 có Status = "Test Bug" (giá trị từ Sheet gốc). Dropdown chuẩn team: `OK / NG / Not test / NG -> Đã fix`. → Khi sync chuẩn hóa lại (có lẽ ý là "chưa test / cần test").

### 4.4 Nit (gợi ý)

- **[NIT] CL5 double-click**: TC012 (spam concurrent) đã cover phần lớn rủi ro double-click ở bước đăng ký. Có thể ghi rõ thêm 1 biến thể "double-click nút đăng ký 1 lần" cho khớp checklist LME CL5.
- **[NIT] CL2 reload**: Sau khi bị chặn đăng ký trùng, reload màn booking → verify trạng thái slot/đăng ký hiển thị đúng (không có TC, mức độ thấp).

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Cancel URL có bookingId hợp lệ nhưng cancel fail silent (alternative root cause) | User có 1 đăng ký WAIT_CANCEL hợp lệ; mô phỏng API cancel trả lỗi/không update (vd record đã bị xử lý song song) | 1. Mở 「キャンセル用URL」 hợp lệ<br>2. Thực hiện hủy trong điều kiện backend không update được record | KHÔNG hiển thị 「予約が解除されました」 khi DB chưa thực sự cancel; hiển thị lỗi phù hợp; user vẫn ở trạng thái còn nhận thông báo (không bị đánh lừa) | High | Negative | BUG (alternative), T2 |
| TC-NEW-02 | Verify nội dung + format message lỗi đăng ký trùng phía LINE user | User đã có WAIT_CANCEL cho slot A | 1. Đăng ký lại slot A (bị chặn)<br>2. Quan sát message trả về trên màn LINE user | Hiển thị đúng chuỗi 「すでにキャンセル待ち通知受け取りの予約があるため、この受付枠は予約できません」, đúng format Nhật (dấu cách/ngoặc theo design), không bị cắt/encode lỗi | Medium | Positive | BUG, T1, CL21 |
| TC-NEW-03 | Nhánh notify hợp lệ KHÔNG bị chặn nhầm sau fix (regression khẳng định) | Có booking WAIT_CANCEL với bookingId hợp lệ; slot trống mở ra | 1. Mở link booking từ thông báo (`bookingType='notify'`)<br>2. Thực hiện book slot A | Book thành công; update vào booking status=3 ban đầu (không tạo mới); **KHÔNG** hiện message "đã đăng ký trùng" | High | Regression | T1, T2 (gắn BLOCKER §4.1 — TC này chính là TC009 cần làm rõ NG) |

> TC-NEW-03 thực chất là làm rõ/định nghĩa lại expected của **TC009 đang NG** — đề nghị member + Dev thống nhất expected trước, rồi cập nhật TC009 thay vì thêm mới nếu trùng.

---

## 6. Spec update needed

- [x] Không cần update spec
- Ghi chú: Journal Redmine 2026-06-02 nêu hiện **chưa có chức năng xóa "thông báo chờ hủy" (キャンセル待ち通知)** và LME dự kiến chặn đăng ký trùng trong tương lai. Fix lần này chính là bước "chặn đăng ký trùng". → Không phải spec change, nhưng Leader nên note: expected luồng **hủy qua URL** (T2) hiện chưa có nút cancel → cần xác nhận behavior mong đợi với PM trước khi chốt TC005/TC006.

---

## 7. Checklist đã chạy

- [x] A. Coverage
- [x] B. Chất lượng từng TC
- [x] C. Chất lượng bộ TC tổng thể
- [x] D. Spec alignment (fallback LME-SYSTEM-SPEC, không có spec riêng)
- [ ] E. Hành chính (Tester name + Type/Priority chưa điền — xem §4.3)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — liên quan: **CL5** (double-click — TC012 cover phần lớn), **CL4** (thao tác liên tục Add→Add — TC002 cover), **CL21** (format message line user — **CHƯA cover**, §4.2), **CL13** (Line friend access link cho 「キャンセル用URL」 — mức độ thấp). CL2 (reload) chưa cover (§4.4 NIT).
  - [x] F.2 Checklist job — **không liên quan trực tiếp** (fix ở controller order, không chạm google sync/job retry). C.6 Google calendar: Lesson có sync nhưng fix không đụng → bỏ qua.
  - [x] F.3 Các tính năng chung — **C.2 Send message** liên quan: fix chặn "gửi lại action + 「キャンセル用URL」 thừa" → TC003 đã verify "không gửi message/URL mới". Đủ ở mức cần thiết cho phạm vi fix.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
