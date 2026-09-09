# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37109 — [Bill tiền tool] Ngày 強制解約 hiển thị khác nhau giữa từng trang` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<chưa điền — file 04 placeholder>` |
| Ngày review | `2026-06-09` |
| Version TCs | `fetch từ Sheet master (tab "Quản lý hợp đồng", row 1624~1642)` |
| Vòng review | `Round 1` |

> **Spec reference**: Folder không có `02-spec-reference.md` → dùng `templates/LME-SYSTEM-SPEC.md` tổng, không có spec riêng cho task này.
> **Nguồn file 04**: fetch từ Redmine #37109 Link TCs (tab checklist-format, KHÔNG phải bảng TC chuẩn 10 cột). TCs là read-only của Sheet master — mọi đề xuất sửa expected phải Leader + Dev confirm trước khi cập nhật Sheet.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER, cần fix và review lại

**Lý do ngắn gọn**: TC 1638 (nhánh bank transfer trên trang list) có **expected mâu thuẫn với cách fix** (vẫn ghi `expired_date + 7 ngày` trong khi fix đổi sang `expired_date_bank_transfer`), và **không có TC so sánh trực tiếp ngày 強制解約 giữa list ↔ detail** — chính là bug KH report. Hai điểm này khiến bộ TC hiện tại **không verify được fix** và có nguy cơ bỏ lọt bug.

---

## 2. Tóm tắt cho member

Bộ TC bao quát tốt UI/luồng của 2 trạng thái overdue (card + bank transfer) và có regression hợp lý cho detail-bill-fail (1642). **Tuy nhiên điểm cốt lõi của bug bị thiếu**: bug là "ngày 強制解約 khác nhau giữa list và detail" cho hợp đồng **銀行振込**, nhưng (1) chưa có TC nào đặt 2 trang cạnh nhau để verify ngày **giống nhau**, và (2) TC 1638 vẫn kỳ vọng `expired_date + 7 ngày` cho bank transfer — đúng bằng **behavior cũ (buggy)** mà fix đang sửa. Cần bổ sung TC so sánh cross-page + cập nhật expected nhánh transfer theo `expired_date_bank_transfer`, và làm rõ TC nào cover **banner (line 256)** vs **cột 延滞中 trong bảng danh sách (line 395)**.

---

## 3. Coverage Matrix

> Impacts từ `03-dev-impact.md`: BUG, F1 (`getOverDueDay`), T1 (banner 決済エラー bill/index), T2 (cột danh sách + 延滞中 inline bill/index). Mục 4.2: **không có data impact** (chỉ sửa hiển thị client-side).

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| **BUG** — list (bill/index) vs detail (bill/detail) hiển thị **cùng** ngày 強制解約 cho hợp đồng 銀行振込 (= `expired_date_bank_transfer`) | Fix | — | 1638 (expected SAI), 1641 (detail không assert giá trị); **không có TC so sánh cross-page** | ~1 | **GAP / BLOCKER** |
| **F1** — `getOverDueDay` nhánh **card** (`payment_method==1`) → `expired_date + 7` (không đổi) | Function | Direct | 1628 (list), 1629 (detail) | 2 | OK |
| **F1** — `getOverDueDay` nhánh **bank transfer** (`payment_method==2`) → `expired_date_bank_transfer` (**nhánh được FIX**) | Function | Direct | 1638 (expected SAI = `expired_date+7`), 1641 (detail, không assert) | 1 | **BLOCKER** |
| **T1** — banner cảnh báo 決済エラー (bill/index, line 256), ngày 強制解約 cho 銀行振込 | Feature | Medium | 1637 (UI generic), 1638 (date — expected SAI) | ~1 | **RISK / BLOCKER** |
| **T2** — cột danh sách hợp đồng + message 延滞中 inline (bill/index, line 395) | Feature | Medium | (không phân biệt rõ với banner; 1638 ambiguous) | 0–1 | **GAP / RISK** |
| Regression — detail-bill-fail (max-friend, `cardBillMaxFriend` không bị ảnh hưởng) | Regression (mục 3) | — | 1642 | 1 | OK |
| Regression — bill/detail (`overdueDate()` logic đúng, không đổi) | Regression (mục 3) | — | 1629 (card), 1641 (transfer) | 2 | OK |

### ORPHAN / Over-coverage TCs (AP-5)

| TC ID | Title | Lý do | Hành động đề xuất |
|---|---|---|---|
| 1630 | Check click text クレジットカードの変更 | Luồng đổi thẻ — không chạm code path `getOverDueDay` đã sửa | Giữ làm **regression trang bill/index** (NIT) |
| 1631 | Check click text プリペイド型カード (open lifecard) | Như trên | Giữ làm regression (NIT) |
| 1632 | check click button クレジットカードの変更 | Như trên | Giữ làm regression (NIT) |
| 1633 | Check màn change card — bill success | Luồng đổi thẻ + bill — không trực tiếp verify fix hiển thị ngày | Giữ làm regression (NIT) |
| 1634 | Check màn change card — bill fail | Như trên | Giữ làm regression (NIT) |

> 1626/1636 (điều kiện hiển thị overdue) = precondition setup; 1627/1637 (banner UI) = supporting. Không tính orphan.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Specific code check** — conditional 2 nhánh theo `payment_method` (`==2` → `expired_date_bank_transfer`; `==1` → `expired_date + 7`). KHÔNG phải generic catch-all. |
| Trigger space cần cover | (a) `payment_method==1` card → date = expired_date+7; (b) `payment_method==2` transfer → date = `expired_date_bank_transfer`; (c) boundary: transfer nhưng `expired_date_bank_transfer` null/empty/chưa set; (d) **mỗi nhánh × 2 vị trí hiển thị** (banner line 256 + cột danh sách line 395); (e) **mỗi nhánh × 2 trang** (list vs detail) phải KHỚP nhau |
| Số trigger TCs hiện cover | **~2 / 5** — card branch (1628 ✓), transfer branch list (1638 nhưng expected SAI). Thiếu: cross-page compare, boundary null, tách banner/list-column |
| KH report dạng | **Symptom-only** — KH chỉ nói "ngày 強制解約 khác nhau giữa từng trang", không nêu giá trị/nguyên nhân. Dev trace ra 1 root cause structural (rõ ràng, độ tin cậy cao). Rủi ro alternative root cause thấp, nhưng "**từng trang**" hàm ý ≥2 trang → cần confirm Dev đã liệt kê ĐỦ mọi nơi hiển thị ngày 強制解約 (xem MAJOR-6). |
| Alternative root causes cần verify | Thấp (root cause là logic hiển thị, không phải lỗi data/timing). Chủ yếu verify **scope đầy đủ các trang** hiển thị ngày này. |
| Anti-patterns dính | **AP-2** (symptom-only — light), **AP-3** (happy-path regression — thiếu edge state null), **AP-4** (PR link trống → không verify được fix shape thực tế). AP-1/AP-6 không dính. AP-5: 1630–1634 over-coverage (NIT). |

> Trigger space cover 2/5 → có [BLOCKER] FIX-SHAPE ở §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / TC1638**: Expected của TC1638 (nhánh **bank transfer** trên trang list) ghi `ngày cancel = expired_date + 7 ngày` — đây đúng là **behavior cũ (buggy)** mà fix đang sửa. Sau fix, `payment_method==2` phải hiển thị `expired_date_bank_transfer`. Giữ nguyên expected → tester sẽ đánh **fail một fix đúng**, hoặc tệ hơn là **không phát hiện bug**. → **Sửa expected TC1638** = "ngày 強制解約 = `expired_date_bank_transfer`, **khớp với trang 契約詳細**". *(TC từ Sheet master — Leader + Dev confirm trước khi cập nhật Sheet.)*

- **[BLOCKER] GAP-1 (BUG root cause)**: Không có TC nào **đặt trang list (bill/index) và trang detail (bill/detail) cạnh nhau** để verify ngày 強制解約 **giống nhau** cho cùng 1 hợp đồng 銀行振込 — đây chính là triệu chứng KH report ("hiển thị khác nhau giữa từng trang"). 1638 (list) + 1641 (detail) đứng riêng, không có bước so sánh, và 1641 không assert giá trị cụ thể. → Cần TC cross-page (xem TC-NEW-01).

- **[BLOCKER] FIX-SHAPE / Trigger space**: Nhánh được fix (`payment_method==2`) chỉ có 1 TC trên list (1638, expected sai) và không assert giá trị ở detail (1641). Nhánh fix thực chất **chưa được verify đúng**. → Cần verify nhánh transfer cho ĐỦ: list banner + list column + detail, tất cả = `expired_date_bank_transfer` (TC-NEW-01, TC-NEW-02).

### 4.2 Major (nên fix)

- **[MAJOR] T2 / TC ambiguous**: Fix chạm **2 vị trí** trên bill/index — banner 決済エラー (line 256) và cột 延滞中 trong bảng danh sách (line 395). TC1638 "Check hiển thị ngày cancel hợp đồng" **không rõ** cover banner hay cột danh sách. Cột 延滞中 inline (T2) gần như **không có TC riêng**. → Tách rõ TC cho banner vs cột danh sách (TC-NEW-03).

- **[MAJOR] SYMPTOM-ONLY / Scope các trang**: KH nói ngày khác nhau "**giữa từng trang**" (ngụ ý ≥2 trang). Dev chỉ xử lý bill/index vs bill/detail (+ loại trừ detail-bill-fail). → Hỏi Dev: còn nơi nào khác hiển thị ngày 強制解約 không (vd app mobile, CSV export, message remind/notification gửi LINE user, email)? Nếu có → cần TC cho các nơi đó.

- **[MAJOR] FORMAT (CL21)**: Mục 2 ghi fix trả `expired_date_bank_transfer` **định dạng `YYYY/MM/DD`**, nhưng format hiển thị hiện tại trên list là `〇月〇日` (xem expected 1628/1629). → Cần TC verify format ngày hiển thị trên banner + cột danh sách **đúng design** (không lẫn `YYYY/MM/DD` với `〇月〇日`), nhất quán giữa list ↔ detail. (Map CL21 — format datetime hiển thị phía user.)

- **[MAJOR] Boundary / AP-3**: Nhánh `payment_method==2` nhưng `expired_date_bank_transfer` **null / empty / chưa set** (admin/bank chưa nhập) → `getOverDueDay` trả gì? Không có TC. → Thêm boundary TC (TC-NEW-04).

- **[MAJOR] AP-4 / PR link trống**: Mục "Commit / Pull Request" = `<chưa có>`. Không thể đọc diff để verify fix có thực sự chỉ phân nhánh `payment_method` (không side-effect nhánh card). → Yêu cầu Dev cung cấp PR link để verify fix shape thực tế.

- **[MAJOR] Auto-fill chưa verify (file 01)**: `01-bug-task.md` "Auto-filled: 2026-06-09 by /new-task" nhưng checkbox "Tester verify auto-fill chính xác" **CHƯA tick**. → Tester đọc lại Redmine #37109 (description + journal #120574) và tick checkbox trước khi review có giá trị chính thức.

- **[MAJOR] Auto-fill chưa verify (file 03)**: `03-dev-impact.md` "Auto-filled: 2026-06-09 by /new-task" nhưng checkbox **CHƯA tick**. F1/T1/T2 có thể chưa đầy đủ. → Tester verify + tick checkbox.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Member checklist trống**: File 04 phần "Thông tin" (Tester/Ngày/Version) và "Member tự check" / "Base checklist LME" để placeholder → không xác nhận được member đã base checklist LME (đặc biệt CL20/CL21, C.1 Bill tiền). → Member điền trước round 2.

- **[MINOR] TC không assert giá trị (1627/1637/1641)**: "Check UI" / "hiện đúng ngày cancel" chung chung, không nêu giá trị đo lường được. → Bổ sung giá trị cụ thể vào expected.

### 4.4 Nit (gợi ý)

- **[NIT] AP-5 over-coverage**: 1630–1634 (luồng đổi thẻ) không trực tiếp verify fix hiển thị ngày — giữ làm regression trang bill/index, gắn nhãn rõ là regression.
- **[NIT] Compatibility**: Fix là hiển thị UI client-side (JS) → nên smoke 1 TC trên Win + Mac (Chrome/Safari) cho banner/cột ngày 強制解約.

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Ngày 強制解約 KHỚP giữa list và detail cho hợp đồng 銀行振込 | Bot contract: `payment_method=2`, `status=1`, `expired_date < now` & `now - expired_date < 7 ngày`, `status_payment=5`, có set `expired_date_bank_transfer` ≠ `expired_date+7` | 1. Mở trang 契約情報・領収書 (bill/index), ghi lại ngày 強制解約 ở banner 決済エラー + ở cột danh sách. 2. Mở 契約詳細 (bill/detail) của cùng contract, ghi lại ngày 強制解約. 3. So sánh 3 giá trị. | Cả 3 = `expired_date_bank_transfer`, **giống hệt nhau** (đúng bug fix). KHÔNG còn lệch ngày. | High | Positive (BUG) | BUG, F1(transfer), T1, T2 |
| TC-NEW-02 | bill/index hiển thị `expired_date_bank_transfer` cho 銀行振込 (không phải +7) | Như TC-NEW-01, đặc biệt `expired_date_bank_transfer` khác rõ `expired_date+7` (vd lệch 3 ngày) | 1. Mở bill/index. 2. Đọc ngày 強制解約 ở banner và cột danh sách. | = `expired_date_bank_transfer`, **không** = `expired_date+7`. | High | Positive (BUG) | F1(transfer), T1, T2 |
| TC-NEW-03 | Tách verify banner (line256) vs cột 延滞中 danh sách (line395) — 銀行振込 | Như TC-NEW-01 | 1. Mở bill/index. 2. Verify ngày trong **banner 決済エラー** đầu trang. 3. Verify ngày trong **message 延滞中 inline ở cột bảng danh sách**. | Cả 2 vị trí đều = `expired_date_bank_transfer`, cùng format design. | High | Positive | T1, T2 |
| TC-NEW-04 | Boundary: 銀行振込 nhưng `expired_date_bank_transfer` null/chưa set | Bot contract `payment_method=2`, overdue, **chưa có** `expired_date_bank_transfer` | 1. Mở bill/index. 2. Quan sát ngày 強制解約 hiển thị. | Không crash / không hiển thị `Invalid Date` / `NaN` / trống bất thường; behavior xác định (Dev confirm: fallback ra sao). | Medium | Boundary | F1(transfer) |
| TC-NEW-05 | Regression nhánh card (`payment_method==1`) KHÔNG đổi sau fix | Bot contract `payment_method=1`, overdue, `status_payment=2`, `status_payment_fail != (0,5)` | 1. Mở bill/index + bill/detail. 2. Đọc ngày 強制解約. | = `expired_date + 7 ngày` ở cả 2 trang (giữ nguyên như trước fix), format `〇月〇日`. | High | Regression | F1(card) |
| TC-NEW-06 | Format ngày 強制解約 đúng design trên list (CL21) | Như TC-NEW-01 | 1. Mở bill/index banner + cột danh sách. 2. So sánh format với 契約詳細 và design. | Format hiển thị nhất quán đúng design (vd `〇月〇日`), không lộ `YYYY/MM/DD` raw từ `expired_date_bank_transfer`. | Medium | Positive | T1, T2, CL21 |

---

## 6. Spec update needed (nếu có)

- [x] Không cần update spec — fix làm trang list **đồng nhất** với logic trang detail (đã đúng spec). Chỉ cần xác nhận behavior nhánh `expired_date_bank_transfer` null (boundary TC-NEW-04) là behavior mong muốn.

---

## 7. Checklist đã chạy

- [x] A. Coverage — A.1 (BUG GAP), A.2 (F1 transfer BLOCKER), A.4 (T2 GAP), A.5 (orphan 1630–1634), A.6 (fix-shape)
- [x] B. Chất lượng từng TC — B.1 (expected chung chung 1627/1637/1641)
- [x] C. Chất lượng bộ TC tổng thể — thiếu boundary + compatibility
- [x] D. Spec alignment — không mâu thuẫn spec (fix theo logic detail đã đúng)
- [x] E. Hành chính — file 04 thiếu Tester/Version (MINOR)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **CL21** (format datetime, RELEVANT → MAJOR format); **CL20** (hủy hợp đồng — fix này chỉ HIỂN THỊ ngày 強制解約, không thực thi cancel → các check clear richmenu/hủy schedule **N/A**, nhưng nên confirm ngày hiển thị = ngày thực thi 強制解約); CL2 (reload) minor; Compatibility Win+Mac (NIT)
  - [x] F.2 Checklist job — **N/A** (fix client-side JS, không chạm job)
  - [x] F.3 Các tính năng chung — **C.1 Bill tiền** RELEVANT nhưng phần *Error scenarios ≥4 error type* **N/A** (đây không phải fix payment-gateway generic, chỉ là hiển thị ngày); C.7 plan / C.8 sort N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
