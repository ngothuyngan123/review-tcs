# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `<e.g. LME-1234>` |
| Reviewer (Leader) | `<tên>` |
| Tester được review | `<tên>` |
| Ngày review | `YYYY-MM-DD` |
| Version TCs | `v1 / v2 / ...` |
| Vòng review | `Round 1 / 2 / ...` |

---

## 1. Verdict

- [ ] **APPROVED** — TCs đạt, không cần chỉnh sửa
- [ ] **APPROVED WITH CHANGES** — Approve sau khi fix các issue MINOR (không cần review lại)
- [ ] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: `<1-2 câu>`

---

## 2. Tóm tắt cho member

<!-- 2-3 câu. Nêu điểm tốt + điểm cần fix. Viết friendly, mang tính coach chứ không phán xét. -->



---

## 3. Coverage Matrix

> Xem cách dùng trong [../../framework/coverage-matrix.md](../../framework/coverage-matrix.md)

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause) | Fix | — | | | |
| F1 — `<func>` | Function | Direct | | | |
| F2 — `<func>` | Function | Indirect | | | |
| D1 — `<data>` | Data | — | | | |
| T1 — `<feature>` | Feature | High | | | |

### ORPHAN TCs (nếu có)

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| | | | Remove / Map lại / Giữ vì... |

---

## 3.5 Fix-shape analysis (adversarial)

> Bắt buộc fill. Chi tiết: [../../framework/review-checklist.md](../../framework/review-checklist.md) §A.6 + [../../framework/anti-patterns.md](../../framework/anti-patterns.md).

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | `Generic catch-all / Specific code check / Validation / Race-condition / Cache / Migration / Soft-delete / Khác` |
| Trigger space cần cover | `<list các trigger condition cho fix shape này, vd: 6 Univapay error codes>` |
| Số trigger TCs hiện cover | `<số/tổng>` |
| KH report dạng | `Symptom-only / Có root cause cụ thể` |
| Alternative root causes cần verify | `<list, hoặc "N/A">` |
| Anti-patterns dính | `<AP-1 / AP-2 / ... hoặc "Không">` |

> Nếu trigger space cover < tổng → flag [BLOCKER] FIX-SHAPE trong §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

<!-- Format: [BLOCKER] <TC ID hoặc GAP-X>: <mô tả> — <đề xuất fix> -->

-

### 4.2 Major (nên fix)

-

### 4.3 Minor (có thể fix sau)

-

### 4.4 Nit (gợi ý)

-

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | | | | | | | |
| TC-NEW-02 | | | | | | | |

---

## 6. Spec update needed (nếu có)

<!-- Nếu bug fix đòi hỏi update spec cũ, ghi rõ ở đây để PM/Dev nắm. -->

- [ ] Không cần update spec
- [ ] Cần update spec — chi tiết:
  - Section:
  - Nội dung cần update:
  - Người chịu trách nhiệm update:

---

## 7. Checklist đã chạy

<!-- Check ✓ các mục đã pass trong framework/review-checklist.md -->

- [ ] A. Coverage
- [ ] B. Chất lượng từng TC
- [ ] C. Chất lượng bộ TC tổng thể
- [ ] D. Spec alignment
- [ ] E. Hành chính
- [ ] F. Base checklist LME (kiểm tra member đã tuân [checklist-lme.md](../../framework/checklist-lme.md) chưa)
  - [ ] F.1 Checklist web (A.1 Function CL1-CL22, A.2 Non-function)
  - [ ] F.2 Checklist job (B.1 Job callback, B.2 Job sync Java)
  - [ ] F.3 Các tính năng chung (C.1-C.8)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
