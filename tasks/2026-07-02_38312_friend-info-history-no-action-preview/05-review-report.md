# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#38312 — Khi lưu lịch sử thay đổi friend info chưa lưu được action preview` |
| Reviewer (Leader) | `<Leader verify>` (draft do Claude sinh) |
| Tester được review | Thanh Phương (nguồn TCs — Sheet "Task nhỏ + fix bug KH") |
| Ngày review | 2026-07-02 |
| Version TCs | v1 (fetch read-only từ Redmine Link TCs) |
| Vòng review | Round 1 |

> **Spec reference**: không có `02-spec-reference.md` riêng → dùng `templates/LME-SYSTEM-SPEC.md` tổng + `framework/checklist-lme.md` §C.3 (Friend info) + §A.1 (CL-Func-17 setting action). Không có spec riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR cần fix + xác nhận với Dev trước khi có giá trị review.

**Lý do ngắn gọn**: Bộ TC bao phủ **tốt** trục "loại info × thao tác admin" (booking/approve/edit/callback) cho **event booking** — cover được đúng bug root cause (cột action → プレビュー click được). Nhưng: (1) cả 2 file auto-fill **chưa được tester tick verify**; (2) mục 3 dev-impact (caller) **trống** → chưa loại được rủi ro các luồng booking khác (Lesson/Salon/Item/Form/multi-action) cùng gán friend info select+action **vẫn còn bug**; (3) **thiếu boundary** case action bị xóa (CL-Func-17).

---

## 2. Tóm tắt cho member

Bộ TC rất chắc ở phần lõi: bạn đã tách đủ **7 loại info** (name/email/sđt/tỉnh/text/select-no-action/select-có-action) × **4 thao tác** (booking mới / approve / edit / callback univapay), và điểm cộng lớn là expected của case select-có-action verify được cả **click ra preview** chứ không chỉ text 「プレビュー」 — đúng trọng tâm bug. Cần bổ sung 3 việc trước khi approve: **tick checkbox verify** 2 file auto-fill (01 + 03); **hỏi Dev** xem các màn booking khác (Lesson/Salon/Item/Form) gán friend info select-có-action có dùng chung code fix không (mục 3 đang trống nên chưa biết); và thêm **1 TC boundary** cho trường hợp action bị xóa sau khi setting.

---

## 3. Coverage Matrix

> TC ID = số thứ tự `#1..#48` trong `04-tc-list.md` (sheet dùng format phân cấp Main Function/Sub, không có TC-ID rời).

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause) — lịch sử friend info: value select có action → cột action = プレビュー click được | Fix | — | #8, #16, #24, #40, #48 (select-có-action, expected プレビュー + click); #2–7 (info khác → 設定なし) | 5 (+ đối chứng) | **RISK** (đủ positive; thiếu boundary "action bị xóa") |
| F1 — `handleOrderCallback` (callback univapay booking) | Function | Direct | #41–48 (Check job callback bill tiền booking) | 8 | **OK** (positive; edge callback fail/delay không liên quan fix) |
| F2 — `saveAdminBooking` (admin booking event) | Function | Direct | #1–24 (web: booking mới/approve/edit) | 24 | **OK** |
| D1 — Lịch sử friend info: cột action/preview (dev ghi "k có" — thực tế fix GHI data này) | Data | — | verify gián tiếp qua GUI click-preview tại #8,#16,#24,#40,#48 | 5 | **RISK** (dev-impact 4.2 mâu thuẫn; xem [MINOR]-1) |
| T1 — Admin booking | Feature | `<Dev không ghi mức>` | #1–40 (web + app) | 40 | **OK** |
| T2 — Booking event có callback univapay | Feature | `<Dev không ghi mức>` | #41–48 | 8 | **OK** (positive) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| #25–32 | App "Admin booking mới" (mọi loại info) | Status = **Reject** — "Ở app không có booking mới" → không áp dụng | Giữ để tài liệu hóa lý do N/A (không phải orphan thật). Không cần chạy. |

_Không có TC lạc chủ đề: toàn bộ #1–48 thuộc scope BUG / F1 / F2 / T1 / T2._

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Khác** — "Lưu preview action lịch sử friend info" = data-write + display fix (KHÔNG phải generic catch / validation / race / migration). |
| Trigger space cần cover | Các **loại friend info** (name/email/sđt/tỉnh/text/select-no-action/**select-có-action**) × các **entry point tạo lịch sử friend info có action** (event booking admin/callback = đã fix; **Lesson/Salon/Item/Form/multi-action/CSV/QR landing = CHƯA rõ**). |
| Số trigger TCs hiện cover | Loại info: **7/7** ✔ (cho event booking). Entry point: **2/≥7** ✖ (chỉ event booking admin + callback). |
| KH report dạng | **Có root cause cụ thể** (dev nêu rõ "chưa lưu preview action"; expected/actual rõ 設定なし↔プレビュー). → AP-2 **không dính**. |
| Alternative root causes cần verify | N/A (root cause rõ). |
| Anti-patterns dính | **AP-6** (mục 3 caller list trống) → kéo theo rủi ro sibling entry point. AP-1/2/3/4/5 không dính. |

> Fix shape không phải generic-catch nên KHÔNG áp quy tắc "≥3 trigger error code". Rủi ro chính là **phạm vi entry point**: fix chỉ áp cho event booking; các màn booking khác cùng pattern (gán friend info select-có-action → tạo lịch sử) chưa được xác nhận. Vì mục 3 trống, không trace được có dùng chung code hay không → phải hỏi Dev.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- _Không có BLOCKER trên các impact đã list (F1/F2 Direct + T1/T2 đều có TC positive cover)._ Lưu ý: nếu Dev trả lời rằng Lesson/Salon/Item/Form **dùng code riêng** (không chung với fix) và cũng gán friend info select-có-action → **nâng G-1 lên BLOCKER** (bỏ lọt bug ở feature cùng nhóm).

### 4.2 Major (nên fix)

- **[MAJOR] AP-6 / G-1 (caller list trống)**: `03-dev-impact.md` mục 3 chỉ ghi "Đã check function/data", **không liệt kê caller**. Fix chỉ nằm ở `saveAdminBooking` + `handleOrderCallback` (event booking). Friend info + action là **tính năng dùng chung** (checklist §C.3: nhiều nơi update). — **Fix**: hỏi Dev: các luồng **Lesson booking / Salon booking / Item / Form / multi-action / QR landing / CSV import** khi gán friend info **select value có action** có tạo lịch sử friend info bằng **cùng đoạn code đã fix** không? Nếu KHÔNG → cần fix + TC riêng cho từng luồng (xem TC-NEW-02).
- **[MAJOR] G-2 (thiếu boundary — CL-Func-17)**: Không có TC cho trường hợp friend info select value **đã setting action rồi XÓA action**. Theo CL-Func-17, màn preview action phải **không bị lỗi** khi xóa hết action. — **Fix**: thêm TC-NEW-01.
- **[MAJOR] G-3 (auto-fill 01 chưa verify)**: `01-bug-task.md` có `Auto-filled: 2026-07-02 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. Thêm nữa Redmine description **trống** (nội dung lấy từ journal) → rủi ro sót thông tin cao. — **Fix**: tester đọc lại journal Redmine #38312, xác nhận Steps/Expected/Actual rồi tick checkbox.
- **[MAJOR] G-4 (auto-fill 03 chưa verify)**: `03-dev-impact.md` `Auto-filled by /new-task`, checkbox "Tester verify" **CHƯA tick** → F/D/T có thể thiếu hoặc map sai. — **Fix**: tester verify mục 1–4 với Dev rồi tick.

### 4.3 Minor (có thể fix sau)

- **[MINOR]-1 (mâu thuẫn dev-impact 4.2)**: Mục 4.2 ghi "k có data update", nhưng cách fix ("lưu preview action lịch sử friend info") **có ghi data** vào bảng lịch sử friend info (cột action/preview). — **Fix**: Dev cập nhật 4.2 để phản ánh data được ghi (D1). TC hiện verify data qua **GUI click-preview** là đủ ở góc nhìn manual tester (không cần TC query DB).
- **[MINOR]-2 (range TC lệch — đã hiệu chỉnh)**: Redmine ghi `row 237~284` nhưng block #38312 thật là **242–290** (237–241 thuộc task khác; 284 cắt cụt nhóm callback). File 04 đã lấy đúng 242–290. — **Fix**: tester confirm lại với người viết rằng bộ 48 TC là đầy đủ, và sửa range trong Redmine cho lần sau.
- **[MINOR]-3 (thiếu cột Steps/Precondition)**: Sheet nguồn dùng format phân cấp, cột Steps/Precondition để trống (steps ngầm định qua Sub1/Sub2/Sub3). — **Fix**: chấp nhận được với format team, nhưng nên ghi Precondition rõ cho case "select value có setting action" (cần seed event + friend info select + action trước).

### 4.4 Nit (gợi ý)

- **[NIT]-1**: Nhóm callback (F1/T2) chỉ test **callback success**. Có thể thêm case callback **delay / re-callback trùng** (checklist §C.1 "delay của callback") — nhưng nằm ngoài trọng tâm fix preview action, ưu tiên thấp.
- **[NIT]-2 (TC-14 web↔app parity)**: TCs verify hiển thị lịch sử ở **web** (Detail friend). App (My page) cũng hiển thị friend info — cân nhắc smoke check cột action preview trên app nếu app có màn lịch sử tương ứng.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` (hoặc dùng `/sync-review-tc`) ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Lịch sử friend info khi action của value select **bị xóa sau khi setting** | Event booking có form link friend info dạng select; 1 value của select **đã setting action**, sau đó **xóa action** đó ở màn setting friend info | 1. Setting friend info select value có action. 2. Admin book cho user (gán value đó) → tạo lịch sử. 3. Vào màn setting friend info xóa action của value đó. 4. Mở Detail friend → Lịch sử thay đổi friend info → xem cột action của bản ghi cũ. 5. Click vào cột action (nếu còn プレビュー). | Màn lịch sử **không văng lỗi/exception**; cột action hiển thị đúng theo spec sau khi action bị xóa (設定なし hoặc preview rỗng); click không lỗi. (CL-Func-17) | High | Boundary | BUG, D1, CL-Func-17 |
| TC-NEW-02 | Lịch sử friend info action preview ở **các luồng booking khác** (Lesson/Salon/Item/Form/multi-action) | **CHỈ tạo sau khi Dev xác nhận** luồng đó gán friend info select-có-action. Mỗi luồng có form/multi-action link friend info select value có action | 1. Thực hiện luồng tương ứng (đặt Lesson/Salon, mua Item, trả lời Form, hoặc chạy multi-action) gán value select-có-action cho user. 2. Mở Detail friend → Lịch sử thay đổi friend info → cột action. 3. Click cột action. | Cột action hiển thị 「プレビュー」, click ra được preview action (giống event booking đã fix). Nếu hiển thị 設定なし → **là bug chưa fix ở luồng đó** → raise ticket riêng. | High | Regression | G-1 (AP-6), §C.3 Friend info |
| TC-NEW-03 | Regression: info **không có action** vẫn hiển thị 設定なし ổn định sau fix (mọi loại + nguồn) | Friend info các loại không setting action (name/email/sđt/tỉnh/text/select-no-action) | 1. Gán các info không-action qua event booking. 2. Mở lịch sử friend info → cột action. | Cột action hiển thị 「設定なし」 đúng, không bị đổi nhầm thành プレビュー (không regression ngược). | Medium | Regression | BUG, T1 |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec
- [ ] Cần update spec

> Không phát hiện mâu thuẫn spec. Chỉ đề nghị Dev cập nhật lại mục **4.2 dev-impact** (data ghi vào lịch sử friend info) cho khớp cách fix — không phải spec sản phẩm.

---

## 7. Checklist đã chạy

- [x] A. Coverage — matrix §3 (F1/F2/T1/T2 OK; BUG/D1 RISK do thiếu boundary)
- [x] B. Chất lượng từng TC — steps ngầm định qua phân cấp Sub, expected đo lường được (click preview). Thiếu Precondition rõ cho case action ([MINOR]-3)
- [x] C. Chất lượng bộ TC — cân bằng tốt ở trục info×thao tác; thiếu Boundary/Negative ([MAJOR] G-2)
- [x] D. Spec alignment — không mâu thuẫn (không có 02-spec-reference)
- [x] E. Hành chính — nguồn sheet OK; range đã hiệu chỉnh 242–290 ([MINOR]-2)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **CL-Func-17 (setting action)** liên quan trực tiếp → **thiếu** case xóa action ([MAJOR] G-2). CL-Func-8 (copy/preview) không áp dụng.
  - [x] F.2 Checklist job — B.1 Job callback: F1 handleOrderCallback là callback → có TC positive (#41–48); edge delay/trùng là [NIT]-1.
  - [x] F.3 Các tính năng chung — **§C.3 Friend info** liên quan trực tiếp: TCs cover nơi **update** (event booking) + 1 nơi **hiển thị** (lịch sử/Detail friend). Các entry point update khác (Lesson/Salon/Item/Form/multi-action/CSV) → [MAJOR] G-1. §C.1 Bill tiền (callback) → [NIT]-1.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<Leader verify draft này>` | |
| Tester | (đã đọc & hiểu feedback) | |
